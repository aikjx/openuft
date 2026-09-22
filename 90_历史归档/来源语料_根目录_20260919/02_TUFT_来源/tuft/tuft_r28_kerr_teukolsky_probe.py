# -*- coding: utf-8 -*-
"""
TUFT · R28 —— Kerr/Teukolsky 推广：第一性结构探测 v2（machinery 已修复并通过自检）
================================================================================
R20–R24（时域/Prony，~1e-3）→ R25（Schwarzschild Leaver 连分式，≤1e-6）
→ R26（全维验证；RW=3 项、Zerilli=5 项）→ R27（SUSY 证明 RW↔Zerilli 等谱）
→ **R28：向旋转 Kerr 推广（Teukolsky 方程）。**

v1 曾"自检失败"；**v2 已定位并修复根因**，machinery 现通过自检，结论可信。

  V1  Teukolsky 径向方程正确建立：a→0、s=0 的标量极限与 Schwarzschild 无质量标量
      径向方程**符号恒等**（相减恰为 0）⇒ 方程本身无误。
  V2  **修复并通过自检**：v1 的 BUG 是**先除以 A**（=f²）以化为标准形；而 f=y 使
      A→0 于 y=0，**人为引入 1/y² 极点**，把本应 (2,2,2) 的结构抬高为 (3,2,1)。
      改为**不除以 A**、并**自动判定 A 在 y=0 的零点阶 p**（RW: A=f² 为双零点 p=2；
      Teukolsky: A=Δ 为单零点 p=1）后，对 RW 复算得 (1−y)² 清净、次数 (2,2,2)
      ⇒ **递推阶数=3，与 R25 的 3 项守恒一致** ⇒ 自检通过。
  V3  修复后的 machinery 对 Teukolsky(a=0,s=−2)（标准 Leaver ansatz
      u=−s−iσ₊=−s−2iMω、v=−1+s）得 (1−y)⁵ 清净、次数 (3,3,3) ⇒ **递推阶数=4**。
      即：**Teukolsky 径向方程在该 ansatz 下是 4 项递推，不是 3 项** ⇒
      R25 的单连分式**不能**直接移植到 Kerr；需 Nollert 广义(矩阵)连分式，或先变换到
      3 项形式（如 Sasaki-Nakamura / Teukolsky→RW 型变换）。

按 TUFT 红线：仍**不产出 Kerr QNM 数值**（未实现广义连分式），只给结构结论。

几何单位 G=c=M=1。评级：C / L2。
"""
from __future__ import print_function
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_r28_report.txt")

import sympy as sp

P = F = B = Icnt = 0
lines = []


def P_(m):
    global P; P += 1; lines.append("[PASS] " + m)


def F_(m):
    global F; F += 1; lines.append("[FAIL] " + m)


def B_(m):
    global B; B += 1; lines.append("[BOUNDARY] " + m)


def I_(m):
    global Icnt; Icnt += 1; lines.append("[INFO] " + m)


def recurrence_order(A_rs, B_rs, C_rs, u, v, kmax=7):
    """修复版 machinery：不除以 A，自动判定 p=A 在 y=0 的零点阶。

    R'(r)=q R_y, R''(r)=q q_y R_y + q^2 R_yy  =>  A R_yy + (A q_y/q + B/q) R_y + (C/q^2) R = 0
    提因子 R=e^{iωr}(r-rp)^u(r-rm)^v S(y), rho = iω dr/dy + u/y + (u+v)/(1-y)：
        A S'' + (2A rho + Bbar) S' + (A(rho^2+rho') + Bbar rho + Cbar) S = 0
    正规奇点结构 A ~ y^p * At ⇒ 递推阶数 = max(deg At, deg Bt, deg Ct) + 1，
    At=A/y^p, Bt=(S'系数)/y^(p-1), Ct=(S系数)/y^(p-2)。3 项 ⇔ 该最大值 = 2。
    返回 (阶数, p, k, 次数元组) 或 (None, p, None, None)。
    """
    subs = {rs: ry}
    A_ = sp.simplify(A_rs.subs(subs))
    B_ = sp.simplify(B_rs.subs(subs))
    C_ = sp.simplify(C_rs.subs(subs))
    Bbar = sp.simplify(A_ * sp.diff(q, y) / q + B_ / q)
    Cbar = sp.simplify(C_ / q ** 2)
    rho = sp.I * om * D0 / (1 - y) ** 2 + u / y + (u + v) / (1 - y)
    c2 = A_
    c1 = sp.simplify(2 * A_ * rho + Bbar)
    c0 = sp.simplify(A_ * (rho ** 2 + sp.diff(rho, y)) + Bbar * rho + Cbar)
    p = None
    for j in range(0, 5):
        fr = sp.fraction(sp.cancel(c2 / y ** j))
        if sp.simplify(fr[1].subs(y, 0)) != 0 and sp.simplify(fr[0].subs(y, 0)) != 0:
            p = j
            break
    if p is None:
        return None, None, None, None
    for k in range(0, kmax):
        e2 = sp.cancel(c2 * (1 - y) ** k / y ** p)
        e1 = sp.cancel(c1 * (1 - y) ** k / y ** (p - 1))
        e0 = sp.cancel(c0 * (1 - y) ** k / y ** (p - 2))
        if all(sp.simplify(sp.fraction(e)[1].subs(y, 0)) != 0 for e in (e2, e1, e0)):
            degs = []
            for e in (e2, e1, e0):
                fr = sp.fraction(e)
                if y in fr[1].free_symbols:
                    degs = None
                    break
                degs.append(sp.degree(sp.expand(fr[0] / fr[1]), y))
            if degs is not None:
                return max(degs) + 1, p, k, tuple(degs)
    return None, p, None, None


