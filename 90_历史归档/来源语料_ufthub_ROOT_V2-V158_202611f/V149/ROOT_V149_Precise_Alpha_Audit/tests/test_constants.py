import math,unittest
from root_v149.core import (ALPHA,ALPHA_STD,HBAR_SI,H_SI,G_SI,ME_SI,C_SI_TO_CONVERT,
        gravitational_fine_structure_electron,q_ed_relation,helix_for_alpha,diagnostic)

class TestConstants(unittest.TestCase):
    def test_nist_alpha(self): self.assertEqual(ALPHA,7.2973525643e-3)
    def test_alpha_positive(self): self.assertGreater(ALPHA,0)
    def test_alpha_less_one(self): self.assertLess(ALPHA,1)
    def test_nist_alpha_inverse(self): self.assertAlmostEqual(1/ALPHA,137.035999177,8)
    def test_nist_uncertainty(self): self.assertEqual(ALPHA_STD,1.1e-12)
    def test_hbar_not_unity(self): self.assertEqual(HBAR_SI,H_SI/(2*math.pi))
    def test_G_not_unity(self): self.assertEqual(G_SI,6.67430e-11)
    def test_g_electron_small(self): self.assertLess(gravitational_fine_structure_electron(),1e-44)
    def test_g_electron_greater(self): self.assertGreater(gravitational_fine_structure_electron(),1e-46)
    def test_G_factor_conversion(self):
        value=G_SI*ME_SI*ME_SI/(HBAR_SI*C_SI_TO_CONVERT)
        self.assertAlmostEqual(value,gravitational_fine_structure_electron(),45)
    def test_alpha_electron_grav_ratio(self): self.assertGreater(ALPHA/gravitational_fine_structure_electron(),1e42)
    def test_fitted_is_not_predicted(self):
        for alpha in [0.01,0.15,0.6]:
            with self.subTest(alpha=alpha):
                self.assertAlmostEqual(helix_for_alpha(alpha).alpha_proxy(),alpha,13)
    def test_qed_charge_normalization(self): self.assertAlmostEqual(q_ed_relation(),4*math.pi*ALPHA,15)
    def test_output_contains_status(self):self.assertIn('Mathematical counterexample',diagnostic()['physical_status'])
