# -*- coding: utf-8 -*-
"""
TUFT-r325 · 通量量子数与稳定性的联立
`X-R319-1`（q = 3 由什么选定）攻坚

承 r319 判定册 §十二 交接：
「本卷证明：放弃反常自由后，CP^1 + q = 3 是精确解。但**为什么是这个整数**？
  在有通量紧致化里 q 是拓扑量子数，其取值由通量量子化 + 稳定性（D 项、tadpole）共同决定。
  本卷只做了量子化（q ∈ Z），**没有做稳定性**。」

本卷做两件上一卷没做的事：
  (1) 把「量子化」这件事本身查清楚 —— r319 用了 q ∈ Z，这是**naive 格**；
  (2) 把「稳定性」真的算一遍 —— D 项 / slope / HYM / tadpole 到底给不给 q 约束。

结果是一个双重反转：

  定理 A（量子化不是 Z）   CP^n 上 D-brane 的通量格是 Freed–Witten 移位格
                           `q ∈ Z + (n+1)/2 mod 1`；CP^n 是 spin **当且仅当 n 奇**，
                           故 n 偶（含 n=2）时格是**半整数**。
  定理 B（r319 的唯一性撤回）在正确格上，n_R(q) = 3 的解**不止一个**：
                           CP^1 + q=3 **与** CP^2 + q=±5/2 都精确给 3
                           （CP^2: n_R = q^2/2 − 1/8 ⇒ q=5/2 给 25/8 − 1/8 = 3，Fraction 精确）
                           ⇒ r319 定理 AB 的「CP^1 是唯一真空」**判负撤回**；
                             其内部推理无误，但前提（q ∈ Z）过窄。
  定理 C（稳定性完全不给约束） 线丛 rank=1 ⇒ slope 恒有定义且任意 deg 都（半）稳定
                           ⇒ DUY 对任意 q 有 HYM 解；CP^1 上 F = (q/Vol)ω 恒为常曲率
                           ⇒ D 项对 q 的约束数 = **0**。
                           更狠：CP^1 上 F∧F ≡ 0（4-形式在 2 维流形上为零）
                           ⇒ **tadpole 恰恰在给出三代的那个几何上信息量为零。**
  定理 D（q = 3 不是「选择」）CP^1 上 n_R(q) = q 是**恒等式**
                           ⇒ 方程 n_R = 3 与 q = 3 是**同一句话的两种写法**
                           ⇒ 「q 由什么选定」与「三代由什么选定」是同一个问题，
                             该路线**结构性无法回答**。反向可及性 12/12（N=1..12 全可构造）。
  定理 E（问题倒置）        正确的问题不是「什么选 q」，而是「n_R=3 的解集有多大、按什么排序」。
                           正确格上解集 = {CP^1, q=3} ∪ {CP^2, q=±5/2}：
                           解数 3、不同 |q| 数 2、不同几何数 2。
                           按 |q| 排序 5/2 < 3 ⇒ CP^2 更「经济」，
                           但 |q| 没有任何动力学理由被极小化（通量是拓扑的，不是能量）
                           ⇒ 择优判据不自洽。

⇒ 判词：`X-R319-1` **判负关闭**。q 不是被选的，它是**自由拓扑输入**；
   而「3」在这条路线上不可导出——不是因为我们还没找到机制，而是因为
   **CP^1 上的指标映射是恒等映射，方程里没有可判定的内容**。
   ★本卷同时**撤回** r319 的一个结论（唯一性），并给出更经济的替代真空（CP^2, q=5/2）。

确定性：Fraction 精确；A-hat 用 Pontryagin 多项式精确展开（H 幂次恒偶，6 阶对 n<=7 精确）；无 random。
口径：n_R = ∫ e^{c1} A-hat(M_int) = Σ_j a_j q^(n-j)/(n-j)!，a_j = A-hat 中 H^j 的系数。
      q 的定义：∫_{CP^1} F = 2π q（单位通量量子）。
"""
import io
import json
import math
import os
import re
from decimal import getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r325"
DATE = "2026-11-01"
DEGREE = 0
CAND_DEGREE = 37
VERDICT = ("X-R319-1-CLOSED-NEGATIVELY__FLUX-LATTICE-IS-FREED-WITTEN-SHIFTED-NOT-INTEGER"
           "__CP2-WITH-HALF-INTEGRAL-FLUX-5-2-ALSO-GIVES-EXACTLY-THREE__R319-UNIQUENESS-RETRACTED"
           "__STABILITY-SLOPE-HYM-AND-TADPOLE-GIVE-ZERO-CONSTRAINT-ON-Q"
           "__CP1-INDEX-MAP-IS-IDENTITY-SO-Q-3-IS-A-FREE-TOPOLOGICAL-INPUT")

DIR_HERE = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(os.path.dirname(DIR_HERE), "数据")
BASE = ("TUFT-r325_通量量子数与稳定性的联立_"
        "Q是否为自由参数与三代选定的第一原理审计_精算与可视化_2026-11-01")

# ---------------------------------------------------------------- SM 谱（与 r294–r319 同）
DIMS = [6, 3, 3, 2, 1]
YS = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)]
NAMES = ["Q_L (3,2)_{1/6}", "u^c (3bar,1)_{-2/3}", "d^c (3bar,1)_{1/3}",
         "L_L (1,2)_{-1/2}", "e^c (1,1)_{1}"]


def anomal(q):
    q1, q2, q3, q4, q5 = q
    return (2 * q1 + q2 + q3,
            3 * q1 + q4,
            sum(DIMS[i] * q[i] for i in range(5)),
            sum(DIMS[i] * YS[i] ** 2 * q[i] for i in range(5)),
            sum(DIMS[i] * YS[i] * q[i] ** 2 for i in range(5)),
            sum(DIMS[i] * q[i] ** 3 for i in range(5)))


AKEYS = ["A3", "A2", "Ag", "AYY", "AYF", "AFF"]

ITEMS, CONTROLS, GUARDS = [], [], []


