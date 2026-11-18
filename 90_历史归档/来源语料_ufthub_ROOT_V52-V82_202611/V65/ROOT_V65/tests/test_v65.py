"""Independent regressions: every test proves an implementation property only."""
import math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src import root_v65 as m

class HelixTests(unittest.TestCase):
    def test_angle_zero(self):
        x=m.helix_from_radius_angle(3,0,4)
        self.assertAlmostEqual(x.curvature,1/3)
        self.assertAlmostEqual(x.torsion,0)
        self.assertAlmostEqual(x.axial_speed,0)
    def test_negative_angle(self):
        x=m.helix_from_radius_angle(2,-.6,5)
        self.assertLess(x.torsion,0)
        self.assertLess(x.axial_speed,0)
    def test_inverse_radius(self):
        for k,t in [(1,0),(.5,.7),(.01,2),(3,-1.2)]:
            x=m.helix_from_curvature_torsion(k,t,7)
            self.assertAlmostEqual(x.curvature,k)
            self.assertAlmostEqual(x.torsion,t)
            self.assertAlmostEqual(x.radius,k/(k*k+t*t))
    def test_angular_speed_identity(self):
        x=m.helix_from_curvature_torsion(.5,1.2,5)
        self.assertAlmostEqual(x.angular_rate,5*1.3)
    def test_speed_norm(self):
        x=m.helix_from_radius_angle(5,.42,123)
        for t in [0.,.1,4.,9.]:self.assertAlmostEqual(m.norm(x.velocity(t)),123,places=10)
    def test_accel_radial(self):
        x=m.helix_from_radius_angle(5,.42,123)
        self.assertAlmostEqual(m.dot(x.velocity(1),x.acceleration(1)),0,places=9)
    def test_curvature_acceleration(self):
        x=m.helix_from_radius_angle(5,.42,123)
        self.assertAlmostEqual(m.norm(x.acceleration(1)),123**2*x.curvature,places=8)
    def test_finite_difference_velocity(self):
        x=m.helix_from_radius_angle(.8,.32,1.4); dt=1e-5;t=.7
        der=tuple((a-b)/(2*dt) for a,b in zip(x.position(t+dt),x.position(t-dt)))
        self.assertLess(m.norm(tuple(a-b for a,b in zip(der,x.velocity(t)))),1e-9)
    def test_finite_difference_accel(self):
        x=m.helix_from_radius_angle(.8,.32,1.4);dt=1e-5;t=.7
        der=tuple((a-b)/(2*dt) for a,b in zip(x.velocity(t+dt),x.velocity(t-dt)))
        self.assertLess(m.norm(tuple(a-b for a,b in zip(der,x.acceleration(t)))),1e-9)
    def test_invalid_straight_inverse(self):
        with self.assertRaises(ValueError):m.helix_from_curvature_torsion(0,0)
    def test_invalid_radius(self):
        with self.assertRaises(ValueError):m.helix_from_radius_angle(-1,.2)
    def test_out_of_range_angle(self):
        with self.assertRaises(ValueError):m.helix_from_radius_angle(1,math.pi/2)
    def test_bad_nan(self):
        with self.assertRaises(ValueError):m.helix_from_radius_angle(1,float('nan'))

class RelativityTests(unittest.TestCase):
    def test_boost_interval(self):
        p=(4.,1.,2.,3.)
        for beta in [-.8,-.3,0.,.3,.8]:
            q=m.boost_z(*p,beta)
            self.assertAlmostEqual(m.lorentz_interval(*p),m.lorentz_interval(*q),places=11)
    def test_boost_reciprocal(self):
        p=(5.,1.,-2.,3.);b=.6
        q=m.boost_z(*m.boost_z(*p,b),-b)
        self.assertLess(max(abs(a-c) for a,c in zip(p,q)),1e-12)
    def test_boost_invalid(self):
        with self.assertRaises(ValueError):m.boost_z(1,0,0,0,1)
    def test_massive_worldline_proper_time(self):
        self.assertEqual(m.massive_proper_time_rate(1),0)
        self.assertEqual(m.massive_proper_time_rate(-1),0)
        self.assertEqual(m.massive_proper_time_rate(0),1)
    def test_massive_sub_luminal(self):
        self.assertAlmostEqual(m.massive_proper_time_rate(.6),.8)
    def test_superluminal_invalid(self):
        with self.assertRaises(ValueError):m.massive_proper_time_rate(1.01)
    def test_KG_group_less_c(self):
        for kz,q,mu in [(2,3,0),(-2,3,0),(10,0,1)]:
            self.assertLess(abs(m.kg_group_velocity(kz,q,mu)),m.C)
    def test_KG_massless_limit(self):
        self.assertEqual(m.kg_group_velocity(2,0,0),m.C)
    def test_KG_zero_invalid(self):
        with self.assertRaises(ValueError):m.kg_group_velocity(0,0,0)

