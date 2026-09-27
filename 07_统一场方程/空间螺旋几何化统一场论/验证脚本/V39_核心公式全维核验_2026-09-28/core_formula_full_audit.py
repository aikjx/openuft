# -*- coding: utf-8 -*-
"""TUFT core-formula full-dimensional audit (reading face V3_9, round of 2026-09-28).

Independent instrument for every formula of 00_核心理论体系总纲.md 体系一..十:
  layer S1  sympy Frenet-Serret derivation of kappa/tau from R(theta) + the ell identity
  layer S2  SI exponent-vector dimension algebra (own implementation, no sympy assumptions)
  layer S3  mpmath 50 dp numeric layer (N_A/N_B, four-force table, alpha closure, primes)
It reproduces the standing verdicts of 01A_附录_体系不自洽点专项复盘.md, whose ledger is X1-X5 plus
X8-X15 (X6 and X7 do not appear in that document at all), and adds the items that ledger does not
cover (N1 theta conflation, N2 asin-vs-sin in 01A 3.2 itself, N3 kappa_drive, N4 G_eff(E),
N5 apparent-strength factorization, N7 alpha anchor-vintage dependence of N at its own printed
precision).  N6 (round(N_A) = 18917 prime vs 18907 = 7*37*73 composite) is NOT net-new: 01A
already registers it as X12, so N6 is a reproduction and is labelled as such in the face.
Each identity prints a mutated control that must be nonzero.
"""
import json
import os
from datetime import datetime

import mpmath as mp
import sympy as sp

mp.mp.dps = 50            # must precede every mp.mpf / 1/x below or the declared dps is a lie

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)                      # 验证脚本/
SERIES = os.path.dirname(PARENT)                    # 空间螺旋几何化统一场论/
OUT = os.path.join(SERIES, "V3_9_core_formula_checks.json")

# external anchors (declared inputs, not derived here)
# primary pair: alpha^-1 = 137.035999177(21); its own reciprocal alpha = 7.2973525643(11)e-3
# (source consulted 2026-09-28: the fine-structure-constant article lists this pair under the
#  latest CODATA dataset).  The parenthetical (21) is written at the last two digits of a value
# whose last digit sits at 1e-9, so u = 0.000000021 = 2.1e-8 ABSOLUTE, i.e. u/alpha^-1 = 1.53e-10
# RELATIVE.  This instrument's first build used 2.1e-7 there and quoted 1.6e-10 in one place
# only; both sigma-normalised readings of this face are therefore a factor 10 too small and are
# corrected below -- see meta.instrument_history.
ALPHA_INV = mp.mpf("137.035999177")      # primary inverse anchor
ALPHA = 1 / ALPHA_INV                    # = 7.2973525643314e-3 at dps=50
# secondary anchor: the number 01A 3.2 itself prints and labels "CODATA 2018".
# It is NOT the reciprocal of the primary anchor (relative gap ~6.8e-10, i.e. >4 sigma of the
# 1.53e-10 relative uncertainty below), so the two anchors belong to different vintages -> N7.
ALPHA_01A = mp.mpf("7.2973525693e-3")
ALPHA_INV_OF_01A = 1 / ALPHA_01A         # = 137.0359990837, the row 01A prints as "1/asin(alpha)"
C = mp.mpf("299792458")                  # exact
HBAR = mp.mpf("1.054571817e-34")
E_CH = mp.mpf("1.602176634e-19")         # exact
EPS0 = mp.mpf("8.8541878128e-12")
MU0 = mp.mpf("1.2566370614e-6")
GG = mp.mpf("6.67430e-11")
M_E = mp.mpf("9.1093837015e-31")
M_P = mp.mpf("1.67262192369e-27")
ALPHA_INV_U = mp.mpf("2.1e-8")           # 1-sigma ABSOLUTE on the primary inverse anchor, from (21)
ALPHA_REL_U = ALPHA_INV_U / ALPHA_INV    # = 1.5324e-10; the only 1-sigma this instrument uses

R = {"checks": {}, "meta": {}}


def rec(name, **kw):
    R["checks"][name] = kw


# ---------------------------------------------------------------- S1 geometry
th, rho, b = sp.symbols("theta rho b", positive=True)
Rv = sp.Matrix([rho * sp.cos(th), rho * sp.sin(th), b * th])
# curvature/torsion from the standard parameter-invariant formulas, parameter = theta
d1 = Rv.diff(th)
d2 = Rv.diff(th, 2)
d3 = Rv.diff(th, 3)
k1 = sp.sqrt((d1.T * d1)[0])
cross12 = d1.cross(d2)
kappa = sp.simplify(sp.sqrt((cross12.T * cross12)[0]) / (k1**3))
tau = sp.simplify(cross12.dot(d3) / (cross12.T * cross12)[0])
kap_doc = rho / (rho**2 + b**2)
tau_doc = b / (rho**2 + b**2)
res_k = sp.simplify(kappa - kap_doc)
res_t = sp.simplify(tau - tau_doc)
mut_k = sp.simplify(kappa - rho / (rho**2 - b**2))          # mutated denominator, must be nonzero
mut_t = sp.simplify(tau + tau_doc)                          # sign flip, must be nonzero
ell = sp.sqrt(rho**2 + b**2)
res_ell = sp.simplify(ell - 1 / sp.sqrt(kap_doc**2 + tau_doc**2))
mut_ell = sp.simplify(ell - 1 / (kap_doc**2 + tau_doc**2))   # missing sqrt, must be nonzero
rec("S1_frenet_helix",
    kappa_from_param=str(kappa), tau_from_param=str(tau),
    doc_kappa=str(kap_doc), doc_tau=str(tau_doc),
    resid_kappa=res_k, resid_tau=res_t,
    mutant_resid_kappa=sp.simplify(mut_k), mutant_resid_tau=sp.simplify(mut_t),
    ell_identity_resid=res_ell, mutant_ell_resid=sp.simplify(mut_ell),
    note="kappa=rho/(rho^2+b^2) and tau=b/(rho^2+b^2) reproduced from first principles")

