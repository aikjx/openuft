#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROOT V133: conditional compact internal phase worldline model.

Unit convention: c=1 ONLY.  hbar and G are never assigned 1.
The model is a toy/probe sector, NOT an experimental unification result.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

# Exact CODATA 2022 central value as listed by NIST (not an exact defined constant).
ALPHA_INV_0 = 137.035999177
HBAR_SI = 1.054571817e-34  # J s, numeric reference, hbar != 1
G_SI = 6.67430e-11         # SI reference only; no conversion of c to 1 numerically
EPSILON0_SI = 8.8541878188e-12 # SI reference only; c=1 conversion must be specified separately
MUON_ELECTRON_RATIO = 206.7682827
ALPHA_INV_MZ_MS = 127.930 # PDG 2025 MS-bar, five active flavors, illustrative scheme


def circle_quantum_number(n: int, hbar: float = HBAR_SI) -> float:
    if not isinstance(n, (int, np.integer)):
        raise TypeError('n must be an integer for a single-valued S1 state')
    return int(n) * hbar


def rotor_spectrum(n: int, I: float, lam: float, m0: float, hbar: float=HBAR_SI) -> dict:
    if I <= 0 or hbar <= 0:
        raise ValueError('I and hbar must be positive')
    J = circle_quantum_number(n, hbar)
    q = lam*J
    mass = m0 + J*J/(2*I)
    alpha = q*q/(4*math.pi*EPSILON0_SI*hbar)  # explicit epsilon0, toy numeric convention only
    return {'n':int(n),'J':J,'charge':q,'mass':mass,'alpha':alpha,'mass_shift':mass-m0}


def lambda_for_alpha(alpha: float, hbar: float=HBAR_SI) -> float:
    if alpha <= 0 or hbar <= 0:
        raise ValueError('positive alpha and hbar required')
    return math.sqrt(4*math.pi*EPSILON0_SI*alpha/hbar)


def helix_geometry(u: float, omega: float) -> dict:
    """External Euclidean cylinder helix, |three-speed|=1 (null spacetime curve)."""
    if abs(u) >= 1 or omega <= 0:
        raise ValueError('need |u|<1, omega>0')
    R=math.sqrt(1-u*u)/omega
    kap=R*omega*omega
    tau=u*omega
    return {'R':R,'omega':omega,'u':u,'kappa':kap,'torsion':tau,
            'normalized_torsion':tau/math.hypot(kap,tau),
            'turn_holonomy_angle':2*math.pi*u}


def boost_axis_velocity(u: float, beta: float) -> float:
    if abs(u) >= 1 or abs(beta)>=1:
        raise ValueError('|u|,|beta| must be below 1')
    return (u-beta)/(1-beta*u)


def gauge_invariant_phase_rate(theta_dot, A_dot_x, lam) -> float:
    return theta_dot+lam*A_dot_x


def fixed_J_routhian(m0: float, I: float, J: float, lam: float) -> tuple[float,float]:
    """Fixed-J Routhian coefficient in proper-time relativistic action:
       S_eff = - M int ds + q int A dx.
    """
    if I<=0: raise ValueError('I must be positive')
    return m0+J**2/(2*I), lam*J


