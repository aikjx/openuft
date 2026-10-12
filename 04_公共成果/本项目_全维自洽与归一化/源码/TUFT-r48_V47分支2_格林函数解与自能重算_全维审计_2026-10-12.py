# -*- coding: utf-8 -*-
"""
TUFT-V4.7｜分支2：∇²κ=0 格林函数解 + 线性球包 + R_c=ξκ^{-β} 幂律耦合 —— 全维审计（r48）

来料：《TUFT-V4.7｜分支2：∇²κ=0 格林函数解，替换指数衰减轮廓，重算自能，抬升稳态质量上限（算法联盟）》

分工（零重复声明）：r44 审 V4.3/V4.4 的 g-2 联合拟合链与自能 ansatz；r45 审 V4.5 的变分导出链 +
指数局域包 + 二次映射 + χ² 代码；**本册审 V4.7 分支2**：调和（"格林函数"）方程解 + 线性球包 +
R_c=ξκ^{-β} 幂律耦合 + β 折中 + m_max 抬升 + 3 参数 dynesty 代码。不重算 r44/r45 已给出的数值，
只做回链交叉印证（r42 的 a_mu 读数、r45 的 4.878E+21 定义域读数均作为独立交叉核对点）。

引擎：纯标准库（Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)）
纪律：任何「恒等于零」裁定必须配阳性对照（r45 纪律）；量纲工具必须先过 guard 再用于判定（r37/r44/r45 三次同族事故）。
红线：数学自洽 != 物理证实；本册只复算来料公式 + 诚实标注边界，不产生新物理。
"""
from __future__ import print_function
import sys, os, io, json
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(BASE), "数据")
STAMP = "2026-10-12"
NAME = "TUFT-r48_V47分支2_格林函数解与自能重算_全维审计_%s" % STAMP

D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194913")

# ---------------------------------------------------------------- CODATA（与 r45 逐位同源）
c     = D("299792458")
hbar  = D("1.0545718176461565e-34")
e_ch  = D("1.602176634e-19")
m_e   = D("9.1093837015e-31")
m_mu  = D("1.883531627e-28")
m_tau = D("3.16754e-27")            # 来料 χ² 代码硬编码值
Gexp  = D("6.67430e-11")
lP_nominal = D("1.616255078e-35")   # 来料 χ² 代码硬编码值
lP_derived = (hbar * Gexp / (c ** 3)).sqrt()
kg_per_GeV = D("1.78266192e-27")    # 1 GeV/c^2

a_e_exp  = D("1.15965218059e-3")
a_e_th   = D("1.15965218128e-3")
a_mu_exp = D("1.16592040e-3")
a_mu_th  = D("1.16591810e-3")
da_e = a_e_exp - a_e_th             # -6.9e-13
da_mu = a_mu_exp - a_mu_th          # +2.30e-9

sigma_e_claim = D("1e-12")          # 来料 χ²
sigma_mu_claim = D("4e-7")
sigma_e_real = D("2.8e-14")         # r44/r45 登记的真实口径
sigma_mu_real = D("5.2e-10")
sigma_G_rel = D("1e-5")             # 来料 χ² 用 Gexp*1e-5

# ---------------------------------------------------------------- 量纲工具
def Dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dadd(a, b):
    return tuple(a[i] + b[i] for i in range(4))

def dmul(a, b):
    """量纲相乘 = 指数相加。r37/r44/r45 各踩过一次「写成逐分量相乘」，本册由 G0-1 当场拦下。"""
    return tuple(a[i] + b[i] for i in range(4))

def dscale(a, k):
    return tuple(a[i] * Fraction(k) for i in range(4))

def dinv(a):
    return tuple(-x for x in a)

def dpow(a, p):
    p = Fraction(p)
    return tuple(a[i] * p for i in range(4))

def deq(a, b):
    return all(a[i] == b[i] for i in range(4))

dONE    = Dim()
dM      = Dim(1, 0, 0)
dL      = Dim(0, 1, 0)
dT      = Dim(0, 0, 1)
dQ      = Dim(0, 0, 0, 1)
dC      = Dim(0, 1, -1)
dH      = Dim(1, 2, -1)
dEnergy = Dim(1, 2, -2)
dKappa  = Dim(0, -1)
dGrad2  = Dim(0, -4)
dVol    = Dim(0, 3, 0)

def _num(fr):
    if fr.denominator == 1:
        return str(fr.numerator)
    return "%s/%s" % (fr.numerator, fr.denominator)

def dstr(a):
    sym = ["M", "L", "T", "Q"]
    out = []
    for i in range(4):
        if a[i] == 0:
            continue
        if a[i] == 1:
            out.append(sym[i])
        else:
            out.append("%s^%s" % (sym[i], _num(a[i])))
    return "".join(out) if out else "1"

# ---------------------------------------------------------------- 数值工具
def dpow_dec(x, p):
    """Decimal 的实数幂：x^p（x>0）。Python3.8 下不用 **（分数指数不稳）。"""
    p = D(str(p))
    if p == 0:
        return D(1)
    if x <= 0:
        raise ValueError("dpow_dec 需要正数")
    return (x.ln() * p).exp()

def _dsin(x):
    s = D(0); term = x; k = 0
    while k <= 300:
        s += term
        k += 1
        term = -term * x * x / D((2 * k) * (2 * k + 1))
        if term == 0:
            break
    return s

def _dcos(x):
    s = D(0); term = D(1); k = 0
    while k <= 300:
        s += term
        k += 1
        term = -term * x * x / D((2 * k - 1) * (2 * k))
        if term == 0:
            break
    return s

def _f(x, n=12):
    return format(x, ".%dE" % n)

def rel(a, b):
    """相对偏差 |a-b|/max(|a|,|b|)"""
    m = max(abs(a), abs(b))
    if m == 0:
        return D(0)
    return abs(a - b) / m

# ---------------------------------------------------------------- 记录器
RECORDS = []
GUARDS = []
OPEN_ITEMS = []
NOT_SELF_DERIVED = []

def _emit(kind, cid, claim, reading, note=""):
    RECORDS.append(dict(id=cid, verdict=kind, claim=claim,
                        machine_reading=reading, note=note))

def PASS(cid, claim, reading, note=""): _emit("PASS", cid, claim, reading, note)
def FAIL(cid, claim, reading, note=""): _emit("FAIL", cid, claim, reading, note)
def BOUNDARY(cid, claim, reading, note=""): _emit("BOUNDARY", cid, claim, reading, note)
def INFO(cid, claim, reading, note=""): _emit("INFO", cid, claim, reading, note)
def CORRECTED(cid, claim, reading, note=""): _emit("CORRECTED", cid, claim, reading, note)
def MISMATCH(cid, claim, reading, note=""): _emit("MISMATCH", cid, claim, reading, note)

def guard(name, ok, detail):
    GUARDS.append(dict(name=name, passed=bool(ok), detail=detail))
    return bool(ok)

# ================================================================ G0 量纲工具自检
guard("dim_mul_additive_not_multiplicative",
      deq(dmul(dL, dL), Dim(0, 2, 0)) and deq(dmul(dL, dinv(dL)), dONE),
      "dmul(L,L)=%s ; dmul(L,1/L)=%s" % (dstr(dmul(dL, dL)), dstr(dmul(dL, dinv(dL)))))
