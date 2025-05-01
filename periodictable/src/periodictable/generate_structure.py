import os
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm
from matplotlib import cm
from elements_data import elements

# Enhanced orbital configuration parser
def parse_electron_config(config):
    orbitals = []
    config = re.sub(r'\[.*?\]\s*', '', config)  # Remove noble gas notation
    pattern = r'(\d{1,2})([spdf])(\^{0,1})(\d{1,2})|(\[[A-Z][a-z]+\])'
    matches = re.findall(pattern, config)
    
    for match in matches:
        if match[4]:  # Skip noble gas notation
            continue
        n = int(match[0])
        l = {'s':0, 'p':1, 'd':2, 'f':3}[match[1]]
        electrons = int(match[3]) if match[3] else 2*(2*l+1)
        
        # Relativistic correction for heavy elements
        if n >= 6 and l == 2:  # 6d orbitals
            n -= 0.4  # Adjust for relativistic contraction
        
        # Distribute electrons across m values
        for m in range(-l, l+1):
            orbitals.append({
                'n': n,
                'l': l,
                'm': m,
                'electrons': electrons/(2*l+1)
            })
    
    return orbitals

def create_scientific_orbital_image(symbol, element_data):
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
        
        # Relativistic scaling factor
        if element_data["num"] > 88:
            scale_factor = 0.7 * (1 - (element_data["num"] - 88)/50)
        else:
            scale_factor = 0.7
        
        r = r / r.max() * n * scale_factor
        
        # Generate wireframe with m-value colors
        m_colors = {
            -2: '#004d00', -1: '#008000',
            0: '#00b300', 1: '#00e600',
            2: '#1aff1a'
        } if l == 2 else colors[['s','p','d','f'][l]]
        
        ax.plot_wireframe(
            r * np.sin(phi) * np.cos(theta),
            r * np.sin(phi) * np.sin(theta),
            r * np.cos(phi),
            color=m_colors if isinstance(m_colors, str) else m_colors[m],
            linewidth=0.8,
            alpha=0.7
        )
        
        # Add electrons with position variation
        if electron_count > 0:
            ex, ey, ez = np.array([]), np.array([]), np.array([])
            
            if l == 0:  # s-orbital
                angles = np.linspace(0, 2*np.pi, max(2, electron_count))
                ex = n * scale_factor * np.cos(angles)
                ey = n * scale_factor * np.sin(angles)
                ez = np.zeros_like(ex)
            
            elif l == 1:  # p-orbital
                axis = [[1,0,0], [0,1,0], [0,0,1]][m+1]
                ex = n * scale_factor * np.array([axis[0]] * electron_count)
                ey = n * scale_factor * np.array([axis[1]] * electron_count)
                ez = n * scale_factor * np.array([axis[2]] * electron_count)
            
            elif l == 2:  # d-orbital
                # Electron count-specific positioning
                if electron_count == 1:
                    angles = [np.pi/2]
                elif electron_count == 2:
                    angles = [0, np.pi]
                elif electron_count == 3:
                    angles = [0, 2*np.pi/3, 4*np.pi/3]
                elif electron_count == 4:
                    angles = [0, np.pi/2, np.pi, 3*np.pi/2]
                elif electron_count == 5:
                    angles = np.linspace(0, 2*np.pi, 5)
                else:
                    angles = np.linspace(0, 2*np.pi, electron_count)
                
                ex = n * scale_factor * np.cos(angles)
                ey = n * scale_factor * np.sin(angles)
                ez = np.zeros_like(ex)
            
            elif l == 3:  # f-orbital
                angles = np.linspace(0, 2*np.pi, electron_count)
                ex = n * scale_factor * np.cos(angles) * 0.5
                ey = n * scale_factor * np.sin(angles) * 0.5
                ez = n * scale_factor * np.cos(angles) * 0.5
            
            # Add electron repulsion effect
            if len(ex) > 1:
                for i in range(len(ex)):
                    for j in range(i+1, len(ex)):
                        dx = ex[j] - ex[i]
                        dy = ey[j] - ey[i]
                        dz = ez[j] - ez[i]
                        distance = np.sqrt(dx**2 + dy**2 + dz**2)
                        if distance < 0.5:
                            adjust = 0.1 * (0.5 - distance)
                            ex[j] += adjust * dx/distance
                            ey[j] += adjust * dy/distance
                            ez[j] += adjust * dz/distance
            
            if len(ex) > 0:
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
        create_scientific_orbital_image(symbol, data)
    print("All 3D atomic structures generated!")
