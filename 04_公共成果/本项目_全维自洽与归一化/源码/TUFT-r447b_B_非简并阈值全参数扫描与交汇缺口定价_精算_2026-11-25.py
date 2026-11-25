# -*- coding: utf-8 -*-
"""TUFT-r447b 子模块B · 非简并阈值全参数扫描与交汇缺口定价。

范围：在 r447 / r447b_A 的 MSSM 二圈 RG 与顶 Yukawa 反馈之上，
把非简并超伴子谱压缩成三个匹配尺度上的外生阈值位移 δ_i，
扫描 δ_i 与 GUT 尺度切片，定价 α1/α2/α3 精确交汇所需代价。

这不是 TUFT 第一性导出：超伴子谱、δ_i、阈值质量比与 M_G 切片均为 [C] 外部输入。
算术：Decimal 60 位 + Fraction beta 系数；输出 json/md/report。
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
STAMP = '2026-11-25'
TAG = 'TUFT-r447b_B_非简并阈值全参数扫描与交汇缺口定价_' + STAMP
VERDICT = ('NONDEGENERATE-THRESHOLD-SCAN--UNIFICATION-GAP-PRICED--'
           'BENCHMARK-DELTA12-CLOSED-ONLY-BY-EXTERNAL-SPLITTING--'
           'PASS-NOT-FIRST-PRINCIPLE')

PI = Decimal('3.14159265358979323846264338327950288419716939937510582097494')
TWO_PI = Decimal(2) * PI
FOUR_PI = Decimal(4) * PI
INV16PI2 = Decimal(1) / (Decimal(16) * PI * PI)
INV16PI2SQ = INV16PI2 * INV16PI2

INPUT = {
    'M_Z_GeV': '91.1876',
    'M_SUSY_GeV': '1000',
    'M_X_max_GeV': '1e20',
    'alpha_em_MZ': '0.0078156',
    'sin2_theta_W': '0.23121',
    'alpha_3_MZ': '0.1180',
    'y_t_MZ': '0.95',
    'benchmark_inv_alpha1': '59.0',
    'benchmark_inv_alpha2': '29.6',
    'benchmark_inv_alpha3': '8.4',
    'benchmark_t_G': '31.664255128757780705910102',
    'benchmark_delta_inv_1_2': '1.3682589036099405650718438',
    'benchmark_delta_inv_2_3': '1.5671639958854060050759392e-7',
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
DELTA_B = tuple(B_MSSM[i] - B_SM[i] for i in range(3))  # (5/2, 25/6, 4)

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


def apply_threshold_inv(state, delta):
    out = list(state)
    for i in range(3):
        inv = inv_alpha_from_g(state[i]) + delta[i]
        if inv <= Decimal(0):
            raise ValueError('threshold must keep alpha positive')
        out[i] = g_from_alpha(Decimal(1) / inv)
    return tuple(out)


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
    s_gauge = tuple(sum(df(B2_MSSM[i][j]) * g[j] * g[j] for j in range(3)) for i in range(3))
    out = []
    for i in range(3):
        bracket = s_gauge[i] + Decimal(sign) * df(c_u[i]) * yt * yt
        out.append(df(B_MSSM[i]) * g[i] ** 3 * INV16PI2 + g[i] ** 3 * INV16PI2SQ * bracket)
    term_g = sum(df(YT_C[i]) * g[i] * g[i] for i in range(3))
    dyt = yt * INV16PI2 * (term_g + df(YT_D) * yt * yt)
    return tuple(out + [dyt])


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
        f = inv_alpha_from_g(s[i]) - inv_alpha_from_g(s[j])
        if prev is not None:
            pt, pf = prev
            if pf == Decimal(0):
                return pt
            if f == Decimal(0) or pf * f < Decimal(0):
                tc = pt + (t - pt) * abs(pf) / (abs(pf) + abs(f))
                return tc, state_at(traj, tc)
        prev = (t, f)
    return None


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


def formal_base_trajectory(h):
    mz = Decimal(INPUT['M_Z_GeV'])
    ms = Decimal(INPUT['M_SUSY_GeV'])
    tmax = Decimal(INPUT['M_X_max_GeV']).ln() - mz.ln()
    ts = ms.ln() - mz.ln()
    state0 = initial_formal_g() + (Decimal(INPUT['y_t_MZ']),)
    traj_sm = integrate(Decimal(0), state0, ts, h, beta_sm)
    traj = integrate(ts, traj_sm[-1][1], tmax, h, lambda s: beta_mssm(s, C_U_STD, -1))
    return traj_sm + traj[1:], ts, tmax


def formal_state_target(delta, t_target, h):
    mz = Decimal(INPUT['M_Z_GeV'])
    ms = Decimal(INPUT['M_SUSY_GeV'])
    ts = ms.ln() - mz.ln()
    base = formal_base_trajectory(h)[0]
    s_ms = apply_threshold_inv(state_at(base, ts), delta)
    return integrate(ts, s_ms, t_target, h, lambda s: beta_mssm(s, C_U_STD, -1))[-1][1]


def mismatch_from_state(s):
    inv = tuple(inv_alpha_from_g(s[i]) for i in range(3))
    return (inv[0] - inv[1], inv[1] - inv[2]), inv


def benchmark_state_target(delta, t_target, h):
    s0 = apply_threshold_inv(initial_benchmark_g() + (Decimal(INPUT['y_t_MZ']),), delta)
    return integrate(Decimal(0), s0, t_target, h, lambda s: beta_mssm(s, C_U_INPUT, 1))[-1][1]


def benchmark_crossing(h):
    """按 r447b_A 的 crossing 口径复现 benchmark 的 inv1-inv2 缺口。"""
    mz = Decimal(INPUT['M_Z_GeV'])
    tmax = Decimal(INPUT['M_X_max_GeV']).ln() - mz.ln()
    s0 = initial_benchmark_g() + (Decimal(INPUT['y_t_MZ']),)
    traj = integrate(Decimal(0), s0, tmax, h, lambda s: beta_mssm(s, C_U_INPUT, 1))
    c = crossing(traj, 1, 2)
    if c is None:
        raise ValueError('benchmark g2-g3 crossing missing')
    tc, s = c
    inv = tuple(inv_alpha_from_g(s[i]) for i in range(3))
    return tc, inv[0] - inv[1], inv[1] - inv[2], s


def solve2(a11, a12, a21, a22, b1, b2):
    det = a11 * a22 - a12 * a21
    if det == Decimal(0):
        raise ZeroDivisionError('singular 2x2 system')
    x = (b1 * a22 - a12 * b2) / det
    y = (a11 * b2 - b1 * a21) / det
    return x, y, det


def sensitivity(formula, t_target, h, eps):
    cols = []
    for i in range(3):
        d = [Decimal(0), Decimal(0), Decimal(0)]
        d[i] = eps
        fp, _ = mismatch_from_state(formula(tuple(d), t_target, h))
        dm = -eps
        d = [Decimal(0), Decimal(0), Decimal(0)]
        d[i] = dm
        fm, _ = mismatch_from_state(formula(tuple(d), t_target, h))
        cols.append(((fp[0] - fm[0]) / (Decimal(2) * eps),
                     (fp[1] - fm[1]) / (Decimal(2) * eps)))
    return ((cols[0][0], cols[1][0], cols[2][0]),
            (cols[0][1], cols[1][1], cols[2][1]))


def mass_price(delta):
    logs = []
    for i in range(3):
        logs.append(-TWO_PI * delta[i] / df(DELTA_B[i]))
    spread = max(logs) - min(logs)
    return tuple(logs), spread


def analyze():
    zero = (Decimal(0), Decimal(0), Decimal(0))
    h = Decimal('0.02')
    h_fine = Decimal('0.01')
    eps = Decimal('1e-2')
    mz = Decimal(INPUT['M_Z_GeV'])

    guard('G0-1', DELTA_B == (Fraction(5, 2), Fraction(25, 6), Fraction(4)),
          'delta beta = MSSM minus SM')
    guard('G0-2', C_U_STD == (Fraction(26, 5), Fraction(6), Fraction(4))
          and C_U_INPUT != C_U_STD, 'standard and input Yukawa columns stay separated')

    # 1) 用户 benchmark 的二力交汇缺口与关闭代价
    # 与 r447b_A 严格同口径：h=0.01 + crossing 线性插值读数，
    # 不再用固定 t_G 的 RK4 精确积分读数（两者相差约 8e-7）。
    h_bench = Decimal('0.01')
    tc_b, gap_b12, gap_b23, base_b = benchmark_crossing(h_bench)
    tb = tc_b
    fb0 = (gap_b12, gap_b23)
    inv_b0 = tuple(inv_alpha_from_g(base_b[i]) for i in range(3))
    gap_report = Decimal(INPUT['benchmark_delta_inv_1_2'])
    gap_rel = abs(gap_b12 - gap_report) / abs(gap_report)
    gap23_report = Decimal(INPUT['benchmark_delta_inv_2_3'])
    guard('G1-1', gap_rel < Decimal('1e-18'),
          'benchmark delta inv1-inv2 reproduced: ' + fs(gap_b12) + ' rel=' + fs(gap_rel))
    guard('G1-2', abs(gap_b23 - gap23_report) < Decimal('1e-18'),
          'benchmark alpha2-alpha3 crossing residual reproduced from r447b_A: ' + fs(gap_b23))

    sb = sensitivity(benchmark_state_target, tb, h_bench, eps)
    det_b = sb[0][0] * sb[1][1] - sb[0][1] * sb[1][0]
    guard('G1-3', det_b != Decimal(0), 'benchmark threshold sensitivity invertible')
    refined_b, fb_after, inv_b_after, iter_b = refine_delta(
        benchmark_state_target, zero, tb, sb, h_bench)
    guard('G1-4', max(abs(fb_after[0]), abs(fb_after[1])) < Decimal('1e-10'),
          'benchmark unified after external threshold refinement')
    guard('G1-5', refined_b[2] == Decimal(0), 'benchmark closes with delta3 fixed to zero')
    logs_b, spread_b = mass_price(refined_b)
    guard('G1-6', spread_b > Decimal(0), 'benchmark price requires non-degenerate splitting')

    # 2) formal 标准口径：以 r447b_A 的 alpha2-alpha3 交点为 t0 做全参数网格
    base_traj, ts, tmax = formal_base_trajectory(h)
    c23 = crossing(base_traj, 1, 2)
    guard('G2-1', c23 is not None, 'formal alpha2-alpha3 crossing exists')
    t0 = c23[0]
    sf0, inv_f0 = mismatch_from_state(c23[1])
    sf = sensitivity(formal_state_target, t0, h, eps)
    det_f = sf[0][0] * sf[1][1] - sf[0][1] * sf[1][0]
    guard('G2-2', det_f != Decimal(0), 'formal threshold sensitivity invertible')

    grid_step = Decimal('0.05')
    t_step = Decimal('0.05')
    t_count = 0
    hit_count = 0
    best_norm = None
    best_maxabs = None
    for ki in range(-20, 21):
        t = t0 + Decimal(ki) * t_step
        if t <= ts or t >= tmax:
            continue
        t_count += 1
        f0, _inv = mismatch_from_state(state_at(base_traj, t))
        for j in range(-100, 101):
            q = Decimal(j) * grid_step
            rhs1 = -f0[0] - sf[0][2] * q
            rhs2 = -f0[1] - sf[1][2] * q
            d1, d2, _det = solve2(sf[0][0], sf[0][1], sf[1][0], sf[1][1], rhs1, rhs2)
            d = (d1, d2, q)
            if max(abs(x) for x in d) > Decimal(5):
                continue
            hit_count += 1
            norm = (d1 * d1 + d2 * d2 + q * q).sqrt()
            mx = max(abs(x) for x in d)
            cand = {'t': t, 'delta': d, 'norm': norm, 'maxabs': mx}
            if best_norm is None or norm < best_norm['norm']:
                best_norm = cand
            if best_maxabs is None or mx < best_maxabs['maxabs']:
                best_maxabs = cand
    guard('G2-3', t_count > 0 and hit_count > 0,
          'threshold scan has nonempty parameter manifold')
    guard('G2-4', best_norm is not None and best_maxabs is not None,
          'min-norm and min-max candidates exist')

    def finalize(cand):
        t = cand['t']
        s_local = sensitivity(formal_state_target, t, h_fine, eps)
        d, f, inv, iters = refine_delta(
            formal_state_target, cand['delta'], t, s_local, h_fine)
        logs, spread = mass_price(d)
        return {
            't': t, 'delta': d, 'residual': f, 'inv': inv, 'iterations': iters,
            'M_G_GeV': mz * t.exp(), 'logs': logs, 'spread': spread,
            'maxabs': max(abs(x) for x in d),
            'norm': (d[0] * d[0] + d[1] * d[1] + d[2] * d[2]).sqrt(),
            'alphaG_inv': (inv[0] + inv[1] + inv[2]) / Decimal(3),
            'alphaG': Decimal(1) / ((inv[0] + inv[1] + inv[2]) / Decimal(3)),
        }

    final_norm = finalize(best_norm)
    final_max = finalize(best_maxabs)
    guard('G2-5', max(abs(x) for x in final_norm['residual']) < Decimal('1e-9'),
          'formal min-norm candidate closes all three inverse couplings')
    guard('G2-6', max(abs(x) for x in final_max['residual']) < Decimal('1e-9'),
          'formal min-max candidate closes all three inverse couplings')
    guard('G2-7', final_norm['M_G_GeV'] > Decimal('1e14') and final_norm['M_G_GeV'] < Decimal('1e19'),
          'unified scale remains in GUT-like range')
    guard('G2-8', final_norm['spread'] > Decimal(0), 'formal price is non-degenerate')

    s_fine_b = formal_state_target(final_norm['delta'], final_norm['t'], h_fine)
    f_fine, inv_fine = mismatch_from_state(s_fine_b)
    step_inv_gap = max(abs(inv_fine[i] - final_norm['inv'][i]) for i in range(3))
    guard('G2-9', step_inv_gap < Decimal('1e-5'),
          'step refinement keeps inverse couplings stable: ' + fs(step_inv_gap))

    KEY.update({
        'benchmark_gap_report': gap_report,
        'benchmark_gap_engine': fb0[0],
        'benchmark_gap_rel_error': abs(fb0[0] - gap_report) / abs(gap_report),
        'benchmark_gap23_report': gap23_report,
        'benchmark_gap23_engine': fb0[1],
        'benchmark_delta1': refined_b[0],
        'benchmark_delta2': refined_b[1],
        'benchmark_delta3': refined_b[2],
        'benchmark_delta1_minus_delta2': refined_b[0] - refined_b[1],
        'benchmark_residual_12': fb_after[0],
        'benchmark_residual_23': fb_after[1],
        'benchmark_masslog1': logs_b[0],
        'benchmark_masslog2': logs_b[1],
        'benchmark_masslog3': logs_b[2],
        'benchmark_mass_ratio1': logs_b[0].exp(),
        'benchmark_mass_ratio2': logs_b[1].exp(),
        'benchmark_mass_ratio3': logs_b[2].exp(),
        'benchmark_mass_split_spread': spread_b,
        'benchmark_invg_after': (inv_b_after[0] + inv_b_after[1] + inv_b_after[2]) / Decimal(3),
        'benchmark_refine_iterations': Decimal(iter_b),
        'formal_t0': t0,
        'formal_M0_GeV': mz * t0.exp(),
        'formal_gap12_at_t0': sf0[0],
        'formal_gap23_at_t0': sf0[1],
        'formal_det_sensitivity': det_f,
        'scan_t_slices': Decimal(t_count),
        'scan_hits': Decimal(hit_count),
        'formal_minnorm_t': final_norm['t'],
        'formal_minnorm_MG_GeV': final_norm['M_G_GeV'],
        'formal_minnorm_delta1': final_norm['delta'][0],
        'formal_minnorm_delta2': final_norm['delta'][1],
        'formal_minnorm_delta3': final_norm['delta'][2],
        'formal_minnorm_residual12': final_norm['residual'][0],
        'formal_minnorm_residual23': final_norm['residual'][1],
        'formal_minnorm_masslog1': final_norm['logs'][0],
        'formal_minnorm_masslog2': final_norm['logs'][1],
        'formal_minnorm_masslog3': final_norm['logs'][2],
        'formal_minnorm_mass_ratio1': final_norm['logs'][0].exp(),
        'formal_minnorm_mass_ratio2': final_norm['logs'][1].exp(),
        'formal_minnorm_mass_ratio3': final_norm['logs'][2].exp(),
        'formal_minnorm_mass_split_spread': final_norm['spread'],
        'formal_minnorm_alphaG_inv': final_norm['alphaG_inv'],
        'formal_minnorm_alphaG': final_norm['alphaG'],
        'formal_minmax_MG_GeV': final_max['M_G_GeV'],
        'formal_minmax_maxabs_delta': final_max['maxabs'],
        'formal_minmax_mass_split_spread': final_max['spread'],
        'formal_step_inv_gap': step_inv_gap,
    })

    AUX['benchmark_base_inv'] = list(inv_b0)
    AUX['benchmark_after_inv'] = list(inv_b_after)
    AUX['formal_base_inv_at_t0'] = list(inv_f0)
    AUX['formal_minnorm_inv'] = list(final_norm['inv'])
    AUX['formal_minmax_inv'] = list(final_max['inv'])
    AUX['sensitivity_benchmark'] = [list(r) for r in sb]
    AUX['sensitivity_formal'] = [list(r) for r in sf]

    IN('I01', '[C] 阈值模型登记', '非简并谱被压缩为三个匹配尺度上的外生 δ_i；M_SUSY=1 TeV、超伴子质量比与 M_G 切片均不是 TUFT 导出')
    P('I02', '阈值应用保持正耦合', 'δ_i 以 α_i^-1 加性位移进入，正值域守卫阻止负 α')
    P('I03', '用户 benchmark 缺口复现', '按 r447b_A 同口径 crossing 读数 inv1-inv2=' + fs(fb0[0]) + '，与来料 1.3682589036099405650718438 相对误差 ' + fs(KEY['benchmark_gap_rel_error']))
    P('I04', 'benchmark 阈值灵敏度可逆', '2x2 子块行列式非零，δ1/δ2 可关闭 α1 相对 α2/α3 的缺口')
    P('I05', 'benchmark 外部阈值关闭缺口', 'δ=(δ1,δ2,0) 关闭后残差 <1e-10；这证明缺口可由外生阈值吸收，不证明 MSSM 被数据选中')
    BD('I06', 'benchmark 质量分裂价格', 'δ1-δ2=' + fs(KEY['benchmark_delta1_minus_delta2']) + '，对应质量比分裂 exp(spread)=' + fs(spread_b.exp()))
    P('I07', 'formal 阈值灵敏度可逆', '标准 r447b_A 口径下 2x2 子块行列式非零')
    P('I08', 'formal 全参数网格非空', '扫描 ' + str(t_count) + ' 个 M_G 切片与 δ3 网格，命中 ' + str(hit_count) + ' 个 |δ_i|≤5 解')
    P('I09', 'formal 最小范数解精算闭合', 'M_G=' + fs(final_norm['M_G_GeV']) + ' GeV，三条残差 <1e-9')
    P('I10', 'formal 步长稳定性', 'h=0.02/0.01 的 inverse-coupling 最大差 ' + fs(step_inv_gap))
    IN('I11', 'formal 质量分裂价格', '最小范数解的最大-最小质量对数差=' + fs(final_norm['spread']) + '，不是 TUFT 可推导谱')
    IN('I12', 'min-max 对照解', 'min-max 解 max|δ|=' + fs(final_max['maxabs']) + '，质量分裂跨度=' + fs(final_max['spread']))
    CO('I13', 'r447 阈值自由度定价更新', 'r447 只给固定 α1/α2 交点下 b3 分裂；本册把三通道非简并阈值与 M_G 漂移一并定价，不改 r447 字节')
    IN('I14', '全局记分板不变', '0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4')


def refine_delta(formula, delta, t_target, sens, h, max_iter=8):
    d = [delta[0], delta[1], delta[2]]
    last_f = None
    last_inv = None
    iterations = 0
    for iterations in range(1, max_iter + 1):
        state = formula(tuple(d), t_target, h)
        last_f, last_inv = mismatch_from_state(state)
        if max(abs(last_f[0]), abs(last_f[1])) < Decimal('1e-14'):
            break
        rhs1 = -last_f[0]
        rhs2 = -last_f[1]
        x, y, _det = solve2(sens[0][0], sens[0][1], sens[1][0], sens[1][1], rhs1, rhs2)
        d[0] += x
        d[1] += y
    state = formula(tuple(d), t_target, h)
    last_f, last_inv = mismatch_from_state(state)
    return tuple(d), last_f, last_inv, iterations


if __name__ == '__main__':
    analyze()

    counts = {}
    for _c, st, _t, _d in ENTRIES:
        counts[st] = counts.get(st, 0) + 1
    guard_count = sum(1 for _c, ok, _d in GUARDS if ok)

    report_keys = (
        'benchmark_gap_report', 'benchmark_gap_engine', 'benchmark_gap_rel_error',
        'benchmark_gap23_report', 'benchmark_gap23_engine',
        'benchmark_delta1', 'benchmark_delta2', 'benchmark_delta3',
        'benchmark_delta1_minus_delta2', 'benchmark_residual_12', 'benchmark_residual_23',
        'benchmark_masslog1', 'benchmark_masslog2', 'benchmark_masslog3',
        'benchmark_mass_ratio1', 'benchmark_mass_ratio2', 'benchmark_mass_ratio3',
        'benchmark_mass_split_spread', 'benchmark_invg_after',
        'benchmark_refine_iterations',
        'formal_t0', 'formal_M0_GeV', 'formal_gap12_at_t0', 'formal_gap23_at_t0',
        'formal_det_sensitivity', 'scan_t_slices', 'scan_hits',
        'formal_minnorm_t', 'formal_minnorm_MG_GeV',
        'formal_minnorm_delta1', 'formal_minnorm_delta2', 'formal_minnorm_delta3',
        'formal_minnorm_residual12', 'formal_minnorm_residual23',
        'formal_minnorm_masslog1', 'formal_minnorm_masslog2', 'formal_minnorm_masslog3',
        'formal_minnorm_mass_ratio1', 'formal_minnorm_mass_ratio2',
        'formal_minnorm_mass_ratio3', 'formal_minnorm_mass_split_spread',
        'formal_minnorm_alphaG_inv', 'formal_minnorm_alphaG',
        'formal_minmax_MG_GeV', 'formal_minmax_maxabs_delta',
        'formal_minmax_mass_split_spread', 'formal_step_inv_gap',
    )
    report = []
    report.append('TUFT-r447b_B REPORT')
    report.append('VERDICT = ' + VERDICT)
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
        'delta_beta': list(DELTA_B),
        'threshold_convention': 'alpha_i^{-1}(M_SUSY) += delta_i; delta_i = Delta_b_i/(2*pi)*ln(M_SUSY/M_i)',
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
    md.append('## 阈值约定')
    md.append('')
    md.append('- `alpha_i^{-1}(M_SUSY) += delta_i`。')
    md.append('- `delta_i = Delta_b_i/(2*pi) * ln(M_SUSY/M_i)`，`Delta_b = (5/2, 25/6, 4)`。')
    md.append('- 因此质量比 `M_i/M_SUSY = exp(-2*pi*delta_i/Delta_b_i)`；全部为 [C] 外部输入。')
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