# N1: theta is used for TWO different angles
#   体系一 line 25 chain: cos^2 th + sin^2 th = rho^2/ell^2 + b^2/ell^2
#   rho/ell is constant along the helix, cos(theta) is not => the middle equality
#   only holds if theta denotes the pitch angle, not the spiral parameter.
rho_over_ell = sp.simplify(rho / ell)
d_theta_dependence = sp.simplify(sp.diff(rho_over_ell, th))          # must be 0
cos_theta_d = sp.simplify(sp.diff(sp.cos(th), th))                   # must be nonzero
pitch_angle = sp.atan(b / rho)                                        # the angle actually meant
rec("N1_theta_conflation",
    resid_d_of_rho_over_ell_wrt_spiral_parameter=d_theta_dependence,
    resid_d_of_cos_theta_wrt_spiral_parameter=cos_theta_d,
    pitch_angle_from_b_over_rho=str(sp.simplify(pitch_angle)),
    cos_of_pitch=str(sp.simplify(sp.cos(pitch_angle))),
    resid_cos_pitch_minus_rho_over_ell=sp.simplify(sp.cos(pitch_angle) - rho_over_ell),
    tan_of_pitch=str(sp.simplify(sp.tan(pitch_angle))),
    verdict_note="rho/ell = cos(pitch angle) identically; writing it as cos^2(theta) with the "
                 "spiral parameter theta of 体系一 line 14 is a symbol reuse, verdict FAIL as written")

# alpha = tau/kappa = b/rho ; N_twist closed form, with alpha as an INDEPENDENT symbol so the
# substitution b = alpha*rho is not a no-op
A = sp.symbols("alpha", positive=True)
alpha_sym = sp.simplify(tau_doc / kap_doc)
res_alpha = sp.simplify(alpha_sym - b / rho)
ntw = b**2 / (rho**2 + b**2)
ntw_in_alpha = sp.simplify(ntw.subs(b, A * rho))                    # b = alpha*rho
res_ntw = sp.simplify(ntw_in_alpha - A**2 / (1 + A**2))
mut_ntw = sp.simplify(ntw_in_alpha - A / (1 + A))
ntw_true = ALPHA ** 2 / (1 + ALPHA ** 2)
ntw_doc_claim = mp.mpf(137) / 138                                    # 体系二: N_twist = N/(N+1)
rec("S2_alpha_and_ntwist",
    resid_tau_over_kappa_minus_b_over_rho=res_alpha,
    N_twist_in_alpha=str(ntw_in_alpha),
    resid_ntw_minus_alpha2_over_1_plus_alpha2=res_ntw,
    mutant_ntw_resid=mut_ntw,
    N_twist_recomputed_from_alpha=mp.nstr(ntw_true, 12),
    N_twist_doc_claimed_N_over_N_plus_1=mp.nstr(ntw_doc_claim, 12),
    doc_claim_over_recomputed=mp.nstr(ntw_doc_claim / ntw_true, 10),
    tan_theta_implied_by_doc_claim=mp.nstr(mp.sqrt(ntw_doc_claim / (1 - ntw_doc_claim)), 10),
    tan_theta_of_theory=mp.nstr(ALPHA, 12),
    verdict_note_reproduces_X5="N_twist = b^2/(rho^2+b^2) = alpha^2/(1+alpha^2) ~ 5.3e-5, while the "
            "same section asserts N_twist = 137/138 ~ 0.9928; reading the second as the first gives "
            "tan(theta) = sqrt(137) ~ 11.7 vs the theory's own tan(theta) = alpha = 1/137 -> the two "
            "statements are mutually exclusive (X5 confirmed)",
    note="alpha = tau/kappa = b/rho confirmed; N_twist = b^2/(rho^2+b^2) = alpha^2/(1+alpha^2)")

# ---------------------------------------------------------------- S2 dimension algebra
BASES = ("M", "L", "T", "I")


def dim(**kw):
    d = dict.fromkeys(BASES, 0)
    for k, v in kw.items():
        d[k] = d.get(k, 0) + v
    return d


def fmt(d):
    return "*".join("%s^%g" % (k, d[k]) for k in BASES if d[k]) or "dimensionless"


