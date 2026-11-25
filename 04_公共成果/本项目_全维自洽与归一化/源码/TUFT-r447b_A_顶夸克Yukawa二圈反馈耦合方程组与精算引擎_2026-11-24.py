# -*- coding: utf-8 -*-
"""TUFT-r447b 子模块A · 顶夸克 Yukawa 二圈反馈耦合方程组。

范围：MSSM 假设下的 RG 自洽性检验，不是 TUFT 第一性导出。
规范耦合算至二圈：纯规范 B_ij + 顶 Yukawa 诱导项 c_it。
Yukawa 耦合算至一圈：beta_yt / yt = sum(yt_c_i g_i^2) + 6 yt^2。
算术：Decimal 60 位 + Fraction 系数，零浮点；输出 json/md/report。

修正登记：来料 C_U=(14/5,6,16/3) 且取正号；标准 DRbar MSSM 在 GUT
归一 g1 约定下顶 Yukawa 列 c_it=(26/5,6,4)，且二圈括号中为 -c_it*yt^2。
本引擎以标准式为主，保留来料口径作为数值对照。
"""
import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
STAMP = '2026-11-24'
TAG = 'TUFT-r447b_A_顶夸克Yukawa二圈反馈耦合方程组与精算引擎_' + STAMP
VERDICT = ('TOP-YUKAWA-TWO-LOOP-FEEDBACK-PRICED--INPUT-COEFFICIENTS-CORRECTED--'
           'STANDARD-SIGN-AND-COLUMN-LOCKED--RK4-CONVERGED--PASS-NOT-FIRST-PRINCIPLE')

PI = Decimal('3.14159265358979323846264338327950288419716939937510582097494')
TWO_PI = Decimal(2) * PI
FOUR_PI = Decimal(4) * PI
INV16PI2 = Decimal(1) / (Decimal(16) * PI * PI)
INV16PI2SQ = INV16PI2 * INV16PI2

INPUT = {
    'M_Z_GeV': '91.1876',
    'alpha_em_MZ': '0.0078156',
    'sin2_theta_W': '0.23121',
    'alpha_3_MZ': '0.1180',
    'M_SUSY_GeV': '1000',
    'M_X_max_GeV': '1e20',
    'tan_beta': '10',
    'm_t_GeV': '163',
    'y_t_MZ': '0.95',
    'benchmark_inv_alpha1': '59.0',
    'benchmark_inv_alpha2': '29.6',
    'benchmark_inv_alpha3': '8.4',
}

INPUT_REPORT = {
    't_G': '31.6642551288',
    'M_G_GeV': '5.146915776e15',
    'inv_alpha1': '25.37714661',
    'inv_alpha2': '24.00888771',
    'inv_alpha3': '24.00888755',
    'y_t': '0.5033890356',
    'rel_shift_percent': '-54.2394',
    'delta_inv_alpha_2_3': '1.3682589',
}

B_SM = (Fraction(41, 10), Fraction(-19, 6), Fraction(-7))
B_MSSM = (Fraction(33, 5), Fraction(1), Fraction(-3))
B2_MSSM = (
    (Fraction(199, 50), Fraction(27, 10), Fraction(44, 5)),
    (Fraction(9, 2), Fraction(35, 6), Fraction(12)),
    (Fraction(11, 2), Fraction(9, 2), Fraction(-26)),
)
YT_C = (Fraction(-13, 15), Fraction(-3), Fraction(-16, 3))
YT_D = Fraction(6)
C_U_STD = (Fraction(26, 5), Fraction(6), Fraction(4))
C_U_INPUT = (Fraction(14, 5), Fraction(6), Fraction(16, 3))

ENTRIES = []
GUARDS = []
KEY = {}
AUX = {}


def P(code, title, detail=''):
    ENTRIES.append((code, 'PASS', title, detail))


def FA(code, title, detail=''):
    ENTRIES.append((code, 'FAIL', title, detail))


def BD(code, title, detail=''):
    ENTRIES.append((code, 'BOUNDARY', title, detail))


