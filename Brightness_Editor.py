#python -m pip install PySide6 qdarkstyle html2text requests markdown2 pygments sqlite-utils

import sys, os, re, subprocess
from Templates import *
from Date_And_Time_Calendar import *
from Find_And_Replace import *
from Table import *
from Badge import *
from Command_Line import CommandHandler
from PySide6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
import json
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
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
import markdown2
from PySide6.QtGui import QContextMenuEvent
from markdown2 import Markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.formatters import HtmlFormatter
from PySide6.QtWidgets import QStyleFactory
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, QTimer
import mistune

#"ME_Icons/"
#"ME_Icons/"

SETTINGS_FILE = "menu_state.json"
REM_RIBBON = "remribbon.json"

from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.formats = {}

        # Header (Royal Blue)
        header_format = QTextCharFormat()
        header_format.setForeground(QColor("royalblue"))
        header_format.setFontWeight(QFont.Bold)
        self.formats['header'] = header_format

        # Bold
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        bold_format.setForeground(QColor("black"))
        self.formats['bold'] = bold_format

        # Italic
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        italic_format.setForeground(QColor("#444444"))
        self.formats['italic'] = italic_format

        # Bold Italic
        bolditalic_format = QTextCharFormat()
        bolditalic_format.setFontWeight(QFont.Bold)
        bolditalic_format.setFontItalic(True)
        bolditalic_format.setForeground(QColor("#222222"))
        self.formats['bolditalic'] = bolditalic_format

        # Strikethrough
        strikethrough_format = QTextCharFormat()
        strikethrough_format.setFontStrikeOut(True)
        strikethrough_format.setForeground(QColor("#999999"))
        self.formats['strikethrough'] = strikethrough_format

        # Inline Code
        code_format = QTextCharFormat()
        code_font = QFont("Courier New,monospace")
        code_format.setFont(code_font)
        code_format.setForeground(QColor("#d14"))
        self.formats['code'] = code_format

        code_block_format = QTextCharFormat()
        code_block_font = QFont("Courier New,monospace")
        code_block_format.setFont(code_block_font)
        code_block_format.setForeground(QColor("#b000b0"))
        self.formats['codeblock'] = code_block_format

        # Blockquote
        quote_format = QTextCharFormat()
        quote_format.setForeground(QColor("#2a8fbd"))  # Light blue
        quote_format.setFontItalic(True)
        self.formats['quote'] = quote_format

        # List items
        list_format = QTextCharFormat()
        list_format.setForeground(QColor("#6a5acd"))  # Slate blue
        self.formats['list'] = list_format

        # Link
        link_format = QTextCharFormat()
        link_format.setForeground(QColor("#0033cc"))  # Deep link blue
        link_format.setFontUnderline(True)
        self.formats['link'] = link_format

        # Comment
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("gray"))
        comment_format.setFontItalic(True)
        self.formats['comment'] = comment_format

        # Image Marker (!)
        image_marker_format = QTextCharFormat()
        image_marker_format.setForeground(QColor("#e67e22"))  # Orange
        self.formats['image_marker'] = image_marker_format

        # Math (LaTeX inline or block)
        math_format = QTextCharFormat()
        math_format.setForeground(QColor("#8A2BE2"))  # BlueViolet
        math_format.setFontItalic(True)
        self.formats['math'] = math_format

        # Mermaid blocks
        self.inside_mermaid = False
        self.mermaid_start_block = None
        mermaid_format = QTextCharFormat()
        mermaid_format.setForeground(QColor("#228B22"))  # Forest Green
        mermaid_format.setFontItalic(True)
        self.formats['mermaid'] = mermaid_format

        # HTML tags
        html_format = QTextCharFormat()
        html_format.setForeground(QColor("#aa0000"))  # Deep red
        html_format.setFontWeight(QFont.Bold)
        self.formats['html'] = html_format

    def highlightBlock(self, text):
        block_number = self.currentBlock().blockNumber()

        if text.strip().startswith("```mermaid"):
            self.inside_mermaid = True
            self.mermaid_start_block = block_number
            return

        if self.inside_mermaid:
            if text.strip() == "```":
                for line in range(self.mermaid_start_block, block_number + 1):
                    block = self.document().findBlockByNumber(line)
                    self.setFormat(block.position(), block.length(), self.formats['mermaid'])
                self.inside_mermaid = False
                self.mermaid_start_block = None
            return

        # Pattern-based highlighting
        self.setFormatByRegex(text, r'^(#{1,6})(\s?)[^\n]+', self.formats['header'])  # Headers
        self.setFormatByRegex(text, r'(?<!\*)\*\*\*(?!\s)(.+?)(?!\s)\*\*\*(?!\*)', self.formats['bolditalic'])
        self.setFormatByRegex(text, r'\*\*(.*?)\*\*', self.formats['bold'])
        self.setFormatByRegex(text, r'\*(.*?)\*', self.formats['italic'])
        self.setFormatByRegex(text, r'`([^`]+)`', self.formats['code'])  # Inline code
        self.setFormatByRegex(text, r'```.*```', self.formats['codeblock'])  # Single-line code blocks
        self.setFormatByRegex(text, r'^>(\s?)[^\n]+', self.formats['quote'])  # Blockquotes
        self.setFormatByRegex(text, r'^(\s*[-*+]|\s*\d+\.)\s', self.formats['list'])  # Lists
        self.setFormatByRegex(text, r'^\d+\.\s+.*', self.formats['list'])
        self.setFormatByRegex(text, r'^[-*+]\s+.*', self.formats['list'])

        self.setFormatByRegex(text, r'<!--.*?-->', self.formats['comment'])  # HTML comments

        self.setFormatByRegex(text, r'</?[a-zA-Z][^>]*?>', self.formats['html'])  # HTML tags

        # Link patterns
        for match in re.finditer(r'\[.*?\]\((.*?)\)', text):
            self.setFormat(match.start(1), len(match.group(1)), self.formats['link'])
        for match in re.finditer(r'\bhttps?://[^\s]+|\bwww\.[^\s)]+', text):
            self.setFormat(match.start(), len(match.group()), self.formats['link'])

        # Image markers
        for match in re.finditer(r'!\[.*?\]\(.*?\)', text):
            self.setFormat(match.start(), 1, self.formats['image_marker'])

        # Math
        for match in re.finditer(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', text):
            self.setFormat(match.start(1), len(match.group(1)), self.formats['math'])
        for match in re.finditer(r'\$\$(.*?)\$\$', text, re.DOTALL):
            self.setFormat(match.start(1), len(match.group(1)), self.formats['math'])

        # Strikethrough
        for match in re.finditer(r'~~(.*?)~~', text):
            self.setFormat(match.start(1), match.end(1) - match.start(1), self.formats['strikethrough'])

    def setFormatByRegex(self, text, pattern, format):
        regex = QRegularExpression(pattern)
        matches = regex.globalMatch(text)
        while matches.hasNext():
            match = matches.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), format)



class BrightnessEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_file = None
        self.command_handler = CommandHandler(self)
        
    def initUI(self):
        self.setWindowTitle('Brightness')
        self.setWindowIcon(QtGui.QIcon("ME_Icons/MEico.png"))
        self.setStyleSheet("""

background:white;

""")
        
        widget = QWidget()
        self.setCentralWidget(widget)
        self.main_layout = QVBoxLayout(widget)

        self.icon_label = QLabel()
        self.icon_pixmap = QPixmap("ME_Icons/MEico.png")
        self.icon_label.setPixmap(self.icon_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_label.setStyleSheet("""
margin-right:10px;
""")

        self.top_tab_widget = QWidget()
        self.main_tabs_layout = QHBoxLayout()
        self.top_tab_widget.setMinimumHeight(10)
        self.top_tab_widget.setMaximumHeight(50)  # Adjust as needed
        self.main_tabs_layout.setSpacing(10)  # Space between buttons

        # Create buttons separately
        self.file_button = QPushButton("File")
        self.edit_button = QPushButton("Edit")
        self.insert_button = QPushButton("Insert")
        self.format_button = QPushButton("Format")
        self.view_button = QPushButton("View")
        self.help_button = QPushButton("Help")

        self.file_button.setCheckable(True)
        self.edit_button.setCheckable(True)
        self.edit_button.setChecked(True)
        self.insert_button.setCheckable(True)
        self.format_button.setCheckable(True)
        self.view_button.setCheckable(True)
        self.help_button.setCheckable(True)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.file_button)
        self.button_group.addButton(self.edit_button)
        self.button_group.addButton(self.insert_button)
        self.button_group.addButton(self.format_button)
        self.button_group.addButton(self.view_button)

        # Connect buttons to function
        self.file_button.clicked.connect(lambda: self.toggle_toolbar(self.file_toolbar, self.file_button))
        self.edit_button.clicked.connect(lambda: self.toggle_toolbar(self.edit_toolbar, self.edit_button))
        self.insert_button.clicked.connect(lambda: self.toggle_toolbar(self.insert_toolbar, self.insert_button))
        self.format_button.clicked.connect(lambda: self.toggle_toolbar(self.format_toolbar, self.format_button))
        self.view_button.clicked.connect(lambda: self.toggle_toolbar(self.view_toolbar, self.view_button))

        # Add buttons to main_tabs_layout
        self.main_tabs_layout.addWidget(self.icon_label)
        self.main_tabs_layout.addWidget(self.file_button)
        self.main_tabs_layout.addWidget(self.edit_button)
        self.main_tabs_layout.addWidget(self.insert_button)
        self.main_tabs_layout.addWidget(self.format_button)
        self.main_tabs_layout.addWidget(self.view_button)
        self.main_tabs_layout.addWidget(self.help_button)

        spacer = QSpacerItem(40, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.main_tabs_layout.addSpacerItem(spacer)

        self.top_tab_widget.setLayout(self.main_tabs_layout)

        self.top_tab_widget.setStyleSheet("""
    QPushButton {
        border: none;
        color:#4d4d4d;
        font-weight: bold;
        border-bottom: 4px solid transparent;
                                          font-size:14px;
                                          margin-right:10px;
                                          padding-left:4px;
                                          padding-right:4px;
    }
    QPushButton:hover {
        border-bottom: 4px solid darkgrey;
    }
    QPushButton:checked {
        color: royalblue;
        border-bottom: 4px solid royalblue;
    }
""")

        self.top_container = QWidget()
        self.top_layout = QVBoxLayout(self.top_container)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.top_tab_widget)

        header_layout = QHBoxLayout()

        self.file_label = QLabel(f"Hi! Welcome to <i>Brightness</i>.")
        QTimer.singleShot(5000, lambda:self.file_label.setText("•••"))
        self.file_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_label.customContextMenuRequested.connect(self.show_file_label_context_menu)
        self.file_label.setFixedHeight(20)
        self.file_label.setAlignment(Qt.AlignCenter)  # Center-align the text
        self.file_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # Minimum height
        self.file_label.setStyleSheet("""
background:#f2f2f2;
                                      border-radius:8px;
                                      padding:1px;
font-size:14px;
""")
        l_h = 25

        self.file_path = ""
        self.file_base_name = ""

        self.file_label.setMinimumHeight(l_h)

        color_style = 'style="color:#777778;"'

        self.file_suggestions = [
            f'<span {color_style}>📝 Ready to create your masterpiece...</span>',
            f'<span {color_style}>📂 No scrolls opened yet — summon one?</span>',
            f'<span {color_style}>✨ An empty canvas awaits...</span>',
            f'<span {color_style}>🚀 Markdown Mission: No file loaded</span>',
            f'<span {color_style}>📄 Where words shall go — file not chosen.</span>',
            f'<span {color_style}>🔍 Nothing to see here... yet.</span>',
            f'<span {color_style}>💡 Start fresh or open a story in Markdown.</span>',
            f'<span {color_style}>📘 Waiting for content to come alive.</span>',
            f'<span {color_style}>🌌 Silence... the editor dreams of words.</span>',
            f'<span {color_style}>🛠️ No file. Just you, your thoughts, and infinite potential.</span>',
            f'<span {color_style}>📜 The story awaits — open a file to begin.</span>',
            f'<span {color_style}>🎨 Markdown art, waiting to be painted.</span>',
            f'<span {color_style}>🕰️ Time to unlock the creativity within.</span>',
            f'<span {color_style}>🌍 Ready for a journey through words?</span>',
            f'<span {color_style}>🖋️ Pen your thoughts — no file opened yet.</span>',
            f'<span {color_style}>🔓 The editors gates are open, but no file to work with.</span>',
            f'<span {color_style}>🚧 Under construction... waiting for a file to edit.</span>',
            f'<span {color_style}>🌱 A blank page waiting for life to be breathed into it.</span>',
            f'<span {color_style}>🔮 The future is unwritten — open a file to start.</span>',
            f'<span {color_style}>📚 Start a new chapter in your Markdown book.</span>',
        ]

        self.suggestion_index = 0
        self.should_rotate = False  # << Key flag

        self.label_timer = QTimer(self)
        self.label_timer.timeout.connect(self.rotate_label)
        self.label_timer.start(10000)

        self.start_label_rotation_if_placeholder()

        header_layout.addWidget(self.file_label)

        self.toggle_mode_button = QPushButton(QtGui.QIcon("ME_Icons/togglemode.png"), '', self)
        self.toggle_mode_button.setToolTip("Toggle live preview between light and dark mode")  # Set tooltip
        self.toggle_mode_button.setShortcut("Ctrl+D")  # Set shortcut (optional for QPushButton)
        self.toggle_mode_button.setIconSize(QSize(25, 25))
        self.toggle_mode_button.setFixedSize(30, 30)
        self.toggle_mode_button.clicked.connect(self.toggle_mode)
        self.toggle_mode_button.setStyleSheet("""
                                         QPushButton {
        background:#f2f2f2;
        border-radius:8px;}
                                         QPushButton:hover {
                                         background:#e5e5e5;
                                         }
""")
        self.is_dark_mode = False

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.setStyleSheet("""
QSplitter{
                                    }
QSplitter::handle:vertical {
    background-color: rgb(234, 234, 234);
    height: 2px;
}
QSplitter::handle:horizontal {
    background-color: rgb(234, 234, 234);
    height: 2px;
}

""")
        self.splitter.setOpaqueResize(True)

        self.file_system_model = QFileSystemModel()
    
        # Set the root path to the user's home directory, which includes Desktop, Documents, etc.
        self.file_system_model.setRootPath(QDir.homePath())

        # Desktop, Home, and Quick View (add specific paths)
        home_dir = QDir.homePath()  # User home directory
        desktop_dir = os.path.join(home_dir, 'Desktop')  # Desktop directory
        documents_dir = os.path.join(home_dir, 'Documents')

        # Create the tree view to show file system
        self.tree_view = QTreeView()
        self.tree_view.setAnimated(True)
        self.tree_view.setRootIsDecorated(True)
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setRootIndex(self.file_system_model.index(QDir.homePath()))  # Start from user's home directory
        self.tree_view.hide()
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.clicked.connect(self.open_file_from_tree)
        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Multi-select
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.AscendingOrder)
        self.tree_view.setEditTriggers(QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        self.file_system_model = QFileSystemModel()

        self.tree_view.setStyleSheet("""
QTreeView {
                                     border:none;
                                     border-radius:8px;
                                     background:#f2f2f2;
color:black;
                show-decoration-selected: 1;
            }
            QTreeView::item:selected {
                background-color:transparent;
                color: royablue;
                font-weight:bold;
            }
            QTreeView::item {
                                    margin:2px;
                                    padding:2px;
            }
                                    QTreeView::item:hover {
            border-radius:6px;
            background:transparent;
                                    margin:2px;
                                    padding:2px;
                                      color:royalblue;
            }
            QTreeView::item:selected:active {
        background-color: transparent;
    }
                                     QScrollBar:vertical {
            background: #eeeeee;
            width: 8px;
            margin: 0px 0px 0px 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #b0b0b0;
            min-height: 10px;
                                     min-width:8px;
            border-radius: 3px;
        }
        QScrollBar::add-line:vertical {
            background: #e3e5e9;
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: #e3e5e9;
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar:horizontal {
            background: #e3e5e9;
            height: 9px;
        }
        QScrollBar::handle:horizontal {
            background: #b0b0b0;
            min-width: 15px;
            border-radius: 4px;
        }
        QScrollBar::add-line:horizontal {
            background: #e3e5e9;
            width: 0px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            background: #e3e5e9;
            width: 0px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
""")

        # Add the tree view to the splitter
        self.splitter.addWidget(self.tree_view)
        
        self.text_edit = QTextEdit()
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.text_edit.setCursorWidth(2)
        self.text_edit.setAcceptDrops(True)
        self.text_edit.setPlaceholderText("Enter your Markdown here...")
        self.text_edit.textChanged.connect(self.update_preview)
        self.text_edit.textChanged.connect(self.update_html_preview)
        self.text_edit.textChanged.connect(self.mark_as_edited)
        self.text_edit.textChanged.connect(self.schedule_outline_update)
        self.text_edit.setUndoRedoEnabled(True)
        self.text_edit.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable custom context menu
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu)

        self.highlighter = MarkdownHighlighter(self.text_edit.document())
        
        palette = self.text_edit.palette()
        palette.setColor(QPalette.Text, QColor("white"))  # Text color
        palette.setColor(QPalette.Highlight, QColor("royalblue"))  # Selection background color
        palette.setColor(QPalette.HighlightedText, QColor("white"))  # Selected text color
        self.text_edit.setPalette(palette)
        
        self.text_edit.setStyleSheet("""
                                     QTextEdit {
                                     border:2px solid white;
padding:3px;
margin-left:20px;
margin-top:20px;
background:white;
selection-background-color: royalblue;  /* Change selection highlight */
        selection-color: white;  /* Change selected text color */
                                     font-size:17px;
                                     }
                                     QTextEdit::cursor {
        width: 3px; /* Cursor width */
        background-color: red;
    }
                                     QTextEdit:focus {
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

        self.text_edit.dragEnterEvent = self.dragEnterEvent
        self.text_edit.dragMoveEvent = self.dragMoveEvent
        self.text_edit.dropEvent = self.dropEvent
        self.text_edit.textChanged.connect(self.update_status_info)
        self.text_edit.textChanged.connect(self.highlight_headers)
        self.text_edit.cursorPositionChanged.connect(self.update_cursor_position)

        self.status_bar = QStatusBar()

        self.md_selection = QComboBox()
        self.md_selection.addItems(["Default Markdown", "Basic Markdown", "Advanced Markdown"])
        self.md_selection.currentTextChanged.connect(self.handle_markdown_selection)
        self.md_selection.setStyleSheet("""
            QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
margin-top:5px;
                font-size: 15px;
                height:20px;
                background-color: white;
                selection-background-color:transparent;
                selection-color: royalblue;
                padding: 1px;
                padding-left:3px;
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
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png);
                background-repeat: no-repeat;
                background-position: right 10px center;
            }
            QComboBox:hover {
                border:1px solid #ccc;
                selection-background-color: white;
                selection-color: white;
            }
            
        """)
        self.status_bar.addPermanentWidget(self.md_selection)

        self.present_markdown_preview_button = QPushButton(QtGui.QIcon("ME_Icons/present.png"),"")
        self.present_markdown_preview_button.setShortcut("F5")
        self.present_markdown_preview_button.setToolTip("Present Markdown")
        self.present_markdown_preview_button.setStatusTip("Present Markdown")
        self.present_markdown_preview_button.setIconSize(QSize(25, 25))
        self.present_markdown_preview_button.setStyleSheet("""
        QPushButton{
        border-radius:8px;}
        QPushButton:hover{
        background:white;
        }
        """)
        self.present_markdown_preview_button.clicked.connect(self.update_preview_2)
        self.status_bar.addPermanentWidget(self.present_markdown_preview_button)

        self.file_status_label = QLabel("")  # Default status
        self.status_bar.addPermanentWidget(self.file_status_label)
        self.status_bar.setStyleSheet("""
                                      padding-left:5px;
        border-radius:8px;
        margin:5px;
        margin-left:7px;
                                      margin-right:7px;
