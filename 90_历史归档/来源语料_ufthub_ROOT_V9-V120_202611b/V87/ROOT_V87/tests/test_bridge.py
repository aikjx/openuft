"""Independent invariants, identities, physical limits and failure handling.
All physical scenarios are analytic or synthetic, NOT observed experiments.
"""
import math, os, sys, unittest
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..','src')))
import bridge as b

class TestCODATAAndUnits(unittest.TestCase):
    def test_c_defined(self): self.assertEqual(b.C,299792458)
    def test_g_reference(self): self.assertEqual(b.G,6.67430e-11)
    def test_hbar(self): self.assertAlmostEqual(b.HBAR*2*math.pi/b.H,1,places=14)
    def test_planck_length(self): self.assertAlmostEqual(b.planck_length()/1.616255e-35,1,places=6)
    def test_planck_mass(self): self.assertAlmostEqual(b.planck_mass()/2.176434e-8,1,places=6)
    def test_l_planck_cube(self): self.assertAlmostEqual(b.planck_length()**2*b.C**3/(b.HBAR*b.G),1,places=14)
    def test_alpha_plank_mass(self): self.assertAlmostEqual(b.alpha_gravity(b.planck_mass()),1,places=14)
    def test_planck_mass_compton_grav_radius(self):
        m=b.planck_mass()
        self.assertAlmostEqual((b.G*m/b.C**2)/(b.HBAR/(m*b.C)),1,places=12)
    def test_planck_schwarzschild_factor_two(self):
        m=b.planck_mass()
        self.assertAlmostEqual(b.schwarzschild_radius(m)/(b.HBAR/(m*b.C)),2,places=12)
    def test_electron_coupling_tiny(self):
        self.assertTrue(1e-46 < b.alpha_gravity(9.1093837139e-31) < 1e-44)
    def test_quantum_parameter_planck_scale(self):
        self.assertAlmostEqual(b.epsilon_quantum_gravity(b.planck_length()),1,places=14)
    def test_quantum_parameter_meter(self): self.assertLess(b.epsilon_quantum_gravity(1),1e-69)

class TestNewtonGRLimits(unittest.TestCase):
    def test_earth_g(self): self.assertTrue(9.7<b.acceleration(b.M_EARTH,b.R_EARTH)<9.9)
    def test_inverse_square(self):
        for r in (.1,1,1e6):
            with self.subTest(r=r): self.assertAlmostEqual(b.acceleration(7,r)/b.acceleration(7,2*r),4,places=14)
    def test_newton_potential(self): self.assertAlmostEqual(b.potential(2,4),-b.G/2,places=25)
    def test_newton_gradient(self):
        for x in (.3,10.,1e5):
            with self.subTest(x=x):
                d=b.numerical_gradient(lambda r:b.potential(80,r),x)
                self.assertAlmostEqual(d/b.acceleration(80,x),1,places=9)
    def test_potential_difference_exact(self):
        self.assertAlmostEqual(b.potential_difference(80,.3,.31),b.potential(80,.31)-b.potential(80,.3),delta=1e-21)
    def test_difference_opposite(self):
        self.assertAlmostEqual(b.potential_difference(80,.31,.3),-b.potential_difference(80,.3,.31),places=20)
    def test_schwarzschild_compactness(self):
        for M,r in ((80,.5),(b.M_EARTH,b.R_EARTH),(b.M_SUN,6.9634e8)):
            with self.subTest(M=M): self.assertAlmostEqual(b.schwarzschild_radius(M)/(2*r),b.compactness(M,r),places=14)
    def test_earth_redshift_meter(self):
        v=b.redshift_static(b.M_EARTH,b.R_EARTH,b.R_EARTH+1)
        approx=b.acceleration(b.M_EARTH,b.R_EARTH)/b.C**2
        # Avoid direct subtractive cancellation in validating tiny ~1e-16 signal.
        self.assertLess(abs(v-(1-approx)),5e-16)
    def test_redshift_no_difference(self): self.assertAlmostEqual(b.redshift_static(b.M_EARTH,b.R_EARTH,b.R_EARTH),1)
    def test_redshift_upward(self): self.assertLess(b.redshift_static(b.M_EARTH,b.R_EARTH,b.R_EARTH+10000),1)
    def test_redshift_reversed_reciprocal(self):
        a=b.R_EARTH;z=b.redshift_static(b.M_EARTH,a,a+5e5)
        self.assertAlmostEqual(z*b.redshift_static(b.M_EARTH,a+5e5,a),1)
    def test_hover_stronger_than_newton(self):
        M=b.M_SUN;r=b.schwarzschild_radius(M)*2
        self.assertGreater(b.hover_proper_acceleration(M,r),b.acceleration(M,r))
    def test_hover_small_compactness(self):
        self.assertAlmostEqual(b.hover_proper_acceleration(b.M_EARTH,b.R_EARTH)/b.acceleration(b.M_EARTH,b.R_EARTH),1,places=8)
    def test_mercury_advance(self):
        d=b.perihelion_advance_rad(b.M_SUN,5.790905e10,.205630)
        self.assertTrue(5e-7<d<6e-7)
    def test_perihelion_increases_with_e(self):
        self.assertGreater(b.perihelion_advance_rad(b.M_SUN,5e10,.5),b.perihelion_advance_rad(b.M_SUN,5e10,0))
    def test_perihelion_scaling(self):
        self.assertAlmostEqual(b.perihelion_advance_rad(2e30,1e11,0)/b.perihelion_advance_rad(2e30,2e11,0),2)

