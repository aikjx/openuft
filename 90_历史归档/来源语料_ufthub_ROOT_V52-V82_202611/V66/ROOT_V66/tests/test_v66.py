"""Unit tests check implementation of hypotheses and known identities, NOT nature."""
import math
import unittest
from src import root_v66 as M


class CoreTests(unittest.TestCase):
    def test_constants_c(self): self.assertEqual(M.C,299792458.)
    def test_constants_h(self): self.assertEqual(M.H,6.62607015e-34)
    def test_alpha_observed(self): self.assertAlmostEqual(M.ALPHA_2022,7.2973525643e-3)
    def test_unit_cutoff(self): self.assertAlmostEqual(M.cutoff_length_from_energy(M.HBAR*M.C),1.0)
    def test_cutoff_electronvolt(self): self.assertAlmostEqual(M.cutoff_length_from_energy(M.E),1.9732698046e-7,delta=2e-16)
    def test_helix_zero(self):
        h=M.helix_from_radius_pitch(2.,0.,3.)
        self.assertAlmostEqual(h.kappa,.5)
        self.assertAlmostEqual(h.tau,0)
        self.assertAlmostEqual(h.axial_speed,0)
    def test_helix_pitch45(self):
        h=M.helix_from_radius_pitch(2.,math.pi/4,3.)
        self.assertAlmostEqual(h.kappa,.25)
        self.assertAlmostEqual(h.tau,.25)
    def test_helix_speed(self):
        h=M.helix_from_radius_pitch(2.,.32,2.)
        self.assertAlmostEqual(M.norm(h.velocity(.82)),2.)
    def test_helix_accel(self):
        h=M.helix_from_radius_pitch(3.,.2,1.1)
        self.assertAlmostEqual(M.norm(h.acceleration(1.)),h.speed*h.speed*h.kappa)
    def test_helix_accel_tangent_orthogonal(self):
        h=M.helix_from_radius_pitch(2.,.15,1.2)
        self.assertAlmostEqual(M.dot(h.velocity(4),h.acceleration(4)),0,delta=1e-12)
    def test_helix_negative_tau(self):
        h=M.helix_invert(.2,-.3,3)
        self.assertAlmostEqual(h.tau,-.3)
    def test_helix_invert(self):
        h=M.helix_from_radius_pitch(1.7,.3,4)
        h2=M.helix_invert(h.kappa,h.tau,h.speed)
        self.assertAlmostEqual(h2.radius,h.radius)
        self.assertAlmostEqual(h2.omega,h.omega)
    def test_helix_invalid_radius(self):
        with self.assertRaises(ValueError): M.helix_from_radius_pitch(0,.4)
    def test_helix_invalid_pitch(self):
        with self.assertRaises(ValueError): M.helix_from_radius_pitch(1,math.pi/2)
    def test_invert_straight_invalid(self):
        with self.assertRaises(ValueError): M.helix_invert(0,0)
    def test_lorentz_interval(self): self.assertEqual(M.lorentz_interval(5,1,2,3),11)
    def test_lorentz_inv(self):
        p=(7.,1.,2.,3.)
        v=M.lorentz_z(*p,.7)
        self.assertAlmostEqual(M.lorentz_interval(*p),M.lorentz_interval(*v),delta=1e-12)
    def test_lorentz_inverse(self):
        p=(7.,1.,2.,3.)
        t=M.lorentz_z(*M.lorentz_z(*p,.6),-.6)
        for a,b in zip(t,p): self.assertAlmostEqual(a,b)
    def test_lorentz_bad(self):
        with self.assertRaises(ValueError): M.lorentz_z(1,0,0,0,1.)
    def test_timelike(self): self.assertAlmostEqual(M.proper_time_rate(.6),.8)
    def test_null(self): self.assertEqual(M.proper_time_rate(1.),0.)
    def test_superluminal(self):
        with self.assertRaises(ValueError): M.proper_time_rate(1.0001)
    def test_group_speed_zero(self): self.assertEqual(M.kg_group_velocity(0,1,1),0)
    def test_group_speed_below_c(self): self.assertLess(abs(M.kg_group_velocity(3,4,0)),M.C)
    def test_group_speed_massless_1d(self): self.assertEqual(M.kg_group_velocity(3,0,0),M.C)
    def test_planck(self): self.assertAlmostEqual(M.planck_length()/1.616255e-35,1,delta=1e-5)
    def test_F_zero(self): self.assertEqual(M.threshold_F(0),1)
    def test_F_one(self): self.assertAlmostEqual(M.threshold_F(1),.148495506775922,delta=1e-13)
    def test_F_strict_decline(self):
        xs=[M.threshold_F(x) for x in [.001,.01,.1,1.,2.,4.]]
        self.assertTrue(all(a>b for a,b in zip(xs,xs[1:])))
    def test_F_large(self): self.assertLess(M.threshold_F(8),1e-28)
    def test_E1_reference(self): self.assertAlmostEqual(M.exponential_integral_E1(1),.219383934395520,delta=1e-14)
    def test_induced_scaling_N(self):
        l=1e-35
        self.assertAlmostEqual(M.inverse_G_induced(4,0,l),4*M.inverse_G_induced(1,0,l))
    def test_induced_scaling_length(self):
        self.assertAlmostEqual(M.inverse_G_induced(1,0,1e-35)/M.inverse_G_induced(1,0,2e-35),4.)
    def test_induced_conformal(self): self.assertAlmostEqual(M.inverse_G_induced(3,1/6,1e-35),0,delta=1e-15)
    def test_induced_bare(self): self.assertAlmostEqual(M.inverse_G_induced(1,1/6,1e-35,bare_inverse_G=5.),5.)
    def test_induced_negative_possible(self): self.assertLess(M.inverse_G_induced(1,.3,1e-35),0)
    def test_reverse_fit(self): self.assertAlmostEqual(M.inverse_G_induced(1,0,M.reverse_fit_length(1)),1/M.G,delta=1e-5)
    def test_degeneracy(self):
        self.assertAlmostEqual(M.inverse_G_induced(1,0,1e-35),M.inverse_G_induced(4,0,2e-35))
    def test_alpha_error(self): self.assertAlmostEqual(M.residual_ppm(M.alpha_candidate(),M.ALPHA_2022),-2.222756159,delta=.00001)
    def test_proton_mass_ratio(self): self.assertGreater(abs(M.MASS_RATIO_2022-56*math.pi),1000)
    def test_earth_surface(self): self.assertAlmostEqual(M.spherical_earth_g(0),9.8203,delta=.0001)
    def test_earth_inverse_square(self):
        g0=M.spherical_earth_g(0)
        g1=M.spherical_earth_g(M.EARTH_RADIUS)
        self.assertAlmostEqual(g0/g1,4.)
    def test_dipole_equator(self): self.assertAlmostEqual(M.dipole_B(0),31.2e-6)
    def test_dipole_pole(self): self.assertAlmostEqual(M.dipole_B(math.pi/2),62.4e-6)
    def test_dipole_height(self): self.assertAlmostEqual(M.dipole_B(0,M.EARTH_RADIUS)/M.dipole_B(0),1/8)
    def test_lorentz_magnetic_work(self):
        v=(1.,2.,3.);B=(.01,.02,.03)
        self.assertAlmostEqual(M.dot(M.cross(v,B),v),0.)
    def test_electric_charge_flip(self):
        p=(M.EARTH_RADIUS,0,0);v=(0,0,0);e=(3,0,0)
        f1=M.force_classical(p,v,1,1,e)[1]
        f2=M.force_classical(p,v,1,-1,e)[1]
        self.assertEqual(f1,tuple(-a for a in f2))
    def test_forces_not_all_orthogonal(self):
        r=(M.EARTH_RADIUS,0,0);v=(0,1,0);e=(1,0,0)
        f=M.force_classical(r,v,1.,1.,e)
        self.assertNotEqual(M.dot(f[0],f[1]),0.)
    def test_magnetic_zero_stationary(self):
        r=(M.EARTH_RADIUS,0,0)
        self.assertEqual(M.force_classical(r,(0,0,0),1,1,B_field=(0,0,1))[2],(0,0,0))
    def test_force_invalid_interior(self):
        with self.assertRaises(ValueError):M.force_classical((0,0,0),(0,0,0),1,0)
    def test_yukawa_zero(self): self.assertEqual(M.yukawa_factor(0),1)
    def test_yukawa_one(self): self.assertAlmostEqual(M.yukawa_factor(1),2/math.e)
    def test_yukawa_decays(self): self.assertGreater(M.yukawa_factor(1),M.yukawa_factor(2))
    def test_yukawa_far(self): self.assertEqual(M.yukawa_factor(900),0)
    def test_yukawa_eta_zero(self): self.assertEqual(M.fifth_force_eta(0,0,2),0)
    def test_yukawa_eta_antisym(self): self.assertAlmostEqual(M.fifth_force_eta(.1,-.1,.2),-M.fifth_force_eta(-.1,.1,.2))
    def test_microscope_sigma(self): self.assertAlmostEqual(M.eotvos_sigma_total(),math.sqrt(7.54)*1e-15)
    def test_microscope_zero_pass(self): self.assertTrue(M.pass_microscope_toy(0,0))
    def test_microscope_large_fail(self): self.assertFalse(M.pass_microscope_toy(1e-8,0))
    def test_metric_F_positive(self): self.assertEqual(M.metric_planck_sq(2,1,1),3.)
    def test_metric_F_zero(self): self.assertEqual(M.metric_planck_sq(1,1,1),0.)
    def test_photon_Z(self): self.assertEqual(M.photon_kinetic_Z(2,3,6),2.)
    def test_alpha_variation(self): self.assertEqual(M.log_alpha_derivative(0,2,4),-.5)
    def test_alpha_reject_ghost(self):
        with self.assertRaises(ValueError): M.log_alpha_derivative(-2,1,1)
    def test_scalar_potential_derivative(self):
        p=.7; h=1e-6; m2=.3; lam=.2
        numeric=(M.scalar_potential(p+h,m2,lam)-M.scalar_potential(p-h,m2,lam))/(2*h)
        self.assertAlmostEqual(numeric,M.scalar_potential_prime(p,m2,lam),delta=1e-10)
    def test_vacuum_positive(self): self.assertGreater(M.vacuum_energy_from_cutoff_energy(1e-8),0)
    def test_vacuum_quartic(self): self.assertAlmostEqual(M.vacuum_energy_from_cutoff_energy(2e-8)/M.vacuum_energy_from_cutoff_energy(1e-8),16.)
    def test_status_open(self): self.assertEqual(M.model_status()['four_force_derivation'],'OPEN')
    def test_nan(self):
        with self.assertRaises(ValueError):M.helix_from_radius_pitch(float('nan'),0)


