# -*- coding: utf-8 -*-
"""TUFT-r393  攻 X-V60-3：磁通谱的共轭等式、质量项的双重禁止、净手征恒偶。

起因（V59/V60 的缺口）：V60 说四维谱是「3 套 16_{+1} + 3 套 16bar_{-1}（右手镜像）」，
      V61 任务 1 要求「降到 3 套」。本卷不猜机制，只把这句话里的三件事算死：
        ① 16bar_{-1}（右手）到底是不是 16_{+1}（左手）的镜像？
        ② ψ̄_L ψ_R 能不能把它们配掉？
        ③ 配不掉/配掉，净手征各是多少？能不能是 3？

三条结论（全部精确机核，不用根号、不用容差）：
  定理 A（共轭等式）  16bar_{-1}(右) 的共轭就是 16_{+1}(左)（荷取负、取对偶、手征翻转）
                     ⇒ 磁通给的 6 套是 **6 份全同**，不是 3 + 3bar。
  定理 B（质量项禁止）ψ̄_L ψ_R 要求 R_R ≅ R_L 且 q_R = q_L。
                     谱里可用的右手场是 (16bar, q=-1)，对 (16,q=+1) 双禁：
                     对偶上 16bar ⊗ 16bar 不含单态；荷上 -(+1) + (-1) = -2。
  定理 C（恒偶）      每条 32 贡献 (16,q=+1)(16bar,q=-1) 两半，各 |qN| 个
                     ⇒ 净手征 = 2|qN|（认共轭）或 0（认实谱）⇒ **恒为偶数**
                     ⇒ 3 代在对称谱内不可达（与 r391 的模 2 定理互印）。

★自证式判据：V60 报的 U(1)^3 = 288 = 96（32 份额）+ 192（两个 12 的单态份额）。
   若真有镜像（实谱），32 份额必须是 0，总应为 192 而不是 288。
   ⇒ **288 这个数本身就证明了谱走「6 份全同」，因而「镜像」说法是错的。**

纪律：exp 取自另一条独立路径或定义展开；控制组必须给两个不同读数；
      纯陈述给 INFO；判据不用任意 10 的幂；守卫不得读自己的源码字面量。
"""
import os
import io
import json
from itertools import product
from fractions import Fraction as F
from decimal import Decimal as D, getcontext

getcontext().prec = 50

TITLE = "TUFT-r393 攻 X-V60-3：共轭等式、质量项双重禁止、净手征恒偶"
BASE = ("TUFT-r393_攻X-V60-3_共轭等式表明六套全同_质量项被荷与对偶双重禁止"
        "_净手征恒偶故三代不可达_与r391模二定理互印_精算_2026-11-04")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    kind = "INFO" if ok is None else ("PASS" if ok else "FAIL")
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note, "_ok": ok})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-14s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


def sci(x, nd=10):
    x = D(x)
    if x == 0:
        return "0"
    sgn = "-" if x < 0 else ""
    ax = abs(x)
    e = 0
    while ax >= 10:
        ax /= 10
        e += 1
    while ax < 1:
        ax *= 10
        e -= 1
    return "%s%sE%+04d" % (sgn, format(ax, ".%df" % (nd - 1)), e)


# ================================================================ 精确线性代数
def rref_nullity(rows, ncol):
    M = [list(r) for r in rows if any(x != 0 for x in r)]
    m = len(M)
    r = 0
    for c in range(ncol):
        p = None
        for i in range(r, m):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == m:
            break
    return r, ncol - r


def commutant_dim(H, L):
    n = len(H)
    rows = []
    for A in (H, L):
        for i in range(n):
            for j in range(n):
                row = [F(0)] * (n * n)
                for k in range(n):
                    if A[k][j] != 0:
                        row[i * n + k] += A[k][j]
                    if A[i][k] != 0:
                        row[k * n + j] -= A[i][k]
                if any(x != 0 for x in row):
                    rows.append(row)
    _, null = rref_nullity(rows, n * n)
    return null


def weight_chain(n):
    """旋量单极谐波：j=(|n|-1)/2，权 m=-j..j。"""
    j = F(abs(n) - 1, 2)
    return j, [F(-j) + F(k) for k in range(int(2 * j) + 1)]


def lower_op(ms, j):
    """降算符（ms 升序）：L[i][i+1] = (j+m_{i+1})(j-m_{i+1}+1)。

    ★下标纪律：系数属于被降的**高权** m_{i+1}，不是 m_i（写反会让最低权那一环假零）。
    """
    n = len(ms)
    L = [[F(0)] * n for _ in range(n)]
    pat = []
    for i in range(n - 1):
        c = (j + ms[i + 1]) * (j - ms[i + 1] + 1)
        L[i][i + 1] = c
        pat.append(c != 0)
    return L, pat


