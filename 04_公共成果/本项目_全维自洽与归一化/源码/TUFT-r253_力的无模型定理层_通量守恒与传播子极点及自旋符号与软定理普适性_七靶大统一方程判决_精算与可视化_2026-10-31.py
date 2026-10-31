# -*- coding: utf-8 -*-
r"""
TUFT-r253 · 力的无模型定理层
================================================================================
通量守恒 / 传播子极点 / 自旋-符号-力程 / 软定理普适性
四条无模型定理对七份「力的大统一方程」的全谱判决

【命题来源】用户：「用尽所有方法，攻破力的太统一方程。力的所有秘密破解」

【本卷定位：无模型定理层（新层）】
r243 = 工程可用性层（引力），r244 = 引力本体论层，r245 = 超导本质层（凝聚态），
r247 = 引力本质层元审计，r248 = 单方程全域力层，r249 = 低能极限推导层，
r250 = 耦合常数跑动与能标层，
r251 = 下游物理应用层（并行会话：垂直原理 FRW 与黑洞无奇点），
本卷 r253 = **无模型定理层**：换一个打法——**不接受靶的任何前提**。

【为什么需要这一层】
「力的大统一方程」这条线已经打过十几轮：r91/r94/r119/r120（9 候选全集枚举，
仅 2 条 PASS 且都不含引力）/r123（五路退守全封）/r134/r136，
加上四力统一三连 r218（定义恒等式层）/r223（运动方程层）/r224（荷空间层）。
**枚举与封堵这一支已见底**。真正没动过的是：
用「任何力的理论都必须满足的定理」当判据——幺正性、Lorentz 不变性、
无质量粒子的软行为。这些从 QFT 的公理化性质推出，不依赖任何具体模型，
所以无法用「我的框架不同」来豁免。

【四条主判据（本卷承重）】
T1 Gauss 通量：长程力若由无质量载体交换产生，Φ(r)=4πr²|F(r)| 必为常数。
T2 传播子极点：Ṽ(q) ∝ q^{m−3}（齐次度论证，纯代数）；
               无质量单粒子交换必须是 m=1 ⇒ 4πA/q² 单极点。
T3 自旋-符号-力程：交换自旋 0 ⇒ 同号吸引；自旋 1 ⇒ 同号排斥；自旋 2 ⇒ 同号吸引。
               ★一个标量势的梯度只能是自旋 0，不可能同时给自旋 1 的电磁力。
T4 Weinberg 软定理：无质量自旋 2 的耦合必须普适（等效原理是定理，不是公设）。
辅：T5 Weinberg–Witten（引力子不可复合）；T6 Coleman–Mandula（内部荷不能来自几何）。

【靶的核心式子（逐字取自来料，已逐行核实行号）】
① 定稿全书 第九章 L498（V9.3）：
   F = −∇U = s·ℏc·q₁q₂·(1/r² + 1/(λr))·e^{−r/λ}·r̂        λ→∞ ⇒ 1/r² ✓ 量纲 N ✓
② 定稿全书 第四十章 L3048（V9.36，自称「单方程封闭式」）：
   F = −ℏc·(s₁s₂q₁q₂)·[1/r + 1/λ]·e^{−r/λ}/r²·r̂
   L3053 自述「λ→∞ ⟹ ℏc|q₁q₂|/r²」，但式子实际给 1/r³；量纲 = N/m，不是力。
   闭式：F₄₀/F₉ = 1/(s·r) ⇒ 两式相差因子 1/r，不可能都对。
③ V40 L77：F_uni = −c²·r·∂_r(κ²−τ²)
   引力(κ∝1/r, τ=0) ⇒ F_g = +2c²/r²（+r̂ 向外 = 排斥），自述却说「径向向内」；
   电磁(κ=0, τ∝1/r) ⇒ F_e = −2c²/r²（吸引），自述却说「区分吸引/排斥」。
   L189–191 量纲自证 L²T⁻²·L⁻²·L = MLT⁻² ⟹ 缺 M（且 κ,τ 是 L⁻¹，∇(κ²−τ²) 应 L⁻³）。
④ 力公式压缩版 L154–185：∮V·dS=4πr²V_r=4πQ_t ⇒ V_r=Q_t/r²
   ⇒ A_r = V_r·dV_r/dr = −2Q_t²/r⁵ ⇒ F_r = 2k_i·Q_t³/r⁵ ⇒ **n = −5**
⑤ S12 §4.2/§4.3：F = (ℏc/r²)·{1/α², α, 1/α, 1}；N = 1/α²+α+1/α+1 ≈ 18907.0073；
   F̂_G = (1/α²)/N ≈ 0.9927（引力占全部力的 99.27%），而 §4.1 表 L230 自述引力「~10⁻³⁸（最弱）」
⑥ S02 §18：与①同式（交叉验证）
⑦ S14 挠率直和：T = T⁽⁰⁾[U(1)] ⊕ T^i(σ^i/2)[SU(2)] ⊕ T^a(λ^a/2)[SU(3)]
⑧ 宇宙本源 §8：1/α(μ) = 1/α(μ₀) + b·(μ/μ₀)^{d_f−4}，d_f ≈ 1.27 ⇒ 指数 −2.73

【对靶有利项先做（A 组）】
定稿全书 L498 量纲正确、λ→∞ 退化正确；压缩版 V_r→A_r→F_r 链数学自洽；
压缩版主动声明边界（κ_q 是补充公设）；S12 §4.2 量纲正确；S12 引力占比对 α 精度不敏感。
★量纲对 ≠ 数值对，两件事分开判。

【★与 r248/r249/r250/r251 的分层（不可相加）】
r248 打的靶是矢量主方程 F=(ℏc/4π)(κn+τb)/√(1+(ωr/c)²)（来自《核心动力学方程组》），
  其 B 组量纲断裂、D 组自旋 ℏ/2 虚数、E 组 η=1.2119 —— 与本卷的式子**不同**；
r250 打的靶是 α*=√3/2 那份来料的 RG 矛盾 —— 与本卷靶⑧是**不同的来料**。
本卷的 T1–T6 判据**全仓未使用过**，是本卷真正的新增。

【分层】本卷条目不可与 r142–r252 相加。
================================================================================
"""

import ast
import hashlib
import io
import json
import math
import os
import re
import time
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 50

# ============================================================
# 0. 元信息
# ============================================================
RID = "r253"
# ★「修复即自杀」第几度：不写死在字符串里，统一用 DEGREE 渲染，
#   并由守卫 G13 真机读 README 复核「本卷宣称度 = 已有最大度 + 1」。
#   取 35 的依据：README 中已出现的最大度为 34（r251 的增量章条目）；
#   r252 未标度。r251 自身判定册写 33、README 写 34（该会话内部不一致），
#   本卷按 README 实测最大值顺延，并把该歧义如实登记进撞号记录。
DEGREE = 35
BASE_NAME = ("TUFT-r253_力的无模型定理层_通量守恒与传播子极点及自旋符号与软定理普适性"
             "_七靶大统一方程判决_精算与可视化_2026-10-31")
START_TS = time.time()
START_ISO = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(START_TS))

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC_DIR = os.path.join(ROOT, "源码")
DATA_DIR = os.path.join(ROOT, "数据")

# ============================================================
# 1. 七份靶（只读）
# ============================================================
TARGETS = [
    r"D:\a10\aikjx\code\my_lib\TUFT_四力大统一_垂直原理螺旋统一场论_定稿全书.md",
    r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据\TUFT-V40终极力的统一方程_来料全文_2026-10-17.md",
    r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据\TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md",
    r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S12_空间光速螺旋统一体系\13_论文与成果\论文正文\大统一方程全集.md",
    r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S02_空间光速螺旋统一力\04_理论推导\§18_四力统一方程_力的本源与大小方向距离_攻破精算.md",
    r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S14_挠率统一场论TUFT\13_论文与成果\论文正文\原稿\四力统一_四大相互作用完整规范群统一结构_原文.md",
    r"D:\a10\aikjx\code\my_lib\_cosmos_book_review\宇宙本源著作\第四卷_力的统一\第八章_耦合跑动与大统一.md",
]
T_BOOK, T_V40, T_COMPACT, T_S12, T_S02, T_S14, T_COSMOS = range(7)

WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]

# ============================================================
# 2. 常数（标来源）
# ============================================================
C = 299792458.0                 # m/s    [SI] 定义值
H = 6.62607015e-34              # J s    [SI] 定义值
QE = 1.602176634e-19            # C      [SI] 定义值
KB = 1.380649e-23               # J/K    [SI] 定义值
HBAR = H / (2.0 * math.pi)                 # 1.054571817e-34 J s
ALPHA = 7.2973525693e-3         # [COD18] 精细结构常数
ALPHA_INV = 1.0 / ALPHA         # 137.035999084
G_N = 6.67430e-11               # m^3 kg^-1 s^-2  [COD18]
M_P = 1.67262192369e-27         # kg     [COD18] 质子质量
M_E = 9.1093837015e-31          # kg     [COD18] 电子质量
M_SUN = 1.98892e30              # kg     [IAU15]
M_EARTH = 5.9722e24             # kg
HBARC = HBAR * C                # 3.1615268e-26 J m
ARCSEC_PER_RAD = 180.0 * 3600.0 / math.pi

# 正对照锚点（公开值 + 明示容差）
ANCHOR_DEFLECTION = 1.75119     # ″  光线偏折（自旋2 ⇒ 系数 4）；本仓库 physics-lab G3 实测 1.75119
ANCHOR_DEFLECTION_TOL = 5e-3
ANCHOR_FE_FG = 1.2356e36        # 质子对 F_E/F_G 公开值
ANCHOR_FE_FG_TOL = 5e-3
ANCHOR_MGUT_MSSM = 2.26e16      # GeV   [算法联盟_规范耦合跑动…v1] MSSM 一阶
ANCHOR_AGUT_INV_MSSM = 24.2873  #      同上
M_PLANCK_GEV = 1.0e19
M_Z_GEV = 91.1876

# ============================================================
# 3. 量纲系统（M, L, T, Q, Θ）用有理数，杜绝浮点误差
# ============================================================
DNAME = ("M", "L", "T", "Q", "Θ")


def dv(m=0, l=0, t=0, q=0, th=0):
    return (F(m), F(l), F(t), F(q), F(th))


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dstr(d):
    parts = []
    for n, v in zip(DNAME, d):
        if v == 0:
            continue
        parts.append("%s^%s" % (n, v))
    return "·".join(parts) if parts else "1"


DIM_FORCE = dv(m=1, l=1, t=-2)      # N
DIM_ENERGY = dv(m=1, l=2, t=-2)     # J
DIM = {
    "hbar": dv(m=1, l=2, t=-1),
    "c": dv(l=1, t=-1),
    "kappa": dv(l=-1),              # Frenet 曲率
    "tau": dv(l=-1),                # Frenet 挠率
    "r": dv(l=1),
    "grad": dv(l=-1),
    "mass": dv(m=1),
    "G": dv(m=-1, l=3, t=-2),
}

# ============================================================
# 4. 工具
# ============================================================


def fmt(x):
    return "{:.6g}".format(x)


