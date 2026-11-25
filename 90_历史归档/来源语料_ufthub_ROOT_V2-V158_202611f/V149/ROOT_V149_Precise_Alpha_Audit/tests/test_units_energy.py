import math,unittest
from root_v149.core import ALPHA,helix_for_alpha
from root_v149.energy import tangent_null_energy_boost_ratio,geometric_frequency_boost_ratio,ratio_E_over_hbar_omega,plane_wave_energy_frequency_ratio
from root_v149.units import dimension_audit
class TestUnitsEnergy(unittest.TestCase):
    def test_dimensions_all(self): self.assertTrue(all(dimension_audit().values()))
    def test_e_over_w_ratio_identity(self):
        h=helix_for_alpha(.21)
        self.assertAlmostEqual(ratio_E_over_hbar_omega(h,0),1,14)
    def test_comoving_ratio_is_fitted_alpha(self):
        h=helix_for_alpha()
        self.assertAlmostEqual(ratio_E_over_hbar_omega(h,h.u),ALPHA,12)
    def test_geometric_frequency_comoving(self):
        h=helix_for_alpha();self.assertAlmostEqual(geometric_frequency_boost_ratio(h,h.u),1/math.sqrt(ALPHA),12)
    def test_tangent_energy_comoving(self):
        h=helix_for_alpha();self.assertAlmostEqual(tangent_null_energy_boost_ratio(h,h.u),math.sqrt(ALPHA),12)
    def test_genuine_wave_doppler_factor(self):
        self.assertAlmostEqual(plane_wave_energy_frequency_ratio(.6),.5,14)
    def test_genuine_wave_doppler_at_zero(self):
        self.assertEqual(plane_wave_energy_frequency_ratio(0),1.0)
    def test_ratio_transform_algebra(self):
        h=helix_for_alpha(.2)
        for b in [-.9,-.3,0,.3,.6,.93]:
            D=(1-b*h.u)/math.sqrt(1-b*b)
            with self.subTest(beta=b):self.assertAlmostEqual(ratio_E_over_hbar_omega(h,b),D*D,12)
    def test_invalid_plane_wave_boost(self):
        with self.assertRaises(ValueError):plane_wave_energy_frequency_ratio(1)
    def test_invalid_tangent_boost(self):
        with self.assertRaises(ValueError):tangent_null_energy_boost_ratio(helix_for_alpha(),-1)
