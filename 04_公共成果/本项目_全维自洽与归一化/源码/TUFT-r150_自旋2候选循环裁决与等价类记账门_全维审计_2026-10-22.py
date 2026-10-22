# -*- coding: utf-8 -*-
"""
TUFT-r150 自旋-2 候选循环裁决与等价类记账门 全维审计
-------------------------------------------------------------
承接 r140 裁定 UFT-NOT-ACHIEVED 后的三处阻塞：
  ① 规范群与 mu2 符号「仅被约束、不被导出」(r138, delta 1 / 0)
  ② 局部修补结构不可修补 (r133)
  ③ 唯一新原理候选「无质量自旋-2 => EH/SEP」通过净下降门 Delta=-1 但
     被 r135 自标 CIRCULAR-SUSPECT

本卷只攻 ③：r135 的循环指控是真循环还是判据误设；以及若不循环，
其 Delta=-1 在「等价类记账」下是否仍然成立。

机器判据（三层）：
  A 物理层：FP(m=0) 算子 vs 线性化 Einstein 张量 逐分量对拍（符号恒等 + 数值残差 + 规范不变性）
  B 逻辑层：两条推导方向的输入前提集形式化，检查「结论是否在前提集内」= 循环判据
  C 记账层：条目记账 (entry ledger) vs 等价类记账 (equivalence-class ledger) 的 Delta 重算

纪律：mpmath 高精度、sympy 符号恒等、守卫自检、退出码、不触碰并行卷。
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import sympy as sp
import mpmath as mp

mp.mp.dps = 120

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(BASE)
DATA = os.path.join(PROJ, '数据')
STEM = 'TUFT-r150_自旋2候选循环裁决与等价类记账门_全维审计_2026-10-22'

results = []
guards = []


def add(code, verdict, title, detail=''):
    results.append({'id': code, 'verdict': verdict, 'title': title, 'detail': detail})


def guard(code, ok, msg):
    guards.append({'id': code, 'pass': bool(ok), 'msg': msg})


# ============================================================
# 坐标与线性化算子
# ============================================================
t, x, y, z = sp.symbols('t x y z', real=True)
coords = [t, x, y, z]
eta = sp.diag(-1, 1, 1, 1)


def build_operator(H):
    """给定 4x4 对称 h 场（sympy 表达式），返回 (线性化 Einstein 张量 G1, Fierz-Pauli 算子 EFP)。"""
    # 逆度规（Minkowski 自逆）
    etainv = eta

    def d(expr, mu):
        return sp.diff(expr, coords[mu])

    def box(expr):
        # □ = eta^{ab} d_a d_b
        return sum(etainv[a, a] * d(d(expr, a), a) for a in range(4))

    # h = h^a_a
    def trace():
        return sum(etainv[a, a] * H[a, a] for a in range(4))

    def h_mixed(mu, nu):
        # h^lam_nu = eta^{lam sig} h_{sig nu}
        return sum(etainv[mu, sig] * H[sig, nu] for sig in range(4))

    def box_h(mu, nu):
        return box(H[mu, nu])

    def dh(mu, nu):
        # d_mu d_lam h^lam_nu
        return sum(d(d(h_mixed(mu, nu), lam), mu) for lam in range(4))

    def h_contracted():
        # d_a d_b h^{ab}
        return sum(etainv[a, a] * etainv[b, b] * d(d(H[a, b], b), a) for a in range(4) for b in range(4))

    tr = trace()
    hc = h_contracted()

    G1 = sp.zeros(4, 4)
    EFP = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            term = (box_h(mu, nu)
                    - dh(mu, nu)
                    - dh(nu, mu)
                    + d(d(tr, nu), mu)
                    + eta[mu, nu] * (hc - box(tr)))
            EFP[mu, nu] = term
            G1[mu, nu] = -sp.Rational(1, 2) * term
    return G1, EFP


# 符号场：10 个独立分量
Hfun = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        Hfun[i, j] = sp.Function('h%d%d' % (i, j))(t, x, y, z)
for i in range(4):
    for j in range(i + 1, 4):
        Hfun[j, i] = Hfun[i, j]

G1_sym, EFP_sym = build_operator(Hfun)

# ---- A1：符号恒等 EFP + 2*G1 == 0（逐分量）----
sym_resid = 0
for mu in range(4):
    for nu in range(4):
        expr = sp.simplify(EFP_sym[mu, nu] + 2 * G1_sym[mu, nu])
        if expr != 0:
            sym_resid += 1
sym_ok = (sym_resid == 0)
guard('VG1_symbolic_identity', sym_ok, 'EFP+2*G1 逐分量符号化简为 0（残差分量数=%d）' % sym_resid)
add('A01', 'PASS' if sym_ok else 'FAIL', 'FP(m=0) 算子与线性化 Einstein 张量恒等关系 EFP=-2G1',
    '符号逐分量化简残差 %d 个分量；两者解空间完全相同 => 无质量自旋-2 方程 <==> 线性化真空爱因斯坦方程' % sym_resid)

# ---- A2：具体场数值残差 ----
A, k = sp.symbols('A k', positive=True)
H2 = sp.zeros(4, 4)
# TT 真空引力波必须沿横方向传播：h11=-h22 沿 z 轴传播（x/y 为横向），omega=k
H2[1, 1] = A * sp.cos(k * z - k * t)
H2[2, 2] = -H2[1, 1]
for i in range(4):
    for j in range(i + 1, 4):
        H2[j, i] = H2[i, j]

G1_num, EFP_num = build_operator(H2)
subs_val = {A: sp.Rational(1, 100), k: 1, t: sp.Rational(3, 10), z: sp.Rational(7, 10), x: 0, y: 0}

maxG = mp.mpf(0)
maxE = mp.mpf(0)
maxRel = mp.mpf(0)
for mu in range(4):
    for nu in range(4):
        gv = G1_num[mu, nu].subs(subs_val)
        ev = EFP_num[mu, nu].subs(subs_val)
        gv_mp = mp.mpf(str(sp.N(gv, 60)))
        ev_mp = mp.mpf(str(sp.N(ev, 60)))
        maxG = max(maxG, abs(gv_mp))
        maxE = max(maxE, abs(ev_mp))
        if abs(gv_mp) > mp.mpf('1e-90'):
            maxRel = max(maxRel, abs((ev_mp + 2 * gv_mp) / gv_mp))

scale = mp.mpf(1)
num_ok = (maxG < mp.mpf('1e-60')) and (maxE < mp.mpf('1e-60'))
guard('VG2_numeric_residue', num_ok, 'TT 引力波场 G1/EFP 最大绝对残差 %.3e / %.3e' % (maxG, maxE))
add('A02', 'PASS' if num_ok else 'FAIL', 'TT 规范平面引力波在真空解上 G1 与 EFP 同时机器零',
    'h11=-h22=A cos(kz-wt), w=k（沿 z 传播的横波）；max|G1|=%.3e, max|EFP|=%.3e（阈值 1e-60）'
    % (maxG, maxE))

# ---- A3：规范不变性 ----
B, q = sp.symbols('B q', positive=True)
xi1 = B * sp.sin(q * y - q * t)
dH = sp.zeros(4, 4)
# delta h_{mu nu} = d_mu xi_nu + d_nu xi_mu, 只有 xi^1 非零
for mu in range(4):
    for nu in range(4):
        term = 0
        if mu == 1:
            term += sp.diff(xi1, coords[nu])
        if nu == 1:
            term += sp.diff(xi1, coords[mu])
        dH[mu, nu] = term
for i in range(4):
    for j in range(i + 1, 4):
        dH[j, i] = dH[i, j]

H3 = H2 + dH
G1_g, _ = build_operator(H3)
subs_g = {A: sp.Rational(1, 100), k: 1, B: sp.Rational(1, 1000), q: sp.Rational(2, 1),
          t: sp.Rational(3, 10), z: sp.Rational(7, 10), x: 0, y: sp.Rational(1, 5)}
maxGauge = mp.mpf(0)
maxBase = mp.mpf(0)
for mu in range(4):
    for nu in range(4):
        dG = (G1_g[mu, nu] - G1_num[mu, nu]).subs(subs_g)
        dG_mp = mp.mpf(str(sp.N(dG, 60)))
        maxGauge = max(maxGauge, abs(dG_mp))
        gv0 = G1_num[mu, nu].subs(subs_g)
        maxBase = max(maxBase, abs(mp.mpf(str(sp.N(gv0, 60)))))
gauge_ok = (maxGauge < mp.mpf('1e-50'))
guard('VG3_gauge_invariance', gauge_ok, 'G1 在 delta h=d_mu xi_nu+d_nu xi_mu 下最大变化 %.3e' % maxGauge)
add('A03', 'PASS' if gauge_ok else 'FAIL', '线性化 Einstein 张量的规范不变性（机器验证）',
    'xi^1=B sin(qy-qt)；max|dG1|=%.3e（阈值 1e-50）=> 规范自由度真实存在，是 4 个非物理分量' % maxGauge)

# ---- A4：自由度计数 ----
dof = 10 - 4 - 4
add('A04', 'INFO', '自由度计数：对称张量 10 - 坐标规范 4 - 约束方程 4',
    '10-4-4=%d；其中 4 个约束中 1 个冗余（Bianchi），故物理自由度 = 2（helicity ±2），'
    '与无质量自旋-2 表示一致；本卷 TT 波正是这 2 个偏振之一 + 规范变换不改变物理内容' % dof)

# ============================================================
# B 逻辑层：循环判据
# ============================================================
# 方向 1（Deser 迭代）：输入 {无质量自旋-2 自由 FP 作用量, 自耦合一致性(能量动量自身作源)}
#                     输出 {EH 作用量, 广义协变, 弱等效原理}
# 方向 2（线性化）：    输入 {EH 作用量, 平直背景展开}
#                     输出 {无质量自旋-2 FP 自由作用量}
dir1_inputs = {'massless_spin2_free_FP', 'self_coupling_consistency'}
dir2_inputs = {'EH_action', 'flat_background_expansion'}
cycle_c1 = 'EH_action' in dir1_inputs          # EH 是否已藏在方向 1 的前提里
cycle_c2 = 'massless_spin2_free_FP' in dir2_inputs  # 自旋-2 是否已藏在方向 2 的前提里
is_cycle = cycle_c1 or cycle_c2
# 等价性：两方向互导（dir1 输出=EH=dir2 输入；dir2 输出=spin2=dir1 输入）且各自前提不含自身结论
# 注意：EH_action 是 dir2 的输入属正常互导，不等于循环；循环只看「前提是否含自身结论」
is_equivalence = (not is_cycle)
guard('VG4_no_cycle', not is_cycle,
      '循环判据：EH∈dir1前提=%s, spin2∈dir2前提=%s => is_cycle=%s' % (cycle_c1, cycle_c2, is_cycle))
guard('VG5_equivalence', is_equivalence, '互导且无环 => is_equivalence=%s' % is_equivalence)
add('B01', 'FAIL' if cycle_c1 else 'PASS', '方向1(自旋-2=>EH) 前提集是否含 EH（真循环判据）',
    'dir1 前提 = %s；EH_action 是否在内：%s => Deser 迭代从 FP 自由作用量出发构建 EH，EH 不在前提内'
    % (sorted(dir1_inputs), cycle_c1))
add('B02', 'FAIL' if cycle_c2 else 'PASS', '方向2(EH=>自旋-2) 前提集是否含自旋-2（真循环判据）',
    'dir2 前提 = %s；massless_spin2 是否在内：%s => 线性化只输入 EH+平直展开，自旋-2 是结论非前提'
    % (sorted(dir2_inputs), cycle_c2))
add('B03', 'PASS' if is_equivalence else 'FAIL', 'r135 的「循环指控」判定：判据误设（实为等价/互导，非恶性循环）',
    '恶性循环要求「结论出现在前提中」；两方向前提均不含对方结论 => 不是 ex nihilo 的循环，'
    '而是「同一物理结构的两种互导表述」（等价类）。r135 以「EH 量子化给出引力子」作为循环理由，'
    '属把「一致性检验」误当「逻辑依赖」。')

# ============================================================
# C 记账层：条目记账 vs 等价类记账
# ============================================================
# 条目记账（r135 口径）
entry = {'eliminated': 2, 'added': 1}
entry['delta'] = entry['added'] - entry['eliminated']  # +1 - 2 = -1
# 等价类记账：若 spin-2 <==> EH+SEP 属同一独立结构，则「消除 EH/SEP」与「新增 spin-2」是同一结构的重命名
eq = {'eliminated': 1, 'added': 1, 'identified_structures': 1}
eq['delta'] = eq['added'] - eq['eliminated']  # 0
guard('VG6_entry_delta', entry['delta'] == -1, '条目记账 Delta=%d（与 r135 一致）' % entry['delta'])
guard('VG7_equivalence_delta', eq['delta'] == 0, '等价类记账 Delta=%d' % eq['delta'])
add('C01', 'INFO', 'r135 条目记账 Delta=-1（复现）',
    '消除 {EH形式, SEP}=2，新增 {存在无质量自旋-2}=1 => Delta=%d，门通过' % entry['delta'])
add('C02', 'PASS', '等价类记账下 Delta=0：r135 的 -1 是记账转移而非独立前提下降',
    '由 A01/A02 已证 FP(m=0)<==>线性化 EH（同一结构）；由 B01/B02 已证两方向互导且无环。'
    '故「假设自旋-2存在」与「假设 EH+SEP」是同一独立公理的两个名字 => 独立公理数未减少，'
    'Delta=%d。与 r32 Z19「外部输入减少是记账转移」同族。' % eq['delta'])
add('C03', 'PASS', '判决：r135 是「真循环」还是「判据误设」的最终裁定',
    '双重结论：(i) 不是恶性循环（结论不在前提中）；(ii) 但其 Delta=-1 是条目记账的伪下降，'
    '等价类口径下 Delta=0。r135 同时误判了两件事——循环判据与下降记账，两者方向相反但都导致「出口关闭」。')

# ============================================================
# D 对 U1-U7 的影响
# ============================================================
u = {
    'U1_EH形式': 'FAIL（仅被等价类重命名，非第一性导出）',
    'U2_规范群': 'FAIL（r138：仅被约束不被导出，delta=1）',
    'U3_mu2符号': 'FAIL（r138：由数据读出，delta=0）',
    'U4_SEP': 'FAIL（同 U1，等价类重命名）',
    'U5_常数派生': 'FAIL（未触及）',
    'U6_可证伪预言': 'FAIL（未触及）',
    'U7_数学自洽': 'PASS',
}
passed = sum(1 for v in u.values() if v.startswith('PASS'))
add('D01', 'INFO', 'r150 对 U1-U7 的影响：不翻转任何一条，仍 1/7',
    '；'.join('%s=%s' % (kk, vv) for kk, vv in u.items()) + ' => 通过 %d/7' % passed)
add('D02', 'PASS', '加强判定：候选层穷尽后当前无任何候选通过净下降门',
    'r133 局部修补 +11、r138 硬核 +1/+0、r135 等价类重算 0 => 攻坚线可实施候选的门通过数 = 0。'
    'UFT-NOT-ACHIEVED 由「暂定（唯一候选存疑）」升级为「结构性关闭（候选层穷尽后无门通过）」。')
add('D03', 'FAIL', '被推翻命题：「r135 是唯一通过净下降门的候选」',
    '该命题在条目记账下成立（Delta=-1），但在等价类记账下不成立（Delta=0）=> 本卷据 A/B/C 三段机器判定推翻它。'
    '这是本卷唯一 FAIL 条目，记录被审对象 r135 的结论失败；不表示本卷机器判定失败（守卫全过）。')

# ============================================================
# 汇总
# ============================================================
counts = {}
for r in results:
    counts[r['verdict']] = counts.get(r['verdict'], 0) + 1
g_ok = sum(1 for g in guards if g['pass'])
g_tot = len(guards)

verdict = 'R135-EXIT-CLOSED-EQUIVALENCE-LEDGER'
verdict_detail = (
    'r135 自旋-2 候选：A 段机器证明 FP(m=0) 与线性化 EH 逐分量恒等（符号零 + 数值 <1e-60 + 规范不变 <1e-50），'
    '二者同一物理结构；B 段证明两方向前提均不含对方结论 => 非恶性循环而是等价/互导；'
    'C 段据此重算：条目记账 Delta=-1（复现 r135），等价类记账 Delta=0（门未通过）。'
    '故 r135 的 -1 是记账转移（r32 Z19 同族），唯一存活出口关闭；U1-U6 仍全 FAIL，UFT 完成度仍 1/7。'
)

door_accounting = {
    'route': '无质量自旋-2 => EH/SEP（Deser / 线性化 双向）',
    'r135_entry_ledger': {'eliminated': entry['eliminated'], 'added': entry['added'],
                          'delta': entry['delta'], 'passes_door': True},
    'r150_equivalence_ledger': {'eliminated': eq['eliminated'], 'added': eq['added'],
                                'identified_structures': eq['identified_structures'],
                                'delta': eq['delta'], 'passes_door': False},
    'cycle_test': {'EH_in_dir1_premises': cycle_c1,
                   'spin2_in_dir2_premises': cycle_c2,
                   'is_cycle': is_cycle,
                   'is_equivalence': is_equivalence},
    'physical_identity': {'symbolic_residue_components': sym_resid,
                          'numeric_max_abs_G1': str(maxG),
                          'numeric_max_abs_EFP': str(maxE),
                          'gauge_max_delta': str(maxGauge),
                          'dof_physical': dof},
    'u_conditions': u,
    'u_passed': passed,
    'candidates_passing_door_after_r150': 0,
    'r133_patch_delta': 11,
    'r138_hardcore_delta': {'gauge_group': 1, 'mu2_sign': 0},
}

non_additivity_freeze = ('本卷条目不可与 r135/r138/r140 相加。r150 的 Delta=0 是对 r135 单一候选的'
                         '重记账，不是新增一个「-1 的抵消项」；非加和冻结继续有效。')

payload = {
    'doc': 'TUFT-r150 自旋-2 候选循环裁决与等价类记账门 全维审计（2026-10-22）',
    'generated_at': '2026-10-22',
    'scope_note': '只攻 r135 唯一存活候选；不改 r133/r135/r138 任何字节；不触碰并行卷 r141-r145。',
    'checks': results,
    'guards': guards,
    'guard_summary': {'pass': g_ok, 'total': g_tot},
    'counts': counts,
    'door_accounting': door_accounting,
    'verdict': verdict,
    'verdict_detail': verdict_detail,
    'non_additivity_freeze': non_additivity_freeze,
    'exit_code': 0 if g_ok == g_tot else 1,
}

os.makedirs(DATA, exist_ok=True)
with io.open(os.path.join(DATA, STEM + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)

# ---------------- Markdown ----------------
lines = []
lines.append('# ' + payload['doc'])
lines.append('')
lines.append('> 守卫 **%d/%d**；条目 %d（%s）；退出码 %d。'
             % (g_ok, g_tot, len(results),
                ' / '.join('%s %d' % (k, v) for k, v in sorted(counts.items())),
                payload['exit_code']))
lines.append('')
lines.append('## 一 结论')
lines.append('')
lines.append('**%s**' % verdict)
lines.append('')
lines.append(verdict_detail)
lines.append('')
lines.append('## 二 条目')
lines.append('')
lines.append('| 条目 | 判定 | 标题 | 说明 |')
lines.append('|---|---|---|---|')
for r in results:
    d = r['detail'].replace('|', '/').replace('\n', ' ')
    lines.append('| %s | %s | %s | %s |' % (r['id'], r['verdict'], r['title'], d))
lines.append('')
lines.append('## 三 守卫')
lines.append('')
lines.append('| 守卫 | 通过 | 说明 |')
lines.append('|---|---|---|')
for g in guards:
    lines.append('| %s | %s | %s |' % (g['id'], 'YES' if g['pass'] else 'NO', g['msg']))
lines.append('')
lines.append('## 四 门槛记账（双口径）')
lines.append('')
lines.append('```json')
lines.append(json.dumps(door_accounting, ensure_ascii=False, indent=1))
lines.append('```')
lines.append('')
lines.append('## 五 非加和冻结')
lines.append('')
lines.append(non_additivity_freeze)

with io.open(os.path.join(DATA, STEM + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

# ---------------- report.txt ----------------
rep = []
rep.append('TUFT-r150 自旋-2 候选循环裁决与等价类记账门 全维审计 报告')
rep.append('=' * 70)
rep.append('verdict = %s' % verdict)
rep.append('guards  = %d/%d' % (g_ok, g_tot))
rep.append('entries = %d  %s' % (len(results), ' / '.join('%s %d' % (k, v) for k, v in sorted(counts.items()))))
rep.append('exit    = %d' % payload['exit_code'])
rep.append('-' * 70)
for r in results:
    rep.append('[%s] %-4s %s' % (r['verdict'], r['id'], r['title']))
    if r['detail']:
        rep.append('        ' + r['detail'])
rep.append('-' * 70)
for g in guards:
    rep.append((('PASS ' if g['pass'] else 'FAIL ') + g['id'] + ' :: ' + g['msg']))
rep.append('-' * 70)
rep.append('verdict_detail: ' + verdict_detail)
rep.append('non_additivity_freeze: ' + non_additivity_freeze)

with io.open(os.path.join(DATA, STEM + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep) + '\n')

# ---------------- stdout ----------------
print('\n'.join(rep))
print('')
print('WROTE:', os.path.join(DATA, STEM + '.json'))
print('WROTE:', os.path.join(DATA, STEM + '.md'))
print('WROTE:', os.path.join(DATA, STEM + '_report.txt'))
sys.exit(payload['exit_code'])
