# -*- coding: utf-8 -*-
"""
tuft_卷系_模态谱方向定理.py
============================
TUFT / H-TUFT 卷系·**跨卷收口分析（第 2 轮）**
  (A) 独立复核最新两卷（补充卷G=CUR-19 / 补充卷H=CUR-20）的**核心数值**（不重跑其脚本，避免覆盖
      并行会话产物；改为按其实跑公式**独立重算**）；
  (B) 攻击卷二十九 §9 认定的**唯一可能真进展的数学问题**——CUR-12 的 H2/H3
      （「三代 = 前 3 个径向/形状模态」与「只 3 代」的严格性），产出一条**新的结构定理 H**。

为何这是"唯一剩余可攻点"：
  · 20 条目已全部落盘（CUR-01~CUR-20），0 问题；
  · no-go 定理族 A~G 已覆盖**所有"拓扑/整数 → 连续量"与"破缺源"类**构造；
  · 唯一未被 A~G 覆盖的，是 CUR-12 的 **H3（模态↔代）**：它不主张"整数编码连续量"，
    而主张"**固定算符的束缚态谱**给出代层级"——这是**谱形状**问题，需独立定理。

判据：
  V0 独立复核 CUR-19/CUR-20 核心数值
  V1 sech²（Pöschl-Teller）精确束缚态计数 N(λ) 与「恰好 3」的窗口
  V2 sech² 精确谱：能隙随模序**递减**
  V3 一般有限阱（方阱/高斯阱/sech²）数值谱：能隙递减（阈值累积）
  V4 紧致内部空间 E_l ∝ l(l+1)/R²：能隙递增但**有界**（首步比 ≤ 2）
  V5 观测带电轻子层级：增量比 = 15.894（**递增**）
  V6 两参数谱族的**排除**（指数谱 / 幂律谱）
  V7 三参数 (m_top, c, p) 唯一精确拟合 ⇒ p≈7.0 ⇒ 定理 D / 卷二十九 T5
  V8 定理 H 陈述与诚实边界

红线：数学自洽 != 实验证实。本脚本**不新增物理主张**，只做**结构诊断 + 独立复核**；
本册**不占 CUR 编号**（属 `tuft_卷系_结构障碍定理族.md` 的定理 H）。

依赖：Python 3.8 + numpy（scipy 可选，本脚本用 numpy 三对角对角化）。
"""

from __future__ import print_function

import hashlib
import os
import sys
import time
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np

from scipy.linalg import eigh_tridiagonal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_卷系_模态谱方向定理_report.txt")

# ── 观测锚（PDG pole 质量，MeV）────────────────────────────────────────────
M_E = 0.510998950
M_MU = 105.6583755
M_TAU = 1776.86

# 观测「增量比」= 第 2 增量 / 第 1 增量 = (m_τ−m_μ)/(m_μ−m_e)（谱能隙须递增该倍数）
NEED_INCREMENT_RATIO = (M_TAU - M_MU) / (M_MU - M_E)

# ── 补充卷G/H 的实跑取值（用于独立复核）────────────────────────────────────
G_SIGMA_COEFF = 0.45
G_ALPHA = 0.07
G_TB_COEF = 0.12
G_OMEGA_PEAK = 1.2e-16
G_KSTAR = 0.008
H_ALPHA_S = 11.5588
H_ALPHA_2 = 3.3137
H_ALPHA_1 = 1.0

_lines = []
_CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P_(m):
    _CNT["PASS"] += 1
    _lines.append("[PASS] " + m)


def F_(m):
    _CNT["FAIL"] += 1
    _lines.append("[FAIL] " + m)


def B_(m):
    _CNT["BOUNDARY"] += 1
    _lines.append("[BOUNDARY] " + m)


def I_(m):
    _CNT["INFO"] += 1
    _lines.append("[INFO] " + m)


