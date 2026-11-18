import math, unittest
import numpy as np
from rootv70.physics import (BODIES,G,C,EARTH_J2,EARTH_A,EARTH_OMEGA,Body,
    gravity_central,gravitational_potential_j2,gravity_j2,rotating_apparent,
    field_at,enclosed_mass_piecewise,gravity_piecewise,gravity_clock_shift,
    curvature_length_effect,helix_kinematics,local_boost_kinematics)

class GravityBaseline(unittest.TestCase):
    def setUp(self): self.e=BODIES['Earth']
    def test_earth_surface_gravity_range(self):
        self.assertTrue(9.7<self.e.g<9.9)
    def test_moon_surface_gravity_range(self):
        self.assertTrue(1.5<BODIES['Moon'].g<1.8)
    def test_jupiter_surface_gravity_is_not_density_order(self):
        self.assertLess(BODIES['Jupiter'].density,self.e.density)
        self.assertGreater(BODIES['Jupiter'].g,self.e.g)
    def test_central_acceleration_sign(self):
        np.testing.assert_allclose(gravity_central(1,[1,0,0]),[-1,0,0])
    def test_central_inverse_square(self):
        a=gravity_central(self.e.mu,[self.e.radius,0,0])
        b=gravity_central(self.e.mu,[2*self.e.radius,0,0])
        np.testing.assert_allclose(b,a/4)
    def test_central_invalid_origin(self):
        with self.assertRaises(ValueError):gravity_central(2,[0,0,0])
    def test_gravity_gradient_of_negative_potential(self):
        p=np.array([7e6,2e6,4e6]); h=2.
        calc=[]
        for k in range(3):
            dp=np.zeros(3);dp[k]=h
            calc.append(-(gravitational_potential_j2(self.e,p+dp)-gravitational_potential_j2(self.e,p-dp))/(2*h))
        np.testing.assert_allclose(gravity_j2(self.e,p),calc,rtol=1e-8,atol=1e-10)
    def test_j2_correction_equatorial_stronger(self):
        p=np.array([EARTH_A,0,0])
        self.assertGreater(np.linalg.norm(gravity_j2(self.e,p)),np.linalg.norm(gravity_central(self.e.mu,p)))
    def test_j2_correction_polar_weaker_at_equal_r(self):
        p=[0,0,EARTH_A]
        self.assertLess(np.linalg.norm(gravity_j2(self.e,p)),np.linalg.norm(gravity_central(self.e.mu,p)))
    def test_j2_zero_gives_central(self):
        b=Body('dummy',2e24,1e6,10,.2)
        p=[1.2e6,2.2e6,3.5e6]
        np.testing.assert_allclose(gravity_j2(b,p),gravity_central(b.mu,p))
    def test_j2_potential_on_equator(self):
        u=gravitational_potential_j2(self.e,[EARTH_A,0,0]); self.assertLess(u,-self.e.mu/EARTH_A)
    def test_rotational_centrifugal_outward(self):
        vec=rotating_apparent(self.e,[EARTH_A,0,0])
        np.testing.assert_allclose(vec,[EARTH_OMEGA**2*EARTH_A,0,0],rtol=3e-5)
    def test_rotational_zero_on_pole(self):
        np.testing.assert_allclose(rotating_apparent(self.e,[0,0,EARTH_A]),[0,0,0])
    def test_coriolis_deflects_eastward_north(self):
        vec=rotating_apparent(self.e,[0,0,EARTH_A],[100,0,0]); self.assertLess(vec[1],0)
    def test_effective_gravity_less_than_gravity_equator(self):
        f=field_at(self.e,0)
        self.assertLess(f['effective'],f['gravity'])
    def test_pole_no_centrifugal(self):
        f=field_at(self.e,90)
        self.assertAlmostEqual(f['effective'],f['gravity'],delta=1e-12)
    def test_gravity_along_altitude_decreases(self):
        self.assertLess(field_at(self.e,0,400e3)['gravity'],field_at(self.e,0)['gravity'])
    def test_tidal_radial_formula(self):
        a=field_at(self.e,20,200e3)
        self.assertAlmostEqual(a['tidal_radial'],2*self.e.mu/a['radius']**3,places=14)
    def test_tidal_gradient_central_finite_difference(self):
        r=self.e.radius+4e5;dr=1.
        calc=(self.e.mu/(r-dr)**2-self.e.mu/(r+dr)**2)/(2*dr)
        self.assertAlmostEqual(calc,2*self.e.mu/r**3,delta=1e-12)
    def test_clock_shift_1mm(self):
        shift=gravity_clock_shift(self.e,.001)
        expected=self.e.g*.001/C**2
        self.assertAlmostEqual(shift,expected,delta=expected*5e-8)
    def test_clock_shift_zero(self):
        self.assertEqual(gravity_clock_shift(self.e,0),0)
    def test_clock_shift_negative_rejected(self):
        with self.assertRaises(ValueError): gravity_clock_shift(self.e,-1)
    def test_kretschmann_scaling_with_radius(self):
        k1=field_at(self.e,0)['kretschmann']
        k2=field_at(self.e,0,self.e.radius)['kretschmann']
        self.assertAlmostEqual(k1/k2,64,places=10)
    def test_curvature_planck_suppression(self):
        self.assertLess(curvature_length_effect(self.e,1.616255e-35),1e-170)
    def test_uniform_sphere_mass(self):
        rho=5000; R=5e6
        self.assertAlmostEqual(enclosed_mass_piecewise(R,[R],[rho]),4*math.pi/3*rho*R**3,delta=1e10)
    def test_uniform_sphere_internal_linear_g(self):
        r=1e6;rho=5000; R=5e6
        self.assertAlmostEqual(gravity_piecewise(r,[R],[rho]),4*math.pi*G*rho*r/3,places=12)
    def test_shell_theorem_exterior_mass(self):
        R=5e6;rho=5000
        M=enclosed_mass_piecewise(R,[R],[rho]);r=2*R
        self.assertAlmostEqual(gravity_piecewise(r,[R],[rho]),G*M/r**2,places=12)
    def test_different_internal_density_same_external_gravity(self):
        R=6e6;rho=5500
        two=[1.5*rho,(1-1.5*0.5**3)/(1-0.5**3)*rho]
        for r in [R,1.3*R,2*R]:
            self.assertAlmostEqual(gravity_piecewise(r,[R],[rho]),gravity_piecewise(r,[R/2,R],two),places=10)
        self.assertGreater(gravity_piecewise(.25*R,[R/2,R],two),gravity_piecewise(.25*R,[R],[rho]))
    def test_invalid_shell_density(self):
        with self.assertRaises(ValueError):enclosed_mass_piecewise(1,[2,1],[4,5])
    def test_negative_altitude_rejected(self):
        with self.assertRaises(ValueError):field_at(self.e,0,-10)
    def test_timelike_gamma(self):
        g,inv=local_boost_kinematics(.8*C)
        self.assertAlmostEqual(g,5/3,places=13)
        self.assertAlmostEqual(inv,.6,places=13)
    def test_massive_speed_of_light_rejected(self):
        with self.assertRaises(ValueError):local_boost_kinematics(C)
    def test_helix_circular(self):
        h=helix_kinematics(2,3,0)
        self.assertAlmostEqual(h['curvature'],.5)
        self.assertAlmostEqual(h['torsion'],0)
    def test_helix_torsion(self):
        h=helix_kinematics(2,3,4)
        self.assertAlmostEqual(h['curvature'],18/52)
        self.assertAlmostEqual(h['torsion'],12/52)
    def test_helix_straight_limit(self):
        h=helix_kinematics(2,0,4)
        self.assertAlmostEqual(h['curvature'],0)
        self.assertAlmostEqual(h['torsion'],0)

if __name__=='__main__':unittest.main()