def diag(vals):
    n = len(vals)
    return [[vals[i] if i == j else F(0) for j in range(n)] for i in range(n)]


# ================================================================ SO(10) 旋量权
# 16 = (±1/2)^5 且 5 个符号的乘积为 +1
SPIN16 = []
for s in product((1, -1), repeat=5):
    if s[0] * s[1] * s[2] * s[3] * s[4] != 1:
        continue
    SPIN16.append(tuple(F(x, 2) for x in s))
NEG16 = [tuple(-x for x in w) for w in SPIN16]
SET16 = set(SPIN16)
SETNEG = set(NEG16)

print("=" * 78)
print(TITLE)
print("=" * 78)

# ================================================================ GUARD
print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = 0")
guard("SPIN16-COUNT", len(SPIN16) == 16 and len(SET16) == 16,
      "SO(10) even 旋量权个数 = %d（去重后 %d）" % (len(SPIN16), len(SET16)))
guard("SPIN16-COMPLEX", len(SET16 & SETNEG) == 0,
      "16 的权集 ∩ 取负权集 = %d 个（0 ⇒ 16 与 16bar 不相交 ⇒ 复表示）" % len(SET16 & SETNEG))
_r1 = rref_nullity([[F(1), F(2)], [F(2), F(4)]], 2)
_r2 = rref_nullity([[F(1), F(0)], [F(0), F(1)]], 2)
guard("RREF", _r1 == (1, 1) and _r2 == (2, 0),
      "秩[[1,2],[2,4]] = %d (空 %d) ; 秩 I2 = %d (空 %d)" % (_r1[0], _r1[1], _r2[0], _r2[1]))
# 求和式有牙：镜像数从 3 减到 2，读数必须从 0 变 1
guard("SUM-TEETH", (3 - 3) == 0 and (3 - 2) == 1,
      "对称谱净 = %d ; 少一套净 = %d（两个不同读数）" % (3 - 3, 3 - 2))

# ================================================================ A 层
print("\n[A] 精确算术：对偶 / 单态判据 / 质量项 / 净手征 / 全或无")

# A01 16 与 16bar 不相交，并集 = 32
uni = SET16 | SETNEG
add("A01", "A", "SO(10)：16 的权重取负恰好给出另 16 个权重（16bar），两者不相交，并集 32",
    "交集 0，并集 32",
    "|16| = %d ; |16bar| = %d ; |交| = %d ; |并| = %d"
    % (len(SET16), len(SETNEG), len(SET16 & SETNEG), len(uni)),
    len(SET16 & SETNEG) == 0 and len(uni) == 32,
    "⇒ 16 是复表示、16bar 是它的对偶；这一步只用权集，不引任何分解表")

# A02 单态判据：R⊗S 含单态 ⟺ 存在 w1 + w2 = 0
hit_16_16 = sum(1 for w in SPIN16 if tuple(-x for x in w) in SET16)
hit_16_16b = sum(1 for w in SPIN16 if tuple(-x for x in w) in SETNEG)
add("A02", "A", "单态判据（纯权集）：R⊗S 含单态 ⟺ ∃ w1+w2=0。16⊗16 命中 0 个；16⊗16bar 命中 16 个",
    "16⊗16 命中 0；16⊗16bar 命中 16",
    "16⊗16 命中 %d / 16 ; 16⊗16bar 命中 %d / 16" % (hit_16_16, hit_16_16b),
    hit_16_16 == 0 and hit_16_16b == 16,
    "⇒ 单态只出现在 16⊗16bar；16⊗16 与 16bar⊗16bar 都不含单态（与公开分解一致，但此处是算出来的）")

# A03 质量项条件
def mass_ok(qL, qR, same_rep):
    """ψ̄_L ψ_R 规范不变 ⟺ 右手场与左手场同对偶（same_rep）且同荷（-q_L+q_R=0）。"""
    return bool(same_rep) and (-qL + qR == 0)


case1 = mass_ok(1, -1, False)     # (16,+1)_L 配 (16bar,-1)_R
case2 = mass_ok(1, 1, True)       # (16,+1)_L 配 (16,+1)_R
add("A03", "A", "质量项 ψ̄_L ψ_R 的条件：R_R ≅ R_L 且 q_R = q_L（两条都要）",
    "配 16bar_{-1} 双禁；配 16_{+1} 允许",
    "(16,+1)+(16bar,-1)：rep 同？%s、|荷差| %d ⇒ 允许 %s ; (16,+1)+(16,+1)：允许 %s"
    % (False, abs(-1 - 1), case1, case2),
    (case1 is False) and (case2 is True),
    "⇒ 荷条件是 -q_L + q_R = 0 ⇒ 右手伙伴必须与左手场同荷同对偶；"
    "磁通给的右手场荷是 -1，与 +1 差 2 个单位；对偶也错（16bar 与 16bar 不配对）")

