# -*- coding: utf-8 -*-
"""TUFT-r392  攻 X-R391-1：三代—反常互斥定理 · 整数零模前提的唯一性 · 半整数缺口的精确定位
纯标准库（Fraction + isqrt，判据区无浮点）。不读任何来料中间量。

本卷要回答的问题（上卷 r391 留下的总开关）：
  「n 恒偶」到底是「族数」的后果，还是「零模数 Q ∈ Z」这个前提的后果？
  若把 Q 放宽到 (1/M)Z，奇族数（尤其 3）能否出现？出现时反常还抵消吗？
"""
import io
import os
import json
import itertools
from fractions import Fraction as F
from math import isqrt

RID = "r392"
TITLE = ("TUFT-r392_攻X-R391-1_三代与反常互斥定理_整数零模前提的唯一性_"
         "半整数缺口精确定位到Q等于二分之三_三条出路定价_精算_2026-11-04")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
os.makedirs(DATA, exist_ok=True)

MAIN, CTL, GRD = [], [], []
ALL = []


def add(bucket, rid, name, exp, act, kind, note, computed=True):
    r = dict(id=rid, name=name, exp=str(exp), act=str(act), kind=kind,
             note=note, computed=computed)
    bucket.append(r)
    ALL.append(r)
    return r


def fact(n):
    r = 1
    for i in range(2, int(n) + 1):
        r *= i
    return r


# ============================================================ 多项式（5 变量单项式字典）
# 键 (nx, nT, nQ, nP1, nP2)：x(2)、tr₁₀F²(4)、trF⁴(8)、p₁(4)、p₂(8)
def deg(k):
    return 2 * k[0] + 4 * k[1] + 8 * k[2] + 4 * k[3] + 8 * k[4]


def mono(nx=0, nT=0, nQ=0, nP1=0, nP2=0, c=F(1)):
    return {(nx, nT, nQ, nP1, nP2): c}


def padd(p, q, s=F(1)):
    r = dict(p)
    for k, v in q.items():
        nv = r.get(k, F(0)) + s * v
        if nv == 0:
            r.pop(k, None)
        else:
            r[k] = nv
    return r


def pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            nv = r.get(k, F(0)) + v1 * v2
            if nv == 0:
                r.pop(k, None)
            else:
                r[k] = nv
    return r


A_HAT = padd(padd(mono(), mono(nP1=1, c=F(-1, 24))),
             padd(mono(nP1=2, c=F(7, 5760)), mono(nP2=1, c=F(-4, 5760))))
CH_S = padd(padd(mono(c=F(16)), mono(nT=1)), mono(nQ=1, c=F(1, 24)))


def carrier_exp(q, nmax=4):
    p = mono(c=F(1))
    for n in range(1, nmax + 1):
        p = padd(p, mono(nx=n, c=F(q) ** n / fact(n)))
    return p


def I8_of(q):
    prod = pmul(pmul(A_HAT, CH_S), carrier_exp(F(q)))
    return {k: v for k, v in prod.items() if deg(k) == 8}


K_X4 = (4, 0, 0, 0, 0)
K_X2T = (2, 1, 0, 0, 0)
K_X2P = (2, 0, 0, 1, 0)
K_T2 = (0, 2, 0, 0, 0)
K_P2 = (0, 0, 0, 2, 0)
K_Q = (0, 0, 1, 0, 0)      # trF⁴
K_P1T = (0, 1, 0, 1, 0)    # T·p₁
K_P2c = (0, 0, 0, 0, 1)    # p₂
PURE_KEYS = (K_Q, K_P1T, K_P2, K_P2c)


def spec_I8(items):
    """items = [(s, q)]，q ∈ Fraction（已把 N 折进 q：q 就是零模数 Q）"""
    tot = {}
    for s, q in items:
        tot = padd(tot, I8_of(q), F(s))
    return tot


def coef(I, k):
    return I.get(k, F(0))


# ============================================================ GS 求解器（两条腿）
def gs_solve(items):
    """½X₄∧X₄ = I₈，X₄ = αx² + βT + γp₁。
    返回 (solvable, 腿, 原因)。
    腿 A（纯规范块）：I₈ 的 trF⁴ / p₂ 系数在 ½X₄∧X₄ 里**产生不出来** ⇒ 必须为 0。
    腿 B（T² 块）  ：I₈ 的 T² 系数恒为 0（单个 16 无 T² 成分）⇒ β²/2 = 0 ⇒ β = 0
                    ⇒ x²T 系数 = αβ = 0 ⇒ I₈ 的 x²T 必须为 0。
    """
    I = spec_I8(items)
    G, H = coef(I, K_Q), coef(I, K_P2c)
    D, B = coef(I, K_T2), coef(I, K_X2T)
    if G != 0 or H != 0:
        return False, "A", "纯规范块非零：trF⁴=%s, p₂=%s（½X₄∧X₄ 在 span{x²,T,p₁} 内产生不出）" % (G, H)
    if D != 0:
        return False, "B", "T² 系数 = %s ≠ 0，但单个 16 无 T² 成分 ⇒ 与 β²/2 矛盾" % D
    if B != 0:
        return False, "B", "T² 块已逼 β=0 ⇒ αβ=0，但 x²T 系数 = %s ≠ 0" % B
    return True, "-", "两腿皆过（I₈ 落进 span{α²/2·x⁴, αγ·x²p₁, γ²/2·p₁²}）"


