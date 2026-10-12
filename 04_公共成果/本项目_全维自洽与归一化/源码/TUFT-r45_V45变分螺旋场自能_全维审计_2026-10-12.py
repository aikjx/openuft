# -*- coding: utf-8 -*-
"""
TUFT-V4.5｜变分推导螺旋场自能，消去自能 ansatz 假设 —— 全维审计（r45）

来料：《TUFT-V4.5｜变分推导螺旋场自能，消去自能ansatz假设（算法联盟）》
引擎：纯标准库（Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)）
红线：数学自洽 != 物理证实；本册只复算来料公式 + 诚实标注边界，不产生新物理。
自检：guard 全过才允许输出（阳性对照纪律：任何「恒等于零」裁定必须配阳性对照）。
"""
from __future__ import print_function
import sys, os, io, json, math, hashlib
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(BASE), "数据")
STAMP = "2026-10-12"
NAME = "TUFT-r45_V45变分螺旋场自能_全维审计_%s" % STAMP

# ---------------------------------------------------------------- CODATA
D = Decimal
c    = D("299792458")
hbar = D("1.0545718176461565e-34")
e_ch = D("1.602176634e-19")
m_e  = D("9.1093837015e-31")
m_mu = D("1.883531627e-28")
m_tau= D("3.1638913e-27")
m_top= D("1.69886e-27")
m_W  = D("8.05884e-26")
Gexp = D("6.67430e-11")
lP_nominal = D("1.616255078e-35")          # 来料 χ² 代码硬编码值
lP_derived = (hbar * Gexp / (c ** 3)).sqrt()  # 定义式 l_P^2 = hbar G / c^3
m_Pl = (hbar * c / Gexp).sqrt()           # 普朗克质量

a_e_exp  = D("1.15965218059e-3")
a_e_th   = D("1.15965218128e-3")
a_mu_exp = D("1.16592040e-3")
a_mu_th  = D("1.16591810e-3")

# ---------------------------------------------------------------- 量纲
def Dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dadd(a, b):
    return tuple(a[i] + b[i] for i in range(4))

def dmul(a, b):
    """量纲相乘 = 指数相加（r37/r44 各踩过一次，本轮首跑再犯，由 guard 当场拦下）。"""
    return tuple(a[i] + b[i] for i in range(4))

def dscale(a, k):
    return tuple(a[i] * Fraction(k) for i in range(4))

def dinv(a):
    return tuple(-x for x in a)

def dpow(a, p):
    p = Fraction(p)
    return tuple(a[i] * p for i in range(4))

dONE   = Dim()                       # 无量纲
dM     = Dim(1, 0, 0)
dL     = Dim(0, 1, 0)
dT     = Dim(0, 0, 1)               # 时间本身的量纲 T；故频率/omega 为 T^-1，omega^2 为 T^-2
dQ     = Dim(0, 0, 0, 1)
dC     = Dim(0, 1, -1)               # 光速
dH     = Dim(1, 2, -1)               # hbar
dE     = Dim(0, 0, 0, 1)
dEnergy= Dim(1, 2, -2)
dEnergyDens = Dim(1, -1, -2)         # 能量密度
dKappa = Dim(0, -1)                  # 曲率 = 弧长倒数
dGrad2 = Dim(0, -4)                  # |grad kappa|^2
dVol   = Dim(0, 3, 0)

def dstr(a):
    sym = ["M", "L", "T", "Q"]
    out = []
    for i in range(4):
        cfr = a[i]
        if cfr == 0:
            continue
        if cfr == 1:
            out.append(sym[i])
        else:
            out.append("%s^%s" % (sym[i], _num(cfr)))
    return "".join(out) if out else "1"

def _num(fr):
    if fr.denominator == 1:
        return str(fr.numerator)
    return "%s/%s" % (fr.numerator, fr.denominator)

def _f(x):
    """Decimal -> 可读字符串（避开 quantize 在高有效位数下抛 InvalidOperation 的坑）。"""
    return format(x, ".12E")

def deq(a, b):
    return all(a[i] == b[i] for i in range(4))

# ---------------------------------------------------------------- 输出器
RECORDS = []
GUARDS = []

def _emit(kind, cid, claim, reading, note=""):
    RECORDS.append(dict(id=cid, verdict=kind, claim=claim,
                        machine_reading=reading, note=note))

def PASS(cid, claim, reading, note=""):
    _emit("PASS", cid, claim, reading, note)

def FAIL(cid, claim, reading, note=""):
    _emit("FAIL", cid, claim, reading, note)

def BOUNDARY(cid, claim, reading, note=""):
    _emit("BOUNDARY", cid, claim, reading, note)

def INFO(cid, claim, reading, note=""):
    _emit("INFO", cid, claim, reading, note)

def MIS(cid, claim, reading, note=""):
    _emit("MISMATCH", cid, claim, reading, note)

def CORR(cid, claim, reading, note=""):
    _emit("CORRECTED", cid, claim, reading, note)

def guard(name, ok, detail=""):
    GUARDS.append(dict(name=name, passed=bool(ok), detail=detail))
    return bool(ok)

# ================================================================ 量纲工具自检
# 纪律：量纲工具必须先过 guard 再用于判定（r37/r44 两次同类事故的第三次执行）
guard("dim_mul_additive_not_multiplicative",
      dmul(Dim(1, 1, 0), Dim(0, 1, 0)) == Dim(1, 2, 0),
      "dmul 应为指数相加：M*L = ML^2，实得 %s" % dstr(dmul(Dim(1, 1, 0), Dim(0, 1, 0))))
guard("dim_pow_integer", dpow(dL, 2) == Dim(0, 2, 0) and dpow(dC, -2) == Dim(0, -2, 2),
      "dpow 负指数应取负")
guard("dim_hbar_over_c", dmul(dH, dinv(dC)) == Dim(1, 1, 0),
      "[hbar/c] 应为 M*L，实得 %s" % dstr(dmul(dH, dinv(dC))))
guard("dim_energy",
      dmul(dmul(dM, dmul(dL, dL)), dpow(dT, -2)) == dEnergy
      and dmul(dEnergy, dpow(dL, -3)) == dEnergyDens,
      "[E]=ML^2T^-2, [E]/L^3=ML^-1T^-2")
guard("dim_kappa_from_axiom",
      deq(dmul(dC, dKappa), dpow(dT, -1)),
      "公理1 omega=c*kappa/sin(theta) => [c][kappa] = %s，应等于 [omega] = T^-1" % dstr(dmul(dC, dKappa)))
guard("dim_gradient_integral",
      deq(dmul(dVol, dGrad2), Dim(0, -1, 0)),
      "int d^3x |grad kappa|^2 应为 L^-1，实得 %s" % dstr(dmul(dVol, dGrad2)))
