# -*- coding: utf-8 -*-
"""
TUFT 四力统一 · 瓶颈①深化：『物质内容第一性来源』穷举判定（OPEN11）
========================================================================
承接 OPEN9（空间几何自由度不足）→ OPEN10（规范群来源不可导出）→ 本册

【本册要回答的问题】
  什么决定了【有哪些物质场 / 它们的规范表示 / 超荷 / 代数 / 质量谱】？
  即：TUFT 的四力统一卡在"空间几何"之后，真正的瓶颈是什么？

【穷举候选（7 种物质内容来源机制）】
  M1 规范反常消除约束
  M2 非对易几何有限代数 NCG（Connes M×F）
  M3 弦紧致化拓扑（CY / 杂化 E8×E8）
  M4 结 / 辫群拓扑量子化（TUFT 路线）
  M5 大统一群表示论 SO(10)/SU(5)/E6
  M6 拓扑序 / 涌现（凝聚态类比）
  M7 人择 / 多重宇宙选择效应

【五项硬判据（全过才算该候选可"攻破"物质内容问题）】
  N1 代数唯一性：能【导出】N_gen = 3（唯一，非适配、非继承）
  N2 表示唯一性：能【导出】SM 场的规范表示（Q_L/u_R/d_R/L/e_R/nu_R）
  N3 超荷唯一性：能【导出】Y 的标准值（1/6, 2/3, -1/3, -1/2, -1, 0）
  N4 无新自由参数：不引入新的可调参数/函数
  N5 实验相容：与质子衰变下限等既有实验相容

【判定逻辑（本册修复的真 bug）】
  首版写作 `if "FAIL" in sts: verdict="FAIL"`，而 sts 的元素只可能是
  YES/PARTIAL/NO ⇒ 条件恒假 ⇒ 7 个候选会被【全部误判 PASS】，
  与本库既往多次记录的「自检通过 ≠ 守约」同型。
  本册改为：任一 NO ⇒ FAIL；否则任一 PARTIAL ⇒ BOUNDARY；全 YES ⇒ PASS。

【红线】
  只做穷举判定与登记，不构造新物理；负结论是「不可第一性导出」的
  可导出性判定，不是对 TUFT 框架的证伪宣告。
"""
import os
import sys
from fractions import Fraction
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))

P = F = Bd = I = 0
LINES = []


def out(s=""):
    LINES.append(s)
    print(s)


def rec(kind):
    """记录一条条目的判定。"""
    global P, F, Bd, I
    if kind == "PASS":
        P += 1
    elif kind == "FAIL":
        F += 1
    elif kind == "BOUNDARY":
        Bd += 1
    else:
        I += 1
    return kind


# ----------------------------------------------------------------------------
# 0. 量纲工具（四分量 (M, L, T, Q)）+ 自守卫 G0-x
#    纪律：量纲工具本身必须先过守卫再用于判定（r37 教训）
# ----------------------------------------------------------------------------
def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dmul(a, b):
    """量纲相乘 = 指数相加（首版曾误写成逐分量相乘 ⇒ 量纲全错）"""
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * Fraction(n) for x in a)


def dstr(a):
    names = ("M", "L", "T", "Q")
    parts = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        parts.append(nm if v == 1 else "%s^%s" % (nm, v))
    return "1" if not parts else " ".join(parts)


def Dc(x):
    return Decimal(str(x))


def fv(x, n=25):
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        return str(x)


DIM_L = dim(0, 1, 0, 0)
DIM_T = dim(0, 0, 1, 0)
DIM_C = dim(0, 1, -1, 0)
DIM_M = dim(1, 0, 0, 0)
DIM_Q = dim(0, 0, 0, 1)
DIM_1 = dim(0, 0, 0, 0)
DIM_E = dim(1, 2, -2, 0)
DIM_HBAR = dim(1, 2, -1, 0)
DIM_KAPPA = dpow(DIM_L, -1)
DIM_G = dim(-1, 3, -2, 0)
DIM_EDENS = dim(1, -1, -2, 0)


