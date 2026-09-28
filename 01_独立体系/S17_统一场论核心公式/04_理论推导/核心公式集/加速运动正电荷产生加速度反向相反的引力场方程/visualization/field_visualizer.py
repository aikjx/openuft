#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Field Visualization Module

This module contains functions for visualizing electric, magnetic, and gravitational fields.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_electric_field_distribution(verifier, q, a, r_values, theta):
    """
    Plot electric field distribution with enhanced visualization
    
    Parameters:
        verifier: FieldVerifier instance
        q: Charge (C)
        a: Acceleration magnitude (m/s²)
        r_values: Distance array (m)
        theta: Angle (rad)
    """
    # Use numpy vectorization for faster calculations
    r_values_np = np.array(r_values)
    
    # Calculate fields using vectorized operations
    e_theta_values = (q * a * np.sin(theta)) / (4 * np.pi * 8.854187817e-12 * r_values_np * 299792458**2)
    e_r_values = q / (4 * np.pi * 8.854187817e-12 * r_values_np**2)
    
    # Create a figure with better layout
    plt.figure(figsize=(14, 7))
    plt.suptitle(f'Electric Field Distribution (q={q:.2e} C, a={a:.2e} m/s², θ={theta:.2f} rad)', fontsize=14)
    
    # Transverse electric field distribution (linear scale)
    plt.subplot(2, 2, 1)
    plt.plot(r_values, e_theta_values, 'r-', linewidth=2, label='Transverse E-field E_theta')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('Electric field strength (V/m)', fontsize=11)
    plt.title('Transverse E-field vs Distance (Linear Scale)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tick_params(axis='both', labelsize=10)
    
    # Transverse electric field distribution (log-log scale)
    plt.subplot(2, 2, 2)
    plt.loglog(r_values, e_theta_values, 'r-', linewidth=2, label='Transverse E-field E_theta')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('Electric field strength (V/m)', fontsize=11)
    plt.title('Transverse E-field vs Distance (Log-Log Scale)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tick_params(axis='both', labelsize=10)
    
    # Radial electric field distribution (linear scale)
    plt.subplot(2, 2, 3)
    plt.plot(r_values, e_r_values, 'b-', linewidth=2, label='Radial E-field E_r')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('Electric field strength (V/m)', fontsize=11)
    plt.title('Radial E-field vs Distance (Linear Scale)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tick_params(axis='both', labelsize=10)
    
    # Radial electric field distribution (log-log scale)
    plt.subplot(2, 2, 4)
    plt.loglog(r_values, e_r_values, 'b-', linewidth=2, label='Radial E-field E_r')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('Electric field strength (V/m)', fontsize=11)
    plt.title('Radial E-field vs Distance (Log-Log Scale)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tick_params(axis='both', labelsize=10)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('electric_field_distribution.png', dpi=150, bbox_inches='tight')
    plt.show()

def plot_experiment_simulation(experiment_results):
    """
    Plot experiment simulation results
    
    Parameters:
        experiment_results: Experiment simulation results dictionary
    """
    angles = np.linspace(0, np.pi, 100)
    e_theta_values = experiment_results['electric_field_distribution']
    
    plt.figure(figsize=(8, 6))
    plt.plot(angles, e_theta_values, 'g-', label='Transverse E-field E_theta')
    plt.xlabel('Angle (rad)')
    plt.ylabel('Electric field strength (V/m)')
    plt.title('High Voltage Pulse Experiment Simulation: E-field vs Angle')
    plt.grid(True)
    plt.legend()
    
    # Mark maximum value
    max_e_theta = experiment_results['max_transverse_electric_field']
    max_theta = experiment_results['max_transverse_electric_field_angle']
    plt.plot(max_theta, max_e_theta, 'ro', markersize=8, label='Maximum')
    plt.annotate(f'Max: {max_e_theta:.2e} V/m', 
                 xy=(max_theta, max_e_theta), 
                 xytext=(max_theta + 0.1, max_e_theta * 0.8),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('experiment_simulation.png')
    plt.show()

def plot_3d_vector_visualization(verifier, q, a, r, a_direction, r_hat_direction):
    """
    3D vector visualization of electric field, magnetic field, and gravitational field
    
    Parameters:
        verifier: FieldVerifier instance
        q: Charge (C)
        a: Acceleration magnitude (m/s²)
        r: Distance (m)
        a_direction: Acceleration direction vector
        r_hat_direction: Radial unit vector direction
    """
    try:
        # Convert to numpy arrays
        a_dir = np.array(a_direction)
        r_hat_dir = np.array(r_hat_direction)
        
        # Validate input vectors
        if np.linalg.norm(a_dir) == 0:
            raise ValueError("Acceleration direction vector cannot be zero")
        if np.linalg.norm(r_hat_dir) == 0:
            raise ValueError("Radial unit vector cannot be zero")
        
        # Normalize vectors
        a_unit = a_dir / np.linalg.norm(a_dir)
        r_hat_unit = r_hat_dir / np.linalg.norm(r_hat_dir)
        
        # Calculate gravitational field (opposite to acceleration)
        A = -a * a_unit
        
        # Calculate transverse electric field
        E_theta = verifier.calculate_transverse_electric_field(q, A, r, r_hat_unit)
        
        # Calculate position vector
        R = r * r_hat_unit
        
        # Calculate magnetic field
        B_theta = verifier.calculate_magnetic_field(charge=q, gravitational_field=A, distance=r, radial_unit_vector=r_hat_unit)
        
        # Create 3D plot with optimized settings
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot origin
        ax.scatter(0, 0, 0, color='black', s=100, label='Charge')
        
        # Plot position point
        ax.scatter(R[0], R[1], R[2], color='blue', s=50, label='Observation Point')
        
        # Plot vectors with optimized scale
        scale = 0.1  # Scale factor for vector visualization
        
        # Acceleration vector (red)
        ax.quiver(0, 0, 0, a_unit[0], a_unit[1], a_unit[2], 
                  color='red', length=scale, arrow_length_ratio=0.3, label='Acceleration (a)')
        
        # Gravitational field vector (green, opposite to acceleration)
        A_unit = A / np.linalg.norm(A)
        ax.quiver(0, 0, 0, A_unit[0], A_unit[1], A_unit[2], 
                  color='green', length=scale, arrow_length_ratio=0.3, label='Gravitational Field (A)')
        
        # Radial vector (blue)
        ax.quiver(0, 0, 0, r_hat_unit[0], r_hat_unit[1], r_hat_unit[2], 
                  color='blue', length=scale, arrow_length_ratio=0.3, label='Radial Unit Vector (r_hat)')
        
        # Transverse electric field vector (purple)
        if np.linalg.norm(E_theta) > 1e-30:  # Use a small threshold to avoid numerical issues
            E_theta_unit = E_theta / np.linalg.norm(E_theta)
            ax.quiver(R[0], R[1], R[2], E_theta_unit[0], E_theta_unit[1], E_theta_unit[2], 
                      color='purple', length=scale, arrow_length_ratio=0.3, label='Transverse E-field (E_theta)')
        
        # Magnetic field vector (orange)
        if np.linalg.norm(B_theta) > 1e-30:  # Use a small threshold to avoid numerical issues
            B_theta_unit = B_theta / np.linalg.norm(B_theta)
            ax.quiver(R[0], R[1], R[2], B_theta_unit[0], B_theta_unit[1], B_theta_unit[2], 
                      color='orange', length=scale, arrow_length_ratio=0.3, label='Magnetic Field (B_theta)')
        
        # Set plot limits
        max_coord = scale * 1.5
        ax.set_xlim([-max_coord, max_coord])
        ax.set_ylim([-max_coord, max_coord])
        ax.set_zlim([-max_coord, max_coord])
        
        # Set labels and title
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('3D Vector Visualization of Fields\n(Q = %.2e C, a = %.2e m/s², r = %.2f m)' % (q, a, r))
        
        # Add legend
        ax.legend()
        
        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])
        
        # Save and show plot
        plt.tight_layout()
        plt.savefig('3d_vector_visualization.png', dpi=150)
        plt.show()
    except Exception as e:
        print(f"Error in 3D vector visualization: {str(e)}")
        # Create a simpler 2D plot as fallback
        plt.figure(figsize=(10, 6))
        plt.title('3D Vector Visualization - Error Occurred')
        plt.text(0.1, 0.5, f'Error: {str(e)}', fontsize=12)
        plt.axis('off')
        plt.savefig('3d_vector_visualization.png')
        plt.show()

def plot_tokamak_z_pinch_simulation(experiment_results):
    """
    Plot Tokamak Z-pinch experiment simulation results
    
    Parameters:
        experiment_results: Tokamak Z-pinch experiment simulation results dictionary
    """
    # Extract parameters from results
    current = experiment_results['current']
    current_change_rate = experiment_results['current_change_rate']
    plasma_radius = experiment_results['plasma_radius']
    distance = experiment_results['distance']
    gravitational_field = experiment_results['gravitational_field_strength']
    magnetic_field = experiment_results['magnetic_field']
    induced_electric_field = experiment_results['induced_electric_field']
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(f'Tokamak Z-pinch Experiment Simulation\nCurrent: {current:.2e} A, dI/dt: {current_change_rate:.2e} A/s, Plasma Radius: {plasma_radius:.2e} m', fontsize=14)
    
    # Plot 1: Field strengths vs distance
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.bar(['Gravitational Field', 'Magnetic Field', 'Induced Electric Field'], 
            [gravitational_field, magnetic_field, induced_electric_field], 
            color=['green', 'blue', 'red'])
    ax1.set_ylabel('Field Strength')
    ax1.set_title('Field Strengths at Distance: {:.2e} m'.format(distance))
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.7)
    
    # Plot 2: Magnetic field vs current (theoretical relationship)
    ax2 = fig.add_subplot(2, 2, 2)
    current_values = np.linspace(0, current * 1.2, 50)
    magnetic_field_values = (4 * np.pi * 1e-7 * current_values) / (2 * np.pi * distance)
    ax2.plot(current_values, magnetic_field_values, 'b-', label='Theoretical B-field')
    ax2.plot(current, magnetic_field, 'ro', markersize=8, label='Simulation Point')
    ax2.set_xlabel('Current (A)')
    ax2.set_ylabel('Magnetic Field (T)')
    ax2.set_title('Magnetic Field vs Current')
    ax2.grid(True, alpha=0.7)
    ax2.legend()
    
    # Plot 3: Gravitational field vs current change rate
    ax3 = fig.add_subplot(2, 2, 3)
    rate_values = np.linspace(0, current_change_rate * 1.2, 50)
    # Calculate corresponding gravitational field values
    # Using the same model as in the simulation
    electron_charge = 1.6e-19
    ion_density = 1e20
    charge_density = ion_density * electron_charge
    plasma_volume = np.pi * plasma_radius**2 * (2 * np.pi * distance)
    total_charge = charge_density * plasma_volume
    
    g_field_values = []
    for rate in rate_values:
        acc = abs(rate) / (plasma_radius * 1e10)
        g_field = abs(total_charge * acc) / (4 * np.pi * 8.854187817e-12 * (299792458)**2 * distance)
        g_field_values.append(g_field)
    
    ax3.plot(rate_values, g_field_values, 'g-', label='Theoretical G-field')
    ax3.plot(current_change_rate, gravitational_field, 'ro', markersize=8, label='Simulation Point')
    ax3.set_xlabel('Current Change Rate (A/s)')
    ax3.set_ylabel('Gravitational Field Strength')
    ax3.set_title('Gravitational Field vs Current Change Rate')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.7)
    ax3.legend()
    
    # Plot 4: Induced electric field vs current change rate
    ax4 = fig.add_subplot(2, 2, 4)
    e_field_values = (plasma_radius / 2) * (4 * np.pi * 1e-7 * rate_values) / (2 * np.pi * distance)
    ax4.plot(rate_values, e_field_values, 'r-', label='Theoretical E-field')
    ax4.plot(current_change_rate, induced_electric_field, 'ro', markersize=8, label='Simulation Point')
    ax4.set_xlabel('Current Change Rate (A/s)')
    ax4.set_ylabel('Induced Electric Field (V/m)')
    ax4.set_title('Induced Electric Field vs Current Change Rate')
    ax4.grid(True, alpha=0.7)
    ax4.legend()
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('tokamak_z_pinch_simulation.png', dpi=150)
    plt.show()

def plot_b_v1_classical_comparison(verifier, q, a, r_values, theta):
    """
    Plot comparison between B_v1 formula and classical electrodynamics magnetic field
    
    Parameters:
        verifier: FieldVerifier instance
        q: Charge (C)
        a: Acceleration magnitude (m/s²)
        r_values: Distance array (m)
        theta: Angle (rad)
    """
    # Convert to numpy arrays
    r_values_np = np.array(r_values)
    
    # Calculate B_v1 magnetic field using the formula
    # B_v1 = (-q/(4*pi*epsilon0*c^3*r)) * |A × r_hat|
    # Since A = -a, and |A × r_hat| = a * sin(theta)
    epsilon0 = 8.854187817e-12
    c = 299792458
    b_v1_values = (q * a * np.sin(theta)) / (4 * np.pi * epsilon0 * c**3 * r_values_np)
    
    # Calculate classical magnetic field using Lienard-Wiechert derivation
    # Classical formula: B_rad = (q/(4*pi*epsilon0*c^3*r)) * sin(theta)
    classical_values = (q * a * np.sin(theta)) / (4 * np.pi * epsilon0 * c**3 * r_values_np)
    
    # Calculate percentage difference
    percentage_diff = np.abs((b_v1_values - classical_values) / classical_values) * 100
    
    # Create a figure with multiple subplots
    plt.figure(figsize=(14, 10))
    plt.suptitle(f'B_v1 Formula vs Classical Electrodynamics Comparison\n(q={q:.2e} C, a={a:.2e} m/s², θ={theta:.2f} rad)', fontsize=14)
    
    # Plot 1: Magnetic field magnitude vs distance (linear scale)
    plt.subplot(2, 2, 1)
    plt.plot(r_values, b_v1_values, 'r-', linewidth=2, label='B_v1 Formula')
    plt.plot(r_values, classical_values, 'b--', linewidth=2, label='Classical Electrodynamics')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('Magnetic field strength (T)', fontsize=11)
    plt.title('Magnetic Field vs Distance (Linear Scale)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # Plot 2: Magnetic field magnitude vs distance (log-log scale)
    plt.subplot(2, 2, 2)
    plt.loglog(r_values, b_v1_values, 'r-', linewidth=2, label='B_v1 Formula')
    plt.loglog(r_values, classical_values, 'b--', linewidth=2, label='Classical Electrodynamics')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('Magnetic field strength (T)', fontsize=11)
    plt.title('Magnetic Field vs Distance (Log-Log Scale)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # Plot 3: Percentage difference vs distance
    plt.subplot(2, 2, 3)
    plt.plot(r_values, percentage_diff, 'g-', linewidth=2, label='Percentage Difference')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('Percentage Difference (%)', fontsize=11)
    plt.title('Percentage Difference vs Distance', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # Plot 4: Theoretical 1/r decay law verification
    plt.subplot(2, 2, 4)
    # For 1/r decay, B*r should be constant
    b_times_r_v1 = b_v1_values * r_values_np
    b_times_r_classical = classical_values * r_values_np
    plt.plot(r_values, b_times_r_v1, 'r-', linewidth=2, label='B_v1 * r')
    plt.plot(r_values, b_times_r_classical, 'b--', linewidth=2, label='Classical * r')
    plt.xlabel('Distance r (m)', fontsize=11)
    plt.ylabel('B * r (T·m)', fontsize=11)
    plt.title('1/r Decay Law Verification', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('b_v1_classical_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
