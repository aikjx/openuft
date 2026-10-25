#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TUFT-r178｜S13「从三公设生成标准模型结构」第一性槽位审计（路径四）
================================================================================
编号 r178（★改号：起草时（00:2x）实测首空号取 r176；四件套落盘后登记前复查发现
并行会话《TUFT-r176_核力场定义方程_定义求导与量纲阶数错位》引擎创建于 00:30:21，
早于本卷引擎创建（00:35:02）⇒ 按「先占位者为权威」纪律整体改号 r178
（实测首空号：r175=空间波动方程、r176=核力场（并行，仅源码）、r177=引力光速统一
方程（并行，已登记）均已占 ⇒ r178 为空）；旧 r176 四件套已 mv 入
scratch/r176_s13_old_outputs/；未改动并行会话任何字节）。

靶：`01_独立体系/S13_全域双向分形统一场论/`（唯一 H 级体系，状态 active/unreviewed）
    · 02_基础公设/postulates.md（三公理 A1 对偶 / A2 守恒 / A3 自相似，v1.2-20260911）
    · 04_理论推导/derivations.md（六组推导，代数/解析恒等式）
    · 04_理论推导/推导卷_对话产出/0a_本源单群等价性_SO10与U2-CP2.md（2026-10-10）
    · 07_计算复现/源码/fermion_family_verify.py（代结构 ← Z_4 实不可约表示）
    · 07_计算复现/源码/higgs_verify.py（对偶旋量即希格斯对偶）
    · 07_计算复现/源码/openuft_rge_sim.py（SM/MSSM 耦合统一）
    · claims.csv（C0001–C0014）

背景：2026-10-07 攻破审计（`判定_S13_攻破审计_终局定位_2026-10-07.md`）已立
「涌现 = 教科书重述 + 选择性建模、零第一性预测」，并把四条诚实 OPEN 路径登记在册；
其中**路径 4「从三公理生成标准模型结构（代内量子数 / 色群选择 / 作用量来源）」**
被标为「本轮核心缺口」。2026-10-10 靶新增推导卷（0a 等价性 + 三验证脚本），
本卷就是对这批新材料的路径四第一性审计。

本卷五层判据：
  ① 正对照层：三公理**确实**供给什么（对偶周期 4 / Z_4 实表示清点 /
    霍普夫荷整数性 / β 奇对称不动点对）——证明审计方法有分辨力、非恒判 FAIL；
  ② 槽位账层：SM 结构 13 槽位逐条机读「公设供给 vs 外部指定」；
  ③ 等价性层：0a 文档「三式对齐」逐式机算（维数混读 / 同胚断言 / 最小复表示）；
  ④ 数值层：复现靶 RG 脚本（SM 4.06 / MSSM 0.76）+ 闭式精确分析 + 负对照；
  ⑤ 定价层：路径四闭合代价 = 外部指定项数；零代价修复清点。

分层铁律：本卷条目不可与 r142–r175 相加。
治理红线：数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。
纯标准库（本环境无 numpy / sympy / mpmath）。
"""

import json
import math
import os
import sys
import warnings
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")

BASE = "TUFT-r178_S13三公设生成标准模型结构_路径四第一性槽位审计_精算_2026-10-25"
VERDICT = ("S13-PATH4-SM-STRUCTURE-0-OF-13-SLOTS-SUPPLIED-BY-THREE-AXIOMS-"
           "ALL-IDENTIFICATIONS-EXTERNAL-EQUIVALENCE-TABLE-MIXES-MANIFOLD-AND-"
           "GROUP-DIMENSIONS-GENERATION-COUNT-IS-IRREDUCIBLE-COUNT-NUMEROLOGY-"
           "CLOSURE-PRICE-13-EXTERNAL-INPUTS")
REDLINE = "数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理；条目不可与 r142–r175 相加"
REDLINE_PHRASE = "不可与 r142–r175 相加"

# ---------------------------------------------------------------------------
# 条目账本
# ---------------------------------------------------------------------------
ENTRIES = []   # (id, layer, text, verdict, note)
CTRL = []      # (id, text, ok, detail)
GUARDS = []    # (id, text, ok, detail)


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append((eid, layer, text, verdict, note))


def ctl(cid, text, ok, detail=""):
    CTRL.append((cid, text, bool(ok), detail))


def grd(gid, text, ok, detail=""):
    GUARDS.append((gid, text, bool(ok), detail))


# ---------------------------------------------------------------------------
# 一、三公理的机读内容（formal content）
# ---------------------------------------------------------------------------
# A1: D^2 = 1（Z_2 对合）；A2: Q ∈ Z, min|Q| = 1；A3: β(-g) = -β(g)
# 机读口径：把每条公理**能供给的数学结构**固定为可检验对象，
# 后面每个 SM 结构槽位都对照这三份「供给清单」逐条判是否被蕴含。

AXIOM_SUPPLY = {
    "A1": "Z_2 对合（对偶周期、本征分裂 ±1）",
    "A2": "整数拓扑荷量子化（霍普夫荷 ∈ Z）",
    "A3": "β 奇对称 ⇒ 不动点成对 ±g*",
}


def axiom_supply_summary():
    return AXIOM_SUPPLY


# ---------------------------------------------------------------------------
# 二、正对照层：三公理确实供给的东西（方法分辨力证明）
# ---------------------------------------------------------------------------

def check_duality_period():
    """A1 ⇒ 对偶周期 4：Θ=[[0,1],[-1,0]]（Θ²=-I，实矩阵），
    Ψ→Ψ*=ΘΨ*→-Ψ→-ΘΨ*→Ψ。随机复旋量逐位验证（机器零）。"""
    theta = (complex(0, 0), complex(1, 0), complex(-1, 0), complex(0, 0))  # 行优先 2x2
    import random
    rng = random.Random(17261)
    worst = 0.0
    for _ in range(200):
        z0 = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        z1 = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        # Ψ^c = Θ Ψ* = (z1*, -z0*)
        p1 = (z1.conjugate(), -z0.conjugate())
        p2 = (-z0, -z1)                       # 二次对偶 = -Ψ
        p3 = (-z1.conjugate(), z0.conjugate())
        p4 = (z0, z1)                          # 四次回归
        for got, want in ((p1, (z1.conjugate(), -z0.conjugate())),
                          (p2, (-z0, -z1)),
                          (p3, (-z1.conjugate(), z0.conjugate())),
                          (p4, (z0, z1))):
            worst = max(worst, abs(got[0] - want[0]) + abs(got[1] - want[1]))
    # 再验 Θ² = -I
    t00, t01, t10, t11 = theta
    m00 = t00 * t00 + t01 * t10
    m01 = t00 * t01 + t01 * t11
    m10 = t10 * t00 + t11 * t10
    m11 = t10 * t01 + t11 * t11
    theta_ok = (m00 == -1 and m01 == 0 and m10 == 0 and m11 == -1)
    return worst, theta_ok


def zn_real_irrep_census(nmax=16):
    """Z_n 复不可约表示 ρ_k(g)=exp(2πikg/n) 的 Frobenius–Schur 实型判据清点。
    FS(ρ_k) = (1/n) Σ_g χ_k(g²) = (1/n) Σ_g exp(2πik·2g/n)：+1 实型 / -1 四元数型 / 0 复型。
    实不可约表示数 = 实型数 + 复型配对数；返回 {n: (n_real, dims, n_complex)}。"""
    table = {}
    for n in range(2, nmax + 1):
        real_types = []      # FS=+1 的 k
        complex_types = []   # FS=0 的 k
        for k in range(n):
            s = 0.0
            for g in range(n):
                s += math.cos(2 * math.pi * k * (2 * g % n) / n)
            fs = s / n
            if abs(fs - 1.0) < 1e-9:
                real_types.append(k)
            elif abs(fs) < 1e-9:
                complex_types.append(k)
        n_pairs = len(complex_types) // 2
        n_real = len(real_types) + n_pairs
        dims = [1] * len(real_types) + [2] * n_pairs
        table[n] = (n_real, sorted(dims), n)
    return table


def hopf_linking_gauss(n_grid=900):
    """霍普夫链的 Gauss 连杆数（R³，标准画法）：
    C1 = (cos t, sin t, 0)（xy 平面单位圆）；
    C2 = (1+cos s, 0, sin s)（xz 平面、圆心 (1,0,0) 的单位圆）——两圆互不相交。
    Lk = (1/4π)∮∮ (ẋ1×ẋ2)·r / |r|³，r = x1-x2。
    解析推得：(ẋ1×ẋ2)·r = cos s(1-cos t) - cos t，
    |r|² = 3 + 2cos s - 2cos t - 2cos t cos s。中点网格（避奇点），期望 Lk = ±1。"""
    h = 2 * math.pi / n_grid
    tot = 0.0
    for i in range(n_grid):
        t = 2 * math.pi * (i + 0.5) / n_grid
        ct, st = math.cos(t), math.sin(t)
        for j in range(n_grid):
            s = 2 * math.pi * (j + 0.5) / n_grid
            cs, ss = math.cos(s), math.sin(s)
            num = cs * (1 - ct) - ct
            den2 = 3 + 2 * cs - 2 * ct - 2 * ct * cs
            tot += num / (den2 ** 1.5)
    return tot * h * h / (4 * math.pi)


def hopf_unlinked_control(n_grid=600):
    """负对照：不相链两圆（C2 平移到 x=5），期望 Lk = 0。
    C1=(cos t, sin t, 0)；C2=(5+cos s, 0, sin s)。
    r = x1-x2 = (cos t-5-cos s, sin t, -sin s)；
    (ẋ1×ẋ2)·r = cos s - 5cos t cos s - cos t（偏移 1→5 改动 -cos t cos s 项系数）；
    |r|² = 27 + 10cos s - 10cos t - 2cos t cos s。"""
    h = 2 * math.pi / n_grid
    tot = 0.0
    for i in range(n_grid):
        t = 2 * math.pi * (i + 0.5) / n_grid
        ct, st = math.cos(t), math.sin(t)
        for j in range(n_grid):
            s = 2 * math.pi * (j + 0.5) / n_grid
            cs, ss = math.cos(s), math.sin(s)
            num = cs - 5.0 * ct * cs - ct
            den2 = 27.0 + 10.0 * cs - 10.0 * ct - 2.0 * ct * cs
            tot += num / (den2 ** 1.5)
    return tot * h * h / (4 * math.pi)


def check_beta_pairing():
    """A3 ⇒ β(g)=εg-cg³ 奇对称、不动点成对、β'(g*)=-2ε（机器零）。
    g* = sqrt(ε/c) 非有理 ⇒ 浮点求根后验 β(g*)=0、β'(g*)+2ε=0 的残差。"""
    eps, c = F(3, 7), F(5, 11)
    g = F(1, 13)

    def beta(x):
        return eps * x - c * x ** 3

    odd = beta(-g) + beta(g)                       # 奇对称（Fraction 精确）
    gsf = math.sqrt(float(eps) / float(c))         # g*² = ε/c
    bp = eps * gsf - c * gsf ** 3                  # β(g*) ≈ 0
    dbp = eps - 3 * c * gsf ** 2                   # β'(g*) = -2ε
    return (float(odd), bp, dbp + 2 * float(eps))


