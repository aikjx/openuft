import cmath, math, unittest
from root_v145.monopole import (
 a_north_phi,a_south_phi,f_theta_phi,transition_phase, analytical_flux,
 simpson_flux,chern_number,section_norm_squared,section_norm_squared_simpson)
class TestMonopole(unittest.TestCase):
 def test_quantized_integer(self):
  for n in range(-8,9):
   with self.subTest(n=n): self.assertEqual(chern_number(n),n)
 def test_noninteger_rejected(self):
  with self.assertRaises(TypeError): chern_number(0.25)
 def test_patch_difference(self):
  for n in (-5,-2,0,1,3,7):
   for theta in (0.3,1.0,2.2):
    with self.subTest(n=n,theta=theta):
     self.assertAlmostEqual(a_north_phi(theta,n)-a_south_phi(theta,n),n,places=13)
 def test_patch_local_regular(self):
  self.assertAlmostEqual(a_north_phi(0,3),0)
  self.assertAlmostEqual(a_south_phi(math.pi,3),0)
 def test_transition_phase_periodic(self):
  for n in range(-7,8):
   for phi in (.1,2.3,5.4):
    with self.subTest(n=n,phi=phi):
     self.assertLess(abs(transition_phase(phi+2*math.pi,n)-transition_phase(phi,n)),3e-14)
 def test_nonintegral_transition_not_single_valued(self):
  phi=0.4
  self.assertGreater(abs(cmath.exp(1j*.5*(phi+2*math.pi))-cmath.exp(1j*.5*phi)),1.9)
 def test_field_is_potential_derivative(self):
  h=1e-6
  for n in (-3,1,5):
   for theta in (.6,1.6,2.6):
    derivative=(a_north_phi(theta+h,n)-a_north_phi(theta-h,n))/(2*h)
    self.assertAlmostEqual(derivative,f_theta_phi(theta,n),delta=2e-9)
 def test_flux_simpson(self):
  for n in range(-8,9):
   with self.subTest(n=n):
    self.assertAlmostEqual(simpson_flux(n),analytical_flux(n),delta=2e-11)
 def test_flux_wrong_simpson_steps(self):
  for steps in (0,1,3,5,-2):
   with self.assertRaises(ValueError): simpson_flux(3,steps)
 def test_zero_flux(self):
  self.assertEqual(simpson_flux(0),0)
 def test_norm_exact_n3(self):
  a=[section_norm_squared(3,k)/(4*math.pi) for k in range(3)]
  self.assertAlmostEqual(a[0],1/3,places=12)
  self.assertAlmostEqual(a[1],1/6,places=12)
  self.assertAlmostEqual(a[2],1/3,places=12)
 def test_norm_numeric_agrees(self):
  for n in range(1,8):
   for k in range(n):
    with self.subTest(n=n,k=k):
     self.assertAlmostEqual(section_norm_squared(n,k),section_norm_squared_simpson(n,k),delta=1e-10)
 def test_norm_radius_scales_area(self):
  for k in range(3):
   self.assertAlmostEqual(section_norm_squared(3,k,2),4*section_norm_squared(3,k,1))
 def test_norm_outside_basis(self):
  for n,k in ((0,0),(2,2),(-1,0),(3,-1)):
   with self.assertRaises(ValueError): section_norm_squared(n,k)
