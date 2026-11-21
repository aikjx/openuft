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
# 约化普朗克质量 Mbar = m_P/sqrt(8pi)：来料 E029/E030 的 2.435e18 GeV 即此量（不是 m_P 本身）
MPBAR_GEV = MP_KG / (D(8) * PI).sqrt() / M_PL_GEV_PER_KG
MP_ROUNDTRIP_KG = MP_GEV * M_PL_GEV_PER_KG
IDENT_RESID = rel(HBAR * C_LIGHT / (MP_ROUNDTRIP_KG * MP_ROUNDTRIP_KG), G_STD_SI)
guard("G_planck_identity",
      rel(MPBAR_GEV, D("2.435e18")) < D("2e-4") and IDENT_RESID < D("1e-50"),
      "m_P=sqrt(hbar·c/G)=%.6e kg = %.6e GeV；约化普朗克质量 Mbar=m_P/sqrt(8pi)=%.6e GeV"
      "（来料 E029/E030 的 2.435e18 即 Mbar，四舍五入到 4 位，相对差 %s）；"
      "hbar·c/m_P^2 与 G 的相对差 %s（恒等式）"
      % (MP_KG, MP_GEV, MPBAR_GEV, sci(rel(MPBAR_GEV, D("2.435e18"))), sci(IDENT_RESID)))

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
    "一旦引入质量标度即退化为已知恒等式、零新内容。"
    "（口径提示：来料的 2.435e18 GeV 是约化普朗克质量 Mbar=m_P/sqrt(8pi)=%.6e GeV，不是 m_P 本身）"
    % (dstr(dim_ext), dstr(DIMG), MP_KG, MP_GEV, sci(IDENT_RESID), MPBAR_GEV))

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
# Lambda(g)=mu*exp(-8pi^2/(b0 g^2))：g 增大 ⇒ 指数项趋近 0 ⇒ Lambda 趋近 mu ⇒ 严格单调递增
mono = all(scale_from_rg(MU_UV, grid[i]) < scale_from_rg(MU_UV, grid[i + 1]) for i in range(len(grid) - 1))
guard("G_rg_monotone_bijection", mono,
      "Lambda(g) 在 g∈[0.30,0.89] 上严格单调递增（值域 (0, mu)）⇒ g→Lambda 为双射，"
      "任意目标 Lambda 恰对应一个 g（零自由度、零约束力）")

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
MPBAR_PKG = D("2.435e18")   # 来料的约化普朗克质量 Mbar（MPBAR_GEV 已在 A 段由 hbar/c/G 算出）


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


def layered_factor(radius, lam, layers, altitude=D(0), force_branch=None):
    """layers: [(inner, outer, rho)]；忠实复刻来料的两分支与末项指数切换。

    force_branch=None 走来料的 X>=250 判据；"high"/"low" 可强制走某一分支（用于分支等价性检验）。
    """
    radius = D(str(radius))
    lam = D(str(lam))
    altitude = D(str(altitude))
    mass_norm = D(0)
    weighted = D(0)
    X = radius / lam
    use_high = (X >= 250) if force_branch is None else (force_branch == "high")
    for inner, outer, rho in layers:
        inner = D(str(inner))
        outer = D(str(outer))
        rho = D(str(rho))
        mass_norm += rho * (outer ** 3 - inner ** 3) / 3
        if use_high:
            def sp(x, _X=X):
                return ((x - 1) * (x - _X).exp() + (x + 1) * (-x - _X).exp()) / 2
            weighted += rho * lam ** 3 * (sp(outer / lam) - sp(inner / lam))
        else:
            weighted += rho * lam ** 3 * (f_of_x(outer / lam) - f_of_x(inner / lam))
    tail = (-altitude / lam).exp() if use_high else (-(radius + altitude) / lam).exp()
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

