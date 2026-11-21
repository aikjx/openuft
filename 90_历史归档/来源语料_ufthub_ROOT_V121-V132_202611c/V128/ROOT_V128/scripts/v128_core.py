"""ROOT V128: reproducible audits, NOT a new validated physical model.
SI for helix; natural units in algebraic gauge calculations.
"""
from __future__ import annotations
import math
import numpy as np
import sympy as sp

C = 299792458.0
HBAR = 1.054571817e-34
ELECTRON_MASS = 9.1093837139e-31
MUON_ELECTRON_RATIO = 206.7682827


def helix_kinematics(omega: float, u: float, c: float = C):
    """Null physical 4D helix: R*omega = sqrt(c²-u²)."""
    if omega <= 0 or not abs(u) < c: raise ValueError('omega>0, |u|<c required')
    R = math.sqrt(c*c-u*u) / omega
    curvature = R*omega*omega/(c*c)
    torsion = u*omega/(c*c)
    return dict(R=R, omega=omega, u=u, speed=c, kappa=curvature,
                tau=torsion, candidate_mass=HBAR*omega/(c*c))


def boost_helix(omega: float, u: float, beta: float, c: float = C):
    """Lorentz boost along helix z; boost maps null worldline to null worldline."""
    if not abs(beta) < 1: raise ValueError('subluminal boosts only')
    gamma=1.0/math.sqrt(1-beta*beta)
    factor=gamma*(1-beta*u/c)
    return omega/factor, (u-beta*c)/(1-beta*u/c), factor


def mass_candidate_ratio(u_frac: float, beta: float):
    """m_cand' / m_cand for frequency assigned in coordinate time."""
    return math.sqrt(1-beta*beta)/(1-beta*u_frac)


def five_dim_projection(v3: float, vy: float, c: float=C):
    """5D null velocity constraint; 4D interval rate = sqrt(c²-v3²)."""
    if not math.isclose(v3*v3+vy*vy,c*c,rel_tol=1e-12):
        raise ValueError('5D line element is not null')
    return (c*c-v3*v3)/(c*c) # (dτ/dt)^2 in 4D


def su2_curvature(a: float, b: float, g: float):
    """D_mu=partial_mu+i*g*A_mu; A_x=a*sigma_x/2, A_y=b*sigma_y/2.
    Constant non-Abelian F_xy=i*g[A_x,A_y], [D_x,D_y]=i*g*F_xy.
    """
    sx=np.array([[0,1],[1,0]],dtype=complex)
    sy=np.array([[0,-1j],[1j,0]],dtype=complex)
    sz=np.array([[1,0],[0,-1]],dtype=complex)
    Ax=a*sx/2
    Ay=b*sy/2
    comm_A=Ax@Ay-Ay@Ax
    F=1j*g*comm_A
    comm_D=(1j*g)**2*comm_A
    return F, comm_D, -g*a*b*sz/2


def spinor_rotation(theta: float):
    return np.diag([np.exp(-0.5j*theta),np.exp(0.5j*theta)])


def gamma_matrices():
    z=np.zeros((2,2), dtype=complex)
    I=np.eye(2,dtype=complex)
    sigma=[np.array([[0,1],[1,0]],complex),
           np.array([[0,-1j],[1j,0]],complex),
           np.array([[1,0],[0,-1]],complex)]
    gamma0=np.block([[I,z],[z,-I]])
    gammas=[gamma0]
    for s in sigma:
        gammas.append(np.block([[z,s],[-s,z]]))
    return gammas


def squared_dirac_residual(p4):
    """Clifford identity (gamma dot p)^2 = (p0² - sum pi²) I4."""
    gm=gamma_matrices()
    D=gm[0]*p4[0]-sum((gm[i]*p4[i] for i in range(1,4)), np.zeros((4,4),complex))
    inv=p4[0]**2-sum(z*z for z in p4[1:])
    return float(np.max(np.abs(D@D-inv*np.eye(4))))


def sphere_scalar_curvature():
    """Compute Ricci scalar from ds²=dtheta²+sin²(theta)dphi² using Christoffels."""
    th=sp.symbols('theta', real=True, positive=True)
    coords=[th, sp.symbols('phi', real=True)]
    g=sp.diag(1,sp.sin(th)**2)
    gi=sp.diag(1,1/sp.sin(th)**2)
    # Gamma^k_{ij}
    Ga={(k,i,j):sp.simplify(sp.Rational(1,2)*sum(gi[k,l]*(sp.diff(g[l,j],coords[i]) + sp.diff(g[l,i],coords[j]) - sp.diff(g[i,j],coords[l])) for l in range(2)))
        for k in range(2) for i in range(2) for j in range(2)}
    # R^rho_{sigma mu nu} = d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma} + ...
    R={(rho,sigma,mu,nu):sp.simplify(
        sp.diff(Ga[rho,nu,sigma],coords[mu]) - sp.diff(Ga[rho,mu,sigma],coords[nu])
        + sum(Ga[rho,mu,l]*Ga[l,nu,sigma]-Ga[rho,nu,l]*Ga[l,mu,sigma] for l in range(2)))
       for rho in range(2) for sigma in range(2) for mu in range(2) for nu in range(2)}
    Ric={(sigma,nu):sp.simplify(sum(R[rho,sigma,rho,nu] for rho in range(2))) for sigma in range(2) for nu in range(2)}
    scalar=sp.simplify(sum(gi[i,i]*Ric[i,i] for i in range(2)))
    return scalar,R[(0,1,0,1)]


def ky_electron_frequency():
    return ELECTRON_MASS*C*C/HBAR


def winding_wilson_flux(g: float, B: float, area: float):
    """U(1) Wilson loop for constant B: exp(i*g*B*area), natural units."""
    return complex(np.exp(1j*g*B*area))
