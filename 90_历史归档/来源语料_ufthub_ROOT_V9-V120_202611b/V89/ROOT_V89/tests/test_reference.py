import math
from dataclasses import replace
import numpy as np
import pytest
from scipy.optimize import brentq
from src.quantum_gravity_audit import Config,geom,phases,cross,negativity,rho_dephased,sphere_radius,scale_terms,scaled_design

P=Config()
@pytest.mark.parametrize('power',[1,2,3,4])
def test_analytic_power_cross_matches_direct_quadrature(power):
    # Fundamental theorem: numerical derivative d/dr r^-n=-n*r^(-n+1)
    from scipy.integrate import quad
    R=np.array([[.00045,.00065],[.00025,.00045]])
    calculated=geom(P,power)
    f=lambda r:quad(lambda x: -power*x**(-power-1),R[0,0],r,epsabs=1e-9)[0]+R[0,0]**(-power)
    rhs=f(R[0,0])-f(R[0,1])-f(R[1,0])+f(R[1,1])
    assert math.isclose(calculated,rhs,rel_tol=1e-11)

@pytest.mark.parametrize('gamma',[0,.003,.01,.03,.1])
def test_dephasing_negative_eigenvalues(gamma):
    p=replace(P,gamma1=gamma,gamma2=gamma)
    rho=rho_dephased(p)
    pt=np.transpose(rho.reshape(2,2,2,2),(0,3,2,1)).reshape(4,4)
    independent=max(0,-np.linalg.eigvalsh(pt)[np.linalg.eigvalsh(pt)<0].sum())
    assert math.isclose(negativity(rho),independent,abs_tol=1e-14)

@pytest.mark.parametrize('radius',[.00035,.0005,.0009,.0015])
def test_finite_spheres_shell_theorem_nonoverlap(radius):
    # A uniform sphere's exterior Newton potential is exactly point-source potential.
    # Numerical Gauss-Legendre shell integration around center, in dimensionless form:
    # average over shell of 1/|d-r| equals 1/d for d>r.
    import numpy.polynomial.legendre as lg
    r_shell=5e-6; r=radius
    nodes,weights=lg.leggauss(100)
    val=.5*sum(w/math.sqrt(r*r+r_shell*r_shell-2*r*r_shell*mu) for mu,w in zip(nodes,weights))
    assert math.isclose(val,1/r,rel_tol=1e-11)

def test_cross_zero_distance_derivative_small_branches():
    # F1 approx -2*s1*s2/d³ (branch-cross derivative convention)
    p=replace(P,s1=2e-7,s2=3e-7)
    expected=-2*p.s1*p.s2/p.d**3
    assert math.isclose(geom(p,1),expected,rel_tol=1e-5)

def test_critical_dephasing_exists_in_demo():
    f=lambda g:negativity(rho_dephased(replace(P,gamma1=g,gamma2=g)))
    assert f(0)>0 and f(.1)==0
    g=brentq(lambda g: np.linalg.eigvalsh(np.transpose(rho_dephased(replace(P,gamma1=g,gamma2=g)).reshape(2,2,2,2),(0,3,2,1)).reshape(4,4)).min(),0,.1,xtol=1e-12)
    assert .01<g<.1

def test_design_rank_dimensionless():
    X=scaled_design(P,(450e-6,600e-6,850e-6))
    assert X.shape==(3,3) and np.linalg.matrix_rank(X)==3
