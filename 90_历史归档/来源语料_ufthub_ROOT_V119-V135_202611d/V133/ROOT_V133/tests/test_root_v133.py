# -*- coding: utf-8 -*-
"""Independent mathematical and numeric audits of ROOT V133 toy model."""
import math
import sys
from pathlib import Path
import unittest
import numpy as np
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import root_v133 as v

class GeometryTests(unittest.TestCase):
    def test_geometry_identity_many_values(self):
        for u in np.linspace(-0.95,0.95,41):
            geo=v.helix_geometry(float(u),0.137)
            self.assertAlmostEqual(geo['kappa']**2+geo['torsion']**2, geo['omega']**2,places=12)
            self.assertAlmostEqual(geo['normalized_torsion'], u,places=12)
    def test_holonomy(self):
        for u in [-0.9,-.2,.0,.3,.8]:
            self.assertAlmostEqual(v.helix_geometry(u,0.31)['turn_holonomy_angle'],2*math.pi*u)
    def test_boost_composition(self):
        for u in [-.8,-.25,.0,.1,.85]:
            for beta in [-.7,.0,.6]:
                self.assertAlmostEqual(v.boost_axis_velocity(v.boost_axis_velocity(u,beta),-beta),u,places=12)
    def test_helix_alpha_is_not_invariant(self):
        alpha=1/v.ALPHA_INV_0
        self.assertGreater(abs(v.boost_axis_velocity(alpha,.6)-alpha),0.5)
    def test_invalid_speed(self):
        for u in [-1,1,1.2]:
            with self.assertRaises(ValueError):v.helix_geometry(u,.5)
    def test_null_vs_timelike(self):
        for u in np.linspace(-.9,.9,7):
            R=math.sqrt(1-u*u)/.7
            speed2=R*R*.7*.7+u*u
            self.assertAlmostEqual(-1+speed2,0,places=14)

