import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from root_v90 import *

class BasicTests(unittest.TestCase):
    def test_v89_newton(self):
        p=interaction_phases(Geometry())
        self.assertAlmostEqual(p['newton'],-0.0692394597353851,places=12)
    def test_v89_eft(self):
        p=eft_phase_components(Geometry(),1e-14,1e-14,1)
        self.assertAlmostEqual(p['1pn_potential_convention'] / (-2.39424850793579e-38),1,places=10)
        self.assertAlmostEqual(p['eft_one_loop_potential_convention'] / (-9.85910115880269e-64),1,places=10)
    def test_v89_concurrence(self):
        self.assertAlmostEqual(pure_concurrence(interaction_phases(Geometry())['newton']),0.03461281484279,places=12)
    def test_illegal_distances(self):
        with self.assertRaises(ValueError):Geometry(0.2e-3,0.2e-3,0.2e-3).distances()
    def test_negative_lambda(self):
        with self.assertRaises(ValueError):yukawa_kernel(Geometry(),-1)
    def test_symmetric_branch_zero(self):
        self.assertEqual(power_kernel(Geometry(0.45e-3,0,0.2e-3)),0)
    def test_yukawa_branch_zero(self):
        self.assertAlmostEqual(yukawa_kernel(Geometry(0.45e-3,0,0.2e-3),1e-3),0,places=11)
    def test_small_lambda_sign(self):
        self.assertLess(yukawa_kernel(Geometry(),0.0001),0)
    def test_yukawa_mixed_curvature(self):
        g=Geometry()
        n=mixed_curvature_integral(g,lambda r:yukawa_curvature(r,.0005))
        self.assertAlmostEqual(n/yukawa_kernel(g,.0005),1,places=11)
    def test_newton_mixed_curvature(self):
        g=Geometry()
        n=mixed_curvature_integral(g,lambda r:2/r**3)
        self.assertAlmostEqual(n/power_kernel(g),1,places=11)
    def test_nulled_newton(self):
        g1=Geometry();g2=Geometry(600e-6,200e-6,200e-6)
        w=newton_nulled_weights(g1,g2)
        self.assertAlmostEqual(w@np.array([power_kernel(g1),power_kernel(g2)]),0.,places=10)
    def test_nulled_yukawa_nonzero(self):
        g1=Geometry();g2=Geometry(600e-6,200e-6,200e-6)
        self.assertNotEqual(newton_nulled_signal(g1,g2,1e-3,1),0)
    def test_parity_exact(self):
        ev,od=charge_parity_projector([2.5,1.5],[1.5,2.5])
        np.testing.assert_allclose(ev,[2,2]); np.testing.assert_allclose(od,[.5,-.5])
    def test_concurrence_parity_invalid(self):
        gd,ed=.4,1.
        got=(pure_concurrence(gd+ed)+pure_concurrence(gd-ed))/2
        self.assertGreater(abs(got-pure_concurrence(gd)),.01)
    def test_coulomb_equal_strength(self):
        eq=residual_charge_equivalent(1e-14,1e-14)
        self.assertAlmostEqual(K_E*eq*eq/(G*1e-28),1,places=12)
    def test_nonoverlap(self):
        g=Geometry();r=sphere_radius(1e-14,3500);g.require_spheres_nonoverlap(r,r)
    def test_sphere_too_large(self):
        with self.assertRaises(ValueError): Geometry().require_spheres_nonoverlap(.0002,.0002)
    def test_sphere_formfactor_small(self):
        self.assertAlmostEqual(sphere_yukawa_form_factor(0),1,places=14)
        self.assertGreater(sphere_yukawa_form_factor(.01),1)
    def test_design_shape(self):
        self.assertEqual(design_matrix([450e-6,600e-6,850e-6],200e-6,200e-6,1e-3).shape,(3,2))
    def test_design_nonzero(self):
        self.assertEqual(np.linalg.matrix_rank(design_matrix([450e-6,600e-6,850e-6],200e-6,200e-6,1e-3)),2)
    def test_same_kernel_rank_one(self):
        f=np.array([power_kernel(Geometry(d,200e-6,200e-6)) for d in [450e-6,600e-6,850e-6]])
        self.assertEqual(np.linalg.matrix_rank(np.column_stack((f,-f))),1)
    def test_synthetic_noise_free_even(self):
        s=synthetic_parity_observations([450e-6,600e-6,850e-6],200e-6,200e-6,1e-3,0.1,.2)
        np.testing.assert_allclose(s['even'],s['even_true'],rtol=1e-14,atol=1e-15)
        np.testing.assert_allclose(s['odd'],s['electric_true'],rtol=1e-14,atol=1e-15)
    def test_yukawa_curvature_positive(self):
        self.assertGreater(yukawa_curvature(1e-3,1e-3),0)
    def test_no_physical_electrical_switching_assumption(self):
        self.assertGreater(K_E*E*E/(G*1e-28),1e9)
    def test_three_distance_null_F1_F2_not_F3(self):
        ds=[450e-6,600e-6,850e-6]
        gs=[Geometry(d) for d in ds]
        f=np.array([[power_kernel(g,n) for n in (1,2,3)] for g in gs])
        a,b,c=f.T
        w=np.cross(a/np.linalg.norm(a),b/np.linalg.norm(b))
        self.assertLess(abs(np.dot(w,a)),1e-10)
        self.assertLess(abs(np.dot(w,b)),1e-5)
        self.assertGreater(abs(np.dot(w,c)),1e-8)
    def test_newton_null_alpha_zero(self):
        self.assertEqual(newton_nulled_signal(Geometry(),Geometry(.0006),.0003,alpha=0),0)
    def test_long_range_condition_deteriorates(self):
        d=[450e-6,600e-6,850e-6,1250e-6]
        n1=identifiability(d,200e-6,200e-6,.001)['condition_number']
        n2=identifiability(d,200e-6,200e-6,.01)['condition_number']
        self.assertGreater(n2,50*n1)
    def test_yukawa_analytic_limit_coeff(self):
        g=Geometry()
        lam=10.
        c=(yukawa_delta_series(g,lam)*lam**3)/(g.s_a*g.s_b)
        self.assertAlmostEqual(c,1/3,places=4)
    def test_charged_classical_phase_sign(self):
        g=Geometry()
        p=interaction_phases(g,q_a=E,q_b=E)
        self.assertGreater(p['coulomb'],0)
    def test_local_yukawa_formfactor(self):
        self.assertAlmostEqual(sphere_yukawa_form_factor(.1),1.001000357,places=6)