background:#efefef;
font-weight:500;
color:#4D4D4D;
""")
        self.word_count_label = QLabel("Word count: 0")
        self.word_count_label.setStyleSheet("""font-size: 12px;
        margin:4px;
        color:#313131;""")
        self.line_count_label = QLabel("Lines: 0")
        self.line_count_label.setStyleSheet("""font-size: 12px;
        margin:4px;
        color:#313131;""")
        self.column_count_label = QLabel("Columns: 0")
        self.column_count_label.setStyleSheet("""font-size: 12px;
        margin:4px;
        color:#313131;""")
        self.space_count_label = QLabel("Spaces: 0")
        self.space_count_label.setStyleSheet("""font-size: 12px;
        margin:4px;
        color:#313131;""")
        self.encoding_label = QLabel("UTF-8")
        self.encoding_label.setStyleSheet("""font-size: 12px;
        margin:4px;
        color:#313131;""")

        self.status_bar.addPermanentWidget(self.encoding_label)
        self.status_bar.addPermanentWidget(self.word_count_label)
        self.status_bar.addPermanentWidget(self.line_count_label)
        self.status_bar.addPermanentWidget(self.column_count_label)
        self.status_bar.addPermanentWidget(self.space_count_label)
        self.setStatusBar(self.status_bar)

        self.tab_widget_for_preview = QTabWidget()
        self.tab_widget_for_preview.setMovable(True)
        self.tab_widget_for_preview.setTabBarAutoHide(True)
        self.tab_widget_for_preview.setTabShape(QTabWidget.Rounded)
        self.tab_widget_for_preview.setTabPosition(QTabWidget.North)
        self.tab_widget_for_preview.setStyleSheet("""
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
            background: white;
            border: 0px solid lightgrey;
            padding: 5px;
            width:150px;
            border-radius:5px;
            margin-bottom:7px;
            margin:4px;
        }
                          QTabBar::tab:hover {
                          background:white;
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
        
        # Create two tabs
        mark_preview_tab = QWidget()
        html_preview_tab = QWidget()
        
        self.preview_browser = QWebEngineView()
        self.preview_browser.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
        self.preview_browser.setStyleSheet("""
QWebEngineView {
border: none;
margin: 0px;
padding: 0px;
border-radius:5px;
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

        mark_preview_tab_layout = QVBoxLayout()
        mark_preview_tab_layout.addWidget(self.preview_browser)
        mark_preview_tab.setLayout(mark_preview_tab_layout)

        self.preview_browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.preview_browser.customContextMenuRequested.connect(self.contextMenuEvent)
        self.clipboard = QApplication.clipboard()
        
        html_preview_tab_layout = QVBoxLayout()

        self.save_button = QPushButton(QtGui.QIcon("ME_Icons/save.png"), '')
        self.save_button.clicked.connect(self.save_html_preview)
        self.save_button.setIconSize(QSize(25, 25))
        self.save_button.setStyleSheet("""
        QPushButton {
        background:#f2f2f2;
        border-radius:8px;}
                                         QPushButton:hover {
                                         background:#e5e5e5;
                                         }
        """)
        self.copy_html_button = QPushButton(QtGui.QIcon("ME_Icons/copy.png"), '')
        self.copy_html_button.clicked.connect(lambda: QApplication.clipboard().setText(self.html_edit.toPlainText()))
        self.copy_html_button.setIconSize(QSize(25, 25))
        self.copy_html_button.setStyleSheet("""
        QPushButton {
        background:#f2f2f2;
        border-radius:8px;
        margin-right:4px;}
                                         QPushButton:hover {
                                         background:#e5e5e5;
                                         }
        """)

        self.html_edit = QTextEdit()
        self.html_edit.setStyleSheet("""
        QTextEdit {
                                     border:2px solid white;
                                     border-radius:10px;
padding:3px;
background:white;
                                     font-size:17px;
                                     }
                                     QTextEdit::cursor {
        width: 3px; /* Cursor width */
    }
                                     QTextEdit:focus {
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
        html_preview_tab_layout.addWidget(self.html_edit)
        html_preview_tab.setLayout(html_preview_tab_layout)

        # copy_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.copy_html_button.setFixedSize(34, 30)
        self.copy_html_button.setIconSize(QSize(25, 25))
        self.save_button.setFixedSize(31, 30)
        self.save_button.setIconSize(QSize(25, 25))

        corner_layout = QHBoxLayout()
        corner_layout.setContentsMargins(0, 0, 2, 0)  # Stretch the second button 
        corner_layout.setSpacing(2)
        corner_layout.addWidget(self.save_button)
        corner_layout.addWidget(self.copy_html_button)
        corner_layout.addWidget(self.toggle_mode_button)

        self.corner_widget = QWidget()
        self.tab_widget_for_preview.currentChanged.connect(self.on_tab_changed)
        self.corner_widget.setMinimumWidth(10)
        self.corner_widget.setLayout(corner_layout)
        
        # Add tabs to the QTabWidget
        self.tab_widget_for_preview.setCornerWidget(self.corner_widget)
        self.tab_widget_for_preview.addTab(mark_preview_tab, "Markdown Preview")
        self.tab_widget_for_preview.addTab(html_preview_tab, "HTML Preview")
            
        self.splitter.addWidget(self.text_edit)
        self.splitter.addWidget(self.tab_widget_for_preview)
        self.splitter.setSizes([200, 500, 500])

        footer_layout = QHBoxLayout()

        left_widget = QWidget()
        self.left_layout = QHBoxLayout(left_widget)
        self.left_layout.setAlignment(Qt.AlignLeft)

        # 🔹 Right Layout (Main Content)
        right_widget = QWidget()
        self.right_layout = QHBoxLayout(right_widget)

        self.run_command = QPushButton(QtGui.QIcon("ME_Icons/runcmd.png"), "")
        self.run_command.setFixedSize(35,35)
        self.run_command.setShortcut(QtGui.QKeySequence("Return"))
        self.run_command.clicked.connect(self.run_command_function)
        self.run_command.setStyleSheet("""
        QPushButton{
                                 border-radius:10px;
                                 border:1px solid #ccc;
                          padding:3px;}
QPushButton:hover{
                          border:2px solid qlineargradient(spread:reflect, x1:0.203, y1:0, x2:1, y2:0, stop:0 rgba(241, 140, 208, 255), stop:0.168539 rgba(0, 164, 255, 255), stop:0.573034 rgba(157, 0, 255, 255), stop:1 rgba(0, 3, 255, 255));;;
                          color:qlineargradient(spread:reflect, x1:0.203, y1:0, x2:1, y2:0, stop:0 rgba(241, 140, 208, 255), stop:0.168539 rgba(0, 164, 255, 255), stop:0.573034 rgba(157, 0, 255, 255), stop:1 rgba(0, 3, 255, 255));;;
                          }
        """)
        self.run_command.hide()

        self.command_line = QLineEdit()
        self.command_line.hide()
        self.command_line.setPlaceholderText(f"Enter your command here.")
        self.command_line.setStyleSheet("""
        border-radius:10px;
background:white;
padding:3px;
font-size:17px;
border:2px solid;
border-color: qlineargradient(spread:reflect, x1:0.203, y1:0, x2:1, y2:0, stop:0 rgba(241, 140, 208, 255), stop:0.168539 rgba(0, 164, 255, 255), stop:0.573034 rgba(157, 0, 255, 255), stop:1 rgba(0, 3, 255, 255));;
        """)
        footer_layout.addWidget(self.command_line)
        footer_layout.addWidget(self.run_command)
        
        self.file_toolbar = QToolBar("File Toolbar")
        self.file_toolbar.setFixedHeight(40)
        self.file_toolbar.setMovable(False)   
        
        self.toggle_treeview_action = QAction(QtGui.QIcon("ME_Icons/filedd.png"),"File Tree", self)
        self.toggle_treeview_action.triggered.connect(self.toggle_tree_view)
        self.toggle_treeview_action.setToolTip("File tree")
        self.toggle_treeview_action.setCheckable(True)
        #self.file_toolbar.addAction(self.toggle_treeview_action)

        self.open_action = QAction(QtGui.QIcon("ME_Icons/open.png"),"Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.open_action.setToolTip("Open a document")  # Set tooltip
        self.open_action.setShortcut("Ctrl+O")  # Set shortcut
        self.file_toolbar.addAction(self.open_action)

        self.file_toolbar.addSeparator()
        
        self.save_action = QAction(QtGui.QIcon("ME_Icons/save.png"),"Save", self)
        self.save_action.triggered.connect(self.save_file)
        self.save_action.setToolTip("Save the current document")  # Set tooltip
        self.save_action.setShortcut("Ctrl+S")  # Set shortcut
        self.file_toolbar.addAction(self.save_action)

        self.save_as_action = QAction(QtGui.QIcon("ME_Icons/saveas.png"),"Save As", self)
        self.save_as_action.triggered.connect(self.save_file_as)
        self.save_as_action.setToolTip("Save the current document with new name")  # Set tooltip
        self.save_as_action.setShortcut("Ctrl+Shift+S")  # Set shortcut
        self.file_toolbar.addAction(self.save_as_action)

        self.save_pdf_action = QAction("Save Preview As PDF", self)
        self.save_pdf_action.setIcon(QtGui.QIcon("ME_Icons/prepdf.png"))  # Optional icon
        self.save_pdf_action.setToolTip("Save the preview as pdf")
        self.save_pdf_action.triggered.connect(self.save_as_pdf)
        self.file_toolbar.addAction(self.save_pdf_action)

        self.file_toolbar.addSeparator()

        self.new_action = QAction(QtGui.QIcon("ME_Icons/newwin.png"),"New Window", self)
        self.new_action.triggered.connect(self.new)
        self.new_action.setToolTip("New window")
        self.file_toolbar.addAction(self.new_action)

        self.file_toolbar.addSeparator()

        self.template_action = QAction(QtGui.QIcon("ME_Icons/templates.png"),"Templates", self)
        self.template_action.triggered.connect(self.open_template_dialog)
        self.template_action.setToolTip("Templates")
        self.template_action.setStatusTip("Templates")
        self.file_toolbar.addAction(self.template_action)

        self.file_toolbar.addSeparator()

        self.close_save_action = QAction(QtGui.QIcon("ME_Icons/saveclose.png"), "Close File", self)
        self.close_save_action.triggered.connect(self.save_and_close)
        self.close_save_action.setToolTip("Close and save file")
        self.file_toolbar.addAction(self.close_save_action)

        self.close_window = QAction(QtGui.QIcon("ME_Icons/closewindow.png"),"Close Window",self)
        self.close_window.triggered.connect(self.close)
        self.close_window.setToolTip("Close window")
        self.file_toolbar.addAction(self.close_window)

        self.toggle_command_line_action = QAction(QtGui.QIcon("ME_Icons/cmdline.png"),"Toggle command line", self)
        self.toggle_command_line_action.triggered.connect(self.toggle_command_line)
        self.toggle_command_line_action.setToolTip("Toggle command line")
        self.toggle_command_line_action.setStatusTip("Toggle command line")
        self.toggle_command_line_action.setShortcut("Ctrl+/")
        #self.file_toolbar.addAction(self.toggle_command_line_action)

        self.toggle_mode_action = QAction(QtGui.QIcon("ME_Icons/togglemode.png"),'Toggle Mode', self)
        self.toggle_mode_action.triggered.connect(self.toggle_mode)
        self.toggle_mode_action.setToolTip("Toggle live preview between light and dark mode")  # Set tooltip
        self.toggle_mode_action.setShortcut("Ctrl+D")
        self.is_dark_mode = False

        self.file_toolbar.layout().setSpacing(5)  # Sets spacing between items
        self.file_toolbar.layout().setContentsMargins(5, 5, 5, 5)

        self.file_toolbar.setStyleSheet("""
    QToolBar {
    
        background-color: #fafafa;
        border-radius: 8px;
                                        margin-top:0px;
                                        margin-left:0px;
                                        margin-right:0px;
                                        margin-bottom:0px;
                                        padding:0px;
                                        border:1px solid rgb(234, 234, 234);
    }
    
    QToolButton {
        background-color: #fafafa;
        border: none;
        padding: 1px;
        margin-left:2px;
        margin-right:2px;
        margin-bottom:5px;
        margin-top:5px;
                                        border-radius:8px;
    }

    QToolButton:hover {
        background-color: #dbdcde;
    }
""")
        self.edit_toolbar = QToolBar("Edit Toolbar")
        self.edit_toolbar.setFixedHeight(40)
        self.edit_toolbar.setMovable(False)   
        self.edit_toolbar.layout().setSpacing(5)  # Sets spacing between items
        self.edit_toolbar.layout().setContentsMargins(5, 5, 5, 5)

        self.undo_action = QAction(QIcon("ME_Icons/undo.png"), "Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")  # Set shortcut
        self.undo_action.setToolTip("Undo the last action")
        self.undo_action.triggered.connect(lambda: self.text_edit.undo())
        
        # Add 'Redo' action
        self.redo_action = QAction(QIcon("ME_Icons/redo.png"), "Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")  # Set shortcut
        self.redo_action.setToolTip("Redo the last undone action")
        self.redo_action.triggered.connect(lambda: self.text_edit.redo())

        self.edit_toolbar.addAction(self.undo_action)
        self.edit_toolbar.addAction(self.redo_action)

        self.edit_toolbar.addSeparator()

        self.cut_action = QAction(QtGui.QIcon("ME_Icons/cut.png"),'Cut', self)
        self.cut_action.setShortcut('Ctrl+X')
        self.cut_action.setToolTip("Cut the text from the editor")
        self.cut_action.triggered.connect(self.text_edit.cut)
        self.edit_toolbar.addAction(self.cut_action)

        self.copy_action = QAction(QtGui.QIcon("ME_Icons/copy.png"),'Copy', self)
        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.setToolTip("Copy the text from the editor")
        self.copy_action.triggered.connect(self.text_edit.copy)
        self.edit_toolbar.addAction(self.copy_action)

        self.paste_action = QAction(QtGui.QIcon("ME_Icons/paste.png"),'Paste', self)
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.setToolTip("Paste the text from clipboard") # Set shortcut
        self.paste_action.triggered.connect(self.text_edit.paste)
        self.edit_toolbar.addAction(self.paste_action)

        self.selectall_action = QAction(QIcon("ME_Icons/selectall.png"), "Select All", self)
        self.selectall_action.setShortcut("Ctrl+Y")  # Set shortcut
        self.selectall_action.setToolTip("Select all text in the editor")
        self.selectall_action.triggered.connect(self.text_edit.selectAll)
        self.edit_toolbar.addAction(self.selectall_action)

        self.clear_action = QAction(QIcon("ME_Icons/clear.png"), "Clear", self)
        self.clear_action.setShortcut("Ctrl+Y")  # Set shortcut
        self.clear_action.setToolTip("Clear all text from the editor")
        self.clear_action.triggered.connect(self.text_edit.clear)
        self.edit_toolbar.addAction(self.clear_action)

        self.edit_toolbar.addSeparator()

        self.find_replace_action = QAction(QtGui.QIcon("ME_Icons/findandreplace.png"),"Find and Replace", self)
        self.find_replace_action.triggered.connect(self.show_find_replace_dialog)
        self.edit_toolbar.addAction(self.find_replace_action)

        self.edit_toolbar.addSeparator()

        self.indent_action = QAction(QtGui.QIcon("ME_Icons/indent.png"),"Indent", self)
        self.indent_action.triggered.connect(self.indent_text)
        self.edit_toolbar.addAction(self.indent_action)

        self.dedent_action = QAction(QtGui.QIcon("ME_Icons/dedent.png"),"Dedent", self)
        self.dedent_action.triggered.connect(self.dedent_text)
        self.edit_toolbar.addAction(self.dedent_action)

        self.edit_toolbar.addSeparator()

        self.comment_action = QAction(QtGui.QIcon("ME_Icons/comment.png"),"Comment", self)
        self.comment_action.triggered.connect(self.insert_comment)
        self.comment_action.setToolTip("Comment selected text")
        self.edit_toolbar.addAction(self.comment_action)

        self.uncomment_action = QAction(QtGui.QIcon("ME_Icons/uncomment.png"),"Uncomment", self)
        self.uncomment_action.triggered.connect(self.remove_comment)
        self.uncomment_action.setToolTip("Uncomment selected text")
        self.edit_toolbar.addAction(self.uncomment_action)

        self.edit_toolbar.addSeparator()

        self.selection_combo = QComboBox(self)
        self.selection_combo.setStyleSheet("""
            QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
margin-top:5px;
                font-size: 15px;
                height:20px;
                background-color: white;
                selection-background-color:transparent;
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
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png);
                background-repeat: no-repeat;
                background-position: right 10px center;
            }
            QComboBox:hover {
                border:1px solid #ccc;
                selection-background-color: white;
                selection-color: white;
            }
            
        """)

        # Add items to the ComboBox
        selection_items = [
            "Paragraph Formatting",
            "Jump to Top",
            "Jump to Selection",
            "Jump to Bottom",
            "Jump to Line Start",
            "Jump to Line End",
            "Duplicate Line"
        ]

        self.selection_combo.addItems(selection_items)
        self.selection_combo.setCurrentIndex(0)
        # Connect the selection change to respective functions
        self.selection_combo.currentIndexChanged.connect(self.handle_selection)
        self.edit_toolbar.addWidget(self.selection_combo)   

        self.edit_toolbar.setStyleSheet("""
    QToolBar {
        background-color: #fafafa;
                                        margin-top:0px;
                                        margin-left:0px;
                                        margin-right:0px;
                                        margin-bottom:0px;
                                        padding:0px;
                                        border-radius: 8px;
                                        border:1px solid rgb(234, 234, 234);
    }
    
    QToolButton {
        background-color: #fafafa;
        border: none;
        padding: 1px;
        margin:2px;
                                        border-radius:8px;
    }

    QToolButton:hover {
        background-color: #dbdcde;
    }
""")

        self.insert_toolbar = QToolBar("Insert Toolbar")
        self.insert_toolbar.setFixedHeight(40)
        self.insert_toolbar.setMovable(False)   
        self.insert_toolbar.layout().setSpacing(5)  # Sets spacing between items
        self.insert_toolbar.layout().setContentsMargins(5, 5, 5, 5)

        self.tool_button = QToolButton(self)
        self.tool_button.setText("Date & Time")
        self.tool_button.setIcon(QIcon("ME_Icons/datetime.png"))
        # Create a dropdown menu
        menu = QMenu(self)

        # Add actions to the menu
        action_date = QAction("Insert Current Date", self)
        action_time = QAction("Insert Current Time", self)
        action_datetime = QAction("Insert Current Date and Time", self)
        action_custom = QAction("Customize Date and Time...", self)

        # Connect actions to functions (assuming self.text_edit exists)
        action_date.triggered.connect(lambda: self.text_edit.textCursor().insertText(date.today().strftime("%A, %d %B %Y")))
        action_time.triggered.connect(lambda: self.text_edit.textCursor().insertText(QDateTime.currentDateTime().toString("hh:mm:ss AP")))
        action_datetime.triggered.connect(lambda: self.text_edit.textCursor().insertText(f"{date.today().strftime('%A, %d %B %Y')}, {QDateTime.currentDateTime().toString('hh:mm:ss AP')}"))
        action_custom.triggered.connect(self.calendershow)  # Opens calendar for customization

        # Add actions to menu
        menu.addAction(action_date)
        menu.addAction(action_time)
        menu.addAction(action_datetime)
        menu.addAction(action_custom)

        # Set the menu to the tool button
        self.tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self.tool_button.setMenu(menu)
        self.tool_button.clicked.connect(self.calendershow)
        self.tool_button.setStyleSheet("""
                                       QToolButton {
                                       padding-right:13px;
            }
            QToolButton::menu-indicator {
                image: url("C:/Users/rishi/OneDrive/Desktop/Brightness_Files/ME_Icons/dda_down.png");
                width: 16px;
                height: 16px;
                subcontrol-origin: border;
                subcontrol-position: center right;
                padding-right: 8px;
            }
            QToolButton::menu-button {
        border: none;
        width: 15px; /* Adjust size */
        background: #fafafa;
                                       border-top-right-radius:8px;
                                       border-bottom-right-radius:8px;
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
        self.insert_toolbar.addWidget(self.tool_button)

        self.link_action = QAction(QtGui.QIcon("ME_Icons/link.png"),"Add Link", self)
        self.link_action.triggered.connect(self.show_link_dialog)
        self.link_action.setToolTip("Add a link")
        self.insert_toolbar.addAction(self.link_action)

        self.image_action = QAction(QtGui.QIcon("ME_Icons/image.png"),"Insert Image", self)
        self.image_action.triggered.connect(self.show_image_dialog)
        self.image_action.setToolTip("Add an image")
        self.insert_toolbar.addAction(self.image_action)

        self.table_action = QAction(QtGui.QIcon("ME_Icons/table.png"),"Table", self)
        self.table_action.triggered.connect(self.insert_table_dialog)
        self.table_action.setToolTip("Insert a table")
        self.insert_toolbar.addAction(self.table_action)

        self.add_equation_action = QAction(QtGui.QIcon("ME_Icons/equation.png"),"Equations", self)
        self.add_equation_action.triggered.connect(self.eq_win)
        self.add_equation_action.setToolTip("Add an equation")  # Set tooltip
        self.insert_toolbar.addAction(self.add_equation_action)

        self.insert_toolbar.addSeparator()

        self.admonition_combobox = QComboBox(self)
        self.admonition_combobox.setFixedWidth(80)
        self.admonition_combobox.setToolTip("Add blocks")
        self.admonition_combobox.setStyleSheet("""
QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
margin-top:5px;
                font-size: 15px;
                height:20px;
                background-color: white;
                selection-background-color: transparent;
                selection-color: royalblue;
                padding: 3px;
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
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png);
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
                                               QComboBox QAbstractItemView::item:disabled {
    color: gray;
    background-color: #f0f0f0;
    font-style: italic;
}
            QComboBox:hover {
                border:1px solid #ccc;
                selection-background-color: white;
                selection-color: white;
            }
""")
        self.admonition_combobox.addItems([
            'Blocks', 
            'Quote block', 
            'Inline code block', 
            'Multiline code block',
            'Note block', 
            'Warning block', 
            'Danger block', 
            'Success block', 
            'Info block', 
            'Tip block'
        ])
        
        # Connect the combo box signal
        self.admonition_combobox.currentIndexChanged.connect(self.insert_admonition_from_combobox)
        self.admonition_combobox.setCurrentIndex(0)
        self.insert_toolbar.addWidget(self.admonition_combobox)

        self.section_header_action = QAction(QtGui.QIcon("ME_Icons/sectionheader.png"),"Section Header", self)
        self.section_header_action.triggered.connect(self.show_section_header_dialog)
        self.section_header_action.setToolTip("Add a section header")
        self.insert_toolbar.addAction(self.section_header_action)

        self.toc_action = QAction(QtGui.QIcon("ME_Icons/instoc.png"), 'Insert Table of Contents', self)
        self.toc_action.triggered.connect(self.insert_toc)
        self.toc_action.setToolTip("Insert Table of Contents")
        self.insert_toolbar.addAction(self.toc_action)

        self.prog_bar_action = QAction(QtGui.QIcon("ME_Icons/progbar.png"), 'Insert Progressbar', self)
        self.prog_bar_action.triggered.connect(self.open_progress_bar_dialog)
        self.prog_bar_action.setToolTip("Insert Progress Bar")
        self.insert_toolbar.addAction(self.prog_bar_action)

        self.custom_badge_action = QAction(QtGui.QIcon("ME_Icons/badge.png"), 'Insert Custom Badge', self)
        self.custom_badge_action.triggered.connect(self.custom_badge_dialog)
        self.custom_badge_action.setToolTip("Insert Custom Badge")
        self.insert_toolbar.addAction(self.custom_badge_action)

        self.hr_action = QAction(QtGui.QIcon("ME_Icons/horzline.png"),"Horizontal Line", self)
        self.hr_action.triggered.connect(self.insert_horizontal_line)
        self.hr_action.setToolTip("Add a horizontal line")
        self.insert_toolbar.addAction(self.hr_action)

        self.footnote_action = QAction(QtGui.QIcon("ME_Icons/footnote.png"),"Footnote", self)
        self.footnote_action.triggered.connect(self.insert_footnote)
        self.footnote_action.setToolTip("Add a footnote")
        self.insert_toolbar.addAction(self.footnote_action)

        self.insert_toolbar.setStyleSheet("""
    QToolBar {
        background-color: #fafafa;
                                        margin-top:0px;
                                        margin-left:0px;
                                        margin-right:0px;
                                        margin-bottom:0px;
                                        padding:0px;
                                        border-radius: 8px;
                                        border:1px solid rgb(234, 234, 234);
    }
    
    QToolButton {
        background-color: #fafafa;
        border: none;
        padding: 1px;
        margin:2px;
                                        border-radius:8px;
    }

    QToolButton:hover {
        background-color: #dbdcde;
    }
""")
        
        self.format_toolbar = QToolBar("Format Toolbar")
        self.format_toolbar.setFixedHeight(40)
        self.format_toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.format_toolbar.setMovable(False)
        self.format_toolbar.setIconSize(QSize(22, 22))
        self.format_toolbar.layout().setSpacing(8)  
        self.format_toolbar.layout().setContentsMargins(5, 5, 5, 5)

        self.format_toolbar.setStyleSheet("""
    QToolBar {
        background-color: #fafafa;
                                        margin-top:0px;
                                            margin-left:0px;
                                            margin-right:0px;
                                            margin-bottom:0px;
                                        border-radius: 8px;
                                        border-top:1px solid rgb(234, 234, 234);
                                            border-bottom:1px solid rgb(234, 234, 234);
                                            border-left:1px solid rgb(234, 234, 234);
                                            border-right:1px solid rgb(234, 234, 234);
    }
    
    QToolButton {
        background-color: #fafafa;
        border: none;
        padding: 2px;
        margin-left:2px;
        margin-right:2px;
        margin-bottom:5px;
        margin-top:5px;
                                        border-radius:7px;
    }

    QToolButton:hover {
        background-color: #dbdcde;
    }
""")

        self.bold_action = QAction(QtGui.QIcon("ME_Icons/bold.png"),"Bold", self)
        self.bold_action.triggered.connect(self.make_bold)
        self.bold_action.setToolTip("Bold the text")  # Set tooltip
        self.bold_action.setShortcut("Ctrl+B")  # Set shortcut
        
        self.italic_action = QAction(QtGui.QIcon("ME_Icons/itallic.png"),"Italic", self)
        self.italic_action.triggered.connect(self.make_italic)
        self.italic_action.setToolTip("Italic the text")  # Set tooltip
        self.italic_action.setShortcut("Ctrl+I")  # Set shortcut
        
        self.bold_italic_action = QAction(QtGui.QIcon("ME_Icons/bolditallic.png"),"Bold Italic", self)
        self.bold_italic_action.triggered.connect(self.make_bold_italic)
        self.bold_italic_action.setToolTip("Bold and italic the text")  # Set tooltip
        self.bold_italic_action.setShortcut("Ctrl+Shift+B")  # Set shortcut
        
        self.strikethrough_action = QAction(QtGui.QIcon("ME_Icons/strickout.png"),"Strikethrough", self)
        self.strikethrough_action.triggered.connect(self.make_strikethrough)
        self.strikethrough_action.setToolTip("Strickout the text")  # Set tooltip
        self.strikethrough_action.setShortcut("Ctrl+Alt+S")  # Set shortcut

        self.highlight_action = QAction(QtGui.QIcon("ME_Icons/highlight.png"),"Highlight", self)
        self.highlight_action.triggered.connect(self.highlight_text)
        self.highlight_action.setToolTip("Highlight selected text")

        self.subscript_action = QAction(QtGui.QIcon("ME_Icons/subscript.png"),"Subscript", self)
        self.subscript_action.triggered.connect(self.make_subscript)
        self.subscript_action.setToolTip("Subscript selected text")

        self.superscript_action = QAction(QtGui.QIcon("ME_Icons/superscript.png"),"Superscript", self)
        self.superscript_action.triggered.connect(self.make_superscript)
        self.superscript_action.setToolTip("Superscript selected text")

        self.format_toolbar.addAction(self.bold_action)
        self.format_toolbar.addAction(self.italic_action)
        self.format_toolbar.addAction(self.bold_italic_action)
        self.format_toolbar.addAction(self.strikethrough_action)
        self.format_toolbar.addAction(self.highlight_action)
        self.format_toolbar.addAction(self.subscript_action)
        self.format_toolbar.addAction(self.superscript_action)

        line_break_action = QAction(QtGui.QIcon("ME_Icons/linebreak.png"),"Insert Line Break", self)
        line_break_action.triggered.connect(lambda: self.text_edit.insertPlainText("<br>"))
        self.format_toolbar.addAction(line_break_action)

        self.case_combobox = QComboBox(self)
        self.case_combobox.setFixedWidth(100)
        self.case_combobox.addItems(["Text Case", "UPPERCASE", "lowercase", "Swapcase", "Title"])
    
        self.case_combobox.currentIndexChanged.connect(self.change_text_case)
        self.case_combobox.setStyleSheet("""
QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
margin-top:5px;
                font-size: 15px;
                height:20px;
                background-color: white;
                selection-background-color:transparent;
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
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png);
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
        self.format_toolbar.addWidget(self.case_combobox)

        self.header_combo = QComboBox()
        self.header_combo.setFixedWidth(93)
        self.header_combo.addItems(["Headers", "Header 1", "Header 2", "Header 3", "Header 4", "Header 5", "Header 6"])
        self.header_combo.setToolTip("Add header (h1,h2,h3,h4,h5,h6)")
        self.header_combo.currentIndexChanged.connect(self.apply_header)
        self.header_combo.setStyleSheet("""
QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
margin-top:5px;
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
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png);
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
        self.format_toolbar.addWidget(self.header_combo)

        self.checklist_combo = QComboBox()
        self.checklist_combo.setFixedWidth(103)
        self.checklist_combo.addItems(["Checklists", "Unchecked Checklist", "Checked Checklist"])
        self.checklist_combo.setToolTip("Add checklist")
        self.checklist_combo.currentIndexChanged.connect(self.apply_checklist)
        self.checklist_combo.setStyleSheet("""
QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
margin-top:5px;
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
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png);
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
        self.format_toolbar.addWidget(self.checklist_combo)
        
        self.list_combo = QComboBox()
        self.list_combo.setFixedWidth(70)
        self.list_combo.addItems(["Lists", "Ordered List", "Unordered List", "Defination List"])
        self.list_combo.setToolTip("Add list")
        self.list_combo.currentIndexChanged.connect(self.apply_list)
        self.list_combo.setStyleSheet("""
QComboBox {
margin-left: 5px;
margin-right: 5px;
margin-bottom:5px;
margin-top:5px;
                font-size: 15px;
                height:20px;
                background-color: white;
                selection-background-color: transparent;
                selection-color: royalblue;
                padding: 3px;
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
                image: url(C:/Users/rishi_7b5nghb/Desktop/Brightness_Files/ME_Icons/dda_down.png);
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
                                      QComboBox QAbstractItemView::item:disabled {
    color: gray;
    background-color: #f0f0f0;
    font-style: italic;
}
            QComboBox:hover {
                border:1px solid #ccc;
                selection-background-color: white;
                selection-color: white;
            }
""")
        self.format_toolbar.addWidget(self.list_combo)
        
        self.format_toolbar.addSeparator()

        self.clear_formatting_action = QAction(QtGui.QIcon("ME_Icons/clearformat.png"),"Clear Formatting", self)
        self.format_toolbar.addAction(self.clear_formatting_action)
        self.clear_formatting_action.triggered.connect(self.clear_formatting)

        self.toggle_treeview_action.setStatusTip("File tree")
        self.save_action.setStatusTip("Save the current document")
        self.save_as_action.setStatusTip("Save the current document with new name")
        self.save_pdf_action.setStatusTip("Save the previewself. as pdf")
        self.new_action.setStatusTip("Open new window")
        self.open_action.setStatusTip("Open a document")
        self.cut_action.setStatusTip("Cut the text from the editor")
        self.copy_action.setStatusTip("Copy the text from the editor")
        self.paste_action.setStatusTip("Paste the text from clipboard")
        self.selectall_action.setStatusTip("Select all text in the editor")
        self.clear_action.setStatusTip("Clear all text from the editor")
        self.undo_action.setStatusTip("Undo the last action")
        self.redo_action.setStatusTip("Redo the last undone action")
        self.toggle_command_line_action.setStatusTip("Toggle command line")
        self.toggle_mode_action.setStatusTip("Toggle live preview between light and dark mode")
        self.bold_action.setStatusTip("Bold the text")
        self.custom_badge_action.setStatusTip("Add a custom badge")
        self.italic_action.setStatusTip("Italic the text")
        self.bold_italic_action.setStatusTip("Bold and italic the text")
        self.strikethrough_action.setStatusTip("Strikethrough the text")
        self.highlight_action.setStatusTip("Highlight selected text")
        self.subscript_action.setStatusTip("Subscript selected text")
        self.superscript_action.setStatusTip("Superscript selected text")
        self.section_header_action.setStatusTip("Add a section header")
        self.link_action.setStatusTip("Add a link")
        self.image_action.setStatusTip("Add an image")
        self.table_action.setStatusTip("Insert a table")
        self.add_equation_action.setStatusTip("Add an equation")
        self.footnote_action.setStatusTip("Add a footnote")
        self.admonition_combobox.setStatusTip("Add block")
        self.toc_action.setStatusTip("Insert Table of Contents")
        self.prog_bar_action.setStatusTip("Insert Progress Bar")
        self.hr_action.setStatusTip("Add a horizontal line")
        self.comment_action.setStatusTip("Comment selected text")
        self.uncomment_action.setStatusTip("Uncomment selected text")

        # For QComboBox objects
        self.header_combo.setStatusTip("Add header (h1,h2,h3,h4,h5,h6)")
        self.checklist_combo.setStatusTip("Add checklist")
        self.list_combo.setStatusTip("Add list")

        self.view_toolbar = QToolBar("View Toolbar")
        self.view_toolbar.setFixedHeight(40)
        self.view_toolbar.setMovable(False)   
        self.view_toolbar.layout().setSpacing(5)  # Sets spacing between items
        self.view_toolbar.layout().setContentsMargins(5, 5, 5, 5)

        # Existing Actions
        self.toggle_ribbon = QAction(QtGui.QIcon("ME_Icons/ribbon.png"), '', self)
        self.toggle_ribbon.setCheckable(True)
        self.toggle_ribbon.setChecked(self.load_ribbon_settings())
        self.toggle_ribbon.triggered.connect(self.toggle_ribbon_function)

        self.last_active_toolbar = self.edit_toolbar
        saved_state = self.load_ribbon_settings()
        self.toggle_ribbon.setChecked(saved_state)

        # Ensure ribbon is hidden on startup if it was previously hidden
        if saved_state:  
            self.toggle_ribbon_function(True)

        self.editor_view_action = QAction(QtGui.QIcon("ME_Icons/editview.png"), '', self)
        self.editor_view_action.setCheckable(True)
        self.editor_view_action.setChecked(False)
        self.editor_view_action.triggered.connect(self.enable_editor_view)

        self.preview_view_action = QAction(QtGui.QIcon("ME_Icons/fullpreview.png"), '', self)
        self.preview_view_action.setCheckable(True)
        self.preview_view_action.setChecked(False)
        self.preview_view_action.triggered.connect(self.enable_preview_view)

        self.splitter_orient = QAction(QtGui.QIcon("ME_Icons/switchor.png"), '', self)
        self.splitter_orient.setCheckable(True)
        self.splitter_orient.toggled.connect(self.save_view_checks_settings)
        self.splitter_orient.setChecked(False)
        self.splitter_orient.triggered.connect(self.splitter_or_func)

        self.hide_file_label = QAction(QtGui.QIcon("ME_Icons/hidefilepath.png"), '', self)
        self.hide_file_label.setCheckable(True)
        self.hide_file_label.toggled.connect(self.save_view_checks_settings)
        self.hide_file_label.setChecked(False)
        self.hide_file_label.triggered.connect(self.hide_file_label_func)

        self.clean_mode = QAction(QtGui.QIcon("ME_Icons/cleanview.png"), '', self)
        self.clean_mode.setCheckable(True)
        self.hide_file_label.toggled.connect(self.save_view_checks_settings)
        self.clean_mode.setChecked(False)
        self.clean_mode.triggered.connect(self.enable_clean_view)

        # Full Screen Action
        self.fullscreen_action = QAction(QtGui.QIcon("ME_Icons/fullscreen.png"), '', self)
        self.fullscreen_action.setCheckable(True)  # Make it toggleable
        self.fullscreen_action.toggled.connect(self.save_view_checks_settings)
        self.fullscreen_action.setChecked(False)   # Initially not checked (normal window)
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)

        esc_shortcut = QShortcut(QKeySequence("Esc"), self)
        esc_shortcut.activated.connect(self.toggle_fullscreen_via_esc)

        # Add actions to the "View" menu
        self.view_toolbar.addAction(self.toggle_ribbon)
        self.view_toolbar.addSeparator()
        self.view_toolbar.addAction(self.editor_view_action)
        self.view_toolbar.addAction(self.preview_view_action)
        self.view_toolbar.addAction(self.clean_mode)
        self.view_toolbar.addSeparator()
        self.view_toolbar.addAction(self.splitter_orient)
        self.view_toolbar.addSeparator()
        self.view_toolbar.addAction(self.hide_file_label)
        self.view_toolbar.addSeparator()
        self.view_toolbar.addAction(self.fullscreen_action)

        self.view_toolbar.setStyleSheet("""
    QToolBar {
        background-color: #fafafa;
                                        margin-top:0px;
                                        margin-left:0px;
                                        margin-right:0px;
                                        margin-bottom:0px;
                                        padding:0px;
                                        border-radius: 8px;
                                        border:1px solid rgb(234, 234, 234);
    }
    
    QToolButton {
        background-color: #fafafa;
        border: none;
        padding: 1px;
        margin:2px;
                                        border-radius:8px;
    }

    QToolButton:hover {
        background-color: #dbdcde;
    }
    QToolButton:checked {
        background-color: #dbdcde;
    }
""")

        self.addToolBar(Qt.TopToolBarArea,self.format_toolbar)
        self.addToolBar(Qt.TopToolBarArea,self.file_toolbar)
        self.addToolBar(Qt.TopToolBarArea,self.edit_toolbar)
        self.addToolBar(Qt.TopToolBarArea,self.insert_toolbar)
        self.addToolBar(Qt.TopToolBarArea,self.view_toolbar)

        middle_layout = QHBoxLayout()

        self.activity_toolbar = QToolBar("Activity Toolbar")
        self.activity_toolbar.setMovable(False)   
        self.activity_toolbar.setIconSize(QSize(27, 27))
        self.activity_toolbar.setFixedWidth(45)
        self.activity_toolbar.setOrientation(Qt.Vertical)

        self.activity_toolbar.addAction(self.toggle_treeview_action)

        self.toggle_outline_action = QAction(QtGui.QIcon("ME_Icons/toc.png"),"", self)
        self.toggle_outline_action.setCheckable(True)
        self.toggle_outline_action.triggered.connect(self.toggle_outline)
        self.activity_toolbar.addAction(self.toggle_outline_action)  

        self.activity_toolbar.addAction(self.find_replace_action)

        self.activity_toolbar.setStyleSheet("""
    QToolBar {
        background-color: #fafafa;
                                        margin-top:0px;
                                        margin-left:0px;
                                        margin-right:0px;
                                        margin-bottom:0px;
                                        padding:3px;
                                        border-radius: 8px;
                                        border:1px solid rgb(234, 234, 234);
    }
    
    QToolButton {
        background-color: #fafafa;
        border: none;
        padding: 4px;
        border-radius:8px;
    }

    QToolButton:hover {
        background-color: #dbdcde;
    }
    QToolButton:checked {
        background-color: #dbdcde;
        border-left:3px solid royalblue;
    }
""")
        
        print_markdown_action = QAction("Print Markdown", self)
        print_markdown_action.triggered.connect(self.print_markdown)

        print_preview_action = QAction("Print Preview", self)
        print_preview_action.triggered.connect(self.print_preview)

        self.format_toolbar.hide()
        self.file_toolbar.hide()
        self.edit_toolbar.show()
        self.insert_toolbar.hide()
        self.view_toolbar.hide()
        
        self.top_layout.addWidget(self.file_toolbar)
        self.top_layout.addWidget(self.format_toolbar)
        self.top_layout.addWidget(self.edit_toolbar)
        self.top_layout.addWidget(self.insert_toolbar)
        self.top_layout.addWidget(self.view_toolbar)

        self.outline_frame = QFrame(self)
        self.outline_frame.setStyleSheet("""
border:none;
                                         border-radius:8px;
                                         background:#f2f2f2;
""")
        self.outline_frame.setFixedWidth(300)
        self.outline_frame.setFrameShape(QFrame.StyledPanel)
        self.outline_frame.hide()

        # List widget inside outline frame
        self.outline_list = QTreeWidget()
        self.outline_list.setHeaderHidden(True)
        self.outline_list.itemClicked.connect(self.scroll_to_outline_position)
        self.outline_list.setStyleSheet(""" 
QTreeWidget {
    background: #f2f2f2;
    font-size:16px;
    color: black;
}
QTreeWidget::item {
    margin: 1px;
    padding: 3px;
}
QTreeWidget::item:selected {
    background-color: #f2f2f2;
    color: royalblue;
    font-weight: bold;
}
QTreeWidget::item:hover {
    background: #f2f2f2;
    color: royalblue;
}
QScrollBar:vertical {
    background: #eeeeee;
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #b0b0b0;
    min-height: 10px;
    border-radius: 3px;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: #e3e5e9;
    height: 0px;
}
QScrollBar:horizontal {
    background: #e3e5e9;
    height: 9px;
}
QScrollBar::handle:horizontal {
    background: #b0b0b0;
    min-width: 15px;
    border-radius: 4px;
}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    background: #e3e5e9;
    width: 0px;
}
""")

        outline_layout = QVBoxLayout(self.outline_frame)
        self.expand_checkbox = QCheckBox("Expand All")
        self.expand_checkbox.setChecked(True)
        self.expand_checkbox.setStyleSheet("""
QCheckBox {
    spacing: 6px;
}
QCheckBox::indicator:checked:enabled {
    image: url(:/qt-project.org/styles/commonstyle/images/checkbox_checked.png);
}
QCheckBox::indicator {
    width: 13px;
    height: 13px;
    border-radius: 4px;
    border: 1px solid #aaa;
    background-color: transparent;
}
QCheckBox::indicator:checked {
    background-color: #dcdcdc;  /* light grey when checked */
    border: 1px solid #888;
}
""")
        self.expand_checkbox.stateChanged.connect(self.toggle_outline_expansion)
        outline_layout.addWidget(self.expand_checkbox)
        outline_layout.addWidget(self.outline_list)

        self.outline_timer = QTimer()
        self.outline_timer.setSingleShot(True)
        self.outline_timer.timeout.connect(self.update_outline)

        self.right_layout.addWidget(self.splitter)
  
        middle_layout.addWidget(self.activity_toolbar, 1)
        middle_layout.addWidget(self.outline_frame, 2)
        middle_layout.addWidget(right_widget, 3)
        
        self.main_layout.addWidget(self.top_container)
        self.main_layout.addLayout(header_layout)
        self.main_layout.addLayout(middle_layout)
        self.main_layout.addLayout(footer_layout)

        self.restore_settings()
        self.showMaximized()

    def handle_markdown_selection(self, text):
        if text == "Default Markdown":
            self.bold_action.setVisible(True)
            self.italic_action.setVisible(True)
            self.bold_italic_action.setVisible(True)
            self.strikethrough_action.setVisible(True)
            self.highlight_action.setVisible(True)
            self.subscript_action.setVisible(True)
            self.superscript_action.setVisible(True)
            self.header_combo.setVisible(True)
            self.checklist_combo.setFixedWidth(103)

            #list
            self.list_combo.clear()
            self.list_combo.setCurrentIndex(0)
            self.list_combo.addItems(["Lists", "Ordered List", "Unordered List", "Defination List"])

            #admonition
            self.admonition_combobox.setCurrentIndex(0)
            self.admonition_combobox.clear()
            self.admonition_combobox.setCurrentIndex(0)
            self.admonition_combobox.addItems([
            'Blocks', 
            'Quote block', 
            'Inline code block', 
            'Multiline code block',
            'Note block', 
            'Warning block', 
            'Danger block', 
            'Success block', 
            'Info block', 
            'Tip block'
        ])

            self.section_header_action.setVisible(True)
            self.toc_action.setVisible(True)
            self.prog_bar_action.setVisible(True)
            self.custom_badge_action.setVisible(True)
            self.hr_action.setVisible(True)
            self.footnote_action.setVisible(True)
            self.link_action.setVisible(True)
            self.image_action.setVisible(True)
            self.table_action.setVisible(True)
            self.add_equation_action.setVisible(True)

        elif text == "Basic Markdown":
            self.bold_action.setVisible(True)
            self.italic_action.setVisible(True)
            self.bold_italic_action.setVisible(True)
            self.strikethrough_action.setVisible(False)
            self.highlight_action.setVisible(False)
            self.subscript_action.setVisible(False)
            self.superscript_action.setVisible(False)
            self.header_combo.setVisible(True)
            self.checklist_combo.setFixedWidth(0)

            #list
            self.list_combo.clear()
            self.list_combo.setCurrentIndex(0)
            self.list_combo.addItems(["Lists", "Ordered List", "Unordered List"])

            #admonition
            self.admonition_combobox.setCurrentIndex(0)
            self.admonition_combobox.clear()
            self.admonition_combobox.setCurrentIndex(0)
            self.admonition_combobox.addItems([
            'Blocks', 
            'Quote block', 
            'Inline code block', 
            'Multiline code block',
        ])

            self.section_header_action.setVisible(False)
            self.toc_action.setVisible(False)
            self.prog_bar_action.setVisible(False)
            self.custom_badge_action.setVisible(False)
            self.hr_action.setVisible(True)
            self.footnote_action.setVisible(False)
            self.link_action.setVisible(True)
            self.image_action.setVisible(True)
            self.table_action.setVisible(False)
            self.add_equation_action.setVisible(False)

        elif text == "Advanced Markdown":
            self.bold_action.setVisible(True)
            self.italic_action.setVisible(True)
            self.bold_italic_action.setVisible(True)
            self.strikethrough_action.setVisible(True)
            self.highlight_action.setVisible(True)
            self.subscript_action.setVisible(True)
            self.superscript_action.setVisible(True)
            self.header_combo.setVisible(True)
            self.checklist_combo.setFixedWidth(103)

            #list
            self.list_combo.clear()
            self.list_combo.setCurrentIndex(0)
            self.list_combo.addItems(["Lists", "Ordered List", "Unordered List", "Defination List"])

            #admonition
            self.admonition_combobox.setCurrentIndex(0)
            self.admonition_combobox.clear()
            self.admonition_combobox.setCurrentIndex(0)
            self.admonition_combobox.addItems([
            'Blocks', 
            'Quote block', 
            'Inline code block', 
            'Multiline code block',
        ])

            self.section_header_action.setVisible(False)
            self.toc_action.setVisible(True)
            self.prog_bar_action.setVisible(False)
            self.custom_badge_action.setVisible(False)
            self.hr_action.setVisible(True)
            self.footnote_action.setVisible(True)
            self.link_action.setVisible(True)
            self.image_action.setVisible(True)
            self.table_action.setVisible(True)
            self.add_equation_action.setVisible(True)

    def start_label_rotation_if_placeholder(self):
        if self.file_label.text() == "•••":
            self.should_rotate = True
            self.suggestion_index = 0

    def rotate_label(self):
        self.update_file_label_info()

        if self.file_path == "":
            self.file_label.setText(self.file_suggestions[self.suggestion_index])
            self.suggestion_index = (self.suggestion_index + 1) % len(self.file_suggestions)

    def stop_label_rotation(self):
        self.should_rotate = False

    def toggle_outline_expansion(self, state):
        if state == Qt.Checked:
            self.outline_list.expandAll()
        if state != Qt.Checked:
            self.outline_list.collapseAll()
        else:
            self.outline_list.collapseAll()

    def toggle_outline(self, checked):
        if checked:
            self.outline_frame.show()
            self.schedule_outline_update()
        else:
            self.outline_frame.hide()

    def schedule_outline_update(self):
        self.outline_timer.start(300)  # update after 300ms of inactivity

    def update_outline(self):
        markdown_text = self.text_edit.toPlainText()
        self.outline_list.clear()

        header_pattern = re.compile(r'^(#{1,6})\s*(.+)$', re.MULTILINE)
        header_stack = []

        for match in header_pattern.finditer(markdown_text):
            hashes, title = match.groups()
            level = len(hashes)
            position = match.start()  # position in the document

            item = QTreeWidgetItem([title])
            item.setData(0, Qt.UserRole, position)  # Store position for later

            # Adjust hierarchy based on level
            while header_stack and header_stack[-1][0] >= level:
                header_stack.pop()

            if not header_stack:
                self.outline_list.addTopLevelItem(item)
            else:
                parent_item = header_stack[-1][1]
                parent_item.addChild(item)

            header_stack.append((level, item))

        self.outline_list.expandAll()

    def scroll_to_outline_position(self, item):
        pos = item.data(0, Qt.UserRole)
        if pos is not None:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(pos)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.setFocus()

    def update_toc_tree(self):
        """Extract Markdown headers and update the tree dynamically."""
        self.toc_tree.clear()  # Clear previous entries
        text = self.text_edit.toPlainText()
        lines = text.split("\n")

        parent_items = {1: None, 2: None, 3: None}  # Track parent headers
        positions = {}  # Store cursor positions for headers

        for i, line in enumerate(lines):
            if line.startswith("#"):
                level = line.count("#")  # Header level based on `#` count
                header_text = line.strip("# ").strip()

                if level in [1, 2, 3]:  # Only process H1, H2, H3
                    item = QTreeWidgetItem([header_text])
                    positions[item] = i  # Store cursor line for scrolling

                    if level == 1:
                        self.toc_tree.addTopLevelItem(item)
                        parent_items[1] = item
                    elif level == 2 and parent_items[1]:
                        parent_items[1].addChild(item)
                        parent_items[2] = item
                    elif level == 3 and parent_items[2]:
                        parent_items[2].addChild(item)

        self.toc_tree.expandAll()  # Expand by default
        self.toc_tree.positions = positions  # Store positions for navigation

    def scroll_to_header(self, item):
        """Scroll text edit to the selected header when clicked."""
        line_number = self.toc_tree.positions.get(item, 0)
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.Start)  # Move to start
        for _ in range(line_number):
            cursor.movePosition(cursor.Down)  # Move to the line
        self.text_edit.setTextCursor(cursor)

    def calendershow(self):
        dialog = Date_And_Time(self)
        dialog.show()

    def toggle_toolbar(self, toolbar, button):
        """Handles toolbar visibility when a tab button is clicked, with ribbon auto-hide support."""
        
        # Hide all toolbars
        self.file_toolbar.hide()
        self.edit_toolbar.hide()
        self.insert_toolbar.hide()
        self.format_toolbar.hide()
        self.view_toolbar.hide()

        # Show only the selected toolbar
        toolbar.show()

        # Set the clicked button as checked
        self.button_group.setExclusive(False)
        button.setChecked(True)
        self.button_group.setExclusive(True)

        # Update the last active toolbar
        self.last_active_toolbar = toolbar  

        # If ribbon auto-hide is enabled, set up mouse tracking
        if self.toggle_ribbon.isChecked():
            toolbar.enterEvent = lambda event: self.cancel_toolbar_hide(toolbar)
            toolbar.leaveEvent = lambda event: self.schedule_toolbar_hide(toolbar)

    def cancel_toolbar_hide(self, toolbar):
        """Cancel scheduled hide when mouse enters the toolbar."""
        if hasattr(toolbar, "hide_timer") and toolbar.hide_timer:
            toolbar.hide_timer.stop()

    def schedule_toolbar_hide(self, toolbar):
        """Schedule hiding the toolbar after 2 seconds when mouse leaves."""
        if not self.toggle_ribbon.isChecked():
            return  # Do nothing if ribbon auto-hide is disabled

        toolbar.hide_timer = QTimer()
        toolbar.hide_timer.setSingleShot(True)
        toolbar.hide_timer.timeout.connect(toolbar.hide)
        toolbar.hide_timer.start(2000)  # Hide after 2 seconds

    def save_ribbon_settings(self):
        """Save ribbon view state to remribbon.json."""
        settings = {"ribbon_view_checked": self.toggle_ribbon.isChecked()}
        with open(REM_RIBBON, "w") as file:
            json.dump(settings, file)

    def load_ribbon_settings(self):
        """Load ribbon view state from remribbon.json."""
        if os.path.exists(REM_RIBBON):
            with open(REM_RIBBON, "r") as file:
                settings = json.load(file)
                return settings.get("ribbon_view_checked", False)  # Default to False if missing
        return False  # Default state

    def toggle_ribbon_function(self, state):
        """Handles ribbon hide/show toggle."""
        if state:  # If ribbon is checked (enabled)
            if hasattr(self, 'last_active_toolbar') and self.last_active_toolbar:
                self.last_active_toolbar.hide()
        else:  # If ribbon is unchecked (disabled)
            if hasattr(self, 'last_active_toolbar') and self.last_active_toolbar:
                self.last_active_toolbar.show()

        self.save_ribbon_settings()  # Save state when toggled

    def handle_selection(self, index):
        if index == 0:
            pass
        elif index == 1:
            self.jump_to_top()
        elif index == 2:
            self.jump_to_selection()
        elif index == 3:
            self.jump_to_bottom()
        elif index == 4:
            self.jump_to_line_start()
        elif index == 5:
            self.jump_to_line_end()
        elif index == 6:
            self.duplicate_line()
        self.selection_combo.setCurrentIndex(0) 

    def duplicate_line(self):
        cursor = self.text_edit.textCursor()  # Get the text cursor
        cursor.select(QTextCursor.LineUnderCursor)  # Select the current line
        line_text = cursor.selectedText()  # Get the line text
        cursor.movePosition(QTextCursor.EndOfBlock)  # Move to the end of the line
        cursor.insertText("\n" + line_text)

    def update_file_label_info(self):
        """Extracts and updates file name and path from the label text."""
        label_text = self.file_label.text()

        if " - " in label_text and "•••" not in label_text:
            base_name, file_path = label_text.replace("<b>", "").replace("</b>", "").split(" - ", 1)
            self.file_base_name = base_name.strip()
            self.file_path = file_path.strip()
        else:
            self.file_base_name = ""
            self.file_path = ""

    def open_file_label_location(self):
        """Opens the file's location in File Explorer and selects it."""
        self.update_file_label_info()  # Ensure self.file_path is updated

        if not self.file_path:
            return  # Exit if no file path is set

        # Ensure the file path is absolute
        file_path = os.path.abspath(self.file_path)
        folder = os.path.dirname(file_path)

        if os.path.exists(folder):
            if sys.platform == "win32":
                subprocess.run(["explorer", "/select,", file_path], check=True)

    def show_file_label_context_menu(self, position):
        """Displays the context menu only when label does not contain '•••'."""
        if "•••" in self.file_label.text() or any(suggestion in self.file_label.text() for suggestion in self.file_suggestions):
            return  # Do not show context menu


        menu = QMenu(self)

        # Copy Path
        copy_path_action = QAction("Copy Path", self)
        copy_path_action.triggered.connect(self.copy_file_label_path)
        menu.addAction(copy_path_action)

        # Open File Location
        open_location_action = QAction("Open File Location", self)
        open_location_action.triggered.connect(self.open_file_label_location)
        menu.addAction(open_location_action)

        # Close and Save File
        save_and_close_action = QAction(QtGui.QIcon("ME_Icons/closeandsavefile.png"),"Close and Save File", self)
        save_and_close_action.triggered.connect(self.save_and_close)
        menu.addAction(save_and_close_action)

        menu.exec(self.mapToGlobal(position))

    def copy_file_label_path(self):
        """Copies the file path to clipboard."""
        if self.file_path:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.file_path, QClipboard.Clipboard)

    def print_markdown(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setDocName("Print Markdown")
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("Print Markdown")
        
        if dialog.exec():
            self.text_edit.print(printer)  # Print text_edit contents

    def print_preview(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setDocName("Print Preview")
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("Print Preview")
        
        if dialog.exec():
            self.preview_browser.page().print(printer, lambda success: None)

    def hide_file_label_func(self):
        if self.hide_file_label.isChecked():
            self.file_label.setVisible(False)
        elif self.hide_file_label.isChecked() == False:
            self.file_label.setVisible(True)

    def save_view_checks_settings(self):
        """Save the checked state of actions to a JSON file."""
        data = {
            "option1": self.splitter_orient.isChecked(),
            "option2": self.hide_file_label.isChecked()
        }
        with open(SETTINGS_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def restore_settings(self):
        """Restore the checked state of actions from a JSON file."""
        if not os.path.exists(SETTINGS_FILE):
            return

        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                content = file.read().strip()  # Remove leading/trailing spaces
                
                if not content:  # Handle empty file
                    return
                
                data = json.loads(content)  # Parse JSON safely

                # Restore settings with default values if keys are missing
                self.splitter_orient.setChecked(data.get("option1", False))
                self.hide_file_label.setChecked(data.get("option2", False))

                # Apply corresponding functions
                if self.splitter_orient.isChecked():
                    self.splitter_or_func()
                elif self.hide_file_label.isChecked():
                    self.hide_file_label_func()

        except json.JSONDecodeError as e:
            return

    def contextMenuEvent_forPresent(self, position):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #f2f2f2;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 2px;
            }

            QMenu::item {
                background-color: transparent;
                color: black;
                padding: 4px;
                margin: 3px;
                width: 150px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background-color: #97B2ED;
                color: black;
            }

            QMenu::item:disabled {
    color: gray;  /* Change text color */
    background: transparent; /* Keep background unchanged */
}

            QMenu::separator {
            }
        """)

        # Navigation Actions
        back_action = QAction("Back", self)
        back_action.setEnabled(self.preview_browser.page().history().canGoBack())
        back_action.triggered.connect(self.preview_browser.back)

        forward_action = QAction("Forward", self)
        forward_action.setEnabled(self.preview_browser.page().history().canGoForward())
        forward_action.triggered.connect(self.preview_browser.forward)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.preview_browser.reload)

        stop_action = QAction("Stop Loading", self)
        stop_action.triggered.connect(self.preview_browser.stop)

        # Zoom Actions
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(lambda: self.preview_browser.setZoomFactor(self.preview_browser.zoomFactor() + 0.1))

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(lambda: self.preview_browser.setZoomFactor(self.preview_browser.zoomFactor() - 0.1))

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.triggered.connect(lambda: self.preview_browser.setZoomFactor(1.0))

        # Exit
        exit_action = QAction("Exit Presentation View", self)
        exit_action.triggered.connect(self.toggle_fullscreen_via_esc)

        # Add actions to menu
        menu.addAction(back_action)
        menu.addAction(forward_action)
        menu.addAction(reload_action)
        menu.addAction(stop_action)
        menu.addSeparator()
        menu.addAction(zoom_in_action)
        menu.addAction(zoom_out_action)
        menu.addAction(reset_zoom_action)
        menu.addSeparator()
        menu.addAction(exit_action)

        # Show menu at cursor position
        menu.exec(self.preview_browser_2.mapToGlobal(position))

    def contextMenuEvent(self,position: QPoint):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #f2f2f2;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 2px;
            }

            QMenu::item {
                background-color: transparent;
                color: black;
                padding: 4px;
                margin: 3px;
                width: 150px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background-color: #97B2ED;
                color: black;
            }

            QMenu::item:disabled {
    color: gray;  /* Change text color */
    background: transparent; /* Keep background unchanged */
}

            QMenu::separator {
            }
        """)

        # Navigation Actions
        back_action = QAction("Back", self)
        back_action.setEnabled(self.preview_browser.page().history().canGoBack())
        back_action.triggered.connect(self.preview_browser.back)

        forward_action = QAction("Forward", self)
        forward_action.setEnabled(self.preview_browser.page().history().canGoForward())
        forward_action.triggered.connect(self.preview_browser.forward)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.preview_browser.reload)

        stop_action = QAction("Stop Loading", self)
        stop_action.triggered.connect(self.preview_browser.stop)

        present_action = QAction("Present", self)
        present_action.triggered.connect(self.update_preview_2)

        # Copy URL
        copy_url_action = QAction("Copy URL", self)
        copy_url_action.triggered.connect(lambda: self.clipboard.setText(self.preview_browser.url().toString()))

        # Zoom Actions
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(lambda: self.preview_browser.setZoomFactor(self.preview_browser.zoomFactor() + 0.1))

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(lambda: self.preview_browser.setZoomFactor(self.preview_browser.zoomFactor() - 0.1))

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.triggered.connect(lambda: self.preview_browser.setZoomFactor(1.0))

        # Save Page as PDF
        save_pdf_action = QAction("Save Page as PDF", self)
        save_pdf_action.triggered.connect(self.save_as_pdf)

        # View Page Source
        view_source_action = QAction("View Page Source", self)
        view_source_action.triggered.connect(self.view_page_source)

        # Inspect Element (Simple Debugging)
        inspect_action = QAction("Inspect Element", self)
        inspect_action.triggered.connect(self.open_dev_tools)

        # Add actions to menu
        menu.addAction(back_action)
        menu.addAction(forward_action)
        menu.addAction(reload_action)
        menu.addAction(stop_action)
        menu.addSeparator()
        menu.addAction(present_action)
        menu.addSeparator()
        menu.addAction(copy_url_action)
        menu.addSeparator()
        menu.addAction(zoom_in_action)
        menu.addAction(zoom_out_action)
        menu.addAction(reset_zoom_action)
        menu.addSeparator()
        menu.addAction(save_pdf_action)
        menu.addAction(view_source_action)
        menu.addAction(inspect_action)

        global_pos = self.preview_browser.mapToGlobal(position)  # Correct mapping
        menu.exec(global_pos)

    def open_dev_tools(self):
        """Open Developer Tools (Inspect Element)."""
        if not hasattr(self, "dev_tools"):
            self.dev_tools = QWebEngineView()
            self.dev_tools.setWindowTitle("Developer Tools")
            self.dev_tools.resize(800, 600)
            self.dev_tools.setPage(QWebEnginePage(QWebEngineProfile.defaultProfile(), self.dev_tools))
            self.preview_browser.page().setDevToolsPage(self.dev_tools.page())

        self.dev_tools.show()

    def view_page_source(self):
        """Fetch and display the page source in a dialog."""
        self.preview_browser.page().toHtml(self.show_source_dialog)

    def show_source_dialog(self, html_content):
        """Create and display the 'View Page Source' dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Page Source")
        dialog.resize(800, 600)

        main_layout = QVBoxLayout(dialog)

        # Button layout (horizontal)
        button_layout = QHBoxLayout()

        # Create buttons
        self.copy_button = QPushButton("Copy Source")
        self.copy_button.clicked.connect(lambda: self.copy_to_clipboard(html_content))
        button_layout.addWidget(self.copy_button)

        self.save_button = QPushButton("Save to File")
        self.save_button.clicked.connect(lambda: self.save_source_to_file(html_content))
        button_layout.addWidget(self.save_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        button_layout.addWidget(close_button)

        # Create a read-only text edit to display the page source
        text_edit = QTextEdit()
        text_edit.setPlainText(html_content)

        # Apply stylesheet for text edit and scrollbar
        text_edit.setStyleSheet("""
            QTextEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border:1px solid #ccc;
                             background:white;
                             }
QTextEdit:focus {
                             border:2px solid royalblue;}
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
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #c6c6c6;
                height: 0px;
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
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: #c6c6c6;
                width: 0px;
            }
        """)

        # Apply stylesheet for buttons
        button_style = """
            QPushButton {
                border-radius:5px;
                padding:5px;
                border:1px solid #ccc;
                font-size:12px;
                background:white;
            }
            QPushButton:hover {
                color:royalblue;
                border:1px solid royalblue;
            }
        """
        self.copy_button.setStyleSheet(button_style)
        self.save_button.setStyleSheet(button_style)
        close_button.setStyleSheet(button_style)

        # Add widgets to layout
        main_layout.addWidget(text_edit)
        main_layout.addLayout(button_layout)

        dialog.exec()

    def copy_to_clipboard(self, text):
        """Copy page source to clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copied", "Page source copied to clipboard!")

    def save_source_to_file(self, text):
        """Save page source to a file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Page Source", "page_source.html", "HTML Files (*.html);;All Files (*)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
            QMessageBox.information(self, "Saved", f"Page source saved to:\n{file_path}")

    def show_find_replace_dialog(self):
        dialog = FindReplaceDialog(self)
        dialog.show()

    def open_template_dialog(self):
        dialog = TemplateDialog(self)
        dialog.show()

    def insert_table_dialog(self):
        dialog = InsertTableDialog(self)
        dialog.show()

    def change_text_case(self):
        """Apply selected case transformation to selected text."""
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return  # Do nothing if no text is selected

        selected_text = cursor.selectedText()

        # Apply transformation based on combobox selection
        choice = self.case_combobox.currentText()
        if choice == "UPPERCASE":
            transformed_text = selected_text.upper()
        elif choice == "lowercase":
            transformed_text = selected_text.lower()
        elif choice == "Swapcase":
            transformed_text = selected_text.swapcase()
        elif choice == "Title":
            transformed_text = selected_text.title()
        else:
            return

        # Replace selected text with transformed text
        cursor.insertText(transformed_text)
        self.case_combobox.setCurrentIndex(0) 

    def sync_scroll(self, value):
        text_scroll = self.text_edit.verticalScrollBar()
        text_height = self.text_edit.document().size().height()
        text_viewport_height = self.text_edit.viewport().height()
        text_scroll_ratio = value / (text_scroll.maximum() if text_scroll.maximum() > 0 else 1)

        self.preview_browser.page().runJavaScript(
            "document.body.scrollHeight",
            lambda web_height: self.scroll_webview(text_scroll_ratio, web_height, text_height, text_viewport_height)
        )

    def scroll_webview(self, ratio, web_height, text_height, text_viewport_height):
        web_visible_area = self.preview_browser.height()
        web_scrollable_height = web_height - web_visible_area
        adjusted_scroll_y = ratio * web_scrollable_height
        
        self.preview_browser.page().runJavaScript(f"window.scrollTo(0, {adjusted_scroll_y});")


    def show_context_menu(self, position):
        # Create the context menu
        context_menu = QMenu(self)

        # Cut/Copy/Paste actions
        context_menu.addAction(self.cut_action)
        context_menu.addAction(self.copy_action)
        context_menu.addAction(self.paste_action)
        context_menu.addSeparator()

        # Select All / Clear actions
        context_menu.addAction(self.selectall_action)
        context_menu.addAction(self.clear_action)
        context_menu.addSeparator()

        # Create Format menu
        format_menu = context_menu.addMenu("Format")

        # Add submenus under Format
        format_menu.addAction(self.bold_action)
        format_menu.addAction(self.italic_action)
        format_menu.addAction(self.bold_italic_action)
        format_menu.addAction(self.strikethrough_action)
        format_menu.addSeparator()
        format_menu.addAction(self.subscript_action)
        format_menu.addAction(self.superscript_action)
        format_menu.addAction(self.highlight_action)
        format_menu.addSeparator()
        format_menu.addAction(self.comment_action)
        format_menu.addAction(self.uncomment_action)
        format_menu.addSeparator()
        format_menu.addAction(self.clear_formatting_action)
        context_menu.addSeparator()

        # Create insert menu
        insert_menu = context_menu.addMenu("Insert")

        # Add submenus under insert
        self.link_action = QAction(QtGui.QIcon("ME_Icons/link.png"),"Link", self)
        self.link_action.triggered.connect(self.show_link_dialog)
        self.link_action.setToolTip("Add a link")
        insert_menu.addAction(self.link_action)
        self.image_action = QAction(QtGui.QIcon("ME_Icons/image.png"),"Image", self)
        self.image_action.triggered.connect(self.show_image_dialog)
        self.image_action.setToolTip("Add an image")
        insert_menu.addAction(self.image_action)
        insert_menu.addAction(self.table_action)
        insert_menu.addAction(self.add_equation_action)
        insert_menu.addSeparator()

        
        # Undo/Redo actions
        context_menu.addSeparator()
        context_menu.addAction(self.undo_action)
        context_menu.addAction(self.redo_action)

        # Apply styles
        context_menu.setStyleSheet("""
            QMenu {
                background-color: #f2f2f2;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 2px;
            }

            QMenu::item {
                background-color: transparent;
                color: black;
                padding: 4px;
                margin: 3px;
                width: 70px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background-color: #97B2ED;
                color: black;
            }

            QMenu::item:disabled {
            }

            QMenu::separator {
            }
        """)

        # Show the context menu at the clicked position
        context_menu.exec(self.mapToGlobal(position))


    def show_preview_dialog(self,styled_html):
        # Create the dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Preview Dialog")
        dialog.resize(800, 600)  # Set a default size for the dialog

        # Create the QWebEngineView widget
        self.preview_browser_2 = QWebEngineView()
        self.preview_browser_2.setHtml(styled_html)
        self.preview_browser_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.preview_browser_2.customContextMenuRequested.connect(self.contextMenuEvent_forPresent)
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(self.preview_browser_2)

        # Set the layout to the dialog
        dialog.setLayout(layout)
        
        # Show the dialog
        dialog.showMaximized()

    def present_markdown_preview(self):
        self.format_toolbar.hide()
        self.splitter.setSizes([0, 0, 1000])
        self.file_toolbar.hide()
        self.menuBar().hide()
        self.tab_widget_for_preview.setTabVisible(0, False)
        self.tab_widget_for_preview.setTabVisible(1, False)
        self.toggle_mode_button.hide()
        self.showFullScreen()
        self.status_bar.hide()
        self.file_label.hide()

    def on_tab_changed(self, index):
        # Show corner widget if Tab 2 is selected, otherwise hide it
        if index == 1:  # Index 1 corresponds to Tab 2
            self.copy_html_button.setVisible(True)
            self.save_button.setVisible(True)
            self.toggle_mode_button.setVisible(False)
        else:
            self.copy_html_button.setVisible(False)
            self.save_button.setVisible(False)
            self.toggle_mode_button.setVisible(True)

    def save_html_preview(self):
        # Open a file dialog to select the save location and filename
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save HTML File", "", "HTML Files (*.html);;All Files (*)", options=options)
        
        if file_name:  # If a file name is selected
            try:
                # Get the HTML content from the QTextEdit
                html_content = self.html_edit.toPlainText()
                
                # Open the file and write the HTML content
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(html_content)
                print("HTML file saved successfully.")  # Optional: Confirmation message
            except Exception as e:
                print(f"Error saving HTML file: {e}")

    def closeEvent(self, event):
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
            self.close()
            event.accept()

    def run_command_function(self):
        self.command_handler.Command_Line_Codes()

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

    def update_html_preview(self):
        """Convert Markdown content to HTML and update html_edit."""
        markdown_text = self.text_edit.toPlainText()
        html_content = markdown2.markdown(markdown_text)
        self.html_edit.setPlainText(html_content)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()  # Exit fullscreen
            self.fullscreen_action.setChecked(False)  # Update action state
        else:
            self.showFullScreen()  # Enter fullscreen
            self.fullscreen_action.setChecked(True)  # Update action state

    def insert_template(self, template_text):
        cursor = self.text_edit.textCursor()
        cursor.insertText(template_text + "\n")
    def update_status_info(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.split())
        line_count = text.count('\n') + 1  # Adding 1 for the last line
        column_count = len(text.split('\n')[-1])  # Columns in the last line
        space_count = text.count(' ')

        self.word_count_label.setText(f"Word count: {word_count}")
        self.space_count_label.setText(f"Spaces: {space_count}")

    def update_cursor_position(self):
        # Get the cursor object from the text edit
        cursor = self.text_edit.textCursor()
        
        # Get the current line number (block number)
        line_number = cursor.blockNumber() + 1  # Block number starts from 0, so add 1
        
        # Get the column number by calculating the position within the current line
        column_number = cursor.columnNumber()
    
        # Update the status bar labels with the current line and column
        self.line_count_label.setText(f"Line: {line_number}")
        self.column_count_label.setText(f"Column: {column_number}")

    def splitter_or_func(self):
        if self.splitter.orientation() == Qt.Horizontal:
            self.splitter.setOrientation(Qt.Vertical)
        else:
            self.splitter.setOrientation(Qt.Horizontal)
            self.splitter.setSizes([0, 500, 500])

    def clear_formatting(self):
        cursor = self.text_edit.textCursor()

        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            # Clear Markdown formatting from selected text
            cleared_text = self.remove_markdown_formatting(selected_text)
            cursor.insertText(cleared_text)

        else:
            # If no selection, apply to the entire text
            full_text = self.text_edit.toPlainText()
            cleared_text = self.remove_markdown_formatting(full_text)
            self.text_edit.setPlainText(cleared_text)

    def remove_markdown_formatting(self, text):
        """Removes Markdown formatting elements from the given text."""
        import re
        # Regex patterns to remove various Markdown elements
        patterns = [
            (r'\*\*([^\*]+)\*\*', r'\1'),     # Bold
            (r'\*\*\*([^\*]+)\*\*\*', r'\1'), # Bold Italic
            (r'\*([^\*]+)\*', r'\1'),         # Italic
            (r'\~\~(.*?)\~\~', r'\1'),        # Strikethrough
            (r'\=\=(.*?)\=\=', r'\1'),        # highlight
            (r'~(.*?)~', r'\1'),         # subscript
            (r'^(.*?)^', r'\1'),         # superscript
            (r'\`(.*?)\`', r'\1'),            # Inline code
            (r'\[(.*?)\]\((.*?)\)', r'\1'),   # Links
            (r'\!\[(.*?)\]\((.*?)\)', r'\1'), # Images
            (r'\#{1,6}\s*(.*)', r'\1'),       # Headers
            (r'^\*\s+', '', re.MULTILINE),    # Unordered list
            (r'^\d+\.\s+', '', re.MULTILINE), # Ordered list
            (r'\-\s\[.\]\s+', ''),            # Task list
        ]

        # Remove Markdown formatting
        for pattern in patterns:
            if len(pattern) == 2:  # No flags provided
                text = re.sub(pattern[0], pattern[1], text)
            elif len(pattern) == 3:  # Flags provided
                text = re.sub(pattern[0], pattern[1], text, flags=pattern[2])
        
        return text
    
    def insert_toc(self):
        """Inserts [TOC] at the cursor position in the text edit."""
        cursor = self.text_edit.textCursor()
        cursor.insertText("[TOC]\n")

    def insert_table_of_contents(self, markdown_text):
        """Inserts a table of contents (ToC) at the top of the Markdown content."""
        import re

        toc_lines = []
        toc_placeholder = "[TOC]"

        # Find all headers in the markdown text
        headers = re.findall(r'(#+)\s+(.*)', markdown_text)
        for level, header_text in headers:
            header_id = header_text.strip().lower().replace(' ', '-')
            indentation = '    ' * (len(level) - 1)  # Indent based on header level
            toc_lines.append(f'{indentation}- [{header_text}](#{header_id})')

        toc = '\n'.join(toc_lines)

        # Insert ToC in place of the [TOC] tag
        if toc_placeholder in markdown_text:
            markdown_text = markdown_text.replace(toc_placeholder, toc)

        return markdown_text

    def indent_text(self):
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()

        if cursor.hasSelection():
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()

            # Move cursor to the start of the selection and process each line
            cursor.setPosition(selection_start)
            while cursor.position() < selection_end:
                cursor.movePosition(cursor.StartOfLine)
                cursor.insertText("    ")  # Indent with 4 spaces
                cursor.movePosition(cursor.NextBlock)
                selection_end += 4  # Adjust selection end due to added indentation

        # If no selection, indent the current line
        else:
            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText("    ")

        cursor.endEditBlock()
    def dedent_text(self):
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()

        if cursor.hasSelection():
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()

            # Move cursor to the start of the selection and process each line
            cursor.setPosition(selection_start)
            while cursor.position() < selection_end:
                cursor.movePosition(cursor.StartOfLine)
                line = cursor.block().text()

                # Dedent only if the line starts with 4 spaces
                if line.startswith("    "):
                    for _ in range(4):
                        cursor.deleteChar()
                    selection_end -= 4  # Adjust selection end due to removed indentation

                cursor.movePosition(cursor.NextBlock)

        # If no selection, dedent the current line
        else:
            cursor.movePosition(cursor.StartOfLine)
            line = cursor.block().text()

            # Dedent only if the line starts with 4 spaces
            if line.startswith("    "):
                for _ in range(4):
                    cursor.deleteChar()

        cursor.endEditBlock()

    def jump_to_selection(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            self.text_edit.setTextCursor(cursor)
        else:
            QMessageBox.information(self, "Info", "No text selected")

    def jump_to_top(self):
        self.text_edit.moveCursor(QTextCursor.Start)

    def jump_to_bottom(self):
        self.text_edit.moveCursor(QTextCursor.End)

    def jump_to_line_start(self):
        self.text_edit.setFocus()  # Force focus back
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.StartOfBlock)
        self.text_edit.setTextCursor(cursor)

    def jump_to_line_end(self):
        self.text_edit.setFocus()  # Force focus back
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.EndOfBlock)
        self.text_edit.setTextCursor(cursor)

    def toggle_fullscreen_via_esc(self):
        if self.isFullScreen():
            self.showMaximized()  # Exit fullscreen
            self.fullscreen_action.setChecked(False)  # Update action state
        else:
            self.showFullScreen()  # Enter fullscreen
            self.fullscreen_action.setChecked(True)

    def enable_clean_view(self, state):
        if state:
            self.file_label.hide()
            self.status_bar.hide()
            self.activity_toolbar.hide()
        else:
            self.file_label.show()
            self.status_bar.show()
            self.activity_toolbar.show()
            
    def enable_editor_view(self, state):
        if state:
            self.splitter.setSizes([0, 1000, 0])
            self.splitter.setStyleSheet("""
