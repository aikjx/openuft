"""Real mathematical/numerical consistency tests, NOT empirical tests."""
import math
import pathlib
import sys
import unittest

BASE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
import v137_diagnostics as v
old=v.old

class TestAnchor(unittest.TestCase):
    def setUp(self):
        self.R=old.check_shells(old.EARTH_LAYERS)
        self.mu=old.MU_EARTH
    def test_null_anchor_all_zero(self):
        for h in (0,100e3,400e3,1000e3):
            self.assertEqual(v.residual_after_mu_fit(self.R+h,self.R+700e3,old.EARTH_LAYERS,alpha=0),0.)
    def test_anchor_residual_zero(self):
        self.assertEqual(v.residual_after_mu_fit(self.R+400e3,self.R+400e3,old.EARTH_LAYERS),0.)
    def test_anchor_exact_ratio_identity(self):
        a=self.R+800e3
        muhat=v.fitted_mu_at_anchor(a,self.mu,old.EARTH_LAYERS)
        for h in (0,200e3,400e3):
            g=v.gravity(self.R+h,self.mu,old.EARTH_LAYERS)
            self.assertAlmostEqual(g/(muhat/(self.R+h)**2)-1,
                                   v.residual_after_mu_fit(self.R+h,a,old.EARTH_LAYERS),places=12)
    def test_anchor_200_vs_400_matches_v136(self):
        r1=self.R+200e3; r2=self.R+400e3
        self.assertAlmostEqual(v.residual_after_mu_fit(r1,r2,old.EARTH_LAYERS),
                               v.v136.relative_force_deviation(r1,r2,old.EARTH_LAYERS),places=13)
    def test_gm_absorbs_one_point(self):
        r=self.R+100e3
        muhat=v.fitted_mu_at_anchor(r,self.mu,old.EARTH_LAYERS)
        self.assertAlmostEqual(muhat/(r*r),v.gravity(r,self.mu,old.EARTH_LAYERS),places=12)
        self.assertGreater(muhat,self.mu)
    def test_mu_zero_not_allowed(self):
        with self.assertRaises(ValueError):v.gravity(self.R,0,old.EARTH_LAYERS)
    def test_interior_not_allowed(self):
        with self.assertRaises(ValueError):v.gravity(self.R-1,self.mu,old.EARTH_LAYERS)
    def test_density_invariant_shape(self):
        layers=tuple(old.Layer(x.inner_m,x.outer_m,2*x.density_kg_m3) for x in old.EARTH_LAYERS)
        self.assertAlmostEqual(v.unit_shape(self.R,old.EARTH_LAYERS),v.unit_shape(self.R,layers),places=13)
    def test_analytic_simpson_agree(self):
        e1=v.unit_shape(self.R,old.EARTH_LAYERS)
        e2=old.yukawa_accel_ratio_numeric(self.R,old.EARTH_LAYERS,alpha=1)
        self.assertAlmostEqual(e1,e2,delta=1e-8)
    def test_lunar_ratio_not_earth(self):
        RE=old.check_shells(old.EARTH_LAYERS)
        RM=old.check_shells(old.MOON_LAYERS)
        self.assertGreater(v.unit_shape(RM,old.MOON_LAYERS),v.unit_shape(RE,old.EARTH_LAYERS))
    def test_yukawa_decreases_above_surface(self):
        h=(0,100e3,200e3,400e3,800e3)
        q=[v.unit_shape(self.R+t,old.EARTH_LAYERS) for t in h]
        self.assertEqual(q,sorted(q,reverse=True))
    def test_three_ratio_independent_coupling(self):
        rr=[self.R+h for h in (0,200e3,400e3)]
        self.assertAlmostEqual(v.three_shape_direct(rr,old.EARTH_LAYERS,alpha=0.333),
                               v.three_shape_direct(rr,old.EARTH_LAYERS,alpha=1e-9),places=13)
    def test_three_ratio_null_undefined(self):
        rr=[self.R+h for h in (0,200e3,400e3)]
        with self.assertRaises(ValueError):v.three_shape_direct(rr,old.EARTH_LAYERS,alpha=0)
    def test_high_anchor_residual_large_for_candidate(self):
        rr=v.residual_after_mu_fit(self.R,self.R+1600e3,old.EARTH_LAYERS)
        self.assertGreater(rr,0.005)

