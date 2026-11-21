"""ROOT V130: exact SU(5) representation/anomaly algebra and one-loop gauge RG.

This module verifies established mathematical structures, not a new unified field theory.
No external dependencies are required for calculations.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import exp, log, pi, sqrt
from typing import Sequence

MZ_GEV = 91.1876
# Illustrative MS-bar-like inputs at M_Z, NOT a correlated precision-fit dataset.
ALPHA_EM_INV_MZ = 127.955
SIN2_THETA_MZ = 0.23122
ALPHA_S_MZ = 0.1180
B_SM = (41/10, -19/6, -7)
B_MSSM = (33/5, 1, -3)  # Toy one-regime MSSM running from M_Z; no thresholds.

Y_FIVE = (F(-1,3), F(-1,3), F(-1,3), F(1,2), F(1,2))
FAMILY = {
    'Q': (6, F(1,6)),
    'u^c': (3, F(-2,3)),
    'd^c': (3, F(1,3)),
    'L': (2, F(-1,2)),
    'e^c': (1, F(1)),
}


def trace_square(xs: Sequence[F]) -> F:
    return sum((x*x for x in xs), F(0))


def trace_cube(xs: Sequence[F]) -> F:
    return sum((x*x*x for x in xs), F(0))


def traceless(xs: Sequence[F]) -> bool:
    return sum(xs, F(0)) == 0


def wedge2_weights(xs: Sequence[F]) -> tuple[F, ...]:
    return tuple(a+b for a,b in combinations(xs, 2))


def anti_weights(xs: Sequence[F]) -> tuple[F, ...]:
    return tuple(-a for a in xs)


def multiplet_hypercharges() -> dict[str, tuple[F, ...]]:
    """SU(5): 5bar=(d^c,L), 10=(Q,u^c,e^c)."""
    return {
        '5bar': anti_weights(Y_FIVE),
        '10': wedge2_weights(Y_FIVE),
    }


def cubic_anomaly_su5(xs: Sequence[F]) -> F:
    """Tr_10(X^3) + Tr_5bar(X^3), diagonal traceless X."""
    if len(xs) != 5 or not traceless(xs):
        raise ValueError('SU(5) Cartan generator requires 5 traceless entries')
    return trace_cube(wedge2_weights(xs)) + trace_cube(anti_weights(xs))


def su5_cubic_trace_identity(xs: Sequence[F]) -> tuple[F,F]:
    """For traceless diag X in SU(5): Tr_wedge2 X^3 = Tr_fund X^3."""
    if len(xs) != 5 or not traceless(xs):
        raise ValueError('invalid traceless SU(5) generator')
    return trace_cube(wedge2_weights(xs)), trace_cube(xs)


def hypercharge_normalization() -> F:
    """Tr_5(Y^2)=5/6, yielding T_Y=sqrt(3/5)Y."""
    return trace_square(Y_FIVE)


def family_anomalies(family: dict[str, tuple[int,F]] | None = None) -> dict[str,F]:
    f = FAMILY if family is None else family
    q, u, d, l, e = (f[x][1] for x in ('Q','u^c','d^c','L','e^c'))
    return {
        'SU3_SU3_U1': 2*q+u+d,  # common Dynkin 1/2 omitted
        'SU2_SU2_U1': 3*q+l,    # common Dynkin 1/2 omitted
        'GRAV_GRAV_U1': sum((F(n)*y for n,y in f.values()), F(0)),
        'U1_CUBED': sum((F(n)*y*y*y for n,y in f.values()), F(0)),
        'SU2_WITTEN_PARITY': F(4%2), # 3 quark doublets + 1 lepton doublet
    }


def inverse_couplings(alpha_em_inv=ALPHA_EM_INV_MZ, sin2=SIN2_THETA_MZ, alpha_s=ALPHA_S_MZ) -> tuple[float,float,float]:
    if not 0 < sin2 < 1 or alpha_em_inv <= 0 or alpha_s <= 0:
        raise ValueError('invalid input couplings')
    return (3/5*(1-sin2)*alpha_em_inv, sin2*alpha_em_inv, 1/alpha_s)


def alpha_inv_at(mu_gev: float, a0: Sequence[float], b: Sequence[float], mu0_gev=MZ_GEV) -> tuple[float,...]:
    if mu_gev <= 0 or mu0_gev <= 0 or len(a0)!=len(b):
        raise ValueError('invalid scale or beta vector')
    t=log(mu_gev/mu0_gev)
    return tuple(a-bi/(2*pi)*t for a,bi in zip(a0,b))


def crossing_log(i: int, j: int, a0: Sequence[float], b: Sequence[float]) -> float:
    if i==j or b[i]==b[j]:
        raise ValueError('parallel or same coupling')
    return 2*pi*(a0[i]-a0[j])/(b[i]-b[j])


def crossing_scale(i: int, j: int, a0: Sequence[float], b: Sequence[float], mu0_gev=MZ_GEV) -> float:
    return mu0_gev*exp(crossing_log(i,j,a0,b))


def unification_determinant(a0: Sequence[float], b: Sequence[float]) -> float:
    """Zero iff all 3 inverse-coupling lines intersect in one point if b_i distinct."""
    if len(a0)!=3 or len(b)!=3:
        raise ValueError('three inputs required')
    return (a0[0]-a0[1])*(b[1]-b[2])-(a0[1]-a0[2])*(b[0]-b[1])


def alpha_s_required_for_unification(alpha_em_inv=ALPHA_EM_INV_MZ, sin2=SIN2_THETA_MZ, b=B_SM) -> float:
    a1,a2,_=inverse_couplings(alpha_em_inv,sin2,0.1180)
    t=crossing_log(0,1,(a1,a2,1.0),b)
    aunified=a1-b[0]*t/(2*pi)
    a3needed=aunified+b[2]*t/(2*pi)
    if a3needed <= 0:
        raise ValueError('unphysical implied alpha_s')
    return 1/a3needed


def best_fit_log_scale(a0: Sequence[float], b: Sequence[float]) -> float:
    """Minimize unweighted sum of squared deviations of inverse couplings."""
    am=sum(a0)/len(a0); bm=sum(b)/len(b)
    numerator=sum((ai-am)*(bi-bm) for ai,bi in zip(a0,b))
    denominator=sum((bi-bm)**2 for bi in b)
    if denominator==0:
        raise ValueError('degenerate beta functions')
    return 2*pi*numerator/denominator


def best_fit_spread(a0: Sequence[float], b: Sequence[float], mu0=MZ_GEV) -> dict[str,float]:
    t=best_fit_log_scale(a0,b)
    ai=[a-bi*t/(2*pi) for a,bi in zip(a0,b)]
    mean=sum(ai)/len(ai)
    return {'ln_mu_over_MZ': t, 'scale_GeV': mu0*exp(t),
            'inv_alpha_max_minus_min': max(ai)-min(ai),
            'rms_inv_alpha':sqrt(sum((v-mean)**2 for v in ai)/len(ai))}


def beta_differences_required(target_gev: float, a0: Sequence[float], mu0_gev=MZ_GEV) -> tuple[float,float]:
    t=log(target_gev/mu0_gev)
    if t == 0: raise ValueError('target same as reference')
    return (2*pi*(a0[0]-a0[1])/t, 2*pi*(a0[1]-a0[2])/t)


def compute_summary() -> dict:
    a0 = inverse_couplings()
    all_crossings = lambda b:{'12':crossing_scale(0,1,a0,b),'13':crossing_scale(0,2,a0,b),'23':crossing_scale(1,2,a0,b)}
    t12=crossing_log(0,1,a0,B_SM)
    at12=tuple(ai-bi*t12/(2*pi) for ai,bi in zip(a0,B_SM))
    req=beta_differences_required(1e16,a0)
    return {
        'input_MZ_GeV':MZ_GEV,'input_alpha_em_inv':ALPHA_EM_INV_MZ,
        'input_sin2_MSbar_like':SIN2_THETA_MZ,'input_alpha_s':ALPHA_S_MZ,
        'inverse_couplings_at_MZ':a0,
        'hypercharge_traceY2':str(hypercharge_normalization()),
        'su5_one_generation_anomalies':{k:str(v) for k,v in family_anomalies().items()},
        'SU5_cubic_example':str(cubic_anomaly_su5(tuple(map(F,[1,1,1,1,-4])))),
        'SM_beta':B_SM,'SM_crossings_GeV':all_crossings(B_SM),
        'SM_determinant':unification_determinant(a0,B_SM),
        'SM_inv_alpha_at_12_crossing':at12,
        'SM_12_vs_3_residual_inv_alpha':at12[2]-at12[0],
        'SM_alpha_s_required_for_exact_one_loop_unification':alpha_s_required_for_unification(),
        'SM_bestfit':best_fit_spread(a0,B_SM),
        'MSSM_toy_beta':B_MSSM,'MSSM_toy_crossings_GeV':all_crossings(B_MSSM),
        'MSSM_toy_determinant':unification_determinant(a0,B_MSSM),
        'MSSM_toy_bestfit':best_fit_spread(a0,B_MSSM),
        'beta_differences_required_at_1e16_GeV':req,
        'difference_from_SM_b12_b23':(req[0]-(B_SM[0]-B_SM[1]),req[1]-(B_SM[1]-B_SM[2]))
    }
