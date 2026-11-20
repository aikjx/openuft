"""ROOT V107: conditional hypercharge rigidity, vectorlike SU5 thresholds,
    and dimensional obstruction for characteristic four-forms.
    All numerical inputs are explicitly illustrative (MSbar-ish MZ benchmark).
    No claim of a new observed force or completed quantum/gravity unification.
"""
from __future__ import annotations
from fractions import Fraction as Q
from dataclasses import dataclass
import math
import sympy as sp
import mpmath as mp

B = (Q(41,10), Q(-19,6), Q(-7))
DB_TRIPLET = (Q(4,15),Q(0),Q(2,3)) # Dirac (3,1,-1/3) + conjugate
DB_DOUBLET = (Q(2,5),Q(2,3),Q(0)) # Dirac (1,2,+1/2) + conjugate
D_BOTH = tuple(x+y for x,y in zip(DB_TRIPLET,DB_DOUBLET))
W = (B[1]-B[2], B[2]-B[0], B[0]-B[1])
K_TRIPLET = sum((a*b for a,b in zip(W,DB_TRIPLET)),Q(0))
K_DOUBLET = sum((a*b for a,b in zip(W,DB_DOUBLET)),Q(0))

@dataclass(frozen=True)
class Benchmark:
    m_z: float = 91.1876
    alpha_em_inv: float = 127.930
    sin2_w: float = 0.23122
    alpha_s: float = 0.1180
    planck_energy: float = 1.22089e19 # conventional Planck energy GeV (G input)

    def initial_inverse(self, prec=50):
        mp.mp.dps=prec
        ae=mp.mpf(str(self.alpha_em_inv)); s=mp.mpf(str(self.sin2_w))
        a_s=mp.mpf(str(self.alpha_s))
        assert 0<s<1 and a_s>0
        return (mp.mpf(3)/5*(1-s)*ae,s*ae,1/a_s)


def mfrac(x):
    if isinstance(x, Q): return mp.mpf(x.numerator)/x.denominator
    return mp.mpf(str(x))


def inv_invariant(a):
    return sum(mfrac(w)*x for w,x in zip(W,a))


def split_required_log_ratio(n_pairs:int, bench=Benchmark(),prec=70):
    if not isinstance(n_pairs,int) or n_pairs<=0: raise ValueError('n_pairs must positive integer')
    mp.mp.dps=prec
    I=inv_invariant(bench.initial_inverse(prec))
    return -2*mp.pi*I/(n_pairs*mfrac(K_TRIPLET))


def required_ratio(n_pairs:int, bench=Benchmark(),prec=70):
    return mp.exp(split_required_log_ratio(n_pairs,bench,prec))


def minimum_pair_count_below_planck(bench=Benchmark(),prec=70):
    # Necessary condition only; all thresholds assumed [MZ, MPl] and <= common matching scale.
    mp.mp.dps=prec
    Lmax=mp.log(mfrac(bench.planck_energy)/mfrac(bench.m_z))
    Nmin=math.ceil(float(split_required_log_ratio(1,bench,prec)/Lmax))
    return Nmin


def flow_at_mu(mu,*,n_pairs=0,m_doublet=1000.,m_triplet=1e12,bench=Benchmark(),prec=70):
    """One-loop decoupling with step-function thresholds, *no* unknown matching terms.
    For each Dirac vectorlike 5+5bar, one doublet & one triplet Dirac field.
    Threshold scale uses effective theory. No precision-data claim.
    """
    mp.mp.dps=prec
    mu=mfrac(mu); mz=mfrac(bench.m_z)
    if mu<mz or n_pairs<0: raise ValueError('invalid mu or pair count')
    a0=bench.initial_inverse(prec)
    l=mp.log(mu/mz)
    def th(mass):
        mass=mfrac(mass)
        if mass<mz: raise ValueError('threshold below MZ not in this model')
        return max(mp.mpf('0'),mp.log(mu/mass))
    ld=th(m_doublet);lt=th(m_triplet)
    return tuple(a0[i]-(mfrac(B[i])*l+n_pairs*(mfrac(DB_DOUBLET[i])*ld+mfrac(DB_TRIPLET[i])*lt))/(2*mp.pi) for i in range(3))


