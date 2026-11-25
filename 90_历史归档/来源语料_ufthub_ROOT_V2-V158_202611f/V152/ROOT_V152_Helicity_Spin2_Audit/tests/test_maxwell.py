import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from root_v152.core import *

class MaxwellTests(unittest.TestCase):
 def test_k_null(self):
  k,a=photon_amplitude(4);self.assertAlmostEqual(abs(k@ETA@k),0)
 def test_k_transverse(self):
  k,a=photon_amplitude(4);self.assertAlmostEqual(abs(k@ETA@a),0)
 def test_photon_plus(self):
  k,a=photon_amplitude(3,helicity=1);self.assertTrue(np.allclose(maxwell_fourier_residual(k,field_strength_fourier(k,a)),0))
 def test_photon_minus(self):
  k,a=photon_amplitude(3,helicity=-1);self.assertTrue(np.allclose(maxwell_fourier_residual(k,field_strength_fourier(k,a)),0))
 def test_photon_oblique(self):
  k,a=photon_amplitude(3,[1,2,3]);self.assertTrue(np.allclose(maxwell_fourier_residual(k,field_strength_fourier(k,a)),0))
 def test_antisymmetry(self):
  k,a=photon_amplitude(3);F=field_strength_fourier(k,a);self.assertTrue(np.allclose(F+F.T,0))
 def test_gauge_invariance_real(self):
  k,a=photon_amplitude(3);self.assertTrue(np.allclose(field_strength_fourier(k,a),field_strength_fourier(k,a+1.27*k)))
 def test_gauge_invariance_complex(self):
  k,a=photon_amplitude(3);self.assertTrue(np.allclose(field_strength_fourier(k,a),field_strength_fourier(k,a+(.5+.9j)*k)))
 def test_null_frequency_condition_required(self):
  k,a=photon_amplitude(3);k[0]*=1.4;self.assertGreater(np.linalg.norm(maxwell_fourier_residual(k,field_strength_fourier(k,a))),.1)
 def test_longitudinal_pure_gauge(self):
  k,a=photon_amplitude(3);self.assertTrue(np.allclose(field_strength_fourier(k,k),0))
 def test_k_cov_sign(self):
  k,a=photon_amplitude(7,[0,0,1]);self.assertTrue(np.allclose(k,[-7,0,0,7]))
 def test_invalid_helicity(self):
  with self.assertRaises(ValueError):photon_amplitude(1,helicity=0)
 def test_invalid_frequency(self):
  with self.assertRaises(ValueError):photon_amplitude(0)
 def test_e_dot_b(self):
  for phi in np.linspace(0,2*np.pi,17):
   E=np.array([np.cos(phi),np.sin(phi),0]);B=np.cross([0,0,1],E);self.assertAlmostEqual(E@B,0,places=14)
 def test_poynting_axis(self):
  for phi in np.linspace(0,2*np.pi,13):
   E=np.array([np.cos(phi),np.sin(phi),0]);B=np.cross([0,0,1],E);self.assertTrue(np.allclose(np.cross(E,B),[0,0,1]))