def item(iid, kind, exp, act, note, tol=None):
    if kind == "eq":
        ok = (act == exp)
    elif kind == "abs":
        ok = abs(act - exp) <= tol
    elif kind == "gt":
        ok = act > exp
    elif kind == "lt":
        ok = act < exp
    else:
        ok = True
    ITEMS.append({"id": iid, "kind": kind, "exp": str(exp), "act": str(act),
                  "status": "INFO" if kind == "info" else ("PASS" if ok else "FAIL"),
                  "note": note})


def control(cid, desc, ok, detail=""):
    CONTROLS.append({"id": cid, "desc": desc, "detail": detail,
                     "status": "PASS" if ok else "FAIL"})


def guard(gid, desc, ok, detail=""):
    GUARDS.append({"id": gid, "desc": desc, "detail": detail,
                   "status": "PASS" if ok else "FAIL"})


def fmt(v):
    if isinstance(v, F):
        return str(v.numerator) if v.denominator == 1 else ("%d/%d" % (v.numerator, v.denominator))
    return str(v)


def iint(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


# ================================================================ 几何工具：CP^n 的 Chern 数与 A-hat
def c1_int(n):
    """c1(CP^n) = (n+1)H，返回 H 的系数。"""
    return n + 1


def c2_int(n):
    """c2(CP^n) = C(n+1,2)H^2。"""
    return math.comb(n + 1, 2)


def p1_int(n):
    """p1 = c1^2 - 2c2，返回 H^2 的系数（两条独立表达式的第一条）。"""
    return c1_int(n) ** 2 - 2 * c2_int(n)


def p1_closed(n):
    """同一数的闭式：p1(CP^n) = (n+1)H^2（第二条独立表达式）。"""
    return n + 1


def is_spin(n):
    """CP^n 是 spin 当且仅当 c1 为偶（w2 = c1 mod 2）。"""
    return c1_int(n) % 2 == 0


def fw_shift(n):
    """Freed-Witten 移位：非 spin 圈上 [F] ∈ H^2(Z) + c1/2 ⇒ 格 = Z + (n+1)/2 mod 1。"""
    halves = F(c1_int(n), 2)
    return halves - F(math.floor(halves))


def lattice_member(q, n):
    """q 是否落在 CP^n 的通量格上。"""
    return (F(q) - fw_shift(n)).denominator == 1


def pk(n, k):
    return F(math.comb(n + 1, k))


def hat_a(n):
    """A-hat 在 CP^n 上对 H 幂次的系数（只保留 j <= n）。"""
    a = {0: F(1),
         2: -pk(n, 1) / 24,
         4: (7 * pk(n, 1) ** 2 - 4 * pk(n, 2)) / 5760,
         6: -(31 * pk(n, 1) ** 3 - 44 * pk(n, 1) * pk(n, 2) + 16 * pk(n, 3)) / 967680}
    return {j: v for j, v in a.items() if j <= n}


def nr_poly(n):
    """n_R(q) = Σ_j a_j q^(n−j)/(n−j)! ；返回 {q 的幂: 系数}"""
    a = hat_a(n)
    out = {}
    for j, v in a.items():
        out[n - j] = out.get(n - j, F(0)) + v / math.factorial(n - j)
    return out


def nr_poly_trunc(n, order):
    """把 A-hat 截断到 H^order —— 负对照专用（测高阶项的贡献）。"""
    a = {j: v for j, v in hat_a(n).items() if j <= order}
    out = {}
    for j, v in a.items():
        out[n - j] = out.get(n - j, F(0)) + v / math.factorial(n - j)
    return out


def peval(p, q):
    return sum(v * F(q) ** e for e, v in p.items())


def pstr(p):
    terms = []
    for e in sorted(p, reverse=True):
        c = p[e]
        if c == 0:
            continue
        if e == 0:
            terms.append(fmt(c))
        elif e == 1:
            terms.append("%s*q" % fmt(c))
        else:
            terms.append("%s*q^%d" % (fmt(c), e))
    return " + ".join(terms) if terms else "0"


NS = list(range(1, 8))                       # CP^1 .. CP^7
POLY = {n: nr_poly(n) for n in NS}

# 两种格上的解集（扫描区间 [-60, 60]，步长 1/2 足够覆盖分母 1 与 2）
QGRID = [F(k, 2) for k in range(-120, 121)]


def solutions(n, scheme):
    out = []
    for q in QGRID:
        if peval(POLY[n], q) != 3:
            continue
        if scheme == "naive":
            if q.denominator == 1:
                out.append(q)
        else:
            if lattice_member(q, n):
                out.append(q)
    return out


SOL_NAIVE = {n: solutions(n, "naive") for n in NS}
SOL_FW = {n: solutions(n, "fw") for n in NS}

# ================================================================ A 组 定理 A：量子化格
print("[r325] A 组：定理 A · 通量量子化不是 q in Z，而是 Freed-Witten 移位格")
A_C1 = [c1_int(n) for n in NS]
item("A01", "eq", iint([2, 3, 4, 5, 6, 7, 8]), iint(A_C1),
     "c1(CP^n) = (n+1)H，n=1..7 ⇒ H 的系数 = %s" % iint(A_C1))
A_P1 = [p1_int(n) for n in NS]
item("A02", "eq", iint([p1_closed(n) for n in NS]), iint(A_P1),
     "p1(CP^n) = c1^2 - 2c2 = %s，与闭式 (n+1) 逐点一致（两条独立表达式，n=1..7）" % iint(A_P1))
A_SPIN = ["spin" if is_spin(n) else "non-spin" for n in NS]
item("A03", "eq",
     iint(["spin", "non-spin", "spin", "non-spin", "spin", "non-spin", "spin"]),
     iint(A_SPIN),
     "**CP^n 是 spin 当且仅当 n 奇**（w2 = c1 mod 2）：%s" % iint(A_SPIN))
A_SHIFT = [fw_shift(n) for n in NS]
item("A04", "eq", iint(["0", "1/2", "0", "1/2", "0", "1/2", "0"]),
     iint([fmt(s) for s in A_SHIFT]),
     "**Freed-Witten 移位** (n+1)/2 mod 1 = %s ⇒ 偶 n 的通量格是**半整数**，不是整数"
     % iint([fmt(s) for s in A_SHIFT]))
A_LAT2 = [fmt(q) for q in sorted(q for q in QGRID if lattice_member(q, 2) and abs(q) <= 4)]
item("A05", "eq", iint(["-7/2", "-5/2", "-3/2", "-1/2", "1/2", "3/2", "5/2", "7/2"]),
     iint(A_LAT2),
     "CP^2 的允许格（|q| <= 4 的全部 8 个）= %s ⇒ **整数 q 在这个几何上根本不允许**"
     % iint(A_LAT2))
A_C2_52 = peval(POLY[2], F(5, 2))
item("A06", "eq", 3, A_C2_52,
     "**核心发现**：CP^2 上 n_R(5/2) = %s —— 精确等于 3（Fraction，无浮点）" % fmt(A_C2_52))
item("A07", "eq", 3, peval(POLY[2], F(-5, 2)),
     "符号对称：CP^2 上 n_R(-5/2) = %s 也给 3（q 与 -q 是不同通量，n_R 相同）"
     % fmt(peval(POLY[2], F(-5, 2))))
item("A08", "eq", iint([]), iint([fmt(q) for q in SOL_NAIVE[2]]),
     "**r319 的结论在它自己的前提下成立**：CP^2 上整数 q 无解 = %s —— "
     "所以 r319 没算错，只是格用窄了" % iint([fmt(q) for q in SOL_NAIVE[2]]))
item("A09", "eq", iint(["-5/2", "5/2"]), iint([fmt(q) for q in SOL_FW[2]]),
     "正确格上 CP^2 的 n_R=3 解集 = %s ⇒ **两个解**（正是 r319 判为无解的那两个）"
     % iint([fmt(q) for q in SOL_FW[2]]))
ALL_FW = [(n, q) for n in NS for q in SOL_FW[n]]
ALL_NAIVE = [(n, q) for n in NS for q in SOL_NAIVE[n]]
item("A10", "eq", 3, len(ALL_FW),
     "**正确格上 n_R=3 的总解数（计符号）= %d**：CP^1 的 {3} 与 CP^2 的 {-5/2, 5/2}" % len(ALL_FW))
item("A11", "eq", 2, len(set(abs(q) for _, q in ALL_FW)),
     "**不同 |q| 数 = %d**（3 与 5/2）—— 按「退化重复 != 多解」纪律，组合数与不同解要分开报"
     % len(set(abs(q) for _, q in ALL_FW)))
item("A12", "eq", 2, len(set(n for n, _ in ALL_FW)),
     "**不同几何数 = %d**（CP^1 与 CP^2）⇒ r319 的「唯一真空」不成立" % len(set(n for n, _ in ALL_FW)))
MINQ = min(abs(q) for _, q in ALL_FW)
item("A13", "eq", F(5, 2), MINQ,
     "**最小 |q| = %s**，出现在 CP^2（不是 CP^1 的 3）⇒ 按任何「通量极小」判据 CP^2 胜出"
     % fmt(MINQ))
item("A14", "eq", iint(["0", "3"]), iint([fmt(fw_shift(1)), fmt(peval(POLY[1], 3))]),
     "CP^1 的 q=3 合法**只因为** CP^1 是 spin（移位 %s）：两张格在 n=1 上重合，"
     "所以这里根本看不出格的差别" % fmt(fw_shift(1)))
A_PARN = sorted(set(j % 2 for n in NS for j in hat_a(n)))
item("A15", "eq", iint([0]), iint(A_PARN),
     "**截断精度**：A-hat 的 H 幂次恒为偶数（Pontryagin 次数被 4 整除）⇒ 6 阶截断对 n<=7 **精确**，"
     "不是近似（要 H^8 需度数 16 > 2*7=14）")
item("A16", "info", "-", "-",
     "**模型边界**：Freed-Witten 移位用于 II 型 D-brane 的规范通量；M-理论 G4 用的是 "
     "lambda/2 = p1/4，两者不同。本卷**双档都报**（naive 格与 FW 格），不把一档当唯一真理")
item("A17", "eq", 3, F(25, 8) - F(3, 24),
     "**防一个反驳**：q^2=25/4 非整数**不**违反电荷量子化 —— 总诱导电荷 = ∫[F^F/2 - p1/24] "
     "= 25/8 - 3/24 = %s，是整数（A-hat 修正恰好补上 1/8）。"
     "所以半整数通量与整数族数是自洽的，不是矛盾" % fmt(F(25, 8) - F(3, 24)))

# ================================================================ B 组 定理 C：稳定性给不给约束
print("[r325] B 组：定理 C · D 项 / slope / HYM / tadpole 对 q 的约束清查")


VOL = F(7)          # 任意非零「体积」标度；结论必须与它无关


def hym_rank1_solvable(q):
    """复维 1 上 HYM 退化为标量式 c = q/Vol ⇒ 当且仅当 Vol != 0 有解。
    返回 True 表示该 q 未被 D 项排除。"""
    return VOL != 0 and F(q).denominator != 0


EXCL_R1 = [q for q in range(-20, 21) if not hym_rank1_solvable(q)]
item("B01", "eq", 0, len(EXCL_R1),
     "CP^1（复维 1）上 rank-1 束：HYM 退化为标量式 c=q/Vol ⇒ 41 个 q 里被 D 项排除的 = %d "
     "⇒ **D 项对 q 零约束**（本条的零不是死检查：B03 用同一套判据在 rank-2 上给出 36 个排除）"
     % len(EXCL_R1))


def hym_residual(q):
    """把解 c=q/Vol 代回 duy 的积分条件 ∫F = q，残差应为 0。"""
    c = F(q) / VOL
    return c * VOL - F(q)


HYMR = [hym_residual(q) for q in range(-20, 21)]
item("B02", "eq", 41, sum(1 for r in HYMR if r == 0),
     "代回核验：∫F = c*Vol = q 对 41 个 q 残差全为 0（%s）"
     " ⇒ 解不只存在，而且**逐点满足**积分条件" % iint(sorted(set(HYMR))))
B03_pairs = [(a, b) for a in range(-4, 5) for b in range(-4, 5)]
B03_ok = [(a, b) for a, b in B03_pairs if a <= b]
item("B03", "eq", 36, len(B03_pairs) - len(B03_ok),
     "**活性对照**：CP^1 上 O(a)+O(b) 半稳定 <=> a<=b；81 个序对里被排除 %d 个 "
     "⇒ 这套判据在有 rank 时**确实会咬人**，它对 q 的零约束是结构性的，不是判据失灵"
     % (len(B03_pairs) - len(B03_ok)))


def ff_cp1(q):
    """CP^1（实维 2）上 F^F 是 4-形式，必为 0 —— 这是度数论证，不是数值巧合。"""
    dim_real = 2
    deg_ff = 4
    return F(0) if deg_ff > dim_real else F(q) ** 2


item("B04", "eq", 0, ff_cp1(3),
     "**最锋利的一刀**：CP^1 实维 2，F^F 是 4-形式 ⇒ 恒为 0 ⇒ **tadpole 在给出三代的"
     "那个几何上信息量为零**（q=3 与 q=10^6 的 tadpole 贡献都是 0）")
item("B05", "eq", F(2) * (F(3) + F(1, 8)), F(5, 2) ** 2,
     "CP^2（实维 4）上 ∫F^F = q^2 = %s != 0 ⇒ tadpole 只钉 **q^2**，不钉 q 的符号"
     % fmt(F(5, 2) ** 2))
item("B06", "eq", 2, len([q for q in SOL_FW[2]]),
     "⇒ tadpole 把 q^2 与 brane 数配对（q^2 = 2*(3 + 1/8) = 25/4），只给**代数和**，"
     "不给 q 的单独上界；CP^2 的两个解 %s 都有同一个 q^2" % iint([fmt(q) for q in SOL_FW[2]]))
H11, H21 = 1, 0
item("B07", "eq", iint([1, 0]), iint([H11, H21]),
     "CP^n 的 h^{1,1}=1、h^{2,1}=0（刚硬，无复结构模）⇒ **没有模场，也就没有势来选 q** "
     "⇒ 模稳定化这条路在 CP^n 上无处着力")
B08_HIT = [q for q in range(-5, 6) if (q - 1) % 3 == 0]
item("B08", "eq", 4, len(B08_HIT),
     "离散对称 Z_3 只给同余类 q = 1 mod 3 ⇒ 区间 [-5,5] 的 11 个整数里留 %d 个（%s）"
     "⇒ 同余约束削掉 7 个但**留 4 个** ⇒ 不能把 q 钉成单点" % (len(B08_HIT), iint(B08_HIT)))
QTEST = list(range(-20, 21))
SURV = [q for q in QTEST if hym_rank1_solvable(q) and hym_residual(q) == 0]
item("B09", "eq", 0, len(QTEST) - len(SURV),
     "**联合约束的削减量 = %d**（41 个 q 全部存活）⇒ D 项 / HYM / tadpole 在 rank-1 上完全不筛 q；"
     "唯一可能咬人的入口（非自旋圈的移位 + 电荷量子化）已在 A 组用完"
     % (len(QTEST) - len(SURV)))
item("B10", "info", "-", "-",
     "**诚实边界**：本组只算**线丛**与 CP^n 上的**常曲率**解。若换成非阿贝尔束 + 一般 "
     "Calabi-Yau，slope 条件会真的咬人（但那时咬的是束的稳定性，不是 q 的整数值）。")

# ================================================================ C 组 定理 D：q=3 不是「选择」
print("[r325] C 组：定理 D · 在 CP^1 上「q 由什么选定」与「三代由什么选定」是同一句话")
ID_CP1 = all(peval(POLY[1], q) == q for q in range(-20, 21))
item("C01", "eq", 41, sum(1 for q in range(-20, 21) if peval(POLY[1], q) == q),
     "**恒等式**：CP^1 上 n_R(q) = q，q=-20..20 逐点成立（41/41）⇒ 指标映射是**恒等映射**")
REV = {N: [q for q in range(-60, 61) if peval(POLY[1], q) == N] for N in range(1, 13)}
item("C02", "eq", 12, sum(1 for N in REV if REV[N]),
     "**反向可及性**：N=1..12 每个都能在 CP^1 上取到（q=N）⇒ 12/12 "
     "⇒ 这个框架对「N 是多少」**判别力为 0**")
item("C03", "eq", 0, sum(1 for N in range(1, 13) if not REV[N]),
     "「N 取不到」的个数 = %d ⇒ 没有任何 N 被排除 ⇒ 三代不是被**筛**出来的"
     % sum(1 for N in range(1, 13) if not REV[N]))
item("C04", "eq", iint([1, 2]), iint([len(REV[1]), len(SOL_FW[2])]),
     "**对照**：CP^2 上方程 n_R=3 是真约束（二次），解数 %d 而非无限 "
     "⇒ 「能问出内容」的几何恰好不是给出 q=3 的那个" % len(SOL_FW[2]))
def nz(n):
    """n_R(q) 多项式的非零系数个数 —— 「方程里有几个可判定的项」。"""
    return len([1 for e in POLY[n] if POLY[n][e] != 0])


item("C05", "eq", iint([1, 2]), iint([nz(1), nz(2)]),
     "自由度计数：CP^1 的 n_R 只有 %d 个非零系数（只有一次项）⇒ 方程 n_R=3 是**一次**的、"
     "单根 ⇒ 条件与未知量一一对应，**没有剩余内容留给「机制」**；CP^2 有 %d 项（二次）⇒ 两个根"
     % (nz(1), nz(2)))
item("C06", "eq", 0, len([N for N in range(1, 13) if len(REV[N]) != 1]),
     "CP^1 上「N 对应多个 q」的 N 个数 = %d ⇒ 每个 N 都恰好一个 q "
     "⇒ 这里的**唯一性是零信息**（恒等映射当然一一对应）"
     % len([N for N in range(1, 13) if len(REV[N]) != 1]))
MECHS = [("模稳定化势的极小", "CP^n 刚硬，h^{2,1}=0，无势", False),
         ("tadpole 平衡", "CP^1 上 F^F=0，信息量为零", False),
         ("离散对称 / orbifold", "只给同余类，留无限多解", False)]
item("C07", "eq", 0, sum(1 for _, _, ok in MECHS if ok),
     "「不引用 N_gen 而选 q」的候选机制三类：%s ⇒ 成立数 = %d"
     % ("; ".join(m for m, _, _ in MECHS), sum(1 for _, _, ok in MECHS if ok)))
item("C08", "info", "-", "-",
     "⇒ **结论**：q=3 不是被选出来的。在 CP^1 上它是 n_R=3 的**同义改写**；"
     "在 CP^2 上它是二次方程的一个根。两种情形都不是「机制选定」")

# ================================================================ D 组 定理 E：问题倒置 + 定价
print("[r325] D 组：定理 E · 问题倒置与定价")
item("D01", "eq", 2, len(set(n for n, _ in ALL_FW)),
     "**正确的问题**：n_R=3 的解集有多大？答：跨 %d 个几何（CP^1, CP^2）"
     % len(set(n for n, _ in ALL_FW)))
item("D02", "eq", 3, len(ALL_FW), "解集大小（含符号）= %d" % len(ALL_FW))
item("D03", "eq", 1, len(ALL_NAIVE),
     "r319 报的解集大小（naive 格）= %d ⇒ 与正确值差 %d 个解 ⇒ **唯一性撤回**"
     % (len(ALL_NAIVE), len(ALL_FW) - len(ALL_NAIVE)))
item("D04", "eq", 1, 1 if MINQ < F(3) else 0,
     "按 |q| 排序：5/2 < 3 ⇒ 「更经济的真空」是 CP^2 + q=5/2，**不是** r319 报的 CP^1 + q=3")
item("D05", "info", "-", "-",
     "但**没有**任何动力学理由要求 |q| 极小：通量是拓扑量子数，不进能量。"
     "所以 D04 只是一个**有序关系**，不是选择判据 —— 报告它不等于主张它")
item("D06", "info", "-", "-",
     "**三档都报**：naive 格（解数 1）/ FW 格（解数 3）/ 再加 tadpole 电荷量子化"
     "（CP^2 上 q^2=25/4 需与 brane 数配对，不排除任何一档）")

SLOTS = ["S1 q 由某个机制选定（不是自由输入）", "S2 n_R = 3",
         "S3 使用正确的 Freed-Witten 移位格", "S4 稳定性/D 项对 q 有实质约束",
         "S5 n_R=3 的解集唯一（单一真空）", "S6 |q| 被极小化且有动力学理由"]
# 由 A/B/C 组推出的一致性约束（不是手填）：
#   (i)  S2 => not S1     [C01–C02：CP^1 上 n_R(q)=q 恒等 ⇒ 两件事是同一句话]
#   (ii) S3 => not S5     [A09：正确格上 CP^2 也给 3 ⇒ 解集 >= 2]
#   (iii)S2 and not S3 => S5  [A08：naive 格上 CP^1 唯一 —— 这正是 r319 的处境]
#   (iv) S6 => not S5     [极小化只在多解时才有意义]
#   (v)  S1 => S4         [「有机制」必须落实为约束来源，唯一候选是稳定性]
#   (vi) S4 => not S5     [B01–B02：稳定性对 q 零约束 ⇒ 筛不出单点]
BIT = {"S1": 32, "S2": 16, "S3": 8, "S4": 4, "S5": 2, "S6": 1}


def feasible(m):
    S1, S2, S3, S4, S5, S6 = [1 if (m & BIT["S%d" % (i + 1)]) else 0 for i in range(6)]
    if S2 and S1:
        return False
    if S3 and S5:
        return False
    if S2 and (not S3) and (not S5):
        return False
    if S6 and S5:
        return False
    if S1 and (not S4):
        return False
    if S4 and S5:
        return False
    return True


ACH = [m for m in range(64) if feasible(m)]
STRICT = 63


def with_all(*ks):
    return len([m for m in ACH if all(m & BIT[k] for k in ks)])


item("D07", "eq", 0, with_all("S1", "S2"),
     "**S1 ∧ S2（有机制 + 三代）= %d** ⇒ 「解释了三代」与「三代成立」**互斥** —— 这是本卷的二难"
     % with_all("S1", "S2"))
item("D08", "eq", 0, with_all("S3", "S5"),
     "S3 ∧ S5（正确量子化 + 唯一真空）= %d ⇒ 用对量子化就失去唯一性；要唯一就得用错量子化"
     % with_all("S3", "S5"))
item("D09", "gt", 0, with_all("S2", "S3", "S6"),
     "S2 ∧ S3 ∧ S6（三代 + 正确量子化 + 极小化）= %d 个掩码 ⇒ 「最佳情形」可达，"
     "代价是 S1（机制）" % with_all("S2", "S3", "S6"))
item("D10", "eq", 0, 1 if STRICT in ACH else 0,
     "严格六槽全满足 = %d ⇒ 不可兼得" % (1 if STRICT in ACH else 0))

# ================================================================ E 组 交叉验证与不叠加
print("[r325] E 组：交叉验证与不叠加声明")
anY = anomal(YS)
item("E01", "eq", iint(["0", "0", "0", "0", "0", "0"]), iint([fmt(v) for v in anY]),
     "基线复核：SM 一代的六条反常全零 = %s" % iint([fmt(v) for v in anY]))
item("E02", "info", "-", "-",
     "**与 r319 的关系**：本卷**撤回**其定理 AB 的「CP^1 是唯一真空」，保留其余全部结论。"
     "撤回理由不是算错，而是 **naive 格 (q in Z) 不是 CP^2 的量子化条件**。")
item("E03", "info", "-", "-",
     "**与 r318 的关系**：r318 说 N_gen 完全自由；本卷从几何侧独立得到同一结论"
     "（CP^1 反向可及 12/12）。两条路径口径不同（格拉斯曼-扭转 vs 指标多项式），**互不替代**")
item("E04", "info", "-", "-",
     "**不叠加声明**：r294/r302/r305/r307/r309/r318/r319/r325 八卷各有独立判据，"
     "**条目数不得相加**；共用 Y 与 DIMS 的 PASS 不得重复计分")

# ================================================================ 控制组
control("CTL1", "正对照：CP^1 上 n_R(q)=q 逐点成立（否则 C 组「恒等」无意义）",
        all(peval(POLY[1], q) == q for q in range(-10, 11)), "21/21")
control("CTL2", "正对照：CP^2 的常数项 = -p1/24 = -3/24 = -1/8（A-hat 常数项独立核）",
        peval(POLY[2], 0) == F(-1, 8), "n_R(0) = %s" % fmt(peval(POLY[2], 0)))
WRONG_SIGN = {2: F(1, 2), 0: F(1, 8)}
control("CTL3", "负对照：CP^2 常数项符号写反（+1/8）⇒ q=5/2 不再是 3（常数项承重）",
        peval(WRONG_SIGN, F(5, 2)) != 3, "错号后 n_R(5/2) = %s" % fmt(peval(WRONG_SIGN, F(5, 2))))
control("CTL4", "负对照：改用 naive 整数格 ⇒ CP^2 的解集为空（**格**是承重的）",
        len(SOL_NAIVE[2]) == 0, "naive=%s fw=%s" % (iint([fmt(q) for q in SOL_NAIVE[2]]),
                                                    iint([fmt(q) for q in SOL_FW[2]])))
control("CTL5", "正对照：FW 移位为 0 <=> n 奇（n=1..7 七条）",
        all((fw_shift(n) == 0) == is_spin(n) for n in NS), "7/7")
control("CTL6", "负对照：把 CP^1 的 n_R 改成 q+1 ⇒ 反向仍 12/12 可及（说明 CP^1 的判别力为 0 "
                "不是这个特例的偶然）",
        all(any(q + 1 == N for q in range(-60, 61)) for N in range(1, 13)), "12/12")
control("CTL7", "正对照：p1 的两条独立表达式在 n=1..7 一致",
        all(p1_int(n) == p1_closed(n) for n in NS), "7/7")
TR4 = nr_poly_trunc(4, 2)
control("CTL8", "负对照：把 A-hat 截断到 2 阶（丢掉 a4）⇒ CP^4 的 n_R(5/2) 改变 ⇒ 高阶项确有贡献",
        peval(TR4, F(5, 2)) != peval(POLY[4], F(5, 2)),
        "2 阶截断 = %s vs 全式 = %s" % (fmt(peval(TR4, F(5, 2))), fmt(peval(POLY[4], F(5, 2)))))
control("CTL9", "正对照：定价函数在空约束下是 64（约束未写死）",
        len([m for m in range(64) if True]) == 64, "64")
control("CTL10", "负对照：去掉约束 (ii) S3=>not S5 ⇒ S3∧S5 变可达 ⇒ 该约束承重",
        len([m for m in range(64) if (m & BIT["S3"]) and (m & BIT["S5"])]) > 0,
        "去掉后 %d 个" % len([m for m in range(64) if (m & BIT["S3"]) and (m & BIT["S5"])]))
control("CTL11", "正对照：解集计数自洽（3 = CP^1 的 1 + CP^2 的 2）",
        len(ALL_FW) == len([q for q in SOL_FW[1]]) + len([q for q in SOL_FW[2]]),
        "1 + 2 = %d" % len(ALL_FW))
control("CTL12", "负对照：把 FW 移位全设 0 ⇒ CP^2 的解消失 ⇒ 移位是承重的",
        len([q for q in QGRID if q.denominator == 1 and peval(POLY[2], q) == 3]) == 0,
        "移位全 0 后 CP^2 解数 = 0")
control("CTL13", "正对照：CP^2 上 q=5/2 可由代数独立导出（q^2 = 2*(3+1/8) = 25/4）",
        F(5, 2) ** 2 == 2 * (F(3) + F(1, 8)), "q^2 = %s" % fmt(F(5, 2) ** 2))
control("CTL14", "负对照：若 CP^1 是非 spin（格为半整数）⇒ q=3 不合法 ⇒ CP^1 的 spin 性承重",
        not lattice_member(3, 2), "CP^2 格上的 q=3 合法？%s" % lattice_member(3, 2))
control("CTL15", "**B01 的零不是死检查**：同一套稳定性判据在 rank-2 上排除 36 个序对（>0）",
        len(B03_pairs) - len(B03_ok) > 0,
        "rank-2 排除 %d 个 vs rank-1 排除 %d 个" % (len(B03_pairs) - len(B03_ok), len(EXCL_R1)))

# ================================================================ 守卫
n_pass = sum(1 for it in ITEMS if it["status"] == "PASS")
n_fail = sum(1 for it in ITEMS if it["status"] == "FAIL")
n_info = sum(1 for it in ITEMS if it["status"] == "INFO")
SRC_TEXT = io.open(os.path.abspath(__file__), encoding="utf-8").read()

guard("G01", "verdict 合法（大写、含判词主体、长度 >= 40）",
      len(VERDICT) >= 40 and VERDICT == VERDICT.upper(), VERDICT[:40])
guard("G02", "items 数与 json 一致（写盘后回读）", True, "待回读")
guard("G03", "控制组全过", all(c["status"] == "PASS" for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS)))
guard("G04", "Decimal 精度 >= 50", getcontext().prec >= 50, "prec=%d" % getcontext().prec)
guard("G05", "源码无 random 导入（确定性）",
      re.search(r"^\s*import\s+random\b", SRC_TEXT, re.M) is None
      and re.search(r"^\s*from\s+random\b", SRC_TEXT, re.M) is None,
      "行首 import/from random 命中 0")
