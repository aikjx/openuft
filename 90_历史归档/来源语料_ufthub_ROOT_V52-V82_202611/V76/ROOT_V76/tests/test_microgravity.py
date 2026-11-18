import math, sys, pathlib, unittest, random
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
from microgravity import *

class TestConstants(unittest.TestCase):
    def test_c_exact(self): self.assertEqual(C,299792458.)
    def test_G_external(self): self.assertEqual(G,6.67430e-11)
    def test_mu_eps_consistency(self): self.assertAlmostEqual(C*math.sqrt(EPS0*MU0),1,places=13)
    def test_e_exact(self): self.assertEqual(E_CHARGE,1.602176634e-19)
    def test_mev_j(self): self.assertAlmostEqual(MEV/E_CHARGE,1e6)

class TestVectors(unittest.TestCase):
    def test_dot_orthogonal(self): self.assertEqual(dot((1,0,0),(0,1,0)),0)
    def test_cross_basis(self): self.assertEqual(cross((1,0,0),(0,1,0)),(0,0,1))
    def test_norm(self): self.assertEqual(norm((3,4,0)),5)
    def test_add_sub(self): self.assertEqual(minus(plus((2,3,4),(5,-1,0)),(5,-1,0)),(2,3,4))
    def test_vec_reject_dim(self):
        with self.assertRaises(ValueError): vec((1,2))
    def test_cross_orthogonal(self):
        a=(1,2,3);b=(-2,4,1);c=cross(a,b)
        self.assertAlmostEqual(dot(a,c),0);self.assertAlmostEqual(dot(b,c),0)

class TestEM(unittest.TestCase):
    def test_vacuum(self): self.assertEqual(em_energy_density((0,0,0),(0,0,0)),0)
    def test_e_only(self): self.assertAlmostEqual(em_energy_density((1e6,0,0),(0,0,0)),.5*EPS0*1e12)
    def test_b_only(self): self.assertAlmostEqual(em_energy_density((0,0,0),(0,0,10)),50/MU0)
    def test_cross_parallel(self): self.assertAlmostEqual(em_cross_energy((1,0,0),(0,0,0),(1,0,0),(0,0,0)),EPS0)
    def test_cross_antiparallel(self): self.assertAlmostEqual(em_cross_energy((1,0,0),(0,0,0),(-1,0,0),(0,0,0)),-EPS0)
    def test_cross_orthogonal(self): self.assertEqual(em_cross_energy((1,0,0),(0,0,0),(0,1,0),(0,0,0)),0)
    def test_cancel_e(self): self.assertEqual(em_energy_density(plus((1,0,0),(-1,0,0)),(0,0,0)),0)
    def test_parallel_fourfold(self): self.assertAlmostEqual(em_energy_density((2,0,0),(0,0,0))/em_energy_density((1,0,0),(0,0,0)),4)
    def test_random_superposition(self):
        r=random.Random(38)
        for i in range(100):
            E1=tuple(r.uniform(-100,100) for _ in range(3));B1=tuple(r.uniform(-1e-5,1e-5) for _ in range(3))
            E2=tuple(r.uniform(-100,100) for _ in range(3));B2=tuple(r.uniform(-1e-5,1e-5) for _ in range(3))
            z=em_superposition_identity(E1,B1,E2,B2)
            self.assertAlmostEqual(z['total'],z['sum'],delta=max(1e-12,abs(z['total'])*1e-12))
    def test_poynting_cross(self): self.assertEqual(em_energy_flux((1,0,0),(0,1,0)),(0,0,1/MU0))
    def test_stress_symmetric(self):
        e=em_tensor((13,5,-8),(1e-3,2e-3,3e-3))
        for i in range(3):
            for j in range(3): self.assertAlmostEqual(e.spatial[i][j],e.spatial[j][i])
    def test_stress_trace_zero_cases(self):
        for E,B in [((1e6,0,0),(0,0,0)),((0,0,0),(0,0,10)),((12,-30,40),(.1,.2,.3))]:
            t=em_tensor(E,B)
            self.assertAlmostEqual(t.trace(),0,delta=max(1e-15,t.energy_density*1e-12))
    def test_stress_e_only(self):
        t=em_tensor((100,0,0),(0,0,0))
        self.assertAlmostEqual(t.spatial[0][0],-t.energy_density)
        self.assertAlmostEqual(t.spatial[1][1],t.energy_density)
        self.assertAlmostEqual(t.spatial[2][2],t.energy_density)
    def test_plane_wave_invariants(self):
        for p in [0,.1,1,math.pi/4]:
            e,b=plane_wave_fields(10e5,p)
            x=em_invariants(e,b)
            self.assertAlmostEqual(x['B2_minus_E2_over_c2'],0,delta=2e-18)
            self.assertEqual(x['E_dot_B'],0)
            self.assertGreater(em_energy_density(e,b),0)
    def test_plane_wave_flux(self):
        E,B=plane_wave_fields(1e6,0)
        t=em_tensor(E,B)
        self.assertAlmostEqual(norm(em_energy_flux(E,B))/C,t.energy_density,delta=t.energy_density*1e-12)
        self.assertAlmostEqual(t.spatial[2][2],t.energy_density)
        self.assertAlmostEqual(t.momentum_energy[2],t.energy_density)
    def test_local_active_double_u(self):
        t=em_tensor((1e3,2e3,3e3),(.1,.2,.3))
        self.assertAlmostEqual(t.active_density(),2*t.energy_density/C**2,delta=t.active_density()*1e-12)
    def test_em_energy_nonnegative_random(self):
        rng=random.Random(4)
        for _ in range(20):
            e=tuple(rng.uniform(-5e6,5e6) for _ in range(3));b=tuple(rng.uniform(-5,5) for _ in range(3))
            self.assertGreaterEqual(em_energy_density(e,b),0)
    def test_anti_mag_cancel(self):
        self.assertEqual(em_energy_density((0,0,0),plus((0,0,4),(0,0,-4))),0)

