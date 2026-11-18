import unittest, math, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
import em_gravity as m

class TestPhysics(unittest.TestCase):
    def test_constants(self):
        self.assertAlmostEqual(m.EPS0, 8.8541878188e-12, delta=2e-21)
    def test_zero_energy(self):
        self.assertEqual(m.energy_density(), 0.)
    def test_e_field_energy(self):
        self.assertAlmostEqual(m.energy_density(E=1e6), m.EPS0*1e12/2)
    def test_b_field_energy(self):
        self.assertAlmostEqual(m.energy_density(B=10), 100/(2*m.MU0))
    def test_sign_b_invariance(self):
        self.assertEqual(m.energy_density(B=3),m.energy_density(B=-3))
    def test_sign_e_invariance(self):
        self.assertEqual(m.energy_density(E=5),m.energy_density(E=-5))
    def test_volume(self):
        self.assertAlmostEqual(m.volume_sphere(1),4*math.pi/3)
    def test_volume_invalid(self):
        with self.assertRaises(ValueError): m.volume_sphere(0)
    def test_energy_volume_scaling(self):
        self.assertAlmostEqual(m.energy_sphere(2,B=2)/m.energy_sphere(1,B=2),8)
    def test_energy_b_scaling(self):
        self.assertAlmostEqual(m.energy_sphere(1,B=4)/m.energy_sphere(1,B=1),16)
    def test_mass_equivalence(self):
        self.assertAlmostEqual(m.equivalent_mass(m.C*m.C),1)
    def test_monopole_from_energy(self):
        self.assertAlmostEqual(m.toy_external_gravity_from_energy(m.C*m.C,1),m.G)
    def test_monopole_inverse_square(self):
        self.assertAlmostEqual(m.toy_external_gravity_from_energy(100,1)/m.toy_external_gravity_from_energy(100,2),4)
    def test_g_invalid_radius(self):
        with self.assertRaises(ValueError):m.toy_external_gravity_from_energy(0,0)
    def test_metric(self):
        e=1e8;r=2
        self.assertAlmostEqual(m.toy_metric_h00(e,r),2*m.G*e/(m.C**4*r))
    def test_metric_invalid(self):
        with self.assertRaises(ValueError):m.toy_metric_h00(1,-1)
    def test_faraday(self):
        self.assertEqual(m.faraday_azimuthal_e(2,5),-5)
    def test_faraday_axis(self):
        self.assertEqual(m.faraday_azimuthal_e(0,5),0)
    def test_faraday_bad(self):
        with self.assertRaises(ValueError):m.faraday_azimuthal_e(-1,1)
    def test_quasi_static_peak(self):
        r=m.quasi_static_sphere_energies(10,50,1,0)
        self.assertAlmostEqual(r['U_B_joule'], m.energy_sphere(1,B=10))
        self.assertAlmostEqual(r['U_E_induced_joule'],0,delta=1e-20)
    def test_quasi_static_quarter_cycle(self):
        r=m.quasi_static_sphere_energies(10,50,1,1/(4*50))
        self.assertAlmostEqual(r['U_B_joule'],0,delta=1e-20)
        self.assertGreater(r['U_E_induced_joule'],0)
    def test_quasi_static_average(self):
        a=m.quasi_static_average(10,50,1)
        self.assertAlmostEqual(a['ratio_induced_to_B'],(100*math.pi/m.C)**2/10)
    def test_quasi_static_average_integration(self):
        N=10000;f=50;B=10;r=1;T=1/f
        avg=sum(m.quasi_static_sphere_energies(B,f,r,j*T/N)['U_total_joule'] for j in range(N))/N
        self.assertAlmostEqual(avg,m.quasi_static_average(B,f,r)['average_total_joule'],delta=2e-7)
    def test_nonnegative_energy_time(self):
        for i in range(25):
            self.assertGreaterEqual(m.quasi_static_sphere_energies(10,50,1,i/1000)['U_total_joule'],0)
    def test_quasi_static_negative_f(self):
        with self.assertRaises(ValueError):m.quasi_static_average(1,-1,1)
    def test_quasi_static_invalid_f(self):
        with self.assertRaises(ValueError):m.quasi_static_sphere_energies(1,-1,1,0)
    def test_quasi_parameter(self):
        self.assertLess(m.quasi_static_average(10,50,1)['quasistatic_parameter'],1e-5)
    def test_plane_wave_invariant(self):
        e=1e6;b=e/m.C
        d=m.em_invariants_si((e,0,0),(0,b,0))
        self.assertAlmostEqual(d['I1_T2'],0,delta=1e-22)
        self.assertAlmostEqual(d['P_T2'],0,delta=1e-22)
        self.assertGreater(d['u_J_m3'],0)
    def test_pure_b_invariant(self):
        d=m.em_invariants_si((0,0,0),(0,0,2))
        self.assertEqual(d['I1_T2'],8)
    def test_pure_e_invariant(self):
        d=m.em_invariants_si((3,0,0),(0,0,0))
        self.assertLess(d['I1_T2'],0)
    def test_parallel_pseudoinvariant(self):
        d=m.em_invariants_si((10,0,0),(2,0,0))
        self.assertAlmostEqual(d['P_T2'],20/m.C)
    def test_invariant_bad_dim(self):
        with self.assertRaises(ValueError):m.em_invariants_si((1,2),(1,2,3))
    def test_scalar_rhssign(self):
        self.assertEqual(m.scalar_photon_equation_source(8,2),1)
    def test_scalar_static(self):
        self.assertEqual(m.scalar_static_homogeneous_phi(8,2,2),-.25)
    def test_scalar_mass_invalid(self):
        with self.assertRaises(ValueError):m.scalar_static_homogeneous_phi(1,1,0)
    def test_scalar_lambda_invalid(self):
        with self.assertRaises(ValueError):m.scalar_photon_equation_source(1,0)
    def test_tensor_ratio(self):
        self.assertEqual(m.grav_coupling_ratio(0,2),1)
        self.assertAlmostEqual(m.grav_coupling_ratio(1,1),.5)
    def test_tensor_unhealthy(self):
        with self.assertRaises(ValueError):m.grav_coupling_ratio(2,-1,1)
    def test_rotating_b_energy(self):
        # B direction changes with time but |B| constant. No monopole change in toy model.
        for k in range(20):
            th=2*math.pi*k/20
            b=10*math.hypot(math.cos(th),math.sin(th))
            self.assertAlmostEqual(m.energy_density(B=b),m.energy_density(B=10),delta=2e-8)
    def test_light_wave_energy(self):
        e=1e6;b=e/m.C
        self.assertAlmostEqual(m.em_invariants_si((e,0,0),(0,b,0))['u_J_m3'],m.EPS0*e*e)
    def test_energy_transfer_not_create(self):
        # Closed system redistributes 20 Joules; total gravitational monopole energy unchanged.
        before=m.toy_external_gravity_from_energy(1000,2)
        after=m.toy_external_gravity_from_energy(980+20,2)
        self.assertEqual(before,after)

if __name__=='__main__':unittest.main()