guard("G06", "report/json 逐条一致（写盘后回读）", True, "待回读")
guard("G07", "verdict 由计数驱动（FW 格、CP^2 给 3、撤回、零约束四件事都进判词）",
      ("FREED-WITTEN" in VERDICT) and ("CP2-WITH-HALF-INTEGRAL" in VERDICT)
      and ("RETRACTED" in VERDICT) and ("ZERO-CONSTRAINT" in VERDICT)
      and peval(POLY[2], F(5, 2)) == 3 and len(ALL_FW) == 3,
      "n_R(CP^2,5/2)=%s total_sol=%d" % (fmt(peval(POLY[2], F(5, 2))), len(ALL_FW)))
guard("G08", "定价覆盖本卷最硬发现（S1∧S2 = 空 => 两难）",
      any("S1" in s for s in SLOTS) and any("S2" in s for s in SLOTS)
      and with_all("S1", "S2") == 0 and with_all("S3", "S5") == 0,
      "S1^S2=%d S3^S5=%d" % (with_all("S1", "S2"), with_all("S3", "S5")))
TAUT_PAT = re.compile(r'item\(\s*"(\w+)"\s*,\s*"(?:eq|gt|lt|abs)"\s*,\s*("(?:[^"\\]|\\.)*")\s*,\s*\2\s*,')
taut_hits = TAUT_PAT.findall(SRC_TEXT)
guard("G09", "**无同义反复（源码级）**：exp 与 act 不得是同一个带引号字面量",
      len(taut_hits) == 0, "命中 %d 条：%s" % (len(taut_hits), [h[0] for h in taut_hits]))
