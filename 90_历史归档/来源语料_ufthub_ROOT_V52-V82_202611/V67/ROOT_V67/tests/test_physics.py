"""Test labels: MATH=mathematics; COND=conditional physics; TOY=toy model.
These unit tests do not establish a new fundamental theory.
"""
import math, random, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.root_v67 import *

class TestHelix(unittest.TestCase):
    def test_moving_frame_orthogonality(self):
        h=Helix(2.0,3.0,4.0)
        for t in [0,0.2,0.9]:
            v=h.velocity(t);a=h.acceleration(t)
            self.assertAlmostEqual(dot(v,a),0,places=10)
    def test_direct_curvature(self):
        h=Helix(1.9,2.3,1.17)
        for t in [0,0.7,2.1]:
            d=h.invariant_checks(t)
            self.assertAlmostEqual(d['kappa_direct'],h.kappa,places=11)
            self.assertAlmostEqual(d['torsion_direct'],h.torsion,places=11)
            self.assertAlmostEqual(d['normal_acceleration'],h.speed**2*h.kappa,places=11)
    def test_pure_circle(self):
        h=Helix(2,3,0)
        self.assertAlmostEqual(h.kappa,0.5)
        self.assertEqual(h.torsion,0)
    def test_pitch(self):
        h=Helix(3,2,4)
        self.assertAlmostEqual(math.tan(h.pitch_angle),2/3)
    def test_timelike_rejects_lightlike(self):
        h=Helix(1,C,0)
        self.assertFalse(h.particle_worldline_admissible())
        self.assertTrue(Helix(1,C/2,0).particle_worldline_admissible())
    def test_invalid_helix(self):
        with self.assertRaises(ValueError):Helix(0,1,1)
        with self.assertRaises(ValueError):inverse_helix(0,1,2)
    def test_torsion_handedness(self):
        self.assertAlmostEqual(Helix(1,2,4).torsion,-Helix(1,2,-4).torsion)
    def test_minkowski_null(self):
        self.assertAlmostEqual(minkowski_interval(3,3,0,0),0)
    def test_helix_angle_scaling(self):
        h=Helix(2,3,4); j=Helix(2,6,8)
        self.assertAlmostEqual(h.kappa,j.kappa)
        self.assertAlmostEqual(h.torsion,j.torsion)

class TestFields(unittest.TestCase):
    def test_EM_charge_sign(self):
        f=electromagnetic_force(2,(1,0,0),(0,2,0),(0,0,3))
        g=electromagnetic_force(-2,(1,0,0),(0,2,0),(0,0,3))
        self.assertEqual(f,tuple(-a for a in g))
    def test_magnetic_work_zero(self):
        v=(2.9,-0.7,1.1)
        f=electromagnetic_force(1,v,(0,0,0),(.5,-.1,2))
        self.assertAlmostEqual(dot(v,f),0,places=13)
    def test_three_forces_need_not_perpendicular(self):
        g=central_gravity((R_EARTH,0,0))
        e=electromagnetic_force(1,(0,1,0),(-1,0,0),(0,0,0))
        self.assertGreater(dot(g,e),0)
    def test_inverse_square(self):
        self.assertAlmostEqual(gravity_magnitude(2*R_EARTH),gravity_magnitude(R_EARTH)/4)
    def test_earth_reference(self):
        self.assertAlmostEqual(gravity_magnitude(R_EARTH),9.820302,places=4)
    def test_dipole_ratio(self):
        m=earth_dipole_moment()
        be=norm(dipole_magnetic((R_EARTH,0,0),m))
        bp=norm(dipole_magnetic((0,0,R_EARTH),m))
        self.assertAlmostEqual(bp/be,2,places=13)
    def test_dipole_not_real_igrf(self):
        self.assertGreater(norm(earth_dipole_moment()),0)
    def test_isco(self):
        self.assertAlmostEqual(schwarzschild_isco_radius(M_EARTH)/schwarzschild_radius(M_EARTH),3)
    def test_invalid_r(self):
        with self.assertRaises(ValueError):gravity_magnitude(0)
        with self.assertRaises(ValueError):dipole_magnetic((0,0,0),(0,0,1))
    def test_known_mass_ratio(self):
        self.assertTrue(1836<mass_ratio()<1837)
        self.assertGreater(abs(56*math.pi-mass_ratio()),1000)

class TestInduced(unittest.TestCase):
    def test_F_massless(self):self.assertEqual(threshold_F(0),1)
    def test_F_decay(self):self.assertGreater(threshold_F(0.2),threshold_F(2.0))
    def test_F_large(self):self.assertEqual(threshold_F(30),0)
    def test_F_zero_conformal(self):
        self.assertAlmostEqual(inverse_g_induced_delta(1e-35,1,1/6,0),0)
    def test_bare_not_predicted(self):
        ell=cutoff_length_fitted_to_G()
        self.assertAlmostEqual(g_from_length_cutoff(ell)/G,1,places=12)
    def test_doubling_N_halves_G(self):
        self.assertAlmostEqual(g_from_length_cutoff(1e-35,2),g_from_length_cutoff(1e-35,1)/2)
    def test_F_derivative(self):
        x=0.8;h=1e-5
        num=(threshold_F(x+h)-threshold_F(x-h))/(2*h)
        self.assertAlmostEqual(num,-2*x*expint_e1(x*x),delta=1e-9)
    def test_invalid_params(self):
        for op in [lambda:threshold_F(-1),lambda:expint_e1(-1),lambda:g_from_length_cutoff(0),lambda:inverse_g_induced_delta(-1)]:
            with self.assertRaises(ValueError):op()
    def test_planck_length(self):
        self.assertAlmostEqual(planck_length()/1e-35,1.616255,delta=0.00001)
    def test_small_mu(self):self.assertTrue(0<threshold_F(0.0001)<1)

