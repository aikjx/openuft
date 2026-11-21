"""No external dependencies: python -m unittest discover -s tests -v"""
import sys, math, random, unittest
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'theory'))
from root_v130 import *

class RepresentationTests(unittest.TestCase):
    def test_trace_zero(self): self.assertTrue(traceless(Y_FIVE))
    def test_five_weights(self): self.assertEqual(len(Y_FIVE),5)
    def test_ten_weights(self): self.assertEqual(len(wedge2_weights(Y_FIVE)),10)
    def test_fivebar_weights(self): self.assertEqual(len(anti_weights(Y_FIVE)),5)
    def test_su5_quark_doublet(self): self.assertEqual(wedge2_weights(Y_FIVE).count(F(1,6)),6)
    def test_su5_uconj(self): self.assertEqual(wedge2_weights(Y_FIVE).count(F(-2,3)),3)
    def test_su5_econj(self): self.assertEqual(wedge2_weights(Y_FIVE).count(F(1)),1)
    def test_su5_dconj(self): self.assertEqual(anti_weights(Y_FIVE).count(F(1,3)),3)
    def test_su5_leptons(self): self.assertEqual(anti_weights(Y_FIVE).count(F(-1,2)),2)
    def test_generation_15(self): self.assertEqual(sum(n for n,y in FAMILY.values()),15)
    def test_trace_square(self): self.assertEqual(hypercharge_normalization(),F(5,6))
    def test_generator_norm(self): self.assertEqual(F(3,5)*hypercharge_normalization(),F(1,2))
    def test_su5_example(self): self.assertEqual(cubic_anomaly_su5(tuple(map(F,[1,1,1,1,-4]))),0)
    def test_traces_in_example(self):
        x=tuple(map(F,[1,1,1,1,-4])); self.assertEqual(su5_cubic_trace_identity(x),(F(-60),F(-60)))
    def test_random_cubic_identity_100(self):
        rng=random.Random(421)
        for _ in range(100):
            x=[F(rng.randint(-20,20)) for _ in range(4)]; x.append(-sum(x))
            self.assertEqual(su5_cubic_trace_identity(x)[0],su5_cubic_trace_identity(x)[1])
            self.assertEqual(cubic_anomaly_su5(x),0)
    def test_trace_condition_required(self):
        with self.assertRaises(ValueError): cubic_anomaly_su5([F(1)]*5)
    def test_dimension_condition_required(self):
        with self.assertRaises(ValueError): cubic_anomaly_su5([F(1),F(-1)])
    def test_second_traceless_generator_cancel(self):
        x=[F(1),F(2),F(-3),F(0),F(0)]
        self.assertEqual(cubic_anomaly_su5(x),0)

class FamilyAnomalies(unittest.TestCase):
    def test_su3_anomaly(self): self.assertEqual(family_anomalies()['SU3_SU3_U1'],0)
    def test_su2_anomaly(self): self.assertEqual(family_anomalies()['SU2_SU2_U1'],0)
    def test_gravity_anomaly(self): self.assertEqual(family_anomalies()['GRAV_GRAV_U1'],0)
    def test_abelian_anomaly(self): self.assertEqual(family_anomalies()['U1_CUBED'],0)
    def test_witten_even(self): self.assertEqual(family_anomalies()['SU2_WITTEN_PARITY'],0)
    def test_perturbed_charge_fails(self):
        f=FAMILY.copy(); f['e^c']=(1,F(4,5));
        self.assertNotEqual(family_anomalies(f)['U1_CUBED'],0)
    def test_charge_units_from_Y(self):
        self.assertEqual(F(1,2)+F(-1,2),0) # neutrino
        self.assertEqual(F(-1,2)+F(-1,2),F(-1)) # electron
        self.assertEqual(F(1,2)+F(1,6),F(2,3)) # up
        self.assertEqual(F(-1,2)+F(1,6),F(-1,3)) # down
    def test_sterile_neutrino_anomaly_free(self):
        f=FAMILY.copy(); f['nu^c']=(1,F(0));
        self.assertEqual(family_anomalies(f)['U1_CUBED'],0)
        self.assertEqual(family_anomalies(f)['GRAV_GRAV_U1'],0)

