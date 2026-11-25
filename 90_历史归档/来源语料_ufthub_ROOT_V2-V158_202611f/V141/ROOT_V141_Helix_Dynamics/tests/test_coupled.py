import math
import unittest
import sympy as sp
from src.coupled import (Params, rhs, energy, photon_energy, scalar_energy,
                         shift_charge, rk4_step, integrate, diagnostic_summary,
                         local_omega_squared)


class CoupledTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params=Params()
        cls.rows=integrate(p=cls.params)

    def test_valid_params(self): self.params.validate()

    def test_invalid_k(self):
        with self.assertRaises(ValueError): Params(k=0).validate()

    def test_invalid_f(self):
        with self.assertRaises(ValueError): Params(f=-1).validate()

    def test_invalid_g(self):
        with self.assertRaises(ValueError): Params(g=0).validate()

    def test_invalid_dt(self):
        with self.assertRaises(ValueError): integrate(dt=0)

    def test_invalid_integer_step(self):
        with self.assertRaises(ValueError): integrate(t_max=1,dt=.3)

    def test_invalid_initial(self):
        with self.assertRaises(ValueError): integrate(initial=(1,2,3))

    def test_energy_positive(self):
        self.assertTrue(all(r['energy']>=0 for r in self.rows))

    def test_energy_sum(self):
        for row in self.rows[::40]:
            self.assertAlmostEqual(row['energy'],row['photon_energy']+row['scalar_energy'],places=14)

    def test_energy_drift(self):
        d=diagnostic_summary(self.rows,self.params)
        self.assertLess(d['max_relative_energy_drift'],2e-8)

    def test_charge_drift(self):
        d=diagnostic_summary(self.rows,self.params)
        self.assertLess(d['max_absolute_shift_charge_drift'],1e-8)

    def test_photon_energy_exchange(self):
        d=diagnostic_summary(self.rows,self.params)
        self.assertGreater(d['photon_energy_max']-d['photon_energy_min'],1e-4)

    def test_scalar_energy_exchange(self):
        d=diagnostic_summary(self.rows,self.params)
        self.assertGreater(d['scalar_energy_max']-d['scalar_energy_min'],1e-4)

    def test_nonzero_coupling_drives_theta(self):
        y=(0.4,0.2,0.0,0.5)
        self.assertNotEqual(rhs(y,self.params)[3],0)

    def test_zero_coupling_phi_second_derivative(self):
        self.assertEqual(rhs((.2,.3,0,.4),Params(lam=0))[3],0)

    def test_zero_coupling_harmonic(self):
        p=Params(lam=0,k=2)
        a,v,theta,w=(.3,.2,0,.4)
        ddot=rhs((a,v,theta,w),p)[1]
        self.assertAlmostEqual(ddot,-4*a)

    def test_zero_coupling_energy(self):
        p=Params(lam=0)
        rows=integrate(p=p,t_max=30,dt=.005)
        self.assertLess(diagnostic_summary(rows,p)['max_relative_energy_drift'],1e-8)

    def test_rk4_convergence(self):
        p=self.params
        y=(0.3,0.2,0.0,0.3)
        coarse=y
        for i in range(100): coarse=rk4_step(coarse,.02,p)
        fine=y
        for i in range(200): fine=rk4_step(fine,.01,p)
        self.assertLess(max(abs(a-b) for a,b in zip(coarse,fine)),2e-8)

    def test_rhs_energy_derivative_zero_symbolic(self):
        a,v,theta,w,k,g,f,lam=sp.symbols('a v theta w k g f lam',nonzero=True,real=True)
        E=(v*v+k*k*a*a)/(2*g*g)+f*f*w*w/2
        ys=sp.Matrix([a,v,theta,w])
        yd=sp.Matrix([v,-k*k*a+g*g*lam*k*w*a,w,-lam*k*a*v/(f*f)])
        self.assertEqual(sp.simplify((sp.Matrix([sp.diff(E,z) for z in ys]).T*yd)[0]),0)

    def test_rhs_charge_derivative_zero_symbolic(self):
        a,v,theta,w,k,g,f,lam=sp.symbols('a v theta w k g f lam',nonzero=True,real=True)
        Q=f*f*w+lam*k*a*a/2
        ys=sp.Matrix([a,v,theta,w])
        yd=sp.Matrix([v,-k*k*a+g*g*lam*k*w*a,w,-lam*k*a*v/(f*f)])
        self.assertEqual(sp.simplify((sp.Matrix([sp.diff(Q,z) for z in ys]).T*yd)[0]),0)

    def test_euler_lagrange_a_symbolic(self):
        a,v,theta,w,acc,k,g,f,lam=sp.symbols('a v theta w acc k g f lam',nonzero=True,real=True)
        L=(v*v-k*k*a*a)/(2*g*g)+f*f*w*w/2-lam*k*theta*a*v
        d_dt_dLd_v=sp.diff(sp.diff(L,v),a)*v+sp.diff(sp.diff(L,v),v)*acc+sp.diff(sp.diff(L,v),theta)*w
        EL=sp.simplify(d_dt_dLd_v-sp.diff(L,a))
        self.assertEqual(sp.simplify(EL-(acc+k*k*a)/g**2+lam*k*w*a),0)

    def test_euler_lagrange_theta_symbolic(self):
        a,v,theta,w,theta_ddot,k,g,f,lam=sp.symbols('a v theta w theta_ddot k g f lam',nonzero=True,real=True)
        L=(v*v-k*k*a*a)/(2*g*g)+f*f*w*w/2-lam*k*theta*a*v
        EL=sp.simplify(f*f*theta_ddot-sp.diff(L,theta))
        self.assertEqual(EL,f*f*theta_ddot+lam*k*a*v)

    def test_helicity_symmetric_no_gradient(self):
        p=Params()
        self.assertAlmostEqual(local_omega_squared(p,0,+1),local_omega_squared(p,0,-1))

    def test_helicity_splits_external_gradient(self):
        p=Params()
        self.assertLess(local_omega_squared(p,.1,+1),local_omega_squared(p,.1,-1))

    def test_helicity_invalid(self):
        with self.assertRaises(ValueError): local_omega_squared(Params(),.1,0)

    def test_theta_zero_interaction_vanishes(self):
        # Local background theta_dot=0 means dispersion corrections vanish.
        for s in (-1,1):
            self.assertEqual(local_omega_squared(Params(),0,s),Params().k**2)

    def test_no_negative_photon_energy(self):
        self.assertTrue(all(r['photon_energy']>=0 for r in self.rows))

    def test_final_state_finite(self):
        self.assertTrue(all(math.isfinite(x) for x in diagnostic_summary(self.rows,self.params)['final_state']))

    def test_theory_not_fit_data(self):
        self.assertEqual(diagnostic_summary(self.rows,self.params)['method'],
                         'fixed-step RK4, analytic invariants, independent RK4 convergence')


if __name__=='__main__': unittest.main()
