# -*- coding: utf-8 -*-
"""UFE-1 耦合统一探针（一环双阈，零第三方依赖）。

背景：`verify_core.py` 的 R1 判定 SM 单圈三耦合**不统一**（α⁻¹ 最小散布 3.66），
MSSM 对照 0.049。本探针回答一个更进攻性的问题（L10）：

    给定一份**具体的新物理内容 Δb**，能否让三耦合在 (M_int, M_GUT) 处真正相遇？
    若可以，则给出被**预言的统一标度 M_GUT 与 α_GUT⁻¹**（可检验数字）。

约定（与 verify_core.py 一致）：1/α_i(μ) = 1/α_i(M_Z) − (b_i/2π)·ln(μ/M_Z)。

求解：设 M_Z → M_int 用 b_low，M_int → M_GUT 用 b_high = b_low + Δb。
两条线性方程（α₁=α₂、α₂=α₃）解出 L=ln(M_int/M_Z)、G=ln(M_GUT/M_int)：

    (a_i − a_j)|_MZ − ((b_low_i−b_low_j)/2π)·L = ((b_high_i−b_high_j)/2π)·G

用法： python -B unification_probe.py
产出： 统一探针报告.md / .json
"""
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent

MZ = 91.1876
ALPHA_MZ = 1.0 / 127.952
SIN2_MS = 0.23121
ALPHAS_MZ = 0.1180
MPL = 1.22e19

# GUT 归一化下的 1/α_i(M_Z)
A_MZ = ((3.0 / 5.0) * (1.0 - SIN2_MS) / ALPHA_MZ, SIN2_MS / ALPHA_MZ, 1.0 / ALPHAS_MZ)
B_SM = (41.0 / 10.0, -19.0 / 6.0, -7.0)


def delta_b_fermion_weyl(d3, T3, d2, T2, Y, n=1):
    """n 个 Weyl 费米子（表示 (d3,d2)_Y）对 (b1,b2,b3) 的贡献。"""
    return ((2.0 / 3.0) * n * (3.0 / 5.0) * Y * Y * d3 * d2,
            (2.0 / 3.0) * n * T2 * d3,
            (2.0 / 3.0) * n * T3 * d2)


def delta_b_scalar(d3, T3, d2, T2, Y, n=1):
    """n 个复标量（表示 (d3,d2)_Y）对 (b1,b2,b3) 的贡献。"""
    return ((1.0 / 3.0) * n * (3.0 / 5.0) * Y * Y * d3 * d2,
            (1.0 / 3.0) * n * T2 * d3,
            (1.0 / 3.0) * n * T3 * d2)


def add(*ds):
    out = [0.0, 0.0, 0.0]
    for d in ds:
        for i in range(3):
            out[i] += d[i]
    return tuple(out)


def solve_thresholds(a, b_low, b_high):
    """解 (L=ln(M_int/MZ), G=ln(M_GUT/Mint))；无解返回 None。"""
    d12 = a[0] - a[1]
    d23 = a[1] - a[2]
    s12 = (b_low[0] - b_low[1]) / (2.0 * math.pi)
    s23 = (b_low[1] - b_low[2]) / (2.0 * math.pi)
    h12 = (b_high[0] - b_high[1]) / (2.0 * math.pi)
    h23 = (b_high[1] - b_high[2]) / (2.0 * math.pi)
    det = s12 * h23 - h12 * s23
    if abs(det) < 1e-30:
        return None
    L = (d12 * h23 - h12 * d23) / det
    G = (s12 * d23 - d12 * s23) / det
    return L, G


def required_db(M_int, M_GUT):
    """给定 (M_int, M_GUT)，解出使三线**精确**相交所需的 Δb（取 Δb2=0 归一）。

    h_ij = (Δb_i−Δb_j)/2π；(a_i=a_j) 给 (d_ij − s_ij·L) = h_ij·G。
    """
    L = math.log(M_int / MZ)
    G = math.log(M_GUT / M_int)
    d12 = A_MZ[0] - A_MZ[1]
    d23 = A_MZ[1] - A_MZ[2]
    s12 = (B_SM[0] - B_SM[1]) / (2.0 * math.pi)
    s23 = (B_SM[1] - B_SM[2]) / (2.0 * math.pi)
    db1 = 2.0 * math.pi * (d12 - s12 * L) / G          # = Δb1（Δb2=0）
    db3 = -2.0 * math.pi * (d23 - s23 * L) / G         # = Δb3（Δb2=0）
    b1_high = B_SM[0] + db1
    a_gut = A_MZ[0] - B_SM[0] / (2.0 * math.pi) * L - b1_high / (2.0 * math.pi) * G
    return (db1, 0.0, db3), a_gut, M_int, M_GUT


