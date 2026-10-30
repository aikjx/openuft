# -*- coding: utf-8 -*-
"""
71 号仪器 · 电磁扇区候选精确解 A = λT 的检验（含证伪与修正候选）

背景
----
26 号正典把 UFE-2 的三条本构式钉死为
    C-01  ∂_t²A = (1/f)[V(∇·E) − c²∇×𝓑]
    C-02  ∇×A = 𝓑/f
    C-03  E = −f ∂_t A
69 号给出标架层精确桥 ∇×T = τT + κB_frame（κ = α²/ρ, τ = αβ/ρ）。
本仪器检验候选解 A = λT（λ 常数、静态）是否为**真空**静磁解。

关键修正（相对初版）
--------------------
1) 螺旋标架必须归一化：T = αê_φ + βẑ、B = αẑ − βê_φ 正交归一要求 α²+β² = 1。
   初版把 α、β 当作自由符号，导致 κ²+τ² 等关系全部带 (α²+β²) 残差。
   本版用螺距角参数化 α = sinθ、β = cosθ，归一化自动成立（θ ∈ (0, π/2)）。
2) 控制组初版只查 ẑ 分量，而轴对称场 (1/ρ)ẑ 的旋度恰好只有 ê_φ 分量，
   故"控制组"恒为零 ⇒ 假阴性。本版一律查**全矢量**。
3) 结论（读数见下）：候选解 A = λT **不是**真空解，E3/E6/E7b 被证伪；
   真正的无源解是 A = λρ ê_φ（均匀 𝓑 = 2fλ ẑ），见 MC 组。

判定项
------
G1/G2  标架旋度   ∇×T = (α/ρ)ẑ, ∇×B_frame = −(β/ρ)ẑ
G3     标架桥     ∇×T = τT + κB_frame（69 号桥，兼作仪器自检）
E3     承重式     ∇×(τT + κB_frame) = 0   ← 候选解的承重恒等式
E4     无散       ∇·(τT + κB_frame) = 0
E5     模长       |τT + κB|² = κ²+τ² = α²/ρ²
E6     本构式     三本构式 + 无源麦克斯韦同时满足
E7a    能流       S = E×𝓑 = 0
E7b    能量密度   u = 𝓑²/(2μ0) 与位置无关
MC1..5 修正候选    A = λρ ê_φ ⇒ 𝓑 = 2fλ ẑ（均匀），全项成立

控制组
------
CT1  去掉归一化 α²+β²=1 ⇒ 标架桥必须失效（证明归一化必要）
CT2  系数互换 κT + τB ⇒ 标架桥必须失效（证明 T、B 角色不可换）
CT3  换成 A = λB_frame ⇒ ∇×𝓑 同样非零（证明失败不是"选了 T"的偶然）
CT4  退化极限 α=0（T = ẑ 直线）⇒ 𝓑 ≡ 0，只剩平凡解

依赖 sympy。运行：python -B em_sector_exact_solution.py [--quiet]
"""

from __future__ import annotations

import json
import os
import sys
import unicodedata

try:
    import sympy as sp
    from sympy.vector import CoordSys3D, curl, divergence
except ImportError:  # pragma: no cover
    print("SKIP: 需要 sympy")
    sys.exit(2)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "em_sector_exact_solution_results.json")
OUT_TXT = os.path.join(HERE, "em_sector_exact_solution_out.txt")

RESULTS: list[dict] = []


def rec(sid, title, tex, kind, verdict, detail, group="E"):
    RESULTS.append({"id": sid, "group": group, "title": title, "tex": tex,
                    "kind": kind, "verdict": verdict, "detail": detail})


# ---------------------------------------------------------------- 几何设置
C = CoordSys3D("C", transformation="cylindrical",
               variable_names=("rho", "phi", "z"))
rho = C.rho

th = sp.Symbol("theta", positive=True)          # 螺距角
a = sp.sin(th)                                  # α
b = sp.cos(th)                                  # β   ⇒ α² + β² ≡ 1
lam, f, mu0 = sp.symbols("lambda f mu_0", positive=True)

