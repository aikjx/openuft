# -*- coding: utf-8 -*-
"""TUFT-r139 · 攻坚线全维总总结 与 统一场论终局裁定（2026-10-21）

分工声明
--------
* r136 = 并行会话《力的大统一方程·非GUT候选族补齐与全链路终局账本》；
* r138 = 并行会话《硬核审计·②规范群 与 ③μ² 符号的不可导出性》。
* 本册 r139 为**总总结卷**：不新开战线，只做三件事——
  (a) 全攻坚线（r98–r138）判定册机读清点；
  (b) 七条完成判据 + 前提账本 + 净前提下降门的**跨册复算与合账**；
  (c) 对「是否已实现统一场论」给出机读终局裁定。
* **各源卷拥有其条目；本册条目与任何源卷不可相加**（non-additivity freeze）。
* 红线：数学自洽 ≠ 实验证实。本册不产出新物理。

退出码：全部守卫通过 ⇒ 0；任一守卫失败 ⇒ 1。
"""
import io
import json
import os
import re
import sys
from datetime import datetime

from mpmath import mp, mpf, log10, sqrt, pi, exp

# Windows GBK 控制台：τ、² 等字符会让 print 抛 UnicodeEncodeError 并吞掉真正的检查结果
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

mp.dps = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DIR_DATA = os.path.join(BASE, '数据')
DIR_VERDICT = os.path.join(BASE, '判定')
STEM = 'TUFT-r139_攻坚线全维总总结与统一场论终局裁定_2026-10-21'
NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

F_R119 = os.path.join(DIR_DATA, 'TUFT-r119_统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.json')
F_R130 = os.path.join(DIR_DATA, 'TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.json')
F_R133 = os.path.join(DIR_DATA, 'TUFT-r133_修补失敗元原理_修改逐个审计与结构不可修补定理_2026-10-20.json')
F_R135 = os.path.join(DIR_DATA, 'TUFT-r135_第一性原理突破尝试_无质量自旋2导出EH与SEP及净前提下降门机检_2026-10-21.json')
F_R138 = os.path.join(DIR_DATA, 'TUFT-r138_硬核审计_规范群与mu2符号的第一性原理可导出性精算_2026-10-21.json')


