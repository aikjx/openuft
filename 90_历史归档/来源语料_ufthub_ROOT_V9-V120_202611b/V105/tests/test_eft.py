import unittest,math
from src.eft import PhaseEFT,DIMENSIONS

class EFTTests(unittest.TestCase):
 def setUp(self):self.x=PhaseEFT(1000.,1.,.1,.2,.3)
 def test_mass_positive(self):self.assertGreater(self.x.canon_mass_GeV(),0)
 def test_mass_exact(self):self.assertAlmostEqual(self.x.canon_mass_GeV(),.001)
 def test_periodicity(self):self.assertAlmostEqual(self.x.potential_GeV4(.3),self.x.potential_GeV4(.3+2*math.pi),places=12)
 def test_potential_minimum(self):self.assertAlmostEqual(self.x.potential_GeV4(0),0)
 def test_potential_nonnegative(self):self.assertGreaterEqual(self.x.potential_GeV4(.8),0)
 def test_potential_derivative(self):
  d=1e-5; v=(self.x.potential_GeV4(.3+d)-self.x.potential_GeV4(.3-d))/(2*d)
  self.assertAlmostEqual(v,self.x.potential_prime_GeV4(.3),places=8)
 def test_source_zero(self):self.assertAlmostEqual(self.x.source_GeV4(),0)
 def test_source_linear(self):self.assertAlmostEqual(self.x.source_GeV4(1,2,3),(.1+2*.2+3*.3)/4)
 def test_theta_accel_zero(self):self.assertAlmostEqual(self.x.theta_acceleration_GeV2(0),0)
 def test_theta_accel_restoring(self):self.assertLess(self.x.theta_acceleration_GeV2(.1),0)
 def test_theta_accel_external(self):self.assertAlmostEqual(self.x.theta_acceleration_GeV2(0,4,0,0),-0.1/1000**2)
 def test_invalid_f(self):
  with self.assertRaises(ValueError):PhaseEFT(0,1)
 def test_invalid_Lambda(self):
  with self.assertRaises(ValueError):PhaseEFT(1,-1)
 def test_zero_coupling(self):self.assertEqual(PhaseEFT(1000,1).source_GeV4(1,2,3),0)
 def test_zero_potential(self):self.assertEqual(PhaseEFT(1000,0).canon_mass_GeV(),0)
 def test_free_flat_theta(self):self.assertEqual(PhaseEFT(1000,0).theta_acceleration_GeV2(.5),0)
 def test_dim_scalar(self):self.assertEqual(DIMENSIONS['theta'],0)
 def test_dim_curvature(self):self.assertEqual(DIMENSIONS['Frenet_curvature'],1)
 def test_dim_riemann(self):self.assertEqual(DIMENSIONS['Riemann_curvature'],2)
 def test_dim_gauge(self):self.assertEqual(DIMENSIONS['gauge_curvature'],2)
 def test_dim_FF(self):self.assertEqual(2*DIMENSIONS['F_mu_nu'],DIMENSIONS['lagrangian_density'])
 def test_dim_f_kinetic(self):self.assertEqual(2*DIMENSIONS['f']+2*DIMENSIONS['partial_mu'],4)
 def test_dim_mass(self):self.assertEqual(2*DIMENSIONS['Lambda']-DIMENSIONS['f'],1)
 def test_action_dimensionless(self):self.assertEqual(DIMENSIONS['d4x']+DIMENSIONS['lagrangian_density'],0)
 def test_kinetic_mass_decouple(self):self.assertLess(PhaseEFT(1e6,1).canon_mass_GeV(),self.x.canon_mass_GeV())
