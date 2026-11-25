import unittest, numpy as np
from src.design import fisher,templates,design_search
class TestDesign(unittest.TestCase):
 def test_orthogonal(self):
  x=fisher([0,0,1],[[1,0],[0,1],[0,0]],np.eye(3));self.assertAlmostEqual(x['information'],1)
 def test_degenerate(self):
  x=fisher([1,2,3],[[1],[2],[3]],np.eye(3));self.assertLess(x['information'],1e-25)
 def test_noise_scaling(self):
  a=fisher([0,1],[[1],[0]],np.eye(2));b=fisher([0,1],[[1],[0]],4*np.eye(2));self.assertAlmostEqual(a['information']/b['information'],4)
 def test_template_shapes(self):self.assertEqual(templates([.001,.002],.0001).shape,(2,3))
 def test_background_identical_to_signal(self):
  T=templates(np.linspace(.0002,.001,6),.00001);T=T/np.linalg.norm(T,axis=0);x=fisher(T[:,2],T,np.eye(6));self.assertLess(x['information'],1e-25)
 def test_invalid_covariance(self):
  with self.assertRaises(np.linalg.LinAlgError):fisher([1,2],[[1],[0]],[[1,2],[2,1]])
 def test_search(self):
  x=design_search(np.linspace(.0002,.001,9),.00001);self.assertEqual(len(x['radii_m']),5);self.assertGreater(x['information'],0)
if __name__=='__main__':unittest.main()
