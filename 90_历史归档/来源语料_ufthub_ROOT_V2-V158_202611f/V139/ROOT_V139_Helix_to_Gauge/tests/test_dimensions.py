import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dimensions import *

class TestDimensions(unittest.TestCase):
    def test_hbar_is_dimensionful(self):self.assertEqual(hbar,D(1,1))
    def test_G_dimensionful(self):self.assertEqual(G,D(-1,1))
    def test_R_over_G(self):self.assertEqual(R/G,expected_density)
    def test_maxwell_density(self):self.assertEqual(hbar*F**2,expected_density)
    def test_phase_density(self):self.assertEqual(hbar*f**2*A**2,expected_density)
    def test_integrated_action(self):self.assertEqual(expected_density*L**4,hbar)
    def test_force(self):self.assertEqual(M/L,D(1,-1))
    def test_reciprocal(self):self.assertEqual((M/L)/(G),D(2,-2))
    def test_audit(self):self.assertEqual(audit()['action_integrated'],{'mass_power':1,'length_power':1})