# X=250 分支切换：同一组参数下强制走两分支，比较分支差异本身
# （此前版本误把「跨 lam 窗口的平滑变化」当分支跳变，判据设计错误，由本次守卫拦下）
LAM_X250 = EARTH_R / D(250)
T_HIGH = layered_factor(EARTH_R, LAM_X250, TWO_LAYER, force_branch="high")
T_LOW = layered_factor(EARTH_R, LAM_X250, TWO_LAYER, force_branch="low")
BRANCH_DIFF = rel(T_HIGH, T_LOW)
guard("G_layer_branch_continuous", BRANCH_DIFF < D("1e-50"),
      "X=250 分支切换：同一组参数下强制走两分支，两结果相对差 %s（scaled_primitive=e^{-X}·f(x) 与末项指数"
      "的补偿精确成立 ⇒ 机器零，非近似）" % sci(BRANCH_DIFF))
# 平滑性参照（信息量，非分支判据）：跨 ±3e-5 的 lam 窗口的相邻变化
CONT = [layered_factor(EARTH_R, LAM_X250 * (1 + D(k) / D(100000)), TWO_LAYER) for k in (-3, -1, 0, 1, 3)]
CONT_SPREAD = max(abs(CONT[i + 1] - CONT[i]) for i in range(len(CONT) - 1))


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
    % (sci(D(NUM_YUK), 12), sci(PKG_ALT, 12), sci(DIFF_YUK), sci(DIFF_YUK), sci(DIFF_YUK_2)))
add("V73-D03", "CORRECTED", "形状因子对「相互作用核」的读法敏感：只用 1/s^3 核会得到不同的数",
    "若把相互作用误当作牛顿型 1/r 力的简化（核仅 1/s^3），同几何同参数下比值变为 %s，"
    "与包内解析值相对差 %s（量级 O(1)，随 x=R/λ 变化）。⇒ 包内因子的隐含前提是"
    "「由 Yukawa 势求梯度」，该前提未在台账 E054–E056 的前提列显式登记"
    % (sci(D(NUM_NEWTON), 10), sci(DIFF_NEWTON)))
add("V73-D04", "PASS", "单层退化与两层球总质量恒等（实现自洽）",
    "单层（rho=5513.4）分层实现与均匀球实现逐位一致（相对差 %s）；两层地球模型总质量与均匀模型"
    "逐位相同（相对差 %s），rho_core=%s kg/m^3。X=250 分支在同一参数下两分支相对差 %s（精确补偿成立）；"
    "跨 ±3e-5 的 lam 窗口相邻变化 %s 属函数自身的平滑变化（信息量，非分支跳变）"
    % (sci(rel(U_SINGLE, U_1E6)), sci(rel(M_TWO, M_UNIF)), sci(RHO_CORE),
       sci(BRANCH_DIFF), sci(CONT_SPREAD)))
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

# ==================================================================
# H 段：来料台账 / 候选矩阵 / 结果摘要的条件式交叉核对
#       （事实源缺失即记 INFO，不产生「解析失败 = 真的为 0」的假零）
# ==================================================================
import csv as _csv

FACT = os.path.join(ROOT, "90_历史归档", "来源语料_ufthub_ROOT_V52-V82_202611",
                    "V73", "ROOT_V73")
FACT_JSON = os.path.join(FACT, "results", "numerical_summary.json")
FACT_LEDGER = os.path.join(FACT, "data", "ROOT_V73_核心方程与证明状态.csv")
FACT_CAND = os.path.join(FACT, "data", "ROOT_V73_全部候选方法与失败条件.csv")

FACT_HASH = {}
for _p in (FACT_JSON, FACT_LEDGER, FACT_CAND):
    if os.path.exists(_p):
        with open(_p, "rb") as _fh:
            FACT_HASH[os.path.basename(_p)] = hashlib.sha256(_fh.read()).hexdigest()

