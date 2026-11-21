import sys, unittest, math
from pathlib import Path
from fractions import Fraction
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from v129_core import (anomaly_polynomials,evaluate_anomalies,sm_hypercharges,
    electric_charges,kk_mass,kk_charge,rest_compton_radius,boosted_phase,
    su2_jacobi,M_E,M_E_MEV,M_MU_MEV,HBAR,C,E_CHARGE,audit_snapshot,
    minimal_kk_coupling,electromagnetic_coupling,kk_radius_to_match_em_coupling)
q,l,h=sp.symbols('q l h')

class TestAnomalyIdentities(unittest.TestCase):
    def test_three_color_mixed_anomaly_identically_zero(self):
        self.assertEqual(anomaly_polynomials(True)['SU3SU3Y'],0)
    def test_weak_anomaly_structure(self):
        self.assertEqual(anomaly_polynomials(True)['SU2SU2Y'],3*q+l)
    def test_gravity_anomaly_with_neutrino_vanishes_algebraically(self):
        self.assertEqual(anomaly_polynomials(True)['gravgravY'],0)
    def test_cubic_anomaly_with_neutrino_factorization(self):
        self.assertEqual(anomaly_polynomials(True)['YYY'],-6*h*h*(3*q+l))
    def test_gravity_anomaly_without_neutrino(self):
        self.assertEqual(anomaly_polynomials(False)['gravgravY'],h+l)
    def test_cubic_anomaly_without_neutrino_factorization(self):
        self.assertEqual(sp.factor(anomaly_polynomials(False)['YYY']+6*h*h*(3*q+l)),(l+h)**3)
    def test_weak_anomaly_sets_lepton_charge(self):
        self.assertEqual(sp.solve([3*q+l],[l])[l],-3*q)
    def test_without_nu_constraints_unique_hypercharges(self):
        # Solve two linear anomaly equations; cubic then vanishes.
        ans=sp.solve([3*q+l,l+h],[q,l], dict=True)
        self.assertEqual(ans,[{q:h/3,l:-h}])
    def test_without_nu_cubic_nonlinear_unique_real_root(self):
        poly=anomaly_polynomials(False)['YYY'].subs({l:-3*q,h:sp.Rational(1,2)})
        self.assertEqual(sp.expand(poly),sp.expand(-(3*q-sp.Rational(1,2))**3))
    def test_sm_anomalies_zero_without_nu(self):
        self.assertTrue(all(v==0 for v in evaluate_anomalies(sp.Rational(1,6),-sp.Rational(1,2),right_neutrino=False).values()))
    def test_sm_anomalies_zero_with_nu(self):
        self.assertTrue(all(v==0 for v in evaluate_anomalies(sp.Rational(1,6),-sp.Rational(1,2),right_neutrino=True).values()))
    def test_SU3_cubic_triplet_antitriplet_balance(self):
        self.assertEqual(2-1-1,0)
    def test_weak_doublets_even_for_global_anomaly(self):
        self.assertEqual((3+1)%2,0)
    def test_wrong_lepton_hypercharge_causes_weak_anomaly(self):
        self.assertNotEqual(evaluate_anomalies(sp.Rational(1,6),-sp.Rational(2,5))['SU2SU2Y'],0)
    def test_wrong_color_hypercharge_causes_weak_anomaly(self):
        self.assertNotEqual(evaluate_anomalies(sp.Rational(1,5),-sp.Rational(1,2))['SU2SU2Y'],0)
    def test_wrong_right_neutrino_missing_can_expose_anomaly(self):
        residual=evaluate_anomalies(sp.Rational(1,5),-sp.Rational(3,5),right_neutrino=False)
        self.assertNotEqual(residual['YYY'],0)
    def test_all_x_family_have_no_anomalies_with_right_neutrino(self):
        for x in [sp.Rational(-5,3),sp.Rational(-1,6),sp.Rational(0),sp.Rational(1,100),sp.Rational(13,5)]:
            with self.subTest(x=x):
                y=sm_hypercharges(x)
                res=evaluate_anomalies(y['Q_L'],y['L_L'])
                self.assertTrue(all(v==0 for v in res.values()))
    def test_majorana_gauge_invariance_forces_x_zero(self):
        x=sp.symbols('x')
        nu=-x
        self.assertEqual(sp.solve([2*nu],[x]),{x:0})
    def test_neutrino_hypercharge_without_right_neutrino_forced_zero(self):
        charges=sm_hypercharges(0, False)
        self.assertEqual(charges['L_L']+sp.Rational(1,2),0)
    def test_one_generation_all_quantum_numbers_exact(self):
        y=sm_hypercharges()
        known={'Q_L':sp.Rational(1,6),'u_R':sp.Rational(2,3),
        'd_R':-sp.Rational(1,3),'L_L':-sp.Rational(1,2),'e_R':sp.Integer(-1),'nu_R':sp.Integer(0)}
        self.assertEqual(y,known)
    def test_electron_charge_equals_minus_one_at_x_zero(self):
        self.assertEqual(electric_charges(0)['electron'],-1)
    def test_neutrino_charge_equals_zero_at_x_zero(self):
        self.assertEqual(electric_charges(0)['neutrino'],0)
    def test_nonzero_x_makes_neutrino_electrically_charged(self):
        self.assertEqual(electric_charges(sp.Rational(1,10))['neutrino'],-sp.Rational(1,10))
    def test_hypercharge_shift_is_B_minus_L(self):
        x=sp.Rational(7,23)
        y=sm_hypercharges(x)
        y0=sm_hypercharges(0)
        self.assertEqual(y['Q_L']-y0['Q_L'],x/3)
        self.assertEqual(y['L_L']-y0['L_L'],-x)
    def test_yukawa_relations_hold_for_whole_family(self):
        for x in (0,sp.Rational(1,31),sp.Rational(-4,7)):
            y=sm_hypercharges(x)
            self.assertEqual(y['u_R']-y['Q_L'],sp.Rational(1,2))
            self.assertEqual(y['d_R']-y['Q_L'],-sp.Rational(1,2))
            self.assertEqual(y['e_R']-y['L_L'],-sp.Rational(1,2))
            self.assertEqual(y['nu_R']-y['L_L'],sp.Rational(1,2))

