import math,random,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import *

class TestHelix(unittest.TestCase):
    def setUp(self):self.h=LightHelix.from_curvature_torsion(.6,.8)
    def test_forward(self):
        self.assertAlmostEqual(self.h.radius,.6);self.assertAlmostEqual(self.h.omega,1.)
        self.assertAlmostEqual(self.h.axial,.8);self.assertAlmostEqual(self.h.pitch,2*math.pi*.8)
    def test_curvature(self):self.assertAlmostEqual(self.h.curvature,.6)
    def test_torsion(self):self.assertAlmostEqual(self.h.torsion,.8)
    def test_frequency(self):self.assertAlmostEqual(self.h.frequency,1/(2*math.pi))
    def test_darboux_axis(self):
        for t in [-1.,0.,2.,100.]:
            v=self.h.darboux(t)
            self.assertAlmostEqual(v[0],0,places=11);self.assertAlmostEqual(v[1],0,places=11)
            self.assertAlmostEqual(v[2],self.h.omega)
    def test_frenet_orthogonality(self):
        for t in [0,.3,.9,2,4.]:
            T,N,B=self.h.frame(t)
            for x in (T,N,B):self.assertAlmostEqual(norm(x),1)
            for x,y in [(T,N),(T,B),(N,B)]:self.assertAlmostEqual(dot(x,y),0)
    def test_force_zero_power(self):
        for t in [0,.123,1.2,8.]: self.assertAlmostEqual(dot(self.h.transverse_force(t,10),self.h.velocity(t)),0,places=12)
    def test_force_scale(self):self.assertAlmostEqual(norm(self.h.transverse_force(.31,2.5)),1.5)
    def test_speed_null(self):
        for t in [-3,0,2.]:self.assertAlmostEqual(norm(self.h.velocity(t)),1)
    def test_nonzero_acceleration(self):self.assertAlmostEqual(norm(self.h.acceleration(1)),.6)
    def test_reconstruction_all_quadrants(self):
        for k in [1e-5,.02,.1,.6,12,1000]:
            for tau in [-100,-.8,0,.8,100]:
                x=LightHelix.from_curvature_torsion(k,tau)
                self.assertAlmostEqual(x.curvature,k,delta=1e-10*max(1,k))
                self.assertAlmostEqual(x.torsion,tau,delta=1e-10*max(1,abs(tau)))
                self.assertAlmostEqual(x.transverse**2+x.axial**2,1,places=12)
    def test_invalid_parameters(self):
        for args in [(0,1,0),(-1,1,0),(.5,1,.8),(.5,-1,0),(.5,1,float('nan'))]:
            with self.assertRaises(ValueError):LightHelix(*args)
        for k,t in [(0,1),(-1,0),(float('nan'),1)]:
            with self.assertRaises(ValueError): LightHelix.from_curvature_torsion(k,t)
    def test_boosts(self):
        for beta in [-.99,-.8,-.3,0.,.3,.8,.99]:
            b,D=self.h.boost_along_axis(beta)
            self.assertAlmostEqual(norm(b.velocity(1.)),1,places=11)
            self.assertAlmostEqual(self.h.omega/b.omega,D,places=11)
            self.assertAlmostEqual(D*b.omega,self.h.omega)
            self.assertAlmostEqual((D*self.h.omega)*(b.omega/self.h.omega),D*b.omega)
    def test_boost_reverse(self):
        for beta in [-.9,-.5,.1,.6,.9]:
            b,D=self.h.boost_along_axis(beta)
            c,_=b.boost_along_axis(-beta)
            self.assertAlmostEqual(c.radius,self.h.radius)
            self.assertAlmostEqual(c.omega,self.h.omega,places=10)
            self.assertAlmostEqual(c.axial,self.h.axial,places=10)
    def test_boost_finite(self):
        for beta in [-1,1,float('nan')]:
            with self.assertRaises(ValueError):self.h.boost_along_axis(beta)

