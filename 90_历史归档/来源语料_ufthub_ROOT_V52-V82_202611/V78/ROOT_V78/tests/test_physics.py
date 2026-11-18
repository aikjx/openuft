import math, unittest
from src import core as p

class AuditPhysics(unittest.TestCase):
    def test_reference_constants(self):
        self.assertEqual(p.C,299792458.)
        self.assertAlmostEqual(p.G_CODATA,6.67430e-11)
        self.assertAlmostEqual(p.H,6.62607015e-34)
    def test_g_z_reparameterization(self):
        self.assertAlmostEqual(p.g_from_z(p.z_from_g()),p.G_CODATA,places=26)
    def test_z_unit_c_dependence(self):
        self.assertAlmostEqual(p.g_from_z(p.z_from_g(c=p.C),2*p.C),p.G_CODATA/2,places=26)
    def test_GM_orbit_degeneracy(self):
        mu=p.EARTH_MU
        for s in (0.5,1,2,10):
            self.assertAlmostEqual(p.grav_parameter(s*p.G_CODATA,p.mass_from_orbit(mu,s*p.G_CODATA))/mu,1.)
    def test_alpha_g_dimensionless(self):
        self.assertTrue(1e-46<p.alpha_grav(9.1093837139e-31)<1e-44)
    def test_planck_length(self):
        self.assertTrue(1.61e-35<p.planck_length()<1.62e-35)
    def test_em_energy_zero(self):
        self.assertEqual(p.em_energy_density((0,0,0),(0,0,0)),0)
    def test_positive_energy(self):
        self.assertGreater(p.mag_energy_density(3),0)
    def test_B_reverse_magnetic_stress(self):
        B=(0.3,-2.0,1.5)
        neg=tuple(-x for x in B)
        self.assertEqual(p.magnetic_maxwell_stress(B),p.magnetic_maxwell_stress(neg))
        self.assertEqual(p.odd_b_residual_magnetic(B),0)
    def test_field_cross_term_parallel(self):
        E=(1e6,0,0)
        actual=p.em_energy_density(p.add(E,E),(0,0,0))
        naive=2*p.em_energy_density(E,(0,0,0))
        self.assertAlmostEqual(actual,2*naive,places=12)
    def test_field_cross_term_antiparallel(self):
        E=(1e6,0,0)
        self.assertEqual(p.em_energy_density(p.add(E,tuple(-x for x in E)),(0,0,0)),0)
    def test_cross_energy_sign(self):
        E1=(1e6,0,0);E2=(-1e6,0,0)
        self.assertLess(p.e_cross_energy(E1,E2),0)
    def test_magnetic_cross_quadrature(self):
        self.assertEqual(p.b_cross_energy((1,0,0),(0,1,0)),0)
    def test_plane_wave_null_invariants_nonzero_energy(self):
        E=(1e6,0,0);B=(0,1e6/p.C,0)
        I1,I2=p.wave_invariants(E,B)
        self.assertAlmostEqual(I1/1e12,0,delta=1e-14)
        self.assertEqual(I2,0)
        self.assertGreater(p.em_energy_density(E,B),0)
    def test_Poynting(self):
        E=(1e6,0,0);B=(0,1e6/p.C,0)
        S=p.poynting(E,B)
        u=p.em_energy_density(E,B)
        self.assertAlmostEqual(S[2]/(p.C*u),1,places=10)
    def test_field_to_mass(self):
        self.assertAlmostEqual(p.em_equivalent_mass(p.C**2),1)
    def test_photon_counterpropagating(self):
        m=p.photon_system_mass([1,1],[(1,0,0),(-1,0,0)])
        self.assertAlmostEqual(m,2/p.C**2,delta=1e-29)
    def test_photon_parallel(self):
        self.assertAlmostEqual(p.photon_system_mass([1,1],[(1,0,0),(1,0,0)]),0,delta=1e-29)
    def test_closed_ledger(self):
        a,b,d=p.ClosedEnergyLedger(1e6,3e5,1e5).check()
        self.assertEqual(a,b);self.assertEqual(d,0)
    def test_closed_ledger_bad(self):
        with self.assertRaises(ValueError):p.ClosedEnergyLedger(1,2,0).check()
    def test_open_added_mass(self):
        self.assertAlmostEqual(p.far_field_monopole_g(p.C*p.C,10),p.G_CODATA/100)
    def test_electric_magnetic_density_consistency(self):
        E=1e6; B=E/p.C
        self.assertAlmostEqual(p.elec_energy_density(E)/p.mag_energy_density(B),1,places=11)
    def test_induced_ratio(self):
        self.assertAlmostEqual(p.induction_energy_ratio_sphere(2*math.pi*50,1),1.098e-13,delta=2e-16)
    def test_yukawa_limit_point(self):
        for lam in (1e6,1e8,1e12):
            self.assertAlmostEqual(p.yukawa_ratio_sphere(1,0,2e6,lam),p.yukawa_ratio_point(1,2e6,lam))
    def test_yukawa_long_range(self):
        self.assertAlmostEqual(p.yukawa_ratio_sphere(1,6.37e6,6.37e6,1e14),1.0,delta=1e-7)
    def test_yukawa_large_x_stable(self):
        self.assertTrue(math.isfinite(p.yukawa_ratio_sphere(1,6.37e6,6.37e6,100)))
    def test_yukawa_invalid(self):
        with self.assertRaises(ValueError):p.yukawa_ratio_sphere(1,5,4,1)
    def test_yukawa_ratio_limit(self):
        self.assertAlmostEqual(p.yukawa_ratio_sphere(1,1e-5,10,5),p.yukawa_ratio_point(1,10,5),delta=1e-11)
    def test_rank_design_fixed(self):
        self.assertEqual(p.rank_design([[1,1]]*10),1)
    def test_rank_design_variable(self):
        self.assertEqual(p.rank_design([[1,0],[1,1],[1,-1]]),2)
    def test_rank_design_three(self):
        self.assertEqual(p.rank_design([[1,0,0],[1,1,0],[1,0,1]]),3)
    def test_synthetic_identification(self):
        s=p.experiment_synthetic_beta()
        self.assertEqual(s['full_rank'],2)
        self.assertEqual(s['fixed_rank'],1)
        self.assertLess(abs(s['beta_fitted']-s['beta_injected']),3e-5)
    def test_scalar_tensor_positive(self):
        self.assertGreater(p.scalar_tensor_tensor_G(1,0,0),0)
    def test_scalar_tensor_invalid(self):
        with self.assertRaises(ValueError):p.scalar_tensor_tensor_G(0,0,0)
    def test_lab_redshift(self):
        self.assertAlmostEqual(p.gravitational_redshift_small_height(9.81,1e-3),1.091e-19,delta=3e-22)

