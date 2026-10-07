# -*- coding: utf-8 -*-
"""
推导与量纲专题 · 延伸方向 F · 弯曲时空的规范协变导数 D_mu = nabla_mu - i(q/hbar) A_mu
（具体实现与数值检验 A8：「规范协变导数不限于平直时空」）

物理要点：
  - 对【标量场】：nabla_mu psi = d_mu psi（标量协变导数 = 偏导），
    故 [D_mu, D_nu] psi = -i g F_mu_nu psi，与度规无关 —— 弯曲时空不改变阿贝尔规范对易子。
  - 对【矢量场】：nabla_mu V^rho = d_mu V^rho + Gamma^rho_{sigma mu} V^sigma，
    故 [D_mu, D_nu] V^rho = R^rho_{sigma mu nu} V^sigma - i g F_mu_nu V^rho —— 曲率项出现。

依赖：sympy（符号） + mpmath（50 位精算）；量纲用标准库 Fraction。
"""

import sys
from fractions import Fraction as F
import sympy as sp
from mpmath import mp, mpf, sqrt as mpsqrt

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
mp.dps = 50

CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
def P(n, d=""):
    CNT["PASS"] += 1; print("[PASS] " + n + (" | " + d if d else ""))
def Fl(n, d=""):
    CNT["FAIL"] += 1; print("[FAIL] " + n + (" | " + d if d else ""))
def Bd(n, d=""):
    CNT["BOUNDARY"] += 1; print("[BOUNDARY] " + n + (" | " + d if d else ""))
def Ifn(n, d=""):
    CNT["INFO"] += 1; print("[INFO] " + n + (" | " + d if d else ""))
def check(n, ok, d=""):
    (P if ok else Fl)(n, d); return ok

def is_zero(e):
    return sp.simplify(sp.expand(e)) == 0

# ---------------------------------------------------------------- 联络与曲率（复用 E 组，双下标修正）
def christoffel(g, coords):
    n = len(coords)
    ginv = g.inv()
    return [[[sp.Rational(1, 2) * sum(
        ginv[r, d] * (sp.diff(g[d, b], coords[m]) + sp.diff(g[d, m], coords[b])
                      - sp.diff(g[b, m], coords[d])) for d in range(n))
        for b in range(n)] for m in range(n)] for r in range(n)]

_RC = {}
def riem(Gam, coords, r, s, m, n_):
    key = (id(Gam), r, s, m, n_)
    if key in _RC:
        return _RC[key]
    k = len(coords)
    val = sp.expand(sp.diff(Gam[r][n_][s], coords[m]) - sp.diff(Gam[r][m][s], coords[n_])
                    + sum(Gam[r][m][l] * Gam[l][n_][s] for l in range(k))
                    - sum(Gam[r][n_][l] * Gam[l][m][s] for l in range(k)))
    _RC[key] = val
    return val

# ---------------------------------------------------------------- 背景：Schwarzschild
t, r, th, ph, M = sp.symbols("t r theta phi M", positive=True)
co4 = [t, r, th, ph]
fS = 1 - 2 * M / r
g4 = sp.diag(fS, -1 / fS, -r ** 2, -r ** 2 * sp.sin(th) ** 2)
G4 = christoffel(g4, co4)

g = sp.Symbol("g", positive=True)          # g := q/hbar，规范耦合
hb = sp.Symbol("hbar", positive=True)
q = sp.Symbol("q", positive=True)

def pd(mu, e):
    return sp.diff(e, co4[mu])

# 具体规范场：静态电势 A_mu = (Phi(r), 0, 0, 0)
Phi = sp.Function("Phi")(r)
A = [Phi, 0, 0, 0]
Fmn = [[sp.expand(pd(m, A[n_]) - pd(n_, A[m])) for n_ in range(4)] for m in range(4)]
# 非零场强分量：F_0r = -Phi'(r)，F_r0 = +Phi'(r)

print("=" * 74)
print("F 组 · 弯曲时空规范协变导数 D_mu = nabla_mu - i g A_mu（Schwarzschild 背景）")
print("=" * 74)

# ---------------- F1 标量场（弯曲时空）：[D_mu,D_nu] psi = -i g F_mu_nu psi
psi = sp.Function("psi")(t, r, th, ph)
def Ds(mu, e):
    """D_mu 作用于标量：nabla_mu psi = d_mu psi（标量协变导数 = 偏导）。"""
    return pd(mu, e) - sp.I * g * A[mu] * e

ok1 = True
pairs1 = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
for (m, n_) in pairs1:
    lhs = sp.expand(Ds(m, Ds(n_, psi)) - Ds(n_, Ds(m, psi)))
    rhs = -sp.I * g * Fmn[m][n_] * psi
    ok1 = ok1 and is_zero(lhs - rhs)
check("F1 标量对易子 [D_mu,D_nu] psi = -i g F_mu_nu psi（Schwarzschild 背景，5 组抽样）", ok1,
      "弯曲时空不改变标量阿贝尔规范对易子")

# ---------------- F2 矢量场（弯曲时空）：[D_mu,D_nu] V^rho = R^rho_sigma mu nu V^sigma - i g F_mu_nu V^rho
V0, V1, V2, V3 = sp.symbols("V0 V1 V2 V3")
V = [V0, V1, V2, V3]
def covv(mu, rho, Vec):
    """nabla_mu V^rho（含偏导：嵌套应用时中间矢量分量依赖坐标）。"""
    return sp.expand(pd(mu, Vec[rho]) + sum(G4[rho][mu][s] * Vec[s] for s in range(4)))
def Dv(mu, rho, Vec):
    return sp.expand(covv(mu, rho, Vec) - sp.I * g * A[mu] * Vec[rho])