def min_spread(b, a=None, lo=1e3, hi=1e19, n=6000):
    """单一 b 从 M_Z 起跑时 α⁻¹ 三曲线的最小散布。"""
    a = a or A_MZ
    best, best_mu = None, None
    for k in range(n + 1):
        lnmu = math.log(lo) + k * (math.log(hi) - math.log(lo)) / n
        vals = [a[i] - b[i] / (2.0 * math.pi) * lnmu for i in range(3)]
        s = max(vals) - min(vals)
        if best is None or s < best:
            best, best_mu = s, math.exp(lnmu)
    return best, best_mu


# ---- 新物理内容候选（Δb 的计算全部来自表示论，可复核）----------------------
def cand_sm():
    return 'SM（基准，无新物理）', (0.0, 0.0, 0.0), '无'


def cand_mssm():
    # 与 verify_core.py R1 的 MSSM 对照同源：b_MSSM=(33/5,1,-3)
    return 'MSSM（超对称，对照）', (33.0 / 5.0 - 41.0 / 10.0, 1.0 + 19.0 / 6.0, -3.0 + 7.0), '超伴子'

def cand_vl_4th():
    # 一组“矢量型第四代”Dirac 费米子（10 个 Dirac = 20 Weyl），逐项求和
    d = (0.0, 0.0, 0.0)
    # Q(3,2,1/6) + Qbar(3bar,2,-1/6)
    d = add(d, delta_b_fermion_weyl(3, 0.5, 2, 0.5, 1 / 6, 2), delta_b_fermion_weyl(3, 0.5, 2, 0.5, -1 / 6, 2))
    # u(3,1,2/3)+ubar, d(3,1,-1/3)+dbar
    d = add(d, delta_b_fermion_weyl(3, 0.5, 1, 0.0, 2 / 3, 2), delta_b_fermion_weyl(3, 0.5, 1, 0.0, -2 / 3, 2))
    d = add(d, delta_b_fermion_weyl(3, 0.5, 1, 0.0, -1 / 3, 2), delta_b_fermion_weyl(3, 0.5, 1, 0.0, 1 / 3, 2))
    # L(1,2,-1/2)+Lbar
    d = add(d, delta_b_fermion_weyl(1, 0.0, 2, 0.5, -1 / 2, 2), delta_b_fermion_weyl(1, 0.0, 2, 0.5, 1 / 2, 2))
    # e(1,1,1)+ebar
    d = add(d, delta_b_fermion_weyl(1, 0.0, 1, 0.0, 1.0, 2), delta_b_fermion_weyl(1, 0.0, 1, 0.0, -1.0, 2))
    return '矢量型第四代（10 Dirac/代，Dirac 质量）', d, '10 个 Dirac 费米子 @ M_int'


def cand_ots():
    # (8,1,0) + (1,3,0) + (1,1,0) 的 Dirac 费米子（“八重态-三重态-单态”暗物质统一候选）
    d = (0.0, 0.0, 0.0)
    d = add(d, delta_b_fermion_weyl(8, 3.0, 1, 0.0, 0.0, 2))   # SU(3) 伴随 T=3
    d = add(d, delta_b_fermion_weyl(1, 0.0, 3, 2.0, 0.0, 2))   # SU(2) 伴随 T=2
    d = add(d, delta_b_fermion_weyl(1, 0.0, 1, 0.0, 0.0, 2))
    return '(8,1,0)+(1,3,0)+(1,1,0) Dirac 费米子（OTS 暗物质统一候选）', d, '3 个 Dirac 费米子 @ M_int'


CANDS = [cand_sm, cand_mssm, cand_vl_4th, cand_ots]


def analyse(name, db, note):
    b_high = tuple(B_SM[i] + db[i] for i in range(3))
    row = {'name': name, 'delta_b': [round(x, 5) for x in db], 'note': note}
    spread, at = min_spread(b_high)
    row['min_spread_single_threshold'] = spread
    row['min_spread_at_GeV'] = at
    sol = solve_thresholds(A_MZ, B_SM, b_high)
    if sol is None:
        row['threshold_solution'] = None
        row['verdict'] = '无二阈解（Δb 方向无法使三线相交）'
        return row
    L, G = sol
    if (not (-50.0 < L < 50.0)) or (not (-50.0 < G < 50.0)):
        row['threshold_solution'] = [L, G]
        row['verdict'] = '二阈解越界（L=%.1f, G=%.1f）⇒ 该内容无法在物理区间统一' % (L, G)
        return row
    M_int = MZ * math.exp(L)
    M_GUT = M_int * math.exp(G)
    a_gut = A_MZ[0] - B_SM[0] / (2 * math.pi) * L - b_high[0] / (2 * math.pi) * G
    row['M_int_GeV'] = M_int
    row['M_GUT_GeV'] = M_GUT
    row['alpha_GUT_inv'] = a_gut
    ok = (M_int > MZ) and (M_GUT > M_int) and (M_GUT < MPL)
    row['physical'] = ok
    row['verdict'] = ('可统一：M_int=%.3e GeV, M_GUT=%.3e GeV, α_GUT⁻¹=%.2f' % (M_int, M_GUT, a_gut)
                      if ok else '二阈解非物理（M_int 或 M_GUT 越界）')
    return row