T = a * C.j + b * C.k                           # 切矢   T = αê_φ + βẑ
Bf = a * C.k - b * C.j                          # 副法矢 B = αẑ − βê_φ
kappa = a**2 / rho                              # 曲率
tau = a * b / rho                               # 挠率

BASES = (C.i, C.j, C.k)


def comps(v):
    """把矢量拆成 (ê_ρ, ê_φ, ẑ) 分量并三角化简。"""
    return tuple(sp.simplify(sp.trigsimp(sp.expand(v.dot(e)))) for e in BASES)


def simp(v):
    """矢量化简：分量化简后重新组装。"""
    out = sp.vector.Vector.zero
    for c, e in zip(comps(v), BASES):
        out += c * e
    return out


def simp0(x):
    """标量化简。"""
    return sp.simplify(sp.trigsimp(sp.expand(x)))


def is_zero(v) -> bool:
    return all(c == 0 for c in comps(v))


def is_nonzero(v) -> bool:
    return not is_zero(v)


# 顺序敏感：先吃掉带幂的三角函数（sin(theta)**2 → sin²θ），
# 再处理裸三角函数，最后才把剩下的 **2 变成上标。
_SUBS = [
    ("sin(theta)**2", "sin²θ"),
    ("cos(theta)**2", "cos²θ"),
    ("sin(theta)**3", "sin³θ"),
    ("cos(theta)**3", "cos³θ"),
    ("sin(theta)", "sinθ"),
    ("cos(theta)", "cosθ"),
    ("theta", "θ"),
    ("C.rho", "ρ"),
    ("C.i", "ê_ρ"),
    ("C.j", "ê_φ"),
    ("C.k", "ẑ"),
    ("mu_0", "μ₀"),
    ("lambda", "λ"),
    ("**2", "²"),
    ("**3", "³"),
    ("*", "·"),
]


def fmt(x) -> str:
    """把 sympy 表达式打印成紧凑可读形式。"""
    s = sp.sstr(x)
    for old, new in _SUBS:
        s = s.replace(old, new)
    while "  " in s:
        s = s.replace("  ", " ")
    return s.strip()


# ================================================================ G 组：标架层
cT = simp(curl(T, C))
cB = simp(curl(Bf, C))

rec("G1", "切矢旋度 ∇×T = (α/ρ) ẑ",
    r"\nabla\times\mathbf T=(\alpha/\rho)\hat z", "IDN",
    "PASS" if is_zero(cT - (a / rho) * C.k) else "FAIL",
    f"∇×T = {fmt(cT)}", group="G")

rec("G2", "副法矢旋度 ∇×B = −(β/ρ) ẑ",
    r"\nabla\times\mathbf B_{\rm frame}=-(\beta/\rho)\hat z", "IDN",
    "PASS" if is_zero(cB + (b / rho) * C.k) else "FAIL",
    f"∇×B = {fmt(cB)}", group="G")

combo = simp(tau * T + kappa * Bf)              # = ∇×T（若桥成立）
rec("G3", "标架桥 ∇×T = τT + κB（69 号，兼仪器自检）",
    r"\nabla\times\mathbf T=\tau\mathbf T+\kappa\mathbf B", "IDN",
    "PASS" if is_zero(cT - combo) else "FAIL",
    f"τT+κB = {fmt(combo)}，与 ∇×T = {fmt(cT)} 一致", group="G")

# ================================================================ E 组：候选解
c_combo = simp(curl(combo, C))
rec("E3", "承重式 ∇×(τT + κB) = 0",
    r"\nabla\times(\tau\mathbf T+\kappa\mathbf B_{\rm frame})=\mathbf 0", "IDN",
    "PASS" if is_zero(c_combo) else "FAIL",
    f"∇×(τT+κB) = {fmt(c_combo)} ≠ 0 —— 因 τT+κB = (sinθ/ρ)ẑ，"
    f"其旋度只剩 ê_φ 分量 sinθ/ρ²", group="E")

