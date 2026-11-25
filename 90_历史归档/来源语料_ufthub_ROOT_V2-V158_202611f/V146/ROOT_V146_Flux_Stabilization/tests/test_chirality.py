from fractions import Fraction
import unittest
from root_v146.chirality import (index,zero_mode_count,anomalies_U1F,
                               sm_hypercharge_anomalies_per_generation)

class TestChirality(unittest.TestCase):
    def test_index_counts_n3(self):
        self.assertEqual(index(1,3),3)
    def test_negative_flux_chirality(self):
        self.assertEqual(index(1,-3),-3)
        self.assertEqual(zero_mode_count(1,-3),3)
    def test_zero_flux(self):
        self.assertEqual(zero_mode_count(1,0),0)
    def test_general_charge(self):
        self.assertEqual(index(-2,3),-6)
    def test_integral_flux(self):
        with self.assertRaises(TypeError): index(1,.5)
    def test_SM_Y_anomaly_free(self):
        for val in sm_hypercharge_anomalies_per_generation().values():
            self.assertEqual(val,0)
    def test_F_SU3_anomaly(self):
        self.assertEqual(anomalies_U1F(3)['SU3^2 F'],6)
    def test_F_SU2_anomaly(self):
        self.assertEqual(anomalies_U1F(3)['SU2^2 F'],6)
    def test_F_gravity_anomaly(self):
        self.assertEqual(anomalies_U1F(3)['grav^2 F'],45)
    def test_F_cubic_anomaly(self):
        self.assertEqual(anomalies_U1F(3)['F^3'],45)
    def test_F_Y2_anomaly(self):
        self.assertEqual(anomalies_U1F(3)['Y^2 F'],10)
    def test_one_family_anomalies(self):
        a=anomalies_U1F(1)
        self.assertEqual(a['SU3^2 F'],2)
        self.assertEqual(a['Y^2 F'],Fraction(10,3))
    def test_family_charge_zero_removes_F_anomaly(self):
        self.assertTrue(all(v==0 for v in anomalies_U1F(3,0).values()))
    def test_negative_family_charge_flips_all_F_odd_anomalies(self):
        positive=anomalies_U1F(3,1); negative=anomalies_U1F(3,-1)
        for key in positive:
            self.assertEqual(positive[key],-negative[key])
    def test_two_opposite_F_assignments_cancel(self):
        a=anomalies_U1F(3,1); b=anomalies_U1F(3,-1)
        for key in a: self.assertEqual(a[key]+b[key],0)
    def test_no_three_generation_selection(self):
        for n in range(1,8):
            self.assertEqual(zero_mode_count(1,n),n)

if __name__=='__main__': unittest.main()
