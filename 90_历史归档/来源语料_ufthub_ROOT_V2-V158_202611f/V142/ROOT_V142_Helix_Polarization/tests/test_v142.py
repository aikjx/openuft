import unittest,math,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.physics import helix,helix_kinematics,inverse_null_helix,wave,maxwell_residuals,noether_mode_count,scalar_pair_field,projected_berry_xy
from src.symbolic_checks import run_symbolic

class TestV142(unittest.TestCase):
    def test_symbolic_all(self):
        self.assertTrue(run_symbolic()['symbolic_assertions_passed'])
    def test_null_speed(self):
        for a,u in ((0.6,0.8),(0.8,0.6),(0.3,math.sqrt(0.91))):
            self.assertAlmostEqual(helix_kinematics(a,1,u)['speed'],1)
    def test_curvature(self):
        self.assertAlmostEqual(helix_kinematics(.6,1,.8)['curvature'],.6)
    def test_torsion(self):
        self.assertAlmostEqual(helix_kinematics(.6,1,.8)['torsion'],.8)
    def test_speed_general(self):
        d=helix_kinematics(1,2,3)
        self.assertAlmostEqual(d['speed'],math.sqrt(13))
    def test_frenet_angular_speed(self):
        self.assertAlmostEqual(helix_kinematics(.6,1,.8)['frame_angular_speed'],1)
    def test_inversion(self):
        a,w,u=inverse_null_helix(.6,.8)
        self.assertAlmostEqual(a,.6)
        self.assertAlmostEqual(w,1)
        self.assertAlmostEqual(u,.8)
    def test_inversion_many(self):
        for a,u in ((.2,math.sqrt(.96)),(.4,math.sqrt(.84)),(.9,math.sqrt(.19))):
            k=helix_kinematics(a,1,u)
            ai,wi,ui=inverse_null_helix(k['curvature'],k['torsion'])
            self.assertAlmostEqual(ai,a)
            self.assertAlmostEqual(wi,1)
            self.assertAlmostEqual(ui,u)
    def test_acceleration(self):
        self.assertAlmostEqual(helix_kinematics(.6,1,.8)['acceleration'],.6)
    def test_helix_pos_origin(self):
        self.assertTrue(np.allclose(helix(.6,1,.8,0),[.6,0,0]))
    def test_helix_one_period(self):
        t=2*math.pi
        self.assertTrue(np.allclose(helix(.6,1,.8,t)[:2],[.6,0],atol=1e-13))
    def test_helix_pitch(self):
        self.assertAlmostEqual(helix(.6,1,.8,2*math.pi)[2],.8*2*math.pi)
    def test_nonpositive_radius(self):
        with self.assertRaises(ValueError):helix_kinematics(0,1,1)
    def test_zero_frequency(self):
        with self.assertRaises(ValueError):helix_kinematics(1,0,1)
    def test_degenerate_reconstruction(self):
        with self.assertRaises(ValueError):inverse_null_helix(0,.1)
    def test_wave_orthogonal(self):
        for t,z in ((0,0),(.4,.7),(1,3),(10,2)):
            E,B=wave(t,z)
            self.assertAlmostEqual(np.dot(E,B),0)
    def test_wave_equal_magnitude(self):
        for t in (.1,.3,4.2):
            E,B=wave(t,.2)
            self.assertAlmostEqual(np.linalg.norm(E),np.linalg.norm(B))
    def test_wave_energy_flux_plus_z(self):
        for t in (0,.2,1.25):
            E,B=wave(t,0)
            self.assertTrue(np.allclose(np.cross(E,B),[0,0,1]))
    def test_wave_energy_flux_negative_for_wrong_sign(self):
        E,B=wave(0,0,magnetic_sign=-1)
        self.assertTrue(np.allclose(np.cross(E,B),[0,0,-1]))
    def test_faraday_zero(self):
        for t,z in ((0,0),(.4,.7),(10,3)):
            r,_=maxwell_residuals(t,z)
            self.assertTrue(np.allclose(r,[0,0,0]))
    def test_ampere_zero(self):
        for t,z in ((0,0),(.4,.7),(10,3)):
            _,r=maxwell_residuals(t,z)
            self.assertTrue(np.allclose(r,[0,0,0]))
    def test_wrong_faraday_nonzero(self):
        a,_=maxwell_residuals(0,0,magnetic_sign=-1)
        self.assertAlmostEqual(np.linalg.norm(a),2)
    def test_wrong_ampere_nonzero(self):
        _,a=maxwell_residuals(0,0,magnetic_sign=-1)
        self.assertAlmostEqual(np.linalg.norm(a),2)
    def test_correct_any_k_amp(self):
        for k,A in ((.2,10),(3.,.7),(10.,1.)):
            a,b=maxwell_residuals(.1,.7,k,A)
            self.assertTrue(np.allclose(a,0))
            self.assertTrue(np.allclose(b,0))
    def test_wave_flux_amplitude_scaling(self):
        E,B=wave(.2,.5,amplitude=3)
        self.assertAlmostEqual(np.cross(E,B)[2],9)
    def test_gauge_photon_dof(self):
        self.assertEqual(noether_mode_count(2,0),2)
    def test_proca_dof(self):
        self.assertEqual(noether_mode_count(0,2),3)
    def test_scalar_pair_quartic(self):
        q1=scalar_pair_field(.1)['L_density'];q2=scalar_pair_field(.2)['L_density']
        self.assertAlmostEqual(q2/q1,16)
    def test_scalar_pair_quadratic_absent(self):
        q=scalar_pair_field(0)
        self.assertEqual(q['F_xy'],0)
        self.assertEqual(q['L_density'],0)
    def test_scalar_pair_F_second_order(self):
        q1=scalar_pair_field(.1)['F_xy'];q2=scalar_pair_field(.2)['F_xy']
        self.assertAlmostEqual(q2/q1,4)
    def test_berry_nonzero(self):
        self.assertAlmostEqual(projected_berry_xy(math.pi/2,1,2),1)
    def test_berry_zero_in_zero_twist(self):
        self.assertEqual(projected_berry_xy(.2,1,0),0)
    def test_berry_odd_about_zero(self):
        self.assertAlmostEqual(projected_berry_xy(-.5,.8,1),-projected_berry_xy(.5,.8,1))
    def test_null_helix_not_geodesic(self):
        self.assertGreater(helix_kinematics(.6,1,.8)['acceleration'],0)
    def test_dimensional_gravity(self):
        # G: L/M; R: L^-2; d^4x: L^4 => R d^4x /G = M L = hbar
        L,M=2.1,3.4
        G=L/M;R=1/L**2;d4x=L**4
        self.assertAlmostEqual(R*d4x/G,M*L)
    def test_dimensional_em(self):
        # A: L^-1, F: L^-2; F^2 d4x dimensionless, multiplied by hbar
        L=2.3
        self.assertAlmostEqual((1/L**4)*L**4,1.)
    def test_em_wave_null_invariants(self):
        for t in (.1,.3,2.):
            E,B=wave(t,.25)
            self.assertAlmostEqual(np.dot(E,B),0)
            self.assertAlmostEqual(np.dot(B,B)-np.dot(E,E),0)

if __name__=='__main__': unittest.main()
