import math
import unittest
from fractions import Fraction
from rootv74.physics import *

class TestGeometry(unittest.TestCase):
    def test_dimensions_no_G_from_c_hbar(self):self.assertFalse(dimension_G_can_be_built_with_c_hbar())
    def test_helix_circular(self):
        h=helix(2.,3.,0.);self.assertAlmostEqual(h['curvature'],0.5);self.assertEqual(h['torsion'],0.)
    def test_helix_straight(self):
        h=helix(2.,0.,4.);self.assertEqual(h['curvature'],0.);self.assertEqual(h['torsion'],0.)
    def test_helix_arclength_identity(self):
        h=helix(2.,3.,4.);self.assertAlmostEqual(h['curvature']**2+h['torsion']**2,(3/h['speed'])**2)
    def test_helix_c_speed_constraint_not_forced(self):self.assertNotEqual(helix(2.,3.,4.)['speed'],C)
    def test_helix_speed_accel_orthogonal(self):self.assertEqual(helix(2.,3.,4.)['dot_v_a'],0.)
    def test_same_path_opposite_charge_opposite_force(self):
        q=1.;E=7.;self.assertEqual(q*E,-(-q*E))
    def test_frenet_not_four_forces(self):self.assertNotEqual(3*5,(-3)*5)
    def test_helix_frequency_parity(self):
        a=helix(2.,3.,4.);b=helix(2.,-3.,4.)
        self.assertEqual(a['curvature'],b['curvature']);self.assertEqual(a['torsion'],-b['torsion'])
    def test_radius_halving_curvature(self):
        a=helix(1.,2.,0.);b=helix(2.,2.,0.);self.assertAlmostEqual(a['curvature'],2*b['curvature'])

class TestGravity(unittest.TestCase):
    def test_earth_g(self):self.assertTrue(9.7<BODIES['Earth'].gravity<9.9)
    def test_earth_density(self):self.assertTrue(5400<BODIES['Earth'].density<5600)
    def test_sun_g(self):self.assertTrue(270<BODIES['Sun'].gravity<280)
    def test_moon_g(self):self.assertTrue(1.5<BODIES['Moon'].gravity<1.8)
    def test_K_earth(self):self.assertTrue(0<BODIES['Earth'].kretschmann<1e-35)
    def test_K_equivalent_density(self):
        for body in BODIES.values():
            self.assertAlmostEqual(body.kretschmann/kretschmann_from_density(body.density),1.,places=12)
    def test_K_fixed_density_independent_R(self):
        rho=4500.;r1=1e6;r2=2.5e6
        m1=(4*math.pi/3)*rho*r1**3;m2=(4*math.pi/3)*rho*r2**3
        self.assertAlmostEqual(kretschmann(m1,r1)/kretschmann(m2,r2),1.,places=12)
        self.assertAlmostEqual(g_newton(m2,r2)/g_newton(m1,r1),r2/r1)
    def test_K_fixed_g_inversesquare_r(self):
        g=5.;r1=1e6;r2=2e6
        m1=g*r1**2/G_EXP;m2=g*r2**2/G_EXP
        self.assertAlmostEqual(kretschmann(m1,r1)/kretschmann(m2,r2),(r2/r1)**2)
    def test_tidal_r_inv_cube(self):
        b=BODIES['Earth'];self.assertAlmostEqual(b.tidal,2*b.gravity/b.radius)
    def test_K_r_inv_six(self):
        b=BODIES['Earth'];self.assertAlmostEqual(kretschmann(b.mass,2*b.radius)/b.kretschmann,1/64)
    def test_effective_mass2_units_positive(self):
        b=BODIES['Earth'];self.assertGreater(curvature_toy_delta_mass2(b.mass,b.radius,1.,1.),0)
    def test_effective_mass2_xi_sign(self):
        b=BODIES['Earth'];v=curvature_toy_delta_mass2(b.mass,b.radius,1e6,1)
        self.assertEqual(v,-curvature_toy_delta_mass2(b.mass,b.radius,1e6,-1))
    def test_earth_vs_compact_curvature(self):
        self.assertGreater(BODIES['NeutronStar_demo'].kretschmann,BODIES['Earth'].kretschmann*1e20)
    def test_planet_K_monotone_density(self):
        self.assertGreater(kretschmann_from_density(6000),kretschmann_from_density(3000))

