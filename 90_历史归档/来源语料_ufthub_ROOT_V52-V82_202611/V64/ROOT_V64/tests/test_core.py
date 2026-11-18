"""No physical discovery claim; tests only verify implementation and conditional math."""
import math, unittest, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from src import root_v64 as p

class HelixTests(unittest.TestCase):
 def test_velocity_magnitude(self):
  for a in (0,5,30,45,60,89,90):
   h=p.helix(2,a,201)
   for t in (0,.1,1.5):self.assertAlmostEqual(p.norm(h.velocity(t))/201,1.,places=13)
 def test_curvature(self):
  h=p.helix(2,30,10);self.assertAlmostEqual(h.curvature,.375)
 def test_torsion(self):
  h=p.helix(2,30,10);self.assertAlmostEqual(h.torsion,math.sqrt(3)/8)
 def test_acceleration(self):
  h=p.helix(2,30,10);self.assertAlmostEqual(p.norm(h.acceleration(.3)),37.5)
 def test_orthogonality(self):
  h=p.helix(.5,60,5)
  for t in (0,.4,1):
   T,N,B=h.frame(t)
   for v,w in ((T,N),(T,B),(N,B)):self.assertAlmostEqual(p.dot(v,w),0,places=13)
   for v in (T,N,B):self.assertAlmostEqual(p.norm(v),1.,places=13)
 def test_straight_frame_undefined(self):
  with self.assertRaises(ValueError):p.helix(1,90,10).frame(0)
 def test_invalid(self):
  for args in ((-1,30,5),(1,-3,5),(1,30,0),(1,91,1)):
   with self.assertRaises(ValueError):p.helix(*args)
 def test_helix_plus_c_is_superluminal(self):
  self.assertGreater(math.hypot(0.1*p.C,p.C),p.C)
 def test_three_forces_not_perpendicular(self):
  fg=(0,0,-1);fe=(0,0,-2);self.assertEqual(p.dot(fg,fe),2)
 def test_magnetic_perpendicular_v_B(self):
  v=(2,3,4);B=(5,7,11);f=p.cross(v,B)
  self.assertAlmostEqual(p.dot(v,f),0);self.assertAlmostEqual(p.dot(B,f),0)
 def test_zero_charge_magnetic(self):
  self.assertEqual(p.vec_scale(p.cross((1,2,3),(4,5,6)),0.),(0.,0.,0.))

class WaveTests(unittest.TestCase):
 def setUp(self):self.m=p.HelicalKGMode()
 def test_root_boundary(self):self.assertLess(abs(p.j_integer(1,p.J11)),1e-12)
 def test_bessel_origin(self):self.assertEqual(p.j_integer(1,0),0)
 def test_bessel_recurrence(self):
  for x in (.2,1.4,3.6):self.assertAlmostEqual(p.j_integer(0,x)+p.j_integer(2,x),2*p.j_integer(1,x)/x,places=12)
 def test_dispersion(self):self.assertAlmostEqual(self.m.omega**2,self.m.k**2+self.m.mu**2+self.m.q**2,places=12)
 def test_wave_boundary(self):self.assertLess(abs(self.m.f(self.m.a)),1e-12)
 def test_radial_residual(self):
  for r in (.1,.33,.61,.89):self.assertLess(abs(self.m.radial_residual(r))/self.m.q**2,3e-8)
 def test_energy_positive(self):
  for r in (.1,.3,.5,.9):self.assertGreater(self.m.energy_density(r),0)
 def test_integrated_energy_identity(self):
  _,_,E=p.integrate_radial(self.m,samples=12000)
  self.assertAlmostEqual(E/self.m.energy_per_length_exact(),1,places=7)
 def test_radial_fraction_monotonic(self):
  _,fs,_=p.integrate_radial(self.m,1000)
  self.assertTrue(all(0<=a<=b<=1.00000001 for a,b in zip(fs,fs[1:])))
 def test_mode_group_vz_sub_c(self):self.assertLess(abs(self.m.axial_group_speed),1.)
 def test_energy_amplitude_squared(self):
  a=p.HelicalKGMode(amplitude=2.0)
  self.assertAlmostEqual(a.energy_per_length_exact()/self.m.energy_per_length_exact(),4)
 def test_mass_increases_frequency(self):
  self.assertGreater(p.HelicalKGMode(mu=3).omega,self.m.omega)
 def test_n_zero_not_supported(self):self.assertEqual(self.m.n,1)
 def test_line_gauss_law_outside(self):
  for r in (.2,.6,3): self.assertAlmostEqual(p.line_gravity(10,r)*r,2*p.G_OBS*10,places=20)
 def test_line_mass_scaling(self):self.assertAlmostEqual(p.line_gravity(20,.5),2*p.line_gravity(10,.5))
 def test_line_not_inverse_square(self):
  self.assertAlmostEqual(p.line_gravity(10,.5)/p.line_gravity(10,1),2)
 def test_inside_less_than_full(self):
  self.assertLess(p.line_gravity(10,.1,.25),p.line_gravity(10,.1,1))

