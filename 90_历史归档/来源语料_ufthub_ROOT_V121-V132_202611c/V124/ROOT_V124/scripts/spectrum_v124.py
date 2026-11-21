"""ROOT V124: mathematical tests of Yukawa spectra, not evidence of a fifth force.

Models: K(r)=A+sum_j B_j(1+k_j*r)exp(-k_j*r) for r outside a source.
F(r)=-K'(r)/r=sum_j B_j k_j^2 exp(-k_j*r).
All input radii are metres; sample calculations are SYNTHETIC.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, log, sqrt
from typing import Sequence
import numpy as np
import mpmath as mp

R_EARTH = 6_371_000.0
ELL = 124_600.0
ALPHA_Y = 1.0 / 3.0


def phi_earth_analytic(ell: float = ELL) -> float:
    """Fayet 2026 improved analytic Earth-density form factor φ(x).

    May exceed ordinary floating-point range for very short ell; in that case
    use phi_earth_scaled(), the physical observable φ*exp(-R/ell).
    """
    if ell <= 0: raise ValueError('ell>0')
    x = R_EARTH / ell
    if x < 0.02:
        return 1+x*x/12+11*x**4/4032+29*x**6/604800
    if x > 650:
        raise OverflowError('phi overflows float; use scaled phi')
    return float(((7*x*x-24)*np.cosh(x)+9*x*np.sinh(x)-4*x*x+24)/(4*x**4))


def phi_earth_scaled(ell: float = ELL) -> float:
    """Stable φ(x)*exp(-x) for x=R/ell, including x>>700 and x~0."""
    if ell <= 0: raise ValueError('ell>0')
    x = R_EARTH / ell
    if x < 40:
        return phi_earth_analytic(ell)*exp(-x)
    e1=exp(-x);e2=e1*e1
    return ((7*x*x-24)*(1+e2)+9*x*(1-e2)+(-8*x*x+48)*e1)/(8*x**4)


def earth_profile(heights_m, ell: float = ELL, alpha: float = ALPHA_Y):
    """Normalised acceleration anomaly epsilon(h), finite spherical source.

    Computes the observable φ*exp(-R/ell) before multiplying exp(-h/ell),
    preventing exp(+R/ell) overflow for short positive ranges.
    """
    h = np.asarray(heights_m, dtype=float)
    if np.any(h < 0): raise ValueError('outside spherical source only')
    if ell <= 0: raise ValueError('ell>0')
    r = R_EARTH+h
    return alpha*phi_earth_scaled(ell)*(1+r/ell)*np.exp(-h/ell)


def point_source_profile(heights_m, ell: float = ELL, alpha: float = ALPHA_Y):
    h = np.asarray(heights_m, dtype=float)
    r = R_EARTH+h
    return alpha*(1+r/ell)*np.exp(-r/ell)


def model_K(radii: Sequence[float], A: float, terms: Sequence[tuple[float,float]]) -> np.ndarray:
    rr = np.asarray(radii,float)
    return A+sum(B*(1+rr*k)*np.exp(-rr*k) for B,k in terms)


def ideal_F_at_height(heights_m: Sequence[float], ranges_m: Sequence[float],
                      weights_at_ground: Sequence[float]) -> np.ndarray:
    """F(R+h)=sum_j w_j exp(-h/ell_j); arbitrary positive units.

    w_j=B_j*k_j^2*exp(-k_j*R) and already includes source geometry.
    """
    rr=np.asarray(ranges_m,float)
    ww=np.asarray(weights_at_ground,float)
    hh=np.asarray(heights_m,float)
    if rr.ndim!=1 or ww.ndim!=1 or len(rr)!=len(ww) or len(rr)==0:
        raise ValueError('spectrum size mismatch')
    if np.any(rr<=0) or np.any(ww<0) or not np.any(ww>0):
        raise ValueError('positive ranges and nonnegative nonzero weights required')
    return np.exp(-hh[:,None]/rr[None,:]) @ ww


def moments_at_height(h_m: float, ranges_m: Sequence[float],
                      weights_at_ground: Sequence[float]):
    ranges=np.asarray(ranges_m,float)
    weights=np.asarray(weights_at_ground,float)
    if np.any(ranges<=0) or np.any(weights<0) or sum(weights)<=0:
        raise ValueError('positive spectrum only')
    kj=1/ranges
    fj=weights*np.exp(-h_m/ranges)
    f=float(sum(fj)); fprime=float(-sum(fj*kj)); fsecond=float(sum(fj*kj*kj))
    curvature=f*fsecond-fprime*fprime
    k_eff=-fprime/f
    variance=curvature/(f*f)
    return {'F':f,'Fprime':fprime,'Fsecond':fsecond,'curvature':curvature,
            'k_effective':k_eff,'ell_effective_m':1/k_eff,
            'dk_effective_dr':-variance,'variance_k':variance}


def spectral_hankel_3(f0: float,f1: float,f2: float) -> float:
    return f0*f2-f1*f1


def prony_five_decimal(ks: Sequence[str|float], r0_m: float,delta_m: float,dps=100):
    """Five K heights, repeated-root 5-height inverse plus physical Yukawa constraint.

    q=J/(2H), H=D0*D2-D1^2, J=D0*D3-D1*D2.
    For Yukawa, u/v=r0/delta-1/ln(q). Fails even if Prony is valid.
    Values should be passed as *decimal strings* when high precision matters.
    """
    if len(ks)!=5 or delta_m<=0 or r0_m<=0: raise ValueError('5 heights; positive radii')
    with mp.workdps(dps):
        K=[mp.mpf(str(z)) for z in ks]
        D=[K[i+1]-K[i] for i in range(4)]
        H=D[0]*D[2]-D[1]**2
        J=D[0]*D[3]-D[1]*D[2]
        if H==0: raise ValueError('degenerate Hankel')
        q=J/(2*H)
        if not mp.mpf(0)<q<mp.mpf(1): raise ValueError('nonphysical q')
        b=D[1]/q-D[0]
        if b==0: raise ValueError('degenerate repeated-root coefficient')
        u_over_v=D[0]/b-q/(q-1)
        required=mp.mpf(str(r0_m))/mp.mpf(str(delta_m))-1/mp.log(q)
        d0_recon=D[0]
        d2_recon=q**2*(D[0]+2*b)
        d3_recon=q**3*(D[0]+3*b)
        return {'q':float(q),'ell_m':float(-mp.mpf(str(delta_m))/mp.log(q)),
                'u_over_v':float(u_over_v), 'required_u_over_v':float(required),
                'shape_residual':float(u_over_v-required),
                'recurrence_residual_D2':float(D[2]-d2_recon),
                'recurrence_residual_D3':float(D[3]-d3_recon),
                'hankel_H':float(H)}


def exact_K_decimal(r0_m: float, delta_m: float, ell_m: float,
                    A: str='1', B: str='0.01', n: int=5, dps=110) -> list[str]:
    with mp.workdps(dps):
        r0=mp.mpf(str(r0_m)); delta=mp.mpf(str(delta_m))
        k=1/mp.mpf(str(ell_m)); a=mp.mpf(A); b=mp.mpf(B)
        return [mp.nstr(a+b*(1+k*(r0+i*delta))*mp.exp(-k*(r0+i*delta)),dps-5) for i in range(n)]


def fake_prony_decimal(r0_m: float, delta_m: float, ell_m: float,
                       A: str='1', u: str='0.01', v: str='0.0002', n: int=5,dps=110):
    with mp.workdps(dps):
        q=mp.exp(-mp.mpf(str(delta_m))/mp.mpf(str(ell_m)))
        a=mp.mpf(A); uu=mp.mpf(u); vv=mp.mpf(v)
        return [mp.nstr(a+(uu+vv*i)*q**i,dps-5) for i in range(n)]


def spectral_mc(n: int=4000,step_m: float=50_000.,noise: float=1e-3, seed: int=20261121):
    """Signs of 3-point Hankel for F, with additive Gaussian point noise.

    Deliberately illustrates single spectrum false positives ~50%; not real inference.
    """
    if n<=0 or step_m<=0 or noise<0: raise ValueError('invalid simulation')
    rng=np.random.default_rng(seed)
    h=np.arange(3)*step_m
    out={}
    for name,rr,w in [('single',[ELL],[1.0]),('double',[ELL,300_000.],[0.6,0.4])]:
        truth=ideal_F_at_height(h,rr,w)
        z=truth+rng.normal(0,noise*truth[0],size=(n,3))
        hh=z[:,0]*z[:,2]-z[:,1]**2
        out[name]={'true_H':float(spectral_hankel_3(*truth)),
                   'fraction_H_positive':float(np.mean(hh>0)),
                   'H_p2_5_p50_p97_5':np.percentile(hh,[2.5,50,97.5]).tolist()}
    return {'n':n,'step_m':step_m,'sigma_over_F0':noise,'seed':seed,**out}
