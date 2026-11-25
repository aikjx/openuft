"""Unit-c=1 mathematical checks for V151 helicity and helical-geometry research.

Physical scope:
- momentum-direction Berry curvature of massless spin-one transverse basis
- plane electromagnetic Maxwell waves (established physics)
- counterexamples to identifying pure frame rotation with real EM field
No running parameter is fitted to experimental alpha.
"""
from __future__ import annotations
from math import sqrt, sin, cos, pi, exp, isclose
from dataclasses import dataclass
import numpy as np


ALPHA_CODATA_2022 = 0.0072973525643  # observation only; not model prediction


def photon_alpha_reference() -> float:
    return ALPHA_CODATA_2022


def sph_frame(theta: float, phi: float):
    """Propagation n, tangent e_theta, e_phi; local chart excludes poles."""
    sth, cth, sph, cph = sin(theta), cos(theta), sin(phi), cos(phi)
    n = np.array([sth*cph, sth*sph, cth], dtype=float)
    et = np.array([cth*cph, cth*sph, -sth], dtype=float)
    ep = np.array([-sph, cph, 0.0], dtype=float)
    return n, et, ep


def circular_basis(theta: float, phi: float, sigma: int = 1) -> np.ndarray:
    if sigma not in (-1, 1):
        raise ValueError("sigma must be +1 or -1")
    _, et, ep = sph_frame(theta, phi)
    return (et + 1j*sigma*ep)/sqrt(2)


def berry_connection(theta: float, sigma: int = 1, dchi_dphi: float = 0.0) -> tuple[float,float]:
    """A=-i e* de, basis e_sigma=(e_theta+i sigma e_phi)/sqrt(2).
    phase e -> e^(i chi) e gives A -> A + dchi.
    """
    if sigma not in (-1,1):
        raise ValueError("sigma must be +1 or -1")
    return 0.0, -sigma*cos(theta)+dchi_dphi


def berry_curvature_theta(theta: float, sigma: int = 1) -> float:
    if sigma not in (-1,1):
        raise ValueError("sigma must be +1 or -1")
    return sigma*sin(theta)


def berry_curvature_k(k: tuple[float,float,float] | np.ndarray, sigma: int = 1) -> np.ndarray:
    """Berry curvature in MOMENTUM SPACE, not spacetime Maxwell F_mu_nu."""
    kval=np.asarray(k, dtype=float)
    if kval.shape != (3,):
        raise ValueError("k must have 3 components")
    norm=np.linalg.norm(kval)
    if norm <= 0:
        raise ValueError("k=0 has an excluded monopole singularity")
    if sigma not in (-1,1):
        raise ValueError("sigma must be +1 or -1")
    return sigma*kval/norm**3


def berry_flux_numeric(n_grid: int = 32, sigma: int = 1) -> float:
    """Independent Gauss-Legendre integration over cos(theta) plus phi grid.
    With sin(theta)dtheta = -d(cos theta), integrate Ftheta_phi.
    """
    if n_grid < 2:
        raise ValueError("n_grid >=2 required")
    nodes,weights=np.polynomial.legendre.leggauss(n_grid)
    # theta=arccos(x); sin(theta)dtheta=-dx; curvature/sin = sigma
    integrand = np.array([berry_curvature_theta(float(np.arccos(x)),sigma) / np.sqrt(1-x*x) for x in nodes])
    return float(2*pi*np.dot(weights,integrand))


def chern_number_numeric(n_grid: int = 32, sigma: int = 1) -> float:
    return berry_flux_numeric(n_grid,sigma)/(2*pi)


def cap_phase(theta: float,sigma:int=1) -> float:
    """Berry flux through northern cap, gauge-invariant phase modulo 2pi."""
    return sigma*2*pi*(1-cos(theta))


def pure_phase_field_strength(hessian: np.ndarray) -> np.ndarray:
    """For A_mu=partial_mu psi, F_mu_nu=H_{nu,mu}-H_{mu,nu}=0 if smooth."""
    h=np.asarray(hessian,dtype=float)
    if h.shape != (4,4):
        raise ValueError("expected 4x4 Hessian")
    return h.T-h


@dataclass(frozen=True)
class PlaneWave:
    """Propagating +z, phase omega(t-z), B=z cross E, c=1."""
    omega: float
    amp: float = 1.0
    sigma: int = 1

    def __post_init__(self):
        if self.omega <= 0 or self.amp <= 0 or self.sigma not in (-1,1):
            raise ValueError("omega, amp positive and sigma=+-1 required")

    def fields(self,t:float,z:float):
        ph=self.omega*(t-z)
        c,s=cos(ph),sin(ph)
        E=self.amp*np.array([c,self.sigma*s,0.0])
        B=self.amp*np.array([-self.sigma*s,c,0.0])
        return E,B

    def maxwell_residuals(self,t:float,z:float):
        """All four vacuum Maxwell residuals in 3+1 notation."""
        ph=self.omega*(t-z); c,s=cos(ph),sin(ph)
        w=self.omega*self.amp; si=self.sigma
        # time derivatives
        dtE=w*np.array([-s,si*c,0.0]); dtB=w*np.array([-si*c,-s,0.0])
        # z derivatives = -time derivatives
        dzE=-dtE; dzB=-dtB
        curlE=np.array([-dzE[1], dzE[0],0.0]);curlB=np.array([-dzB[1],dzB[0],0.0])
        return {
            "faraday":dtB+curlE,
            "ampere":dtE-curlB,
            "divE":0.0,
            "divB":0.0,
        }

    def boost_z(self,beta:float):
        if not (-1<beta<1):
            raise ValueError("proper boost beta must satisfy |beta|<1")
        D=(1-beta)/sqrt(1-beta*beta)
        return PlaneWave(self.omega*D,self.amp*D,self.sigma),D


def plane_wave(omega:float=1, amp:float=1, sigma:int=1)->PlaneWave:
    return PlaneWave(omega,amp,sigma)


def plane_wave_residuals(wave:PlaneWave,t:float,z:float):
    return wave.maxwell_residuals(t,z)


def plane_wave_lorentz_boost(wave:PlaneWave,beta:float):
    return wave.boost_z(beta)


def helix_data(a:float,omega:float,u:float)->dict[str,float]:
    """Spatial helix for an arbitrary constant v, including null spatial v=1.
    For parameter t, curvature=k=a omega^2/v^2; torsion=u omega/v^2.
    """
    if a<=0 or omega<=0 or not (-1<=u<=1):
        raise ValueError("a,omega positive and |u|<=1")
    v2=(a*omega)**2+u*u
    if v2>1+1e-12:
        raise ValueError("superluminal spatial speed not admissible in c=1")
    return {"v":sqrt(v2), "curvature":a*omega*omega/v2,
            "torsion":u*omega/v2,
            "omega":omega,"a":a,"u":u,
            "geometric_fraction":(a*omega)**2/v2}


def helicity_eigen_residual(theta:float,phi:float,sigma:int=1)->float:
    n,_,_=sph_frame(theta,phi)
    eps=circular_basis(theta,phi,sigma)
    return float(np.linalg.norm(1j*np.cross(n,eps)-sigma*eps))


def electromagnetic_invariants(E:np.ndarray,B:np.ndarray)->tuple[float,float]:
    """I1=2(B²-E²), I2=-4 E·B in (+---) convention."""
    E=np.asarray(E,dtype=float);B=np.asarray(B,dtype=float)
    return 2*(float(B@B)-float(E@E)), -4*float(E@B)


def photon_dof_count()->int:
    """Four-vector phase space 8 minus 2 first-class constraints, /2."""
    return (8-2*2)//2
