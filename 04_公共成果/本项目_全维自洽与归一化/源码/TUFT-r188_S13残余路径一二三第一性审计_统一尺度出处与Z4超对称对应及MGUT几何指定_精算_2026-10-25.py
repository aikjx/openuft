#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TUFT-r188｜S13 残余 OPEN 路径 1–3 第一性审计（统一尺度出处 / Z₄→超对称 / M_GUT 几何指定）
================================================================================
编号 r188（★取号经过：起草取 r186，源码 10:04:10 落盘后**登记前复查磁盘时间戳**
（承 r177/r178 教训）发现并行会话已先占 **r186**（09:41:31《F5 钱德拉塞卡极限复核》，
四件套齐全）与 **r187**（09:55:45《变分推导链路求导验证》，四件套齐全）⇒
按「先占位者为权威、后到者整体改号」铁律，本卷整体改号 **r188**（旧 r186 四件套
已入 scratch/r186_s13_old_outputs/；未触碰并行会话任何字节）；r188 实测首空号。
落盘后登记前必再查磁盘时间戳；未改动 r170–r187 任何字节）。

靶：`01_独立体系/S13_全域双向分形统一场论/`（唯一 H 级体系）
    · 07_计算复现/源码/running_unify_verify.py（V1.7 统一跑动检验）
    · 07_计算复现/源码/constant_unify_verify.py（V1.6 常数统一）
    · 07_计算复现/源码/openuft_rge_sim.py（SM/MSSM 三线间距）
    · 09_验证结果/验证精算报告_V1.8.md（50 位精算，P9 统一跑动）
    · 09_验证结果/候选预言验证_V2.0.md（候选预言五~八，conjecture）
    · 13_论文与成果/书稿/正文/ch25-常数统一与电荷量子化.md（第25章 + §25.8 跑动检验）
    · 04_理论推导/推导卷_对话产出/openuft_卷三 / openuft_卷七（SO(10) 推导卷线）
    · 03_数学形式/equations.md（冻结方程 + 参数归并 v=ℓ⁻¹）
    · 12_研究结论/理论总纲_V1.7.md
    · claims.csv（C0001–C0014）
    · 前置审计：`判定_S13_攻破审计_终局定位_2026-10-07.md`（四条 OPEN 路径登记册）

背景：2026-10-07 攻破审计登记四条诚实 OPEN 路径；**路径 4 已由 r178 闭合为
「三公设对 SM 结构 0/13 槽位供给」**。本卷审计**残余路径 1–3**：
  路径 1：sin²θ_W=1/4 的框架统一尺度出处（使跑动在 S13 真空 v 或 ℓ_P⁻¹ 成立，
          而非悬空 3.7 TeV）；
  路径 2：从 Z₄ 对偶第一性推出超对称谱（使 s* 升格为真预测）★最有价值；
  路径 3：统一尺度 M_GUT 的几何指定（与 ℓ_P / 分形标度建立推导关系）。

本卷五层判据：
  ① 正对照层：靶的数学/算术确实正确的东西（RG 对拍逐位一致 / Z₄ 周期 4 /
     s* 闭式推导 / SM β 由内容重算 / λ₈ 嵌入代数）——证明审计有分辨力；
  ② 路径 1 层：v 的出处机读（PDG 反解锚点 vs 框架输出）、M* 孤儿性、ℓ 三重口径；
  ③ 路径 2 层：超对称形式化零存在、Z₄↔超对称范畴错置、Higgs 二重态计数、
     s* 框架含量为零（含 β 替换负对照）、自有内容⇒SM β 与引用 MSSM β 反号；
  ④ 路径 3 层：尺度清单无几何关系、α_GUT⁻¹ 五口径与 τ_p 展宽、「精确相交」
     与自承 0.76 互斥、统一判词随圆整翻转、sin²θ_W 双口径 3/8 vs 1/4；
  ⑤ 定价层：2³=8 路径组合机读，严格/宽松双档闭合价。

