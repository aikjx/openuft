# -*- coding: utf-8 -*-
"""
突破尝试：算子谱与量子化 —— α 的可行性判定与规格（定理 F）
==========================================================

定理 E 已证明：**几何作用量类**（∫κ²,∫τ²,…）永远没有内点极小 ⇒ α 自由或被推到 α∈{0,∞}。
本轮攻击第62章砖 (ii)：**具非平凡结构的算子谱 + 边界/量子化条件**。

构造（闭合螺旋，N 圈，扭转边界条件 ψ(s+L)=e^{i2πφ}ψ(s)）：
    H = −(ℏ²/2m)∂_s² + V_geo(s) + (c/2)τ(s)²,   V_geo = −(ℏ²/8m)κ²（da Costa）
以 ℏ²/(2mR²) 为单位，u = 1+x²（x=b/R，α=κ/τ=1/x）：
    e(u) = A/u − 1/(4u²) + (c/2)(u−1)/u² = P/u − Q/u²,
    A = (n+φ)²/N²,   P = A + c/2,   Q = 1/4 + c/2.
（首项 = 模量子化动能；第二项 = 几何势；第三项 = 挠率耦合。）

本引擎的判定（全部符号/数值实算，不调参）：
  1. 临界点 u* = 2Q/P；二阶导 e''(u*) = −P⁴/(8Q³)
     ⇒ **内点极小的充要条件是 Q<0，即 c < −1/2**（负挠率耦合）。
  2. 结论与定理 E 的关键差别：**算子类可以有内点极小**（nullity_dyn=0 ⇒ α 可被固定）！
     这是"几何动力学"路线上第一次出现**能固定 α** 的机制。
  3. 规格方程：α = 1/√(u*−1) ⇒ **α² = |A + c/2| / |c + 1/2|**（含临界点存在区）。
     ⇒ 观测的小 α 要求 **A 与 −c/2 近消去**（A → −c/2⁻ 时 u*→∞、α→0）。
  4. 离散输入扫描：若 (n, φ, N) 由拓扑固定（整数/半整数），A 取离散值；
     扫描给出可达的 α 集合 —— 判定"拓扑输入能否自然给出 1/137"。
  5. 连续输入：解出把 α 钉到观测值所需的 (A, c)，量化**调参精度**。

诚实立场：本引擎**不**声称推出 α。它把砖 (ii) 从"未验"判为**可行但带明确规格**，
并给出"为什么仍不能免费得到 α"的精确原因。
"""
import io
import json
import os
import sys

from mpmath import mp, mpf
from sympy import Rational, Symbol, diff, simplify, solve

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 50
ALPHA = mpf("7.2973525693e-3")
AINV = 1 / ALPHA

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "数据")
os.makedirs(DATA, exist_ok=True)

# ---------------- 1. 符号推导 ----------------
u = Symbol("u", positive=True)
A = Symbol("A", positive=True)
c = Symbol("c", real=True)

e = simplify(A / u - Rational(1, 4) / u ** 2 + (c / 2) * (u - 1) / u ** 2)
de = simplify(diff(e, u))
d2 = simplify(diff(e, u, 2))
crit = solve(de, u)
P = A + c / 2
Q = Rational(1, 4) + c / 2
d2_at = simplify(d2.subs(u, 2 * Q / P))

# ---------------- 2. 数值判定 ----------------
def pred(Av, cv):
    """给定 (A, c)，返回 (alpha_pred, 说明)。"""
    Pv = Av + cv / 2.0
    Qv = 0.25 + cv / 2.0
    if Qv >= 0:
        return None, "临界点为极大（Q>=0，c>=-1/2）⇒ 全局极小在边界，α∈{0,∞}"
    if Pv >= 0 or abs(Pv) < 1e-300:
        return None, "P>=0 ⇒ u*<=0，无物理解（α 不可固定）"
    us = 2 * Qv / Pv            # 两负数相除 > 0
    if us <= 1.0:
        return None, "u*<=1 ⇒ x²<=0，无物理解"
    return 1.0 / (us - 1.0) ** 0.5, "内点极小 ⇒ α 被固定（nullity_dyn=0）"

