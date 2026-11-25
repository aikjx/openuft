import math
import unittest
from root_v147.flux import (FluxModel, illustrated, tuned_flat_vacuum,
                         six_d_coefficients)
from root_v147.numerics import numerical_drdC

class FluxTest(unittest.TestCase):
    def test_illustrated_parameters(self):
        p=illustrated(3)
        for x,y in ((p.A,1),(p.B,2),(p.C,1),(p.K4,2)):
            self.assertAlmostEqual(x,y)
    def test_flux_sign_vacuum_symmetry(self):
        for n in range(1,10):
            p=illustrated(n);q=illustrated(-n)
            self.assertEqual(p,q)
            for r in (.4,1,2,7):self.assertAlmostEqual(p.v(r),q.v(r))
    def test_example_n3_flat(self):
        e=illustrated(3).min(); self.assertAlmostEqual(e.radius,1)
        self.assertAlmostEqual(e.energy,0)
    def test_example_n3_radion_mass(self):
        e=illustrated(3).min();self.assertAlmostEqual(e.radial_mass2,1)
    def test_example_n3_factorization(self):
        p=illustrated(3)
        for r in (.1,.5,1,1.5,3):
            self.assertAlmostEqual(p.v(r),(r*r-1)**2/r**6,delta=1e-9*max(1,abs(p.v(r))))
    def test_example_n3_barrier(self):
        p=illustrated(3)
        mx=next(v for v in p.stationary() if v.kind=='maximum')
        self.assertAlmostEqual(mx.radius,math.sqrt(3))
        self.assertAlmostEqual(mx.energy,4/27)
    def test_decompactification_energy_limit(self):
        p=illustrated(3)
        self.assertGreater(p.v(10.),0)
        self.assertLess(p.v(10000.),p.v(10.))
        self.assertLess(p.v(10000.),1e-7)
    def test_barrier_stationary_derivative(self):
        p=illustrated(3)
        for v in p.stationary(): self.assertAlmostEqual(p.dv(v.radius),0,places=10)
    def test_n4_no_extrema(self):
        self.assertLess(illustrated(4).D,0)
        self.assertIsNone(illustrated(4).min())
    def test_n2_AdS_minimum(self):
        e=illustrated(2).min(); self.assertLess(e.energy,0)
        self.assertGreater(e.radial_mass2,0)
    def test_n0_no_minimum(self):
        self.assertIsNone(illustrated(0).min())
    def test_critical_degenerate(self):
        p=FluxModel(1,2,4/3,2)
        self.assertEqual(p.stationary()[0].kind,'degenerate')
        self.assertIsNone(p.min())
    def test_critical_sensitivity_grows(self):
        d=[]; masses=[]
        for delta in (.1,.01,.001,.0001):
            p=FluxModel(1,2,4/3*(1-delta),2)
            d.append(p.drdC_at_min()); masses.append(p.min().radial_mass2)
        self.assertTrue(all(d[i+1]>d[i] for i in range(3)))
        self.assertTrue(all(masses[i+1]<masses[i] for i in range(3)))
    def test_radion_mass_hessian_agrees(self):
        for n in (1,2,3):
            p=illustrated(n);e=p.min()
            self.assertAlmostEqual(e.radial_mass2,p.mass2_direct(e.radius),delta=1e-9)
    def test_analytical_derivative_C(self):
        p=FluxModel(1,2,.8,2)
        self.assertAlmostEqual(p.drdC_at_min(),numerical_drdC(1,2,.8,2),delta=1e-8)
    def test_potential_derivative_finite_difference(self):
        p=illustrated(3)
        for r in (.5,.8,1.2,2.4):
            h=r*1e-5
            self.assertAlmostEqual(p.dv(r),(p.v(r+h)-p.v(r-h))/(2*h),delta=1e-6*max(1,abs(p.dv(r))))
    def test_canonical_mass_finite_difference(self):
        p=illustrated(3);r=1.;h=1e-5
        d2=(p.dv(r+h)-p.dv(r-h))/(2*h)
        self.assertAlmostEqual(p.mass2_direct(r),r*r*d2/(4*p.K4),delta=1e-7)
    def test_flat_vacuum_tunable_any_nonzero_integer_n(self):
        for n in (-9,-3,-1,1,2,3,4,7,11):
            d=tuned_flat_vacuum(n)
            self.assertAlmostEqual(d['V'],0,delta=1e-10)
            self.assertGreater(d['m2'],0)
            self.assertGreater(d['G4'],0)
    def test_flat_vacuum_formula_R(self):
        for n in (1,2,7):
            d=tuned_flat_vacuum(n)
            self.assertAlmostEqual(d['Rstar']**2,.7*n*n/(4*1.5))
    def test_flat_flux_sign_degeneracy(self):
        for n in (1,2,3,7):
            self.assertEqual(tuned_flat_vacuum(n)['Rstar'],tuned_flat_vacuum(-n)['Rstar'])
    def test_no_n_zero_tuning(self):
        with self.assertRaises(ValueError):tuned_flat_vacuum(0)
    def test_invalid_radius(self):
        p=illustrated(3)
        for r in (-1,0,float('nan')):
            with self.assertRaises(ValueError):p.v(r)
    def test_invalid_coefficients(self):
        with self.assertRaises(ValueError):FluxModel(1,-1,2,1)
        with self.assertRaises(ValueError):FluxModel(1,2,-1,1)
    def test_6D_to_4D_gravity_matching(self):
        d=tuned_flat_vacuum(3)
        self.assertAlmostEqual(d['K4']/2,1/(16*math.pi*d['G4']))

if __name__=='__main__':unittest.main()