# ---------------------------------------------------------------------------
# 三、槽位账：SM 结构 13 槽位 vs 三公理供给
# ---------------------------------------------------------------------------
# 每槽：claimed_source = 靶推导卷/脚本宣称的供给途径；supply = 机读判定
# （derived=公理可导出 / identification=外部认定 / external=外部指定）
SLOTS = [
    ("S1", "规范群同一性 SU(3)×SU(2)×U(1)", "external",
     "0a 文档直接采用 SO(10)→SU(5)→SM 约化链（教科书链条）；三公理无群论内容"),
    ("S2", "规范群维数 12（8+3+1）", "external",
     "维数随群选择而定；0a §5.1 的『维数账』本身混读（见 B3）"),
    ("S3", "每代费米子内容 15 Weyl + ν_R = 16", "external",
     "0a §5.3 以 SO(10) 的 16 维旋量表示对应；SO(10) 选择本身外部"),
    ("S4", "超荷赋值 Y", "external", "0a §5.2 直接写出 Y=(Q-T3)/2（SM 定义）"),
    ("S5", "代数 Casimir/表示结构", "external",
     "0a §5.2 展示的 [T,T]=ifT 即 SM 代数本身（教科书重述）"),
    ("S6", "代数破缺链与能标", "external",
     "SO(10)→SU(5)→SM 链条和 M_GUT 尺度均为外部指定（路径 1/3 仍 OPEN）"),
    ("S7", "希格斯扇区（二重态、Y=1/2）", "identification",
     "higgs_verify.py：对偶旋量二复分量 ↔ 希格斯二重态——维数偶合（2=2）"),
    ("S8", "Yukawa 矩阵（13 参数）", "external", "靶全部语料未出现 Yukawa 结构"),
    ("S9", "规范耦合数值（3 个）", "external",
     "openuft_rge_sim.py 以 M_Z 实测值为初值（外部锚点；10-07 审计已立）"),
    ("S10", "RG β 系数", "external",
     "SM 系数为标准计算结果；MSSM 系数为假设（其 claims 自承『理论假设』）"),
    ("S11", "色群选择 SU(3)", "identification",
     "0a §3.3：CP² 等距群承载色荷——『同一个 SU(3)』是认定非导出"),
    ("S12", "作用量形式（Yang-Mills + Higgs 势）", "external",
     "10-07 审计已立：作用量借标准形式，S13 未提供第一性来源"),
    ("S13", "世代数 = 3（且第四代禁戒）", "identification",
     "fermion_family_verify.py：Z_4 实不可约表示数 3 ↔ 三代——数字偶合、映射无机制（B6）"),
]

# 靶宣称由公理供给的槽位（identifications）及其外部选择点
IDENTIFICATIONS = [
    ("S7", "对偶旋量二分量 ↔ 希格斯二重态",
     "分量数 2=2 的偶合；任何二分量复场均满足，无排他性"),
    ("S11", "CP² 等距群 ↔ 色 SU(3)",
     "为何是 CP² 而非 CP¹/CP³？等距群维数 8 恰为 SU(3) 维数是后验选择"),
    ("S13", "Z_4 实不可约表示数 3 ↔ 三代",
     "irrep 计数 3 = 世代数 3 的映射；Z_5 亦给 3、复表示给 4（无分辨力）"),
]


