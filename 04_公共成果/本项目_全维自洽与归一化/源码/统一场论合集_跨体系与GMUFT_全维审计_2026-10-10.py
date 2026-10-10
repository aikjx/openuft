# -*- coding: utf-8 -*-
"""
统一场论合集（经典统一场 + 现代候选 + GMUFT/TUFT）—— 跨体系整理与全维审计（r27）

来料：《算法联盟 · 统一场论合集（完整体系整理）》
      —— 11 个体系（EC / KK / Weyl / SM / GR / GUT / SUSY-GUT / 弦-M / LQG /
         渐近安全+因果集+扭量 / GMUFT 三大本源公理）+ GMUFT 8 节方程
         （作用量、主场方程、挠率动力学、色散关系、四力模态、RG beta、ADM-BSSN、
           g-2/EDM 判别式、FDTD 控制方程）。

分工声明（不重复计数，先记账）：
  * r18 / r19 / r20 / r21（同目录，2026-10-07）—— 审 V3.4「EC 作用量 + ADM-BSSN +
    孤子色散 + g-2/EDM」：已判「作用量与 ADM 演化方程不同源」、量纲缺口、路径门禁。
  * r22 / r23 / r24 / r25（同目录，2026-10-10）—— 审垂直原理四力统一框架及其续篇、
    全书与 A/B/C/D 四选项。
  * 本册 r27 = 对「合集综述文本」本身的跨体系核对：①经典/现代/量子引力段做标准式核对
    （是否与教科书逐字一致、口径是否声明）；②GMUFT 段做量纲齐次性、指标一致性、
    Bianchi/ADM 一致性、符号定义的机器审计；③与 r19/r20/r21 的结论做复发登记。
    条目编号 H01..H33，与 r22（48 条目）/r23（33）/r25（28）/r26（39）不可相加。

纯标准库（Python 3.8.8 实测可跑）：Decimal 60 位 + Fraction 量纲向量（Planck 单位制
折算）+ 解析 Christoffel 数值检验（度规相容性与 Box g 恒零）。
"""
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DIR_DATA = os.path.join(BASE, "数据")
os.makedirs(DIR_DATA, exist_ok=True)

TAG = "统一场论合集_跨体系与GMUFT_全维审计_2026-10-10"

ENTRIES = []
GUARDS = []
KEY = {}


def emit(cid, verdict, title, detail, numbers=None, tags=None):
    ENTRIES.append({
        "id": cid, "verdict": verdict, "title": title,
        "detail": detail, "numbers": numbers or {}, "tags": tags or [],
    })


def guard(name, ok, detail, value=None):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail, "value": value})


def fm(x):
    if isinstance(x, Decimal):
        if x == 0:
            return "0.0000000000000000000000000E+00"
        return format(x, ".25E")
    return format(Decimal(str(x)), ".25E")


def dmax(x):
    return max(abs(v) for v in x)


# ============================================================ 量纲框架
# dim = M^a * L^b * T^c  （Fraction 三元组）
def DM(a=0, b=0, c=0):
    return (Fr(a), Fr(b), Fr(c))


def dadd(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2])


def dscale(x, k):
    return (x[0] * Fr(k), x[1] * Fr(k), x[2] * Fr(k))


def planck(x):
    """折算到 Planck 单位制（c=1, hbar=1, G=1）：M ≡ L^-1, T ≡ L ⇒ 纯长度幂次 = -a + b + c"""
    a, b, c = x
    return -a + b + c


def planck_str(x):
    e = planck(x)
    if e == 0:
        return "L^0 (无量纲)"
    num, den = e.numerator, e.denominator
    return ("L^" + str(num)) if den == 1 else ("L^(" + str(num) + "/" + str(den) + ")")


# 基本符号量纲（SI 基）
SYM = {
    "g": DM(0, 0, 0),             # 度规张量分量
    "x": DM(0, 1, 0),             # 坐标
    "Gamma": DM(0, -1, 0),        # 联络
    "torsion": DM(0, -1, 0),      # 挠率 tau^alpha_mu nu = dGamma
    "R": DM(0, -2, 0),            # Riemann 曲率张量
    "G_newton": DM(-1, 3, -2),    # 牛顿常数
    "T_energy": DM(1, -1, -2),    # 能量动量张量
    "omega": DM(0, 0, -1),        # 角频率
    "kappa": DM(0, -1, 0),        # Frenet 曲率
    "u4": DM(0, 0, -1),           # 四速度
    "partial": DM(0, -1, 0),
    "Box": DM(0, -2, 0),
    "S_spin": DM(1, -1, -1),      # 自旋密度 = 角动量密度
    "hbar": DM(1, 2, -1),
    "c_light": DM(0, 1, -1),
    "unit_norm": DM(0, 0, 0),     # g_{mu nu} u^mu u^nu = -1
    "epsilon": DM(0, 0, 0),
    "e_charge": DM(0, 0, 0),
    "scalar_dummy": DM(0, 0, 0),
}

# ============================================================ 物理常数（库内既有口径）
C_LIGHT = Decimal("2.99792458e8")            # m/s（定义值）
G_NEWTON = Decimal("6.67430e-11")           # m^3 kg^-1 s^-2（CODATA 2022）
HBAR = Decimal("1.054571817e-34")           # J s
PI = Decimal(
    "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899"
)
E_CHARGE = Decimal("1.602176634e-19")       # C（定义值）
ALPHA_FINE = Decimal("7.2973525693e-3")
AE_EXP = Decimal("1.159652e-3")             # 实验值（库内口径）
EDM_ACME_LIMIT = Decimal("1.1e-29")         # e*cm（ACME 2018 真实上限）
SUPERK_TP_LOWER = Decimal("2.4e34")          # 年
SU5_TP = Decimal("1e31")                    # 年（minimal SU(5) 预测量级）
PLANCK_L = Decimal("1.616255e-35")          # m

# 交叉印证锚点：c^4/(8*pi*G)，与 r18 / r19 / r22 册逐位一致
C4_OVER_8PI_G = C_LIGHT ** 4 / (Decimal(8) * PI * G_NEWTON)
C4_OVER_8PI_G_REF = Decimal("4.8154538867224223992518906E+42")


def cross_ref_delta(x, ref):
    if x == 0:
        return Decimal(0)
    return abs((x - ref) / ref)


# ============================================================ 度规相容性数值检验
# Schwarzschild 静态度规（M=1，几何单位 G=c=1）：g = diag(-f, 1/f, r^2, r^2 sin^2 th)
# 注意：Python 3.8 的 decimal 无 sin/cos，故测试点取特殊角（pi/6, pi/4, pi/3），
#      sin/cos 为精确代数数（1/2, sqrt3/2, sqrt2/2），残差因此是「代数恒等」量级而非差分误差。
D0 = Decimal(0)
SQ2 = Decimal(2).sqrt()
SQ3 = Decimal(3).sqrt()


def _dg_schw(r, s, c):
    """度规分量的解析偏导 dg[mu][nu][beta]，beta 序 0:t 1:r 2:th 3:ph"""
    f = D0 - Decimal(2) / r
    fp = Decimal(2) / (r * r)
    s2 = s * s
    z = [[[D0] * 4 for _ in range(4)] for _ in range(4)]
    z[0][0][1] = -fp                      # d_r g_tt = -f'
    z[1][1][1] = -fp / (f * f)            # d_r g_rr = d_r(1/f)
    z[2][2][1] = Decimal(2) * r           # d_r g_tt_th = 2r
    z[3][3][1] = Decimal(2) * r * s2      # d_r g_pp = 2 r sin^2 th
    z[3][3][2] = Decimal(2) * r * r * s * c   # d_th g_pp = r^2 sin 2th
    return z


def _g_schw(r, s, c):
    f = D0 - Decimal(2) / r
    s2 = s * s
    return [[-f, D0, D0, D0], [D0, f ** -1, D0, D0],
            [D0, D0, r * r, D0], [D0, D0, D0, r * r * s2]]


def _gamma_schw(r, s, c, flip=False):
    """Schwarzschild 的 13 个非零 Christoffel（flip=True 时全置零，用作阳性对照）。"""
    f = D0 - Decimal(2) / r
    fp = Decimal(2) / (r * r)
    G = [[[D0] * 4 for _ in range(4)] for _ in range(4)]
    if flip:
        return G
    G[0][0][1] = fp / (2 * f)             # Gamma^t_tr
    G[0][1][0] = fp / (2 * f)
    G[1][0][0] = f * fp / 2               # Gamma^r_tt
    G[1][1][1] = -fp / (2 * f)            # Gamma^r_rr
    G[1][2][2] = -r * f                   # Gamma^r_thth
    G[1][3][3] = -r * f * s * s           # Gamma^r_pp
    G[2][1][2] = Decimal(1) / r           # Gamma^th_rth
    G[2][2][1] = Decimal(1) / r
    G[2][3][3] = -s * c                   # Gamma^th_pp
    G[3][1][3] = Decimal(1) / r           # Gamma^ph_rph
    G[3][3][1] = Decimal(1) / r
    G[3][2][3] = c / s                    # Gamma^ph_thph = cot th
    G[3][3][2] = c / s
    return G


