"""Run with: python -m unittest discover -s tests -v"""
import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.gravity_c import *


class TestInputs(unittest.TestCase):
    def test_c_exact_SI(self): self.assertEqual(C, 299792458)
    def test_G_CODATA2022(self): self.assertEqual(G, 6.67430e-11)
    def test_uG_CODATA2022(self): self.assertEqual(SIGMA_G, 1.5e-15)
    def test_h_exact(self): self.assertEqual(H, 6.62607015e-34)
    def test_hbar(self): self.assertAlmostEqual(HBAR*2*math.pi/H, 1, places=14)
    def test_positive_masses(self): self.assertGreater(MPROTON,ME)
    def test_earth_GM(self): self.assertAlmostEqual(GM_EARTH/1e14,3.98600435507,places=10)


class TestDimensionalAnalysis(unittest.TestCase):
    def test_dim_z(self): self.assertEqual(dim_mul(('G',1),('c',1)),dimensional_power('Z'))
    def test_dim_alpha(self):
        self.assertEqual(dim_mul(('G',1),('mass',2),('hbar',-1),('c',-1)),(0,0,0))
    def test_dim_planck_length_squared(self):
        self.assertEqual(dim_mul(('hbar',1),('G',1),('c',-3)),(2,0,0))
    def test_dim_newton_constant_from_radius(self):
        self.assertEqual(dim_mul(('c',2),('length',1),('mass',-1)),dimensional_power('G'))
    def test_dim_G_from_planck(self):
        self.assertEqual(dim_mul(('c',3),('length',2),('hbar',-1)), dimensional_power('G'))
    def test_dim_einstein_coupling(self):
        self.assertEqual(dim_mul(('G',1),('c',-4)), dimensional_power('kappa_E'))
    def test_impossible_c_hbar_only(self):
        self.assertFalse(dimensional_no_go_c_hbar()['possible'])
        self.assertEqual(dimensional_no_go_c_hbar()['time_exponent_obtained'],-4)
    def test_no_negative_dimensionless(self): self.assertEqual(dimensional_power('alpha_g'),(0,0,0))


class TestOriginalROOTRelation(unittest.TestCase):
    def test_z_numerical(self): self.assertAlmostEqual(z_from_g(),0.010004524012147,places=14)
    def test_z_inverse(self): self.assertAlmostEqual(g_from_z(z_from_g())/G,1,places=14)
    def test_z_uncertainty(self): self.assertAlmostEqual(z_measured().sigma/(SIGMA_G*C/2),1,places=14)
    def test_z_units(self): self.assertIn('kg^-1', z_measured().unit)
    def test_z_const_0p01_diff(self): self.assertLess(one_percent_z_hypothesis()['sigma_residual'],-20)
    def test_z_const_0p01_rel(self): self.assertLess(one_percent_z_hypothesis()['relative_residual'],-4e-4)
    def test_unrelated_z_parameter(self):
        for z in [1e-10,0.0001,0.01,123]:
            with self.subTest(z=z): self.assertAlmostEqual(g_from_z(z)*C/(2*z),1)


class TestRelativity(unittest.TestCase):
    def test_earth_gravitational_length(self): self.assertAlmostEqual(earth_geometric_radius(),0.0044350279691,places=11)
    def test_earth_r_s(self): self.assertAlmostEqual(2*earth_geometric_radius(),0.0088700559382,places=11)
    def test_schwarz_radius_mass(self): self.assertAlmostEqual(schwarzschild_radius(100),2*gravitational_radius(100))
    def test_G_from_radius(self):
        r=gravitational_radius(1e21)
        self.assertAlmostEqual(g_from_gravitational_radius(r,1e21)/G,1)
    def test_einstein_coupling(self): self.assertAlmostEqual(einstein_coupling()/2.0766474428449717e-43,1)
    def test_earth_g(self): self.assertAlmostEqual(newton_gravity_accel(GM_EARTH,R_EARTH),9.82025033202437)
    def test_earth_mass_not_independent(self): self.assertAlmostEqual(G*earth_mass_inferred()/GM_EARTH,1,places=14)
    def test_G_from_surface_accel(self):
        m=earth_mass_inferred()
        g=newton_gravity_accel(GM_EARTH,R_EARTH)
        self.assertAlmostEqual(g_from_surface_accel(g,R_EARTH,m)/G,1)