guard("dim_pow_and_scale",
      deq(dpow(dL, 3), Dim(0, 3, 0)) and deq(dscale(dL, D("0.5")), Dim(0, Fraction(1, 2), 0)),
      "dpow(L,3)=%s ; dscale(L,1/2)=%s" % (dstr(dpow(dL, 3)), dstr(dscale(dL, D("0.5")))))
guard("dim_energy_chain",
      deq(dmul(dmul(dH, dC), dKappa), dEnergy),
      "[hbar*c*kappa]=%s 应为 %s" % (dstr(dmul(dmul(dH, dC), dKappa)), dstr(dEnergy)))
guard("dim_kappa_is_inverse_length", deq(dKappa, Dim(0, -1, 0)),
      "[kappa]=%s" % dstr(dKappa))
guard("trig_identity_positive_control",
      rel(_dsin(D("1")) ** 2 + _dcos(D("1")) ** 2, D(1)) < D("1e-50"),
      "sin^2(1)+cos^2(1)-1 = %s" % _f(_dsin(D("1")) ** 2 + _dcos(D("1")) ** 2 - 1))
guard("pi_guard_sin_pi_over_6",
      rel(_dsin(PI / 6), D("0.5")) < D("1e-50"),
      "sin(pi/6)=%s" % _f(_dsin(PI / 6)))

# ================================================================ A 组：方程层
Rc_ = D(1)
kap0_ = D(1)

def kap_profile(r):
    return kap0_ * (1 - r / Rc_)

# A01 来料显式解是否满足它自己的方程
lap_rows = []
fd_ok = True
for r_ in [D("0.25"), D("0.5"), D("0.75")]:
    k_p = kap_profile(r_ + D("1e-12"))
    k_m = kap_profile(r_ - D("1e-12"))
    k_0 = kap_profile(r_)
    d1 = (k_p - k_m) / (2 * D("1e-12"))
    d2 = (k_p - 2 * k_0 + k_m) / (D("1e-12") ** 2)
    lap_fd = d2 + 2 * d1 / r_
    lap_an = D(0) + 2 * (-kap0_ / Rc_) / r_
    if rel(lap_fd, lap_an) > D("1e-30"):
        fd_ok = False
    lap_rows.append((str(r_), _f(lap_an), _f(lap_fd)))
norm_resid = abs(D(-4)) / (abs(D(-4)) + abs(D(0)))   # r=Rc/2: kappa''=0, (2/r)kappa'=-4
FAIL("A01", "来料称 κ(r)=κ₀(1−r/R_c) 是 ∇²κ=0 球对称有限域唯一非平凡正则解",
     "∇²κ = κ''+2κ'/r = −2κ₀/(rR_c) ≠ 0：r=0.25/0.5/0.75 处解析值 %s / %s / %s（差分对拍逐位一致）；"
     "r=R_c/2 处 = −4κ₀/R_c²，归一化残差 = %s（100%%）。该函数是**一维平面** Laplace 方程 κ''=0 的解，"
     "球对称三维径向拉普拉斯多了 2κ'/r 项"
     % (lap_rows[0][1], lap_rows[1][1], lap_rows[2][1], _f(norm_resid, 6)),
     "来料把 d/dr(r²dκ/dr) 的 r² 权重漏掉了；正确通解是 C₁+C₂/r，不是线性函数")
guard("laplacian_fd_vs_analytic", fd_ok, "差分与解析逐点一致（对拍通过，排除我自己的代数失误）")

# 阳性对照：真正的调和函数 C1+C2/r 必须给出 0
C1p, C2p = D(2), D("0.5")
def kap_harm(r):
    return C1p + C2p / r
pc_rows = []
for r_ in [D("0.25"), D("0.5"), D("0.75")]:
    h = D("1e-10")
    d1 = (kap_harm(r_ + h) - kap_harm(r_ - h)) / (2 * h)
    d2 = (kap_harm(r_ + h) - 2 * kap_harm(r_) + kap_harm(r_ - h)) / (h * h)
    pc_rows.append(_f(d2 + 2 * d1 / r_))
# 注意：_f 输出是 "尾数E指数" 的科学计数法字符串，判"≈0"必须整体 D(x) 解析，
# 不能只取 "E" 前的尾数（首版写成 x.split("E")[0] ⇒ 拿 4.0 当 4e-40 ⇒ 假 FAIL，12/13 抓出）
guard("harmonic_positive_control_is_zero",
      all(abs(D(x)) < D("1e-25") for x in pc_rows),
      "阳性对照：κ=C₁+C₂/r 的 ∇²κ 在三点均 ≈0（%s / %s / %s），检验器非恒零" % tuple(pc_rows))

# A02 有限域正则 BVP 只有平凡解
triv_rows = []
for eps_r in ["1e-1", "1e-3", "1e-6", "1e-9"]:
    eps = Rc_ * D(eps_r)
    C2v = kap0_ * eps * Rc_ / (Rc_ - eps)
    C1v = -C2v / Rc_
    k_half = C1v + C2v / (D("0.5") * Rc_)
    triv_rows.append((eps_r, _f(k_half / kap0_)))
FAIL("A02", "来料称该 BVP『唯一非平凡正则解』存在",
     "∇²κ=0 的球对称通解 κ=C₁+C₂/r：原点正则 ⇒ C₂=0 ⇒ κ≡C₁；边界 κ(R_c)=0 ⇒ C₁=0 ⇒ **κ≡0**。"
     "以内半径 ε 正则化后场幅随 ε 线性趋于 0：ε/R_c=1e-1/1e-3/1e-6/1e-9 ⇒ κ(R_c/2)/κ₀ = %s / %s / %s / %s"
     % (triv_rows[0][1], triv_rows[1][1], triv_rows[2][1], triv_rows[3][1]),
     "即调和函数最大值原理：边界归零 + 内部无源 ⇒ 内部恒零。与 r45 T03/T04/T05 同结论、独立复算。")

# A03 若按格林函数真义必须有源 ⇒ 1/r ⇒ 自能幂次发散
div_rows = []
for eps_r in ["1e-1", "1e-3", "1e-6", "1e-9"]:
    eps = Rc_ * D(eps_r)
    val = (1 / eps - 1 / Rc_) * Rc_          # 以 1/R_c 为单位
    div_rows.append((eps_r, _f(val)))
FAIL("A03", "来料用『格林函数解』命名该轮廓",
     "格林函数对应**非齐次**方程 ∇²G=−4πδ³(r)（解 G=1/r），而 ∇²κ=0 是齐次无源方程 ⇒ 名实不符；"
     "且 r45 T03 已证 V(κ)≡0 ⇒ 无源 ⇒ 无格林函数非平凡解。若真取点源解 κ=C(1/r−1/R_c)，"
     "则 |∇κ|²=C²/r⁴，∫4πr²|∇κ|²dr = 4πC²(1/r_min−1/R_c) **幂次发散**："
     "r_min/R_c=1e-1/1e-3/1e-6/1e-9 ⇒ %s / %s / %s / %s（每十倍程 ×10）"
     % (div_rows[0][1], div_rows[1][1], div_rows[2][1], div_rows[3][1]),
     "且 κ(0) 发散，与来料物理约束『原点正则』直接冲突")

