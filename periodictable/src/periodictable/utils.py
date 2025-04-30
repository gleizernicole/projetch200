from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QGridLayout, QMessageBox, QHBoxLayout, QFrame, QInputDialog, 
                             QApplication, QScrollArea, QDialog, QLineEdit, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import sys, random, unicodedata
import os 
import QPixmap

# Dictionnaire des éléments complet
elements = {
    "H":  {"nom": "Hydrogène", "num": 1, "masse": 1.008, "famille": "non-métal",
           "state": "Gaz", "electron_config": "1s¹", "isotopes": ["¹H", "²H", "³H"]},
    "He": {"nom": "Hélium", "num": 2, "masse": 4.0026, "famille": "gaz noble",
           "state": "Gaz", "electron_config": "1s²", "isotopes": ["³He", "⁴He"]},
    "Li": {"nom": "Lithium", "num": 3, "masse": 6.94, "famille": "métal alcalin",
           "state": "Solide", "electron_config": "[He] 2s¹", "isotopes": ["⁶Li", "⁷Li"]},
    "Be": {"nom": "Béryllium", "num": 4, "masse": 9.0122, "famille": "métal alcalino-terreux",
           "state": "Solide", "electron_config": "[He] 2s²", "isotopes": ["⁹Be"]},
    "B":  {"nom": "Bore", "num": 5, "masse": 10.81, "famille": "métalloïde",
           "state": "Solide", "electron_config": "[He] 2s² 2p¹", "isotopes": ["¹⁰B", "¹¹B"]},
    "C":  {"nom": "Carbone", "num": 6, "masse": 12.011, "famille": "non-métal",
           "state": "Solide", "electron_config": "[He] 2s² 2p²", "isotopes": ["¹²C", "¹³C", "¹⁴C"]},
    "N":  {"nom": "Azote", "num": 7, "masse": 14.007, "famille": "non-métal",
           "state": "Gaz", "electron_config": "[He] 2s² 2p³", "isotopes": ["¹⁴N", "¹⁵N"]},
    "O":  {"nom": "Oxygène", "num": 8, "masse": 15.999, "famille": "chalcogène",
           "state": "Gaz", "electron_config": "[He] 2s² 2p⁴", "isotopes": ["¹⁶O", "¹⁷O", "¹⁸O"]},
    "F":  {"nom": "Fluor", "num": 9, "masse": 18.998, "famille": "halogène",
           "state": "Gaz", "electron_config": "[He] 2s² 2p⁵", "isotopes": ["¹⁹F"]},
    "Ne": {"nom": "Néon", "num": 10, "masse": 20.180, "famille": "gaz noble",
           "state": "Gaz", "electron_config": "[He] 2s² 2p⁶", "isotopes": ["²⁰Ne", "²¹Ne", "²²Ne"]},
    "Na": {"nom": "Sodium", "num": 11, "masse": 22.990, "famille": "métal alcalin",
           "state": "Solide", "electron_config": "[Ne] 3s¹", "isotopes": ["²³Na"]},
    "Mg": {"nom": "Magnésium", "num": 12, "masse": 24.305, "famille": "métal alcalino-terreux",
           "state": "Solide", "electron_config": "[Ne] 3s²", "isotopes": ["²⁴Mg", "²⁵Mg", "²⁶Mg"]},
    "Al": {"nom": "Aluminium", "num": 13, "masse": 26.982, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Ne] 3s² 3p¹", "isotopes": ["²⁷Al"]},
    "Si": {"nom": "Silicium", "num": 14, "masse": 28.085, "famille": "métalloïde",
           "state": "Solide", "electron_config": "[Ne] 3s² 3p²", "isotopes": ["²⁸Si", "²⁹Si", "³⁰Si"]},
    "P":  {"nom": "Phosphore", "num": 15, "masse": 30.974, "famille": "non-métal",
           "state": "Solide", "electron_config": "[Ne] 3s² 3p³", "isotopes": ["³¹P"]},
    "S":  {"nom": "Soufre", "num": 16, "masse": 32.06, "famille": "chalcogène",
           "state": "Solide", "electron_config": "[Ne] 3s² 3p⁴", "isotopes": ["³²S", "³³S", "³⁴S"]},
    "Cl": {"nom": "Chlore", "num": 17, "masse": 35.45, "famille": "halogène",
           "state": "Gaz", "electron_config": "[Ne] 3s² 3p⁵", "isotopes": ["³⁵Cl", "³⁷Cl"]},
    "Ar": {"nom": "Argon", "num": 18, "masse": 39.948, "famille": "gaz noble",
           "state": "Gaz", "electron_config": "[Ne] 3s² 3p⁶", "isotopes": ["³⁶Ar", "³⁸Ar", "⁴⁰Ar"]},
    "K":  {"nom": "Potassium", "num": 19, "masse": 39.098, "famille": "métal alcalin",
           "state": "Solide", "electron_config": "[Ar] 4s¹", "isotopes": ["³⁹K", "⁴⁰K", "⁴¹K"]},
    "Ca": {"nom": "Calcium", "num": 20, "masse": 40.078, "famille": "métal alcalino-terreux",
           "state": "Solide", "electron_config": "[Ar] 4s²", "isotopes": ["⁴⁰Ca", "⁴²Ca", "⁴³Ca"]},
    "Sc": {"nom": "Scandium", "num": 21, "masse": 44.956, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d¹ 4s²", "isotopes": ["⁴⁵Sc"]},
    "Ti": {"nom": "Titane", "num": 22, "masse": 47.867, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d² 4s²", "isotopes": ["⁴⁶Ti", "⁴⁷Ti", "⁴⁸Ti"]},
    "V":  {"nom": "Vanadium", "num": 23, "masse": 50.942, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d³ 4s²", "isotopes": ["⁵¹V"]},
    "Cr": {"nom": "Chrome", "num": 24, "masse": 51.996, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d⁵ 4s¹", "isotopes": ["⁵²Cr", "⁵³Cr"]},
    "Mn": {"nom": "Manganèse", "num": 25, "masse": 54.938, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d⁵ 4s²", "isotopes": ["⁵⁵Mn"]},
    "Fe": {"nom": "Fer", "num": 26, "masse": 55.845, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d⁶ 4s²", "isotopes": ["⁵⁴Fe", "⁵⁶Fe", "⁵⁷Fe"]},
    "Co": {"nom": "Cobalt", "num": 27, "masse": 58.933, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d⁷ 4s²", "isotopes": ["⁵⁹Co"]},
    "Ni": {"nom": "Nickel", "num": 28, "masse": 58.693, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d⁸ 4s²", "isotopes": ["⁵⁸Ni", "⁶⁰Ni"]},
    "Cu": {"nom": "Cuivre", "num": 29, "masse": 63.546, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d¹⁰ 4s¹", "isotopes": ["⁶³Cu", "⁶⁵Cu"]},
    "Zn": {"nom": "Zinc", "num": 30, "masse": 65.38, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Ar] 3d¹⁰ 4s²", "isotopes": ["⁶⁴Zn", "⁶⁶Zn"]},
    "Ga": {"nom": "Gallium", "num": 31, "masse": 69.723, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Ar] 3d¹⁰ 4s² 4p¹", "isotopes": ["⁶⁹Ga", "⁷¹Ga"]},
    "Ge": {"nom": "Germanium", "num": 32, "masse": 72.630, "famille": "métalloïde",
           "state": "Solide", "electron_config": "[Ar] 3d¹⁰ 4s² 4p²", "isotopes": ["⁷⁰Ge", "⁷²Ge"]},
    "As": {"nom": "Arsenic", "num": 33, "masse": 74.922, "famille": "métalloïde",
           "state": "Solide", "electron_config": "[Ar] 3d¹⁰ 4s² 4p³", "isotopes": ["⁷⁵As"]},
    "Se": {"nom": "Sélénium", "num": 34, "masse": 78.971, "famille": "chalcogène",
           "state": "Solide", "electron_config": "[Ar] 3d¹⁰ 4s² 4p⁴", "isotopes": ["⁷⁴Se", "⁷⁶Se"]},
    "Br": {"nom": "Brome", "num": 35, "masse": 79.904, "famille": "halogène",
           "state": "Liquide", "electron_config": "[Ar] 3d¹⁰ 4s² 4p⁵", "isotopes": ["⁷⁹Br", "⁸¹Br"]},
    "Kr": {"nom": "Krypton", "num": 36, "masse": 83.798, "famille": "gaz noble",
           "state": "Gaz", "electron_config": "[Ar] 3d¹⁰ 4s² 4p⁶", "isotopes": ["⁷⁸Kr", "⁸⁰Kr"]},
    "Rb": {"nom": "Rubidium", "num": 37, "masse": 85.468, "famille": "métal alcalin",
           "state": "Solide", "electron_config": "[Kr] 5s¹", "isotopes": ["⁸⁵Rb", "⁸⁷Rb"]},
    "Sr": {"nom": "Strontium", "num": 38, "masse": 87.62, "famille": "métal alcalino-terreux",
           "state": "Solide", "electron_config": "[Kr] 5s²", "isotopes": ["⁸⁴Sr", "⁸⁶Sr"]},
    "Y":  {"nom": "Yttrium", "num": 39, "masse": 88.906, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d¹ 5s²", "isotopes": ["⁸⁹Y"]},
    "Zr": {"nom": "Zirconium", "num": 40, "masse": 91.224, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d² 5s²", "isotopes": ["⁹⁰Zr", "⁹¹Zr"]},
    "Nb": {"nom": "Niobium", "num": 41, "masse": 92.906, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d⁴ 5s¹", "isotopes": ["⁹³Nb"]},
    "Mo": {"nom": "Molybdène", "num": 42, "masse": 95.95, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d⁵ 5s¹", "isotopes": ["⁹²Mo", "⁹⁴Mo"]},
    "Tc": {"nom": "Technétium", "num": 43, "masse": 98, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d⁵ 5s²", "isotopes": ["⁹⁷Tc", "⁹⁸Tc"]},
    "Ru": {"nom": "Ruthénium", "num": 44, "masse": 101.07, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d⁷ 5s¹", "isotopes": ["⁹⁶Ru", "⁹⁸Ru"]},
    "Rh": {"nom": "Rhodium", "num": 45, "masse": 102.91, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d⁸ 5s¹", "isotopes": ["¹⁰³Rh"]},
    "Pd": {"nom": "Palladium", "num": 46, "masse": 106.42, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰", "isotopes": ["¹⁰²Pd", "¹⁰⁴Pd"]},
    "Ag": {"nom": "Argent", "num": 47, "masse": 107.87, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰ 5s¹", "isotopes": ["¹⁰⁷Ag", "¹⁰⁹Ag"]},
    "Cd": {"nom": "Cadmium", "num": 48, "masse": 112.41, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰ 5s²", "isotopes": ["¹⁰⁶Cd", "¹⁰⁸Cd"]},
    "In": {"nom": "Indium", "num": 49, "masse": 114.82, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰ 5s² 5p¹", "isotopes": ["¹¹³In", "¹¹⁵In"]},
    "Sn": {"nom": "Étain", "num": 50, "masse": 118.71, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰ 5s² 5p²", "isotopes": ["¹¹²Sn", "¹¹⁴Sn"]},
    "Sb": {"nom": "Antimoine", "num": 51, "masse": 121.76, "famille": "métalloïde",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰ 5s² 5p³", "isotopes": ["¹²¹Sb", "¹²³Sb"]},
    "Te": {"nom": "Tellure", "num": 52, "masse": 127.60, "famille": "chalcogène",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰ 5s² 5p⁴", "isotopes": ["¹²⁰Te", "¹²²Te"]},
    "I":  {"nom": "Iode", "num": 53, "masse": 126.90, "famille": "halogène",
           "state": "Solide", "electron_config": "[Kr] 4d¹⁰ 5s² 5p⁵", "isotopes": ["¹²⁷I"]},
    "Xe": {"nom": "Xénon", "num": 54, "masse": 131.29, "famille": "gaz noble",
           "state": "Gaz", "electron_config": "[Kr] 4d¹⁰ 5s² 5p⁶", "isotopes": ["¹²⁴Xe", "¹²⁶Xe"]},
    "Cs": {"nom": "Césium", "num": 55, "masse": 132.91, "famille": "métal alcalin",
           "state": "Solide", "electron_config": "[Xe] 6s¹", "isotopes": ["¹³³Cs"]},
    "Ba": {"nom": "Baryum", "num": 56, "masse": 137.33, "famille": "métal alcalino-terreux",
           "state": "Solide", "electron_config": "[Xe] 6s²", "isotopes": ["¹³⁰Ba", "¹³²Ba"]},
    "La": {"nom": "Lanthane", "num": 57, "masse": 138.91, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 5d¹ 6s²", "isotopes": ["¹³⁸La", "¹³⁹La"]},
    "Ce": {"nom": "Cérium", "num": 58, "masse": 140.12, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f¹ 5d¹ 6s²", "isotopes": ["¹³⁶Ce", "¹³⁸Ce"]},
    "Pr": {"nom": "Praséodyme", "num": 59, "masse": 140.91, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f³ 6s²", "isotopes": ["¹⁴¹Pr"]},
    "Nd": {"nom": "Néodyme", "num": 60, "masse": 144.24, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f⁴ 6s²", "isotopes": ["¹⁴²Nd", "¹⁴³Nd"]},
    "Pm": {"nom": "Prométhium", "num": 61, "masse": 145, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f⁵ 6s²", "isotopes": ["¹⁴⁵Pm", "¹⁴⁷Pm"]},
    "Sm": {"nom": "Samarium", "num": 62, "masse": 150.36, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f⁶ 6s²", "isotopes": ["¹⁴⁴Sm", "¹⁴⁸Sm"]},
    "Eu": {"nom": "Europium", "num": 63, "masse": 151.98, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f⁷ 6s²", "isotopes": ["¹⁵¹Eu", "¹⁵³Eu"]},
    "Gd": {"nom": "Gadolinium", "num": 64, "masse": 157.25, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f⁷ 5d¹ 6s²", "isotopes": ["¹⁵²Gd", "¹⁵⁴Gd"]},
    "Tb": {"nom": "Terbium", "num": 65, "masse": 158.93, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f⁹ 6s²", "isotopes": ["¹⁵⁹Tb"]},
    "Dy": {"nom": "Dysprosium", "num": 66, "masse": 162.50, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁰ 6s²", "isotopes": ["¹⁵⁶Dy", "¹⁵⁸Dy"]},
    "Ho": {"nom": "Holmium", "num": 67, "masse": 164.93, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f¹¹ 6s²", "isotopes": ["¹⁶⁵Ho"]},
    "Er": {"nom": "Erbium", "num": 68, "masse": 167.26, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f¹² 6s²", "isotopes": ["¹⁶²Er", "¹⁶⁴Er"]},
    "Tm": {"nom": "Thulium", "num": 69, "masse": 168.93, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f¹³ 6s²", "isotopes": ["¹⁶⁹Tm"]},
    "Yb": {"nom": "Ytterbium", "num": 70, "masse": 173.04, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 6s²", "isotopes": ["¹⁶⁸Yb", "¹⁷⁰Yb"]},
    "Lu": {"nom": "Lutécium", "num": 71, "masse": 175.00, "famille": "lanthanide",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d¹ 6s²", "isotopes": ["¹⁷⁵Lu", "¹⁷⁶Lu"]},
    "Hf": {"nom": "Hafnium", "num": 72, "masse": 178.49, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d² 6s²", "isotopes": ["¹⁷⁴Hf", "¹⁷⁶Hf"]},
    "Ta": {"nom": "Tantale", "num": 73, "masse": 180.95, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d³ 6s²", "isotopes": ["¹⁸⁰Ta", "¹⁸¹Ta"]},
    "W":  {"nom": "Wolfram", "num": 74, "masse": 183.84, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d⁴ 6s²", "isotopes": ["¹⁸²W", "¹⁸³W"]},
    "Re": {"nom": "Rhénium", "num": 75, "masse": 186.21, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d⁵ 6s²", "isotopes": ["¹⁸⁵Re", "¹⁸⁷Re"]},
    "Os": {"nom": "Osmium", "num": 76, "masse": 190.23, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d⁶ 6s²", "isotopes": ["¹⁸⁴Os", "¹⁸⁶Os"]},
    "Ir": {"nom": "Iridium", "num": 77, "masse": 192.22, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d⁷ 6s²", "isotopes": ["¹⁹¹Ir", "¹⁹³Ir"]},
    "Pt": {"nom": "Platine", "num": 78, "masse": 195.08, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d⁹ 6s¹", "isotopes": ["¹⁹⁴Pt", "¹⁹⁵Pt"]},
    "Au": {"nom": "Or", "num": 79, "masse": 196.97, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s¹", "isotopes": ["¹⁹⁷Au"]},
    "Hg": {"nom": "Mercure", "num": 80, "masse": 200.59, "famille": "métal de transition",
           "state": "Liquide", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s²", "isotopes": ["¹⁹⁶Hg", "¹⁹⁸Hg"]},
    "Tl": {"nom": "Thallium", "num": 81, "masse": 204.38, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹", "isotopes": ["²⁰³Tl", "²⁰⁵Tl"]},
    "Pb": {"nom": "Plomb", "num": 82, "masse": 207.2, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²", "isotopes": ["²⁰⁴Pb", "²⁰⁶Pb"]},
    "Bi": {"nom": "Bismuth", "num": 83, "masse": 208.98, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p³", "isotopes": ["²⁰⁹Bi"]},
    "Po": {"nom": "Polonium", "num": 84, "masse": 209, "famille": "métalloïde",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁴", "isotopes": ["²¹⁰Po"]},
    "At": {"nom": "Astate", "num": 85, "masse": 210, "famille": "halogène",
           "state": "Solide", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁵", "isotopes": ["²¹⁰At", "²¹¹At"]},
    "Rn": {"nom": "Radon", "num": 86, "masse": 222, "famille": "gaz noble",
           "state": "Gaz", "electron_config": "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁶", "isotopes": ["²²²Rn"]},
    "Fr": {"nom": "Francium", "num": 87, "masse": 223, "famille": "métal alcalin",
           "state": "Solide", "electron_config": "[Rn] 7s¹", "isotopes": ["²²³Fr"]},
    "Ra": {"nom": "Radium", "num": 88, "masse": 226, "famille": "métal alcalino-terreux",
           "state": "Solide", "electron_config": "[Rn] 7s²", "isotopes": ["²²⁶Ra"]},
    "Ac": {"nom": "Actinium", "num": 89, "masse": 227, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 6d¹ 7s²", "isotopes": ["²²⁷Ac"]},
    "Th": {"nom": "Thorium", "num": 90, "masse": 232.04, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 6d² 7s²", "isotopes": ["²³²Th"]},
    "Pa": {"nom": "Protactinium", "num": 91, "masse": 231.04, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f² 6d¹ 7s²", "isotopes": ["²³¹Pa"]},
    "U":  {"nom": "Uranium", "num": 92, "masse": 238.03, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f³ 6d¹ 7s²", "isotopes": ["²³⁸U"]},
    "Np": {"nom": "Neptunium", "num": 93, "masse": 237, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f⁴ 6d¹ 7s²", "isotopes": ["²³⁷Np"]},
    "Pu": {"nom": "Plutonium", "num": 94, "masse": 244, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f⁶ 7s²", "isotopes": ["²³⁹Pu", "²⁴⁰Pu"]},
    "Am": {"nom": "Américium", "num": 95, "masse": 243, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f⁷ 7s²", "isotopes": ["²⁴¹Am"]},
    "Cm": {"nom": "Curium", "num": 96, "masse": 247, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f⁷ 6d¹ 7s²", "isotopes": ["²⁴⁴Cm"]},
    "Bk": {"nom": "Berkélium", "num": 97, "masse": 247, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f⁹ 7s²", "isotopes": ["²⁴⁷Bk"]},
    "Cf": {"nom": "Californium", "num": 98, "masse": 251, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁰ 7s²", "isotopes": ["²⁵²Cf"]},
    "Es": {"nom": "Einsteinium", "num": 99, "masse": 252, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f¹¹ 7s²", "isotopes": ["²⁵²Es"]},
    "Fm": {"nom": "Fermium", "num": 100, "masse": 257, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f¹² 7s²", "isotopes": ["²⁵⁷Fm"]},
    "Md": {"nom": "Mendélévium", "num": 101, "masse": 258, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f¹³ 7s²", "isotopes": ["²⁵⁸Md"]},
    "No": {"nom": "Nobelium", "num": 102, "masse": 259, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 7s²", "isotopes": ["²⁵⁹No"]},
    "Lr": {"nom": "Lawrencium", "num": 103, "masse": 262, "famille": "actinide",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 7s² 7p¹", "isotopes": ["²⁶²Lr"]},
    "Rf": {"nom": "Rutherfordium", "num": 104, "masse": 267, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d² 7s²", "isotopes": ["²⁶³Rf"]},
    "Db": {"nom": "Dubnium", "num": 105, "masse": 270, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d³ 7s²", "isotopes": ["²⁶⁸Db"]},
    "Sg": {"nom": "Seaborgium", "num": 106, "masse": 271, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d⁴ 7s²", "isotopes": ["²⁶⁹Sg"]},
    "Bh": {"nom": "Bohrium", "num": 107, "masse": 270, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d⁵ 7s²", "isotopes": ["²⁷⁰Bh"]},
    "Hs": {"nom": "Hassium", "num": 108, "masse": 277, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d⁶ 7s²", "isotopes": ["²⁷⁰Hs"]},
    "Mt": {"nom": "Meitnérium", "num": 109, "masse": 276, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d⁷ 7s²", "isotopes": ["²⁷⁶Mt"]},
    "Ds": {"nom": "Darmstadtium", "num": 110, "masse": 281, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d⁸ 7s²", "isotopes": ["²⁸¹Ds"]},
    "Rg": {"nom": "Roentgénium", "num": 111, "masse": 280, "famille": "métal de transition",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d⁹ 7s²", "isotopes": ["²⁸²Rg"]},
    "Cn": {"nom": "Copernicium", "num": 112, "masse": 285, "famille": "métal de transition",
           "state": "Liquide", "electron_config": "[Rn] 5f¹⁴ 6d¹⁰ 7s²", "isotopes": ["²⁸⁵Cn"]},
    "Nh": {"nom": "Nihonium", "num": 113, "masse": 284, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p¹", "isotopes": ["²⁸⁴Nh"]},
    "Fl": {"nom": "Flérovium", "num": 114, "masse": 289, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p²", "isotopes": ["²⁸⁹Fl"]},
    "Mc": {"nom": "Moscovium", "num": 115, "masse": 288, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p³", "isotopes": ["²⁸⁸Mc"]},
    "Lv": {"nom": "Livermorium", "num": 116, "masse": 293, "famille": "métal pauvre",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁴", "isotopes": ["²⁹³Lv"]},
    "Ts": {"nom": "Tennessine", "num": 117, "masse": 294, "famille": "halogène",
           "state": "Solide", "electron_config": "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁵", "isotopes": ["²⁹⁴Ts"]},
    "Og": {"nom": "Oganesson", "num": 118, "masse": 294, "famille": "gaz noble",
           "state": "Gaz", "electron_config": "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁶", "isotopes": ["²⁹⁴Og"]}
}

# Positions dans le tableau périodique (unchanged)
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

# Couleurs par famille (unchanged)
colors = {
            "non-métal": "#93C572",
            "métal alcalin": "#FFAAAA",
            "métal alcalino-terreux": "#FF5555",
            "métal de transition": "#ADD8E6",
            "métal pauvre": "#FFA500",
            "métalloïde": "#FF80FF",
            "chalcogène": "#A52A2A",
            "halogène": "#7B68EE",
            "gaz noble": "#00A36C",
            "lanthanide": "#00CCFF",
            "actinide": "#CCCCCC"
        }

class TableauPeriodique(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tableau Périodique Interactif + Quizz 🎲")
        self.setGeometry(100, 100, 800, 600)

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

        # Titre
        titre_label = QLabel("🧪 Tableau Périodique des Éléments 🧪")
        titre_label.setFont(QFont("Arial", 24, QFont.Bold))
        titre_label.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titre_label)

        # Score
        self.score_label = QLabel("Score : 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont("Arial", 16))
        layout_principal.addWidget(self.score_label)

        # Timer
        self.timer_label = QLabel(f"Temps restant : {self.time_remaining}s")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 16))
        layout_principal.addWidget(self.timer_label)

        # Bouton Quizz
        bouton_quizz = QPushButton("🎲 Lancer un Quizz")
        bouton_quizz.setFixedHeight(50)
        bouton_quizz.clicked.connect(self.lancer_quizz)
        layout_principal.addWidget(bouton_quizz)

        # Zone de défilement pour le tableau
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(1)
        self.grid.setContentsMargins(1, 1, 1, 1)
        scroll.setWidget(container)
        layout_principal.addWidget(scroll)
      
        # Création des boutons du tableau
        for symbole, position in positions.items():
            element = elements[symbole]
            bouton = QPushButton(symbole)
            bouton.setFixedSize(50, 50)
            couleur = colors.get(element["famille"], "#FFFFFF")
            bouton.setStyleSheet(f"""
                background-color: {couleur}; 
                border: 1px solid #333;
                font-weight: bold;
                font-size: 12px;
            """)
            bouton.clicked.connect(lambda checked, sym=symbole: self.afficher_infos(sym))
            self.grid.addWidget(bouton, *position)
          
        # Légende
        legend_layout = QHBoxLayout()
        for family, color in colors.items():
            color_box = QFrame()
            color_box.setFixedSize(20, 20)
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            label = QLabel(family)
            label.setContentsMargins(5, 0, 10, 0)
            family_layout = QHBoxLayout()
            family_layout.addWidget(color_box)
            family_layout.addWidget(label)
            container = QWidget()
            container.setLayout(family_layout)
            legend_layout.addWidget(container)

        layout_principal.addLayout(legend_layout)

    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.setText(f"Temps restant : {self.time_remaining}s")
        if self.time_remaining == 0:
            self.timer.stop()
            self.trop_tard()

   
    # In your main TableauPeriodique class
    def afficher_infos(self, symbole):
        element = elements[symbole]
    
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Structure atomique - {element['nom']}")
        dialog.setFixedSize(600, 700)
    
        layout = QVBoxLayout(dialog)
    
    # Atomic structure image
        img_label = QLabel()
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))  # File location
            img_path = os.path.join(current_dir, "..", "..", "atomic_structures", f"{symbole}.png")
        
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                img_label.setPixmap(pixmap.scaled(400, 400, 
                  Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                raise FileNotFoundError
   
        except Exception as e:
            img_label.setText(f"<i>Structure de {symbole} non disponible</i>")
            img_label.setStyleSheet("color: #666; font-size: 14px;")
    
        img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(img_label)
    
    # Element information
        info_text = QLabel((
            f"<b>{element['nom']} ({symbole})</b><br>"
            f"Numéro atomique: {element['num']}<br>"
            f"Masse atomique: {element['masse']} u<br>"
            f"Famille: {element['famille']}<br>"
            f"État: {element['state']}<br>"
            f"Configuration: {element['electron_config']}<br>"
            f"Isotopes: {', '.join(element['isotopes']}"
          ))
        info_text.setStyleSheet("font-size: 14px; padding: 15px;")
        layout.addWidget(info_text)
    
        dialog.exec_()
  
    def nettoyer(self, texte):
        texte = ''.join(c for c in unicodedata.normalize('NFD', texte)
                        if unicodedata.category(c) != 'Mn')
        return texte.lower().replace(" ", "")

    def lancer_quizz(self):
        self.score = 0
        self.question_count = 0
        self.score_label.setText(f"Score : {self.score}")
        self.time_remaining = 30
        self.quiz_active = True
        self.poser_question()

    def poser_question(self):
        if not self.quiz_active or self.question_count >= 10:
            if self.quiz_active:
                QMessageBox.information(self, "Quiz terminé ! 🎉", f"Score final : {self.score}/10")
            self.quiz_active = False
            return

        symbole = random.choice(list(elements.keys()))
        element = elements[symbole]
        question_type = random.choice(["symbole", "num"])

        if question_type == "symbole":
            question = f"Quel est le nom de l'élément de symbole <b>{symbole}</b> ?"
        else:
            question = f"Quel est le nom de l'élément de numéro atomique <b>{element['num']}</b> ?"

        self.reponse_attendue = element["nom"]
        self.time_remaining = 30
        self.timer.start()

        dialog = QDialog(self)
        dialog.setWindowTitle("Quizz 🎲 (30 sec)")
        layout = QVBoxLayout(dialog)
        
        question_label = QLabel(question)
        layout.addWidget(question_label)
        
        self.answer_input = QLineEdit()
        layout.addWidget(self.answer_input)
        
        button_box = QDialogButtonBox()
        submit_btn = button_box.addButton("Submit", QDialogButtonBox.AcceptRole)
        another_btn = button_box.addButton("Another Question", QDialogButtonBox.RejectRole)
        exit_btn = button_box.addButton("Exit Quiz", QDialogButtonBox.HelpRole)
        layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        exit_btn.clicked.connect(lambda: dialog.done(2))

        result = dialog.exec_()
        
        self.timer.stop()
        
        if result == QDialog.Accepted:
            reponse = self.answer_input.text()
            self.verifier_reponse(reponse)
            self.question_count += 1
            self.poser_question()
        elif result == 2:
            self.quiz_active = False
            QMessageBox.information(self, "Quiz abandonné", f"Score actuel : {self.score}/10")
        else:
            self.question_count += 1
            self.poser_question()

    def verifier_reponse(self, reponse):
        if self.nettoyer(reponse) == self.nettoyer(self.reponse_attendue):
            self.score += 1
            self.score_label.setText(f"Score : {self.score}")
            QMessageBox.information(self, "Bravo ! 🎉", f"Bonne réponse ! ✔️ C'était : {self.reponse_attendue}")
        else:
            QMessageBox.warning(self, "Oups ! 😢", f"Mauvaise réponse ! ❌\nLa bonne réponse était : {self.reponse_attendue}")

    def trop_tard(self):
        self.timer.stop()
        QMessageBox.warning(self, "⏰ Temps écoulé !", f"Trop tard ! La bonne réponse était : {self.reponse_attendue}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = TableauPeriodique()
    fenetre.show()
    sys.exit(app.exec_())