QSplitter::handle:vertical {
    background-color: transparent;
    height: 2px;
}
QSplitter::handle:horizontal {
    background-color: transparent;
    height: 2px;
}
""")
        else:
            self.splitter.setSizes([0, 500, 500])
            self.splitter.setStyleSheet("""
QSplitter::handle:vertical {
    background-color: rgb(234, 234, 234);
    height: 2px;
}
QSplitter::handle:horizontal {
    background-color: rgb(234, 234, 234);
    height: 2px;
}
""")

    def enable_preview_view(self, state):
        if state:
            self.splitter.setSizes([0, 0, 1000])
            self.splitter.setStyleSheet("""
QSplitter::handle:vertical {
    background-color: transparent;
    height: 2px;
}
QSplitter::handle:horizontal {
    background-color: transparent;
    height: 2px;
}
""")
        else:
            self.splitter.setSizes([0, 500, 500])
            self.splitter.setStyleSheet("""
QSplitter::handle:vertical {
    background-color: rgb(234, 234, 234);
    height: 2px;
}
QSplitter::handle:horizontal {
    background-color: rgb(234, 234, 234);
    height: 2px;
}
""")

    def copy_file_path(self):
        if self.current_file:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_file)
            print("File path copied to clipboard.")

    # Function to save and close the current file
    def save_and_close(self):
            self.text_edit.clear()
            self.file_label.setText("•••")
            self.file_label.setStyleSheet("""