class TestGaugeAndGravity(unittest.TestCase):
    def test_gauge_initial(self):
        a=gauge_inverse_at_mu(91.1876)
        self.assertAlmostEqual(a[0],59.0192406,places=6)
    def test_pair_intersection(self):
        for i,j in [(0,1),(0,2),(1,2)]:
            mu=gauge_pair_intersection(i,j)
            a=gauge_inverse_at_mu(mu)
            self.assertAlmostEqual(a[i],a[j],delta=1e-12)
    def test_not_single_SM_GUT_point(self):
        pairs=[gauge_pair_intersection(i,j) for i,j in [(0,1),(0,2),(1,2)]]
        self.assertGreater(max(pairs)/min(pairs),1000)
    def test_gauge_invalid(self):
        with self.assertRaises(ValueError):gauge_pair_intersection(1,1)
        with self.assertRaises(ValueError):gauge_inverse_at_mu(-2)
    def test_kk_one_form_invariance(self):
        k=1.7;A=(0.5,-2.2,1.0); dL=(0.13,0.05,-0.3); dx=(1.2,-.7,2.5);dy=-.8
        before=kk_one_form(dy,k,A,dx)
        after=kk_one_form(dy-k*dot(dL,dx),k,kk_gauge_transform(A,dL),dx)
        self.assertAlmostEqual(before,after)
    def test_yukawa_zero(self):self.assertEqual(yukawa_relative_accel(0,1,2),0)
    def test_yukawa_limit(self):self.assertAlmostEqual(yukawa_relative_accel(.3,0,2),.3)
    def test_eta_equal_charge(self):self.assertAlmostEqual(comp_dependent_eta(1,.3,.3,1,2),0)
    def test_ppn_gr_limit(self):
        gamma,ratio=scalar_tensor_ppn(1,1,0)
        self.assertEqual(gamma,1)
        self.assertEqual(ratio,1)
    def test_ppn_coupled(self):
        gamma,ratio=scalar_tensor_ppn(1,1,0.1)
        self.assertLess(gamma,1)
        self.assertGreater(ratio,1)
    def test_ppn_ghost_condition(self):
        with self.assertRaises(ValueError):scalar_tensor_ppn(1,-3,1)

# Explicitly named deterministic parameter-sweep tests, not counted as independent scientific experiments.
for i in range(48):
    def helix_case(self,index=i):
        radius=0.2+index/10;omega=0.3+(index%7);u=(index-24)/10
        h=Helix(radius,omega,u)
        r=inverse_helix(h.kappa,h.torsion,h.speed)
        self.assertAlmostEqual(r.radius,h.radius,delta=1e-11*max(1,h.radius))
        self.assertAlmostEqual(r.omega,h.omega,delta=1e-11*max(1,h.omega))
        self.assertAlmostEqual(r.axial_speed,h.axial_speed,delta=1e-11*max(1,abs(h.axial_speed)))
    setattr(TestHelix,f'test_parameter_inverse_{i:02d}',helix_case)
for i in range(24):
    def boost_case(self,index=i):
        beta=-0.93+1.86*index/23
        ct,x=(2.5+index/8,1.1-index/14)
        a=lorentz_boost_x(ct,x,beta)
        self.assertAlmostEqual(minkowski_interval(ct,x,0,0),minkowski_interval(*a,0,0),delta=1e-11*max(1,abs(ct)))
    setattr(TestHelix,f'test_lorentz_interval_{i:02d}',boost_case)
if __name__=='__main__':unittest.main(verbosity=2)

class TestChiralAnomalies(unittest.TestCase):
    def test_all_local_gauge_anomalies_cancel(self):
        from src.root_v67 import standard_model_one_generation_anomalies
        self.assertTrue(all(v==0 for v in standard_model_one_generation_anomalies().values()))
    def test_tree_ew_rho(self):
        from src.root_v67 import electroweak_tree_masses
        g,gp,v=.65,.35,246
        mw,mz=electroweak_tree_masses(g,gp,v)
        cos2=g*g/(g*g+gp*gp)
        self.assertAlmostEqual(mw*mw/(mz*mz*cos2),1,places=13)
    def test_tree_ew_invalid(self):
        from src.root_v67 import electroweak_tree_masses
        with self.assertRaises(ValueError):electroweak_tree_masses(.65,-.1,246)
    def test_electromagnetic_grav_ratio_p(self):
        from src.root_v67 import charged_pair_force_ratio
        self.assertTrue(1.2e36<charged_pair_force_ratio(MP,MP)<1.3e36)
    def test_electromagnetic_grav_ratio_e(self):
        from src.root_v67 import charged_pair_force_ratio
        self.assertTrue(4e42<charged_pair_force_ratio(ME,ME)<4.3e42)
