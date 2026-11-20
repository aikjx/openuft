"""Independent analytic, dimensional, source-profile and inverse-problem tests.
Run: python -m unittest discover -s tests -v
"""
import unittest, math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src import model as m

V=m.V_QCD_GEV
XI=m.xi_from_newton_calibration()
A=m.alpha_xi(XI)
ELL=m.range_m(1,V,XI)

class ActionAndNormalization(unittest.TestCase):
    def test_mass_positive(self):self.assertGreater(m.canonical_mass_ev(1,V,XI),0)
    def test_canonical_scale(self):self.assertAlmostEqual(m.canonical_scale_f(V,XI)/(V*math.sqrt(6*XI)),1,places=12)
    def test_alpha(self):self.assertAlmostEqual(A,1/3,places=12)
    def test_G_calibration(self):
        self.assertAlmostEqual(XI*(V/m.MPL_OBS_GEV)**2/(1+A),1,places=12)
    def test_einstein_coupling_identity(self):
        self.assertAlmostEqual(2*(m.einstein_scale(V,XI)/m.canonical_scale_f(V,XI))**2,A,places=12)
    def test_range_mass(self):self.assertAlmostEqual(ELL*m.canonical_mass_ev(1,V,XI)/m.HBAR_C_EV_M,1,places=13)
    def test_range_lambda_scaling(self):
        for k in [.001,.01,.25,2,math.pi,4*math.pi,100]:
            self.assertAlmostEqual(m.range_m(k,V,XI)*math.sqrt(k)/ELL,1,places=12)
    def test_potential_vacuum(self):self.assertEqual(m.induced_potential_gev4(0,1,V,XI),0)
    def test_potential_positive(self):
        for h in [-2.,-.5,.5,2.]:
            self.assertGreater(m.induced_potential_gev4(h*V,1,V,XI),0)
    def test_matter_factor_vacuum(self):self.assertEqual(m.matter_factor(0,V,XI),1)
    def test_matter_factor_half(self):
        f=m.canonical_scale_f(V,XI)
        self.assertAlmostEqual(m.matter_factor(f*math.log(2),V,XI),.5,places=12)
    def test_potential_lam_scaling(self):
        self.assertAlmostEqual(m.induced_potential_gev4(.1*V,7,V,XI)/m.induced_potential_gev4(.1*V,1,V,XI),7,places=12)
    def test_mass_range_order(self):
        self.assertLess(m.range_m(4*math.pi,V,XI),m.range_m(1,V,XI))
        self.assertGreater(m.range_m(.01,V,XI),m.range_m(1,V,XI))
    def test_newton_xi_positive(self):self.assertGreater(XI,1e38)
    def test_general_newton_xi_small_ratio(self):
        for ratio in [.1,.5,1,3,10]:
            z=m.xi_from_newton_calibration(v_gev=1,mpl_gev=ratio)
            self.assertAlmostEqual(z/(1+m.alpha_xi(z))/ratio**2,1,places=12)
    def test_invalid_mass(self):
        for args in [(0,V,XI),(-1,V,XI),(1,-V,XI),(1,V,-2)]:
            with self.assertRaises(ValueError):m.canonical_mass_ev(*args)
    def test_invalid_xi_input(self):
        with self.assertRaises(AssertionError):m.alpha_xi(-.1)
    def test_invalid_calibration(self):
        with self.assertRaises(ValueError):m.xi_from_newton_calibration(0,1)
    def test_mass_lambda_upper_bound(self):
        self.assertGreater(m.range_m(4*math.pi,V,XI),30e3)
        self.assertLess(m.range_m(4*math.pi,V,XI),40e3)
    def test_point_inversion_quartic(self):
        for ell in [1e3,1e4,1e5,1e6,1e9]:
            q=m.quartic_needed_for_range(ell,V,XI)
            self.assertAlmostEqual(m.range_m(q,V,XI)/ell,1,places=12)
    def test_mass_from_range(self):self.assertAlmostEqual(m.mass_eV_from_range(ELL),m.canonical_mass_ev(1,V,XI),places=20)

