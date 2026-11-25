# -*- coding: utf-8 -*-
"""TUFT-r447c · 精确交汇微调量化与自然度审计（对来料的独立复核）。

复用 r447b_B 引擎（无副作用 import），机器裁定来料四项承重断言：
1. 来料把 r447 的 dL=0.4819 归因为「g2=g3 交点处 |inv1-inv2|」是否正确；
2. 来料「RMS ΔL_min≈0.41 且 μ* 与 g2=g3 偏差<0.5%」是否可复现；
3. 来料「二圈 MSSM 内 ΔL=0 数学上不可实现」是否被 r447b_C 的双阈值解反证；
4. 来料「SLSQP 全局最优 ΔL_min≈0.12」是否为真全局最优；
并用 Barbieri-Giudice 对数敏感度做自然度分级（δ 参数化，映射口径登记 BOUNDARY）。

这不是 TUFT 第一性导出：所有阈值、y_t 与误差口径均为 [C] 外部输入。
输出 json/md/report；Decimal 60 位 + Fraction beta 系数。
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
C_JSON = os.path.join(DATA, 'TUFT-r447b_C_精确交汇微调量化_2026-11-25.json')
R447_JSON = os.path.join(DATA, 'TUFT-r447_二圈RG阈值修正与质子衰变定价_MSSMbeta矩阵RK4积分_精算_2026-11-24.json')
STAMP = '2026-11-25'
TAG = 'TUFT-r447c_精确交汇微调量化与自然度审计_' + STAMP
VERDICT = ('R447C-INPUT-CLAIMS-AUDITED--DL-DEFINITION-MISATTRIBUTED--'
           'RMS-CLAIMS-NOT-REPRODUCED--EXACT-CROSSING-IS-ACHIEVABLE--'
           'SLSQP-012-NOT-GLOBAL--NATURALNESS-REGISTERED--PASS-NOT-FIRST-PRINCIPLE')

_spec = importlib.util.spec_from_file_location('b_engine_r447c', B_PATH)
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
    if isinstance(x, D):
        return format(x, '.25E')
    return str(x)


def jsonable(x):
    if isinstance(x, D):
        return fs(x)
    if isinstance(x, Fraction):
        return [x.numerator, x.denominator]
    if isinstance(x, (tuple, list)):
        return [jsonable(v) for v in x]
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    return x


def inv_vec(s):
    return tuple(b.inv_alpha_from_g(s[i]) for i in range(3))


def dl_rms(inv):
    m = (inv[0] + inv[1] + inv[2]) / D(3)
    return (((inv[0] - m) ** 2 + (inv[1] - m) ** 2 + (inv[2] - m) ** 2) / D(3)).sqrt()


def scan_rms(traj):
    best = None
    for t, s in traj:
        inv = inv_vec(s)
        r = dl_rms(inv)
        if best is None or r < best[0]:
            best = (r, t, inv)
    return best


def ref_gap_at_g23(traj):
    c = b.crossing(traj, 1, 2)
    if c is None:
        raise ValueError('no g2=g3 crossing')
    inv = inv_vec(c[1])
    return abs(inv[0] - inv[1]), c[0], inv


def pairwise_dl(traj):
    c12 = b.crossing(traj, 0, 1)
    c13 = b.crossing(traj, 0, 2)
    c23 = b.crossing(traj, 1, 2)
    if c12 is None or c13 is None or c23 is None:
        raise ValueError('pairwise crossings incomplete')
    ls = (c12[0], c13[0], c23[0])
    return max(ls) - min(ls), ls


def formal_no_y_traj(h):
    mz = D(b.INPUT['M_Z_GeV'])
    ms = D(b.INPUT['M_SUSY_GeV'])
    ts = ms.ln() - mz.ln()
    tmax = D(b.INPUT['M_X_max_GeV']).ln() - mz.ln()
    s0 = b.initial_formal_g() + (D(0),)
    t1 = b.integrate(D(0), s0, ts, h, b.beta_sm)
    t2 = b.integrate(ts, t1[-1][1], tmax, h,
                     lambda s: b.beta_mssm(s, (Fraction(0), Fraction(0), Fraction(0)), -1))
    return t1 + t2[1:]


def run_formal(delta, yt, h):
    """带外生阈值与指定 y_t 的 formal 轨迹。"""
    mz = D(b.INPUT['M_Z_GeV'])
    ms = D(b.INPUT['M_SUSY_GeV'])
    ts = ms.ln() - mz.ln()
    tmax = D(b.INPUT['M_X_max_GeV']).ln() - mz.ln()
    s0 = b.initial_formal_g() + (yt,)
    t1 = b.integrate(D(0), s0, ts, h, b.beta_sm)
    s_ms = b.apply_threshold_inv(t1[-1][1], delta)
    t2 = b.integrate(ts, s_ms, tmax, h, lambda s: b.beta_mssm(s, b.C_U_STD, -1))
    return t1 + t2[1:]


def outputs(delta, yt, h):
    traj = run_formal(delta, yt, h)
    c = b.crossing(traj, 1, 2)
    if c is None:
        raise ValueError('no g2=g3 crossing in perturbed run')
    inv = inv_vec(c[1])
    mg = D(b.INPUT['M_Z_GeV']) * c[0].exp()
    invg = (inv[1] + inv[2]) / D(2)
    rms = scan_rms(traj)[0]
    return mg, invg, rms


def bg_sensitivity(param_idx, h, step=D('1e-3')):
    """Barbieri-Giudice 对数敏感度（δ 参数化；idx 0..2=δ, 3=y_t）。"""
    yt0 = D(b.INPUT['y_t_MZ'])
    base = outputs(ZERO, yt0, h)

    def perturb(sign):
        delta = [D(0), D(0), D(0)]
        yt = yt0
        if param_idx < 3:
            delta[param_idx] = sign * step
        else:
            yt = yt0 * (D(1) + sign * step)
        return outputs(tuple(delta), yt, h)

    plus = perturb(1)
    minus = perturb(-1)
    den = D(2) * step
    sens = []
    for k in range(3):
        if plus[k] <= D(0) or minus[k] <= D(0):
            raise ValueError('BG log derivative requires positive output')
        dln = (plus[k].ln() - minus[k].ln()) / den
        sens.append(abs(dln))
    return base, sens


def analyze():
    h = D('0.01')
    h_coarse = D('0.02')

    guard('G0-1', hasattr(b, 'formal_state_target') and b.DELTA_B ==
          (Fraction(5, 2), Fraction(25, 6), Fraction(4)),
          'r447b_B engine imported without side effects')
    guard('G0-2', b.C_U_STD == (Fraction(26, 5), Fraction(6), Fraction(4)),
          'standard top Yukawa column locked')

    # 1) 复现 r447 原始 dL 口径
    r447 = json.load(io.open(R447_JSON, encoding='utf-8'))['key_numbers']
    dL_ref = D(r447['dL'])
    guard('A1-1', abs(dL_ref - D('0.4819077285193969628214751E+0')) < D('1e-12'),
          'r447 dL=0.4819 reproduced')

    traj = formal_no_y_traj(h)
    pairwise, crossings = pairwise_dl(traj)
    guard('A1-2', abs(pairwise - dL_ref) < D('1e-3'),
          'r447 dL is pairwise-crossing e-fold span: ' + fs(pairwise))
    ref_gap, t_ref, inv_ref = ref_gap_at_g23(traj)
    rel_gap_def = abs(ref_gap - dL_ref) / dL_ref
    guard('A1-3', rel_gap_def > D('0.01'),
          'input attribution |inv1-inv2| at g23 differs from r447 dL: ' + fs(rel_gap_def))

    # 2) RMS ΔL 最小值与 mu* 位置
    rms_best = scan_rms(traj)
    rms_min, t_rms, inv_rms = rms_best
    rel_t = abs(t_rms - t_ref) / t_ref
    guard('A2-1', rms_min > D(0), 'RMS mismatch positive')
    guard('A2-2', rel_t > D('0.005'),
          'input claim mu* vs g23 <0.5% fails: ' + fs(rel_t))
    guard('A2-3', abs(rms_min - D('0.41')) / D('0.41') > D('0.5'),
          'input claim RMS min ~0.41 fails: ' + fs(rms_min))

    # 3) 反证「ΔL=0 不可实现」
    cdata = json.load(io.open(C_JSON, encoding='utf-8'))['key_numbers']
    t_star = D(cdata['no_threshold_best_t'])
    d_pair = (D(cdata['pair_01_delta1']), D(cdata['pair_01_delta2']), D(0))
    s_pair = b.formal_state_target(d_pair, t_star, h_coarse)
    rms_pair = dl_rms(inv_vec(s_pair))
    guard('A3-1', rms_pair < D('1e-9'),
          'exact crossing achievable: RMS=' + fs(rms_pair))
    guard('A3-2', rms_min > D('0.01'), 'positive control: no-threshold RMS bounded away from zero')

    logs, spread = b.mass_price(d_pair)
    mass_geV = [D(b.INPUT['M_SUSY_GeV']) * x.exp() for x in logs]
    guard('A4-1', all(D('100') <= m <= D('10000') for m in mass_geV),
          'closing thresholds inside input-declared 100GeV..10TeV window')
    guard('A4-2', rms_pair < D('0.12'),
          'input SLSQP optimum 0.12 is not global: ' + fs(rms_pair))
    improvement = (rms_min - rms_pair) / rms_min
    guard('A4-3', improvement > D('0.99'), 'improvement exceeds input 71% claim')

    # 4) Barbieri-Giudice 敏感度（δ 参数化）
    yt0 = D(b.INPUT['y_t_MZ'])
    sens_rows = []
    for idx in range(4):
        base, sens = bg_sensitivity(idx, h)
        sens_rows.append(sens)
        for k in range(3):
            guard('B1-' + str(idx) + '-' + str(k), sens[k] >= D(0),
                  'BG sensitivity nonnegative')
    max_sens = [max(row[k] for row in sens_rows) for k in range(3)]
    guard('B2-1', max_sens[0] < D(10), 'MG naturalness Δ<10')
    guard('B2-2', max_sens[1] < D(10), 'inv_alphaG naturalness Δ<10')
    guard('B2-3', max_sens[2] < D(10), 'RMS mismatch naturalness Δ<10')

    # 步长检验：step 减半，BG 敏感度应收敛
    _base, s_half = bg_sensitivity(0, h, D('5e-4'))
    step_shift = max(abs(s_half[k] - sens_rows[0][k]) for k in range(3))
    guard('B3-1', step_shift < D('1e-3'), 'BG central difference step stable: ' + fs(step_shift))

    KEY.update({
        'r447_dL_ref': dL_ref,
        'r447_pairwise_dL_recomputed': pairwise,
        'ref_gap_at_g23': ref_gap,
        'ref_definition_rel_error': rel_gap_def,
        'rms_min_no_threshold': rms_min,
        'rms_best_t': t_rms,
        'rms_best_M_GeV': D(b.INPUT['M_Z_GeV']) * t_rms.exp(),
        'ref_g23_t': t_ref,
        'mu_star_rel_offset': rel_t,
        'rms_pair_exact': rms_pair,
        'exact_closing_delta1': d_pair[0],
        'exact_closing_delta2': d_pair[1],
        'exact_closing_mass1_GeV': mass_geV[0],
        'exact_closing_mass2_GeV': mass_geV[1],
        'exact_closing_mass3_GeV': mass_geV[2],
        'exact_improvement_over_rms_min': improvement,
        'input_claim_DL_opt': D('0.12'),
        'BG_MG_delta1': sens_rows[0][0], 'BG_inva_delta1': sens_rows[0][1], 'BG_DL_delta1': sens_rows[0][2],
        'BG_MG_delta2': sens_rows[1][0], 'BG_inva_delta2': sens_rows[1][1], 'BG_DL_delta2': sens_rows[1][2],
        'BG_MG_delta3': sens_rows[2][0], 'BG_inva_delta3': sens_rows[2][1], 'BG_DL_delta3': sens_rows[2][2],
        'BG_MG_yt': sens_rows[3][0], 'BG_inva_yt': sens_rows[3][1], 'BG_DL_yt': sens_rows[3][2],
        'BG_max_MG': max_sens[0], 'BG_max_inva': max_sens[1], 'BG_max_DL': max_sens[2],
        'BG_step_shift': step_shift,
    })
    AUX['r447_crossings'] = crossings
    AUX['rms_best_inv'] = list(inv_rms)
    AUX['ref_g23_inv'] = list(inv_ref)
    AUX['exact_closing_inv'] = list(inv_vec(s_pair))

    IN('I01', '[C] 外部输入登记', '超伴子阈值、y_t、实验误差与 100GeV~10TeV 搜索窗均为 [C] 外部输入')
    P('I02', 'r447 原始 ΔL 口径复现', 'pairwise crossing e-fold 跨度 ' + fs(pairwise) + '，与 0.4819 一致')
    CO('I03', '来料 ΔL 定义错归因', 'r447 的 0.4819 是 pairwise crossing 跨度，不是 g2=g3 处 |inv1−inv2|；后者 ' + fs(ref_gap) + '，相对差 ' + fs(rel_gap_def))
    P('I04', 'RMS ΔL 定义与实现', '三倒数耦合标准差，无自创定义')
    CO('I05', '来料 RMS≈0.41 与 μ*偏差<0.5% 不成立', '实测 RMS_min=' + fs(rms_min) + '，μ* 相对 g23 偏差 ' + fs(rel_t))
    CO('I06', '来料「二圈无法严格共点」被反证', 'r447b_C 双阈值解处 RMS=' + fs(rms_pair) + '，机器零')
    P('I07', '精确交汇可由外生阈值实现', 'δ1=' + fs(d_pair[0]) + '、δ2=' + fs(d_pair[1]) + '、δ3=0')
    P('I08', '闭合阈值在来料声明窗内', 'M1/M2/M3=' + ' / '.join(fs(m) for m in mass_geV) + ' GeV')
    CO('I09', '来料 SLSQP 0.12 非全局最优', '同参数窗内机器解 RMS=' + fs(rms_pair) + '，改善 ' + fs(improvement))
    P('I10', 'BG 对数敏感度实现', '中心差分 + step 减半稳定，最大偏移 ' + fs(step_shift))
    P('I11', '自然度分级', 'Δ(M_G)/Δ(1/α_G)/Δ(RMS) 最大 ' + ' / '.join(fs(x) for x in max_sens) + '，均 <10')
    BD('I12', '4 质量→δ 映射未给全', '来料未给 M_ew/M_hig/M_sfer/M_glu 到 δ_i 的显式映射；本册用等价 δ 参数化做自然度上界')
    IN('I13', '残余不匹配来源登记', '无阈值 RMS=' + fs(rms_min) + '，来源为二圈曲率差异；外生阈值可压到机器零，不是不可消除')
    IN('I14', 'r447 全卷收口状态', 'A/B/C/c 四册均落盘；c 只审计来料断言，不改前册字节')
    IN('I15', '全局记分板不变', '0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4')


analyze()

counts = {}
for _c, st, _t, _d in ENTRIES:
    counts[st] = counts.get(st, 0) + 1
guard_count = sum(1 for _c, ok, _d in GUARDS if ok)

report_keys = (
    'r447_dL_ref', 'r447_pairwise_dL_recomputed', 'ref_gap_at_g23',
    'ref_definition_rel_error', 'rms_min_no_threshold', 'rms_best_t',
    'rms_best_M_GeV', 'ref_g23_t', 'mu_star_rel_offset', 'rms_pair_exact',
    'exact_closing_delta1', 'exact_closing_delta2',
    'exact_closing_mass1_GeV', 'exact_closing_mass2_GeV', 'exact_closing_mass3_GeV',
    'exact_improvement_over_rms_min', 'input_claim_DL_opt',
    'BG_MG_delta1', 'BG_inva_delta1', 'BG_DL_delta1',
    'BG_MG_delta2', 'BG_inva_delta2', 'BG_DL_delta2',
    'BG_MG_delta3', 'BG_inva_delta3', 'BG_DL_delta3',
    'BG_MG_yt', 'BG_inva_yt', 'BG_DL_yt',
    'BG_max_MG', 'BG_max_inva', 'BG_max_DL', 'BG_step_shift',
)
report = ['TUFT-r447c REPORT', 'VERDICT = ' + VERDICT]
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
    'inherited_from': ['r447', 'r447b_B', 'r447b_C'],
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