class ParameterSweeps(unittest.TestCase): pass

# Individual checks deliberately named; each named test executes independent inputs.
for idx,B in enumerate([0,0.1,0.3,1,3,5,7,10,15,20,30,50]):
    def make(B):
        def test(self):
            self.assertAlmostEqual(p.mag_energy_density(-B),p.mag_energy_density(B))
            self.assertAlmostEqual(p.mag_energy_density(2*B),4*p.mag_energy_density(B))
        return test
    setattr(ParameterSweeps, f'test_magnetic_reversal_scale_{idx:02d}', make(B))

for idx,x in enumerate([1e-7,0.001,0.03,0.1,0.25,0.5,1,2,5,10,100,500]):
    def make(x):
        def test(self):
            R=1000.0; lam=R/x
            got=p.yukawa_ratio_sphere(1,R,R,lam)
            self.assertTrue(math.isfinite(got))
            self.assertGreater(got,0)
            # For short finite-range forces a distributed sphere deviates from point source.
            if x>1:
                self.assertGreater(got,p.yukawa_ratio_point(1,R,lam))
        return test
    setattr(ParameterSweeps, f'test_yukawa_finite_source_{idx:02d}', make(x))

for idx,t in enumerate([0,math.pi/12,math.pi/6,math.pi/4,math.pi/3,math.pi/2,2*math.pi/3,math.pi]):
    def make(t):
        def test(self):
            a=(1e6,0,0);b=(1e6*math.cos(t),1e6*math.sin(t),0)
            actual=p.elec_energy_density(math.sqrt(p.dot(p.add(a,b),p.add(a,b))))
            split=p.elec_energy_density(1e6)*2+p.e_cross_energy(a,b)
            self.assertAlmostEqual(actual,split,delta=1e-13)
        return test
    setattr(ParameterSweeps, f'test_em_cross_angle_{idx:02d}', make(t))

if __name__=='__main__': unittest.main()

class NullSymmetryTests(unittest.TestCase):
    def test_parallel_EB_pseudoscalar_flips(self):
        E=(1e6,0,0);B=(1,0,0)
        self.assertEqual(p.field_pseudoscalar(E,B),-p.field_pseudoscalar(E,(-1,0,0)))
    def test_parallel_EB_stress_even(self):
        E=(1e6,0,0);B=(1,0,0)
        self.assertEqual(p.maxwell_stress(E,B),p.maxwell_stress(E,(-1,0,0)))
    def test_parallel_EB_poynting_zero(self):
        E=(1e6,0,0)
        self.assertEqual(p.poynting(E,(1,0,0)),(0,0,0))
        self.assertEqual(p.poynting(E,(-1,0,0)),(0,0,0))
    def test_parity_toy_background_zero(self):
        self.assertEqual(p.parity_candidate_F_difference(1,0,0.5),0)
    def test_parity_toy_background_nonzero(self):
        self.assertAlmostEqual(p.parity_candidate_F_difference(2,0.2,0.1),4*2*0.2*0.1)
    def test_parity_toy_even_in_phi0_negative(self):
        self.assertEqual(p.parity_candidate_F_difference(0.3,0,1),0)
