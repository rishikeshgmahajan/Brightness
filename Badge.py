import sys, os, re
import webbrowser
from ShieldsLicense import *
from Command_Line import CommandHandler
from PySide6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
import json
from PySide6.QtWidgets import QTabBar
from PySide6.QtCore import QRegularExpression
import requests
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

class BadgeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        def show_license_dialog():
            dialog = ShieldsLicenseDialog(self)
            dialog.exec()

        self.setWindowIcon(QtGui.QIcon("ME_Icons/badge.png"))
        self.setWindowTitle("Custom Badges")
        self.setGeometry(100, 100, 580, 600)
        self.setStyleSheet("""
background-color:#fafafa;
""")

        # Create a QTabWidget
        tab_widget =QTabWidget()
        tab_widget.setStyleSheet("""
                                 QPushButton{
                                 border-radius:7px;
                                 border:1px solid #ccc;
                          padding:3px;}
QPushButton:hover{
                          border:1px solid royalblue;
                          color:royalblue;
                          }
QTabWidget {
            border:none;
            margin-bottom:10px;
        }
        QTabWidget::pane { 
            background: white;
            border-radius: 10px;
        }
        QTabWidget::tab-bar {
            border-radius:4px;
            alignment: center;
            background:white;
        }
        
        QTabBar::tab {
            background: #fafafa;
            border: 0px solid lightgrey;
            padding: 5px;
            width:150px;
            border-radius:5px;
            margin-bottom:7px;
            margin:4px;
        }
                          QTabBar::tab:hover {
                          background:#fafafa;
            color:black;
            font-weight:bold;
            padding: 5px;
            border-radius:5px;
            margin-bottom:7px;
            margin:4px;
        }
        
        QTabBar::tab:selected {
        background:#f2f2f2;
        color:RoyalBlue;
        font-weight:bold;
            color:royalblue;
            padding: 5px;
            border-top-left-radius:5px;
            border-top-right-radius:5px;
            border-bottom-left-radius:5px;
            border-bottom-right-radius:5px;
            margin-bottom:7px;
            margin:4px;}
                                 """)

        # Tab 1: Scrollable badge icons area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
QScrollArea {
border:1px solid #ccc;
padding:3px;
border-radius:7px;
                                  background:white;
                                  }
        QScrollBar:vertical {
            background: #f2f2f2;
            width: 9px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #b0b0b0;
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical {
            background: #c6c6c6;
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: #c6c6c6;
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar:horizontal {
            background: #f2f2f2;
            height: 9px;
        }
        QScrollBar::handle:horizontal {
            background: #b0b0b0;
            min-width: 20px;
            border-radius: 4px;
        }
        QScrollBar::add-line:horizontal {
            background: #c6c6c6;
            width: 0px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            background: #c6c6c6;
            width: 0px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
""")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("""
        background:white;
        """)
        scroll_layout = QGridLayout()

        # Create buttons individually with icons only
        # Define the size for the buttons
        button_size = QSize(250, 90)  # Set your desired button size (3 times larger)

        # Button 1
        button1 = QPushButton()
        button1.setFixedSize(button_size)
        button1.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button1.setIcon(QtGui.QIcon("ME_Icons/standardB.png"))
        button1.setIconSize(button_size)  # Set icon size to button size
        button1.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; border-radius: 5px; line-height: 1; margin-bottom: 10px;">
        <span style="background-color: #555; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-left-radius: 5px; border-bottom-left-radius: 5px;">Standard</span>
        <span style="background-color: #007bff; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-right-radius: 5px; border-bottom-right-radius: 5px;">Badge</span>
    </div>
"""))
        scroll_layout.addWidget(button1, 0, 0)

        # Button 2
        button2 = QPushButton()
        button2.setFixedSize(button_size)
        button2.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button2.setIcon(QtGui.QIcon("ME_Icons/shadB.png"))
        button2.setIconSize(button_size)  # Set icon size to button size
        button2.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; border-radius: 5px; line-height: 1; margin-bottom: 10px;">
        <span style="background-color: #ff9800; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-left-radius: 5px; border-bottom-left-radius: 5px;">Shadow</span>
        <span style="background-color: #ff5722; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-right-radius: 5px; border-bottom-right-radius: 5px;">Effect</span>
    </div>
"""))
        scroll_layout.addWidget(button2, 0, 1)

        # Button 3
        button3 = QPushButton()
        button3.setFixedSize(button_size)
        button3.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button3.setIcon(QtGui.QIcon("ME_Icons/breakB.png"))
        button3.setIconSize(button_size)  # Set icon size to button size
        button3.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; border-radius: 5px; line-height: 1; margin-bottom: 10px;">
        <span style="background-color: #f44336; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-left-radius: 5px; border-bottom-left-radius: 5px; transform: rotate(-10deg);">Diagonal</span>
        <span style="background-color: #e91e63; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-right-radius: 5px; border-bottom-right-radius: 5px; transform: rotate(10deg);">Text</span>
    </div>
"""))
        scroll_layout.addWidget(button3, 1, 0)

        # Button 4
        button4 = QPushButton()
        button4.setFixedSize(button_size)
        button4.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button4.setIcon(QtGui.QIcon("ME_Icons/alertB.png"))
        button4.setIconSize(button_size)  # Set icon size to button size
        button4.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px;">
        <span style="background-color: #FF5733; color: #FFF; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Alert</span>
        <span style="background-color: #C70039; color: #FFF; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Notification</span>
    </div>