class TestQuantumNewtonBridge(unittest.TestCase):
    def test_uniform_phase(self):
        m=b.M_RB87;T=.001;h=1e-7
        self.assertAlmostEqual(b.phase_uniform(m,b.G_STD,h,T),-m*b.G_STD*h*T/b.HBAR,places=14)
    def test_phase_100nm_range(self): self.assertTrue(1.3<abs(b.phase_uniform(b.M_RB87,b.G_STD,1e-7,.001))<1.4)
    def test_phase_mass_linear(self):
        self.assertAlmostEqual(b.phase_uniform(2,9,1,.1)/b.phase_uniform(1,9,1,.1),2)
    def test_phase_height_linear(self):
        self.assertAlmostEqual(b.phase_uniform(1,9,2,.1)/b.phase_uniform(1,9,1,.1),2)
    def test_phase_time_linear(self):
        self.assertAlmostEqual(b.phase_uniform(1,9,1,.2)/b.phase_uniform(1,9,1,.1),2)
    def test_global_phase_cancel(self):
        for offset in (-1e3,0,1e3):
            diff=(10+offset)-(7+offset)
            self.assertEqual(diff,3)
    def test_spherical_phase_negative(self):
        self.assertLess(b.phase_spherical(b.M_RB87,100,.3,.31,1),0)
    def test_spherical_shape_normalization(self):
        for R,h in ((.3,.01),(1,1e-3),(b.R_EARTH,1)):
            with self.subTest(R=R):
                ph=b.phase_spherical(b.M_RB87,100,R,R+h,1)
                uniform=b.phase_uniform(b.M_RB87,b.acceleration(100,R),h,1)
                self.assertAlmostEqual(ph/uniform,b.phase_shape_ratio(R,h),delta=2e-13)
    def test_spherical_to_uniform_limit(self): self.assertAlmostEqual(b.phase_shape_ratio(1,1e-7),1,places=6)
    def test_spherical_finite_height_deviation(self): self.assertAlmostEqual(b.phase_shape_ratio(.3,.01),.3/.31)
    def test_shape_independent_GM(self):
        for M in (1,1e3,1e10):
            with self.subTest(M=M):
                s=b.potential_difference(M,.3,.31)/(b.acceleration(M,.3)*.01)
                self.assertAlmostEqual(s,.3/.31,places=12)
    def test_small_source_phase_scale(self):
        res=b.source_phase_design(100,.3,.01,1)
        self.assertTrue(.9<abs(res['phase_rad'])<1.1)
    def test_assumed_noise_snr(self): self.assertTrue(b.source_phase_design(100,.3,.01,1,phase_noise_rad=.01)['phase_snr']>90)
    def test_change_noise_changes_snr(self):
        a=b.source_phase_design(100,.3,.01,1,phase_noise_rad=.01)['phase_snr']
        z=b.source_phase_design(100,.3,.01,1,phase_noise_rad=.02)['phase_snr']
        self.assertAlmostEqual(a/z,2)
    def test_source_phase_scale_mass(self):
        x=b.source_phase_design(100,.3,.01,1)['phase_rad']
        y=b.source_phase_design(200,.3,.01,1)['phase_rad']
        self.assertAlmostEqual(y/x,2)
    def test_no_independent_G_with_phase(self):
        # a=GM/R², deltaPhi=GM (1/r1-1/r2); Jacobian wrt G and M has zero determinant.
        M=100.; R=.3;h=.01
        dg_dG=M/R**2;dg_dM=b.G/R**2
        dphi_dG=M*h/(R*(R+h));dphi_dM=b.G*h/(R*(R+h))
        determinant=dg_dG*dphi_dM-dg_dM*dphi_dG
        self.assertAlmostEqual(determinant,0,delta=1e-20)