def _load(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


r119 = _load(F_R119)
r130 = _load(F_R130)
r133 = _load(F_R133)
r135 = _load(F_R135)
r138 = _load(F_R138)

items = []          # 机读条目
guards = []         # 守卫
computations = {}


def add(iid, name, value, verdict, note=''):
    items.append({'id': iid, 'name': name, 'value': value,
                  'verdict': verdict, 'note': note})
    print('  [%s] %-6s %-52s %s' % (iid, verdict, name[:52], value))


def guard(gid, ok, desc):
    guards.append({'id': gid, 'passed': bool(ok), 'desc': desc})
    return bool(ok)


print('=' * 78)
print('TUFT-r139 · 攻坚线全维总总结 与 统一场论终局裁定')
print('=' * 78)

# ────────────────────────────────────────────────────────────────
# §1 全攻坚线判定册机读清点
# ────────────────────────────────────────────────────────────────
print('\n§1 全攻坚线判定册机读清点')

CAT = re.compile(r'\b(PASS|FAIL|BOUNDARY|INFO|CORRECTED|CONFIRMED)\s+(\d+)')
LEDGER = []


def _scan_dir(d):
    if not os.path.isdir(d):
        return
    for name in sorted(os.listdir(d)):
        if not (name.startswith('判定_') and name.endswith('.md')):
            continue
        m = re.search(r'r(\d+)', name)
        if not m:
            continue
        body = io.open(os.path.join(d, name), encoding='utf-8-sig', errors='replace').read()
        # 取「条目 N（PASS a / FAIL b / …）」所在的同一括号块
        counts = {}
        blk = body
        m2 = re.search(r'条目[^\n]{0,160}', blk)
        if m2:
            blk = m2.group(0)
        for k, v in CAT.findall(blk):
            counts[k] = counts.get(k, 0) + int(v)
        g = re.search(r'守卫\s*(\d+)\s*/\s*(\d+)', body)
        LEDGER.append({
            'r': int(m.group(1)),
            'file': os.path.relpath(os.path.join(d, name), BASE).replace('\\', '/'),
            'counts': counts,
            'guards': (int(g.group(1)), int(g.group(2))) if g else None,
        })


_scan_dir(BASE)
_scan_dir(DIR_VERDICT)
_scan_dir(DIR_DATA)

seen = {}
for rec in LEDGER:
    key = (rec['r'], os.path.basename(rec['file']))
    seen[key] = rec
LEDGER = sorted(seen.values(), key=lambda x: x['r'])

agg = {}
for rec in LEDGER:
    for k, v in rec['counts'].items():
        agg[k] = agg.get(k, 0) + v
guards_total = sum(r['guards'][1] for r in LEDGER if r['guards'])
guards_passed = sum(r['guards'][0] for r in LEDGER if r['guards'])
shortfall = [{'r': r['r'], 'file': r['file'], 'guards': '%d/%d' % r['guards']}
             for r in LEDGER if r['guards'] and r['guards'][0] != r['guards'][1]]
n_line = sum(1 for r in LEDGER if r['r'] >= 98)

print('  判定册 %d 份，编号 r%d–r%d（其中本轮攻坚线 r98+ 共 %d 份）'
      % (len(LEDGER), LEDGER[0]['r'], LEDGER[-1]['r'], n_line))
print('  条目聚合：%s' % agg)
print('  守卫聚合：%d/%d' % (guards_passed, guards_total))
computations['ledger'] = {
    'n_verdict_volumes': len(LEDGER),
    'r_min': LEDGER[0]['r'], 'r_max': LEDGER[-1]['r'],
    'n_volumes_r98plus': n_line,
    'item_counts': agg,
    'guards_passed': guards_passed, 'guards_total': guards_total,
    'guard_shortfall_volumes': shortfall,
    'volumes': LEDGER,
}
add('L01', '全库判定册总数', '%d（r%d–r%d；本轮攻坚线 r98+ 共 %d 份）'
    % (len(LEDGER), LEDGER[0]['r'], LEDGER[-1]['r'], n_line), 'INFO')
add('L02', '条目聚合（PASS/FAIL/BOUNDARY/INFO…）',
    ' '.join('%s=%d' % (k, v) for k, v in sorted(agg.items())), 'INFO')
add('L03', '守卫聚合', '%d/%d' % (guards_passed, guards_total), 'INFO')

# ────────────────────────────────────────────────────────────────
# §2 七条完成判据的跨册复核（含控制组）
# ────────────────────────────────────────────────────────────────
print('\n§2 七条完成判据复核（r119 机读 + 本册复算）')

v = r119['verdict']
target_pass, target_total = v['target_pass'], v['target_total']
ctrl_pass, ctrl_total = v['control_pass'], v['control_total']
criteria = [{'id': c['id'], 'name': c['name'], 'verdict': c['verdict']}
            for c in r119['criteria_target']]
for c in criteria:
    add('U%s' % c['id'][1:] if c['id'].startswith('U') else c['id'],
        c['name'], c['verdict'], c['verdict'])
add('Ctl1', '电弱控制组通过率', '%g/%g = %g' % (ctrl_pass, ctrl_total, mpf(ctrl_pass) / ctrl_total),
    'PASS' if mpf(ctrl_pass) == ctrl_total else 'FAIL',
    '控制组 6/6 ⇒ 七条判据确有判别力（不是「谁都不给过」的空判据）')
add('Ctl3', '判据区分度（靶 vs 控制组）',
    'target %g/%g vs control %g/%g' % (target_pass, target_total, ctrl_pass, ctrl_total),
    'PASS' if (mpf(ctrl_pass) / ctrl_total) > (mpf(target_pass) / target_total) else 'FAIL')

# ────────────────────────────────────────────────────────────────
# §3 独立 250 位复算（不走 r119 的中间量，只走原始常数）
# ────────────────────────────────────────────────────────────────
print('\n§3 独立 250 位复算')

E_Pl = mpf('1.22089e19')          # GeV, CODATA-2018（r119 data.planck 同源）
M_GUT = mpf('2.014e16')           # GeV, MSSM 一圈统一（r119 data.gut_mssm）
alpha_GUT_inv = mpf('24.3')
alpha_GUT = 1 / alpha_GUT_inv
u3 = r119['U3_gravity']

alpha_G_at_MGUT = (M_GUT / E_Pl) ** 2
dex_gap = log10(alpha_GUT / alpha_G_at_MGUT)
rel_aG = abs(alpha_G_at_MGUT - mpf(repr(u3['alpha_G_at_MGUT']))) / mpf(repr(u3['alpha_G_at_MGUT']))
print('  α_G(M_GUT) 本册 %s ｜ r119 %s ｜ 相对残差 %s' %
      (mp.nstr(alpha_G_at_MGUT, 12), u3['alpha_G_at_MGUT'], mp.nstr(rel_aG, 6)))
# 容差说明：r119 的 json 只落 6 位有效数字（2.72123e-06），故残差下界就是它的存储精度 ~1e-6，
# 容差按存储精度放宽到 5e-6，而不是把它当成真分歧。
tol_aG = mpf('5e-6')
computations['N1_alpha_G_at_MGUT'] = {
    'this': mp.nstr(alpha_G_at_MGUT, 30), 'r119': u3['alpha_G_at_MGUT'],
    'rel_diff': float(rel_aG), 'tolerance': float(tol_aG),
    'tolerance_basis': 'r119 json 仅存 6 位有效数字 ⇒ 残差下界即其存储精度 ~1e-6',
    'formula': 'α_G(E) = (E/E_Pl)^2'}
add('N1', 'α_G(M_GUT) = (M_GUT/E_Pl)²', mp.nstr(alpha_G_at_MGUT, 12),
    'PASS' if rel_aG < tol_aG else 'FAIL',
    '与 r119 相对残差 %s（容差 %s，按 r119 存储精度定）' % (mp.nstr(rel_aG, 6), mp.nstr(tol_aG, 3)))

dex_gap_r119 = mpf(repr(u3['dex_gap']))
d_dex = abs(dex_gap - dex_gap_r119)
print('  dex_gap 本册 %s ｜ r119 %s ｜ 差 %s' %
      (mp.nstr(dex_gap, 10), u3['dex_gap'], mp.nstr(d_dex, 6)))
computations['N2_dex_gap'] = {'this': mp.nstr(dex_gap, 30), 'r119': u3['dex_gap'],
                              'abs_diff': float(d_dex)}
add('N2', '引力间隙 dex = log10(α_GUT/α_G(M_GUT))', mp.nstr(dex_gap, 10),
    'PASS' if d_dex < mpf('1e-3') else 'FAIL', '与 r119 差 %s dex' % mp.nstr(d_dex, 6))

sm = r119['data']['sm_unification_failure']
sigma = (mpf(repr(sm['alpha_s_obs'])) - mpf(repr(sm['alpha_s_pred']))) / mpf(repr(sm['alpha_s_unc']))
d_sig = abs(sigma - mpf(repr(sm['sigma'])))
computations['N3_alpha_s_sigma'] = {'this': mp.nstr(sigma, 30), 'r119': sm['sigma'],
                                    'abs_diff': float(d_sig)}
add('N3', 'α_s 偏离（α_s^pred vs 观测）σ', mp.nstr(sigma, 8),
    'PASS' if d_sig < mpf('1e-2') else 'FAIL', '与 r119 差 %s σ' % mp.nstr(d_sig, 6))

pd_ = r119['data']['proton_decay']
dex_now = log10(mpf(repr(pd_['tau_p_pred_yr'])) / mpf(repr(pd_['tau_p_limit_yr'])))
dex_near = log10(mpf(repr(pd_['tau_p_pred_yr'])) / mpf('1e35'))
computations['N4_proton_decay'] = {
    'tau_p_pred_yr': pd_['tau_p_pred_yr'], 'tau_p_limit_yr': pd_['tau_p_limit_yr'],
    'dex_over_current_limit': float(dex_now), 'dex_over_near_future_1e35': float(dex_near),
    'note': 'r119 登记的 0.53 dex 是「超近期可及 1e35 yr」口径；对当前上限 2.4e34 yr 为 1.15 dex'}
add('N4', 'τ_p 预言超界（两种口径）',
    'vs 当前上限 %.2f dex ｜ vs 近期可及 1e35 yr %.2f dex' % (dex_now, dex_near), 'FAIL',
    '无论哪一口径，唯一预言链都落在可及窗口之外 ⇒ U6 无判别力')

# 电弱控制组：树图自洽解 vs 实测（偏差即辐射修正 Δr）
M_Z = mpf(repr(r119['data']['electroweak']['M_Z_GeV']))
M_W_obs = mpf(repr(r119['data']['electroweak']['M_W_GeV']))
s2 = mpf(repr(r119['data']['electroweak']['sin2theta_MSbar']))
G_F = mpf(repr(r119['data']['electroweak']['G_F_GeV^-2']))
alpha_inv_MZ = mpf('127.95')          # α^{-1}(M_Z) MS-bar（外部常数，登记用）
alpha_MZ = 1 / alpha_inv_MZ

# 树图自洽关系：M_W² (1 − M_W²/M_Z²) = π α / (√2 G_F)
# 解 x(1 − x/M_Z²) = c  ⇒  x² − M_Z² x + c M_Z² = 0，取小根（物理支）
c_rhs = pi * alpha_MZ / (sqrt(2) * G_F)
disc = M_Z ** 4 - 4 * c_rhs * M_Z ** 2
# 二次方程有两根：大根 = M_W（物理支），小根 = 44 GeV 的伪支（W/Z 互换解），取大根
M_W_tree = sqrt((M_Z ** 2 + sqrt(disc)) / 2)
s2_tree = 1 - M_W_tree ** 2 / M_Z ** 2
dev_dr = abs(M_W_tree - M_W_obs) / M_W_obs             # 树图 vs 实测 = 辐射修正量级
# 口径自检：MS-bar sin²θ 与树图 sin²θ 不是同一个量，其差即方案差（教科书已知）
scheme_gap = abs(s2 - s2_tree)
computations['N5_electroweak_tree'] = {
    'M_Z_GeV': float(M_Z), 'M_W_obs_GeV': float(M_W_obs), 'G_F_GeV^-2': float(G_F),
    'alpha_inv_MZ': float(alpha_inv_MZ), 'sin2theta_MSbar': float(s2),
    'M_W_tree_GeV': mp.nstr(M_W_tree, 30), 'sin2theta_tree': mp.nstr(s2_tree, 30),
    'rel_dev_tree_vs_obs': float(dev_dr),
    'scheme_gap_MSbar_minus_tree': float(scheme_gap),
    'note': ('树图自洽解与实测之差即辐射修正 Δr（教科书量级 ~1%）；'
             'MS-bar 与树图 sin²θ 不是同一量，直接混用会伪造 0.35% 的假分歧')}
add('N5', '电弱树图自洽解 M_W^tree vs 实测',
    '%s vs %s ｜ 相对 %s' % (mp.nstr(M_W_tree, 10), mp.nstr(M_W_obs, 10), mp.nstr(dev_dr, 6)),
    'PASS' if (dev_dr > 0 and dev_dr < mpf('2e-2')) else 'FAIL',
    '差值即辐射修正 Δr（0 < 偏差 < 2%%）；MS-bar/树图 sin²θ 方案差 %s，两者不可混用'
    % mp.nstr(scheme_gap, 6))

# U(1)_Y Landau 极点（一圈，GUT 归一化）
b1 = mpf(41) / 10
alpha1_inv_MZ = mpf('59.0')           # α_1^{-1}(M_Z)（GUT 归一化，PDG 口径；登记为外部输入）
ln_ratio = 2 * pi * alpha1_inv_MZ / b1
Lambda_U1 = M_Z * exp(ln_ratio)
over_planck = log10(Lambda_U1 / E_Pl)
g2 = r138['checks']['G2']
rel_landau = abs(Lambda_U1 - mpf(repr(g2['u1_landau_gev']))) / mpf(repr(g2['u1_landau_gev']))
computations['N6_U1_landau'] = {
    'b1': '41/10', 'alpha1_inv_MZ': float(alpha1_inv_MZ),
    'Lambda_GeV': mp.nstr(Lambda_U1, 30), 'r138': g2['u1_landau_gev'],
    'rel_diff': float(rel_landau),
    'log10_over_planck': float(over_planck), 'r138_log10_over_planck': g2['log10_ratio_over_planck']}
add('N6', 'U(1)_Y 一圈 Landau 极点',
    '%s GeV ｜ 跨普朗克 %s dex' % (mp.nstr(Lambda_U1, 10), mp.nstr(over_planck, 8)),
    'PASS' if rel_landau < mpf('5e-2') else 'FAIL',
    '与 r138 相对残差 %s；跨普朗克 ⇒ 形式 UV 不完备，非经验相关' % mp.nstr(rel_landau, 6))

# ────────────────────────────────────────────────────────────────
# §4 前提账本与净前提下降门（跨册合账）
# ────────────────────────────────────────────────────────────────
print('\n§4 前提账本与净前提下降门')

s = r130['summary']
n_posted, n_assumed = s['n_posted'], s['n_assumed']
n_derived, n_open = s['n_derived'], s['n_open']
n_total = s['n_total_premises']
non_derived = n_posted + n_assumed + n_open
closure = mpf(n_derived) / n_total
computations['premise_ledger'] = {
    'posted': n_posted, 'assumed': n_assumed, 'derived': n_derived, 'open': n_open,
    'total': n_total, 'non_derived': non_derived,
    'closure_this': float(closure), 'closure_r130': s['closure_all']}
add('P1', '前提账本（r130）',
    'POSTED %d + ASSUMED %d + DERIVED %d + OPEN %d = %d' % (n_posted, n_assumed, n_derived, n_open, n_total),
    'INFO')
add('P2', '未导出前提（= 缺口）', '%d' % non_derived, 'INFO',
    'closure = %d/%d = %s' % (n_derived, n_total, mp.nstr(closure, 6)))

m133 = r133['meta']
d135 = r135['door_accounting']
d138 = r138['door_accounting']
e135, a135 = d135['e'], d135['a']
dgauge = int(d138['gauge_group']['delta'])      # ② 规范群
dmu2 = int(d138['mu2_sign']['delta'])           # ③ μ² 符号
computations['gate'] = {
    'r133_net_premise_delta': m133['net_premise_delta'],
    'r133_structural_unpatchable': m133['structural_unpatchable'],
    'r133_net_decrease_satisfied': m133['net_decrease_satisfied'],
    'r135_e': e135, 'r135_a': a135, 'r135_delta': d135['delta'],
    'r135_door_passes': d135['door_passes'], 'r135_circular_suspect': d135['circular_suspect'],
    'r138_gauge_delta': dgauge, 'r138_mu2_delta': dmu2,
    'r138_registered_combined': d138.get('combined_best_delta_with_r135'),
    'need_e_for_closure': non_derived, 'need_a': 0}

add('G1', '局部修补净前提变化（r133，19 次修补）', '+%d' % m133['net_premise_delta'], 'FAIL',
    '四型穷尽（%s）且 structural_unpatchable=%s' %
    (m133['type_counts'], m133['structural_unpatchable']))
add('G2', '新原理路线：无质量自旋-2（r135）', 'e=%d a=%d Δ=%+d' % (e135, a135, d135['delta']),
    'BOUNDARY', 'door_passes=%s 但 circular_suspect=%s ⇒ 净下降存疑，不计为过门' %
    (d135['door_passes'], d135['circular_suspect']))
add('G3', '硬核两块（r138：②规范群 / ③μ²）',
    '②Δ=%+d ③Δ=%+d' % (dgauge, dmu2),
    'FAIL', '②仅被约束不被导出（U(1)_Y 还有跨普朗克 Landau 极点）；③由 (m_H, v) 读出且两条逃逸被排除')

# 口径 A（本册）：把两块硬核「若去攻则必付的代价」一并计入
best_delta = d135['delta'] + dgauge + dmu2
# 口径 B（r138 登记）：只计 r135，未计硬核代价
registered_delta = int(d138.get('combined_best_delta_with_r135', 0))
computations['gate']['best_case_total_delta_口径A'] = best_delta
computations['gate']['best_case_total_delta_口径B_r138登记'] = registered_delta
add('G4', '全库最好合计 Δ（口径 A：r135 + 两块硬核）', '%+d' % best_delta, 'FAIL',
    '过门需 Δ < 0 且 e = %d、a = 0 才封口；口径 A 实测 %+d ⇒ 未通过' % (non_derived, best_delta))
add('G4b', '口径 B（r138 登记：只计 r135）', '%+d' % registered_delta, 'BOUNDARY',
    '两口径差 %+d 来自「是否把硬核代价计入」；本册两口径并列登记，不代选' %
    (best_delta - registered_delta))
add('G5', '封口所需（e, a）', 'e=%d, a=0' % non_derived, 'FAIL',
    '实际最好 e=%d（且循环存疑）、a=%d' % (e135, a135))

# ────────────────────────────────────────────────────────────────
# §5 守卫
# ────────────────────────────────────────────────────────────────
print('\n§5 守卫')
guard('VG1', mpf(ctrl_pass) == ctrl_total,
      '控制组通过率必须为 1（否则七条判据无判别力，全套判定作废）；实测 %g/%g' % (ctrl_pass, ctrl_total))
guard('VG2', target_pass == 1 and target_total == 7,
      '目标侧完成度必须机读复现为 1/7；实测 %d/%d' % (target_pass, target_total))
guard('VG3', non_derived == 37 and abs(float(closure) - s['closure_all']) < 1e-9,
      '未导出前提数必须为 37 且 closure 与 r130 一致；实测 %d / %s' % (non_derived, mp.nstr(closure, 8)))
guard('VG4', m133['net_premise_delta'] == 11 and m133['structural_unpatchable'] is True
      and m133['net_decrease_satisfied'] is False,
      'r133 必须仍为 net +11、结构不可修补、净下降未满足')
guard('VG5', best_delta >= 0 and registered_delta == -1,
      '口径 A 合计 Δ 必须 ≥ 0（门确实未通过）且口径 B 复现 r138 登记的 −1；实测 A=%+d、B=%+d'
      % (best_delta, registered_delta))
guard('VG6', d135['circular_suspect'] is True and d135['door_passes'] is True,
      'r135 必须同时记录 door_passes=True 与 circular_suspect=True（不得只报好消息）')
guard('VG7', rel_aG < tol_aG,
      'α_G(M_GUT) 独立复算与 r119 相对残差 < %s（按 r119 存储精度定）；实测 %s'
      % (mp.nstr(tol_aG, 3), mp.nstr(rel_aG, 6)))
guard('VG8', d_dex < mpf('1e-3'),
      '引力间隙 dex 独立复算与 r119 差 < 1e-3；实测 %s' % mp.nstr(d_dex, 6))
guard('VG9', d_sig < mpf('1e-2'),
      'α_s σ 独立复算与 r119 差 < 1e-2；实测 %s' % mp.nstr(d_sig, 6))
guard('VG10', dev_dr > 0 and dev_dr < mpf('2e-2'),
      '电弱树图自洽解与实测之差必须落在辐射修正量级（0 < 偏差 < 2%%）；实测 %s' % mp.nstr(dev_dr, 6))
guard('VG11', agg.get('FAIL', 0) >= agg.get('PASS', 0) and agg.get('FAIL', 0) > 0,
      '全攻坚线负结论条目数必须 ≥ 正结论条目数且非空（FAIL %d vs PASS %d）' %
      (agg.get('FAIL', 0), agg.get('PASS', 0)))
guard('VG12', n_line >= 40,
      '本轮攻坚线（r98+）判定册必须 ≥ 40 份；实测 %d' % n_line)
guard('VG13', 0 <= guards_passed <= guards_total and guards_total > 0,
      '守卫聚合必须是合法分数（0 ≤ passed ≤ total，total > 0）；实测 %d/%d' %
      (guards_passed, guards_total))
if shortfall:
    add('X1', '守卫未满分册（登记为遗留，非本册可修）',
        '%d 册：%s' % (len(shortfall), ', '.join('r%d(%s)' % (s['r'], s['guards']) for s in shortfall[:12])),
        'INFO', '本册只登记不代修：这些册的自报守卫未满分，属上游产物，需各册自行复核')

n_guard_pass = sum(1 for g in guards if g['passed'])
print('  守卫 %d/%d' % (n_guard_pass, len(guards)))
for g in guards:
    print('   %-5s %s %s' % (g['id'], 'PASS' if g['passed'] else 'FAIL', g['desc'][:90]))

# ────────────────────────────────────────────────────────────────
# §6 终局裁定
# ────────────────────────────────────────────────────────────────
print('\n§6 终局裁定')
FINAL = 'UFT-NOT-ACHIEVED'
conclusion = (
    '统一场论【未实现】：七条机读必要条件完成度 %d/%d = %s；'
    '控制组（电弱）%g/%g = 1 ⇒ 判据确有判别力。'
    '前提账本未导出 %d 条、closure=%s；净前提下降门最好合计 Δ=%+d（需 e=%d、a=0 才封口）⇒ 未通过。'
    '局部修补结构不可修补（r133，19 次修补净 +11）；唯一新原理候选（r135 无质量自旋-2）'
    '净下降 −1 但循环存疑；两块硬核（r138：②规范群、③μ²）Δ≥0。'
    '故本库当前不存在可宣称「已实现」的统一场论。'
    % (target_pass, target_total, mp.nstr(mpf(target_pass) / target_total, 6),
       ctrl_pass, ctrl_total, non_derived, mp.nstr(closure, 6), best_delta, non_derived))
add('F1', '终局裁定', FINAL, FINAL, conclusion)

payload = {
    'doc': 'TUFT-r139 攻坚线全维总总结与统一场论终局裁定',
    'generated_at': NOW,
    'scope_note': '总总结卷：不新开战线；条目与 r136/r138 及各源卷不可相加（non-additivity freeze）',
    'module': os.path.abspath(__file__),
    'final_verdict': FINAL,
    'conclusion': conclusion,
    'completion': {'target_pass': target_pass, 'target_total': target_total,
                   'target_ratio': float(mpf(target_pass) / target_total),
                   'control_pass': ctrl_pass, 'control_total': ctrl_total,
                   'control_ratio': float(mpf(ctrl_pass) / ctrl_total),
                   'criteria': criteria},
    'computations': computations,
    'items': items,
    'guards': {'passed': n_guard_pass, 'total': len(guards), 'items': guards},
    'non_additivity_freeze': True,
    'new_physics_claim': 0,
}

os.makedirs(DIR_DATA, exist_ok=True)
with io.open(os.path.join(DIR_DATA, STEM + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = []
lines.append('# TUFT-r139 · 攻坚线全维总总结 与 统一场论终局裁定')
lines.append('')
lines.append('> 生成时间 %s ｜ mpmath %d 位 ｜ 守卫 %d/%d' % (NOW, mp.dps, n_guard_pass, len(guards)))
lines.append('')
lines.append('## 终局裁定')
lines.append('')
lines.append('**%s**' % FINAL)
lines.append('')
lines.append(conclusion)
lines.append('')
lines.append('## 一 攻坚线清点（r%d–r%d，%d 册）' % (LEDGER[0]['r'], LEDGER[-1]['r'], len(LEDGER)))
lines.append('')
lines.append('| 册 | 条目聚合 | 守卫 |')
lines.append('|---|---|---|')
for rec in LEDGER:
    cs = ' '.join('%s %d' % (k, v) for k, v in sorted(rec['counts'].items())) or '—'
    lines.append('| r%d | %s | %s |' % (rec['r'], cs,
                                        '%d/%d' % rec['guards'] if rec['guards'] else '—'))
lines.append('')
lines.append('**聚合**：%s ｜ 守卫 %d/%d' % (
    ' ｜ '.join('%s=%d' % (k, v) for k, v in sorted(agg.items())), guards_passed, guards_total))
lines.append('')
lines.append('## 二 七条判据')
lines.append('')
lines.append('| 条件 | 名称 | 判定 |')
lines.append('|---|---|---|')
for c, raw in zip(criteria, r119['criteria_target']):
    lines.append('| %s | %s | **%s** |' % (c['id'], c['name'], c['verdict']))
lines.append('')
lines.append('- 目标侧：**%d/%d = %s**' % (target_pass, target_total,
                                          mp.nstr(mpf(target_pass) / target_total, 6)))
lines.append('- 控制组（电弱统一）：**%g/%g = 1** ⇒ 判据有判别力' % (ctrl_pass, ctrl_total))
lines.append('')
lines.append('## 三 独立 250 位复算')
lines.append('')
lines.append('| 项 | 本册 | 上游 | 残差 |')
lines.append('|---|---|---|---|')
lines.append('| α_G(M_GUT)=(M_GUT/E_Pl)² | %s | %s | %s |'
             % (mp.nstr(alpha_G_at_MGUT, 12), u3['alpha_G_at_MGUT'], mp.nstr(rel_aG, 6)))
lines.append('| 引力间隙 dex | %s | %s | %s |'
             % (mp.nstr(dex_gap, 10), u3['dex_gap'], mp.nstr(d_dex, 6)))
lines.append('| α_s 偏离 σ | %s | %s | %s |'
             % (mp.nstr(sigma, 8), sm['sigma'], mp.nstr(d_sig, 6)))
lines.append('| M_W 树图自洽解 vs 实测 | %s | %s | %s（=Δr 量级）|'
             % (mp.nstr(M_W_tree, 10), mp.nstr(M_W_obs, 10), mp.nstr(dev_dr, 6)))
lines.append('| U(1)_Y Landau 极点 GeV | %s | %.6g | %s |'
             % (mp.nstr(Lambda_U1, 10), g2['u1_landau_gev'], mp.nstr(rel_landau, 6)))
lines.append('')
lines.append('## 四 前提账本与净前提下降门')
lines.append('')
lines.append('| 类 | 计数 |')
lines.append('|---|---|')
for k, val in (('POSTED', n_posted), ('ASSUMED', n_assumed),
               ('DERIVED', n_derived), ('OPEN', n_open)):
    lines.append('| %s | %d |' % (k, val))
lines.append('| **未导出合计（缺口）** | **%d** |' % non_derived)
lines.append('| closure | %s |' % mp.nstr(closure, 6))
lines.append('')
lines.append('| 门项 | 值 | 判定 |')
lines.append('|---|---|---|')
lines.append('| r133 局部修补净变化 | +%d | FAIL |' % m133['net_premise_delta'])
lines.append('| r135 无质量自旋-2（e/a/Δ） | %d/%d/%+d | BOUNDARY（循环存疑） |'
             % (e135, a135, d135['delta']))
lines.append('| r138 硬核 ②规范群 | Δ=%+d | FAIL |' % dgauge)
lines.append('| r138 硬核 ③μ² | Δ=%+d | FAIL |' % dmu2)
lines.append('| **全库最好合计（口径 A：含硬核代价）** | **%+d** | **FAIL（需 e=%d、a=0）** |'
             % (best_delta, non_derived))
lines.append('| 口径 B（r138 登记，只计 r135） | %+d | BOUNDARY（两口径并列登记） |' % registered_delta)
lines.append('')
lines.append('## 五 守卫')
lines.append('')
lines.append('| 守卫 | 判定 | 说明 |')
lines.append('|---|---|---|')
for g in guards:
    lines.append('| %s | %s | %s |' % (g['id'], 'PASS' if g['passed'] else 'FAIL', g['desc']))
lines.append('')
lines.append('## 六 条目明细')
lines.append('')
lines.append('| 条目 | 名称 | 值 | 判定 |')
lines.append('|---|---|---|---|')
for it in items:
    lines.append('| %s | %s | %s | %s |' % (it['id'], it['name'], it['value'], it['verdict']))
lines.append('')
lines.append('---')
lines.append('')
lines.append('**红线**：本册是总总结卷，不产出新物理。数学自洽 ≠ 实验证实。')

with io.open(os.path.join(DIR_DATA, STEM + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

rep = []
rep.append('TUFT-r139 攻坚线全维总总结与统一场论终局裁定')
rep.append('生成时间 = %s' % NOW)
rep.append('模块路径 = %s' % os.path.abspath(__file__))
rep.append('判定册 = %d（r%d–r%d）' % (len(LEDGER), LEDGER[0]['r'], LEDGER[-1]['r']))
rep.append('条目聚合 = %s' % agg)
rep.append('守卫聚合 = %d/%d' % (guards_passed, guards_total))
rep.append('完成度 = %d/%d' % (target_pass, target_total))
rep.append('控制组 = %d/%d' % (ctrl_pass, ctrl_total))
rep.append('未导出前提 = %d / %d（closure = %s）' % (non_derived, n_total, mp.nstr(closure, 8)))
rep.append('全库最好合计 Δ = %+d（需 e=%d、a=0）' % (best_delta, non_derived))
rep.append('本册守卫 = %d/%d' % (n_guard_pass, len(guards)))
rep.append('终局裁定 = %s' % FINAL)
rep.append('结论 = %s' % conclusion)
with io.open(os.path.join(DIR_DATA, STEM + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep) + '\n')

print('\n' + '=' * 78)
print('终局裁定 = %s' % FINAL)
print('守卫 %d/%d ｜ 退出码 %d' % (n_guard_pass, len(guards), 0 if n_guard_pass == len(guards) else 1))
print('=' * 78)

sys.exit(0 if n_guard_pass == len(guards) else 1)