background:#f2f2f2;
                                      border-radius:9px;
                                      padding:1px;
font-size:14px;
""")
            self.current_file = None
            self.reset_tree_view()
            self.suggestion_index = 0

    def reset_tree_view(self):
        self.tree_view.collapseAll()
        root_path = QDir.rootPath()  # This sets to the root directory ("/" in Linux, "C:/" in Windows)
        root_index = self.file_system_model.index(root_path)
        self.tree_view.setRootIndex(root_index)
        home_path = QDir.homePath()
        home_index = self.file_system_model.index(home_path)
        self.tree_view.setRootIndex(home_index)
        self.tree_view.expand(self.file_system_model.index(QDir.homePath()))

    def show_badge_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Insert Badge")
        layout = QFormLayout(dialog)
        
        self.badge_lhs = QLineEdit()
        self.badge_rhs = QLineEdit()
        self.badge_color = QLineEdit()
        layout.addRow("Left Text:", self.badge_lhs)
        layout.addRow("Right Text:", self.badge_rhs)
        layout.addRow("Color:", self.badge_color)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_badge)
        button_box.button(QDialogButtonBox.Apply).clicked.connect(self.add_badge)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec()

    def add_badge(self):
        lhs_text = self.badge_lhs.text()
        rhs_text = self.badge_rhs.text()
        color = self.badge_color.text()
        badge_syntax = f":badge|{lhs_text}|{rhs_text}|{color}:"
        cursor = self.text_edit.textCursor()
        cursor.insertText(badge_syntax)
        self.update_preview()

    def insert_footnote(self):
        cursor = self.text_edit.textCursor()

        # Insert the footnote reference at the cursor position
        footnote_reference = "Add text here"
        cursor.insertText(footnote_reference)

        # Insert the superscript footnote marker
        cursor.insertText(" [^1]")
        
        # Move the cursor to the end of the document to insert the footnote definition
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(f"\n\n[^1]: Add footnote text here.")

        # Apply superscript formatting to [^1]
        cursor.setPosition(cursor.position() - len(f"[^1]"))
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(f"[^1]"))

        format = QTextCharFormat()
        format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
        cursor.setCharFormat(format)

        # Update the preview
        self.update_preview()
        
    def toggle_mode(self):
        if self.is_dark_mode:
            # Light Mode JavaScript
            self.preview_browser.page().runJavaScript("""
                document.documentElement.style.backgroundColor = 'white';
                document.documentElement.style.color = 'black';

                document.querySelectorAll('pre').forEach(function(pre) {
                    pre.style.backgroundColor = '#f5f5f5';
                    pre.style.color = 'black';
                });
                document.querySelectorAll('code').forEach(function(code) {
                    code.style.backgroundColor = '#f5f5f5';
                    code.style.color = 'black';
                });
                document.querySelectorAll('blockquote').forEach(function(blockquote) {
                    blockquote.style.backgroundColor = '#f9f9f9';
                    blockquote.style.color = 'black';
                    blockquote.style.borderLeft = '5px solid #ccc';
                });
                document.querySelectorAll('table').forEach(function(table) {
                    table.style.backgroundColor = 'white';
                    table.style.color = 'black';
                    table.querySelectorAll('th').forEach(function(th) {
                        th.style.backgroundColor = '#f2f2f2';
                    });
                    table.querySelectorAll('tr:nth-child(even)').forEach(function(tr) {
                        tr.style.backgroundColor = '#f2f2f2';
                    });
                });

                // Admonitions in Light Mode
                document.querySelectorAll('.admonition.note').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#e7f3fe'; // Light blue
                    admonition.style.color = 'black';
                    admonition.style.borderLeft = '5px solid #007bff'; // Blue border
                });
                document.querySelectorAll('.admonition.warning').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#fff3cd'; // Light yellow
                    admonition.style.color = 'black';
                    admonition.style.borderLeft = '5px solid #ffa726'; // Orange border
                });
                document.querySelectorAll('.admonition.danger').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#f8d7da'; // Light red
                    admonition.style.color = 'black';
                    admonition.style.borderLeft = '5px solid #dc3545'; // Red border
                });
                document.querySelectorAll('.admonition.success').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#d4edda'; // Light blue
                    admonition.style.color = 'black';
                    admonition.style.borderLeft = '5px solid #28a745'; // Blue border
                });
                document.querySelectorAll('.admonition.info').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#d1ecf1'; // Light yellow
                    admonition.style.color = 'black';
                    admonition.style.borderLeft = '5px solid #17a2b8'; // Orange border
                });
                document.querySelectorAll('.admonition.tip').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#e2e3e5'; // Light red
                    admonition.style.color = 'black';
                    admonition.style.borderLeft = '5px solid #007bff'; // Red border
                });
                document.querySelectorAll('.custom-button').forEach(function(button) {
                    button.style.backgroundColor = '#007bff'; // Light mode button color
                });
                document.querySelectorAll('.highlight').forEach(function(highlight) {
                    highlight.style.backgroundColor = '#f9ff0f'; // Light mode highlight color
                    highlight.style.color = 'black'; // Text color for light mode
                });
            """)
        else:
            # Dark Mode JavaScript
            self.preview_browser.page().runJavaScript("""
                document.documentElement.style.backgroundColor = '#2e2e2e';
                document.documentElement.style.color = 'white';

                document.querySelectorAll('pre').forEach(function(pre) {
                    pre.style.backgroundColor = 'black';
                    pre.style.color = 'white';
                });
                document.querySelectorAll('code').forEach(function(code) {
                    code.style.backgroundColor = 'black';
                    code.style.color = 'white';
                });
                document.querySelectorAll('blockquote').forEach(function(blockquote) {
                    blockquote.style.backgroundColor = '#444';
                    blockquote.style.color = 'white';
                    blockquote.style.borderLeft = '5px solid #666';
                });
                document.querySelectorAll('table').forEach(function(table) {
                    table.style.backgroundColor = '#333';
                    table.style.color = 'white';
                    table.querySelectorAll('th').forEach(function(th) {
                        th.style.backgroundColor = '#555';
                    });
                    table.querySelectorAll('tr:nth-child(even)').forEach(function(tr) {
                        tr.style.backgroundColor = '#444';
                    });
                });

                // Admonitions in Dark Mode
                document.querySelectorAll('.admonition.note').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#005f7f'; // Dark blue
                    admonition.style.color = 'white';
                    admonition.style.borderLeft = '5px solid #00aaff'; // Brighter blue border
                });
                document.querySelectorAll('.admonition.warning').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#806000'; // Darker yellow
                    admonition.style.color = 'white';
                    admonition.style.borderLeft = '5px solid #ffcc00'; // Yellow border
                });
                document.querySelectorAll('.admonition.danger').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#721c24'; // Dark red
                    admonition.style.color = 'white';
                    admonition.style.borderLeft = '5px solid #f50000'; // Bright red border
                });
                document.querySelectorAll('.admonition.success').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#2f5b3b'; // Light blue
                    admonition.style.color = 'white';
                    admonition.style.borderLeft = '5px solid #28a745'; // Blue border
                });
                document.querySelectorAll('.admonition.info').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#2b4e58'; // Light yellow
                    admonition.style.color = 'white';
                    admonition.style.borderLeft = '5px solid #17a2b8'; // Orange border
                });
                document.querySelectorAll('.admonition.tip').forEach(function(admonition) {
                    admonition.style.backgroundColor = '#4e545c'; // Light red
                    admonition.style.color = 'white';
                    admonition.style.borderLeft = '5px solid #007bff'; // Red border
                });
                document.querySelectorAll('.custom-button').forEach(function(button) {
                    button.style.backgroundColor = '#005f7f'; // Dark mode button color
                });
                document.querySelectorAll('.highlight').forEach(function(highlight) {
                    highlight.style.backgroundColor = '#b0b000'; // Dark mode highlight color
                    highlight.style.color = 'white'; // Text color for dark mode
                });
            """)

        # Toggle the mode flag
        self.is_dark_mode = not self.is_dark_mode
    
    def update_preview(self):
        try:
            markdown_text = self.text_edit.toPlainText()

            def convert_mermaid_blocks(markdown_text):
                # Convert ```mermaid blocks to <div class="mermaid">...</div>
                return re.sub(
                    r'```mermaid\s+([\s\S]*?)```',
                    r'<div class="mermaid">\1</div>',
                    markdown_text
                )
            
            processed_text = self.generate_toc(markdown_text)
            processed_text = self.custom_admonition_parser(processed_text)
            processed_text = self.custom_inline_alert_parser(processed_text)
            processed_text = self.custom_task_list_parser(processed_text)
            processed_text = self.custom_definition_list_parser(processed_text)
            processed_text = self.highlight_text_with_equal(processed_text)
            processed_text = convert_mermaid_blocks(processed_text)
            processed_text = self.convert_sub(processed_text)
            processed_text = self.convert_super(processed_text)

            # Parse the markdown text with checkbox and admonition block support
            self.html = markdown2.markdown(
                processed_text,
                extras=["fenced-code-blocks","tables","strike",
                        "cuddled-lists","metadata","footnotes",
                        "task_list","abbr","def_list",
                        "smarty","toc","pypages"  
                ]
            )

            self.pygments_css = HtmlFormatter().get_style_defs('.codehilite')

            # CSS for rendering the admonition blocks and other elements
            self.styled_html = f"""
            <html>
            <head>
            <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script>
            MathJax = {{
                tex: {{
                    inlineMath: [['$', '$'], ['\\(', '\\)']]
                }},
                svg: {{ fontCache: 'global' }}
            }};
        </script>
        <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
            <style>
            body {{
                line-height: 1.6;
                margin: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            table, th, td {{
                border: 1px solid #ddd;
                border-radius:5px;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            img {{
                display: inline-block;
                max-width: 100%;
                height: auto;
            }}
            blockquote {{
                margin: 20px 0;
                padding: 10px 20px;
                background-color: #f9f9f9;
                border-left: 5px solid #ccc;
                border-radius: 3px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin: 20px 0 10px;
                padding-bottom: 10px;
                border-bottom: 1px solid #ddd;
            }}
            .btn {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-align: center;
                border-radius: 4px;
                text-decoration: none;
            }}
            pre {{
    background-color: #E9E9E9;
    padding: 10px;
    overflow-x: auto;
    border-radius: 5px;
    border: 1px solid #b5b5b5;
    /* Removed font-weight to not affect inner text */
}}
pre code {{
    font-weight: normal; /* Neutralize if needed */
    border: none; /* No extra border here */
}}
code {{
    background-color: #E9E9E9; /* Match pre background if needed */
    padding: 2px 4px;
    border-radius: 5px;
    border: 1px solid #b5b5b5;
    font-weight: normal; /* Prevent bold text */
}}
            mark {{
                background-color: #f9ff0f;
                border-radius: 7px;
                padding: 4px;
                color: black;
            }}
            input[type="checkbox"] {{
                transform: scale(1.2);
                margin-right: 10px;
            }}
            li.task-list-item {{
                list-style-type: none;
                display: flex;
                align-items: center;
            }}
            /* Inline Alert Styles */
            .inline-alert {{
                padding: 0.5em;
                border-radius: 5px;
            }}
            /* Admonition styles */
            .admonition {{
                border-left: 5px solid #ccc;
                padding: 10px;
                margin: 20px 0;
                border-radius: 3px;
            }}
            .admonition.note {{
                background-color: #e7f3fe;
                border-color: #007bff;
            }}
            .admonition.warning {{
                background-color: #fff3cd;
                border-color: #ffa726;
            }}
            .admonition.danger {{
                background-color: #f8d7da;
                border-color: #dc3545;
            }}
            .admonition.success {{
                background-color: #d4edda;
                border-color: #28a745;
            }}
            .admonition.info {{
                background-color: #d1ecf1;
                border-color: #17a2b8;
            }}
            .admonition.tip {{
                background-color: #e2e3e5;
                border-color: #007bff;
            }}
            progress {{
            width: 100%;
        }}
            /* Badge Styles */
            .custom-badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 12px;
                background-color: #007bff;
                color: white;
                margin: 0 5px;
            }}

            /* Highlight Block Styles */
            .highlight {{
                background-color: #f9ff0f;
                border-radius: 7px;
                padding: 4px;
                color: black;
            }}

            /* Callout Styles */
            .custom-callout {{
                padding: 10px;
                border-left: 5px solid #007bff;
                background-color: #e3f2fd;
                margin: 10px 0;
            }}

            /* Button Styles */
            .custom-button {{
                display: inline-block;
                padding: 10px 15px;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
            }}
            /* Custom Progress Bar Styles */
.custom-progress-bar {{
    background-color: #f3f3f3;
    border-radius: 8px;
    overflow: hidden;
}}
            </style>
            <style>
            {self.pygments_css}
            </style>
            <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script type="text/javascript">
document.addEventListener('DOMContentLoaded', function() {{
    if (window.mermaid) {{
        mermaid.initialize({{ startOnLoad: true }});
        mermaid.init(undefined, document.querySelectorAll('.mermaid'));
    }} else {{
        console.error("Mermaid.js failed to load.");
    }}
}});
<script type="text/javascript" async
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>

    <!-- MathJax Configuration -->
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({{
            tex2jax: {{
                inlineMath: [['$','$'], ['\\(','\\)']],
                displayMath: [['$$','$$'], ['\\[','\\]']],
                processEscapes: true
            }},
            "HTML-CSS": {{
                linebreaks: {{ automatic: true }},
                scale: 90
            }},
            SVG: {{
                font: "TeX"
            }},
            MathML: {{
                extensions: ["mml3.js"]
            }},
            showMathMenu: false,  // Optional: Hide MathJax context menu
            menuSettings: {{
                zoom: "Click"  // Enable zoom on click for formulas
            }}
        }});
    </script>
    <script type="text/javascript">
        // Ensure MathJax processes the page after content is loaded
        window.onload = function() {{
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        }};
        </script>
            </head>
            <body>{self.html}</body>
            </html>
            """

            self.preview_browser.setHtml(self.styled_html)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while updating the preview: {e}")
   
    def update_preview_2(self):
        try:
            markdown_text = self.text_edit.toPlainText()

            processed_text = self.generate_toc(markdown_text)
            processed_text = self.custom_admonition_parser(processed_text)
            processed_text = self.custom_inline_alert_parser(processed_text)
            processed_text = self.custom_task_list_parser(processed_text)
            processed_text = self.custom_definition_list_parser(processed_text)
            processed_text = self.highlight_text_with_equal(processed_text)
            

            def mermaid_replacer(match):
                mermaid_code = match.group(1).strip()
                return f'<div class="mermaid">\n{mermaid_code}\n</div>'

            processed_text = re.sub(r"```mermaid\s*([\s\S]*?)```", mermaid_replacer, processed_text)

            # Parse the markdown text with checkbox and admonition block support
            html = markdown2.markdown(
                processed_text,
                extras=["fenced-code-blocks","tables","strike",
                        "cuddled-lists","metadata","footnotes",
                        "task_list","abbr","def_list",
                        "smarty","toc","pypages"  
                ]
            )

            pygments_css = HtmlFormatter().get_style_defs('.codehilite')

            # CSS for rendering the admonition blocks and other elements
            styled_html = f"""
            <html>
            <head>
            <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
       
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
            <style>
            body {{
                line-height: 1.6;
                margin: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            table, th, td {{
                border: 1px solid #ddd;
                border-radius:5px;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            img {{
                display: inline-block;
                max-width: 100%;
                height: auto;
            }}
            blockquote {{
                margin: 20px 0;
                padding: 10px 20px;
                background-color: #f9f9f9;
                border-left: 5px solid #ccc;
                border-radius: 3px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin: 20px 0 10px;
                padding-bottom: 10px;
                border-bottom: 1px solid #ddd;
            }}
            .btn {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-align: center;
                border-radius: 4px;
                text-decoration: none;
            }}
            pre {{
                background-color: #E9E9E9;
                padding: 10px;
                overflow-x: auto;
                border-radius: 5px;
                font-wight: bold;
            }}
            pre code {{
                font-weight: bold; /* Make text bold */
            }}
            code {{
                background-color: #E9E9E9;
                padding: 2px 4px;
                border-radius: 3px;
            }}
            mark {{
                background-color: #f9ff0f;
                border-radius: 7px;
                padding: 4px;
                color: black;
            }}
            input[type="checkbox"] {{
                transform: scale(1.2);
                margin-right: 10px;
            }}
            li.task-list-item {{
                list-style-type: none;
                display: flex;
                align-items: center;
            }}
            /* Inline Alert Styles */
            .inline-alert {{
                padding: 0.5em;
                border-radius: 5px;
            }}
            /* Admonition styles */
            .admonition {{
                border-left: 5px solid #ccc;
                padding: 10px;
                margin: 20px 0;
                border-radius: 3px;
            }}
            .admonition.note {{
                background-color: #e7f3fe;
                border-color: #007bff;
            }}
            .admonition.warning {{
                background-color: #fff3cd;
                border-color: #ffa726;
            }}
            .admonition.danger {{
                background-color: #f8d7da;
                border-color: #dc3545;
            }}
            .admonition.success {{
                background-color: #d4edda;
                border-color: #28a745;
            }}
            .admonition.info {{
                background-color: #d1ecf1;
                border-color: #17a2b8;
            }}
            .admonition.tip {{
                background-color: #e2e3e5;
                border-color: #007bff;
            }}
            progress {{
            width: 100%;
        }}
            /* Badge Styles */
            .custom-badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 12px;
                background-color: #007bff;
                color: white;
                margin: 0 5px;
            }}

            /* Highlight Block Styles */
            .highlight {{
                background-color: #f9ff0f;
                border-radius: 7px;
                padding: 4px;
                color: black;
            }}

            /* Callout Styles */
            .custom-callout {{
                padding: 10px;
                border-left: 5px solid #007bff;
                background-color: #e3f2fd;
                margin: 10px 0;
            }}

            /* Button Styles */
            .custom-button {{
                display: inline-block;
                padding: 10px 15px;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
            }}
            /* Custom Progress Bar Styles */
.custom-progress-bar {{
    background-color: #f3f3f3;
    border-radius: 8px;
    overflow: hidden;
}}
            </style>
            <style>
            {pygments_css}
            </style>
            <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script type="text/javascript">
document.addEventListener('DOMContentLoaded', function() {{
    if (window.mermaid) {{
        mermaid.initialize({{ startOnLoad: true }});
        mermaid.init(undefined, document.querySelectorAll('.mermaid'));
    }} else {{
        console.error("Mermaid.js failed to load.");
    }}
}});
</script>
<!-- MathJax Configuration -->
<script type="text/javascript">
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    packages: {{ '[+]': ['noerrors'] }}
  }},
  options: {{
    ignoreHtmlClass: 'tex2jax_ignore',
    processHtmlClass: 'tex2jax_process'
  }}
}};
</script>
<script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>
            </head>
            <body>{html}</body>
            </html>
            """
            dialog = QDialog()
            dialog.setWindowTitle("Present")
            dialog.resize(800, 600)
            dialog.setStyleSheet("""
            QDialog{
                    background:white;}
        
                    """)

            preview_browser_2 = QWebEngineView()
            preview_browser_2.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
            preview_browser_2.setHtml(styled_html)

            layout = QVBoxLayout(dialog)
            layout.addWidget(preview_browser_2)
            dialog.setLayout(layout)

            dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            dialog.showFullScreen()

            # Dark mode toggle flag
            is_dark_mode = [False]

            def toggle_mode_2():
                if is_dark_mode[0]:
                    # Light Mode JavaScript
                    dialog.setStyleSheet("""
                    background:white;
                    """)
                    preview_browser_2.page().runJavaScript("""
                        document.documentElement.style.backgroundColor = 'white';
                        document.documentElement.style.color = 'black';

                        document.querySelectorAll('pre').forEach(function(pre) {
                            pre.style.backgroundColor = '#f5f5f5';
                            pre.style.color = 'black';
                        });
                        document.querySelectorAll('code').forEach(function(code) {
                            code.style.backgroundColor = '#f5f5f5';
                            code.style.color = 'black';
                        });
                        document.querySelectorAll('blockquote').forEach(function(blockquote) {
                            blockquote.style.backgroundColor = '#f9f9f9';
                            blockquote.style.color = 'black';
                            blockquote.style.borderLeft = '5px solid #ccc';
                        });
                        document.querySelectorAll('table').forEach(function(table) {
                            table.style.backgroundColor = 'white';
                            table.style.color = 'black';
                            table.querySelectorAll('th').forEach(function(th) {
                                th.style.backgroundColor = '#f2f2f2';
                            });
                            table.querySelectorAll('tr:nth-child(even)').forEach(function(tr) {
                                tr.style.backgroundColor = '#f2f2f2';
                            });
                        });

                        // Admonitions in Light Mode
                        document.querySelectorAll('.admonition.note').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#e7f3fe'; // Light blue
                            admonition.style.color = 'black';
                            admonition.style.borderLeft = '5px solid #007bff'; // Blue border
                        });
                        document.querySelectorAll('.admonition.warning').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#fff3cd'; // Light yellow
                            admonition.style.color = 'black';
                            admonition.style.borderLeft = '5px solid #ffa726'; // Orange border
                        });
                        document.querySelectorAll('.admonition.danger').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#f8d7da'; // Light red
                            admonition.style.color = 'black';
                            admonition.style.borderLeft = '5px solid #dc3545'; // Red border
                        });
                        document.querySelectorAll('.admonition.success').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#d4edda'; // Light blue
                            admonition.style.color = 'black';
                            admonition.style.borderLeft = '5px solid #28a745'; // Blue border
                        });
                        document.querySelectorAll('.admonition.info').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#d1ecf1'; // Light yellow
                            admonition.style.color = 'black';
                            admonition.style.borderLeft = '5px solid #17a2b8'; // Orange border
                        });
                        document.querySelectorAll('.admonition.tip').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#e2e3e5'; // Light red
                            admonition.style.color = 'black';
                            admonition.style.borderLeft = '5px solid #007bff'; // Red border
                        });
                        document.querySelectorAll('.custom-button').forEach(function(button) {
                            button.style.backgroundColor = '#007bff'; // Light mode button color
                        });
                        document.querySelectorAll('.highlight').forEach(function(highlight) {
                            highlight.style.backgroundColor = '#f9ff0f'; // Light mode highlight color
                            highlight.style.color = 'black'; // Text color for light mode
                        });
                    """)
                else:
                    dialog.setStyleSheet("""
                    background:#2e2e2e;
                    """)
                    # Dark Mode JavaScript
                    preview_browser_2.page().runJavaScript("""
                        document.documentElement.style.backgroundColor = '#2e2e2e';
                        document.documentElement.style.color = 'white';

                        document.querySelectorAll('pre').forEach(function(pre) {
                            pre.style.backgroundColor = 'black';
                            pre.style.color = 'white';
                        });
                        document.querySelectorAll('code').forEach(function(code) {
                            code.style.backgroundColor = 'black';
                            code.style.color = 'white';
                        });
                        document.querySelectorAll('blockquote').forEach(function(blockquote) {
                            blockquote.style.backgroundColor = '#444';
                            blockquote.style.color = 'white';
                            blockquote.style.borderLeft = '5px solid #666';
                        });
                        document.querySelectorAll('table').forEach(function(table) {
                            table.style.backgroundColor = '#333';
                            table.style.color = 'white';
                            table.querySelectorAll('th').forEach(function(th) {
                                th.style.backgroundColor = '#555';
                            });
                            table.querySelectorAll('tr:nth-child(even)').forEach(function(tr) {
                                tr.style.backgroundColor = '#444';
                            });
                        });

                        // Admonitions in Dark Mode
                        document.querySelectorAll('.admonition.note').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#005f7f'; // Dark blue
                            admonition.style.color = 'white';
                            admonition.style.borderLeft = '5px solid #00aaff'; // Brighter blue border
                        });
                        document.querySelectorAll('.admonition.warning').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#806000'; // Darker yellow
                            admonition.style.color = 'white';
                            admonition.style.borderLeft = '5px solid #ffcc00'; // Yellow border
                        });
                        document.querySelectorAll('.admonition.danger').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#721c24'; // Dark red
                            admonition.style.color = 'white';
                            admonition.style.borderLeft = '5px solid #f50000'; // Bright red border
                        });
                        document.querySelectorAll('.admonition.success').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#2f5b3b'; // Light blue
                            admonition.style.color = 'white';
                            admonition.style.borderLeft = '5px solid #28a745'; // Blue border
                        });
                        document.querySelectorAll('.admonition.info').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#2b4e58'; // Light yellow
                            admonition.style.color = 'white';
                            admonition.style.borderLeft = '5px solid #17a2b8'; // Orange border
                        });
                        document.querySelectorAll('.admonition.tip').forEach(function(admonition) {
                            admonition.style.backgroundColor = '#4e545c'; // Light red
                            admonition.style.color = 'white';
                            admonition.style.borderLeft = '5px solid #007bff'; // Red border
                        });
                        document.querySelectorAll('.custom-button').forEach(function(button) {
                            button.style.backgroundColor = '#005f7f'; // Dark mode button color
                        });
                        document.querySelectorAll('.highlight').forEach(function(highlight) {
                            highlight.style.backgroundColor = '#b0b000'; // Dark mode highlight color
                            highlight.style.color = 'white'; // Text color for dark mode
                        });
                    """)

                is_dark_mode[0] = not is_dark_mode[0]

            # Shortcut for toggling mode with Ctrl+M
            shortcut_toggle = QShortcut(QKeySequence("Ctrl+M"), dialog)
            shortcut_toggle.activated.connect(toggle_mode_2)

            esc_toggle = QShortcut(QKeySequence("Esc"), dialog)
            esc_toggle.activated.connect(lambda: dialog.close())

            # Show dialog
            dialog.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while updating the preview: {e}")

    def custom_admonition_parser(self, text):
        admonition_pattern = r':::(\w+)\s+(.*?)\n:::\s*'
        return re.sub(admonition_pattern, r'<div class="admonition \1">\2</div>', text, flags=re.DOTALL)

    def insert_admonition_from_combobox(self):
        # Get the selected index

        selected_index = self.admonition_combobox.currentIndex()
        
        # Define Markdown format based on the selected index
        if selected_index == 0:
            return  # Do nothing if the default option is selected
        elif selected_index == 1:
            self.insert_blockquote()
            return
        elif selected_index == 2:
            self.make_inline_code()
            return
        elif selected_index == 3:
            self.insert_code_block()
            return
        else:
            selected_admonition = self.admonition_combobox.currentText().replace(" block" or " Block", "").lower()

            if selected_admonition=="note":
                markdown_format = f"\n:::{selected_admonition}\n<span style='color: #007bff; font-weight: bold;'>{selected_admonition.capitalize()}:</span>\nYour message here\n:::<br>\n"
            elif selected_admonition=="warning":
                markdown_format = f"\n:::{selected_admonition}\n<span style='color: #ffa726; font-weight: bold;'>{selected_admonition.capitalize()}:</span>\nYour message here\n:::<br>\n"
            elif selected_admonition=="danger":
                markdown_format = f"\n:::{selected_admonition}\n<span style='color: #dc3545; font-weight: bold;'>{selected_admonition.capitalize()}:</span>\nYour message here\n:::<br>\n"
            elif selected_admonition=="success":
                markdown_format = f"\n:::{selected_admonition}\n<span style='color: #28a745; font-weight: bold;'>{selected_admonition.capitalize()}:</span>\nYour message here\n:::<br>\n"
            elif selected_admonition=="info":
                markdown_format = f"\n:::{selected_admonition}\n<span style='color: #17a2b8; font-weight: bold;'>{selected_admonition.capitalize()}:</span>\nYour message here\n:::<br>\n"
            elif selected_admonition=="tip":
                markdown_format = f"\n:::{selected_admonition}\n<span style='color: #007bff; font-weight: bold;'>{selected_admonition.capitalize()}:</span>\nYour message here\n:::<br>\n"
            else:
                markdown_format = ""

            cursor = self.text_edit.textCursor()
            cursor.insertText(markdown_format)
            self.text_edit.setTextCursor(cursor)

        self.admonition_combobox.setCurrentIndex(0)

    def custom_badge_dialog(self):
        dialog = BadgeDialog(self)
        dialog.show()

    def custom_inline_alert_parser(self, text):
        inline_alert_pattern = r'> (.*?)\n'
        return re.sub(inline_alert_pattern, r'<div class="alert">\1</div>', text)

    def custom_task_list_parser(self, text):
        # Ensure task list items are wrapped inside <ul> or <ol>
        text = re.sub(r"(^|\n)- \[ \] (.+)", r'\1<li class="task-list-item"><input type="checkbox"> \2</li>', text)
        text = re.sub(r"(^|\n)- \[x\] (.+)", r'\1<li class="task-list-item"><input type="checkbox" checked> \2</li>', text)

        # Wrap list items inside <ul> to maintain structure
        text = re.sub(r"(<li class=\"task-list-item\">.*?</li>)", r'<ul class="task-list">\1</ul>', text)

        return text
    
    def custom_definition_list_parser(self, text):
        definition_list_pattern = r'(^.+)\n(: .+(\n: .+)*)'
        def replace_match(match):
            term = match.group(1).strip()
            definitions = match.group(2).split("\n")
            formatted_definitions = "".join(f"<dd>{d[2:].strip()}</dd>" for d in definitions)  # Removing '- ' prefix
            return f"<dl><dt>{term}</dt>{formatted_definitions}</dl>"
        
        return re.sub(definition_list_pattern, replace_match, text, flags=re.MULTILINE)

    def generate_toc(self, markdown_text):
        # Regular expression to find headings
        headings = re.findall(r'^(#{1,6})\s+(.*)', markdown_text, re.MULTILINE)

        # If no headings, return the original text
        if not headings:
            return markdown_text

        toc_lines = []
        toc_lines.append("<ul>")

        # Generate ToC based on the headings
        for level, title in headings:
            indent_level = len(level) - 1
            toc_lines.append(f'{"    " * indent_level}<li><a href="#{title}">{title}</a></li>')

        toc_lines.append("</ul>")

        toc = "\n".join(toc_lines)

        # Replace the [TOC] placeholder with the generated ToC
        return markdown_text.replace('[TOC]', toc)


    def save_as_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'
            self.preview_browser.page().printToPdf(file_path)

    def toggle_tree_view(self):
        if self.tree_view.isVisible():
            self.tree_view.hide()  # Collapse TreeView
            self.splitter.setSizes([0, 500, 500])
        else:
            self.tree_view.show()
            self.splitter.setSizes([200, 500, 500])

    def toggle_command_line(self):
        if self.command_line.isVisible():
            self.command_line.hide()
            self.run_command.hide()
        else:
            self.command_line.show()
            self.command_line.setFocus()
            self.run_command.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg','.md', '.commonmark', '.markdown', '.textile', '.mmd', '.Rmd', '.gfm', '.txt', '.rtf', '.docx', '.xml', '.odt')):
                event.acceptProposedAction()  # Accept only if it's an `.md` file
            else:
                event.ignore()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            file_path = urls[0].toLocalFile()

            # Check if the dropped file is a Markdown-related file
            if file_path.endswith(('.md', '.commonmark', '.markdown', '.textile', '.mmd', '.Rmd', '.gfm', '.txt', '.rtf', '.docx', '.xml', '.odt')):
                self.open_file_using_Drag_drop(file_path)  # Call the file opening function with the file path
                event.acceptProposedAction()
            elif urls[0].scheme() in ['http', 'https']:
                image_url = urls[0].toString()
                image_name = os.path.basename(image_url)  # You can modify how you want the image name
                markdown_image = f"![{image_name}]({image_url})"
                self.text_edit.insertPlainText(markdown_image)  # Insert Markdown for web image
                event.acceptProposedAction()
            else:
                # Check if the dropped file is an image
                file_extension = os.path.splitext(file_path)[1].lower()
                if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']:
                    image_name = os.path.basename(file_path)
                    # Convert the file path to a file:// URL
                    file_url = QUrl.fromLocalFile(file_path).toString()
                    markdown_image = f"[{image_name}]({file_url})"
                    self.text_edit.insertPlainText(markdown_image)
                    event.acceptProposedAction()
                else:
                    event.ignore()
        else:
            event.ignore()

    def open_file_using_Drag_drop(self, file_path=None):
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", 
"Markdown Files (*.md);;"
"CommonMark Files (*.commonmark);;"
"Markdown Extra Files (*.markdown);;"
"GitHub Flavored Markdown Files (*.gfm);;"
"Word Files (*.docx);;"
"LaTeX Files (*.tex);;"
"OpenDocument Text (*.odt);;"
"Rich Text Format (*.rtf);;"
"Plain Text (*.txt);;"
"All Files (*)")
        try:
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                file_base_name = os.path.basename(file_path)
                self.text_edit.setPlainText(file_content)
                self.current_file = file_path
                self.file_label.setText(f"<b>{file_base_name}</b> - {file_path}")
                self.file_label.setStyleSheet("""
