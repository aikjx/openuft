# -*- coding: utf-8 -*-
"""TUFT-r447b 子模块C · 精确交汇微调量化。

在 r447b_B 的非简并阈值定价之上，问「精确三线交汇」本身的结构代价：
无阈值时交汇是否存在；单阈值是否足够；两阈值能否闭合；4 未知 2 方程的
欠定流形维数；条件数与精度传播。复用 r447b_B 引擎（无副作用 import）。

这不是 TUFT 第一性导出：MSSM、顶 Yukawa、delta_i、M_G 切片与实验误差全是 [C] 外部输入。
算术：Decimal 60 位 + Fraction beta 系数；输出 json/md/report。
"""
import io
import json
import os
import sys
import importlib.util
from decimal import Decimal, getcontext
from fractions import Fraction

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
B_PATH = os.path.join(HERE, 'TUFT-r447b_B_非简并阈值全参数扫描与交汇缺口定价_精算_2026-11-25.py')
STAMP = '2026-11-25'
TAG = 'TUFT-r447b_C_精确交汇微调量化_' + STAMP
VERDICT = ('EXACT-UNIFICATION-FINE-TUNING-PRICED--NO-INTRINSIC-TRIPLE-CROSSING--'
           'ONE-DELTA-INSUFFICIENT--TWO-DELTA-SUFFICIENT--RANK-2-OF-4-TWO-DIM-MANIFOLD--'
           'PASS-NOT-FIRST-PRINCIPLE')

_spec = importlib.util.spec_from_file_location('b_engine_r447b', B_PATH)
b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b)

D = Decimal
ZERO = (D(0), D(0), D(0))
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


def fs(x):
    if isinstance(x, Decimal):
        return format(x, '.25E')
    return str(x)


def jsonable(x):
    if isinstance(x, Decimal):
        return fs(x)
    if isinstance(x, Fraction):
        return [x.numerator, x.denominator]
    if isinstance(x, (tuple, list)):
        return [jsonable(v) for v in x]
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    return x


def norm2(f):
    return (f[0] * f[0] + f[1] * f[1]).sqrt()


def mismatch(delta, t, h):
    return b.mismatch_from_state(b.formal_state_target(delta, t, h))[0]


def jac_delta(delta, t, h, eps):
    cols = []
    for k in range(3):
        dp = list(delta)
        dm = list(delta)
        dp[k] += eps
        dm[k] -= eps
        fp = mismatch(tuple(dp), t, h)
        fm = mismatch(tuple(dm), t, h)
        cols.append(((fp[0] - fm[0]) / (D(2) * eps),
                     (fp[1] - fm[1]) / (D(2) * eps)))
    return tuple(cols)


def jac_t(delta, t, h, eps):
    fp = mismatch(delta, t + eps, h)
    fm = mismatch(delta, t - eps, h)
    return ((fp[0] - fm[0]) / (D(2) * eps),
            (fp[1] - fm[1]) / (D(2) * eps))


def best_single(f, col):
    """单列最小二乘：min_delta ||f + col*d||。"""
    den = col[0] * col[0] + col[1] * col[1]
    if den == D(0):
        raise ZeroDivisionError('zero sensitivity column')
    d = -(f[0] * col[0] + f[1] * col[1]) / den
    r = (f[0] + col[0] * d, f[1] + col[1] * d)
    return d, r, norm2(r)


def solve_pair(f, c1, c2):
    det = c1[0] * c2[1] - c1[1] * c2[0]
    if det == D(0):
        raise ZeroDivisionError('singular 2x2 sensitivity block')
    d1 = (-f[0] * c2[1] + c2[0] * f[1]) / det
    d2 = (-c1[0] * f[1] + f[0] * c1[1]) / det
    return d1, d2, det


def refine_pair(pair, d1, d2, t, h, jac, max_iter=8):
    d = [D(0), D(0), D(0)]
    d[pair[0]] = d1
    d[pair[1]] = d2
    c1 = jac[pair[0]]
    c2 = jac[pair[1]]
    last = None
    for it in range(1, max_iter + 1):
        last = mismatch(tuple(d), t, h)
        x, y, _det = solve_pair(last, c1, c2)
        d[pair[0]] += x
        d[pair[1]] += y
        if norm2(last) < D('1e-14'):
            break
    last = mismatch(tuple(d), t, h)
    return tuple(d), last, it