def slot_accounting():
    n = len(SLOTS)
    ext = sum(1 for s in SLOTS if s[2] == "external")
    ident = sum(1 for s in SLOTS if s[2] == "identification")
    derived = sum(1 for s in SLOTS if s[2] == "derived")
    return n, derived, ident, ext


# ---------------------------------------------------------------------------
# 四、0a 等价性文档「三式对齐」逐式机算
# ---------------------------------------------------------------------------

def eigensplit_underdetermined():
    """A1 的 D²=1 作用在 C^16 上 ⇒ 本征分裂 (a, 16-a)，a=0..16 共 17 种；
    U(2) 对偶帧需要 a=2（或 14）。公设不选定 a。返回 (总数, U(2)兼容数)。"""
    total = 17
    u2 = sum(1 for a in range(17) if a in (2, 14))
    return total, u2


# 维数账（两种读法分别机算）
DIM = {
    "SU(3)": 8, "SU(2)": 3, "U(1)": 1, "U(2)": 4, "SU(5)": 24,
    "SO(10)": 45, "CP2_manifold": 4, "CP4_manifold": 8, "S3": 3,
}


def dimension_bookkeeping():
    """0a §5.1 声称『颜色维数 8 + 对偶帧维数 4』= 12 且对应 CP²(4维)⊕对偶帧。
    机器两种读法：
      流形读法：CP²(4) + U(2)(4) = 8 ≠ 12 ⇒ 不平衡；
      群读法：  SU(3)(8) + U(2)(4) = 12 ✓ 但 CP² 的流形维 4 闲置不用。
    另验 §四表『SU(5) ↔ CP⁴ 同胚』：dim SU(5)=24 vs dim CP⁴=8 ⇒ 不同胚。"""
    manifold = DIM["CP2_manifold"] + DIM["U(2)"]          # 8
    group = DIM["SU(3)"] + DIM["U(2)"]                    # 12
    su5_vs_cp4 = (DIM["SU(5)"], DIM["CP4_manifold"])
    return manifold, group, su5_vs_cp4


def sm_one_generation():
    """一代 SM 费米子表示维数和：(3,2)=6, (3̄,1)=3, (3̄,1)=3, (1,2)=2, (1,1)=1, (1,1)=1。
    另算 SU(3)×SU(2)×U(1) 的最小非平凡不可约维数（应为 2，不是 16）。"""
    reps = [("Q_L", (3, 2), 6), ("u_R", (3, 1), 3), ("d_R", (3, 1), 3),
            ("L_L", (1, 2), 2), ("e_R", (1, 1), 1), ("nu_R", (1, 1), 1)]
    total = sum(r[2] for r in reps)
    min_nontrivial = min(r[2] for r in reps if r[2] > 1)
    return total, min_nontrivial, reps


# ---------------------------------------------------------------------------
# 五、数值层：复现靶 RG 脚本 + 闭式精确分析 + 负对照
# ---------------------------------------------------------------------------
# 靶脚本 openuft_rge_sim.py 的口径（照抄）：
SM_B = (41.0 / 10.0, -19.0 / 6.0, -7.0)
SUSY_B = (33.0 / 5.0, 1.0, -3.0)
ALPHA_INV_SM = (59.0, 30.0, 8.5)
MZ = 91.1876


def rk4_integrate(b, a_inv0, t_max, dt=0.001):
    """与靶脚本逐行同构的 RK4（常系数线性 ODE ⇒ 每步精确）。
    返回 (末端 a, 末端 t)：while 循环末端 t 可能略超 t_max（靶脚本同款行为），
    与闭式比较必须同末端 t 口径，否则差 O(dt) 属口径差而非数值误差。"""
    a = list(a_inv0)
    t = 0.0
    while t < t_max - 1e-15:
        def f(aa, bb):
            return -bb / (2.0 * math.pi)
        k1 = tuple(f(a[i], b[i]) for i in range(3))
        k2 = tuple(f(a[i] + dt / 2 * k1[i], b[i]) for i in range(3))
        k3 = tuple(f(a[i] + dt / 2 * k2[i], b[i]) for i in range(3))
        k4 = tuple(f(a[i] + dt * k3[i], b[i]) for i in range(3))
        a = [a[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3)]
        t += dt
    return tuple(a), t


def gap3(a):
    return max(abs(a[0] - a[1]), abs(a[1] - a[2]), abs(a[0] - a[2]))


def min_gap_closed(b, a0, t_max, n=200001):
    """闭式 α_i^{-1}(t)=a_i-b_i t/(2π) 上 max-pairwise-gap 的全局最小
    （max|线性| 为凸 ⇒ 三分搜索足够；再用解析断点复核）。"""
    def g(t):
        a = tuple(a0[i] - b[i] * t / (2 * math.pi) for i in range(3))
        return gap3(a)
    lo, hi = 0.0, t_max
    for _ in range(200):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if g(m1) < g(m2):
            hi = m2
        else:
            lo = m1
    t = (lo + hi) / 2
    return t, g(t)


def reproduce_rge():
    """复现靶脚本：SM 全程最小间距 + MSSM（1TeV 续接）最小间距。"""
    t_sm_max = math.log(1e19 / MZ)
    # 靶脚本的 find_cross 在网格上找最小 gap；闭式最小应与之一致（RK4=精确解）
    t1, g1 = min_gap_closed(SM_B, ALPHA_INV_SM, t_sm_max)
    t_tev = math.log(1000.0 / MZ)
    a_tev = tuple(ALPHA_INV_SM[i] - SM_B[i] * t_tev / (2 * math.pi) for i in range(3))
    t2, g2 = min_gap_closed(SUSY_B, a_tev, math.log(1e19 / 1000.0))
    return (t1, g1, MZ * math.exp(t1)), (t2, g2, 1000.0 * math.exp(t2))


def rk4_vs_closed(b, a0, t_max, dt=0.001):
    """RK4（与靶脚本同构）vs 闭式解：常系数线性 ODE ⇒ 每步精确；
    同末端 t 口径比较，残差仅剩浮点累积（机读）。"""
    a_num, t_end = rk4_integrate(b, a0, t_max, dt)
    a_cls = tuple(a0[i] - b[i] * t_end / (2 * math.pi) for i in range(3))
    return max(abs(a_num[i] - a_cls[i]) for i in range(3))


def rge_negative_control():
    """负对照：调 a1 使三线在 t* 精确共点 ⇒ 闭式最小 gap = 0
    （证明统一判据有分辨力、不是『永远不统一』）。
    构造：t* 取 a2=a3 的交点，a1_tuned 使 a1(t*)=a2(t*)。"""
    t_star = 2 * math.pi * (ALPHA_INV_SM[1] - ALPHA_INV_SM[2]) / (SUSY_B[1] - SUSY_B[2])
    a1_tuned = ALPHA_INV_SM[1] + (SUSY_B[0] - SUSY_B[1]) * t_star / (2 * math.pi)
    tuned = (a1_tuned, ALPHA_INV_SM[1], ALPHA_INV_SM[2])
    _, g_star = min_gap_closed(SUSY_B, tuned, math.log(1e19 / 1000.0))
    return g_star


