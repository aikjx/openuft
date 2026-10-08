# -*- coding: utf-8 -*-
"""
S03-V18.13
来稿：GAQ-UFT V18「电荷作为拓扑通量不变量；正负电荷对应场线左右手缠绕」（§1-§7）

编号说明：S03 内部当日已用至 V18_10（分支三·孤子拓扑相变守恒律），
          本册顺延为 V18_13；条目前缀统一为 V13-*。
          （V18_11 同日已被《分支 B-1 · 几何 anholonomy》占用、V18_12 已被《β 衰变本体审计》占用，
            按「后到者改号不覆盖他人」顺延；V13-* 前缀为该册所用，本册不得复用。）

定位（重要）：本册不是新开方向，而是执行 S03-V18.6 §11 遗留的唯一未执行项——
    「分支二 · 电荷作为拓扑通量不变量（半阻塞，待执行）」。
    V18.6 预判其量子化需 hbar（被 V18.3 锁死）；本册给出完整机器验证与最终裁定。
    同时裁定来稿 §7 的三条候选分支（β 衰变 / 夸克色荷 / 中微子零通量扭结）：
    三条在库内均已有既有产物覆盖，按「不重复造轮子」不得新开。

任务：(A) 先校准工具（Stokes / Gauss / 磁通量子 / Ps 衰变率），再判来稿；
      (B) 对来稿 §1-§6 做自洽性、量纲与可否证性审计；
      (C) 对 §7 三条分支做收口裁定并给出体系能力边界增补。

纯标准库（math / cmath / decimal / sys / os / io），Python 3.8+
红线：本册全部为自洽性/可否证性裁定与标准物理事实的独立复算，
      不含任何对 GAQ 主张的正面支持证据。所有 PASS 仅指
      「该式在机器精度下自洽」或「外部事实被独立复算」。

输出：07_计算复现/运行记录/S03_V18_13_电荷拓扑通量不变量_审计与分支收口报告.txt
"""

import sys
import os
import io
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PI = math.pi

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))      # 07_计算复现/源码
CALC = os.path.dirname(HERE)                            # 07_计算复现
SYSROOT = os.path.dirname(CALC)                         # S03_GAQ几何原子与作用量子
LOGDIR = os.path.join(CALC, "运行记录")
REPORT_NAME = "S03_V18_13_电荷拓扑通量不变量_审计与分支收口报告.txt"

# ---------------------------------------------------------------------------
# 输出器（命名纪律：B/I/C/P/F 为输出器，任何推导变量不得占用这些单字母名）
# ---------------------------------------------------------------------------
LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "CORRECTED": 0}
ITEMS = []


def emit(text=""):
    LINES.append(text)


def rec(code, verdict, title):
    COUNTS[verdict] += 1
    ITEMS.append((code, verdict, title))
    emit("[%s] %s  %s" % (verdict, code, title))


def P(code, title):
    rec(code, "PASS", title)


def F(code, title):
    rec(code, "FAIL", title)


def B(code, title):
    rec(code, "BOUNDARY", title)


def I(code, title):
    rec(code, "INFO", title)


def C(code, title):
    rec(code, "CORRECTED", title)


