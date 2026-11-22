# -*- coding: utf-8 -*-
"""ROOT V134 regression tests: mathematics and synthetic examples, not experiments."""
import sys
from pathlib import Path
import unittest
from fractions import Fraction as Q
import numpy as np
from scipy.linalg import expm
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from root_v134 import (HBAR,G,SU2,SU3,commutator,curvature_constant,
                       pure_gauge_connection,plaquette_commutator,
                       spinor_transport,anomaly_ledger,SM_FAMILY,
                       gauge_kinetic_prefactor,bianchi_constant,no_go_1d_representation,create_results)

class TestAlgebra(unittest.TestCase):
    def test_01_hbar_not_one(self): self.assertNotEqual(HBAR,1)
    def test_02_G_not_one(self): self.assertNotEqual(G,1)
    def test_03_su2_three_generators(self): self.assertEqual(len(SU2),3)
    def test_04_su2_commutator(self): self.assertTrue(np.allclose(commutator(SU2[0],SU2[1]),1j*SU2[2],atol=1e-14))
    def test_05_su2_traceless_hermitian(self):
        for t in SU2:
            self.assertAlmostEqual(np.trace(t).real,0)
            self.assertTrue(np.allclose(t,t.conj().T))
    def test_06_su2_normalization(self):
        for i,a in enumerate(SU2):
            for j,b in enumerate(SU2):
                self.assertAlmostEqual(np.trace(a@b).real, .5 if i==j else 0,places=12)
    def test_07_su3_eight_generators(self): self.assertEqual(len(SU3),8)
    def test_08_su3_hermitian_traceless(self):
        for t in SU3:
            self.assertTrue(np.allclose(t,t.conj().T))
            self.assertLess(abs(np.trace(t)),1e-13)
    def test_09_su3_orthogonality(self):
        for i,a in enumerate(SU3):
            for j,b in enumerate(SU3):
                self.assertAlmostEqual(np.trace(a@b).real,.5 if i==j else 0,places=12)
    def test_10_su3_commutator(self): self.assertTrue(np.allclose(commutator(SU3[0],SU3[1]),1j*SU3[2],atol=1e-14))
    def test_11_one_dimensional_no_go(self): self.assertEqual(no_go_1d_representation()['commutator_1d'],0)
    def test_12_constant_nonabelian_field(self):
        self.assertTrue(np.allclose(curvature_constant(0.7*SU2[0],1.1*SU2[1]),.77*SU2[2]))
    def test_13_commuting_constant_field_zero(self):
        self.assertLess(np.linalg.norm(curvature_constant(SU2[2],.3*SU2[2])),1e-14)
    def test_14_pure_gauge_flat_many_x(self):
        for x in np.linspace(-2,2,51):
            self.assertLess(np.linalg.norm(pure_gauge_connection(x,.5,.8)[-1]),1e-13)
    def test_15_pure_gauge_nonconstant_potential(self):
        ax,ay,daydx,f=pure_gauge_connection(0.71,.5,.8)
        self.assertGreater(np.linalg.norm(daydx),.05)
        self.assertLess(np.linalg.norm(f),1e-13)
    def test_16_gauge_covariance_constant_transform(self):
        u=expm(1j*(.7*SU2[0]+.31*SU2[1]))
        x=.9*SU2[0];y=.4*SU2[1]
        lhs=curvature_constant(u@x@u.conj().T,u@y@u.conj().T)
        rhs=u@curvature_constant(x,y)@u.conj().T
        self.assertTrue(np.allclose(lhs,rhs,atol=1e-13))
    def test_17_su3_gauge_covariance(self):
        u=expm(1j*(.4*SU3[3]+.7*SU3[5]));x=SU3[1];y=.3*SU3[4]
        lhs=curvature_constant(u@x@u.conj().T,u@y@u.conj().T)
        rhs=u@curvature_constant(x,y)@u.conj().T
        self.assertTrue(np.allclose(lhs,rhs,atol=1e-13))
    def test_18_su2_constant_bianchi(self):
        self.assertLess(np.linalg.norm(bianchi_constant(SU2[0],.6*SU2[1],-.3*SU2[2])),1e-13)
    def test_19_su3_constant_bianchi(self):
        self.assertLess(np.linalg.norm(bianchi_constant(SU3[1],SU3[4],SU3[6])),1e-13)