# ────────────────────────────────────────────────────────────────────────────
# V0 独立复核 CUR-19 / CUR-20 的核心数值
# ────────────────────────────────────────────────────────────────────────────
def v0_crosscheck():
    I_("§V0 独立复核补充卷G（CUR-19）/ 补充卷H（CUR-20）的核心数值（按其实跑公式独立重算）")

    # --- G1 手征强度与 TB 振幅（补充卷G note 声明 ΔΠ=8.334e-03、TB=1.000e-03）---
    dPi = G_SIGMA_COEFF * G_ALPHA ** 1.5
    TB = G_TB_COEF * dPi
    I_("   [G] ΔΠ = σ_coeff·α^1.5 = %.6g × %.6g^1.5 = %.6e（G 声明 8.334e-03）"
       % (G_SIGMA_COEFF, G_ALPHA, dPi))
    I_("   [G] TB = %.2f·ΔΠ = %.6e（G 声明 1.000e-03）" % (G_TB_COEF, TB))
    if abs(dPi - 8.334e-3) / 8.334e-3 < 5e-3 and abs(TB - 1.000e-3) / 1.000e-3 < 5e-3:
        P_("V0a 复核通过：CUR-19 的 ΔΠ/TB 与其声明一致（ΔΠ=%.6e、TB=%.6e）⇒ 其『输出全为自由参数』"
           "的自我判定成立（两参数 σ_coeff/α 皆自由，无动力学输入）" % (dPi, TB))
    else:
        F_("V0a CUR-19 的 ΔΠ/TB 与声明不一致（ΔΠ=%.6e、TB=%.6e）" % (dPi, TB))

    # --- G2 σ_wall 量纲复核 ---
    I_("   [G] σ_wall ∝ α/l_P²：alpha 无量纲、l_P² 量纲 L² ⇒ α/l_P² 量纲 **L^-2**")
    I_("       而面张力（域壁张力）量纲 = 能量/面积 ⇒ 自然单位 (ħ=c=1) 下 = L^-1/L² = **L^-3**")
    F_("V0b 复核确认 CUR-19 的量纲缺口：α/l_P² 为 L^-2，面张力须 L^-3 ⇒ **差 1 个能量量纲**"
       "（缺一个 M_Pl 因子）⇒ 与补充卷A 的 Ω_DM 量纲反属同类缺陷")

    # --- H1 一代 SM 反常四条件（精确分数，全左手 Weyl 约定）---
    # 场：(多重数, SU(3) 维, SU(2) 维, Y)
    # 使用共轭（全左手）约定：u_R^c: Y=-2/3；d_R^c: Y=+1/3；e_R^c: Y=+1
    gen = [
        ("Q_L", 6, Fraction(1, 6)),      # 3 色 × 2 弱 = 6 个 Weyl
        ("u_R^c", 3, Fraction(-2, 3)),
        ("d_R^c", 3, Fraction(1, 3)),
        ("L_L", 2, Fraction(-1, 2)),
        ("e_R^c", 1, Fraction(1)),
    ]
    grav = sum(Fraction(n) * Y for (_s, n, Y) in gen)
    Y3 = sum(Fraction(n) * Y ** 3 for (_s, n, Y) in gen)
    # [SU(3)]^2 U(1)：按色多重数加权（Q_L 有 2 个弱分量共享 Y_Q）
    a33 = Fraction(2) * Fraction(1, 6) + Fraction(-2, 3) + Fraction(1, 3)
    # [SU(2)]^2 U(1)：按弱双重数加权（Q_L 有 3 色）
    a22 = Fraction(3) * Fraction(1, 6) + Fraction(-1, 2)
    I_("   [H] 一代 SM（全左手 Weyl 约定，精确分数）：")
    I_("       grav-U(1)  ΣY   = %s" % (grav,))
    I_("       [U(1)]^3   ΣY³  = %s" % (Y3,))
    I_("       [SU(3)]²U(1)    = %s" % (a33,))
    I_("       [SU(2)]²U(1)    = %s" % (a22,))
    if grav == 0 and Y3 == 0 and a33 == 0 and a22 == 0:
        P_("V0c 复核通过：一代 SM 的**四个反常条件精确为 0**（Fraction 精确）⇒ CUR-20 的『反常相消是"
           "约束不是导出』成立，且其引擎实现正确（此亦为对我方独立实现的交叉校验）")
    else:
        F_("V0c 反常条件不为 0（%s/%s/%s/%s）" % (grav, Y3, a33, a22))

    # --- H2 超荷晶格（以 1/6 为单位）---
    lat = [Y * 6 for (_s, _n, Y) in gen]
    lat_s = "{" + ",".join(str(int(v)) for v in lat) + "}"
    I_("   [H] 超荷晶格（以 1/6 为单位）= %s（CUR-20 声明 {1,-4,2,-3,6}）" % lat_s)
    if lat == [Fraction(1), Fraction(-4), Fraction(2), Fraction(-3), Fraction(6)]:
        P_("V0d 复核通过：超荷晶格 = %s ⇒ **非单一缠绕模式**（取值跨 1~6，非同一整数的倍数）"
           "⇒ CUR-20 的『U(1)_Y 量子化需额外机制』成立" % lat_s)
    else:
        F_("V0d 超荷晶格与 CUR-20 声明不一致（%s）" % lat_s)

    # --- H3 耦合比值（纯数值，无拓扑来源）---
    I_("   [H] α_s:α_2:α_1(M_Z) = %.4f:%.4f:%.4f（GUT 归一化）" % (H_ALPHA_S, H_ALPHA_2, H_ALPHA_1))
    I_("       三者跑动 β≠0 ⇒ 撞定理 C（无跑动）与定理 D（重参数化）")
    I_("   [H] 本轮**不重跑** CUR-19/CUR-20 脚本（避免覆盖并行会话的报告产物）；"
       "其 script_sha256 已由 `tuft_卷系_归一化总览.py` 实跑核对为 MATCH")


