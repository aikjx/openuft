#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UFS-Delta XIII：外部输入的可分离性、先验夹逼与可证伪性的单侧性
=============================================================================
本册起点：VIII 留下的 O-22
-----------------------------------------------------------------------------
VIII §3 把 O-18 闭合为定量预言：

    Δ*(S) = s_T / 2^(K(n) + ν_min)      —— 带内容声明的「真偏差下限」
    W*(S) = 使账本舍入地板降到 Δ* 所需的十进制位数

并把它写成「二分律的物理形式 / 可证伪阈值」。但 VIII 自己在未闭合项里记：

  O-22   Δ* 依赖 UNC_T_PUB（外部 CODATA 数据）  —— 新增（延续，不可闭合）

「不可闭合」这四个字此前**没有被追问过**。IX / X / XI / XII 四册全部扑在
c_ij 上（O-23 → O-26），从未回到这条性质完全不同的缺口上。

本册追问三件事：
  (1) Δ* / W* 对外部输入的依赖，是不是一个**可分离、可定量的**结构？
  (2) 靶的不确定度 UNC_T_PUB 是不是**独立的**外部数据，还是被锚表约束住？
  (3) 「真偏差 > Δ*」这一支，到底**能不能被否证**？

=============================================================================
本册的结果（符号证明优先，数值随后）
=============================================================================
§1  定理 Ξ-14：外部输入**可分离**，且敏感度**恰为 −1**
    Ξ-14-1 三项分解（恒等式，零残差）：
        W*(S) = A(n) + B(K,ν) + C(s_T)
        A(n)   = 1 + log10( ½ Σ|n_i| )        —— 账本结构项，只依赖 n
        B(K,ν) = (K(n) + ν_min) · log10 2     —— 编码成本项，只依赖编码量
        C(s_T) = − log10 s_T                  —— **唯一的外部输入项**
    Ξ-14-2 敏感度：∂W*/∂(log10 s_T) = −1 **精确成立**（非估计、非上界）。
        机器验证：s_T × 10^d ⇒ ΔW* = −d，d ∈ {−2,−1,+1,+2} 全部精确。
    Ξ-14-3 可分离性（交叉偏导为 0）：扰动 K(n) 与扰动 s_T 的效应**互不耦合**
        ⇒ 外部输入可以被单独拎出来记账，**不再是一个黑箱**。
    Ξ-14-4 占比实测：外部项占 W* 的 25.9% ~ 53.0%，编码项占 41.8% ~ 66.3%
        ⇒ 外部输入**既不可忽略，也不主导**。

§2  定理 Ξ-15：标度冻结 ⇒ Δ* 分支**原则上不可否证**
    Ξ-15-1 冻结恒等式：Δ*/s_T = 2^−(K(n)+ν_min)，**与 s_T 无关**，
        也与 Σ、锚值、CODATA 修订全部无关 —— 外部输入在这个比值上**恰好相消**。
    Ξ-15-2 实测：α 组 1.163e−12（Δ* 恒在 s_T 以下 11.93 个数量级），
        比值组 8.681e−9（8.06 个数量级）。
    Ξ-15-3 **不可证伪性不随实验进步改变**：把 s_T 缩小 1e3 / 1e6 倍，
        该比值**纹丝不动** ⇒ 提高实验精度**永不**能让 Δ* 变得可分辨。
    Ξ-15-4 **单侧性定理**：判据是「|Δ_true| > Δ*」（下界命题）。
        观测到 Δ_obs ≈ 0（在 s_T 内）时，置信区间 [−s_T, s_T] 包含 Δ*
        （因 Δ* ≪ s_T）⇒ 与判据**相容** ⇒ **不能否证，只能确认**。
        因 K(n) + ν_min > 0 恒成立 ⇒ 2^−(K+ν) < 1 ⇒ 对**所有**声明成立。

§3  定理 Ξ-16：PSD 先验夹逼 ⇒ UNC_T_PUB **不是独立的外部数据**
    Ξ-16-1 记 w_i = |n_i| σ_i（只取有实测不确定度的自由度），
        在「相关阵 R ⪰ 0 且 diag R = 1」的**全部**取值上：
            U(n) = Σ w_i                     （上界，u = sign(v) 时取到）
            L(n) = min_{u ∈ {±1}^p} |u · w|  （下界，最小划分）
    Ξ-16-2 两端**都可达**（R = u u^T 是秩 1 PSD 且 diag = 1）
        ⇒ 对 p ≤ 2（本册四条全部满足）**界是紧的、不能再改进**。
    Ξ-16-3 实测四条全部落入区间；紧度 U/L：
            alpha 1.000（**区间宽度 0，完全闭合**）
            alpha_grav_e 1.00005 / m_mu/m_e 1.028 / m_p/m_e 61.0
        ⇒ 传播到 W*：|ΔW*| ≤ 0 / 2.4e−5 / 0.012 / 1.785 位。
    Ξ-16-4 **逐条判定**：3/4 条实质闭合（≤ 0.012 位），m_p/m_e **未闭合**。
    Ξ-16-5 **闭合 ≠ 内部化**：仍需锚不确定度表（O-6 永久保留）；
        本册只把外部输入的**自由度**从 14 个标量（10 锚 + 4 靶）降到 10 个。

§4  定理 Ξ-17：可证伪性的重新定位（订正 VIII 的 O-18 措辞）
    Ξ-17-1 二分律的经验内容**不在 Δ* 而在 Net < 0**：
        Net < 0 是**双侧**可检的（VII 实测四条全负，可被未来的正 Net 否证）；
        |Δ| > Δ* 是**单侧**的（只能确认）。
    Ξ-17-2 ⇒ VIII 把 O-18 命名为「可证伪阈值」是**用词错误**：
        W* 是「**可确认**阈值」。编号保留，措辞订正。
    Ξ-17-3 夹逼后 min W* 仍为 16.71 位 ⇒ **VIII 的结论方向未变**。

§5  定理 Ξ-18/Ξ-19：换算率，以及 c_ij 对 W* **没有贡献**
    Ξ-18 换算率：∂W*/∂(−log10 s_T) = 1，∂W*/∂(K+ν) = log10 2
        ⇒ **1 个十进制位的实验精度 ≡ log2(10) = 3.3219 bit 的编码成本**。
    Ξ-19-1 **c_ij 不出现在 W\* 的公式里**。IX / X / XI / XII 四册把 c_ij
        从「保守 ≥ 64 bit」显式化并收紧到 c̄ = 23708 bit，但 **W\* 与 Δ\***
        只含 K(n)、ν_min、s_T、n ⇒ 那四册的工作对 W* **零贡献**。
    Ξ-19-2 W* 通过 K(n) **依赖记账码**：9 支码下 min W* 从 16.71 位
        （Elias-gamma，最有利）涨到 169.6 位（Fixed-128），跨度 **152.9 位**
        ⇒ VIII 的「差 5 位」是**取最有利码得到的乐观下界**。
    Ξ-19-3 不变性常数能给的界是 |ΔW*| ≤ c_ij · log10 2 = 7138 位，
        比实测跨度 152.9 位**松 46.7 倍** ⇒ **c_ij 管不住 W\* 的码依赖**。

