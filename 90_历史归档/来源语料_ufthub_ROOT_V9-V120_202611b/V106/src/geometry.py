"""V106: rigorous restricted geometry statement, numerically checked two-phase repair."""
import numpy as np
from scipy.linalg import expm

SIGMA_X = np.array([[0,1],[1,0]], dtype=complex)
SIGMA_Y = np.array([[0,-1j],[1j,0]], dtype=complex)
SIGMA_Z = np.diag([1,-1]).astype(complex)
X = .5j*SIGMA_X
Y = .5j*SIGMA_Y
Z = -.5j*SIGMA_Z


def matrix_curvature_two_phase(length_m: float):
    """For A=X dtheta+Y dphi, theta=x/l, phi=y/l.
    Anti-Hermitian SU(2) convention F=dA+A∧A; F_xy=[X,Y]/l².
    """
    if length_m <= 0: raise ValueError('length_m must be positive')
    return (X @ Y - Y @ X) / length_m**2


def matrix_holonomy(a: float, b: float):
    """Rectangular commutator loop exp(aX) exp(bY) exp(-aX) exp(-bY)."""
    return expm(a*X) @ expm(b*Y) @ expm(-a*X) @ expm(-b*Y)


def phase_only_curvature(theta_x, theta_y, theta_xy, theta_yx, M, dM):
    """Compute F_xy in A_i=M(theta)*∂_i theta, where same M(theta) applies.
    For C² theta, ∂xy=∂yx and F vanishes, even for non-Abelian M.
    """
    dxA_y = dM * (theta_x*theta_y) + M*theta_xy
    dyA_x = dM * (theta_y*theta_x) + M*theta_yx
    comm = (M@M - M@M) * theta_x*theta_y
    return dxA_y-dyA_x+comm


def su2_holonomy_small_loop_error(h):
    if h <= 0: raise ValueError('h>0')
    return np.linalg.norm(matrix_holonomy(h,h) - (np.eye(2)+h*h*Z), ord='fro')


def connection_holonomy_eigenphases(theta):
    """Flat S1 example: A=X dtheta, holonomy exp(2πX); F=0 despite nonidentity holonomy."""
    return np.linalg.eigvals(expm(theta*X))
