import sys, os, re

import sqlite3
import pandas as pd
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

class InsertTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Insert Table")
        self.setStyleSheet("background:#f2f2f2;")
        self.setWindowIcon(QIcon("ME_Icons/table.png"))
        self.setGeometry(600, 300, 700, 500)

        # Main layout for the dialog
        layout = QVBoxLayout(self)

        # Create a toolbar for table actions
        toolbar = QToolBar("Table Actions")
        toolbar.setStyleSheet("""
            QToolBar {
                background-color:#fafafa;
                border-radius:8px;
                border:1px solid rgb(234, 234, 234);
            }
            QToolButton {
                background-color:#fafafa;
                border: none;
                margin-right:5px;
                padding: 2px;
                border-radius:9px;
            }
            QToolButton:hover {
                background-color: #dbdcde;
            }
        """)
        layout.addWidget(toolbar)

        # Create Table widget
        self.table_widget = QTableWidget(2, 2)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                background-color: white;
                color: #333333;
                border: none;
            }
            QTableWidget::item:hover {
                background-color: #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: royalblue;
                color: white;
            }
            QTableWidget QHeaderView::section {
                background-color: #f3f3f3;
                color: #444444;
                padding: 6px;
                border: 1px solid #dcdcdc;
                font-weight: bold;
            }
            QTableWidget QHeaderView {
                background-color: #f8f8f8;
                border: none;
            }
            QTableCornerButton::section {
                background-color: #f3f3f3;
                border: 1px solid #dcdcdc;
            }
        """)
        self.table_widget.setHorizontalHeaderLabels(["1", "2"])
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Function to show context menu
        self.context_menu = QMenu(self)

        # Actions for the context menu
        self.add_row_above_action = QAction("Add Row Above", self)
        self.add_row_above_action.triggered.connect(self.add_row_above)
        self.context_menu.addAction(self.add_row_above_action)

        self.add_row_below_action = QAction("Add Row Below", self)
        self.add_row_below_action.triggered.connect(self.add_row_below)
        self.context_menu.addAction(self.add_row_below_action)

        self.context_menu.addSeparator()

        self.add_column_left_action = QAction("Add Column Left", self)
        self.add_column_left_action.triggered.connect(self.add_column_left)
        self.context_menu.addAction(self.add_column_left_action)

        self.add_column_right_action = QAction("Add Column Right", self)
        self.add_column_right_action.triggered.connect(self.add_column_right)
        self.context_menu.addAction(self.add_column_right_action)

        layout.addWidget(self.table_widget)

        # Toolbar actions for table modifications
        self.add_row_action = QAction(QIcon("ME_Icons/addrow.png"), "Add Row", self)
        self.add_column_action = QAction(QIcon("ME_Icons/addcol.png"), "Add Column", self)
        self.delete_row_action = QAction(QIcon("ME_Icons/delrow.png"), "Delete Row", self)
        self.delete_column_action = QAction(QIcon("ME_Icons/delcol.png"), "Delete Column", self)
        self.clear_table_action = QAction(QIcon("ME_Icons/deltab.png"), "Clear Table", self)
        self.clear_table_contents_action = QAction(QIcon("ME_Icons/delcont.png"), "Clear Table Contents", self)

        # Connecting actions
        self.add_row_action.triggered.connect(self.add_row)
        self.add_column_action.triggered.connect(self.add_column)
        self.delete_row_action.triggered.connect(self.delete_row)
        self.delete_column_action.triggered.connect(self.delete_column)
        self.clear_table_action.triggered.connect(self.clear_table)
        self.clear_table_contents_action.triggered.connect(self.clear_table_contents)

        self.open_table_action = QAction(QIcon("ME_Icons/opentable.png"), "Open External Table", self)
        self.open_table_action.triggered.connect(self.load_file)
        toolbar.addAction(self.open_table_action)

        # Adding actions to the toolbar
        toolbar.addAction(self.add_row_action)
        toolbar.addAction(self.add_column_action)
        toolbar.addAction(self.delete_row_action)
        toolbar.addAction(self.delete_column_action)
        toolbar.addAction(self.clear_table_action)
        toolbar.addAction(self.clear_table_contents_action)

        # Add header editing action to the toolbar
        self.edit_headers_action = QAction(QIcon("ME_Icons/edithead.png"), "Edit Headers", self)
        self.edit_headers_action.triggered.connect(self.edit_headers)
        toolbar.addAction(self.edit_headers_action)

        toolbar.addSeparator()

        # Alignment Dropdown for table cells
        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems(["Left", "Center", "Right"])
        self.alignment_combo.setStyleSheet("""
            QComboBox {
margin-left: 5px;
margin-right: 5px;
                font-size: 15px;
                height:20px;
                background-color: white;
                selection-background-color: #eeeeee;
                selection-color: royalblue;
                padding: 6px;
                color:#4D4D4D;
                border-radius:7px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                background:white;
                border-top-right-radius:7px;
                border-bottom-right-radius:7px;
                image: url(C:/Users/rishi/OneDrive/Desktop/Brightness_Files/ME_Icons/dda.png);
                background-size: 5px;
                background-repeat: no-repeat;
                background-position: right 10px center;
            }
            QComboBox QAbstractItemView {
    }
    QComboBox QAbstractItemView::item {
    }
    QComboBox QAbstractItemView::item:selected {
    }
            QComboBox:hover {
                border:1px solid #ccc;
                selection-background-color: white;
                selection-color: white;
            }
        """)
        self.alignment_combo.currentIndexChanged.connect(self.apply_alignment)
        toolbar.addWidget(self.alignment_combo)

        # Embed Button for markdown
        self.embed_button = QPushButton("Insert Table")
        self.embed_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                padding: 6px;
                border: 1px solid #ccc;
                background: white;
            }
            QPushButton:hover {
                border: 1px solid royalblue;
                color: royalblue;
            }
        """)
        self.embed_button.clicked.connect(self.embed_table)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.embed_button)
        layout.addLayout(button_layout)

    def show_context_menu(self, pos):
        """Show context menu when right-clicking on the table."""
        self.context_menu.exec(self.table_widget.mapToGlobal(pos))

    def add_row_above(self):
        """Add a row above the currently selected row."""
        row = self.table_widget.currentRow()
        self.table_widget.insertRow(row)

    def add_row_below(self):
        """Add a row below the currently selected row."""
        row = self.table_widget.currentRow() + 1
        self.table_widget.insertRow(row)

    def add_column_left(self):
        """Add a column to the left of the currently selected column."""
        col = self.table_widget.currentColumn()
        self.table_widget.insertColumn(col)

    def add_column_right(self):
        """Add a column to the right of the currently selected column."""
        col = self.table_widget.currentColumn() + 1
        self.table_widget.insertColumn(col)

    def apply_alignment(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        alignment = self.alignment_combo.currentText()
        for item in selected_items:
            if alignment == "Left":
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            elif alignment == "Center":
                item.setTextAlignment(Qt.AlignCenter)
            elif alignment == "Right":
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def add_row(self):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

    def add_column(self):
        col_position = self.table_widget.columnCount()
        self.table_widget.insertColumn(col_position)

    def delete_row(self):
        """Deletes selected row(s) or the last row if no selection."""
        selected_rows = sorted(set(item.row() for item in self.table_widget.selectedItems()))
        if selected_rows:
            # If rows are selected, delete them one by one (starting from the last selected row to avoid reindexing issues)
            for row in reversed(selected_rows):
                self.table_widget.removeRow(row)
        else:
            # If no row is selected, delete the last row
            row_count = self.table_widget.rowCount()
            if row_count > 0:
                self.table_widget.removeRow(row_count - 1)

    def delete_column(self):
        """Deletes selected column(s) or the last column if no selection."""
        selected_columns = sorted(set(item.column() for item in self.table_widget.selectedItems()))
        if selected_columns:
            # If columns are selected, delete them one by one (starting from the last selected column to avoid reindexing issues)
            for col in reversed(selected_columns):
                self.table_widget.removeColumn(col)
        else:
            # If no column is selected, delete the last column
            column_count = self.table_widget.columnCount()
            if column_count > 0:
                self.table_widget.removeColumn(column_count - 1)


    def clear_table(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)

    def clear_table_contents(self):
        self.table_widget.clearContents()

    def edit_headers(self):
        cols = self.table_widget.columnCount()
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Column Headers")
        dialog.setFixedSize(400, 200)
        dialog.setWindowIcon(QIcon("C:/Users/rishi/OneDrive/Documents/ME_Icons/edithead.png"))

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        line_edits = []
        for col in range(cols):
            current_header = self.table_widget.horizontalHeaderItem(col).text() if self.table_widget.horizontalHeaderItem(col) else ''
            line_edit = QLineEdit(current_header)
            line_edits.append(line_edit)
            form_layout.addRow(f"Column {col+1}:", line_edit)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(form_widget)
        layout.addWidget(scroll_area)

        button = QPushButton("Edit")
        button.clicked.connect(lambda: self.update_headers(dialog, line_edits))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    def update_headers(self, dialog, line_edits):
        for col, line_edit in enumerate(line_edits):
            new_header = line_edit.text()
            self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(new_header))
        dialog.accept()

    def load_file(self):
        """Open file and load into QTableWidget."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;SQLite Database (*.db *.sqlite);;All Files (*)")
        
        if not file_path:
            return  # User canceled file selection

        if file_path.endswith((".xlsx", ".xls", ".csv")):
            self.load_excel_csv(file_path)
        elif file_path.endswith((".db", ".sqlite")):
            self.load_sqlite(file_path)

    def load_excel_csv(self, file_path):
        """Load Excel or CSV files into QTableWidget."""
        try:
            df = pd.read_excel(file_path) if file_path.endswith((".xlsx", ".xls")) else pd.read_csv(file_path)
            self.populate_table(df.values.tolist(), df.columns.tolist())
        except Exception as e:
            print(f"Error loading file: {e}")

    def load_sqlite(self, file_path):
        """Load SQLite database and fetch the first table."""
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
            first_table = cursor.fetchone()
            
            if not first_table:
                print("No tables found in the database.")
                return
            
            table_name = first_table[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            self.populate_table(data, columns)
            conn.close()
        except Exception as e:
            print(f"Error loading database: {e}")

    def populate_table(self, data, columns=None):
        """Fill QTableWidget with data."""
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(columns) if columns else len(data[0]))
        if columns:
            self.table_widget.setHorizontalHeaderLabels(columns)

        for row, record in enumerate(data):
            for col, value in enumerate(record):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))

    def embed_table(self):
        rows = self.table_widget.rowCount()
        cols = self.table_widget.columnCount()

        markdown_table = []

        # Extract headers
        headers = ["| " + " | ".join(
            [self.table_widget.horizontalHeaderItem(c).text() if self.table_widget.horizontalHeaderItem(c) else '' for c in range(cols)]
        ) + " |"]
        markdown_table.append(headers[0])

        # Generate alignment row for markdown
        alignments = []
        for col in range(cols):
            alignment = Qt.AlignLeft  # Default alignment

            for row in range(rows):  # Check alignment from the first non-empty row
                item = self.table_widget.item(row, col)
                if item and item.text().strip():  # Ensure item is not empty
                    alignment = item.textAlignment()
                    break  # Stop after finding the first non-empty alignment

            # ✅ Use bitwise `&` to correctly detect alignment in PySide6
            if alignment & Qt.AlignRight:
                alignments.append("------:")
            elif alignment & Qt.AlignCenter:
                alignments.append(":------:")
            else:
                alignments.append(":------")

        markdown_table.append("| " + " | ".join(alignments) + " |")

        # Extract table content
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.table_widget.item(row, col)
                row_data.append(item.text() if item else " ")
            markdown_table.append("| " + " | ".join(row_data) + " |")

        markdown_text = "\n".join(markdown_table)
        self.parent().text_edit.insertPlainText(markdown_text)
        self.accept()

        
