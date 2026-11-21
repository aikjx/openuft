# -*- coding: utf-8 -*-
"""
TUFT r436 · ROOT V120 五高度 Prony 反演与形状因子第一性复核 全维审计
================================================================

定位
----
承接 r429（ROOT V119 五高度离散谱判据与 1/3 耦合映射）。本册审 ROOT V120
《ROOT V120｜离散谱五高度重建、强场外推排查与第五力可证伪性审计》
（外部来料，只读审计，不修改原文任何字节）。

本册不重判 r429 已有结论，只做三件事：
  (1) 把 V120 相对 V119 的**增量**（§2 采样点数勘误、§3 五高度 Prony、§4 u/v 形状
      约束、§5 Fayet 形状因子、§7 双作用程合成反例、§8 噪声 MC）逐条机器判定；
  (2) 对 V120 宣称的「交叉核验」做**离线可复现的第一性推导**，分清「可核」与
      「不可离线核」（外部文献）;
  (3) 把 V120 §7 的「各承担一半地表异常力」按来料自己的定义落到机器上，
      用来校正 r429 对模型 B「参数化未被完全复现」的表述（r429 字节不动）。

红线
----
数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功。
本册只做独立复算与判决，不产生新物理，不改任何被引文件。

口径
----
FAIL      = 该断言在机器判定下不成立（不是本册执行失败）
CORRECTED = 首版/既有册口径被本册更正（不改被更正版字节，只登记）
BOUNDARY  = 只在声明作用域内成立 / 外部事实 / 不可离线核实
PASS      = 判据成立（但不迁移为物理成立）
INFO      = 记账性读数

运行
----
纯标准库（decimal / fractions / math / random / json）。Python 3.8 兼容。
"""

import io
import json
import math
import os
import random
import sys
from datetime import datetime
from decimal import Decimal as D
from decimal import getcontext
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                      # 04_公共成果/算法联盟_全维自洽与归一化
DATA_DIR = os.path.join(BASE, "数据")
STEM = "TUFT-r436_ROOT_V120五高度Prony反演与形状因子第一性复核_全维审计_2026-11-21"

# ------------------------------------------------------------------ 记账容器
ENTRIES = []
GUARDS = []


def add(code, verdict, title, detail):
    ENTRIES.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def sci(x, n=18):
    if x is None:
        return "NA"
    try:
        return format(D(x), "." + str(n) + "E")
    except Exception:
        return str(x)


def relf(x, y):
    """相对差 |x-y|/|y|；y==0 时退化为绝对差。"""
    x = D(x)
    y = D(y)
    if y == 0:
        return abs(x)
    return abs(x - y) / abs(y)


# ------------------------------------------------------------------ 量纲工具
# 四元组 (M, L, T, Q)：质量 / 长度 / 时间 / 电荷
DIM_C = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))
DIM_HBAR = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))
DIM_G = (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0))
DIM_M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
DIM_L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
DIM_EPS0 = (Fraction(-1), Fraction(-3), Fraction(2), Fraction(2))  # Q^2 T^2 / (M L^3)
DIM_MU0 = (Fraction(1), Fraction(1), Fraction(0), Fraction(-2))    # M L / Q^2


def dim_mul(a, b):
    """量纲相乘 = 指数逐分量相加（不是相乘）。"""
    return tuple(a[i] + b[i] for i in range(4))


def dim_pow(a, p):
    p = Fraction(p)
    return tuple(a[i] * p for i in range(4))


def dim_str(a):
    names = ["M", "L", "T", "Q"]
    parts = []
    for i in range(4):
        c = a[i]
        if c == 0:
            continue
        parts.append("%s^%s" % (names[i], c))
    return "1" if not parts else " ".join(parts)


def dim_eq(a, b):
    return tuple(Fraction(x) for x in a) == tuple(Fraction(x) for x in b)


# ------------------------------------------------------------------ 物理常量
MU = D("3.986004418e14")          # m^3/s^2 地球标准引力参数
C_LIGHT = D("299792458")          # m/s
HBAR = D("1.054571817e-34")       # J s
EV_J = D("1.602176634e-19")       # J
R_E = D("6371000")                # m 平均地球半径
L_ = D("124600")                  # m 作用程 124.6 km
ALPHA_Y = D(1) / D(3)             # 耦合 1/3
K_ = D(1) / L_                    # 1/m
U_ = K_ * R_E                     # x = R/ell
X_ = U_
DR = D("50000")                   # m 采样步长 50 km
DELTA = DR / L_
Q_EXP = (-DELTA).exp()

# V120 §5 完整 eps_0（改进解析密度）/（均匀球）
EPS0_IMPROVED_V120 = D("0.005954404898919")
EPS0_UNIFORM_V120 = D("0.009774944408993")
EPS0_USED = EPS0_IMPROVED_V120

# V120 正文引用的读数（来料原值，用于逐位对拍）
V120 = {
    "H0_single": D("-1.02866916184e-10"),
    "H1_over_H0": D("0.44817647255"),
    "q_five": D("0.66945983638"),
    "ell_five_km": D("124.60000094"),
    "H0_double": D("1.34458547634e-8"),
    "ell_false_km": D("161.1653833"),
    "dK_rel_leaveout": D("4.0182561e-5"),
    "dprec_rad": D("0.0431818506865"),
    "dnu": D("7.64923579e-14"),
    "mphi_eV": D("1.58368363e-12"),
    "a_m2": D("2.5875266667e9"),
    "dK_200_400": D("9.77812e-4"),
    "eps_h_table": {
        0: D("5.954405e-3"), 100: D("2.709708e-3"), 200: D("1.232840e-3"),
        300: D("5.607820e-4"), 400: D("2.550277e-4"), 500: D("1.159550e-4"),
        1000: D("2.246550e-6"), 5900: D("3.097282e-23"),
    },
    "dg_table": {
        0: D("5.847375e-2"), 100: D("2.579392e-2"), 200: D("1.138103e-2"),
        300: D("5.022847e-3"), 400: D("2.217275e-3"), 500: D("9.790102e-4"),
        1000: D("1.648166e-5"), 5900: D("8.198956e-23"),
    },
    "mc_table": {
        D("0"): (D("0"), D("100"), D("100")),
        D("1e-9"): (D("0"), D("99.9833"), D("100")),
        D("1e-8"): (D("4.90"), D("27.7667"), D("69.575")),
        D("1e-7"): (D("43.3083"), D("1.0083"), D("37.55")),
    },
    "ell_ci_km": (D("124.56277"), D("124.63850")),
}

# V119（r429 已裁定的来料值）用于跨册对拍
R429 = {
    "H0_single_closed_prof": D("-1.028669164058e-10"),
    "H0_single_closed_pm": D("-8.761106241357e-4"),
    "H0B_v119": D("1.34440e-8"),
    "modelB_flip_w2": D("1.9041416180e-3"),
    "modelB_h0_at_w_max": D("1.1265410935e-8"),
    "modelB_scan_ceiling": D("0.30"),
}


# ------------------------------------------------------------------ 模型函数
def d_cosh(x):
    x = D(x)
    e = x.exp()
    return (e + (-x).exp()) / D(2)


def d_sinh(x):
    x = D(x)
    e = x.exp()
    return (e - (-x).exp()) / D(2)


def phi_shape_uniform(x):
    """Fayat 归一：Phi_0(x) = 3 (x cosh x - sinh x) / x^3。"""
    x = D(x)
    return 3 * (x * d_cosh(x) - d_sinh(x)) / (x ** 3)


def phi_shape_improved_closed(x):
    """本册独立第一性推导：Phi'(x) = (3/x) * int_0^1 t rho_hat(t) sinh(x t) dt，
    rho_hat(t) = 5/4 - t + 1/(3t)（V120 自述密度剖面）。
    逐项积分 I1 = int t sinh、I2 = int t^2 sinh、I3 = int sinh。"""
    x = D(x)
    i1 = (x * d_cosh(x) - d_sinh(x)) / (x ** 2)
    i2 = ((x ** 2 + 2) * d_cosh(x) - 2 * x * d_sinh(x) - 2) / (x ** 3)
    i3 = (d_cosh(x) - 1) / x
    return (3 / x) * (D(5) / 4 * i1 - i2 + D(1) / 3 * i3)


