import unittest
import math
from src.root_v66 import *

class TheoryChecks(unittest.TestCase):
    def test_cav_equals_tensor_if_decoupled(self):
        self.assertAlmostEqual(cavendish_massless_scalar_G(1,0),1/(8*math.pi))
    def test_cav_neq_tensor_if_scalar_exchange(self):
        self.assertGreater(cavendish_massless_scalar_G(1,.7),1/(8*math.pi))
    def test_gamma_gr(self):self.assertEqual(ppn_gamma_massless_scalar(1,0),1)
    def test_gamma_nonzero_slope(self):self.assertLess(ppn_gamma_massless_scalar(1,.1),1)
    def test_gamma_cassini_gr_passes(self):self.assertTrue(pass_cassini_toy(1,0))
    def test_gamma_cassini_large_scalar_fails(self):self.assertFalse(pass_cassini_toy(1,.1))
    def test_gamma_omega_bran_dicke(self):
        omega=40000.0
        fp=math.sqrt(1/omega)
        self.assertAlmostEqual(ppn_gamma_massless_scalar(1,fp),(omega+1)/(omega+2))
    def test_cav_bran_dicke(self):
        omega=3.0
        fp=math.sqrt(1/omega)
        ratio=cavendish_massless_scalar_G(1,fp)*8*math.pi
        self.assertAlmostEqual(ratio,(2*omega+4)/(2*omega+3))
    def test_cav_bad(self):
        with self.assertRaises(ValueError): cavendish_massless_scalar_G(-1,.1)
    def test_cassini_interval_contains_GR(self):
        lo,hi=cassini_illustrative_interval()
        self.assertTrue(lo<=1<=hi)

if __name__=='__main__':unittest.main()