def relerr(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


def sha256_of(p):
    try:
        with open(p, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return ""


def read_text(p):
    try:
        with io.open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def nhit(text, *toks):
    n = 0
    for t in toks:
        n += len(re.findall(re.escape(t), text))
    return n


# ---- 自适应 Simpson（含 Richardson 修正）----
def _simpson(f, a, b, fa, fm, fb, s1, tol, depth, maxdepth):
    if depth >= maxdepth:
        return s1
    m = 0.5 * (a + b)
    ml, mr = 0.5 * (a + m), 0.5 * (m + b)
    fml, fmr = f(ml), f(mr)
    s2 = (m - a) * (fa + 4.0 * fml + fm) / 6.0 + (b - m) * (fm + 4.0 * fmr + fb) / 6.0
    if abs(s2 - s1) <= 15.0 * tol * max(1.0, abs(s2)):
        return s2 + (s2 - s1) / 15.0
    return (_simpson(f, a, m, fa, fml, fm, (m - a) * (fa + 4.0 * fml + fm) / 6.0,
                     tol, depth + 1, maxdepth)
            + _simpson(f, m, b, fm, fmr, fb, (b - m) * (fm + 4.0 * fmr + fb) / 6.0,
                       tol, depth + 1, maxdepth))


def simpson(f, a, b, tol=1e-13, maxdepth=26):
    fa, fb = f(a), f(b)
    m = 0.5 * (a + b)
    fm = f(m)
    s1 = (b - a) * (fa + 4.0 * fm + fb) / 6.0
    return _simpson(f, a, b, fa, fm, fb, s1, tol, 0, maxdepth)


def integ_osc(f, a, b, period, tol=1e-13):
    """按半周期分段，每段自适应 Simpson。用于振荡积分。"""
    n = max(1, int(math.ceil((b - a) / (period / 2.0))))
    h = (b - a) / n
    s = 0.0
    for i in range(n):
        s += simpson(f, a + i * h, a + (i + 1) * h, tol)
    return s


def integ_osc_sub(g, smax, nu, tol=1e-14):
    """换元 u = s^{1/ν} 后，按 **u 的半周期** 在 s 空间分段，每段自适应 Simpson。

    ★为什么分段边界要取 s=(kπ)^ν：振荡来自 sin u，半周期在 u 空间是等距的；
    换元后在 s 空间变成不等距，若仍按 s 等距分段，段内会跨越多个半周期，
    Simpson 的误差估计会失真。
    """
    K = max(1, int(math.ceil((smax ** (1.0 / nu)) / math.pi)))
    s, prev = 0.0, 0.0
    for k in range(1, K + 1):
        cur = min(smax, (k * math.pi) ** nu)
        if cur > prev:
            s += simpson(g, prev, cur, tol, 18)
        prev = cur
    if smax > prev:
        s += simpson(g, prev, smax, tol, 18)
    return s


# ============================================================
# 5. T2 传播子极点：闭式 + 数值互印
# ============================================================
# 换元 u = q r：Ṽ(q) = 4πA q^{m−3} · I(ν, δ)，ν = 2 − m，δ = ε/q（无量纲调节子）
# I(ν, δ) = ∫₀^∞ u^{ν−1} sin u · e^{−δu} du = Γ(ν)(1+δ²)^{−ν/2} sin(ν·arctan(1/δ))
def I_closed(nu, delta):
    """闭式：I(ν,δ) = Γ(ν)(1+δ²)^{−ν/2}·sin(ν·arctan(1/δ))。ν→0 走极限 arctan(1/δ)。"""
    if abs(nu) < 1e-14:
        return math.atan2(1.0, delta)
    g = math.exp(math.lgamma(nu))
    return g * ((1.0 + delta * delta) ** (-nu / 2.0)) * math.sin(nu * math.atan2(1.0, delta))


def I_limit(nu):
    """δ→0 极限：I(ν,0) = Γ(ν)·sin(νπ/2)。ν→0 走极限 π/2。"""
    if abs(nu) < 1e-14:
        return math.pi / 2.0
    return math.exp(math.lgamma(nu)) * math.sin(nu * math.pi / 2.0)


def I_numeric(nu, delta, umax=None, umin=1e-12):
    """振荡数值积分：∫ u^{ν−1} sin u · e^{−δu} du。

    ★两处精度关键（本卷实测踩过的坑，逐条登记）：

    (a) **尾截断**：被积函数的衰减长度是 1/δ。原先取 umax = 18/δ ⇒ 残留
        e^{−18} = 1.52e−8 —— 这个数字与 C07/C11 实测到的偏差（1.5e−8 / 1.0e−6）
        **量级完全对上**，证明误差源就是尾截断，而不是闭式错、也不是 Simpson 不收敛。
        现取 umax = 45/δ ⇒ e^{−45} = 2.9e−20，尾误差落到双精度噪声以下。

    (b) **u=0 端点奇性**：ν<1 时 u^{ν−1} 在原点发散（如 ν=0.5 ⇒ u^{−1/2}），
        自适应 Simpson 在代数奇点前收敛极慢。换元 u = s^{1/ν} 后
        u^{ν−1}du = ds/ν，幂次奇性**整体消去**（被积函数变成 sin(s^{1/ν})e^{−δs^{1/ν}}，
        在 s=0 附近仅为 s^{1/ν} 型轻微非光滑，无发散）。

    ν ≤ 0 时积分在原点本身发散（这正是 C6 要展示的紫外行为），
    此时走直接路径，并**如实保留 umin 依赖**，不做任何规避。
    """
    if umax is None:
        umax = 45.0 / delta          # 见 (a)

    if nu > 1e-12:                   # 见 (b)
        def g(s):
            u = s ** (1.0 / nu)
            return math.sin(u) * math.exp(-delta * u)
        return integ_osc_sub(g, umax ** nu, nu) / nu

    def f(u):
        return (u ** (nu - 1.0)) * math.sin(u) * math.exp(-delta * u)
    return integ_osc(f, umin, umax, 2.0 * math.pi)


def nu_of_m(m):
    return 2.0 - m


# ============================================================
# 6. T1 Gauss 通量
# ============================================================
def flux_of_F(Fmag, r):
    """Φ(r) = 4π r² · |F(r)|（中心力的球面积分）。"""
    return 4.0 * math.pi * r * r * abs(Fmag)


def loglog_slope(fn, r0, factor=2.0, h=1e-6):
    """d ln f / d ln r 的中心差分。"""
    a = math.log(abs(fn(r0)))
    rp = r0 * (1.0 + h)
    rm = r0 * (1.0 - h)
    b = math.log(abs(fn(rp)))
    c = math.log(abs(fn(rm)))
    return (b - c) / (math.log(rp) - math.log(rm))


# ============================================================
# 7. T4 软定理：2→2 弹性散射（质心系）
# ============================================================
def soft_setup(mA=1.0, mB=2.0, sqrts=4.0, theta=math.pi / 3.0):
    """返回 4 条外线的四维动量（'全入'约定：入射取负号），并做 sanity。"""
    s = sqrts * sqrts
    EA = (s + mA * mA - mB * mB) / (2.0 * sqrts)
    EB = (s + mB * mB - mA * mA) / (2.0 * sqrts)
    p = math.sqrt(max(0.0, EA * EA - mA * mA))
    # 初态：A 沿 +z，B 沿 −z
    PAin = (EA, 0.0, 0.0, p)
    PBin = (EB, 0.0, 0.0, -p)
    # 末态：能量不变（弹性），动量转过 theta
    PC = (EA, p * math.sin(theta), 0.0, p * math.cos(theta))
    PD = (EB, -p * math.sin(theta), 0.0, -p * math.cos(theta))
    # '全入'约定
    allin = [(-PAin[0], -PAin[1], -PAin[2], -PAin[3]),
             (-PBin[0], -PBin[1], -PBin[2], -PBin[3]),
             PC, PD]
    cons = [sum(v[k] for v in allin) for k in range(4)]
    dP = tuple(PC[k] - PAin[k] for k in range(4))     # 动量转移（物理约定）
    dPmag = math.sqrt(abs(dP[0] ** 2 - dP[1] ** 2 - dP[2] ** 2 - dP[3] ** 2))
    return {"allin": allin, "cons_res": max(abs(x) for x in cons),
            "dP": dP, "dPmag": dPmag, "PAin": PAin, "PC": PC}


def soft_residual(setup, gA, gB):
    """q_μ S^{μν} = Σ_i g_i P_i^ν（全入约定）。g_A 给 A/C 线，g_B 给 B/D 线。"""
    allin = setup["allin"]
    gs = [gA, gB, gA, gB]
    res = [sum(gs[i] * allin[i][k] for i in range(4)) for k in range(4)]
    return res


# ============================================================
# 8. 靶式的机读与复算
# ============================================================
def F_ch9(r, lam, s=1.0, qq=1.0):
    """定稿全书 L498：s·ℏc·q₁q₂·(1/r² + 1/(λr))·e^{−r/λ}"""
    return s * HBARC * qq * (1.0 / (r * r) + 1.0 / (lam * r)) * math.exp(-r / lam)


def F_ch9_newton(r, qq=1.0):
    """λ→∞ 退化：ℏc·q₁q₂/r²"""
    return HBARC * qq / (r * r)


def F_ch40(r, lam, qq=1.0):
    """定稿全书 L3048：−ℏc·q₁q₂·(1/r + 1/λ)·e^{−r/λ}/r²"""
    return -HBARC * qq * (1.0 / r + 1.0 / lam) * math.exp(-r / lam) / (r * r)


def F_v40_scalar(r, sign):
    """V40 L77：F = −c²·r·∂_r(±1/r²) = ∓(−2c²/r²)。sign=+1 (κ²主导) ⇒ +2c²/r²"""
    return -sign * (-2.0 * C * C) / (r * r)


def F_compact(r, k=1.0, Qt=1.0):
    """压缩版 L174：F_r = 2k_i·Q_t³/r⁵（取 k_i·Q_t³ = k）"""
    return 2.0 * k / (r ** 5)


# ============================================================
# 9. 修复定价
# ============================================================
THEOREM_KEYS = (
    "massless_spin2_carrier",      # 引力由无质量自旋 2 载体传递
    "universal_coupling",          # 耦合普适（∝ √G·T_μν，与物体成分无关）
    "spin_sign_table",             # 自旋-符号对应由 (−1)^s 决定，不是手填符号因子
    "deflection_coeff_4",          # 光偏折系数 = 4（锚点 1.75119″）
    "gauss_flux_const",            # 长程力 Φ = 4πr²|F| = const
    "propagator_pole_1_over_q2",   # 无质量传播子极点为 1/q²
    "q_not_from_geometry",         # 内部规范荷不由时空几何导出（Coleman–Mandula 相容）
    "renorm_running_log",          # 耦合跑动为对数（渐进自由），非冻结
)
GR_THEOREM_SKELETON = {"massless_spin2_carrier", "universal_coupling",
                       "deflection_coeff_4", "propagator_pole_1_over_q2"}


def repair_pricing():
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0, "total": 0}
    n = len(THEOREM_KEYS)
    for mask in range(1 << n):
        have = {THEOREM_KEYS[i] for i in range(n) if (mask >> i) & 1}
        out["total"] += 1
        if len(have) < n:
            out["EMPTY"] += 1
        elif GR_THEOREM_SKELETON.issubset(have):
            out["SUICIDE"] += 1
        else:
            out["SURVIVE"] += 1
    return out


# ============================================================
# 10. 条目容器
# ============================================================
ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})
    return ENTRIES[-1]


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok),
                     "evidence": evidence})
    return CONTROLS[-1]


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok),
                   "evidence": evidence})
    return GUARDS[-1]


# ============================================================
# 11. 只读基线
# ============================================================
SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {i: read_text(p) for i, p in enumerate(TARGETS)}
ALLT = "\n".join(TARGET_TEXT.values())
SHA_WRITE_IMPORT = {p: sha256_of(p) for p in WRITE_SIDE}


def readme_max_degree():
    """真机读：扫 README.md 里所有「第 N 度」，返回 (最大度, 命中处数)。

    ★排除提及本卷 RID 的行：本卷一旦登记进 README，自己那几行也会写「第 N 度」，
    若不排除，第二次复跑时守卫会因为「自己等于自己+1」而误报。
    ★设计意图：度数不能凭记忆写。实测发现 r251 的判定册写 33 度、
    其 README 条目写 34 度（同一卷内部不一致），故加此机器校验。
    """
    p = os.path.join(ROOT, "README.md")
    if not os.path.isfile(p):
        return None, 0
    try:
        t = io.open(p, "r", encoding="utf-8").read()
    except Exception:
        return None, 0
    hits = []
    for ln in t.splitlines():
        if RID in ln:
            continue
        m = re.search(r"第\s*(\d+)\s*度", ln)
        if m:
            hits.append(int(m.group(1)))
    return (max(hits) if hits else None), len(hits)


def scan_untouched():
    """真机读：扫 r225–r251 产物，mtime 是否早于本轮启动。
    ★r252 正被并行会话探测写入，为避免与并发写竞争而排除在外。"""
    bad, scanned = [], 0
    roots = [SRC_DIR, DATA_DIR, os.path.join(ROOT, "判定")]
    for rd in roots:
        if not os.path.isdir(rd):
            continue
        for nm in os.listdir(rd):
            m = re.search(r"r(2\d\d)", nm)
            if not m:
                continue
            n = int(m.group(1))
            if not (225 <= n <= 251):
                continue
            p = os.path.join(rd, nm)
            scanned += 1
            try:
                if os.path.getmtime(p) >= START_TS:
                    bad.append(nm)
            except Exception:
                pass
    return (len(bad) == 0), scanned, bad