# --- H-1 结果摘要逐项核对 ---
FACT_JSON_OK = os.path.exists(FACT_JSON)
if FACT_JSON_OK:
    with open(FACT_JSON, "r", encoding="utf-8") as _fh:
        _js = json.load(_fh)
    _rg = _js["rg_calibration"]
    _sh = _js["source_shape"]
    _cm = _js["conditional_microscope"]
    _tc = _js["triple_contrast"]
    CHK = [
        ("g_uv_fitted", D(str(_rg["g_uv_fitted"])), G_UV_FITTED),
        ("species_for_IR", D(str(_rg["species_for_IR_as_gravity_cutoff"])), N_PKG),
        ("eta_95_bound", D(str(_cm["eta_conservative_approx_95_bound"])), ETA_LIMIT),
        ("alpha_lambda_1e7", D(str(_cm["bound_alpha_lambda_1e7m"])), ALPHA_1E7),
        ("shape_uniform", D(str(_sh["uniform_sphere"])), U_1E6),
        ("shape_point", D(str(_sh["point_approx"])), P_1E6),
        ("shape_two_layer", D(str(_sh["two_layer_sphere_same_mass"])), T_1E6),
        ("shape_ratio", D(str(_sh["uniform_over_point_ratio"])), U_1E6 / P_1E6),
        ("noise_std_factor", D(str(_tc["fully_contrast_noise_std_factor"])), NOISE_FACTOR),
    ]
    JSON_MAX_REL = max(rel(a, b) for _n, a, b in CHK)
    RANK_MATCH = int(_tc["unidentifiable_same_signature_rank"]) == RANK_CONF
    guard("G_fact_json_match", JSON_MAX_REL < D("1e-12") and RANK_MATCH,
          "来料 results/numerical_summary.json 的 %d 项关键读数与本册独立复算逐项一致（最大相对差 %s）；"
          "同形不可辨识秩 %s 与本册精确有理数秩 %s 一致"
          % (len(CHK), sci(JSON_MAX_REL), _tc["unidentifiable_same_signature_rank"], RANK_CONF))
    add("V73-H01", "PASS", "来料结果摘要的 9 项关键读数与本册独立复算逐项一致",
        "g_uv_fitted / species / eta 上限 / alpha(λ=1e7) / 三个形状因子 / 球点比 / 噪声因子 共 %d 项，"
        "最大相对差 %s；同形秩 %s = 本册精确秩 %s。⇒ 本册不是复述来料数字，而是独立算得同一组读数"
        % (len(CHK), sci(JSON_MAX_REL), _tc["unidentifiable_same_signature_rank"], RANK_CONF))
else:
    JSON_MAX_REL = None
    RANK_MATCH = None
    add("V73-H01", "INFO", "来料结果摘要缺失，跳过交叉核对（不产生假零）",
        "未找到 %s ⇒ 本册只报自算读数，不以「核对通过」充数" % FACT_JSON)

# --- H-2 核心方程台账（77 条） ---
LEDGER_ROWS = []
if os.path.exists(FACT_LEDGER):
    with open(FACT_LEDGER, "r", encoding="utf-8-sig", newline="") as _fh:
        _rd = list(_csv.reader(_fh))
    LEDGER_ROWS = [r for r in _rd[1:] if r and r[0].strip()]
LEDGER_BY_CODE = {r[0].strip(): r for r in LEDGER_ROWS}
LEDGER_STATUS = {}
for _r in LEDGER_ROWS:
    _st = _r[4].strip()
    LEDGER_STATUS[_st] = LEDGER_STATUS.get(_st, 0) + 1
LEDGER_CODES = [r[0].strip() for r in LEDGER_ROWS]
LEDGER_CONTIG = all(LEDGER_CODES[i] == "V73-E%03d" % (i + 1) for i in range(len(LEDGER_CODES)))