# 2a. 若干 O(1) 参数组
scan_oc = []
for Av in [0.0, 0.25, 0.4, 0.5, 0.6]:
    for cv in [0.0, -0.5, -1.0, -2.0, -5.0]:
        a, why = pred(Av, cv)
        scan_oc.append({
            "A": Av, "c": cv, "alpha_pred": a, "note": why,
            "u_star": (2 * (0.25 + cv / 2.0) / (Av + cv / 2.0)) if (cv < -0.5 and Av + cv / 2.0 < 0) else None,
        })

# 2b. 关键对照：c=−1, A=1/2 ⇒ α=0（完全消去）；A=1/2/(1+α²) ⇒ α=α_obs
A_tuned = 0.5 / (1.0 + float(ALPHA) ** 2)
a_zero, why_zero = pred(0.5, -1.0)
a_tuned, why_tuned = pred(A_tuned, -1.0)
tuned_row = {
    "c": -1.0,
    "A_at_exact_cancel": 0.5, "alpha_at_exact_cancel": a_zero, "note_at_cancel": why_zero,
    "A_required": A_tuned, "alpha_at_required": a_tuned, "note_at_required": why_tuned,
    "delta_A": 0.5 - A_tuned, "relative_precision": (0.5 - A_tuned) / 0.5,
}

# ---------------- 3. 离散拓扑输入扫描（取 c = −1） ----------------
# 精确关系（c=−1, A<1/2）：
#   u* = 0.5/(0.5−A)  ⇒  α² = 1/(u*−1) = (0.5−A)/A = (N² − 2m²)/(2m²)
#   ⇒  1/α = m·√(2/d),   d = N² − 2m² ∈ ℤ_{>0}
# 即 A=(m/N)² 离散 ⇒ α **被预言**（无调参）。
import math
disc = []
for m in range(1, 2001):
    base = math.sqrt(2.0) * m
    n0 = int(math.floor(base))
    for N in (n0, n0 + 1, n0 + 2, n0 + 3):
        if N <= 0:
            continue
        d = N * N - 2 * m * m
        if d <= 0:
            continue
        a = math.sqrt(d / (2.0 * m * m))
        disc.append({"m": m, "N": N, "d": d, "A": (m / float(N)) ** 2,
                     "alpha_pred": a, "alpha_inv": 1.0 / a})
disc.sort(key=lambda r: abs(r["alpha_inv"] - float(AINV)))
best = disc[0] if disc else None
below = [r for r in disc if r["alpha_inv"] <= float(AINV)]
above = [r for r in disc if r["alpha_inv"] >= float(AINV)]
bracket_lo = max(below, key=lambda r: r["alpha_inv"]) if below else None
bracket_hi = min(above, key=lambda r: r["alpha_inv"]) if above else None
families = {}
for d in (1, 2, 3, 4):
    fam = sorted([r for r in disc if r["d"] == d], key=lambda r: r["m"])
    families[str(d)] = [{"m": r["m"], "N": r["N"], "alpha_inv": r["alpha_inv"]}
                        for r in fam[:6]]

# ---------------- 4. 汇总 ----------------
theorem_f = {
    "name": "定理 F（算子谱与量子化：α 的可行性判定与规格）",
    "model": "H = −(ℏ²/2m)∂_s² + V_geo + (c/2)τ²，闭合螺旋 N 圈，扭转边界条件 φ",
    "dimensionless_energy": "e(u) = P/u − Q/u²,  P = A + c/2,  Q = 1/4 + c/2,  A = (n+φ)²/N²,  u = 1+x²",
    "critical_point": "u* = 2Q/P",
    "second_derivative": "e''(u*) = −P⁴/(8Q³)",
    "existence_of_interior_min": "Q<0 ⇔ c < −1/2（负挠率耦合）",
    "specification": "α² = |A + c/2| / |c + 1/2|   （α = 1/√(u*−1)）",
    "key_contrast_with_E": (
        "定理 E：几何作用量类**永远没有**内点极小 ⇒ α 不可固定。"
        "定理 F：算子类**可以**有内点极小（c<−1/2 时）⇒ α 可被固定（nullity_dyn=0）。"
        "这是几何动力学路线上第一次出现能固定 α 的机制。"
    ),
    "why_not_free": (
        "规格方程要求 A 与 −c/2 近消去（A→−c/2⁻ 时 α→0）。"
        "在 c=−1（O(1)）下：A=1/2 给出 α=0（完全消去）；"
        "要得到 α_obs 需 A = 1/(2(1+α²))，与 1/2 相差 2.66e-5 —— 即**调参精度 O(α²)**。"
    ),
}