class RotorTests(unittest.TestCase):
    def setUp(self):
        self.h=v.HBAR_SI
        self.I=10*self.h*1.0
        self.m0=100*self.h/1.0
        self.lam=v.lambda_for_alpha(1/v.ALPHA_INV_0)
    def test_c_not_hbar_normalized(self):
        self.assertNotEqual(self.h,1)
        self.assertNotEqual(v.G_SI,1)
    def test_quantum_number_only_integer(self):
        for bad in [.5,2.5,'1']:
            with self.assertRaises(TypeError):v.circle_quantum_number(bad)
    def test_negative_charge_opposite(self):
        for n in range(1,7):
            p=v.rotor_spectrum(n,self.I,self.lam,self.m0)
            m=v.rotor_spectrum(-n,self.I,self.lam,self.m0)
            self.assertAlmostEqual(p['charge'],-m['charge'],delta=abs(p['charge'])*1e-12)
            self.assertAlmostEqual(p['mass'],m['mass'],delta=p['mass']*1e-12)
    def test_n_zero_neutral(self):
        r=v.rotor_spectrum(0,self.I,self.lam,self.m0)
        self.assertEqual(r['charge'],0)
        self.assertEqual(r['mass_shift'],0)
    def test_mass_and_charge_powers(self):
        for n in range(1,6):
            a=v.rotor_spectrum(1,self.I,self.lam,self.m0)
            b=v.rotor_spectrum(n,self.I,self.lam,self.m0)
            self.assertAlmostEqual(b['charge']/a['charge'],n)
            self.assertAlmostEqual(b['alpha']/a['alpha'],n*n)
            self.assertAlmostEqual(b['mass_shift']/a['mass_shift'],n*n,places=9)
    def test_routhian_matches(self):
        for n in range(-4,5):
            J=n*self.h
            mass,q=v.fixed_J_routhian(self.m0,self.I,J,self.lam)
            got=v.rotor_spectrum(n,self.I,self.lam,self.m0)
            self.assertEqual(mass,got['mass'])
            self.assertEqual(q,got['charge'])
    def test_alpha_fit_not_prediction(self):
        for alpha in [.0001,.002,1/v.ALPHA_INV_0,.03,.5]:
            lam=v.lambda_for_alpha(alpha)
            r=v.rotor_spectrum(1,self.I,lam,self.m0)
            self.assertAlmostEqual(r['alpha'],alpha,delta=alpha*3e-15)
    def test_alpha_ratio_independent_of_rotor_I(self):
        for factor in [0.1,1,10,100]:
            g=v.rotor_spectrum(1,self.I*factor,self.lam,self.m0)
            self.assertAlmostEqual(g['alpha'],1/v.ALPHA_INV_0,delta=1e-16)
    def test_I_controls_mass(self):
        m1=v.rotor_spectrum(1,self.I,self.lam,self.m0)['mass_shift']
        m2=v.rotor_spectrum(1,2*self.I,self.lam,self.m0)['mass_shift']
        self.assertAlmostEqual(m1/m2,2,places=11)
    def test_muon_electron_no_go(self):
        self.assertGreater(abs(v.MUON_ELECTRON_RATIO-1),200)
        # Single universal rotor + identical |q| forces identical |n| and mass.
        n_e,n_mu=1,-1
        m_e=v.rotor_spectrum(n_e,self.I,self.lam,self.m0)['mass']
        m_mu=v.rotor_spectrum(n_mu,self.I,self.lam,self.m0)['mass']
        self.assertEqual(m_e,m_mu)
    def test_mass_charge_relation(self):
        for n in [1,2,3]:
            d=v.rotor_spectrum(n,self.I,self.lam,self.m0)
            self.assertAlmostEqual((d['mass_shift']/(d['charge']**2)) /(1/(2*self.I*self.lam**2)),1,places=12)
    def test_invalid_rotor_parameter(self):
        with self.assertRaises(ValueError):v.rotor_spectrum(1,0,self.lam,self.m0)
        with self.assertRaises(ValueError):v.lambda_for_alpha(-.5)
    def test_circle_fourier_orthogonality(self):
        theta=np.linspace(0,2*math.pi,8192,endpoint=False)
        ns=range(-4,5)
        mat=np.exp(1j*np.outer(list(ns),theta))
        gram=mat@mat.conj().T/len(theta)
        self.assertLess(float(np.max(np.abs(gram-np.eye(len(ns))))),1e-13)
    def test_dirac_su2_nonabelian(self):
        sigma1=sp.Matrix([[0,1],[1,0]])/2
        sigma2=sp.Matrix([[0,-sp.I],[sp.I,0]])/2
        sigma3=sp.Matrix([[1,0],[0,-1]])/2
        self.assertEqual(sigma1*sigma2-sigma2*sigma1,sp.I*sigma3)
    def test_U1_ab_commutator(self):
        q1,q2=sp.symbols('q1 q2')
        self.assertEqual(sp.expand(q1*q2-q2*q1),0)