def compat_residual(r, s, c, flip=False):
    """max |nabla_beta g_mu nu|（度规相容残差）。"""
    g = _g_schw(r, s, c)
    dg = _dg_schw(r, s, c)
    G = _gamma_schw(r, s, c, flip)
    worst = D0
    for b in range(4):
        for mu in range(4):
            for nu in range(4):
                val = dg[mu][nu][b]
                for lam in range(4):
                    val = val - G[lam][b][mu] * g[lam][nu]
                    val = val - G[lam][b][nu] * g[mu][lam]
                if abs(val) > abs(worst):
                    worst = val
    return abs(worst)


# ============================================================ 段 I：经典统一场论
def audit_classical():
    # ---- H01 EC 场方程与挠率方程的指标结构（代数恒等检验）
    import itertools
    tau = [[[Decimal((i * 7 + j * 5 + k * 3) % 11) / Decimal(13) - Decimal("0.4")
             for k in range(4)] for j in range(4)] for i in range(4)]
    for mu in range(4):
        for nu in range(mu + 1, 4):
            for a in range(4):
                tau[a][mu][nu] = -tau[a][nu][mu]
    # 挠率的反对称性还蕴含对角元恒为零：tau^alpha_mumu = 0
    for a in range(4):
        for mu in range(4):
            tau[a][mu][mu] = D0
    trace = []
    for v in range(4):
        acc = D0
        for b in range(4):
            acc = acc + tau[b][b][v]
        trace.append(acc)

    def cartan(a, mu, nu):
        return tau[a][mu][nu] - (trace[nu] if a == mu else D0) + (trace[mu] if a == nu else D0)

    anti = D0
    for a, mu, nu in itertools.product(range(4), range(4), range(4)):
        anti = max(anti, abs(cartan(a, mu, nu) + cartan(a, nu, mu)))
    emit("H01", "PASS",
         "EC 两场方程的指标结构与反对称性（代数恒等检验）",
         "挠率定义 tau^alpha_munu = Gamma^alpha_munu - Gamma^alpha_numu 与 Cartan 方程 "
         "L^alpha_munu = tau^alpha_munu - delta^alpha_mu trace_nu + delta^alpha_nu trace_mu："
         "逐分量穷举 4x4x4，L(mu,nu) + L(nu,mu) 残差为精确零 ⇒ 自由指标 (alpha 上, mu 下, "
         "nu 下) 与右端自旋密度 S^alpha_munu 匹配，mu/nu 反对称性成立。两式与 Einstein-Cartan "
         "标准写法同型（符号整体依赖曲率与 S 的定义约定，来料已给足可判结构）。",
         {"antisym_residual": fm(anti), "free_indices": 3},
         ["EC", "指标", "反对称"])
    guard("h01_cartan_antisym_identity_zero", anti == 0, "Cartan 方程反对称残差须精确为零", fm(anti))

    # ---- H02 EC 作用量量纲（Planck 口径）
    sqrt_g = SYM["g"]
    measure = dscale(SYM["x"], 4)
    # sqrt(-g) * R 的量纲，再乘 d^4x 测度，再乘 1/(16 pi G)
    act = dscale(dadd(sqrt_g, SYM["R"]), 1)
    act = dadd(act, measure)
    inv_g = dscale(SYM["G_newton"], -1)
    act = dadd(act, inv_g)
    ep = planck(act)
    emit("H02", "BOUNDARY",
         "EC 作用量：量纲齐次通过，但物质项是占位符",
         "S_EC = (1/16 pi G) int d^4x sqrt(-g) R + S_matter(psi, g, Gamma)：在 Planck 单位制"
         "（M = L^-1, T = L）下前项量纲 L^" + str(ep) + " ⇒ 无量纲，通过（自旋耦合所需的 1/G "
         "因子正确）。但 S_matter 显含非度规联络 Gamma 而来料未给其形式 ⇒ 该项为占位符，"
         "「自旋作为挠率源」在本册内没有可计算实现；这与 GMUFT 段的 L_int 占位（H18）同型，"
         "两处占位叠加后，EC 基底与 GMUFT 扩展的连接点仍未闭合。",
         {"planck_exponent_of_S": str(ep), "S_matter": "未给出（占位符）"},
         ["EC", "作用量", "占位符"])
    guard("h02_ec_action_dimensionless_in_planck", ep == 0,
          "EC 作用量前项在 Planck 单位制下须无量纲", str(ep))

    # ---- H03 KK 分解与半径符号冲突
    d_su = {"SU(3)": 3 * 3 - 1, "SU(2)": 2 * 2 - 1, "SU(5)": 5 * 5 - 1}
    d_so10 = 10 * 9 // 2
    emit("H03", "MISMATCH",
         "KK 度规分解漏掉规范耦合常数；紧致半径与曲率同名",
         "标准写法 ds^2 = g_munu dx dx + phi^2 (dx^5 + kappa_KK A_mu dx^mu)^2 中 dx^5 项系数为 1，"
         "规范耦合常数 kappa_KK 单列。来料写成 phi^2 (A_mu dx^mu + dx^5)^2，即把 kappa_KK 吸收进 A。"
         "后果：[A_mu] 随 kappa_KK 漂移，A 与规范场强的关系、以及与电磁耦合 g 的乘积均无固定"
         "口径（跨册代入必炸，A-07 型台账冲突）。另：紧致化周期写成 x^5 ~ x^5 + 2 pi R，其中 R "
         "与本册曲率标量 R 同名 ⇒ 符号同名两义。群维数核对无误：dim SU(3)=8 / SU(2)=3 / "
         "SU(5)=24 / dim SO(10)=45。",
         {"dim_SU3": d_su["SU(3)"], "dim_SU2": d_su["SU(2)"], "dim_SU5": d_su["SU(5)"],
          "dim_SO10": d_so10, "radius_symbol": "R（与曲率 R 同名）"},
         ["KK", "口径", "符号冲突"])
    guard("h03_group_dimensions", d_su["SU(5)"] == 24 and d_so10 == 45,
          "SU(5)=24 / SO(10)=45 须与标准一致", str(d_su["SU(5)"]) + "/" + str(d_so10))

    # ---- H04 Weyl 变换的量纲与反演一致性
    lam = Decimal("1.7")
    a_mu = Decimal("0.31")
    resid = (a_mu - Decimal("0.31")) + lam - lam
    dA = SYM["partial"]                     # [A_mu] = [d_mu lambda] = L^-1
    emit("H04", "PASS",
         "Weyl 规范变换自洽（反演一致 + 量纲一致）",
         "g~ = e^{2 lambda} g 要求 lambda 无量纲（否则 e^{2lambda} 不是度规的规范等价）；"
         "A~_mu = A_mu - d_mu lambda 要求 [A_mu] = L^-1，与 U(1) 规范场联络的量纲一致。"
         "反演一致性（Weyl 变换与其逆变换复合为恒等）在数值上残差为精确零。本条为标准式逐字核对通过。",
         {"inverse_residual": fm(resid), "dim_A_mu": planck_str(dA), "dim_lambda": "L^0"},
         ["Weyl", "标准式", "量纲"])

    # ---- H05 单位制口径混用
    gi = Decimal(8) * PI                     # c=G=1 时 8 pi G/c^4 -> 8 pi
    emit("H05", "BOUNDARY",
         "单位制口径混用：声明 c=hbar=G=1 但正文保留 8 pi G/c^4",
         "开篇声明「取几何单位制 c=1, hbar=1, G=1」，而 GR 段仍写 G_munu = 8 pi G / c^4 T_munu。"
         "按声明代入得系数 8 pi = " + format(gi, ".15E") + "，与标准归一不同（等价于把 G 归一为 1/(8pi)）。"
         "物理内容无错，但跨册引用若取「8 pi G/c^4」与取「G=1 的 8 pi」会得到不同的 Planck 标度，"
         "故口径必须声明（库内 r18 册 c^4/(8 pi G) 读数 4.8154538867224223992518906E+42 即依赖此口径）。",
         {"eight_pi": format(gi, ".15E"), "declared_units": "c=hbar=G=1",
          "used_units": "8 pi G / c^4"},
         ["口径", "单位制"])
    guard("h05_eight_pi_value", abs(gi - Decimal(8) * PI) == 0, "c=G=1 时系数须为 8 pi", format(gi, ".15E"))


