"""ROOT V71: finite-source Yukawa, helical kinematics, gravity reference, RG running.
SI unless explicitly identified as high-energy natural units. No discovery claims.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import cos, sin, pi, sqrt, exp, log, sinh
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

G = 6.67430e-11      # CODATA 2022 central value, INPUT not prediction
C = 299792458.0
HBAR = 1.054571817e-34
EARTH_MU = 3.986004418e14
EARTH_R = 6378137.0
EARTH_OMEGA = 7.292115e-5

@dataclass(frozen=True)
class Shell:
    outer: float
    rho: float
    q: float = 1.0  # hypothetical charge-per-mass ratio, arbitrary; NOT measured material data


def _validate_shells(shells):
    if not shells: raise ValueError('shells empty')
    prev=0.
    for s in shells:
        if not np.isfinite(s.outer) or s.outer <= prev or not np.isfinite(s.rho) or s.rho<0 or not np.isfinite(s.q):
            raise ValueError('invalid shell geometry/density/charge')
        prev=s.outer
    return prev


def mass_shells(shells):
    _validate_shells(shells)
    inner=0.
    total=0.
    for s in shells:
        total+=4*pi/3*s.rho*(s.outer**3-inner**3)
        inner=s.outer
    if total<=0: raise ValueError('source mass must be positive')
    return total


def uniform_sphere_form_factor(x:float)->float:
    """F(x)=3(x cosh x - sinh x)/x^3, x>=0; may overflow for x > 700.
    Prefer stable_surface_form for large x. This function is for moderate x.
    """
    if x<0: raise ValueError('x must be nonnegative')
    if x<.15:
        return 1+x*x/10+x**4/280+x**6/15120+x**8/1330560
    if x>600: raise OverflowError('Use stable_surface_form for large x')
    return 3*(x*np.cosh(x)-np.sinh(x))/x**3


def stable_surface_form(x:float)->float:
    """e^-x F(x); robust for x>=0 including macroscopic Earth with lambda << R."""
    if x<0 or not np.isfinite(x):raise ValueError('invalid x')
    if x<.1:
        return exp(-x)*uniform_sphere_form_factor(x)
    return (1.5/x**3)*((x-1)+(x+1)*exp(-2*x))


def uniform_ratio(R:float, h:float, lam:float, alpha:float=1.0, qsrc:float=1., qtest:float=1.) -> float:
    """Outside source: delta g / g_Newton for a point test body and uniform spherical source."""
    if R<=0 or h<0 or lam<=0:raise ValueError('invalid geometry or lambda')
    x=R/lam
    return alpha*qsrc*qtest*stable_surface_form(x)*(1+(R+h)/lam)*exp(-h/lam)


def point_ratio(R:float, h:float, lam:float, alpha:float=1.) -> float:
    """Incorrect for finite sized sources when lambda is small; comparison ONLY."""
    if R<=0 or h<0 or lam<=0:raise ValueError('invalid geometry')
    r=R+h
    return alpha*(1+r/lam)*exp(-r/lam)


def _shifted_kernel(s:float,R:float,lam:float)->float:
    """e^-R/lam * sinh(s/lam)/(s/lam), for 0<=s<=R, stable at s=0."""
    if s==0:return exp(-R/lam)
    return lam/(2*s)*(exp(-(R-s)/lam)-exp(-(R+s)/lam))


def layered_surface_form(shells, lam:float, rtol:float=1e-11)->float:
    """Mass-normalized shifted form factor Q=e^-R/lam <q sinh(s/lam)/(s/lam)>_mass.
    Source q may vary radially; no empirical charge assignments implied.
    Numerical integration in dimensionless u=s/R for stable cross-scales.
    """
    R=_validate_shells(shells)
    if lam<=0:raise ValueError('invalid lambda')
    M=mass_shells(shells)
    inner=0.
    accum=0.
    # piecewise integrate in u; avoid hasty absolute tolerance when function very small
    for sh in shells:
        if sh.rho==0 or sh.q==0:
            inner=sh.outer;continue
        a,b=inner/R,sh.outer/R
        def fn(u):
            s=R*u
            return u*u*_shifted_kernel(s,R,lam)
        if R/lam>15:
            # Exact antiderivative with exponents <= 0 avoids overflow and
            # resolves thin surface layers even when lambda/R is tiny.
            xb=sh.outer/lam; xa=inner/lam
            def primitive(x):
                return .5*((x-1)*exp(-(R/lam-x))+(x+1)*exp(-(R/lam+x)))
            integral_phys=lam**3*(primitive(xb)-primitive(xa))
            accum += 4*pi*sh.rho*sh.q*integral_phys
        else:
            integral,_=quad(fn,a,b,epsabs=1e-15,epsrel=rtol,limit=300)
            accum += 4*pi*sh.rho*sh.q*R**3*integral
        inner=sh.outer
    return float(accum/M)


def layered_ratio(shells,h:float,lam:float,alpha:float=1.,qtest:float=1.)->float:
    if h<0 or lam<=0:raise ValueError('invalid')
    R=_validate_shells(shells)
    return alpha*qtest*layered_surface_form(shells,lam)*(1+(R+h)/lam)*exp(-h/lam)


def homogeneous_shells(R:float, rho:float=1., q:float=1.):
    return [Shell(R,rho,q)]


def same_mass_layered_shells(R:float,rho:float=1.,qcore:float=1.,qshell:float=1.):
    """Core R/2 with 1.5 rho, outer shell 13/14 rho: same total M as uniform rho."""
    return [Shell(R/2,1.5*rho,qcore),Shell(R,(13/14)*rho,qshell)]


def central_gravity(mu:float,r:float)->float:
    if mu<=0 or r<=0:raise ValueError('invalid')
    return mu/r**2


def redshift_height(mu:float,R:float,h:float)->float:
    """Weak field static potential difference, stable for h << R."""
    if mu<=0 or R<=0 or h<0:raise ValueError('invalid')
    return mu*h/(C*C*R*(R+h))


def tidal_radial(mu:float,r:float)->float:
    return 2*mu/r**3


def helical_kinematics(R:float,omega:float,u:float):
    if R<=0 or omega==0:raise ValueError('R>0, omega nonzero')
    s=sqrt((R*omega)**2+u*u)
    return {'speed':s,'kappa':R*omega**2/s**2,'torsion':u*omega/s**2,'acceleration':R*omega**2,
            'dot_v_a':0.0}


def dimensions_G_from_c_hbar():
    """Solve three dimension equations: c^a hbar^b has target dimensions of G."""
    A=np.array([[1,2],[0,1],[-1,-1]],float)   # L, M, T
    target=np.array([3.,-1.,-2.])
    exponents,_,rank,_=np.linalg.lstsq(A,target,rcond=None)
    return exponents,float(np.linalg.norm(A@exponents-target)),int(rank)


def anomaly_sums():
    F=Fraction
    Ys=[(6,F(1,6)),(3,F(-2,3)),(3,F(1,3)),(2,F(-1,2)),(1,F(1,1))]
    return {'U1_cubed':sum((mult*y**3 for mult,y in Ys),F(0)),
            'grav_U1':sum((mult*y for mult,y in Ys),F(0)),
            'SU2_SU2_U1':3*F(1,6)+F(-1,2),
            'SU3_SU3_U1':2*F(1,6)+F(-2,3)+F(1,3),
            'SU2_doublets':4}

MZ=91.1876
BETAS=np.array([41/10,-19/6,-7.],float)


def gauge_inverse_alphas(q_GeV:float, alpha_em_inv=127.95,sin2w=.23122,alpha_s=.118):
    """One-loop MSbar-like demonstration inputs; thresholds/higher loops NOT included."""
    if q_GeV<=0 or not 0<sin2w<1 or alpha_em_inv<=0 or alpha_s<=0:
        raise ValueError('invalid coupling inputs')
    alpha_em=1/alpha_em_inv
    # g1^2=(5/3) gY^2, alpha1 = (5/3) alpha_em/cos^2 theta
    initial=np.array([(3/5)*(1-sin2w)/alpha_em,sin2w/alpha_em,1/alpha_s])
    return initial-BETAS/(2*pi)*log(q_GeV/MZ)


def gauge_pair_crossings():
    initial=gauge_inverse_alphas(MZ)
    out={}
    for i,j in ((0,1),(0,2),(1,2)):
        ln_q=2*pi*(initial[i]-initial[j])/(BETAS[i]-BETAS[j])
        out[f'{i+1}_{j+1}']=MZ*exp(ln_q)
    return out


def gauge_best_fit():
    def score(logq):
        arr=gauge_inverse_alphas(exp(logq))
        return float(np.sum((arr-arr.mean())**2))
    ans=minimize_scalar(score,bounds=(log(1e8),log(1e20)),method='bounded',options={'xatol':1e-12})
    arr=gauge_inverse_alphas(exp(ans.x))
    return {'q':exp(ans.x),'inverse_alphas':arr.tolist(),'spread':float(max(arr)-min(arr)),
            'rms':float(np.sqrt(np.mean((arr-arr.mean())**2)))}


def eotvos(a:float,b:float):
    if a+b==0:raise ValueError('a+b zero')
    return 2*(a-b)/(a+b)


def micro_WEP_bound_eta(delta_q:float,qsrc:float,R:float,h:float,lam:float,eta_upper:float=6e-15):
    """Illustrative alpha bound from |eta|<eta_upper, weak coupling; assumes charges known.
    NOT a published bound, and source qsrc here is hypothetical.
    """
    f=abs(delta_q*qsrc*uniform_ratio(R,h,lam))
    if f==0: return np.inf
    return eta_upper/f
