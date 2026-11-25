"""ROOT V136: mathematical null tests, Earth/Moon cross-altitude Yukawa diagnostics.

MODEL_PREDICTION_NOT_OBSERVATION. No genuine gravity observations ingested.
All numerical gravitational inputs are SI; field theory uses c=1, hbar and G distinct.
"""
from __future__ import annotations
import math
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE/'legacy'/'ROOT_V135_Unified_Field_Research'/'src'))
import physics as old


def eps_at(r, layers, alpha=old.ROOT_ALPHA, lam=old.ROOT_LAMBDA):
    return old.yukawa_accel_ratio(r,layers,alpha,lam)


def relative_force_deviation(r1,r2,layers,alpha=old.ROOT_ALPHA,lam=old.ROOT_LAMBDA):
    """A(r1)/A(r2)-1 where A=r^2 |g|; exact in spherical Newton+Yukawa.
    Cancels bare mu exactly, but a realistic observational comparison must account
    for J2, tides, non-gravity accelerations, trajectory covariance and GM-fit.
    """
    e1=eps_at(r1,layers,alpha,lam)
    e2=eps_at(r2,layers,alpha,lam)
    return (e1-e2)/(1+e2)


def yukawa_decay_shape(r1,r2,lam):
    """eps(r2)/eps(r1): independent of alpha, density, GM for exterior spherical source."""
    if lam<=0 or r2<r1 or r1<=0: raise ValueError('positive lam and 0<r1<=r2')
    return math.exp(-(r2-r1)/lam)*(1+r2/lam)/(1+r1/lam)


def weighted_radial_force(r,mu,layers,alpha=old.ROOT_ALPHA,lam=old.ROOT_LAMBDA):
    """Observable proxy A=r^2 g (units m^3/s^2), spherical candidate only."""
    if mu<=0:raise ValueError('positive mu')
    return mu*(1+eps_at(r,layers,alpha,lam))


def three_altitude_shape_ratio(r0,r1,r2,layers,alpha=old.ROOT_ALPHA,lam=old.ROOT_LAMBDA):
    """[A(r0)-A(r1)]/[A(r1)-A(r2)]; alpha, GM, source radial density cancel.
    Requires 0<r0<r1<r2 exterior and alpha != 0. For tiny alpha use
    exact analytical shapes instead of cancellation of nearly equal numbers.
    """
    R=old.check_shells(layers)
    if not (R<=r0<r1<r2): raise ValueError('exterior ordered radii')
    if alpha==0: raise ValueError('zero signal: undefined 0/0')
    h0=(1+r0/lam)
    h1=(1+r1/lam)*math.exp(-(r1-r0)/lam)
    h2=(1+r2/lam)*math.exp(-(r2-r0)/lam)
    if h1==h2: raise ValueError('degenerate sampling')
    return (h0-h1)/(h1-h2)


def eps_radial_derivative(r,layers,alpha=old.ROOT_ALPHA,lam=old.ROOT_LAMBDA):
    """d epsilon/dr for exterior finite sphere with universal Yukawa coupling."""
    e=eps_at(r,layers,alpha,lam)
    return -e*r/(lam*(r+lam))


def epicycle_from_eps_gradient(r,mu,layers,alpha=old.ROOT_ALPHA,lam=old.ROOT_LAMBDA):
    e=eps_at(r,layers,alpha,lam)
    oe=mu/r**3*(1+e)
    kr=mu/r**3*(1+e+r*eps_radial_derivative(r,layers,alpha,lam))
    if kr<=0 or oe<=0: return {'stable':False, 'omega2':oe,'kappa2':kr,'precession':None}
    return {'stable':True,'omega2':oe,'kappa2':kr,
            'precession':2*math.pi*(math.sqrt(oe/kr)-1)}


def helix_geometry(a,omega,u):
    """Simple flat-space null-speed parameterized spiral, coordinate time t (c=1)."""
    if a<=0 or omega<=0:raise ValueError('a,omega positive')
    v2=(a*omega)**2+u*u
    kappa=a*omega**2/v2
    torsion=u*omega/v2
    return {'speed2':v2,'curvature':kappa,'torsion':torsion,
            'acceleration_magnitude':a*omega**2,
            'frequency_norm':math.sqrt(kappa*kappa+torsion*torsion)}


def free_pitch_for_ratio(tau_over_kappa,omega):
    """Prove arbitrary positive torsion/curvature ratio can be fit at c=1.
    Choose u=t/sqrt(1+t^2), a=1/[omega sqrt(1+t^2)]; tau/kappa=t.
    So geometry alone cannot predict a unique fine-structure constant.
    """
    if tau_over_kappa<=0 or omega<=0:raise ValueError('positive')
    x=tau_over_kappa
    u=x/math.sqrt(1+x*x)
    a=1/(omega*math.sqrt(1+x*x))
    return a,omega,u


def dot3(a,b):return sum(x*y for x,y in zip(a,b))


def cross3(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def lorentz_boost_fields(E,B,beta):
    """Heaviside-Lorentz c=1, boost vector beta, fields in same units.
    E' = gamma(E+beta x B)-gamma^2/(gamma+1)*beta(beta.E)
    B' = gamma(B-beta x E)-gamma^2/(gamma+1)*beta(beta.B)
    """
    b2=dot3(beta,beta)
    if b2>=1:raise ValueError('subluminal boost required')
    g=1/math.sqrt(1-b2)
    f=g*g/(g+1)
    vxB=cross3(beta,B);vxE=cross3(beta,E)
    return (tuple(g*(E[i]+vxB[i])-f*beta[i]*dot3(beta,E) for i in range(3)),
            tuple(g*(B[i]-vxE[i])-f*beta[i]*dot3(beta,B) for i in range(3)))


def em_invariants(E,B):
    """Lorentz invariant scalars I1=B^2-E^2, I2=E.B, in c=1 HL units."""
    return (dot3(B,B)-dot3(E,E),dot3(E,B))


def gauss_flux_newton(r,mu):
    """Magnitude of Gauss flux integral for a point-source Newtonian field."""
    if r<=0:raise ValueError('positive')
    return 4*math.pi*r*r*(mu/r**2)
