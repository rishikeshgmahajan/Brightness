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


TEMPLATES_FILE = "templates.json"
PREINSTALLED_TEMPLATES = [
    "README 1",
    "README 2",
    "Project Overview",
    "Getting Started",
    "Tutorial",
    "Project License",
    "Feature Request",
    "Bug Report"
]

class TemplateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Templates")
        self.setWindowIcon(QtGui.QIcon("ME_Icons/templates.png"))
        self.setFixedSize(600, 600)

        # Set the background color of the dialog to light grey
        self.setStyleSheet("background-color: #f2f2f2;")
        
        self.layout = QVBoxLayout(self)

        # Search bar layout (QLineEdit and QPushButton side by side)
        self.search_layout = QHBoxLayout()
        
        # Create the search line edit
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search templates")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 6px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid royalblue;
            }
        """)
        
        # Create the search button with an icon
        self.search_button = QPushButton(self)
        self.search_button.setIcon(QtGui.QIcon("ME_Icons/search.png"))  # Replace with your icon path
        self.search_button.setStyleSheet("""
            QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white;}
            QPushButton:hover{
                                   border:1px solid royalblue;
                                   color:royalblue;}
        """)
        self.search_button.clicked.connect(self.perform_search)

        # Add the search bar and button to the search layout
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)
        
        # Add the search layout to the main layout
        self.layout.addLayout(self.search_layout)
        
        # Preinstalled Templates Label and List Styling
        self.preinstalled_label = QLabel("Preinstalled Templates", self)
        self.preinstalled_label.setStyleSheet("""font-weight: bold;
        border:none;
        font-size:14px;
        """)
        self.list_widget_preinstalled = QListWidget(self)
        self.list_widget_preinstalled.setStyleSheet("""
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
            QListWidget {
                background-color: #fafafa;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 2px;
                margin:1px;
                border-radius:4px;
            }
            QListWidget::item:hover {
                background-color: #e6e6e6;
            }
            QListWidget::item:selected {
                background-color: #97B2ED;
                color:black;
            }
        """)

        # Frame for Preinstalled Templates Section
        self.frame_preinstalled = QFrame(self)
        self.frame_preinstalled.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
                border:1px solid rgb(234, 234, 234);
            }
        """)
        frame_layout_preinstalled = QVBoxLayout(self.frame_preinstalled)
        frame_layout_preinstalled.addWidget(self.preinstalled_label)
        frame_layout_preinstalled.addWidget(self.list_widget_preinstalled)
        
        self.layout.addWidget(self.frame_preinstalled)
        
        # User Templates Label and List Styling
        self.user_label = QLabel("User Templates", self)
        self.user_label.setStyleSheet("""font-weight: bold;
        border:none;
        font-size:14px;
        """)
        self.list_widget_user = QListWidget(self)
        self.list_widget_user.setStyleSheet("""
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
            QListWidget {
                background-color: #fafafa;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 2px;
                margin:1px;
                border-radius:4px;
            }
            QListWidget::item:hover {
                background-color: #e6e6e6;
            }
            QListWidget::item:selected {
                background-color: #97B2ED;
                color:black;
            }
        """)

        # Frame for User Templates Section
        self.frame_user = QFrame(self)
        self.frame_user.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
                border:1px solid rgb(234, 234, 234);
            }
        """)
        frame_layout_user = QVBoxLayout(self.frame_user)
        frame_layout_user.addWidget(self.user_label)
        frame_layout_user.addWidget(self.list_widget_user)
        
        self.layout.addWidget(self.frame_user)
        
        # Load templates from file
        self.load_templates()

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()

        # Save button for new template
        self.save_button = QPushButton("Save as new template", self)
        self.save_button.clicked.connect(self.save_new_template)
        self.save_button.setStyleSheet("""
                                   QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white; }

QPushButton:hover {
    border:1px solid royalblue;
    color:royalblue;
}
""")
        self.button_layout.addWidget(self.save_button)

        # Delete selected template
        self.delete_button = QPushButton("Delete template", self)
        self.delete_button.clicked.connect(self.delete_template)
        self.delete_button.setStyleSheet("""
                                   QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white; }

QPushButton:hover {
    border:1px solid royalblue;
    color:royalblue;
}
""")
        self.button_layout.addWidget(self.delete_button)

        # Delete all templates
        self.delete_all_button = QPushButton("Delete all templates", self)
        self.delete_all_button.clicked.connect(self.delete_all_templates)
        self.delete_all_button.setStyleSheet("""
                                   QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white; }

