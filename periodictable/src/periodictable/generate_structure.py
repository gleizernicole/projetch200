import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from elements_data import elements

def create_atomic_structure(symbol, element_data):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('equal')
    
    # Nucleus
    ax.add_patch(Circle((0.5, 0.5), 0.1, color='#FF6666', alpha=0.7))
    ax.text(0.5, 0.53, f'P: {element_data["protons"]}', ha='center', va='center', fontsize=8)
    ax.text(0.5, 0.47, f'N: {element_data["neutrons"]}', ha='center', va='center', fontsize=8)
    
    # Electron configuration
    electron_config = element_data["electron_config"]
    shells = {
        1: 2,
        2: 8,
        3: 8,
        4: 18,
        5: 18,
        6: 32,
        7: 32
    }
    
    total_electrons = element_data["electrons"]
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
    
    os.makedirs("atomic_structures", exist_ok=True)
    plt.savefig(f"atomic_structures/{symbol}.png", dpi=100, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    for symbol, data in elements.items():
        create_atomic_structure(symbol, data)
    print("Atomic structure images generated successfully!")