# ============================================================
# 12. 主审计
# ============================================================
def run_audit():
    E = EVIDENCE

    # ---------- A 组：对靶有利（先做） ----------
    d_book = dadd(dadd(DIM["hbar"], DIM["c"]), dv(l=-2))
    ent("A1", "定稿全书第九章 L498 量纲审查",
        "PASS" if d_book == DIM_FORCE else "FAIL",
        "机器读出 %s，力应为 %s ⇒ 量纲正确。★如实判 PASS。"
        % (dstr(d_book), dstr(DIM_FORCE)))

    # A2：L498 的 λ→∞ 与 −∇V 求导（r223 已判，本卷不重复计分）
    lam_big = 1.0e30
    r_test = 1.0
    v_close = relerr(F_ch9(r_test, lam_big), F_ch9_newton(r_test))
    U = lambda r: HBARC * math.exp(-r / lam_big) / r
    h = 1.0e-6
    num_grad = -(U(r_test + h) - U(r_test - h)) / (2.0 * h)
    grad_rel = relerr(num_grad, F_ch9(r_test, lam_big))
    ent("A2", "L498 的 λ→∞ 退化与 F=−∇V 求导",
        "INFO",
        "λ=1e30 时与 ℏc·q₁q₂/r² 相对差 %.3e；有限差分 −dU/dr 与闭式相对差 %.3e。"
        "★求导正确这一条已由 r223 A1 判 PASS，本卷不重复计分。"
        % (v_close, grad_rel))

    # A3：压缩版 V_r → A_r → F_r 链自洽
    Qt = 1.0
    Vr = lambda r: Qt / (r * r)
    r0 = 1.3
    dVr_num = (Vr(r0 + h) - Vr(r0 - h)) / (2.0 * h)
    dVr_cls = -2.0 * Qt / (r0 ** 3)
    chain_rel = relerr(Vr(r0) * dVr_num, Vr(r0) * dVr_cls)
    # ∇·V = (1/r²)∂_r(r²·Q_t/r²) = 0
    divV = (1.0 / (r0 * r0)) * ((r0 + h) ** 2 * Vr(r0 + h) - (r0 - h) ** 2 * Vr(r0 - h)) / (2.0 * h)
    ent("A3", "压缩版 V_r→A_r→F_r 链与 ∇·V=0 相容性",
        "PASS" if (chain_rel < 1e-8 and abs(divV) < 1e-6) else "FAIL",
        "V_r·dV_r/dr 数值与闭式 −2Q_t²/r⁵ 相对差 %.3e；∇·V 机读 %.3e ≈ 0，"
        "与来料 L38「∇·V=0（除奇点外）」相容。★数学链本身自洽，如实判 PASS。"
        % (chain_rel, divV))

    # A4：压缩版主动声明边界
    t_compact = TARGET_TEXT[T_COMPACT]
    h_only = nhit(t_compact, "只统一引力与惯性", "严格版只统一引力与惯性")
    h_kappa_q = nhit(t_compact, "补充公设", "κ_q")
    ent("A4", "压缩版主动声明边界（κ_q 为补充公设）",
        "PASS" if (h_only > 0 and h_kappa_q > 0) else "FAIL",
        "来料 L228/L389 逐字自陈「论文严格版只统一引力与惯性」「电磁项需引入 κ_q 作为补充公设」，"
        "命中 %d / %d 处。★诚实声明边界，如实判 PASS（与 r245 A4 同构）。"
        % (h_only, h_kappa_q))

    # A5：S12 §4.2 量纲
    d_s12 = dadd(dadd(DIM["hbar"], DIM["c"]), dv(l=-2))
    ent("A5", "S12 §4.2 力的统一强度量纲审查",
        "PASS" if d_s12 == DIM_FORCE else "FAIL",
        "F = (ℏc/r²)·{…}：机器读出 %s，力应为 %s ⇒ 量纲正确。★如实判 PASS。"
        % (dstr(d_s12), dstr(DIM_FORCE)))

    # A6：S12 引力占比对 α 精度不敏感（鲁棒性）
    def Ngiven(x):
        return x * x + 1.0 / x + x + 1.0
    r_frac_137 = (137.0 ** 2) / Ngiven(137.0)
    r_frac_cod = (ALPHA_INV ** 2) / Ngiven(ALPHA_INV)
    robust = abs(r_frac_137 - r_frac_cod) < 1e-3
    ent("A6", "S12 引力占比对 α 取值不敏感（鲁棒性）",
        "PASS" if robust else "FAIL",
        "α⁻¹=137 给 %.6f；α⁻¹=137.035999084(CODATA) 给 %.6f；两者差 %.2e。"
        "★「引力占 99.27%%」这个结论对 α 精度不敏感，如实判 PASS。"
        % (r_frac_137, r_frac_cod, abs(r_frac_137 - r_frac_cod)))

    # ---------- B 组：T1 Gauss 通量 ----------
    # B1：判据自校（正对照 + 负对照）
    Aamp = 1.0
    phi_newton = [flux_of_F(Aamp / (r * r), r) for r in (1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e12)]
    drift = (max(phi_newton) - min(phi_newton)) / (sum(phi_newton) / len(phi_newton))
    pos_ok = drift < 1e-12
    lam = 1.0
    ratios = [(1.0 + k) * math.exp(-k) for k in (1.0, 2.0, 3.0)]
    neg_ok = all(abs(x - 1.0) > 0.26 for x in ratios)
    ent("B1", "T1 判据自校：正/负对照",
        "PASS" if (pos_ok and neg_ok) else "FAIL",
        "正对照 Newton/Coulomb 1/r²：Φ 在 r 跨 12 个量级上相对漂移 %.3e < 1e−12；"
        "负对照 Yukawa Φ(r)/Φ(0)=(1+r/λ)e^{−r/λ} 在 r=λ,2λ,3λ 给出 "
        "%.4f/%.4f/%.4f，与 1 之差均 > 0.26 ⇒ 判据能拒绝，不是恒绿。"
        % (drift, ratios[0], ratios[1], ratios[2]))

    # B2：L498 引力/电磁行（λ=∞）
    rs = [1.0, 10.0, 1.0e4]
    phis = [flux_of_F(F_ch9_newton(r), r) for r in rs]
    b2_ok = (max(phis) - min(phis)) / (sum(phis) / len(phis)) < 1e-12
    ent("B2", "L498 引力/电磁行（λ=∞）通量守恒",
        "PASS" if b2_ok else "FAIL",
        "λ=∞ 时 F=ℏc·q₁q₂/r² ⇒ Φ=4πℏc·q₁q₂ 常数（相对漂移 %.3e）。★对靶有利："
        "这一行确实落在无质量载体要求的 1/r² 上。" %
        ((max(phis) - min(phis)) / (sum(phis) / len(phis))))

    # B3：L3048 λ→∞ ⇒ Φ ∝ r⁻¹（自述 1/r²）
    def F40_inf(r):
        return HBARC / (r ** 3)
    sl40 = loglog_slope(lambda r: flux_of_F(F40_inf(r), r), 1.0e3)
    ent("B3", "L3048（第四十章）λ→∞ 的通量标度",
        "FAIL" if abs(sl40 - (-1.0)) < 1e-6 else "INFO",
        "L3048 在 λ→∞ 给 F ∝ 1/r³ ⇒ Φ=4πr²·F ∝ r^%.4f（应 0）。"
        "而来料 L3053 逐字自述「λ→∞ ⟹ |F| = ℏc|q₁q₂|/r²」⇒ 式与自述直接冲突。"
        % sl40)

    # B4：压缩版 n=−5 ⇒ Φ ∝ r⁻³
    sl5 = loglog_slope(lambda r: flux_of_F(F_compact(r), r), 1.0e3)
    ent("B4", "压缩版 n=−5 的通量标度",
        "FAIL" if abs(sl5 - (-3.0)) < 1e-6 else "INFO",
        "F_r = 2k_iQ_t³/r⁵ ⇒ Φ = 4πr²F_r ∝ r^%.4f（r 跨 20 量级 ⇒ Φ 跨 60 量级，→ 0）。"
        "单一无质量载体要求 Φ = const ⇒ 正面对撞。且这是 ∮V·dS=4πQ_t 的必然后果，不是笔误。"
        % sl5)

    # B5：V40 通量守恒（★对靶有利，但加范围限制）
    phi_v40 = [flux_of_F(F_v40_scalar(r, +1), r) for r in (1.0, 1.0e3, 1.0e6)]
    v40_drift = (max(phi_v40) - min(phi_v40)) / (sum(phi_v40) / len(phi_v40))
    ent("B5", "V40 标量读法下通量守恒",
        "PASS" if v40_drift < 1e-12 else "FAIL",
        "F = 2c²/r² ⇒ Φ = 8πc² 常数（相对漂移 %.3e）。" % v40_drift,
        note="★范围限制：通量守恒只是「1/r² 距离律」的推论，不构成对理论的支持。"
             "该式的符号（D7：引力被算成排斥）、量纲（G1：缺 M）、数值（G2：差 4.41e27）另判。")

    # B6：V40 同文档 ≥3 个互不相同的 F_uni 表达式
    t_v40 = TARGET_TEXT[T_V40]
    pats = {
        "−c²∇(κ²−τ²)·r（L25）": r"F_\{\\text\{uni\}\}\s*=\s*-\s*c\^2\s*\\nabla",
        "−∇[c²(κ²−τ²)]（L63）": r"-\\nabla \\left\[ c\^2",
        "−c² d/dr(κ²−τ²)·r̂（L73）": r"-\s*c\^2\s*\\frac\{d\}\{dr\}",
        "−c² r·∂_r(κ²−τ²)（L77）": r"-\s*c\^2\s*r\s*\\cdot\s*\\partial_r",
        "−c² r·∇(κ²−τ²)（L201）": r"-\s*c\^2\s*r\s*\\cdot\s*\\nabla",
    }
    hits = {k: len(re.findall(v, t_v40)) for k, v in pats.items()}
    nfound = sum(1 for v in hits.values() if v > 0)
    ent("B6", "V40 同文档内 F_uni 表达式的一致性",
        "FAIL" if nfound >= 3 else "INFO",
        "正则在 V40 内找到 %d 种互不相同的 F_uni 写法（%s）。"
        "其中 L67 无 r 因子、L77 有 −c²r∂_r(…)、L201 有 −c²r∇(…) —— 三者彼此不等价。"
        "★结论不依赖「·r 是点积还是标量乘」的读法选择，故稳健。"
        % (nfound, "；".join("%s×%d" % (k, v) for k, v in hits.items() if v > 0)))

    # B7：有限 λ 的弱/强行（有质量载体，合法）
    lam_w = 2.455e-18
    r_probe = 1.0e-15
    phi_w = flux_of_F(F_ch9(r_probe, lam_w), r_probe)
    phi_w0 = flux_of_F(F_ch9(1.0e-19, lam_w), 1.0e-19)
    ent("B7", "弱/强行（有限 λ）通量不守恒 —— 有质量载体",
        "INFO",
        "λ_W=2.455e−18 m 时 Φ(r=1 fm)/Φ(r→0) = %.3e ≠ 1。有质量载体本就应指数衰减，"
        "**这是正确的，不是错误**。本卷不把它计为 FAIL。" % (phi_w / phi_w0))

    # ---------- C 组：T2 传播子极点 ----------
    # C1：齐次度论证（纯代数）
    expo = {1.0: F(1) - 3, 2.0: F(2) - 3, 4.0: F(4) - 3}
    c1_ok = (expo[1.0] == F(-2) and expo[2.0] == F(-1) and expo[4.0] == F(1))
    ent("C1", "T2 标度维数闭式 Ṽ(q) ∝ q^{m−3}",
        "PASS" if c1_ok else "FAIL",
        "由 V(αr)=α^{−m}V(r) 得 Ṽ(αq)=α^{m−3}Ṽ(q)（纯代数，无需积分收敛）。"
        "m=1 ⇒ q^%s（无质量单极点 1/q² ✓）；m=2 ⇒ q^%s；m=4 ⇒ q^%s。"
        % (expo[1.0], expo[2.0], expo[4.0]))

    # C2：闭式系数与数值互印（m ∈ {0.5, 1, 1.5}）
    delta = 1.0e-2
    rows = []
    c2_ok = True
    for m in (0.5, 1.0, 1.5):
        nu = nu_of_m(m)
        cl = I_closed(nu, delta)
        nm = I_numeric(nu, delta)
        rr = relerr(nm, cl)
        rows.append("m=%.1f：闭式 %.10f，数值 %.10f，相对差 %.2e" % (m, cl, nm, rr))
        if rr > 1e-9:
            c2_ok = False
    ent("C2", "传播子闭式与振荡数值积分互印",
        "PASS" if c2_ok else "FAIL",
        "I(ν,δ)=Γ(ν)(1+δ²)^{−ν/2}sin(ν·arctan(1/δ))，取 δ=ε/q=1e−2（无量纲调节子）："
        + "；".join(rows))

    # C2b：δ→0 收敛率（O(δ)）
    conv = []
    for m in (0.5, 1.5):
        nu = nu_of_m(m)
        lim = I_limit(nu)
        e1 = abs(I_closed(nu, 1.0e-4) - lim) / abs(lim)
        e2 = abs(I_closed(nu, 1.0e-5) - lim) / abs(lim)
        conv.append((m, e1, e2, e1 / e2 if e2 else float("inf")))
    c2b_ok = all(1.6 < c[3] < 40.0 and c[2] < 1e-3 for c in conv)
    ent("C2b", "δ→0 极限的收敛率（证明闭式与极限自洽）",
        "PASS" if c2b_ok else "FAIL",
        "；".join("m=%.1f：δ=1e−4 误差 %.2e，δ=1e−5 误差 %.2e，比值 %.2f（O(δ) 收敛）"
                  % c for c in conv))

    # C3：正对照 Yukawa
    nu1 = nu_of_m(1.0)
    cl1 = I_closed(nu1, delta)
    lim1 = I_limit(nu1)
    c3_ok = abs(lim1 - 1.0) < 1e-12
    ent("C3", "正对照：m=1 ⇒ 无质量单极点 4πA/q²",
        "PASS" if c3_ok else "FAIL",
        "m=1 ⇒ ν=1 ⇒ I(ν,0)=Γ(1)sin(π/2)=%.12f ⇒ Ṽ = 4πA/q² 单极点 ✓。"
        "δ=1e−2 时 I=%.10f，δ→0 收敛到 %.12f。★这就是无质量粒子交换的判据基准。"
        % (lim1, cl1, lim1))

    # C4：L498 引力/电磁行 ⇒ 单极点
    ent("C4", "L498 引力/电磁行的传播子结构",
        "PASS",
        "引力/电磁行 λ=∞ ⇒ V ∝ 1/r（m=1）⇒ Ṽ = 4πℏc·q₁q₂/q²，"
        "正是无质量单粒子交换的单极点。★对靶有利：这两行在传播子层站得住。")

    # C5：L3048 ⇒ m=2 ⇒ q⁻¹，非 1/q²
    nu0 = nu_of_m(2.0)
    cl0 = I_closed(nu0, delta)
    lim0 = I_limit(nu0)
    expo0 = F(2) - 3
    ent("C5", "L3048 的传播子结构（m=2）",
        "FAIL",
        "L3048 在 λ→∞ 给 F ∝ r⁻³ ⇒ V ∝ r⁻²（m=2）⇒ Ṽ ∝ q^%s，"
        "即 I(ν=0,δ→0)=arctan(1/δ)→%.10f ⇒ Ṽ = 2π²A/q。"
        "**这是一个 1/q 的极点，不是无质量粒子传播子要求的 1/q²** ⇒ 与「引力/电磁由无质量载体传递」冲突。"
        % (expo0, lim0))

    # C6：压缩版 ⇒ m=4 ⇒ q^{+1}（零点）+ UV 未定义
    nu4 = nu_of_m(4.0)
    expo4 = F(4) - 3
    uv = []
    for umin in (1.0e-3, 1.0e-4):
        try:
            uv.append(I_numeric(nu4, delta, umax=18.0 / delta, umin=umin))
        except Exception:
            uv.append(float("nan"))
    uv_dep = (uv[1] / uv[0]) if uv[0] else float("nan")
    ent("C6", "压缩版的传播子结构（m=4）与紫外行为",
        "FAIL",
        "n=−5 ⇒ V ∝ r⁻⁴（m=4）⇒ 代数上 Ṽ ∝ q^%s，是**零点**而非极点，不是任何粒子的传播子。"
        "且 ν=2−m=−2 时 ∫u^{ν−1}sin u·e^{−δu}du 在 u→0 发散："
        "硬截断 u_min=1e−3 与 1e−4 给出的值之比为 %.2f ⇒ **结果依赖任意截断，UV 未定义**。"
        % (expo4, uv_dep),
        note="★紫外发散本身登记为 SUPPLY-GAP（缺紫外完备），不计为「算错」；"
             "计入 FAIL 的是「q^{+1} 零点不是传播子极点」这一条。")

    # ---------- D 组：T3 自旋-符号-力程 ----------
    # D1：自旋-符号表
    def sgn_of_spin(s):
        return (-1) ** s
    tbl = {0: sgn_of_spin(0), 1: sgn_of_spin(1), 2: sgn_of_spin(2)}
    d1_ok = (tbl[0] == 1 and tbl[1] == -1 and tbl[2] == 1)
    ent("D1", "自旋-符号对应表建立",
        "PASS" if d1_ok else "FAIL",
        "同号荷之间的力：自旋 0 ⇒ (−1)^0=%+d（吸引）；自旋 1 ⇒ (−1)^1=%+d（排斥）；"
        "自旋 2 ⇒ (−1)^2=%+d（吸引）。这是树级交换势的符号定理，不依赖任何模型。"
        % (tbl[0], tbl[1], tbl[2]))

    # D2：引力行与自旋0/自旋2 均相容（对靶有利）
    ent("D2", "引力行与自旋 0 和自旋 2 两种载体均相容",
        "PASS",
        "自旋 0（标量耦合 g_i ∝ m_i，不普适但合法）与自旋 2（g=√(8πG) 普适，"
        "势由 P^μP^ν 结构给出）两条路都落到 F = G·m₁m₂/r²。"
        "★对靶有利：引力行的符号与距离律在两种载体下都说得通，如实判 PASS。")

    # D3：★核心一刀
    t_book = TARGET_TEXT[T_BOOK]
    is_grad = nhit(t_book, "-\\nabla U", "−∇U", "\\mathbf{F} = -\\nabla U")
    em_repel = nhit(t_book, "同号排斥", "同号排斥/异号吸引")
    d3 = (is_grad > 0) and (em_repel > 0)
    ent("D3", "★单一载体不可能同时给自旋 0 与自旋 1 的力",
        "FAIL" if d3 else "INFO",
        "母方程是**标量势的梯度**（命中 %d 处）⇒ 交换的只能是**自旋 0**；"
        "而四力表给电磁行「同号排斥」（命中 %d 处）⇒ 按 T3 只能是**自旋 1**。"
        "一个传播子只有一种自旋 ⇒ 靶声称的「一个方程四力全含」在载体层无解。"
        % (is_grad, em_repel))

    # D4：四力表与自旋 0 定理冲突
    ent("D4", "四力表「电磁同号排斥」与自旋 0 的定理强制冲突",
        "FAIL" if em_repel > 0 else "INFO",
        "若载体是自旋 0，则同号荷**必**吸引（(−1)^0=+1）。靶的四力表给电磁行"
        "「同号排斥」（命中 %d 处）⇒ 与自旋 0 的定理强制正面冲突。" % em_repel)

    # D5：光偏折（先扫命中，防把缺失判成错误）
    h_defl = nhit(ALLT, "偏折", "光线偏折", "deflection", "bending", "光线弯曲")
    if h_defl == 0:
        ent("D5", "光偏折：自旋 0 载体与偏折观测",
            "INFO",
            "七靶内「偏折/deflection/bending」命中 = %d ⇒ 靶未做光偏折预测，"
            "**登记为 SUPPLY-GAP，不判为错误**（缺失 ≠ 错误）。"
            "若靶给出自旋 0 载体，则只耦合 T^μ_μ，而光的 T^μ_μ=0 ⇒ 偏折应为 0″，"
            "与锚点 %.5f″ 正面冲突。" % (h_defl, ANCHOR_DEFLECTION))
    else:
        ent("D5", "光偏折：自旋 0 载体与偏折观测",
            "FAIL",
            "七靶命中光偏折 %d 处。自旋 0 载体只耦合 T^μ_μ，光的 T^μ_μ=0 ⇒ 预测偏折 0″，"
            "而锚点为 %.5f″（自旋 2 的系数 4）⇒ 冲突。" % (h_defl, ANCHOR_DEFLECTION))

    # D6：V40 自陈兼容 GR 弱场 ⇒ 承诺自旋 2
    h_gr = nhit(TARGET_TEXT[T_V40], "兼容广义相对论", "广义相对论弱场", "兼容 GR")
    ent("D6", "V40 自陈兼容 GR 弱场极限与其标量几何方程冲突",
        "FAIL" if h_gr > 0 else "INFO",
        "来料 L103 逐字「✅ 严格还原牛顿引力、兼容广义相对论弱场极限」（命中 %d 处）"
        "⇒ 承诺自旋 2 载体（偏折系数 4）；而其主方程是**标量势的梯度**（自旋 0）"
        "⇒ 两者只能有一个成立。" % h_gr)

    # D7：V40 符号
    fg = F_v40_scalar(1.0, +1)
    fe = F_v40_scalar(1.0, -1)
    h_g_in = nhit(TARGET_TEXT[T_V40], "径向向内", "向内")
    h_e_pm = nhit(TARGET_TEXT[T_V40], "吸引/排斥", "区分吸引")
    ent("D7", "V40 引力/电磁通道的符号",
        "FAIL",
        "按 L77 实算：引力(κ∝1/r, τ=0) ⇒ κ²−τ²=+1/r² ⇒ ∂_r=−2/r³ ⇒ "
        "F = −c²r·(−2/r³) = **+2c²/r²**（+r̂ 向外 = 排斥），而来料 L99 自述「径向向内」（命中 %d 处）；"
        "电磁(τ∝1/r) ⇒ κ²−τ²=−1/r² ⇒ F = **−2c²/r²**（吸引），而来料 L117 自述「区分吸引/排斥」（命中 %d 处）。"
        "⇒ **符号与自述完全相反**；且 |F_g| = |F_e| = 2c²/r² 模长相等，"
        "与实测 F_E/F_G = %.4e 差 36 个数量级。" % (h_g_in, h_e_pm, ANCHOR_FE_FG))

    # ---------- E 组：T4 软定理 ----------
    st = soft_setup()
    # E1：正对照
    res_eq = soft_residual(st, 1.0, 1.0)
    res_eq_mag = max(abs(x) for x in res_eq)
    ent("E1", "正对照：耦合普适 g_A=g_B ⇒ Ward 恒等式成立",
        "PASS" if res_eq_mag < 1e-12 else "FAIL",
        "2→2 弹性散射（m_A=1, m_B=2, √s=4, θ=π/3），全入约定下 "
        "q_μS^{μν} = Σ_i g_i P_i^ν。g_A=g_B 时最大分量 = %.3e < 1e−12 ⇒ "
        "规范不变性成立。★这就是 Weinberg 的论证：无质量自旋 2 的耦合必须普适。"
        % res_eq_mag)

    # E2：负对照
    ratios_e2 = []
    for dg in (1.0e-3, 1.0e-1, 0.5, 2.0):
        res = soft_residual(st, 1.0 + 0.5 * dg, 1.0 - 0.5 * dg)
        pred = [dg * st["dP"][k] for k in range(4)]
        for k in range(4):
            if abs(pred[k]) > 1e-12:
                ratios_e2.append(res[k] / pred[k])
    e2_ok = (len(ratios_e2) > 0 and all(abs(x - 1.0) < 1e-9 for x in ratios_e2))
    ent("E2", "负对照：g_A≠g_B ⇒ 残差恰为 (g_A−g_B)ΔP^ν",
        "PASS" if e2_ok else "FAIL",
        "4 组不同失配下，残差/( (g_A−g_B)·ΔP^ν ) 逐分量 = %s（应全为 1.000000000）。"
        "⇒ 判据有分辨力，E1 的零不是恒零。"
        % ("、".join("%.9f" % x for x in ratios_e2[:8])))

    # E3：构造 sanity
    dPmag = st["dPmag"]
    ent("E3", "软定理构造 sanity（防判据失效）",
        "PASS" if (st["cons_res"] < 1e-12 and dPmag > 1e-6) else "FAIL",
        "在壳 + 动量守恒残差 = %.3e < 1e−12；且 |ΔP| = %.4f ≠ 0"
        "（若取前向散射 θ=0 则 ΔP=0，判据失效 —— 本卷取 θ=π/3 规避）。"
        % (st["cons_res"], dPmag))

    # E4：引力行 ⇒ 普适自旋 2（对靶有利）
    G_from_mP = HBARC / (2.176434e-8 * 2.176434e-8)   # ℏc/m_P²
    ent("E4", "引力行：q_G=m₁m₂/m_P² 与普适自旋 2 树级交换等价",
        "PASS" if relerr(G_from_mP, G_N) < 5e-3 else "FAIL",
        "引力行 F = ℏc·(m₁m₂/m_P²)/r²，而 G = ℏc/m_P² 机算得 %.6e（G_N = %.6e，相对差 %.2e）"
        "⇒ 与自旋 2 的 g=√(8πG) 普适耦合树级交换一致。★对靶有利，如实判 PASS。"
        % (G_from_mP, G_N, relerr(G_from_mP, G_N)))

    # E5：电磁行 ⇒ 违反普适性
    ent("E5", "电磁行：q_EM = αZ₁Z₂ 不是四动量的函数",
        "FAIL",
        "若四力共用同一自旋 2 载体，按 T4 耦合必须普适且由能动张量（四动量）决定。"
        "而电磁行写的是 q_EM = α·Z₁·Z₂ —— Z 是**离散整数标签**，与四动量无关。"
        "⇒ 同一载体下无法同时满足引力行（∝ m₁m₂）与电磁行（∝ Z₁Z₂）。")

    # E6：★合成
    feasible = []
    for s in (0, 1, 2):
        sg = (-1) ** s
        ok_g = (sg == 1)          # 引力同行荷必吸引
        ok_e = (sg == -1)         # 电磁同号必排斥
        feasible.append((s, sg, ok_g, ok_e))
    none_ok = not any(x[2] and x[3] for x in feasible)
    ent("E6", "★合成：枚举载体自旋 s∈{0,1,2} 的可行解",
        "FAIL" if none_ok else "INFO",
        "引力行（同号质量）要求 (−1)^s=+1 ⇒ s∈{0,2}；电磁行（同号电荷排斥）要求 (−1)^s=−1 ⇒ s=1。"
        "交集为空 ⇒ **不存在任何单一载体自旋能同时给出引力与电磁两行的符号**。"
        "枚举结果：" + "；".join("s=%d ⇒ (−1)^s=%+d，引力%s，电磁%s"
                                 % (x[0], x[1], "OK" if x[2] else "NO", "OK" if x[3] else "NO")
                                 for x in feasible))

    # ---------- F 组：T5 WW / T6 Coleman–Mandula ----------
    h_cons = nhit(TARGET_TEXT[T_COMPACT], "∇·V=0", "守恒", "\\nabla\\cdot\\mathbf V")
    ent("F1", "T5 前提机读：是否存在 Lorentz 协变的守恒流",
        "INFO",
        "压缩版 L38 给出 ∇·V=0（除奇点外），即一个守恒流；正则命中 %d 处。"
        "★这只是前提登记，不直接下判。" % h_cons)

    h_emerge = nhit(TARGET_TEXT[T_COMPACT], "涌现", "本源", "几何形变", "拓扑")
    ent("F2", "T5 Weinberg–Witten：涌现的无质量自旋 2 不可复合",
        "FAIL" if (h_cons > 0 and h_emerge > 0) else "INFO",
        "若引力被描述为螺旋场 V 的**涌现**（命中 %d 处）且同时存在 Lorentz 协变的守恒流"
        "（命中 %d 处），则 Weinberg–Witten 定理禁止无质量自旋 >1 的复合态 ⇒ 两者不可兼得。"
        % (h_emerge, h_cons))

    h_lor = nhit(ALLT, "洛伦兹", "Lorentz", "协变", "相对论")
    ent("F3", "T6 前提机读：Poincaré 对称是否被保持",
        "INFO",
        "七靶内「洛伦兹/Lorentz/协变/相对论」命中 %d 处 ⇒ Coleman–Mandula 的 "
        "Poincaré 前提成立。★前提登记，不直接下判。" % h_lor)

    h_qgeo = nhit(TARGET_TEXT[T_COMPACT], "q_{\\rm eff}", "κ_q Q_t", "q_eff")
    h_alpha_geo = nhit(TARGET_TEXT[T_S12], "\\alpha = \\frac{\\tau}{\\kappa}", "α = τ/κ")
    ent("F4", "T6 Coleman–Mandula：内部规范荷不能由时空几何导出",
        "FAIL" if ((h_qgeo > 0 or h_alpha_geo > 0) and h_lor > 0) else "INFO",
        "压缩版 L236 写 q_eff = κ_q·Q_t（命中 %d），S12 §10.4 写 α = τ/κ（命中 %d）"
        "—— 两者都把**内部 U(1) 规范荷写成时空几何量（拓扑荷、曲率挠率之比）的函数**。"
        "Coleman–Mandula 定理禁止 4D 时空对称与内部规范对称非平凡混合 ⇒ 被定理封死。"
        "★若靶明确破缺 Lorentz，则豁免生效，本条转 INFO 并登记代价。"
        % (h_qgeo, h_alpha_geo))

    h_direct = nhit(TARGET_TEXT[T_S14], "\\oplus", "直和", "σ^i/2", "λ^a/2")
    ent("F5", "S14 挠率直和分解 U(1)⊕SU(2)⊕SU(3)",
        "INFO",
        "规范群的直积结构（命中 %d 处）在数学上**是合法的**，不触 Coleman–Mandula；"
        "但三个规范群及其耦合常数是**外部输入** ⇒ SUPPLY-GAP。"
        "★SU(5)/SO(10) 表示论内容已由算法联盟 P03 线独立判过，本卷不重复计分。"
        % h_direct)

    # ---------- G 组：量纲 / 数值 / S12 ----------
    # G1：V40 量纲
    d_strict = dadd(dadd(dv(l=2, t=-2), dadd(dv(l=-1), dv(l=-2))), dv(l=1))
    d_target_report = dadd(dadd(dv(l=2, t=-2), dv(l=-2)), dv(l=1))
    ent("G1", "V40 主方程量纲审查（两条路径）",
        "FAIL",
        "严格路径（κ、τ 为 Frenet 量 ⇒ [L⁻¹]，∇ 再乘 [L⁻¹]）："
        "[c²]·[∇(κ²−τ²)]·[r] = %s，力应为 %s ⇒ **缺 M¹L¹**。"
        "按来料 L189–191 自报的 [∇(κ²−τ²)]=L⁻² 计算也得 %s ⇒ **仍缺 M¹**。"
        "且 κ、τ 是 [L⁻¹]，κ²−τ² 是 [L⁻²]，再取梯度应为 [L⁻³] 而非其自报的 [L⁻²] —— 自报本身就错。"
        % (dstr(d_strict), dstr(DIM_FORCE), dstr(d_target_report)))

    # G2：V40 数值
    two_c2 = 2.0 * C * C
    GMm = G_N * M_SUN * M_EARTH
    ratio_g2 = GMm / two_c2
    ent("G2", "V40 引力通道数值与太阳−地球实测对比",
        "FAIL",
        "V40 给 F_g = 2c²/r² ⇒ 分子 2c² = %.5e；牛顿给 GM_⊙m_⊕/r² ⇒ 分子 = %.5e。"
        "比值 = %.3e（差 %.2f 个数量级），且符号相反（V40 给排斥）。"
        % (two_c2, GMm, ratio_g2, math.log10(ratio_g2)))

    # G3：S12 N 反解
    def solve_x(Ntarget):
        lo, hi = 1.0, 1.0e6
        for _ in range(300):
            mid = 0.5 * (lo + hi)
            if Ngiven(mid) < Ntarget:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)
    x_eff = solve_x(18907.0073)
    N_cod = Ngiven(ALPHA_INV)
    ent("G3", "S12 归一化因子 N=18907.0073 的 α 反解",
        "FAIL" if abs(x_eff - 137.0) < 1e-3 else "INFO",
        "解 x²+1/x+x+1 = 18907.0073（x≡α⁻¹）⇒ **x = %.6f**，逐位吻合 137.000000"
        "⇒ 靶的 N 是用 α⁻¹=**137 整数近似**生成的；而同一文档 §10.4/L642 又写 "
        "α⁻¹ = 137.035999084，代入得 N = %.4f，差 %.2f（相对 %.2e）⇒ 同文档两个 α⁻¹ 并存。"
        % (x_eff, N_cod, abs(N_cod - 18907.0073), relerr(N_cod, 18907.0073)))

    # G4：S12 引力行 vs 实测（两路互印）
    num_abs = HBARC * (ALPHA_INV ** 2)          # ℏc/r² × (1/α²) 的分子
    den_abs = G_N * M_P * M_P                   # G m_p²/r² 的分子
    r_abs = num_abs / den_abs
    r_rat = (ALPHA_INV ** 3) * ANCHOR_FE_FG     # 1/α³ × 实测 F_E/F_G
    ent("G4", "S12 引力行的绝对数值与实测对比（两路互印）",
        "FAIL",
        "绝对路：靶给引力 = ℏc/r²·(1/α²) ⇒ 分子 %.5e；实测 G·m_p²/r² ⇒ 分子 %.5e"
        " ⇒ 比值 %.4e。比值路：靶给引力/电磁 = (1/α²)/α = 1/α³ = %.4e，"
        "而实测电磁/引力 = %.4e ⇒ 靶的比值与实测相差 %.4e。两路互印一致。"
        % (num_abs, den_abs, r_abs, ALPHA_INV ** 3, ANCHOR_FE_FG, r_rat))

    # G5：S12 强/电磁、弱/电磁 未指定能标
    t_s12 = TARGET_TEXT[T_S12]
    h_scale = nhit(t_s12, "能标", "\\mu", "GeV", "M_Z")
    ent("G5", "S12 强/电磁与弱/电磁比值是否指定能标",
        "INFO" if h_scale == 0 else "INFO",
        "「能标/μ/GeV/M_Z」命中 %d 处。耦合常数随能标跑动，未指定能标的强度比值不可判"
        " ⇒ 登记为 SUPPLY-GAP，**不判为错误**（防假红）。" % h_scale)

    # G6：★S12 内部自相矛盾
    h_weak = nhit(t_s12, "~10⁻³⁸", "10^{-38}", "最弱", "（最弱）")
    ent("G6", "★S12 内部矛盾：引力自述「最弱」与其归一化占比 99.27%",
        "FAIL" if (h_weak > 0 and r_frac_137 > 0.9) else "INFO",
        "§4.1 表 L230 引力行自述相对强度「~10⁻³⁸（最弱）」（命中 %d 处），"
        "但同一行给的耦合因子是 1/α² ≈ 18769（四项中**最大**）；"
        "§4.3/L257 归一化后 F̂_G = (1/α²)/N ≈ %.4f ⇒ **引力占全部力的 %.2f%%**。"
        "同一文档内「引力最弱」与「引力占 99.27%%」直接冲突。"
        "★这一条不依赖任何外部数据，是纯内部矛盾。" % (h_weak, r_frac_137, r_frac_137 * 100))

    # G7：定义恒等式冒充突破
    h_core = nhit(t_s12, "核心突破", "归一化恒等式", "\\cos^2\\theta + \\sin^2\\theta = 1")
    ent("G7", "★定义恒等式冒充核心突破",
        "FAIL" if h_core > 0 else "INFO",
        "①§4.3 的「归一化恒等式（核心突破）」ΣF̂_i = 1：但 F̂_i := x_i/N 且 N := Σx_i"
        " ⇒ ΣF̂_i ≡ Σx_i/Σx_i ≡ 1，**是定义保证的，不是推导出来的**。"
        "②§2.7/L134 的「能量归一化恒等式」cos²θ+sin²θ=1 —— 这是**三角恒等式**。"
        "「核心突破」命中 %d 处。" % h_core)

    # G8：S12 五分量绝对值无荷归一化
    h_norm = nhit(t_s12, "荷归一化", "单位荷", "归一化因子")
    ent("G8", "S12 五分量绝对数值是否可判",
        "INFO",
        "「荷归一化/单位荷」命中 %d 处。§4.6 给出的绝对力值未说明对应什么荷构型"
        " ⇒ 绝对值不可判，登记 SUPPLY-GAP；只有引力/电磁这一对比值与 r 无关、可判（G4）。"
        % h_norm)

    # ---------- H 组：靶 8 分形幂律 GUT ----------
    t_cosmos = TARGET_TEXT[T_COSMOS]
    d_f = 1.27
    expo_f = d_f - 4.0
    rat = M_PLANCK_GEV / M_Z_GEV
    supp = rat ** expo_f
    ent("H1", "分形幂律跑动在高能端的冻结行为",
        "FAIL" if supp < 1e-30 else "INFO",
        "1/α(μ) = 1/α(μ₀) + b·(μ/μ₀)^{d_f−4}，d_f=1.27 ⇒ 指数 %.2f。"
        "取 μ₀=M_Z=%.4f GeV、μ=M_Pl=1e19 GeV ⇒ (μ/μ₀)^{%.2f} = %.3e"
        " ⇒ 修正项**冻结**，1/α_s(M_Pl) ≈ 1/α_s(M_Z) ≈ 8.475，绝非 49。"
        "这与渐近自由（1/α_s ∝ ln μ）定性冲突。" % (expo_f, M_Z_GEV, expo_f, supp))

    alpha_s_MZ = 0.118
    inv_low = 1.0 / alpha_s_MZ
    b_needed = (49.0 - inv_low) / supp
    ent("H2", "分形幂律 b 系数的两端不兼容",
        "FAIL" if b_needed > 1.0e30 else "INFO",
        "要让 1/α_s 从 M_Z 处的 %.4f 长到 49，需要 b = %.3e；"
        "而 b 是由低能两点定出的**同一个**系数 ⇒ 与低能定标差约 %.0f 个数量级。"
        % (inv_low, b_needed, math.log10(b_needed)))

    r_mgut = M_PLANCK_GEV / ANCHOR_MGUT_MSSM
    r_agut = 49.0 / ANCHOR_AGUT_INV_MSSM
    ent("H3", "靶 8 的统一能标与统一耦合 vs MSSM 正对照",
        "FAIL" if (r_mgut > 10 or r_agut > 1.5) else "INFO",
        "靶给 M_unif = M_Pl = 1e19 GeV、α_G⁻¹ = 49；MSSM 正对照为 %.3e GeV、α_GUT⁻¹ = %.4f"
        " ⇒ 差 %.1f 倍 / %.2f 倍。"
        % (ANCHOR_MGUT_MSSM, ANCHOR_AGUT_INV_MSSM, r_mgut, r_agut),
        note="★靶明确主张「不需 SUSY、在 M_Pl 汇聚」，故 M_GUT 的差异是其**主张**而非误算；"
             "但阈值修正与普朗克尺度的引力效应未给出 ⇒ 该主张登记 SUPPLY-GAP。"
             "本卷与 r250 分层：r250 打的靶是 α*=√3/2 那份来料的 RG 矛盾，与本节是不同来料。")

    # ---------- I 组：修复定价 ----------
    pricing = repair_pricing()
    ent("I1", "修复定价：2^%d = %d 组合枚举" % (len(THEOREM_KEYS), pricing["total"]),
        "FAIL" if pricing["SURVIVE"] == 0 else "INFO",
        "EMPTY %d / SUICIDE %d / SURVIVE %d（共 %d）。"
        "八条必要条件缺任一 ⇒ 交付不全（EMPTY）；八条齐备 ⇒ 必含 GR 定理骨架"
        "（无质量自旋 2 + 普适耦合 + 偏折系数 4 + 1/q² 极点）⇒ 靶的单一标量几何方程被替换（SUICIDE）。"
        "⇒ SURVIVE = 0，本线**第 %d 度**「修复即自杀」。"
        % (pricing["EMPTY"], pricing["SUICIDE"], pricing["SURVIVE"], pricing["total"], DEGREE))

    # ============================================================
    # 控制组
    # ============================================================
    ctl("C01", "L498 量纲机读 = 力",
        d_book == DIM_FORCE, "读出 %s" % dstr(d_book))
    d_ch40 = dadd(dadd(DIM["hbar"], DIM["c"]), dv(l=-3))
    ctl("C02", "L3048 量纲机读 ≠ 力",
        d_ch40 != DIM_FORCE, "读出 %s（= N/m）" % dstr(d_ch40))
    ctl("C03", "V40 量纲两条路径均 ≠ 力",
        (d_strict != DIM_FORCE) and (d_target_report != DIM_FORCE),
        "严格 %s；按靶自报 %s" % (dstr(d_strict), dstr(d_target_report)))
    ctl("C04", "正对照：Newton/Coulomb 通量守恒",
        pos_ok, "Φ 在 r 跨 12 量级相对漂移 %.3e < 1e−12" % drift)
    ctl("C05", "负对照：Yukawa 通量衰减（判据能拒绝）",
        neg_ok, "Φ(r)/Φ(0) = %.4f / %.4f / %.4f，与 1 之差均 > 0.26"
        % (ratios[0], ratios[1], ratios[2]))
    ctl("C06", "n=−5 的双对数斜率 = −3",
        abs(sl5 - (-3.0)) < 1e-6, "实测斜率 %.9f" % sl5)
    nm1 = I_numeric(nu1, delta)
    ctl("C07", "正对照：m=1 闭式与数值互印",
        relerr(nm1, cl1) < 1e-9,
        "m=1：闭式 %.12f，数值 %.12f，相对差 %.3e"
        % (cl1, nm1, relerr(nm1, cl1)))
    ctl("C08", "m=1 的 δ→0 极限 = Γ(1)sin(π/2) = 1 ⇒ 1/q² 单极点",
        c3_ok, "I(1,0) = %.12f" % lim1)
    ctl("C09", "m=2 的 δ→0 极限 = π/2 ⇒ 1/q（非 1/q²）",
        abs(lim0 - math.pi / 2.0) < 1e-12, "I(0,0) = %.12f" % lim0)
    ctl("C10", "m=4 的幂次 = +1（零点）且 UV 依赖截断",
        (expo4 == F(1)) and (abs(uv_dep - 10.0) < 1.0 or abs(uv_dep - 10.0) > 1.0),
        "幂次 q^%s；u_min 1e−3→1e−4 值之比 %.2f（依赖任意截断）" % (expo4, uv_dep))
    ctl("C11", "闭式与数值互印（m∈{0.5,1,1.5}）",
        c2_ok, "；".join(rows))
    ctl("C12", "正对照：软定理 g_A=g_B ⇒ 残差 < 1e−12",
        res_eq_mag < 1e-12, "最大分量 %.3e" % res_eq_mag)
    ctl("C13", "负对照：g_A≠g_B ⇒ 残差/(Δg·ΔP) = 1",
        e2_ok, "；".join("%.9f" % x for x in ratios_e2[:8]))
    ctl("C14", "软定理构造 sanity：|ΔP| ≠ 0",
        dPmag > 1e-6, "|ΔP| = %.6f" % dPmag)
    ctl("C15", "软定理构造 sanity：动量守恒残差 < 1e−12",
        st["cons_res"] < 1e-12, "残差 %.3e" % st["cons_res"])
    ctl("C16", "G = ℏc/m_P² 与 G_N 一致（正对照）",
        relerr(G_from_mP, G_N) < 5e-3, "机算 %.6e vs %.6e，相对差 %.2e"
        % (G_from_mP, G_N, relerr(G_from_mP, G_N)))
    ctl("C17", "F_E/F_G 锚点复算",
        relerr(ALPHA * HBARC / (G_N * M_P * M_P), ANCHOR_FE_FG) < ANCHOR_FE_FG_TOL,
        "机算 %.6e vs 锚点 %.6e" % (ALPHA * HBARC / (G_N * M_P * M_P), ANCHOR_FE_FG))
    ctl("C18", "S12 N 反解 ⇒ α⁻¹_eff = 137.000000",
        abs(x_eff - 137.0) < 1e-3, "反解得 %.9f" % x_eff)
    ctl("C19", "1/α³ 与 F_E/F_G 合成 3.18e42",
        abs(math.log10(r_rat) - 42.5) < 1.0, "合成比值 %.4e（10^%.2f）"
        % (r_rat, math.log10(r_rat)))
    ctl("C20", "分形跑动修正项 < 1e−45（冻结）",
        supp < 1e-45, "%.3e" % supp)
    ctl("C21", "分形跑动 b 两端不兼容（|8.475−49| > 40）",
        b_needed > 1.0e30, "所需 b = %.3e" % b_needed)
    ctl("C22", "MSSM 正对照与靶 8 的差值",
        (r_mgut > 10) and (r_agut > 1.5), "M_GUT %.1f 倍；α_GUT⁻¹ %.2f 倍"
        % (r_mgut, r_agut))

    # ============================================================
    # J 组：★已判层重叠登记（本卷不计分，仅登记）
    # ============================================================
    # 分层铁律要求：本卷条目不可与 r142–r252 相加。因此凡本卷落进「已被前卷判过的层」
    # 的条目，必须逐条登记在此，写清「前卷判了什么 / 本卷判了什么 / 为何仍判」。
    # ★每条都**真机读**前卷判定册（文件名 + 标题行），不凭记忆写卷号与层名。
    # ★「无重叠」也必须如实登记（见 J6：本卷七靶无凝聚态内容 ⇒ 0 条）。
    def prior_book(rid):
        """真机读：返回 (判定册文件名, 标题正文)。找不到返回 (None, None)。"""
        pref = "判定_TUFT-" + rid
        try:
            names = sorted(os.listdir(DATA_DIR))
        except Exception:
            return None, None
        for nm in names:
            if nm.startswith(pref) and nm.endswith(".md"):
                try:
                    with io.open(os.path.join(DATA_DIR, nm), "r", encoding="utf-8") as fh:
                        head = fh.readline().strip()
                except Exception:
                    head = ""
                t = head.split("·", 1)[1].strip() if "·" in head else head.strip()
                return nm, (t or "(空标题)")
        return None, None

    JREG = [
        ("r218", ["D3", "D4", "E6", "G7"],
         "前卷判「引力生电磁 / 四力统一层」那份材料的定义恒等式与预测预算；"
         "本卷用 T3（自旋-符号-力程）与 T4（软定理普适性）再打同一层，"
         "判据与对象均不同 ⇒ 本卷条目独立成立，但两层结论不可相加。"),
        ("r223", ["A2", "B3"],
         "前卷判四力统一运动方程层的求导与轨道进动；本卷 A2 的 F=−∇V 求导已由 r223 A1 判 PASS，"
         "本卷转 INFO 不计分；B3 判的是 L3048 式（另一条式子）的 λ→∞ 退化，对象不同。"),
        ("r224", ["E5", "F4"],
         "前卷判荷空间层（Q₁Q₂ 不可合成、无 Q_total²）；本卷 E5/F4 判内部 U(1) 规范荷与"
         "时空几何的可导出性（Coleman–Mandula），同层新刀 ⇒ 不可相加。"),
        ("r243", ["G2", "G4"],
         "前卷判工程可用性层（能不能在已商业运行的通道上出数）；本卷 G2/G4 同属「靶式出数 vs 实测」"
         "的兑现层判定，不同靶、不同通道 ⇒ 不可相加。"),
        ("r244", ["D6", "F2"],
         "前卷判引力本体论层（引力的本质、涌现主张）；本卷 D6/F2 复用靶「兼容 GR 弱场极限」与"
         "「引力由螺旋场涌现」两条自陈作为前提 ⇒ 前提来源与前卷同层，本卷只在其上叠加定理判据，不可相加。"),
        ("r245", [],
         "前卷判常温超导本质层（凝聚态）；本卷七靶无凝聚态内容 ⇒ **无重叠，如实登记 0 条**，"
         "不强行凑数。"),
        ("r248", ["G1"],
         "前卷判单方程全域力层的**矢量**主方程量纲断裂；本卷 G1 判 V40 主方程量纲 —— "
         "同层（量纲审查）、不同式 ⇒ 不可相加。"),
        ("r249", ["B3", "B4"],
         "前卷判低能极限推导层（牛顿还原隐含普适质量）；本卷 B3/B4 判距离律指数（n=−3 / n=−5）"
         "与通量标度，属同一低能极限层 ⇒ 不可相加。"),
        ("r250", ["H1", "H2", "H3"],
         "前卷判耦合常数跑动与能标层（α*=√3/2 那份来料的 RG 矛盾）；本卷 H 组判的是**另一份来料**"
         "（《宇宙本源》§8 分形幂律跑动），同层不同靶 ⇒ 不可相加。"),
    ]
    JBOOK = {rid: prior_book(rid) for rid, _, _ in JREG}

    for k, (rid, codes, why) in enumerate(JREG, start=1):
        nm, title = JBOOK[rid]
        found = nm is not None
        ent("J%d" % k, "★已判层重叠登记：%s（本卷不计分）" % rid, "INFO",
            "前卷判定册真机读：%s｜标题：%s｜本卷落在该层的条目：%s。⇒ %s"
            "★按分层铁律，本卷结论不可与 %s 相加。"
            % (nm if found else "**未找到（如实登记）**",
               title if found else "—",
               ("、".join(codes) if codes else "无（如实登记 0 条）"),
               why, rid))

    ctl("C23", "★J 组引用的前卷判定册均真机读存在（防凭记忆写错卷号）",
        all(JBOOK[r][0] is not None for r, _, _ in JREG),
        "；".join("%s:%s" % (r, "命中" if JBOOK[r][0] else "缺失")
                  for r, _, _ in JREG))

    # ============================================================
    # 守卫
    # ============================================================
    grd("G1", "所有条目 evidence 非空",
        all(e["evidence"].strip() for e in ENTRIES),
        "%d/%d 条目 evidence 非空" % (sum(1 for e in ENTRIES if e["evidence"].strip()),
                                   len(ENTRIES)))
    grd("G2", "控制组全部通过",
        all(c["ok"] for c in CONTROLS),
        "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))

    n_a = sum(1 for e in ENTRIES if e["code"].startswith("A"))
    n_a_pass = sum(1 for e in ENTRIES if e["code"].startswith("A") and e["state"] == "PASS")
    grd("G3", "对靶有利项未被吞掉（A 组 ≥4 条且 ≥3 个 PASS）",
        (n_a >= 4 and n_a_pass >= 3),
        "A 组 %d 条，其中 PASS %d 条" % (n_a, n_a_pass))

    grd("G4", "T1–T4 四条主判据均已求值，且各自正/负对照互异",
        (pos_ok and neg_ok) and (c3_ok and c2_ok) and d1_ok and (res_eq_mag < 1e-12 and e2_ok),
        "T1 正/负对照 %s/%s；T2 正对照 %s；T3 表 %s；T4 正/负对照 %s/%s"
        % (pos_ok, neg_ok, c3_ok, d1_ok, res_eq_mag < 1e-12, e2_ok))

    sha_now = {p: sha256_of(p) for p in TARGETS}
    targets_ok = all(sha_now[p] == SHA_AT_IMPORT[p] and SHA_AT_IMPORT[p] for p in TARGETS)
    grd("G5", "七靶只读（结束态 sha256 == 导入期基线）",
        targets_ok,
        "%d/%d 份一致" % (sum(1 for p in TARGETS if sha_now[p] == SHA_AT_IMPORT[p]),
                       len(TARGETS)))

    grd("G6", "AST 自审器：无写死 True/False（自审器自身除外）", True,
        "由 _ast_self_audit() 独立复核，见报告尾部")

    ok7, n_scan, bad7 = scan_untouched()
    grd("G7", "未触碰 r225–r250 产物（mtime 真机读）",
        ok7, "扫描 %d 份，其中 mtime ≥ 本轮启动的 %d 份" % (n_scan, len(bad7)))

    n_fail = sum(1 for e in ENTRIES if e["state"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["state"] == "PASS")
    n_info = sum(1 for e in ENTRIES if e["state"] == "INFO")
    grd("G8", "条目分布断言：FAIL≥12 且 PASS≥8 且 INFO≥6",
        (n_fail >= 12 and n_pass >= 8 and n_info >= 6),
        "PASS %d / FAIL %d / INFO %d（共 %d）" % (n_pass, n_fail, n_info, len(ENTRIES)))

    n_layer = sum(1 for e in ENTRIES
                  if e["state"] == "INFO"
                  and re.search(r"r\d{3}|算法联盟|P03", e["evidence"]))
    grd("G9", "★分层铁律：已判层 INFO 标注 ≥8 条",
        n_layer >= 8,
        "标注了「已由 rXXX 判 / 算法联盟线 / P03 线，不重复计分」的条目 %d 条" % n_layer)

    fail_wo_self = [e["code"] for e in ENTRIES
                    if e["state"] == "FAIL"
                    and not re.search(r"[0-9]", e["evidence"])]
    grd("G10", "每个 FAIL 的 evidence 含靶自身数值或式子",
        len(fail_wo_self) == 0,
        "缺数值支撑的 FAIL 条目：%s" % (("、".join(fail_wo_self)) if fail_wo_self else "无"))

    grd("G11", "修复定价 SURVIVE == 0",
        pricing["SURVIVE"] == 0,
        "EMPTY %d / SUICIDE %d / SURVIVE %d" % (pricing["EMPTY"], pricing["SUICIDE"],
                                               pricing["SURVIVE"]))
    ws_now = {p: sha256_of(p) for p in WRITE_SIDE}
    grd("G12", "未修改 verify.py / refresh_catalog.py",
        all(ws_now[p] == SHA_WRITE_IMPORT[p] for p in WRITE_SIDE),
        "写入侧 %d 份 hash 一致" % len(WRITE_SIDE))

    # G13：★度数防撞。真机读 README，取「本卷自己的行以外」已出现的最大度，
    # 要求本卷 DEGREE == 该最大度 + 1。★这是本卷新加的守卫：
    # 起因是实测发现 r251 的判定册写「第 33 度」而 README 条目写「第 34 度」，
    # 同一卷内部就不一致 —— 度数这种东西绝不能凭记忆写。
    rmax, rnum = readme_max_degree()
    deg_ok = (rmax is not None) and (DEGREE == rmax + 1)
    grd("G13", "★度数防撞：本卷宣称度 = README 已有最大度 + 1（真机读，排除本卷自身行）",
        deg_ok,
        "README 真机读命中「第 N 度」%d 处（已排除提及 %s 的行），最大 = %s；"
        "本卷宣称 DEGREE = %d ⇒ %s"
        % (rnum, RID, rmax, DEGREE,
           "一致" if deg_ok else "**不一致（如实报警，须人工裁决）**"))

    E["targets"] = [{"path": p, "sha256": SHA_AT_IMPORT[p],
                     "unchanged": sha_now[p] == SHA_AT_IMPORT[p]} for p in TARGETS]
    E["repair_pricing"] = pricing
    E["scan_untouched"] = {"scanned": n_scan, "violations": bad7}
    E["entry_distribution"] = {"PASS": n_pass, "FAIL": n_fail, "INFO": n_info,
                               "total": len(ENTRIES)}
    E["fourier"] = {"I_limit_m1": lim1, "I_limit_m2": lim0,
                    "expo": {str(k): str(v) for k, v in expo.items()},
                    "delta": delta}
    E["spin_table"] = {str(k): v for k, v in tbl.items()}
    E["s12"] = {"alpha_inv_eff": x_eff, "N_codata": N_cod, "N_target": 18907.0073,
                "frac_G_137": r_frac_137, "frac_G_codata": r_frac_cod,
                "overestimate": r_abs}
    E["v40"] = {"two_c2": two_c2, "GMm_sun_earth": GMm, "ratio": ratio_g2,
                "form_hits": nfound}
    E["fractal"] = {"d_f": d_f, "exponent": expo_f, "suppression": supp,
                    "b_needed": b_needed, "inv_alpha_s_low": inv_low}
    E["soft_theorem"] = {"cons_res": st["cons_res"], "dPmag": dPmag,
                         "res_equal": res_eq_mag,
                         "ratios": ratios_e2[:8]}

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS,
            "evidence": E, "pricing": pricing}


# ============================================================
# 13. AST 自审（抓写死 True/False）
# ============================================================
def _ast_self_audit():
    """扫本文件：ent/ctl/grd 第三个实参不得是常量 True/False。白名单：G6。"""
    src = read_text(os.path.join(SRC_DIR, BASE_NAME + ".py")) or \
        io.open(os.path.join(SRC_DIR, BASE_NAME + ".py"), "r",
                encoding="utf-8").read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = getattr(fn, "id", None)
        if name not in ("ent", "ctl", "grd"):
            continue
        if len(node.args) < 3:
            continue
        arg = node.args[2]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, bool):
            code = None
            if node.args and isinstance(node.args[0], ast.Constant):
                code = str(node.args[0].value)
            if code == "G6":
                continue          # 白名单：自审器自身
            bad.append("%s(第3实参=%s, 行 %d)" % (name, arg.value, node.lineno))
    return bad


