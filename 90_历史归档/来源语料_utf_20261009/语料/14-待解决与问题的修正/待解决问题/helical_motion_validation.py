import numpy as np
import matplotlib
matplotlib.use(\'Agg\')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
c = 3.0e8  # Speed of light in m/s

def validate_helical_motion(R, omega, t):
    """
    Validate the helical motion equation and velocity constraint
    
    Parameters:
    R : float - Radius of helix in meters
    omega : float - Angular velocity in rad/s
    t : float - Time in seconds
    
    Returns:
    dict - Validation results including position, velocity, and magnitude
    """
    # Calculate axial velocity
    v_z = c * np.sqrt(1 - (R * omega / c)**2)
    
    # Position vector components
    x = R * np.cos(omega * t)
    y = R * np.sin(omega * t)
    z = v_z * t
    
    # Velocity vector components (derivative of position)
    vx = -R * omega * np.sin(omega * t)
    vy = R * omega * np.cos(omega * t)
    vz = v_z
    
    # Calculate velocity magnitude
    v_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
    
    # Calculate theoretical velocity magnitude (should be c)
    theoretical_v = c
    
    # Calculate error
    error = np.abs(v_magnitude - theoretical_v)
    
    return {
        'position': (x, y, z),
        'velocity': (vx, vy, vz),
        'v_magnitude': v_magnitude,
        'theoretical_v': theoretical_v,
        'error': error,
        'v_z': v_z,
        'R_omega': R * omega,
        't': t
    }

def plot_helical_motion(R, omega, duration=1.0, steps=100):
    """
    Plot the helical motion trajectory
    
    Parameters:
    R : float - Radius of helix
    omega : float - Angular velocity
    duration : float - Total time for plot
    steps : int - Number of steps in plot
    """
    t_values = np.linspace(0, duration, steps)
    x_values = []
    y_values = []
    z_values = []
    v_magnitudes = []
    
    for t in t_values:
        result = validate_helical_motion(R, omega, t)
        x, y, z = result['position']
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)
        v_magnitudes.append(result['v_magnitude'])
    
    # Create 3D plot of helical motion
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 3D trajectory
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot(x_values, y_values, z_values, 'b-', linewidth=2)
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_title('3D Helical Motion Trajectory')
    ax1.grid(True)
    
    # Plot velocity magnitude over time
    ax2 = fig.add_subplot(222)
    ax2.plot(t_values, v_magnitudes, 'r-', linewidth=2)
    ax2.axhline(y=c, color='g', linestyle='--', label=f'Theoretical c = {c:.2e} m/s')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity Magnitude (m/s)')
    ax2.set_title('Velocity Magnitude Over Time')
    ax2.legend()
    ax2.grid(True)
    
    # Plot XY projection (circular motion)
    ax3 = fig.add_subplot(223)
    ax3.plot(x_values, y_values, 'm-', linewidth=2)
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Y (m)')
    ax3.set_title('XY Projection (Circular Motion)')
    ax3.grid(True)
    ax3.set_aspect('equal')
    
    # Plot Z vs Time (linear motion)
    ax4 = fig.add_subplot(224)
    ax4.plot(t_values, z_values, 'c-', linewidth=2)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Z Position (m)')
    ax4.set_title('Z Position Over Time (Linear Motion)')
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('helical_motion_validation.png', dpi=150, bbox_inches='tight')
    plt.show()

def run_comprehensive_validation():
    """
    Run comprehensive validation with different parameters
    """
    print("=== Space Helical Motion Validation ===")
    print("=" * 50)
    
    # Test cases with different parameters
    test_cases = [
        {"R": 1.0, "omega": 1.0e6},
        {"R": 0.5, "omega": 2.0e6},
        {"R": 2.0, "omega": 5.0e5},
        {"R": 1.0, "omega": 1.5e6},
    ]
    
    for i, case in enumerate(test_cases, 1):
        R = case["R"]
        omega = case["omega"]
        
        print(f"/nTest Case {i}: R = {R} m, ω = {omega:.2e} rad/s")
        print("-" * 30)
        
        # Calculate v_z
        v_z = c * np.sqrt(1 - (R * omega / c)**2)
        print(f"Calculated v_z: {v_z:.2e} m/s")
        
        # Calculate rω
        R_omega = R * omega
        print(f"rω: {R_omega:.2e} m/s")
        
        # Validate at multiple time points
        for t in [0.0, 0.1, 0.5, 1.0]:
            result = validate_helical_motion(R, omega, t)
            print(f"t = {t} s: |v| = {result['v_magnitude']:.2e} m/s, Error = {result['error']:.2e} m/s")
        
        # Check if velocity constraint is satisfied
        if np.isclose(result['v_magnitude'], c, rtol=1e-10):
            print("✓ Velocity constraint |v| = c is satisfied!")
        else:
            print("✗ Velocity constraint |v| = c is NOT satisfied!")
    
    print("/n" + "=" * 50)
    print("Validation completed!")

if __name__ == "__main__":
    # Run comprehensive validation
    run_comprehensive_validation()
    
    # Plot helical motion for a specific case
    print("/nGenerating helical motion plot...")
    plot_helical_motion(R=1.0, omega=1.0e6, duration=1.0, steps=200)
    
    print("All validation tasks completed!")