D_LEN, D_TIME, D_MASS = dim(L=1), dim(T=1), dim(M=1)
D_HBAR = dim(M=1, L=2, T=-1)
D_C = dim(L=1, T=-1)
D_MU0 = dim(M=1, L=1, T=-2, I=-2)
D_EPS0 = dim(M=-1, L=-3, T=4, I=2)
D_G = dim(M=-1, L=3, T=-2)
D_FORCE = dim(M=1, L=1, T=-2)
D_FREQ = dim(T=-1)
D_CHARGE = dim(T=1, I=1)
D_ENERGY = dim(M=1, L=2, T=-2)

rho_G_dim = {x: D_G[x] - D_MU0[x] - 2 * D_C[x] for x in BASES}      # rho^2 = G/(alpha^2 mu0 c^2)
rho_G_dim = {x: rho_G_dim[x] / 2 for x in BASES}
omega_doc1 = {x: D_C[x] - D_LEN[x] for x in BASES}                  # omega = c/ell
omega_doc2 = {x: D_C[x] - D_LEN[x] for x in BASES}                  # c (k^2+t^2)/k -> c/rho
kappa_drive = {x: D_LEN[x] + 2 * D_FREQ[x] - 2 * D_C[x] for x in BASES}     # rho w^2 / c^2
A_expr = {x: D_HBAR[x] + 2 * D_FREQ[x] - D_MASS[x] - D_C[x] for x in BASES}
A_expr["L"] += 1                                                    # x kappa/(k^2+t^2) = one length
Fmax_expr = {x: 5 * D_C[x] - D_HBAR[x] - 2 * D_FREQ[x] + 2 * D_LEN[x] for x in BASES}
F5_expr = {x: D_HBAR[x] - 2 * D_TIME[x] for x in BASES}
# G E^2/(hbar c^5): the dimensionless completion the doc's 1/E^2 statement would need
geff_closure = {x: D_G[x] + 2 * D_ENERGY[x] - D_HBAR[x] - 5 * D_C[x] for x in BASES}
e2_expr = {x: D_EPS0[x] + D_HBAR[x] + D_C[x] for x in BASES}
em0mu0 = {x: D_EPS0[x] + D_MU0[x] for x in BASES}
inv_c2 = {x: -2 * D_C[x] for x in BASES}
m_expr = {x: D_HBAR[x] - D_C[x] - D_LEN[x] for x in BASES}           # hbar/(c*rho_C)
p_expr = {x: D_HBAR[x] - D_LEN[x] for x in BASES}                    # hbar/ell
planck = {x: D_HBAR[x] + D_C[x] - 2 * D_MASS[x] for x in BASES}      # hbar c / m_P^2

rec("S2_dimension_sweep",
    unit_system="SI base exponents over M,L,T,I (current as base I)",
    G_equals_alpha2_mu0_c2_rho2={"lhs": fmt(D_G), "rhs_with_rho_as_length": fmt(dim(M=1, L=5, T=-4, I=-2)),
                                 "required_rho_dim": fmt(rho_G_dim), "verdict": "FAIL",
                                 "already_registered_as": "X8"},
    omega_c_over_ell_vs_c_k2t2_over_k={"omega_c_over_ell": fmt(omega_doc1),
                                        "omega_c_times_k2t2_over_k": fmt(omega_doc2),
                                        "note": "both are 1/T; the mismatch is geometric not dimensional "
                                                "(c/rho vs c/ell) -> X10",
                                        "verdict": "BOUNDARY", "already_registered_as": "X10"},
    kappa_drive_rho_omega2_over_c2={"dims": fmt(kappa_drive), "expected": fmt(dim(L=-1)),
                                    "verdict": "PASS", "already_registered_as": "not in the 01A ledger"},
    A_hbar_omega2_over_mc_times_kappa={"dims": fmt(A_expr), "label_in_doc": "引力场的频率表达式",
                                       "force_dims": fmt(D_FORCE), "freq_dims": fmt(D_FREQ),
                                       "verdict": "FAIL", "already_registered_as": "X14"},
    F_G_max={"dims": fmt(Fmax_expr), "force_dims": fmt(D_FORCE), "verdict": "FAIL",
             "already_registered_as": "X15"},
    F5_hbar_over2_domega_dt={"dims": fmt(F5_expr), "force_dims": fmt(D_FORCE),
                             "power_dims": fmt(dim(M=1, L=2, T=-3)), "verdict": "FAIL",
                             "already_registered_as": "X11"},
    G_eff_propto_1_over_E2={"lhs_dims": fmt(D_G), "closure_G_E2_over_hbar_c5_dims": fmt(geff_closure),
                            "verdict": "FAIL as written",
                            "note": "1/E^2 needs the pair of hbar,c factors shown in "
                                    "closure_G_E2_over_hbar_c5_dims to be a statement at all",
                            "already_registered_as": "not in the 01A ledger"},
    e2_equals_4pi_eps0_hbar_c_alpha={"dims": fmt(e2_expr), "charge_dims": fmt(D_CHARGE),
                                     "verdict": "PASS_but_definition_of_alpha"},
    eps0_mu0_equals_1_over_c2={"lhs": fmt(em0mu0), "rhs": fmt(inv_c2), "verdict": "PASS_in_SI"},
    m_hbar_over_c_rhoC={"dims": fmt(m_expr), "verdict": "PASS_but_definition_of_rho_C"},
    p_hbar_over_ell={"dims": fmt(p_expr), "verdict": "PASS"},
    G_hbar_c_over_mP2={"dims": fmt(planck), "verdict": "PASS_but_definition_of_mP"})

