"""ROOT V126 -- vacuum modified Helmholtz mean-value checks.

Every numerical experiment is SYNTHETIC, not measured orbital data.
All lengths are metres. The trace of acceleration Jacobian is s^-2.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

EARTH_R=6_371_000.0
ELL=124_600.0


def sinhc(x):
    """sinh(x)/x with stable small-x series. Supports scalars/ndarrays."""
    x = np.asarray(x,dtype=float)
    out = np.empty_like(x)
    small=np.abs(x)<0.001
    z=x[small]**2
    out[small]=1+z/6+z*z/120+z*z*z/5040+z**4/362880
    out[~small]=np.sinh(x[~small])/x[~small]
    return float(out) if out.ndim==0 else out


def point_trace(points, sources, strengths, ell=ELL):
    """T=-laplacian(U_Y), where U_Y=-Σ C_j exp(-distance/ell)/distance.

    strengths C_j=G*alpha*M_j (m^3/s^2); may be ± for mathematical tests.
    Outputs acceleration Jacobian trace in s^-2, any source arrangement.
    """
    x=np.asarray(points,float)
    s=np.asarray(sources,float)
    c=np.asarray(strengths,float)
    if x.shape[-1]!=3 or s.ndim!=2 or s.shape[1]!=3 or c.shape!=(len(s),):
        raise ValueError('point/source shapes invalid')
    if not np.isfinite(ell) or ell<=0 or not np.all(np.isfinite(x)) or not np.all(np.isfinite(s)) or not np.all(np.isfinite(c)):
        raise ValueError('nonphysical or non-finite input')
    d=np.linalg.norm(x[...,None,:]-s,axis=-1)
    if np.any(d==0):
        raise ValueError('sample at a source singularity')
    return np.sum(c*np.exp(-d/ell)/(ell**2*d),axis=-1)


def mixed_point_trace(points, sources, strengths, ells):
    """Sum of different Helmholtz scales: intentionally violates single-k PDE."""
    src=np.asarray(sources,float); amp=np.asarray(strengths,float); ls=np.asarray(ells,float)
    if ls.shape!=(len(src),):
        raise ValueError('one length per source required')
    return sum(point_trace(points,src[j:j+1],amp[j:j+1],ls[j]) for j in range(len(src)))


def sphere_quadrature(n_theta=24,n_phi=48):
    """Fixed tensor-product Gauss-Legendre×trapezoid quadrature on S²."""
    u,w=leggauss(n_theta)
    phi=2*np.pi*np.arange(n_phi)/n_phi
    q=np.sqrt(1-u*u)
    dirs=np.stack([np.broadcast_to(q[:,None]*np.cos(phi)[None,:],(n_theta,n_phi)),
                   np.broadcast_to(q[:,None]*np.sin(phi)[None,:],(n_theta,n_phi)),
                   np.broadcast_to(u[:,None],(n_theta,n_phi))],axis=-1)
    weights=np.broadcast_to(w[:,None]/(2*n_phi),(n_theta,n_phi))
    return dirs.reshape(-1,3),weights.ravel()


def shell_average(trace_func, centre, radius, dirs=None, weights=None):
    if radius<0: raise ValueError('radius < 0')
    centre=np.asarray(centre,float)
    if centre.shape!=(3,):raise ValueError('centre must be (3,)')
    if dirs is None or weights is None: dirs,weights=sphere_quadrature()
    values=trace_func(centre+radius*dirs)
    return float(np.sum(np.asarray(values)*weights))


def shell_ratio_from_length(a,b,ell):
    if not 0<=a<b or ell<=0: raise ValueError('require 0<=a<b and ell>0')
    return float(sinhc(b/ell)/sinhc(a/ell))


def inverse_two_shells(a,b,m_a,m_b):
    """Uniquely recover ell from two noise-free positive shell means."""
    if not (0<=a<b and m_a*m_b>0): raise ValueError('bad geometry or trace signs')
    ratio=m_b/m_a
    if ratio<=1:raise ValueError('nondecaying or incompatible data')
    def f(x): return float(sinhc(x)/sinhc(x*a/b)-ratio)
    hi=1.0
    while f(hi)<0 and hi<200: hi*=2
    if hi>=200 and f(hi)<0: raise ValueError('ratio exceeds numerical bracket')
    return b/brentq(f,1e-10,hi,xtol=1e-13,rtol=1e-13)


def shell_contrast(a,b,c,m_a,m_b,m_c):
    """Differences cancel one common additive DC calibration offset."""
    if not 0<=a<b<c:raise ValueError('bad radii ordering')
    denom=m_b-m_a
    if denom==0:raise ValueError('no measured contrast')
    return (m_c-m_b)/denom


def contrast_from_length(a,b,c,ell):
    if not 0<=a<b<c or ell<=0:raise ValueError('bad radii/ell')
    return float((sinhc(c/ell)-sinhc(b/ell))/(sinhc(b/ell)-sinhc(a/ell)))


def inverse_three_shells(a,b,c,m_a,m_b,m_c):
    """Solve 3-shell common-offset invariant. Monotonic checked over scope.

    Throws when ratio is inconsistent with positive-k predictions.
    """
    obs=shell_contrast(a,b,c,m_a,m_b,m_c)
    k0=(c*c-b*b)/(b*b-a*a)
    if obs<=k0:raise ValueError('ratio requires zero or negative k')
    def f(x):
        scale=c/x
        return contrast_from_length(a,b,c,scale)-obs
    hi=1.0
    while f(hi)<0 and hi<80:hi*=2
    if f(hi)<0:raise ValueError('ratio out of inversion range')
    return c/brentq(f,0.0001,hi,xtol=1e-12,rtol=1e-12)


def weak_bump(r,a,p=4):
    r=np.asarray(r,float)
    if a<=0 or p<3:raise ValueError('bad bump')
    u=(r/a)**2
    w=np.maximum(1-u,0)
    return w**p


def weak_laplacian_bump(r,a,p=4):
    r=np.asarray(r,float)
    u=(r/a)**2
    w=np.maximum(1-u,0)
    return -6*p*w**(p-1)/a**2 + 4*p*(p-1)*r*r*w**(p-2)/a**4


def weak_k_squared(trace_func,centre,ball_radius,radial_count=42,theta=16,phi=32):
    """∫T Δψ /∫T ψ using a smooth compact support ψ=(1-r²/a²)^4_+.

    This uses measured T itself, never takes a numeric derivative of T.
    Requires full 3-D vacuum ball and instrument transfer accounted for.
    """
    rnodes,rweights=leggauss(radial_count)
    rad=(rnodes+1)*ball_radius/2
    w=rweights*ball_radius/2
    dirs,angweights=sphere_quadrature(theta,phi)
    m=np.array([shell_average(trace_func,centre,rr,dirs,angweights) for rr in rad])
    jac=4*np.pi*w*rad**2
    denominator=float(np.sum(jac*m*weak_bump(rad,ball_radius)))
    numerator=float(np.sum(jac*m*weak_laplacian_bump(rad,ball_radius)))
    if denominator==0:raise ValueError('no nonzero signal')
    return numerator/denominator


def candidate_earth_trace_at_altitude(h):
    """Reuse fixed V125 400 km amplitude and analytic radial falloff; synthetic."""
    radius=EARTH_R+np.asarray(h,dtype=float)
    rref=EARTH_R+400_000.0
    tref=17.473593e-9
    return tref*(rref/radius)*np.exp(-(radius-rref)/ELL)


def sim_multi_center_geometry():
    # Synthetic non-spherical source points all INSIDE R=6371 km.
    sources=np.array([[0,0,0],[6.25e6,0,0],[6.15e6,0.70e6,0.24e6],[-3.1e6,3.2e6,-2.7e6]],float)
    strengths=np.array([8e13,1e10,3e10,2e10],float)
    centre=np.array([EARTH_R+400_000.,80_000.,20_000.])
    return sources,strengths,centre
