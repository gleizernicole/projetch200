"""
Interactive Periodic Table Application with Quiz Features
Features:
- Complete periodic table visualization
- Element information display with atomic structure images
- Timed quiz game with multiple question types
- Score tracking and time management
"""

import sys
import os
import random
import unicodedata
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox,
    QHBoxLayout, QFrame, QInputDialog, QApplication, QScrollArea, QDialog, QLineEdit,
    QDialogButtonBox, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtGui import QFont, QPixmap

try:
    # First try relative import (when run as module)
    from .elements_data import elements, positions, colors, production_methods
except ImportError:
    # Fallback for direct execution - add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from elements_data import elements, positions, colors, production_methods

# ======================================================================================
# MAIN APPLICATION CLASS
# ======================================================================================

class PeriodicTableApp(QMainWindow):
    """
    Main application class for the Interactive Periodic Table with Quiz functionality.
    
    This class creates a PyQt5 application that displays an interactive periodic table
    where users can click on elements to view detailed information, and participate
    in timed quiz games with various question types.
    
    Attributes:
        score (int): Current quiz score
        question_count (int): Number of questions answered in current quiz
        quiz_active (bool): Whether a quiz is currently running
        current_answer (str): Correct answer for current quiz question
        time_remaining (int): Seconds remaining for current question
        quiz_type (str): Type of quiz ("Multiple Choice" or "Free Response")
        user_answer (str): User's selected answer in multiple choice
        current_dialog (QDialog): Reference to currently open dialog
    """
    
    def __init__(self):
        """
        Initialize the main application window and UI components.
        
        Sets up the main window properties, initializes quiz state variables,
        creates the user interface, timer, and displays the welcome dialog.
        
        Args:
            None
            
        Returns:
            None
        """
        super().__init__()
        self.setWindowTitle("Interactive Periodic Table + Quiz 🎲")
        self.setGeometry(100, 100, 600, 500)

        # Quiz game state variables
        self.score = 0
        self.question_count = 0
        self.quiz_active = False
        self.current_answer = None
        self.time_remaining = 30

        # Initialize UI components
        self.init_ui()
        self.init_timer()

        self.quiz_type = None
        self.user_answer = None
        self.current_dialog = None

        # Show initial information dialog
        self.show_initial_info()

    def show_initial_info(self):
        """
        Display an initial information dialog about the application features.
        
        Creates and shows a modal dialog with comprehensive information about
        the periodic table features, element information display, and quiz
        game functionality. Uses HTML formatting for better presentation.
        
        Args:
            None
            
        Returns:
            None
        """
        info_dialog = QDialog(self)
        info_dialog.setWindowTitle("Welcome to the Interactive Periodic Table!")
        info_dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout(info_dialog)

        # Title
        title = QLabel("🧪 Interactive Periodic Table + Quiz 🎲")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Scrollable info text
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml("""
        <h2>Application Features</h2>
        <h3>Periodic Table</h3>
        <p>• Click on any element button to view detailed information</p>
        <p>• The periodic table is color-coded by element families</p>
        
        <h3>Element Information Includes:</h3>
        <ul>
            <li>Atomic structure image</li>
            <li>Element name and symbol</li>
            <li>Atomic number</li>
            <li>Atomic weight</li>
            <li>Element family</li>
            <li>Physical state</li>
            <li>Electron configuration</li>
            <li>Isotopes</li>
            <li>Production methods</li>
        </ul>

        <h3>Quiz Game Features</h3>
        <p>• Press "Start Quiz" to begin</p>
        <p>• Choose between Multiple Choice or Free Response formats</p>
        <p>• 10 questions per quiz session</p>
        <p>• 30 seconds per question</p>

        <h3>Quiz Question Types:</h3>
        <ul>
            <li>Identify element by symbol</li>
            <li>Identify element by atomic number</li>
            <li>Match electron configuration</li>
            <li>Identify element by production method</li>
        </ul>""")
        info_text.setStyleSheet("""
            background-color: #FF7F50;
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 14px;
        """)
        layout.addWidget(info_text)

        # OK Button
        ok_btn = QPushButton("Got it! Let's Explore 🚀")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C63FF;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        ok_btn.clicked.connect(info_dialog.accept)
        layout.addWidget(ok_btn)

        info_dialog.exec_()

    def init_ui(self):
        """
        Set up all user interface components for the main window.
        
        Creates the central widget and main layout, adds the application title,
        score display, timer display, quiz control button, periodic table grid,
        and element family legend. Configures fonts and alignments.
        
        Args:
            None
            
        Returns:
            None
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Application title
        title = QLabel("🧪 Periodic Table of Elements 🧪")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Score display
        self.score_display = QLabel("Score: 0")
        self.score_display.setAlignment(Qt.AlignCenter)
        self.score_display.setFont(QFont("Arial", 16))
        main_layout.addWidget(self.score_display)

        # Timer display
        self.timer_display = QLabel(f"Time remaining: {self.time_remaining}s")
        self.timer_display.setAlignment(Qt.AlignCenter)
        self.timer_display.setFont(QFont("Arial", 16))
        main_layout.addWidget(self.timer_display)

        # Quiz control button
        self.quiz_btn = QPushButton("🎲 Start Quiz")
        self.quiz_btn.setFixedHeight(50)
        self.quiz_btn.clicked.connect(self.start_quiz)
        main_layout.addWidget(self.quiz_btn)

        # Periodic table grid
        self.init_periodic_table_grid(main_layout)

        # Element family legend
        self.create_legend(main_layout)

    def init_timer(self):
        """
        Initialize and configure the quiz timer.
        
        Creates a QTimer object with 1-second intervals and connects it to
        the update_timer method for countdown functionality during quiz questions.
        
        Args:
            None
            
        Returns:
            None
        """
        self.quiz_timer = QTimer()
        self.quiz_timer.setInterval(1000)  # 1 second intervals
        self.quiz_timer.timeout.connect(self.update_timer)

    def init_periodic_table_grid(self, parent_layout):
        """
        Create the scrollable periodic table grid with element buttons.
        
        Sets up a scroll area containing a grid layout with element buttons
        positioned according to their standard periodic table locations.
        Configures scrolling behavior and minimal spacing for compact display.
        
        Args:
            parent_layout (QVBoxLayout): The parent layout to add the grid to
            
        Returns:
            None
        """
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Enable horizontal scrollbar to allow scrolling when table is wider than the window
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        grid_container = QWidget()
        self.element_grid = QGridLayout(grid_container)

        # Reduce spacing and margins to minimum for compact display
        self.element_grid.setSpacing(0)
        self.element_grid.setContentsMargins(0, 0, 0, 0)

        # Create element buttons using position data
        for symbol, (row, col) in positions.items():
            self.create_element_button(symbol, row, col)

        scroll_area.setWidget(grid_container)
        parent_layout.addWidget(scroll_area)

    def create_element_button(self, symbol, row, col):
        """
        Create an individual element button for the periodic table.
        
        Creates a QPushButton for a specific element with appropriate styling
        based on the element's family color. Connects the button to show
        element information when clicked.
        
        Args:
            symbol (str): The chemical symbol of the element (e.g., "H", "He")
            row (int): Grid row position for the element
            col (int): Grid column position for the element
            
        Returns:
            None
        """
        element = elements[symbol]
        btn = QPushButton(symbol)
        # Reduce button size to make table more compact
        btn.setFixedSize(40, 40)  # Compact size for better table display
        btn.setStyleSheet(f"""
            background-color: {colors[element["famille"]]};
            border: 1px solid #333;
            font-weight: bold;
            font-size: 10px;
            margin: 0;
            padding: 0;
        """)
        btn.clicked.connect(lambda _, sym=symbol: self.show_element_info(sym))
        self.element_grid.addWidget(btn, row, col)

    def create_legend(self, parent_layout):
        """
        Create the element family color legend below the periodic table.
        
        Generates a horizontal layout with color-coded indicators and labels
        for each element family, helping users understand the color coding
        used in the periodic table display.
        
        Args:
            parent_layout (QVBoxLayout): The parent layout to add the legend to
            
        Returns:
            None
        """
        legend = QHBoxLayout()
        legend.setSpacing(2)  # Minimal spacing between legend items

        for family, color in colors.items():
            legend_item = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(1, 1, 1, 1)  # Minimal margins

            # Color indicator square
            color_box = QFrame()
            color_box.setFixedSize(12, 12)
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

            # Family name label
            label = QLabel(family)
            label.setContentsMargins(2, 0, 2, 0)
            label.setFont(QFont("Arial", 8))  # Small font for compact display

            item_layout.addWidget(color_box)
            item_layout.addWidget(label)
            legend_item.setLayout(item_layout)
            legend.addWidget(legend_item)

        parent_layout.addLayout(legend)

    # ==================================================================================
    # QUIZ FUNCTIONALITY
    # ==================================================================================

    def update_timer(self):
        """
        Update the quiz timer display and handle timeout conditions.
        
        Decrements the time remaining by 1 second, updates the timer display,
        and triggers timeout handling when time reaches zero. Called every
        second by the QTimer during quiz questions.
        
        Args:
            None
            
        Returns:
            None
        """
        self.time_remaining -= 1
        self.timer_display.setText(f"Time remaining: {self.time_remaining}s")
        if self.time_remaining <= 0:
            self.quiz_timer.stop()
            self.handle_timeout()

    def start_quiz(self):
        """
        Initialize and start a new quiz session.
        
        Prompts the user to choose between Multiple Choice or Free Response
        quiz format, then resets quiz state variables and begins the first
        question. Handles user cancellation gracefully.
        
        Args:
            None
            
        Returns:
            None (returns early if user cancels format selection)
        """
        quiz_type, ok = QInputDialog.getItem(
            self, "Quiz Format", "Choose quiz format:",
            ["Multiple Choice", "Free Response"], 0, False
        )
        if not ok:
            return

        self.quiz_type = quiz_type
        self.score = 0
        self.question_count = 0
        self.quiz_active = True
        self.update_score_display()
        self.time_remaining = 30
        self.ask_question()

    def ask_question(self):
        """
        Present a new quiz question to the user.
        
        Generates a random question from available question types, creates
        the appropriate dialog interface (multiple choice or free response),
        starts the timer, and handles user interactions. Manages quiz
        completion and question progression.
        
        Args:
            None
            
        Returns:
            None (returns early if quiz is complete or inactive)
        """
        if not self.quiz_active or self.question_count >= 10:
            if self.quiz_active:
                QMessageBox.information(self, "Quiz Complete! 🎉",
                                      f"Final Score: {self.score}/10")
            self.quiz_active = False
            return

        self.user_answer = None

        # Filter elements excluding complex transition metals and rare earths
        allowed_symbols = [
            sym for sym in elements
            if elements[sym]["famille"] not in ['Transition Metal', 'Lanthanide', 'Actinide']
        ]
        symbol = random.choice(allowed_symbols)
        element = elements[symbol]

        # Random question type selection
        question_type = random.choice(["symbol", "atomic_number","electron_config", "electron_config_reverse","production", "production_reverse"])

        # Generate question based on type
        if question_type == "symbol":
            question = f"What is the name of the element with symbol <b>{symbol}</b>?"
            self.current_answer = element["nom"]

        elif question_type == "atomic_number":
            question = f"What is the name of the element with atomic number <b>{element['num']}</b>?"
            self.current_answer = element["nom"]

        elif question_type == "electron_config":
            if "electron_config" in element:
                question = f"Which element has the electron configuration <b>{element['electron_config']}</b>?"
                self.current_answer = element["nom"]
            else:
                return self.ask_question()  # Skip if electron config not defined

        elif question_type == "production":
            methods = production_methods.get(symbol, [])
            if methods:
                method = random.choice(methods) if isinstance(methods, list) else list(methods.values())[0]
                question = f"Which element is produced by the following method?<br><b>{method}</b>"
                self.current_answer = element["nom"]
            else:
                return self.ask_question()  # Skip if no production method available
            
        elif question_type == "electron_config_reverse":
            if "electron_config" in element:
                question = f"What is the electron configuration of <b>{element['nom']}</b>?"
                self.current_answer = element["electron_config"]
            else:
                return self.ask_question()

        elif question_type == "production_reverse":
            methods = production_methods.get(symbol, [])
            if methods:
                method = random.choice(methods) if isinstance(methods, list) else list(methods.values())[0]
                question = f"Which production method corresponds to <b>{element['nom']}</b>?"
                self.current_answer = method
            else:
                return self.ask_question()

        # Set correct answer for name-based questions
        if question_type in ["symbol", "atomic_number", "electron_config", "production"]:
            self.current_answer = element["nom"]
            
        # Reset timer and start countdown
        self.time_remaining = 30
        self.quiz_timer.start()

        # Create question dialog
        quiz_dialog = QDialog(self)
        quiz_dialog.setWindowTitle("Element Quiz 🎲 (30s)")
        quiz_dialog.setMinimumSize(400, 200)
        dialog_layout = QVBoxLayout(quiz_dialog)

        # Question display
        question_label = QLabel(question)
        question_label.setStyleSheet("font-size: 16px; color: black; padding: 10px;")
        question_label.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(question_label)

        # Answer section - Multiple Choice or Free Response
        if self.quiz_type == "Multiple Choice":
            # Generate multiple choice options
            options = [self.current_answer]
            seen = set(options)
            attempts = 0
            max_attempts = 100

            # Generate 3 additional incorrect options
            while len(options) < 4 and attempts < max_attempts:
                attempts += 1
                other_symbol = random.choice(allowed_symbols)
                other_element = elements[other_symbol]

                # Generate candidate answer based on question type
                if question_type in ["symbol", "atomic_number", "electron_config", "production"]:
                    candidate = other_element["nom"]

                elif question_type == "electron_config_reverse":
                    candidate = other_element.get("electron_config", None)

                elif question_type == "production_reverse":
                    methods = production_methods.get(other_symbol)
                    if isinstance(methods, list) and methods:
                        candidate = random.choice(methods)
                    elif isinstance(methods, dict) and methods:
                        candidate = list(methods.values())[0]
                    else:
                        candidate = None
                else:
                    candidate = None

                # Add unique valid candidates
                if candidate and candidate not in seen:
                    options.append(candidate)
                    seen.add(candidate)

            # Fill remaining slots if needed
            while len(options) < 4:
                options.append("N/A")

            random.shuffle(options)

            # Create option buttons
            for option in options:
                btn = QPushButton(option)
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 10px;
                        margin: 5px;
                        background-color: #CF9FFF;
                        border: 1px solid #ccc;
                    }
                    QPushButton:hover {
                        background-color: #7F00FF;
                    }
                """)
                btn.clicked.connect(lambda _, opt=option: self.mc_answer_selected(opt, quiz_dialog))
                dialog_layout.addWidget(btn)
        else:
            # Free response input field
            self.answer_input = QLineEdit()
            self.answer_input.setStyleSheet("font-size: 14px; margin: 10px;")
            dialog_layout.addWidget(self.answer_input)

        # Control buttons layout
        control_layout = QHBoxLayout()

        # Exit quiz button
        exit_btn = QPushButton("Exit Quiz")
        exit_btn.setStyleSheet(
            "QPushButton { padding: 8px 16px; margin: 5px; "
            "background-color: #f44336; color: white; }"
            "QPushButton:hover { background-color: #d32f2f; }"
        )
        exit_btn.clicked.connect(lambda: quiz_dialog.done(2))

        # New question button
        new_btn = QPushButton("New Question")
        new_btn.setStyleSheet(
            "QPushButton { padding: 8px 16px; margin: 5px; "
            "background-color: #2196F3; color: white; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        new_btn.clicked.connect(quiz_dialog.reject)

        # Submit button for free response
        if self.quiz_type != "Multiple Choice":
            submit_btn = QPushButton("Submit")
            submit_btn.setStyleSheet(
                "QPushButton { padding: 8px 24px; margin: 5px; "
                "background-color: #4CAF50; color: white; }"
                "QPushButton:hover { background-color: #388E3C; }"
            )
            submit_btn.clicked.connect(quiz_dialog.accept)
            control_layout.addWidget(submit_btn)

        control_layout.addWidget(exit_btn)
        control_layout.addWidget(new_btn)
        control_layout.addStretch()
        dialog_layout.addLayout(control_layout)

        # Display dialog and handle events
        self.current_dialog = quiz_dialog
        event_loop = QEventLoop()
        quiz_dialog.finished.connect(event_loop.quit)
        quiz_dialog.show()
        event_loop.exec_()

        # Process dialog results
        self.quiz_timer.stop()
        result = quiz_dialog.result()

        if result == QDialog.Accepted:
            # User submitted an answer
            answer = (self.user_answer if self.quiz_type == "Multiple Choice"
                     else self.answer_input.text())
            if answer:
                self.check_answer(answer)
                self.question_count += 1
            self.ask_question()
        elif result == 2:
            # User exited quiz
            self.quiz_active = False
            QMessageBox.information(self, "Quiz Abandoned", f"Current Score: {self.score}/10")
        else:
            # User requested new question (skip current)
            self.question_count += 1
            self.ask_question()

    def mc_answer_selected(self, answer, dialog):
        """
        Handle multiple choice answer selection.
        
        Called when user clicks on a multiple choice option button.
        Stores the selected answer and closes the dialog to proceed
        with answer checking.
        
        Args:
            answer (str): The selected answer text
            dialog (QDialog): The quiz dialog to close
            
        Returns:
            None
        """
        self.user_answer = answer
        dialog.accept()

    def check_answer(self, answer):
        """
        Validate user's answer against the correct answer and update score.
        
        Normalizes both the user's answer and correct answer for comparison,
        updates the score if correct, and displays appropriate feedback
        messages with the correct answer information.
        
        Args:
            answer (str): The user's submitted answer
            
        Returns:
            None (returns early if no answer provided)
        """
        if not answer:
            QMessageBox.warning(self, "No Answer", "Please provide an answer!")
            return

        normalized_answer = self.normalize_text(answer)
        normalized_correct = self.normalize_text(self.current_answer)

        if normalized_answer == normalized_correct:
            self.score += 1
            self.update_score_display()
            QMessageBox.information(self, "Correct! 🎉",
                                  f"Correct answer! ✔️\nAnswer was: {self.current_answer}\nCurrent Score: {self.score}/10")
        else:
            QMessageBox.warning(self, "Incorrect 😢",
                              f"Wrong answer! ❌\nCorrect answer: {self.current_answer}")

    def normalize_text(self, text):
        """
        Normalize text for accurate answer comparison.
        
        Removes accents, converts to lowercase, and removes spaces to
        enable flexible answer matching that ignores formatting differences
        and minor spelling variations.
        
        Args:
            text (str): The text to normalize
            
        Returns:
            str: Normalized text with accents removed, lowercase, no spaces
        """
        return ''.join(c for c in unicodedata.normalize('NFD', text)
                     if unicodedata.category(c) != 'Mn').lower().replace(" ", "")

    def handle_timeout(self):
        """
        Handle quiz question timeout when timer reaches zero.
        
        Stops the timer, displays timeout message with correct answer,
        increments question count, closes current dialog, and proceeds
        to the next question automatically.
        
        Args:
            None
            
        Returns:
            None
        """
        self.quiz_timer.stop()
        QMessageBox.warning(self, "⏰ Time's Up!",
                        f"Time expired! Correct answer was: {self.current_answer}")

        self.question_count += 1

        if self.current_dialog:
            self.current_dialog.close()

        self.ask_question()

    # ==================================================================================
    # ELEMENT INFORMATION DISPLAY
    # ==================================================================================

    def get_production_content(self, symbol):
        """
        Generate formatted HTML content for element production methods.
        
        Retrieves production method data for the specified element and
        formats it into readable HTML with proper styling for display
        in the element information dialog.
        
        Args:
            symbol (str): Chemical symbol of the element (e.g., "H", "He")
            
        Returns:
            str: HTML-formatted string containing production method information
                 or message indicating no methods are available
        """
        production_info = production_methods.get(symbol, {})
    
        if not production_info:
            return "<i>No production methods recorded</i>"
    
        content = []
        for method, details in production_info.items():
            # Convert method name to readable format
            formatted_method = method.replace('_', ' ').capitalize()
            
            # Handle different data structure types
            if isinstance(details, list):
                # For list of reactions
                content.append(f"<b>{formatted_method}:</b>")
                content.extend(f"• {item}" for item in details)
            elif isinstance(details, dict):
                # For dictionary with reaction and conditions
                content.append(f"<b>{formatted_method}:</b>")
                content.append(f"  Reaction: {details.get('reaction', 'N/A')}")
                content.append(f"  Conditions: {details.get('conditions', 'N/A')}")
            else:
                # For simple string reactions or methods
                content.append(f"<b>{formatted_method}:</b> {details}")
        
        return "<br>".join(content)
    
    def add_production_info(self, layout, symbol):
        """
        Add production methods section to element information dialog.
        
        Creates and adds widgets displaying production method information
        to the provided layout, including a section header and formatted
        content with proper styling.
        
        Args:
            layout (QVBoxLayout): The layout to add production info widgets to
            symbol (str): Chemical symbol of the element
            
        Returns:
            None
        """
        print(f"Adding production info for {symbol}")  # Debug print
        print(f"Production methods: {production_methods.get(symbol)}")  # Debug print
    
        # Section header
        section_header = QLabel("<b>Production Methods:</b>")
        section_header.setStyleSheet("font-size: 14px; padding-top: 15px;")
        layout.addWidget(section_header)
    
        # Content with formatting
        content = self.get_production_content(symbol)
        print(f"Production content: {content}")  # Debug print
    
        content_label = QLabel(content)
        content_label.setStyleSheet("font-size: 12px; color: black; margin-left: 10px;")
        content_label.setWordWrap(True)
        layout.addWidget(content_label)
    
    def show_element_info(self, symbol):
        """
        Display detailed information dialog for a selected element.
        
        Creates a modal dialog showing comprehensive element information
        including atomic structure image, basic properties, electron
        configuration, isotopes, and production methods. Handles missing
        images gracefully with fallback text.
        
        Args:
            symbol (str): Chemical symbol of the element to display
            
        Returns:
            None
        """
        element = elements[symbol]
        info_dialog = QDialog(self)
        info_dialog.setWindowTitle(f"Atomic Structure - {element['nom']}")
        info_dialog.setFixedSize(600, 700)
        layout = QVBoxLayout(info_dialog)
    
        # Atomic structure image display
        img_label = QLabel()
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(current_dir, "..", "..", "scientific_structures",
                                  f"{symbol}_scientific.png")
    
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                img_label.setPixmap(pixmap.scaled(400, 400,
                                                Qt.KeepAspectRatio,
                                                Qt.SmoothTransformation))
            else:
                raise FileNotFoundError
        except Exception as e:
            # Fallback for missing images
            img_label.setText(f"<i>Atomic structure for {symbol} not available</i>")
            img_label.setStyleSheet("color: #666; font-size: 14px;")
    
        img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(img_label)
    
        # Element properties information
        info_text = QLabel(
            f"<b>{element['nom']} ({symbol})</b><br>"
            f"Atomic Number: {element['num']}<br>"
            f"Atomic Weight: {element['masse']} u<br>"
            f"Family: {element['famille']}<br>"
            f"State: {element['state']}<br>"
            f"Electron Configuration: {element['electron_config']}<br>"
            f"Isotopes: {', '.join(element['isotopes'])}<br><br>"
        )
        info_text.setStyleSheet("font-size: 14px; padding: 15px;")
        layout.addWidget(info_text)
    
        # Add production methods if available
        if production_methods.get(symbol):
            self.add_production_info(layout, symbol)
    
        info_dialog.exec_()

    def update_score_display(self):
        """
        Update the score display label with current quiz score.
        
        Refreshes the score display widget to show the current score
        value. Called whenever the score changes during quiz gameplay.
        
        Args:
            None
            
        Returns:
            None
        """
        self.score_display.setText(f"Score: {self.score}")

# ======================================================================================
# APPLICATION ENTRY POINT
# ======================================================================================

def main():
    """
    Main function to initialize and run the PyQt5 application.
    
    Creates the QApplication instance, initializes the main window,
    displays it, and starts the event loop. Handles application
    shutdown gracefully when the window is closed.
    
    Args:
        None
        
    Returns:
        None
    """
    app = QApplication(sys.argv)
    window = PeriodicTableApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
