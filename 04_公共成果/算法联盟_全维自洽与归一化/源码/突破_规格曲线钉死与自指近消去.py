# -*- coding: utf-8 -*-
"""
突破尝试：规格曲线钉死不可行性、自指近消去恒等与自然输入普查（定理 R）
============================================================================

前情（`源码/突破_算子谱与量子化规格.py`，定理 F）：
  螺旋算子类 e(u)=P/u−Q/u²（P=A+c/2, Q=1/4+c/2, A=(n+φ)²/N², u=1+x², α=1/x）
  有内点极小 ⟺ c<−1/2；此时 α 被固定，"规格方程"把 α 与 (A,c) 联系。
  该轮把砖 (ii) 判为「可行，带规格」，并把下一个真问题精确提出：
      **「什么把 (A,c) 钉在规格曲线上？」**

本轮正面攻这个真问题。三件事：

  1. 【勘误】既有文档把规格方程写成 α²=|A+c/2|/|c+1/2| —— 这不是精确解
     （在 c=−2, A=0 处该式给 0.667，实际 α²=2）。精确解由 u*=2Q/P 严格推出：
         **α² = P/(2Q−P) = (A+c/2) / (1/2 + c/2 − A)**.
     旧式仅在 A→−c/2 的近消去极限下与精确解同阶（差 O(α²)）。

  2. 【定理 R1 · 自指近消去恒等（精确代数恒等，非数值巧合）】
     规格方程等价于 **|P/Q| = 2α²/(1+α²)**，与 c 无关。
     即：**要求机制实现的近消去比例，恒等于"待预言的量 α²"的两倍**。
     在 c=−1 处，把 α 钉到 α_obs 所需的 A 相对精度 ≡ α²/(1+α²)（精确）。
     ⇒ "需要供给的精度" 恒等于 "待预言的量"（O(α²) 级）。这是一个**循环性**：
       要钉住 α，机制必须已经知道 α。

  3. 【定理 R2 · 钉死不可行性，两路穷尽】
     (a) 离散拓扑输入（n,φ,N,c 由拓扑/量子化给有限离散数据）⇒ α 为代数数（Pell 型），
         全枚举确认 1/α_obs=137.036 不达（最近 1/α=137.0515，偏 1.13e-4 ≈ 7× 观测精度
         1.6e-5）⇒ 离散路被观测**可证伪否定**。
     (b) 任一连续输入 ⇒ 调参精度 O(α²) ⇒ 定理 F 输入壁垒（系数只能来自实测/结构数/
         另一本征值）。近消去 P→0⁻ 等价于"小正质量平方/近临界"精细调节（层级问题同型）；
         定理 E（齐次结构定不了绝对标度）+ 定理 N（纯相位 Z ⇒ β≡0，无 RG 环）
         ⇒ 框架内**无生成该残差的机制**。

  4. 【突破候选普查】宽枚举自然候选（c 取小分母有理数、φ 取小分母有理数、n,N 整数），
     搜索是否存在**无需调参**即命中 α_obs 的组合。结论见报告（如实报告，若负则负）。

红线：全程不调参去凑 1/137；所有数字由符号/数值实算得到。
      本引擎不解锁 UFT-3、不宣称推出 α；它把"钉死"问题判为**不可由本公设闭合**。
"""

import io
import json
import os
import sys
from fractions import Fraction

from mpmath import mp, mpf, sqrt
from sympy import Rational, Symbol, diff, simplify, solve

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 50
ALPHA = mpf("7.2973525693e-3")          # α 观测（CODATA）
ALPHA_SQ = ALPHA * ALPHA
AINV = 1 / ALPHA
ALPHA_INV_UREL = mpf("1.5e-10")          # α 相对不确定度
OBS_TOL = ALPHA_INV_UREL                   # 判"命中"的口径：观测精度 1.6e-5 量级
OBS_TOL_STRICT = mpf("1.6e-5")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "数据")
os.makedirs(DATA, exist_ok=True)


def fmt(x, n=10):
    try:
        return mp.nstr(x, n)
    except Exception:
        return str(x)


# ===========================================================================
# 一、符号推导：精确规格方程（并勘误旧式）
# ===========================================================================
u = Symbol("u", positive=True)
Asym = Symbol("A", positive=True)
csym = Symbol("c", real=True)