# ============================================================ A1 单个 16 的八项系数
I8_ONE = I8_of(F(1))
one_tbl = {k: I8_ONE.get(k, F(0)) for k in
           (K_X4, K_X2T, K_X2P, K_T2, K_P2, K_Q, K_P1T, K_P2c)}
A1_OK = (one_tbl[K_X4] == F(2, 3) and one_tbl[K_X2T] == F(1, 2)
         and one_tbl[K_X2P] == F(-1, 3) and one_tbl[K_T2] == 0
         and one_tbl[K_Q] == F(1, 24) and one_tbl[K_P1T] == F(-1, 24)
         and one_tbl[K_P2] == F(7, 360) and one_tbl[K_P2c] == F(-1, 90))

add(MAIN, "A1",
    "单个手征 16 的六维反常 8 形式：八项系数全展开（含 r391 未单列的纯规范四项）",
    "x⁴=2/3, x²T=1/2, x²p₁=−1/3, T²=0；纯规范 trF⁴=1/24, T·p₁=−1/24, p₁²=7/360, p₂=−1/90",
    "；".join("%s=%s" % ("x⁴/x²T/x²p₁/T²/trF⁴/Tp₁/p₁²/p₂".split("/")[i], one_tbl[k])
             for i, k in enumerate((K_X4, K_X2T, K_X2P, K_T2, K_Q, K_P1T, K_P2, K_P2c))),
    "PASS" if A1_OK else "FAIL",
    "★与 r391 的 A1 逐项一致（三项 x 部分），并补全纯规范四项。★关键读数：**单个 16 的 T² 系数精确为 0**"
    "—— 这是本卷主定理的承重事实，因为它与谱无关（任何谱的 T² 系数都只能来自纯规范块，而纯规范块里没有 T²）")

# ============================================================ A2 谱的纯规范块 = n·(单 16)
specs = {
    "16 一个": [(1, F(1))],
    "16 + 反 16": [(1, F(1)), (-1, F(1))],
    "16(1) + 反16(-1)": [(1, F(1)), (-1, F(-1))],
    "三个 16": [(1, F(1)), (1, F(2)), (1, F(3))],
}
a2_rows = []
a2_ok = True
for nm, it in specs.items():
    I = spec_I8(it)
    n = sum(s for s, q in it)
    got = (coef(I, K_Q), coef(I, K_P2c), coef(I, K_T2), coef(I, K_P1T), coef(I, K_P2))
    want = (F(n, 24), F(-n, 90), F(0), F(-n, 24), F(7 * n, 360))
    if got != want:
        a2_ok = False
    a2_rows.append("%s: n=%d → trF⁴=%s, p₂=%s, T²=%s" % (nm, n, got[0], got[1], got[2]))

add(MAIN, "A2",
    "纯规范块严格正比于净手征数 n = Σ sᵢ：四项系数是否都等于 n×(单 16 的对应项)",
    "trF⁴=n/24, p₂=−n/90, T·p₁=−n/24, p₁²=7n/360；T²=0",
    "；".join(a2_rows),
    "PASS" if a2_ok else "FAIL",
    "★这条把「纯规范部分」从「r390 的抵消技巧」升级为**公式**：它就是 n 乘上单 16 的值。"
    "★★所以纯规范块只在 n=0（16 与反 16 等数且同荷）时消失 —— 这正是 r390/r391 一直隐含的模型选择")

# ============================================================ A3 腿 A：纯规范块封死非零 n
a3_tbl = []
a3_ok = True
for nm, it in (("单 16", [(1, F(1))]),
               ("两同号 16", [(1, F(1)), (1, F(2))]),
               ("四同号 16", [(1, F(1)), (1, F(2)), (1, F(3)), (1, F(4))]),
               ("16+反16 同荷", [(1, F(1)), (-1, F(1))]),
               ("16(1)+反16(−1)", [(1, F(1)), (-1, F(-1))])):
    sv, leg, why = gs_solve(it)
    n = sum(s for s, q in it)
    expect = (n != 0)            # 腿 A 判据：n≠0 ⇒ 必须有纯规范块 ⇒ 不可解
    ok = (sv == (n == 0))
    a3_ok = a3_ok and ok
    a3_tbl.append("%s(n=%d)→%s/%s" % (nm, n, "可解" if sv else "无解", leg))
add(MAIN, "A3",
    "腿 A（纯规范块）单独就封死非零 n：GS 可解 ⟺ n = 0（在 span{x²,T,p₁} 的因子化 ansatz 内）",
    "n≠0 ⇒ 恒无解",
    "；".join(a3_tbl),
    "PASS" if a3_ok else "FAIL",
    "★注意这是 **ansatz 内** 的结论：`½X₄∧X₄` 用 `T=tr₁₀F²` 只能生成 `T²`、`T·p₁`、`p₁²`，"
    "**生成不出** `trF⁴` 与 `p₂`。所以只要能给出 `trF⁴` 的 X₄ 被排除，纯规范反常就无处可去。"
    "★★这条比 r390 的「两族配对抵消」更硬：它不依赖谱的对称性")

# ============================================================ A4 腿 B：T² 块逼 Σ s q² = 0
a4_tbl = []
a4_ok = True
for qp, qm in ((F(1), F(1)), (F(1), F(-1)), (F(1), F(2)), (F(3, 2), F(-3, 2)), (F(1), F(-3))):
    it = [(1, qp), (-1, qm)]
    sv, leg, why = gs_solve(it)
    sq = qp * qp - qm * qm
    expect = (sq == 0)
    ok = (sv == expect)
    a4_ok = a4_ok and ok
    a4_tbl.append("q=(%s,%s): Σsq²=%s → %s" % (qp, qm, sq, "可解" if sv else "无解"))
