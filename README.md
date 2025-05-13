# 🧪 Interactive Periodic Table for S&P Package


## 🎓 Project background

### The problem

In the third semester of the Chemistry bachelor at EPFL students are required to take a course on the chemistry of s and p block elements of the periodic table. Existing resources are limited and fragmented. 

### Our solution

We created an interactive periodic table to help learn details more effectively, group useful information, and practice with either free response or multiple choice quizzes. 

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

## ✨ Features

### 🔍 Interactive Periodic Table
- **Visual Element Navigation**: Colour-coded periodic table organised by element families
- **Detailed Element Information**: Access data for each element by clicking on its tile
- **Compact Design**: Optimised layout that fits on standard screens while maintaining readability

### 📊 Element data visualisation
- **Atomic Structure Images**: Visual representation of electron configuration for each element
- **Comprehensive Element Properties**:
  - Element name and symbol
  - Atomic number and weight
  - Element family classification
  - Physical state at standard conditions
  - Electron configuration
  - Isotope information
  - Production methods with detailed reactions

### 🎮 Interactive Quiz System
- **Multiple Quiz Formats**: Choose between multiple-choice or free-response questions
- **Diverse Question Types**:
  - Identify elements by symbol
  - Identify elements by atomic number
  - Match electron configurations to elements
  - Connect production methods to elements
- **Timed Challenges**: 30-second countdown per question to test rapid recall
- **Progress Tracking**: Score monitoring throughout the quiz session
- **Session Management**: 10-question sessions with final score summary

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
git clone https://github.com/gleizernicole/projetch200.git

# Navigate to project directory
cd periodictable

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