# ---------------------------------------------------------------- S3 numeric layer
inv_a = ALPHA_INV
a2_inv = inv_a ** 2
N_A = a2_inv / (1 - ALPHA)
N_B = a2_inv + inv_a + 1 + ALPHA
N_B_rounded_alpha = mp.mpf(137) ** 2 + 137 + 1 + mp.mpf(1) / 137
N_A_rounded_alpha = (mp.mpf(137) ** 2) / (1 - mp.mpf(1) / 137)
closed_AB = ALPHA ** 2 / (1 - ALPHA)
rec("S3_N_definitions",
    alpha_inv_used=mp.nstr(inv_a, 12),
    N_A_at_primary_anchor=mp.nstr(N_A, 14), N_B_at_primary_anchor=mp.nstr(N_B, 14),
    N_A_minus_N_B=mp.nstr(N_A - N_B, 8), closed_form_alpha2_over_1_minus_alpha=mp.nstr(closed_AB, 8),
    N_A_at_alpha_137=mp.nstr(N_A_rounded_alpha, 12), N_B_at_alpha_137=mp.nstr(N_B_rounded_alpha, 12),
    doc_printed={"A": "18916.90839", "B": "18907"},
    verdict="A and B agree to 2.8e-9 relative at fixed alpha; the printed 18907 is B evaluated at "
            "alpha=1/137 -> reproduces X1/X13 (rounding, not a definitional conflict)")

# four-force table of 体系三
Fg = a2_inv / N_B
Fs = inv_a / N_B
Fw = 1 / N_B
Fe = ALPHA / N_B
printed = [mp.mpf("0.9927"), mp.mpf("0.00725"), mp.mpf("5.29e-5"), mp.mpf("3.86e-7")]
PRINTED_SF = [4, 3, 3, 3]                     # significant digits the doc actually prints
A137 = mp.mpf(1) / 137
N137 = A137 ** -2 + A137 ** -1 + 1 + A137
cols137 = [A137 ** -2 / N137, A137 ** -1 / N137, 1 / N137, A137 / N137]
cols_anchor = [Fg, Fs, Fw, Fe]
intensity137 = [A137 ** -2, A137 ** -1, mp.mpf(1), A137]
intensity_anchor = [a2_inv, inv_a, mp.mpf(1), ALPHA]
printed_intensity = [mp.mpf("18769"), mp.mpf("137"), mp.mpf("1"), mp.mpf("0.0073")]
INTENSITY_SF = [5, 3, 1, 2]


def half_ulp(p, sf):
    """half of one unit in the last printed digit of p (p printed with sf significant digits)"""
    return mp.mpf(10) ** (mp.floor(mp.log(mp.fabs(p), 10)) - (sf - 1)) / 2


def reproduce(vals, ps, sfs, keys):
    rows = {}
    for k, v, p, sf in zip(keys, vals, ps, sfs):
        hu = half_ulp(p, sf)
        rows[k] = {"printed": mp.nstr(p, sf), "recomputed": mp.nstr(v, 12),
                   "gap": mp.nstr(v - p, 6), "half_ulp_of_printed": mp.nstr(hu, 3),
                   "reachable_by_rounding": bool(abs(v - p) <= hu)}
    return rows


KEYS = ("G", "S", "W", "E")
rep_anchor = reproduce(cols_anchor, printed, PRINTED_SF, KEYS)
rep_137 = reproduce(cols137, printed, PRINTED_SF, KEYS)
rep_int_anchor = reproduce(intensity_anchor, printed_intensity, INTENSITY_SF, KEYS)
rep_int_137 = reproduce(intensity137, printed_intensity, INTENSITY_SF, KEYS)


def unreachable(rep):
    return [k for k in KEYS if not rep[k]["reachable_by_rounding"]]


rec("S3_four_force_table",
    F_hat_G=mp.nstr(Fg, 8), F_hat_S=mp.nstr(Fs, 8), F_hat_W=mp.nstr(Fw, 8), F_hat_E=mp.nstr(Fe, 10),
    doc_printed_columns={"G": "0.9927", "S": "0.00725", "W": "5.29e-5", "E": "3.86e-7"},
    normalized_at_primary_anchor=rep_anchor,
    normalized_at_alpha_1_over_137=rep_137,
    intensity_factor_at_primary_anchor=rep_int_anchor,
    intensity_factor_at_alpha_1_over_137=rep_int_137,
    not_reachable_normalized_anchor=unreachable(rep_anchor),
    not_reachable_normalized_137=unreachable(rep_137),
    not_reachable_intensity_anchor=unreachable(rep_int_anchor),
    not_reachable_intensity_137=unreachable(rep_int_137),
    sum_exact=mp.nstr(Fg + Fs + Fw + Fe, 12),
    sum_resid=mp.nstr(Fg + Fs + Fw + Fe - 1, 6),
    mutant_sum_without_last_column=mp.nstr(Fg + Fs + Fw - 1, 6),
    sum_of_printed_decimals=mp.nstr(sum(printed), 10),
    printed_minus_one=mp.nstr(sum(printed) - 1, 6),
    verdict="the four exact normalized strengths sum to 1 by construction (sum_resid, with the "
            "drop-one-column mutant beside it, so the sum is bookkeeping not physics). Judged "
            "against the doc's OWN printed precision (half a unit of the last stated digit): "
            "at alpha = 1/137 the unreachable normalized columns are %r and the unreachable "
            "intensity factors are %r; at the inverse-structure anchor they are %r and %r. "
            "Net-new (not in the 01A ledger): the printed 体系三 table is reproducible only under the "
            "truncated alpha, so its stated precision is a statement about the anchor choice, not "
            "about the arithmetic -- the same defect X1/X13 register for N, now visible in the "
            "force table. The four rounded columns overshoot 1 by 3.3e-6"
            % (unreachable(rep_137), unreachable(rep_int_137),
               unreachable(rep_anchor), unreachable(rep_int_anchor)))

