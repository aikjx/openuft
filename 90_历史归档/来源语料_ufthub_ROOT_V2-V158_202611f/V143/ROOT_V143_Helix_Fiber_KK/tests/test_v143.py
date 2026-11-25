import cmath
import math
import unittest
from src.physics import (ALPHA,ELECTRON_MASS_KG,PLANCK_LENGTH_M,PLANCK_MASS_KG,
                         Helix,null_helix_example,alpha_from_mass,alpha_from_mass_planck,
                         mass_from_alpha_planck,circle_radius_from_alpha,mass_tower_ratio,
                         gauge_covariant_mode,coupling_matching,diagnostics)

class TestNullHelix(unittest.TestCase):
    def setUp(self): self.h=null_helix_example()
    def test_five_dimensional_null(self):self.assertAlmostEqual(self.h.v5_squared,1,places=14)
    def test_four_dimensional_subluminal(self):self.assertLess(self.h.v3_squared,1)
    def test_spatial_velocity(self):self.assertAlmostEqual(self.h.v3_squared,0.73)
    def test_internal_velocity(self):self.assertAlmostEqual(self.h.internal_speed**2,0.27)
    def test_curvature_exact(self):self.assertAlmostEqual(self.h.curvature,0.3/0.73)
    def test_torsion_exact(self):self.assertAlmostEqual(self.h.torsion,0.8/0.73)
    def test_general_helix_identity(self):
        self.assertAlmostEqual(self.h.v3_squared*(self.h.curvature**2+self.h.torsion**2),self.h.omega**2)
    def test_old_unit_speed_helix_identity_not_valid(self):
        self.assertGreater(abs(self.h.curvature**2+self.h.torsion**2-self.h.omega**2),0.1)
    def test_speed_one_3d_case(self):
        h=Helix(0.6,1,0.8,1,0)
        self.assertAlmostEqual(h.curvature**2+h.torsion**2,1)
        self.assertTrue(h.validate_null())
    def test_nonunit_spatial_speed_nonnull_5d(self):
        self.assertFalse(Helix(0.3,1,0.8,1,0).validate_null())
    def test_bad_zero_spatial_velocity(self):
        with self.assertRaises(ValueError):_=Helix(0,1,0,1,1).curvature
    def test_reconstruction_axial_rotation_positive(self):
        h=self.h
        omega_back=math.sqrt(h.v3_squared*(h.curvature**2+h.torsion**2))
        self.assertAlmostEqual(h.omega,omega_back)
    def test_reconstruction_negative_helicity(self):
        h=Helix(0.3,-1,0.8,2,math.sqrt(0.27)/2)
        self.assertLess(h.torsion,0)
        self.assertAlmostEqual(h.angle_frequency_from_geometry,1)
    def test_omega_from_curvature_reject_undefined(self):
        with self.assertRaises(ValueError):_=Helix(0,0,0,1,1).angle_frequency_from_geometry

class TestCircleGauge(unittest.TestCase):
    def test_local_fiber_gauge_invariance(self):
        # dphi+k A dx is gauge invariant: phi'=phi-k chi(x); A'=A+dchi.
        dphi, A, dchi, k = 0.4, 0.15, -0.31, 0.8
        self.assertAlmostEqual(dphi+k*A,(dphi-k*dchi)+k*(A+dchi))
    def test_covariant_mode_transformation_complex(self):
        n,k,A,dxchi=3,0.7,0.5,-0.9
        chi=0.4
        psi=complex(0.4,-0.25)
        deriv=complex(-0.2,0.3)
        phase=cmath.exp(1j*n*k*chi)
        newpsi=psi*phase
        newderiv=(deriv+1j*n*k*dxchi*psi)*phase
        lhs=gauge_covariant_mode(newderiv,newpsi,A+dxchi,n,k)
        rhs=phase*gauge_covariant_mode(deriv,psi,A,n,k)
        self.assertAlmostEqual(abs(lhs-rhs),0,places=13)
    def test_unit_k_consistency(self):
        # normalized g² scales as k^-2 while mode coupling nk scales as k.
        a=coupling_matching(0.2,0.4,1,1)
        b=coupling_matching(0.2,0.4,1,2)
        self.assertAlmostEqual(a/b,4)
    def test_dimensionless_g_squared(self):
        self.assertGreater(coupling_matching(1,1,1),0)
    def test_invalid_coupling_args(self):
        for vals in [(0,1,1,1),(1,0,1,1),(1,1,0,1),(1,1,1,0)]:
            with self.assertRaises(ValueError):coupling_matching(*vals)
    def test_mass_mode_n0(self):self.assertEqual(mass_tower_ratio(0,2),0)
    def test_mass_mode_scaling(self):self.assertEqual(mass_tower_ratio(-3,1),3)
    def test_mass_ratio_failure(self):
        with self.assertRaises(ValueError): mass_tower_ratio(1,0)