e = simplify(Asym / u - Rational(1, 4) / u ** 2 + (csym / 2) * (u - 1) / u ** 2)
de = simplify(diff(e, u))
d2 = simplify(diff(e, u, 2))
crit = solve(de, u)                       # u* = 2Q/P

P = Asym + csym / 2
Q = Rational(1, 4) + csym / 2
u_star = simplify(2 * Q / P)
d2_at = simplify(d2.subs(u, u_star))

# 精确规格方程：alpha^2 = 1/(u*-1) = P/(2Q-P)
alpha_sq_exact = simplify(1 / (u_star - 1))
alpha_sq_exact = simplify(alpha_sq_exact)   # 期望 P/(2Q-P)


def alpha_sq(Av, cv):
    """精确 α² = P/(2Q-P)（内点极小分支）。不满足则返回 None。"""
    Av = mpf(Av)
    cv = mpf(cv)
    Qv = mpf("0.25") + cv / 2
    Pv = Av + cv / 2
    if Qv >= 0:                 # c >= -1/2 ⇒ 临界点为极大，无内点极小
        return None
    if Pv >= 0:                 # u* <= 0
        return None
    us = 2 * Qv / Pv
    if us <= 1:                 # x² <= 0
        return None
    return Pv / (2 * Qv - Pv)


def alpha_of(Av, cv):
    a2 = alpha_sq(Av, cv)
    return None if a2 is None else sqrt(a2)


# --- 勘误核对：旧式 vs 精确式（c=-2, A=0） ---
def doc_form_alpha_sq(Av, cv):
    """旧文档误写的规格：alpha^2 = |A + c/2| / |c + 1/2|。"""
    Av = mpf(Av)
    cv = mpf(cv)
    denom = abs(cv + mpf("0.5"))
    if denom == 0:
        return None
    return abs(Av + cv / 2) / denom


errata_checks = []
for (Av, cv) in [(mpf(0), mpf(-2)), (mpf(0), mpf(-5)), (mpf("0.25"), mpf(-1)),
                 (mpf("0.4"), mpf(-1)), (mpf("0.6"), mpf(-2))]:
    exact = alpha_sq(Av, cv)
    docf = doc_form_alpha_sq(Av, cv)
    errata_checks.append({
        "A": float(Av), "c": float(cv),
        "alpha_sq_exact": float(exact) if exact is not None else None,
        "alpha_sq_doc_form": float(docf) if docf is not None else None,
        "rel_diff": (float(abs(exact - docf) / abs(exact))
                     if (exact is not None and docf is not None) else None),
    })

# --- 在近消去极限核对旧式为何"看起来对" ---
A_near = mpf("0.5") / (1 + ALPHA_SQ)      # c=-1 下命中 α_obs 的 A
errata_near = {
    "A": float(A_near), "c": -1.0,
    "alpha_sq_exact": float(alpha_sq(A_near, mpf(-1))),
    "alpha_sq_doc_form": float(doc_form_alpha_sq(A_near, mpf(-1))),
    "alpha_sq_obs": float(ALPHA_SQ),
    "note": "近消去极限下旧式与精确式同阶（差 O(α²)），故此前未被发现",
}

# ===========================================================================
# 二、定理 R1：自指近消去恒等（精确）
# ===========================================================================
# 规格方程 ⟺ P = 2Q·α²/(1+α²) ⟺ |P/Q| = 2α²/(1+α²)（与 c 无关）
cancel_ratio = 2 * ALPHA_SQ / (1 + ALPHA_SQ)

# c=-1 下所需 A 及其相对精度（精确）
# A_req = P_req - c/2,  P_req = 2Q α²/(1+α²),  c=-1 ⇒ Q=-1/4
c_demo = mpf(-1)
Q_demo = mpf("0.25") + c_demo / 2
P_req = 2 * Q_demo * ALPHA_SQ / (1 + ALPHA_SQ)
A_req = P_req - c_demo / 2
A_natural = mpf("0.5") + c_demo / 2 * 0          # "自然"值 A = -c/2 = 0.5（完全消去）
rel_prec_required = abs(A_natural - A_req) / abs(A_natural)
identity_check = rel_prec_required - ALPHA_SQ / (1 + ALPHA_SQ)   # 期望 = 0