d_combo = simp0(divergence(combo, C))
rec("E4", "无散 ∇·(τT + κB) = 0",
    r"\nabla\cdot(\tau\mathbf T+\kappa\mathbf B_{\rm frame})=0", "IDN",
    "PASS" if d_combo == 0 else "FAIL",
    f"∇·(τT+κB) = {fmt(d_combo)}", group="E")

mag2 = simp0(combo.dot(combo))
res5 = simp0(mag2 - (kappa**2 + tau**2))
res5b = simp0(kappa**2 + tau**2 - a**2 / rho**2)
rec("E5", "模长 |τT + κB|² = κ²+τ² = α²/ρ²",
    r"|\tau\mathbf T+\kappa\mathbf B|^2=\kappa^2+\tau^2=\alpha^2/\rho^2", "IDN",
    "PASS" if (res5 == 0 and res5b == 0) else "FAIL",
    f"|combo|² = {fmt(mag2)}；κ²+τ² 残差 = {fmt(res5)}；α²/ρ² 残差 = {fmt(res5b)}",
    group="E")

# E6 · 三本构式 + 无源麦克斯韦（A = λT）
Bfield = simp(f * lam * combo)                  # 𝓑 = f ∇×A = fλ(τT+κB)
curl_B = simp(curl(Bfield, C))
div_B = simp0(divergence(Bfield, C))
J_req = simp(curl_B / mu0)
ok_E6 = is_zero(curl_B) and div_B == 0
rec("E6", "三本构式 + 无源麦克斯韦同时满足（A = λT）",
    r"\text{三本构式}+\text{无源麦克斯韦}", "RES",
    "PASS" if ok_E6 else "FAIL",
    f"𝓑 = {fmt(Bfield)}；∇×𝓑 = {fmt(curl_B)} ≠ 0；∇·𝓑 = {fmt(div_B)}。"
    f"C-03 与 C-02 成立（E=0、𝓑≡f∇×A），但 C-01 静态式要求 ∇×𝓑=0 ⇒ 矛盾。"
    f"若取 ∇×𝓑=μ₀J，则所需体电流 J = {fmt(J_req)}", group="E")

# E7a / E7b（拆开：能流与能量密度是两件事）
rec("E7a", "能流 S = E×𝓑 = 0",
    r"\mathbf S=\mathbf E\times\mathcal B=\mathbf 0", "RES",
    "PASS",
    "E = −f∂_t(λT) = 0（静态）⇒ S ≡ 0，无条件成立", group="E")

u_rho = simp0(mag2 * f**2 * lam**2 / (2 * mu0))
u_uniform = (u_rho == simp0(u_rho.subs(rho, 1)))   # 与 ρ 无关与否
rec("E7b", "能量密度 u = 𝓑²/(2μ₀) 与位置无关",
    r"u=\mathcal B^2/(2\mu_0)\ \text{与位置无关}", "RES",
    "PASS" if u_uniform else "FAIL",
    f"u = {fmt(u_rho)} ∝ 1/ρ²，随 ρ 变化 ⇒「处处相等」为假", group="E")

# ================================================================ MC 组：修正候选
# 轴对称静态无源解的通解：𝓑 = c₀ẑ + (c₁/ρ)ê_φ（轴上有源时才有 1/ρ 项）。
# 真正无源且轴上正则的解是均匀场，其矢势 A = λρ ê_φ = −λρ N（沿法矢、幅值 ∝ ρ）。
A_mc = lam * rho * C.j
B_mc = simp(f * curl(A_mc, C))
curl_B_mc = simp(curl(B_mc, C))
div_B_mc = simp0(divergence(B_mc, C))

rec("MC1", "A = λρ ê_φ ⇒ 𝓑 = 2fλ ẑ（均匀）",
    r"A=\lambda\rho\hat e_\phi\Rightarrow\mathcal B=2f\lambda\hat z", "IDN",
    "PASS" if is_zero(B_mc - 2 * f * lam * C.k) else "FAIL",
    f"∇×A = {fmt(simp(curl(A_mc, C)))}，𝓑 = {fmt(B_mc)}", group="MC")

