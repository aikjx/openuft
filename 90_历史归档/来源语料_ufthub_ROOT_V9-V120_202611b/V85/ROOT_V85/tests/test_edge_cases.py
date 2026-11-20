import unittest,math
from src.physics import *
from src.simulation import *

class EdgeCases(unittest.TestCase):
    def test_lambda_tiny_zero(self):self.assertEqual(yukawa_point_factor(.3,1e-10),0.)
    def test_r_bad(self):
        with self.assertRaises(ValueError):newton_acceleration(2,0)
    def test_mu_bad(self):
        with self.assertRaises(ValueError):newton_acceleration(0,1)
    def test_lambda_bad(self):
        with self.assertRaises(ValueError):yukawa_point_factor(.2,0)
    def test_negative_l_range(self):
        with self.assertRaises(ValueError):radial_shape_point(.2,.2,-.1)
    def test_denominator_invalid(self):
        with self.assertRaises(ValueError):radial_shape_point(.3,0,.1,universal=-1)
    def test_radius_negative(self):
        with self.assertRaises(ValueError):finite_envelope(-.1,.3,.1)
    def test_rad_inside(self):
        with self.assertRaises(ValueError):finite_envelope(.6,.3,.1)
    def test_R_equal_r(self):self.assertTrue(finite_envelope(.1,.1,.1)>0)
    def test_vary_G_same_mu(self):
        mu=1.e20
        self.assertAlmostEqual(G_REF*2*(mu/(G_REF*2)),mu,delta=1e5)
    def test_a_zero(self):self.assertEqual(normalized_material_difference(1,1,0,0,.3,.1),0)
    def test_equal_q(self):self.assertEqual(normalized_material_difference(1,1,1,.1,.3,.1),0)
    def test_universal_zero_material_difference(self):
        s1=point_yukawa_acceleration(3,.6,0,.3,universal=.2)
        s2=point_yukawa_acceleration(3,.6,0,.3,universal=.2)
        self.assertEqual(s1-s2,0)
    def test_alpha_negative_repulsive_small(self):self.assertLess(point_yukawa_acceleration(1,.1,-.1,.3),newton_acceleration(1,.1))
    def test_Q_positive_alpha(self):self.assertGreater(radial_shape_point(.3,.1,.3),1)
    def test_Q_negative_alpha(self):self.assertLess(radial_shape_point(.3,-.1,.3),1)
    def test_spherical_zero_legacy(self):self.assertAlmostEqual(finite_envelope(0,.2,.3),math.exp(-2/3))
    def test_long_range(self):self.assertAlmostEqual(yukawa_point_factor(.5,1e11),1,delta=1e-14)
    def test_Eotvos_reverse_sign(self):self.assertAlmostEqual(eotvos(1,.3,.9,.05,.4,.2),-eotvos(1,.9,.3,.05,.4,.2))
    def test_two_sensor_bad_geo(self):
        with self.assertRaises(ValueError):two_sensor_common(1,.1,.2)
    def test_two_sensor_grad_bad_geo(self):
        with self.assertRaises(ValueError):two_sensor_gradient(1,.1,.2)
    def test_noise_std_zero(self):
        m=[[1.,2.],[3.,4.]]
        self.assertEqual(gaussian_noisy(m,0,123),m)
    def test_singular_reproduce(self):
        m=[[1.,2.],[2.,4.]]
        sv=singular_values(m)
        self.assertLess(sv[1]/sv[0],1e-15)
    def test_second_field_zero(self):
        src=[(.2,.7,.3,.05),(.8,-.3,.4,.07)]
        pair=[(.1,.7,.3,.8),(.6,.8,.7,.2)]
        z=two_mediator_matrix(src,pair,.3,.2,0,.9)
        one=exact_factor_matrix([(.2,.3,.05),(.8,.4,.07)],[(.1,.7),(.6,.8)],.3,.2)
        for r0,r1 in zip(z,one):
            for x,y in zip(r0,r1):self.assertAlmostEqual(x,y)

if __name__=='__main__':unittest.main()
