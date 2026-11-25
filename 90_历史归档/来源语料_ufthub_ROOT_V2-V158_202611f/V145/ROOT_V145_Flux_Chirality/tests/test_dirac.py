import math,unittest
from root_v145.dirac_spectrum import (
 index,chiral_zero_modes,sphere_spectrum,first_massive_gap_per_length,
 holomorphic_basis_count,all_chiral_modes_for_6d_dirac)
class TestDirac(unittest.TestCase):
 def test_index_matches_charge_times_flux(self):
  for n in range(-7,8):
   for q in range(-3,4):
    with self.subTest(n=n,q=q):
     self.assertEqual(index(n,q),n*q)
 def test_index_integrality_required(self):
  with self.assertRaises(TypeError): index(2,.5)
 def test_zero_modes_chirality(self):
  self.assertEqual(chiral_zero_modes(3),(3,0))
  self.assertEqual(chiral_zero_modes(-3),(0,3))
  self.assertEqual(chiral_zero_modes(0),(0,0))
 def test_conjugate_charge_flips_index(self):
  for n in range(-5,6):
   self.assertEqual(index(n,2),-index(n,-2))
 def test_three_holomorphic_sections(self):
  self.assertEqual(holomorphic_basis_count(3),3)
  self.assertEqual(holomorphic_basis_count(-3),0)
 def test_spectrum_first_gap(self):
  self.assertAlmostEqual(sphere_spectrum(3,1,1)[1].eigenvalue_abs_per_length,2.0)
  self.assertAlmostEqual(sphere_spectrum(0,1,1)[0].eigenvalue_abs_per_length,1.0)
 def test_finite_flux_zero_degeneracies(self):
  for n in range(-7,8):
   levels=sphere_spectrum(n,1,3)
   z=[x for x in levels if x.zero_mode]
   self.assertEqual(sum(x.degeneracy_per_sign for x in z),abs(n))
 def test_excited_level_formula(self):
  for n in (-7,-3,-1,0,1,2,5):
   for level in sphere_spectrum(n,2.7,5):
    if level.level:
     self.assertAlmostEqual(level.eigenvalue_abs_per_length**2*2.7**2,
       level.level*(level.level+abs(n)),places=12)
     self.assertEqual(level.degeneracy_per_sign,abs(n)+2*level.level)
 def test_radius_spectrum_scale(self):
  for n in (-3,0,2):
   for k in range(1,4):
    x=sphere_spectrum(n,1,3)[k if n else k-1]
    y=sphere_spectrum(n,5,3)[k if n else k-1]
    self.assertAlmostEqual(x.eigenvalue_abs_per_length/y.eigenvalue_abs_per_length,5)
 def test_no_spurious_zero_without_flux(self):
  self.assertTrue(all(level.eigenvalue_abs_per_length>0 for level in sphere_spectrum(0,1,4)))
 def test_6d_dirac_vectorlike(self):
  for n in range(-5,6):
   self.assertEqual(all_chiral_modes_for_6d_dirac(n),(abs(n),abs(n)))
 def test_radius_invalid(self):
  with self.assertRaises(ValueError): sphere_spectrum(3,0)
  with self.assertRaises(ValueError): first_massive_gap_per_length(3,-1)
 def test_high_flux_gap_increases(self):
  vals=[first_massive_gap_per_length(n,1) for n in (0,1,2,3,5,9)]
  self.assertTrue(all(y>x for x,y in zip(vals,vals[1:])))
 def test_gap_with_charge_two(self):
  self.assertAlmostEqual(first_massive_gap_per_length(3,1,2),math.sqrt(7))
