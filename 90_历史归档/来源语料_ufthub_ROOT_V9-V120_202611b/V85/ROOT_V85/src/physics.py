"""ROOT V85: reproducible model diagnostics. All astrophysical/body parameters are inputs.
NOT a theory determining Newton's constant or a report of observed new forces.
"""
from __future__ import annotations
import math

G_REF = 6.67430e-11  # CODATA 2022, measured, m^3 kg^-1 s^-2
G_STD = 1.5e-15
C = 299_792_458.0
H = 6.62607015e-34
HBAR = H/(2*math.pi)


def newton_acceleration(mu: float, r: float) -> float:
    if mu <= 0 or r <= 0: raise ValueError('mu and r must be positive')
    return mu / r**2


def compactness(mu: float, r: float) -> float:
    return mu / (r * C*C)


def kretschmann(mu: float, r: float) -> float:
    """Exterior Schwarzschild only; not for rotating/extended magnetized bodies."""
    return 48*(mu/(C*C))**2/r**6


def z_from_G(G=G_REF) -> float:
    return 0.5 * G*C


def alpha_grav(m: float, G=G_REF) -> float:
    return G*m*m/(HBAR*C)


def radial_shape_newton() -> float:
    return 1.0


def yukawa_point_factor(r: float, length: float) -> float:
    if r <= 0 or length <= 0: raise ValueError('positive distance and range required')
    x = r/length
    if x >= 750.0: return 0.0
    return (1+x)*math.exp(-x)


def point_yukawa_acceleration(mu: float, r: float, alpha: float, length: float,
                              q_source=1.0, q_test=1.0, universal=0.0) -> float:
    """Phenomenological model, linear source charge, not a measured fifth force."""
    if not math.isfinite(alpha) or not math.isfinite(universal): raise ValueError('nonfinite coupling')
    return newton_acceleration(mu,r)*(1.0+universal+
        alpha*q_source*q_test*yukawa_point_factor(r,length))


def radial_shape_point(r: float, alpha: float, length: float,
                       q_source=1.0, q_test=1.0, universal=0.0) -> float:
    """Q=-r g'(r)/(2g(r)), assuming universal=constant with r.
    For g_N*(1+u+A(1+x)e^-x)."""
    if r <= 0 or length <= 0 or not math.isfinite(alpha) or not math.isfinite(universal):
        raise ValueError("positive distance/range and finite couplings required")
    x=r/length
    A=alpha*q_source*q_test
    if x >= 750.0: return 1.0
    e=math.exp(-x)
    denominator=1.0+universal+A*(1+x)*e
    if abs(denominator)<1.e-14: raise ValueError('g nearly zero; shape undefined')
    return 1 + A*x*x*e/(2*denominator)


def finite_envelope(radius:float, r:float, length:float)->float:
    """F(R/lambda)*exp(-r/lambda), uniform source sphere, r>=R.
    Numerically stable at large R/lambda, no cosh overflow.
    """
    if radius < 0 or r <= 0 or length <= 0 or r < radius:
        raise ValueError('require 0<=radius<=r and positive r and length')
    x=radius/length
    if x < 0.2:
        f=(1+x*x/10+x**4/280+x**6/15120+x**8/1330560)
        return f*math.exp(-r/length)
    return 3/(2*x**3)*((x-1)*math.exp(-(r-radius)/length)
                      +(x+1)*math.exp(-(r+radius)/length))


def sphere_acceleration(mu:float,r:float,radius:float,alpha:float,length:float,
                        q_source=1.0,q_test=1.0,universal=0.0)->float:
    if r < radius: raise ValueError('external solution only')
    f=finite_envelope(radius,r,length)
    return newton_acceleration(mu,r)*(
        1+universal+alpha*q_source*q_test*(1+r/length)*f)


def normalized_material_difference(q_source: float, q_i: float, q_j:float,
                                   alpha:float,r:float,length:float, radius:float=0.) -> float:
    """(a_i-a_j)/a_N for one source; exact linear factorization in this ansatz.
    Universal source factor cancels but not necessarily experimental systematics.
    """
    if radius:
        shape=finite_envelope(radius,r,length)*(1+r/length)
    else:
        shape=yukawa_point_factor(r,length)
    return alpha*q_source*(q_i-q_j)*shape


def eotvos(q_source:float,q_i:float,q_j:float,alpha:float,r:float,length:float,
           universal:float=0.0)->float:
    si=1+universal+alpha*q_source*q_i*yukawa_point_factor(r,length)
    sj=1+universal+alpha*q_source*q_j*yukawa_point_factor(r,length)
    if abs(si+sj) < 1e-14: raise ValueError('zero denominator')
    return 2*(si-sj)/(si+sj)


def matrix_rank_one_invariant(d11,d12,d21,d22)->float:
    """Exact 2x2 determinant: zero for one factorized mediator."""
    return d11*d22 - d12*d21


def circular_orbit_mu(r:float,period:float)->float:
    """Newtonian two body circular orbit relative motion; no independent G determination."""
    if r<=0 or period<=0: raise ValueError('positive orbital parameters')
    return 4*math.pi**2*r**3/period**2


def two_sensor_common(mu:float,d:float,s:float)->float:
    if d<=s or s<=0: raise ValueError('outside sensor geometry')
    return mu/2*((d-s)**-2+(d+s)**-2)


def two_sensor_gradient(mu:float,d:float,s:float)->float:
    if d<=s or s<=0: raise ValueError('outside sensor geometry')
    return mu/(2*s)*((d-s)**-2-(d+s)**-2)


def conservative_95_eta_bound(central=-1.5e-15,stat=2.3e-15,syst=1.5e-15):
    """Illustrative |central|+1.96*sqrt(stat^2+syst^2), assumes independent Gaussian uncertainties;
    NOT a collaboration published 95% frequentist confidence limit.
    """
    return abs(central)+1.96*math.hypot(stat,syst)
