"""Deterministic correctness checks for stated equations, not experimental proof."""
import math
import unittest
from src import physics as p


class HelixTests(unittest.TestCase):
    def test_speed_constraint_0_to_90(self):
        for a in (0,1,15,35,45,89,90):
            h=p.helix(2.,a)
            self.assertAlmostEqual(p.norm(h.velocity(2e-9))/p.C,1.,places=13)
            self.assertAlmostEqual(h.azimuthal_m_s**2+h.axial_m_s**2,p.C**2,delta=30.)

    def test_curvature_and_torsion(self):
        h=p.helix(4.,30)
        self.assertAlmostEqual(h.curvature_m_inv,0.75/4,places=13)
        self.assertAlmostEqual(h.torsion_m_inv,math.sin(math.radians(30))*math.cos(math.radians(30))/4,places=13)

    def test_v_dot_a_is_zero(self):
        h=p.helix(0.7,45,speed_m_s=3.7)
        for t in (0,0.3,4.1):
            self.assertAlmostEqual(p.dot(h.velocity(t),h.acceleration(t)),0,delta=1e-11)

    def test_numerical_derivatives(self):
        h=p.helix(2.0,35,speed_m_s=4.0)
        t=0.25
        dt=1e-5
        pos_plus=h.position(t+dt);pos_minus=h.position(t-dt)
        v_fd=tuple((x-y)/(2*dt) for x,y in zip(pos_plus,pos_minus))
        self.assertLess(p.norm(tuple(a-b for a,b in zip(v_fd,h.velocity(t)))),1e-8)
        vel_plus=h.velocity(t+dt);vel_minus=h.velocity(t-dt)
        a_fd=tuple((x-y)/(2*dt) for x,y in zip(vel_plus,vel_minus))
        self.assertLess(p.norm(tuple(a-b for a,b in zip(a_fd,h.acceleration(t)))),1e-7)

    def test_straight_axis(self):
        h=p.helix(4,90)
        self.assertLess(h.curvature_m_inv,1e-30)
        self.assertLess(h.torsion_m_inv,1e-16)

    def test_invalid_radius_and_angle(self):
        with self.assertRaises(ValueError):p.helix(-1,30)
        with self.assertRaises(ValueError):p.helix(1,110)


class WaveTests(unittest.TestCase):
    def test_massless_cylindrical_group_speed_c(self):
        w=p.cylindrical_wave_mode(0.2,10,30.)
        self.assertAlmostEqual(w.group_speed_m_s/p.C,1.,places=14)
        self.assertAlmostEqual(w.omega_rad_s/p.C,math.hypot(50,30),places=13)
        self.assertAlmostEqual(w.energy_j/p.HBAR,w.omega_rad_s,delta=1e-5)

    def test_massive_wave_sub_luminal(self):
        w=p.cylindrical_wave_mode(0.1,10,50,rest_mass_kg=1e-34)
        self.assertLess(w.group_speed_m_s,p.C)
        self.assertGreater(w.energy_j,0)

    def test_discrete_winding(self):
        with self.assertRaises(ValueError):p.cylindrical_wave_mode(1,0,1)
        with self.assertRaises(ValueError):p.cylindrical_wave_mode(1,0.5,1)


