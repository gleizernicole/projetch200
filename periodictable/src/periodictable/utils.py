from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QGridLayout, QMessageBox, QHBoxLayout, QFrame, QInputDialog, 
                             QApplication, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import sys, random, unicodedata

#  Dictionnaire des éléments 
elements = {
    "H":  {"nom": "Hydrogène", "num": 1, "masse": 1.008, "famille": "non-métal"},
    "He": {"nom": "Hélium", "num": 2, "masse": 4.0026, "famille": "gaz noble"},
    "Li": {"nom": "Lithium", "num": 3, "masse": 6.94, "famille": "métal alcalin"},
    "Be": {"nom": "Béryllium", "num": 4, "masse": 9.0122, "famille": "métal alcalino-terreux"},
    "B":  {"nom": "Bore", "num": 5, "masse": 10.81, "famille": "métalloïde"},
    "C":  {"nom": "Carbone", "num": 6, "masse": 12.011, "famille": "non-métal"},
    "N":  {"nom": "Azote", "num": 7, "masse": 14.007, "famille": "non-métal"},
    "O":  {"nom": "Oxygène", "num": 8, "masse": 15.999, "famille": "non-métal"},
    "F":  {"nom": "Fluor", "num": 9, "masse": 18.998, "famille": "halogène"},
    "Ne": {"nom": "Néon", "num": 10, "masse": 20.180, "famille": "gaz noble"},
    "Na": {"nom": "Sodium", "num": 11, "masse": 22.990, "famille": "métal alcalin"},
    "Mg": {"nom": "Magnésium", "num": 12, "masse": 24.305, "famille": "métal alcalino-terreux"},
    "Al": {"nom": "Aluminium", "num": 13, "masse": 26.982, "famille": "métal pauvre"},
    "Si": {"nom": "Silicium", "num": 14, "masse": 28.085, "famille": "métalloïde"},
    "P":  {"nom": "Phosphore", "num": 15, "masse": 30.974, "famille": "non-métal"},
    "S":  {"nom": "Soufre", "num": 16, "masse": 32.06, "famille": "non-métal"},
    "Cl": {"nom": "Chlore", "num": 17, "masse": 35.45, "famille": "halogène"},
    "Ar": {"nom": "Argon", "num": 18, "masse": 39.948, "famille": "gaz noble"},
    "K":  {"nom": "Potassium", "num": 19, "masse": 39.098, "famille": "métal alcalin"},
    "Ca": {"nom": "Calcium", "num": 20, "masse": 40.078, "famille": "métal alcalino-terreux"},
    "Sc": {"nom": "Scandium", "num": 21, "masse": 44.956, "famille": "métal de transition"},
    "Ti": {"nom": "Titane", "num": 22, "masse": 47.867, "famille": "métal de transition"},
    "V":  {"nom": "Vanadium", "num": 23, "masse": 50.942, "famille": "métal de transition"},
    "Cr": {"nom": "Chrome", "num": 24, "masse": 51.996, "famille": "métal de transition"},
    "Mn": {"nom": "Manganèse", "num": 25, "masse": 54.938, "famille": "métal de transition"},
    "Fe": {"nom": "Fer", "num": 26, "masse": 55.845, "famille": "métal de transition"},
    "Co": {"nom": "Cobalt", "num": 27, "masse": 58.933, "famille": "métal de transition"},
    "Ni": {"nom": "Nickel", "num": 28, "masse": 58.693, "famille": "métal de transition"},
    "Cu": {"nom": "Cuivre", "num": 29, "masse": 63.546, "famille": "métal de transition"},
    "Zn": {"nom": "Zinc", "num": 30, "masse": 65.38, "famille": "métal de transition"},
    "Ga": {"nom": "Gallium", "num": 31, "masse": 69.723, "famille": "métal pauvre"},
    "Ge": {"nom": "Germanium", "num": 32, "masse": 72.630, "famille": "métalloïde"},
    "As": {"nom": "Arsenic", "num": 33, "masse": 74.922, "famille": "métalloïde"},
    "Se": {"nom": "Sélénium", "num": 34, "masse": 78.971, "famille": "non-métal"},
    "Br": {"nom": "Brome", "num": 35, "masse": 79.904, "famille": "halogène"},
    "Kr": {"nom": "Krypton", "num": 36, "masse": 83.798, "famille": "gaz noble"},
    "Rb": {"nom": "Rubidium", "num": 37, "masse": 85.468, "famille": "métal alcalin"},
    "Sr": {"nom": "Strontium", "num": 38, "masse": 87.62, "famille": "métal alcalino-terreux"},
    "Y":  {"nom": "Yttrium", "num": 39, "masse": 88.906, "famille": "métal de transition"},
    "Zr": {"nom": "Zirconium", "num": 40, "masse": 91.224, "famille": "métal de transition"},
    "Nb": {"nom": "Niobium", "num": 41, "masse": 92.906, "famille": "métal de transition"},
    "Mo": {"nom": "Molybdène", "num": 42, "masse": 95.95, "famille": "métal de transition"},
    "Tc": {"nom": "Technétium", "num": 43, "masse": 98, "famille": "métal de transition"},
    "Ru": {"nom": "Ruthénium", "num": 44, "masse": 101.07, "famille": "métal de transition"},
    "Rh": {"nom": "Rhodium", "num": 45, "masse": 102.91, "famille": "métal de transition"},
    "Pd": {"nom": "Palladium", "num": 46, "masse": 106.42, "famille": "métal de transition"},
    "Ag": {"nom": "Argent", "num": 47, "masse": 107.87, "famille": "métal de transition"},
    "Cd": {"nom": "Cadmium", "num": 48, "masse": 112.41, "famille": "métal de transition"},
    "In": {"nom": "Indium", "num": 49, "masse": 114.82, "famille": "métal pauvre"},
    "Sn": {"nom": "Étain", "num": 50, "masse": 118.71, "famille": "métal pauvre"},
    "Sb": {"nom": "Antimoine", "num": 51, "masse": 121.76, "famille": "métalloïde"},
    "Te": {"nom": "Tellure", "num": 52, "masse": 127.60, "famille": "chalcogène"},
    "I":  {"nom": "Iode", "num": 53, "masse": 126.90, "famille": "halogène"},
    "Xe": {"nom": "Xénon", "num": 54, "masse": 131.29, "famille": "gaz noble"},
    "Cs": {"nom": "Césium", "num": 55, "masse": 132.91, "famille": "métal alcalin"},
    "Ba": {"nom": "Baryum", "num": 56, "masse": 137.33, "famille": "métal alcalino-terreux"},
    "La": {"nom": "Lanthane", "num": 57, "masse": 138.91, "famille": "lanthanide"},
    "Ce": {"nom": "Cérium", "num": 58, "masse": 140.12, "famille": "lanthanide"},
    "Pr": {"nom": "Praséodyme", "num": 59, "masse": 140.91, "famille": "lanthanide"},
    "Nd": {"nom": "Néodyme", "num": 60, "masse": 144.24, "famille": "lanthanide"},
    "Pm": {"nom": "Prométhium", "num": 61, "masse": 145, "famille": "lanthanide"},
    "Sm": {"nom": "Samarium", "num": 62, "masse": 150.36, "famille": "lanthanide"},
    "Eu": {"nom": "Europium", "num": 63, "masse": 151.98, "famille": "lanthanide"},
    "Gd": {"nom": "Gadolinium", "num": 64, "masse": 157.25, "famille": "lanthanide"},
    "Tb": {"nom": "Terbium", "num": 65, "masse": 158.93, "famille": "lanthanide"},
    "Dy": {"nom": "Dysprosium", "num": 66, "masse": 162.50, "famille": "lanthanide"},
    "Ho": {"nom": "Holmium", "num": 67, "masse": 164.93, "famille": "lanthanide"},
    "Er": {"nom": "Erbium", "num": 68, "masse": 167.26, "famille": "lanthanide"},
    "Tm": {"nom": "Thulium", "num": 69, "masse": 168.93, "famille": "lanthanide"},
    "Yb": {"nom": "Ytterbium", "num": 70, "masse": 173.04, "famille": "lanthanide"},
    "Lu": {"nom": "Lutécium", "num": 71, "masse": 175.00, "famille": "lanthanide"},
    "Hf": {"nom": "Hafnium", "num": 72, "masse": 178.49, "famille": "métal de transition"},
    "Ta": {"nom": "Tantale", "num": 73, "masse": 180.95, "famille": "métal de transition"},
    "W":  {"nom": "Wolfram", "num": 74, "masse": 183.84, "famille": "métal de transition"},
    "Re": {"nom": "Rhénium", "num": 75, "masse": 186.21, "famille": "métal de transition"},
    "Os": {"nom": "Osmium", "num": 76, "masse": 190.23, "famille": "métal de transition"},
    "Ir": {"nom": "Iridium", "num": 77, "masse": 192.22, "famille": "métal de transition"},
    "Pt": {"nom": "Platine", "num": 78, "masse": 195.08, "famille": "métal de transition"},
    "Au": {"nom": "Or", "num": 79, "masse": 196.97, "famille": "métal de transition"},
    "Hg": {"nom": "Mercure", "num": 80, "masse": 200.59, "famille": "métal de transition"},
    "Tl": {"nom": "Thallium", "num": 81, "masse": 204.38, "famille": "métal pauvre"},
    "Pb": {"nom": "Plomb", "num": 82, "masse": 207.2, "famille": "métal pauvre"},
    "Bi": {"nom": "Bismuth", "num": 83, "masse": 208.98, "famille": "métal pauvre"},
    "Po": {"nom": "Polonium", "num": 84, "masse": 209, "famille": "métalloïde"},
    "At": {"nom": "Astate", "num": 85, "masse": 210, "famille": "halogène"},
    "Rn": {"nom": "Radon", "num": 86, "masse": 222, "famille": "gaz noble"},
    "Fr": {"nom": "Francium", "num": 87, "masse": 223, "famille": "métal alcalin"},
    "Ra": {"nom": "Radium", "num": 88, "masse": 226, "famille": "métal alcalino-terreux"},
    "Ac": {"nom": "Actinium", "num": 89, "masse": 227, "famille": "actinide"},
    "Th": {"nom": "Thorium", "num": 90, "masse": 232.04, "famille": "actinide"},
    "Pa": {"nom": "Protactinium", "num": 91, "masse": 231.04, "famille": "actinide"},
    "U":  {"nom": "Uranium", "num": 92, "masse": 238.03, "famille": "actinide"},
    "Np": {"nom": "Neptunium", "num": 93, "masse": 237, "famille": "actinide"},
    "Pu": {"nom": "Plutonium", "num": 94, "masse": 244, "famille": "actinide"},
    "Am": {"nom": "Américium", "num": 95, "masse": 243, "famille": "actinide"},
    "Cm": {"nom": "Curium", "num": 96, "masse": 247, "famille": "actinide"},
    "Bk": {"nom": "Berkélium", "num": 97, "masse": 247, "famille": "actinide"},
    "Cf": {"nom": "Californium", "num": 98, "masse": 251, "famille": "actinide"},
    "Es": {"nom": "Einsteinium", "num": 99, "masse": 252, "famille": "actinide"},
    "Fm": {"nom": "Fermium", "num": 100, "masse": 257, "famille": "actinide"},
    "Md": {"nom": "Mendélévium", "num": 101, "masse": 258, "famille": "actinide"},
    "No": {"nom": "Nobelium", "num": 102, "masse": 259, "famille": "actinide"},
    "Lr": {"nom": "Lawrencium", "num": 103, "masse": 262, "famille": "actinide"},
    "Rf": {"nom": "Rutherfordium", "num": 104, "masse": 267, "famille": "métal de transition"},
    "Db": {"nom": "Dubnium", "num": 105, "masse": 270, "famille": "métal de transition"},
    "Sg": {"nom": "Seaborgium", "num": 106, "masse": 271, "famille": "métal de transition"},
    "Bh": {"nom": "Bohrium", "num": 107, "masse": 270, "famille": "métal de transition"},
    "Hs": {"nom": "Hassium", "num": 108, "masse": 277, "famille": "métal de transition"},
    "Mt": {"nom": "Meitnérium", "num": 109, "masse": 276, "famille": "métal de transition"},
    "Ds": {"nom": "Darmstadtium", "num": 110, "masse": 281, "famille": "métal de transition"},
    "Rg": {"nom": "Roentgénium", "num": 111, "masse": 280, "famille": "métal de transition"},
    "Cn": {"nom": "Copernicium", "num": 112, "masse": 285, "famille": "métal de transition"},
    "Nh": {"nom": "Nihonium", "num": 113, "masse": 284, "famille": "métal pauvre"},
    "Fl": {"nom": "Flérovium", "num": 114, "masse": 289, "famille": "métal pauvre"},
    "Mc": {"nom": "Moscovium", "num": 115, "masse": 288, "famille": "métal pauvre"},
    "Lv": {"nom": "Livermorium", "num": 116, "masse": 293, "famille": "métal pauvre"},
    "Ts": {"nom": "Tennessine", "num": 117, "masse": 294, "famille": "halogène"},
    "Og": {"nom": "Oganesson", "num": 118, "masse": 294, "famille": "gaz noble"}
}

