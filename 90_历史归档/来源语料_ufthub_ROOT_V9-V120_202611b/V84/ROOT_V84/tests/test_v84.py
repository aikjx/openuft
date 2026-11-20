import math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.physics import *
from src.analysis import *
from src.simulate import *

class PhysicsTests(unittest.TestCase):
    def setUp(self):self.r=Rig()
    def test_G_units_reference(self):self.assertAlmostEqual(G_REF,6.67430e-11)
    def test_speed_exact(self):self.assertEqual(C_LIGHT,299792458.)
    def test_valid_rig(self):self.r.validate(.38)
    def test_bad_distance(self):
        with self.assertRaises(ValueError):self.r.validate(.22)
    def test_bad_mass(self):
        with self.assertRaises(ValueError):Rig(-1,.1,.12).validate(.4)
    def test_source_outside_matches_point(self):
        self.assertAlmostEqual(sphere_newton_acceleration(0,.4,20,.1),G_REF*20/.16)
    def test_uniform_inside_linear(self):
        self.assertAlmostEqual(sphere_newton_acceleration(0,.05,20,.1),G_REF*20*.05/.1**3)
    def test_sphere_center_zero(self):self.assertEqual(sphere_newton_acceleration(0,0,20,.1),0.)
    def test_shell_surface_continuity(self):
        at=sphere_newton_acceleration(0,.1,20,.1)
        expected=G_REF*20/.01
        self.assertAlmostEqual(at,expected)
    def test_mirror_common_odd(self):
        p=gravity_readings(self.r,.5,1);m=gravity_readings(self.r,.5,-1)
        self.assertAlmostEqual(p['common'],-m['common'],delta=1e-20)
    def test_mirror_gradient_even(self):
        p=gravity_readings(self.r,.5,1);m=gravity_readings(self.r,.5,-1)
        self.assertAlmostEqual(p['gradient'],m['gradient'],delta=1e-19)
    def test_formula_common(self):self.assertAlmostEqual(gravity_readings(self.r,.5,1)['common'],common_amplitude(self.r,.5))
    def test_formula_gradient(self):self.assertAlmostEqual(gravity_readings(self.r,.5,1)['gradient'],even_gradient(self.r,.5))
    def test_mass_proportional(self):
        x=common_amplitude(self.r,.5)
        self.assertAlmostEqual(common_amplitude(Rig(200,.1,.12),.5),2*x)
    def test_distance_monotonic(self):
        arr=[common_amplitude(self.r,d) for d in DISTANCES]
        self.assertTrue(all(a>b for a,b in zip(arr,arr[1:])))
    def test_derivative_distance(self):
        d=.5;h=1e-5
        fd=(common_amplitude(self.r,d+h)-common_amplitude(self.r,d-h))/(2*h)
        self.assertAlmostEqual(fd/partials_common(self.r,d)['distance_m'],1,delta=3e-9)
    def test_derivative_half_baseline(self):
        d=.5;h=1e-5
        f=lambda s:common_amplitude(Rig(100.,s,.12),d)
        fd=(f(.1+h)-f(.1-h))/(2*h)
        self.assertAlmostEqual(fd/partials_common(self.r,d)['half_baseline_m'],1,delta=4e-9)
    def test_derivative_mass(self):
        self.assertAlmostEqual(partials_common(self.r,.5)['mass_kg'],common_amplitude(self.r,.5)/100)
    def test_gravity_benchmark(self):
        self.assertAlmostEqual(common_amplitude(self.r,.5),3.012704861111111e-8,delta=1e-20)
    def test_uncertainty_positive(self):
        v=source_geometry_uncertainty(self.r,.5)
        self.assertGreater(v['rss_m_s2'],0)
        self.assertLess(v['relative_rss'],1)
    def test_baseline_sigma_half_factor(self):
        v=source_geometry_uncertainty(self.r,.5,0.,0.,.001,0.)
        self.assertAlmostEqual(abs(v['terms_m_s2']['baseline']),abs(partials_common(self.r,.5)['half_baseline_m']*.0005))
    def test_tilt_dominance_as_config(self):
        v=source_geometry_uncertainty(self.r,.5)
        self.assertGreater(abs(v['terms_m_s2']['tilt']),abs(v['terms_m_s2']['reference_G']))
    def test_no_point_inside(self):
        with self.assertRaises(ValueError):common_amplitude(self.r,.20)
    def test_yukawa_ff_zero(self):self.assertEqual(yukawa_form_factor(0.),1.)
    def test_yukawa_ff_small_series(self):
        self.assertAlmostEqual(yukawa_form_factor(1e-4),1+1e-9,delta=1e-14)
    def test_yukawa_ff_direct(self):
        x=.5
        self.assertAlmostEqual(yukawa_form_factor(x),3*(x*math.cosh(x)-math.sinh(x))/x**3)
    def test_yukawa_stable_vs_naive(self):
        a=.12;lam=.25;r=.5
        self.assertAlmostEqual(yukawa_kernel_product(a,r,lam),yukawa_form_factor(a/lam)*math.exp(-r/lam),delta=2e-15)
    def test_large_x_stable(self):
        v=yukawa_kernel_product(.12,.1201,.0001)
        self.assertTrue(math.isfinite(v))
        self.assertGreater(v,0.)
    def test_yukawa_long_range(self):
        n=common_amplitude(self.r,.5)
        y=yukawa_amplitude_per_alpha(self.r,.5,1e7)
        self.assertAlmostEqual(y/n,1.,delta=1e-11)
    def test_yukawa_short_range(self):
        self.assertLess(yukawa_amplitude_per_alpha(self.r,.5,.02),common_amplitude(self.r,.5)*.0001)
    def test_yukawa_finite_sphere_enhancement(self):
        self.assertGreater(yukawa_form_factor(.5),1.)
    def test_yukawa_increases_with_mass(self):
        self.assertAlmostEqual(yukawa_amplitude_per_alpha(Rig(200,.1,.12),.5,.25)/yukawa_amplitude_per_alpha(self.r,.5,.25),2.)
    def test_yukawa_bad_lambda(self):
        with self.assertRaises(ValueError):yukawa_amplitude_per_alpha(self.r,.5,0.)
    def test_em_energy_quadratic(self):
        self.assertAlmostEqual(em_stored_energy(2,.001),4*em_stored_energy(1,.001))
    def test_em_sign_even(self):self.assertEqual(em_stored_energy(1.2,.01),em_stored_energy(-1.2,.01))
    def test_em_closed_system_no_net_energy(self):
        E=em_stored_energy(.1,.001)
        self.assertAlmostEqual((E-E)/C_LIGHT**2,0.)
    def test_energy_mass(self):self.assertAlmostEqual(net_added_mass_kg(C_LIGHT**2),1.)