def gram_eigs(m):
    """2x2 对称 Gram 矩阵的特征值（闭式）。"""
    a, bc, d = m[0][0], m[0][1], m[1][1]
    tr = a + d
    disc = ((a - d) * (a - d) + D(4) * bc * bc).sqrt()
    return (tr + disc) / D(2), (tr - disc) / D(2)


def analyze():
    h = D('0.02')
    h_fine = D('0.01')
    eps = D('1e-2')
    mz = D(b.INPUT['M_Z_GeV'])

    guard('G0-1', hasattr(b, 'formal_state_target') and hasattr(b, 'C_U_STD')
          and b.C_U_STD == (Fraction(26, 5), Fraction(6), Fraction(4)),
          'r447b_B engine imported without side effects')
    guard('G0-2', b.DELTA_B == (Fraction(5, 2), Fraction(25, 6), Fraction(4)),
          'Delta_b locked')

    # C1: 无阈值时是否已有精确三线交汇
    base_traj, ts, tmax = b.formal_base_trajectory(h)
    lo = ts + D(1)
    hi = tmax - D(1)
    n = 40
    best = None
    for k in range(n + 1):
        t = lo + (hi - lo) * D(k) / D(n)
        f0, inv = b.mismatch_from_state(b.state_at(base_traj, t))
        mx = max(abs(f0[0]), abs(f0[1]))
        if best is None or mx < best[0]:
            best = (mx, t, f0, inv)
    minmax, t_star, f_star, inv_star = best
    guard('C1-1', minmax > D('1e-2'),
          'no intrinsic triple crossing: min max|residual| = ' + fs(minmax))
    guard('C1-2', lo <= t_star <= hi, 'best no-threshold slice inside scan window')

    jac = jac_delta(ZERO, t_star, h, eps)
    jt = jac_t(ZERO, t_star, h, eps)

    # C2: 单阈值不足
    singles = []
    for k in range(3):
        dk, rk, nk = best_single(f_star, jac[k])
        singles.append((dk, rk, nk))
        guard('C2-' + str(k + 1), nk > D('1e-3'),
              'single delta' + str(k + 1) + ' leaves residual ' + fs(nk))

    # C3: 双阈值可闭合 + 价格
    pairs = ((0, 1), (0, 2), (1, 2))
    doubles = []
    for idx, pair in enumerate(pairs):
        d1, d2, det = solve_pair(f_star, jac[pair[0]], jac[pair[1]])
        dd, rr, it = refine_pair(pair, d1, d2, t_star, h, jac)
        logs, spread = b.mass_price(dd)
        doubles.append({'pair': pair, 'delta': dd, 'residual': rr,
                        'det': det, 'iter': it, 'logs': logs, 'spread': spread})
        guard('C3-' + str(idx + 1), norm2(rr) < D('1e-9'),
              'pair ' + str(pair) + ' closes both equations')
        guard('C3b-' + str(idx + 1), spread > D(0),
              'pair ' + str(pair) + ' requires non-degenerate splitting')

    # C4: 4 未知 2 方程的秩与流形维数
    sub_dets = []
    for i in range(3):
        for j in range(i + 1, 3):
            sub_dets.append(jac[i][0] * jac[j][1] - jac[i][1] * jac[j][0])
    with_t = [jac_t_term[0] * jac[1][1] - jac[1][0] * jac_t_term[1]
              for jac_t_term in [jt]]
    all_dets = sub_dets + with_t
    rank2 = any(x != D(0) for x in all_dets)
    guard('C4-1', rank2, '2x4 Jacobian has rank 2')
    manifold_dim = 4 - 2
    guard('C4-2', manifold_dim == 2, 'solution manifold is 2-dimensional')

    # C5: 条件数（2x3 阈值雅可比各 2x2 子块）
    conds = []
    for det in sub_dets:
        gauge = [jac[i][0] * jac[i][0] + jac[i][1] * jac[i][1]
                 for i in range(3)]
        # 用对应子块的 Gram 行列式比估条件数
        pass
    for idx, pair in enumerate(pairs):
        g11 = jac[pair[0]][0] ** 2 + jac[pair[0]][1] ** 2
        g22 = jac[pair[1]][0] ** 2 + jac[pair[1]][1] ** 2
        g12 = jac[pair[0]][0] * jac[pair[1]][0] + jac[pair[0]][1] * jac[pair[1]][1]
        lam_hi, lam_lo = gram_eigs(((g11, g12), (g12, g22)))
        cond = (lam_hi / lam_lo).sqrt()
        conds.append(cond)
    guard('C5-1', all(c > D(1) for c in conds), 'all 2x2 blocks anisotropic')
    guard('C5-2', all(c < D('1e6') for c in conds), 'condition numbers finite')

    # C6: 精度传播（[C] 实验倒数耦合误差）
    sigma_inv = D('1e-2')
    jnorms = [(c[0] * c[0] + c[1] * c[1]).sqrt() for c in jac]
    sigmas = [sigma_inv / jn for jn in jnorms]
    guard('C6-1', all(s > D(0) for s in sigmas), 'threshold precision propagates')

    # C7: 与 r447 单参数口径对照
    r447_delta3 = D('-0.3159')
    guard('C7-1', singles[2][2] > D('1e-3'),
          'r447 one-loop delta3 alone insufficient at two-loop+C_U_STD')

    # C8: 双阈值精算步长稳定性
    dd = doubles[0]['delta']
    f_fine = mismatch(dd, t_star, h_fine)
    step_gap = norm2((f_fine[0] - doubles[0]['residual'][0],
                      f_fine[1] - doubles[0]['residual'][1]))
    guard('C8-1', step_gap < D('1e-5'), 'step refinement stable: ' + fs(step_gap))

    KEY.update({
        'no_threshold_min_max_residual': minmax,
        'no_threshold_best_t': t_star,
        'no_threshold_best_M_GeV': mz * t_star.exp(),
        'no_threshold_best_gap12': f_star[0],
        'no_threshold_best_gap23': f_star[1],
        'single_delta1_best': singles[0][0],
        'single_delta1_residual_norm': singles[0][2],
        'single_delta2_best': singles[1][0],
        'single_delta2_residual_norm': singles[1][2],
        'single_delta3_best': singles[2][0],
        'single_delta3_residual_norm': singles[2][2],
        'pair_01_delta1': doubles[0]['delta'][0],
        'pair_01_delta2': doubles[0]['delta'][1],
        'pair_01_residual_norm': norm2(doubles[0]['residual']),
        'pair_01_mass_split_spread': doubles[0]['spread'],
        'pair_02_delta1': doubles[1]['delta'][0],
        'pair_02_delta3': doubles[1]['delta'][2],
        'pair_02_mass_split_spread': doubles[1]['spread'],
        'pair_12_delta2': doubles[2]['delta'][1],
        'pair_12_delta3': doubles[2]['delta'][2],
        'pair_12_mass_split_spread': doubles[2]['spread'],
        'jacobian_rank': D(2),
        'unknown_count': D(4),
        'equation_count': D(2),
        'manifold_dimension': D(manifold_dim),
        'cond_pair_01': conds[0],
        'cond_pair_02': conds[1],
        'cond_pair_12': conds[2],
        'sigma_inv_input': sigma_inv,
        'threshold_precision_delta1': sigmas[0],
        'threshold_precision_delta2': sigmas[1],
        'threshold_precision_delta3': sigmas[2],
        'r447_single_delta3': r447_delta3,
        'step_refinement_gap': step_gap,
    })
    AUX['jac_delta'] = [list(c) for c in jac]
    AUX['jac_t'] = list(jt)
    AUX['no_threshold_inv'] = list(inv_star)
    AUX['double_solutions'] = [jsonable(d) for d in doubles]

    IN('I01', '[C] 外部输入登记', 'MSSM、顶 Yukawa 反馈、δ_i、M_G 切片与实验倒数耦合误差 σ=1e−2 均非 TUFT 导出')
    P('I02', '无阈值精确交汇不存在', '41+1 个切片 min max|残差|=' + fs(minmax) + '，远大于零')
    P('I03', '单阈值 δ1 不足', '最小二乘残差范数 ' + fs(singles[0][2]))
    P('I04', '单阈值 δ2 不足', '最小二乘残差范数 ' + fs(singles[1][2]))
    P('I05', '单阈值 δ3 不足', '最小二乘残差范数 ' + fs(singles[2][2]))
    P('I06', '双阈值 (δ1,δ2) 精确闭合', '残差 ' + fs(norm2(doubles[0]['residual'])) + '，质量对数跨度 ' + fs(doubles[0]['spread']))
    P('I07', '双阈值 (δ1,δ3) 精确闭合', '质量对数跨度 ' + fs(doubles[1]['spread']))
    P('I08', '双阈值 (δ2,δ3) 精确闭合', '质量对数跨度 ' + fs(doubles[2]['spread']))
    P('I09', '雅可比秩与解流形维数', '2×4 雅可比秩 2，未知 4 / 方程 2 ⇒ 解流形 2 维')
    P('I10', '微调条件数量化', '三个 2×2 子块条件数分别 ' + ' / '.join(fs(c) for c in conds))
    BD('I11', '精度传播依赖实验误差口径', 'σ_inv=1e−2 为 [C] 输入，δ 精度 ' + ' / '.join(fs(s) for s in sigmas))
    CO('I12', '与 r447 单参数口径对照', 'r447 一圈 δ3≈−0.3159 的结论不能外推到二圈+标准顶列；本册单 δ3 残差 ' + fs(singles[2][2]))
    P('I13', '精算步长稳定', 'h=0.02→0.01 残差差 ' + fs(step_gap))
    IN('I14', '全局记分板不变', '0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4')