# A04 概念互斥
FAIL("A04", "§6 自评『✅ 严格求解 ∇²κ=0 格林函数，移除指数包经验假设』",
     "齐次方程 ∇²κ=0 无格林函数解（格林函数必须有源）；A01 的轮廓非解；A02 的 BVP 只有零解；"
     "A03 的真格林函数解发散。四条独立路径同指：分支2 的轮廓层在球对称有限域内**无可用解**。",
     "与 r45 §8 选项2『格林函数不可执行』同结论，本册补出具体落点（漏 2κ'/r 项 + 无源 + 发散）")

# A05 算术 PASS
Nn = 20000
acc = D(0)
for i in range(Nn):
    rr = Rc_ * (D(i) + D("0.5")) / D(Nn)
    acc += 4 * PI * rr * rr * (kap0_ / Rc_) ** 2 * (Rc_ / D(Nn))
int_exact = (D(4) / 3) * PI * Rc_ * kap0_ ** 2
guard("volume_integral_arithmetic", rel(acc, int_exact) < D("1e-6"),
      "∫4πr²dr·(κ₀²/R_c²) 数值 %s vs 解析 %s" % (_f(acc), _f(int_exact)))
PASS("A05", "§2 的体积分算术（含 4π/3 系数）",
     "∫₀^{R_c}4πr²dr·κ₀²/R_c² = (4π/3)R_cκ₀²：黎曼和 %s vs 解析 %s，相对偏差 %s ⇒ **算术正确**"
     % (_f(acc), _f(int_exact), _f(rel(acc, int_exact), 6)),
     "但该算术建立在一个非解轮廓上（A01），正确不等于可用")

# A06 释放 R_c 确实解除了 r45 的定义域阻塞（真实进步）
A1 = hbar / c                                   # sinθ=1
dom_v45 = 2 * PI * m_e * c ** 2 / hbar          # r45 读数：1/sin²θ > 2πmc²/ħ
mmax_fixed = 3 * hbar / (8 * PI * c * lP_nominal)
guard("crosscheck_r45_domain_reading", rel(dom_v45, D("4.878E+21")) < D("1e-3"),
      "本册复算 2πm_e c²/ħ = %s，r45 登记 4.878E+21（独立交叉核对通过）" % _f(dom_v45))
CORRECTED("A06", "『R_c 不再强制等于 l_P，作为场局域化边界尺度』",
          "这一步**确有实质改善**：r45 的阻塞（1/sin²θ>2πmc²/ħ，电子项 %s，需 θ<1.43e-11 rad，"
          "全部真实粒子恒无实根）在 R_c 自由后消失——最小修正版判别式给出 m < 3ħ/(8πcR_c sin²θ)，"
          "R_c=l_P 时上限 %s kg ≫ m_e。⇒ 定义域阻塞被正确定位为『尺度绑死 l_P』，解除方式有效"
          % (_f(dom_v45), _f(mmax_fixed)),
          "但代价见 C05：m_max 变为 ξ 的连续可调函数 ⇒ 由『不可能』变成『零判别力』")

# A07 不可能三角
INFO("A07", "分支2 的三条件不可能三角",
     "『∇²κ=0（无源）』+『κ(R_c)=0（边界归零）』+『κ(0)=κ₀≠0（原点非平凡）』三者不可兼得："
     "任取两条可满足（放弃第 3 条 ⇒ κ≡0；放弃第 2 条 ⇒ κ=常数非局域；放弃第 1 条 ⇒ 需源项 ⇒ 1/r 发散）。"
     "⇒ 分支2 的可行域是空集，不是『尚未找到解』。",
     "与 r45『有界-衰减调和函数唯一性判据』同族，本册给出有限域边界条件版本")

# A08 UV 主导
div_ratios = [D(div_rows[i][1].split("E")[0]) for i in range(len(div_rows))]
BOUNDARY("A08", "『R_c 为新的场局域化尺度』",
         "若按 A03 的真格林函数解，自能 = 4πC²(1/r_min−1/R_c) 完全由**内截断 r_min** 主导，"
         "R_c 只出现在可忽略的 −1/R_c 项 ⇒ R_c 不是自由尺度而是 UV 敏感量的残余参数"
         "（1e-9 相对 1e-1 相差 %s 倍）。复发 r37/r45 的『标度由截断主导 ⇒ 无预言力』族。"
         % _f(div_ratios[3] / div_ratios[0], 6),
         "不代选：是否改用带源 Poisson 方程须由公设层决定")

# ================================================================ B 组：量纲层
# B01 [U_self]
dim_U = dmul(dmul(dmul(dH, dinv(dC)), dL), dpow(dKappa, 2))
FAIL("B01", "§2 量纲核验称 [U_self]=ML²T⁻²（能量）",
     "机器量纲（按其自列因子 ħ·R_c·κ²/c）= **%s**，即**质量**而非能量；缺口恰为 c²。"
     "来料核验行的算术本身也错：[' ML²T⁻¹·L ']/[' LT⁻¹ ']·L⁻² 实得 M，却写成 ML²T⁻²"
     % dstr(dim_U),
     "量纲非齐次缺陷族跨册复发（r18→r19→r22→r26→r27→r32→r35→r37→r44→r45→**r48**）第 11 次；"
     "与 r45 T11 完全同点（V4.5 的 U 同样是 M）：属同一未修上游")

# B02 mc² = ħω − U_self
FAIL("B02", "§3 的 mc² = ħω − U_self",
     "[ħω]=%s（能量），[U_self]=%s（质量）⇒ 两式不可相减，缺口 c²。零成本最小修正：U→U·c²，"
     "即前因子 ħ/(2c)→ħc/2（与 r45 T13 给出的修法逐字相同）" % (dstr(dEnergy), dstr(dim_U)),
     "修正后 U=(2πħcR_c/3)κ²，与 r44 登记的 V4.4 形式 (ħc/2)l_P²κ² 同族（同有 ħc）")

# B03 修正后的 A 与判别式
dim_A_draft = dmul(dmul(dmul(dH, dL), dinv(dpow(dC, 3))), dpow(dKappa, 2))
dim_A_fixed = dmul(dmul(dmul(dH, dL), dinv(dC)), dpow(dKappa, 2))
FAIL("B03", "§3 的 A = 2πħR_c/(3c³)",
     "来料 A 的量纲 = %s（非质量）；最小修正后 A = 2πħR_c/(3c)，量纲 = %s = [m] ✓"
     % (dstr(dim_A_draft), dstr(dim_A_fixed)),
     "c³→c 这一个幂次即 B01/B02 的 c² 缺口的全部后果")
guard("dim_A_fixed_is_mass", deq(dim_A_fixed, dM), "[A_fixed·κ²]=%s" % dstr(dim_A_fixed))