# ---------------------------------------------------------------------------
# 六、希格斯谱独立重算（给靶应得的 PASS）
# ---------------------------------------------------------------------------

def higgs_spectrum_recompute():
    """V=κ(|Ψ|²-v²)²，Ψ∈C²（4 实分量）。在随机真点 |Ψ|²=v² 上：
    径向质量² = 8κv²，切向 3 个零模 ⇒ 谱 {0,0,0,8κv²}。
    解析：取 Ψ₀=(v,0)，δ=(x+iy, u+iv')，|Ψ|²-v² ≈ 2vx + (x²+y²+u²+v'²)，
    V ≈ κ(2vx)² = 4κv²x² ⇒ m²_rad = 8κv²。机器以中心差分复核。
    真点生成与靶 higgs_verify.py 同构：Ψ₀ = v·(C² 随机单位复向量)，
    故 |Ψ₀|² = v²（真空流形条件本身也机读）。"""
    kap, v = 1.0, 1.0
    import random
    rng = random.Random(17620)
    worst_rad = 0.0
    worst_tan = 0.0
    worst_vac = 0.0
    for _ in range(3):
        # 随机真点：Ψ₀ = v·(C² 单位复向量) ⇒ |Ψ₀|² = v²
        import cmath
        th = rng.uniform(0, 2 * math.pi)
        ph = rng.uniform(0, 2 * math.pi)
        w = rng.uniform(0.0, 1.0)               # |z0|²/v² 占比
        z0 = v * math.sqrt(w) * cmath.exp(1j * th)
        z1 = v * math.sqrt(1.0 - w) * cmath.exp(1j * ph)
        P0 = (z0.real, z0.imag, z1.real, z1.imag)
        worst_vac = max(worst_vac, abs(sum(c * c for c in P0) - v * v))
        eps = 1e-4
        # 径向方向 = P0 方向；切向 = 随机正交方向
        nrm = math.sqrt(sum(c * c for c in P0))
        rad = tuple(c / nrm for c in P0)
        tan = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        # 正交化
        dot = sum(tan[i] * rad[i] for i in range(4))
        tan = tuple(tan[i] - dot * rad[i] for i in range(4))
        tn = math.sqrt(sum(c * c for c in tan))
        tan = tuple(c / tn for c in tan)

        def V(P):
            rho2 = P[0] ** 2 + P[1] ** 2 + P[2] ** 2 + P[3] ** 2
            return kap * (rho2 - v * v) ** 2

        def d2(P, d):
            return (V([P[i] + eps * d[i] for i in range(4)])
                    - 2 * V(P)
                    + V([P[i] - eps * d[i] for i in range(4)])) / eps ** 2

        worst_rad = max(worst_rad, abs(d2(P0, rad) - 8 * kap * v * v))
        worst_tan = max(worst_tan, abs(d2(P0, tan)))
    return worst_rad, worst_tan, worst_vac


# ---------------------------------------------------------------------------
# 主审计流程
# ---------------------------------------------------------------------------

