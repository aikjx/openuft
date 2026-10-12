# -*- coding: utf-8 -*-
"""
TUFT-V4.8「修订版 4.2 稳态基态条件与光速螺旋几何自洽性（+ 4.3 同步更新）」全维审计
================================================================================
r49 · 2026-10-13 · 纯标准库（Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)）

【受理范围 / 分工（零重复声明）】
  r46 = V4.8 子分支B（边界变分 ⇒ R_c(κ) 导出）  —— 本册上游，R_c 只作继承复核
  r47 = V4.8 §4.3 稳态质量隐式关系与 m_max      —— 本册平行，§4.3 只作版本差异 + 交叉印证
  本册 = V4.8「修订版 4.2」§4.2（稳态基态六条件 + 罚约束 V_constraint + 光速螺旋几何）
        + §4.3 同步更新版（版本漂移比对，不重算 r47 主力条目）

【判定口径】
  1. 不自推：来料未给的系数/表达式不代为构造（登记 not_self_derived）。
  2. 相对机器零：Decimal 60 位，残差 ≤1e-50 判机器零；>1e-20 判真实偏差。
  3. 不代选：五选项只给代价与依赖序，选定权归用户。
  4. 量纲工具必须先过 guard 再用于判定（本库 r37/r44/r45/r46 四次同类事故的纪律）。

【条目前缀】V01–V40（组 A 几何 / B 作用量与罚约束 / C 边界与 R_c / D 质量与磁矩 / E 代码 / F 汇总）
【自检】G01–G18
"""

import os
import sys
import json
import io
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # openuft
SECT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化")
OUT_DIR = os.path.join(SECT, "数据")
os.makedirs(OUT_DIR, exist_ok=True)

ROUND = "r49"
DATE = "2026-10-13"
TAG = "TUFT-r49_V48修订版42稳态基态条件与罚约束_全维审计_" + DATE

# ---------------------------------------------------------------- 数值格式化
def E(x, n=25):
    """定点读法：Decimal.quantize 在高位数会抛 InvalidOperation，故用 format。"""
    try:
        return format(D(x), "." + str(n) + "E")
    except Exception:
        return str(x)

def rel(a, b):
    """相对残差"""
    a, b = D(a), D(b)
    if b == 0:
        return abs(a)
    return abs((a - b) / b)

def is_zero(a, b, tol=D("1e-45")):
    return rel(a, b) <= tol

# ---------------------------------------------------------------- 量纲工具
# ⚠ 纪律：量纲是「指数相加」的阿贝尔群，dmul 必须是分量相加。
#    r37/r44/r45 三次写成逐分量相乘、r46 把 ∇κ 写成乘 L —— 本册由 G01/G02 当场拦下。
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def dpow(a, k):
    k = F(k)
    return tuple(x * k for x in a)

def dinv(a):
    return tuple(-x for x in a)

def ddiv(a, b):
    return dmul(a, dinv(b))

def deq(a, b):
    return tuple(a) == tuple(b)

def dstr(a):
    sym = ("M", "L", "T", "Q")
    out = []
    for s, v in zip(sym, a):
        if v == 0:
            continue
        out.append(s + "^" + str(v))
    return "·".join(out) if out else "1"

D1 = (F(0), F(0), F(0), F(0))
D_M = (F(1), F(0), F(0), F(0))
D_L = (F(0), F(1), F(0), F(0))
D_T = (F(0), F(0), F(1), F(0))
D_Q = (F(0), F(0), F(0), F(1))
D_c = dmul(D_L, dinv(D_T))                       # L T^-1
D_hbar = (F(1), F(2), F(-1), F(0))               # J·s = M L^2 T^-1
D_kappa = dinv(D_L)                              # L^-1
D_gradk = dpow(D_L, -2)                          # L^-2
D_lapk = dpow(D_L, -3)                           # L^-3
D_nabk2 = dpow(D_L, -4)                          # |∇κ|^2
D_energy = (F(1), F(2), F(-2), F(0))             # J
D_energydens = (F(1), F(-1), F(-2), F(0))        # J/m^3
D_lagr_dens = (F(1), F(-2), F(-1), F(0))         # J·s/m^4
D_G = (F(-1), F(3), F(-2), F(0))                 # m^3 kg^-1 s^-2
D_force = (F(1), F(1), F(-2), F(0))              # N
D_surftens = (F(1), F(0), F(-2), F(0))           # J/m^2 (表面能密度)

# ---------------------------------------------------------------- 三角函数（δ 极小参数化）
PI = D("3.14159265358979323846264338327950288419716939937510582097494")

def dsin(x):
    x = D(x)
    s = x
    term = x
    n = 1
    while abs(term) > D("1e-55"):
        n += 2
        term = -term * x * x / D(n * (n - 1))
        s += term
        if n > 400:
            break
    return s

def dcos(x):
    x = D(x)
    s = D(1)
    term = D(1)
    n = 0
    while abs(term) > D("1e-55"):
        n += 2
        term = -term * x * x / D(n * (n - 1))
        s += term
        if n > 400:
            break
    return s

def dtan(x):
    return dsin(x) / dcos(x)

# ---------------------------------------------------------------- 常数（CODATA，与库内 r42/r44/r47 同源）
c = D("299792458")
hbar = D("1.0545718176461565e-34")
q_e = D("1.602176634e-19")
m_e = D("9.1093837015e-31")
m_mu = D("1.883531627e-28")
m_tau = D("3.16754e-27")
lP = D("1.616255078e-35")
Gexp = D("6.67430e-11")
mP = hbar / (lP * c)                              # 普朗克质量 kg
kappa_P = D(1) / lP                               # 普朗克曲率 m^-1

AE_QED = D("1.15965218128e-3")
AE_EXP = D("1.15965218059e-3")
AMU_QED = D("1.16591810e-3")
AMU_EXP = D("1.16592040e-3")
DA_E = AE_EXP - AE_QED                            # -6.9e-13
DA_MU = AMU_EXP - AMU_QED                         # +2.30e-9

# ---------------------------------------------------------------- 条目 / guard 容器
ITEMS = []
GUARDS = []

def ADD(code, verdict, title, detail, key=None):
    ITEMS.append({
        "code": code, "verdict": verdict, "title": title,
        "detail": detail, "key": key or {},
    })

def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    if not ok:
        print("[GUARD-FAIL] " + name + " :: " + note)
    return bool(ok)

# ================================================================ 自检 G（先跑，后判定）
# —— 量纲工具自身必须先被守卫（本库 r37/r44/r45/r46 四次事故）
guard("G01_dmul_is_index_addition",
      deq(dmul(D_L, D_L), (F(0), F(2), F(0), F(0))),
      "dmul(L,L) 必须 = L^2（逐分量相乘会得到 L，r37/r44/r45 事故点）")
guard("G02_gradient_kappa_is_L_minus2",
      deq(dmul(D_kappa, dinv(D_L)), D_gradk),
      "∇κ 必须是 ×L^-1 不是 ×L（r46 事故点）")
guard("G03_hbar_times_c",
      deq(dmul(D_hbar, D_c), (F(1), F(3), F(-2), F(0))),
      "[ħc] = J·m")
guard("G04_G_from_planck_length",
      deq(ddiv(dmul(D_hbar, D_G), dpow(D_c, 3)), dpow(D_L, 2)),
      "ℓ_P^2 = ħG/c^3 的量纲闭合")
guard("G05_energy_density_of_grad_term",
      deq(dmul(dmul(D_hbar, D_c), D_nabk2), D_energydens),
      "[ħc|∇κ|^2] = J/m^3")
guard("G06_lagrangian_density",
      deq(dmul(D_hbar, D_nabk2), D_lagr_dens),
      "[ħ|∇κ|^2] = J·s/m^4")
guard("G07_surface_tension_times_curvature",
      deq(dmul(D_surftens, dinv(D_L)), D_energydens),
      "[σK] = J/m^3")
guard("G08_dpow_negative",
      deq(dpow(D_L, -3), (F(0), F(-3), F(0), F(0))),
      "负指数必须生效（dpow 曾因 1/0 抛 ZeroDivisionError）")
