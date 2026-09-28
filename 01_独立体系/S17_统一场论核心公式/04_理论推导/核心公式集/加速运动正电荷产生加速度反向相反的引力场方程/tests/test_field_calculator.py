#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test module for field calculator functionality
"""

import unittest
import numpy as np
from core.field_calculator import FieldCalculator

class TestFieldCalculator(unittest.TestCase):
    """
    Test case for FieldCalculator class
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.calculator = FieldCalculator()
        
    def test_calculate_transverse_electric_field(self):
        """
        Test transverse electric field calculation
        """
        # Test with basic parameters
        q = 1.6e-19  # Electron charge
        A = [1, 0, 0]  # Gravitational field in x-direction
        r = 1.0  # Distance
        r_hat = [0, 1, 0]  # Radial unit vector in y-direction
        
        result = self.calculator.calculate_transverse_electric_field(q, A, r, r_hat)
        
        # Check that result is a numpy array
        self.assertIsInstance(result, np.ndarray)
        # Check that result has 3 dimensions
        self.assertEqual(len(result), 3)
        # Check that result is in z-direction (cross product of x and y)
        self.assertNotEqual(result[2], 0)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)
    
    def test_calculate_radial_electric_field(self):
        """
        Test radial electric field calculation (Coulomb's law)
        """
        q = 1.6e-19  # Electron charge
        r = 1.0  # Distance
        
        result = self.calculator.calculate_radial_electric_field(q, r)
        
        # Check that result is a float
        self.assertIsInstance(result, (int, float))
        # Check that result is positive (for positive charge)
        self.assertGreater(result, 0)
    
    def test_calculate_transverse_electric_field_from_geometry(self):
        """
        Test transverse electric field calculation from geometry
        """
        q = 1.6e-19  # Electron charge
        a = 1e10  # Acceleration
        r = 1.0  # Distance
        theta = np.pi/2  # 90 degrees
        
        result = self.calculator.calculate_transverse_electric_field_from_geometry(q, a, r, theta)
        
        # Check that result is a float
        self.assertIsInstance(result, (int, float))
        # Check that result is positive
        self.assertGreater(result, 0)
    
    def test_calculate_magnetic_field(self):
        """
        Test magnetic field calculation
        """
        q = 1.6e-19  # Electron charge
        A = [1, 0, 0]  # Gravitational field in x-direction
        R = [0, 1, 0]  # Position vector in y-direction
        
        result = self.calculator.calculate_magnetic_field(q, A, R)
        
        # Check that result is a numpy array
        self.assertIsInstance(result, np.ndarray)
        # Check that result has 3 dimensions
        self.assertEqual(len(result), 3)
        # Check that result is in z-direction (cross product of x and y)
        self.assertNotEqual(result[2], 0)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)
    
    def test_verify_dimension_analysis(self):
        """
        Test dimension analysis verification
        """
        result = self.calculator.verify_dimension_analysis()
        
        # Check that result is a boolean
        self.assertIsInstance(result, bool)
        # Check that dimensions are consistent
        self.assertTrue(result)
    
    def test_verify_direction_relation(self):
        """
        Test direction relation verification
        """
        a_direction = [1, 0, 0]  # Acceleration in x-direction
        r_hat_direction = [0, 1, 0]  # Radial unit vector in y-direction
        
        result = self.calculator.verify_direction_relation(a_direction, r_hat_direction)
        
        # Check that result is a dictionary
        self.assertIsInstance(result, dict)
        # Check that all direction relations are True
        for key, value in result.items():
            self.assertTrue(value)
    
    def test_verify_decay_law(self):
        """
        Test decay law verification
        """
        q = 1.6e-19  # Electron charge
        a = 1e10  # Acceleration
        theta = np.pi/2  # 90 degrees
        r_values = [0.1, 0.2, 0.5, 1.0, 2.0]  # Distance values
        
        result = self.calculator.verify_decay_law(q, a, theta, r_values)
        
        # Check that result is a dictionary
        self.assertIsInstance(result, dict)
        # Check that follows_1_over_r_law is True
        self.assertTrue(result['follows_1_over_r_law'])
    
    def test_simulate_high_voltage_pulse_experiment(self):
        """
        Test high voltage pulse experiment simulation
        """
        q = 1.6e-19  # Electron charge
        a = 1e10  # Acceleration
        distance = 1.0  # Distance
        
        result = self.calculator.simulate_high_voltage_pulse_experiment(q, a, distance)
        
        # Check that result is a dictionary
        self.assertIsInstance(result, dict)
        # Check that max_transverse_electric_field is positive
        self.assertGreater(result['max_transverse_electric_field'], 0)
        # Check that max_transverse_electric_field_angle is between 0 and pi
        self.assertGreaterEqual(result['max_transverse_electric_field_angle'], 0)
        self.assertLessEqual(result['max_transverse_electric_field_angle'], np.pi)
    
    def test_run_comprehensive_verification(self):
        """
        Test comprehensive verification
        """
        result = self.calculator.run_comprehensive_verification()
        
        # Check that result is a dictionary
        self.assertIsInstance(result, dict)
        # Check that dimension_analysis_verification is True
        self.assertTrue(result['dimension_analysis_verification'])
        # Check that there are test case results
        self.assertGreater(len(result['test_case_results']), 0)

if __name__ == '__main__':
    unittest.main()
