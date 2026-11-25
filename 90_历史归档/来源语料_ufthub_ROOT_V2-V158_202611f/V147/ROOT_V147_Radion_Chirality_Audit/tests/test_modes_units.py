import math
import unittest
from root_v147.flux import (scalar_test_mass_squared,degeneracy,scalar_beta_brane,
    scalar_strength_brane,yukawa_potential_fraction,yukawa_force_fraction,illustrated)
from root_v147.numerics import simpson_legendre_inner
from root_v147.units import S,L,hbar,G4,K6,Lambda6,chi6,K4,V4

class ModeTest(unittest.TestCase):
    def test_l0_massless_neutral_scalar(self): self.assertEqual(scalar_test_mass_squared(0,2),0)
    def test_l1_threefold(self):
        self.assertEqual(scalar_test_mass_squared(1,1),2)
        self.assertEqual(degeneracy(1),3)
    def test_l2_fivefold(self):
        self.assertEqual(scalar_test_mass_squared(2,1),6)
        self.assertEqual(degeneracy(2),5)
    def test_positive_eigenvalue(self):
        for l in range(1,10):self.assertGreater(scalar_test_mass_squared(l,3),0)
    def test_eigenvalue_inverse_R2(self):
        for l in range(1,6):
            self.assertAlmostEqual(scalar_test_mass_squared(l,1)/scalar_test_mass_squared(l,2),4)
    def test_nonzero_bulk_scalar_mass(self):
        self.assertAlmostEqual(scalar_test_mass_squared(2,3,4),4+6/9)
    def test_legendre_diagonal(self):
        for l in range(5):
            self.assertAlmostEqual(simpson_legendre_inner(l,l),2/(2*l+1),delta=3e-9)
    def test_legendre_offdiag(self):
        for l,m in ((0,1),(0,4),(1,3),(2,4)):
            self.assertAlmostEqual(simpson_legendre_inner(l,m),0,delta=3e-9)
    def test_beta_scalar(self):self.assertEqual(scalar_beta_brane(),-.5)
    def test_strength_scalar(self):self.assertEqual(scalar_strength_brane(),.5)
    def test_Yukawa_potential_at_one_range(self):
        self.assertAlmostEqual(yukawa_potential_fraction(1,1),.5/math.e)
    def test_Yukawa_force_at_one_range(self):
        self.assertAlmostEqual(yukawa_force_fraction(1,1),1/math.e)
    def test_Yukawa_force_monotone(self):
        self.assertTrue(all(yukawa_force_fraction(i,1)>=yukawa_force_fraction(i+1,1) for i in range(0,10)))
    def test_Yukawa_strength_large_distance_zero(self):
        self.assertLess(yukawa_force_fraction(40,1),1e-14)
    def test_bad_ell(self):
        with self.assertRaises(ValueError):scalar_test_mass_squared(-1,1)
    def test_hbar_independent(self):self.assertEqual(hbar,S)
    def test_G4_dimensional(self):self.assertEqual(G4,L**2/S)
    def test_K6_Lambda_chi_dimensions(self):
        self.assertEqual(K6,S/L**4)
        self.assertEqual(Lambda6,S/L**6)
        self.assertEqual(chi6,S/L**2)
    def test_potential_A_term_dimensions(self):
        self.assertEqual((Lambda6*L**4)/L**2,V4)
    def test_potential_B_term_dimensions(self):
        self.assertEqual((K6*L**4)/L**4,V4)
    def test_potential_C_term_dimensions(self):
        self.assertEqual((chi6*L**4)*L**0/L**6,V4)
    def test_radion_mass_length(self):
        self.assertEqual(V4/K4,1/L**2)
    def test_radion_physical_mass(self):
        self.assertEqual(hbar*(1/L**2)**(1/2),S/L)
    def test_newton_relation(self):
        self.assertEqual(1/K4,G4)

if __name__=='__main__':unittest.main()