QPushButton:hover {
    border:1px solid royalblue;
    color:royalblue;
}
""")
        self.button_layout.addWidget(self.delete_all_button)

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        # Set double-click handler to open template
        self.list_widget_preinstalled.doubleClicked.connect(self.open_template)
        self.list_widget_user.doubleClicked.connect(self.open_template)
        self.list_widget_user.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget_user.customContextMenuRequested.connect(self.show_context_menu)

    def perform_search(self):
        """Search the templates based on the input text and select the matching templates."""
        search_text = self.search_bar.text().strip()
        search_text = re.sub(r'\s+', ' ', search_text)  # Normalize spaces

        if search_text == "":
            self.list_widget_user.clearSelection()
            self.list_widget_preinstalled.clearSelection()
        else:
            # Search and select matching templates in preinstalled list
            for i in range(self.list_widget_preinstalled.count()):
                item = self.list_widget_preinstalled.item(i)
                if re.search(re.escape(search_text), item.text(), re.IGNORECASE):
                    item.setSelected(True)
                else:
                    item.setSelected(False)
            
            # Search and select matching templates in user list
            for i in range(self.list_widget_user.count()):
                item = self.list_widget_user.item(i)
                if re.search(re.escape(search_text), item.text(), re.IGNORECASE):
                    item.setSelected(True)
                else:
                    item.setSelected(False)

    def load_templates(self):
        """ Load templates from a file and organize them into sections """
        self.list_widget_preinstalled.addItems(PREINSTALLED_TEMPLATES)
        
        # Load user templates from file as a dictionary
        templates = self.get_all_templates()
        
        if templates:
            # Add user templates to the list widget
            for template_name in templates:
                self.list_widget_user.addItem(template_name)

    def save_new_template(self):
        """ Save a new template entered by the user """
        # Create a custom QDialog to capture the template name
        dialog = QDialog(self)
        dialog.setWindowTitle("New Template")

        # Layout for the dialog
        layout = QVBoxLayout(dialog)

        # Create a QLineEdit to enter the template name
        line_edit = QLineEdit(dialog)
        line_edit.setPlaceholderText("Enter template name")
        line_edit.setStyleSheet("""
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
        layout.addWidget(line_edit)

        # OK button
        ok_button = QPushButton("OK", dialog)
        ok_button.setStyleSheet("""
            QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white;}

QPushButton:hover{
border:1px solid royalblue;
                                   color:royalblue;}
        """)
        layout.addWidget(ok_button)

        # Cancel button
        cancel_button = QPushButton("Cancel", dialog)
        cancel_button.setStyleSheet("""
            QPushButton{
                                   border-radius:5px;
                                   padding:6px;
                                   border:1px solid #ccc;
                                   background:white;}

QPushButton:hover{
border:1px solid royalblue;
                                   color:royalblue;}
        """)
        layout.addWidget(cancel_button)

        # Handle button clicks
        def on_ok():
            template_name = line_edit.text()
            if template_name:
                # Get the Markdown content from QTextEdit
                template_content = self.parent().text_edit.toPlainText()
                self.save_template(template_name, template_content)
            dialog.accept()

        def on_cancel():
            dialog.reject()

        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(on_cancel)

        # Show the dialog
        dialog.exec()

    def save_template(self, template_name, template_content):
        """ Save the new template to the file and update the list """
        templates = self.get_all_templates()
        templates[template_name] = template_content  # Add template to dictionary
        
        # Save the updated templates dictionary to the JSON file
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(templates, f)
        
        # Update the list widget (add to user section)
        self.list_widget_user.addItem(template_name)

    def open_template(self):
        """ Open the selected template """
        item = self.sender().currentItem()
        if item:
            template_name = item.text()
            # Retrieve template content for the selected template
            if template_name in PREINSTALLED_TEMPLATES:
                if template_name == "README 1":
                    template_content = ("# Project Title\n\nBrief description of your project.\n\n## Installation\n\n1. Clone the repository:\n    ```bash\n    git clone <repository-url>\n    ```\n2. Install the dependencies:\n    ```bash\n    pip install -r requirements.txt\n    ```\n\n## Usage\n\nSteps for using your project:\n\n1. Run the main program:\n    ```bash\n    python main.py\n    ```\n\n2. Example of how to use the functionality:\n    ```python\n    import your_project\n    your_project.run()\n    ```\n\n## Contributing\n\n1. Fork the repository.\n2. Create a new branch (`git checkout -b feature-branch`).\n3. Commit your changes (`git commit -am 'Add new feature'`).\n4. Push to the branch (`git push origin feature-branch`).\n5. Create a new Pull Request.\n\n## License\n\nThis project is licensed under the {License Name} License - see the [LICENSE](LICENSE) file for details.\n\n## Acknowledgments\n\n- Inspiration\n- Resources used\n")
                elif template_name == "README 2":
                    template_content = ("# Project Name\n\n![Project Logo](path/to/logo.png)\n\n> **Project tagline or one-liner.**\n> A brief description of what the project does.\n\n---\n\n## Table of Contents\n- [Project Overview](#project-overview)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Features](#features)\n- [Contributing](#contributing)\n- [License](#license)\n- [Acknowledgements](#acknowledgements)\n\n---\n\n## Project Overview\n\n### About\n\nProvide a detailed description of the project here. What problem does it solve? How does it work? Be concise but informative.\n\n- **Tech Stack**: List the technologies used in the project.\n- **Key Highlights**: Describe any standout features or functionalities of the project.\n\n### Screenshots\n\n![Project Screenshot](path/to/screenshot.png)\n\n> Add screenshots, GIFs, or videos of your project in action.\n\n---\n\n## Installation\n\nTo get this project up and running on your local machine for development and testing purposes, follow these instructions.\n\n### Prerequisites\n\n- List any prerequisites or dependencies required before installation (e.g., Python 3.x, Node.js).\n- Provide installation instructions for each dependency.\n\n### Steps\n\n1. **Clone the repository**:\n   ```bash\ngit clone https://github.com/your-username/project-name.git\ncd project-name\n```")
                elif template_name == "Project Overview":
                    template_content = ("# Project Overview\n\nThis is a template for documentation with project overview, installation instructions, and usage examples.\n\n## Table of Contents\n- [Overview](#overview)\n- [Installation](#installation)\n- [Usage](#usage)\n\n## Overview\n\nProvide a detailed overview of your project, its goals, and objectives.\n\n## Installation\n\n1. Clone the repository:\n    ```bash\n    git clone <repository-url>\n    ```\n2. Install dependencies:\n    ```bash\n    pip install -r requirements.txt\n    ```\n\n## Usage\n\nExample of how to use your project:\n```python\nimport project\nproject.run()\n```")
                elif template_name == "Getting Started":
                    template_content = ("# Introduction\n\nWelcome to this project. Here’s a brief introduction to the project and its purpose.\n\n## Getting Started\n\nTo get started, follow these steps:\n1. Clone the repository:\n    ```bash\n    git clone <repository-url>\n    ```\n2. Install the dependencies:\n    ```bash\n    pip install -r requirements.txt\n    ```\n3. Run the project:\n    ```bash\n    python app.py\n    ```")
                elif template_name == "Tutorial":
                    template_content = ("# Tutorial: How to Use Project\n\nWelcome to the tutorial. In this guide, we’ll walk you through the setup and usage of the project.\n\n## Prerequisites\n- [List of tools or knowledge needed to follow the tutorial.]\n\n## Steps\n1. **Step 1**: [Explanation of step]\n   - Example code or command\n2. **Step 2**: [Explanation of step]\n   - Example code or command\n\n## Conclusion\n[Wrap-up, next steps, or additional learning resources.]\n\n## Troubleshooting\n[Provide common issues and solutions.]\n\n## Additional Resources\n- [Link to further tutorials or documentation]")
                elif template_name == "Project License":
                    template_content = ("# Project License\n\nThis project is licensed under the {License Name} License.\n\n## License Terms\n\nBy using this project, you agree to the following terms:\n- You can use, modify, and distribute this code under the terms of the {License Name} License.\n\nSee the [LICENSE](LICENSE) file for full details.")
                elif template_name == "Feature Request":
                    template_content = ("# Feature Request\n\n## Summary\nPlease provide a summary of the feature you are requesting.\n\n## Problem\nWhat problem does this feature solve?\n\n## Expected Behavior\nDescribe what you expect the behavior of the feature to be.\n\n## Additional Context\nAdd any other context about the feature request, such as use cases, examples, or references to other work.")
                elif template_name == "Bug Report":
                    template_content = ("# Bug Report\n\n## Summary\nProvide a short summary of the bug.\n\n## Steps to Reproduce\nList the steps needed to reproduce the issue.\n\n1. Step 1\n2. Step 2\n3. Step 3\n\n## Expected Behavior\nDescribe what you expected to happen.\n\n## Actual Behavior\nDescribe what actually happened.\n\n## Screenshots or Logs\nIf applicable, add screenshots or logs to help explain your problem.\n\n## Environment\n- OS: [e.g. Windows, macOS, Linux]\n- Version: [e.g. v1.2.3]\n- Additional context")

            else:
                templates = self.get_all_templates()
                template_content = templates.get(template_name, "Template not found")
            
            # Display template content in the QTextEdit
            self.show_template_content(template_name, template_content)

    def show_template_content(self, template_name, template_content):
        """ Show template content in the QTextEdit """
        self.parent().text_edit.setPlainText(template_content)

    def delete_template(self):
        """ Delete the selected template """
        item = self.list_widget_user.currentItem()  # Directly get the selected item from the user template list
        if item:
            template_name = item.text()
            if template_name not in PREINSTALLED_TEMPLATES:  # Ensure the template isn't preinstalled
                templates = self.get_all_templates()
                if template_name in templates:
                    del templates[template_name]  # Delete the template from the dictionary
                    self.save_all_templates(templates)  # Save the updated templates
                    self.list_widget_user.takeItem(self.list_widget_user.row(item))  # Remove from the list widget


    def delete_all_templates(self):
        """ Delete all user templates """
        templates = self.get_all_templates()
        templates.clear()
        self.save_all_templates(templates)
        self.list_widget_user.clear()

    def save_all_templates(self, templates):
        """ Save all templates to the JSON file """
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(templates, f)

    def get_all_templates(self):
        """ Get all user templates from the file as a dictionary """
        if os.path.exists(TEMPLATES_FILE):
            with open(TEMPLATES_FILE, 'r') as f:
                templates = json.load(f)  # Load the JSON data into a dictionary
                if isinstance(templates, dict):
                    return templates
                else:
                    return {}  # In case the data is not a dictionary, return an empty dictionary
        return {}

    def show_context_menu(self, position):
        """Show context menu when right-clicking on an item in the list widget."""
        # Get the list widget where the context menu is requested
        list_widget = self.sender()

        # Create the context menu
        context_menu = QMenu(self)

        # Add actions for Open, Delete, and Rename
        open_action = QAction("Open", self)
        delete_action = QAction("Delete", self)
        rename_action = QAction("Rename", self)

        # Add actions to the context menu
        context_menu.addAction(open_action)
        context_menu.addAction(delete_action)
        context_menu.addAction(rename_action)

        context_menu.setStyleSheet("""
        QMenu {
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 2px;
        }
        
        QMenu::item {
            background-color: transparent;
            color: black;
            padding: 4px;
            margin:3px;
            width:70px;
            border-radius: 5px;
        }
        
        QMenu::item:selected {
            background-color: #97B2ED;
            color: Black;
        }
        
        QMenu::item:disabled {
        }
        
        QMenu::separator {
        }
        """)

        # Connect actions to their respective slots
        open_action.triggered.connect(lambda: self.open_template_from_menu(list_widget))
        delete_action.triggered.connect(lambda: self.delete_template_from_menu(list_widget))
        rename_action.triggered.connect(lambda: self.rename_template_from_menu(list_widget))

        # Show the context menu at the cursor position
        context_menu.exec(list_widget.mapToGlobal(position))

    def open_template_from_menu(self, list_widget):
        """Open the selected template."""
        item = list_widget.currentItem()
        if item:
            template_name = item.text()
            template_content = self.get_template_content(template_name)
            self.show_template_content(template_name, template_content)

    def delete_template_from_menu(self, list_widget):
        """Delete the selected template."""
        item = list_widget.currentItem()
        if item:
            template_name = item.text()
            if template_name not in PREINSTALLED_TEMPLATES:  # Ensure the template isn't preinstalled
                templates = self.get_all_templates()
                if template_name in templates:
                    del templates[template_name]  # Delete the template from the dictionary
                    self.save_all_templates(templates)  # Save the updated templates
                    list_widget.takeItem(list_widget.row(item))  # Remove from the list widget

    def rename_template_from_menu(self, list_widget):
        """Rename the selected template."""
        item = list_widget.currentItem()
        if item:
            template_name = item.text()
            
            # Ensure the template exists in the dictionary
            templates = self.get_all_templates()
            
            # Check if the template name exists in the templates
            if template_name in templates:
                new_name, ok = QInputDialog.getText(self, "Rename Template", "Enter new template name:", text=template_name)
                if ok and new_name:
                    # Check if the new name is valid and doesn't already exist
                    if new_name not in templates and new_name != template_name:
                        # Rename the template in the dictionary
                        templates[new_name] = templates.pop(template_name)  # Rename
                        self.save_all_templates(templates)  # Save the updated templates
                        item.setText(new_name)  # Update the list widget display
                    else:
                        self.show_error_message("Template name already exists or is invalid!")
                else:
                    self.show_error_message("Rename operation canceled or invalid name.")
            else:
                self.show_error_message(f"Template '{template_name}' not found in the dictionary!")

    def show_error_message(self, message):
        """Show an error message."""
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(message)
        error_dialog.setWindowTitle("Templates")
        error_dialog.setStyleSheet("""
        QPushButton{
                                 border-radius:7px;
                                 border:1px solid #ccc;
                          padding:3px;}
QPushButton:hover{
                          border:1px solid royalblue;
                          color:royalblue;
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
        """)
        error_dialog.setWindowIcon(QtGui.QIcon("ME_Icons/templates.png"))

    def get_template_content(self, template_name):
        """Retrieve the template content for the selected template."""
        # Load the template content based on the template name
        if template_name in PREINSTALLED_TEMPLATES:
            return "## Preinstalled template content"
        else:
            templates = self.get_all_templates()
            return templates.get(template_name, "Template not found")
