"""ROOT V144: Lie-algebra audit, KK charged mode bound and chirality obstruction.
Established mathematics, NOT an experimentally confirmed unified theory.
Conventions: c=1 in symbolic equations; c_SI is restored only for dimensional conversion.
"""
from __future__ import annotations
import math
import numpy as np

# NIST / CODATA 2022 references. SI constants used only for numeric conversion.
G_SI = 6.67430e-11
H_SI = 6.62607015e-34
HBAR_SI = H_SI / (2 * math.pi)
C_SI = 299792458.0
M_E_SI = 9.1093837139e-31
M_MU_SI = 1.883531627e-28
M_P_SI = 1.67262192595e-27
ALPHA_OBS = 7.2973525643e-3


def sigma_matrices():
    i = 1j
    return [np.array([[0, 1], [1, 0]], complex),
            np.array([[0, -i], [i, 0]], complex),
            np.array([[1, 0], [0, -1]], complex)]


def gell_mann_matrices():
    i = 1j
    z = lambda: np.zeros((3, 3), dtype=complex)
    out = []
    for (a, b, imaginary) in [(0, 1, False), (0, 1, True),
                               (0, 2, False), (0, 2, True),
                               (1, 2, False), (1, 2, True)]:
        m = z()
        if imaginary:
            m[a, b], m[b, a] = -i, i
        else:
            m[a, b] = m[b, a] = 1
        out.append(m)
    d3 = np.diag([1, -1, 0]).astype(complex)
    d8 = np.diag([1, 1, -2]).astype(complex) / math.sqrt(3)
    # Standard numbering lambda_1 ... lambda_8
    return [out[0], out[1], d3, out[2], out[3], out[4], out[5], d8]


def antihermitian_generators(group: str):
    mats = sigma_matrices() if group == 'su2' else gell_mann_matrices() if group == 'su3' else None
    if mats is None:
        raise ValueError('group must be su2 or su3')
    return [-0.5j * m for m in mats]


def comm(a, b):
    return a @ b - b @ a


def structure_constants(generators):
    """[T_a,T_b]=sum_c f_abc T_c and tr(T_a T_b)=-delta_ab/2."""
    n = len(generators)
    f = np.zeros((n, n, n))
    for a in range(n):
        for b in range(n):
            z = comm(generators[a], generators[b])
            for c in range(n):
                v = -2.0 * np.trace(z @ generators[c])
                if abs(v.imag) > 1e-10:
                    raise ValueError('non-real structure constant')
                f[a, b, c] = v.real
    return f


def jacobi_tensor(f):
    """J_abcd=sum_e(f_abe f_ecd+f_bce f_ead+f_cae f_ebd)."""
    return (np.einsum('abe,ecd->abcd', f, f) +
            np.einsum('bce,ead->abcd', f, f) +
            np.einsum('cae,ebd->abcd', f, f))


def total_generators():
    """12 generators in explicit 3+2+1 block rep, NOT realistic matter hypercharges."""
    result = []
    for t in antihermitian_generators('su3'):
        m = np.zeros((6, 6), complex); m[:3, :3] = t; result.append(m)
    for t in antihermitian_generators('su2'):
        m = np.zeros((6, 6), complex); m[3:5, 3:5] = t; result.append(m)
    m = np.zeros((6, 6), complex); m[5, 5] = 1j; result.append(m)
    return result


def su2_pure_gauge_components(y):
    """U=exp(x T1)exp(y T2), omega=U^-1 dU, returns coordinate T coefficients."""
    # omega_x = cos(y) T1 + sin(y) T3, omega_y = T2
    return np.array([math.cos(y), 0., math.sin(y)]), np.array([0., 1., 0.])


def su2_pure_gauge_curvature(y):
    """F_xy=partial_x omega_y-partial_y omega_x + [omega_x,omega_y]."""
    dx_omega_y = np.zeros(3)
    dy_omega_x = np.array([-math.sin(y), 0., math.cos(y)])
    wx, wy = su2_pure_gauge_components(y)
    return dx_omega_y - dy_omega_x + np.cross(wx, wy)


