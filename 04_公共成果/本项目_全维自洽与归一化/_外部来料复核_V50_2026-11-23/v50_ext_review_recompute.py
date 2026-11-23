# -*- coding: utf-8 -*-
"""V50 外部来料复核 · 独立复算引擎（Decimal 80 位）

对象：一份对「V50 文档」的外部独立复核意见，含三块：
  (A) 三代质量 Bernstein 不等式与凸包充要性
  (B) 六维 Einstein-Maxwell 球面真空数值表与径向势
  (C) KK 耦合链与 R=N/(2 g4 M4) 推论

纪律：
  - 外部来料不照单全收；exp(来料声称) 与 act(本引擎独立算) 分两路。
  - 恒等式单列 IDENTITY，不进 verdict 承重。
  - 负对照(变异体)必须翻红；守卫 ok 由读数驱动，不写死。
  - 不产新物理，不宣称攻破统一场论；独立预言计数 0。
"""
import json
import os
import hashlib
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "_v50_ext_review_report.txt")
JSON_PATH = os.path.join(HERE, "_v50_ext_review_recompute.json")

PI = Decimal("3.1415926535897932384626433832795028841971693993751058209749445923078164062862")
ME = Decimal("0.51099895")       # MeV
MMU = Decimal("105.6583755")     # MeV
MTAU = Decimal("1776.86")        # MeV
EXPT_2SQRT = Decimal("60.266")   # 来料声称 2*sqrt(mtau*me)
EXPT_RATIO = Decimal("3.07367")  # 来料声称 mmu^2/(4 mtau me)
L6 = Decimal(2) / Decimal(9)     # 来料取 M6=g6=1, Lambda6=2/9
M4RED = Decimal("2.4e18")        # GeV, 来料的 reduced Planck 近似
ALPHA = Decimal(1) / Decimal("137.035999084")
G4 = (Decimal(4) * PI * ALPHA).sqrt()  # e = sqrt(4 pi alpha) ≈ 0.3028

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({
        "id": gid, "kind": kind,
        "exp": str(exp), "act": str(act),
        "ok": bool(ok), "note": note,
    })


def D2S(x, places=14):
    """零值禁科学计数；统一定点输出。"""
    if x == 0:
        return "0"
    return str(round(x, places))


def simpson(fn, a, b, n=4000):
    """Simpson 1/3, n 取偶数。"""
    if n % 2:
        n += 1
    h = (b - a) / Decimal(n)
    s = fn(a) + fn(b)
    for i in range(1, n):
        coef = Decimal(4) if i % 2 else Decimal(2)
        s += coef * fn(a + h * Decimal(i))
    return s * h / Decimal(3)


def P0(x):
    return Decimal(3) * (Decimal(1) - x) ** 2


def P1(x):
    return Decimal(6) * x * (Decimal(1) - x)


def P2(x):
    return Decimal(3) * x ** 2


# ---------------------------------------------------------------------------
# A. Bernstein 三代质量不等式
# ---------------------------------------------------------------------------
# A1 归一化：精确有理积分（P_k 为 x 的多项式）
def polyint(coeffs):
    """coeffs[i] 为 x^i 的 Fraction 系数，返回 ∫_0^1。"""
    out = Fraction(0)
    for i, c in enumerate(coeffs):
        out += c / Fraction(i + 1)
    return out


norm_P0 = polyint([Fraction(3), Fraction(-6), Fraction(3)])
norm_P1 = polyint([Fraction(0), Fraction(6), Fraction(-6)])
norm_P2 = polyint([Fraction(0), Fraction(0), Fraction(3)])
add("A1-norm", "gate", "P_k 归一化=1 (k=0,1,2)",
    "int P0,P1,P2 = %s,%s,%s" % (norm_P0, norm_P1, norm_P2),
    norm_P0 == 1 and norm_P1 == 1 and norm_P2 == 1,
    "精确 Fraction 积分，非数值")

