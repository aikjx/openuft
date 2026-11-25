import math
import unittest
from root_v149.core import Helix,helix_for_alpha,ALPHA

class TestHelix(unittest.TestCase):
    def test_lab_null(self): self.assertAlmostEqual(helix_for_alpha().speed2(),1.0,14)
    def test_fit_input_recovered(self): self.assertAlmostEqual(helix_for_alpha().alpha_proxy(),ALPHA,14)
    def test_curvature_torsion_relation(self):
        h=helix_for_alpha(); self.assertAlmostEqual(h.curvature()**2+h.torsion()**2,h.omega**2,13)
    def test_axial_comoving_zero_torsion(self):
        h=helix_for_alpha(); self.assertAlmostEqual(h.boost_z(h.u).torsion(),0.0,12)
    def test_axial_comoving_alpha_proxy_is_one(self):
        h=helix_for_alpha(); self.assertAlmostEqual(h.boost_z(h.u).alpha_proxy(),1.0,13)
    def test_boost_changes_ratio(self):
        h=helix_for_alpha(); self.assertGreater(abs(h.alpha_proxy()-h.boost_z(h.u).alpha_proxy()),0.9)
    def test_boost_frequency(self):
        h=helix_for_alpha(); b=0.45
        D=(1-b*h.u)/math.sqrt(1-b*b)
        self.assertAlmostEqual(h.boost_z(b).omega,h.omega/D,12)
    def test_boost_axial_speed(self):
        h=helix_for_alpha(); b=0.45
        self.assertAlmostEqual(h.boost_z(b).u,(h.u-b)/(1-b*h.u),14)
    def test_boost_radius_invariant(self):
        h=helix_for_alpha(); self.assertEqual(h.boost_z(0.91).a,h.a)
    def test_null_preserved_grid(self):
        for alpha in [1e-7,0.001,ALPHA,0.2,0.5,0.99]:
            h=helix_for_alpha(alpha)
            for b in [-0.9,-0.4,0,0.3,0.85,0.99]:
                with self.subTest(alpha=alpha,beta=b):
                    self.assertAlmostEqual(h.boost_z(b).speed2(),1.0,11)
    def test_recovered_curve_original(self):
        h=helix_for_alpha(0.35,omega=3.7)
        r=math.sqrt(h.curvature()**2+h.torsion()**2)
        self.assertAlmostEqual(r,h.omega,12)
        self.assertAlmostEqual(h.curvature()/r**2,h.a,12)
        self.assertAlmostEqual(h.torsion()/r,h.u,12)
    def test_tangent_unit(self):
        h=helix_for_alpha()
        for t in [0,0.03,2,100]:
            with self.subTest(t=t): self.assertAlmostEqual(sum(x*x for x in h.tangent(t)),1.0,13)
    def test_acceleration_normal(self):
        h=helix_for_alpha()
        for t in [0,.11,2.0]:
            with self.subTest(t=t):
                v=h.tangent(t); a=h.acceleration(t)
                self.assertAlmostEqual(sum(x*y for x,y in zip(v,a)),0.0,13)
    def test_acceleration_nonzero(self):
        h=helix_for_alpha(); self.assertGreater(sum(x*x for x in h.acceleration(0)),0)
    def test_coordinate_boost_matches_helix(self):
        h=helix_for_alpha(.2,omega=1.5); b=.4; t=1.3
        z=h.u*t
        g=1/math.sqrt(1-b*b)
        tp=g*(t-b*z); zp=g*(z-b*t)
        hp=h.boost_z(b)
        xp=hp.position(tp)
        p=h.position(t)
        for x,y in zip(xp[:2],p[:2]): self.assertAlmostEqual(x,y,12)
        self.assertAlmostEqual(xp[2],zp,12)
    def test_invalid_alpha_zero(self):
        with self.assertRaises(ValueError):helix_for_alpha(0)
    def test_invalid_alpha_one(self):
        with self.assertRaises(ValueError):helix_for_alpha(1)
    def test_invalid_omega(self):
        with self.assertRaises(ValueError):helix_for_alpha(ALPHA,-2)
    def test_invalid_speed(self):
        with self.assertRaises(ValueError):Helix(.5,1,.3)
    def test_invalid_null_beta(self):
        with self.assertRaises(ValueError):helix_for_alpha().boost_z(1)
    def test_invalid_negative_radius(self):
        with self.assertRaises(ValueError):Helix(-1,1,0)
    def test_well_defined_negative_axial_speed(self):
        h=Helix(.6,1,-.8); self.assertAlmostEqual(h.torsion(),-.8,14)
    def test_axial_boost_reverse(self):
        h=helix_for_alpha(.7); hp=h.boost_z(.5).boost_z(-.5)
        self.assertAlmostEqual(hp.omega,h.omega,13)
        self.assertAlmostEqual(hp.u,h.u,13)