# ────────────────────────────────────────────────────────────────────────────
# V1 sech² 精确束缚态计数
# ────────────────────────────────────────────────────────────────────────────
def v1_pt_count():
    I_("§V1 Pöschl-Teller（sech²）阱的**精确**束缚态计数")
    I_("   算符 L = −d²/dx² + V(x)，V(x) = −V₀·sech²(x/a)；令 λ ≡ V₀a²")
    I_("   精确解：s(s−1)=λ ⇒ s = [1+√(1+4λ)]/2；E_n = −(s−1−n)²/a²，n=0..N−1")
    I_("   ⇒ 束缚态数 **N(λ) = ceil((sqrt(1+4λ) − 1)/2)**（≈ √λ）")
    I_("   阈值：N=k  ⟺  λ ∈ (k(k−1), k(k+1)]")
    for k in range(1, 7):
        lo, hi = k * (k - 1), k * (k + 1)
        I_("      N=%-2d ⟺ λ ∈ (%4d, %4d]    窗口宽 %d（上下界之比 = %.3f）"
           % (k, lo, hi, hi - lo, (hi / float(lo)) if lo > 0 else float("inf")))
    I_("   数值核验：")
    for lam in [1.0, 2.0, 2.5, 6.0, 6.5, 12.0, 13.0]:
        N = int(np.ceil((np.sqrt(1 + 4 * lam) - 1) / 2.0))
        I_("      λ=%-6.2f ⇒ N=%d" % (lam, N))
    P_("V1 『恰好 3 个束缚态』的可达性被**量化**：须 λ = V₀a² ∈ (6, 12]，即一个**倍频程"
       "（因子 2）窗口**；λ 由 4~5 个连续参数（V₀, a, …）合成，卷系**未给任何机制**固定它落在该窗口"
       "⇒ CUR-12 的 H2（只 3 代）不是「未导出」，而是「需因子 2 的调参窗口且无固定机制」")


# ────────────────────────────────────────────────────────────────────────────
# V2 / V3 谱与能隙单调性（精确 + 数值）
# ────────────────────────────────────────────────────────────────────────────
def _tridiag_bound_states(V_of_x, L, N):
    """有限差分三对角对角化（scipy 三对角专用求解器，O(N²)）：
    返回束缚态 |E|（**按由深到浅**排序，即模序 n=0,1,2,...）。"""
    x = np.linspace(-L, L, N)
    h = x[1] - x[0]
    V = V_of_x(x)
    d = 2.0 / h ** 2 + V
    e = -1.0 / h ** 2 * np.ones(N - 1)
    w = eigh_tridiagonal(d, e, eigvals_only=True)   # 只求特征值，O(N²)
    bound_asc = np.sort(np.abs(w[w < 0.0]))
    bound = bound_asc[::-1]             # 由深到浅（模序）
    return bound, x, h


