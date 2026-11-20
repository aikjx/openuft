"""ROOT V108 reproducible, conditional mathematical/physics audits.

No conclusion in this module purports to demonstrate observed new physics,
UV-complete quantum gravity, or non-circular G.
"""
from __future__ import annotations
import math
import sympy as sp
import mpmath as mp
from fractions import Fraction

SM_BETA = (sp.Rational(41,10),sp.Rational(-19,6),sp.Integer(-7))
DB_D = (sp.Rational(2,5),sp.Rational(2,3),sp.Integer(0))
DB_T = (sp.Rational(4,15),sp.Integer(0),sp.Rational(2,3))

# All rows in the matched one-loop threshold regime mu>MT>MD>MZ.
def threshold_design(n:int=2)->sp.Matrix:
    if n < 1 or int(n)!=n: raise ValueError('positive integer multiplets required')
    return sp.Matrix([[sp.Integer(1), SM_BETA[i]+n*(DB_D[i]+DB_T[i]),
                       -n*DB_D[i],-n*DB_T[i]] for i in range(3)])

def threshold_identifiability(n:int=2)->dict:
    mat=threshold_design(n)
    ns=mat.nullspace()
    return dict(rank=mat.rank(), unknowns=mat.cols, nullity=len(ns),
                null_vector=[str(x) for x in ns[0]],
                fixed_doublet_det=str(mat[:,[0,1,3]].det()),
                matrix=[[str(x) for x in row] for row in mat.tolist()])

def predicted_low_couplings(alpha_u_inv, t, log_md, log_mt, n=2):
    """Exact normalized 2*pi times inverse couplings, all thresholds active.
    parameters (2*pi*alpha_u_inv, t, log_md, log_mt)
    output 2*pi*alpha_i^-1, with t=ln(mu/MZ), log_md=ln(MD/MZ).
    """
    M=threshold_design(n)
    vec=sp.Matrix([alpha_u_inv,t,log_md,log_mt])
    return M*vec

def compact_torus_translation_commutator(k):
    if k<1: raise ValueError('torus dimension positive')
    # Lie algebra of translations is R^k, all structure constants identically zero.
    return {(i,j,l): 0 for i in range(k) for j in range(k) for l in range(k)}

def bpst_density(r, rho=1):
    """Positive BPST charge density: q(x)=6*rho^4/[pi^2 (r^2+rho^2)^4].
    SU(2) on R4 (compactifies to S4); this is |c2|=1 in standard orientation.
    """
    if rho <= 0 or r < 0: raise ValueError('positive radius, nonnegative r')
    return 6*rho**4/(mp.pi**2*(r*r+rho*rho)**4)

def bpst_cumulative(R, rho=1):
    """Exact topological charge contained in a radius-R four-ball, Q(infty)=1."""
    if rho <= 0 or R < 0: raise ValueError('positive rho, nonnegative R')
    if mp.isinf(R): return mp.mpf(1)
    z=mp.mpf(R)**2/(mp.mpf(R)**2+mp.mpf(rho)**2)
    return z*z*(3-2*z)  # 1 - 3/(1+x)^2 + 2/(1+x)^3

def bpst_radial_integral(R=mp.inf, rho=1, precision=60):
    mp.mp.dps=precision
    if rho<=0 or R < 0: raise ValueError('positive rho, nonnegative R')
    return mp.quad(lambda r:2*mp.pi**2*r**3*bpst_density(r,rho),[0,R])

