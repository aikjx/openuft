# -*- coding: utf-8 -*-
"""
TUFT V2.1「球对称流体微扰 + 临界半径闭式隐式解 + 引力波辐射 + 量纲全维修复」
全维机器审计（r26）
================================================================================
来料形态：**一份跨多轮的连续对话长稿**（同一作者，前后互相修订），含 7 个编号片段：
  片段 1  §14 球对称静态解（对标 CODATA 2022，tau_0 -> alpha）        （出现两次，重复粘贴）
  片段 2  §12 Navier-Stokes 涡旋 <-> 挠率张量映射
  片段 3  §9  四维 Frenet 标架升维 + chi^2 扫描框架
  片段 4  §4-8 pi 螺旋本征值几何推导
  片段 5  TUFT 球对称静态解微扰展开与稳定性分析（含 Python 250 位数值与"本征值"输出表）
  片段 6  临界半径闭式推导 + 带理想流体球对称微扰 + 量纲全维修复（第二版，真空 det M 分析）
  片段 7  TUFT V2.1 恒星球对称流体微扰 + 临界半径闭式 + 引力波辐射 + 量纲全维修复（最新版）

分工声明（避免与既有册重复计数）
--------------------------------------------------------------------------------
- 本库 r19（V34B 场方程展开）/ r20（P0 同源化）/ r21（P1 门禁与 ADM）已判
  「tau 非传播场 / 输运方程与作用量不同源」，本册凡引用者标「同 rXX」，不重复计数。
- 本库 r22 / r23（垂直原理）已判「恒等式复读」「250 位伪精度」，本册凡复发者
  只登记**第 N 次复发**，不重新论证。
- 本册新增对象 = 来料的**球对称恒星微扰 + 临界半径方程 + 引力波色散 + tau_0->alpha**，
  库内检索「临界半径 / 临界稳定半径」0 命中 ⇒ **本册为该主题首册**。

坐标与口径
--------------------------------------------------------------------------------
  - 量纲一律 Fraction 向量 (L, M, T)；数值一律 Decimal 60 位
  - c, G, Lambda, alpha 取 CODATA 2022 公布值（不引入本库其它册的重定值）
  - 挠率张量 tau^rho_{mu nu}：L^-1；挠率"能动张量" mathcal{T}_{mu nu}：L^-2（需区分）
  - kappa_0 = 8*pi*G/c^4

作者：算法联盟归一化链 r26
日期：2026-10-10
"""
import ast
import json
import os
import sys
from decimal import Decimal as Dc, getcontext
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUTDIR = os.path.join(BASE, "数据")

# ------------------------------------------------------------------ 常数
PI = Dc("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")
TWO_PI = PI * Dc(2)
D0, D1, D2 = Dc(0), Dc(1), Dc(2)


class CD:
    c = Dc("299792458")
    G = Dc("6.67430e-11")
    u_G = Dc("0.00015e-11")
    Lambda = Dc("1.1056e-52")          # 宇宙学常数 m^-2（Planck 量级）
    u_Lambda = Dc("0.0005e-52")
    alpha = Dc("7.2973525693e-03")     # 精细结构常数 CODATA 2022
    hbar = Dc("1.054571817e-34")

    @classmethod
    def kappa0(cls):
        return Dc(8) * PI * cls.G / (cls.c ** 4)

    @classmethod
    def m_P(cls):
        return (cls.hbar * cls.c / cls.G).sqrt()


# ------------------------------------------------------------------ 量纲工具
def dv(L=0, M=0, T=0):
    return (Fraction(L), Fraction(M), Fraction(T))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * Fraction(n) for x in a)


def dstr(a):
    return "L^%d M^%d T^%d" % (a[0], a[1], a[2])


ZERO = dv()
LEN = dv(L=1)
MASS = dv(M=1)
TIME = dv(T=1)
C = dv(L=1, T=-1)
GG = dv(L=3, M=-1, T=-2)
KAPPA0 = dpow(C, -4)
KAPPA0 = dmul(GG, KAPPA0)
TMUNU = dv(L=-1, M=1, T=-2)      # 能动张量 = 能量密度
RIC = dv(L=-2)                   # R_mu nu / R / Lambda
TAU_TENSOR = dv(L=-1)            # 挠率张量
PRESS = dv(L=-1, M=1, T=-2)
RHO = dv(L=-3, M=1)
OMEGA = dv(T=-1)
KVEC = dv(L=-1)
QDDOT = dv(L=2, M=1, T=-2)
VEL = dv(L=1, T=-1)

ITEMS = []
_SELF = []


def add(name, verdict, detail, note=""):
    ITEMS.append({"name": name, "verdict": verdict, "detail": detail, "note": note})
    print("  [%-9s] %s" % (verdict, name))
    print("             %s" % detail)


def selfchk(name, ok, detail=""):
    _SELF.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  自检[%s] %s %s" % ("OK " if ok else "!! ", name, detail))
    return ok


def rel(a, b):
    a, b = Dc(a), Dc(b)
    if b == 0:
        return Dc(0) if a == 0 else Dc("1e99")
    return abs(a - b) / abs(b)


def fmt(x, n=12):
    return "%.{}E".format(n) % Dc(x)


