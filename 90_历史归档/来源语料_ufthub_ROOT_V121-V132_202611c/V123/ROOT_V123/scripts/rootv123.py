"""ROOT V123 - amplitude-free exact three-height Yukawa inverse.

All measurements are SYNTHETIC and all satellite/geodesy predictions are
conditional on static spherical linear unscreened Yukawa assumptions.
Mathematical formulae are known exponential/Laplace transform properties;
no fifth-force detection or unification is implied.
"""
from __future__ import annotations
import math
from typing import Sequence
import numpy as np
from scipy.optimize import brentq
from rootv120 import R_EARTH, MU_EARTH_REF, C_LIGHT, ELL_PRE_REGISTERED, ground_fraction, relative_yukawa, two_range_gm
from rootv122 import epsilon, frequencies


def weighted_offset_fraction(z: float) -> float:
    """E[t]/Delta for weight exp(-z*t/Delta), 0<=t<=Delta.

    Handles the removable singularity at z=0 without cancellation.
    """
    if z < 0 or not math.isfinite(z):
        raise ValueError('z must be finite and nonnegative')
    if z == 0:
        return .5
    if z < 1e-3:
        return .5-z/12+z**3/720-z**5/30240
    if z > 650:
        return 1/z
    return 1/z-1/math.expm1(z)


def adjacent_difference_ratio(k: float, r: float, delta: float) -> float:
    """Q(k)=(K(r+2d)-K(r+d))/(K(r+d)-K(r)) for any A,B!=0.

    Stable version of ratio of weighted integrals, no subtraction of near-1 K.
    """
    if not math.isfinite(k) or k < 0 or r <= 0 or delta <= 0:
        raise ValueError('k>=0, r>0, delta>0 required')
    z=k*delta
    tbar=delta*weighted_offset_fraction(z)
    return math.exp(-z)*(1+delta/(r+tbar))


def ratio_from_three(ks: Sequence[float]) -> float:
    if len(ks) != 3:
        raise ValueError('exactly three apparent-GM values required')
    d0=float(ks[1])-float(ks[0])
    d1=float(ks[2])-float(ks[1])
    if d0 == 0:
        raise ValueError('zero first difference: nonidentifiable')
    return d1/d0


def three_height_shape_bounds(q_obs: float, r: float, delta: float) -> dict:
    """Conservative explicit inverse bounds independent of A,B.

    Q=e^-z*(1+Delta/(r+E[t])), E[t] in (0,Delta/2).
    0<k_lower<k_true<k_upper for a strictly positive Yukawa k.
    """
    if r<=0 or delta<=0:
        raise ValueError('r and delta must be positive')
    q_max=(r+1.5*delta)/(r+.5*delta)
    if not 0<q_obs<q_max:
        raise ValueError('ratio incompatible with finite k>0 single Yukawa')
    k_lower=math.log((1+delta/(r+delta/2))/q_obs)/delta
    k_upper=math.log((1+delta/r)/q_obs)/delta
    return dict(q_max=q_max,k_lower=k_lower,k_upper=k_upper,
                ell_lower=1/k_upper,ell_upper=1/k_lower)


def invert_three_heights(ks: Sequence[float], r: float, delta: float) -> dict:
    """Unique positive range from 3 radii; excludes B=0, invalid signs etc.

    Caution: arbitrary triples may pass, and do not confirm a Yukawa force.
    """
    if len(ks) != 3:
        raise ValueError('need 3 K values')
    d0=float(ks[1])-float(ks[0]);d1=float(ks[2])-float(ks[1])
    if d0*d1 <= 0:
        raise ValueError('nonzero adjacent differences must have same sign')
    q_obs=ratio_from_three(ks)
    bounds=three_height_shape_bounds(q_obs,r,delta)
    # z=k*delta, monotone on [0,infinity).
    hi=max(1., -math.log(q_obs)+2)
    while adjacent_difference_ratio(hi/delta,r,delta)>q_obs and hi<700:
        hi*=2
    if hi>=700 and adjacent_difference_ratio(hi/delta,r,delta)>q_obs:
        raise ValueError('outside resolvable floating-point range')
    z=brentq(lambda z: adjacent_difference_ratio(z/delta,r,delta)-q_obs,
             0.,hi,xtol=1e-14,rtol=9e-15)
    k=z/delta
    return dict(r_m=r,step_m=delta,d0=d0,d1=d1,Q=q_obs,
                k_inverse_m=k,ell_m=1/k,**bounds)


def synthetic_three(r: float, delta: float, ell: float, amplitude: float=.005954404898918548,
                    base: float=1.):
    if ell<=0 or amplitude==0:
        raise ValueError('ell>0 and nonzero amplitude required')
    h=np.arange(3,dtype=float)*delta+(r-R_EARTH)
    return np.asarray(base+amplitude*relative_yukawa(h,ell),float)


def recover_windows(ks: Sequence[float], r0: float, step: float):
    k=np.asarray(ks,float)
    return [invert_three_heights(k[i:i+3],r0+i*step,step)['ell_m']
            for i in range(len(k)-2)]


def gaussian_ratio_uncertainty(ks: Sequence[float], covariance: np.ndarray) -> dict:
    """Linear propagation for Q=(K2-K1)/(K1-K0)."""
    y=np.asarray(ks,float)
    C=np.asarray(covariance,float)
    if y.shape!=(3,) or C.shape!=(3,3):
        raise ValueError('3 observations and 3x3 covariance required')
    d0=y[1]-y[0];d1=y[2]-y[1]
    if d0==0:
        raise ValueError('nonidentifiable')
    grad=np.array([d1/d0**2,-(d0+d1)/d0**2,1/d0])
    variance=float(grad@C@grad)
    if variance<0:
        raise ValueError('invalid covariance')
    return {'Q':d1/d0,'gradient':grad.tolist(), 'sigma_Q':math.sqrt(variance)}


