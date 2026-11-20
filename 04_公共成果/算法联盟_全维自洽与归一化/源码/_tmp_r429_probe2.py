# -*- coding: utf-8 -*-
"""只读探针：一次性定清 r429 所有容差与口径（不做结论，只出读数）。"""
import sys, math, random
from decimal import Decimal as D, getcontext

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

G = D("6.67430e-11")
M_E = D("5.9722e24")
GM = D("3.986004418e14")
C_LIGHT = D("299792458")
HBAR = D("1.054571817e-34")
EV_J = D("1.602176634e-19")
R_E = D("6371000")
L_ = D("124600")
ALPHA_Y = D(1) / D(3)
K_ = D(1) / L_
U_ = K_ * R_E
X_ = U_
DR = D("50000")
DELTA = DR / L_
Q = (-DELTA).exp()
EPS0_UNIFORM = D("0.0097749444")
EPS0_IMPROVED = D("0.0059544049")
EPS0_USED = EPS0_IMPROVED
H1H0 = D("0.44817647")
H0A = D("-1.02853e-10")
H0B = D("1.34440e-8")
LP = D("161.165")
DG400 = D("2.217e-3")
DPREC = D("0.04317888")
DNU = D("7.65e-14")
MPHI = D("1.5837e-12")
A_V119 = D("2.5875e9")
L2 = D("300000")
K2 = D(1) / L2
U2 = K2 * R_E

def rel(a, b):
    a = D(str(a)); b = D(str(b))
    if b == 0: return D("Infinity")
    return abs(a - b) / abs(b)

def fs(x, n=10): return format(D(str(x)), ".%dE" % n)

# ---------- 1. eps 剖面与 H_0 三口径 ----------
def eps_profile(r, eps0=EPS0_USED):
    return eps0 * (1 + K_ * r) / (1 + U_) * (-(K_ * (r - R_E))).exp()

def kt(h, eps0=EPS0_USED, shape=1):
    return 1 + shape * eps_profile(R_E + h, eps0)

def d_seq(n, eps0=EPS0_USED):
    return kt(D(n) * DR, eps0) - kt(D(n - 1) * DR, eps0)

def h_seq(n, eps0=EPS0_USED):
    return d_seq(n, eps0) * d_seq(n + 2, eps0) - d_seq(n + 1, eps0) ** 2

C_prof = EPS0_USED / (1 + U_)
b_prof = (Q - 1) * DELTA
h0_prof_closed = -(C_prof ** 2) * (b_prof ** 2) * (Q ** 2)
h0_prof_samp = h_seq(0)
C_pm = ALPHA_Y
h0_pm_closed = -(C_pm ** 2) * (b_prof ** 2) * (Q ** 2)
print("[H0] eps-profile closed =", fs(h0_prof_closed, 12))
print("[H0] eps-profile sample =", fs(h0_prof_samp, 12))
print("[H0] eps-profile rel(samp,closed) =", fs(rel(h0_prof_samp, h0_prof_closed), 5))
print("[H0] v119 H0A =", H0A, " rel =", fs(rel(h0_prof_closed, H0A), 5))
print("[H0] pointmass closed =", fs(h0_pm_closed, 12), " ratio prof/pm =", fs(h0_prof_closed / h0_pm_closed, 8))
print("[H0] C_prof =", fs(C_prof, 12), " b_prof =", fs(b_prof, 12))

# 反解 ell 使 H_0 精确等于来料
def h0_of_ell(ell):
    k = D(1) / ell; q = (-(k * DR)).exp(); u = k * R_E
    c = EPS0_USED / (1 + u); b = (q - 1) * (DR / ell)
    return -(c ** 2) * (b ** 2) * (q ** 2)

lo, hi = D("124000"), D("125200")
for _ in range(300):
    mid = (lo + hi) / 2
    if abs(h0_of_ell(mid) - H0A) > 0:   # h0 随 ell 单调？用符号比较
        pass
    # 手动二分：比较 |h0| 与 |H0A|
    if abs(h0_of_ell(mid)) > abs(H0A):
        hi = mid
    else:
        lo = mid
ell_impl = (lo + hi) / 2
print("[H0] 反解 ell =", fs(ell_impl, 12), " m ; 与 124600 相对差 =", fs(rel(ell_impl, L_), 5))

# ---------- 2. 均匀球双路径 ----------
def eps0_uniform_closed(alpha=ALPHA_Y):
    lead = D(3) * alpha / D(2) * (X_ ** 2 - 1) / X_ ** 3
    extra = D(3) * alpha / D(2) * (X_ + 1) ** 2 * (-(2 * X_)).exp() / X_ ** 3
    return lead, extra

