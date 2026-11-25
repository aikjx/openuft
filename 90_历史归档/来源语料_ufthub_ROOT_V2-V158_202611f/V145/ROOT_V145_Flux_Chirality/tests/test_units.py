import math,unittest
from root_v145.units import dirac_gap_gev,gap_mass_kg,HBAR_SI,C_SI,EV_J
class TestUnits(unittest.TestCase):
 def test_gap_n3_1am(self):
  self.assertAlmostEqual(dirac_gap_gev(3,1e-18),394.65396,delta=.0001)
 def test_gap_scales_inverse_radius(self):
  self.assertAlmostEqual(dirac_gap_gev(3,1e-18)/dirac_gap_gev(3,2e-18),2)
 def test_hbar_c_conversion(self):
  self.assertAlmostEqual(HBAR_SI*C_SI/(EV_J*1e9*1e-15),.1973269804,delta=1e-8)
 def test_restored_c_mass_energy_equivalence(self):
  m=gap_mass_kg(3,1e-18)
  e=dirac_gap_gev(3,1e-18)*1e9*EV_J
  self.assertAlmostEqual(m*C_SI*C_SI/e,1,places=14)
 def test_negative_radius_rejected(self):
  with self.assertRaises(ValueError): dirac_gap_gev(3,0)
  with self.assertRaises(ValueError): gap_mass_kg(3,-1)
 def test_charge_changes_gap(self):
  self.assertAlmostEqual(dirac_gap_gev(3,1e-18,2)/dirac_gap_gev(3,1e-18),math.sqrt(7/4))