def kk_alpha_for_mass(m_si):
    """alpha_KK=4 G m^2/hbar with c=1; restoring c to read SI masses/constants."""
    return 4 * G_SI * (m_si ** 2) / (HBAR_SI * C_SI)


def kk_min_mass_for_alpha(alpha=ALPHA_OBS):
    """Minimum 4D charged mass at prescribed alpha for untwisted 5D KK n!=0."""
    return math.sqrt(alpha * HBAR_SI * C_SI / (4 * G_SI))


def kk_radius_for_mass(m_si):
    """n=1 and m5=0: R=hbar/(m*c), SI conversion only."""
    return HBAR_SI / (m_si * C_SI)


def kk_radius_for_alpha(alpha=ALPHA_OBS):
    return kk_radius_for_mass(kk_min_mass_for_alpha(alpha))


def kk_mass_from_radius(r_si, n=1, m5_si=0.):
    return math.hypot(m5_si, abs(n) * HBAR_SI / (r_si * C_SI))


def bi_invariant_scalar_coefficient(f):
    """Scal * (orthonormal-frame length)^2 = sum_abc f_abc^2/4."""
    return np.sum(f*f) / 4.


def product_scalar_curvature(ell_su3=1., ell_su2=1.):
    """Positive bi-invariant product metric SU3 x SU2 x U1.
    ell's describe physical lengths of the reference Lie algebra frames.
    """
    if ell_su3 <= 0 or ell_su2 <= 0:
        raise ValueError('positive metric scales required')
    f3 = structure_constants(antihermitian_generators('su3'))
    f2 = structure_constants(antihermitian_generators('su2'))
    return bi_invariant_scalar_coefficient(f3)/ell_su3**2 + bi_invariant_scalar_coefficient(f2)/ell_su2**2


def lie_algebra_summary():
    f2 = structure_constants(antihermitian_generators('su2'))
    f3 = structure_constants(antihermitian_generators('su3'))
    return {'dims': {'SO3_spatial_rotations': 3, 'SU3':8, 'SU2':3,'U1':1,'SM_generators':12,
                      'direct_group_internal_dimension':12,'direct_product_total_dimension':16,
                      'SU3_internal_dimension_alternative':8,'SU3_alternative_total_dimension':12},
            'f2_123': float(f2[0,1,2]), 'f3_123': float(f3[0,1,2]),
            'f3_458': float(f3[3,4,7]),
            'jacobi_max_su2': float(np.max(np.abs(jacobi_tensor(f2)))),
            'jacobi_max_su3': float(np.max(np.abs(jacobi_tensor(f3)))),
            'scalar_coeff_su2': float(bi_invariant_scalar_coefficient(f2)),
            'scalar_coeff_su3': float(bi_invariant_scalar_coefficient(f3)),
            'scalar_product_equal_length_L0': float(product_scalar_curvature())}


def kk_summary():
    alpha_e = kk_alpha_for_mass(M_E_SI)
    mfit = kk_min_mass_for_alpha()
    return {'alpha_observed': ALPHA_OBS,
            'alpha_electron_naive_kk': alpha_e,
            'alpha_mismatch_factor': ALPHA_OBS/alpha_e,
            'charged_kk_lower_mass_kg': mfit,
            'lower_mass_to_electron_ratio': mfit/M_E_SI,
            'radius_for_electron_mass_m': kk_radius_for_mass(M_E_SI),
            'radius_for_observed_alpha_m': kk_radius_for_alpha(),
            'radius_mismatch_factor': kk_radius_for_mass(M_E_SI)/kk_radius_for_alpha(),
            'G_SI':G_SI,'hbar_SI':HBAR_SI,'c_SI_conversion_only':C_SI,
            'not_new_physics':True}