if LEDGER_ROWS:
    guard("G_ledger_rows", len(LEDGER_ROWS) == 77 and LEDGER_CONTIG,
          "台账 %s 共 %d 条且编号 V73-E001..V73-E077 连续无缺"
          % (os.path.basename(FACT_LEDGER), len(LEDGER_ROWS)))
    guard("G_ledger_status_domain", set(LEDGER_STATUS) <= set(["E", "C", "H", "O", "X"]),
          "台账证明状态分布 = %s（仅 E/C/H/O/X 五类，无越界取值）" % LEDGER_STATUS)
    E013 = LEDGER_BY_CODE.get("V73-E013", ["", "", "", "", ""])
    E030 = LEDGER_BY_CODE.get("V73-E030", ["", "", "", "", ""])
    E071 = LEDGER_BY_CODE.get("V73-E071", ["", "", "", "", ""])
    KEY_OK = (E013[4].strip() == "C" and "不可行" in E013[3]
              and E030[4].strip() == "H" and "玩具" in E030[2]
              and E071[4].strip() == "C" and "rank([1,X,X])=2<3" in E071[3])
    guard("G_ledger_key_rows", KEY_OK,
          "台账三条关键陈述与本册独立结论一致：E013「G 不能由 c 与 ħ 组合」标 C 且陈述含「不可行」；"
          "E030 标 H（玩具公式）；E071 标 C 且陈述含 rank([1,X,X])=2<3")
    add("V73-H02", "PASS", "台账 77 条闭合，E013/E030/E071 三条关键陈述与本册独立结论一致",
        "台账 %s：%d 条，编号 E001–E077 连续，状态分布 %s（E=已证、C=条件成立、H=玩具/启发、"
        "O=开放、X=未做）。本册 A/C/G 三段的 FAIL 全部落在这三条已自陈的边界内 ⇒ 是定价不是纠错"
        % (os.path.basename(FACT_LEDGER), len(LEDGER_ROWS), LEDGER_STATUS))
else:
    add("V73-H02", "INFO", "来料台账缺失，跳过台账核对",
        "未找到 %s" % FACT_LEDGER)

# --- H-3 候选方法矩阵（37 条）的「不能跳过的限制」列 ---
CAND_ROWS = []
if os.path.exists(FACT_CAND):
    with open(FACT_CAND, "r", encoding="utf-8-sig", newline="") as _fh:
        _rd2 = list(_csv.reader(_fh))
    CAND_ROWS = [r for r in _rd2[1:] if r and r[0].strip()]
CAND_LIMIT = [r[6].strip() for r in CAND_ROWS if len(r) > 6]
CAND_SAME = [t for t in CAND_LIMIT if "同形" in t]
CAND_SCALE = [r for r in CAND_ROWS if len(r) > 1 and r[1].strip() == "尺度生成"]

if CAND_ROWS:
    guard("G_cand_rows", len(CAND_ROWS) == 37,
          "候选方法矩阵 %s 共 %d 条" % (os.path.basename(FACT_CAND), len(CAND_ROWS)))
    guard("G_cand_same_shape", len(CAND_SAME) == 4,
          "「不能跳过的限制」列中直指同形伪差的共 %d 条：%s" % (len(CAND_SAME), "；".join(CAND_SAME)))
    guard("G_cand_scale_gen", len(CAND_SCALE) == 5,
          "「尺度生成」类候选共 %d 条，其限制列分别写明：%s"
          % (len(CAND_SCALE), "；".join(r[6].strip() for r in CAND_SCALE)))
    add("V73-H03", "INFO", "候选矩阵 37 条的限制列已逐条覆盖本册全部 FAIL 点（来料自陈边界）",
        "37 条候选中 %d 条限制列直指同形伪差（hr 同形 / hrs 同形 / 同形环境伪差不可分 / 不消完全同形干扰），"
        "「尺度生成」类 %d 条的限制列分别为：%s。⇒ 本册 C02/F02/F03/G02 四个 FAIL 均落在来料自陈的"
        "限制之内，属边界定价而非新发现；台账 E076「无输入 G 预测」标 O 的结论同样被保留"
        % (len(CAND_SAME), len(CAND_SCALE), "；".join(r[6].strip() for r in CAND_SCALE)))
else:
    add("V73-H03", "INFO", "来料候选矩阵缺失，跳过候选矩阵核对",
        "未找到 %s" % FACT_CAND)