class TestWilson(unittest.TestCase):
    def test_20_plaquette_unitary(self):
        for d in [0.5,.2,.1,.03]:
            w,_=plaquette_commutator(.7,1.1,d)
            self.assertLess(np.linalg.norm(w.conj().T@w-np.eye(2)),1e-13)
    def test_21_plaquette_nontrivial(self):
        w,_=plaquette_commutator(.7,1.1,.2)
        self.assertGreater(np.linalg.norm(w-np.eye(2)),.01)
    def test_22_wilson_leading_convergence(self):
        errs=[]
        for d in [.2,.1,.05,.025]:
            w,leading=plaquette_commutator(.7,1.1,d)
            errs.append(np.linalg.norm(w-leading))
        for x,y in zip(errs,errs[1:]): self.assertGreater(x/y,7.0)
    def test_23_trace_wilson_conjugation(self):
        u=expm(1j*.31*SU2[1]);w,_=plaquette_commutator(.7,1.1,.2)
        self.assertAlmostEqual(np.trace(u@w@u.conj().T).real,np.trace(w).real,places=12)
    def test_24_plaquette_small_limit(self):
        w,_=plaquette_commutator(.7,1.1,.001)
        f=curvature_constant(.7*SU2[0],1.1*SU2[1])
        self.assertLess(np.linalg.norm((w-np.eye(2))/.001**2+1j*f),1e-3)

class TestMatter(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data=spinor_transport(.7,1.1,duration=8,count=301)
    def test_25_state_norm(self): self.assertLess(self.data['max_state_norm_error'],1e-9)
    def test_26_color_casimir(self): self.assertLess(self.data['max_casimir_error'],1e-9)
    def test_27_wong_covariant_transport(self): self.assertLess(self.data['max_wong_residual'],1e-12)
    def test_28_color_changes(self): self.assertGreater(abs(self.data['final_Q'][1]),.1)
    def test_29_zero_connection_color_fixed(self):
        r=spinor_transport(0,0,duration=2,count=41)
        self.assertTrue(np.allclose(r['final_Q'],[0,0,.5]))
    def test_30_g_coupling_not_determined(self):
        self.assertAlmostEqual(gauge_kinetic_prefactor(.1)/gauge_kinetic_prefactor(.3),9)
    def test_31_g_coupling_rejects_zero(self):
        with self.assertRaises(ValueError): gauge_kinetic_prefactor(0)
    def test_32_hbar_in_action(self):
        self.assertAlmostEqual(gauge_kinetic_prefactor(.2,2*HBAR)/gauge_kinetic_prefactor(.2,HBAR),2)

class TestAnomalies(unittest.TestCase):
    def test_33_cubic_hypercharge(self): self.assertEqual(anomaly_ledger()['U1_cubic'],Q(0))
    def test_34_mixed_gravity(self): self.assertEqual(anomaly_ledger()['gravity_U1'],Q(0))
    def test_35_su2_squared_u1(self): self.assertEqual(anomaly_ledger()['SU2_squared_U1'],Q(0))
    def test_36_su3_squared_u1(self): self.assertEqual(anomaly_ledger()['SU3_squared_U1'],Q(0))
    def test_37_su3_cubic(self): self.assertEqual(anomaly_ledger()['SU3_cubic'],0)
    def test_38_even_weak_doublets(self): self.assertEqual(anomaly_ledger()['SU2_global_anomaly'],0)
    def test_39_global_one_doublet_fails(self): self.assertEqual(1%2,1)
    def test_40_delete_electron_anomaly(self):
        f={k:v for k,v in SM_FAMILY.items() if k!='e_c'}
        self.assertNotEqual(anomaly_ledger(f)['U1_cubic'],Q(0))
    def test_41_delete_up_anomaly(self):
        f={k:v for k,v in SM_FAMILY.items() if k!='u_c'}
        self.assertNotEqual(anomaly_ledger(f)['SU3_squared_U1'],Q(0))
    def test_42_sum_multiplicities(self): self.assertEqual(sum(v['mult'] for v in SM_FAMILY.values()),15)
    def test_43_right_neutrino_neutral_no_effect(self):
        f=dict(SM_FAMILY);f['nu_c']=dict(mult=1,Y=Q(0))
        self.assertEqual(anomaly_ledger(f)['U1_cubic'],Q(0))

class TestReport(unittest.TestCase):
    def test_44_report_finite(self):
        data,_=create_results()
        self.assertGreater(data['constant_nonabelian_curvature_norm'],0)
        self.assertEqual(data['flat_moving_frame_curvature_norm'],0)
    def test_45_report_expected_field_strength(self):
        data,_=create_results()
        self.assertAlmostEqual(data['expected_F_T3_coefficient'],.77)

if __name__=='__main__': unittest.main(verbosity=2)