class FiniteSource(unittest.TestCase):
    def test_form_factor_small_limit(self):
        for z in [0,1e-6,.001,.025]:
            self.assertAlmostEqual(m.homogeneous_yukawa_form(z),1+z*z/10,delta=1e-6)
    def test_form_factor_zero(self):self.assertEqual(m.homogeneous_yukawa_form(0),1)
    def test_scaled_zero(self):self.assertEqual(m.uniform_scaled_form(0),1)
    def test_scaled_matches_direct(self):
        for x in [.01,.1,1,5,10,30,100]:
            v1=m.uniform_scaled_form(x)
            v2=math.exp(-x)*m.homogeneous_yukawa_form(x)
            self.assertAlmostEqual(v1/v2,1,places=11)
    def test_scaled_height_factor(self):
        for h in [0,1,3,100]:
            self.assertAlmostEqual(m.uniform_scaled_form(10,h)/m.uniform_scaled_form(10),math.exp(-h),places=11)
    def test_inverse_r_form(self):
        for x in [.001,.03,.1,.5,2,12,50]:
            direct=math.exp(-x)*2*(math.cosh(x)-1)/(x*x)
            self.assertAlmostEqual(m.inverse_r_scaled_form(x)/direct,1,delta=2e-10)
    def test_inverse_r_zero(self):self.assertEqual(m.inverse_r_scaled_form(0),1)
    def test_exact_one_third(self):self.assertAlmostEqual(A,1/3,places=14)
    def test_uniform_surface_excess(self):
        self.assertAlmostEqual(m.yukawa_relative_force_sphere(ELL,0,coupling=A),.0097749036252,delta=1e-12)
    def test_inverse_r_surface_excess(self):
        self.assertAlmostEqual(m.yukawa_relative_force_sphere(ELL,0,coupling=A,profile='inverse_r'),.00664659172315,delta=1e-12)
    def test_surface_more_than_satellite(self):
        for p in ['uniform','inverse_r']:
            v0=m.yukawa_relative_force_sphere(ELL,0,profile=p)
            v500=m.yukawa_relative_force_sphere(ELL,500e3,profile=p)
            v1000=m.yukawa_relative_force_sphere(ELL,1000e3,profile=p)
            self.assertGreater(v0,v500);self.assertGreater(v500,v1000)
    def test_point_mass_wrong_for_Earth(self):
        point=m.yukawa_relative_force_point(ELL,m.EARTH_R_M,coupling=A)
        finite=m.yukawa_relative_force_sphere(ELL,0,coupling=A)
        self.assertGreater(finite,point*1e10)
    def test_source_profile_matters(self):
        homo=m.yukawa_relative_force_sphere(ELL,0,profile='uniform')
        other=m.yukawa_relative_force_sphere(ELL,0,profile='inverse_r')
        self.assertGreater(homo,other)
        self.assertGreater(homo/other,1.45)
    def test_uniform_ratio_gm_altitudes(self):
        r=m.two_altitude_force_ratio(ELL,0,500e3)
        self.assertLess(r,1);self.assertGreater(r,.98)
    def test_inverse_r_ratio_gm_altitudes(self):
        r=m.two_altitude_force_ratio(ELL,100e3,1000e3,profile='inverse_r')
        self.assertLess(r,1);self.assertGreater(r,.99)
    def test_homogeneous_scaled_large_no_overflow(self):
        self.assertTrue(math.isfinite(m.uniform_scaled_form(2000)))
        self.assertGreater(m.uniform_scaled_form(2000),0)
    def test_invalid_altitude(self):
        with self.assertRaises(ValueError):m.yukawa_relative_force_sphere(ELL,-1)
    def test_invalid_density(self):
        with self.assertRaises(ValueError):m.yukawa_relative_force_sphere(ELL,1,profile='invented')
    def test_invalid_yukawa_range(self):
        with self.assertRaises(ValueError):m.yukawa_relative_force_point(-1,1)
    def test_linear_coupling(self):
        y=m.yukawa_relative_force_sphere(ELL,10e3,coupling=.22)
        y2=m.yukawa_relative_force_sphere(ELL,10e3,coupling=.44)
        self.assertAlmostEqual(y2/y,2,places=12)
    def test_range_to_infinity_equal_point_mass(self):
        for ell in [1e12,1e14]:
            y=m.yukawa_relative_force_sphere(ell,1000e3)
            x=m.yukawa_relative_force_point(ell,m.EARTH_R_M+1000e3)
            self.assertAlmostEqual(y/x,1,delta=1e-6)
    def test_calibrated_near_field_no_deviation(self):
        res=m.relative_observable_after_G_calibration(ELL,10,1)
        self.assertLess(abs(res),2e-9)
    def test_calibrated_far_field_change(self):
        res=m.relative_observable_after_G_calibration(ELL,1e6,1)
        self.assertLess(res,-.2)
    def test_mass_coupling_strength(self):
        self.assertAlmostEqual(m.yukawa_relative_force_point(ELL,0),1/3)
    def test_density_at_100km(self):
        self.assertGreater(m.yukawa_relative_force_sphere(ELL,100e3),.004)
        self.assertLess(m.yukawa_relative_force_sphere(ELL,100e3),.005)
    def test_density_at_500km(self):
        self.assertGreater(m.yukawa_relative_force_sphere(ELL,500e3),1e-4)
        self.assertLess(m.yukawa_relative_force_sphere(ELL,500e3),3e-4)