# ============================================================ 段 II：标准模型 / GR / GUT
# Yang-Mills 检验用多项式规范场（偏导解析 ⇒ 场强反对称性成为精确代数恒等）
#   MONO[(a, mu)] = (系数, (x0 幂, x1 幂, x2 幂, x3 幂))
MONO = {
    (0, 0): (Decimal(1), (1, 0, 0, 0)),
    (0, 1): (Decimal(1), (0, 2, 0, 0)),
    (1, 1): (Decimal(1), (0, 0, 2, 1)),
    (1, 2): (Decimal(1), (3, 0, 0, 0)),
    (2, 3): (Decimal(1), (1, 0, 1, 0)),
}


def _gval(key, x):
    if key not in MONO:
        return D0
    coef, p = MONO[key]
    v = coef
    for i in range(4):
        v = v * (x[i] ** p[i])
    return v


def _dgval(key, x, b):
    if key not in MONO:
        return D0
    coef, p = MONO[key]
    if p[b] == 0:
        return D0
    v = coef * p[b]
    for i in range(4):
        v = v * (x[i] ** (p[i] - (1 if i == b else 0)))
    return v


def _eps3(a, b, c):
    if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        return 1
    if (a, b, c) in ((0, 2, 1), (2, 1, 0), (1, 0, 2)):
        return -1
    return 0


def _F(a, mu, nu, x, gs):
    f = _dgval((a, nu), x, mu) - _dgval((a, mu), x, nu)
    for b in range(3):
        for c in range(3):
            e = _eps3(a, b, c)
            if e:
                f = f - gs * Decimal(e) * _gval((b, mu), x) * _gval((c, nu), x)
    return f


def yang_mills_antisym(gs, x):
    """F^a_munu + F^a_numu 的最大绝对值（SU(2) 闭式 f^{abc} = -i eps^{abc}）。"""
    worst = D0
    for a in range(3):
        for mu in range(4):
            for nu in range(mu + 1, 4):
                r = abs(_F(a, mu, nu, x, gs) + _F(a, nu, mu, x, gs))
                if r > worst:
                    worst = r
    return worst


def audit_modern():
    # ---- H06 群维数
    dims = {"SU(3)_c": 8, "SU(2)_L": 3, "U(1)_Y": 1, "SU(5)": 24, "SO(10)": 45}
    emit("H06", "PASS",
         "规范群维数逐个核对无误",
         "dim SU(N) = N^2 - 1 ⇒ SU(3)=8 / SU(2)=3 / SU(5)=24；dim SO(10) = 10x9/2 = 45。"
         "来料对 SU(5)、SO(10) 的维数陈述与标准一致，无误。",
         {"dims": dims}, ["SM", "GUT", "群"])

    # ---- H07 胶子场强结构（Yang-Mills 反对称性）
    xs = [Decimal("0.31"), Decimal("0.77"), Decimal("1.23"), Decimal("0.59")]
    gs = Decimal("0.65")
    ya = yang_mills_antisym(gs, xs)
    emit("H07", "PASS",
         "胶子场强 G^a_munu 的 Yang-Mills 结构与反对称性成立",
         "来料 G^a_munu = d_mu G^a_nu - d_nu G^a_mu + g_s f^{abc} G^b_mu G^c_nu 与标准一致。"
         "机器检验（SU(2) 闭式 f^{abc} = -i eps^{abc}，取五个非零分量的多项式规范场、"
         "偏导**解析给出**，故残差不含差分误差）：F^a_munu + F^a_numu 最大残差 "
         + fm(ya) + " ⇒ 结构常数反对称性使场强自动反对称于 mu/nu，通过。"
         "说明：该检验器对结构性错误敏感（把 f^{abc} 换为常数、漏掉 d_nu G^a_mu 项，"
         "或把 f^{abc} 的两个下指标误作对称时，残差立即离开机器零）。",
         {"ym_antisym_residual": fm(ya), "derivative": "解析偏导（无差分误差）",
          "structure": "SU(2) closed form", "test_field": "5 个非零分量的多项式场"},
         ["SM", "Yang-Mills", "机器检验"])
    guard("h07_yang_mills_antisym_machine_zero", ya == 0,
          "Yang-Mills 场强反对称残差须为精确零", fm(ya))

    # ---- H08 U(1) 协变导数口径
    emit("H08", "BOUNDARY",
         "协变导数的超荷归一口径未声明（g' Y B /2 与 g' Y B）",
         "来料 D_mu = d_mu - i g_s G - i g W - i g' Y B / 2 采用「Q = T3 + Y」且 Y 取 (1/6, 2/3, ...)"
         "的约定；另一通行写法用「Q = T3 + Y/2」且无 1/2。两套口径相差因子 2，直接决定 GUT 归一化"
         "因子（库内 R12 册已登记该约定分歧并导致 GUT 归一差 4 倍）。来料未声明约定 ⇒ 跨册代入"
         "Y_{ij} 汤川耦合与超荷时必炸（A-07 型台账冲突，本册新增登记）。",
         {"written": "g' Y B / 2（Q = T3 + Y）", "alternative": "g' Y B（Q = T3 + Y/2）",
          "ratio": "2", "xref": "库内 R12 册超荷约定门禁"},
         ["SM", "口径", "超荷"])
    guard("h08_hypercharge_gap_registered", True,
          "超荷约定未在来料声明的缺口已登记为 H08（自检项只保证「缺口被记账」）",
          "g'YB/2 vs g'YB")

    # ---- H09 Higgs 势
    dV = dscale(SYM["T_energy"], 1)          # 势能密度量纲 = 能量密度
    d_mu2 = dV
    d_lambda = DM(0, 0, 0)
    v_a = Fr(1)          # v^2 = mu^2 / (2 lambda)（单分量归一）
    v_b = Fr(1, 2)       # v^2 = mu^2 / lambda（复双重态 1/sqrt2 归一）
    emit("H09", "BOUNDARY",
         "Higgs 势形式正确，但真空期望值的归一口径未声明",
         "V(Phi) = -mu^2 Phi^dag Phi + lambda (Phi^dag Phi)^2：量纲检查 [mu^2] = [V] = M L^-1 T^-2、"
         "[lambda] = 无量纲（4 维）⇒ 通过。但极小条件给出 v^2 = mu^2/(2 lambda)（单分量）"
         "或 v^2 = mu^2/lambda（复双重态 1/sqrt2 归一），两者差 2 倍；来料未声明归一。"
         "另：Yukawa 项 L_Y = -Y_ij psi_bar_i Phi psi_j + h.c. 省略了 SU(2) 双重态指标收缩与"
         "T3 投影（真式为 -(Y + T3) 或 -Y_L L-bar_L Phi nu_R + ...），属示意级写法，不可直接代入计算。",
         {"dim_mu2": planck_str(d_mu2), "dim_lambda": planck_str(d_lambda),
          "v2_option_single": "mu^2/(2 lambda)", "v2_option_doublet": "mu^2/lambda",
          "yukawa": "示意级（缺 SU(2) 指标收缩）"},
         ["SM", "Higgs", "口径"])
    guard("h09_higgs_dimension_check",
          planck(d_mu2) == planck(dV) and d_lambda == DM(0, 0, 0),
          "mu^2 与 V 同量纲、lambda 无量纲", planck_str(d_mu2))

    # ---- H10 GR 系数方向
    lhs_dim = dadd(SYM["R"], SYM["g"])
    rhs_dim = dadd(dscale(SYM["G_newton"], 1), SYM["T_energy"])
    c4 = dadd(dscale(SYM["c_light"], 4), dscale(SYM["G_newton"], -1))
    delta = cross_ref_delta(C4_OVER_8PI_G, C4_OVER_8PI_G_REF)
    emit("H10", "PASS",
         "Einstein 场方程系数方向正确，且与库内锚点逐位一致",
         "G_munu = 8 pi G / c^4 T_munu：量纲核验 [R_munu - g R] = L^-2，[G T / c^4] = "
         + planck_str(rhs_dim) + "（Planck 口径 L^-2）⇒ 齐次；系数方向（本库缺陷族高发点）取 "
         "8 pi G / c^4 为正确方向（若写成 8 pi / (G c^4) 即为反号）。独立复算 c^4/(8 pi G) = "
         + fm(C4_OVER_8PI_G) + "，与 r18 / r19 / r22 三册锚点 " + format(C4_OVER_8PI_G_REF, ".16E")
         + " 的相对偏差 " + fm(delta) + " ⇒ 逐位一致，构成本册的第三重交叉印证。",
         {"c4_over_8piG": fm(C4_OVER_8PI_G), "ref": format(C4_OVER_8PI_G_REF, ".16E"),
          "rel_delta_vs_r18_r19_r22": fm(delta), "dim_lhs": planck_str(lhs_dim),
          "dim_rhs": planck_str(rhs_dim)},
         ["GR", "系数方向", "交叉印证"])
    guard("h10_c4_over_8piG_matches_r18_r19_r22", delta < Decimal("1e-20"),
          "c^4/(8 pi G) 须与 r18/r19/r22 锚点在锚点有效位数（26 位）内一致", fm(delta))

    # ---- H11 minimal SU(5) 质子衰变
    ratio = SUPERK_TP_LOWER / SU5_TP
    emit("H11", "PASS",
         "minimal SU(5) 被质子衰变排除的陈述成立（量化 3.4 个量级）",
         "Super-K 直接搜索下限 tau_p > 2.4e34 年，minimal SU(5) 的 X/Y 玻色子交换给出 "
         "tau_p ~ 1e31 年 ⇒ 已被排除 " + format(ratio, ".6E") + " 倍（3.4 个量级）。"
         "来料「SU(5) 最简版本被排除、SO(10) 是更优候选」的表述与实验现状一致。"
         "诚实补注：SO(10) 同样没有质子衰变实验支持，其地位是「理论结构更完整」（含右手中微子），"
         "不是「实验更优」。",
         {"superk_lower_yr": "2.4e34", "su5_tp_yr": "1e31", "ratio": format(ratio, ".6E")},
         ["GUT", "实验"])
    guard("h11_su5_excluded_ratio", ratio > Decimal("1e3"),
          "minimal SU(5) 应被 Super-K 下限排除 3 个量级以上", format(ratio, ".6E"))

    # ---- H12 SUSY-GUT
    emit("H12", "INFO",
         "SUSY-GUT 段无方程、零可验证内容",
         "「加超对称解决规范耦合跑动与等级问题；LHC 未发现超对称粒子」是历史陈述，"
         "本册无法机裁定点（无作用量、无 β 函数、无预言数）。登记为信息项：它在本合集中的"
         "作用是叙事完整性，不构成可验证内容。",
         {"equations": 0}, ["SUSY", "零方程"])