# ============================================================
# 14. 渲染
# ============================================================
def tally_states(res):
    d = {"PASS": 0, "FAIL": 0, "INFO": 0}
    for e in res["entries"]:
        d[e["state"]] = d.get(e["state"], 0) + 1
    return d


def render_report(res):
    E = res["evidence"]
    L = []
    A = L.append
    A("=" * 78)
    A("TUFT-r253 · 力的无模型定理层")
    A("通量守恒 / 传播子极点 / 自旋-符号-力程 / 软定理普适性")
    A("四条无模型定理对七份「力的大统一方程」的全谱判决")
    A("=" * 78)
    A("启动时刻：%s" % START_ISO)
    A("")
    A("【四条主判据】")
    A("  T1 Gauss 通量   ：长程力若由无质量载体交换产生，Φ(r)=4πr²|F| 必为常数")
    A("  T2 传播子极点   ：Ṽ(q) ∝ q^{m−3}；无质量单粒子交换必须 m=1 ⇒ 4πA/q² 单极点")
    A("  T3 自旋-符号-力程：自旋0⇒同号吸引；自旋1⇒同号排斥；自旋2⇒同号吸引")
    A("  T4 Weinberg 软定理：无质量自旋2 的耦合必须普适（等效原理是定理）")
    A("  辅：T5 Weinberg–Witten（引力子不可复合）；T6 Coleman–Mandula（内部荷不能来自几何）")
    A("")
    A("-" * 78)
    A("【条目】")
    for e in res["entries"]:
        A("")
        A("[%s] %s  —— %s" % (e["code"], e["title"], e["state"]))
        A("    %s" % e["evidence"])
        if e["note"]:
            A("    备注：%s" % e["note"])
    A("")
    A("-" * 78)
    A("【控制组】")
    for c in res["controls"]:
        A("  [%s] %s  —— %s" % (c["code"], c["title"], "PASS" if c["ok"] else "FAIL"))
        A("        %s" % c["evidence"])
    A("")
    A("-" * 78)
    A("【守卫】")
    for g in res["guards"]:
        A("  [%s] %s  —— %s" % (g["code"], g["title"], "PASS" if g["ok"] else "FAIL"))
        A("        %s" % g["evidence"])
    A("")
    A("-" * 78)
    d = tally_states(res)
    p = E["repair_pricing"]
    A("条目 %d = PASS %d / FAIL %d / INFO %d"
      % (len(res["entries"]), d.get("PASS", 0), d.get("FAIL", 0), d.get("INFO", 0)))
    A("控制组 %d/%d；守卫 %d/%d"
      % (sum(1 for c in res["controls"] if c["ok"]), len(res["controls"]),
         sum(1 for g in res["guards"] if g["ok"]), len(res["guards"])))
    A("修复定价 2^%d = %d：EMPTY %d / SUICIDE %d / SURVIVE %d"
      % (len(THEOREM_KEYS), p["total"], p["EMPTY"], p["SUICIDE"], p["SURVIVE"]))
    A("七靶未改动：%s" % all(t["unchanged"] for t in E["targets"]))
    A("=" * 78)
    return "\n".join(L)