# B04 [ξ]
xi_rows = []
for b_ in ["0", "0.25", "0.5", "0.75", "1"]:
    bb = Fraction(b_)
    d_xi = dadd(dL, dpow(dKappa, -bb))
    xi_rows.append((b_, dstr(d_xi)))
FAIL("B04", "§3 称 ξ 为『无量纲几何常数（全局普适常数）』",
     "R_c=ξκ^{-β} ⇒ [ξ]=[R_c]·[κ]^{β}=L^{1−β}：β=0/0.25/0.5/0.75/1 ⇒ %s / %s / %s / %s / %s。"
     "**仅 β=1 时 ξ 无量纲**；来料推荐的折中区 β∈(0,1) 恰好使 ξ 成为**有量纲**新标度"
     % tuple([r[1] for r in xi_rows]),
     "⇒ 折中方案不是『不引入新标度』，而是引入一个未被任何观测约束的长度幂（比 l_P 更自由，因 l_P 至少被 G 约束）")

# B05 [a_TUFT]
dim_a = dmul(dmul(dmul(dC, dinv(dmul(dQ, dH))), dM), dKappa)
MISMATCH("B05", "§4 的 a^TUFT = −3c·cotθ/(4eħ)·m·κ(m)",
         "本册按来料原式机器量纲 = **%s**（非无量纲；a 是无量纲量）。"
         "r42 登记的同类读数为 (0,−3,+1,−1)=T/(C·L³)，本册 (0,−2,0,−1)；二者之差恰为 1/c ⇒ 口径差登记，**不代选**。"
         % dstr(dim_a),
         "补齐因子需 L²Q；穷举见 B06")
guard("dim_a_not_dimensionless", not deq(dim_a, dONE), "[a_TUFT]=%s ≠ 1" % dstr(dim_a))

# B06 补齐因子穷举
basis = [("c", dC), ("hbar", dH), ("G", Dim(-1, 3, -2)), ("m_e", dM), ("l_P", dL), ("e", dQ)]
target = Dim(0, 2, 0, 1)
hits = []
RNG = [D(k) for k in (-3, -2, -1, 0, 1, 2, 3)]
for a0 in RNG:
    for a1 in RNG:
        for a2 in RNG:
            for a3 in RNG:
                for a4 in RNG:
                    for a5 in RNG:
                        exps = [a0, a1, a2, a3, a4, a5]
                        tot = dONE
                        for (nm, dd), ex in zip(basis, exps):
                            tot = dmul(tot, dpow(dd, ex))
                        if deq(tot, target):
                            nz = sum(1 for x in exps if x != 0)
                            hits.append((nz, sum(abs(x) for x in exps), exps))
hits.sort(key=lambda z: (z[0], z[1]))
simplest = ["·".join("%s^%s" % (basis[i][0], _num(Fraction(str(e))))
                     for i, e in enumerate(h[2]) if e != 0) for h in hits[:6]]
INFO("B06", "a^TUFT 量纲补齐因子的参数空间穷举（±3 幂，基 {c,ħ,G,m_e,l_P,e}）",
     "目标量纲 %s：命中 **%d** 组。最简若干组：%s" % (dstr(target), len(hits), " ; ".join(simplest)),
     "同 r42 判据：缺口必给出目标量纲向量，穷举可机器判定『框架内有无解』；本册有解但**全部含 e¹**（无量纲磁矩反常本不该含电荷）")

# B07 "自能定义不变"
dim_U_v44 = dmul(dmul(dmul(dH, dC), dpow(dL, 2)), dpow(dKappa, 2))
MISMATCH("B07", "§2 称『自能定义不变：U_self=(ħ/2c)∫d³x|∇κ|²』",
         "与 r44 登记的 V4.4 自能 (ħc/2)l_P²κ² 相比：V4.4 量纲 = %s，V4.7 量纲 = %s —— **不同族**，"
         "二者之比 = 3c²l_P²/(4πR_c) 是**有量纲**量 ⇒ 『定义不变』被量纲直接否证"
         % (dstr(dim_U_v44), dstr(dim_U)),
         "记账转移（复发 r32 Z19）：经验假设从『固定 l_P』(1 个) 变为『非解轮廓 + ξ + β』(3 个)，总数增加。见 E03")

# B08 少数成立项
dim_omega = dmul(dC, dKappa)
PASS("B08", "ω = cκ/sinθ 与 ħω 的量纲",
     "[cκ]=%s=T⁻¹ ✓ 角频率；[ħω]=%s=能量 ✓" % (dstr(dim_omega), dstr(dmul(dH, dim_omega))),
     "本册少数成立项之一；与 m c² 相减需 B02 修正后才闭合")

# ================================================================ C 组：映射 / 判别式 / m_max
# C01 判别式推导
mmax_claim = 3 * hbar / (4 * PI * c ** 2)
mmax_from_AB = 3 * hbar * c / (8 * PI * lP_nominal)     # 从来料自身 A,B 严格得（R_c=l_P）
dim_mmax_claim = dmul(dH, dinv(dpow(dC, 2)))
FAIL("C01", "§3 的 m_max = 3ħ/(4πc²sin²θ)",
     "从来料自身的 A=2πħR_c/(3c³)、B=−ħ/(c sinθ) 严格得判别式条件 m < 3ħc/(8πR_c sin²θ)："
     "①**丢失 R_c** ②c 幂次为 c¹ 非 c⁻² ③系数 8π 非 4π；来料式量纲 = %s（**非质量**），值 %s（SI 组合单位）。"
     "R_c=l_P 时来料自身链条给出 %s（量纲 = 能量，也不是质量）"
     % (dstr(dim_mmax_claim), _f(mmax_claim), _f(mmax_from_AB)),
     "⇒ 来料的 m_max 与其自己写的 A、B 不自洽；它只是把 r45 已判错的 V4.6 表达式手工乘了 1.5")

# C02 显式根公式
inner = 4 * PI * m_e * c ** 2 / (3 * hbar)
ratio_inner = (4 * PI * m_e * c ** 2 / (3 * hbar)) / (8 * PI * lP_nominal * m_e / (3 * hbar * c))
FAIL("C02", "§3 的显式根公式 κ = (3c²/2πR_c)[1/sinθ − √(1/sin²θ − 4πmc²/3ħ)]",
     "①内层判别式对电子 = 1 − %s < 0 ⇒ **复根**（全部真实粒子皆无实根）；"
     "②按来料自身 A,B 应为 (3c²/4πR_c)[1/sinθ − √(1/sin²θ − 8πR_cm/3ħc)] ⇒ 前因子差 **2 倍**、"
     "内层项差 c³/(2R_c) = %s 倍 ⇒ 显式公式与自己的二次方程不同源，代回残差非零"
     % (_f(inner), _f(ratio_inner)),
     "方法论：『公布值互相代入自洽性检验』（r26 纪律）——来料未做")
guard("inner_discriminant_negative", inner > 1, "1 − %s < 0 ⇒ 复根" % _f(inner))

# C03 1.5 倍
INFO("C03", "『V4.7 新上限 = 1.5 × V4.6』",
     "1.5 是**两个同错表达式之比**（3ħ/4πc² ÷ ħ/2πc²）：两者都丢 R_c、都量纲为 MT、都不是质量 ⇒ "
     "1.5 不携带任何物理增益信息，只是笔算 artifact。",
     "与 C04 合读：真实情况不是『差 1.5 倍不够』，而是『根本不需要抬升』")