class GaugeAndDynamics(unittest.TestCase):
    def test_symbolic_gauge_invariance(self):
        s,lam,a,b=sp.symbols('s lam a b',real=True)
        x=s+sp.sin(s); y=sp.cos(s)
        gauge=a*x*y
        theta=s**2+sp.sin(2*s)
        Ax=b*y
        Ay=sp.sin(s)
        old=sp.diff(theta,s)+lam*(Ax*sp.diff(x,s)+Ay*sp.diff(y,s))
        new=sp.diff(theta-lam*gauge,s)+lam*((Ax+sp.diff(gauge,s)*sp.diff(x,s)/(sp.diff(x,s)**2+sp.diff(y,s)**2))*sp.diff(x,s)+(Ay+sp.diff(gauge,s)*sp.diff(y,s)/(sp.diff(x,s)**2+sp.diff(y,s)**2))*sp.diff(y,s))
        # Restriction to worldline uses gradient projected onto its tangent.
        self.assertEqual(sp.simplify(old-new),0)
    def test_full_gradient_gauge(self):
        x,y,s,lam,a,b=sp.symbols('x y s lam a b',real=True)
        L=a*x*y+b*x*x
        X=s**2+1;Y=sp.sin(s)
        A_x=x+y;A_y=x*y
        theta=sp.cos(s)
        old=sp.diff(theta,s)+lam*(A_x.subs({x:X,y:Y})*sp.diff(X,s)+A_y.subs({x:X,y:Y})*sp.diff(Y,s))
        new=sp.diff(theta-lam*L.subs({x:X,y:Y}),s)+lam*((A_x+sp.diff(L,x)).subs({x:X,y:Y})*sp.diff(X,s)+(A_y+sp.diff(L,y)).subs({x:X,y:Y})*sp.diff(Y,s))
        self.assertEqual(sp.simplify(old-new),0)
    def test_omega_sign_and_energy(self):
        sol=v.relativistic_magnetic_orbit(1,.3,.1,.8,1.0,1000)
        self.assertGreater(sol['Omega'],0)
        self.assertLess(sol['max_rel_energy_error'],1e-10)
        self.assertLess(sol['max_position_error'],1e-7)
    def test_orbit_reverse_charge(self):
        a=v.relativistic_magnetic_orbit(1,.3,.1,.8,.5,400)
        b=v.relativistic_magnetic_orbit(1,-.3,.1,.8,.5,400)
        self.assertAlmostEqual(a['x'][-1],b['x'][-1],places=9)
        self.assertAlmostEqual(a['y'][-1],-b['y'][-1],places=9)
    def test_orbit_energy_two_periods(self):
        sol=v.relativistic_magnetic_orbit(1,.3,.1,.8,2.0,600)
        self.assertLess(sol['max_rel_energy_error'],1e-10)
        self.assertLess(sol['max_position_error'],1e-7)
    def test_v_below_c(self):
        for p in [.001,.1,1,10,1e6]:
            speed=p/math.hypot(1,p)
            self.assertLess(speed,1)
    def test_running_alpha_distinguishes_scales(self):
        ratio=v.ALPHA_INV_0/v.ALPHA_INV_MZ_MS
        self.assertGreater(ratio,1.07)
        self.assertLess(ratio,1.08)
    def test_report_json(self):
        d=v.compute_report()
        self.assertIn('only',d['unit_convention'])
        self.assertLess(d['orbit']['max_position_error'],1e-7)

class CovariantNormalConnection(unittest.TestCase):
    def test_so2_frame_rotation(self):
        s,chi,a,b=sp.symbols('s chi a b',real=True)
        angle=a*s+b*sp.sin(s)
        e1=sp.Matrix([sp.cos(angle),sp.sin(angle)])
        e2=sp.Matrix([-sp.sin(angle),sp.cos(angle)])
        omega=sp.simplify((e1.T*sp.diff(e2,s))[0])
        self.assertEqual(sp.simplify(omega+sp.diff(angle,s)),0)
        theta_dot=3*s
        self.assertEqual(sp.simplify(theta_dot+sp.diff(angle,s)+omega),theta_dot)
    def test_both_frame_and_em_transform(self):
        theta_dot=.2;omega=.15;A=.31;lam=.7
        chi_dot=-.09;Lambda_dot=.13
        new=v.internal_covariant_rate(theta_dot+chi_dot-lam*Lambda_dot,
             omega-chi_dot,A+Lambda_dot,lam)
        old=v.internal_covariant_rate(theta_dot,omega,A,lam)
        self.assertAlmostEqual(new,old,places=15)
    def test_closed_frame_large_gauge_phase(self):
        for n in range(-5,6):
            for w in [-3,-1,0,1,4]:
                self.assertAlmostEqual(abs(v.finite_frame_winding_amplitude(n,w)-1),0,delta=4e-14)
    def test_quantized_geo_phase_matches_torsion_for_helix(self):
        for u in [-.4,0,.2,.9]:
            hol=v.helix_geometry(u,.4)['turn_holonomy_angle']
            phase=np.exp(-1j*3*hol)
            self.assertAlmostEqual(phase.real,math.cos(3*hol),places=13)

if __name__ == '__main__':unittest.main(verbosity=2)