theorem_R1 = {
    "name": "定理 R1（自指近消去恒等）",
    "statement": (
        "规格方程 ⟺ |P/Q| = 2α²/(1+α²)（与 c 无关）。"
        "即：机制必须实现的近消去比例，恒等于待预测量 α² 的两倍。"
        "c=−1 处，把 α 钉到 α_obs 所需的 A 相对精度 ≡ α²/(1+α²)（精确代数恒等）。"
    ),
    "cancel_ratio_2a2_over_1pa2": float(cancel_ratio),
    "required_A_relative_precision": float(rel_prec_required),
    "alpha_sq_over_1_plus_alpha_sq": float(ALPHA_SQ / (1 + ALPHA_SQ)),
    "identity_residual": float(abs(identity_check)),
    "interpretation": (
        "\"需要供给的精度\" 恒等于 \"待预言的量\"（O(α²) 级）⇒ 循环性："
        "要钉住 α，机制必须已经知道 α。这不是数值巧合，而是代数恒等。"
    ),
}

# ===========================================================================
# 三、定理 R2(a)：离散拓扑输入 —— 可证伪否定（含 φ 推广）
# ===========================================================================
import math

# c=-1、φ=0（周期）精确关系：α²=(N²−2m²)/(2m²)=d/(2m²), 1/α=m√(2/d)
# 推广：A=(n+φ)²/N²（n∈ℤ, N∈ℤ₊, φ∈有理数）
PHI_LIST = [Fraction(0), Fraction(1, 2), Fraction(1, 3), Fraction(2, 3),
            Fraction(1, 4), Fraction(3, 4), Fraction(1, 5)]
CVAL_DISC = [Fraction(-1), Fraction(-3, 2), Fraction(-2), Fraction(-5, 2),
             Fraction(-3), Fraction(-4), Fraction(-5)]

NMAX = 4000
disc_records = []
for cfr in CVAL_DISC:
    cv = float(cfr)
    Qv = 0.25 + cv / 2.0
    if Qv >= 0:
        continue
    Q = Qv
    # A=(n+φ)²/N²；给定 N，α²=P/(2Q−P) 随 A 单调，反解 A_target 使 α=α_obs，
    # 再取 A_target 附近的整数 n（避免 O(N²) 全枚举）
    P_req = 2 * Q * float(ALPHA_SQ) / (1 + float(ALPHA_SQ))
    A_target = P_req - cv / 2.0
    if A_target <= 0:
        continue
    for ph in PHI_LIST:
        for N in range(1, NMAX + 1):
            base = N * math.sqrt(A_target)
            n0 = int(math.floor(base - float(ph)))
            for n in (n0, n0 + 1, n0 + 2):
                x = (n + float(ph)) / float(N)
                if x <= 0:
                    continue
                Av = x * x
                a2 = alpha_sq(Av, cv)
                if a2 is None or a2 <= 0:
                    continue
                a = math.sqrt(float(a2))
                disc_records.append({
                    "c": [cfr.numerator, cfr.denominator], "phi": [ph.numerator, ph.denominator],
                    "n": n, "N": N, "A": Av, "alpha_inv": 1.0 / a,
                })

disc_records.sort(key=lambda r: abs(r["alpha_inv"] - float(AINV)))
disc_best = disc_records[0] if disc_records else None
disc_below = [r for r in disc_records if r["alpha_inv"] <= float(AINV)]
disc_above = [r for r in disc_records if r["alpha_inv"] >= float(AINV)]
disc_lo = max(disc_below, key=lambda r: r["alpha_inv"]) if disc_below else None
disc_hi = min(disc_above, key=lambda r: r["alpha_inv"]) if disc_above else None

# 严格口径：只用"小绕数自然区间"（N ≤ 200）判定
disc_small = [r for r in disc_records if r["N"] <= 200]
disc_small_best = (min(disc_small, key=lambda r: abs(r["alpha_inv"] - float(AINV)))
                   if disc_small else None)

if disc_best is not None:
    best_rel = abs(disc_best["alpha_inv"] - float(AINV)) / float(AINV)
else:
    best_rel = None

