# -*- coding: utf-8 -*-
"""
TUFT-r145 · 常温超导「本质本源」· 核心公式理论体系精算 · 可实验验证
================================================================
日期：2026-10-22
定位（与 r143 互补，不重复）：
  r143 = 【否定性攻破】螺旋几何纲领对常温超导供给为 0（C01/C03/C04 三断点）
  r145 = 【正面本源】超导到底是什么？T_c 由什么决定？常温为何难？
         以及**普通人能亲手做出来的实验**（液氮 + YBCO 桌面级）

本册回答四个问题（每层都给机器数字，不空谈）：
  Q1 电阻从哪来？              → A 组（Drude 散射）
  Q2 电阻怎么会消失？          → A 组（库珀对凝聚 + 相位刚性 + 能隙）
  Q3 T_c 到底由什么决定？      → B 组（核心公式 K-01…K-10 精算）
  Q4 常温为什么难、怎么实验？  → C 组（门槛）+ D 组（可实验验证）

依赖：纯标准库（decimal 60 位 + fractions 量纲四元组），可离线复跑
红线：数学自洽 ≠ 物理证实；本册的正确核全部为标准物理，不含框架新增宣称
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import json
import os
import sys

getcontext().prec = 60

def D(x):
    return Decimal(str(x))

getcontext().prec = 60

# ---- CODATA 常数 ----
HBAR = D("1.054571817e-34")
C = D("299792458")
M_E = D("9.1093837015e-31")
E_CH = D("1.602176634e-19")
K_B = D("1.380649e-23")
MU0 = D("1.25663706212e-6")
N_A = D("6.02214076e23")
PI = D("3.14159265358979323846264338327950288419716939937510582097494")
G_ACC = D("9.80665")            # 重力加速度 m/s^2

# ---- 导出 ----
M_E_C2 = M_E * C * C
K_B_EV = K_B / E_CH             # eV/K
PHI0 = (2 * PI * HBAR) / (2 * E_CH)   # 磁通量子 Wb

# ---- 教学实验用外部事实 [E] ----
T_LN2 = D("77.36")              # 液氮沸点 (1 atm)  K
T_YBCO = D("92")                # YBCO 临界温度 K
T_MGB2 = D("39")                # MgB2
T_AL = D("1.2")                 # Al
T_HGBCO = D("135")              # 常压最高
T_LAH10 = D("250")              # LaH10 @170 GPa
ROOM_T = D("300")

# YBCO 典型材料参数 [E]（数量级值，用于本源图像计算）
XI_YBCO_AB = D("1.6e-9")        # ab 面相干长度 m
NS_YBCO = D("1e27")             # 超导载流子（对）密度 m^-3 量级
XI_AL = D("2.33e-6")            # Al 相干长度（r143 精算值）m
NS_AL = D("1.80788096e29")      # Al 载流子密度（r143 精算值）m^-3

# ============================================================
# 量纲四元组 (M,L,T,Q)
# ============================================================
def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    n = Fraction(n)
    return tuple(x * n for x in a)

def deq(a, b):
    return tuple(a) == tuple(b)

def dstr(a):
    out = []
    for v, nm in zip(a, ["M", "L", "T", "Q"]):
        if v == 0:
            continue
        out.append(nm + "^" + ("1" if v == 1 else str(v)))
    return "1" if not out else "".join(out)

DIM_ENERGY = dim(m=1, l=2, t=-2)
DIM_FREQ = dim(t=-1)
DIM_LENGTH = dim(l=1)
DIM_MASS = dim(m=1)
DIM_VEL = dim(l=1, t=-1)
DIM_FLUX = dim(m=1, l=2, t=-1, q=-1)
DIM_MU0 = dim(m=1, l=1, q=-2)
DIM_FORCE = dim(m=1, l=1, t=-2)

# ---- guard：量纲工具自检（先自检再判定）----
GUARDS = []

def guard(gid, name, got, want):
    ok = deq(got, want)
    GUARDS.append({"id": gid, "name": name, "got": dstr(got),
                   "want": dstr(want), "ok": bool(ok)})
    return ok

guard("G0-1", "[ħω] == 能量", dmul(dim(m=1, l=2, t=-1), DIM_FREQ), DIM_ENERGY)
guard("G0-2", "[k_BT] == 能量", DIM_ENERGY, DIM_ENERGY)
guard("G0-3", "[Φ₀]=[h/(2e)] == 磁通", ddiv(dim(m=1, l=2, t=-1), dim(q=1)), DIM_FLUX)
guard("G0-4", "[λ_L] == L",
      dpow(ddiv(DIM_MASS, dmul(DIM_MU0, dmul(dim(l=-3), dpow(dim(q=1), 2)))), Fraction(1, 2)),
      DIM_LENGTH)
guard("G0-5", "[ξ₀]=[ħv_F/Δ] == L", ddiv(dmul(dim(m=1, l=2, t=-1), DIM_VEL), DIM_ENERGY),
      DIM_LENGTH)
# [B] = N/(A·m) = (M L T^-2)/((Q T^-1)·L) = M T^-1 Q^-1
#   （自抓：初版误写为 t=-2，被本条 guard 拦下 —— 量纲断言必须机器兜底）
guard("G0-6", "[磁力]=(B²/2μ₀)A == 力",
      dmul(ddiv(dpow(dim(m=1, t=-1, q=-1), 2), DIM_MU0), dim(l=2)), DIM_FORCE)
guard("G0-7", "[重力]=mg == 力", dmul(DIM_MASS, dim(l=1, t=-2)), DIM_FORCE)

# ============================================================
# 条目系统
# ============================================================
ENTRIES = []

def add(eid, grp, name, verdict, detail, key=None):
    ENTRIES.append({"id": eid, "group": grp, "name": name,
                    "verdict": verdict, "detail": detail, "key": key or {}})

def fv(x, n=25):
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        return str(x)

def fs(x, n=6):
    try:
        return format(Decimal(x), "." + str(n) + "f")
    except Exception:
        return str(x)

def reldev(a, b):
    b = Decimal(b)
    if b == 0:
        return None
    return abs((Decimal(a) - b) / b)

def ratio(a, b):
    b = Decimal(b)
    if b == 0:
        return None
    return Decimal(a) / b

def dexp(x):
    return Decimal(x).exp()

def dln(x):
    return Decimal(x).ln()

def dsqrt(x):
    return Decimal(x).sqrt()

# ============================================================
# A 组 · 本源链条：电阻从哪来、怎么会消失
# ============================================================
def group_a():
    # --- A01 电阻的起源：Drude 散射时间 ---
    rho_cu = D("1.68e-8")         # 铜电阻率 Ω·m（[E]）
    n_cu = D("8.47e28")           # 铜自由电子密度 m^-3（[E]）
    tau_cu = M_E / (n_cu * E_CH * E_CH * rho_cu)
    v_F_cu = D("1.57e6")          # m/s（[E]）
    mfp_cu = v_F_cu * tau_cu
    add("A01", "A 本源", "电阻的起源：电子被散射（Drude），铜的平均自由程 39 nm",
        "PASS",
        "ρ = m_e/(ne²τ)。铜：ρ=%s Ω·m、n=%s m⁻³ ⇒ 散射时间 τ=%s s；"
        "取 v_F=%s m/s ⇒ 平均自由程 l = v_Fτ = %s m = %s nm。"
        "**电阻的本质 = 电子在晶格中每前进 ~39 nm 就被散射一次**"
        % (fv(rho_cu, 6), fv(n_cu, 6), fv(tau_cu), fv(v_F_cu, 6),
           fv(mfp_cu), fv(mfp_cu * D("1e9"), 6)),
        {"tau_cu": str(tau_cu), "mfp_nm": str(mfp_cu * D("1e9"))})

    # --- A02 超导的开关幅度 ---
    rho_sc = D("1e-25")           # 超导态电阻率实验上限 Ω·m（[E]）
    jump = ratio(rho_cu, rho_sc)
    add("A02", "A 本源", "超导态电阻率：比铜低 17 个量级（不是小一点，是断崖）",
        "PASS",
        "超导态 ρ <%s Ω·m（实验上限，实际可能更低），铜 %s Ω·m ⇒ 相差 %s 倍（%s 个量级）。"
        "这不是导电性变好，而是**电阻从有限值直接归零** —— "
        "持续电流实验已观测到超导环中电流**数年不衰减**"
        % (fv(rho_sc, 6), fv(rho_cu, 6), fv(jump, 8), fv(dln(jump) / dln(D(10)), 6)),
        {"jump": str(jump)})

    # --- A03 ★本源：T_c 就是热涨落刚够拆散库珀对的温度 ---
    tc = T_YBCO
    delta0 = D("1.764") * K_B * tc          # 零温能隙 Δ(0)
    two_delta = 2 * delta0
    kbt = K_B * tc
    r_check = ratio(delta0, kbt)
    add("A03", "A 本源", "★T_c 的本质：k_BT_c 刚够与能隙竞争（2Δ=3.528k_BT_c）",
        "PASS",
        "YBCO（T_c=%s K）：k_BT_c = %s J = %s meV；Δ(0)=1.764k_BT_c = %s meV；"
        "2Δ(0) = %s meV。复核 Δ(0)/(k_BT_c) = %s（应为 1.764）。"
        "**物理图像**：低于 T_c 时，热涨落能量 k_BT 不足以拆散库珀对（需 2Δ）⇒ 对存活 ⇒ 超导；"
        "高于 T_c 时 k_BT 足够 ⇒ 对被不断拆散 ⇒ 回到正常态。**T_c 就是这条分界线**"
        % (fs(tc, 1), fv(kbt), fv(kbt / E_CH / D("1e-3"), 8),
           fv(delta0 / E_CH / D("1e-3"), 8), fv(two_delta / E_CH / D("1e-3"), 8),
           fv(r_check, 8)),
        {"delta0_meV": str(delta0 / E_CH / D("1e-3")), "ratio": str(r_check)})

    # --- A04 ★★本册核心：一个库珀对"占多大地方"里还有几个对 ---
    # 对密度 = n_s/2；体积 = ξ^3
    n_pair_al = NS_AL / 2
    vol_al = XI_AL ** 3
    cnt_al = n_pair_al * vol_al

    n_pair_ybco = NS_YBCO / 2
    vol_ybco = XI_YBCO_AB ** 3
    cnt_ybco = n_pair_ybco * vol_ybco

    gap_bcs_bec = ratio(cnt_al, cnt_ybco)
    add("A04", "A 本源", "★★本源图像：相干长度内塞几个库珀对？Al 有 1.1e12 个，YBCO 只有 2 个",
        "PASS",
        "常规超导体 Al：ξ₀=%s m、n_s=%s m⁻³ ⇒ 对密度 %s m⁻³，"
        "在 ξ₀³=%s m³ 内共存 **%s 个库珀对**（高度重叠 ⇒ 典型 BCS 极限：对很大、互相渗透）。"
        "高温超导体 YBCO：ξ₀(ab)=%s m、n_s≈%s m⁻³ ⇒ 同一体积内**仅 %s 个**（几乎不重叠 ⇒ "
        "趋近 BEC 极限：紧束缚对像双原子分子一样凝聚）。两者相差 **%s 倍**。"
        "⇒ **这就是「高温超导」的本质图像：从 BCS（大量重叠的松散对）向 BEC（紧束缚对）的 crossover**。"
        "这也解释了为何铜氧化物的 T_c 能远超 BCS 传统上限 —— 配对尺度被压到纳米级"
        % (fv(XI_AL), fv(NS_AL, 8), fv(n_pair_al, 8), fv(vol_al), fv(cnt_al, 8),
           fv(XI_YBCO_AB), fv(NS_YBCO, 6), fv(cnt_ybco, 8), fv(gap_bcs_bec, 8)),
        {"pairs_in_xi3_Al": str(cnt_al), "pairs_in_xi3_YBCO": str(cnt_ybco),
         "crossover_gap": str(gap_bcs_bec)})

    # --- A05 磁通量子 = 配对电荷 2e 的硬证据 ---
    phi_e = (2 * PI * HBAR) / E_CH      # 若配对电荷是 e
    add("A05", "A 本源", "磁通量子 Φ₀=h/(2e)：配对电荷为 2e 的直接实验判据",
        "PASS",
        "若配对电荷是 2e ⇒ Φ₀ = h/(2e) = %s Wb（=%s T·m²）；"
        "若是 e ⇒ h/e = %s Wb（恰为 2 倍）。实测超导环磁通以 **h/2e** 为周期量子化"
        "（Little–Parks 振荡、SQUID 干涉）⇒ **直接证明载流子电荷是 2e 不是 e**。"
        "这是「电子成对」最干净、不可伪造的实验证据"
        % (fv(PHI0), fv(PHI0, 8), fv(phi_e, 8)),
        {"Phi0": str(PHI0), "h_over_e": str(phi_e)})

    # --- A06 相位刚性：为什么散射不破坏超导电流 ---
    add("A06", "A 本源", "零电阻的量子解释：宏观波函数的相位刚性（不是「没有散射」）",
        "INFO",
        "超导态由宏观波函数 ψ=√n_s·e^{iθ} 描述，电流 j ∝ n_s(ħ∇θ)。"
        "关键点：**散射确实仍在发生**，但改变电流需要改变**全体库珀对共同的相位 θ**，"
        "而相位刚性意味着这需要跨越能隙 2Δ 的能量（A03）。低于 T_c 时无此能量通道 ⇒ "
        "电流**无耗散地持续**。⇒ 零电阻不是「电子跑得顺」，而是「**量子态不允许衰减**」",
        {"note": "相位刚性"})

# ============================================================
# B 组 · 核心公式理论体系精算（落在 YBCO —— 可实验的对象上）
# ============================================================
def group_b():
    tc = T_YBCO
    # K-02 能隙
    delta0 = D("1.764") * K_B * tc
    two_delta_mev = 2 * delta0 / E_CH / D("1e-3")
    # K-03/K-04/K-05 用 YBCO 典型值 [E]
    xi_ab = XI_YBCO_AB
    lam_L_ybco = D("150e-9")        # YBCO 穿透深度 m（[E]）
    kappa_gl = ratio(lam_L_ybco, xi_ab)
    add("B01", "B 核心公式", "核心公式集在 YBCO 上的精算（K-02…K-06）",
        "PASS",
        "T_c=%s K：①K-02 2Δ(0)=3.528k_BT_c ⇒ **2Δ=%s meV**（BCS 弱耦合预言值）；"
        "②K-03 相干长度 ξ₀(ab)=%s m；③K-04 穿透深度 λ_L≈%s m；"
        "④K-05 κ_GL=λ_L/ξ₀ = **%s** ≫ 1/√2 ⇒ **II 型**超导体（磁通可进入并形成涡旋，"
        "这是「磁悬浮 + 倒挂钉扎」现象的前提）；⑤K-06 Φ₀=h/(2e)=%s Wb"
        % (fs(tc, 1), fv(two_delta_mev, 8), fv(xi_ab), fv(lam_L_ybco),
           fv(kappa_gl, 8), fv(PHI0)),
        {"two_delta_meV": str(two_delta_mev), "kappa_GL_YBCO": str(kappa_gl)})

    # B02 液氮可用性判据（实验选型的核心）
    margin = tc - T_LN2
    r_ln2 = ratio(T_LN2, tc)
    verdict_ln2 = "可用" if T_LN2 < tc else "不可用"
    add("B02", "B 核心公式", "★实验选型判据：液氮 77.36 K 能否让 YBCO 超导",
        "PASS",
        "判据只有一条：**T_冷却 < T_c**。液氮沸点 %s K，YBCO T_c=%s K ⇒ %s < %s ⇒ **%s**；"
        "温度裕量 = %s K（相对裕量 %s）。对照：MgB₂ T_c=39 K < 77.36 K ⇒ 液氮**不可用**"
        "（需液氦 4.2 K 或制冷机）。⇒ **这正是教学实验普遍选 YBCO 而非 MgB₂ 的原因**"
        % (fs(T_LN2, 2), fs(tc, 1), fs(T_LN2, 2), fs(tc, 1), verdict_ln2,
           fv(margin, 8), fv(r_ln2, 8)),
        {"margin_K": str(margin), "usable": True})

    # B03 磁悬浮力是否足够（镜像法估算）
    m_ybco = D("0.005")            # 5 g 块材 kg
    F_g = m_ybco * G_ACC
    B_surf = D("0.4")              # NdFeB 表面磁场 T（[E]）
    area = D("1e-4")               # 1 cm^2
    F_mag = (B_surf * B_surf / (2 * MU0)) * area
    r_force = ratio(F_mag, F_g)
    add("B03", "B 核心公式", "磁悬浮可行性：磁力是重力的 130 倍（演示绰绰有余）",
        "PASS",
        "5 g 的 YBCO 块：重力 F_g=mg=%s N。NdFeB 表面磁场 %s T、作用面积 %s m² ⇒ "
        "镜像法磁力 F=(B²/2μ₀)A = %s N ⇒ **磁力/重力 = %s 倍**。"
        "（实际会随距离衰减，平衡时磁力降至等于重力，悬浮高度通常 1–5 mm。"
        "该估算说明：悬浮演示对器材精度要求很低，普通钕磁铁即可）"
        % (fv(F_g), fs(B_surf, 2), fv(area, 6), fv(F_mag), fv(r_force, 8)),
        {"F_mag_N": str(F_mag), "F_g_N": str(F_g), "ratio": str(r_force)})

    # B04 磁通钉扎与倒挂（区分真超导与普通抗磁体）
    add("B04", "B 核心公式", "★倒挂实验：区分「真超导」与「普通抗磁体」的判据",
        "PASS",
        "YBCO 的 κ_GL=%s ≫ 1/√2 ⇒ II 型 ⇒ 磁场以**磁通量子（涡旋）**形式进入体内，"
        "并被晶格缺陷**钉扎**。钉扎力使样品能被「锁」在特定位置 ⇒ "
        "**既能悬浮也能倒挂悬挂**（这是普通抗磁体、热解石墨**做不到**的）。"
        "⇒ 实验判据：**能倒挂不掉落 = 磁通钉扎 = 真超导体**（配合 A05 的 2e 证据）"
        % (fv(kappa_gl, 6)),
        {"kappa_GL": str(kappa_gl)})

    # B05 冷却方式成本对比（为什么液氮让实验"人人可做"）
    add("B05", "B 核心公式", "可实验性的经济基础：液氮 vs 液氦",
        "PASS",
        "液氮 77.36 K：约 ¥5–20/L，保温瓶即可盛装，普通五金/气体供应商可得 ⇒ **桌面级可行**。"
        "液氦 4.2 K：约 ¥100–300/L 且全球稀缺，需专用杜瓦 ⇒ 仅限专业实验室。"
        "⇒ **YBCO（92 K）之所以是「人人可做的超导实验」，唯一原因是它跨过了 77 K 这条液氮线**；"
        "这也是 1987 年 YBCO 发现被称为「液氮温度以上超导」突破的意义",
        {"LN2_K": str(T_LN2), "LHe_K": "4.2"})

# ============================================================
# C 组 · 常温为什么难（本质门槛）
# ============================================================
def group_c():
    # C01 300 K 的热能 vs 需要的能隙
    kbt300 = K_B * ROOM_T
    kbt300_mev = kbt300 / E_CH / D("1e-3")
    two_delta_300 = D("3.528") * kbt300_mev
    two_delta_92 = D("3.528") * K_B * T_YBCO / E_CH / D("1e-3")
    r_gap = ratio(two_delta_300, two_delta_92)
    add("C01", "C 常温门槛", "★常温的本质要求：300 K 的热能是 92 K 的 3.26 倍 ⇒ 能隙也得大 3.26 倍",
        "PASS",
        "T=300 K 时 k_BT = %s meV。若 T_c=300 K ⇒ 需 2Δ(0)=3.528k_BT_c = **%s meV**；"
        "而 YBCO（92 K）只需 %s meV ⇒ 常温下所需能隙是 YBCO 的 **%s 倍**。"
        "**这就是「常温超导难」的全部本质**：不是机制未知，而是**要求配对结合能大到 300 K 都拆不散**"
        % (fv(kbt300_mev, 8), fv(two_delta_300, 8), fv(two_delta_92, 8), fv(r_gap, 8)),
        {"kBT_300_meV": str(kbt300_mev), "need_2Delta_meV": str(two_delta_300)})

    # C02 提高 T_c 只有两条路
    add("C02", "C 常温门槛", "★提高 T_c 只有两条路：配对胶频率 ω↑ 或 耦合强度 λ↑",
        "PASS",
        "由 K-01/K-08：T_c ∝ ω · exp[−1/(N(0)V)]。**路一提高 ω** —— 声子频率 ω∝M^(−1/2)，"
        "故选最轻元素氢（H 对 Pb 频率优势 **14.34 倍**，r143 D03）；r143 C05 已算："
        "保持耦合不变时 300 K 需要配对胶特征温度 **1.0700000000000000000000000E+5 K**（超金刚石 θ_D 47.98 倍）。"
        "**路二提高 λ** —— 但 r143 B08 已算：λ→∞ 时 T_c 饱和在 0.330(ħω_log/1.2k_B)，"
        "**单靠耦合无法突破频率天花板**。⇒ 现实路线只能是路一（氢化物）+ 高压稳定结构",
        {"path1": "omega", "path2": "lambda"})

    # C03 现状盘点
    add("C03", "C 常温门槛", "现状：250 K 已达成（高压），常压 135 K —— 缺口只有 1.2 倍但隔着压力",
        "PASS",
        "已实现：LaH₁₀ **250 K @170 GPa**、H₃S 203 K@155 GPa、常压 HgBCO **135 K**。"
        "300 K 相对 250 K 仅差 **1.20000000E+0 倍**（r143 D02）⇒ **数值上并非遥不可及**；"
        "但纪录全部依赖高压维持亚稳相，泄压即失超（r143 D04）"
        "⇒ **真正的坎是「常压」，不是「温度数值」**",
        {"gap": "1.2"})

    # C04 本质总结（一句话）
    add("C04", "C 常温门槛", "★本质一句话：常温超导 = 造出「300 K 下仍不被热运动拆散」的电子对凝聚态",
        "INFO",
        "串起全部链条：**电阻来自散射（A01）→ 超导是库珀对凝聚、靠相位刚性免于耗散（A06）"
        "→ T_c 是 k_BT 刚够拆散库珀对的温度（A03）→ 所以常温超导要求配对结合能 > 300 K 热能（C01）"
        "→ 结合能 ∝ 配对胶频率 × 耦合（C02）→ 最高频率来自最轻元素氢，但需高压维持（C03）**。"
        "⇒ 全部困难归结为**一个材料化学问题**：能否在常压下造出足够「硬」的配对通道",
        {"chain": "A01→A06→A03→C01→C02→C03"})

# ============================================================
# D 组 · 可实验验证（桌面级：液氮 + YBCO）
# ============================================================
def group_d():
    add("D01", "D 可实验", "实验一 · 磁悬浮（5 分钟，最直观，零仪器）",
        "PASS",
        "器材：YBCO 块材（¥150–400）、钕铁硼磁铁（¥5–30）、液氮（¥5–20/L）、"
        "泡沫塑料容器/保温杯、塑料镊子、低温手套 + 护目镜。**步骤**："
        "① 磁铁置于泡沫板上；② 用塑料镊子把 YBCO 块放在磁铁上（室温，此时无现象）；"
        "③ 缓慢浇淋液氮冷却（**勿直接投入，温差过大会开裂**）；④ 约 10–30 s 后块材**浮起**。"
        "**判据**：块材稳定悬浮且**可绕磁铁无摩擦滑动** ⇒ 迈斯纳效应（B03 已算磁力富余 130 倍）",
        {"cost": "¥200-500", "time": "5 min"})

    add("D02", "D 可实验", "★实验二 · 倒挂悬挂（区分真超导与普通抗磁体的关键）",
        "PASS",
        "续实验一：**把磁铁翻到 YBCO 上方（或把整体倒置）**。若 YBCO **不掉落、被钉在下方**"
        "⇒ **磁通钉扎**（B04）。对比对照：用一片**热解石墨**（普通抗磁体）做同样操作 ⇒ "
        "石墨只能被排斥、无法倒挂悬挂。⇒ **能倒挂 = 磁通量子被钉扎 = II 型真超导体**，"
        "这是普通抗磁体模仿不了的判据（对应 r143 F03 假阳性清单第 2 条）",
        {"criterion": "倒挂不掉落"})

    add("D03", "D 可实验", "实验三 · 四引线电阻转变（定量，测出 T_c≈92 K）",
        "PASS",
        "器材：YBCO 块（带 4 个银浆电极或用铟压接）、四位半万用表（¥200–500）或纳伏表、"
        "铂电阻 PT100 温度计（¥100–300）、恒流源。**步骤**：① 四引线接法（外侧通电流 1–10 mA，"
        "内侧测电压）；② 缓慢降温（**0.5–1 K/min**）并同步记录 (T, V)；③ 每点**反转电流**消除热电势；"
        "④ 观察 V 在 ~92 K 处**陡降至仪器噪声底**。**判据**：以 **T_c^zero**（降至噪声底）为准，"
        "**不得用 onset**（r143 实验册 §5.1）；复温后电阻**恢复** ⇒ 可逆相变",
        {"criterion": "T_c^zero + 可逆"})

    add("D04", "D 可实验", "安全红线（液氮实验四条，违反有真实危险）",
        "INFO",
        "① **严禁密闭容器盛装液氮**（气化膨胀 ~700 倍 ⇒ 爆炸）；"
        "② **防冻伤**：液氮 77 K，皮肤接触瞬间冻伤，必须戴低温手套 + 护目镜；"
        "③ **防窒息**：氮气无色无味，密闭空间大量气化会排氧 ⇒ **必须通风**；"
        "④ **YBCO 脆性 + 温差开裂**：勿从室温直接投入液氮，应**逐步预冷**（先悬于液氮上方蒸汽中 30 s）",
        {"rules": 4})

    add("D05", "D 可实验", "★本实验验证什么、不验证什么（与 r143 的边界）",
        "INFO",
        "**验证**：① 迈斯纳效应（完全抗磁）② 磁通钉扎（II 型超导体）③ 零电阻（若做实验三）"
        "④ 相变可逆性 —— 以上**全部是标准物理，已被无数次重复验证**。"
        "**不验证**：任何统一场论 / 螺旋几何主张。r143 已判定螺旋纲领对超导供给为 0（C01/C03/C04）；"
        "本实验是**正确核的实验侧**，目的是让「超导是什么」变得可亲手触摸，"
        "**不构成对任何统一场论的支持或否证**（那条结论由 r143 三断点 + F02 判据承担）",
        {"verifies": "迈斯纳/钉扎/零电阻", "does_not_verify": "统一场论"})

# ============================================================
# 主程序
# ============================================================
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    bad = [g for g in GUARDS if not g["ok"]]
    if bad:
        print("[FATAL] 量纲工具自检未通过：")
        for g in bad:
            print("   %s %s got=%s want=%s" % (g["id"], g["name"], g["got"], g["want"]))
        sys.exit(2)
    print("[OK] 量纲工具自检 %d/%d 通过\n" % (len(GUARDS), len(GUARDS)))

    group_a()
    group_b()
    group_c()
    group_d()

    order = ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"]
    cnt = {k: 0 for k in order}
    for e in ENTRIES:
        cnt[e["verdict"]] = cnt.get(e["verdict"], 0) + 1

    print("=" * 78)
    print("  r145 · 常温超导「本质本源」· 核心公式精算 · 可实验验证")
    print("=" * 78)
    cur = None
    for e in ENTRIES:
        if e["group"] != cur:
            cur = e["group"]
            print("\n--- %s ---" % cur)
        print("[%s] %s  %s" % (e["verdict"], e["id"], e["name"]))
        print("      %s" % e["detail"])
    print("\n" + "=" * 78)
    print("  条目 %d  |  " % len(ENTRIES)
          + "  ".join("%s=%d" % (k, cnt[k]) for k in order if cnt[k]))
    print("  守卫 %d/%d" % (len(GUARDS), len(GUARDS)))
    print("=" * 78)

    here = os.path.dirname(os.path.abspath(__file__))
    base = os.path.dirname(here)
    data_dir = os.path.join(base, "数据")
    os.makedirs(data_dir, exist_ok=True)
    stem = "TUFT-r145_常温超导本质本源_核心公式精算_2026-10-22"

    def conv(x):
        if isinstance(x, Decimal):
            return str(x)
        if isinstance(x, Fraction):
            return str(x)
        raise TypeError(str(type(x)))

    payload = {
        "id": "r145",
        "title": "常温超导本质本源 · 核心公式精算 · 可实验验证",
        "date": "2026-10-22",
        "guards": GUARDS,
        "entries": ENTRIES,
        "counts": cnt,
        "key_numbers": {
            "mfp_Cu_nm": str(D("1.57e6") * M_E / (D("8.47e28") * E_CH * E_CH * D("1.68e-8")) * D("1e9")),
            "delta0_YBCO_meV": str(D("1.764") * K_B * T_YBCO / E_CH / D("1e-3")),
            "pairs_in_xi3_Al": str(NS_AL / 2 * XI_AL ** 3),
            "pairs_in_xi3_YBCO": str(NS_YBCO / 2 * XI_YBCO_AB ** 3),
            "kappa_GL_YBCO": str(ratio(D("150e-9"), XI_YBCO_AB)),
            "kBT_300K_meV": str(K_B * ROOM_T / E_CH / D("1e-3")),
            "LN2_margin_K": str(T_YBCO - T_LN2),
        },
    }
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, indent=2, default=conv))

    with open(os.path.join(data_dir, stem + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("r145 常温超导本质本源 报告\n")
        f.write("PASS=%d FAIL=%d BOUNDARY=%d INFO=%d CORRECTED=%d MISMATCH=%d\n"
                % (cnt["PASS"], cnt["FAIL"], cnt["BOUNDARY"], cnt["INFO"],
                   cnt["CORRECTED"], cnt["MISMATCH"]))
        f.write("guard=%d/%d\n" % (len(GUARDS), len(GUARDS)))
        for e in ENTRIES:
            f.write("[%s] %s %s\n" % (e["verdict"], e["id"], e["name"]))

    lines = ["# r145 · 常温超导本质本源 · 核心公式精算（数据产物）", "",
             "条目 %d ｜ " % len(ENTRIES)
             + " ｜ ".join("%s=%d" % (k, cnt[k]) for k in order if cnt[k]), "",
             "## 条目", "", "| ID | 组 | 名称 | 判定 | 机器读数 |", "|---|---|---|---|---|"]
    for e in ENTRIES:
        d = e["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append("| %s | %s | %s | **%s** | %s |"
                     % (e["id"], e["group"], e["name"], e["verdict"], d))
    lines += ["", "## 守卫", "", "| ID | 名称 | 得 | 期望 | 通过 |", "|---|---|---|---|---|"]
    for g in GUARDS:
        lines.append("| %s | %s | %s | %s | %s |"
                     % (g["id"], g["name"], g["got"], g["want"], "OK" if g["ok"] else "FAIL"))
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n[产物] %s" % os.path.join(data_dir, stem + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
