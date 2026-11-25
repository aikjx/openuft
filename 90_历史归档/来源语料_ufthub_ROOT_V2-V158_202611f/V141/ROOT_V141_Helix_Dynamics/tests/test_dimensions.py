import unittest
from src.field import lagrangian_density_units


class DimensionTests(unittest.TestCase):
    def test_gravity_unit(self): self.assertEqual(lagrangian_density_units()['gravity_R_over_Ghbar'],-4)
    def test_maxwell_unit(self): self.assertEqual(lagrangian_density_units()['Maxwell_F_squared'],-4)
    def test_scalar_unit(self): self.assertEqual(lagrangian_density_units()['scalar_f_squared_gradtheta_squared'],-4)
    def test_topological_unit(self): self.assertEqual(lagrangian_density_units()['axion_theta_F_dualF'],-4)
    def test_G_hbar_dimension(self): self.assertEqual(lagrangian_density_units()['G_times_hbar'],2)
    def test_d4x_dimension(self): self.assertEqual(lagrangian_density_units()['d4x'],4)
    def test_theta_dimensionless(self): self.assertEqual(lagrangian_density_units()['theta'],0)
    def test_kinetic_prefactor_f(self): self.assertEqual(lagrangian_density_units()['f'],-1)
    def test_no_hbar_equals_one(self):
        self.assertEqual(lagrangian_density_units()['gravity_R_over_Ghbar']+lagrangian_density_units()['d4x'],0)


if __name__=='__main__': unittest.main()
