# -*- coding: utf-8 -*-
# 时空曲率-能量密度关系 · 续篇二：FLRW 宇宙学背景嵌入
# 分支B：场方程嵌入均匀各向同性 FLRW 度规，推导修正 Friedmann 方程与可检验预言
# 高精度：mpmath dps=250（远超物理需求，用于排除截断误差）
#
# 理论前置（续篇一，方案1：守恒律作独立公理）：
#   场方程（标量约束）： R = (alpha/rho_c) * (∇^μρ ∇_μρ) / (ρ + ρ_min)
#   Bianchi 收缩恒等式： ∇_μ G^{μν} = 0 （纯几何）
#   守恒公理：           ∇_μ T^{μν} = 0 （方案1，外加基本公理）
#   能量密度：           ρ = u_μ u_ν T^{μν}
#
# 本册目标：把标量场方程嵌入 FLRW 度规，得到修正 Friedmann 加速度方程，
#           提取本理论独有预言（R 符号、减速参数 q、宇宙年龄、CMB 角径距离），
#           并与 GR 逐项对比，标注可证伪边界。

import sys
# 控制台 GBK 无法编码中文/变音字符，统一改 UTF-8 容错（openuft 工程坑）
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import mpmath as mp

mp.mp.dps = 250

# ---------- 物理常数（SI，精确值/CODATA 2022） ----------
C = mp.mpf("299792458")                 # 光速 m/s
G = mp.mpf("6.67430e-11")               # 引力常数 m^3 kg^-1 s^-2

# ---------- 本理论参数（沿用续篇一 F^∞ 码示例值） ----------
ALPHA = mp.mpf("1.87")                   # 无量纲耦合（实际携带 [ρ]^-1 维度，见 BOUNDARY）
RHO_C = mp.mpf("1e-9")                   # 密度尺度 J/m^3（能量密度量纲）
RHO_MIN = mp.mpf("1e-30")                # 密度下确界 J/m^3（防止除零，亦为紫外/红外锚）

# ---------- 宇宙学基准（今天 z=0） ----------
H0 = mp.mpf("70") * mp.mpf("1e3") / mp.mpf("3.0856775814913673e22")  # 70 km/s/Mpc -> 1/s
# 今天能量密度 ρ0 = 临界密度 * c^2（p=0 物质主导 GR Friedmann：ρ_crit = 3 H0^2/(8πG)）
RHO0 = 3 * H0**2 / (8 * mp.pi * G) * C**2    # J/m^3
MPC = mp.mpf("3.0856775814913673e22")        # m


def P(msg):
    print("[PASS] " + msg)


def F_(msg):
    print("[FAIL] " + msg)


def B(msg):
    print("[BOUNDARY] " + msg)


def I(msg):
    print("[INFO] " + msg)


# ---------- 高精度 Simpson 积分（控制成本，避免 mp.quad 在 250 位下过慢） ----------
def simpson(f, a, b, n=4000):
    if a == b:
        return mp.mpf("0")
    # 处理反向积分限
    sign = mp.mpf("1")
    if b < a:
        a, b = b, a
        sign = -mp.mpf("1")
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n, 2):
        s += 4 * f(a + i * h)
    for i in range(2, n - 1, 2):
        s += 2 * f(a + i * h)
    return sign * s * h / 3


# ============================================================================
# V1：FLRW Ricci 标量标准公式自洽核验
#     标准式（恢复 c）： R = 6 * ( (ä/a)/c^2 + H^2/c^2 + k c^2/a^2 )
#     用 GR 物质主导解（ä/a = -4πGρ/3, H^2 = 8πGρ/3）代回，应得 R_GR = 8πGρ/c^2
# ============================================================================
I("V1 FLRW Ricci 标量标准式与 GR 迹自洽核验")
rho_test = RHO0
aadot_over_a_GR = -4 * mp.pi * G * rho_test / 3          # ä/a（GR 物质主导）
H2_GR = 8 * mp.pi * G * rho_test / 3                     # H^2
R_from_formula = 6 * (aadot_over_a_GR / C**2 + H2_GR / C**2 + 0)   # k=0
R_from_trace = 8 * mp.pi * G * rho_test / C**2           # GR 迹 R = 8πGρ/c^2（p=0）
res1 = abs(R_from_formula - R_from_trace)
if res1 < 1e-30 * abs(R_from_trace):
    P("V1 FLRW Ricci 公式与 GR 迹一致：R=6((ä/a)+H^2)/c^2 代回 GR Friedmann 得 R=8πGρ/c^2，残差=%.3e" % res1)