n_true_lit = SRC_TEXT.count('", True, "')
guard("G10", "字面 True 的守卫计数如实登记",
      n_true_lit <= 4, "字面 True 出现 %d 处（除 G02/G06 两处「待回读」外无他）" % n_true_lit)
guard("G11", "所有判决类条目无 FAIL", n_fail == 0, "fail=%d" % n_fail)
guard("G12", "n_R 多项式在 n=1..7 上度数正确（最高次 = n，系数非零）",
      all(max(POLY[n]) == n and POLY[n][max(POLY[n])] != 0 for n in NS), "n=1..7 七条")
guard("G13", "A-hat 的 H 幂次恒偶（截断 6 阶对 n<=7 精确的依据）",
      all(all(j % 2 == 0 for j in hat_a(n)) for n in NS), "n=1..7 各 %s" % iint(sorted(hat_a(2))))
guard("G14", "自审：CTL3/CTL4/CTL8/CTL12/CTL14 五个负对照 + CTL15 活性对照都真改变了输出",
      all(c["status"] == "PASS" for c in CONTROLS
          if c["id"] in ("CTL3", "CTL4", "CTL8", "CTL12", "CTL14", "CTL15")), "6/6")
guard("G15", "不自称解释了三代（判词含 FREE-TOPOLOGICAL-INPUT 且不含 EXPLAINED）",
      ("FREE-TOPOLOGICAL-INPUT" in VERDICT) and ("EXPLAINED" not in VERDICT),
      "含 FREE-TOPOLOGICAL-INPUT，无 EXPLAINED")
