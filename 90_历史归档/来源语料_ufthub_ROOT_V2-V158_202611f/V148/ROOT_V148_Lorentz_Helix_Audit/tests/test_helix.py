import unittest,math
from root_v148.helix import NullHelix,dot,cross,norm,ratio_to_u

class HelixTests(unittest.TestCase):
    def setUp(self): self.h=NullHelix(.6,1.,.8)
    def test_speed(self): self.assertAlmostEqual(self.h.speed(),1)
    def test_x_at_zero(self): self.assertEqual(self.h.position(0)[0],.6)
    def test_axis_motion(self): self.assertAlmostEqual(self.h.position(1.25)[2],1.)
    def test_velocity_norm(self):
        for t in (-5,-1.2,0,3,9): self.assertAlmostEqual(norm(self.h.velocity(t)),1,places=12)
    def test_v_dot_a_zero(self):
        for t in (-2,0,1.2): self.assertAlmostEqual(dot(self.h.velocity(t),self.h.acceleration(t)),0,places=12)
    def test_accelerated_null(self): self.assertAlmostEqual(self.h.four_second_norm(0),.36)
    def test_non_geodesic(self): self.assertGreater(self.h.four_second_norm(.1),0)
    def test_four_null(self):
        for t in [-3,0,2,12]: self.assertAlmostEqual(self.h.null_norm(t),0,places=12)
    def test_curvature(self): self.assertAlmostEqual(self.h.curvature(),.6)
    def test_torsion(self): self.assertAlmostEqual(self.h.torsion(),.8)
    def test_curvature_torsion_identity(self): self.assertAlmostEqual(self.h.curvature()**2+self.h.torsion()**2,self.h.omega**2)
    def test_triple_product_torsion(self):
        for t in [-3,0,.7,8]:
            v=self.h.velocity(t);a=self.h.acceleration(t);j=self.h.jerk(t)
            self.assertAlmostEqual(dot(v,cross(a,j))/norm(cross(v,a))**2,self.h.torsion(),places=12)
    def test_cross_product_curvature(self):
        for t in [0,.3,3]:
            self.assertAlmostEqual(norm(cross(self.h.velocity(t),self.h.acceleration(t)))/norm(self.h.velocity(t))**3,self.h.curvature())
    def test_frenet_orthogonality(self):
        for t in [-1,0,2.8]:
            T,N,B=self.h.frenet(t)
            for a,b in ((T,N),(T,B),(N,B)): self.assertAlmostEqual(dot(a,b),0,places=12)
    def test_frenet_unit(self):
        for t in [0,.1,3.4]:
            for e in self.h.frenet(t): self.assertAlmostEqual(norm(e),1,places=12)
    def test_pitch(self): self.assertAlmostEqual(self.h.pitch(),2*math.pi*.8)
    def test_chirality_changes_torsion(self):
        h=NullHelix(.6,-1,.8); self.assertAlmostEqual(h.curvature(),.6);self.assertAlmostEqual(h.torsion(),-.8)
    def test_planar_circle(self):
        h=NullHelix.from_u_omega(0,1.6);self.assertAlmostEqual(h.torsion(),0);self.assertAlmostEqual(h.curvature(),1.6)
    def test_arbitrary_dimensionless_ratio(self):
        for r in [-999,-4,-1,0,.001,1,17,10000]:
            h=NullHelix.from_u_omega(ratio_to_u(r),1)
            self.assertAlmostEqual(h.torsion()/h.curvature(),r,delta=abs(r)*1e-7+1e-10)
    def test_invalid_speed(self):
        with self.assertRaises(ValueError): NullHelix(.7,1,.8)
    def test_invalid_degenerate(self):
        with self.assertRaises(ValueError): NullHelix(0,1,1)
    def test_invalid_axis(self):
        with self.assertRaises(ValueError): NullHelix.from_u_omega(1,1)