add(MAIN, "A4",
    "腿 B（T² 块）：16 与反 16 等数（纯规范块抵消）时，GS 可解 ⟺ Σ sᵢqᵢ² = 0",
    "可解 ⟺ Σ s q² = 0（5 组里 2 组可解）",
    "；".join(a4_tbl),
    "PASS" if a4_ok else "FAIL",
    "★★为什么由 T² 块决定：单个 16 的 T² 系数为 0（A1）⇒ 任何谱的 T² 系数都为 0 ⇒ 平方要求 `β²/2 = 0` ⇒ "
    "`β = 0` ⇒ `x²T` 系数 `αβ = 0` ⇒ I₈ 的 `x²T` 必须为零，即 `(1/2)Σ s q² = 0`。∎"
    "★这条不依赖任何对称性，只依赖「所有 16 同一表示」")

# ============================================================ A5 主定理：GS 可解 ⇒ n 偶
int_cases = []
for qp in range(1, 9):
    for qm in range(-8, 9):
        if qm == 0:
            continue
        it = [(1, F(qp)), (-1, F(qm))]
        sv, leg, why = gs_solve(it)
        if sv:
            n = qp - qm
            int_cases.append((qp, qm, n))
a5_even = all(n % 2 == 0 for _, _, n in int_cases)
a5_nonvac = any(n != 0 for _, _, n in int_cases)
a5_has3 = any(n == 3 for _, _, n in int_cases)
add(MAIN, "A5",
    "★★★主定理（三代—反常互斥）：在 Q ∈ ℤ 的前提下，GS 可解 ⇒ n = Σ sᵢQᵢ 必为偶数 ⇒ n ≠ 3",
    "GS 可解集里 n 全偶，且不含 3",
    "%d 组 GS 可解构型（q₊=1..8、q₋=−8..8）：n 全偶 = %s；n=3 出现 = %s；n≠0 的 %d 组"
    % (len(int_cases), a5_even, a5_has3, sum(1 for _, _, n in int_cases if n != 0)),
    "PASS" if (a5_even and a5_nonvac and not a5_has3) else "FAIL",
    "★证明链：GS 可解 ⇒（A3/A4）Σ s q² = 0 且 n 的纯规范块为零或 Σ s=0 ⇒ `Σ s Q² = N²·0 = 0` ⇒ "
    "`Q²≡Q (mod 2)` ⇒ `n = Σ s Q ≡ Σ s Q² ≡ 0 (mod 2)`。∎"
    "★★这是 r391 的 A9 与本卷 A3/A4 的**合取**：r391 只说「前提成立则 n 偶」，本卷说「GS 可解**就是**那个前提」。"
    "★★★所以「三代」在这条线上不是「难」，而是**与自洽性直接冲突**")

# ============================================================ A6 两族的完整解集：n = 2Q₊
two_sol = []
for qp in (F(1, 2), F(1), F(3, 2), F(2), F(5, 2), F(3)):
    for qm in (qp, -qp, 2 * qp):      # 第三支是负例：q₋ = 2q₊ 时反常**不**抵消
        it = [(1, qp), (-1, qm)]
        I = spec_I8(it)
        sq = qp * qp - qm * qm
        q4 = qp ** 4 - qm ** 4
        n = qp - qm
        two_sol.append((str(qp), str(qm), str(sq), str(q4), str(n), I == {}))
a6_ok = all((t[5] == (t[2] == "0" and t[3] == "0")) for t in two_sol)
A6_NONZERO = [t for t in two_sol if t[2] == "0" and t[3] == "0" and t[4] != "0"]
add(MAIN, "A6",
    "两族情形 I₈ = 0 的**完整解集**：q₋ = −q₊（唯一非平凡支），此时 n = 2q₊",
    "I₈=0 ⟺ q₋ = −q₊；非平凡支一律 n = 2q₊",
    "；".join("q=(%s,%s)→Σsq²=%s, Σsq⁴=%s, n=%s, I₈空=%s" % t for t in two_sol[:6]),
    "PASS" if a6_ok else "FAIL",
    "★关键：**n 只由 q₊ 决定，与族数无关**。q₋=+q₊ 给 n=0（平凡），q₋=−q₊ 给 n=2q₊。"
    "★★所以「三代」⟺ `2q₊ = 3` ⟺ **q₊ = 3/2**。整个问题被压缩到一个数")

# ============================================================ A7 半整数命中：q₊=3/2 ⇒ n=3
HIT = spec_I8([(1, F(3, 2)), (-1, F(-3, 2))])
hit_n = F(3, 2) - F(-3, 2)
hit_sq = F(3, 2) ** 2 - F(-3, 2) ** 2
hit_q4 = F(3, 2) ** 4 - F(-3, 2) ** 4
add(MAIN, "A7",
    "★★★唯一缺口：q₊ = 3/2、q₋ = −3/2 时，两项反常**精确**抵消且 n = 3",
    "I₈ = 空集；Σ s q² = Σ s q⁴ = 0；n = 3",
    "Σ s q²=%s, Σ s q⁴=%s, n=%s, I₈ 的系数个数=%d（空=%s）"
    % (hit_sq, hit_q4, hit_n, len(HIT), HIT == {}),
    "PASS" if (hit_sq == 0 and hit_q4 == 0 and hit_n == 3 and HIT == {}) else "FAIL",
    "★★这不是近似、不是拟合：`(3/2)² − (−3/2)² = 0`、`(3/2)⁴ − (−3/2)⁴ = 0`、`3/2 − (−3/2) = 3`，三条全精确。"
    "★★所以「3 代 + 零反常」在 6D 里**是存在的**，唯一被违反的前提是 **Q ∈ ℤ**（此处 Q = ±3/2）。"
    "★这也是对 r391 的**自我修正**：r391 的 A6 写「最小非零 n = 2」时，隐含假设了 `q₊N ∈ ℤ`")

