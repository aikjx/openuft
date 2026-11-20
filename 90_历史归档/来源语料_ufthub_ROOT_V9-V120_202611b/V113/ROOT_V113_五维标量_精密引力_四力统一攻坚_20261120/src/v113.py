"""ROOT V113: falsifiable scalar-tensor, equivalence-principle and torsion audits.

Mathematical conventions: Jordan metric minimally coupled to matter; omega > -3/2;
finite scalar range and local gamma(r) are weak-field toy observables, not a
reanalysis of Cassini's light path. No new fundamental physics is claimed.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

C = 299_792_458.0
HBAR_C_EV_M = 1.973269804593025e-7    # eV*m
AU_M = 149_597_870_700.0
CASSINI_CENTER = 2.1e-5            # gamma-1
CASSINI_SIGMA = 2.3e-5             # 1 sigma
MICROSCOPE_ETA_CENTER = -1.5e-15
MICROSCOPE_STAT = 2.3e-15
MICROSCOPE_SYST = 1.5e-15


def alpha2(omega: float) -> float:
    """Square of dimensionless massless Einstein-frame scalar coupling."""
    if omega <= -1.5:
        raise ValueError('Require 2omega+3 > 0 (positive scalar kinetic coefficient)')
    return 1.0 / (2.0 * omega + 3.0)


def measured_newton_G(bare_G: float, phi0: float, omega: float) -> float:
    """Massless BD weak-field Cavendish normalization; inputs remain independent.

    G_N=(bare_G/phi0)*(2omega+4)/(2omega+3).
    This relationship does not independently predict G_N.
    """
    if bare_G<=0 or phi0<=0:raise ValueError('positive gravitational prefactor and scalar background')
    alpha2(omega)
    return (bare_G/phi0)*(2*omega+4)/(2*omega+3)


def gamma_bd(omega: float) -> float:
    """Brans-Dicke massless, standard universal Jordan-matter coupling."""
    return 1.0 + gamma_minus_one_bd(omega)


def gamma_minus_one_bd(omega: float) -> float:
    if omega <= -1.5:
        raise ValueError('Require 2omega+3 > 0')
    return -1.0 / (omega + 2.0)


def gamma_alpha(alpha_sq: float) -> float:
    if alpha_sq < 0:
        raise ValueError('alpha^2 cannot be negative')
    return (1.0-alpha_sq)/(1.0+alpha_sq)


def zscore_cassini(gamma: float) -> float:
    """Only Gaussian proxy using the published gamma point measurement."""
    return (gamma - 1.0 - CASSINI_CENTER)/CASSINI_SIGMA


def omega_min_at_sigma(nsigma: float=2.0) -> float:
    """One-sided omega lower bound conditional on gamma<=1, Gaussian proxy.

    gamma-1 >= measured_center - n_sigma*reported_sigma.
    """
    delta = nsigma * CASSINI_SIGMA - CASSINI_CENTER
    if delta <= 0:
        raise ValueError('No allowed gamma<=1 from selected one-sided window')
    return 1.0 / delta - 2.0


def gamma_eff(r_m: float, omega: float, scalar_mass_eV: float) -> float:
    """Illustrative local weak-field Yukawa PPN ratio, NOT a Cassini data fit."""
    if r_m < 0 or scalar_mass_eV < 0:
        raise ValueError('Distance and mass must be nonnegative')
    a2=alpha2(omega)
    u=a2*math.exp(-r_m*scalar_mass_eV/HBAR_C_EV_M)
    return (1.0-u)/(1.0+u)


def gamma_eff_minus_one(r_m: float, omega: float, scalar_mass_eV: float) -> float:
    if r_m < 0 or scalar_mass_eV < 0:
        raise ValueError('Distance and mass must be nonnegative')
    u=alpha2(omega)*math.exp(-r_m*scalar_mass_eV/HBAR_C_EV_M)
    return -2.0*u/(1.0+u)


def mass_eV_from_range_m(range_m: float) -> float:
    if range_m <= 0:raise ValueError('Positive range required')
    return HBAR_C_EV_M/range_m


def range_m_from_mass_eV(mass_eV: float) -> float:
    if mass_eV <= 0:raise ValueError('Positive mass required')
    return HBAR_C_EV_M/mass_eV


def proxy_mass_min_eV(r_m: float, omega: float=0.0, nsigma: float=2.0) -> float:
    """Toy sufficient mass for a *local* gamma(r) proxy to lie in Cassini band.

    NOT a physical bound from Cassini: real time delay is a path integral and
    sensitive to solar impact parameter, not just distance r.
    """
    delta=nsigma*CASSINI_SIGMA - CASSINI_CENTER
    if r_m<=0:raise ValueError('Positive proxy observation distance required')
    if delta<=0:raise ValueError('Invalid band for gamma<=1')
    a2=alpha2(omega)
    u_limit=delta/(2.0-delta)
    if a2<=u_limit: return 0.0
    return HBAR_C_EV_M/r_m * math.log(a2/u_limit)


def yukawa_gradient_factor(r_m:float,scalar_mass_eV:float) -> float:
    if r_m<0 or scalar_mass_eV<0:raise ValueError
    x=r_m*scalar_mass_eV/HBAR_C_EV_M
    return (1.0+x)*math.exp(-x) if x < 740 else 0.0


def eotvos_eta(alpha_a:float,alpha_b:float,alpha_s:float,r_m:float,scalar_mass_eV:float)->float:
    """Signed eta = 2(a_A-a_B)/(a_A+a_B), Newtonian Yukawa toy model."""
    x=yukawa_gradient_factor(r_m,scalar_mass_eV)
    d_a=alpha_a*alpha_s*x
    d_b=alpha_b*alpha_s*x
    if 2+d_a+d_b <= 0:raise ValueError('Effective accelerations unphysical')
    return 2*(d_a-d_b)/(2+d_a+d_b)


def microscope_sigma_combined()->float:
    return math.hypot(MICROSCOPE_STAT,MICROSCOPE_SYST)


def microscope_conservative_abs_band(nsigma:float=2.0)->float:
    """Conservative illustrative absolute band, not an official combined CL."""
    return abs(MICROSCOPE_ETA_CENTER)+nsigma*microscope_sigma_combined()


def local_gamma_jacobian(r_m:float,a2:float,range_m:float)->tuple[float,float]:
    """(d gamma/d(a^2), d gamma/d range) at fixed position, a2>0, range>0."""
    if a2<=0 or range_m<=0 or r_m<0:raise ValueError
    y=math.exp(-r_m/range_m)
    u=a2*y
    deriv_a=-2*y/(1+u)**2
    deriv_range=deriv_a*a2*r_m/range_m**2
    return deriv_a,deriv_range


def two_scale_det(r1:float,r2:float,a2:float,range_m:float)->float:
    a,b=local_gamma_jacobian(r1,a2,range_m)
    c,d=local_gamma_jacobian(r2,a2,range_m)
    return a*d-c*b


def algebraic_torsion_solution(j:float,g:float,m2:float)->float:
    """Toy L=-M^2/2 S^2 + g S J: auxiliary torsion field solution."""
    if m2<=0:raise ValueError('Positive mass-squared required')
    return g*j/m2


def torsion_effective_contact(j:float,g:float,m2:float)->float:
    """Effective L after eliminating algebraic S. Not a propagating force."""
    return g*g*j*j/(2*m2)


def torsion_lagrangian(s:float,j:float,g:float,m2:float)->float:
    if m2<=0:raise ValueError
    return -.5*m2*s*s+g*s*j


def wrap_summary()->dict:
    a=alpha2(0.)
    o=omega_min_at_sigma(2.)
    mass=proxy_mass_min_eV(AU_M)
    return {'kk_omega':0.,'kk_gamma':gamma_bd(0.),'cassini_z':zscore_cassini(gamma_bd(0.)),
            'omega_min_2sigma_proxy':o,'kk_alpha2':a,
            'massive_proxy_1AU_eV':mass,'massive_proxy_1AU_lambda_m':range_m_from_mass_eV(mass),
            'microscope_sigma_combined':microscope_sigma_combined(),
            'microscope_abs_band_2sigma_illustrative':microscope_conservative_abs_band(2.),
            'science_status':'5D massless KK weak-field model excluded under specified assumptions; four-force unification OPEN'}