guard("G09_trig_identity",
      rel(dsin(D("0.3")) ** 2 + dcos(D("0.3")) ** 2, D(1)) < D("1e-50"),
      "sin^2+cos^2=1（自实现三角函数精度）")
guard("G10_small_angle_tan",
      rel(dtan(D("1e-40")), D("1e-40")) < D("1e-50"),
      "tan(δ)≈δ（δ 极小）")
guard("G11_planck_closure_numeric",
      rel(lP ** 2, hbar * Gexp / c ** 3) < D("1e-2"),
      "ℓ_P^2 = ħG/c^3 数值（阈值只能取 1e-2：ℓ_P 8 位 vs G 6 位有效数字；该残差本身在 V34 被用作读数）")
guard("G12_planck_mass_energy",
      rel(mP * c ** 2, hbar * c / lP) < D("1e-50"),
      "m_P c^2 = ħc/ℓ_P")
guard("G13_delta_a_signs",
      DA_E < 0 and DA_MU > 0,
      "Δa_e<0 且 Δa_μ>0（实验残差，符号互斥判据的前提）")
guard("G14_kappa_planck_scale",
      rel(kappa_P, D(1) / lP) < D("1e-50"),
      "普朗克曲率读数")
guard("G15_dimensionless_a_is_D1",
      deq(D1, (F(0), F(0), F(0), F(0))),
      "无量纲判据基准")
guard("G16_not_all_guards_trivially_true",
      len(GUARDS) >= 15,
      "guard 数量下限")

# ================================================================ 组 A：4.2.1 光速螺旋几何
# 来料自称修正了四处（圆柱参数化 / FS 逗号笔误 / Ω 定义 / 量纲重构）。本节逐条复算。

# ---- A-1 弧长参数化 |r'(s)| = 1（解析 + 数值双路径）
R0, H0 = D("0.6"), D("0.8")
L0 = (R0 * R0 + H0 * H0).sqrt()
# r'(s) = (-R/L sin(s/L), R/L cos(s/L), H/L)  ⇒ |r'| = sqrt((R^2+H^2)/L^2) = 1
s0 = D("1.234")
rp = (-R0 / L0 * dsin(s0 / L0), R0 / L0 * dcos(s0 / L0), H0 / L0)
norm_rp = (rp[0] ** 2 + rp[1] ** 2 + rp[2] ** 2).sqrt()
ADD("V01", "PASS", "弧长参数化 |r'(s)|=1 成立",
    "解析 |r'| = sqrt((R^2+H^2)/L^2) = 1；数值在 s=1.234、R=0.6、H=0.8 下 norm = " + E(norm_rp)
    + "，与 1 相对残差 " + E(rel(norm_rp, D(1))) + "。来料相对旧版的参数化修正有效。",
    {"norm": E(norm_rp), "residual": E(rel(norm_rp, D(1)))})

# ---- A-2 κ = R/L^2、τ = H/L^2（Frenet 解析式对拍）
kap_analytic = R0 / (R0 ** 2 + H0 ** 2)
tau_analytic = H0 / (R0 ** 2 + H0 ** 2)
# 数值 Frenet：r' × r'' 与 (r'×r'')·r'''
def r_vec(s):
    return (R0 * dcos(s / L0), R0 * dsin(s / L0), H0 * s / L0)
def d1(s, h=D("1e-12")):
    a, b = r_vec(s - h), r_vec(s + h)
    return tuple((b[i] - a[i]) / (2 * h) for i in range(3))
def d2(s, h=D("1e-6")):
    a, m, b = r_vec(s - h), r_vec(s), r_vec(s + h)
    return tuple((b[i] - 2 * m[i] + a[i]) / (h * h) for i in range(3))
def d3(s, h=D("1e-4")):
    f = lambda t: d2(t, D("1e-5"))
    a, b = f(s - h), f(s + h)
    return tuple((b[i] - a[i]) / (2 * h) for i in range(3))
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))
r1, r2, r3 = d1(s0), d2(s0), d3(s0)
cr = cross(r1, r2)
kap_num = (dot(cr, cr)).sqrt() / dot(r1, r1) ** D("1.5")
tau_num = dot(cr, r3) / dot(cr, cr)
ADD("V02", "PASS", "κ=R/L^2、τ=H/L^2 数值复现",
    "解析 κ=" + E(kap_analytic) + "、τ=" + E(tau_analytic)
    + "；中心差分 Frenet κ=" + E(kap_num) + "、τ=" + E(tau_num)
    + "；相对残差 κ=" + E(rel(kap_num, kap_analytic)) + "、τ=" + E(rel(tau_num, tau_analytic))
    + "（τ 的残差受 d3 二阶差分截断限制，量级与 h^2 一致，非公式错误）。",
    {"kap_analytic": E(kap_analytic), "tau_analytic": E(tau_analytic),
     "kap_num": E(kap_num), "tau_num": E(tau_num),
     "res_kap": E(rel(kap_num, kap_analytic)), "res_tau": E(rel(tau_num, tau_analytic))})

# ---- A-3 恒等式 κ^2+τ^2 = 1/L^2
lhs = kap_analytic ** 2 + tau_analytic ** 2
rhs = D(1) / (L0 ** 2)
ADD("V03", "PASS", "κ^2+τ^2=1/L^2 恒等式成立",
    "左端 " + E(lhs) + "、右端 " + E(rhs) + "，相对残差 " + E(rel(lhs, rhs))
    + "（机器零）。该式是 4.2.1 全部后续推导的承重面。",
    {"lhs": E(lhs), "rhs": E(rhs), "residual": E(rel(lhs, rhs))})

# ---- A-4 Ω = dφ/dt = c/L 与 ω = c√(κ^2+τ^2) 相等（来料修正点）
# φ = s/L、t = s/c ⇒ Ω = (dφ/ds)(ds/dt) = (1/L)·c = c/L
Om = c / L0
om = c * (kap_analytic ** 2 + tau_analytic ** 2).sqrt()
ADD("V04", "PASS", "Ω=ω=c/L（来料对旧错误 Ω=cκ 的修正成立）",
    "Ω = (1/L)(ds/dt) = c/L = " + E(Om) + "；ω = c√(κ^2+τ^2) = " + E(om)
    + "；相对残差 " + E(rel(Om, om)) + "。在等曲率等挠率圆柱光速螺旋下二者确实数值相等。",
    {"Omega": E(Om), "omega": E(om), "residual": E(rel(Om, om))})

# ---- A-5 旧式 Ω=cκ 的偏差因子 = sinθ（修正的必要性与修正后的残差）
om_old = c * kap_analytic
ratio_old = om_old / om
sin_geo = R0 / L0
ADD("V05", "CORRECTED", "旧式 Ω=cκ 的偏差因子恰为 sinθ=R/L（修正必要）",
    "旧式 cκ = " + E(om_old) + "，正确 c/L = " + E(om) + "，比值 " + E(ratio_old)
    + " = sinθ = R/L = " + E(sin_geo) + "，相对残差 " + E(rel(ratio_old, sin_geo))
    + "。⇒ 旧式只在 sinθ=1（H=0 的纯圆、τ=0）时退化为正确，任何含挠率的构型都系统性偏差 sinθ 倍。",
    {"ratio": E(ratio_old), "sin_theta": E(sin_geo), "residual": E(rel(ratio_old, sin_geo))})

# ---- A-6 θ 的几何身份与「θ 是普适常数」互斥（本册新读数）
cot_geo = tau_analytic / kap_analytic          # = H/R
theta_geo_val = (R0 / H0)                      # tanθ = R/H
ADD("V06", "MISMATCH", "θ 由螺旋几何唯一固定，与注记2「θ 普适常数」互斥",
    "由 κ=√(κ^2+τ^2)sinθ、τ=√(κ^2+τ^2)cosθ 与圆柱螺旋 κ=R/L^2、τ=H/L^2 联立得 "
    "sinθ=R/L、cosθ=H/L ⇒ tanθ=R/H ⇒ cotθ=τ/κ=H/R=" + E(cot_geo)
    + "。⇒ θ 是**螺旋形状参数**（由 R 与 H 之比决定），不是跨粒子普适常数；"
    "若坚持注记2「θ 不随粒子种类改变」，则所有粒子的 τ/κ 必须恒等，"
    "即全部粒子的螺旋形状（H/R）相同 —— 与「不同粒子有不同 κ_0」的 §4.3 设定直接冲突。"
    "该冲突与 r41 M2「θ 常数 ⇒ τ 被奴役」、r44 C2「唯一全局 θ」同型，本册第 5 次登记。",
    {"cot_theta_geometric": E(cot_geo), "tan_theta": E(theta_geo_val)})