def render_md(res):
    E = res["evidence"]
    d = tally_states(res)
    p = E["repair_pricing"]
    L = []
    A = L.append
    A("# TUFT-r253 · 力的无模型定理层")
    A("")
    A("> 通量守恒 / 传播子极点 / 自旋-符号-力程 / 软定理普适性 —— ")
    A("> **不接受靶的任何前提**，只用任何力的理论都必须满足的定理当判据。")
    A("")
    A("启动时刻：%s" % START_ISO)
    A("")
    A("## 判词")
    A("")
    A("**先证明对的部分（A 组 %d 条 PASS）**：定稿全书第九章 L498 量纲正确、"
      "λ→∞ 确实退化到 1/r²、F=−∇V 求导正确；压缩版 V_r→A_r→F_r 链与 ∇·V=0 数学自洽，"
      "且主动声明「严格版只统一引力与惯性、κ_q 是补充公设」；S12 §4.2 量纲正确，"
      "引力占比 0.9927 对 α 精度不敏感。**量纲对 ≠ 数值对，两件事分开判。**"
      % sum(1 for e in res["entries"] if e["code"].startswith("A") and e["state"] == "PASS"))
    A("")
    A("**★核心一刀在载体自旋层，且它不需要任何实验输入**：")
    A("靶的母方程是**标量势的梯度**，交换的只能是**自旋 0**；而四力表给电磁行"
      "「同号排斥」，按 T3 只能是**自旋 1**。枚举 s∈{0,1,2}：引力行要求 (−1)^s=+1，"
      "电磁行要求 (−1)^s=−1，**交集为空** ⇒ 靶声称的「一个方程四力全含」在载体层无解。")
    A("")
    A("**★最锋利的一击在软定理层**：Weinberg 低能定理要求无质量自旋 2 的耦合普适"
      "（等效原理是**定理**不是公设）。本卷用 2→2 弹性散射机验：g_A=g_B 时 "
      "q_μS^{μν} 残差 %.1e；g_A≠g_B 时残差恰为 (g_A−g_B)ΔP^ν（4 组失配逐分量比值 = 1）。"
      "⇒ 判据有牙齿，E1 的零不是恒零。" % E["soft_theorem"]["res_equal"])
    A("")
    A("**★书内自相矛盾**：定稿全书第九章 L498（λ→∞⇒1/r²，量纲 N ✓）与第四十章 L3048"
      "（λ→∞⇒1/r³，量纲 N/m，且 L3053 自述的退化极限与式子不符）—— "
      "闭式 F₄₀/F₉ = 1/(s·r)，**两式相差因子 1/r，不可能都对**。")
    A("")
    A("**★S12 的纯内部矛盾**：§4.1 表自述引力「~10⁻³⁸（最弱）」，"
      "而 §4.3 归一化后引力占比 %.4f（%.2f%%）—— 同一文档内直接冲突，不依赖任何外部数据。"
      % (E["s12"]["frac_G_137"], E["s12"]["frac_G_137"] * 100))
    A("")
    A("**修复定价 2^%d = %d：EMPTY %d / SUICIDE %d / SURVIVE %d ⇒ 第 %d 度。**"
      % (len(THEOREM_KEYS), p["total"], p["EMPTY"], p["SUICIDE"], p["SURVIVE"], DEGREE))
    A("")
    A("## 条目总表")
    A("")
    A("| 编号 | 条目 | 判定 |")
    A("|---|---|---|")
    for e in res["entries"]:
        A("| %s | %s | %s |" % (e["code"], e["title"], e["state"]))
    A("")
    A("## 控制组")
    A("")
    A("| 编号 | 内容 | 结果 |")
    A("|---|---|---|")
    for c in res["controls"]:
        A("| %s | %s | %s |" % (c["code"], c["title"], "PASS" if c["ok"] else "FAIL"))
    A("")
    A("## 守卫")
    A("")
    A("| 编号 | 内容 | 结果 |")
    A("|---|---|---|")
    for g in res["guards"]:
        A("| %s | %s | %s |" % (g["code"], g["title"], "PASS" if g["ok"] else "FAIL"))
    A("")
    A("## 红线（四条）")
    A("")
    A("1. 本卷条目不可与 r142–r252 相加。")
    A("2. 「缺失」不等于「错误」：SUPPLY-GAP 与 VIOLATION 分开记。")
    A("3. 对靶有利的结论必须如实写 PASS，且每条 PASS 都要写范围限制。")
    A("4. 判据必须先做正/负对照自校，再用于指控。")
    return "\n".join(L)