# infinite-series closure of 体系七
n = sp.symbols("n", integer=True)
A_SP = sp.Float(mp.nstr(ALPHA, 45), 50)
series = mp.mpf(str(sp.N(sp.summation(A_SP ** n, (n, -2, sp.oo)), 45)))
rec("S3_series_closure",
    sum_alpha_n_from_minus2_to_infinity=mp.nstr(series, 14),
    equals_N_A_resid=mp.nstr(series - N_A, 6),
    mutant_missing_last_term=mp.nstr(series - N_A + ALPHA ** 2, 6),
    verdict="definition A IS the closed form of the 体系七 series; B is its 4-term truncation")

# N2: asin vs sin in the alpha closure (tests 01A section 3.2 itself)
asin_a = mp.asin(ALPHA)
sin_form_inverse = 1 / asin_a
doc_asin_printed = mp.mpf("7.29722e-03")
doc_inv_asin_printed = mp.mpf("137.03599908")
alpha_pred_doc_form = mp.sin(1 / (137 + mp.mpf("0.036")))
rec("N2_asin_vs_sin_closure",
    alpha=mp.nstr(ALPHA, 14),
    asin_of_alpha=mp.nstr(asin_a, 14),
    asin_gt_alpha=bool(asin_a > ALPHA),
    one_over_asin=mp.nstr(sin_form_inverse, 14),
    one_over_alpha=mp.nstr(inv_a, 14),
    delta_top_required_by_sin_form=mp.nstr(sin_form_inverse - 137, 12),
    delta_top_required_by_linear_form=mp.nstr(inv_a - 137, 12),
    doc_01A_printed={"asin_alpha": "7.29722e-03", "one_over_asin": "137.03599908",
                     "delta_top": "0.03599908", "verdict_mark": "数值一致"},
    # (a) is 01A's own printed row pair internally consistent?
    recip_of_doc_printed_asin=mp.nstr(1 / doc_asin_printed, 14),
    internal_gap_of_doc_rows=mp.nstr(1 / doc_asin_printed - doc_inv_asin_printed, 8),
    asin_of_01A_alpha=mp.nstr(mp.asin(ALPHA_01A), 14),
    # could row 2 of 01A 3.2 be sin(alpha) mislabelled as asin(alpha)? test that reading too
    sin_of_01A_alpha=mp.nstr(mp.sin(ALPHA_01A), 14),
    gap_row2_vs_sin_reading=mp.nstr(doc_asin_printed - mp.sin(ALPHA_01A), 8),
    gap_row2_vs_asin_reading=mp.nstr(doc_asin_printed - mp.asin(ALPHA_01A), 8),
    # is either reading reachable by rounding the printed 6-sf row 2?  price it, do not narrate it
    row2_printed_sf=6,
    row2_half_ulp=mp.nstr(half_ulp(doc_asin_printed, 6), 3),
    row2_sin_reading_in_half_ulps=mp.nstr(
        abs(doc_asin_printed - mp.sin(ALPHA_01A)) / half_ulp(doc_asin_printed, 6), 4),
    row2_asin_reading_in_half_ulps=mp.nstr(
        abs(doc_asin_printed - mp.asin(ALPHA_01A)) / half_ulp(doc_asin_printed, 6), 4),
    one_over_asin_of_01A_alpha=mp.nstr(1 / mp.asin(ALPHA_01A), 14),
    delta_top_sin_form_on_01A_anchor=mp.nstr(1 / mp.asin(ALPHA_01A) - 137, 12),
    delta_top_linear_form_on_01A_anchor=mp.nstr(ALPHA_INV_OF_01A - 137, 12),
    rel_error_of_doc_sin_form_on_01A_anchor=mp.nstr(
        (alpha_pred_doc_form - ALPHA_01A) / ALPHA_01A, 8),
    # (b) which anchor is 01A's "1/asin(alpha)" row actually equal to?
    equals_reciprocal_of_01A_alpha=mp.nstr(ALPHA_INV_OF_01A, 14),
    gap_doc_row_vs_reciprocal_of_01A_alpha=mp.nstr(doc_inv_asin_printed - ALPHA_INV_OF_01A, 8),
    gap_doc_row_vs_primary_anchor=mp.nstr(doc_inv_asin_printed - ALPHA_INV, 8),
    gap_of_printed_asin_vs_true_asin=mp.nstr(asin_a - doc_asin_printed, 8),
    gap_in_units_of_alpha_inv_sigma=mp.nstr(
        abs(sin_form_inverse - doc_inv_asin_printed) / ALPHA_INV_U, 8),
    alpha_pred_from_doc_sin_form=mp.nstr(alpha_pred_doc_form, 14),
    rel_error_of_doc_sin_form=mp.nstr((alpha_pred_doc_form - ALPHA) / ALPHA, 8),
    rel_error_of_linear_form=mp.nstr((mp.mpf(1) / (137 + mp.mpf("0.036")) - ALPHA) / ALPHA, 8),
    rel_error_of_linear_form_on_01A_anchor=mp.nstr(
        (mp.mpf(1) / (137 + mp.mpf("0.036")) - ALPHA_01A) / ALPHA_01A, 8),
    how_many_alpha_sigmas_off=mp.nstr(
        abs((alpha_pred_doc_form - ALPHA) / ALPHA) / (ALPHA_INV_U / inv_a), 8),
    verdict="asin(x) > x for x > 0, so a printed asin(alpha) = 7.29722e-03 BELOW the printed "
            "alpha = 7.2973525693e-03 is impossible on 01A's own anchor; and the row labelled "
            "1/asin(alpha) = 137.03599908 is the reciprocal of the alpha in the row above, not the "
            "reciprocal of its asin (reading the printed asin literally gives 137.03849, so the two "
            "printed rows are not even reciprocals of each other). Recomputed on 01A's own anchor: "
            "1/asin(alpha) = 137.03478, i.e. the sin form needs delta_top ~ 0.03478, not the ticked "
            "0.035999. Therefore 01A 3.2's 'delta_top ~ 0.036 数值一致 ✔' is not earned: as written, "
            "sin(1/(137+0.036)) misses alpha by the printed relative amount, "
            + mp.nstr(abs((alpha_pred_doc_form - ALPHA) / ALPHA) / (ALPHA_INV_U / inv_a), 6)
            + " times the 1-sigma relative precision of the primary anchor (u = 2.1e-8 absolute on "
            "137.035999177(21)).")