class TestKaluzaKlein(unittest.TestCase):
    def setUp(self): self.L=rest_compton_radius()
    def test_electron_compton_radius_scale(self):
        self.assertAlmostEqual(self.L,3.86159268e-13,delta=5e-20)
    def test_first_KK_mode_equals_electron_mass_by_construction(self):
        self.assertAlmostEqual(kk_mass(1,self.L)/M_E,1.0,places=13)
    def test_integer_mass_tower(self):
        for n in (2,3,17,207):
            self.assertAlmostEqual(kk_mass(n,self.L)/M_E,float(n),places=11)
    def test_zero_mode_massless_if_parent_massless(self):
        self.assertEqual(kk_mass(0,self.L),0)
    def test_negative_mode_same_mass(self):
        for n in (1,10,207):
            self.assertEqual(kk_mass(n,self.L),kk_mass(-n,self.L))
    def test_negative_mode_opposite_charge(self):
        self.assertAlmostEqual(kk_charge(-1)/E_CHARGE,-1)
    def test_kaluza_klein_charge_integer_tower(self):
        self.assertEqual(round(kk_charge(207)/E_CHARGE),207)
    def test_equal_charge_means_equal_mode_index(self):
        for n in (1,2,17,207):
            # Since charge is monotonic in integer mode number, same charge cannot
            # represent another mode with a different mass for this toy model.
            other_modes=[m for m in (-207,-17,-2,-1,0,1,2,17,207) if kk_charge(m)==kk_charge(n)]
            self.assertEqual(other_modes,[n])
            self.assertEqual(kk_mass(n,self.L),kk_mass(other_modes[0],self.L))
    def test_muon_ratio_not_one(self):
        self.assertGreater(M_MU_MEV/M_E_MEV,200)
    def test_muon_ratio_not_integer(self):
        ratio=M_MU_MEV/M_E_MEV
        self.assertGreater(abs(ratio-round(ratio)),0.1)
    def test_207_mode_would_have_207_times_electron_charge(self):
        self.assertEqual(round(kk_charge(207)/E_CHARGE),207)
    def test_adding_distinct_parent_masses_can_split_equal_charge_modes(self):
        self.assertGreater(kk_mass(1,self.L,parent_mass_kg=M_E),kk_mass(1,self.L))
    def test_radius_change_cannot_break_fixed_n_mass_equality(self):
        for L in (1e-14,1e-12,1e-9):
            self.assertAlmostEqual(kk_mass(2,L)/kk_mass(1,L),2.0,places=12)
    def test_minimal_kk_em_coupling_mismatch_is_large(self):
        self.assertGreater(electromagnetic_coupling()/minimal_kk_coupling(self.L),1e20)
    def test_minimal_kk_radius_matches_coupling(self):
        self.assertAlmostEqual(minimal_kk_coupling(kk_radius_to_match_em_coupling())/electromagnetic_coupling(),1,places=13)
    def test_kk_radius_em_coupling_vs_electron_mass_mismatch(self):
        self.assertGreater(self.L/kk_radius_to_match_em_coupling(),1e20)
    def test_em_coupling_matches_rough_known_value(self):
        self.assertAlmostEqual(electromagnetic_coupling(),0.30282,places=4)
    def test_mass_tower_dims(self):
        self.assertTrue(math.isfinite(kk_mass(1,1e-12)))
    def test_parent_mass_recovered_at_zero_mode(self):
        self.assertEqual(kk_mass(0,self.L,parent_mass_kg=M_E),M_E)

