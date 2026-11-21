"""ROOT V121: explicit mathematical and physical hypothesis audit.

All satellite/geodesy outputs below are synthetic forecasts, NEVER observational fits.
No grand unification or new force discovery is claimed.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from scipy.optimize import brentq
from rootv120 import (R_EARTH, ELL_PRE_REGISTERED, ALPHA_PRE_REGISTERED,
                      ground_fraction, relative_yukawa, near_circular_precession_rad,
                      apparent_gm, finite_spectrum, two_range_gm, extra_clock_shift,
                      MU_EARTH_REF, C_LIGHT, HBAR)

CODATA2022_INV_ALPHA = 137.035999177
CODATA2022_INV_ALPHA_STD = 0.000000021
CODATA2022_MP_ME = 1836.152673426
CODATA2022_MP_ME_STD = 0.000000032
ELECTRON_MASS = 9.1093837139e-31  # only for illustrative Compton radius; not CODATA precision audit


def yukawa_epsilon(height_m, ell_m=ELL_PRE_REGISTERED, alpha=ALPHA_PRE_REGISTERED,
                   density_model='improved'):
    return ground_fraction(ell_m,alpha,density_model)*relative_yukawa(height_m,ell_m)


def mu_free_altitude_ratio(h1_m,h2_m,ell_m=ELL_PRE_REGISTERED,
                           alpha=ALPHA_PRE_REGISTERED,density_model='improved'):
    """K(h1)/K(h2), with unknown common G_infty*M exactly eliminated."""
    ep1=yukawa_epsilon(h1_m,ell_m,alpha,density_model)
    ep2=yukawa_epsilon(h2_m,ell_m,alpha,density_model)
    return float((1+ep1)/(1+ep2))


def log_slope_K(height_m, ell_m=ELL_PRE_REGISTERED,alpha=ALPHA_PRE_REGISTERED,
                density_model='improved'):
    """S = d ln K / d ln r, for the assumed spherical Yukawa model."""
    r=R_EARTH+float(height_m)
    e=float(yukawa_epsilon(height_m,ell_m,alpha,density_model))
    x=r/ell_m
    return -(e/(1+e))*x*x/(1+x)


def precession_from_slope(s):
    """Generic Newtonian spherical central-force near-circular orbit identity."""
    if s<=-1:
        return math.nan
    return 2*math.pi*(1/math.sqrt(1+s)-1)


def precession_from_fixed_model(h_m):
    return near_circular_precession_rad(h_m,ELL_PRE_REGISTERED,
                                       ground_fraction(ELL_PRE_REGISTERED))


def three_height_ratio(h0_m,step_m,ell_m):
    e=relative_yukawa(np.array([h0_m, h0_m+step_m, h0_m+2*step_m]),ell_m)
    return float((e[0]-e[1])/(e[1]-e[2]))


def recover_ell_three(h0_m,step_m,K012,ell_min=10000.,ell_max=2e6):
    """Three-height physical Yukawa inversion; no A, B input.

    Returns nan if the observed ratio lies outside the candidate domain.
    """
    vals=np.asarray(K012,dtype=float)
    if len(vals)!=3 or step_m<=0 or not np.all(np.isfinite(vals)):
        raise ValueError('Exactly 3 finite K values and positive step required')
    d0=vals[0]-vals[1]; d1=vals[1]-vals[2]
    if abs(d1)<1e-20:
        return math.nan
    obs=d0/d1
    def z(ell):
        return three_height_ratio(h0_m,step_m,ell)-obs
    lo=z(ell_min); hi=z(ell_max)
    if lo*hi>0:
        return math.nan
    return float(brentq(z,ell_min,ell_max,xtol=1e-8))


def five_height_prony(K,delta_m):
    arr=np.asarray(K,dtype=float)
    if len(arr)!=5: raise ValueError('Five heights required')
    d=np.diff(arr)
    H=d[0]*d[2]-d[1]*d[1]
    J=d[0]*d[3]-d[1]*d[2]
    P=d[0]*J*J-4*d[1]*J*H+4*d[2]*H*H
    q=J/(2*H) if H!=0 else math.nan
    ell=(-delta_m/math.log(q)) if (0<q<1) else math.nan
    return {'H0':float(H),'J0':float(J),'P5':float(P),
            'q':float(q),'ell_m':float(ell)}


def helix_speed(vtheta,vz):
    """Ordinary 3D cylindrical helix: transverse and axial velocity orthogonal."""
    return math.hypot(vtheta,vz)


def kk_mass_level_ratio(n1,n2):
    """Toy 5D compact dimension, same radius and purely KK mass m_n∝|n|."""
    if n1==0: raise ZeroDivisionError('zero mode is massless in toy model')
    return abs(n2/n1)


def alpha_numerology_audit():
    predicted_inverse=4*math.pi**3+math.pi**2+math.pi
    return {'inverse_alpha_geometric':predicted_inverse,
            'inverse_alpha_CODATA2022':CODATA2022_INV_ALPHA,
            'difference':predicted_inverse-CODATA2022_INV_ALPHA,
            'relative_error_ppm':(predicted_inverse/CODATA2022_INV_ALPHA-1)*1e6,
            'difference_in_CODATA_std':(predicted_inverse-CODATA2022_INV_ALPHA)/CODATA2022_INV_ALPHA_STD}


def proton_ratio_audit():
    expression=2*math.pi*3**3+2*math.pi
    return {'expression_2pi_3cubed_plus_2pi':expression,
            'CODATA2022_mp_over_me':CODATA2022_MP_ME,
            'difference':expression-CODATA2022_MP_ME,
            'difference_in_CODATA_std':(expression-CODATA2022_MP_ME)/CODATA2022_MP_ME_STD,
            'nearest_integer':round(CODATA2022_MP_ME),
            'gap_to_integer':CODATA2022_MP_ME-round(CODATA2022_MP_ME)}


def centered_difference_derivative(fun,x,dx):
    return (fun(x+dx)-fun(x-dx))/(2*dx)


def gaussian_chi2_null_vs_fixed(heights, y, covariance):
    """Synthetic proxy: both models have ONE free common normalization; ell, alpha fixed.
    This MUST NOT be interpreted as observational constraints or true satellite POD.
    """
    x=np.asarray(heights,dtype=float)
    y=np.asarray(y,dtype=float)
    C=np.asarray(covariance,dtype=float)
    if C.shape!=(len(y),len(y)): raise ValueError('covariance shape mismatch')
    W=np.linalg.inv(C)
    def fit_basis(b):
        mu=(b@W@y)/(b@W@b)
        r=y-mu*b
        return {'mu':float(mu),'chi2':float(r@W@r)}
    return {'fixed':fit_basis(1+yukawa_epsilon(x)),
            'newtonian_null':fit_basis(np.ones_like(y)),
            'observation_status':'SYNTHETIC ONLY'}


def whitened_model_residuals(y,template,covariance):
    """GLS profile out common normalization, whiten via Cholesky."""
    L=np.linalg.cholesky(covariance)
    W=np.linalg.inv(covariance)
    mu=float(template@W@y/(template@W@template))
    return np.linalg.solve(L, y-mu*template)


def two_scale_counterexamples():
    h=np.arange(6)*50000.
    eps=ground_fraction()
    out=[]
    for ell2 in [125000.,130000.,300000.]:
        vals=two_range_gm(h,ELL_PRE_REGISTERED,ell2,eps,weight=0.5)
        s=finite_spectrum(vals,50000.)
        out.append({'ell_1_m':ELL_PRE_REGISTERED,'ell_2_m':ell2,
                    'H0':float(s.H[0]),'recovered_ell_m':float(s.ell_five_m),
                    'yukawa_shape_residual_m_over_m':float(s.yukawa_shape_residual)})
    return out


def fixed_prediction_table(heights_m):
    eps=ground_fraction()
    out=[]
    for h in heights_m:
        e=float(yukawa_epsilon(h))
        sl=log_slope_K(h)
        out.append({'altitude_km':float(h/1000),
                    'epsilon':e,
                    'extra_accel_m_s2':float(MU_EARTH_REF/(R_EARTH+h)**2*e),
                    'd_lnK_d_lnr':sl,
                    'near_circular_precession_rad':precession_from_slope(sl)})
    return out