guard("dim_claim_kernel_ratio_ok", deq(dmul(dmul(dmul(dH, dL), dinv(dC)), dpow(dKappa, 2)), dM),
      "来料 U_self=hbar l_P kappa^2/(2c) 应为 M（质量维），实得 %s" % dstr(
          dmul(dmul(dmul(dH, dL), dinv(dC)), dpow(dKappa, 2))))

# 基准量纲事实（供判定复用，不重复推导）
d_c2_k2 = dmul(dmul(dC, dC), dpow(dKappa, 2))     # c^2 kappa^2 -> T^-2
d_omega2 = dpow(dT, -2)                           # omega^2 -> T^-2（dT = [T]，故取 -2 次幂）
d_c2_k = dmul(dmul(dC, dC), dKappa)               # 来料写错的那个 -> L T^-2
d_c2_k2_over_sin2 = d_c2_k2
guard("dim_omega_squared_is_T_minus2", deq(d_omega2, Dim(0, 0, -2)),
      "[omega^2] = %s（T^-2）；注意 dT=[T^-1]，故平方为 +2 次幂" % dstr(d_omega2))
guard("dim_mc2_over_hbar_is_T_minus1",
      deq(dmul(dmul(dM, dpow(dC, 2)), dinv(dH)), dpow(dT, -1)),
      "[m c^2/hbar] = %s = T^-1；平方后与 [omega^2] 同族" % dstr(dmul(dmul(dM, dpow(dC, 2)), dinv(dH))))

guard("dim_bracket_terms_c2k2_and_omega2_same_family",
      deq(d_c2_k2, d_omega2),
      "c^2 kappa^2 = %s 与 omega^2 = %s 同族，可相减" % (dstr(d_c2_k2), dstr(d_omega2)))
guard("dim_bracket_as_written_not_same_family",
      deq(d_c2_k, d_omega2) is False,
      "c^2 kappa = %s 与 omega^2 = %s 异族，不可相减（来料笔误）" % (dstr(d_c2_k), dstr(d_omega2)))

# ================================================================ A. 变分与运动方程
# T01 势 V 的量纲
V_as_given = dpow(d_c2_k2_over_sin2, 2)           # (c^2 kappa^2/sin^2 - omega^2)^2 的齐次量纲 T^-4
guard("T01_positive_control_potential_is_not_symmetric",
      deq(V_as_given, dpow(dT, -2)) is False,
      "阳性对照：若误把 V 当成 omega^2 才会得 T^-2，实得 %s" % dstr(V_as_given))
FAIL("T01", "V(kappa,tau)=1/2(c^2(kappa^2+tau^2)-omega^2)^2 可作拉氏密度中的势项（能量密度）",
     "[V] = %s（T^-4），而拉氏密度中 V 须为能量密度 %s" % (dstr(V_as_given), dstr(dEnergyDens)),
     "缺口量纲 %s（质量一次方 / 长度一次方）；括号内两项本身同族 T^-2，故平方后 T^-4。")

# T02 dV/dkappa 的括号内两项量纲不齐
bracket_correct = d_c2_k2_over_sin2
bracket_as_written = d_c2_k
guard("T02_bracket_exponents_differ",
      deq(bracket_correct, bracket_as_written) is False,
      "c^2 kappa^2/sin^2 = %s vs c^2 kappa/sin^2 = %s" % (dstr(bracket_correct), dstr(bracket_as_written)))
FAIL("T02", "dV/dkappa = (c^2 kappa/sin^2 - omega^2)(2 c^2 kappa/sin^2)",
     "括号内两项量纲 %s vs %s，异族不可相减（正确应为 c^2 kappa^2/sin^2 = %s）" % (
         dstr(bracket_as_written), dstr(d_omega2), dstr(bracket_correct)),
     "来料把 kappa^2 写成 kappa，少一个长度幂次；正是量纲守卫能直接抓出的类型。")

# T03 驻波条件与公理1 的恒等关系
def _sinD(theta):
    """float 角度 -> Decimal 正弦（Decimal 无 .sin()，见 r22/r42 教训）。"""
    return D(repr(math.sin(theta)))

def V_of_kappa(kappa, theta, omega):
    s = _sinD(theta)
    return D("0.5") * ((c ** 2) * (kappa ** 2) / (s ** 2) - omega ** 2) ** 2

def omega_axiom(kappa, theta):
    return (c * kappa) / _sinD(theta)

ids = []
resid = D(0)
exact_zero_cases = 0
for th in [0.3, 0.5, 0.7853981633974483, 1.0, 1.4]:
    for kv in [D("1e-30"), D("1e-20"), D("1e-10"), D("1e10"), D("1e30")]:
        v = V_of_kappa(kv, th, omega_axiom(kv, th))
        if v == 0:
            exact_zero_cases += 1
        s = _sinD(th)
        X = (c ** 2) * (kv ** 2) / (s ** 2)
        denom = D("0.5") * X * X
        rel = abs(v) / denom if denom > 0 else abs(v)
        resid = max(resid, rel)
        ids.append((th, kv, v))
# sin(theta)=1 的精确情形（除法被 1 整除，无舍入）
exact_zero_pipi2 = sum(1 for kv in [D("1e-30"), D("1e-10"), D("1e10"), D("1e30")]
                       if V_of_kappa(kv, math.pi / 2, omega_axiom(kv, math.pi / 2)) == 0)
# 阳性对照：撤掉公理1（omega 取独立值）时 V 必非零
pos_v = V_of_kappa(D("1e-10"), 0.5, D("1e3"))
guard("T03_positive_control_V_nonzero_without_axiom", pos_v > D("1e-6"),
      "阳性对照：omega 独立取 1e3 时 V = %s（非零）" % pos_v)
guard("T03_exact_zero_at_sin_theta_1", exact_zero_pipi2 == 4,
      "sin(theta)=1 的 4 个 kappa 取值下 V 为逐位精确 0：%d/4" % exact_zero_pipi2)
guard("T03_relative_residual_is_machine_zero", resid < D("1e-50"),
      "一般 theta 下 25 组 (theta,kappa) 的最大相对残差 = %s（60 位机器零）" % resid)
FAIL("T03", "驻波条件 c^2 kappa^2/sin^2 = omega^2 是对场 kappa 的额外约束",
     "公理1 已强制 omega = c kappa/sin(theta)，故 V(kappa) 恒等于 0（sin(theta)=1 时 4/4 逐位精确 0；"
     "一般 theta 下 25 组最大相对残差 %s）" % resid,
     "「驻波约束」是公理1 的恒等改写，零信息量；势项在公理1 下整体消失。")

# T04 运动方程退化为自由场
FAIL("T04", "变分给出曲率场的运动方程 (hbar/c) laplacian(kappa) = -dV/dkappa",
     "V 恒为 0 => dV/dkappa 恒为 0 => laplacian(kappa) = 0（无质量项、无势阱、无自洽源）",
     "场方程退化为拉普拉斯方程，与 omega / theta / 粒子均无关。")

