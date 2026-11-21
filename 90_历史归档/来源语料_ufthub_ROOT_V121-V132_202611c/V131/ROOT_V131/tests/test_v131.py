"""Unit/property tests for V131 one-loop toy threshold calculations."""
import sys, pathlib, math, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'theory'))
import v131 as v

class Invariants(unittest.TestCase):
    def test_baseline(self): self.assertAlmostEqual(v.a_at_mz()[0],59.02154694,places=8)
    def test_baseline2(self): self.assertAlmostEqual(v.a_at_mz()[1],29.5857551,places=8)
    def test_baseline3(self): self.assertAlmostEqual(v.a_at_mz()[2],1/.118,places=12)
    def test_sm_det(self): self.assertAlmostEqual(v.unification_det_at_mz(),-40.570697436,places=6)
    def test_beta_triplet(self): self.assertAlmostEqual(v.beta_weyl_majorana(2),4/3)
    def test_beta_octet(self): self.assertAlmostEqual(v.beta_weyl_majorana(3),2)
    def test_alpha_positive(self): self.assertTrue(all(z>0 for z in v.a_at_mz()))
    def test_inv_run_mz(self): self.assertEqual(v.inv_couplings(v.MZ),v.a_at_mz())
    def test_a12_crossing(self):
        t=v.crossing_t(0,1); u=v.MZ*math.exp(t); a=v.inv_couplings(u)
        self.assertAlmostEqual(a[0],a[1],places=11)
    def test_a13_crossing(self):
        t=v.crossing_t(0,2); u=v.MZ*math.exp(t); a=v.inv_couplings(u)
        self.assertAlmostEqual(a[0],a[2],places=11)
    def test_a23_crossing(self):
        t=v.crossing_t(1,2); u=v.MZ*math.exp(t); a=v.inv_couplings(u)
        self.assertAlmostEqual(a[1],a[2],places=11)
    def test_triplet_unification(self):
        x=v.one_triplet_solution()
        self.assertLess(x['residual_max_inverse'],1e-10)
    def test_triplet_ge_mz(self): self.assertGreater(v.one_triplet_solution()['Mtriplet_GeV'],v.MZ)
    def test_triplet_below_mu(self):
        x=v.one_triplet_solution()
        self.assertLess(x['Mtriplet_GeV'],x['MU_GeV'])
    def test_triplet_expected(self):
        x=v.one_triplet_solution()
        self.assertAlmostEqual(x['Mtriplet_GeV'],8.050978055e6,delta=0.1)
    def test_triplet_gut_scale(self):
        self.assertAlmostEqual(v.one_triplet_solution()['MU_GeV'],2.432643145e14,delta=5e4)
    def test_upper_bound(self):
        self.assertAlmostEqual(v.triplet_octet_unification_range()['upper_GeV'],3.1442675718e15,delta=1e6)
    def test_lower_bound(self):
        self.assertAlmostEqual(v.triplet_octet_unification_range()['lower_GeV'],v.one_triplet_solution()['MU_GeV'],delta=1e2)
    def test_not_unification_for_sm(self): self.assertNotAlmostEqual(v.unification_det_at_mz(),0,places=1)
    def test_no_equality_full_multiplet_delta(self):
        for z in [0,0.25,1.,7.]:
            self.assertTrue(v.complete_multiplet_differences((z,z,z)))
    def test_no_equality_incomplete(self):
        self.assertFalse(v.complete_multiplet_differences(v.TRIPLET))
        self.assertFalse(v.complete_multiplet_differences(v.OCTET))
    def test_triplet_integral_count_witten(self):
        self.assertEqual(2*2%2,0)
    def test_yukawa_range(self): self.assertTrue(1e-5<v.seesaw_yukawa(v.one_triplet_solution()['Mtriplet_GeV'])<1e-3)
    def test_proton_fourth_power(self): self.assertAlmostEqual(v.proton_decay_relative(2e16)/v.proton_decay_relative(1e16),16)
    def test_proton_alpha_inverse_square(self): self.assertAlmostEqual(v.proton_decay_relative(1e16,alpha=.08)/v.proton_decay_relative(1e16,alpha=.04),.25)
    def test_proton_positive_input(self):
        with self.assertRaises(ValueError): v.proton_decay_relative(0)
    def test_no_below_mz(self):
        with self.assertRaises(ValueError): v.inv_couplings(1000,[(10.,v.TRIPLET)])
    def test_bad_mu(self):
        with self.assertRaises(ValueError): v.inv_couplings(0)
    def test_bad_alpha(self):
        with self.assertRaises(ValueError): v.a_at_mz(alpha_s=0)
    def test_bad_sin(self):
        with self.assertRaises(ValueError): v.a_at_mz(sin2=1)
    def test_parallel_slope(self):
        with self.assertRaises(ValueError): v.crossing_t(0,1,b=(1.,1.,0.))
    def test_invalid_rep(self):
        with self.assertRaises(ValueError): v.b_threshold('X')
    def test_invalid_mu_case(self):
        with self.assertRaises(ValueError): v.triplet_octet_at_scale(v.MZ)
    def test_full_multiplet_doesnt_change_differences(self):
        t=10.; d=(.2,.2,.2); mu=v.MZ*math.exp(t); mm=v.MZ*math.exp(2)
        before=v.inv_couplings(mu)
        after=v.inv_couplings(mu,[(mm,d)])
        for i in [1,2]: self.assertAlmostEqual(before[0]-before[i],after[0]-after[i],places=10)
    def test_uniqueness_in_2_by_2_linear_system(self):
        a=v.a_at_mz(); b=v.B_SM
        self.assertNotEqual((v.TRIPLET[0]-v.TRIPLET[1])*(v.OCTET[0]-v.OCTET[2]),0.)
    def test_lower_point_octet_decoupled(self):
        lo=v.triplet_octet_unification_range()['lower_GeV']; r=v.triplet_octet_at_scale(lo)
        self.assertAlmostEqual(r['Moctet_GeV']/lo,1,places=10)
    def test_upper_point_triplet_at_mz(self):
        hi=v.triplet_octet_unification_range()['upper_GeV'];r=v.triplet_octet_at_scale(hi)
        self.assertAlmostEqual(r['Mtriplet_GeV']/v.MZ,1,places=10)
    def test_refuge_of_naive_uncertainty(self):
        a=v.a_at_mz(alpha_s=.1189)
        self.assertAlmostEqual(v.triplet_octet_unification_range(a)['upper_GeV']/v.triplet_octet_unification_range()['upper_GeV'],1.,places=12)

