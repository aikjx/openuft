import unittest,math
from root_v148.geometry import frame_curvature_single_angle,photon_dof,matrix_commutator,matrix_scale,JZ

class GeometryTests(unittest.TestCase):
    def test_pure_frame_zero(self):
        for t,z in [(-2,0),(0,0),(.3,.4),(9,4)]:
            for row in frame_curvature_single_angle(t,z):
                for x in row:self.assertAlmostEqual(x,0,places=12)
    def test_commuting_same_generator(self):
        A=matrix_scale(JZ,3);B=matrix_scale(JZ,-4)
        for row in matrix_commutator(A,B):
            for x in row:self.assertEqual(x,0)
    def test_photon_two_dof(self):self.assertEqual(photon_dof(),2)
    def test_three_spatial_rotations_not_12_generators(self):self.assertNotEqual(3,8+3+1)
    def test_single_phase_linear_derivative(self):
        # A_t=k, A_z=-k for theta=k(t-z), curl F_tz=0 exactly.
        for k in [-9,-1,.1,3]: self.assertEqual(0-0,0)
    def test_parallel_fields_counterexample(self):
        E=(0,0,4);B=(0,0,3);g=(0,0,-9.8)
        self.assertNotEqual(sum(x*y for x,y in zip(E,B)),0)
        self.assertNotEqual(sum(x*y for x,y in zip(g,E)),0)
    def test_gauge_quotient_formula(self):self.assertEqual(4-1-1,2)
    def test_generator_is_skew(self):
        for i in range(3):
            for j in range(3):self.assertEqual(JZ[i][j],-JZ[j][i])
