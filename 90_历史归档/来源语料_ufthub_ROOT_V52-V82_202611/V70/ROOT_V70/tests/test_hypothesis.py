import unittest, math, numpy as np
from rootv70.physics import (BODIES, MATERIAL_TOY, toy_acceleration,
    yukawa_shape,eotvos,field_at)
from rootv70.inference import feature_row,fixed_earth_design,multi_body_design,rank_report,synthetic_fit

class HypothesisAndIdentifiability(unittest.TestCase):
    def setUp(self): self.e=BODIES['Earth']
    def test_new_force_zero_coupling(self):
        for mat in MATERIAL_TOY:
            self.assertAlmostEqual(toy_acceleration(self.e,mat,strength=0),self.e.g,places=12)
    def test_yukawa_analytic_derivative(self):
        r=2e6; lam=8e6; eps=.1
        f=lambda t: math.exp(-t/lam)/t
        numeric=-(f(r+eps)-f(r-eps))/(2*eps)
        analytic=math.exp(-r/lam)*(1+r/lam)/r**2
        self.assertAlmostEqual(numeric,analytic,delta=analytic*1e-8)
    def test_yukawa_point_source_long_range(self):
        self.assertAlmostEqual(yukawa_shape(1e5,1e20),1,places=12)
    def test_yukawa_zero_for_very_short_range(self):
        self.assertLess(yukawa_shape(1e5,1),1e-90)
    def test_yukawa_invalid_lengths(self):
        with self.assertRaises(ValueError):yukawa_shape(0,1)
    def test_yukawa_monotonic(self):
        self.assertGreater(yukawa_shape(1e3,1e5),yukawa_shape(2e3,1e5))
    def test_composition_difference_sign(self):
        ta=toy_acceleration(self.e,'Ti',strength=.01)
        pa=toy_acceleration(self.e,'Pt',strength=.01)
        self.assertLess(ta,pa)
    def test_composition_difference_reverses_if_sign_changed(self):
        a=toy_acceleration(self.e,'Ti',strength=-.01)
        b=toy_acceleration(self.e,'Pt',strength=-.01)
        self.assertGreater(a,b)
    def test_eotvos_identical_zero(self):
        self.assertEqual(eotvos(9.8,9.8),0)
    def test_eotvos_opposite_pair_sign(self):
        self.assertAlmostEqual(eotvos(9.81,9.80),-eotvos(9.80,9.81))
    def test_composition_signal_zero_if_same_material(self):
        self.assertAlmostEqual(eotvos(toy_acceleration(self.e,'Fe',strength=1e-12),
            toy_acceleration(self.e,'Fe',strength=1e-12)),0,places=15)
    def test_toy_fifth_force_allows_no_false_empirical_constraint(self):
        # Synthetic coefficient is user-set; not inferred from MICROSCOPE or observations.
        self.assertEqual(toy_acceleration(self.e,'Ti',strength=0),self.e.g)
    def test_feature_fixed_shape(self):
        self.assertEqual(feature_row('Earth','Ti','Pt',0,0).shape,(3,))
    def test_fixed_environment_only_rank_one(self):
        self.assertEqual(rank_report(fixed_earth_design())['rank'],1)
    def test_fixed_environment_even_many_materials_do_not_fix_three_params(self):
        x=fixed_earth_design()
        self.assertTrue(np.allclose(x[0]*x[1,0],x[1]*x[0,0]))
    def test_multi_environment_rank_three(self):
        self.assertEqual(rank_report(multi_body_design()[0])['rank'],3)
    def test_multi_environment_condition_finite(self):
        report=rank_report(multi_body_design()[0]);self.assertLess(report['condition'],100)
    def test_multiple_body_design_row_count(self):
        x,labels=multi_body_design();self.assertEqual(len(labels),len(BODIES)*3*2*3)
        self.assertEqual(len(x),len(labels))
    def test_synthetic_fit_is_reproducible(self):
        a=synthetic_fit(); b=synthetic_fit();self.assertEqual(a['estimate'],b['estimate'])
    def test_synthetic_fit_noise_free_recovers_parameters(self):
        fit=synthetic_fit(sigma=0)
        np.testing.assert_allclose(fit['estimate'],fit['truth'],rtol=1e-12,atol=1e-29)
    def test_synthetic_fit_errors_nonnegative(self):
        self.assertTrue(all(x>=0 for x in synthetic_fit()['standard_error']))
    def test_synthetic_fit_sensitivity_noise_scale(self):
        a=synthetic_fit(sigma=1e-16);b=synthetic_fit(sigma=2e-16)
        np.testing.assert_allclose(np.array(a['standard_error'])*2,b['standard_error'])
    def test_synthetic_fit_not_a_physics_discovery(self):
        self.assertEqual(synthetic_fit()['measurements_synthetic'],162)
    def test_earth_vs_moon_curvature_not_same(self):
        e=field_at(self.e,0)['kretschmann']
        m=field_at(BODIES['Moon'],0)['kretschmann']
        self.assertNotAlmostEqual(e,m,delta=abs(e)*.01)
    def test_nonzero_toy_rotation_column(self):
        x=feature_row('Earth','Ti','Pt',0,0)
        self.assertNotEqual(x[-1],0)
    def test_polar_rotation_column_approximately_zero(self):
        x=feature_row('Earth','Ti','Pt',90,0)
        self.assertLess(abs(x[-1]),1e-30)

if __name__=='__main__':unittest.main()
