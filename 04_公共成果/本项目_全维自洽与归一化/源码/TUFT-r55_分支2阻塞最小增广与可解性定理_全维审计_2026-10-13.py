# -*- coding: utf-8 -*-
"""
TUFT-V4.7 分支2 阻塞的「最小增广与可解性定理」——全维审计（r55 · 2026-10-13）

【编号仲裁】三次迁号（本目录 r 序列处在多会话竞争态，务必落盘前 search_file 复核）：
           ①起草暂用 r49 → 发现并行会话占用 r49（V4.8 修订版4.2 稳态基态）⇒ 迁 r53；
           ②r53 又被并行会话占用（空间螺旋结构光与光子）⇒ 复核 r54（四维类光层）、
             r56（光光子与空间螺旋三分法）亦被占用 ⇒ 取空号 **r55**。
           其余占用：r50（路线B 演化方程 M1M2）、r51 ×2、r52。

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
STAMP = "2026-10-13"
ROUND = "r55"
NAME = "TUFT-r55_分支2阻塞最小增广与可解性定理_全维审计_%s" % STAMP

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
a_e_exp = D("1.15965218073e-3")
a_e_th = D("1.15965218161e-3")
a_mu_exp = D("1.16592061e-3")
a_mu_th = D("1.16591705e-3")
# Δa 直接采用 r42/r44/r48 登记的「实验 − SM」口径，保证与 r48 的比值 −3.3333E+3 逐位同源
da_e = D("-6.9e-13")
da_mu = D("2.3e-9")                 # 与 da_e 反号（本册符号判据同取向）

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


dEnergy = dmul(dmul(dM, dpow(dL, 2)), dpow(dT, -2))    # M·L^2·T^-2
dim_c = Dim(0, 1, -1)                                   # [c] = L·T^-1
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


def guard(name, ok, detail, note=""):
    GUARDS.append(dict(name=name, passed=bool(ok), detail=detail, note=note))
    return bool(ok)


# ================================================================ G0 量纲工具自检
guard("dim_mul_additive_not_multiplicative",
      deq(dmul(dL, dL), Dim(0, 2, 0)) and deq(dmul(dL, dinv(dL)), dONE),
      "dmul(L,L)=L^2 ; dmul(L,1/L)=1（指数相加，非逐分量相乘）")
guard("dim_pow_and_scale",
      deq(dpow(dL, 3), Dim(0, 3, 0)) and deq(dscale(dL, Fraction(1, 2)), Dim(0, Fraction(1, 2), 0)),
      "dpow(L,3)=L^3 ; dscale(L,1/2)=L^1/2")
dim_kappa = dinv(dL)                       # [κ]=L^-1
dim_hbar_c_kappa = dmul(dmul(Dim(1, 2, -1), dim_c), dim_kappa)   # ħ·c·κ
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

# 口径登记：用原始四位 a 值**直接相减**得到的 Δa 与 r48 登记口径不同（诚实登记，不擅自统一）
da_e_raw = a_e_exp - a_e_th
da_mu_raw = a_mu_exp - a_mu_th
ratio_raw = da_mu_raw / da_e_raw
guard("raw_delta_a_keeps_opposite_sign", da_e_raw < 0 and da_mu_raw > 0,
      "原始四位值直接相减：Δa_e=%s < 0、Δa_μ=%s > 0 ⇒ **符号裁定对口径选择稳健**"
      % (fmt(da_e_raw), fmt(da_mu_raw)))
INFO("D00", "Δa 存在两个口径（%s vs %s），本册采用 r48 登记口径，符号结论不变"
     % (fmt(ratio_req), fmt(ratio_raw)),
     "口径①（本册/r42/r44/r48 登记）Δa_e=−6.9e−13、Δa_μ=+2.3e−9 ⇒ 比值 %s；"
     "口径②（原始四位 a 值直接相减）Δa_e=%s、Δa_μ=%s ⇒ 比值 %s。"
     "两者**反号一致**（guard 确认）⇒ 符号阻塞（II01）与破局定理（II02/III03）**不受口径影响**；"
     "仅量级读数（m_0 的具体数值、a_τ 预言值）随口径变化 ⇒ 二者只作量级参考，不作判据"
     % (fmt(ratio_req), fmt(da_e_raw), fmt(da_mu_raw), fmt(ratio_raw)),
     "不擅自统一口径：统一属实验/理论侧的取值决策，须由用户裁决")

# ================================================================ I 组：轮廓层最小增广
# 说明：r48 已用「逐点法」证 κ=κ₀(1−r/R_c) 不是 ∇²κ=0 的解（漏 2κ'/r）。
#       本册给**第二条独立路径**（积分形式 / 散度定理），并给出最小合法增广的闭式解。

Rc_ = D(1)          # 归一化半径（判结构用，量纲结论不受影响）
kap0_ = D(1)


def kap_claim(r):
    """来料轮廓 κ(r)=κ₀(1−r/R_c)"""
    return kap0_ * (1 - r / Rc_)


def lap_fd(fn, r, h=D("1e-10")):
    """球对称拉普拉斯：κ'' + 2κ'/r（中心差分，Decimal）"""
    d1 = (fn(r + h) - fn(r - h)) / (2 * h)
    d2 = (fn(r + h) - 2 * fn(r) + fn(r - h)) / (h * h)
    return d2 + 2 * d1 / r


# I01 散度定理第二条独立证伪
flux_claim = 4 * PI * Rc_ ** 2 * (-kap0_ / Rc_)      # ∮∇κ·dA = 4πR_c²·κ'(R_c)
guard("flux_nonzero_for_claimed_profile",
      abs(flux_claim) > D("1e-30"),
      "来料轮廓的边界通量 ∮∇κ·dA = 4πR_c²κ'(R_c) = %s ≠ 0；齐次 ∇²κ=0 要求 ∮=0（散度定理）"
      "⇒ 第二条独立证伪路径（与 r48 逐点法并列）" % fmt(flux_claim))
# 阳性对照：真点源场 κ=A(1/r−1/R_c) 满足 r>0 处 ∇²κ=0，其通量恰等于源强 −4πA（Gauss）
A_src = D("0.5")


def kap_ps(r):
    return A_src * (1 / r - 1 / Rc_)


flux_ps = 4 * PI * Rc_ ** 2 * (-A_src / Rc_ ** 2)    # κ'(R_c) = −A/R_c²
guard("point_source_flux_matches_gauss",
      rel(flux_ps, -4 * PI * A_src) < D("1e-40"),
      "阳性对照：点源场通量 %s 恰 = −4πA = %s（Gauss 定理成立，检验器非恒零）"
      % (fmt(flux_ps), fmt(-4 * PI * A_src)))
