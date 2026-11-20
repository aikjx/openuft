"""ROOT V118 -- external spherical linear Yukawa gravity observables.

This re-evaluates V117 with a published Earth-like density form factor and
constructs amplitude-free, mass-free multi-altitude consistency tests.
The equations describe established conditional Yukawa phenomenology;
they do not derive a new fundamental force or a unified field theory.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
import numpy as np
from scipy.optimize import brentq

R_EARTH = 6_371_000.0
ELL_BASELINE = 124_599.47973598285  # V117 lambda4=1, measured G calibration
ALPHA_BASELINE = 1.0/3.0
H_BAR_C_EV_M=1.973269804e-7
FIVE_SHELL_WEIGHTS = ((.5,1.0),(.1333,.9953),(.1715,.8948),(.1929,.5462),(.0023,.1916))


def _moments_rhoprime(n: int) -> float:
    """Mass-weighted <u^(2n)> for rho'/rho0 = 5/4-u+1/(3u)."""
    return 3.0*(1.25/(2*n+3)-1.0/(2*n+4)+(1.0/3.0)/(2*n+2))


def _series_s_scaled(x: float, profile: str) -> float:
    """e^-x Phi(x), stable for small x using even-moment series."""
    if profile=='uniform': moments=lambda n: 3.0/(2*n+3)
    elif profile=='inverse_r': moments=lambda n: 2.0/(2*n+2)
    elif profile=='earth_analytic': moments=_moments_rhoprime
    else: raise ValueError(profile)
    total=0.0
    for n in range(24):
        term=moments(n)*x**(2*n)/math.factorial(2*n+1)
        total+=term
        if abs(term)<1e-17*total: break
    return math.exp(-x)*total


def _scaled_uniform(x: float) -> float:
    if x<.2: return _series_s_scaled(x,'uniform')
    return 1.5*((x-1)+(x+1)*math.exp(-2*x))/x**3


def scaled_form(x: float, profile: str='earth_analytic') -> float:
    """Return exp(-x) Phi_profile(x) without overflow/cancellation.

    Source normalization: Phi(0)=1. Surface-density behavior is captured.
    `five_shell_reference` is the approximate published five-shell fit (2026).
    """
    if not math.isfinite(x) or x<0:raise ValueError('x must be nonnegative and finite')
    if profile=='uniform': return _scaled_uniform(x)
    if profile=='inverse_r':
        if x<.2: return _series_s_scaled(x,'inverse_r')
        return (-math.expm1(-x)/x)**2
    if profile=='earth_analytic':
        if x<.2:return _series_s_scaled(x,'earth_analytic')
        z=math.exp(-2*x); y=math.exp(-x)
        return ((7*x*x-24+9*x)+(7*x*x-24-9*x)*z+(-8*x*x+48)*y)/(8*x**4)
    if profile=='five_shell_reference':
        return sum(w*math.exp(-(1-frac)*x)*_scaled_uniform(frac*x)
                   for w,frac in FIVE_SHELL_WEIGHTS)
    raise ValueError(f'Unknown density profile {profile}')


def yukawa_excess(height_m: float, ell_m: float=ELL_BASELINE,
                  alpha: float=ALPHA_BASELINE,
                  profile: str='earth_analytic', radius_m:float=R_EARTH)->float:
    """Linear spherical Yukawa g_Y/g_Newton outside a fixed body, h >=0."""
    if height_m<0 or ell_m<=0 or alpha<0 or radius_m<=0:
        raise ValueError('Require h>=0, ell>0, alpha>=0, R>0')
    x=radius_m/ell_m; u=height_m/ell_m
    return alpha*(1+x+u)*scaled_form(x,profile)*math.exp(-u)


def effective_gm(height_m: float, ell_m: float=ELL_BASELINE,
                 alpha:float=ALPHA_BASELINE,
                 profile:str='earth_analytic', gm_baseline:float=1.0)->float:
    """The inferred r^2*g(r), normalized to a positive GM in units supplied."""
    if gm_baseline<=0:raise ValueError('GM positive')
    return gm_baseline*(1+yukawa_excess(height_m,ell_m,alpha,profile))


def altitude_invariant(ell_m:float, heights_m:tuple[float,float,float],
                       radius_m:float=R_EARTH)->float:
    """(K1-K2)/(K2-K3), independent of GM, alpha and spherical rho.
    Numerically stabilized by factoring out exp(-r1/ell).
    """
    h1,h2,h3=heights_m
    if not(ell_m>0 and 0<=h1<h2<h3):raise ValueError('three ascending external heights')
    d2=(h2-h1)/ell_m;d3=(h3-h1)/ell_m
    x=(radius_m+h1)/ell_m
    u1=1+x
    u2=(1+x+d2)*math.exp(-d2)
    u3=(1+x+d3)*math.exp(-d3)
    den=u2-u3
    if den<=0:raise ValueError('degenerate ratio; use a shorter range bracket')
    return (u1-u2)/den