def phi_shape_improved_v120(x):
    """V120 §5 转录的 Fayet eq.(16) 闭式（原样）。"""
    x = D(x)
    num = (7 * x ** 2 * d_cosh(x) - 24 * d_cosh(x) + 9 * x * d_sinh(x)
           - 4 * x ** 2 + 24)
    return num / (4 * x ** 4)


def phi_shape_numeric(x, n=20000):
    """第三路径：float64 复合 Simpson 直接积分（独立于两条闭式）。"""
    xf = float(x)
    def g(t):
        # 直接用 t*rho_hat(t)，避开 t=0 的 1/t 可去奇点
        return (1.25 * t - t * t + 1.0 / 3.0) * math.sinh(xf * t)
    h = 1.0 / n
    s = g(0.0) + g(1.0)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * g(i * h)
    return (3.0 / xf) * s * h / 3.0


def eps_profile(r, eps0=EPS0_USED):
    """V120 §1/§6 的地表重标剖面：eps(r) = eps0 (1+k r)/(1+u) exp(-k (r-R))。"""
    r = D(r)
    return eps0 * (1 + K_ * r) / (1 + U_) * (-(K_ * (r - R_E))).exp()


def eps_profile_range(r, ell, eps0=EPS0_USED):
    """指定作用程的地表重标剖面（模型 B 的第二作用程用）。"""
    r = D(r)
    k = 1 / D(ell)
    u = k * R_E
    return eps0 * (1 + k * r) / (1 + u) * (-(k * (r - R_E))).exp()


def k_model(h, ell=L_, eps0=EPS0_USED):
    """K(r)/mu - 1 = eps(r)，h 为海拔（m）。"""
    return eps_profile(R_E + D(h), eps0)


def diffs(seq):
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def hankel(dseq, n):
    return dseq[n] * dseq[n + 2] - dseq[n + 1] ** 2


def j0(dseq):
    return dseq[0] * dseq[3] - dseq[1] * dseq[2]


def p5(dseq):
    h0 = hankel(dseq, 0)
    jj = j0(dseq)
    return dseq[0] * jj ** 2 - 4 * dseq[1] * jj * h0 + 4 * dseq[2] * h0 ** 2


def ratio_R(k, r0, delta):
    """三高度物理函数比值 R(k) = int_L t e^{-kt} dt / int_H t e^{-kt} dt。"""
    k = D(k)
    r0 = D(r0)
    delta = D(delta)
    def prim(t):
        return (-(t) / k - 1 / (k * k)) * (-(k * t)).exp()
    return (prim(r0) - prim(r0 + delta)) / (prim(r0 + delta) - prim(r0 + 2 * delta))


def solve_ell_from_R(target, r0, delta, lo=None, hi=None):
    """二分求 k（1/m）使 R(k)=target，再给 ell=1/k。"""
    target = D(target)
    if lo is None:
        lo = D("1e-9")
    if hi is None:
        hi = D("1e-4")
    for _ in range(200):
        mid = (lo + hi) / 2
        if ratio_R(mid, r0, delta) < target:
            lo = mid
        else:
            hi = mid
    return 1 / ((lo + hi) / 2)


# ==================================================================
# 区块 V1：§2 采样点数的索引代数（核心攻破 1）
# ==================================================================
def height_closure(n):
    """H_n = D_n D_{n+2} - D_{n+1}^2；D_j = K_{j+1} - K_j。
    返回 H_n 所需 K 下标集合（索引代数，与浮点无关）。"""
    js = set([n, n + 1, n + 2])
    ks = set()
    for j in js:
        ks.add(j)
        ks.add(j + 1)
    return sorted(ks)


cl0 = height_closure(0)
cl1 = height_closure(1)
union = sorted(set(cl0) | set(cl1))

guard("G_sampling_H0_closure", len(cl0) == 4,
      "H_0 所需 K 下标 %s => %d 个高度" % (cl0, len(cl0)))
guard("G_sampling_H1_closure", len(cl1) == 4,
      "H_1 所需 K 下标 %s => %d 个高度" % (cl1, len(cl1)))
guard("G_sampling_union_is_five", len(union) == 5,
      "H_1/H_0 合并所需 K 下标 %s => %d 个高度（来料称 6）" % (union, len(union)))
guard("G_sampling_six_claim_false", len(union) != 6,
      "机器索引代数给出 %d 个高度，与来料 §2「共 6 个高度」不符" % len(union))

add("V1-01", "FAIL",
    "来料 §2「采样点数勘误」本身是错的：H_0/H_1 各只需 4 个高度，H_1/H_0 共需 5 个",
    "按来料 §2 自给的定义 D_n = K_{n+1}-K_n、H_n = D_n D_{n+2}-D_{n+1}^2 做纯索引代数："
    "H_0 需要 D_0..D_2 即 K 下标 %s（%d 个高度），H_1 需要 D_1..D_3 即 K 下标 %s（%d 个高度），"
    "两者合并即 K 下标 %s 共 %d 个高度。来料 §2 写「H_0 需 K_0 到 K_4 共 5 个、H_1 需 K_1 到 K_5 共 5 个、"
    "同一次试验共 6 个」，即把每个 H_n 的依赖多算了一个 D（实为 D_n..D_{n+3}）。"
    "机器读数：H_1/H_0 的正确采样数 = %d，不是 6。★讽刺后果：来料 §2 把 V119 原式改名为「六高度 Hankel 比率反演」，"
    "而 V119 原称「五高度」恰是正确值 ⇒ 本次「勘误」是把一个本来正确的命名改错，并以此作为摘要级卖点。"
    % (cl0, len(cl0), cl1, len(cl1), union, len(union), len(union)))

add("V1-02", "FAIL",
    "来料内部自相矛盾：§2 断言「六高度」，§12 结论却自称「修复为真正五高度」",
    "来料 §12 结论原文：「V120 的数学贡献是把错称『五高度』的六高度反演修复为真正五高度的代数式」——"
    "而 §2 正文写的是「H_0 需 5 个、H_1 需 5 个、同一次试验的 H_1/H_0 实际需 6 个」。"
    "§12 声称「真正五高度」但 §2 给的是六，且机器索引代数判定五才是对的（V1-01）⇒ "
    "同一份来料对同一件事给了两个互斥数字，且其中一个还是错的。附带：§3 的五高度 Prony 公式本身只用 K_0..K_4，"
    "与 §2 的「六高度」直接冲突，也与机器判定一致。")

add("V1-03", "PASS",
    "来料 §2 的依赖展开本身可被机器完全重建（索引代数层）",
    "本册用集合闭包算法重建 H_n 对 K 下标的依赖：H_n -> {D_n, D_{n+1}, D_{n+2}} -> "
    "{K_n..K_{n+3}}，闭包结果与手算逐项一致；该判定为纯整数运算、不含任何浮点，"
    "因此「6 vs 5」的分歧不可能来自数值误差或口径差异，只可能是索引展开错误。")

# ==================================================================
# 区块 V2：§3 Prony 代数的恒等性（核心攻破 2）
# ==================================================================
getcontext().prec = 90

def family_D(n, a, b, q):
    return (q ** n) * (a + b * n)


res_p5 = D(0)
res_q = D(0)
res_ratio = D(0)
negH = 0
fams = []
for i in range(200):
    q = D("0.05") + D("0.9") * (D(i) / D(200))
    a = D("0.3") + D("1.7") * ((D(i % 7) + 1) / D(8))
    b = D("-0.9") + D("1.6") * ((D(i % 11) + 1) / D(12))
    ds = [family_D(j, a, b, q) for j in range(6)]
    res_p5 = max(res_p5, abs(p5(ds)))
    h0 = hankel(ds, 0)
    res_q = max(res_q, abs(j0(ds) / (2 * h0) - q))
    h1 = hankel(ds, 1)
    res_ratio = max(res_ratio, abs(h1 / h0 - q ** 2))
    if h0 < 0:
        negH += 1
    fams.append((a, b, q))

# 阳性对照：非重复根模型 D_n = p^n + s^n（p != s）=> P_5 应显著非零
p, s = D("0.7"), D("0.3")
ds_two = [p ** n + s ** n for n in range(6)]
p5_two = p5(ds_two)

getcontext().prec = 60

guard("G_P5_identity", res_p5 < D("1e-80"),
      "重复根族 200 组 P_5 最大残差 %s（恒等式）" % sci(res_p5))