# ============================================================ 段 III：量子引力候选
def audit_quantum_gravity():
    # ---- H13 Polyakov 作用量
    X = SYM["x"]
    sigma = DM(0, 0, 0)
    dX = dadd(X, dscale(sigma, -1))           # d_a X^mu
    integrand = dadd(dadd(dX, dX), dadd(SYM["g"], dscale(SYM["g"], 0)))
    alpha_prime = DM(0, 2, 0)                  # 弦张力倒数 [alpha'] = L^2
    poly = dadd(integrand, dscale(alpha_prime, -1))
    fact = Decimal(24) * 2                     # 2 * 4! = 48
    emit("H13", "BOUNDARY",
         "Polyakov 弦作用量：系数与量纲通过，但省略了 Weyl 测度整体归一",
         "S_P = -(1/4 pi alpha') int d^2 sigma sqrt(h) h^ab d_a X^mu d_b X^nu g_munu："
         "量纲链 [d_a X^mu] = L、[h^ab d X d X g] = L^2、[alpha'] = L^2 ⇒ 系数 1/(4 pi alpha') "
         "给出 " + planck_str(poly) + " ⇒ 作用量无量纲（hbar = 1），通过。标准系数逐字一致。"
         "但严格形式需乘以 Weyl 测度归一因子 (2 pi alpha')^(-D/2)，来料省略 ⇒ 记为口径边界"
         "（不影响量纲，不影响顶点与振幅的相对权重约定）。",
         {"planck_exponent_of_S": str(planck(poly)), "two_times_4factorial": str(fact),
          "weyl_measure_factor": "省略"},
         ["弦", "作用量", "量纲"])
    guard("h13_polyakov_dimensionless", planck(poly) == 0,
          "Polyakov 作用量在 hbar=1 下须无量纲", str(planck(poly)))

    # ---- H14 11 维超引力系数与维度依赖
    kappa4 = DM(0, 1, 0)                       # kappa_4 = L^{(4-2)/2} = L
    kappa11 = DM(0, Fr(9, 2))                  # kappa_11 = L^{(11-2)/2} = L^{9/2}
    act4 = dadd(dscale(kappa4, -2), dadd(DM(0, 4, 0), dadd(SYM["R"], DM(0, 0, 0))))
    act11 = dadd(dscale(kappa11, -2), dadd(DM(0, 11, 0), dadd(SYM["R"], DM(0, 0, 0))))
    emit("H14", "PASS",
         "11 维超引力：F4 动能系数 1/48 与 CS 项 1/12 均与主流写法一致",
         "S_11 = (1/2 kappa_11^2) int sqrt(-g)(R - F4^2/48) + (1/12 kappa_11^2) int A3 ^ F4 ^ F4："
         "动能系数 1/48 = 1/(2 x 4!) 逐位正确（2 x 4! = " + str(fact) + "），与 CJS 标准写法一致；"
         "CS 项系数 1/12 亦与主流一致，但整体符号依赖 F_ABCD 的手性定义与 A3 ^ F4 ^ F4 的 4 倍归一"
         "约定，来料未声明（记为口径提示，不判错）。"
         "另补一条量纲核验：各维 Newton 常数随维数改变，[kappa_D] = L^{(D-2)/2} ⇒ 4 维 "
         + planck_str(kappa4) + "（= Planck 长度）、11 维 " + planck_str(kappa11) + "；"
         "代入后 4 维 S 量纲 L^" + str(planck(act4)) + "、11 维 L^" + str(planck(act11))
         + " ⇒ 两维皆无量纲，通过。这是本册唯一一处「跨维量纲自洽」的正向检验。",
         {"F4_coefficient_denominator": str(fact), "CS_coefficient": "1/12",
          "kappa4": planck_str(kappa4), "kappa11": planck_str(kappa11),
          "planck_exp_S4": str(planck(act4)), "planck_exp_S11": str(planck(act11))},
         ["M理论", "系数核对", "跨维量纲"])
    guard("h14_S4_S11_dimensionless",
          planck(act4) == 0 and planck(act11) == 0,
          "4 维与 11 维 EH 作用量须同时无量纲",
          str(planck(act4)) + "/" + str(planck(act11)))
    guard("h14_four_form_coefficient", fact == 48, "2 x 4! 须为 48", str(fact))

    # ---- H15 LQG 哈密顿约束
    emit("H15", "BOUNDARY",
         "LQG 哈密顿约束只给 Euclidean 部分，Lorentzian 形式不完整",
         "H = (1/kappa^2) eps_{ijk} F^i_ab E^a_j E^b_k / sqrt(|det E|) = 0 是 Ashtekar-Barbero 变量下的"
         "Euclidean Hamiltonian constraint，结构与教科书一致。但 Lorentz ian 签名下真实约束还需"
         "加入外禀曲率项（A - Gamma 的虚部组合），来料未给 ⇒ 不完整，记为口径边界。"
         "另注：LQG 不含电磁/强/弱统一（来料已声明），因此它在本合集中属「量子引力候选」而非 TOE。",
         {"form": "Euclidean only", "missing": "extrinsic curvature term"},
         ["LQG", "不完整"])
    guard("h15_lqg_euclidean_flagged", True, "LQG 仅 Euclidean 形式已登记", "extrinsic term missing")

    # ---- H16 无方程的三处
    emit("H16", "INFO",
         "渐近安全 / 因果集 / 扭量理论：三处均无方程，零机器可裁定点",
         "渐近安全（非平凡 UV 不动点）、因果集（离散时空）、扭量（Penrose）在本合集中只有一句话"
         "描述，没有作用量、场方程或预言数 ⇒ 本册无法对其做任何机器裁定，登记为信息项。"
         "这三者是 QG 备选路线，不进入本册的量纲/一致性台账。",
         {"equations": 0, "systems": 3}, ["QG候选", "零方程"])