# ==================================================================
# W3 四门禁（C1 定量 / C2 非反解 / C3 可执行且未拟合 / C4 双锚点不自相矛盾）
# ==================================================================
W3_GATES = [
    {
        "id": "V73-尺度生成（RG 量纲嬗变 + 诱导引力场数）",
        "C1": True, "C2": False, "C3": False, "C4": False,
        "reason": "Lambda(g) 与 N=96pi^2(Mbar/Lambda)^2 均可算且已复算；但 g->Lambda 是严格单调双射"
                  "（零约束力），E021/E031 自陈是逆算；b0=7 硬编码、边界耦合与 Mbar 均为外部输入；"
                  "Mbar 由 G 导出后 N∝1/G，双锚点退化为同一参数的重参数化。",
    },
    {
        "id": "V73-有限尺寸条件界（Yukawa 形状因子 + MICROSCOPE）",
        "C1": True, "C2": False, "C3": True, "C4": False,
        "reason": "球源形状因子通过独立二维积分检验（实现无关），条件 alpha 界可算；但界的换算依赖"
                  "实测 η 与玩具 Z/A 代理荷（台账 E060 自陈非普适源荷），且同卷并存两套地球几何口径，"
                  "使同一 λ 的界移动 18.33% ⇒ 理论与实验双锚点不自洽。",
    },
    {
        "id": "V73-三重反转 8 态（Walsh–Hadamard）",
        "C1": True, "C2": True, "C3": True, "C4": False,
        "reason": "设计矩阵正交性精确成立、无反解、无拟合，量纲与方差缩减均可复算；但 8 观测 / 8 参数"
                  "⇒ df=0 ⇒ 残差恒 0、无任何拟合优度检验，且对 3 阶（hrs 形）同形伪差的分离力精确为 0。"
                  "⇒ 「完全正交 ⇒ 可鉴出新力」这一双锚点不成立。",
    },
    {
        "id": "V73-无输入 G 的独立预测（台账 E076 开放项）",
        "C1": False, "C2": False, "C3": False, "C4": False,
        "reason": "该候选在库内没有输出物：C 段给出其价码=需 1.4e41 个场且 G 始终外部；"
                  "台账 E076 本身标 O（开放），本册不为其代做实现。",
    },
]
for gitem in W3_GATES:
    gitem["PASS"] = bool(gitem["C1"] and gitem["C2"] and gitem["C3"] and gitem["C4"])
W3_PASS = sum(1 for gitem in W3_GATES if gitem["PASS"])
guard("G_w3_zero_pass", W3_PASS == 0, "W3 四候选全部未过门，PASS=%d/4" % W3_PASS)

# W3 阳性对照：注入一个 C2=True 的候选 ⇒ 计数必须变化（证明 PASS=0 不是解析失败的假零）
W3_CTRL = [dict(g) for g in W3_GATES]
W3_CTRL[2]["C2"] = True
W3_CTRL[2]["PASS"] = bool(W3_CTRL[2]["C1"] and W3_CTRL[2]["C2"] and W3_CTRL[2]["C3"] and W3_CTRL[2]["C4"])
W3_CTRL_PASS = sum(1 for gitem in W3_CTRL if gitem["PASS"])
guard("G_w3_positive_control", W3_CTRL_PASS == W3_PASS + 1,
      "注入 C2=True 的阳性候选后 PASS 计数 %d -> %d（计数逻辑有牙，PASS=0 非假零）"
      % (W3_PASS, W3_CTRL_PASS))

add("W3-01", "FAIL", "W3 四门禁：四候选 0/4",
    "尺度生成（C2/C3/C4 败：纯逆算 + 外部输入 + G 重参数化）、有限尺寸条件界（C2/C4 败：实测 η 反解 + "
    "两套地球几何口径）、三重反转（C4 败：df=0 无检验力且对 3 阶同形伪差分离力=0）、"
    "无输入 G 预测（C1–C4 全败，无输出物）。⇒ W3/L3 不得新增计数")
add("W3-02", "PASS", "W3 门禁机器化并带阳性对照",
    "C1/C2/C3/C4 四列为可执行布尔；实测 PASS=%d/4；注入一个 C2=True 的阳性候选后 PASS 变为 %d/4 ⇒ "
    "计数逻辑有牙，0/4 是真读数而非解析失败造成的假零" % (W3_PASS, W3_CTRL_PASS))