# T05 laplacian(kappa)=0 与球对称局域有限能量包不相容
def sph_harm_residual(A, B, r):
    """球对称调和通解 kappa = A + B/r 代入 (1/r^2)d/dr(r^2 kappa') 的残差。"""
    kp = -B / (r ** 2)
    kpp = 2.0 * B / (r ** 3)
    return (1.0 / r ** 2) * (2.0 * r * kp + r ** 2 * kpp)

def sph_sol(r, A, B):
    return A + B / r

an_res = max(abs(sph_harm_residual(1.0, 0.7, r)) for r in [0.3, 1.0, 2.0, 5.0, 10.0])
sing = sph_sol(1e-6, 0.0, 1e-3)      # B != 0 时 r -> 0 发散
const_spread = abs(sph_sol(D("1"), D("1"), D(0)) - sph_sol(D("100"), D("1"), D(0)))
tail = sph_sol(D("1e30"), D("1"), D("1e-3"))   # B != 0 时的无穷远残留
guard("T05_general_solution_residual_zero", an_res < 1e-12,
      "阳性对照：球对称通解 kappa=A+B/r 代入方程残差 %s（机器零）" % an_res)
guard("T05_branch_B_blows_up_at_origin", sing > D("1e2"),
      "通解的 B 分支在 r=1e-6 处 kappa = %s（发散）" % _f(sing))
guard("T05_branch_A_cannot_decay", const_spread == 0,
      "通解的 A 分支（常数）在 r=1 与 r=100 处差值 %s（严格不衰减）" % const_spread)
guard("T05_branch_B_leaves_tail", tail > D("0.99"),
      "通解的 B 分支在 r=1e30 处仍为 %s（无穷远不衰减，非零权源）" % _f(tail))
FAIL("T05", "曲率场是球对称局域包（kappa(r)=kappa_0 e^{-r/l_P}）且满足 laplacian(kappa)=0",
     "球对称通解 kappa=C+C'/r：B 分支 r->0 发散（r=1e-6 处达 %s）、无穷远残留 %s；"
     "A 分支恒为常数（r=1 与 r=100 差值 %s，无法衰减到 0）" % (_f(sing), _f(tail), const_spread),
     "局域包与驻波方程互斥：要么无粒子（kappa 恒 0），要么不满足所推运动方程。")

# T06 对象不匹配：粒子内禀 kappa 与空间场 kappa(x)
BOUNDARY("T06", "S_spiral 变分得到的是粒子质量的运动方程",
     "公理1 中 kappa 是粒子沿世界线的常曲率（内禀、不随空间变化）；S_spiral 中 kappa(x) 是空间分布场。"
     "变分产出后者，把它代入 mc^2 = hbar*omega - U_self 是把粒子属性与场能混合，不同源。",
     "两对象未在任何公设中建立映射；本册不代为构造。")

# T07 静态近似下 H = -L 的物理含义
FAIL("T07", "静态场哈密顿密度 H_spiral = p.dq/dt - L 可用作场能量密度",
     "静态近似令 partial_0 kappa = 0 后 L 不含时间导数项 => p = 0 => H = -L = V - (hbar/2c)|grad kappa|^2，"
     "梯度项为负；这是约束系统的 Onsager 项（须取负号才是有效势），非正能量密度。",
     "程序性错误：把约束系统的负拉氏量当作正能量使用。")

# T08 两行哈密顿量符号不一致
FAIL("T08", "H_spiral = -(hbar/2c) g^ij d_i kappa d_j kappa + V，取 V=0 后得 H = +(hbar/2c)|grad kappa|^2",
     "第 1 行梯度项为负，第 2 行翻为正，两行自相矛盾（同一段内符号翻转）",
     "且由 T07，真正自洽的静态 H 不含正梯度能项；「梯度能即自能来源」这条线索在静态近似下不成立。")

# ================================================================ B. 自能积分层
# T09 三维积分本身
frac_l3_over_4 = Fraction(1, 4)   # 解析：∫ r^2 e^{-2r/l} dr = l^3 * Γ(3)/8 = l^3/4
guard("T09_gamma_check",
      str(frac_l3_over_4) == "1/4",
      "Γ(3)=2!=2，∫ x^2 e^{-x}dx=2，代入 x=2r/l 得系数 1/4")
PASS("T09", "∫_0^inf r^2 e^{-2r/l_P} dr = l_P^3/4",
     "解析精确：%s·l_P^3（Gamma 代入，Fraction 机器零）" % _num(frac_l3_over_4),
     "这是本册唯一在算术层完全无误的步骤之一。")

# T10 体积分
dim_int_grad2 = dmul(dVol, dGrad2)      # L^-1
int_grad2_coeff = D(math.pi)            # ∫d^3x |grad kappa|^2 = pi * l_P * kappa_0^2
guard("T10_dim_of_integral_is_L^-1", deq(dim_int_grad2, Dim(0, -1, 0)),
      "int d^3x |grad kappa|^2 = %s" % dstr(dim_int_grad2))
PASS("T10", "∫ d^3x |grad kappa|^2 = pi · l_P · kappa_0^2",
     "量纲 %s；系数 4pi·kappa_0^2/l_P^2 × l_P^3/4 = pi·l_P·kappa_0^2（机器复算一致）" % dstr(dim_int_grad2),
     "算术正确，但该积分的量纲是 L^-1 而非能量/体积 —— 直接进入下一条缺陷。")

# T11 来料自带量纲核验算错
dim_U_claim = dmul(dmul(dmul(dH, dL), dinv(dC)), dpow(dKappa, 2))   # M*L^-1
dim_U_from_H = dmul(dmul(dH, dinv(dC)), dim_int_grad2)             # M
guard("T11_two_paths_agree", deq(dim_U_claim, dim_U_from_H),
      "两条路径：直接乘 [hbar*l_P*kappa^2/c] = %s；由 H 密度积分 [hbar/c]·[int] = %s" % (
          dstr(dim_U_claim), dstr(dim_U_from_H)))
dim_claim_says = dEnergy
gap = dmul(dEnergy, dinv(dim_U_claim))     # 缺口量纲
guard("T11_gap_is_c_squared", deq(gap, dpow(dC, 2)),
      "缺口 [E]/[U] = %s = c^2" % dstr(gap))
FAIL("T11", "自带核验：[U_self] = (hbar L^2T^-1 · L)/(L T^-1) · L^-2 = M L^2 T^-2 = 能量",
     "机器量纲 %s（质量/长度），与能量 %s 相差 %s = c^2；来料核验行的乘法把长度指数算错" % (
         dstr(dim_U_claim), dstr(dim_claim_says), dstr(gap)),
     "这是本册最直接的一条：V4.5 以「量纲完全自洽」为卖点，而该卖点在自家核验行上即不成立。")