class AnalysisTests(unittest.TestCase):
    def setUp(self):self.r=Rig()
    def test_abba_constant_cancel(self):
        a=[{'p':p,'common_m_s2':7.} for p in (1,-1,-1,1)]
        self.assertEqual(abba_amplitude(a),0.)
    def test_abba_linear_drift_cancel(self):
        a=[{'p':p,'common_m_s2':6.+10.*i+p*2.} for i,p in enumerate((1,-1,-1,1))]
        self.assertAlmostEqual(abba_amplitude(a),2.)
    def test_baab_linear_drift_cancel(self):
        a=[{'p':p,'common_m_s2':6.+10.*i+p*2.} for i,p in enumerate((-1,1,1,-1))]
        self.assertAlmostEqual(abba_amplitude(a),2.)
    def test_abba_reject_invalid(self):
        with self.assertRaises(ValueError):abba_amplitude([{'p':1,'common_m_s2':0.}]*4)
    def test_quadratic_drift_not_canceled(self):
        a=[{'p':p,'common_m_s2':i*i} for i,p in enumerate((1,-1,-1,1))]
        self.assertNotEqual(abba_amplitude(a),0.)
    def test_abba_sem(self):
        a=[]
        for v in (1.,2.,3.,4.):a +=[{'p':p,'common_m_s2':p*v} for p in (1,-1,-1,1)]
        self.assertAlmostEqual(estimate_records(a)['mean'],2.5)
    def test_corrected_real_sham(self):
        mk=lambda v:[{'p':p,'common_m_s2':p*v} for _ in range(6) for p in (1,-1,-1,1)]
        self.assertAlmostEqual(corrected(mk(4.),mk(1.))['signal'],3.)
    def test_2fit_exact(self):
        rows=[{'distance_m':d,'signal':1.17*common_amplitude(self.r,d)+3e-11,'sem':1e-10} for d in DISTANCES]
        r=estimate_two_parameter(self.r,rows)
        self.assertAlmostEqual(r['beta_G_ratio'],1.17,delta=1e-11)
        self.assertAlmostEqual(r['offset_m_s2'],3e-11,delta=1e-19)
    def test_3fit_exact(self):
        rows=[]
        for d in DISTANCES:
            v=1.03*common_amplitude(self.r,d)+.05*yukawa_amplitude_per_alpha(self.r,d,.25)-2e-11
            rows.append({'distance_m':d,'signal':v,'sem':1e-10})
        v=fit_three_parameter(self.r,rows,.25)
        self.assertAlmostEqual(v['beta_G_ratio'],1.03,delta=1e-9)
        self.assertAlmostEqual(v['alpha_yukawa'],.05,delta=1e-9)
        self.assertAlmostEqual(v['offset_m_s2'],-2e-11,delta=1e-19)
    def test_3fit_small_dataset(self):
        with self.assertRaises(ValueError):fit_three_parameter(self.r,[{'distance_m':.5,'signal':0.,'sem':1e-10}],.25)
    def test_rank_loss_repeated_distance(self):
        rows=[{'distance_m':.5,'signal':4e-8,'sem':1e-10} for _ in range(6)]
        with self.assertRaises(ValueError):fit_three_parameter(self.r,rows,.25)
    def test_correlated_newton_yukawa_long_range(self):
        for d in DISTANCES:
            self.assertAlmostEqual(yukawa_amplitude_per_alpha(self.r,d,1e8)/common_amplitude(self.r,d),1.,delta=1e-12)
    def test_nuisance_exact_confounded(self):
        # A real-only artifact shaped exactly as Yukawa cannot be distinguished in this dataset.
        rows=[{'distance_m':d,'signal':common_amplitude(self.r,d)+.08*yukawa_amplitude_per_alpha(self.r,d,.25),'sem':1e-10} for d in DISTANCES]
        out=fit_three_parameter(self.r,rows,.25)
        self.assertAlmostEqual(out['alpha_yukawa'],.08,delta=1e-9)
    def test_synthetic_reproducible(self):
        r1=synthetic_trial(self.r,distances=[.5],blocks=3,seed=90)
        r2=synthetic_trial(self.r,distances=[.5],blocks=3,seed=90)
        self.assertEqual(r1,r2)
    def test_synthetic_not_observed(self):
        rows=synthetic_trial(self.r,distances=[.5],blocks=3)
        self.assertTrue(all(x['provenance']=='SYNTHETIC_NOT_REAL_DATA' for x in rows))
    def test_synthetic_data_arms_count(self):
        self.assertEqual(len(synthetic_trial(self.r,distances=[.4,.5],blocks=4)),2*4*4*2)
    def test_synthetic_abba_each_block(self):
        rows=synthetic_trial(self.r,distances=[.5],blocks=3)
        for k in range(0,len(rows),4): self.assertAlmostEqual(sum(x['p'] for x in rows[k:k+4]),0.)
    def test_synthetic_fit_null_not_large(self):
        v=synthetic_trial(self.r,blocks=112,seed=84001)
        a=summarize_trials(self.r,v)['fits']['newton_yukawa_offset']
        self.assertLess(abs(a['alpha_yukawa']/a['alpha_se']),3.)
    def test_synthetic_fit_injected(self):
        v=synthetic_trial(self.r,blocks=112,seed=84002,alpha_injected=.08)
        a=summarize_trials(self.r,v)['fits']['newton_yukawa_offset']
        self.assertGreater(a['alpha_yukawa']/a['alpha_se'],5.)
        self.assertLess(abs(a['alpha_yukawa']-.08),3*a['alpha_se'])
    def test_synthetic_confounded_false_positive(self):
        v=synthetic_trial(self.r,blocks=112,seed=84003,identical_nuisance=True)
        a=summarize_trials(self.r,v)['fits']['newton_yukawa_offset']
        self.assertGreater(a['alpha_yukawa']/a['alpha_se'],5.)
    def test_tilt_floor(self):
        budget=source_geometry_uncertainty(self.r,.5,0.,0.,0.,1e-10)
        self.assertAlmostEqual(budget['terms_m_s2']['tilt'],G_EARTH_REF*1e-10)

if __name__=='__main__':unittest.main()