def v2_v3_spectrum():
    I_("§V2 sech² 精确谱（λ=8 ⇒ N=3）与能隙单调性")
    lam = 8.0
    a = 1.0
    V0 = lam / a ** 2
    s = (1.0 + np.sqrt(1.0 + 4.0 * lam)) / 2.0
    N = int(np.ceil(s - 1.0))
    I_("   λ=%.1f ⇒ s=%.6f, s−1=%.6f, N=%d" % (lam, s, s - 1.0, N))
    mu = np.array([(s - 1.0 - n) ** 2 / a ** 2 for n in range(N)])
    I_("   精确 |E_n| = %s" % np.array2string(mu, precision=6))
    gaps = mu[:-1] - mu[1:]
    I_("   能隙（相邻|E|差）= %s" % np.array2string(gaps, precision=6))
    if len(gaps) >= 2 and np.all(np.diff(gaps) < 0):
        P_("V2a sech² 精确谱的能隙**严格递减**（%.6f → %.6f，比 %.4f < 1）⇒ 与「递增」的观测层级方向相反"
           % (gaps[0], gaps[-1], gaps[-1] / gaps[0]))
    else:
        B_("V2a sech² 能隙单调性未通过（gaps=%s）" % gaps)

    I_("§V3 一般有限阱的**数值**谱（三对角差分 + 对角化，作为独立核验）")
    I_("   先做**自检**：对 sech²(λ=8) 的数值谱应与 V2 的精确谱一致")
    bound, x, h = _tridiag_bound_states(lambda xx: -V0 / np.cosh(xx / a) ** 2, L=40.0, N=6001)
    I_("   数值束缚态数 = %d（精确 N=%d）；数值 |E| = %s"
       % (len(bound), N, np.array2string(bound, precision=6)))
    if len(bound) == N and np.allclose(bound, mu, rtol=2e-3, atol=2e-3):
        P_("V3a 自检通过：数值三对角谱与 sech² 精确谱一致（相对误差 < 0.2%）⇒ 数值机器可信")
    else:
        B_("V3a 数值与精确谱有偏差（数值 %s vs 精确 %s），仍可用于**单调性**判据" % (bound, mu))

    I_("   其余阱型（同法）：")
    wells = [
        ("sech² (λ=8)", lambda xx: -8.0 / np.cosh(xx) ** 2),
        ("sech² (λ=30)", lambda xx: -30.0 / np.cosh(xx) ** 2),
        ("方阱 (V0=200, a=1)", lambda xx: np.where(np.abs(xx) < 1.0, -200.0, 0.0)),
        ("高斯阱 (V0=80, σ=1.5)", lambda xx: -80.0 * np.exp(-xx ** 2 / (2.0 * 1.5 ** 2))),
    ]
    well_info = []
    for name, fn in wells:
        b, _x, _h = _tridiag_bound_states(fn, L=60.0, N=12001)
        if len(b) >= 3:
            g = np.abs(np.diff(b))          # b 已按由深到浅 ⇒ g[k] 为第 k 个能隙
            tr = ("递增" if np.all(np.diff(g) > 0) else
                  ("递减" if np.all(np.diff(g) < 0) else "非单调"))
            r = float(g[1] / g[0])
            well_info.append((name, len(b), r, tr))
            I_("      %-22s N=%-2d 首增量比=%.4f（%s）  能隙(前4)=%s"
               % (name, len(b), r, tr, np.array2string(g[:4], precision=4)))
        else:
            I_("      %-22s N=%d（束缚态过少，跳过）" % (name, len(b)))
    rmax = max(x[2] for x in well_info)
    F_("V3b **CUR-12 的 H3（模态↔代）机制被排除——两分支均不足**：4 种阱型的首增量比 = %s"
       "（最大 %.4f）而观测需 **%.4f** ⇒ 相差 ≥ %.1f 倍。规律分两支：**浅阱/阈值累积 ⇒ 递减**"
       "（sech²(8)=0.466、sech²(30)=0.778、高斯=0.957）；**深阱/紧致几何 ⇒ 递增但有界**"
       "（方阱(200)=1.663、紧致空间首步=2.000）⇒ 标准几何的增量比恒 ≲ 3，无法企及 %.3f"
       "（须谱指数 p≈6.8，见 V6/V7）"
       % (", ".join("%s=%.3f" % (x[0].split()[0], x[2]) for x in well_info), rmax,
          NEED_INCREMENT_RATIO, NEED_INCREMENT_RATIO / rmax, NEED_INCREMENT_RATIO))


