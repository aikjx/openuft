import unittest, subprocess,sys,json
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parents[1]
class Checks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  subprocess.run([sys.executable,str(B/'src/verify.py')],check=True,capture_output=True)
  cls.d=json.loads((B/'results/calculations.json').read_text())
 def test_positive_spectrum(self): self.assertGreater(min(self.d['eigenvalues']),0)
 def test_orthogonal(self): self.assertLess(self.d['orthogonality_residual'],1e-12)
 def test_diagonal(self): self.assertLess(self.d['diagonalization_residual'],1e-12)
 def test_dispersion(self): self.assertLess(max(x['dispersion_residual'] for x in self.d['dispersion']),1e-12)
 def test_group_speed(self): self.assertTrue(all(0<=x['group_speed']<=1 for x in self.d['dispersion']))
 def test_counterexample(self): self.assertLess(self.d['negative_mass_squared_counterexample'],0)
 def test_gravity(self): self.assertAlmostEqual(self.d['engineering']['point_mass_for_1g_at_1m_kg'],1.469e11,delta=1e8)
 def test_rotation(self): self.assertAlmostEqual(self.d['engineering']['rotating_100m_rpm'],2.99,delta=0.01)
if __name__=='__main__': unittest.main()
