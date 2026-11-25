"""Reproducible unit / consistency / red-team tests (not empirical discoveries)."""
import math,sys,pathlib,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
import physics as p

class TestDimensionAndConstants(unittest.TestCase):
    def test_G_is_not_one(self): self.assertNotEqual(p.G,1.)
    def test_hbar_is_not_one(self): self.assertNotEqual(p.HBAR,1.)
    def test_earth_mass_JPL(self): self.assertLess(abs(p.MU_EARTH/p.G/5.9722e24-1),1e-4)
    def test_moon_mass_JPL(self): self.assertAlmostEqual(p.MU_MOON/p.G/1e22,7.34578925,places=6)
    def test_shells_well_formed(self):
        for ls in [p.EARTH_LAYERS,p.MOON_LAYERS]: self.assertGreater(p.check_shells(ls),0.)
    def test_shell_mass_positive(self): self.assertTrue(p.mass_shells(p.EARTH_LAYERS)>0)
    def test_invalid_shells(self):
        with self.assertRaises(ValueError): p.check_shells([p.Layer(0,1,3),p.Layer(1.1,2,4)])

class TestNewton(unittest.TestCase):
    def test_inverse_square(self):
        for mu in [p.MU_EARTH,p.MU_MOON]:
            a=p.norm(p.newton_vector((1e7,0,0),mu))
            b=p.norm(p.newton_vector((2e7,0,0),mu))
            self.assertAlmostEqual(a/b,4,places=12)
    def test_vector_radial(self):
        x=(4e6,3e6,5e6);g=p.newton_vector(x,p.MU_EARTH)
        self.assertLess(p.dot(x,g),0)
        for i in range(3): self.assertAlmostEqual(g[i]/x[i],g[0]/x[0])
    def test_origin_rejected(self):
        with self.assertRaises(ValueError):p.newton_vector((0,0,0),p.MU_EARTH)
    def test_enclosed_mass_center(self):
        for ls in (p.EARTH_LAYERS,p.MOON_LAYERS):self.assertEqual(p.shell_cumulative_mass(0,ls),0)
    def test_enclosed_mass_at_surface(self):
        for ls in (p.EARTH_LAYERS,p.MOON_LAYERS):self.assertAlmostEqual(p.shell_cumulative_mass(p.check_shells(ls),ls)/p.mass_shells(ls),1,places=13)
    def test_internal_center_zero(self):self.assertEqual(p.internal_g(0,p.EARTH_LAYERS),0)
    def test_internal_surface(self):
        R=p.R_EARTH_MEAN
        self.assertAlmostEqual(p.internal_g(R,p.EARTH_LAYERS),p.G*p.mass_shells(p.EARTH_LAYERS)/R**2,places=12)
    def test_enclosed_monotonic(self):
        ls=p.EARTH_LAYERS;R=p.R_EARTH_MEAN
        mm=[p.shell_cumulative_mass(i*R/100,ls) for i in range(101)]
        self.assertTrue(all(a<=b for a,b in zip(mm,mm[1:])))
    def test_negative_radius_rejected(self):
        with self.assertRaises(ValueError):p.shell_cumulative_mass(-1,p.EARTH_LAYERS)

class TestEarthJ2(unittest.TestCase):
    def test_gradient_3d(self):
        for x in [(p.R_EARTH_EQUATOR,0.,0.),(1e6,5e6,5e6),(-6e6,-2e6,3e6)]:
            a=p.earth_gravity(x)
            b=tuple(-v for v in p.gradient_numeric(p.j2_potential,x,step=.5))
            self.assertLess(max(abs(a[i]-b[i]) for i in range(3)),2e-7)
    def test_earth_equatorial_g(self):self.assertLess(abs(p.norm(p.earth_rotating_effective((p.R_EARTH_EQUATOR,0.,0.)))-9.780),.003)
    def test_earth_polar_g(self):self.assertLess(abs(p.norm(p.earth_rotating_effective((0.,0.,p.R_EARTH_POLAR)))-9.832),.003)
    def test_rotation_zero_at_pole(self):
        x=(0.,0.,p.R_EARTH_POLAR)
        self.assertEqual(p.earth_gravity(x),p.earth_rotating_effective(x))
    def test_rotation_reduces_equator(self):
        x=(p.R_EARTH_EQUATOR,0.,0.)
        self.assertLess(p.norm(p.earth_rotating_effective(x)),p.norm(p.earth_gravity(x)))
    def test_azimuthal_symmetry(self):
        a=p.earth_gravity((p.R_EARTH_EQUATOR,0.,0.))
        b=p.earth_gravity((0.,p.R_EARTH_EQUATOR,0.))
        self.assertAlmostEqual(a[0],b[1],places=12)
        self.assertEqual(a[1],0)
    def test_potential_even_under_z(self):
        self.assertEqual(p.j2_potential((1e6,2e6,7e6)),p.j2_potential((1e6,2e6,-7e6)))