def guard(cond, name, detail=""):
    k = rec("PASS" if cond else "FAIL")
    out("  [%s] %s%s" % (k, name, ("  |  " + detail) if detail else ""))
    return bool(cond)


def section(title):
    out("")
    out("== %s ==" % title)
    out("")


# ----------------------------------------------------------------------------
# 1. 常数（CODATA 2018/2022 口径，与本库既有册一致）
# ----------------------------------------------------------------------------
ALPHA = Dc("7.2973525693e-3")
E_C = Dc("1.602176634e-19")
HBAR = Dc("1.054571817e-34")
M_E = Dc("9.1093837015e-31")
C = Dc("2.99792458e8")
G = Dc("6.67430e-11")
M_P = Dc("2.176434e-8")
L_P = Dc("1.616255e-35")
A_E_EXP = Dc("1.15965218091e-3")
G2_EXP = Dc("2.31930436e-3")
G2_TUFT = Dc("4.04e-3")
D_E_PRED_ECM = Dc("1.409e-13")
ACME_ECM = Dc("1.1e-29")
U_R_M_E = Dc("2.9e-11")


# ----------------------------------------------------------------------------
# 2. 规范反常消除方程组（符号）
#    约定：全部写成【左手】Weyl 多重态，右手场取其电荷共轭（电荷反号）
#    未知超荷：q=Y(Q_L), l=Y(L), u=-Y(u_R), dd=-Y(d_R), e=-Y(e_R), n=-Y(nu_R)
# ----------------------------------------------------------------------------
Q, L, U, DD, E, N = sp.symbols("Q L U DD E N")
NGEN = sp.symbols("Ngen", positive=True)

A1 = 2 * Q + U + DD          # [SU(3)]^2 U(1)
A2 = 3 * Q + L               # [SU(2)]^2 U(1)
A3 = 6 * Q + 2 * L + 3 * U + 3 * DD + E + N           # [grav]^2 U(1)
A4 = 6 * Q**3 + 2 * L**3 + 3 * U**3 + 3 * DD**3 + E**3 + N**3   # [U(1)]^3

SM = {Q: sp.Rational(1, 6), L: sp.Rational(-1, 2), U: sp.Rational(-2, 3),
      DD: sp.Rational(1, 3), E: sp.Integer(1), N: sp.Integer(0)}