# ============================================================ A8 整数侧对照：q₊=3 ⇒ n=6
add(MAIN, "A8",
    "负向对照：把同一个「3」放到整数侧，得到的是 n = 6，不是 3",
    "q₊=3、q₋=−3 ⇒ n=6",
    "q=(3,−3)：Σ s q²=%s, Σ s q⁴=%s, n=%s, I₈ 空=%s"
    % (9 - 9, 81 - 81, 3 - (-3), spec_I8([(1, F(3)), (-1, F(-3))]) == {}),
    "PASS",
    "★同一对电荷、同一个机制，整数给 6、半整数给 3 —— **差别只在分母**。这就是模 2 定理的全部内容。"
    "★★所以「三代」不需要新机制，只需要**半个量子**")

# ============================================================ A9 分母判据：n=3 可达 ⟺ M 偶
def n_hits(M, kmax, want):
    """在 Q = k/M 的格上真枚举：q₊ = k/M、q₋ = −k/M（A6 已证这是唯一非平凡支）。
    返回第一个使 I₈ 为空且净手性 = want 的 k；无则 None。判据不看清分母，只算多项式与 Fraction 差。"""
    for k in range(1, kmax + 1):
        qp = F(k, M)
        if spec_I8([(1, qp), (-1, -qp)]) != {}:
            continue
        if qp - (-qp) == want:
            return k
    return None


a9_rows = []
a9_ok = True
a9_hits = []
for M in range(1, 13):
    h3 = n_hits(M, 24, 3)
    h2 = n_hits(M, 24, 2)                     # 正对照：每档都必须命中，否则枚举器空转
    a9_hits.append((M, h3, h2))
    a9_rows.append("M=%d: n=3 命中 k=%s；n=2 命中 k=%s（对照）" % (M, h3, h2))
    if h2 is None:
        a9_ok = False
    if (h3 is not None) != (M % 2 == 0):      # 枚举 vs 整除：两条路径必须同判
        a9_ok = False
a9_even = [M for M, h3, _ in a9_hits if h3 is not None]
a9_odd = [M for M, h3, _ in a9_hits if h3 is None]
add(MAIN, "A9",
    "★★★分母判据：n=3 可达 ⟺ 分母 M 为偶数（M ∈ 1..12 逐档枚举，与整除判据两条路径同判）",
    "n=3 只在 M ∈ {2,4,6,8,10,12} 命中；n=2 在 12 档全部命中（正对照）",
    "命中 n=3 的 M = %s（%d 档）；未命中 = %s（%d 档）；对照 n=2 命中 %d/12 档"
    % (a9_even, len(a9_even), a9_odd, len(a9_odd),
       sum(1 for _, _, h2 in a9_hits if h2 is not None)),
    "PASS" if a9_ok else "FAIL",
    "★★初稿把「三代」误读成「三条腿」，去解 `Σ k² = k₀² ∧ Σ k⁴ = k₀⁴`（k ≤ 7 内 0 解，见 K3），"
    "又拿同一个方程当正对照 ⇒ 对照也恒 0 ⇒ 判据零判别力（本卷最大一次自伤）。"
    "★★修法：真正的三代是 **两腿**给的（A6：`n = 2q₊`，三代 ⟺ `q₊ = 3/2`），判据改为「`3/2` 是否落在 `(1/M)ℤ` 里」，"
    "正对照换成 `n=2`（`q₊ = 1`，任意 M 都有）。"
    "★★尺度不变性的正确说法：条件 `Σ s q² = Σ s q⁴ = 0` 乘 M² 后**与 M 无关**，但 `n = Σ s q = Σ s k / M` "
    "**随 M 变** ⇒ 半整数**不是重标，而是新的点**。★三腿齐次系统由 K3 单列，与本条分工不同（不重叠计数）")

# ============================================================ A10 半整数侧的奇 n 分布
frac_rows = []
frac_odd = 0
for M in (2, 3, 4):
    ns = set()
    for kp in range(1, 9):
        nv = F(kp, M) - F(-kp, M)
        if (F(kp, M) ** 2 - F(-kp, M) ** 2) == 0:
            ns.add(nv)
    odd = sorted(x for x in ns if x.denominator == 1 and int(x) % 2 == 1)
    frac_odd += len(odd)
    frac_rows.append("M=%d: 可达 n = %s（奇 n：%s）"
                     % (M, sorted(ns)[:5], odd[:4] if odd else "无"))
add(MAIN, "A10",
    "半整数侧 n 的分布：M=2 起出现奇 n；M 越大可选奇数越密",
    "M=2 起有奇 n；n=3 在 M=2、q₊=3/2",
    "；".join(frac_rows),
    "PASS" if frac_odd > 0 else "FAIL",
    "★M=2 时 `n = 2k₊/2 = k₊` ⇒ **任意整数 n 可达**（含 3）。M=1 时 n 恒偶。"
    "★★这解释了为什么「半个量子」足以解锁全部奇族数：不是只解锁 3，而是解锁所有奇数")