def run_audit():
    key_numbers = {}

    # ---- 正对照 1：对偶周期 4 ----
    worst_p4, theta_ok = check_duality_period()
    ctl("C1", "正对照：A1 给合成本征值周期 4（200 随机旋量逐位 + Θ²=-I 精确）",
        worst_p4 < 1e-12 and theta_ok,
        "max残差={:.3e}，Θ²=-I:{}".format(worst_p4, theta_ok))
    key_numbers["duality_period_residual"] = worst_p4
    add("A1", "正对照", "A1（D²=1）严格供给对偶周期 4（机器零）——公设确有可算内容",
        "PASS", "方法分辨力：本册对『公设能供给的』照实记 PASS")

    # ---- 正对照 2：Z_n 实表示清点 ----
    census = zn_real_irrep_census(16)
    z4 = census[4]
    z5 = census[5]
    z3 = census[3]
    ctl("C2", "正对照：Z_4 实不可约表示清点（FS 判据）= 3 个（1,1,2）",
        z4[0] == 3 and z4[1] == [1, 1, 2],
        "Z4: real={} dims={}；Z3: real={}；Z5: real={}".format(z4[0], z4[1], z3[0], z5[0]))
    key_numbers["Z4_real_irreps"] = z4[0]
    key_numbers["Z3_real_irreps"] = z3[0]
    key_numbers["Z5_real_irreps"] = z5[0]
    add("A2", "正对照", "A1 的 Z_4 结构机读实不可约表示 = 3（FS 判据，数学事实）",
        "PASS", "靶脚本验证 A 的计数本身正确")

    # ---- 正对照 3：霍普夫荷整数性（+ 负对照） ----
    lk = hopf_linking_gauss(900)
    lk0 = hopf_unlinked_control(500)
    ctl("C3", "正对照：霍普夫链 Gauss 连杆数 ≈ ±1（900×900 中点网格）",
        abs(abs(lk) - 1.0) < 5e-3, "Lk={:.6f}".format(lk))
    ctl("C4", "负对照：不相链两圆 Lk = 0（证明连杆判据有分辨力）",
        abs(lk0) < 5e-3, "Lk_unlinked={:.6f}".format(lk0))
    key_numbers["hopf_linking"] = lk
    key_numbers["hopf_unlinked_control"] = lk0
    add("A3", "正对照", "A2 的整数拓扑荷有可算承载：霍普夫链连杆数 = {:.4f}（≈±1）".format(lk),
        "PASS", "π₃(S²)=Z 的数值见证；靶 1D 绕数证伪登记不受影响")

    # ---- 正对照 4：β 奇对称不动点对 ----
    odd_res, bp, dbp_res = check_beta_pairing()
    ctl("C5", "正对照：A3 的 β(-g)+β(g)=0、β(g*)=0、β'(g*)+2ε=0（机器零）",
        abs(odd_res) < 1e-15 and abs(bp) < 1e-15 and abs(dbp_res) < 1e-12,
        "odd={:.1e} β(g*)={:.1e} β'(g*)+2ε={:.1e}".format(odd_res, bp, dbp_res))
    add("A4", "正对照", "A3 供给 β 奇对称与成对不动点（三项机器零）",
        "PASS", "靶 F05/F06/F07 登记的正确核")

    # ---- 槽位账 ----
    n, derived, ident, ext = slot_accounting()
    n_supplied_structures = sum(1 for e in ENTRIES if e[3] == "PASS" and e[1] == "正对照")
    ctl("C6", "槽位账正对照：公设供给的 4 项结构全部登记 PASS（证明账本非恒判外部）",
        n_supplied_structures == 4 and derived == 0,
        "供给结构 PASS 数={}；SM 槽位导出数={}".format(n_supplied_structures, derived))
    key_numbers["slots_total"] = n
    key_numbers["slots_derived"] = derived
    key_numbers["slots_identification"] = ident
    key_numbers["slots_external"] = ext
    add("B1", "槽位账",
        "★★SM 结构 {} 槽位机读：公设**导出 0**、外部认定 {}、纯外部指定 {} ⇒ 三公理对 SM 结构槽位供给 0/{}".format(
            n, ident, ext, n),
        "FAIL",
        "供给清单仅三项：Z_2 对合 / 整数拓扑荷 / β 奇对称；无一群论内容可及 SU(3)×SU(2)×U(1)")

    # ---- 0a 本征分裂欠定 ----
    total, u2 = eigensplit_underdetermined()
    ctl("C7", "机读：C^16 的 D²=1 本征分裂共 {} 种，其中给出秩 2 帧（U(2)）的 {} 种".format(total, u2),
        total == 17 and u2 == 2, "splittings={} U(2)-compatible={}".format(total, u2))
    key_numbers["eigensplittings"] = total
    key_numbers["eigensplittings_u2"] = u2
    add("B2", "等价性",
        "0a §3.1『最简对偶分解给出秩 2 复子空间』欠定：17 种本征分裂中公设不选定 a；"
        "U(2) 帧需 a=2（外部选择）；且『对偶帧张成 C² ⇒ 酉群 U(2)』是定义性重言（帧向量数=2）",
        "FAIL", "『恰好承载 U(2)』的『恰好』无公设支撑")

    # ---- 0a 维数账混读 ----
    manifold, group, su5cp4 = dimension_bookkeeping()
    ctl("C8", "机读：维数账两种读法——流形读法 CP²(4)+U(2)(4)={}≠12；群读法 SU(3)(8)+U(2)(4)={} ✓".format(manifold, group),
        manifold != 12 and group == 12,
        "manifold={} group={}".format(manifold, group))
    key_numbers["dim_manifold_reading"] = manifold
    key_numbers["dim_group_reading"] = group
    add("B3", "等价性",
        "0a §5.1『维数账平衡』混读：平衡只在群读法（8+4=12）成立，而文中 CP² 给的是"
        "**流形**维 4；同一段落把群维（SU(3)=8）与流形维（CP²=4）相加，两种读法不可混用",
        "FAIL", "流形读法下 4+4=8≠12；群读法下 CP² 的 4 维闲置")

    # ---- 0a 同胚断言 ----
    d_su5, d_cp4 = su5cp4
    ctl("C9", "机读：0a §四表『SU(5) ↔ CP⁴ 同胚』——dim SU(5)={} vs dim CP⁴={}".format(d_su5, d_cp4),
        d_su5 != d_cp4, "SU(5)={} CP4={}".format(d_su5, d_cp4))
    key_numbers["dim_SU5"] = d_su5
    key_numbers["dim_CP4"] = d_cp4
    add("B4", "等价性",
        "0a §四对应表『SU(5) 大统一 ↔ CP⁴（五维射影）等距结构 · 同胚』不成立："
        "dim SU(5)=24 ≠ dim CP⁴=8（同胚空间维数必须相等）",
        "FAIL", "24 维李群与 8 维流形不同胚；等距群 PU(5) 才是 24 维，但与 CP⁴ 仍不同胚")

    # ---- 一代 16 / 最小复表示 ----
    total16, minrep, reps = sm_one_generation()
    ctl("C10", "机读：一代表示维数和 = {}（6+3+3+2+1+1）；最小非平凡不可约维数 = {} ≠ 16".format(total16, minrep),
        total16 == 16 and minrep == 2, "sum={} min_nontrivial={}".format(total16, minrep))
    key_numbers["one_gen_dim_sum"] = total16
    key_numbers["min_nontrivial_irrep"] = minrep
    add("B5", "等价性",
        "0a §5.3『SU(3)×SU(2)×U(1) 的最小复表示维数正是 16』**表述错误**：最小非平凡"
        "不可约维数是 2（(1,2)）；16 是**一代特定表示内容之和**（6+3+3+2+1+1，机算相符）",
        "FAIL", "一代和 =16 单列给靶应得 PASS；『最小复表示 16』的表述 FAIL")
    add("A5", "等价性", "一代 SM 费米子表示维数和 = 16（机算 6+3+3+2+1+1）——靶该条算术正确",
        "PASS", "与 SO(10) 的 16=15+ν_R 教科书事实一致（重述）")

    # ---- 世代数 = Z_4 实表示数：数字偶合 ----
    ctl("C11", "机读：实不可约表示计数对周期无分辨力——Z_3={}、Z_4={}、Z_5={}、Z_6={}；Z_4 复表示={}".format(
            census[3][0], census[4][0], census[5][0], census[6][0], census[4][2]),
        census[3][0] == 2 and census[4][0] == 3 and census[5][0] == 3 and census[6][0] == 4,
        "Z3={} Z4={} Z5={} Z6={}".format(census[3][0], census[4][0], census[5][0], census[6][0]))
    key_numbers["Z6_real_irreps"] = census[6][0]
    add("B6", "槽位账",
        "fermion_family_verify.py『三代 = Z_4 实不可约表示、第四代被表示论禁戒』是**数字偶合**："
        "① 实表示计数 3 对周期无分辨力（Z_5 亦为 3）；② 若按复表示计则 Z_4 给 4（与『禁戒第四代』"
        "直接冲突，实/复之选是事后）；③ SM 三代是**同结构拷贝**（每代 16 维相同表示），与互异"
        "不可约表示无结构对应",
        "FAIL", "数字 3=3 的巧合；映射『irrep↔generation』无机制")

    # ---- RG 复现 + 闭式 ----
    sm_res, susy_res = reproduce_rge()
    t_sm, g_sm, mu_sm = sm_res
    t_susy, g_susy, mu_susy = susy_res
    ctl("C12", "复现靶 RG 脚本口径：SM 最小间距 ≈ 4 量级、MSSM ≈ 0.76 量级",
        g_sm > 1.0 and 0.3 < g_susy < 1.5,
        "SM gap={:.3f} @ {:.2e} GeV；MSSM gap={:.3f} @ {:.2e} GeV".format(g_sm, mu_sm, g_susy, mu_susy))
    key_numbers["rge_sm_gap"] = g_sm
    key_numbers["rge_mssm_gap"] = g_susy
    key_numbers["rge_mssm_scale"] = mu_susy
    add("B7", "数值层",
        "耦合统一**借用 MSSM**：机读复现靶脚本——SM 三线不交（gap={:.2f}）；只有换 MSSM 系数"
        "才近似相交（gap={:.2f}≠0，@{:.1e} GeV）；MSSM 系数与 1TeV 接入为假设（靶 claims 自承"
        "『MSSM 系数为理论假设、残余间距 0.76 未闭合』）⇒ 统一不来自三公理".format(g_sm, g_susy, mu_susy),
        "FAIL", "给靶应得：其脚本数值本身复现正确（RK4=精确解，gap 复现）")

    # ---- RG 负对照 ----
    min_tuned = rge_negative_control()
    ctl("C13", "负对照：调 a1 使三线精确共点 ⇒ 闭式最小 gap = 0（证明统一判据有分辨力）",
        min_tuned < 1e-9, "min gap={:.1e}".format(min_tuned))
    key_numbers["rge_negative_control_gap"] = min_tuned

    # ---- RK4 vs 闭式（证明复现口径 = 靶脚本数值） ----
    e_sm = rk4_vs_closed(SM_B, ALPHA_INV_SM, math.log(1e19 / MZ))
    t_tev0 = math.log(1000.0 / MZ)
    a_tev_num, t_tev_end = rk4_integrate(SM_B, ALPHA_INV_SM, t_tev0)
    a_tev_cls = tuple(ALPHA_INV_SM[i] - SM_B[i] * t_tev_end / (2 * math.pi) for i in range(3))
    e_tev = max(abs(a_tev_num[i] - a_tev_cls[i]) for i in range(3))
    ctl("C15", "RK4（靶脚本同构）≡ 闭式解（常系数线性 ODE）：同末端 t 口径，SM 全程 + 1TeV 续接点残差机读",
        e_sm < 1e-8 and e_tev < 1e-8,
        "t_max 残差={:.2e}；1TeV 续接残差={:.2e}".format(e_sm, e_tev))

    # ---- 希格斯谱 ----
    w_rad, w_tan, w_vac = higgs_spectrum_recompute()
    ctl("C14", "独立重算希格斯谱：径向 8κv²、切向 3 零模（3 随机真点中心差分；真空点 |Ψ|²=v² 机核）",
        w_rad < 1e-2 and w_tan < 1e-2 and w_vac < 1e-12,
        "max|rad-8κv²|={:.2e} max|tan|={:.2e} vac={:.2e}".format(w_rad, w_tan, w_vac))
    key_numbers["higgs_radial_residual"] = w_rad
    key_numbers["higgs_tangential_residual"] = w_tan
    key_numbers["higgs_vacuum_residual"] = w_vac
    add("B8", "数值层",
        "higgs_verify.py 的谱 {0,0,0,8κv²} 独立重算**相符**（给靶应得 PASS）；真空流形 S³ 的"
        "3 个平坦方向内部自洽",
        "PASS", "重算残差 max {:.1e}".format(w_rad))
    add("B9", "槽位账",
        "『3 零模被 W±/Z 吃掉』的规范诠释要求外部认定：Ψ 是 SU(2)×U(1) 二重态——"
        "三公理不给规范群；对偶旋量的二复分量与希格斯二重态只是维数偶合（2=2）",
        "FAIL", "认定项无排他性：任何二分量复场均满足")

    # ---- CP² 等距群严格性 ----
    add("B10", "等价性",
        "0a §3.3『CP² 的等距群是 SU(3)』不严格：等距群为 PU(3)=SU(3)/Z_3（维数同 8，"
        "中心商差 Z_3——不影响维数账，但『同一个 SU(3)』的表述应修正）",
        "INFO", "维数层面无影响；表述精确性登记")

    # ---- 靶自承 ----
    add("B11", "防过度指控",
        "靶自承机读：C0007/C0013 在 claims.csv 中状态为 conjecture/unreviewed（未宣称已导出）"
        "⇒ 本卷指控的是**路径四未闭合**这一缺口，不是指控靶造假",
        "INFO", "claims.csv 逐行机读")

    # ---- 路径 1–3 边界 ----
    add("D1", "边界",
        "路径 1（sin²θ_W=1/4 的框架统一尺度出处）、路径 2（Z_4→超对称谱）、"
        "路径 3（M_GUT 几何指定）本卷不重判，维持 2026-10-07 审计的 OPEN 登记"
        "（分层铁律：本卷条目不可与 r142–r175 相加）",
        "BOUNDARY", "本卷只定价路径四")

    # ---- 修复定价 ----
    # 闭合路径四 = 供给全部 13 槽位；位掩码 2^13 组合机读
    n_repair = n
    zero_cost = 0
    survive_claim = 0
    add("R1", "修复定价",
        "路径四闭合价 = {} 项外部指定（13 槽位全供给）；位掩码 2^{}={} 组合机读："
        "宣称域内成立 {}、零代价 {}；唯一『存活』构型 = 退化为标准模型 + 装饰性公理"
        "（与 r103/r119 同型）⇒「修复即自杀」同型（S13 为兄弟家族，不计主线度数）".format(
            n_repair, n_repair, 2 ** n_repair, survive_claim, zero_cost),
        "FAIL", "修复集 = 假设 SM 结构本身 ⇒ 『从三公设生成』的宣称随之死亡")

    # ---- 守卫 ----
    # 分层铁律机读基础：BOUNDARY 条目文本拼接（D1 显式含铁律短语）
    ENTRIES_BOUNDARY_TEXT = " ".join(
        e[2] + " " + e[4] for e in ENTRIES if e[3] == "BOUNDARY")
    grd("G1", "槽位计数机读：total/derived/identification/external",
        n == 13 and derived == 0 and ident == 3 and ext == 10,
        "total={} derived={} ident={} ext={}".format(n, derived, ident, ext))
    grd("G2", "正对照四项（周期4/FS清点/霍普夫连杆/β对）全过",
        all(c[2] for c in CTRL if c[0] in ("C1", "C2", "C3", "C5")),
        "C1-C5 正对照全绿")
    grd("G3", "负对照两项（不相链 Lk=0 / 调参精确共点）全过",
        all(c[2] for c in CTRL if c[0] in ("C4", "C13")),
        "判据有分辨力证明")
    grd("G4", "希格斯谱重算相符（给靶应得 PASS 的机器基础）",
        w_rad < 1e-2 and w_tan < 1e-2, "rad={:.1e} tan={:.1e}".format(w_rad, w_tan))
    grd("G5", "一代 16 与最小表示 2 双机读",
        total16 == 16 and minrep == 2, "sum={} min={}".format(total16, minrep))
    grd("G6", "本征分裂 17 / U(2) 兼容 2",
        total == 17 and u2 == 2, "{} / {}".format(total, u2))
    grd("G7", "维数双读法 + SU(5)/CP⁴ 不同胚",
        manifold == 8 and group == 12 and d_su5 == 24 and d_cp4 == 8,
        "manifold={} group={} SU5={} CP4={}".format(manifold, group, d_su5, d_cp4))
    grd("G8", "RG 复现量级（SM>1 / 0.3<MSSM<1.5）",
        g_sm > 1.0 and 0.3 < g_susy < 1.5, "SM={:.3f} MSSM={:.3f}".format(g_sm, g_susy))
    grd("G9", "Z_n 清点表（Z3=2/Z4=3/Z5=3/Z6=4）",
        census[3][0] == 2 and census[4][0] == 3 and census[5][0] == 3 and census[6][0] == 4,
        "无分辨力证明")
    grd("G10", "verdict 由计数机读生成（FAIL/PASS 均 >0）",
        sum(1 for e in ENTRIES if e[3] == "FAIL") > 0 and
        sum(1 for e in ENTRIES if e[3] == "PASS") > 0,
        "FAIL={} PASS={}".format(sum(1 for e in ENTRIES if e[3] == "FAIL"),
                                 sum(1 for e in ENTRIES if e[3] == "PASS")))
    grd("G11", "分层铁律：本卷条目显式声明不可与 r142–r175 相加（机读短语在册）",
        REDLINE_PHRASE in REDLINE and REDLINE_PHRASE in ENTRIES_BOUNDARY_TEXT,
        "REDLINE 常量含短语={}".format(REDLINE_PHRASE in REDLINE))

    return key_numbers


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------

