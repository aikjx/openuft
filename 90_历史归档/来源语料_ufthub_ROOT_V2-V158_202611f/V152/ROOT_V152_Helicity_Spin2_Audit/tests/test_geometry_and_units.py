import sys,unittest,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from root_v152.core import *

class GeometryAndUnitsTests(unittest.TestCase):
 def test_c_equal_one(self):self.assertAlmostEqual(helical_geometry(.6,1,.8)['v'],1)
 def test_curvature(self):self.assertAlmostEqual(helical_geometry(.6,1,.8)['kappa'],.6)
 def test_torsion(self):self.assertAlmostEqual(helical_geometry(.6,1,.8)['tau'],.8)
 def test_general_helix_identity(self):self.assertAlmostEqual(helical_geometry(.6,3,.8)['identity_residual'],0,places=12)
 def test_planar_circle(self):self.assertAlmostEqual(helical_geometry(2,.5,0)['tau'],0)
 def test_errors_radius(self):
  with self.assertRaises(ValueError):helical_geometry(0,1,0)
 def test_errors_freq(self):
  with self.assertRaises(ValueError):helical_geometry(2,0,0)
 def test_dimensions_grav(self):self.assertEqual(dimensional_audit()['L_grav'],(-4,1))
 def test_dimensions_maxwell(self):self.assertEqual(dimensional_audit()['L_maxwell'],(-4,1))
 def test_action_hbar(self):self.assertEqual(dimensional_audit()['action'],(0,1))
 def test_dimensions_g(self):self.assertEqual(dimensional_audit()['G'],(2,-1))
 def test_gravitational_wave_arm(self):self.assertAlmostEqual(simple_gravitational_wave()['one_arm_displacement_amplitude_m'],2e-18,places=27)
 def test_gravitational_wave_differential(self):self.assertAlmostEqual(simple_gravitational_wave()['x_minus_y_displacement_amplitude_m'],4e-18,places=27)
 def test_wavelength(self):self.assertAlmostEqual(simple_gravitational_wave()['wavelength_m'],2997924.58)
 def test_tidal_positive(self):self.assertGreater(simple_gravitational_wave()['tidal_acceleration_amplitude_m_s2'],0)
 def test_wrong_wave_frequency(self):
  with self.assertRaises(ValueError):simple_gravitational_wave(f_hz=-1)
 def test_helicity_not_unique(self):
  import numpy as np
  a=vector_phase([0,0,1],.1)[0];b=tensor_phase([0,0,1],.1)[0];self.assertTrue(np.allclose(b,a*a))
