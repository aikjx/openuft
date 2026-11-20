import unittest
from fractions import Fraction as F
from src.anomaly import STATES,Weyl,anomaly_coefficients,su5_hypercharge_generator,su5_normalization

class TestAnomaly(unittest.TestCase):
    def test_01_generation_five_multiplets(self):self.assertEqual(len(STATES),5)
    def test_02_su3_cubic_zero(self):self.assertEqual(anomaly_coefficients()['SU3^3'],0)
    def test_03_su3squared_y_zero(self):self.assertEqual(anomaly_coefficients()['SU3^2-U1'],0)
    def test_04_su2squared_y_zero(self):self.assertEqual(anomaly_coefficients()['SU2^2-U1'],0)
    def test_05_y_cubic_zero(self):self.assertEqual(anomaly_coefficients()['U1^3'],0)
    def test_06_grav_y_zero(self):self.assertEqual(anomaly_coefficients()['grav^2-U1'],0)
    def test_07_witten_even(self):self.assertEqual(anomaly_coefficients()['Witten_SU2_obstruction'],0)
    def test_08_four_doublets(self):self.assertEqual(anomaly_coefficients()['SU2_doublets'],4)
    def test_09_remove_e_c_breaks_y(self):
        x=anomaly_coefficients(STATES[:-1]);self.assertNotEqual(x['U1^3'],0)
    def test_10_remove_q_breaks_witten(self):
        x=anomaly_coefficients(STATES[1:]);self.assertEqual(x['SU2_doublets'],1)
    def test_11_su5_traceless(self):self.assertEqual(su5_normalization()['trace'],0)
    def test_12_su5_trace_y2(self):self.assertEqual(su5_normalization()['trace_Y_squared'],F(5,6))
    def test_13_su5_generator_normalized(self):self.assertEqual(su5_normalization()['normalized_trace_squared'],F(1,2))
    def test_14_su5_normalization_squared(self):self.assertEqual(su5_normalization()['normalization_squared'],F(3,5))
    def test_15_su5_entries(self):self.assertEqual(len(su5_hypercharge_generator()),5)
    def test_16_all_values_exact_rational(self):
        self.assertTrue(all(isinstance(x.y,F) for x in STATES))
    def test_17_anomaly_rational(self):self.assertEqual(type(anomaly_coefficients()['U1^3']),F)