# ────────────────────────────────────────────────────────────────────────────
# V4 紧致内部空间
# ────────────────────────────────────────────────────────────────────────────
def v4_compact():
    I_("§V4 紧致内部空间（唯一有希望给「递增能隙」的标准几何）")
    I_("   球面/紧致流形上的 Laplacian：E_l = l(l+1)/R²（l=0,1,2,...）")
    E = np.array([l * (l + 1.0) for l in range(0, 8)])
    gaps = np.diff(E)
    ratios = gaps[1:] / gaps[:-1]
    I_("   E_l = %s（单位 1/R²）" % np.array2string(E, precision=1))
    I_("   能隙 = %s" % np.array2string(gaps, precision=1))
    I_("   相邻能隙之比 = %s（首步 = %.4f）" % (np.array2string(ratios, precision=4), ratios[0]))
    I_("   一般 E_n = A(n+α)^p 的能隙比 = [(2+α)^p−... ；α=0、p=2 时首步比 = 3；p=2 ⇒ 递减趋 1")
    F_("V4 紧致内部空间属「递增但有界」支：E∝l(l+1) 的首步比 = %.4f，随后递减趋 1 ⇒ 最大 ≲ 2，"
       "**远不能达到观测所需的 %.3f**（差 %.1f 倍）⇒ 该类几何亦被排除"
       % (ratios[0], NEED_INCREMENT_RATIO, NEED_INCREMENT_RATIO / ratios[0]))


# ────────────────────────────────────────────────────────────────────────────
# V5 观测层级
# ────────────────────────────────────────────────────────────────────────────
def v5_observed():
    I_("§V5 观测带电轻子层级（PDG pole 质量，单位 MeV）")
    r12 = M_MU / M_E
    r23 = M_TAU / M_MU
    r13 = M_TAU / M_E
    inc1 = M_MU - M_E
    inc2 = M_TAU - M_MU
    inc_ratio = inc2 / inc1
    I_("   m_e=%.6f  m_μ=%.6f  m_τ=%.3f" % (M_E, M_MU, M_TAU))
    I_("   r12 = m_μ/m_e = %.4f ；r23 = m_τ/m_μ = %.4f ；r13 = m_τ/m_e = %.4f" % (r12, r23, r13))
    I_("   增量（以 m_e 为单位）：第1增量 = %.4f ；第2增量 = %.4f" % (inc1 / M_E, inc2 / M_E))
    I_("   **增量比 = 第2增量/第1增量 = %.4f（> 1 ⇒ 递增层级）**" % inc_ratio)
    P_("V5 观测层级的**方向**被量化：增量比 = %.4f ⇒ 谱的能隙必须**递增 15.9 倍**。"
       "这是对被检验机制的一条**强方向约束**（此前卷系只比较过比值 r，未使用「增量比」这一判据）" % inc_ratio)
    return r12, r23, r13, inc_ratio


# ────────────────────────────────────────────────────────────────────────────
# V6 两参数谱族的排除
# ────────────────────────────────────────────────────────────────────────────
def v6_two_param(r12, r23, inc_ratio):
    I_("§V6 两参数谱族的**双约束排除**（用 r12 与 r23 两个独立观测值）")
    # (a) 纯指数谱 m_n ∝ e^{a n}
    a_exp = np.log(r12)
    pred_r23_exp = np.exp(a_exp)
    I_("   (a) 指数谱 m_n ∝ e^{a n}：由 r12 定 a=ln(%.4f)=%.6f" % (r12, a_exp))
    I_("       预测 r23 = e^a = %.4f ；实测 r23 = %.4f ⇒ 偏差 %.4f 倍" % (pred_r23_exp, r23,
                                                                     pred_r23_exp / r23))
    F_("V6a 指数谱被排除：预测 r23=%.3f vs 实测 %.3f ⇒ 差 **%.2f×**" % (pred_r23_exp, r23,
                                                                     pred_r23_exp / r23))
    # (b) 纯幂律谱 m_n ∝ (n+1)^p
    p_from_r12 = np.log(r12) / np.log(2.0)
    pred_r23_pl = 1.5 ** p_from_r12
    I_("   (b) 幂律谱 m_n ∝ (n+1)^p：由 r12 = 2^p ⇒ p = %.6f" % p_from_r12)
    I_("       预测 r23 = 1.5^p = %.4f ；实测 %.4f ⇒ 偏差 %.4f 倍" % (pred_r23_pl, r23,
                                                                pred_r23_pl / r23))
    F_("V6b 幂律谱（由 r12 定参）被排除：预测 r23=%.3f vs 实测 %.3f ⇒ 差 **%.2f×**"
       % (pred_r23_pl, r23, pred_r23_pl / r23))
    # 交叉：由增量比反解 p，看与 r12 是否相容
    # 幂律 (n+1)^p 的增量比 = (3^p−2^p)/(2^p−1) —— 单调递增，可反解
    ps = np.linspace(0.01, 30.0, 300000)
    vals = (3.0 ** ps - 2.0 ** ps) / (2.0 ** ps - 1.0)
    idx = int(np.argmin(np.abs(vals - inc_ratio)))
    p_from_inc = ps[idx]
    pred_r12 = 2.0 ** p_from_inc
    I_("   (c) 交叉检验：由增量比 %.4f 反解 p = %.6f ⇒ 预测 r12 = 2^p = %.4f（实测 %.4f）"
       % (inc_ratio, p_from_inc, pred_r12, r12))
    F_("V6c **两约束不相容**：r12 给 p=%.4f，增量比给 p=%.4f（相差 %.1f%%），由 p_from_inc 预测 "
       "r12 偏 %.1f%% ⇒ 单一**两参数**幂律谱同时拟合 r12 与增量比**不可能**。"
       "（注：本处的 p_from_inc 与 V7 的 p* 由同一代数恒等式 (1−A)/A 决定，故必然相等——"
       "V6c 只用于**排除两参数版**，与 V7 的『三参数精确拟合』不是两个独立检验）" %
       (p_from_r12, p_from_inc, abs(p_from_r12 - p_from_inc) / p_from_r12 * 100.0,
        abs(pred_r12 - r12) / r12 * 100.0))
    return p_from_r12, p_from_inc