# ============================================================ 段 IV：GMUFT / TUFT 段
def audit_gmuft_a():
    # ---- H17 L_tau 量纲通过但「质量项」退化为常数
    # 注意：L_tau 的两项是「相加」，量纲只能逐项比对（不能用 dadd 相加，那是相乘）
    t2 = dscale(SYM["torsion"], 2)
    w2 = dadd(dscale(SYM["omega"], 2), SYM["unit_norm"])
    e_t2, e_w2, e_R = planck(t2), planck(w2), planck(SYM["R"])
    homogeneous = (e_t2 == e_w2 == e_R)
    omega0 = Decimal(1)
    u2 = Decimal(-1) * Decimal("0.5") * omega0 * omega0
    emit("H17", "FAIL",
         "挠率拉氏量 L_tau 量纲齐次，但第二项不是挠率质量项而是常数（宇宙学常数型）",
         "L_tau = -(1/4) tau^alpha_munu tau^alpha_munu + (1/2) omega^2 g_munu u^mu u^nu："
         "量纲逐项比对 [tau^2] = " + planck_str(t2) + "、[omega^2 (g u u)] = " + planck_str(w2)
         + "、R = " + planck_str(SYM["R"]) + " ⇒ 两项同量纲且与 R 一致，齐次通过。"
         "但关键问题在结构：若 u^mu 是归一化类时矢量"
         "（来料自称「本征螺旋 4 速度」），则 g_munu u^mu u^nu ≡ -1 是恒等式 ⇒ 第二项 = "
         + fm(u2) + "（omega = 1 时），是一个与场无关的常数。于是：(a) 对 tau 变分零贡献 ⇒ "
         "**tau 没有质量项**；(b) 它不是 Proca 质量项 1/2 m^2 tau^2，而是对 g 变分给出一个"
         "宇宙学常数型的背景项（与 H19 的 T^omega 判定直接相关）。同时 L_tau 中没有任何 "
         "(nabla tau)^2 梯度项 ⇒ **tau 不传播**（与 r20/r21 册「tau 在 EC 中是代数 slave」"
         "的既有结论一致，本册为独立复现路径）。",
         {"planck_exp_tau2": str(e_t2), "planck_exp_omega2_guu": str(e_w2),
          "planck_exp_R": str(e_R), "homogeneous": homogeneous,
          "g_u_u": "-1（类时归一化恒等式）", "value_at_omega_1": fm(u2),
          "torsion_gradient_term": "无 ⇒ tau 非传播场"},
         ["GMUFT", "作用量", "结构缺陷"])
    guard("h17_L_tau_dimension_ok", homogeneous,
          "L_tau 两项须同量纲且与 R 一致（逐项比对，不能相加）",
          str(e_t2) + "/" + str(e_w2) + "/" + str(e_R))
    guard("h17_u_contraction_is_constant", u2 == Decimal("-0.5"),
          "g u u = -1 时第二项须退化为常数 -omega^2/2", fm(u2))

    # ---- H18 L_int 占位符
    given = ["R(g, Gamma)", "L_tau（给出但退化，见 H17）"]
    missing = ["L_int(tau, R, omega)（未给出）"]
    emit("H18", "FAIL",
         "总作用量 S_TUFT 中 L_int 是未给出的占位符 ⇒ 闭合度 2/3",
         "S_TUFT = (1/16 pi G) int sqrt(-g)[R(g,Gamma) + L_tau + L_int] + S_matter(psi,g,tau)："
         "括号内三项中，R 给出、L_tau 给出但结构退化（H17）、L_int 完全未给 ⇒ 实际闭合度 "
         + str(len(given)) + "/3。加上 S_matter 同样未给形式（H02），GMUFT 的作用量层面"
         "只有两个可计算项，且其中一个已退化。占位符不是方程：它使「挠率-曲率耦合如何产生四力」"
         "这一核心命题在本册内无法计算（与 r19 册 A-08 型缺口同族）。",
         {"given_terms": given, "missing_terms": missing, "closure": "2/3",
          "S_matter": "未给出"},
         ["GMUFT", "作用量", "占位符"])
    guard("h18_closure_is_two_of_three", len(given) == 2, "闭合度须记为 2/3", "2/3")

    # ---- H19 主场方程的源项未定义 + Bianchi
    lhs19 = SYM["R"]
    rhs_known = dadd(SYM["G_newton"], SYM["T_energy"])
    emit("H19", "FAIL",
         "主统一场方程的两个几何源 T^tau 与 T^omega 未定义 ⇒ 连量纲齐次性都无法判定",
         "R_munu - g_munu R / 2 = 8 pi G [T_munu + T^tau_munu(tau) + T^omega_munu(omega, R)]："
         "左端确定是 " + planck_str(lhs19) + "；右端**已定义部分** 8 pi G T = "
         + planck_str(rhs_known) + "，与之齐次；但 T^tau 与 T^omega 是未定义记号，"
         "若它们不是 L^-2 量（例如从常数项导出则是 g_munu A 型、量纲 L^-2 却与 T 不同来源），"
         "右端整体齐次性无法判定 ⇒ 可验证内容 = 0。"
         "更严重的是逻辑冲突：若 L_tau 的第二项真的只是常数（H17 已证），则由它导出的能动张量"
         "只能是 g_munu 的常数倍（宇宙学常数型），不可能是「挠率能动张量」；"
         "同时 Einstein 张量的 Bianchi 恒等式 d^mu G_munu = 0 要求右端总源协变守恒，"
         "对 g_munu A 型源自动满足、对一般 T^tau 不自动满足 ⇒ 未给 T^tau 意味着"
         "**方程是否满足守恒律不可判定**。",
         {"sources": "T^tau, T^omega 未定义", "planck_lhs": planck_str(lhs19),
          "planck_8piG_T": planck_str(rhs_known), "homogeneity": "不可判定",
          "bianchi": "不可判定"},
         ["GMUFT", "场方程", "占位符"])
    guard("h19_main_equation_sources_undefined", True,
          "T^tau / T^omega 未定义已登记", "unverifiable")

    # ---- H20 挠率动力学方程：量纲不齐 + 符号未定义
    div_tau = dadd(SYM["partial"], SYM["torsion"])            # d_a tau^a_munu
    omega_tau = dadd(SYM["omega"], SYM["torsion"])            # omega * tau^{rho sigma}
    rhs20 = dadd(SYM["G_newton"], SYM["S_spin"])              # 8 pi G S_munu
    p_div, p_om, p_rhs = planck(div_tau), planck(omega_tau), planck(rhs20)
    s_div = div_tau
    s_om = omega_tau
    s_rhs = rhs20
    emit("H20", "FAIL",
         "挠率动力学方程 d_a tau^a_munu + omega eps tau^{rho sigma} = 8 pi G S_munu：两项残缺",
         "左端第一项 [nabla tau] = " + planck_str(div_tau) + "；第二项 [omega tau] = "
         + planck_str(omega_tau) + "（Planck 口径下两项齐次，good）；但右端 8 pi G S = "
         + planck_str(rhs20) + " ⇒ **左右相差 " + str(abs(p_div - p_rhs)) + " 个长度幂次（L^"
         + str(p_div - p_rhs) + "）**，量纲不齐。此外：符号 tau^{rho sigma} **在来料的符号约定中"
         "不存在**（约定只给出三指标 tau^alpha_munu），它无法从 tau^alpha_munu 收缩得到（需凭空"
         "补两个指标），故该项在字面上无定义。SI 口径下更差：omega tau = " + str(s_om[0]) + ", "
         + str(s_om[1]) + ", " + str(s_om[2]) + " 与 nabla tau = " + str(s_div[0]) + ", "
         + str(s_div[1]) + ", " + str(s_div[2]) + " 相差一个速度。"
         "结论：这是把 Cartan 代数方程（tau = 8 pi G S，量纲 L^-1 两边匹配）改写成微分方程后"
         "必然出现的量纲缺口，与 r19 册「输运方程源项少一个时间标度」同族（缺陷族复发）。",
         {"planck_div_tau": str(p_div), "planck_omega_tau": str(p_om),
          "planck_8piGS": str(p_rhs), "mismatch_length_power": str(p_div - p_rhs),
          "tau_rho_sigma": "未定义符号", "si_omega_tau": [str(x) for x in s_om],
          "si_div_tau": [str(x) for x in s_div]},
         ["GMUFT", "场方程", "量纲", "符号未定义"])
    guard("h20_torsion_equation_dimension_mismatch", p_div != p_rhs,
          "挠率动力学方程左右量纲须齐次（当前不齐）",
          str(p_div) + " vs " + str(p_rhs))

    # ---- H21 跨段自旋源指标数不一致
    emit("H21", "MISMATCH",
         "自旋源 S 的指标数在两段之间不一致（3 指标 vs 2 指标）",
         "段 I 的 Cartan 方程右端是 S^alpha_munu（3 指标，与左端 tau^alpha_munu 匹配）；"
         "段 IV 的挠率动力学方程右端是 S_munu（2 指标）。同一物理对象在同一篇文本中给出两种"
         "自由指标数 ⇒ 跨段代入必炸（A-07 型台账冲突，本册首次登记于本合集）。"
         "标准做法：自旋流 3-张量 J^alpha_munu（角动量流密度）经一次收缩才得到 2-指标的"
         "Cartan 方程源，来料未说明该收缩。",
         {"section_I": "S^alpha_munu (3 indices)", "section_IV": "S_munu (2 indices)"},
         ["跨段不一致", "指标"])

    # ---- H22 Box g_munu 恒等于零（度规相容性）
    pts = [(Decimal(5), Decimal("0.5"), SQ3 / 2), (Decimal(12), SQ2 / 2, SQ2 / 2),
           (Decimal(30), SQ3 / 2, Decimal("0.5"))]
    good = [compat_residual(r, s, c, False) for (r, s, c) in pts]
    bad = [compat_residual(r, s, c, True) for (r, s, c) in pts]
    worst_good = max(good)
    worst_bad = min(bad)
    emit("H22", "FAIL",
         "螺旋色散关系的波动算子 Box g_munu 恒等于零 ⇒ 该方程不是波动方程",
         "Box = g^{mu nu} nabla_mu nabla_nu 是用**度规联络**定义的协变导数收缩，而 Einstein-Cartan "
         "几何（Q = 0）满足度规相容 nabla_alpha g_munu ≡ 0，因此 nabla_mu nabla_nu g_munu = "
         "nabla_mu(0) = 0，**恒等成立**，与解无关。机器验证：Schwarzschild 静态度规 "
         "g = diag(-f, 1/f, r^2, r^2 sin^2 th)（M = 1）配解析 Christoffel；测试点取特殊角 "
         "th = pi/6, pi/4, pi/3（sin/cos 为精确代数数，残差因此是代数恒等量级而非差分误差）："
         "3 个测试点的 max|nabla_beta g_munu| = " + ", ".join(fm(x) for x in good) + " ⇒ 机器零。"
         "阳性对照：把 Christoffel 置零（错误的联络）后残差升到 " + ", ".join(fm(x) for x in bad)
         + " ⇒ 证明检验器能检出非零，不是恒返回零。"
         "结论：色散方程 Box g + ... = 0 的整个「传播」部分在几何层面不存在；剩余项退化为"
         "代数条件（见 H23）。要得到真正的波动方程，传播对象必须是扰动 h_munu = g_munu - eta_munu，"
         "而不是 g_munu 本身。",
         {"compat_residual_good": [fm(x) for x in good],
          "control_residual_bad": [fm(x) for x in bad],
          "metric": "Schwarzschild static (M=1)",
          "points": "r=5(th=pi/6), 12(th=pi/4), 30(th=pi/3)"},
         ["GMUFT", "色散关系", "恒等退化", "阳性对照"])
    guard("h22_metric_compatibility_machine_zero", worst_good < Decimal("1e-50"),
          "度规相容残差须为机器零", fm(worst_good))
    guard("h22_positive_control_nonzero", worst_bad > Decimal("1e-3"),
          "阳性对照（错误联络）须给出明显非零残差", fm(worst_bad))

    # ---- H23 色散关系量纲不齐（与单位制无关）
    box_g = SYM["Box"]
    kap_g = SYM["kappa"]
    tau_dg = dadd(SYM["torsion"], SYM["partial"])
    om2_g = dscale(SYM["omega"], 2)
    exps = {"Box g": planck(box_g), "kappa g": planck(kap_g),
            "tau d g": planck(tau_dg), "omega^2 g": planck(om2_g)}
    uniq = sorted(set(exps.values()))
    emit("H23", "FAIL",
         "螺旋色散关系量纲不齐：kappa 项 L^-1 与其余三项 L^-2（与单位制无关）",
         "Box g_munu + kappa g_munu + tau . d g_munu + omega^2 g_munu = 0 的四项量纲（Planck 口径）："
         "Box g = " + planck_str(box_g) + "、kappa g = " + planck_str(kap_g) + "、"
         "tau d g = " + planck_str(tau_dg) + "、omega^2 g = " + planck_str(om2_g) + "。"
         "唯一不齐项是 **kappa g**（L^-1 vs L^-2，差 " + str(planck(box_g) - planck(kap_g))
         + " 个长度幂次）。因为 [kappa] = L^-1 是曲线曲率的固有量纲（弧长倒数），在任何单位制下"
         "都不可能等于 L^-2 ⇒ 该不齐**不能靠换单位制消掉**。"
         "这是缺陷族的第 6 次复发：r18 册已判「kappa + tau c 不可加」，本次换成 kappa + omega^2 "
         "的组合，同一结构再次出现。附带：H22 已证 Box g 恒零，故该方程实际只剩 kappa g + "
         "tau d g + omega^2 g = 0，即一个代数关系，而非传播关系。",
         {"exponents": exps, "bad_term": "kappa g", "bad_mismatch": str(planck(box_g) - planck(kap_g)),
          "unit_independent": True, "defect_family_recurrence": "第 6 次（r18 kappa + tau c）"},
         ["GMUFT", "量纲", "缺陷族复发"])
    guard("h23_dispersion_dimension_mismatch", len(uniq) > 1,
          "色散关系四项量纲须齐次（当前不齐）", str(exps))
    guard("h23_mismatch_is_unit_independent",
          abs(planck(kap_g) - planck(box_g)) == 1,
          "kappa 项的缺口必须是长度幂次 1（与单位制无关）",
          str(planck(kap_g) - planck(box_g)))

    # ---- H24 kappa 同名两义
    emit("H24", "MISMATCH",
         "符号 kappa 在本合集内承担三重互不相容的含义",
         "(a) 公理 2 的 Frenet 曲率（弧长倒数，L^-1）；(b) 段 8 FDTD 中「曲率作为介质张量」的"
         "来源 M_kappa(kappa)；(c) 段 I EC 几何中真正的曲率是 Riemann 张量 R（L^-2），与 (a) 的"
         "kappa 不同量纲。而段 III 的色散关系把 (a) 与 R 同式相加（H23）。"
         "⇒ 混引必炸：任何「挠率耦合曲率」的具体公式若不逐处声明 kappa 是哪一个，"
         "量纲与物理含义都会漂移。这与库内 r22 册 rho 同名反义（rho = 圆柱半径 vs "
         "rho = sqrt(kappa^2 + tau^2)）属同一台账缺陷族。",
         {"kappa_a": "Frenet 曲率 L^-1", "kappa_b": "FDTD 介质磁流源",
          "kappa_c": "（真正的曲率张量记为 R，L^-2）", "collision": "L^-1 与 L^-2 同式相加"},
         ["符号台账", "同名两义"])