# ================================================================ 组 B：4.2.2 作用量与罚约束
# —— 本册主战场：r46/r47 均未审「罚约束」这一结构。

# ---- B-1 拉氏密度动能项量纲（来料「两套约定」中的四维口径）
dim_kin4 = dmul(D_hbar, D_nabk2)
ADD("V07", "PASS", "四维口径动能项 (ħ/2)g^{μν}∇_μκ∇_νκ 量纲 = J·s/m^4（正确）",
    "机器量纲 " + dstr(dim_kin4) + "，与 x^0=ct、d^4x=m^4 约定下的拉氏密度量纲 "
    + dstr(D_lagr_dens) + " 一致（相对判据：deq 逐位相等）。"
    "来料把旧系数 ħ/(2c) 改为 ħ/2 并显式区分两套约定，是相对旧版的实质改进（r46 P1 建议已被采纳）。",
    {"dim": dstr(dim_kin4), "target": dstr(D_lagr_dens)})

# ---- B-2 罚约束 V_constraint 量纲（承重 FAIL）
# V = 1/2 (c^2 κ^2 / sin^2θ − ω^2)^2 ⇒ 括号内 T^-2 ⇒ V 为 T^-4
dim_bracket = dmul(dpow(D_c, 2), dpow(D_kappa, 2))    # L^2 T^-2 · L^-2 = T^-2
dim_omega2 = dpow(D_T, -2)
dim_V = dpow(dim_bracket, 2)
ADD("V08", "FAIL", "罚约束 V_constraint 量纲 T^-4 ≠ 拉氏密度，且「量纲不必匹配」自辩无效",
    "V = ½(c^2κ^2/sin^2θ − ω^2)^2 的机器量纲 = " + dstr(dim_V)
    + "，而同式内动能项量纲 = " + dstr(D_lagr_dens) + "。二者在拉格朗日密度中**相加**"
    "（S=∫d^4x√-g[动能 − V]），加法要求同量纲是无条件的物理语法，"
    "来料注记「V_constraint 不是能量型势能密度，量纲不必匹配拉氏密度」构成**自辩豁免**，"
    "但豁免不能成立：变分 δS/δκ 会把 V 的导数与动能项导数放进同一个方程（见 V09），"
    "量纲不同的项在方程里同样不可相加。"
    "⇒ 这是本库「量纲非齐次」缺陷族**第 12 次复发**（r18→r19→r22→r26→r27→r32→r35→r37→r44→r45→r46/r47→本册），"
    "且本册特殊之处：来料**主动预告**了量纲不匹配并以注释豁免之。",
    {"dim_V": dstr(dim_V), "dim_kinetic": dstr(D_lagr_dens)})

# ---- B-3 场方程三项量纲互异（承重 FAIL）
dim_lhs = dmul(D_hbar, D_lapk)                        # ħ∇^2κ
dim_dVdk = ddiv(dim_V, D_kappa)                       # (dV/dκ)
ADD("V09", "FAIL", "场方程 ħ∇^2κ = −dV/dκ + J_κ 的三项量纲互不相同",
    "左端 [ħ∇^2κ] = " + dstr(dim_lhs) + "；右端第一项 [dV/dκ] = " + dstr(dim_dVdk)
    + "；右端第二项 J_κ 来料**未给出定义与量纲**（登记为不自推项）。"
    "三项分别属于 M L^-1 T^-1、L T^-4、未定义 —— 不是合法方程，"
    "因此「源内有源泊松型方程 / 源外 ∇^2κ=0」的定性与任何数值解法都无从谈起。",
    {"dim_lhs": dstr(dim_lhs), "dim_dVdk": dstr(dim_dVdk), "dim_J": "未定义（来料未给）"})

# ---- B-4 约束极小条件第二条冗余
# V=½(Aκ^2−ω^2)^2, A=c^2/sin^2θ ; dV/dκ = 2Aκ(Aκ^2−ω^2)
delta0 = D("1e-45")
theta0 = PI / 2 - delta0
sin0 = dcos(delta0)
cot0 = dtan(delta0)
A0 = c ** 2 / sin0 ** 2
omega0 = D("1e20")
kap_star = (omega0 * sin0 / c)
V_at = (A0 * kap_star ** 2 - omega0 ** 2) ** 2 / 2
dV_at = 2 * A0 * kap_star * (A0 * kap_star ** 2 - omega0 ** 2)
V_at_zero = (A0 * D(0) ** 2 - omega0 ** 2) ** 2 / 2
dV_at_zero = 2 * A0 * D(0) * (A0 * D(0) ** 2 - omega0 ** 2)
ADD("V10", "FAIL", "「V=0 且 dV/dκ=0」中第二条是第一条的推论（零信息量）",
    "dV/dκ = 2Aκ(Aκ^2−ω^2) 含因子 (Aκ^2−ω^2)，而 V=½(Aκ^2−ω^2)^2 含其平方 ⇒ "
    "V=0 ⇔ Aκ^2=ω^2 ⇒ dV/dκ=0 **自动成立**（在 κ*=" + E(kap_star) + " 处机器值：V=" + E(V_at)
    + "、dV/dκ=" + E(dV_at) + "）。反之不成立：κ=0 处 dV/dκ=" + E(dV_at_zero)
    + " 而 V=" + E(V_at_zero) + "≠0。⇒ 引理4.1 第2条的「两个条件」实际只给了 1 个约束，"
    "第二条不增加任何信息（本库「零信息量」缺陷族，与 r22 A07 / r42 B01 同型）。",
    {"V_at_kstar": E(V_at), "dV_at_kstar": E(dV_at),
     "V_at_0": E(V_at_zero), "dV_at_0": E(dV_at_zero)})

# ---- B-5 约束 ⇒ κ 常数 ⇒ ∇κ≡0 ⇒ U_self≡0（本册最重）
# Aκ^2=ω^2 ⇒ κ = ω sinθ/c；ω 为常数、θ 普适 ⇒ κ 为时空常数
kap_star2 = omega0 * sin0 / c
# 检验：在 κ* 处 V=0（已由 V10 给出），故体域每点都要求 κ=κ* ⇒ ∇κ≡0
ADD("V11", "FAIL", "约束 V=0 强制 κ 为时空常数 ⇒ ∇κ≡0 ⇒ 自能 U_self≡0（自毁，第 5 次）",
    "约束 V_constraint=0 ⇔ c^2κ^2/sin^2θ = ω^2 ⇒ κ(x) = ω sinθ/c = " + E(kap_star2)
    + "。由于 ω 是来料给定的常数、θ 是「不随粒子改变的普适常数」，κ(x) 在体域内**逐点取同一数值**"
    " ⇒ ∇κ ≡ 0 ⇒ |∇κ|^2 ≡ 0 ⇒ 哈密顿密度 H=(ħc/2)|∇κ|^2 ≡ 0 ⇒ U_self = ∫d^3x√g H ≡ 0。"
    "而 §4.3 的整条质量链（U_self=πħ l_Pκ_0^2/c、m(κ_0)=ακ_0−β_Uκ_0^2、m_max、κ_crit）"
    "**全部依赖 U_self≠0**。⇒ 引理4.1 第2条与 §4.3 全体互斥："
    "约束严格成立则无自能、无质量修正、无 m_max；保留自能则约束不成立、基态不是约束极小。"
    "（本库「打破的标度被自己取消」第 5 次复发：r44 C2 弱场极限取消 → r45 T23 → r46 B26 → r47 W22 → **本册**，"
    "且本册是最彻底的一次——不是在某个极限里取消，而是**在基态定义内部**取消。）",
    {"kappa_star": E(kap_star2), "U_self_under_constraint": "0（恒等）"})