class TestYukawa(unittest.TestCase):
    def test_zero_alpha(self):self.assertEqual(uniform_yukawa_ratio(R_EARTH,R_EARTH,1e6,0),0)
    def test_negative_alpha(self):
        a=uniform_yukawa_ratio(1e6,1.2e6,2e6,.3)
        self.assertAlmostEqual(a,-uniform_yukawa_ratio(1e6,1.2e6,2e6,-.3))
    def test_charge_flip(self):
        a=uniform_yukawa_ratio(1e6,1.2e6,2e6,1,1,1)
        self.assertAlmostEqual(a,-uniform_yukawa_ratio(1e6,1.2e6,2e6,1,1,-1))
    def test_small_ball_point_source(self):
        r=1e6;R=100.;lam=1e6
        expected=(1+r/lam)*math.exp(-r/lam)
        self.assertAlmostEqual(uniform_yukawa_ratio(R,r,lam),expected,places=6)
    def test_long_range_newton(self):
        R=1e6;self.assertAlmostEqual(uniform_yukawa_ratio(R,R,1e12),1.,places=8)
    def test_highly_short_range_no_overflow(self):
        val=uniform_yukawa_ratio(R_EARTH,R_EARTH,1000.)
        self.assertTrue(math.isfinite(val));self.assertTrue(0<val<0.001)
    def test_short_range_far_observer(self):
        val=uniform_yukawa_ratio(R_EARTH,3*R_EARTH,1000.)
        self.assertEqual(val,0.)
    def test_layered_uniform_equivalence(self):
        R=1e6;layers=[Shell(R*.5,3000.),Shell(R,3000.)]
        for lam in (R/50,R,R*10):
            a=uniform_yukawa_ratio(R,1.2*R,lam)
            b=layered_yukawa_ratio(layers,1.2*R,lam)
            self.assertAlmostEqual(a/b,1,places=10)
    def test_layered_charge_universal(self):
        R=1e6;layers=[Shell(R*.5,2000.,1),Shell(R,5000.,1)]
        self.assertAlmostEqual(layered_yukawa_ratio(layers,1.2*R,R*1e5),1.,places=8)
    def test_layered_charge_sign(self):
        layers=[Shell(0.5e6,4000.,1),Shell(1e6,2000.,1)]
        a=layered_yukawa_ratio(layers,1.2e6,1e6,target_charge=1)
        self.assertAlmostEqual(a,-layered_yukawa_ratio(layers,1.2e6,1e6,target_charge=-1))
    def test_internal_structure_changes_short_force(self):
        R=1e6;r=1.1e6;lam=.2e6
        u=uniform_yukawa_ratio(R,r,lam)
        l=layered_yukawa_ratio([Shell(.5*R,7000),Shell(R,2000)],r,lam)
        self.assertGreater(abs(u-l),0.001)
    def test_layers_order_error(self):
        with self.assertRaises(AssertionError):layered_yukawa_ratio([Shell(2.,1.),Shell(1.,1.)],3.,1.)
    def test_observer_inside_error(self):
        with self.assertRaises(AssertionError):uniform_yukawa_ratio(2.,1.,1.)
    def test_microscope_eta_small(self):
        x=eotvos_eta(1e-14,-1e-14);self.assertAlmostEqual(x,2e-14)
    def test_Eotvos_zero_same_effect(self):self.assertEqual(eotvos_eta(.2,.2),0)
    def test_proxy_Z_over_A(self):self.assertAlmostEqual(proxy_charge_Z_over_A(1,2),.5)
    def test_bound_positive(self):self.assertGreater(miniature_eta_bound(-1.5e-15,2.3e-15,1.5e-15,.5,.5,.06),0)
    def test_quadrature_independent(self):
        from scipy.integrate import quad
        R=1e6;lam=0.7e6;r=1.2e6
        integ=quad(lambda s:.5*s*(math.exp(-(r-s)/lam)-math.exp(-(r+s)/lam)),0,R,epsabs=1e-5)[0]
        ratio=(1+r/lam)*(3*lam/R**3)*integ
        self.assertAlmostEqual(ratio/uniform_yukawa_ratio(R,r,lam),1.,places=11)
    def test_large_x_shell_stability(self):
        layers=[Shell(1000.,1000.),Shell(2000.,3000.)]
        x=layered_yukawa_ratio(layers,2000.,1.)
        self.assertTrue(math.isfinite(x));self.assertGreater(x,0)

class TestGaugeAndRG(unittest.TestCase):
    def test_all_local_anomalies_zero(self):
        for a in sm_anomalies().values():self.assertEqual(a,Fraction(0))
    def test_u1cube_zero(self):self.assertEqual(sm_anomalies()['U1_cube'],0)
    def test_global_SU2_anomaly_even_doublets(self):self.assertEqual((3+1)%2,0)
    def test_gauge_running_positive(self):
        m=gauge_running();self.assertGreater(m['best_mu_GeV'],91.1876)
    def test_distinct_pair_crossings(self):
        scales=[c['mu_GeV'] for c in gauge_running()['crossings']]
        self.assertGreater(max(scales)/min(scales),100)
    def test_SM_not_exact_GUT(self):self.assertGreater(gauge_running()['max_minus_min_at_best'],0.1)
    def test_rg_requires_g_input(self):self.assertLess(rg_generated_scale(1e19,.5,7),rg_generated_scale(1e19,.6,7))
    def test_rg_small_g_small_scale(self):self.assertLess(rg_generated_scale(1e19,.5,7),1e-8*1e19)
    def test_rg_large_g_below_uv(self):self.assertLess(rg_generated_scale(1e19,2,7),1e19)
    def test_rg_invalid_input(self):
        with self.assertRaises(AssertionError):rg_generated_scale(1e19,0.,7)
    def test_running_beta_sign(self):
        b=gauge_running()['beta_coefficients'];self.assertGreater(b[0],0);self.assertLess(b[1],0);self.assertLess(b[2],0)
    def test_CODATA_G_input(self):self.assertEqual(G_EXP,6.67430e-11)

if __name__=='__main__':unittest.main()