# C04 核心：m_max 早已远超 τ
mmax_corr = 3 * hbar / (8 * PI * c * lP_nominal)
mmax_GeV = mmax_corr / kg_per_GeV
ratio_tau = mmax_corr / m_tau
mtau_GeV = m_tau / kg_per_GeV
FAIL("C04", "§3『单纯更换轮廓只能提升 1.5 倍，仍不足以容纳 τ 子（1777 MeV）』—— 本册核心裁定",
     "最小量纲修正（c³→c）后 m_max = 3ħ/(8πcR_c sin²θ)，量纲 = %s = 质量 ✓；R_c=l_P 时 = **%s kg = %s GeV/c²**，"
     "而 m_τ = %s kg = %s GeV/c² ⇒ **m_max/m_τ = %s**（τ 子比上限小 17.9 个量级）。"
     "⇒ 『上限不够、必须抬升以容纳 τ』是 **c 幂次笔误造成的伪命题**（自毁式：来料式量纲 MT、值 %s，"
     "电子反而是它的 1.5×10²¹ 倍，与 r45 T20 同型）"
     % (dstr(dM), _f(mmax_corr), _f(mmax_GeV), _f(m_tau), _f(mtau_GeV), _f(ratio_tau), _f(mmax_claim)),
     "⇒ 分支2 立项动机（抬升 m_max 容纳 τ）在其自身修正后即告消失；这是本册与 r45 的最大差别（r45 判的是『不可能』，本册判的是『不需要』）")
guard("mmax_fixed_is_mass", deq(dmul(dH, dinv(dmul(dC, dL))), dM),
      "[ħ/(cR_c)]=%s" % dstr(dmul(dH, dinv(dmul(dC, dL)))))
guard("mmax_exceeds_tau", mmax_corr > m_tau, "m_max/m_tau = %s" % _f(ratio_tau))

# C05 m_max 随 ξ 连续可调 ⇒ 零判别力
def kappa_star(xi, beta, sin_th=D(1)):
    if beta == 1:
        return None
    base = D(3) / (2 * PI * xi * (2 - beta) * sin_th)
    return dpow_dec(base, 1 / (1 - beta))

def m_max_of(xi, beta, sin_th=D(1)):
    if beta == 1:
        return None
    ks = kappa_star(xi, beta, sin_th)
    return (hbar / (c * sin_th)) * ks * (1 - beta) / (2 - beta)

def xi_for_target(mtarget, beta, sin_th=D(1)):
    if beta == 1:
        return None
    A1v = hbar / (c * sin_th)
    ks = mtarget * (2 - beta) / ((1 - beta) * A1v)
    return D(3) / (2 * PI * (2 - beta) * sin_th * dpow_dec(ks, 1 - beta))

tune_rows = []
for b_ in ["0", "0.25", "0.5", "0.75", "0.9"]:
    bb = D(b_)
    row = []
    for mult in ["1", "10", "1e-6"]:
        mt = m_tau * D(mult)
        xv = xi_for_target(mt, bb)
        chk = m_max_of(xv, bb)
        row.append((mult, _f(xv), _f(rel(chk, mt), 3)))
    tune_rows.append((b_, row))
FAIL("C05", "『把 m_max 抬升到容纳 τ 子』作为可检验目标",
     "ξ 连续可调 ⇒ 任意目标 m_max 都有解（反解且逐位吻合）。m_max/m_τ = 1 / 10 / 1e-6 时所需 ξ："
     + " ".join(["β=%s ⇒ [%s / %s / %s]" % (b_, r[0][1], r[1][1], r[2][1]) for b_, r in tune_rows])
     + " ⇒ 『容纳 τ 子』对 (ξ,β) 无任何约束，**零判别力**（复发 r26 临界半径族：跨 193 倍的一族解全存在）",
     "与 C04 合读：不仅『不需要抬升』，而且『抬升了也不能说明任何事』")

# C06 修正后的二次映射自洽性
A2_demo = 2 * PI * hbar * D("1e-9") / (3 * c)
A1v = hbar / c
kk = m_e / A1v * D("1.05")
mm_chk = A1v * kk - A2_demo * kk ** 2
guard("corrected_quadratic_is_mass", deq(dmul(dmul(dmul(dH, dL), dinv(dC)), dpow(dKappa, 2)), dM),
      "[A_fixed κ²]=%s" % dstr(dmul(dmul(dmul(dH, dL), dinv(dC)), dpow(dKappa, 2))))
PASS("C06", "最小修正后（c³→c）的二次映射内部自洽性",
     "m = ħκ/(c sinθ) − (2πħR_c/3c)κ² 三项量纲齐为 M ✓；判别式、根、m_max 三者互推闭合"
     "（抽样点 m(A₁κ−A₂κ²) = %s kg 与输入一致）" % _f(mm_chk),
     "⇒ 该族方程『改对后可用』，问题在参数语义（C05）与拟合层（D 组），不在代数")

# ================================================================ D 组：拟合层
kappa_e_lin = m_e * c / hbar
kappa_tau_lin = m_tau * c / hbar
ratio_req = da_mu / da_e
mm_ratio_sq = (m_mu / m_e) ** 2

# D01 符号互斥
guard("data_signs_are_opposite", (da_e < 0) and (da_mu > 0),
      "Δa_e=%s < 0，Δa_μ=%s > 0（机器确认，排除我自己的符号读反）" % (_f(da_e), _f(da_mu)))
FAIL("D01", "§6『维持全部已成功结果：e/μ g-2 拟合』+ 目标『同时拟合 e 与 μ』",
     "a^TUFT = −(3c·cotθ/4eħ)·m·κ(m)，其中 m>0、κ(m)>0 ⇒ sign(a^TUFT) 只由 cotθ 决定，**对 e/μ 必然同号**；"
     "而数据要求 Δa_μ/Δa_e = %s / %s = **%s < 0（反号）** ⇒ 1 个符号自由度、2 个反号数据点 ⇒ "
     "**任意 (θ,ξ,β) 皆不可解**" % (_f(da_mu), _f(da_e), _f(ratio_req)),
     "复发并加强 r42 N02/N03：r42 已证『符号证伪对量纲补齐因子免疫』，本册补证『对 β 全区间亦免疫』（结构性，非数值）")

# D02 凸性定理：|a_μ/a_e| ≥ (m_μ/m_e)²
def solve_kappa(mm, A1v, A2v, p_exp, kstar):
    lo, hi = D(0), kstar
    for _ in range(180):
        mid = (lo + hi) / 2
        if mid <= 0:
            break
        val = A1v * mid - A2v * dpow_dec(mid, p_exp) - mm
        if val < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