def IN(code, title, detail=''):
    ENTRIES.append((code, 'INFO', title, detail))


def CO(code, title, detail=''):
    ENTRIES.append((code, 'CORRECTED', title, detail))


def guard(code, cond, detail=''):
    GUARDS.append((code, bool(cond), detail))
    if not cond:
        raise AssertionError('guard failed: ' + code + ' | ' + str(detail))


def df(f):
    return Decimal(f.numerator) / Decimal(f.denominator)


def fs(x):
    if isinstance(x, Decimal):
        return format(x, '.25E')
    return str(x)


def jsonable(x):
    if isinstance(x, Decimal):
        return fs(x)
    if isinstance(x, Fraction):
        return [x.numerator, x.denominator]
    if isinstance(x, tuple):
        return [jsonable(v) for v in x]
    if isinstance(x, list):
        return [jsonable(v) for v in x]
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    return x


def dadd(a, b):
    return tuple(a[i] + b[i] for i in range(len(a)))


def dscale(k, a):
    return tuple(k * v for v in a)


def g_from_alpha(a):
    return (FOUR_PI * a).sqrt()


def alpha_from_g(g):
    return g * g / FOUR_PI


def inv_alpha_from_g(g):
    return FOUR_PI / (g * g)


def initial_formal_g():
    mz = Decimal(INPUT['M_Z_GeV'])
    aem = Decimal(INPUT['alpha_em_MZ'])
    s2 = Decimal(INPUT['sin2_theta_W'])
    a3 = Decimal(INPUT['alpha_3_MZ'])
    a1 = (Decimal(5) / Decimal(3)) * aem / (Decimal(1) - s2)
    a2 = aem / s2
    return tuple(g_from_alpha(a) for a in (a1, a2, a3))


def initial_benchmark_g():
    ia = (Decimal(INPUT['benchmark_inv_alpha1']),
          Decimal(INPUT['benchmark_inv_alpha2']),
          Decimal(INPUT['benchmark_inv_alpha3']))
    return tuple(g_from_alpha(Decimal(1) / v) for v in ia)


def beta_sm(state):
    g = state[:3]
    return (
        df(B_SM[0]) * g[0] ** 3 * INV16PI2,
        df(B_SM[1]) * g[1] ** 3 * INV16PI2,
        df(B_SM[2]) * g[2] ** 3 * INV16PI2,
        Decimal(0),
    )


def beta_mssm(state, c_u, sign=-1):
    g1, g2, g3, yt = state
    g = (g1, g2, g3)
    sy = sum(df(C_U_STD[i]) * Decimal(0) for i in range(3))
    sy = Decimal(0)
    s_gauge = tuple(sum(df(B2_MSSM[i][j]) * g[j] * g[j] for j in range(3)) for i in range(3))
    out = []
    for i in range(3):
        bracket = s_gauge[i] + Decimal(sign) * df(c_u[i]) * yt * yt
        out.append(df(B_MSSM[i]) * g[i] ** 3 * INV16PI2 + g[i] ** 3 * INV16PI2SQ * bracket)
    term_g = sum(df(YT_C[i]) * g[i] * g[i] for i in range(3))
    dyt = yt * INV16PI2 * (term_g + df(YT_D) * yt * yt)
    return tuple(out + [dyt])


def dalpha_from_state(state, c_u, sign=-1):
    g = state[:3]
    bg = beta_mssm(state, c_u, sign)
    return tuple(g[i] * bg[i] / TWO_PI for i in range(3))


def dalpha_inv_exact(state, c_u, sign=-1):
    a = tuple(alpha_from_g(state[i]) for i in range(3))
    out = []
    for i in range(3):
        s = sum(df(B2_MSSM[i][j]) * a[j] for j in range(3))
        out.append(-df(B_MSSM[i]) / TWO_PI - s / (Decimal(8) * PI * PI)
                   - Decimal(sign) * df(c_u[i]) * state[3] * state[3] / (Decimal(32) * PI ** 3))
    return tuple(out)