"""))
        scroll_layout.addWidget(button4, 1, 1)

        # Button 5
        button5 = QPushButton()
        button5.setFixedSize(button_size)
        button5.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button5.setIcon(QtGui.QIcon("ME_Icons/gradB.png"))
        button5.setIconSize(button_size)  # Set icon size to button size
        button5.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; border-radius: 5px; line-height: 1; margin-bottom: 10px;">
        <span style="background: linear-gradient(90deg, #00c6ff, #0072ff); color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-left-radius: 5px; border-bottom-left-radius: 5px;">Gradient</span>
        <span style="background: linear-gradient(90deg, #f6d365, #fda085); color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-right-radius: 5px; border-bottom-right-radius: 5px;">Badge</span>
    </div>
"""))
        scroll_layout.addWidget(button5, 2, 0)

        # Button 6
        button6 = QPushButton()
        button6.setFixedSize(button_size)
        button6.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button6.setIcon(QtGui.QIcon("ME_Icons/rouncorB.png"))
        button6.setIconSize(button_size)  # Set icon size to button size
        button6.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; border-radius: 15px; line-height: 1; margin-bottom: 10px;">
        <span style="background-color: #4CAF50; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-left-radius: 15px; border-bottom-left-radius: 15px;">Round</span>
        <span style="background-color: #8BC34A; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center; border-top-right-radius: 15px; border-bottom-right-radius: 15px;">Corners</span>
    </div>
"""))
        scroll_layout.addWidget(button6, 2, 1)

        # Button 7
        button7 = QPushButton()
        button7.setFixedSize(button_size)
        button7.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button7.setIcon(QtGui.QIcon("ME_Icons/outlB.png"))
        button7.setIconSize(button_size)  # Set icon size to button size
        button7.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px; border: 2px solid #4CAF50;">
        <span style="background-color: transparent; color: #4CAF50; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Outline</span>
        <span style="background-color: transparent; color: #4CAF50; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Badge</span>
    </div>
"""))
        scroll_layout.addWidget(button7, 3, 0)

        # Button 8
        button8 = QPushButton()
        button8.setFixedSize(button_size)
        button8.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button8.setIcon(QtGui.QIcon("ME_Icons/sharpgradB.png"))
        button8.setIconSize(button_size)  # Set icon size to button size
        button8.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px;">
        <span style="background: linear-gradient(90deg, #FF6B6B, #FFD93D); color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Sharp</span>
        <span style="background: linear-gradient(90deg, #6BCB77, #4D96FF); color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Edges</span>
    </div>
