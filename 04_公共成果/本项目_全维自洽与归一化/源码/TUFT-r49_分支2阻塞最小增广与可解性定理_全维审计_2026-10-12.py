# -*- coding: utf-8 -*-
"""
TUFT-V4.7 分支2 阻塞的「最小增广与可解性定理」——全维审计（r49 · 2026-10-12）

来料链：r48 已裁定 V4.7 分支2 的三重阻塞
    (A) 轮廓层：∇²κ=0（无源）+ κ(R_c)=0（边界归零）+ κ(0)=κ₀≠0（原点非平凡）
        ⇒ 不可能三角 ⇒ 可行域为空（唯一解 κ≡0）
    (B) 拟合层·符号：a^TUFT 的符号只由 cotθ 决定 ⇒ e/μ 必然同号，
        而数据要求 Δa_μ/Δa_e = 2.3E-9 / −6.9E-13 = −3.3333E+3 < 0（反号）
        ⇒ 任意 (θ,ξ,β) 不可解（对量纲补齐因子与 β 全区间免疫）
    (C) 拟合层·量级：κ(m) 凸增定理 ⇒ a_μ/a_e ≥ (m_μ/m_e)² = 4.2753E+4
        ⇒ 与目标 3.3333E+3 反向且差 12.83×，非线性只会更糟

本册定位（与 r46/r47/r48 分工·零重复）：
  r46 = V4.8 子分支B（边界变分 + 点源泊松 + 表面张力 ⇒ R_c(κ) 幂律）
  r47 = V4.8 §4.3 稳态质量隐式关系 m(κ₀) 与 m_max（r46 的直接下游）
  r48 = V4.7 分支2（格林函数解 + 线性球包 + R_c=ξκ^{-β}）全维审计 —— 判"不成立"
  **本册 = r48 的直接下游**：不重审 r48 已给数值（只做回链交叉印证），
  改问一个**构造性问题**：在上述三重阻塞下，
      (i) 轮廓层是否存在「最小合法增广」，若存在其自由度为几？
      (ii) 符号与量级这两个阻塞，是不是同一个自由度？（本册核心定理）
      (iii) 若用最小增广达成 e/μ 双拟合，剩余的可证伪读数是什么、当前实验能否检验？
    ⇒ 目标是把"不可解"升级为"**最小增广的存在性 + 唯一性 + 代价 + 可证伪读数**"。

纪律（继承 r37/r44/r45/r48）：
  1. 量纲工具必须先过 G0 guard 再用于判定（dmul 写成逐分量相乘已复发 3 次）
  2. 任何"恒等于零 / 恒不成立"的裁定必须配**阳性对照**，且阈值先在解析上算清量级
  3. 所有结论由机器读数生成，不硬编码结论文本
  4. guard 未全过 ⇒ return 2，禁止输出结论

红线：数学自洽 ≠ 物理证实。本册是**可解性与代价的机器判定**，
      **不代选方向**、不产生新物理；所有"最小增广"仅登记其存在性与代价。

引擎：纯标准库 —— decimal（60 位）+ fractions（四分量量纲 (M,L,T,Q)）
"""

import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(BASE), "数据")
STAMP = "2026-10-12"
NAME = "TUFT-r49_分支2阻塞最小增广与可解性定理_全维审计_%s" % STAMP

D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494")

# ---------------------------------------------------------------- CODATA（与 r45/r48 逐位同源）
c = D("299792458")
hbar = D("1.0545718176461565e-34")
e_ch = D("1.602176634e-19")
m_e = D("9.1093837015e-31")
m_mu = D("1.883531627e-28")
m_tau = D("3.16754e-27")             # 来料值 ≈1777 MeV
Gexp = D("6.67430e-11")
lP_nominal = D("1.616255078e-35")
GEV_OVER_C2 = D("1.78266192e-27")    # kg per GeV/c^2

# g-2 数据（与 r42/r44/r48 同源）
a_e_th = D("1.15965218161e-3")
a_e_exp = D("1.15965218073e-3")
a_mu_th = D("1.16591705e-3")
a_mu_exp = D("1.16592061e-3")
da_e = a_e_exp - a_e_th             # −6.9E-13
da_mu = a_mu_exp - a_mu_th          # +2.3E-9（与本册符号判据同取向）

# τ 反常磁矩实验界限（DELPHI 95% CL）
A_TAU_LO = D("-0.052")
A_TAU_HI = D("0.013")
A_TAU_SM = D("1.17721e-3")          # SM 预言，仅作对照，不作判据

# ---------------------------------------------------------------- 量纲工具
M_, L_, T_, Q_ = 0, 1, 2, 3


def Dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


dONE = Dim()
dL = Dim(0, 1, 0)
dT = Dim(0, 0, 1)
dM = Dim(1, 0, 0)
dQ = Dim(0, 0, 0, 1)


def dmul(a, b):
    """量纲相乘 = 指数相加。r37/r44/r45 各踩过一次「写成逐分量相乘」，本册当场拦下。"""
    return tuple(a[i] + b[i] for i in range(4))


def dinv(a):
    return tuple(-a[i] for i in range(4))


def dpow(a, p):
    return tuple(a[i] * Fraction(p) for i in range(4))


def dscale(a, p):
    return dpow(a, p)


def deq(a, b):
    return all(a[i] == b[i] for i in range(4))


DSYM = {0: "M", 1: "L", 2: "T", 3: "Q"}