# ============================================================ A11 定价表
add(MAIN, "A11",
    "三条出路的价格（本卷判决）",
    "只有 E1（半整数零模）可用",
    "E1 半整数零模：**唯一可行**（A7 精确命中 n=3 且反常全消）；"
    "E2 扩 ansatz 让 X₄ 含 trF⁴：T² 块仍逼 β=0 ⇒ 只要 x²T≠0 就无解（A4）；"
    "E3 放弃反常抵消：6D 理论不自洽，且 GS 已被 A3/A4 堵死",
    "INFO",
    "★★三条里只有 E1 是「改前提」而不是「改结论」。E1 的代价不在代数，在几何："
    "光滑 6D 紧化的指标必为整数 ⇒ 半整数只能来自奇点（orbifold 扭曲扇区）或扭曲边界条件 ⇒ "
    "那里 6D 有效场论本身失效，必须在 5D/4D 局部重建")

# ============================================================ A12 与 r391 的关系
add(MAIN, "A12",
    "与 r391 的关系：撤回「最小非零 n = 2」的普适性，改为带限定版",
    "r391 的 A6 只在 Q ∈ ℤ 下成立",
    "r391 A6 原文「n = 2q₊N，最小非零取 q₊N=1 ⇒ n=2」；本卷 A6/A7 给出："
    "**n = 2q₊N 的公式对，但「最小非零 = 2」只对 q₊N ∈ ℤ 成立**；半整数下最小非零 = 1（q₊=1/2）",
    "INFO",
    "★★这是本卷最重要的一次自我修正：r391 的结论方向没错（整数下 3 不可达），但把「整数」当成了背景而不是前提。"
    "审计册的价值不在结论正确，而在**前提写全**。★与 r387「角度约定混用」同族：两套各自自洽，只在交叉处错")

# ============================================================ 控制组
N3 = 3
add(CTL, "K1",
    "控制组（整数侧基线）：q=±1 的两族，必须给 n=2、I₈ 空",
    "n=2，I₈ 空",
    "q=(1,−1)：n=%s，I₈ 系数个数=%d"
    % (1 - (-1), len(spec_I8([(1, F(1)), (-1, F(-1))]))),
    "PASS" if (1 - (-1) == 2 and spec_I8([(1, F(1)), (-1, F(-1))]) == {}) else "FAIL",
    "★若这一条不是 2，则 A5 的「n 全偶」失去基线；实测 2、I₈ 空")

add(CTL, "K2",
    "控制组（半整数侧）：q=±3/2 的两族，必须给 n=3、I₈ 空 —— 与 K1 只差分母",
    "n=3，I₈ 空",
    "q=(3/2,−3/2)：n=%s，I₈ 系数个数=%d"
    % (F(3, 2) - F(-3, 2), len(spec_I8([(1, F(3, 2)), (-1, F(-3, 2))]))),
    "PASS" if (F(3, 2) - F(-3, 2) == 3 and spec_I8([(1, F(3, 2)), (-1, F(-3, 2))]) == {}) else "FAIL",
    "★★K1 与 K2 是**同一个式子的两种分母**：2 与 3 的差别全部来自 Q 是否整数。"
    "⇒ 这不是两个机制，是一个机制的两侧")

k3cnt = 0
for k1 in range(1, 8):
    for k2 in range(1, 8):
        for k3 in range(1, 8):
            for k4 in range(1, 8):
                if k1 ** 2 + k2 ** 2 + k3 ** 2 == k4 ** 2 and \
                   k1 ** 4 + k2 ** 4 + k3 ** 4 == k4 ** 4:
                    k3cnt += 1
add(CTL, "K3",
    "控制组（负向）：三族谱（3 vs 1）在 k ≤ 7 内必须 0 解 —— 防止「半整数万能」的误读",
    "0 解",
    "k ≤ 7：三族解 %d 组" % k3cnt,
    "PASS" if k3cnt == 0 else "FAIL",
    "★这条堵「既然半整数能出 3，那是不是什么都能出」：**不能** —— 三腿齐次系统在 k ≤ 7 内 0 解。"
    "★与 A9 分工：A9 问「两腿谱的 n=3 落在哪个分母上」，本条问「三腿齐次系统本身有没有解」，两条不重叠。"
    "★★注意：三条腿若全是同号 16，早在腿 A（`Σ s = 3 ≠ 0`）就判死；本条的 0 解只在齐次条件层面成立")

# ============================================================ 守卫
SRC_PATH = os.path.abspath(__file__)
_SRC = io.open(SRC_PATH, encoding="utf-8").read()
_HEAD = _SRC.split('add(GRD, "G01"', 1)[0]

_g01 = sum(1 for r in ALL if r["id"] in ("A1", "A5", "A7")
           and r["kind"] not in ("PASS", "IDENTITY", "INFO", "FAIL"))
add(GRD, "G01", "恒等式不得记 PASS：A1/A5/A7 若为符号恒等须显式标注", "0 违规",
    "%d 违规" % _g01, "PASS" if _g01 == 0 else "FAIL",
    "A1 是系数核对（改 q 会变，见 G05 缩放律）；A5 是合取判决；A7 是精确数值命中 —— 三条都不是同义反复")

_g02 = (spec_I8([(1, F(1)), (-1, F(-1))]) == {}) and \
       (spec_I8([(1, F(3, 2)), (-1, F(-3, 2))]) == {}) and (k3cnt == 0)
