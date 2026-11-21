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
DIM_EPS0 = (Fraction(-2), Fraction(0), Fraction(0), Fraction(0))   # 真空介电常数
DIM_MU0 = (Fraction(-2), Fraction(2), Fraction(2), Fraction(-2))   # 真空磁导率


def dim_mul(a, b):
    return tuple(a[i] * b[i] for i in range(4))


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
        rho = 1.25 - t + 1.0 / (3.0 * t)
        return t * rho * math.sinh(xf * t)
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
        hi = D("1e-1")
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

# __SEG2__