def table(headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for k in range(len(headers)):
            widths[k] = max(widths[k], len(str(r[k])))
    fmt = " | ".join("{:<%d}" % w for w in widths)
    emit("  " + fmt.format(*headers))
    emit("  " + "-" * (sum(widths) + 3 * (len(widths) - 1)))
    for r in rows:
        emit("  " + fmt.format(*[str(x) for x in r]))


CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    return ok


def fx(x, n=6):
    """定点/科学计数格式化（避免 Decimal.quantize 在高位数抛 InvalidOperation）。"""
    try:
        return ("%." + str(n) + "E") % float(x)
    except Exception:
        return str(x)


# ---------------------------------------------------------------------------
# 外部事实基准（CODATA 2018 / PDG；仅作对照，不作拟合）
# ---------------------------------------------------------------------------
E_CH = 1.602176634e-19              # C   元电荷（SI 定义值）
H_PLANCK = 6.62607015e-34           # J s 普朗克常数（SI 定义值）
HBAR = H_PLANCK / (2.0 * PI)        # J s
EPS0 = 8.8541878128e-12             # F/m
MU0 = 1.25663706212e-06             # H/m（2019 后含不确定度，此处取 CODATA 值）
C_LIGHT = 299792458.0               # m/s（定义值）
ALPHA = 7.2973525693e-03            # 精细结构常数
Z0_VAC = 376.730313668              # ohm 真空阻抗
M_E_C2 = 8.1871057769e-14           # J  (0.510998950 MeV)
PHI0_CODATA = 2.067833848e-15       # Wb 磁通量子 h/(2e)

# 正电子偶素（PDG）：p-Ps -> 2gamma，o-Ps -> 3gamma
TAU_PPS_PDG = 1.2519e-10            # s  (125.19 ps)
TAU_OPS_PDG = 1.4205e-07            # s  (142.05 ns)

# ---------------------------------------------------------------------------
# 量纲工具：指数向量 (M, L, T, I)
# ---------------------------------------------------------------------------
D_Q = (0, 0, 1, 1)          # 电荷 I T
D_FLUX = (1, 2, -2, -1)     # 磁通 Wb = M L^2 T^-2 I^-1
D_ENERGY = (1, 2, -2, 0)
D_EPS0 = (-1, -3, 4, 2)     # F/m = I^2 T^4 M^-1 L^-3
D_MU0 = (1, 1, -2, -2)      # H/m
D_Z0 = (1, 2, -3, -2)       # ohm
D_R = (0, 1, 0, 0)
D_T = (0, 0, 1, 0)


def dsub(a, b):
    return tuple(a[k] - b[k] for k in range(4))


def dadd(a, b):
    return tuple(a[k] + b[k] for k in range(4))


def dscale(a, k):
    return tuple(k * x for x in a)


def dname(a):
    names = ["M", "L", "T", "I"]
    out = []
    for k in range(4):
        if a[k] == 0:
            continue
        out.append("%s^%d" % (names[k], a[k]))
    return "1" if not out else " ".join(out)


# ---------------------------------------------------------------------------
# 数值积分基元
# ---------------------------------------------------------------------------
def loop_integral(field, curve, n=20000, dcurve=None):
    """∮ A·dl：curve(t) -> (x,y,z)，t in [0,2π]。

    dcurve 给定时使用解析切线 dl = curve'(t)dt（机器精度）；
    否则退化为中点法 + 中心差分切线（O(dt^2) 截断）。
    """
    s = 0.0
    dt = 2.0 * PI / n
    for k in range(n):
        t = (k + 0.5) * dt
        p = curve(t)
        if dcurve is not None:
            dv = dcurve(t)
            dl = (dv[0] * dt, dv[1] * dt, dv[2] * dt)
        else:
            pm = curve(t - dt * 0.5)
            pp = curve(t + dt * 0.5)
            dl = ((pp[0] - pm[0]), (pp[1] - pm[1]), (pp[2] - pm[2]))
        a = field(p[0], p[1], p[2])
        s += a[0] * dl[0] + a[1] * dl[1] + a[2] * dl[2]
    return s


def sphere_flux(field, R, n=20000):
    """∮ F·n dS：Fibonacci 球等权采样（权重 4πR²/n）。

    对球面上为常数的被积函数（点电荷的 E·n）精确成立。
    """
    s = 0.0
    w = 4.0 * PI * R * R / n
    ga = PI * (3.0 - math.sqrt(5.0))     # 黄金角
    for k in range(n):
        zz = 1.0 - (2.0 * k + 1.0) / n
        rr = math.sqrt(max(0.0, 1.0 - zz * zz))
        th = ga * k
        nx = rr * math.cos(th)
        ny = rr * math.sin(th)
        nz = zz
        f = field(R * nx, R * ny, R * nz)
        s += (f[0] * nx + f[1] * ny + f[2] * nz) * w
    return s


# ===========================================================================
emit("=" * 78)
emit("S03-V18.13  电荷作为拓扑通量不变量 · 来稿审计与分支收口")
emit("体系：s03_gaq_geometric_atom（GAQ 几何原子与作用量子）")
emit("承接：S03-V18.6 §11 分支二（电荷拓扑通量 · 半阻塞，本册执行）")
emit("      来稿 §7 三条候选分支（库内均已覆盖，本册收口）")
emit("红线：本册不含任何对 GAQ 主张的正面支持证据")
emit("=" * 78)
emit()

# ---------------------------------------------------------------------------
# §0 工具校准（先证明量具可靠，再判来稿；全部为非 GAQ 的外部事实复算）
# ---------------------------------------------------------------------------
emit("§0  工具校准（实现验证器）")
emit("-" * 78)

# T1：Stokes 定理 —— A = (-y/2, x/2, 0)，∇×A = (0,0,1)，单位圆
def A_uniform(x, y, z):
    return (-0.5 * y, 0.5 * x, 0.0)


def unit_circle(t):
    return (math.cos(t), math.sin(t), 0.0)


def unit_circle_d(t):
    return (-math.sin(t), math.cos(t), 0.0)


circ = loop_integral(A_uniform, unit_circle, 20000, dcurve=unit_circle_d)
flux_exact = PI * 1.0
t1 = abs(circ - flux_exact) / abs(flux_exact)
check("T1 Stokes ∮A·dl = ∫∫(∇×A)·dS", t1 < 1e-9, "rel=%.3e" % t1)
emit("  T1  Stokes 闭合：∮A·dl = %s，解析磁通 = %s，相对残差 %.3e"
     % (fx(circ, 10), fx(flux_exact, 10), t1))

# T2：静电点电荷的 ∮E·dl（静电场无旋 ⇒ 包围与否皆为 0）
QTEST = 1.0e-09   # C
KQ = QTEST / (4.0 * PI * EPS0)


def E_point(x, y, z):
    r2 = x * x + y * y + z * z
    r = math.sqrt(r2)
    return (KQ * x / (r2 * r), KQ * y / (r2 * r), KQ * z / (r2 * r))


def circle_R(R):
    def c(t):
        return (R * math.cos(t), R * math.sin(t), 0.0)
    return c


def circle_R_d(R):
    def cd(t):
        return (-R * math.sin(t), R * math.cos(t), 0.0)
    return cd


circ_E = loop_integral(E_point, circle_R(1.0), 20000, dcurve=circle_R_d(1.0))
scale_E = abs(KQ) / 1.0   # E 在 r=1 处的量级
t2 = abs(circ_E) / scale_E
check("T2 静电场环量 ∮E·dl = 0", t2 < 1e-12, "rel=%.3e" % t2)
emit("  T2  静电点电荷 ∮E·dl = %s（相对 E 量级 %.3e）⇒ 静电场环量恒为 0"
     % (fx(circ_E, 6), t2))

# T3：Gauss 定律 ∮E·dS = q/ε₀
gauss = sphere_flux(E_point, 1.0)
exact_gauss = QTEST / EPS0
t3 = abs(gauss - exact_gauss) / abs(exact_gauss)
check("T3 Gauss ∮E·dS = q/eps0", t3 < 1e-9, "rel=%.3e" % t3)
emit("  T3  Gauss 积分 = %s，解析 q/ε₀ = %s，相对残差 %.3e"
     % (fx(gauss, 10), fx(exact_gauss, 10), t3))

# T4：磁通量子 Φ₀ = h/(2e)
phi0 = H_PLANCK / (2.0 * E_CH)
t4 = abs(phi0 - PHI0_CODATA) / PHI0_CODATA
check("T4 磁通量子 h/(2e)", t4 < 1e-8, "rel=%.3e" % t4)
emit("  T4  Φ₀ = h/(2e) = %s Wb，CODATA %s Wb，相对残差 %.3e"
     % (fx(phi0, 10), fx(PHI0_CODATA, 10), t4))

# T5：α = e²/(4πε₀ℏc) 反解 e（循环性演示）
e_from_alpha = math.sqrt(4.0 * PI * EPS0 * ALPHA * HBAR * C_LIGHT)
t5 = abs(e_from_alpha - E_CH) / E_CH
check("T5 α 反解 e", t5 < 1e-8, "rel=%.3e" % t5)
emit("  T5  由 α,ℏ,c,ε₀ 反解 e = %s C，相对残差 %.3e（⇒ e 与 α 互为输入）"
     % (fx(e_from_alpha, 10), t5))

# T6：新恒等式 Φ₀/(Z₀·e) = 1/(4α)
ratio = phi0 / (Z0_VAC * E_CH)
inv4a = 1.0 / (4.0 * ALPHA)
t6 = abs(ratio - inv4a) / inv4a
check("T6 Φ0/(Z0 e) = 1/(4α)", t6 < 1e-8, "rel=%.3e" % t6)
emit("  T6  Φ₀/(Z₀·e) = %s，1/(4α) = %s，相对残差 %.3e  【本册关键读数】"
     % (fx(ratio, 10), fx(inv4a, 10), t6))

# T7：离散 ∇·(∇×A) ≡ 0（恒等式，非预言）
def A_test(x, y, z):
    return (math.sin(y) * z, x * x * z, math.cos(x) * y)


def curl(f, x, y, z, h=1e-2):
    def comp(i):
        def g(a, b, c):
            return f(a, b, c)[i]
        return g
    g0, g1, g2 = comp(0), comp(1), comp(2)
    cx = (g2(x, y + h, z) - g2(x, y - h, z)) / (2 * h) - (g1(x, y, z + h) - g1(x, y, z - h)) / (2 * h)
    cy = (g0(x, y, z + h) - g0(x, y, z - h)) / (2 * h) - (g2(x + h, y, z) - g2(x - h, y, z)) / (2 * h)
    cz = (g1(x + h, y, z) - g1(x - h, y, z)) / (2 * h) - (g0(x, y + h, z) - g0(x, y - h, z)) / (2 * h)
    return (cx, cy, cz)


def div(f, x, y, z, h=1e-2):
    dx = (f(x + h, y, z)[0] - f(x - h, y, z)[0]) / (2 * h)
    dy = (f(x, y + h, z)[1] - f(x, y - h, z)[1]) / (2 * h)
    dz = (f(x, y, z + h)[2] - f(x, y, z - h)[2]) / (2 * h)
    return dx + dy + dz


worst = 0.0
for xs in (0.3, 0.7, 1.1):
    for ys in (0.2, 0.9):
        for zs in (0.4, 1.3):
            worst = max(worst, abs(div(lambda a, b, c: curl(A_test, a, b, c), xs, ys, zs)))
cscale = 1.0
t7 = worst / cscale
check("T7 离散 ∇·(∇×A) = 0", worst < 1e-3, "max=%.3e" % worst)
emit("  T7  离散 ∇·(∇×A) 最大值 = %.3e（差分截断量级，恒等式而非预言）" % worst)

# T8：正电子偶素 2γ / 3γ 衰变率（PDG 对照）
rate_unit = M_E_C2 / HBAR
gamma2 = 0.5 * (ALPHA ** 5) * rate_unit
gamma3 = (2.0 / (9.0 * PI)) * (PI * PI - 9.0) * (ALPHA ** 6) * rate_unit
tau2 = 1.0 / gamma2
tau3 = 1.0 / gamma3
r_calc = tau3 / tau2
r_pdg = TAU_OPS_PDG / TAU_PPS_PDG
t8 = abs(r_calc - r_pdg) / r_pdg
check("T8 Ps 寿命比与 PDG 同量级", t8 < 0.10, "rel=%.3e" % t8)
emit("  T8  领头阶：τ(p-Ps→2γ) = %.4e s，τ(o-Ps→3γ) = %.4e s，比值 %.4e"
     % (tau2, tau3, r_calc))
emit("      PDG 实测比值 = %.4e，相对差 %.3e（领头阶，遗漏 O(α) 修正）" % (r_pdg, t8))
emit()

# ---------------------------------------------------------------------------
# §1 审计：电荷 = 拓扑通量环积分 q ∝ ∮_C A·dl
# ---------------------------------------------------------------------------
emit("§1  来稿 §1：q ∝ ∮_C A·dl 与缠绕手性")
emit("-" * 78)

# --- V13-a：决定性反例（静电荷的 ∮A·dl 恒为 0）--------------------------------
emit("V13-a  决定性检验：电荷是不是 ∮_C A·dl 的函数？")
rows = []
for R in (0.5, 1.0, 2.0, 5.0):
    ce = loop_integral(E_point, circle_R(R), 8000, dcurve=circle_R_d(R))
    gs = sphere_flux(E_point, R)
    rows.append((R, fx(ce / (abs(KQ) / (R * R)), 4), fx(gs, 6), fx(QTEST / EPS0, 6)))
table(["回路半径 R", "∮E·dl / E量级", "∮_S E·dS（Gauss）", "解析 q/ε₀"], rows)
emit("  同一构型：Gauss 曲面通量 = q/ε₀ ≠ 0，而回路积分 ∮A·dl 在 Coulomb 规范（A≡0）下为 0；")
emit("  换规范 A′ = A + ∇χ 时 ∮∇χ·dl = 0（闭合回路，数值见下），换 A = −Et 时 ∮ = −t∮E·dl = 0。")
chi_int = loop_integral(lambda x, y, z: (2.0 * x * y, x * x + 3.0 * z * z, 2.0 * y * z + 0.0),
                        circle_R(1.0), 8000, dcurve=circle_R_d(1.0))
emit("  规范函数 χ = x²y + z³ 的 ∮∇χ·dl = %s（机器零）⇒ 三种规范下回路积分全为 0。"
     % fx(chi_int, 6))
emit("  ⇒ 同一电荷 q 对应 ∮A·dl ≡ 0；同一 ∮A·dl = 0 对应任意 q。")
F("V13-a", "决定性否证：q 不是 ∮_C A·dl 的函数（静电荷 q≠0 而回路积分恒 0；"
           "对照 R14「Y 不是 Lk 的函数」同型反例）")

# --- V13-b：量纲 -------------------------------------------------------------
d_gap = dsub(D_FLUX, D_Q)
check("V13-b 量纲缺口 = 电阻", d_gap == D_Z0, str(d_gap))
check("V13-b' 唯一量纲可行修补 q=Φ/Z0 闭合",
      dsub(D_FLUX, D_Z0) == D_Q, str(dsub(D_FLUX, D_Z0)))
check("V13-p' 库仑势量纲闭合 U=q1q2/(eps0 r)",
      dsub(dadd(D_Q, D_Q), dadd(D_EPS0, D_R)) == D_ENERGY,
      str(dsub(dadd(D_Q, D_Q), dadd(D_EPS0, D_R))))
emit()
emit("V13-b  量纲审计：[∮A·dl] = 磁通 = %s；[q] = %s" % (dname(D_FLUX), dname(D_Q)))
emit("  缺口 = %s = 真空阻抗量纲 ⇒ 比例常数必须自带电阻量纲（外加有量纲输入）。" % dname(d_gap))
emit("  唯一量纲可行的修补：q = (∮A·dl)/Z₀（Z₀ = %.9f Ω），与既有 S03-C0027/C0028 同族。"
     % Z0_VAC)
F("V13-b", "量纲缺口 = 电阻量纲：q ∝ ∮A·dl 需外加有量纲常数（Z₀ 或等价物），非纯拓扑定义")

# --- V13-c：拓扑守恒 vs 1/r 衰减的二难 ---------------------------------------
emit()
emit("V13-c  二难检验：拓扑不变量不衰减，衰减则非拓扑")
PHI_TUBE = 3.7e-15   # Wb，细管内的总磁通（AB 型构型）


def A_tube(x, y, z):
    r2 = x * x + y * y
    if r2 < 1e-18:
        return (0.0, 0.0, 0.0)
    k = PHI_TUBE / (2.0 * PI * r2)
    return (-k * y, k * x, 0.0)


rows = []
for R in (0.5, 1.0, 2.0, 4.0, 8.0):
    v = loop_integral(A_tube, circle_R(R), 8000, dcurve=circle_R_d(R))
    rows.append((R, fx(v, 8), fx(abs(v - PHI_TUBE) / PHI_TUBE, 3)))
table(["回路半径 R", "∮A·dl（AB 细管场）", "相对 Φ 残差"], rows)
emit("  ⇒ 只要回路包围同一根通量管，∮A·dl 与 R 无关（拓扑/AB 型 holonomy 的本征性质）。")
emit("  分支 (i)：若 q 如此不随距离变 ⇒ U 不含 r ⇒ F = −∇U = 0，没有库仑力；")
emit("  分支 (ii)：若 q 随 1/r 衰减（来稿 §5 所需）⇒ q 依赖距离 ⇒ §1 的「拓扑守恒量」失效。")
F("V13-c", "二难：拓扑不变量不随距离衰减（无库仑力），随 1/r 衰减则电荷非拓扑守恒；"
           "来稿 §1 与 §5 只能二选一，不能同时主张")

# --- V13-d：唯一站得住的性质（规范不变性）------------------------------------
emit()
emit("V13-d  规范不变性：∮_C (A+∇χ)·dl = ∮_C A·dl（闭合回路）")
P("V13-d", "规范不变性成立：该积分确为 U(1) Wilson 环 / AB holonomy；"
           "但这是任何 U(1) 规范场共有的性质，不构成 GAQ 还原麦克斯韦的正面证据")
emit()

# ---------------------------------------------------------------------------
# §2 审计：麦克斯韦方程的拓扑还原
# ---------------------------------------------------------------------------
emit("§2  来稿 §2：麦克斯韦方程的拓扑还原")
emit("-" * 78)

# --- V13-e：∇·(回路积分) 无定义 ----------------------------------------------
emit("V13-e  ρ_q ∝ ∇·(∮_C A·dl) 的良定义性")
emit("  ∮_C A·dl 是回路 C 的泛函（一个数），不是空间点的标量场 ⇒ 对它取散度在数学上无定义。")
emit("  即便强行「每点配一个回路」，结果依赖配法（同一场 A、同一物理构型）：")
rows = []
for px in (0.4, 0.8, 1.2):
    # 方案 1：以 x 为圆心、半径固定 1、法向 z
    f1 = loop_integral(A_uniform, circle_R(1.0), 4000, dcurve=circle_R_d(1.0))
    # 方案 2：圆心原点、半径 |x|
    rr = math.sqrt(px * px + 0.3 * 0.3 + 0.2 * 0.2)
    f2 = loop_integral(A_uniform, circle_R(rr), 4000, dcurve=circle_R_d(rr))
    rows.append((px, fx(f1, 6), fx(f2, 6), fx(f2 - f1, 6)))
table(["考察点 x", "方案1（圆心=x, r=1）", "方案2（圆心=O, r=|x|）", "差"], rows)
emit("  两者给不同的「ρ_q 分布」⇒ 定义欠定（与 S03-C0023 同型的参数/约定欠定）。")
F("V13-e", "ρ_q ∝ ∇·(∮_C A·dl) 类型错误且欠定：散度作用于标量泛函无定义；"
           "强行解释为「每点配回路」则结果依赖配法，非唯一")

# --- V13-f：∇·B=0 是恒等式 ---------------------------------------------------
emit()
I("V13-f", "∇·B = ∇·(∇×A) = 0 是恒等式（T7 机器零），任何规范场皆成立；"
           "不构成 GAQ 对麦克斯韦的还原成就，不得计为正面证据")

# --- V13-g：范畴错置（曲面通量 vs 回路积分）----------------------------------
emit()
emit("V13-g  电荷在 Gauss 曲面通量里，不在回路积分里：")
table(["对象", "点电荷构型下的取值"],
      [("∮_S E·dS（2 维闭曲面）", fx(sphere_flux(E_point, 1.0), 8)),
       ("∮_C A·dl（1 维闭回路，Coulomb 规范）", "0.0"),
       ("解析 q/ε₀", fx(QTEST / EPS0, 8))])
F("V13-g", "范畴错置：麦克斯韦的电荷是闭合曲面上的 E 通量（源），∮_C A·dl 是磁通（holonomy）；"
           "同一构型下前者 ∝ q ≠ 0、后者 ≡ 0，二者不是同一对象")

# --- V13-h：E = −∂_tA 缺 −∇φ ------------------------------------------------
emit()
emit("V13-h  静态自相矛盾检查：")
emit("  来稿 §2 给 E ∝ −∂_t A（漏掉 −∇φ）；静态条件 ∂_t A = 0 ⇒ E ≡ 0。")
emit("  来稿 §5 却要在「弱场、静态」下还原库仑势 U ∝ q₁q₂/(4πε₀r)，其力 F = −∇U ≠ 0 需要 E ≠ 0。")
static_ok = (0.0 == 0.0) and (1.0 != 0.0)   # 静态下 E=0，而库仑力要求 E≠0
F("V13-h", "自相矛盾：E ∝ −∂_tA 使一切静电场为零（∂_tA=0），与 §5 静态库仑势还原直接冲突；"
           "正确式为 E = −∇φ − ∂_tA，来稿遗漏的正是承载库仑场的 φ 项")

# --- V13-i：赝矢量 vs 标量 ---------------------------------------------------
emit()
emit("V13-i  B ∝ ∇×A 是赝矢量（轴矢量，3 分量）；挠率 τ 是 F–S 标量（无方向指标，V18.4 V4-d）。")
emit("  标量场不能生成赝矢量分量 ⇒ 「B 对应挠率 τ 的空间分布」缺方向结构来源。")
F("V13-i", "B = ∇×A 为赝矢量而 τ 为标量：标量场无方向指标，不能生成赝矢量；"
           "与 S03-V18.4 V4-d 同源，属体系既有边界的应用")
emit()

# ---------------------------------------------------------------------------
# §3 审计：正负费米子镜像手性与湮灭拓扑条件
# ---------------------------------------------------------------------------
emit("§3  来稿 §3：镜像手性与 e⁻e⁺ → 2γ 的重联条件")
emit("-" * 78)
emit("  来稿主张：闭合扭结 → 两条开式横螺旋（光子零模），故湮灭产物为「一对」光子。")
emit("  实测（PDG）：正电子偶素 p-Ps(¹S₀, C=+1) → 2γ；o-Ps(³S₁, C=−1) → 3γ。")
table(["态", "C 宇称", "主渠道", "领头阶寿命", "PDG 寿命"],
      [("p-Ps ¹S₀", "+1", "2γ", "%.4e s" % tau2, "%.4e s" % TAU_PPS_PDG),
       ("o-Ps ³S₁", "−1", "3γ", "%.4e s" % tau3, "%.4e s" % TAU_OPS_PDG)])
F("V13-j", "实测否证：o-Ps(³S₁) → 3γ 是主渠道（寿命 %.4e s），来稿「一对开式横螺旋」"
           "只能容纳 2γ；2γ/3γ 由电荷共轭 C 宇称选择定则决定，GAQ 拓扑内无 C 量子数"
           % tau3)
emit()
emit("V13-k  重联阈值可否证性：")
emit("  来稿：「距离降到临界尺度，总净通量趋近 0，满足场线重联条件」。")
emit("  但 (+1) + (−1) = 0 在**任何**距离都成立 ⇒ 不给出任何临界尺度；")
emit("  若改指场值叠加的连续量，则随距离连续变化无阈值 ⇒ 恒可事后赋值。")
F("V13-k", "重联阈值不可证伪：缠绕荷之和恒为 0 与距离无关，不产生临界尺度；"
           "与 S03-V18.6 V6-j、V18.1 P1、V18.2 V2-e 同型的「恒可事后赋值」")
emit()
B("V13-l", "防过度否定：单光子禁戒（e⁻e⁺ ↛ γ）是能量动量守恒的运动学结果，"
           "不是拓扑结果；本册仅否证「必须 2γ」的拓扑论证，不否证「湮灭需场重联」这一叙事本身")
emit()

# ---------------------------------------------------------------------------
# §4 审计：电荷量子化的几何来源
# ---------------------------------------------------------------------------
emit("§4  来稿 §4：q = n q_e，n ∈ Z（环绕整数圈）")
emit("-" * 78)
sm_charges = [-1.0, -2.0 / 3.0, -1.0 / 3.0, 0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0]
n_values = len(sm_charges)
bits_needed = math.log(n_values, 2.0)
bits_handed = math.log(2.0, 2.0)
gap_bits = bits_needed - bits_handed
emit("  SM 实测电荷值集合（含反粒子、W±）：%s" % ", ".join("%+.3f" % v for v in sm_charges))
emit("  不同取值个数 = %d ⇒ 需 %.4f bit；左右手缠绕只给 2 值 = 1 bit ⇒ 信息缺口 %.4f bit。"
     % (n_values, bits_needed, gap_bits))
frac = [v for v in sm_charges if abs(v) > 1e-15 and abs(v - round(v)) > 1e-15]
emit("  分数电荷值（非整数）：%s ⇒ 与 q = n·e（n∈Z）直接矛盾。" % ", ".join("%+.3f" % v for v in frac))
F("V13-m", "实测否证双重：(i) 夸克电荷 ±1/3、±2/3 非整数，q = n q_e 被否证；"
           "(ii) 电荷取值至少 7 种而手性标签仅 2 值，信息缺口 %.4f bit" % gap_bits)
emit()
emit("V13-n  量子化的两条可能出路：")
emit("  出路 (i) 通量本身量子化 —— 磁通量子 Φ₀ = h/(2e) = %s Wb。" % fx(phi0, 10))
emit("        ⇒ e = h/(2Φ₀)：e 出现在量子化条件里，是输入不是输出（T5 反解残差 %.1e）⇒ 循环。" % t5)
emit("        且 h = 2πℏ 依赖 ℏ，S03-V18.3 已把 ℏ 改判为公设边界。")
emit("  出路 (ii) 直接用缠绕数 n 作荷 —— 则 q ∈ Z，与分数电荷矛盾（见 V13-m），")
emit("        且量纲仍须外加 Z₀ 定标（见 V13-b）。")
F("V13-n", "电荷量子化的两个出口均不通：通量量子化循环依赖 ℏ（V18.3 锁死）；"
           "缠绕数作荷则值域为 Z，与实测分数电荷矛盾")
emit()
B("V13-o", "防过度否定：体系外确存在电荷量子化的拓扑论证（Dirac 磁单极 eg = 2πn·ℏ/2），"
           "但需磁单极存在（未观测），且其量子单位为 1/(2g) 而非 e，与 1/3 分数电荷不相容；"
           "GAQ 未采用该路径，本册不据此判 GAQ FAIL，仅登记为可选外部输入")
emit()

# ---------------------------------------------------------------------------
# §5 审计：库仑定律的弱场还原
# ---------------------------------------------------------------------------
emit("§5  来稿 §5：库仑势的弱场还原")
emit("-" * 78)
q_from_phi0 = phi0 / Z0_VAC
ratio_to_e = q_from_phi0 / E_CH
ratio_to_quark = q_from_phi0 / (E_CH / 3.0)
emit("  取量纲可行的唯一修补 q = Φ/Z₀：")
emit("    n=1（单圈缠绕）对应 Φ = Φ₀ ⇒ q_min = Φ₀/Z₀ = %s C = %.4f e" % (fx(q_from_phi0, 8), ratio_to_e))
emit("    实测最小非零电荷 |q| = e/3 = %s C ⇒ 相差 %.2f 倍。" % (fx(E_CH / 3.0, 8), ratio_to_quark))
emit("    恒等核对：Φ₀/(Z₀·e) = 1/(4α) = %.6f（T6 残差 %.1e）" % (inv4a, t6))
F("V13-p", "定量否证：若取整数缠绕对应的最小通量量子，则最小电荷为 %.4f e，"
           "与实测最小非零电荷 e/3 相差 %.2f 倍" % (ratio_to_e, ratio_to_quark))
emit()
I("V13-q", "§5 的「通量积分随 1/r 衰减」归因已在 V13-c 判否（拓扑量不衰减）；"
           "本条不重复计数否证，仅留痕：库仑 1/r 可来自传播而非荷的衰减，"
           "故 V13-c 否的是几何叙事，不是库仑势本身")
emit()

# ---------------------------------------------------------------------------
# §6 审计：来稿自列的五条遗留缺口 —— 与库内既有裁定逐条核对
# ---------------------------------------------------------------------------
emit("§6  来稿 §6 遗留缺口 × 库内既有裁定")
emit("-" * 78)
rows = [
    ("1 弱相互作用/β 衰变", "S03-D1 整理稿 + V18_1（接口 P1–P3）+ V18_8（CKM 收口）", "已覆盖"),
    ("2 强相互作用/夸克色荷", "S03-V18_4 五条独立 FAIL，分支一关闭", "已关闭"),
    ("3 普朗克常数 ℏ", "S03-V18.3 改判公设边界", "公设边界"),
    ("4 中微子零通量扭结", "S03-V18_1（零通量扭结）+ V18_9（振荡拓扑重联）", "已裁定"),
    ("5 拓扑量子化（量子算符）", "本册 §4（V13-m/V13-n）", "本册否证"),
]
table(["来稿缺口", "库内既有裁定", "状态"], rows)
I("V13-r", "来稿 §6 五条缺口在库内 5/5 已有裁定（含本册 §4）⇒ 来稿未提出任何新增缺口；"
           "登记时不得计为新发现")
emit()

# ---------------------------------------------------------------------------
# §7 来稿 §7 三条候选分支的收口裁定
# ---------------------------------------------------------------------------
emit("§7  来稿 §7 三条候选分支 × 库内既有产物（不重复造轮子）")
emit("-" * 78)
rows = [
    ("一", "中子 β 衰变拓扑图像 / 弱相互作用作为受限场重联",
     "S03-D1 整理稿（04_理论推导）+ S03-V18_1（接口 P1–P3）+ S03-V18_8（CKM/弱作用收口）",
     "已裁定，不新开"),
    ("二", "夸克与色荷拓扑（色荷作为非阿贝尔环绕数、禁闭）",
     "S03-V18_4：五条独立 FAIL（Z₂ 代数、SU(3) 六项要求、σ=0 与 QCD 矛盾、无场强张量、Z₃ 不自洽）",
     "已关闭，不新开"),
    ("三", "中微子零通量扭结孤子 + 振荡的拓扑形变机制",
     "S03-V18_1（中微子零通量扭结，接口 P1–P3）+ S03-V18_9（中微子振荡拓扑重联，五条 FAIL）",
     "已裁定，不新开"),
]
table(["分支", "内容", "库内既有产物", "裁定"], rows)
emit()
emit("  ⇒ 来稿 §7 提出的三条分支**在库内均已有裁定**，按既有约定不得重复开工。")
emit("  ⇒ 本册执行的命题（电荷 = 拓扑通量不变量）本身，正是 S03-V18.6 §11 遗留的")
emit("     「分支二 · 电荷作为拓扑通量不变量（半阻塞，待执行）」，本册给出最终裁定：")
F("V13-s", "来稿 §7 三分支全部已有库内裁定 ⇒ 分支选择问题收口；"
           "本册执行 V18.6 §11 遗留的「电荷拓扑通量」分支，判为**关闭**")
emit()

# --- 收口：体系能力边界增补 --------------------------------------------------
emit("§8  收口：体系能力边界地图增补（承接 S03-C0034 / V18.4 §8）")
emit("-" * 78)
rows = [
    ("U(1) 电荷（作为源 / Noether 荷）", "不可承载",
     "V13-a：静电荷 q≠0 而 ∮_C A·dl ≡ 0；V13-g：电荷在曲面 E 通量而非回路 holonomy"),
    ("电荷量子化（整数缠绕 ⇒ n·e）", "不可承载",
     "V13-m 分数电荷否证 + 值域不足；V13-n 两条出口（循环 / ℏ 依赖）均不通；V13-p 定量差 %.1f 倍" % ratio_to_quark),
    ("静态电场 / 库仑势的几何来源", "不可承载",
     "V13-h：E ∝ −∂_tA 缺 −∇φ ⇒ 静电场恒零，与库仑还原自相矛盾"),
    ("非阿贝尔场强", "不可承载", "V13-i / V18.4 V4-d：κ、τ 为标量，无方向指标"),
]
table(["能力", "判定", "依据"], rows)
I("V13-t", "能力边界地图增补 3 行（U(1) 电荷、电荷量子化、静态电场来源）；"
           "非阿贝尔场强为既有条目，此处仅作同族留痕不重复计数")
emit()
B("V13-u", "唯一存活的窄域结论（防过度否定）：镜像构型使 Wr 严格反号（V18_8 V8-e，机器零），"
           "故「e⁻ 与 e⁺ 成对区分」在符号层面成立；但标签容量仅 2 值（V13-m），"
           "且 V13-a 的决定性反例使「电荷 = 该积分」的定义本身不成立 ⇒ 该结论只能用于成对区分，"
           "不能用于导出电荷值或电荷量子化")
emit()

# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------
emit("=" * 78)
emit("汇总")
emit("-" * 78)
total_items = sum(COUNTS.values())
emit("  条目合计 %d：PASS=%d FAIL=%d BOUNDARY=%d INFO=%d CORRECTED=%d"
     % (total_items, COUNTS["PASS"], COUNTS["FAIL"], COUNTS["BOUNDARY"],
        COUNTS["INFO"], COUNTS["CORRECTED"]))
nchk = len(CHECKS)
npass = sum(1 for _, ok, _ in CHECKS if ok)
emit("  自检 %d / %d" % (npass, nchk))
for nm, ok, det in CHECKS:
    emit("    [%s] %s  %s" % ("OK" if ok else "XX", nm, det))
emit()
emit("  条目清单：")
for code, verdict, title in ITEMS:
    emit("    [%s] %s  %s" % (verdict, code, title))
emit()
emit("  一句话结论：")
emit("    ∮_C A·dl 是 U(1) holonomy（磁通），不是电荷：静电荷 q≠0 时该积分恒为 0（V13-a），")
emit("    且它与 1/r 库仑衰减、整数电荷量子化、静态电场三者均不相容（V13-c/h/m/p）。")
emit("    「电荷 = U(1) 缠绕荷」曾被 V18.6 判为体系内最顺的方向，本册执行后判为关闭。")
emit("=" * 78)

# ---------------------------------------------------------------------------
# 落盘
# ---------------------------------------------------------------------------
if not os.path.isdir(LOGDIR):
    os.makedirs(LOGDIR)
out_path = os.path.join(LOGDIR, REPORT_NAME)
with io.open(out_path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(LINES) + "\n")

sys.stdout.write("\n".join(LINES[-40:]) + "\n")
sys.stdout.write("\n[written] %s\n" % out_path)
sys.stdout.write("[items] %d  [checks] %d/%d\n" % (total_items, npass, nchk))
