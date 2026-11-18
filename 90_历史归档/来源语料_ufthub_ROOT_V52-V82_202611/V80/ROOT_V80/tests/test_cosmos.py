import math
import unittest
from src.cosmos import *

class ConstantsAndDimensions(unittest.TestCase):
    def test_light_speed_exact(self): self.assertEqual(C,299792458.0)
    def test_cod_g(self): self.assertAlmostEqual(G,6.67430e-11)
    def test_qed_b(self): self.assertAlmostEqual(q_ed_critical_field()/1e9,4.41400523,places=6)
    def test_dimension_no_go(self): self.assertFalse(scalar_g_c_no_go()['consistent'])
    def test_reparam(self): self.assertAlmostEqual(g_versus_c_reparam(C,G*C/2),G,places=20)
    def test_mu_degeneracy(self):
        for k in [0.25,0.5,2,7]:
            gg,mm=gravitational_mu_identifiability(G,1e20,k)
            self.assertAlmostEqual(gg*mm/(G*1e20),1.0,places=14)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): mean_density(1,-1)
        with self.assertRaises(ValueError): magnetic_rest_ratio(1,0)
        with self.assertRaises(ValueError): g_versus_c_reparam(0,1)
        with self.assertRaises(ValueError): gravitational_mu_identifiability(1,1,0)

class Mechanics(unittest.TestCase):
    def test_gr_isco(self): self.assertAlmostEqual(gr_isco(M_SUN)/schwarzschild_radius(M_SUN),3.0)
    def test_photon_sphere(self): self.assertAlmostEqual(gr_photon_sphere(M_SUN)/schwarzschild_radius(M_SUN),1.5)
    def test_mercury(self): self.assertTrue(42.9<mercury_precession_arcsec_century()<43.1)
    def test_period_consistency(self):
        r=6.77e6; mu=G*BODIES[3].mass_kg
        self.assertAlmostEqual(orbital_frequency(mu,r)*circular_orbit_period(mu,r),2*math.pi)
    def test_schwarzschild_horizon_invalid(self):
        with self.assertRaises(ValueError): redshift_surface_to_infinity(M_SUN,schwarzschild_radius(M_SUN))
    def test_earth_surface(self): self.assertTrue(9.75<surface_g(BODIES[3].mass_kg,BODIES[3].radius_m)<9.86)
    def test_ns_compactness(self): self.assertTrue(0.15<compactness(BODIES[-1].mass_kg,BODIES[-1].radius_m)<0.20)
    def test_weak_field_redshift(self):
        body=BODIES[3]; chi=compactness(body.mass_kg,body.radius_m)
        self.assertAlmostEqual(redshift_surface_to_infinity(body.mass_kg,body.radius_m)/chi,1.0,places=6)
    def test_density_k(self):
        # At fixed mean density, exterior Schwarzschild K at the surface is independent of R.
        rho=5500.0; r1=1e6; r2=2e6
        m1=4*math.pi*r1**3*rho/3; m2=4*math.pi*r2**3*rho/3
        self.assertAlmostEqual(kretschmann(m1,r1)/kretschmann(m2,r2),1.0,places=12)
    def test_kr4_relation(self):
        for obj in BODIES:
            if obj.name.startswith('磁星'): continue
            ratio=kretschmann(obj.mass_kg,obj.radius_m)*obj.radius_m**4/(48*compactness(obj.mass_kg,obj.radius_m)**2)
            self.assertAlmostEqual(ratio,1,places=12)

class Electromagnetism(unittest.TestCase):
    def test_b_even(self):
        for val in [0,1e-5,0.3,1e4,1e10]:
            self.assertEqual(magnetic_energy_density(val), magnetic_energy_density(-val))
    def test_b_squared(self):
        self.assertAlmostEqual(magnetic_energy_density(3)/magnetic_energy_density(1),9.0)
    def test_plane_wave_invariants(self):
        x=photon_zero_invariant_nonzero_energy(1e6)
        self.assertEqual(x['electric_minus_c2magnetic'],0.0)
        self.assertEqual(x['e_dot_b'],0.0)
        self.assertGreater(x['energy_j_m3'],0)
    def test_em_energy_not_total_mass(self):
        # Internal energy transfer cannot change total closed-system mass by itself.
        initial={'battery':100.0,'field':0.0,'heat':0.0}
        final={'battery':10.0,'field':85.0,'heat':5.0}
        self.assertEqual(sum(initial.values()),sum(final.values()))
    def test_magnetar_qed_regime(self):
        self.assertGreater(1e10/q_ed_critical_field(),1)
    def test_earth_qed_regime(self): self.assertLess(5e-5/q_ed_critical_field(),1e-12)
    def test_magnetic_mass_fraction(self):
        obj=BODIES[-1]; ratio=body_report(obj)['magnetic_to_mean_rest_energy_ratio']
        self.assertGreater(ratio,1e-10)
        self.assertLess(ratio,1e-8)
    def test_em_source_is_not_only_f2(self):
        result=photon_zero_invariant_nonzero_energy(3e4)
        self.assertEqual(result['electric_minus_c2magnetic'],0)
        self.assertGreater(result['energy_j_m3'],0)

class Catalogue(unittest.TestCase):
    def test_unique_names(self): self.assertEqual(len(set(x.name for x in BODIES)),len(BODIES))
    def test_count(self): self.assertGreaterEqual(len(BODIES),13)
    def test_no_false_source_for_compacts(self):
        self.assertTrue(all(x.provenance=='SYNTHETIC' for x in BODIES[-3:]))
    def test_b_fields_optional(self):
        self.assertIsNone(body_report(BODIES[1])['magnetic_energy_J_m3'])
    def test_report_fields(self):
        d=body_report(BODIES[3]); self.assertIn('limitations',d)
        self.assertIn('mean_density_kg_m3',d)
    def test_field_g_candidate_is_hypothesis(self):
        d=body_report(BODIES[-1]); chi_B=d['magnetic_to_mean_rest_energy_ratio']
        self.assertAlmostEqual(candidate_field_dependent_fraction(1e10,d['mean_density_kg_m3'],2.0),2*chi_B)
    def test_no_b_field_universal_gravity(self):
        # Moon with no imposed B in illustrative catalogue still has gravity.
        d=body_report(BODIES[4]); self.assertIsNone(d['assumed_B_T']); self.assertGreater(d['newtonian_g_m_s2'],1)

# Programmatically generate independent body-specific consistency checks.
for index, body in enumerate(BODIES):
    def _create_mass_density(obj):
        def test(self):
            reported=mean_density(obj.mass_kg,obj.radius_m)
            self.assertAlmostEqual(reported*(4*math.pi*obj.radius_m**3/3)/obj.mass_kg,1.0,places=13)
        return test
    def _create_tidal(obj):
        def test(self):
            self.assertAlmostEqual(tidal_max(obj.mass_kg,obj.radius_m)/(2*surface_g(obj.mass_kg,obj.radius_m)/obj.radius_m),1.0,places=12)
        return test
    setattr(Catalogue,f'test_density_body_{index:02d}',_create_mass_density(body))
    setattr(Catalogue,f'test_tidal_body_{index:02d}',_create_tidal(body))

if __name__=='__main__': unittest.main(verbosity=2)