rec("MC2", "无源：∇×𝓑 = 0 且 ∇·𝓑 = 0",
    r"\nabla\times\mathcal B=\mathbf 0,\ \nabla\cdot\mathcal B=0", "IDN",
    "PASS" if (is_zero(curl_B_mc) and div_B_mc == 0) else "FAIL",
    f"∇×𝓑 = {fmt(curl_B_mc)}，∇·𝓑 = {fmt(div_B_mc)}", group="MC")

rec("MC3", "三本构式 C-01 / C-02 / C-03 同时成立",
    r"\text{C-01/C-02/C-03 同时成立}", "RES",
    "PASS" if (is_zero(curl_B_mc) and div_B_mc == 0) else "FAIL",
    "E = −f∂_tA = 0 ⇒ C-03 恒真、∇·E = 0；C-02 由 𝓑 ≡ f∇×A 构造成立；"
    "静态 C-01：0 = (1/f)[V·0 − c²∇×𝓑] = 0，因 ∇×𝓑 = 0", group="MC")

u_mc = simp0(B_mc.dot(B_mc) / (2 * mu0))
rec("MC4", "u 均匀且 S = 0",
    r"u=\mathcal B^2/(2\mu_0)\ \text{均匀；}\ \mathbf S=\mathbf 0", "RES",
    "PASS" if (u_mc == simp0(u_mc.subs(rho, 1))) else "FAIL",
    f"u = {fmt(u_mc)}（与 ρ 无关）；S = E×𝓑 = 0", group="MC")

frame_form = simp(B_mc - 2 * f * lam * (b * T + a * Bf))
frame_form2 = simp(B_mc - 2 * f * lam * (rho / a) * combo)
rec("MC5", "𝓑 = 2fλ(βT + αB) = 2fλ(ρ/α)(τT + κB)",
    r"\mathcal B=2f\lambda(\beta\mathbf T+\alpha\mathbf B)"
    r"=2f\lambda\frac{\rho}{\alpha}(\tau\mathbf T+\kappa\mathbf B)", "IDN",
    "PASS" if (is_zero(frame_form) and is_zero(frame_form2)) else "FAIL",
    f"残差(βT+αB) = {fmt(frame_form)}；残差((ρ/α)(τT+κB)) = {fmt(frame_form2)}"
    f" ⇒ 均匀场正是 τT+κB 方向，但权重 ∝ ρ（而非 λ = 常数）", group="MC")

# ================================================================ 控制组
# CT1 · 不做归一化：α,β 自由 ⇒ 桥必须失效
a2, b2 = sp.symbols("alpha beta", positive=True)
T2 = a2 * C.j + b2 * C.k
Bf2 = a2 * C.k - b2 * C.j
bridge2 = simp(curl(T2, C) - (a2 * b2 / rho * T2 + a2**2 / rho * Bf2))
rec("CT1", "控制组：去掉归一化 α²+β²=1 ⇒ 标架桥必须失效",
    r"\text{去归一化} \Rightarrow \text{桥失效}", "CTRL",
    "PASS" if is_nonzero(bridge2) else "FAIL",
    f"残差 = {fmt(bridge2)} ∝ 1−α²−β² ⇒ |T| = 1 是桥成立的必要条件",
    group="CT")

# CT2 · 系数互换 κT + τB ⇒ 桥必须失效
combo2 = simp(kappa * T + tau * Bf)
rec("CT2", "控制组：系数互换 κT+τB ⇒ 标架桥必须失效",
    r"\kappa\mathbf T+\tau\mathbf B \neq \nabla\times\mathbf T", "CTRL",
    "PASS" if is_nonzero(combo2 - cT) else "FAIL",
    f"κT+τB = {fmt(combo2)}，与 ∇×T = {fmt(cT)} 不等 ⇒ T、B 角色不可互换",
    group="CT")

# CT3 · 换成 A = λB_frame：同样不是真空解
B_alt = simp(f * lam * curl(Bf, C))
curl_B_alt = simp(curl(B_alt, C))
rec("CT3", "控制组：换成 A = λB ⇒ ∇×𝓑 同样非零",
    r"A=\lambda\mathbf B_{\rm frame}\Rightarrow\nabla\times\mathcal B\neq 0",
    "CTRL",
    "PASS" if is_nonzero(curl_B_alt) else "FAIL",
    f"𝓑 = {fmt(B_alt)}，∇×𝓑 = {fmt(curl_B_alt)} ⇒ A=λT 的失败不是「选了 T」的偶然",
    group="CT")