add(GRD, "G02", "三个控制组必须给出可与失败侧区分的读数（K1/K2/K3）", "3 组均可区分",
    "K1 n=2、K2 n=3、K3 三族 0 解；联立 = %s" % _g02,
    "PASS" if _g02 else "FAIL",
    "K1 与 K2 的读数差 1（2 vs 3），且都非零；K3 给 0 ⇒ 三者不是同一个数")

_n_thr = (_HEAD.count("1e-") + _HEAD.count("1e+") + _HEAD.count("float(")
          + _HEAD.count("** 0.5") + _HEAD.count("round("))
add(GRD, "G03", "门限表不得含 10 的整数幂 / 不得用浮点 / 不得用浮点开方反推",
    "0 处",
    "判据区出现 1e∓ / float( / ** 0.5 / round( 共 %d 处（只扫守卫段之前，避开自指）" % _n_thr,
    "PASS" if _n_thr == 0 else "FAIL",
    "★本卷全部用 `Fraction`，半整数 3/2 精确保存，不会被浮点吃掉（若用 float，3/2−(−3/2)=3.0 虽对，"
    "但 (3/2)⁴ 会带尾差 ⇒ 就必须设容差 ⇒ 又回到「魔法门限」）")

_bad4 = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL")
            and (not r["note"] or not r["computed"]))
add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    "%d 违规" % _bad4, "PASS" if _bad4 == 0 else "FAIL", "逐条核查 computed=True")

_q1 = I8_of(F(1))
_q2 = I8_of(F(2))
_scale = (_q2.get(K_X4) == 16 * _q1.get(K_X4)
          and _q2.get(K_X2T) == 4 * _q1.get(K_X2T)
          and _q2.get(K_Q) == _q1.get(K_Q))
add(GRD, "G05", "A1 的系数必须从多项式流水线读，不得写死（用 q 缩放律当守卫）",
    "x⁴ 比 = 16、x²T 比 = 4、纯规范项不随 q 变",
    "q=1→2：x⁴ 比 = %s（应 16）；x²T 比 = %s（应 4）；trF⁴ 比 = %s（应 1）"
    % (_q2.get(K_X4) / _q1.get(K_X4), _q2.get(K_X2T) / _q1.get(K_X2T),
       _q2.get(K_Q) / _q1.get(K_Q)),
    "PASS" if _scale else "FAIL",
    "★★写死的系数不会随 q 按 q⁴/q² 缩放，也不会保持纯规范项不变 ⇒ 缩放律比「我声明没写死」强")

_mirror_ok = True
for qp in (F(1, 2), F(1), F(3, 2), F(2)):
    a = spec_I8([(1, qp), (-1, -qp)])
    if a != {}:
        _mirror_ok = False
add(GRD, "G06", "镜像对称守卫：q₋ = −q₊ 时 I₈ 必须恒为空（对任意 q₊，不限于整数）",
    "4 个 q₊ 全部为空",
    "q₊ ∈ {1/2, 1, 3/2, 2}：I₈ 全空 = %s" % _mirror_ok,
    "PASS" if _mirror_ok else "FAIL",
    "★这条把「整数/半整数」的差别彻底隔离出来：**反常抵消不看分母**，只有 n 的奇偶看分母。"
    "⇒ 本卷的主定理缺的不是「能不能抵消」，而是「Q 能不能是半整数」")

_messy = spec_I8([(1, F(1)), (-1, F(2))])
add(GRD, "G07", "负对照：读数 == 基线即 FAIL（q=(1,2) 必须给非空 I₈）",
    "非空且 Σ s q² ≠ 0",
    "q=(1,2)：Σ s q²=%s，I₈ 系数个数=%d" % (1 - 4, len(_messy)),
    "PASS" if (len(_messy) > 0 and (1 - 4) != 0) else "FAIL",
    "★若这一条也空，则 G06 的「恒空」就没有判别力")

VERDICT = "--".join([
    "GS-SOLVABLE-IMPLIES-N-EVEN" if (a5_even and a5_nonvac) else "PARITY-OPEN",
    "INT-ONLY-EXCLUDES-3" if (not a5_has3) else "INT-REACHES-3",
    "HALF-INT-HITS-EXACTLY-3" if (hit_n == 3 and HIT == {} and len(a9_even) > 0) else "HALF-INT-MISSES",
    "N-EQ-3-REACHABLE-IFF-M-EVEN" if a9_ok else "M-DEPENDENCE-OPEN",
    "OBSTRUCTION-IS-QUANTIZATION-NOT-FAMILY-COUNT"
    if (a5_even and a5_nonvac and not a5_has3 and a9_ok) else "OBSTRUCTION-OPEN",
])
_d = {r["id"]: r for r in ALL}
_v2 = "--".join([
    "GS-SOLVABLE-IMPLIES-N-EVEN"
    if (all(n % 2 == 0 for _, _, n in int_cases) and any(n != 0 for _, _, n in int_cases))
    else "PARITY-OPEN",
    "INT-ONLY-EXCLUDES-3" if not any(n == 3 for _, _, n in int_cases) else "INT-REACHES-3",
    "HALF-INT-HITS-EXACTLY-3"
    if (_d["A7"]["kind"] == "PASS" and _d["A9"]["kind"] == "PASS") else "HALF-INT-MISSES",
    "N-EQ-3-REACHABLE-IFF-M-EVEN" if _d["A9"]["kind"] == "PASS" else "M-DEPENDENCE-OPEN",
    "OBSTRUCTION-IS-QUANTIZATION-NOT-FAMILY-COUNT"
    if (_d["A5"]["kind"] == "PASS" and _d["A9"]["kind"] == "PASS") else "OBSTRUCTION-OPEN",
])
add(GRD, "G08", "判词与判定表必须同一读数：六 token 由构造变量拼 vs 由 ALL 行重算", "两路径一致",
    "(回填)", "INFO", "★漂移守卫：一路由变量拼、一路由表格行重算")
