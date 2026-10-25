#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TUFT-r172｜「光速飞行器动力学方程」F=(C−V)dm/dt 精算：定义重排 + 三重硬伤
================================================================================
编号 r172。★改号留痕：本卷起草时取 r170；登记时发现 README 已有并行会话的
r170（《物理常数本质本源》，09:14:06）与 r171（《常数 k′ 量纲最终裁定》）且均已
登记 ⇒ 按「已产三件套并已登记者为权威，后到者整体改号」纪律，本卷整体改号 r172
（不改动 r170/r171 任何字节）。

靶：`01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/17-光速飞行器动力学方程/1.md`
    （实测 249 行；`code/` 内 2 个自称「验证」的脚本，但 **assert 总数 = 0**、
     `diff(` 零调用、量纲结论硬编码 ⇒ 零机器验证）

本卷三层判据：
  ① 代数层：完整方程 (3.1) 与 F=dP/dt 的乘积法则展开是否**精确恒等**（Fraction 多项式，无浮点）
  ② 物理层：能量方程、动量守恒、伽利略不变性、v→c 自限 四条可算判据
  ③ 方法论层：自称「验证」的脚本 vs 机器审计（assert=0 / diff=0 / 量纲硬编码）

分层铁律：本卷条目**不可与 r159–r169 相加**。
治理红线：数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。
纯标准库（本环境无 numpy / sympy / mpmath），Python 3.8。
"""

import json
import os
import sys
from decimal import Decimal as DEC, getcontext
from fractions import Fraction as F

# GBK 控制台守卫
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

# ============================== 路径 ==============================
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
COM = os.path.dirname(PROJ)
ROOT = os.path.dirname(COM)
DDIR = os.path.join(PROJ, "数据")

S17 = os.path.join(ROOT, "01_独立体系", "S17_统一场论核心公式",
                   "04_理论推导", "核心公式集")
TDIR = os.path.join(S17, "17-光速飞行器动力学方程")
TARGET = os.path.join(TDIR, "1.md")
CODE_DIR = os.path.join(TDIR, "code")
CTRL_DIR = os.path.join(S17, "常数 f 的量纲最终裁定", "code")   # 正对照：非空 code/

C_LIGHT = DEC("299792458.0")


def efmt(x, prec=6):
    """Decimal 友好科学计数格式化。

    坑（本册自抓）：`"{:.6E}".format(Decimal(0))` 在 prec=60 的 context 下会给出
    `0.000000E+6`（`0E-34` 更给出 `0.000000E-34`）——指数随 Decimal 的内部 exponent 漂移，
    产出"看似有量级"的假读数。零值一律经 float 走，保证输出 `0.000000E+00`。
    """
    d = x if isinstance(x, DEC) else DEC(str(x))
    if d == 0:
        return "{:.{p}E}".format(0.0, p=prec)
    return "{:.{p}E}".format(d, p=prec)

# ============================== 登记器 ==============================
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, group, name, verdict, note):
    ENTRIES.append({"code": code, "group": group, "name": name,
                    "verdict": verdict, "note": note})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


def control(name, ok, detail):
    CONTROLS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


# ============================== 量纲 (M, L, T, Q) ==============================
def d_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def d_div(a, b):
    return tuple(x - y for x, y in zip(a, b))


def d_pow(a, n):
    return tuple(x * n for x in a)


def d_str(a):
    return "M^{} L^{} T^{} Q^{}".format(*a)


D_M = (1, 0, 0, 0)
D_L = (0, 1, 0, 0)
D_T = (0, 0, 1, 0)
D_Q = (0, 0, 0, 1)
D_V = d_div(D_L, D_T)                     # 速度
D_F = d_div(d_mul(D_M, D_L), d_pow(D_T, 2))   # 力
D_E = d_div(d_mul(D_M, d_pow(D_L, 2)), d_pow(D_T, 2))
D_P = d_div(d_mul(D_M, D_L), D_T)

# ============================== 精确多项式（Fraction） ==============================
def ptrim(a):
    b = list(a)
    while len(b) > 1 and b[-1] == 0:
        b.pop()
    return tuple(b) if b else (F(0),)


def padd(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0))
                  for i in range(n)])


def psub(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else F(0)) - (b[i] if i < len(b) else F(0))
                  for i in range(n)])


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return ptrim(out)


def pder(a):
    if len(a) <= 1:
        return (F(0),)
    return ptrim([a[i] * i for i in range(1, len(a))])


def pconst(x):
    return (F(x),)


def pstr(a):
    """低次在前渲染为可读串（a0 + a1 t + ...）。"""
    terms = []
    for i, c in enumerate(a):
        if c == 0:
            continue
        if i == 0:
            terms.append(str(c))
        elif i == 1:
            terms.append("{}t".format(c))
        else:
            terms.append("{}t^{}".format(c, i))
    return " + ".join(terms) if terms else "0"


def peval(a, t):
    acc = DEC(0)
    tt = DEC(t)
    for c in reversed(a):
        acc = acc * tt + DEC(c.numerator) / DEC(c.denominator)
    return acc


def pmaxabs(a):
    return max(abs(c) for c in a)


# 三维多项式矢量
def vadd(a, b):
    return [padd(a[i], b[i]) for i in range(3)]


def vsub(a, b):
    return [psub(a[i], b[i]) for i in range(3)]


def vder(a):
    return [pder(a[i]) for i in range(3)]


def vscale(a, k):
    return [pmul(a[i], (F(k),)) for i in range(3)]


def vzero(a):
    return all(pmaxabs(c) == 0 for c in a)


# ============================== A 组：先给靶应得的 PASS ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 先给靶应得的 PASS：量纲、恒等式、简化条件")
    print("=" * 78)
    out = {}

    # ---- A0 量纲 ----
    dmdt = d_div(D_M, D_T)
    rhs_dim = d_mul(D_V, dmdt)
    ok = (rhs_dim == D_F)
    print("[A0] (C−V) 的量纲 = {}；dm/dt = {}；右端 = {}；[F] = {}".format(
        d_str(D_V), d_str(dmdt), d_str(rhs_dim), d_str(D_F)))
    print("     ⇒ 左右同量纲 = {}".format(ok))
    out["A0_rhs_dim"] = d_str(rhs_dim)
    out["A0_ok"] = ok
    add("A0", "代数层",
        "§4.1 的量纲验证**正确**：[(C−V)·dm/dt] = M L T^-2 = [F]",
        "PASS" if ok else "FAIL",
        "§4.1 逐步给出 [(C−V)] = L T^-1、[dm/dt] = M T^-1、乘积 = M L T^-2 = [F]。"
        "本卷用 (M,L,T,Q) 四元组独立复算：右端 = **{}**，标准 [F] = **{}** ⇒ 相等 = {}。"
        "★这条靶是对的，诚实登记。".format(d_str(rhs_dim), d_str(D_F), ok))

    # ---- A1 完整方程 (3.1) 是否精确恒等 ----
    # m(t) = 2 + 3t + t^2；C、V 各分量为不同多项式（含常数项与非零导数）
    m = (F(2), F(3), F(1))
    C = [(F(5), F(1)), (F(-2), F(0), F(1)), (F(7), F(-3))]
    V = [(F(1), F(2)), (F(4), F(0), F(-1)), (F(0), F(6))]
    diff = vsub(C, V)
    lhs = vder([pmul(m, diff[i]) for i in range(3)])
    rhs = vadd([pmul(pder(m), diff[i]) for i in range(3)],
               [pmul(m, pder(diff[i])) for i in range(3)])
    res = vsub(lhs, rhs)
    ident_ok = vzero(res)
    print("[A1] 精确多项式（Fraction）验证 F = d/dt[m(C−V)] 与 (3.1) 是否恒等：")
    print("     m(t) = {}；C(t)、V(t) 三分量取互异多项式".format(pstr(m)))
    print("     m·(C−V) 各分量导数 − [ṁ(C−V) + m(Ċ−V̇)] 的残差多项式 = {}".format(
        [pstr(x) for x in res]))
    print("     ⇒ 三组件残差全零 = {}".format(ident_ok))
    out["A1_ident_ok"] = ident_ok
    add("A1", "代数层",
        "完整方程 (3.1) 是乘积法则的**精确恒等式**（Fraction 多项式残差全零）",
        "PASS" if ident_ok else "FAIL",
        "以 m(t)=2+3t+t²、C/V 三分量取互异多项式，用 Fraction 精确多项式（无浮点、无差分误差）"
        "比对 d/dt[m(C−V)] 与 ṁ(C−V)+m(Ċ−V̇)：三分量残差多项式 = {} ⇒ **逐项恒等**。"
        "★这条也成立；但正因为它恒等（见 D1），它**不含新物理**。".format(
            [pstr(x) for x in res]))

    # ---- A2 简化条件（Ċ=0, V̇=0）确实给出 (3.2) ----
    Cc = [pconst(5), pconst(-2), pconst(7)]
    Vc = [pconst(1), pconst(4), pconst(0)]
    diffc = vsub(Cc, Vc)
    lhs2 = vder([pmul(m, diffc[i]) for i in range(3)])
    rhs2 = [pmul(pder(m), diffc[i]) for i in range(3)]
    res2 = vsub(lhs2, rhs2)
    simp_ok = vzero(res2)
    # 反对照：Ċ≠0 时若强行丢掉该项，残差必须非零
    Cvar = [(F(5), F(1)), pconst(-2), pconst(7)]
    diffv = vsub(Cvar, Vc)
    lhs3 = vder([pmul(m, diffv[i]) for i in range(3)])
    rhs3 = [pmul(pder(m), diffv[i]) for i in range(3)]
    res3 = vsub(lhs3, rhs3)
    anti_ok = (not vzero(res3))
    print("[A2] 施加 Ċ=0 且 V̇=0 后，完整方程是否精确简化为 (3.2)：")
    print("     残差 = {} ⇒ 简化成立 = {}".format([pstr(x) for x in res2], simp_ok))
    print("     反对照（令 Ċ_x≠0 却仍丢该项）：残差 = {} ⇒ 非零 = {}".format(
        [pstr(x) for x in res3], anti_ok))
    out["A2_simp_ok"] = simp_ok
    out["A2_anti_ok"] = anti_ok
    add("A2", "代数层",
        "「Ċ≈0 且 V̇≈0 ⇒ 退化为 (3.2)」的代数步骤**成立**（反对照同时成立）",
        "PASS" if (simp_ok and anti_ok) else "FAIL",
        "把 C、V 取为常矢量后，完整方程三项中后两项严格为零 ⇒ 残差多项式全零 ⇒ (3.2) 精确成立。"
        "★同时给反对照：令 Ċ_x≠0 却仍丢掉该因子，残差 = {} ≠ 0 ⇒ 本判据不是恒真检测器。".format(
            [pstr(x) for x in res3]))

    # ---- A3 附录 A 符号表的量纲 ----
    sym_ok = (D_P == d_mul(D_M, D_V))
    print("[A3] 附录 A 符号表 [P] = kg·m/s ⇒ {} = [m]·[V] = {} ⇒ {}".format(
        d_str(D_P), d_str(d_mul(D_M, D_V)), sym_ok))
    out["A3_sym_ok"] = sym_ok
    add("A3", "代数层",
        "附录 A 符号表与动量定义 P = m(C−V) 的量纲自洽（[P] = kg·m/s）",
        "PASS" if sym_ok else "FAIL",
        "符号表给 [P] = kg·m/s，而 P = m(C−V) ⇒ {}，与 [P] = {} 相同 ⇒ {}。".format(
            d_str(d_mul(D_M, D_V)), d_str(D_P), sym_ok))
    return out


# ============================== B 组：物理层四条可算判据 ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 物理层：能量方程、动量守恒、不变性、v→c 自限")
    print("=" * 78)
    out = {}

    # ---- B1 能量方程：E = m c^2 sqrt(1-v^2/c^2) 与 m = m0/sqrt(1-v^2/c^2) ----
    # 代入后 E ≡ m0 c^2，对 v 零依赖 ⇒ 动能恒零
    betas = ["0", "0.5", "0.9", "0.99", "0.999999", "0.9999999999"]
    m0 = DEC("1.0")
    rows = []
    maxdev = DEC(0)
    for b in betas:
        bb = DEC(b)
        root = (DEC(1) - bb * bb).sqrt()
        gamma = DEC(1) / root
        m = m0 * gamma
        E = m * C_LIGHT * C_LIGHT * root
        dev = abs(E - m0 * C_LIGHT * C_LIGHT) / (m0 * C_LIGHT * C_LIGHT)
        if dev > maxdev:
            maxdev = dev
        rows.append((b, gamma, E / (m0 * C_LIGHT * C_LIGHT), dev))
    print("[B1] 能量方程 E = m c²√(1−v²/c²) 与质速关系 m = m₀/√(1−v²/c²) 联立：")
    for b, g, ratio, dev in rows:
        print("     v/c = {:<12s} γ = {:>22.14E}   E/(m₀c²) = {:.20E}   相对偏差 = {:.3E}".format(
            b, g, ratio, float(dev)))
    print("     ⇒ E/(m₀c²) 恒等于 1（最大相对偏差 {:.3E}）⇒ E 对 v **零依赖**".format(maxdev))
    e_ok = (maxdev < DEC("1e-50"))
    out["B1_max_rel_dev"] = efmt(maxdev)
    out["B1_rows"] = [[b, efmt(g, 14), efmt(r, 20), efmt(d)] for b, g, r, d in rows]
    out["B1_identity_ok"] = e_ok
    add("B1", "物理层",
        "★能量方程代入质速关系后 **E ≡ m₀c²**：对 v 零依赖 ⇒ 动能恒为 0，「加速」不耗能",
        "FAIL",
        "靶 §4.2.3 写「能量方程为 E = m₀c² = mc²√(1−v²/c²)（能量强守恒）」，并同时使用 "
        "m = m₀/√(1−v²/c²)。两者联立是**代数恒等式**：mc²√(1−v²/c²) = (m₀/√(1−v²/c²))·c²·√(1−v²/c²)"
        " = **m₀c²**，与 v 完全无关。机器复算 v/c ∈ {{0, 0.5, 0.9, 0.99, 0.999999, 0.9999999999}}："
        "E/(m₀c²) 全部 = 1（最大相对偏差 **{}**）。".format("{:.6E}".format(maxdev)) +
        "⇒ 该「能量方程」给不出任何动能项（标准相对论动能 (γ−1)m₀c² 在 v=0.99c 时为 **{} m₀c²**），"
        "因此**无法描述**「加速需要能量」，也无法与 §4.4「改变 m₀ 涉及 E=m₀c² 的巨大能量」构成"
        "能量收支：一个对速度零依赖的能量式，不能支撑一个以速度为目标的推进方案。".format(
            "{:.6f}".format(float((1 / (1 - DEC("0.99") ** 2).sqrt()) - 1))))

    # ---- B2 动量守恒 ----
    # 封闭系统 F_ext = 0 ⇒ dP/dt = 0 ⇒ (C−V) dm/dt = 0；若 dm/dt≠0 则 |C−V|=0 ⇒ V=C
    md = DEC("1.0")                 # kg/s
    imbalance = C_LIGHT * md        # N（V=0 时）
    print("[B2] 封闭系统（无外力）动量守恒判据：")
    print("     F_ext = 0 ⇒ dP/dt = 0 ⇒ (C−V)·dm/dt = 0；若 dm/dt = {} kg/s ≠ 0".format(md))
    print("     ⇒ 必须 |C−V| = 0 ⇒ V = C（物体本身以矢量光速运动）")
    print("     V=0 时该方程仍报出 F = |C|·dm/dt = {:.6E} N 的「推力」⇒ 这笔动量无外部来源".format(
        imbalance))
    cons_ok = (imbalance > DEC("1e6"))
    out["B2_imbalance_N"] = efmt(imbalance)
    add("B2", "物理层",
        "★「不依赖工质的推进」与动量守恒**直接冲突**：封闭系统 ⇒ (C−V)dm/dt = 0，"
        "dm/dt≠0 只能是 V=C",
        "FAIL",
        "把 F = dP/dt 当作**定义**时，F 不是预言而是记账；一旦要求它是**真实推力**（靶 §4.3「推力几何起源…"
        "并非来自外力作用」），就必须回答动量去哪了。机读：封闭系统 F_ext=0 ⇒ dP/dt=0 ⇒ "
        "(C−V)·dm/dt=0。取 dm/dt = 1 kg/s、V=0，该式要求 F = |C|·dm/dt = **{} N** 的动量凭空增加，"
        "而外部无任何反向动量流 ⇒ 唯一的自洽解是 dm/dt=0 或 V=C（后者与「飞行器」语义矛盾）。"
        "靶 §4.2.2 把「冲量-动量定理」（∫F dt = ΔP，F 为**外**力）称作「动量守恒定律在质量变化主导"
        "模式下的表现形式」，属**概念替换**：冲量-动量定理不是守恒律，守恒律要求 F=0。".format(
            "{:.6E}".format(imbalance)))

    # ---- B3 伽利略不变性 / |C|=c ----
    u = DEC("1.0")          # m/s 相对速度
    mdot = DEC("1.0")       # kg/s
    deltaF = u * mdot
    Cmod_after = C_LIGHT + u
    dev_c = Cmod_after - C_LIGHT
    print("[B3] 伽利略推动 V→V+u（u = {} m/s）：".format(u))
    print("     F = (C−V)dm/dt → F' = F − u·dm/dt ⇒ 力的改变量 = {:.6E} N（≠0）".format(deltaF))
    print("     若同时把 C→C+u 以保住 F，则 |C| = {:.6E} m/s ≠ c（差 {:.6E} m/s）".format(
        Cmod_after, dev_c))
    inv_ok = (deltaF != 0 and dev_c != 0)
    out["B3_deltaF_N"] = efmt(deltaF)
    out["B3_C_after"] = efmt(Cmod_after)
    out["B3_dc"] = efmt(dev_c)
    add("B3", "物理层",
        "★力的定义式**既不伽利略不变、也无法在不破坏 |C|=c 的前提下修好**",
        "FAIL",
        "两条路都不通（机器判据，不是修辞）：① 保持 C 不变、只推动 V（V→V+u）⇒ "
        "F' = F − u·dm/dt，力的改变量 = **{} N** ≠ 0 ⇒ 同一物理过程在不同惯性系给出不同推力；"
        "② 让 C 一起推动（C→C+u）以保住 F ⇒ |C| 变为 **{} m/s**，比 c 大 **{} m/s** ⇒ 与靶 §2.1 "
        "「C 的模为常数 c」**直接冲突**。⇒ 该方程只能存在于一个**指定的绝对参考系**（C 为绝对量）中，"
        "而靶从未声明这一点，也未给出任何可测的绝对系判据。".format(
            "{:.6E}".format(deltaF), "{:.6E}".format(Cmod_after), "{:.6E}".format(dev_c)))

    # ---- B4 v→c 自限 ----
    vs = ["0", "0.5", "0.9", "0.99", "0.999", "0.999999"]
    ratios = []
    for b in vs:
        bb = DEC(b)
        ratios.append((b, DEC(1) / (DEC(1) - bb)))
    mono = all(ratios[i][1] < ratios[i + 1][1] for i in range(len(ratios) - 1))
    print("[B4] 同推力所需质量变化率放大倍数 F/(c−v) 归一：")
    for b, r in ratios:
        print("     v/c = {:<10s} 1/(1−v/c) = {:.6E}".format(b, r))
    print("     ⇒ 单调递增 = {}；v→c 时 |C−V|→0 ⇒ 推力→0（给定 dm/dt）".format(mono))
    out["B4_ratios"] = [[b, efmt(r)] for b, r in ratios]
    out["B4_monotone"] = mono
    add("B4", "物理层",
        "★v→c **自限**：|C−V| = c−v → 0 ⇒ 越接近光速推力越弱，与「减小 m₀ 可驱动 v→c」矛盾",
        "FAIL",
        "靶 §4.3 第 4 条称「持续减小质量（特别是 m₀）可以使 v 无限趋近 c」。但方程本身含因子 "
        "(C−V)：两矢量平行时 |C−V| = c−v，v→c 时该因子 → 0。机器读数：同一推力 F 所需 "
        "dm/dt = F/(c−v) 相对 v=0 的放大倍数依次为 **1 / 2 / 10 / 100 / 1000 / 1e6**"
        "（v/c = 0 / 0.5 / 0.9 / 0.99 / 0.999 / 0.999999），且严格单调递增 = {}。"
        "⇒ 该方程给出的不是「通向光速的路径」而是**光速前的软墙**：越成功越推不动；"
        "且 V=C 时 F ≡ 0（无论 dm/dt 多大）。".format(mono))

    # ---- B5 经典还原 ----
    ve = DEC("3000")      # m/s 火箭有效排气速度
    md2 = DEC("1.0")      # kg/s
    rocket = ve * md2
    degenerate_at_V0 = DEC(0) * md2      # −V·dm/dt with V=0
    degenerate_at_Ve = ve * md2
    print("[B5] §4.2.4「还原经典」：令 C=0 得 F ≈ −V·dm/dt，与火箭 F = −v_e·dm/dt 对比：")
    print("     V=0 时：本文式 = {} N；火箭式 = {:.6E} N ⇒ 差 {:.6E} N".format(
        degenerate_at_V0, rocket, rocket))
    print("     V=v_e=3000 m/s 时：本文式 = {:.6E} N（与火箭**数值巧合相等**，物理量不同）".format(
        degenerate_at_Ve))
    print("     且 C=0 ⇒ |C|=0 ≠ c ⇒ **违反靶 §2.1 公设**（靶 §4.2.4 自承「与理论基本公设不符」）")
    red_ok = (rocket > 0 and degenerate_at_V0 == 0)
    out["B5_rocket_N"] = efmt(rocket)
    out["B5_degen_V0"] = "0"
    out["B5_ldiff_N"] = efmt(rocket - degenerate_at_V0)
    out["B5_ok"] = red_ok
    add("B5", "物理层",
        "★「还原经典」不成立：C=0 使 |C|=0 违反自身公设；且 V=0 处给出 0 N 而火箭给 v_e·dm/dt",
        "FAIL",
        "靶 §4.2.4 自己注明「C=0 此假设与理论基本公设不符，但可作为形式对比」——本卷把它当真检查："
        "① C=0 ⇒ |C| = 0 ≠ c ⇒ 该「极限」不是本理论的参数域内点，故不构成还原（不能用非法点证明相容）；"
        "② 退化式 −V·dm/dt 中的 V 是**飞行器相对观察者速度**，而火箭式的 v_e 是**排气相对飞行器速度**，"
        "二者物理身份不同；③ 数值判别：取 dm/dt = 1 kg/s、v_e = 3000 m/s，火箭推力 = **{} N**（与 V 无关），"
        "退化式在 V=0 时给 **0 N**（差 {} N），在 V=v_e 时数值恰等于 {} N —— 这条「形式相似」实为"
        "**单点巧合**，不是同构。".format("{:.6E}".format(rocket),
                                   "{:.6E}".format(rocket), "{:.6E}".format(degenerate_at_Ve)))

    # ---- B6 四力清单 ----
    print("[B6] 附录 B.1 称完整方程「包含了四种基本力」，实际明列 3 项：")
    print("     ① 质量变化力 = ṁ(C−V)   ② 核力 = mĊ   ③ 引力 = −mV̇   ④ 电磁力「（隐含在其他项中）」")
    out["B6_explicit"] = 3
    out["B6_claimed"] = 4
    add("B6", "口径层",
        "附录 B.1「包含四种基本力」的清单只明列 **3** 项，电磁力「隐含」无具体项 ⇒ 不可判",
        "BOUNDARY",
        "附录 B.1 列：① 质量变化力 ṁ(C−V)、② 核力 mĊ、③ 引力 −mV̇、④ 电磁力「（隐含在其他项中）」。"
        "前三项在 (3.1) 中逐项可指认；第四项无任何具体表达式，本卷**不判其对错**（防过度指控），"
        "但「四力统一」的计数因此只有 3 项可核 ⇒ 记 BOUNDARY。")
    return out


# ============================== C 组：方法论层（AST 审计靶 code/） ==============================
def analyze_py(path):
    """AST 审计：assert 数、print 数、纯字面量 print 数、BinOp/Compare 数、源码文本。"""
    import ast
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {"parse_ok": False, "assert_": 0, "print_": 0, "print_lit": 0,
                "binop": 0, "compare": 0, "src": src}
    n_assert = 0
    n_print = 0
    n_print_lit = 0
    n_binop = 0
    n_compare = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert):
            n_assert += 1
        elif isinstance(n, ast.BinOp):
            n_binop += 1
        elif isinstance(n, ast.Compare):
            n_compare += 1
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print":
            n_print += 1
            if n.args and all(isinstance(a, ast.Constant) and isinstance(a.value, str)
                              for a in n.args):
                n_print_lit += 1
    return {"parse_ok": True, "assert_": n_assert, "print_": n_print,
            "print_lit": n_print_lit, "binop": n_binop, "compare": n_compare, "src": src}


CODE_FILES = ["verify_simple.py", "verify_dynamics_equation.py"]
SYNTH_WITH_ASSERT = ("x = 1 + 2\n"
                     "assert x == 3, 'bad'\n"
                     "print('ok')\n")


def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 方法论层：靶 code/ 内两个「验证脚本」的 AST 审计")
    print("=" * 78)
    out = {}

    target_lines = 0
    if os.path.isfile(TARGET):
        with open(TARGET, "r", encoding="utf-8") as f:
            target_lines = sum(1 for _ in f)

    rows = []
    for fn in CODE_FILES:
        p = os.path.join(CODE_DIR, fn)
        if os.path.isfile(p):
            rows.append((fn, os.path.getsize(p), analyze_py(p)))
        else:
            rows.append((fn, 0, None))
    n_exist = sum(1 for _, _, st in rows if st is not None)
    tot_assert = sum(st["assert_"] for _, _, st in rows if st)
    tot_print = sum(st["print_"] for _, _, st in rows if st)
    tot_lit = sum(st["print_lit"] for _, _, st in rows if st)
    tot_binop = sum(st["binop"] for _, _, st in rows if st)

    print("[C1] 靶文档 {} 行；`code/` 内自称验证的脚本 {} 个（存在 {}）".format(
        target_lines, len(CODE_FILES), n_exist))
    for fn, size, st in rows:
        if st is None:
            print("     {} — 不存在".format(fn))
        else:
            print("     {:<32s} {:>6d} B  可解析={}  assert={}  print={}（纯字面量 {}）  BinOp={}".format(
                fn, size, st["parse_ok"], st["assert_"], st["print_"], st["print_lit"], st["binop"]))
    print("     ⇒ 两脚本 **assert 总数 = {}**，print 总数 = {}（其中纯字符串字面量结论 {} 条）".format(
        tot_assert, tot_print, tot_lit))
    out["C1_lines"] = target_lines
    out["C1_files"] = n_exist
    out["C1_assert"] = tot_assert
    out["C1_print"] = tot_print
    out["C1_print_lit"] = tot_lit
    out["C1_binop"] = tot_binop
    c1_ok = (n_exist == len(CODE_FILES) and tot_assert == 0 and tot_lit >= 10)
    add("C1", "方法论层",
        "★靶 `code/` 里两个「验证脚本」的 **assert 总数 = 0**：结论全是 print 字面量，永不可能失败",
        "FAIL" if c1_ok else "BOUNDARY",
        "AST 审计（不是看标题）：`verify_simple.py` 与 `verify_dynamics_equation.py` 均可解析，"
        "但 **assert 语句 = {} 条**；print 语句 = {} 条，其中**参数全为字符串字面量**的 = {} 条。"
        "⇒ 两个脚本无论公式对错都只会打印「✅ 通过」，**没有任何一条判据能失败** ⇒ 它们是"
        "「结论朗读器」而非验证器。判断依据：assert 数 = 0 时，脚本的输出与被验证命题的真值**无关**。".format(
            tot_assert, tot_print, tot_lit))

    # ---- C2 符号求导与量纲「检验」的真伪 ----
    st_dyn = dict((fn, st) for fn, _, st in rows).get("verify_dynamics_equation.py")
    src_dyn = st_dyn["src"] if st_dyn else ""
    n_diff = src_dyn.count("diff(")
    n_none = src_dyn.count("return None, None, None")
    n_dimlit = src_dyn.count("\"[M][L][T]^-2\"")
    n_strip = src_dyn.count("replace('[', '')")
    print("[C2] `verify_dynamics_equation.py` 的「第一性原理」成分：diff( 出现 {} 次；"
          "`return None, None, None` 出现 {} 次；硬编码量纲常量 `\"[M][L][T]^-2\"` 出现 {} 次；"
          "字符串剥离 `replace('[', '')` 出现 {} 次".format(
              n_diff, n_none, n_dimlit, n_strip))
    # 口径（本轮修正）：左端 left_dim 由 f-string 拼装（f'{M}{L}{T}^-2'），右端才是硬编码常量；
    # 因此判据不是「两侧字面量相同」，而是「乘积根本没算 —— 用字符串剥离伪装成量纲乘除，
    # 最后拿一个硬编码常量当结果」。故 n_dimlit 应 == 1（只有一个写死的答案），且剥离调用 >= 1。
    c2_ok = (n_diff == 0 and n_none >= 1 and n_dimlit == 1 and n_strip >= 1)
    out["C2_diff"] = n_diff
    out["C2_none_ret"] = n_none
    out["C2_dim_lit"] = n_dimlit
    out["C2_strip_calls"] = n_strip
    add("C2", "方法论层",
        "★`verify_dynamics_equation.py` 引 sympy 却 **`diff(` 零调用**；求导函数 `return None, None, None`；"
        "量纲「检验」不含量纲代数（字符串剥离 + 硬编码答案）",
        "FAIL" if c2_ok else "BOUNDARY",
        "该脚本 import 了 `diff`、建了 ReferenceFrame 与 m(t) 符号，但通篇 **`diff(` 出现 {} 次**——"
        "`derive_force_equation()` 直接 **`return None, None, None`**（出现 {} 次），"
        "`simplify_force_equation(None, None, None)` 收到三个 None 仍照常打印「简化为 F = (C−V)dm/dt」。"
        "量纲「验证」分两步作弊：① `right_dim` 用 `.replace('[', '').replace(']', '')` 把量纲符号"
        "剥成裸字母再拼字符串（该剥离出现 {} 次），**从未做指数相加**；② 真正的结论不是算出来的，"
        "而是硬编码 `right_dim_result = \"[M][L][T]^-2\"`（该字面常量出现 {} 次）——"
        "左端 `left_dim` 是同源的 f-string 拼装，两边本就同源 ⇒ 比较必然成立。"
        "⇒ 二脚本合起来构不成任何机器验证：一个全 print、一个把结论写死。".format(
            n_diff, n_none, n_strip, n_dimlit))

    # ---- C3 可量化预言 ----
    print("[C3] 可量化实验预言清点：0 个（§4.4 三条「挑战」全为定性表述）")
    out["C3_quant_pred"] = 0
    add("C3", "方法论层",
        "全文**零个可量化预言**：无「给定 dm/dt 与 m₀ 的预期加速度/到达时间」，§4.4 三条全定性",
        "FAIL",
        "§4.4「技术预言与挑战」列：① 能量需求（定性，仅引 E=m₀c²）；② 场产生机制（纯猜想）；"
        "③ 稳定性与控制（定性）。三者均无数字、无阈值、无实验条件，且 §5 自承「尚未被主流物理学接受"
        "和实验验证」。⇒ 计数 = **0** 个可量化预言。按 Popper 层（承 r167）该命题在「推进能力」上"
        "**不可证伪**：任何失败都可归因于「人工场尚未实现」。")

    # ---- C4 能量强守恒的自证 ----
    print("[C4] 「能量强守恒」的自证强度：E 与 v 无关（见 B1）⇒ 该律对任何推进方案零约束")
    out["C4_constraint"] = 0
    add("C4", "方法论层",
        "「能量强守恒」对推进方案**零约束力**：E ≡ m₀c² 与 v 无关 ⇒ 任何速度都「守恒」",
        "FAIL",
        "一个对所有 v 恒取同值的守恒量，无法排除任何速度变化过程 ⇒ 它既不能支持也不能否定"
        "「加质量推进」，属**零信息量的守恒律**（与 D1 同类，但作用点不同：D1 是方程恒等，"
        "C4 是守恒律恒等）。")
    return out


# ============================== D 组：零信息量 ==============================
def group_D():
    print("\n" + "=" * 78)
    print(" [D 组] 零信息量：方程是定义重排")
    print("=" * 78)
    out = {}
    print("[D1] F = (C−V)dm/dt 的推导链：F ≡ dP/dt、P ≡ m(C−V)、Ċ=0、V̇=0 ⇒ 恒等重排")
    out["D1_steps"] = 4
    add("D1", "口径层",
        "★目标方程是**定义重排**（零信息量）：F≡dP/dt 与 P≡m(C−V) 两条定义 + 两项置零",
        "INFO",
        "推导链 = ① P ≡ m(C−V)（公设）→ ② F ≡ dP/dt（定义）→ ③ 乘积法则（恒等式）→ "
        "④ Ċ≈0、V̇≈0（场景假设）。前两步都是**定义**，第三步是**恒等式**（A1 残差全零），"
        "第四步只是把两项丢掉 ⇒ 得到的 (3.2) 不含任何超出定义的新内容。"
        "⇒ 该「第一性原理推导」在形式上完全正确，在信息量上为零：它没有排除任何替代方程，"
        "因为任何 P 的定义都会给出 F=dP/dt 的相应形式。")

    # ---- D2 与 r16x 链路的对照 ----
    print("[D2] 与 r166/r168 同族的对照：三卷共同点是「定义重排 + 硬伤在物理层」")
    out["D2_chain"] = "r166（能量方程方法论）/ r168（常数 f 量纲）/ r172（本卷）"
    add("D2", "口径层",
        "与 r166/r168 同族对照（**不计入和**）：三卷共同症结＝代数层恒等，物理层失守",
        "INFO",
        "r166 判「能量方程验证脚本与结论脱钩」、r168 判「同一 f 五重量纲且代回失败」、"
        "本卷判「方程恒等但动量/不变性/自限三处失守」。三者条目**不可相加**（分层铁律），"
        "但可作**同族现象**并列：该体系的文档普遍在代数层正确、在物理层缺少守恒/协变/极限检验。")
    return out


# ============================== E 组：修复定价 ==============================
ACTIONS = [
    ("a1", "删除「不依赖工质 / 范式革命」宣称（方程降格为定义重排）", 2),
    ("a2", "补外部动量交换项（回到 F_ext = dP/dt，承认需外部场携带反向动量）", 3),
    ("a3", "重建能量方程（恢复 (γ−1)m₀c² 动能项）", 3),
    ("a4", "声明绝对参考系并放弃 |C|=c 与伽利略协变的兼容（或反之）", 4),
    ("a5", "删除 §4.2.4 的 C=0 退化段", 1),
]


def group_E():
    print("\n" + "=" * 78)
    print(" [E 组] 修复定价（5 动作 32 组合）")
    print("=" * 78)
    out = {}
    loose = []
    strict = []
    for mask in range(32):
        sel = [(mask >> i) & 1 for i in range(5)]
        a = dict(zip([x[0] for x in ACTIONS], sel))
        s_mom = (a["a1"] or a["a2"])
        s_energy = a["a3"]
        s_inv = a["a4"]
        s_red = (a["a4"] or a["a5"])
        if s_mom and s_energy and s_inv and s_red:
            cost = sum(c for (k, _, c), s in zip(ACTIONS, sel) if s)
            loose.append((mask, cost))
            if a["a1"] and a["a5"]:
                strict.append((mask, cost))
    zero = [x for x in loose if x[1] == 0]
    min_cost = min([c for _, c in strict]) if strict else None
    print("[E1] 宽松存活 {} / 32；严格存活 {} / 32；零代价存活 {}；最小代价 = {}".format(
        len(loose), len(strict), len(zero), min_cost))
    print("     ⇒ 每一个存活组合都要求「删宣称 或 补外场」且「重建能量方程」且「声明绝对系」")
    out["E_loose"] = len(loose)
    out["E_strict"] = len(strict)
    out["E_zero"] = len(zero)
    out["E_min_cost"] = min_cost
    add("E1", "修复定价",
        "修复定价：32 组合 ⇒ 宽松 {} / 严格 {} / 零代价 {}（最小代价 {}）".format(
            len(loose), len(strict), len(zero), min_cost),
        "FAIL" if min_cost is not None else "BOUNDARY",
        "动作与代价：" + "；".join("{}={}（代价 {}）".format(k, n, c) for k, n, c in ACTIONS) +
        "。存活条件（同时满足，均为机器判据）：动量项须选 a1∨a2、能量项须 a3、不变性须 a4、"
        "还原项须 a4∨a5。⇒ 宽松 **{}** / 严格（另需 a1∧a5）**{}** / 零代价 **{}**，"
        "严格最小代价 **{}**。".format(len(loose), len(strict), len(zero), min_cost))

    add("E2", "修复定价",
        "★「修复即自杀」第十六度：任何存活路径都要放弃一条已发布的核心宣称",
        "FAIL",
        "存活集合里 a1（删「不依赖工质」）与 a2（补外场动量交换）**至少选一**，a3（能量方程）"
        "**必选**，a4（绝对参考系声明）**必选**：即无论如何都要放弃「无工质 + 相对性原理 + "
        "现有能量方程」三者之一以上。零代价路径 = **0**。")
    return out


# ============================== 控制组 ==============================
def run_controls(A, B, C, D, E):
    print("\n" + "=" * 78)
    print(" [控制组]（验证检测器本身不是恒真/恒假）")
    print("=" * 78)

    # U1 多项式求导
    p = (F(7), F(-5), F(0), F(2))
    dp = pder(p)
    control("U1 精确求导对照：d/dt(2t³−5t+7) 应为 6t²−5",
            dp == (F(-5), F(0), F(6)), "der = {}".format(pstr(dp)))

    # U2 乘积法则数值反对照
    m = (F(2), F(3), F(1))
    Cc = [pconst(5), pconst(-2), pconst(7)]
    Vc = [pconst(1), pconst(4), pconst(0)]
    diffc = vsub(Cc, Vc)
    lhs = vder([pmul(m, diffc[i]) for i in range(3)])
    rhs = [pmul(pder(m), diffc[i]) for i in range(3)]
    control("U2 乘积法则在常矢量下退化为 ṁ(C−V)（残差全零）",
            vzero(vsub(lhs, rhs)), "res = {}".format([pstr(x) for x in vsub(lhs, rhs)]))

    # U3 γ 恒等
    bb = DEC("0.6")
    root = (DEC(1) - bb * bb).sqrt()
    m0 = DEC("1")
    mrel = m0 / root
    Eratio = (mrel * C_LIGHT * C_LIGHT * root) / (m0 * C_LIGHT * C_LIGHT)
    control("U3 质速关系+能量式联立应给 E/(m₀c²)=1（对 v 零依赖的机制自检）",
            abs(Eratio - 1) < DEC("1e-50"), "E/(m0c2) = {:.20E}".format(Eratio))

    # U4 火箭反例正对照
    control("U4 数值判别正对照：v_e=3000、dm/dt=1 ⇒ 火箭推力 3000 N ≠ 退化式 V=0 的 0 N",
            abs(DEC("3000") * DEC("1") - 0) == DEC("3000"), "3000 N vs 0 N")

    # U5 量纲工具自检
    control("U5 量纲工具自检：[F] = M L T^-2 且 [F]·[T] = [P]",
            D_F == (1, 1, -2, 0) and d_mul(D_F, D_T) == D_P,
            "F = {} ; P = {}".format(d_str(D_F), d_str(D_P)))

    # U6 靶可定位
    nline = 0
    if os.path.isfile(TARGET):
        with open(TARGET, "r", encoding="utf-8") as f:
            nline = sum(1 for _ in f)
    control("U6 靶可定位且行数 ≥ 200（实测 {} 行）".format(nline), nline >= 200,
            "exists = {} lines = {}".format(os.path.isfile(TARGET), nline))

    # U7 AST 检测器正对照：合成的含 assert 源码必须被检出 assert>=1
    tf = os.path.join(PROJ, "_tmp_ctrl_u7_r172.py")
    with open(tf, "w", encoding="utf-8") as f:
        f.write(SYNTH_WITH_ASSERT)
    st = analyze_py(tf)
    os.remove(tf)
    control("U7 assert 检测器正对照：含 assert 的合成源码须判 assert = 1 且纯字面量 print ≥ 1",
            st["assert_"] == 1 and st["print_lit"] >= 1,
            "assert={} print_lit={} parse_ok={}".format(
                st["assert_"], st["print_lit"], st["parse_ok"]))

    # U8 单调性检测器正/反对照
    inc = [DEC(1), DEC(2), DEC(3)]
    dec = [DEC(3), DEC(2), DEC(1)]
    f_inc = all(inc[i] < inc[i + 1] for i in range(2))
    f_dec = all(dec[i] < dec[i + 1] for i in range(2))
    control("U8 单调检测器反对照：递增序列判真、递减序列判假",
            f_inc and (not f_dec), "inc={} dec={}".format(f_inc, f_dec))

    # U9 恒等检测器反对照（注入非恒等情况）
    m2 = (F(2), F(3), F(1))
    C2 = [(F(5), F(1)), pconst(-2), pconst(7)]
    V2 = [pconst(1), pconst(4), pconst(0)]
    d2 = vsub(C2, V2)
    l2 = vder([pmul(m2, d2[i]) for i in range(3)])
    r2 = [pmul(pder(m2), d2[i]) for i in range(3)]
    control("U9 恒等检测器反对照：Ċ≠0 却丢项时必须报非零残差",
            not vzero(vsub(l2, r2)), "res = {}".format([pstr(x) for x in vsub(l2, r2)]))

    # U10 定价规则正/反对照（旧版写成 len(range(32))==32 是恒真式，本轮改为真检验）
    def _survive(mask):
        sel = [(mask >> i) & 1 for i in range(5)]
        a = dict(zip([x[0] for x in ACTIONS], sel))
        return bool((a["a1"] or a["a2"]) and a["a3"] and a["a4"]
                    and (a["a4"] or a["a5"]))
    all_on = _survive(31)
    all_off = _survive(0)
    control("U10 定价规则正/反对照：全选必存活、全不选必不存活，且严格 ⊆ 宽松 ⊆ 32",
            all_on and (not all_off)
            and E["E_strict"] <= E["E_loose"] <= 32 and E["E_zero"] <= E["E_loose"],
            "all_on={} all_off={} loose={} strict={} zero={}".format(
                all_on, all_off, E["E_loose"], E["E_strict"], E["E_zero"]))

    # U11 格式化器自检（本册自抓：Decimal 的 0 会给出 0.000000E+6 / 0.000000E-34 假读数）
    z1 = efmt(DEC(0))
    z2 = efmt(DEC("0E-34"))
    nz = efmt(DEC("1.001385E-59"))
    control("U11 efmt 自检：Decimal 零值（含 0E-34）须统一给 0.000000E+00，非零须保留有效位",
            z1 == "0.000000E+00" and z2 == "0.000000E+00" and nz == "1.001385E-59",
            "efmt(0)={} efmt(0E-34)={} efmt(1.001385E-59)={}".format(z1, z2, nz))


# ============================== 守卫 ==============================
def run_guards(A, B, C, D, E):
    print("\n" + "=" * 78)
    print(" [守卫]（★全部机读驱动，无一处 ok 写死 True）")
    print("=" * 78)

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    n_bnd = sum(1 for e in ENTRIES if e["verdict"] == "BOUNDARY")
    guard("G1 verdict 由机读驱动：FAIL {} / PASS {} / BOUNDARY {}（FAIL 与 PASS 都须 > 0）".format(
        n_fail, n_pass, n_bnd), n_fail > 0 and n_pass > 0,
        "机读累加 FAIL={} PASS={} BOUNDARY={}".format(n_fail, n_pass, n_bnd))

    guard("G2 恒等式守卫：(3.1) 与 F=dP/dt 的 Fraction 多项式残差须**逐项精确为零**",
          A["A1_ident_ok"], "A1 恒等 = {}".format(A["A1_ident_ok"]))

    guard("G3 简化守卫：Ċ=V̇=0 后须精确给出 (3.2)，且反对照须非零",
          A["A2_simp_ok"] and A["A2_anti_ok"],
          "simp={} anti={}".format(A["A2_simp_ok"], A["A2_anti_ok"]))

    maxdev = DEC(B["B1_max_rel_dev"])
    guard("G4 能量零依赖守卫：E/(m₀c²) 在所有 v 上须恒为 1（相对偏差 < 1e-50）",
          maxdev < DEC("1e-50"), "最大相对偏差 = {}".format(B["B1_max_rel_dev"]))

    imb = DEC(B["B2_imbalance_N"])
    guard("G5 动量亏损守卫：封闭系统 V=0、dm/dt=1 时的无源动量流须 > 1e6 N",
          imb > DEC("1e6"), "imbalance = {} N".format(B["B2_imbalance_N"]))

    dF = DEC(B["B3_deltaF_N"])
    dc = DEC(B["B3_dc"])
    guard("G6 不变性守卫：伽利略推动的力改变量须 ≠ 0，且 |C+u|−c 须 ≠ 0",
          dF != 0 and dc != 0,
          "dF = {} N ; |C+u|-c = {} m/s".format(B["B3_deltaF_N"], B["B3_dc"]))

    guard("G7 自限守卫：1/(1−v/c) 随 v 严格单调递增（v→c 推力→0）",
          B["B4_monotone"], "单调 = {}".format(B["B4_monotone"]))

    guard("G8 还原守卫：火箭式推力须 > 0 而退化式在 V=0 处须 = 0",
          B["B5_ok"], "rocket = {} N ; degen(V=0) = 0 N".format(B["B5_rocket_N"]))

    guard("G9 零断言守卫：靶两个 verify 脚本须都在、可解析，且 **assert 总数 = 0**、print 字面量 ≥ 10",
          C["C1_files"] == 2 and C["C1_assert"] == 0 and C["C1_print_lit"] >= 10,
          "files={} assert={} print_lit={}".format(
              C["C1_files"], C["C1_assert"], C["C1_print_lit"]))

    guard("G9b 伪求导守卫：`diff(` 须 = 0、`return None, None, None` 须存在、"
          "硬编码量纲常量须恰为 1 且存在字符串剥离（无指数相加）",
          C["C2_diff"] == 0 and C["C2_none_ret"] >= 1
          and C["C2_dim_lit"] == 1 and C["C2_strip_calls"] >= 1,
          "diff={} none_ret={} dim_lit={} strip={}".format(
              C["C2_diff"], C["C2_none_ret"], C["C2_dim_lit"], C["C2_strip_calls"]))

    guard("G10 防过度指控守卫：对靶有利的 PASS 须 ≥ 3 条且各自单列",
          n_pass >= 3, "PASS 条目数 = {}".format(n_pass))

    g10b = any(("分层铁律" in r) and ("相加" in r) for r in REDLINE)
    guard("G11 分层铁律守卫：须显式声明本卷条目不可与 r159–r169 相加（真查 REDLINE）",
          g10b, "含分层声明 = {}".format(g10b))


# ============================== 输出 ==============================
REDLINE = [
    "数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。",
    "不宣称「张祥前体系全错」，只判决本卷所列命题。",
    "A0/A1/A2/A3 四条代数层结论**靶是对的**，已诚实记为 PASS。",
    "B6 的「电磁力隐含」按防过度指控原则记 BOUNDARY，不作缺陷证据。",
    "分层铁律：本卷条目不可与 r159–r169 相加。",
]


def build_payload(A, B, C, D, E):
    stats = {}
    for e in ENTRIES:
        stats[e["verdict"]] = stats.get(e["verdict"], 0) + 1
    verdict = ("F-MASS-CHANGE-THRUST-EQUATION-IS-DEFINITION-RESTATEMENT-"
               "MOMENTUM-NONCONSERVING-GALILEAN-VIOLATING-AND-SELF-LIMITING")
    verdict_zh = (
        "S17「光速飞行器动力学方程」F=(C−V)dm/dt 的推导在代数层完全正确"
        "（量纲、乘积法则恒等、简化条件三条机器复算全通过），但它是「F≡dP/dt + P≡m(C−V) + 两项置零」"
        "的定义重排，零信息量；物理层四处失守：①与质速关系联立的能量式给出 E≡m₀c²、对 v 零依赖、"
        "动能恒零；②封闭系统动量守恒要求 (C−V)dm/dt=0，与「不依赖工质的推进」直接冲突"
        "（V=0、dm/dt=1 kg/s 时凭空报出 2.998e8 N）；③力的定义既不伽利略不变"
        "（力改变量 u·dm/dt），也无法在不破坏 |C|=c 的前提下修好；④|C−V|=c−v⇒v→c 时推力→0，"
        "与「减小 m₀ 可驱动 v→c」自相矛盾。§4「验证」为零机器验证"
        "（code/ 内两个脚本 assert 总数 0、diff( 零调用、量纲结论硬编码），"
        "全文零个可量化预言。修复定价：32 组合仅 6 宽松存活、2 严格存活、零代价 0。")
    key_numbers = {
        "rhs_dim": A["A0_rhs_dim"],
        "identity_ok": A["A1_ident_ok"],
        "simplify_ok": A["A2_simp_ok"],
        "symbol_table_ok": A["A3_sym_ok"],
        "energy_ratio_max_rel_dev": B["B1_max_rel_dev"],
        "energy_ratio_rows": B["B1_rows"],
        "momentum_imbalance_N": B["B2_imbalance_N"],
        "galilean_deltaF_N": B["B3_deltaF_N"],
        "C_mod_after_boost": B["B3_C_after"],
        "C_mod_minus_c": B["B3_dc"],
        "thrust_ratio_rows": B["B4_ratios"],
        "thrust_ratio_monotone": B["B4_monotone"],
        "rocket_thrust_N": B["B5_rocket_N"],
        "degenerate_at_V0_N": B["B5_degen_V0"],
        "degenerate_vs_rocket_N": B["B5_ldiff_N"],
        "four_forces_explicit": B["B6_explicit"],
        "four_forces_claimed": B["B6_claimed"],
        "target_lines": C["C1_lines"],
        "code_file_count": C["C1_files"],
        "code_assert_total": C["C1_assert"],
        "code_print_total": C["C1_print"],
        "code_print_literal_total": C["C1_print_lit"],
        "code_binop_total": C["C1_binop"],
        "sympy_diff_calls": C["C2_diff"],
        "none_return_count": C["C2_none_ret"],
        "hardcoded_dim_literals": C["C2_dim_lit"],
        "dim_string_strip_calls": C["C2_strip_calls"],
        "quantitative_predictions": C["C3_quant_pred"],
        "energy_law_constraint": C["C4_constraint"],
        "definition_restatement_steps": D["D1_steps"],
        "repair_loose": E["E_loose"],
        "repair_strict": E["E_strict"],
        "repair_zero_cost": E["E_zero"],
        "repair_min_cost": E["E_min_cost"],
    }
    return {
        "id": "TUFT-r172",
        "title": "「光速飞行器动力学方程」精算：定义重排 + 三重硬伤",
        "date": "2026-10-24",
        "target": "S17 核心公式集 17-光速飞行器动力学方程/1.md",
        "target_files": ["01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/"
                         "17-光速飞行器动力学方程/1.md"],
        "verdict": verdict,
        "verdict_zh": verdict_zh,
        "stats": stats,
        "entries": ENTRIES,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": key_numbers,
        "not_closed": [
            "本卷审 1.md（249 行）+ 其 `code/` 内两个 verify 脚本；若体系别处另有「加质量运动」的权威表述，B1/B2 需重审。",
            "B2 的动量论证假定「外力=0」，若人工场被视为合法外力，则「无工质」宣称须改写而非方程被否——"
            "该分支已计入 E 组的 a2。",
            "B3 只用伽利略推动检验；若该体系自认洛伦兹协变，需另做洛伦兹推动检验（本卷未做，因 |C|=c 已与推动冲突）。",
            "B4 只算平行情形 |C−V|=c−v；一般夹角下为 sqrt(c²+v²−2cv cosθ)，结论方向不变但倍数表不同。",
            "§4.3 的「人工场扫描」实现属工程假设，本卷不判其可行性。",
        ],
        "redline": REDLINE,
    }


def _fmt(x):
    return x if isinstance(x, str) else str(x)


def write_outputs(payload):
    base = os.path.splitext(os.path.basename(__file__))[0]
    paths = {}
    pj = os.path.join(DDIR, base + ".json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    paths["json"] = pj

    kn = payload["key_numbers"]
    L = []
    L.append("# " + payload["title"])
    L.append("")
    L.append("- 编号：**{}**　日期：{}".format(payload["id"], payload["date"]))
    L.append("- 靶：`{}`".format(payload["target"]))
    L.append("- 分层：本卷条目**不可与 r159–r169 相加**")
    L.append("")
    L.append("## 一、判词")
    L.append("")
    L.append("`{}`".format(payload["verdict"]))
    L.append("")
    L.append(payload["verdict_zh"])
    L.append("")
    L.append("## 二、条目（{}）".format(len(payload["entries"])))
    L.append("")
    L.append("| # | 组 | 结论 | 条目 |")
    L.append("|---|---|---|---|")
    for e in payload["entries"]:
        L.append("| {} | {} | **{}** | {} |".format(
            e["code"], e["group"], e["verdict"], e["name"]))
    L.append("")
    L.append("## 三、关键读数")
    L.append("")
    L.append("| 量 | 值 |")
    L.append("|---|---|")
    for k in ("rhs_dim", "identity_ok", "simplify_ok", "energy_ratio_max_rel_dev",
              "momentum_imbalance_N", "galilean_deltaF_N", "C_mod_minus_c",
              "thrust_ratio_monotone", "rocket_thrust_N", "degenerate_vs_rocket_N",
              "four_forces_explicit", "four_forces_claimed", "target_lines",
              "code_file_count", "code_assert_total", "code_print_literal_total",
              "sympy_diff_calls", "none_return_count", "hardcoded_dim_literals",
              "dim_string_strip_calls", "quantitative_predictions",
              "repair_loose", "repair_strict", "repair_zero_cost", "repair_min_cost"):
        L.append("| `{}` | {} |".format(k, _fmt(kn[k])))
    L.append("")
    L.append("### v→c 自限倍数表")
    L.append("")
    L.append("| v/c | 1/(1−v/c) |")
    L.append("|---|---|")
    for b, r in kn["thrust_ratio_rows"]:
        L.append("| {} | {} |".format(b, r))
    L.append("")
    L.append("### 能量式对 v 的依赖")
    L.append("")
    L.append("| v/c | γ | E/(m₀c²) | 相对偏差 |")
    L.append("|---|---|---|---|")
    for row in kn["energy_ratio_rows"]:
        L.append("| {} | {} | {} | {} |".format(row[0], row[1], row[2], row[3]))
    L.append("")
    L.append("## 四、控制组与守卫")
    L.append("")
    L.append("控制组 {} / {}；守卫 {} / {}".format(
        sum(1 for c in payload["controls"] if c["ok"]), len(payload["controls"]),
        sum(1 for g in payload["guards"] if g["ok"]), len(payload["guards"])))
    L.append("")
    L.append("## 五、未闭合项与红线")
    L.append("")
    for s in payload["not_closed"]:
        L.append("- " + s)
    L.append("")
    for s in payload["redline"]:
        L.append("- " + s)
    pm = os.path.join(DDIR, base + ".md")
    with open(pm, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    paths["md"] = pm

    V = []
    V.append("# 判定 · " + payload["title"])
    V.append("")
    V.append("- 编号：**{}**　日期：{}".format(payload["id"], payload["date"]))
    V.append("- 靶：`{}`".format(payload["target"]))
    V.append("- 分层：本卷条目**不可与 r159–r169 相加**")
    V.append("")
    V.append("## 一、判词")
    V.append("")
    V.append("`{}`".format(payload["verdict"]))
    V.append("")
    V.append(payload["verdict_zh"])
    V.append("")
    V.append("## 二、先给靶应得的 PASS")
    V.append("")
    for e in payload["entries"]:
        if e["verdict"] == "PASS":
            V.append("### {} {}".format(e["code"], e["name"]))
            V.append("")
            V.append(e["note"])
            V.append("")
    V.append("## 三、FAIL / BOUNDARY / INFO 逐条")
    V.append("")
    for e in payload["entries"]:
        if e["verdict"] != "PASS":
            V.append("### {} [{}] {}".format(e["code"], e["verdict"], e["name"]))
            V.append("")
            V.append(e["note"])
            V.append("")
    V.append("## 四、控制组与守卫")
    V.append("")
    for c in payload["controls"]:
        V.append("- {} `{}` — {}".format("OK" if c["ok"] else "BAD", c["name"], c["detail"]))
    for g in payload["guards"]:
        V.append("- {} `{}` — {}".format("OK" if g["ok"] else "BAD", g["name"], g["detail"]))
    V.append("")
    V.append("## 五、未闭合项与红线")
    V.append("")
    for s in payload["not_closed"]:
        V.append("- " + s)
    V.append("")
    for s in payload["redline"]:
        V.append("- " + s)
    pv = os.path.join(DDIR, "判定_" + base + ".md")
    with open(pv, "w", encoding="utf-8") as f:
        f.write("\n".join(V))
    paths["verdict"] = pv

    pr = os.path.join(DDIR, base + "_report.txt")
    Rl = []
    Rl.append("TUFT-r172 报告")
    Rl.append("条目：" + " / ".join("{}={}".format(k, payload["stats"][k])
                                 for k in sorted(payload["stats"])))
    Rl.append("控制组：{} / {}".format(
        sum(1 for c in payload["controls"] if c["ok"]), len(payload["controls"])))
    Rl.append("守卫：{} / {}".format(
        sum(1 for g in payload["guards"] if g["ok"]), len(payload["guards"])))
    Rl.append("判词：" + payload["verdict"])
    Rl.append("")
    Rl.append("关键读数：")
    for k in sorted(kn):
        Rl.append("  {} = {}".format(k, _fmt(kn[k])))
    with open(pr, "w", encoding="utf-8") as f:
        f.write("\n".join(Rl) + "\n")
    paths["report"] = pr
    return paths


# ============================== 主流程 ==============================
def main():
    print("=" * 78)
    print(" TUFT-r172｜「光速飞行器动力学方程」F=(C−V)dm/dt：定义重排 + 三重硬伤")
    print(" 2026-10-24")
    print("=" * 78)

    A = group_A()
    B = group_B()
    C = group_C()
    D = group_D()
    E = group_E()

    run_controls(A, B, C, D, E)
    run_guards(A, B, C, D, E)

    payload = build_payload(A, B, C, D, E)
    paths = write_outputs(payload)

    print("\n" + "=" * 78)
    print(" 终盘")
    print("=" * 78)
    print(" 条目： " + " / ".join("{}={}".format(k, payload["stats"][k])
                                for k in sorted(payload["stats"])))
    nco = sum(1 for c in CONTROLS if c["ok"])
    ngo = sum(1 for g in GUARDS if g["ok"])
    print(" 控制组： {} / {}".format(nco, len(CONTROLS)))
    print(" 守卫  ： {} / {}".format(ngo, len(GUARDS)))
    print(" 判词  ： " + payload["verdict"])
    for k in ("json", "md", "report", "verdict"):
        print(" 产物  ： " + os.path.basename(paths[k]))

    if nco != len(CONTROLS) or ngo != len(GUARDS):
        print("\n !! 控制组/守卫有失控项 => 退出码 2")
        sys.exit(2)
    print("\n 退出码 0")
    sys.exit(0)


if __name__ == "__main__":
    main()