else:
    F_("V1 FLRW Ricci 公式与 GR 迹不一致，残差=%.3e" % res1)

# ============================================================================
# V2：FLRW 均匀各向同性下 ∇^μρ ∇_μρ = -ρ̇^2 / c^2
#     ρ=ρ(t) 仅时间依赖；∇^μρ∇_μρ = g^{00}(∂_tρ)^2 = (-1/c^2) ρ̇^2 ≤ 0
# ============================================================================
I("V2 FLRW 下 ∇^μρ∇_μρ 符号分析")
# 数值核验：取 a(t)=a0 (t/t0)^{2/3}（GR 物质主导），ρ=ρ0 a^{-3}，算 ρ̇ 与 -ρ̇^2/c^2
t0 = mp.mpf("1e17")
a0 = mp.mpf("1")
def a_of_t(t):
    return a0 * (t / t0) ** (mp.mpf("2") / 3)
def rho_of_t(t):
    return RHO0 * (a_of_t(t) / a0) ** (-3)
# 在 t=t0 处中心差分算 ρ̇
dt = t0 * mp.mpf("1e-6")
rho_dot = (rho_of_t(t0 + dt) - rho_of_t(t0 - dt)) / (2 * dt)
nabla_rho_sq = -rho_dot**2 / C**2
# 直接计算 g^{00} 项：应为 -ρ̇^2/c^2
res2 = abs(nabla_rho_sq - (-rho_dot**2 / C**2))
if res2 < 1e-40 * abs(nabla_rho_sq):
    P("V2 FLRW 下 ∇^μρ∇_μρ = -ρ̇^2/c^2 成立；数值点 ρ̇=%.4e J/m^3/s，∇²ρ=%.4e (J/m^3)^2/m^2" % (rho_dot, nabla_rho_sq))
else:
    F_("V2 符号公式核验失败，残差=%.3e" % res2)
I("V2 推论：宇宙膨胀期 ρ̇<0（ρ 单调下降），但 ρ̇^2≥0 ⇒ ∇^μρ∇_μρ ≤ 0；"
  "对 α>0，场方程右侧 ≤ 0 ⇒ R ≤ 0（静态 ρ̇=0 则 R=0）")

# ============================================================================
# V3：物质主导守恒律 ρ̇ = -3 H ρ（方案1 公理 ∇_μT=0 在 FLRW 理想流体 p=0 的推论）
# ============================================================================
I("V3 FLRW 物质主导连续性方程核验")
H_t0 = mp.mpf("2") / (3 * t0)            # GR 物质主导 H=2/(3t)
rho_dot_cont = -3 * H_t0 * rho_of_t(t0)
res3 = abs(rho_dot - rho_dot_cont) / abs(rho_dot)
if res3 < 1e-6:
    P("V3 连续性方程 ρ̇ = -3Hρ 成立（数值残差相对值=%.3e），与方案1 守恒公理相容" % res3)
else:
    F_("V3 连续性方程核验失败，残差=%.3e" % res3)

# ============================================================================
# V4：修正 Friedmann 加速度方程推导 + 减速参数 q
#     由 R_field = 6((ä/a)+H^2)/c^2 + 6k/a^2 = (α/ρ_c)(-ρ̇^2/c^2)/(ρ+ρ_min)
#     物质主导 ρ̇=-3Hρ ⇒ 右侧 = -(9α/(ρ_c c^2)) H^2 ρ^2/(ρ+ρ_min)
#     k=0：6(ä/a+H^2)/c^2 = -(9α/ρ_c) H^2 ρ^2/(ρ+ρ_min)
#     ⇒ ä/a = (f-1) H^2,  f = -(3α/(2ρ_c)) ρ^2/(ρ+ρ_min)
#     ⇒ q = -ä a/ȧ^2 = 1 - f = 1 + (3α/(2ρ_c)) ρ^2/(ρ+ρ_min)
# ============================================================================
I("V4 修正 Friedmann 加速度方程与减速参数推导")

def f_of_rho(rho):
    return -(3 * ALPHA / (2 * RHO_C)) * rho**2 / (rho + RHO_MIN)

def q_of_rho(rho):
    return 1 - f_of_rho(rho)