grid = []
for b_ in ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"]:
    bb = D(b_)
    p_exp = 2 - bb
    for s_ in ["1.01", "1.1", "2", "10", "100"]:
        sv = D(s_)
        mt = sv * m_mu
        xv = xi_for_target(mt, bb)
        ks = kappa_star(xv, bb)
        if ks is None:
            continue
        A2v = 2 * PI * hbar * xv / (3 * c)
        k_e = solve_kappa(m_e, A1v, A2v, p_exp, ks)
        k_mu = solve_kappa(m_mu, A1v, A2v, p_exp, ks)
        r_ = (m_mu * k_mu) / (m_e * k_e)
        grid.append((bb, sv, r_, k_e, k_mu))
grid_min = min(g[2] for g in grid)
grid_max = max(g[2] for g in grid)
# β=1 精确线性情形
A2_lin = 2 * PI * hbar * D("1e-9") / (3 * c)
slope = A1v - A2_lin
k_e_lin = m_e / slope
k_mu_lin = m_mu / slope
ratio_beta1 = (m_mu * k_mu_lin) / (m_e * k_e_lin)
guard("convexity_lower_bound", grid_min >= mm_ratio_sq * (1 - D("1e-30")),
      "网格最小比值 %s ≥ (m_μ/m_e)² = %s" % (_f(grid_min), _f(mm_ratio_sq)))
guard("beta1_is_exactly_m_squared", rel(ratio_beta1, mm_ratio_sq) < D("1e-40"),
      "β=1 时比值 %s 与 (m_μ/m_e)² %s 逐位相等" % (_f(ratio_beta1), _f(mm_ratio_sq)))
FAIL("D02", "§4『取中间 β∈(0,1)，可自由调节 a^TUFT(m) 的增长速率』—— 本册最强裁定",
     "m(κ)=A₁κ−A₂κ^{2−β} 是**凹增**函数 ⇒ 反函数 κ(m) **凸增**且 κ(0)=0 ⇒ κ(m)/m 单调不减 ⇒ "
     "a_μ/a_e = (m_μκ_μ)/(m_eκ_e) ≥ (m_μ/m_e)² = **%s**（β=1 或 ξ→0 取等号，β<1 时严格更大）。"
     "网格（β=0…0.9 × m_max/m_μ=1.01…100，50 组）实测比值 ∈ [%s, %s]，最小值 = (m_μ/m_e)²。"
     "而数据要求 |Δa_μ/Δa_e| = **%s** ⇒ 量级也差 **%s 倍**，且**非线性只会使其更大**（方向完全相反）"
     % (_f(mm_ratio_sq), _f(grid_min), _f(grid_max), _f(abs(ratio_req)), _f(mm_ratio_sq / abs(ratio_req))),
     "⇒ V4.7 的『折中』在数学上不可能成立：自能非线性把比值推离目标而非拉近。与 r44 的『12.8×』读数逐位吻合（独立交叉印证）")

# D03 δ 反解
K_a = 3 * c / (4 * e_ch * hbar)
delta_fit = abs(da_e) / (K_a * m_e * kappa_e_lin)
INFO("D03", "拟合电子所需的 cotθ（=tan δ，δ=π/2−θ）",
     "线性极限 κ_e=m_e c/ħ=%s ⇒ cotθ = %s。库内同族读数：r42 5.14E-46（V4.2）、r44 6.5E-48（V4.4）、"
     "本册 %s（V4.7 线性极限）——**具体数值随版本映射漂移 10 个量级，但全部 ≲1e-45**"
     % (_f(kappa_e_lin), _f(delta_fit), _f(delta_fit)),
     "⇒ 结论对数值不敏感：δ≲1e-45 ⇒ 1/sinθ−1 = δ²/2 ≲ 1e-90 ⇒ χ_G 恒机器零（D04）")

# D04 χ_G 恒零
sin_th_req = c ** 3 * lP_nominal ** 2 / (hbar * Gexp)
chi_G_at_delta = (delta_fit ** 2 / 2 / sigma_G_rel) ** 2
chi_G_best = ((sin_th_req - 1) / sigma_G_rel) ** 2 if sin_th_req >= 1 else D(0)
# 阳性对照：δ 取远离拟合值的大值时 χ_G 必须显著非零
# （首版取 δ=1e-3 只给 χ_G=2.5e-3 < 阈值 ⇒ 假 FAIL；χ_G=(δ²/2/σ_G)² 要 >1e3 需 δ≳2.5e-2，取 0.1）
delta_pos = D("0.1")
chi_G_pos = (delta_pos ** 2 / 2 / sigma_G_rel) ** 2
guard("chi_G_zero_has_positive_control", chi_G_pos > D("1e3"),
      "阳性对照：δ=0.1（远离拟合值 ≲1e-45）⇒ χ_G = %s ≫ 0，检验器非恒零" % _f(chi_G_pos))
FAIL("D04", "§5 χ² 中的引力项 χ_G（G_th=c³l_P²/(ħ sinθ)）",
     "①拟合 δ 下 1/sinθ−1 = δ²/2 ⇒ χ_G = %s（机器零）⇒ 引力约束**零判别力**；"
     "②若反从 G 解 sinθ = c³l_P²/(ħG_exp) = %s（>1 则无实数 θ），θ=π/2 处残差 %s/1e-5 ⇒ χ_G 最大仅 %s，"
     "相对 g-2 项可忽略 ⇒ **G 项在实际采样中不参与**。复发第 10 次恒等式复读（r44 同点）"
     % (_f(chi_G_at_delta), _f(sin_th_req), _f(sin_th_req - 1), _f(chi_G_best)),
     "注意 l_P 若取定义式 √(ħG/c³) 则 sinθ≡1 严格成立 ⇒ G_th≡G_exp 是恒等重排（r44 已登记）")

# D05 σ 口径
a_mu_from_e = da_e * mm_ratio_sq
chi_mu_claim = ((a_mu_from_e - da_mu) / sigma_mu_claim) ** 2
chi_mu_real = ((a_mu_from_e - da_mu) / sigma_mu_real) ** 2
guard("crosscheck_r42_a_mu_reading", rel(abs(a_mu_from_e), D("2.9497E-8")) < D("1e-4"),
      "拟合电子后 a_μ^TUFT = Δa_e·(m_μ/m_e)² = %s，r42 登记 2.94997E-8（独立交叉核对通过）" % _f(a_mu_from_e))
FAIL("D05", "§5 χ² 的误差条 σ_e=1e-12 / σ_μ=4e-7（未声明来源）",
     "拟合电子后 a_μ^TUFT = %s（与 r42 逐位一致），观测 %s ⇒ 残差 %s。"
     "来料 σ_μ=4e-7 ⇒ χ²_μ = **%s**（『不失配』）；真实口径 σ_μ=5.2e-10 ⇒ χ²_μ = **%s**（强失配）⇒ "
     "**判决支点完全依赖未声明的 σ 口径**（复发 r44 同型）"
     % (_f(a_mu_from_e), _f(da_mu), _f(a_mu_from_e - da_mu), _f(chi_mu_claim), _f(chi_mu_real)),
     "σ_e 同理：1e-12 vs 真实 2.8e-14，相差 35.7 倍 ⇒ χ² 差 1.27e3 倍")