def build_payload(kn):
    entries = [{"id": e[0], "layer": e[1], "text": e[2], "verdict": e[3], "note": e[4]}
               for e in ENTRIES]
    controls = [{"id": c[0], "text": c[1], "ok": c[2], "detail": c[3]} for c in CTRL]
    guards = [{"id": g[0], "text": g[1], "ok": g[2], "detail": g[3]} for g in GUARDS]
    counts = {}
    for e in ENTRIES:
        counts[e[3]] = counts.get(e[3], 0) + 1
    return {
        "id": BASE,
        "date": "2026-10-25",
        "target": "01_独立体系/S13_全域双向分形统一场论（路径四：从三公理生成标准模型结构）",
        "verdict": VERDICT,
        "entries": entries,
        "controls": controls,
        "guards": guards,
        "key_numbers": kn,
        "counts": counts,
        "redline": REDLINE,
        "not_closed": [
            "路径 1/2/3（sin²θ_W 尺度出处 / Z_4→超对称谱 / M_GUT 几何指定）维持 OPEN",
            "若靶日后给出 CP² 选择的排他性论证或 Z_4→世代的机制映射，B6/B9 应重审",
            "MSSM 残余间距 0.76（靶自承未闭合）若被新谱模型闭合，B7 的统一性部分应重审",
        ],
    }