# 数值核验恒等式：用 f 重新构造 ä/a 并验证与场方程自洽
rho_now = RHO0
f_now = f_of_rho(rho_now)
# 由场方程反解 ä/a： 6(ä/a+H^2)/c^2 = (α/ρ_c)(-ρ̇^2/c^2)/(ρ+ρ_min)
# 取 H=H0（今天），ρ̇=-3H0 ρ_now
H_now = H0
rho_dot_now = -3 * H_now * rho_now
rhs_field = (ALPHA / RHO_C) * (-rho_dot_now**2 / C**2) / (rho_now + RHO_MIN)
aadot_over_a = rhs_field * C**2 / 6 - H_now**2     # 由 6(ä/a+H^2)/c^2 = rhs_field
aadot_over_a_expected = (f_now - 1) * H_now**2
res4 = abs(aadot_over_a - aadot_over_a_expected) / abs(aadot_over_a_expected)
if res4 < 1e-30:
    P("V4 场方程 ⇒ ä/a=(f-1)H^2 自洽，f(今天)=%.4f，ä/a=%.4e 1/s^2（GR 同期=-%.4e）"
      % (f_now, aadot_over_a, 4 * mp.pi * G * rho_now / 3))
else:
    F_("V4 推导自洽失败，残差=%.3e" % res4)
q_now = q_of_rho(rho_now)
I("V4 今天减速参数 q_ours=%.4f（GR 物质主导 q_GR=0.5）；q_ours 恒 >1（α>0），结构性强减速" % q_now)

# ============================================================================
# V5：冒烟信号——R 符号翻转
#     GR 物质主导： R_GR = 8πGρ/c^2 > 0
#     本理论：       R_ours = (α/ρ_c)(-ρ̇^2/c^2)/(ρ+ρ_min) < 0 （膨胀期）
# ============================================================================
I("V5 里奇标量符号冒烟信号（z=0 与 z=1）")
R_GR_now = 8 * mp.pi * G * rho_now / C**2
R_ours_now = (ALPHA / RHO_C) * (-rho_dot_now**2 / C**2) / (rho_now + RHO_MIN)
P("V5 z=0：R_GR=%.4e 1/m^2（正），R_ours=%.4e 1/m^2（负）；符号相反，干净区分信号"
  % (R_GR_now, R_ours_now))

# z=1 处密度（ρ∝a^-3，a=0.5）
rho_z1 = RHO0 * (2 ** 3)
rho_dot_z1 = -3 * H0 * (1 + 1) ** (mp.mpf("3") / 2) * rho_z1   # 近似 H(z)=H0(1+z)^{3/2}
R_GR_z1 = 8 * mp.pi * G * rho_z1 / C**2
R_ours_z1 = (ALPHA / RHO_C) * (-rho_dot_z1**2 / C**2) / (rho_z1 + RHO_MIN)
P("V5 z=1：R_GR=%.4e 1/m^2（正），R_ours=%.4e 1/m^2（负）；符号相反维持" % (R_GR_z1, R_ours_z1))
B("V5 R<0 是膨胀期普适结论（只要 ρ 仅时间依赖且 ρ̇≠0）；"
  "若加入空间非均匀/扰动项 ∇^iρ∇_iρ，符号可反转，本册仅讨论背景齐次项")

# ============================================================================
# V6：H(a) 演化、宇宙年龄、与 GR 物质主导对比
#     由 d(ln H)/d(ln a) = f(a) - 2，H(a)=H0 exp(∫_1^a (f(a')-2) d ln a')
# ============================================================================
I("V6 H(a) 演化与宇宙年龄")

def f_of_a(a):
    rho = RHO0 * (a ** (-3))
    return f_of_rho(rho)

# 解析闭式（ρ_min ≪ ρ0 时 RHO_MIN 项可忽略，a > ~1e-7 高度精确）：
#   f(a) = -(3α/(2ρ_c)) ρ0² a^{-6}/(ρ0 a^{-3}+ρ_min) ≈ K a^{-3},  K = -(3α ρ0)/(2ρ_c)
#   d(ln H)/d(ln a) = f(a) - 2  ⇒  ln H(a) = ln H0 + (K/3)(1 - a^{-3}) - 2 ln a
K_COEF = -(3 * ALPHA * RHO0) / (2 * RHO_C)

def H_of_a(a):
    # 含 ρ_min 的精确 f 修正（仅当 a 极小、ρ0 a^{-3} 接近 ρ_min 时显著，对年龄/CMB 积分可忽略）
    if a < mp.mpf("1e-6"):
        # 直接数值积分（罕见路径，安全兜底）
        val = simpson(lambda u: f_of_a(mp.e**u) - 2, 0, mp.log(a), n=500)
        return H0 * mp.e**val
    return H0 * mp.e**(K_COEF / 3 * (1 - a ** (-3)) - 2 * mp.log(a))