def dstr(a):
    out = []
    for i in range(4):
        if a[i] == 0:
            continue
        out.append("%s^%s" % (DSYM[i], str(a[i])))
    return "·".join(out) if out else "1"


dEnergy = dmul(dM, dpow(dL, 2))
dmul_t = dmul


# ---------------------------------------------------------------- 三角/数值工具（Decimal）
def _dsin(x):
    x = D(x)
    s = D(0)
    term = x
    n = 1
    while True:
        s += term
        n += 2
        term = -term * x * x / (D(n - 1) * D(n))
        if abs(term) < D("1e-70"):
            break
    return s


def _dcos(x):
    x = D(x)
    s = D(1)
    term = D(1)
    n = 0
    while True:
        n += 2
        term = -term * x * x / (D(n - 1) * D(n))
        s += term
        if abs(term) < D("1e-70"):
            break
    return s


def rel(a, b):
    a, b = D(a), D(b)
    if a == 0 and b == 0:
        return D(0)
    den = max(abs(a), abs(b))
    if den == 0:
        return D(0)
    return abs(a - b) / den


def _f(x, n=12):
    try:
        return "%s" % (D(x),)
    except Exception:
        return str(x)


def fmt(x, n=12):
    """定点科学计数法：12 位有效数字"""
    q = D(x)
    if q == 0:
        return "0.000000000000E+0"
    s = q.normalize()
    sign = "-" if s < 0 else ""
    s = abs(s)
    exp = s.adjusted()
    mant = s.scaleb(-exp)
    ms = ("%.12f" % mant)[:14]
    return "%s%sE%+d" % (sign, ms, exp)


# ---------------------------------------------------------------- 记录器
RECORDS = []
GUARDS = []
OPEN_ITEMS = []
NOT_SELF_DERIVED = []


def _emit(kind, cid, claim, reading, note=""):
    RECORDS.append(dict(id=cid, verdict=kind, claim=claim,
                        machine_reading=reading, note=note))


def FAIL(cid, claim, reading, note=""):
    _emit("FAIL", cid, claim, reading, note)


def PASS(cid, claim, reading, note=""):
    _emit("PASS", cid, claim, reading, note)


def INFO(cid, claim, reading, note=""):
    _emit("INFO", cid, claim, reading, note)


def BOUNDARY(cid, claim, reading, note=""):
    _emit("BOUNDARY", cid, claim, reading, note)


def CORRECTED(cid, claim, reading, note=""):
    _emit("CORRECTED", cid, claim, reading, note)


def MISMATCH(cid, claim, reading, note=""):
    _emit("MISMATCH", cid, claim, reading, note)


def guard(name, ok, detail):
    GUARDS.append(dict(name=name, passed=bool(ok), detail=detail))
    return bool(ok)


# ================================================================ G0 量纲工具自检
guard("dim_mul_additive_not_multiplicative",
      deq(dmul(dL, dL), Dim(0, 2, 0)) and deq(dmul(dL, dinv(dL)), dONE),
      "dmul(L,L)=L^2 ; dmul(L,1/L)=1（指数相加，非逐分量相乘）")
guard("dim_pow_and_scale",
      deq(dpow(dL, 3), Dim(0, 3, 0)) and deq(dscale(dL, Fraction(1, 2)), Dim(0, Fraction(1, 2), 0)),
      "dpow(L,3)=L^3 ; dscale(L,1/2)=L^1/2")
dim_kappa = dinv(dL)                       # [κ]=L^-1
dim_hbar_c_kappa = dmul(dmul(Dim(1, 2, -1), dL), dim_kappa)   # ħ·c·κ
guard("dim_energy_chain",
      deq(dim_hbar_c_kappa, dEnergy),
      "[hbar*c*kappa]=%s 应为 %s" % (dstr(dim_hbar_c_kappa), dstr(dEnergy)))
guard("trig_identity_positive_control",
      abs(_dsin(D(1)) ** 2 + _dcos(D(1)) ** 2 - 1) < D("1e-50"),
      "sin^2(1)+cos^2(1)-1 = %s" % fmt(_dsin(D(1)) ** 2 + _dcos(D(1)) ** 2 - 1))
guard("pi_guard_sin_pi_over_6",
      abs(_dsin(PI / 6) - D("0.5")) < D("1e-50"),
      "sin(pi/6)=%s" % fmt(_dsin(PI / 6)))
guard("data_signs_are_opposite",
      da_e < 0 and da_mu > 0,
      "Δa_e=%s < 0，Δa_μ=%s > 0（机器确认，排除我自己的符号读反）" % (fmt(da_e), fmt(da_mu)))

ratio_req = da_mu / da_e                    # 负值
mm_ratio = m_mu / m_e
mm_ratio_sq = mm_ratio ** 2

# 交叉印证：r48 登记的 (m_μ/m_e)² 与 Δa 比值
guard("crosscheck_r48_ratio_readings",
      rel(mm_ratio_sq, D("4.275312284808E+4")) < D("1e-10")
      and rel(abs(ratio_req), D("3.333333333333E+3")) < D("1e-10"),
      "本册复算 (m_μ/m_e)²=%s、|Δa_μ/Δa_e|=%s，与 r48 登记 4.2753E+4 / 3.3333E+3 一致"
      % (fmt(mm_ratio_sq), fmt(abs(ratio_req))))

# __NEXT__