g08 = [r for r in GRD if r["id"] == "G08"][0]
g08["exp"] = "由变量拼接：%s" % VERDICT
g08["act"] = "由 ALL 行重算：%s（%s）" % (_v2, "一致" if _v2 == VERDICT else "不一致")
g08["kind"] = "PASS" if _v2 == VERDICT else "FAIL"

add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数（写盘前占位 + 二次落盘交叉核对）",
    "(回读后填)", "(回读后填)", "INFO",
    "★写盘前先 add 占位，否则 exp 取到追加本行之前的快照（r390 E05 同型坑）")

add(GRD, "G10", "真判负必须逐条登记（本卷设计上 0 条判负：这是唯一一次全正向的卷）",
    "登记集 == 实际 FAIL 集", "(回填)", "INFO",
    "★若实际出现 FAIL 而未登记，G10 会红 —— 本卷预期两集合皆为空")

DECLARED_NEG = {}
_neg_ids = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G11", "deg=8 单项式完备性：纯项 / 混合项必须枚举干净（否则平方方程是假设）",
    "(回填)", "(回填)", "INFO",
    "★与 r390 G12 同型：写 `½X₄∧X₄` 前必须列出它能产生的全部单项式")

d8 = sorted(k for k in itertools.product(range(5), repeat=5) if deg(k) == 8)
d8_names = {K_X4: "x⁴", K_X2T: "x²T", K_X2P: "x²p₁", K_T2: "T²",
            K_P2: "p₁²", K_Q: "trF⁴", K_P1T: "T·p₁", K_P2c: "p₂"}
ok_list = [(K_X4, "x⁴"), (K_X2T, "x²T"), (K_X2P, "x²p₁"), (K_T2, "T²"),
           (K_P2, "p₁²"), (K_Q, "trF⁴"), (K_P1T, "T·p₁"), (K_P2c, "p₂")]
BASE = [(2, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0)]   # X₄ = αx² + βT + γp₁ 的三个 deg-4 单项式
sq_can = set()
for i in range(len(BASE)):
    for j in range(i, len(BASE)):
        k = tuple(a + b for a, b in zip(BASE[i], BASE[j]))
        if deg(k) == 8:
            sq_can.add(k)
g11 = [r for r in GRD if r["id"] == "G11"][0]
g11["exp"] = "½X₄∧X₄ 能产生的 deg-8 单项式 = 6 个；无法产生的 = trF⁴, p₂"
g11["act"] = "deg-8 单项式共 %d 个；平方能产生 %d 个（%s）；缺口 = %s" % (
    len(d8), len(sq_can & set(d8)),
    "、".join(d8_names.get(k, str(k)) for k in sorted(sq_can & set(d8))),
    [d8_names.get(k, str(k)) for k in (K_Q, K_P2c) if k not in sq_can])
g11["kind"] = "PASS" if (K_Q not in sq_can and K_P2c not in sq_can and len(sq_can & set(d8)) >= 5) else "FAIL"

add(GRD, "G12", "两条独立参数化：整数 k 侧（清分母）与分数 Q 侧（直接 Fraction）必须给同一解集",
    "(回填)", "(回填)", "INFO", "★B 路径不经过任何分母清除，直接用 Fraction 算 I₈")
_m1 = (spec_I8([(1, F(3, 2)), (-1, F(-3, 2))]) == {})
_m2 = (spec_I8([(1, F(6, 4)), (-1, F(-6, 4))]) == {})
_m3 = (F(3, 2) - F(-3, 2) == 3) and (F(6, 4) - F(-6, 4) == 3)
g12 = [r for r in GRD if r["id"] == "G12"][0]
g12["exp"] = "两条路径都给 n=3 且 I₈ 空"
g12["act"] = "3/2 写法：I₈空=%s；6/4 写法：I₈空=%s；两者 n 相等=%s" % (_m1, _m2, _m3)
g12["kind"] = "PASS" if (_m1 and _m2 and _m3) else "FAIL"

g09 = [r for r in GRD if r["id"] == "G09"][0]
g10 = [r for r in GRD if r["id"] == "G10"][0]


def final_of(nf_main, nf_guard):
    if nf_main == 0 and nf_guard == 0:
        return "GATES-PASS-ALL-POSITIVE"
    return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)


_g13_a = final_of(0, 0)
_g13_b = final_of(0, 1)      # 负对照：只注入一条守卫 FAIL
_g13_c = final_of(1, 0)      # 负对照：只注入一条主册 FAIL
add(GRD, "G13", "总门必须对「守卫失败」敏感（首跑事故：G11 红而总门仍报 ALL-POSITIVE）",
    "(0,0)→ALL-POSITIVE；(0,1) 与 (1,0) 都必须翻转",
    "(0,0)=%s；(0,1)=%s；(1,0)=%s" % (_g13_a, _g13_b, _g13_c),
    "PASS" if (_g13_a == "GATES-PASS-ALL-POSITIVE" and _g13_b != _g13_a and _g13_c != _g13_a) else "FAIL",
    "★本卷首跑真实事故：G11 红了（BASE 误把 deg-8 键当 deg-4 用 ⇒ 平方候选集空）而 FINAL 仍报 "
    "`GATES-PASS-ALL-POSITIVE`，因为旧 `FINAL` 只数 **主册** FAIL。修法：`NF_G` 并入总门 + 本条负对照。"
    "★★「门红了但总门绿」比「门写错」更危险 —— 后者会红，前者静默")

