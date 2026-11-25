"""Reproducible c=1, hbar/G dimensional-audit geometry and linear-field identities.

No fitted parameters and no claims of four-force unification.
All plane-wave tensors use lower spacetime indices and signature (-,+,+,+).
"""
from __future__ import annotations
import math
import numpy as np

ETA = np.diag([-1., 1., 1., 1.])


def unit(v):
    x = np.asarray(v, dtype=float)
    norm = np.linalg.norm(x)
    if not np.isfinite(norm) or norm <= 0:
        raise ValueError('nonzero finite direction required')
    return x / norm


def orthonormal_frame(direction):
    n = unit(direction)
    reference = np.array([0., 0., 1.]) if abs(n[2]) < .9 else np.array([0., 1., 0.])
    e1 = unit(np.cross(reference, n))
    e2 = unit(np.cross(n, e1))
    return e1, e2, n


def circular_vectors(direction):
    e1, e2, n = orthonormal_frame(direction)
    return (e1 + 1j * e2)/math.sqrt(2), (e1 - 1j * e2)/math.sqrt(2), n


def tensor_circular(direction):
    ep, em, n = circular_vectors(direction)
    return np.outer(ep, ep), np.outer(em, em), n


def tensor_plus_cross(direction):
    e1, e2, _ = orthonormal_frame(direction)
    return ((np.outer(e1,e1)-np.outer(e2,e2))/math.sqrt(2),
            (np.outer(e1,e2)+np.outer(e2,e1))/math.sqrt(2))


def rotation(axis, angle):
    n=unit(axis)
    x,y,z=n
    K=np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])
    return np.eye(3)+math.sin(angle)*K+(1-math.cos(angle))*(K@K)


def vector_phase(direction, angle):
    ep, em, n=circular_vectors(direction)
    mat=rotation(n,angle)
    return np.vdot(ep,mat@ep), np.vdot(em,mat@em)


def tensor_phase(direction, angle):
    tp,tm,n=tensor_circular(direction)
    mat=rotation(n,angle)
    return (np.vdot(tp,(mat@tp@mat.T)),np.vdot(tm,(mat@tm@mat.T)))


def transverse_projector(direction):
    n=unit(direction)
    return np.eye(3)-np.outer(n,n)


def tt_projector_tensor(direction):
    P=transverse_projector(direction)
    return .5*(np.einsum('ik,jl->ijkl',P,P)+np.einsum('il,jk->ijkl',P,P)
               -np.einsum('ij,kl->ijkl',P,P))


def tt_project(direction, symmetric_tensor):
    s=np.asarray(symmetric_tensor,dtype=float)
    if s.shape != (3,3): raise ValueError('3x3 tensor required')
    return np.einsum('ijkl,kl->ij',tt_projector_tensor(direction),s)


def photon_amplitude(frequency, spatial_direction=(0,0,1), helicity=1):
    """Return covariant null k_mu and covariant epsilon_mu at frequency=|spatial k|."""
    if frequency<=0: raise ValueError('positive frequency required')
    ep,em,n=circular_vectors(spatial_direction)
    eps=ep if helicity==1 else em if helicity==-1 else None
    if eps is None: raise ValueError('helicity +/-1')
    k=np.concatenate(([-frequency],frequency*n))
    a=np.concatenate(([0j],eps))
    return k.astype(complex), a


def field_strength_fourier(k_cov,a_cov):
    k=np.asarray(k_cov,dtype=complex)
    a=np.asarray(a_cov,dtype=complex)
    return 1j*(np.outer(k,a)-np.outer(a,k))


def maxwell_fourier_residual(k_cov,F_cov):
    return (ETA @ np.asarray(k_cov,dtype=complex)) @ np.asarray(F_cov,dtype=complex)


def spin2_tt_amplitude(direction=(0,0,1), helicity=2, frequency=1):
    tp,tm,n=tensor_circular(direction)
    tensor=tp if helicity==2 else tm if helicity==-2 else None
    if tensor is None: raise ValueError('helicity +/-2')
    h=np.zeros((4,4),dtype=complex)
    h[1:,1:]=tensor
    k=np.concatenate(([-frequency],frequency*n)).astype(complex)
    return k,h


def spin2_gauge_shift(k_cov, xi_cov):
    k=np.asarray(k_cov,dtype=complex)
    xi=np.asarray(xi_cov,dtype=complex)
    return np.outer(k,xi)+np.outer(xi,k)