class TestYukawaAndFailures(unittest.TestCase):
    def test_yukawa_zero_alpha(self):
        for r in (.01,.2,3):
            with self.subTest(r=r):
                self.assertAlmostEqual(b.potential_yukawa(5,r,0,.5),b.potential(5,r),places=20)
                self.assertAlmostEqual(b.acceleration_yukawa(5,r,0,.5),b.acceleration(5,r),places=20)
    def test_shape_newton(self): self.assertEqual(b.shape_yukawa(.3,0,.4),1)
    def test_yukawa_long_length(self):
        self.assertAlmostEqual(b.acceleration_yukawa(10,.2,.1,1e8)/b.acceleration(10,.2),1.1,places=10)
    def test_yukawa_short_length(self):
        self.assertAlmostEqual(b.acceleration_yukawa(10,.2,.1,1e-8)/b.acceleration(10,.2),1,places=14)
    def test_yukawa_gradient(self):
        M=1.;alpha=.2;lamb=.4;r=.3
        dd=b.numerical_gradient(lambda t:b.potential_yukawa(M,t,alpha,lamb),r)
        self.assertAlmostEqual(dd/b.acceleration_yukawa(M,r,alpha,lamb),1,places=8)
    def test_yukawa_newton_shape(self): self.assertAlmostEqual(b.normalized_yukawa_shape(10,.3,.31,0,.4),.3/.31,places=12)
    def test_yukawa_phase_alpha_zero(self):
        a=b.phase_yukawa(b.M_RB87,100,.3,.31,1,0,.4)
        self.assertAlmostEqual(a/b.phase_spherical(b.M_RB87,100,.3,.31,1),1)
    def test_yukawa_shape_sign_positive(self): self.assertGreater(b.shape_yukawa(.3,.3,.3),1)
    def test_yukawa_shape_sign_negative(self): self.assertLess(b.shape_yukawa(.3,-.2,.3),1)
    def test_negative_lambda_rejected(self):
        for val in (-1,0):
            with self.subTest(val=val):
                with self.assertRaises(ValueError): b.shape_yukawa(.2,.1,val)
    def test_overhorizon_rejected(self):
        with self.assertRaises(ValueError): b.redshift_static(1e30,1,2)
    def test_zero_mass_rejected(self):
        with self.assertRaises(ValueError): b.acceleration(0,1)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): b.potential(float('nan'),1)
    def test_phase_zero_time_rejected(self):
        with self.assertRaises(ValueError): b.phase_uniform(1,1,1,0)
    def test_invalid_eccentricity_rejected(self):
        for val in (-.01,1,2):
            with self.subTest(val=val):
                with self.assertRaises(ValueError): b.perihelion_advance_rad(b.M_SUN,1e11,val)

class TestGaussianSemiclassicalToy(unittest.TestCase):
    def test_gaussian_center_value(self):
        self.assertAlmostEqual(b.gaussian_potential(3,1,0),-2*b.G*3/math.sqrt(math.pi),places=14)
    def test_gaussian_near_center_continuity(self):
        a=b.gaussian_potential(1,.5,0);z=b.gaussian_potential(1,.5,1e-8)
        self.assertAlmostEqual(a/z,1,places=11)
    def test_gaussian_far_field(self):
        self.assertAlmostEqual(b.gaussian_potential(3,.1,2)/b.potential(3,2),1,places=14)
    def test_gaussian_density_positive(self): self.assertGreater(b.gaussian_density(1,.1,0),0)
    def test_gaussian_density_decrease(self): self.assertGreater(b.gaussian_density(1,.1,0),b.gaussian_density(1,.1,.1))
    def test_gaussian_density_normalization(self):
        from scipy.integrate import quad
        M,a=2.,.3
        integral=quad(lambda r:4*math.pi*r*r*b.gaussian_density(M,a,r),0,8*a,epsabs=1e-12)[0]
        self.assertAlmostEqual(integral/M,1,places=10)
    def test_gaussian_potential_gradient_poisson(self):
        from scipy.special import erf
        M,a,r=2.,.3,.2
        x=r/a
        mencl=M*(erf(x)-2*x*math.exp(-x*x)/math.sqrt(math.pi))
        numeric=b.numerical_gradient(lambda t:b.gaussian_potential(M,a,t),r)
        self.assertAlmostEqual(numeric/(b.G*mencl/r**2),1,places=8)
    def test_sn_kinetic_positive(self): self.assertGreater(b.gaussian_quantum_kinetic(1e-20,1e-4),0)
    def test_sn_gravity_negative(self): self.assertLess(b.gaussian_grav_self_energy(1e-20,1e-4),0)
    def test_sn_potential_double_counting_half(self):
        # Reference energy = 1/2 integral rho Phi for a Gaussian.
        from scipy.integrate import quad
        m,a=1e-9,.01
        energy=quad(lambda r:2*math.pi*r*r*b.gaussian_density(m,a,r)*b.gaussian_potential(m,a,r),0,10*a,epsabs=1e-32)[0]
        self.assertAlmostEqual(energy/b.gaussian_grav_self_energy(m,a),1,places=7)
    def test_sn_stationary_radius(self):
        m=1e-16;a=b.sn_variational_radius(m)
        self.assertAlmostEqual(b.gaussian_quantum_kinetic(m,a),-b.gaussian_grav_self_energy(m,a)/2,places=14)
    def test_sn_minimum(self):
        m=1e-16;a=b.sn_variational_radius(m)
        self.assertLess(b.sn_gaussian_toy_energy(m,a),b.sn_gaussian_toy_energy(m,a*.9))
        self.assertLess(b.sn_gaussian_toy_energy(m,a),b.sn_gaussian_toy_energy(m,a*1.1))
    def test_sn_radius_mass_cubic(self):
        self.assertAlmostEqual(b.sn_variational_radius(1e-16)/b.sn_variational_radius(2e-16),8,places=12)
    def test_sn_quantum_dominates_electron(self):
        # At 1 micron an electron's gravitational self-energy is negligible.
        self.assertGreater(b.gaussian_quantum_kinetic(9.11e-31,1e-6)/abs(b.gaussian_grav_self_energy(9.11e-31,1e-6)),1e30)