# ────────────────────────────────────────────────────────────────────────────
# V7 三参数族的唯一精确拟合
# ────────────────────────────────────────────────────────────────────────────
def v7_three_param():
    I_("§V7 三参数族 m_n = m_top + c·(n+1)^p 的拟合性质")
    # 由第 1、2 点消去 (m_top, c)，第 3 点给出 p 的方程：
    #   (m1-m0)/(2^p-1) = (m2-m0)/(3^p-1)
    target = (M_MU - M_E) / (M_TAU - M_E)
    I_("   消去 (m_top,c) 后须满足：(m_μ−m_e)/(m_τ−m_e) = (2^p−1)/(3^p−1)")
    I_("   左端 = %.8f" % target)
    ps = np.linspace(0.01, 40.0, 400000)
    vals = (2.0 ** ps - 1.0) / (3.0 ** ps - 1.0)
    idx = int(np.argmin(np.abs(vals - target)))
    p_star = ps[idx]
    c_star = (M_MU - M_E) / (2.0 ** p_star - 1.0)
    mtop_star = M_E - c_star
    I_("   唯一解：p* = %.6f ⇒ c* = %.6f MeV ；m_top* = %.6f MeV" % (p_star, c_star, mtop_star))
    chk = np.array([mtop_star + c_star * ((n + 1) ** p_star) for n in range(3)])
    I_("   回代检验：m = %s（实测 %s）" % (np.array2string(chk, precision=6),
                                    np.array2string(np.array([M_E, M_MU, M_TAU]), precision=6)))
    err = float(np.max(np.abs(chk - np.array([M_E, M_MU, M_TAU])) / np.array([M_E, M_MU, M_TAU])))
    I_("   最大相对误差 = %.3e" % err)
    F_("V7 **三数据点 = 三参数 ⇒ 精确拟合、零预言力**（定理 D / 卷二十九 T5 的实例化）："
       "p*≈%.2f、c*≈%.2f MeV、m_top*≈%.2f MeV 全部由数据反解；且 p*≈%.2f **不是任何标准几何的指数**"
       "（紧致内部空间 E∝l(l+1) ⇒ p=2；幂律拟合 r12 要求 p=%.2f）⇒ 该拟合无独立约束"
       % (p_star, c_star, mtop_star, p_star, np.log(M_MU / M_E) / np.log(2.0)))
    return p_star


