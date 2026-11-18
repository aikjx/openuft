import unittest, math
import numpy as np
from scipy.integrate import quad
from rootv71.physics import *

class YukawaTests(unittest.TestCase):
    def test_uniform_limits(self): self.assertAlmostEqual(uniform_sphere_form_factor(0),1)
    def test_nonnegative(self):
        for x in [0,.01,.2,2,12]:self.assertGreaterEqual(uniform_sphere_form_factor(x),1)
    def test_small_x(self): self.assertAlmostEqual(uniform_sphere_form_factor(.001),1+.001**2/10,places=10)
    def test_large_x_stable(self): self.assertTrue(math.isfinite(stable_surface_form(1e7)))
    def test_stable_large_x_asymptotic(self):
        x=1e5
        self.assertAlmostEqual(stable_surface_form(x)/(1.5/x**2),1,delta=2e-5)
    def test_point_limit(self):
        self.assertAlmostEqual(uniform_ratio(1.,.1,1e7),point_ratio(1.,.1,1e7),delta=1e-12)
    def test_layered_analytic_crosscheck(self):
        for x in [.001,.1,1.,5.,15.,17.,80.,1e5]:
            self.assertAlmostEqual(layered_surface_form(homogeneous_shells(1),1/x),stable_surface_form(x),delta=3e-11)
    def test_same_mass(self):
        self.assertAlmostEqual(mass_shells(homogeneous_shells(1)),mass_shells(same_mass_layered_shells(1)),places=12)
    def test_newton_external_shell_structure(self):
        self.assertAlmostEqual(mass_shells(homogeneous_shells(4)),mass_shells(same_mass_layered_shells(4)))
    def test_yukawa_internal_structure_effect(self):
        a=layered_ratio(homogeneous_shells(1),0.,.1)
        b=layered_ratio(same_mass_layered_shells(1),0.,.1)
        self.assertGreater(a,b)
    def test_charge_changes_sign(self):
        self.assertLess(uniform_ratio(10.,0.,10.,qtest=-1.),0.)
    def test_scale_linear_alpha(self):
        self.assertAlmostEqual(uniform_ratio(1.,0.,.7,alpha=2),2*uniform_ratio(1.,0.,.7))
    def test_altitude_monotone(self):
        self.assertGreater(uniform_ratio(1.,0.,.5),uniform_ratio(1.,.2,.5))
    def test_delta_g_grad(self):
        # potential U_Y/m=-G alpha M*F exp(-r/lambda)/r;
        # acceleration correction to G*M/r² = alpha F e^-r/lambda (1+r/lambda)
        R=1.;lam=.7;h=.4;eps=1e-5;r=R+h
        F=uniform_sphere_form_factor(R/lam)
        def potential(rr):return -F*math.exp(-rr/lam)/rr
        gmag=(potential(r+eps)-potential(r-eps))/(2*eps)
        self.assertAlmostEqual(gmag*r*r,uniform_ratio(R,h,lam),delta=1e-8)
    def test_layered_integral_independent(self):
        R=1.; lam=.4; shells=same_mass_layered_shells(R)
        def integrand(s):
            rho=1.5 if s<=.5 else 13/14
            k=math.sinh(s/lam)/(s/lam) if s else 1.
            return 4*math.pi*rho*s*s*k*math.exp(-R/lam)
        m=mass_shells(shells)
        integral=(quad(integrand,0.,.5,epsabs=1e-12)[0]+quad(integrand,.5,1.,epsabs=1e-12)[0])/m
        self.assertAlmostEqual(layered_surface_form(shells,lam),integral,delta=1e-11)
    def test_large_x_no_point_source(self):
        R=EARTH_R;lam=1000.
        self.assertEqual(point_ratio(R,0.,lam),0.)  # floating underflow
        self.assertGreater(uniform_ratio(R,0.,lam),0.)
    def test_large_x_surface_lam_scaling(self):
        R=1e6;lam=1e2
        # ratio behaves 3lambda/(2R) at fixed h=0 and lambda<<R
        self.assertAlmostEqual(uniform_ratio(R,0.,lam)/(1.5*lam/R),1,delta=2e-4)
    def test_short_range_core_insensitivity(self):
        R=1.;lam=.001
        corechange=layered_ratio(same_mass_layered_shells(R,qcore=5.,qshell=1.),0.,lam)
        plain=layered_ratio(same_mass_layered_shells(R,qcore=1.,qshell=1.),0.,lam)
        self.assertAlmostEqual(corechange,plain,delta=1e-12)
    def test_q_weighted_long_range(self):
        shells=same_mass_layered_shells(1.,qcore=2.,qshell=1.)
        qmean=(1.5*(.5**3)*2+(13/14)*(1-.5**3)*1)/(1.5*(.5**3)+(13/14)*(1-.5**3))
        self.assertAlmostEqual(layered_surface_form(shells,1e10),qmean,delta=1e-8)
    def test_bad_radius(self):
        with self.assertRaises(ValueError):uniform_ratio(0.,0.,1.)
    def test_bad_lambda(self):
        with self.assertRaises(ValueError):layered_ratio(homogeneous_shells(1),0.,0.)
    def test_bad_shells(self):
        with self.assertRaises(ValueError):mass_shells([Shell(1,2),Shell(.5,2)])
    def test_shell_negative_density(self):
        with self.assertRaises(ValueError):mass_shells([Shell(1,-2)])
    def test_zero_source_mass(self):
        with self.assertRaises(ValueError):mass_shells([Shell(1,0)])
    def test_charge_profile_linearity(self):
        sh=same_mass_layered_shells(1.,qcore=2,qshell=1.)
        a=layered_surface_form(sh,.5)
        b=layered_surface_form(same_mass_layered_shells(1.,qcore=4,qshell=2),.5)
        self.assertAlmostEqual(b,2*a,delta=1e-12)
    def test_earth_g_positive(self):self.assertTrue(9.7<central_gravity(EARTH_MU,EARTH_R)<9.9)
    def test_redshift_small_h(self):
        h=.001
        self.assertAlmostEqual(redshift_height(EARTH_MU,EARTH_R,h),EARTH_MU/EARTH_R**2*h/C**2,delta=1e-27)
    def test_tidal(self):self.assertAlmostEqual(tidal_radial(EARTH_MU,EARTH_R),2*central_gravity(EARTH_MU,EARTH_R)/EARTH_R)
    def test_micro_bound_positive(self):self.assertGreater(micro_WEP_bound_eta(.3,.5,EARTH_R,1e5,1e7),0)
    def test_micro_bound_no_composition(self):self.assertEqual(micro_WEP_bound_eta(0.,.5,EARTH_R,0.,1e7),math.inf)

if __name__=='__main__':unittest.main()