# D06 先验盒可行性
box = []
for b_ in ["0", "0.05", "0.1", "0.2", "0.4", "0.6", "0.8", "0.95"]:
    bb = D(b_)
    for xv in [D(1), D(10), D(100), D("1e3"), D("1e6")]:
        mv = m_max_of(xv, bb)
        if mv is not None:
            box.append((bb, xv, mv))
box_max = max(z[2] for z in box)
box_max_arg = [z for z in box if z[2] == box_max][0]
xi_need = xi_for_target(2 * m_mu, D("0.5"))
guard("prior_box_infeasible", box_max < m_e, "盒内 m_max 最大 %s kg < m_e %s kg" % (_f(box_max), _f(m_e)))
FAIL("D06", "§5 先验 ptform：ξ=10^(u₁·6)∈[1,1e6]、β=u₂∈(0,1) —— 选项1 的可执行性",
     "修正后模型下盒内 m_max 最大值 = **%s kg**（β=%s, ξ=%s），而 m_e = %s kg ⇒ **m_max 比电子质量小 %s 倍**"
     " ⇒ 盒内所有点均无实根 ⇒ findroot 全失败 ⇒ χ² 恒 ≥1e12 ⇒ dynesty 在其自设先验下**必输出垃圾**。"
     "物理射程所需 ξ ≈ %s（β=0.5, m_max=2m_μ），落在先验下界外 %s 个量级"
     % (_f(box_max), _f(box_max_arg[0], 3), _f(box_max_arg[1], 3), _f(m_e), _f(m_e / box_max),
        _f(xi_need), _f(D(1) / xi_need)),
     "⇒ 选项1（3 参数嵌套采样）在**执行前**即被否证：先验与物理射程不相交。与 r45 T29『χ² 无定义域』同族但落点不同")

# D07 findroot 初值
guard("findroot_seed_far_outside", D("1e35") / kappa_tau_lin > D("1e15"),
      "初值 1e35 / κ_τ(线性) %s = %s" % (_f(kappa_tau_lin), _f(D("1e35") / kappa_tau_lin)))
FAIL("D07", "§5 kappa() 用 mp.findroot(f, 1e35) 求根",
     "物理射程 κ ∈ [κ_e≈%s, κ_τ≈%s] m⁻¹；初值 1e35 高出 %s ~ %s 个量级。且 m(κ) 非单调（κ* 处取极大后下降），"
     "方程有两个正根 ⇒ 初值决定取哪一支，而代码未指定、未校验 κ<κ*"
     % (_f(kappa_e_lin), _f(kappa_tau_lin), _f(D("1e35") / kappa_tau_lin), _f(D("1e35") / kappa_e_lin)),
     "⇒ 即便先验改对，数值结果仍不可信（分支歧义 + 无物理支校验）")

# D08 τ 罚项
FAIL("D08", "§5 的 τ 约束『chi_tau = 0 若 findroot 成功，否则 1e12』",
     "①τ 罚项在成功时恒为 **0** ⇒ τ 对 χ² **零约束**（只在不可行时惩罚），不检验 τ 落在物理支、"
     "也不检验 findroot 是否返回复根（mpmath 在实初值下可能返回复数而不抛错）⇒ 罚项本身不可靠；"
     "②τ 的 g-2 未参与拟合 ⇒ 所谓『容纳 τ 作为基本单螺旋激发』不产生任何可检验读数",
     "与 C05 合读：τ 可存在性由 ξ 任意保证，不构成检验")

# D09 β 的量级匹配边界
p_req = (abs(ratio_req).ln() / (m_mu / m_e).ln()) - 1
beta_req = 2 - 1 / p_req
INFO("D09", "若（反事实地）κ(m) 为幂律，量级匹配要求什么",
     "所需标度指数 1+1/(2−β) = ln|Δa_μ/Δa_e|/ln(m_μ/m_e) = %s ⇒ β = %s。但 D02 的凸性定理给出 κ(m) 的指数恒 ≥1"
     "（即 1+1/(2−β) ≥ 2）⇒ 所需指数 %s < 2 落在该族**值域之外** ⇒ 量级与符号双杀"
     % (_f(p_req + 1), _f(beta_req), _f(p_req + 1)),
     "来料设想的『β∈(0,1) 自由调节』依赖的是凹的 κ(m)，而自能项给的是凸的")

# D10 参数账
BOUNDARY("D10", "§6『全局 3 参数，不向 e/μ/τ 分配独立参数，保留理论核心愿景』",
         "参数确为全局（θ, ξ, β），但 χ² 另硬编码 l_P（且 G_exp 作为数据）⇒ 全局常数 ≥ 3~4；"
         "Ω5（自由常数 ≤1）被违反。更关键：β∈(0,1) 时 ξ 量纲 L^{1−β}（B04）⇒ 实为"
         "『1 个角度 + 1 个未定长度标度 + 1 个指数』三维自由，比 V4.5 的『l_P 固定尺度』**更自由**"
         "（l_P 至少被 G 约束，ξ 无任何约束）。复发 r41『外部输入 ≥2 撞 Ω5』。",
         "不代选：是否接受 ≥3 个登记外部输入，属公设层决策")

# ================================================================ E 组：代码 / 自评 / 互链
FAIL("E01", "§6『维持全部已成功结果：e/μ g-2 拟合、全局唯一 θ、EC 挠率耦合不变』",
     "①e/μ g-2 拟合：不成立（D01 符号 + D02 量级双杀，对 θ,ξ,β 全空间免疫）；"
     "②全局唯一 θ：θ 由 g-2 反解得 δ≲1e-45（D03），而 G 约束要求 δ≈%s（D04）⇒ 两者口径不一致，"
     "实际是 G 项权重过小而被忽略；③EC 挠率耦合 3/8 不变 ✓（r42 已登记为标准写法，PASS 但非 TUFT 新物理）"
     % _f((sin_th_req - 1).copy_abs().sqrt() * D("1.4142135623730950488016887242096980785696718753769480731766797379") if sin_th_req >= 1 else D(0)),
     "⇒ 三条自评中仅第 ③ 条成立，且它不属于 V4.7 的新内容")

PASS("E02", "EC 挠率耦合 3/8 与 Pauli 约化（来料称不变）",
     "r42 已机器登记为标准写法（PASS），本册不重复计算；沿用不构成 V4.7 的新增可算结果",
     "记 PASS 仅为记账完整；该常数非 TUFT 派生")

INFO("E03", "『移除经验假设』的记账审计",
     "V4.5/V4.6 的经验假设 = 固定尺度 l_P（1 个，且被 G 部分约束）；V4.7 的假设 = 非解轮廓（A01）"
     "+ ξ（B04 有量纲、无约束）+ β（指数）⇒ 经验假设从 1 个变为 3 个，且自由度类型升级（常数→常数+标度+指数）。"
     "复发 r32 Z19 记账转移：『移除假设』实际是『把假设换了位置并加量』。",
     "不否认方向：把局域化尺度从 l_P 释放出来是有信息量的动作（A06），问题是释放后未提供任何自洽约束")

INFO("E04", "本册不自推清单（4 项）",
     "①∇²κ=0 的正确有源版本应取何种源项（须公设层决定）；②R_c(κ) 的真实依赖关系（子分支B 的目标，本册不推）；"
     "③a^TUFT 的量纲补齐因子应取哪一解（B06 多解）；④χ² 的 σ 应取实验还是 SM 理论口径（须来料声明）",
     "本册只判来料所给公式的机器读数，不代为推导")