# ---------------- 红线与继承口径 ----------------
REDLINES = {
    "UFT_goals": "0/6 未完成",
    "systems": "0/22 完成架构统一",
    "UFT3": "0（不能第一性独立给出四力耦合常量与量级）",
    "L3": "0（本轮不新增可证伪独立预言）",
    "validated": "0（无独立实验验证）",
    "four_force_correct_equation": "0 条（含引力的四力正确方程）",
    "L3_to_L4": "L3 不成立，L3→L4 禁止",
    "w3_pass": "0/4（本轮候选）",
    "redline": "数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确",
}
add("RED-01", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4；"
    "本轮只是把 ROOT V73 的尺度生成 / 有限尺寸 / 三重反转三条路线压为可复算判定，不增加任何 W3/L3 计数")

# ==================================================================
# 产物生成：JSON / 数据 md / report / 判定册
# ==================================================================
BASE_NAME = "TUFT-r430_ROOT_V73_尺度生成与三重反转_全维审计_2026-11-21"
VERDICT_NAME = "判定_TUFT-r430-ROOT_V73_尺度生成与三重反转_全维审计_2026-11-21.md"


def verdict_counts(rows):
    out = {}
    for row in rows:
        out[row["verdict"]] = out.get(row["verdict"], 0) + 1
    return out


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", "<br>")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


COUNTS = verdict_counts(ENTRIES)
SOURCE_PATH = os.path.abspath(__file__)
with open(SOURCE_PATH, "rb") as fh:
    SOURCE_SHA = hashlib.sha256(fh.read()).hexdigest()

with open(SOURCE_PATH, "r", encoding="utf-8") as fh:
    SOURCE_TEXT = fh.read()
PLACEHOLDER = chr(36) + "{"
guard("G_no_template_placeholder", PLACEHOLDER not in SOURCE_TEXT,
      "源码不得出现美元花括号占位符")
guard("G_entry_floor", len(ENTRIES) >= 30, "条目数 %d >= 30" % len(ENTRIES))
guard("G_guard_floor", len(GUARDS) >= 16, "守卫数 %d >= 16" % len(GUARDS))
guard("G_counts_sum", sum(COUNTS.values()) == len(ENTRIES),
      "条目计数闭合：%s" % COUNTS)

json_obj = {
    "meta": {
        "rid": RID,
        "stamp": STAMP,
        "title": "ROOT V73 尺度生成 / 有限尺寸条件界 / 三重反转 全维审计",
        "method": "纯标准库 Decimal 60 位 + Fraction 精确算术 + 四元量纲 (M,L,T,Q) + "
                  "阳性对照 + 独立二维 Simpson 积分 + W3 四门禁 + 幂等 SHA-256",
        "source_sha256": SOURCE_SHA,
        "verdict_counts": COUNTS,
        "entry_total": len(ENTRIES),
        "guard_total": len(GUARDS),
        "w3_pass": W3_PASS,
        "fact_source": os.path.relpath(FACT, ROOT).replace("\\", "/"),
        "fact_sha256": FACT_HASH,
    },
    "entries": ENTRIES,
    "guards": GUARDS,
    "w3_gate": W3_GATES,
    "redlines": REDLINES,
    "key_numbers": {
        "dim_rank_A": rank_A,
        "dim_rank_augmented": rank_aug_real,
        "dim_det_augmented": str(det_aug_real),
        "planck_mass_kg": sci(MP_KG, 16),
        "planck_mass_gev": sci(MP_GEV, 16),
        "planck_identity_residual": sci(IDENT_RESID),
        "rg_lambda_from_g": sci(LAMBDA_FROM_G, 16),
        "rg_roundtrip_residual": sci(RT_RESID),
        "rg_sensitivity": sci(SENS, 16),
        "g_uv_fitted": sci(G_UV_FITTED, 16),
        "species_count": sci(N_PKG, 16),
        "species_count_2G": sci(N_FROM_2G, 16),
        "shape_uniform_1e6": sci(U_1E6, 16),
        "shape_point_1e6": sci(P_1E6, 16),
        "shape_two_layer_1e6": sci(T_1E6, 16),
        "shape_ratio_over_point": sci(U_1E6 / P_1E6, 16),
        "shape_integral_rel_diff": sci(DIFF_YUK),
        "shape_integral_newton_kernel_rel_diff": sci(DIFF_NEWTON),
        "eta_95_limit": sci(ETA_LIMIT, 16),
        "alpha_bound_1e7": sci(ALPHA_1E7, 16),
        "bound_geometry_shift": sci(BOUND_SHIFT, 16),
        "noise_factor": sci(NOISE_FACTOR, 16),
        "bias_low_order_sum": str(LOW_ORDER_BIAS),
        "bias_third_order": str(THIRD_ORDER_BIAS),
        "resid_max_saturated_design": str(RESID_MAX),
        "df_model": DF_MODEL,
        "rank_same_signature": RANK_CONF,
        "cross_env_slope": str(SLOPE_FIT),
        "fact_json_max_rel_diff": (sci(JSON_MAX_REL) if JSON_MAX_REL is not None else None),
        "w3_pass": W3_PASS,
        "w3_pass_positive_control": W3_CTRL_PASS,
    },
}