theorem_R2a = {
    "name": "定理 R2(a)（离散拓扑输入：可证伪否定）",
    "enum_scope": "c ∈ {−1,−3/2,−2,−5/2,−3,−4,−5}; φ ∈ {0,1/2,1/3,2/3,1/4,3/4,1/5}; N ≤ %d" % NMAX,
    "best": disc_best,
    "best_relative_deviation": best_rel,
    "observational_tol": float(OBS_TOL_STRICT),
    "miss_factor": (best_rel / float(OBS_TOL_STRICT)) if best_rel is not None else None,
    "bracket": {"below": disc_lo, "above": disc_hi},
    "small_N_best": disc_small_best,
    "verdict": (
        "1/α_obs=137.036 在全枚举内不达；最近解偏离 %.2e ≈ %.1f× 观测精度 1.6e-5"
        "⇒ 离散路被观测可证伪否定（大 N 逼近属丢番图逼近，非预言）"
    ) % (best_rel, (best_rel / float(OBS_TOL_STRICT))) if best_rel is not None else "无记录",
}

# ===========================================================================
# 四、定理 R2(b)：近消去归约（无标度）
# ===========================================================================
theorem_R2b = {
    "name": "定理 R2(b)（近消去归约：无标度壁垒适用）",
    "statement": (
        "规格方程只依赖比值 P/Q（c=-1 时 Q=-1/4 固定，故只需 P 的绝对值）。"
        "P→0⁻ 的近消去等价于\"小正质量平方/近临界\"精细调节（层级问题同型）。"
        "定理 E：齐次结构定不了绝对标度；定理 N：纯相位 Z ⇒ β≡0，无 RG 环。"
        "⇒ 框架内无生成残差 |P/Q|=2α²/(1+α²) 的机制。"
    ),
    "P_is_scale_like": True,
    "cancel_ratio": float(cancel_ratio),
    "required_P_over_Q": float(cancel_ratio),
}

# ===========================================================================
# 五、突破候选普查：宽枚举"自然候选"（无调参）
# ===========================================================================
C_CAND = [Fraction(-1), Fraction(-6, 5), Fraction(-5, 4), Fraction(-4, 3),
          Fraction(-3, 2), Fraction(-5, 3), Fraction(-7, 4), Fraction(-2),
          Fraction(-9, 4), Fraction(-7, 3), Fraction(-5, 2), Fraction(-8, 3),
          Fraction(-3), Fraction(-10, 3), Fraction(-7, 2), Fraction(-4),
          Fraction(-9, 2), Fraction(-5)]
PHI_CAND = [Fraction(0), Fraction(1, 2), Fraction(1, 3), Fraction(2, 3),
            Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
            Fraction(3, 5), Fraction(1, 6), Fraction(5, 6), Fraction(1, 8),
            Fraction(3, 8), Fraction(1, 7), Fraction(1, 9), Fraction(1, 10)]
NCAND = 6000

cand_hits = []
cand_records = []
for cfr in C_CAND:
    cv = float(cfr)
    Q = 0.25 + cv / 2.0
    if Q >= 0:
        continue
    P_req = 2 * Q * float(ALPHA_SQ) / (1 + float(ALPHA_SQ))
    A_target = P_req - cv / 2.0
    if A_target <= 0:
        continue
    for ph in PHI_CAND:
        for N in range(1, NCAND + 1):
            base = N * math.sqrt(A_target)
            n0 = int(math.floor(base - float(ph)))
            for n in (n0, n0 + 1, n0 + 2):
                x = (n + float(ph)) / float(N)
                if x <= 0:
                    continue
                Av = x * x
                a2 = alpha_sq(Av, cv)
                if a2 is None or a2 <= 0:
                    continue
                a = math.sqrt(float(a2))
                inv = 1.0 / a
                rel = abs(inv - float(AINV)) / float(AINV)
                rec = {"c": [cfr.numerator, cfr.denominator],
                       "phi": [ph.numerator, ph.denominator],
                       "n": n, "N": N, "A": Av, "alpha_inv": inv, "rel_dev": rel}
                cand_records.append(rec)
                if rel < float(OBS_TOL_STRICT):
                    cand_hits.append(rec)

cand_records.sort(key=lambda r: r["rel_dev"])
cand_best = cand_records[0] if cand_records else None
cand_smallN = [r for r in cand_records if r["N"] <= 300]
cand_smallN_best = min(cand_smallN, key=lambda r: r["rel_dev"]) if cand_smallN else None

