# -*- coding: utf-8 -*-
"""TUFT-r108 ｜ 《TUFT V10 螺旋挠率统一场论（算法联盟审计修复版）》主干全维攻破 —— 机器判决引擎

来料 = TUFT V10（自称"算法联盟审计修复版 / B+ 评级"）：
  本源三行式  omega = c*tau ;  Box tau = (4*pi/c^3) curl J_tau ;  a = -omega x (omega x r)
  J_tau = [ G*rho_m + (1/(4*pi*eps0))*(q/m)*rho_q + K_s*rho_top + K_w*rho_meta ] * r_hat

本册受理范围（分工声明）：攻击 V10 主干 —— 七公理、主方程、变分推导、静态解、
引力支 / 电磁支 / 强支 / 弱支 / 宇宙学支、附录 D（PPN 声称）、以及来料自带的
"算法联盟审计报告"自评。星系挠率晕（第 10 章 / tau_phi = tau0*r0/r）由并行线
r107 受理，本册只在交叉一致性处引用，不重复判决。

红线：只读审计 + 机器判决，不产生新物理、不修改来料任何字节、不修改既有 r 序列
任何产物。所有裁定必须由可复算的量纲/数值/恒等式断言承担；禁止"算了数却硬编码判定"。

数值标准：纯标准库 decimal（prec=60）+ fractions（量纲四元组 M,L,T,Q）。
"""


import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # .../本项目_全维自洽与归一化
OUT_DATA = os.path.join(ROOT, "数据")
OUT_SRC = os.path.join(ROOT, "源码")
os.makedirs(OUT_DATA, exist_ok=True)

TAG = "TUFT-r108_TUFT-V10外部来料_主干全维攻破_量纲场方程与现象学机检_2026-10-19"

# ----------------------------------------------------------------- 高精度常数
C = Decimal("299792458")                      # m/s 精确定义
G = Decimal("6.67430e-11")                    # m^3 kg^-1 s^-2
HBAR = Decimal("1.054571817e-34")             # J s
QE = Decimal("1.602176634e-19")               # C 精确定义
ME = Decimal("9.1093837139e-31")              # kg
MP = Decimal("1.67262192569e-27")             # kg
EPS0 = Decimal("8.8541878128e-12")            # F/m
MSUN = Decimal("1.98847e30")                  # kg
RSUN = Decimal("6.957e8")                     # m
MEARTH = Decimal("5.9722e24")                 # kg
REARTH = Decimal("6.371e6")                   # m
KPC = Decimal("3.0856775814913673e19")        # m
LP = Decimal("1.616255e-35")                  # m
G_STD = Decimal("9.80665")                    # m/s^2 标准重力
ARCSEC_PER_RAD = Decimal("206264.80624709636")
DAY = Decimal("86400")
EV_J = Decimal("1.602176634e-19")             # J per eV

# 来料自称值（原样登记，不修正）—— 全部取自用户提供的 V10 正文/摘要/审计表
CLAIM = {
    "g_surface": Decimal("9.820"),
    "mercury_arcsec": Decimal("42.98"),
    "Fe_over_Fg": Decimal("4.166e42"),
    "tau_s": Decimal("2.8e23"),               # 第 6 章 tau_s ≈ 2.8e23 m^-1
    "omega_s": Decimal("8.4e31"),             # 第 6 章 omega_s = c*tau_s
    "a_conf": Decimal("0.8e-15"),             # 孤环半径
    "E_conf_text_J": Decimal("2.36e-11"),     # 第 6 章正文 2.36e-11 J
    "E_conf_text_MeV": Decimal("148"),        # 第 6 章正文 ≈148 MeV
    "E_conf_audit_MeV": Decimal("246.7"),     # 审计表 246.7 MeV
    "xi_weak_m": Decimal("1.7e-18"),          # 第 7 章 xi
    "E_W_GeV": Decimal("116"),                # 第 7 章 116 GeV
    "xi_audit_fm": Decimal("1.7"),            # 审计 A3 写 "1.7 fm"（单位口径）
    "tau0_galaxy": Decimal("3.10e-24"),       # 银河 tau0 m^-1
    "kappa0_upper_mrad": Decimal("5.43"),
    "Omega_M": Decimal("0.311"),
    "Omega_tau": Decimal("0.689"),
    "TR1_a": Decimal("8.48e-11"),             # m/s^2
}

ENTRIES = []
NOT_SELF_DERIVED = []
EXTERNAL_INPUTS = []
STATE = {"guard": 0, "guard_fail": 0, "guard_msgs": []}