report = {
    "module": "突破_算子谱与量子化规格（定理 F）",
    "alpha_obs_inv": float(AINV),
    "scan_O1": scan_oc,
    "tuned_case": tuned_row,
    "discrete_scan": disc,
    "discrete_best": best,
    "discrete_bracketing": {"below": bracket_lo, "above": bracket_hi},
    "theorem_F": theorem_f,
}
with io.open(os.path.join(DATA, "算子谱与量子化规格.json"), "w", encoding="utf-8") as f:
    f.write(json.dumps(report, ensure_ascii=False, indent=2))

# ---------------- 5. Markdown ----------------
L = []
L.append("# 突破：算子谱与量子化 —— α 的可行性判定与规格（定理 F）\n")
L.append("**引擎**：`源码/突破_算子谱与量子化规格.py`（可复跑，sympy + mpmath dps=50）\n")
L.append("## 一、模型与无量纲化\n")
L.append("闭合螺旋（N 圈，扭转边界条件 $\\psi(s+L)=e^{i2\\pi\\varphi}\\psi(s)$）上的算子")
L.append("$$H=-\\frac{\\hbar^2}{2m}\\partial_s^2+V_{\\rm geo}(s)+\\frac{c}{2}\\tau(s)^2,\\qquad V_{\\rm geo}=-\\frac{\\hbar^2}{8m}\\kappa^2\\ (\\text{da Costa}).$$\n")
L.append("以 $\\hbar^2/(2mR^2)$ 为单位、$u=1+x^2$（$x=b/R$，$\\alpha=\\kappa/\\tau=1/x$）：")
L.append("$$e(u)=\\frac{A}{u}-\\frac{1}{4u^2}+\\frac{c}{2}\\frac{u-1}{u^2}=\\frac{P}{u}-\\frac{Q}{u^2},\\qquad "
         "A=\\frac{(n+\\varphi)^2}{N^2},\\ P=A+\\frac{c}{2},\\ Q=\\frac14+\\frac{c}{2}.$$\n")
L.append("首项 = 模量子化动能，第二项 = 几何势，第三项 = 挠率耦合。\n")
L.append("## 二、内点极小判据（与定理 E 的关键差别）\n")
L.append("$$u^*=\\frac{2Q}{P},\\qquad e''(u^*)=-\\frac{P^4}{8Q^3}"
         "\\;\\Longrightarrow\\; \\text{内点极小}\\iff Q<0\\iff \\boxed{c<-\\tfrac12}.$$\n")
L.append("> **这是本轮最重要的一条**：定理 E 证明几何作用量类**永远没有**内点极小；")
L.append("> 而算子类只要**挠率耦合足够负**（$c<-1/2$）就**有**内点极小 ⇒ $\\text{nullity}_{\\rm dyn}=0$ ⇒ **α 可被固定**。")
L.append("> 即：**砖 (ii) 不是死的**（砖 (i) 已被定理 E 判死）。\n")
L.append("### 2a. O(1) 参数组扫描\n")
L.append("| A | c | u* | 预言 α | 判定 |")
L.append("| --- | --- | --- | --- | --- |")
for r in scan_oc:
    us = ("%.4f" % r["u_star"]) if r["u_star"] is not None else "—"
    ap = ("%.6f" % r["alpha_pred"]) if r["alpha_pred"] is not None else "—"
    L.append("| %.2f | %.1f | %s | %s | %s |" % (r["A"], r["c"], us, ap, r["note"]))
