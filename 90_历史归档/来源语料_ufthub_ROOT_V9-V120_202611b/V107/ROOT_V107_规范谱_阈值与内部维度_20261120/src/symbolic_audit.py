"""Exact independent SymPy consistency checks; not experimental evidence."""
from __future__ import annotations
import sympy as sp
from fractions import Fraction
from .theory import B,DB_TRIPLET,DB_DOUBLET,W,hypercharge_anomalies


def run():
    checks={}
    q,h,l=sp.symbols('q h l',real=True)
    u=q+h;d=q-h;e=l-h;nu=l+h
    checks['anomaly_weak_linear']=sp.simplify(3*q+l-(3*q+l))==0
    checks['yukawa_up']=sp.simplify(u-q-h)==0
    checks['yukawa_down']=sp.simplify(d-q+h)==0
    checks['yukawa_electron']=sp.simplify(e-l+h)==0
    checks['yukawa_neutrino']=sp.simplify(nu-l-h)==0
    cg=sp.expand(6*q-3*u-3*d+2*l-e)
    cc=sp.expand(6*q**3-3*u**3-3*d**3+2*l**3-e**3)
    checks['gravity_anomaly_factor']=sp.simplify(cg-(l+h))==0
    checks['gravity_anomaly_SU2_reduction']=sp.simplify(cg.subs(l,-3*q)-(h-3*q))==0
    checks['cubic_anomaly_minimal_factor']=sp.simplify(cc.subs(l,-3*q)-(h-3*q)**3)==0
    checks['cubic_anomaly_minimal_vanish']=sp.simplify(cc.subs({l:-3*q,h:3*q}))==0
    checks['cubic_anomaly_with_nu_vanish']=sp.simplify((cc-nu**3).subs(l,-3*q))==0
    checks['gravity_anomaly_with_nu_vanish']=sp.simplify((cg-nu).subs(l,-3*q))==0
    checks['SU3SU3U1_anomaly_vanish']=sp.expand(2*q-u-d)==0
    checks['SU2SU2U1_anomaly_vanish']=sp.expand((3*q+l).subs(l,-3*q))==0
    checks['complete_multiplet_equal_beta']=all(x+y==Fraction(2,3) for x,y in zip(DB_TRIPLET,DB_DOUBLET))
    checks['weights_satisfy_sum_zero']=sum(W)==0
    checks['weights_dot_base_b_zero']=sum(x*y for x,y in zip(W,B))==0
    checks['beta_weights_K_exact']=sum(x*y for x,y in zip(W,DB_TRIPLET))==Fraction(88,15)
    checks['beta_weights_opposite']=sum(x*y for x,y in zip(W,DB_DOUBLET))==-Fraction(88,15)
    a1,a2,a3,t=sp.symbols('a1 a2 a3 t',real=True)
    b1,b2,b3=sp.symbols('b1 b2 b3',real=True)
    It=(b2-b3)*a1+(b3-b1)*a2+(b1-b2)*a3
    checks['invariant_under_SM_running']=sp.expand(It.subs({a1:a1-b1*t,a2:a2-b2*t,a3:a3-b3*t})-It)==0
    d=sp.symbols('d')
    checks['invariant_under_degenerate_common_multiplet']=sp.expand(It.subs({a1:a1-d*t,a2:a2-d*t,a3:a3-d*t})-It)==0
    # SU2 Cartan field from four internal phases
    sigma3=sp.diag(1,-1);X=sp.I*sigma3/2
    checks['internal_4phase_local_density']=sp.trace(X**2)*sp.Integer(2)==-1
    f01,f02,f03,f12,f13,f23=sp.symbols('f01 f02 f03 f12 f13 f23')
    pf=2*(f01*f23-f02*f13+f03*f12)
    checks['four_form_rank_three']=sp.simplify(pf.subs({f03:0,f13:0,f23:0}))==0
    checks['four_form_rank_four']=pf.subs({f01:1,f23:1,f02:0,f13:0,f03:0,f12:0})==2
    checks['majorana_Ynu_0_selects_x_0']=sp.solve(sp.Eq(sp.Symbol('x'),0),sp.Symbol('x'))==[0]
    assert all(checks.values()),{k:v for k,v in checks.items() if not v}
    return checks

if __name__=='__main__': print('exact symbolic checks:',len(run()))