# N7: the two alpha anchors in circulation are not reciprocals of each other
N_A_01A = 1 / (ALPHA_01A ** 2 * (1 - ALPHA_01A))
N_B_01A = ALPHA_01A ** -2 + 1 / ALPHA_01A + 1 + ALPHA_01A
REL_ANCHOR_GAP = (ALPHA_01A - ALPHA) / ALPHA
DOC_NA = mp.mpf("18916.90839")          # 10 significant digits as printed
DOC_NB = mp.mpf("18907")                # 5 significant digits as printed
rec("N7_anchor_vintage",
    primary_alpha=mp.nstr(ALPHA, 14), primary_alpha_inv=mp.nstr(ALPHA_INV, 14),
    alpha_01A=mp.nstr(ALPHA_01A, 14), alpha_inv_of_01A=mp.nstr(ALPHA_INV_OF_01A, 14),
    rel_gap_between_anchors=mp.nstr(REL_ANCHOR_GAP, 6),
    rel_gap_in_units_of_primary_rel_sigma=mp.nstr(abs(REL_ANCHOR_GAP) / ALPHA_REL_U, 6),
    N_A_primary=mp.nstr(N_A, 14), N_A_01A_anchor=mp.nstr(N_A_01A, 14),
    N_A_shift=mp.nstr(N_A_01A - N_A, 6),
    N_B_shift=mp.nstr(N_B_01A - N_B, 6),
    F_hat_G_shift=mp.nstr((1 / ALPHA_01A ** 2) / N_B_01A - Fg, 6),
    doc_printed_N_A=mp.nstr(DOC_NA, 10),
    N_A_reachable_at_primary=reproduce([N_A], [DOC_NA], [10], ("N",))["N"],
    N_A_reachable_at_01A_anchor=reproduce([N_A_01A], [DOC_NA], [10], ("N",))["N"],
    N_B_reachable_at_primary=reproduce([N_B], [DOC_NB], [5], ("N",))["N"],
    N_B_reachable_at_1_over_137=reproduce([N_B_rounded_alpha], [DOC_NB], [5], ("N",))["N"],
    mutant_N_A_test_if_precision_read_as_6sf=reproduce([N_A], [DOC_NA], [6], ("N",))["N"],
    verdict="the anchor 01A 3.2 labels 'CODATA 2018' (alpha = 7.2973525693e-03) and the primary "
            "inverse anchor 137.035999177(21) are not reciprocals of one another: their relative "
            "gap and its size in units of the primary relative uncertainty are both printed above "
            "(~4 sigma apart), so they belong to different vintages and must not be mixed inside "
            "one derivation. Net-new (not in the 01A ledger): the two headline numbers of 体系三/十 are "
            "anchor-vintage dependent AT THEIR OWN PRINTED PRECISION -- the printed 18916.90839 is "
            "reachable by rounding under the 01A anchor but not under the primary one "
            "(N_A_reachable_*), and the printed 18907 for definition B is reachable only at "
            "alpha = 1/137, not at either anchor (N_B_reachable_*), i.e. X1's '18907 vs 18916.9' is "
            "not two definitions but one definition evaluated at two different alphas. The mutant "
            "row shows the test has teeth: read the doc's precision as 6 s.f. instead of 10 and the "
            "same comparison calls the primary anchor reachable.")