# CT4 · 退化极限 α = 0（T = ẑ，无螺旋）：𝓑 ≡ 0，只剩平凡解
B_deg = simp(Bfield.subs(th, 0))
rec("CT4", "控制组：退化极限 α=0 ⇒ 𝓑 ≡ 0（只剩平凡解）",
    r"\alpha=0\Rightarrow\mathcal B\equiv\mathbf 0", "CTRL",
    "PASS" if is_zero(B_deg) else "FAIL",
    f"𝓑|_(α=0) = {fmt(B_deg)} ⇒ 螺旋度是场强的唯一来源，代价是 ∇×𝓑 ≠ 0",
    group="CT")

# ================================================================ 诊断（不计 PASS/FAIL）
rec("D1", "诊断：轴对称静态无源场的通解", "", "INFO", "INFO",
    "∂_φ = ∂_z = 0 下 ∇·𝓑 = 0 ⇒ B_ρ = c/ρ；∇×𝓑 = 0 ⇒ B_z = 常数、B_φ = c′/ρ。"
    "轴上正则 ⇒ c = c′ = 0 ⇒ 𝓑 只能是均匀场（MC 组）。"
    "A = λT 给出 𝓑 ∝ (1/ρ)ẑ，落在「需体电流 J ∝ 1/ρ² ê_φ」的一族里，不是真空解。",
    group="D")

rec("D2", "诊断：候选解被证伪的根源", "", "INFO", "INFO",
    "τT+κB = ∇×T = (sinθ/ρ)ẑ。承重式 E3 要求 ∇×∇×T = 0，"
    "但 ∇×((sinθ/ρ)ẑ) = (sinθ/ρ²)ê_φ ≠ 0。即：沿切矢的矢势必然携带 1/ρ 型轴向场，"
    "而任何 1/ρ 型轴向场的旋度都不为零 ⇒ 与 C-01 静态真空式不相容。", group="D")

# ================================================================ 排版输出
WIDTH = 78
GROUPS = [
    ("G",  "几何层 · 螺旋标架恒等式（兼仪器自检）"),
    ("E",  "候选解 A = λT 的承重检验"),
    ("MC", "修正候选 A = λρ ê_φ（真正的无源解）"),
    ("CT", "控制组"),
    ("D",  "诊断（不计入 PASS/FAIL）"),
]


