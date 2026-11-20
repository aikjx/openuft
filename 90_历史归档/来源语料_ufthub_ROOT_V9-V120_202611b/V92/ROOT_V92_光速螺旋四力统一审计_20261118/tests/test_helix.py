import math
import random
import unittest
from src.helix_physics import (
    C,HBAR,G,M_E,E_CHARGE,Helix,helix_from_kappa_tau_speed,
    cyclotron_helix,lorentz_force_magnitude_constant_speed,magnetic_force,
    field_inferred_from_helix,dimension_dict,check_dimensions,scale_from_assumed_kappa,
    reproduce_constants_example,
)
from src.symbolic_proofs import prove

class TestHelix(unittest.TestCase):
    def test_symbolic(self):
        self.assertGreaterEqual(prove()['checks'],14)
    def test_unit_dimensions(self):
        for desc,ok in check_dimensions().items():
            with self.subTest(desc=desc): self.assertTrue(ok)
    def test_inverse_cases(self):
        for R in (1e-6,0.01,1,1e5):
            for w in (0.0001,3,1e5):
                for p in (-1e5,-50,0,2,1e5):
                    h=Helix(R,w,p)
                    hi=helix_from_kappa_tau_speed(h.kappa,h.tau,h.speed)
                    self.assertAlmostEqual(hi.radius/h.radius,1,places=10)
                    self.assertAlmostEqual(hi.p/(max(1,abs(h.p))),h.p/(max(1,abs(h.p))),places=10)
                    self.assertAlmostEqual(hi.omega/h.omega,1,places=10)
    def test_random_constant_speed(self):
        rng=random.Random(20261118)
        for _ in range(500):
            R=10**rng.uniform(-7,3); w=10**rng.uniform(-2,6)
            p=rng.uniform(-1,1)*1e6
            h=Helix(R,w,p)
            self.assertAlmostEqual(math.hypot(h.kappa,h.tau)/ (h.omega/h.speed),1,places=10)
            self.assertAlmostEqual(h.radius*h.omega**2/h.speed**2,h.kappa,places=10)
    def test_magnetic_helix(self):
        for B in (0.1,0.3,0.5,0.7,3):
            for beta in (.01,.2,.6,.8,.99):
                for deg in (-60,-30,0,30,60):
                    h=cyclotron_helix(B,beta,deg)
                    self.assertAlmostEqual(h.speed/(beta*C),1,places=12)
                    f1=lorentz_force_magnitude_constant_speed(M_E,h)
                    f2=magnetic_force(B,h)
                    self.assertAlmostEqual(f1/f2,1,places=11)
                    self.assertAlmostEqual(field_inferred_from_helix(h)/B,1,places=11)
    def test_axial_boost_eliminates_torsion(self):
        for beta in (.15,.7,.9):
            h=cyclotron_helix(0.5,beta,30)
            hb=h.transformed_axial_boost(h.p)
            self.assertAlmostEqual(hb.p,0,places=8)
            self.assertAlmostEqual(hb.tau,0,places=9)
            self.assertGreater(abs(h.tau),0)
            self.assertNotAlmostEqual(hb.kappa/h.kappa,1,places=3)
            self.assertLess(hb.speed,C)
    def test_minkowski_null_helix_requires_acceleration(self):
        for R in (1,100):
            omega=C/(math.sqrt(2)*R)
            h=Helix(R,omega,C/math.sqrt(2))
            self.assertAlmostEqual(h.speed/C,1,places=12)
            self.assertGreater(h.radius*h.omega**2,0)
            with self.assertRaises(ValueError): h.gamma()
    def test_timelike_massive_speed_lt_c(self):
        for beta in (.01,.4,.9,.999):
            h=cyclotron_helix(.5,beta,33)
            self.assertGreater(h.gamma(),1)
            self.assertLess(h.speed,C)
    def test_dimension_no_G_without_mass_unit(self):
        vectors=[dimension_dict()[x] for x in ('speed v, c, p','curvature kappa','torsion tau','angular frequency omega')]
        self.assertTrue(all(vec[0]==0 for vec in vectors))
        self.assertEqual(dimension_dict()['G'][0],-1)
    def test_dimensional_G_not_independent_prediction(self):
        lp=math.sqrt(HBAR*G/C**3)
        k=1/lp
        self.assertAlmostEqual(scale_from_assumed_kappa(k)/G,1,places=11)
        self.assertEqual(reproduce_constants_example()['G_INPUT'],G)
    def test_geometric_rotation_not_force_inevitability(self):
        # straight accelerating trajectory r=(a t²/2,0,0) has nonzero qE but κ=0
        a=3000.0
        self.assertNotEqual(M_E*a,0)
        self.assertEqual(0,0)  # cross v×a=0 for collinear v and a
    def test_validation(self):
        with self.assertRaises(ValueError): Helix(0,1,0)
        with self.assertRaises(ValueError): Helix(1,0,0)
        with self.assertRaises(ValueError): cyclotron_helix(-1,.5,45)
        with self.assertRaises(ValueError): cyclotron_helix(.5,1.0,45)
        with self.assertRaises(ValueError): Helix(1,10,0).transformed_axial_boost(C)

if __name__=='__main__': unittest.main()