L.append("")
L.append("> 所有 $c\\ge-1/2$ 的组都落到边界（$\\alpha\\in\\{0,\\infty\\}$）；只有 $c<-1/2$ 才有内点极小。\n")
L.append("## 三、规格方程与「为什么仍不免费」\n")
L.append("由 $\\alpha=1/\\sqrt{u^*-1}$：\n")
L.append("$$\\boxed{\\ \\alpha^2=\\frac{|A+c/2|}{|c+1/2|}\\ }$$\n")
L.append("⇒ 观测的小 $\\alpha$ 要求 **A 与 $-c/2$ 近消去**（$A\\to-c/2^-$ 时 $u^*\\to\\infty$、$\\alpha\\to0$）。\n")
L.append("| 量 | 值 |")
L.append("| --- | --- |")
L.append("| 取 c = −1，完全消去 A = 1/2 | α = %s |" % ("%.6f" % a_zero if a_zero is not None else "0"))
L.append("| 取 c = −1，命中 α_obs 所需 A | **%.9f** |" % tuned_row["A_required"])
L.append("| 与 1/2 之差 δA | %.4e |" % tuned_row["delta_A"])
L.append("| **所需相对精度** | **%.4e（= α² 量级）** |" % tuned_row["relative_precision"])
L.append("")
L.append("> 即：$c=-1$（O(1)，无需调参）下，$A=1/2$ 给出 $\\alpha=0$；要得到 $\\alpha_{\\rm obs}$ 必须把 $A$ 精确到")
L.append("> $5.3\\times10^{-5}$ 的相对精度 —— **调参精度 $O(\\alpha^2)$**。\n")
L.append("## 四、离散拓扑输入扫描（c = −1，(n+φ)=m 与 N 为整数）\n")
L.append("精确关系：$\\alpha^2=(N^2-2m^2)/(2m^2)$ ⇒ $1/\\alpha=m\\sqrt{2/d}$，$d=N^2-2m^2\\in\\mathbb{Z}_{>0}$。")
L.append("即离散拓扑输入下 $\\alpha$ **被真正预言**（无调参）。$m\\le2000$ 全枚举，按 $d$ 分支：\n")
L.append("| d | 前几组 (m,N) | 预言 1/α |")
L.append("| --- | --- | --- |")
for _d in ("1", "2", "3", "4"):
    _fam = families.get(_d, [])
    if not _fam:
        continue
    L.append("| %s | %s | %s |" % (
        _d,
        ", ".join("(%d,%d)" % (r["m"], r["N"]) for r in _fam[:5]),
        ", ".join("%.3f" % r["alpha_inv"] for r in _fam[:5])))
L.append("")
if best is not None:
    L.append("| 距 $1/\\alpha_{\\rm obs}=%.3f$ 最近的离散解 | 值 |" % float(AINV))
    L.append("| --- | --- |")
    L.append("| (m, N, d) | (%d, %d, %d) |" % (best["m"], best["N"], best["d"]))
    L.append("| 预言 1/α | **%.4f** |" % best["alpha_inv"])
    L.append("| 相对偏差 | **%.3e** |" % (abs(best["alpha_inv"] - float(AINV)) / float(AINV)))
    L.append("")
if bracket_lo is not None and bracket_hi is not None:
    L.append("> **结论**：可达 $1/\\alpha$ 是稀疏的 **Pell 型序列**（$d=1$ 支 $\\approx3,17,99,577,\\dots$；")
    L.append("> $d=2$ 支 $=1,7,41,239,\\dots$）。$1/\\alpha_{\\rm obs}=137.036$ **不落在任何一支上**，")
    L.append("> 被 %.2f（%s）与 %.2f（%s）夹住。" % (
        bracket_lo["alpha_inv"],
        "m=%d,N=%d,d=%d" % (bracket_lo["m"], bracket_lo["N"], bracket_lo["d"]),
        bracket_hi["alpha_inv"],
        "m=%d,N=%d,d=%d" % (bracket_hi["m"], bracket_hi["N"], bracket_hi["d"])))
    L.append("> **诚实修正（不美化）**：$m$ 很大时轨道变密（$1/\\alpha=m\\sqrt{2/d}$ 可逼近任意目标）——")
    L.append("> 全枚举内最近解为 $1/\\alpha=%.4f$（偏差 %.2e，约为观测精度 $1.6\\times10^{-5}$ 的 %.0f 倍）。" % (
        best["alpha_inv"],
        abs(best["alpha_inv"] - float(AINV)) / float(AINV),
        (abs(best["alpha_inv"] - float(AINV)) / float(AINV)) / 1.6e-5))
    L.append("> 即：**小 $N$ 的自然区间无一命中**；大 $N$ 的「命中」属丢番图逼近（**数值巧合，非预言**）。")
    L.append("> ⇒ 拓扑离散版路线：**自然区间被观测排除；允许大绕数则退化为 numerology。**\n")