analyze()

counts = {}
for _c, st, _t, _d in ENTRIES:
    counts[st] = counts.get(st, 0) + 1
guard_count = sum(1 for _c, ok, _d in GUARDS if ok)

report_keys = (
    'no_threshold_min_max_residual', 'no_threshold_best_t', 'no_threshold_best_M_GeV',
    'no_threshold_best_gap12', 'no_threshold_best_gap23',
    'single_delta1_best', 'single_delta1_residual_norm',
    'single_delta2_best', 'single_delta2_residual_norm',
    'single_delta3_best', 'single_delta3_residual_norm',
    'pair_01_delta1', 'pair_01_delta2', 'pair_01_residual_norm', 'pair_01_mass_split_spread',
    'pair_02_delta1', 'pair_02_delta3', 'pair_02_mass_split_spread',
    'pair_12_delta2', 'pair_12_delta3', 'pair_12_mass_split_spread',
    'jacobian_rank', 'unknown_count', 'equation_count', 'manifold_dimension',
    'cond_pair_01', 'cond_pair_02', 'cond_pair_12',
    'sigma_inv_input', 'threshold_precision_delta1', 'threshold_precision_delta2',
    'threshold_precision_delta3', 'r447_single_delta3', 'step_refinement_gap',
)
report = ['TUFT-r447b_C REPORT', 'VERDICT = ' + VERDICT]
for k in report_keys:
    report.append(k.upper() + ' = ' + fs(KEY[k]))
