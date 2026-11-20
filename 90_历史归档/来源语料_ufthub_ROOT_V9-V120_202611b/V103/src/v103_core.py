"""ROOT V103. Conditional classical-physics audit, not a theory of quantum gravity.
Constants from scipy.constants (CODATA precision depending on installed scipy).
"""
from __future__ import annotations
import math
from dataclasses import dataclass
import numpy as np
from scipy.constants import c, epsilon_0, e, m_e

PI=math.pi

def gamma_beta(beta:float)->float:
    if not (0 < beta < 1): raise ValueError('Requires 0 < v/c < 1')
    return 1/math.sqrt(1-beta*beta)

def knot_energy_floor(L:float,beta:float,q:float=e)->float:
    """Radiation per period lower bound, conditional on a nontrivial smoothly embedded knot."""
    if L<=0 or not math.isfinite(L) or q==0:raise ValueError('L positive, q nonzero')
    g=gamma_beta(beta); v=beta*c
    return 8*PI*q*q*g**4*v**3/(3*epsilon_0*c**3*L)

def curve_radiation(K2:float,beta:float,q:float=e)->float:
    if K2<0 or not math.isfinite(K2) or q==0: raise ValueError('K2 nonnegative, q nonzero')
    return q*q*gamma_beta(beta)**4*beta**3*K2/(6*PI*epsilon_0)

def supply_budget(L:float,K2:float,beta:float,q:float=e)->dict:
    v=beta*c; T=L/v
    E=curve_radiation(K2,beta,q); Emin=knot_energy_floor(L,beta,q)
    return dict(period_s=T,energy_rad_J=E,topological_energy_floor_J=Emin,
        avg_power_W=E/T,minimum_power_W=Emin/T,
        compensation_voltage_V=E/abs(q),min_voltage_V=Emin/abs(q),
        equivalent_tangential_E_V_per_m=E/(abs(q)*L),
        minimum_equivalent_E_V_per_m=Emin/(abs(q)*L),ratio_to_floor=E/Emin)

def discrete_geometry(points:np.ndarray)->dict:
    """V102 compatible closed-polygon reconstruction; assumes no repeated endpoint."""
    p=np.asarray(points,dtype=float)
    if p.ndim!=2 or p.shape[1]!=3 or len(p)<50 or not np.isfinite(p).all(): raise ValueError('finite Nx3')
    edges=np.roll(p,-1,axis=0)-p
    ds=np.linalg.norm(edges,axis=1)
    if np.min(ds)<=0: raise ValueError('repeated vertices')
    tangents=edges/ds[:,None]
    angles=np.arctan2(np.linalg.norm(np.cross(np.roll(tangents,1,axis=0),tangents),axis=1),
                      np.clip(np.sum(np.roll(tangents,1,axis=0)*tangents,axis=1),-1,1))
    weights=(ds+np.roll(ds,1))/2
    return dict(L=float(np.sum(ds)),K=float(np.sum(angles)),K2=float(np.sum(angles**2/weights)),
                min_segment_m=float(np.min(ds)),n=int(len(p)))

def circle(R=0.01,N=1200):
    x=np.linspace(0,2*PI,N,endpoint=False)
    return np.column_stack((R*np.cos(x),R*np.sin(x),np.zeros_like(x)))

def trefoil_torus(R=.01,r=.002,N=1200):
    x=np.linspace(0,2*PI,N,endpoint=False)
    radius=R+r*np.cos(3*x)
    return np.column_stack((radius*np.cos(2*x),radius*np.sin(2*x),r*np.sin(3*x)))

def boosted_circle(beta_particle=.6,beta_boost=.4,R=0.01)->dict:
    """Boost z of a lab planar circle (uniform B along z). A spatial circle becomes a helix."""
    if not(-.999 < beta_boost < .999): raise ValueError('bad boost')
    v=beta_particle*c; u=beta_boost*c; gb=1/math.sqrt(1-beta_boost**2)
    omega=v/R
    omega_prime=omega/gb
    v_perp_prime=v/gb
    v_axial_prime=-u
    vp=math.hypot(v_perp_prime,v_axial_prime)
    kappa_lab=1/R; tau_lab=0.
    kp=R*omega_prime**2/vp**2
    tp=v_axial_prime*omega_prime/vp**2
    proper_accel_lab=gamma_beta(beta_particle)**2 * v*v/R
    proper_accel_prime=gamma_beta(vp/c)**2 * R*omega_prime**2
    return dict(beta_particle=beta_particle,beta_boost=beta_boost,
        lab_curvature_inv_m=kappa_lab,lab_torsion_inv_m=tau_lab,
        boosted_curvature_inv_m=kp,boosted_torsion_inv_m=tp,
        lab_omega_rad_s=omega,boosted_omega_rad_s=omega_prime,
        boosted_speed_m_s=vp,lab_proper_accel_m_s2=proper_accel_lab,
        boosted_proper_accel_m_s2=proper_accel_prime,
        invariant_relative_error=abs(proper_accel_prime-proper_accel_lab)/proper_accel_lab)

def comp_signal(kinetic_J:float,loss_J:float):
    return loss_J/kinetic_J