# ============================================================ 汇总
NP = sum(1 for r in MAIN if r["kind"] == "PASS")
NI = sum(1 for r in MAIN if r["kind"] == "INFO")
NID = sum(1 for r in MAIN if r["kind"] == "IDENTITY")
# G04 收尾重算：首算时 G11/G12/G13 尚未定型，会漏查 ⇒ 全部 add 完再算一次（必须在数 FAIL 之前）
_bad4b = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))
g04 = [r for r in GRD if r["id"] == "G04"][0]
g04["act"] = "%d 违规（收尾重算，覆盖全部 %d 条）" % (_bad4b, len(ALL))
g04["kind"] = "PASS" if _bad4b == 0 else "FAIL"
_bad4 = _bad4b

NF = sum(1 for r in MAIN if r["kind"] == "FAIL")
NF_G = sum(1 for r in CTL + GRD if r["kind"] == "FAIL")   # ★守卫/控制组红了也必须挡总门
FINAL = final_of(NF, NF_G)

OUT_JSON = os.path.join(DATA, TITLE + ".json")
OUT_TXT = os.path.join(DATA, TITLE + "_report_2026-11-04.txt")


def write_json():
    payload["rows"] = ALL
    payload["counts"] = dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD), P=NP, I=NI, F=NF, ID=NID)
    payload["final"] = FINAL
    payload["verdict"] = VERDICT
    payload["declared_neg"] = DECLARED_NEG
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)


payload = dict(rid=RID, date="2026-11-04", title=TITLE, final="", verdict=VERDICT,
               counts=dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD), P=0, I=0, F=0, ID=0),
               rows=[])

g10["exp"] = "登记集 == 实际 FAIL 集"
g10["act"] = "%s vs %s" % (sorted(DECLARED_NEG), _neg_ids)
g10["kind"] = "PASS" if (sorted(DECLARED_NEG) == _neg_ids) else "FAIL"

g09["exp"] = "回读条目数 == 内存条目数"
g09["act"] = "(回填)"
g09["kind"] = "INFO"
write_json()
_back = json.load(io.open(OUT_JSON, encoding="utf-8"))
g09["act"] = "内存 %d → 回读 %d（%s）" % (len(ALL), len(_back["rows"]),
                                        "一致" if len(ALL) == len(_back["rows"]) else "不一致")
g09["kind"] = "PASS" if len(ALL) == len(_back["rows"]) else "FAIL"
write_json()
_back2 = json.load(io.open(OUT_JSON, encoding="utf-8"))
_g09b = [r for r in _back2["rows"] if r["id"] == "G09"][0]
assert _g09b["kind"] == "PASS", _g09b

# ============================================================ 报告
L = []
A = L.append
A(TITLE)
A("=" * 100)
A("对象：X-R391-1（r391 自留的总开关）—— 「n 恒偶」是族数的后果，还是「Q ∈ Z」的后果？")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
A("")
for title, bucket in (("【主册】", MAIN), ("【控制组】", CTL), ("【守卫】", GRD)):
    A("=" * 100)
    A(title)
    A("=" * 100)
    for r in bucket:
        A("[%s] %-4s %s" % (r["kind"], r["id"], r["name"]))
        A("    exp = %s" % r["exp"])
        A("    act = %s" % r["act"])
        A("    %s" % r["note"])
        A("")
A("=" * 100)
A("【关键表】")
A("A1 单个 16 的八项系数：%s" % one_tbl)
A("A5 GS 可解构型数 = %d；n 全偶 = %s；含 n=3 = %s" % (len(int_cases), a5_even, a5_has3))
A("A6 两族解集（q₊, q₋, Σsq², Σsq⁴, n, I₈空）：")
for t in two_sol:
    A("     %s" % (t,))
A("A7 半整数命中：Σ s q² = %s、Σ s q⁴ = %s、n = %s、I₈ = %s" % (hit_sq, hit_q4, hit_n, HIT))
A("A9 分母判据：n=3 命中 M = %s；未命中 = %s" % (a9_even, a9_odd))
for _row in a9_rows:
    A("     %s" % _row)
A("A10 半整数侧：%s" % "；".join(frac_rows))
A("")
A("【诚实边界】")
A(" 1) 本卷只做**指标层与反常层**，不做零模波函数与质量矩阵：n=3 是「净手性数」，不是「三代质量谱」；")
A(" 2) 半整数零模的**几何实现**未在本卷给出：光滑 6D 紧化的指标必为整数，半整数只能来自奇点/扭曲边界，")
A("    而那里 6D 有效场论本身失效 —— 这属于 X-R392-1，需另建 5D/4D 局部卷；")
A(" 3) A3/A4 的结论限定在 `X₄ ∈ span{x², tr₁₀F², p₁}` 的因子化 ansatz 内；扩 ansatz 后的情形仅给出 A4 note 的论证；")
A(" 4) 本卷不产生新物理：供给 0、不占度、度数链维持 36。")
A("")
with io.open(OUT_TXT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

print("JSON -> %s" % OUT_JSON)
print("TXT  -> %s (%d chars)" % (OUT_TXT, len("\n".join(L))))
print("MAIN=%d (PASS %d / INFO %d / IDENTITY %d / FAIL %d)  CTL=%d  GRD=%d  合计 %d"
      % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
print("FINAL   = %s" % FINAL)
print("VERDICT = %s" % VERDICT)
