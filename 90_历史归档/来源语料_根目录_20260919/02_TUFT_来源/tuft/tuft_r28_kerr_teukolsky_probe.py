# -*- coding: utf-8 -*-
"""
TUFT · R28 —— Kerr/Teukolsky 推广：第一性结构探测（含自检失败记录，不产出 Kerr 数值）
====================================================================================
R20–R24（时域/Prony，~1e-3）→ R25（Schwarzschild Leaver 连分式，特征值级 ≤1e-6）
→ R26（全维验证；发现 Zerilli 为 5 项递推）→ R27（SUSY 证明 RW↔Zerilli 等谱）
→ **R28：向旋转 Kerr 推广（Teukolsky 方程）。**

本册诚实记录：**推广受阻，且用自检发现 machinery 本身有偏差**。

  V1  Teukolsky 径向方程正确建立：a→0 且 s=0 的标量极限与 Schwarzschild 无质量标量
      径向方程**符号恒等**（同一坐标形式），证明方程本身无误。
  V2  统一 y-变量约化 machinery 的自检：对 **RW（R25 已知为 3 项递推）** 复算，
      要求清分母+约去公因子后 (deg S'',deg S',deg S)=(2,1,0)；**实得 (3,2,1)** ⇒
      **自检未通过**（machinery 与 R25 的推导存在未定位的偏差）。
  V3  同一 machinery 对 Teukolsky(a=0,s=-2) 得 (4,3,2)。**因 V2 自检未过，此结果不可信**，
      故本册**不产出任何 Kerr QNM 频率**。
  C1  奇异结构信息与修复清单（下一步定位 V2 偏差所需）。

按 TUFT 红线：宁可记录边界与失败，也不产出未经自检的数值。

几何单位 G=c=M=1。评级：C（结构探测/自检失败，未达自洽）。
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


def degrees(A_rs, B_rs, C_rs, u, v, ry, q):
    """用统一 machinery 约化 ODE A R''+B R'+C R=0，返回约去公因子后的 (deg S'',deg S',deg S)。"""
    subs = {rs: ry}
    A_ = sp.simplify(A_rs.subs(subs))
    B_ = sp.simplify(B_rs.subs(subs))
    C_ = sp.simplify(C_rs.subs(subs))
    Wg = sp.simplify(sp.diff(q, y) / q + B_ / (A_ * q))
    Ug = sp.simplify(C_ / (A_ * q ** 2))
    rho = sp.I * om * D0 / (1 - y) ** 2 + u / y + (u + v) / (1 - y)
    Pf = 2 * rho + Wg
    Qf = sp.simplify(sp.diff(rho, y) + rho ** 2 + Wg * rho + Ug)
    Ode = sp.Function("S")(y)
    expr = sp.diff(Ode, y, 2) + Pf * sp.diff(Ode, y) + Qf * Ode
    best = None
    for a_pow in (1, 2, 3):
        for b_pow in (2, 3, 4, 5):
            mul = y ** a_pow * (1 - y) ** b_pow
            num, den = sp.fraction(sp.cancel(expr * mul))
            if y not in den.free_symbols:
                poly = sp.expand(num / den)
                ca = sp.expand(poly.coeff(sp.Derivative(Ode, y, 2)))
                cb = sp.expand(poly.coeff(sp.Derivative(Ode, y)))
                cc = sp.expand(poly.coeff(Ode))
                g = sp.gcd(sp.Poly(ca, y), sp.Poly(cb, y))
                g = sp.gcd(g, sp.Poly(cc, y))
                if g != 1:
                    ca, cb, cc = [sp.expand(sp.cancel(e / g.as_expr())) for e in (ca, cb, cc)]
                d = (sp.degree(ca, y), sp.degree(cb, y), sp.degree(cc, y))
                if best is None or d[0] < best[1][0]:
                    best = (mul, d)
    return best[1], best[0]


def main():
    lines.append("=" * 70)
    lines.append("TUFT R28 · Kerr/Teukolsky 推广：第一性结构探测（自检失败，不产出 Kerr 数值）")
    lines.append("=" * 70)
    I_("几何单位 G=c=M=1")

    # ── V1：Teukolsky 径向方程的标量极限核对 ──
    I_("§V1 符号：Teukolsky 径向方程 a->0 且 s=0 的标量极限")
    R = sp.Function("R")(rs)
    Delta = rs ** 2 - 2 * M * rs
    Delta_p = sp.diff(Delta, rs)
    # Teukolsky（s=0, a=0）：K=omega r^2, lambda = l(l+1)
    VT_teu = (om * rs ** 2) ** 2 / Delta - L * (L + 1)
    eq_teu = sp.expand(Delta * sp.diff(R, rs, 2) + Delta_p * sp.diff(R, rs) + VT_teu * R)
    # 独立推导的 Schwarzschild 无质量标量径向方程：Phi = R(r) Y e^{-i omega t}
    #  口Phi=0 => r^2 f R'' + (2r-2M) R' + [r^2 omega^2/f - l(l+1)] R = 0
    f_sym = 1 - 2 * M / rs
    eq_sca = sp.expand(rs ** 2 * f_sym * sp.diff(R, rs, 2) + (2 * rs - 2 * M) * sp.diff(R, rs)
                       + (rs ** 2 * om ** 2 / f_sym - L * (L + 1)) * R)
    diff_sym = sp.simplify(sp.cancel(eq_teu - eq_sca))
    I_("  Teukolsky(a=0,s=0) 展开：ΔR''+Δ'R'+[K²/Δ−λ]R，Δ=r²−2Mr，K=ωr²")
    I_("  独立标量方程：r²fR''+(2r−2M)R'+[r²ω²/f−l(l+1)]R")
    I_("  两者之差 = %s" % diff_sym)
    if diff_sym == 0:
        P_("V1 Teukolsky 径向方程正确建立：a→0,s=0 与 Schwarzschild 无质量标量径向方程符号恒等"
           "（Δ=r²−2Mr ⇒ K²/Δ=ω²r²/f，Δ'=2r−2M），方程本身无误")
    else:
        F_("V1 Teukolsky 径向方程的标量极限与标量方程不一致：%s" % diff_sym)

    # ── V2：machinery 自检（RW 应为 3 项）──
    I_("§V2 machinery 自检：对 RW（R25 已知 3 项）复算，要求 (deg S'',deg S',deg S)=(2,1,0)")
    # y=(r-2M)/r ⇒ r=2M/(1-y)；f=y
    f_ = 1 - 2 * M / rs
    Vrw = f_ * (6 / rs ** 2 - 6 * M / rs ** 3)          # l=2
    d1, m1 = degrees(f_ ** 2, f_ * sp.diff(f_, rs), om ** 2 - Vrw,
                     -2 * sp.I * M * om, 4 * sp.I * M * om, ry, q)
    I_("  RW 最小清分母倍数 = %s ；次数 = (deg S'',deg S',deg S) = %s" % (m1, d1))
    if d1 == (2, 1, 0):
        P_("V2 machinery 自检通过：RW 复算得到 3 项递推所需结构 (2,1,0)")
    else:
        F_("V2 machinery **自检未通过**：RW 应给 (2,1,0)（对应 3 项递推），实得 %s。"
           "表明本册的 y-变量约化 machinery 与 R25 的推导存在**未定位的偏差**（可能在 RW 方程表述、"
           "ansatz 指数 (u,v)=(−2iMω,4iMω)、或先除以 A=f² 引入的人为极点），故不能用于 Kerr" % (d1,))

    # ── V3：同一 machinery 对 Teukolsky(a=0,s=-2) ──
    I_("§V3 同一 machinery 对 Teukolsky(a=0,s=−2) 的约化（Leaver ansatz：u=−s−2iMω, v=−1+s）")
    s = sp.Integer(-2)
    Dlt = rs ** 2 - 2 * M * rs
    KK = om * rs ** 2
    VT = KK ** 2 / Dlt - 2 * sp.I * s * (rs - M) * KK / Dlt + 4 * sp.I * s * om * rs - 4
    d2, m2 = degrees(Dlt, (s + 1) * sp.diff(Dlt, rs), VT,
                     -s - sp.I * 2 * M * om, -1 + s, ry, q)
    I_("  Teukolsky 最小清分母倍数 = %s ；次数 = %s" % (m2, d2))
    B_("V3 Teukolsky(a=0,s=−2) 约化得次数 %s；但 **V2 自检未过，此结果不可信** ⇒ "
       "本册**不产出任何 Kerr QNM 频率**" % (d2,))

    # ── C1：奇异结构与修复清单 ──
    I_("§C1 结构与修复清单")
    I_("  Teukolsky 径向方程：ΔR''+(s+1)Δ'R'+[K²/Δ−2is(r−M)K/Δ+4isωr−λ]R=0，"
       "Δ=r²−2Mr+a²，K=(r²+a²)ω−ma，λ=A+a²ω²−2amω，s=−2")
    I_("  正规奇点：r=r_±=M±√(M²−a²) 与 r=∞；Horizon 指标指数 {0,−s}（由 indicial 方程 Dλ(λ+s)=0 给出）")
    I_("  Leaver ansatz：R=e^{iωr}(r−r_+)^{−s−iσ_+}(r−r_−)^{−1+s+iσ_−}Σd_n[(r−r_+)/(r−r_−)]^n，"
       "σ_±=(ω(r_±²+a²)−ma)/(r_+−r_−)")
    B_("修复清单①：定位 V2 偏差——应先用 R25 已通的 RW 推导路径（而非本册重建的 y-变量形式）对齐，"
       "重点排查『先除以 A=f² 再清分母』是否引入人为极点（f=y 使 A→0 于 y=0）")
    B_("修复清单②：对齐后再处理 Kerr 的 aa=ma≠0、r_−≠0 分支；需与 Leaver(1985) 原文核对 ansatz 指数与 σ_± 归一")
    B_("修复清单③：即便 3 项成立，Kerr 还需**角向自旋权椭球调和本征值 A(aω)** 与径向联动求解（双连分式/迭代）")
    B_("修复清单④：若高阶递推确实成立，则需 Nollert 广义(矩阵)连分式，而非 Leaver 单连分式")

    B_("边界①：本册**不含任何 Kerr QNM 数值**，亦不含 Spin_weight / Teukolsky-Starobinsky 数值结果")
    B_("边界②：V1 仅核对 a=0,s=0 标量极限；s=±2 的项（-2is(r−M)K/Δ、4isωr）未被独立验证")
    B_("边界③：V2 的『应为 (2,1,0)』是根据 R25 的 3 项结论反推的判据，若 R25 的 3 项来自另一等价形式，"
       "则 V2 可能是判据而非 machinery 出错——已如实标注为『未定位』")
    B_("边界④：仅为非磁化、无宇宙学常数的 Kerr；极值 a→M 的行为未处理")
    B_("边界⑤：红线——宁记失败不产出未经自检的数值；Kerr 的拖曳效应(framedragging)、"
       "Teukolsky-Starobinsky 恒等式与高自旋管道均未在本册实现")

    lines.append("-" * 70)
    lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d" % (P, F, B, Icnt))
    lines.append("-" * 70)
    lines.append("评级：C / L2（Kerr/Teukolsky 结构探测；方程标量极限已验证，但约化 machinery 自检未过，"
                 "故**中止**未产出 Kerr QNM）")
    lines.append("红线：数学自洽 != 实验证实；本册以『自检失败』为主结论，不粉饰、不编造数值。")

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