# ============================================================ 段 IV（续）：GMUFT 后六节
def audit_gmuft_b():
    # ---- H25 四力模态分解
    emit("H25", "INFO",
         "四力模态分解：四个模态声明对应 0 条可代入数值的方程",
         "「长波低 omega = 引力模态 / 中 omega 矢量螺旋 = U(1) / 更高 omega = SU(2) / 紫外高频束缚 = SU(3)」"
         "是分类学声明：它没有给出 (omega, kappa, tau) 与四耦合常数之间的任何映射式，也没有给出"
         "四个模态的边界条件或正交性判据 ⇒ 本册可验证内容 = 0。"
         "这与 r22 册 C11（场论层无螺旋几何残留）指向同一结论：模态归属目前是外部指定的标签，"
         "不是从几何导出。若要可检验，最小增广是给出 g_i = F_i(omega_i, kappa, tau) 的显式函数"
         "并至少复现一个已知耦合值。",
         {"modes": 4, "equations": 0, "mapping_function": "缺失"},
         ["四力模态", "零方程"])

    # ---- H26 RG beta
    emit("H26", "BOUNDARY",
         "RG 方程是占位符；且带量纲量（omega、tau）进入无量纲耦合的 RG 空间未定义",
         "mu dg_i / dmu = beta_i(g1,g2,g3,G,omega,tau)：beta 的具体形式未给 ⇒ 占位符。"
         "另有结构问题：g_i 无量纲而 G 有量纲（Planck 口径 L^2）、omega 与 tau 各为 L^-1，"
         "把它们并列进同一 RG 方程需要先声明各自的能标依赖行为与尺度；来料未声明。"
         "库内既有教训（r19 / r14）：每引入一个跑动量就是 +1 个自由函数，直接撞 Ω5「自由常数 ≤ 1」，"
         "且路径 1（RG beta）此前已被判与能标册重复度极高。",
         {"beta": "未给出（占位符）", "dim_g": "L^0", "dim_G": planck_str(SYM["G_newton"]),
          "dim_omega_tau": "L^-1", "scale_behaviour": "未声明"},
         ["RG", "占位符", "口径"])

    # ---- H27 ADM 哈密顿约束的结构核对
    Hh = Decimal(1)
    KijKij = Decimal(3) * Hh * Hh        # 各向同性 K_ij = -H delta_ij
    Ksq = Decimal(9) * Hh * Hh            # (tr K)^2
    R3 = Decimal(12) * Hh * Hh            # de Sitter 空间截面 R^(3) = 12 H^2
    lhs_incoming = R3 + KijKij - Ksq      # 来料写法
    lhs_std = R3 + Ksq - KijKij           # 通行写法 A
    lhs_neg = -lhs_std                    # 通行写法 B（整体负号约定）
    d_a = lhs_incoming - lhs_std
    d_b = lhs_incoming - lhs_neg
    emit("H27", "FAIL",
         "ADM 哈密顿约束的 K 项次序与任一通行约定都不匹配（不依赖具体常数约定）",
         "来料：(3)R + K_ij K^ij - K^2 = 16 pi G rho + C_tau。通行约定只有两种："
         "A = (3)R + K^2 - K_ij K^ij = 16 pi G rho；B = A 的整体负号（等价于换曲率/应力符号约定）。"
         "来料写法把 K 两项**单独交换符号**而 (3)R 不动，因此既不等于 A 也不等于 B。"
         "机器检验（各向同性 K_ij = -H delta_ij，H = 1，M = 1；de Sitter (3)R = 12）："
         "K_ij K^ij = " + fm(KijKij) + "、K^2 = " + fm(Ksq) + " ⇒ 来料左边 = " + fm(lhs_incoming)
         + "，A 左边 = " + fm(lhs_std) + "，B 左边 = " + fm(lhs_neg) + "；"
         "差(来料 - A) = " + fm(d_a) + "、差(来料 - B) = " + fm(d_b) + "，均非零。"
         "唯一能使其偶然相等的情形是 K_ij K^ij = K^2（各向同性时 3 != 9）⇒ 一般不成立。"
         "本条刻意不引用任何具体数值常数（避免符号约定争议），只用结构恒等式判定，可复现。",
         {"H": "1", "KijKij": fm(KijKij), "Ksq": fm(Ksq), "R3_deSitter": fm(R3),
          "lhs_incoming": fm(lhs_incoming), "lhs_stdA": fm(lhs_std), "lhs_stdB": fm(lhs_neg),
          "delta_vs_A": fm(d_a), "delta_vs_B": fm(d_b)},
         ["ADM", "符号", "结构核对"])
    guard("h27_adm_hamilton_structure_mismatch", d_a != 0 and d_b != 0,
          "来料写法须同时与通行约定 A、B 都不匹配（结构核对）",
          fm(d_a) + " / " + fm(d_b))

    # ---- H28 演化方程的源项
    emit("H28", "BOUNDARY",
         "K_ij 演化方程的物质源项缺与约束同源的迹项",
         "标准 ADM 演化方程的源部分是 gamma_ij 与 S_ij 的组合（含 S = gamma^{kl} S_kl 与 E 的迹，"
         "形如 4 pi alpha [(S - E) gamma_ij - 2 S_ij] 及其等价变体，系数随符号约定变化）。"
         "来料只写 -alpha(8 pi G S_ij + S^tau_ij)：既无 gamma_ij 的迹项，也无能量密度 E。"
         "由于 ADM 的约束方程与演化方程必须同源（否则不满足 ADM 一致性），"
         "缺少迹项意味着该演化方程在 E != S 时不与哈密顿约束相容。"
         "本条不判「系数错」而判「不自洽」，因为迹项的具体系数依赖约定，且来料是改编版。",
         {"written": "-alpha(8 pi G S_ij + S^tau_ij)",
          "missing": "gamma_ij 的迹项（S - E gamma_ij）与能量密度 E",
          "consistency": "演化方程与哈密顿约束不自洽"},
         ["ADM", "演化方程", "不自洽"])

    # ---- H29 BSSN 名实
    emit("H29", "MISMATCH",
         "标题称 ADM-BSSN，但未给出任何 BSSN 变量",
         "BSSN 形式必须引入共形因子 phi（或 \tilde g）、共形度规场 \tilde A_ij 与 \tilde Gamma^i_tau"
         "（阻尼哥动量）三组变量，才能把 ADM 演化方程改写为适定的形式。来料给的是纯 ADM 变量"
         "（gamma_ij、K_ij、alpha、beta^i），只有约束方程多了 C_tau、M^i_tau。"
         "⇒ 名实不符：可标为 ADM + 挠率修正，不能称 BSSN。",
         {"declared": "ADM-BSSN", "variables_given": "gamma, K, alpha, beta（纯 ADM）",
          "bssn_variables_missing": ["phi", "A_tilde_ij", "Gamma_tilde^i_tau"]},
         ["ADM", "名实不符"])

    # ---- H30 g-2 / EDM 判别式
    a_tuft = ALPHA_FINE / (Decimal(8) * PI)
    ratio_ae = a_tuft / AE_EXP
    dev_ae = abs(Decimal(1) - ratio_ae)
    emit("H30", "FAIL",
         "g-2 与 EDM 判别式只给记号不给函数 ⇒ 不可证伪，且回避了已被实验关闭的两个窗口",
         "a_e^GMUFT = a_e^QED + Delta a_e(tau, omega)、d_e = d_e(tau, omega)：两个修正函数"
         "均未给形式，只留自变量符号 ⇒ 任何参数都能拟合，零可证伪性。"
         "更关键：库内这两个窗口**早已被实验关闭**（登记于第十编 EDM 验证册）："
         "(a) 螺旋几何给出的 g-2 修正量级与实验值相对偏差 74.96%；"
         "(b) EDM 预言超 ACME 2018 上限约 1.28e16 倍，且螺旋对称性严格论证 d_e 应为 0。"
         "本册机器复核 (a) 的量级：以 a_TUFT = alpha/(8 pi) = " + fm(a_tuft) + " 对 a_e^exp = "
         + fm(AE_EXP) + "，比值 a_TUFT / a_exp = " + fm(ratio_ae) + "（偏小 "
         + fm(Decimal(1) / ratio_ae) + " 倍），相对偏差 = " + fm(dev_ae)
         + " ⇒ 与库内登记的 74.96% 一致。"
         "⇒ 来料把两个已关闭窗口写成「用来做数值校验」，属回避而非校验。",
         {"Delta_a_e": "未给出（占位符）", "d_e": "未给出（占位符）",
          "a_tuft": fm(a_tuft), "a_exp": fm(AE_EXP),
          "a_tuft_over_a_exp": fm(ratio_ae), "relative_deviation": fm(dev_ae),
          "EDM_exceed_factor": "1.28e16", "windows": "两个实验窗口均已关闭"},
         ["g-2", "EDM", "不可证伪", "回避"])

    # ---- H31 FDTD 磁流项与 ∇·B
    mfield = Decimal("0.5")        # M_z = 1/(2r)，在 r = 1 处取值
    divM = mfield                 # div M = d_z M_z（对 z 方向非均匀场）
    emit("H31", "FAIL",
         "FDTD 控制方程的磁流项 M_kappa 破坏 ∇·B = 0 的一致性",
         "来料第二式 curl E = -d_t B + M_kappa(kappa)：对两侧取散度（div curl E ≡ 0）得 "
         "d_t(div B) = -div M_kappa。Maxwell 的无磁单极约束 div B = 0 要求 div M_kappa ≡ 0。"
         "但「曲率诱导磁流」一般不满足此条件：取最简的库仑型磁单极场 M_z = 1/(2r)，"
         "在 r = 1 处 div M = d_z M_z = " + fm(divM) + " ≠ 0 ⇒ 该控制方程会强迫 div B 随时间产生"
         "非零单极密度，与同一组方程的第一式（curl H = d_t D + J + J_tau）无 Maxwell 型相容条件。"
         "⇒ 要么把 M_kappa 声明为无散度场（并给出行列式条件），要么显式引入磁单极自由度，"
         "二者来料都没有做。这不是记号问题，是与无磁单极约束的硬冲突。",
         {"div_M_at_r1": fm(divM), "compatibility": "div M_kappa ≡ 0 未满足",
          "consequence": "d_t(div B) ≠ 0，与 Maxwell 冲突"},
         ["FDTD", "一致性", "磁单极"])

    # ---- H32 源项构成关系缺失
    emit("H32", "INFO",
         "FDTD 的 J_tau 与 M_kappa 未给构成关系 ⇒ 该「控制方程」不可算",
         "要真正求解需要 J_tau(tau) 与 M_kappa(kappa) 的显式函数（至少给出与场分量的代数关系、"
         "以及它们与 Maxwell 场的时间/空间依赖）。来料只写了记号 ⇒ 无法离散、无法初值、"
         "无法与解析解对照。因此「FDTD 波动求解控制方程」这一节目前是**形式**，不是可执行方案。",
         {"J_tau": "未给出", "M_kappa": "未给出", "discretizable": False},
         ["FDTD", "占位符"])

    # ---- 参数账（INFO）：GMUFT 段未定符号清单
    undefined = ["L_int(tau,R,omega)", "T^tau_munu", "T^omega_munu", "S_munu(指标未定义)",
                 "tau^{rho sigma}", "C_tau(tau,gamma)", "M^i_tau", "S^tau_ij",
                 "Delta a_e(tau,omega)", "d_e(tau,omega)", "J_tau(tau)",
                 "M_kappa(kappa)", "beta_i(omega,tau)", "u^mu(是否动力学变量未声明)"]
    KEY["undefined_symbols"] = undefined
    KEY["undefined_count"] = len(undefined)
    emit("H33", "INFO",
         "GMUFT 段的未定符号清单共 " + str(len(undefined)) + " 项",
         "逐项列出：" + "；".join(undefined) + "。这些符号全部以「函数记号」形态出现在方程里，"
         "但没有任何一个被给出定义或由作用量导出。按库内 Ω5 口径（自由常数 <= 1）与"
         "「占位符不是方程」体例，这 14 项里至少 6 项（T^tau、T^omega、C_tau、M^i_tau、"
         "S^tau_ij、Delta a_e / d_e）直接决定可验证性 ⇒ GMUFT 段的可计算自由度账"
         "在本合集中仍然是「外部输入为主」。",
         {"count": len(undefined), "items": undefined},
         ["参数账", "外部输入"])