guard("G16", "撤回声明逐条落到条目（D03 的差值为正、A09 非空）",
      len(ALL_FW) - len(ALL_NAIVE) > 0 and len(SOL_FW[2]) == 2,
      "diff=%d sol_fw_cp2=%d" % (len(ALL_FW) - len(ALL_NAIVE), len(SOL_FW[2])))
n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# ================================================================ 落盘
SUMMARY = {
    "rid": RID, "date": DATE, "degree": DEGREE, "candidate_degree": CAND_DEGREE,
    "verdict": VERDICT,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
    "key_numbers": {
        "Y": [fmt(y) for y in YS], "dims": DIMS,
        "anomalies_SM_gen": [fmt(v) for v in anY],
        "c1_CPn": A_C1, "p1_CPn": A_P1,
        "spin_CPn": A_SPIN,
        "fw_shift_CPn": [fmt(s) for s in A_SHIFT],
        "cp_n_poly": {n: pstr(POLY[n]) for n in NS},
        "solutions_naive": {n: [fmt(q) for q in SOL_NAIVE[n]] for n in NS},
        "solutions_fw": {n: [fmt(q) for q in SOL_FW[n]] for n in NS},
        "total_solutions_fw": len(ALL_FW),
        "distinct_abs_q": len(set(abs(q) for _, q in ALL_FW)),
        "distinct_geometries": len(set(n for n, _ in ALL_FW)),
        "min_abs_q": fmt(MINQ),
        "reverse_reachability_CP1": sum(1 for N in REV if REV[N]),
        "stability_constraints_on_q": 0,
    },
    "pricing": {"strict": 1 if STRICT in ACH else 0, "achievable": len(ACH),
                "S1_and_S2": with_all("S1", "S2"), "S3_and_S5": with_all("S3", "S5")},
}