class TestQuantumGravityRelations(unittest.TestCase):
    def test_planck_length(self): self.assertAlmostEqual(planck_length()/1.6162550244e-35,1,places=10)
    def test_planck_mass(self): self.assertAlmostEqual(planck_mass()/2.1764343427e-8,1,places=10)
    def test_planck_length_inversion(self): self.assertAlmostEqual(g_from_length(planck_length())/G,1,places=14)
    def test_planck_mass_inversion(self): self.assertAlmostEqual(g_from_mass(planck_mass())/G,1,places=14)
    def test_planck_mass_c_equals_hbar_over_length(self):
        self.assertAlmostEqual(planck_mass()*C*planck_length()/HBAR,1,places=14)
    def test_planck_radius_equals_compton(self):
        self.assertAlmostEqual(gravitational_radius(planck_mass())/reduced_compton_wavelength(planck_mass()),1)
    def test_alpha_e(self): self.assertAlmostEqual(gravitational_alpha(ME)/1.75180939879e-45,1,places=10)
    def test_alpha_p(self): self.assertAlmostEqual(gravitational_alpha(MPROTON)/5.90614942977e-39,1,places=10)
    def test_ratio_gravity_compton_e(self):
        vals=mass_radius_consistency(ME)
        self.assertAlmostEqual(vals['ratio']/vals['alpha_g'],1,places=14)
    def test_ratio_gravity_compton_p(self):
        vals=mass_radius_consistency(MPROTON)
        self.assertAlmostEqual(vals['ratio']/vals['alpha_g'],1,places=14)
    def test_electron_compton_scale(self): self.assertAlmostEqual(reduced_compton_wavelength(ME)/3.861592674e-13,1,places=9)
    def test_electron_wrong_equality(self): self.assertLess(mass_radius_consistency(ME)['ratio'],1e-44)
    def test_alpha_mass_squared(self):
        self.assertAlmostEqual(gravitational_alpha(MPROTON)/gravitational_alpha(ME)/(MPROTON/ME)**2,1)
    def test_G_alpha_inversion(self):
        self.assertAlmostEqual(g_from_gravitational_alpha(gravitational_alpha(MPROTON),MPROTON)/G,1)
    def test_G_length_scaling_quadratic(self):
        l=planck_length()
        self.assertAlmostEqual(g_from_length(2*l)/g_from_length(l),4)
    def test_uncertainty_planck_length_half_G(self):
        # linear error propagation of a square-root function
        self.assertAlmostEqual(0.5*relative_g_uncertainty(), SIGMA_G/(2*G))


class TestConditionalVaryingC(unittest.TestCase):
    def test_scale_at_one(self):
        vals=c_scaling_models(1)
        self.assertTrue(all(abs(v/G-1)<1e-14 for v in vals.values()))
    def test_fixed_Z_inverse(self): self.assertAlmostEqual(c_scaling_models(2)['fixed_Z']/G,0.5)
    def test_fixed_radius_quadratic(self): self.assertAlmostEqual(c_scaling_models(2)['fixed_gravitational_radius_and_mass']/G,4)
    def test_fixed_planck_length_cubic(self): self.assertAlmostEqual(c_scaling_models(2)['fixed_planck_length_and_hbar']/G,8)
    def test_fixed_G(self): self.assertEqual(c_scaling_models(0.5)['fixed_G'],G)
    def test_zero_rejected(self):
        with self.assertRaises(ValueError): c_scaling_models(0)
    def test_negative_rejected(self):
        with self.assertRaises(ValueError): c_scaling_models(-1)
    def test_sensitivity_Z(self):
        eps=1e-5
        f=lambda u: c_scaling_models(u)['fixed_Z']/G
        slope=(math.log(f(1+eps))-math.log(f(1-eps)))/(math.log(1+eps)-math.log(1-eps))
        self.assertAlmostEqual(slope,-1,places=7)
    def test_sensitivity_radius(self):
        eps=1e-5
        f=lambda u: c_scaling_models(u)['fixed_gravitational_radius_and_mass']/G
        slope=(math.log(f(1+eps))-math.log(f(1-eps)))/(math.log(1+eps)-math.log(1-eps))
        self.assertAlmostEqual(slope,2,places=7)
    def test_sensitivity_length(self):
        eps=1e-5
        f=lambda u: c_scaling_models(u)['fixed_planck_length_and_hbar']/G
        slope=(math.log(f(1+eps))-math.log(f(1-eps)))/(math.log(1+eps)-math.log(1-eps))
        self.assertAlmostEqual(slope,3,places=7)
    def test_invariant_variation(self):
        self.assertAlmostEqual(dimensionless_variation(.02,.01,0,.04),0)
    def test_dimless_alpha_c_change_only(self):
        self.assertAlmostEqual(dimensionless_variation(c_fraction=.01),-.01)

if __name__=='__main__': unittest.main()