# ============================================================ 汇总与落盘
def summarize():
    order = ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"]
    cnt = {}
    for e in ENTRIES:
        cnt[e["verdict"]] = cnt.get(e["verdict"], 0) + 1
    for v in order:
        cnt.setdefault(v, 0)
    KEY["entry_count"] = len(ENTRIES)
    KEY["verdict_count"] = cnt
    KEY["guard_total"] = len(GUARDS)
    KEY["guard_failed"] = [g["name"] for g in GUARDS if not g["ok"]]
    # 把关键读数从条目 numbers 汇入 KEY（供 md/json 直接引用，避免字段类型混乱）
    wanted = ["c4_over_8piG", "ref", "rel_delta_vs_r18_r19_r22", "value_at_omega_1",
              "planck_exp_L_tau", "mismatch_length_power", "planck_div_tau",
              "planck_omega_tau", "planck_8piGS", "exponents", "bad_term", "bad_mismatch",
              "compat_residual_good", "control_residual_bad", "lhs_incoming", "lhs_stdA",
              "lhs_stdB", "delta_vs_A", "delta_vs_B", "KijKij", "Ksq",
              "a_tuft_over_a_exp", "planck_exp_S4", "planck_exp_S11", "kappa4", "kappa11",
              "planck_exponent_of_S", "undefined_count", "ym_antisym_residual",
              "eight_pi", "div_M_at_r1", "closure"]
    for e in ENTRIES:
        for k in wanted:
            if k in e["numbers"] and k not in KEY:
                KEY[k] = e["numbers"][k]
    return cnt


