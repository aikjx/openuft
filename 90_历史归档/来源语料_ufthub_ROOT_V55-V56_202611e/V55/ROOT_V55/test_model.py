import unittest,math
from model import *
class TestFields(unittest.TestCase):
 def test_surface_g(self): self.assertAlmostEqual(norm(fields((R,0,0))['g']),9.82,delta=.03)
 def test_inverse_square(self): self.assertAlmostEqual(norm(fields((2*R,0,0))['g'])/norm(fields((R,0,0))['g']),.25)
 def test_dipole_equator(self): self.assertAlmostEqual(norm(fields((R,0,0))['B']),B_EQ)
 def test_dipole_pole(self): self.assertAlmostEqual(norm(fields((0,0,R))['B']),2*B_EQ)
 def test_magnetic_perpendicular(self):
  v=(1200,400,50);b=fields((R,0,0))['B'];self.assertAlmostEqual(dot(cross(v,b),v),0,places=10)
 def test_zero_charge(self):
  f=forces((R,0,0),(0,1000,0),2,0);self.assertEqual(f['Fe'],(0,0,0));self.assertEqual(f['Fb'],(0,0,0))
 def test_superposition(self):
  f=forces((R,0,0),(0,1000,0),1,1e-6,(0,100,0));self.assertEqual(f['Ftotal'],add(f['Fg'],f['Fe'],f['Fb']))
 def test_bad_interior(self):
  with self.assertRaises(ValueError):fields((0,0,0))
if __name__=='__main__':unittest.main(verbosity=2)
