import math,unittest
from model import *
class Tests(unittest.TestCase):
 def test_surface_g(self):self.assertTrue(9.7<norm(gravity(ecef(0,0)))<9.9)
 def test_j2_pole_equator(self):self.assertNotAlmostEqual(norm(gravity(ecef(0,0))),norm(gravity(ecef(90,0))),places=3)
 def test_inverse_square(self):self.assertAlmostEqual(norm(gravity(ecef(0,0),False))/norm(gravity(ecef(0,0,R),False)),4.,places=10)
 def test_dipole_equator(self):self.assertAlmostEqual(norm(magnetic(ecef(0,0))),B_EQ,places=12)
 def test_dipole_pole(self):self.assertAlmostEqual(norm(magnetic(ecef(90,0))),2*B_EQ,places=12)
 def test_dipole_cube(self):self.assertAlmostEqual(norm(magnetic(ecef(0,0)))/norm(magnetic(ecef(0,0,R))),8.,places=10)
 def test_magnetic_orthogonal(self):
  v=(300.,100.,50.);f=forces(32,18,1000,1.,1.,v)
  self.assertAlmostEqual(dot(v,f['magnetic_N']),0.,places=9)
 def test_charge_sign(self):
  a=forces(10,20,0,0,1,(0,100,0));b=forces(10,20,0,0,-1,(0,100,0))
  self.assertEqual(a['magnetic_N'],mul(-1,b['magnetic_N']))
 def test_zero_charge(self):
  f=forces(20,20,0,2,0,(100,0,0),100)
  self.assertEqual(f['total_N'],f['gravity_N'])
 def test_centrifugal(self):
  self.assertEqual(norm(centrifugal(ecef(90,0)))<1e-10,True)
  self.assertGreater(norm(centrifugal(ecef(0,0))),0.03)
 def test_field_finite(self):
  for lat in [-90,-45,0,45,90]:
   f=fields(lat,30,500)
   self.assertTrue(all(math.isfinite(v) for vec in [f['gravity_m_s2'],f['magnetic_T']] for v in vec))
 def test_cross_orthogonal(self):
  a=(1,2,3);b=(4,5,6);c=cross(a,b)
  self.assertAlmostEqual(dot(a,c),0);self.assertAlmostEqual(dot(b,c),0)
if __name__=='__main__':unittest.main(verbosity=2)