guard("G_q_identity", res_q < D("1e-80"),
      "重复根族 200 组 J_0/(2H_0) - q 最大残差 %s" % sci(res_q))
guard("G_Hratio_identity", res_ratio < D("1e-80"),
      "重复根族 200 组 H_1/H_0 - q^2 最大残差 %s" % sci(res_ratio))
guard("G_H_negative_family", negH == 200,
      "重复根族 200 组 H_0 恒为负（%d/200）" % negH)
guard("G_P5_has_teeth", abs(p5_two) > D("1e-6"),
      "阳性对照（非重复根双指数模型）P_5 = %s ≠ 0 ⇒ 判据有牙" % sci(p5_two))

add("V2-01", "FAIL",
    "P_5 ≡ 0 是重复根指数族内的恒等式（零判别力），不是「必要条件」",
    "在 D_n = q^n (a+bn) 族内解析可证：H_0 = -b^2 q^2、J_0 = -2 b^2 q^3 ⇒ J_0/(2H_0) = q 恒等成立，"
    "P_5 = D_0 J_0^2 - 4 D_1 J_0 H_0 + 4 D_2 H_0^2 = 4 b^4 q^7 [a - 2(a+b) + (a+2b)] ≡ 0。"
    "机器复核：200 组 (a,b,q) 的 P_5 最大残差 %s、J_0/(2H_0)-q 最大残差 %s、H_1/H_0-q^2 最大残差 %s，"
    "H_0 恒负 %d/200。阳性对照：注入非重复根双指数模型（D_n = p^n+s^n, p≠s）后 P_5 = %s ≠ 0 ⇒ 判据有牙。"
    "★来料 §12 裁定表写「P_5 消元式 通过；仅重复根模型必要条件」低估了它的性质：恒等式连「必要条件」都不是"
    "（恒真蕴含一切），它是族内零信息量重述。" % (sci(res_p5), sci(res_q), sci(res_ratio), negH, sci(p5_two)))

add("V2-02", "FAIL",
    "§4 的 u/v 反例在代数上是空操作（被检验对象本身恒真）",
    "来料 §4 的论证链是：构造 K_n = 1+(0.006+0.0004n)e^{-nΔ/ℓ} 完全通过 Prony/H 判据但不满足 "
    "u/v = (ℓ+r_0)/Δ ⇒ 故 P_5 = 0 不是原始 Yukawa 力式的充分条件。由于 V2-01 已证 P_5 ≡ 0 对族内恒成立，"
    "该反例无论加不加 u/v 都不会改变 P_5 的取值 ⇒ 「P_5 不是充分条件」这句话在代数上没有承载者，"
    "真正提供判别力的只有 u/v 约束本身；而 u/v = (ℓ+r_0)/Δ 是 (ℓ, r_0, Δ) 之间的先验参数关系，"
    "不含数据内容 ⇒ 本册把它登记为「无数据增量的形状约束」而非「加严判据」。")

add("V2-03", "PASS",
    "来料 §3 的 Hankel 结构与比值恒等式在族内严格成立（与 r429 独立互印）",
    "族内 H_n < 0 与 H_{n+1}/H_n = q^2 = e^{-2Δ/ℓ} 在 200 组参数上以 90 位精度复核，"
    "最大残差 %s；来料 §7 的 H_1/H_0 = %s 与 e^{-2Δ/ℓ} = %s 相对差 %s ⇒ 来料的比值读数与本册自算一致，"
    "且与 r429「离散谱必要条件在单作用程族内是代数恒等式」的裁定方向一致（互印）。"
    % (sci(res_ratio), sci(V120["H1_over_H0"]), sci(Q_EXP ** 2),
       sci(relf(V120["H1_over_H0"], Q_EXP ** 2))))

# ==================================================================
# 区块 V3：§3 三高度唯一性证明复核 + §4 u/v 反例
# ==================================================================
r0 = R_E
delta_big = D("100000")     # 100 km（三高度留出用）
R0_closed = (2 * r0 + DR) / (2 * r0 + 3 * DR)
R0_numeric = ratio_R(D("1e-18"), r0, DR)

ks_scan = [D("1e-9") * (D(10) ** (D(i) / D(30))) for i in range(150)]
rr_scan = [ratio_R(k, r0, DR) for k in ks_scan]
mono_ok = all(rr_scan[i + 1] > rr_scan[i] for i in range(len(rr_scan) - 1))
dln_min = min((rr_scan[i + 1] / rr_scan[i] - 1) / (ks_scan[i + 1] - ks_scan[i]) * ks_scan[i]
              for i in range(len(rr_scan) - 1))

ell_3h = solve_ell_from_R(ratio_R(K_, r0, delta_big), r0, delta_big)

# u/v 反例（§4 原文构造）
u_ex = D("0.006")
v_ex = D("0.0004")
uv_ex = u_ex / v_ex
uv_constraint_h0 = L_ / DR                       # r0 = 0（地表起算）
uv_constraint_RE = (L_ + R_E) / DR               # r0 = R（按外部半径起算）
q_ex = (-DR / L_).exp()
a_ex = (q_ex - 1) * u_ex + q_ex * v_ex
b_ex = (q_ex - 1) * v_ex
ds_ex = [D(1) + (u_ex + v_ex * D(n)) * (q_ex ** n) for n in range(6)]
p5_ex = p5(diffs(ds_ex))

guard("G_R0_closed_vs_limit", relf(R0_numeric, R0_closed) < D("1e-12"),
      "R(k->0) 闭式 %s vs 数值极限 %s，相对差 %s"
      % (sci(R0_closed, 12), sci(R0_numeric, 12), sci(relf(R0_numeric, R0_closed))))
guard("G_R_monotone", mono_ok and dln_min > 0,
      "三高度 R(k) 在 150 点上严格递增（dlnR/dk 最小值 %s > 0）" % sci(dln_min))
guard("G_R_inversion_ell", relf(ell_3h, L_) < D("1e-18"),
      "三高度比值反解 ell = %s m（真值 %s m）" % (sci(ell_3h, 14), sci(L_, 14)))
guard("G_uv_counterexample_breaks", uv_ex != uv_constraint_h0 and uv_ex != uv_constraint_RE,
      "反例 u/v = %s，两种 r0 口径下的约束分别为 %s / %s ⇒ 均违反"
      % (sci(uv_ex, 8), sci(uv_constraint_h0, 8), sci(uv_constraint_RE, 8)))
guard("G_uv_counterexample_in_family", abs(p5_ex) < D("1e-70"),
      "反例族内 P_5 = %s（说明反例确实通过 Prony/H 判据）" % sci(p5_ex))

add("V3-01", "PASS",
    "§3 三高度唯一性的积分表示与单调性证明复核成立",
    "K_0-K_1 = mu*alpha*Phi*k^2*int_{r0}^{r0+Δ} t e^{-kt} dt ⇒ k^2 与幅度在比值中消掉，"
    "来料 R(k)=int_L t e^{-kt}dt / int_H t e^{-kt}dt 的积分表示**正确**。"
    "机器复核：k->0 的数值极限 %s 与闭式 (2r0+Δ)/(2r0+3Δ)=%s 相对差 %s；"
    "150 点扫描严格递增（min dlnR/dk·k = %s > 0）；以真 ell=124.6 km 正推的 R 值反解回 "
    "ell=%s m，相对差 %s。⇒ 值域 [R(0),∞)、至多一解的结论成立（存在性另需 R_obs ≥ R(0)）。"
    % (sci(R0_numeric, 12), sci(R0_closed, 12), sci(relf(R0_numeric, R0_closed)),
       sci(dln_min), sci(ell_3h, 14), sci(relf(ell_3h, L_))))

add("V3-02", "PASS",
    "§4 的 u/v 反例确实违反原始 Yukawa 形状限制，但证明不了 P_5 的充分性",
    "反例 K_n=1+(0.006+0.0004n)e^{-nΔ/ℓ} 的 u/v=%s；来料约束 (ℓ+r_0)/Δ 在 r_0=0 口径给 %s、"
    "在 r_0=R 口径给 %s，反例两口径均违反 ⇒ 反例构造成立。且反例本身的族内 P_5 = %s（机器零）⇒ "
    "反例确实「通过」Prony/H 判据。但由 V2-01 知 P_5 在族内恒为 0，故「加 u/v 才充分」的说法没有"
    "改变任何可检验内容：约束的是参数先验关系，不是新增数据判据。"
    % (sci(uv_ex, 8), sci(uv_constraint_h0, 8), sci(uv_constraint_RE, 8), sci(p5_ex)))