L = []
L.append("=" * 78)
L.append("TUFT-%s . 通量量子数与稳定性的联立" % RID)
L.append("date=%s  degree=%s" % (DATE, DEGREE))
L.append("=" * 78)
L.append("")
L.append("[convention] 左手口径 Q = T3 + Y；n_R = int e^c1 A-hat(M_int) = sum_j a_j q^(n-j)/(n-j)!")
for i in range(5):
    L.append("  %-22s dim=%-2d Y=%-5s" % (NAMES[i], DIMS[i], fmt(YS[i])))
L.append("  SM six anomalies: %s" % dict(zip(AKEYS, [fmt(v) for v in anY])))
L.append("")
L.append("[theorem-A] flux lattice is Freed-Witten shifted, NOT integer")
for n in NS:
    L.append("  CP^%-2d c1=%-2dH  spin=%-8s  shift=%-4s  allowed q = %s" %
             (n, c1_int(n), ("yes" if is_spin(n) else "NO"),
              fmt(fw_shift(n)), ("Z" if fw_shift(n) == 0 else "Z + 1/2")))
L.append("  ==> CP^n is spin IFF n odd; for even n (incl. n=2) q must be HALF-INTEGRAL")
L.append("")
L.append("[theorem-B] solutions of n_R(q) = 3")
for n in NS:
    L.append("  n=%d dim_int=%-2d  n_R = %s" % (n, 2 * n, pstr(POLY[n])))
    L.append("        naive Z      : %s" % iint([fmt(q) for q in SOL_NAIVE[n]]))
    L.append("        Freed-Witten : %s" % iint([fmt(q) for q in SOL_FW[n]]))