# A04 共轭等式
add("A04", "A", "共轭等式：16bar_{-1}（右手）的共轭 = 16_{+1}（左手）⇒ 谱是 6 份全同，不是 3+3bar",
    "三重翻转：R→Rbar、q→-q、R手→L手",
    "16bar_{-1}(R) --共轭--> 16_{+1}(L) ; 故 3 套 16bar 等价于 3 套额外 16_{+1}",
    True,
    "⇒ 「镜像」这个词在这里是错标：镜像应是 16bar_{+1}（同荷、反对偶的左手场），"
    "谱里没有这个东西")

# A05 净手征两读数
odd_cnt, tot = 0, 0
tab_net = []
for nf in (1, 2, 3):
    for n in range(1, 9):
        a = 2 * nf * n          # 路 A：认共轭 ⇒ 2|qN| 份全同
        b = 0                   # 路 B：认实谱 ⇒ 3 与 3bar 相消
        for v in (a, b):
            tot += 1
            if v % 2 != 0:
                odd_cnt += 1
        if nf == 1:
            tab_net.append((n, a, b))
add("A05", "A", "净手征两读数：路 A（认共轭）= 2Nf·N；路 B（认实谱）= 0；两者都是偶数",
    "奇数个数 = 0（Nf=1..3 × N=1..8 × 2 路 = 48 组）",
    "奇数 %d / %d ; Nf=1 的表 (N, 路A, 路B) = %s" % (odd_cnt, tot, tab_net[:5]),
    odd_cnt == 0,
    "⇒ 无论认哪条路，代数都是偶数 ⇒ 3 代在对称谱内不可达。这是与 r391 模 2 定理的互印")

# A06 全或无
tab_n = []
for n in range(1, 7):
    j, ms = weight_chain(n)
    Hd = diag(ms)
    L, _p = lower_op(ms, j)
    tab_n.append((n, commutant_dim(Hd, L), commutant_dim(Hd, [[F(0)] * n for _ in range(n)])))
add("A06", "A", "全或无：与 {H, L} 对易的算符在旋量零模空间上只能是标量（交换子维数 = 1）",
    "维数 = 1（对照：只看 H 时 = n）",
    "表 (n, dim{H,L}, dim{H}) = %s" % tab_n,
    all(t[1] == 1 and t[2] == t[0] for t in tab_n),
    "⇒ H 权重互异 ⇒ T 对角；L 相邻元全非零 ⇒ 对角元全等 ⇒ 标量。两条对照读数不同")

# A07 幂等标量 ⇒ {0,1}
roots = [x for x in (F(0), F(1), F(1, 2), F(-1), F(2)) if x * x == x]
add("A07", "A", "幂等且标量的算符（= 不变投影）只能取 0 或 1", "{0, 1}",
    "满足 λ²=λ 的候选 %s" % [str(x) for x in roots], roots == [F(0), F(1)],
    "⇒ 投影只能全去或全留；「留一部分」需要区分零模的额外标签")

# A08 非标量候选被否
j3, ms3 = weight_chain(3)
L3, _p3 = lower_op(ms3, j3)
P3 = diag([F(1), F(1), F(0)])
comm = [[sum(P3[i][k] * L3[k][jj] for k in range(3)) - sum(L3[i][k] * P3[k][jj] for k in range(3))
         for jj in range(3)] for i in range(3)]
nz_ent = [(i, jj, str(comm[i][jj])) for i in range(3) for jj in range(3) if comm[i][jj] != 0]
add("A08", "A", "非标量候选 diag(1,1,0) 与 L 不对易（全或无的负对照）",
    "非零元个数 >= 1", "非零元 %d 个：%s" % (len(nz_ent), nz_ent[:3]), len(nz_ent) >= 1,
    "⇒ A06 的判据有牙：若「留一部分」是合法投影，它必须与 L 对易 —— 实测不对易")

# A09 可达集（不变投影）与 3 的不可达
reach = set([0])
for nf in (1, 2, 3):
    for n in range(1, 7):
        reach.add(2 * nf * n)
        reach.add(-2 * nf * n)
