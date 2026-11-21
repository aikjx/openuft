"""ROOT V122: reproducible physics *hypothesis* testing, not detection or unification.

Scope: static, spherical, weak-field, Newtonian satellite orbits and the
linearized unscreened metric f(R)=R+aR^2 scalaron. Synthetic examples only.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.integrate import quad, solve_ivp
from rootv120 import (R_EARTH, ELL_PRE_REGISTERED, MU_EARTH_REF, C_LIGHT,
                       HBAR, E_CHARGE, ground_fraction, relative_yukawa,
                       extra_potential, extra_clock_shift, near_circular_precession_rad,
                       apparent_gm, finite_spectrum)

ELL=ELL_PRE_REGISTERED
EPS0=ground_fraction()


def epsilon(r_m: float, ell: float=ELL, eps0: float=EPS0) -> float:
    if r_m<R_EARTH or ell<=0: raise ValueError('external sphere and ell>0 required')
    return float(eps0*relative_yukawa(r_m-R_EARTH,ell))


def K(r_m: float, mu:float=MU_EARTH_REF, ell:float=ELL, eps0:float=EPS0):
    return mu*(1+epsilon(r_m,ell,eps0))


def potential(r_m, mu=MU_EARTH_REF, ell=ELL, eps0=EPS0):
    x=epsilon(r_m,ell,eps0)/(1+r_m/ell)
    return -mu*(1+x)/r_m


def g_radial(r_m, mu=MU_EARTH_REF, ell=ELL, eps0=EPS0):
    return K(r_m,mu,ell,eps0)/r_m**2


def frequencies(r_m,mu=MU_EARTH_REF,ell=ELL,eps0=EPS0):
    """Newtonian spherical central force: circular and radial epicyclic."""
    ep=epsilon(r_m,ell,eps0)
    S=-(ep/(1+ep))*(r_m/ell)**2/(1+r_m/ell)
    O2=mu*(1+ep)/r_m**3
    k2=O2*(1+S)
    return dict(Omega2=O2,kappa2=k2,S=S,stable=k2>0,
                periapsis=2*math.pi*(1/math.sqrt(1+S)-1) if k2>0 else float('nan'))


def scalar_metric_potentials(r_m,mu=MU_EARTH_REF,ell=ELL,eps0=EPS0):
    """Linearized Jordan-frame metric potentials in inverse length-normalized form.

    Phi/c^2 and Psi/c^2. Scalar contribution cancels from Phi+Psi
    at leading weak-field order. No relativistic full ray-tracing claim.
    """
    eta=epsilon(r_m,ell,eps0)/(1+r_m/ell)
    base=-mu/(r_m*C_LIGHT**2)
    Phi=base*(1+eta)
    Psi=base*(1-eta)
    gamma=Psi/Phi
    return dict(Phi=Phi,Psi=Psi,eta=eta,gamma=gamma,
                lensing_sum=Phi+Psi,lensing_GR_sum=2*base,
                dynamical_to_lensing_mass=1+epsilon(r_m,ell,eps0))


def clock_shift_from_integral(r1,r2,mu=MU_EARTH_REF,ell=ELL,eps0=EPS0):
    return quad(lambda r:g_radial(r,mu,ell,eps0)/C_LIGHT**2,
                r1,r2,epsabs=1e-18,epsrel=1e-12)[0]


def central_orbit_precession(h_m=400000.,e=1e-4,ell=ELL,eps0=EPS0):
    """Independent ODE integration, dimensionless t=Omega0*physical time.

    At x=1+e,w=0, angular momentum chosen for circular orbit at x=1.
    For e->0 the measured radial apsidal advance approaches epicyclic limit.
    """
    if not 0<e<0.01: raise ValueError('e must be small and positive')
    r0=R_EARTH+h_m
    K0=K(r0,mu=1.,ell=ell,eps0=eps0)
    def ode(t,y):
        x,xd,theta=y
        Kr=K(r0*x,mu=1.,ell=ell,eps0=eps0)
        return (xd, x**-3 - (Kr/K0)*x**-2, x**-2)
    def apo(t,y): return y[1]
    apo.direction=-1
    apo.terminal=False
    sol=solve_ivp(ode,(0,28),[1+e,0.,0.],events=apo,method='DOP853',
                  atol=1e-12,rtol=1e-12,max_step=0.08)
    if not sol.success or len(sol.y_events[0])<4:
        raise RuntimeError('orbit integration did not resolve multiple apoapses')
    angles=sol.y_events[0][:,2]
    return dict(n_apoapses=len(angles),precession=float(np.mean(np.diff(angles))-2*math.pi),
                per_orbit_values=[float(x-2*math.pi) for x in np.diff(angles)],
                epicycle=frequencies(r0,ell=ell,eps0=eps0)['periapsis'])


def expected_profiled_null_chi2(shape, covariance, mu=1.):
    """Asimov Δχ²: fixed Yukawa truth versus Newtonian constant mu fit.

    No stochastic observations here. Common GM nuisance marginalized;
    C is full supplied covariance of *normalized* apparent-GM vector.
    """
    y=np.asarray(shape,float)
    C=np.asarray(covariance,float)
    if y.ndim!=1 or C.shape!=(len(y),len(y)):
        raise ValueError('shape and covariance dimensions inconsistent')
    ones=np.ones_like(y)
    W1=np.linalg.solve(C,ones)
    Wy=np.linalg.solve(C,y)
    proj=(ones@Wy)/(ones@W1)
    d=y-proj*ones
    val=mu**2*float(d@np.linalg.solve(C,d))
    return max(val,0.)


def expected_projection_with_nuisances(shape,covariance,nuisance):
    """Projected χ² after fitting multiple linear nuisance templates.

    Columns can include common GM, calibrated altitude trends, etc.
    This is a diagnostic of identifiability, not real tracking inference.
    """
    y=np.asarray(shape,float)
    C=np.asarray(covariance,float)
    X=np.asarray(nuisance,float)
    if X.ndim!=2 or X.shape[0]!=len(y): raise ValueError('nuisance matrix mismatch')
    yc=np.linalg.solve(C,y)
    xc=np.linalg.solve(C,X)
    beta=np.linalg.lstsq(X.T@xc,X.T@yc,rcond=None)[0]
    res=y-X@beta
    return max(0.,float(res@np.linalg.solve(C,res)))


def profile_diagnostic(heights_m, sigma_ind=1e-5, sigma_common=0.,
                       float_height_slope=False):
    hh=np.asarray(heights_m,dtype=float)
    shape=1+np.array([epsilon(R_EARTH+h) for h in hh])
    C=np.eye(len(hh))*sigma_ind**2 + np.ones((len(hh),len(hh)))*sigma_common**2
    X=np.ones((len(hh),1))
    if float_height_slope:
        z=(hh-hh.mean())/(max(hh)-min(hh))
        X=np.column_stack((X,z))
    return {'delta_chi2':expected_projection_with_nuisances(shape,C,X),
            'heights_km':(hh/1e3).tolist(),
            'sigma_ind':sigma_ind,'sigma_common':sigma_common,
            'floating_linear_height_trend':float_height_slope}


def scalaron(ell_m=ELL):
    """Field content/scale of f(R)=R+aR²: a=ell²/6, beta=1/sqrt(6)."""
    if ell_m<=0: raise ValueError('ell must be positive')
    a=ell_m**2/6
    beta=1/math.sqrt(6)
    mass_eV=HBAR*C_LIGHT/ell_m/E_CHARGE
    return {'a_m2':a,'ell_m':ell_m,'beta':beta,
            'alpha_yukawa':2*beta**2,'mass_energy_eV':mass_eV,
            'is_a_free_parameter':True}


def five_height_hankel_trap(step_m=50000.,r0=R_EARTH):
    """Construct an exact two-root degeneracy counterexample.

    A+(u+v*n)q^n satisfies repeated-root Prony perfectly but NOT the
    physical Yukawa 3-parameter shape relation. No satellite data.
    """
    q=math.exp(-step_m/ELL)
    vals=np.array([1+0.01*(1+0.02*n)*q**n for n in range(6)],float)
    s=finite_spectrum(vals,step_m,r0)
    return {'q':s.q_five,'ell_m':s.ell_five_m,
            'repeated_root_residual':s.recurrence_residual,
            'physical_shape_residual':s.yukawa_shape_residual,
            'H0':float(s.H[0]), 'synthetic_K':vals.tolist()}


def noise_correlation_matrix(n,sigma_ind,sigma_common):
    if n<2 or sigma_ind<=0 or sigma_common<0: raise ValueError('invalid noise')
    return sigma_ind**2*np.eye(n)+sigma_common**2*np.ones((n,n))
