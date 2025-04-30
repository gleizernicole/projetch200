import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from elements_data import elements

def create_atomic_structure(symbol, element_data):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('equal')
    
    # Calculate values
    protons = element_data["num"]
    neutrons = int(round(element_data["masse"])) - protons
    electrons = protons
    
    # Nucleus
    ax.add_patch(Circle((0.5, 0.5), 0.1, color='#FF6666', alpha=0.7))
    ax.text(0.5, 0.53, f'P: {protons}', ha='center', va='center', fontsize=8)
    ax.text(0.5, 0.47, f'N: {neutrons}', ha='center', va='center', fontsize=8)
    
    # Electron shells
    shells = {1: 2, 2: 8, 3: 8, 4: 18, 5: 18, 6: 32, 7: 32}
    total_electrons = electrons
    current_shell = 1
    
    while total_electrons > 0:
        capacity = shells[current_shell]
        electrons_in_shell = min(capacity, total_electrons)
        radius = 0.2 + current_shell * 0.15
        
        for i in range(electrons_in_shell):
            angle = 2 * np.pi * i / electrons_in_shell
            x = 0.5 + radius * np.cos(angle)
            y = 0.5 + radius * np.sin(angle)
            ax.add_patch(Circle((x, y), 0.03, color='#6666FF', alpha=0.7))
        
        total_electrons -= electrons_in_shell
        current_shell += 1
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Create full path to target directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(project_root, "periodictable", "atomic_structures")
    os.makedirs(target_dir, exist_ok=True)
    
    output_path = os.path.join(target_dir, f"{symbol}.png")
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")  # Verification output

if __name__ == "__main__":
    for symbol, data in elements.items():
        create_atomic_structure(symbol, data)
    print("Atomic structure images generated successfully!")