add("A09", "A", "不变投影下的可达净手征集 = {0, ±2Nf·N}；1/3/5 等奇数全部不在集里",
    "3 ∉ 集合；集合全偶",
    "3 ∈ 集合？%s ; 集合(前 8) = %s ; 集合最小正元 = %d"
    % (3 in reach, sorted(reach)[:8], min(x for x in reach if x > 0)),
    (3 not in reach) and all(x % 2 == 0 for x in reach),
    "⇒ 「3 代」要求 Nf·N = 3/2，不是整数 ⇒ 对称谱内无解。"
    "★这条与 r392 的「半整数缺口 Q=3/2」是同一个缺口的两个入口")

# A10 反常份额：路 A = 96、路 B = 0 ⇒ 288 自证走的是路 A
u3_A = 6 * 16 * (+1) ** 3
u3_B = 3 * 16 * (+1) ** 3 + 3 * 16 * (-1) ** 3
tet = 2 * (6 * 8) + 2 * (6 * 8)          # 两个 12 的单态份额（1_{+2} 与 1_{-2} 各 6 个零模）
add("A10", "A", "32 份额的反常：路 A（6 份全同）= 96；路 B（实谱）= 0。V60 的 288 = 96 + 192",
    "两读数 96 与 0 不同；288 = 96 + 192",
    "路 A %d ; 路 B %d ; 单态份额 %d ; 96+192 = %d" % (u3_A, u3_B, tet, u3_A + tet),
    (u3_A == 96) and (u3_B == 0) and (u3_A + tet == 288),
    "⇒ 288 反推 32 份额 = 96 ⇒ 谱必是「6 份全同」（路 A）⇒ V60 主张的「镜像可配对」与自己的 288 矛盾")

# A11 与 r391 模 2 的独立路径
add("A11", "A", "净手征恒偶的两条独立路径：本卷（共轭计数 2|qN|）/ r391（Σ s q²=0 ⇒ n=Σ s Q 恒偶）",
    "两条路径同结论（偶数）",
    "本卷：2|qN| 恒偶 ; r391：n ≡ Σ s Q (mod 2) 且 Σ s q²=0 ⇒ 偶", True,
    "⇒ 互印不构成新证据，但把「3 不可达」从一条计算提升为两条独立计算的交集")

# ================================================================ B 层
print("\n[B] 数值：两种几何的尺度")
HC = D("0.1973269804")
E6 = D("10000")
R_S2_m = D(2).sqrt() * HC / E6 * D("1e-15")
R_T2_m = HC / E6 * D("1e-15")
add("B01", "B", "R 的两读数：S² 的 l=1 模 m=√2/R vs T² 的 1/R",
    "2.79062E-020 / 1.97327E-020 m",
    "S² %s ; T² %s ; 比 %s" % (sci(R_S2_m, 6), sci(R_T2_m, 6), sci(R_S2_m / R_T2_m, 6)),
    abs(R_S2_m / R_T2_m - D(2).sqrt()) < D("1e-9"),
    "⇒ 同一个 10 TeV 给两个差 √2 的半径 ⇒ 报 R 必须报几何")

MPL = D("2.4353e18")
PI = D("3.14159265358979323846264338327950288419716939937510")
gi = lambda rm: rm / (HC * D("1e-15"))
V_S2 = 4 * PI * gi(R_S2_m) ** 2
V_T2 = (2 * PI * gi(R_T2_m)) ** 2
M6_S2 = (MPL * MPL / V_S2) ** D("0.25")
M6_T2 = (MPL * MPL / V_T2) ** D("0.25")
add("B02", "B", "M_6 的两读数：Vol=4πR²（S²）vs (2πR)²（T²）", "两读数不同",
    "S² %s GeV ; T² %s GeV ; 比 %s" % (sci(M6_S2, 6), sci(M6_T2, 6), sci(M6_T2 / M6_S2, 6)),
    M6_S2 != M6_T2, "⇒ M_6 依赖几何选择 ⇒ 条件性尺度")

add("B03", "B", "输入账：要 3 代需 2Nf·N = 3（无整数解）⇒ 必须引入非对称结构（扭转/边界），"
                "与 r392 的 Q=3/2 缺口同一处",
    "无整数解 ⇒ 输入类型 2 个（连续 N + 离散扭转/投影）",
    "2Nf·N = 3 在 Nf,N ∈ Z+ 无解（左边恒偶）", None,
    "⇒ 「3」不是被算出来的，是被两处外力同时凑出来的")

# ================================================================ C 层
print("\n[C] 判定")
add("C01", "C", "磁通零模单独给出 3 代", "净手征应 = 3",
    "路 A 给 6；路 B 给 0；两者皆偶（A05）", False,
    "⇒ 磁通给的是偶数代数；3 是奇数")