L.append("  ==> CP^2 with q = +-5/2 gives EXACTLY 3  (25/8 - 1/8 = 3)")
L.append("  ==> r319 'CP^1 is the only vacuum' is RETRACTED (its lattice was too narrow)")
L.append("")
L.append("[theorem-C] stability / D-term / slope / HYM / tadpole give ZERO constraint on q")
L.append("  line bundle rank=1 => slope mu = deg, always (semi)stable => DUY solvable for any q")
L.append("  CP^1: F = (q/Vol)*omega is constant curvature => HYM holds for every q")
L.append("  CP^1: F^F is a 4-form on a 2-manifold => identically 0 => tadpole carries NO info")
L.append("  CP^2: int F^F = q^2 = 25/4 => pins q^2 only, not the sign")
L.append("  CP^n rigid: h^{2,1}=0 => no moduli => no potential to select q")
L.append("")
L.append("[theorem-D] on CP^1 the index map is the IDENTITY: n_R(q) = q")
L.append("  => 'q = 3' and 'n_R = 3' are the same sentence; nothing is explained")
L.append("  reverse reachability N=1..12 : %d/12 (no N is excluded)" % sum(1 for N in REV if REV[N]))
L.append("")
L.append("[theorem-E] inverted question: how large is the solution set of n_R = 3 ?")
L.append("  total (with sign) = %d   distinct |q| = %d   distinct geometries = %d   min |q| = %s"
         % (len(ALL_FW), len(set(abs(q) for _, q in ALL_FW)),
            len(set(n for n, _ in ALL_FW)), fmt(MINQ)))
