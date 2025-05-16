import sys, os, re, subprocess
import webbrowser
import qdarkstyle
from Command_Line import CommandHandler
from PySide6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
import json
import html
from PySide6.QtWidgets import QTabBar
import html2text
from PySide6.QtCore import QRegularExpression
import requests
import datetime
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtGui import QFontMetrics, QTextCharFormat, QFont
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
import markdown2
from PySide6.QtGui import QContextMenuEvent
import sqlite3
from markdown2 import Markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.formatters import HtmlFormatter
from PySide6.QtWidgets import QStyleFactory
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt

class FileMenuDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Menu")
        self.setStyleSheet("background-color: #fafafa;")
        self.setGeometry(200, 200, 400, 300)
        self.parent = parent
        
        icon_path = "ME_Icons/"

        # Main Layout
        main_layout = QVBoxLayout(self)
        
        # Top Frame
        top_frame = QFrame()
        top_frame.setStyleSheet("""background-color: #f2f2f2;
                                border-radius:8px;
                                padding:10px;
                                border: 1px solid rgb(234,234,234);
                                """)
        top_layout = QHBoxLayout(top_frame)
        
        button_style = """
            QPushButton, QToolButton {
                background-color: white;
                color: black;
                border: 1px solid rgb(234,234,234);
                border-radius: 15px;
                padding: 9px
            }
            QPushButton:hover, QToolButton:hover {
                background-color: #d6d6d6;
            }
        """
        
        # Left-aligned buttons
        button1 = QPushButton("")
        button1.setIconSize(QSize(50, 50))
        button1.setIcon(QIcon(icon_path + "open.png"))
        button2 = QPushButton("")
        button2.setIconSize(QSize(50, 50))
        button2.setIcon(QIcon(icon_path + "save.png"))
        button3 = QPushButton("")
        button3.setIconSize(QSize(50, 50))
        button3.setIcon(QIcon(icon_path + "saveas.png"))
        button4 = QPushButton("")
        button4.setIconSize(QSize(50, 50))
        button4.setIcon(QIcon(icon_path + "prepdf.png"))
        
        self.tool_button = QToolButton(self)
        self.tool_button.setText("Date & Time")
        self.tool_button.setIcon(QIcon(icon_path + "print.png"))
        # Create a dropdown menu
        menu = QMenu(self)
        menu.setStyleSheet("""
QMenu {
    
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 2px;
        }

        QMenu::item {
            background-color: transparent;
            color: black;
            padding: 4px;
            margin: 3px;
            border-radius: 5px;
        }

        QMenu::item:selected {
            background-color: #97B2ED;
            color: black;
        }

        QMenu::separator {
            height: 1px;
            background-color: #ccc;
            margin: 4px 0;
        }
        QMenu::item:disabled {
            color: grey;
        }
""")

        # Add actions to the menu
        action_code = QAction("Print Code", self)
        action_prev = QAction("Print Output", self)

        # Connect actions to functions (assuming self.text_edit exists)
        action_code.triggered.connect(self.print_markdown)
        action_prev.triggered.connect(self.print_preview)
        
        # Add actions to menu
        menu.addAction(action_code)
        menu.addAction(action_prev)

        # Set the menu to the tool button
        self.tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self.tool_button.setIconSize(QSize(50, 50))
        self.tool_button.setMenu(menu)
        self.tool_button.clicked.connect(self.print_preview)
        self.tool_button.setStyleSheet("""
                                       QToolButton {
                                       background-color: white;
                color: black;
                border: 1px solid rgb(234,234,234);
                border-radius: 15px;
                padding: 9px
            }
            QToolButton::menu-indicator {
                image: url("C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png");
                width: 16px;
                height: 16px;
                subcontrol-origin: border;
                subcontrol-position: center right;
                padding-right: 8px;
            }
            QToolButton::menu-button {
        border: none;
        width: 15px; /* Adjust size */
        background: white;
                                       border-top-right-radius:15px;
                                       border-bottom-right-radius:15px;
    }
                                       QToolButton::menu-button:hover {
        border: none;
        width: 15px; /* Adjust size */
        background: #dbdcde;
    }
    
    QToolButton::menu-arrow {
        image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png); /* Custom arrow image */
        width: 20px;
        height: 20px;
    }
""")
        # Right-aligned buttons
        right_button1 = QPushButton("Right 1")
        right_button1.setIcon(QIcon(icon_path + "right1.png"))
        right_button2 = QPushButton("Right 2")
        right_button2.setIcon(QIcon(icon_path + "right2.png"))
        
        # Apply styles
        button1.setStyleSheet(button_style)
        button2.setStyleSheet(button_style)
        button3.setStyleSheet(button_style)
        button4.setStyleSheet(button_style)
        right_button1.setStyleSheet(button_style)
        right_button2.setStyleSheet(button_style)
        
        # Adding left-aligned buttons
        top_layout.addWidget(button1)
        top_layout.addWidget(button2)
        top_layout.addWidget(button3)
        top_layout.addWidget(button4)
        top_layout.addWidget(self.tool_button)
        
        # Spacer to push right buttons to the right
        top_layout.addStretch()
        
        # Adding right-aligned buttons
        top_layout.addWidget(right_button1)
        top_layout.addWidget(right_button2)
        
        # Set layout for top_frame
        top_frame.setLayout(top_layout)
        
        # Bottom Frame with Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        bottom_frame = QFrame()
        bottom_frame.setStyleSheet("background-color: #fafafa;")
        bottom_layout = QVBoxLayout(bottom_frame)
        
        # Add some placeholder content to the bottom frame
        for i in range(10):
            label = QLabel(f"Content {i+1}")
            label.setStyleSheet("color: black; font-size: 14px; padding: 5px;")
            bottom_layout.addWidget(label)
        
        bottom_frame.setLayout(bottom_layout)
        scroll_area.setWidget(bottom_frame)
        
        # Adding frames to main layout
        main_layout.addWidget(top_frame)
        main_layout.addWidget(scroll_area)

    def print_markdown(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setDocName("Print Markdown")
        dialog = QPrintPreviewDialog(printer, self)
        dialog.setWindowTitle("Print Markdown")
        
        if dialog.exec():
            self.parent.text_edit.print(printer)  # Print text_edit contents

    def print_preview(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setDocName("Print Preview")
        dialog = QPrintPreviewDialog(printer, self)
        dialog.setWindowTitle("Print Preview")
        
        if dialog.exec():
            self.parent.preview_browser.page().print(printer, lambda success: None)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
"Markdown Files (*.md);;"
"CommonMark Files (*.commonmark);;"
"Markdown Extra Files (*.markdown);;"
"GitHub Flavored Markdown Files (*.gfm);;"
"Word Files (*.docx);;"
"LaTeX Files (*.tex);;"
"OpenDocument Text (*.odt);;"
"Rich Text Format (*.rtf);;"
"Plain Text (*.txt);;"
"All Files (*)", options=options)
        
        try:
            if file_name:
                self.current_file = file_name

                file_base_name = os.path.basename(file_name) 

                # Update the file label
                self.file_label.setText(f"<b>{file_base_name}</b> - {file_name}")
                self.file_label.setStyleSheet("""
background:#f2f2f2;
                                      border-radius:9px;
                                              border:1px solid #92d051;
                                      padding:1px;
font-size:14px;
""")

                # Open and display the file in the text edit
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.text_edit.setPlainText(file.read())
                
                self.update_preview()

                # Find the index of the file in the QFileSystemModel and highlight it in the tree view
                file_index = self.file_system_model.index(file_name)
                if file_index.isValid():
                    self.tree_view.setCurrentIndex(file_index)
                    self.tree_view.scrollTo(file_index)  # Scroll to the file in the tree view

            else:
                self.file_label.setText("•••")
                self.file_label.setStyleSheet("""
background:#f2f2f2;
                                      border-radius:9px;
                                      padding:1px;
font-size:14px;
""")
                self.update_file_status("Saved")
        except Exception as e:
            self.file_label.setStyleSheet("""
    background:#f2f2f2;
    border-radius:9px;
    border:1px solid red;
    padding:1px;
    font-size:14px;
""")
            QTimer.singleShot(5000, lambda: self.file_label.setStyleSheet("""
                background:#f2f2f2;
                border-radius:9px;
                padding:1px;
                font-size:14px;
            """))
            QMessageBox.critical(self, "Error", f"An error occurred while opening the file:\n{str(e)}")

    def mark_as_edited(self):
        # Call this method whenever the user edits the text
        self.update_file_status("Edited and Unsaved")

    def update_file_status(self, status):
        
        if status == "Saved":
            self.file_status_label.setText(status)
            self.file_status_label.setStyleSheet("""
                color: green;
                font-weight: bold;
            """)
        elif status == "Edited and Unsaved":
            self.file_status_label.setText(status)
            self.file_status_label.setStyleSheet("""
                color: red;
                font-weight: bold;
            """)
        elif status == "Unsaved":
            self.file_status_label.setText(status)
            self.file_status_label.setStyleSheet("""
                color: red;
                font-weight: bold;
            """)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = FileMenuDialog()
    dialog.show()
    sys.exit(app.exec())