class TestYukawa(unittest.TestCase):
    def test_analytic_against_independent_simpson(self):
        for ls in (p.EARTH_LAYERS,p.MOON_LAYERS):
            a=p.yukawa_compensated_mass_analytic(ls,p.ROOT_LAMBDA)
            b=p.yukawa_compensated_mass_simpson(ls,p.ROOT_LAMBDA,2048)
            self.assertLess(abs(a-b)/a,1e-9)
    def test_convergence_order(self):
        ls=p.EARTH_LAYERS;lam=p.ROOT_LAMBDA
        target=p.yukawa_compensated_mass_analytic(ls,lam)
        errors=[abs(p.yukawa_compensated_mass_simpson(ls,lam,n)-target) for n in (64,128,256)]
        self.assertTrue(errors[0]>errors[1]>errors[2])
        self.assertTrue(errors[0]/errors[1]>14)
    def test_earth_inherited_v132_fraction(self):
        self.assertAlmostEqual(p.yukawa_accel_ratio(p.R_EARTH_MEAN,p.EARTH_LAYERS),.0062804,delta=.00004)
    def test_moon_positive(self):
        self.assertGreater(p.yukawa_accel_ratio(p.R_MOON,p.MOON_LAYERS),0)
    def test_alpha_linear(self):
        for ls in (p.EARTH_LAYERS,p.MOON_LAYERS):
            R=p.check_shells(ls)
            self.assertAlmostEqual(p.yukawa_accel_ratio(R,ls,alpha=.4)/p.yukawa_accel_ratio(R,ls,alpha=.2),2.)
    def test_alpha_zero(self):
        self.assertEqual(p.yukawa_accel_ratio(p.R_EARTH_MEAN,p.EARTH_LAYERS,alpha=0),0)
    def test_decay_with_height(self):
        R=p.R_EARTH_MEAN
        r=[p.yukawa_accel_ratio(R+h,p.EARTH_LAYERS) for h in (0,100e3,200e3,400e3,800e3)]
        self.assertTrue(all(a>b for a,b in zip(r,r[1:])))
    def test_far_distance_limit(self):
        self.assertLess(p.yukawa_accel_ratio(p.R_EARTH_MEAN+5000e3,p.EARTH_LAYERS),1e-15)
    def test_long_range_alpha_limit(self):
        lam=1e13
        for ls in (p.EARTH_LAYERS,p.MOON_LAYERS):
            R=p.check_shells(ls)
            self.assertAlmostEqual(p.yukawa_accel_ratio(R,ls,alpha=.42,lam=lam),.42,delta=3e-6)
    def test_invalid_inside_exterior(self):
        with self.assertRaises(ValueError):p.yukawa_accel_ratio(p.R_EARTH_MEAN-1,p.EARTH_LAYERS)
    def test_invalid_lambda(self):
        with self.assertRaises(ValueError):p.yukawa_compensated_mass_analytic(p.EARTH_LAYERS,0)
    def test_vector_radial(self):
        x=(0.,p.R_EARTH_MEAN+400e3,0.)
        a=p.yukawa_vector(x,p.MU_EARTH,p.EARTH_LAYERS)
        self.assertLess(a[1],0);self.assertEqual(a[0],0.)
    def test_uniform_shape_normalization(self):
        # For a uniform sphere, analytic and Simpson results must match.
        s=(p.Layer(0.,2e6,4000.),)
        self.assertAlmostEqual(p.yukawa_accel_ratio(2e6,s),p.yukawa_accel_ratio_numeric(2e6,s),delta=1e-9)
    def test_point_mass_not_valid_for_extended_source(self):
        full=p.yukawa_accel_ratio(p.R_EARTH_MEAN,p.EARTH_LAYERS)
        point=p.point_yukawa_ratio(p.R_EARTH_MEAN)
        self.assertGreater(full,point*1e9)

