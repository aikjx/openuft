# -*- coding: utf-8 -*-
"""
Warsaw 色/弱群指标 Fierz 恒等的机器核验（群指标展开层，承接 19A 卷 §5 点名）。

背景：
  19A 卷把 J_5^2 四费米算符匹配到 Warsaw 四费米类（类级，13/13 PASS）。本卷补其
  「群指标展开」的代数内核：核验 Warsaw 论文(arXiv:1008.4884)用于约化四费米算符的
  色 Fierz 恒等式与弱指标 Fierz 恒等式：
    (7.3):  T^A_{αβ}T^A_{κλ} = (1/2)δ_{αλ}δ_{κβ} - (1/6)δ_{αβ}δ_{κλ}
    (4.3):  τ^I_{jk}τ^I_{mn} = 2δ_{jn}δ_{mk} - δ_{jk}δ_{mn}
  以及 λ^A 版本（λ=2T, Tr λ^Aλ^B=2δ^AB）。

约定：零第三方依赖；复扩域 Q(i,√3)（元素 x+y·i，x,y∈Q(√3)，i²=-1, √3²=3）。
色为 SU(3)，T^A=λ^A/2（Gell-Mann）；弱为 SU(2)，τ^I=Pauli。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_colour_fierz.json")


class S3:
    """Q(√3) 扩展域数：a + b√3，a,b 为 Fraction。"""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a) if not isinstance(a, Fraction) else a
        self.b = Fraction(b) if not isinstance(b, Fraction) else b

    def __add__(self, o):
        o = o if isinstance(o, S3) else S3(o)
        return S3(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        o = o if isinstance(o, S3) else S3(o)
        return S3(self.a - o.a, self.b - o.b)

    def __neg__(self):
        return S3(-self.a, -self.b)

    def __mul__(self, o):
        if isinstance(o, S3):
            return S3(self.a * o.a + 3 * self.b * o.b,
                      self.a * o.b + self.b * o.a)
        return S3(self.a * o, self.b * o)

    def __truediv__(self, o):
        if isinstance(o, S3):
            d = o.a * o.a - 3 * o.b * o.b      # 范数（√3²=3）
            return S3((self.a * o.a - 3 * self.b * o.b) / d,
                      (self.b * o.a - self.a * o.b) / d)
        return S3(self.a / o, self.b / o)

    def __eq__(self, o):
        o = o if isinstance(o, S3) else S3(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        if self.b == 0:
            return f"{self.a}"
        if self.a == 0:
            return f"({self.b})√3"
        return f"{self.a}+({self.b})√3"


class C3:
    """Q(i,√3) 复扩域：x + y·i，x,y∈Q(√3)，i²=-1。"""
    __slots__ = ("x", "y")

    def __init__(self, x=0, y=0):
        self.x = x if isinstance(x, S3) else S3(x)
        self.y = y if isinstance(y, S3) else S3(y)

    def __add__(self, o):
        o = o if isinstance(o, C3) else C3(o)
        return C3(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        o = o if isinstance(o, C3) else C3(o)
        return C3(self.x - o.x, self.y - o.y)

    def __neg__(self):
        return C3(-self.x, -self.y)

    def __mul__(self, o):
        if isinstance(o, C3):
            return C3(self.x * o.x - self.y * o.y, self.x * o.y + self.y * o.x)
        return C3(self.x * o, self.y * o)

    def __truediv__(self, o):
        if isinstance(o, C3):
            # (x+y·i)/(u+v·i)，共轭乘 (u-v·i)/(u²+v²)
            d = o.x * o.x + o.y * o.y
            return C3((self.x * o.x + self.y * o.y) / d,
                      (self.y * o.x - self.x * o.y) / d)
        return C3(self.x / o, self.y / o)

    def __eq__(self, o):
        o = o if isinstance(o, C3) else C3(o)
        return self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        if self.y == S3(0):
            return f"{self.x}"
        if self.x == S3(0):
            return f"{self.y}·i"
        return f"{self.x}+{self.y}·i"


Z = C3(S3(0), S3(0))
ONE = C3(S3(1), S3(0))
II = C3(S3(0), S3(1))          # 虚数单位 i
SQRT3 = C3(S3(0, 1), S3(0))    # √3（实，Q(√3) 的 b 分量）


def mmul(A, B):
    n = len(A)
    C = [[Z for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
    return C


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]


def mscale(s, A):
    return [[A[i][j] * s for j in range(len(A))] for i in range(len(A))]


def mtrans(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A))]


def mconj(A):
    return [[C3(A[i][j].x, -A[i][j].y) for j in range(len(A))] for i in range(len(A))]


def mtrace(A):
    s = Z
    for i in range(len(A)):
        s = s + A[i][i]
    return s


# ---- Gell-Mann λ^A（3×3，元为 Q(i,√3)）----
def r0(): return C3(S3(0), S3(0))
def r1(): return C3(S3(1), S3(0))
def rn1(): return C3(S3(-1), S3(0))
def ri(): return C3(S3(0), S3(1))
def rni(): return C3(S3(0), S3(-1))
def r_sqrt3_over3(): return C3(S3(0, Fraction(1, 3)), S3(0))   # √3/3 = 1/√3


def l1():
    return [[r0(), r1(), r0()], [r1(), r0(), r0()], [r0(), r0(), r0()]]
def l2():
    return [[r0(), rni(), r0()], [ri(), r0(), r0()], [r0(), r0(), r0()]]
def l3():
    return [[r1(), r0(), r0()], [r0(), rn1(), r0()], [r0(), r0(), r0()]]
def l4():
    return [[r0(), r0(), r1()], [r0(), r0(), r0()], [r1(), r0(), r0()]]
def l5():
    return [[r0(), r0(), rni()], [r0(), r0(), r0()], [ri(), r0(), r0()]]
def l6():
    return [[r0(), r0(), r0()], [r0(), r0(), r1()], [r0(), r1(), r0()]]
def l7():
    return [[r0(), r0(), r0()], [r0(), r0(), rni()], [r0(), ri(), r0()]]
def l8():
    s = r_sqrt3_over3()
    return [[s, r0(), r0()], [r0(), s, r0()], [r0(), r0(), s * S3(-2)]]


LAMBDAS = [l1(), l2(), l3(), l4(), l5(), l6(), l7(), l8()]
TAUS = [[[x / 2 for x in row] for row in mat] for mat in LAMBDAS]   # T^A = λ^A/2


def is_scalar_zero(c):
    return c.x == S3(0) and c.y == S3(0)


def id3(a, b):
    return ONE if a == b else Z


RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- C0 λ 无迹且厄米 ----
traceless = all(is_scalar_zero(mtrace(L)) for L in LAMBDAS)
herm = all(mconj(L) == mtrans(L) for L in LAMBDAS)
check("C0 λ 无迹且厄米", "Gell-Mann λ^A 无迹且厄米（Q(i,√3) 精确）", traceless and herm)

# ---- C1 Tr(λ^Aλ^B)=2δ^AB ----
norm_ok = True
for A in range(8):
    for B in range(8):
        t = mtrace(mmul(LAMBDAS[A], LAMBDAS[B]))
        want = C3(S3(2)) if A == B else Z
        if t != want:
            norm_ok = False
check("C1 Tr(λ^Aλ^B)=2δ^AB", "λ 生成元归一化 Tr λ^Aλ^B = 2δ^AB（SU(3) 基础表示）", norm_ok)

# ---- C2 λ 版本色 Fierz: Σ_A λ^A_{αβ}λ^A_{κλ} = 2δ_{αλ}δ_{κβ} - (2/3)δ_{αβ}δ_{κλ} ----
c2_ok = True
for a in range(3):
    for b in range(3):
        for k in range(3):
            for l in range(3):
                s = Z
                for A in range(8):
                    s = s + LAMBDAS[A][a][b] * LAMBDAS[A][k][l]
                want = C3(S3(2)) * id3(a, l) * id3(k, b) - C3(S3(Fraction(2, 3))) * id3(a, b) * id3(k, l)
                if s != want:
                    c2_ok = False
check("C2 λ 色Fierz", "Σ_A λ^A_{αβ}λ^A_{κλ} = 2δ_{αλ}δ_{κβ} - (2/3)δ_{αβ}δ_{κλ}", c2_ok)

# ---- C3 T 版本（论文 (7.3)）: Σ_A T^A_{αβ}T^A_{κλ} = (1/2)δ_{αλ}δ_{κβ} - (1/6)δ_{αβ}δ_{κλ} ----
c3_ok = True
for a in range(3):
    for b in range(3):
        for k in range(3):
            for l in range(3):
                s = Z
                for A in range(8):
                    s = s + TAUS[A][a][b] * TAUS[A][k][l]
                want = C3(S3(Fraction(1, 2))) * id3(a, l) * id3(k, b) \
                       - C3(S3(Fraction(1, 6))) * id3(a, b) * id3(k, l)
                if s != want:
                    c3_ok = False
check("C3 T 色Fierz (7.3)", "Σ_A T^A_{αβ}T^A_{κλ} = (1/2)δ_{αλ}δ_{κβ} - (1/6)δ_{αβ}δ_{κλ}（论文(7.3)）", c3_ok)

# ---- C4 弱指标 (4.3): Σ_I τ^I_{jk}τ^I_{mn} = 2δ_{jn}δ_{mk} - δ_{jk}δ_{mn} ----
TAU = [
    [[r0(), r1()], [r1(), r0()]],
    [[r0(), rni()], [ri(), r0()]],
    [[r1(), r0()], [r0(), rn1()]],
]
c4_ok = True
for j in range(2):
    for k in range(2):
        for m in range(2):
            for n in range(2):
                s = Z
                for I in range(3):
                    s = s + TAU[I][j][k] * TAU[I][m][n]
                want = C3(S3(2)) * id3(j, n) * id3(m, k) - id3(j, k) * id3(m, n)
                if s != want:
                    c4_ok = False
check("C4 τ 弱Fierz (4.3)", "Σ_I τ^I_{jk}τ^I_{mn} = 2δ_{jn}δ_{mk} - δ_{jk}δ_{mn}（论文(4.3)）", c4_ok)

# ---- C5 由 (7.3) 推 (7.4) 色分解（Q_uu 型） ----
# (ū_pγ_μT^A u_r)(ū_sT^Aγ^μu_t): 色收缩张量 F_{αβκλ}=Σ_A T^A_{αβ}T^A_{κλ}
# 由 (7.3): = (1/2)δ_{αλ}δ_{κβ}(交叉=Q_uu^{ptsr}) - (1/6)δ_{αβ}δ_{κλ}(同色=Q_uu^{prst})
c5_ok = True
for a in range(3):
    for b in range(3):
        for k in range(3):
            for l in range(3):
                s = Z
                for A in range(8):
                    s = s + TAUS[A][a][b] * TAUS[A][k][l]
                cross = id3(a, l) * id3(k, b)
                same = id3(a, b) * id3(k, l)
                want = C3(S3(Fraction(1, 2))) * cross - C3(S3(Fraction(1, 6))) * same
                if s != want:
                    c5_ok = False
check("C5 (7.4) 色分解", "色收缩 T^A_{αβ}T^A_{κλ} 分解 = (1/2)交叉(Q_uu^{ptsr}) - (1/6)同色(Q_uu^{prst})，指标层与 (7.3) 一致", c5_ok)

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_colour_fierz.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "field": "Q(i,√3)：λ^8=(1/√3)diag(1,1,-2)，T^A=λ^A/2",
        "gellmann_normalisation": "Tr λ^Aλ^B = 2δ^AB (SU(3) 基础表示)",
        "colour_fierz_T": "Σ_A T^A_{αβ}T^A_{κλ} = (1/2)δ_{αλ}δ_{κβ} - (1/6)δ_{αβ}δ_{κλ}  (7.3)",
        "weak_fierz_tau": "Σ_I τ^I_{jk}τ^I_{mn} = 2δ_{jn}δ_{mk} - δ_{jk}δ_{mn}  (4.3)",
        "quu_decomp": "T^A 收缩 → (1/2)Q_uu^{ptsr} - (1/6)Q_uu^{prst}",
    },
    "context": {
        "ref": "arXiv:1008.4884 Eqs.(7.3)-(7.7),(4.3)",
        "boundary": "本卷核验群指标 Fierz 恒等的代数内核；(7.4)-(7.7) 的完整算符级推导还涉及矢量流 Fierz 场重排(4.1)与 Grassmann 符号，未在本卷重演——与 18A 卷「Fierz 是算符级恒等」的结论一致。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_colour_fierz: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
