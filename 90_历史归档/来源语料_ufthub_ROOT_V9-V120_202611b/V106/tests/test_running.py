import unittest, math
import numpy as np
from src.running import B,Benchmark,inverse_at,intersection,invariant,optimal_spread,benchmark_scan

class TestRunning(unittest.TestCase):
    def test_01_betas(self):np.testing.assert_allclose(B,[4.1,-19/6,-7])
    def test_02_input_couplings(self):np.testing.assert_allclose(Benchmark().inv_couplings(),[59.01001524,29.5799746,8.47457627118644])
    def test_03_recover_start(self):np.testing.assert_allclose(inverse_at(0),Benchmark().inv_couplings())
    def test_04_exact_linear(self):np.testing.assert_allclose(inverse_at(4)-inverse_at(2),-B/math.pi)
    def test_05_intersection_12(self):self.assertAlmostEqual(intersection(0,1)['mu_gev'],1.0265958696446e13,delta=2e5)
    def test_06_intersection_13(self):self.assertAlmostEqual(intersection(0,2)['mu_gev'],2.41681565847583e14,delta=5e6)
    def test_07_intersection_23(self):self.assertAlmostEqual(intersection(1,2)['mu_gev'],9.633466964396e16,delta=5e9)
    def test_08_intersection_symmetric(self):self.assertAlmostEqual(intersection(1,0)['mu_gev'],intersection(0,1)['mu_gev'])
    def test_09_no_triplet_meeting(self):self.assertGreater(abs(intersection(0,1)['inv_at_scale'][2]-intersection(0,1)['inv_at_scale'][0]),5)
    def test_10_invariant_nonzero(self):self.assertAlmostEqual(invariant(),-40.55073873604525,places=9)
    def test_11_invariant_at_different_scales(self):
        aa=Benchmark().inv_couplings()
        for t in [-4,0,7,20,30]:
            bb=inverse_at(t);v=lambda x:(B[1]-B[2])*x[0]+(B[2]-B[0])*x[1]+(B[0]-B[1])*x[2]
            self.assertAlmostEqual(v(aa),v(bb),places=11)
    def test_12_optimal_spread_nonzero(self):self.assertGreater(optimal_spread()['range'],3)
    def test_13_optimal_spread_smaller_than_t0(self):self.assertLess(optimal_spread()['range'],float(np.ptp(inverse_at(0))))
    def test_14_alpha_s_sensitivity(self):
        a=invariant(Benchmark(alpha_s=.1171));b=invariant(Benchmark(alpha_s=.1189));self.assertNotEqual(a,b)
    def test_15_small_toy_scan(self):
        x=benchmark_scan(1001,123);self.assertEqual(x['n'],1001);self.assertTrue(x['all_negative'])
    def test_16_scan_reproducible(self):self.assertEqual(benchmark_scan(90,42),benchmark_scan(90,42))
    def test_17_bad_alpha(self):
        with self.assertRaises(ValueError):Benchmark(alpha_s=0).inv_couplings()
    def test_18_bad_angle(self):
        with self.assertRaises(ValueError):Benchmark(sin2_theta=1.2).inv_couplings()
    def test_19_bad_intersection(self):
        with self.assertRaises(ValueError):intersection(1,1)
    def test_20_pairwise_scales_distinct(self):
        es=[intersection(*ij)['mu_gev'] for ij in [(0,1),(0,2),(1,2)]]
        self.assertTrue(es[0]<es[1]<es[2])
    def test_21_slope_signs(self):self.assertEqual(list(np.sign(B)),[1.,-1.,-1.])
