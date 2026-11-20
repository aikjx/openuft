"""ROOT V114: auditable linear massive scalar--tensor phenomenology.

This module is NOT a new theory of gravity. It implements a restricted, weak-field,
constant-coupling, universal-matter-coupling Yukawa model. Gstar is the coefficient
of the tensor 1/r potential, not a directly measured Newton constant.

Distances and lengths: meters, a=alpha**2 dimensionless. A solar-system PPN
constant gamma cannot be inferred by substituting a single r into local_gamma.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.optimize import brentq

C = 299792458.0
HBAR = 1.054571817e-34
E_CHARGE = 1.602176634e-19
AU = 149597870700.0
GSTAR = 6.67430e-11  # sample only, not predicted
SUN_MASS = 1.9885e30

@dataclass(frozen=True)
class Model:
    a: float       # nonnegative scalar-force strength alpha_0^2
    lam: float     # scalar Compton length in metres
    def validate(self):
        if not math.isfinite(self.a) or self.a < 0:
            raise ValueError('a must be finite and >= 0')
        if not math.isfinite(self.lam) or self.lam <= 0:
            raise ValueError('lam must be finite and > 0')
        return self


def _x(r, model):
    model.validate()
    if not np.all(np.asarray(r, dtype=float) > 0):
        raise ValueError('r must be positive')
    return np.asarray(r, dtype=float) / model.lam


def gamma_local(r, model):
    """psi/U in isotropic linear metric; NOT a fitted finite-range PPN constant."""
    x = _x(r, model)
    z = model.a * np.exp(-x)
    return (1 - z) / (1 + z)


def potential_enhancement(r, model):
    return 1 + model.a * np.exp(-_x(r, model))


def force_enhancement(r, model):
    """G_force(r)/Gstar for test particle in this universal-coupling model."""
    x = _x(r, model)
    return 1 + model.a * (1 + x) * np.exp(-x)


def force_excess(r, model):
    x = _x(r, model)
    return model.a * (1 + x) * np.exp(-x)


def lensing_sum(r, tensor_GM):
    """U+psi for conformal scalar linear order, source normalization fixed."""
    if np.any(np.asarray(r) <= 0):
        raise ValueError('r must be positive')
    return 2 * tensor_GM / np.asarray(r)


def gamma_from_force_reference(r, model):
    """Toy Shapiro 'gamma' inferred if fitting 2 Gstar with G_force at r.
    NOT the genuine Cassini observable: real time-delay fits an entire light path.
    """
    return 2 / force_enhancement(r, model) - 1


def local_gamma_excess(gamma):
    if not (-1 < gamma <= 1):
        raise ValueError('expected -1 < gamma <= 1')
    return (1 - gamma) / (1 + gamma)


def infer_one_radius(r, gamma, force_ratio):
    """Recover a and lambda assuming known tensor GM and both independent channels.
    Returns (a,lam). Ill conditioned for weak signals or long/short scalar ranges.
    """
    if r <= 0: raise ValueError('r>0 required')
    z = local_gamma_excess(gamma)
    y = force_ratio - 1
    if z <= 0 or y <= z:
        raise ValueError('no identifiable positive-mass positive-coupling scalar')
    x = y / z - 1
    lam = r / x
    a = z * math.exp(x)
    return (a, lam)


def force_ratio_two_radii(r1, r2, model):
    if r2 <= r1 or r1 <= 0:
        raise ValueError('requires r2>r1>0')
    y1 = float(force_excess(r1,model));y2 = float(force_excess(r2,model))
    if y1 == 0: return float('nan')
    return y2/y1


def two_scale_ratio_from_m(r1, r2, m):
    """m = 1/lam in inverse length units; a cancels."""
    if not (r2 > r1 > 0 and m >= 0):
        raise ValueError('r2>r1>0, m>=0 needed')
    return (1+m*r2)/(1+m*r1)*math.exp(-m*(r2-r1))


def two_scale_logderivative(r1, r2, m):
    """d/dm log[R(m)], strictly negative when m>0 and r2>r1."""
    if not (r2>r1>0 and m>=0): raise ValueError('invalid radii or mass')
    return -(r2-r1)*m*(r1+r2+m*r1*r2)/((1+m*r1)*(1+m*r2))


def solve_two_scales(r1, r2, y1, y2):
    """Infer (a, lambda), assuming separately known tensor-GM normalization.
    Uses dimensionless x=r1/lambda for numerical stability.
    """
    if not (r2>r1>0 and y1>y2>0):
        raise ValueError('need r2>r1>0 and y1>y2>0')
    R = y2/y1
    rho=r2/r1
    def ratio(x):
        return (1+rho*x)/(1+x)*math.exp(-x*(rho-1))
    hi=1.0
    while ratio(hi)>R: hi*=2
    x=brentq(lambda t: ratio(t)-R,1e-13,hi,xtol=1e-14)
    lam=r1/x
    a=y1*math.exp(x)/(1+x)
    return (a,lam)


def joint_jacobian(r, model):
    """Jacobian of (gamma_local, force_excess) w.r.t. (a, ln lambda)."""
    x=float(_x(r,model)); e=math.exp(-x); z=model.a*e
    return np.array([[-2*e/(1+z)**2, -2*z*x/(1+z)**2],
                     [(1+x)*e,         model.a*x*x*e]])


def joint_det_closed_form(r, model):
    x=float(_x(r, model));e=math.exp(-x);z=model.a*e
    return 2*model.a*x*e**2/(1+z)**2


def scalar_energy_eV(lam):
    if lam<=0:raise ValueError('lambda must be positive')
    return HBAR*C/(lam*E_CHARGE)


def scalar_frequency_threshold_Hz(lam):
    if lam<=0:raise ValueError('lambda must be positive')
    return C/(2*math.pi*lam)


def scalar_group_velocity_fraction(f, lam):
    """Free massive scalar dispersion. Real propagating mode only f>fthreshold."""
    f0=scalar_frequency_threshold_Hz(lam)
    if f<=f0:return 0.0
    return math.sqrt(1-(f0/f)**2)


def shapiro_bare_delay_oneway(M, b, L, Gstar=GSTAR):
    """Straight unperturbed line of sight z in [-L,L], 1PN leading Shapiro delay.
    Assumes the two potential coefficient terms cancel in U+psi.
    This is NOT a fit to Cassini ephemeris and does not calibrate source mass.
    """
    if min(M,b,L,Gstar)<=0:raise ValueError('positive inputs required')
    return 4*Gstar*M/C**3*math.asinh(L/b)


def synthetic_noise_demo(model, r, sigma_gamma=0.001, sigma_force=0.001,
                         n=1000, seed=20261120):
    """Toy Gaussian measurement noise, not actual experimental errors or bounds."""
    rg=np.random.default_rng(seed)
    gam=float(gamma_local(r,model)); force=float(force_enhancement(r,model))
    recovered=[]
    for gg,ff in zip(rg.normal(gam,sigma_gamma,n), rg.normal(force,sigma_force,n)):
        try:
            a,lam=infer_one_radius(r,float(gg),float(ff))
            if a>0 and math.isfinite(a) and lam>0 and math.isfinite(lam):
                recovered.append((a,lam))
        except (ValueError, OverflowError):pass
    arr=np.asarray(recovered, dtype=float)
    return { 'n_requested':int(n),'n_identifiable':len(arr),
             'a_quantiles':list(np.quantile(arr[:,0],[.05,.5,.95])),
             'lam_AU_quantiles':list(np.quantile(arr[:,1]/AU,[.05,.5,.95]))}