def eps0_uniform_integral(alpha=ALPHA_Y, rho=D("5515")):
    sh = U_.sinh(); ch = U_.cosh()
    I = rho * (R_E * ch / K_ - sh / K_ ** 2)
    mass = D(4) / D(3) * D(str(math.pi)) * rho * R_E ** 3
    return D(4) * D(str(math.pi)) * alpha * (1 + U_) * (-U_).exp() * I / (K_ * mass)

lead, extra = eps0_uniform_closed()
integ = eps0_uniform_integral()
print("[V2] closed =", fs(lead, 12), " integral =", fs(integ, 12), " rel =", fs(rel(lead, integ), 5))
print("[V2] extra =", fs(extra, 6), " vs v119 ", EPS0_UNIFORM, " rel =", fs(rel(lead, EPS0_UNIFORM), 5))
print("[V2] pointmass surface eps =", fs(ALPHA_Y * (1 + K_ * R_E) * (-(K_ * R_E)).exp(), 12))
print("[V2] ratio ext/pm =", fs(rel(lead, ALPHA_Y * (1 + K_ * R_E) * (-(K_ * R_E)).exp()), 5),
      " decades =", fs(D(str(math.log10(abs(lead / (ALPHA_Y * (1 + K_ * R_E) * (-(K_ * R_E)).exp()))))), 6))

# ---------- 3. 分层反解 ----------
def eps0_layered(layers, alpha=ALPHA_Y):
    raw_i = D(0); raw_m = D(0)
    for r0, r1, rho in layers:
        f = lambda r: r * (K_ * r).cosh() / K_ - (K_ * r).sinh() / K_ ** 2
        raw_i += rho * (f(r1) - f(r0))
        raw_m += D(4) / D(3) * D(str(math.pi)) * rho * (r1 ** 3 - r0 ** 3)
    scale = M_E / raw_m
    I = raw_i * scale
    return D(4) * D(str(math.pi)) * alpha * (1 + U_) * (-U_).exp() * I / (K_ * M_E)

RC = D("3480000")
cands = {
    "two-layer(13000/5515)": [(D(0), RC, D("13000")), (RC, R_E, D("5515"))],
    "three-layer(11000/5400/2900)": [(D(0), RC, D("11000")), (RC, R_E - D("35000"), D("5400")), (R_E - D("35000"), R_E, D("2900"))],
    "four-layer(13200/10500/5500/2900)": [(D(0), RC, D("13200")), (RC, D("410000"), D("10500")), (D("410000"), R_E - D("35000"), D("5500")), (R_E - D("35000"), R_E, D("2900"))],
}
for nm, lay in cands.items():
    e = eps0_layered(lay)
    print("[V2-03]", nm, "eps0 =", fs(e, 12), " ratio_to_uniform =", fs(e / lead, 8))
def eps0_core(rho_c):
    return eps0_layered([(D(0), RC, rho_c), (RC, R_E, D("5515"))])
lo, hi = D("8000"), D("40000")
for _ in range(300):
    mid = (lo + hi) / 2
    if eps0_core(mid) > EPS0_IMPROVED: lo = mid
    else: hi = mid
rho_impl = (lo + hi) / 2
print("[V2-03] rho_core implied =", fs(rho_impl, 10), " eps0 =", fs(eps0_core(rho_impl), 12),
      " rel =", fs(rel(eps0_core(rho_impl), EPS0_IMPROVED), 5))

# ---------- 4. 模型 B 翻转 ----------
def dual_eps(h, w2):
    r = R_E + h
    e1 = eps_profile(r, EPS0_USED)
    e2 = EPS0_USED * (1 + K2 * r) / (1 + U2) * (-(K2 * (r - R_E))).exp()
    return (1 - w2) * e1 + w2 * e2

def dual_h(n, w2):
    def dd(m): return dual_eps(D(m) * DR, w2) - dual_eps(D(m - 1) * DR, w2)
    return dd(n) * dd(n + 2) - dd(n + 1) ** 2

flip = None; prev = None
w = D("0.0005")
rows = []
while w <= D("0.30"):
    h0 = dual_h(0, w)
    sg = 1 if h0 > 0 else (-1 if h0 < 0 else 0)
    if prev is not None and sg != 0 and prev != 0 and sg != prev and flip is None:
        flip = w
    if prev is None: prev = sg
    rows.append((w, h0))
    w += D("0.0025")
print("[V1-05] flip_w2 =", fs(flip, 8) if flip is not None else "NONE")
print("[V1-05] h0 at w=0:", fs(rows[0][1], 8), " at w=0.3:", fs(rows[-1][1], 8))
print("[V1-05] pseudo-ell ratio =", fs((-(D(2) * DR / (LP * 1000))).exp() ** 2, 12), " vs q^2 =", fs(Q ** 2, 12))

# ---------- 5. dg / 进动 / 频移 ----------
def dg_extra(r): return GM / r ** 2 * eps_profile(r, EPS0_USED)
def dg_prime(r):
    e = eps_profile(r, EPS0_USED); ep = -EPS0_USED * K_ * K_ * r * (-(K_ * (r - R_E))).exp() / (1 + U_)
    return GM * (ep / r ** 2 - 2 * e / r ** 3)