FAIL("I01", "来料轮廓满足 ∇²κ=0（积分形式复核）",
     "散度定理：齐次方程 ⇒ ∮∇κ·dA 必须 = 0；来料轮廓 κ=κ₀(1−r/R_c) 给 ∮ = %s ≠ 0 ⇒ "
     "**与 r48 A01（逐点法：∇²κ=−2κ₀/(rR_c)）互为独立的两条证伪路径**。"
     "三条边界条件（无源 / Dirichlet / 原点非平凡）仍构成不可能三角 ⇒ 可行域为空"
     % fmt(flux_claim),
     "⇒ 要得到非平凡解，必须放弃「无源」这一条 ⇒ 最小增广方向被唯一指定为「引入源项」")

# I02 最小平滑源增广：均匀源 S=S₀（常值）⇒ ∇²κ=−4πS₀ ⇒ κ=(2π/3)S₀(R_c²−r²)
S0_ = D("0.37")


def kap_unif(r):
    return (2 * PI / 3) * S0_ * (Rc_ ** 2 - r ** 2)


lap_unif_rows = []
for r_ in [D("0.25"), D("0.5"), D("0.75")]:
    lap_unif_rows.append((fmt(lap_fd(kap_unif, r_)), fmt(-4 * PI * S0_)))
unif_ok = all(rel(D(a), D(b)) < D("1e-15") for a, b in lap_unif_rows)
guard("uniform_source_solution_satisfies_poisson", unif_ok,
      "均匀源闭式解 κ=(2π/3)S₀(R_c²−r²) 代回：∇²κ 在三点 = %s / %s / %s，"
      "解析值 −4πS₀ = %s（差分对拍通过）"
      % (lap_unif_rows[0][0], lap_unif_rows[1][0], lap_unif_rows[2][0], fmt(-4 * PI * S0_)))
# 自能：∇κ=−(4π/3)S₀ r ⇒ ∫4πr²|∇κ|²dr = 64π³S₀²R_c⁵/45（解析）
self_en_unif = 64 * PI ** 3 * S0_ ** 2 * Rc_ ** 5 / 45
# 黎曼和对拍
N_int = 20000
h_int = Rc_ / N_int
num_int = D(0)
for i in range(N_int):
    r_mid = (D(i) + D("0.5")) * h_int
    grad = -(4 * PI / 3) * S0_ * r_mid
    num_int += 4 * PI * r_mid ** 2 * grad ** 2 * h_int
guard("uniform_source_self_energy_finite",
      rel(num_int, self_en_unif) < D("1e-8"),
      "均匀源自能：黎曼和 %s vs 解析 64π³S₀²R_c⁵/45 = %s（有限 ✓，无 UV 发散）"
      % (fmt(num_int), fmt(self_en_unif)))
CORRECTED("I02", "轮廓层最小合法增广 = 均匀（平滑）源 ⇒ 局域包由方程推出而非 ansatz",
          "取最简平滑源 S=S₀（常值）：∇²κ=−4πS₀ 的球对称正则解为 "
          "**κ(r)=(2π/3)S₀(R_c²−r²)**（差分对拍 ∇²κ 三点逐位 = −4πS₀），"
          "自能 ∫4πr²|∇κ|²dr = **64π³S₀²R_c⁵/45 = %s**（黎曼和 %s，**有限**）。"
          "⇒ 该解天然是钟形局域包（κ(0) 有限、κ(R_c)=0 严格、κ 单调）"
          % (fmt(self_en_unif), fmt(num_int)),
          "**这是本册识别出的实质路径**：来料想要的「不用经验指数包、由方程推出局域包」"
          "在「引入平滑源」这一条增广下即可实现（对应 r48 §7 选项2 的前半步）。"
          "代价见 I06：+1 源强度 S₀、+1 源形状约定")

# I03 点源自能发散（继承 r48 A03，只做交叉印证）
div_rows = []
for rr in [D("1e-1"), D("1e-3"), D("1e-6"), D("1e-9")]:
    rmin = Rc_ * rr
    val = 4 * PI * A_src ** 2 * (1 / rmin - 1 / Rc_)
    div_rows.append(fmt(val))
div_ratio = D(div_rows[3]) / D(div_rows[0])
guard("point_source_self_energy_diverges",
      div_ratio > D("1e7"),
      "点源自能 4πA²(1/r_min−1/R_c)：r_min/R_c=1e-1→1e-9 得 %s→%s（比值 %s，跨 8 个十倍程 "
      "⇒ 每十倍程约 ×10 ⇒ **幂次发散**）"
      % (div_rows[0], div_rows[3], fmt(D(div_rows[3]) / D(div_rows[0]))))
FAIL("I03", "点源（δ 源）方案可作为最小增广",
     "点源解 κ=A(1/r−1/R_c) 满足 Dirichlet，但自能 %s→%s 随内截断**幂次发散**"
     "（每十倍程 ×10，与 r48 A03 同读数，本册独立复算）⇒ 需引入内截断 r_min，"
     "而 r_min 支配全部标度 ⇒ **无预言力**（复发 r37/r45/r48 的『标度由截断主导』族）。"
     "⇒ 点源不是合法增广，**平滑源（I02）才是最小合法增广**" % (div_rows[0], div_rows[3]),
     "注意：来料 §8/r48 A03 已判同点，本册只作交叉印证与「最小性」比较")

# I04 自洽源幂次 ⇒ R_c(κ₀) 指数定理
#     设源自洽：S₀ = λ·κ₀^s（κ₀ ≡ κ(0)）。由 κ₀=(2π/3)S₀R_c² 得
#     R_c = sqrt(3/(2πλ))·κ₀^{(1−s)/2}  ⇒  与来料 R_c=ξκ^{−β} 比对：β = (s−2)/2 的相反数 ⇒ β=(s−1)/2
beta_rows = []
for s_ in [D(1), D(2), D(3), D(4)]:
    beta_rows.append((fmt(s_), fmt((s_ - 1) / 2)))
s_for_beta_half = D(2)          # β=1/2 ⇒ s=2（源自洽 ∝κ₀²）
guard("exponent_theorem_beta_from_source_power",
      all(rel((D(a) - 1) / 2, D(b)) < D("1e-40") for a, b in beta_rows),
      "指数定理：R_c ∝ κ₀^{(1−s)/2} ⇒ 来料 β = (s−1)/2；s=1/2/3/4 ⇒ β = 0/0.5/1/1.5",
      note="")
INFO("I04", "自洽源幂次 s 与来料幂律指数 β 的对应定理（把 ansatz 换成可推导族）",
     "设源自洽 S₀=λκ₀^s，由 κ₀=(2π/3)S₀R_c² 闭式得 **R_c = sqrt(3/(2πλ))·κ₀^{(1−s)/2}**，"
     "与来料 R_c=ξκ^{−β} 比对 ⇒ **β=(s−1)/2**：s=1/2/3/4 ⇒ β=0/0.5/1/1.5。"
     "⇒ 来料作为自由指数的 β，**可由源的非线性幂次 s 决定**；"
     "特别地 **s=1（线性自洽源）⇒ β=0 ⇒ R_c 为常数且是被推导出来的**（不再是 ansatz）",
     "代价记账：s 仍须外部给定 ⇒ **自由度未减，只是从「指数 β」换位为「源幂次 s」**"
     "（复发 r32 Z19 / r48 E03 记账转移族）。且 [λ]=L^{−2} ⇒ R_c=sqrt(3/(2π))·ℓ 需一个长度 ℓ"
     "（若取 ℓ=l_P 则回到 V4.5 的固定普朗克尺度）")

