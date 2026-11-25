"""Differential-form and axion-Maxwell audit for ROOT V141.

Signature (-,+,+,+). Coordinates (t,x,y,z). Only c=1;
no choice setting hbar=1 or G=1 is made in the physical action.
Numerical dimensionless examples use a reference length L0, with
physical energies restored by the hbar/L0^4 factor.
"""
import sympy as sp

coords = (t, x, y, z) = sp.symbols('t x y z', real=True)
metric = sp.diag(-1, 1, 1, 1)


def differential(expr):
    return sp.Matrix([sp.diff(expr, coord) for coord in coords])


def wedge(v, w):
    return v*w.T - w*v.T


def field_strength(potential):
    if len(potential) != 4:
        raise ValueError('A must have four components')
    mat = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            mat[mu, nu] = sp.diff(potential[nu], coords[mu]) - sp.diff(potential[mu], coords[nu])
    return mat.applyfunc(sp.simplify)


def internal_field(pairs):
    tensor = sp.zeros(4)
    for q, p in pairs:
        tensor += wedge(differential(q), differential(p))
    return tensor.applyfunc(sp.simplify)


def bianchi(field_tensor):
    vals = []
    for a in range(4):
        for b in range(a+1, 4):
            for c in range(b+1, 4):
                vals.append(sp.simplify(
                    sp.diff(field_tensor[b, c], coords[a]) +
                    sp.diff(field_tensor[c, a], coords[b]) +
                    sp.diff(field_tensor[a, b], coords[c])))
    return vals


def maxwell_current(field_tensor):
    raised = metric * field_tensor * metric
    return sp.Matrix([sp.simplify(sum(sp.diff(raised[mu, nu], coords[mu])
                                    for mu in range(4))) for nu in range(4)])


def composite_shift(potential, pairs, eta):
    """Locally A_eff=A+eta sum(q dp): dA_eff = dA+eta Omega."""
    beta = sp.zeros(4, 1)
    for q,p in pairs:
        beta += q * differential(p)
    shifted = potential + eta*beta
    return shifted, field_strength(shifted)


def plane_wave(k, omega):
    """Traveling plane wave: A_x=cos(kz-omega*t); source-free when omega^2=k^2."""
    return sp.Matrix([0, sp.cos(k*z-omega*t), 0, 0])


def lagrangian_density_units():
    """Powers of L of bracket terms using c=1, hbar of dimension ML.

    [G]=L/M, [hbar]=ML so [G*hbar]=L^2.
    """
    return {
        'coordinate': 1,
        'A': -1,
        'F': -2,
        'theta': 0,
        'f': -1,
        'R': -2,
        'G_times_hbar': 2,
        'gravity_R_over_Ghbar': -4,
        'Maxwell_F_squared': -4,
        'scalar_f_squared_gradtheta_squared': -4,
        'axion_theta_F_dualF': -4,
        'd4x': 4,
    }


def single_field_quartic_order():
    """Internal q=q0+e*x, p=p0+e*y => F_xy=e^2, F^2=2e^4."""
    epsilon = sp.symbols('epsilon', real=True)
    q0,p0 = sp.symbols('q0 p0', real=True)
    tensor = internal_field([(q0+epsilon*x, p0+epsilon*y)])
    invariant = sp.expand(sum(tensor[i,j]*(metric*tensor*metric)[i,j]
                             for i in range(4) for j in range(4)))
    return sp.simplify(tensor[1,2]), sp.factor(invariant)