class InducedGTests(unittest.TestCase):
 def test_planck_length(self):self.assertAlmostEqual(p.planck_length()/1.616255e-35,1,places=6)
 def test_cutoff_roundtrip(self):
  for E in (1e-21,1,1e9): self.assertAlmostEqual(p.cutoff_energy(p.cutoff_length(E))/E,1,places=12)
 def test_mass_factor_0(self):self.assertEqual(p.proper_time_factor(0),1)
 def test_mass_factor_monotonic(self):
  vals=[p.proper_time_factor(a) for a in (0,.1,.3,1,2,4)]
  self.assertTrue(all(a>b for a,b in zip(vals,vals[1:])))
 def test_factor_large_suppression(self):self.assertLess(p.proper_time_factor(5),1e-11)
 def test_factor_small_near_unity(self):self.assertGreater(p.proper_time_factor(.001),.9999)
 def test_scalar_induced_fit_not_prediction(self):
  ell=p.inverse_fit_length()
  self.assertAlmostEqual(p.inverse_G_induced(1,ell)*p.G_OBS,1,places=13)
 def test_field_count_scale_degeneracy(self):
  ell=p.planck_length()
  self.assertAlmostEqual(p.inverse_G_induced(1,ell)/p.inverse_G_induced(4,2*ell),1,places=14)
 def test_xi_conformal_zero(self):self.assertAlmostEqual(p.inverse_G_induced(1,1e-35,1/6),0,places=10)
 def test_negative_coefficient(self):self.assertLess(p.inverse_G_induced(1,1e-35,.25),0)
 def test_bare_cancellation(self):
  ell=1e-35;target=1/p.G_OBS
  correction=p.inverse_G_induced(1,ell)
  self.assertAlmostEqual(p.inverse_G_induced(1,ell,bare_inverse_G=target-correction)/target,1,places=14)
 def test_cutoff_power(self):
  self.assertAlmostEqual(p.inverse_G_induced(1,1e-35)/p.inverse_G_induced(1,2e-35),4,places=14)
 def test_mu_influences_G(self):self.assertLess(p.inverse_G_induced(1,1e-35,mu=2),p.inverse_G_induced(1,1e-35,mu=0))
 def test_negative_bare_parameter_allowed(self):self.assertLess(p.inverse_G_induced(1,1e-35,bare_inverse_G=-1e44),0)
 def test_invalid(self):
  with self.assertRaises(ValueError):p.inverse_G_induced(0,1)
  with self.assertRaises(ValueError):p.inverse_G_induced(1,0)
  with self.assertRaises(ValueError):p.inverse_fit_length(xi=.2)
 def test_dimensional_obstruction_c_hbar(self):
  # mass power fixes hbar^-1, time fixes c^3, then length exponent equals 1 not 3.
  b=-1;a=2-b
  self.assertNotEqual(a+2*b,3)
 def test_alpha_guess_is_not_exact(self):self.assertGreater(abs(p.bad_alpha_guess()/p.ALPHA_OBS-1),1e-6)
 def test_proton_mass_ratio_guess_false(self):self.assertLess(p.bad_mass_ratio_guess(),200)