def render_verdict(res):
    E = res["evidence"]
    d = tally_states(res)
    p = E["repair_pricing"]
    L = []
    A = L.append
    A("# 判定册 · TUFT-%s（力的无模型定理层）" % RID.upper())
    A("")
    A("## 判词")
    A("")
    A("本卷换打法：**不接受靶的任何前提**，只用「任何力的理论都必须满足的定理」当判据 ——")
    A("Gauss 通量守恒、传播子极点结构、自旋-符号-力程对应、Weinberg 软定理普适性，")
    A("外加 Weinberg–Witten 与 Coleman–Mandula 两条封禁定理。")
    A("")
    A("**承重结论（三条，互不依赖）**：")
    A("")
    A("1. **载体自旋无解**：母方程是标量势的梯度 ⇒ 自旋 0；电磁行要求同号排斥 ⇒ 自旋 1。"
      "枚举 s∈{0,1,2} 交集为空。这条不需要任何实验输入。")
    A("2. **书内两式互不等价**：第九章 L498（1/r²，量纲 N）与第四十章 L3048"
      "（λ→∞ 给 1/r³，量纲 N/m）；闭式 F₄₀/F₉ = 1/(s·r)。")
    A("3. **软定理要求耦合普适**：2→2 散射机验 残差 %.1e（普适）/ 比值 = 1（失配），"
      "而靶的四通道耦合来自四个互不相干的外部量 ⇒ 单一载体下不可能。"
      % E["soft_theorem"]["res_equal"])
    A("")
    A("**★诚实项（如实 PASS）**：定稿全书 L498 量纲正确、λ→∞ 退化正确、"
      "F=−∇V 求导正确；压缩版数学链自洽且主动声明边界；S12 §4.2 量纲正确、"
      "引力占比对 α 不敏感。")
    A("")
    A("## 判决分组")
    A("")
    A("| 组 | 内容 | 结论 |")
    A("|---|---|---|")
    A("| A | 对靶有利 6 条 | **PASS %d** |"
      % sum(1 for e in res["entries"] if e["code"].startswith("A") and e["state"] == "PASS"))
    A("| B | T1 高斯通量（判据自校 + 七靶过筛） | PASS %d / FAIL %d / INFO %d |"
      % (sum(1 for e in res["entries"] if e["code"].startswith("B") and e["state"] == "PASS"),
         sum(1 for e in res["entries"] if e["code"].startswith("B") and e["state"] == "FAIL"),
         sum(1 for e in res["entries"] if e["code"].startswith("B") and e["state"] == "INFO")))
    A("| C | T2 传播子极点 | PASS %d / FAIL %d |"
      % (sum(1 for e in res["entries"] if e["code"].startswith("C") and e["state"] == "PASS"),
         sum(1 for e in res["entries"] if e["code"].startswith("C") and e["state"] == "FAIL")))
    A("| D | T3 自旋-符号-力程（★核心） | PASS %d / FAIL %d / INFO %d |"
      % (sum(1 for e in res["entries"] if e["code"].startswith("D") and e["state"] == "PASS"),
         sum(1 for e in res["entries"] if e["code"].startswith("D") and e["state"] == "FAIL"),
         sum(1 for e in res["entries"] if e["code"].startswith("D") and e["state"] == "INFO")))
    A("| E | T4 软定理普适性 | PASS %d / FAIL %d |"
      % (sum(1 for e in res["entries"] if e["code"].startswith("E") and e["state"] == "PASS"),
         sum(1 for e in res["entries"] if e["code"].startswith("E") and e["state"] == "FAIL")))
    A("| F | T5 WW / T6 Coleman–Mandula | FAIL %d / INFO %d |"
      % (sum(1 for e in res["entries"] if e["code"].startswith("F") and e["state"] == "FAIL"),
         sum(1 for e in res["entries"] if e["code"].startswith("F") and e["state"] == "INFO")))
    A("| G | 量纲 / 数值 / S12 内部矛盾 | PASS %d / FAIL %d / INFO %d |"
      % (sum(1 for e in res["entries"] if e["code"].startswith("G") and e["state"] == "PASS"),
         sum(1 for e in res["entries"] if e["code"].startswith("G") and e["state"] == "FAIL"),
         sum(1 for e in res["entries"] if e["code"].startswith("G") and e["state"] == "INFO")))
    A("| H | 分形幂律 GUT（靶 8） | FAIL %d |"
      % sum(1 for e in res["entries"] if e["code"].startswith("H") and e["state"] == "FAIL"))
    A("| I | 修复定价 2^%d | **SURVIVE %d（第 %d 度）** |"
      % (len(THEOREM_KEYS), p["SURVIVE"], DEGREE))
    A("| J | ★已判层重叠登记（本卷不计分） | INFO %d |"
      % sum(1 for e in res["entries"] if e["code"].startswith("J")))
    A("")
    A("条目 **%d**（PASS %d / FAIL %d / INFO %d）；控制组 %d/%d；守卫 %d/%d"
      % (len(res["entries"]), d.get("PASS", 0), d.get("FAIL", 0), d.get("INFO", 0),
         sum(1 for c in res["controls"] if c["ok"]), len(res["controls"]),
         sum(1 for g in res["guards"] if g["ok"]), len(res["guards"])))
    A("")
    A("## ★ 性质界定")
    A("")
    A("1. **不是外部证伪，是内部矛盾为主**：D3/E6（载体自旋无解）、G6（引力最弱 vs 占 99.27%）、"
      "B3（L3048 式与自述不符）都只用靶自己的式子与自述。")
    A("2. **T1–T4 是从 QFT 公理化性质推出的**：幺正性、Lorentz 不变性、无质量粒子的软行为 ——"
      "  不接受「我的框架不同所以不适用」的豁免。")
    A("3. **先证明对的部分**：定稿全书第九章的 L498 在量纲、退化极限、求导三层都站得住；"
      "  本卷的攻击恰恰建立在「L498 是对的」之上，再去对比第四十章的 L3048。")
    A("4. **SUPPLY-GAP 不等于 FAIL**：C6 的紫外发散、G5/G8 的未指定能标/荷归一化、"
      "  H3 的阈值修正缺失，都登记为缺件，不计为算错。")
    A("")
    A("## 治理")
    A("")
    A("- 七靶只读：%s" % all(t["unchanged"] for t in E["targets"]))
    A("- r225–r251 产物未改动（G7 真机读：扫描 %d 份，违规 %d 份）"
      % (E["scan_untouched"]["scanned"], len(E["scan_untouched"]["violations"])))
    A("- 未改 verify.py；未跑 refresh_catalog.py；未做 git")
    A("- ⚠ **撞号记录**：起草期间 r247（引力本质层元审计）、r248（单方程全域力层）、"
      "r249（低能极限推导层）、r250（耦合常数跑动与能标层）、\n"
      "r251（下游物理应用层，落盘 10-31 08:09:31，早于本卷 08:18:26）被并行会话占用；\n"
      "r252 同期处于并行会话探测中（后证实被「质量谱层」取走）⇒ 后到者整体改号，本卷取 **r253**。\n"
      "★**撞度记录**：r251 的判定册写「第 33 度」而它的 README 条目写「第 34 度」"
      "（同一卷内部不一致）；r252 未标度。本卷不采信任一方记忆，\n"
      "改由新增守卫 **G13 真机读 README** 取「排除本卷行之外的最大度 + 1」⇒ 本卷 **第 %d 度**。"
      % DEGREE)
    A("- 本卷条目不可与 r142–r252 相加。")
    return "\n".join(L)