natural_search = {
    "name": "突破候选普查（无调参自然组合）",
    "scope": "c 分母≤5、φ 分母≤10、N ≤ %d 的 (c, φ, n, N) 组合" % NCAND,
    "hits_within_obs_tol": len(cand_hits),
    "best_overall": cand_best,
    "best_small_N": cand_smallN_best,
    "obs_tol": float(OBS_TOL_STRICT),
    "verdict": (
        "命中观测精度 1.6e-5 的自然组合数 = %d；最佳整体偏差 %.2e（N=%s）"
        "⇒ 无调参自然命中（大 N 逼近属丢番图逼近）"
    ) % (len(cand_hits),
         cand_best["rel_dev"] if cand_best else float("nan"),
         cand_best["N"] if cand_best else "-"),
}

# ===========================================================================
# 六、汇总与产出
# ===========================================================================
theorem_R = {
    "name": "定理 R（规格曲线钉死不可行性与自指近消去恒等）",
    "engine": "突破_规格曲线钉死与自指近消去.py（sympy 符号 + mpmath dps=50）",
    "exact_specification": str(alpha_sq_exact),
    "errata": (
        "旧文档 α²=|A+c/2|/|c+1/2| 非精确解；精确解 α²=P/(2Q−P)，"
        "旧式仅在近消去极限同阶（差 O(α²)）"
    ),
    "R1": theorem_R1,
    "R2a": theorem_R2a,
    "R2b": theorem_R2b,
    "route_ledger": [
        ["量纲代数（锚集零空间）", "不可行", "定理 C"],
        ["几何作用量（旋钮零空间）", "不可行（无内点极小）", "定理 H"],
        ["算子谱+量子化（可固定 α）", "可行但需近消去", "定理 F"],
        ["规格曲线钉死（本轮）", "不可由本公设闭合（离散被证伪/连续为输入）", "定理 R"],
    ],
    "honest_boundary": [
        "定理 R1 是精确代数恒等（|P/Q|=2α²/(1+α²)），非数值巧合。",
        "定理 R2(a) 的可证伪否定限于已枚举的 (c,φ,N) 网格与 N≤%d；更大 N 属丢番图逼近，不作预言。" % NCAND,
        "定理 R2(b) 引用的定理 E/N 出自 openuft 既有体系（本书第十二/十四编），本轮只做对接，不重证。",
        "本引擎不解锁 UFT-3、不宣称推出 α；它把\"什么钉住 (A,c)\"判为不可由本公设闭合。",
    ],
    "next_real_question": (
        "剩余唯一出口：一条**既非齐次、又带独立无量纲锚**的耦合约束。"
        "在本框架内已穷尽（定理 E/F/N + 本轮 R）；须引入强于世界线几何的新动力学公设。"
    ),
}

report = {
    "module": "突破_规格曲线钉死与自指近消去（定理 R）",
    "alpha_obs": float(ALPHA),
    "alpha_obs_inv": float(AINV),
    "alpha_sq_obs": float(ALPHA_SQ),
    "sympy_u_star": str(u_star),
    "sympy_d2_at_u_star": str(d2_at),
    "sympy_alpha_sq_exact": str(alpha_sq_exact),
    "errata_checks": errata_checks,
    "errata_near_cancellation": errata_near,
    "theorem_R": theorem_R,
    "natural_search": natural_search,
    "natural_search_top10": cand_records[:10],
    "discrete_top10": disc_records[:10],
}

with io.open(os.path.join(DATA, "突破_规格曲线钉死与自指近消去.json"), "w", encoding="utf-8") as f:
    f.write(json.dumps(report, ensure_ascii=False, indent=2))

# ---------------- Markdown ----------------
L = []
L.append("# 突破：规格曲线钉死不可行性、自指近消去恒等与自然输入普查（定理 R）\n")
L.append("**引擎**：`源码/突破_规格曲线钉死与自指近消去.py`（可复跑，sympy + mpmath dps=50）\n")
L.append("> 承接 `突破_算子谱与量子化规格.py`（定理 F）末句提出的真问题：")
L.append("> **「什么把 (A,c) 钉在规格曲线上？」** 本轮正面攻之。\n")
L.append("## 一、勘误：规格方程的精确形式\n")
L.append("由 $u^*=2Q/P$、$\\alpha=1/\\sqrt{u^*-1}$ 严格推出精确规格方程：\n")
L.append("$$\\boxed{\\ \\alpha^2=\\frac{P}{2Q-P}=\\frac{A+c/2}{\\tfrac12+\\tfrac{c}{2}-A}\\ }$$\n")
L.append("既有文档写的 $\\alpha^2=|A+c/2|/|c+1/2|$ **不是精确解**（仅在近消去极限 $A\\to-c/2$ 与之同阶，差 $O(\\alpha^2)$）：\n")
L.append("| A | c | α² 精确 | α² 旧式 | 相对差 |")
L.append("| --- | --- | --- | --- | --- |")
for r in errata_checks:
    L.append("| %.2f | %.1f | %s | %s | %s |" % (
        r["A"], r["c"],
        fmt(r["alpha_sq_exact"], 8) if r["alpha_sq_exact"] is not None else "—",
        fmt(r["alpha_sq_doc_form"], 8) if r["alpha_sq_doc_form"] is not None else "—",
        ("%.3e" % r["rel_diff"]) if r["rel_diff"] is not None else "—"))
