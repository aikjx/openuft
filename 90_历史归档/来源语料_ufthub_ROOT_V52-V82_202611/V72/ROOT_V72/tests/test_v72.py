import unittest, math
import numpy as np
from scipy.linalg import expm
from rootv72 import physics as p, holonomy as h, experiment as e

class PhysicsTests(unittest.TestCase):
    def test_g_is_input(self):self.assertEqual(p.G,6.67430e-11)
    def test_c_exact(self):self.assertEqual(p.C,299792458)
    def test_earth_g(self):self.assertAlmostEqual(p.gravity(p.EARTH_M,p.EARTH_R),9.8203,3)
    def test_height_decrease(self):self.assertLess(p.gravity(p.EARTH_M,p.EARTH_R+400e3),p.gravity(p.EARTH_M,p.EARTH_R))
    def test_bad_mass(self):
        with self.assertRaises(ValueError):p.gravity(-1,1)
    def test_bad_radius(self):
        with self.assertRaises(ValueError):p.gravity(1,0)
    def test_tidal(self):self.assertAlmostEqual(p.tidal_gradient(p.EARTH_M,p.EARTH_R),3.08e-6,1)
    def test_centrifugal(self):self.assertAlmostEqual(p.centrifugal(p.EARTH_OMEGA,p.EARTH_R),.0339,3)
    def test_centrifugal_pole(self):self.assertAlmostEqual(p.centrifugal(p.EARTH_OMEGA,p.EARTH_R,math.pi/2),0,14)
    def test_rot_ratio_small(self):self.assertLess(p.rot_energy_ratio_uniform(p.EARTH_R,p.EARTH_OMEGA),1e-11)
    def test_redshift_mm(self):self.assertAlmostEqual(p.redshift(9.81,.001),1.0915e-19,23)
    def test_charge_reversal(self):self.assertEqual(p.electric_force(-2,(3,0,1)),tuple(-x for x in p.electric_force(2,(3,0,1))))
    def test_no_go_dimensions(self):self.assertNotEqual(p.dimension_no_go()['length_predicted'],p.dimension_no_go()['length_required'])
    def test_hypothesis_parity_double_flip(self):
        q=p.hypothetical_feature(1,.7,10,5,2)
        self.assertEqual(p.hypothetical_feature(-1,.7,-10,5,2),q)
    def test_hypothesis_single_flip(self):
        q=p.hypothetical_feature(1,.7,10,5,2)
        self.assertEqual(p.hypothetical_feature(-1,.7,10,5,2),-q)
    def test_hypothesis_bad_norm(self):
        with self.assertRaises(ValueError):p.hypothetical_feature(1,1,1,0,1)
    def test_planet_count(self):self.assertEqual(len(p.environments()),5)
    def test_sun_larger_earth(self):self.assertGreater(p.environments()[0]['g_m_s2'],p.environments()[1]['g_m_s2'])
    def test_earth_larger_moon(self):self.assertGreater(p.environments()[1]['g_m_s2'],p.environments()[2]['g_m_s2'])
    def test_helix_general(self):
        a=p.Helix(3,4,5)
        self.assertAlmostEqual(a.speed,13)
        self.assertAlmostEqual(a.curvature,3*16/169)
        self.assertAlmostEqual(a.torsion,20/169)
        self.assertEqual(a.acceleration,48)
    def test_helix_axial_reversal(self):
        a=p.Helix(3,4,5);b=p.Helix(3,4,-5)
        self.assertEqual(a.curvature,b.curvature)
        self.assertEqual(a.torsion,-b.torsion)
    def test_helix_omega_reversal(self):
        a=p.Helix(3,4,5);b=p.Helix(3,-4,5)
        self.assertEqual(a.curvature,b.curvature)
        self.assertEqual(a.torsion,-b.torsion)