def common_scale(n_pairs:int,m_doublet,bench=Benchmark(),prec=75):
    """Solve 1-2 crossing with split threshold ratio fixed by I=0; validate order explicitly."""
    mp.mp.dps=prec
    mz=mfrac(bench.m_z)
    md=mfrac(m_doublet)
    log_ratio=split_required_log_ratio(n_pairs,bench,prec)
    mt=md*mp.exp(log_ratio)
    a=bench.initial_inverse(prec)
    # Above both thresholds, relative beta coefficients revert to SM ones.
    shifted_delta12=a[0]-a[1] + n_pairs*(mfrac(DB_TRIPLET[0])-mfrac(DB_TRIPLET[1]))*log_ratio/(2*mp.pi)
    log_mu=2*mp.pi*shifted_delta12/(mfrac(B[0])-mfrac(B[1]))
    mu=mz*mp.exp(log_mu)
    inv=flow_at_mu(mu,n_pairs=n_pairs,m_doublet=md,m_triplet=mt,bench=bench,prec=prec)
    return dict(m_doublet=md,m_triplet=mt,mu=mu,log_ratio=log_ratio,
                inv=inv,max_spread=max(inv)-min(inv),
                conditions_met=bool(mz<md<mt<mu<bench.planck_energy))


def hypercharge_anomalies(with_nu:bool=False):
    """SymPy anomaly formulas for physical (right-handed) charges u,d,e,nu.
    q,l are left-doublet charges. Left-handed conjugate RH singlets enter with minus.
    """
    q,l,h=sp.symbols('q l h', real=True)
    u,d,e=q+h,q-h,l-h
    nu=l+h
    a2=3*q+l
    a3=sp.expand(6*q**3-3*u**3-3*d**3+2*l**3-e**3-(nu**3 if with_nu else 0))
    agr=sp.expand(6*q-3*u-3*d+2*l-e-(nu if with_nu else 0))
    a32=sp.simplify(2*q-u-d)
    return {'q':q,'l':l,'h':h,'u':u,'d':d,'e':e,'nu':nu,
            'A_SU2_SU2_U1':a2,'A_U1_3':a3,'A_gravity_gravity_U1':agr,'A_SU3_SU3_U1':a32}


def verify_hypercharge():
    n=hypercharge_anomalies(False)
    q,l,h=n['q'],n['l'],n['h']
    sub={l:-3*q,h:3*q}
    assert sp.simplify(n['A_U1_3'].subs(sub))==0
    assert sp.simplify(n['A_gravity_gravity_U1'].subs(sub))==0
    assert sp.simplify(n['A_SU2_SU2_U1'].subs(sub))==0
    r=hypercharge_anomalies(True)
    red={l:-3*q}
    assert sp.simplify(r['A_U1_3'].subs(red))==0
    assert sp.simplify(r['A_gravity_gravity_U1'].subs(red))==0
    assert sp.simplify(r['A_SU2_SU2_U1'].subs(red))==0
    assert sp.simplify(n['A_U1_3'].subs({l:-3*q})-(h-3*q)**3)==0
    # normalized h=1/2, q=(1/6 + x/3), yields Y=YSM+x(B-L).
    x=sp.Symbol('x', real=True)
    subs={h:sp.Rational(1,2),q:sp.Rational(1,6)+x/3,l:-sp.Rational(1,2)-x}
    expected=(sp.Rational(1,6)+x/3,sp.Rational(2,3)+x/3,-sp.Rational(1,3)+x/3,
              -sp.Rational(1,2)-x,-1-x,-x)
    vals=tuple(sp.simplify(r[k].subs(subs)) for k in ('q','u','d','l','e','nu'))
    assert all(sp.simplify(a-b)==0 for a,b in zip(vals,expected))
    return dict(minimal_ratios=['1','4','-2','-3','-6','3'],
                no_nu_cubic_factor=str(sp.factor(n['A_U1_3'].subs({l:-3*q}))),
                with_nu_residual='Y = Y_SM + x(B-L) with x free; Majorana nu_R requires x=0 in this setup')


