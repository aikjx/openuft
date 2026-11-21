"""ROOT V123 minimal symbolic field-theory audit (NOT a unified theory).

Four-dimensional metric f(R) trace equation; classical Maxwell trace; 5D
null dispersion -> 4D massive dispersion. No dynamical mass prediction.
"""
from __future__ import annotations
import sympy as sp


def quadratic_fR_trace_equation():
    """Verify 3 □ f_R+ f_R R-2 f = 6 a □R-R for f=R+aR²."""
    a,R,boxR=sp.symbols('a R boxR',real=True)
    f=R+a*R**2
    derivative=sp.diff(f,R)
    lhs=3*(2*a*boxR)+derivative*R-2*f
    rhs=6*a*boxR-R
    return {'lhs':lhs,'rhs':rhs,'remainder':sp.simplify(lhs-rhs),
            'mass_inv_m2':1/(6*a)}


def classical_maxwell_trace():
    """Compute T^mu_mu from the 4D classical Maxwell stress tensor."""
    E1,E2,E3,B1,B2,B3=sp.symbols('E1 E2 E3 B1 B2 B3',real=True)
    metric=sp.diag(-1,1,1,1)
    F=sp.Matrix([[0,E1,E2,E3],
                 [-E1,0,B3,-B2],
                 [-E2,-B3,0,B1],
                 [-E3,B2,-B1,0]])
    F_up=metric*F*metric
    FF=sum(F[i,j]*F_up[i,j] for i in range(4) for j in range(4))
    T=F*metric*F.T-sp.Rational(1,4)*metric*FF
    trace=sp.simplify(sum(metric[i,i]*T[i,i] for i in range(4)))
    return {'trace':trace,'invariant':sp.simplify(FF)}


def five_dimensional_null_dispersion():
    """Flat 5D null momentum with + space fifth dimension, algebra only."""
    c,E,p,p5,m=sp.symbols('c E p p5 m',real=True,positive=True)
    five_null=-E**2/c**2+p**2+p5**2
    four_mass_shell=E**2-c**2*p**2-m**2*c**4
    equivalence=sp.simplify((five_null.subs(p5,m*c)*(-c**2))-four_mass_shell)
    return {'5D_null':five_null, '4D_mass_shell':four_mass_shell,
            'difference_after_p5_equals_mc':equivalence}


def circle_kk_mass_scale(ell:float,n:int,hbar=1.054571817e-34,c=299792458.):
    if ell<=0 or not isinstance(n,int): raise ValueError('ell>0 and integer n')
    return abs(n)*hbar/(ell*c)