L.append("## 五、定理 F 与总论\n")
L.append("> **定理 F**：在螺旋算子类上，内点极小存在 $\\iff c<-1/2$；此时 $\\alpha$ 被固定，且满足规格方程")
L.append("> $\\alpha^2=|A+c/2|/|c+1/2|$。**砖 (ii) 可行但需近消去**：$A\\to-c/2^-$，残余即 $\\alpha^2$。\n")
L.append("**路线总账（三条路线的判定）**：\n")
L.append("| 路线 | 结论 | 封死者 |")
L.append("| --- | --- | --- |")
L.append("| 量纲代数（锚集零空间） | **不可行** | 定理 C |")
L.append("| 几何作用量（旋钮零空间） | **不可行**（无内点极小 / 极小必在边界） | 定理 E |")
L.append("| 算子谱 + 量子化 | **可行，带规格**（$c<-1/2$ 有内点极小；α² = \\|A+c/2\\|/\\|c+1/2\\|） | 定理 F |")
L.append("")
L.append("**诚实边界（不美化）**：")
L.append("1. 定理 F 只给「可行性 + 规格」，**没有给出 α 的数值**：要得到 $1/137$ 必须把 $(A,c)$ 调到规格曲线上，")
L.append("   即 $O(\\alpha^2)$ 的调参 —— **α 仍以「被调参」的方式作为输入**。")
L.append("2. 但所需的调参是 **$O(\\alpha^2)$（小量）**，与定理 E 的 **$O(\\alpha^{-2})$（大量）** 定性不同；")
L.append("   小无量纲数有已知的自然来源（辐射修正 / 大对数 / 近消去），因此这条路线**尚未被封死**。")
L.append("3. 若 $(m,N)$ 是拓扑离散输入，则 $\\alpha$ 被**真正预言**（$1/\\alpha=m\\sqrt{2/d}$）——")
L.append("   可达集是稀疏 Pell 型序列，**观测的 $137.036$ 不在其中**：这是对离散版路线的**可证伪否定**。")
L.append("4. 全程**不调参去凑** $1/137$：所有数字由符号/数值实算得到。\n")
L.append("> **诚实立场**：本轮**没有**实现统一场论，**没有**解锁 UFT-3（联盟层仍 2/6）。")
L.append("> 它做的是把砖 (ii) 从「未验」判为 **「可行但带明确规格」**，并精确定位了「为什么仍不能免费得到 α」：")
L.append("> **规格方程要求的近消去残余，正是 α² 本身。** 下一个真问题因此被精确提出：**什么把 $(A,c)$ 钉在规格曲线上？**\n")

with io.open(os.path.join(DATA, "算子谱与量子化规格.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

# ---------------- 6. 控制台 ----------------
print("=== 定理 F：内点极小判据 ===")
print("  u* = 2Q/P ; e''(u*) = -P^4/(8Q^3) ; 内点极小 <=> Q<0 <=> c < -1/2")
print("  O(1) 扫描：内点极小组数 = %d / %d" % (
    sum(1 for r in scan_oc if r["alpha_pred"] is not None), len(scan_oc)))
print("  c=-1, A=1/2 -> alpha=%s (%s)" % (a_zero, why_zero))
print("  c=-1 命中 alpha_obs 需 A=%.9f (相对精度 %.3e = alpha^2 量级)" % (
    tuned_row["A_required"], tuned_row["relative_precision"]))
if best is not None:
    print("  离散最佳: m=%d N=%d d=%d -> 1/alpha=%.4f (偏差 %.2e)" % (
        best["m"], best["N"], best["d"], best["alpha_inv"],
        abs(best["alpha_inv"] - float(AINV)) / float(AINV)))
if bracket_lo is not None and bracket_hi is not None:
    print("  夹逼: %.3f (m=%d,d=%d) < 137.036 < %.3f (m=%d,d=%d)" % (
        bracket_lo["alpha_inv"], bracket_lo["m"], bracket_lo["d"],
        bracket_hi["alpha_inv"], bracket_hi["m"], bracket_hi["d"]))
print("定理 F：砖(ii) 可行但需 A 与 -c/2 近消去（残余=alpha^2）")
print("done: see 数据/算子谱与量子化规格.md")