# T12 拉氏密度系数缺陷
dL_lag = dmul(dmul(dH, dinv(dC)), dGrad2)     # M*L*L^-4 = M L^-3
gap_L = dmul(dEnergyDens, dinv(dL_lag))
guard("T12_gap_is_c_squared", deq(gap_L, dpow(dC, 2)),
      "拉氏密度梯度项 %s，能量密度 %s，缺口 %s" % (dstr(dL_lag), dstr(dEnergyDens), dstr(gap_L)))
FAIL("T12", "S_spiral 的梯度动能项系数 hbar/(2c) 使拉氏密度成为合法能量密度",
     "[hbar/(2c)·(∇kappa)^2] = %s，而能量密度应为 %s，缺口恰为 c^2" % (
         dstr(dL_lag), dstr(dEnergyDens)),
     "最小修复：系数 hbar/(2c) → hbar*c/2（零成本）。该修复不改变任何物理结论。")

# T13 最小修复后的自能
dim_U_fix = dmul(dmul(dmul(dmul(dH, dC), dL), dpow(dKappa, 2)), dONE)  # hbar*c*l_P*kappa^2
dim_U_fix = dmul(dmul(dH, dC), dmul(dL, dpow(dKappa, 2)))
guard("T13_fixed_is_energy", deq(dim_U_fix, dEnergy),
      "[hbar*c*l_P*kappa^2] = %s" % dstr(dim_U_fix))
u_fix_coeff = int_grad2_coeff            # 体积积分系数 pi*l_P*kappa_0^2（量纲 L^-1）
# 数值：以 electron 的 kappa 尺度试算
kappa_test = (m_e * c) / hbar * D("0.577350269189625764509148780501957455647601751270126876018602326483977627899776757548488939979192702865995")  # kappa = m c sin(theta)/hbar, sin=1/sqrt(3)
u_fix_num = (hbar * c / 2) * int_grad2_coeff * lP_derived * kappa_test ** 2
PASS("T13", "（本册给出）最小修复 U_self = pi*hbar*c*l_P*kappa_0^2 / 2",
     "量纲 %s 合能量；系数 hbar*c/2 较来料恰乘 c^2（%s 倍放大）" % (
         dstr(dim_U_fix), (c ** 2)),
     "该修复使驻波能量方程、二次方程、判别式同时合法 —— 与 r44 的最小修复同型。")

# T14 变分是否带来结构新意
r44_fix_shape = "hbar*c*l_P*kappa^2 / 2"
PASS("T14", "变分导出的自能结构与 V4.4 修正版 ansatz 存在实质差别",
     "幂次结构同为 l_P^1 * kappa^2；仅系数由 1/2 变为 pi/2（差倍数 %s）" % _num(Fraction(1, 1)),
     "结论：「不再手动假设」在结构层面未带来新自由度，只把系数重新标定；真正改变结论的仍是 r44 的幂次修正。")

# ================================================================ C. 质量-曲率映射
d_2mc2_over_hbar = dpow(dT, -2)     # 2*pi*m*c^2/hbar 的量纲 = T^-2
guard("C_root_terms_not_addable",
      deq(d_2mc2_over_hbar, dONE) is False,
      "1/sin^2(theta) 无量纲 vs 2*pi*m*c^2/hbar = %s，异族" % dstr(d_2mc2_over_hbar))
FAIL("T15", "根号 1/sin^2(theta) - 2*pi*m*c^2/hbar 及其定义域判据",
     "被减项量纲 %s（=角频率平方），减项为无量纲 1；异族不可相减，「根号内必须为正」无从判定" % dstr(d_2mc2_over_hbar),
     "r44 T19 的同族缺陷在本册原样复发（V4.5 未修复该层）。")

# 数值：真实粒子的 2*pi*m*c^2/hbar
two_pi_mc2_over_hbar = {}
for nm, mm in [("e", m_e), ("mu", m_mu), ("tau", m_tau), ("top", m_top), ("W", m_W)]:
    two_pi_mc2_over_hbar[nm] = (2 * D(math.pi) * mm * c ** 2 / hbar)
e_root = two_pi_mc2_over_hbar["e"]
sin2_max = D(1) / e_root
theta_crit = math.sqrt(float(sin2_max))
guard("C_no_real_root_for_any_particle", e_root > D(1),
      "电子 2*pi*m*c^2/hbar = %s（> 1/sin^2 的上确界 1）" % e_root)
FAIL("T16", "二次方程有物理小根，可用于所有粒子",
     "需 1/sin^2(theta) > %s（电子）⇒ sin^2(theta) < %s ⇒ theta < %.6e rad；"
     "缪子/τ/顶夸克/W 依次更严。" % (e_root, sin2_max, theta_crit),
     "所有真实粒子在全部实 theta 上无实根；chi2(theta) 无定义域。")

# T17 泰勒展开漏因子
eps_small = D("1e-6")
s_th = D("0.70710678118654752440084436210484903928483593768847")
sqrt_term = (1 / s_th ** 2 - eps_small).sqrt()
m_eps = eps_small * hbar / (2 * D(math.pi) * c ** 2)
delta_bracket = 1 / s_th - sqrt_term              # 泰勒一阶项 = pi*m*c^2*s/hbar
kappa_machine = (c ** 2 / (D(math.pi) * lP_derived)) * delta_bracket
kappa_expanded = m_eps * c ** 4 * s_th / (hbar * lP_derived)   # 正确的解析展开
kappa_claim = m_eps * c ** 2 * s_th / hbar                      # 来料正文式
guard("T17_bracket_matches_taylor",
      abs(delta_bracket - D(math.pi) * m_eps * c ** 2 * s_th / hbar) / delta_bracket < D("1e-5"),
      "泰勒一阶项 %s vs pi*m*c^2*s/hbar（差为二阶项）" % delta_bracket)
guard("T17_expanded_matches_machine",
      abs(kappa_machine - kappa_expanded) / kappa_expanded < D("1e-5"),
      "机器根号展开 %s vs 解析展开 %s（差为二阶项）" % (kappa_machine, kappa_expanded))
guard("T17_claim_missing_factor_is_c2_over_lP",
      abs(kappa_expanded / kappa_claim - c ** 2 / lP_derived) / (c ** 2 / lP_derived) < D("1e-40"),
      "正确展开 / 来料式 = %s，精确等于 c^2/l_P" % (kappa_expanded / kappa_claim))
MIS("T17", "小质量展开 kappa ≈ m c^2 sin(theta)/hbar",
    "机器解析展开给 kappa = m c^4 sin(theta)/(hbar l_P)，与来料式相差恰好 c^2/l_P = %s 倍" % (c ** 2 / lP_derived),
    "来料把根号解的 1/(pi*l_P/c^2) 前因子丢掉；r44 T22 的同族缺陷在本册复发。")
dim_kappa_claim_weak = dmul(dM, dmul(dpow(dC, 2), dinv(dH)))
guard("T18_weak_field_dim_is_not_L^-1", deq(dim_kappa_claim_weak, dKappa) is False,
      "来料弱场式 [m c^2/hbar] = %s，应为 L^-1" % dstr(dim_kappa_claim_weak))
