import math
import unittest
from root_v146.model import (SixDimensional, Potential, illustrative_six_d,
                             theoretical_minkowski_parameters)

class TestDimensionalReduction(unittest.TestCase):
    def setUp(self):
        self.sd = illustrative_six_d(3)
        self.p = self.sd.reduce()

    def test_params(self):
        self.assertAlmostEqual(self.p.A,1)
        self.assertAlmostEqual(self.p.B,2)
        self.assertAlmostEqual(self.p.C,1)
        self.assertAlmostEqual(self.p.K4,2)
    def test_jordan_einstein_agree(self):
        for n in range(-5,6):
            sd=illustrative_six_d(n)
            for R in (.15,.4,.8,1,1.5,3,12):
                self.assertAlmostEqual(sd.reduce().v(R), sd.einstein_potential_direct(R),delta=1e-11*max(1,abs(sd.reduce().v(R))))
    def test_flux_integral(self):
        for n in range(-5,6):
            sd=illustrative_six_d(n)
            h=math.pi/4096
            integ=h/3*sum((1 if i in (0,4096) else (4 if i%2 else 2))*sd.f_theta_phi(i*h) for i in range(4097))*2*math.pi
            self.assertAlmostEqual(integ,sd.flux(),delta=1e-11)
    def test_fnorm(self):
        self.assertAlmostEqual(self.sd.f_squared(2),9/32)
    def test_sign_independent_flux_potential(self):
        self.assertEqual(illustrative_six_d(-3).reduce(),self.p)
    def test_G4_matching(self):
        self.assertAlmostEqual(1/(16*math.pi*self.sd.G4()),self.p.K4/2)
    def test_positive_G4(self):
        self.assertGreater(self.sd.G4(),0)
    def test_no_prediction_of_G4(self):
        a=SixDimensional(1,1,1,1,3)
        b=SixDimensional(2,1,1,1,3)
        self.assertAlmostEqual(a.G4()/b.G4(),2)
    def test_6d_Einstein_equations_at_tuned_flat_vacuum(self):
        e=self.sd.minkowski_einstein_residuals(1)
        self.assertAlmostEqual(e['external'],0,places=13)
        self.assertAlmostEqual(e['internal'],0,places=13)
    def test_6d_Einstein_equations_fail_for_n2(self):
        e=illustrative_six_d(2).minkowski_einstein_residuals(1)
        self.assertGreater(max(abs(v) for v in e.values()),1e-3)
    def test_6d_Einstein_equations_flat_at_tuned_other_flux(self):
        for n in (-5,-2,1,4,6):
            sd=theoretical_minkowski_parameters(n,1.5,.7,2.3)
            R=sd.reduce().stable().radius
            e=sd.minkowski_einstein_residuals(R)
            for val in e.values(): self.assertAlmostEqual(val,0,delta=1e-12)
    def test_internal_Monopole_Maxwell_equation(self):
        self.assertAlmostEqual(self.sd.maxwell_monopole_flux_density(2),3/8)
    def test_flat_requires_fine_tuning(self):
        e=self.sd.minkowski_einstein_residuals(1)
        self.assertAlmostEqual(e['external']+e['internal'], -self.sd.K6+2*self.sd.Lambda6)
    def test_flux_amplitude_n_squared(self):
        self.assertAlmostEqual(illustrative_six_d(2).reduce().C/illustrative_six_d(1).reduce().C,4)
    def test_derivative_finite_difference(self):
        for R in (.2,.5,1.,1.5,3.,7.):
            h=1e-5*R
            fd=(self.p.v(R+h)-self.p.v(R-h))/(2*h)
            self.assertAlmostEqual(fd,self.p.dv(R),delta=1e-6*max(1,abs(self.p.dv(R))))
    def test_second_derivative_finite_difference(self):
        for R in (.3,.8,1,2,4):
            h=1e-4*R
            fd=(self.p.dv(R+h)-self.p.dv(R-h))/(2*h)
            self.assertAlmostEqual(fd,self.p.d2v(R),delta=1e-5*max(1,abs(self.p.d2v(R))))
    def test_y_derivative(self):
        y=1.7
        h=1e-6
        fd=(self.p.v(math.sqrt(y+h))-self.p.v(math.sqrt(y-h)))/(2*h)
        self.assertAlmostEqual(fd,self.p.derivative_y(y),places=8)
    def test_bad_six_params(self):
        for args in ((0,1,1,1,1),(1,-1,1,1,1),(1,1,0,1,1),(1,1,1,0,1)):
            with self.assertRaises(ValueError): SixDimensional(*args)
    def test_non_integer_flux_rejected(self):
        with self.assertRaises(TypeError): SixDimensional(1,1,1,1,1.2)
    def test_negative_or_zero_radius_rejected(self):
        for r in (0,-1,math.inf,math.nan):
            with self.assertRaises(ValueError): self.p.v(r)
    def test_n_zero_has_no_stable_vacuum(self):
        self.assertIsNone(illustrative_six_d(0).reduce().stable())
    def test_no_lambda_case(self):
        sd=SixDimensional(1,0,1,1,3)
        p=sd.reduce()
        ex=p.stable()
        self.assertIsNotNone(ex)
        self.assertLess(ex.value,0)
    def test_minkowski_tune_family(self):
        for n in (-8,-4,-1,1,2,3,9):
            sd=theoretical_minkowski_parameters(n, 1.5, .7, 2.3)
            p=sd.reduce()
            e=p.stable()
            self.assertIsNotNone(e)
            self.assertAlmostEqual(e.value,0,delta=1e-9)
            self.assertGreater(e.mass2_homogeneous,0)
    def test_minkowski_n0_reject(self):
        with self.assertRaises(ValueError): theoretical_minkowski_parameters(0,1,1,1)
    def test_minkowski_critical_ratio(self):
        self.assertAlmostEqual(self.p.minkowski_tuning_residual(),0)
    def test_min_and_max(self):
        e=self.p.extrema()
        self.assertEqual([x.kind for x in e],['minimum','maximum'])
        self.assertAlmostEqual(e[0].radius,1)
        self.assertAlmostEqual(e[1].radius,math.sqrt(3))
    def test_minkowski_r0(self):
        self.assertAlmostEqual(self.p.v(1),0)
    def test_potential_factorization(self):
        for R in (.22,.5,1,1.3,3):
            self.assertAlmostEqual(self.p.v(R),(R*R-1)**2/R**6,delta=1e-11)
    def test_barrier(self):
        self.assertAlmostEqual(self.p.v(math.sqrt(3)),4/27)
    def test_radion_mass(self):
        self.assertAlmostEqual(self.p.mass2(1),1)
    def test_small_flux_min_is_AdS(self):
        for n in (1,2):
            self.assertLess(illustrative_six_d(n).reduce().stable().value,0)
    def test_n3_minkowski_and_n4_runaway(self):
        self.assertAlmostEqual(illustrative_six_d(3).reduce().stable().value,0)
        for n in (4,5,6):
            self.assertIsNone(illustrative_six_d(n).reduce().stable())
    def test_n4_no_stationary(self):
        self.assertLess(illustrative_six_d(4).reduce().discriminant(),0)
    def test_stationary_dv_zero(self):
        for n in (1,2,3):
            p=illustrative_six_d(n).reduce()
            for e in p.extrema():
                self.assertAlmostEqual(p.dv(e.radius),0,delta=1e-6)
    def test_stability_numeric_neighborhood(self):
        for n in (1,2,3):
            p=illustrative_six_d(n).reduce()
            e=p.stable()
            for frac in (.001,.01,.03):
                self.assertGreater(p.v(e.radius*(1+frac)),e.value)
                self.assertGreater(p.v(e.radius*(1-frac)),e.value)
    def test_critical_discriminant(self):
        p=Potential(A=1,B=2,C=4/3,K4=1)
        ex=p.extrema()
        self.assertEqual(len(ex),1)
        self.assertEqual(ex[0].kind,'degenerate')
        self.assertIsNone(p.stable())
    def test_no_flux_only_maximum(self):
        p=Potential(A=1,B=2,C=0,K4=1)
        self.assertEqual(p.extrema()[0].kind,'maximum')
    def test_zero_chi_flux_n_zero(self):
        p=Potential(1,2,0,1)
        self.assertIsNone(p.stable())
    def test_input_does_not_set_hbar_equal_one(self):
        self.assertFalse(hasattr(self.p,'hbar'))

if __name__=='__main__': unittest.main()
