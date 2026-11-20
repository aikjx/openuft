import unittest, math
import numpy as np
from src.geometry import X,Y,Z,matrix_curvature_two_phase,matrix_holonomy,phase_only_curvature,su2_holonomy_small_loop_error,connection_holonomy_eigenphases

class TestGeometry(unittest.TestCase):
    def test_01_generators_antihermitian(self):
        for a in [X,Y,Z]:np.testing.assert_allclose(a.conj().T,-a,atol=1e-16)
    def test_02_generators_traceless(self):
        for a in [X,Y,Z]: self.assertAlmostEqual(abs(np.trace(a)),0)
    def test_03_su2_commutator(self): np.testing.assert_allclose(X@Y-Y@X,Z)
    def test_04_nonzero_curvature(self): self.assertGreater(np.linalg.norm(matrix_curvature_two_phase(.01)),0)
    def test_05_inverse_square(self):
        np.testing.assert_allclose(matrix_curvature_two_phase(1),4*matrix_curvature_two_phase(2))
    def test_06_l_positive(self):
        with self.assertRaises(ValueError): matrix_curvature_two_phase(0)
    def test_07_su2_trace_curvature(self): self.assertAlmostEqual(abs(np.trace(matrix_curvature_two_phase(.2))),0)
    def test_08_small_loop_unitary(self):
        w=matrix_holonomy(.1,.2)
        np.testing.assert_allclose(w.conj().T@w,np.eye(2),atol=1e-14)
    def test_09_small_loop_det(self):self.assertAlmostEqual(np.linalg.det(matrix_holonomy(.1,.2)).real,1,places=12)
    def test_10_zero_area(self):np.testing.assert_allclose(matrix_holonomy(.1,0),np.eye(2),atol=1e-15)
    def test_11_small_loop_convergence(self):
        e1=su2_holonomy_small_loop_error(.01);e2=su2_holonomy_small_loop_error(.005)
        self.assertTrue(6.5 < e1/e2 < 9.5,(e1,e2))
    def test_12_single_phase_random(self):
        rng=np.random.default_rng(1)
        for _ in range(100):
            M=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            dM=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            a,b,c=rng.normal(size=3)
            val=phase_only_curvature(a,b,c,c,M,dM)
            self.assertLess(np.max(np.abs(val)),1e-12)
    def test_13_single_phase_cross_partial(self):
        val=phase_only_curvature(.2,.3,.4,.41,X,Y)
        np.testing.assert_allclose(val,-.01*X,atol=1e-13)
    def test_14_flat_holonomy_not_identity(self):
        vals=connection_holonomy_eigenphases(2*math.pi)
        self.assertTrue(np.allclose(vals,[-1,-1],atol=1e-14))
    def test_15_zero_loop_holonomy(self):
        self.assertTrue(np.allclose(connection_holonomy_eigenphases(0),[1,1]))
    def test_16_loop_order_matters(self):
        self.assertGreater(np.linalg.norm(matrix_holonomy(.25,.3)-np.eye(2)),1e-4)
    def test_17_const_generator_flat(self):
        self.assertTrue(np.allclose(phase_only_curvature(.1,.5,0,0,X,np.zeros((2,2))),0))
    def test_18_loop_small_trace(self):
        self.assertTrue(np.real(np.trace(matrix_holonomy(.02,.04))/2)<=1+1e-14)