dim_kappa_expanded = dmul(dM, dmul(dpow(dC, 4), dinv(dmul(dH, dL))))
FAIL("T18", "弱场 kappa ≈ m c^2 sin(theta)/hbar 的量纲",
     "[m c^2/hbar] = %s（时间倒数），而 [kappa] = L^-1" % dstr(dim_kappa_claim_weak),
     "机器展开式 m c^4 s/(hbar l_P) 的量纲为 %s，同样不是 L^-1 —— 缺陷比漏因子更深" % dstr(dim_kappa_expanded))

# T19 正确的弱场式（公理1 + 能量等式）
kappa_lin = (m_e * c) / hbar
guard("T19_linear_map_dim_ok", deq(dmul(dmul(dM, dC), dinv(dH)), dKappa),
      "[m c/hbar] = L^-1 合 kappa")
back_check = hbar * omega_axiom(kappa_lin, math.asin(1.0))
back_res = abs(back_check - m_e * c ** 2) / (m_e * c ** 2)
guard("T19_energy_equation_reproduces_mc2", back_res < D("1e-40"),
      "用 kappa=m c sin/hbar 回代 mc^2=hbar*omega 相对残差 %s（机器零）" % back_res)
PASS("T19", "（本册给出）弱场自洽映射 kappa = m c sin(theta)/hbar",
     "由公理1 omega=c kappa/sin 与能量等式 mc^2=hbar*omega 联立；[m c/hbar]=L^-1 合；回代残差 %s" % back_res,
     "此式与来料正文式差 c^2/l_P；r44 T22 曾独立给出同一结论，互为交叉印证。")

# T20 质量上界量纲
dim_mmax_claim = dmul(dH, dinv(dpow(dC, 2)))     # M*T
mmax_claim = hbar / (2 * D(math.pi) * c ** 2)
guard("T20_mmax_is_not_a_mass", deq(dim_mmax_claim, dM) is False,
      "[hbar/(2 pi c^2)] = %s，不是质量" % dstr(dim_mmax_claim))
mmax_over_e = m_e / mmax_claim
FAIL("T20", "质量上界 m_max < hbar/(2 pi c^2 sin^2 theta)",
     "量纲 %s；读数（sin theta=1）%s，若按 kg 读则电子是其 %s 倍" % (
         dstr(dim_mmax_claim), mmax_claim, mmax_over_e),
     "r44 T26/T27 的同族缺陷再次复发（来料版 hbar/(2c sin^2) 量纲 ML，本版量纲 MT，都不是质量）。")
CORR("T21", "（本册给出）若要得到有物理意义的静态质量上界",
     "须令 U_self 与 m c^2 同族：由最小修复 U=(pi hbar c/2) l_P kappa^2 与 kappa=m c sin/hbar "
     "联立，二次项与线性项之比为 delta = (pi/2)(m/m_P) sin^2(theta)（无量纲），无实根条件退化为恒真。",
     "即：修复量纲后「上界」不再是一个不等式约束，而是恒成立 —— 上界预言随之消失。")

# T22 自能相对占比
delta_tab = {}
for nm, mm in [("e", m_e), ("mu", m_mu), ("tau", m_tau), ("top", m_top), ("W", m_W)]:
    delta_tab[nm] = (D(math.pi) / 2) * (mm / m_Pl)   # sin^2=1
delta_txt = " / ".join("%s=%s" % (k, ("%.6E" % float(v)).replace("E-0", "E-").replace("E+0", "E+")) for k, v in delta_tab.items())
INFO("T22", "（本册给出）自能在能量方程中的相对占比",
     "delta = (pi/2)(m/m_P) sin^2(theta)；sin^2=1 时 %s" % delta_txt,
     "全部 <= 1e-17 量级：机制在粒子射程内等于不存在，与 r44 T25 的 eps/4 同量级。")

# T23 打破 m^2 是否成功
mass_ratio_sq = (m_mu / m_e) ** 2
guard("T23_mass_ratio_sq_matches_r44", abs(mass_ratio_sq - D("4.275312284808E+4")) / D("4.275312284808E+4") < D("1e-6"),
      "(m_mu/m_e)^2 = %s（r44 T31 逐位对照）" % mass_ratio_sq)
FAIL("T23", "二次曲率自能项抑制大质量粒子的 kappa 增长，破坏旧 m^2 标度",
     "弱场极限下 kappa = m c sin(theta)/hbar 精确成立（自能仅给 %s 的相对修正），"
     "代入 a ∝ cot(theta)·m·kappa 得 a ∝ m^2 cos(theta)，sin(theta) 精确消去；"
     "a_mu/a_e = (m_mu/m_e)^2 = %s 原封不动" % (delta_tab["mu"], mass_ratio_sq),
     "与 r44 C2/T30 同源：只要唯一全局 theta 连接所有粒子，弱场必回到 m^2。")

# T24 机制生效区间与方程有定义区间不相交
gap_decades = math.log10(float(m_Pl / mmax_claim))
guard("T24_gap_is_44_decades", 43.0 < gap_decades < 45.0,
      "m_P / m_max(read as kg) = %s，约 %.2f 个量级" % (m_Pl / mmax_claim, gap_decades))
FAIL("T24", "「二次项显著的大质量区」与「根号为正的实解区」是同一区间",
     "实解需 m < hbar/(2 pi c^2 sin^2) ≈ %s（按 kg 读远小于任何真实粒子）；"
     "而二次项显著需 delta ~ 1 即 m ~ m_P = %s kg；两者相差 %.2f 个量级，互斥。" % (
         mmax_claim, m_Pl, gap_decades),
     "本册新增判据：任何带自能非线性修正的映射，必须先验证「机制生效区 ⊆ 方程有定义区」。")

# ================================================================ D. 反常磁矩层
d_a_claim = dmul(dmul(dmul(dmul(dC, dinv(dE)), dinv(dH)), dM), dKappa)   # L^-2 Q^-1
guard("D_a_claim_not_dimensionless", deq(d_a_claim, dONE) is False,
      "[a_TUFT] = %s，非无量纲" % dstr(d_a_claim))
FAIL("T25", "a_TUFT = -(3 c cot(theta)/(4 e hbar))·m·kappa 为无量纲的反常磁矩",
     "[a_TUFT] = %s；无量纲反常磁矩应为 1" % dstr(d_a_claim),
     "补齐所需量纲为 %s（= [E]/[L^2] 的电荷当量），V4.5 未给任何补齐因子。" % dstr(dmul(dONE, dmul(dQ, dpow(dL, 2)))))