"""))
        scroll_layout.addWidget(button8, 3, 1)

        # Button 9
        button9 = QPushButton()
        button9.setFixedSize(button_size)
        button9.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button9.setIcon(QtGui.QIcon("ME_Icons/sharshadB.png"))
        button9.setIconSize(button_size)  # Set icon size to button size
        button9.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px;">
        <span style="background-color: #3F51B5; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Shadow</span>
        <span style="background-color: #5C6BC0; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Effect</span>
    </div>
"""))
        scroll_layout.addWidget(button9, 4, 0)

        # Button 10
        button10 = QPushButton()
        button10.setFixedSize(button_size)
        button10.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button10.setIcon(QtGui.QIcon("ME_Icons/stripB.png"))
        button10.setIconSize(button_size)  # Set icon size to button size
        button10.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px;">
        <span style="background: repeating-linear-gradient(45deg, #FFC107, #FFC107 10px, #FF5722 10px, #FF5722 20px); color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Striped</span>
        <span style="background: repeating-linear-gradient(45deg, #8BC34A, #8BC34A 10px, #CDDC39 10px, #CDDC39 20px); color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Badge</span>
    </div>
"""))
        scroll_layout.addWidget(button10, 4, 1)

        # Button 11
        button11 = QPushButton()
        button11.setFixedSize(button_size)
        button11.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button11.setIcon(QtGui.QIcon("ME_Icons/wiborB.png"))
        button11.setIconSize(button_size)  # Set icon size to button size
        button11.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px; border: 2px solid #333;">
        <span style="background-color: #333; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">With</span>
        <span style="background-color: #FF8C00; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Border</span>
    </div>
"""))
        scroll_layout.addWidget(button11, 5, 0)

        # Button 12
        button12 = QPushButton()
        button12.setFixedSize(button_size)
        button12.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button12.setIcon(QtGui.QIcon("ME_Icons/dottedB.png"))
        button12.setIconSize(button_size)  # Set icon size to button size
        button12.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px; border: 2px dotted #2196F3;">
        <span style="background-color: #E91E63; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Dotted</span>
        <span style="background-color: #673AB7; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Border</span>
    </div>
"""))
        scroll_layout.addWidget(button12, 5, 1)

        # Button 13
        button13 = QPushButton()
        button13.setFixedSize(button_size)
        button13.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button13.setIcon(QtGui.QIcon("ME_Icons/noradB.png"))
        button13.setIconSize(button_size)  # Set icon size to button size
        button13.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; line-height: 1; margin-bottom: 10px;">
        <span style="background-color: #555; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">No</span>
        <span style="background-color: #007bff; color: white; margin: 0; padding: 5px 10px; display: flex; align-items: center; justify-content: center;">Radius</span>
    </div1
"""))
        scroll_layout.addWidget(button13, 6, 0)

        button14 = QPushButton()
        button14.setFixedSize(button_size)
        button14.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 5px;
        """)
        button14.setIcon(QtGui.QIcon("ME_Icons/primhov.png"))
        button14.setIconSize(button_size)  # Set icon size to button size
        button14.clicked.connect(lambda: self.parent.text_edit.textCursor().insertText("""
\n<div style="display: inline-flex; align-items: center; justify-content: center; border-radius: 20px; padding: 10px 15px; margin: 5px; font-size: 14px; color: white; background: linear-gradient(45deg, #6200ea, #3700b3); cursor: pointer;" 
         onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 5px 15px rgba(0, 0, 0, 0.2)';" 
         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        Mouse Hover
    </div>
"""))
        scroll_layout.addWidget(button14, 6, 1)

        # Add the grid layout to the scroll content widget
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(scroll_area)
        tab1.setLayout(tab1_layout)

        # Tab 2: Badge customization form layout
        tab2 = QWidget()
        tab2.setStyleSheet("""
background:white;
                           border-radius:7px;
                           padding:3px;
""")
        form_layout = QFormLayout()

        # Required fields
        label_input = QLineEdit()
        label_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                                  border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")
        message_input = QLineEdit()
        message_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")

        # Optional fields with default values
        label_color_input = QLineEdit()
        label_color_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")
        message_color_input = QLineEdit()
        message_color_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")

        # ComboBox for Style (optional)
        style_input = QComboBox()
        style_input.setFixedWidth(450)
        style_input.setStyleSheet("""
QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
                font-size: 15px;
                height:20px;
                background-color: white;
                selection-background-color: transparent;
                selection-color: royalblue;
                padding: 3px;
                color:#4D4D4D;
                border-radius:7px;
                                  border:1px solid rgb(234, 234, 234);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                background:white;
                border-top-right-radius:7px;
                border-bottom-right-radius:7px;
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda.png);
                background-repeat: no-repeat;
                background-position: right 10px center;
            }
            QComboBox QAbstractItemView {
            border-radius:5px;
    }
    QComboBox QAbstractItemView::item {
    border-radius:5px;
    }
    QComboBox QAbstractItemView::item:selected {
    border-radius:5px;
    }
            QComboBox:hover {
                border:1px solid #ccc;
                selection-background-color: white;
                selection-color: white;
            }
""")
        style_input.addItems(["flat", "plastic", "flat-square", "for-the-badge", "social"])

        # Other optional fields
        logo_input = QLineEdit()
        logo_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")
        logo_color_input = QLineEdit()
        logo_color_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
     QComboBox                         padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")
        logo_width_input = QLineEdit()
        logo_width_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")
        link_input = QLineEdit()
        link_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")
        label_font_color_input = QLineEdit()
        label_font_color_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc1px solid #ccc;
                                  border-left:1px solid #ccc1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")
        message_font_color_input = QLineEdit()
        message_font_color_input.setStyleSheet("""