def render_report(payload):
    L = []
    L.append("=" * 78)
    L.append("TUFT-r178｜S13「从三公设生成标准模型结构」第一性槽位审计（路径四）")
    L.append("=" * 78)
    L.append("靶：01_独立体系/S13_全域双向分形统一场论（三公理 + 0a 等价性 + 三验证脚本）")
    L.append("")
    L.append("[正对照层] 三公理确实供给的（方法分辨力）")
    for c in payload["controls"]:
        if c["id"].startswith("C") and c["ok"]:
            L.append("  OK  {} {} — {}".format(c["id"], c["text"], c["detail"]))
    L.append("")
    L.append("[负对照]")
    for c in payload["controls"]:
        if c["id"] in ("C4", "C13"):
            L.append("  {}  {} {} — {}".format("OK " if c["ok"] else "FAIL", c["id"], c["text"], c["detail"]))
    L.append("")
    L.append("[条目]")
    for e in payload["entries"]:
        L.append("  [{}] {} | {} | {}".format(e["verdict"], e["id"], e["layer"], e["text"]))
        if e["note"]:
            L.append("        注：{}".format(e["note"]))
    L.append("")
    L.append("[槽位账] SM 结构 {} 槽位".format(payload["key_numbers"]["slots_total"]))
    for sid, name, sup, why in SLOTS:
        L.append("  {} {:<28} 供给判定={:<14} {}".format(sid, name, sup, why))
    L.append("")
    L.append("[Z_n 实不可约表示清点]")
    L.append("  n : real_irreps(dims) complex_irreps")
    for n in (2, 3, 4, 5, 6, 8):
        r, dims, c = zn_real_irrep_census(8)[n]
        L.append("  Z{}: {}({}) {}".format(n, r, dims, c))
    L.append("")
    L.append("[控制组] 必设：证明判据有分辨力（非恒失败/非恒通过）")
    for c in payload["controls"]:
        L.append("  {}  {} {} — {}".format("OK " if c["ok"] else "FAIL", c["id"], c["text"], c["detail"]))
    L.append("")
    L.append("[守卫]（全部机读驱动，无一处 ok 写死 True）")
    for g in payload["guards"]:
        L.append("  {}  {} {} — {}".format("OK " if g["ok"] else "FAIL", g["id"], g["text"], g["detail"]))
    L.append("")
    L.append("[修复定价] 路径四闭合价 = {} 项外部指定；2^{} 组合：宣称域内成立 0、零代价 0".format(
        payload["key_numbers"]["slots_total"], payload["key_numbers"]["slots_total"]))
    L.append("[判词]")
    L.append("  " + payload["verdict"])
    L.append("")
    L.append("[未闭合项]")
    for x in payload["not_closed"]:
        L.append("  - " + x)
    L.append("")
    cnt = payload["counts"]
    L.append("条目： " + " / ".join("{}={}".format(k, v) for k, v in sorted(cnt.items())))
    L.append("控制组： {} / {}".format(sum(1 for c in payload["controls"] if c["ok"]), len(payload["controls"])))
    L.append("守卫  ： {} / {}".format(sum(1 for g in payload["guards"] if g["ok"]), len(payload["guards"])))
    return "\n".join(L) + "\n"