# ────────────────────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    _lines.append("=" * 76)
    _lines.append("TUFT / H-TUFT 卷系·跨卷收口分析（第 2 轮）：模态谱方向定理（定理 H）")
    _lines.append("=" * 76)
    I_("背景：CUR-01~CUR-20 已全部落盘（20 条目 / 0 问题）；no-go 定理族已至 A~G（含定理 F/G）。")
    I_("本册攻击 A~G **未覆盖**的唯一一点：CUR-12 的 H3（「模态↔代」）——它不主张「整数编码连续量」，"
       "而主张「固定算符的束缚态谱给出代层级」，属**谱形状**问题，需独立判据。")

    v0_crosscheck()
    v1_pt_count()
    v2_v3_spectrum()
    v4_compact()
    r12, r23, r13, inc_ratio = v5_observed()
    p12, pinc = v6_two_param(r12, r23, inc_ratio)
    p_star = v7_three_param()

    I_("§结论摘要")
    I_("   ① 独立复核：CUR-19 的 ΔΠ/TB 与声明一致、σ_wall 量纲缺口 L^-2 vs L^-3 确认；"
       "CUR-20 的反常四条件精确为 0、超荷晶格 {1,−4,2,−3,6} 确认。")
    I_("   ② 【定理 H·新】标准几何的束缚态谱**增量比有界**：浅阱/阈值累积 ⇒ 递减（<1）；"
       "深阱/紧致几何 ⇒ 递增但 ≲ 3。观测增量比 = %.4f ⇒ 相差约 **8~10 倍**（视分支）"
       "⇒ 「三代 = 前 3 个模态」机制**两分支均不能企及**。" % inc_ratio)
    I_("   ③ 紧致内部空间 E∝l(l+1)/R² 属「递增但有界」支（首步比 = 2.000），远不能达 %.3f"
       "⇒ 亦被排除。" % inc_ratio)
    I_("   ④ 两参数谱族被双约束排除：指数谱 off %.2f×；幂律谱 off %.2f×；由 r12 与增量比反解的 p"
       "**不相容**（%.4f vs %.4f）。" % ((np.exp(np.log(r12)) / r23), (1.5 ** p12) / r23, p12, pinc))
    I_("   ⑤ 三参数 (m_top, c, p) 精确拟合（p*≈%.2f）⇒ 零预言力（定理 D 实例化）。" % p_star)
    I_("   ⑥ 「只 3 代」被量化：sech² 给出「恰好 3」⟺ λ=V₀a²∈(6,12]（**因子 2 的窗口**），"
       "而无任何机制固定 λ 落入该窗口。")

    B_("边界①：定理 H 针对**固定算符的束缚态谱**（1D 形状模 / 紧致内部空间）；"
       "**论证强度 = 计算级 + 一般论证**（4 种阱型解析/数值覆盖 + 两条一般论证：阈值累积 ⇒ 靠上能隙趋 0；"
       "深阱 ⇒ 趋于粒子在盒 ⇒ 比值 →1）——**不是**对所有阱型的严格定理。"
       "不排除「指数型谱」类机制——但那需要**新自由度**（标度不变性/维度嬗变），且其两参数版已被 V6a 排除。")
    B_("边界②：不排除「三代不是同一孤子的前 3 个模，而是三类不同孤子」——但那就退化为"
       "O-KNOTMAP 的字典赋值，回到定理 D。")
    B_("边界③：V3 数值用有限差分 + 三对角对角化（N=6001/12001，L=40~60）；"
       "已用 sech² 精确谱做**自检**（相对误差 < 0.2%）后才用于单调性判据。")
    B_("边界④：观测质量取 PDG pole 值（MeV）；用 pole 还是 MS-bar 不改变方向性结论（增量比 15.9 ≫ 1）。")
    B_("边界⑤：本册**不占 CUR 编号**（属 `tuft_卷系_结构障碍定理族.md` 的定理 H）；"
       "不改动任何 CURATED 真源状态。")
    B_("边界⑥：红线——数学自洽 != 实验证实。定理 H 是**结构诊断**，不构成对 H-TUFT 的经验支持，"
       "也不构成对带电轻子质量起源的解答。")

    _lines.append("-" * 76)
    _lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d"
                  % (_CNT["PASS"], _CNT["FAIL"], _CNT["BOUNDARY"], _CNT["INFO"]))
    _lines.append("-" * 76)
    _lines.append("评级：O/L2（结构诊断册；新增定理 H（模态谱方向），并独立复核 CUR-19/CUR-20 核心数值）")
    _lines.append("红线：数学自洽 != 实验证实；本册为结构诊断，不新增物理主张、不改动 CURATED 真源。")

    text = "\n".join(_lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    with open(os.path.abspath(__file__), "rb") as fh:
        self_sha = hashlib.sha256(fh.read()).hexdigest()
    text2 = text + "自哈希(SHA256) = %s\n耗时 = %.1fs\n" % (self_sha, time.time() - t0)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text2)
    print(text2)
    return _CNT


if __name__ == "__main__":
    main()