def bpst_field_strength_identity():
    """Independently generate regular-gauge A and verify symbolic field strength.
    Convention: F^a_mn=d_m A^a_n-d_n A^a_m+epsilon_abc A^b_m A^c_n.
    eta^a_{ij}=epsilon_aij, eta^a_{i4}=delta_ai.
    """
    x=sp.symbols('x0:4', real=True)
    rho=sp.symbols('rho',positive=True)
    radius=sp.expand(sum(t*t for t in x)+rho*rho)
    eta=[[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3): eta[a][i][j]=sp.LeviCivita(a,i,j)
            eta[a][i][3]=sp.KroneckerDelta(a,i)
            eta[a][3][i]=-sp.KroneckerDelta(a,i)
    A=[[2*sum(eta[a][m][j]*x[j] for j in range(4))/radius for m in range(4)] for a in range(3)]
    checked=0
    for a in range(3):
        for m in range(4):
            for n in range(m+1,4):
                f=sp.diff(A[a][n],x[m])-sp.diff(A[a][m],x[n])
                f+=sum(sp.LeviCivita(a,b,c)*A[b][m]*A[c][n] for b in range(3) for c in range(3))
                assert sp.cancel(f+4*rho*rho*eta[a][m][n]/radius**2)==0,(a,m,n)
                checked+=1
    return checked

def bpst_normalization_symbolic():
    x=sp.symbols('x',nonnegative=True)
    return sp.integrate(6*x/(1+x)**4,(x,0,sp.oo))

def g_dimension_exponents():
    """SI dimensions for c^a hbar^b curvature^d matching G: a=3,b=-1,d=-2."""
    a,b,d=sp.symbols('a b d')
    with_curvature=sp.solve([b+1,a+2*b-d-3,-a-b+2],[a,b,d],dict=True)
    without_curvature=sp.solve([b+1,a+2*b-3,-a-b+2],[a,b],dict=True)
    return {'with_curvature': with_curvature,'without_curvature': without_curvature}

def lifetime_from_gauge_scale(mx_gev,prefactor_years=8.0e34,scale_gev=1e16):
    """Illustrative dim-6 matching normalization; MUST NOT equate mx with gauge crossing automatically."""
    if mx_gev<=0: raise ValueError('positive MX required')
    return prefactor_years*(mx_gev/scale_gev)**4

def min_boson_scale(lifetime_bound_years=2.4e34,prefactor_years=8e34,scale_gev=1e16):
    return scale_gev*(lifetime_bound_years/prefactor_years)**0.25

def proton_audit(mu_gev, mx_equals_mu=True):
    """Conditional: ONLY when mu is also MX, unsuppressed dim-6 mode and adopted prefactor."""
    tau=lifetime_from_gauge_scale(mu_gev)
    bound=2.4e34
    return {'mu_GeV':mu_gev,'assumed_MX_GeV':mu_gev if mx_equals_mu else None,
            'reference_lower_bound_years_90pct':bound,
            'illustrative_tau_years':tau,'bound_to_model_ratio':bound/tau,
            'illustrative_MX_min_GeV':min_boson_scale(),
            'conditional_exclusion': bool(tau<bound) if mx_equals_mu else None,
            'status':'model-dependent; no proton lifetime predicted without full GUT amplitudes and MX'}

# Constructive nonuniqueness: S_gravity+SM + free hidden scalar M,
# whose vacuum phi=0 is a classical solution with T_phi=0 for M>0.
def hidden_scalar_vacuum(M, lam=0):
    if M<=0 or lam<0: raise ValueError('stable illustrative M>0, lambda>=0')
    f=sp.symbols('phi',real=True)
    V=sp.Rational(1,2)*sp.sympify(M)**2*f**2+sp.Rational(1,4)*sp.sympify(lam)*f**4
    return {'V_at_zero':sp.simplify(V.subs(f,0)),
            'dV_at_zero':sp.simplify(sp.diff(V,f).subs(f,0)),
            'mass_squared':sp.simplify(sp.diff(V,f,2).subs(f,0))}

def full_summary(unification_scale):
    mat=threshold_identifiability()
    p=proton_audit(unification_scale)
    return {'threshold_identifiability':mat,'proton_decay':p,
            'bpst_integral':str(bpst_normalization_symbolic()),
            'g_dimension_exponents':{k:[{str(x):str(y) for x,y in sol.items()} for sol in v] for k,v in g_dimension_exponents().items()},
            'source_claim':'ROOT V107 conditional one-loop toy, NOT complete GUT',
            'observed_new_physics':False,'UV_complete':False,'G_derived':False}
