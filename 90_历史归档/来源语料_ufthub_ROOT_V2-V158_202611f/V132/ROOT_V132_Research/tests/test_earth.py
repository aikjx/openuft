import unittest,math,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
import earth as e
class EarthTests(unittest.TestCase):
 def test_inverse_square(self):
  self.assertAlmostEqual(e.norm(e.central((2*e.RE,0,0)))/e.norm(e.central((e.RE,0,0))),.25,places=13)
 def test_equator_pole(self):
  self.assertTrue(9.77<e.norm(e.effective((e.RE,0,0)))<9.80)
  self.assertTrue(9.82<e.norm(e.effective((0,0,e.RP)))<9.85)
 def test_gradient(self):
  p=(4.3e6,3.2e6,4.0e6)
  for a,b in zip(e.gravity(p),e.finite_diff_grad(p)):
   self.assertLess(abs(a-b),2e-8)
 def test_rotation(self):
  self.assertAlmostEqual(e.effective((0,0,e.RP))[2],e.gravity((0,0,e.RP))[2])
 def test_symmetry(self):
  a=e.gravity((e.RE,0,0));b=e.gravity((-e.RE,0,0))
  self.assertAlmostEqual(a[0],-b[0]);self.assertAlmostEqual(a[2],0)
 def test_mass(self): self.assertTrue(4e24<e.mass_layers(e.layers())<8e24)
 def test_yukawa_finite_size(self):
  r=6371000.
  v=e.yukawa_ratio_exterior(r,n=1000)
  self.assertGreater(v,0);self.assertLess(v,1)
  self.assertGreater(v,e.yukawa_point_ratio(r))
 def test_yukawa_monotonic(self):
  a=e.yukawa_ratio_exterior(6371000,n=600)
  b=e.yukawa_ratio_exterior(6771000,n=600)
  self.assertGreater(a,b)
 def test_yukawa_zero_alpha(self): self.assertEqual(e.yukawa_ratio_exterior(6371000,alpha=0,n=100),0)
 def test_yukawa_longrange(self):
  # lambda -> infinity: acceleration ratio tends to alpha for spherical exterior
  self.assertAlmostEqual(e.yukawa_ratio_exterior(6371000,lam=1e12,n=200),1/3,delta=1e-5)
 def test_gradient_random_points(self):
  for p in [(6.4e6,1.2e6,2e6),(-2e6,7e6,1e6),(1e6,2e6,7e6)]:
   self.assertLess(max(abs(a-b) for a,b in zip(e.gravity(p),e.finite_diff_grad(p))),2e-8)
 def test_energy_radial(self):
  r=7e6; self.assertAlmostEqual(e.dot(e.central((r,0,0)),(r,0,0)),-e.MU/r)
if __name__=='__main__': unittest.main()