class InducedTests(unittest.TestCase):
    def test_planck_length(self):self.assertAlmostEqual(m.planck_length()/1.616255e-35,1,places=5)
    def test_cutoff_energy_relation(self):
        e=1e9*1.602176634e-19
        self.assertAlmostEqual(m.cutoff_length(e)/(m.HBAR*m.C/e),1)
    def test_threshold_massless(self):self.assertEqual(m.cutoff_threshold(0),1)
    def test_threshold_monotone(self):
        self.assertGreater(m.cutoff_threshold(.1),m.cutoff_threshold(1))
        self.assertGreater(m.cutoff_threshold(1),m.cutoff_threshold(3))
    def test_threshold_massive_zero(self):self.assertEqual(m.cutoff_threshold(40),0)
    def test_threshold_bounds(self):
        for mu in [.001,.1,1,2,4]:
            self.assertGreaterEqual(m.cutoff_threshold(mu),0.)
            self.assertLessEqual(m.cutoff_threshold(mu),1.)
    def test_massless_scaling_degeneracy(self):
        a=m.induced_scalar_coefficient(1,0,1e-35)
        b=m.induced_scalar_coefficient(4,0,2e-35)
        self.assertAlmostEqual(a/b,1,places=12)
    def test_conformal_scalar_zero(self):
        self.assertEqual(m.induced_scalar_coefficient(1,1/6,1e-35),0.)
    def test_nonminimal_sign(self):
        self.assertLess(m.induced_scalar_coefficient(1,.3,1e-35),0)
    def test_bare_arbitrariness(self):
        result=m.induced_scalar_coefficient(3,0,2e-35)
        desired=1/m.G_CODATA_2022
        self.assertAlmostEqual(m.induced_scalar_coefficient(3,0,2e-35,bare_inverse_g=desired-result)/desired,1.)
    def test_reverse_fit_observation(self):
        ell=m.inverse_fit_cutoff(1)
        self.assertAlmostEqual(m.induced_scalar_coefficient(1,0,ell)*m.G_CODATA_2022,1,places=12)
    def test_reverse_fit_scaling(self):self.assertAlmostEqual(m.inverse_fit_cutoff(9)/m.inverse_fit_cutoff(1),3)
    def test_jacobian_rank_one(self):self.assertEqual(m.scalar_cutoff_rank_log_jacobian(9,1),(1.,-2.))
    def test_cutoff_invalid(self):
        with self.assertRaises(ValueError):m.cutoff_length(0)
    def test_induced_badN(self):
        with self.assertRaises(ValueError):m.induced_scalar_coefficient(0,0,1e-35)
    def test_induced_bad_mu(self):
        with self.assertRaises(ValueError):m.cutoff_threshold(-1)
    def test_numerical_threshold_vs_scipy_if_present(self):
        try:
            from scipy.special import exp1
        except ImportError:return
        for u in [.05,.1,.3,1,3]:
            ref=math.exp(-u*u)-u*u*exp1(u*u)
            self.assertAlmostEqual(m.cutoff_threshold(u),ref,delta=2e-7)