def relativistic_magnetic_orbit(mass: float, charge:float, Bz:float, p0:float,
                                periods:float=2.0, samples:int=2001) -> dict:
    """Integrates dp/dt=q v x B with v=p/sqrt(M^2+p^2), c=1."""
    if mass<=0 or p0<=0 or charge*Bz==0:
        raise ValueError('mass, p0 positive and charge*B != 0 required')
    e0=math.hypot(mass,p0)
    Omega=charge*Bz/e0
    duration=periods*2*math.pi/abs(Omega)
    v0=p0/e0
    times=np.linspace(0,duration,samples)
    def dyn(t, y):
        px,py,pz=y[3:]
        energy=math.sqrt(mass*mass+px*px+py*py+pz*pz)
        vx,vy,vz=px/energy,py/energy,pz/energy
        return [vx,vy,vz,charge*vy*Bz,-charge*vx*Bz,0.0]
    sol=solve_ivp(dyn,(0,duration),[0,0,0,p0,0,0],t_eval=times,rtol=2e-11,atol=2e-12,method='DOP853')
    if not sol.success: raise RuntimeError(sol.message)
    px,py,pz=sol.y[3:]
    energies=np.sqrt(mass*mass+px*px+py*py+pz*pz)
    xtrue=v0/Omega*np.sin(Omega*times)
    ytrue=v0/Omega*(np.cos(Omega*times)-1)
    dr=np.hypot(sol.y[0]-xtrue, sol.y[1]-ytrue)
    return {'Omega':Omega,'duration':duration,'max_rel_energy_error':float(np.max(abs(energies/e0-1))),
            'max_position_error':float(dr.max()),'t':times,'x':sol.y[0],'y':sol.y[1],
            'px':px,'py':py,'x_exact':xtrue,'y_exact':ytrue}


def compute_report() -> dict:
    alpha0=1/ALPHA_INV_0
    hbar=HBAR_SI
    lambda0=lambda_for_alpha(alpha0, hbar)
    tau0=1.0  # illustrative chosen time unit: 1 s, NOT a physical prediction
    I=10*hbar*tau0
    m0=100*hbar/tau0
    tower=[rotor_spectrum(n,I,lambda0,m0,hbar) for n in range(-4,5)]
    u=alpha0
    geom=helix_geometry(u, 0.2)
    boosted=boost_axis_velocity(u,0.6)
    orbit=relativistic_magnetic_orbit(1.0,0.3,0.1,0.8)
    return {
        'unit_convention':'c=1 only; hbar,G remain explicit',
        'codata_2022_inverse_alpha':ALPHA_INV_0,
        'alpha_0':alpha0,
        'hbar_SI_Js':hbar,
        'G_SI_reference':G_SI,
        'epsilon0_SI_reference':EPSILON0_SI,
        'lambda_fit_to_alpha_0_not_predicted':lambda0,
        'sample_I':I,'sample_m0':m0,
        'toy_rotor_tower':tower,
        'boost_counterexample':{'u_before':u,'beta':0.6,'u_after':boosted},
        'helix_reference':geom,
        'running_alpha':{'alpha0_inverse':ALPHA_INV_0,'alphaMZ_MS_inverse':ALPHA_INV_MZ_MS,
                         'alpha_MZ_over_alpha0':ALPHA_INV_0/ALPHA_INV_MZ_MS},
        'muon_to_electron_mass_ratio':MUON_ELECTRON_RATIO,
        'orbit':{k:v for k,v in orbit.items() if not isinstance(v,np.ndarray)},
        'interpretation':'All numeric rotor spectrum values are synthetic; SI numerical hbar and epsilon0 are references, not a self-consistent unconverted SI-to-c=1 calculation; no four-force unification claimed.'
    }

if __name__ == '__main__':
    here=Path(__file__).resolve().parents[1]
    out=here/'results'/'numerical_results.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(compute_report(),indent=2,ensure_ascii=False),encoding='utf-8')
    print('results:',out)
    print(json.dumps({k:v for k,v in compute_report().items() if k in ['alpha_0','boost_counterexample','orbit','running_alpha']},indent=2))


def internal_covariant_rate(theta_dot:float, normal_connection:float, em_pullback:float, lam:float) -> float:
    """Xi = d theta/ds + Omega_perp + lambda A_mu u^mu.
    Omega_perp is a Lorentz-scalar pullback of an SO(2) normal-plane connection,
    provided the internal oriented 2-plane has actually been supplied.
    """
    return theta_dot+normal_connection+lam*em_pullback


def finite_frame_winding_amplitude(n:int, winding:int) -> complex:
    """Quantum change of amplitude on a closed SO(2) frame-gauge loop."""
    return complex(np.exp(-1j*2*math.pi*n*winding))
