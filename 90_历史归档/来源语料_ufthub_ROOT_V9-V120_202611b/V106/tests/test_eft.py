import unittest, math
from src.eft import normalized_scalar_mass,topological_path_integral_phase
class TestEFT(unittest.TestCase):
    def test_01_integer_level_one(self):self.assertAlmostEqual(abs(topological_path_integral_phase(1,1)-1),0,places=12)
    def test_02_integer_levels(self):
        for k in range(-5,6):
            for n in range(-3,4):self.assertLess(abs(topological_path_integral_phase(k,n)-1),1e-13)
    def test_03_fractional_level_fails(self):self.assertGreater(abs(topological_path_integral_phase(.5,1)-1),1)
    def test_04_fractional_possible_even_Q(self):self.assertLess(abs(topological_path_integral_phase(.5,2)-1),1e-13)
    def test_05_zero_top_charge(self):self.assertEqual(topological_path_integral_phase(.13,0),1+0j)
    def test_06_mass_formula(self):self.assertAlmostEqual(normalized_scalar_mass(1000,1),.001)
    def test_07_zero_mass(self):self.assertEqual(normalized_scalar_mass(1000,0),0)
    def test_08_negative_f_rejected(self):
        with self.assertRaises(ValueError):normalized_scalar_mass(-1,1)
    def test_09_bad_lambda_rejected(self):
        with self.assertRaises(ValueError):normalized_scalar_mass(1,-1)
