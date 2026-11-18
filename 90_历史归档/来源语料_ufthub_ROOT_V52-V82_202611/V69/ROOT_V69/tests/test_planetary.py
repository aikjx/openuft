"""V69 physical, boundary, negative and numerical derivative tests."""
import sys, math, unittest, random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from planetary import *

B=load_bodies(); EARTH=B['Earth']

class PlanetaryTests(unittest.TestCase):
    def test_population(self):self.assertEqual(len(B),10)
    def test_mass_density_consistency(self):
        for b in B.values(): self.assertAlmostEqual(4/3*math.pi*b.mean_radius_m**3*b.density/b.mass_kg,1.,places=13)
    def test_all_planets_positive(self):
        for b in B.values():
            d=surface_stats(b)
            self.assertGreater(d['g_spherical_m_s2'],0)
            self.assertGreater(d['v_escape_m_s'],d['v_circular_m_s'])
            self.assertLess(d['compactness_rs_over_R'],0.01)
    def test_nasa_benchmark_earth(self):
        v=surface_stats(EARTH)
        self.assertAlmostEqual(v['g_spherical_m_s2'],9.82,delta=.04)
    def test_nasa_benchmark_moon(self):self.assertAlmostEqual(surface_stats(B['Moon'])['g_spherical_m_s2'],1.62,delta=.04)
    def test_nasa_benchmark_sun(self):self.assertAlmostEqual(surface_stats(B['Sun'])['g_spherical_m_s2'],274,delta=2)
    def test_nasa_benchmark_mars(self):self.assertAlmostEqual(surface_stats(B['Mars'])['g_spherical_m_s2'],3.71,delta=.05)
    def test_nasa_benchmark_jupiter(self):self.assertAlmostEqual(surface_stats(B['Jupiter'])['g_spherical_m_s2'],25.92,delta=.5)
    def test_density_fixed_radius(self):
        a=density_gravity(3000,1e6);self.assertAlmostEqual(density_gravity(6000,1e6)/a,2)
    def test_density_fixed_density_size(self):
        a=density_gravity(3000,1e6);self.assertAlmostEqual(density_gravity(3000,2e6)/a,2)
    def test_composition_fixed_MR_no_effect(self):
        self.assertEqual(uniform_sphere_accel(10**25,1e7,1e7),uniform_sphere_accel(10**25,1e7,1e7))
    def test_layered_total_mass_exact(self):self.assertAlmostEqual(earth_toy_layers().mass/EARTH.mass_kg,1,places=13)
    def test_layered_surface_same(self):
        l=earth_toy_layers();self.assertAlmostEqual(l.accel(l.radius),uniform_sphere_accel(l.mass,l.radius,l.radius),places=12)
    def test_layered_center_zero(self):self.assertEqual(earth_toy_layers().accel(0),0)
    def test_layered_interior_differs(self):
        l=earth_toy_layers();r=.3*l.radius
        self.assertGreater(l.accel(r),uniform_sphere_accel(l.mass,l.radius,r))
    def test_gauss_piecewise(self):
        l=earth_toy_layers()
        for x in [.1,.2,.5,.7,1.,1.3]:
            r=x*l.radius
            self.assertAlmostEqual(l.accel(r)*r*r/G/l.enclosed_mass(r),1,places=12)
    def test_layered_hydrostatic_pressure_positive(self):self.assertGreater(earth_toy_layers().hydrostatic_pressure(n=1200),0)
    def test_uniform_sphere_internal_linear(self):
        self.assertAlmostEqual(uniform_sphere_accel(1e24,5e6,2e6)*2,
                               uniform_sphere_accel(1e24,5e6,4e6),places=12)
    def test_uniform_sphere_surface_continuous(self):
        m=1e24;R=5e6
        self.assertAlmostEqual(uniform_sphere_accel(m,R,R),G*m/R**2,places=12)
    def test_j2_is_gradient(self):
        # Numerical finite diff of potential, independent formula implementation
        for r in [(7e6,1e6,3e6),(8e6,2e6,0.),(4e6,3e6,8e6)]:
            v=j2_accel(EARTH,r)
            for i in range(3):
                h=10.
                plus=list(r);minus=list(r);plus[i]+=h;minus[i]-=h
                d=-(j2_potential(EARTH,plus)-j2_potential(EARTH,minus))/(2*h)
                self.assertAlmostEqual(v[i],d,delta=max(1e-8,abs(v[i])*5e-8))
    def test_j2_zero_monopole(self):
        from dataclasses import replace
        e=replace(EARTH,J2=0.0);r=(7e6,2e6,3e6)
        self.assertAlmostEqual(norm(sub(j2_accel(e,r),point_accel(e.mu,r))),0.,delta=1e-14)
    def test_earth_equator_effective(self):self.assertAlmostEqual(earth_surface_field(0)['g_effective_m_s2'],9.780,delta=.008)
    def test_earth_pole_effective(self):self.assertAlmostEqual(earth_surface_field(90)['g_effective_m_s2'],9.832,delta=.008)
    def test_earth_J2_nonzero(self):
        self.assertNotAlmostEqual(earth_surface_field(45)['g_effective_m_s2'],earth_surface_field(45,include_J2=False)['g_effective_m_s2'],places=4)
    def test_altitude_weaker(self):self.assertLess(earth_surface_field(45,400e3)['g_gravity_m_s2'],earth_surface_field(45)['g_gravity_m_s2'])
    def test_centrifugal_equator(self):
        e=earth_surface_field(0)
        self.assertLess(e['g_effective_m_s2'],e['g_gravity_m_s2'])
    def test_pole_centrifugal_zero(self):self.assertAlmostEqual(earth_surface_field(90)['g_effective_m_s2'],earth_surface_field(90)['g_gravity_m_s2'],places=11)
    def test_coriolis_anti_perpendicular(self):
        v=(123.,12.,45.);f=coriolis_accel(EARTH_OMEGA,v)
        self.assertAlmostEqual(dot(v,f),0.,delta=1e-15)
    def test_inertial_translation_gravity(self):
        r=(7e6,0,0); self.assertEqual(point_accel(EARTH.mu,r),point_accel(EARTH.mu,r))
        # Uniform boost leaves acceleration and relative position unchanged in Newtonian limit
        vt=(2e4,-1e4,0.); dt=1000.
        b1=add(r,mul(dt,vt));b0=mul(dt,vt)
        self.assertAlmostEqual(norm(sub(point_accel(EARTH.mu,sub(b1,b0)),point_accel(EARTH.mu,r))),0,delta=1e-14)
    def test_tidal_radial_sign(self):
        R=(AU,0.,0.);x=(1000.,0.,0.)
        self.assertGreater(tidal_relative_accel(B['Sun'].mu,R,x)[0],0)
    def test_tidal_transverse_sign(self):
        self.assertLess(tidal_relative_accel(B['Sun'].mu,(AU,0,0),(0,1000.,0))[1],0)
    def test_tidal_linear_scale(self):
        a=norm(tidal_relative_accel(B['Moon'].mu,(384400e3,0,0),(1000.,0,0)))
        b=norm(tidal_relative_accel(B['Moon'].mu,(384400e3,0,0),(2000.,0,0)))
        self.assertAlmostEqual(b/a,2,delta=3e-5)
    def test_frame_dragging_tiny(self):
        v=lense_thirring_precession(EARTH,(EARTH.mean_radius_m,0,0))
        self.assertGreater(norm(v),0);self.assertLess(norm(v),1e-12)
    def test_spin_reversal_changes_sign(self):
        from dataclasses import replace
        flip=replace(EARTH,rotation_hours=-EARTH.rotation_hours)
        x=(EARTH.mean_radius_m,0,0)
        v1=lense_thirring_precession(EARTH,x);v2=lense_thirring_precession(flip,x)
        self.assertAlmostEqual(norm(add(v1,v2)),0,delta=1e-28)
    def test_yukawa_unity_alpha0(self):
        self.assertAlmostEqual(yukawa_accel(EARTH.mu,EARTH.mean_radius_m,0,.49,.5,1e8),EARTH.mu/EARTH.mean_radius_m**2)
    def test_eotvos_charge_sign(self):
        self.assertGreater(eotvos_yukawa(EARTH.mean_radius_m,1e9,1e-12),0)
        self.assertLess(eotvos_yukawa(EARTH.mean_radius_m,1e9,-1e-12),0)
    def test_eotvos_small_alpha_linear(self):
        eta=eotvos_yukawa(EARTH.mean_radius_m,1e10,1e-13)
        prediction=1e-13*.49*(z_over_a('Ti')-z_over_a('Pt'))*yukawa_factor(EARTH.mean_radius_m,1e10)
        self.assertAlmostEqual(eta,prediction,delta=3e-16)
    def test_eta_bound_order(self):
        a=alpha_bound_toy(7e-15)
        self.assertLess(a,1e-12);self.assertGreater(a,1e-14)
    def test_yukawa_short_range(self):
        self.assertLess(yukawa_factor(1e8,1e4),1e-100)
    def test_electron_grav_1m(self):
        e=gravitational_energy_eV(9.1093837139e-31,1.)
        self.assertAlmostEqual(e,5.57e-11,delta=1e-13)
    def test_atom_Bohr_extremely_small(self):
        e=gravitational_energy_eV(9.1093837139e-31,5.29177210903e-11)
        self.assertLess(e,1e-19)
    def test_grav_clock_1m(self):
        self.assertAlmostEqual(gravitational_redshift_fraction(9.81,1),1.091e-16,delta=1e-19)
    def test_dimensional_obstruction(self):self.assertFalse(dimension_G_obstruction()['constructible'])
    def test_GM_scaling_degeneracy(self):
        for k in [.01,.1,1.,10.,100.]:self.assertAlmostEqual(gm_degeneracy(G,EARTH.mass_kg,k),1.,places=12)
    def test_helix_finite(self):
        h=helix(5.,30.,10.)
        self.assertAlmostEqual(h['curvature'],.15)
        self.assertAlmostEqual(h['torsion'],math.sqrt(3)/20)
    def test_helix_pure_axial(self):self.assertEqual(helix(2.,90.,10.)['curvature'],0.)
    def test_helix_geometry_not_G(self):self.assertNotIn('G',helix(1.,30.))
    def test_source_EM_energy_positive(self): self.assertGreater(source_energy_density_from_field(B=1.),0)
    def test_inequality_input_bad(self):
        for f,args in [(j2_accel,(EARTH,(0,0,0))),
                       (uniform_sphere_accel,(1,0,1)),
                       (ecef_geodetic_earth,(100,)),
                       (yukawa_factor,(1.,0.)),
                       (point_accel,(1,(0,0,0)))]:
            with self.assertRaises(ValueError):f(*args)

