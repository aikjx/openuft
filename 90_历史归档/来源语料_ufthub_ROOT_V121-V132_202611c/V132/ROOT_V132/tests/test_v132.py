import math,random,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from root_v132 import *

class V132MathematicalTests(unittest.TestCase):
    def test_01_alpha_inv(self): self.assertAlmostEqual(1/ALPHA_CODATA22,ALPHA_INV_CODATA22,12)
    def test_02_hbar_vs_h(self): self.assertAlmostEqual(HBAR_SI*2*math.pi/H_PLANCK_SI,1,14)
    def test_03_bohr_radius(self): self.assertAlmostEqual(bohr_radius_si()/5.29177210544e-11,1,10)
    def test_04_compton(self): self.assertAlmostEqual(reduced_compton_si()/3.8615926744e-13,1,10)
    def test_05_alpha_length_ratio(self): self.assertAlmostEqual(reduced_compton_si()/bohr_radius_si(),ALPHA_CODATA22,14)
    def test_06_bohr_binding(self): self.assertAlmostEqual(bohr_energy_ev(),13.60569,4)
    def test_07_alpha_charge(self): self.assertLess(abs(alpha_from_charge_si()/ALPHA_CODATA22-1),1e-9)
    def test_08_unit_speed(self): self.assertAlmostEqual(helix_for_geo_alpha(ALPHA_CODATA22).total_speed,1,14)
    def test_09_curvature_identity(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.omega_geometry,h.omega,14)
    def test_10_torsion_ratio(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.tau/h.kappa,ALPHA_CODATA22/math.sqrt(1-ALPHA_CODATA22**2),14)
    def test_11_normalized_circle(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.h_geo*h.h_geo+h.normalized_curvature**2,1,14)
    def test_12_h_geo_alpha(self): self.assertAlmostEqual(helix_for_geo_alpha(ALPHA_CODATA22).h_geo,ALPHA_CODATA22,14)
    def test_13_transverse_convention_alpha(self): self.assertAlmostEqual(helix_for_geo_alpha(ALPHA_CODATA22,mapping='transverse').normalized_curvature,ALPHA_CODATA22,14)
    def test_14_transverse_has_different_h(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22,mapping='transverse')
        self.assertGreater(h.h_geo,0.99)
    def test_15_pitch_curvature_ratio(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.pitch/(2*math.pi*h.radius),h.tau/h.kappa,14)
    def test_16_torsion_per_turn(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.torsion_per_turn/(2*math.pi),ALPHA_CODATA22,14)
    def test_17_curvature_per_turn(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.curvature_per_turn/(2*math.pi),math.sqrt(1-ALPHA_CODATA22**2),14)
    def test_18_inverse_from_kappa_tau(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22,radius=1.7)
        h2=from_kappa_tau(h.kappa,h.tau)
        for a,b in [(h.radius,h2.radius),(h.omega,h2.omega),(h.axial_speed,h2.axial_speed)]: self.assertAlmostEqual(a,b,13)
    def test_19_scale_invariance_dimensionless(self):
        h1=helix_for_geo_alpha(ALPHA_CODATA22,radius=1)
        h2=helix_for_geo_alpha(ALPHA_CODATA22,radius=500)
        self.assertAlmostEqual(h1.h_geo,h2.h_geo,14)
        self.assertAlmostEqual(h1.kappa/h2.kappa,500,12)
    def test_20_action_imports_hbar(self):
        self.assertAlmostEqual(h_geometry_action(ALPHA_CODATA22,HBAR_SI*3)/h_geometry_action(ALPHA_CODATA22,HBAR_SI),3,14)
    def test_21_geometry_cannot_set_hbar(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.h_geo,ALPHA_CODATA22,14)
        self.assertNotEqual(h_geometry_action(h.h_geo),h.h_geo)
    def test_22_nonzero_boost_breaks_alpha(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        hb=h.boosted_axial(0.6)
        self.assertGreater(abs(hb.h_geo-ALPHA_CODATA22),0.5)
    def test_23_boost_null(self): self.assertAlmostEqual(helix_for_geo_alpha(ALPHA_CODATA22).boosted_axial(-0.4).total_speed,1,13)
    def test_24_velocity_addition(self): self.assertAlmostEqual(velocity_addition(0.5,0.5),0,14)
    def test_25_boost_inverse(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        recovered=h.boosted_axial(0.4).boosted_axial(-0.4)
        self.assertAlmostEqual(recovered.h_geo,h.h_geo,13)
    def test_26_geo_energy_sign(self):
        R=reduced_compton_si();h=helix_for_geo_alpha(ALPHA_CODATA22,radius=R)
        self.assertLess(quantum_wire_geometric_potential(M_E_SI,h.kappa),0)
    def test_27_geo_energy_scaling(self):
        R=reduced_compton_si(); h1=helix_for_geo_alpha(ALPHA_CODATA22,radius=R)
        h2=helix_for_geo_alpha(ALPHA_CODATA22,radius=2*R)
        self.assertAlmostEqual(quantum_wire_geometric_potential(M_E_SI,h1.kappa)/quantum_wire_geometric_potential(M_E_SI,h2.kappa),4,12)
    def test_28_geo_energy_large_vs_hydrogen(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22,radius=reduced_compton_si())
        E_geo=abs(quantum_wire_geometric_potential(M_E_SI,h.kappa))/E_CHARGE
        self.assertGreater(E_geo/bohr_energy_ev(),1000)
    def test_29_alpha_uncertainty(self):
        lo,hi=interval_for_alpha_inv()
        self.assertLess(lo,ALPHA_CODATA22);self.assertLess(ALPHA_CODATA22,hi)
    def test_30_wilson_unit(self): self.assertAlmostEqual(abs(wilson_link(.1,20)),1,14)
    def test_31_negative_torsion(self):
        h=from_kappa_tau(1,-0.4)
        self.assertLess(h.h_geo,0)
    def test_32_zero_torsion(self):
        h=from_kappa_tau(1,0)
        self.assertEqual(h.h_geo,0)
    def test_33_arbitrary_geometry_example(self):
        for a in (0.1,0.2,0.5,0.9):
            self.assertAlmostEqual(helix_for_geo_alpha(a).h_geo,a,14)
    def test_34_scale_compton_to_bohr(self):
        a=ALPHA_CODATA22
        self.assertAlmostEqual(bohr_radius_si()*a,reduced_compton_si(),14)
    def test_35_torsion_sign_under_reflection(self):
        h1=from_kappa_tau(1,.2);h2=from_kappa_tau(1,-.2)
        self.assertAlmostEqual(h1.kappa,h2.kappa,14)
        self.assertAlmostEqual(h1.h_geo,-h2.h_geo,14)
    def test_36_helix_period(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(h.length_per_turn,2*math.pi/h.omega,14)
    def test_37_low_energy_alpha_squared(self): self.assertAlmostEqual(standard_born_spectrum_ratio(ALPHA_CODATA22),5.3251354e-5,10)
    def test_38_angular_varies_with_alpha(self):
        self.assertGreater(helix_for_geo_alpha(.2).pitch,helix_for_geo_alpha(.1).pitch)
    def test_39_bad_alpha_value_rejected(self):
        for a in (0,1,1.1,-.2):
            with self.assertRaises(AssertionError):helix_for_geo_alpha(a)
    def test_40_null_physical_proper_time(self):
        h=helix_for_geo_alpha(ALPHA_CODATA22)
        self.assertAlmostEqual(1-h.total_speed**2,0,14)
    def test_41_random_kinematics_property_2000(self):
        rng=random.Random(20261121)
        for i in range(2000):
            eta=rng.uniform(-.9999,.9999);R=10**rng.uniform(-4,4)
            h=Helix(R,math.sqrt(1-eta*eta)/R,eta)
            self.assertAlmostEqual(h.h_geo,eta,12)
            self.assertAlmostEqual(h.total_speed,1,12)
    def test_42_random_boost_property_500(self):
        rng=random.Random(17)
        for i in range(500):
            eta=rng.uniform(-.9,.9);b=rng.uniform(-.85,.85)
            h=Helix(1.,math.sqrt(1-eta*eta),eta).boosted_axial(b)
            self.assertAlmostEqual(h.total_speed,1,11)
            self.assertAlmostEqual(h.h_geo,velocity_addition(eta,b),11)
    def test_43_many_chirality_modes(self):
        h=from_kappa_tau(.7,.3)
        for charge in (-3,-2,-1,0,1,2,3):
            self.assertAlmostEqual(abs(wilson_link(h.tau,h.length_per_turn,charge)),1,13)

if __name__=='__main__': unittest.main(verbosity=2)