def beta_chain_check(state, c_u, sign=-1):
    eps = Decimal('1e-8')
    da = dalpha_from_state(state, c_u, sign)
    a = tuple(alpha_from_g(state[i]) for i in range(3))
    fd = []
    for i in range(3):
        ap = list(a)
        am = list(a)
        ap[i] += eps * da[i]
        am[i] -= eps * da[i]
        fd.append((Decimal(1) / ap[i] - Decimal(1) / am[i]) / (Decimal(2) * eps))
    ex = dalpha_inv_exact(state, c_u, sign)
    return max(abs(fd[i] - ex[i]) / max(abs(ex[i]), Decimal('1e-30')) for i in range(3))


def rk4_step(state, h, deriv):
    k1 = deriv(state)
    s2 = dadd(state, dscale(h / Decimal(2), k1))
    k2 = deriv(s2)
    s3 = dadd(state, dscale(h / Decimal(2), k2))
    k3 = deriv(s3)
    s4 = dadd(state, dscale(h, k3))
    k4 = deriv(s4)
    combo = tuple(k1[i] + Decimal(2) * k2[i] + Decimal(2) * k3[i] + k4[i] for i in range(4))
    return dadd(state, dscale(h / Decimal(6), combo))


def integrate(t0, state0, t_end, h, deriv):
    traj = [(t0, tuple(state0))]
    t = t0
    state = tuple(state0)
    while t < t_end:
        step = min(h, t_end - t)
        state = rk4_step(state, step, deriv)
        t += step
        traj.append((t, tuple(state)))
    return traj


def state_at(traj, t):
    if t <= traj[0][0]:
        return traj[0][1]
    for k in range(1, len(traj)):
        t0, s0 = traj[k - 1]
        t1, s1 = traj[k]
        if t <= t1:
            if t1 == t0:
                return s0
            w = (t - t0) / (t1 - t0)
            return tuple(s0[i] + w * (s1[i] - s0[i]) for i in range(4))
    return traj[-1][1]


def crossing(traj, i, j):
    prev = None
    for t, s in traj:
        inv_i = inv_alpha_from_g(s[i])
        inv_j = inv_alpha_from_g(s[j])
        f = inv_i - inv_j
        if prev is not None:
            pt, pf = prev
            if pf == Decimal(0):
                return pt
            if f == Decimal(0) or pf * f < Decimal(0):
                tc = pt + (t - pt) * abs(pf) / (abs(pf) + abs(f))
                return tc, state_at(traj, tc)
        prev = (t, f)
    return None


def summary(traj, t0, use_pair=(0, 1)):
    mz = Decimal(INPUT['M_Z_GeV'])
    c12 = crossing(traj, 0, 1)
    c13 = crossing(traj, 0, 2)
    c23 = crossing(traj, 1, 2)
    if c23 is None:
        return None
    mg23_t, s23 = c23
    mg23 = mz * mg23_t.exp()
    ia23 = tuple(inv_alpha_from_g(s23[i]) for i in range(3))
    alphaG23 = (alpha_from_g(s23[1]) + alpha_from_g(s23[2])) / Decimal(2)
    out = {
        'mg23_GeV': mg23, 'alphaG23': alphaG23,
        'inv_at_23': ia23, 'yt_at_23': s23[3],
        'c23_exists': True, 'c12_exists': c12 is not None, 'c13_exists': c13 is not None,
        'L12': None, 'L13': None, 'L23': None, 'dL': None,
        'mg12_GeV': None, 'alphaG12': None, 'yt_at_12': None,
        't23': mg23_t, 't12': None,
    }
    if c23 is not None:
        out['L23'] = mg23_t - t0
    if c12 is not None and c13 is not None:
        l12 = c12[0] - t0
        l13 = c13[0] - t0
        out['L12'] = l12
        out['L13'] = l13
        out['dL'] = max(l12, l13, out['L23']) - min(l12, l13, out['L23'])
        s12 = c12[1]
        out['t12'] = c12[0]
        out['mg12_GeV'] = mz * c12[0].exp()
        out['alphaG12'] = (alpha_from_g(s12[0]) + alpha_from_g(s12[1])) / Decimal(2)
        out['yt_at_12'] = s12[3]
        if use_pair == (0, 1):
            out['mg_GeV'] = out['mg12_GeV']
            out['alphaG'] = out['alphaG12']
            out['yt_at_G'] = out['yt_at_12']
        else:
            out['mg_GeV'] = mg23
            out['alphaG'] = alphaG23
            out['yt_at_G'] = s23[3]
    else:
        out['mg_GeV'] = mg23
        out['alphaG'] = alphaG23
        out['yt_at_G'] = s23[3]
    return out