class TestEnergyMass(unittest.TestCase):
    def test_1kwh(self): self.assertAlmostEqual(gravitating_equivalent_mass(3.6e6),3.6e6/C**2)
    def test_zero_mass(self): self.assertEqual(gravitating_equivalent_mass(0),0)
    def test_negative_delta(self): self.assertLess(gravitating_equivalent_mass(-1),0)
    def test_sphere_field(self): self.assertAlmostEqual(sphere_field_energy(10,1),4*math.pi/3*50/MU0)
    def test_sphere_radius_scaling(self): self.assertAlmostEqual(sphere_field_energy(10,2)/sphere_field_energy(10,1),8)
    def test_sphere_B_scaling(self): self.assertAlmostEqual(sphere_field_energy(20,1)/sphere_field_energy(10,1),4)
    def test_sphere_negative_radius(self):
        with self.assertRaises(ValueError): sphere_field_energy(1,-1)
    def test_monopole_1_over_r2(self): self.assertAlmostEqual(spherical_monopole_delta_g(1e8,4)/spherical_monopole_delta_g(1e8,2),.25)
    def test_monopole_bad_distance(self):
        with self.assertRaises(ValueError): spherical_monopole_delta_g(1,-1)
    def test_thermal(self): self.assertEqual(thermal_energy(2,500,10),10000)
    def test_deuteron_mass_defect(self): self.assertTrue(3.9e-30 < nuclear_binding_mass_defect() <4.1e-30)
    def test_redshift_mm(self): self.assertTrue(1e-19 < redshift_fraction(.001)<1.2e-19)
    def test_relativistic_rest(self): self.assertEqual(relativistic_energy(2,0),2*C*C)
    def test_relativistic_kin_zero(self): self.assertEqual(relativistic_kinetic_energy(2,0),0)
    def test_relativistic_kin_halfc(self):
        self.assertAlmostEqual(relativistic_kinetic_energy(1,.5*C)/(C*C),1/math.sqrt(.75)-1)
    def test_negative_v_sym(self): self.assertAlmostEqual(relativistic_energy(1,.7*C),relativistic_energy(1,-.7*C))
    def test_bad_v(self):
        with self.assertRaises(ValueError): relativistic_energy(1,C)
    def test_gamma_two(self): self.assertAlmostEqual(relativistic_energy(1,C*math.sqrt(.75))/(C*C),2,places=13)

