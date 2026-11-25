import math
import unittest
from root_v146.model import illustrative_six_d, SixDimensional

class TestScaling(unittest.TestCase):
    def test_R0_scaling_K4(self):
        a=SixDimensional(1,2,3,1,3).reduce()
        b=SixDimensional(1,2,3,2,3).reduce()
        self.assertAlmostEqual(b.K4/a.K4,4)
    def test_R0_scaling_ABCs(self):
        a=SixDimensional(1,2,3,1,3).reduce()
        b=SixDimensional(1,2,3,2,3).reduce()
        for name in 'ABC': self.assertAlmostEqual(getattr(b,name)/getattr(a,name),16)
    def test_R0_reference_change_vacuum_invariant(self):
        # Different R0 changes the 4D Weyl frame and scales V, not the
        # stationary physical R in a fixed 6D theory.
        sd=illustrative_six_d(3)
        a=sd.reduce()
        b=SixDimensional(sd.K6,sd.Lambda6,sd.chi6,2,sd.n).reduce()
        self.assertAlmostEqual(a.stable().radius,b.stable().radius)
    def test_minkowski_fine_tuning_depends_on_n(self):
        p=illustrative_six_d(3).reduce()
        self.assertAlmostEqual(p.minkowski_tuning_residual(),0)
        self.assertNotAlmostEqual(illustrative_six_d(2).reduce().minkowski_tuning_residual(),0)
    def test_Λ0_AdS_stable(self):
        p=SixDimensional(1,0,1,1,1).reduce()
        e=p.stable(); self.assertLess(e.value,0); self.assertGreater(e.mass2_homogeneous,0)
    def test_4d_G_not_predicted(self):
        a=SixDimensional(1,1,1,1,1).G4()
        b=SixDimensional(2,1,1,1,1).G4()
        self.assertAlmostEqual(b,a/2)
    def test_small_charge_stable_radius_scaling(self):
        sd=illustrative_six_d(1)
        sd2=illustrative_six_d(2)
        self.assertGreater(sd2.reduce().stable().radius,sd.reduce().stable().radius)
    def test_higher_flux_no_local_minimum_at_fixed_Λ(self):
        for n in (4,5,6,7,8): self.assertIsNone(illustrative_six_d(n).reduce().stable())
    def test_stationary_energy_negative_small_n(self):
        for n in (1,2):
            sd=illustrative_six_d(n)
            self.assertLess(sd.reduce().stable().value,0)

if __name__=='__main__': unittest.main()