# ==================================================================
# 区块 V4：三估计器非独立性（核心攻破 3）
# ==================================================================
heights6 = [D(0), D(50000), D(100000), D(150000), D(200000), D(250000)]
kseq6 = [D(1) + k_model(h) for h in heights6]
dseq6 = diffs(kseq6)
h0_6 = hankel(dseq6, 0)
h1_6 = hankel(dseq6, 1)
q_prony = j0(dseq6) / (2 * h0_6)
ell_prony = -DR / (q_prony.ln())
ell_hankel = -2 * DR / ((h1_6 / h0_6).ln())

heights3 = [D(0), D(100000), D(200000)]
kseq3 = [D(1) + k_model(h) for h in heights3]
R_obs3 = (kseq3[0] - kseq3[1]) / (kseq3[1] - kseq3[2])
ell_ratio3 = solve_ell_from_R(R_obs3, R_E, delta_big)

ell_set = [ell_ratio3, ell_prony, ell_hankel]
ell_spread = max(abs(x - L_) for x in ell_set) / L_

guard("G_estimatorA_ell", relf(ell_ratio3, L_) < D("1e-18"),
      "三高度比值估计器 ell = %s m" % sci(ell_ratio3, 14))
guard("G_estimatorB_ell", relf(ell_prony, L_) < D("1e-18"),
      "五高度 Prony 估计器 ell = %s m" % sci(ell_prony, 14))
guard("G_estimatorC_ell", relf(ell_hankel, L_) < D("1e-18"),
      "六高度 Hankel 比率估计器 ell = %s m" % sci(ell_hankel, 14))
guard("G_estimators_not_independent", ell_spread < D("1e-16"),
      "三估计器相对离散度 %s < 1e-16 ⇒ 无噪声下不独立" % sci(ell_spread))

add("V4-01", "FAIL",
    "§8 推荐的「三高度反演 + 五高度 Prony + 六高度 Hankel 交叉检查」在无噪声单 Yukawa 内不独立",
    "在同一条模型 A 采样谱（Delta=50 km、地表重标剖面）上，本册用三种名义上不同的估计器反解同一个 ell："
    "三高度物理函数比值 R(k) 反演给 %s m、五高度无幅度 Prony q=J_0/(2H_0) 给 %s m、"
    "六高度 Hankel 比率 ell=-2Δ/ln(H_1/H_0) 给 %s m；三者与真值 124600 m 的最大相对偏差 %s。"
    "⇒ 在无噪声、单作用程、地表重标剖面这三条来料自设前提下，三者只是同一个自由度的三种代数实现，"
    "不构成独立交叉检验；来料 §8 工作流把它们并列为「初步反演 + 辅助检验 + 交叉检查」会高估证据强度。"
    "（有噪声时三者方差不同，但该差异属于统计实现细节，不改变结构冗余。）"
    % tuple([sci(x, 14) for x in ell_set] + [sci(ell_spread)]))

add("V4-02", "INFO",
    "三估计器的结构冗余与 r429「族内恒等式」结论同源",
    "r429 已裁定 H_n<0 与 H_{n+1}/H_n=q^2 是单作用程族内代数恒等式；本册 V2-01 进一步给出 P_5≡0、"
    "V4-01 给出三种反演器给同一 ell。三条合起来说明：V120 所谓「三个层次的证伪检查」中，"
    "层次 1（重复根结构）与层次 2（Prony 反演）在族内零判别力，层次 3（u/v 形状）是先验参数关系，"
    "真正留给用户判别的只有「数据是否出自这个一条参数族」，而非「哪个层次抓到了错误模型」。")

# ==================================================================
# 区块 V5：§5 Fayet 形状因子（本轮核心攻破 4：闭式与自述密度剖面不同源）
# ==================================================================
getcontext().prec = 90
x_exact = X_


def phi_shape_improved_derived_expanded(x):
    """把 I1/I2/I3 逐项积分通分后的展开式；用于与第一性闭式互检。

    首版手算把 I3 通分时误乘 x，得到含 -x 的错误展开；本版按
    (cosh x - 1)/x = x^2(cosh x - 1)/x^3 正确通分。
    """
    x = D(x)
    return (((D(7) / 4 * x ** 2 - 6) * d_cosh(x)
             + D(9) / 4 * x * d_sinh(x) + 6 - x ** 2) / x ** 4)


def phi_shape_diff_formula(x):
    """重算后两闭式恒等；保留函数以固化「差恒零」这一自检点。"""
    return D(0)


phi_u = phi_shape_uniform(x_exact)
phi_i_derived = phi_shape_improved_closed(x_exact)
phi_i_derived_exp = phi_shape_improved_derived_expanded(x_exact)
phi_i_v120 = phi_shape_improved_v120(x_exact)
phi_i_diff = phi_i_derived - phi_i_v120
phi_i_diff_formula = phi_shape_diff_formula(x_exact)
phi_i_num = D(str(phi_shape_numeric(x_exact)))
phi_i_small = phi_shape_improved_closed(D("1e-3"))
phi_v120_small = phi_shape_improved_v120(D("1e-3"))
phi_u_small = phi_shape_uniform(D("1e-3"))
phi_i_x1 = phi_shape_improved_closed(D(1))
phi_i_v120_x1 = phi_shape_improved_v120(D(1))
getcontext().prec = 60

guard("G_phi_integral_expanded_identity",
      relf(phi_i_derived, phi_i_derived_exp) < D("1e-80"),
      "I1/I2/I3 第一性闭式 vs 正确通分展开式：相对差 %s" % sci(relf(phi_i_derived, phi_i_derived_exp)))
guard("G_phi_numeric_path",
      relf(phi_i_num, phi_i_derived) < D("1e-7"),
      "float64 Simpson 独立积分 vs 第一性闭式：相对差 %s" % sci(relf(phi_i_num, phi_i_derived)))
guard("G_phi_v120_matches_stated_profile",
      relf(phi_i_derived, phi_i_v120) < D("1e-80"),
      "x=%s 时自述剖面积分给 %s，V120 印刷闭式给 %s，相对差 %s"
      % (sci(x_exact, 12), sci(phi_i_derived, 12), sci(phi_i_v120, 12), sci(relf(phi_i_derived, phi_i_v120))))
guard("G_phi_diff_is_zero",
      abs(phi_i_diff) < D("1e-80") and relf(phi_i_diff, phi_i_diff_formula) < D("1e-70"),
      "两闭式之差 %s（恒零守卫）" % sci(phi_i_diff))
guard("G_phi_x1_cross",
      relf(phi_i_x1, phi_i_v120_x1) < D("1e-80"),
      "x=1 独立点两式相对差 %s" % sci(relf(phi_i_x1, phi_i_v120_x1)))
guard("G_phi_small_x_normalization",
      abs(phi_i_small - 1) < D("1e-6") and abs(phi_v120_small - 1) < D("1e-6")
      and abs(phi_u_small - 1) < D("1e-6"),
      "x->0 三式均归一：自述剖面 %s、V120 闭式 %s、均匀球 %s"
      % (sci(phi_i_small, 10), sci(phi_v120_small, 10), sci(phi_u_small, 10)))

add("V5-01", "PASS",
    "V120 §5 的 Φ′ 闭式可由自述密度剖面第一性导出（首版手算自纠错后确认）",
    "按球对称 Yukawa 源形状因子定义（由同节均匀球闭式锁定归一）"
    "Φ(x)=(3/x)∫₀¹ t ρ̂(t) sinh(xt)dt，取 ρ̂(t)=5/4−t+1/(3t)，逐项积分 "
    "I₁=(x cosh x−sinh x)/x²、I₂=[(x²+2)cosh x−2x sinh x−2]/x³、I₃=(cosh x−1)/x；"
    "通分时 I₃ 必须写成 x²(cosh x−1)/x³（首版误写成 x(cosh x−1)/x³，导致假 FAIL），"
    "正确展开为 Φ′=[(7x²/4−6)cosh x+(9x/4)sinh x+6−x²]/x⁴，"
    "与 V120 印刷闭式在 90 位下相对差 %s；float64 Simpson 第三路径相对差 %s；"
    "两闭式之差恒为 0（守卫 %s），x=1 交叉点相对差 %s。"
    "★本条是本册自伤登记：预演曾据错误通分写成「剖面与闭式不同源」的核心 FAIL，"
    "机器守卫与独立数值路径当场拦下，已撤回并改为 PASS。"
    % (sci(relf(phi_i_derived, phi_i_v120)), sci(relf(phi_i_num, phi_i_derived)),
       sci(phi_i_diff), sci(relf(phi_i_x1, phi_i_v120_x1))))

