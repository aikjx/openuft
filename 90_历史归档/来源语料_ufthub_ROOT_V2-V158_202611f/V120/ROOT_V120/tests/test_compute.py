import unittest,sys,pathlib,math
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
from compute import *
class Tests(unittest.TestCase):
 def test_helix(self):
  for w in (.1,.2,.4):
   h=helix(2,w,math.sqrt(1-4*w*w));self.assertAlmostEqual(h['speed'],1,places=13);self.assertAlmostEqual(h['identity_residual'],0,places=13)
 def test_point_mass(self):
  for r in (1,10,100):
   m=artificial(r)['equivalent_point_mass_kg'];self.assertAlmostEqual(G*m/r**2,g,places=10)
 def test_magnetic_scaling(self):
  self.assertAlmostEqual(magnetic(10,1)['ideal_uniform_field_energy_J']/magnetic(1,1)['ideal_uniform_field_energy_J'],100)
 def test_rotation(self):
  a=artificial(100);self.assertAlmostEqual((a['rotation_rpm']*2*math.pi/60)**2*100,g)
if __name__=='__main__':unittest.main()