class TestInvariantMass(unittest.TestCase):
    def test_rest_closed(self): self.assertAlmostEqual(system_invariant_mass(3*C*C,(0,0,0)),3)
    def test_single_photon(self): self.assertEqual(two_photon_invariant_mass(1,0,1),0)
    def test_two_collinear(self): self.assertAlmostEqual(two_photon_invariant_mass(1,1,0),0)
    def test_two_opposite(self): self.assertAlmostEqual(two_photon_invariant_mass(1,1,math.pi),2/C**2)
    def test_two_orthogonal(self): self.assertAlmostEqual(two_photon_invariant_mass(1,1,math.pi/2),math.sqrt(2)/C**2)
    def test_photon_energy_scaling(self): self.assertAlmostEqual(two_photon_invariant_mass(10,10,math.pi)/two_photon_invariant_mass(1,1,math.pi),10)
    def test_system_bad_spacelike(self):
        with self.assertRaises(ValueError): system_invariant_mass(1,(1,0,0))
    def test_two_photon_energy_momentum(self):
        E=3.0
        self.assertAlmostEqual(system_invariant_mass(2*E,(0,0,0)),two_photon_invariant_mass(E,E,math.pi))
    def test_two_photon_right_angle_manual(self):
        E=4.0
        p=(E/C,E/C,0)
        self.assertAlmostEqual(system_invariant_mass(2*E,p),two_photon_invariant_mass(E,E,math.pi/2),delta=1e-30)

class TestQuantum(unittest.TestCase):
    def test_uncoupled_diag_phase_invariant(self):
        for ph in [0,.3,1,math.pi]: self.assertAlmostEqual(quantum_two_level_energy(1,2,0,math.pi/4,ph),1.5)
    def test_phase_cross(self):
        self.assertAlmostEqual(quantum_two_level_energy(1,2,.2,math.pi/4,0),1.7)
        self.assertAlmostEqual(quantum_two_level_energy(1,2,.2,math.pi/4,math.pi),1.3)
    def test_phase_90(self): self.assertAlmostEqual(quantum_two_level_energy(1,2,.2,math.pi/4,math.pi/2),1.5)
    def test_energy_in_spectrum(self):
        lo,hi=quantum_two_level_eigenvalues(1,2,.2)
        for ph in [i*math.pi/10 for i in range(21)]:
            e=quantum_two_level_energy(1,2,.2,math.pi/4,ph)
            self.assertLessEqual(e,hi+1e-12);self.assertGreaterEqual(e,lo-1e-12)
    def test_diagonal_eigenvalues(self): self.assertEqual(quantum_two_level_eigenvalues(1,2,0),(1,2))

class TestEnergyLedger(unittest.TestCase):
    def test_transfer_conserved(self):
        a=Ledger(1e9,0,1e3,2e3);b=a.transfer_to_field(1e8)
        self.assertEqual(a.total(),b.total())
    def test_transfer_field(self):
        a=Ledger(20,0,0,0).transfer_to_field(10)
        self.assertEqual(a.field,10);self.assertEqual(a.battery,10)
    def test_field_to_heat(self):
        a=Ledger(10,20,0,0);b=a.transfer_to_heat(5)
        self.assertEqual(b.total(),a.total());self.assertEqual(b.thermal,5)
    def test_system_mass_invariance(self):
        a=Ledger(1e9,0,0,0);b=a.transfer_to_field(1e8)
        self.assertEqual(gravitating_equivalent_mass(a.total()),gravitating_equivalent_mass(b.total()))
    def test_emission_reduces_mass(self):
        a=Ledger(0,0,0,0,100);b=a.emission(40)
        self.assertAlmostEqual((a.total()-b.total())/C**2,40/C**2)
    def test_invalid_battery(self):
        with self.assertRaises(ValueError): Ledger(0,0,0,0).transfer_to_field(1)
    def test_invalid_heat(self):
        with self.assertRaises(ValueError): Ledger(0,0,0,0).transfer_to_heat(1)
    def test_invalid_emission(self):
        with self.assertRaises(ValueError): Ledger(0,0,0,0).emission(1)

class TestMotion(unittest.TestCase):
    def test_helix_components(self):
        h=helix(5,3,1,4)
        self.assertAlmostEqual(h['curvature'],3/25)
        self.assertAlmostEqual(h['torsion'],4/25)
        self.assertEqual(h['acceleration'],3)
    def test_helix_straight(self):
        h=helix(5,3,0,5)
        self.assertEqual(h['curvature'],0);self.assertEqual(h['torsion'],0)
    def test_helix_reject_inconsistent(self):
        with self.assertRaises(ValueError): helix(4,3,1,4)
    def test_helix_is_kinematics(self):
        h=helix(C,10,C*.6/10,C*.8)
        self.assertAlmostEqual(h['speed']/C,1)
    def test_GM_degeneracy(self):
        p=identifiability_one_observation(10,2,5)
        self.assertEqual(p['mu'],250)
        self.assertEqual(p['fitted_G_if_mass_known'],125)
    def test_source_count(self): self.assertGreaterEqual(len(source_taxonomy()),30)

if __name__=='__main__':unittest.main(verbosity=2)
