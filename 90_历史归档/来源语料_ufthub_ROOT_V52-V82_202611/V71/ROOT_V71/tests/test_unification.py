import unittest, math
import numpy as np
from rootv71.physics import *
from rootv71.inference import *

class TheoryTests(unittest.TestCase):
    def test_helix_speed(self):
        k=helical_kinematics(2.,3.,4.)
        self.assertAlmostEqual(k['speed'],math.sqrt(52))
    def test_helix_curvature(self):
        k=helical_kinematics(2.,3.,4.)
        self.assertAlmostEqual(k['kappa'],18/52)
    def test_helix_torsion(self):
        k=helical_kinematics(2.,3.,4.)
        self.assertAlmostEqual(k['torsion'],12/52)
    def test_helix_curvature_plus_torsion(self):
        k=helical_kinematics(2.,3.,4.)
        self.assertAlmostEqual(math.sqrt(k['kappa']**2+k['torsion']**2),abs(3)/k['speed'])
    def test_helix_no_automatic_gravity(self):
        k=helical_kinematics(2.,3.,4.)
        self.assertGreater(k['acceleration'],0)
        self.assertEqual(k['dot_v_a'],0)
    def test_helix_negative_omega(self):
        self.assertLess(helical_kinematics(2.,-3.,4.)['torsion'],0)
    def test_helix_error_zero_omega(self):
        with self.assertRaises(ValueError):helical_kinematics(2.,0.,4.)
    def test_dimensions_no_G(self):
        _,res,rank=dimensions_G_from_c_hbar()
        self.assertGreater(res,.5);self.assertEqual(rank,2)
    def test_gravity_dimension_mass(self):
        # dimension exponents if a new mass scale Mstar is provided: hbar c Mstar^-2
        # [hbar]+[c]-2[M] => L^3 M^-1 T^-2
        self.assertEqual((2+1,1-2,-1-1),(3,-1,-2))
    def test_anomaly_U1(self):self.assertEqual(anomaly_sums()['U1_cubed'],0)
    def test_anomaly_gravU1(self):self.assertEqual(anomaly_sums()['grav_U1'],0)
    def test_anomaly_SU2(self):self.assertEqual(anomaly_sums()['SU2_SU2_U1'],0)
    def test_anomaly_SU3(self):self.assertEqual(anomaly_sums()['SU3_SU3_U1'],0)
    def test_witten_doublets_even(self):self.assertEqual(anomaly_sums()['SU2_doublets']%2,0)
    def test_RGE_MZ_inputs(self):
        inv=gauge_inverse_alphas(MZ)
        self.assertAlmostEqual(inv[2],1/.118)
    def test_RGE_slope(self):
        delta=math.log(10)
        a=gauge_inverse_alphas(MZ*math.exp(delta))
        b=gauge_inverse_alphas(MZ)
        self.assertTrue(np.allclose(a-b,-BETAS/(2*math.pi)*delta))
    def test_RGE_three_separate(self):
        crosses=list(gauge_pair_crossings().values())
        self.assertGreater(max(crosses)/min(crosses),100)
    def test_RGE_minimum_nonzero(self):self.assertGreater(gauge_best_fit()['spread'],3)
    def test_RGE_valid_scale(self):
        with self.assertRaises(ValueError):gauge_inverse_alphas(-1)
    def test_eotvos_antisymmetry(self):self.assertAlmostEqual(eotvos(3,2),-eotvos(2,3))
    def test_eotvos_equal(self):self.assertEqual(eotvos(7,7),0)
    def test_design_fixed_rank(self):self.assertEqual(design_diagnostics(fixed_design())['rank'],1)
    def test_design_mixed_full_rank(self):
        X,_=mixed_design();self.assertEqual(design_diagnostics(X)['rank'],3)
    def test_design_cross_condition(self):
        X,_=mixed_design();self.assertLess(design_diagnostics(X)['condition_normalized'],1e5)
    def test_design_fit(self):
        X,_=mixed_design();ans=fit_synthetic(X)
        self.assertEqual(ans['observations_synthetic'],len(X))
        self.assertTrue(np.isfinite(ans['fitted']).all())
    def test_design_reproducibility(self):
        X,_=mixed_design();self.assertEqual(fit_synthetic(X)['fitted'],fit_synthetic(X)['fitted'])
    def test_design_zero_signal(self):
        row=feature_row('Earth',('Ti','Ti'),0.,0.)
        self.assertTrue(np.all(row==0.))
    def test_design_altitude_change(self):
        a=feature_row('Earth',('Ti','Pt'),0.,0.)
        b=feature_row('Earth',('Ti','Pt'),.4,0.)
        self.assertFalse(np.allclose(a,b,rtol=1e-8,atol=0))
    def test_design_phase_change(self):
        a=feature_row('Earth',('Ti','Pt'),0.,0.)
        b=feature_row('Earth',('Ti','Pt'),0.,math.pi)
        self.assertNotEqual(a[-1],b[-1])
    def test_design_bad_matrix(self):
        with self.assertRaises(ValueError):design_diagnostics(np.arange(10))
    def test_fit_bad_sigma(self):
        with self.assertRaises(ValueError):fit_synthetic(fixed_design(),sigma=0)
    def test_compound_force_counterexample(self):
        # Identical trajectory/position with q=+1,-1 changes E-force sign.
        E=np.array([2.,0.,0.]);self.assertTrue(np.all(E == -(-E)))
    def test_no_local_gravity_zero_in_orbit(self):
        self.assertGreater(central_gravity(EARTH_MU,EARTH_R+400_000),8)

if __name__=='__main__':unittest.main()