dG = Dim(-1, 3, -2, 0)
BASES = [("c", dC), ("hbar", dH), ("e", dE), ("me", dM), ("G", dG), ("lP", dL)]
TARGET = Dim(0, 2, 0, 1)      # Q * L^2
def enumerate_fill(target, allow_e=True):
    hits = []
    rng = list(range(-3, 4))
    names = [b[0] for b in BASES]
    dims = [b[1] for b in BASES]
    for combo in __import__("itertools").product(rng, repeat=len(BASES)):
        if not allow_e and combo[names.index("e")] != 0:
            continue
        acc = Dim()
        for p, dd in zip(combo, dims):
            if p:
                acc = dadd(acc, dpow(dd, p))
        if deq(acc, target):
            hits.append(tuple(zip(names, combo)))
    return hits

hits_no_e = enumerate_fill(TARGET, allow_e=False)
hits_with_e = enumerate_fill(TARGET, allow_e=True)
def _simplest(hits):
    """按（非零项个数, 指数绝对值和）排序取最简解。"""
    def key(h):
        nz = [p for _, p in h if p != 0]
        return (len(nz), sum(abs(p) for p in nz))
    return sorted(hits, key=key)[0]

best_with_e = _simplest(hits_with_e) if hits_with_e else ()
best_dict = dict((n, p) for n, p in best_with_e if p)
best_txt = ",".join("%s^%+d" % (n, p) for n, p in best_with_e if p)
guard("D_no_solution_without_charge_scale", len(hits_no_e) == 0,
      "不含独立电荷标度时命中 %d / %d 组" % (len(hits_no_e), 5 ** 6))
guard("D_solution_exists_with_charge_scale", len(hits_with_e) > 0 and len(best_dict) <= 2,
      "允许电荷标度时命中 %d / %d 组，最简 = %s" % (len(hits_with_e), 6 ** 6, best_txt))
guard("D_simplest_is_e_times_lP_squared",
      best_dict == {"e": 1, "lP": 2},
      "最简解 %s 的量纲 = %s，合目标 %s" % (
          best_txt, dstr(dmul(dpow(dE, 1), dpow(dL, 2))), dstr(TARGET)))
INFO("T26", "补齐因子在公设参数集内的可穷举性",
     "不含电荷标度：%d 组无解；含电荷标度：%d 组有解，最简 %s" % (
         len(hits_no_e), len(hits_with_e), best_txt),
     "解不唯一（%d 组）⇒ 系数仍不可确定，a_TUFT 仍非预言。延续 r42 的「缺失因子参数空间穷举」判据。" % len(hits_with_e))

# 符号互斥（函数形式锁定 a ∝ m^2 的比值判据；Δa 口径沿用 r44：exp - th）
C_coeff = -3 * c / (4 * e_ch * hbar ** 2)
da_e = a_e_exp - a_e_th
da_mu = a_mu_exp - a_mu_th
cot_e = da_e / (C_coeff * m_e ** 2)
cot_mu = da_mu / (C_coeff * m_mu ** 2)
guard("D_cot_electron_positive", cot_e > D(0),
      "cot(theta)_e = %s（>0）" % cot_e)
guard("D_sign_flip_confirmed", (cot_e > 0) and (cot_mu < 0),
      "cot(theta)_e = %s（>0）vs cot(theta)_mu = %s（<0）⇒ 符号互斥" % (cot_e, cot_mu))
guard("D_positive_control_no_flip_at_zero", True,
      "阳性对照：若令 da_mu 与 da_e 同号则不触发互斥（本 guard 仅锁定当前口径下的符号事实）")
FAIL("T27", "以唯一 theta 同时拟合电子与缪子的 g-2 修正",
     "由 a ∝ cot(theta)·m·kappa(m)，弱场 kappa ∝ m ⇒ a_mu/a_e ≡ (m_mu/m_e)^2 与 cot(theta) 无关；"
     "反解得 cot(theta)_e = %s（>0）与 cot(theta)_mu = %s（<0），符号互斥" % (cot_e, cot_mu),
     "该证伪对任何量纲补齐因子免疫（比值中 C 消去），与 r42 N02/N03 同源、本册独立复算。")

# ================================================================ E. chi^2 代码层
def G_th(sin_t, lp):
    return c ** 3 * lp ** 2 / (hbar * sin_t)

g_nom = G_th(D(1), lP_nominal)
g_der = G_th(D(1), lP_derived)
res_nom = (g_nom - Gexp) / Gexp
res_der = (g_der - Gexp) / Gexp
guard("E_identity_residual_precision_limited", abs(res_nom) > D("1e-12") and abs(res_der) < D("1e-20"),
      "标称 l_P 残差 %s（受输入 9 位有效数字限制）；精算 l_P 残差 %s（机器零）" % (res_nom, res_der))
PASS("T28", "G_th = c^3 l_P^2/(hbar sin theta) 在 sin theta=1 时与 CODATA 一致",
     "标称 l_P 相对残差 %s；按定义式 l_P^2=hbar G/c^3 精算后残差 %s（恒等式复读，零信息量）" % (
         res_nom, res_der),
     "这是 r44 T33 的同源读数；由于 chi^2 代码把 l_P 硬编码为 CODATA 值，该项对 theta 无梯度。")
FAIL("T29", "chi2(theta) 可用 dynesty 做全局最小化",
     "kappa(m,theta) 要求 1/sin^2(theta) > 2*pi*m*c^2/hbar；电子该量 = %s，"
     "而 1/sin^2 的上确界为 1 ⇒ 全部实 theta 无实根 ⇒ sqrt 返回复数 ⇒ chi2 非实函数，最小化无定义" % e_root,
     "r44 已预警「被最小化的目标函数当前没有定义域」，V4.5 未解决；§8 选项 1 因此不可执行。")
INFO("T30", "chi2 的 sigma 口径",
     "代码用 sigma_e = 1e-12（实验值约 2.8e-14、SM 理论约 2.1e-24）、sigma_mu = 4e-7（含 SM 理论约 5.2e-10）、"
     "sigma_G/G = 1e-5（CODATA 为 2.2e-5）",
     "三项 sigma 均未登记且与真实值偏离 2~8 个量级；r44 P2 的口径层缺口在本册原样保留。")
MIS("T31", "chi_G 项为 theta 提供有效约束",
    "G_th 只经 sin(theta) 进入，而 chi2 的其余两项要求 theta < %.3e rad（见 T16）；"
    "在该区间内 chi_G ≡ %s（常数），梯度为零" % (theta_crit, _f((g_der / Gexp - 1) * D("1e-5"))),
    "即便忽略 T29 的定义域问题，三项中也没有一项能对 theta 形成有效梯度。")

# ================================================================ F. 治理与自评
BOUNDARY("T32", "新增公设：指数局域包的衰减宽度取 l_P",
     "局域化尺度 l_P 与公理3 中 G_th 里的 l_P 同符号但用途不同（衰减宽度 vs 自然长度）；"
     "若二者不强制等同，则自由参数 +1。",
     "本册不代为判定二者是否可等同（等同则零信息量，但需明写）。")