class TestBerry(unittest.TestCase):
    def test_curvature_from_connection(self):
        for theta in [.1,.3,1.,2.,2.9]:
            h=1e-5
            numerical=(berry_connection_theta_phi(theta+h)-berry_connection_theta_phi(theta-h))/(2*h)
            self.assertAlmostEqual(numerical,berry_curvature_theta_phi(theta),delta=1e-10)
    def test_curvature_from_orientation(self):
        for winding in [-3,-1,0,1,2,3]:
            for theta in [.1,.7,1.2,2.5]:
                for phi in [0.,.12,1.8]:
                    self.assertAlmostEqual(berry_curvature_theta_phi(theta,winding),berry_curvature_via_n(theta,phi,winding),places=12)
    def test_flux_chern_quantization(self):
        for winding in [-3,-2,-1,0,1,2,3]:
            self.assertAlmostEqual(berry_flux_analytic(winding)/(2*math.pi),winding)
            self.assertAlmostEqual(berry_flux_midpoint(600,12,winding),berry_flux_analytic(winding),delta=.00005)
    def test_orientation_unit_norm(self):
        for theta in [.1,math.pi/3,math.pi-0.2]:
            for phi in [0,.5,3,6]:self.assertAlmostEqual(norm(orientation(theta,phi)),1)
    def test_winding_changes_flux(self):
        self.assertAlmostEqual(berry_flux_analytic(2),2*berry_flux_analytic(1))
    def test_same_phase_uniform_n_no_field(self):
        # only phase varies: dtheta=0 implies f=0 everywhere
        F=spacetime_berry_field(math.pi/2,[0,0,0,0],[1,3,4,5])
        self.assertTrue(all(abs(x)<1e-14 for row in F for x in row))
    def test_transverse_texture_generates_field(self):
        F=spacetime_berry_field(math.pi/4,[0,.25,0,0],[2,0,0,0])
        self.assertAlmostEqual(F[1][0],math.sin(math.pi/4)/4)
        self.assertAlmostEqual(F[0][1],-math.sin(math.pi/4)/4)
    def test_antisymmetric(self):
        rng=random.Random(123)
        for _ in range(30):
            theta=rng.uniform(0,math.pi)
            t=[rng.uniform(-3,3) for _ in range(4)]
            p=[rng.uniform(-3,3) for _ in range(4)]
            F=spacetime_berry_field(theta,t,p)
            for i in range(4):
                self.assertAlmostEqual(F[i][i],0)
                for j in range(4):self.assertAlmostEqual(F[i][j],-F[j][i])
    def test_parallel_gradients_zero(self):
        F=spacetime_berry_field(1.,[2,3,5,7],[4,6,10,14]);self.assertTrue(all(abs(x)<1e-14 for row in F for x in row))
    def test_simple_field_zero_pfaffian(self):
        rng=random.Random(725)
        for _ in range(150):
            theta=rng.uniform(0,math.pi)
            t=[rng.uniform(-2,2) for _ in range(4)]
            p=[rng.uniform(-2,2) for _ in range(4)]
            F=spacetime_berry_field(theta,t,p)
            self.assertAlmostEqual(pfaffian4(F),0,delta=1e-12)
    def test_generic_em_nonzero_pfaffian(self):
        # Constant E_x and B_x field in flat space provides a valid local Maxwell solution.
        F=[[0.,1.,0.,0.],[-1.,0.,0.,0.],[0.,0.,0.,1.],[0.,0.,-1.,0.]]
        self.assertAlmostEqual(pfaffian4(F),1.)
        with self.assertRaises(ValueError):pfaffian4([[0]])
    def test_two_orientation_fields_can_have_nonzero_pfaffian(self):
        # Separate textures F01 and F23: each simple, but the sum has rank 4.
        F1=spacetime_berry_field(math.pi/2,[1,0,0,0],[0,2,0,0])
        F2=spacetime_berry_field(math.pi/2,[0,0,1,0],[0,0,0,2])
        self.assertAlmostEqual(pfaffian4(F1),0)
        self.assertAlmostEqual(pfaffian4(F2),0)
        self.assertAlmostEqual(pfaffian4(sum_two_forms(F1,F2)),1)
    def test_grad_length_mismatch(self):
        with self.assertRaises(ValueError):spacetime_berry_field(1.,[1],[1,2])
    def test_flux_quadrature_invalid(self):
        with self.assertRaises(ValueError):berry_flux_midpoint(1,100)

class TestGauge(unittest.TestCase):
    def test_pure_gauge_zero_B(self): self.assertEqual(stueckelberg_B([3,-4],[3,-4]),(0,0))
    def test_gauge_covariance_B(self):
        theta=(1.,-2.,.5,3.)
        A=(-1.,2.,-3.,4.)
        chi=(5.,6.,7.,8.)
        tt,AA=stueckelberg_gauge_transform(theta,A,chi)
        self.assertEqual(stueckelberg_B(theta,A),stueckelberg_B(tt,AA))
    def test_non_pure_phase_B(self):self.assertEqual(stueckelberg_B([1,0],[0,0]),(1,0))
    def test_gauge_unequal(self):
        with self.assertRaises(ValueError):stueckelberg_B([1,2],[1])
        with self.assertRaises(ValueError):stueckelberg_gauge_transform([1],[2],[3,4])
    def test_mass_zero(self):
        self.assertEqual(vector_inverse_length_mass(0,3),0)
        self.assertEqual(vector_inverse_length_mass(2,0),0)
    def test_mass_gap(self):self.assertAlmostEqual(vector_inverse_length_mass(.2,3),.6)
    def test_dispersion(self):self.assertAlmostEqual(relative_dispersion(2,.2,3),math.sqrt(4+.36))
    def test_massless_wave(self):self.assertEqual(relative_dispersion(2,0,3),2)
    def test_massive_wave(self):self.assertGreater(relative_dispersion(2,.2,3),2)

if __name__=='__main__':unittest.main()