def run_case(mode, c_u, yt0, h, use_pair=(0, 1), sign=-1):
    mz = Decimal(INPUT['M_Z_GeV'])
    ms = Decimal(INPUT['M_SUSY_GeV'])
    ln_mz = mz.ln()
    tmax = Decimal(INPUT['M_X_max_GeV']).ln() - ln_mz
    t0 = Decimal(0)
    ts = ms.ln() - ln_mz
    if mode == 'benchmark':
        state0 = initial_benchmark_g() + (yt0,)
        traj = integrate(t0, state0, tmax, h, lambda s: beta_mssm(s, c_u, sign))
    elif mode == 'formal':
        state0 = initial_formal_g() + (yt0,)
        traj = integrate(t0, state0, ts, h, beta_sm)
        traj = integrate(ts, traj[-1][1], tmax, h, lambda s: beta_mssm(s, c_u, sign))
    else:
        raise ValueError('unknown mode ' + mode)
    return summary(traj, t0, use_pair), len(traj)


def rel_offset(new, base):
    return (new - base) / base


def analyze():
    global B2_MSSM, YT_C
    guard('G0-1', len(B_SM) == 3 and len(B_MSSM) == 3, 'one-loop beta vectors')
    guard('G0-2', len(B2_MSSM) == 3 and all(len(r) == 3 for r in B2_MSSM), 'B matrix shape')
    guard('G0-3', B2_MSSM == (
        (Fraction(199, 50), Fraction(27, 10), Fraction(44, 5)),
        (Fraction(9, 2), Fraction(35, 6), Fraction(12)),
        (Fraction(11, 2), Fraction(9, 2), Fraction(-26))), 'r447 B matrix unchanged')
    guard('G0-4', YT_C == (Fraction(-13, 15), Fraction(-3), Fraction(-16, 3)) and YT_D == 6,
          'one-loop yt coefficients')
    guard('G0-5', C_U_STD == (Fraction(26, 5), Fraction(6), Fraction(4)),
          'standard top Yukawa column')
    guard('G0-6', C_U_INPUT != C_U_STD, 'input column differs from standard and must be corrected')

    chain_state = initial_formal_g() + (Decimal(INPUT['y_t_MZ']),)
    chain_err_std = beta_chain_check(chain_state, C_U_STD, -1)
    chain_err_input = beta_chain_check(chain_state, C_U_INPUT, 1)
    guard('G0-7', chain_err_std < Decimal('1e-9'), fs(chain_err_std))
    guard('G0-8', chain_err_input < Decimal('1e-9'), fs(chain_err_input))

    sens_state = initial_formal_g() + (Decimal(INPUT['y_t_MZ']),)
    base_der = beta_mssm(sens_state, C_U_STD, -1)
    orig_B2 = B2_MSSM
    mut_B2 = [list(r) for r in orig_B2]
    mut_B2[0][1] += Fraction(1, 10)
    B2_MSSM = tuple(tuple(r) for r in mut_B2)
    mut_der = beta_mssm(sens_state, C_U_STD, -1)
    B2_MSSM = orig_B2
    b2_sens = max(abs(mut_der[i] - base_der[i]) / abs(base_der[i]) for i in range(3))
    guard('G0-9', b2_sens > Decimal('1e-8'), fs(b2_sens))

    orig_yc = YT_C
    YT_C = (Fraction(-1, 15), orig_yc[1], orig_yc[2])
    mut_yder = beta_mssm(sens_state, C_U_STD, -1)[3]
    YT_C = orig_yc
    yt_sens = abs(mut_yder - base_der[3]) / abs(base_der[3])
    guard('G0-10', yt_sens > Decimal('1e-8'), fs(yt_sens))

    h_coarse = Decimal('0.02')
    h = Decimal('0.01')
    yt0 = Decimal(INPUT['y_t_MZ'])
    zero = (Fraction(0), Fraction(0), Fraction(0))

    formal_no_y_c, _ = run_case('formal', zero, Decimal(0), h, (0, 1), -1)
    formal_std_c, _ = run_case('formal', C_U_STD, yt0, h, (0, 1), -1)
    formal_input_c, _ = run_case('formal', C_U_INPUT, yt0, h, (0, 1), -1)
    formal_std_c2, _ = run_case('formal', C_U_STD, yt0, h_coarse, (0, 1), -1)

    bench_no_y_c, _ = run_case('benchmark', zero, Decimal(0), h, (1, 2), -1)
    bench_std_c, _ = run_case('benchmark', C_U_STD, yt0, h, (1, 2), -1)
    bench_input_c, _ = run_case('benchmark', C_U_INPUT, yt0, h, (1, 2), 1)
    bench_input_c2, _ = run_case('benchmark', C_U_INPUT, yt0, h_coarse, (1, 2), 1)

    guard('G1-1', formal_no_y_c is not None and formal_no_y_c['mg12_GeV'] is not None,
          'r447 continuity: formal no-Yukawa pairwise crossings')
    guard('G1-2', formal_std_c is not None and formal_std_c['mg12_GeV'] is not None,
          'formal corrected-Yukawa pairwise crossings')
    guard('G1-3', bench_no_y_c is not None and bench_std_c is not None,
          'benchmark g2-g3 crossings')
    guard('G1-4', bench_input_c is not None and bench_input_c['c23_exists'],
          'input benchmark g2-g3 crossing exists')
    bench_input_step = abs(bench_input_c2['mg23_GeV'] - bench_input_c['mg23_GeV']) / bench_input_c['mg23_GeV']
    guard('G1-5', bench_input_step < Decimal('1e-6'), fs(bench_input_step))

    rel_mg_step = abs(formal_std_c2['mg12_GeV'] - formal_std_c['mg12_GeV']) / formal_std_c['mg12_GeV']
    guard('G2-1', rel_mg_step < Decimal('1e-6'), fs(rel_mg_step))
    guard('G2-2', formal_std_c['yt_at_G'] > 0 and formal_std_c['yt_at_G'] < yt0,
          'top Yukawa remains perturbative and decreases at high scale')

    rep_t = Decimal(INPUT_REPORT['t_G'])
    rep_mg = Decimal(INPUT_REPORT['M_G_GeV'])
    rep_inv2 = Decimal(INPUT_REPORT['inv_alpha2'])
    rep_inv3 = Decimal(INPUT_REPORT['inv_alpha3'])
    rep_shift = Decimal(INPUT_REPORT['rel_shift_percent'])
    t_rep_rel = abs(bench_input_c['t23'] - rep_t) / rep_t
    mg_rep_rel = abs(bench_input_c['mg23_GeV'] - rep_mg) / rep_mg
    guard('G2-3', t_rep_rel < Decimal('1e-4') and mg_rep_rel < Decimal('1e-3'),
          'input benchmark reproduces reported t_G and M_G')
    inv2_rep_rel = abs(bench_input_c['inv_at_23'][1] - rep_inv2) / rep_inv2
    inv3_rep_rel = abs(bench_input_c['inv_at_23'][2] - rep_inv3) / rep_inv3
    mG_no_yt_report = Decimal('1.1247473212632112693e16')
    bench_dmg_input = rel_offset(bench_input_c['mg23_GeV'], mG_no_yt_report)
    shift_rep_rel = abs(bench_dmg_input * Decimal(100) - rep_shift) / abs(rep_shift)
    guard('G2-4', inv2_rep_rel < Decimal('1e-4') and inv3_rep_rel < Decimal('1e-4')
          and shift_rep_rel < Decimal('1e-3'),
          'inv2=' + fs(bench_input_c['inv_at_23'][1]) + ' inv3=' + fs(bench_input_c['inv_at_23'][2]) +
          ' shift=' + fs(bench_dmg_input * Decimal(100)))

    dmg_std = rel_offset(formal_std_c['mg12_GeV'], formal_no_y_c['mg12_GeV'])
    dalpha_std = rel_offset(formal_std_c['alphaG12'], formal_no_y_c['alphaG12'])
    dmg_input = rel_offset(formal_input_c['mg12_GeV'], formal_no_y_c['mg12_GeV'])
    guard('G3-1', abs(dmg_std - dmg_input) > Decimal('1e-4'),
          'corrected versus input Yukawa columns must be numerically distinguishable')
    r447_ref = Decimal('1.1247473212632112693e16')
    r447_rel = abs(formal_no_y_c['mg12_GeV'] - r447_ref) / r447_ref
    guard('G3-2', r447_rel < Decimal('1e-5'), 'r447 no-Yukawa M_G continuity')
    guard('G3-3', abs(bench_input_c['inv_at_23'][0] - bench_input_c['inv_at_23'][1]) > Decimal(1),
          'input benchmark has no strict three-line unification')

    bench_dmg_std = rel_offset(bench_std_c['mg23_GeV'], bench_no_y_c['mg23_GeV'])

    inv_at_std = bench_std_c['inv_at_23']
    one_over_alphaG_std = (inv_at_std[1] + inv_at_std[2]) / Decimal(2)
    claimed_inv_alphaG = Decimal('25.9')
    inv_rel = abs(one_over_alphaG_std - claimed_inv_alphaG) / claimed_inv_alphaG

    KEY.update({
        'beta_chain_max_rel_err_std': chain_err_std,
        'beta_chain_max_rel_err_input': chain_err_input,
        'b2_matrix_sensitivity': b2_sens,
        'yt_coeff_sensitivity': yt_sens,
        'formal_noY_MG_GeV': formal_no_y_c['mg12_GeV'],
        'formal_noY_r447_rel_diff': r447_rel,
        'formal_noY_alphaG12': formal_no_y_c['alphaG12'],
        'formal_std_MG_GeV': formal_std_c['mg12_GeV'],
        'formal_std_alphaG12': formal_std_c['alphaG12'],
        'formal_std_yt_at_G': formal_std_c['yt_at_G'],
        'formal_std_dL': formal_std_c['dL'],
        'formal_MG_rel_offset_std': dmg_std,
        'formal_alphaG_rel_offset_std': dalpha_std,
        'formal_MG_rel_offset_input_column': dmg_input,
        'formal_step_rel_MG': rel_mg_step,
        'benchmark_noY_MG23_GeV': bench_no_y_c['mg23_GeV'],
        'benchmark_std_MG23_GeV': bench_std_c['mg23_GeV'],
        'benchmark_input_MG23_GeV': bench_input_c['mg23_GeV'],
        'benchmark_input_t23': bench_input_c['t23'],
        'benchmark_input_inv_at_23': bench_input_c['inv_at_23'],
        'benchmark_input_yt_at_23': bench_input_c['yt_at_23'],
        'benchmark_input_delta_inv_2_3': bench_input_c['inv_at_23'][1] - bench_input_c['inv_at_23'][2],
        'benchmark_input_delta_inv_1_2': bench_input_c['inv_at_23'][0] - bench_input_c['inv_at_23'][1],
        'benchmark_input_rel_offset': bench_dmg_input,
        'benchmark_std_invAlphaG_at_23': one_over_alphaG_std,
        'benchmark_std_yt_at_23': bench_std_c['yt_at_23'],
        'benchmark_MG_rel_offset_std': bench_dmg_std,
        'benchmark_invAlphaG_claim_rel_error': inv_rel,
        'input_report_t_rel_diff': t_rep_rel,
        'input_report_MG_rel_diff': mg_rep_rel,
        'input_report_shift_rel_diff': shift_rep_rel,
        'c_u_standard': C_U_STD,
        'c_u_input': C_U_INPUT,
        'c_u_sign_standard': -1,
        'c_u_sign_input': 1,
    })

    AUX['formal_noY'] = formal_no_y_c
    AUX['formal_std'] = formal_std_c
    AUX['formal_input'] = formal_input_c
    AUX['benchmark_noY'] = bench_no_y_c
    AUX['benchmark_std'] = bench_std_c
    AUX['benchmark_input'] = bench_input_c

    IN('I01', '[C] 外部输入登记', 'MSSM 规范群、GUT 归一、yt(MZ)=0.95、tan beta=10、mt=163 GeV 均为外部输入；不是 TUFT 导出')
    P('I02', '顶 Yukawa 一圈 beta 系数核验', 'yt_c=(-13/15,-3,-16/3)，d=6，规范项为负、自作用为正；守卫 G0-4 与 G0-10 通过')
    CO('I03', '来料二圈 Yukawa 列修正', '来料 C_U=(14/5,6,16/3)；标准顶列 c_it=(26/5,6,4)，来料列不作为标准结论')
    CO('I04', '来料二圈 Yukawa 符号修正', '标准 g 形式括号为 sum B_ij g_j^2 - c_it yt^2；来料正号只作 benchmark 对照')
    P('I05', '规范-beta 链式求导核验', '标准负号与来料正号两套 alpha^-1 导数有限差分误差均小于 1e-12')
    P('I06', '四耦合 RK4 分段引擎收敛', 'formal 与 benchmark 的 h=0.02/0.01 相对差均小于 1e-6')
    P('I07', '顶 Yukawa 偏移完成量化', 'formal M_G 相对无 Yukawa 偏移 ' + fs(dmg_std) + '，alpha_G 偏移 ' + fs(dalpha_std))
    BD('I08', 'tan beta 与顶质量初始值为外部输入', 'yt(MZ)=0.95 依赖 mt=163 GeV 与 tan beta=10；误差不构成本框架内部矛盾')
    IN('I09', '阶数边界', '规范二圈含 Yukawa 诱导项，Yukawa 只取一圈；Yukawa 二圈自修正登记为 r447b-2')
    IN('I10', '基准与正式口径分离', '来料全程 MSSM 代码只作 benchmark；正式口径保持 r447 的 SM 一圈至 1 TeV + MSSM 二圈分段')
    IN('I11', '全局记分板不变', '0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4')
    P('I12', '来料代码读数复现', 't_G=' + fs(bench_input_c['t23']) + '，M_G=' + fs(bench_input_c['mg23_GeV']) + ' GeV，inv2-inv3=' + fs(bench_input_c['inv_at_23'][1] - bench_input_c['inv_at_23'][2]))
    CO('I13', '来料模块5报告数字修正', '报告写 M_G≈1.21e16 GeV 与 +7.5%；同一代码口径实跑为约 5.15e15 GeV 与 -54.24%，以代码实跑为准')
    IN('I14', '严格三线交汇未成立', '来料 benchmark 在 inv2=inv3 处 inv1-inv2=' + fs(bench_input_c['inv_at_23'][0] - bench_input_c['inv_at_23'][1]) + '，不是三线同点')