def main():
    rows = [analyse(*f()) for f in CANDS]

    lines = ['# UFE-1 耦合统一探针报告', '',
             '由 [unification_probe.py](unification_probe.py) 自动生成，**零第三方依赖**。',
             '一环两条线性方程解 (M_int, M_GUT)；Δb 由表示论逐项计算。', '',
             '## 基准与结论', '',
             '| 内容 | Δb=(b1,b2,b3) | 二阈解 | M_int (GeV) | M_GUT (GeV) | α_GUT⁻¹ | 判定 |',
             '|---|---|---|---|---|---|---|']
    for r in rows:
        if 'M_int_GeV' not in r:
            lines.append('| %s | %s | — | — | — | — | %s |' %
                         (r['name'], r['delta_b'], r['verdict']))
        else:
            lines.append('| %s | %s | 是 | %.3e | %.3e | %.2f | %s |' %
                         (r['name'], r['delta_b'], r['M_int_GeV'], r['M_GUT_GeV'],
                          r['alpha_GUT_inv'], r['verdict']))
    lines += ['',
              '## 单阈最小散布（与 R1 同口径）', '',
              '| 内容 | α⁻¹ 最小散布 | 出现标度 (GeV) |', '|---|---|---|']
    for r in rows:
        lines.append('| %s | %.4f | %.3e |' %
                     (r['name'], r['min_spread_single_threshold'], r['min_spread_at_GeV']))
    lines += ['',
              '## 目标标度 → 所需 Δb（统一规格）', '',
              '固定 (M_int, M_GUT)，解出让三线**精确**相交所需的 Δb（取 Δb2=0 归一）。'
              '任何非 SUSY 统一方案，其 Δb 必须命中下表对应行。', '',
              '| M_int (GeV) | M_GUT (GeV) | 所需 Δb=(Δb1, Δb2, Δb3) | α_GUT⁻¹ |',
              '|---|---|---|---|']
    targets = [(1e3, 2e16), (1e4, 2e16), (1e5, 2e16), (1e10, 2e16), (1e16, 1e19)]
    trows = []
    for mi, mg in targets:
        db, ag, _, _ = required_db(mi, mg)
        trows.append((mi, mg, db, ag))
        lines.append('| %.0e | %.0e | (%.3f, 0, %.3f) | %.2f |' % (mi, mg, db[0], db[2], ag))
    lines += ['',
              '## 结构结论', '',
              '1. **SM 无二阈解**（det=0）：三条线在单环下永不相交 ⇒ 强化 R1.1/R1.2。',
              '2. **整代矢量费米子对统一"盲"**：其 Δb ∝ (1,1,1)（见候选表），只平移三线、不改两两之差',
              '   ⇒ h12=h23=0 ⇒ 无论加几代都不统一。这是**表示论层面的 no-go**。',
              '3. **MSSM（超对称）** 单阈散布 0.049 ⇒ 唯一"自然阈值（~TeV）"下的统一解。',
              '4. **非 SUSY 统一** 需 Δb 命中上表，且 (M_int, M_GUT) 被"钉死"——代价是引入具体新态并预言其标度。',
              '',
              '## 红线', '',
              '*以上为新物理**可行性**规格，不宣称任何新态真实存在；"能统一"不等于"自然界选它"。*',
              '',
              '- 本探针只做**一环 RGE 可行性**判定，不宣称这些新物理真实存在。',
              '- 若某内容"可统一"，其 M_int/M_GUT 是**该内容下的预言标度**（可被对撞机/质子衰变检验），',
              '  但"能统一"本身不等于"自然界选它"。',
              '',
              '[返回理论核心](../README.md) · [预言与判据](../08_预言与判据.md)']
    (ROOT / '统一探针报告.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (ROOT / '统一探针报告.json').write_text(
        json.dumps({'theory': 'UFE-1', 'check': 'unification_probe', 'rows': rows},
                   ensure_ascii=False, indent=2), encoding='utf-8')

    print('UFE-1 耦合统一探针（一环）')
    for r in rows:
        print('  %-46s Δb=%s' % (r['name'][:46], r['delta_b']))
        print('      单阈最小散布=%.4f @ %.2e GeV ; %s'
              % (r['min_spread_single_threshold'], r['min_spread_at_GeV'], r['verdict']))
    print('产出：统一探针报告.md / .json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