def inverse_condition_number(ks: Sequence[float],r:float,delta:float, covariance: np.ndarray):
    """delta method: sigma_ell = |d ell / d Q| sigma_Q.

    Uncertain because correlated errors/physical nuisance not captured by C.
    """
    fit=invert_three_heights(ks,r,delta)
    k=fit['k_inverse_m']
    # d log Q/dk = -(mean radius in next weighted window
    #                - mean radius in first weighted window).
    # The extra radial factor s means the two weighted means do not shift
    # by precisely Delta, so estimate this derivative numerically.
    hk=max(1e-12,k*1e-4)
    kminus=max(0.,k-hk)
    dQdk=(adjacent_difference_ratio(k+hk,r,delta)-adjacent_difference_ratio(kminus,r,delta))/(k+hk-kminus)
    sigQ=gaussian_ratio_uncertainty(ks,covariance)['sigma_Q']
    sig_ell=abs(sigQ/(k*k*dQdk))
    return {**fit, 'sigma_Q_linear':sigQ,'sigma_ell_m_linear':sig_ell,
            'dQdk':dQdk}


def synthetic_mc(r=R_EARTH,delta=100_000.,n=2500,noise_sigma=1e-7,
                 shared_sigma=0.,seed=20261121):
    """Monte Carlo of 3-height inversion. Every input and output synthetic."""
    rng=np.random.default_rng(seed)
    y=synthetic_three(r,delta,ELL_PRE_REGISTERED,
                      amplitude=ground_fraction())
    estimates=[];invalid=0
    for _ in range(n):
        z=y+rng.normal(0,noise_sigma,3)+rng.normal(0,shared_sigma)
        try:
            estimates.append(invert_three_heights(z,r,delta)['ell_m'])
        except ValueError:
            invalid+=1
    p=np.percentile(estimates,[2.5,50,97.5]).tolist() if estimates else None
    return {'seed':seed,'n':n,'invalid':invalid,'accepted':len(estimates),
            'noise_sigma_independent':noise_sigma,'noise_sigma_shared':shared_sigma,
            'ell_truth_m':ELL_PRE_REGISTERED,'p2_5_p50_p97_5_m':p}


def compare_synthetic_single_double(r0=R_EARTH,step=50_000.,count=8):
    heights=np.arange(count)*step+(r0-R_EARTH)
    eps=ground_fraction()
    one=1+eps*relative_yukawa(heights,ELL_PRE_REGISTERED)
    two=two_range_gm(heights,ELL_PRE_REGISTERED,300_000.,eps,.5)
    return {'heights_km':(heights/1e3).tolist(),
            'single_ell_windows_m':recover_windows(one,r0,step),
            'double_ell_windows_m':recover_windows(two,r0,step),
            'single_values':one.tolist(),'double_values':two.tolist()}


def orbit_comparison(h=400_000.,mu=MU_EARTH_REF,
                     J2_ref=1.08263e-3, inclination_deg=45.):
    """Qualitative comparison of near-circular central-Yukawa, GR and J2.

    J2 formula is argument of perigee in an axisymmetric non-spherical model;
    it is NOT literally interchangeable with spherical epicyclic prediction.
    """
    r=R_EARTH+h
    newton_GR=6*math.pi*mu/(C_LIGHT*C_LIGHT*r)
    yukawa=frequencies(r)['periapsis']
    i=math.radians(inclination_deg)
    J2_omega=(3*math.pi/2)*J2_ref*(R_EARTH/r)**2*(5*math.cos(i)**2-1)
    return {'altitude_km':h/1e3,'yukawa_spherical_epicycle_rad':yukawa,
            'Schwarzschild_GR_periapsis_rad':newton_GR,
            'J2_argument_of_perigee_rad_per_orbit':J2_omega,
            'reference_J2':J2_ref,'inclination_deg':inclination_deg,
            'different_apsidal_conventions_warning':True}


def amplitude_sign_and_fixed_alpha_test(ks: Sequence[float],
                                        heights_m: Sequence[float],
                                        ell:float=ELL_PRE_REGISTERED,
                                        epsilon_expected: float|None=None) -> dict:
    """Second-layer physics test: does 3-height inferred range also match
    the fixed α=1/3 source amplitude? A,C profiled from first two points.

    Positive C/A necessary for the attractive, unscreened fixed candidate.
    Result is a model diagnostic only, not an observed likelihood.
    """
    y=np.asarray(ks,float)
    heights=np.asarray(heights_m,float)
    if y.ndim!=1 or len(y)<2 or y.shape!=heights.shape or ell<=0:
        raise ValueError('matching heights and values required')
    if epsilon_expected is None:
        epsilon_expected=ground_fraction(ell)
    f=relative_yukawa(heights,ell)
    if f[1]==f[0]:raise ValueError('no range to estimate amplitude')
    C=(y[1]-y[0])/(f[1]-f[0]); A=y[0]-C*f[0]
    if A==0:raise ValueError('zero Newtonian baseline')
    eps=float(C/A)
    predictions=A+C*f
    return {'baseline_A':float(A),'anomaly_C':float(C),
            'epsilon_inferred':eps,'epsilon_fixed_expected':float(epsilon_expected),
            'fixed_alpha_fractional_mismatch':eps/epsilon_expected-1,
            'attractive_source_sign_passes':bool(A>0 and C>0),
            'max_abs_holdout_error':float(np.max(abs(y[2:]-predictions[2:]))) if len(y)>2 else None,
            'n_holdout':int(max(0,len(y)-2))}