# N5: 体系九 factorization  apparent = normalized x coupling factor
alpha_G_p = GG * M_P ** 2 / (HBAR * C ** 3)
grav_em_ratio_pp = GG * M_P ** 2 / (E_CH ** 2 / (4 * mp.pi * EPS0))
needed_factor = mp.mpf("1e-36") / Fg
rec("N5_apparent_strength_factorization",
    gravitational_fine_structure_pp=mp.nstr(alpha_G_p, 8),
    G_m_p2_over_k_e_e2=mp.nstr(grav_em_ratio_pp, 8),
    doc_claimed_apparent="~1e-36",
    coupling_factor_needed_to_close=mp.nstr(needed_factor, 8),
    verdict="the stated order is reproduced (8.1e-37 for the proton-proton ratio), but "
            "'apparent = normalized x coupling factor' leaves the coupling factor free: "
            "any value reproduces any target, so the identity carries no prediction")

# N6: prime anchor of 体系十
def primepi_sieve(x):
    s = bytearray([1]) * (x + 1)
    s[0] = s[1] = 0
    i = 2
    while i * i <= x:
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
        i += 1
    return sum(s)


def nth_prime(k):
    x, cnt = 1, 0
    while cnt < k:
        x += 1
        if all(x % i for i in range(2, int(x ** 0.5) + 1)):
            cnt += 1
    return x


rec("N6_prime_anchor",
    is_18917_prime=bool(all(18917 % i for i in range(2, 138))),
    primepi_18917=primepi_sieve(18917),
    prime_2153=nth_prime(2153),
    is_2153_prime=bool(all(2153 % i for i in range(2, 47))),
    digit_root_18917=1 + (18917 - 1) % 9,
    mod_8_18917=18917 % 8,
    round_N_A=int(mp.nint(N_A)), round_N_B_at_137=int(mp.nint(N_B_rounded_alpha)),
    factor_18907="7*37*73" if (7 * 37 * 73 == 18907) else "NOT 7*37*73",
    net_new="no: 01A registers this as X12 (its §4.3 X12 paragraph and its §6 ledger row), so this "
            "block is a reproduction of an existing verdict, not a new defect",
    verdict="all stated arithmetic properties hold; they are properties of the integer nearest "
            "N_A and inherit X12's alpha-dependence (at alpha=1/137 the anchor is 18907 = 7*37*73, "
            "composite). Structural, not physical.")

# ---------------------------------------------------------------- regression of X9/X10 numbers
rho_G = mp.sqrt(GG / (ALPHA ** 2 * MU0 * C ** 2))
rho_C_e = HBAR / (M_E * C)
ell_P = mp.sqrt(HBAR * GG / C ** 3)
ratio_x10 = mp.sqrt(1 + ALPHA ** 2)
Fmax_at_ellP = C ** 3 * ell_P ** 4 / HBAR
max_force = C ** 4 / (4 * GG)
rec("X9_X10_X15_regression",
    rho_G_from_G=mp.nstr(rho_G, 10), rho_C_electron=mp.nstr(rho_C_e, 10),
    ratio=mp.nstr(rho_G / rho_C_e, 10),
    doc_01A_values={"rho_G": "3.33129e-09", "rho_C": "3.86159e-13", "ratio": "8626.71"},
    sqrt_1_plus_alpha2=mp.nstr(ratio_x10, 12),
    doc_01A_sqrt_1_plus_alpha2="1.000026625",
    F_G_max_at_ell_Planck=mp.nstr(Fmax_at_ellP, 10), max_force_c4_over_4G=mp.nstr(max_force, 10),
    gap_decades=mp.nstr(mp.log10(max_force / Fmax_at_ellP), 8),
    doc_01A_gap="1.7e+123",
    verdict="01A's X9/X10/X15 numbers reproduced")