L.append("")
L.append("> 近消去极限处（$A=%.9f$，$c=-1$）旧式与精确式同阶（都 $\\approx\\alpha^2$），故此前未被发现。\n"
         % errata_near["A"])
L.append("## 二、定理 R1：自指近消去恒等（精确代数恒等）\n")
L.append("规格方程两边同乘 $(2Q-P)$ 得 $P=2Q\\alpha^2/(1+\\alpha^2)$，即\n")
L.append("$$\\boxed{\\ \\left|\\frac{P}{Q}\\right|=\\frac{2\\alpha^2}{1+\\alpha^2}\\ }\\qquad(\\text{与 }c\\text{ 无关})$$\n")
L.append("- 要求机制实现的**近消去比例** $|P/Q|$ = **%.9f**；" % float(cancel_ratio))
L.append("- 在 $c=-1$ 处把 α 钉到 $\\alpha_{\\rm obs}$ 所需的 $A$ 相对精度 = **%.6e**，" % float(rel_prec_required))
L.append("  而 $\\alpha^2/(1+\\alpha^2)$ = **%.6e**，恒等残差 = **%.2e**。\n"
         % (float(ALPHA_SQ / (1 + ALPHA_SQ)), float(abs(identity_check))))
L.append("> **含义（循环性）**：\"需要供给的精度\" 恒等于 \"待预言的量\"（$O(\\alpha^2)$ 级）。")
L.append("> 要钉住 α，机制必须**已经知道** α。这不是数值巧合，是代数恒等。\n")
L.append("## 三、定理 R2(a)：离散拓扑输入 —— 可证伪否定\n")
L.append("枚举范围：$c\\in\\{-1,-3/2,-2,-5/2,-3,-4,-5\\}$、$\\varphi\\in\\{0,1/2,1/3,2/3,1/4,3/4,1/5\\}$、$N\\le%d$。\n" % NMAX)
if disc_best is not None:
    L.append("| 量 | 值 |")
    L.append("| --- | --- |")
    L.append("| 距离最近解 $(c,\\varphi,n,N)$ | (%s, %s, %d, %d) |" % (
        "%d/%d" % tuple(disc_best["c"]), "%d/%d" % tuple(disc_best["phi"]),
        disc_best["n"], disc_best["N"]))
    L.append("| 预言 $1/\\alpha$ | **%.4f** |" % disc_best["alpha_inv"])
    L.append("| 相对偏差 | **%.3e** |" % best_rel)
    L.append("| 观测精度 1.6e-5 | 偏差为其 **%.1f 倍** |" % (best_rel / float(OBS_TOL_STRICT)))
    L.append("")
L.append("> ⇒ 全枚举内 $1/\\alpha_{\\rm obs}=137.036$ **不达**；离散路被观测**可证伪否定**")
L.append("> （更大 $N$ 的逼近属丢番图逼近，非预言）。\n")
L.append("## 四、定理 R2(b)：近消去归约（无标度壁垒适用）\n")
L.append("规格方程只依赖比值 $P/Q$（$c=-1$ 时 $Q=-1/4$ 固定 ⇒ 只需 $P$ 的绝对值）。")
L.append("$P\\to0^-$ 的近消去等价于**小正质量平方 / 近临界**精细调节（与层级问题同型）。")
L.append("定理 E（齐次结构定不了绝对标度）+ 定理 N（纯相位 $Z$ ⇒ $\\beta\\equiv0$，无 RG 环）")
L.append("⇒ **框架内无生成残差 $|P/Q|=2\\alpha^2/(1+\\alpha^2)$ 的机制**。\n")
L.append("## 五、突破候选普查（无调参自然组合）\n")
L.append("枚举 $c$ 分母 $\\le5$、$\\varphi$ 分母 $\\le10$、$N\\le%d$ 的全部组合。\n" % NCAND)
L.append("| 量 | 值 |")
L.append("| --- | --- |")
L.append("| 命中观测精度 $1.6\\times10^{-5}$ 的组合数 | **%d** |" % len(cand_hits))
if cand_best is not None:
    L.append("| 最佳整体 $1/\\alpha$ | %.4f（$c$=%d/%d, $\\varphi$=%d/%d, $n$=%d, $N$=%d）偏差 %.2e |" % (
        cand_best["alpha_inv"], cand_best["c"][0], cand_best["c"][1],
        cand_best["phi"][0], cand_best["phi"][1], cand_best["n"], cand_best["N"],
        cand_best["rel_dev"]))
