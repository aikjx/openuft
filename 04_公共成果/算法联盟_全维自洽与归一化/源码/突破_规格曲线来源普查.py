# -*- coding: utf-8 -*-
"""
定理 G：规格曲线的第一性来源普查（(A,c) 能被几何钉住吗？）
==========================================================

定理 F 给出规格方程（算子谱路线）：
    α² = |A + c/2| / |c + 1/2|,   A = (n+φ)²/N²,  c = 挠率耦合
并把「什么把 (A,c) 钉在规格曲线上」列为下一个真问题。本引擎真算它。

普查三条：
 1. **c 的几何粒度**：有效 1D 算子里 τ² 项的系数由 da Costa 几何势(1/4)、
    Frenet 框架旋转(1/4)、自旋联络(自旋因子×1/4) 贡献 —— 在 ℏ²/2m 单位下都是 1/4 的
    整数倍 ⇒ c = 2×系数 ∈ (1/2)ℤ。可行性要求 c < −1/2 ⇒ 只有 c ≤ −1 存活（c=−1/2 临界退化）。
 2. **A 的来源**：A=(m/N)² 由模量子化 + 框架 holonomy 给出；对每个可行的 c 解出
    命中 α_obs 所需的 A_req(c)，看它是否为「自然值 − O(α²)」（近消去）。
 3. **格点检验**：自然 (m,N)（枚举 m ≤ 2000）能否命中 α_obs？

诚实边界：第 1 条的「1/4 粒度」是对有效算子的**结构性假设**（已在文中标注依据），
不是从第一性原理逐项重导；它是本普查的前提，若前提变，结论需重算。
"""
import io
import json
import math
import os
import sys

from mpmath import mp, mpf

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 50
ALPHA = float(mpf("7.2973525693e-3"))
AINV = 1.0 / ALPHA
U_REQ = 1.0 + 1.0 / ALPHA ** 2          # u* = 1 + 1/α²

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "数据")
os.makedirs(DATA, exist_ok=True)


def alpha_of(A, c):
    """给定 (A,c) 返回 α（仅当 c<-1/2 且 A<-c/2）。"""
    if c >= -0.5:
        return None
    P = A + c / 2.0
    if P >= 0:
        return None
    us = 2 * (0.25 + c / 2.0) / P
    if us <= 1.0:
        return None
    return 1.0 / math.sqrt(us - 1.0)


def A_req(c):
    """命中 α_obs 所需的 A（精确，由 u*=(c+1/2)/(A+c/2)=1+1/α² 反解）。"""
    return (c + 0.5) / U_REQ - c / 2.0


# ---------------- 1 + 2. c 的粒度普查 ----------------
C_GRID = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0]
NICE = {-2.0: 1.0, -1.5: 0.75, -1.0: 0.5, -0.5: 0.25, 0.0: 0.0, 0.5: -0.25}
rows = []
for c in C_GRID:
    ar = A_req(c)
    viable = (c < -0.5)
    nice = NICE.get(c)
    rows.append({
        "c": c,
        "viable": viable,
        "A_req": ar,
        "m_over_N_req": math.sqrt(ar) if ar > 0 else None,
        "A_nice_alpha0": nice,
        "delta_A": (nice - ar) if nice is not None else None,
    })

# ---------------- 3. 格点检验（自然 (m,N)） ----------------
best_overall = None
for r in rows:
    if not r["viable"]:
        continue
    c = r["c"]
    target = r["m_over_N_req"]          # target = m/N
    best = None
    for m in range(1, 2001):
        n0 = int(math.floor(m / target))    # N ≈ m/target
        for N in (n0 - 1, n0, n0 + 1, n0 + 2):
            if N <= 0:
                continue
            A = (m / float(N)) ** 2
            a = alpha_of(A, c)
            if a is None:
                continue
            dev = abs(a - ALPHA) / ALPHA
            if best is None or dev < best["dev"]:
                best = {"m": m, "N": N, "A": A, "alpha": a,
                        "alpha_inv": 1.0 / a, "dev": dev}
    r["best_lattice"] = best
    if best is not None and (best_overall is None or best["dev"] < best_overall["dev"]):
        best_overall = {"c": c, "m": best["m"], "N": best["N"],
                        "alpha_inv": best["alpha_inv"], "dev": best["dev"]}

