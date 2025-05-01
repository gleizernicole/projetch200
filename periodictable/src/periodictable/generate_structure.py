import os
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm
from matplotlib import cm

def create_orbital_diagram(symbol, element_data):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot nucleus
    ax.scatter([0], [0], [0], s=500, c='#FF4444', alpha=0.9)
    
    # Get orbital data
    orbitals = parse_electron_config(element_data["electron_config"])
    colors = {'s':'#1f77b4', 'p':'#ff7f0e', 'd':'#2ca02c', 'f':'#9467bd'}
    
    # Create grid
    theta, phi = np.linspace(0, 2*np.pi, 100), np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    # Plot orbitals and electrons
    for orb in orbitals:
        l, m = orb['l'], orb['m']
        n = orb['n']
        electron_count = int(orb['electrons'])
        
        # Calculate spherical harmonic
        Y = sph_harm(m, l, theta, phi)
        r = np.abs(Y.real)
        r = r / r.max() * n * 0.7
        
        # Generate wireframe
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        
        ax.plot_wireframe(x, y, z, 
                        color=colors[['s','p','d','f'][l]],
                        linewidth=0.8,
                        alpha=0.7)
        
        # Add electrons
        if electron_count > 0:
            # Generate electron positions based on orbital type
            if l == 0:  # s-orbital
                angles = np.linspace(0, 2*np.pi, max(2, electron_count))
                ex = n * 0.7 * np.cos(angles)
                ey = n * 0.7 * np.sin(angles)
                ez = np.zeros_like(ex)
            elif l == 1:  # p-orbital
                axis = [[1,0,0], [0,1,0], [0,0,1]][m+1]
                ex = n * 0.7 * np.array([axis[0]] * electron_count)
                ey = n * 0.7 * np.array([axis[1]] * electron_count)
                ez = n * 0.7 * np.array([axis[2]] * electron_count)
            elif l == 2:  # d-orbital
                # Simplified d-orbital positions
                angles = np.linspace(0, 2*np.pi, electron_count)
                ex = n * 0.7 * np.cos(angles)
                ey = n * 0.7 * np.sin(angles)
                ez = np.zeros_like(ex)
            
            ax.scatter(ex, ey, ez, s=30, c='#FFFF00', 
                      edgecolors='#333333', alpha=0.9)

    # Visualization settings
    max_orb = max([o['n'] for o in orbitals], default=1)
    ax.set_xlim([-max_orb, max_orb])
    ax.set_ylim([-max_orb, max_orb])
    ax.set_zlim([-max_orb, max_orb])
    ax.view_init(elev=25, azim=45)
    ax.axis('off')
    
    # Save image
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "scientific_structures")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{symbol}_scientific.png")
    
    plt.savefig(output_path, dpi=300, transparent=True, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")

# Example Titanium (Ti) output:
# - 4s orbital: 2 electrons on circular wireframe
# - 3d orbitals: 2 electrons distributed on cloverleaf wireframe
# - All orbitals shown as thin colored lines
# - Electrons as yellow spheres on orbital paths

    # Generate for all elements
    if __name__ == "__main__":
        for symbol, data in elements.items():
            try:
                create_scientific_orbital_image(symbol, data)
            except Exception as e:
                print(f"Error generating {symbol}: {str(e)}")
        print("All orbital images generated!")

# Generate for all elements
    if __name__ == "__main__":
        for symbol, data in elements.items():
            create_3d_atomic_structure(symbol, data)
        print("All 3D atomic structures generated!")