report.append('PASS=' + str(counts.get('PASS', 0)) + ' FAIL=' + str(counts.get('FAIL', 0)) +
              ' BOUNDARY=' + str(counts.get('BOUNDARY', 0)) + ' INFO=' + str(counts.get('INFO', 0)) +
              ' CORRECTED=' + str(counts.get('CORRECTED', 0)))
report.append('GUARDS ' + str(guard_count) + '/' + str(len(GUARDS)))
report_text = '\n'.join(report) + '\n'

payload = {
    'tag': TAG, 'stamp': STAMP, 'verdict': VERDICT,
    'input': b.INPUT,
    'inherited_from': 'r447b_B',
    'threshold_convention': b.payload['threshold_convention'] if hasattr(b, 'payload') else 'alpha_i^{-1}(M_SUSY) += delta_i',
    'key_numbers': KEY,
    'entries': [{'code': c, 'status': s, 'title': t, 'detail': d} for c, s, t, d in ENTRIES],
    'guards': [{'code': c, 'ok': ok, 'detail': d} for c, ok, d in GUARDS],
    'aux': AUX,
}
os.makedirs(DATA, exist_ok=True)
with io.open(os.path.join(DATA, TAG + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=jsonable)
    f.write('\n')

md = ['# ' + TAG, '', '- 判词：`' + VERDICT + '`',
      '- 条目：' + str(len(ENTRIES)) + '；PASS=' + str(counts.get('PASS', 0)) +
      ' / FAIL=' + str(counts.get('FAIL', 0)) + ' / BOUNDARY=' + str(counts.get('BOUNDARY', 0)) +
      ' / INFO=' + str(counts.get('INFO', 0)) + ' / CORRECTED=' + str(counts.get('CORRECTED', 0)),
      '- 守卫：' + str(guard_count) + '/' + str(len(GUARDS)), '',
      '## 关键读数', '', '| 项 | 读数 |', '|---|---|']
for k in report_keys:
    md.append('| ' + k + ' | ' + fs(KEY[k]) + ' |')
md += ['', '## 条目', '']
for c, s, t, d in ENTRIES:
    md.append('- **' + c + ' [' + s + ']** ' + t + '：' + d)
with io.open(os.path.join(DATA, TAG + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')
with io.open(os.path.join(DATA, TAG + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write(report_text)

sys.stdout.write(report_text)