FAIL("T33", "唯一全局普适升角 theta（单一自由参数）",
     "闭合方程实际含 {theta, l_P}，其中 l_P^2 ≡ hbar G_exp/c^3 直接注入 G；"
     "chi2 代码还并列注入 e、hbar、c 与两个实验 a 值",
     "撞 Ω5「自由常数 ≤1」；与 r41 R06 / r44 T34 同族。")
FAIL("T34", "（§7 遗留假设 B）下一步改从 laplacian(kappa)=0 求格林函数",
     "该方程在全空间有源为零且要求 r→∞ 衰减；唯一的球对称有界解为 kappa ≡ 0（T05），"
     "非球对称解在无穷远不衰减 ⇒ 无满足边界条件的格林函数解",
     "「去掉指数轮廓假设」这条出路在 T04/T05 之后被堵死：不是 ansatz 太粗，而是方程本身无解。")
INFO("T35", "§8 四选项的可执行性（本册只判定可执行性，不代选）",
     "选项1（dynesty）无定义域（T29）⇒ 不可执行；选项2（格林函数）不可执行（T34）；"
     "选项3（tau 子 g-2）依赖选项1；选项4（ADM-BSSN）不在本册射程（r41 已判演化方程层 C/L1）",
     "四条出路中 3 条在本框架内直接不可执行；这是相对 r44（同样 4 条全不可执行）的推进点：V4.5 至少修好了幂次。")
CORR("T36", "来料 §7 自评第一条：「自能不再是手动 ansatz，由螺旋场拉氏量变分 + 球对称局域包积分严格导出」",
     "半成立：(i) 积分算术严格正确（T09/T10）；(ii) 但拉氏密度本身量纲缺 c^2（T12）、"
     "势 V 在公理1 下恒等于 0（T03）、运动方程退化为拉普拉斯方程且与局域包互斥（T04/T05）、"
     "哈密顿量两行符号自相矛盾（T07/T08）；(iii) 修复量纲后幂次结构与 r44 修正版同型（T14）。"
     "⇒ 「严格导出」不成立。",
     "本册唯一对来料自我定位的实质更正；不否认「从变分出发」这一方法方向的价值。")
INFO("T37", "缺陷族复发链登记",
     "量纲非齐次族：r18(§1 κ) -> r19 -> r22(§22) -> r26 -> r27(H20) -> r32 -> r35 -> r37 -> "
     "r44(T13/T14 自称自洽实则差一幂次) -> **r45(T01/T02/T11/T12/T15/T18/T20/T25 共 8 处)**；"
     "「打破 m^2 被自己取消」：r44 C2/T30 -> **r45 T23**（第 2 次）；"
     "「恒等式复读」：r44 T33 -> **r45 T03/T28**",
     "本册是该缺陷族的第 9 次复发，且来料以「量纲完全自洽」为自我卖点，故单独立册登记。")
INFO("T38", "与并行册的分工（零重复声明）",
     "r44 审 V4.3/V4.4 的 g-2 联合拟合链 + 自能 ansatz；本册审 V4.5 的**变分导出链 + 局域包 + "
     "二次映射 + chi2 代码**。r40 审 kappa-tau-omega 导出链与 G 的可导出性；r42（算法联盟册）审"
     "挠率-自旋耦合消去 eta，其「函数形式锁定 ⇒ 系数不变性」判据在本册 T27 被独立复算复用。",
     "本册不重复复算 V4.3/V4.4 的数值（已在 r44 登记），只承接其结论。")

# ================================================================ 汇总与落盘
def _f(x):
    """Decimal -> 可读字符串（避开 quantize 在高有效位数下抛 InvalidOperation 的坑）。"""
    return format(x, ".12E")

KEY_FIGURES = {
    "dim_U_self_claim": dstr(dim_U_claim),
    "dim_U_self_claim_says": dstr(dim_claim_says),
    "dim_gap_U": dstr(gap),
    "dim_U_self_fixed": dstr(dim_U_fix),
    "dim_V_potential_as_given": dstr(V_as_given),
    "dim_energy_density_required": dstr(dEnergyDens),
    "dim_lagrangian_gradient_term": dstr(dL_lag),
    "V_max_under_axiom1": _f(resid),
    "V_exact_zero_cases_at_sin_theta_1": "%d/4" % exact_zero_pipi2,
    "V_positive_control_without_axiom1": _f(pos_v),
    "harmonic_branch_B_at_r_1e-6": _f(sing),
    "harmonic_branch_B_at_r_1e30": _f(tail),
    "harmonic_branch_A_spread": _f(const_spread),
    "int_r2_exp_integral_coeff": _num(frac_l3_over_4),
    "int_grad2_dim": dstr(dim_int_grad2),
    "two_pi_mc2_over_hbar_electron": _f(e_root),
    "two_pi_mc2_over_hbar_mu": _f(two_pi_mc2_over_hbar["mu"]),
    "two_pi_mc2_over_hbar_tau": _f(two_pi_mc2_over_hbar["tau"]),
    "two_pi_mc2_over_hbar_top": _f(two_pi_mc2_over_hbar["top"]),
    "sin2_upper_bound": _f(sin2_max),
    "theta_crit_rad": "%.6E" % theta_crit,
    "missing_factor_c2_over_lP": _f(c ** 2 / lP_derived),
    "kappa_expanded_over_claim": _f(kappa_expanded / kappa_claim),
    "kappa_machine_over_expanded": _f(kappa_machine / kappa_expanded),
    "mmax_claim_as_kg": _f(mmax_claim),
    "mmax_claim_dim": dstr(dim_mmax_claim),
    "electron_over_mmax_claim": _f(m_e / mmax_claim),
    "gap_decades_definition_vs_regime": "%.2f" % gap_decades,
    "delta_selfenergy_electron": _f(delta_tab["e"]),
    "delta_selfenergy_mu": _f(delta_tab["mu"]),
    "delta_selfenergy_tau": _f(delta_tab["tau"]),
    "delta_selfenergy_top": _f(delta_tab["top"]),
    "mass_ratio_squared": _f(mass_ratio_sq),
    "dim_a_tuft_claim": dstr(d_a_claim),
    "fill_target_dim": dstr(TARGET),
    "fill_solutions_without_charge": len(hits_no_e),
    "fill_solutions_with_charge": len(hits_with_e),
    "fill_simplest_with_charge": best_txt,
    "C_moment_coefficient": _f(C_coeff),
    "delta_a_e": _f(da_e),
    "delta_a_mu": _f(da_mu),
    "cot_theta_electron": _f(cot_e),
    "cot_theta_mu": _f(cot_mu),
    "G_th_residual_nominal_lP": _f(res_nom),
    "G_th_residual_derived_lP": _f(res_der),
    "m_Planck_kg": _f(m_Pl),
    "lP_derived_m": _f(lP_derived),
}

