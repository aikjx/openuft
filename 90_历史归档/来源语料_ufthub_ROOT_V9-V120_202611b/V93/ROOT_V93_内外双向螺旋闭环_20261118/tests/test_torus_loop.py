import math
import unittest
import numpy as np
from numpy.testing import assert_allclose
from src.torus_loop import TorusLoop, C, HBAR_EXACT_FROM_H, E, ME

class TorusLoopTest(unittest.TestCase):
    def setUp(self): self.loop=TorusLoop()
    def test_invalid_geometry(self):
        for R,a,m,n in [(1,1,2,3),(1,-.1,2,3),(1,2,2,3),(1,.2,0,3),(1,.2,2,-3),(1,.2,2,1.5)]:
            with self.subTest(params=(R,a,m,n)),self.assertRaises(ValueError): TorusLoop(R,a,m,n)
    def test_primitive_period_23(self):
        self.assertAlmostEqual(self.loop.primitive_period,2*math.pi)
    def test_primitive_period_46(self):
        self.assertAlmostEqual(TorusLoop(m=4,n=6).primitive_period,math.pi)
    def test_closed_position(self):
        c=self.loop
        assert_allclose(c.pos(0),c.pos(c.primitive_period),rtol=0,atol=1e-16)
    def test_closed_tangent_first_and_second(self):
        c=self.loop
        for j in [0,1,2]:
            assert_allclose(c._components(0)[j],c._components(c.primitive_period)[j],rtol=0,atol=1e-14)
    def test_positive_rho(self):
        u=np.linspace(0,self.loop.primitive_period,1001)
        rho=np.hypot(*self.loop.pos(u)[...,:2].T)
        self.assertGreaterEqual(np.min(rho),self.loop.R-self.loop.a-1e-15)
    def test_inner_outer_exact(self):
        c=self.loop
        self.assertAlmostEqual(np.linalg.norm(c.pos(0)[:2]),c.R+c.a)
        self.assertAlmostEqual(np.linalg.norm(c.pos(math.pi/c.n)[:2]),c.R-c.a)
    def test_sigma_matches_finite_difference(self):
        c=self.loop
        for u in [.1,.4,1.1,2.6]:
            h=1e-5
            speed=np.linalg.norm((c.pos(u+h)-c.pos(u-h))/(2*h))
            self.assertAlmostEqual(speed/c.sigma(u),1,places=9)
    def test_beta_speed_exact_1000_samples(self):
        c=self.loop
        u=np.linspace(0,c.primitive_period,1000)
        for beta in [.2,.8,1.]:
            vr,vt,vz,om,vp=c.speed_components(u,beta)
            assert_allclose(vr**2+vt**2+vz**2,np.full_like(u,(beta*C)**2),rtol=2e-15)
            assert_allclose(vr**2+vz**2,vp**2,rtol=3e-15)
    def test_invalid_beta(self):
        for beta in [-.1,0,1.001]:
            with self.assertRaises(ValueError): self.loop.speed_components(0,beta)
    def test_omega_nonconstant_and_inner_faster(self):
        c=self.loop
        om_out=c.speed_components(0)[3]
        om_in=c.speed_components(math.pi/c.n)[3]
        self.assertGreater(om_in,om_out)
        self.assertGreater(om_in/om_out,1.4)
    def test_period_matches_quad_inversion(self):
        c=self.loop
        u,t=c.time_map(N=20001)
        self.assertLess(abs(t[-1]/c.period() - 1),2e-9)
    def test_interpolate_u_of_t(self):
        c=self.loop; u,t=c.time_map(beta=.6,N=50001)
        ix=np.array([500,5000,10000,30000,49000])
        recovered=c.phase_at_times(t[ix],beta=.6,N=50001)
        assert_allclose(recovered,u[ix],atol=1e-9)
    def test_negative_physical_time(self):
        with self.assertRaises(ValueError):self.loop.phase_at_times(np.array([-.01]))
    def test_acceleration_perpendicular(self):
        c=self.loop
        u=np.linspace(.1,c.primitive_period-.1,201)
        q1,*_=c._components(u); acc=c.accel_components(u,beta=.8)
        v=q1*(.8*C/c.sigma(u))[...,None]
        ratio=np.sum(v*acc,axis=-1)/(np.linalg.norm(v,axis=-1)*np.linalg.norm(acc,axis=-1))
        self.assertLess(np.max(abs(ratio)),5e-15)
    def test_acceleration_kappa(self):
        c=self.loop; u=np.linspace(0,c.primitive_period,231)
        acc=c.accel_components(u,beta=.8)
        assert_allclose(np.linalg.norm(acc,axis=-1),(.8*C)**2*c.curvature(u),rtol=5e-15)
    def test_finite_difference_curvature(self):
        c=self.loop
        for u in [.23,.75,1.23,2.2]:
            h=1e-4
            q1=(c.pos(u+h)-c.pos(u-h))/(2*h)
            q2=(c.pos(u+h)-2*c.pos(u)+c.pos(u-h))/h**2
            k=np.linalg.norm(np.cross(q1,q2))/np.linalg.norm(q1)**3
            self.assertLess(abs(k/c.curvature(u)-1),1e-7)
    def test_finite_difference_torsion(self):
        c=self.loop
        for u in [.43,1.13,2.23]:
            h=1e-3
            q1=(c.pos(u-2*h)-8*c.pos(u-h)+8*c.pos(u+h)-c.pos(u+2*h))/(12*h)
            q2=(-c.pos(u-2*h)+16*c.pos(u-h)-30*c.pos(u)+16*c.pos(u+h)-c.pos(u+2*h))/(12*h*h)
            # central third derivative stencil
            q3=(-c.pos(u-2*h)+2*c.pos(u-h)-2*c.pos(u+h)+c.pos(u+2*h))/(2*h**3)
            k=np.dot(np.cross(q1,q2),q3)/np.linalg.norm(np.cross(q1,q2))**2
            self.assertLess(abs(k-c.torsion(u)),.01)
    def test_nonzero_curvature_at_1000_points(self):
        u=np.linspace(0,self.loop.primitive_period,1000)
        self.assertGreater(np.min(self.loop.curvature(u)),1)
    def test_fenchel(self): self.assertGreater(self.loop.total_curvature(),2*math.pi)
    def test_fary_milnor_trefoil(self): self.assertGreater(self.loop.total_curvature(),4*math.pi)
    def test_length_greater_azimuth_lower_bound(self):
        self.assertGreater(self.loop.arc_length(), self.loop.m*2*math.pi*(self.loop.R-self.loop.a))
    def test_length_scales_with_radii(self):
        c=self.loop
        scaled=TorusLoop(c.R*4,c.a*4,c.m,c.n)
        self.assertAlmostEqual(scaled.arc_length()/c.arc_length(),4)
        self.assertAlmostEqual(scaled.curvature(.4)/c.curvature(.4),1/4)
        self.assertAlmostEqual(scaled.torsion(.4)/c.torsion(.4),1/4)
    def test_wilson_flux_numeric_quadrature(self):
        for m,n in [(2,3),(3,4),(4,6),(1,3),(3,1)]:
            c=TorusLoop(m=m,n=n)
            for B in [-0.2,.03]:
                with self.subTest(m=m,n=n,B=B):
                    self.assertAlmostEqual(c.numerical_flux(B),c.wilson_flux(B),delta=1e-12*max(abs(c.wilson_flux(B)),1e-25))
    def test_wilson_gauge_gradient_closed(self):
        # ∮grad(chi).dl=chi(end)-chi(start)=0 for periodic single-valued chi.
        c=self.loop; u=np.linspace(0,c.primitive_period,10001)
        chi=np.sin(2*u)+.3*np.cos(7*u)
        self.assertLess(abs(chi[-1]-chi[0]),1e-14)
    def test_flux_independent_n_for_coprime(self):
        a=TorusLoop(m=2,n=3).wilson_flux(.1)
        b=TorusLoop(m=2,n=5).wilson_flux(.1)
        self.assertAlmostEqual(a,b)
    def test_force_nonlight_beta(self):
        with self.assertRaises(ValueError):self.loop.relativistic_inverse_force(0,beta=1)
    def test_inverse_force_lorentz(self):
        c=self.loop; k=c.curvature(np.array([0,.2,1.]))
        force,B=c.relativistic_inverse_force(np.array([0,.2,1.]),beta=.8)
        gamma=1/math.sqrt(1-.8**2)
        assert_allclose(force,gamma*ME*(.8*C)**2*k,rtol=1e-15)
        assert_allclose(B,force/(E*.8*C),rtol=1e-15)
    def test_torsion_not_topological_integer(self):
        val=self.loop.signed_total_torsion()
        self.assertGreater(val,.01)
        self.assertGreater(abs(val/(2*math.pi)-round(val/(2*math.pi))),.01)
    def test_net_impulse_over_closed_loop_zero(self):
        c=self.loop
        impulse=c.net_impulse_per_unit_mass(beta=.8)
        self.assertLess(np.linalg.norm(impulse)/(.8*C),1e-11)
    def test_acceleration_lab_cartesian_finite_differences(self):
        c=self.loop; u=.51;beta=.8; h=1e-5
        v=lambda s:(c.pos(s+h)-c.pos(s-h))/(2*h)*(beta*C/c.sigma(s))
        a_num=(v(u+h)-v(u-h))/(2*h)*(beta*C/c.sigma(u))
        a_exact=c.accel_cartesian(u,beta)
        self.assertLess(np.linalg.norm(a_num-a_exact)/np.linalg.norm(a_exact),1e-6)
    def test_zero_work_v_dot_force(self):
        c=self.loop; us=np.linspace(.01,c.primitive_period-.01,101)
        q1,*_=c._components(us);v=q1*(.8*C/c.sigma(us))[...,None]
        F=c.accel_components(us,beta=.8)
        self.assertLess(np.max(np.abs(np.sum(v*F,axis=-1)))/((.8*C)**3*np.max(c.curvature(us))),1e-14)

    def test_radiation_power_positive_and_scales_as_q_squared(self):
        c=self.loop
        p=c.classical_radiated_power(np.array([0.,1.]),beta=.8,charge=E)
        pp=c.classical_radiated_power(np.array([0.,1.]),beta=.8,charge=2*E)
        self.assertTrue(np.all(p>0))
        assert_allclose(pp,4*p)
    def test_classical_radiative_energy_nonzero(self):
        c=self.loop
        e=c.classical_radiated_energy_one_lap(beta=.8)
        self.assertTrue(0<e<1e-18)

    def test_baseline_precise(self):
        c=self.loop
        self.assertAlmostEqual(c.arc_length(),.1312986594444883,places=12)
        self.assertAlmostEqual(c.total_curvature(),13.03204942973894,places=8)

class RandomizedGeometryTests(unittest.TestCase):
    def test_random_closed_and_velocity(self):
        rng=np.random.default_rng(20261118)
        for j in range(300):
            R=float(rng.uniform(.002,.05))
            a=float(R*rng.uniform(.02,.75))
            m=int(rng.integers(1,7)); n=int(rng.integers(1,7))
            c=TorusLoop(R,a,m,n); u=float(rng.uniform(0,c.primitive_period))
            with self.subTest(j=j):
                assert_allclose(c.pos(0),c.pos(c.primitive_period),atol=2e-15)
                vr,vt,vz,om,vp=c.speed_components(u,.95)
                self.assertLess(abs((vr*vr+vt*vt+vz*vz)/(.95*C)**2-1),2e-15)
                self.assertTrue(np.isfinite(c.curvature(u)))
                self.assertTrue(np.isfinite(c.torsion(u)) or c.curvature(u)==0)

if __name__=='__main__': unittest.main()
