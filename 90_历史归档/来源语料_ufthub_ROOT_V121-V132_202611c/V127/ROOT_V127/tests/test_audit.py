import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from audit import audit
import numpy as np
class AuditTests(unittest.TestCase):
 def test_canonical(self):
  a=audit(np.eye(3),np.eye(3),np.diag([0,1,4]),1);self.assertTrue(a['gradient_stable']);self.assertTrue(a['principal_speeds_leq_c']);self.assertTrue(a['no_tachyon_at_k'])
 def test_ghost(self):self.assertEqual(audit(np.diag([1,-1,1]),np.eye(3),np.eye(3),1)['status'],'ghost_or_singular_kinetic')
 def test_gradient(self):self.assertFalse(audit(np.eye(3),np.diag([1,-.2,1]),np.eye(3),3)['gradient_stable'])
 def test_tachyon(self):self.assertFalse(audit(np.eye(3),np.eye(3),np.diag([-1,1,1]),.1)['no_tachyon_at_k'])
 def test_superluminal(self):self.assertFalse(audit(np.eye(3),np.diag([1,1.2,1]),np.eye(3),1)['principal_speeds_leq_c'])
 def test_mixed(self):self.assertTrue(audit([[2,.2,0],[.2,1.5,.1],[0,.1,1.2]],np.eye(3),np.diag([.2,.5,1]),2)['no_tachyon_at_k'])
if __name__=='__main__':unittest.main()