class YukawaAndGRTests(unittest.TestCase):
 def test_fifth_force_zero_coupling(self):self.assertEqual(p.yukawa_g_ratio(0,3,5),0)
 def test_fifth_force_short_range(self):self.assertLess(abs(p.yukawa_g_ratio(1,100,1)),1e-30)
 def test_fifth_force_sign(self):self.assertLess(p.yukawa_g_ratio(-1,.1,1),0)
 def test_yukawa_gradient(self):
  r=3.; h=1e-4;G=p.G_OBS
  dV=(p.yukawa_potential(.2,r+h,2)-p.yukawa_potential(.2,r-h,2))/(2*h)
  gr=G/r**2*(1+p.yukawa_g_ratio(.2,r,2))
  self.assertAlmostEqual(dV/gr,1.,places=8)
 def test_yukawa_at_zero(self):self.assertAlmostEqual(p.yukawa_g_ratio(.1,0,2),.1)
 def test_lorentz_interval(self):
  a,b=4.,2.
  for beta in (-.9,-.2,.0,.7,.99):
   aa,bb=p.lorentz_boost(a,b,beta)
   self.assertAlmostEqual((aa*aa-bb*bb)/(a*a-b*b),1,places=12)
 def test_invalid_boost(self):
  with self.assertRaises(ValueError):p.lorentz_boost(1,1,1)
 def test_microscope_constraint_not_assumed_universal(self):
  eta_mean=-1.5e-15; sigma=math.hypot(2.3e-15,1.5e-15)
  self.assertGreater(sigma,2.7e-15)
  self.assertLess(abs(eta_mean)/sigma,1)

class GaugeAndFieldTests(unittest.TestCase):
 def test_su2_nonabelian(self):
  residual,nonzero=p.su2_commutator();self.assertLess(residual,1e-14);self.assertGreater(nonzero,1)
 def test_maxwell_orientation(self):
  E,B=p.maxwell_plane_wave(.25,0,5,1)
  P=p.cross(E,B)
  self.assertGreaterEqual(P[2],0)
  self.assertAlmostEqual(p.norm(E)/(p.C*p.norm(B)),1)
 def test_maxwell_vacuum_faraday(self):
  a=100.;lam=3.;z=.25;t=.0000000001
  dz=lam*1e-6;dt=lam/p.C*1e-6
  E1,_=p.maxwell_plane_wave(z+dz,t,a,lam)
  E0,_=p.maxwell_plane_wave(z-dz,t,a,lam)
  _,B1=p.maxwell_plane_wave(z,t+dt,a,lam)
  _,B0=p.maxwell_plane_wave(z,t-dt,a,lam)
  curlEx=-(E1[1]-E0[1])/(2*dz)
  minus_dtBx=-(B1[0]-B0[0])/(2*dt)
  self.assertLess(abs(curlEx-minus_dtBx)/max(1,abs(curlEx)),3e-9)
 def test_maxwell_amperes_law(self):
  a=100.;lam=3.;z=.25;t=.0000000001
  dz=lam*1e-6;dt=lam/p.C*1e-6
  _,B1=p.maxwell_plane_wave(z+dz,t,a,lam)
  _,B0=p.maxwell_plane_wave(z-dz,t,a,lam)
  E1,_=p.maxwell_plane_wave(z,t+dt,a,lam)
  E0,_=p.maxwell_plane_wave(z,t-dt,a,lam)
  curlBy=(B1[0]-B0[0])/(2*dz)
  dtEy=(E1[1]-E0[1])/(2*dt*p.C**2)
  self.assertLess(abs(curlBy-dtEy)/max(1e-12,abs(curlBy)),3e-9)
 def test_nonminimal_scalar_positive(self):self.assertGreater(p.scalar_tensor_effective_M2(1,.1,.5),0)
 def test_nonminimal_scalar_negative_not_allowed(self):self.assertLess(p.scalar_tensor_effective_M2(1,.7,1),0)
 def test_scalar_tensor_zero_coupling(self):self.assertEqual(p.scalar_tensor_effective_M2(10,0,12),10)
 def test_opposite_charge_force_same_trajectory(self):
  E=(0,1,0);self.assertEqual(p.vec_scale(E,1),(0,1,0));self.assertEqual(p.vec_scale(E,-1),(0,-1,0))
 def test_maxwell_bad_wavelength(self):
  with self.assertRaises(ValueError):p.maxwell_plane_wave(0,0,2,0)

if __name__=='__main__':unittest.main()
