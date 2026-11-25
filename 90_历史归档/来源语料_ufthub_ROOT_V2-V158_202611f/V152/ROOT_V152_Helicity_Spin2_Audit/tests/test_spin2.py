import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from root_v152.core import *

class Spin2Tests(unittest.TestCase):
 def test_tt_null(self):
  k,h=spin2_tt_amplitude(frequency=2);self.assertAlmostEqual(abs(k@ETA@k),0)
 def test_tt_trace(self):
  k,h=spin2_tt_amplitude();self.assertAlmostEqual(abs(np.trace(ETA@h)),0)
 def test_tt_divergence(self):
  k,h=spin2_tt_amplitude();self.assertTrue(np.allclose((ETA@k)@h,0))
 def test_tt_plus_einstein(self):
  k,h=spin2_tt_amplitude(helicity=2);self.assertTrue(np.allclose(linearized_einstein(k,h),0))
 def test_tt_minus_einstein(self):
  k,h=spin2_tt_amplitude(helicity=-2);self.assertTrue(np.allclose(linearized_einstein(k,h),0))
 def test_tt_oblique_einstein(self):
  k,h=spin2_tt_amplitude([1,2,3],2,7);self.assertTrue(np.allclose(linearized_einstein(k,h),0,atol=1e-12))
 def test_riemann_antisym_first(self):
  k,h=spin2_tt_amplitude();R=linearized_riemann(k,h);self.assertTrue(np.allclose(R+R.swapaxes(0,1),0))
 def test_riemann_antisym_second(self):
  k,h=spin2_tt_amplitude();R=linearized_riemann(k,h);self.assertTrue(np.allclose(R+R.swapaxes(2,3),0))
 def test_riemann_pair_symmetry(self):
  k,h=spin2_tt_amplitude();R=linearized_riemann(k,h);self.assertTrue(np.allclose(R,R.transpose(2,3,0,1)))
 def test_riemann_nonzero(self):
  k,h=spin2_tt_amplitude();self.assertGreater(np.max(np.abs(linearized_riemann(k,h))),.1)
 def test_riemann_gauge_invariance(self):
  k,h=spin2_tt_amplitude([1,2,3],2,2);xi=np.array([.1,-.2,.3,.4]);R=linearized_riemann(k,h);R2=linearized_riemann(k,h+spin2_gauge_shift(k,xi));self.assertTrue(np.allclose(R,R2,atol=1e-13))
 def test_einstein_gauge_invariance(self):
  k,h=spin2_tt_amplitude([1,2,3],2,2);xi=np.array([.1,-.2,.3,.4]);self.assertTrue(np.allclose(linearized_einstein(k,h+spin2_gauge_shift(k,xi)),linearized_einstein(k,h),atol=1e-13))
 def test_einstein_bianchi_generic(self):
  k=np.array([-2.,1.,3.,4.]);s=np.arange(16.).reshape(4,4);h=(s+s.T)/2;self.assertTrue(np.allclose((ETA@k)@linearized_einstein(k,h),0,atol=1e-12))
 def test_riemann_tidal_component(self):
  k,h=spin2_tt_amplitude(frequency=4);R=linearized_riemann(k,h);self.assertAlmostEqual(abs(R[0,1,0,1]-.5*16*h[1,1]),0,places=12)
 def test_invalid_helicity(self):
  with self.assertRaises(ValueError):spin2_tt_amplitude(helicity=1)
 def test_plus_cross_tt(self):
  a,b=tensor_plus_cross([.1,.2,.7]);self.assertAlmostEqual(np.trace(a),0,places=12);self.assertAlmostEqual(np.trace(b),0,places=12)
 def test_gauge_nonzero_potentials_zero_curvature(self):
  k=np.array([-2.,0.,0.,2.]);xi=np.array([1.,2.,3.,4.]);h=spin2_gauge_shift(k,xi);self.assertGreater(np.linalg.norm(h),1);self.assertTrue(np.allclose(linearized_riemann(k,h),0))