class InducedGravityTests(unittest.TestCase):
    def test_energy_length_units_inverse(self):
        for ell in (1e-35,1e-15,0.5):
            self.assertAlmostEqual(p.cutoff_length_m(p.cutoff_energy_j(ell))/ell,1.,places=13)

    def test_planck_length(self):
        self.assertAlmostEqual(p.planck_length_m()/1.616255e-35,1,delta=2e-6)

    def test_minimal_scalar_massless_coeff(self):
        ell=1e-35
        G=p.induced_G(1,ell)
        self.assertAlmostEqual(G,12*math.pi*p.C**3*ell**2/p.HBAR,delta=1e-12*G)

    def test_N_scaling(self):
        ell=1e-35
        self.assertAlmostEqual(p.induced_G(20,ell)*20,p.induced_G(1,ell),delta=1e-11*p.induced_G(1,ell))

    def test_xi_conformal_vanish(self):
        self.assertEqual(p.induced_inverse_G(3,1e-35,xi=1/6),0.)
        self.assertTrue(math.isinf(p.induced_G(3,1e-35,xi=1/6)))

    def test_negative_induced_curvature_weight(self):
        self.assertLess(p.induced_inverse_G(1,1e-35,xi=0.25),0)

    def test_calibration_is_invertible_not_prediction(self):
        for N in (1,2,10,100):
            ell=p.calibrated_length_m(N=N)
            self.assertAlmostEqual(p.induced_G(N,ell)/p.G_CODATA_2022,1,places=13)

    def test_calibrated_ell_1(self):
        self.assertAlmostEqual(p.calibrated_length_m()/p.planck_length_m(),1/math.sqrt(12*math.pi),places=12)

    def test_mass_cutoff_factor(self):
        self.assertAlmostEqual(p.proper_time_mass_factor(0),1.,places=14)
        self.assertAlmostEqual(p.proper_time_mass_factor(1),0.148495506775922,delta=1e-8)
        self.assertGreater(p.proper_time_mass_factor(0.2),p.proper_time_mass_factor(1))
        self.assertLess(p.proper_time_mass_factor(1),p.proper_time_mass_factor(0))

    def test_mass_suppresses_induced_1_over_G(self):
        ell=1e-35
        self.assertLess(p.induced_inverse_G(1,ell,mu=1.),p.induced_inverse_G(1,ell,mu=0.))

    def test_bare_coupling_additivity(self):
        ell=1e-35
        bare=5e9
        delta=p.induced_inverse_G(1,ell,bare_inverse_G=bare)-p.induced_inverse_G(1,ell)
        self.assertAlmostEqual(delta,bare,delta=1e-6)

    def test_invalid_sign_calibration(self):
        with self.assertRaises(ValueError):p.calibrated_length_m(xi=0.3)


class ConventionalTests(unittest.TestCase):
    def test_gravity_surface(self):
        self.assertTrue(9.7<p.earth_g_m_s2()<9.9)

    def test_inverse_square(self):
        g0=p.earth_g_m_s2(0)
        self.assertAlmostEqual(p.earth_g_m_s2(p.R_EARTH)/g0,0.25,places=14)

    def test_dipole_equator_pole(self):
        eq=p.norm(p.dipole_B_tesla((p.R_EARTH,0,0)))
        pole=p.norm(p.dipole_B_tesla((0,0,p.R_EARTH)))
        self.assertAlmostEqual(pole/eq,2,places=13)

    def test_magnetic_force_orthogonal_to_B_and_v(self):
        v=(2.3,3.1,-4.2); B=(1e-5,-2e-5,3e-5)
        f=p.lorentz_force(v,B,p.H)
        self.assertAlmostEqual(p.dot(f,v),0,delta=1e-47)
        self.assertAlmostEqual(p.dot(f,B),0,delta=1e-47)

    def test_gravity_electric_not_orthogonal(self):
        gravitational=(0.,0.,-10.)
        electrical=(0.,0.,-2.)
        self.assertNotEqual(p.dot(gravitational,electrical),0.)

    def test_yukawa_limiting_values(self):
        self.assertAlmostEqual(p.yukawa_relative_accel(0.2,0,1),0.2)
        self.assertLess(p.yukawa_relative_accel(0.2,30,1),1e-10)

    def test_old_alpha_formula_is_approx_not_identity(self):
        alpha=7.2973525643e-3  # CODATA 2022
        rel=abs(p.old_alpha_guess()-alpha)/alpha
        self.assertGreater(rel,1e-6)
        self.assertLess(rel,1e-5)

    def test_old_proton_mass_ratio_arithmetic_false(self):
        self.assertAlmostEqual(p.old_mass_ratio_guess(),56*math.pi,places=12)
        self.assertNotAlmostEqual(p.old_mass_ratio_guess(),1836.15267343,delta=1)


