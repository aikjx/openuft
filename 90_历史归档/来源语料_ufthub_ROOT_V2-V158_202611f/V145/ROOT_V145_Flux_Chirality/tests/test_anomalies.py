from fractions import Fraction as F
import unittest
from root_v145.anomalies import (
 SM_GEN,cubic_u1_anomaly,grav_u1_anomaly,su2_squared_u1_anomaly,
 su3_squared_u1_anomaly,su2_global_doublet_count,single_chiral_u1_anomalies,
 hypercharge_flux_index,family_flux_index)
class TestAnomalies(unittest.TestCase):
 def test_sm_cubic(self): self.assertEqual(cubic_u1_anomaly(),F(0))
 def test_sm_mixed_gravity(self): self.assertEqual(grav_u1_anomaly(),F(0))
 def test_sm_mixed_su2(self): self.assertEqual(su2_squared_u1_anomaly(),F(0))
 def test_sm_mixed_su3(self): self.assertEqual(su3_squared_u1_anomaly(),F(0))
 def test_su2_global_even(self): self.assertEqual(su2_global_doublet_count()%2,0)
 def test_sm_hypercharges(self):
  self.assertEqual(SM_GEN['Q_L'][2],F(1,6))
  self.assertEqual(SM_GEN['u_L_conj'][2],F(-2,3))
  self.assertEqual(SM_GEN['d_L_conj'][2],F(1,3))
  self.assertEqual(SM_GEN['L_L'][2],F(-1,2))
  self.assertEqual(SM_GEN['e_L_conj'][2],F(1))
 def test_single_flux3_anomalous(self):
  self.assertEqual(single_chiral_u1_anomalies(3),{'cubic':3,'mixed_gravity':3})
 def test_single_flux_negative_charge(self):
  self.assertEqual(single_chiral_u1_anomalies(3,-1),{'cubic':3,'mixed_gravity':3})
 def test_three_generation_replication_still_anomaly_free(self):
  self.assertEqual(3*cubic_u1_anomaly(),0)
  self.assertEqual(3*grav_u1_anomaly(),0)
 def test_hypercharge_flux_nonuniform(self):
  x=hypercharge_flux_index(3)
  self.assertEqual(x,{'Q_L':3,'u_L_conj':-12,'d_L_conj':6,'L_L':-9,'e_L_conj':18})
  self.assertEqual(len(set(map(abs,x.values()))),5)
 def test_family_charge_uniform(self):
  self.assertEqual(set(family_flux_index(3).values()),{3})
 def test_nonzero_flux_not_automatically_anomaly_free(self):
  for n in (1,3,7):
   self.assertNotEqual(single_chiral_u1_anomalies(n)['cubic'],0)
 def test_hypercharge_integer_normalization(self):
  self.assertEqual(set(int(6*y) for _,_,y in SM_GEN.values()),{1,-4,2,-3,6})
