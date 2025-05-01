"""
Atomic Orbital Visualization System
Generates 3D scientific visualizations of atomic orbitals for all elements based on their electron configurations.
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm
from matplotlib import cm
from elements_data import elements  # Import element data containing electron configurations

def parse_electron_config(config):
    """
    Parses electron configuration string into orbital data.
    Converts notation like '4s^2 3d^2' into orbital parameters including:
    - Principal quantum number (n)
    - Orbital type (l: 0=s, 1=p, 2=d, 3=f)
    - Magnetic quantum number (m)
    - Electron count distributed across m values
    
    Args:
        config (str): Electron configuration string (e.g., '1s² 2s² 2p⁶')
    
    Returns:
        list: Dictionary of orbital parameters for each m orbital
    """
    orbitals = []
    # Remove noble gas shorthand notation (e.g., [He])
    config = re.sub(r'\[.*?\]\s*', '', config)  
    # Find all orbital matches (e.g., '3d^10' -> n=3, l=d, electrons=10)
    matches = re.findall(r'(\d)([spdf])(\^?\d+)?', config)
    
    for n, l_type, electrons in matches:
        n = int(n)
        # Convert orbital type letter to quantum number l
        l = {'s':0, 'p':1, 'd':2, 'f':3}[l_type]
        # Handle electron count (default to full orbital capacity if not specified)
        electrons = int(electrons.replace('^','')) if electrons else 2*(2*l+1)
        
        # Create separate entry for each m value (-l to +l)
        for m in range(-l, l+1):
            orbitals.append({
                'n': n,
                'l': l,
                'm': m,
                # Distribute electrons equally among m orbitals
                'electrons': electrons/(2*l+1)  
            })
    
    return orbitals

def create_scientific_orbital_image(symbol, element_data):
    """
    Creates and saves a 3D visualization of atomic orbitals for an element.
    
    Args:
        symbol (str): Element symbol (e.g., 'He')
        element_data (dict): Element data including electron configuration
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot nucleus as central red sphere
    ax.scatter([0], [0], [0], s=500, c='#FF4444', alpha=0.9)
    
    # Parse electron configuration into orbital data
    orbitals = parse_electron_config(element_data["electron_config"])
    # Color scheme for different orbital types
    colors = {'s':'#1f77b4', 'p':'#ff7f0e', 'd':'#2ca02c', 'f':'#9467bd'}
    
    # Create spherical coordinate grid for orbital visualization
    theta, phi = np.linspace(0, 2*np.pi, 100), np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    # Plot each orbital and its electrons
    for orb in orbitals:
        l, m = orb['l'], orb['m']
        n = orb['n']
        electron_count = int(orb['electrons'])
        
        # Calculate spherical harmonic function for orbital shape
        Y = sph_harm(m, l, theta, phi)
        r = np.abs(Y.real)
        # Normalize radius and scale by principal quantum number
        r = r / r.max() * n * 0.7
        
        # Convert spherical coordinates to Cartesian
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        
        # Plot orbital surface as wireframe
        ax.plot_wireframe(x, y, z, 
                        color=colors[['s','p','d','f'][l]],
                        linewidth=0.8,
                        alpha=0.7)
        
        # Add electron positions as yellow spheres
        if electron_count > 0:
            ex, ey, ez = np.array([]), np.array([]), np.array([])
            
            # s-orbital: electrons distributed in spherical shell
            if l == 0:  
                angles = np.linspace(0, 2*np.pi, max(2, electron_count))
                ex = n * 0.7 * np.cos(angles)
                ey = n * 0.7 * np.sin(angles)
                ez = np.zeros_like(ex)
            
            # p-orbital: electrons aligned along axes
            elif l == 1:  
                axis = [[1,0,0], [0,1,0], [0,0,1]][m+1]
                ex = n * 0.7 * np.array([axis[0]] * electron_count)
                ey = n * 0.7 * np.array([axis[1]] * electron_count)
                ez = n * 0.7 * np.array([axis[2]] * electron_count)
            
            # d-orbital: electrons in cloverleaf pattern
            elif l == 2:  
                angles = np.linspace(0, 2*np.pi, electron_count)
                ex = n * 0.7 * np.cos(angles)
                ey = n * 0.7 * np.sin(angles)
                ez = np.zeros_like(ex)
            
            # f-orbital: complex 3D pattern
            elif l == 3:  
                angles = np.linspace(0, 2*np.pi, electron_count)
                ex = n * 0.7 * np.cos(angles) * 0.5
                ey = n * 0.7 * np.sin(angles) * 0.5
                ez = n * 0.7 * np.cos(angles) * 0.5
            
            # Plot electron positions if coordinates were generated
            if len(ex) > 0:
                ax.scatter(ex, ey, ez, s=30, c='#FFFF00', 
                          edgecolors='#333333', alpha=0.9)

    # Set visualization parameters
    max_orb = max([o['n'] for o in orbitals], default=1)
    ax.set_xlim([-max_orb, max_orb])
    ax.set_ylim([-max_orb, max_orb])
    ax.set_zlim([-max_orb, max_orb])
    ax.view_init(elev=25, azim=45)  # Set camera angle
    ax.axis('off')  # Remove axes
    
    # Create output directory and save image
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "scientific_structures")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{symbol}_scientific.png")
    
    plt.savefig(output_path, dpi=300, transparent=True, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")

# Main execution block
if __name__ == "__main__":
    # Generate images for all elements in the periodic table data
    for symbol, data in elements.items():
        try:
            create_scientific_orbital_image(symbol, data)
        except Exception as e:
            print(f"Error generating {symbol}: {str(e)}")
    print("All orbital images generated!")
