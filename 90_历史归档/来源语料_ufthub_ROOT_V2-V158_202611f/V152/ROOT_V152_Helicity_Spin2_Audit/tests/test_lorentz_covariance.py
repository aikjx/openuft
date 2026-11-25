import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from root_v152.core import *

class LorentzCovarianceTests(unittest.TestCase):
 def test_lorentz_metric(self):
  L=lorentz_boost_x(.4);self.assertTrue(np.allclose(L.T@ETA@L,ETA))
 def test_lorentz_inverse(self):
  self.assertTrue(np.allclose(lorentz_boost_x(.4)@lorentz_boost_x(-.4),np.eye(4)))
 def test_invalid_boost(self):
  with self.assertRaises(ValueError):lorentz_boost_x(1.1)
 def test_null_preserved(self):
  k,a=photon_amplitude(3,[1,2,3]);kt=transform_covector(lorentz_boost_x(.6),k);self.assertAlmostEqual(abs(kt@ETA@kt),0,places=12)
 def test_maxwell_field_tensor_covariance(self):
  k,a=photon_amplitude(2,[1,2,3]);L=lorentz_boost_x(.5)
  expected=transform_cov2(L,field_strength_fourier(k,a));actual=field_strength_fourier(transform_covector(L,k),transform_covector(L,a))
  self.assertTrue(np.allclose(actual,expected))
 def test_maxwell_equation_covariance(self):
  k,a=photon_amplitude(2,[1,2,3]);L=lorentz_boost_x(.5);F=field_strength_fourier(k,a)
  self.assertTrue(np.allclose(maxwell_fourier_residual(transform_covector(L,k),transform_cov2(L,F)),0,atol=1e-12))
 def test_spin2_einstein_covariance(self):
  k,h=spin2_tt_amplitude([1,2,3],2,2);L=lorentz_boost_x(.3)
  self.assertTrue(np.allclose(linearized_einstein(transform_covector(L,k),transform_cov2(L,h)),transform_cov2(L,linearized_einstein(k,h)),atol=1e-12))
 def test_spin2_curvature_covariance(self):
  k,h=spin2_tt_amplitude([1,2,3],2,2);L=lorentz_boost_x(.3)
  target=transform_cov4(L,linearized_riemann(k,h));actual=linearized_riemann(transform_covector(L,k),transform_cov2(L,h))
  self.assertTrue(np.allclose(actual,target,atol=1e-12))
 def test_minkowski_tensor_invariant(self):
  L=lorentz_boost_x(.8);self.assertTrue(np.allclose(transform_cov2(L,ETA),ETA))
 def test_photon_doppler_nontrivial(self):
  k,a=photon_amplitude(3,[0,0,1]);kt=transform_covector(lorentz_boost_x(.6),k)
  self.assertGreater(abs(kt[0]),abs(k[0]))
