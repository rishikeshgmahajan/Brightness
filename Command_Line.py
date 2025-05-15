from PySide6.QtWidgets import QMessageBox
import os
import pandas as pd
import tabulate
import re
from urllib.parse import quote
import sys


class CommandHandler:
    def __init__(self, parent):
        self.parent = parent  # Reference to the main window or editor

    def Command_Line_Codes(self):
        input_text = self.parent.command_line.text()  # Ensure `self.parent.command_line` exists

        if input_text == "":
            self.parent.command_line.setFocus()

        elif input_text.startswith("open"):
            parts = input_text.split(" ", 1)  # Split at first space
            if len(parts) == 1 or parts[1].strip() == "*":
                self.parent.open_file()
            else:
                file_path = parts[1].strip('"')
                valid_extensions = (".md", ".commonmark", ".markdown", ".gfm", ".docx", ".tex", ".odt", ".rtf", ".txt")

                if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in valid_extensions):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        self.parent.text_edit.setPlainText(content)
                    except Exception as e:
                        self.show_error_message(f"Error opening file:\n{str(e)}")
                else:
                    self.show_error_message(f"Invalid file or file type:\n{file_path}")

        elif input_text == "save":
            self.parent.save_file()

        elif input_text.startswith("saveAs"):
            parts = input_text.split(" ", 1)
            if len(parts) == 1 or parts[1].strip() == "*":
                self.parent.save_file_as()
            else:
                file_path = parts[1].strip('"')
                valid_extensions = (".md", ".commonmark", ".markdown", ".gfm", ".docx", ".tex", ".odt", ".rtf", ".txt")

                if any(file_path.lower().endswith(ext) for ext in valid_extensions):
                    try:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(self.parent.text_edit.toPlainText())
                    except Exception as e:
                        self.show_error_message(f"Error saving file:\n{str(e)}")
                else:
                    self.show_error_message(f"Invalid file type for saving:\n{file_path}")

        elif input_text.startswith("saveAsPdf"):
            parts = input_text.split(" ", 1)
            if len(parts) == 1 or parts[1].strip() == "*":
                self.parent.save_as_pdf()  # Opens Save As dialog
            else:
                file_path = parts[1].strip().strip('"')
                file_path = os.path.splitext(file_path)[0] + ".pdf"  # Ensure .pdf extension

                try:
                    # Print the rendered Markdown preview to a PDF file
                    self.parent.preview_browser.page().printToPdf(file_path, lambda: self.show_info_message(f"PDF saved: {file_path}"))
                except Exception as e:
                    self.show_error_message(f"Error saving PDF:\n{str(e)}")

        elif input_text.startswith("saveAsHtml"):
            parts = input_text.split(" ", 1)
            if len(parts) == 1 or parts[1].strip() == "*":
                self.parent.save_html_preview()
            else:
                file_path = parts[1].strip().strip('"')
                file_path = os.path.splitext(file_path)[0] + ".html"  # Ensure .html extension

                try:
                    self.parent.save_html_preview(file_path)
                except Exception as e:
                    self.show_error_message(f"Error saving HTML:\n{str(e)}")

        elif input_text.startswith("insertImage"):
            parts = input_text.split(" ", 2)  # Split into at most three parts

            if len(parts) == 2 and parts[1].strip() == "*":
                self.parent.show_image_dialog()

            elif len(parts) == 2:  # If only URL is provided
                image_url = parts[1].strip().strip('"')
                markdown_image = f"![Image]({image_url})"
                cursor = self.parent.text_edit.textCursor()
                cursor.insertText(markdown_image)

            elif len(parts) == 3:  # If alt text is provided
                alt_text_flag, image_url = parts[1], parts[2].strip().strip('"')

                if alt_text_flag.startswith("-altText"):
                    alt_text = alt_text_flag.replace("-altText", "")
                elif alt_text_flag.startswith("-sAltText"):
                    alt_text = alt_text_flag.replace("-sAltText", "").replace("_", " ")
                else:
                    self.show_error_message("Invalid alt text flag. Use -altText or -sAltText.")
                    sys.exit(1)

                markdown_image = f"![{alt_text}]({image_url})"
                cursor = self.parent.text_edit.textCursor()
                cursor.insertText(markdown_image)

            else:
                self.show_error_message("Invalid command format.")

        elif input_text.startswith("insertLink"):
            parts = input_text.split(" ", 2)  # Split into at most three parts

            if len(parts) == 2 and parts[1].strip() == "*":
                self.parent.show_link_dialog()

            elif len(parts) == 2:  # If only URL is provided
                image_url = parts[1].strip().strip('"')
                markdown_image = f"[Link]({image_url})"
                cursor = self.parent.text_edit.textCursor()
                cursor.insertText(markdown_image)

            elif len(parts) == 3:  # If alt text is provided
                alt_text_flag, image_url = parts[1], parts[2].strip().strip('"')

                if alt_text_flag.startswith("-altText"):
                    alt_text = alt_text_flag.replace("-altText", "")
                elif alt_text_flag.startswith("-sAltText"):
                    alt_text = alt_text_flag.replace("-sAltText", "").replace("_", " ")
                else:
                    self.show_error_message("Invalid alt text flag. Use -altText or -sAltText.")
                    sys.exit(1)

                markdown_image = f"[{alt_text}]({image_url})"
                cursor = self.parent.text_edit.textCursor()
                cursor.insertText(markdown_image)

            else:
                self.show_error_message("Invalid command format.")

        elif input_text.startswith("insertBadge"):
            # Define valid styles
            valid_styles = {"flat", "plastic", "flat-square", "for-the-badge", "social"}

            # Regular expression to extract flags without space after them
            pattern = r"-(label|sLabel|msg|message|sMsg|sMessage|LabelColor|MsgColor|MessageColor|style|logo|LogoColor|LogoWidth|link)([^\s-]+)"
            matches = re.findall(pattern, input_text)

            # Convert extracted data into a dictionary
            badge_params = {key: value.strip() for key, value in matches}

            # Handle required parameters
            label = badge_params.get("label") or badge_params.get("sLabel")
            message = badge_params.get("msg") or badge_params.get("message") or badge_params.get("sMsg") or badge_params.get("sMessage")

            # If -sLabel or -sMsg is used, replace underscores with spaces
            if "sLabel" in badge_params:
                label = label.replace("_", " ")
            if "sMsg" in badge_params or "sMessage" in badge_params:
                message = message.replace("_", " ")

            if not label or not message:
                print("Error: -label and -msg (or their alternatives) are required.")
            else:
                # Optional parameters
                label_color = badge_params.get("LabelColor", "grey")
                msg_color = badge_params.get("MsgColor") or badge_params.get("MessageColor") or "blue"
                style = badge_params.get("style", "flat")

                if style not in valid_styles:
                    print("Error: Invalid style. Choose from flat, plastic, flat-square, for-the-badge, social.")
                else:
                    logo = badge_params.get("logo", "")
                    logo_color = badge_params.get("LogoColor", "")
                    logo_width = badge_params.get("LogoWidth", "")
                    link = badge_params.get("link", "")

                    # Construct Shields.io URL
                    url = f"https://img.shields.io/badge/{quote(label)}-{quote(message)}-{quote(label_color)}"
                    params = []

                    if msg_color:
                        params.append(f"color={quote(msg_color)}")
                    if style:
                        params.append(f"style={quote(style)}")
                    if logo:
                        params.append(f"logo={quote(logo)}")
                    if logo_color:
                        params.append(f"LogoColor={quote(logo_color)}")
                    if logo_width:
                        params.append(f"LogoWidth={quote(logo_width)}")
                    if link:
                        params.append(f"link={quote(link)}")

                    if params:
                        url += "?" + "&".join(params)

                    # Generate Markdown
                    markdown_badge = f"![{label}]({url})"
                    self.parent.text_edit.insertPlainText(markdown_badge)

        elif input_text.startswith("insertTable"):
            parts = input_text.split(" ", 1)
            if len(parts) == 1 or parts[1].strip() == "*":
                self.parent.save_file_as()
            else:
                args = parts[1].strip().split()
                file_path = args[-1].strip('"')
                if not os.path.exists(file_path):
                    QMessageBox.warning(self.parent, "Invalid File Path", "The specified file does not exist.")
                    return
                
                valid_extensions = (".csv", ".xls", ".xlsx", ".ods", ".db")
                if not file_path.lower().endswith(valid_extensions):
                    QMessageBox.warning(self.parent, "Invalid File Type", "Only table and spreadsheet files (CSV, Excel, ODS, Database) are supported.")
                    return
                
                sheet_name = None
                alignments = {}
                remaining_args = []
                
                for arg in args[:-1]:
                    match = re.match(r"-(center|right|left)([0-9,]*)", arg)
                    if match:
                        align_type, cols = match.groups()
                        cols = list(map(int, cols.split(","))) if cols else []
                        alignments[align_type] = cols
                    else:
                        remaining_args.append(arg)
                
                if remaining_args:
                    sheet_name = remaining_args[-1]
                
                try:
                    if file_path.lower().endswith(".csv"):
                        df = pd.read_csv(file_path)
                    elif file_path.lower().endswith((".xls", ".xlsx", ".ods")):
                        excel_file = pd.ExcelFile(file_path, engine="odf" if file_path.lower().endswith(".ods") else None)
                        if sheet_name and sheet_name in excel_file.sheet_names:
                            df = excel_file.parse(sheet_name)
                        else:
                            df = excel_file.parse(excel_file.sheet_names[0])  # Default to first sheet
                    elif file_path.lower().endswith(".db"):
                        import sqlite3
                        conn = sqlite3.connect(file_path)
                        query = "SELECT name FROM sqlite_master WHERE type='table';"
                        tables = pd.read_sql(query, conn)
                        if tables.empty:
                            QMessageBox.warning(self.parent, "Database Error", "No tables found in the database.")
                            return
                        table_name = tables.iloc[0, 0]
                        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
                        conn.close()
                    
                    max_columns = len(df.columns)
                    column_alignment = [":---" for _ in range(max_columns)]
                    
                    for align_type, cols in alignments.items():
                        if not cols:
                            cols = list(range(1, max_columns + 1))
                        for col in cols:
                            if col - 1 < max_columns:
                                if align_type == "center":
                                    column_alignment[col - 1] = ":---:"
                                elif align_type == "right":
                                    column_alignment[col - 1] = "---:"
                                elif align_type == "left":
                                    column_alignment[col - 1] = ":---"
                    
                    md_table = "| " + " | ".join(df.columns) + " |\n"
                    md_table += "| " + " | ".join(column_alignment) + " |\n"
                    for _, row in df.iterrows():
                        md_table += "| " + " | ".join(map(str, row)) + " |\n"
                
                except Exception as e:
                    QMessageBox.warning(self.parent, "File Read Error", f"Error reading file:\n{str(e)}")
                    return
                
                self.parent.text_edit.insertPlainText(f"\n{md_table}\n")


        elif input_text == "new":
            self.parent.new()

        elif input_text == "end":
            self.parent.toggle_command_line()

        else:
            QMessageBox.warning(self.parent, "Input Error", "Invalid statement.")

    def show_error_message(self, message):
        msg_box = QMessageBox(self.parent)  # FIXED: Removed extra parentheses
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()