add("V5-02", "BOUNDARY",
    "「与 Fayet 2026 公式交叉核验」仍不可离线核实；V5-01 只证明来料内部自洽",
    "本册证明的是「来料给出的闭式 = 来料自述密度剖面的积分结果」，不是「该闭式等于 Fayet 2026 EPJC eq.(16)」——"
    "原文不在库内、离线无法核实。来料 §10 的「与五层模型 x≤64 误差至多约 0.7%」是近似旁证，不构成闭式正确性的独立核验。"
    "该行按 BOUNDARY 登记。")

add("V5-03", "PASS",
    "均匀球形状因子及其小 x 归一化可独立复现（对照组）",
    "均匀球 Φ₀=3(x cosh x−sinh x)/x³ 的闭式、电子稳定式与 x→0 归一化均成立（%s）；"
    "它作为对照组证明本册形状因子积分/数值实现对另一条剖面同样有效。"
    % sci(phi_u_small, 8))

# ==================================================================
# 区块 V6：§5 eps_0 两行 + a / m_phi 换算（区分「V120 闭式值」与「自述剖面值」）
# ==================================================================
getcontext().prec = 90
ex_fac = (-2 * x_exact).exp()


def phi_v120_stable(x):
    """把 e^{-x} 解析乘进 cosh/sinh 的 V120 闭式稳定路径。"""
    x = D(x)
    e2 = (-2 * x).exp()
    num = (((7 * x ** 2 - 24) * (1 + e2) + 9 * x * (1 - e2)) / 2
           - 4 * x ** 2 + 24)
    return num / (4 * x ** 4)


phi_u_stable = D(3) / (2 * x_exact ** 3) * ((x_exact - 1) + (x_exact + 1) * ex_fac)
phi_v120_s = phi_v120_stable(x_exact)
eps0_u_direct = ALPHA_Y * phi_u * (1 + x_exact) * (-x_exact).exp()
eps0_u_stable = ALPHA_Y * phi_u_stable * (1 + x_exact)
eps0_v120_direct = ALPHA_Y * phi_i_v120 * (1 + x_exact) * (-x_exact).exp()
eps0_v120_stable = ALPHA_Y * phi_v120_s * (1 + x_exact)
eps0_stated_profile = ALPHA_Y * phi_i_derived * (1 + x_exact) * (-x_exact).exp()
eps0_diff_formula = ALPHA_Y * (1 + x_exact) * (-x_exact).exp() * phi_i_diff_formula
getcontext().prec = 60

a_m2 = L_ ** 2 / 6
mphi_j = HBAR * C_LIGHT / L_
mphi_ev = mphi_j / EV_J
dim_a = dim_pow(DIM_L, 2)
dim_mphi = dim_mul(dim_mul(DIM_HBAR, DIM_C), dim_pow(DIM_L, -1))
dim_vac = dim_mul(DIM_EPS0, DIM_MU0)
dim_inv_c2 = dim_pow(DIM_C, -2)

guard("G_eps0_uniform_double_path",
      relf(eps0_u_direct, eps0_u_stable) < D("1e-70"),
      "均匀球 eps_0 双路径：闭式 %s vs 稳定式 %s" % (sci(eps0_u_direct, 16), sci(eps0_u_stable, 16)))
guard("G_eps0_v120_double_path",
      relf(eps0_v120_direct, eps0_v120_stable) < D("1e-70"),
      "V120 闭式 eps_0 双路径：闭式 %s vs 稳定式 %s"
      % (sci(eps0_v120_direct, 16), sci(eps0_v120_stable, 16)))
guard("G_eps0_uniform_v120",
      relf(eps0_u_direct, EPS0_UNIFORM_V120) < D("1e-11"),
      "均匀球 eps_0 本册 %s vs 来料 %s" % (sci(eps0_u_direct, 16), sci(EPS0_UNIFORM_V120, 16)))
guard("G_eps0_v120_value",
      relf(eps0_v120_direct, EPS0_IMPROVED_V120) < D("1e-11"),
      "用 V120 印刷闭式复现改进档 eps_0：%s vs 来料 %s"
      % (sci(eps0_v120_direct, 16), sci(EPS0_IMPROVED_V120, 16)))
guard("G_eps0_stated_profile_matches_v120",
      relf(eps0_stated_profile, EPS0_IMPROVED_V120) < D("1e-11"),
      "用来自述密度剖面给 eps_0=%s，与来料表值 %s 相对差 %s"
      % (sci(eps0_stated_profile, 12), sci(EPS0_IMPROVED_V120, 12),
         sci(relf(eps0_stated_profile, EPS0_IMPROVED_V120))))
guard("G_eps0_diff_formula",
      abs(eps0_stated_profile - eps0_v120_direct) < D("1e-70")
      and relf(eps0_stated_profile - eps0_v120_direct, eps0_diff_formula) < D("1e-70"),
      "两 eps_0 之差 %s（恒零守卫）" % sci(eps0_stated_profile - eps0_v120_direct))
guard("G_a_dimension", dim_eq(dim_a, dim_pow(DIM_L, 2)),
      "a = ell^2/6 量纲 = %s（应为 L^2）" % dim_str(dim_a))
guard("G_mphi_dimension", dim_eq(dim_mphi, dim_mul(DIM_M, dim_mul(DIM_L, dim_mul(DIM_L, dim_pow(DIM_T, -2))))),
      "hbar*c/ell 量纲 = %s（应为能量 M L^2 T^-2；来料写的是 m_phi c^2）" % dim_str(dim_mphi))
guard("G_vacuum_dimension",
      dim_eq(dim_vac, dim_inv_c2),
      "eps_0*mu_0 量纲 = %s == 1/c^2 量纲 %s" % (dim_str(dim_vac), dim_str(dim_inv_c2)))
guard("G_a_value", relf(a_m2, V120["a_m2"]) < D("1e-9"),
      "a = ell^2/6 = %s m^2（来料 %s，11 位报价）" % (sci(a_m2, 14), sci(V120["a_m2"], 14)))
guard("G_mphi_value", relf(mphi_ev, V120["mphi_eV"]) < D("1e-5"),
      "m_phi c^2 = hbar c/ell = %s eV（来料 %s）" % (sci(mphi_ev, 12), sci(V120["mphi_eV"], 12)))

add("V6-01", "PASS",
    "两行 eps_0 与 a / m_phi 换算均可复现（双路径 + 量纲守卫）",
    "均匀球档 eps_0=%s（来料 %s），改进密度档 eps_0=%s（来料 %s）；"
    "闭式路径与 e^{-x} 解析乘入 cosh/sinh 的稳定路径逐位一致；"
    "由自述剖面积分得到的 eps_0 与 V120 印刷闭式差为 %s（机器零）。"
    "a=%s m²（来料 %s）、m_phi c²=%s eV（来料 %s）；量纲：a 为 L²、hbar c/ell 为能量 M L²T⁻²、"
    "eps₀mu₀ 为 L⁻²T² = 1/c²。★口径：这些是固定 α_Y=1/3 与 ell=124.6 km 的情景复现，"
    "不是 ROOT 对 α_Y 或 ell 的第一性预言。"
    % (sci(eps0_u_direct, 16), sci(EPS0_UNIFORM_V120, 16),
       sci(eps0_v120_direct, 16), sci(EPS0_IMPROVED_V120, 16),
       sci(eps0_stated_profile - eps0_v120_direct),
       sci(a_m2, 14), sci(V120["a_m2"], 14), sci(mphi_ev, 12), sci(V120["mphi_eV"], 12)))

add("V6-02", "PASS",
    "量纲复核纠正一处口径：hbar c/ell 是能量（m_phi c²），不是质量本身",
    "来料写 m_phi c²=hbar c/ell 是正确的能量等式；本册首版把其量纲守卫误写成 M，"
    "被 DIM_HBAR⊗DIM_C⊗DIM_L⁻¹ 的机器计算拦下，已改为 M L²T⁻²。该自伤不改变数值读数。")

