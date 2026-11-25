import unittest
from root_v146.units import (S,L,HBAR,G,K6,LAM6,CHI6,R6,F_SQUARED,
                             K4,V4,A,B,C,Dim)

class TestDimensions(unittest.TestCase):
    def test_hbar_retained(self): self.assertEqual(HBAR,S)
    def test_G_dimension_c1(self): self.assertEqual(G,L**2/S)
    def test_Einstein_6D_action(self): self.assertEqual(K6*R6*L**6,S)
    def test_vacuum_action(self): self.assertEqual(LAM6*L**6,S)
    def test_flux_action(self): self.assertEqual(CHI6*F_SQUARED*L**6,S)
    def test_Einstein_4D_action(self): self.assertEqual(K4*(L**-2)*L**4,S)
    def test_four_dimensional_cosmological_action(self): self.assertEqual(V4*L**4,S)
    def test_A_contribution(self): self.assertEqual(A/L**2,V4)
    def test_B_contribution(self): self.assertEqual(B/L**4,V4)
    def test_C_contribution(self): self.assertEqual(C/L**6,V4)
    def test_discriminant_dims(self): self.assertEqual(B**2,A*C)
    def test_mass_squared_dim(self): self.assertEqual((V4/K4),L**-2)
    def test_K4_to_G4(self): self.assertEqual(K4,Dim()/G)
    def test_radion_canonical_action(self): self.assertEqual(K4*L**-2*L**4,S)

if __name__=='__main__': unittest.main()