background:#f2f2f2;
                                      border-radius:9px;
                                              border:1px solid #92d051;
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

    def open_file_from_tree(self, index):
        file_path = self.file_system_model.filePath(index)
        try:
            if file_path:
                file_base_name = os.path.basename(file_path)
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    # For image files, insert Markdown at the cursor position
                    image_markdown = f"![{file_base_name}]({file_path})"
                    cursor = self.text_edit.textCursor()
                    cursor.insertText(image_markdown)
                    self.text_edit.setTextCursor(cursor)
                else:
                    # For other file types, open and read the file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        self.text_edit.setPlainText(file_content)
                    
                self.current_file = file_path
                self.file_label.setText(f"<b>{file_base_name}</b> - {file_path}")
                self.file_label.setStyleSheet("""
background:#f2f2f2;
                                      border-radius:9px;
                                              border:1px solid #92d051;
                                      padding:1px;
font-size:14px;
""")
                self.update_preview()
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


    def convert_size(self, size_bytes):
        """
        Converts the given file size in bytes to GB:MB:Bits format
        """
        size_in_bits = size_bytes * 8  # Convert bytes to bits
        size_gb = size_in_bits // (8 * 1024 * 1024 * 1024)  # Calculate GB
        size_in_bits -= size_gb * (8 * 1024 * 1024 * 1024)

        size_mb = size_in_bits // (8 * 1024 * 1024)  # Calculate MB
        size_in_bits -= size_mb * (8 * 1024 * 1024)

        return size_gb, size_mb, size_in_bits  # Remaining bits

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
                self.update_file_status("Saved")
        else:
            self.save_file_as()

    def save_file_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", 