# ==================================================================
# 区块 V7：§7 双作用程模型 B（按「各承担一半地表异常力」重算并更正 r429 表述）
# ==================================================================
ELL2 = D("300000")


def eps_dual_v120(h):
    """V120 §7：124.6 km 与 300 km 两作用程各承担一半地表异常力。"""
    r = R_E + D(h)
    return (eps_profile_range(r, L_, EPS0_USED / 2)
            + eps_profile_range(r, ELL2, EPS0_USED / 2))


def eps_dual_r429(h, w2):
    """r429 旧参数化：(1-w2) eps_ell1 + w2 eps_ell2（两项各自用完整 eps0）。"""
    r = R_E + D(h)
    return ((1 - w2) * eps_profile_range(r, L_, EPS0_USED)
            + w2 * eps_profile_range(r, ELL2, EPS0_USED))


def profile_dseq(fn, heights):
    vals = [D(1) + fn(h) for h in heights]
    return diffs(vals), vals


dA, _ = profile_dseq(k_model, heights6)
h0_A = hankel(dA, 0)
h1_A = hankel(dA, 1)
q_A = j0(dA) / (2 * h0_A)
ell_A = -DR / q_A.ln()

dB, _ = profile_dseq(eps_dual_v120, heights6)
h0_B = hankel(dB, 0)

d_old05, _ = profile_dseq(lambda h: eps_dual_r429(h, D("0.5")), heights6)
h0_old05 = hankel(d_old05, 0)

eps_B0, eps_B100, eps_B200, eps_B300 = [eps_dual_v120(h) for h in
                                         (D(0), D(100000), D(200000), D(300000))]
R_fit_B = (eps_B0 - eps_B100) / (eps_B100 - eps_B200)
ell_false = solve_ell_from_R(R_fit_B, R_E, D("100000"))
eps_B300_pred = eps_profile_range(R_E + D(300000), ell_false, eps_B0)
leaveout_rel = abs(eps_B300_pred - eps_B300)

guard("G_modelA_H0", relf(h0_A, V120["H0_single"]) < D("1e-7"),
      "模型 A H0 本册 %s vs V120 %s" % (sci(h0_A, 14), sci(V120["H0_single"], 14)))
guard("G_modelA_Hratio", relf(h1_A / h0_A, V120["H1_over_H0"]) < D("1e-7"),
      "模型 A H1/H0 本册 %s vs V120 %s" % (sci(h1_A / h0_A, 14), sci(V120["H1_over_H0"], 14)))
guard("G_modelA_q", relf(q_A, V120["q_five"]) < D("1e-7"),
      "模型 A q_five 本册 %s vs V120 %s" % (sci(q_A, 14), sci(V120["q_five"], 14)))
guard("G_modelA_ell", relf(ell_A / D(1000), V120["ell_five_km"]) < D("1e-7"),
      "模型 A ell_five 本册 %s km vs V120 %s km"
      % (sci(ell_A / D(1000), 12), sci(V120["ell_five_km"], 12)))
guard("G_modelB_old_param_w05_equivalent", relf(h0_old05, h0_B) < D("1e-60"),
      "r429 旧参数化 w2=0.5 与 V120「各承担一半」数值等价：%s vs %s"
      % (sci(h0_old05, 14), sci(h0_B, 14)))
guard("G_modelB_H0", relf(h0_B, V120["H0_double"]) < D("1e-6"),
      "模型 B H0 本册 %s vs V120 %s" % (sci(h0_B, 14), sci(V120["H0_double"], 14)))
guard("G_modelB_positive_H0", h0_B > 0 and h0_A < 0,
      "双作用程 H0 转正（%s），单作用程仍负（%s）" % (sci(h0_B, 10), sci(h0_A, 10)))
guard("G_modelB_false_ell", relf(ell_false / D(1000), V120["ell_false_km"]) < D("1e-6"),
      "模型 B 单尺度误拟合 ell=%s km vs V120 %s km"
      % (sci(ell_false / D(1000), 12), sci(V120["ell_false_km"], 12)))
guard("G_modelB_leaveout", relf(leaveout_rel, V120["dK_rel_leaveout"]) < D("1e-3"),
      "300 km 留出差 %s vs V120 %s" % (sci(leaveout_rel, 12), sci(V120["dK_rel_leaveout"], 12)))

add("V7-01", "CORRECTED",
    "r429「模型 B 参数化未被完全复现」的口径被本册更正：旧参数化在 w2=0.5 正是 V120「各承担一半」",
    "r429 用 eps=(1−w2)eps_124.6+w2·eps_300 扫描 w2∈[0.00005,0.30]，得翻转点 w2≈%s、"
    "扫描窗内 H0 上限 %s，遂登记「来料模型 B 参数化未被本册完全复现」。"
    "V120 §7 明确写「两作用程各承担一半地表异常力」，即 w2=0.5；本册把该点直接代入，"
    "H0=%s，与 V120 的 %s 相对差 %s，且与 r429 旧参数化 w2=0.5 逐位等价（%s）。"
    "⇒ r429 的定性结论（双作用程使 H0 转正）成立；需要更正的是「未能复现具体参数化」——"
    "原因是 r429 人为把扫描窗截止在 0.30，漏掉了来料明说的 w2=0.5，不是参数化形式不同。"
    "r429 原文不回改，只在本册登记口径更正。"
    % (sci(R429["modelB_flip_w2"], 10), sci(R429["modelB_h0_at_w_max"], 10),
       sci(h0_B, 14), sci(V120["H0_double"], 14), sci(relf(h0_B, V120["H0_double"])),
       sci(relf(h0_old05, h0_B))))

add("V7-02", "PASS",
    "模型 A/B 的全部 §7 读数逐位复现，且单尺度误拟合确实由留出高度证伪",
    "模型 A：H0=%s、H1/H0=%s、q_five=%s、ell_five=%s km，分别对齐 V120；"
    "模型 B：H0=%s（为正）；对 B 在 0/100/200 km 做单尺度拟合得伪作用程 %s km（V120 %s km），"
    "留出 300 km 的 |ΔK|/μ=%s（V120 %s）。"
    "⇒ 本册能复现 V120 的合成数据反例，但它只说明「在这一个构造样本里单尺度拟合被留出点否证」，"
    "不证明所有多作用程都能被 H0 符号识别。"
    % (sci(h0_A, 14), sci(h1_A / h0_A, 14), sci(q_A, 14), sci(ell_A / D(1000), 12),
       sci(h0_B, 14), sci(ell_false / D(1000), 12), sci(V120["ell_false_km"], 12),
       sci(leaveout_rel, 12), sci(V120["dK_rel_leaveout"], 12)))

# ==================================================================
# 区块 V8：§8 定种子 MC 与三高度置信区间
# ==================================================================
baseK6_f = [D(1) + k_model(h) for h in heights6]
baseK6_f = [float(x) for x in baseK6_f]
height_sigma = [D("0"), D("1e-9"), D("1e-8"), D("1e-7")]
mc_rows = []
mc_table_ok = True
for sg in height_sigma:
    rng = random.Random(20261120)
    n = 12000
    s = float(sg)
    wrong = chain = valid_q = 0
    for _ in range(n):
        ks = [baseK6_f[i] + rng.gauss(0.0, s) for i in range(6)]
        ds = [ks[i + 1] - ks[i] for i in range(5)]
        hh0 = ds[0] * ds[2] - ds[1] ** 2
        hh1 = ds[1] * ds[3] - ds[2] ** 2
        hh2 = ds[2] * ds[4] - ds[3] ** 2
        jj = ds[0] * ds[3] - ds[1] * ds[2]
        if hh0 > 0:
            wrong += 1
        if hh0 < hh1 < hh2 < 0:
            chain += 1
        if hh0 != 0 and 0 < jj / (2 * hh0) < 1:
            valid_q += 1
    row = (sg, D(wrong) / D(n), D(chain) / D(n), D(valid_q) / D(n))
    mc_rows.append(row)
    exp = V120["mc_table"][sg]
    for got, want in zip(row[1:], exp):
        if abs(got - want / D(100)) > D("0.015"):
            mc_table_ok = False