# I05 自洽 Helmholtz（负源 S=(k²/4π)κ）⇒ 离散谱
k_h = PI / Rc_                      # n=1
A_h = D(1)


def kap_h(r):
    return A_h * _dsin(k_h * r) / (k_h * r)


helm_rows = []
for r_ in [D("0.25"), D("0.5"), D("0.75")]:
    fd = lap_fd(kap_h, r_)
    an = -k_h ** 2 * kap_h(r_)
    helm_rows.append((fmt(fd), fmt(an), rel(fd, an)))
helm_ok = all(x[2] < D("1e-15") for x in helm_rows)
guard("helmholtz_solution_fd_vs_analytic", helm_ok,
      "κ=A sin(kr)/(kr) 满足 ∇²κ=−k²κ：三点差分 %s / %s / %s vs 解析 %s / %s / %s（相对残差 ≤ %s）"
      % (helm_rows[0][0], helm_rows[1][0], helm_rows[2][0],
         helm_rows[0][1], helm_rows[1][1], helm_rows[2][1],
         fmt(max(x[2] for x in helm_rows))))
guard("helmholtz_dirichlet_quantization",
      abs(_dsin(k_h * Rc_)) < D("1e-50"),
      "Dirichlet κ(R_c)=0 ⇒ sin(k R_c)=0 ⇒ k_n R_c = nπ；n=1 时 sin(π)=%s（机器零）"
      % fmt(_dsin(k_h * Rc_)))
# 阳性对照：取 k 使 kR_c=π/2 ⇒ κ(R_c)≠0（检验器非恒零）
k_ctl = PI / (2 * Rc_)
kap_ctl_Rc = _dsin(k_ctl * Rc_) / (k_ctl * Rc_)
guard("helmholtz_positive_control", abs(kap_ctl_Rc) > D("1e-3"),
      "阳性对照：kR_c=π/2 ⇒ κ(R_c)=%s ≠ 0（检验器非恒零）" % fmt(kap_ctl_Rc))
kappa_at_origin = kap_h(D("1e-20"))
guard("helmholtz_finite_at_origin",
      abs(kappa_at_origin - A_h) < D("1e-15"),
      "κ(0)=lim sin(kr)/(kr)=A=%s（有限 ✓，与点源的 1/r 发散对比）" % fmt(kappa_at_origin))
# 谱对质量比的判别力：m_n/m_1 = n（线性极限下 m ∝ κ_0 ∝ ... 见下）
n_mu = D(int(mm_ratio + D("0.5")))          # m_μ/m_e ≈ 206.77 ⇒ 最近整数 207
n_tau = D(int(m_tau / m_e + D("0.5")))      # m_τ/m_e ≈ 3477
INFO("I05", "自洽 Helmholtz 增广给出离散曲率谱（量子化成立，但对质量比零判别力）",
     "取负源 S=(k²/4π)κ ⇒ ∇²κ+k²κ=0 ⇒ 球对称正则解 **κ=A sin(kr)/(kr)**（差分对拍相对残差 ≤ %s），"
     "Dirichlet ⇒ **k_n=nπ/R_c（谱量子化成立）**，κ(0)=A 有限、自能有限（与点源的 1/r 发散对比）。"
     "但谱只给 κ_n ∝ n ⇒ 线性极限 m ∝ κ ⇒ **m_n/m_1 = n**，即质量比必须是整数；"
     "实测 m_μ/m_e=%s（≈%s）、m_τ/m_e=%s（≈%s）⇒ 任何整数 n 都能配（n=207、3477），"
     "**无任何约束 ⇒ 零判别力**（复发 r26 临界半径族：跨 193 倍的一族解全存在）"
     % (fmt(max(x[2] for x in helm_rows)), fmt(mm_ratio), fmt(n_mu),
        fmt(m_tau / m_e), fmt(n_tau)),
     "⇒ 量子化本身不是代际问题的解：等间距谱与实测质量比（206.8 / 16.8）不构成匹配判据")

INFO("I06", "轮廓层增广的代价记账（自由度是否真的减少）",
     "候选增广与代价：①**点源** — 自能幂次发散 ⇒ 不合法；②**均匀平滑源** — 合法，"
     "代价 +1 源强度 S₀、+1 源形状约定（p=0 是最简）；③**自洽源 S₀=λκ₀^s** — 把 β 变成可推导量，"
     "代价 +1 幂次 s 与 +1 常数 λ（[λ]=L^{−2} ⇒ 仍需一个长度 ℓ）；④**自洽 Helmholtz** — 给出离散谱，"
     "代价 +1 k 的定标（等价于 +1 长度）。⇒ **没有任何一条使总自由度下降**；"
     "②相对其它三条的差别是「局域包不再是 ansatz」而非「参数更少」",
     "不代选：源项的具体形式与系数属公设层决策，本册只给存在性与代价")

# ================================================================ II 组：符号/量级统一破局（本册核心）
# 记号：把 e/μ 双拟合的要求写成**单一比值条件**
#        a(m) = C·m·κ(m)·cotθ ，κ_lin(m)=m c/ħ
#     ⇒  a_μ/a_e = (m_μ κ_μ)/(m_e κ_e) = (m_μ/m_e)² · F(m_μ)/F(m_e)，其中 F(m) ≡ κ(m)/κ_lin(m)
#        数据要求 a_μ/a_e = Δa_μ/Δa_e = −3.3333E+3（**负值**）
#        纯线性极限 F≡1 ⇒ 比值 = +4.2753E+4（r48 D02 的凸性定理下界，且 F 单调不减只会更大）

target_ratio = ratio_req            # 负值 −3333.33…

# II01 符号不可解（复算 r48 D01，本册只作交叉印证）
sign_block_ok = (da_e < 0) and (da_mu > 0)
guard("sign_block_confirmed", sign_block_ok,
      "Δa_e=%s 与 Δa_μ=%s 反号；a^TUFT 的符号只由 cotθ 决定 ⇒ 1 个符号自由度 / 2 个反号数据点"
      % (fmt(da_e), fmt(da_mu)))