QLineEdit {
                             border-radius:5px;
                             border-top:1px solid #ccc;
                                  border-left:1px solid #ccc;
                                  border-right:1px solid #ccc;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
""")

        # Link label and copy button
        link_label = QLineEdit("Badge Link will appear here")
        link_label.setStyleSheet("""
background:white;
                                      border-radius:5px;
font-size:15px;
""")
        copy_button = QPushButton(QtGui.QIcon("ME_Icons/copy_tag_link.png"),"")
        copy_button.setFixedSize(30, 35)
        copy_button.setIconSize(QtCore.QSize(20, 20))
        copy_button.setStyleSheet("""
QPushButton{
                             border-radius:5px;
                             padding:5px;
                             border:1px solid #ccc;
                             font-size:12px;
                             background:white;
                                  margin-bottom:5px;
                             }
QPushButton:hover{
                             color:royalblue;
                             border:1px solid royalblue;}
""")

        # Adding fields to form layout
        form_layout.addRow("Label (Required):", label_input)
        form_layout.addRow("Message (Required):", message_input)
        form_layout.addRow("Label Color (Optional):", label_color_input)
        form_layout.addRow("Message Color (Optional):", message_color_input)
        form_layout.addRow("Style (Optional):", style_input)
        form_layout.addRow("Logo (Optional):", logo_input)
        form_layout.addRow("Logo Color (Optional):", logo_color_input)
        form_layout.addRow("Logo Width (Optional):", logo_width_input)
        form_layout.addRow("Link (Optional):", link_input)

        # Buttons
        create_badge_button = QPushButton(QtGui.QIcon("ME_Icons/tag_create.png"),"")
        create_badge_button.setIconSize(QtCore.QSize(40, 40))
        create_badge_button.setStyleSheet("""
QPushButton{
                             border-radius:5px;
                             padding:1px;
                             border:1px solid #ccc;
                             font-size:12px;
                             background:white;
                             }
QPushButton:hover{
                             color:royalblue;
                             border:1px solid royalblue;}
""")
        add_badge_button = QPushButton(QtGui.QIcon("ME_Icons/tag_add.png"),"")
        add_badge_button.setIconSize(QtCore.QSize(40, 40))
        add_badge_button.setStyleSheet("""
QPushButton{
                             border-radius:5px;
                             padding:1px;
                             border:1px solid #ccc;
                             font-size:12px;
                             background:white;
                             }
QPushButton:hover{
                             color:royalblue;
                             border:1px solid royalblue;}
""")

        shieldspowered = QPushButton("Powered by Shields.io")
        shieldspowered.setStyleSheet("""border: 0px solid #ccc;
        margin-top:10px; 
                                   background-color: white;
                                   color:grey;
                                   alignment: center;""")
        shieldspowered.clicked.connect(show_license_dialog)

        # Horizontal layout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(create_badge_button)
        buttons_layout.addWidget(add_badge_button)

        # Layout setup for tab 2
        link_layout = QHBoxLayout()
        link_layout.addWidget(link_label)
        link_layout.addWidget(copy_button)

        tab2_layout = QVBoxLayout()
        tab2_layout.addLayout(form_layout)      
        tab2_layout.addLayout(link_layout)      
        tab2_layout.addLayout(buttons_layout)    
        tab2_layout.addWidget(shieldspowered)

        tab2.setLayout(tab2_layout)

        # Add both tabs to the QTabWidget
        tab_widget.addTab(tab1, "HTML Badges")
        tab_widget.addTab(tab2, "Custom Badges")

        # Set up the main layout of the self
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(tab_widget)
        self.setLayout(dialog_layout)

        # Function to create custom badge preview
        def create_custom_badge():
            # Gather input values, using default values for required fields, and optional fields left blank if empty
            label = label_input.text() if label_input.text() else "Label"
            message = message_input.text() if message_input.text() else "Message"
            label_color = label_color_input.text() if label_color_input.text() else "blue"
            message_color = message_color_input.text() if message_color_input.text() else "green"
            style = style_input.currentText()  # Style from the ComboBox
            logo = logo_input.text() if logo_input.text() else ""
            logo_color = logo_color_input.text() if logo_color_input.text() else ""
            logo_width = logo_width_input.text() if logo_width_input.text() else ""
            link = link_input.text() if link_input.text() else ""
            label_font_color = label_font_color_input.text() if label_font_color_input.text() else ""
            message_font_color = message_font_color_input.text() if message_font_color_input.text() else ""

            # Construct the badge URL based on inputs
            badge_url = f"https://img.shields.io/badge/{label}-{message}-{message_color}?style={style}&scale=2"
            if label_color:
                badge_url += f"&labelColor={label_color}"
            if logo:
                badge_url += f"&logo={logo}"
            if logo_color:
                badge_url += f"&logoColor={logo_color}"
            if logo_width:
                badge_url += f"&logoWidth={logo_width}"
            if label_font_color:
                badge_url += f"&labelTextColor={label_font_color}"
            if message_font_color:
                badge_url += f"&messageTextColor={message_font_color}"

            link_label.setText(badge_url)

        # Function to copy badge link to clipboard
        def copy_badge_link():
            clipboard = QApplication.clipboard()
            clipboard.setText(link_label.text())

        # Connect button signals
        create_badge_button.clicked.connect(create_custom_badge)
        copy_button.clicked.connect(copy_badge_link)

        # Function to add custom badge Markdown to text edit
        def add_custom_badge():
            # Gather input values, using default values for required fields and optional fields left blank if empty
            label = label_input.text() if label_input.text() else "Label"
            message = message_input.text() if message_input.text() else "Message"
            label_color = label_color_input.text() if label_color_input.text() else "blue"
            message_color = message_color_input.text() if message_color_input.text() else "green"
            style = style_input.currentText()  # Style from the ComboBox
            logo = logo_input.text() if logo_input.text() else ""
            logo_color = logo_color_input.text() if logo_color_input.text() else ""
            logo_width = logo_width_input.text() if logo_width_input.text() else ""
            link = link_input.text() if link_input.text() else ""
            label_font_color = label_font_color_input.text() if label_font_color_input.text() else ""
            message_font_color = message_font_color_input.text() if message_font_color_input.text() else ""

            # Construct the badge Markdown with the gathered inputs
            badge_md = f"\n![{label}](https://img.shields.io/badge/{label}-{message}-{message_color}?style={style}"
            if label_color:
                badge_md += f"&labelColor={label_color}"
            if logo:
                badge_md += f"&logo={logo}"
            if logo_color:
                badge_md += f"&logoColor={logo_color}"
            if logo_width:
                badge_md += f"&logoWidth={logo_width}"
            if label_font_color:
                badge_md += f"&labelTextColor={label_font_color}"
            if message_font_color:
                badge_md += f"&messageTextColor={message_font_color}"
            badge_md += ")"

            # Add the constructed Markdown to the text edit
            self.parent.text_edit.insertPlainText(badge_md)

        add_badge_button.clicked.connect(add_custom_badge)

        self.show()