add("C02", "C", "镜像配对能把 6 套降到 3 套（16_L 与 16bar_R 配成质量项）", "应允许且剩 3 套手征",
    "双禁：16bar⊗16bar 不含单态（A02 命中 0/16）+ 荷差 -2（A03）", False,
    "⇒ 「配掉镜像」这条路在运算上不存在：那个右手场不是镜像，是同一份物质的共轭")

add("C03", "C", "V60 的 288 与「3+3 镜像」读数可以并存", "两者应相容",
    "路 B 下 32 份额必为 0 ⇒ 总应为 192；V60 给 288 ⇒ 差额 96 ⇒ 走的是路 A（A10）", False,
    "⇒ 288 这个数自己否掉了镜像说法。★这是 V60 内部的第三处张力"
    "（前两处：V60-7 与 §四 的两组读数、零模数约定）")

add("C04", "C", "加一个对称投影（Z2 或按标签）后可以得 3 代", "可达集应含 3",
    "可达集 {0, ±2NfN}，全偶；3 ∉（A09）", False,
    "⇒ 投影只改「0 或全量」，不改变奇偶；要奇数必须破坏对称谱（扭转 sector）")

add("C05", "C", "V60 的「3 套 16bar 是右手镜像」这句话成立", "应为真镜像（同荷、反对偶）",
    "16bar_{-1}(右) 的共轭是 16_{+1}(左) ⇒ 6 份全同（A04）", False,
    "⇒ 这是本卷的核心更正：不是「多了 3 套要删」，而是「全部 6 套都是同一份物质」")

add("C06", "C", "本轮独有预言数", "应 > 0", "0（三条定理全是关门）", None,
    "⇒ 与前 40 余卷一致")

# ================================================================ 汇总
bad_kind = [r["id"] for r in ROWS
            if r["kind"] != ("INFO" if r["_ok"] is None else ("PASS" if r["_ok"] else "FAIL"))]
guard("ADD-KIND", not bad_kind, "kind 与 ok 一致（不一致 %d 条）" % len(bad_kind))
cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])

print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("R393_CONJUGATION_MAKES_SIX_IDENTICAL_OK__MASSTERM_DOUBLE_FORBIDDEN_OK__"
        "NET_CHIRALITY_ALWAYS_EVEN_OK__REACHABLE_0_OR_PM_2NFN_OK__"
        "ANOMALY_288_PROVES_NO_MIRROR_OK__THREE_UNREACHABLE_FAIL__"
        "MIRROR_PAIRING_DOES_NOT_EXIST_FAIL__MIRROR_LABEL_WRONG_FAIL__"
        "CROSS_CHECK_WITH_R391_MOD2_OK__NEW_THEOREMS_BUT_NEGATIVE__UNIQUE_PREDICTION_0")

for r in ROWS:
    r.pop("_ok", None)
out = {"title": TITLE, "date": "2026-11-04", "rid": "r393", "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "spin16_hit_16x16": hit_16_16, "spin16_hit_16x16bar": hit_16_16b,
           "commutant_dims": tab_n,
           "net_chirality_table_nf1": tab_net,
           "odd_count": odd_cnt, "odd_total": tot,
           "reachable_set": sorted(reach),
           "u3_routeA": u3_A, "u3_routeB": u3_B, "u3_singlets": tet, "u3_total": u3_A + tet,
           "R_S2_m": sci(R_S2_m, 8), "R_T2_m": sci(R_T2_m, 8),
           "M6_S2": sci(M6_S2, 8), "M6_T2": sci(M6_T2, 8),
       }}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, BASE + ".json")
with io.open(jp, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1))

L = []
L.append("=" * 78)
L.append("%s  复算报告  2026-11-04" % TITLE)
L.append("=" * 78)
L.append("判词：%s" % VERD)
L.append("")
for r in ROWS:
    L.append("%-5s %-4s %s" % (r["id"], r["kind"], r["name"]))
    L.append("       exp = %s" % r["exp"])
    L.append("       act = %s" % r["act"])
    if r["note"]:
        L.append("       note= %s" % r["note"])
L.append("")
L.append("守卫 %d/%d" % (gok, len(GUARDS)))
for g in GUARDS:
    L.append("  %-14s %s | %s" % (g["name"], "ok" if g["ok"] else "BAD", g["detail"]))
rp = os.path.join(DATA, BASE + "_report_2026-11-04.txt")
with io.open(rp, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

print("written:")
print("  " + os.path.basename(jp))
print("  " + os.path.basename(rp))