FAIL("II01", "在来料 (θ,ξ,β) 三参数族内存在 e/μ 双拟合解（符号侧）",
     "数据比值 a_μ/a_e 的**要求值 = %s（负）**，而来料函数形式在任意 (θ,ξ,β) 下给出"
     "a_μ/a_e = (m_μκ_μ)/(m_eκ_e) > 0（κ 在物理支恒正、m>0、cotθ 对两粒子同号）"
     "⇒ **符号结构性不可解**（与 r48 D01 同裁定，本册复算确认）" % fmt(target_ratio),
     "本册的任务不是重复裁定，而是问：要解除它，最少需要什么？见 II02")

# II06 先做：框架内可变号因子穷举 ⇒ 定理化「框架内无解」
#   a(m) 的因子候选（全部取自来料自身表达式）：m、κ(m)（二次映射的两个正根）、
#   sinθ、cosθ、cotθ、R_c=ξκ^{−β}、(1−m/m_max)^{1/2}、自能修正 (1−√(1−ε))
#   除「θ 全局唯一 ⇒ cosθ/cotθ 对所有粒子同号」外，其余因子在 m>0 且 m<m_max 时**恒正**
sign_grid = []
beta_list = [D("0.0"), D("0.25"), D("0.5"), D("0.75"), D("0.9")]
A1_ = hbar / c                       # A₁=ħ/(c sinθ)，取 sinθ≈1（θ≈π/2，与拟合 δ≲1e−45 一致）
for b_ in beta_list:
    # 选 ξ 使 m_max ≥ 2 m_μ（保证 e 与 μ 都在定义域内）：二分求 ξ
    def mmax_of_xi(xi_):
        B_ = 2 * PI * hbar * xi_ / (3 * c)
        p_ = D(2) - b_                                  # m = A₁κ − B κ^{p}
        # κ* : dm/dκ = A₁ − p B κ^{p−1} = 0
        kstar = (A1_ / (p_ * B_)) ** (D(1) / (D(1) - b_))
        return A1_ * kstar - B_ * kstar ** p_
    lo, hi = D("1e-30"), D("1e30")
    for _ in range(200):
        mid = (lo * hi).sqrt()
        if mmax_of_xi(mid) > 2 * m_mu:
            lo = mid
        else:
            hi = mid
    xi_sel = (lo * hi).sqrt()
    Bsel = 2 * PI * hbar * xi_sel / (3 * c)
    psel = D(2) - b_

    def m_of_kappa(kk):
        return A1_ * kk - Bsel * kk ** psel

    kstar_sel = (A1_ / (psel * Bsel)) ** (D(1) / (D(1) - b_))
    for mm in [m_e, m_mu]:
        # 二分求物理支（κ<κ*）上的正根
        a_lo, a_hi = D("1e-20"), kstar_sel
        for _ in range(160):
            mid = (a_lo + a_hi) / 2
            if m_of_kappa(mid) < mm:
                a_lo = mid
            else:
                a_hi = mid
        kk = (a_lo + a_hi) / 2
        sign_grid.append((fmt(b_), fmt(mm), fmt(kk)))

all_positive = all(D(r[2]) > 0 for r in sign_grid)
guard("no_sign_flip_factor_inside_framework", all_positive,
      "穷举 β=%s 五档 × (ξ 使 m_max=2m_μ) × m∈{m_e,m_μ}：物理支 κ(m) 全部 > 0（共 %d 点）"
      "⇒ 框架内不存在随粒子变号的因子" % ("/".join(fmt(x) for x in beta_list), len(sign_grid)))
INFO("II06", "定理（框架内无反号因子）：符号阻塞只能由**外部输入**解除",
     "对来料自身可用的全部因子逐一判定：①m>0；②κ(m) 在物理支恒正（β=%s 五档 × m∈{m_e,m_μ} "
     "共 %d 点机器确认全 > 0）；③sinθ>0；④cosθ 与 cotθ 因「全局唯一 θ」对所有粒子**同号**；"
     "⑤R_c=ξκ^{−β}>0；⑥(1−m/m_max)^{1/2} 在定义域内 ≥0（到 m_max 才归零，不变号）；"
     "⑦自能修正因子 (1−√(1−ε))>0。⇒ **没有任何因子可以只对 μ 变号而不对 e 变号**"
     "⇒ 符号阻塞不可能在 (θ,ξ,β) 内解决，必须引入**新的质量依赖自由度**（定理化，非数值巧合）"
     % ("/".join(fmt(x) for x in beta_list), len(sign_grid)),
     "与 r48 D01 的关系：r48 判「不可解」，本册给出「为什么不可解」的因子级穷举证明，"
     "并把出路收窄为唯一形态（II02）")

# II02/II03：最小破局形态 ⇒ 引入一个含零点的质量依赖因子 F(m)，最简 F(m)=1−m/m_0
def ratio_of_m0(m0_):
    F_e = 1 - m_e / m0_
    F_mu = 1 - m_mu / m0_
    return mm_ratio_sq * F_mu / F_e


# 单调性/唯一性：h(m_0) 在 (m_e, m_μ) 上严格单调递增（机器扫描确认）
mono_rows = []
prev = None
mono_ok = True
N_m0 = 40
for i in range(1, N_m0):
    x = m_e + (m_mu - m_e) * D(i) / D(N_m0)
    v = ratio_of_m0(x)
    mono_rows.append(v)
    if prev is not None and v <= prev:
        mono_ok = False
    prev = v
guard("m0_map_is_monotone", mono_ok,
      "h(m_0)=(m_μ/m_e)²·F_μ/F_e 在 (m_e,m_μ) 上 39 点扫描**严格单调递增**"
      "（从 %s 到 %s）⇒ 目标值 %s 的解**唯一**" % (fmt(mono_rows[0]), fmt(mono_rows[-1]), fmt(target_ratio)))

# 二分求 m_0
lo, hi = m_e * (1 + D("1e-12")), m_mu * (1 - D("1e-12"))
for _ in range(300):
    mid = (lo + hi) / 2
    if ratio_of_m0(mid) < target_ratio:
        lo = mid
    else:
        hi = mid
m0_sol = (lo + hi) / 2
resid_m0 = rel(ratio_of_m0(m0_sol), target_ratio)
guard("m0_solution_exists_and_unique", resid_m0 < D("1e-30"),
      "二分求得 m_0 = %s kg = %s MeV/c²，代回比值 %s vs 目标 %s（相对残差 %s）"
      % (fmt(m0_sol), fmt(m0_sol / GEV_OVER_C2 / 1000), fmt(ratio_of_m0(m0_sol)),
         fmt(target_ratio), fmt(resid_m0)))
m0_over_mu = m0_sol / m_mu
# kg -> GeV/c^2 除 GEV_OVER_C2；GeV -> MeV **乘** 1000（首版写成除，MeV 读数差 1e6，已被量级常识复核抓出）
m0_MeV = m0_sol / GEV_OVER_C2 * 1000
guard("m0_MeV_in_particle_range", D("0.5") < m0_MeV < D("106"),
      "单位换算自检：m_0 = %s MeV/c² 必须落在 m_e=0.511 与 m_μ=105.66 之间"
      "（首版把 GeV→MeV 写成除 1000，读数为 9.8e−5 MeV，被本 guard 拦下）" % fmt(m0_MeV))
