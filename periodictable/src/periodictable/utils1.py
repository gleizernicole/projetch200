from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QGridLayout, QMessageBox, QHBoxLayout, QFrame, QInputDialog, QApplication)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import sys, random, unicodedata
import pandas as pd

# Load and process CSV data
def load_periodic_table_data():
    # Read CSV with proper configuration
    df = pd.read_csv(
        'CH-200 projet prog(Feuil1).csv',
        sep=';',
        decimal=',',
        skipinitialspace=True,
        na_values=['', ' ']
    )
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Clean data
    df = df.dropna(subset=['symbole', 'position']).copy()
    
    # Process position column
    df[['row', 'col']] = df['position'].str.extract(r'\((\d+),\s*(\d+)\)').astype(float).astype('Int64')
    
    # Convert numeric columns
    df['num'] = pd.to_numeric(df['num'], errors='coerce')
    df['masse'] = pd.to_numeric(df['masse'].str.replace(',', '.'), errors='coerce')
    
    # Create elements dictionary
    elements = {}
    for _, row in df.iterrows():
        elements[row['symbole']] = {
            'nom': row['nom'],
            'num': row['num'],
            'masse': row['masse'],
            'famille': row['famille']
        }
    
    # Create positions dictionary
    positions = {row['symbole']: (row['row'], row['col']) for _, row in df.iterrows()}
    
    return elements, positions

# Load data from CSV
elements, positions = load_periodic_table_data()

# Define colors for families (adjusted to match CSV family names)
colors = {
    "Diatomic nonmetal": "#FFFF00",
    "Alkali metal": "#FFAAAA",
    "Alkaline Earth Metal": "#FF5555",
    "Transition Metal": "#F5F5DC",
    "Post-Transition Metal": "#FFA500",
    "Metalloid": "#FF80FF",
    "Polyatomic Nonmetal": "#A52A2A",
    "Noble Gas": "#00FF00",
    "Lanthanide": "#00CCFF",        # Note: Add corresponding entry in CSV if needed
    "Actinide": "#CCCCCC"           # Note: Add corresponding entry in CSV if needed
}

class PeriodicTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Periodic Table + Quiz 🎲")
        self.setGeometry(100, 100, 1400, 800)

        self.score = 0
        self.question_count = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.reponse_attendue = None
        self.time_remaining = 30

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout()
        central_widget.setLayout(layout_principal)

        # Title
        title_label = QLabel("🧪 Interactive Periodic Table 🧪")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(title_label)

        # Score and timer
        self.score_label = QLabel("Score: 0")
        self.score_label.setFont(QFont("Arial", 16))
        layout_principal.addWidget(self.score_label)

        self.timer_label = QLabel(f"Time remaining: {self.time_remaining}s")
        self.timer_label.setFont(QFont("Arial", 16))
        layout_principal.addWidget(self.timer_label)

        # Quiz button
        quiz_btn = QPushButton("🎲 Start Quiz")
        quiz_btn.setFixedHeight(40)
        quiz_btn.clicked.connect(self.start_quiz)
        layout_principal.addWidget(quiz_btn)

        # Grid layout for elements
        grid = QGridLayout()
        layout_principal.addLayout(grid)
        
        # Create buttons for each element
        for symb, pos in positions.items():
            btn = QPushButton(symb)
            btn.setFixedSize(80, 80)
            family = elements[symb]['famille']
            btn.setStyleSheet(f"background-color: {colors.get(family, '#FFFFFF')}; border: 1px solid #333;")
            btn.clicked.connect(lambda _, s=symb: self.show_element_info(s))
            grid.addWidget(btn, pos[0], pos[1])

        # Legend
        legend_layout = QHBoxLayout()
        for family, color in colors.items():
            color_box = QFrame()
            color_box.setFixedSize(20, 20)
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            
            family_layout = QHBoxLayout()
            family_layout.addWidget(color_box)
            family_layout.addWidget(QLabel(family))
            
            container = QWidget()
            container.setLayout(family_layout)
            legend_layout.addWidget(container)
        
        layout_principal.addLayout(legend_layout)

    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.setText(f"Time remaining: {self.time_remaining}s")
        if self.time_remaining <= 0:
            self.timer.stop()
            self.timeout()

    def show_element_info(self, symbol):
        element = elements[symbol]
        info = (
            f"<b>Name:</b> {element['nom']}<br>"
            f"<b>Symbol:</b> {symbol}<br>"
            f"<b>Atomic number:</b> {element['num']}<br>"
            f"<b>Atomic mass:</b> {element['masse']:.4f}<br>"
            f"<b>Family:</b> {element['famille']}"
        )
        QMessageBox.information(self, f"Information about {symbol}", info)

    def normalize_text(self, text):
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode()
        return text.lower().replace(" ", "").replace("-", "").replace("'", "")

    def start_quiz(self):
        self.score = 0
        self.question_count = 0
        self.score_label.setText(f"Score: {self.score}")
        self.next_question()

    def next_question(self):
        if self.question_count >= 10:
            QMessageBox.information(self, "Quiz Complete!", f"Final Score: {self.score}/10")
            return

        symbol = random.choice(list(elements.keys()))
        element = elements[symbol]
        question_type = random.choice(["symbol", "number"])

        if question_type == "symbol":
            question = f"What element has the symbol <b>{symbol}</b>?"
        else:
            question = f"What element has atomic number <b>{element['num']}</b>?"

        self.reponse_attendue = element['nom']
        self.time_remaining = 30
        self.timer.start()

        answer, ok = QInputDialog.getText(self, "Quiz (30s)", question)
        self.timer.stop()

        if ok:
            if self.normalize_text(answer) == self.normalize_text(self.reponse_attendue):
                self.score += 1
                QMessageBox.information(self, "Correct!", "✔️ Well done!")
            else:
                QMessageBox.warning(self, "Incorrect", f"❌ Correct answer: {self.reponse_attendue}")

        self.score_label.setText(f"Score: {self.score}")
        self.question_count += 1
        self.next_question()

    def timeout(self):
        QMessageBox.warning(self, "Timeout!", f"Time's up! Correct answer was: {self.reponse_attendue}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PeriodicTable()
    window.show()
    sys.exit(app.exec_())
