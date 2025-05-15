import sys, os, re

import json
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtGui import QFontMetrics, QTextCharFormat, QFont
from PySide6.QtWebEngineWidgets import QWebEngineView
import markdown2
import sqlite3
from markdown2 import Markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.formatters import HtmlFormatter
from PySide6.QtWidgets import QStyleFactory
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt

class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Find and Replace")
        self.setFixedSize(300, 130)  # Set dialog size
        self.setStyleSheet("background:#f2f2f2;")

        # Main layout
        main_layout = QVBoxLayout()

        # Find layout (Find label and Find line edit in a horizontal layout)
        find_layout = QHBoxLayout()
        self.find_label = QLabel("Find:")
        self.find_edit = QLineEdit()  # Same width for both QLineEdits
        self.find_edit.setStyleSheet("""
            QLineEdit {
                border-radius: 5px;
                font-size: 12px;
                padding: 5px;
                margin-left:20px;
                border-bottom: 1px solid #ccc;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid royalblue;
            }
        """)
        find_layout.addWidget(self.find_label)
        find_layout.addWidget(self.find_edit)

        # Replace layout (Replace label and Replace line edit in a horizontal layout)
        replace_layout = QHBoxLayout()
        self.replace_label = QLabel("Replace:")
        self.replace_edit = QLineEdit()  # Same width for both QLineEdits
        self.replace_edit.setStyleSheet("""
            QLineEdit {
                border-radius: 5px;
                font-size: 12px;
                padding: 5px;
                border-bottom: 1px solid #ccc;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid royalblue;
            }
        """)
        replace_layout.addWidget(self.replace_label)
        replace_layout.addWidget(self.replace_edit)

        # Combining find and replace layouts in a horizontal layout
        find_replace_layout = QVBoxLayout()
        find_replace_layout.addLayout(find_layout)
        find_replace_layout.addLayout(replace_layout)

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.find_button = QPushButton("Find")
        self.find_button.setStyleSheet("""
            QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white;}
            QPushButton:hover{
                                   border:1px solid royalblue;
                                   color:royalblue;}
        """)
        self.replace_button = QPushButton("Replace")
        self.replace_button.setStyleSheet("""
            QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white;}
            QPushButton:hover{
                                   border:1px solid royalblue;
                                   color:royalblue;}
        """)
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.replace_button)

        # Add all layouts to the main layout
        main_layout.addLayout(find_replace_layout)
        main_layout.addLayout(button_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # Connect buttons to their respective functions
        self.find_button.clicked.connect(self.find_text)
        self.replace_button.clicked.connect(self.find_replace_text)


    def find_text(self):
        find_text = self.find_edit.text()
        if not find_text:
            return

        text_edit = self.parent().text_edit
        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)  # Start from the beginning of the document
        text_format = QTextCharFormat()
        text_format.setBackground(QColor("yellow"))  # Highlight with yellow background

        document = text_edit.document()
        while True:
            cursor = document.find(find_text, cursor)
            if cursor.isNull():
                break  # No more occurrences found
            cursor.mergeCharFormat(text_format)  # Highlight the found text

    def find_replace_text(self):
        find_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        if not find_text:
            return

        text_edit = self.parent().text_edit
        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)  # Start from the beginning of the document

        document = text_edit.document()
        while True:
            cursor = document.find(find_text, cursor)
            if cursor.isNull():
                break  # No more occurrences found
            cursor.insertText(replace_text)  # Replace the found text

    def closeEvent(self, event):
        """Reset text formatting when the dialog is closed."""
        text_edit = self.parent().text_edit
        cursor = QTextCursor(text_edit.document())  # Create a cursor for the entire document

        # Default format (clears all formatting)
        default_format = QTextCharFormat()

        # Select the entire document and apply the default format
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(default_format)

        super().closeEvent(event)
