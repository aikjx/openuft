"""ROOT V117: conditionally specified nonminimal scalar + quartic model.
This is a classical scalar–tensor *test model*, not a grand unified theory.

Natural units ℏ=c=1 inside induced-gravity formulas;
SI lengths and masses for Yukawa observables.
"""
from __future__ import annotations
import math
from dataclasses import dataclass

# Inputs inherited from V115–V116. G and reduced M_P are measured-input
# derived, not predictions. GeV QCD fixed-five-flavor one-loop demonstrator.
V_QCD_GEV = 0.0878270801455
MPL_OBS_GEV = 2.435323460084e18
HBAR_C_EV_M = 1.973269804e-7
EARTH_R_M = 6_371_000.0


def alpha_xi(xi: float) -> float:
    assert xi > 0
    return 2 * xi / (1 + 6 * xi)


def xi_from_newton_calibration(v_gev: float = V_QCD_GEV,
                               mpl_gev: float = MPL_OBS_GEV) -> float:
    """Solve xi*v²=[1+2xi/(1+6xi)] Mobs² for positive xi.
    Solve 6xi²+(1-8R)xi-R=0, R=(Mobs/v)².
    """
    if not(v_gev>0 and mpl_gev>0): raise ValueError('positive mass scale required')
    R = (mpl_gev / v_gev)**2
    b = 1 - 8*R
    D = math.hypot(b, math.sqrt(24*R))
    return (-b + D)/12 if b < 0 else 2*R/(D+b)


def einstein_scale(v_gev: float, xi: float) -> float:
    return math.sqrt(xi)*v_gev


def canonical_scale_f(v_gev: float, xi: float) -> float:
    return v_gev*math.sqrt(1+6*xi)


def canonical_mass_ev(lam4: float, v_gev: float, xi: float) -> float:
    """From U_E''(0)=2 lambda4*v^2/(1+6xi), with energy in eV."""
    if not (lam4>0 and v_gev>0 and xi>0): raise ValueError('lam4, v, xi must be >0')
    return 1e9*math.sqrt(2*lam4)*v_gev/math.sqrt(1+6*xi)


def range_m(lam4: float, v_gev: float, xi: float) -> float:
    return HBAR_C_EV_M / canonical_mass_ev(lam4, v_gev, xi)


def induced_potential_gev4(chi_gev: float, lam4: float,
                           v_gev: float, xi: float) -> float:
    """Exact Einstein-frame potential U_E=lam4*v^4/4*(1-exp(-2chi/f))²."""
    f=canonical_scale_f(v_gev,xi)
    return lam4*v_gev**4/4 * (-math.expm1(-2*chi_gev/f))**2


def matter_factor(chi_gev: float, v_gev: float, xi: float) -> float:
    return math.exp(-chi_gev/canonical_scale_f(v_gev,xi))


def homogeneous_yukawa_form(x: float) -> float:
    """Unscaled uniform sphere form factor; x up to ~600 before overflow."""
    if x<0: raise ValueError('nonnegative x')
    if x<.03:
        return 1+x*x/10+x**4/280+x**6/15120+x**8/1330560
    return 3*(x*math.cosh(x)-math.sinh(x))/x**3


def uniform_scaled_form(x: float, height_over_range: float=0.0) -> float:
    """e^[-(x+h/ell)] Phi_uniform(x), with no overflow for huge x.
    x=R/ell, h>=0. Use small-x stabilized Taylor branch.
    """
    if x<0 or height_over_range<0: raise ValueError('nonnegative arguments required')
    if x<0.03:
        return math.exp(-(x+height_over_range))*homogeneous_yukawa_form(x)
    return 3/(2*x**3)*((x-1)*math.exp(-height_over_range) +
                        (x+1)*math.exp(-2*x-height_over_range))


def inverse_r_scaled_form(x: float, height_over_range: float=0.0) -> float:
    """e^[-(x+h/ell)] Phi_{rho proportional 1/r}(x), same total mass."""
    if x<0 or height_over_range<0: raise ValueError('nonnegative arguments required')
    if x==0: return math.exp(-height_over_range)
    return (-math.expm1(-x))**2 / x**2 * math.exp(-height_over_range)


def yukawa_relative_force_sphere(ell_m: float, altitude_m: float,
                                 radius_m: float=EARTH_R_M,
                                 coupling: float=1/3,
                                 profile: str='uniform') -> float:
    """F_Y/F_Newton for external point test mass and spherical finite-size source.
    Homogeneous and inverse-r shapes are two explicit *toy* Earth profiles.
    """
    if not(ell_m>0 and altitude_m>=0 and radius_m>0 and coupling>=0):
        raise ValueError('invalid physical parameters')
    x=radius_m/ell_m
    u=altitude_m/ell_m
    if profile=='uniform': fac=uniform_scaled_form(x,u)
    elif profile=='inverse_r': fac=inverse_r_scaled_form(x,u)
    else: raise ValueError('unknown density profile')
    return coupling*(1+x+u)*fac


def yukawa_relative_force_point(ell_m: float,r_m:float,coupling:float=1/3) ->float:
    if not(ell_m>0 and r_m>=0):raise ValueError('ell positive and r nonnegative')
    y=r_m/ell_m
    return coupling*(1+y)*math.exp(-y)


def relative_observable_after_G_calibration(ell_m:float,r_m:float,
                                             r_cal_m:float,
                                             coupling:float=1/3)->float:
    """(1+Y(r))/(1+Y(r_cal))-1 for identical point masses.
    Demonstrates why constant 1/3 near-field strength can be absorbed in G.
    """
    return (1+yukawa_relative_force_point(ell_m,r_m,coupling))/(
        1+yukawa_relative_force_point(ell_m,r_cal_m,coupling))-1


def two_altitude_force_ratio(ell_m:float, h1:float,h2:float,
                            radius:float=EARTH_R_M,coupling:float=1/3,
                            profile:str='uniform')->float:
    """Inferred GM at h2 / inferred GM at h1 for same spherical source."""
    y1=yukawa_relative_force_sphere(ell_m,h1,radius,coupling,profile)
    y2=yukawa_relative_force_sphere(ell_m,h2,radius,coupling,profile)
    return (1+y2)/(1+y1)


def mass_eV_from_range(ell_m: float)->float:
    if ell_m<=0:raise ValueError('positive range required')
    return HBAR_C_EV_M/ell_m


def quartic_needed_for_range(target_ell_m: float, v_gev:float, xi:float)->float:
    """Target range or shorter requires lambda4 >= returned threshold."""
    baseline=range_m(1,v_gev,xi)
    return (baseline/target_ell_m)**2


def lambda_upper_weak(upper:float=4*math.pi)->bool:
    return upper>0
