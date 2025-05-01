import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from elements_data import elements

def create_3d_atomic_structure(symbol, element_data):
    # Create 3D figure
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Atomic properties
    protons = element_data["num"]
    electrons = protons
    max_shell = 7
    
    # Create nucleus
    ax.scatter(0, 0, 0, s=1000, c='#FF6666', alpha=0.7, label='Nucleus')
    
    # Create electron orbitals
    shell_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                    '#9467bd', '#8c564b', '#e377c2']
    
    current_shell = 1
    remaining_electrons = electrons
    
    while remaining_electrons > 0 and current_shell <= max_shell:
        # Calculate electrons in this shell
        shell_capacity = 2 * current_shell**2
        electrons_in_shell = min(shell_capacity, remaining_electrons)
        
        # Generate spherical coordinates
        theta = np.linspace(0, 2*np.pi, electrons_in_shell)
        phi = np.linspace(0, np.pi, electrons_in_shell)
        r = current_shell * 0.5  # Scaling factor
        
        # Convert to cartesian coordinates
        x = r * np.outer(np.cos(theta), np.sin(phi)).flatten()
        y = r * np.outer(np.sin(theta), np.sin(phi)).flatten()
        z = r * np.outer(np.ones(electrons_in_shell), np.cos(phi)).flatten()
        
        # Add some randomness for orbital visualization
        x += np.random.normal(0, 0.1, x.shape)
        y += np.random.normal(0, 0.1, y.shape)
        z += np.random.normal(0, 0.1, z.shape)
        
        # Plot electrons
        ax.scatter(x, y, z, s=50, 
                 color=shell_colors[current_shell-1],
                 alpha=0.6,
                 label=f'Shell {current_shell}')
        
        remaining_electrons -= electrons_in_shell
        current_shell += 1
    
    # Visualization settings
    ax.set_xlim([-max_shell*0.5, max_shell*0.5])
    ax.set_ylim([-max_shell*0.5, max_shell*0.5])
    ax.set_zlim([-max_shell*0.5, max_shell*0.5])
    ax.axis('off')
    
    # Adjust view angle
    ax.view_init(elev=30, azim=45)
    
    # Save image
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "3d_structures")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{symbol}_3d.png")
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Generated 3D structure: {output_path}")

# Generate for all elements
if __name__ == "__main__":
    for symbol, data in elements.items():
        create_3d_atomic_structure(symbol, data)
    print("All 3D atomic structures generated!")
