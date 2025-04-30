import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def create_atomic_structure(symbol, element_data):
    # Create figure and plot elements first
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('equal')
    
    # Calculate values
    protons = element_data["num"]
    neutrons = int(round(element_data["masse"])) - protons
    electrons = protons
    
    # Draw nucleus
    ax.add_patch(Circle((0.5, 0.5), 0.1, color='#FF6666', alpha=0.7))
    ax.text(0.5, 0.53, f'P: {protons}', ha='center', va='center', fontsize=8)
    ax.text(0.5, 0.47, f'N: {neutrons}', ha='center', va='center', fontsize=8)
    
    # Draw electron shells
    shells = {1: 2, 2: 8, 3: 8, 4: 18, 5: 18, 6: 32, 7: 32}
    total_electrons = electrons
    current_shell = 1
    
    while total_electrons > 0:
        # ... electron drawing code ...
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # ====== CORRECT PATH HANDLING ======
    current_dir = os.path.dirname(os.path.abspath(__file__))  # src/periodictable/
    output_dir = os.path.join(current_dir, "..", "..", "atomic_structures")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{symbol}.png")
    # ===================================
    
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")  # Verification
