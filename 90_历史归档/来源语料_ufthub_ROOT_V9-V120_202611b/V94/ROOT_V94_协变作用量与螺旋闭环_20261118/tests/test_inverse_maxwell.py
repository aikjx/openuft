import unittest
import numpy as np
from numpy.testing import assert_allclose
from src.v93_reference import TorusLoop, C,E,ME,EPS0
from src.inverse_maxwell import InverseDrive,lorentz_frame_displacement,uniform_static_B_trajectory

class TestDrive(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.d=InverseDrive()
    def test_invalid_beta(self):
        for b in [-1,0,1,1.2]:
            with self.subTest(beta=b),self.assertRaises(ValueError):InverseDrive(beta=b)
    def test_invalid_charge(self):
        with self.assertRaises(ValueError):InverseDrive(charge=0.)
    def test_invalid_mass(self):
        with self.assertRaises(ValueError):InverseDrive(mass=0.)
    def test_exact_cyclic_position(self):
        d=self.d
        assert_allclose(d.curve_state(0)[0],d.curve_state(d.loop.primitive_period)[0],atol=1e-16)
    def test_exact_cyclic_velocity(self):
        d=self.d
        assert_allclose(d.curve_state(0)[1]/d.v0,d.curve_state(d.loop.primitive_period)[1]/d.v0,atol=1e-14)
    def test_constant_speed(self):
        d=self.d
        for u in np.linspace(0,d.loop.primitive_period,200):
            _,v,a,j=d.curve_state(u)
            self.assertLess(abs(np.linalg.norm(v)/d.v0-1),6e-16)
    def test_orthogonal_accel(self):
        d=self.d
        for u in np.linspace(0,d.loop.primitive_period,100):
            _,v,a,_=d.curve_state(u)
            self.assertLess(abs(np.dot(v,a))/(np.linalg.norm(v)*np.linalg.norm(a)),5e-15)
    def test_jerk_numeric(self):
        d=self.d
        for u in [.11,.42,1.2,2.7]:
            h=1e-5
            a_plus=d.curve_state(u+h)[2];a_minus=d.curve_state(u-h)[2]
            num=(a_plus-a_minus)/(2*h)*d.v0/d.loop.sigma(u)
            j=d.curve_state(u)[3]
            self.assertLess(np.linalg.norm(num-j)/np.linalg.norm(j),1e-8)
    def test_b_dot_numeric(self):
        d=self.d
        for u in [.1,.5,1.8,3.9]:
            h=1e-5
            bplus=d.B_and_dotB(u+h)[0];bminus=d.B_and_dotB(u-h)[0]
            num=(bplus-bminus)/(2*h)*d.v0/d.loop.sigma(u)
            dot=d.B_and_dotB(u)[1]
            self.assertLess(np.linalg.norm(num-dot)/np.linalg.norm(dot),1e-8)
    def test_zero_e_along_path(self):
        d=self.d
        for u in np.linspace(0,d.loop.primitive_period,100):
            r=d.curve_state(u)[0]
            e,_=d.fields(u,r)
            assert_allclose(e,np.zeros(3),atol=1e-8)
    def test_inverse_lorentz_force(self):
        d=self.d
        for u in np.linspace(0,d.loop.primitive_period,151):
            r,v,a,_=d.curve_state(u)
            e,b=d.fields(u,r)
            self.assertLess(np.linalg.norm(d.charge*(e+np.cross(v,b))-d.gamma0*d.mass*a)/
                            np.linalg.norm(d.gamma0*d.mass*a),2e-14)
    def test_B_perpendicular_to_velocity(self):
        d=self.d
        for u in np.linspace(0,d.loop.primitive_period,51):
            _,v,_,_=d.curve_state(u); b,_=d.B_and_dotB(u)
            self.assertLess(abs(np.dot(v,b))/(np.linalg.norm(v)*np.linalg.norm(b)),1e-14)
    def test_B_matches_curvature(self):
        d=self.d
        for u in [0,.4,1.,2.4]:
            b=d.B_and_dotB(u)[0]
            target=d.gamma0*d.mass*d.v0/abs(d.charge)*d.loop.curvature(u)
            self.assertAlmostEqual(np.linalg.norm(b)/target,1,places=13)
    def test_b_field_uniform(self):
        d=self.d
        for u in [.2,1.7]:
            a=d.fields(u,np.array([.03,.04,.05]))[1]
            b=d.fields(u,np.array([-.03,.01,.0]))[1]
            assert_allclose(a,b,atol=0)
    def test_linear_E_field(self):
        d=self.d;u=.29;r=d.curve_state(u)[0]
        h=np.array([.001,-.0004,.002])
        e1=d.fields(u,r+h)[0];e2=d.fields(u,r-h)[0]
        assert_allclose(e1,-e2,atol=1e-8)
    def test_maxwell_faraday_analytic_numeric(self):
        d=self.d;u=.7;x=np.array([.021,-.01,.009]);h=2e-5
        # spatial curl(E), finite difference in physical coordinates
        def ef(z):return d.fields(u,z)[0]
        de=np.zeros((3,3))
        for i in range(3):
            dx=np.zeros(3);dx[i]=h
            de[:,i]=(ef(x+dx)-ef(x-dx))/(2*h)
        curl=np.array([de[2,1]-de[1,2],de[0,2]-de[2,0],de[1,0]-de[0,1]])
        db=d.B_and_dotB(u)[1]
        self.assertLess(np.linalg.norm(curl+db)/np.linalg.norm(db),1e-12)
    def test_maxwell_gauss_e_and_b(self):
        d=self.d;u=.9;x=np.array([.015,.008,-.012]);h=1e-5
        divergence_e=0
        for i in range(3):
            dx=np.zeros(3);dx[i]=h
            divergence_e+=(d.fields(u,x+dx)[0][i]-d.fields(u,x-dx)[0][i])/(2*h)
        self.assertLess(abs(divergence_e),1e-2) # scale: E gradient~Bdot; numeric near exact zero
        self.assertEqual(d.charge_density(u,x),0)
    def test_gauge_potentials_E(self):
        d=self.d;u=1.1; x=np.array([.019,.003,-.009]);h=1e-5;dx=1e-5
        ap=d.potentials(u+h,x)[1];am=d.potentials(u-h,x)[1]
        dtA=(ap-am)/(2*h)*d.v0/d.loop.sigma(u)
        grad=np.zeros(3)
        for k in range(3):
            off=np.zeros(3);off[k]=dx
            grad[k]=(d.potentials(u,x+off)[0]-d.potentials(u,x-off)[0])/(2*dx)
        pred=-dtA-grad; tru=d.fields(u,x)[0]
        self.assertLess(np.linalg.norm(pred-tru)/max(np.linalg.norm(tru),1),1e-8)
    def test_current_source_ampere(self):
        d=self.d;u=.9;x=np.array([.023,.012,.014]);h=2e-4
        ep=d.fields(u+h,x)[0];em=d.fields(u-h,x)[0]
        dtE=(ep-em)/(2*h)*d.v0/d.loop.sigma(u)
        J=d.current_density(u,x,du=h)
        self.assertLess(np.linalg.norm(J+EPS0*dtE)/max(np.linalg.norm(J),1e-30),3e-6)
    def test_testcharge_sign_flip(self):
        d=self.d;alt=InverseDrive(charge=E)
        for u in [.2,2.4]:
            b=d.B_and_dotB(u)[0];bb=alt.B_and_dotB(u)[0]
            assert_allclose(b,-bb,atol=0)
    def test_orbit_numerical_accuracy(self):
        res=self.d.integrated_orbit(samples=151)
        self.assertLess(res['max_scaled_state_error'],5e-9)
    def test_return_map_stability_not_presumed(self):
        # Only verifies a perturbation does not coincide with the exact reference;
        # full Floquet audit is performed in generate_results.py
        d=self.d
        pt=np.array([1e-6,0,0,0,0,0])
        res=d.integrated_orbit(perturb=pt,samples=15)
        self.assertGreater(np.linalg.norm(res['final_scaled_state']-res['reference'][-1]),2e-7)
    def test_beta_scaling_B_nonzero(self):
        d1=InverseDrive(beta=.5);d2=InverseDrive(beta=.8)
        u=.7
        b1=np.linalg.norm(d1.B_and_dotB(u)[0]);b2=np.linalg.norm(d2.B_and_dotB(u)[0])
        expected=(d2.gamma0*d2.v0)/(d1.gamma0*d1.v0)
        self.assertAlmostEqual(b2/b1,expected,places=12)
    def test_period_and_no_closed_spacetime(self):
        d=self.d
        delta=lorentz_frame_displacement(d.period,.3)
        self.assertGreater(delta['delta_t_prime_s'],d.period)
        self.assertNotEqual(delta['delta_x_prime_m'],0)
    def test_zero_boost_no_spatial_shift(self):
        delta=lorentz_frame_displacement(self.d.period,0)
        self.assertEqual(delta['delta_x_prime_m'],0)
    def test_invalid_boost(self):
        with self.assertRaises(ValueError):lorentz_frame_displacement(self.d.period,1.0)
    def test_static_B_circular(self):
        t=np.linspace(0,1e-9,21)
        pos=uniform_static_B_trajectory(1e8,0,.5,t=t)
        self.assertLess(abs(pos[-1,2]),1e-15)
        self.assertGreater(np.max(np.linalg.norm(pos,axis=1)),0)
    def test_static_B_helical_not_closed(self):
        t=np.linspace(0,1e-9,21)
        pos=uniform_static_B_trajectory(1e8,1e8,.5,t=t)
        assert_allclose(pos[:,2],t*1e8,rtol=1e-15)
    def test_static_B_zero_field_straight(self):
        t=np.linspace(0,1e-9,21)
        pos=uniform_static_B_trajectory(1e8,1e7,0,t=t)
        assert_allclose(pos[:,0],1e8*t)
    def test_torus_knot_curvature_varies(self):
        d=self.d
        vals=d.loop.curvature(np.linspace(0,d.loop.primitive_period,100))
        self.assertGreater(np.max(vals)/np.min(vals),1.5)
    def test_nonuniform_b_drive(self):
        d=self.d
        us=np.linspace(0,d.loop.primitive_period,100)
        b=np.array([d.B_and_dotB(u)[0] for u in us])
        self.assertGreater(np.std(np.linalg.norm(b,axis=1)),.01)
    def test_source_energy_not_finite(self):
        # For nonzero dB/dt, E grows linearly with distance from curve.
        d=self.d;u=.33;r=d.curve_state(u)[0]
        a=np.array([1.,.4,-.3])
        e1=np.linalg.norm(d.fields(u,r+a)[0]);e2=np.linalg.norm(d.fields(u,r+2*a)[0])
        self.assertAlmostEqual(e2/e1,2,places=12)
    def test_local_current_continuity(self):
        # rho=0 and J divergence=0 due to affine curl-free structure of J.
        d=self.d;u=.4;x=np.array([.01,.03,.012]);h=1e-5
        div=0
        for k in range(3):
            dx=np.zeros(3);dx[k]=h
            div+=(d.current_density(u,x+dx)[k]-d.current_density(u,x-dx)[k])/(2*h)
        self.assertLess(abs(div),1e-7)
    def test_radiated_energy_nonzero(self):
        e=self.d.loop.classical_radiated_energy_one_lap(beta=self.d.beta)
        self.assertGreater(e,0)

class RandomPhysicsTests(unittest.TestCase):
    def test_inverse_drive_random_geometry(self):
        rng=np.random.default_rng(94)
        for _ in range(90):
            R=float(rng.uniform(.002,.03));a=float(R*rng.uniform(.05,.7))
            m=int(rng.integers(1,6));n=int(rng.integers(1,6))
            b=float(rng.uniform(.05,.95));charge=-E if rng.random()<.5 else E
            dr=InverseDrive(TorusLoop(R,a,m,n),b,ME,charge)
            u=float(rng.uniform(0,dr.loop.primitive_period))
            r,v,a,j=dr.curve_state(u)
            B,db=dr.B_and_dotB(u)
            residual=np.linalg.norm(charge*np.cross(v,B)-dr.gamma0*ME*a)
            self.assertLess(residual/max(np.linalg.norm(dr.gamma0*ME*a),1e-50),4e-14)
            self.assertLess(abs(np.dot(v,a)/(np.linalg.norm(v)*np.linalg.norm(a))),2e-13)

if __name__=='__main__':unittest.main()

class InverseNonUniquenessTests(unittest.TestCase):
    def test_longitudinal_B_not_identifiable_from_trajectory(self):
        d=InverseDrive(); u=.73
        x,v,a,_=d.curve_state(u)
        Ef,B=d.fields(u,x)
        for lam in [-1e-9,1e-9,2e-8]:
            Bnew=B+lam*v
            force=d.charge*np.cross(v,Bnew)
            self.assertLess(np.linalg.norm(force-d.gamma0*d.mass*a)/np.linalg.norm(d.gamma0*d.mass*a),2e-14)
    def test_minimal_field_perpendicular(self):
        d=InverseDrive(); u=1.9
        v=d.curve_state(u)[1];b=d.B_and_dotB(u)[0]
        for lam in [-1e-9,1e-9]:
            self.assertGreater(np.linalg.norm(b+lam*v),np.linalg.norm(b))
    def test_cannot_apply_massive_action_to_zero_mass(self):
        with self.assertRaises(ValueError):InverseDrive(mass=0.0)
    def test_source_field_energy_cannot_be_globally_finite(self):
        d=InverseDrive(); b=d.B_and_dotB(.5)[0]
        self.assertGreater(np.linalg.norm(b),0)
        # uniform nonzero magnetic-energy density integrated over ever larger balls ~ radius^3
        volume=lambda radius:4*np.pi*radius**3/3
        e_density=np.dot(b,b)/(2*1.25663706127e-6)
        self.assertAlmostEqual(e_density*volume(2)/ (e_density*volume(1)),8,places=12)