class TestHelixAndOrthogonality(unittest.TestCase):
    def test_c1_spatial_speed(self):
        a=2.;om=.3;u=.8
        self.assertAlmostEqual(p.norm(p.helix_velocity(2.,a,om,u)),1.,places=13)
    def test_accel_perpendicular_velocity(self):
        a=2.;om=.3;u=.8
        for t in (.0,.73,5.13):
            self.assertAlmostEqual(p.dot(p.helix_velocity(t,a,om,u),p.helix_acceleration(t,a,om,u)),0,places=13)
    def test_helix_invariant(self):
        a=2.;om=.3;u=.8
        kap,tau=p.helix_curvature_torsion(a,om,u)
        self.assertAlmostEqual(kap*kap+tau*tau,om*om,places=13)
    def test_curvature_equals_accel_at_c1(self):
        a=2.;om=.3;u=.8
        k,_=p.helix_curvature_torsion(a,om,u)
        self.assertAlmostEqual(k,p.norm(p.helix_acceleration(.33,a,om,u)))
    def test_zero_tangential_acceleration(self):
        a=2.;om=.3;u=.8
        self.assertAlmostEqual(p.dot(p.helix_velocity(.5,a,om,u),p.helix_acceleration(.5,a,om,u)),0)
    def test_nonzero_binormal_is_not_force(self):
        # In a constant-speed Euclidean helix the physical acceleration is normal only.
        a=2.;om=.3;u=.8
        t=.31
        vel=p.helix_velocity(t,a,om,u);acc=p.helix_acceleration(t,a,om,u)
        bx=(vel[1]*acc[2]-vel[2]*acc[1],vel[2]*acc[0]-vel[0]*acc[2],vel[0]*acc[1]-vel[1]*acc[0])
        self.assertAlmostEqual(p.dot(bx,acc),0,places=13)
    def test_universal_g_perp_B_counterexample(self):
        # Ideal aligned dipole's B is parallel/anti-parallel to radial gravity at polar axis.
        x=(0.,0.,p.R_EARTH_MEAN)
        g=p.newton_vector(x,p.MU_EARTH)
        b=p.dipole_field(x)
        cosine=p.dot(g,b)/(p.norm(g)*p.norm(b))
        self.assertAlmostEqual(abs(cosine),1.,places=13)
    def test_helix_invalid(self):
        with self.assertRaises(ValueError):p.helix_curvature_torsion(2,0,1)

class TestIdentifiability(unittest.TestCase):
    def test_one_height_cannot_separate_parameters(self):
        with self.assertRaises(ValueError):p.fit_fractional_offset_and_alpha([0.,0.],[0.,0.],[1e-6,1e-6],p.EARTH_LAYERS)
    def test_synthetic_injection_recovery(self):
        heights=[0.,100e3,400e3,800e3,2000e3]
        shapes=[p.yukawa_accel_ratio(p.R_EARTH_MEAN+h,p.EARTH_LAYERS,alpha=1.) for h in heights]
        y=[.0002+.05*f for f in shapes]
        res=p.fit_fractional_offset_and_alpha(heights,y,[1e-5]*len(y),p.EARTH_LAYERS)
        self.assertAlmostEqual(res['alpha'],.05,places=12)
        self.assertAlmostEqual(res['beta'],.0002,places=12)
        self.assertLess(res['chi2'],1e-16)
    def test_synthetic_null(self):
        heights=[0.,100e3,400e3,800e3]
        res=p.fit_fractional_offset_and_alpha(heights,[0]*len(heights),[1e-5]*len(heights),p.EARTH_LAYERS)
        self.assertEqual(res['alpha'],0.)
    def test_error_estimate_positive(self):
        heights=[0.,200e3,400e3,800e3]
        res=p.fit_fractional_offset_and_alpha(heights,[0]*len(heights),[1e-5]*len(heights),p.EARTH_LAYERS)
        self.assertGreater(res['sigma_alpha'],0.)
    def test_two_identical_heights_degenerate(self):
        with self.assertRaises(ValueError):p.fit_fractional_offset_and_alpha([300e3,300e3],[0.,0.],[1e-5]*2,p.EARTH_LAYERS)

if __name__=='__main__':unittest.main()

