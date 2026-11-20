import unittest
import numpy as np
from src.holonomy import (
 I2, SIGMA_X, SIGMA_Y, SIGMA_Z, su2_rotation, su2_holonomy,
 su2_closed_form,su2_wilson_trace,su3_closed_form,su3_wilson_trace,
 su3_embed, matrix_commutator, u1_wilson_commutator,
 conjugated_wilson_trace,small_loop_ratio)

class HolonomyTests(unittest.TestCase):
 def test_su2_identity(self):self.assertTrue(np.allclose(su2_holonomy(0,0),I2))
 def test_su2_x_unitary(self):
  u=su2_rotation(.41,'x');self.assertTrue(np.allclose(u@u.conj().T,I2))
 def test_su2_y_unitary(self):
  u=su2_rotation(.41,'y');self.assertTrue(np.allclose(u@u.conj().T,I2))
 def test_su2_z_unitary(self):
  u=su2_rotation(.41,'z');self.assertTrue(np.allclose(u@u.conj().T,I2))
 def test_pauli_x_square(self):self.assertTrue(np.allclose(SIGMA_X@SIGMA_X,I2))
 def test_pauli_y_square(self):self.assertTrue(np.allclose(SIGMA_Y@SIGMA_Y,I2))
 def test_pauli_z_square(self):self.assertTrue(np.allclose(SIGMA_Z@SIGMA_Z,I2))
 def test_pauli_noncommutation(self):self.assertTrue(np.allclose(SIGMA_X@SIGMA_Y-SIGMA_Y@SIGMA_X,2j*SIGMA_Z))
 def test_u1_commutes(self):self.assertAlmostEqual(abs(u1_wilson_commutator(.13,.49)-1),0,places=13)
 def test_su2_rotation_det(self):self.assertAlmostEqual(np.linalg.det(su2_rotation(.83,'x')).real,1,places=13)
 def test_su3_embed_det(self):self.assertAlmostEqual(np.linalg.det(su3_embed(su2_rotation(.83,'x'))).real,1,places=13)
 def test_su2_wilson_closed_form(self):self.assertAlmostEqual(su2_wilson_trace(.35,.6),su2_closed_form(.35,.6),places=14)
 def test_su3_wilson_closed_form(self):self.assertAlmostEqual(su3_wilson_trace(.35,.6),su3_closed_form(.35,.6),places=14)
 def test_su2_special_pi2(self):self.assertAlmostEqual(su2_wilson_trace(np.pi/2,np.pi/2),-1,places=12)
 def test_su3_special_pi2(self):self.assertAlmostEqual(su3_wilson_trace(np.pi/2,np.pi/2),-1/3,places=12)
 def test_su2_zero_alpha(self):self.assertAlmostEqual(su2_wilson_trace(0,.7),1,places=13)
 def test_su2_zero_beta(self):self.assertAlmostEqual(su2_wilson_trace(.7,0),1,places=13)
 def test_su2_parallel_axes_commute(self):
  u=su2_rotation(.2,'x');v=su2_rotation(.4,'x');self.assertTrue(np.allclose(matrix_commutator(u,v),I2))
 def test_su2_antihermitian_generators(self):
  A=1j*SIGMA_X;self.assertTrue(np.allclose(A.conj().T,-A))
 def test_su2_commutator_unitary(self):
  w=su2_holonomy(.36,.77);self.assertTrue(np.allclose(w@w.conj().T,I2))
 def test_su2_commutator_det(self):self.assertAlmostEqual(np.linalg.det(su2_holonomy(.36,.77)).real,1,places=12)
 def test_conjugation_trace_invariant(self):self.assertAlmostEqual(conjugated_wilson_trace(.36,.77),su2_wilson_trace(.36,.77),places=13)
 def test_conjugation_trace_invariant_second(self):self.assertAlmostEqual(conjugated_wilson_trace(.36,.77,1.17),su2_wilson_trace(.36,.77),places=13)
 def test_su2_real_trace(self):self.assertAlmostEqual(np.trace(su2_holonomy(.7,.9)).imag,0,places=12)
 def test_su3_range(self):self.assertGreaterEqual(su3_wilson_trace(.7,.9),-1/3-1e-12)
 def test_su2_range(self):self.assertGreaterEqual(su2_wilson_trace(.7,.9),-1-1e-12)
 def test_small_loop_leading(self):
  got,expect=small_loop_ratio(1e-4);self.assertLess(np.linalg.norm(got-expect),1e-3)
 def test_small_loop_converges(self):
  large=np.linalg.norm(small_loop_ratio(.05)[0]-small_loop_ratio(.05)[1])
  small=np.linalg.norm(small_loop_ratio(.025)[0]-small_loop_ratio(.025)[1])
  self.assertLess(small,large)
 def test_trace_SU3_relation_to_SU2(self):
  a,b=.44,.6;self.assertAlmostEqual(su3_wilson_trace(a,b),(2*su2_wilson_trace(a,b)+1)/3,places=13)
 def test_repeated_samples(self):
  for a in (.1,.5,1.1):
   for b in (.2,.8,1.3):
    with self.subTest(a=a,b=b):self.assertAlmostEqual(su2_wilson_trace(a,b),su2_closed_form(a,b),places=13)
 def test_angles_negative_formula(self):self.assertAlmostEqual(su2_wilson_trace(-.35,.6),su2_closed_form(.35,.6),places=13)
 def test_angles_period_pi_formula(self):self.assertAlmostEqual(su2_wilson_trace(.35+np.pi,.6),su2_wilson_trace(.35,.6),places=13)