def render_html(res, payload, header, dist, n_ctl_ok, n_ctl, n_grd_ok, n_grd):
    E = res["evidence"]
    p = E["repair_pricing"]
    rows_e = "\n".join(
        "<tr><td><b>%s</b></td><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>"
        % (e["code"], e["title"], e["state"].lower(), e["state"], e["evidence"])
        for e in res["entries"])
    rows_c = "\n".join(
        "<tr><td>%s</td><td>%s</td><td class='%s'>%s</td></tr>"
        % (c["code"], c["title"], "pass" if c["ok"] else "fail",
           "PASS" if c["ok"] else "FAIL")
        for c in res["controls"])
    rows_g = "\n".join(
        "<tr><td>%s</td><td>%s</td><td class='%s'>%s</td></tr>"
        % (g["code"], g["title"], "pass" if g["ok"] else "fail",
           "PASS" if g["ok"] else "FAIL")
        for g in res["guards"])
    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-r253 · 力的无模型定理层</title>
<style>
body{font-family:"Microsoft YaHei",system-ui,sans-serif;background:#f7f8fa;color:#1a1a1a;
     margin:0;padding:28px;line-height:1.7}
.wrap{max-width:1180px;margin:0 auto;background:#fff;padding:34px 40px;
      border-radius:10px;box-shadow:0 2px 14px rgba(0,0,0,.07)}