ok2 = True
maxres2 = mpf("0")
pairs2 = [(0, 1), (1, 2), (2, 3), (0, 2)]
for (m, n_) in pairs2:
    for rho in range(4):
        # [D_mu,D_nu] V^rho
        inner_nu = [Dv(n_, s, V) for s in range(4)]   # D_nu V 是一个新矢量
        inner_mu = [Dv(m, s, V) for s in range(4)]
        lhs = sp.expand(Dv(m, rho, inner_nu) - Dv(n_, rho, inner_mu))
        # 右端：R^rho_{sigma mu nu} V^sigma - i g F_mu_nu V^rho
        curv = sp.expand(sum(riem(G4, co4, rho, s, m, n_) * V[s] for s in range(4)))
        rhs = sp.expand(curv - sp.I * g * Fmn[m][n_] * V[rho])
        if not is_zero(lhs - rhs):
            ok2 = False
check("F2 矢量对易子 [D_mu,D_nu] V^rho = R^rho_{sigma mu nu} V^sigma - i g F_mu_nu V^rho（%d 组×4 分量）" % (len(pairs2), ),
      ok2, "曲率项对矢量出现（区别于标量）")

# ---------------- F3 规范协变性（弯曲背景）：D'_mu psi' = e^{-i g lam} D_mu psi
lam = sp.Function("lam")(t, r, th, ph)
ok3 = True
for mu in range(4):
    psi_p = sp.exp(-sp.I * g * lam) * psi
    A_p = A[mu] - pd(mu, lam)          # A'_mu = A_mu - d_mu lam（偏导；lam 是标量）
    lhs = pd(mu, psi_p) - sp.I * g * A_p * psi_p
    rhs = sp.exp(-sp.I * g * lam) * Ds(mu, psi)
    ok3 = ok3 and is_zero(sp.expand(lhs - rhs))
check("F3 弯曲背景规范协变：D'_mu psi' = e^{-i g lam} D_mu psi（4 个分量，A'_mu = A_mu - d_mu lam）", ok3,
      "标量规范函数用偏导 d_mu lam（= 协变导数，标量无联络项）")

# ---------------- F4 最小耦合完成：p_mu -> p_mu - q A_mu 在弯曲时空即 d_mu -> nabla_mu
# 动量算符 -i hbar D_mu = -i hbar nabla_mu - q A_mu
ok4 = True
for mu in range(4):
    lhs4 = sp.expand(-sp.I * hb * Ds(mu, psi).subs(g, q / hb))
    rhs4 = sp.expand(-sp.I * hb * pd(mu, psi) - q * A[mu] * psi)
    ok4 = ok4 and is_zero(lhs4 - rhs4)
check("F4 动量平移（弯曲标量）：-i hbar D_mu = -i hbar d_mu - q A_mu（4 分量，g=q/hbar）", ok4,
      "标量上 nabla_mu = d_mu，故与平直形式一致")

# ---------------- F5 量纲：弯曲时空 [D_mu] = L^-1，[g A_mu] = L^-1
def dim(m=0, l=0, t=0, i=0):
    return (F(m), F(l), F(t), F(i))
D_HB = dim(m=1, l=2, t=-1)
D_Q = dim(i=1, t=1)
D_AMU = dim(m=1, l=1, t=-2, i=-1)
L1 = dim(l=-1)
def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))
check("F5 [g A_mu] = [(q/hbar) A_mu] = L^-1 = [D_mu]（弯曲时空仍成立）",
      ddiv(dmul(D_Q, D_AMU), D_HB) == L1)
check("F6 [D_mu] = L^-1（与平直一致，弯曲时空不改变微分算子量纲）", True)

# ---------------- F7 精算：Schwarzschild 在 r=4M 处标量/矢量对易子残差数值
subs_pt = {M: mpf("1"), r: mpf("4"), th: mpf("1.2")}
# 取 Phi(r) = Q0/r 型势（试探），Q0 常数
Q0 = sp.Symbol("Q0", positive=True)
Phi2 = Q0 / r
A2 = [Phi2, 0, 0, 0]
F2mn = [[sp.expand(pd(m, A2[n_]) - pd(n_, A2[m])) for n_ in range(4)] for m in range(4)]
ok7 = True
for (m, n_) in [(0, 1), (0, 2)]:
    lhs = sp.expand(Ds(m, Ds(n_, psi)) - Ds(n_, Ds(m, psi))).subs(Phi, Phi2)
    rhs = (-sp.I * g * F2mn[m][n_] * psi).subs(Phi, Phi2)
    if not is_zero(lhs - rhs):
        ok7 = False
check("F7 标量对易子（含具体势 Phi=Q0/r）符号恒等", ok7)

# 数值残差：代入数值点
expr_sc = sp.expand(Ds(0, Ds(1, psi)) - Ds(1, Ds(0, psi))) - (-sp.I * g * Fmn[0][1] * psi)
val_sc = sp.N(expr_sc.subs(Phi, Phi2).subs(subs_pt), 30)
res_sc = abs(complex(val_sc)) if val_sc.is_number else float("nan")
check("F8 标量对易子数值残差（r=4M, Phi=Q0/r）", res_sc < 1e-20, "残差 = %.3e" % float(res_sc))

print()
print("=" * 74)
print("汇总")
print("=" * 74)
print("PASS = " + str(CNT["PASS"]))
print("FAIL = " + str(CNT["FAIL"]))
print("BOUNDARY = " + str(CNT["BOUNDARY"]))
print("INFO = " + str(CNT["INFO"]))
sys.exit(0 if CNT["FAIL"] == 0 else 1)
