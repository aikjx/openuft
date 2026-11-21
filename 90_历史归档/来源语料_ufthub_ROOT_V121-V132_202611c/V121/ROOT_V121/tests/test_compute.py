import unittest,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from compute import *
class TestPhysics(unittest.TestCase):
 def test_helix(self):
  for p in (0,.2,.5,.9):self.assertLess(abs(helix(3,p)['identity_residual']),1e-12)
 def test_spectrum(self):self.assertAlmostEqual(spectral(2*math.pi,.2,3),3.2)
 def test_gravity(self):self.assertAlmostEqual(gravity_mass(10)/gravity_mass(1),100)
 def test_rotation(self):self.assertAlmostEqual(rotation_rpm(100)/rotation_rpm(1),.1)
 def test_magnetic(self):self.assertAlmostEqual(magnetic(20,1)['stored_J']/magnetic(10,1)['stored_J'],4)
if __name__=='__main__':unittest.main()