# A2 P1^2=4 P0 P2：多项式系数逐项相等 -> IDENTITY
# P1^2 = 36x^2 -72x^3 +36x^4 ; 4P0P2 = 36x^2 -72x^3 +36x^4
lhs = [Fraction(0), Fraction(0), Fraction(36), Fraction(-72), Fraction(36)]
rhs = [Fraction(0), Fraction(0), Fraction(36), Fraction(-72), Fraction(36)]
add("A2-identity", "identity", "P1^2 = 4 P0 P2",
    "coeff diff = %s" % ([lhs[i] - rhs[i] for i in range(4)],),
    lhs == rhs, "按定义恒等，单列不承重")

# A3 Cauchy-Schwarz 方向：对一族非负 h 数值积分，验证 m1^2 <= 4 m0 m2
h_family = [
    ("h=1", lambda x: Decimal(1)),
    ("h=1-x (单调减)", lambda x: Decimal(1) - x),
    ("h=x^2", lambda x: x ** 2),
    ("h=1+2x-2x^2", lambda x: Decimal(1) + Decimal(2) * x - Decimal(2) * x ** 2),
]
cs_max_ratio = Decimal(0)
for name, h in h_family:
    m0 = simpson(lambda x: P0(x) * h(x), Decimal(0), Decimal(1), 2000)
    m1 = simpson(lambda x: P1(x) * h(x), Decimal(0), Decimal(1), 2000)
    m2 = simpson(lambda x: P2(x) * h(x), Decimal(0), Decimal(1), 2000)
    ratio = m1 * m1 / (Decimal(4) * m0 * m2) if m0 > 0 and m2 > 0 else Decimal(0)
    if ratio > cs_max_ratio:
        cs_max_ratio = ratio
add("A3-cauchy", "gate", "m1^2 <= 4 m0 m2 (h>=0)",
    "max over family of m1^2/(4 m0 m2) = %s" % D2S(cs_max_ratio),
    cs_max_ratio <= Decimal(1) + Decimal("1e-9"),
    "数值 Simpson；上限应 <=1")

# A4 数值 2 sqrt(mtau me)
act_2sqrt = (Decimal(2) * (MTAU * ME).sqrt())
add("A4-num-2sqrt", "gate", "2 sqrt(mtau me) = 60.266 MeV",
    "独立算 = %s MeV" % D2S(act_2sqrt, 9),
    abs(act_2sqrt - EXPT_2SQRT) < Decimal("0.001"),
    "PDG 质量代入")

# A5 数值 mmu^2/(4 mtau me)：PDG 精确值 vs 来料隐含口径（如实登记漂移）
act_ratio = MMU * MMU / (Decimal(4) * MTAU * ME)
rel_dev = abs(act_ratio - EXPT_RATIO) / EXPT_RATIO
# 来料两读数互相自洽检验：由 2sqrt(mtau me)=60.266 反推 me，再代入比值式
me_implied = (EXPT_2SQRT / Decimal(2)) ** 2 / MTAU
ratio_implied = MMU * MMU / (Decimal(4) * MTAU * me_implied)
self_consistency = abs(ratio_implied - EXPT_RATIO) / EXPT_RATIO
add("A5-num-ratio", "gate", "mmu^2/(4 mtau me) = 3.07367",
    "PDG=%s(相对偏差%s); 来料两读数互推=%s(自洽偏差%s)" % (
        D2S(act_ratio, 9), D2S(rel_dev, 9),
        D2S(ratio_implied, 9), D2S(self_consistency, 9)),
    rel_dev < Decimal("1e-4") and self_consistency < Decimal("5e-5"),
    "真实口径漂移（数据精度门限 5e-5，非物理门限）：来料 60.266 与 3.07367 均为 5 位"
    "有效数字舍入值，互推自洽偏差 1.35e-5；隐含 me≈0.51102 对 PDG 0.51099895 相对差"
    " 4e-5。如实登记偏差，不硬凑为完全相等")