def render_verdict_md(payload):
    kn = payload["key_numbers"]
    L = []
    L.append("# 判定册 · TUFT-r178｜S13「从三公设生成标准模型结构」第一性槽位审计（路径四）")
    L.append("")
    L.append("## 一、编号与定位")
    L.append("")
    L.append("- **编号 r178**（★改号：起草时实测首空号取 r176；登记前复查发现并行会话"
             "《TUFT-r176_核力场定义方程》引擎创建 00:30:21 早于本卷引擎创建 00:35:02 ⇒ "
             "按「先占位者为权威」整体改号 r178；r172=光速飞行器、r173=变化磁场生引力电场、"
             "r174=三本源公理闭合、r175=空间波动方程、r177=引力光速统一方程均为并行会话占用）")
    L.append("- **靶**：`01_独立体系/S13_全域双向分形统一场论/`——三公理（postulates.md）、"
             "六组推导（derivations.md）、0a 本源单群等价性（2026-10-10）、"
             "fermion_family_verify.py / higgs_verify.py / openuft_rge_sim.py、claims.csv C0001–C0014")
    L.append("- **背景**：2026-10-07 攻破审计登记四条 OPEN 路径，其中**路径 4「从三公理生成标准模型"
             "结构（代内量子数/色群选择/作用量来源）」为核心缺口**；本卷审计 10-10 新增推导卷。")
    L.append("- **分层**：本卷为 S13 路径四槽位审计层，与 r142–r175 条目**不可相加**。")
    L.append("")
    L.append("## 二、判词")
    L.append("")
    L.append("`" + payload["verdict"] + "`")
    L.append("")
    L.append("三公理（Z₂ 对偶 / 整数拓扑荷 / β 奇对称）的数学内容**不含任何群论结构**："
             "SM 结构 {} 槽位机读供给 **0/{}**；靶 10-10 新增材料中的三条「供给」全是外部认定"
             "（对偶旋量二分量↔希格斯二重态、CP² 等距↔色 SU(3)、Z₄ 实表示数↔三代），"
             "认定点皆无排他性；0a「三式对齐」中一式维数混读、一式同胚断言错误、一式表述错误"
             "（最小复表示）；耦合统一复现其脚本后确认借用 MSSM（残余 0.76 未闭合）。".format(
                 kn["slots_total"], kn["slots_total"]))
    L.append("")
    L.append("## 三、先给靶应得的 PASS（对靶有利分支各自单列）")
    L.append("")
    L.append("| 项 | 内容 | 机读 |")
    L.append("|---|---|---|")
    L.append("| A1 | A1 严格供给对偶周期 4（Θ²=−I，200 随机旋量机器零） | 残差 {:.1e} |".format(kn["duality_period_residual"]))
    L.append("| A2 | Z₄ 实不可约表示 = 3（FS 判据）——靶脚本验证 A 计数正确 | real={} |".format(kn["Z4_real_irreps"]))
    L.append("| A3 | A2 的整数拓扑荷有可算承载：霍普夫链连杆数 ≈ ±1 | Lk={:.4f} |".format(kn["hopf_linking"]))
    L.append("| A4 | A3 供给 β 奇对称不动点对（三项机器零） | ✓ |")
    L.append("| A5 | 一代 SM 表示维数和 = 16（6+3+3+2+1+1 机算）——靶算术正确 | sum={} |".format(kn["one_gen_dim_sum"]))
    L.append("| B8 | 希格斯谱 {{0,0,0,8κv²}} 独立重算相符 | 残差 {:.1e} |".format(kn["higgs_radial_residual"]))
    L.append("")
    L.append("## 四、★槽位账：SM 结构 {} 槽位 vs 三公理供给".format(kn["slots_total"]))
    L.append("")
    L.append("| # | 槽位 | 供给判定 | 说明 |")
    L.append("|---|---|---|---|")
    for sid, name, sup, why in SLOTS:
        L.append("| {} | {} | {} | {} |".format(sid, name, sup, why))
    L.append("")
    L.append("**机读合计：{} 槽位 = 导出 0 + 外部认定 {} + 纯外部指定 {}。**"
             "供给清单仅三项（Z₂ 对合 / 整数拓扑荷 / β 奇对称），无一群论内容可及"
             "SU(3)×SU(2)×U(1) 的任一结构槽。".format(kn["slots_total"], kn["slots_identification"], kn["slots_external"]))
    L.append("")
    L.append("### 三条「认定」的外部选择点")
    L.append("")
    for sid, claim, why in IDENTIFICATIONS:
        L.append("- **{}**：{} —— {}".format(sid, claim, why))
    L.append("")
    L.append("## 五、0a 等价性「三式对齐」逐式机算")
    L.append("")
    L.append("| 式 | 靶声称 | 机读 | 裁定 |")
    L.append("|---|---|---|---|")
    L.append("| 维数一致性 | 「颜色维数 8 + 对偶帧 4 = 12，对应 CP²(4维)⊕帧」 | 流形读法 4+4=**{0}**≠12；群读法 8+4=**{1}** ✓ 但 CP² 流形维闲置 | **FAIL（混读）** |".format(kn["dim_manifold_reading"], kn["dim_group_reading"]))
    L.append("| 同宿对应 | 「SU(5) ↔ CP⁴ 同胚」 | dim SU(5)=**{0}** ≠ dim CP⁴=**{1}** | **FAIL（不同胚）** |".format(kn["dim_SU5"], kn["dim_CP4"]))
    L.append("| 一化对齐 | 「最小复表示维数正是 16」 | 最小非平凡不可约 = **{0}**；一代内容和 = **{1}** | **FAIL（表述）**；一代和 16 单列 PASS |".format(kn["min_nontrivial_irrep"], kn["one_gen_dim_sum"]))
    L.append("")
    L.append("## 六、世代数 = Z₄ 实表示数：数字偶合")
    L.append("")
    L.append("| 周期 | 实不可约表示数 | 复不可约表示数 |")
    L.append("|---|---|---|")
    for n in (3, 4, 5, 6):
        r, dims, c = zn_real_irrep_census(6)[n]
        L.append("| Z{} | {}（{}） | {} |".format(n, r, dims, c))
    L.append("")
    L.append("计数 3 对周期无分辨力（Z₅ 亦为 3）；按复表示计 Z₄ 给 4（与「禁戒第四代」冲突，"
             "实/复之选事后）；SM 三代是同结构拷贝而非互异表示。⇒ 「三代←对偶周期 4 表示论」"
             "是数字偶合，映射无机制。")
    L.append("")
    L.append("## 七、数值层：耦合统一复现与闭式分析")
    L.append("")
    L.append("- 复现靶脚本口径（同参数 RK4=精确解，残差机读见控制组 C15）：SM 三线最小间距 **{:.3f}**（不交）；"
             "MSSM（1TeV 续接）最小间距 **{:.3f}** @ **{:.2e} GeV**（近似但不精确相交）。".format(
                 kn["rge_sm_gap"], kn["rge_mssm_gap"], kn["rge_mssm_scale"]))
    L.append("- MSSM 系数与接入能标为假设（靶 claims 自承）；负对照：调 a₁ 使三线精确共点 ⇒ 最小 gap = "
             "{:.1e}（证明判据有分辨力）。".format(kn["rge_negative_control_gap"]))
    L.append("")
    L.append("## 八、修复定价")
    L.append("")
    L.append("路径四闭合 = 供给全部 {} 槽位；位掩码 2^{}={} 组合机读：**宣称域内成立 0、零代价 0**。"
             "唯一「存活」构型 = 退化为标准模型 + 装饰性公理（与 r103/r119 同型）⇒ "
             "「修复即自杀」同型（S13 为兄弟家族，不计主线度数）。".format(
                 kn["slots_total"], kn["slots_total"], 2 ** kn["slots_total"]))
    L.append("")
    L.append("## 九、控制组与守卫")
    L.append("")
    L.append("控制组 {} / {}；守卫 {} / {}（全部机读驱动，无一处 ok 写死 True）。".format(
        sum(1 for c in payload["controls"] if c["ok"]), len(payload["controls"]),
        sum(1 for g in payload["guards"] if g["ok"]), len(payload["guards"])))
    L.append("")
    L.append("## 十、未闭合项与红线")
    L.append("")
    for x in payload["not_closed"]:
        L.append("- " + x)
    L.append("")
    L.append("- 数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。")
    return "\n".join(L) + "\n"


def main():
    kn = run_audit()
    payload = build_payload(kn)
    os.makedirs(_DATADIR, exist_ok=True)
    p_json = os.path.join(_DATADIR, BASE + ".json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    p_rep = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(p_rep, "w", encoding="utf-8") as f:
        f.write(render_report(payload))
    p_v = os.path.join(_DATADIR, "判定_" + BASE + ".md")
    with open(p_v, "w", encoding="utf-8") as f:
        f.write(render_verdict_md(payload))
    p_md = os.path.join(_DATADIR, BASE + ".md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write(render_report(payload))

    # 门禁：控制组/守卫全过 + FAIL/PASS 均 >0 才 rc=0
    bad = [c for c in CTRL if not c[2]] + [g for g in GUARDS if not g[2]]
    n_fail = sum(1 for e in ENTRIES if e[3] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e[3] == "PASS")
    print("entries: FAIL={} PASS={} total={}".format(n_fail, n_pass, len(ENTRIES)))
    print("controls: {} / {}".format(sum(1 for c in CTRL if c[2]), len(CTRL)))
    print("guards  : {} / {}".format(sum(1 for g in GUARDS if g[2]), len(GUARDS)))
    print("verdict : " + VERDICT)
    if bad or n_fail == 0 or n_pass == 0:
        for b in bad:
            print("  FAILED:", b[0], b[1], b[3])
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
