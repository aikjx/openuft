"""ROOT V105: exact SU(2)/SU(3) holonomy benchmarks.
All objects are mathematical test cases, not physical observation.
"""
import numpy as np

I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def su2_rotation(angle: float, axis: str):
    """exp(i angle sigma_axis); angle in radians."""
    sigma = {"x": SIGMA_X, "y": SIGMA_Y, "z": SIGMA_Z}[axis]
    return np.cos(angle)*I2 + 1j*np.sin(angle)*sigma


def matrix_commutator(U, V):
    """Unitary group commutator U V U^-1 V^-1."""
    return U @ V @ U.conj().T @ V.conj().T


def su2_holonomy(alpha, beta):
    U = su2_rotation(alpha, 'x')
    V = su2_rotation(beta, 'y')
    return matrix_commutator(U, V)


def su2_wilson_trace(alpha, beta):
    return float(np.trace(su2_holonomy(alpha, beta)).real / 2)


def su2_closed_form(alpha, beta):
    return float(1-2*np.sin(alpha)**2 * np.sin(beta)**2)


def su3_embed(U2):
    V3 = np.eye(3, dtype=complex)
    V3[:2,:2] = U2
    return V3


def su3_wilson_trace(alpha, beta):
    U = su3_embed(su2_rotation(alpha, 'x'))
    V = su3_embed(su2_rotation(beta, 'y'))
    return float(np.trace(matrix_commutator(U,V)).real / 3)


def su3_closed_form(alpha, beta):
    return float(1-(4/3)*np.sin(alpha)**2*np.sin(beta)**2)


def u1_wilson_commutator(alpha, beta):
    A, B = np.exp(1j*alpha), np.exp(1j*beta)
    return A*B/A/B


def gauge_transform_unitary(alpha=0.2, axis='z'):
    return su2_rotation(alpha,axis)


def conjugated_wilson_trace(alpha,beta,rotation=0.31):
    H = su2_holonomy(alpha,beta)
    Q = gauge_transform_unitary(rotation)
    return float(np.trace(Q@H@Q.conj().T).real/2)


def small_loop_ratio(epsilon):
    """Gauge group commutator (U V U^-1 V^-1) leading term / eps^2.
    U=e^(eps X), V=e^(eps Y), X=i sigma_x, Y=i sigma_y.
    """
    X, Y = 1j*SIGMA_X, 1j*SIGMA_Y
    W = su2_holonomy(epsilon,epsilon)
    return (W-I2)/epsilon**2, X@Y-Y@X
