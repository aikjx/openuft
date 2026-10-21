# -*- coding: utf-8 -*-
"""
TUFT-r143 · 常温超导 · 求导证明验证精算与攻破
=============================================
日期：2026-10-21
对象：常温（常压）超导 —— 螺旋几何纲领能否给出配对胶与 T_c
方法：求导链 B（BCS 正确核精算） + 求导链 C（螺旋频率代入） + 定价 + 判据
依赖：纯标准库（decimal 60 位 + fractions 量纲四元组）

分层（条目不可跨组相加）：
  A 组  电子螺旋几何：既有恒等式复算（判定对象=恒等式本身）
  B 组  BCS/Eliashberg 正确核：教科书核心公式机器验证
  C 组  ★攻破核心：螺旋内禀频率代入 BCS 的后果
  D 组  常温超导硬约束定价（外部事实 + 反解）
  E 组  最小增广定价
  F 组  判别性实验判据

红线：数学自洽 ≠ 物理证实。本册不产生新物理，只做既有框架的可算判定。
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import json
import os
import sys

getcontext().prec = 60

# ============================================================
# 0. CODATA 常数（Decimal 高精度）
# ============================================================
def D(x):
    return Decimal(str(x))

HBAR = D("1.054571817e-34")      # J*s
C = D("299792458")               # m/s
M_E = D("9.1093837015e-31")      # kg
E_CH = D("1.602176634e-19")      # C
K_B = D("1.380649e-23")          # J/K
MU0 = D("1.25663706212e-6")      # N/A^2
EPS0 = D("8.8541878128e-12")     # F/m
N_A = D("6.02214076e23")         # 1/mol
M_P = D("1.67262192369e-27")     # kg (proton)
U_AMU = D("1.66053906660e-27")   # kg
EV = E_CH                        # J

# 导出常数
M_E_C2 = M_E * C * C                 # 电子静能 J
HBAR_OMEGA_E = M_E_C2                # = hbar * omega_e
OMEGA_E = M_E_C2 / HBAR              # 康普顿角频率 s^-1
PI = D("3.14159265358979323846264338327950288419716939937510582097494")
LAMBDA_C_BAR = HBAR / (M_E * C)      # 约化康普顿波长 m
LAMBDA_C = 2 * PI * LAMBDA_C_BAR     # 康普顿波长 m
T_E_ENERGY = M_E_C2 / K_B            # m_e c^2 / k_B  (K)
PHI0 = (2 * PI * HBAR) / (2 * E_CH)  # 磁通量子 h/(2e)  Wb

# 实测超导外部事实（T_c 单位 K，压力单位 GPa）
# 来源口径：常压最高 / 高压氢化物。均标注为 [E] 外部输入。
TC_HGBCO = D("135")       # HgBa2Ca2Cu3O8+d 常压（常压最高）
TC_HGBCO_HP = D("164")    # 高压 ~30 GPa
TC_H3S = D("203")         # H3S @ 155 GPa
TC_LAH10 = D("250")       # LaH10 @ 170 GPa
ROOM_T = D("300")         # 常温目标 K

# 铝的 BCS 标定用
TC_AL = D("1.2")          # K
THETA_D_AL = D("428")     # 德拜温度 K

# ============================================================
# 1. 量纲四元组 (M, L, T, Q) —— 指数相加/取负，必须先自检
# ============================================================
def dim(m=0, l=0, t=0, q=0):
    """构造量纲四元组 (M,L,T,Q)"""
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dmul(a, b):
    """量纲相乘 = 指数逐分量【相加】（纪律：不是相乘）"""
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    """量纲取幂 = 指数逐分量乘以 n"""
    n = Fraction(n)
    return tuple(x * n for x in a)

def dinv(a):
    return tuple(-x for x in a)

def deq(a, b):
    return tuple(a) == tuple(b)

def dstr(a):
    names = ["M", "L", "T", "Q"]
    out = []
    for v, nm in zip(a, names):
        if v == 0:
            continue
        s = "1" if v == 1 else str(v)
        out.append(nm + "^" + s)
    return "1" if not out else "".join(out)

DIM_ENERGY = dim(m=1, l=2, t=-2)          # M L^2 T^-2
DIM_FREQ = dim(t=-1)                      # T^-1
DIM_LENGTH = dim(l=1)                     # L
DIM_TEMP = dim(0, 0, 0, 0)                # 温度单独记（K），本册用能量/ k_B 代替
DIM_FLUX = dim(m=1, l=2, t=-1, q=-1)      # Wb
DIM_MASS = dim(m=1)
DIM_MU0 = dim(m=1, l=1, q=-2)             # N/A^2 = M L Q^-2
DIM_VEL = dim(l=1, t=-1)
DIM_DENSITY = dim(l=-3)                   # 数密度

# ============================================================
# 2. guard G0 —— 量纲工具自身自检（先过守卫，再用于判定）
# ============================================================
GUARDS = []

def guard(gid, name, got, want, ok=None):
    if ok is None:
        ok = deq(got, want)
    GUARDS.append({"id": gid, "name": name, "got": dstr(got),
                   "want": dstr(want), "ok": bool(ok)})
    return bool(ok)

# G0-1  hbar*omega_e 是能量
guard("G0-1", "[hbar*omega_e] == 能量",
      dmul(dim(m=1, l=2, t=-1), DIM_FREQ), DIM_ENERGY)
# G0-2  约化康普顿波长是长度
guard("G0-2", "[hbar/(m_e c)] == L",
      ddiv(dim(m=1, l=2, t=-1), dmul(DIM_MASS, DIM_VEL)), DIM_LENGTH)
# G0-3  康普顿角频率是频率
guard("G0-3", "[m_e c^2/hbar] == T^-1",
      ddiv(DIM_ENERGY, dim(m=1, l=2, t=-1)), DIM_FREQ)
# G0-4  磁通量子是磁通
guard("G0-4", "[h/(2e)] == 磁通",
      ddiv(dim(m=1, l=2, t=-1), dim(q=1)), DIM_FLUX)
# G0-5  mu0 的量纲
guard("G0-5", "[mu0] == M L Q^-2", DIM_MU0, dim(m=1, l=1, q=-2))
# G0-6  穿透深度 lambda_L = sqrt(m/(mu0 n e^2)) 是长度
_t = ddiv(DIM_MASS, dmul(DIM_MU0, dmul(DIM_DENSITY, dpow(dim(q=1), 2))))
guard("G0-6", "[lambda_L] == L（穿透深度公式量纲）", dpow(_t, Fraction(1, 2)), DIM_LENGTH)
# G0-7  相干长度 xi0 = hbar v_F / Delta 是长度
_t2 = ddiv(dmul(dim(m=1, l=2, t=-1), DIM_VEL), DIM_ENERGY)
guard("G0-7", "[xi_0] == L（相干长度公式量纲）", _t2, DIM_LENGTH)
# G0-8  dpow 取幂正确性（指数乘 2 再开方回到原量纲）
guard("G0-8", "dpow 幂运算自检", dpow(dpow(DIM_LENGTH, 2), Fraction(1, 2)), DIM_LENGTH)

# ============================================================
# 3. 条目系统与数值工具
# ============================================================
ENTRIES = []

def add(eid, grp, name, verdict, detail, key=None):
    ENTRIES.append({
        "id": eid, "group": grp, "name": name,
        "verdict": verdict, "detail": detail,
        "key": key or {}
    })

def fv(x, n=25):
    """定点科学计数（纪律：不用 quantize，>prec 会抛 InvalidOperation）"""
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        return str(x)

def fs(x, n=12):
    try:
        return format(Decimal(x), "." + str(n) + "f")
    except Exception:
        return str(x)

def reldev(a, b):
    """相对偏差 |a-b|/|b|"""
    b = Decimal(b)
    if b == 0:
        return None
    return abs((Decimal(a) - b) / b)

def ratio(a, b):
    b = Decimal(b)
    if b == 0:
        return None
    return Decimal(a) / b

# 高精度 exp（Decimal 自带 ln/exp）
def dexp(x):
    return Decimal(x).exp()

def dln(x):
    return Decimal(x).ln()

def dsqrt(x):
    return Decimal(x).sqrt()

# ============================================================
# A 组 · 电子螺旋几何：既有恒等式复算
# ============================================================
def group_a():
    # --- A01 三重奏恒等式 kappa^2 + tau^2 = (omega/c)^2 ---
    # 螺旋 r(t) = (R cos wt, R sin wt, b t)，约束 (Rw)^2 + b^2 = c^2
    # kappa = R w^2 / c^2 ,  tau = b w / c^2
    R = D("1e-13")
    W = D("1e21")
    Rw = R * W
    b2 = C * C - Rw * Rw
    b = dsqrt(b2)
    kappa = R * W * W / (C * C)
    tau = b * W / (C * C)
    lhs = kappa * kappa + tau * tau
    rhs = (W / C) * (W / C)
    res = reldev(lhs, rhs)
    add("A01", "A 螺旋几何", "三重奏恒等式 κ²+τ²=(ω/c)²（螺旋参数化数值核对）",
        "PASS" if res is not None and res < D("1e-30") else "FAIL",
        "取 R=%s m, ω=%s s⁻¹，由 (Rω)²+b²=c² 定 b=%s m/s ⇒ κ=%s m⁻¹, τ=%s m⁻¹；"
        "κ²+τ²=%s vs (ω/c)²=%s，相对残差 %s"
        % (fv(R, 6), fv(W, 6), fv(b, 12), fv(kappa, 12), fv(tau, 12),
           fv(lhs, 12), fv(rhs, 12), fv(res, 6)),
        {"kappa": str(kappa), "tau": str(tau), "residual": str(res)})

    # --- A02 电子约化康普顿波长 ---
    lam_bar = HBAR / (M_E * C)
    ref = D("3.8615926796e-13")
    dev = reldev(lam_bar, ref)
    add("A02", "A 螺旋几何", "电子约化康普顿波长 R_e = ħ/(m_e c)",
        "PASS" if dev < D("1e-8") else "FAIL",
        "ħ/(m_e c) = %s m，与 CODATA 约化康普顿波长 %s m 相对偏差 %s"
        % (fv(lam_bar), fv(ref), fv(dev)),
        {"R_e": str(lam_bar), "dev": str(dev)})

    # --- A03 康普顿角频率 ---
    # 纪律（r59 确立，本册自纠一次）：容差必须与【参照值的报价精度】同源。
    # 参照值 7.7634407e20 为 8 位有效数字 ⇒ 半位容差取 5e-8，
    # 不得用 1e-8 去卡 8 位报价（否则把参照值自身的截断误判为计算错误）。
    w_e = M_E * C * C / HBAR
    ref_w = D("7.7634407e20")        # 8 位有效数字
    tol_w = D("5e-8")                # 与 8 位报价同源的半位容差
    dev2 = reldev(w_e, ref_w)
    add("A03", "A 螺旋几何", "电子康普顿角频率 ω_e = m_e c²/ħ（容差按参照值 8 位报价取 5e−8）",
        "PASS" if dev2 < tol_w else "FAIL",
        "m_e c²/ħ = %s s⁻¹（ħω_e = m_e c² = %s J = %s MeV）；对应温度 ħω_e/k_B = %s K"
        % (fv(w_e), fv(M_E_C2), fv(M_E_C2 / EV / D("1e6"), 8), fv(T_E_ENERGY)),
        {"omega_e": str(w_e), "T_equiv": str(T_E_ENERGY)})

    # --- A04 恒等式零判别力（换任意以 c 运动的曲线，恒等式仍成立）---
    # 对照组：换一组完全不同量级的 (R, ω)，恒等式残差应同量级
    R2, W2 = D("1e-25"), D("1e29")
    Rw2 = R2 * W2
    b_2 = dsqrt(C * C - Rw2 * Rw2)
    k2 = R2 * W2 * W2 / (C * C)
    t2 = b_2 * W2 / (C * C)
    lhs2 = k2 * k2 + t2 * t2
    rhs2 = (W2 / C) * (W2 / C)
    res2 = reldev(lhs2, rhs2)
    add("A04", "A 螺旋几何", "零判别力：三重奏对 (R,ω) 取任意值恒成立 ⇒ 不区分物理构型",
        "INFO",
        "把 (R,ω) 从 (1e-13, 1e21) 换成 (1e-25, 1e29)（跨 12 个量级），"
        "κ、τ 各自变化巨大（κ=%s→%s, τ=%s→%s），但残差恒为 %s ⇒ "
        "该式是 Frenet–Serret 恒等式，任何以速率 c 的曲线自动满足，不承载物理内容"
        % (fv(kappa, 6), fv(k2, 6), fv(tau, 6), fv(t2, 6), fv(res2, 6)),
        {"res2": str(res2)})

    # --- A05 电子若 v_perp=c 则 tau=0 的边界 ---
    # R = R_e, w = w_e ⇒ Rw = c ⇒ b = 0 ⇒ tau = 0
    Rw_e = LAMBDA_C_BAR * OMEGA_E
    dev_boundary = reldev(Rw_e, C)
    b_e2 = C * C - Rw_e * Rw_e
    add("A05", "A 螺旋几何", "电子取康普顿半径+康普顿频率时 τ≡0（轴向速度必须为零）",
        "BOUNDARY",
        "R_e ω_e = %s vs c = %s（相对偏差 %s）⇒ 若电子横向速度就是 c，"
        "则轴向分量 b²=%s 必须为 0 ⇒ τ=0 ⇒ 螺旋退化为平面圆，挠率自由度消失。"
        "（与 S03-V18.5「平面圆 τ=0」同型）"
        % (fv(Rw_e), fv(C), fv(dev_boundary, 6), fv(b_e2, 6)),
        {"Rw_over_c": str(ratio(Rw_e, C))})

# ============================================================
# B 组 · BCS / Eliashberg 正确核（教科书核心公式，机器验证）
# ============================================================
def group_b():
    # 铝的标定：T_c = A (hbar*w_D/k_B) exp(-1/(N(0)V))，A 取两口径
    # hbar*w_D/k_B = theta_D
    theta_D = THETA_D_AL
    tc_obs = TC_AL
    # 反解 N(0)V
    lam_113 = D(1) / dln(D("1.13") * theta_D / tc_obs)
    lam_1134 = D(1) / dln(D("1.134") * theta_D / tc_obs)
    add("B01", "B 正确核", "BCS 弱耦合 T_c = A(ħω_D/k_B)exp[−1/(N(0)V)]，铝标定反解耦合常数",
        "PASS",
        "取 Al：θ_D=%s K、T_c=%s K。A=1.13 ⇒ N(0)V=%s；A=1.134（标准口径）⇒ N(0)V=%s。"
        "（CM3 脚本用 A=1.13，教科书常写 1.134，两口径登记不合并）"
        % (fs(theta_D, 2), fs(tc_obs, 3), fv(lam_113), fv(lam_1134)),
        {"N0V_A113": str(lam_113), "N0V_A1134": str(lam_1134)})

    # B02 能隙比
    r_gap = D("3.528")            # 2Δ(0)/k_B T_c 精确弱耦合值
    delta_al = r_gap / 2 * K_B * TC_AL
    add("B02", "B 正确核", "弱耦合普适比 2Δ(0)/(k_B T_c) = 3.528",
        "PASS",
        "弱耦合 BCS 给出 2Δ(0)=3.528 k_BT_c。对 Al（T_c=1.2 K）⇒ Δ(0)=%s J = %s μeV；"
        "与实测 Al 能隙 ~0.18 meV 同量级" % (fv(delta_al), fv(delta_al / EV / D("1e-6"), 6)),
        {"delta_Al_J": str(delta_al)})

    # B03 相干长度
    v_F = D("2.03e6")             # Al 费米速度 m/s（自由电子气值，[E] 外部输入）
    xi0 = HBAR * v_F / (PI * delta_al)
    add("B03", "B 正确核", "相干长度 ξ₀ = ħv_F/(πΔ(0))",
        "PASS",
        "Al：v_F=%s m/s ⇒ ξ₀ = %s m = %s nm（文献 Al ξ₀≈1600 nm，"
        "差来自 v_F 取值与纯度，量级一致）"
        % (fv(v_F, 6), fv(xi0), fv(xi0 * D("1e9"), 6)),
        {"xi0_m": str(xi0)})

    # B04 穿透深度
    # Al：密度 2700 kg/m^3，摩尔质量 26.9815 g/mol，价电子 3
    rho_al = D("2700")
    M_mol_al = D("26.9815e-3")
    n_s = rho_al / M_mol_al * N_A * D(3)
    lam_L = dsqrt(M_E / (MU0 * n_s * E_CH * E_CH))
    add("B04", "B 正确核", "伦敦穿透深度 λ_L = √(m_e/(μ₀ n_s e²))",
        "PASS",
        "Al：n_s=%s m⁻³ ⇒ λ_L = %s m = %s nm（文献 Al λ_L≈16 nm，量级一致）；"
        "GL 参数 κ_GL=λ_L/ξ₀ = %s < 1/√2 ⇒ Al 为 I 型超导体"
        % (fv(n_s, 8), fv(lam_L), fv(lam_L * D("1e9"), 6), fv(ratio(lam_L, xi0), 6)),
        {"lambda_L_m": str(lam_L), "n_s": str(n_s)})

    # B05 磁通量子
    dev_phi = reldev(PHI0, D("2.067833848e-15"))
    add("B05", "B 正确核", "磁通量子 Φ₀ = h/(2e)（库珀对电荷 2e 的标志）",
        "PASS" if dev_phi < D("1e-8") else "FAIL",
        "h/(2e) = %s Wb，与 CODATA %s Wb 相对偏差 %s。"
        "该量是配对电荷为 2e 的直接实验判据（非零温超导的硬证据之一）"
        % (fv(PHI0), fv(D("2.067833848e-15")), fv(dev_phi, 6)),
        {"Phi0": str(PHI0)})

    # B06 同位素效应
    # T_c ∝ M^-alpha，BCS 下 alpha = 1/2（因 omega_D ∝ M^-1/2）
    # 数值演示：M 变为 2 倍
    tc_scaled = TC_AL / dsqrt(D(2))
    add("B06", "B 正确核", "同位素效应指数 α = 1/2（BCS 声子机制特征）",
        "PASS",
        "ω_D ∝ M^(−1/2) ⇒ T_c ∝ M^(−1/2)。若 M→2M，Al 的 T_c 由 %s K 降为 %s K"
        "（比值 %s = 1/√2）。实测：Hg 同位素 α≈0.5；非常规超导体 α 显著偏离 0.5"
        % (fs(TC_AL, 3), fv(tc_scaled, 8), fv(D(1) / dsqrt(D(2)), 8)),
        {"alpha_BCS": "0.5"})

    # B07 McMillan / Allen-Dynes 强耦合
    # T_c = (hbar*w_log/1.2k_B) exp[-1.04(1+lam)/(lam - mu*(1+0.62 lam))]
    def mcmillan(w_log_K, lam, mu_star=D("0.1")):
        # w_log_K 以 K 为单位传入（= hbar*w_log/k_B）
        expo = -D("1.04") * (1 + lam) / (lam - mu_star * (1 + D("0.62") * lam))
        return (w_log_K / D("1.2")) * dexp(expo), expo

    # 用 H3S 反解：T_c=203K, w_log 典型 ~ 1000-1400 K（[E]）
    w_log_H3S = D("1200")   # K（外部输入，电声谱对数值）
    tc_calc, expo_calc = mcmillan(w_log_H3S, D("2.0"))
    add("B07", "B 正确核", "McMillan–Allen–Dynes 强耦合公式 λ=2 数值核对（H₃S 口径）",
        "PASS",
        "T_c=(ħω_log/1.2k_B)exp[−1.04(1+λ)/(λ−μ*(1+0.62λ))]。取 ω_log/k_B=%s K、λ=2.0、μ*=0.1"
        " ⇒ 指数 %s，T_c=%s K（与 H₃S 实测 203 K 同量级，λ 为可调输入）"
        % (fs(w_log_H3S, 1), fv(expo_calc, 8), fv(tc_calc, 8)),
        {"tc_H3S_calc": str(tc_calc), "exponent": str(expo_calc)})

    # B08 强耦合极限：lambda -> infinity
    tc_big, expo_big = mcmillan(w_log_H3S, D("1000"))
    limit_factor = dexp(-D("1.04") / (1 - D("0.1") * D("0.62")))
    add("B08", "B 正确核", "强耦合极限 λ→∞：T_c 仍被声子频率封顶（McMillan 极限）",
        "PASS",
        "λ=1000 时 T_c=%s K，而 λ=2 时为 %s K ⇒ 增大 λ 的收益迅速饱和："
        "极限因子 exp[−1.04/(1−0.62μ*)]=%s ⇒ T_c^max ≈ (ħω_log/1.2k_B)×%s。"
        "即：耦合再强也不能突破声子（配对胶）频率量级"
        % (fv(tc_big, 8), fv(tc_calc, 8), fv(limit_factor, 8), fv(limit_factor, 8)),
        {"limit_factor": str(limit_factor)})

# ============================================================
# C 组 · ★攻破核心：螺旋几何量能否充当配对胶 / 给出 T_c
# ============================================================
def group_c():
    # 复用 B 组 Al 标定出的耦合常数（保持耦合不变，只替换频率）
    n0v = D(1) / dln(D("1.13") * THETA_D_AL / TC_AL)

    # --- C01 把电子康普顿频率当作 BCS 的特征频率 ---
    tc_helix = D("1.13") * T_E_ENERGY * dexp(-D(1) / n0v)
    dev_c01 = ratio(tc_helix, TC_AL)
    add("C01", "C 攻破核心", "★把螺旋内禀频率 ω_e=m_ec²/ħ 代入 BCS ⇒ T_c 预测 1.66e7 K",
        "FAIL",
        "保持 Al 标定出的耦合常数 N(0)V=%s 不变，只把特征频率由德拜频率（ħω_D/k_B=θ_D=%s K）"
        "换成螺旋内禀频率（ħω_e/k_B=m_ec²/k_B=%s K）⇒ T_c=%s K。"
        "实测 Al 为 %s K ⇒ **高估 %s 倍**。该错误对所有材料同向（因 ω_e 与材料无关），"
        "意味着按此读法「一切物质都应是亿开尔文级超导体」，与现实矛盾"
        % (fv(n0v), fs(THETA_D_AL, 1), fv(T_E_ENERGY), fv(tc_helix),
           fs(TC_AL, 3), fv(dev_c01, 8)),
        {"Tc_helix_K": str(tc_helix), "overestimate": str(dev_c01)})

    # --- C02 量纲齐次性审计：该代入量纲合法，但物理角色错配 ---
    dim_tc_from = ddiv(dmul(dim(m=1, l=2, t=-1), DIM_FREQ), dim())   # 能量量纲（温度经 k_B 折算）
    add("C02", "C 攻破核心", "量纲审计：C01 的代入【量纲完全齐次】，故量纲检查抓不住它",
        "FAIL",
        "[ħω_e/k_B] = 能量量纲（温度经 k_B 折算）⇒ T_c 式量纲 100% 齐次，"
        "量纲门禁对 C01 **零判别力**。错的是物理角色：BCS 中的 ω 是【配对胶（声子）的截止频率】，"
        "不是【被配对电子的内禀频率】。⇒ 本库「量纲自洽 ≠ 成立」的又一教科书反例"
        "（与归一化方程 23「量纲 100% 自洽但等价于 hν=Mc²」同型）",
        {"dim_ok": True, "physical_role": "MISMATCH"})

    # --- C03 挠率能否充当配对胶：继承 τ 的代数 slave 判定 ---
    add("C03", "C 攻破核心", "挠率 τ 不能充当配对胶（不传播 ⇒ 不传递相互作用）",
        "FAIL",
        "继承 r19/r20/r21/r27 四册独立裁定：对作用量变分 ⇒ 对 τ 变分给 τ=−cR/(2α)"
        "（代数 slave），L_tau 第二项因 g_μνu^μu^ν≡−1 退化为常数 ⇒ 无 (∇τ)² ⇒ **τ 不传播**。"
        "不传播的场不能作为相互作用媒介：配对相互作用需要交换一个【传播】的玻色子"
        "（声子/自旋涨落）。⇒ 螺旋几何在框架内不提供任何配对胶",
        {"inherits": "r19/r20/r21/r27"})

    # --- C04 尺度困境 ---
    lam_C = LAMBDA_C
    v_F = D("2.03e6")
    delta_al = D("3.528") / 2 * K_B * TC_AL
    xi0 = HBAR * v_F / (PI * delta_al)
    span1 = ratio(xi0, lam_C)
    span2 = ratio(D("1e-3"), lam_C)
    add("C04", "C 攻破核心", "尺度困境：电子螺旋尺度与超导相干尺度跨 6 个量级",
        "FAIL",
        "电子康普顿波长 λ_C=%s m；超导相干长度 ξ₀(Al)=%s m；宏观样品 ~1e−3 m。"
        "λ_C→ξ₀ 跨 %s 倍，λ_C→宏观跨 %s 倍。螺旋几何的【唯一内禀尺度】是 λ_C（普朗克/康普顿级），"
        "而超导的相干长度由 ħv_F/Δ 决定 —— 后者不出现在螺旋几何的任何量中"
        "⇒ 与 D2 册「尺度困境定理」（26 量级）同型复发"
        % (fv(lam_C), fv(xi0), fv(span1, 8), fv(span2, 8)),
        {"span_xi0": str(span1), "span_macro": str(span2)})

    # --- C05 反解：BCS 机制下 300 K 需要多高的配对胶频率 ---
    tc_target = ROOM_T
    omega_needed = tc_target / (D("1.13") * dexp(-D(1) / n0v))
    # 已知最高德拜温度：金刚石 ~2230 K
    theta_D_max = D("2230")
    add("C05", "C 攻破核心", "反解：BCS 机制达 300 K 需配对胶特征温度 ~1.07e5 K",
        "PASS",
        "设 T_c=%s K、保持 N(0)V=%s ⇒ 需 ħω/k_B = %s K。"
        "对比已知最高德拜温度（金刚石 %s K，差 %s 倍）、H₃S 的 ω_log≈1200 K"
        "（差 %s 倍）。⇒ 常温超导在【电声子 BCS 机制】内的硬门槛是配对胶频率，"
        "这正是高压氢化物路线选择【最轻元素氢】的物理原因（ω∝M^(−1/2)）"
        % (fs(tc_target, 1), fv(n0v), fv(omega_needed), fs(theta_D_max, 1),
           fv(ratio(omega_needed, theta_D_max), 8), fv(ratio(omega_needed, D("1200")), 8)),
        {"omega_needed_K": str(omega_needed)})

    # --- C06 若把耦合常数也放自由：不可证伪（复发模式）---
    n0v_for_300 = D(1) / dln(D("1.13") * T_E_ENERGY / ROOM_T)
    add("C06", "C 攻破核心", "★若把 N(0)V 也放自由 ⇒ 任何 T_c 都能拟合（不可证伪）",
        "FAIL",
        "在 ω_e 固定下反解：要 T_c=%s K 只需 N(0)V=%s（对比 Al 标定值 %s，仅差 %s 倍）。"
        "⇒ 「螺旋频率 + 自由耦合」这一组合对 T_c **零判别力**："
        "任何观测到的 T_c（含 0 K 与 1e7 K）都能被某个 N(0)V 拟合。"
        "本库「固定则被排除、自由则不可证伪」模式第 4 次复发（前三次：r95 的 k_B / ω(r) / (α,β,η)）"
        % (fs(ROOM_T, 1), fv(n0v_for_300), fv(n0v), fv(ratio(n0v, n0v_for_300), 8)),
        {"N0V_for_300K": str(n0v_for_300), "recurrence": "第4次"})

# ============================================================
# D 组 · 常温超导硬约束定价（外部事实 + 反解）
# ============================================================
def group_d():
    add("D01", "D 硬约束", "实测 T_c 纪录盘点（全部为 [E] 外部输入，非框架导出）",
        "PASS",
        "常压最高：HgBa₂Ca₂Cu₃O₈₊δ %s K（高压 ~30 GPa 下 %s K）；"
        "高压氢化物：H₃S %s K @155 GPa、LaH₁₀ %s K @170 GPa。"
        "常压常温（%s K）**尚未实现**"
        % (fs(TC_HGBCO, 1), fs(TC_HGBCO_HP, 1), fs(TC_H3S, 1), fs(TC_LAH10, 1), fs(ROOM_T, 1)),
        {"records": {"HgBCO_ap": str(TC_HGBCO), "H3S": str(TC_H3S), "LaH10": str(TC_LAH10)}})

    g1 = ratio(ROOM_T, TC_HGBCO)
    g2 = ratio(ROOM_T, TC_LAH10)
    g3 = ratio(ROOM_T, TC_HGBCO_HP)
    add("D02", "D 硬约束", "常温缺口定价：相对常压最高 2.22 倍，相对高压纪录仅 1.20 倍",
        "PASS",
        "300 K 相对：常压最高 %s K ⇒ %s 倍；高压 LaH₁₀ %s K ⇒ %s 倍；"
        "HgBCO 高压 %s K ⇒ %s 倍。⇒ 缺口本身【不大】（1.2~2.2 倍），"
        "真正困难在于【常压】：LaH₁₀ 的 %s K 需 170 GPa（≈1.7×10⁶ atm），泄压即失超"
        % (fs(TC_HGBCO, 1), fv(g1, 8), fs(TC_LAH10, 1), fv(g2, 8),
           fs(TC_HGBCO_HP, 1), fv(g3, 8), fs(TC_LAH10, 1)),
        {"gap_ap": str(g1), "gap_hp": str(g2)})

    # 氢的最轻元素优势：omega ∝ M^(-1/2)
    # 用 H(1) vs 典型金属(如 Pb 207) 的频率比
    m_h, m_pb = D("1.008"), D("207.2")
    freq_ratio = dsqrt(m_pb / m_h)
    add("D03", "D 硬约束", "为何选氢：ω∝M^(−1/2) ⇒ 氢相对铅的声子频率优势",
        "PASS",
        "配对胶频率 ω∝M^(−1/2)。以 H（%s u）对比 Pb（%s u）⇒ 频率比 %s 倍。"
        "这就是高压氢化物（H₃S/LaH₁₀）能把 T_c 推到 200~250 K 的唯一机制来源 —— "
        "该机制是【标准电声子物理】，与螺旋几何无关"
        % (fv(m_h, 6), fv(m_pb, 6), fv(freq_ratio, 8)),
        {"freq_ratio": str(freq_ratio)})

    add("D04", "D 硬约束", "常压常温的真正阻塞：不是机制，而是【结构稳定性】",
        "BOUNDARY",
        "已知达到 200 K 以上的材料全部依赖【高压维持亚稳相】（H₃S@155 GPa、LaH₁₀@170 GPa）。"
        "常压下这些相不存在 ⇒ 阻塞点是【常压下的晶体结构/亚稳相合成】，"
        "属材料化学与高压物理问题，不是统一场论问题。⇒ 登记为框架外开放项",
        {"open_item": "O-RT-SC-AMBIENT"})

# ============================================================
# E 组 · 最小增广定价
# ============================================================
def group_e():
    add("E01", "E 最小增广", "M1 给一个传播的配对胶场：代价 = +1 玻色场 +1 耦合常数 +1 截断",
        "FAIL",
        "要使螺旋几何产生超导，最小增广是引入一个【传播】的配对胶（声子或自旋涨落）。"
        "但声子/自旋涨落是【晶格与电子关联】的产物，不由电子内禀螺旋决定 ⇒ M1 实质是引入标准物理，"
        "不是从螺旋几何导出。代价：+1 场、+1 耦合常数、+1 频率截断 ⇒ 撞 C3（零自由参数）",
        {"cost": "+3 inputs", "violates": "C3"})

    add("E02", "E 最小增广", "M2 给一个长度尺度（连接 λ_C 与 ξ₀）：代价 = +1 外部输入",
        "FAIL",
        "C04 表明螺旋几何只有 λ_C 一个内禀尺度，而 ξ₀=ħv_F/Δ 不由它决定。"
        "补一个长度尺度可弥合，但该尺度必须是具体材料的（v_F、n_s、Δ 都是材料参数）"
        "⇒ M2 = 引入材料参数，等于放弃「第一性导出」",
        {"cost": "+1 input", "violates": "C2"})

    add("E03", "E 最小增广", "任一增广后：框架的可检验增量仍为 0（撞 C5/C6）",
        "FAIL",
        "施加 M1 或 M2 后，所得 T_c 公式即标准 BCS/McMillan 式（B07/B08 已验证），"
        "螺旋几何不贡献任何项。⇒ 与 T067 既有登记一致：高温超导机理【非统一场论载体】，"
        "撞 C5（可检验）与 C6（误差带）：框架既不给出新数值，也不给出误差带",
        {"consistent_with": "T067"})

# ============================================================
# F 组 · 判别性实验判据
# ============================================================
def group_f():
    # F01 四重确认
    add("F01", "F 实验判据", "超导四重确认标准（缺一不可，防假阳性）",
        "PASS",
        "① 零电阻：四引线法，ρ < 仪器下限（通常 <1e−8 Ω·cm），且【电流反向/变电流不变】；"
        "② 迈斯纳效应：ZFC 与 FC 曲线分离（χ_ZFC ≈ −1，4πχ 满抗磁），排除石墨/热释电等普通抗磁；"
        "③ 比热跳变：ΔC/(γT_c) = 1.43（BCS 弱耦合），证明是【体相】相变而非表面/丝状通路；"
        "④ 磁通量子化或约瑟夫森效应：证明配对电荷为 2e（Φ₀=h/2e）",
        {"four_tests": ["零电阻", "迈斯纳", "比热跳变", "磁通量子化"]})

    # F02 与材料无关的判别（本册最有用的实验判据）
    tc_min, tc_max = TC_AL, TC_LAH10
    spread = ratio(tc_max, tc_min)
    add("F02", "F 实验判据", "★判别性判据：T_c 是否为【电子内禀频率】的函数（与材料无关）",
        "FAIL",
        "若螺旋纲领成立（T_c 由电子内禀螺旋频率 ω_e 决定），因所有材料的 m_e 相同 ⇒ ω_e 相同"
        " ⇒ 所有超导体的 T_c 应【相同】。实测：Al %s K → LaH₁₀ %s K，跨 %s 倍。"
        "⇒ 该判据【一次性否证】「T_c 由电子内禀频率主导」这一支，且不需要新实验，"
        "用既有 T_c 数据库即可执行"
        % (fs(tc_min, 2), fs(tc_max, 1), fv(spread, 8)),
        {"Tc_spread": str(spread), "verdict": "否证"})

    # F03 假阳性陷阱
    add("F03", "F 实验判据", "假阳性陷阱清单（LK-99 类事件的机器可检特征）",
        "INFO",
        "① 电阻骤降但【非零剩余电阻】⇒ 金属-绝缘体转变或渗流，非超导；"
        "② 仅 FC 抗磁、ZFC 不分离 ⇒ 普通抗磁/铁磁杂质；"
        "③ 无比热跳变 ⇒ 丝状/表面超导（体积分数 <1%）；"
        "④ 磁悬浮视频不能作为证据（抗磁体、热解石墨均可悬浮）；"
        "⑤ 单样品、不可复现、无原始数据反例 ⇒ 不构成证据。LK-99（2023）即同时命中 ①②③⑤",
        {"traps": 5})

# ============================================================
# 主程序
# ============================================================
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    g_bad = [g for g in GUARDS if not g["ok"]]
    if g_bad:
        print("[FATAL] 量纲工具自检未通过，禁止继续判定：")
        for g in g_bad:
            print("   %s %s: got=%s want=%s" % (g["id"], g["name"], g["got"], g["want"]))
        sys.exit(2)
    print("[OK] 量纲工具自检 %d/%d 通过\n" % (len(GUARDS), len(GUARDS)))

    group_a()
    group_b()
    group_c()
    group_d()
    group_e()
    group_f()

    # 统计
    order = ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"]
    cnt = {k: 0 for k in order}
    for e in ENTRIES:
        cnt[e["verdict"]] = cnt.get(e["verdict"], 0) + 1

    print("=" * 78)
    print("  r143 · 常温超导 · 求导证明验证精算与攻破")
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

    # 落盘
    here = os.path.dirname(os.path.abspath(__file__))
    base = os.path.dirname(here)
    data_dir = os.path.join(base, "数据")
    os.makedirs(data_dir, exist_ok=True)
    stem = "TUFT-r143_常温超导_求导证明验证精算_2026-10-21"

    def jdump(o):
        def conv(x):
            if isinstance(x, Decimal):
                return str(x)
            if isinstance(x, Fraction):
                return str(x)
            raise TypeError(str(type(x)))
        return json.dumps(o, ensure_ascii=False, indent=2, default=conv)

    payload = {
        "id": "r143",
        "title": "常温超导 · 求导证明验证精算与攻破",
        "date": "2026-10-21",
        "guards": GUARDS,
        "entries": ENTRIES,
        "counts": cnt,
        "key_numbers": {
            "omega_e_s^-1": str(OMEGA_E),
            "lambda_C_m": str(LAMBDA_C),
            "mec2_over_kB_K": str(T_E_ENERGY),
            "Phi0_Wb": str(PHI0),
            "Tc_helix_prediction_K": str(D("1.13") * T_E_ENERGY
                                       * dexp(-D(1) / (D(1) / dln(D("1.13") * THETA_D_AL / TC_AL)))),
        },
    }
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        f.write(jdump(payload))

    with open(os.path.join(data_dir, stem + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("r143 常温超导 报告\n")
        f.write("PASS=%d FAIL=%d BOUNDARY=%d INFO=%d CORRECTED=%d MISMATCH=%d\n"
                % (cnt["PASS"], cnt["FAIL"], cnt["BOUNDARY"], cnt["INFO"],
                   cnt["CORRECTED"], cnt["MISMATCH"]))
        f.write("guard=%d/%d\n" % (len(GUARDS), len(GUARDS)))
        for e in ENTRIES:
            f.write("[%s] %s %s\n" % (e["verdict"], e["id"], e["name"]))

    # md
    lines = ["# r143 · 常温超导 · 求导证明验证精算（数据产物）", "",
             "条目 %d ｜ " % len(ENTRIES)
             + " ｜ ".join("%s=%d" % (k, cnt[k]) for k in order if cnt[k]), "",
             "## 条目", "",
             "| ID | 组 | 名称 | 判定 | 机器读数 |", "|---|---|---|---|---|"]
    for e in ENTRIES:
        d = e["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append("| %s | %s | %s | **%s** | %s |"
                     % (e["id"], e["group"], e["name"], e["verdict"], d))
    lines += ["", "## 守卫", "",
              "| ID | 名称 | 得 | 期望 | 通过 |", "|---|---|---|---|---|"]
    for g in GUARDS:
        lines.append("| %s | %s | %s | %s | %s |"
                     % (g["id"], g["name"], g["got"], g["want"], "✅" if g["ok"] else "❌"))
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n[产物] %s" % os.path.join(data_dir, stem + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