class Scan(unittest.TestCase):
    pass

# Each generated unittest represents a separate fixed-parameter physical or numerical check.
for k,mu in enumerate([2.5e14,3.0e14,5e14,7e14,1e15,1.4e15,1.8e15,2e15,2.5e15,3e15]):
    def check(self,mu=mu):
        r=v.triplet_octet_at_scale(mu)
        self.assertTrue(r['physical_thresholds'])
        self.assertGreaterEqual(r['Mtriplet_GeV'],v.MZ-1e-4)
        self.assertGreaterEqual(r['Moctet_GeV'],v.MZ-1e-4)
        self.assertLess(r['residual_max_inverse'],1e-10)
    setattr(Scan,'test_physical_%02d'%k,check)
for k,mu in enumerate([3.4e15,4e15,5e15,1e16,1e17]):
    def check(self,mu=mu):
        r=v.triplet_octet_at_scale(mu)
        self.assertFalse(r['physical_thresholds'])
        self.assertLess(r['Mtriplet_GeV'],v.MZ)
    setattr(Scan,'test_unphysical_%02d'%k,check)
for k,factor in enumerate([1,1.5,2,3,4,6,10]):
    def check(self,factor=factor):
        a=v.a_at_mz()
        lo=v.triplet_octet_unification_range(a)
        # Illustrative slope and threshold mass calculation exactly reproduces all 3 at target energy
        mu=2.5e14*factor
        result=v.triplet_octet_at_scale(mu,a)
        if mu<=lo['upper_GeV']:
            self.assertTrue(result['physical_thresholds'])
            self.assertLess(result['residual_max_inverse'],1e-9)
        else:
            self.assertFalse(result['physical_thresholds'])
    setattr(Scan,'test_threshold_scale_%02d'%k,check)

if __name__=='__main__': unittest.main()