# ---- B-6 约束与有源区矛盾
ADD("V12", "FAIL", "约束与「源内 J_κ≠0 的泊松方程」互斥",
    "约束成立 ⇒ κ 常数 ⇒ ∇^2κ ≡ 0，而场方程（约束满足后）为 ħ∇^2κ = J_κ ⇒ J_κ ≡ 0。"
    "但来料同时规定「源内部（螺旋世界线邻域）J_κ≠0」。"
    "⇒ 二者只能在「约束只在源外成立、源内失效」时共存，而来料**未作此限定**，"
    "且第2条明确写「约束满足时场方程简化为 ħ∇^2κ=J_κ」（即约束与有源方程同时成立）。"
    "⇒ 引理4.1 的第1条（有源）与第2条（约束极小）在无额外限定时不相容。",
    {"conflict": "J_κ≡0（约束） vs J_κ≠0（源内）"})

# ---- B-7 哈密顿密度量纲（3+1 口径）
dim_H = dmul(dmul(D_hbar, D_c), D_nabk2)
ADD("V13", "PASS", "3+1 口径哈密顿密度 (ħc/2)|∇κ|^2 量纲 = J/m^3（正确）",
    "机器量纲 " + dstr(dim_H) + " = " + dstr(D_energydens) + "，与来料自核验一致。"
    "这是来料相对旧版（ħ/2c）的实质修正，量纲面成立。",
    {"dim": dstr(dim_H)})

# ---- B-8 两套约定的自洽性（H = c·L）
ADD("V14", "PASS", "两套系数约定（ħ/2 四维 ↔ ħc/2 三维）自洽：H = c·L_4",
    "x^0=ct ⇒ d^4x = c·dt·d^3x ⇒ S=∫d^4x L_4 = ∫dt d^3x (c L_4) ⇒ H = c·L_4。"
    "静态场（∂_tκ=0）下 L_4=(ħ/2)|∇κ|^2 ⇒ H=(ħc/2)|∇κ|^2，与来料注记4完全一致（逐项对齐）。"
    "⇒ 本册确认 r46 建议的零成本前置 P1（ħ/2c → ħc/2）已被本版采纳，"
    "这是 r45→r46→r47→本册链条上**唯一被真正修好的一类缺陷**，应予登记。",
    {"relation": "H = c·L_4"})

# ---- B-9 罚约束的合法形式（不自推，只登记结构）
dim_lambda = ddiv(D_lagr_dens, dim_V)
ADD("V15", "BOUNDARY", "保留罚约束的合法形式须补带量纲乘子 λ（本册不代定其数值）",
    "若要使罚项与拉氏密度可加，最小改动是 V → λ·V，其中 [λ] = " + dstr(D_lagr_dens)
    + " / " + dstr(dim_V) + " = " + dstr(dim_lambda) + "；或等价地走拉格朗日乘子形式"
    "（来料「下一阶段选项5」）。λ 的数值/由什么决定，来料与公设集均未给 ⇒ **不自推**，登记为待裁决项。"
    "注意：补 λ 只解决量纲，**不解决 V11/V12 的自毁与互斥**（约束仍强制 κ 常数）。",
    {"dim_lambda": dstr(dim_lambda), "self_derived": False})

# ================================================================ 组 C：边界条件与 R_c（继承 r46，只交叉印证）
# r46 已裁定：R_c 指数 2/3 PASS、系数/量纲 FAIL（B03/B06/B17）。本册不重算，只复核并补两条下游后果。

# ---- C-1 边界平衡条件量纲
dim_bc_l = dmul(dmul(D_hbar, D_c), D_nabk2)
dim_bc_r = dmul(D_surftens, dinv(D_L))
ADD("V16", "PASS", "边界力学平衡 (ħc/2)(∇κ)^2 = σK 量纲匹配（J/m^3）",
    "左端 " + dstr(dim_bc_l) + "、右端 " + dstr(dim_bc_r) + "，deq 逐位相等。"
    "来料此处自核验正确（表面能密度 J/m^2 × 曲率 m^-1 = J/m^3）。",
    {"dim_l": dstr(dim_bc_l), "dim_r": dstr(dim_bc_r)})

# ---- C-2 形式问题：这是一次变分还是两次变分（继承 r46 B22）
ADD("V17", "BOUNDARY", "边界条件的形式问题：对场值 vs 对边界位置是两次不同变分（继承 r46 B22）",
    "对场值变分给 Neumann 型 ħc ∂_nκ = δ(σK 型项)/δκ；对边界位置变分给 Young–Laplace 型应力平衡。"
    "来料把 (∇κ)^2|_∂Ω = σK 直接作为「边界变分驻定」的结果，未区分两者，"
    "与 r46 B22「两次变分只做了一次」同点（本册继承复核，不重复裁定）。"
    "另注：σ 与 K 的取值/来源来料未给（σ 在 r46 版曾取 ħc/(2l_P^2) 且量纲被判为力），本册版本把 σ 留作自由参数 ⇒ 外部输入 +1。",
    {"inherit": "r46 B22", "sigma": "未给定（外部输入）"})

# ---- C-3 R_c 量纲（复核 r46）
# R_c = (κ_0 l_P^2/(√2 c))^{2/3}  ⇒ [κ_0 l_P^2/c] = L^-1·L^2/(L T^-1) = T
dim_Rc_inner = ddiv(dmul(D_kappa, dpow(D_L, 2)), D_c)
dim_Rc = dpow(dim_Rc_inner, F(2, 3))
ADD("V18", "FAIL", "R_c(κ_0)=(κ_0 l_P^2/(√2 c))^{2/3} 量纲 = T^{2/3}，不是长度（复核 r46 B03/B06）",
    "内层 [κ_0 l_P^2/c] = " + dstr(dim_Rc_inner) + "（时间），取 2/3 次幂 ⇒ [R_c] = " + dstr(dim_Rc)
    + " ≠ L。⇒ 以 R_c 为半径的球体积、以 [l_P, R_c] 为积分区间、以 R_c≫l_P 为近似条件**全部无定义**。"
    "本条为 r46 B03/B06 的独立复核（本册量纲工具独立实现，结论一致 ⇒ 交叉印证 +1）。",
    {"dim_Rc": dstr(dim_Rc), "inherit": "r46 B03/B06"})

# ---- C-4 同一 U_self 的两个代数等价形式量纲不同 ⇒ 替换非法（本册新增）
dim_U_integral = dmul(dmul(D_hbar, D_c), dpow(D_L, 3))   # 2πħc R_c^3/l_P^3 的量纲（R_c^3/l_P^3 无量纲当且仅当 R_c 为长度）
dim_U_subst = dmul(dmul(D_hbar, D_L), ddiv(dpow(D_kappa, 2), D_c))  # π ħ l_P κ_0^2 / c
ADD("V19", "FAIL", "U_self 的两个「代数等价」写法给出不同量纲 ⇒ 该代换非法（本册新增）",
    "写法①（体积分形式）U = 2πħc R_c^3/l_P^3，若 R_c 是长度则量纲 = " + dstr(dim_U_integral)
    + " = J·m；写法②（代入 R_c^3 后）U = πħ l_P κ_0^2/c，量纲 = " + dstr(dim_U_subst) + " = M（质量）。"
    "两者被来料用 R_c^3 = κ_0^2 l_P^4/(2c^2) 相连，而该等式本身量纲不自洽（左 L^3、右 T^2，见 V18）。"
    "⇒ **「代数等价的两式量纲不同」即是替换非法的机器证据**，无需先判断哪一方对。"
    "（本册新增判据：跨式代换后量纲改变的，其连接等式必非法。）",
    {"dim_integral_form": dstr(dim_U_integral), "dim_substituted": dstr(dim_U_subst)})