"Markdown Files (*.md);;"
"CommonMark Files (*.commonmark);;"
"Markdown Extra Files (*.markdown);;"
"Textile Files (*.textile);;"
"MultiMarkdown Files (*.mmd);;"
"GitHub Flavored Markdown Files (*.gfm);;"
"PDF Files (*.pdf);;"
"HTML Files (*.html);;"
"Word Files (*.docx);;"
"LaTeX Files (*.tex);;"
"EPUB Files (*.epub);;"
"OpenDocument Text (*.odt);;"
"Rich Text Format (*.rtf);;"
"XML Files (*.xml);;"
"Plain Text (*.txt);;"
"Beamer Files (*.tex);;"
"All Files (*)", options=options)
        self.update_file_status("Saved")
        if file_name:
            self.current_file = file_name
            self.save_file()

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

    def make_bold(self):
        self.format_text('**', '**')

    def make_italic(self):
        self.format_text('*', '*')

    def make_bold_italic(self):
        self.format_text('***', '***')

    def make_strikethrough(self):
        self.format_text('~~', '~~')

    def make_inline_code(self):
        self.format_text('`', '`')
        self.admonition_combobox.setCurrentIndex(0)

    def convert_super(self,text):
        # Superscript: ^text^
        text = re.sub(r'\^([^^]+?)\^', r'<sup>\1</sup>', text)
        return text
    
    def convert_sub(self,text):
        # Subscript: ~text~
        text = re.sub(r'(?<!~)~([^~]+?)~(?!~)', r'<sub>\1</sub>', text)
        return text
    
    def highlight_text_with_equal(self, text):
        return re.sub(r'(?<!~)(?<!^)==([^=]+)==(?<!~)(?<!^)', r'<mark>\1</mark>', text)

    def format_text(self, start_delim, end_delim):
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()
        cursor.insertText(start_delim + cursor.selectedText() + end_delim)
        cursor.endEditBlock()
        self.update_preview()

    def apply_header(self, index):
        headers = ['# ', '## ', '### ', '#### ', '##### ', '###### ']
        if index != 0:
            self.apply_list(None)
            self.format_text(headers[index - 1], '')
            self.update_preview()
        else:
            self.apply_list(None)
            self.format_text('', '')
            self.update_preview()
        self.header_combo.setCurrentIndex(0) 

    def apply_checklist(self, index):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        checklist = ['- [ ] ', '- [x] ']

        if index == 0:  # If reset option is selected, remove checklist formatting
            self.format_text('', '')
            self.checklist_combo.setCurrentIndex(0)
            return

        prefix = checklist[index - 1]  # Get the correct checklist prefix

        if selected_text:
            # Split selected text correctly using `\u2029`
            lines = selected_text.split('\u2029')
            lines = [line for line in lines if line.strip()]  # Remove empty lines

            formatted_lines = [f"{prefix}{line}" for line in lines]

            if formatted_lines:
                cursor.beginEditBlock()  # Start grouping undo actions
                cursor.removeSelectedText()
                cursor.insertText('\n'.join(formatted_lines))
                cursor.endEditBlock()  # End grouping undo actions
        else:
            # No selection, just insert at cursor position
            cursor.insertText(prefix)

        self.update_preview()
        self.checklist_combo.setCurrentIndex(0)


    def apply_list(self, index):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        if index == 0:  # Reset option
            self.format_text('', '')
            self.list_combo.setCurrentIndex(0)
            return

        if selected_text:
            # Split selected text correctly using `\u2029`
            lines = selected_text.split('\u2029')
            lines = [line for line in lines if line.strip()]  # Remove empty lines

            formatted_lines = []
            if index == 1:  # Ordered List
                formatted_lines = [f"{i + 1}. {line}" for i, line in enumerate(lines)]
            elif index == 2:  # Unordered List
                formatted_lines = [f"- {line}" for line in lines]
            elif index == 3:  # Definition List
                if len(lines) > 1:
                    formatted_lines = [lines[0]] + [f": {line}" for line in lines[1:]]
                else:
                    formatted_lines = [f": {lines[0]}"] if lines else []

            if formatted_lines:
                cursor.beginEditBlock()  # Start grouping undo actions
                cursor.removeSelectedText()
                cursor.insertText('\n'.join(formatted_lines))
                cursor.endEditBlock()  # End grouping undo actions
        else:
            # No selection, just insert list marker at the cursor position
            if index == 1:
                cursor.insertText("1. ")
            elif index == 2:
                cursor.insertText("- ")
            elif index == 3:
                cursor.insertText(": ")

        self.update_preview()
        self.list_combo.setCurrentIndex(0)


    def eq_win(self):
        self.eqwin = QDialog(self)
        self.eqwin.setWindowTitle("Equations")
        self.eqwin.setWindowIcon(QtGui.QIcon("ME_Icons/equation.png"))
        self.eqwin.setGeometry(100, 100, 680, 290)
        self.eqwin.setStyleSheet("""background:#f2f2f2;""")

        tsymcursor = self.text_edit.textCursor()

        trigo_fn = {
        "Sin": "$\\sin()$","Cos": "$\\cos()$","Tan": "$\\tan()$",
        "Cosec": "$\\csc()$","Sec": "$\\sec()$","Cot": "$\\cot()$",
        "Sinh": "$\\sinh()$","Cosh": "$\\cosh()$","Tanh": "$\\tanh()$",
        "Cosech": "$\\csch()$","Sech": "$\\sech()$","Coth": "$\\coth()$",
        "Sin⁻¹": "$\\sin^{-1}()$","Cos⁻¹": "$\\cos^{-1}()$","Tan⁻¹": "$\\tan^{-1}()$",
        "Cosec⁻¹": "$\\csc^{-1}()$","Sec⁻¹": "$\\sec^{-1}()$","Cot⁻¹": "$\\cot^{-1}()$",
        "Sinh⁻¹": "$\\sinh^{-1}()$","Cosh⁻¹": "$\\cosh^{-1}()$","Tanh⁻¹": "$\\tanh^{-1}()$",
        "Cosech⁻¹": "$\\csch^{-1}()$","Sech⁻¹": "$\\sech^{-1}()$","Coth⁻¹": "$\\coth^{-1}()$"
        }

        log_fn = {
            "Log": "$\\log()$","Ln": "$\\ln()$","Log⁻¹": "$\\log^{-1}()$",
    "Exp": "$\\exp()$","E": "$e$","10^x": "$10^x$",
    "2^x": "$2^x$","Log₁₀": "$\\log_{10}()$","Log₂": "$\\log_{2}()$",
    "Logₑ": "$\\log_{e}()$","Exp⁻¹": "$\\exp^{-1}()$","10^(-x)": "$10^{-x}$",
    "2^(-x)": "$2^{-x}$","Natural Log": "$\\ln(x)$","Logarithm": "$\\log_b(x)$",
    "Power": "$b^x$","Exp Growth": "$a e^{bx}$","Exp Decay": "$a e^{-bx}$",
    "Log Growth": "$a \\log_b(x)$","Log Decay": "$a \\log_b(x)^{-1}$"
        }

        algebraic = {
    "Polynomial": "$P(x) = a_n x^n + a_{n-1} x^{n-1} + \\cdots + a_1 x + a_0$",
    "Quadratic": "$ax^2 + bx + c$",
    "Cubic": "$ax^3 + bx^2 + cx + d$",
    "Linear": "$mx + b$",
    "Exponential": "$a e^{bx}$",
    "Rational": "$\\frac{P(x)}{Q(x)}$",
    "Absolute Value": "$|x|$",
    "Square Root": "$\\sqrt{x}$",
    "Cube Root": "$\\sqrt[3]{x}$",
    "Nth Root": "$\\sqrt[n]{x}$",
    "Logarithmic": "$a \\log_b(x) + c$",
    "Step Function": "$\\lfloor x \\rfloor$",
    "Greatest Integer": "$\\lfloor x \\rfloor$",
    "Least Integer": "$\\lceil x \\rceil$",
    "Piecewise": "$\\begin{cases} a x + b & \\text{if } x < 0 \\\\ c x^2 + d & \\text{if } x \\geq 0 \\end{cases}$",
    "Floor Function": "$\\lfloor x \\rfloor$",
    "Ceiling Function": "$\\lceil x \\rceil$"
}
        
        calculas = {
    "Derivative": "$\\frac{d}{dx} f(x)$",
    "Partial Derivative": "$\\frac{\\partial}{\\partial x} f(x, y)$",
    "Second Derivative": "$\\frac{d^2}{dx^2} f(x)$",
    "Integral": "$\\int f(x) \\, dx$",
    "Definite Integral": "$\\int_{a}^{b} f(x) \\, dx$",
    "Double Integral": "$\\int_{a}^{b} \\int_{c}^{d} f(x, y) \\, dy \\, dx$",
    "Triple Integral": "$\\int_{a}^{b} \\int_{c}^{d} \\int_{e}^{f} f(x, y, z) \\, dz \\, dy \\, dx$",
    "Surface Integral": "$\\int_{S} f(x, y, z) \\, dS$",
    "Line Integral": "$\\int_{C} f(x, y) \\, ds$",
    "Gradient": "$\\nabla f(x, y, z)$",
    "Divergence": "$\\nabla \\cdot \\mathbf{F}$",
    "Curl": "$\\nabla \\times \\mathbf{F}$",
    "Laplace Transform": "$\\mathcal{L}\\{f(t)\\}(s)$",
    "Inverse Laplace Transform": "$\\mathcal{L}^{-1}\\{F(s)\\}(t)$",
    "Fourier Transform": "$\\mathcal{F}\\{f(t)\\}(\\omega)$",
    "Inverse Fourier Transform": "$\\mathcal{F}^{-1}\\{F(\\omega)\\}(t)$",
    "Taylor Series": "$f(x) = f(a) + f'(a)(x - a) + \\frac{f''(a)}{2!}(x - a)^2 + \\cdots$",
    "Maclaurin Series": "$f(x) = f(0) + f'(0)x + \\frac{f''(0)}{2!}x^2 + \\cdots$",
    "Integral Test": "$\\int_{a}^{\\infty} f(x) \\, dx$",
    "Comparison Test": "$\\text{Compare } f(x) \\text{ and } g(x)$",
}


        def create_button(text, insert_text, parent):
            button = QPushButton(text, parent)
            button.setFixedWidth(160)
            button.setStyleSheet("""
font-size:15px;
                                 margin:4px;
                                 padding:3px;
                                 background:white;
""")
            button.pressed.connect(lambda: tsymcursor.insertText(insert_text))
            return button

        # Create a tab widget
        tab = QTabWidget(self.eqwin)  # Adjust the geometry as needed
        tab.setStyleSheet("""
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
            background: white;
            border: 0px solid lightgrey;
            padding: 5px;
            width:150px;
            border-radius:5px;
            margin-bottom:7px;
            margin:4px;
        }
                          QTabBar::tab:hover {
                          background:white;
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

        # Create the tab for Trigonometric Functions
        trig_functions_tab = QWidget()
        trig_functions_tab.setStyleSheet("""
background:white;
                           border-radius:7px;
                           padding:3px;
                           margin:7px;
""")
        trig_grid = QGridLayout(trig_functions_tab)

        # Add buttons for trigonometric functions
        row, column = 0, 0
        for name, insert_text in trigo_fn.items():
            button = create_button(name, insert_text, trig_functions_tab)
            trig_grid.addWidget(button, row, column)
            column += 1
            if column > 3:  # Adjust column limit as per your layout
                column = 0
                row += 1

        trig_functions_tab.setLayout(trig_grid)

        log_functions_tab = QWidget()
        log_functions_tab.setStyleSheet("""
background:white;
                           border-radius:7px;
                           padding:3px;
                           margin:7px;
""")
        log_grid = QGridLayout(log_functions_tab)

        # Add buttons for logarithmic functions
        row, column = 0, 0
        for name, insert_text in log_fn.items():
            button = create_button(name, insert_text, log_functions_tab)
            log_grid.addWidget(button, row, column)
            column += 1
            if column > 3:  # Adjust column limit as per your layout
                column = 0
                row += 1

        log_functions_tab.setLayout(log_grid)

        algebraic_functions_tab = QWidget()
        algebraic_functions_tab.setStyleSheet("""
background:white;
                           border-radius:7px;
                           padding:3px;
                           margin:7px;
""")
        algebraic_grid = QGridLayout(algebraic_functions_tab)

        # Add buttons for trigonometric functions
        row, column = 0, 0
        for name, insert_text in algebraic.items():
            button = create_button(name, insert_text, algebraic_functions_tab)
            algebraic_grid.addWidget(button, row, column)
            column += 1
            if column > 3:  # Adjust column limit as per your layout
                column = 0
                row += 1

        algebraic_functions_tab.setLayout(algebraic_grid)

        calculas_functions_tab = QWidget()
        calculas_functions_tab.setStyleSheet("""
background:white;
                           border-radius:7px;
                           padding:3px;
                           margin:7px;
""")
        calculas_grid = QGridLayout(calculas_functions_tab)

        # Add buttons for trigonometric functions
        row, column = 0, 0
        for name, insert_text in calculas.items():
            button = create_button(name, insert_text, calculas_functions_tab)
            calculas_grid.addWidget(button, row, column)
            column += 1
            if column > 3:  # Adjust column limit as per your layout
                column = 0
                row += 1

        calculas_functions_tab.setLayout(calculas_grid)

        # Add the Trigonometric Functions tab to the tab widget
        tab.addTab(trig_functions_tab, "Trigonometric Functions")
        tab.addTab(log_functions_tab, "Logarithmic Functions")
        tab.addTab(algebraic_functions_tab, "Algebraic Functions")
        tab.addTab(calculas_functions_tab, "Calculas Functions")

        self.eqwin.show()

    def show_link_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon("ME_Icons/link.png"))
        dialog.setWindowTitle("Add Link")
        dialog.setStyleSheet("""
QDialog {
                             background:#f2f2f2;
                             }
QLabel{
                             font-size:12px;
                             background:#f2f2f2;
                             }
QLineEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
QTextEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border:1px solid #ccc;
                             background:white;
                             }