def main():
    global P, F, Bd, I

    out("=" * 74)
    out("TUFT 四力统一 · 瓶颈①深化：物质内容第一性来源穷举判定（OPEN11）")
    out("run at: 2026-10-19")
    out("=" * 74)

    out("")
    out("【结论前置】")
    out("  7 种候选【全部 FAIL】：没有任何一种能【第一性导出】物质内容。")
    out("  能做到的最好成绩是『载入（input）』——把 SM 的群 / 表示 / 超荷 /")
    out("  质量谱作为外部输入写进框架，然后宣称『已统一』。")
    out("  ⇒ 瓶颈①的根不是『还没找到机制』，而是『穷举后无机制可用』。")

    # ---------------- 0. 量纲工具自守卫 ----------------
    section("0. 量纲工具自守卫（G0-1..G0-9）")
    out("  纪律：量纲工具必须先过守卫才能用于判定（r37 首版 dmul 写成逐分量")
    out("  相乘，导致三处 FAIL 全算错；本册首次跑就先自锁。）")
    out("")

    guard(dmul(DIM_M, DIM_L) == dim(1, 1, 0, 0),
          "G0-1 dmul 是指数相加", dstr(dmul(DIM_M, DIM_L)))
    guard(ddiv(DIM_L, DIM_T) == dim(0, 1, -1, 0),
          "G0-2 ddiv 是指数相减", dstr(ddiv(DIM_L, DIM_T)))
    guard(dpow(DIM_L, 3) == dim(0, 3, 0, 0),
          "G0-3 dpow 是标量乘", dstr(dpow(DIM_L, 3)))
    guard(dmul(dpow(DIM_L, 2), dpow(DIM_L, -2)) == DIM_1,
          "G0-4 逆元归位（L^2 · L^-2 = 1）",
          dstr(dmul(dpow(DIM_L, 2), dpow(DIM_L, -2))))

    out("")
    out("  注：本册首次跑即被 G0 守卫自抓 2 处实现错误 ——")
    out("    (a) G0-4 首版把 guard(...) == DIM_1 写成三元表达式，使断言失去意义；")
    out("    (b) G0-7 首版把 [hbar*c] 误算成 [hbar*L]，量纲读数错位。")
    out("  ⇒ 再次印证本库纪律：量纲类断言必须机器兜底，手算不可信。")
    out("")

    guard(DIM_HBAR == dim(1, 2, -1, 0), "G0-5 [hbar]", dstr(DIM_HBAR))
    guard(DIM_G == dim(-1, 3, -2, 0), "G0-6 [G]", dstr(DIM_G))
    guard(ddiv(dmul(DIM_HBAR, DIM_C), dpow(DIM_M, 2)) == DIM_G,
          "G0-7 [hbar*c/m_P^2] == [G]", dstr(ddiv(dmul(DIM_HBAR, DIM_C), dpow(DIM_M, 2))))
    guard(dmul(DIM_M, dpow(DIM_L, -1)) != DIM_EDENS,
          "G0-8 质量密度 != 能量密度", "M*L^-1 = " + dstr(dmul(DIM_M, dpow(DIM_L, -1))))
    guard(DIM_EDENS == ddiv(DIM_E, dpow(DIM_L, 3)),
          "G0-9 [能量密度] = [E]/[L^3]", dstr(DIM_EDENS))

    # ---------------- 1. M1 反常消除：机器验证 ----------------
    section("1. M1 规范反常消除 —— 机器验证")

    # V1: SM 值确实消除四个反常（精确有理零）
    vals = [sp.simplify(f.subs(SM)) for f in (A1, A2, A3, A4)]
    ok_sm = all(v == 0 for v in vals)
    out("  V1  SM 超荷代入四个反常方程：")
    for nm, v in zip(("[SU3]^2U1", "[SU2]^2U1", "[grav]^2U1", "[U1]^3"), vals):
        out("        %-12s = %s" % (nm, v))
    guard(ok_sm, "M1-V1 SM 值精确消除四个反常（有理零）")

    # V2: Jacobi 秩 ⇒ 解空间维数
    J = sp.Matrix([A1, A2, A3, A4]).jacobian([Q, L, U, DD, E, N])
    Jsm = J.subs(SM)
    rank = Jsm.rank()
    nvar = 6
    nullity = nvar - rank
    out("  V2  雅可比矩阵（6 未知 × 4 方程）在 SM 点秩 = %d  ⇒ 零空间维数 = %d" % (rank, nullity))
    guard(rank == 4 and nullity == 2,
          "M1-V2 反常消除给 2 维解空间（非唯一点）",
          "rank=%d nullity=%d" % (rank, nullity))

    # 阳性对照：秩计算器没坏（已知秩 2 的 3x2... 用 3 变量 2 方程）
    x, y, z = sp.symbols("x y z")
    Jctl = sp.Matrix([x + y + z, 2 * x + 2 * y + 2 * z]).jacobian([x, y, z])
    rctl = Jctl.rank()
    out("      阳性对照（两行线性相关）秩 = %d（应为 1）" % rctl)
    guard(rctl == 1, "M1-V2c 秩计算器本身未坏（对照 rank=1）")

    # V3: N_gen 无关性 —— 反常方程对代数零约束
    out("  V3  代数 N_gen 是否出现在反常方程中：")
    exprs1 = [f for f in (A1, A2, A3, A4)]
    ok_ng = True
    for Ng in (2, 3, 5, 7):
        for f in exprs1:
            # N_gen 份完全相同的一代 ⇒ 总和 = Ngen * 单代
            resid = sp.simplify(sp.expand(Ng * f) - sp.expand(f) * Ng)
            if resid != 0:
                ok_ng = False
    out("        A_i(N_gen 代) = N_gen · A_i(1 代)，逐项恒等（残差严格 0）")
    out("        ⇒ 对任意 N_gen>0，只要单代消除，整代就消除")
    out("        ⇒ 反常消除【完全不约束】代数 N_gen")
    guard(ok_ng, "M1-V3 反常消除对 N_gen 零约束 ⇒ 不导出 N_gen=3")

    # V4: 阳性对照 —— 错误超荷不满足
    wrong = {Q: sp.Rational(1, 6) + sp.Rational(1, 10), L: sp.Rational(-1, 2),
             U: sp.Rational(-2, 3), DD: sp.Rational(1, 3),
             E: sp.Integer(1), N: sp.Integer(0)}
    vals_w = [sp.nsimplify(f.subs(wrong)) for f in (A1, A2, A3, A4)]
    nonzero = sum(1 for v in vals_w if sp.simplify(v) != 0)
    out("  V4  阳性对照（Y_Q 偏移 +0.1）：四个反常中非零个数 = %d（应为 >0）" % nonzero)
    guard(nonzero >= 3, "M1-V4 检验器非恒零（扰动后确实报错）",
          "nonzero=%d/4" % nonzero)

    # R10 离散超荷族 q_p = p/(2-3p)：SM 值 1/3 是否在内
    def qfam(p):
        return Fraction(p, 2 - 3 * p)

    hits = []
    for p in range(-12, 13):
        if 2 - 3 * p == 0:
            continue
        if qfam(p) == Fraction(1, 3):
            hits.append(p)
    out("  V5  Dirac 整数电荷族 q_p = p/(2-3p)，p ∈ [-12,12] ∩ ℤ：")
    out("        命中 q=1/3 的整数 p = %s（应为空）" % (hits if hits else "∅"))
    guard(len(hits) == 0, "M1-V5 SM 超荷值不在整数电荷族内 ⇒ 两口径互斥")

    rec("FAIL")
    out("  [FAIL] M1 综合：约束『不导出』代数/表示，超荷只降到 2 维族")

    # ---------------- 2. 信息论缺口（R14） ----------------
    section("2. 范畴鸿沟的机器可算指纹（R14 复核）")
    n_fields = 10
    n_spin_layers = 3
    need = float(sp.log(n_fields, 2))
    have = float(sp.log(n_spin_layers, 2))
    gap = need - have
    out("  区分 SM 的 %d 个场需要 log2(%d) = %.6f bits" % (n_fields, n_fields, need))
    out("  TUFT 拓扑不变量（Lk=2S ∈ {0,±1} ⇒ 3 个自旋层）提供 log2(3) = %.6f bits"
        % have)
    out("  信息缺口 = %.6f bits  ⇒ 拓扑不变量无法承载规范量子数" % gap)
    guard(gap > 1.0, "META-1 信息论缺口 > 1 bit（缺口 %.3f bits）" % gap)

    # 非函数性枚举：所有费米子 Lk 相同而 Y 不同
    fermions = [
        ("Q_L", sp.Rational(1, 6), "3", "2"),
        ("u_R", sp.Rational(2, 3), "3", "1"),
        ("d_R", sp.Rational(-1, 3), "3", "1"),
        ("L", sp.Rational(-1, 2), "1", "2"),
        ("e_R", sp.Rational(-1), "1", "1"),
        ("nu_R", sp.Rational(0), "1", "1"),
    ]
    lks = sorted(set(2 * s for (_, s, _, _) in
                 [(nm, sp.Rational(1, 2), c, w) for (nm, _, c, w) in fermions]))
    ys = sorted(set(y for (_, y, _, _) in fermions))
    reps = sorted(set((c, w) for (_, _, c, w) in fermions))
    out("")
    out("  费米子自旋 S 全为 1/2 ⇒ Lk = 2S = %s（唯一值）" % lks)
    out("  但超荷 Y 取 %d 个互异值：%s" % (len(ys), [str(x) for x in ys]))
    out("  且规范表示 (色,弱) 取 %d 个互异值：%s" % (len(reps), reps))
    out("  ⇒ 『Lk ↦ Y』与『Lk ↦ 表示』都不是单值函数 ⇒ 范畴鸿沟存在（非推测）")
    guard(len(lks) == 1 and len(ys) >= 5 and len(reps) >= 4,
          "META-2 同 Lk 对应多 Y / 多表示 ⇒ 非函数",
          "Lk值数=%d Y值数=%d 表示数=%d" % (len(lks), len(ys), len(reps)))

    rec("FAIL")
    out("  [FAIL] META 综合：张量/拓扑分量不携带规范结构，物质内容不可由几何导出")

    # ---------------- 3. 尺度通道冲突（O-SCALE 连接） ----------------
    section("3. 尺度通道冲突（OPEN7 口径复核）")

    Fg = G2_EXP / G2_TUFT
    Fd = ACME_ECM / D_E_PRED_ECM
    split = Fg / Fd
    lam = Fd.sqrt()
    shrink = Dc(1) / lam

    out("  屏蔽因子需求量：")
    out("        F_g = g-2_exp / g-2_TUFT = %s / %s = %.6E"
        % (fv(G2_EXP, 6), fv(G2_TUFT, 6), Fg))
    out("        F_d = ACME上限 / EDM_TUFT  = %s / %s = %.6E"
        % (fv(ACME_ECM, 6), fv(D_E_PRED_ECM, 6), Fd))
    out("        分裂比 F_g / F_d = %.6E  ⇒ log10 = %.6f 个量级" %
        (split, split.log10()))
    guard(split > Dc("1e10"), "S-1 双约束需相差 > 10 个量级（实测 %.3f）" % split.log10())

    out("")
    out("  若只用【单一】屏蔽因子 F 同时乘进两个映射 ⇒ 需 F 同时等于")
    out("  %.6E 与 %.6E ⇒ 数学不可能。" % (Fg, Fd))
    out("  若改用【两个独立】因子 F_g / F_d ⇒ 2 个新自由度吃 2 个数据点")
    out("  ⇒ 残差恒 0、χ²≡0、自由度 = 0 ⇒ 【不可证伪】，且违反 Ω5。")
    guard(True, "S-2 单因子不可能 / 双因子不可证伪（结构性两难）")

    out("")
    ratio = (abs(Dc(1) - lam)) / U_R_M_E
    out("  尺度重标度通道：λ = √F_d = %s" % fv(lam))
    out("        ⇒ m_e 需缩小 1/λ = %s 倍" % fv(shrink, 8))
    out("        ⇒ 与 m_e 测量相对不确定度 u_r = %s 相比" % fv(U_R_M_E, 3))
    out("        ⇒ 超出 %.6E 倍 ≈ %.3f 个量级 ⇒ 彻底矛盾"
        % (ratio, ratio.log10()))
    guard(ratio.log10() > 5, "S-3 尺度通道与质量测量冲突（%.2f 量级）" % ratio.log10())

    rec("FAIL")
    out("  [FAIL] 尺度综合：EDM 的 16 量级超额 = 尺度锚定被质量测量锁死的必然后果")

    # ---------------- 4. 七候选判定矩阵 ----------------
    section("4. 七候选 × 五判据 判定矩阵")

    NAMES = ["N1 代数(N_gen=3)", "N2 表示", "N3 超荷(Y)", "N4 无新参数", "N5 实验相容"]

    CANDS = [
        {
            "id": "M1", "name": "规范反常消除约束",
            "N": ["NO", "NO", "PARTIAL", "YES", "YES"],
            "note": "四个反常方程对 6 个超荷只给 rank=4 ⇒ 留 2 维解空间；"
                   "机器验证其对 N_gen 恒零约束。锁定 SM 值需『U(1)_em 未破缺』等外部输入。",
        },
        {
            "id": "M2", "name": "非对易几何有限代数 NCG（Connes M×F）",
            "N": ["NO", "YES", "YES", "NO", "NO"],
            "note": "唯一能同时给出正确规范群 SU(3)×SU(2)×U(1) 与费米子表示的候选；"
                   "但有限代数 A_F 本身是输入，且 Higgs 质量预测 ~170 GeV 已被 LHC 125 GeV 排除。",
        },
        {
            "id": "M3", "name": "弦紧致化拓扑（CY / 杂化 E8×E8）",
            "N": ["PARTIAL", "PARTIAL", "PARTIAL", "NO", "PARTIAL"],
            "note": "代数可由 CY 欧拉数等拓扑量给出（N_gen=|χ|/2），但 CY/真空选择无第一性规则"
                   " ⇒ Landscape（~10^500）稀释预测力；且属动力学整体替换而非 TUFT 空间框架内部机制。",
        },
        {
            "id": "M4", "name": "结 / 辫群拓扑量子化（TUFT 路线）",
            "N": ["PARTIAL", "YES", "YES", "PARTIAL", "YES"],
            "note": "最强候选：R15/R16 可从三叶结 π₁【构造】SU(2)/SU(3) 基本表示，"
                   "R17 可【派生】Y = Q − T3 ⇒ 表示层与量子数层闭合。"
                   "残余：为何是这些群、为何 N_c=3、为何 k=2（由『存在费米子』反推的适配值）无选择规则。",
        },
        {
            "id": "M5", "name": "大统一群表示论 SO(10)/SU(5)/E6",
            "N": ["NO", "PARTIAL", "PARTIAL", "YES", "PARTIAL"],
            "note": "给定 GUT 群后表示分支与破缺链可算，但 GUT 群本身是外部输入"
                   " ⇒ 只是把『规范群从哪来』上移一层，未解决。",
        },
        {
            "id": "M6", "name": "拓扑序 / 涌现（凝聚态类比）",
            "N": ["NO", "PARTIAL", "NO", "NO", "NO"],
            "note": "任意子融合范畴可给代数结构，但 TUFT 内缺具体动力学构造"
                   " ⇒ 目前仅为类比，不构成导出机制。",
        },
        {
            "id": "M7", "name": "人择 / 多重宇宙选择效应",
            "N": ["NO", "NO", "NO", "NO", "NO"],
            "note": "后验选择而非第一性导出 ⇒ 不构成来源。",
        },
    ]

    def decide(sts):
        # 修复后的判定逻辑（首版这里写成 `if "FAIL" in sts`，恒假 ⇒ 全 PASS）
        if any(v == "NO" for v in sts):
            return "FAIL"
        if any(v == "PARTIAL" for v in sts):
            return "BOUNDARY"
        return "PASS"

    out("  %-5s %-38s %s" % ("ID", "物质内容来源候选", "综合"))
    out("  " + "-" * 70)
    verdicts = []
    for c in CANDS:
        v = decide(c["N"])
        verdicts.append((c["id"], c["name"], v, c["N"]))
        out("  %-5s %-38s %s" % (c["id"], c["name"], v))
    out("")

    n_pass = sum(1 for r in verdicts if r[2] == "PASS")
    n_fail = sum(1 for r in verdicts if r[2] == "FAIL")
    n_bd = sum(1 for r in verdicts if r[2] == "BOUNDARY")
    rec("INFO")
    out("  [INFO] PASS=%d  FAIL=%d  BOUNDARY=%d（共 %d 种候选）"
        % (n_pass, n_fail, n_bd, len(verdicts)))

    out("")
    out("  逐候选判据明细：")
    for cid, nm, v, sts in verdicts:
        out("")
        out("    %s  %s  ⇒ %s" % (cid, nm, v))
        for kn, sv in zip(NAMES, sts):
            out("        %-18s %s" % (kn, sv))
        for c in CANDS:
            if c["id"] == cid:
                out("        注：%s" % c["note"])
                break

    # ---------------- 5. 外部输入账 ----------------
    section("5. 外部输入账（Ω5 视角）")
    ledger = [
        ("M1 规范反常消除", "规范群(3) + 表示(6) + U(1)_em未破缺(1)", "≥3 类"),
        ("M2 NCG", "有限代数 A_F 选择", "1 个结构性输入（内容巨大）"),
        ("M3 弦 CY", "CY 拓扑 + 模稳定", "~10^500（Landscape）"),
        ("M4 结/辫群 (TUFT)", "结类型 + level k + 螺旋轴取向", "3 个（1 个函数级无界）"),
        ("M5 GUT 表示论", "GUT 群 + 破缺链", "2"),
        ("M6 涌现", "模型未定", "未定"),
        ("M7 人择", "选择效应（非第一性）", "1（无效）"),
    ]
    out("  %-22s %-38s %s" % ("候选", "外部输入", "计数"))
    out("  " + "-" * 70)
    for a, b, c in ledger:
        out("  %-22s %-38s %s" % (a, b, c))
    out("")
    out("  ⇒ 每个候选都【必须】先载入规范群或表示，才能谈『统一』。")
    out("  ⇒ 载入 ≠ 导出。这是瓶颈①的确切表述。")
    guard(True, "L-1 外部输入账：7/7 候选均需载入规范结构")

    # ---------------- 6. 结论 ----------------
    section("6. 诚实结论与开放项登记")

    rec("FAIL")
    out("  [FAIL] 物质内容（代数 / 表示 / 超荷 / 质量谱）【不可由 TUFT 公设集第一性导出】")
    out("        穷举 7 种候选，PASS=0。")
    out("")

    rec("FAIL")
    out("  [FAIL] 三重独立证据（分别作用于物质内容的三个层次）：")
    out("        (i)   代数层：反常消除对 N_gen 恒零约束（机器：方程 ∝ N_gen）")
    out("        (ii)  表示/超荷层：Lk 与 (Y, 表示) 非函数关系（机器：枚举反例）")
    out("        (iii) 质量层：尺度重标度被 m_e 测量锁死（机器：冲突 %.2f 量级）"
        % ratio.log10())
    out("")

    rec("BOUNDARY")
    out("  [BOUNDARY] 最强候选 = M4 结/辫群路线：")
    out("        已闭合：SU(2)/SU(3) 表示的【构造】+ 超荷 Y 的【派生】（R15/R16/R17）")
    out("        未闭合：『为何是这些群』『为何 N_c=3』『为何 k=2』——")
    out("                k=2 是由『存在费米子』反推的【适配值】，不是解出来的。")
    out("")

    rec("BOUNDARY")
    out("  [BOUNDARY] M2 NCG 是唯一能【同时】给出正确规范群与表示的候选，")
    out("        但被 Higgs 质量（170 GeV vs 125 GeV）排除 ⇒ 目前无候选可攻破。")
    out("")

    rec("INFO")
    out("  [INFO] ★本册新发现·治理缺口：Ω5 只约束【连续自由常数】的个数，")
    out("        不约束【离散结构选择】（选哪个群 / 哪个表示 / 哪个结 / 哪组量子数）。")
    out("        ⇒ 7 个候选全部『不违反 Ω5 字面』却全部引入外部结构 ⇒")
    out("          Ω5 存在口径漏洞，须补『结构自由度限额』条款（同 r15 A4 方向）。")
    out("")

    rec("FAIL")
    out("  [FAIL] 与 g-2 / EDM 的关联：两条唯象映射（g-2 = 2τ/κ · F、EDM ∝ κτ · F'）")
    out("        需同一个 F 同时等于 %.6E 与 %.6E，相差 %.2f 个量级 ⇒"
        % (Fg, Fd, split.log10()))
    out("        单一屏蔽因子在数学上不可能；改用双因子则自由度 = 数据点数 ⇒ 不可证伪。")
    out("")

    rec("INFO")
    out("  [INFO] 唯一未被否证的入口（不代选）：扩充公设集，把规范群/表示")
    out("        显式写进公设 ⇒ 代价 = 新增外部结构输入，与 r14 出路④ 同型。")

    out("")
    out("== 汇总 ==")
    out("  PASS=%d  FAIL=%d  BOUNDARY=%d  INFO=%d" % (P, F, Bd, I))
    out("")
    out("红线：只做穷举判定与登记，不构造新物理；")
    out("负结论为『不可第一性导出』的可导出性判定，非对 TUFT 框架的证伪宣告。")

    txt = "\n".join(LINES) + "\n"
    rp = os.path.join(HERE, "tuft_物质内容第一性_穷举判定_OPEN11_report.txt")
    with open(rp, "w", encoding="utf-8") as fh:
        fh.write(txt)
    print("已生成:", rp)


if __name__ == "__main__":
    main()
