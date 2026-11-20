"""ROOT V104: reproducible mathematical audits. All results are THEORY, not measurements.

This is established Lorentz-force mechanics / numerical linear algebra, not a new unification.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

C = 299_792_458.0
ELEM_CHARGE = 1.602176634e-19
ELECTRON_MASS = 9.1093837139e-31
EPS0 = 8.8541878188e-12


def skew_cross(v):
    """Return matrix such that skew_cross(v) @ b == np.cross(v,b)."""
    x,y,z = map(float, v)
    return np.array([[0,-z,y],[z,0,-x],[-y,x,0]], float)


def lorentz_design(betas):
    """y = E + beta cross (c*B) in V/m for known test-particle charge."""
    a=np.asarray(betas, dtype=float).reshape(-1,3)
    if np.any(np.linalg.norm(a,axis=1)>=1):
        raise ValueError("All dimensionless probe speeds must be < c")
    return np.vstack([np.hstack([np.eye(3),skew_cross(beta)]) for beta in a])


def reconstruct_fields(betas, force_over_charge):
    """Solve for E and B; reject underidentified inverse problems."""
    d=lorentz_design(betas)
    if np.linalg.matrix_rank(d,tol=1e-10)<6:
        raise ValueError("Fields not uniquely identifiable from these probe velocities")
    y=np.asarray(force_over_charge,dtype=float).reshape(-1)
    x,_,_,s=np.linalg.lstsq(d,y,rcond=None)
    return {'E_V_per_m':x[:3], 'B_T':x[3:]/C, 'condition_number':s[0]/s[-1], 'residual_norm':np.linalg.norm(d@x-y)}


def lorentz_observations(betas, efield, bfield):
    xx=np.r_[np.asarray(efield,dtype=float), C*np.asarray(bfield,dtype=float)]
    return lorentz_design(betas) @ xx


def exact_rank(betas):
    return int(np.linalg.matrix_rank(lorentz_design(betas),tol=1e-10))


def lorentz_trajectory_force(m0,v,dvdt,kappa,tangent,normal):
    """Net 3-force for differentiable timelike trajectory and unit Frenet vectors."""
    if not (0<v<C): raise ValueError('requires 0 < v < c')
    if kappa<0: raise ValueError('curvature must be nonnegative')
    T=np.asarray(tangent,dtype=float)
    N=np.asarray(normal,dtype=float)
    if not (np.isclose(np.linalg.norm(T),1) and np.isclose(np.linalg.norm(N),1) and np.isclose(T@N,0)):
        raise ValueError('requires orthonormal tangent/normal')
    gamma=1/math.sqrt(1-(v/C)**2)
    return gamma**3*m0*dvdt*T+gamma*m0*v*v*kappa*N


def boost_circle_axis(radius, v, u):
    """Circular 3-path boosted along axis: Frenet curvatures change, proper a invariant."""
    if not (radius>0 and 0<v<C and abs(u)<C): raise ValueError('invalid timelike parameters')
    gb=1/math.sqrt(1-(u/C)**2)
    g=1/math.sqrt(1-(v/C)**2)
    omega=v/radius
    omega2=omega/gb
    speed2sq=(v/gb)**2+u*u
    kappa2=radius*omega2*omega2/speed2sq
    torsion2=-u*omega2/speed2sq
    g2=1/math.sqrt(1-speed2sq/C**2)
    a0=g*g*v*v/radius
    a1=g2*g2*speed2sq*kappa2
    return dict(kappa_original=1/radius,torsion_original=0.0,
                kappa_boost=kappa2,torsion_boost=torsion2,
                proper_acc_original=a0,proper_acc_boost=a1)


def wavy_planar_total_curvature(k=5, a=0.2, reltol=1e-11):
    """Star-shaped planar unknot with total curvature >4*pi. Radius rho=1+a*cos(k t)."""
    if not (int(k)==k and k>=2 and 0<a<1): raise ValueError('requires k>=2 integer, 0<a<1')
    def numerator(t):
        r=1+a*math.cos(k*t)
        rp=-a*k*math.sin(k*t)
        rpp=-a*k*k*math.cos(k*t)
        return r*r+2*rp*rp-r*rpp
    def integrand(t):
        r=1+a*math.cos(k*t)
        rp=-a*k*math.sin(k*t)
        return abs(numerator(t))/(r*r+rp*rp)
    # Split at inflection points where the absolute value changes smooth branch.
    grid=np.linspace(0,2*math.pi,400*k+1)
    roots=[brentq(numerator,float(l),float(h)) for l,h in zip(grid[:-1],grid[1:]) if numerator(float(l))*numerator(float(h))<0]
    result,err=quad(integrand,0,2*math.pi,epsabs=reltol,epsrel=reltol,limit=600,points=roots)
    return {'total_curvature':result,'error_estimate':err,'topology':'UNKNOT (simple planar curve; rho>0)','ratio_to_4pi':result/(4*math.pi)}


def bound_radiation_nontrivial_knot(q,v,length,m=ELECTRON_MASS):
    if q==0 or not (0<v<C) or length<=0: raise ValueError('physical parameters required')
    g=1/math.sqrt(1-(v/C)**2)
    energy=8*math.pi*q*q*g**4*v**3/(3*EPS0*C**3*length)
    return dict(E_min_J=energy, P_min_W=energy*v/length, T_s=length/v,
                mean_field_min_V_per_m=energy/(abs(q)*length))


def dimensionless_field_example():
    betas=np.array([[0.1,0.2,0.3],[-0.2,0.1,0.1],[0.0,-0.2,0.3]])
    E=np.array([1.2,-0.7,0.3])
    B=np.array([3e-9,-2e-9,5e-9])
    y=lorentz_observations(betas,E,B)
    return betas,E,B,y
