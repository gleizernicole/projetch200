# 🧪 Interactive Periodic Table for S&P Package

## 🎓 Project background

### The problem

In the third semester of the Chemistry bachelor at EPFL students are required to take a course on the chemistry of s and p block elements of the periodic table.

---

## 📄 Description

The package generates a structured periodic table and includes utilities for working with element data. It emphasizes interactive learning and modular design for future extensions.


## 📂 Project structure 

```text
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
```

---

## 🚀 Getting started

### Prerequisites

- Python 3.10+
- Conda or virtual environment (optional but recommended)
- PyQt5
- pandas
- numpy
- scipy

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/periodic-table-project.git

# Navigate to project directory
cd periodic-table-project

# Create and activate virtual environment
conda create -n periodictable python=3.10
conda activate periodictable

# Install dependencies
pip install -r requirements.txt
```

### Running the application 

```bash
# Navigate to source directory
cd src

# Launch interactive periodic table
python -m periodictable.utils

# Generate periodic table structure
python -m periodictable.generate_structure
```

## ✅ Testing

```bash
# Run unit tests
cd src
python -m unittest periodictable/tests/test_periodictable.py
```
