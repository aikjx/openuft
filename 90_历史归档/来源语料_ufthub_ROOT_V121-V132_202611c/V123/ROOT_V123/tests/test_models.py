import unittest,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import calculate as c
class ModelTests(unittest.TestCase):
 def test_helix(self):
  for row in c.rows:self.assertAlmostEqual(row['identity_residual'],0,places=13)
 def test_spectrum(self):self.assertLess(c.err,1e-11)
 def test_gravity_scaling(self):self.assertAlmostEqual(c.out['gravity']['10']['mass_kg']/c.out['gravity']['1']['mass_kg'],100)
 def test_rotation(self):self.assertAlmostEqual(c.out['rotation']['1']['rpm_1g']/c.out['rotation']['100']['rpm_1g'],10)
 def test_magnetic_energy(self):self.assertAlmostEqual(c.out['magnet']['10']['field_energy_J']/c.out['magnet']['1']['field_energy_J'],100)
if __name__=='__main__':unittest.main()