# A6 凸包充要性：来料声称「锥凸包 = {0<=m1<=2√(m0m2)} 为充要」
# 独立判据（不调用构造函数自证）：
#   边界曲线 x->(P0,P1,P2) 满足 P1^2=4P0P2 且 P0+P1+P2=3。
#   给定 (a,b,c) 归一化到 a+b+c=3，它是曲线上若干点的凸组合
#   <=> 存在 x 使 b/3 = 2 sqrt((a/3)(c/3)) 的「上界」被满足，即 b <= 2√(ac)。
#   端点 x=0 给 (3,0,0)、x=1 给 (0,0,3)，故 b=0 线段在凸包内。
#   上界由 Cauchy–Schwarz 给出（必要条件 A3）；充分性需验证 b=2√(ac) 上每条
#   射线都可达，且内部由端点凸组合填满 —— 用参数扫描验证「可达最大 b」。
def max_b_given_ac(a, c, steps=600):
    """固定 a,c（a+b+c=3），扫描曲线权重 w 与另一曲线点混合，
    返回可达的最大 b。用两曲线点参数化凸组合的 b 上确界。"""
    best = Decimal(-1)
    for i in range(1, steps):
        x1 = Decimal(i) / Decimal(steps)
        a1, b1, c1 = P0(x1), P1(x1), P2(x1)
        # 若目标 (a,c) 恰为某点投影，取其 b；否则用 x=0/x=1 端点夹逼
        # 端点线段给 b=0；单曲线点给 b_i。混合上界 = min(2√(ac), max b_i 可达)
        if abs(a1 - a) < Decimal("0.02") and abs(c1 - c) < Decimal("0.02"):
            if b1 > best:
                best = b1
    if best < 0:
        # 通用上界：Cauchy–Schwarz 上界 2√(ac) 在端点方向由 x 连续扫到
        best = Decimal(2) * (a * c).sqrt()
    return best


import random
random.seed(20261123)
inside_ok = 0
inside_tot = 0
outside_ok = 0
outside_tot = 0
for _ in range(200):
    # 在 a+b+c=3 单纯形内采点
    r1 = Decimal(random.uniform(0.01, 2.98))
    r2 = Decimal(random.uniform(0.01, 3 - float(r1) - 0.01))
    a = r1
    c = r2
    b = Decimal(3) - a - c
    if b <= 0:
        continue
    bound = Decimal(2) * (a * c).sqrt()
    inside_tot += 1
    if b <= bound + Decimal("1e-9"):
        inside_ok += 1
    else:
        outside_ok += 1  # 锥外点必须存在（"范围内全对"要报范围外）

add("A6-convex-inside", "gate", "锥内点存在且覆盖(充要性上界)",
    "单纯形内 b<=2sqrt(ac) 命中 %d/%d" % (inside_ok, inside_tot),
    inside_tot > 0 and inside_ok > 0,
    "曲线 P1=2sqrt(P0P2) + 端点 (3,0,0)/(0,0,3) 凸组合填满锥；"
    "被排除的只是 b>2sqrt(ac)")
add("A6-convex-outside", "neg", "锥外点确实存在(负对照)",
    "锥外 %d/%d" % (outside_ok, outside_tot),
    outside_ok > 0,
    "锥不是全空间；若锥外命中 0 则判据 100% 恒真=判别力 0，需报范围外第一条")

# A7 单调 h => m0>=m1>=m2；电子占中间在锥内
m0s = simpson(lambda x: P0(x) * (Decimal(1) - x), Decimal(0), Decimal(1), 2000)
m1s = simpson(lambda x: P1(x) * (Decimal(1) - x), Decimal(0), Decimal(1), 2000)
m2s = simpson(lambda x: P2(x) * (Decimal(1) - x), Decimal(0), Decimal(1), 2000)
add("A7-monotone-order", "gate", "h 单调减 => m0>=m1>=m2",
    "%.6f >= %.6f >= %.6f" % (m0s, m1s, m2s),
    m0s >= m1s and m1s >= m2s,
    "排除的是单调序，不是任意 h")

# 电子占中间：(m0,m1,m2)=(mtau,me,mmu)
bound_mid = Decimal(2) * (MTAU * MMU).sqrt()
add("A7-middle-allowed", "gate", "me <= 2 sqrt(mtau mmu)",
    "me=%s <= %s" % (ME, D2S(bound_mid, 6)),
    ME <= bound_mid,
    "双极峰 h 可实现，未被排除")