class GravityAndFifthForceTests(unittest.TestCase):
    def test_spherical_g(self):
        g=m.gravity_acceleration((m.EARTH_RADIUS,0,0))
        self.assertAlmostEqual(m.norm(g),m.G_CODATA_2022*m.EARTH_MASS/m.EARTH_RADIUS**2,places=12)
    def test_radial_g_inward(self):
        r=(m.EARTH_RADIUS,0,0)
        self.assertLess(m.dot(m.gravity_acceleration(r),r),0)
    def test_inverse_square(self):
        a=m.norm(m.gravity_acceleration((m.EARTH_RADIUS,0,0)))
        b=m.norm(m.gravity_acceleration((2*m.EARTH_RADIUS,0,0)))
        self.assertAlmostEqual(a/b,4)
    def test_dipole_equator_field(self):
        b=m.toy_magnetic_field((m.EARTH_RADIUS,0,0))
        self.assertEqual(b,(0.,0.,-m.B_EQUATOR))
    def test_dipole_pole_ratio(self):
        a=m.norm(m.toy_magnetic_field((m.EARTH_RADIUS,0,0)))
        b=m.norm(m.toy_magnetic_field((0,0,m.EARTH_RADIUS)))
        self.assertAlmostEqual(b/a,2)
    def test_dipole_inverse_cube(self):
        a=m.norm(m.toy_magnetic_field((m.EARTH_RADIUS,0,0)))
        b=m.norm(m.toy_magnetic_field((2*m.EARTH_RADIUS,0,0)))
        self.assertAlmostEqual(a/b,8)
    def test_lorentz_charge_sign_reversal(self):
        r=(m.EARTH_RADIUS,0,0); E=(0,100,0)
        fplus=m.test_body_force(r,(0,0,0),1,1,E)
        fminus=m.test_body_force(r,(0,0,0),1,-1,E)
        self.assertAlmostEqual(fplus[1],100)
        self.assertAlmostEqual(fminus[1],-100)
    def test_magnetic_force_orthogonal_to_velocity(self):
        v=(2000,3000,4000); b=m.toy_magnetic_field((m.EARTH_RADIUS,0,0))
        self.assertAlmostEqual(m.dot(v,m.cross(v,b)),0,places=9)
    def test_grav_field_not_universally_orthogonal_E(self):
        g=m.gravity_acceleration((m.EARTH_RADIUS,0,0))
        self.assertNotEqual(m.dot(g,(1,0,0)),0)
    def test_no_EM_field_if_zero_charge(self):
        r=(m.EARTH_RADIUS,0,0);m1=.3
        self.assertEqual(m.test_body_force(r,(30,0,0),m1,0,(10,0,0)),m.vmul(m.gravity_acceleration(r),m1))
    def test_no_inside_Earth(self):
        with self.assertRaises(ValueError):m.gravity_acceleration((10,0,0))
    def test_yukawa_small_r(self):self.assertEqual(m.yukawa_shape(0,1),1)
    def test_yukawa_monotone(self):self.assertGreater(m.yukawa_shape(1,2),m.yukawa_shape(4,2))
    def test_Eotvos_equal(self):self.assertEqual(m.eotvos_eta(.01,.01,1,1),0)
    def test_Eotvos_sign(self):self.assertGreater(m.eotvos_eta(.01,0,1,1),0)
    def test_Eotvos_antisymmetric(self):self.assertAlmostEqual(m.eotvos_eta(.1,.01,1,2),-m.eotvos_eta(.01,.1,1,2))
    def test_Microscope_interval(self):
        lo,hi=m.microscope_interval()
        self.assertLess(lo,-1.5e-15);self.assertGreater(hi,-1.5e-15)
    def test_95illustrative_not_universal(self):
        lo,hi=m.microscope_interval()
        self.assertAlmostEqual((lo+hi)/2,m.MICROSCOPE_ETA)

if __name__=='__main__': unittest.main()

class LegacyBackportRegression(unittest.TestCase):
    def test_cylindrical_winding_parameter_n_rejected_when_not_implemented(self):
        import importlib.util
        base=Path(__file__).resolve().parents[1]/'legacy_v64'/'src'/'root_v64.py'
        # The legacy solver uses fixed J1 and must not silently claim n=2.
        text=base.read_text(encoding='utf-8')
        self.assertIn("Only winding n=1 is implemented",text)

class HistoricalCandidateAudits(unittest.TestCase):
    """Regression against historic mathematical mistakes; not evidence of GUT."""
    def test_legacy_alpha_candidate_is_not_exact(self):
        candidate=1/(4*math.pi**3+math.pi**2+math.pi)
        alpha_obs=1/137.035999084
        self.assertGreater(abs(candidate/alpha_obs-1),2e-6)
    def test_legacy_proton_electron_mass_ratio_typo(self):
        self.assertAlmostEqual(56*math.pi,175.92918860102841)
        self.assertGreater(abs(56*math.pi-1836.15267343),1000)
    def test_schwarzschild_isco_is_3_horizon_radii(self):
        G=6.67430e-11; M=1.9885e30;c=299792458
        rs=2*G*M/c**2;isco=6*G*M/c**2
        self.assertAlmostEqual(isco/rs,3)
        self.assertLess(rs/2,rs)
    def test_c_axis_plus_c_tangential_superluminal(self):
        self.assertGreater(math.hypot(1,0.1),1)
    def test_speed_decomposition_not_superluminal(self):
        for angle in [.1,.8,1.3]:self.assertAlmostEqual(math.hypot(math.cos(angle),math.sin(angle)),1)
    def test_Z_G_identity_not_prediction(self):
        z=m.G_CODATA_2022*m.C/2
        self.assertEqual(2*z/m.C,m.G_CODATA_2022)
    def test_schwarzschild_coordinate_rate_radial_is_not_simple(self):
        h=.7;v=.2
        true_sq=h-v*v/h;naive_sq=h-v*v
        self.assertNotAlmostEqual(true_sq,naive_sq)
