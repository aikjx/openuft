import math, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src import core as c
import sympy as s

class GravityModels(unittest.TestCase):
    def test_qcd_baseline(self): self.assertAlmostEqual(c.lambda_one_loop(),.08782708014552353,places=12)
    def test_planck_baseline(self): self.assertAlmostEqual(c.Mplbar_observed()/2.435323459338203e18,1,places=13)
    def test_vev_ratio(self): self.assertAlmostEqual(c.xi_eh_match()/7.688761955262903e38,1,places=13)
    def test_bd_no_bare(self):
        for x in [1e-9,1e-5,.1,1,100,1e35]:
            self.assertTrue(math.isclose(c.bd_omega(x,1),1/(4*x),rel_tol=1e-13))
    def test_general_bd(self):
        xi=2.;v=3.;m0=100.
        self.assertAlmostEqual(c.bd_omega(xi,v,m0),(m0+xi*v*v)/(4*xi*xi*v*v),places=13)
    def test_gamma_bd_equivalence(self):
        for x in [1e-7,1e-4,.01,.25,1,123456.]:
            self.assertAlmostEqual(c.gamma_massless(x,1),c.gamma_from_bd(c.bd_omega(x,1)),places=12)
    def test_gamma_xi_closed(self):
        for x in [1e-8,1e-2,1,10000.]:
            self.assertAlmostEqual(c.gamma_massless(x,1),(1+4*x)/(1+8*x),places=12)
    def test_gamma_canonical_limits(self):
        self.assertGreater(c.gamma_massless(1e-9,1),.99999999)
        self.assertAlmostEqual(c.gamma_massless(1e38,1),.5,places=14)
    def test_alpha2_limits(self):
        self.assertAlmostEqual(c.alpha2_massless(1e38,1),1/3,places=14)
    def test_newton_calibration(self):
        for x in [1e-3,1e-1,1,1e6]:
            self.assertAlmostEqual(c.grav_newton_F_ratio(x,1),1+c.alpha2_massless(x,1),places=12)
    def test_corrected_match_greater(self):
        self.assertGreater(float(c.solve_pure_massless_xi_match()),c.xi_eh_match())
    def test_corrected_match_ratio(self):
        self.assertAlmostEqual(float(c.solve_pure_massless_xi_match())/c.xi_eh_match(),4/3,places=13)
    def test_cassini_delta(self): self.assertAlmostEqual(c.cassini_delta_lower(),2.5e-5,places=14)
    def test_cassini_xi_upper(self): self.assertAlmostEqual(c.xi_cassini_pure_massless_bound(),6.250312515625781e-6,places=16)
    def test_cassini_omega_lower(self): self.assertAlmostEqual(c.omega_cassini_bound()/39998,1,places=11)
    def test_minimum_vev_pure_massless_huge(self):
        self.assertGreater(c.minimal_vev_for_pure_massless_cassini(),9e20)
    def test_cassini_equal_boundary(self):
        x=c.xi_cassini_pure_massless_bound()
        self.assertAlmostEqual(c.gamma_massless(x,1),c.cassini_min_gamma(),places=13)
    def test_bare_plus_induced_xi_upper(self):
        self.assertAlmostEqual(c.conservative_bare_plus_induced_xi_bound()/6.932327536884497e16,1,places=4)
    def test_fraction_upper(self): self.assertLess(c.max_induced_fraction_bound(),1e-21)
    def test_fraction_positive(self): self.assertGreater(c.max_induced_fraction_bound(),0)
    def test_massless_toy_is_excluded(self):
        self.assertLess(c.gamma_massless(c.xi_eh_match(),c.lambda_one_loop()),c.cassini_min_gamma())
    def test_massive_gamma_no_range_change_at_zero(self):
        for a in [0.001,.1,1/3]:self.assertAlmostEqual(c.gamma_radius(a,0),(1-a)/(1+a),places=12)
    def test_gamma_massive_goes_to_one(self): self.assertAlmostEqual(c.gamma_radius(1/3,100),1.,places=12)
    def test_orbit_force_decreases(self):
        for a in [.02,1/3,.9]:
            self.assertGreater(c.effective_orbit_G_ratio(a,0),c.effective_orbit_G_ratio(a,5))
    def test_gamma_fit_differs_local(self):
        a=1/3;x=1
        self.assertLess(c.gamma_fit_orbit_calibrated(a,x),c.gamma_radius(a,x))
    def test_gamma_fit_at_zero_equal(self):
        self.assertAlmostEqual(c.gamma_fit_orbit_calibrated(.2,0),c.gamma_radius(.2,0),places=12)
    def test_local_r_1au(self): self.assertAlmostEqual(c.illustrative_lambda_max_over_r(1/3),.09812428439119493,places=12)
    def test_mass_benchmark(self): self.assertAlmostEqual(c.illustrative_scalar_mass_min_eV(1/3)/1.3442639609979376e-17,1,places=8)
    def test_no_coupling_case(self): self.assertEqual(c.illustrative_scalar_mass_min_eV(1e-8),0)
    def test_invalid(self):
        for vals in [(0,1,0),(1,0,0),(1,1,-1)]:
            with self.assertRaises(ValueError):c.F_value(*vals)
    def test_invalid_qcd(self):
        with self.assertRaises(ValueError):c.lambda_one_loop(-1)
    def test_summary_open(self):
        self.assertIn('OPEN',c.summary()['theory_status'])
    def test_scalar_fraction_not_100pct_if_light(self):
        self.assertLess(c.max_induced_fraction_bound(),1.)

