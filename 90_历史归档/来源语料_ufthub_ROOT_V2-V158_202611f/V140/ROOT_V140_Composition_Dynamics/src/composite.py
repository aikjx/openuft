"""ROOT V140: composite two-form geometric model in flat Minkowski spacetime.
Coordinates (t,x,y,z), metric signature (-,+,+,+). c=1; hbar and G
are retained as independent constants in the research notes.
This is a representation/equivalence audit, NOT a new physics proof.
"""
import sympy as sp

t, x, y, z = COORDS = sp.symbols('t x y z', real=True)
eta = sp.diag(-1, 1, 1, 1)


def simp_m(M):
    return M.applyfunc(sp.trigsimp).applyfunc(sp.simplify)


def grad(f):
    return sp.Matrix([sp.diff(f, c) for c in COORDS])


def wedge1(a, b):
    return a*b.T - b*a.T


def field(pairs):
    f = sp.zeros(4, 4)
    for q, p in pairs:
        f += wedge1(grad(q), grad(p))
    return simp_m(f)


def raise_both(f):
    return simp_m(eta * f * eta)


def current(f):
    """J^nu = partial_mu F^{mu nu}, no external electric source."""
    fu = raise_both(f)
    return sp.Matrix([sp.simplify(sum(sp.diff(fu[m, n], COORDS[m]) for m in range(4))) for n in range(4)])


def projections(j, pairs):
    return [sp.simplify((grad(s).T * j)[0]) for pair in pairs for s in pair]


def pfaff(f):
    return sp.factor(f[0, 1]*f[2, 3]-f[0, 2]*f[1, 3]+f[0, 3]*f[1, 2])


def f_squared(f):
    fu = raise_both(f)
    return sp.simplify(sum(f[i, j]*fu[i, j] for i in range(4) for j in range(4)))


def bianchi(f):
    out=[]
    for i in range(4):
        for j in range(i+1, 4):
            for k in range(j+1, 4):
                out.append(sp.simplify(sp.diff(f[j,k], COORDS[i])+
                    sp.diff(f[k,i], COORDS[j])+sp.diff(f[i,j], COORDS[k])))
    return out


def jacobian(pairs):
    return sp.Matrix([list(grad(v)) for pair in pairs for v in pair])


def electric_magnetic(f):
    # E_i := F_0i; B=(F_23,F_31,F_12). In this sign convention,
    # field energy density is (E^2+B^2)/2 times hbar/g_F^2.
    E = sp.Matrix([f[0,1], f[0,2], f[0,3]])
    B = sp.Matrix([f[2,3], f[3,1], f[1,2]])
    return E, B


def stress(f):
    """T_{mu nu} / (hbar/g_F^2) = F_{mu alpha} F_nu{}^alpha - eta_mu nu F^2/4."""
    return simp_m(f*eta*f.T - eta*f_squared(f)/4)


def stress_divergence(f):
    upper = simp_m(eta * stress(f) * eta)
    return [sp.simplify(sum(sp.diff(upper[m,n], COORDS[m]) for m in range(4))) for n in range(4)]


def constant_rank4():
    return [(t,x),(y,z)]


def rank4_offshell(beta=sp.Rational(1, 3)):
    return [(t, x+beta*y*y),(y,z)]


def forcefree_beltrami(k=sp.Integer(2)):
    # Locally equivalent to a single unit-vector pullback; second pair constant.
    return [(z, x*sp.sin(k*z)-y*sp.cos(k*z)), (sp.Integer(0),sp.Integer(0))]


def circular_plane_wave(k=sp.Integer(3)):
    s=t-z
    # This field is a rotating polarization propagating along a straight null direction.
    return [(s, x*sp.cos(k*s)+y*sp.sin(k*s)), (sp.Integer(0),sp.Integer(0))]


def rank4_parallel_fields():
    # E parallel B; both point along x in this convention.
    # F01 = 1, F23=1, Pfaffian=1.
    return [(t,x),(y,z)]


def lorentz_boost_x(beta):
    ga=1/sp.sqrt(1-beta**2)
    return sp.Matrix([[ga,-ga*beta,0,0],[-ga*beta,ga,0,0],[0,0,1,0],[0,0,0,1]])


def simple_status(pairs):
    f=field(pairs)
    j=current(f)
    return {
        'pfaffian': str(pfaff(f)),
        'F2': str(f_squared(f)),
        'J': [str(v) for v in j],
        'projected_EOM': [str(v) for v in projections(j,pairs)],
        'Bianchi': [str(v) for v in bianchi(f)],
    }
