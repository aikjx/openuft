import unittest
from src.unit_audit import *
class TestDimensions(unittest.TestCase):
 def test_01_hbar(self):self.assertEqual(hbar,Dim(1,1))
 def test_02_G(self):self.assertEqual(G,Dim(-1,1))
 def test_03_curvature(self):self.assertEqual(curvature,Dim(0,-2))
 def test_04_F(self):self.assertEqual(F,Dim(0,-2))
 def test_05_Einstein(self):self.assertEqual(EinsteinAction,hbar)
 def test_06_Maxwell(self):self.assertEqual(MaxwellAction,hbar)
 def test_07_helix(self):self.assertEqual(helix_kappa,helix_omega)
 def test_08_dimless_square(self):self.assertEqual(F*F*d4x,ONE)
