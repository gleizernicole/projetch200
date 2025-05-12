# 🧪 Interactive Periodic Table for S&P Package

This project is part of a programming assignment focused on the s and p blocks of the periodic table. It provides Python tools to generate the table structure and perform element-related utilities.

---

## 📄 Description

The package generates a structured periodic table and includes utilities for working with element data. It emphasizes interactive learning and modular design for future extensions.

## 📂 Project structure 

periodictable/
├── README.md                     # Project documentation
├── src/
│   └── periodictable/
│       ├── __init__.py
│       ├── generate_structure.py # Generates the periodic table structure
│       ├── utils.py              # Utility functions for periodic table operations
│       ├── elements_data.py      # Contains element configurations and metadata
│       └── tests/
│           ├── __init__.py
│           └── test_periodictable.py # Unit tests for the package

---

## 🚀 Getting started

### Prerequisites

- Python 3.10+
- Conda or virtual environment (optional but recommended)
- PyQt5
- pandas
- numpy
- scipy

Activate your environment:

```bash
conda activate projetch200
```
## ⚙️ Usage 

```bash
cd src
# Generate the periodic table structure
python -m periodictable.generate_structure
# Run utility functions
python -m periodictable.utils
```

## ✅ Running tests

```bash
cd src
python -m unittest periodictable/tests/test_periodictable.py
```