class ConnectionTests(unittest.TestCase):
    def test_pauli_hermitian(self):
        for p0 in h.PAULI:self.assertTrue(np.allclose(p0,p0.conj().T))
    def test_pauli_traceless(self):
        for p0 in h.PAULI:self.assertAlmostEqual(np.trace(p0).real,0)
    def test_su2_commutator(self):self.assertTrue(np.allclose(h.curvature(h.T[0],h.T[1]),1j*h.T[2]))
    def test_so3_antisymmetric(self):
        for s in h.so3():self.assertTrue(np.allclose(s,-s.T))
    def test_product_curvature_exact(self):
        a,b=h.product_connections()
        self.assertTrue(np.allclose(h.curvature(a,b),h.separate_curvature(),atol=1e-14))
    def test_plaquette_unitary(self):
        a,b=h.su2();u=h.plaquette(a,b,.12)
        self.assertTrue(np.allclose(u.conj().T@u,np.eye(2),atol=1e-13))
    def test_plaquette_commutator_limit(self):
        a,b=h.su2();v=h.curvature(a,b)
        e1=np.linalg.norm((h.plaquette(a,b,.1)-np.eye(2))/.1**2-v)
        e2=np.linalg.norm((h.plaquette(a,b,.05)-np.eye(2))/.05**2-v)
        self.assertLess(e2,e1)
    def test_loop_gauge_conjugation(self):
        a,b=h.su2();u=h.plaquette(a,b,.12);V=expm(1j*.43*h.T[2]);g=h.transform_loop(u,V)
        self.assertAlmostEqual(np.trace(g).real,np.trace(u).real,13)
    def test_nonzero_curvature(self):
        a,b=h.product_connections();self.assertGreater(np.linalg.norm(h.curvature(a,b)),0)
    def test_wrong_edge(self):
        a,b=h.su2()
        with self.assertRaises(ValueError):h.plaquette(a,b,0)
    def test_flat_connection(self):
        a,b=h.su2()
        self.assertTrue(np.allclose(h.plaquette(a,a,.2),np.eye(2)))

class ExperimentTests(unittest.TestCase):
    def test_contrast_signal(self):
        self.assertAlmostEqual(e.contrast(9,3,1,7),3)
    def test_baseline_cancels(self):self.assertEqual(e.contrast(5,5,5,5),0)
    def test_h_only_cancels(self):self.assertEqual(e.contrast(3,3,-3,-3),0)
    def test_s_only_cancels(self):self.assertEqual(e.contrast(3,-3,3,-3),0)
    def test_hs_survives(self):self.assertEqual(e.contrast(5,-5,-5,5),5)
    def test_reproducible(self):self.assertEqual(e.generate(seed=12,repeats=1),e.generate(seed=12,repeats=1))
    def test_sample_size(self):self.assertEqual(len(e.generate(repeats=3)),36)
    def test_null_identification(self):self.assertEqual(e.fit(e.generate(beta=0)).rank,2)
    def test_injection_recovery(self):
        f=e.fit(e.generate());self.assertLess(abs(f.beta-3e-15),5*f.se)
    def test_nuisance_recovery(self):
        f=e.fit(e.generate());self.assertLess(abs(f.nuisance_hs+5e-16),4*f.se)
    def test_fisher(self):
        rows=e.generate(repeats=3);f=e.fit(rows)
        self.assertAlmostEqual(f.se,1/math.sqrt(e.fisher_information(rows)),25)
    def test_rank_deficiency(self):
        rows=e.generate(repeats=2)
        for row in rows:row['x']=1
        with self.assertRaises(ValueError):e.fit(rows)
    def test_rank_recovered_by_environments(self):self.assertEqual(e.fit(e.generate(repeats=2)).rank,2)
    def test_drift_false_positive(self):self.assertEqual(e.four_state_drift_quadratic(1e-15),1e-15)
    def test_null_p_range(self):
        f=e.fit(e.generate(seed=131,beta=0));self.assertTrue(0<=f.p_two_sided<=1)
    def test_small_noise_smaller_se(self):
        f1=e.fit(e.generate(),noise=1.2e-15)
        f2=e.fit(e.generate(noise=6e-16),noise=6e-16)
        self.assertLess(f2.se,f1.se)
    def test_repeats_better_precision(self):
        f1=e.fit(e.generate(repeats=4));f2=e.fit(e.generate(repeats=16))
        self.assertLess(f2.se,f1.se)
    def test_artifact_cannot_be_uniquely_excluded(self):
        a=e.generate(seed=33,beta=3e-15,repeats=2)
        b=e.generate(seed=33,beta=0,repeats=2)
        # Any unknown systematic proportional to x and hs is mathematically identical to beta*x.
        for ai,bi in zip(a,b):
            bi['contrast'] += 3e-15*bi['x']
            self.assertAlmostEqual(ai['contrast'],bi['contrast'],24)
        self.assertAlmostEqual(e.fit(a).beta,e.fit(b).beta,24)

if __name__=='__main__':unittest.main()