json_path = os.path.join(DATA, BASE_NAME + ".json")
md_path = os.path.join(DATA, BASE_NAME + ".md")
report_path = os.path.join(DATA, BASE_NAME + "_report.txt")
verdict_path = os.path.join(os.path.dirname(HERE), VERDICT_NAME)

json_text = json.dumps(json_obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

entry_lines = [
    "| ID | 判定 | 标题 | 读数 |",
    "|---|---|---|---|",
]
for row in ENTRIES:
    entry_lines.append("| %s | %s | %s | %s |" %
                       (cell(row["id"]), cell(row["verdict"]), cell(row["title"]), cell(row["detail"])))

guard_lines = ["| ID | OK | 读数 |", "|---|---|---|"]
for row in GUARDS:
    guard_lines.append("| %s | %s | %s |" %
                       (cell(row["id"]), "PASS" if row["ok"] else "FAIL", cell(row["detail"])))

w3_lines = ["| 候选 | C1 | C2 | C3 | C4 | PASS | 理由 |", "|---|---|---|---|---|---|---|"]
for row in W3_GATES:
    w3_lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
        cell(row["id"]), row["C1"], row["C2"], row["C3"], row["C4"], row["PASS"], cell(row["reason"])))

counts_text = " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS))
hash_lines = ["- 事实源 `%s`" % os.path.relpath(FACT, ROOT).replace("\\", "/")]
for _name in sorted(FACT_HASH):
    hash_lines.append("  - `%s` SHA-256 `%s`" % (_name, FACT_HASH[_name]))
if not FACT_HASH:
    hash_lines.append("  - （事实源文件未找到，本册只报自算读数）")

md_text = "\n".join([
    "# r430 数据产物：ROOT V73 尺度生成 / 有限尺寸 / 三重反转 全维审计",
    "",
    "- 条目：%d（%s）" % (len(ENTRIES), counts_text),
    "- 守卫：%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "- W3 门禁：%d/4（阳性对照 %d/4）" % (W3_PASS, W3_CTRL_PASS),
    "- 源码 SHA-256：`%s`" % SOURCE_SHA,
    "- 判定册：[%s](../%s)" % (VERDICT_NAME, VERDICT_NAME),
    "- 引擎：[源码](%s)" % ("../源码/" + os.path.basename(SOURCE_PATH)),
    "",
    "## 事实源与哈希",
    "",
] + hash_lines + [
    "",
    "## 条目表",
    "",
] + entry_lines + [
    "",
    "## 守卫表",
    "",
] + guard_lines + [
    "",
    "## W3 门禁",
    "",
] + w3_lines + [
    "",
    "## 红线",
    "",
] + ["- %s：%s" % (k, v) for k, v in REDLINES.items()] + [""])