def section_A():
    print("\n" + "=" * 78)
    print("§A  量纲层（来料自称「量纲全维修复」，本段逐个核验该声称）")
    print("=" * 78)

    # --- A00 自检：量纲表自身闭合 ---
    s00 = (dmul(KAPPA0, TMUNU) == RIC)
    selfchk("A00 量纲表自洽：kappa_0 * T_{mu nu} = [R_{mu nu}] = L^-2",
            s00, "kappa_0 = %s ; T = %s ; 积 = %s" % (dstr(KAPPA0), dstr(TMUNU),
                                                      dstr(dmul(KAPPA0, TMUNU))))

    # --- A01 来料声称的 [kappa_0] ---
    claim_k0 = dv(L=1, M=-1, T=2)          # 来料 §1 写 M^{-1} L T^{2}
    true_k0 = KAPPA0
    ratio = ddiv(claim_k0, true_k0)
    ok = (ratio == ZERO)
    add("A01 §1 声称 [kappa_0] = M^-1 L T^2", "PASS" if ok else "FAIL",
        "真值 [8*pi*G/c^4] = %s；来料声称 %s；比值 = %s ⇒ 多出 L^2。"
        "尽管来料整段的**目标**是修量纲，第一步就把引力耦合常数的量纲写错了。"
        "（数值 %s 与本库 r18/r22 册逐位同源，数值无误，仅量纲声明错。）"
        % (dstr(true_k0), dstr(claim_k0), dstr(ratio), fmt(CD.kappa0())))

    # --- A02 挠率-物质耦合项所需 [alpha] ---
    need_a = ddiv(ddiv(RIC, TAU_TENSOR), TMUNU)     # 使 alpha*tau*T 与 G_{mu nu} 同量纲
    claim_a = LEN                                    # 来料 §1 声称 [alpha] = L
    ratio = ddiv(claim_a, need_a)
    ok = (ratio == ZERO)
    add("A02 §1 修正耦合项 alpha * tau_mu^rho_nu * T^{rho nu} 所需 [alpha]",
        "PASS" if ok else "FAIL",
        "与 G_{mu nu} 同量纲要求 [alpha] = %s；来料声称 L；比值 = %s ⇒ **不兼容**。"
        "⇒ 来料「改用挠率张量做缩并耦合，所有项量纲统一」的声称**未兑现**："
        "换了张量缩并却把 alpha 的量纲写错，失配从 M^-1T^2 缺口整体搬到别的缺口。"
        % (dstr(need_a), dstr(ratio)))

    # --- A03 同一 alpha 在微扰方程里被要求的第三个量纲 ---
    q_ref = dpow(LEN, -1)                            # d(delta Lambda)/dr 的量纲
    need_a2 = ddiv(ddiv(q_ref, TAU_TENSOR), PRESS)   # 使 (alpha*tau_r*delta P) = L^-1
    ok = (need_a2 == need_a) or (need_a2 == claim_a)
    add("A03 §2 微扰方程(1) 中同一 alpha 的第二次出现",
        "PASS" if ok else "FAIL",
        "该项与 d(delta Lambda)/dr (L^-1) 同量纲要求 [alpha] = %s；"
        "而 §1 主方程要求 %s、§1 正文声称 L ⇒ **同一符号三个互不相容量纲**"
        "（相差 %s 与 %s）。⇒ 不是笔误级失配，是**符号体系未定**。"
        % (dstr(need_a2), dstr(need_a), dstr(ddiv(need_a2, LEN)), dstr(ddiv(need_a, LEN))))

    # --- A04 临界半径方程三项齐性 ---
    t1 = dmul(KAPPA0, PRESS)
    t2 = dpow(LEN, -2)
    t3 = dmul(dmul(LEN, PRESS), dpow(LEN, -1))       # [alpha]*[P]/r, [beta]=1
    r13 = ddiv(t3, t1)
    ok_all = (t1 == RIC) and (t2 == RIC) and (t3 == RIC)
    add("A04 §2 临界半径隐式方程三项量纲齐性（按来料 [alpha]=L, [beta]=1）",
        "PASS" if ok_all else "FAIL",
        "项1 kappa_0(P+rho c^2/2) = %s ✓；项2 e^{-2L}(e^{2L}-1)/r^2 = %s ✓；"
        "项3 alpha*beta*P/r*(1-r_s/r) = %s ✗ ⇒ 与项1相差 %s。⇒ 该方程**三项不可相加**，"
        "所谓「隐式闭式解」在量纲层即不成立。" % (dstr(t1), dstr(t2), dstr(t3), dstr(r13)))

    # --- A05 kappa = c_perp / c^2 ---
    got = ddiv(VEL, dpow(C, 2))
    ok = (got == dpow(LEN, -1))
    add("A05 片段4 §5 声称 kappa = c_perp/c^2 且 [kappa] = L^-1",
        "PASS" if ok else "FAIL",
        "[c_perp/c^2] = %s ≠ L^-1，多出一个 T。正确形式应为 kappa = omega_perp/c"
        "（[omega/c] = %s）；来料同段自己写的「量纲核验：[kappa]=[tau]=m^-1」是**自欺性核验**——"
        "它只核对了结论没核对推导。" % (dstr(got), dstr(ddiv(OMEGA, C))))

    # --- A06 omega = c*kappa 的内部矛盾 ---
    d_omega = dmul(C, got)                           # 用片段4 自己定义的 kappa
    ok = (d_omega == OMEGA)
    add("A06 片段4 §5 omega = c*kappa 与 §4 的 kappa 定义联立",
        "PASS" if ok else "FAIL",
        "以 §4 的 kappa = c_perp/c^2 代入：[c*kappa] = %s ≠ [omega] = T^-1（无量纲）。"
        "⇒ 同一片段内两式**互相否证**；若改回标准 [kappa]=L^-1 则 omega=c*kappa 成立。"
        "⇒ 只需改一处（kappa 定义），但来料把两处都当作已核验结论。" % dstr(d_omega))

    # --- A07 挠率源项 mathcal{T}_{mu nu} = (1/c^2)(kappa^2-tau^2) e0 e0 ---
    base = dmul(dpow(C, -2), dpow(LEN, -2))
    d_std = dmul(base, dpow(ZERO, 2))                # 标准 tetrad：e_a 无量纲
    d_vel = dmul(base, dpow(VEL, 2))                 # 来料约定：e_0 = 四速度
    add("A07 片段3 §9.1 mathcal{T}_{mu nu} = (1/c^2)(kappa^2-tau^2) e_{0 mu} e_{0 nu}",
        "BOUNDARY",
        "标准 tetrad 约定（e_a^mu 无量纲）下 = %s ≠ L^-2 ✗；"
        "仅在来料的**非标准**约定（e_0^mu = dx^mu/dtau，归一化 -c^2，即 e_0 是四速度）下 = %s ✓。"
        "⇒ 量纲是否成立**完全由未声明的标架约定决定**，而来料把两者混用（同一段既写"
        "「四元标架 e_0,e_1,e_2,e_3」又令 e_0 为四速度）。登记为约定依赖，不作 PASS。"
        % (dstr(d_std), dstr(d_vel)))

    # --- A08 引力波色散关系 ---
    w2 = dpow(OMEGA, 2)
    ck = dmul(dpow(C, 2), dpow(KVEC, 2))
    claimed_term = RIC                                # 来料第二项 kaR
    corrected_term = dmul(dpow(C, 2), RIC)
    ok = (claimed_term == w2)
    add("A08 片段6 §4 色散式 omega^2 = c^2 k^2 - kappa*alpha*R",
        "FAIL" if not ok else "PASS",
        "[omega^2] = %s；[c^2k^2] = %s ✓；来料第二项 [kappa*alpha*R] = %s ✗"
        "⇒ **缺 c^2 因子**（差 %s）。正确项应为 c^2*kappa*alpha*R = %s ✓。"
        "符号（负号）与从波动方程的推导一致 ⇒ 属**可修笔误**，但量纲层判 FAIL。"
        % (dstr(w2), dstr(ck), dstr(claimed_term), dstr(ddiv(corrected_term, claimed_term)),
           dstr(corrected_term)))

    # --- A09 波动方程本体齐性 ---
    lhs1 = dpow(LEN, -2)
    lhs2 = RIC
    rhs = dmul(ddiv(GG, dpow(C, 4)), TMUNU)
    ok = (lhs1 == lhs2 == rhs)
    add("A09 片段6 §4 波动方程 Box h + kappa*alpha*R*h = (16 pi G/c^4) delta T 齐性",
        "PASS" if ok else "FAIL",
        "[Box h] = %s；[kaRh] = %s；[16 pi G/c^4 * delta T] = %s ⇒ 三项齐 ✓，"
        "且 16 pi G/c^4 = 2*kappa_0 与标准 GR 线性化系数一致（%s ⇒ 2*kappa_0）"
        "⇒ **这是来料中少数真正量纲自洽且系数正确的方程**，PASS。"
        % (dstr(lhs1), dstr(lhs2), dstr(rhs), fmt(Dc(16) * PI * CD.G / CD.c ** 4)))

    # --- A10 引力波应变系数 ---
    d_h = ddiv(dmul(GG, QDDOT), dmul(dpow(C, 4), LEN))
    ok = (d_h == ZERO)
    add("A10 片段7 §4 h_ij = (G/(c^4 R))[Qddot + alpha*F]",
        "CORRECTED" if ok else "FAIL",
        "量纲 = %s（无量纲 ✓，h 确为无量纲）；但标准四极公式为 **2G/(c^4 R) Qddot**，"
        "来料漏因子 2 ⇒ 与 GR 极限的振幅差 2 倍（可修笔误）。"
        "第二项 alpha*F[tau,Q] 中 **F 是未定义泛函**（无表达式、无量纲声明、无量级估计）"
        "⇒ 该修正项**不可计算、不可证伪**（本册不代其构造）。" % dstr(d_h))

    # --- A11 beta 的量纲 ---
    beta_dim = dmul(TAU_TENSOR, LEN)
    ok = (beta_dim == ZERO)
    add("A11 §2 挠率径向关系 tau_r(r) = (beta/r)(1 - r_s/r)",
        "PASS" if ok else "FAIL",
        "反解 [beta] = %s（无量纲）⇒ 与 [tau] = L^-1 自洽 ✓，且 r_s = 2GM/c^2 写法正确。"
        "⇒ 这是来料中量纲**干净**的一处，PASS。" % dstr(beta_dim))


# ------------------------------------------------------------------ 来料原文语料（用于机器核对符号用法确实存在）
SRC = {
    "frag7_s1": "alpha ,tau_{mu}{}^{rho}{}*{nu},T*{rho nu} ; [alpha]= L ; [kappa_0]=M^{-1}LT^{2}",
    "frag7_s2": "tau_r(r_c) = beta/r_c (1 - r_s/r_c) ; r_s = 2GM/c^2",
    "frag6_s1": "tau_{mu nu}^{(0)} = alpha R_{mu nu}^{(0)}（保留原耦合假设，量纲：alpha 无量纲）",
    "frag5_s3": "delta tau_{mu nu} = alpha * delta R_{mu nu} ; alpha 由第一性公理锁定",
    "frag5_s5": "alpha = mpf(0.082)",
    "frag1_s4": "alpha_tuft = mp.exp(-2*mp.pi/tau0) ; alpha_codata = 7.2973525693e-3",
    "frag3_s9": "参数替换为**固有时** tau 替代弧长 s ; omega_01 = c*kappa, omega_12 = c*tau",
    "frag1_s14": "mathcal{T}_{mu nu} = 挠率贡献额外几何能动张量",
    "frag2_s13": "T^vortex_{mu nu} = rho (omega_{f mu} omega_{f nu} - 1/2 g_{mu nu} omega_f^2)",
    "frag5_sM": "m11 = -(Lambda + kappa*alpha/A0v) ; m22 = -1/r",
    "frag6_sM": "M(r) = [[-Lambda/(1+kappa*alpha), 0], [A_0/(r B_0), -1/r]]",
    "frag7_py": "Lambda = mp.log(1 + kappa0 * rhoc * r**2 / 6)",
    "frag1_s14b": "tau_0 为全局挠率常数，由时空螺旋的拓扑缠绕数锁定",
    "frag5_A0": "A0(r) = 1 - 2*G/(c**2 * r) + Lambda*r**2 /3",
    "frag7_rs": "r_s = 2GM/c^2",
}