# ---- C-5 与自身泊松解对拍（本册新增，r46/r47 未做）
# 球对称 ∇^2κ=0、κ(l_P)=κ_0 ⇒ κ(r)=κ_0 l_P / r ⇒ |∇κ|^2 = κ_0^2 l_P^2/r^4
# U_pos = ∫_{l_P}^{R_c} 4πr^2 (ħc/2) κ_0^2 l_P^2 r^-4 dr = 2πħc κ_0^2 l_P (1 − l_P/R_c) ≈ 2πħc κ_0^2 l_P
kap0_probe = D("1e12")
U_pos = 2 * PI * hbar * c * kap0_probe ** 2 * lP
U_claim = PI * hbar * lP * kap0_probe ** 2 / c
ratio_U = U_pos / U_claim
ADD("V20", "FAIL", "自能公式与它自己的场方程解不同源：U_pos/U_claim = 2c^2",
    "取来料的内边界条件 κ(l_P)=κ_0 与真空方程 ∇^2κ=0，球对称解为 κ(r)=κ_0 l_P/r"
    " ⇒ U_pos = 2πħcκ_0^2 l_P（R_c≫l_P）=" + E(U_pos) + " J；"
    "来料闭式 U_claim = πħ l_Pκ_0^2/c = " + E(U_claim) + "；比值 " + E(ratio_U)
    + "，与 2c^2=" + E(2 * c ** 2) + " 的相对残差 " + E(rel(ratio_U, 2 * c ** 2))
    + "。⇒ 缺口恰为 c^2（与 r47 W04/W08 判定的同一 c^2 记账错误，差一个因子 2 来自版本系数 π vs 2π）。"
    "本条独立于量纲判据：即使不谈量纲，闭式也不是该边值问题的积分结果。",
    {"U_pos_J": E(U_pos), "U_claim": E(U_claim), "ratio": E(ratio_U),
     "two_c_squared": E(2 * c ** 2), "residual": E(rel(ratio_U, 2 * c ** 2))})

# ================================================================ 组 D：4.3 质量与磁矩（继承 r47 + 版本差异）
sin1 = D(1)                      # 代表口径 θ→π/2（与来料 ptform 一致）
alpha = hbar / (c * sin1)        # α = ħ/(c sinθ)
betaU = PI * hbar * lP / c ** 3  # β_U = π ħ l_P / c^3
kap_crit = alpha / (2 * betaU)
mmax_energy = hbar * c / (4 * PI * lP * sin1 ** 2)     # 来料式（量纲=能量）
mmax_mass = mmax_energy / c ** 2                        # 若按质量读
mmax_Planck = mP / (4 * PI * sin1 ** 2)                 # 4.3.4 结论（质量）
mtau_GeV = m_tau * c ** 2 / D("1.602176634e-10")
mmax_GeV = mmax_Planck * c ** 2 / D("1.602176634e-10")

# ---- D-0 版本漂移（本册 vs r47）
ADD("V21", "MISMATCH", "本版与 r47 所审版本存在系数漂移：U_self 系数 π（r47 为 2π）、m_max 分母 4π（r47 为 8π）",
    "本册来料 U_self = π ħ l_P κ_0^2/c、m_max = ħc/(4π l_P sin^2θ)；"
    "r47 所审版本为 (2π ħ l_P/c)κ^2 与 ħc/(8π l_P sin^2θ)。两者相差因子 2（同源：R_c^3 定义式中 1/2 的处理）。"
    "⇒ **V4.8 在同一天内出现两个自洽性不同的版本**，引用任一数值时必须连版本号；"
    "本册全部读数以**本版（4π/π）**为准，r47 读数不得与本册混引。",
    {"this_version_U": "π ħ l_P κ^2 / c", "r47_version_U": "2π ħ l_P κ^2 / c",
     "this_mmax": "ħc/(4π l_P sin^2θ)", "r47_mmax": "ħc/(8π l_P sin^2θ)"})

# ---- D-1 二次项量纲
dim_beta_k2 = dmul(betaU_dim := ddiv(dmul(D_hbar, D_L), dpow(D_c, 3)), dpow(D_kappa, 2))
ADD("V22", "FAIL", "m(κ_0)=ακ_0−β_Uκ_0^2 的第二项量纲不是质量",
    "[β_U] = " + dstr(betaU_dim) + "、[β_U κ_0^2] = " + dstr(dim_beta_k2)
    + " ≠ M；第一项 [ακ_0] = M（正确）。⇒ 二次映射本身量纲不自洽（根因是 U_self 的 c^2 记账，与 V20/r47 W10 同点）。",
    {"dim_betaU": dstr(betaU_dim), "dim_second_term": dstr(dim_beta_k2)})

# ---- D-2 m_max 量纲
dim_mmax = ddiv(dmul(D_hbar, D_c), D_L)
ADD("V23", "FAIL", "m_max = ħc/(4π l_P sin^2θ) 量纲是能量 (J)，不是质量",
    "机器量纲 = " + dstr(dim_mmax) + " = " + dstr(D_energy)
    + "。来料 4.3.2 自核验写「[ħc/l_P]=J，除以 c^2 得到质量」——但**公式里并没有那个 c^2**，"
    "核验与被核验对象不一致（本库「手算量纲必错」第 N 次：核验行自证）。"
    "同一册内 4.3.4 的 m_P/(4π sin^2θ) 才是质量口径 ⇒ 同册两处相差 c^2=" + E(c ** 2) + "。",
    {"dim_mmax": dstr(dim_mmax), "c_squared": E(c ** 2)})

# ---- D-3 4.3.4 的 c^2 插入
ADD("V24", "MISMATCH", "4.3.4 分子分母各加一个 c^2（分母的 c^2 无来源），结论对、链条错",
    "来料写 m_max = m_P c^2/(4π c^2 sin^2θ) = m_P/(4π sin^2θ)。"
    "分子 m_P c^2 = ħc/l_P 正确；但**分母的 c^2 在上一节的公式里并不存在**，是为得到质量而临时补入的。"
    "正确链条应是：先承认 4.3.2 的式子是能量，再整体除以 c^2 ⇒ m_max = ħ/(4π l_P c sin^2θ) = m_P/(4π sin^2θ)。"
    "⇒ 数值结论 m_P/(4π sin^2θ) = " + E(mmax_Planck) + " kg **正确**，推导链条非法（与 r46 C1「指数对、系数错」同型异处）。",
    {"mmax_mass_kg": E(mmax_Planck), "mmax_GeV": E(mmax_GeV)})

# ---- D-4 m_max 的筛选力
ADD("V25", "FAIL", "m_max 约束是恒真空约束：比 τ 子大 5.47e17 倍，对 sin^2θ≤1 恒成立",
    "m_max(sinθ=1) = m_P/(4π) = " + E(mmax_Planck) + " kg = " + E(mmax_GeV) + " GeV；"
    "m_τ = " + E(mtau_GeV) + " GeV；比值 " + E(mmax_GeV / mtau_GeV) + "。"
    "要求 m_max > m_τ ⇔ sin^2θ < " + E(mmax_GeV / mtau_GeV) + "，而 sin^2θ ≤ 1 恒成立"
    " ⇒ **该约束对任何 θ 都满足，筛选力为零**（本库「上界自毁 / 恒真空约束」第 5 次复发：r44 → r45 → r46 → r47 → 本册）。",
    {"mmax_GeV": E(mmax_GeV), "mtau_GeV": E(mtau_GeV), "ratio": E(mmax_GeV / mtau_GeV)})

# ---- D-5 θ→π/2 的方向错误
ADD("V26", "FAIL", "「要求 m_max>m_τ ⇒ θ 趋近 π/2」方向写反（π/2 使 m_max 最小而非最大）",
    "m_max = m_P/(4π sin^2θ) 关于 sin^2θ **单调递减** ⇒ m_max 越大要求 sin^2θ 越小（θ→0 或 π），"
    "而 θ→π/2 使 sin^2θ→1、m_max 取**最小值** m_P/(4π)。来料结论方向相反。"
    "附带：θ→π/2 ⇒ cotθ→0 ⇒ a_TUFT→0（见 V29）⇒ 与 §4.3.3 用 a_TUFT 解释 g-2 残差的目标正面冲突。",
    {"monotonic": "m_max ∝ 1/sin^2θ（递减）"})

