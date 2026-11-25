import unittest
import numpy as np
from src.quantum import *
class TestQuantum(unittest.TestCase):
 def test_normalization(self):self.assertAlmostEqual(np.trace(density(phases())).real,1)
 def test_hermitian(self):self.assertTrue(np.allclose(density(phases()),density(phases()).conj().T))
 def test_positive(self):self.assertGreaterEqual(np.linalg.eigvalsh(density(phases())).min(),-1e-13)
 def test_pure_formula(self):self.assertAlmostEqual(negativity(density(phases())),pure_negativity(phases()),places=12)
 def test_local_phase_invariance(self):
  p=phases();self.assertAlmostEqual(negativity(density(p)),negativity(density(p+np.array([.2,.8,.2,.8]))),places=12)
 def test_no_interaction(self):self.assertAlmostEqual(negativity(density([0,1,2,3])),0,places=12)
 def test_bell_max(self):self.assertAlmostEqual(negativity(density([0,0,0,np.pi])),.5,places=12)
 def test_dephase(self):self.assertAlmostEqual(negativity(density(phases(),0)),0,places=12)
 def test_classical_separable(self):self.assertAlmostEqual(negativity(classical_shared_phase_mixture()),0,places=12)
 def test_invalid_visibility(self):
  with self.assertRaises(ValueError):density(phases(),1.1)
 def test_time_scaling(self):self.assertAlmostEqual(delta_phase(phases(t=2)),2*delta_phase(phases()),places=10)
 def test_ppt_eigenvalues(self):self.assertTrue(np.all(np.linalg.eigvalsh(partial_transpose(classical_shared_phase_mixture()))>=-1e-12))
