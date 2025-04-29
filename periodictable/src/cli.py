import sys
import argparse
from utils import elements, positions  # Assuming utils.py is in the same folder.

def show_element(symbol):
    """Function to show details of an element by its symbol."""
    element = elements.get(symbol.capitalize())
    if element:
        print(f"Element: {element['nom']}")
        print(f"Atomic Number: {element['num']}")
        print(f"Atomic Mass: {element['masse']}")
        print(f"Family: {element['famille']}")
        print(f"Position: Row {positions[symbol][0] + 1}, Column {positions[symbol][1] + 1}")
    else:
        print(f"Element {symbol} not found!")

def list_elements():
    """Function to list all elements by their symbol."""
    print("Elements available:")
    for symbol in elements:
        print(f"- {symbol}")

def search_element_by_family(family):
    """Search and list elements by their family."""
    found = False
    for symbol, element in elements.items():
        if element['famille'].lower() == family.lower():
            print(f"{symbol}: {element['nom']} - {element['famille']}")
            found = True
    if not found:
        print(f"No elements found in the family: {family}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Periodic Table CLI")
    
    # Commands and options
    parser.add_argument('-l', '--list', action='store_true', help="List all elements")
    parser.add_argument('-s', '--show', type=str, help="Show details of a specific element by symbol")
    parser.add_argument('-f', '--family', type=str, help="Search for elements by their family")
    
    # Parse the arguments
    args = parser.parse_args()

    # Handle different commands
    if args.list:
        list_elements()
    elif args.show:
        show_element(args.show)
    elif args.family:
        search_element_by_family(args.family)
    else:
        print("No valid option provided. Use -h for help.")

if __name__ == '__main__':
    main()