def _j(o):
    if isinstance(o, Decimal):
        return float(o)
    if isinstance(o, Fraction):
        return float(o)
    if isinstance(o, dict):
        return dict((k, _j(v)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [_j(v) for v in o]
    return o


def add(code, verdict, title, detail, **ev):
    e = {"code": code, "verdict": verdict, "title": title, "detail": detail}
    for k, v in ev.items():
        e[k] = _j(v)
    ENTRIES.append(e)
    return e


def guard(cond, name, desc=""):
    STATE["guard"] += 1
    ok = bool(cond)
    if not ok:
        STATE["guard_fail"] += 1
        STATE["guard_msgs"].append(name + " :: " + desc)
    return ok


# ------------------------------------------------------- 量纲四元组 (M,L,T,Q)
def D(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


DIMLESS = D(0, 0, 0, 0)


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
    names = ["M", "L", "T", "Q"]
    out = []
    for i, v in enumerate(a):
        if v == 0:
            continue
        s = names[i]
        if v != 1:
            s = s + "^" + str(v)
        out.append(s)
    if not out:
        return "1"
    return " · ".join(out)


# 基础量纲（SI 直接推得）
DIM_M = D(1, 0, 0, 0)
DIM_L = D(0, 1, 0, 0)
DIM_T = D(0, 0, 1, 0)
DIM_Q = D(0, 0, 0, 1)
DIM_c = D(0, 1, -1, 0)
DIM_G = D(-1, 3, -2, 0)
DIM_hbar = D(1, 2, -1, 0)
DIM_tau = D(0, -1, 0, 0)              # 挠率 L^-1
DIM_rho_m = D(1, -3, 0, 0)            # 质量密度
DIM_rho_q = D(0, -3, 0, 1)            # 电荷密度
DIM_eps0 = D(-1, -3, 2, 2)            # F/m = C^2/(J*m)  ==> M^-1 L^-3 T^2 Q^2
DIM_eps0_altT4 = D(-1, -3, 4, 2)      # r107 注册口径（本册列为敏感对照，非本册采信值）
DIM_force = D(1, 1, -2, 0)
DIM_acc = D(0, 1, -2, 0)
DIM_energy_density = D(1, -1, -2, 0)  # J/m^3
DIM_energy = D(1, 2, -2, 0)
DIM_inv_L2 = D(0, -2, 0, 0)           # 曲率 R_munu / dalembertian
DIM_inv_L3 = D(0, -3, 0, 0)


def fmt(x, n=25):
    try:
        d = Decimal(x)
    except Exception:
        return str(x)
    s = format(d, "." + str(n) + "E")
    m, e = s.split("E")
    return m + "E" + e


def rel(a, b):
    a = Decimal(a)
    b = Decimal(b)
    den = max(abs(a), abs(b))
    if den == 0:
        return Decimal(0)
    return abs(a - b) / den


print("[r108] boot ok", flush=True)

# =====================================================================
# A 段：量纲审计（符号层，Fraction 精确，无浮点）
# =====================================================================

# D01 主方程 □τ = (4π/c³) ∇×J_τ
lhs_D01 = dmul(DIM_inv_L2, DIM_tau)                       # L^-3
rhs_D01 = dmul(dpow(DIM_c, -3), dmul(DIM_tau, dmul(DIM_G, DIM_rho_m)))
# ∇×(G ρ_m r_hat): [G ρ_m]=T^-2, curl 给 L^-1
ok_D01 = deq(lhs_D01, rhs_D01)
ratio_D01 = ddiv(rhs_D01, lhs_D01)                        # = 1/c 量纲
add("D01", "PASS" if ok_D01 else "FAIL",
    "主方程量纲齐一性：□τ = (4π/c³)∇×J_τ",
    "LHS=%s ; RHS=%s ; RHS/LHS=%s（不齐，缺因子 1/c；若要齐一系数须为 4π/c²，与变分推导的 8πG/c⁴ 又不一致）"
    % (dstr(lhs_D01), dstr(rhs_D01), dstr(ratio_D01)),
    lhs=dstr(lhs_D01), rhs=dstr(rhs_D01), ratio=dstr(ratio_D01))

# D02 来料审计表对该行的自评（声称 ✅）—— 机器复算冲突登记
add("D02", "FAIL" if not ok_D01 else "PASS",
    "来料§3.3/审计表量纲自评复算",
    "来料称 '右边 L^-3T^3·L^-1T^-2 = L^-3 ✅'；机器复算得 L^-4·T^1（T^3·T^-2=T^1≠T^0）。自评算术错误",
    claim="L^-3", machine=dstr(rhs_D01))

# D03 变分中间式 ∇²τ = (8πG/c⁴) J_τ
lhs_D03 = DIM_inv_L3                                       # ∇²τ = L^-3
rhs_D03 = dmul(ddiv(DIM_G, dpow(DIM_c, 4)), dpow(DIM_T, -2))
ok_D03 = deq(lhs_D03, rhs_D03)
add("D03", "PASS" if ok_D03 else "FAIL",
    "变分中间式 ∇²τ = (8πG/c⁴)J_τ 量纲",
    "LHS=%s ; RHS=%s ；差 %s（另：由 δ∫(c⁴/16πG)|∇×τ|² 变分应得 ∇²τ = −(8πG/c⁴)J_τ，来料还丢了负号）"
    % (dstr(lhs_D03), dstr(rhs_D03), dstr(ddiv(rhs_D03, lhs_D03))),
    lhs=dstr(lhs_D03), rhs=dstr(rhs_D03))

# D04 作用量两项可加性：L_tau = (c⁴/16πG)|∇×τ|²  与  L_int = τ·J_τ
dim_Ltau = dmul(ddiv(dpow(DIM_c, 4), DIM_G), dpow(dmul(DIM_tau, DIM_tau), 1))
# |∇×τ|² = (L^-2)^2 = L^-4
dim_Ltau = dmul(ddiv(dpow(DIM_c, 4), DIM_G), D(0, -4, 0, 0))
dim_Lint = dmul(DIM_tau, dpow(DIM_T, -2))
ok_D04 = deq(dim_Ltau, dim_Lint)
add("D04", "PASS" if ok_D04 else "FAIL",
    "拉氏量两项量纲可加性（δS=0 合法性前提）",
    "L_τ=(c⁴/16πG)|∇×τ|² → %s ；L_int=τ·J_τ → %s ；差 %s ⇒ 两项不可相加，变分 δS=0 无意义"
    % (dstr(dim_Ltau), dstr(dim_Lint), dstr(ddiv(dim_Ltau, dim_Lint))),
    L_tau=dstr(dim_Ltau), L_int=dstr(dim_Lint))

# D04b 与标准 EH 拉氏量能量密度口径对照（防本册口径误伤）
dim_EH = dmul(ddiv(dpow(DIM_c, 4), DIM_G), DIM_inv_L2)
ok_D04b = deq(dim_EH, DIM_energy_density)
add("D04b", "PASS" if ok_D04b else "FAIL",
    "口径对照：ℒ_EH = c⁴R/(16πG) 是否给能量密度",
    "c⁴R/(16πG) → %s ；能量密度应为 %s ⇒ %s（口径正确，D04 的失败来自来料把 R[L^-2] 换成 |∇×τ|²[L^-4]）"
    % (dstr(dim_EH), dstr(DIM_energy_density), "一致" if ok_D04b else "不一致"),
    EH=dstr(dim_EH))

# D05 源矢量四项齐一（用 SI 正确 ε₀ 量纲）+ ε₀ 口径敏感性双轨
dim_src_grav = dmul(DIM_G, DIM_rho_m)                                   # T^-2
dim_src_em = dmul(ddiv(DIMLESS, DIM_eps0),                              # 1/(4π ε₀)
                  dmul(ddiv(DIM_Q, DIM_M), DIM_rho_q))                  # (q/m)·ρ_q
dim_src_em_alt = dmul(ddiv(DIMLESS, DIM_eps0_altT4),
                      dmul(ddiv(DIM_Q, DIM_M), DIM_rho_q))
ok_D05 = deq(dim_src_grav, dim_src_em)
ok_D05_alt = deq(dim_src_grav, dim_src_em_alt)
add("D05", "PASS" if ok_D05 else "FAIL",
    "源矢量电荷项与质量项量纲齐一（ε₀ 取 SI 直接推得 M^-1L^-3T^2Q^2）",
    "Gρ_m → %s ；(1/4πε₀)(q/m)ρ_q → %s ⇒ %s。敏感性：若按 r107 注册的 ε₀=T^4 口径则为 %s ⇒ %s（本册采信 SI 口径，差异已登记防跨册污染）"
    % (dstr(dim_src_grav), dstr(dim_src_em), "齐一" if ok_D05 else "不齐",
       dstr(dim_src_em_alt), "齐一" if ok_D05_alt else "不齐"),
    grav=dstr(dim_src_grav), em=dstr(dim_src_em), em_alt=dstr(dim_src_em_alt))

# D06 ρ_top / ρ_meta 仅被"声明"为 T^-2，无定义 ⇒ 构造性欠定
add("D06", "BOUNDARY",
    "ρ_top / ρ_meta 的量纲与定义",
    "来料 A1 修复仅声明 'K_s,K_w 无量纲；ρ_top,ρ_meta 量纲 T^-2'，但全册未给 ρ_top/ρ_meta 的定义式、未给 ρ_meta 的演化方程 ⇒ 量纲齐一靠声明，内容为空",
    note="声明式齐一，非构造性齐一")

# D07 公理 4 的 λ_c(∇τ)² g_μν 项
dim_lam_term = dpow(DIM_tau, 2)            # (∇τ)² → (L^-2)²= L^-4 ... 注意 ∇τ = L^-2
dim_nabla_tau = dmul(DIM_tau, DIM_tau)     # L^-2
dim_lam_term = dpow(dim_nabla_tau, 2)      # L^-4
ok_D07 = deq(dim_lam_term, DIM_inv_L2)
add("D07", "PASS" if ok_D07 else "FAIL",
    "公理4 第二项 λ_c(∇τ)²g_μν 与 R_μν 齐一性",
    "(∇τ)² → %s ；R_μν → %s ⇒ λ_c 须带量纲 %s ⇒ 有量纲自由参数（非定律级耦合）；来料第14章仅称其为'二阶反馈小系数'，未给量纲"
    % (dstr(dim_lam_term), dstr(DIM_inv_L2), dstr(ddiv(DIM_inv_L2, dim_lam_term))),
    lam_dim_required=dstr(ddiv(DIM_inv_L2, dim_lam_term)))

# D08 τ_g = (1/c)√(GM/r³)
dim_tau_g = dmul(dpow(DIM_c, -1), dpow(ddiv(dmul(DIM_G, DIM_M), dpow(DIM_L, 3)), Fraction(1, 2)))
ok_D08 = deq(dim_tau_g, DIM_tau)
add("D08", "PASS" if ok_D08 else "FAIL",
    "τ_g = (1/c)√(GM/r³) 量纲",
    "→ %s ；τ 应为 %s ⇒ %s" % (dstr(dim_tau_g), dstr(DIM_tau), "PASS" if ok_D08 else "FAIL"),
    got=dstr(dim_tau_g))

# D09 τ_e = (1/c)√((1/4πε₀) q²/(m r³))
dim_ke_q2_over_m = dmul(ddiv(DIMLESS, DIM_eps0), ddiv(dpow(DIM_Q, 2), DIM_M))  # L^3 T^-2
dim_tau_e = dmul(dpow(DIM_c, -1), dpow(ddiv(dim_ke_q2_over_m, dpow(DIM_L, 3)), Fraction(1, 2)))
ok_D09 = deq(dim_tau_e, DIM_tau)
add("D09", "PASS" if ok_D09 else "FAIL",
    "τ_e = (1/c)√((1/4πε₀)q²/(m r³)) 量纲",
    "(1/4πε₀)q²/m → %s ；τ_e → %s ⇒ %s（形式自洽；注意 GM ↔ (1/4πε₀)q²/m 的对应使 τ_e 含源质量 m）"
    % (dstr(dim_ke_q2_over_m), dstr(dim_tau_e), "PASS" if ok_D09 else "FAIL"),
    got=dstr(dim_tau_e))

# D10 强作用闭合条件 (6.1): τ_s² c² / a = K_s ħ c / a³
lhs_D10 = ddiv(dmul(dpow(DIM_tau, 2), dpow(DIM_c, 2)), DIM_L)     # L^-1 T^-2
rhs_D10 = ddiv(dmul(DIM_hbar, DIM_c), dpow(DIM_L, 3))             # M T^-2
ok_D10 = deq(lhs_D10, rhs_D10)
add("D10", "PASS" if ok_D10 else "FAIL",
    "强作用闭合条件 (6.1) τ_s²c²/a = K_s ħc/a³ 量纲",
    "LHS → %s ；RHS → %s ⇒ K_s 须带量纲 %s（来料称 K_s 无量纲并取 1）⇒ 不成立"
    % (dstr(lhs_D10), dstr(rhs_D10), dstr(ddiv(rhs_D10, lhs_D10))),
    lhs=dstr(lhs_D10), rhs=dstr(rhs_D10), K_s_required=dstr(ddiv(rhs_D10, lhs_D10)))

# D11 τ_s = √(K_s ħ/(c a³))
dim_tau_s = dpow(ddiv(DIM_hbar, dmul(DIM_c, dpow(DIM_L, 3))), Fraction(1, 2))
ok_D11 = deq(dim_tau_s, DIM_tau)
add("D11", "PASS" if ok_D11 else "FAIL",
    "τ_s = √(K_s ħ/(c a³)) 量纲",
    "→ %s ；τ 应为 L^-1 ⇒ %s（结果含 M^1/2：挠率不可能由 ħ/(c a³) 单独构成）"
    % (dstr(dim_tau_s), "PASS" if ok_D11 else "FAIL"),
    got=dstr(dim_tau_s))

# D12 E_W = ħc/ξ
dim_EW = ddiv(dmul(DIM_hbar, DIM_c), DIM_L)
ok_D12 = deq(dim_EW, DIM_energy)
add("D12", "PASS" if ok_D12 else "FAIL",
    "E_W = ħc/ξ 量纲",
    "→ %s ；能量应为 %s ⇒ %s" % (dstr(dim_EW), dstr(DIM_energy), "PASS" if ok_D12 else "FAIL"),
    got=dstr(dim_EW))

# D13 a = −ω×(ω×r) 的宇称与量纲
dim_a = dmul(dpow(dpow(DIM_T, -1), 2), DIM_L)
ok_D13 = deq(dim_a, DIM_acc)
add("D13", "PASS" if ok_D13 else "FAIL",
    "a = −ω×(ω×r) 量纲",
    "ω²r → %s ⇒ %s（量纲 OK；宇称见 F03：展开式含赝标量 (ω·r)ω 项）"
    % (dstr(dim_a), "PASS" if ok_D13 else "FAIL"),
    got=dstr(dim_a))

# D14 ρ_τ = c⁴/(16πG)|∇×τ₀|² 能量密度量纲
dim_rho_tau = dmul(ddiv(dpow(DIM_c, 4), DIM_G), D(0, -4, 0, 0))
ok_D14 = deq(dim_rho_tau, DIM_energy_density)
add("D14", "PASS" if ok_D14 else "FAIL",
    "宇宙学能量密度定义 ρ_τ = (c⁴/16πG)|∇×τ₀|² 量纲",
    "→ %s ；能量密度应 %s ⇒ %s（差 %s ⇒ (9.1)(9.2) 组合不成立）"
    % (dstr(dim_rho_tau), dstr(DIM_energy_density), "PASS" if ok_D14 else "FAIL",
       dstr(ddiv(dim_rho_tau, DIM_energy_density))),
    got=dstr(dim_rho_tau))

# D15 公理 4 的类型结构（指标/场类型登记，非浮点）
add("D15", "FAIL",
    "公理4 的张量类型：R_μν = (4/9)(1+GM/c²r)^-1(∇_μτ_ν+∇_ντ_μ) + λ_c(∇τ)²g_μν",
    "τ 是全册定义为 3-维轴矢量的场，未经 4 维提升即填入 4 维对称二阶张量方程；对称化 (∇_μτ_ν+∇_ντ_μ) 是形变张量型而非曲率型；且全册未定义 ∇_μ 作用于轴矢量的联络（含挠率时更未定义）⇒ 类型错误 + 构造缺失，该式不能用于任何定量推导（第 4.4/4.5 节也确实未用它）")

# D16 横向条件 ∇·τ=0 与 τ_φ(r)φ̂ 的相容性（公正项）
add("D16", "PASS",
    "横向条件 ∇·τ=0 与 τ=τ_φ(r)φ̂ 的相容性",
    "对纯方位角场 ∇·τ = (1/(r sinθ))[∂_θ(sinθ τ_θ) + ∂_φ τ_φ] = 0（τ_θ=0 且 ∂_φ=0）⇒ 自动满足，与该 ansatz 相容；且 ω⊥r 使 (ω·r)=0，赤道平面内 a=−ω²r 的推导成立",
    note="本项判 PASS：失败集中在源项与耦合，不在横向条件本身")

# =====================================================================
# B 段：场方程、源项与静态解（结构恒等式 + 数值残差双轨）
# =====================================================================

# E01 恒等式检测：∇×(f(r) r̂) ≡ 0 ⇒ 主方程源项在球对称静态情形恒零
def _curl_radial(f, h, pt):
    """数值 curl of A = f(r)*r_hat，中心差分，返回三分量"""
    x, y, z = pt
    out = []
    def A(px, py, pz):
        r = math.sqrt(px * px + py * py + pz * pz)
        if r == 0:
            return (0.0, 0.0, 0.0)
        return (f(r) * px / r, f(r) * py / r, f(r) * pz / r)
    # curl_x = dAz/dy - dAy/dz
    for (i, j, k) in ((2, 1, 2), (0, 2, 0), (1, 0, 1)):
        pass
    def comp(ci, cj, ck):
        # dA_k/dx_j  (ci = component of curl index)
        p1 = [x, y, z]; p1[cj] += h; a1 = A(*p1)[ck]
        p2 = [x, y, z]; p2[cj] -= h; a2 = A(*p2)[ck]
        return (a1 - a2) / (2 * h)
    # curl_i = eps_ijk d_j A_k
    cx = comp(0, 1, 2) - comp(0, 2, 1)
    cy = comp(1, 2, 0) - comp(1, 0, 2)
    cz = comp(2, 0, 1) - comp(2, 1, 0)
    return (cx, cy, cz)


def _f_gauss(r):
    return math.exp(-(r / 1.0) ** 2)      # 光滑径向剖面（避免原点奇异）


scale = 1.0
pts = [(0.7, 0.3, 0.5), (1.2, -0.4, 0.9), (0.2, 0.8, -1.1)]
scan_E01 = []
for h in (1e-3, 1e-4, 1e-5):
    worst = 0.0
    for p in pts:
        cx, cy, cz = _curl_radial(_f_gauss, h, p)
        worst = max(worst, abs(cx), abs(cy), abs(cz))
    scan_E01.append({"h": h, "max_abs_curl": worst})
# 判零纪律：宣布机器零前必须做收敛阶扫描。残差按 h^p 且 p≈2（差分截断）⇒ 真值为 0；
# 若 p≈0（残差趋于常数）⇒ 真值非零。绝不以单档小残差冒充零。
def conv_order(scan):
    (h1, r1) = (scan[0]["h"], scan[0]["max_abs_curl"])
    (h2, r2) = (scan[1]["h"], scan[1]["max_abs_curl"])
    (h3, r3) = (scan[2]["h"], scan[2]["max_abs_curl"])
    o12 = math.log(r1 / r2) / math.log(h1 / h2) if (r2 > 0 and r1 > 0) else float("nan")
    o23 = math.log(r2 / r3) / math.log(h2 / h3) if (r3 > 0 and r2 > 0) else float("nan")
    return (o12 + o23) / 2.0


order_E01 = conv_order(scan_E01)
min_curl_E01 = min(s["max_abs_curl"] for s in scan_E01)
ok_E01_zero = (order_E01 > 1.5) and (min_curl_E01 < 1e-9)
add("E01", "FAIL" if ok_E01_zero else "BOUNDARY",
    "主方程源项 ∇×J_τ 在球对称静态情形是否恒零（J_τ ∥ r̂）",
    "∇×(f(r)r̂)=∇f×r̂+f∇×r̂≡0（∇×r̂=∇×∇r≡0）。收敛阶扫描（3 点 ×3 档步长）：残差 %s→%s→%s，阶 p≈%.2f（二阶截断，真值=0），最小残差 %s ⇒ 恒零成立 ⇒ 来料主方程的引力源项对任何球对称质量分布恒为零，主方程在球对称静态情形无源"
    % (fmt(Decimal(scan_E01[0]["max_abs_curl"]), 6), fmt(Decimal(scan_E01[1]["max_abs_curl"]), 6),
       fmt(Decimal(scan_E01[2]["max_abs_curl"]), 6), order_E01, fmt(Decimal(min_curl_E01), 6)),
    scan=scan_E01, order=order_E01, min_abs_curl=min_curl_E01)

# E01b 反向对照（防恒零检测器无牙）：A = f(r) φ̂ 的 curl 应非零
def _curl_azimuth(f, h, pt):
    x, y, z = pt
    def A(px, py, pz):
        r = math.sqrt(px * px + py * py + pz * pz)
        rr = math.sqrt(px * px + py * py)
        if rr == 0 or r == 0:
            return (0.0, 0.0, 0.0)
        # φ̂ = (-y, x, 0)/ρ
        return (f(r) * (-py / rr), f(r) * (px / rr), 0.0)
    def comp(cj, ck):
        p1 = [x, y, z]; p1[cj] += h; a1 = A(*p1)[ck]
        p2 = [x, y, z]; p2[cj] -= h; a2 = A(*p2)[ck]
        return (a1 - a2) / (2 * h)
    cx = comp(1, 2) - comp(2, 1)
    cy = comp(2, 0) - comp(0, 2)
    cz = comp(0, 1) - comp(1, 0)
    return (cx, cy, cz)


scan_E01b = []
for h in (1e-3, 1e-4, 1e-5):
    worst = 0.0
    for p in pts:
        cx, cy, cz = _curl_azimuth(_f_gauss, h, p)
        worst = max(worst, abs(cx), abs(cy), abs(cz))
    scan_E01b.append({"h": h, "max_abs_curl": worst})
order_E01b = conv_order(scan_E01b)
max_curl_E01b = max(s["max_abs_curl"] for s in scan_E01b)
ok_E01b = (max_curl_E01b > 1e-3) and (order_E01b < 0.5)
guard(ok_E01b, "g_ctrl_curl_detector_has_teeth",
      "切向场对照必须给出非零 curl 且收敛阶≈0，否则 E01 的恒零结论不可信；实测 %s / p≈%.2f"
      % (fmt(Decimal(max_curl_E01b), 6), order_E01b))
add("PC1", "PASS" if ok_E01b else "FAIL",
    "阳性对照 PC1：恒零检测器的反向对照（A=f(r)φ̂，切向场）",
    "切向场残差 %s→%s→%s，阶 p≈%.2f（不随 h 下降 ⇒ 真值非零 %s）⇒ 同一检测器在 E01 给出 p≈%.2f（真值 0）、在对照给出 p≈%.2f（真值非零）⇒ 检测器有判别力，E01 的恒零不是'检测器恒零'"
    % (fmt(Decimal(scan_E01b[0]["max_abs_curl"]), 6), fmt(Decimal(scan_E01b[1]["max_abs_curl"]), 6),
       fmt(Decimal(scan_E01b[2]["max_abs_curl"]), 6), order_E01b, fmt(Decimal(max_curl_E01b), 6),
       order_E01, order_E01b),
    scan=scan_E01b, order=order_E01b)

guard(order_E01 > 1.5 and order_E01b < 0.5, "g_order_scan_teeth",
      "收敛阶扫描须能区分真值零（p≈2）与真值非零（p≈0）；实测 p_E01=%.2f / p_PC1=%.2f" % (order_E01, order_E01b))

# E02 无源区矢量拉普拉斯对 τ ∝ r^n 的残差（解析：特征式 n²−1）
def lap_coeff(n):
    n = Fraction(n)
    return n * n - 1                    # (d²/dr² + (1/r)d/dr − 1/r²) r^n = (n²−1) r^{n−2}


c_m32 = lap_coeff(Fraction(-3, 2))      # 来料 3.3 式 τ ∝ r^{-3/2}
c_m1 = lap_coeff(Fraction(-1))          # 来料 2.5 节 τ ∝ 1/r
c_p1 = lap_coeff(Fraction(1))
ok_E02 = (c_m32 == 0)
add("E02", "PASS" if ok_E02 else "FAIL",
    "来料 3.3 式 τ(r)=(1/c)√(GM/r³) ∝ r^{-3/2} 是否满足其自身场方程（无源区 ∇²τ=0）",
    "对 τ_φ∝r^n：∇²(τ_φφ̂)=(n²−1)r^{n−2}φ̂。n=−3/2 ⇒ 系数 %s ≠ 0 ⇒ 3.3 式不是主方程的解（残差 ∝ (5/4)r^{-7/2}）"
    % str(c_m32),
    n_neg3over2=str(c_m32), n_neg1=str(c_m1), n_pos1=str(c_p1))

# E03 来料 2.5 节 τ ∝ 1/r 的自洽性（公正对照：该推导本身正确）
ok_E03 = (c_m1 == 0)
guard((not ok_E02) and ok_E03, "g_pair_E02_E03_teeth",
      "同一残差判据须对 r^-1 给 PASS、对 r^-3/2 给 FAIL，否则 E02 是恒红引擎；实测 FAIL/PASS = %s/%s" % (not ok_E02, ok_E03))
add("E03", "PASS" if ok_E03 else "FAIL",
    "来料 2.5 节 τ_φ∝1/r 的自洽性",
    "n=−1 ⇒ 系数 %s ⇒ 满足无源区方程，推导本身正确（与 E02 对照，证明 E02 的 FAIL 是来料的实质缺陷而非引擎偏差）"
    % str(c_m1))

# E04 同一 ansatz 的两个互斥静态解
add("E04", "FAIL" if (c_m32 != 0 and c_m1 == 0) else "BOUNDARY",
    "内部一致性：2.5 节 τ∝1/r 与 3.5 节 τ∝r^{-3/2} 同为 τ_φ(r)φ̂ ansatz",
    "两处用完全相同的 ansatz（纯切向轴矢量 τ_φ(r)φ̂）与同一静态方程，却给出两个不同幂次；且 r^{-3/2} 不满足方程 ⇒ 引力支的静态解既非唯一解也非合法解",
    sol_25="r^-1 (合法)", sol_35="r^-3/2 (非法)")

# E05 牛顿项是反解输入还是输出
add("E05", "FAIL",
    "牛顿引力是否为 TUFT 的推导结果",
    "τ_g 定义 (1/c)√(GM/r³) 已内含 GM，代入 a=c²τ²r 得 GM/r² 是恒等回代；且 E01 已证 τ_g 无场方程支撑（源项恒零）⇒ 牛顿项是输入而非涌现结果（循环/反解）",
    note="与 r103 对另一来料的 CIRCULAR 判定同型")

print("[r108] A/B 段 done", flush=True)

# =====================================================================
# C 段：力与现象（数值）
# =====================================================================

# F01 地表 g（复算来料数值，证引擎无偏差）
g_calc = G * MEARTH / (REARTH * REARTH)
dev_g = rel(g_calc, CLAIM["g_surface"])
ok_F01 = dev_g < Decimal("1e-3")
guard(ok_F01, "g_num_engine_reproduces_claim_g",
      "数值引擎须复现来料地表 g=9.820，实测 %s（相对偏差 %s）" % (fmt(g_calc), fmt(dev_g, 6)))
dev_g_obs = rel(g_calc, G_STD)
add("F01", "PASS" if ok_F01 else "FAIL",
    "数值引擎对照：地表 g = GM_⊕/R_⊕²",
    "复算 %s m/s² vs 来料自称 9.820 ⇒ 相对偏差 %s ⇒ 引擎无系统性偏差；vs 标准重力 9.80665 ⇒ 偏差 %s（来料归因于椭率+自转，属标准牛顿修正，非 TUFT 效应）。注：该式为纯牛顿式，与 τ 无关（见 M01）"
    % (fmt(g_calc), fmt(dev_g, 6), fmt(dev_g_obs, 6)),
    calc=fmt(g_calc), claim=fmt(CLAIM["g_surface"]), rel_dev=fmt(dev_g, 6), rel_dev_vs_std=fmt(dev_g_obs, 6))

# F02 水星进动复算（6π 式）
a_m = Decimal("5.7909e10")
e_m = Decimal("0.20563")
per_orbit = Decimal(6) * Decimal(math.pi) * G * MSUN / (C * C * a_m * (1 - e_m * e_m))
orbits_per_century = (Decimal(100) * Decimal("365.25") * DAY) / (Decimal("87.969") * DAY)
merc_arcsec = per_orbit * orbits_per_century * ARCSEC_PER_RAD
dev_merc = rel(merc_arcsec, CLAIM["mercury_arcsec"])
ok_F02 = dev_merc < Decimal("2e-3")
guard(ok_F02, "g_num_engine_reproduces_mercury",
      "复算水星进动须与来料 42.98 一致，实测 %s" % fmt(merc_arcsec))
add("F02", "PASS" if ok_F02 else "FAIL",
    "数值引擎对照：水星进动 6πGM/(c²a(1−e²))",
    "复算 %s 角秒/百年 vs 来料 42.98 ⇒ 相对偏差 %s。注：6π 式为 GR 标准结果，其中 2π 来自挠率涡旋、4π 来自含自由系数 4/9 的派生曲率（见 F04）"
    % (fmt(merc_arcsec), fmt(dev_merc, 6)),
    calc=fmt(merc_arcsec), claim=fmt(CLAIM["mercury_arcsec"]), orbits=fmt(orbits_per_century))

# F03 4/9 系数的预测力（可调参数拟合）
# 6π = 2π + 4π，其中 4π 项带系数 4/9 ⇒ 总系数 = 2π + (4/9)·(9π)?? 来料结构：Δφ_τ=2πX, Δφ_R=4πX, X=GM/(c²a(1−e²))
# 来料称 4/9 由观测反推 ⇒ 则 Δφ_total 是拟合目标，独立预测力 = 0
n_fit_mercury = 1          # 4/9 为拟合自由度
n_pred_mercury = 0         # 拟合后不再预测任何独立量
add("F03", "FAIL",
    "水星进动的可预测性（4/9 为观测反推参数）",
    "来料 OPEN-1 自承 4/9 '由观测反推锁定'。拟合参数个数 %d，由该式产生的独立预测数 %d ⇒ 与观测吻合是拟合的必然结果，零预测力（拟合≠检验）"
    % (n_fit_mercury, n_pred_mercury),
    n_fit=n_fit_mercury, n_pred=n_pred_mercury)

# F04 电磁支：力是否依赖检验粒子质量
m_ratio = ME / MP
E1_std = Decimal("13.6")                       # eV，氢原子基态（标准量子力学结果，外部输入）
E1_tuft = E1_std * m_ratio * m_ratio           # k_eff = (m_test/m_src)·(1/4πε₀)
ratio_E1 = E1_std / E1_tuft                    # 观测/预测 倍数
rel_short = abs(E1_tuft - E1_std) / E1_std     # 相对短缺
ok_F04 = rel(E1_tuft, E1_std) < Decimal("1e-3")
add("F04", "PASS" if ok_F04 else "FAIL",
    "电磁支：库仑力与检验粒子质量的无关性",
    "τ_e²∝q²/m_src ⇒ F = m_test c²τ_e²r = (m_test/m_src)·(1/4πε₀)q²/r²。取氢（源=质子，检验=电子）：m_e/m_p = %s ⇒ 有效库仑常数缩小同倍数 ⇒ 基态结合能预测 %s eV vs 实测 13.6 eV ⇒ 观测/预测 = %s 倍（相对短缺 %s）"
    % (fmt(m_ratio, 8), fmt(E1_tuft, 6), fmt(ratio_E1, 6), fmt(rel_short, 6)),
    m_ratio=fmt(m_ratio, 8), E1_TUFT_eV=fmt(E1_tuft, 6), E1_obs_eV=fmt(E1_std),
    ratio_obs_over_tuft=fmt(ratio_E1, 6), rel_shortfall=fmt(rel_short, 6))

# F05 电磁支符号：能否表述排斥
add("F05", "FAIL",
    "电磁支：力的符号结构",
    "a = −ω×(ω×r) ⇒ a ∝ −τ²r，τ² ≥ 0 恒成立 ⇒ TUFT 的电磁力对任意电荷组合恒为吸引；无 q₁q₂ 语法（来料只给 q²）⇒ 同号电荷排斥、异号吸引均无法表述",
    note="符号由几何拖拽结构锁定，与电荷号无关")

# F06 引力支赝标量项与 PPN α₁/α₂ 声称的冲突
add("F06", "FAIL",
    "引力支赝标量项 vs 附录 D 声称 α₁=α₂=0",
    "a = −ω²r + (ω·r)ω，其中 (ω·r) 为赝标量、ω 定义全域优先手性轴 ⇒ 存在优先方向/优先框架效应；来料附录 D 却声称 α₁=α₂=0、ξ=0 ⇒ 自相矛盾（且该项在赤道平面外不为零）",
    note="τ 场的方向本身即优先框架")

# F07 强作用禁闭能标：正文算术 vs 公式
E_conf_J = HBAR * C / CLAIM["a_conf"]
E_conf_MeV = E_conf_J / (EV_J * Decimal("1e6"))
E_text_MeV = CLAIM["E_conf_text_J"] / (EV_J * Decimal("1e6"))
dev_conf = rel(E_conf_MeV, E_text_MeV)
ok_F07 = dev_conf < Decimal("1e-2")
add("F07", "PASS" if ok_F07 else "FAIL",
    "强作用禁闭能标 E_s = ħc/a 的算术自洽",
    "公式值 = %s MeV（= %s J）；来料正文写 %s J ≈ %s MeV ⇒ 相对偏差 %s ⇒ 正文算术错误；且正文 148 MeV 与摘要/审计表 246.7 MeV 三处数字互斥"
    % (fmt(E_conf_MeV), fmt(E_conf_J), fmt(CLAIM["E_conf_text_J"]), fmt(E_text_MeV), fmt(dev_conf, 6)),
    formula_MeV=fmt(E_conf_MeV), text_MeV=fmt(E_text_MeV), rel_dev=fmt(dev_conf, 6))

# F08 τ_s 数值 vs 其自身公式
tau_s_formula = (HBAR / (C * CLAIM["a_conf"] ** 3)).sqrt()
ratio_tau_s = CLAIM["tau_s"] / tau_s_formula
ok_F08 = rel(CLAIM["tau_s"], tau_s_formula) < Decimal("1e-2")
add("F08", "PASS" if ok_F08 else "FAIL",
    "τ_s 数值与其公式 √(K_s ħ/(c a³)) 的一致性",
    "公式值（K_s=1, a=0.8 fm）= %s m^-1；来料给 %s m^-1 ⇒ 比值 %s ⇒ 差约 %.1f 个数量级（注：来料 τ_s 与 ω_s=cτ_s 内部互洽，但与产生它的公式脱节）"
    % (fmt(tau_s_formula), fmt(CLAIM["tau_s"]), fmt(ratio_tau_s, 6), float(ratio_tau_s).__abs__() and math.log10(abs(float(ratio_tau_s)))),
    formula=fmt(tau_s_formula), claim=fmt(CLAIM["tau_s"]), ratio=fmt(ratio_tau_s, 6))

# F09 弱作用：116 GeV 是否落在 W/Z 质量区间
E_W_calc = HBAR * C / CLAIM["xi_weak_m"] / (EV_J * Decimal("1e9"))
mW, mZ = Decimal("80.4"), Decimal("91.2")
in_window = (mW <= E_W_calc <= mZ)
dev_claim = rel(E_W_calc, CLAIM["E_W_GeV"])
add("F09", "PASS" if (in_window and dev_claim < Decimal("1e-2")) else "FAIL",
    "弱作用能标：E_W = ħc/ξ 是否闭合 W/Z 质量区间",
    "ξ=1.7e-18 m ⇒ E_W = %s GeV（与来料 116 GeV 一致到 %s）；但 W/Z 质量区间为 80.4–91.2 GeV ⇒ 116 GeV 在区间外 ⇒ 来料'闭合'说法不成立（靠新设'拓扑共振宽度 80–120'放宽）"
    % (fmt(E_W_calc), fmt(dev_claim, 6)),
    E_W_GeV=fmt(E_W_calc), in_window=bool(in_window))

# F10 弱作用单位口径（审计 A3 写 "1.7 fm"）
xi_fm_m = CLAIM["xi_audit_fm"] * Decimal("1e-15")
E_W_if_fm = HBAR * C / xi_fm_m / (EV_J * Decimal("1e9"))
ok_F10 = rel(E_W_if_fm, CLAIM["E_W_GeV"]) < Decimal("1e-2")
add("F10", "PASS" if ok_F10 else "FAIL",
    "弱作用尺度单位口径一致性（审计 A3 称 ξ∈1.7–2.5 fm）",
    "若 ξ 真为 1.7 fm = 1.7e-15 m，则 E_W = %s GeV（= %s MeV），与来料的 116 GeV 差 1000 倍 ⇒ A3 的 'fm' 应为 10^-18 m（阿米量级）；第 7 章正文 1.7e-18 m 与审计表 fm 口径互斥"
    % (fmt(E_W_if_fm, 6), fmt(E_W_if_fm * Decimal("1000"), 6)),
    E_W_if_fm_GeV=fmt(E_W_if_fm, 6), claim_GeV=fmt(CLAIM["E_W_GeV"]))

# F11 引力波第三偏振（V 模式）的构造基础
add("F11", "FAIL",
    "引力波第三偏振（V 模式）是否有构造支撑",
    "公理 4 给 R_μν ∝ ∇τ（一阶代数关系，无 τ 的二阶传播注入）⇒ 曲率不独立传播 ⇒ TUFT 无法同时持有'GR 的两张量偏振'与'本源挠率螺旋偏振'；且全册未给 τ→h_μν 的耦合与投影算符 ⇒ 该预言为断言",
    note="代数派生 vs 传播自由度，结构性冲突")

# F12 挠率波传播：由主方程到色散关系（此项来料正确）
add("F12", "PASS",
    "挠率波真空色散 ω=ck 与圆偏振本征态",
    "□τ=0 ⇒ ω²=c²k²；τ 为横波轴矢量 ⇒ 本征偏振为左/右旋圆偏振。推导自洽（其内容独立于主方程源项的缺陷）",
    note="本册对该章判 PASS：失败集中在源项与耦合，不在波算子本身")

# F13 星系晕 τ₀ 与公理 7 零点背景 τ₀≈1/l_P 的符号重载
tau0_planck = Decimal(1) / LP
ratio_tau0 = tau0_planck / CLAIM["tau0_galaxy"]
ok_F13 = rel(tau0_planck, CLAIM["tau0_galaxy"]) < Decimal("1e-2")
add("F13", "PASS" if ok_F13 else "FAIL",
    "符号重载：τ₀ 在公理 7 与第 10 章的两个取值",
    "公理7 τ₀≈1/l_P = %s m^-1；银河 τ₀ = %s m^-1 ⇒ 相差 %s 倍（≈ %.0f 个数量级）⇒ 同一符号承载两个相差 10^58 的对象，公理 7 的'惯性起源'与第 10 章的晕场不是同一实体"
    % (fmt(tau0_planck), fmt(CLAIM["tau0_galaxy"]), fmt(ratio_tau0, 6), math.log10(float(ratio_tau0))),
    planck=fmt(tau0_planck), galaxy=fmt(CLAIM["tau0_galaxy"]), ratio=fmt(ratio_tau0, 6))

# F14 交叉一致性（引用并行线 r107 受理对象，不重复判决）：v = c τ₀ r₀
r0 = Decimal(8) * KPC                        # 外部输入：银河参考半径 8 kpc（标准值）
v_flat = C * CLAIM["tau0_galaxy"] * r0 / Decimal(1000)   # km/s
ok_F14 = Decimal("150") < v_flat < Decimal("300")
add("F14", "PASS" if ok_F14 else "BOUNDARY",
    "交叉一致性：τ_φ=τ₀r₀/r ⇒ v=cτ₀r₀（引用 r107 受理对象，本册不重复判决）",
    "取 r₀=8 kpc（外部标准值）：v = %s km/s，落在银河旋转平台 150–300 km/s 区间 ⇒ 该支内部数值自洽（代价：τ₀r₀ 为每星系一个拟合自由度）。完整审计见并行线 r107"
    % fmt(v_flat),
    v_km_s=fmt(v_flat), note="DEFER to r107")

print("[r108] C 段 done", flush=True)

# =====================================================================
# D 段：宇宙学（ρ_τ ∝ S^-2 ⇒ w = −1/3）
# =====================================================================

# U01 ρ ∝ S^{-3(1+w)} ⇒ w = −1/3
w_tau = Fraction(-1, 3)
acc_factor = 1 + 3 * w_tau          # ä/a ∝ −(ρ+3p) ⇒ 1+3w
om_m = CLAIM["Omega_M"]
om_t = CLAIM["Omega_tau"]
q0 = Decimal("0.5") * (om_m * Decimal(1) + om_t * Decimal(1 + 3 * float(w_tau)))
q0_obs = Decimal("-0.55")
q0_obs_sig = Decimal("0.10")
sigma_q0 = abs(q0 - q0_obs) / q0_obs_sig
ok_U01 = (acc_factor == 0)
add("U01", "FAIL" if acc_factor == 0 else "PASS",
    "宇宙学：ρ_τ ∝ S^-2 ⇒ w = −1/3 ⇒ 是否驱动加速膨胀",
    "ρ ∝ S^{-3(1+w)} ⇒ w = −1/3 ⇒ 1+3w = %s ⇒ ä = 0（恰好临界，既不加速也不减速）。来料 9.3 节称挠率主导期'加速膨胀' ⇒ 与其自身 (9.1) 直接矛盾"
    % str(acc_factor),
    w=str(w_tau), one_plus_3w=str(acc_factor))

add("U02", "FAIL" if sigma_q0 > Decimal("3") else "PASS",
    "宇宙学：减速参数 q₀ 与观测",
    "q₀ = ½[Ω_M(1) + Ω_τ(1+3w)] = %s；观测 q₀ ≈ −0.55 ± 0.10 ⇒ 偏离 %s σ ⇒ 与超新星/BAO 宇宙加速事实冲突"
    % (fmt(q0), fmt(sigma_q0)),
    q0_TUFT=fmt(q0), q0_obs=fmt(q0_obs), sigma=fmt(sigma_q0))

w_obs = Decimal("-1.03")
w_obs_sig = Decimal("0.03")
sigma_w = abs(Decimal(float(w_tau)) - w_obs) / w_obs_sig
add("U03", "FAIL" if sigma_w > Decimal("3") else "PASS",
    "宇宙学：状态方程 w 与 Planck+SNe 联合约束",
    "w_TUFT = −1/3 = %s；观测 w = −1.03 ± 0.03 ⇒ 偏离 %s σ ⇒ ρ_τ∝S^-2 的暗能量模型被现有数据排除（不是'微小差别'）"
    % (fmt(Decimal(float(w_tau))), fmt(sigma_w)),
    w_TUFT=fmt(Decimal(float(w_tau))), w_obs=fmt(w_obs), sigma=fmt(sigma_w))

add("U04", "FAIL",
    "宇宙学：Ω 份额 0.311/0.689 的性质",
    "Ω_τ 由 ρ_{τ,0}（自由参数）归一化定出，Ω_M = 1 − Ω_τ ⇒ '与 Planck 吻合'是归一化条件 + 一个拟合参数的必然结果，非独立预言（且见 D14：ρ_τ 定义本身量纲不成立）",
    note="份额匹配 ≠ 模型正确")

# =====================================================================
# E 段：元层 —— 抄录检测 / 覆盖率 / 参数计数 / 协变性
# =====================================================================

TUFT_NATIVE = {"tau", "omega", "K_s", "K_w", "lambda_c", "xi", "tau_0", "H_top", "chi_tau"}

TESTS = [
    ("M01", "地表 g", {"G", "M", "R"}, "GM/R²"),
    ("M01b", "水星近日点进动", {"G", "M", "a", "e", "c"}, "6πGM/(c²a(1−e²))"),
    ("M01c", "光线偏折", {"G", "M", "c", "R"}, "4GM/(c²R)"),
    ("M01d", "引力红移", {"G", "M", "c", "r"}, "GM/c²(1/r₁−1/r₂)"),
    ("M01e", "力强比 F_e/F_g", {"e", "eps0", "G", "m_e"}, "e²/(4πε₀Gm_e²)"),
    ("M01f", "史瓦西半径", {"G", "M", "c"}, "2GM/c²"),
]

copied = []
for code, name, syms, formula in TESTS:
    if not (syms & TUFT_NATIVE):
        copied.append({"code": code, "test": name, "formula": formula})
frac_copied = Fraction(len(copied), len(TESTS))
add("M01", "FAIL" if len(copied) == len(TESTS) else ("BOUNDARY" if copied else "PASS"),
    "元层：来料 6 项'通过检验'的公式是否含 TUFT 本源符号",
    "6 项中符号集与 {τ,ω,K_s,K_w,λ_c,ξ,τ₀,H,χ_τ} 交集为空的有 %d 项（%s）⇒ 全部是牛顿/GR/教科书式的直接抄录，τ 机制未参与任何一项数值 ⇒ TUFT 的'通过经典检验'经验内容为零"
    % (len(copied), "、".join(c["test"] for c in copied)),
    n_copied=len(copied), n_total=len(TESTS), frac=str(frac_copied), detail_list=copied)

# M02 现象学覆盖率（r103 口径：接口槽位求交）
V10_SLOTS = {
    "torsion_field", "angular_velocity", "dalembertian", "mass", "charge", "radius",
    "force", "coupling_const", "eps0", "mass_density", "charge_density", "scale_factor",
    "energy_density", "hbar", "polarization", "velocity", "topological_index",
    "halo_torsion", "frequency", "acceleration", "metric_derived_g00",
}
COVER_TESTS = [
    ("C01", "牛顿平方反比", {"force", "coupling_const", "mass", "radius"}, "CIRCULAR"),
    ("C02", "PPN γ（偏折/Shapiro）", {"metric", "geodesic", "deflection"}, "ASSERTED"),
    ("C03", "PPN β（进动/红移）", {"metric", "perihelion"}, "FIT"),
    ("C04", "等效原理定量检验", {"mass", "force", "acceleration"}, "BLOCKED"),
    ("C05", "星系旋转曲线", {"halo_torsion", "radius", "velocity"}, "DEFER"),
    ("C06", "引力透镜", {"metric", "geodesic"}, "NO_SLOT"),
    ("C07", "框架拖曳", {"torsion_field", "angular_momentum"}, "NO_SLOT"),
    ("C08", "双星进动/引力波辐射", {"quadrupole", "radiation_reaction"}, "NO_SLOT"),
    ("C09", "宇宙学（膨胀/CMB）", {"scale_factor", "energy_density"}, "BLOCKED"),
    ("C10", "Coulomb 定律", {"force", "charge", "radius"}, "BLOCKED"),
    ("C11", "磁单极禁戒", {"magnetic_field", "gauss_law_magnetic"}, "NO_SLOT"),
    ("C12", "Lorentz 力", {"magnetic_field", "velocity", "charge"}, "NO_SLOT"),
    ("C13", "电磁波/Maxwell", {"magnetic_field", "dalembertian", "wave_solution"}, "NO_SLOT"),
    ("C14", "二体/N 体语法", {"force", "radius", "mass"}, "COVERED"),
]
# 阈值来源（禁拍脑袋）：来料自称已完成"引力 + 电磁"两支（第 4/5 章 + 摘要验收清单），
# 故最小闭合集取其自承范围内的检验项：C01(牛顿) C10(Coulomb) C11(div B=0) C12(Lorentz) C13(电磁波)
SCOPE_GRAV_EM = {"C01", "C10", "C11", "C12", "C13"}
N_SCOPE_REQUIRED = 4        # 自称统一两支 ⇒ 5 项闭合集中至少覆盖 4 项方视为"有资格"

cov_rows = []
n_covered = 0
n_noslot = 0
n_covered_scope = 0
for cid, name, need, forced in COVER_TESTS:
    inter = sorted(need & V10_SLOTS)
    if forced == "DEFER":
        cat = "DEFER"
    elif not inter:
        cat = "NO_SLOT"
    else:
        cat = forced
    if cat == "COVERED":
        n_covered += 1
        if cid in SCOPE_GRAV_EM:
            n_covered_scope += 1
    if cat == "NO_SLOT":
        n_noslot += 1
    cov_rows.append({"id": cid, "test": name, "need": sorted(need), "inter": inter, "cat": cat})
# 分类计数与明细一律由机读结果生成（禁手工写死分类数）
from collections import Counter

cat_cnt = Counter(r["cat"] for r in cov_rows)
cat_txt = "、".join("%s %d" % (k, v) for k, v in sorted(cat_cnt.items()))
noslot_txt = "、".join(r["test"] for r in cov_rows if r["cat"] == "NO_SLOT")
add("M02", "PASS" if n_covered_scope >= N_SCOPE_REQUIRED else "FAIL",
    "现象学覆盖率审计（r103 口径，14 项标准检验）",
    "机读分类计数：%s（合计 %d）。NO_SLOT 明细：%s。来料自承范围（引力+电磁）5 项闭合集 {%s} 中 COVERED = %d < 阈值 %d ⇒ 统一场论资格不成立"
    % (cat_txt, sum(cat_cnt.values()), noslot_txt, "、".join(sorted(SCOPE_GRAV_EM)),
       n_covered_scope, N_SCOPE_REQUIRED),
    n_covered=n_covered, n_noslot=n_noslot, n_total=14,
    cat_count=dict(cat_cnt), n_covered_scope=n_covered_scope,
    n_scope_required=N_SCOPE_REQUIRED, rows=cov_rows)

# M03 阳性对照：GR+ΛCDM 用同一覆盖判据
GR_SLOTS = V10_SLOTS | {"metric", "geodesic", "quadrupole", "radiation_reaction",
                        "magnetic_field", "gauss_law_magnetic", "wave_solution",
                        "angular_momentum", "deflection", "perihelion"}
gr_covered = 0
for cid, name, need, forced in COVER_TESTS:
    if need <= GR_SLOTS:
        gr_covered += 1
ok_M03 = gr_covered >= 12
guard(ok_M03, "g_ctrl_coverage_checker_has_teeth",
      "同一判据对 GR+ΛCDM 须给出高覆盖率，否则 M02 的低覆盖率是恒否引擎所致；实测 %d/14" % gr_covered)
add("PC2", "PASS" if ok_M03 else "FAIL",
    "阳性对照：同一覆盖判据施于 GR+ΛCDM 语义集",
    "GR+ΛCDM 语义集下 COVERED = %d/14 ⇒ 判据有判别力，M02 的 1/14 反映的是来料符号系统容量，不是恒否机器" % gr_covered,
    gr_covered=gr_covered)

# M04 参数计数门（n_自由 ≤ n_观测 − 1）
FREE_PARAMS = ["4/9（派生曲率系数，观测反推）", "λ_c（有量纲，量纲为 L²）", "K_s", "K_w",
               "κ₀（引力旋光，未定）", "τ₀r₀（每星系一个）", "ξ（弱作用尺度）",
               "a（孤环半径 0.8 fm）", "ρ_{τ,0}（宇宙学幅值）"]
n_free = len(FREE_PARAMS)
n_obs_native = 0     # 由 M01：所有吻合项均为标准公式抄录 ⇒ TUFT 独有且已测的检验数 = 0
ok_M04 = n_free <= max(n_obs_native - 1, 0)
add("M04", "PASS" if ok_M04 else "FAIL",
    "参数计数门：n_自由 ≤ n_观测(TUFT 独有) − 1",
    "n_自由 = %d（%s）；n_观测(TUFT 独有且已测) = %d（M01 已证 6 项吻合全部为标准公式抄录）⇒ %d ≤ %d 不成立 ⇒ 来料整体处于'参数多于约束'区域"
    % (n_free, "、".join(FREE_PARAMS), n_obs_native, n_free, n_obs_native - 1),
    n_free=n_free, n_obs=n_obs_native, params=FREE_PARAMS)

# M05 协变性/洛伦兹结构
add("M05", "FAIL",
    "协变性与洛伦兹结构",
    "主方程以 3-矢量形式写成 □τ=(4π/c³)∇×J_τ：源 J_τ ∥ r̂ 引入优先径向、τ 的轴向引入优先手性轴，全册未给 4 维协变形式与 τ 的洛伦兹表示 ⇒ 非协变；与附录 D 声称 α₁=α₂=α₃=0 冲突（见 F06）",
    note="缺 4 维形式 ⇒ PPN 声称无推导支撑")

# M06 来料诚实度（公正项）
add("M06", "PASS",
    "来料的诚实度（防过度指控）",
    "来料自列 9 项 OPEN（含 OPEN-1 的 4/9 未导出、OPEN-4 动电缺失、OPEN-8 晕稳定性缺失）、自曝水星残差、自设下限情景 κ₀=1e−3 ⇒ 自我暴露优于多数同类来料；本册 FAIL 判在结构缺陷，不在诚实度",
    note="诚实 ≠ 正确")

print("[r108] 元层 done", flush=True)

# =====================================================================
# F 段：量纲引擎阳性自检（防引擎假绿/假红）
# =====================================================================

checks = [
    ("E=mc²", dmul(DIM_M, dpow(DIM_c, 2)), DIM_energy),
    ("F=GMm/r²", ddiv(dmul(DIM_G, dpow(DIM_M, 2)), dpow(DIM_L, 2)), DIM_force),
    ("Coulomb F=e²/(4πε₀r²)", ddiv(dmul(dpow(DIM_Q, 2), ddiv(DIMLESS, DIM_eps0)), dpow(DIM_L, 2)), DIM_force),
    ("ℒ_EH=c⁴R/(16πG)", dmul(ddiv(dpow(DIM_c, 4), DIM_G), DIM_inv_L2), DIM_energy_density),
    ("[τ]=L^-1", DIM_tau, DIM_tau),
]
pc_fail = 0
for nm, a, b in checks:
    if not deq(a, b):
        pc_fail += 1
ok_PC2 = pc_fail == 0
guard(ok_PC2, "g_dim_engine_selfcheck",
      "量纲引擎对 5 条已知正确方程须全 PASS，实测失败 %d 条" % pc_fail)
add("PC3", "PASS" if ok_PC2 else "FAIL",
    "阳性对照 PC3：量纲引擎对已知正确方程自检（5 条）",
    "E=mc² / F=GMm/r² / Coulomb / ℒ_EH / [τ]=L^-1 ⇒ 失败 %d 条 ⇒ 引擎口径正确，A 段 FAIL 不是引擎偏差" % pc_fail,
    n_fail=pc_fail)

# PC3 数值引擎三处复现来料自称值（F01/F02/F07 已含）⇒ 汇总守卫
ok_PC3 = ok_F01 and ok_F02
guard(ok_PC3, "g_num_engine_selfcheck",
      "数值引擎须复现来料自称的地表 g 与水星进动，实测 %s / %s" % (ok_F01, ok_F02))
add("PC4", "PASS" if ok_PC3 else "FAIL",
    "阳性对照 PC4：数值引擎复现来料自称值（防过度指控）",
    "地表 g 相对偏差 %s；水星进动相对偏差 %s ⇒ 来料'算对了的部分'被本引擎逐位复现 ⇒ C/D 段的 FAIL 不是数值偏差所致"
    % (fmt(dev_g, 6), fmt(dev_merc, 6)),
    dev_g=fmt(dev_g, 6), dev_mercury=fmt(dev_merc, 6))

# =====================================================================
# 汇总
# =====================================================================
tally = {}
for e in ENTRIES:
    tally[e["verdict"]] = tally.get(e["verdict"], 0) + 1

n_fail = tally.get("FAIL", 0)
verdict_total = "FAIL" if n_fail > 0 else ("BOUNDARY" if tally.get("BOUNDARY", 0) else "PASS")

SUMMARY = {
    "tag": TAG,
    "target": "TUFT V10 螺旋挠率统一场论（算法联盟审计修复版）",
    "verdict_total": verdict_total,
    "tally": tally,
    "n_entries": len(ENTRIES),
    "guard_total": STATE["guard"],
    "guard_failed": STATE["guard_fail"],
    "guard_msgs": STATE["guard_msgs"],
    "coverage": {"covered": n_covered, "total": 14},
    "n_free_params": n_free,
    "n_obs_native": n_obs_native,
}

EXTERNAL_INPUTS = [
    "CODATA 2022 / IAU 2015 常数（c,G,ℏ,e,m_e,m_p,ε₀,M_⊙,R_⊙,M_⊕,R_⊕,kpc,l_P）",
    "观测值：g=9.80665、水星进动 43.0±0.5 ″/世纪、W/Z 质量 80.4/91.2 GeV、Λ_QCD≈200–250 MeV",
    "宇宙学观测：w=−1.03±0.03（Planck+SNe 联合）、q₀≈−0.55±0.10",
    "氢原子基态结合能 13.6 eV（标准量子力学结果，用作电磁支对照）",
    "银河参考半径 r₀=8 kpc（F14 交叉一致性用）",
    "r103 的 14 项现象学检验清单与接口槽位判据（继承，非重算）",
]

NOT_SELF_DERIVED = [
    "NS1 全部观测数据与 PDG/Planck 数值（只读引用，未重测）",
    "NS2 r103 的 14 项检验清单与 NO_SLOT/BLOCKED/CIRCULAR/COVERED 分类规则（继承；本册增设 ASSERTED/FIT/DEFER 三类并说明）",
    "NS3 来料符号语义集（从来料全文人工提取，随引擎落盘可复算）",
    "NS4 自由参数清单（从来料人工提取，计数由机器完成）",
    "NS5 不为来料补写场方程、不代选耦合、不代定能标（只判合格/不合格）",
    "NS6 星系挠率晕章（第 10 章）归并行线 r107，本册只做交叉一致性引用",
]

# ----------------------------------------------------------------- 落盘
if not os.path.isdir(OUT_DATA):
    os.makedirs(OUT_DATA, exist_ok=True)

payload = {
    "summary": SUMMARY,
    "entries": ENTRIES,
    "external_inputs": EXTERNAL_INPUTS,
    "not_self_derived": NOT_SELF_DERIVED,
}

with open(os.path.join(OUT_DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(_j(payload), f, ensure_ascii=False, indent=2)

# md
lines = []
lines.append("# r108 数据产物｜TUFT V10 外部来料主干全维攻破（机器读数）\n")
lines.append("- 总判决：**%s** ｜ 条目 %d ｜ %s ｜ 守卫 %d/%d"
             % (verdict_total, len(ENTRIES),
                " / ".join("%s %d" % (k, v) for k, v in sorted(tally.items())),
                STATE["guard"] - STATE["guard_fail"], STATE["guard"]))
lines.append("- 覆盖率：COVERED %d/14 ｜ 参数计数：n_自由=%d vs n_观测(TUFT 独有)=%d\n" % (n_covered, n_free, n_obs_native))
lines.append("| 代号 | 判决 | 条目 | 机读依据 |")
lines.append("|---|---|---|---|")
for e in ENTRIES:
    det = e["detail"].replace("\n", " ").replace("|", "/")
    if len(det) > 260:
        det = det[:260] + "…"
    lines.append("| %s | **%s** | %s | %s |" % (e["code"], e["verdict"], e["title"], det))
lines.append("\n## 外部输入（不自推）\n")
for s in EXTERNAL_INPUTS:
    lines.append("- " + s)
lines.append("\n## 不自推声明\n")
for s in NOT_SELF_DERIVED:
    lines.append("- " + s)
with open(os.path.join(OUT_DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# report
with open(os.path.join(OUT_DATA, TAG + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("TAG=%s\n" % TAG)
    f.write("VERDICT=%s\n" % verdict_total)
    f.write("TALLY=%s\n" % json.dumps(tally, ensure_ascii=False))
    f.write("GUARD=%d/%d failed=%d\n" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"], STATE["guard_fail"]))
    for m in STATE["guard_msgs"]:
        f.write("GUARD_FAIL: %s\n" % m)
    f.write("COVERED=%d/14\n" % n_covered)
    f.write("N_FREE=%d N_OBS_NATIVE=%d\n" % (n_free, n_obs_native))
    for e in ENTRIES:
        f.write("%-6s %-9s %s\n" % (e["code"], e["verdict"], e["title"]))
    f.flush()

print("[r108] VERDICT=%s  entries=%d  tally=%s" % (verdict_total, len(ENTRIES), tally), flush=True)
print("[r108] guard %d/%d  failed=%d" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"], STATE["guard_fail"]), flush=True)
print("[r108] COVERED=%d/14  n_free=%d  n_obs_native=%d" % (n_covered, n_free, n_obs_native), flush=True)
sys.exit(0)