R["meta"] = {
    "script": os.path.relpath(os.path.abspath(__file__), SERIES).replace("\\", "/"),
    "checks_face": os.path.relpath(OUT, SERIES).replace("\\", "/"),
    "sympy_version": sp.__version__,
    "mpmath_version": mp.__version__,
    "run_time": datetime.now().isoformat(timespec="seconds"),
    "external_anchors": {"alpha_inv_primary": mp.nstr(ALPHA_INV, 12),
                         "alpha_from_primary_inverse": mp.nstr(ALPHA, 14),
                         "alpha_01A_declared_CODATA2018": mp.nstr(ALPHA_01A, 14),
                         "alpha_inv_of_01A_anchor": mp.nstr(ALPHA_INV_OF_01A, 14),
                         "alpha_inv_1sigma_absolute": mp.nstr(ALPHA_INV_U, 3),
                         "alpha_inv_1sigma_relative": mp.nstr(ALPHA_REL_U, 4),
                         "anchor_source_note": "137.035999177(21), i.e. u = 2.1e-8 absolute = "
                                               "1.53e-10 relative, as listed for the latest CODATA "
                                               "dataset in the fine-structure-constant article "
                                               "consulted 2026-09-28; the 01A anchor is quoted as "
                                               "that document prints it, vintage not adjudicated",
                         "c_m_s": "299792458 exact", "hbar_J_s": "1.054571817e-34",
                         "G_m3_kg-1_s-2": "6.67430e-11", "e_C": "1.602176634e-19 exact",
                         "mu0": "1.2566370614e-6", "eps0": "8.8541878128e-12",
                         "m_e_kg": "9.1093837015e-31", "m_p_kg": "1.67262192369e-27"},
    "instrument_history": "self-caught defect in the FIRST build of this face: ALPHA_INV_U was "
                          "typed 2.1e-7 (the (21) of 137.035999177(21) aligned one digit too far "
                          "left) while a hardcoded 1.6e-10 was used for the same quantity elsewhere "
                          "in the file -- two values for one uncertainty. Every sigma-normalised "
                          "reading (N2.gap_in_units_of_alpha_inv_sigma, N2.how_many_alpha_sigmas_off, "
                          "N7.rel_gap_in_units_of_primary_rel_sigma) was therefore ~10x too small. "
                          "Now u = 2.1e-8 absolute / 1.53e-10 relative, derived once into "
                          "ALPHA_REL_U and used from that single source; the N2 verdict no longer "
                          "narrates the multiple in words at all -- it interpolates the computed "
                          "reading, so prose cannot drift from the sigma it is priced with.",
    "dps": 50,
    "doc_face": "24_TUFT核心公式全维核验_体系一至十_2026-09-28.md",
}

SAMPLE = {rho: sp.Integer(1), b: sp.Rational(72973525693, 10 ** 13),
          A: sp.Rational(72973525693, 10 ** 13),
          th: sp.Rational(7, 10)}     # theta only appears in the N1 controls


def _as_mpf(v):
    if isinstance(v, str):
        return mp.mpf(v)
    if isinstance(v, bool):
        return mp.mpf(int(v))
    if isinstance(v, sp.Basic):               # needles only need magnitude, not full precision
        if v.free_symbols:
            v = v.subs(SAMPLE)
        v = sp.N(v, 30)
        if not v.is_number:
            raise TypeError("non-numeric needle value %s" % v)
        return mp.mpf(repr(float(v)))
    return mp.mpf(str(v))


# every identity check must come with a mutated control that is NOT zero, otherwise the
# "residual == 0" rows below prove only that the script ran.
NEEDLES = [
    ("S1_frenet_helix", "resid_kappa", "mutant_resid_kappa"),
    ("S1_frenet_helix", "resid_tau", "mutant_resid_tau"),
    ("S1_frenet_helix", "ell_identity_resid", "mutant_ell_resid"),
    ("S2_alpha_and_ntwist", "resid_ntw_minus_alpha2_over_1_plus_alpha2", "mutant_ntw_resid"),
    ("S3_series_closure", "equals_N_A_resid", "mutant_missing_last_term"),
    ("S3_four_force_table", "sum_resid", "mutant_sum_without_last_column"),
]
TOL = mp.mpf("1e-25")
needle_rows, needle_fail = [], []
for check, zero_key, mut_key in NEEDLES:
    z = _as_mpf(R["checks"][check][zero_key])
    m = _as_mpf(R["checks"][check][mut_key])
    ok = abs(z) < TOL and m != 0
    needle_rows.append("%s.%s zero=%s mutant=%s -> %s"
                       % (check, zero_key, mp.nstr(z, 6), mp.nstr(m, 8), "TEETH" if ok else "FAIL"))
    if not ok:
        needle_fail.append("%s.%s zero=%s mutant=%s"
                           % (check, zero_key, mp.nstr(z, 6), mp.nstr(m, 8)))
# N1 prints a constant-geometry control: rho/ell must be theta-independent while cos(theta) is not
if _as_mpf(R["checks"]["N1_theta_conflation"]
           ["resid_d_of_rho_over_ell_wrt_spiral_parameter"]) != 0:
    needle_fail.append("N1.rho_over_ell_should_be_theta_independent")
if _as_mpf(R["checks"]["N1_theta_conflation"]
           ["resid_d_of_cos_theta_wrt_spiral_parameter"]) == 0:
    needle_fail.append("N1.cos_theta_control_should_be_nonzero")
R["meta"]["needles"] = needle_rows
R["meta"]["needle_failures"] = needle_fail
if needle_fail:
    print("NEEDLE FAILURE", needle_fail)
    raise SystemExit(3)
print("\n".join("needle " + x for x in needle_rows))

with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=1, default=str)
    fh.flush()
    os.fsync(fh.fileno())
print("wrote", os.path.relpath(OUT, SERIES).replace("\\", "/"), os.path.getsize(OUT), "bytes")
for k in ("S1_frenet_helix", "S3_four_force_table", "S2_alpha_and_ntwist", "S3_N_definitions",
      "N2_asin_vs_sin_closure", "N7_anchor_vintage"):
    print("<<", k, json.dumps(R["checks"][k], ensure_ascii=False, default=str)[:620])