guard("m0_lies_between_e_and_mu", (m_e < m0_sol < m_mu),
      "m_0 落在 (m_e, m_μ) 内：m_0/m_μ = %s，m_0/m_e = %s（介值定理的必要条件满足）"
      % (fmt(m0_over_mu), fmt(m0_sol / m_e)))
CORRECTED("II02", "符号阻塞的最小破局形态：必须在 (m_e,m_μ) 内引入一个新质量标度 m_0",
          "定理：设 a(m)=C·m·κ(m)·cotθ 且 F(m)≡κ(m)/κ_lin(m) 连续。要 sign a(m_e) ≠ sign a(m_μ)，"
          "由介值定理 F 必在 (m_e,m_μ) 内有**零点** ⇒ 必须引入一个质量标度 m_0（**+1 自由度**）。"
          "取最简含单零点的 F(m)=1−m/m_0，机器二分得 **m_0 = %s kg = %s MeV/c² = %s m_μ**，"
          "代回比值 %s 与目标 %s 相对残差 %s（唯一解，39 点单调性扫描确认）"
          % (fmt(m0_sol), fmt(m0_MeV), fmt(m0_over_mu), fmt(ratio_of_m0(m0_sol)),
             fmt(target_ratio), fmt(resid_m0)),
          "代价：+1 质量标度（撞 Ω5，除非登记为外部输入）；该标度 ≈%s MeV 不对应任何已知基本粒子质量"
          "（μ=105.66 MeV、π±=139.57 MeV）⇒ 目前是**纯拟合参数**，零独立预言（除 II05 的 a_τ）"
          % fmt(m0_MeV))

# II04 核心定理：量级阻塞与符号阻塞是**同一个比值条件** ⇒ 同一自由度
ratio_linear = mm_ratio_sq                     # F≡1 时的比值（凸性定理下界）
shortfall = ratio_linear / abs(target_ratio)
guard("same_single_condition", rel(ratio_of_m0(m0_sol), target_ratio) < D("1e-30"),
      "同一个 m_0 同时满足「符号（负号）」与「量级（|比值|=%s）」——二者不是两个阻塞，"
      "而是**同一个方程 a_μ/a_e=−3.3333E+3 的两面**" % fmt(abs(target_ratio)))
CORRECTED("II04", "本册核心定理：符号阻塞与量级阻塞是**同一自由度**（净增广 +1，不是 +2）",
          "r48 把两者列为 D01（符号）与 D02（量级）两条，本册证明它们其实是**同一个比值条件**："
          "a_μ/a_e = (m_μ/m_e)²·F(m_μ)/F(m_e) = −%s —— 负号即符号阻塞、绝对值即量级阻塞。"
          "纯线性 F≡1 给 +%s（比目标大 %s 倍，正是 r48 D02 的 12.83×）；"
          "一个参数 m_0 的 F(m)=1−m/m_0 **同时**给出正确的符号与正确的量级。"
          "⇒ **净增广 = +1 个质量标度**（另加原本就有的 θ），不是 +2"
          % (fmt(abs(target_ratio)), fmt(ratio_linear), fmt(shortfall)),
          "这是本册在**数值层**的结论：r48 判「不可解」是对的，且它不需要同时修符号和量级；"
          "但该 m_0 能挂在哪个载体上，由 III 组判定（本册自抓：最简载体 κ(m) 被几何封死）")

# II05 可证伪读数：m_0 被 e/μ 两点定死后，τ 的反常磁矩被唯一预言
F_e_sol = 1 - m_e / m0_sol
F_mu_sol = 1 - m_mu / m0_sol
F_tau_sol = 1 - m_tau / m0_sol
a_tau_pred = da_e * (m_tau / m_e) ** 2 * F_tau_sol / F_e_sol
a_mu_check = da_e * mm_ratio_sq * F_mu_sol / F_e_sol
guard("a_mu_reproduction_is_exact", rel(a_mu_check, da_mu) < D("1e-30"),
      "自检：用拟合出的 m_0 反算 a_μ = %s，与数据 Δa_μ = %s 相对残差 %s（两点定一参数，必然吻合）"
      % (fmt(a_mu_check), fmt(da_mu), fmt(rel(a_mu_check, da_mu))))
gap_to_bound = abs(a_tau_pred) / A_TAU_HI
guard("a_tau_prediction_is_not_yet_testable", gap_to_bound < 1,
      "预言 |a_τ| = %s < 实验上界 %s ⇒ **当前未被排除**；但仅占界限的 %s ⇒ 需精度提升 %s 倍才可达"
      % (fmt(abs(a_tau_pred)), fmt(A_TAU_HI), fmt(gap_to_bound), fmt(1 / gap_to_bound)))
INFO("II05", "最小增广的**唯一可证伪读数**：a_τ^TUFT = %s（对比界限与 SM）"
     % fmt(a_tau_pred),
     "m_0 被 e/μ 两点定死后不再有自由度 ⇒ τ 的反常磁矩被**唯一预言**："
     "a_τ = Δa_e·(m_τ/m_e)²·F(m_τ)/F(m_e) = %s（F(m_τ)=%s，F(m_e)=%s）。"
     "①实验界限（DELPHI 95%% CL）%s ~ %s ⇒ |a_τ^TUFT| 仅为上界的 %s ⇒ **未被排除但也不可检验**，"
     "需 τ 的 g−2 精度提升约 **%s 倍**（从 1e−2 到 1e−4 级）；"
     "②与 SM 预言 a_τ^SM = %s 相比，本预言为 %s（相对偏差 %s）⇒ 一旦精度到位即**可证伪**；"
     "③附带读数：F(m) 在 m=m_0≈%s MeV 处过零 ⇒ 预言该质量处反常磁矩为零，"
     "但该区间无带电基本粒子（μ=105.66 MeV、τ=1777 MeV）⇒ **无检验点**"
     % (fmt(a_tau_pred), fmt(F_tau_sol), fmt(F_e_sol),
        fmt(A_TAU_LO), fmt(A_TAU_HI), fmt(gap_to_bound), fmt(1 / gap_to_bound),
        fmt(A_TAU_SM), fmt(a_tau_pred), fmt(rel(a_tau_pred, A_TAU_SM)), fmt(m0_MeV)),
     "⇒ 这是「最小增广」能给出的最强可检验读数：**存在，但比现有实验精度低 %s 倍**"
     "（这是本册给「跑 dynesty 之前该先做什么」的答复：先把实验精度门槛算清）"
     % fmt(1 / gap_to_bound))