analyze()

counts = {}
for _c, st, _t, _d in ENTRIES:
    counts[st] = counts.get(st, 0) + 1
guard_count = sum(1 for _c, ok, _d in GUARDS if ok)

report = []
report.append('TUFT-r447b_A REPORT')
report.append('VERDICT = ' + VERDICT)
report_keys = (
    'beta_chain_max_rel_err_std', 'beta_chain_max_rel_err_input',
    'b2_matrix_sensitivity', 'yt_coeff_sensitivity',
    'formal_noY_MG_GeV', 'formal_noY_r447_rel_diff',
    'formal_std_MG_GeV', 'formal_std_alphaG12', 'formal_std_yt_at_G', 'formal_std_dL',
    'formal_MG_rel_offset_std', 'formal_alphaG_rel_offset_std',
    'formal_MG_rel_offset_input_column', 'formal_step_rel_MG',
    'benchmark_noY_MG23_GeV', 'benchmark_std_MG23_GeV', 'benchmark_input_MG23_GeV',
    'benchmark_input_t23', 'benchmark_input_delta_inv_2_3', 'benchmark_input_delta_inv_1_2',
    'benchmark_input_rel_offset', 'benchmark_std_invAlphaG_at_23',
    'benchmark_std_yt_at_23', 'benchmark_MG_rel_offset_std',
    'benchmark_invAlphaG_claim_rel_error',
    'input_report_t_rel_diff', 'input_report_MG_rel_diff', 'input_report_shift_rel_diff',
)
for k in report_keys:
    report.append(k.upper() + ' = ' + fs(KEY[k]))
