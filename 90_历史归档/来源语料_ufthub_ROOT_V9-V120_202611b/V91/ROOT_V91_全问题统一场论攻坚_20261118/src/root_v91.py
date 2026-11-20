"""ROOT V91 independent, reproducible toy-model/diagnostic calculations.
All quantities SI except explicitly dimensionless; not a full theory of quantum gravity.
No claim of a new physical force or four-force unification.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, sin, sinh, pi, sqrt, fsum, isfinite
from typing import Iterable
import numpy as np

G = 6.67430e-11
C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2*pi)
EPS0 = 8.8541878128e-12
KE = 1/(4*pi*EPS0)
E = 1.602176634e-19
CODATA2022_ALPHA_INV = 137.035999177

@dataclass(frozen=True)
class Geometry:
    d: float
    a: float
    b: float
    def __post_init__(self):
        if not all(isfinite(x) for x in (self.d,self.a,self.b)):
            raise ValueError('geometry must be finite')
        if self.d <= 0 or self.a < 0 or self.b < 0 or self.d <= (self.a+self.b)/2:
            raise ValueError('require d > (a+b)/2, a,b>=0')
    def radii(self):
        d,a,b = self.d,self.a,self.b
        return (d+(a-b)/2,d+(a+b)/2,d-(a+b)/2,d+(b-a)/2)
    @property
    def delta(self): return self.d-(self.a+self.b)/2

SIGNS=(1,-1,-1,1)
def newton_kernel(g: Geometry) -> float:
    return fsum(s/r for s,r in zip(SIGNS,g.radii()))

def yukawa_kernel_naive(g: Geometry, lam:float) -> float:
    if not isfinite(lam) or lam<=0: raise ValueError('lambda positive and finite')
    return fsum(s*exp(-r/lam)/r for s,r in zip(SIGNS,g.radii()))

def _sinhc(x:float)->float:
    if abs(x)<1e-4:
        z=x*x
        return 1+z/6+z*z/120+z*z*z/5040
    return sinh(x)/x

def gaussian_nodes(n=64):
    x,w=np.polynomial.legendre.leggauss(n)
    return (x+1)/2,w/2

def yukawa_delta_integral(g:Geometry,lam:float,n:int=64)->float:
    """Stable exact (to quadrature error) F_Y-F_N, for lambda not extremely short.
    mu=1/lam; D=ab mu^3 ∫_0^1 u^2 exp(-mu*d*u) sinhc(mu*a*u/2) sinhc(mu*b*u/2)du.
    This avoids cancellation even when lambda is enormous.
    """
    if not isfinite(lam) or lam<=0: raise ValueError('lambda positive and finite')
    if g.a==0 or g.b==0: return 0.0
    mu=1/lam
    if mu*max(g.radii())>200:  # asymptotically F_Y ~ 0; exact with negligible abs error
        return yukawa_kernel_naive(g,lam)-newton_kernel(g)
    nodes,weights=gaussian_nodes(n)
    integral=fsum(float(w)*float(u*u)*exp(-mu*g.d*float(u))*_sinhc(mu*g.a*float(u)/2)*_sinhc(mu*g.b*float(u)/2)
                  for u,w in zip(nodes,weights))
    return g.a*g.b*mu**3*integral

def yukawa_kernel(g:Geometry,lam:float)->float:
    mu=1/lam if lam>0 else float('inf')
    if mu*max(g.radii())>5: return yukawa_kernel_naive(g,lam)
    return newton_kernel(g)+yukawa_delta_integral(g,lam)

def derivative_mu(g:Geometry,mu:float)->float:
    """d/dmu F_Y = 4 e^-mu*d sinh(mu*a/2)sinh(mu*b/2), with stable low-mu expression."""
    if not isfinite(mu) or mu<0: raise ValueError('mu nonnegative and finite')
    if mu==0 or g.a==0 or g.b==0: return 0.0
    # stable even when mu*a enormous, by writing differences of exponentials
    if mu*(g.a+g.b)>800:
        rs=g.radii()
        return -fsum(s*exp(-mu*r) for s,r in zip(SIGNS,rs))
    return g.a*g.b*mu**2*exp(-mu*g.d)*_sinhc(mu*g.a/2)*_sinhc(mu*g.b/2)

def integral_t2_exponential(mu:float, length:float,n:int=64)->float:
    """∫_0^mu t²exp(-length*t)dt via stable fixed-interval quadrature."""
    if mu<0 or length<=0: raise ValueError('mu>=0 and length>0')
    if mu==0:return 0.0
    # for mu*length huge, saturated expression is accurate
    if mu*length>100:
        return 2/length**3
    nodes,weights=gaussian_nodes(n)
    return mu**3*fsum(float(w)*float(u*u)*exp(-mu*length*float(u)) for u,w in zip(nodes,weights))

def rigorous_delta_bounds(g:Geometry,lam:float)->tuple[float,float]:
    """Lower and upper rigorous (analytic) bounds based on sinh inequalities;
    numerical integral evaluates exact bounding integrals via positive quadrature.
    """
    if lam<=0:raise ValueError('lambda positive')
    mu=1/lam
    return (g.a*g.b*integral_t2_exponential(mu,g.d),
            g.a*g.b*min(integral_t2_exponential(mu,g.delta),mu**3/3))

def phase_benchmark(g:Geometry, m_a=1e-14,m_b=1e-14,t=1.):
    return G*m_a*m_b*t/HBAR*newton_kernel(g)

def candidate_scalar_alpha(beta_a:float,beta_b:float)->float:
    """Einstein-frame universal/coupled scalar: alpha_AB=2 beta_A beta_B, c=hbar=1."""
    return 2*beta_a*beta_b

def scalar_force_relative(alpha:float,r:float,lam:float)->float:
    """F/F_Newton under attractive Yukawa scalar in weak static point-source model."""
    if r<=0 or lam<=0:raise ValueError('positive radii and lambda')
    return 1+alpha*(1+r/lam)*exp(-r/lam)

def stable_signal(g:Geometry,lam:float,alpha:float=1.,mass:float=1e-14,time:float=1.):
    return alpha*G*mass**2*time/HBAR*yukawa_delta_integral(g,lam)

def design_matrix(ds:Iterable[float],a:float,b:float,lam:float):
    gs=[Geometry(float(d),a,b) for d in ds]
    fn=np.array([newton_kernel(g) for g in gs])
    # build explicitly h=f+delta; very large lambda can be ill-conditioned even mathematically
    z=np.array([yukawa_delta_integral(g,lam) for g in gs])
    return np.column_stack((fn,fn+z))

def stable_shape_separation(ds,a,b,lam):
    """Return fractional separation without constructing ill-conditioned [f,f+delta]."""
    gs=[Geometry(float(d),a,b) for d in ds]
    f=np.array([newton_kernel(g) for g in gs])
    delta=np.array([yukawa_delta_integral(g,lam) for g in gs])
    orth=delta-f*(float(f@delta)/float(f@f))
    return float(np.linalg.norm(orth)/np.linalg.norm(f)), float(np.linalg.norm(delta)),float(np.linalg.norm(orth))

def nuisance_marginalized_fisher(signal:np.ndarray,nuisance:np.ndarray,cov:np.ndarray):
    """Fisher information for signal amplitude after marginalizing linear nuisances.
    If signal lies exactly in the nuisance span, result = 0 up to machine rounding.
    """
    sig=np.asarray(signal,float).reshape(-1)
    B=np.asarray(nuisance,float)
    S=np.asarray(cov,float)
    if B.ndim!=2 or B.shape[0]!=len(sig) or S.shape!=(len(sig),len(sig)):
        raise ValueError('dimension mismatch')
    L=np.linalg.cholesky(S)
    sw=np.linalg.solve(L,sig)
    bw=np.linalg.solve(L,B)
    if bw.shape[1]>0:
        coeff=np.linalg.lstsq(bw,sw,rcond=None)[0]
        res=sw-bw@coeff
    else:res=sw
    return max(0.,float(res@res))

def sign_flip_design(f:Iterable[float]):
    """columns: gravity g, charge-odd e, charge-even nuisance b (same 1/r kernel)."""
    f=np.asarray(list(f),float)
    rows=[]
    for sign in (+1,-1):
        rows.extend([[x,sign*x,x] for x in f])
    return np.asarray(rows,float)

def condition_after_external_even_calibration(f:Iterable[float],sigma:float=1.):
    """Independent measurement of even nuisance adds row [0,0,1] => full rank."""
    X=sign_flip_design(f)
    return np.vstack([X,np.array([[0.,0.,1.]])])

def legacy_audit():
    alpha_candidate = float(4*pi**3+pi**2+pi)
    alpha_ref = CODATA2022_ALPHA_INV
    return {
        'G_2Z_over_c':'identity_if_Z_defined_as_Gc_over_2',
        'G_c2r_over_m':'identity_if_r_defined_as_Gm_over_c2',
        'velocity_condition':'(R*omega)^2+p^2=c^2_for_real_3d_speed',
        'alpha_inverse_candidate':alpha_candidate,
        'alpha_inverse_CODATA_2022':alpha_ref,
        'alpha_difference':alpha_candidate-alpha_ref,
        'alpha_difference_ppm':(alpha_candidate-alpha_ref)/alpha_ref*1e6,
        'mass_ratio_candidate_56pi':56*pi,
        'schwarzschild_ISCO_GM_over_c2':6,
        'historical_claim_ISCO_GM_over_c2':1,
        'strong_frequency_large_R_power':-0.5,
        'newton_orbit_frequency_large_R_power':-1.5,
        'Z_plus_iZprime':'dimensionally_invalid_if_no_conversion_or_normalization'
    }

def polynomial_nuisance_projection(ds,a,b,lam,degree=-1,include_newton=True):
    """Project Yukawa-Newton shape on nuisance space in Euclidean whitened geometry.
    degree=-1 means no polynomial offsets, 0 means unknown constant, 1 means
    unknown constant+linear drift with distance. For correlated noise use
    nuisance_marginalized_fisher instead. Numerical cancellation may occur at extreme lambda.
    """
    ds=np.asarray(list(ds),dtype=float)
    if len(ds)<=degree+1 or (include_newton and len(ds)<=degree+2):
        raise ValueError('too few distances for nuisance design')
    gs=[Geometry(float(d),a,b) for d in ds]
    shape=np.array([yukawa_delta_integral(g,lam) for g in gs])
    cols=[]
    if include_newton: cols.append(np.array([newton_kernel(g) for g in gs]))
    z=(ds-np.mean(ds))/np.ptp(ds)
    for k in range(degree+1):cols.append(z**k)
    if cols:
        B=np.stack(cols,axis=1)
        # scale columns to avoid inverse-square kernel vs constant mixed units
        B=B/np.linalg.norm(B,axis=0)
        proj=B@np.linalg.lstsq(B,shape,rcond=None)[0]
        return float(np.linalg.norm(shape-proj)),float(np.linalg.norm(shape))
    return float(np.linalg.norm(shape)),float(np.linalg.norm(shape))