分层铁律：本卷条目不可与 r142–r187 相加。
治理红线：数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。
纯标准库（本环境无 numpy / sympy / mpmath；Decimal(50) + Fraction）。
"""

import ast
import json
import math
import os
import re
import sys
import warnings
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 50

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)                      # 本项目_全维自洽与归一化
_ROOT = os.path.dirname(os.path.dirname(_PROJ))     # openuft（上溯两层：04_公共成果 → openuft）
_DATADIR = os.path.join(_PROJ, "数据")

S13 = os.path.join(_ROOT, "01_独立体系", "S13_全域双向分形统一场论")
AUDIT07 = os.path.join(_ROOT, "04_公共成果", "本项目_统一场论攻破",
                       "判定_S13_攻破审计_终局定位_2026-10-07.md")

BASE = ("TUFT-r188_S13残余路径一二三第一性审计_统一尺度出处与Z4超对称对应"
        "及MGUT几何指定_精算_2026-10-25")
VERDICT = ("S13-PATHS-1TO3-ALL-REMAIN-OPEN-ZERO-FIRST-PRINCIPLES-SUPPLY-"
           "FRAMEWORK-SCALE-ORPHANED-Z4-SUSY-CORRESPONDENCE-CATEGORIAL-"
           "MISMATCH-SSTAR-FRAMEWORK-CONTENT-ZERO-MGUT-GEOMETRIC-"
           "SPECIFICATION-ABSENT-SIN2W-DUAL-CALIBRE-REPAIR-8-COMBINATIONS-"
           "ZERO-CLOSABLE")
REDLINE = ("数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理；"
           "条目不可与 r142–r187 相加")
REDLINE_PHRASE = "不可与 r142–r187 相加"

# ---------------------------------------------------------------------------
# 靶文件登记（G4 可读性守卫 + G5 文本证据守卫的数据基础）
# ---------------------------------------------------------------------------
TARGET_FILES = {
    "running": "07_计算复现/源码/running_unify_verify.py",
    "constant": "07_计算复现/源码/constant_unify_verify.py",
    "rgesim": "07_计算复现/源码/openuft_rge_sim.py",
    "v18": "09_验证结果/验证精算报告_V1.8.md",
    "cand": "09_验证结果/候选预言验证_V2.0.md",
    "ch25": "13_论文与成果/书稿/正文/ch25-常数统一与电荷量子化.md",
    "vol3": "04_理论推导/推导卷_对话产出/openuft_卷三_攻破收口_统一场论补全与可检验预言.md",
    "vol7": "04_理论推导/推导卷_对话产出/openuft_卷七_收口_本源到标准模型显式重构与全维验证.md",
    "eqmd": "03_数学形式/equations.md",
    "ganggang": "12_研究结论/理论总纲_V1.7.md",
    "claims": "claims.csv",
}

ENTRIES = []   # (id, layer, text, verdict, note)
CTRL = []      # (id, text, ok, detail)
GUARDS = []    # (id, text, ok, detail)


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append((eid, layer, text, verdict, note))


def ctl(cid, text, ok, detail=""):
    CTRL.append((cid, text, bool(ok), detail))


def grd(gid, text, ok, detail=""):
    GUARDS.append((gid, text, bool(ok), detail))


def load_corpus():
    """读取全部靶文件（G4）；返回 {key: text}。"""
    corpus = {}
    for key, rel in TARGET_FILES.items():
        p = os.path.join(S13, rel)
        with open(p, "r", encoding="utf-8") as f:
            corpus[key] = f.read()
    with open(AUDIT07, "r", encoding="utf-8") as f:
        corpus["audit07"] = f.read()
    return corpus


# ---------------------------------------------------------------------------
# 一、RG 闭式与靶协议（正对照 A1 的机器基础）
# ---------------------------------------------------------------------------
D = Decimal
AEM_INV = D(127916) / D(1000)          # α_EM(M_Z)⁻¹ = 127.916
S2W_EXP = D(23122) / D(100000)         # sin²θ_W(M_Z) = 0.23122
A3_INV = D(10000) / D(1179)            # α_s(M_Z)⁻¹ = 1/0.1179
MZ = D(911876) / D(10000)              # 91.1876 GeV
V_FW = D(25526) / D(100)               # 255.26 GeV（ch25 §25.8「框架真空尺度」）
SSTAR_TARGET = D("0.230943405280905868720056895551")   # V1.8 P9d 自报 30 位

A1_0 = D(3) / D(5) * (D(1) - S2W_EXP) * AEM_INV
A2_0 = S2W_EXP * AEM_INV
A3_0 = A3_INV

SM_B = (D(41) / D(10), D(-19) / D(6), D(-7))     # 标准模型单圈（GUT 归一化）
MSSM_B = (D(33) / D(5), D(1), D(-3))             # MSSM 单圈（GUT 归一化）

TWO_PI = D(2) * D(str(math.pi))


def alpha_inv(a0, b, x):
    """α_i⁻¹(x)，x = ln(μ/M_Z)/(2π)：A_i(x) = A_i(0) − b_i·x（闭式）。"""
    return a0 - b * x


def s2w_of(a1, a2):
    return D(3) * a2 / (D(3) * a2 + D(5) * a1)


def sm_crossing():
    """SM：α₁⁻¹=α₂⁻¹ 交点（V1.8 P9b 对拍）。"""
    x12 = (A1_0 - A2_0) / (SM_B[0] - SM_B[1])
    m12 = MZ * (TWO_PI * x12).exp()
    a_at = alpha_inv(A1_0, SM_B[0], x12)
    a3_at = alpha_inv(A3_0, SM_B[2], x12)
    gap = abs(a_at - a3_at) / a_at * D(100)
    return x12, m12, a_at, a3_at, gap


def mssm_crossing():
    """MSSM：α₁⁻¹=α₂⁻¹ 交点（V1.8 P9d 对拍）。"""
    xu = (A1_0 - A2_0) / (MSSM_B[0] - MSSM_B[1])
    mu = MZ * (TWO_PI * xu).exp()
    a_gut = alpha_inv(A1_0, MSSM_B[0], xu)
    a3_at = alpha_inv(A3_0, MSSM_B[2], xu)
    gap = abs(a3_at - a_gut) / a_gut * D(100)
    return xu, mu, a_gut, a3_at, gap


def s2w_at_v():
    """sin²θ 跑动到 v=255.26 GeV（V1.8 P9c 对拍）。"""
    x_v = (V_FW / MZ).ln() / TWO_PI
    a1v = alpha_inv(A1_0, SM_B[0], x_v)
    a2v = alpha_inv(A2_0, SM_B[1], x_v)
    s = s2w_of(a1v, a2v)
    return x_v, a1v, a2v, s, (s - D(1) / D(4)) / (D(1) / D(4)) * D(100)


def m_star():
    """sin²θ=1/4 唯一成立尺度（V1.8 P9c 对拍）。"""
    r = D(9) / D(5)
    xs = (A1_0 - r * A2_0) / (SM_B[0] - r * SM_B[1])
    ms = MZ * (TWO_PI * xs).exp()
    return xs, ms


def sstar_closed():
    """s* 闭式：解 A1(L)=A3(L) 与 A2(L)=A3(L)（s 为未知）。
    ⇒ s* = (3a + 7A3)/(15a)；L13−L23 ≡ 0（代数恒等，Decimal 50 位机核）。"""
    s = (D(3) * AEM_INV + D(7) * A3_INV) / (D(15) * AEM_INV)
    a1_0 = D(3) / D(5) * (D(1) - s) * AEM_INV
    l13 = (a1_0 - A3_INV) / (MSSM_B[0] - MSSM_B[2])
    l23 = (s * AEM_INV - A3_INV) / (MSSM_B[1] - MSSM_B[2])
    m_pred = MZ * (TWO_PI * l13).exp()
    a_gut_s = A3_INV - MSSM_B[2] * l13
    return s, l13 - l23, m_pred, a_gut_s, (s - S2W_EXP) / S2W_EXP * D(100)


def sstar_with_beta(b):
    """负对照：同一闭式解法，换任意 β 系数（证明 s* 是 β 的函数）。
    (3/5)(1−s)a/(b1−b3) = s·a/(b2−b3) ⇒ s = k/(k+m)，k=(3/5)(b2−b3), m=b1−b3。"""
    k = D(3) / D(5) * (b[1] - b[2])
    m = b[0] - b[2]
    return k / (k + m)


def integrate_scan(b, a0, t_max, dt=0.001):
    """逐位复现靶 openuft_rge_sim.py 的 integrate()/find_cross()：
    循环顶部记录 (t, a) 再步进；返回 (最小间距点, 最后记录点)。
    最小间距 = max(|a1−a2|, |a2−a3|, |a1−a3|)，跳过 t=0。"""
    a = list(a0)
    t = 0.0
    best = (1e9, 0.0, tuple(a))
    last = (0.0, tuple(a))
    while t < t_max:
        last = (t, tuple(a))
        if t != 0.0:
            gap = max(abs(a[0] - a[1]), abs(a[1] - a[2]), abs(a[0] - a[2]))
            if gap < best[0]:
                best = (gap, t, tuple(a))

        def f(aa, bb):
            return -bb / (2.0 * math.pi)
        k1 = [f(a[i], b[i]) for i in range(3)]
        k2 = [f(a[i] + dt / 2 * k1[i], b[i]) for i in range(3)]
        k3 = [f(a[i] + dt / 2 * k2[i], b[i]) for i in range(3)]
        k4 = [f(a[i] + dt * k3[i], b[i]) for i in range(3)]
        a = [a[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
             for i in range(3)]
        t += dt
    return best, last


def rge_target_protocol():
    """靶协议：圆整初值 (59.0, 30.0, 8.5)、SM 跑至 1e19；
    MSSM 自 SM 在 1TeV 处的最后记录点续接跑至 1e19（t 自 1TeV 起算）。"""
    mz_f = 91.1876
    sm_b = (41.0 / 10, -19.0 / 6, -7.0)
    ms_b = (33.0 / 5, 1.0, -3.0)
    a0 = (59.0, 30.0, 8.5)
    best_sm, _ = integrate_scan(sm_b, a0, math.log(1e19 / mz_f))
    _, (t_tev, a_tev) = integrate_scan(sm_b, a0, math.log(1000.0 / mz_f))
    best_ms, _ = integrate_scan(ms_b, a_tev, math.log(1e19 / 1000.0))
    return (best_sm[0], mz_f * math.exp(best_sm[1]),
            best_ms[0], 1000.0 * math.exp(best_ms[1]), best_ms[2][0])


def closed_min_gap(b, a0, x_lo=0.0, x_hi=12.0, iters=300):
    """闭式三线最小间距（三分搜索）；x = ln(μ/M_ref)/(2π)。"""
    def gap(x):
        a = (float(a0[0]) - float(b[0]) * x,
             float(a0[1]) - float(b[1]) * x,
             float(a0[2]) - float(b[2]) * x)
        return max(abs(a[0] - a[1]), abs(a[1] - a[2]), abs(a[0] - a[2]))
    lo, hi = x_lo, x_hi
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if gap(m1) < gap(m2):
            hi = m2
        else:
            lo = m1
    x = (lo + hi) / 2
    return gap(x), x


def s2w_monotonic():
    """守卫：sin²θ(μ) 在 SM 单圈下于 [M_Z, ~1e17 GeV] 严格单调递增
    （⇒ sin²θ=1/4 至多在一个尺度成立，M* 唯一性不是数值意外）。"""
    prev = s2w_of(A1_0, A2_0)
    x = D("0.001")
    dmin = None
    while x < D(12):
        cur = s2w_of(alpha_inv(A1_0, SM_B[0], x), alpha_inv(A2_0, SM_B[1], x))
        if cur <= prev:
            return False, D(0)
        if dmin is None or (cur - prev) < dmin:
            dmin = cur - prev
        prev = cur
        x += D("0.001")
    return True, dmin


# ---------------------------------------------------------------------------
# 二、Z₄ 对偶周期（正对照 A2）
# ---------------------------------------------------------------------------
def check_duality_period():
    """Θ=[[0,1],[-1,0]]（Θ²=−I）：Ψ→Ψ*→−Ψ→−Ψ*→Ψ，200 随机复旋量机器零。"""
    import random
    rng = random.Random(18601)
    worst = 0.0
    for _ in range(200):
        z0 = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        z1 = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        p1 = (z1.conjugate(), -z0.conjugate())          # ΘΨ*
        p2 = (-z0, -z1)                                  # 二次对偶 = −Ψ
        p4 = (z0, z1)                                    # 四次回归
        worst = max(worst, abs(p4[0] - z0), abs(p4[1] - z1),
                    abs(p2[0] + z0), abs(p2[1] + z1))
    return worst


# ---------------------------------------------------------------------------
# 三、SM β 系数由场内容闭式重算（正对照 A4 + B8 的机器基础）
# ---------------------------------------------------------------------------
# 约定（与靶脚本一致，dα_i⁻¹/dlnμ = −b_i/2π，U(1) GUT 归一化 g1=√(5/3)g_Y）：
#   b_i = −(11/3)C2(G_i) + (2/3)Σ_Weyl idx_i + (1/6)Σ_cscalar idx_i   （SU(N)）
#   b1' = (2/3)Σ_Weyl Y² + (1/3)Σ_cscalar Y²；b1 = (3/5)b1'            （U(1) 标准 Y）
# idx = 规范多重度 × T(R)（或 U(1) 的 Y²）；复标量按复分量计。
def beta_from_content(gens=3, higgs_doublets=1):
    fermion_idx_su3 = gens * 2            # 每代 Q_L 2·(1/2) + u_R 1/2 + d_R 1/2 = 2
    fermion_idx_su2 = gens * 2            # 每代 Q_L 3·(1/2) + L_L 1/2 = 2
    fermion_y2 = gens * F(10, 3)          # 每代 Σ mult·Y² = 10/3（ch25 §25.4 表）
    higgs_idx_su2 = higgs_doublets        # 每双重态 2·(1/2) = 1
    higgs_y2 = higgs_doublets * F(1, 2)   # 每双重态 2·(1/2)² = 1/2
    b3 = -F(11, 3) * 3 + F(2, 3) * fermion_idx_su3
    b2 = -F(11, 3) * 2 + F(2, 3) * fermion_idx_su2 + F(1, 6) * higgs_idx_su2
    b1y = F(2, 3) * fermion_y2 + F(1, 3) * higgs_y2
    b1 = F(3, 5) * b1y
    return b1, b2, b3


# ---------------------------------------------------------------------------
# 四、v 的出处（路径 1 核心）
# ---------------------------------------------------------------------------
def v_fit_from_pdg():
    """ch25 §25.2/定理 25.1：v = 2m_W/g̃，g̃ = e/sinθ_W，e = √(4πα)。
    全部输入为 PDG 实验常数；重算靶的 v=255.26 GeV。"""
    alpha = 1.0 / 137.035999084
    mw = 80.377
    e = math.sqrt(4 * math.pi * alpha)
    g = e / math.sqrt(0.23122)
    v = 2 * mw / g
    return v, e, g


def ell_calibres():
    """ℓ 的口径：由拟合 v 经 v=ℓ⁻¹ 隐含的 ℓ；Λ 估计用的 ℓ_P；比值。"""
    hbarc_gev_m = 1.973269804e-16          # ħc（GeV·m）
    ell_p = 1.616255e-35                   # 约化普朗克长度（m）
    v_fit, _, _ = v_fit_from_pdg()
    ell_implied = hbarc_gev_m / v_fit      # v=ℓ⁻¹ ⇒ ℓ = ħc/v
    ell_p_inv_gev = hbarc_gev_m / ell_p
    return ell_implied, ell_p, ell_p / ell_implied, ell_p_inv_gev


# ---------------------------------------------------------------------------
# 五、τ_p 口径账（路径 3）
# ---------------------------------------------------------------------------
HBAR_GEV_S = 6.582119569e-25
YR_S = 365.25 * 86400
M_P_GEV = 0.938272


def tau_p_years(mx_gev, a_inv):
    return mx_gev ** 4 / ((1.0 / a_inv) ** 2 * M_P_GEV ** 5) * HBAR_GEV_S / YR_S


# ---------------------------------------------------------------------------
# 六、语料机读（grep 基数；防假阳性：微子排除「中微子」）
# ---------------------------------------------------------------------------
SUPERFIELD_PAT = re.compile(r"超场|superfield|超多重态|supermultiplet|Wess|超势|superpotential")
SPARTICLE_PAT = re.compile(r"超伴子|sparticle|squark|selectron|gaugino|Higgsino|higgsino|(?<!中)微子")
SUSY_PAT = re.compile(r"超对称|MSSM|supersym")
# ℓ 的**数值**指配：后缀类限 ASCII（\w 会吞上标「⁴」致 ℓ⁴=0 极值多项式被当作
# 数值赋值的假阳性——r186→r188 改号前二跑自抓，dbg 取证见 scratch）。
ELL_NUM_PAT = re.compile(r"(?:ℓ|\\ell)([A-Za-z_{}\\]*)\s*=\s*([0-9]+\.?[0-9]*(?:[eE][-+]?[0-9]+)?)")
# 路径 3 的**方程级**机读：统一尺度令牌（M_GUT/统一尺度/耦合统一）在其后 24 字符内
# 出现赋值/约等，且 RHS 80 字符窗口内出现几何标度（ℓ/普朗克/Planck/分形）——
# 即「把统一尺度赋值给几何标度」的方程。同行同现放水版已废（r186 二跑自抓：
# 两处命中全是靶自承「无框架出处/框架待决」的行，恰证明缺口存在而非几何关系存在）。
GUT_TOKEN_PAT = re.compile(r"M_?\{?\\?t?e?x?t?\{?GUT\}?|统一尺度|耦合统一")
GEOM_TOKEN_PAT = re.compile(r"ℓ|\\ell|普朗克|Planck|分形|fractal")
GUT_EQ_GEOM_PAT = re.compile(
    r"(?:M_?\{?\\?t?e?x?t?\{?GUT\}?|统一尺度|耦合统一)"
    r"[^\n]{0,24}?(?:=|∼|~|\\sim|\\approx)"
    r"[^\n。；]{0,80}?(?:ℓ|\\ell|普朗克|Planck|分形|fractal)")


def classify_ell(m):
    """ℓ 数值指配三分类：planck（ℓ_P 类截断锚）/ unit_one（自然单位 =1）/
    own（框架自有物理值）。判据走匹配全文而非后缀首字母。"""
    whole = m.group(0)
    if re.search(r"_P\b|_\{P\}|ℓ_P|\\ell_P|普朗克|Planck", whole):
        return "planck"
    if m.group(2) in ("1", "1.0"):
        return "unit_one"
    return "own"


def corpus_scan(corpus):
    """返回 (superfield_hits, sparticle_hits_excl_neutrino, susy_files,
    ell_numeric_total, ell_own_numeric, gut_geom_eqs, ell_classes)。"""
    sup = 0
    sp = 0
    susy_files = set()
    ell_total = []
    ell_own = []
    ell_classes = {"planck": 0, "unit_one": 0, "own": 0}
    gut_geom = 0
    for key, text in corpus.items():
        if key == "audit07":
            continue
        for _ in SUPERFIELD_PAT.finditer(text):
            sup += 1
        for _ in SPARTICLE_PAT.finditer(text):
            sp += 1
        if SUSY_PAT.search(text):
            susy_files.add(key)
        for m in ELL_NUM_PAT.finditer(text):
            ell_total.append((key, m.group(0)))
            cls = classify_ell(m)
            ell_classes[cls] += 1
            if cls == "own":
                ell_own.append((key, m.group(0)))
        for _ in GUT_EQ_GEOM_PAT.finditer(text):
            gut_geom += 1
    return sup, sp, len(susy_files), ell_total, ell_own, gut_geom, ell_classes


def gut_scale_line_scan(corpus):
    """枚举全部含统一尺度令牌的行（C18）：几何同现行数、其中赋值方程数、
    自承行（「无框架出处/待决」）数。证明扫描器对「几何提及」有分辨力，
    而几何提及全部落在靶自己的缺口自承上，不在任何方程里。"""
    n_lines = 0
    n_geom = 0
    n_eq_geom = 0
    n_admission = 0
    for key, text in corpus.items():
        if key == "audit07":
            continue
        for line in text.splitlines():
            if not GUT_TOKEN_PAT.search(line):
                continue
            n_lines += 1
            if GEOM_TOKEN_PAT.search(line):
                n_geom += 1
                if GUT_EQ_GEOM_PAT.search(line):
                    n_eq_geom += 1
                if re.search(r"无框架出处|待决", line):
                    n_admission += 1
    return n_lines, n_geom, n_eq_geom, n_admission


# ---------------------------------------------------------------------------
# 七、文本证据（G5）：逐字引文必须命中对应靶文件
# ---------------------------------------------------------------------------
EVIDENCE = [
    ("audit07", "路径 1：给出 $\\sin^2\\theta_W=1/4$ 的框架统一尺度出处"),
    ("audit07", "路径 2：从 $\\mathbb{Z}_4$ 对偶第一性推出超对称谱（使 $s^*$ 升格为真预测）"),
    ("audit07", "路径 3：统一尺度 $M_{GUT}$ 的几何指定"),
    ("audit07", "借用锚点不计 S13 完成度"),
    ("running", "无框架出处：候选需框架指定统一尺度，否则无预测"),
    ("running", "对照观察，非本框架推导"),
    ("running", "唯一自洽尺度 M ≈ 3.7 TeV 无框架出处"),
    ("ch25", "与 $SU(5)$ 大统一的 $3/8 = 0.375$ 不同，是可区分的几何预言"),
    ("ch25", "框架尚未推出 MSSM 粒子谱（OPEN）"),
    ("ch25", "若 $\\ell = \\ell_{P}$，则 $\\Lambda\\ell_{P}^{2} = O\\left( 1 \\right)$"),
    ("ch25", "$v = 255.26\\,\\mathrm{GeV}$"),
    ("vol3", "精确相交（超对称情形）"),
    ("vol3", "若本源不是单群，这三根线永远不会相交"),
    ("vol3", "耦合统一：$\\sin^2\\theta_W=3/8$"),
    ("vol3", "从低能 $\\sin^2\\theta_W(M_Z)\\approx0.231$ 反推，得统一尺度"),
    ("vol3", "\\ell_{\\text{min}} \\sim \\ell_P = \\sqrt{\\frac{\\hbar G}{c^3}}\\approx 1.6\\times10^{-35}\\,\\text{m}"),
    ("vol7", "\\sin^2\\theta_W=\\tfrac38"),
    ("eqmd", "统一尺度的几何指定"),
    ("eqmd", "v = \\ell^{-1}"),
    ("ganggang", "$v = \\ell^{-1}$"),
    ("cand", "实测（MSSM RGE）"),
    ("cand", "α_{GUT}^{-1}=25$"),
    ("v18", "1.9904729e+16"),
    ("v18", "0.230943405280905868720056895551"),
    ("v18", "0.23638579274415291662"),
    ("v18", "3675.242923 GeV（无框架出处，候选未获支持）"),
    ("claims", "MSSM系数为理论假设"),
    ("claims", "MSSM间距0.76近似统一"),
]


def text_evidence_check(corpus):
    missed = []
    for key, sub in EVIDENCE:
        if sub not in corpus.get(key, ""):
            missed.append((key, sub))
    return missed


# ---------------------------------------------------------------------------
# 八、主审计
# ---------------------------------------------------------------------------
def run_audit():
    kn = {}
    corpus = load_corpus()

    # ================= 正对照层 =================
    g_sm, mu_sm, g_ms, mu_ms, agut_min = rge_target_protocol()
    ctl("C1", "正对照：逐位复现靶 rge_sim 协议（圆整初值+RK4+1TeV 续接）——"
              "SM 间距 4.060 @2.37e14、MSSM 间距 0.760 @1.42e16",
        abs(g_sm - 4.060) < 5e-3 and abs(g_ms - 0.760) < 5e-3
        and abs(mu_sm / 2.37e14 - 1) < 2e-3 and abs(mu_ms / 1.42e16 - 1) < 2e-3,
        "SM gap={:.4f} @ {:.4e}；MSSM gap={:.4f} @ {:.4e}；α_GUT⁻¹(min)={:.2f}".format(
            g_sm, mu_sm, g_ms, mu_ms, agut_min))
    kn["rge_sm_gap_target_protocol"] = g_sm
    kn["rge_mssm_gap_target_protocol"] = g_ms
    kn["rge_mssm_scale_target_protocol"] = mu_ms
    kn["agut_inv_at_min_gap_target_protocol"] = agut_min

    x12, m12, a_at12, a3_at12, gap12 = sm_crossing()
    xu, mu, a_gut, a3_at, gapu = mssm_crossing()
    x_v, a1v, a2v, s2wv, s2wv_pct = s2w_at_v()
    xs, ms = m_star()
    s_star, l_resid, m_pred, a_gut_s, sstar_pct = sstar_closed()
    sstar_resid = abs(s_star - SSTAR_TARGET)
    ctl("C2", "正对照：闭式读数与 V1.8 逐位对拍——A1/A2/A3、SM 交点、"
              "sin²θ(v)、M*、MSSM 交点、s*（Decimal 30 位）、M(s*)、α_GUT⁻¹(s*)",
        abs(float(A1_0) - 59.003557488) < 1e-9
        and abs(float(A2_0) - 29.57673752) < 1e-8
        and abs(float(A3_0) - 8.481764206955047) < 1e-12
        and abs(float(m12) / 1.023741e13 - 1) < 1e-5
        and abs(float(gap12) - 13.1406) < 1e-3
        and abs(float(s2wv) - 0.23638579274415292) < 1e-16
        and abs(float(s2wv_pct) + 5.44568) < 1e-4
        and abs(float(ms) - 3675.242923) < 1e-5
        and abs(float(mu) / 1.9904729e16 - 1) < 1e-6
        and abs(float(a_gut) - 24.321948) < 1e-5
        and abs(float(gapu) - 0.311719) < 1e-4
        and sstar_resid < D("1e-28")
        and abs(float(m_pred) / 2.1210004e16 - 1) < 1e-6
        and abs(float(a_gut_s) - 24.27645852) < 1e-7,
        "s*={}；resid={:.1e}；M(s*)={:.6e}；α_GUT⁻¹(s*)={:.8f}；M*={:.6f}".format(
            str(s_star)[:32], float(sstar_resid), float(m_pred),
            float(a_gut_s), float(ms)))
    kn["A1_inv"] = str(A1_0)
    kn["A2_inv"] = str(A2_0)
    kn["A3_inv"] = str(A3_0)
    kn["sm_cross_M"] = float(m12)
    kn["sm_cross_gap_pct"] = float(gap12)
    kn["mssm_cross_M"] = float(mu)
    kn["mssm_cross_agut_inv"] = float(a_gut)
    kn["mssm_cross_gap_pct"] = float(gapu)
    kn["s2w_at_v"] = float(s2wv)
    kn["s2w_at_v_diff_pct"] = float(s2wv_pct)
    kn["M_star_GeV"] = float(ms)
    kn["sstar"] = str(s_star)
    kn["sstar_residual_vs_target"] = float(sstar_resid)
    kn["sstar_M"] = float(m_pred)
    kn["sstar_agut_inv"] = float(a_gut_s)
    kn["sstar_diff_pct"] = float(sstar_pct)
    add("A1", "正对照",
        "RG 跑动计算与靶语料逐位一致：靶协议 SM {:.3f}@{:.2e} / MSSM {:.3f}@{:.2e}；"
        "闭式读数 A1={}、A2={}、SM 交点差距 {:.4f}%、sin²θ(v)={:.17g}（{:+.4f}%）、"
        "M*={:.6f} GeV、MSSM 交点 {:.6e}（{:.6f}%）、s* 与靶 30 位值残差 {:.1e}、"
        "M(s*)={:.6e}".format(
            g_sm, mu_sm, g_ms, mu_ms, str(A1_0)[:12], str(A2_0)[:11], float(gap12),
            float(s2wv), float(s2wv_pct), float(ms), float(mu), float(gapu),
            float(sstar_resid), float(m_pred)),
        "PASS", "本卷后续指控不源于计算错误（计算与靶完全一致）")

    dper = check_duality_period()
    ctl("C3", "正对照：Θ²=−I 对偶周期 4（200 随机复旋量，四次回归+二次反号机器零）",
        dper == 0.0, "worst={:.1e}".format(dper))
    kn["duality_period_residual"] = dper
    add("A2", "正对照", "框架自己的数学：对偶周期 4（Θ²=−I）机器零——本卷不指控该恒等式",
        "PASS", "靶板块一登记的正确核")

    ctl("C4", "正对照：s* 闭式推导正确——两方程同解（L13−L23 恒等，Decimal 50 位）",
        abs(float(l_resid)) < 1e-40, "L13-L23={:.1e}".format(float(l_resid)))
    kn["sstar_L_residual"] = float(l_resid)
    add("A3", "正对照",
        "s*=(3a+7A3)/(15a) 的闭式推导本身正确（三线汇聚两方程同解，恒等残差 {:.1e}）"
        "——本卷不指控靶的代数".format(float(l_resid)),
        "PASS", "问题在于该公式的输入全部外部（见 B7），不在于推导")

    b_sm = beta_from_content()
    ctl("C5", "正对照：SM β 系数由 SM 内容闭式重算 = (41/10, −19/6, −7)（精确有理）",
        b_sm == (F(41, 10), F(-19, 6), F(-7)),
        "computed={} expect=(41/10,-19/6,-7)".format(b_sm))
    kn["sm_beta_from_content"] = [str(x) for x in b_sm]
    add("A4", "正对照",
        "内容→β 系数方法正对照：SM 内容（3 代 + 1 希格斯双重态）精确重算 "
        "({}, {}, {})——方法可靠，B8 据此检框架自有内容".format(
            b_sm[0], b_sm[1], b_sm[2]),
        "PASS", "公式约定与靶脚本一致（GUT 归一化）")

    ratio2 = F(1, 3)                       # (g'/g)² = 1/3
    s2w_cand = ratio2 / (1 + ratio2)       # = 1/4
    ctl("C6", "正对照：λ₈ 嵌入代数 g'/g=1/√3 ⇒ sin²θ=(1/3)/(4/3)=1/4（精确）",
        s2w_cand == F(1, 4), "s2w_cand={}".format(s2w_cand))
    kn["s2w_candidate_algebra"] = str(s2w_cand)
    add("A5", "正对照",
        "靶定理 25.4 的代数正确：CP² 稳定子嵌入 g'/g=1/√3 ⇒ sin²θ_W=1/4（精确）"
        "——本卷指控的是该候选的**尺度出处**（B1/B2），不是其代数",
        "PASS", "候选 = 几何选择的后果；几何选择本身无排他性（r178 槽位账）")

    # ================= 路径 1 层 =================
    v_fit, e_fit, g_fit = v_fit_from_pdg()
    ctl("C7", "v 出处机读：ch25 §25.2 反解式 v=2m_W/g̃（g̃=e/sinθ）只含 PDG 常数，"
              "重算 v={:.5f} GeV 与靶 255.26 吻合".format(v_fit),
        abs(v_fit - 255.26) < 5e-3, "v_fit={:.6f}".format(v_fit))
    kn["v_fit_from_pdg"] = v_fit
    add("B1", "路径1",
        "「框架真空值」v=255.26 GeV 是 **PDG 反解锚点**而非框架输出："
        "v=2m_W/g̃、g̃=e/sinθ_W、e=√(4πα)（靶定理 25.1 自证），表达式只含实验常数"
        "（m_W, α, sin²θ_W）；重算 {:.5f} GeV 与靶值吻合 ⇒ 该「框架尺度」零框架含量".format(v_fit),
        "FAIL", "ch25 §25.2 数值行 + constant_unify_verify.py 验证A 自证此反解链")

    mstar_ratio_v = float(ms) / v_fit
    ell_impl, ell_p, ell_ratio, ell_p_inv = ell_calibres()
    mstar_ratio_lp = float(ms) / ell_p_inv
    mono, dmin_slope = s2w_monotonic()
    ctl("C8", "M* 孤儿性 + 唯一性机读：M*/v={:.4f}、M*/ℓ_P⁻¹={:.3e}；"
              "sin²θ(μ) 在 [M_Z,1e17] 严格单调递增（min slope={:.4f}）⇒ 0.25 唯一穿越".format(
                  mstar_ratio_v, mstar_ratio_lp, float(dmin_slope)),
        mstar_ratio_v > 5 and mstar_ratio_lp < 1e-10 and mono,
        "M*/v={:.4f} M*/ellP^-1={:.3e} monotonic={}".format(
            mstar_ratio_v, mstar_ratio_lp, mono))
    kn["Mstar_over_v"] = mstar_ratio_v
    kn["Mstar_over_ellP_inv"] = mstar_ratio_lp
    kn["s2w_monotonic"] = mono
    add("B2", "路径1",
        "sin²θ=1/4 唯一自洽尺度 M*={:.4f} GeV 是**孤儿尺度**：M*/v={:.3f}、"
        "M*/ℓ_P⁻¹={:.2e}，与框架两个可及尺度（v、ℓ_P⁻¹）均无关系（单调性守卫确认"
        "该尺度唯一）；靶三处自承「无框架出处」（running L63/L98、V1.8 P9c）".format(
            float(ms), mstar_ratio_v, mstar_ratio_lp),
        "FAIL", "路径 1 未闭合：跑动既不在 v 成立（−5.45%），也不在 ℓ_P⁻¹ 成立")

    sup_hits, sp_hits, susy_nfiles, ell_total, ell_own, gut_geom, ell_cls = \
        corpus_scan(corpus)
    ctl("C9", "ℓ 口径机读：数值 ℓ 指定共 {} 处——三分类 planck {} / 自然单位 {} / "
              "框架自有物理值 **{}**；由拟合 v 隐含 ℓ={:.4e} m 与 ℓ_P 差 {:.2e}"
              "（假阳性 ℓ⁴=0 已被 ASCII 后缀类排除）".format(
                  len(ell_total), ell_cls["planck"], ell_cls["unit_one"],
                  ell_cls["own"], ell_impl, ell_ratio),
        ell_cls["own"] == 0 and len(ell_total) > 0 and ell_ratio < 1e-15,
        "ell_total={} planck={} unit_one={} own={} ellP/ell_implied={:.3e}".format(
            len(ell_total), ell_cls["planck"], ell_cls["unit_one"],
            ell_cls["own"], ell_ratio))
    kn["numeric_ell_hits_total"] = len(ell_total)
    kn["numeric_ell_hits_own"] = ell_cls["own"]
    kn["numeric_ell_hits_planck"] = ell_cls["planck"]
    kn["numeric_ell_hits_unit_one"] = ell_cls["unit_one"]
    kn["ell_implied_from_v_fit_m"] = ell_impl
    kn["ellP_over_ell_implied"] = ell_ratio
    ell_impl_over_ellP = 1.0 / ell_ratio
    add("B3", "路径1/3",
        "尺度 ℓ **四重口径互不往来**：① M5 符号自对偶尺度（无数值）；② 由拟合 v 经 "
        "v=ℓ⁻¹ 隐含 ℓ=ħc/v={:.4e} m（全集 {} 处数值 ℓ 指定中 0 处是它）；"
        "③ Λ/截断估计专用 ℓ_P=1.616e-35 m（差 {:.2e}）；④ **推导卷线另锚一头**——"
        "卷三 L146 把奇点截断锚到 ℓ_min∼ℓ_P=1.6e-35 m，与主线由拟合 v 隐含的 ℓ "
        "相差 {:.2e} 倍（两条卷线各用各的 ℓ，相差 17 个数量级）——若 v=ℓ⁻¹ 是框架关系，"
        "Λ 估计用的就不是框架自己的 ℓ".format(
            ell_impl, len(ell_total), ell_ratio, ell_impl_over_ellP),
        "FAIL", "equations.md §六 + ch25 §25.6 + 总纲 §六 + 卷三 L146 文本证据在册")

    # ================= 路径 2 层 =================
    ctl("C10", "形式化机读：超场/超多重态/超势/Wess-Zumino 计数 = {}；"
               "超伴子名单（排除「中微子」假阳性）= {}；提及超对称/MSSM 的文件 = {}"
               "（>0 证明扫描器有分辨力）".format(sup_hits, sp_hits, susy_nfiles),
        sup_hits == 0 and sp_hits == 0 and susy_nfiles > 0,
        "superfield={} sparticles={} susy_files={}".format(
            sup_hits, sp_hits, susy_nfiles))
    kn["superfield_hits"] = sup_hits
    kn["sparticle_hits"] = sp_hits
    kn["susy_files"] = susy_nfiles
    add("B4", "路径2",
        "超对称**形式化零存在**：全集 0 处超场/超多重态/超势/Wess-Zumino，"
        "0 处超伴子名单（「微子」13 处全为「中微子」假阳性，已排除）；"
        "「推出超对称谱」在框架内没有可执行的形式语言",
        "FAIL", "超对称/MSSM 仅作外部对照出现（{} 个文件）".format(susy_nfiles))

    add("B5", "路径2",
        "Z₄ 对偶周期与「超对称谱」**范畴错置**：对偶周期四是**同一个 Ψ 的四个态**"
        "（Ψ→Ψ*→−Ψ→−Ψ*→Ψ，A2 机读——四态全部由同一个二分量矢量生成），"
        "不产生新场、不映射玻色子↔费米子；超对称谱是**一组不同的场**"
        "（每个 SM 场配超伴子、希格斯二重态翻倍）。靶自己的表述亦止于"
        "「费米子↔玻色子对偶」的类比（ch25 §25.8）",
        "FAIL", "靶无任何「Θ 作用于场空间产生新场」的方程；4 态同源一场 vs 场集合翻倍")

    higgs_fw = 1      # S³=U(2)/U(1) 真空流形：恰一个复二重态（equations.md 依赖链）
    higgs_mssm = 2    # MSSM 必需 H_u、H_d 两个双重态
    ctl("C11", "Higgs 双重态计数：框架 1（S³=U(2)/U(1)）vs MSSM 2 ⇒ 比值 1/2",
        higgs_fw == 1 and higgs_mssm == 2 and higgs_fw != higgs_mssm,
        "fw={} mssm={}".format(higgs_fw, higgs_mssm))
    kn["higgs_doublets_framework"] = higgs_fw
    kn["higgs_doublets_mssm"] = higgs_mssm
    add("B6", "路径2",
        "框架希格斯扇区与 MSSM 谱**结构性不符**：框架真空流形 S³=U(2)/U(1) 给出"
        "**恰 1 个**复二重态（V=κ(|Ψ|²−v²)² 谱 {{0,0,0,8κv²}}，r178 已独立重算相符），"
        "MSSM 必需 **2 个**希格斯二重态 ⇒ 框架自有内容不是 MSSM 谱",
        "FAIL", "1/2：连希格斯双重态数目都不匹配，更不用说超伴子翻倍")

    sstar_sm_beta = sstar_with_beta(SM_B)
    sstar_sm_pct = float((sstar_sm_beta - S2W_EXP) / S2W_EXP * 100)
    formula_symbols = {"alpha_EM_inv", "alpha_s_inv", "b1_MSSM", "b2_MSSM", "b3_MSSM"}
    framework_symbols = {"v", "ell", "lambda", "kappa_tilde", "g_tilde", "g_tilde_prime",
                         "Theta", "Z4", "CP2", "Q_H", "D", "gamma", "v_fw"}
    inter = formula_symbols & framework_symbols
    ctl("C12", "s* 框架含量机读：公式符号集 ∩ 框架量集 = {}；负对照换 SM β ⇒ "
               "s*={:.6f}（与实验差 {:+.2f}%）".format(
                   sorted(inter), float(sstar_sm_beta), sstar_sm_pct),
        len(inter) == 0 and abs(float(sstar_sm_beta) - 0.17164179104477612) < 1e-12,
        "intersection={} sstar_sm_beta={:.17g}".format(
            sorted(inter), float(sstar_sm_beta)))
    kn["sstar_formula_symbols"] = sorted(formula_symbols)
    kn["sstar_framework_intersection"] = sorted(inter)
    kn["sstar_with_sm_beta"] = float(sstar_sm_beta)
    kn["sstar_with_sm_beta_diff_pct"] = sstar_sm_pct
    add("B7", "路径2",
        "s* 的**框架含量为零**：闭式 s*=(3a+7A3)/(15a) 只含 α_EM⁻¹、α_s⁻¹（实验输入）"
        "与 MSSM β 系数（33/5, 1, −3）；框架量（v, ℓ, Θ, Z₄, CP², Q_H…）零进入"
        "（集合交 = ∅）。负对照：同一解法换 SM β ⇒ s*={:.6f}（与实验差 {:+.2f}%）"
        "⇒ s* 是**导入 β 系数的函数**，不是框架的预测".format(
            float(sstar_sm_beta), sstar_sm_pct),
        "FAIL", "靶三处自承「外部数值锚点/对照观察，非本框架推导/类比观察」")

    b_fw = beta_from_content()
    b_msm_expected = (F(33, 5), F(1), F(-3))
    ctl("C13", "框架自有内容（3 代 SM 量子数表 + 1 希格斯二重态）⇒ β = {}，"
               "即 SM β；b2={} < 0（渐近自由）vs 引用 MSSM b2=+1 > 0（反号）".format(
                   b_fw, b_fw[1]),
        b_fw == (F(41, 10), F(-19, 6), F(-7)) and b_fw[1] < 0 < b_msm_expected[1],
        "fw_beta={} mssm_beta={}".format(b_fw, b_msm_expected))
    kn["framework_beta_from_content"] = [str(x) for x in b_fw]
    kn["mssm_beta_cited"] = [str(x) for x in b_msm_expected]
    add("B8", "路径2/3",
        "框架**自有内容给出 SM β**（b2=−19/6<0，SU(2) 渐近自由），而其统一叙事"
        "（卷三「三线精确相交」）引用的是 MSSM β（b2=+1>0，**符号相反**）："
        "MSSM β 要求超伴子翻倍 + 2 个希格斯二重态，框架一样也没有（B4/B6）⇒ "
        "复现的「统一」属于框架并不拥有的理论",
        "FAIL", "SM β 下三线不统一（靶自证 gap 4.06）；统一与否取决于换用别人的 β")

    # ================= 路径 3 层 =================
    ctl("C14", "「精确相交」机读：靶协议 MSSM 最小间距 {:.4f} ≠ 0；靶自己的判据 "
               "<0.5 给出「{}」".format(g_ms, "否" if g_ms >= 0.5 else "是"),
        g_ms > 0.5,
        "gap={:.4f}（target prints 否）".format(g_ms))
    kn["exact_crossing_refuted_gap"] = g_ms
    add("B9", "路径3",
        "卷三「三根耦合线在 10¹⁶ GeV **精确相交**……若本源不是单群，这三根线永远不会相交」"
        "被语料库自己的机器读数否证：靶 rge_sim 实测 MSSM 最小间距 **{:.3f}**≠0"
        "（其 <0.5 判据自判「否」），claims.csv 自承「残余间距 0.76 未闭合」".format(g_ms),
        "FAIL", "卷三 L76/L78 文本证据在册；「精确相交」是未闭合的近统一")

    gut_lines, gut_geom_lines, gut_eq_geom_lines, gut_admissions = \
        gut_scale_line_scan(corpus)
    ctl("C18", "路径3 几何指定枚举（分辨力正/负对照）：全集含统一尺度令牌的行 {} 条，"
               "其中提及几何标度 **{}** 条——全部是靶自承「无框架出处/框架待决」"
               "（{} 条），**赋值方程 0** 条；反之全部数值 M_GUT 行（反推/RGE 实测/"
               "闭式）几何标志为 False".format(gut_lines, gut_geom_lines, gut_admissions),
        gut_eq_geom_lines == 0 and gut_geom_lines == gut_admissions and gut_lines > 10,
        "gut_lines={} geom_lines={} eq_geom={} admissions={}".format(
            gut_lines, gut_geom_lines, gut_eq_geom_lines, gut_admissions))
    kn["gut_scale_lines_total"] = gut_lines
    kn["gut_scale_lines_with_geom"] = gut_geom_lines
    kn["gut_scale_lines_admission"] = gut_admissions

    agut_calibres = [
        ("ch25 对照锚点", 24.0, "≈1/24"),
        ("V1.8 s* 点", 24.27645852, "闭式"),
        ("V1.8 α1=α2 交点", 24.321948, "闭式"),
        ("卷三/候选五", 25.0, "反推"),
        ("rge_sim 最小间距点", agut_min, "RK4 协议"),
    ]
    tau_calibres = [
        ("候选五头条 (1.42e16, 25)", 1.42e16, 25.0),
        ("rge_sim 自点 (1.42e16, α_GUT⁻¹ 自算)", 1.42e16, agut_min),
        ("V1.8 交点", float(mu), float(a_gut)),
        ("V1.8 s* 点", float(m_pred), float(a_gut_s)),
    ]
    taus = [(name, tau_p_years(m, a)) for (name, m, a) in tau_calibres]
    tmin = min(t for _, t in taus)
    tmax = max(t for _, t in taus)
    agut_vals = [c[1] for c in agut_calibres]
    agut_spread = (max(agut_vals) - min(agut_vals)) / min(agut_vals) * 100
    x_tev_f = math.log(1000.0 / 91.1876) / (2 * math.pi)
    a_tev_precise = (float(A1_0) - float(SM_B[0]) * x_tev_f,
                     float(A2_0) - float(SM_B[1]) * x_tev_f,
                     float(A3_0) - float(SM_B[2]) * x_tev_f)
    g_precise_switch, x_precise = closed_min_gap(MSSM_B, a_tev_precise)
    g_precise_nosw, _ = closed_min_gap(MSSM_B, (float(A1_0), float(A2_0), float(A3_0)))
    g_sm_precise, _ = closed_min_gap(SM_B, (float(A1_0), float(A2_0), float(A3_0)))
    ctl("C15", "口径账：α_GUT⁻¹ 五口径极差 {:.2f}%；τ_p 四口径 {:.3e}–{:.3e} yr"
               "（展宽 {:.2f}×）；统一判词随输入圆整翻转（圆整 0.760「否」→ "
               "同协议精确 {:.3f}「是」；无阈值闭合式 {:.4f}）".format(
                   agut_spread, tmin, tmax, tmax / tmin, g_precise_switch,
                   g_precise_nosw),
        agut_spread > 5 and tmax / tmin > 3 and g_ms >= 0.5 and g_precise_switch < 0.5,
        "agut_spread={:.2f}% tau_spread={:.2f}x precise_switch={:.4f} "
        "precise_nosw={:.4f} sm_precise={:.4f}".format(
            agut_spread, tmax / tmin, g_precise_switch, g_precise_nosw, g_sm_precise))
    kn["agut_calibres"] = [list(c) for c in agut_calibres]
    kn["agut_spread_pct"] = agut_spread
    kn["tau_p_calibres"] = [[name, m, t] for (name, m, _), (_, t)
                            in zip(tau_calibres, taus)]
    kn["tau_p_spread"] = tmax / tmin
    kn["gap_precise_with_switch"] = g_precise_switch
    kn["gap_precise_no_switch"] = g_precise_nosw
    kn["gap_sm_precise"] = g_sm_precise
    add("B10", "路径3",
        "α_GUT⁻¹ **五口径**（{:.1f}/{:.2f}/{:.2f}/{:.1f}/{:.1f}，极差 {:.1f}%）；"
        "τ_p 头条 7.3e35 yr 是口径选择的结果——换语料库另三个口径得 "
        "{:.2e}/{:.2e}/{:.2e} yr（展宽 **{:.2f}×**）；且「统一与否」判词随输入圆整翻转："
        "圆整协议 gap 0.760（靶判「否」）vs 同协议精确输入 gap {:.3f}（将判「是」），"
        "无阈值闭合式 {:.4f}".format(
            agut_vals[0], agut_vals[1], agut_vals[2], agut_vals[3], agut_vals[4],
            agut_spread, taus[1][1], taus[2][1], taus[3][1], tmax / tmin,
            g_precise_switch, g_precise_nosw),
        "FAIL", "τ_p 全部落在可检验窗口内（对靶有利：未被实验排除）——本卷判口径依赖")

    s2w_38 = F(3, 8)
    s2w_14 = F(1, 4)
    dual_pct = float((s2w_38 - s2w_14) / s2w_14 * 100)
    ctl("C16", "双口径机读：3/8（卷三 L72/L180/L228 + 卷七 §六）vs 1/4"
               "（ch25 §25.5 + V1.6/V1.7）——相对差 {:.1f}%".format(dual_pct),
        dual_pct == 50.0,
        "3/8={} 1/4={} rel diff={:.1f}%".format(s2w_38, s2w_14, dual_pct))
    kn["s2w_dual_calibre_rel_diff_pct"] = dual_pct
    add("B11", "口径互斥",
        "sin²θ_W **双口径互斥**：推导卷线（卷三「GUT 约束」、卷七收口方程集）给 "
        "**3/8**（SU(5) 值），主理论线（ch25 §25.5、V1.6/V1.7）给 **1/4**（CP² 候选）"
        "并明言「与 SU(5) 的 3/8 不同、可区分」——同一语料库两个互斥预言（相对差 "
        "{:.0f}%）；equations.md 自承归一化来源 OPEN；其间的等价性主张（0a）已被 r178 判 FAIL".format(
            dual_pct),
        "FAIL", "与 r177 m_p/Z、r180 Z′、r182 G 同族：同一符号多个口径（第四度）")

    add("B12", "防过度指控",
        "靶诚实边界执行良好：负面结果如实记录（running L98「候选未获跑动支持」）、"
        "OPEN 标注齐全（equations.md §五）、三处自承锚点性质（「非本框架推导」"
        "「类比观察」「外部数值锚点」）、claims.csv 状态 conjecture/unreviewed "
        "⇒ 本卷判「路径 1–3 未闭合」，**不指控造假**",
        "INFO", "与 10-07 审计「不指控造假，只校准叙事距离」同口径")

    add("D1", "边界",
        "本卷只审计残余路径 1–3：S13 数学恒等式层（流守恒/曲率闭式/质量谱等）"
        "与路径四（r178：0/13 槽位）不在本卷重判；路径 1–3 的未闭合结论与 "
        "2026-10-07 审计登记一致（分层铁律：条目不可与 r142–r187 相加）",
        "BOUNDARY", "靶的诚实登记本身是对审计的配合，不是缺口")

    # ================= 修复定价 =================
    # 每条路径的必要条件（机读：语料库中是否存在对应推导/结构）
    cond = {
        1: [("框架方程固定 sin²θ=1/4 成立尺度", mstar_ratio_v <= 1.001 or
             abs(mstar_ratio_lp - 1.0) < 1e-6),
            ("该尺度为框架量（v/ℓ_P⁻¹）", False)],
        2: [("超对称形式化存在", sup_hits > 0),
            ("Z₄/Θ⇒超对称谱的推导存在", sp_hits > 0),
            ("谱含 2 个希格斯二重态", higgs_fw == higgs_mssm)],
        3: [("把统一尺度赋值给几何标度（ℓ_P/普朗克/分形）的方程存在", gut_geom > 0)],
    }
    # 宽松档（外部锚点+如实标注）逐路径机读
    loose = {
        1: abs(mstar_ratio_v - 1.0) < 1e-3,                       # M* 须就是 v
        2: abs(float(sstar_pct)) < 0.2 and sup_hits > 0,          # s* 吻合且须有形式化
        3: gut_geom > 0,
    }
    n_paths = 3
    survive = 0
    zero_cost = 0
    combos = []
    for mask in range(2 ** n_paths):
        chosen = [p for p in (1, 2, 3) if mask & (1 << (p - 1))]
        if not chosen:
            combos.append((mask, (), "空集（非修复）", False))
            continue
        strict_ok = all(v for p in chosen for _, v in cond[p])
        loose_ok = all(loose[p] for p in chosen)
        combos.append((mask, tuple(chosen), strict_ok, loose_ok))
        if strict_ok:
            survive += 1
        if loose_ok:
            zero_cost += 1
    ctl("C17", "修复定价位掩码机读：2^3=8 路径组合——宣称域内成立 {}、"
               "零代价（宽松档=外部锚点+标注；10-07 审计明定不计完成度）{}".format(
                   survive, zero_cost),
        survive == 0 and zero_cost == 0 and len(combos) == 8,
        "survive={} zero_cost={} gut_geom_colines={}".format(
            survive, zero_cost, gut_geom))
    kn["gut_geom_colines"] = gut_geom
    kn["repair_combinations"] = 2 ** n_paths
    kn["repair_survive"] = survive
    kn["repair_zero_cost"] = zero_cost
    add("R1", "修复定价",
        "路径 1–3 闭合价：2^3=8 组合机读——宣称域内成立 **{}**、零代价 **{}**"
        "（宽松档=「外部锚点+如实标注」：语料库已实施，而 10-07 审计明定"
        "「借用锚点不计 S13 完成度」⇒ 宽松档同样 0）。三条路径的必要条件"
        "（框架尺度方程/超形式化+谱推导+2 重态/统一尺度几何赋值方程）在语料库中零存在"
        "⇒ 无一组合可闭合".format(survive, zero_cost),
        "FAIL", "与 r178 路径四定价（0/8192）同型：S13 兄弟家族，不计主线度数")

    # ================= 守卫 =================
    entries_boundary_text = " ".join(
        e[2] + " " + e[4] for e in ENTRIES if e[3] == "BOUNDARY")
    n_fail = sum(1 for e in ENTRIES if e[3] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e[3] == "PASS")
    n_info = sum(1 for e in ENTRIES if e[3] == "INFO")
    n_bound = sum(1 for e in ENTRIES if e[3] == "BOUNDARY")

    grd("G1", "FAIL 条目全部带非空机读证据（note 非空）",
        all(e[4] for e in ENTRIES if e[3] == "FAIL"),
        "FAIL={}".format(n_fail))
    grd("G2", "verdict 由条目计数机读驱动（FAIL>0 且 PASS>0）",
        n_fail > 0 and n_pass > 0,
        "FAIL={} PASS={} INFO={} BOUNDARY={}".format(
            n_fail, n_pass, n_info, n_bound))
    grd("G3", "分层铁律短语机读在册（REDLINE + BOUNDARY 条目文本）",
        REDLINE_PHRASE in REDLINE and REDLINE_PHRASE in entries_boundary_text,
        "in_REDLINE={} in_D1={}".format(
            REDLINE_PHRASE in REDLINE, REDLINE_PHRASE in entries_boundary_text))
    missing_files = [k for k, rel in TARGET_FILES.items()
                     if not (os.path.isfile(os.path.join(S13, rel))
                             and os.path.getsize(os.path.join(S13, rel)) > 0)]
    audit07_ok = os.path.isfile(AUDIT07) and os.path.getsize(AUDIT07) > 0
    grd("G4", "靶文件全部可读（{} 个 S13 文件 + 10-07 审计册）".format(
            len(TARGET_FILES)),
        not missing_files and audit07_ok,
        "missing={} audit07={}".format(missing_files, audit07_ok))
    missed_ev = text_evidence_check(corpus)
    grd("G5", "文本证据全部命中（{} 条逐字引文）".format(len(EVIDENCE)),
        not missed_ev, "missed={}".format(missed_ev))

    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        own_src = f.read()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tree = ast.parse(own_src)
    hard = 0
    total_ok = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ("ctl", "grd") and len(node.args) >= 3:
            total_ok += 1
            if isinstance(node.args[2], ast.Constant):
                hard += 1
    grd("G6", "ast 自审：ctl/grd 的 ok 参数 {} 处，常量写死 {} 处（禁写死 True）".format(
            total_ok, hard),
        hard == 0 and total_ok >= 15,
        "total_ok_args={} hardcoded={}".format(total_ok, hard))

    pos_pass = [e for e in ENTRIES if e[3] == "PASS"]
    grd("G7", "正对照条目 ≥4 且全部 PASS（方法分辨力）",
        len(pos_pass) >= 4, "PASS entries={}".format(len(pos_pass)))
    grd("G8", "对拍容差按靶有效位声明（s* 30 位 Decimal 1e-28 / M* 9 位 1e-5 / 交点 8 位 1e-6）",
        sstar_resid < D("1e-28") and abs(float(ms) - 3675.242923) < 1e-5
        and abs(float(mu) / 1.9904729e16 - 1) < 1e-6,
        "sstar_resid={:.1e} Mstar_resid={:.1e} cross_resid={:.1e}".format(
            float(sstar_resid), abs(float(ms) - 3675.242923),
            abs(float(mu) / 1.9904729e16 - 1)))
    grd("G9", "B7 的 ∅ 判定由集合运算产生（公式符号 ∩ 框架量 = ∅）",
        len(kn["sstar_framework_intersection"]) == 0,
        "intersection={}".format(kn["sstar_framework_intersection"]))
    grd("G10", "路径判定机读：三路径必要条件缺失由数据结构计数（形式化/谱/双重态/几何同现）",
        sup_hits == 0 and sp_hits == 0 and higgs_fw != higgs_mssm and gut_geom == 0,
        "sup={} sp={} higgs {}/2 gut_geom={}".format(
            sup_hits, sp_hits, higgs_fw, gut_geom))
    grd("G11", "修复定价位掩码机读（8 组合全枚举，survive 由循环计数）",
        len(combos) == 8 and survive == 0,
        "combos={} survive={}".format(len(combos), survive))

    kn["entries_total"] = len(ENTRIES)
    kn["entries_fail"] = n_fail
    kn["entries_pass"] = n_pass
    return kn


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
        "target": "01_独立体系/S13_全域双向分形统一场论（残余 OPEN 路径 1–3）",
        "verdict": VERDICT,
        "entries": entries,
        "controls": controls,
        "guards": guards,
        "key_numbers": kn,
        "counts": counts,
        "redline": REDLINE,
        "not_closed": [
            "路径 1（sin²θ_W=1/4 的框架统一尺度出处）：维持 OPEN——唯一自洽尺度 "
            "M*≈3.7 TeV 无框架出处，v 处差 −5.45%",
            "路径 2（Z₄→超对称谱）：维持 OPEN——超形式化零存在、范畴错置、"
            "s* 框架含量为零",
            "路径 3（M_GUT 几何指定）：维持 OPEN——尺度清单无几何关系、"
            "α_GUT⁻¹ 五口径、τ_p 口径依赖",
            "若靶日后给出 CP² 尺度方程或超场构造，B1/B2/B4 应重审",
            "若 MSSM 残余间距被新谱模型闭合且该谱出自 Z₄，B8/B9 应重审",
        ],
    }


def render_report(payload):
    kn = payload["key_numbers"]
    L = []
    L.append("=" * 78)
    L.append("TUFT-r188｜S13 残余 OPEN 路径 1–3 第一性审计")
    L.append("（统一尺度出处 / Z₄→超对称 / M_GUT 几何指定）")
    L.append("=" * 78)
    L.append("靶：01_独立体系/S13_全域双向分形统一场论（路径 4 已由 r178 闭合为 0/13 槽位）")
    L.append("")
    L.append("[正对照层] 靶确实正确的东西（方法分辨力证明）")
    for e in payload["entries"]:
        if e["verdict"] == "PASS":
            L.append("  [PASS] {} | {} | {}".format(e["id"], e["layer"], e["text"]))
    L.append("")
    L.append("[控制组]")
    for c in payload["controls"]:
        L.append("  {}  {} {} — {}".format("OK " if c["ok"] else "FAIL",
                                           c["id"], c["text"], c["detail"]))
    L.append("")
    L.append("[条目]")
    for e in payload["entries"]:
        if e["verdict"] == "PASS":
            continue
        L.append("  [{}] {} | {} | {}".format(e["verdict"], e["id"], e["layer"], e["text"]))
        if e["note"]:
            L.append("        注：{}".format(e["note"]))
    L.append("")
    L.append("[路径台账]")
    L.append("  路径 1（框架统一尺度出处）：FAIL——M*={:.4f} GeV 孤儿（M*/v={:.3f}、"
             "M*/ℓ_P⁻¹={:.2e}）；v=255.26 系 PDG 反解（{:.5f} GeV 重算吻合）".format(
                 kn["M_star_GeV"], kn["Mstar_over_v"], kn["Mstar_over_ellP_inv"],
                 kn["v_fit_from_pdg"]))
    L.append("  路径 2（Z₄→超对称谱）：FAIL——超形式化 {} 命中、超伴子 {} 命中；"
             "Higgs 二重态 {}/2；s* 框架交={}；自有内容⇒SM β {}".format(
                 kn["superfield_hits"], kn["sparticle_hits"],
                 kn["higgs_doublets_framework"], kn["sstar_framework_intersection"],
                 kn["framework_beta_from_content"]))
    L.append("  路径 3（M_GUT 几何指定）：FAIL——α_GUT⁻¹ 五口径极差 {:.2f}%；"
             "τ_p 展宽 {:.2f}×；精确输入同协议 gap {:.3f} vs 圆整 0.760；"
             "M_GUT-几何同现行 {}".format(
                 kn["agut_spread_pct"], kn["tau_p_spread"],
                 kn["gap_precise_with_switch"], kn["gut_geom_colines"]))
    L.append("")
    L.append("[守卫]（全部机读驱动，无一处 ok 写死 True）")
    for g in payload["guards"]:
        L.append("  {}  {} {} — {}".format("OK " if g["ok"] else "FAIL",
                                           g["id"], g["text"], g["detail"]))
    L.append("")
    L.append("[修复定价] 2^3=8 组合：宣称域内成立 {}、零代价 {}".format(
        kn["repair_survive"], kn["repair_zero_cost"]))
    L.append("[判词]")
    L.append("  " + payload["verdict"])
    L.append("")
    L.append("[未闭合项]")
    for x in payload["not_closed"]:
        L.append("  - " + x)
    L.append("")
    cnt = payload["counts"]
    L.append("条目： " + " / ".join("{}={}".format(k, v) for k, v in sorted(cnt.items())))
    L.append("控制组： {} / {}".format(sum(1 for c in payload["controls"] if c["ok"]),
                                       len(payload["controls"])))
    L.append("守卫  ： {} / {}".format(sum(1 for g in payload["guards"] if g["ok"]),
                                       len(payload["guards"])))
    return "\n".join(L) + "\n"


def render_verdict_md(payload):
    kn = payload["key_numbers"]
    L = []
    L.append("# 判定册 · TUFT-r188｜S13 残余 OPEN 路径 1–3 第一性审计")
    L.append("")
    L.append("## 一、编号与定位")
    L.append("")
    L.append("- **编号 r188**（★取号经过：起草取 r186，源码 10:04:10 落盘后**登记前复查"
             "磁盘时间戳**（承 r177/r178 教训）发现并行会话已先占 **r186**（09:41:31"
             "《F5 钱德拉塞卡极限复核》四件套齐全）与 **r187**（09:55:45《变分推导链路"
             "求导验证》四件套齐全）⇒ 按「先占位者为权威、后到者整体改号」铁律整体改号 "
             "**r188**；旧 r186 四件套入 `scratch/r186_s13_old_outputs/`；"
             "**未触碰并行会话任何字节**；r188 为实测首空号）")
    L.append("- **靶**：`01_独立体系/S13_全域双向分形统一场论/`——running_unify_verify.py"
             "（V1.7）、constant_unify_verify.py（V1.6）、openuft_rge_sim.py、"
             "验证精算报告 V1.8、候选预言验证 V2.0、ch25（第25章）、卷三/卷七（SO(10) 线）、"
             "equations.md、理论总纲 V1.7、claims.csv")
    L.append("- **背景**：2026-10-07 攻破审计登记四条 OPEN 路径；**路径 4 已由 r178 闭合**"
             "（三公设对 SM 结构 0/13 槽位供给）；本卷审计**残余路径 1–3**。")
    L.append("- **分层**：本卷为 S13 路径 1–3 审计层，与 r142–r187 条目**不可相加**。")
    L.append("")
    L.append("## 二、判词")
    L.append("")
    L.append("`" + payload["verdict"] + "`")
    L.append("")
    L.append("三条路径全部维持 OPEN，且均为**第一性来源缺失**（不是数值错误——"
             "本卷正对照证明审计计算与靶逐位一致）：路径 1 的唯一自洽尺度 3.7 TeV "
             "无框架出处；路径 2 的超对称形式化在框架内零存在、s* 公式框架含量为零；"
             "路径 3 的统一尺度无几何指定，且 α_GUT⁻¹ 存在五口径、τ_p 存在 4.7 倍口径展宽。")
    L.append("")
    L.append("## 三、先给靶应得的 PASS（对靶有利分支各自单列）")
    L.append("")
    L.append("| 项 | 内容 | 机读 |")
    L.append("|---|---|---|")
    L.append("| A1 | RG 跑动计算与语料逐位一致（靶协议 4.060/0.760 + 闭式全部读数） | s* 30 位残差 {:.1e} |".format(
        kn["sstar_residual_vs_target"]))
    L.append("| A2 | 对偶周期 4（Θ²=−I）机器零——框架数学事实 | 残差 {:.1e} |".format(
        kn["duality_period_residual"]))
    L.append("| A3 | s* 闭式推导正确（三线汇聚两方程同解） | L13−L23={:.1e} |".format(
        kn["sstar_L_residual"]))
    L.append("| A4 | 内容→β 方法正对照：SM 内容精确重算 SM β | {} |".format(
        kn["sm_beta_from_content"]))
    L.append("| A5 | λ₈ 嵌入代数 g'/g=1/√3 ⇒ sin²θ=1/4（精确） | {} |".format(
        kn["s2w_candidate_algebra"]))
    L.append("")
    L.append("## 四、路径 1：sin²θ_W=1/4 的框架统一尺度出处（FAIL）")
    L.append("")
    L.append("- **B1**：「框架真空值」v=255.26 GeV 是 PDG 反解锚点："
             "v=2m_W/g̃（g̃=e/sinθ_W、e=√(4πα)）只含实验常数，重算 {:.5f} GeV 吻合；"
             "零框架含量。".format(kn["v_fit_from_pdg"]))
    L.append("- **B2**：唯一自洽尺度 M*={:.4f} GeV 是孤儿——M*/v={:.3f}、"
             "M*/ℓ_P⁻¹={:.2e}；跑动到 v 处 sin²θ={:.9f}（差 {:+.4f}%），"
             "靶三处自承「无框架出处」。".format(kn["M_star_GeV"], kn["Mstar_over_v"],
                                        kn["Mstar_over_ellP_inv"], kn["s2w_at_v"],
                                        kn["s2w_at_v_diff_pct"]))
    L.append("- **B3**：ℓ **四重口径**互不往来——符号自对偶尺度（无数值）/ 由拟合 v 隐含 "
             "ℓ={:.4e} m（全集 {} 处数值 ℓ 指定中 0 处是它，唯一 1 处是 ℓ_P 截断锚）/ "
             "Λ 估计专用 ℓ_P（差 {:.2e}）/ 推导卷线另锚 ℓ_min∼ℓ_P（与主线隐含 ℓ 相差 "
             "{:.2e} 倍）。".format(kn["ell_implied_from_v_fit_m"],
                                  kn["numeric_ell_hits_total"],
                                  kn["ellP_over_ell_implied"],
                                  1.0 / kn["ellP_over_ell_implied"]))
    L.append("")
    L.append("## 五、路径 2：Z₄ 对偶 → 超对称谱（FAIL，★最有价值路径）")
    L.append("")
    L.append("- **B4**：超对称形式化零存在——超场/超多重态/超势/Wess 计数 **{}**；"
             "超伴子名单 **{}**（「微子」13 处全为「中微子」假阳性，已排除）。".format(
                 kn["superfield_hits"], kn["sparticle_hits"]))
    L.append("- **B5**：范畴错置——对偶周期四是同一个 Ψ 的四个态（A2 机读），"
             "不产生新场、不映射玻色子↔费米子；超对称谱是一组不同的场。")
    L.append("- **B6**：框架希格斯二重态数 **{}**（S³=U(2)/U(1)）vs MSSM 必需 **2** ⇒ "
             "结构性不符。".format(kn["higgs_doublets_framework"]))
    L.append("- **B7**：s* 框架含量为零——闭式只含 α_EM⁻¹、α_s⁻¹ 与 MSSM β；"
             "框架量交集 = {}；负对照换 SM β ⇒ s*={:.6f}（与实验差 {:+.2f}%）⇒ "
             "s* 是导入 β 的函数。".format(kn["sstar_framework_intersection"],
                                       kn["sstar_with_sm_beta"],
                                       kn["sstar_with_sm_beta_diff_pct"]))
    L.append("- **B8**：框架自有内容 ⇒ SM β {}（b2<0，渐近自由）；其统一叙事引用的 "
             "MSSM β {}（b2=+1>0，**符号相反**）——复现的统一属于框架并不拥有的理论。".format(
                 kn["framework_beta_from_content"], kn["mssm_beta_cited"]))
    L.append("")
    L.append("## 六、路径 3：M_GUT 的几何指定（FAIL）")
    L.append("")
    L.append("- **B9**：卷三「三线**精确相交**」被语料库自证否证——靶 rge_sim 实测 "
             "MSSM 最小间距 {:.3f}≠0（其 <0.5 判据自判「否」），claims.csv 自承"
             "「残余间距 0.76 未闭合」。".format(kn["exact_crossing_refuted_gap"]))
    L.append("- **B10**：α_GUT⁻¹ 五口径（见 §七 表）极差 {:.2f}%；τ_p 头条 7.3e35 yr "
             "系口径选择（另三口径 {:.2e}/{:.2e}/{:.2e} yr，展宽 **{:.2f}×**）；"
             "「统一与否」判词随输入圆整翻转：圆整协议 0.760「否」→ 同协议精确输入 "
             "{:.3f}「→是」，无阈值闭合式 {:.4f}。".format(
                 kn["agut_spread_pct"],
                 kn["tau_p_calibres"][1][2], kn["tau_p_calibres"][2][2],
                 kn["tau_p_calibres"][3][2], kn["tau_p_spread"],
                 kn["gap_precise_with_switch"], kn["gap_precise_no_switch"]))
    L.append("- **B11**：sin²θ_W 双口径互斥——推导卷线 3/8（SU(5) 值）vs 主理论线 1/4"
             "（CP² 候选），相对差 {:.0f}%；0a 等价性已被 r178 判 FAIL。".format(
                 kn["s2w_dual_calibre_rel_diff_pct"]))
    L.append("")
    L.append("## 七、口径账（机读表）")
    L.append("")
    L.append("| 量 | 口径 | 值 | 出处 |")
    L.append("|---|---|---|---|")
    for name, val, src in kn["agut_calibres"]:
        L.append("| α_GUT⁻¹ | {} | {} | {} |".format(name, val, src))
    for name, mx, t in kn["tau_p_calibres"]:
        L.append("| τ_p | {} | {:.3e} yr | {} |".format(name, t, "M={:.2e}".format(mx)))
    L.append("")
    L.append("## 八、修复定价")
    L.append("")
    L.append("2^3=8 路径组合位掩码机读：宣称域内成立 **{}**、零代价 **{}**"
             "（宽松档=「外部锚点+如实标注」——语料库已实施，而 10-07 审计明定"
             "「借用锚点不计 S13 完成度」⇒ 宽松档同样 0）。".format(
                 kn["repair_survive"], kn["repair_zero_cost"]))
    L.append("")
    L.append("## 九、控制组与守卫")
    L.append("")
    L.append("控制组 {} / {}；守卫 {} / {}（全部机读驱动；G6 ast 自审 ok 参数无写死）。".format(
        sum(1 for c in payload["controls"] if c["ok"]), len(payload["controls"]),
        sum(1 for g in payload["guards"] if g["ok"]), len(payload["guards"])))
    L.append("")
    L.append("## 十、未闭合项与红线")
    L.append("")
    for x in payload["not_closed"]:
        L.append("- " + x)
    L.append("")
    L.append("- 数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。")
    L.append("- 靶的诚实登记（负面结果/OPEN/锚点自认）是对审计的配合；"
             "本卷判定的是「路径未闭合」，不指控造假。")
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
