import math
import unittest
from fractions import Fraction
from src.root_v68 import *

class HelixProofs(unittest.TestCase):
    def test_pure_circle(self):
        h=helix(2,0,10);self.assertAlmostEqual(h['v_z'],0);self.assertAlmostEqual(h['omega'],5)
    def test_circular_curvature(self):self.assertAlmostEqual(helix(2,0,10)['kappa'],0.5)
    def test_circular_torsion(self):self.assertAlmostEqual(helix(2,0,10)['tau'],0)
    def test_circular_accel(self):self.assertAlmostEqual(helix(2,0,10)['accel'],50)
    def test_axis_line_degeneracy(self):self.assertAlmostEqual(helix(2,90,10)['kappa'],0,places=12)
    def test_negative_torsion(self):self.assertLess(helix(2,-45,10)['tau'],0)
    def test_positive_torsion(self):self.assertGreater(helix(2,45,10)['tau'],0)
    def test_speed_constraint(self):
        for ang in [-90,-78,-45,0,12,34,89,90]:self.assertAlmostEqual(helix(3,ang,11)['speed'],11,places=12)
    def test_inverse_helix(self):
        for angle in [-75,-35,0,25,55,88]:
            h=helix(2.3,angle,10)
            x=helix_inverse(h['kappa'],h['tau'],10)
            self.assertAlmostEqual(x['radius'],2.3,places=11)
            self.assertAlmostEqual(x['angle_degrees'],angle,places=11)
    def test_inverse_frequency(self):
        h=helix(4.,26.,9.);self.assertAlmostEqual(helix_inverse(h['kappa'],h['tau'],9)['omega'],h['omega'])
    def test_inverse_degenerate_rejected(self):
        with self.assertRaises(ValueError):helix_inverse(0,0)
    def test_radius_invalid(self):
        with self.assertRaises(ValueError):helix(0,30)
    def test_angle_invalid(self):
        with self.assertRaises(ValueError):helix(2,95)
    def test_dimensional_no_go(self):
        self.assertFalse(dimensional_obstruction()['possible'])
        self.assertEqual(dimensional_obstruction()['time_derived_sum'],4)
    def test_theta_component(self):self.assertAlmostEqual(helix(1,60,8)['v_theta'],4)
    def test_axial_component(self):self.assertAlmostEqual(helix(1,30,8)['v_z'],4)

class InducedGravity(unittest.TestCase):
    def test_e1_one(self):self.assertAlmostEqual(expint_e1(1),0.2193839343955203,places=12)
    def test_e1_small(self):self.assertAlmostEqual(expint_e1(.01),4.037929576538114,places=12)
    def test_e1_large(self):self.assertAlmostEqual(expint_e1(10),4.156968929685325e-6,places=16)
    def test_f_zero(self):self.assertEqual(heat_kernel_f(0),1)
    def test_f_one(self):self.assertAlmostEqual(heat_kernel_f(1),0.148495506775922,places=12)
    def test_f_is_decreasing(self):
        vals=[heat_kernel_f(x) for x in [0,.1,.2,.6,1,3,10]]
        self.assertTrue(all(a>b for a,b in zip(vals,vals[1:])))
    def test_f_positive(self):self.assertGreater(heat_kernel_f(5),0)
    def test_f_bounded(self):self.assertTrue(all(0<=heat_kernel_f(x)<=1 for x in [0,.01,.2,2,10]))
    def test_f_negative_invalid(self):
        with self.assertRaises(ValueError):heat_kernel_f(-1)
    def test_G_fit(self):self.assertAlmostEqual(induced_g(1,0,reverse_fitted_length(1,0))/G_OBS,1,places=12)
    def test_fit_degeneracy_n(self):
        x=reverse_fitted_length(1,0);self.assertAlmostEqual(induced_g(4,0,2*x)/induced_g(1,0,x),1)
    def test_fit_degeneracy_xi(self):
        a=reverse_fitted_length(1,0);b=reverse_fitted_length(2,.05)
        self.assertAlmostEqual(induced_g(1,0,a)/induced_g(2,.05,b),1)
    def test_G_scales_ell_squared(self):
        x=1e-35;self.assertAlmostEqual(induced_g(1,0,2*x)/induced_g(1,0,x),4)
    def test_G_mass_threshold_increases(self):
        x=1e-35;self.assertGreater(induced_g(1,0,x,.6),induced_g(1,0,x,0))
    def test_bare_term(self):
        x=1e-35;g=induced_g(1,0,x);self.assertAlmostEqual(induced_g(1,0,x,bare_inv_g=1/g),g/2)
    def test_unphysical_negative_inv(self):
        with self.assertRaises(ValueError):induced_g(1,.2,1e-35)
    def test_unphysical_n(self):
        with self.assertRaises(ValueError):induced_g(0,0,1e-35)
    def test_reverse_fit_xi_invalid(self):
        with self.assertRaises(ValueError):reverse_fitted_length(1,1/6)
    def test_planck_length(self):self.assertAlmostEqual(planck_length(),1.616255e-35,delta=1e-40)
    def test_dimensional_scale(self):
        l=planck_length();self.assertAlmostEqual(C**3*l*l/HBAR/G_OBS,1,places=12)