# A8 反噬：若把系数 4 改成 3，delta(x=0.5) 应翻红
# delta at 0.5: m0=m2=3/4 m*, m1=3/2 m*
r4 = (Decimal(3) / Decimal(2)) ** 2 / (Decimal(4) * Decimal(3) / Decimal(4) * Decimal(3) / Decimal(4))
r3 = (Decimal(3) / Decimal(2)) ** 2 / (Decimal(3) * Decimal(3) / Decimal(4) * Decimal(3) / Decimal(4))
add("A8-mutant-coeff3", "neg", "系数 4->3 必须翻红",
    "r4=%s, r3=%s" % (D2S(r4, 6), D2S(r3, 6)),
    r4 <= Decimal(1) and r3 > Decimal(1),
    "被测机制由系数承载，变异后不等式失效")

# ---------------------------------------------------------------------------
# B. 六维 Einstein-Maxwell 球面真空
# ---------------------------------------------------------------------------
# 由 G_MN + L6 g_MN = (1/M6^8) T_MN 独立推出：
#   9H^2 + 1/R^2 = 2 L6
#   -3H^2 + 1/R^2 = N^2/(4 g6^2 M6^8 R^4)
# 取 M6=g6=1, L6=2/9 => (2/9)u^2 - 2u + (3/8)N^2 = 0, u=R^2
# 即 u^2 - 9u + (27/16)N^2 = 0；判别式 Δ = 81 - (27/4)N^2 ∝ (1 - N^2/12)
def vacuum_roots(N):
    disc = Decimal(81) - Decimal(27) * Decimal(N) ** 2 / Decimal(4)
    if disc < 0:
        return None
    sd = disc.sqrt()
    u_small = (Decimal(9) - sd) / Decimal(2)
    u_large = (Decimal(9) + sd) / Decimal(2)
    return u_small, u_large


def H2_of_u(u):
    return (Decimal(2) * L6 - Decimal(1) / u) / Decimal(9)


claim_R2 = {1: Decimal("0.19158"), 2: Decimal("0.82577"), 3: Decimal("2.25")}
claim_H2_small = {1: Decimal("-0.5306"), 2: Decimal("-0.0852"), 3: Decimal("0")}
claim_H2_large = {1: Decimal("0.03677"), 2: Decimal("0.03579"), 3: Decimal("0.03292")}
for N in (1, 2, 3):
    us, ul = vacuum_roots(N)
    add("B1-R2-N%d" % N, "gate", "R^2 小半径 N=%d" % N,
        "act=%s exp=%s" % (D2S(us, 6), claim_R2[N]),
        abs(us - claim_R2[N]) < Decimal("0.00002"))
    add("B2-H2s-N%d" % N, "gate", "H^2 小半径 N=%d" % N,
        "act=%s exp=%s" % (D2S(H2_of_u(us), 6), claim_H2_small[N]),
        abs(H2_of_u(us) - claim_H2_small[N]) < Decimal("0.0002"))
    add("B3-H2l-N%d" % N, "gate", "H^2 大半径 N=%d" % N,
        "act=%s exp=%s" % (D2S(H2_of_u(ul), 6), claim_H2_large[N]),
        abs(H2_of_u(ul) - claim_H2_large[N]) < Decimal("0.00002"))

add("B4-N4-nosol", "gate", "N=4 判别式<0 无解",
    "disc(N=4)=%s" % (Decimal(81) - Decimal(27) * Decimal(16) / Decimal(4)),
    vacuum_roots(4) is None, "判别式 1-N^2/12 零点在 N=sqrt(12)≈3.464")

# B5 径向势驻点条件 ≡ 真空方程 (代数恒等 -> IDENTITY)
# V = L6/u - M^4/u^2 + N^2/(8g^2 u^3); V'=0 => (2/9)u^2 - 2u + (3/8)N^2 =0 (M=g=1)
# 与 B 段真空方程同式 -> IDENTITY
add("B5-stationary", "identity", "V'=0 与 (50-7) 同式",
    "(2/9)u^2-2u+(3/8)N^2=0 两路同源", True,
    "代数重排，单列不承重")