# 开放项
OPEN_ITEMS.append(dict(id="X-R48-1",
    text="分支2 的球对称有限域 BVP『无源+边界归零+原点非平凡』不可能三角 ⇒ 须在公设层三选一放弃一条（不代选）"))
OPEN_ITEMS.append(dict(id="X-R48-2",
    text="m_max 成为 ξ 的连续可调函数 ⇒ 任何『容纳某粒子』类命题零判别力；须给出 ξ 的独立约束或放弃该类命题"))
OPEN_ITEMS.append(dict(id="X-R48-3",
    text="κ(m) 凸性定理 ⇒ a∝m·κ(m) 恒给出 |a_μ/a_e| ≥ (m_μ/m_e)²=4.2753E+04，与目标 3.3333E+03 反向；"
         "要下调该比值须使 κ(m) **凹**（即自能项须为**正贡献**或换映射结构），属结构级改动"))
OPEN_ITEMS.append(dict(id="X-R48-4",
    text="先验盒 ξ∈[1,1e6] 与物理射程（ξ≈1.9E-9）不相交 ⇒ 选项1 采样须先验改界后方可讨论"))
OPEN_ITEMS.append(dict(id="X-R48-5",
    text="β∈(0,1) 时 ξ 量纲 L^{1−β} ⇒ 『无量纲几何常数』声明须撤回或把 β 固定为 1（后者退回 m²）"))

NOT_SELF_DERIVED.append("∇²κ=0 的正确有源（Poisson）形式与源项系数——本册只证齐次版无可用解，不给替代方程")
NOT_SELF_DERIVED.append("R_c(κ) 的函数形式——来料 ansatz，本册只核算其后果（C05/D02），不推导")
NOT_SELF_DERIVED.append("a^TUFT 量纲补齐因子的唯一选择——B06 穷举给出多解，不代选")
NOT_SELF_DERIVED.append("σ_e/σ_μ/σ_G 的权威口径——本册只做两档对照（D05），不裁定")

# ================================================================ 输出
def _jsonable(x):
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, dict):
        return dict((k, _jsonable(v)) for k, v in x.items())
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    return x

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)

    counts = {}
    for r in RECORDS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    summary_line = " ".join("%s=%d" % (k, counts[k]) for k in sorted(counts))

    payload = dict(
        round="r48", stamp=STAMP,
        title="TUFT-V4.7 分支2（∇²κ=0 格林函数解 + 线性球包 + R_c=ξκ^{-β}）全维审计",
        engine="纯标准库 Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)",
        verdicts=counts, summary=summary_line, items=len(RECORDS),
        guards=GUARDS, guards_passed=sum(1 for g in GUARDS if g["passed"]),
        records=RECORDS, open_items=OPEN_ITEMS, not_self_derived=NOT_SELF_DERIVED,
        key_numbers=dict(
            laplacian_residual_at_half="−4κ₀/R_c²（归一化残差 1.000）",
            mmax_claim=_f(mmax_claim), mmax_claim_dim=dstr(dim_mmax_claim),
            mmax_corrected_kg=_f(mmax_corr), mmax_corrected_GeV=_f(mmax_GeV),
            m_tau_kg=_f(m_tau), m_tau_GeV=_f(mtau_GeV), mmax_over_mtau=_f(ratio_tau),
            ratio_required=_f(ratio_req), ratio_mu_e_squared=_f(mm_ratio_sq),
            ratio_grid_min=_f(grid_min), ratio_grid_max=_f(grid_max),
            a_mu_from_electron_fit=_f(a_mu_from_e),
            chi2_mu_claim_sigma=_f(chi_mu_claim), chi2_mu_real_sigma=_f(chi_mu_real),
            delta_cot_theta=_f(delta_fit), chi_G_at_delta=_f(chi_G_at_delta),
            prior_box_mmax_max_kg=_f(box_max), xi_physical_example=_f(xi_need),
            inner_discriminant_electron=_f(inner),
            xi_dim_by_beta=dict((b_, d_) for b_, d_ in xi_rows),
            dim_U_self=dstr(dim_U), dim_a_tuft=dstr(dim_a),
        ),
    )
    p_json = os.path.join(OUT_DIR, NAME + ".json")
    with io.open(p_json, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(_jsonable(payload), ensure_ascii=False, indent=2))

    md = []
    md.append("# %s" % NAME)
    md.append("")
    md.append("- 轮次：r48。**撞号处置**：起草时 r46/r47 为空号，落盘后复核发现并行会话同日已占 r46"
              "（《V4.8 子分支B 边界变分与 R_c 导出》）与 r47（《V4.8-4.3 稳态质量隐式关系与 m_max》），"
              "按「后到者改号不覆盖他人」纪律迁至空号 r48，未触碰他人任何字节。")
    md.append("- 条目：**%d**（%s）" % (len(RECORDS), summary_line))
    md.append("- 自检 guard：**%d/%d**" % (sum(1 for g in GUARDS if g["passed"]), len(GUARDS)))
    md.append("")
    md.append("## 判定表")
    md.append("")
    md.append("| 条目 | 判定 | 来料主张 | 机器读数 |")
    md.append("|---|---|---|---|")
    for r in RECORDS:
        md.append("| %s | %s | %s | %s |" % (r["id"], r["verdict"],
                                             r["claim"].replace("|", "/"),
                                             r["machine_reading"].replace("|", "/")))
    md.append("")
    md.append("## 关键读数")
    md.append("")
    for k in sorted(payload["key_numbers"]):
        md.append("- `%s` = %s" % (k, payload["key_numbers"][k]))
    md.append("")
    md.append("## 自检")
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

    rep = []
    rep.append("REPORT %s" % NAME)
    rep.append("ITEMS %d  %s" % (len(RECORDS), summary_line))
    rep.append("")
    for r in RECORDS:
        rep.append("[%s] %s :: %s" % (r["verdict"], r["id"], r["claim"]))
        rep.append("      -> %s" % r["machine_reading"])
        if r["note"]:
            rep.append("      note: %s" % r["note"])
    rep.append("")
    rep.append("GUARDS %d/%d" % (sum(1 for g in GUARDS if g["passed"]), len(GUARDS)))
    for g in GUARDS:
        rep.append("  [%s] %s -- %s" % ("PASS" if g["passed"] else "FAIL", g["name"], g["detail"]))
    p_rep = os.path.join(OUT_DIR, NAME + "_report.txt")
    with io.open(p_rep, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rep) + "\n")

    g_ok = sum(1 for g in GUARDS if g["passed"])
    g_n = len(GUARDS)
    if g_ok != g_n:
        sys.stdout.write("GUARD FAIL %d/%d -- 审计器本身有问题，禁止输出结论\n" % (g_ok, g_n))
        return 2
    sys.stdout.write("OK items=%d %s guards=%d/%d\n" % (len(RECORDS), summary_line, g_ok, g_n))
    return 0

if __name__ == "__main__":
    sys.exit(main())