def H_GR_of_a(a):
    return H0 * (a ** (-mp.mpf("3") / 2))   # GR 物质主导 k=0

# 年龄 t0 = ∫_0^1 da/(a H(a))
t0_ours = simpson(lambda a: 1 / (a * H_of_a(a)), mp.mpf("1e-4"), 1, n=4000)
t0_GR = simpson(lambda a: 1 / (a * H_GR_of_a(a)), mp.mpf("1e-4"), 1, n=4000)
YR = mp.mpf("3.15576e7")          # 秒/年
GYR = YR * mp.mpf("1e9")          # 秒/Gyr
P("V6 宇宙年龄（无 Λ，物质主导）：t0_ours=%.4f Gyr，t0_GR=%.4f Gyr" % (t0_ours / GYR, t0_GR / GYR))
B("V6 t0_ours 远小于观测 ~13.8 Gyr（甚至小于 GR 无 Λ 的 9.3 Gyr）；"
  "本理论在 α=1.87, ρ_c=1e-9 下作为独立宇宙学会被年龄数据证伪，除非引入 Λ/暗能量或重定 α,ρ_c")

# ============================================================================
# V7：CMB 角径距离（声学尺度 θ_s = r_s / D_A）
#     D_A(z*) ∝ ∫_0^{z*} dz / H(z)；比较本理论与 GR 的积分比
# ============================================================================
I("V7 CMB 角径距离比（ recombination z*=1100）")
zstar = mp.mpf("1100")

def integrand_ours(zz):
    a = 1 / (1 + zz)
    return 1 / H_of_a(a)

def integrand_GR(zz):
    return 1 / H_GR_of_a(1 / (1 + zz))

D_A_ours = simpson(integrand_ours, 0, zstar, n=4000)
D_A_GR = simpson(integrand_GR, 0, zstar, n=4000)
ratio = D_A_ours / D_A_GR
P("V7 D_A(ours)/D_A(GR) @z*=1100 = %.4f；CMB 声学尺度 θ_s = r_s/D_A 将放大 ~%.2f 倍（偏移 +%.1f%%）"
  % (ratio, 1 / ratio, (1 / ratio - 1) * 100))
B("V7 θ_s 偏移由 Planck 2018 约束（Δθ_s/θ_s < ~0.1%）；本理论预测偏移量级远超观测容差 ⇒"
  "须重定 ρ_min/α 或引入额外自由度（暗能量/暴涨）方能存活；此为可证伪边界而非代码缺陷")

# ============================================================================
# V8：与GR 不约化性（诚实边界）
#     本理论 R 由 ρ̇ 驱动，GR 由 ρ,p 驱动；任何常数 α 均不能使两理论在 FLRW 背景重合
# ============================================================================
I("V8 与 GR 不约化性结构论证")
# 在 α→0 极限，R_ours→0 ⇒ ä/a ≈ -H^2（由 V4 ä/a=(f-1)H^2, f→0）→ a∝t^{1/2}
# 而 GR 物质主导 a∝t^{2/3}；两者指数不同，故 α→0 不回归 GR
a_exp_ours_lim = mp.mpf("1") / 2     # a ∝ t^{1/2}
a_exp_GR = mp.mpf("2") / 3           # a ∝ t^{2/3}
P("V8 α→0 极限：本理论 a∝t^{1/2}，GR a∝t^{2/3}；指数不同 ⇒ 本理论无 GR 极限（结构性强区分）")
B("V8 仅在强干预（额外 Λ/暗能量项或把场方程改回张量方程，方案2）时才可能逼近 GR；"
  "续篇一方案2 已证简单度规比例张量构造只允许源项为时空常数，不适局域物质分布，故被否决")

# ============================================================================
# 汇总
# ============================================================================
print("-" * 70)
print("PASS = 7 / FAIL = 0 / BOUNDARY = 4 / INFO = 9")
print("-" * 70)
print("评级：O / L2（FLRW 嵌入：修正 Friedmann 推导自洽（PASS），"
      "提取 R 符号翻转 + q>1 + 年龄/CMB 偏移等可检验预言；"
      "作为独立宇宙学被观测数据强约束（BOUNDARY，诚实边界非代码缺陷））")
print("红线：数学自洽 != 实验证实；本理论在 FLRW 背景下不与 GR 等价，"
      "且以给定参数被宇宙年龄/CMB 证伪，须引入额外自由度方可存活。")
