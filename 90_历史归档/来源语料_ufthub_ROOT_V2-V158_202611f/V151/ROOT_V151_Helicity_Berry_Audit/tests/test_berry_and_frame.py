import unittest, sys, pathlib, math
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from root_v151.core import *
from root_v151.core import helicity_eigen_residual

class TestFrame(unittest.TestCase):
    def test_invalid_sigma(self):
        with self.assertRaises(ValueError): circular_basis(0.4,0.8,0)
    def test_invalid_connection_sigma(self):
        with self.assertRaises(ValueError): berry_connection(0.4,0)
    def test_alpha_is_reference_not_predicted(self):
        self.assertAlmostEqual(photon_alpha_reference(),0.0072973525643,places=15)
    def test_gauge_shift(self):
        for s in (-1,1):
            a=berry_connection(0.67,s)[1]
            self.assertAlmostEqual(berry_connection(0.67,s,dchi_dphi=3.25)[1]-a,3.25)
    def test_curvature_from_connection_finite_difference(self):
        for t in (.3,.79,1.7,2.8):
            for sigma in (-1,1):
                h=1e-5
                num=(berry_connection(t+h,sigma)[1]-berry_connection(t-h,sigma)[1])/(2*h)
                self.assertAlmostEqual(num,berry_curvature_theta(t,sigma),delta=1e-10)
    def test_chern_opposite_polarizations(self):
        self.assertAlmostEqual(chern_number_numeric(12,1)+chern_number_numeric(12,-1),0.0,places=12)
    def test_chern_momentum_vs_spacetime(self):
        # This numerical result is defined on sphere of directions, not a spacetime field.
        self.assertEqual(round(chern_number_numeric(10,1)),2)
    def test_k_monopole_invalid(self):
        with self.assertRaises(ValueError): berry_curvature_k([0,0,0],1)
    def test_k_invalid_dimension(self):
        with self.assertRaises(ValueError): berry_curvature_k([1,2],1)
    def test_k_invalid_sigma(self):
        with self.assertRaises(ValueError): berry_curvature_k([1,2,3],0)
    def test_solid_angle_phase_pi(self):
        self.assertAlmostEqual(cap_phase(math.pi/3,1),math.pi,places=12)
    def test_phase_opposite_sign(self):
        self.assertAlmostEqual(cap_phase(0.8,1)+cap_phase(0.8,-1),0.0,places=12)
    def test_circular_basis_conjugacy(self):
        self.assertTrue(np.allclose(circular_basis(.85,1.2,-1),np.conj(circular_basis(.85,1.2,1))))

def add_frame_test(j,t,p):
    def test(self):
        n,et,ep=sph_frame(t,p)
        arr=np.column_stack((n,et,ep))
        np.testing.assert_allclose(arr.T@arr,np.eye(3),rtol=0,atol=3e-15)
        self.assertAlmostEqual(float(np.linalg.det(arr)),1.0,places=13)
        for sigma in (-1,1):
            eps=circular_basis(t,p,sigma)
            self.assertAlmostEqual(float(np.vdot(eps,eps).real),1.0,places=13)
            self.assertAlmostEqual(float(np.abs(n@eps)),0.0,places=13)
            self.assertLess(helicity_eigen_residual(t,p,sigma),1e-13)
    setattr(TestFrame,f'test_sample_frame_{j:02d}',test)

for j,(theta,phi) in enumerate([(0.14,0.01),(.24,.21),(.42,.71),(.57,1.3),(.86,2.2),(1.13,.33),(1.41,4.8),(1.88,3.8),(2.03,5.5),(2.35,1.1),(2.78,3.1),(3.0,5.1)]):
    add_frame_test(j,theta,phi)

class TestFlux(unittest.TestCase):
    def test_cap_boundary_zero(self):
        self.assertAlmostEqual(cap_phase(0,1),0.0)
    def test_cap_full_sphere(self):
        self.assertAlmostEqual(cap_phase(math.pi,1),4*math.pi)
    def test_curvature_at_poles(self):
        self.assertAlmostEqual(berry_curvature_theta(0),0)
        self.assertAlmostEqual(berry_curvature_theta(math.pi),0,places=14)
    def test_k_curvature_radial(self):
        kval=np.array([1.,2.,3.]); f=berry_curvature_k(kval)
        np.testing.assert_allclose(np.cross(kval,f),[0,0,0],atol=2e-16)
    def test_k_curvature_inverse_square(self):
        k=np.array([2.,3.,4.]); r=np.linalg.norm(k)
        self.assertAlmostEqual(np.linalg.norm(berry_curvature_k(k)),1/r**2,places=14)
    def test_k_scale(self):
        k=np.array([.4,1.,2.]);f1=berry_curvature_k(k)
        np.testing.assert_allclose(berry_curvature_k(3*k),f1/9,rtol=2e-15)

def add_chern_test(j,points,sign):
    def test(self):
        self.assertAlmostEqual(chern_number_numeric(points,sign),2*sign,delta=2e-13)
        self.assertAlmostEqual(berry_flux_numeric(points,sign),4*math.pi*sign,delta=2e-12)
    setattr(TestFlux,f'test_chern_quad_{j:02d}',test)
for j,(n,s) in enumerate([(n,s) for n in (3,5,8,12,18,32,48) for s in (-1,1)]):
    add_chern_test(j,n,s)

if __name__=='__main__':unittest.main()