#  Positions dans le tableau périodique 
positions = {
    "H": (0, 0), "He": (0, 17),
    "Li": (1, 0), "Be": (1, 1), "B": (1, 12), "C": (1, 13), "N": (1, 14), "O": (1, 15), "F": (1, 16), "Ne": (1, 17),
    "Na": (2, 0), "Mg": (2, 1), "Al": (2, 12), "Si": (2, 13), "P": (2, 14), "S": (2, 15), "Cl": (2, 16), "Ar": (2, 17),
    "K": (3, 0), "Ca": (3, 1), "Sc": (3, 2), "Ti": (3, 3), "V": (3, 4), "Cr": (3, 5), "Mn": (3, 6), "Fe": (3, 7), 
    "Co": (3, 8), "Ni": (3, 9), "Cu": (3, 10), "Zn": (3, 11), "Ga": (3, 12), "Ge": (3, 13), "As": (3, 14), "Se": (3, 15), 
    "Br": (3, 16), "Kr": (3, 17),
    "Rb": (4, 0), "Sr": (4, 1), "Y": (4, 2), "Zr": (4, 3), "Nb": (4, 4), "Mo": (4, 5), "Tc": (4, 6), "Ru": (4, 7), 
    "Rh": (4, 8), "Pd": (4, 9), "Ag": (4, 10), "Cd": (4, 11), "In": (4, 12), "Sn": (4, 13), "Sb": (4, 14), "Te":(4,15), "I": (4, 16), 
    "Xe": (4, 17),
    "Cs": (5, 0), "Ba": (5, 1), "La": (10, 2), "Ce": (10, 3), "Pr": (10, 4), "Nd": (10, 5), "Pm": (10, 6), "Sm": (10, 7), 
    "Eu": (10, 8), "Gd": (10, 9), "Tb": (10, 10), "Dy": (10, 11), "Ho": (10, 12), "Er": (10, 13), "Tm": (10, 14), "Yb": (10, 15), 
    "Lu": (5, 2),
    "Hf": (5, 3), "Ta": (5, 4), "W": (5, 5), "Re": (5, 6), "Os": (5, 7), "Ir": (5, 8), "Pt": (5, 9), "Au": (5, 10), 
    "Hg": (5, 11), "Tl": (5, 12), "Pb": (5, 13), "Bi": (5, 14), "Po": (5, 15), "At": (5, 16), "Rn": (5, 17),
    "Fr": (6, 0), "Ra": (6, 1), "Ac": (11, 2), "Th": (11, 3), "Pa": (11, 4), "U": (11, 5), "Np": (11, 6), "Pu": (11, 7), 
    "Am": (11, 8), "Cm": (11, 9), "Bk": (11, 10), "Cf": (11, 11), "Es": (11, 12), "Fm": (11, 13), "Md": (11, 14), "No": (11, 15), 
    "Lr": (6, 2),
    "Rf": (6, 3), "Db": (6, 4), "Sg": (6, 5), "Bh": (6, 6), "Hs": (6, 7), "Mt": (6, 8), "Ds": (6, 9), "Rg": (6, 10), 
    "Cn": (6, 11), "Nh": (6, 12), "Fl": (6, 13), "Mc": (6, 14), "Lv": (6, 15), "Ts": (6, 16), "Og": (6, 17)
}