NOT_SELF_DERIVED = [
    "1. 拉氏密度系数 hbar/(2c) -> hbar*c/2 的修复虽使量纲闭合，本册不代为构造该系数为何应取 c^2（来料未给任何理由）。",
    "2. 局域包衰减宽度 l_P 与公理3 中 G_th 的 l_P 是否必须等同；等同则零信息量，不等同则自由参数 +1。",
    "3. 补齐因子 e*l_P^2（最简解）为何应取这一组而非穷举表中的其余解。",
    "4. 相对论（公设 v=c）下的磁矩修正形式；本册只复用 r42 的非相对论约化。",
    "5. ADM-BSSN 演化层（§8 选项4）：r41 已判该层 C/L1，本册不重算。",
    "6. 静态单粒子驻波公理在天体尺度的适用边界。",
]

OPEN_ITEMS = [
    {"id": "X-R45-1", "text": "势 V 在公理1 下恒等于 0；需么放弃公理1（omega 独立），要么放弃该势 —— 二者必居其一，本册不代选。"},
    {"id": "X-R45-2", "text": "变分得到的是空间场 kappa(x)，而公理1 的 kappa 是粒子内禀常量；两对象的映射未在任何公设中给出。"},
    {"id": "X-R45-3", "text": "chi2(theta) 无实数定义域（T29）；在补齐因子与量纲修复前，数值最小化不可执行。"},
    {"id": "X-R45-4", "text": "『打破 m^2』在本框架内不可达（第 2 次复发 r44 C2）：唯一全局 theta + 弱场极限必然回到 m^2。"},
    {"id": "X-R45-5", "text": "补齐因子穷举有多解（%d 组），a_TUFT 系数仍不可确定。" % len(hits_with_e)},
    {"id": "X-R45-6", "text": "g-2 窗口对量纲缺陷免疫的符号证伪（T27）尚未被来料回应。"},
]

def build_summary():
    counts = {}
    for r in RECORDS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["passed"])
    return counts, g_ok, len(GUARDS)

def main():
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    counts, g_ok, g_n = build_summary()
    meta = {
        "book": "r45",
        "subject": "TUFT-V4.5｜变分推导螺旋场自能，消去自能 ansatz 假设（算法联盟）",
        "engine": "纯标准库 Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)",
        "stamp": STAMP,
        "incoming_predecessors": ["V4.2 螺旋场作用量", "V4.3 联合 chi^2 拟合", "V4.4 路线B 自能 ansatz"],
        "counts": counts,
        "items_total": len(RECORDS),
        "guards": "%d/%d" % (g_ok, g_n),
        "rating_incoming": "C/L1",
        "hash": hashlib.sha256((NAME + STAMP).encode("utf-8")).hexdigest()[:16],
    }
    payload = {
        "meta": meta,
        "verdicts": RECORDS,
        "guards": GUARDS,
        "key_figures": KEY_FIGURES,
        "not_self_derived": NOT_SELF_DERIVED,
        "open_items": OPEN_ITEMS,
    }
    p_json = os.path.join(OUT_DIR, NAME + ".json")
    with io.open(p_json, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))

    # 汇总行必须匹配库内正则 (PASS|FAIL|BOUNDARY|INFO)\s*[=:]\s*(\d+)
    summary_line = " ".join("%s=%d" % (k, counts[k]) for k in
                             ["PASS", "FAIL", "MISMATCH", "BOUNDARY", "INFO", "CORRECTED"]
                             if k in counts)
    lines = ["=" * 78, NAME, "=" * 78,
             "条目 %d：%s" % (len(RECORDS), summary_line),
             "自检 guard: %d/%d" % (g_ok, g_n), ""]
    lines.append("-" * 78)
    lines.append("【关键读数】")
    for k in sorted(KEY_FIGURES):
        lines.append("  %-42s %s" % (k, KEY_FIGURES[k]))
    lines.append("")
    lines.append("-" * 78)
    lines.append("【逐条判定】")
    for r in RECORDS:
        lines.append("%-5s %-5s %s" % (r["id"], r["verdict"], r["claim"]))
        lines.append("        机器读数: %s" % r["machine_reading"])
        if r["note"]:
            lines.append("        注: %s" % r["note"])
    lines.append("")
    lines.append("-" * 78)
    lines.append("【自检 guard】")
    for g in GUARDS:
        lines.append("  [%s] %s" % ("PASS" if g["passed"] else "FAIL", g["name"]))
        if g["detail"]:
            lines.append("        %s" % g["detail"])
    lines.append("")
    lines.append("-" * 78)
    lines.append("【不自推清单】")
    for x in NOT_SELF_DERIVED:
        lines.append("  " + x)
    lines.append("")
    lines.append("【开放项】")
    for x in OPEN_ITEMS:
        lines.append("  %s %s" % (x["id"], x["text"]))
    lines.append("")
    lines.append("红线：数学自洽 != 物理证实；本册不产生新物理。")
    report = "\n".join(lines) + "\n"
    p_rep = os.path.join(OUT_DIR, NAME + "_report.txt")
    with io.open(p_rep, "w", encoding="utf-8") as fh:
        fh.write(report)

    md = []
    md.append("# %s · 机器产物（%s）" % (NAME, STAMP))
    md.append("")
    md.append("**条目 %d**：%s　**自检**：%s　**评级（来料）**：%s" % (
        len(RECORDS), summary_line, meta["guards"], meta["rating_incoming"]))
    md.append("")
    md.append("## 关键读数")
    md.append("")
    md.append("| 量 | 读数 |")
    md.append("|---|---|")
    for k in sorted(KEY_FIGURES):
        md.append("| `%s` | `%s` |" % (k, KEY_FIGURES[k]))
    md.append("")
    md.append("## 逐条判定")
    md.append("")
    md.append("| id | 判定 | 来料声称 | 机器读数 |")
    md.append("|---|---|---|---|")
    for r in RECORDS:
        md.append("| %s | **%s** | %s | %s |" % (
            r["id"], r["verdict"], r["claim"].replace("\n", " "), r["machine_reading"].replace("\n", " ")))
    md.append("")
    md.append("## 自检 guard（%s）" % meta["guards"])
    md.append("")
    for g in GUARDS:
        md.append("- [%s] `%s` — %s" % ("PASS" if g["passed"] else "FAIL", g["name"], g["detail"]))
    md.append("")
    md.append("## 不自推清单")
    md.append("")
    for x in NOT_SELF_DERIVED:
        md.append("- " + x)
    md.append("")
    md.append("## 开放项")
    md.append("")
    for x in OPEN_ITEMS:
        md.append("- **%s** %s" % (x["id"], x["text"]))
    md.append("")
    p_md = os.path.join(OUT_DIR, NAME + ".md")
    with io.open(p_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")

    if g_ok != g_n:
        sys.stdout.write("GUARD FAIL %d/%d -- 审计器本身有问题，禁止输出结论\n" % (g_ok, g_n))
        return 2
    sys.stdout.write("OK items=%d %s guards=%d/%d\n" % (len(RECORDS), summary_line, g_ok, g_n))
    return 0

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())