if __name__=='__main__':unittest.main(verbosity=2)

class OrbitalAndMicroTests(unittest.TestCase):
    def test_circular_orbit_1_period_verlet(self):
        b=EARTH;r0=7e6;v0=math.sqrt(b.mu/r0)
        T=2*math.pi*math.sqrt(r0**3/b.mu)
        r=(r0,0.,0.);v=(0.,v0,0.);E=orbital_energy_per_mass(r,v,b.mu)
        dt=T/4000
        for i in range(4000):r,v=kepler_verlet_step(r,v,b.mu,dt)
        self.assertLess(norm(sub(r,(r0,0.,0.)))/r0,3e-5)
        self.assertLess(abs(orbital_energy_per_mass(r,v,b.mu)/E-1),1e-9)
    def test_orbit_boost_no_absolute_space(self):
        b=EARTH;r=(7e6,0.,0.);v=(0,1000.,0.)
        baseline=point_accel(b.mu,r)
        boost=(30000.,0.,-10000.)
        dt=1e3
        position_lab=add(r,mul(dt,boost))
        center_lab=mul(dt,boost)
        self.assertLess(norm(sub(point_accel(b.mu,sub(position_lab,center_lab)),baseline)),1e-12)
    def test_tidal_radial_grad(self):
        b=EARTH;r=7e6;length=1.;dr=10.
        # analytic leading gradient of spherical acceleration magnitude
        exact=b.mu*(1/(r-length/2)**2-1/(r+length/2)**2)
        self.assertAlmostEqual(earth_tidal_gradient_radial(b.mu,r,length),exact,delta=1e-10)
    def test_microscope_not_no_gravity(self):
        self.assertGreater(EARTH.mu/(EARTH.mean_radius_m+710e3)**2,7.5)
    def test_figure_G_scaling(self):
        self.assertAlmostEqual(gm_degeneracy(G,EARTH.mass_kg,2),1.)