# ================================================================ III 组：载体层判定（本册自抓）
# II02 只证明了「数值上存在唯一 m_0」。本组问：这个 m_0 能挂在哪个载体上？
#   载体 A：塞进曲率剖面 F(m)=κ(m)/κ_lin(m)（II02 的默认理解）
#   载体 B：塞进耦合层 cotθ→cotθ(m) 或 C→C(m)
# 载体 A 的前提是 F(m) 在 (m_e,m_μ) 内过零；下面由机器检验该前提。


def _dpow(x, p):
    """Decimal 分数幂的安全实现（本库 r37 记录过 x**(1/3) 的坑）"""
    if isinstance(p, Fraction):
        if p.denominator == 1:
            return x ** int(p)
        return (x.ln() * (D(p.numerator) / D(p.denominator))).exp()
    p = D(p)
    if p == p.to_integral_value():
        return x ** int(p)
    return (x.ln() * p).exp()


def _m_of_kappa_factory(b_, xi_):
    B_ = 2 * PI * hbar * xi_ / (3 * c)
    p_ = D(2) - b_
    kstar = _dpow(A1_ / (p_ * B_), D(1) / (D(1) - b_))
    return (lambda kk: A1_ * kk - B_ * _dpow(kk, p_)), kstar


def _xi_for_mmax(b_, target_mmax):
    # m_max(ξ) 随 ξ 单调**递减** ⇒ m_max 偏大时应**增大** ξ
    # （首版方向写反，导致 κ(m) 落在物理支之外、F 值荒谬到 1e-319，被 III01 guard 当场拦下）
    lo_, hi_ = D("1e-40"), D("1e40")
    for _ in range(200):
        mid_ = (lo_ * hi_).sqrt()
        f_, ks_ = _m_of_kappa_factory(b_, mid_)
        if f_(ks_) > target_mmax:
            lo_ = mid_
        else:
            hi_ = mid_
    return (lo_ * hi_).sqrt()


def _kappa_of_m(b_, xi_, mm):
    f_, kstar = _m_of_kappa_factory(b_, xi_)
    a_lo, a_hi = kstar * D("1e-40"), kstar
    for _ in range(200):
        mid_ = (a_lo + a_hi) / 2
        if f_(mid_) < mm:
            a_lo = mid_
        else:
            a_hi = mid_
    return (a_lo + a_hi) / 2


# III01 F(m) 的正性扫描
Fscan = []
Fmin = None
Fmax = None
for b_ in beta_list:
    xi_b = _xi_for_mmax(b_, 2 * m_mu)
    for i in range(1, 13):
        mm = m_mu * (D("0.05") + D("1.85") * D(i) / D(12))
        kk = _kappa_of_m(b_, xi_b, mm)
        Fv = kk * hbar / (mm * c)                 # F = κ/κ_lin，κ_lin = m c/ħ
        Fscan.append(Fv)
        if Fmin is None or Fv < Fmin:
            Fmin = Fv
        if Fmax is None or Fv > Fmax:
            Fmax = Fv
allF_positive = all(x > 0 for x in Fscan)
guard("kappa_ratio_F_has_no_zero_on_positive_mass", allF_positive and Fmin > D("1e-6"),
      "β=%s 五档 × m∈(0.05,1.90)m_μ 十二点（共 %d 点）：F(m)=κ(m)/κ_lin(m) ∈ [%s, %s] 全部 > 0，"
      "且最小值 %s 远离 0 ⇒ **F 在 m>0 上无零点**"
      % ("/".join(fmt(x) for x in beta_list), len(Fscan), fmt(Fmin), fmt(Fmax), fmt(Fmin)))

mm_small = m_e * D("1e-6")
kk_small = _kappa_of_m(beta_list[0], _xi_for_mmax(beta_list[0], 2 * m_mu), mm_small)
F_small = kk_small * hbar / (mm_small * c)
guard("weak_field_limit_F_tends_to_sin_theta", rel(F_small, D(1)) < D("1e-6"),
      "弱场极限 m→0：F(m)=%s → sinθ=1（相对残差 %s）⇒ 与 r44「弱场 κ≈mc sinθ/ħ」逐位同源，"
      "且 F 从正值侧趋近 1，**不可能在该侧过零**" % (fmt(F_small), fmt(rel(F_small, D(1)))))

# 解析层面的死锁：来料 m(κ)=A₁κ−Bκ^p 满足 κ=0 ⇔ m=0 ⇒ F 的零点只能在 m=0
B_demo = 2 * PI * hbar * _xi_for_mmax(beta_list[0], 2 * m_mu) / (3 * c)
m_at_zero = A1_ * D(0) - B_demo * _dpow(D(0), D(2))
guard("F_strictly_greater_than_one", Fmin > D(1),
      "解析（比扫描更强）：m(κ)=A₁κ−Bκ^{2−β} 且 B>0、κ>0 ⇒ m < A₁κ ⇒ κ > m/A₁ = κ_lin（本册 sinθ=1）"
      " ⇒ F=κ/κ_lin **恒严格 > 1**；机器扫描最小 F=%s > 1 ⇒ **F 连趋近 0 都不可能**" % fmt(Fmin))
guard("m_of_kappa_zero_iff_kappa_zero", m_at_zero == 0,
      "来料质量映射 m(κ)=A₁κ−Bκ^{2−β}：κ=0 ⇒ m=%s（机器零）⇒ F=κ/κ_lin 的零点只可能在 m=0"
      % fmt(m_at_zero))

FAIL("III01", "最简破局形态 F(m)=1−m/m_0 可挂到曲率剖面 κ(m) 上",
     "四条独立判据同时封死：①几何 — Frenet 曲率 **κ≥0** 由定义，κ_lin=mc/ħ>0 ⇒ F=κ/κ_lin ≥ 0；"
     "②机器扫描 — %d 点（β 五档 × m∈(0.05,1.90)m_μ）F ∈ [%s, %s]，最小 %s **> 1**；"
     "③解析 A — m(κ)=A₁κ−Bκ^{2−β}（B>0）⇒ m<A₁κ ⇒ **F 恒严格 > 1**，连趋近 0 都不可能；"
     "④解析 B — 来料 m(κ) 满足 κ=0 ⇔ m=0 ⇒ F 的零点只可能在 m=0，而 m_0=%s MeV ≫ 0 ⇒ **矛盾**。"
     "⇒ **变号因子不能塞进 κ(m)**"
     % (len(Fscan), fmt(Fmin), fmt(Fmax), fmt(Fmin), fmt(m0_MeV)),
     "这是本册对自己的 II02 的**自抓修正**（II02 默认把 m_0 放进 κ，机器判定该载体不合法）；"
     "m_0 的数值仍成立（作为比值方程的解），但必须换载体")

# III02 m_0 的自然性：能否由框架常数的低阶幂构造
DIM_HBAR = Dim(1, 2, -1)
DIM_C = Dim(0, 1, -1)
DIM_G = Dim(-1, 3, -2)
DIM_ME = Dim(1, 0, 0)
par_dims = [DIM_HBAR, DIM_C, DIM_G, DIM_ME]
par_vals = [hbar, c, Gexp, m_e]
RNG = range(-3, 4)