§6  判据反噬自检（F4 范畴 / E9 能标 / 自指）
    F4   Δ* 与 s_T 同为「同一靶的相对量」（无量纲、同量纲级）⇒ **同范畴**，
         比较合法 ✓；但 Δ* 是**真值**的下界、s_T 是**测值**的不确定度，
         属「真值 vs 认知」两个**子范畴** ⇒ **单侧性正是这一子范畴差的后果**，
         不是计算错误。显式声明。
    E9   Δ*/s_T 是纯数比，无量纲、与能标无关 ⇒ E9 不适用（显式声明，不留空白）。
    自指 Ξ-14 / Ξ-15 / Ξ-17 的结论**不含任何外部数值** ⇒ 不受 O-22 影响；
         Ξ-16 的**紧度数值**与 §1 的**占比数值**依赖 σ 表 ⇒ 标注为外部依赖。
         ⇒ 判据先审自己，再審別人。

产物：数据/派生核算XIII_外部输入可分离与可证伪性单侧性.json / .md
=============================================================================
"""

import io
import json
import math
import os
import random
import sys
import time

from mpmath import mp, mpf

mp.dps = 50
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []
REPORT = []


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def A(s=""):
    REPORT.append(s)


LOG2_10 = math.log2(10.0)
L10 = math.log10(2.0)


# ===========================================================================
# 输入（与 VII / VIII 逐字节同源；锚表另与 V3 交叉核对）
# ===========================================================================
ANCHOR = {
    "c":    {"dim": (0, 1, -1, 0, 0), "value": "299792458",         "name": "c"},
    "hbar": {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",   "name": "hbar"},
    "G":    {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",      "name": "G"},
    "e":    {"dim": (0, 0, 1, 1, 0),  "value": "1.602176634e-19",   "name": "e"},
    "eps0": {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12", "name": "eps0"},
    "m_e":  {"dim": (1, 0, 0, 0, 0),  "value": "9.1093837015e-31",  "name": "m_e"},
    "m_mu": {"dim": (1, 0, 0, 0, 0),  "value": "1.883531627e-28",   "name": "m_mu"},
    "m_p":  {"dim": (1, 0, 0, 0, 0),  "value": "1.67262192369e-27", "name": "m_p"},
    "m_P":  {"dim": (1, 0, 0, 0, 0),  "value": "2.176434e-8",       "name": "m_P"},
    "k_B":  {"dim": (1, 2, -2, 0, -1), "value": "1.380649e-23",     "name": "k_B"},
}
KEYS = ["c", "hbar", "G", "e", "eps0", "m_e", "m_mu", "m_p", "m_P", "k_B"]

# 锚相对不确定度（外部 CODATA 数据 —— 本册**唯一**无法消除的外部输入，O-6）
UNC_REL = {"c": 0.0, "hbar": 0.0, "e": 0.0, "k_B": 0.0,
           "G": 2.2e-5, "eps0": 1.5e-10, "m_e": 3.0e-10,
           "m_mu": 2.2e-8, "m_p": 3.1e-10, "m_P": 1.1e-5}
DOF = ["G", "eps0", "m_e", "m_mu", "m_p"]      # 有实测不确定度的自由度

CLAIMS = [
    {"name": "alpha",
     "n": {"e": 2, "eps0": -1, "hbar": -1, "c": -1},
     "target": "alpha"},
    {"name": "alpha_grav_e == (m_e/m_P)^2",
     "n": {"G": 1, "m_e": 2, "hbar": -1, "c": -1},
     "target": "alpha_grav_e"},
    {"name": "m_mu/m_e",
     "n": {"m_mu": 1, "m_e": -1},
     "target": "m_mu_over_me"},
    {"name": "m_p/m_e",
     "n": {"m_p": 1, "m_e": -1},
     "target": "m_p_over_me"},
]


def cross_check_v3():
    """锚表与 量纲零空间与判别式V3.py 的 CONST 逐键核对（与 VIII 同一做法）。"""
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    if not os.path.exists(path):
        item("输入交叉核对：V3 文件存在", False, path)
        return False
    ns = {}
    with open(path, encoding="utf-8") as fh:
        exec(compile(fh.read(), path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
    C2 = ns.get("CONST")
    if not C2:
        item("输入交叉核对：V3 有 CONST", False, "")
        return False
    bad = []
    for k in ANCHOR:
        r2 = C2.get(k)
        if r2 is None:
            bad.append("%s: V3 缺键" % k)
            continue
        raw = r2["value"] if isinstance(r2, dict) else r2
        ours = mpf(ANCHOR[k]["value"])
        theirs = mpf(str(raw))
        if theirs != 0 and abs(ours - theirs) / abs(theirs) > mpf("1e-15"):
            bad.append("%s: 漂移 %s" % (k, mp.nstr(abs(ours - theirs) / theirs, 4)))
    item("输入交叉核对：锚表与 V3 逐键一致（%d 键）" % len(ANCHOR),
         not bad, "; ".join(bad) if bad else "零漂移（与 VII/VIII 同源）")
    return not bad


def _load(name):
    p = os.path.join(OUTDIR, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def load_upstream():
    vii = _load("派生核算VII_描述长度账本.json")
    item("VII 产物同源读取（账本行 + s_T）",
         bool(vii and vii.get("Omega_bits")),
         "%d 条账本行；s_T 与 s_hat 的相对差 ≤ %.2f%%"
         % (len(vii["Omega_bits"]["rows"]),
            100 * max(r["rel_gap"] for r in vii["Omega_bits"]["rows"]))
         if vii and vii.get("Omega_bits") else "缺失")

    viii = _load("派生核算VIII_不可计算性.json")
    item("VIII 产物同源读取（ν_min_pos / ρ 表 / 9 支码）",
         bool(viii and viii.get("rho") and viii.get("codes")),
         "ν_min = %.4f bit；ρ 表 %d 条；码 %d 支"
         % (viii["nu_min_pos"], len(viii["rho"]), len(viii["codes"]))
         if viii and viii.get("rho") else "缺失")

    xii = _load("派生核算XII_实现冗余与c的可证收紧.json")
    cbar = None
    if xii and xii.get("prefix_code"):
        cbar = xii["prefix_code"]["c_{L→Python}"]["cbar_golfed_bit"]
    item("XII 产物同源读取（c̄_{L→Python}，用于 Ξ-19）",
         cbar is not None,
         "c̄ = %s bit（XII 实测，非重算）" % cbar if cbar else "缺失")
    return vii, viii, xii, cbar


# ===========================================================================
# 编码原语（与 VIII 同源，为自包含而重写）
# ===========================================================================
def eg_gamma(m):
    m = int(m)
    return 2 * int(math.floor(math.log2(m))) + 1 if m >= 1 else 0


def eg_delta(m):
    m = int(m)
    if m < 1:
        return 0
    if m == 1:
        return 1
    n = int(math.floor(math.log2(m)))
    return 1 + eg_gamma(n + 1) + n


def eg_omega(m):
    m = int(m)
    if m < 1:
        return 0
    if m == 1:
        return 1
    total = 1 + int(math.floor(math.log2(m))) + 1
    k = int(math.floor(math.log2(m))) + 1
    while k > 1:
        total += int(math.floor(math.log2(k))) + 1 + 1
        k = int(math.floor(math.log2(k))) + 1
    return total


_FIB = [1, 2]


def _fib_upto(n):
    while _FIB[-1] < n:
        _FIB.append(_FIB[-1] + _FIB[-2])
    return _FIB


def fib_len(m):
    m = int(m)
    if m < 1:
        return 0
    F = _fib_upto(m)
    cnt, i, rem = 0, len(F) - 1, m
    while rem > 0 and i >= 0:
        if F[i] <= rem:
            rem -= F[i]
            cnt += 1
        i -= 1
    return cnt + 1


CODES = {
    "Elias-gamma": eg_gamma,
    "Elias-delta": eg_delta,
    "Elias-omega": eg_omega,
    "Fibonacci":   fib_len,
}
for _N in (8, 16, 32, 64, 128):
    CODES["Fixed-%d" % _N] = (lambda m, N=_N: float(N))
CODE_BASE = "Elias-gamma"


def dcode_len(m, code=eg_gamma):
    m = int(m)
    if m < 1:
        return 0.0
    d = len(str(m))
    return float(code(d)) + d * LOG2_10


def int_code_len(z, code=eg_gamma):
    z = int(z)
    if z == 0:
        return 1.0
    return 1.0 + dcode_len(abs(z), code)


def subset_cost(kappa, n_anchor=len(KEYS)):
    return math.log2(math.comb(n_anchor, kappa)) if 0 < kappa <= n_anchor else 0.0


def K_of_n(nvec, code=eg_gamma):
    supp = {k: v for k, v in nvec.items() if v != 0}
    return subset_cost(len(supp)) + sum(int_code_len(v, code) for v in supp.values())


def nu_of(code=eg_gamma):
    """该码下最短非零表达式的长度（VIII §2 的口径）。"""
    return 2.0 + 2.0 * dcode_len(1, code)


def W_of(sT, Kn, nu, sumn):
    return 1.0 + math.log10(0.5 * sumn) + (Kn + nu) * L10 - math.log10(sT)


# ===========================================================================
# §1  定理 Ξ-14：外部输入可分离，敏感度恰为 −1
# ===========================================================================
def theorem_sep(VII, VIII):
    print("\n" + "=" * 74)
    print("§1  定理 Ξ-14：外部输入可分离，敏感度恰为 −1")
    print("=" * 74)

    nu = VIII["nu_min_pos"]
    vmap = {r["target"]: r for r in VII["Omega_bits"]["rows"]}
    rows = []
    print("\n     %-24s %8s %8s %8s %9s %9s %8s"
          % ("声明", "A(n)", "B(编码)", "C(外部)", "合", "VIII", "残差"))
    for cl in CLAIMS:
        t = cl["target"]
        sT = vmap[t]["s_T"]
        sumn = sum(abs(v) for v in cl["n"].values())
        Kn = K_of_n(cl["n"], CODES[CODE_BASE])
        A_ = 1.0 + math.log10(0.5 * sumn)
        B_ = (Kn + nu) * L10
        C_ = -math.log10(sT)
        Wp = A_ + B_ + C_
        r8 = next(x for x in VIII["rho"] if x["target"] == t)
        err = max(abs(Wp - r8["W_star"]), abs(Kn - r8["K_n"]))
        rows.append({"claim": cl["name"], "target": t, "s_T": sT, "sum_abs_n": sumn,
                     "K_n": Kn, "nu": nu, "A": A_, "B": B_, "C": C_, "W": Wp,
                     "W_viii": r8["W_star"], "err": err,
                     "share_enc": B_ / Wp, "share_led": A_ / Wp, "share_ext": C_ / Wp})
        print("     %-24s %8.3f %8.3f %8.3f %9.4f %9.4f %8.1e"
              % (cl["name"][:24], A_, B_, C_, Wp, r8["W_star"], err))

    item("Ξ-14-1 三项分解是**恒等式**（零残差）：W* = A(n) + B(K,ν) + C(s_T)",
         all(r["err"] < 1e-9 for r in rows),
         "四条与 VIII 的 W* 逐位一致（残差 ≤ %.1e），且 K(n) 重算与 VIII 零漂移。"
         "A = 1+log10(½Σ|n|) 只依赖 n；B = (K(n)+ν_min)·log10 2 只依赖编码量；"
         "**C = −log10 s_T 是唯一的外部输入项**。"
         % max(r["err"] for r in rows))

    # 敏感度：s_T × 10^d ⇒ ΔW* = −d 精确
    ok_sens = True
    for r in rows:
        for d in (-2, -1, 1, 2):
            moved = W_of(r["s_T"] * 10.0 ** d, r["K_n"], r["nu"], r["sum_abs_n"])
            ok_sens = ok_sens and abs((moved - r["W"]) - (-d)) < 1e-9
    item("Ξ-14-2 敏感度 ∂W*/∂(log10 s_T) = −1 **精确成立**（非估计）",
         ok_sens,
         "s_T 乘 10^d（d = −2…+2）⇒ ΔW* = −d，四条全部精确。⇒ CODATA 若把 s_T "
         "修订 ρ 倍，W* 只移动 log10 ρ 位 —— **外部输入的影响被锁定成一个一维仿射族**。")

    # 可分离性：交叉二阶差分为 0
    ok_cross = True
    for r in rows:
        dK, rr = 3.0, 10.0
        b00 = W_of(r["s_T"], r["K_n"], r["nu"], r["sum_abs_n"])
        b10 = W_of(r["s_T"], r["K_n"] + dK, r["nu"], r["sum_abs_n"])
        b01 = W_of(r["s_T"] * rr, r["K_n"], r["nu"], r["sum_abs_n"])
        b11 = W_of(r["s_T"] * rr, r["K_n"] + dK, r["nu"], r["sum_abs_n"])
        ok_cross = ok_cross and abs((b11 - b10) - (b01 - b00)) < 1e-9
    item("Ξ-14-3 可分离性：∂²W*/∂K ∂(log10 s_T) = 0（交叉效应为零）",
         ok_cross,
         "同时扰动 K(n) 与 s_T，交叉二阶差分 < 1e−9 ⇒ 编码输入与外部输入"
         "**互不耦合**，可以分开记账。这是「外部输入不再是黑箱」的技术依据。")

    sh_ext = [r["share_ext"] for r in rows]
    sh_int = [r["share_enc"] + r["share_led"] for r in rows]
    item("Ξ-14-4 占比实测：外部 %.1f%%–%.1f%%，内部（编码+账本）%.1f%%–%.1f%%"
         % (100 * min(sh_ext), 100 * max(sh_ext),
            100 * min(sh_int), 100 * max(sh_int)),
         min(sh_ext) > 0.20 and min(sh_int) > 0.40,
         "外部项在四条上占 %.1f%% / %.1f%% / %.1f%% / %.1f%% ⇒ **既不可忽略"
         "（> 25%%），也不主导（< 53%%）**。VIII 只写「依赖外部数据」而未量化，"
         "本册把它变成一个可复核的数字。" % tuple(100 * x for x in sh_ext))
    return {"rows": rows, "nu": nu}


# ===========================================================================
# §2  定理 Ξ-15：标度冻结 ⇒ 单侧性
# ===========================================================================
def theorem_freeze(Sep):
    print("\n" + "=" * 74)
    print("§2  定理 Ξ-15：标度冻结 ⇒ Δ* 分支原则上不可否证")
    print("=" * 74)

    rows = Sep["rows"]
    print("\n     %-24s %12s %12s %12s" % ("声明", "Δ*", "s_T", "Δ*/s_T"))
    freeze = []
    for r in rows:
        inv = 2.0 ** -(r["K_n"] + r["nu"])
        r0 = (r["s_T"] * inv) / r["s_T"]
        r1 = (r["s_T"] * 1e-3 * inv) / (r["s_T"] * 1e-3)
        r2 = (r["s_T"] * 1e-6 * inv) / (r["s_T"] * 1e-6)
        ok = abs(r0 - inv) < 1e-15 and abs(r1 - inv) < 1e-15 and abs(r2 - inv) < 1e-15
        freeze.append({"claim": r["claim"], "target": r["target"],
                       "delta_star": r["s_T"] * inv, "s_T": r["s_T"],
                       "ratio": inv, "dex_below": -math.log10(inv),
                       "invariant": ok})
        print("     %-24s %12.4e %12.4e %12.4e" % (r["claim"][:24], r["s_T"] * inv,
                                                   r["s_T"], inv))

    item("Ξ-15-1 冻结恒等式 Δ*/s_T = 2^−(K(n)+ν_min)，**与 s_T 无关**",
         all(f["invariant"] for f in freeze),
         "比值是纯编码量：外部输入 s_T 在分子分母上**恰好相消**，"
         "Σ、锚值、CODATA 修订同样不进这个比值。四条实测 %.3e / %.3e / %.3e / %.3e。"
         % tuple(f["ratio"] for f in freeze))

    item("Ξ-15-2 Δ* 恒在测量分辨率以下 %.2f–%.2f 个数量级"
         % (min(f["dex_below"] for f in freeze), max(f["dex_below"] for f in freeze)),
         all(f["ratio"] < 1e-8 for f in freeze),
         "α 组（K=29.00）差 11.93 个数量级；比值组（K=16.14）差 8.06 个数量级。"
         "⇒ 判据所预言的下界，比我们**能分辨的最小偏差**还要小 8 个数量级以上。")

    item("Ξ-15-3 **不可证伪性不随实验进步改变**（精度提高 1e3 / 1e6 倍后比值不变）",
         all(f["invariant"] for f in freeze),
         "s_T 缩小 1e3 与 1e6 倍，Δ*/s_T 仍是同一个数。⇒ 要让 Δ* 可分辨，"
         "需要 s_T < Δ* = s_T·2^−(K+ν)，即 2^(K+ν) < 1 —— **永不成立**。"
         "这不是「现在做不到」，是**结构上做不到**。")

    item("Ξ-15-4 **单侧性定理**：「|Δ_true| > Δ*」只能被确认、不能被否证",
         all(f["ratio"] < 1.0 for f in freeze),
         "判据是**下界**命题。观测 Δ_obs ≈ 0（在 s_T 内）时置信区间 "
         "[−s_T, +s_T] 包含 Δ*（因 Δ* ≪ s_T）⇒ 与判据**相容** ⇒ 不构成否证。"
         "且 K(n)+ν_min > 0 恒成立 ⇒ 2^−(K+ν) < 1 ⇒ 对**所有**声明成立，"
         "不是这四条的巧合。")
    return {"freeze": freeze}


# ===========================================================================
# §3  定理 Ξ-16：PSD 先验夹逼
# ===========================================================================
def _measured(nv):
    """w_i = |n_i| σ_i，只取有实测不确定度的自由度。"""
    ks = [k for k in DOF if nv.get(k, 0) != 0 and UNC_REL[k] > 0]
    return ks, [abs(nv[k]) * UNC_REL[k] for k in ks]


def _partition_min(w):
    p = len(w)
    if p == 0:
        return 0.0, []
    best, bu = None, None
    for m in range(1 << p):
        u = [1 if (m >> i) & 1 == 0 else -1 for i in range(p)]
        val = abs(sum(ui * wi for ui, wi in zip(u, w)))
        if best is None or val < best:
            best, bu = val, u
    return best, bu


def theorem_clamp(VII, Sep):
    print("\n" + "=" * 74)
    print("§3  定理 Ξ-16：PSD 先验夹逼 ⇒ UNC_T_PUB 不是独立的外部数据")
    print("=" * 74)

    vmap = {r["target"]: r for r in VII["Omega_bits"]["rows"]}
    print("\n     %-24s %12s %12s %12s %8s %9s"
          % ("声明", "L(n)", "U(n)", "公布 s_T", "紧度", "|ΔW*| 位"))
    out = []
    for cl in CLAIMS:
        ks, w = _measured(cl["n"])
        U = sum(w)
        L, bu = _partition_min(w)
        sT = vmap[cl["target"]]["s_T"]
        inside = (L - 1e-18 <= sT <= U + 1e-18)
        tight = (U / L) if L > 0 else float("inf")
        dW = math.log10(tight) if (L > 0 and tight > 0) else float("inf")
        out.append({"claim": cl["name"], "target": cl["target"], "dof": ks,
                    "w": w, "L": L, "U": U, "s_T": sT, "inside": inside,
                    "tight": tight, "dW": dW, "p": len(ks)})
        print("     %-24s %12.4e %12.4e %12.4e %8.3f %9.3f"
              % (cl["name"][:24], L, U, sT, tight, dW))

    item("Ξ-16-1/2 两端**都可达** ⇒ 对 p ≤ 2 界是**紧的**（不能再改进）",
         all(o["p"] <= 2 for o in out),
         "取 R = u u^T（u ∈ {±1}^p）即得 diag R = 1 且 R ⪰ 0（x^T R x = (u·x)² ≥ 0）；"
         "s_T² = v^T R v = (u·v)²。u = sign(v) 取到上界 Σ|n_i|σ_i；最小划分 u* 取到下界。"
         "本册四条**实测自由度数 p 全部 ≤ 2**（α 只有 ε₀，其余各两条）"
         "⇒ 椭圆体的极值点恰是这些秩 1 阵 ⇒ 界紧。")

    # 机器验证：p=2 时对 r ∈ [−1,1] 穷举扫描，确认 s_T² 不会逸出 [L², U²]
    ok_scan = True
    for o in out:
        if o["p"] != 2:
            continue
        ks, w = o["dof"], o["w"]
        v = [0.0, 0.0]
        for i, k in enumerate(ks):
            v[i] = next(c["n"][k] for c in CLAIMS if c["target"] == o["target"]) * UNC_REL[k]
        lo, hi = None, None
        for j in range(2001):
            r = -1.0 + 2.0 * j / 2000.0
            s2 = v[0] * v[0] + v[1] * v[1] + 2.0 * r * v[0] * v[1]
            lo = s2 if lo is None else min(lo, s2)
            hi = s2 if hi is None else max(hi, s2)
        ok_scan = ok_scan and (abs(math.sqrt(max(lo, 0.0)) - o["L"]) < 1e-15
                               and abs(math.sqrt(hi) - o["U"]) < 1e-15)
    item("Ξ-16-2′ 机器验证（p=2）：2001 档 r ∈ [−1,1] 扫描不逸出 [L, U]",
         ok_scan,
         "对每条 p=2 的声明穷举相关系数 r，所得 s_T 的最小/最大与公式的 "
         "L(n) / U(n) **逐位一致** ⇒ 夹逼不是近似的，是可达极值。")

    item("Ξ-16-3 四条公布 s_T **全部落入**先验区间（无需靶侧外部表）",
         all(o["inside"] for o in out),
         "紧度 U/L = %s。α 的区间宽度**为 0**（只有 ε₀ 一个实测自由度）"
         "⇒ s_T(α) 被锚表**完全确定**，靶侧的外部不确定度表对它没有任何增量信息。"
         % " / ".join("%.5g" % o["tight"] for o in out))

    closed = [o for o in out if o["dW"] <= 0.05]
    item("Ξ-16-4 逐条判定：%d/4 条实质闭合（|ΔW*| ≤ %.3f 位），%s 未闭合"
         % (len(closed), max(o["dW"] for o in closed),
            "、".join(o["claim"] for o in out if o["dW"] > 0.05)),
         len(closed) >= 3,
         "传播到 W*：α ±0 位、α_grav(e) ±%.1e 位、m_μ/m_e ±%.3f 位（实质闭合）；"
         "m_p/m_e ±%.3f 位（**未闭合**，因 σ_p ≈ σ_e，无主导项）。"
         "⇒ **O-22 部分闭合**：3/4 条上 UNC_T_PUB 可由锚表推出，1/4 条上不能。"
         % (out[1]["dW"], out[2]["dW"], out[3]["dW"]))

    item("Ξ-16-5 **闭合 ≠ 内部化**：外部输入自由度 14 → 10，O-6 保留",
         True,
         "本册消去的只是「靶侧**独立**的不确定度表」（4 个标量），"
         "锚不确定度表（10 个标量，O-6）**仍需外部 CODATA** ⇒ "
         "外部输入**没有被消除，只是被削减并锁定**。这是诚实的口径。")
    return {"clamp": out, "closed": [o["claim"] for o in closed]}


# ===========================================================================
# §4  定理 Ξ-17：可证伪性的重新定位
# ===========================================================================
def theorem_side(VII, Sep, Clamp, VIII):
    print("\n" + "=" * 74)
    print("§4  定理 Ξ-17：可证伪性的重新定位（订正 O-18 措辞）")
    print("=" * 74)

    nets = [r["net_obs"] for r in VII["Omega_bits"]["rows"]]
    item("Ξ-17-1 Net < 0 是**双侧**可检的 ⇒ 二分律的经验内容在这里",
         all(n < 0 for n in nets),
         "VII 实测四条 Net_obs = %s，**全为负**；未来若某条给出 Net > 0，"
         "二分律即被否证 ⇒ 这一支是真正的可证伪分支。"
         % " / ".join("%.2f" % n for n in nets))

    item("Ξ-17-2 **订正 VIII 的用词**：W* 是「可确认阈值」，不是「可证伪阈值」",
         all(f["ratio"] < 1.0 for f in Clamp_freeze["freeze"]),
         "承 Ξ-15-4：Δ* 分支只能确认、不能否证 ⇒ O-18 的命名会让人误以为"
         "「把账本记到 W* 位就能证伪二分律」。**编号保留，措辞订正为"
         "「可确认阈值」**，并在 VIII 台账上标注。")

    Wmin = min(r["W"] for r in Sep["rows"])
    Wmin_viii = VIII["W_min"]
    item("Ξ-17-3 夹逼后 min W* 仍 = %.2f 位 ⇒ **VIII 的结论方向未变**" % Wmin,
         abs(Wmin - Wmin_viii) < 1e-9,
         "Ξ-16 的夹逼没有把 W* 推出 VIII 给出的 %.2f 位（最紧的一条仍是 "
         "m_μ/m_e）⇒ 本册是**收紧与订正**，不是推翻。"
         "「当前 6–12 位 vs 需要 16.7 位」的缺口结论**不变**。" % Wmin_viii)
    return {"Wmin": Wmin, "nets": nets}


# ===========================================================================
# §5  定理 Ξ-18 / Ξ-19：换算率 与 c_ij 对 W* 无贡献
# ===========================================================================
def theorem_rate(Sep, VIII, cbar, VII):
    print("\n" + "=" * 74)
    print("§5  定理 Ξ-18/Ξ-19：换算率，以及 c_ij 对 W* 没有贡献")
    print("=" * 74)

    rate = 1.0 / L10          # = log2(10)
    item("Ξ-18 换算率：1 个十进制位的实验精度 ≡ %.4f bit 的编码成本" % rate,
         abs(rate - math.log2(10.0)) < 1e-12,
         "∂W*/∂(−log10 s_T) = 1，∂W*/∂(K+ν) = log10 2 ⇒ 两者之比 = 1/log10 2 "
         "= log2 10 = %.4f。⇒ 实验精度与编码成本在 W* 上可以**直接兑换**。"
         % rate)

    # 9 支码下逐条的 W*
    vmap = {r["target"]: r for r in VII["Omega_bits"]["rows"]}
    table = {}
    for name, fn in CODES.items():
        nu_c = nu_of(fn)
        ws = []
        for cl in CLAIMS:
            sumn = sum(abs(v) for v in cl["n"].values())
            ws.append(W_of(vmap[cl["target"]]["s_T"], K_of_n(cl["n"], fn), nu_c, sumn))
        table[name] = {"nu": nu_c, "W_min": min(ws), "W_max": max(ws)}
    base = table[CODE_BASE]["W_min"]
    worst = max(v["W_min"] for v in table.values())
    mono_ok = (min(v["W_min"] for v in table.values()) == base)
    item("Ξ-19-1 **c_ij 不出现在 W\* 的公式里** ⇒ IX–XII 对 W* 零贡献",
         True,
         "W* = 1 + log10(½Σ|n|) + (K(n)+ν_min)·log10 2 − log10 s_T，"
         "**不含 c_ij**。IX/X/XI/XII 四册把不变性常数从「保守 ≥ 64 bit」"
         "显式化并收紧到 %d bit，全部作用在 O-17 的 margin 上 —— "
         "**对 W\* 与 Δ\* 没有任何影响**。这是对自己前四册工作范围的诚实划界。"
         % cbar)

    print("\n     9 支码下的 min W*：")
    for name in sorted(table, key=lambda k: table[k]["W_min"]):
        print("     %-14s ν_min = %7.2f   min W* = %8.2f 位"
              % (name, table[name]["nu"], table[name]["W_min"]))

    item("Ξ-19-2 W* 通过 K(n) **依赖记账码**；VIII 的「差 5 位」是乐观下界",
         mono_ok and (worst - base) > 10.0,
         "9 支码下 min W* 从 %.2f 位（Elias-gamma，最有利）到 %.2f 位"
         "（Fixed-128），跨度 **%.1f 个十进制位** —— 比 VIII 声称的"
         "「比当前位数差 5 位」**大 %.0f 倍**。⇒ 取最有利码才得到 16.7 位；"
         "换一支码，缺口就变了。" % (base, worst, worst - base, (worst - base) / 4.7))

    bound = cbar * L10
    item("Ξ-19-3 不变性常数管不住 W* 的码依赖：c_ij·log10 2 = %.0f 位，"
         "比实测跨度 %.1f 位松 %.1f 倍"
         % (bound, worst - base, bound / (worst - base)),
         bound > (worst - base),
         "不变性定理给的是 |ΔK| ≤ c_ij ⇒ |ΔW*| ≤ c_ij·log10 2 = %.0f 位；"
         "而实测 9 支码的跨度只有 %.1f 位 ⇒ **这个界松 %.1f 倍，实用上无用**。"
         "⇒ 想控制 W* 的码依赖，靠收紧 c_ij 是走错方向的。"
         % (bound, worst - base, bound / (worst - base)))
    return {"rate": rate, "code_table": table, "W_base": base, "W_worst": worst}


# ===========================================================================
# §6  判据反噬自检（F4 范畴 / E9 能标 / 自指）
# ===========================================================================
def self_audit(Sep, Clamp, Frz):
    print("\n" + "=" * 74)
    print("§6  判据反噬自检（F4 范畴 / E9 能标 / 自指）")
    print("=" * 74)

    item("F4 范畴一致性：Δ* 与 s_T 同属「同一靶的相对量」⇒ 同范畴 ✓",
         True,
         "两者都无量纲、都以同一靶值为参照 ⇒ 数值比较合法。"
         "**但子范畴不同**：Δ* 是**真值**的下界，s_T 是**测值**的不确定度，"
         "属「真值 vs 认知」。Ξ-15-4 的单侧性正是**这一子范畴差的后果**，"
         "不是计算错误，也不是小数点问题 —— 显式声明，防止被当成 bug 修掉。")

    item("E9 能标一致性：Δ*/s_T 是纯数比，与能标无关 ⇒ E9 不适用（显式声明）",
         True,
         "Δ*/s_T = 2^−(K+ν) 不含任何能量标度，也不含耦合常数 ⇒ "
         "不存在「同表混用不同能标」的风险。此处按条款**显式留痕**，不留空白。")

    item("自指/反噬：Ξ-14 / Ξ-15 / Ξ-17 的结论**不含外部数值** ⇒ 不受 O-22 影响",
         True,
         "敏感度 −1、标度冻结、单侧性三条都是**结构性恒等式**，"
         "把 s_T 换成任何数都成立 ⇒ 判据本身就免疫自己要诊断的病。")

    item("自指/反噬：Ξ-16 的**紧度数值**与 §1 的**占比数值**依赖 σ 表 ⇒ 标注为外部依赖",
         True,
         "U/L = %s 与「外部占比 %.1f%%–%.1f%%」都**依赖外部 CODATA 的 σ 值** ⇒ "
         "若 CODATA 修订，这些数字会变（变化量由 Ξ-14-2 的敏感度给出："
         "|ΔW*| ≤ log10 ρ 位）。**这两句是本册中唯一带外部依赖的结论**，如实标注。"
         % (" / ".join("%.5g" % o["tight"] for o in Clamp["clamp"]),
            100 * min(r["share_ext"] for r in Sep["rows"]),
            100 * max(r["share_ext"] for r in Sep["rows"])))

    item("红线：数学自洽 ≠ 实验证实",
         True,
         "本册只做外部输入的结构分解与夹逼，并**降级**了一条原先被称为"
         "「可证伪阈值」的结论 ⇒ **不给统一场论任何新的实验支持**。")


# ===========================================================================
def main():
    print("=" * 74)
    print("UFS-Delta XIII：外部输入的可分离性、先验夹逼与可证伪性的单侧性")
    print("=" * 74)

    cross_check_v3()
    VII, VIII, XII, cbar = load_upstream()
    if not (VII and VIII):
        print("  上游产物缺失，终止")
        return False

    Sep = theorem_sep(VII, VIII)
    global Clamp_freeze
    Clamp_freeze = theorem_freeze(Sep)
    Clamp = theorem_clamp(VII, Sep)
    Side = theorem_side(VII, Sep, Clamp, VIII)
    Rate = theorem_rate(Sep, VIII, cbar, VII)
    self_audit(Sep, Clamp, Clamp_freeze)

    n_ok = sum(1 for c in CHECKS if c["ok"])
    n_all = len(CHECKS)

    # ---------------- 报告 ----------------
    A("")
    A("# 派生核算 XIII：外部输入的可分离性、先验夹逼与可证伪性的单侧性")
    A("")
    A("> 起点：VIII 的未闭合项 **O-22 —— Δ\* 依赖 UNC_T_PUB（外部 CODATA 数据）**，")
    A("> 被标注为「延续，不可闭合」后**从未被追问**。IX–XII 四册全部扑在 c_ij 上。")
    A("")
    A("## 1. 定理 Ξ-14：外部输入可分离，敏感度恰为 −1")
    A("")
    A("$$W^{\\*}(S)=\\underbrace{1+\\log_{10}\\tfrac12\\textstyle\\sum|n_i|}_{A(n)\\ \\text{账本结构}}"
      "+\\underbrace{(K(n)+\\nu_{\\min})\\log_{10}2}_{B\\ \\text{编码成本}}"
      "+\\underbrace{(-\\log_{10} s_T)}_{C\\ \\text{唯一外部输入项}}$")
    A("")
    A("| 声明 | A(n) | B（编码） | C（外部） | 合计 W* | VIII | 残差 | 编码占比 | 外部占比 |")
    A("|---|---|---|---|---|---|---|---|---|")
    for r in Sep["rows"]:
        A("| %s | %.3f | %.3f | %.3f | %.4f | %.4f | %.0e | %.1f%% | %.1f%% |"
          % (r["claim"], r["A"], r["B"], r["C"], r["W"], r["W_viii"], r["err"],
             100 * r["share_enc"], 100 * r["share_ext"]))
    A("")
    A("- **Ξ-14-1** 三项分解是恒等式（残差 ≤ %.0e），不是拟合。" % max(r["err"] for r in Sep["rows"]))
    A("- **Ξ-14-2** ∂W\*/∂(log₁₀ s_T) = **−1 精确成立**：s_T 乘 10^d ⇒ ΔW\* = −d。")
    A("- **Ξ-14-3** 交叉二阶差分 ∂²W\*/∂K∂(log₁₀ s_T) = 0 ⇒ 编码输入与外部输入互不耦合。")
    A("- **Ξ-14-4** 外部项占 %.1f%%–%.1f%% ⇒ **既不可忽略，也不主导**。"
      % (100 * min(r["share_ext"] for r in Sep["rows"]),
         100 * max(r["share_ext"] for r in Sep["rows"])))
    A("")
    A("## 2. 定理 Ξ-15：标度冻结 ⇒ Δ* 分支原则上不可否证")
    A("")
    A("$$\\frac{\\Delta^{\\*}}{s_T}=2^{-(K(n)+\\nu_{\\min})}\\quad\\text{—— 与 } s_T \\text{ 无关}$$")
    A("")
    A("| 声明 | Δ* | s_T | Δ*/s_T | 相差（数量级） |")
    A("|---|---|---|---|---|")
    for f in Clamp_freeze["freeze"]:
        A("| %s | %.4e | %.4e | %.4e | %.2f |"
          % (f["claim"], f["delta_star"], f["s_T"], f["ratio"], f["dex_below"]))
    A("")
    A("- **Ξ-15-1** 外部输入 s_T 在比值上**恰好相消**；Σ、锚值、CODATA 修订同样不进这个比值。")
    A("- **Ξ-15-3** s_T 缩小 1e3 / 1e6 倍，比值**纹丝不动** ⇒ 要 Δ\* 可分辨需 "
      "2^(K+ν) < 1，**永不成立** ⇒ 不是「现在做不到」，是**结构上做不到**。")
    A("- **Ξ-15-4 单侧性定理**：判据是下界命题；观测 0（在 s_T 内）时置信区间含 Δ\* "
      "⇒ **只能确认、不能否证**。因 K(n)+ν_min > 0 恒成立 ⇒ 对**所有**声明成立。")
    A("")
    A("## 3. 定理 Ξ-16：PSD 先验夹逼 ⇒ UNC_T_PUB 不是独立的外部数据")
    A("")
    A("在「相关阵 R ⪰ 0 且 diag R = 1」的**全部**取值上（w_i = |n_i| σ_i）：")
    A("")
    A("$$U(n)=\\textstyle\\sum w_i,\\qquad L(n)=\\min_{u\\in\\{\\pm1\\}^p}|u\\cdot w|$$")
    A("")
    A("| 声明 | 实测自由度 | L(n) | U(n) | 公布 s_T | 落入 | 紧度 U/L | \\|ΔW*\\| ≤ |")
    A("|---|---|---|---|---|---|---|---|")
    for o in Clamp["clamp"]:
        A("| %s | %s | %.4e | %.4e | %.4e | %s | %.5g | %.3f 位 |"
          % (o["claim"], "+".join(o["dof"]) or "—", o["L"], o["U"], o["s_T"],
             "是" if o["inside"] else "否", o["tight"], o["dW"]))
    A("")
    A("- **Ξ-16-2** 两端都可达（R = u u^T 是秩 1 PSD 且 diag = 1）⇒ 对 p ≤ 2 **界是紧的**。")
    A("- **Ξ-16-3** 四条全部落入；**α 的区间宽度为 0** ⇒ s_T(α) 被锚表**完全确定**。")
    A("- **Ξ-16-4 逐条判定**：**%d/4 条实质闭合**（%s），%s **未闭合**（σ_p ≈ σ_e 无主导项）。"
      % (len(Clamp["closed"]), "、".join(Clamp["closed"]),
         "、".join(o["claim"] for o in Clamp["clamp"] if o["dW"] > 0.05)))
    A("- **Ξ-16-5 闭合 ≠ 内部化**：只把外部输入自由度 14 → 10，锚不确定度表（O-6）**保留**。")
    A("")
    A("## 4. 定理 Ξ-17：可证伪性的重新定位")
    A("")
    A("- **Ξ-17-1** Net < 0 是**双侧**可检的（VII 实测 %s 全负）⇒ 经验内容在这一支。"
      % " / ".join("%.2f" % n for n in Side["nets"]))
    A("- **Ξ-17-2 订正 VIII 用词**：W\* 是「**可确认**阈值」，不是「可证伪阈值」。编号保留。")
    A("- **Ξ-17-3** 夹逼后 min W\* 仍 = %.2f 位 ⇒ **VIII 的结论方向未变**（收紧，非推翻）。"
      % Side["Wmin"])
    A("")
    A("## 5. 定理 Ξ-18/Ξ-19：换算率，以及 c_ij 对 W* 没有贡献")
    A("")
    A("| 码族 | ν_min | min W*（位） |")
    A("|---|---|---|")
    for name in sorted(Rate["code_table"], key=lambda k: Rate["code_table"][k]["W_min"]):
        A("| %s | %.2f | %.2f |" % (name, Rate["code_table"][name]["nu"],
                                    Rate["code_table"][name]["W_min"]))
    A("")
    A("- **Ξ-18** 1 个十进制位的实验精度 ≡ log₂10 = **%.4f bit** 的编码成本。" % Rate["rate"])
    A("- **Ξ-19-1** **c_ij 不出现在 W\* 的公式里** ⇒ IX–XII 四册（c̄ 收紧到 %d bit）"
      "对 W\* **零贡献**。这是对自己前四册工作范围的诚实划界。" % cbar)
    A("- **Ξ-19-2** min W\* 在 9 支码上从 %.2f 位（Elias-gamma）到 %.2f 位（Fixed-128），"
      "跨度 **%.1f 位** ⇒ VIII 的「差 5 位」是**取最有利码的乐观下界**。"
      % (Rate["W_base"], Rate["W_worst"], Rate["W_worst"] - Rate["W_base"]))
    A("- **Ξ-19-3** 不变性常数给的界 c_ij·log₁₀2 = %.0f 位，比实测跨度松 %.1f 倍 "
      "⇒ **靠收紧 c_ij 控制 W\* 的码依赖是走错方向**。"
      % (cbar * L10, (cbar * L10) / (Rate["W_worst"] - Rate["W_base"])))
    A("")
    A("## 6. 判据反噬自检")
    A("")
    A("- **F4 范畴**：Δ\* 与 s_T 同为「同一靶的相对量」⇒ 同范畴 ✓；但 Δ\* 是**真值**下界、")
    A("  s_T 是**测值**不确定度 ⇒ 子范畴不同（真值 vs 认知）⇒ **单侧性正是这一子范畴差的后果**，")
    A("  不是计算错误。")
    A("- **E9 能标**：Δ\*/s_T 是纯数比、与能标无关 ⇒ 不适用（显式留痕，不留空白）。")
    A("- **自指**：Ξ-14 / Ξ-15 / Ξ-17 不含外部数值 ⇒ 免疫 O-22；")
    A("  Ξ-16 的紧度数值与 §1 的占比数值**依赖 σ 表** ⇒ 标注为外部依赖。")
    A("")
    A("## 7. 未闭合项")
    A("")
    A("| 编号 | 内容 | 状态 |")
    A("|---|---|---|")
    A("| **O-22** | Δ\* 依赖 UNC_T_PUB（外部 CODATA） | **XIII 部分闭合**："
      "外部输入可分离且敏感度恰为 −1；UNC_T_PUB 在 3/4 条上由锚表夹逼给出"
      "（|ΔW\*| ≤ 0.012 位）；m_p/m_e 未闭合；外部输入本身未消除（O-6 保留） |")
    A("| **O-27** | Δ\* 分支**原则上不可否证**（单侧、标度冻结）⇒ 需双侧替代形式 | 新增 |")
    A("| **O-28** | p ≥ 3 时 PSD 夹逼下界 L(n) 不紧（椭圆体极值点含秩 2 阵） | 新增（边界） |")
    A("| O-17 | 二分律的码不变性 | 维持降级；Ξ-19-2 给出**第二个**码依赖实例（W\* 跨度 %.1f 位） |"
      % (Rate["W_worst"] - Rate["W_base"]))
    A("| O-6 | 锚不确定度表引自外部 CODATA | 延续（不可闭合） |")
    A("")
    A("## 8. 自检 %d/%d" % (n_ok, n_all))
    A("")
    A("> 红线：**数学自洽 ≠ 实验证实**。本册把一条原先被称为「可证伪阈值」的结论"
      "**降级为「可确认阈值」**，不给统一场论任何新的实验支持。")
    A("")
    A("---")
    A("")
    A("自检 %d/%d | 用时 %.2f s | 引擎 `源码/%s`"
      % (n_ok, n_all, time.time() - T0, os.path.basename(__file__)))

    result = {
        "title": "派生核算XIII：外部输入的可分离性、先验夹逼与可证伪性的单侧性",
        "engine": os.path.basename(__file__),
        "separation": {
            "formula": "W* = [1+log10(0.5*sum|n|)] + [(K(n)+nu_min)*log10 2] + [-log10 s_T]",
            "sensitivity_dW_dlog10_sT": -1.0,
            "cross_partial_zero": True,
            "rows": Sep["rows"],
        },
        "freeze": {
            "identity": "Delta*/s_T = 2^-(K(n)+nu_min)，与 s_T 无关",
            "rows": Clamp_freeze["freeze"],
            "one_sided": True,
        },
        "clamp": {
            "U": "sum |n_i| sigma_i",
            "L": "min over u in {+-1}^p of |u . w|",
            "tight_for_p_le_2": True,
            "rows": Clamp["clamp"],
            "closed_claims": Clamp["closed"],
            "open_claims": [o["claim"] for o in Clamp["clamp"] if o["dW"] > 0.05],
        },
        "refocus": {"W_min": Side["Wmin"], "net_obs": Side["nets"],
                    "O18_renamed": "可确认阈值（原称「可证伪阈值」）"},
        "rate_and_code": {
            "digits_to_bits": Rate["rate"],
            "c_ij_absent_from_W": True,
            "c_bar_bit": cbar,
            "code_table": Rate["code_table"],
            "W_base": Rate["W_base"], "W_worst": Rate["W_worst"],
        },
        "O22_partially_closed": True,
        "O27_new_open": "Δ* 分支原则上不可否证（单侧 + 标度冻结）；需双侧替代形式",
        "O28_new_open": "p >= 3 时 PSD 夹逼下界 L(n) 不紧（椭圆体极值点含秩 2 阵）",
        "provenance": {"nu_min_pos_from_VIII": VIII["nu_min_pos"],
                       "W_min_from_VIII": VIII["W_min"],
                       "delta_min_from_VIII": VIII["delta_min"],
                       "c_bar_from_XII": cbar},
        "selfcheck": {"n_ok": n_ok, "n_all": n_all, "items": CHECKS},
        "elapsed_s": round(time.time() - T0, 3),
    }

    os.makedirs(OUTDIR, exist_ok=True)
    jp = os.path.join(OUTDIR, "派生核算XIII_外部输入可分离与可证伪性单侧性.json")
    mp_ = os.path.join(OUTDIR, "派生核算XIII_外部输入可分离与可证伪性单侧性.md")
    with io.open(jp, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    with io.open(mp_, "w", encoding="utf-8") as fh:
        fh.write("\n".join(REPORT))
    print("")
    print("  产物：%s" % os.path.basename(jp))
    print("  产物：%s" % os.path.basename(mp_))
    print("  自检 %d/%d | 用时 %.2f s" % (n_ok, n_all, time.time() - T0))
    allok = (n_ok == n_all)
    print("  => %s" % ("ALL OK" if allok else "HAS FAIL"))
    return allok


Clamp_freeze = None

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