def section_B():
    print("\n" + "=" * 78)
    print("§B  符号口径台账（同名异义登记）")
    print("=" * 78)

    # B01 alpha
    alpha_specs = [
        ("片段7 §1", "挠率-物质耦合系数", "L（来料显式声称）"),
        ("片段6 §1", "tau=alpha*R 的耦合系数", "无量纲（来料显式声称）"),
        ("片段5 §3", "挠率-曲率微扰耦合系数", "未声明；代码中取 0.082"),
        ("片段1 §14.4", "精细结构常数", "无量纲；7.2973525693e-3"),
    ]
    n_incompat = len(set(s[2] for s in alpha_specs))
    add("B01 符号 alpha 在来料内的四种互不相容含义", "FAIL",
        "；".join("%s：%s（%s）" % s for s in alpha_specs) +
        " ⇒ 至少 3 种互斥（L vs 无量纲 vs 无声明），且第 4 义与前三义**数值直接冲突**"
        "（0.082 vs 1/137）。机器核验原文命中 %d/4 处。"
        % sum(1 for k in SRC if "alpha" in SRC[k]))

    # B02 kappa
    kappa_specs = [
        ("片段4 §4", "Frenet 曲率 kappa", "L^-1"),
        ("片段5/6 场方程", "挠率耦合常数 kappa（kappa*tau_{mu nu}）", "由 kappa*tau 需 L^-2 ⇒ L^-1"),
        ("片段7 §1", "kappa_0 = 8 pi G/c^4 引力耦合", "L^-1 M^-1 T^2"),
    ]
    add("B02 符号 kappa 的三种含义", "FAIL",
        "；".join("%s：%s（%s）" % s for s in kappa_specs) +
        " ⇒ 曲率与耦合常数同名，场方程 kappa*tau_{mu nu} 与 kappa_0*T_{mu nu} 并排出现时"
        "**无法区分**；且片段5 数值取 kappa=1.0（无量纲），与任一种都不符。")

    # B03 tau
    tau_specs = [
        ("片段3 §9", "固有时（替代弧长 s 的曲线参数）", "T"),
        ("片段7 §1", "挠率张量 tau_mu^rho_nu", "L^-1"),
        ("片段7 §2", "挠率标量径向分量 tau_r(r)", "L^-1"),
        ("片段1 §14.4", "全局挠率常数 tau_0", "无量纲（来料取 0.9622…）"),
    ]
    add("B03 符号 tau 的四种含义（含同章内直接冲突）", "FAIL",
        "；".join("%s：%s（%s）" % s for s in tau_specs) +
        " ⇒ **片段3 §9 单节内** tau 既是固有时参数（d/dtau）又是挠率分量（omega_12=c*tau），"
        "同一公式 ∇_{e_0} e_a 中两个 tau 同时出现且数学对象不同。另：tau_0 在片段1 是无量纲"
        "（0.9622），与 [tau]=L^-1 冲突。")

    # B04 挠率"张量"家族
    add("B04 挠率源项符号家族 tau_{mu nu} / mathcal{T}_{mu nu} / T^vortex_{mu nu}", "FAIL",
        "三种近同名符号、四种定义：①片段7 挠率张量 tau_mu^rho_nu（L^-1）；"
        "②片段6 tau_{mu nu}=alpha R_{mu nu}（L^-2 若 alpha 无量纲）；"
        "③片段1/3 mathcal{T}_{mu nu}=(1/c^2)(kappa^2-tau^2)e_0 e_0（约定依赖，见 A07）；"
        "④片段2 T^vortex 涡旋能动张量。②与①量纲差一个 L ⇒ **互相否证**；"
        "③与②在真空中是**同一位置的两个不同表达式** ⇒ 场方程右侧挠率项无唯一定义。")

    # B05 Lambda
    lam_specs = [
        ("片段5/6/7", "宇宙学常数 Lambda", "L^-2（1.1056e-52 m^-2）"),
        ("片段7 Python", "度规函数 Lambda(r) = log(1 + kappa_0*rho_c*r^2/6)", "应为无量纲"),
        ("片段6 §1", "势矩阵元 -Lambda/(1+kappa*alpha)", "L^-2（与 1/r 项混装）"),
    ]
    add("B05 符号 Lambda 的三种含义 + 一个数值撞名", "FAIL",
        "；".join("%s：%s（%s）" % s for s in lam_specs) +
        " ⇒ 最严重的是片段7 校验脚本把**度规函数**命名为 Lambda，与宇宙学常数同名，"
        "而同一脚本 term2 用的正是这个 Lambda ⇒ 凡复用该脚本者必把宇宙学常数当作度规函数代入。")