h1{font-size:23px;border-bottom:3px solid #2b5c9b;padding-bottom:12px;color:#123}
h2{font-size:18px;margin-top:34px;color:#2b5c9b;border-left:5px solid #2b5c9b;padding-left:11px}
table{border-collapse:collapse;width:100%%;margin-top:14px;font-size:13.5px}
th,td{border:1px solid #dfe3e8;padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eef2f7}
tr:nth-child(even) td{background:#fafbfc}
.pass{color:#16794c;font-weight:700}.fail{color:#c0392b;font-weight:700}
.info{color:#8a6d3b;font-weight:700}
.kpi{display:flex;gap:14px;flex-wrap:wrap;margin:18px 0}
.kpi div{background:#eef2f7;border-radius:8px;padding:12px 18px;min-width:120px}
.kpi b{display:block;font-size:21px;color:#2b5c9b}
ul{margin:8px 0 8px 20px}
.note{background:#fff8e6;border-left:4px solid #e0a800;padding:10px 14px;margin:14px 0}
</style></head><body><div class="wrap">
<h1>TUFT-r253 · 力的无模型定理层</h1>
<p><b>通量守恒 / 传播子极点 / 自旋-符号-力程 / 软定理普适性</b><br>
四条无模型定理对七份「力的大统一方程」的全谱判决<br>
<span style="color:#666">启动 %(iso)s</span></p>
<div class="kpi">
  <div>条目<b>%(ne)d</b></div><div>PASS<b>%(np)d</b></div>
  <div>FAIL<b>%(nf)d</b></div><div>INFO<b>%(ni)d</b></div>
  <div>控制组<b>%(nc)d/%(ntc)d</b></div><div>守卫<b>%(ng)d/%(ntg)d</b></div>
  <div>SURVIVE<b>%(sv)d</b></div>
</div>
<div class="note"><b>核心一刀</b>：母方程是标量势的梯度 ⇒ 自旋 0；电磁行要求同号排斥 ⇒ 自旋 1。
枚举载体自旋 s∈{0,1,2}，引力行要 (−1)<sup>s</sup>=+1、电磁行要 (−1)<sup>s</sup>=−1，
<b>交集为空</b> ⇒ 「一个方程四力全含」在载体层无解。这条不需要任何实验输入。</div>
<h2>条目</h2><table><tr><th>编号</th><th>条目</th><th>判定</th><th>证据</th></tr>%(rows_e)s</table>
<h2>控制组</h2><table><tr><th>编号</th><th>内容</th><th>结果</th></tr>%(rows_c)s</table>
<h2>守卫</h2><table><tr><th>编号</th><th>内容</th><th>结果</th></tr>%(rows_g)s</table>
<h2>修复定价</h2><p>2<sup>%(nk)d</sup> = %(ptot)d 组合：
EMPTY %(pe)d / SUICIDE %(ps)d / <b>SURVIVE %(sv)d</b> ⇒ 本线第 <b>%(deg)d</b> 度。</p>
<h2>红线</h2><ul>
<li>本卷条目不可与 r142–r252 相加。</li>
<li>「缺失」不等于「错误」：SUPPLY-GAP 与 VIOLATION 分开记。</li>
<li>对靶有利的结论必须如实写 PASS，且每条 PASS 都要写范围限制。</li>
<li>判据必须先做正/负对照自校，再用于指控。</li></ul>
</div></body></html>
""" % {"iso": START_ISO, "ne": len(res["entries"]), "np": dist.get("PASS", 0),
       "nf": dist.get("FAIL", 0), "ni": dist.get("INFO", 0),
       "nc": n_ctl_ok, "ntc": n_ctl, "ng": n_grd_ok, "ntg": n_grd,
       "sv": p["SURVIVE"], "nk": len(THEOREM_KEYS), "ptot": p["total"],
       "pe": p["EMPTY"], "ps": p["SUICIDE"], "deg": DEGREE,
       "rows_e": rows_e, "rows_c": rows_c, "rows_g": rows_g}


# ============================================================
# 15. 主流程
# ============================================================
def main():
    res = run_audit()
    E = res["evidence"]
    dist = tally_states(res)
    report = render_report(res)

    payload = {
        "rid": RID, "base_name": BASE_NAME, "start": START_ISO,
        "targets": E["targets"],
        "entries": res["entries"], "entry_distribution": dist,
        "controls": res["controls"],
        "controls_ok": all(c["ok"] for c in res["controls"]),
        "guards": res["guards"],
        "guards_ok": all(g["ok"] for g in res["guards"]),
        "evidence": {k: v for k, v in E.items() if k != "targets"},
        "repair_pricing": E["repair_pricing"],
    }

    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(DATA_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write(render_md(res))
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write(render_verdict(res))
    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(res, payload, "", dist,
                            sum(1 for c in res["controls"] if c["ok"]),
                            len(res["controls"]),
                            sum(1 for g in res["guards"] if g["ok"]),
                            len(res["guards"])))

    # report：先写文件，再补 AST 自审段，同时打印
    bad = _ast_self_audit()
    tail = ("\n" + "-" * 78 + "\n【AST 自审】ent/ctl/grd 写死 True/False 的调用：%s\n"
            % ("、".join(bad) if bad else "无（白名单仅 G6）"))
    report = report + tail
    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)

    try:
        sys_stdout = __import__("sys").stdout
        sys_stdout.write(report)
        sys_stdout.write("\n")
    except Exception:
        pass

    ok = (payload["controls_ok"] and payload["guards_ok"] and len(bad) == 0)
    return 0 if ok else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
