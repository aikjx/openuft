"""ROOT V153 audit: verified existing linear gauge theory mathematics.

Units: c=1 only. eta=(-,+,+,+). All four-vector arrays are COVARIANT
unless labeled 'contrav'. Fourier amplitudes omit a common factor of i.
A scalar phase alone generates only pure-gauge fields in the local smooth ansatz.
"""
from __future__ import annotations
import numpy as np

ETA = np.diag([-1., 1., 1., 1.])


def k_lower(energy: float=1.):
    return np.array([-energy, 0., 0., energy])


def k_upper(energy: float=1.):
    return np.array([energy, 0., 0., energy])


def maxwell_field(k_cov, a_cov):
    """Fourier-amplitude F_mn / i (multiply by i for e^{ikx} field)."""
    k = np.asarray(k_cov)
    a = np.asarray(a_cov)
    return np.outer(k, a) - np.outer(a, k)


def maxwell_divergence(k_up, F):
    return np.einsum('m,mn->n', k_up, F)


def spin2_pure_gauge(k_cov, xi_cov):
    k, x = np.asarray(k_cov), np.asarray(xi_cov)
    return np.outer(k, x) + np.outer(x, k)


def spin2_tt(plus=1., cross=0.):
    h = np.zeros((4, 4))
    h[1, 1] = plus
    h[2, 2] = -plus
    h[1, 2] = h[2, 1] = cross
    return h


def linear_riemann(k_cov, h):
    """Linear R_mnrs amplitude for h_mn*exp(i k*x).
    R_mnrs = 1/2 (d_r d_n h_ms + d_s d_m h_nr
                   -d_r d_m h_ns -d_s d_n h_mr).
    """
    k, h = np.asarray(k_cov), np.asarray(h)
    r = np.zeros((4, 4, 4, 4), dtype=np.result_type(k, h, float))
    for m in range(4):
        for n in range(4):
            for p in range(4):
                for q in range(4):
                    r[m,n,p,q] = -.5 * (
                        k[p]*k[n]*h[m,q] + k[q]*k[m]*h[n,p]
                        - k[p]*k[m]*h[n,q] - k[q]*k[n]*h[m,p])
    return r


def lorentz_z(beta):
    if not (-1 < beta < 1):
        raise ValueError('beta must be strictly between -1 and 1')
    gamma = 1. / np.sqrt(1.-beta**2)
    mat = np.eye(4)
    mat[0,0] = mat[3,3] = gamma
    mat[0,3] = mat[3,0] = -gamma*beta
    return mat


def lorentz_cov(beta):
    return ETA @ lorentz_z(beta) @ ETA


def transform_rank4_cov(r, transform):
    return np.einsum('am,bn,cp,dq,mnpq->abcd', transform, transform,
                     transform, transform, r, optimize=True)


def vector_physical_modes():
    """Null k=(1,0,0,1), Lorenz condition and gauge quotient => e1,e2."""
    a1 = np.array([0.,1.,0.,0.])
    a2 = np.array([0.,0.,1.,0.])
    return a1,a2


def rotate_transverse(angle, e1, e2):
    c,s = np.cos(angle),np.sin(angle)
    return c*e1+s*e2, -s*e1+c*e2


def scalar_helicity_phase(angle):
    """Complex Lorentz scalar transforms trivially under a spatial rotation."""
    return 1.+0j


def wave_helicity_phase(spin, angle):
    return np.exp(-1j*spin*angle)


def linear_ricci(k_cov, h):
    """Linear Ricci tensor from contraction R_mnrs: Ricci_nq=eta^mp R_mnpq."""
    r = linear_riemann(k_cov, h)
    return np.einsum('mp,mnpq->nq',ETA,r)


def linear_einstein(k_cov,h):
    ricci=linear_ricci(k_cov,h)
    scalar=np.einsum('mn,mn',ETA,ricci)
    return ricci-.5*ETA*scalar


def rotation_z4(phi):
    c,s=np.cos(phi),np.sin(phi)
    R=np.eye(4)
    R[1,1]=R[2,2]=c
    R[1,2]=-s
    R[2,1]=s
    return R
