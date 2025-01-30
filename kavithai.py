import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox, QWidget, QDialog, QDialogButtonBox, QTabWidget, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import Qt
import time

# Define black theme stylesheet
black_stylesheet = """
    QMainWindow {
        background-color: #2E2E2E;
        color: white;
    }
    QTextEdit, QLineEdit {
        background-color: #444444;
        color: white;
        border: 1px solid #666666;
    }
    QTextEdit {
        border-radius: 5px;
    }
    QLabel {
        color: white;
    }
    QPushButton {
        background-color: #5A5A5A;
        color: white;
        border: 1px solid #777777;
        border-radius: 5px;
        padding: 5px 15px;
    }
    QPushButton:hover {
        background-color: #888888;
    }
    QMenuBar {
        background-color: #333333;
        color: white;
    }
    QMenuBar::item:selected {
        background-color: #555555;
    }
    QMenu {
        background-color: #333333;
        color: white;
    }
    QMenu::item:selected {
        background-color: #555555;
    }
    QDialog {
        background-color: #333333;
        color: white;
    }
    
"""

def evaluate_expression(expr):
    """Evaluate basic arithmetic expressions."""
    try:
        expr = expr.strip()
        if not re.match(r"^[\d+\-*/().\s]+$", expr):
            return f"Error: Invalid arithmetic expression - {expr}"
        
        # Evaluate the expression using eval (Python's built-in function)
        return str(eval(expr))
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception:
        return f"Error: Invalid arithmetic expression - {expr}"

def is_valid_string(value):
    """Check if the value is a properly formatted string (enclosed in double quotes)."""
    return value.startswith('"') and value.endswith('"')

def is_valid_number(value):
    """Check if the value is a valid number (integer or float)."""
    return re.match(r"^\d+(\.\d+)?$", value) is not None

def ullitu(prompt):
    """Simulate user input dynamically."""
    return prompt  # Simply return the prompt as an example of how user would input.

def parse_nex(code, user_input=None):
    """Parse and execute Nex syntax, including loops and dynamic input."""
    statements = code.split("\n")
    results = []

    for statement in statements:
        statement = statement.strip()
        
        if statement.startswith("accu("):
            # Handle accu() as a print statement
            content = re.findall(r'accu\((.*?)\)', statement)
            if content:
                parts = [p.strip() for p in content[0].split(",")]
                output = ""
                for part in parts:
                    if is_valid_string(part):
                        output += part[1:-1]  # Remove quotes and add to output
                    elif is_valid_number(part):
                        output += part
                    elif re.match(r"[\d+\-*/().\s]+", part):
                        output += evaluate_expression(part)
                    elif "ullitu" in part:
                        prompt = re.findall(r'ullitu\("(.*?)"\)', part)
                        if prompt:
                            user_input_value = user_input  # Get the user input
                            output += f" {prompt[0]}: {user_input_value}"  # Display user input
                results.append(output)
        
        elif "for" in statement:
            # Handle for loop
            loop_content = re.findall(r'for\s+(\w+)\s+in\s+range\((.*?)\):\s*(.*)', statement)
            if loop_content:
                var, range_values, body = loop_content[0]
                start, end = [int(x) for x in range_values.split(",")]
                loop_output = []
                for i in range(start, end):
                    loop_output.append(parse_nex(body.replace(var, str(i)), user_input))
                results.append(" ".join(loop_output))
        
        elif "while" in statement:
            # Handle while loop
            loop_content = re.findall(r'while\s+(.*):\s*(.*)', statement)
            if loop_content:
                condition, body = loop_content[0]
                loop_output = []
                while eval(condition):
                    loop_output.append(parse_nex(body, user_input))
                results.append(" ".join(loop_output))
        
        else:
            # If the statement is just a regular expression or text
            results.append(f"Error: Invalid content - {statement}")

    return "\n".join(results)

class CodeExecutionThread(QThread):
    """Thread for executing code in the background to keep UI responsive."""
    result_ready = pyqtSignal(str)

    def __init__(self, code, user_input):
        super().__init__()
        self.code = code
        self.user_input = user_input

    def run(self):
        """Run code execution in a separate thread."""
        try:
            time.sleep(1)  # Simulate processing time
            result = parse_nex(self.code, self.user_input)
            self.result_ready.emit(result)
        except Exception as e:
            self.result_ready.emit(f"Error: {str(e)}")

class HelpDialog(QDialog):
    """Dialog to show help information about the application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(150, 150, 500, 300)

        # Create layout
        layout = QVBoxLayout()
        
        # Help content
        help_text = (
        """    Nex Help:

1. Write your code in the text area (e.g., for loops, while loops, accu for print statements).

2. The 'accu()' function works as a print statement. Example: accu('Hello World')

3. You can use for loops like:
   for i in range(0, 5):
       accu('Iteration: ' + str(i))

4. You can use while loops like:
   while i < 5:
       accu('Iteration: ' + str(i))

5. Use 'ullitu()' for dynamic input prompts. Example: ullitu('Enter a number')

6. You can load/save your code with the 'File' menu.

7. For more information, please refer to the documentation.

8. Use 'if' statements for conditional logic. Example:
   if i < 5:
       accu('i is less than 5')

9. To create functions, use the syntax:
   def function_name(parameters):
       # function body

10. You can call a function like this:
    function_name(arguments)

11. To use variables, simply assign them with '=':
    x = 5

 """

        )
        
        # Text display widget for help content
        help_label = QLabel(help_text, self)
        layout.addWidget(help_label)

        # OK button to close the help dialog
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)

class CompilerGUI(QMainWindow):  
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Apply black theme stylesheet
        self.setStyleSheet(black_stylesheet)

        # Create layout
        layout = QVBoxLayout()

        # Create input area for user to input code
        self.code_input = QTextEdit(self)
        self.code_input.setPlaceholderText("")  # Remove the placeholder text
        self.code_input.setStyleSheet("QTextEdit {border: none; padding: 10px;}")  # Remove box inside text area
        layout.addWidget(self.code_input)

        # Create input for the user to enter dynamic values
        self.user_input_label = QLabel("Enter a number or text:", self)
        layout.addWidget(self.user_input_label)
        
        self.user_input_field = QLineEdit(self)
        self.user_input_field.setPlaceholderText("")  # Remove the placeholder text
        layout.addWidget(self.user_input_field)

        # Create run button
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

        # Create a tab widget for output
        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)

        # Set central widget for layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add Menu Bar
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        close_action = QAction('Close', self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        help_menu = menubar.addMenu('Help')
        help_action = QAction('Help', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        # Set window properties
        self.setWindowTitle('Nex')
        self.setGeometry(100, 100, 600, 400)
        self.show()

    def run_code(self):
        code = self.code_input.toPlainText()  # Get code from input field
        user_input_value = self.user_input_field.text()  # Get user input value
        
        # Disable input and button to prevent re-triggering during execution
        self.code_input.setDisabled(True)
        self.user_input_field.setDisabled(True)
        self.run_button.setDisabled(True)

        # Start code execution in a background thread
        self.execution_thread = CodeExecutionThread(code, user_input_value)
        self.execution_thread.result_ready.connect(self.display_result)
        self.execution_thread.start()

    def display_result(self, result):
        """Display the result in a new tab with a cancel button to close it."""
        new_tab = QWidget()
        layout = QVBoxLayout()

        # Create a horizontal layout to add the close button and output area
        close_layout = QHBoxLayout()
        close_button = QPushButton("Close Tab", self)
        close_button.clicked.connect(self.close_tab)
        close_layout.addWidget(close_button)

        output_area = QTextEdit()
        output_area.setPlainText(result)
        output_area.setReadOnly(True)
        output_area.setStyleSheet("""
            QTextEdit {
                background-color: #121212;
                color: #A9D0D1;
                border: 1px solid #333333;
                border-radius: 8px;
                padding: 10px;
                font-family: "Courier New", Courier, monospace;
                font-size: 14px;
            }
        """)
        close_layout.addWidget(output_area)
        
        layout.addLayout(close_layout)
        new_tab.setLayout(layout)

        # Add the new tab
        tab_name = "Output " + str(self.tab_widget.count() + 1)
        self.tab_widget.addTab(new_tab, tab_name)
        
        # Re-enable inputs and button
        self.code_input.setEnabled(True)
        self.user_input_field.setEnabled(True)
        self.run_button.setEnabled(True)

    def close_tab(self):
        """Close the currently selected tab."""
        current_index = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(current_index)

    def open_file(self):
        """Open a file dialog to select a file and load the content."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                code = file.read()
                self.code_input.setPlainText(code)

    def save_file(self):
        """Save the content of the text area to a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                code = self.code_input.toPlainText()
                file.write(code)

    def show_help(self):
        """Show help dialog with detailed information."""
        help_dialog = HelpDialog()
        help_dialog.exec_()
        

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CompilerGUI()
    sys.exit(app.exec_())
