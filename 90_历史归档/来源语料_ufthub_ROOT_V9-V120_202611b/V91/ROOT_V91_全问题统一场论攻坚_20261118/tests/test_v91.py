import json,math,unittest
from pathlib import Path
import numpy as np
from src.root_v91 import (
    Geometry,newton_kernel,yukawa_kernel,yukawa_kernel_naive,yukawa_delta_integral,
    derivative_mu,rigorous_delta_bounds,phase_benchmark,C,HBAR,H,G,E,KE,
    candidate_scalar_alpha,scalar_force_relative,stable_shape_separation,
    sign_flip_design,condition_after_external_even_calibration,
    nuisance_marginalized_fisher,legacy_audit,stable_signal,polynomial_nuisance_projection)

ROOT=Path(__file__).resolve().parents[1]
class CoreTests(unittest.TestCase):
    def setUp(self): self.g=Geometry(450e-6,200e-6,200e-6)
    def test_v89_phase_regression(self):
        self.assertAlmostEqual(phase_benchmark(self.g),-0.0692394597353851,delta=1e-15)
    def test_yukawa_short_and_long_limits(self):
        self.assertAlmostEqual(yukawa_kernel(self.g,1e8),newton_kernel(self.g),delta=1e-8)
        self.assertAlmostEqual(yukawa_kernel(self.g,1e-9),0.,delta=1e-12)
    def test_sign(self):
        self.assertLess(newton_kernel(self.g),0)
        for lam in [1e-5,1e-4,1e-3,1e-2,1]:
            self.assertLess(newton_kernel(self.g),yukawa_kernel(self.g,lam))
            self.assertLess(yukawa_kernel(self.g,lam),0.)
    def test_derivative_analytic_vs_central_difference(self):
        for mu in (1.,50.,1e3,1e4):
            h=mu*5e-5
            exact=derivative_mu(self.g,mu)
            fd=(yukawa_kernel_naive(self.g,1/(mu+h))-yukawa_kernel_naive(self.g,1/(mu-h)))/(2*h)
            # direct sums of four terms lose precision for small mu, so use useful absolute+relative tolerance
            self.assertLess(abs(exact-fd),max(2e-6*exact,3e-9))
    def test_legacy_correction(self):
        x=legacy_audit()
        self.assertGreater(x['alpha_difference_ppm'],2.2)
        self.assertLess(x['alpha_difference_ppm'],2.3)
        self.assertAlmostEqual(x['mass_ratio_candidate_56pi'],56*math.pi)
        self.assertNotAlmostEqual(x['mass_ratio_candidate_56pi'],1836.152673)
        self.assertNotEqual(x['strong_frequency_large_R_power'],x['newton_orbit_frequency_large_R_power'])
        self.assertEqual(x['schwarzschild_ISCO_GM_over_c2'],6)
    def test_both_displacements_zero(self):
        for gg in [Geometry(0.001,0,1e-4),Geometry(0.001,1e-4,0),Geometry(0.001,0,0)]:
            self.assertAlmostEqual(newton_kernel(gg),0,places=11)
            self.assertEqual(yukawa_delta_integral(gg,0.001),0)
    def test_geometries_invalid(self):
        for args in [(0,0,0),(1e-4,200e-6,200e-6),(1e-4,-1e-5,0),(float('nan'),0,0)]:
            with self.assertRaises(ValueError):Geometry(*args)
    def test_invalid_lambda(self):
        with self.assertRaises(ValueError):yukawa_delta_integral(self.g,-1)
        with self.assertRaises(ValueError):yukawa_kernel_naive(self.g,0)
    def test_exact_derivative_positive(self):
        for mu in [0.01,1,10,100,1000,1e5]: self.assertGreater(derivative_mu(self.g,mu),0)
    def test_positive_alpha_for_universal_scalar(self):
        for beta in [0,1e-4,0.001,0.5,1.0]:
            self.assertEqual(candidate_scalar_alpha(beta,beta),2*beta*beta)
    def test_scalar_force_weak_yukawa(self):
        alpha=0.2;r=0.0003;lam=0.001
        expected=1+alpha*(1+r/lam)*math.exp(-r/lam)
        self.assertAlmostEqual(scalar_force_relative(alpha,r,lam),expected,places=14)
    def test_scalar_force_far(self):
        self.assertAlmostEqual(scalar_force_relative(0.2,10,1e-4),1.)
    def test_residual_signal_extreme_lambda(self):
        g=self.g
        for lam in [1,1e2,1e6]:
            sig=stable_signal(g,lam)
            goal=G*1e-28/HBAR*g.a*g.b/(3*lam**3)
            self.assertLess(abs(sig-goal)/abs(goal),0.001)
    def test_stable_separation_scales_lambda_minus_three(self):
        ds=[450e-6,600e-6,850e-6,1250e-6]
        a=stable_shape_separation(ds,200e-6,200e-6,1.)[0]
        b=stable_shape_separation(ds,200e-6,200e-6,10.)[0]
        self.assertAlmostEqual(a/b,1000,delta=5.)
    def test_sign_flip_has_rank_two_and_even_nuisance_degeneracy(self):
        x=sign_flip_design([1.,2.,3.,5.])
        self.assertEqual(np.linalg.matrix_rank(x),2)
        self.assertTrue(np.all(x[:,0]==x[:,2]))
        self.assertEqual(np.linalg.matrix_rank(condition_after_external_even_calibration([1,2,3,5])),3)
    def test_even_nuisance_zero_information(self):
        f=np.array([1.,2.,3.])
        cov=np.diag([1.,2.,3.])
        self.assertLess(nuisance_marginalized_fisher(f,f.reshape(-1,1),cov),1e-27)
    def test_GLs_whitening_robust_against_scaling(self):
        sig=np.array([1.,0.4,-0.5])
        nuisance=np.array([[1.],[1.],[1.]])
        cov=np.array([[1.,0.2,0],[0.2,2.,0.1],[0,0.1,0.5]])
        v=nuisance_marginalized_fisher(sig,nuisance,cov)
        self.assertGreater(v,0)
        self.assertAlmostEqual(v,nuisance_marginalized_fisher(sig,nuisance*1e7,cov),places=12)
    def test_non_pd_cov_fails(self):
        with self.assertRaises(np.linalg.LinAlgError):
            nuisance_marginalized_fisher(np.array([1.,2.]),np.zeros((2,0)),np.array([[1.,2.],[2.,1.]]))
    def test_unknown_polynomial_background_suppresses_higher_orders(self):
        ds=[450e-6,550e-6,650e-6,850e-6,1100e-6,1300e-6,1700e-6]
        # halving lambda should multiply residual by 2**(degree+4) for degree>=0
        for degree in [-1,0,1,2]:
            x=polynomial_nuisance_projection(ds,200e-6,200e-6,0.03,degree)[0]
            y=polynomial_nuisance_projection(ds,200e-6,200e-6,0.06,degree)[0]
            expected=2**(degree+4)
            self.assertAlmostEqual(x/y,expected,delta=expected*0.035)
    def test_polynomial_background_dimension_guard(self):
        with self.assertRaises(ValueError):
            polynomial_nuisance_projection([1.,2.],0.1,0.1,10.,1)
    def test_hbar_derived_exact_h(self):
        self.assertEqual(H,6.62607015e-34)
        self.assertEqual(HBAR,H/(2*math.pi))
    def test_issue_ledger_exact_coverage(self):
        rows=json.loads((ROOT/'ledger/ROOT_V91_115_issues.json').read_text(encoding='utf8'))
        self.assertEqual(len(rows),115)
        self.assertEqual(len({x['id'] for x in rows}),115)
        self.assertEqual(rows[0]['id'],'A01')
        self.assertEqual(rows[-1]['id'],'G115')
        self.assertTrue(all(x['acceptance_criterion'] for x in rows))
    def test_evidence_not_mislabeled(self):
        rows=json.loads((ROOT/'ledger/ROOT_V91_115_issues.json').read_text(encoding='utf8'))
        self.assertTrue(all(x['status'] not in ('PROVEN_UNIFICATION','OBSERVED_NEW_FORCE') for x in rows))
    def test_phase_non_linear_charge_reversal_failure(self):
        grav=0.4;charged=1.0
        avg=(abs(math.sin((grav+charged)/2))+abs(math.sin((grav-charged)/2)))/2
        even=abs(math.sin(grav/2))
        self.assertGreater(abs(avg-even),0.1)