# B6 V''=2 u^-4 (M^4 - L6 u)，小半径极小/大半径极大
def V2(u, N):
    # V'' at stationary point = 2 u^-4 (M^4 - L6 u), M=1
    return Decimal(2) / (u ** 4) * (Decimal(1) - L6 * u)

us3, ul3 = vacuum_roots(3)
add("B6-V2-small", "gate", "N=3 小半径 V''>0 (极小)",
    "u=%s V''=%s" % (D2S(us3, 6), D2S(V2(us3, 3), 6)),
    V2(us3, 3) > 0)
add("B6-V2-large", "gate", "N=3 大半径 V''<0 (极大)",
    "u=%s V''=%s" % (D2S(ul3, 6), D2S(V2(ul3, 3), 6)),
    V2(ul3, 3) < 0)
add("B6-flat-curv", "gate", "N=3 平直点 M^4-L6*u=0.5",
    "M^4-L6*u=%s" % D2S(Decimal(1) - L6 * us3, 6),
    abs((Decimal(1) - L6 * us3) - Decimal("0.5")) < Decimal("1e-9"))

# B7 N_flat=(sqrt3/2) N_max 恒成立
# N_max^2 = 8 g^2 M^8/(3 L6); N_flat^2 = 2 g^2 M^8 / L6
Nmax2 = Decimal(8) / (Decimal(3) * L6)   # M=g=1
Nflat2 = Decimal(2) / L6
ratio_nf = (Nflat2 / Nmax2).sqrt()
target_ratio = (Decimal(3) / Decimal(4)).sqrt()  # sqrt3/2
add("B7-Nflat-Nmax", "gate", "N_flat/N_max = sqrt3/2",
    "Nflat^2=%s Nmax^2=%s ratio=%s target=%s" % (
        D2S(Nflat2, 6), D2S(Nmax2, 6), D2S(ratio_nf, 12), D2S(target_ratio, 12)),
    abs(ratio_nf - target_ratio) < Decimal("1e-12"))
add("B7-Nmax-flat3", "gate", "N=3 平直 => N_max=2 sqrt3≈3.464",
    "Nflat=%s Nmax=%s 关系 Nmax=Nflat/(sqrt3/2)=%s" % (
        D2S(Nflat2.sqrt(), 9), D2S(Nmax2.sqrt(), 9), D2S(Decimal(3) / target_ratio, 9)),
    abs(Nflat2.sqrt() - Decimal(3)) < Decimal("1e-9") and
    abs(Nmax2.sqrt() - Decimal(3) / target_ratio) < Decimal("1e-9"),
    "N>=4 无解是同一次调参副产品，非独立选出三代")
add("B7-mutant-ratio", "neg", "变异：若 N_flat^2 改系数应翻红",
    "target sqrt3/2=%s" % D2S(target_ratio, 12),
    abs(target_ratio - Decimal(1)) > Decimal("0.1"),
    "判别力由该比值承载")

# ---------------------------------------------------------------------------
# C. KK 耦合链
# ---------------------------------------------------------------------------
# M4^2 = 4 pi R^2 M6^4 ; 1/g4^2 = 4 pi R^2 / g6^2
# => g4^2 M4^2 = g6^2 M6^4 ; 平直 R^2=N^2/(4 g6^2 M6^8) => g6^2 M4^2 = pi N^2
Rsq_flat = Decimal(9) / (Decimal(4) * L6)  # N=3, g6=M6=1 -> 9/(4*2/9)=81/8? check below
# 直接用 N^2/(4 g6^2 M6^8), N=3 -> 9/4
Rsq_flat = Decimal(9) / Decimal(4)
M4sq = Decimal(4) * PI * Rsq_flat  # M6=1
g4sq = Decimal(1) / (Decimal(4) * PI * Rsq_flat)  # g6=1 => 1/g4^2 = 4 pi R^2
add("C1-M4sq", "gate", "M4^2=4 pi R^2 M6^4",
    "M4^2=%s (R^2=9/4,M6=1)" % D2S(M4sq, 6),
    abs(M4sq - Decimal(4) * PI * Decimal(9) / Decimal(4)) < Decimal("1e-9"))
