import unittest,math,dataclasses
import numpy as np
from src.bmv import *

class TestPhysics(unittest.TestCase):
 def setUp(self):self.p=Setup()
 def test_distances_symmetric(self):
  r=distances(self.p);self.assertAlmostEqual(r[0,0],self.p.d);self.assertAlmostEqual(r[1,1],self.p.d)
 def test_opposite_offsets(self):
  r=distances(self.p);self.assertAlmostEqual(r[0,1],self.p.d+self.p.s2/2+self.p.s1/2)
  self.assertAlmostEqual(r[1,0],self.p.d-self.p.s2/2-self.p.s1/2)
 def test_equal_branches_zero(self):
  p=dataclasses.replace(self.p,s1=0);self.assertAlmostEqual(cross_phase(phases(p)),0,places=13)
 def test_zero_time(self):self.assertEqual(cross_phase(phases(dataclasses.replace(self.p,t=0))),0)
 def test_mass_scaling(self):
  p=dataclasses.replace(self.p,m1=self.p.m1*2);self.assertAlmostEqual(cross_phase(phases(p))/cross_phase(phases(self.p)),2)
 def test_time_scaling(self):
  p=dataclasses.replace(self.p,t=2);self.assertAlmostEqual(cross_phase(phases(p))/cross_phase(phases(self.p)),2)
 def test_geometry_symmetry(self):
  p=dataclasses.replace(self.p,s1=self.p.s2,s2=self.p.s1);self.assertAlmostEqual(cross_phase(phases(p)),cross_phase(phases(self.p)))
 def test_radius_scale(self):
  p=dataclasses.replace(self.p,d=self.p.d*2,s1=self.p.s1*2,s2=self.p.s2*2);self.assertAlmostEqual(cross_phase(phases(p))/cross_phase(phases(self.p)),.5)
 def test_pure_state_norm(self):self.assertAlmostEqual(np.linalg.norm(pure_state(phases(self.p))),1)
 def test_pure_formula(self):self.assertAlmostEqual(negativity(density(self.p)),pure_concurrence(phases(self.p))/2,places=13)
 def test_local_phase_gauge(self):
  th=phases(self.p);a=np.array([[.1,-.2],[.1,-.2]]);b=np.array([[.3,.3],[-.4,-.4]])
  self.assertAlmostEqual(cross_phase(th+a+b),cross_phase(th))
  self.assertAlmostEqual(negativity(np.outer(pure_state(th+a+b),pure_state(th+a+b).conj())),negativity(density(self.p)))
 def test_pure_phase_pi(self):self.assertAlmostEqual(pure_concurrence(np.array([[math.pi,0],[0,0]])),1)
 def test_pure_phase_2pi(self):self.assertAlmostEqual(pure_concurrence(np.array([[2*math.pi,0],[0,0]])),0,places=14)
 def test_trace(self):self.assertAlmostEqual(np.trace(density(self.p)).real,1)
 def test_hermitian(self):self.assertTrue(np.allclose(density(self.p),density(self.p).conj().T))
 def test_positive(self):self.assertGreaterEqual(np.linalg.eigvalsh(density(self.p)).min(),-1e-14)
 def test_zero_dephasing_is_pure(self):self.assertAlmostEqual(linear_entropy(density(self.p)),0,places=13)
 def test_dephasing_reduces_entanglement(self):
  self.assertLessEqual(negativity(density(dataclasses.replace(self.p,gamma1=1,gamma2=1))),negativity(density(self.p))+1e-14)
 def test_complete_dephasing_approx(self):
  p=dataclasses.replace(self.p,gamma1=500,gamma2=500);self.assertLess(negativity(density(p)),1e-14)
 def test_only_gravity_zero_if_off(self):self.assertAlmostEqual(cross_phase(phases(self.p,gravity=False)),0)
 def test_only_coulomb_zero_if_q0(self):self.assertAlmostEqual(cross_phase(phases(self.p,gravity=False,coulomb=True)),0)
 def test_equal_coulomb_cancel(self):
  q=coulomb_equivalent_charge(self.p);p=dataclasses.replace(self.p,q1=q,q2=q)
  self.assertLess(np.max(np.abs(phases(p))),1e-12)
 def test_charge_sign_reverse(self):
  q=coulomb_equivalent_charge(self.p);p=dataclasses.replace(self.p,q1=q,q2=-q)
  self.assertAlmostEqual(cross_phase(phases(p))/cross_phase(phases(self.p)),2,places=12)
 def test_coefficient_finite_difference(self):
  coeff=mass_coefficient(self.p);self.assertAlmostEqual(coeff*G,cross_phase(phases(self.p)),places=12)
 def test_local_classical_channel(self):self.assertLess(negativity(classical_channel_state(self.p,64)),1e-12)
 def test_classical_channel_psd(self):self.assertGreater(np.linalg.eigvalsh(classical_channel_state(self.p,20)).min(),-1e-14)
 def test_invalid_overlap(self):
  with self.assertRaises(ValueError):distances(dataclasses.replace(self.p,d=1e-6))
 def test_invalid_gamma(self):
  with self.assertRaises(ValueError):density(dataclasses.replace(self.p,gamma1=-1))
 def test_invalid_nan(self):
  with self.assertRaises(ValueError):phases(dataclasses.replace(self.p,m1=math.nan))
 def test_no_negative_mass(self):
  with self.assertRaises(ValueError):phases(dataclasses.replace(self.p,m2=-1))
 def test_nonnegative_negativity(self):self.assertGreaterEqual(negativity(density(self.p)),0)
 def test_entanglement_local_unitaries(self):
  vec=pure_state(phases(self.p));rho=np.outer(vec,vec.conj());u1=np.diag(np.exp(1j*np.array([.6,-.7])));u2=np.diag(np.exp(1j*np.array([.1,-.2])));u=np.kron(u1,u2)
  self.assertAlmostEqual(negativity(u@rho@u.conj().T),negativity(rho),places=13)
 def test_mass_identifiability(self):
  p=dataclasses.replace(self.p,m1=self.p.m1*2,m2=self.p.m2/2)
  self.assertAlmostEqual(cross_phase(phases(p)),cross_phase(phases(self.p)))
 def test_interaction_entangled_at_nonzero_phase(self):self.assertGreater(negativity(density(self.p)),0)
 def test_simulate_outputs(self):self.assertEqual(simulate(self.p)['status'].split(' / ')[0],'SYNTHETIC')

if __name__=='__main__':unittest.main()