def _hits_for(target_val):
    out = []
    for a in RNG:
        for b in RNG:
            for d in RNG:
                for e2 in RNG:
                    exps = (Fraction(a), Fraction(b), Fraction(d), Fraction(e2))
                    acc = [Fraction(0)] * 4
                    for k in range(4):
                        for j in range(4):
                            acc[j] += exps[k] * par_dims[k][j]
                    if tuple(acc) == (Fraction(1), Fraction(0), Fraction(0), Fraction(0)):
                        val = D(1)
                        for k in range(4):
                            val *= _dpow(par_vals[k], exps[k])
                        if rel(val, D(target_val)) < D("1e-6"):
                            out.append((str(a), str(b), str(d), str(e2)))
    return out


hits_m0 = _hits_for(m0_sol)
hits_me = _hits_for(m_e)
hits_mmu = _hits_for(m_mu)
guard("naturalness_scan_has_positive_control", len(hits_me) >= 1 and len(hits_mmu) == 0,
      "阳性对照：同一穷举（ħ,c,G,m_e 的 ±3 幂，共 2401 组合）对目标 m_e 命中 %d 组、"
      "对目标 m_μ 命中 %d 组 ⇒ 检验器既非恒命中也非恒不命中" % (len(hits_me), len(hits_mmu)))
guard("m0_is_not_constructible_from_framework_constants", len(hits_m0) == 0,
      "对目标 m_0 命中 **%d 组** ⇒ m_0=%s MeV 不能由 {ħ,c,G,m_e} 的低阶幂构造 ⇒ **纯外部输入**"
      % (len(hits_m0), fmt(m0_MeV)))
m_pi = D("139.57039") * GEV_OVER_C2 / 1000
m_pr = D("938.27208816") * GEV_OVER_C2 / 1000
INFO("III02", "m_0 无框架内来源（穷举 0 命中）且不对应任何已知粒子",
     "穷举 {ħ,c,G,m_e} 的 ±3 次幂（2401 组，量纲先筛纯质量维）：命中 m_0 的组合数 = **%d**，"
     "命中 m_e = %d（阳性对照，检验器有效），命中 m_μ = %d。"
     "m_0 = %s MeV/c² 与 m_μ=105.66（相对偏差 %s）、m_π±=139.57（%s）、m_p=938.27（%s）全不等"
     " ⇒ 该标度**既不可由框架常数构造，也不落在任何已知基本粒子质量上**"
     % (len(hits_m0), len(hits_me), len(hits_mmu), fmt(m0_MeV),
        fmt(rel(m0_sol, m_mu)), fmt(rel(m0_sol, m_pi)), fmt(rel(m0_sol, m_pr))),
     "⇒ 即便换到合法载体，这个质量标度仍然是**纯拟合参数**，无独立来源（撞 Ω5 且无处登记来源）")

# III03 唯一几何一致的载体 = 耦合层 ⇒ 自由度从常数升为函数
CORRECTED("III03", "本册核心定理（最终形态）：破局因子只能进耦合层 ⇒ 代价是**函数**而非常数",
          "载体穷举：a(m)=C·m·κ(m)·cotθ 中可变号的因子只有 ①κ(m)（被 III01 三条判据封死："
          "几何非负、%d 点机器扫描全正、m(κ) 解析 κ=0⇔m=0）、②m（恒正）、③cotθ（全局唯一 θ ⇒ "
          "对所有粒子同号）。⇒ **唯一剩余载体是把 θ 或 C 提升为质量的函数**："
          "cotθ → cotθ(m) 或 C → C(m)，即在 (m_e,m_μ) 内过零。"
          "⇒ **自由度形态从「+1 个常数 m_0」升级为「+1 个自由函数 θ(m)/C(m)」**"
          % len(Fscan),
          "按 r15 的三口径记账：口径 I（只数连续常数）下是 +1；口径 II/III（含自由函数）下是**无界**。"
          "⇒ r48 的「不可解」成立，且本册给出「为什么不能便宜地修」：常数级修补与几何自洽**互斥**")

# III04 两难的结构性读数
BOUNDARY("III04", "耦合层载体的两条支路各有硬代价（不代选）",
         "支路 ① θ→θ(m)：cotθ 在 m_0 过零 ⇒ θ(m_0)=π/2 ⇒ **cosθ=0 ⇒ τ/κ=cotθ=0 ⇒ 挠率在该质量处归零**"
         " ⇒ 该粒子完全不受挠率效应影响，与 V4.7「挠率驱动反常磁矩」的定位自相矛盾；"
         "且 θ 非常数 ⇒ 来料 G_th∝1/sinθ 之类关系使 **G 不再是常数**（复发 r41 M2 二阶两难 B："
         "θ 为场 ⇒ G_th 非常数，与 G 的 CODATA 精度 ~1.5e−4 冲突）。"
         "支路 ② C→C(m)：反常磁矩的整体系数随质量变 ⇒ 等于承认耦合常数非普适，"
         "与「四力同源、单一 θ」的纲领定位冲突，且 C(m) 无任何方程约束 ⇒ 完全自由。",
         "⇒ 两条支路都**不在现有公设集内**，属「修改公设集」层级（与 r14 出路④同型），须用户裁决")

# ================================================================ IV 组：可证伪读数的最终定位
# II05 的 a_τ 唯一预言依赖「m_0 是唯一自由度」。III03 后载体是函数 ⇒ 1 函数 / 2 数据点 ⇒ 欠定。
FAIL("IV01", "在几何一致的载体下仍存在唯一可证伪读数（a_τ）",
     "II05 的 a_τ=%s 之所以唯一，是因为载体为「单常数 m_0」时 2 个数据点（e/μ）恰好定死 1 个参数。"
     "III03 判定合法载体是**函数 θ(m)/C(m)** ⇒ 自由度无界而数据点仍为 2 ⇒ "
     "a_τ 可被任意函数取值吸收 ⇒ **唯一预言消失**（复发第十二轮步3 的可识别性结论："
     "连续函数 + 有限数据 ⇒ 零判别力）" % fmt(a_tau_pred),
     "⇒ 本册对「先跑 dynesty 还是先补判据」的答复进一步收紧："
     "在载体未由公设层固定之前，任何拟合（含 MCMC/dynesty）都只是在拟合一个自由函数的取值")