def dwidth(s: str) -> int:
    """终端显示宽度：中日韩全角字符按 2 计。"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def _is_atom(ch: str) -> bool:
    """是否属于不可断开的「数学原子」（如 (sinθ/ρ)·ẑ）。"""
    if ch.isascii() and (ch.isalnum() or ch in "(){}[]/·^+_.,-=²³"):
        return True
    o = ord(ch)
    return (0x0370 <= o <= 0x03FF          # 希腊字母
            or 0x00C0 <= o <= 0x024F       # Latin-1 补充 / Latin Ext
            or 0x1E00 <= o <= 0x1EFF       # Latin Extended Additional
            or 0x2070 <= o <= 0x209F        # 上标下标
            or 0x2190 <= o <= 0x22FF       # 箭头与数学运算符
            or 0x1D400 <= o <= 0x1D7FF)    # 数学字母符号（𝓑）


def _tokenize(text: str) -> list[str]:
    """切成数学原子与可逐字断开的 CJK 字符。"""
    toks: list[str] = []
    buf = ""
    for ch in text:
        if _is_atom(ch):
            buf += ch
        else:
            if buf:
                toks.append(buf)
                buf = ""
            toks.append(ch)
    if buf:
        toks.append(buf)
    return toks


def wrap(text: str, indent: str, width: int = WIDTH) -> list[str]:
    """按显示宽度折行：数学原子整体搬运，CJK 逐字断开，保留悬挂缩进。"""
    limit = width - dwidth(indent)
    lines: list[str] = []
    line = ""
    for tok in _tokenize(text):
        if tok == "\n":
            lines.append(line)
            line = ""
            continue
        if line and dwidth(line) + dwidth(tok) > limit:
            lines.append(line.rstrip())
            line = "" if tok.isspace() else tok
        else:
            line += tok
    lines.append(line.rstrip())
    return [indent + s for s in lines if s.strip()] or [indent.rstrip()]


def bar(ch: str = "=") -> str:
    return ch * WIDTH


def rule(head: str, tail: str = "") -> str:
    """画一条带标题的横向分隔线：── head ──────── tail"""
    pad = max(0, WIDTH - dwidth(head) - dwidth(tail))
    return head + "─" * pad + tail


by_group: dict[str, list[dict]] = {g: [] for g, _ in GROUPS}
for item in RESULTS:
    by_group.setdefault(item["group"], []).append(item)

lines = [
    bar(),
    "71 号仪器 · 电磁扇区候选精确解 A = λT 的读数",
    bar(),
    "本构式  C-01 ∂_t²A = (1/f)[V(∇·E) − c²∇×𝓑]   C-02 ∇×A = 𝓑/f   C-03 E = −f ∂_t A",
    "标架    α = sinθ, β = cosθ（α²+β² = 1）；κ = α²/ρ, τ = αβ/ρ",
    bar(),
]

for tag, name in GROUPS:
    items = by_group.get(tag, [])
    if not items:
        continue
    n_p = sum(1 for x in items if x["verdict"] == "PASS")
    n_f = sum(1 for x in items if x["verdict"] == "FAIL")
    n_i = sum(1 for x in items if x["verdict"] == "INFO")
    parts = [f"{n_p}P"] if n_p else []
    parts += [f"{n_f}F"] if n_f else []
    parts += [f"{n_i}I"] if n_i else []
    lines.append(rule(f"── {tag} · {name} ", "[" + "/".join(parts) + "]"))

    for x in items:
        lines.append(f"  [{x['verdict']:4s}] {x['id']:4s} ({x['kind']}) {x['title']}")
        lines.extend(wrap(x["detail"], " " * 12))
    lines.append("")

n_pass = sum(1 for x in RESULTS if x["verdict"] == "PASS")
n_fail = sum(1 for x in RESULTS if x["verdict"] == "FAIL")
verdicts = {x["id"]: x["verdict"] for x in RESULTS}
if verdicts.get("E3") == "FAIL" and all(
        verdicts.get(k) == "PASS" for k in ("MC1", "MC2", "MC3", "MC4", "MC5")):
    concl = ("结论：候选解 A = λT 被证伪（∇×(τT+κB) = (sinθ/ρ²) ê_φ ≠ 0，与 C-01 静态真空式矛盾）；"
             "轴对称无源正则解只能是均匀场 𝓑 = 2fλ ẑ，由 A = λρ ê_φ 给出。")
else:
    concl = "结论：见上表读数（与上轮不一致，请复核）。"

lines += [bar()]
lines += wrap(concl, "  ")
lines.append(bar())
lines.append(f"合计 {n_pass + n_fail} 条判定：PASS {n_pass} / FAIL {n_fail}"
             f" ⇒ exit {1 if n_fail else 0}")

summary = {
    "doc": "71_电磁扇区精确解_矢势沿螺旋切矢_攻破与修正候选_2026-10-30.md",
    "tool": os.path.basename(__file__),
    "total": n_pass + n_fail,
    "pass": n_pass,
    "fail": n_fail,
    "exit_code": 1 if n_fail else 0,
    "conclusion": concl,
    "items": RESULTS,
}

with open(OUT_JSON, "w", encoding="utf-8") as g:
    json.dump(summary, g, ensure_ascii=False, indent=2)
with open(OUT_TXT, "w", encoding="utf-8") as g:
    g.write("\n".join(lines) + "\n")

if "--quiet" not in sys.argv:
    print("\n".join(lines))

sys.exit(summary["exit_code"])
