import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm
from matplotlib import cm

def create_scientific_orbital_image(symbol, element_data):
    # Create 3D figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Atomic properties
    atomic_number = element_data["num"]
    electrons = atomic_number
    
    # Plot nucleus
    ax.scatter([0], [0], [0], s=700, c='#FF4444', alpha=0.9, label='Nucleus')
    
    # Create orbital grid
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    # Calculate spherical harmonics for different orbitals
    orbitals = {
        '1s': {'n': 1, 'l': 0, 'm': 0, 'color': '#1f77b4'},
        '2p': {'n': 2, 'l': 1, 'm': 0, 'color': '#ff7f0e'},
        '3d': {'n': 3, 'l': 2, 'm': 0, 'color': '#2ca02c'}
    }
    
    # Plot orbitals based on electron configuration
    for orb in orbitals.values():
        # Radial wavefunction component
        r = np.abs(sph_harm(orb['m'], orb['l'], theta, phi).real
        
        # Scale for visualization
        x = r * np.sin(phi) * np.cos(theta) * (orb['n'] * 0.8)
        y = r * np.sin(phi) * np.sin(theta) * (orb['n'] * 0.8)
        z = r * np.cos(phi) * (orb['n'] * 0.8)
        
        # Plot surface
        ax.plot_surface(x, y, z, 
                      color=orb['color'],
                      alpha=0.4,
                      antialiased=True,
                      shade=False)

    # Visualization settings
    ax.set_axis_off()
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-4, 4])
    ax.view_init(elev=25, azim=45)
    
    # Save image
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "scientific_structures")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{symbol}_scientific.png")
    
    plt.savefig(output_path, dpi=300, transparent=True, bbox_inches='tight')
    plt.close()
    print(f"Generated scientific image: {output_path}")

# Generate images for first 18 elements
if __name__ == "__main__":
    elements_to_generate = {k: v for k, v in elements.items() if v["num"] <= 18}
    for symbol, data in elements_to_generate.items():
        create_scientific_orbital_image(symbol, data)
    print(f"Generated 3D structure: {output_path}")

# Generate for all elements
if __name__ == "__main__":
    for symbol, data in elements.items():
        create_3d_atomic_structure(symbol, data)
    print("All 3D atomic structures generated!")
