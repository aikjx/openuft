import unittest, math, pathlib, sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from root_v151.core import *
from root_v151.core import electromagnetic_invariants, photon_dof_count

class TestWave(unittest.TestCase):
    def test_invalid_wave_params(self):
        for args in [(0,1,1),(1,0,1),(1,1,0),(1,1,2)]:
            with self.subTest(args=args),self.assertRaises(ValueError): plane_wave(*args)
    def test_invalid_boost(self):
        for beta in (-1,1,1.5):
            with self.subTest(beta=beta),self.assertRaises(ValueError): plane_wave().boost_z(beta)
    def test_dof(self):
        self.assertEqual(photon_dof_count(),2)
    def test_pure_gradient_symmetric(self):
        h=np.array([[1,2,3,4],[2,8,5,6],[3,5,7,9],[4,6,9,12]],dtype=float)
        np.testing.assert_array_equal(pure_phase_field_strength(h),np.zeros((4,4)))
    def test_bad_nonsmooth_hessian(self):
        h=np.eye(4);h[0,1]=7
        self.assertGreater(np.linalg.norm(pure_phase_field_strength(h)),0)
    def test_bad_hessian_shape(self):
        with self.assertRaises(ValueError):pure_phase_field_strength(np.eye(3))
    def test_parallel_fields_exist(self):
        E=np.array([0.,0.,2.]);B=np.array([0.,0.,3.]);I1,I2=electromagnetic_invariants(E,B)
        self.assertEqual(I1,10.); self.assertEqual(I2,-24.)
    def test_null_field_invariants(self):
        E,B=plane_wave().fields(.3,.7)
        I1,I2=electromagnetic_invariants(E,B)
        self.assertAlmostEqual(I1,0.0,places=14);self.assertAlmostEqual(I2,0.0,places=14)
    def test_field_strength_zero_does_not_imply_theta_constant(self):
        h=np.diag([1.,2.,3.,4.]);np.testing.assert_array_equal(pure_phase_field_strength(h),np.zeros((4,4)))
    def test_boost_frequency_energy_same_factor(self):
        w=plane_wave(3.1,2.0,1)
        for beta in (-.8,-.4,0,.2,.7):
            wprime,D=w.boost_z(beta)
            self.assertAlmostEqual(wprime.omega/w.omega,D,places=13)
            self.assertAlmostEqual(wprime.amp/w.amp,D,places=13)
            self.assertEqual(wprime.sigma,w.sigma)
    def test_handedness_under_boost(self):
        for sigma in (-1,1):
            w=plane_wave(1.1,.8,sigma)
            self.assertEqual(w.boost_z(.56)[0].sigma,sigma)

def add_wave_case(j,sigma,t,z,omega,amp):
    def test(self):
        wave=plane_wave(omega,amp,sigma)
        E,B=wave.fields(t,z)
        res=wave.maxwell_residuals(t,z)
        np.testing.assert_allclose(res['faraday'],np.zeros(3),rtol=0,atol=2e-13)
        np.testing.assert_allclose(res['ampere'],np.zeros(3),rtol=0,atol=2e-13)
        self.assertEqual(res['divE'],0);self.assertEqual(res['divB'],0)
        self.assertLess(abs(float(E@B)),1e-12)
        self.assertLess(abs(float(E@E-B@B)),1e-12)
        self.assertAlmostEqual(float(np.cross(E,B)[2]),amp*amp,delta=1e-12)
        np.testing.assert_allclose(np.cross(np.array([0.,0.,1.]),E),B,atol=1e-12)
    setattr(TestWave,f'test_wave_{j:02d}',test)

cases=[]
for sigma in (-1,1):
    for t,z,w,A in [(.1,.2,1.,1.),(.3,-1.,2.,.5),(.9,1.23,5.,2.),(-2.,.23,1.7,.8),(.8,-.8,3.6,1.3),(1.9,.4,.5,3.)]:
        cases.append((sigma,t,z,w,A))
for i,case in enumerate(cases):add_wave_case(i,*case)

class TestHelix(unittest.TestCase):
    def test_helix_null_geometry(self):
        v=helix_data(.6,1.,.8)
        self.assertAlmostEqual(v['v'],1.)
        self.assertAlmostEqual(v['curvature'],.6)
        self.assertAlmostEqual(v['torsion'],.8)
        self.assertAlmostEqual(v['curvature']**2+v['torsion']**2,1.)
    def test_invalid_speed(self):
        with self.assertRaises(ValueError):helix_data(.8,1.,.8)
    def test_invalid_radius(self):
        with self.assertRaises(ValueError):helix_data(0.,1.,.5)
    def test_spatial_curve_noninvariant_fraction(self):
        v=helix_data(.6,1.,.8)
        self.assertAlmostEqual(v['geometric_fraction'],.36)
        # axial boost beta=u implies u'=0 and a'=a, omega'=1/a,
        # thus fraction'=1; a frame-dependent ratio can't predict alpha.
        boosted=helix_data(.6,1/.6,0.)
        self.assertAlmostEqual(boosted['geometric_fraction'],1.)
    def test_alpha_fit_is_free_parameter(self):
        alpha=photon_alpha_reference()
        a=math.sqrt(alpha);u=math.sqrt(1-alpha)
        h=helix_data(a,1.,u)
        self.assertAlmostEqual(h['geometric_fraction'],alpha,places=14)
        self.assertNotAlmostEqual(h['geometric_fraction'],1.,places=2)
    def test_helix_torsion_sign(self):
        a=helix_data(.4,1.,.8);b=helix_data(.4,1.,-.8)
        self.assertEqual(a['curvature'],b['curvature'])
        self.assertEqual(a['torsion'],-b['torsion'])

if __name__=='__main__':unittest.main()