def linearized_riemann(k_cov,h_cov):
    """Plane-wave linearized R_{mu nu rho sigma}; Fourier convention exp(i k.x)."""
    k=np.asarray(k_cov,dtype=complex)
    h=np.asarray(h_cov,dtype=complex)
    R=np.empty((4,4,4,4),dtype=complex)
    for mu in range(4):
      for nu in range(4):
       for rho in range(4):
        for sigma in range(4):
         R[mu,nu,rho,sigma]=-.5*(
            k[rho]*k[nu]*h[mu,sigma]+k[sigma]*k[mu]*h[nu,rho]
            -k[sigma]*k[nu]*h[mu,rho]-k[rho]*k[mu]*h[nu,sigma])
    return R


def linearized_einstein(k_cov,h_cov):
    """Plane-wave G^(1)_mu,nu; exact Bianchi identity for any k and symmetric h."""
    k=np.asarray(k_cov,dtype=complex)
    h=np.asarray(h_cov,dtype=complex)
    kup=ETA@k
    k_sq=k@kup
    trace=np.trace(ETA@h)
    kh=kup@h
    khk=kup@h@kup
    return -.5*(np.outer(k,kh)+np.outer(kh,k)-k_sq*h
                  -np.outer(k,k)*trace-ETA*(khk-k_sq*trace))


def helical_geometry(a, omega, u):
    """3D helix; includes non-null speed to validate v²(kappa²+tau²)=omega²."""
    if a<=0 or omega==0: raise ValueError('a>0 and omega nonzero')
    v2=(a*omega)**2+u**2
    return {'v':math.sqrt(v2), 'kappa':a*omega**2/v2,
            'tau':u*omega/v2, 'omega':omega, 'a':a,'u':u,
            'identity_residual':v2*((a*omega**2/v2)**2+(u*omega/v2)**2)-omega**2}


def simple_gravitational_wave(f_hz=100., strain=1e-21, arm_m=4000.):
    """SI conversion only for display; theoretical equations use x0=ct, c=1."""
    if f_hz<=0 or arm_m<=0 or strain<0: raise ValueError('positive inputs required')
    c_si=299792458.0
    omega_si=2*math.pi*f_hz
    k_inv_m=omega_si/c_si
    return {'f_hz':f_hz,'arm_m':arm_m,'strain':strain,
            'k_inv_m':k_inv_m,'wavelength_m':c_si/f_hz,
            'R_0x0x_amplitude_inv_m2': .5*k_inv_m*k_inv_m*strain,
            'one_arm_displacement_amplitude_m': .5*arm_m*strain,
            'x_minus_y_displacement_amplitude_m':arm_m*strain,
            'tidal_acceleration_amplitude_m_s2': .5*omega_si**2*arm_m*strain}


def dimensional_audit():
    """Exponent tuple (L, H) where H is action [hbar]; c=1 implies T=L."""
    # [G]=L^2 / H, [R]=L^-2, [F]=L^-2, [A]=L^-1
    G=(2,-1); R=(-2,0); H=(0,1); F=(-2,0)
    def plus(*args): return tuple(sum(v[i] for v in args) for i in range(2))
    def neg(v): return tuple(-q for q in v)
    grav=plus(neg(G),R)
    em=plus(H,F,F)
    return {'G':G,'hbar':H,'Ricci':R,'F':F,
            'L_grav':grav,'L_maxwell':em,'expected_density':(-4,1),
            'action':plus(grav,(4,0))}


def lorentz_boost_x(beta):
    """Contravariant x'^mu=Lambda^mu_nu x^nu; signature (-,+,+,+)."""
    if abs(beta)>=1: raise ValueError('boost speed must be |beta|<1')
    gamma=1/math.sqrt(1-beta*beta)
    out=np.eye(4)
    out[0,0]=out[1,1]=gamma
    out[0,1]=out[1,0]=-gamma*beta
    return out


def transform_covector(Lambda, covector):
    return np.linalg.inv(Lambda).T @ np.asarray(covector)


def transform_cov2(Lambda, tensor):
    linv=np.linalg.inv(Lambda)
    return linv.T @ np.asarray(tensor) @ linv


def transform_cov4(Lambda, tensor):
    linv=np.linalg.inv(Lambda)
    return np.einsum('am,bn,cp,dq,abcd->mnpq',linv,linv,linv,linv,np.asarray(tensor))
