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
    QDialogButtonBox
)
from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtGui import QFont, QPixmap

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from periodictable.elements_data import elements, positions, colors, production_methods

# ======================================================================================
# MAIN APPLICATION CLASS
# ======================================================================================

class PeriodicTableApp(QMainWindow):
    def __init__(self):
        """Initialize the main application window and UI components"""
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

    def init_ui(self):
        """Set up all user interface components"""
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
        """Initialize and configure the quiz timer"""
        self.quiz_timer = QTimer()
        self.quiz_timer.setInterval(1000)
        self.quiz_timer.timeout.connect(self.update_timer)

    def init_periodic_table_grid(self, parent_layout):
        """Create the scrollable periodic table grid"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Enable horizontal scrollbar to allow scrolling when table is wider than the window
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        grid_container = QWidget()
        self.element_grid = QGridLayout(grid_container)

        # Reduce spacing and margins to minimum
        self.element_grid.setSpacing(0)
        self.element_grid.setContentsMargins(0, 0, 0, 0)

        # Create element buttons
        for symbol, (row, col) in positions.items():
            self.create_element_button(symbol, row, col)

        scroll_area.setWidget(grid_container)
        parent_layout.addWidget(scroll_area)

    def create_element_button(self, symbol, row, col):
        """Create an individual element button for the periodic table"""
        element = elements[symbol]
        btn = QPushButton(symbol)
        # Reduce button size to make table more compact
        btn.setFixedSize(40, 40)  # Reduced from 50,50 to 40,40
        btn.setStyleSheet(f"""
            background-color: {colors[element["famille"]]};
            border: 1px solid #333;
            font-weight: bold;
            font-size: 10px;  /* Reduced from 12px to 10px */
            margin: 0;
            padding: 0;
        """)
        btn.clicked.connect(lambda _, sym=symbol: self.show_element_info(sym))
        self.element_grid.addWidget(btn, row, col)

    def create_legend(self, parent_layout):
        """Create the element family color legend"""
        legend = QHBoxLayout()
        legend.setSpacing(2)  # Reduce spacing between legend items

        for family, color in colors.items():
            legend_item = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(1, 1, 1, 1)  # Minimal margins

            # Color indicator
            color_box = QFrame()
            color_box.setFixedSize(12, 12)  # Smaller color box
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

            # Family name label with smaller font
            label = QLabel(family)
            label.setContentsMargins(2, 0, 2, 0)  # Minimal margins
            label.setFont(QFont("Arial", 8))  # Smaller font

            item_layout.addWidget(color_box)
            item_layout.addWidget(label)
            legend_item.setLayout(item_layout)
            legend.addWidget(legend_item)

        parent_layout.addLayout(legend)

    # ==================================================================================
    # QUIZ FUNCTIONALITY
    # ==================================================================================

    def update_timer(self):
        """Update the quiz timer and handle timeout"""
        self.time_remaining -= 1
        self.timer_display.setText(f"Time remaining: {self.time_remaining}s")
        if self.time_remaining <= 0:
            self.quiz_timer.stop()
            self.handle_timeout()

    def start_quiz(self):
        """Initialize and start a new quiz session"""
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
        """Present a new quiz question to the user"""
        if not self.quiz_active or self.question_count >= 10:
            if self.quiz_active:
                QMessageBox.information(self, "Quiz Complete! 🎉",
                                      f"Final Score: {self.score}/10")
            self.quiz_active = False
            return

        self.user_answer = None

        # Filter elements using English family names
        allowed_symbols = [
            sym for sym in elements
            if elements[sym]["famille"] not in ['Transition Metal', 'Lanthanide', 'Actinide']
        ]
        symbol = random.choice(allowed_symbols)
        element = elements[symbol]

        question_type = random.choice(["symbol", "atomic_number","electron_config", "electron_config_reverse","production", "production_reverse"])


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
                return self.ask_question()  # Skip if not defined

        elif question_type == "production":
            methods = production_methods.get(symbol, [])
            if methods:
                method = random.choice(methods) if isinstance(methods, list) else list(methods.values())[0]
                question = f"Which element is produced by the following method?<br><b>{method}</b>"
                self.current_answer = element["nom"]
            else:
                return self.ask_question()  # Skip if no method
            
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

        if question_type in ["symbol", "atomic_number", "electron_config", "production"]:
            self.current_answer = element["nom"]
        self.time_remaining = 30
        self.quiz_timer.start()

        quiz_dialog = QDialog(self)
        quiz_dialog.setWindowTitle("Element Quiz 🎲 (30s)")
        quiz_dialog.setMinimumSize(400, 200)
        dialog_layout = QVBoxLayout(quiz_dialog)

        question_label = QLabel(question)
        question_label.setStyleSheet("font-size: 16px; color: black; padding: 10px;")
        question_label.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(question_label)

        # Answer Section
        if self.quiz_type == "Multiple Choice":
            options = [self.current_answer]
            seen = set(options)
            attempts = 0
            max_attempts = 100

            while len(options) < 4 and attempts < max_attempts:
                attempts += 1
                other_symbol = random.choice(allowed_symbols)
                other_element = elements[other_symbol]

            # Choix selon le type de question
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

                # Ajout uniquement si valide et pas déjà présent
                if candidate and candidate not in seen:
                    options.append(candidate)
                    seen.add(candidate)

            # Complément de sécurité
            while len(options) < 4:
                options.append("N/A")  # ou un dummy pour éviter crash


            random.shuffle(options)


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
            self.answer_input = QLineEdit()
            self.answer_input.setStyleSheet("font-size: 14px; margin: 10px;")
            dialog_layout.addWidget(self.answer_input)

        # Control Buttons
        control_layout = QHBoxLayout()

        exit_btn = QPushButton("Exit Quiz")
        exit_btn.setStyleSheet(
            "QPushButton { padding: 8px 16px; margin: 5px; "
            "background-color: #f44336; color: white; }"
            "QPushButton:hover { background-color: #d32f2f; }"
        )
        exit_btn.clicked.connect(lambda: quiz_dialog.done(2))

        new_btn = QPushButton("New Question")
        new_btn.setStyleSheet(
            "QPushButton { padding: 8px 16px; margin: 5px; "
            "background-color: #2196F3; color: white; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        new_btn.clicked.connect(quiz_dialog.reject)

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

        # Show dialog
        self.current_dialog = quiz_dialog
        event_loop = QEventLoop()
        quiz_dialog.finished.connect(event_loop.quit)
        quiz_dialog.show()
        event_loop.exec_()

        # Process results
        self.quiz_timer.stop()
        result = quiz_dialog.result()

        if result == QDialog.Accepted:
            answer = (self.user_answer if self.quiz_type == "Multiple Choice"
                     else self.answer_input.text())
            if answer:
                self.check_answer(answer)
                self.question_count += 1
            self.ask_question()
        elif result == 2:
            self.quiz_active = False
            QMessageBox.information(self, "Quiz Abandoned", f"Current Score: {self.score}/10")
        else:
            self.question_count += 1
            self.ask_question()

    def mc_answer_selected(self, answer, dialog):
        """Handle multiple choice selection"""
        self.user_answer = answer
        dialog.accept()

    def check_answer(self, answer):
        """Validate user's answer and update score"""
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
        """Normalize text for answer comparison"""
        return ''.join(c for c in unicodedata.normalize('NFD', text)
                     if unicodedata.category(c) != 'Mn').lower().replace(" ", "")

    def handle_timeout(self):
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

    def add_production_info(self, layout, symbol):
        """Add production equations section to element info dialog"""
        section_header = QLabel("<b>Production Methods:</b>")
        section_header.setStyleSheet("font-size: 14px; padding-top: 15px;")
        layout.addWidget(section_header)

        content = self.get_production_content(symbol)
        content_label = QLabel(content)
        content_label.setStyleSheet("font-size: 12px; color: #444; margin-left: 10px;")
        content_label.setWordWrap(True)
        layout.addWidget(content_label)

    def get_production_content(self, symbol):
        """Generate formatted production methods content"""
        element = elements.get(symbol)
        if element and "production" in element:
            production = element["production"]
            content = []
            for key, value in production.items():
                if isinstance(value, list):
                    content.append(f"<b>{key.replace('_', ' ').capitalize()}:</b>")
                    content.extend(f"• {item}" for item in value)
                elif isinstance(value, dict):
                    content.append(f"<b>{key.replace('_', ' ').capitalize()}:</b>")
                    content.append(f"  Reaction: {value.get('reaction', 'N/A')}")
                    content.append(f"  Conditions: {value.get('conditions', 'N/A')}")
                else:
                    content.append(f"<b>{key.replace('_', ' ').capitalize()}:</b> {value}")
            return "<br>".join(content)
        return "<i>No production methods recorded</i>"

    def show_element_info(self, symbol):
        """Display detailed information about a selected element"""
        element = elements[symbol]
        info_dialog = QDialog(self)
        info_dialog.setWindowTitle(f"Atomic Structure - {element['nom']}")
        info_dialog.setFixedSize(600, 700)
        layout = QVBoxLayout(info_dialog)

        # Atomic structure image
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
            img_label.setText(f"<i>Atomic structure for {symbol} not available</i>")
            img_label.setStyleSheet("color: #666; font-size: 14px;")

        img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(img_label)

        # Element properties
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

        # Add production info if available
        if "production" in element:
            self.add_production_info(layout, symbol)

        info_dialog.exec_()

    def update_score_display(self):
        """Update the score display label"""
        self.score_display.setText(f"Score: {self.score}")

# ======================================================================================
# APPLICATION ENTRY POINT
# ======================================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PeriodicTableApp()
    window.show()
    sys.exit(app.exec_())