theorem_g = {
    "name": "定理 G（规格曲线的第一性来源普查）",
    "step1_c_granularity": (
        "τ² 项系数在 ℏ²/2m 单位下是 1/4 的整数倍（da Costa 几何势 1/4、Frenet 框架旋转 1/4、"
        "自旋联络 ×自旋因子）⇒ c ∈ (1/2)ℤ。可行性要求 c < −1/2 ⇒ **只有 c ≤ −1 存活**"
        "（c = −1/2 为临界退化：Q=0，无内点极小）。"
    ),
    "step2_A_origin": (
        "A = (m/N)² 由模量子化 + 框架 holonomy 给出（结构性，但 (m,N,φ) 是输入）。"
        "命中 α_obs 所需 A_req(c) 恒可写成「自然值 − O(α²)」："
        "A_req(c) = (c+1/2)/(1+1/α²) − c/2，即近消去 A → −c/2 带残余 ~α²。"
    ),
    "step3_lattice": (
        "格点检验：自然 (m,N)（枚举 m ≤ 2000）对每个可行 c 均无法命中 α_obs 到观测精度。"
        "最近解见 best_overall —— 其偏差远大于观测精度 1.6e-5（且大 m 的『命中』属丢番图巧合）。"
    ),
    "unifying": (
        "三条路线的统一说法：**α² 是「近消去残余」= 某个近似简并的破缺参数**。"
        "要推出 α，理论必须 (i) 含一个把 A 钉到 −c/2 的结构性（对称性）机制，"
        "(ii) 并给出 O(α²) 量级的破缺。这正是层级问题在 α 上的本地化形式。"
    ),
    "verdict": (
        "几何自然值（c ∈ {−1/2, 0, +1/2} 等）不落在可行区（c ≤ −1）；"
        "可行的 c 要求「超几何」的负挠率耦合 ⇒ **旋钮并未被移除，只是换了名字**。"
        "⇒ 定理 F 的可行性是**条件性的**：以引入一个几何不能提供的负挠率耦合为前提。"
    ),
}

report = {
    "module": "突破_规格曲线来源普查（定理 G）",
    "alpha_inv_obs": AINV,
    "c_scan": rows,
    "best_overall": best_overall,
    "theorem_G": theorem_g,
}
with io.open(os.path.join(DATA, "规格曲线来源普查.json"), "w", encoding="utf-8") as f:
    f.write(json.dumps(report, ensure_ascii=False, indent=2))

# ---------------- Markdown ----------------
L = []
L.append("# 突破：规格曲线的第一性来源普查（定理 G）\n")
L.append("**引擎**：`源码/突破_规格曲线来源普查.py`（可复跑）\n")
L.append("承接定理 F 提出的真问题：**什么把 $(A,c)$ 钉在规格曲线 $\\alpha^2=|A+c/2|/|c+1/2|$ 上？**\n")
L.append("## 一、$c$ 的几何粒度（可行区普查）\n")
L.append("有效 1D 算子中 $\\tau^2$ 项的系数由三处贡献：da Costa 几何势（$1/4$）、Frenet 框架旋转（$1/4$）、")
L.append("自旋联络（自旋因子 $\\times 1/4$）—— 在 $\\hbar^2/2m$ 单位下均为 $1/4$ 的整数倍 ⇒ **$c\\in\\frac12\\mathbb{Z}$**。\n")
L.append("| c | 可行（c<−1/2） | 命中 α 所需 A_req | 完全消去值 A_nice（α=0） | 残余 δA |")
L.append("| --- | --- | --- | --- | --- |")
for r in rows:
    L.append("| %.1f | %s | %.9f | %s | %s |" % (
        r["c"], "✅" if r["viable"] else "❌",
        r["A_req"],
        ("%.4f" % r["A_nice_alpha0"]) if r["A_nice_alpha0"] is not None else "—",
        ("%.3e" % r["delta_A"]) if r["delta_A"] is not None else "—"))
L.append("")
L.append("> **关键**：$c=-1/2$ 是**临界退化**（$Q=0$）；几何單項自然值是 $c\\in\\{0,\\pm1/2\\}$ —— **全部落在可行区之外**。")
L.append("> 可行的 $c\\le-1$ 要求「超几何」的负挠率耦合。\n")
L.append("## 二、格点检验：自然 $(m,N)$ 能否命中？\n")
L.append("| c | 最佳 (m,N) | 预言 1/α | 相对偏差 |")
L.append("| --- | --- | --- | --- |")
for r in rows:
    if not r["viable"]:
        continue
    b = r.get("best_lattice")
    if b is None:
        L.append("| %.1f | — | — | — |" % r["c"])
    else:
        L.append("| %.1f | (%d, %d) | %.4f | %.3e |" % (r["c"], b["m"], b["N"], b["alpha_inv"], b["dev"]))