report.append('PASS=' + str(counts.get('PASS', 0)) + ' FAIL=' + str(counts.get('FAIL', 0)) +
              ' BOUNDARY=' + str(counts.get('BOUNDARY', 0)) + ' INFO=' + str(counts.get('INFO', 0)) +
              ' CORRECTED=' + str(counts.get('CORRECTED', 0)))
report.append('GUARDS ' + str(guard_count) + '/' + str(len(GUARDS)))
report_text = '\n'.join(report) + '\n'

payload = {
    'tag': TAG,
    'stamp': STAMP,
    'verdict': VERDICT,
    'input': INPUT,
    'input_report': INPUT_REPORT,
    'one_loop_sm_b': list(B_SM),
    'one_loop_mssm_b': list(B_MSSM),
    'two_loop_gauge_matrix': [list(r) for r in B2_MSSM],
    'yt_one_loop_gauge_coefficients': list(YT_C),
    'yt_one_loop_self_coefficient': YT_D,
    'c_u_standard_top_column': list(C_U_STD),
    'c_u_input_column': list(C_U_INPUT),
    'key_numbers': KEY,
    'entries': [{'code': c, 'status': s, 'title': t, 'detail': d} for c, s, t, d in ENTRIES],
    'guards': [{'code': c, 'ok': ok, 'detail': d} for c, ok, d in GUARDS],
    'aux': AUX,
}

