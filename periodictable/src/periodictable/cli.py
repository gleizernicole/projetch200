import sys
import argparse
from .utils import elements, positions  # Use relative import for packages

def show_element(symbol):
    """Display element details by symbol."""
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
    """List all element symbols."""
    print("Available elements:")
    for symbol in elements:
        print(f"- {symbol}")

def search_element_by_family(family):
    """Search elements by family."""
    found = False
    for symbol, element in elements.items():
        if element['famille'].lower() == family.lower():
            print(f"{symbol}: {element['nom']} - {element['famille']}")
            found = True
    if not found:
        print(f"No elements found in family: {family}")

def run():
    """Entry point function for CLI execution."""
    parser = argparse.ArgumentParser(description="Periodic Table CLI Tool")
    
    # Command-line arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', action='store_true', help="List all elements")
    group.add_argument('-s', '--show', type=str, help="Show details of an element")
    group.add_argument('-f', '--family', type=str, help="Search elements by family")
    
    args = parser.parse_args()

    if args.list:
        list_elements()
    elif args.show:
        show_element(args.show)
    elif args.family:
        search_element_by_family(args.family)
    else:
        parser.print_help()  # Show help when no args provided

if __name__ == '__main__':
    run()  # Direct script execution