class ParameterizedTests(unittest.TestCase):
    pass


def _add_test(name,fn):
    setattr(ParameterizedTests,name,fn)

for i,pitch in enumerate([-.95,-.7,-.5,-.3,-.1,.03,.12,.4,.75,.95]):
    def _test(self, pitch=pitch):
        h=M.helix_from_radius_pitch(2.7,pitch,3.1)
        h2=M.helix_invert(h.kappa,h.tau,3.1)
        self.assertAlmostEqual(h.radius,h2.radius,places=12)
        self.assertAlmostEqual(h.axial_speed,h2.axial_speed,places=12)
    _add_test(f'test_helix_inverse_{i:02}',_test)

for i,mu in enumerate([0.000001,.0001,.001,.01,.1,.3,.75,1.,1.1,1.3,2.,3.,5.,10.]):
    def _test(self,mu=mu):
        # Strict independent numerical cross check against SciPy, when installed.
        try:
            from scipy.special import exp1
        except ImportError:
            self.skipTest('optional SciPy not installed')
        ref=math.exp(-mu*mu)-mu*mu*exp1(mu*mu)
        self.assertAlmostEqual(M.threshold_F(mu),ref,delta=max(2e-13,abs(ref)*1e-10))
    _add_test(f'test_F_scipy_{i:02}',_test)

for i,beta in enumerate([-.96,-.8,-.52,-.2,.0,.2,.5,.7,.98]):
    def _test(self,beta=beta):
        src=(9.,1.4,-3.,4.2)
        boosted=M.lorentz_z(*src,beta)
        self.assertAlmostEqual(M.lorentz_interval(*src),M.lorentz_interval(*boosted),delta=1e-11)
    _add_test(f'test_interval_boost_{i:02}',_test)

for i,scale in enumerate([2,3,4,5,8]):
    def _test(self,scale=scale):
        one=M.inverse_G_induced(1,0,1e-35)
        many=M.inverse_G_induced(scale*scale,0,scale*1e-35)
        self.assertAlmostEqual(one,many,delta=one*1e-13)
    _add_test(f'test_induced_degeneracy_{i:02}',_test)


if __name__=='__main__':unittest.main()