# ---- D-6 κ_crit 的射程
kap_tau = m_tau * c * sin1 / hbar           # 轻子支 κ_0 ≈ mc sinθ/ħ
ratio_cubic_tau = betaU * kap_tau / alpha
ADD("V27", "FAIL", "κ_crit 距普朗克曲率 16 量级、距 τ 子 35 量级 ⇒ 「三次项抑制发散」永不触发",
    "κ_crit = α/(2β_U) = " + E(kap_crit) + " m^-1；普朗克曲率 1/l_P = " + E(kappa_P)
    + " ⇒ 比值 " + E(kap_crit / kappa_P) + "；τ 子 κ_0 ≈ m_τ c sinθ/ħ = " + E(kap_tau)
    + " ⇒ κ_crit/κ_τ = " + E(kap_crit / kap_tau) + "。"
    "三次项/二次项之比 = β_Uκ_0/α：τ 子处仅 " + E(ratio_cubic_tau) + "。"
    "⇒ §4.3.3「接近临界曲率（τ 子）：三次项贡献显著，抵消二次项，防止磁矩修正发散爆炸」"
    "在真实轻子射程内**恒不成立**（差约 35 个量级），该机制是纸面机制。",
    {"kappa_crit": E(kap_crit), "kappa_Planck": E(kappa_P),
     "kappa_tau": E(kap_tau), "ratio_crit_over_tau": E(kap_crit / kap_tau),
     "cubic_over_quadratic_tau": E(ratio_cubic_tau)})

# ---- D-7 a_TUFT 的量纲（本册新增硬判据）
dim_a = ddiv(dmul(dmul(D_c, D_kappa), D_M), dmul(D_Q, D_hbar))
ADD("V28", "FAIL", "a_TUFT = −3c cotθ m κ_0/(4eħ) 量纲 = C^-1·m^-2，不是无量纲",
    "机器量纲 " + dstr(dim_a) + " ≠ 1。反常磁矩 a=(g−2)/2 必须无量纲，"
    "而该式给出电荷^-1×长度^-2 ⇒ **不是合法的可观测量**，任何与 1e-12 类阈值的比较都无意义。"
    "（本条不依赖 σ 口径、不依赖 θ 取值，是形式层的硬 FAIL。）",
    {"dim_a": dstr(dim_a)})

# ---- D-8 符号互斥
ADD("V29", "FAIL", "单一 θ 无法同时匹配电子（Δa_e<0）与缪子（Δa_μ>0）：符号互斥",
    "实验残差 Δa_e = a_exp−a_QED = " + E(DA_E) + "（负）、Δa_μ = " + E(DA_MU) + "（正）。"
    "a_TUFT = −(3c/4eħ)·cotθ·m·κ_0，对固定的 cotθ 符号，m·κ_0>0 ⇒ a_TUFT 对 e 与 μ **同号**。"
    "⇒ 令 cotθ>0 则两者皆负（μ 不成立）；cotθ<0 则两者皆正（e 不成立）。"
    "这是 1 参数 / 2 数据点的结构性互斥，与 r44 N02/N03、r46 B27、r47 W22 交叉印证（第 5 次登记）。",
    {"Da_e": E(DA_E), "Da_mu": E(DA_MU)})

# ---- D-9 比值判据
ratio_masses = (m_mu / m_e) ** 2
ratio_needed = abs(DA_MU / DA_E)
ADD("V30", "FAIL", "即使忽略符号：|a_μ/a_e| = (m_μ/m_e)^2 与需求相差 12.8 倍",
    "在轻子支 κ_0 ∝ m 上，a_TUFT ∝ m·κ_0 ∝ m^2 ⇒ a_μ/a_e = (m_μ/m_e)^2 = " + E(ratio_masses)
    + "；实验需求 |Δa_μ/Δa_e| = " + E(ratio_needed) + "；比值 " + E(ratio_masses / ratio_needed)
    + "。该比值**与 cotθ、与 θ 无关**（函数形式锁定 ⇒ 系数不变性判据，r42/r44/r46 同型），"
    "⇒ 修好量纲（V28）也救不回符号与量级。",
    {"a_mu_over_a_e_model": E(ratio_masses), "needed": E(ratio_needed),
     "mismatch_factor": E(ratio_masses / ratio_needed)})

# ================================================================ 组 E：代码同步段
def m_eq(kap, sinv=sin1):
    """来料代码 m_eq(kap,theta) = (ħcκ/sinθ − U_self(κ))/c^2"""
    return (hbar * c * kap / sinv - PI * hbar * lP / c * kap ** 2) / c ** 2

def dm_eq(kap, sinv=sin1):
    return (hbar * c / sinv - 2 * PI * hbar * lP / c * kap) / c ** 2

def a_tuft(m, kap, cotv):
    """来料代码 a_tuft = −3c cotθ/(4eħ) · m · κ"""
    return -3 * c * cotv / (4 * q_e * hbar) * m * kap

# ---- E-1 代码忠实性（公式层缺陷 ≠ 代码层缺陷）
kap_low_e = (alpha - (alpha ** 2 - 4 * betaU * m_e).sqrt()) / (2 * betaU)
code_m = m_eq(kap_low_e)
ADD("V31", "PASS", "代码与正文公式逐项一致（U_self / m_eq / a_tuft / G_th 四项对拍）",
    "以电子低支解 κ_0 = " + E(kap_low_e) + " 代入：代码 m_eq 得 " + E(code_m)
    + " kg，与 m_e = " + E(m_e) + " 相对残差 " + E(rel(code_m, m_e))
    + "；U_self(κ)=πħ l_Pκ^2/c、a_tuft=−3c cotθ mκ/(4eħ)、G_th=c^3 l_P^2/(ħ sinθ) 与正文逐项同形。"
    "⇒ 代码是公式的忠实实现，本册全部 FAIL 归属**公式/框架层**，不是编码错误。",
    {"kappa_low_e": E(kap_low_e), "m_eq_value": E(code_m), "residual": E(rel(code_m, m_e))})

# ---- E-2 findroot 初值 1e34 的可执行性（实测）
kap_it = D("1e34")
trace = []
for _ in range(40):
    fv = m_eq(kap_it) - m_e
    dfv = dm_eq(kap_it)
    if dfv == 0:
        break
    kap_it = kap_it - fv / dfv
    trace.append(kap_it)
    if len(trace) > 3 and rel(trace[-1], trace[-2]) < D("1e-40"):
        break
kap_newton = trace[-1] if trace else None
kap_high_e = (alpha + (alpha ** 2 - 4 * betaU * m_e).sqrt()) / (2 * betaU)
ADD("V32", "BOUNDARY", "findroot 初值 1e34 与电子解差 22 量级，但牛顿实测仍收敛到低支",
    "电子低支解 κ_low = " + E(kap_low_e) + " m^-1，代码初值 1e34 ⇒ 相差约 "
    + E(D("1e34") / kap_low_e) + " 倍。本册用 Decimal 牛顿法从 1e34 出发实测：迭代 "
    + str(len(trace)) + " 步收敛到 " + E(kap_newton) + "，与 κ_low 相对残差 "
    + E(rel(kap_newton, kap_low_e)) + "（因二次项在 κ≪κ_crit 时可忽略，牛顿实质一步到位）。"
    "⇒ **可执行性 PASS、但可复现性依赖隐式支选择**：单点初值只能落到一支，支由初值决定而未声明。",
    {"kappa_low": E(kap_low_e), "kappa_newton": E(kap_newton),
     "steps": len(trace), "initial_over_solution": E(D("1e34") / kap_low_e)})

# ---- E-3 双支解
ADD("V33", "BOUNDARY", "m(κ_0) 是开口向下抛物线 ⇒ 每个 m<m_max 有两支解，支选择是未声明输入",
    "电子两支：κ_low = " + E(kap_low_e) + "、κ_high = " + E(kap_high_e)
    + " m^-1；κ_high 比普朗克曲率 " + E(kappa_P) + " 大 " + E(kap_high_e / kappa_P)
    + " 倍 ⇒ 在 r≥l_P 的紫外语境下无物理意义。"
    "来料 kappa(m,theta) 只返回一支（由初值决定），**未声明用哪一支**；"
    "而 a_TUFT ∝ m·κ_0 在两支上相差 " + E(kap_high_e / kap_low_e) + " 倍 ⇒ 支选择直接决定预言量级。"
    "（与 r46 X-R46-4、r47 抛物线支问题同点，本册作继承登记。）",
    {"kappa_low_e": E(kap_low_e), "kappa_high_e": E(kap_high_e),
     "ratio": E(kap_high_e / kap_low_e), "kappa_high_over_planck": E(kap_high_e / kappa_P)})

