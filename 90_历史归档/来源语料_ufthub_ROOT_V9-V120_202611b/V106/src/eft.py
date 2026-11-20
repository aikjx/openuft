"""Topological theta shift quantum consistency (conditional on Q in integers)."""
import cmath, math

def topological_path_integral_phase(k, Q, winding=1):
    """Ratio of e^{iS} under θ -> θ+2π winding, normalized topological Q∈Z."""
    return cmath.exp(2j*math.pi*k*Q*winding)

def normalized_scalar_mass(f_gev, lam_gev):
    if f_gev<=0 or lam_gev<0: raise ValueError('f>0, lambda>=0')
    return lam_gev**2/f_gev