class GaugeTests(unittest.TestCase):
    def test_anomaly_cubic(self):self.assertEqual(anomaly_coefficients()['U1_cubed'],0)
    def test_anomaly_grav(self):self.assertEqual(anomaly_coefficients()['gravity_squared_U1'],0)
    def test_anomaly_su3(self):self.assertEqual(anomaly_coefficients()['SU3_squared_U1'],0)
    def test_anomaly_su2(self):self.assertEqual(anomaly_coefficients()['SU2_squared_U1'],0)
    def test_global_doublets(self):self.assertEqual(anomaly_coefficients()['SU2_doublets']%2,0)
    def test_incomplete_spectrum_anomalous(self):
        spec=(('Q',3,2,Fraction(1,6)),)
        self.assertNotEqual(anomaly_coefficients(spec)['U1_cubed'],0)
        self.assertNotEqual(anomaly_coefficients(spec)['SU3_squared_U1'],0)
    def test_exact_fractions(self):self.assertIsInstance(anomaly_coefficients()['U1_cubed'],Fraction)
    def test_su5_alpha1(self):self.assertAlmostEqual(alpha_inv_at_mz()[0],(3/5)*(.76878)*127.95)
    def test_alpha2(self):self.assertAlmostEqual(alpha_inv_at_mz()[1],.23122*127.95)
    def test_alpha3(self):self.assertAlmostEqual(alpha_inv_at_mz()[2],1/.118)
    def test_rge_at_mz(self):self.assertEqual(rge_inv(MZ_GEV),alpha_inv_at_mz())
    def test_rge_alpha1_decreases(self):self.assertLess(rge_inv(1e8)[0],rge_inv(MZ_GEV)[0])
    def test_rge_alpha2_increases(self):self.assertGreater(rge_inv(1e8)[1],rge_inv(MZ_GEV)[1])
    def test_rge_alpha3_increases(self):self.assertGreater(rge_inv(1e8)[2],rge_inv(MZ_GEV)[2])
    def test_gauge_not_triple_unified(self):self.assertGreater(best_meeting()['max_gap'],3)
    def test_pair_crossings_distinct(self):
        p=pair_intersections();self.assertTrue(p['1-2']<p['1-3']<p['2-3'])
    def test_pair_first_cross_1e13(self):self.assertAlmostEqual(math.log10(pair_intersections()['1-2']),13.013,delta=.01)
    def test_first_cross_condition(self):
        mu=pair_intersections()['1-2'];a=rge_inv(mu);self.assertAlmostEqual(a[0],a[1],places=12)
    def test_second_cross_condition(self):
        mu=pair_intersections()['1-3'];a=rge_inv(mu);self.assertAlmostEqual(a[0],a[2],places=12)
    def test_third_cross_condition(self):
        mu=pair_intersections()['2-3'];a=rge_inv(mu);self.assertAlmostEqual(a[1],a[2],places=12)
    def test_optimum_spread(self):
        m=best_meeting();r=m['rms_spread'];self.assertLess(r,math.sqrt(sum((v-sum(rge_inv(1e12))/3)**2 for v in rge_inv(1e12))/3))
    def test_input_invalid(self):
        with self.assertRaises(ValueError):alpha_inv_at_mz(sin2=1.2)
    def test_kk_shift(self):
        a=.12;d=.41;self.assertAlmostEqual(kk_one_form_component(a,d)+d,a)
    def test_kk_zero_shift(self):self.assertEqual(kk_one_form_component(2,0),2)

class ExperimentalPredictions(unittest.TestCase):
    def test_newton_limit(self):self.assertEqual(yukawa_acc_factor(2,0,4),1.)
    def test_yukawa_positive(self):self.assertGreater(yukawa_acc_factor(1,.1,3),1)
    def test_yukawa_negative(self):self.assertLess(yukawa_acc_factor(1,-.1,3),1)
    def test_yukawa_farfield(self):self.assertAlmostEqual(yukawa_acc_factor(1000,3,1),1)
    def test_weakfield_eotvos_zero(self):self.assertEqual(eotvos_eta(1,0,1,1,.1,.5),0)
    def test_universal_eotvos_zero(self):self.assertEqual(eotvos_eta(1,.5,1,1,.2,.2),0)
    def test_composition_dependence(self):self.assertNotEqual(eotvos_eta(1,.1,1,1,.2,.5),0)
    def test_antisymmetric_eta(self):
        a=eotvos_eta(1,.1,2,1,.2,.6);b=eotvos_eta(1,.1,2,1,.6,.2);self.assertAlmostEqual(a,-b)
    def test_source_charge_zero(self):self.assertEqual(eotvos_eta(1,.1,2,0,.2,.6),0)
    def test_envelope(self):self.assertTrue(5e-15<microscope_approx_envelope()<9e-15)
    def test_gamma_bd_zero_omega(self):self.assertAlmostEqual(brans_dicke_gamma(0),.5)
    def test_gamma_bd_large_omega(self):self.assertAlmostEqual(brans_dicke_gamma(1e6),1.,delta=1.1e-6)
    def test_lambda_invalid(self):
        with self.assertRaises(ValueError):yukawa_acc_factor(1,1,0)
    def test_eta_invalid(self):
        with self.assertRaises(ValueError):eotvos_eta(1,1,0,1,1,2)
    def test_ledger_not_claim_proof(self):self.assertTrue(any('measured G' in s for s in model_ledger()['NOT_DERIVED']))

if __name__=='__main__':unittest.main()