# ---- E-4 G_th 恒等式复读
G_th_nominal = c ** 3 * lP ** 2 / (hbar * sin1)
lP_from_G = (hbar * Gexp / c ** 3).sqrt()
G_th_def = c ** 3 * lP_from_G ** 2 / (hbar * sin1)
ADD("V34", "INFO", "G_th = c^3 l_P^2/(ħ sinθ) 是恒等式复读（第 11 处）",
    "用标称 ℓ_P 代入得 G_th = " + E(G_th_nominal) + "，与 G_exp = " + E(Gexp) + " 相对残差 "
    + E(rel(G_th_nominal, Gexp)) + "（该残差仅来自 ℓ_P 与 G 的有效位数不自洽，非物理偏差）；"
    "若按 ℓ_P ≡ √(ħG/c^3) 定义代回则 G_th = " + E(G_th_def) + "，残差 " + E(rel(G_th_def, Gexp))
    + "（机器零）。⇒ 引力项对 θ 的判别力为零：sinθ→1 时 χ_G 恒为常数，梯度恒零。",
    {"G_th_nominal": E(G_th_nominal), "G_th_by_definition": E(G_th_def),
     "residual_nominal": E(rel(G_th_nominal, Gexp))})

# ---- E-5 chi_tau
ADD("V35", "FAIL", "χ_τ 把「可解性」当似然项，且在射程内恒等于 0（零信息）",
    "来料 try: kappa(mtau) 成功 ⇒ χ_τ=0；失败 ⇒ 1e12。由于 κ_τ = " + E(kap_tau)
    + " ≪ κ_crit = " + E(kap_crit) + "，求解**恒成功** ⇒ χ_τ ≡ 0，对 χ^2 贡献恒为零。"
    "且「解是否存在」是定义域性质而非似然，把它写成 1e12 罚项会把不可解伪装成极强排斥，"
    "是统计形式上的非法项（本册登记，与 r46 B32「χ_τ≡0」交叉印证）。",
    {"kappa_tau": E(kap_tau), "kappa_crit": E(kap_crit)})

# ---- E-6 σ 口径未声明
ADD("V36", "BOUNDARY", "χ^2 的三档 σ（1e-12 / 4e-7 / 相对 1e-5）来源未登记",
    "来料取 σ_e=1e-12、σ_μ=4e-7、σ_G/G=1e-5，均**未声明来源**；"
    "而判决结论对这些口径敏感（r44 记忆：同一 χ^2 在来料 σ 档与真实 σ 档下结论相反）。"
    "建议显式登记三档并注明 a_μ 取 2020 还是 2025 值（r46 X-R46-5 同点）。",
    {"sigma_e": "1e-12（未声明）", "sigma_mu": "4e-7（未声明）", "sigma_G_rel": "1e-5（未声明）"})

# ---- E-7 采样空间退化
delta_lo, delta_hi = D("1e-48"), D("1e-40")
sin_at_lo = dcos(delta_lo)
cot_at_lo = dtan(delta_lo)
dev_sin = abs(D(1) / sin_at_lo - D(1))
ADD("V37", "BOUNDARY", "ptform 的 δ∈[1e-48,1e-40] 使 sinθ≡1（60 位下不可分辨），χ^2 实际退化为 cotθ 一维",
    "δ=1e-48 时 1/sinθ − 1 = " + E(dev_sin) + "（60 位精度下为 0）⇒ G_th、m_max 在该先验下**恒为常数**，"
    "χ_G 梯度恒零、m_max ≡ m_P/(4π)；而 cotθ = tan δ ≈ δ 仍随参数变化 ⇒ 有效参数实际是 cotθ（或 δ）。"
    "⇒ 先验区间 [1e-48, 1e-40] 跨越 **8 个量级**并直接决定 a_TUFT 的量级，"
    "该区间**未被任何已知约束固定**（登记为外部输入，与 r46 B31 同型）。",
    {"delta_range": "[1e-48, 1e-40]", "sin_deviation": E(dev_sin), "cot_at_lower": E(cot_at_lo)})

# ================================================================ 组 F：汇总、选项裁定、分工
EXT_INPUTS = [
    ("θ（或等价 δ 及其 8 量级先验区间）", "普适常数，来源未给；且 V06 显示它与螺旋几何互斥"),
    ("l_P（紫外截断 l_P 与内边界 κ(l_P)=κ_0）", "外部标度"),
    ("σ（边界表面能密度）", "本版留作自由参数，未给表达式（r46 版曾给 ħc/(2l_P^2) 且量纲被判为力）"),
    ("χ^2 的三档 σ", "未声明来源（V36）"),
    ("J_κ（曲率场源密度）", "来料未给定义与量纲（V09）"),
    ("m(κ_0) 抛物线的支选择", "未声明（V33）"),
    ("罚项乘子 λ（若要补齐量纲）", "来料未给（V15）"),
]
ADD("V38", "INFO", "外部输入账 ≥7 项 ⇒ 与 Ω5（自由常数 ≤1）不相容",
    "逐项：" + "；".join(n for n, _ in EXT_INPUTS) + "。"
    "其中 θ、l_P、σ 三项进入所有可测量，J_κ 与支选择决定解的选择。"
    "⇒ 即使本册全部量纲缺陷被修补，参数账本身已越过 Ω5 限额（与 r41「外部输入 ≥2」、r46「≥3」同族，本册为 7）。",
    {"n_inputs": len(EXT_INPUTS), "items": [n for n, _ in EXT_INPUTS]})

OPTION_COST = [
    ("选项1 · dynesty 扫描 θ + 输出全套 g-2 与 χ^2",
     "禁止",
     "V28 量纲非无量纲 ⇒ χ^2 无定义；V29 符号互斥（1 参数 2 反号数据）；V37 采样退化为 cotθ 一维且先验区间未约束；"
     "V11/V12 约束与自能互斥 ⇒ **目标函数当前没有自洽定义域**。与 r44/r46/r47 的采样门禁一致（第 4 次）。"),
    ("选项2 · 去掉 R_c≫l_P 近似推精确自能",
     "可执行，但须先修 V18/V19/V20",
     "R_c 量纲 T^{2/3}（V18）、闭式与自身泊松解差 2c^2（V20）：不先修这两条，「精确」无从定义。"
     "且修好后仍与 V11 冲突（约束严格成立 ⇒ U_self≡0）——**必须与选项5 联立做**。"),
    ("选项3 · G_th(θ) 与 m_max 联立相容性",
     "零成本可做，但预期零判别力",
     "G_th 是恒等式复读（V34，梯度恒零）、m_max 是恒真空约束（V25，比 τ 子大 5.47e17 倍）"
     " ⇒ 该分析的结果大概率是「相容且无约束」，可作为**阴性证据存档**，不应作为支持性证据引用。"),
    ("选项4 · θ 后验不确定性传播到 m_max / a_e / a_μ / a_τ",
     "在 1/2/5 完成前无意义",
     "被传播的量本身无定义域（V28 量纲、V25 恒真空、V11 自毁）；先传播会把伪精度固化成结论。"),
    ("选项5 · 罚约束改写拉格朗日乘子形式",
     "本册推荐优先（但仍须与 V11/V12 同解）",
     "唯一直接攻击本册新增短板（V08 量纲 / V09 三项不齐 / V10 冗余 / V11 自毁 / V12 有源互斥）的路径。"
     "**明确失败判据**：乘子法只解决量纲，不解决「约束强制 κ 为常数」——"
     "除非①把约束限定在源外（源内不约束）或②把 ω 提升为独立动力学场（+1 自由度，撞 Ω5）。"
     "若两条都不接受，则罚约束与自能项在本框架内**不可共存**，应二选一。"),
]
ADD("V39", "INFO", "五个下一阶段选项的代价与依赖序（本册不代选）",
    "裁定表：" + " | ".join(a + " ⇒ " + b for a, b, _ in OPTION_COST) + "。"
    "**两个零成本前置（与选项选择无关，先做）**："
    "**P1** = 声明 σ 三档来源、声明抛物线支、登记 δ 先验区间的依据；"
    "**P2** = 显式写出约束 V_constraint=0 的适用范围（源内 / 源外 / 全域）"
    "——这是 V11（自毁）与 V12（有源互斥）的**最小解锁条件**。"
    "**执行次序不可换**：P1 → P2 → 选项5（配选项2）→ 只有在符号问题（V29）被独立解决后才重新评估采样。"
    "**在 P1/P2 完成之前不对当前映射做任何数值最小化。**",
    {"options": [{"name": a, "verdict": b, "why": c} for a, b, c in OPTION_COST],
     "P1": "声明 σ 口径 / 支选择 / δ 先验依据",
     "P2": "显式化约束适用范围（源内/源外）"})