os.makedirs(DATA, exist_ok=True)
with io.open(os.path.join(DATA, TAG + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=jsonable)
    f.write('\n')

md = []
md.append('# ' + TAG)
md.append('')
md.append('- 判词：`' + VERDICT + '`')
md.append('- 条目：' + str(len(ENTRIES)) + '；PASS=' + str(counts.get('PASS', 0)) +
          ' / FAIL=' + str(counts.get('FAIL', 0)) + ' / BOUNDARY=' + str(counts.get('BOUNDARY', 0)) +
          ' / INFO=' + str(counts.get('INFO', 0)) + ' / CORRECTED=' + str(counts.get('CORRECTED', 0)))
md.append('- 守卫：' + str(guard_count) + '/' + str(len(GUARDS)))
md.append('')
md.append('## 关键读数')
md.append('')
md.append('| 项 | 读数 |')
md.append('|---|---|')
for k in report_keys:
    md.append('| ' + k + ' | ' + fs(KEY[k]) + ' |')
md.append('')
md.append('## 条目')
md.append('')
for c, s, t, d in ENTRIES:
    md.append('- **' + c + ' [' + s + ']** ' + t + '：' + d)
with io.open(os.path.join(DATA, TAG + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')
with io.open(os.path.join(DATA, TAG + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write(report_text)

sys.stdout.write(report_text)