def main():
    lines.append("=" * 70)
    lines.append("TUFT R28 · Kerr/Teukolsky 结构探测 v2（machinery 已修复并通过自检）")
    lines.append("=" * 70)
    I_("几何单位 G=c=M=1")

    # ── V1 ──
    I_("§V1 符号：Teukolsky 径向方程 a->0 且 s=0 的标量极限")
    R = sp.Function("R")(rs)
    Delta = rs ** 2 - 2 * M * rs
    eq_teu = sp.expand(Delta * sp.diff(R, rs, 2) + sp.diff(Delta, rs) * sp.diff(R, rs)
                       + ((om * rs ** 2) ** 2 / Delta - L * (L + 1)) * R)
    f_sym = 1 - 2 * M / rs
    eq_sca = sp.expand(rs ** 2 * f_sym * sp.diff(R, rs, 2) + (2 * rs - 2 * M) * sp.diff(R, rs)
                       + (rs ** 2 * om ** 2 / f_sym - L * (L + 1)) * R)
    diff_sym = sp.simplify(sp.cancel(eq_teu - eq_sca))
    I_("  Teukolsky(a=0,s=0)：ΔR''+Δ'R'+[K²/Δ−λ]R，Δ=r²−2Mr，K=ωr²")
    I_("  独立标量方程：r²fR''+(2r−2M)R'+[r²ω²/f−l(l+1)]R")
    I_("  两者之差 = %s" % diff_sym)
    if diff_sym == 0:
        P_("V1 Teukolsky 径向方程正确建立：a→0,s=0 与 Schwarzschild 无质量标量径向方程符号恒等"
           "（Δ=r²−2Mr ⇒ K²/Δ=ω²r²/f、Δ'=2r−2M），方程本身无误")
    else:
        F_("V1 Teukolsky 径向方程的标量极限与标量方程不一致：%s" % diff_sym)

    # ── V2 修复并自检 ──
    I_("§V2 修复后 machinery 自检：对 RW（R25 已知 3 项）复算")
    I_("  v1 BUG：先除以 A(=f²) 化标准形；f=y 使 A→0 于 y=0，人为引入 1/y² 极点"
       " ⇒ 得 (3,2,1)。v2：不除以 A，并自动判定 p（A 在 y=0 的零点阶）")
    f_ = 1 - 2 * M / rs
    Vrw = f_ * (6 / rs ** 2 - 6 * M / rs ** 3)
    o1, p1, k1, dg1 = recurrence_order(f_ ** 2, f_ * sp.diff(f_, rs), om ** 2 - Vrw,
                                       -2 * sp.I * M * om, 4 * sp.I * M * om)
    I_("  RW：p=%s ；最小清分母 (1−y)^%s ；约化次数=%s" % (p1, k1, dg1))
    if o1 == 3:
        P_("V2 machinery **修复后自检通过**：RW 复算得递推阶数=3（次数 (2,2,2) 清净于 (1−y)²），"
           "与 R25 的 3 项递推**一致** ⇒ v1 的偏差根因确认为『先除以 A 引入人为极点』，已修复")
    else:
        F_("V2 machinery 自检仍未通过：RW 阶数=%s（期望 3）" % o1)

    # ── V3 ──
    I_("§V3 修复后 machinery 对 Teukolsky(a=0,s=−2)（Leaver ansatz u=−s−2iMω, v=−1+s）")
    s = sp.Integer(-2)
    Dlt = rs ** 2 - 2 * M * rs
    KK = om * rs ** 2
    VT = KK ** 2 / Dlt - 2 * sp.I * s * (rs - M) * KK / Dlt + 4 * sp.I * s * om * rs - 4
    o2, p2, k2, dg2 = recurrence_order(Dlt, (s + 1) * sp.diff(Dlt, rs), VT,
                                       -s - sp.I * 2 * M * om, -1 + s)
    I_("  Teukolsky：p=%s（A=Δ 为单零点）；最小清分母 (1−y)^%s ；约化次数=%s" % (p2, k2, dg2))
    if o2 == 3:
        P_("V3 Teukolsky(a=0,s=−2) 为 3 项递推 ⇒ 可直接移植 R25 的 Leaver 连分式")
    else:
        B_("V3 Teukolsky(a=0,s=−2) 递推阶数=%s（次数 %s）⇒ **不是 3 项**。故 R25 的单连分式"
           "**不能**直接移植到 Kerr：需 Nollert 广义(矩阵)连分式，或先经 Sasaki-Nakamura / "
           "Teukolsky→RW 型变换化到 3 项形式。本册未实现 ⇒ **不产出 Kerr QNM 数值**" % (o2, dg2))

    # ── C1 ──
    I_("§C1 结构与后续")
    I_("  Teukolsky：ΔR''+(s+1)Δ'R'+[K²/Δ−2is(r−M)K/Δ+4isωr−λ]R=0，Δ=r²−2Mr+a²，"
       "K=(r²+a²)ω−ma，λ=A+a²ω²−2amω，s=−2")
    I_("  正规奇点 r=r_±=M±√(M²−a²) 与 ∞；视界指标指数 {0,−s}（indicial Dλ(λ+s)=0）；"
       "σ±=(ω(r±²+a²)−ma)/(r₊−r₋)")
    I_("  关键结构差异：RW 的 A=f² 在 y=0 为**双零点**(p=2)；Teukolsky 的 A=Δ 为**单零点**(p=1)，"
       "且 K²/Δ 在 r→∞ 不衰减（∝r²），故 y=1 处奇性更重（需 (1−y)^5 清净）")

    B_("边界①：本册**不含任何 Kerr QNM 数值**，未实现广义连分式/角向本征值联动")
    B_("边界②：V1 仅核对 a=0,s=0 标量极限；s=±2 的 −2is(r−M)K/Δ、4isωr 项未被独立验证")
    B_("边界③：V3 只做 a=0；Kerr(a≠0) 时 aa=ma≠0、r₋≠0，奇性结构可能进一步变化，未测")
    B_("边界④：Kerr 还需角向自旋权椭球调和本征值 A(aω) 与径向**联动求解**（比 Schwarzschild 多一维）")
    B_("边界⑤：仅非磁化、无宇宙学常数 Kerr；极值 a→M 未处理；拖曳效应与 Teukolsky-Starobinsky 恒等式未实现")
    B_("边界⑥：红线——数学自洽 != 实验证实；宁记边界，不产出未闭合的数值")

    lines.append("-" * 70)
    lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d" % (P, F, B, Icnt))
    lines.append("-" * 70)
    lines.append("评级：C / L2（Kerr/Teukolsky 结构探测；方程已验证、machinery 已修复并通过 RW 自检，"
                 "给出『Teukolsky 为 4 项递推』的结构结论，但**未产出 Kerr QNM**）")
    lines.append("红线：数学自洽 != 实验证实；本册以结构结论为主，不粉饰、不编造数值。")

    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return P, F, B, Icnt


if __name__ == "__main__":
    rs, y, M, om = sp.symbols("r y M omega")
    L = sp.Integer(2)
    rp, rm = 2 * M, 0
    D0 = rp - rm
    ry = (rp - y * rm) / (1 - y)
    q = (1 - y) ** 2 / D0
    t0 = time.time()
    main()
    print("用时 %.1fs" % (time.time() - t0))
