import unittest
from src.numerical_lab import efield_straight_analytic, rk4_magnetic
from src.helix_physics import C
class TestIndependentDynamics(unittest.TestCase):
 def test_rk4_full_orbit(self):
  for B in (.3,.5,.7):
   d=rk4_magnetic(B,steps=3000)
   self.assertLess(d['error_in_radii'],1e-8)
   self.assertLess(d['momentum_rel_drift'],1e-10)
 def test_electric_straight_nonzero_force_zero_curvature(self):
  for t in (1e-12,1e-10,1e-8):
   d=efield_straight_analytic(t)
   self.assertGreater(d['field_force_N'],0)
   self.assertEqual(d['spatial_curvature_inverse_m'],0)
   self.assertLess(d['speed_m_s'],C)
 def test_electric_small_time_limit(self):
  d=efield_straight_analytic(1e-15)
  from src.helix_physics import E_CHARGE,M_E
  a=E_CHARGE*1e5/M_E
  self.assertAlmostEqual(d['speed_m_s']/(a*1e-15),1,places=6)
if __name__=='__main__':unittest.main()