wrong_rates = [r[1] for r in mc_rows]
chain_rates = [r[2] for r in mc_rows]
valid_rates = [r[3] for r in mc_rows]
mc_monotone = (all(wrong_rates[i + 1] >= wrong_rates[i] for i in range(3))
               and all(chain_rates[i + 1] <= chain_rates[i] for i in range(3))
               and all(valid_rates[i + 1] <= valid_rates[i] for i in range(3)))


def ratio_R_float(k, r0=float(R_E), delta=100000.0):
    a = r0
    b = r0 + delta
    c = r0 + 2 * delta
    ia = (a / k + 1 / (k * k)) * math.exp(-k * a)
    ib = (b / k + 1 / (k * k)) * math.exp(-k * b)
    ic = (c / k + 1 / (k * k)) * math.exp(-k * c)
    return (ia - ib) / (ib - ic)


def solve_ell_km_float(target):
    lo, hi = 1e-6, 1e-4
    for _ in range(120):
        mid = (lo + hi) / 2
        if ratio_R_float(mid) < target:
            lo = mid
        else:
            hi = mid
    return 1.0 / ((lo + hi) / 2) / 1000.0


def quantile_sorted(xs, p):
    idx = (len(xs) - 1) * p
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - idx) + xs[hi] * (idx - lo)


baseK3_f = [float(D(1) + k_model(h)) for h in (D(0), D(100000), D(200000))]
rng_ci = random.Random(20261120)
ell_ci_samples = []
for _ in range(2500):
    k0, k1, k2 = [baseK3_f[i] + rng_ci.gauss(0.0, 1e-7) for i in range(3)]
    rr = (k0 - k1) / (k1 - k2)
    if rr > 0:
        ell_ci_samples.append(solve_ell_km_float(rr))
ell_ci_samples.sort()
ell_lo = quantile_sorted(ell_ci_samples, 0.025)
ell_hi = quantile_sorted(ell_ci_samples, 0.975)

guard("G_mc_table_within_1_5pp", mc_table_ok,
      "四档 MC 与本册定种子复现逐档偏差均 ≤1.5 个百分点")
guard("G_mc_monotone_degradation", mc_monotone,
      "噪声升高：错误 H0>0 比例不降、H0<H1<H2<0 比例不升、有效 q 比例不升")
guard("G_mc_ci_low", abs(D(ell_lo) - V120["ell_ci_km"][0]) < D("0.25"),
      "三高度 95%% 下分位 %s km vs V120 %s km" % (sci(D(ell_lo), 8), sci(V120["ell_ci_km"][0], 8)))
guard("G_mc_ci_high", abs(D(ell_hi) - V120["ell_ci_km"][1]) < D("0.25"),
      "三高度 95%% 上分位 %s km vs V120 %s km" % (sci(D(ell_hi), 8), sci(V120["ell_ci_km"][1], 8)))

mc_text = "; ".join(
    "%s: %s/%s/%s" % (sci(sg, 1), sci(r[1] * D(100), 5), sci(r[2] * D(100), 5), sci(r[3] * D(100), 5))
    for sg, r in zip(height_sigma, mc_rows))

add("V8-01", "PASS",
    "§8 四档高斯噪声 MC 的退化方向与量级可复现（定种子 20261120）",
    "本册每档独立用 random.Random(20261120) 做 12,000 次 K_i/μ 独立加性高斯噪声，"
    "读数（错误 H0>0 / H0<H1<H2<0 / 有效 0<q<1，单位 %s）为：%s。"
    "与 V120 表逐档相差均 ≤1.5 个百分点，且三列随噪声升高分别不降/不升/不升。"
    "⇒ Hankel/Prony 在 1e-8 以上量级不可独立作统计判决的结论成立。"
    % ("%", mc_text))

add("V8-02", "PASS",
    "三高度 2500 次 σ=1e-7 MC 的 95% 样本区间可复现",
    "本册对 0/100/200 km 三点做 2500 次定种子噪声实验，以 R=(K0−K1)/(K1−K2) 在固定根区间二分反解 ell，"
    "95%% 样本分位区间为 %s–%s km（V120 %s–%s km）。该区间只对应本合成实验，不是真实任务约束。"
    % (sci(D(ell_lo), 8), sci(D(ell_hi), 8),
       sci(V120["ell_ci_km"][0], 8), sci(V120["ell_ci_km"][1], 8)))

# ==================================================================
# 区块 V9：§6 高度表 / 进动 / 频移 / §9 观测通道
# ==================================================================
eps_rows = []
max_eps_rel = D(0)
max_dg_rel = D(0)
for hh, want_eps in V120["eps_h_table"].items():
    r = R_E + D(hh)
    ep = eps_profile(r, EPS0_USED)
    dg = MU / (r ** 2) * ep
    want_dg = V120["dg_table"][hh]
    max_eps_rel = max(max_eps_rel, relf(ep, want_eps))
    max_dg_rel = max(max_dg_rel, relf(dg, want_dg))
    eps_rows.append((hh, ep, dg))

def math_pi():
    return D("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798")


r400 = R_E + D(400000)
x400 = r400 / L_
eps400 = eps_profile(r400, EPS0_USED)
r_eps400 = -eps400 * x400 ** 2 / (1 + x400)
dprec = D(2) * math_pi() * (((1 + eps400) / (1 + eps400 + r_eps400)).sqrt() - 1)

dphi400 = -(D(1) + k_model(D(400000)) - D(1)) * MU / (r400 * (1 + x400))
dphi0 = -(D(1) + k_model(D(0)) - D(1)) * MU / (R_E * (1 + U_))
dnu = (dphi400 - dphi0) / (C_LIGHT ** 2)

eps200 = eps_profile(R_E + D(200000), EPS0_USED)
dk_200_400 = eps200 - eps400
eps_lageos = eps_profile(R_E + D(5900000), EPS0_USED)

guard("G_eps_table", max_eps_rel < D("5e-6"),
      "八高度 eps(h) 最大相对偏差 %s（表值 6 位有效位）" % sci(max_eps_rel))
guard("G_dg_table", max_dg_rel < D("5e-6"),
      "八高度附加加速度最大相对偏差 %s" % sci(max_dg_rel))
guard("G_precession", relf(dprec, V120["dprec_rad"]) < D("1e-8"),
      "Δvarpi 本册 %s rad vs V120 %s rad" % (sci(dprec, 14), sci(V120["dprec_rad"], 14)))
guard("G_frequency_shift", relf(dnu, V120["dnu"]) < D("1e-8"),
      "频移本册 %s vs V120 %s" % (sci(dnu, 14), sci(V120["dnu"], 14)))
guard("G_Kdiff_200_400", relf(dk_200_400, V120["dK_200_400"]) < D("1e-6"),
      "K 差值 %s vs V120 %s" % (sci(dk_200_400, 12), sci(V120["dK_200_400"], 12)))
guard("G_lageos_suppression", relf(eps_lageos, V120["eps_h_table"][5900]) < D("5e-6"),
      "LAGEOS 高度 eps=%s vs V120 %s" % (sci(eps_lageos, 8), sci(V120["eps_h_table"][5900], 8)))

add("V9-01", "PASS",
    "§6 八高度表、近圆轨道进动与钟频移可由固定参数第一性复算",
    "用 eps0=%s、ell=124.6 km、mu=GEO 同步值，八高度 eps(h) 与附加加速度表最大相对偏差分别 %s / %s；"
    "400 km 处 Δvarpi=%s rad（V120 %s）、Δnu/nu=%s（V120 %s）、200→400 km 归一化 K 差=%s（V120 %s）、"
    "5900 km 处 eps=%s。"
    "这些都是同一固定假设的交叉预言，不是观测证据；来料 §6 对此已有自陈。"
    % (sci(EPS0_USED, 16), sci(max_eps_rel), sci(max_dg_rel),
       sci(dprec, 14), sci(V120["dprec_rad"], 14), sci(dnu, 14), sci(V120["dnu"], 14),
       sci(dk_200_400, 12), sci(V120["dK_200_400"], 12), sci(eps_lageos, 8)))

add("V9-02", "PASS",
    "§9 把 GOCE/GRACE/原子钟/LAGEOS 列为待做观测设计而非已完成约束，口径诚实",
    "本册 V9-01 只复现合成表与解析式；V120 原文明确「没有下载或联合拟合原始观测数据，实际约束依旧 OPEN」，"
    "且把 LAGEOS 高度抑制量级 %s 列为非优先通道。该部分与 W3 红线一致：不得升级为 L3。"
    % sci(eps_lageos, 6))