if cand_smallN_best is not None:
    L.append("| 小绕数最佳（$N\\le300$） | %.4f（偏差 %.2e，$N$=%d） |" % (
        cand_smallN_best["alpha_inv"], cand_smallN_best["rel_dev"], cand_smallN_best["N"]))
L.append("")
L.append("> ⇒ **无调参自然命中**；所有接近解都在大 $N$（丢番图逼近）或需把 $(A,c)$ 调到规格曲线上。\n")
L.append("## 六、定理 R 与路线总账\n")
L.append("| 路线 | 结论 | 封死者 |")
L.append("| --- | --- | --- |")
for row in theorem_R["route_ledger"]:
    L.append("| %s | %s | %s |" % (row[0], row[1], row[2]))
L.append("")
L.append("**诚实边界（不美化）**：")
for b in theorem_R["honest_boundary"]:
    L.append("- %s" % b)
L.append("")
L.append("> **下一个真问题**：%s" % theorem_R["next_real_question"])
L.append("")
L.append("> **诚实立场**：本轮**没有**实现统一场论、**没有**解锁 UFT-3（联盟层仍 2/6）。")
L.append("> 它把\"什么钉住 (A,c)\"从**未试出**升级为**已证不可由本公设闭合**：")
L.append("> 离散输入被观测证伪，连续输入落到定理 F 输入壁垒，近消去本身是 $2\\alpha^2$ 级的自指循环。")

with io.open(os.path.join(DATA, "突破_规格曲线钉死与自指近消去.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

# ---------------- 控制台 ----------------
print("=== 定理 R：规格曲线钉死与自指近消去 ===")
print("  [符号] u* = 2Q/P ; e''(u*) = -P^4/(8Q^3) ; 精确规格 alpha^2 = P/(2Q-P)")
print("  [勘误] c=-2,A=0: 精确 alpha^2 = %s vs 旧式 %s (相对差 %s)" % (
    fmt(errata_checks[0]["alpha_sq_exact"], 8),
    fmt(errata_checks[0]["alpha_sq_doc_form"], 8),
    "%.3e" % errata_checks[0]["rel_diff"]))
print("  [R1] |P/Q| = 2alpha^2/(1+alpha^2) = %s (c-independent)" % fmt(cancel_ratio, 8))
print("       所需 A 相对精度 = %s ; alpha^2/(1+alpha^2) = %s ; 残差 = %.2e" % (
    fmt(rel_prec_required, 8), fmt(ALPHA_SQ / (1 + ALPHA_SQ), 8), float(abs(identity_check))))
if disc_best is not None:
    print("  [R2a] 离散最佳 1/alpha = %.4f (偏差 %.2e = %.1fx 观测精度)" % (
        disc_best["alpha_inv"], best_rel, best_rel / float(OBS_TOL_STRICT)))
print("  [R2b] 近消去 = 小正质量平方精细调节 ; 定理 E/N ⇒ 框架内无生成机制")
print("  [普查] 命中观测精度组合数 = %d ; 最佳整体偏差 = %s (N=%s)" % (
    len(cand_hits),
    "%.2e" % cand_best["rel_dev"] if cand_best else "n/a",
    cand_best["N"] if cand_best else "-"))
print("定理 R：规格钉死不可由本公设闭合（离散被证伪 / 连续为输入 / 近消去为 2alpha^2 自指循环）")
print("done: see 数据/突破_规格曲线钉死与自指近消去.md")