def invert_range_3heights(heights_m:tuple[float,float,float],ratio:float,
                          lower_m:float=2e3,upper_m:float=5e7)->float:
    """Synthetic three-altitude shape inversion; no data measurement claimed."""
    if not math.isfinite(ratio) or ratio<=0:raise ValueError('ratio must be positive')
    fn=lambda ell:altitude_invariant(ell,heights_m)-ratio
    a=fn(lower_m);b=fn(upper_m)
    if not(a*b<0):raise ValueError('ratio outside inversion bracket')
    return brentq(fn,lower_m,upper_m,xtol=1e-6,rtol=1e-12)


def observed_difference_ratio(K_values: list[float]|tuple[float,...])->float:
    if len(K_values)!=3: raise ValueError('requires 3 altitude measurements')
    numerator=K_values[0]-K_values[1]
    denominator=K_values[1]-K_values[2]
    if denominator==0:raise ValueError('degenerate differences')
    return numerator/denominator


def four_altitude_validation(heights:tuple[float,float,float,float],
                             K:list[float]|tuple[float,...])->dict:
    """Fit ell to first three K; 4th is out-of-sample one-parameter test.
    G*M and Yukawa amplitude are nuisance parameters inferred from first 3.
    """
    if len(K)!=4 or len(heights)!=4 or not all(heights[i]<heights[i+1] for i in range(3)):
        raise ValueError('requires four increasing heights')
    r12=observed_difference_ratio(K[:3]);ell=invert_range_3heights(heights[:3],r12)
    r0=R_EARTH+heights[0]
    def u(h):
        d=h-heights[0]
        return (1+(R_EARTH+h)/ell)*math.exp(-d/ell)
    u1,u2,u4=u(heights[0]),u(heights[1]),u(heights[3])
    slope=(K[0]-K[1])/(u1-u2)
    intercept=K[0]-slope*u1
    K4_pred=intercept+slope*u4
    return {'ell_m':ell,'GM_fitted':intercept,'fourth_predicted':K4_pred,
            'fourth_actual':K[3],'fractional_fourth_residual':(K[3]-K4_pred)/intercept,
            'input_difference_ratio':r12}


def apparent_GM_derivatives(r: float,ell: float,C:float=1.0,GM:float=1.0):
    """Analytic derivatives for K(r)=GM*[1+C*(1+r/ell)*exp(-r/ell)]."""
    if r<=0 or ell<=0 or C<=0:raise ValueError('positive')
    e=math.exp(-r/ell);P=-GM*C*e/(ell*ell)
    K1=P*r
    K2=P*(1-r/ell)
    K3=P*(r/ell**2-2/ell)
    return K1,K2,K3


def local_inverse_range(r:float,Kp:float,Kpp:float):
    if r<=0 or Kp==0:raise ValueError('r>0 Kp!=0')
    return 1.0/r-Kpp/Kp


def differential_closure(r:float,Kp:float,Kpp:float,Kppp:float):
    """(K'')²-K''' K'-(K')²/r²: exact zero for single Yukawa."""
    return Kpp*Kpp-Kppp*Kp-(Kp/r)**2


def mass_ev(ell_m:float)->float:
    if ell_m<=0:raise ValueError('positive range')
    return H_BAR_C_EV_M/ell_m


def epicyclic_observables(height_m:float, ell_m:float=ELL_BASELINE,
                          alpha:float=ALPHA_BASELINE,
                          profile:str='earth_analytic')->dict[str,float|bool]:
    """Nearly circular orbit in central Newton+Yukawa potential.

    Omega_r^2 / Omega_phi^2 = 1 - alpha * Phi * exp(-r/ell)
                                      * (r/ell)^2/(1+Y).
    Ignores J2, tides, drag, GR, atmospheric forces, and spin.
    """
    if height_m<0 or ell_m<=0 or alpha<0:raise ValueError('invalid')
    r=R_EARTH+height_m
    S=scaled_form(R_EARTH/ell_m,profile)*math.exp(-height_m/ell_m)
    q=r/ell_m
    Y=alpha*(1+q)*S
    ep_shift=alpha*q*q*S/(1+Y)
    ratio_sq=1-ep_shift
    return {'radial_to_azimuth_frequency_sq':ratio_sq,
            'radially_stable':ratio_sq>0,
            'pericenter_advance_rad_per_radial_period':
               2*math.pi*(1/math.sqrt(ratio_sq)-1) if ratio_sq>0 else math.nan,
            'yukawa_force_fraction':Y,
            'epicyclic_fractional_shift':ep_shift}