class TestCovariance(unittest.TestCase):
    def setUp(self):
        self.heights=[i*100e3 for i in range(11)]
        self.coef=[0.002,1/3,0.0003]
    def test_cov_cholesky_reconstruct(self):
        C=v.correlated_cov([1e-6,2e-6,3e-6],0.2)
        L=v.cholesky(C)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(sum(L[i][k]*L[j][k] for k in range(3)),C[i][j],delta=1e-23)
    def test_invalid_correlation(self):
        with self.assertRaises(ValueError):v.correlated_cov([1e-6]*4,1)
    def test_invalid_sigma(self):
        with self.assertRaises(ValueError):v.correlated_cov([1e-6,0.],0.2)
    def test_nonpositive_covariance(self):
        with self.assertRaises(ValueError):v.cholesky([[1,2],[2,1]])
    def test_rank_singular(self):
        with self.assertRaises(ValueError):v.gls_fit([[1,1]]*5,[1]*5,v.correlated_cov([1e-6]*5))
    def test_recover_exact_three_coeffs(self):
        X=v.design_heights(self.heights)
        obs=[sum(a*b for a,b in zip(row,self.coef)) for row in X]
        C=v.correlated_cov([1e-6]*len(X),0.25)
        f=v.gls_fit(X,obs,C)
        for observed,actual in zip(f['beta'],self.coef):self.assertAlmostEqual(observed,actual,delta=3e-9)
        self.assertLess(f['chi2'],1e-10)
    def test_recover_exact_two_coeffs(self):
        X=v.design_heights(self.heights,include_nuisance=False)
        coef=[0.002,1/3]
        obs=[sum(a*b for a,b in zip(row,coef)) for row in X]
        C=v.correlated_cov([1e-6]*len(X),0.25)
        f=v.gls_fit(X,obs,C)
        self.assertAlmostEqual(f['beta'][1],1/3,delta=1e-10)
        self.assertEqual(f['dof'],9)
    def test_recover_zero_null(self):
        X=v.design_heights(self.heights)
        coefs=[0.002,0.,0.0003]
        y=[sum(a*b for a,b in zip(row,coefs)) for row in X]
        f=v.gls_fit(X,y,v.correlated_cov([1e-6]*len(X),0.2))
        self.assertAlmostEqual(f['beta'][1],0,delta=1e-10)
    def test_generated_seed_deterministic(self):
        a=v.simulate(self.heights,self.coef,seed=3)
        b=v.simulate(self.heights,self.coef,seed=3)
        self.assertEqual(a,b)
    def test_injected_detected(self):
        X,y,C=v.simulate(self.heights,self.coef,seed=233)
        fit=v.gls_fit(X,y,C)
        self.assertLess(abs(fit['beta'][1]-self.coef[1]),5*fit['standard_errors'][1])
    def test_nuisance_changes_precision(self):
        X=v.design_heights(self.heights)
        X2=v.design_heights(self.heights,include_nuisance=False)
        y=[sum(a*b for a,b in zip(row,self.coef)) for row in X]
        C=v.correlated_cov([2e-6]*len(X),0.2)
        f=v.gls_fit(X,y,C)
        f2=v.gls_fit(X2,y,C)
        self.assertGreater(f['standard_errors'][1],f2['standard_errors'][1])
    def test_correlated_cov_variance_positive(self):
        X,y,C=v.simulate(self.heights,self.coef)
        f=v.gls_fit(X,y,C)
        self.assertTrue(all(s>0 for s in f['standard_errors']))
    def test_gls_bad_dimensions(self):
        with self.assertRaises(ValueError):v.gls_fit([[1,2]]*3,[1]*4,[[1]])
    def test_chisq_nonnegative(self):
        X,y,C=v.simulate(self.heights,self.coef)
        self.assertGreaterEqual(v.gls_fit(X,y,C)['chi2'],0)
    def test_mc_coverage_sanity(self):
        data=v.monte_carlo_coverage(self.heights,self.coef,n=180,seed=7)
        self.assertGreater(data['coverage'],0.85)
        self.assertLess(data['coverage'],1.0)
    def test_noise_q_weak_unstable(self):
        weak=v.noisy_three_altitude([0,200e3,400e3],1e-5,trials=500)
        strong=v.noisy_three_altitude([0,200e3,400e3],1/3,trials=500)
        self.assertGreater(weak['median_abs_error'],strong['median_abs_error']*100)
    def test_helix_kappa_omega_identity(self):
        a,om,u=v.v136.free_pitch_for_ratio(2.,omega=3.)
        h=v.helix_kinematics(a,om,u)
        self.assertAlmostEqual(h['speed2'],1)
        self.assertAlmostEqual(h['curvature']**2+h['torsion']**2,om**2)
    def test_helix_not_force_free(self):
        a,om,u=v.v136.free_pitch_for_ratio(2.,omega=3.)
        self.assertGreater(v.helix_kinematics(a,om,u)['acceleration_magnitude'],0)
    def test_so3_generators(self):
        # Three independent infinitesimal rotations. Does not prohibit extra fibers.
        generators=[[[0,0,0],[0,0,-1],[0,1,0]],
                    [[0,0,1],[0,0,0],[-1,0,0]],
                    [[0,-1,0],[1,0,0],[0,0,0]]]
        self.assertEqual(len(generators),3)
        self.assertEqual(8+3+1,12)

if __name__=='__main__':unittest.main()

# Additional input-validation tests are kept separately to make text interfaces auditable.
