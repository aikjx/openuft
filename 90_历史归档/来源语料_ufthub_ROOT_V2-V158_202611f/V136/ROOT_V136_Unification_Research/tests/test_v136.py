import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import v136_physics as p
old=p.old

class TestYukawaNullTests(unittest.TestCase):
    def setUp(self):
        self.R=old.R_EARTH_MEAN
        self.l=old.EARTH_LAYERS
    def test_earth_reference_fixed_ratio(self):
        x=p.relative_force_deviation(self.R,self.R+400e3,self.l)
        self.assertAlmostEqual(x,0.006009780629580241,delta=1e-13)
    def test_mu_exact_cancellation(self):
        a=self.R;b=a+400e3
        expected=p.relative_force_deviation(a,b,self.l)
        for mu in (old.MU_EARTH,old.MU_EARTH*0.7,old.MU_EARTH*1.23):
            actual=p.weighted_radial_force(a,mu,self.l)/p.weighted_radial_force(b,mu,self.l)-1
            self.assertAlmostEqual(actual,expected,delta=4e-16)
    def test_zero_alpha_null(self):
        self.assertEqual(p.relative_force_deviation(self.R,self.R+400e3,self.l,0),0)
    def test_analytic_attenuation(self):
        for lay in (old.EARTH_LAYERS,old.MOON_LAYERS):
            R=old.check_shells(lay)
            e1=p.eps_at(R,lay)
            e2=p.eps_at(R+400e3,lay)
            self.assertAlmostEqual(e2/e1,p.yukawa_decay_shape(R,R+400e3,old.ROOT_LAMBDA),places=12)
    def test_alpha_independent_three_point(self):
        r0=self.R;r1=r0+200e3;r2=r0+400e3
        ratios=[p.three_altitude_shape_ratio(r0,r1,r2,self.l,a) for a in (.003,.03,.3,1.)]
        for x in ratios:self.assertAlmostEqual(x,ratios[0],places=12)
    def test_density_independent_three_point(self):
        r0=self.R;r1=r0+200e3;r2=r0+400e3
        d1=p.three_altitude_shape_ratio(r0,r1,r2,self.l)
        alt=(old.Layer(0.,self.R,5514.),)
        d2=p.three_altitude_shape_ratio(r0,r1,r2,alt)
        self.assertEqual(d1,d2)
    def test_three_point_raw_accel(self):
        r0=self.R;r1=r0+200e3;r2=r0+400e3
        y=[p.weighted_radial_force(r,old.MU_EARTH,self.l) for r in (r0,r1,r2)]
        direct=(y[0]-y[1])/(y[1]-y[2])
        calc=p.three_altitude_shape_ratio(r0,r1,r2,self.l)
        self.assertAlmostEqual(direct,calc,delta=5e-12)
    def test_three_point_zero_is_undefined(self):
        with self.assertRaises(ValueError):
            p.three_altitude_shape_ratio(self.R,self.R+100e3,self.R+400e3,self.l,0.)
    def test_decay_monotone(self):
        ratios=[p.eps_at(self.R+h,self.l) for h in (0.,100e3,200e3,400e3,800e3)]
        self.assertTrue(all(a>b>0 for a,b in zip(ratios,ratios[1:])))
    def test_epsilon_derivative_independent(self):
        for h in (1e3,100e3,400e3):
            r=self.R+h; step=1.
            fd=(p.eps_at(r+step,self.l)-p.eps_at(r-step,self.l))/(2*step)
            self.assertAlmostEqual(fd,p.eps_radial_derivative(r,self.l),delta=abs(fd)*1e-8)
    def test_epicycle_identity(self):
        for h in (0.,100e3,400e3,800e3):
            r=self.R+h
            a=p.epicycle_from_eps_gradient(r,old.MU_EARTH,self.l)
            b=old.near_circular_orbit_frequencies(r,old.MU_EARTH,self.l)
            self.assertAlmostEqual(a['omega2'],b['Omega2_s_minus2'],delta=1e-18)
            self.assertAlmostEqual(a['kappa2'],b['kappa2_s_minus2'],delta=1e-18)
            self.assertAlmostEqual(a['precession'],b['precession_rad_per_rev'],delta=1e-13)
    def test_negative_alpha_produces_other_sign(self):
        r=self.R+400e3
        result=p.epicycle_from_eps_gradient(r,old.MU_EARTH,self.l,alpha=-.01)
        self.assertTrue(result['stable'])
        self.assertLess(result['precession'],0.)
    def test_surface_ratio_differs_earth_moon(self):
        earth=p.eps_at(self.R,self.l)
        moon=p.eps_at(old.R_MOON,old.MOON_LAYERS)
        self.assertGreater(moon,earth)
    def test_radius_validation(self):
        with self.assertRaises(ValueError):
            p.three_altitude_shape_ratio(self.R-1,self.R,self.R+1,self.l)
        with self.assertRaises(ValueError):
            p.yukawa_decay_shape(1.,2.,-1.)

class TestGeometryAndOrthogonality(unittest.TestCase):
    def test_null_speed_identity(self):
        for u in (.05,.3,.8,.999):
            w=.25;a=math.sqrt(1-u*u)/w
            h=p.helix_geometry(a,w,u)
            self.assertAlmostEqual(h['speed2'],1,places=12)
            self.assertAlmostEqual(h['frequency_norm'],w,places=12)
    def test_constant_speed_acceleration_not_zero(self):
        a,w,u=p.free_pitch_for_ratio(1.,2.)
        h=p.helix_geometry(a,w,u)
        self.assertGreater(h['acceleration_magnitude'],0)
    def test_arbitrary_geometry_ratio(self):
        for target in (.00001,1/137.035999084,.1,1.,100.):
            a,w,u=p.free_pitch_for_ratio(target,1.7)
            h=p.helix_geometry(a,w,u)
            self.assertAlmostEqual(h['torsion']/h['curvature'],target,delta=max(1e-12,target*1e-13))
    def test_parallel_em_fields_counterexample(self):
        E=(0.,0.,4.);B=(0.,0.,3.)
        self.assertEqual(p.dot3(E,B),12.)
        self.assertEqual(p.cross3(E,B),(0.,0.,0.))
    def test_lorentz_invariant_both_scalars(self):
        E=(2.,-1.,4.);B=(1.,4.,3.)
        invariant=p.em_invariants(E,B)
        E2,B2=p.lorentz_boost_fields(E,B,(.45,.1,-.2))
        transformed=p.em_invariants(E2,B2)
        for a,b in zip(invariant,transformed):self.assertAlmostEqual(a,b,delta=1e-12)
    def test_parallel_fields_stay_nonorthogonal(self):
        E=(0.,0.,4.);B=(0.,0.,3.)
        Ep,Bp=p.lorentz_boost_fields(E,B,(.5,0.,0.))
        self.assertAlmostEqual(p.dot3(Ep,Bp),12.,places=11)
    def test_cannot_boost_at_light_speed(self):
        with self.assertRaises(ValueError):
            p.lorentz_boost_fields((0.,0.,1.),(1.,0.,0.),(1.,0.,0.))
    def test_gauss_inverse_square(self):
        for r in (1.,200.,old.R_EARTH_MEAN,old.R_EARTH_MEAN+400e3):
            self.assertAlmostEqual(p.gauss_flux_newton(r,old.MU_EARTH),4*math.pi*old.MU_EARTH,delta=1.)

if __name__=='__main__':unittest.main()
