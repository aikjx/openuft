import sys, unittest, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from root_v152.core import *

class FrameHelicityTests(unittest.TestCase):
 def test_frame_x(self): self.assertTrue(np.allclose(np.array(orthonormal_frame([1,0,0]))@np.array(orthonormal_frame([1,0,0])).T,np.eye(3)))
 def test_frame_z(self): self.assertTrue(np.allclose(np.array(orthonormal_frame([0,0,1]))@np.array(orthonormal_frame([0,0,1])).T,np.eye(3)))
 def test_frame_oblique(self): self.assertTrue(np.allclose(np.array(orthonormal_frame([1,2,3]))@np.array(orthonormal_frame([1,2,3])).T,np.eye(3)))
 def test_frame_right_handed(self):
  a,b,n=orthonormal_frame([2,3,4]);self.assertTrue(np.allclose(np.cross(a,b),n))
 def test_frame_unit_error(self):
  with self.assertRaises(ValueError): orthonormal_frame([0,0,0])
 def test_circular_norm(self):
  ep,em,_=circular_vectors([1,2,3]);self.assertAlmostEqual(np.vdot(ep,ep).real,1)
 def test_circular_orthogonal(self):
  ep,em,_=circular_vectors([1,2,3]);self.assertAlmostEqual(abs(np.vdot(ep,em)),0,places=12)
 def test_circular_complex_null(self):
  ep,_,_=circular_vectors([1,2,3]);self.assertAlmostEqual(abs(ep@ep),0,places=12)
 def test_circular_transverse(self):
  ep,em,n=circular_vectors([1,2,3]);self.assertAlmostEqual(abs(n@ep)+abs(n@em),0,places=12)
 def test_vector_phase_plus(self): self.assertTrue(np.allclose(vector_phase([0,0,1],.371)[0],np.exp(-1j*.371)))
 def test_vector_phase_minus(self): self.assertTrue(np.allclose(vector_phase([0,0,1],.371)[1],np.exp(1j*.371)))
 def test_tensor_phase_plus(self): self.assertTrue(np.allclose(tensor_phase([0,0,1],.371)[0],np.exp(-2j*.371)))
 def test_tensor_phase_minus(self): self.assertTrue(np.allclose(tensor_phase([0,0,1],.371)[1],np.exp(2j*.371)))
 def test_tensor_circular_trace(self):
  tp,tm,n=tensor_circular([1,2,3]);self.assertAlmostEqual(abs(np.trace(tp))+abs(np.trace(tm)),0,places=12)
 def test_tensor_transverse(self):
  tp,tm,n=tensor_circular([1,2,3]);self.assertTrue(np.allclose(tp@n,0) and np.allclose(tm@n,0))
 def test_tensor_norm(self):
  tp,tm,_=tensor_circular([0,0,1]);self.assertAlmostEqual(np.vdot(tp,tp).real,1);self.assertAlmostEqual(np.vdot(tm,tm).real,1)
 def test_tensor_orthogonal(self):
  tp,tm,_=tensor_circular([0,0,1]);self.assertAlmostEqual(abs(np.vdot(tp,tm)),0,places=12)
 def test_tt_traceless(self):self.assertAlmostEqual(np.trace(tt_project([1,1,1],np.array([[2,3,4],[3,5,1],[4,1,7.]]))),0,places=12)
 def test_tt_transverse(self):
  n=unit([1,2,3]);s=np.arange(9.).reshape(3,3);t=tt_project(n,(s+s.T)/2);self.assertTrue(np.allclose(t@n,0))
 def test_tt_symmetric(self):
  s=np.arange(9.).reshape(3,3);t=tt_project([1,2,3],(s+s.T)/2);self.assertTrue(np.allclose(t,t.T))
 def test_tt_idempotent(self):
  s=np.array([[2.,1,3],[1.,4,5],[3.,5,6]]);t=tt_project([1,3,4],s);self.assertTrue(np.allclose(tt_project([1,3,4],t),t))
 def test_tt_two_components(self):
  a,b=tensor_plus_cross([.3,.4,.5]);self.assertAlmostEqual(np.vdot(a,a),1);self.assertAlmostEqual(np.vdot(b,b),1);self.assertAlmostEqual(np.vdot(a,b),0)
 def test_spin_3_counterexample(self):
  ep,_,n=circular_vectors([0,0,1]);t=np.einsum('i,j,k->ijk',ep,ep,ep);R=rotation(n,.21);rot=np.einsum('ia,jb,kc,abc->ijk',R,R,R,t);self.assertTrue(np.allclose(rot,np.exp(-3j*.21)*t))