r400 = R_E + D("400000")
dg4 = dg_extra(r400)
print("[V4] eps(400km) =", fs(eps_profile(r400, EPS0_USED), 12))
print("[V4] dg400 =", fs(dg4, 12), " v119 =", DG400, " rel =", fs(rel(dg4, DG400), 5))

def prec(r, use_dgp=True, exact=True):
    dgp = dg_extra(r); dgpp = dg_prime(r) if use_dgp else D(0)
    wphi2 = GM / r ** 3 + dgp / r
    wr2 = GM / r ** 3 + dgpp + 3 * dgp / r
    if exact: return D(2) * D(str(math.pi)) * (wphi2 / wr2).sqrt() - D(2) * D(str(math.pi))
    return D(str(math.pi)) * (wphi2 - wr2) / wr2

pe = prec(r400, True, True); pl = prec(r400, True, False); pn = prec(r400, False, True)
pf = -r400 * (-EPS0_USED * K_ * K_ * r400 * (-(K_ * (r400 - R_E))).exp() / (1 + U_)) / 2
print("[V4] prec exact =", fs(pe, 12), " rel v119 =", fs(rel(pe, DPREC), 5))
print("[V4] prec linear =", fs(pl, 12), " prec no-dg' =", fs(pn, 12), " prec 1st-order =", fs(pf, 12))

def dU(r): return -GM * eps_profile(r, EPS0_USED) / (r * (1 + r / L_))
dnu = (dU(R_E) - dU(r400)) / (C_LIGHT ** 2)
print("[V5] dnu =", fs(dnu, 12), " v119 =", DNU, " rel =", fs(rel(dnu, DNU), 5))

# ---------- 6. f(R) ----------
A6 = L_ ** 2 / D(6)
AC = D(3) * L_ ** 2 / D(2)
MP = HBAR * C_LIGHT / L_ / EV_J
print("[V3] a(l^2/6) =", fs(A6, 12), " rel v119 =", fs(rel(A6, A_V119), 5))
print("[V3] a(3l^2/2) =", fs(AC, 12), " ratio =", fs(AC / A6, 8))
print("[V3] m_phi c^2 =", fs(MP, 12), " v119 =", MPHI, " rel =", fs(rel(MP, MPHI), 5))

# ---------- 7. 噪声 ----------
def norm_cdf(z): return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
def inv_norm(p):
    lo, hi = 0.0, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)
z1 = D(str(inv_norm(1 - 0.436))); z2 = D(str(inv_norm(1 - 0.049)))
print("[V7] z1 =", fs(z1, 8), " z2 =", fs(z2, 8), " ratio =", fs(z2 / z1, 8))
print("[V7] 12000 次 MC 零翻转 -> z >= ", fs(inv_norm(1 - 3.0/12000.0), 8), " (95%)")

d0 = d_seq(0); d1 = d_seq(1); d2 = d_seq(2)
coef = (2 * (d0 ** 2 + d2 ** 2 + 4 * d1 ** 2)).sqrt()
print("[V7] d0,d1,d2 =", fs(d0, 8), fs(d1, 8), fs(d2, 8))
print("[V7] sigma_H_coef =", fs(coef, 8), " |H0| =", fs(abs(h_seq(0)), 8),
      " sigma_usable =", fs(abs(h_seq(0)) / (coef * D(2)), 6))
print("[V7] H0/sigmaH at 1e-8 =", fs(abs(h_seq(0)) / (D("1e-8") * coef), 6))

def mc_flip(sigma, trials=4000, seed=20261121):
    rnd = random.Random(seed); cnt = 0
    for _ in range(trials):
        v = [kt(D(n) * DR, EPS0_USED) + rnd.gauss(0.0, float(sigma)) for n in range(4)]
        d_0 = v[1]-v[0]; d_1 = v[2]-v[1]; d_2 = v[3]-v[2]
        if d_0*d_2 - d_1*d_1 > 0: cnt += 1
    return cnt, trials
for s in (D("1e-7"), D("1e-8"), D("1e-9"), D("1e-10")):
    c, t = mc_flip(s)
    print("[V7] MC sigma=", fs(s, 2), " ->", c, "/", t)

# ---------- 8. G_inf 口径 ----------
print("[V6] 1/(1+alpha) =", fs(D(1)/(1+ALPHA_Y), 10), " alpha/(1+alpha) =", fs(ALPHA_Y/(1+ALPHA_Y), 10),
      " 1/(1+alpha_eff) =", fs(D(1)/(1+ALPHA_Y/(1+ALPHA_Y)), 10))
print("[V6] eps0 short-range profile =", fs(EPS0_USED/(1+U_), 10))
