# -*- coding: utf-8 -*-
"""独立探索：离散谱判据的真实代数结构（不做结论，只做机器读数）。

模型族：K(r) = A + B (1 + k r) e^{-k r}
采样：  r_n = r0 + n * dr
D_n = K_{n+1} - K_n
H_n = D_n * D_{n+2} - D_{n+1}^2
问：(a) H_n 是否恒 < 0？(b) H_{n+1}/H_n 是否恒 = q^2 (q = e^{-k dr})？
"""
import sys
from decimal import Decimal as D, getcontext

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60


def build(r0, dr, ell, A=D("1"), B=D("1")):
    r0 = D(str(r0)); dr = D(str(dr)); ell = D(str(ell))
    A = D(str(A)); B = D(str(B))
    k = D(1) / ell
    q = (-(k * dr)).exp()

    def Kn(n):
        r = D(r0) + D(n) * D(dr)
        return A + B * (1 + k * r) * (-(k * r)).exp()

    def Dn(n):
        return Kn(n + 1) - Kn(n)

    def Hn(n):
        return Dn(n) * Dn(n + 2) - Dn(n + 1) ** 2

    return k, q, Kn, Dn, Hn


def closed_form(r0, dr, ell):
    """D_n = C q^n (a + b n)；C = B e^{-k r0}, a = (q-1)(1+k r0) + q k dr, b = (q-1) k dr"""
    r0 = D(str(r0)); dr = D(str(dr)); ell = D(str(ell))
    k = D(1) / ell
    q = (-(k * dr)).exp()
    x0 = k * D(r0)
    dd = k * D(dr)
    C = (-x0).exp()
    a = (q - 1) * (1 + x0) + q * dd
    b = (q - 1) * dd
    return k, q, C, a, b


def show(title, r0, dr, ell, A=D("1"), B=D("1")):
    k, q, Kn, Dn, Hn = build(r0, dr, ell, A, B)
    _, _, C, a, b = closed_form(r0, dr, ell)
    print("==", title, "r0=", r0, "dr=", dr, "ell=", ell, "A=", A, "B=", B)
    print("   q=", q, " q^2=", q * q)
    for n in (0, 1, 2, 3, 4):
        Dn_s = Dn(n)
        Dn_c = C * (q ** n) * (a + b * n)
        Hn_s = Hn(n)
        print("   n=%d  D_samp=%s" % (n, Dn_s))
        print("        D_closed=%s  relerr=%s" % (Dn_c, abs(Dn_s - Dn_c) / abs(Dn_c) if Dn_c != 0 else "n/a"))
        print("        H_samp=%s" % Hn_s)
    for n in (0, 1, 2):
        r1 = Hn(n + 1) / Hn(n) if Hn(n) != 0 else None
        print("   H_%d/H_%d = %s   (q^2=%s)  diff=%s"
              % (n + 1, n, r1, q * q, (abs(r1 - q * q) if r1 is not None else "n/a")))


show("case A: r0=0, dr=50km, ell=124.6km", "0", "50000", "124600")
show("case B: r0=0, dr=20km, ell=90km", "0", "20000", "90000")
show("case C: r0=6371km, dr=50km, ell=124.6km", "6371000", "50000", "124600")
show("case D: r0=0, dr=50km, ell=124.6km, A=0", "0", "50000", "124600", A=D("0"))

# 解析核对：H_n = C^2 q^{2n} [ (1-q)(u^2+2bu) - q b^2 ],  u = a+bn
print()
print("--- 解析式核对 ---")
r0, dr, ell = D("0"), D("50000"), D("124600")
k, q, C, a, b = closed_form(r0, dr, ell)
_, _, Kn, Dn, Hn = build(r0, dr, ell)
for n in (0, 1, 2, 3):
    u = a + b * n
    analytic = (C * C) * (q ** (2 * n)) * ((1 - q) * (u * u + 2 * b * u) - q * b * b)
    print("n=%d  H_samp=%s" % (n, Hn(n)))
    print("     H_analytic=%s  relerr=%s" % (analytic, abs(Hn(n) - analytic) / abs(analytic)))
print("  -(C^2) b^2 q^{2n} (来料式):", [format(-(C * C) * (b * b) * (q ** (2 * n)), ".6E") for n in (0, 1, 2)])