class ExactSymbolic(unittest.TestCase):
    def test_Sympy_Einstein_potential_hessian(self):
        import sympy as s
        chi,v,xi,lam=s.symbols('chi v xi lam',real=True,positive=True)
        f=v*s.sqrt(1+6*xi)
        U=lam*v**4/s.Integer(4)*(1-s.exp(-2*chi/f))**2
        self.assertEqual(s.simplify(s.diff(U,chi,2).subs(chi,0)),2*lam*v*v/(1+6*xi))
    def test_Sympy_kinetic_change_of_variables(self):
        import sympy as s
        phi,v,xi=s.symbols('phi v xi',positive=True)
        F=xi*phi**2; M2=xi*v**2
        K=M2/F+s.Rational(3,2)*M2*(s.diff(F,phi)/F)**2
        self.assertEqual(s.simplify(K-(1+6*xi)*v*v/phi**2),0)
    def test_Sympy_Einstein_potential_exact(self):
        import sympy as s
        v,xi,lam,chi=s.symbols('v xi lam chi',positive=True)
        f=v*s.sqrt(1+6*xi);phi=v*s.exp(chi/f)
        V=lam*s.Rational(1,4)*(phi**2-v**2)**2
        U=(v/phi)**4*V
        expected=lam*v**4*s.Rational(1,4)*(1-s.exp(-2*chi/f))**2
        self.assertEqual(s.simplify(U-expected),0)
    def test_Sympy_matter_factor(self):
        import sympy as s
        phi,v,xi,chi=s.symbols('phi v xi chi',positive=True)
        f=v*s.sqrt(1+6*xi)
        self.assertEqual(s.simplify((v/(v*s.exp(chi/f)))-s.exp(-chi/f)),0)
    def test_Sympy_Newton_xi_quadratic(self):
        import sympy as s
        xi,R=s.symbols('xi R',positive=True)
        eq=xi*(1+6*xi)-R*(1+8*xi)
        self.assertEqual(s.expand(eq-(6*xi**2+(1-8*R)*xi-R)),0)
    def test_Sympy_Yukawa_force_derivative(self):
        import sympy as s
        r,R,ell,a,G,M=s.symbols('r R ell a G M',positive=True)
        x=R/ell; form=s.symbols('form',positive=True)
        potential=-G*M*a*form*s.exp(-r/ell)/r
        magnitude=s.diff(potential,r)
        target=G*M*a*form*s.exp(-r/ell)*(1+r/ell)/r**2
        self.assertEqual(s.simplify(magnitude-target),0)
    def test_Sympy_uniform_form_integral(self):
        import sympy as s
        x=s.symbols('x',positive=True)
        u=s.symbols('u',nonnegative=True)
        expr=s.integrate(3*u*s.sinh(x*u)/x,(u,0,1))
        expected=3*(x*s.cosh(x)-s.sinh(x))/x**3
        self.assertEqual(s.simplify(expr-expected),0)
    def test_Sympy_uniform_scaled_form(self):
        import sympy as s
        x,u=s.symbols('x u',positive=True)
        lhs=s.exp(-x-u)*3*(x*s.cosh(x)-s.sinh(x))/x**3
        rhs=3*((x-1)*s.exp(-u)+(x+1)*s.exp(-2*x-u))/(2*x**3)
        self.assertEqual(s.simplify(s.expand(lhs.rewrite(s.exp))-rhs),0)
    def test_Sympy_inverse_r_shape(self):
        import sympy as s
        x=s.symbols('x',positive=True)
        self.assertEqual(s.simplify(s.expand((2*(s.cosh(x)-1)*s.exp(-x)-(1-s.exp(-x))**2).rewrite(s.exp))),0)

class HighPrecisionIndependent(unittest.TestCase):
    def test_mpmath_xi_calibration(self):
        import mpmath as mp
        mp.mp.dps=65
        R=(mp.mpf(str(m.MPL_OBS_GEV))/mp.mpf(str(V)))**2
        xi=(8*R-1+mp.sqrt((8*R-1)**2+24*R))/12
        self.assertAlmostEqual(float(xi)/XI,1,places=12)
    def test_mpmath_homogeneous_form_factor(self):
        import mpmath as mp
        mp.mp.dps=65
        for x in [mp.mpf('.2'),mp.mpf('5'),mp.mpf('51.131834687429524')]:
            q=3*mp.quad(lambda z:z*mp.sinh(x*z)/x,[0,1])
            p=3*(x*mp.cosh(x)-mp.sinh(x))/(x**3)
            self.assertLess(abs(q/p-1),mp.mpf('1e-45'))
    def test_mpmath_mass(self):
        import mpmath as mp
        mp.mp.dps=65
        xi=mp.mpf(str(XI));v=mp.mpf(str(V));
        mass=mp.sqrt(2)*v*mp.mpf('1e9')/mp.sqrt(1+6*xi)
        self.assertAlmostEqual(float(mass)/m.canonical_mass_ev(1,V,XI),1,places=12)

if __name__=='__main__':unittest.main()