class TestMatterMassAndCoupling(unittest.TestCase):
    def test_alpha_mass_relation(self):
        # using mP=sqrt(hbar/G), so alpha=4(m/mP)^2
        x=0.1
        self.assertAlmostEqual(alpha_from_mass_planck(x,1),4*x*x)
    def test_alpha_mass_direct(self):
        self.assertAlmostEqual(alpha_from_mass(0.1,2,4),0.02)
    def test_reference_electron_alpha_is_tiny(self):
        self.assertLess(alpha_from_mass_planck(ELECTRON_MASS_KG),1e-43)
    def test_reference_observed_alpha_not_predicted(self):
        self.assertGreater(ALPHA/alpha_from_mass_planck(ELECTRON_MASS_KG),1e40)
    def test_matching_mass_is_heavy(self):
        self.assertGreater(mass_from_alpha_planck(ALPHA)/ELECTRON_MASS_KG,1e20)
    def test_match_identity(self):
        m=mass_from_alpha_planck(ALPHA)
        self.assertAlmostEqual(alpha_from_mass_planck(m),ALPHA,places=14)
    def test_radius_reference(self):
        self.assertGreater(circle_radius_from_alpha(ALPHA),PLANCK_LENGTH_M)
    def test_radius_n_scaling(self):
        self.assertAlmostEqual(circle_radius_from_alpha(ALPHA,2)/circle_radius_from_alpha(ALPHA,1),2)
    def test_bad_radius_alpha(self):
        with self.assertRaises(ValueError):circle_radius_from_alpha(0)
    def test_bad_radius_n(self):
        with self.assertRaises(ValueError):circle_radius_from_alpha(ALPHA,0)
    def test_negative_alpha(self):
        with self.assertRaises(ValueError):mass_from_alpha_planck(-1)
    def test_negative_mass(self):
        with self.assertRaises(ValueError):alpha_from_mass(-1,2,4)
    def test_reference_kg_consistency(self):
        self.assertLess(abs(PLANCK_MASS_KG-2.176434e-8),1e-16)
    def test_summary_clear_scientific_status(self):
        self.assertEqual(diagnostics()['status']['full_four_force_unification'],'NOT established')

class TestSymbolic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from src.symbolic_checks import main
        cls.res=main()
    def test_5D_ricci_computed_exactly(self):self.assertTrue(self.res['fiveD_Ricci']['passed'])
    def test_5D_ricci_expected_B2(self):self.assertIn('B**2',self.res['fiveD_Ricci']['ricci_scalar'])
    def test_5D_ricci_no_difference(self):self.assertEqual(self.res['fiveD_Ricci']['difference'],'0')
    def test_4D_maxwell(self):self.assertTrue(self.res['source_free_4D_photon']['passed'])
    def test_4D_source_current_zero(self):self.assertEqual(self.res['source_free_4D_photon']['divergence'],['0']*4)
    def test_4D_bianchi_zero(self):self.assertEqual(self.res['source_free_4D_photon']['bianchi'],['0']*4)
    def test_two_polarizations(self):self.assertEqual(len(self.res['source_free_4D_photon']['two_transverse_amplitudes']),2)
    def test_radius_scalar_source(self):self.assertTrue(self.res['radius_variation']['passed'])
    def test_radius_scalar_contains_F2(self):self.assertIn('F2',self.res['radius_variation']['radion_equation'])

if __name__=='__main__':unittest.main()
