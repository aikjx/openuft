import unittest
import sympy as sp
from src.composite import (
    t,x,y,z,COORDS,eta,field,grad,current,projections,pfaff,f_squared,
    bianchi,jacobian,electric_magnetic,stress,stress_divergence,
    constant_rank4,rank4_offshell,forcefree_beltrami,circular_plane_wave,
    lorentz_boost_x,simp_m
)

class TestRepresentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.non = constant_rank4()
        cls.off = rank4_offshell()
        cls.forcefree = forcefree_beltrami()
        cls.wave = circular_plane_wave()
        cls.fn=field(cls.non)
        cls.fo=field(cls.off)
        cls.fb=field(cls.forcefree)
        cls.fw=field(cls.wave)

    def zero_matrix(self,m):
        self.assertEqual(simp_m(m),sp.zeros(*m.shape))

    def test_01_antisymmetry_all(self):
        for f in [self.fn,self.fo,self.fb,self.fw]: self.zero_matrix(f+f.T)

    def test_02_closed_all(self):
        for f in [self.fn,self.fo,self.fb,self.fw]:
            self.assertTrue(all(v==0 for v in bianchi(f)))

    def test_03_rank4_pfaff(self): self.assertEqual(pfaff(self.fn),1)
    def test_04_rank4_det(self): self.assertEqual(jacobian(self.non).det(),1)
    def test_05_rank4_divergence(self): self.zero_matrix(current(self.fn))
    def test_06_rank4_projection(self): self.assertEqual(projections(current(self.fn),self.non),[0,0,0,0])
    def test_07_rank4_stationary_stress(self): self.assertEqual(stress_divergence(self.fn),[0]*4)
    def test_08_nonrank4_determinant(self): self.assertEqual(jacobian(self.off).det(),1)
    def test_09_nonrank4_pfaffian(self): self.assertEqual(pfaff(self.fo),1)
    def test_10_nonrank4_current(self): self.assertEqual(current(self.fo),sp.Matrix([sp.Rational(2,3),0,0,0]))
    def test_11_nonrank4_eom_violation(self): self.assertEqual(projections(current(self.fo),self.off)[0],sp.Rational(2,3))
    def test_12_nonrank4_bianchi(self): self.assertEqual(bianchi(self.fo),[0]*4)
    def test_13_pfaff_det_variable(self):
        pairs=[(t+x*y,y+z*t),(x*x+z,y+t*z)]
        self.assertEqual(sp.simplify(pfaff(field(pairs))-jacobian(pairs).det()),0)
    def test_14_offshell_stress_not_conserved(self):
        self.assertNotEqual(stress_divergence(self.fo),[0]*4)

    def test_15_beltrami_b(self):
        _,B=electric_magnetic(self.fb)
        self.zero_matrix(B-sp.Matrix([sp.cos(2*z),sp.sin(2*z),0]))
    def test_16_beltrami_J_nonzero(self):
        J=current(self.fb)
        self.zero_matrix(J-sp.Matrix([0,2*sp.cos(2*z),2*sp.sin(2*z),0]))
    def test_17_beltrami_projected_equations_hold(self):
        self.assertEqual(projections(current(self.fb),self.forcefree),[0,0,0,0])
    def test_18_beltrami_but_not_maxwell(self):
        self.assertNotEqual(current(self.fb),sp.zeros(4,1))
    def test_19_beltrami_pfaff_zero(self): self.assertEqual(pfaff(self.fb),0)
    def test_20_beltrami_jacobian_degenerate(self): self.assertEqual(jacobian(self.forcefree).rank(),2)
    def test_21_beltrami_stress_conserved_despite_nonzero_J(self):
        # Force-free current gives F_{nu mu} J^mu = 0: conservation alone is insufficient.
        self.assertEqual(stress_divergence(self.fb),[0]*4)

    def test_22_wave_current_zero(self): self.zero_matrix(current(self.fw))
    def test_23_wave_F2_null(self): self.assertEqual(f_squared(self.fw),0)
    def test_24_wave_pfaff_zero(self): self.assertEqual(pfaff(self.fw),0)
    def test_25_wave_jacobian_degenerate(self): self.assertEqual(jacobian(self.wave).rank(),2)
    def test_26_wave_E2(self):
        E,_=electric_magnetic(self.fw)
        self.assertEqual(sp.trigsimp(E.dot(E)),1)
    def test_27_wave_B2(self):
        _,B=electric_magnetic(self.fw)
        self.assertEqual(sp.trigsimp(B.dot(B)),1)
    def test_28_wave_EdotB(self):
        E,B=electric_magnetic(self.fw)
        self.assertEqual(sp.trigsimp(E.dot(B)),0)
    def test_29_wave_stress_conserved(self): self.assertEqual(stress_divergence(self.fw),[0]*4)
    def test_30_wave_energy_density(self): self.assertEqual(sp.trigsimp(stress(self.fw)[0,0]),1)
    def test_31_wave_rotates(self):
        E,_=electric_magnetic(self.fw)
        self.assertEqual(E[0],sp.cos(3*(t-z)))
        self.assertEqual(E[1],sp.sin(3*(t-z)))
    def test_32_wave_bianchi(self): self.assertEqual(bianchi(self.fw),[0]*4)

    def test_33_lorentz_invariant_F2(self):
        L=lorentz_boost_x(sp.Rational(3,5))
        self.assertEqual(sp.simplify(f_squared(L*self.fn*L.T)-f_squared(self.fn)),0)
    def test_34_lorentz_invariant_pfaff(self):
        L=lorentz_boost_x(sp.Rational(3,5))
        self.assertEqual(sp.simplify(pfaff(L*self.fn*L.T)-pfaff(self.fn)),0)
    def test_35_lorentz_metric(self):
        L=lorentz_boost_x(sp.Rational(3,5))
        self.zero_matrix(L.T*eta*L-eta)
    def test_36_lorentz_wave_invariant_F2(self):
        L=lorentz_boost_x(sp.Rational(4,5))
        self.assertEqual(sp.trigsimp(f_squared(L*self.fw*L.T)),0)
    def test_37_stress_symmetric(self):
        for f in [self.fn,self.fo,self.fb,self.fw]: self.zero_matrix(stress(f)-stress(f).T)
    def test_38_stress_trace_zero(self):
        for f in [self.fn,self.fo,self.fb,self.fw]:
            self.assertEqual(sp.simplify(sum(eta[i,i]*stress(f)[i,i] for i in range(4))),0)
    def test_39_energy_positive_constant(self): self.assertEqual(stress(self.fn)[0,0],1)
    def test_40_energy_positive_offshell(self):
        self.assertGreater(float(stress(self.fo)[0,0].subs({y:1})),0)

    def test_41_sign_efields(self):
        E,B=electric_magnetic(self.fn)
        self.assertEqual(E,sp.Matrix([1,0,0]));self.assertEqual(B,sp.Matrix([1,0,0]))
    def test_42_dot_parallel(self):
        E,B=electric_magnetic(self.fn)
        self.assertEqual(E.dot(B),1)
    def test_43_pfaff_EdotB(self):
        for f in [self.fn,self.fo,self.fb,self.fw]:
            E,B=electric_magnetic(f)
            self.assertEqual(sp.trigsimp(pfaff(f)-E.dot(B)),0)
    def test_44_F2_EM(self):
        for f in [self.fn,self.fo,self.fb,self.fw]:
            E,B=electric_magnetic(f)
            self.assertEqual(sp.trigsimp(f_squared(f)-2*(B.dot(B)-E.dot(E))),0)
    def test_45_stress00_EM(self):
        for f in [self.fn,self.fo,self.fb,self.fw]:
            E,B=electric_magnetic(f)
            self.assertEqual(sp.trigsimp(stress(f)[0,0]-(B.dot(B)+E.dot(E))/2),0)
    def test_46_zero_field(self):
        ff=field([(sp.Integer(1),t),(sp.Integer(0),x)])
        self.zero_matrix(ff)
    def test_47_qp_reparam_invariance(self):
        q=t+x; p=y+z
        self.zero_matrix(field([(q,p)])-field([(2*q,p/2)]))
    def test_48_reparam_area_preservation(self):
        q=t+x; p=y+z
        self.zero_matrix(field([(q,p)])-field([(q+p,p)]))


    def test_49_constant_vacuum_field_is_quadratic_in_fluctuations(self):
        eps=sp.symbols('eps',real=True)
        f=field([(eps*t,eps*x),(eps*y,eps*z)])
        self.assertEqual(f[0,1],eps**2)
        self.assertEqual(f[2,3],eps**2)

    def test_50_constant_vacuum_no_quadratic_kinetic_term(self):
        eps=sp.symbols('eps',real=True)
        f=field([(eps*t,eps*x),(eps*y,eps*z)])
        self.assertEqual(sp.diff(f_squared(f),eps,2).subs(eps,0),0)

    def test_51_constant_vacuum_first_nonzero_action_quartic(self):
        eps=sp.symbols('eps',real=True)
        f=field([(eps*t,eps*x)])
        self.assertEqual(f_squared(f),-2*eps**4)

    def test_52_nontrivial_background_linear_field_variation(self):
        eps=sp.symbols('eps',real=True)
        f=field([(t+eps*y,x)])
        self.assertEqual(f[1,2],-eps)
        self.assertEqual(f[0,1],1)

    def test_53_closedness_constant_vacuum_fluctuation(self):
        eps=sp.symbols('eps',real=True)
        f=field([(eps*t*y,eps*x*z)])
        self.assertEqual(bianchi(f),[0]*4)

if __name__=='__main__': unittest.main()