class SymbolicProofs(unittest.TestCase):
    def test_change_of_field(self):
        xi,phi=s.symbols('xi phi',positive=True)
        Phi=xi*phi**2
        omega=Phi/s.diff(Phi,phi)**2
        self.assertEqual(s.simplify(omega-1/(4*xi)),0)
    def test_change_of_field_plus_bare(self):
        xi,phi,m0=s.symbols('xi phi m0',positive=True)
        Phi=m0**2+xi*phi**2
        self.assertEqual(s.simplify(Phi/s.diff(Phi,phi)**2-Phi/(4*xi**2*phi**2)),0)
    def test_massless_gamma_simplification(self):
        xi=s.symbols('xi',positive=True)
        om=1/(4*xi)
        self.assertEqual(s.simplify((om+1)/(om+2)-(1+4*xi)/(1+8*xi)),0)
    def test_fifth_force_alpha2(self):
        xi=s.symbols('xi',positive=True)
        self.assertEqual(s.simplify(1/(2/(4*xi)+3)-2*xi/(1+6*xi)),0)
    def test_xi_ppn_bound(self):
        delta=s.symbols('delta',positive=True)
        x=delta/(4-8*delta)
        self.assertEqual(s.factor(1-(1+4*x)/(1+8*x)-delta),0)
    def test_full_newton_match_quadratic(self):
        xi,R=s.symbols('xi R',positive=True)
        a=2*xi/(1+6*xi)
        eq=s.together(xi-R*(1+a))
        self.assertEqual(s.simplify(s.together(eq)*(1+6*xi)-(6*xi*xi+(1-8*R)*xi-R)),0)
    def test_two_potentials_sum(self):
        a,e,u=s.symbols('a e u')
        self.assertEqual(s.simplify(u*(1+a*e)+u*(1-a*e)-2*u),0)
    def test_radial_derivative_orbit_factor(self):
        G,M,r,lam,a=s.symbols('G M r lam a',positive=True)
        U=G*M*(1+a*s.exp(-r/lam))/r
        g=-s.diff(U,r)
        self.assertEqual(s.simplify(g-G*M*(1+a*(1+r/lam)*s.exp(-r/lam))/r**2),0)
    def test_log_derivative_monotone(self):
        x,r=s.symbols('x r',positive=True)
        f=(1+x)*s.exp(-x)
        self.assertEqual(s.simplify(s.diff(f,x)),-x*s.exp(-x))
    def test_orbit_gamma_calibration(self):
        t=s.symbols('t',positive=True)
        g=(1-t)/(1+t)
        self.assertEqual(s.simplify((1+g)*(1+t)-2),0)
    def test_QCD_RG_lambda_invariance(self):
        b,alpha,mu=s.symbols('b alpha mu',positive=True)
        beta=-b*alpha**2/(2*s.pi)
        logLam=s.log(mu)-2*s.pi/(b*alpha)
        self.assertEqual(s.simplify(s.diff(logLam,mu)*mu+s.diff(logLam,alpha)*beta),0)

if __name__=='__main__': unittest.main()