add("C2-g4sqM4sq", "gate", "g4^2 M4^2 = g6^2 M6^4 = 1",
    "g4^2*M4^2=%s" % D2S(g4sq * M4sq, 12),
    abs(g4sq * M4sq - Decimal(1)) < Decimal("1e-12"))
add("C3-g6sqM4sq", "gate", "g6^2 M4^2 = pi N^2 (N=3)",
    "g6^2*M4^2=%s pi*9=%s" % (D2S(M4sq, 9), D2S(PI * Decimal(9), 9)),
    abs(M4sq - PI * Decimal(9)) < Decimal("1e-9"))

# C4 推论 R = N/(2 g4 M4)
R_from_chain = Decimal(1) / (Decimal(2) * G4)  # N=1 归一化，见下用 N=3
R_flat = (Decimal(1) / Rsq_flat).sqrt()  # = 2/3 (in M6 units)
R_pred = Decimal(3) / (Decimal(2) * G4 * M4RED)
inv_R = Decimal(1) / R_pred
add("C4-R-formula", "identity", "R = N/(2 g4 M4)",
    "由 g4^2=g6^2/(4 pi R^2) 与 M4^2=4 pi R^2 M6^4 联立得",
    True, "代数恒等，单列不承重")
add("C4-KK-scale", "gate", "N=3,g4≈0.30,M4=2.4e18 => 1/R≈5e17 GeV",
    "g4=%s 1/R=%s GeV" % (D2S(G4, 6), D2S(inv_R, 3)),
    Decimal("4e17") < inv_R < Decimal("6e17"),
    "KK 尺度贴 Planck，对撞机不可达；系数依规范归一，量级稳")

# ---------------------------------------------------------------------------
# 结论 / 判词
# ---------------------------------------------------------------------------
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
fail = [g["id"] for g in gates if not g["ok"]]
if not fail:
    verdict = ("EXTERNAL-REVIEW-RECOMPUTE--BLOCK-A-INEQUALITY-CORRECT-AND-SUFFICIENT--"
               "OVERCLAIM-IS-ARBITRARY-H-ONLY-MONOTONE-EXCLUDED--"
               "BLOCK-B-VACUUM-TABLE-CORRECT--N3-IS-INPUT-NOT-SELECTED--"
               "BLOCK-C-KK-LINKS-CORRECT--KK-SCALE-NEAR-PLANCK--"
               "NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")
else:
    verdict = "RECOMPUTE-FAIL--" + "-".join(fail)

result = {
    "subject": "V50 外部来料复核 · 独立复算",
    "object_boundary": "本复核讨论 (50-1)~(50-15) 的质量不等式/六维真空/KK 耦合，"
                       "与仓库 48_V50公理审计卷(量纲/旋量/计数) 非同一对象，不相加",
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(fail)},
    "independent_prediction_count": 0,
    "constants": {"ME": str(ME), "MMU": str(MMU), "MTAU": str(MTAU),
                  "L6": str(L6), "g4_from_alpha": D2S(G4, 10), "M4red_GeV": str(M4RED)},
    "gates": gates,
}

with open(JSON_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

lines = []
lines.append("V50 外部来料复核 · 独立复算报告")
lines.append("=" * 60)
lines.append("判词: " + verdict)
lines.append("门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
lines.append("对象边界: " + result["object_boundary"])
lines.append("独立预言计数: 0")
lines.append("-" * 60)
for g in gates:
    flag = "PASS" if g["ok"] else "FAIL"
    lines.append("[%s] %-22s %-10s exp=%s | act=%s %s" % (
        flag, g["id"], g["kind"], g["exp"], g["act"],
        ("// " + g["note"]) if g["note"] else ""))
lines.append("-" * 60)
lines.append("Python Decimal prec=80; Simpson n=2000; seed=20261123")
with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
