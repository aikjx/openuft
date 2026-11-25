import unittest
from fractions import Fraction
from root_v148.units import *

class UnitsTests(unittest.TestCase):
    def test_hbar_dimension(self):self.assertEqual(HBAR,(1,1))
    def test_G_dimension(self):self.assertEqual(G,(-1,1))
    def test_kappa_and_omega_same(self):self.assertEqual(KAPPA,OMEGA)
    def test_photon_energy(self):self.assertEqual(PHOTON_ENERGY,ENERGY)
    def test_curvature_energy(self):self.assertEqual(CURVATURE_ENERGY,ENERGY)
    def test_planck_mass(self):self.assertEqual(PLANCK_MASS,ENERGY)
    def test_gravity_action(self):self.assertEqual(GRAVITATIONAL_ACTION,HBAR)
    def test_dimensionless_u(self):self.assertEqual((0,0),(0,0))
    def test_g_not_dimensionless(self):self.assertNotEqual(G,(0,0))
    def test_hbar_not_dimensionless(self):self.assertNotEqual(HBAR,(0,0))