def fourform_rank_obstruction():
    """All F components on k<=3 internal scalar directions give identically zero F wedge F.
    For k=4 exhibit an SU2 Cartan-valued local curvature with nonzero trace F wedge F.
    Note: a local density is NOT an instanton or quantized global topological charge.
    """
    x,y,z,w=sp.symbols('x y z w')
    F4={(0,1):sp.Integer(1),(2,3):sp.Integer(1)}
    def pfaffian4(f):
        return sp.expand(2*(f.get((0,1),0)*f.get((2,3),0)
                            -f.get((0,2),0)*f.get((1,3),0)
                            +f.get((0,3),0)*f.get((1,2),0)))
    assert pfaffian4(F4)==2
    # X=i*sigma3/2: Tr(X^2)=-1/2 => Tr(F^F) coefficient=-1.
    sigma3=sp.diag(1,-1); X=sp.I*sigma3/2
    trval=sp.simplify(sp.trace(X*X)*pfaffian4(F4))
    assert trval==-1
    f3={(0,1):x,(0,2):y,(1,2):z}
    assert pfaffian4(f3)==0
    return {'max_internal_rank_with_zero_local_4form':3,'local_trace_FwedgeF_example':str(trval),
            'qualifier':'nonzero local density does not imply nonzero integer instanton number'}


def summary(bench=Benchmark(),prec=75):
    mp.mp.dps=prec
    a=bench.initial_inverse(prec)
    I=inv_invariant(a)
    log_r1=split_required_log_ratio(1,bench,prec)
    log_r2=split_required_log_ratio(2,bench,prec)
    toy=common_scale(2,1000,bench,prec)
    return dict(benchmark={'mz_GeV':bench.m_z,'alpha_em_inv_MZ':bench.alpha_em_inv,
                           'sin2W_MZ':bench.sin2_w,'alpha_s_MZ':bench.alpha_s},
        sm_inverse_at_MZ=[mp.nstr(t,20) for t in a],
        one_loop_invariant=mp.nstr(I,30),
        delta_b_triplet=[str(q) for q in DB_TRIPLET],
        delta_b_doublet=[str(q) for q in DB_DOUBLET],
        delta_b_complete=[str(q) for q in D_BOTH],
        K_triplet=str(K_TRIPLET),
        K_doublet=str(K_DOUBLET),
        one_pair_log_mass_ratio_required=mp.nstr(log_r1,30),
        one_pair_mass_ratio_required=mp.nstr(mp.exp(log_r1),30),
        maximum_log_ratio_MZ_to_Planck=mp.nstr(mp.log(mp.mpf(str(bench.planck_energy))/mp.mpf(str(bench.m_z))),30),
        minimum_number_of_split_pairs_necessary_below_planck=minimum_pair_count_below_planck(bench,prec),
        two_pairs_toy={'m_doublet_GeV':mp.nstr(toy['m_doublet'],30),
                       'm_triplet_GeV':mp.nstr(toy['m_triplet'],30),
                       'mu_unify_GeV':mp.nstr(toy['mu'],30),
                       'inverse_couplings_at_mu':[mp.nstr(t,30) for t in toy['inv']],
                       'inverse_spread':mp.nstr(toy['max_spread'],12),
                       'ordering_ok':toy['conditions_met']},
        hypercharge=verify_hypercharge(),phase_rank=fourform_rank_obstruction(),
        evidence={'model':'one-loop, step thresholds, illustrative inputs','new_physics_observed':False,
                  'G_derived':False,'four_forces_unified':False})
