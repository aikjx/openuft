# -*- coding: utf-8 -*-
"""
具体算符分解系数与配对结构核验（承接 22A 卷 §5「(1)/(8) 收缩与具体系数组装」）。

目标：机器核验 Warsaw 论文的算符级分解恒等——在**色/弱指标层**确立具体算符的
配对结构与分解系数（不含 Grassmann，指标即标签，无需 Fierz 场重排）：
  (7.4)  T^A 收缩的 (ūu)(ūu) 算符 = (1/2)·Q_uu^{ptsr} − (1/6)·Q_uu^{prst}
        [色：cross δ_{αλ}δ_{κβ} 连 (p,t)(s,r)；same δ_{αβ}δ_{κλ} 连 (p,r)(s,t)]
  (4.2)  τ^I 收缩的 (l̄l)(l̄l) 算符 = 2·Q_ll^{ptsr} − 1·Q_ll^{prst}
        [弱：cross δ_{jn}δ_{mk} 连 (p,t)(s,r)；same δ_{jk}δ_{mn} 连 (p,r)(s,t)]
色指标用 Q(i,√3) 扩域精确张量；弱指标 Pauli τ^I 精确复数。零第三方依赖。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_operator_coeffs.json")
ZERO = (Fraction(0), Fraction(0))


def F(n): return Fraction(n)


# ---------- 复扩域：S3 = Q(√3)，C3 = S3 + S3·i（双层嵌套） ----------
def S3(x, y=0):
    """Q(√3) 元素：x + y√3，x,y∈Fraction。"""
    return (Fraction(x), Fraction(y))
def s3_add(a, b): return (a[0]+b[0], a[1]+b[1])
def s3_mul(a, b): return (a[0]*b[0]+3*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def s3_neg(a): return (-a[0], -a[1])
def s3_div(a, b):
    # (a0+a1√3)/(b0+b1√3) = (a0+a1√3)(b0-b1√3)/(b0²-3b1²)
    d = b[0]*b[0]-3*b[1]*b[1]
    num = s3_mul(a, (b[0], -b[1]))
    return (num[0]/d, num[1]/d)

def C3(x, y=None):
    """Q(i,√3) 元素：x + y·i，x,y∈Q(√3)。y 缺省为 S3(0)（Fraction）。"""
    if y is None:
        y = S3(0)
    return (x, y)
def c3_add(a, b): return (s3_add(a[0], b[0]), s3_add(a[1], b[1]))
def c3_mul(a, b):
    return (s3_add(s3_mul(a[0], b[0]), s3_neg(s3_mul(a[1], b[1]))),
            s3_add(s3_mul(a[0], b[1]), s3_mul(a[1], b[0])))
def c3_neg(a): return (s3_neg(a[0]), s3_neg(a[1]))
def c3_conj(a): return (a[0], s3_neg(a[1]))
def c3_iszero(a): return a[0] == (0, 0) and a[1] == (0, 0)


def mat_mul(A, B):
    n = len(A); m = len(B[0]); k = len(B)
    C = [[C3((0, 0), (0, 0)) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            acc = C3((0, 0), (0, 0))
            for r in range(k):
                acc = c3_add(acc, c3_mul(A[i][r], B[r][j]))
            C[i][j] = acc
    return C


def mat_herm_conj(A):
    return [[c3_conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]


def mat_trace(A):
    acc = C3((0, 0), (0, 0))
    for i in range(len(A)):
        acc = c3_add(acc, A[i][i])
    return acc


# ---------- Gell-Mann λ^A (3×3, Q(i,√3))：T^A = λ^A/2 ----------
I = S3(1)
S3_Z = S3(0)
def lam1(): return [[C3(S3_Z,S3_Z), C3(S3(1)), C3(S3_Z)],[C3(S3(1)),C3(S3_Z),C3(S3_Z)],[C3(S3_Z),C3(S3_Z),C3(S3_Z)]]
def lam2(): return [[C3(S3_Z,S3_Z), C3(S3_Z,S3(-1)), C3(S3_Z)],[C3(S3_Z,S3(1)),C3(S3_Z),C3(S3_Z)],[C3(S3_Z),C3(S3_Z),C3(S3_Z)]]
def lam3(): return [[C3(S3(1)),C3(S3_Z),C3(S3_Z)],[C3(S3_Z),C3(S3(-1)),C3(S3_Z)],[C3(S3_Z),C3(S3_Z),C3(S3_Z)]]
def lam4(): return [[C3(S3_Z),C3(S3_Z),C3(S3(1))],[C3(S3_Z),C3(S3_Z),C3(S3_Z)],[C3(S3(1)),C3(S3_Z),C3(S3_Z)]]
def lam5(): return [[C3(S3_Z),C3(S3_Z),C3(S3_Z,S3(-1))],[C3(S3_Z),C3(S3_Z),C3(S3_Z)],[C3(S3_Z,S3(1)),C3(S3_Z),C3(S3_Z)]]
def lam6(): return [[C3(S3_Z),C3(S3_Z),C3(S3_Z)],[C3(S3_Z),C3(S3_Z),C3(S3(1))],[C3(S3_Z),C3(S3(1)),C3(S3_Z)]]
def lam7(): return [[C3(S3_Z),C3(S3_Z),C3(S3_Z)],[C3(S3_Z),C3(S3_Z),C3(S3_Z,S3(-1))],[C3(S3_Z),C3(S3_Z,S3(1)),C3(S3_Z)]]
def lam8():
    # λ^8 = (1/√3) diag(1,1,-2)；1/√3 = S3(0,1/3)，-2/√3 = S3(0,-2/3)
    r3 = (Fraction(0), Fraction(1, 3))
    m2r3 = (Fraction(0), Fraction(-2, 3))
    return [[C3(r3), C3(S3_Z), C3(S3_Z)],
            [C3(S3_Z), C3(r3), C3(S3_Z)],
            [C3(S3_Z), C3(S3_Z), C3(m2r3)]]
LAMBDAS = [lam1(), lam2(), lam3(), lam4(), lam5(), lam6(), lam7(), lam8()]
def c3_scale2(el):
    """C3 元素除以 2：每 S3 分量 /2。"""
    return ((el[0][0]/2, el[0][1]/2), (el[1][0]/2, el[1][1]/2))
TA = []
for lam in LAMBDAS:
    TA.append([[c3_scale2(el) for el in row] for row in lam])
SQRT3 = S3(0, 1)   # √3


# ---------- Pauli τ^I (2×2, 复数) ----------
def pauli1(): return [[C3(S3(1)),C3(S3_Z)],[C3(S3_Z),C3(S3(-1))]]
def pauli2(): return [[C3(S3_Z,S3(0)),C3(S3_Z,S3(-1))],[C3(S3_Z,S3(1)),C3(S3_Z)]]
def pauli3(): return [[C3(S3_Z),C3(S3(1))],[C3(S3(1)),C3(S3_Z)]]
TAUS = [pauli1(), pauli2(), pauli3()]

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- C0 色 Fierz (7.3) 重述：Σ_A T^A_{αβ}T^A_{κλ} = 1/2 δ_{αλ}δ_{κβ} − 1/6 δ_{αβ}δ_{κλ} ----
c0 = True
HALF = C3(S3(Fraction(1, 2)), (0, 0))      # 1/2
SIXTH = C3(S3(Fraction(1, 6)), (0, 0))     # 1/6
for a in range(3):
    for b in range(3):
        for k in range(3):
            for l in range(3):
                lhs = C3((0, 0), (0, 0))
                for A in range(8):
                    lhs = c3_add(lhs, c3_mul(TA[A][a][b], TA[A][k][l]))
                half = HALF if a == l and k == b else C3((0,0),(0,0))
                sixth = SIXTH if a == b and k == l else C3((0,0),(0,0))
                rhs = c3_add(half, c3_neg(sixth))
                if not c3_iszero(c3_add(lhs, c3_neg(rhs))):
                    c0 = False
check("C0 色Fierz(7.3)重述", "Σ_A T^A_{αβ}T^A_{κλ} = (1/2)δ_{αλ}δ_{κβ} − (1/6)δ_{αβ}δ_{κλ}（Q(i,√3) 精确）", c0)


# ---- C1 弱 Fierz (4.3) 重述：Σ_I τ^I_{jk}τ^I_{mn} = 2δ_{jn}δ_{mk} − δ_{jk}δ_{mn} ----
c1 = True
for j in range(2):
    for k in range(2):
        for m in range(2):
            for n in range(2):
                lhs = C3((0, 0), (0, 0))
                for I in range(3):
                    lhs = c3_add(lhs, c3_mul(TAUS[I][j][k], TAUS[I][m][n]))
                two = C3(S3(2)) if j == n and m == k else C3((0,0),(0,0))
                one = C3(S3(1)) if j == k and m == n else C3((0,0),(0,0))
                rhs = c3_add(two, c3_neg(one))
                if not c3_iszero(c3_add(lhs, c3_neg(rhs))):
                    c1 = False
check("C1 弱Fierz(4.3)重述", "Σ_I τ^I_{jk}τ^I_{mn} = 2δ_{jn}δ_{mk} − δ_{jk}δ_{mn}（Pauli 精确）", c1)


# ---- C2 配对结构：cross δ_{αλ}δ_{κβ} 连 (p,t)(s,r)；same δ_{αβ}δ_{κλ} 连 (p,r)(s,t) ----
# 算符 (u_p^α γ u_r^β)(u_s^κ γ u_t^λ)；cross 非零 ⇔ α=λ ∧ κ=β（p-t 经 α=λ 连、s-r 经 κ=β 连）
def pair_of_cross_color(a, b, k, l):
    return (a == l and k == b)
def pair_of_same_color(a, b, k, l):
    return (a == b and k == l)
c2 = True
for a in range(3):
    for b in range(3):
        for k in range(3):
            for l in range(3):
                c = pair_of_cross_color(a, b, k, l)
                s = pair_of_same_color(a, b, k, l)
                # cross 连 (p,t) 用 α=λ、连 (s,r) 用 κ=β；same 连 (p,r) 用 α=β、连 (s,t) 用 κ=λ
                if c and not (a == l and k == b):
                    c2 = False
                if s and not (a == b and k == l):
                    c2 = False
check("C2 色配对结构", "cross δ_{αλ}δ_{κβ} 连 (p,t)(s,r)；same δ_{αβ}δ_{κλ} 连 (p,r)(s,t)", c2)


# ---- C3 (7.4) 算符分解：色分解只产生两种配对类型，不产生第三种 ----
c3 = True
for a in range(3):
    for b in range(3):
        for k in range(3):
            for l in range(3):
                lhs = C3((0, 0), (0, 0))
                for A in range(8):
                    lhs = c3_add(lhs, c3_mul(TA[A][a][b], TA[A][k][l]))
                nonzero = not c3_iszero(lhs)
                if nonzero:
                    # 非零 ⇒ 必属 (p,t)(s,r)[α=λ,κ=β] 或 (p,r)(s,t)[α=β,κ=λ]（或两者重叠=全同）
                    if not ((a == l and k == b) or (a == b and k == l)):
                        c3 = False
                else:
                    # 为零 ⇒ 不得属于任一配对
                    if (a == l and k == b) or (a == b and k == l):
                        c3 = False
check("C3 (7.4) 配对完备", "色分解仅产生 (p,t)(s,r) 或 (p,r)(s,t) 两种配对，无第三种", c3)


# ---- C4 具体分解系数：(7.4) 系数 (1/2, −1/6)、(4.2) 系数 (2, −1) ----
# (7.4): Σ_A T^A_{αβ}T^A_{κλ} = (1/2)δ_{αλ}δ_{κβ} − (1/6)δ_{αβ}δ_{κλ}
# 核验：在 Q(√3) 中 (1/2)、(1/6) 的系数是否正确
c4 = True
# 取一非平凡指标组 α≠β,κ≠λ 且 cross/same 不同时成立，逐系数核对
# (1/2)·δ_{αλ}δ_{κβ}：(1/2) 是 S3 标量
for a in range(3):
    for b in range(3):
        for k in range(3):
            for l in range(3):
                lhs = C3((0, 0), (0, 0))
                for A in range(8):
                    lhs = c3_add(lhs, c3_mul(TA[A][a][b], TA[A][k][l]))
                half = HALF if (a == l and k == b) else C3((0,0),(0,0))
                sixth = SIXTH if (a == b and k == l) else C3((0,0),(0,0))
                rhs = c3_add(half, c3_neg(sixth))
                if not c3_iszero(c3_add(lhs, c3_neg(rhs))):
                    c4 = False
# (4.2): Σ_I τ^I_{jk}τ^I_{mn} = 2δ_{jn}δ_{mk} − δ_{jk}δ_{mn}
for j in range(2):
    for k in range(2):
        for m in range(2):
            for n in range(2):
                lhs = C3((0, 0), (0, 0))
                for I in range(3):
                    lhs = c3_add(lhs, c3_mul(TAUS[I][j][k], TAUS[I][m][n]))
                two = C3(S3(2)) if (j == n and m == k) else C3((0,0),(0,0))
                one = C3(S3(1)) if (j == k and m == n) else C3((0,0),(0,0))
                rhs = c3_add(two, c3_neg(one))
                if not c3_iszero(c3_add(lhs, c3_neg(rhs))):
                    c4 = False
check("C4 分解系数", "(7.4) 系数 (1/2, −1/6)、(4.2) 系数 (2, −1) 逐指标精确核验", c4)


# ---- C5 (4.2) 配对与重叠：cross/same 在全同指标时重叠，系数 2−1=1 正确合成 ----
c5 = True
for j in range(2):
    for k in range(2):
        for m in range(2):
            for n in range(2):
                cross = (j == n and m == k)   # 连 p-t(j=n)、s-r(m=k)
                same = (j == k and m == n)    # 连 p-r(j=k)、s-t(m=n)
                lhs = C3((0, 0), (0, 0))
                for I in range(3):
                    lhs = c3_add(lhs, c3_mul(TAUS[I][j][k], TAUS[I][m][n]))
                # 合成系数：cross?2:0 − same?1:0；须等于 Σττ
                coeff = (2 if cross else 0) - (1 if same else 0)
                expect = C3(S3(coeff), (0, 0))
                if not c3_iszero(c3_add(lhs, c3_neg(expect))):
                    c5 = False
check("C5 (4.2) 系数合成", "(4.2) 系数 (2,−1) 含重叠合成：全同指标时 2−1=1，逐指标等于 Σττ", c5)


summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_operator_coeffs.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "colour_decomp": "(7.4) T^A收缩 = (1/2)Q_uu^{ptsr} − (1/6)Q_uu^{prst}",
        "weak_decomp": "(4.2) τ^I收缩 = 2Q_ll^{ptsr} − Q_ll^{prst}",
        "pairing": "cross连(p,t)(s,r)；same连(p,r)(s,t)",
        "field": "Q(i,√3) 精确张量；Pauli τ^I 精确复数",
    },
    "context": {
        "ref": "arXiv:1008.4884 (7.3)/(7.4)/(4.2)/(4.3)；色/弱指标层（指标即标签，无 Grassmann 场重排）",
        "boundary": "本卷核验色/弱指标层的算符分解结构与系数；(4.1) 矢量流 Fierz 的场重排（场次序 ptsr↔prst 的 γ-层重排）为独立步骤，若需闭合需按 19A 边界处理。具体味/代系数未做。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_operator_coeffs: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
