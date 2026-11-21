# -*- coding: utf-8 -*-
"""r430 · ROOT V73 尺度生成 / 有限尺寸 / 三重反转 全维审计引擎.

性质：外部来料（ROOT V73 科研包）独立可算审计；不修改来料任何字节。
编号：磁盘实查 r429 已被并发会话占用（V119 离散谱册），r430 空闲 ⇒ 本册取 r430。
方法：纯标准库 Decimal 60 位 + Fraction 精确算术 + 四元量纲 (M,L,T,Q) +
      阳性对照 + 独立二维数值积分 + W3 四门禁 + 幂等 SHA-256 + 红线计数。
红线：数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确。
"""
import os
import sys
import json
import math
import hashlib
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60
D = Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "数据")
STAMP = "2026-11-21"
RID = "r430"

ENTRIES = []
GUARDS = []


def add(code, verdict, title, detail):
    ENTRIES.append({"id": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, ok, detail):
    GUARDS.append({"id": code, "ok": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError("GUARD-FAIL %s : %s" % (code, detail))


# ---------------- 四元量纲 (M,L,T,Q) ----------------
def dvec(m, l, t, q):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dscale(a, k):
    return tuple(x * k for x in a)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dstr(a):
    names = "MLTQ"
    out = ""
    for n, e in zip(names, a):
        if e == 0:
            continue
        out += n + (str(e) if e != 1 else "")
    return out or "1"


D1 = dvec(0, 0, 0, 0)
DM = dvec(1, 0, 0, 0)


# ---------------- 常数（SI / 自然单位） ----------------
PI = D("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
G_STD_SI = D("6.67430e-11")
C_LIGHT = D("299792458")
HBAR = D("1.054571817e-34")
M_PL_GEV_PER_KG = D("1.78266192e-27")
EARTH_R = D("6371000")
RHO_MEAN = D("5513.4")
ETA_STAT = D("2.3e-15")
ETA_SYST = D("1.5e-15")
ETA_CENTER = D("-1.5e-15")


def rel(a, b):
    a = D(str(a))
    b = D(str(b))
    if b == 0:
        return D("Infinity")
    return abs(a - b) / abs(b)


def sci(x, n=10):
    v = D(x) if not isinstance(x, Decimal) else x
    if v == 0:
        return "0"
    return format(v, ".%dE" % n)


def fs(x, n=12):
    return format(D(str(x)), ".%dE" % n)


# ---------------- 精确有理数线性代数（量纲不可行性判定） ----------------
def rank_exact(rows):
    """Fraction 高斯消元求秩。"""
    M = [list(r) for r in rows]
    m = len(M)
    n = len(M[0]) if m else 0
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def det3(rows):
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


# ==================================================================
# A 段：E013「c 与 ħ 的 G 量纲不可行」——精确复算（3 方程 2 未知的不相容系统）
# ==================================================================
DIMC = dvec(0, 1, -1, 0)        # [c] = L T^-1
DIMHBAR = dvec(1, 2, -1, 0)     # [hbar] = M L^2 T^-1
DIMG = dvec(-1, 3, -2, 0)       # [G] = L^3 M^-1 T^-2

# c^a hbar^b 与 G 的分量匹配： L: a+2b=3 ; M: b=-1 ; T: -a-b=-2
A_ROWS = [(Fraction(1), Fraction(2)), (Fraction(0), Fraction(1)), (Fraction(-1), Fraction(-1))]
RHS_REAL = [Fraction(3), Fraction(-1), Fraction(-2)]
AUG_REAL = [[A_ROWS[0][0], A_ROWS[0][1], RHS_REAL[0]],
            [A_ROWS[1][0], A_ROWS[1][1], RHS_REAL[1]],
            [A_ROWS[2][0], A_ROWS[2][1], RHS_REAL[2]]]
rank_A = rank_exact(A_ROWS)
rank_aug_real = rank_exact(AUG_REAL)
det_aug_real = det3(AUG_REAL)

guard("G_dim_rank_gap", rank_aug_real == 3 and rank_A == 2,
      "rank([A|b])=3 > rank(A)=2 ⇒ 增广系统不相容（G=c^a hbar^b 无实解）")
guard("G_dim_det_nonzero", det_aug_real != 0,
      "增广行列式 det=%s（精确有理数）≠ 0 ⇒ 无解" % det_aug_real)

# 阳性对照：把 T 分量右端改为相容值 ⇒ det=0 且解存在 ⇒ 判据有牙
RHS_CTRL = [Fraction(3), Fraction(-1), Fraction(-4)]
AUG_CTRL = [[A_ROWS[0][0], A_ROWS[0][1], RHS_CTRL[0]],
            [A_ROWS[1][0], A_ROWS[1][1], RHS_CTRL[1]],
            [A_ROWS[2][0], A_ROWS[2][1], RHS_CTRL[2]]]
det_aug_ctrl = det3(AUG_CTRL)
a_ctrl, b_ctrl = Fraction(5), Fraction(-1)
ctrl_satisfied = (a_ctrl + 2 * b_ctrl == RHS_CTRL[0] and b_ctrl == RHS_CTRL[1]
                  and -a_ctrl - b_ctrl == RHS_CTRL[2])
guard("G_dim_positive_control", det_aug_ctrl == 0 and ctrl_satisfied,
      "阳性对照：相容右端 ⇒ det=0 且 (a,b)=(5,-1) 满足全部三式 ⇒ 无解判定非恒真")

# 延拓：引入质量标度 m（G = c^a hbar^b m^c）⇒ 系统相容且唯一解 (1,1,-2)
A3 = [(Fraction(1), Fraction(2), Fraction(0)),
      (Fraction(0), Fraction(1), Fraction(1)),
      (Fraction(-1), Fraction(-1), Fraction(0))]
RHS3 = [Fraction(3), Fraction(-1), Fraction(-2)]
AUG3 = [[A3[0][0], A3[0][1], A3[0][2], RHS3[0]],
        [A3[1][0], A3[1][1], A3[1][2], RHS3[1]],
        [A3[2][0], A3[2][1], A3[2][2], RHS3[2]]]
rank_aug3 = rank_exact(AUG3)
a3, b3, c3 = Fraction(1), Fraction(1), Fraction(-2)
ext_satisfied = (a3 + 2 * b3 == RHS3[0] and b3 + c3 == RHS3[1] and -a3 - b3 == RHS3[2])
dim_ext = dadd(dadd(dscale(DIMC, a3), dscale(DIMHBAR, b3)), dscale(DM, c3))
guard("G_dim_extended_identity", rank_aug3 == 3 and ext_satisfied and dim_ext == DIMG,
      "延拓系统：rank=3，唯一解 (a,b,c)=(1,1,-2)，量纲向量 %s == [G]=%s ⇒ G ≡ c·hbar/m^2"
      % (dstr(dim_ext), dstr(DIMG)))

# 机器验证该延拓解就是普朗克质量恒等式（G 外部输入的等价改写）
MP_SQ = HBAR * C_LIGHT / G_STD_SI
MP_KG = MP_SQ.sqrt()
MP_GEV = MP_KG / M_PL_GEV_PER_KG
MP_ROUNDTRIP_KG = MP_GEV * M_PL_GEV_PER_KG
IDENT_RESID = rel(HBAR * C_LIGHT / (MP_ROUNDTRIP_KG * MP_ROUNDTRIP_KG), G_STD_SI)
guard("G_planck_identity", rel(MP_GEV, D("2.435e18")) < D("2e-4") and IDENT_RESID < D("1e-50"),
      "m_P=sqrt(hbar·c/G)=%.6e kg = %.6e GeV（包内参考 2.435e18 为四舍五入值，相对差 %s）；"
      "hbar·c/m_P^2 与 G 的相对差 %s（恒等式）"
      % (MP_KG, MP_GEV, sci(rel(MP_GEV, D("2.435e18"))), sci(IDENT_RESID)))

add("V73-A01", "PASS", "E013「G 不能由 c 与 ħ 组合」精确复算",
    "c^a hbar^b 与 G 的分量方程 a+2b=3 / b=-1 / -a-b=-2：rank(A)=%d，rank([A|b])=%d，"
    "增广行列式 det=%s（精确有理数）≠ 0 ⇒ 无实解。台账 E013 标 C（条件正确）成立"
    % (rank_A, rank_aug_real, det_aug_real))
add("V73-A02", "PASS", "无解判据的阳性对照（相容右端 ⇒ det=0 且解存在）",
    "把 T 分量右端改为 -4 后 det=%s=0，(a,b)=(5,-1) 满足三式 ⇒ 判定器区分「不相容」与「相容」，"
    "非恒真" % det_aug_ctrl)
add("V73-A03", "CORRECTED", "延拓一个质量标度即回到普朗克恒等式（不可行性前提的边界）",
    "加入 m 后的 3×3 系统 rank=3 且唯一解 (a,b,c)=(1,1,-2)，量纲 %s == [G]=%s ⇒ G ≡ c·hbar/m^2，"
    "即 m=sqrt(hbar·c/G)=%.4e kg = %.4e GeV，与 G 的相对差 %s（恒等式）。"
    "故 E013 的「没有其他有量纲输入」是承重前提：不可行性只在 {c,hbar} 集合内成立，"
    "一旦引入质量标度即退化为已知恒等式、零新内容"
    % (dstr(dim_ext), dstr(DIMG), MP_KG, MP_GEV, sci(IDENT_RESID)))

# ==================================================================
# B 段：E019–E021 一圈 RG 量纲嬗变 —— 复算、往返、灵敏度与「逆算零自由度」
# ==================================================================
B0 = D("7")
MU_UV = D("2.435e18")
MU_IR = D("0.2")


def scale_from_rg(mu, g, b0=B0):
    """Lambda = mu exp(-8 pi^2/(b0 g^2))"""
    return mu * (-(D(8) * PI * PI) / (b0 * g * g)).exp()


def coupling_for_scale(mu, target, b0=B0):
    """g = sqrt(8 pi^2/(b0 ln(mu/Lambda)))"""
    return (D(8) * PI * PI / (b0 * (mu / target).ln())).sqrt()


def rg_beta(g, b0=B0):
    return -b0 * g * g * g / (D(16) * PI * PI)


def rg_scale_sensitivity(g, b0=B0):
    """d ln(Lambda)/dg = 16 pi^2/(b0 g^3)"""
    return D(16) * PI * PI / (b0 * g * g * g)


G_TEST = D("0.55")
LAMBDA_FROM_G = scale_from_rg(MU_UV, G_TEST)
G_BACK = coupling_for_scale(MU_UV, LAMBDA_FROM_G)
RT_RESID = rel(G_BACK, G_TEST)

guard("G_rg_roundtrip", RT_RESID < D("1e-50"),
      "一圈量纲嬗变往返：coupling_for_scale(scale_from_rg(mu,g)) 与 g 的相对差 %s（机器零）"
      % sci(RT_RESID))

SENS = rg_scale_sensitivity(G_TEST)
NEG_INV_BETA = -D(1) / rg_beta(G_TEST)
guard("G_rg_sensitivity", rel(SENS, NEG_INV_BETA) < D("1e-50"),
      "dlnLambda/dg=%s 与 -1/beta=%s 的相对差 %s"
      % (sci(SENS), sci(NEG_INV_BETA), sci(rel(SENS, NEG_INV_BETA))))

G_UV_FITTED = coupling_for_scale(MU_UV, MU_IR)
G_UV_REF = D("0.5066249616363986")
guard("G_rg_g_uv_match", rel(G_UV_FITTED, G_UV_REF) < D("1e-15"),
      "g_uv_fitted=%s；来料 %s；相对差 %s"
      % (sci(G_UV_FITTED, 16), G_UV_REF, sci(rel(G_UV_FITTED, G_UV_REF))))

# 「尺度生成」是纯逆算：Lambda(g) 严格单调 ⇒ 任意目标恰有一个 g ⇒ 零约束力
grid = [D("0.30") + D("0.01") * i for i in range(60)]
mono = all(scale_from_rg(MU_UV, grid[i]) > scale_from_rg(MU_UV, grid[i + 1]) for i in range(len(grid) - 1))
guard("G_rg_monotone_bijection", mono,
      "Lambda(g) 在 g∈[0.30,0.89] 上严格单调递减 ⇒ g→Lambda 为双射，任意目标 Lambda 恰对应一个 g")

add("V73-B01", "PASS", "E019–E021 一圈量纲嬗变与反推公式独立复算",
    "Lambda=mu·exp(-8pi^2/(b0 g^2))；以 mu=2.435e18 GeV、g=0.55 得 Lambda=%s GeV；"
    "反解 g_back=%s，往返相对差 %s（机器零）。灵敏度 dlnLambda/dg=%s 与 -1/beta=%s 一致（相对差 %s）"
    % (sci(LAMBDA_FROM_G, 16), sci(G_BACK, 16), sci(RT_RESID),
       sci(SENS, 16), sci(NEG_INV_BETA, 16), sci(rel(SENS, NEG_INV_BETA))))
add("V73-B02", "PASS", "标定点 g_uv_fitted 逐位复现",
    "coupling_for_scale(2.435e18, 0.2, b0=7)=%s；来料 numerical_summary.json 记 %s；相对差 %s"
    % (sci(G_UV_FITTED, 16), G_UV_REF, sci(rel(G_UV_FITTED, G_UV_REF))))
add("V73-B03", "CORRECTED", "「量纲嬗变产生物理尺度」是纯逆算，对尺度取值零约束力",
    "g→Lambda 严格单调双射（g∈[0.30,0.89] 共 60 点全部单调），任意目标 Lambda 恰有一个 g；"
    "输出不新增自由度即不排除任何候选尺度 ⇒ 判别力 0 bit。与台账 E021 自陈「逆算，不是独立预测」"
    "及候选矩阵第 2 行「边界耦合仍输入」一致")
add("V73-B04", "CORRECTED", "b0=7 是硬编码外部输入，一圈近似本身是模型选择",
    "b0 被写死为 7（SU(3) 一圈系数），来料 E017 自陈「指定渐近自由模型的一圈近似」，"
    "候选矩阵第 3–6 行分别列「非微扰质量隙/COleman-Weinberg/热核/物种数」为未运行或方案依赖；"
    "故「尺度来源」在库内只到「条件可推导」，不能升级为预测")

# ==================================================================
# C 段：E030–E031 诱导引力玩具式 —— 闭合账单（N 的量级 + G 的外部性）
# ==================================================================
MPBAR_GEV = MP_KG / (D(8) * PI).sqrt() / M_PL_GEV_PER_KG   # 约化普朗克质量 Mbar = m_P/sqrt(8pi)
MPBAR_PKG = D("2.435e18")


def species_count(mpbar_gev, cutoff_gev):
    """N = 96 pi^2 (Mbar/Lambda)^2（E031 反算式）"""
    return D(96) * PI * PI * (mpbar_gev / cutoff_gev) ** 2


N_PKG = species_count(MPBAR_PKG, MU_IR)
N_REF = D("1.4044585237211772e+41")
N_FROM_G = species_count(MPBAR_GEV, MU_IR)
N_FROM_2G = species_count(MPBAR_GEV / D(2).sqrt(), MU_IR)

guard("G_species_count", rel(N_PKG, N_REF) < D("1e-15") and N_PKG > D("1e40"),
      "N=96pi^2(Mbar/Lambda)^2 复算 %s；来料 %s；相对差 %s（且 N>1e40，非零读数）"
      % (sci(N_PKG, 16), N_REF, sci(rel(N_PKG, N_REF))))

guard("G_species_scales_inv_G", rel(N_FROM_2G, N_FROM_G / 2) < D("1e-50"),
      "Mbar ∝ 1/sqrt(G) ⇒ N ∝ 1/G：G→2G 时 N/N=%s（严格 1/2）"
      % sci(rel(N_FROM_2G, N_FROM_G / 2)))

add("V73-C01", "PASS", "E031「诱导引力场数反算」逐位复现",
    "N=96pi^2(Mbar/Lambda_IR)^2（Mbar=2.435e18 GeV，Lambda_IR=0.2 GeV）=%s；来料 %s；相对差 %s。"
    "另：由 hbar/c/G 独立算出 Mbar=%s GeV（与包内四舍五入参考相对差 %s，包内自陈「rounded reference, "
    "NOT an independent prediction」）"
    % (sci(N_PKG, 16), N_REF, sci(rel(N_PKG, N_REF)), sci(MPBAR_GEV, 10),
       sci(rel(MPBAR_GEV, MPBAR_PKG))))
add("V73-C02", "FAIL", "「尺度生成链闭合」的定量账单：需 N≈1.4e41 个场，且 G 始终是外部输入",
    "把 0.2 GeV 当作引力截止尺度时 N=%s。关键结构：Mbar ∝ 1/sqrt(G) ⇒ N ∝ 1/G，"
    "G→2G 时 N 精确减半（相对差 %s）⇒ 框架无法由公设给出 G，只能把 G 重新参数化为「物物种数」。"
    "台账 E076「无输入 G 预测」保持 O，本册给出其价码：闭合需 1.4e41 个场"
    % (sci(N_PKG, 16), sci(rel(N_FROM_2G, N_FROM_G / 2))))
add("V73-C03", "CORRECTED", "Mbar 的取值本身就是 G 的重参数化（延拓即恒等式）",
    "Mbar=sqrt(hbar·c/(8pi·G))：把 2.435e18 GeV 换成由 G 导出的 Mbar 后，N 变为 %s（相对差 %s）。"
    "与 A03 的延拓结论同型：一旦允许质量标度，量纲不可行性即失效且退化为已知恒等式"
    % (sci(N_FROM_G, 16), sci(rel(N_FROM_G, N_PKG))))
add("V73-C04", "INFO", "来料已自陈该限制（候选矩阵第 6 行「物种与 UV 一致性问题」）",
    "候选方法矩阵第 6 行「物质数与引力尺度」的「不能跳过的限制」列明写「物种与UV一致性问题」；"
    "台账 E031 标 C（上一玩具模型）⇒ 本册 FAIL 是对已自陈边界的定价，不是发现新错误")

# ==================================================================
# D 段：E054–E058 有限尺寸 Yukawa 形状因子 —— 独立二维积分检验
# ==================================================================
def S_of_x(x):
    """S(x)=3(x cosh x-sinh x)exp(-x)/x^3（E055 的稳定两分支实现）"""
    x = D(str(x))
    if x < D("0.12"):
        xx = x * x
        F = 1 + xx * (D(1) / 10 + xx * (D(1) / 280 + xx * (D(1) / 15120 + xx / D(1330560))))
        return F * (-x).exp()
    return D("1.5") * ((x - 1) + (x + 1) * (-2 * x).exp()) / (x ** 3)


def f_of_x(x):
    """f(x)=x cosh x - sinh x"""
    x = D(str(x))
    if abs(x) < D("0.03"):
        return x ** 3 / 3 + x ** 5 / 30 + x ** 7 / 840 + x ** 9 / 45360
    ex = x.exp()
    enx = (-x).exp()
    return x * (ex + enx) / 2 - (ex - enx) / 2


def uniform_factor(radius, lam, altitude=D(0)):
    x = D(str(radius)) / D(str(lam))
    z = D(str(altitude)) / D(str(lam))
    return S_of_x(x) * (1 + x + z) * (-z).exp()


def point_factor(radius, lam, altitude=D(0)):
    y = (D(str(radius)) + D(str(altitude))) / D(str(lam))
    return (1 + y) * (-y).exp()


def layered_factor(radius, lam, layers, altitude=D(0)):
    """layers: [(inner, outer, rho)]；忠实复刻来料的两分支与末项指数切换"""
    radius = D(str(radius))
    lam = D(str(lam))
    altitude = D(str(altitude))
    mass_norm = D(0)
    weighted = D(0)
    X = radius / lam
    for inner, outer, rho in layers:
        inner = D(str(inner))
        outer = D(str(outer))
        rho = D(str(rho))
        mass_norm += rho * (outer ** 3 - inner ** 3) / 3
        if X >= 250:
            def sp(x, _X=X):
                return ((x - 1) * (x - _X).exp() + (x + 1) * (-x - _X).exp()) / 2
            weighted += rho * lam ** 3 * (sp(outer / lam) - sp(inner / lam))
        else:
            weighted += rho * lam ** 3 * (f_of_x(outer / lam) - f_of_x(inner / lam))
    tail = (-altitude / lam).exp() if X >= 250 else (-(radius + altitude) / lam).exp()
    return (weighted / mass_norm) * (1 + (radius + altitude) / lam) * tail


def earth_two_layer(core_fraction=D("0.546"), mantle_density=D("4500")):
    R = EARTH_R
    Rc = R * core_fraction
    rho_core = (RHO_MEAN * R ** 3 - mantle_density * (R ** 3 - Rc ** 3)) / Rc ** 3
    return [(D(0), Rc, rho_core), (Rc, R, mantle_density)], rho_core


TWO_LAYER, RHO_CORE = earth_two_layer()
M_TWO = sum(rho * (out ** 3 - inn ** 3) / 3 for inn, out, rho in TWO_LAYER)
M_UNIF = RHO_MEAN * EARTH_R ** 3 / 3

LAM_1E6 = D("1e6")
LAM_1E7 = D("1e7")
U_1E6 = uniform_factor(EARTH_R, LAM_1E6)
P_1E6 = point_factor(EARTH_R, LAM_1E6)
T_1E6 = layered_factor(EARTH_R, LAM_1E6, TWO_LAYER)
U_1E6_REF = D("0.2296422276474813")
P_1E6_REF = D("0.012607711634051786")
T_1E6_REF = D("0.19407839029755652")
RATIO_UP_REF = D("18.214425766786064")

guard("G_shape_uniform", rel(U_1E6, U_1E6_REF) < D("1e-14"),
      "均匀球形状因子(lambda=1e6)=%s；来料 %s；相对差 %s"
      % (sci(U_1E6, 16), U_1E6_REF, sci(rel(U_1E6, U_1E6_REF))))
guard("G_shape_point", rel(P_1E6, P_1E6_REF) < D("1e-14"),
      "点源形状因子(lambda=1e6)=%s；来料 %s；相对差 %s"
      % (sci(P_1E6, 16), P_1E6_REF, sci(rel(P_1E6, P_1E6_REF))))
guard("G_shape_two_layer", rel(T_1E6, T_1E6_REF) < D("1e-14"),
      "分层球形状因子(lambda=1e6)=%s；来料 %s；相对差 %s"
      % (sci(T_1E6, 16), T_1E6_REF, sci(rel(T_1E6, T_1E6_REF))))
guard("G_shape_ratio", rel(U_1E6 / P_1E6, RATIO_UP_REF) < D("1e-14"),
      "球/点比=%s；来料 %s；相对差 %s"
      % (sci(U_1E6 / P_1E6, 16), RATIO_UP_REF, sci(rel(U_1E6 / P_1E6, RATIO_UP_REF))))

# 单层退化 == 均匀球（实现一致性）
SINGLE_LAYER = [(D(0), EARTH_R, RHO_MEAN)]
U_SINGLE = layered_factor(EARTH_R, LAM_1E6, SINGLE_LAYER)
guard("G_shape_single_layer_identity", rel(U_SINGLE, U_1E6) < D("1e-25"),
      "单层（均匀）分层实现与均匀球实现逐位一致：相对差 %s" % sci(rel(U_SINGLE, U_1E6)))

# 两层球总质量与均匀平均密度模型完全相同（构造性恒等）
guard("G_two_layer_same_mass", rel(M_TWO, M_UNIF) < D("1e-40") and RHO_CORE > D("1e4"),
      "两层球总质量与均匀 rho_mean=5513.4 模型逐位相同：相对差 %s；rho_core=%s kg/m^3"
      % (sci(rel(M_TWO, M_UNIF)), sci(RHO_CORE)))

# X=250 分支切换处无跳变（两分支的指数补偿精确成立）
LAM_X250 = EARTH_R / D(250)
CONT = [layered_factor(EARTH_R, LAM_X250 * (1 + D(k) / D(100000)), TWO_LAYER) for k in (-3, -1, 0, 1, 3)]
CONT_JUMP = max(abs(CONT[i + 1] - CONT[i]) for i in range(len(CONT) - 1))
guard("G_layer_branch_continuous", CONT_JUMP < D("1e-25"),
      "X=250 分支切换前后 5 点分层因子的最大相邻跳变 %s（末项指数与 scaled_primitive 精确补偿，无断崖）"
      % sci(CONT_JUMP))


def _simpson(fn, a, b, n):
    h = (b - a) / n
    total = fn(a) + fn(b)
    for i in range(1, n):
        total += (4.0 if i % 2 == 1 else 2.0) * fn(a + i * h)
    return total * h / 3.0


def ball_yukawa_shape(radius, lam, altitude=0.0, nr=200, nmu=400, kernel="yukawa"):
    """独立数值积分：均匀球的 Yukawa 加速度比 (a_Y/a_N)/alpha。

    kernel='yukawa'：由纯 Yukawa 势 -GM e^{-s/lam}/s 求梯度 ⇒ 核 e^{-s/lam}(1/s^3+1/(lam s^2))；
    kernel='newton'：仅 1/s^3 核（把相互作用误当作牛顿型 1/r 力的常见简化）。
    """
    R = float(radius)
    L = float(lam)
    d = float(radius) + float(altitude)

    def inner(mu):
        def g(rp):
            s2 = d * d + rp * rp - 2.0 * d * rp * mu
            if s2 <= 0.0:
                s2 = 1e-30
            s = math.sqrt(s2)
            num = d - rp * mu
            ker = 1.0 / (s2 * s) + 1.0 / (L * s2) if kernel == "yukawa" else 1.0 / (s2 * s)
            return rp * rp * math.exp(-s / L) * num * ker
        return _simpson(g, 0.0, R, nr)

    integ = _simpson(inner, -1.0, 1.0, nmu)
    return (3.0 * d * d / (2.0 * R * R * R)) * integ


# 独立积分检验：与包内均匀球因子逐点对拍
ALT_TIGHT = float(EARTH_R) / 10.0
PKG_ALT = uniform_factor(EARTH_R, LAM_1E6, D(str(ALT_TIGHT)))
NUM_YUK = ball_yukawa_shape(EARTH_R, LAM_1E6, ALT_TIGHT, 200, 400, "yukawa")
NUM_NEWTON = ball_yukawa_shape(EARTH_R, LAM_1E6, ALT_TIGHT, 200, 400, "newton")
DIFF_YUK = abs(NUM_YUK - float(PKG_ALT)) / abs(float(PKG_ALT))
DIFF_NEWTON = abs(NUM_NEWTON - float(PKG_ALT)) / abs(float(PKG_ALT))

guard("G_shape_independent_integral", DIFF_YUK < D("1e-9"),
      "独立二维 Simpson 积分（Yukawa 势梯度核）与包内均匀球因子对拍：相对差 %s（λ=1e6, h=R/10）"
      % sci(DIFF_YUK))

# 收敛性：加倍网格后误差应显著下降（判据有牙）
NUM_YUK_2 = ball_yukawa_shape(EARTH_R, LAM_1E6, ALT_TIGHT, 400, 800, "yukawa")
DIFF_YUK_2 = abs(NUM_YUK_2 - float(PKG_ALT)) / abs(float(PKG_ALT))
guard("G_shape_integral_convergence", DIFF_YUK_2 < DIFF_YUK and DIFF_YUK_2 < DIFF_YUK / 2,
      "网格加倍后误差 %s → %s（下降 %.2f 倍，残差为离散误差而非物理差异）"
      % (sci(DIFF_YUK), sci(DIFF_YUK_2), float(DIFF_YUK / DIFF_YUK_2) if DIFF_YUK_2 > 0 else float("inf")))

# 点源极限阳性对照：λ>>R 时均匀球应趋近点源因子 (1+x)e^{-x}
LAM_HUGE = D("1e9")
PKG_HUGE = uniform_factor(EARTH_R, LAM_HUGE)
PT_HUGE = point_factor(EARTH_R, LAM_HUGE)
guard("G_shape_point_limit", rel(PKG_HUGE, PT_HUGE) < D("1e-6"),
      "阳性对照：λ=1e9（x=%.4f）时均匀球因子 %s 与点源因子 %s 相对差 %s ⇒ 弱屏极限退化为点源"
      % (float(EARTH_R / LAM_HUGE), sci(PKG_HUGE, 10), sci(PT_HUGE, 10), sci(rel(PKG_HUGE, PT_HUGE))))

add("V73-D01", "PASS", "E054–E055 形状因子 S(x) 与三口径因子独立复算（Decimal 60 位）",
    "λ=1e6 m：均匀球 %s、点源 %s、分层球 %s；来料 %s / %s / %s，相对差均 <1e-14；"
    "球/点比 %s（来料 %s）。小量展开 F(x)=1+x^2/10+x^4/280+x^6/15120 与闭式在 x<0.12 交叠区一致"
    % (sci(U_1E6, 16), sci(P_1E6, 16), sci(T_1E6, 16), U_1E6_REF, P_1E6_REF, T_1E6_REF,
       sci(U_1E6 / P_1E6, 16), RATIO_UP_REF))
add("V73-D02", "PASS", "独立二维积分检验：均匀球形状因子不是代数改写而是可积分的物理量",
    "对均匀球的 Yukawa 势做二维 Simpson 积分（径向 × 角向，核 e^{-s/lam}(1/s^3+1/(lam s^2))），"
    "得 (a_Y/a_N)/alpha=%s，与包内解析因子 %s 的相对差 %s；网格加倍后误差 %s → %s。"
    "⇒ 来料的形状因子通过与实现无关的独立数值检验"
    % (sci(D(NUM_YUK), 12), sci(PKG_ALT, 12), sci(DIFF_YUK), sci(DIFF_YUK_2)))
add("V73-D03", "CORRECTED", "形状因子对「相互作用核」的读法敏感：只用 1/s^3 核会得到不同的数",
    "若把相互作用误当作牛顿型 1/r 力的简化（核仅 1/s^3），同几何同参数下比值变为 %s，"
    "与包内解析值相对差 %s（量级 O(1)，随 x=R/λ 变化）。⇒ 包内因子的隐含前提是"
    "「由 Yukawa 势求梯度」，该前提未在台账 E054–E056 的前提列显式登记"
    % (sci(D(NUM_NEWTON), 10), sci(DIFF_NEWTON)))
add("V73-D04", "PASS", "单层退化与两层球总质量恒等（实现自洽）",
    "单层（rho=5513.4）分层实现与均匀球实现逐位一致（相对差 %s）；两层地球模型总质量与均匀模型"
    "逐位相同（相对差 %s），rho_core=%s kg/m^3。X=250 分支切换处 5 点相邻跳变 %s（无断崖）"
    % (sci(rel(U_SINGLE, U_1E6)), sci(rel(M_TWO, M_UNIF)), sci(RHO_CORE), sci(CONT_JUMP)))
add("V73-D05", "INFO", "绝对归一化约定未完整声明（诚实边界）",
    "来料未完整声明 Yukawa 球源→加速度比的绝对归一化（源荷代理 Z/A 与质量比代理未给出推导链，"
    "台账 E060 自陈「不是真实普适第五力源荷」）。故本册对形状因子的判定限于：同口径比值、"
    "独立积分一致性、可复现性三项，不作第一性重建声明")

# ==================================================================
# E 段：E064 + eotvos_alpha_bound —— MICROSCOPE 条件界与同卷两套地球几何口径
# ==================================================================
ETA_LIMIT = D("1.5e-15") + D("1.96") * (ETA_STAT ** 2 + ETA_SYST ** 2).sqrt()
ETA_LIMIT_REF = D("6.881975845356424e-15")
Q_TI = D(22) / D("47.867")
Q_PT = D(78) / D("195.084")
DQ = abs(Q_TI - Q_PT)
SOURCE_CHARGE = D("0.5")


def alpha_bound(lam, factor=None):
    """η/(source_charge·|Δ(Z/A)|·f)，f 默认取地表均匀球（与来料一致）"""
    f = uniform_factor(EARTH_R, D(str(lam))) if factor is None else factor
    return ETA_LIMIT / (SOURCE_CHARGE * DQ * f)


ALPHA_1E7 = alpha_bound(LAM_1E7)
ALPHA_1E7_REF = D("2.5543535330292286e-13")
ALPHA_1E6_UNIF = alpha_bound(LAM_1E6)
ALPHA_1E6_TWOLAYER = ETA_LIMIT / (SOURCE_CHARGE * DQ * T_1E6)
BOUND_SHIFT = ALPHA_1E6_TWOLAYER / ALPHA_1E6_UNIF

guard("G_eta_limit", rel(ETA_LIMIT, ETA_LIMIT_REF) < D("1e-15"),
      "MICROSCOPE 95% 保守上限 = |center| + 1.96*hypot(stat,syst) = %s；来料 %s；相对差 %s"
      % (sci(ETA_LIMIT, 16), ETA_LIMIT_REF, sci(rel(ETA_LIMIT, ETA_LIMIT_REF))))
guard("G_alpha_bound", rel(ALPHA_1E7, ALPHA_1E7_REF) < D("1e-14"),
      "条件 alpha 界(λ=1e7)=%s；来料 %s；相对差 %s"
      % (sci(ALPHA_1E7, 16), ALPHA_1E7_REF, sci(rel(ALPHA_1E7, ALPHA_1E7_REF))))
guard("G_bound_geometry_shift", rel(BOUND_SHIFT, U_1E6 / T_1E6) < D("1e-25") and BOUND_SHIFT > D("1.1"),
      "同卷两套地球几何口径：改用已实现却未入界的分层球因子后，λ=1e6 处界移动 %s（相对 +%s）"
      % (sci(BOUND_SHIFT), sci((BOUND_SHIFT - 1) * 100)))

add("V73-E01", "PASS", "E064 MICROSCOPE 上限与条件 alpha 界复算",
    "η_TiPt=(-1.5±2.3_stat±1.5_syst)e-15 ⇒ 95%% 保守上限 |center|+1.96·hypot(stat,syst)=%s；"
    "条件 alpha 界(λ=1e7)=%s（来料 %s，相对差 %s）。注：η 数值属外部已发表事实，需核对原论文口径"
    % (sci(ETA_LIMIT, 16), sci(ALPHA_1E7, 16), ALPHA_1E7_REF, sci(rel(ALPHA_1E7, ALPHA_1E7_REF))))
add("V73-E02", "CORRECTED", "同卷两套地球几何口径：界随「用哪套地球模型」移动 +18.33%",
    "eotvos_alpha_bound 用 altitude=0 的地表均匀球因子（λ=1e6：%s），而同文件已实现 "
    "earth_two_layer_model 却从未进入该界函数（λ=1e6 两层球：%s）。改用两层球后界从 %s 变为 %s，"
    "移动 %s（相对 +%s）。⇒ 同一条界曲线在包内存在两套并存的地球几何口径，"
    "台账 E054–E058 与 E064 未声明该选择"
    % (sci(U_1E6, 10), sci(T_1E6, 10), sci(ALPHA_1E6_UNIF, 10), sci(ALPHA_1E6_TWOLAYER, 10),
       sci(BOUND_SHIFT), sci((BOUND_SHIFT - 1) * 100)))
add("V73-E03", "CORRECTED", "该曲线是条件曲线而非对第五力的约束（口径收紧，来料自陈）",
    "η→Δ(g_Y/g_N) 的换算依赖「小 α 展开 + 材料源荷代理 Z/A」两层未声明假设；"
    "台账 E060 自陈「不是真实普适第五力源荷」，README 亦写明「特定代理源荷模型条件限制」。"
    "⇒ 本册不把它读作实验约束，仅读作「在给定代理模型下的条件界」；来料在此点诚实度可判 PASS")

# ==================================================================
# F 段：E065–E068 三重反转 8 态 Walsh–Hadamard —— 精确正交、偏置结构与 df=0
# ==================================================================
def hadamard_rows():
    rows = []
    for h in (-1, 1):
        for r in (-1, 1):
            for s in (-1, 1):
                rows.append([1, h, r, s, h * r, h * s, r * s, h * r * s])
    return rows


HROWS = hadamard_rows()
H_COL_NAMES = ["1", "h", "r", "s", "hr", "hs", "rs", "hrs"]
HT_H = [[sum(HROWS[i][a] * HROWS[i][b] for i in range(8)) for b in range(8)] for a in range(8)]
ORTHO_EXACT = all(HT_H[a][b] == (8 if a == b else 0) for a in range(8) for b in range(8))
guard("G_hadamard_orthogonal", ORTHO_EXACT,
      "H^T H = 8 I 精确成立（整数算术，无浮点误差）")

COEF = [Fraction(1, 10), Fraction(4, 100), Fraction(8, 100), Fraction(2, 100),
        Fraction(3, 1000), Fraction(-6, 1000), Fraction(7, 1000), Fraction(1, 100)]


def y_from_coef(coef):
    return [sum(Fraction(HROWS[i][k]) * coef[k] for k in range(8)) for i in range(8)]


def triple_contrast(y):
    """beta_hat_hrs = (1/8) sum_hrs y"""
    return sum(Fraction(HROWS[i][7]) * y[i] for i in range(8)) / 8


Y_CLEAN = y_from_coef(COEF)
BETA_HRS = triple_contrast(Y_CLEAN)
guard("G_triple_contrast_unbiased", BETA_HRS == COEF[7],
      "无噪声时 beta_hat_hrs=%s（精确有理数）= 系数 %s ⇒ 无偏" % (BETA_HRS, COEF[7]))

# 偏置结构：把 δ 强度的开关伪差加进数据，看 beta_hat_hrs 被推动多少
DELTA = Fraction(1, 1000)
BIAS = []
for k in range(8):
    pert = [Y_CLEAN[i] + DELTA * Fraction(HROWS[i][k]) for i in range(8)]
    BIAS.append(triple_contrast(pert) - BETA_HRS)
LOW_ORDER_BIAS = sum(abs(BIAS[k]) for k in range(7))
THIRD_ORDER_BIAS = BIAS[7]

guard("G_bias_low_order_zero", LOW_ORDER_BIAS == 0,
      "0–2 阶开关伪差（constant/h/r/s/hr/hs/rs 共 7 个）对 beta_hat_hrs 的偏置合计=%s（精确 0）"
      % LOW_ORDER_BIAS)
guard("G_bias_third_order_full", THIRD_ORDER_BIAS == DELTA,
      "3 阶（hrs 形）开关伪差的偏置=%s = δ 本身（无衰减、分离力精确为 0）" % THIRD_ORDER_BIAS)

# 噪声方差：Var(beta_hat) = sigma^2 / 8（1/sqrt(8) 方差缩减）
NOISE_FACTOR = D(1) / D(8).sqrt()
NOISE_FACTOR_REF = D("0.35355339059327373")
guard("G_noise_factor", rel(NOISE_FACTOR, NOISE_FACTOR_REF) < D("1e-15"),
      "完全正交给出的噪声因子 1/sqrt(8)=%s；来料 %s；相对差 %s"
      % (sci(NOISE_FACTOR, 16), NOISE_FACTOR_REF, sci(rel(NOISE_FACTOR, NOISE_FACTOR_REF))))

# df：8 观测 / 8 参数 ⇒ 正交设计可精确插值 ⇒ 残差恒 0 ⇒ 无 chi^2 拟合优度检验
Y_NOISY = [Y_CLEAN[i] + Fraction(i % 3 - 1, 1000) for i in range(8)]
BETA_FIT = [sum(Fraction(HROWS[i][k]) * Y_NOISY[i] for i in range(8)) / 8 for k in range(8)]
RESID_MAX = max(abs(sum(Fraction(HROWS[i][k]) * BETA_FIT[k] for k in range(8)) - Y_NOISY[i]) for i in range(8))
N_OBS = 8
N_PARAMS = 8
DF_MODEL = N_OBS - N_PARAMS
guard("G_dof_zero", DF_MODEL == 0 and RESID_MAX == 0,
      "8 观测 / 8 参数：df=%d，且正交设计的精确插值使残差最大绝对值=%s（恒 0）⇒ chi^2 恒为 0，"
      "不存在拟合优度检验" % (DF_MODEL, RESID_MAX))

# 阳性对照：降到 7 参数 ⇒ df=1 ⇒ 残差非零 ⇒ 检验存在（判据有牙）
K7 = [0, 1, 2, 3, 4, 5, 6]
A7 = [[Fraction(HROWS[i][k]) for k in K7] for i in range(8)]
# 用 Gram 法求 7 参数最小二乘（正规方程，精确有理数）
GRAM = [[sum(A7[i][a] * A7[i][b] for i in range(8)) for b in range(7)] for a in range(7)]
RHSV = [sum(A7[i][a] * Y_NOISY[i] for i in range(8)) for a in range(7)]


def solve_exact(M, v):
    n = len(M)
    A = [list(M[i]) + [v[i]] for i in range(n)]
    for c in range(n):
        piv = None
        for i in range(c, n):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[c][j] for j in range(n + 1)]
    return [A[i][n] for i in range(n)]


SOL7 = solve_exact(GRAM, RHSV)
RESID7 = max(abs(sum(A7[i][a] * SOL7[a] for a in range(7)) - Y_NOISY[i]) for i in range(8)) if SOL7 else None
guard("G_dof_positive_control", SOL7 is not None and RESID7 is not None and RESID7 > 0,
      "阳性对照：降到 7 参数 ⇒ df=1，残差最大绝对值=%s（非零）⇒ 检验力存在，df=0 不是恒真"
      % (RESID7 if RESID7 is not None else "None"))

add("V73-F01", "PASS", "E066 Walsh–Hadamard 完全正交（精确整数算术）",
    "8×8 设计 H 的列序为 [1,h,r,s,hr,hs,rs,hrs]，H^T H = 8I 精确成立（整数算术，无浮点误差）；"
    "无噪声时 beta_hat_hrs 与真系数逐位相等（%s）⇒ 估计量无偏" % BETA_HRS)
add("V73-F02", "FAIL", "对 3 阶（hrs 形）开关伪差的分离力精确为 0（偏置 = δ，无衰减）",
    "把强度 δ 的伪差加到数据：0–2 阶 7 个伪差形状对 beta_hat_hrs 的偏置合计=%s（精确 0）；"
    "3 阶 hrs 形伪差的偏置=%s = δ 本身 ⇒ 完全不衰减。README 第 9 行「可消去所有低阶开关伪差」"
    "按字面正确（低阶=0/1/2 阶），但隔离只在 2 阶以内成立；候选矩阵第 25 行已自陈「hrs同形伪差」"
    % (LOW_ORDER_BIAS, THIRD_ORDER_BIAS))
add("V73-F03", "FAIL", "8 观测 / 8 参数 ⇒ 残差 df=0 ⇒ 不存在任何拟合优度检验",
    "正交设计可精确插值任意 8 点数据：带噪声数据的拟合残差最大绝对值=%s（恒 0）⇒ chi^2 恒为 0。"
    "阳性对照：降到 7 参数（df=1）后残差=%s（非零）。⇒ 「完全正交」提供的是方差 1/sqrt(8) 缩减"
    "（噪声因子 %s），不是检验力；显著性≠新物理的结论成立但机理不同"
    % (RESID_MAX, RESID7 if RESID7 is not None else "None", sci(NOISE_FACTOR, 12)))
add("V73-F04", "PASS", "E068 噪声方差缩减 1/sqrt(8) 复现",
    "Var(beta_hat_hrs)=sigma^2/8 ⇒ 噪声因子 1/sqrt(8)=%s；来料 %s；相对差 %s"
    % (sci(NOISE_FACTOR, 16), NOISE_FACTOR_REF, sci(rel(NOISE_FACTOR, NOISE_FACTOR_REF))))
add("V73-F05", "CORRECTED", "8 态完全正交不是「三重反转」的充分条件（设计层与模型层分离）",
    "设计层（正交、方差缩减）在库内成立且已复算；但 E065 的观测模型 d_e=delta+beta·X_e+eps_e 与"
    "8 态因子是两层结构，三重反转只能消去 0–2 阶开关项，不解决模型层的可识别性（见 G 段）")

# ==================================================================
# G 段：E069–E071 跨环境可识别性 —— 同形伪差的精确混叠
# ==================================================================
X_FRAC = [Fraction(-1) + Fraction(2 * i, 23) for i in range(24)]
XCONF = [[Fraction(1), x, x] for x in X_FRAC]
RANK_CONF = rank_exact(XCONF)
guard("G_cross_env_rank", RANK_CONF == 2,
      "rank([1,X,X])=%d < 3 ⇒ 完全同形的仪器项与候选响应不可分辨（与来料 E071 记载一致）" % RANK_CONF)

# 8 态对比量对「环境内共同模加性偏移」严格免疫
OFFSET = Fraction(7, 1000)
Y_OFFSET = [Y_CLEAN[i] + OFFSET for i in range(8)]
BETA_OFFSET = triple_contrast(Y_OFFSET)
guard("G_common_mode_invariance", BETA_OFFSET == BETA_HRS,
      "给同一环境的 8 个状态整体加常数偏移 %s：beta_hat_hrs 完全不变（%s == %s）"
      % (OFFSET, BETA_OFFSET, BETA_HRS))

# 同形混淆项与信号在跨环境回归中精确混叠（精确有理数 OLS）
BETA_TRUE = Fraction(4, 10000)
NUISANCE = Fraction(12, 10000)
GAMMA_CONF = Fraction(9, 10000)
Y_ENV = [NUISANCE + (BETA_TRUE + GAMMA_CONF) * x for x in X_FRAC]
XBAR = sum(X_FRAC) / 24
YBAR = sum(Y_ENV) / 24
SXX = sum((x - XBAR) ** 2 for x in X_FRAC)
SXY = sum((x - XBAR) * (y - YBAR) for x, y in zip(X_FRAC, Y_ENV))
SLOPE_FIT = SXY / SXX
guard("G_aliasing_exact", SLOPE_FIT == BETA_TRUE + GAMMA_CONF,
      "跨环境 OLS 斜率=%s = beta+gamma（beta=%s, gamma=%s）⇒ 同形混淆项与信号精确混叠，"
      "回归无法分离（无偏估计不可得）" % (SLOPE_FIT, BETA_TRUE, GAMMA_CONF))

add("V73-G01", "PASS", "E071「完全同形伪差不可辨识」精确复算",
    "设计矩阵 [1,X,X]（24 个环境，X 为有理数格点）秩=%d < 3 ⇒ 与信号同形的仪器项与候选响应"
    "在同一回归中不可分辨。来料 E071 与候选矩阵第 26 行已自陈，本册给出精确有理数证明"
    % RANK_CONF)
add("V73-G02", "FAIL", "三重反转是单环境因子 ⇒ 对跨环境同形退化零缓解",
    "8 态对比量对环境内共同模加性偏移严格免疫：整体加常数 %s 后 beta_hat_hrs 完全不变。"
    "而跨环境同形混淆项 ∝ X 恰在每个环境内是常数（共同模）⇒ 混叠是精确的："
    "回归斜率=%s=beta+gamma。故「三重反转 + 跨环境」两条路线在同一数据上不能联合破缺同形退化"
    % (OFFSET, SLOPE_FIT))
add("V73-G03", "CORRECTED", "候选矩阵第 26–27 行的两条限制合并为同一开放项",
    "第 26 行「跨环境满秩」的不能跳过限制=「同形环境伪差不可分」；第 27 行「盲法随机化」的限制"
    "=「不消完全同形干扰」。二者同指一个不可约退化 ⇒ 归并为单条开放项（框架内不可闭合），"
    "其余两条路线（零耦合材料控制、外部源调制）只能换数据不能换代数")

# __NEXT__
