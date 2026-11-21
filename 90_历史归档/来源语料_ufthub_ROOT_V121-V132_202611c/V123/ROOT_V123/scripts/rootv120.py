"""ROOT V120: falsifiable Yukawa spectrum tools (hypothesis, not detection).

SI units throughout. K is apparent GM normalized by mu_inf by default.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, log, pi, sqrt
import numpy as np
from scipy.optimize import minimize_scalar

R_EARTH = 6_371_000.0
MU_EARTH_REF = 3.986004418e14  # illustrative reference; not fitted from tracking here
C_LIGHT = 299_792_458.0
HBAR = 1.054571817e-34
E_CHARGE = 1.602176634e-19
ELL_PRE_REGISTERED = 124_600.0
ALPHA_PRE_REGISTERED = 1.0 / 3.0


def formfactor_times_exp(x: float, model: str = "improved") -> float:
    """Compute Phi(x) * exp(-x) without overflowing for large x.

    improved: Fayet 2026 Eq.(16), rho/rho0=5/4-r/R+R/(3r).
    uniform: constant-density sphere.
    """
    if x < 0:
        raise ValueError("x=R/ell must be nonnegative")
    if x < 0.08:
        # For tiny x, avoid 0/0 cancellation in cosh/sinh expressions.
        # Derived from published small-x expansions of Phi.
        if model == "improved":
            phi = 1 + x*x/12 + 11*x**4/4032
        elif model == "uniform":
            phi = 1 + x*x/10 + x**4/280
        else:
            raise ValueError(model)
        return phi * exp(-x)
    e1, e2 = exp(-x), exp(-2*x)
    if model == "uniform":
        return 3.0*((x-1)+(x+1)*e2)/(2*x**3)
    if model == "improved":
        return (((7*x*x-24+9*x)/2) + ((7*x*x-24-9*x)/2)*e2
                - (4*x*x-24)*e1)/(4*x**4)
    raise ValueError(model)


def ground_fraction(ell: float = ELL_PRE_REGISTERED,
                    alpha: float = ALPHA_PRE_REGISTERED,
                    model: str = "improved") -> float:
    x = R_EARTH / ell
    return alpha * formfactor_times_exp(x, model) * (1+x)


def relative_yukawa(h_m: np.ndarray | float, ell: float, r0: float = R_EARTH):
    """K excess relative to its value at r0 (h=0) for spherical Yukawa force."""
    h = np.asarray(h_m, dtype=float)
    return ((1+(r0+h)/ell)/(1+r0/ell))*np.exp(-h/ell)


def apparent_gm(heights_m: np.ndarray, ell: float, mu: float = 1.,
                epsilon_ground: float | None = None):
    if epsilon_ground is None:
        epsilon_ground = ground_fraction(ell)
    return mu * (1 + epsilon_ground*relative_yukawa(heights_m, ell))


def two_range_gm(heights_m: np.ndarray, ell1: float, ell2: float,
                 epsilon_ground: float, weight: float = 0.5):
    r1 = relative_yukawa(heights_m,ell1)
    r2 = relative_yukawa(heights_m,ell2)
    return 1 + epsilon_ground*(weight*r1 + (1-weight)*r2)


@dataclass
class Spectrum:
    H: np.ndarray
    J0: float
    q_five: float
    ell_five_m: float
    q_six: float
    ell_six_m: float
    recurrence_residual: float
    yukawa_shape_residual: float


def finite_spectrum(k_values: np.ndarray, step_m: float, r0: float = R_EARTH) -> Spectrum:
    """Five-point Prony estimator and six-point Hankel ratio.

    Five-point conditions are necessary for repeated-root exponential polynomials,
    but full Yukawa also imposes u/v=(1+r0/ell)/(step/ell).
    """
    k = np.asarray(k_values, float)
    if len(k) < 5:
        raise ValueError("Need >=5 K samples for five-height algebraic inverse")
    d = np.diff(k)
    h = np.array([d[i]*d[i+2]-d[i+1]**2 for i in range(len(d)-2)])
    h0 = float(h[0]); j0 = float(d[0]*d[3] - d[1]*d[2])
    q = j0/(2*h0) if h0 != 0 else float('nan')
    ell = -step_m/log(q) if 0 < q < 1 else float('nan')
    rec = float(d[2]-2*q*d[1]+q*q*d[0]) if np.isfinite(q) else float('nan')
    # If 6 values present, Hankel ratio also estimates q, independently.
    q6 = sqrt(h[1]/h[0]) if len(k) >= 6 and h[0]*h[1] > 0 else float('nan')
    ell6 = -step_m/log(q6) if 0 < q6 < 1 else float('nan')
    shape_res = float('nan')
    if 0 < q < 1:
        # Given q, recover u,v,A by K_n=A+(u+vn)q^n.
        n = np.arange(len(k), dtype=float)
        X = np.column_stack((np.ones(len(k)),q**n,n*q**n))
        A,u,v = np.linalg.lstsq(X,k,rcond=None)[0]
        if abs(v) > 0:
            # u/v must equal (1+r0/ell)/(step/ell) for genuine Yukawa.
            shape_res = float(u/v - (ell+r0)/step_m)
    return Spectrum(h, j0, q, ell, q6, ell6, rec, shape_res)


def fit_profile_gls(k_values: np.ndarray, heights_m: np.ndarray,
                    cov: np.ndarray | None = None,
                    bounds_m: tuple[float,float] = (30_000.,1_000_000.)) -> dict:
    """At each ell, analytically profile out A and C in K=A+C*force_shape.

    This is an *illustrative synthetic-data* generalized least squares fit.
    No true satellite observations are bundled or implied.
    """
    y=np.asarray(k_values, dtype=float)
    h=np.asarray(heights_m, dtype=float)
    if cov is None:
        W = np.eye(len(y))
    else:
        W = np.linalg.inv(np.asarray(cov, dtype=float))
    def profile(ell):
        f=relative_yukawa(h, ell)
        X=np.column_stack((np.ones_like(f),f))
        normal=X.T@W@X
        rhs=X.T@W@y
        coef=np.linalg.solve(normal,rhs)
        resid=y-X@coef
        chi=float(resid@W@resid)
        return chi,coef,resid
    opt=minimize_scalar(lambda ell: profile(ell)[0],bounds=bounds_m,method='bounded',
                        options={'xatol':1e-4})
    chi,coef,resid=profile(opt.x)
    return {'ell_m':float(opt.x),'A':float(coef[0]),'C':float(coef[1]),
            'epsilon_surface':float(coef[1]/coef[0]),'chi2':chi,
            'max_residual':float(np.max(np.abs(resid))), 'success':bool(opt.success)}


def near_circular_precession_rad(h_m: float, ell: float, epsilon_ground: float):
    r=R_EARTH+h_m
    e=epsilon_ground*relative_yukawa(h_m,ell)
    # r d epsilon/dr = -epsilon * (r/ell)^2/(1+r/ell).
    rd=-e*(r/ell)**2/(1+r/ell)
    if 1+e+rd <= 0:
        return float('nan')  # unstable radial epicyclic oscillations
    return 2*pi*(sqrt((1+e)/(1+e+rd))-1)


def extra_potential(h_m: float, ell: float, epsilon_ground: float,
                    mu: float=MU_EARTH_REF):
    r=R_EARTH+h_m
    e=epsilon_ground*relative_yukawa(h_m,ell)
    return -mu*e/(r*(1+r/ell))


def extra_clock_shift(h1_m: float, h2_m: float, ell: float, epsilon_ground: float):
    return (extra_potential(h2_m,ell,epsilon_ground)-
            extra_potential(h1_m,ell,epsilon_ground))/C_LIGHT**2


def fixed_hypothesis_gls(k_values: np.ndarray, heights_m: np.ndarray,
                         cov: np.ndarray,
                         ell: float = ELL_PRE_REGISTERED,
                         alpha: float = ALPHA_PRE_REGISTERED,
                         density_model: str = 'improved') -> dict:
    """Confirmatory 1-parameter fit (mu only), candidate versus null GR.

    Both hypotheses profile the SAME mu. alpha, ell and form factor are FIXED.
    Additional real orbit, attitude, geodesy and clock nuisance are NOT included.
    This is therefore only a surrogate for demonstration/testing.
    """
    y=np.asarray(k_values, dtype=float)
    h=np.asarray(heights_m, dtype=float)
    W=np.linalg.inv(np.asarray(cov,dtype=float))
    shape=1+ground_fraction(ell,alpha,density_model)*relative_yukawa(h,ell)
    def check(s):
        mu=float((s@W@y)/(s@W@s))
        resid=y-mu*s
        return {'mu_fit':mu,'chi2':float(resid@W@resid),
                'max_abs_residual':float(np.max(np.abs(resid)))}
    h1=check(shape); h0=check(np.ones_like(shape))
    return {'fixed_candidate':h1, 'newtonian_null':h0,
            'chi2_null_minus_fixed':h0['chi2']-h1['chi2'],
            'warning':'surrogate only; not a real satellite hypothesis test'}