class RunningTests(unittest.TestCase):
    def setUp(self): self.a0=inverse_couplings()
    def test_inverse_gauge_couplings(self):
        self.assertAlmostEqual(self.a0[0],59.02154694,places=8)
        self.assertAlmostEqual(self.a0[1],29.5857551,places=7)
    def test_alpha3(self): self.assertAlmostEqual(self.a0[2],1/ALPHA_S_MZ)
    def test_at_mz_equal_input(self): self.assertEqual(alpha_inv_at(MZ_GEV,self.a0,B_SM),self.a0)
    def test_sm12_scale(self): self.assertAlmostEqual(crossing_scale(0,1,self.a0,B_SM)/1e13,1.031713664757,places=8)
    def test_sm13_scale(self): self.assertAlmostEqual(crossing_scale(0,2,self.a0,B_SM)/1e14,2.43264314534,places=7)
    def test_sm23_scale(self): self.assertAlmostEqual(crossing_scale(1,2,self.a0,B_SM)/1e16,9.72517562388,places=8)
    def test_pair_matches_at_crossing(self):
        for i,j in ((0,1),(0,2),(1,2)):
            v=alpha_inv_at(crossing_scale(i,j,self.a0,B_SM),self.a0,B_SM)
            self.assertAlmostEqual(v[i],v[j],places=11)
    def test_sm_nonunification_det(self): self.assertGreater(abs(unification_determinant(self.a0,B_SM)),40)
    def test_sm_unification_residual(self):
        t=crossing_log(0,1,self.a0,B_SM)
        v=[ai-bi*t/(2*math.pi) for ai,bi in zip(self.a0,B_SM)]
        self.assertAlmostEqual(v[0]-v[2],5.583123500373,places=8)
    def test_required_alpha_s(self): self.assertAlmostEqual(alpha_s_required_for_unification(),0.0711353931475,places=10)
    def test_required_alpha_s_discrepancy(self): self.assertGreater(ALPHA_S_MZ-alpha_s_required_for_unification(),0.04)
    def test_beta_sm(self): self.assertAlmostEqual(B_SM[0]-B_SM[1],109/15)
    def test_mssm_toy_crossings_near(self):
        xs=[crossing_scale(i,j,self.a0,B_MSSM) for i,j in ((0,1),(0,2),(1,2))]
        self.assertTrue(all(1.9e16<x<2.4e16 for x in xs))
    def test_mssm_not_exact(self): self.assertGreater(abs(unification_determinant(self.a0,B_MSSM)),0.1)
    def test_mssm_sm_comparison(self):
        self.assertLess(abs(unification_determinant(self.a0,B_MSSM)),abs(unification_determinant(self.a0,B_SM)))
    def test_beta_target_difference(self):
        d12,d23=beta_differences_required(1e16,self.a0)
        self.assertAlmostEqual(d12,5.72098499402,places=6)
        self.assertAlmostEqual(d23,4.10305718773,places=6)
    def test_bestfit_sm_positive_residual(self): self.assertGreater(best_fit_spread(self.a0,B_SM)['rms_inv_alpha'],1)
    def test_bestfit_mssm_smaller(self):
        self.assertLess(best_fit_spread(self.a0,B_MSSM)['rms_inv_alpha'],best_fit_spread(self.a0,B_SM)['rms_inv_alpha'])
    def test_scale_reparametrization_invariance(self):
        newscale=1000.0
        at=alpha_inv_at(newscale,self.a0,B_SM)
        for i,j in ((0,1),(0,2),(1,2)):
            mu1=crossing_scale(i,j,self.a0,B_SM)
            mu2=crossing_scale(i,j,at,B_SM,newscale)
            self.assertAlmostEqual(mu1/mu2,1,places=12)
    def test_det_scale_invariance(self):
        self.assertAlmostEqual(unification_determinant(self.a0,B_SM),unification_determinant(alpha_inv_at(1000,self.a0,B_SM),B_SM),places=10)
    def test_exact_toy_unification(self):
        # Synthetic data generated from a single GUT coupling and RG flow.
        alphaG=42.0; t=30.0
        ai=tuple(alphaG+bi*t/(2*math.pi) for bi in B_SM)
        self.assertAlmostEqual(unification_determinant(ai,B_SM),0,places=11)
        self.assertAlmostEqual(crossing_log(0,1,ai,B_SM),t,places=10)
    def test_wrong_spectrum_beta_detected(self):
        self.assertNotAlmostEqual(unification_determinant(self.a0,B_SM),unification_determinant(self.a0,B_MSSM))
    def test_sensitivity_range_no_exact(self):
        for asvalue in [0.115,0.116,0.117,0.118,0.119,0.120,0.121]:
            self.assertGreater(abs(unification_determinant(inverse_couplings(alpha_s=asvalue),B_SM)),25)
    def test_invalid_inputs(self):
        for x in [-1,0,1,1.1]:
            with self.assertRaises(ValueError): inverse_couplings(sin2=x)
    def test_invalid_scale(self):
        with self.assertRaises(ValueError): alpha_inv_at(0,self.a0,B_SM)
    def test_parallel_betas(self):
        with self.assertRaises(ValueError): crossing_log(0,1,[1,2,3],[1,1,2])
    def test_beta_same_reference(self):
        with self.assertRaises(ValueError): beta_differences_required(MZ_GEV,self.a0)
    def test_best_fit_zero_for_exact(self):
        t=33; a=tuple(45+b*t/(2*math.pi) for b in B_SM)
        self.assertLess(best_fit_spread(a,B_SM)['rms_inv_alpha'],1e-13)

if __name__=='__main__':unittest.main()