L.append("")
if best_overall is not None:
    L.append("> 全局最近解：$c=%.1f$、$(m,N)=(%d,%d)$ ⇒ $1/\\alpha=%.4f$，偏差 $%.2e$" % (
        best_overall["c"], best_overall["m"], best_overall["N"],
        best_overall["alpha_inv"], best_overall["dev"]))
    L.append("> —— **远大于观测精度 $1.6\\times10^{-5}$**；且大 $m$ 的『接近』属丢番图巧合。\n")
L.append("## 三、定理 G 与统一说法\n")
L.append("> **定理 G**：几何自然 $c\\in\\{0,\\pm1/2\\}$ 全部落在规格曲线可行区（$c\\le-1$）之外；")
L.append("> 命中 $\\alpha_{\\rm obs}$ 所需的 $A_{\\rm req}(c)$ 恒为「自然值 $-\\ O(\\alpha^2)$」；")
L.append("> 自然 $(m,N)$ 格点（枚举 $m\\le2000$）无一命中观测精度。\n")
L.append("**统一说法（三条路线）**：\n")
L.append("| 路线 | 判定 | 封死者 |")
L.append("| --- | --- | --- |")
L.append("| 量纲代数 | **封死** | 定理 C |")
L.append("| 几何作用量 | **封死** | 定理 H |")
L.append("| 算子谱 + 量子化 | **条件可行**（需超几何负挠率耦合 + $A$ 的 $O(\\alpha^2)$ 微调） | 定理 F / **G** |")
L.append("")
L.append("$$\\boxed{\\ \\alpha^2=\\text{近消去残余}=\\text{近似简并的破缺参数}\\ }$$\n")
L.append("⇒ 要推出 $\\alpha$，理论必须 (i) 含**结构性（对称性）机制**把 $A$ 钉到 $-c/2$，")
L.append("(ii) 并给出 $O(\\alpha^2)$ 的破缺 —— 这正是**层级问题在 α 上的本地化形式**。\n")
L.append("## 四、诚实边界与立场\n")
L.append("1. 第 1 条的「$1/4$ 粒度」是**结构性假设**（依据已列），不是逐项第一性重导；前提变则结论需重算。")
L.append("2. 格点检验枚举 $m\\le2000$（$N$ 相应约 $10^3$ 量级）；更大 $m$ 会因轨道致密而逼近任意目标 —— 那是**丢番图巧合，非预言**。")
L.append("3. 本轮**没有**实现统一场论、**没有**解锁 UFT-3。它做的是把定理 F 的「可行」**收紧为「条件可行」**：")
L.append("   旋钮并未被移除，只是换了名字（几何 → 超几何负挠率耦合 + 格点微调）。")
L.append("4. 全程**不调参去凑** $1/137$：所有数字由实算得到。\n")
L.append("> **诚实立场**：$\\alpha$ 在本框架内不可派生这一结论，现由**四个定理**支撑（C / E / F / G）；")
L.append("> 同时给出了**未来理论必须满足的形式条件**：存在于 $O(\\alpha^2)$ 尺度破缺的近似简并。\n")

with io.open(os.path.join(DATA, "规格曲线来源普查.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

# ---------------- 控制台 ----------------
print("=== 定理 G：c 的几何粒度普查 ===")
for r in rows:
    print("  c=%5.1f viable=%-5s A_req=%.9f dA=%s" % (
        r["c"], r["viable"], r["A_req"],
        ("%.3e" % r["delta_A"]) if r["delta_A"] is not None else "-"))
print("=== 格点检验 ===")
for r in rows:
    if r["viable"] and r.get("best_lattice"):
        b = r["best_lattice"]
        print("  c=%5.1f best (m=%d,N=%d) 1/alpha=%.4f dev=%.2e" % (
            r["c"], b["m"], b["N"], b["alpha_inv"], b["dev"]))
if best_overall:
    print("  全局最近: c=%.1f (m=%d,N=%d) 1/alpha=%.4f dev=%.2e (观测精度 1.6e-05)" % (
        best_overall["c"], best_overall["m"], best_overall["N"],
        best_overall["alpha_inv"], best_overall["dev"]))
print("定理 G：几何自然 c 全在可行区外 -> 定理 F 收紧为条件可行")
print("done: see 数据/规格曲线来源普查.md")