report_text = "\n".join([
    "r430 ROOT V73 尺度生成/有限尺寸/三重反转 全维审计",
    "================================================",
    "entries=%d" % len(ENTRIES),
    "counts=%s" % counts_text,
    "guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "w3_pass=%d/4" % W3_PASS,
    "w3_positive_control=%d/4" % W3_CTRL_PASS,
    "source_sha256=%s" % SOURCE_SHA,
    "dim_det_augmented=%s" % det_aug_real,
    "planck_mass_gev=%s" % sci(MP_GEV),
    "g_uv_fitted=%s" % sci(G_UV_FITTED),
    "species_count=%s" % sci(N_PKG),
    "shape_ratio_over_point=%s" % sci(U_1E6 / P_1E6),
    "alpha_bound_1e7=%s" % sci(ALPHA_1E7),
    "bound_geometry_shift=%s" % sci(BOUND_SHIFT),
    "noise_factor=%s" % sci(NOISE_FACTOR),
    "bias_third_order=%s" % THIRD_ORDER_BIAS,
    "rank_same_signature=%s" % RANK_CONF,
    "cross_env_slope=%s" % SLOPE_FIT,
    "redline=数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确",
])

verdict_text = "\n".join([
    "# 判定 r430：ROOT V73 尺度生成 / 有限尺寸条件界 / 三重反转 全维审计",
    "",
    "## 〇、一句话",
    "",
    "ROOT V73 的每一条数值都可以独立复算（本册 9 项关键读数与来料逐位一致），"
    "但复算的三条路线各自撞在自己的结构边界上：尺度生成是纯逆算且 G 始终外部输入"
    "（闭合需 1.4e41 个场）；有限尺寸界依赖实测 η 与玩具代理荷，同卷并存两套地球几何使界移动 18.33%；"
    "三重反转对 3 阶同形伪差的分离力精确为 0 且 df=0 无任何拟合优度检验。W3 四候选 0/4，"
    "L3/validated/UFT3 计数不变。",
    "",
    "## 一、产物",
    "",
    "| 顺序 | 文件 | 作用 |",
    "|---|---|---|",
    "| 0 | 本判定册 | 三段裁定 + W3 + 红线 |",
    "| 1 | [引擎](源码/%s) | %d 条目 / %d 守卫 / 纯标准库 |"
    % (os.path.basename(SOURCE_PATH), len(ENTRIES), len(GUARDS)),
    "| 2 | [数据 md](数据/%s) · [json](数据/%s) · [报告](数据/%s) | 机器读数留档 |"
    % (os.path.basename(md_path), os.path.basename(json_path), os.path.basename(report_path)),
    "",
    "## 二、条目与守卫",
    "",
    "条目 %d（%s），守卫 %d/%d，W3 %d/4（阳性对照 %d/4），源码 SHA-256 `%s`。"
    % (len(ENTRIES), counts_text, sum(1 for g in GUARDS if g["ok"]), len(GUARDS),
       W3_PASS, W3_CTRL_PASS, SOURCE_SHA),
    "",
    "### 事实源",
    "",
] + hash_lines + [
    "",
] + entry_lines + [
    "",
    "## 三、守卫表",
    "",
] + guard_lines + [
    "",
    "## 四、W3 门禁",
    "",
] + w3_lines + [
    "",
    "## 五、红线与边界",
    "",
] + ["- %s：%s" % (k, v) for k, v in REDLINES.items()] + [
    "",
    "本册不把计算复现、W3 C1 定量、程序守卫通过解释为新物理；不修改 ROOT V73 原文任何字节，"
    "不覆盖并发会话文件；本册的 FAIL 全部落在来料自陈的限制之内（台账 E013/E021/E031/E060/E071、"
    "候选矩阵第 2/6/24/25/26/27 行），属边界定价而非新发现。",
    "",
])

write_text(json_path, json_text)
write_text(md_path, md_text)
write_text(report_path, report_text)
write_text(verdict_path, verdict_text)

with open(json_path, "r", encoding="utf-8") as fh:
    reread = fh.read()
if reread != json_text:
    raise AssertionError("JSON idempotence failed")
for p in (md_path, report_path, verdict_path):
    if os.path.getsize(p) <= 200:
        raise AssertionError("Empty output: %s" % os.path.basename(p))


def main():
    print("r430 entries=%d counts=%s" % (len(ENTRIES), counts_text))
    print("r430 guards=%d/%d w3=%d/4 (ctrl=%d/4)" %
          (sum(1 for g in GUARDS if g["ok"]), len(GUARDS), W3_PASS, W3_CTRL_PASS))
    print("r430 json=%s" % json_path)
    print("r430 verdict=%s" % verdict_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