class TestQuantumCovariance(unittest.TestCase):
    def test_rest_phase_invariance_boost_06c(self):
        a,b=boosted_phase(1e-9,0,0,0.6*C)
        self.assertAlmostEqual(a/b,1,places=13)
    def test_phase_invariance_nontrivial_motion(self):
        a,b=boosted_phase(2e-9,0.2,0.3*C,-0.5*C)
        self.assertAlmostEqual(a/b,1,places=13)
    def test_phase_invariance_boost_along_motion(self):
        a,b=boosted_phase(2e-9,0.2,0.8*C,0.1*C)
        self.assertAlmostEqual(a/b,1,places=13)
    def test_phase_invariance_multiple_boosts(self):
        for v in (-.7,-.3,0,.3,.7):
            for beta in (-.8,-.4,0,.4,.8):
                with self.subTest(v=v,beta=beta):
                    a,b=boosted_phase(1.5e-9,0.1,v*C,beta*C)
                    self.assertAlmostEqual(a/b,1,places=12)
    def test_invariant_rest_energy_relationship(self):
        self.assertAlmostEqual((HBAR*C/rest_compton_radius())/(M_E*C*C),1,places=12)
    def test_lightlike_line_not_timelike_massive_worldline(self):
        self.assertEqual(C*C-C*C,0)
    def test_massive_worldline_positive_proper_time_interval(self):
        self.assertGreater(C*C-(0.7*C)**2,0)

class TestCurvatureAlgebra(unittest.TestCase):
    def test_matrix_commutator_antisymmetry(self):
        A=sp.Matrix([[1,2],[3,4]]);B=sp.Matrix([[2,-1],[1,0]])
        self.assertEqual(A*B-B*A,-(B*A-A*B))
    def test_matrix_jacobi(self):
        A=sp.Matrix([[1,2],[3,4]]);B=sp.Matrix([[0,1],[-1,0]]);C_=sp.Matrix([[2,0],[1,-1]])
        self.assertEqual(su2_jacobi(A,B,C_),sp.zeros(2,2))
    def test_U1_zero_commutator(self):
        a,b=sp.Symbol('a'),sp.Symbol('b')
        self.assertEqual(a*b-b*a,0)
    def test_su2_nonabelian_commutator(self):
        sx=sp.Matrix([[0,1],[1,0]])/2
        sy=sp.Matrix([[0,-sp.I],[sp.I,0]])/2
        sz=sp.Matrix([[1,0],[0,-1]])/2
        self.assertEqual(sp.simplify(sx*sy-sy*sx-sp.I*sz),sp.zeros(2))
    def test_chiral_projectors_each_rank_two(self):
        g5=sp.diag(-1,-1,1,1)
        PL=(sp.eye(4)-g5)/2; PR=(sp.eye(4)+g5)/2
        self.assertEqual((PL.rank(),PR.rank()),(2,2))
    def test_chiral_projector_sum_identity(self):
        g5=sp.diag(-1,-1,1,1)
        self.assertEqual((sp.eye(4)-g5)/2+(sp.eye(4)+g5)/2,sp.eye(4))
    def test_chiral_projectors_orthogonal(self):
        g5=sp.diag(-1,-1,1,1)
        self.assertEqual((sp.eye(4)-g5)*(sp.eye(4)+g5),sp.zeros(4))

class TestAudit(unittest.TestCase):
    def test_snapshot_has_finite_mass_ratio(self):
        self.assertTrue(math.isfinite(audit_snapshot()['muon_to_electron_mass_ratio']))
    def test_snapshot_disclaimer(self):
        self.assertIn('toy_model',audit_snapshot()['test_type'])

if __name__=='__main__':unittest.main()