QTextEdit:focus {
                             border:2px solid royalblue;}
QPushButton{
                             border-radius:5px;
                             padding:5px;
                             border:1px solid #ccc;
                             font-size:12px;
                             background:white;
                             }
QPushButton:hover{
                             color:royalblue;
                             border:2px solid royalblue;

""")
        layout = QFormLayout(dialog)
        
        self.link_url = QLineEdit()
        self.link_text = QLineEdit()
        layout.addRow("URL:", self.link_url)
        layout.addRow("Text:", self.link_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_link)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)

        button_stylesheet = """
            QPushButton:hover {
                border: 1px solid royalblue;
                color: royalblue;
            }
        """

        ok_button.setStyleSheet(button_stylesheet)
        cancel_button.setStyleSheet(button_stylesheet)
        
        dialog.setLayout(layout)
        dialog.exec()

    def add_link(self):
        url = self.link_url.text()
        text = self.link_text.text()
        if url:
            if text:
                self.text_edit.insertPlainText(f"[{text}]({url})")
                self.update_preview()
        elif url:
            self.text_edit.insertPlainText(f"[]({url})")
            self.update_preview()
        elif text:
            self.text_edit.insertPlainText(f"[{text}](url of link)")
            self.update_preview()
        else:
            self.text_edit.insertPlainText(f"[title of link](url of link)")
            self.update_preview()

    def show_image_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Insert Image")
        dialog.setWindowIcon(QtGui.QIcon("ME_Icons/image.png"))
        dialog.setStyleSheet("""
QDialog {
                             background:#f2f2f2;
                             }
QLabel{
                             font-size:12px;
                             background:#f2f2f2;
                             }
QLineEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
QTextEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border:1px solid #ccc;
                             background:white;
                             }
