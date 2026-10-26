# -*- coding utf-8 -*-
"""Prototype: r215 numeric feasibility checks (not an audit volume)."""
import math
from decimal import Decimal, getcontext

getcontext().prec = 60

hbar = Decimal("1.054571817e-34")
c = Decimal("2.99792458e8")
hc = hbar * c
alpha = Decimal("7.2973525693e-3")
G = Decimal("6.67430e-11")
m_p = Decimal("1.67262192369e-27")
eV = Decimal("1.602176634e-19")
GeV = Decimal(1e9) * eV
mW = Decimal("80.369") * GeV
mpi0 = Decimal("134.9768e6") * eV

lamW = hc / mW
lamPi = hc / mpi0
print("lamW  =", lamW)
print("lamPi =", lamPi)


def dsqrt(x):
    x = Decimal(x)
    g = Decimal(math.sqrt(float(x)))
    for _ in range(80):
        g = (g + x / g) / 2
    return g


mP = dsqrt(hc / G)
ratio = alpha * (mP / m_p) ** 2
print("mP    =", mP)
print("ratio =", ratio, " (target claims 1.236e36)")

sigma = Decimal("0.18") * GeV / Decimal("1e-15")
print("sigma =", sigma, "N")
alpha_pi = Decimal("14.3")

print("---- overlap: pi-Yukawa vs constant sigma ----")
for fm in ["0.2", "0.5", "1.0", "1.2"]:
    r = Decimal(fm) * Decimal("1e-15")
    Fy = hc * alpha_pi * (1 / (r * r) + 1 / (r * lamPi)) * (-(r / lamPi)).exp()
    print("  r=%s fm: F_pi=%s N ; F_pi/sigma=%.1f" % (fm, "%.4e" % float(Fy), float(abs(Fy) / sigma)))

print("---- power-law fit test (decade window) ----")


def fit_report(n, r0):
    # log-space shape: log[(1/r^2+1/(r*lam)) e^{-r/lam}] = log(1+r/lam) - 2log r - r/lam
    r0f = float(r0)
    rs = [r0f * (10.0 ** (i / 20.0)) for i in range(21)]
    lt = [-n * math.log(r) for r in rs]  # log of C/r^n with C=1
    best = (1e99, None, None)
    for i in range(1201):
        lam = r0f * 10.0 ** (-3 + i * (9.0 / 1200.0))
        lv = [math.log1p(r / lam) - 2 * math.log(r) - r / lam for r in rs]
        alog = sum(lt) / len(lt) - sum(lv) / len(lv)
        resid = [abs(lt[i] - (lv[i] + alog)) for i in range(len(rs))]
        worst = max(resid)
        if worst < best[0]:
            best = (worst, lam, alog)
    rel = math.exp(best[0]) - 1
    return rel, best[1], best[2]


for n in (1, 3, 4, 5):
    rel, lam, A = fit_report(n, "1e-15")
    print("  n=%d : max rel err=%.2f%% lam=%.3e lnA=%.2f" % (n, rel * 100, lam, A))
