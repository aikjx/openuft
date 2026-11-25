import unittest
from decimal import Decimal
from root_v149.precision import audit_decimal
from root_v149.core import ALPHA,gravitational_fine_structure_electron
class TestPrecision(unittest.TestCase):
    def test_inverse_alpha(self):
        self.assertTrue(Decimal(audit_decimal()['alpha_inverse_calculated'])>Decimal(137))
    def test_precise_fitted_radius(self):
        self.assertAlmostEqual(float(audit_decimal()['fit_sqrt_alpha']),ALPHA**.5,15)
    def test_precise_fitted_u(self):
        self.assertAlmostEqual(float(audit_decimal()['fit_u_sqrt_1_minus_alpha']),(1-ALPHA)**.5,15)
    def test_precise_gravity(self):
        self.assertAlmostEqual(float(audit_decimal()['electron_alpha_gravity'])/gravitational_fine_structure_electron(),1.0,14)
    def test_physical_uncertainty_not_equal_computational_digits(self):
        self.assertIn('uncertainty',audit_decimal()['precision_note'])
    def test_negative_precision_rejected(self):
        with self.assertRaises(ValueError):audit_decimal(10)
