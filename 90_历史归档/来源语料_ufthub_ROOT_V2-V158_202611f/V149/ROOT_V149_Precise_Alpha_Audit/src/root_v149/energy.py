"""Comparing geometry-rotation and propagating-wave frequencies (c=1)."""
import math
from .core import Helix

def tangent_null_energy_boost_ratio(h:Helix,beta:float)->float:
    """Conditional model: null momentum spatial direction equals helix tangent."""
    if not -1.0 < beta < 1.0: raise ValueError('invalid boost')
    return (1-beta*h.u)/math.sqrt(1-beta*beta)

def geometric_frequency_boost_ratio(h:Helix,beta:float)->float:
    return h.boost_z(beta).omega / h.omega

def ratio_E_over_hbar_omega(h:Helix,beta:float)->float:
    """Ratio (E'/hbar omega')/(E/hbar omega) under conditional tangent momentum."""
    return tangent_null_energy_boost_ratio(h,beta)/geometric_frequency_boost_ratio(h,beta)

def plane_wave_energy_frequency_ratio(beta:float)->float:
    """E' / E and omega' / omega for true photon moving along +z, both equal this."""
    if not -1.0 < beta < 1.0:raise ValueError('invalid boost')
    return (1-beta)/math.sqrt(1-beta*beta)