def section_C():
    print("\n" + "=" * 78)
    print("§C  数值与代码层（来料的数值输出是否真由其代码产生）")
    print("=" * 78)

    # --- C01 M 矩阵本征值 ---
    # 来料片段5 代码：m11 = -(Lambda + kappa*alpha/A0), m22 = -1/r，m12 = 0 ⇒ 下三角
    kap, alp = Dc("1.0"), Dc("0.082")

    def A0(r):
        return Dc(1) - Dc(2) * CD.G / (CD.c ** 2 * r) + CD.Lambda * r ** 2 / Dc(3)

    claimed = {Dc(1): (Dc("-8.2e-14"), Dc("-1.000000000000001")),
               Dc(1000): (Dc("1.02e-6"), Dc("1.14e-7")),
               Dc("1e6"): (Dc("9.7e-9"), Dc("1.01e-9")),
               Dc("1e9"): (Dc("1.005e-11"), Dc("1.001e-12"))}
    rows = []
    worst = Dc(0)
    for r in (Dc(1), Dc(1000), Dc("1e6"), Dc("1e9")):
        a0 = A0(r)
        m11 = -(CD.Lambda + kap * alp / a0)
        m22 = -Dc(1) / r
        c1, c2 = claimed[r]
        d1, d2 = abs(m11 - c1), abs(m22 - c2)
        rows.append((r, m11, c1, d1, m22, c2, d2))
        worst = max(worst, d1 / abs(m11) if m11 != 0 else Dc(0))
    selfchk("C01 自检：2x2 下三角矩阵（m12=0）的本征值 = 两个对角元",
            all(abs((ro[1] * ro[4]) - ((ro[1] + ro[4]) * ro[1] - ro[1] ** 2)) < Dc("1e-50")
                for ro in rows),
            "特征多项式 (m11-L)(m22-L)=0 恒成立")
    add("C01 片段5 的「本征值输出表」与其自身代码是否自洽", "FAIL",
        "M 为下三角 ⇒ 本征值**精确等于** (m11, m22)。复算：r=1 → (%.6E, %.6E)，"
        "来料报 (%.3E, %.15E) ⇒ 第一个**相对偏差 %.2f（100%% 级）**，第二个相符；"
        "r=1000 → (%.6E, %.6E)，来料报 (%.3E, %.3E) ⇒ **两者符号全相反**（m22 应恒为 -1/r = -1e-3）。"
        "四个半径全部不符，且来料声称的「近域负本征值 ⇒ 不稳定」读数在其自身代码下**不成立**"
        "（真值 m11 ≈ -0.082 在四个半径上**恒为负**，与半径无关 ⇒ 本就没有「临界半径」这一转折点）。"
        "⇒ 该输出表**不是该代码的输出**（未运行 / 转录自别处 / 编造），"
        "而片段5 的「临界稳定半径 r_c」结论**完全建立在这张表上**。"
        % (rows[0][1], rows[0][4], rows[0][2], rows[0][5],
           float(rows[0][3] / abs(rows[0][1])),
           rows[1][1], rows[1][4], rows[1][2], rows[1][5]))

    # --- C01b 文档式 vs 代码式 ---
    m11_doc = -CD.Lambda / (Dc(1) + kap * alp)
    m11_code = -(CD.Lambda + kap * alp / A0(Dc(1)))
    add("C01b 片段6 正文的 M 矩阵 vs 片段5 代码的 M 矩阵", "MISMATCH",
        "正文 m11 = -Lambda/(1+kappa*alpha) = %.6E；代码 m11 = -(Lambda + kappa*alpha/A0) = %.6E"
        " ⇒ 相差 %.2E 倍，**同一个 M 矩阵在来料内有两个不同的定义**。"
        "（附带观察：正文式的值 1.0218e-52 与来料 r=1000 报的 1.02e-6 尾数一致、指数差 46 量级，"
        "提示输出表来自某次**单位换算错误**的旧运行，本册不代其复原。）"
        % (m11_doc, m11_code, abs(m11_code / m11_doc) if m11_doc != 0 else Dc(0)))

    # --- C02 A0 缺质量 ---
    d_term = ddiv(dmul(GG, dpow(LEN, -1)), dpow(C, 2))    # 2G/(c^2 r)
    ok = (d_term == ZERO)
    add("C02 片段5 背景解 A0(r) = 1 - 2G/(c^2 r) + Lambda r^2/3", "FAIL",
        "项 2G/(c^2 r) 的量纲 = %s ≠ 无量纲 ⇒ **漏了质量因子 M**（应为 2GM/(c^2 r)）。"
        "同册片段7 §2 正确写作 r_s = 2GM/c^2 ⇒ 前后不一致；数值后果：以 M=1 kg 计该项 = %.6E，"
        "以太阳质量计 = %.6E，相差 30 个量级 ⇒ 后续所有「本征值」数值无定义。"
        % (dstr(d_term), Dc(2) * CD.G / CD.c ** 2, Dc(2) * CD.G * Dc("1.98847e30") / CD.c ** 2))

    # --- C03/C04/C05 tau_0 -> alpha ---
    tau0 = Dc("0.962241978827134")
    a_pred = (-TWO_PI / tau0).exp()
    a_claim = Dc("7.2973525693e-03")
    ratio_pred = a_pred / a_claim
    tau0_star = -TWO_PI / a_claim.ln()
    selfchk("C03 自检：exp(-2pi/tau0) 在 tau0>0 上严格单调（双射 (0,inf)->(0,1)）",
            all(((-TWO_PI / Dc(x)).exp() < (-TWO_PI / (Dc(x) * 2)).exp())
                for x in ("0.01", "0.1", "1", "10", "100")),
            "单调性 5 点采样通过")
    add("C03 片段1 §14.4 tau_0 = 0.962241978827134 代入 alpha = exp(-2 pi/tau_0)", "FAIL",
        "复算 alpha_pred = %.12E；来料称 alpha = %.12E ⇒ **相对偏差 %.4f（%.1f %%）**。"
        "⇒ 公布的 tau_0 与公布的 alpha **互斥**：代入即得 80%% 级偏差，不是 1e-16。"
        % (a_pred, a_claim, rel(a_pred, a_claim), float(rel(a_pred, a_claim) * 100)))

    add("C03b 使 alpha = exp(-2 pi/tau_0) 命中 CODATA 的正确 tau_0", "MISMATCH",
        "tau_0* = -2 pi/ln(alpha_CODATA) = %.15E；来料公布 %.15E ⇒ 相差 %.4f。"
        "（附带读数：来料值 %.6E 恰好对应 exp(-2pi/tau_0) = %.6E = alpha_CODATA/%.4f ⇒ "
        "疑似存在 5 倍因子错位，本册只登记不代其复原。）"
        % (tau0_star, tau0, rel(tau0, tau0_star), tau0, a_pred, a_claim / a_pred))

    add("C04 片段1 声称「残差 = 1.000000000000000e-16，满足 250 位精度约束」", "FAIL",
        "三重问题：①在 mp.dps=250 下 findroot 的残差应是 ~1e-250 量级，1e-16 **恰是双精度机器精度**"
        " ⇒ 声称的 250 位从未生效；②残差写成整齐的 1.000000000000000e-16 不像真实浮点输出；"
        "③由 C03，用公布的 tau_0 代入所得残差是 %.3E（80%% 级），与 1e-16 差 16 个量级。"
        "⇒ 该数值块为**未运行/转录**输出。登记为 r23 N05「伪精度」的**第 2 次复发**。"
        % rel(a_pred, a_claim))

    # --- C05 闭合积分恒等式 ---
    worst_id = Dc(0)
    for a, b in ((Dc("0.2"), Dc("0.8")), (Dc(1), Dc(1)), (Dc(3), Dc("0.5")), (Dc(5), Dc(2))):
        S = a * a + b * b
        kap_, tau_ = a / S, b / S
        Om = (kap_ * kap_ + tau_ * tau_).sqrt()
        worst_id = max(worst_id, rel(Om * TWO_PI * S.sqrt(), TWO_PI))
    selfchk("C05 自检：|Omega| * Delta s = 2 pi 对 4 组 (a,b) 成立（残差 <1e-50）",
            worst_id < Dc("1e-50"), "%.2E" % worst_id)
    add("C05 片段4 §6 / 片段2 §12.3 的「拓扑积分恒等式」∮|Omega| ds = 2 pi n", "INFO",
        "机器确认残差 %.2E ⇒ **恒成立**，但这是**代数恒等式**而非物理结论："
        "|Omega| = sqrt(kappa^2+tau^2) = 1/sqrt(a^2+b^2)，Delta s = 2 pi sqrt(a^2+b^2)，"
        "两式相乘 sqrt 因子**逐字相消**。⇒ 它不依赖螺旋参数、不依赖拓扑、不依赖 TUFT 任何公设，"
        "换成任意一条曲线重新参数化后同形 ⇒ **零信息量**。登记为库内恒等式复读**第 6 次**"
        "（前 5 次见 r22 A07/D01、r23 P03）。附带：来料写 n∈Z 却**从未给出任何 n≠1 的实例**"
        " ⇒ 所谓整数族是空族（伪量子化）。" % worst_id)

    # --- C06 校验脚本的度规函数 ---
    d_lam = dmul(dmul(KAPPA0, RHO), dpow(LEN, 2))
    ok = (d_lam == ZERO)
    add("C06 片段7 校验脚本 `Lambda = log(1 + kappa0*rhoc*r**2/6)`", "FAIL",
        "量纲 [kappa_0 * rho * r^2] = %s ≠ 无量纲 ⇒ **漏 c^2**（应为 kappa_0*rho*c^2*r^2）。"
        "同一脚本 term1 写的是 kappa0*(Pc + 0.5*rhoc*c**2)（**显式带了 c^2**）"
        " ⇒ 同脚本内自证是笔误而非约定。另：标准均匀密度球内解 e^{-2Lambda} = 1 - 8 pi G rho r^2/(3 c^2)"
        " ⇒ 来料还差**符号反**（+ 应为 -）与**因子 2**（4pi/3 应为 8pi/3）。三错叠加。"
        % dstr(d_lam))

    # --- C07 代码可运行性 ---
    SNIPPET = (
        "import mpmath as mp\n"
        "def solve_rc(alpha, beta, kappa0, Pc, rhoc, rs):\n"
        "    def f(r):\n"
        "        Lambda = mp.log(1 + kappa0 * rhoc * r**2 / 6)\n"
        "        t1 = kappa0*(Pc + 0.5*rhoc*mp.c**2)\n"
        "        t2 = mp.e**(-2*Lambda)/r**2 * (mp.e**(2*Lambda)-1)\n"
        "        t3 = alpha*beta*Pc/r*(1 - rs/r)\n"
        "        return t1 + t2 + t3\n"
        "    return mp.findroot(f, 1e7)\n"
        "def chi2_tuft(alpha, kappa):\n"
        "    rc = solve_rc(alpha, beta=0.1, kappa0=kappa, Pc=1e16, rhoc=1e18, rs=3000)\n"
        "    pred_G = tuft_predict_G(rc, alpha, kappa)\n"
        "    G_codata = mp.mpf('6.67430e-11')\n"
        "    sigma_G = mp.mpf('1.5e-15')\n"
        "    return ((pred_G - G_codata)/sigma_G)**2\n"
    )
    tree = ast.parse(SNIPPET)
    defined = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef,))}
    assigned = {t.id for n in ast.walk(tree) if isinstance(n, ast.Assign)
                for t in n.targets if isinstance(t, ast.Name)}
    imported = {a.asname or a.name.split(".")[0] for n in ast.walk(tree)
                if isinstance(n, ast.Import) for a in n.names}
    called = {n.func.id for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    builtins_ok = {"mpmath", "print", "abs", "float", "int", "list", "range"}
    undef = sorted(c for c in called
                   if c not in defined and c not in assigned
                   and c not in imported and c not in builtins_ok and c != "mp")
    selfchk("C07 自检：AST 扫描能正确识别已定义名（solve_rc 命中）",
            "solve_rc" in defined and "solve_rc" in called, "defined=%s" % sorted(defined))
    add("C07 片段7 校验脚本的可运行性（AST 未定义名扫描）", "FAIL" if undef else "PASS",
        "被调用但未定义的名字：%s ⇒ 脚本**无法运行**（`tuft_predict_G` 从未给出定义）。"
        "⇒ 与 C01/C04 同型：来料的「250 位校验脚本」是**展示性伪代码**，"
        "其数值结论（chi^2、r_c）没有任何一次真实运行的支撑。"
        "（本册同 r23 N04 的教训：残差趋零**不能**作为公式正确的证据，因为代码根本没跑。）"
        % (undef if undef else "无"))

    # --- C08 Rust chi^2 退化 ---
    def chi2_rust(k, a):
        u = Dc(1) + Dc(k) * Dc(a)
        g = ((CD.G / u - CD.G) / CD.u_G) ** 2
        l = ((CD.Lambda * u - CD.Lambda) / CD.u_Lambda) ** 2
        return g + l

    pairs = [("0.001", "0.05"), ("0.005", "0.01"), ("0.0025", "0.02"), ("0.01", "0.005")]
    vals = [chi2_rust(k, a) for k, a in pairs]
    same = max(rel(v, vals[0]) for v in vals)
    selfchk("C08 自检：来料 Rust 的 chi^2 只依赖乘积 u = kappa*alpha（4 组同 u 组合一致）",
            same < Dc("1e-40"), "%.2E" % same)
    bound_G = CD.u_G / CD.G
    bound_L = CD.u_Lambda / CD.Lambda
    add("C08 片段6/7 Rust 参数扫描 chi^2(kappa, alpha) 的判别力", "FAIL",
        "chi^2 只依赖 u = kappa*alpha（4 组同 u=5e-5 的不同 (kappa,alpha) 给出同一值，相对差 %.2E）"
        " ⇒ 二维网格扫描是**一维退化**，200x200 网格只测到 1 个有效组合；"
        "且全局最小在 u=0（即无 TUFT 效应）⇒ 扫描必然返回「退化解」。"
        "**有价值的附带读数**：在来料自己的耦合形式下，G 的 CODATA 精度把 |kappa*alpha| 限到 "
        "1sigma ≲ %.3E、Lambda 侧 ≲ %.3E ⇒ 取严者 |kappa*alpha| ≲ %.2E。"
        "⇒ 若真按此形式重标 G 与 Lambda，TUFT 修正在任何非引力测量中已不可见。**这是本册少有的可用定量读数。**"
        % (same, bound_G, bound_L, min(bound_G, bound_L)))

    # --- C09 输入数值自洽性 ---
    rhoc, Pc, rs = Dc("1e18"), Dc("1e16"), Dc("3000")
    M_from_rs = rs * CD.c ** 2 / (Dc(2) * CD.G)
    M_from_rho = Dc(4) / Dc(3) * PI * rhoc * rs ** 3
    M_sun = Dc("1.98847e30")
    ratio_P = Pc / (rhoc * CD.c ** 2)
    add("C09 片段7 输入三元组 (Pc=1e16 Pa, rho_c=1e18 kg/m^3, r_s=3000 m) 的自洽性", "BOUNDARY",
        "由 r_s 反解 M = %.4E kg = %.4f M_sun；由均匀密度球 M = (4/3)pi*rho*R^3 = %.4E kg = %.4f M_sun"
        " ⇒ 两者相差 **%.2f 倍**。另 P_c/(rho_c c^2) = %.3E，而相对论恒星（中子星）该比值量级 ~0.1"
        " ⇒ 所给 P_c 比同密度流体的自然压强低约 19 个量级，且**未给 c_s^2 = dP/drho**（微扰方程必需）。"
        "⇒ 求解器输入本身欠定，r_c 的任何数值都不是物理读数。"
        % (M_from_rs, float(M_from_rs / M_sun), M_from_rho, float(M_from_rho / M_sun),
           float(M_from_rs / M_from_rho), ratio_P))


def section_D():
    print("\n" + "=" * 78)
    print("§D  结构层（来料的核心声称是否成立）")
    print("=" * 78)

    k0 = CD.kappa0()
    rhoc, Pc, rs = Dc("1e18"), Dc("1e16"), Dc("3000")
    term1 = k0 * (Pc + rhoc * CD.c ** 2 / Dc(2))

    def term2(r):
        # 采用「补上 c^2」后的来料形式（原式见 C06 已判 FAIL）；e^{2L} = 1 + kappa_0 rho c^2 r^2/6
        e2 = Dc(1) + k0 * rhoc * CD.c ** 2 * r * r / Dc(6)
        return (Dc(1) - Dc(1) / e2) / (r * r)

    def f_rc(r, ab):
        return term1 + term2(r) + ab * Pc / r * (Dc(1) - rs / r)

    # --- D01 正耦合下无解 ---
    scan = [rs * (Dc(1) + Dc(i) * Dc("0.05")) for i in range(1, 401)]
    fmin = min(f_rc(r, Dc(1)) for r in scan)
    fmin0 = min(term1 + term2(r) for r in scan)
    add("D01 §2 临界半径隐式方程在 alpha*beta > 0 时是否有解", "FAIL",
        "在 r ∈ (r_s, 21 r_s] 上取 400 点：项1 = kappa_0(P+rho c^2/2) = %.6E > 0；"
        "项2 = (1-e^{-2Lambda})/r^2 = %.6E ~ %.6E > 0（物质内部 e^{-2Lambda}<1 恒成立）；"
        "项3 = alpha*beta*P/r*(1-r_s/r)，r>r_s 时符号 = sign(alpha*beta)。"
        "⇒ alpha*beta>0 时三项**全正**：即使先令 alpha*beta=0（去掉挠率项），(项1+项2) 的最小值仍为 "
        "%.6E > 0；取 alpha*beta=+1 时 f 最小值 = %.6E > 0 ⇒ **无解**。"
        "来料「给定物态方程 P(rho) 就可以求解 r_c」在此情形下**不成立**。"
        % (term1, min(term2(r) for r in scan), max(term2(r) for r in scan), fmin0, fmin))

    # --- D01b 反解：任意 r_c 都能配出 alpha*beta ---
    need = []
    for rc in (rs * Dc("1.05"), rs * Dc(2), rs * Dc(5), rs * Dc(50), rs * Dc(1000)):
        ab = -(term1 + term2(rc)) * rc / (Pc * (Dc(1) - rs / rc))
        need.append((rc, ab))
    spread = max(abs(x[1]) for x in need) / min(abs(x[1]) for x in need)
    selfchk("D01b 自检：对任意 r_c > r_s 均可反解出使方程成立的 alpha*beta（5 点）",
            all(abs(f_rc(rc, ab)) / term1 < Dc("1e-40") for rc, ab in need),
            "最大残差/项1 = %.2E" % max(abs(f_rc(rc, ab)) / term1 for rc, ab in need))
    add("D01b 该方程的判别力（关键）：一个未知数 vs 两个自由参数", "FAIL",
        "给定 (P_c, rho_c, r_s) 后，方程只约束**乘积 alpha*beta**。反解显示：欲使 r_c = 1.05 r_s / 2 r_s / "
        "5 r_s / 50 r_s / 1000 r_s，分别只需 alpha*beta = %s ⇒ **跨 %.2E 倍的一族解全部存在**。"
        "⇒ 该方程**不可能被任何观测否证**：测到任意临界半径都能回头配一组 (alpha,beta)；"
        "反之任意 (alpha,beta) 也都能给出某个 r_c。⇒ 所谓「隐式闭式解」"
        "**只是把两个自由参数重排成一个未知数**，净信息量 = 0。（与 r23 Q04「豁免型判据」同型。）"
        % (" / ".join(fmt(x[1], 6) for x in need), spread))

    # --- D02 delta tau 与 tau_r 的导数一致性 ---
    beta = Dc("1.0")

    def tau_r(r):
        return beta / r * (Dc(1) - rs / r)

    r0 = rs * Dc("1.7")
    h = r0 * Dc("1e-20")
    num = (tau_r(r0 + h) - tau_r(r0 - h)) / (Dc(2) * h)
    ana = -beta / (r0 * r0) * (Dc(1) - Dc(2) * rs / r0)
    ok_d = rel(num, ana) < Dc("1e-25")
    selfchk("D02 自检：d/dr[beta/r (1-r_s/r)] = -beta/r^2 (1-2 r_s/r)（中心差分残差 <1e-25）",
            ok_d, "%.2E" % rel(num, ana))
    add("D02 §2 微扰方程(4) delta tau = -beta/r_c^2 (1-2 r_s/r_c) delta r 是否为 tau_r 的微分",
        "PASS",
        "数值微分 %.12E vs 解析式 %.12E，相对残差 %.2E ⇒ **确为 tau_r(r) 的导数**，"
        "是来料中少数推导正确的一步（量纲亦齐，见 A11）。PASS。"
        % (num, ana, rel(num, ana)))

    # --- D03 boxed 方程 -> 隐式方程的代数等价 ---
    ok_alg = True
    for L in (Dc("0.3"), Dc("-0.7"), Dc("1.9")):
        e2 = (Dc(2) * L).exp()
        lhs = -(-Dc(2) * L).exp() / Dc(1) * (Dc(1) - e2)
        rhs = (-Dc(2) * L).exp() * (e2 - Dc(1))
        if rel(lhs, rhs) > Dc("1e-40"):
            ok_alg = False
    selfchk("D03 自检：-e^{-2L}(1-e^{2L}) = e^{-2L}(e^{2L}-1)（3 组 Lambda）", ok_alg, "")
    add("D03 §2 boxed 方程 → 隐式闭式方程的代数翻折", "PASS",
        "三项逐字对应、符号翻折正确（残差 <1e-40）⇒ 这一步是**正确的代数整理**，"
        "失败不在变换而在被变换的方程本身（见 A04 / D01）。")

    # --- D04 来料对旧 ODE 的自诊 ---
    d_old_rhs = dmul(dpow(C, -2), RIC)          # (A0 B0/c^2) * (-2 Lambda A)
    ok = (d_old_rhs == dpow(LEN, -2))
    add("D04 片段6 前置诊断：旧微扰 ODE 中因子 A_0 B_0/c^2 破坏量纲", "PASS" if not ok else "FAIL",
        "右端 [A_0B_0/c^2 · (-2 Lambda A)] = %s，左端 [d^2A/dr^2] = L^-2 ⇒ 确**不齐**，"
        "来料的自我诊断**正确**。但修正方式（直接移除该因子）见 D05。"
        % dstr(d_old_rhs))

    need_ka = ddiv(dpow(LEN, -2), dpow(LEN, -1))
    add("D05 「移除 A_0B_0/c^2」这一修法本身引入的新约束", "CORRECTED",
        "移除后方程 d^2(delta A)/dr^2 = -2 Lambda (delta A) + kappa*alpha*d(delta A)/dr，"
        "要量纲齐须 [kappa*alpha] = %s = L^-1。而来料 §1 称 [alpha]=L、kappa 未给量纲"
        " ⇒ 修法把量纲问题**从显式因子转嫁到未声明的 kappa**，属于「修了症状」。"
        % dstr(need_ka))

    add("D06 片段6 §4 球对称不辐射引力波（Birkhoff）vs 同片段从球对称微扰推 l=2 张量模", "FAIL",
        "来料自述「球对称本身不辐射引力波，引力波来自非球对称微扰，取 l=2」；"
        "但片段6/7 建立的整个微扰体系（delta Phi, delta Lambda, delta P, delta rho, delta v_r）"
        "**只有径向依赖、无球谐分解** ⇒ 该体系只含 l=0，**不含 l=2 扇区**。"
        "⇒ 用球对称微扰体系的结论去谈 l=2 引力波是**范畴错置**："
        "要么补球谐分解（则原微扰方程组需整体重推），要么承认该体系与引力波无关。")

    # --- D07 tau_0 -> alpha 的预测力 ---
    img = [(-TWO_PI / Dc(x)).exp() for x in ("0.05", "0.5", "5", "50")]
    add("D07 片段1 §14 声称「不用实验输入，由拓扑几何直接导出 alpha」", "FAIL",
        "实际做法 = **用 alpha 的实验值反解 tau_0**（findroot），再正向代回「预测」同一个 alpha"
        " ⇒ **循环拟合**，不是导出。机器确认映射 tau_0 ↦ exp(-2pi/tau_0) 是 (0,inf) → (0,1) 的**双射**："
        "tau_0 = %s 分别给出 %s ⇒ 值域覆盖 (0,1) 全域，**任给 alpha ∈ (0,1) 都有解**"
        " ⇒ 该关系对 alpha 的取值**零约束力**（换任何无量纲常数都成立）。"
        "另：来料声称 alpha = f(tau_0, G, c, e)，但实际式 exp(-2pi/tau_0) **不含 G、c、e** ⇒ 签名与式子不符。"
        % (" / ".join(("0.05", "0.5", "5", "50")), " / ".join(fmt(v, 6) for v in img)))

    # --- D08 伪精度复发 ---
    digits = {"G": 6, "alpha": 11, "Lambda": 5, "c": 9}
    worst_in = min(digits.values())
    add("D08 「250 位精度」声称的有效位核算", "FAIL",
        "输入有效位：G 6 位、alpha 11 位、Lambda 5 位、c 9 位 ⇒ **最弱环节 5 位**，"
        "其余 245 位全是噪声。⇒ 250 位 dps 是**伪精度**。登记为 r23 N05 的**第 2 次复发**，"
        "并再次确认 r23 沉淀的跨册纪律：**数值判据的阈值必须来自输入不确定度传播，不得拍脑袋取机器零**。")

    add("D09 片段2 §12 涡旋 ↔ 挠率的「几何-流体对偶字典」的性质", "BOUNDARY",
        "该字典（涡线↔世界线、涡量↔自旋联络、涡线曲率/挠率↔时空曲率/挠率）是**逐条人工指定的对应关系**，"
        "不是推导：R^3 中曲线的 Frenet 不变量与联络的反对称部分是**不同范畴**的数学对象，"
        "二者之间不存在自然函子（同本库 R14「Lk 不是规范量子数的函数」的缺函子结论）。"
        "⇒ 该映射可作**启发式类比**登记，不可作**导出**引用；"
        "「Helmholtz 涡通量守恒 ↔ TUFT 拓扑不变量守恒」是类比句，不是定理。")

    add("D10 片段7 §六-2「TUFT 可能存在额外极化分量」的前置条件", "BOUNDARY",
        "Poincare 规范理论（PGT/ECSK）确可给出 6 种极化模式，但**前提是挠率有动力学**（传播自由度）。"
        "本库 r20 已判：在来料的作用量形式下 tau 是**代数 slave 而非传播场**；"
        "r19 已判「作用量与 ADM 演化方程不同源」。⇒ 在挠率动力学补齐之前，"
        "「额外极化」是**未兑现的承诺**，不能计入可证伪预言清单。")

    # --- D11 色散项的可观测性 ---
    omega = TWO_PI * Dc("100")                      # LIGO 敏感带 ~100 Hz
    rho_ism = Dc("1e-21")                           # 星际介质平均质量密度 kg/m^3
    R_ism = k0 * rho_ism * CD.c ** 2
    delta_w2 = CD.c ** 2 * R_ism                    # c^2 * kappa*alpha*R，取 kappa*alpha = 1
    ratio_w = delta_w2 / (omega * omega)
    bound_ka = CD.u_G / CD.G
    add("D11 片段6 §4 引力波色散修正的可观测性（本册最强定量读数）", "FAIL",
        "修正项 ∝ 背景 Ricci 标量 R：①**真空区 R ≡ 0**（GR 真空解 Ricci 标量为零）"
        " ⇒ 引力波在传播路径上**修正恒为零**；②即便取星际介质 rho ~ %s kg/m^3 ⇒ R ~ %.3E m^-2，"
        "c^2*kappa*alpha*R / omega^2（omega = 2pi*100 Hz）≈ %.3E（已令 kappa*alpha = 1）；"
        "③再叠加 C08 由 G 精度给出的 |kappa*alpha| ≲ %.2E ⇒ **相对相位修正上界 %.2E**。"
        "⇒ 该色散预言在 LIGO 及任何可预见探测器上**不可观测**，"
        "来料「可利用 LIGO 事件残差做参数限制」不成立（限制存在但等于把参数压到 0，无新物理）。"
        % (rho_ism, R_ism, ratio_w, bound_ka, ratio_w * bound_ka))
    selfchk("D11 自检：色散相对修正上界 < 1e-30（可观测性判据）",
            (ratio_w * bound_ka) < Dc("1e-30"), "%.2E" % (ratio_w * bound_ka))

    # --- D12 数值常数交叉核对 ---
    k0_ref = Dc("2.0766e-43")
    selfchk("D12 自检：kappa_0 = 8 pi G/c^4 与本库 r18/r22 归档读数 2.0766e-43 一致",
            rel(k0, k0_ref) < Dc("1e-4"), "%s vs %s" % (fmt(k0), fmt(k0_ref)))
    mP_ref = Dc("2.176434e-8")
    selfchk("D13 自检：m_P = sqrt(hbar c/G) 与 CODATA 公布值一致",
            rel(CD.m_P(), mP_ref) < Dc("1e-5"), "%s vs %s" % (fmt(CD.m_P()), fmt(mP_ref)))


ROUTE_ANSWERS = {
    "分支1 · TUFT-TOV 数值积分与质量-半径曲线": (
        "**不推荐按原计划推进**。阻塞点不在积分器而在方程：本册 A04 已判临界方程三项不齐、"
        "D01 已判 alpha*beta>0 时无解、D01b 已判该方程零判别力。"
        "⇒ 先做 P0：①固定 alpha/beta 的量纲与符号；②固定 kappa/κ_0/kappa_0 三个符号的命名；"
        "③给出 c_s^2 = dP/drho 与 EOS。三条补齐后，TOV 积分才是**可判真假的数值实验**。"),
    "分支2 · 引力波偏振模式": (
        "**阻塞于挠率动力学**（同本库 r20）：来料的作用量使 tau 为代数 slave，无传播自由度 ⇒ 无额外极化。"
        "且 D06 已判当前球对称微扰体系不含 l=2 扇区。**先修 D06 再谈分支 2**，否则是空转。"),
    "分支3 · alpha/kappa 的重整化群跑动": (
        "**当前不可做**：RG 需要可重整的作用量 + 传播场，而 tau 非传播（r20）。"
        "另注意 C08：G 的 CODATA 精度已把 |kappa*alpha| 压到 ≲ 2.2e-5 ⇒ 即便跑动做出，"
        "其低能效应也已低于现有测量精度 4~5 个量级。性价比最低的一条。"),
    "分支4 · LaTeX 论文骨架（PRD）": (
        "**无争议可并行，但建议延后**：来料目前有 4 处硬量纲错误（A01/A02/A04/A08）、"
        "1 处伪数值（C01）、1 处伪精度（C04/D08）。按现状成稿会把错误固化进可引用文本"
        "（同 r23 N04 教训）。建议 P0 改稿后再写。"),
    "分支5 · 旋转（稳态轴对称）TUFT 解": (
        "**不推荐先做**：球对称层尚有 A04/D01/D06 三条未闭合，升维到轴对称只会把同样的"
        "量纲与符号问题乘以 2（并引入 frame-dragging 与挠率轴向分量的新自由度）。"
        "层级上属于「在坏地基上加层」。"),
    "分支6 · 回到公理体系重证 tau_{mu nu} = alpha R_{mu nu}": (
        "**推荐，且应最先做**。本册全部结构性问题（A02/A04/B01/B04/D01）**同源**："
        "tau_{mu nu} 到底是挠率张量（L^-1）还是挠率能动张量（L^-2）？"
        "alpha 是 L、无量纲、还是 M^-1T^2？这两个问题不回答，后面五条分支全在错误符号上推进。"
        "⇒ 建议顺序：**分支6 → P0 改稿 → 分支1 → 分支2/4**。"),
}

P0_ACTIONS = [
    "统一 alpha 的量纲与命名：精细结构常数改称 alpha_fs，耦合系数改称 alpha_tau（并给出唯一量纲）",
    "统一 kappa：Frenet 曲率 kappa_F、挠率耦合 kappa_T、引力耦合 kappa_0，三者不得混写",
    "统一 tau：固有时改称 tau_p（或 s），挠率张量 tau^rho_{mu nu}，挠率能动张量 mathcal{T}_{mu nu}",
    "按 A02 把耦合项改写为量纲齐的形式，或显式声明 [alpha] = M^-1 T^2 并放弃 [alpha] = L 的声称",
    "重推临界半径方程使三项同量纲（A04），并声明 alpha*beta 的符号（D01）",
    "补 c^2 并修正符号与因子 2（C06 的 e^{2Lambda}），或改用标准 TOV 的 e^{-2Lambda} = 1 - 2Gm(r)/(c^2 r)",
    "删除或重跑片段5 的本征值输出表（C01：输出与代码差 1e12 且 r=1000 处符号相反）",
    "复核片段1 的 tau_0 = 0.9622… 与 alpha = 7.297e-3（C03：代入得 80% 偏差），并撤回「残差 1e-16 / 250 位」表述",
    "把「导出 alpha」改写为「以 alpha 定标 tau_0」（D07），或给出真正不含实测输入的独立约束",
    "删除或补定义 tuft_predict_G（C07），使校验脚本可运行",
    "给引力波修正项写出 F[tau,Q] 的显式表达式，否则该修正不可证伪（A10）",
    "声明「四极公式」系数 2G/(c^4 R)（A10 当前缺因子 2）",
]


def main():
    section_A()
    section_B()
    section_C()
    section_D()

    verdicts = {}
    for it in ITEMS:
        verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
    self_ok = sum(1 for s in _SELF if s["ok"])

    hocus = {
        "H（稳固/自洽）": [
            "A09 波动方程 Box h + kaRh = 16piG/c^4 delta T 三项齐且系数 = 2*kappa_0 正确",
            "A11 tau_r = (beta/r)(1-r_s/r) 反解 [beta] 无量纲，量纲干净",
            "D02 delta tau = d tau_r/dr * delta r 确为 tau_r 的微分（数值微分残差 <1e-25）",
            "D03 boxed 方程 → 隐式方程的代数翻折逐字正确",
            "D04 来料对旧 ODE「A_0B_0/c^2 破坏量纲」的自我诊断正确",
        ],
        "O（欠定/约定依赖）": [
            "A07 mathcal{T}_{mu nu} 量纲仅在「e_0 = 四速度」的非标准约定下自洽",
            "A10 引力波修正项 F[tau,Q] 无定义 ⇒ 不可计算、不可证伪",
            "C09 求解器输入 (P_c, rho_c, r_s) 三者互相矛盾且缺 c_s^2",
            "D09 涡旋↔挠率对偶字典是人工指定，缺函子（同 R14）",
            "D10 额外极化模式的前置 = 挠率动力学（r20 已判 tau 非传播场）",
        ],
        "C（缺陷/冲突/已否证）": [
            "A01 [kappa_0] 声称 M^-1LT^2（真值 L^-1M^-1T^2，差 L^2）",
            "A02/A03 同一 alpha 在主方程与微扰方程中被要求三个互不相容的量纲",
            "A04 临界半径方程三项不可相加（项3 差 LMT^-2）",
            "A05/A06 kappa = c_perp/c^2 量纲为 L^-1T，且与 omega = c*kappa 自相矛盾",
            "A08 色散式缺 c^2（差 L^2T^-2）",
            "B01-B05 五组符号同名异义（alpha/kappa/tau/挠率张量家族/Lambda）",
            "C01 本征值输出表与自身代码差 1e12（r=1000 处符号相反）⇒ 伪数值",
            "C01b 同一 M 矩阵在正文与代码中两个不同定义",
            "C02 背景解 A0 漏质量因子 M",
            "C03/C03b/C04 公布的 tau_0 代入得 80% 偏差，与「残差 1e-16」互斥；250 位为伪精度",
            "C06 度规函数漏 c^2、符号反、因子差 2（三错叠加）",
            "C07 校验脚本调用未定义的 tuft_predict_G ⇒ 从未运行",
            "C08 Rust chi^2 一维退化，最小在 u=kappa*alpha=0",
            "D01/D01b 临界方程 alpha*beta>0 无解；且对任意 r_c 都能反解出参数 ⇒ 零判别力",
            "D05 移除 A_0B_0/c^2 只是把量纲问题转嫁给未声明的 kappa",
            "D06 球对称体系（仅 l=0）被用于推导 l=2 引力波 ⇒ 范畴错置",
            "D07 tau_0 ↦ alpha 是双射 ⇒ 零预测力，且是反解拟合而非导出",
            "D11 色散相对修正上界 < 1e-40（真空区恒为零）⇒ 不可观测",
        ],
        "U（需新输入/新公理）": [
            "tau_{mu nu} 的张量阶与量纲（L^-1 挠率张量 vs L^-2 挠率能动张量）必须由公理层指定",
            "alpha 的唯一定量纲与数值来源（目前 0.082 / 1/137 / L / 无量纲 四选一未定）",
            "beta 的符号与量级（决定 r_c 是否存在）",
            "挠率动力学的来源（决定额外极化是否存在）",
        ],
    }

    payload = {
        "round": "r26",
        "date": "2026-10-10",
        "target": ("TUFT V2.1：恒星球对称流体微扰 + 临界半径闭式隐式解 + 引力波辐射 + 量纲全维修复"
                   "（含前序片段 §4/§9/§12/§14 与两次球对称微扰稿）"),
        "engine": os.path.basename(__file__),
        "items": len(ITEMS),
        "verdicts": verdicts,
        "selfcheck": {"n_ok": self_ok, "n_all": len(_SELF), "items": _SELF},
        "items_detail": ITEMS,
        "rating_target": "C / L1（来料体系：4 处硬量纲错误 + 伪数值 + 伪精度 + 核心方程零判别力）",
        "rating_book": "O / L2（本册：审计结论中 A07/A10/C09/D09/D10 依赖符号约定或外部输入）",
        "HOCU": hocus,
        "key_numbers": {
            "kappa_0 = 8 pi G/c^4": fmt(CD.kappa0()),
            "m_P = sqrt(hbar c/G)": fmt(CD.m_P()),
            "alpha_pred from tau_0=0.962241978827134": fmt((-TWO_PI / Dc("0.962241978827134")).exp()),
            "alpha_CODATA": fmt(CD.alpha),
            "tau_0_star = -2pi/ln(alpha)": fmt(-TWO_PI / CD.alpha.ln()),
            "|kappa*alpha| 1sigma bound from G": fmt(CD.u_G / CD.G),
            "dispersion relative bound (LIGO 100Hz, ISM)": fmt(
                (CD.c ** 2 * CD.kappa0() * Dc("1e-21") * CD.c ** 2)
                / ((TWO_PI * Dc("100")) ** 2) * (CD.u_G / CD.G)),
        },
        "route_answers": ROUTE_ANSWERS,
        "P0_actions": P0_ACTIONS,
        "open_items": [
            "X-R26-1：tau_{mu nu} 的张量阶与量纲未定（L^-1 挠率张量 vs L^-2 挠率能动张量），"
            "是 A02/A04/B04 三条硬错的共同根因",
            "X-R26-2：alpha 的量纲与数值四义未收敛（0.082 / 1/137 / L / 无量纲）",
            "X-R26-3：beta 的符号与量级未定 ⇒ 临界半径方程对任意 r_c 可配解（零判别力）",
            "X-R26-4：引力波修正泛函 F[tau,Q] 未定义 ⇒ 该项不可证伪",
            "X-R26-5：tau_0 的拓扑整数 n 从未给出 n≠1 的实例（空族量子化）",
        ],
        "recurrence": [
            "恒等式复读（|Omega|*Delta s = 2 pi）：库内第 6 次（前 5 次见 r22 A07/D01、r23 P03）",
            "250 位伪精度：第 2 次（首次 r23 N05）",
            "代码从未运行却给出数值输出：第 2 次（首次 r23 N04）",
            "挠率非传播场 ⇒ 额外极化不可兑现：第 2 次（首次 r20）",
        ],
    }

    os.makedirs(OUTDIR, exist_ok=True)
    stem = "TUFT-V21球对称流体微扰与临界半径_全维审计_2026-10-10"
    json_path = os.path.join(OUTDIR, stem + ".json")
    md_path = os.path.join(OUTDIR, stem + ".md")
    txt_path = os.path.join(OUTDIR, stem + "_report.txt")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# TUFT V2.1 球对称流体微扰与临界半径 · 全维机器审计（r26）")
    lines.append("")
    lines.append("- 日期：2026-10-10")
    lines.append("- 引擎：`源码/%s`（纯标准库：Decimal 60 位 + Fraction 量纲向量 + ast 静态扫描）" % os.path.basename(__file__))
    lines.append("- 读数：**条目 %d ｜ %s ｜ 自检 %d/%d**"
                 % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False), self_ok, len(_SELF)))
    lines.append("- 评级：来料 **%s** ｜ 本册 **%s**" % (payload["rating_target"], payload["rating_book"]))
    lines.append("")
    lines.append("## 一、逐条读数")
    lines.append("")
    lines.append("| # | 条目 | 判定 | 说明 |")
    lines.append("|---|---|---|---|")
    for i, it in enumerate(ITEMS, 1):
        d = it["detail"].replace("|", "\\|")
        lines.append("| %d | %s | **%s** | %s |" % (i, it["name"], it["verdict"], d))
    lines.append("")
    lines.append("## 二、关键数值")
    lines.append("")
    for k, v in payload["key_numbers"].items():
        lines.append("- `%s` = %s" % (k, v))
    lines.append("")
    lines.append("## 三、归一化 H/O/C/U")
    lines.append("")
    for k, v in hocus.items():
        lines.append("### %s（%d 条）" % (k, len(v)))
        lines.append("")
        for x in v:
            lines.append("- %s" % x)
        lines.append("")
    lines.append("## 四、回答来料末尾的六条分支")
    lines.append("")
    for k, v in ROUTE_ANSWERS.items():
        lines.append("- **%s**：%s" % (k, v))
    lines.append("")
    lines.append("## 五、P0 改稿清单（零争议，当天可完成）")
    lines.append("")
    for a in P0_ACTIONS:
        lines.append("- %s" % a)
    lines.append("")
    lines.append("## 六、新增开放项与复发登记")
    lines.append("")
    for x in payload["open_items"]:
        lines.append("- %s" % x)
    lines.append("")
    for x in payload["recurrence"]:
        lines.append("- 复发：%s" % x)
    lines.append("")
    lines.append("## 七、自检")
    lines.append("")
    for s in _SELF:
        lines.append("- [%s] %s %s" % ("PASS" if s["ok"] else "FAIL", s["name"],
                                       ("（%s）" % s["detail"]) if s["detail"] else ""))
    lines.append("")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write("TUFT V2.1 球对称流体微扰与临界半径 全维审计 r26 · 运行记录\n")
        fh.write("=" * 74 + "\n")
        fh.write("条目 %d ｜ %s\n自检 %d/%d\n\n"
                 % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False), self_ok, len(_SELF)))
        for i, it in enumerate(ITEMS, 1):
            fh.write("[%02d] %-9s %s\n     %s\n" % (i, it["verdict"], it["name"], it["detail"]))
            if it["note"]:
                fh.write("     注: %s\n" % it["note"])
        fh.write("\n" + "-" * 74 + "\n")
        for k, v in ROUTE_ANSWERS.items():
            fh.write("%s: %s\n" % (k, v))

    print("")
    print("=" * 78)
    print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    print("自检：%d/%d" % (self_ok, len(_SELF)))
    for s in _SELF:
        if not s["ok"]:
            print("  自检未过：%s %s" % (s["name"], s["detail"]))
    print("产物：")
    for p in (json_path, md_path, txt_path):
        print("  " + os.path.relpath(p, BASE))
    print("=" * 78)
    sys.exit(0 if self_ok == len(_SELF) else 1)


if __name__ == "__main__":
    main()




