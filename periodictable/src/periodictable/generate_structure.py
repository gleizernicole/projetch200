import os
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm
from matplotlib import cm
from elements_data import elements

# Orbital configuration parser
def parse_electron_config(config):
    orbitals = []
    config = re.sub(r'\[.*?\]\s*', '', config)  # Remove noble gas notation
    matches = re.findall(r'(\d)([spdf])(\^?\d+)?', config)
    
    for n, l_type, electrons in matches:
        n = int(n)
        l = {'s':0, 'p':1, 'd':2, 'f':3}[l_type]
        electrons = int(electrons.replace('^','')) if electrons else 2*(2*l+1)
        
        # Handle different m values
        for m in range(-l, l+1):
            orbitals.append({
                'n': n,
                'l': l,
                'm': m,
                'electrons': electrons/(2*l+1)  # Distribute electrons across m values
            })
    
    return orbitals

# Scientific visualization function
def create_scientific_orbital_image(symbol, element_data):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot nucleus
    ax.scatter([0], [0], [0], s=1000, c='#FF4444', alpha=0.9)
    
    # Get orbital data
    orbitals = parse_electron_config(element_data["electron_config"])
    colors = {'s':'#1f77b4', 'p':'#ff7f0e', 'd':'#2ca02c', 'f':'#9467bd'}
    
    # Create grid
    theta, phi = np.linspace(0, 2*np.pi, 100), np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    # Plot each orbital component
    for orb in orbitals:
        l, m = orb['l'], orb['m']
        n = orb['n']
        
        # Calculate spherical harmonic
        Y = sph_harm(m, l, theta, phi)
        r = np.abs(Y.real)
        
        # Normalize and scale
        r = r / r.max() * n * 0.7
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        
        # Color and opacity based on orbital type
        color = colors[['s','p','d','f'][orb['l']]]
        alpha = min(0.3 + 0.1*orb['electrons'], 0.7)
        
        ax.plot_surface(x, y, z,
                      color=color,
                      alpha=alpha,
                      shade=False,
                      antialiased=True,
                      rcount=40, 
                      ccount=40)

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
