import unittest
from fractions import Fraction as Q
from root_v147.anomalies import (fields_uniform_family,fields_B_minus_L,
    anomaly_coefficients,multiply,with_singlets,chiral_index)

class AnomalyTest(unittest.TestCase):
    def test_chirality_flip(self):
        for n in range(1,20): self.assertEqual(chiral_index(n),-chiral_index(-n))
    def test_chiral_index_coupling(self):
        self.assertEqual(chiral_index(3,-2),-6)
    def test_chiral_index_not_mass_positive(self):
        self.assertNotEqual(chiral_index(3),chiral_index(-3))
    def test_reject_fractional_flux(self):
        with self.assertRaises(TypeError):chiral_index(1.5)
    def test_uniform_SU3_anomaly(self):
        self.assertEqual(multiply(anomaly_coefficients(fields_uniform_family()),3)['SU3^2-F'],6)
    def test_uniform_SU2_anomaly(self):
        self.assertEqual(multiply(anomaly_coefficients(fields_uniform_family()),3)['SU2^2-F'],6)
    def test_uniform_hypercharge_squared_family(self):
        self.assertEqual(multiply(anomaly_coefficients(fields_uniform_family()),3)['Y^2-F'],10)
    def test_uniform_cubic_F(self):
        self.assertEqual(multiply(anomaly_coefficients(fields_uniform_family()),3)['F^3'],45)
    def test_uniform_gravitational_F(self):
        self.assertEqual(multiply(anomaly_coefficients(fields_uniform_family()),3)['grav^2-F'],45)
    def test_uniform_mixed_Y_F_squared(self):
        self.assertEqual(anomaly_coefficients(fields_uniform_family())['Y-F^2'],0)
    def test_SM_hypercharge_anomalies_cancel(self):
        a=anomaly_coefficients(fields_uniform_family())
        for k in ('Y^3','grav^2-Y','SU3^2-Y','SU2^2-Y'):self.assertEqual(a[k],0)
    def test_B_minus_L_all_local_anomalies_cancel(self):
        a=anomaly_coefficients(fields_B_minus_L())
        for k,v in a.items():self.assertEqual(v,0,f'{k}: {v}')
    def test_B_minus_L_three_generations(self):
        a=multiply(anomaly_coefficients(fields_B_minus_L()),3)
        self.assertTrue(all(x==0 for x in a.values()))
    def test_singlets_cannot_fix_nonabelian_anomalies(self):
        raw=anomaly_coefficients(fields_uniform_family())
        for charges in ((1,),(1,-1,2,-2),(100,-100,0)):
            new=anomaly_coefficients(with_singlets(fields_uniform_family(),charges))
            self.assertEqual(new['SU3^2-F'],raw['SU3^2-F'])
            self.assertEqual(new['SU2^2-F'],raw['SU2^2-F'])
    def test_witten_SU2_number_even(self):
        a=fields_uniform_family()
        self.assertEqual(sum(x.d3 for x in a if x.d2==2)%2,0)

if __name__=='__main__':unittest.main()