class SymbolicChecks(unittest.TestCase):
    def test_moments(self):
        import sympy as s
        d,a,b=s.symbols('d a b',real=True)
        rr=[d+(a-b)/2,d+(a+b)/2,d-(a+b)/2,d+(b-a)/2]
        mom=lambda n:s.factor(sum(c*r**n for c,r in zip([1,-1,-1,1],rr)))
        self.assertEqual(mom(0),0)
        self.assertEqual(mom(1),0)
        self.assertEqual(mom(2),-2*a*b)
        self.assertEqual(mom(3),-6*a*b*d)
    def test_derivative_identity(self):
        import sympy as s
        mu,d,a,b=s.symbols('mu d a b',positive=True)
        r=[d+(a-b)/2,d+(a+b)/2,d-(a+b)/2,d+(b-a)/2]
        fy=sum(sign*s.exp(-mu*x)/x for sign,x in zip((1,-1,-1,1),r))
        exact=4*s.exp(-mu*d)*s.sinh(mu*a/2)*s.sinh(mu*b/2)
        self.assertEqual(s.simplify(s.expand((s.diff(fy,mu)-exact).rewrite(s.exp))),0)
    def test_long_range_moment_four(self):
        import sympy as s
        d,a,b=s.symbols('d a b',real=True)
        r=[d+(a-b)/2,d+(a+b)/2,d-(a+b)/2,d+(b-a)/2]
        m4=s.factor(sum(sign*x**4 for sign,x in zip((1,-1,-1,1),r)))
        self.assertEqual(m4,-a*b*(a*a+b*b+12*d*d))

# Each generated case tests a distinct numerical geometry/length regime (not copy-paste fake tests).
def _numerical_case(d,a,b,lam):
    def test(self):
        g=Geometry(d,a,b)
        delta=yukawa_delta_integral(g,lam)
        lo,hi=rigorous_delta_bounds(g,lam)
        self.assertGreater(delta,0.)
        self.assertLessEqual(lo-delta,1e-9*max(abs(delta),1e-50))
        self.assertLessEqual(delta-hi,1e-9*max(abs(delta),1e-50))
        self.assertLessEqual(delta,g.a*g.b/(3*lam**3)*(1+1e-12))
        # direct evaluation is numerically reliable for the short/intermediate cases only
        if lam<0.02:
            brute=yukawa_kernel_naive(g,lam)-newton_kernel(g)
            self.assertAlmostEqual(delta,brute,delta=max(1e-7*delta,1e-9))
    return test

for i in range(10):
    d=(450+i*75)*1e-6
    a=(150+(i%4)*10)*1e-6
    b=(120+(i%3)*12)*1e-6
    for j,L in enumerate([8e-5,3e-4,1e-3,5e-3,2e-2,1.,1e3,1e6]):
        setattr(CoreTests,f'test_parametric_{i:02d}_{j:02d}',_numerical_case(d,a,b,L))

if __name__=='__main__':unittest.main()