class TestPotentialAndRobustness(unittest.TestCase):
    def test_yukawa_potential_gradient(self):
        for layers,mu,R in [(p.EARTH_LAYERS,p.MU_EARTH,p.R_EARTH_MEAN),(p.MOON_LAYERS,p.MU_MOON,p.R_MOON)]:
            for h in [1000.,100e3,400e3,1000e3]:
                r=R+h
                step=.1
                measured=-(p.yukawa_potential_per_kg(r+step,mu,layers)-p.yukawa_potential_per_kg(r-step,mu,layers))/(2*step)
                expected=-mu/r**2*p.yukawa_accel_ratio(r,layers)
                self.assertAlmostEqual(measured/expected,1.,delta=1e-7)
    def test_uniform_sphere_closed_form(self):
        for R,lam in [(1e6,1e6),(3e6,1e6),(6e6,250e3)]:
            model=(p.Layer(0.,R,2000.),)
            numeric=p.yukawa_accel_ratio(R,model,alpha=1.,lam=lam)
            exact=p.uniform_sphere_yukawa_shape(R,lam)
            self.assertAlmostEqual(numeric/exact,1.,delta=1e-10)
    def test_density_rescaling_invariance_of_fraction(self):
        for ls in (p.EARTH_LAYERS,p.MOON_LAYERS):
            R=p.check_shells(ls)
            scaled=tuple(p.Layer(l.inner_m,l.outer_m,l.density_kg_m3*1.17) for l in ls)
            self.assertAlmostEqual(p.yukawa_accel_ratio(R,ls),p.yukawa_accel_ratio(R,scaled),places=12)
    def test_surface_density_sensitivity(self):
        ls=list(p.EARTH_LAYERS);l=ls[-1];R=p.R_EARTH_MEAN
        ls[-1]=p.Layer(l.inner_m,l.outer_m,l.density_kg_m3*1.2)
        self.assertNotEqual(p.yukawa_accel_ratio(R,ls),p.yukawa_accel_ratio(R,p.EARTH_LAYERS))
    def test_conservation_of_energy_circular_helix_not_free(self):
        # No full 4-force claim; nonzero geometric acceleration requires a driving interaction
        a=2.;omega=.3;u=.8
        self.assertGreater(p.norm(p.helix_acceleration(.2,a,omega,u)),0)
        self.assertAlmostEqual(p.dot(p.helix_velocity(.2,a,omega,u),p.helix_acceleration(.2,a,omega,u)),0.)

class TestOrbitalDiscriminant(unittest.TestCase):
    def test_newton_no_precession(self):
        r=p.R_EARTH_MEAN+400e3
        o=p.near_circular_orbit_frequencies(r,p.MU_EARTH,p.EARTH_LAYERS,alpha=0)
        self.assertTrue(o['stable'])
        self.assertAlmostEqual(o['precession_rad_per_rev'],0.)
    def test_yukawa_400km_orbit_precession(self):
        r=p.R_EARTH_MEAN+400e3
        o=p.near_circular_orbit_frequencies(r,p.MU_EARTH,p.EARTH_LAYERS)
        self.assertTrue(o['stable'])
        self.assertAlmostEqual(o['precession_rad_per_rev'],.04557103568257941,delta=1e-8)
    def test_finite_diff_epicycle(self):
        r=p.R_EARTH_MEAN+400e3
        h=500.
        phi=lambda x:p.gravitational_specific_potential(x,p.MU_EARTH)+p.yukawa_potential_per_kg(x,p.MU_EARTH,p.EARTH_LAYERS)
        grad=(phi(r+h)-phi(r-h))/(2*h)
        second=(phi(r+h)-2*phi(r)+phi(r-h))/(h*h)
        o=p.near_circular_orbit_frequencies(r,p.MU_EARTH,p.EARTH_LAYERS)
        self.assertAlmostEqual(grad/r/o['Omega2_s_minus2'],1.,delta=5e-7)
        self.assertAlmostEqual((second+3*grad/r)/o['kappa2_s_minus2'],1.,delta=1e-5)
    def test_small_alpha_linear_sensitivity(self):
        r=p.R_EARTH_MEAN+400e3
        a=p.near_circular_orbit_frequencies(r,p.MU_EARTH,p.EARTH_LAYERS,alpha=.001)['precession_rad_per_rev']
        b=p.near_circular_orbit_frequencies(r,p.MU_EARTH,p.EARTH_LAYERS,alpha=.002)['precession_rad_per_rev']
        self.assertAlmostEqual(b/a,2.,delta=.001)