class ConsistencyExtensions(unittest.TestCase):
    def test_frenet_frame_is_orthonormal(self):
        h=p.helix(3,40,speed_m_s=123)
        for t in (0,0.07,1.1):
            T,N,B=p.frenet_frame(h,t)
            for v in (T,N,B): self.assertAlmostEqual(p.norm(v),1.,places=12)
            for a,b in ((T,N),(T,B),(N,B)):
                self.assertAlmostEqual(p.dot(a,b),0,places=12)

    def test_frenet_frame_not_defined_for_straight_trajectory(self):
        with self.assertRaises(ValueError):p.frenet_frame(p.helix(2,90))

    def test_lorentz_interval_invariance(self):
        ct,z=13.5,5.2
        inv=ct*ct-z*z
        for beta in (-.999,-.5,0.,.7,.999):
            ct1,z1=p.lorentz_boost_z(ct,z,beta)
            self.assertAlmostEqual(ct1**2-z1**2,inv,delta=1e-9)

    def test_lorentz_boost_invalid(self):
        for beta in (-1.,1.,1.2):
            with self.assertRaises(ValueError):p.lorentz_boost_z(1.,2.,beta)

    def test_em_wave_magnitudes_orthogonality_and_poynting(self):
        for z,t in ((0.,0.),(.4,0.),(.3,1e-9)):
            E,B=p.electromagnetic_plane_wave(z,t,1000.,2.)
            self.assertAlmostEqual(p.dot(E,B),0.,places=12)
            self.assertAlmostEqual(p.norm(E),p.C*p.norm(B),delta=1e-11)
            self.assertGreaterEqual(p.cross(E,B)[2],-1e-17)

    def test_em_wave_faraday_equation_numerically(self):
        # x component: -(dE_y/dz) = -dB_x/dt
        z,t=.123,1.27e-9; dz=1e-5;dt=1e-14
        ey1=p.electromagnetic_plane_wave(z+dz,t,100.,2.)[0][1]
        ey0=p.electromagnetic_plane_wave(z-dz,t,100.,2.)[0][1]
        bx1=p.electromagnetic_plane_wave(z,t+dt,100.,2.)[1][0]
        bx0=p.electromagnetic_plane_wave(z,t-dt,100.,2.)[1][0]
        self.assertAlmostEqual((ey1-ey0)/(2*dz), (bx1-bx0)/(2*dt),delta=5e-5)

    def test_induced_mass_weight_monotone_and_bounded(self):
        vals=[p.proper_time_mass_factor(x) for x in (0.,0.05,.2,.5,1.,2.,4.)]
        self.assertEqual(vals[0],1.)
        self.assertTrue(all(0<=x<=1 for x in vals))
        self.assertTrue(all(x>y for x,y in zip(vals,vals[1:])))

    def test_formal_vacuum_density_cutoff_scaling(self):
        d=p.vacuum_energy_magnitude_j_m3(1e-35)
        self.assertAlmostEqual(p.vacuum_energy_magnitude_j_m3(2e-35)/d,1/16,places=14)

    def test_finite_mass_decreases_required_induced_inverse_g(self):
        u=p.induced_inverse_G(10,1e-35,mu=0.7)
        m=p.induced_inverse_G(10,1e-35,mu=0.0)
        self.assertLess(u,m)
        self.assertGreater(u,0)

    def test_yukawa_is_not_inverse_square_except_limits(self):
        a=p.yukawa_relative_accel(0.1,1.,2.)
        b=p.yukawa_relative_accel(0.1,10.,2.)
        self.assertGreater(a,b)


if __name__=='__main__': unittest.main()