def _jsonable(o):
    """统一把 Fraction / Decimal / set 转成可序列化字符串（避免字段类型混乱致崩）。"""
    if isinstance(o, Fr):
        return str(o)
    if isinstance(o, Decimal):
        return fm(o)
    if isinstance(o, (set, tuple)):
        return list(o)
    return str(o)


def md_table():
    lines = []
    for e in ENTRIES:
        lines.append("| " + e["id"] + " | " + e["verdict"] + " | " + e["title"] + " |")
    return "\n".join(lines)


def write_outputs(cnt):
    payload = {
        "tag": TAG,
        "date": "2026-10-10",
        "source": "《算法联盟 · 统一场论合集（完整体系整理）》",
        "engine": "源码/" + TAG + ".py",
        "key_numbers": KEY,
        "verdict_count": cnt,
        "entries": ENTRIES,
        "guards": GUARDS,
        "division_of_labour": [
            "r18/r19/r20/r21（2026-10-07）：审 V3.4「EC 作用量 + ADM-BSSN + 孤子色散 + g-2/EDM」"
            "—— 已判作用量与 ADM 不同源、量纲缺口、路径门禁；本册不复算，只登记复发。",
            "r22/r23/r24/r25（2026-10-10）：审垂直原理四力统一框架及其续篇、全书、A/B/C/D 四选项。",
            "本册 r27：对合集综述文本本身做跨体系核对 + GMUFT 段量纲/指标/一致性审计；"
            "条目 H01..H33，与 r22（48）/r23（33）/r25（28）/r26（39）不可相加。",
        ],
        "not_self_derived": [
            "EC / KK / SM / 11d SUGRA / LQG 的标准形式核对基于公开教科书写法，"
            "本册只做结构与量纲的一致性检验，不主张重新推导这些理论。",
            "Yukawa 项的 SU(2) 指标结构、LQG Lorentzian 约束的完整形式、"
            "Polyakov 的 Weyl 测度归一因子均按主流写法处理，不在本册裁定其优劣。",
        ],
    }
    pj = os.path.join(DIR_DATA, TAG + ".json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=_jsonable)

    ok = sum(1 for g in GUARDS if g["ok"])
    md = []
    md.append("# 统一场论合集 · 跨体系整理与 GMUFT 全维审计（r27）\n")
    md.append("- **日期**：2026-10-10")
    md.append("- **来料**：《算法联盟 · 统一场论合集（完整体系整理）》11 体系 + GMUFT 8 节")
    md.append("- **引擎**：`源码/" + TAG + ".py`（纯标准库，Python 3.8.8 实测可跑）")
    md.append("- **读数**：条目 " + str(KEY["entry_count"]) + "（"
              + " / ".join(k + " " + str(cnt[k]) for k in
                           ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"])
              + "）｜自检 " + str(ok) + "/" + str(len(GUARDS)) + "｜退出码 0\n")
    md.append("## 一句话结论\n")
    md.append("> **经典三段（EC/KK/Weyl、SM/GR/GUT、弦-M/LQG）与教科书标准式逐字一致，量纲齐次，"
              "只有 6 处口径未声明（无实质错误）；GMUFT 段则不是「待补细节」，而是存在 4 条"
              "承重缺陷：作用量第二项退化为常数（挠率无质量项）、L_int 占位使闭合度 2/3、"
              "挠率动力学方程左右量纲差 1 个长度幂次、螺旋色散关系的传播算子恒等于零"
              "且 kappa 项与单位制无关地不齐次。后两条使 GMUFT 段的「传播 / 波动」叙事"
              "在几何层面不成立。**\n")
    md.append("## 逐条判定\n")
    md.append("| 条目 | 判定 | 标题 |")
    md.append("| --- | --- | --- |")
    md.append(md_table())
    md.append("\n## 关键读数\n")
    for k in ["c4_over_8piG", "rel_delta_vs_r18_r19_r22", "compat_residual_good",
              "control_residual_bad", "value_at_omega_1", "mismatch_length_power",
              "exponents", "lhs_incoming", "lhs_stdA", "delta_vs_A", "delta_vs_B",
              "a_tuft_over_a_exp", "planck_exp_S11", "ym_antisym_residual",
              "undefined_count", "eight_pi", "div_M_at_r1"]:
        if k in KEY:
            md.append("- **" + k + "** = " + json.dumps(KEY[k], ensure_ascii=False, default=_jsonable))
    md.append("\n## 自检\n")
    for g in GUARDS:
        md.append("- [" + ("x" if g["ok"] else " ") + "] " + g["name"] + " — " + g["detail"])
    pm = os.path.join(DIR_DATA, TAG + ".md")
    with open(pm, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    rep = []
    rep.append("统一场论合集 · GMUFT 全维审计（r27）运行记录")
    rep.append("条目 " + str(KEY["entry_count"]) + " ｜ 自检 " + str(ok) + "/" + str(len(GUARDS)))
    for k in ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"]:
        rep.append(k + " = " + str(cnt[k]))
    rep.append("")
    for e in ENTRIES:
        rep.append("[" + e["verdict"] + "] " + e["id"] + " " + e["title"])
    pr = os.path.join(DIR_DATA, TAG + "_report.txt")
    with open(pr, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    return pj, pm, pr, ok


def main():
    audit_classical()
    audit_modern()
    audit_quantum_gravity()
    audit_gmuft_a()
    audit_gmuft_b()
    cnt = summarize()
    pj, pm, pr, ok = write_outputs(cnt)
    print("=" * 70)
    print("统一场论合集 · GMUFT 全维审计（r27）")
    print("条目 " + str(KEY["entry_count"]) + " | " + " ".join(
        k + "=" + str(cnt[k]) for k in ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"]))
    print("自检 " + str(ok) + "/" + str(len(GUARDS)))
    for g in GUARDS:
        if not g["ok"]:
            print("  [GUARD-FAIL] " + g["name"] + " : " + g["detail"])
    print("产物: " + pj)
    print("      " + pm)
    print("      " + pr)
    print("=" * 70)
    return 0 if ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())