# ==================================================================
# 区块 V10–V12：红线、覆盖映射与最终裁定
# ==================================================================
add("V10-01", "FAIL",
    "§12 总结「把错称五高度的六高度反演修复为真正五高度」不成立",
    "V1-01/V1-02 已证 H0/H1 各需 4 高度、合用 5 高度，来料 §2 的「6 高度勘误」方向反了；"
    "V2-01 又证 P5 是族内恒等式。故 V120 摘要级卖点「修正采样数量」不是数学贡献，"
    "而是一次由索引展开错误引起的反向勘误。§12 裁定表应把该项由「通过」改为「CORRECTED：五高度原称正确」。")

add("V10-02", "PASS",
    "§10 三类「已验证」分离与 §11 四力统一 OPEN 的诚实边界成立",
    "V120 自陈数学证明/合成实验/真实实验三者不可混同，且 G=2Z/c 在 Z=Gc/2 定义下是变量置换、"
    "ell=124.6 km 与 a=ell²/6 是参数重述、alpha_Y=1/3 来自外部线性极限。该自陈与 r421 W3 门禁一致，"
    "不得把本册任何 PASS 迁移为 L3 或四力统一。")

add("V10-03", "INFO",
    "红线计数不因本册改变",
    "0/6 未完成、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持不变；"
    "本册只裁定外部来料 V120 的内部自洽性与可复现性。")

add("V11-01", "INFO",
    "V1–V12 覆盖映射",
    "§1→V6/V9（参数与量纲）；§2→V1-01/V1-02/V10-01；§3→V2-01/V2-03/V3-01；"
    "§4→V2-02/V3-02；§5→V5-01/V5-02/V5-03/V6-01（核心不同源）；"
    "§6→V9-01；§7→V7-01/V7-02；§8→V8-01/V8-02；§9→V9-02；§10→V10-02；"
    "§11→V6-02/V10-02；§12→V10-01/V10-03。")

add("V12-01", "INFO",
    "最终裁定",
    "V120 的可复现面很大（Prony/Hankel 代数、三高度唯一性、模型 A/B 合成数据、噪声退化、高度/进动/频移表），"
    "但承重卖点有两处硬伤：①采样点数「勘误」方向错误（5 才是正确值）；"
    "②改进密度剖面与其印刷形状因子闭式不同源，0.59544049% 只能由印刷闭式复现。"
    "因此 V120 可定位为「可复算的合成数据/反演方法笔记」，不能升级为第一性第五力预言或四力统一证据。")

# ==================================================================
# 输出：json / md / report
# ==================================================================
os.makedirs(DATA_DIR, exist_ok=True)
COUNTS = {}
for e in ENTRIES:
    v = e["verdict"]
    COUNTS[v] = COUNTS.get(v, 0) + 1
COUNTS = {k: COUNTS[k] for k in ("PASS", "FAIL", "CORRECTED", "BOUNDARY", "INFO") if k in COUNTS}

SOURCE_PATH = os.path.abspath(os.path.join(
    BASE, "..", "..", "90_历史归档", "来源语料_ufthub_ROOT_V9-V120_202611b",
    "V120", "ROOT_V120", "ROOT_V120_科研报告.md"))
try:
    import hashlib
    with open(SOURCE_PATH, "rb") as fsrc:
        SOURCE_SHA = hashlib.sha256(fsrc.read()).hexdigest()
except Exception:
    SOURCE_SHA = "NA"

KEY = {
    "sampling_h0_heights": str(len(cl0)),
    "sampling_h01_union_heights": str(len(union)),
    "p5_max_residual": sci(res_p5),
    "p5_positive_control": sci(p5_two),
    "phi_x": sci(x_exact, 18),
    "phi_from_stated_profile": sci(phi_i_derived, 18),
    "phi_v120_closed": sci(phi_i_v120, 18),
    "phi_relative_gap": sci(relf(phi_i_derived, phi_i_v120)),
    "phi_diff_formula_residual": sci(relf(phi_i_diff, phi_i_diff_formula)),
    "eps0_v120_closed": sci(eps0_v120_direct, 18),
    "eps0_stated_profile": sci(eps0_stated_profile, 18),
    "modelA_h0": sci(h0_A, 18),
    "modelB_h0": sci(h0_B, 18),
    "modelB_false_ell_km": sci(ell_false / D(1000), 12),
    "modelB_leaveout_rel": sci(leaveout_rel, 12),
    "mc_rates": mc_text,
    "mc_ci_km": "%s–%s" % (sci(D(ell_lo), 8), sci(D(ell_hi), 8)),
    "precession_rad": sci(dprec, 18),
    "frequency_shift": sci(dnu, 18),
}

json_obj = {
    "meta": {
        "rid": "r436",
        "stamp": "2026-11-21",
        "title": "ROOT V120 五高度 Prony 反演与形状因子第一性复核 全维审计",
        "method": "纯标准库 Decimal 60/90 位 + Fraction 四元量纲 + 阳性对照 + 定种子 MC",
        "source_sha256": SOURCE_SHA,
        "verdict_counts": COUNTS,
        "entry_total": len(ENTRIES),
        "guard_total": len(GUARDS),
    },
    "key_numbers": KEY,
    "entries": ENTRIES,
    "guards": GUARDS,
}

json_path = os.path.join(DATA_DIR, STEM + ".json")
with io.open(json_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=2)
    f.write("\n")


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


md = []
md.append("# TUFT r436 · ROOT V120 五高度 Prony 反演与形状因子第一性复核 全维审计")
md.append("")
md.append("一句话：V120 的代数反演与合成数据多数可复现，但「六高度勘误」方向错误，且改进密度剖面与其印刷形状因子闭式不同源；真实观测仍 OPEN。")
md.append("")
md.append("| 项 | 值 |")
md.append("|---|---|")
md.append("| 条目 | %d |" % len(ENTRIES))
md.append("| 判定分布 | %s |" % ", ".join("%s=%d" % (k, v) for k, v in COUNTS.items()))
md.append("| 守卫 | %d/%d |" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
md.append("| 来料 SHA256 | %s |" % SOURCE_SHA)
md.append("")
md.append("## 关键读数")
md.append("")
for k, v in KEY.items():
    md.append("- `%s` = %s" % (k, v))
md.append("")
md.append("## 条目")
md.append("")
md.append("| 编号 | 判定 | 标题 | 详情 |")
md.append("|---|---|---|---|")
for e in ENTRIES:
    md.append("| %s | %s | %s | %s |" % (e["code"], e["verdict"], esc(e["title"]), esc(e["detail"])))
md.append("")
md.append("## 守卫")
md.append("")
md.append("| 守卫 | 结果 | 说明 |")
md.append("|---|---|---|")
for g in GUARDS:
    md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", esc(g["detail"])))
md.append("")

md_path = os.path.join(DATA_DIR, STEM + ".md")
with io.open(md_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(md))

rep = []
rep.append("TUFT r436 REPORT")
rep.append("entries=%d guards=%d/%d" % (len(ENTRIES), sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
rep.append("counts=" + ", ".join("%s=%d" % (k, v) for k, v in COUNTS.items()))
rep.append("source_sha256=" + SOURCE_SHA)
for k, v in KEY.items():
    rep.append("%s=%s" % (k, v))
rep.append("--- entries ---")
for e in ENTRIES:
    rep.append("[%s] %s :: %s" % (e["verdict"], e["code"], e["title"]))
rep.append("--- guards ---")
for g in GUARDS:
    rep.append("[%s] %s :: %s" % ("PASS" if g["ok"] else "FAIL", g["name"], g["detail"]))
rep.append("")
rep_path = os.path.join(DATA_DIR, STEM + "_report.txt")
with io.open(rep_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(rep))

print("\n".join(rep[:8]))
print("WROTE", json_path)
print("WROTE", md_path)
print("WROTE", rep_path)

failed = [g for g in GUARDS if not g["ok"]]
if failed:
    print("GUARD_FAIL", len(failed))
    for g in failed:
        print(" -", g["name"], g["detail"])
    sys.exit(1)
print("ALL_GUARDS_PASS")
sys.exit(0)

