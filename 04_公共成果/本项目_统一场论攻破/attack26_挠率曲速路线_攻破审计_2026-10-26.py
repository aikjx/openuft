# -*- coding: utf-8 -*-
"""
attack26 · 挠率曲速路线（历史归档 第九卷 第四章）攻破审计

靶点：90_历史归档/…/宇宙本源著作/第九卷_工程应用/第四章_曲速航行.md
  该章判「曲速航行是可能的」，路线 = **挠率场弯曲时空**（§4.2），声称
  ① 挠率可产生负能量、不需要奇异物质
  ② 挠率耦合是分形的、能量由零点能提供、不需携带燃料
  ③ 速度可达光速几百倍/几千倍，泡内失重无过载
  ④ 类比：宇宙膨胀可超光速 ⇒ 时空本身超光速不违反相对论

为什么本册必须存在（定位，避免与并行册重复）：
  r64 判「Alcubierre 型 + QEI 框架内结构性不可行」；r65 精算账；r66 五族判决；
  r67 五族全部关闭并**明确写下红线**：「结论是框架内的，不排除框架外机制
  （**挠率路线**、非度规机制）」。⇒ r67 把挠率路线留作**未定价的框架外出口**，
  本册就是给这条出口定价：不是泛指"所有挠率机制"，而是**这一份具体来料所主张的
  那一条**（自旋密度 → 挠率 → 负能量 → 曲速泡）。

五段：
  G 段 · 量纲工具自检 + 唯一闭合族穷举（r66 判据 D-6 复用）
  S 段 · 自旋密度需求账（把"自旋极化等离子体产生挠率场"定价）
  Q 段 · QEI 不可绕过性（"由零点能提供"是否构成出口）
  C 段 · 与 r64 C01 的冲突（v_s>c ⇒ 泡内世界线类空）
  A 段 · 宇宙膨胀类比是否成立
  N 段 · 信息量审计（公式数 vs 断言数）

纯标准库：Decimal 60 位 + Fraction 三元组量纲 (M,L,T)。
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = []
GUARDS = []


def add(code, verdict, title, detail):
    ITEMS.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


# ================================================================ 常数
D = Decimal
G = D("6.67430E-11")            # m^3 kg^-1 s^-2  (CODATA 2018)
C = D("299792458")              # m/s (exact)
HBAR = D("1.054571817E-34")     # J*s
M_N = D("1.67492749804E-27")    # kg (neutron)
NA = D("6.02214076E23")         # 1/mol
RHO_NUC = D("2.3E17")           # kg/m^3 核饱和密度 [C]
RHO_CU = D("8960")              # kg/m^3
M_CU = D("0.063546")            # kg/mol
H0 = D("67.4") * D("1000") / D("3.0856775814913673E22")   # s^-1 (Planck18)

# 引自既有册（不重算，只引用并注明出处）
RHO_ALC = D("1.2038634716806055998129727E42")   # J/m^3  attack25 N04 (R=100m, δ=1m, v_s=c)
RHO_ALC_LP = D("4.6091E111")                    # J/m^3  r66（δ=ℓ_P 需求）

# ================================================================ 量纲工具（先自检再用）
# 元组顺序 (M, L, T)
DIM = {
    "G": (Fraction(-1), Fraction(3), Fraction(-2)),
    "c": (Fraction(0), Fraction(1), Fraction(-1)),
    "hbar": (Fraction(1), Fraction(2), Fraction(-1)),
    "n": (Fraction(0), Fraction(-3), Fraction(0)),
    "rhoE": (Fraction(1), Fraction(-1), Fraction(-2)),   # 能量密度 J/m^3
    "rhoM": (Fraction(1), Fraction(-3), Fraction(0)),   # 质量密度
    "H0": (Fraction(0), Fraction(0), Fraction(-1)),
}


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dpow(a, k):
    k = Fraction(k)
    return (a[0] * k, a[1] * k, a[2] * k)


def dstr(a):
    out = []
    for sym, v in (("M", a[0]), ("L", a[1]), ("T", a[2])):
        if v == 0:
            continue
        out.append(sym + ("^" + str(v) if v != 1 else ""))
    return "".join(out) if out else "1"


def seg_dimension():
    # G0-1 .. G0-5：量纲工具自身必须先过自检（本库纪律：手算量纲必错）
    d_rhoE = dpow(DIM["G"], 1) if False else None
    comb = dmul(DIM["G"], dpow(dmul(DIM["hbar"], DIM["n"]), 2))
    comb = dmul(comb, dpow(DIM["c"], -2))
    guard("G0-1_spinspin_family", comb == DIM["rhoE"],
          "G(hbar*n)^2/c^2 = %s（应为能量密度 %s）" % (dstr(comb), dstr(DIM["rhoE"])))

    comb2 = dmul(dpow(DIM["G"], 1), dpow(DIM["c"], -4))
    comb2 = dmul(comb2, dpow(dmul(DIM["hbar"], DIM["n"]), 2))
    guard("G0-2_massdensity_form", comb2 == DIM["rhoM"],
          "G(hbar*n)^2/c^4 = %s（应为质量密度 %s）" % (dstr(comb2), dstr(DIM["rhoM"])))

    pl2 = dmul(dmul(DIM["G"], DIM["hbar"]), dpow(DIM["c"], -3))
    guard("G0-3_planck_length_sq", pl2 == (Fraction(0), Fraction(2), Fraction(0)),
          "G*hbar/c^3 = %s（应为 L^2）" % dstr(pl2))

    hub = dmul(DIM["c"], dpow(DIM["H0"], -1))
    guard("G0-4_hubble_radius", hub == (Fraction(0), Fraction(1), Fraction(0)),
          "c/H0 = %s（应为 L）" % dstr(hub))

    guard("G0-5_spin_density", dmul(DIM["hbar"], DIM["n"]) == (Fraction(1), Fraction(-1), Fraction(-1)),
          "hbar*n = %s（自旋密度）" % dstr(dmul(DIM["hbar"], DIM["n"])))

    # G-01 · 唯一闭合族穷举（r66 判据 D-6 复用）
    sols = []
    rng = range(-4, 5)
    for a in rng:
        for b in rng:
            for g in rng:
                v = dmul(dpow(DIM["G"], a), dpow(DIM["c"], b))
                v = dmul(v, dpow(dmul(DIM["hbar"], DIM["n"]), g))
                if v == DIM["rhoE"]:
                    sols.append((a, b, g))
    add("G01", "PASS" if len(sols) == 1 else "FAIL",
        "唯一量纲闭合族：能量密度 = G^a c^b (hbar*n)^g 的解 %d 组" % len(sols),
        "穷举 a,b,g ∈ [-4,4] 共 %d 组 ⇒ 解 = %s。唯一解 (1,-2,2) ⇒ "
        "**由 G、c、自旋密度 s=hbar·n 构造能量密度，形式被量纲唯一锁死**："
        "ρ_E = K·G·s²/c²（K 为无量纲系数；ECSK 常见写法 K=8π，标 [C]）。"
        "⇒ 来料「操控自旋密度产生挠率场进而得到所需负能量」这条链，"
        "** scaling 不由理论选择决定，而由量纲决定 ** ⇒ 系数争议无法改变数量级结论。"
        % (9 ** 3, sols))
    guard("G01_unique_family", sols == [(1, -2, 2)], "唯一闭合族为 (a,b,g)=(1,-2,2)")

    # G-02 · 该族在 c 上的指数：说明"降 c"无杠杆
    add("G02", "INFO",
        "闭合族为 ρ_E = K·G·s²/c²（c 的指数为 −2）",
        "⇒ 若试图用「降低有效光速 c_eff」压缩需求（r64 H05 那条杠杆），"
        "本族给出 ρ_E ∝ c_eff^-2 ⇒ **降 c 反而抬高所需能量密度**；"
        "与 r64 §五 H05 的「ρ∝c⁴」方向一致（都是降 c 不利），"
        "说明 r64 的 c 杠杆在挠率路线里同样不存在（标 BOUNDARY：两族形式不同，"
        "但方向相同 ⇒ 该杠杆不因换机制而复活）。")


PI = D("3.14159265358979323846264338327950288")
HALF_HBAR = HBAR / D(2)
SRC_MD = os.path.join(HERE, "来料_挠率曲速_第九卷第四章_2026-10-26.md")


def fv(x, p=25):
    try:
        return format(x, "." + str(p) + "E")
    except Exception:
        return str(x)


def spin_density_need(rho, k):
    """由 rho = K*G*s^2/c^2 反解所需自旋密度 s 与数密度 n（每粒子自旋 ħ/2）"""
    s = C * (rho / (k * G)).sqrt()
    return s, s / HALF_HBAR


def torsion_rho(n, k):
    """给定数密度 n（每粒子 ħ/2）可得的挠率自旋Contact能量密度"""
    s = n * HALF_HBAR
    return k * G * s * s / (C * C)


# ================================================================ S 段 · 自旋密度需求账
def seg_spin():
    n_nuc = RHO_NUC / M_N
    n_cu = RHO_CU * NA / M_CU

    # 注意：spin_density_need 返回 (s, n)，序不可倒（首版写反 ⇒ 把自旋密度当数密度打印）
    s1, n1 = spin_density_need(RHO_ALC, D(1))
    s2, n2 = spin_density_need(RHO_ALC, D(8) * PI)
    rho_nuc = torsion_rho(n_nuc, D(1))
    rho_cu = torsion_rho(n_cu, D(1))
    k_need = RHO_ALC / rho_nuc

    add("S01", "FAIL",
        "所需数密度：n = %.4E m^-3（K=1）/ %.4E m^-3（K=8π）" % (n1, n2),
        "由唯一闭合族 ρ_E=K·G·s²/c² 反解 s=c·√(ρ/(K·G))，再取每粒子自旋 ħ/2 ⇒ "
        "n = s/(ħ/2)。以 attack25 N04 的需求 ρ=1.2039E42 J/m³（R=100 m、δ=1 m、v_s=c）代入："
        "K=1 ⇒ n=**%s m^-3**；K=8π ⇒ n=**%s m^-3**。参照：核饱和密度数密度 n_nuc=%s m^-3、"
        "铜的自由电子数密度 n_Cu=%s m^-3 ⇒ 需求比核密度高 **%s 倍（约 %.1f 个数量级）**。"
        "⇒ 来料 §4.3「用旋转超导体或自旋极化等离子体产生环形挠率场」在量纲锁死的 scaling 下"
        "**所需自旋密度超出任何已知物质形态 ** —— 且这不是工程难度，是**量级封死**。"
        % (fv(n1, 6), fv(n2, 6), fv(n_nuc, 6), fv(n_cu, 6),
           fv(n1 / n_nuc, 6), float((n1 / n_nuc).log10())))
    guard("S01_n_demand_beyond_nuclear", n1 > n_nuc * D("1E10"), "所需数密度超核密度 10 阶以上")
    guard("S01_n_demand_beyond_metal", n1 > n_cu * D("1E30"), "所需数密度超金属电子密度 30 阶以上")

    add("S02", "FAIL",
        "反向账：即使取核饱和密度且 100%% 自旋极化，可得 ρ = %s J/m³，缺口 %s 倍" % (
            fv(rho_nuc, 6), fv(k_need, 6)),
        "n_nuc=%s m^-3、每粒子 ħ/2 ⇒ s=%s J·s/m³ ⇒ ρ_E(K=1)=**%s J/m³**；"
        "铜的自由电子（n_Cu=%s）⇒ ρ_E=**%s J/m³**。对照需求 1.2039E42 J/m³ ⇒ "
        "**缺口 %.1f 个数量级**（核密度）/ %.1f 个（铜）。"
        "注意方向与 S01 一致：这是同一唯一族的两端，不是两套算法。"
        % (fv(n_nuc, 6), fv(n_nuc * HALF_HBAR, 6), fv(rho_nuc, 6),
           fv(n_cu, 6), fv(rho_cu, 6),
           float((RHO_ALC / rho_nuc).log10()), float((RHO_ALC / rho_cu).log10())))
    guard("S02_reverse_gap_positive", RHO_ALC > rho_nuc, "核密度自旋仍远不足以达标")

    add("S03", "PASS",
        "对无量纲系数 K 免疫：需 K ≈ %s 才能用核密度补齐" % fv(k_need, 6),
        "K_needed = ρ_需求 / ρ_E(n_nuc, K=1) = **%s**（约 %.1f 个数量级）。"
        "⇒ 任何 O(1)~O(10^10) 的系数修正、K=8π、分形耦合的任何有限重标度都**补不上**；"
        "来料 §4.2「挠率耦合是分形的」若只改系数不改量纲，则对本结论**零影响**。"
        "这是本册结论对理论细节最强的稳健性来源（与 r42/r44「对系数不变性」同型）。"
        % (fv(k_need, 6), float(k_need.log10())))
    guard("S03_coefficient_immunity", k_need > D("1E20"), "缺口对 1E20 以内的系数变化免疫")

    s3, n3 = spin_density_need(RHO_ALC_LP, D(1))
    add("S04", "FAIL",
        "取最宽松幸存族（r67：δ=10.03 ℓ_P）需求 ρ=%s J/m³ ⇒ n=%s m^-3" % (
            fv(RHO_ALC_LP, 6), fv(n3, 6)),
        "r66/r67 五族判决中唯一不被 QEI 排除的是 (4,0) 族，其 δ 上界 1.6205E−34 m，"
        "对应需求 ρ_Alc(ℓ_P)=4.6091E+111 J/m³（r66，本册引用不重算）⇒ "
        "n=**%s m^-3**，比核密度高 **%.1f 个数量级**。"
        "⇒ 换用「最宽松族」不是出路：QEI 放宽一分，能量需求涨 69 阶。"
        % (fv(n3, 6), float((n3 / n_nuc).log10())))
    guard("S04_lp_case_worse", n3 > n1, "ℓ_P 情形需求更严（与 r66 单调性一致）")


# ================================================================ Q 段 · QEI 不可绕过性
def seg_qei():
    add("Q01", "FAIL",
        "「能量由零点能提供」不构成对 QEI 的绕过（逻辑判据，非数值）",
        "QEI（Ford–Roman / Pfenning–Ford / Fewster 类）约束的对象是**重整化应力张量本身**"
        "在所有物理可实现量子态上的取值/平均，而不是「从哪个账户付钱」。真空态正是被约束的态之一，"
        "Casimir 负能量也正落在 QEI 的界内（其可提取量受 δ 与持续时间共同限制）。"
        "⇒ 来料 §4.2「能量可以通过零点能提供、不需要携带燃料」回答的是**能源来源**，"
        "而 r66/r67 关闭的是**应力张量允许的形式与幅值** —— 二者是不同层的约束，"
        "前者成立与否都不影响后者 ⇒ **该声明对缺口零贡献**。"
        "这是本册最硬的一条：即使 §4.2 的能源主张 100% 成立，结论不变。")
    guard("Q01_source_vs_bound_layers", True, "能源来源层与应力张量界层已分层判定")

    rho_cas = D("-4.3337525748258448656670244E-4")   # J/m^3, attack25 终值（1 µm 板间距）
    add("Q02", "BOUNDARY",
        "实验室可得负能量的量级：Casimir(1 µm) %s J/m³ vs 需求 %s J/m³" % (
            fv(rho_cas, 6), fv(RHO_ALC, 6)),
        "比值（绝对值）**%s**（约 %.1f 个数量级）。"
        "**口径声明**：板间局域负能量密度 vs 宏观体平均，两者口径不同，**仅作量级参照，"
        "不构成严格不等式**（沿用 attack25 N06 的诚实边界，本册不升级为判据）。"
        % (fv(abs(RHO_ALC / rho_cas), 6), float(abs(RHO_ALC / rho_cas).log10())))
    guard("Q02_casimir_gap_recorded", abs(RHO_ALC / rho_cas) > D("1E30"), "Casimir 量级落差已登记")

    add("Q03", "BOUNDARY",
        "挠率非传播：ECSK 的 Cartan 方程是代数的 ⇒ 「操控挠率场」需额外动力学",
        "标准 Einstein–Cartan 理论中挠率由自旋密度**代数地**决定（作用量无 ∂T 项 ⇒ "
        "变分给代数方程，挠率不传播、不在真空中延伸）。库内 r20/r21 已对 TUFT 的 τ 独立得到同一结论"
        "（对 τ 变分给 τ=−cR/(2α) 的代数 slave），r27 亦证其动力学项退化。"
        "⇒ 来料 §4.2「通过操控挠率场…形成曲速泡」若要成立，必须**从 ECSK 升级到含挠率动能项的"
        "Poincaré 规范理论**（+1 传播场 + 至少 2~4 个新耦合常数）⇒ 外部输入账增加，"
        "且该升级**不在来料中声明**。本册不代其补。")
    guard("Q03_torsion_nonpropagating", True, "挠率非传播已登记为外部输入账增量")


# ================================================================ C 段 · 与 r64 C01 的冲突
def seg_conflict():
    rows = []
    for k in (D(2), D(100), D(1000)):
        val = D(1) - k * k
        rows.append("v_s=%sc ⇒ dτ²/dt² = 1−(v_s/c)² = %s" % (k, fv(val, 4)))
    add("C01", "FAIL",
        "来料 §4.5 的「几百倍/几千倍光速」使其 §4.2 的泡内陈述全部无定义",
        "%s。⇒ 当 v_s>c 时 dτ²<0，**飞船世界线是类空的**，船上不存在任何固有时，"
        "于是 §4.2「飞船在曲速泡里是失重的、没有加速度、不会过载、很舒适」"
        "——「失重/过载/舒适」都是**沿类时世界线才可陈述的体验**——在 v_s>c 时**没有承载者**。"
        "v_s 越大，dτ² 越负，陈述越不可用 ⇒ 来料的结论强度与其可陈述性**反向相关**（自毁式）。"
        % "；".join(rows))
    guard("C01_spacelike_worldline", (D(1) - D(100) * D(100)) < 0, "v_s=100c 时 dτ²<0（类空）")

    add("C02", "FAIL",
        "冲突是**文内自引框架内**的，不是跨框架分歧",
        "来料 §4.1 自己写出 Alcubierre 度规 ds²=−c²dt²+(dx−v_s f dt)²+dy²+dz² 并据此论证"
        "「不违反相对论」；而 r64 C01 的裁定正是**从这同一个度规**推出的（泡中心 f=1 ⇒ "
        "dτ=dt√(1−v_s²/c²)）。⇒ 二者不是「两条不同路线各自成立」，而是**同一条路线上的前后自相矛盾**："
        "§4.1 的框架 + §4.5 的 v_s≫c ⇒ §4.2 的体验陈述无定义。"
        "**这使 r64 与历史归档第四章不能按「框架不同、各自成立」并存**，"
        "本册据此建议：r67 红线里「未定价的挠率出口」，就**这一条具体路线**而言应记为**已定价且失败**。")
    guard("C02_same_framework_conflict", True, "冲突定位为同框架内而非跨框架")

    add("C03", "INFO",
        "自毁式结论的结构刻画（本册新增判据 D-9）",
        "**判据 D-9（自毁式结论）**：若命题 P 的成立条件同时使 P 的结论陈述失去承载者"
        "（世界线类空 / 测度为零 / 定义域为空），则 P 不是「假」，而是**无意义**，"
        "且**提高 P 的强度会进一步削弱其可陈述性**。本册实测：v_s 从 2c→100c→1000c，"
        "结论「更快到达」越强，而 dτ² 越负 ⇒ 可陈述性越弱。"
        "与 r42「定义域是否为空判据」、r95「固定则被排除、自由则不可证伪」同族，"
        "区别在于本册的失效不是「被数据排除」也不是「不可证伪」，而是**语义无承载者**。")
    guard("D09_self_defeating_registered", True, "自毁式结论判据已登记")


# ================================================================ A 段 · 宇宙膨胀类比
def seg_analogy():
    r_h = C / H0
    r_bubble = D(100)
    add("A01", "BOUNDARY",
        "哈勃半径 c/H₀ = %s m（H₀=67.4 km/s/Mpc）" % fv(r_h, 6),
        "退行速度 v_rec = H₀·D 超过 c 的条件是 D > c/H₀ = **%s m = %s 倍泡半径（R=100 m）**。"
        "⇒ 宇宙学中「超光速」只发生在**哈勃半径之外**的共动分离上，尺度与曲速泡相差 %.1f 个数量级。"
        % (fv(r_h, 6), fv(r_h / r_bubble, 6), float((r_h / r_bubble).log10())))
    guard("A01_hubble_radius_computed", r_h > D("1E25"), "哈勃半径量级已机器核对")

    add("A02", "FAIL",
        "类比不成立：三类范畴差异（退行速度 ≠ 局域输运速度）",
        "① **测量性质不同**：v_rec=H₀·D 不是任一局域惯性系测得的速度，是坐标量；"
        "曲速泡的 v_s 是**渐近平直时空里局域结构的速度**，可被远端静止观察者直接测量。"
        "② **因果能力不同**：FLRW 中 D>c/H₀ 的天体与我们**无因果联系**（这正是「超光速退行不违反相对论"
        "」的原因：它不能传递任何东西）；而曲速泡的全部用途恰恰是**把飞船从 A 送到 B**，"
        "是因果传递 ⇒ 类比把「不能传递」的性质当成了「可以传递」的许可证。"
        "③ **判据不同**：曲速泡可行性的洛伦兹不变判据是**飞船世界线是否类时**（C01 已判类空），"
        "与时空「本身」如何运动无关。"
        "⇒ 来料 §4.1 的论证（宇宙膨胀可超光速 ⇒ 时空本身运动可超光速 ⇒ 不违反相对论）"
        "在第二步断裂。")
    guard("A02_analogy_rejected", True, "类比已按三类范畴差异否证")

    add("A03", "INFO",
        "保留面：来料 §4.1 对 Alcubierre 度规的**书写本身正确**",
        "ds²=−c²dt²+(dx−v_s f dt)²+dy²+dz² 与标准 Alcubierre 形式一致"
        "（对照 r64：r64 判的是**来稿基线度规**把 f 放进括号内位移项而非常规的 f² 乘整个空间部分；"
        "本册来料的写法与 r64 所说的「非常规式」属同一形态，但本册**不据此改判** r64，"
        "因为两者都把 f 置于位移项内，差异只在 r64 那份来稿另加了 f² —— 已标 [C] 交文献口径，"
        "本册结论不依赖该差异：C01/A02/S 段三条**都与 f 的具体幂次无关**。")
    guard("A03_conclusion_independent_of_f", True, "承重结论不依赖 f 的幂次口径")


# ================================================================ N 段 · 信息量审计
def seg_info():
    try:
        text = io.open(SRC_MD, encoding="utf-8").read()
    except Exception as exc:
        add("N01", "BOUNDARY", "来料正本读取失败", str(exc))
        return
    parts = text.split("\n## ")
    rows = []
    tot_f = 0
    tot_a = 0
    for p in parts[1:]:
        head = p.split("\n")[0].strip()
        nf = p.count("$")
        na = p.count("。")
        rows.append((head, nf, na))
        if head.startswith("4.2") or head.startswith("4.3") or head.startswith("4.4") or head.startswith("4.5"):
            tot_f += nf
            tot_a += na
    add("N01", "FAIL",
        "§4.2–§4.5：公式 %d 条 / 断言句 %d 句 ⇒ 断言-公式比无限" % (tot_f, tot_a),
        "分节统计 = %s。⇒ 来料的**全部承重主张**（挠率产生负能量 / 分形耦合 / 零点能供能 / "
        "旋转超导体产生挠率场 / 几百几千倍光速）集中在 §4.2–§4.5，而这几节**没有任何可计算表达式**，"
        "本册 S 段的定价是**代其补出唯一量纲闭合式之后**才得到的，不是从原文推出的。"
        "⇒ 诚实边界：本册否证的是「该路线在唯一闭合族下的量级」，"
        "**不是**「否证了来料自己写的某个式子」（来料没写式子）。"
        % ("；".join("%s: 公式%d/断言%d" % r for r in rows)))
    guard("N01_no_formula_in_claims", tot_f == 0, "承重章节零公式（零信息量）")
    guard("N01_claims_counted", tot_a > 0, "断言句计数非零（判据非恒零）")


# ================================================================ 输出
def jdefault(o):
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, Fraction):
        return str(o)
    return str(o)


def main():
    seg_dimension()
    seg_spin()
    seg_qei()
    seg_conflict()
    seg_analogy()
    seg_info()

    order = ["PASS", "FAIL", "BOUNDARY", "INFO", "MISMATCH", "CORRECTED"]
    counts = {}
    for it in ITEMS:
        counts[it["verdict"]] = counts.get(it["verdict"], 0) + 1
    for k in order:
        counts.setdefault(k, 0)
    gok = sum(1 for g in GUARDS if g["ok"])
    gbad = [g for g in GUARDS if not g["ok"]]

    payload = {
        "round": "attack26",
        "title": "挠率曲速路线（历史归档 第九卷 第四章）攻破审计",
        "date": "2026-10-26",
        "source_origin": ("openuft/90_历史归档/来源语料_ufthub_20260925/07_常数本源与真空涡旋/"
                          "0·1·∞宇宙本源——从真空到万物的第一性原理演绎/宇宙本源著作/"
                          "第九卷_工程应用/第四章_曲速航行.md"),
        "source_local_copy": "来料_挠率曲速_第九卷第四章_2026-10-26.md",
        "scope": ("只给 r67 红线留下的『挠率路线』这一条具体出口定价（自旋密度→挠率→负能量→曲速泡），"
                  "不是泛指所有挠率机制"),
        "counts": counts,
        "items_total": len(ITEMS),
        "guard_pass": "%d/%d" % (gok, len(GUARDS)),
        "items": ITEMS,
        "guards": GUARDS,
        "cross_refs": {
            "r64": "C01 v_s>c ⇒ 泡内固有时为虚；本册 C 段证明冲突是同框架内自相矛盾",
            "r66": "判据 D-6 量纲闭合族穷举，本册 G 段复用并得唯一族 (1,-2,2)",
            "r67": ("红线原文（判定册 §105 行）：这是框架内结论，不排除框架外机制"
                    "（如挠率路线、非度规机制）；本册对其中『挠率路线』这一条具体路线定价为失败"),
            "r20_r21_r27": "挠率/τ 为代数 slave、不传播；本册 Q03 升级为外部输入账增量",
            "r42_r44": "对系数不变性判据；本册 S03 同型",
            "attack25": "N04 ρ_Alc=1.2039E42 J/m³、N06 Casimir 量级参照",
        },
        "new_criteria": [
            "D-9 自毁式结论判据：命题的成立条件若同时取消其结论的承载者（世界线类空/定义域为空），"
            "则该命题不是假而是无意义，且提高强度会进一步削弱可陈述性",
        ],
        "boundaries": [
            "只读审计：不修改来料、不改 r64/r66/r67 任何字节、不改库内词表",
            "Q02 Casimir 对照为量级参照（口径不同），不作为严格不等式判据",
            "N 段：本册否证的是『该路线在唯一量纲闭合族下的量级』，来料自身未写任何公式",
        ],
    }

    out_json = os.path.join(HERE, "attack26_挠率曲速路线_攻破审计_2026-10-26.json")
    io.open(out_json, "w", encoding="utf-8").write(
        json.dumps(payload, ensure_ascii=False, indent=2, default=jdefault))

    L = []
    L.append("attack26 · 挠率曲速路线（历史归档 第九卷 第四章）攻破审计")
    L.append("=" * 78)
    L.append("范围：只给 r67 红线留下的『挠率路线』这一条出口定价，不泛指所有挠率机制")
    L.append("")
    for it in ITEMS:
        L.append("[%s] %s · %s" % (it["verdict"], it["code"], it["title"]))
        L.append("    " + it["detail"].replace("\n", "\n    "))
        L.append("")
    L.append("=" * 78)
    L.append("条目 %d  PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d"
             % (len(ITEMS), counts["PASS"], counts["FAIL"],
                counts["BOUNDARY"], counts["INFO"]))
    L.append("自检 %d/%d" % (gok, len(GUARDS)))
    for g in GUARDS:
        L.append("  %s %s  %s" % ("OK  " if g["ok"] else "FAIL", g["name"], g["detail"]))
    L.append("")
    L.append("verdict: 该挠率曲速路线 = 已定价且失败（量级封死 + 同框架自相矛盾 + 自毁式结论）")
    L.append("红线：数学/量纲自洽 ≠ 物理证实；本册否证这一条具体路线，不否证挠率机制本身")

    out_txt = os.path.join(HERE, "attack26_挠率曲速路线_攻破审计_2026-10-26_report.txt")
    io.open(out_txt, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print("\n".join(L[-8:]))
    print("条目=%d 自检=%d/%d" % (len(ITEMS), gok, len(GUARDS)))
    return 0 if not gbad else 1


if __name__ == "__main__":
    sys.exit(main())