# Parameterized cases are registered as actual individual tests (not inflated subTests).
def add_generated_tests():
    for idx, d in enumerate([.45,.50,.55,.60,.70,.85,1.,1.2],start=1):
        def test_kernel(self, d=d):
            g=Geometry(d*1e-3,150e-6,120e-6)
            for lam in [.1,.3,.8,1.5]:
                l=lam*1e-3
                self.assertAlmostEqual(yukawa_kernel(g,l)/yukawa_kernel_naive(g,l),1,places=9)
        setattr(BasicTests,f'test_kernel_scan_{idx:02d}',test_kernel)
    for idx, lam in enumerate([.004,.007,.01,.02,.05,.1,.4,1,10],start=1):
        def test_stable_series(self, lam=lam):
            g=Geometry()
            exact=yukawa_delta_series(g,lam)
            approx=leading_delta(g,lam)
            # leading order + first correction: relative remainder O((maxr/lambda)^2)
            self.assertLess(abs((exact-approx)/exact),.01)
        setattr(BasicTests,f'test_asymptotic_scan_{idx:02d}',test_stable_series)
    for idx,(a,b) in enumerate([(50,50),(50,100),(150,200),(200,200),(120,240),(30,190)],start=1):
        def test_mixed_sign(self,a=a,b=b):
            g=Geometry(.6e-3,a*1e-6,b*1e-6)
            self.assertLess(power_kernel(g),0)
            self.assertLess(yukawa_kernel(g,1e-3),0)
        setattr(BasicTests,f'test_mixed_sign_{idx:02d}',test_mixed_sign)
    for idx, density in enumerate([1000,2000,3500,5000,8000,15000],start=1):
        def test_sphere(self,density=density):
            r=sphere_radius(1e-14,density)
            self.assertGreater(r,0)
            self.assertAlmostEqual(4/3*math.pi*r**3*density/1e-14,1,places=12)
        setattr(BasicTests,f'test_sphere_density_{idx:02d}',test_sphere)
    for idx,lam in enumerate([.5e-3,.75e-3,1.25e-3,2e-3,5e-3,1e-2],start=1):
        def test_lambda_derivative(self,lam=lam):
            g=Geometry()
            step=lam*1e-4
            numerical=(yukawa_kernel(g,lam+step)-yukawa_kernel(g,lam-step))/(2*step)
            analytic=yukawa_kernel_derivative_lambda(g,lam)
            self.assertAlmostEqual(numerical/analytic,1,places=6)
        setattr(BasicTests,f'test_derivative_{idx:02d}',test_lambda_derivative)
add_generated_tests()

if __name__=='__main__':unittest.main(verbosity=2)