CORRECTED("IV02", "代价总账：从「+1 常数」到「无界函数」，且无任何增广降低总自由度",
          "轮廓层（I 组）与拟合层（II/III 组）合并记账："
          "①轮廓层最小合法增广 = **均匀平滑源**（+1 源强度 S₀ 与 +1 源形状约定；"
          "点源因自能幂次发散不合法；自洽源把 β 换位为 s，自由度不减；Helmholtz 谱对质量比零判别力）；"
          "②拟合层最小数值增广 = 1 个质量标度 m_0=%s MeV（唯一，残差 %s）；"
          "③但该标度**不能挂在 κ 上**（III01 三条判据）⇒ 合法载体是函数 ⇒ **自由度无界**。"
          "⇒ 三层合计：**总自由度只增不减**，且 Ω5（自由常数 ≤1）在任何一层都被撞"
          % (fmt(m0_MeV), fmt(resid_m0)),
          "红线：本册不代选方向。所有「增广」仅登记存在性、唯一性与代价，不构成推荐")

# ================================================================ 开放项 / 非自推登记
OPEN_ITEMS.append(dict(
    id="O-R53-1", kind="载体未定",
    text="破局因子的合法载体有两条支路（θ(m) 与 C(m)），二者自由度结构与物理后果不同（III04），未代选"))
OPEN_ITEMS.append(dict(
    id="O-R53-2", kind="外部输入",
    text="质量标度 m_0=%s MeV 在 {ħ,c,G,m_e} 的 ±3 次幂穷举中命中 0 组，且不对应任何已知粒子质量"
         % fmt(m0_MeV)))
OPEN_ITEMS.append(dict(
    id="O-R53-3", kind="可检验性",
    text="a_τ 预言 |a_τ|=%s 仅为 DELPHI 上界的 %s，需 τ 的 g−2 精度提升约 %s 倍才可达"
         % (fmt(abs(a_tau_pred)), fmt(gap_to_bound), fmt(1 / gap_to_bound))))
OPEN_ITEMS.append(dict(
    id="O-R53-4", kind="源项形式未定",
    text="轮廓层四条增广（点源/均匀源/自洽幂次源/自洽 Helmholtz）代价与判别力各不相同（I06），未代选"))

NOT_SELF_DERIVED.append(
    "m_0 的数值由 e/μ 两组实验数据反解得到，非第一性推导（二分残差 %s）" % fmt(resid_m0))
NOT_SELF_DERIVED.append(
    "τ 反常磁矩实验界限 (−0.052, 0.013) 为 DELPHI 95% CL 文献值；a_τ^SM=1.17721e-3 引自文献，仅作对照")
NOT_SELF_DERIVED.append(
    "Δa_e 与 Δa_μ 取自实验与 SM 理论值之差（CODATA / Fermilab—SM 口径），本册只引用不复算")
NOT_SELF_DERIVED.append(
    "Frenet 曲率 κ≥0（几何非负）与来料质量映射 m(κ)=A₁κ−Bκ^{2−β} 均取自来料，本册只检验不推导")


# ================================================================ 输出
def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    bad = [g for g in GUARDS if not g["passed"]]
    if bad:
        print("[%s] GUARD FAILED %d / %d —— 禁止输出结论" % (ROUND, len(bad), len(GUARDS)))
        for g in bad:
            print("  FAIL-GUARD %s :: %s" % (g["name"], g["detail"]))
        return 2
    counts = {}
    for r in RECORDS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    payload = dict(
        round=ROUND, stamp=STAMP, name=NAME,
        source="TUFT-V4.7 分支2（r48 下游）：最小增广与可解性定理",
        guards_total=len(GUARDS), guards_passed=len(GUARDS),
        counts=counts,
        key_numbers=dict(
            da_e=fmt(da_e), da_mu=fmt(da_mu),
            target_ratio=fmt(target_ratio),
            mm_ratio_sq=fmt(mm_ratio_sq),
            m0_solution_kg=fmt(m0_sol),
            m0_solution_MeV=fmt(m0_MeV),
            m0_over_mu=fmt(m0_over_mu),
            m0_residual=fmt(resid_m0),
            a_tau_prediction=fmt(a_tau_pred),
            a_tau_gap_to_bound=fmt(gap_to_bound),
            a_tau_precision_factor_needed=fmt(1 / gap_to_bound),
            F_scan_min=fmt(Fmin), F_scan_max=fmt(Fmax), F_scan_points=len(Fscan),
            point_source_divergence_ratio=fmt(div_ratio),
            naturalness_hits_m0=len(hits_m0),
            naturalness_hits_me=len(hits_me),
            naturalness_hits_mmu=len(hits_mmu),
            uniform_source_self_energy=fmt(self_en_unif)),
        records=RECORDS, guards=GUARDS,
        open_items=OPEN_ITEMS, not_self_derived=NOT_SELF_DERIVED,
        red_line="数学自洽 ≠ 物理证实；本册不代选方向、不产生新物理")
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    with io.open(os.path.join(OUT_DIR, NAME + ".json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
    # 数据 md 与纯文本报告（与 r44/r45/r50/r51 同构）
    md = ["# %s" % NAME, "",
          "- 轮次：%s　日期：%s　guard：%d/%d PASS" % (ROUND, STAMP, len(GUARDS), len(GUARDS)),
          "- 条目计数：%s" % counts, "",
          "## 关键读数", ""]
    for k, v in payload["key_numbers"].items():
        md.append("- `%s` = %s" % (k, v))
    md += ["", "## 条目", ""]
    for r in RECORDS:
        md += ["### %s　%s" % (r["id"], r["verdict"]), "",
               "- 判定对象：%s" % r.get("claim", ""),
               "- 机器读数：%s" % r.get("reading", ""),
               "- 备注：%s" % r.get("note", ""), ""]
    md += ["## 开放项", ""]
    for it in OPEN_ITEMS:
        md.append("- `%s`（%s）：%s" % (it["id"], it["kind"], it["text"]))
    md += ["", "## 非自推登记", ""]
    for s in NOT_SELF_DERIVED:
        md.append("- %s" % s)
    md += ["", "> 红线：%s" % payload["red_line"], ""]
    with io.open(os.path.join(OUT_DIR, NAME + ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    rep = ["%s  %s" % (ROUND, STAMP),
           "guards %d/%d PASS" % (len(GUARDS), len(GUARDS)),
           "counts %s" % counts, ""]
    for r in RECORDS:
        rep.append("[%s] %s :: %s" % (r["verdict"], r["id"], r.get("claim", "")))
    rep.append("")
    for k, v in payload["key_numbers"].items():
        rep.append("%s = %s" % (k, v))
    with io.open(os.path.join(OUT_DIR, NAME + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(rep) + "\n")
    print("[%s] guards %d/%d PASS" % (ROUND, len(GUARDS), len(GUARDS)))
    print("[%s] counts %s" % (ROUND, counts))
    print("[%s] m0 = %s MeV  a_tau = %s  gap = %s" % (ROUND, fmt(m0_MeV), fmt(a_tau_pred), fmt(gap_to_bound)))
    print("[%s] F scan min = %s (%d pts)  naturalness hits(m0) = %d"
          % (ROUND, fmt(Fmin), len(Fscan), len(hits_m0)))
    print("[%s] json -> %s" % (ROUND, os.path.join(OUT_DIR, NAME + ".json")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
