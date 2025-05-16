import sys, os, re
import webbrowser
from ShieldsLicense import *
from Command_Line import CommandHandler
from PySide6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
import json
from datetime import date
from datetime import*
from PySide6.QtWidgets import QTabBar
from PySide6.QtCore import QRegularExpression
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

class Date_And_Time(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setWindowIcon(QtGui.QIcon("ME_Icons/datetime.png"))
        self.setWindowTitle("Customize Date and Time")
        self.setFixedSize(700, 280)  # Fixed height changed from 350 to 280
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet("""
            QDialog {
                background-color: #f2f2f2;
            }
            QPushButton {
                border-radius: 5px;
                padding: 4px;
                border: 1px solid #ccc;
                font-size: 14px;
                background: white;
            }
            QPushButton:hover {
                color: royalblue;
                border: 1px solid royalblue;
            }
            QFrame {
                background-color: #ccc;  /* Grey line */
            }
        """)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        format = QTextCharFormat()
        format.setFontWeight(QFont.Bold)
        format.setBackground(QBrush(QColor("#f2f2f2")))  # Change color as needed
        format.setForeground(QBrush(QColor("black")))  # Change color as needed     
        self.calendar.setHeaderTextFormat(format)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setStyleSheet("""
QCalendarWidget QSpinBox {
    background-color: royalblue;
                                    color:white;
                                    font-weight:bold;
                                    font-size:14px;
    border-radius: 5px;
    padding: 3px;
                                    selection-background-color: royalblue;  /* Light Blue */
    selection-color: white;
}
/* Increase/Decrease Year Buttons */
QCalendarWidget QSpinBox::up-button{
image:url(C:/Users/rishi/OneDrive/Desktop/Brightness_Files/ME_Icons/dda_up_white.png);
                        background: royalblue;
    width: 16px;
    height: 16px;            
                                    } 
QCalendarWidget QSpinBox::down-button {
image:url(C:/Users/rishi/OneDrive/Desktop/Brightness_Files/ME_Icons/dda_down_white.png);
    background: royalblue;
    width: 16px;
    height: 16px;
}

/* Hover Effect for Buttons */
QCalendarWidget QSpinBox::up-button:hover{
    border-top-left-radius:5px;
    border-top-right-radius:5px;
    background: #97B2ED;
                                    }
QCalendarWidget QSpinBox::down-button:hover {
    border-bottom-left-radius:5px;
    border-bottom-right-radius:5px;
    background: #97B2ED;
}

/* Arrow Icons */
QCalendarWidget QSpinBox::up-arrow, 
QCalendarWidget QSpinBox::down-arrow {
    width: 8px;
    height: 8px;
}                                    

/* Overall Calendar - Rounded exterior */
QCalendarWidget {
    background-color: white;
    border: 1px solid #ccc;
}

/* Navigation Bar (Month & Year Selector) */
QCalendarWidget QToolButton {
    background: transparent;
    margin: 3px;
    border: none;
    padding: 1px;
                                    padding-right:5px;
    color: #f2f2f2;
    font-size: 14px;
}
QCalendarWidget QToolButton:hover {
    color: white;
}

/* Left & Right Arrows */
QCalendarWidget QToolButton#qt_calendar_prevmonth{
    qproperty-icon:url(C:/Users/rishi/OneDrive/Desktop/Brightness_Files/ME_Icons/dda_left_white.png);
    background: transparent;
    margin: 3px;
    border: none;
    padding: 1px;
    font-size: 14px;
                                                       }
QCalendarWidget QToolButton#qt_calendar_nextmonth {
    qproperty-icon:url(C:/Users/rishi/OneDrive/Desktop/Brightness_Files/ME_Icons/dda_right_white.png);
    background: transparent;
    margin: 3px;
    border: none;
    padding: 1px;
    font-size: 14px;
}
QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator {
        image: none; /* Custom dropdown arrow */
        width: 0px;
        height: 0px;
    }
QCalendarWidget QToolButton#qt_calendar_prevmonth:hover{
                       background: #97B2ED;
    border-top-left-radius:5px;
                                    border-bottom-left-radius:5px;             
                                    }
QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
    background: #97B2ED;
    border-top-right-radius:5px;
                                    border-bottom-right-radius:5px;
}

/* Weekday Headers */
QCalendarWidget QHeaderView::section {
    background: royalblue;
    font-weight: bold;
    border: none;
    padding: 5px;
}
QCalendarWidget QTableView QHeaderView::section {
    font-weight: 900; /* Force extra bold */
    font-size: 14px; /* Adjust size */
    font-family: Arial, sans-serif; /* Set font family */
    color: white; /* Ensure text is visible */
}
                                    
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background: royalblue;  /* Change to your preferred color */
    color: white;           /* Text color */
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

/* Grid (Days Background) */
QCalendarWidget QTableView {
    background: white;
    border: none;
    gridline-color: rgb(234, 234, 234);
}

/* Days */
QCalendarWidget QTableView::item {
    background: white;
    border: none;
    color: black;
}
QCalendarWidget QTableView::item:hover {
    background: #f2f2f2;
    border-radius: 5px;
}
QCalendarWidget QTableView::item:selected {
    background: #97B2ED;
    color: black;
                                    font-weight: bold;
}

/* Today's Date */
QCalendarWidget QTableView::item:enabled[selected=true] {
    background: #ffcc00;
    color: black;
    font-weight: bold;
}

/* Disabled Days */
QCalendarWidget QTableView::item:disabled {
    color: #a0a0a0;
}

""")



        main_layout.addWidget(self.calendar)

        # Separator (Grey Line)
        separator = QFrame(self)
        separator.setFrameShape(QFrame.VLine)  # Vertical line
        separator.setFrameShadow(QFrame.Plain)  # Plain line (no shadow)
        separator.setStyleSheet("""
                                background-color: #ccc;
                                margin-left:5px;
                                margin-right:5px;
                                """)  # Grey color
        separator.setFixedWidth(1)  # Thin line
        main_layout.addWidget(separator)

        # Button layout (VBox beside Calendar)
        button_layout = QVBoxLayout()

        # Create QPushButtons and add to layout
        buttons = [
            (date.today().strftime("%A, %d %B %Y")),
            (date.today().strftime("%a, %d %B %Y %p")),
            (QDateTime.currentDateTime().toString("hh:mm:ss")),
            (QDateTime.currentDateTime().toString("hh:mm:ss AP")),
            (QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")),
            (QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss AP")),
            (f"{date.today().strftime('%A, %d %B %Y')}, {QDateTime.currentDateTime().toString('hh:mm:ss AP')}"),
            (f"{date.today().strftime('%a, %d %B %Y')}, {QDateTime.currentDateTime().toString('hh:mm:ss AP')}")
        ]

        for text in buttons:
            btn = QPushButton(text, self)
            btn.clicked.connect(lambda _, t=text: self.parent.text_edit.textCursor().insertText(t))
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        self.calendar.clicked.connect(self.date_selected)

        self.show()

    def date_selected(self, date):
        selected_date = date.toString("dd-MM-yyyy")
        self.parent.text_edit.textCursor().insertText(selected_date)


    def showdate(self, qDate):
        cursor = self.parent.text_edit.textCursor()
        cursor.insertText('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
