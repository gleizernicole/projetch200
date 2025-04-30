from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QGridLayout, QMessageBox, QHBoxLayout, QFrame, QInputDialog, QApplication)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import sys
import random
import unicodedata
import pandas as pd
from pathlib import Path

# Load and process CSV data with exact filename matching
def load_periodic_table_data():
    try:
        # Get script directory
        script_dir = Path(__file__).parent
        
        # Use correct filename with underscores
        csv_filename = "CH-200_projet_prog(Feuil1).csv"
        csv_path = script_dir / csv_filename
        
        print(f"Looking for CSV at: {csv_path}")
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        # Read CSV with proper parameters
        df = pd.read_csv(
            csv_path,
            sep=';',
            decimal=',',
            skipinitialspace=True,
            encoding='utf-8'
        )
        
        # Clean and process data
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=['symbole', 'position'])
        
        # Extract position coordinates
        df[['row', 'col']] = df['position'].str.extract(r'\((\d+),\s*(\d+)\)').astype(float).astype('Int64')
        
        # Create data structures
        elements = {}
        positions = {}
        for _, row in df.iterrows():
            symb = row['symbole'].strip()
            elements[symb] = {
                'nom': row['nom'],
                'num': int(row['num']),
                'masse': float(row['masse']),
                'famille': row['famille']
            }
            positions[symb] = (int(row['row']), int(row['col']))
        
        print(f"Loaded {len(elements)} elements successfully")
        return elements, positions
        
    except Exception as e:
        QMessageBox.critical(None, "Data Error", f"Failed to load data: {str(e)}")
        return {}, {}

# Family colors mapping
colors = {
    "Diatomic nonmetal": "#FFFF00",
    "Alkali metal": "#FFAAAA",
    "Alkaline Earth Metal": "#FF5555",
    "Transition Metal": "#F5F5DC",
    "Post-Transition Metal": "#FFA500",
    "Metalloid": "#FF80FF",
    "Polyatomic Nonmetal": "#A52A2A",
    "Noble Gas": "#00FF00"
}

class PeriodicTableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.elements, self.positions = load_periodic_table_data()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Interactive Periodic Table")
        self.setGeometry(100, 100, 1400, 800)
        
        # Central widget setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("Periodic Table of Elements")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Create grid layout
        grid = QGridLayout()
        main_layout.addLayout(grid)
        
        # Create element buttons
        for symb, pos in self.positions.items():
            btn = QPushButton(symb)
            btn.setFixedSize(80, 80)
            if symb in self.elements:
                family = self.elements[symb]['famille']
                btn.setStyleSheet(f"background-color: {colors.get(family, '#FFFFFF')};")
                btn.clicked.connect(lambda _, s=symb: self.show_info(s))
            grid.addWidget(btn, pos[0], pos[1])
        
        # Add legend
        self.add_legend(main_layout)
        
    def add_legend(self, layout):
        legend = QHBoxLayout()
        for family, color in colors.items():
            container = QWidget()
            box = QFrame()
            box.setFixedSize(20, 20)
            box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            
            hbox = QHBoxLayout()
            hbox.addWidget(box)
            hbox.addWidget(QLabel(family))
            container.setLayout(hbox)
            legend.addWidget(container)
        
        layout.addLayout(legend)
    
    def show_info(self, symbol):
        element = self.elements.get(symbol)
        if element:
            info = (
                f"<b>{element['nom']}</b><br>"
                f"Symbol: {symbol}<br>"
                f"Atomic Number: {element['num']}<br>"
                f"Atomic Mass: {element['masse']}<br>"
                f"Family: {element['famille']}"
            )
            QMessageBox.information(self, "Element Info", info)
        else:
            QMessageBox.warning(self, "Error", "Element data not found")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PeriodicTableApp()
    window.show()
    sys.exit(app.exec_())