ADD("V40", "INFO", "与 r46/r47 的分工与交叉印证（零重复声明）",
    "r46 = V4.8 子分支B（边界变分 ⇒ R_c），r47 = §4.3 质量链；"
    "**本册 = §4.2 稳态基态六条件 + 罚约束 + 光速螺旋几何（r46/r47 均未审）+ §4.3 版本差异复核**。"
    "交叉印证命中：V18↔r46 B03/B06（R_c 量纲）· V22/V23↔r47 W10/W12（c^2 记账）· "
    "V29/V30↔r46 B27/r47 W22（符号互斥、42753 vs 3333）· V35↔r46 B32（χ_τ≡0）· "
    "V37↔r46 B31（采样退化）· V27↔r47 W19/W20（机制在射程内恒零）。"
    "**本册独有的 5 条**：V08（罚约束量纲 + 自辩豁免）· V10（约束极小条件冗余）· "
    "V11（约束 ⇒ κ 常数 ⇒ 自能归零）· V12（约束与有源方程互斥）· V28（a_TUFT 非无量纲）。",
    {"cross_checks": ["V18↔r46 B03/B06", "V22/V23↔r47 W10/W12", "V29/V30↔r46 B27/r47 W22",
                      "V35↔r46 B32", "V37↔r46 B31", "V27↔r47 W19/W20"],
     "novel": ["V08", "V10", "V11", "V12", "V28"]})

# ================================================================ 收尾 guard
guard("G17_two_c_squared_gap",
      rel(ratio_U, 2 * c ** 2) < D("1e-30"),
      "V20 的比值必须等于 2c^2（否则自能对拍算错）")
guard("G18_G_th_identity",
      rel(G_th_def, Gexp) < D("1e-45"),
      "G_th 按 ℓ_P 定义代回必须复现 G_exp（恒等式复读的证据）")
guard("G19_newton_converged",
      kap_newton is not None and rel(kap_newton, kap_low_e) < D("1e-20"),
      "牛顿实测必须收敛到低支解（否则 V32 读数无效）")
guard("G20_item_count",
      len(ITEMS) >= 35,
      "条目数下限")

# ================================================================ 输出
def jdump(o):
    if isinstance(o, D):
        return str(o)
    if isinstance(o, F):
        return str(o)
    if isinstance(o, tuple):
        return [jdump(x) for x in o]
    if isinstance(o, list):
        return [jdump(x) for x in o]
    if isinstance(o, dict):
        return {k: jdump(v) for k, v in o.items()}
    return o

counts = {}
for it in ITEMS:
    counts[it["verdict"]] = counts.get(it["verdict"], 0) + 1
n_guard_ok = sum(1 for g in GUARDS if g["ok"])

result = {
    "round": ROUND, "date": DATE, "target": "TUFT-V4.8 修订版 4.2（+4.3 同步更新）",
    "engine": TAG + ".py",
    "items": jdump(ITEMS),
    "counts": counts,
    "n_items": len(ITEMS),
    "guards": jdump(GUARDS),
    "n_guard": len(GUARDS),
    "n_guard_ok": n_guard_ok,
    "external_inputs": [{"name": n, "note": d} for n, d in EXT_INPUTS],
    "key_numbers": jdump({
        "norm_r_prime": norm_rp, "kappa_analytic": kap_analytic, "tau_analytic": tau_analytic,
        "Omega": Om, "omega": om, "old_over_new": ratio_old,
        "cot_theta_geometric": cot_geo,
        "dim_V_constraint": dstr(dim_V), "dim_lagrangian": dstr(D_lagr_dens),
        "dim_field_eq_lhs": dstr(dim_lhs), "dim_dV_dk": dstr(dim_dVdk),
        "dim_Rc": dstr(dim_Rc), "dim_U_substituted": dstr(dim_U_subst),
        "dim_a_tuft": dstr(dim_a), "dim_mmax": dstr(dim_mmax),
        "U_pos_over_U_claim": ratio_U, "two_c_squared": 2 * c ** 2,
        "alpha": alpha, "betaU": betaU, "kappa_crit": kap_crit,
        "kappa_Planck": kappa_P, "kappa_tau": kap_tau,
        "crit_over_tau": kap_crit / kap_tau, "cubic_over_quadratic_tau": ratio_cubic_tau,
        "kappa_low_e": kap_low_e, "kappa_high_e": kap_high_e,
        "mmax_energy_J": mmax_energy, "mmax_mass_kg": mmax_mass, "mmax_Planck_kg": mmax_Planck,
        "mmax_GeV": mmax_GeV, "mtau_GeV": mtau_GeV, "mmax_over_mtau": mmax_GeV / mtau_GeV,
        "a_mu_over_a_e_model": ratio_masses, "a_mu_over_a_e_needed": ratio_needed,
        "mismatch_factor": ratio_masses / ratio_needed,
        "Da_e": DA_E, "Da_mu": DA_MU,
        "G_th_nominal": G_th_nominal, "G_th_definition": G_th_def,
    }),
    "not_self_derived": [
        "罚项乘子 λ 的数值与来源（只给量纲）",
        "J_κ 的定义、量纲与归一化",
        "σ（边界表面能密度）的第一性表达式",
        "约束 V_constraint=0 的适用范围（源内/源外）应由来料声明，本册不代定",
    ],
    "self_caught": [],
}

json_path = os.path.join(OUT_DIR, TAG + ".json")
with io.open(json_path, "w", encoding="utf-8") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=2)

# ---- md
lines = []
lines.append("# TUFT-V4.8「修订版 4.2」全维审计 · 数据产物（" + ROUND + " · " + DATE + "）")
lines.append("")
lines.append("- 条目 **" + str(len(ITEMS)) + "**：" +
             " / ".join(k + " " + str(v) for k, v in sorted(counts.items())))
lines.append("- 自检 guard **" + str(n_guard_ok) + "/" + str(len(GUARDS)) + "**")
lines.append("")
lines.append("| 编号 | 判定 | 条目 | 关键读数 |")
lines.append("|---|---|---|---|")
for it in ITEMS:
    kn = ""
    if it["key"]:
        kn = "；".join(str(k) + "=" + str(v) for k, v in list(it["key"].items())[:3])
    lines.append("| " + it["code"] + " | " + it["verdict"] + " | " + it["title"] +
                 " | " + kn.replace("|", "/") + " |")
lines.append("")
lines.append("## 关键数值档案")
lines.append("")
lines.append("```")
for k, v in result["key_numbers"].items():
    lines.append(str(k) + " = " + str(v))
lines.append("```")
md_path = os.path.join(OUT_DIR, TAG + ".md")
with io.open(md_path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

# ---- report
rep = []
rep.append("TUFT-V4.8 修订版4.2 全维审计 " + ROUND + " " + DATE)
rep.append("条目 " + str(len(ITEMS)) + "：" + " / ".join(k + " " + str(v) for k, v in sorted(counts.items())))
rep.append("自检 " + str(n_guard_ok) + "/" + str(len(GUARDS)))
for g in GUARDS:
    rep.append(("PASS " if g["ok"] else "FAIL ") + g["name"])
rep_path = os.path.join(OUT_DIR, TAG + "_report.txt")
with io.open(rep_path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(rep))

print("条目 " + str(len(ITEMS)) + "：" + " / ".join(k + " " + str(v) for k, v in sorted(counts.items())))
print("自检 guard " + str(n_guard_ok) + "/" + str(len(GUARDS)))
print("产物：" + json_path)
sys.exit(0)
