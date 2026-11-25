import unittest,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import *
class ModelTests(unittest.TestCase):
 def test_signs(self):
  self.assertTrue(all(v>0 for v in phase_terms().values()))
 def test_scaling_mass(self):
  a=phase_terms(m=1e-14);b=phase_terms(m=2e-14)
  self.assertAlmostEqual(b['newton_rad']/a['newton_rad'],4)
  self.assertAlmostEqual(b['pn_illustrative_rad']/a['pn_illustrative_rad'],8)
  self.assertAlmostEqual(b['eft_illustrative_rad']/a['eft_illustrative_rad'],4)
 def test_time(self):
  a=phase_terms();b=phase_terms(t=2)
  for k in a:self.assertAlmostEqual(b[k]/a[k],2)
 def test_nulling(self):
  r=[1.,2.,3.];w=weights(r)
  self.assertAlmostEqual(sum(w[i]/r[i] for i in range(3)),0,places=12)
  self.assertAlmostEqual(sum(w[i]/r[i]**2 for i in range(3)),0,places=12)
  self.assertAlmostEqual(sum(w[i]/r[i]**3 for i in range(3)),1,places=12)
 def test_nonidentifiability(self):
  r=[1.,2.,3.]
  self.assertAlmostEqual(diagnostic(r,[2/x+3/x**2 for x in r]),0,places=12)
 def test_validation(self):
  with self.assertRaises(ValueError):phase_terms(r=-1)
  with self.assertRaises(ValueError):weights([1,1,2])
if __name__=='__main__':unittest.main()