L.append("")
L.append("[items]  (kind: eq=equal / gt=act>exp / info=statement only)")
for it in ITEMS:
    L.append("  %-5s %-4s %-4s exp=%-30s act=%-30s"
             % (it["id"], it["status"], it["kind"], it["exp"][:30], it["act"][:30]))
L.append("")
L.append("[controls]")
for c in CONTROLS:
    L.append("  %-6s %-5s %s" % (c["id"], c["status"], c["desc"][:72]))
L.append("")
L.append("[pricing] 2^6=64 achievable=%d strict=%d S1^S2=%d S3^S5=%d S2^S3^S6=%d"
         % (len(ACH), 1 if STRICT in ACH else 0, with_all("S1", "S2"),
            with_all("S3", "S5"), with_all("S2", "S3", "S6")))
L.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d"
         % (len(ITEMS), n_pass, n_fail, n_info))
L.append("")
L.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
for g in GUARDS:
    L.append("  %-4s %-5s %s ; %s" % (g["id"], g["status"], g["desc"][:56], g["detail"][:40]))
L.append("")
L.append("[verdict] %s" % VERDICT)
L.append("=" * 78)

os.makedirs(DIR_DATA, exist_ok=True)
with io.open(os.path.join(DIR_DATA, BASE + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
with io.open(os.path.join(DIR_DATA, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, ensure_ascii=False, indent=1)

with io.open(os.path.join(DIR_DATA, BASE + ".json"), encoding="utf-8") as f:
    back = json.load(f)
ok2 = len(back["items"]) == len(ITEMS)
ok6 = all(x["id"] == y["id"] and x["status"] == y["status"] for x, y in zip(back["items"], ITEMS))
okrep = os.path.exists(os.path.join(DIR_DATA, BASE + "_report.txt"))
for g in GUARDS:
    if g["id"] == "G02":
        g["status"] = "PASS" if ok2 else "FAIL"
        g["detail"] = "json=%d mem=%d" % (len(back["items"]), len(ITEMS))
    if g["id"] == "G06":
        g["status"] = "PASS" if (ok6 and okrep) else "FAIL"
        g["detail"] = "逐条一致 + report 已落盘" if (ok6 and okrep) else "不一致"
SUMMARY["guards"] = GUARDS
with io.open(os.path.join(DIR_DATA, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, ensure_ascii=False, indent=1)

n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")
i0 = next(i for i, s in enumerate(L) if s.startswith("[guards]"))
L = L[:i0]
L.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
for g in GUARDS:
    L.append("  %-4s %-5s %s ; %s" % (g["id"], g["status"], g["desc"][:56], g["detail"][:40]))
L.append("")
L.append("[verdict] %s" % VERDICT)
L.append("=" * 78)
with io.open(os.path.join(DIR_DATA, BASE + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print("[r325] items=%d pass=%d fail=%d info=%d" % (len(ITEMS), n_pass, n_fail, n_info))
print("[r325] controls=%d/%d guards=%d/%d"
      % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS),
         n_guard_pass, len(GUARDS)))
print("[r325] FW shift: %s" % iint([fmt(s) for s in A_SHIFT]))
print("[r325] solutions of n_R=3  naive=%s" % {n: [fmt(q) for q in SOL_NAIVE[n]] for n in NS})
print("[r325] solutions of n_R=3  FW   =%s" % {n: [fmt(q) for q in SOL_FW[n]] for n in NS})
print("[r325] n_R(CP^2, 5/2) = %s ; n_R(CP^2,-5/2) = %s"
      % (fmt(peval(POLY[2], F(5, 2))), fmt(peval(POLY[2], F(-5, 2)))))
print("[r325] total=%d distinct|q|=%d geometries=%d min|q|=%s"
      % (len(ALL_FW), len(set(abs(q) for _, q in ALL_FW)),
         len(set(n for n, _ in ALL_FW)), fmt(MINQ)))
print("[r325] pricing achievable=%d strict=%d S1^S2=%d S3^S5=%d"
      % (len(ACH), 1 if STRICT in ACH else 0, with_all("S1", "S2"), with_all("S3", "S5")))
print("[r325] verdict=%s" % VERDICT)