class TestInterferenceAndEnergy(unittest.TestCase):
    def test_entangling_phase_zero_if_separable(self):
        # r00=r01 and r10=r11 -> row-only source phase; no nonlocal phase invariant.
        self.assertAlmostEqual(b.branch_entangling_phase(1e-12,1e-12,.001,.001,.002,.002,1),0)
    def test_entangling_phase_nonzero(self):
        self.assertNotEqual(b.branch_entangling_phase(1e-12,1e-12,.001,.002,.003,.001,1),0)
    def test_entangling_phase_masses(self):
        a=b.branch_entangling_phase(1e-12,1e-12,.001,.002,.003,.004,1)
        z=b.branch_entangling_phase(2e-12,1e-12,.001,.002,.003,.004,1)
        self.assertAlmostEqual(z/a,2)
    def test_em_energy_mass(self): self.assertEqual(b.em_energy_mass(0),0)
    def test_em_energy_mass_linear(self): self.assertAlmostEqual(b.em_energy_mass(200)/b.em_energy_mass(100),2)
    def test_closed_transfer_no_mass_increase(self):
        U=1e5
        self.assertAlmostEqual(b.em_energy_mass(U)+b.em_energy_mass(-U),0)

if __name__=='__main__':unittest.main(verbosity=2)

class TestClockTriangleAndCurvature(unittest.TestCase):
    def test_clock_height_earth(self):
        d=b.clock_high_over_low_fractional(b.M_EARTH,b.R_EARTH,b.R_EARTH+1)
        approximate=b.acceleration(b.M_EARTH,b.R_EARTH)/b.C**2
        self.assertAlmostEqual(d/approximate,1,places=6)
    def test_clock_height_linear_near_surface(self):
        a=b.clock_high_over_low_fractional(b.M_EARTH,b.R_EARTH,b.R_EARTH+1)
        z=b.clock_high_over_low_fractional(b.M_EARTH,b.R_EARTH,b.R_EARTH+2)
        self.assertAlmostEqual(z/a,2,places=6)
    def test_clock_strong_field_positive(self):
        M=b.M_SUN;r=3*b.schwarzschild_radius(M)
        self.assertGreater(b.clock_high_over_low_fractional(M,r,2*r),0)
    def test_clock_invalid(self):
        with self.assertRaises(ValueError):b.clock_high_over_low_fractional(b.M_EARTH,b.R_EARTH,b.R_EARTH)
    def test_triangle_small_earth(self):
        z=b.consistency_triangle(b.M_EARTH,b.R_EARTH,b.R_EARTH+10,b.M_RB87,.01)
        self.assertLess(abs(z['fractional_difference']),1e-8)
    def test_triangle_more_strong_field_correction(self):
        M=b.M_SUN;rs=b.schwarzschild_radius(M)
        x=b.consistency_triangle(M,1.1*rs,1.2*rs,b.M_RB87,.01)
        self.assertGreater(abs(x['fractional_difference']),.01)
    def test_kretschmann_r_minus_six(self):
        M=b.M_SUN;r=10*b.schwarzschild_radius(M)
        self.assertAlmostEqual(b.kretschmann_schwarzschild(M,r)/b.kretschmann_schwarzschild(M,2*r),64)
    def test_kretschmann_mass_squared(self):
        self.assertAlmostEqual(b.kretschmann_schwarzschild(20,1)/b.kretschmann_schwarzschild(10,1),4)
