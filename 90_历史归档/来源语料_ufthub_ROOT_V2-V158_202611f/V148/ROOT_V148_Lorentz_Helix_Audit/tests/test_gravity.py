import unittest,math
from root_v148.gravity import EARTH,MOON

class GravityTests(unittest.TestCase):
    def test_earth_mu(self):self.assertAlmostEqual(EARTH.GM_SI,398600.435507e9)
    def test_moon_mu(self):self.assertAlmostEqual(MOON.GM_SI,4902.800118e9)
    def test_earth_g_range(self):self.assertGreater(EARTH.g(0),9.8);self.assertLess(EARTH.g(0),9.9)
    def test_moon_g_range(self):self.assertGreater(MOON.g(0),1.62);self.assertLess(MOON.g(0),1.63)
    def test_altitude_decay_earth(self):self.assertGreater(EARTH.g(100e3),EARTH.g(400e3))
    def test_altitude_decay_moon(self):self.assertGreater(MOON.g(100e3),MOON.g(400e3))
    def test_inverse_square_ratio_earth(self):self.assertAlmostEqual(EARTH.distance_ratio(0,400e3),1)
    def test_inverse_square_ratio_moon(self):self.assertAlmostEqual(MOON.distance_ratio(0,400e3),1)
    def test_acceleration_direction(self):
        a=MOON.acceleration((MOON.radius_m,0,0))
        self.assertLess(a[0],0);self.assertEqual(a[1:],(0.,0.))
    def test_acceleration_magnitude(self):
        g=EARTH.acceleration((0,0,EARTH.radius_m))
        self.assertAlmostEqual(abs(g[2]),EARTH.g(0))
    def test_inside_sphere_not_supported(self):
        with self.assertRaises(ValueError):MOON.acceleration((5,0,0))
    def test_negative_radius(self):
        with self.assertRaises(ValueError):EARTH.g(-EARTH.radius_m)
