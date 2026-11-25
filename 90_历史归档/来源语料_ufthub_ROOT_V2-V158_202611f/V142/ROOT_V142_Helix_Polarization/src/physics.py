"""ROOT V142: exact basic geometry & Maxwell wave checks. Units c=1, not hbar=G=1.
All model predictions remain hypotheses; these checks only test mathematical identities.
"""
import math
import numpy as np


def helix(a, omega, u, t):
    return np.array([a*math.cos(omega*t), a*math.sin(omega*t), u*t],dtype=float)

def helix_kinematics(a, omega, u):
    if a <= 0 or omega <= 0:
        raise ValueError('For signed torsion use signed u; a, omega must be positive')
    speed2=a*a*omega*omega+u*u
    if speed2 <= 0:
        raise ValueError('zero speed')
    kappa=a*omega*omega/speed2
    torsion=u*omega/speed2
    return dict(speed=math.sqrt(speed2),curvature=kappa,torsion=torsion,
                frame_angular_speed=math.hypot(kappa,torsion)*math.sqrt(speed2),
                acceleration=a*omega*omega)

def inverse_null_helix(kappa, torsion):
    if kappa<=0:
        raise ValueError('nondegenerate right-handed null helix only')
    w=math.hypot(kappa,torsion)
    return kappa/(w*w),w,torsion/w

def wave(t,z,k=1.0,amplitude=1.0,magnetic_sign=1):
    """For k>0, phase k(t-z); magnetic_sign=+1 gives +z Poynting."""
    phase=k*(t-z)
    c,s=math.cos(phase),math.sin(phase)
    E=amplitude*np.array([c,s,0.])
    B=magnetic_sign*amplitude*np.array([-s,c,0.])
    return E,B

def maxwell_residuals(t,z,k=1.0,amplitude=1.0,magnetic_sign=1):
    """Exact residuals (Faraday, Ampere) using analytic derivatives, not finite differences."""
    phase=k*(t-z)
    c,s=math.cos(phase),math.sin(phase)
    # For E=(c,s,0), curl E=(k*c,k*s,0); dt B=sign*(-k*c,-k*s,0)
    faraday=amplitude*k*(1-magnetic_sign)*np.array([c,s,0.])
    # dt E=(-k*s,k*c,0); curl B=sign*(-k*s,k*c,0)
    ampere=amplitude*k*(1-magnetic_sign)*np.array([-s,c,0.])
    return faraday,ampere

def noether_mode_count(number_of_first_class,number_of_second_class):
    n_phase=8
    return (n_phase-2*number_of_first_class-number_of_second_class)/2

def scalar_pair_field(epsilon,g=1.,hbar=1.):
    """Example q=epsilon*x,p=epsilon*y in local Cartesian patch: F_xy=epsilon^2."""
    return {'F_xy':epsilon**2,'L_density':-hbar*epsilon**4/(2*g*g)}

def projected_berry_xy(x, alpha, beta):
    """theta=alpha*x, phi=beta*y (coefficient of dx wedge dy)."""
    return 0.5*alpha*beta*math.sin(alpha*x)