#  Couleurs par famille
colors = {
            "non-métal": "#FFFF00",
            "métal alcalin": "#FFAAAA",
            "métal alcalino-terreux": "#FF5555",
            "métal de transition": "#ADD8E6",
            "métal pauvre": "#FFA500",
            "métalloïde": "#FF80FF",
            "chalcogène": "#A52A2A",
            "halogène": "#80FFFF",
            "gaz noble": "#00FF00",
            "lanthanide": "#00CCFF",
            "actinide": "#CCCCCC"
        }

class TableauPeriodique(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Tableau Périodique Interactif + Quizz 🎲")
        self.setGeometry(100, 100, 1000, 800)

        # Variables du jeu
        self.score = 0
        self.question_count = 0
        self.time_remaining = 30
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Section supérieure (titre, score, timer, bouton)
        self.setup_top_section(main_layout)
        
        # Tableau périodique avec scroll
        self.setup_periodic_table(main_layout)
        
        # Légende avec scroll
        self.setup_legend(main_layout)

    def setup_top_section(self, layout):
        # Titre
        title = QLabel("🧪 Tableau Périodique des Éléments 🧪")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Score et Timer
        info_layout = QHBoxLayout()
        self.score_label = QLabel("Score : 0")
        self.timer_label = QLabel(f"Temps : {self.time_remaining}s")
        for lbl in [self.score_label, self.timer_label]:
            lbl.setFont(QFont("Arial", 14))
            info_layout.addWidget(lbl)
        layout.addLayout(info_layout)

        # Bouton Quizz
        btn_quiz = QPushButton("🎲 Lancer le Quizz (10 questions)")
        btn_quiz.setStyleSheet("font-size: 16px; padding: 10px;")
        btn_quiz.clicked.connect(self.lancer_quizz)
        layout.addWidget(btn_quiz)

    def setup_periodic_table(self, layout):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        
        for symb, pos in positions.items():
            btn = self.create_element_button(symb)
            grid.addWidget(btn, *pos)
            
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def create_element_button(self, symbole):
        element = elements[symbole]
        btn = QPushButton(symbole)
        btn.setFixedSize(55, 55)
        btn.setStyleSheet(f"""
            background-color: {colors[element['famille']};
            border: 1px solid #333;
            font-weight: bold;
            font-size: 14px;
        """)
        btn.clicked.connect(lambda: self.afficher_infos(symbole))
        return btn

    def setup_legend(self, layout):
        legend_scroll = QScrollArea()
        legend_scroll.setWidgetResizable(True)
        legend_container = QWidget()
        legend_layout = QVBoxLayout(legend_container)
        
        # Groupements logiques
        categories = {
            "Métaux": [
                ("métal alcalin", ["Li", "Na", "K", "Rb", "Cs", "Fr"]),
                ("métal alcalino-terreux", ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"]),
                ("métal de transition", [symb for symb, data in elements.items() if data["famille"] == "métal de transition"]),
                ("métal pauvre", ["Al", "Ga", "In", "Sn", "Tl", "Pb", "Bi"])
            ],
            "Non-métaux": [
                ("non-métal", ["H", "C", "N", "O", "P", "S", "Se"]),
                ("métalloïde", ["B", "Si", "Ge", "As", "Sb", "Te", "Po"]),
                ("halogène", ["F", "Cl", "Br", "I", "At", "Ts"]),
                ("gaz noble", ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"])
            ],
            "Terres Rares": [
                ("lanthanide", [symb for symb, data in elements.items() if data["famille"] == "lanthanide"]),
                ("actinide", [symb for symb, data in elements.items() if data["famille"] == "actinide"])
            ],
            "Autres": [
                ("chalcogène", ["O", "S", "Se", "Te", "Po"])
            ]
        }

        for categorie, familles in categories.items():
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet("margin: 5px; padding: 5px;")
            categorie_layout = QVBoxLayout(frame)
            
            # Titre catégorie
            lbl_cat = QLabel(categorie)
            lbl_cat.setStyleSheet("font-weight: bold; color: #333; font-size: 16px;")
            categorie_layout.addWidget(lbl_cat)
            
            # Items
            for famille, elements in familles:
                hbox = QHBoxLayout()
                hbox.addSpacing(15)
                
                # Carré couleur
                color_box = QFrame()
                color_box.setFixedSize(20, 20)
                color_box.setStyleSheet(f"background-color: {colors[famille]}; border: 1px solid black;")
                hbox.addWidget(color_box)
                
                # Texte
                lbl = QLabel(f"{famille.capitalize()}: {', '.join(elements)}")
                lbl.setStyleSheet("font-size: 12px; margin-left: 5px;")
                lbl.setWordWrap(True)
                hbox.addWidget(lbl)
                
                categorie_layout.addLayout(hbox)
            
            legend_layout.addWidget(frame)
        
        legend_scroll.setWidget(legend_container)
        layout.addWidget(legend_scroll)

    # ... (Les méthodes restantes inchangées: update_timer, afficher_infos, nettoyer, 
    # lancer_quizz, poser_question, verifier_reponse, trop_tard)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableauPeriodique()
    window.show()
    sys.exit(app.exec_())
