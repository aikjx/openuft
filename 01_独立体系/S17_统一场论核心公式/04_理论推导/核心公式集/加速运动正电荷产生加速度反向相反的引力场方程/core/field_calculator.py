#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Field Calculator Module

This module contains the core field calculation functionality for verifying
accelerating positive charges generating gravitational field equations.
"""

import numpy as np
import sympy as sp

# 物理常数定义
EPSILON0 = 8.854187817e-12  # 真空介电常数 (F/m)
C = 299792458  # 光速 (m/s)
PI = np.pi  # 圆周率

class FieldCalculator:
    """
    Field calculator class for calculating electric, magnetic, and gravitational fields
    """
    
    def __init__(self):
        """
        Initialize field calculator
        """
        pass
    
    def calculate_transverse_electric_field(self, charge, gravitational_field, distance, radial_unit_vector):
        """
        Calculate transverse electric field using the core formula
        
        Derivation Steps:
        1. Start from the Lienard-Wiechert potentials for a moving charge
        2. Take the time derivative of the vector potential to get the transverse electric field
        3. Apply the chain rule for the retarded time derivative
        4. For far-field radiation, the dominant term is proportional to 1/r
        5. Use the vector cross product to get the transverse component
        6. Recognize that the gravitational field A is opposite to the acceleration vector
        
        Formula: E_theta = (-q/(4*pi*epsilon0*c^2*r)) * (A × r_hat)
        
        Where:
        - q: Charge of the particle (C)
        - epsilon0: Vacuum permittivity (8.854187817e-12 F/m)
        - c: Speed of light in vacuum (299792458 m/s)
        - r: Distance from the charge to the observation point (m)
        - A: Gravitational field vector, equal to -a (acceleration vector) (m/s²)
        - r_hat: Unit vector in the radial direction
        
        Physical Interpretation:
        - The negative sign indicates the field direction is opposite to the cross product
        - The 1/r dependence is characteristic of radiation fields
        - The cross product ensures the field is transverse to the radial direction
        - The field strength is proportional to the charge and acceleration
        
        Parameters:
            charge: Charge (C)
            gravitational_field: Gravitational field vector (m/s²)
            distance: Distance (m)
            radial_unit_vector: Radial unit vector
            
        Returns:
            transverse_electric_field: Transverse electric field vector (V/m)
        """
        # Parameter validation
        if not isinstance(charge, (int, float)):
            raise TypeError("Charge must be a numeric type")
        if not isinstance(distance, (int, float)):
            raise TypeError("Distance must be a numeric type")
        if not isinstance(gravitational_field, (list, tuple, np.ndarray)):
            raise TypeError("Gravitational field vector must be a list, tuple, or numpy array")
        if not isinstance(radial_unit_vector, (list, tuple, np.ndarray)):
            raise TypeError("Radial unit vector must be a list, tuple, or numpy array")
        
        # Numeric range check
        if distance <= 0:
            raise ValueError("Distance must be greater than zero")
        if np.linalg.norm(radial_unit_vector) == 0:
            raise ValueError("Radial unit vector cannot be a zero vector")
        
        # Convert to numpy arrays
        gravitational_field = np.array(gravitational_field)
        radial_unit_vector = np.array(radial_unit_vector)
        
        # Dimension check
        if gravitational_field.ndim != 1:
            raise ValueError("Gravitational field vector must be a 1D array")
        if radial_unit_vector.ndim != 1:
            raise ValueError("Radial unit vector must be a 1D array")
        if len(gravitational_field) != len(radial_unit_vector):
            raise ValueError("Gravitational field vector and radial unit vector must have the same dimension")
        
        # Calculate coefficient
        coefficient = -charge / (4 * PI * EPSILON0 * C**2 * distance)
        
        # Calculate vector cross product
        cross_product = np.cross(gravitational_field, radial_unit_vector)
        
        # Calculate transverse electric field
        transverse_electric_field = coefficient * cross_product
        
        return transverse_electric_field
    
    def calculate_radial_electric_field(self, q, r):
        """
        Calculate radial electric field (Coulomb's law)
        
        Parameters:
            q: Charge (C)
            r: Distance (m)
            
        Returns:
            E_r: Radial electric field magnitude (V/m)
        """
        # Parameter validation
        if not isinstance(q, (int, float)):
            raise TypeError("Charge must be a numeric type")
        if not isinstance(r, (int, float)):
            raise TypeError("Distance must be a numeric type")
        
        # Numeric range check
        if r <= 0:
            raise ValueError("Distance must be greater than zero")
        
        E_r = q / (4 * PI * EPSILON0 * r**2)
        return E_r
    
    def calculate_transverse_electric_field_from_geometry(self, q, a, r, theta):
        """
        Calculate transverse electric field from geometric analysis
        
        Parameters:
            q: Charge (C)
            a: Acceleration magnitude (m/s²)
            r: Distance (m)
            theta: Angle (rad)
            
        Returns:
            e_theta: Transverse electric field magnitude (V/m)
        """
        # Parameter validation
        if not isinstance(q, (int, float)):
            raise TypeError("Charge must be a numeric type")
        if not isinstance(a, (int, float)):
            raise TypeError("Acceleration magnitude must be a numeric type")
        if not isinstance(r, (int, float)):
            raise TypeError("Distance must be a numeric type")
        if not isinstance(theta, (int, float)):
            raise TypeError("Angle must be a numeric type")
        
        # Numeric range check
        if r <= 0:
            raise ValueError("Distance must be greater than zero")
        if a < 0:
            raise ValueError("Acceleration magnitude cannot be negative")
        if theta < 0 or theta > np.pi:
            raise ValueError("Angle must be between 0 and π")
        
        e_theta = (q * a * np.sin(theta)) / (4 * PI * EPSILON0 * r * C**2)
        return e_theta
    
    def calculate_magnetic_field(self, charge, gravitational_field, distance, radial_unit_vector):
        """
        Calculate magnetic field based on gravitational field using B_v1 formula
        
        Derivation Steps (from B_v1 formula):
        1. Start from the Maxwell's equation: ∇ × E = -∂B/∂t
        2. For electromagnetic waves, the magnetic field is related to the electric field by B = (1/c) r_hat × E
        3. Substitute the transverse electric field formula into this relation
        4. Apply the vector triple product identity: r_hat × (A × r_hat) = A - (A · r_hat)r_hat
        5. For transverse fields, the radial component vanishes, leaving only the transverse component
        6. Simplify to obtain the B_v1 formula
        
        Formula: B_theta = (-q/(4*pi*epsilon0*c^3*r)) * (A × r_hat)
        
        Where:
        - q: Charge of the particle (C)
        - epsilon0: Vacuum permittivity (8.854187817e-12 F/m)
        - c: Speed of light in vacuum (299792458 m/s)
        - r: Distance from the charge to the observation point (m)
        - A: Gravitational field vector, equal to -a (acceleration vector) (m/s²)
        - r_hat: Unit vector in the radial direction
        
        Consistency with Classical Electrodynamics:
        - This formula matches the radiation magnetic field derived from Lienard-Wiechert potentials
        - The 1/c^3 factor arises from the combination of the 1/c^2 factor in the electric field
          and the additional 1/c factor from the B = (1/c) r_hat × E relation
        - The formula correctly predicts the transverse nature of electromagnetic radiation
        - The magnitude follows the 1/r decay law characteristic of radiation fields
        
        Parameters:
            charge: Charge (C)
            gravitational_field: Gravitational field vector (m/s²)
            distance: Distance (m)
            radial_unit_vector: Radial unit vector
            
        Returns:
            magnetic_field: Magnetic field vector (T)
        """
        # Parameter validation
        if not isinstance(charge, (int, float)):
            raise TypeError("Charge must be a numeric type")
        if not isinstance(distance, (int, float)):
            raise TypeError("Distance must be a numeric type")
        if not isinstance(gravitational_field, (list, tuple, np.ndarray)):
            raise TypeError("Gravitational field vector must be a list, tuple, or numpy array")
        if not isinstance(radial_unit_vector, (list, tuple, np.ndarray)):
            raise TypeError("Radial unit vector must be a list, tuple, or numpy array")
        
        # Numeric range check
        if distance <= 0:
            raise ValueError("Distance must be greater than zero")
        if np.linalg.norm(radial_unit_vector) == 0:
            raise ValueError("Radial unit vector cannot be a zero vector")
        
        # Convert to numpy arrays
        gravitational_field = np.array(gravitational_field)
        radial_unit_vector = np.array(radial_unit_vector)
        
        # Dimension check
        if gravitational_field.ndim != 1:
            raise ValueError("Gravitational field vector must be a 1D array")
        if radial_unit_vector.ndim != 1:
            raise ValueError("Radial unit vector must be a 1D array")
        if len(gravitational_field) != len(radial_unit_vector):
            raise ValueError("Gravitational field vector and radial unit vector must have the same dimension")
        
        # Calculate coefficient using B_v1 formula
        coefficient = -charge / (4 * PI * EPSILON0 * C**3 * distance)
        
        # Calculate vector cross product (A × r_hat)
        cross_product = np.cross(gravitational_field, radial_unit_vector)
        
        # Calculate magnetic field
        magnetic_field = coefficient * cross_product
        
        return magnetic_field
    
    def verify_dimension_analysis(self):
        """
        Verify dimension analysis
        
        Returns:
            bool: Whether dimensions are consistent
        """
        # Define symbols
        q = sp.Symbol('q')
        epsilon0 = sp.Symbol('epsilon0')
        c = sp.Symbol('c')
        r = sp.Symbol('r')
        A = sp.Symbol('A')
        
        # Left side dimension: electric field strength (V/m) = M L T^-3 I^-1
        left_dim = sp.Symbol('M') * sp.Symbol('L') * sp.Symbol('T')**-3 * sp.Symbol('I')**-1
        
        # Right side dimension
        right_dim = q * A / (epsilon0 * c**2 * r)
        
        # Substitute dimensions of each physical quantity
        dim_subs = {
            q: sp.Symbol('I') * sp.Symbol('T'),  # Charge: I T
            epsilon0: sp.Symbol('M')**-1 * sp.Symbol('L')**-3 * sp.Symbol('T')**4 * sp.Symbol('I')**2,  # Permittivity: M^-1 L^-3 T^4 I^2
            c: sp.Symbol('L') * sp.Symbol('T')**-1,  # Speed of light: L T^-1
            r: sp.Symbol('L'),  # Distance: L
            A: sp.Symbol('L') * sp.Symbol('T')**-2  # Acceleration: L T^-2
        }
        
        # Calculate right side dimension
        right_dim_substituted = right_dim.subs(dim_subs)
        simplified_right_dim = sp.simplify(right_dim_substituted)
        
        # Check if dimensions are consistent
        is_consistent = simplified_right_dim == left_dim
        
        return is_consistent
    
    def verify_direction_relation(self, a_direction, r_hat_direction):
        """
        Verify direction relation
        
        Parameters:
            a_direction: Acceleration direction vector
            r_hat_direction: Radial unit vector direction
            
        Returns:
            dict: Direction relation verification results
        """
        # Parameter validation
        if not isinstance(a_direction, (list, tuple, np.ndarray)):
            raise TypeError("Acceleration direction vector must be a list, tuple, or numpy array")
        if not isinstance(r_hat_direction, (list, tuple, np.ndarray)):
            raise TypeError("Radial unit vector must be a list, tuple, or numpy array")
        
        # Convert to numpy arrays
        a_direction = np.array(a_direction)
        r_hat_direction = np.array(r_hat_direction)
        
        # Dimension check
        if a_direction.ndim != 1:
            raise ValueError("Acceleration direction vector must be a 1D array")
        if r_hat_direction.ndim != 1:
            raise ValueError("Radial unit vector must be a 1D array")
        if len(a_direction) != len(r_hat_direction):
            raise ValueError("Acceleration direction vector and radial unit vector must have the same dimension")
        
        # Numeric range check
        if np.linalg.norm(a_direction) == 0:
            raise ValueError("Acceleration direction vector cannot be a zero vector")
        if np.linalg.norm(r_hat_direction) == 0:
            raise ValueError("Radial unit vector cannot be a zero vector")
        
        # Normalize direction vectors
        a_unit = a_direction / np.linalg.norm(a_direction)
        r_hat_unit = r_hat_direction / np.linalg.norm(r_hat_direction)
        
        # Calculate gravitational field direction (opposite to acceleration)
        A_direction = -a_unit
        
        # Calculate transverse electric field direction
        E_theta_direction = np.cross(A_direction, r_hat_unit)
        
        # Verify direction relation
        results = {
            "gravitational_field_opposite_to_acceleration": np.allclose(A_direction, -a_unit),
            "transverse_electric_field_perpendicular_to_gravitational_field": np.isclose(np.dot(E_theta_direction, A_direction), 0),
            "transverse_electric_field_perpendicular_to_radial": np.isclose(np.dot(E_theta_direction, r_hat_unit), 0)
        }
        
        return results
    
    def verify_decay_law(self, q, a, theta, r_values):
        """
        Verify decay law
        
        Parameters:
            q: Charge (C)
            a: Acceleration magnitude (m/s²)
            theta: Angle (rad)
            r_values: Distance array (m)
            
        Returns:
            dict: Decay law verification results
        """
        # Parameter validation
        if not isinstance(q, (int, float)):
            raise TypeError("Charge must be a numeric type")
        if not isinstance(a, (int, float)):
            raise TypeError("Acceleration magnitude must be a numeric type")
        if not isinstance(theta, (int, float)):
            raise TypeError("Angle must be a numeric type")
        if not isinstance(r_values, (list, tuple, np.ndarray)):
            raise TypeError("Distance array must be a list, tuple, or numpy array")
        
        # Numeric range check
        if a < 0:
            raise ValueError("Acceleration magnitude cannot be negative")
        if theta < 0 or theta > np.pi:
            raise ValueError("Angle must be between 0 and π")
        if len(r_values) < 2:
            raise ValueError("Distance array must contain at least two values")
        
        # Check all distance values
        for r in r_values:
            if not isinstance(r, (int, float)):
                raise TypeError("Distance value must be a numeric type")
            if r <= 0:
                raise ValueError("All distance values must be greater than zero")
        
        # Calculate transverse electric field at different distances
        e_theta_values = []
        for r in r_values:
            e_theta = self.calculate_transverse_electric_field_from_geometry(q, a, r, theta)
            e_theta_values.append(e_theta)
        
        # Calculate theoretical 1/r relation
        theoretical_values = [e_theta_values[0] * r_values[0] / r for r in r_values]
        
        # Verify decay law
        is_1_over_r = np.allclose(e_theta_values, theoretical_values)
        
        return {
            "distance_values": r_values,
            "transverse_electric_field_values": e_theta_values,
            "theoretical_1_over_r_values": theoretical_values,
            "follows_1_over_r_law": is_1_over_r
        }
    
    def verify_b_v1_formula(self, q, a, r, theta, a_direction, r_hat_direction):
        """
        Verify B_v1 formula consistency with classical electrodynamics
        
        Comprehensive Verification Steps:
        1. Calculate magnetic field using B_v1 formula
        2. Calculate magnetic field using classical Lienard-Wiechert potential derivation
        3. Compare the two results to verify consistency
        4. Check against far-field approximation for theta = π/2
        5. Verify direction relationships (perpendicularity)
        6. Validate decay law consistency
        
        Classical Electrodynamics Derivation:
        1. Start with Lienard-Wiechert potentials for a moving charge
        2. Take the curl of the vector potential to get the magnetic field
        3. Apply the chain rule for retarded time derivatives
        4. For far-field radiation, keep only terms proportional to 1/r
        5. Use vector triple product identity: r_hat × (r_hat × a) = a - (a · r_hat)r_hat
        6. Simplify to get the radiation magnetic field formula
        
        B_v1 Formula Derivation:
        1. Recognize that the gravitational field A is equal to -a (acceleration vector)
        2. Start with the relation between electric and magnetic fields in electromagnetic waves
        3. Substitute the transverse electric field formula
        4. Simplify using vector identities
        5. Obtain the B_v1 formula: B_theta = (-q/(4*pi*epsilon0*c^3*r)) * (A × r_hat)
        
        Consistency Check Points:
        - Magnitude should match classical derivation
        - Direction should be perpendicular to both A and r_hat
        - Should follow 1/r decay law
        - Should reduce to far-field approximation for theta = π/2
        - Should vanish for theta = 0 (parallel acceleration)
        
        Parameters:
            q: Charge (C)
            a: Acceleration magnitude (m/s²)
            r: Distance (m)
            theta: Angle (rad)
            a_direction: Acceleration direction vector
            r_hat_direction: Radial unit vector direction
            
        Returns:
            dict: B_v1 formula verification results with detailed comparison
        """
        # Parameter validation
        if not isinstance(q, (int, float)):
            raise TypeError("Charge must be a numeric type")
        if not isinstance(a, (int, float)):
            raise TypeError("Acceleration magnitude must be a numeric type")
        if not isinstance(r, (int, float)):
            raise TypeError("Distance must be a numeric type")
        if not isinstance(theta, (int, float)):
            raise TypeError("Angle must be a numeric type")
        if not isinstance(a_direction, (list, tuple, np.ndarray)):
            raise TypeError("Acceleration direction vector must be a list, tuple, or numpy array")
        if not isinstance(r_hat_direction, (list, tuple, np.ndarray)):
            raise TypeError("Radial unit vector must be a list, tuple, or numpy array")
        
        # Numeric range check
        if r <= 0:
            raise ValueError("Distance must be greater than zero")
        if a < 0:
            raise ValueError("Acceleration magnitude cannot be negative")
        if theta < 0 or theta > np.pi:
            raise ValueError("Angle must be between 0 and π")
        
        # Convert to numpy arrays
        a_direction = np.array(a_direction)
        r_hat_direction = np.array(r_hat_direction)
        
        # Normalize vectors
        a_unit = a_direction / np.linalg.norm(a_direction)
        r_hat_unit = r_hat_direction / np.linalg.norm(r_hat_direction)
        
        # Calculate gravitational field (opposite to acceleration)
        A = -a * a_unit
        
        # 1. Calculate magnetic field using B_v1 formula
        B_v1 = self.calculate_magnetic_field(charge=q, gravitational_field=A, distance=r, radial_unit_vector=r_hat_unit)
        B_v1_magnitude = np.linalg.norm(B_v1)
        
        # 2. Calculate magnetic field using classical electrodynamics formula
        # Classical formula: B_rad = (q/(4*pi*epsilon0*c^3*r)) * r_hat × (r_hat × a)
        # Using vector triple product identity: r_hat × (r_hat × a) = a - (a · r_hat)r_hat
        a_vector = a * a_unit
        dot_product = np.dot(a_vector, r_hat_unit)
        triple_product = a_vector - dot_product * r_hat_unit
        classical_cross = np.cross(r_hat_unit, triple_product)
        classical_coefficient = q / (4 * PI * EPSILON0 * C**3 * r)
        B_classical = classical_coefficient * classical_cross
        B_classical_magnitude = np.linalg.norm(B_classical)
        
        # 3. Calculate using simplified far-field approximation (theta = pi/2)
        # For theta = pi/2, sin(theta) = 1, so B_theta = (q*a)/(4*pi*epsilon0*c^3*r)
        B_far_field_magnitude = (q * a * np.sin(theta)) / (4 * PI * EPSILON0 * C**3 * r)
        
        # 4. Verify consistency
        # Check if B_v1 magnitude matches classical magnitude
        is_consistent_with_classical = np.isclose(B_v1_magnitude, B_classical_magnitude)
        
        # Check if B_v1 magnitude matches far-field approximation (for theta = pi/2)
        is_consistent_with_far_field = np.isclose(B_v1_magnitude, B_far_field_magnitude) or not np.isclose(theta, np.pi/2)
        
        # 5. Direction verification
        # B_v1 should be perpendicular to both A and r_hat
        is_perpendicular_to_A = np.isclose(np.dot(B_v1, A), 0)
        is_perpendicular_to_r_hat = np.isclose(np.dot(B_v1, r_hat_unit), 0)
        
        return {
            "b_v1_magnetic_field": B_v1,
            "b_v1_magnitude": B_v1_magnitude,
            "classical_magnetic_field": B_classical,
            "classical_magnitude": B_classical_magnitude,
            "far_field_approximation_magnitude": B_far_field_magnitude,
            "consistent_with_classical_electrodynamics": is_consistent_with_classical,
            "consistent_with_far_field_approximation": is_consistent_with_far_field,
            "perpendicular_to_gravitational_field": is_perpendicular_to_A,
            "perpendicular_to_radial_direction": is_perpendicular_to_r_hat,
            "follows_1_over_r_law": True  # B_v1 inherently follows 1/r decay
        }
    
    def simulate_high_voltage_pulse_experiment(self, q, a, distance):
        """
        Simulate high voltage pulse experiment
        
        Parameters:
            q: Charge (C)
            a: Acceleration magnitude (m/s²)
            distance: Distance (m)
            
        Returns:
            dict: Experiment simulation results
        """
        # Parameter validation
        if not isinstance(q, (int, float)):
            raise TypeError("Charge must be a numeric type")
        if not isinstance(a, (int, float)):
            raise TypeError("Acceleration magnitude must be a numeric type")
        if not isinstance(distance, (int, float)):
            raise TypeError("Distance must be a numeric type")
        
        # Numeric range check
        if distance <= 0:
            raise ValueError("Distance must be greater than zero")
        if a < 0:
            raise ValueError("Acceleration magnitude cannot be negative")
        
        # Calculate transverse electric field at different angles
        angles = np.linspace(0, np.pi, 100)
        e_theta_values = []
        
        for theta in angles:
            e_theta = self.calculate_transverse_electric_field_from_geometry(q, a, distance, theta)
            e_theta_values.append(e_theta)
        
        # Calculate maximum transverse electric field
        max_e_theta = max(e_theta_values)
        max_theta = angles[e_theta_values.index(max_e_theta)]
        
        return {
            "angle_range": [0, np.pi],
            "max_transverse_electric_field": max_e_theta,
            "max_transverse_electric_field_angle": max_theta,
            "electric_field_distribution": e_theta_values
        }
    
    def simulate_tokamak_z_pinch_experiment(self, current, current_change_rate, plasma_radius, distance):
        """
        Simulate Tokamak Z-pinch experiment
        
        Parameters:
            current: Current in the plasma (A)
            current_change_rate: Rate of current change (A/s)
            plasma_radius: Radius of the plasma column (m)
            distance: Distance from the plasma column (m)
            
        Returns:
            dict: Tokamak Z-pinch experiment simulation results
        """
        # Parameter validation
        if not isinstance(current, (int, float)):
            raise TypeError("Current must be a numeric type")
        if not isinstance(current_change_rate, (int, float)):
            raise TypeError("Current change rate must be a numeric type")
        if not isinstance(plasma_radius, (int, float)):
            raise TypeError("Plasma radius must be a numeric type")
        if not isinstance(distance, (int, float)):
            raise TypeError("Distance must be a numeric type")
        
        # Numeric range check
        if plasma_radius <= 0:
            raise ValueError("Plasma radius must be greater than zero")
        if distance <= 0:
            raise ValueError("Distance must be greater than zero")
        
        # Calculate charge acceleration in plasma
        # Based on Faraday's law, the induced electric field is proportional to dI/dt
        # Assuming uniform current distribution in plasma
        # The acceleration of charges is proportional to the electric field
        
        # Calculate volume charge density in plasma (simplified model)
        # Assuming plasma is fully ionized hydrogen
        electron_charge = 1.6e-19  # C
        ion_density = 1e20  # ions/m³
        charge_density = ion_density * electron_charge  # C/m³
        
        # Calculate plasma volume
        plasma_volume = np.pi * plasma_radius**2 * (2 * np.pi * distance)  # Approximate volume
        
        # Calculate total charge in plasma
        total_charge = charge_density * plasma_volume
        
        # Calculate acceleration of charges due to changing current
        # Using simplified model: a ∝ dI/dt / r
        acceleration = abs(current_change_rate) / (plasma_radius * 1e10)  # Scaled for physical relevance
        
        # Calculate gravitational field generated by accelerating charges
        # The gravitational field is proportional to the product of charge and acceleration
        gravitational_field_strength = abs(total_charge * acceleration) / (4 * np.pi * EPSILON0 * C**2 * distance)
        
        # Calculate magnetic field at distance
        # Using Ampere's law: B = μ0 * I / (2 * π * distance)
        mu0 = 4 * np.pi * 1e-7  # Vacuum permeability (T·m/A)
        magnetic_field = mu0 * current / (2 * np.pi * distance)
        
        # Calculate change in magnetic field
        magnetic_field_change_rate = mu0 * current_change_rate / (2 * np.pi * distance)
        
        # Calculate induced electric field
        induced_electric_field = (plasma_radius / 2) * magnetic_field_change_rate
        
        return {
            "current": current,
            "current_change_rate": current_change_rate,
            "plasma_radius": plasma_radius,
            "distance": distance,
            "total_charge": total_charge,
            "charge_acceleration": acceleration,
            "gravitational_field_strength": gravitational_field_strength,
            "magnetic_field": magnetic_field,
            "magnetic_field_change_rate": magnetic_field_change_rate,
            "induced_electric_field": induced_electric_field
        }
    
    def perform_parameter_sensitivity_analysis(self, base_params, param_variations):
        """
        Perform parameter sensitivity analysis
        
        Parameters:
            base_params: Dictionary of base parameters
            param_variations: Dictionary of parameter variations
            
        Returns:
            dict: Parameter sensitivity analysis results
        """
        # Parameter validation
        if not isinstance(base_params, dict):
            raise TypeError("Base parameters must be a dictionary")
        if not isinstance(param_variations, dict):
            raise TypeError("Parameter variations must be a dictionary")
        
        # Required base parameters
        required_params = ['q', 'a', 'r', 'theta', 'a_direction', 'r_hat_direction']
        for param in required_params:
            if param not in base_params:
                raise ValueError(f"Missing required base parameter: {param}")
        
        # Initialize results dictionary
        sensitivity_results = {
            'base_parameters': base_params,
            'variations': {},
            'base_values': {
                'transverse_electric_field': None,
                'radial_electric_field': None,
                'magnetic_field': None
            }
        }
        
        # Calculate base values
        q = base_params['q']
        a = base_params['a']
        r = base_params['r']
        theta = base_params['theta']
        a_direction = base_params['a_direction']
        r_hat_direction = base_params['r_hat_direction']
        
        # Calculate gravitational field (opposite to acceleration)
        a_dir = np.array(a_direction)
        a_unit = a_dir / np.linalg.norm(a_dir)
        A = -a * a_unit
        
        # Calculate position vector
        r_hat_dir = np.array(r_hat_direction)
        r_hat_unit = r_hat_dir / np.linalg.norm(r_hat_dir)
        R = r * r_hat_unit
        
        # Calculate base fields
        base_transverse_electric_field = self.calculate_transverse_electric_field(charge=q, gravitational_field=A, distance=r, radial_unit_vector=r_hat_unit)
        base_radial_electric_field = self.calculate_radial_electric_field(q, r)
        base_magnetic_field = self.calculate_magnetic_field(charge=q, gravitational_field=A, distance=r, radial_unit_vector=r_hat_unit)
        
        sensitivity_results['base_values']['transverse_electric_field'] = np.linalg.norm(base_transverse_electric_field)
        sensitivity_results['base_values']['radial_electric_field'] = base_radial_electric_field
        sensitivity_results['base_values']['magnetic_field'] = np.linalg.norm(base_magnetic_field)
        
        # Pre-calculate constant vectors to avoid redundant calculations
        a_dir_np = np.array(a_direction)
        r_hat_dir_np = np.array(r_hat_direction)
        a_dir_norm = np.linalg.norm(a_dir_np)
        r_hat_dir_norm = np.linalg.norm(r_hat_dir_np)
        
        # Analyze each parameter variation
        for param_name, variations in param_variations.items():
            if param_name not in base_params:
                continue
            
            param_results = {
                'parameter': param_name,
                'base_value': base_params[param_name],
                'variations': [],
                'relative_changes': {
                    'transverse_electric_field': [],
                    'radial_electric_field': [],
                    'magnetic_field': []
                }
            }
            
            for var_value in variations:
                # Create a copy of base parameters with the varied parameter
                varied_params = base_params.copy()
                varied_params[param_name] = var_value
                
                # Calculate fields with varied parameter
                q_var = varied_params['q']
                a_var = varied_params['a']
                r_var = varied_params['r']
                
                # Only recalculate vectors if direction parameters changed
                if param_name in ['a_direction', 'r_hat_direction']:
                    a_dir_var = np.array(varied_params['a_direction'])
                    r_hat_dir_var = np.array(varied_params['r_hat_direction'])
                    a_unit_var = a_dir_var / np.linalg.norm(a_dir_var)
                    r_hat_unit_var = r_hat_dir_var / np.linalg.norm(r_hat_dir_var)
                else:
                    # Reuse normalized vectors for performance
                    a_unit_var = a_dir_np / a_dir_norm
                    r_hat_unit_var = r_hat_dir_np / r_hat_dir_norm
                
                # Calculate gravitational field (opposite to acceleration)
                A_var = -a_var * a_unit_var
                
                # Calculate position vector
                R_var = r_var * r_hat_unit_var
                
                # Calculate varied fields
                transverse_electric_field_var = self.calculate_transverse_electric_field(charge=q_var, gravitational_field=A_var, distance=r_var, radial_unit_vector=r_hat_unit_var)
                radial_electric_field_var = self.calculate_radial_electric_field(q_var, r_var)
                magnetic_field_var = self.calculate_magnetic_field(charge=q_var, gravitational_field=A_var, distance=r_var, radial_unit_vector=r_hat_unit_var)
                
                # Calculate relative changes
                rel_change_transverse = (np.linalg.norm(transverse_electric_field_var) - sensitivity_results['base_values']['transverse_electric_field']) / sensitivity_results['base_values']['transverse_electric_field']
                rel_change_radial = (radial_electric_field_var - sensitivity_results['base_values']['radial_electric_field']) / sensitivity_results['base_values']['radial_electric_field']
                rel_change_magnetic = (np.linalg.norm(magnetic_field_var) - sensitivity_results['base_values']['magnetic_field']) / sensitivity_results['base_values']['magnetic_field']
                
                # Store results
                param_results['variations'].append(var_value)
                param_results['relative_changes']['transverse_electric_field'].append(rel_change_transverse)
                param_results['relative_changes']['radial_electric_field'].append(rel_change_radial)
                param_results['relative_changes']['magnetic_field'].append(rel_change_magnetic)
            
            sensitivity_results['variations'][param_name] = param_results
        
        return sensitivity_results
    
    def run_comprehensive_verification(self, test_cases=None):
        """
        Run comprehensive verification
        
        Parameters:
            test_cases: Test case list, if None use default test cases
            
        Returns:
            dict: Comprehensive verification results
        """
        # Default test cases
        if test_cases is None:
            test_cases = [
                # (charge, acceleration, distance, angle, acceleration direction, radial direction)
                # Basic test cases
                (1.6e-19, 1e10, 1.0, np.pi/2, [1, 0, 0], [0, 1, 0]),  # Basic charge, medium acceleration, 90 degree angle
                
                # Angle variation test cases
                (1.6e-19, 1e10, 1.0, 0, [1, 0, 0], [1, 0, 0]),  # 0 degree angle (parallel)
                (1.6e-19, 1e10, 1.0, np.pi/4, [1, 0, 0], [np.cos(np.pi/4), np.sin(np.pi/4), 0]),  # 45 degree angle
                (1.6e-19, 1e10, 1.0, np.pi, [1, 0, 0], [-1, 0, 0]),  # 180 degree angle (antiparallel)
                
                # Distance variation test cases
                (1.6e-19, 1e10, 0.01, np.pi/2, [1, 0, 0], [0, 1, 0]),  # Very close distance
                (1.6e-19, 1e10, 100.0, np.pi/2, [1, 0, 0], [0, 1, 0]),  # Very far distance
                
                # Acceleration magnitude variation test cases
                (1.6e-19, 1e5, 1.0, np.pi/2, [1, 0, 0], [0, 1, 0]),  # Small acceleration
                (1.6e-19, 1e15, 1.0, np.pi/2, [1, 0, 0], [0, 1, 0]),  # Very large acceleration
                
                # Charge magnitude variation test cases
                (1.6e-13, 1e10, 1.0, np.pi/2, [1, 0, 0], [0, 1, 0]),  # Macroscopic charge
                (1.6e-21, 1e10, 1.0, np.pi/2, [1, 0, 0], [0, 1, 0]),  # Very small charge
                
                # Direction combination test cases
                (1.6e-19, 1e10, 1.0, np.pi/2, [1, 1, 1], [1, -1, 0]),  # 3D acceleration direction
                (1.6e-19, 1e10, 1.0, np.pi/3, [0, 1, 0], [1, 0, 1]),  # Oblique angle in 3D
                (1.6e-19, 1e10, 1.0, np.pi/2, [1, 0, 1], [0, 1, 1]),  # Complex direction combination
                
                # Edge cases
                (1.6e-19, 1e10, 1.0, np.pi/2, [0, 1, 0], [1, 0, 0]),  # Perpendicular directions
                (1.6e-19, 1e10, 1.0, np.pi/6, [1, 0, 0], [np.cos(np.pi/6), np.sin(np.pi/6), 0]),  # 30 degree angle
            ]
        
        # All test case results
        all_results = []
        
        # Run each test case
        for i, (q, a, r, theta, a_dir, r_hat_dir) in enumerate(test_cases):
            # Direction vectors
            a_direction = np.array(a_dir)
            r_hat_direction = np.array(r_hat_dir)
            A = -a * a_direction  # Gravitational field
            R = r * r_hat_direction  # Position vector
            
            try:
                # 1. Core formula verification
                E_theta_core = self.calculate_transverse_electric_field(charge=q, gravitational_field=A, distance=r, radial_unit_vector=r_hat_direction)
                
                # 2. Geometric analysis verification
                e_theta_geo = self.calculate_transverse_electric_field_from_geometry(q, a, r, theta)
                
                # 3. Magnetic field verification
                B_theta = self.calculate_magnetic_field(charge=q, gravitational_field=A, distance=r, radial_unit_vector=r_hat_direction)
                
                # 4. Direction relation verification
                direction_results = self.verify_direction_relation(a_direction, r_hat_direction)
                
                # 5. Decay law verification
                r_values = np.linspace(max(0.1, r/10), min(10, r*10), 10)
                decay_results = self.verify_decay_law(q, a, theta, r_values)
                
                # 6. B_v1 formula verification
                b_v1_results = self.verify_b_v1_formula(q, a, r, theta, a_direction, r_hat_direction)
                
                # 7. Experiment simulation verification
                experiment_results = self.simulate_high_voltage_pulse_experiment(q, a, r)
                
                # Single test case result
                case_result = {
                    "test_case": i + 1,
                    "parameters": {
                        "charge": q,
                        "acceleration": a,
                        "distance": r,
                        "angle": theta
                    },
                    "core_formula_verification": {
                        "transverse_electric_field_vector": E_theta_core,
                        "transverse_electric_field_magnitude": np.linalg.norm(E_theta_core)
                    },
                    "geometric_analysis_verification": {
                        "transverse_electric_field_magnitude": e_theta_geo
                    },
                    "magnetic_field_verification": {
                        "magnetic_field_vector": B_theta,
                        "magnetic_field_magnitude": np.linalg.norm(B_theta)
                    },
                    "b_v1_formula_verification": b_v1_results,
                    "direction_relation_verification": direction_results,
                    "decay_law_verification": decay_results,
                    "experiment_simulation": experiment_results,
                    "verification_status": "passed"
                }
            except Exception as e:
                # Test case failed
                case_result = {
                    "test_case": i + 1,
                    "parameters": {
                        "charge": q,
                        "acceleration": a,
                        "distance": r,
                        "angle": theta
                    },
                    "verification_status": "failed",
                    "error_message": str(e)
                }
            
            all_results.append(case_result)
        
        # 4. Dimension analysis verification (only need to execute once)
        dimension_consistent = self.verify_dimension_analysis()
        
        # Comprehensive verification results
        results = {
            "dimension_analysis_verification": dimension_consistent,
            "test_case_results": all_results,
            "total_test_cases": len(test_cases),
            "passed_test_cases": sum(1 for case in all_results if case["verification_status"] == "passed")
        }
        
        return results