QTextEdit:focus {
                             border:2px solid royalblue;}
QPushButton{
                             border-radius:5px;
                             padding:5px;
                             border:1px solid #ccc;
                             font-size:12px;
                             background:white;
                             }
QPushButton:hover{
                             color:royalblue;
                             border:2px solid royalblue;

""")
        layout = QFormLayout(dialog)
        
        self.image_url = QLineEdit()
        self.alt_text = QLineEdit()
        layout.addRow("Image URL:", self.image_url)
        layout.addRow("Alt Text:", self.alt_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_image)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)

        button_stylesheet = """
            QPushButton:hover {
                border: 1px solid royalblue;
                color: royalblue;
            }
        """

        ok_button.setStyleSheet(button_stylesheet)
        cancel_button.setStyleSheet(button_stylesheet)
        
        dialog.setLayout(layout)
        dialog.exec()

    def open_progress_bar_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon("ME_Icons/progbar.png"))
        dialog.setWindowTitle("Insert Progress Bar")
        dialog.setStyleSheet("""
        QDialog {
            background:#f2f2f2;
        }
        QLabel {
            font-size:12px;
            background:#f2f2f2;
        }
        QLineEdit {
            border-radius:5px;
            font-size:12px;
            padding:5px;
            border-bottom:1px solid #ccc;
            background:white;
        }
        QLineEdit:focus {
            border:2px solid royalblue;
        }
        QPushButton {
            border-radius:5px;
            padding:5px;
            border:1px solid #ccc;
            font-size:12px;
            background:white;
        }
        QPushButton:hover {
            color:royalblue;
            border:2px solid royalblue;
        }
        """)

        layout = QFormLayout(dialog)

        # Create input fields with labels
        progress_value_input = QLineEdit(dialog)
        progress_value_input.setPlaceholderText("Enter progress percentage (0-100%)")
        progress_width_input = QLineEdit(dialog)
        progress_width_input.setPlaceholderText("Enter width (e.g., 200px, 50%)")
        progress_height_input = QLineEdit(dialog)
        progress_height_input.setPlaceholderText("Enter height (e.g., 20px)")
        progress_label_input = QLineEdit(dialog)
        progress_label_input.setPlaceholderText("Enter label text (optional)")

        # Set fixed width for all line edits
        fixed_width = 250  # Set suitable width for the placeholders
        for line_edit in [progress_value_input, progress_width_input, progress_height_input, progress_label_input]:
            line_edit.setFixedWidth(fixed_width)

        layout.addRow("Progress Value:", progress_value_input)
        layout.addRow("Progress Width:", progress_width_input)
        layout.addRow("Progress Height:", progress_height_input)
        layout.addRow("Label Text:", progress_label_input)

        # Create button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.add_progress_bar(
            progress_value_input.text(),
            progress_width_input.text(),
            progress_height_input.text(),
            progress_label_input.text(),
            dialog
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # Set custom styles for buttons
        button_stylesheet = """
            QPushButton:hover {
                border: 1px solid royalblue;
                color: royalblue;
            }
        """

        ok_button = button_box.button(QDialogButtonBox.Ok)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)

        ok_button.setStyleSheet(button_stylesheet)
        cancel_button.setStyleSheet(button_stylesheet)

        dialog.setLayout(layout)
        dialog.exec()


    def add_progress_bar(self, progress_value, progress_width, progress_height, progress_label, dialog):
        # Input validation for progress value
        if not progress_value.isdigit() or not (0 <= int(progress_value) <= 100):
            QMessageBox.warning(dialog, "Invalid Input", "Please enter a valid percentage between 0 and 100.")
            return

        max_val = 100  # Set maximum value for progress bar

        # Construct the style string
        style = ""
        if progress_width:
            style += f"width: {progress_width}; "
        if progress_height:
            style += f"height: {progress_height}; "

        # Construct the HTML for the progress bar
        progress_html = f'\n<div style="padding: 2px;">'
        if progress_label:
            progress_html += f'<label>{progress_label}</label><br>'
        progress_html += f'<progress value="{progress_value}" max="{max_val}" style="{style}"></progress>'
        progress_html += f'</div>'

        # Insert the progress bar tag at the cursor position
        cursor = self.text_edit.textCursor()
        cursor.insertText(progress_html)
        dialog.accept()
        self.update_preview()

    def add_image(self):
        url = self.image_url.text()
        alt_text = self.alt_text.text()
        if url:
            if alt_text:
                self.text_edit.insertPlainText(f"\n![{alt_text}]({url})")
                self.update_preview()
        elif url:
            self.text_edit.insertPlainText(f"\n![]({url})")
            self.update_preview()
        elif alt_text:
            self.text_edit.insertPlainText(f"\n![{alt_text}](url of image)")
            self.update_preview()
        else:
            self.text_edit.insertPlainText(f"\n![title of image](url of image)")
            self.update_preview()

    def show_section_header_dialog(self):
        dialog = QDialog(self)
        dialog.setGeometry(600, 300, 700, 500)
        dialog.setWindowIcon(QtGui.QIcon("ME_Icons/sectionheader.png"))
        dialog.setWindowTitle("Add Header")
        dialog.setStyleSheet("""
QDialog {
                             background:#f2f2f2;
                             }
QLabel{
                             font-size:12px;
                             background:#f2f2f2;
                             }
QLineEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QLineEdit:focus {
                             border:2px solid royalblue;}
QTextEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border:1px solid #ccc;
                             background:white;
                             }
QTextEdit:focus {
                             border:2px solid royalblue;}
QPushButton{
                             border-radius:5px;
                             padding:5px;
                             border:1px solid #ccc;
                             font-size:12px;
                             background:white;
                             }
QPushButton:hover{
                             color:royalblue;
                             border:1px solid royalblue;}

""")
        layout = QFormLayout(dialog)
        
        self.header_text = QLineEdit()
        layout.addRow("Header Text:", self.header_text)

        self.content_text = QTextEdit()
        layout.addRow("Content:", self.content_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_header)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)

        button_stylesheet = """
            QPushButton:hover {
                border: 1px solid royalblue;
                color: royalblue;
            }
        """

        ok_button.setStyleSheet(button_stylesheet)
        cancel_button.setStyleSheet(button_stylesheet)
        
        dialog.setLayout(layout)
        dialog.exec()

    def add_header(self):
        header = self.header_text.text()
        content = self.content_text.toPlainText()
        if header:
            if content:
                self.text_edit.insertPlainText(f"<details>\n<summary>{header}</summary>\n{content}\n</details>")
                self.update_preview()
        elif content:
            self.text_edit.insertPlainText(f"<details>\n<summary>Your Header Here</summary>\n{content}\n</details>")
            self.update_preview()
        elif header:
            self.text_edit.insertPlainText(f"<details>\n<summary>{header}</summary>\nYour Content Here\n</details>")
            self.update_preview()
        else:
            self.text_edit.insertPlainText(f"<details>\n<summary>Your Header Here</summary>\nYour Content Here\n</details>")
            self.update_preview()

    def insert_blockquote(self):
        cursor = self.text_edit.textCursor()
        cursor.insertText("> " + cursor.selectedText().replace("\n", "\n> "))
        self.update_preview()
        self.admonition_combobox.setCurrentIndex(0)

    def insert_code_block(self):
        self.format_text("```\n", "\n```")
        self.admonition_combobox.setCurrentIndex(0)

    def highlight_text(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.beginEditBlock()
            cursor.removeSelectedText()
            cursor.insertText(f'=={selected_text}==')
            cursor.endEditBlock()
            self.update_preview()

    def make_subscript(self):
        self.format_text("~", "~")

    def make_superscript(self):
        self.format_text("^", "^")

    def insert_horizontal_line(self):
        self.text_edit.insertPlainText("\n---\n")
        self.update_preview()

    def insert_comment(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.beginEditBlock()
            cursor.removeSelectedText()
            cursor.insertText(f'<!-- {selected_text} -->')
            cursor.endEditBlock()
            self.update_preview()

    def highlight_headers(self):
        pass

    def remove_comment(self):
        """
        Removes HTML comments from the selected text.

        If text is selected, this method removes any HTML comments from the
        selected text and replaces the selected text with the uncommented text.
        """
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            uncommented_text = selected_text.replace("<!-- ", "").replace(" -->", "")
            cursor.beginEditBlock()
            cursor.removeSelectedText()
            cursor.insertText(uncommented_text)
            cursor.endEditBlock()
            self.update_preview()

    def new(self):
        spawn = BrightnessEditor()
        spawn.show()

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setStyleSheet("""
                      QTextEdit {
                          selection-background-color: royalblue;
                selection-color: white;
                      }
                      QLineEdit {
                          selection-background-color: royalblue;
                selection-color: white;
                      }
QWidget{
color:black;
}
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
        QToolTip {
        background: #ffffff; /* White background */
        color: #000000; /* Black text */
        border: 1px solid #cccccc; /* Light grey border */
        border-radius: 10px; /* Rounded corners */
        padding: 3px; /* Comfortable padding */
        font-size: 14px; /* Standard font size */
    }
QInputDialog QPushButton{ 
border-radius:5px;
                             padding:5px;
                             border:1px solid #ccc;
                             font-size:12px;
                             background:white;
                          }
QInputDialog QPushButton:hover{
                          color:royalblue;
                             border:2px solid royalblue;
                          }
                          QInputDialog QLineEdit {
                             border-radius:5px;
                             font-size:12px;
                             padding:5px;
                             border-bottom:1px solid #ccc;
                             background:white;
                             }
QInputDialog QLineEdit:focus {
                             border:2px solid royalblue;}
    """)
    editor = BrightnessEditor()
    editor.showMaximized()

    sys.exit(app.exec())

if __name__ == '__main__':   
    main()
