# -*- coding: utf-8 -*-
import sys
import mpmath as mp
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
mp.mp.dps = 40

c = mp.mpf('299792458')
hbar = mp.mpf('1.054571817e-34')
me = mp.mpf('9.1093837015e-31')
e = mp.mpf('1.602176634e-19')
ae = mp.mpf('1.15965218128e-3')
amu = mp.mpf('1.16592089e-3')

f = lambda r: (1 + 2 * r) / (1 + r) ** 2
g = lambda r: 2 * r * f(r)
fp = lambda r: (1 - r) / (1 + r)

target = 2 * ae
rs = mp.findroot(lambda r: g(r) - target, mp.mpf('0.00116'))
print("r*           =", mp.nstr(rs, 12))
print("g-2(r*)      =", mp.nstr(g(rs), 12), "target =", mp.nstr(target, 12))
print("r_no_shield  =", mp.nstr(target / 2, 12))
print("f(r*)        =", mp.nstr(f(rs), 15), "|f-1| =", mp.nstr(abs(f(rs) - 1), 6))
print("fp(r*)       =", mp.nstr(fp(rs), 15), "|fp-1| =", mp.nstr(abs(fp(rs) - 1), 6))

om = me * c ** 2 / hbar
kap2 = om ** 2 / c ** 2
print("omega_e      =", mp.nstr(om, 8))
print("sqrt(k^2+t^2)=", mp.nstr(mp.sqrt(kap2), 8))
kap = mp.sqrt(kap2 / (1 + rs ** 2))
tau = rs * kap
print("kappa        =", mp.nstr(kap, 8))
print("tau          =", mp.nstr(tau, 8))

d1 = tau * kap * (e * hbar / (me * c)) * fp(rs)
print("d_e raw      =", mp.nstr(d1, 8), "C/m  <-- 非法单位")
cm_per_ecm = mp.mpf('1.602176634e-21')
lam = hbar / (me * c)
print("reduced compton =", mp.nstr(lam, 8), "m")
d2 = d1 * lam ** 2
print("d_e*lam^2    =", mp.nstr(d2, 8), "C m =", mp.nstr(d2 / cm_per_ecm, 8), "e cm")
print("vs ACME 1.1e-29:", mp.nstr(d2 / cm_per_ecm / mp.mpf('1.1e-29'), 8), "倍")
print("文稿声称 1e-57 e cm; 差量级 =", mp.nstr(mp.log10(d2 / cm_per_ecm / mp.mpf('1e-57')), 6))

r0 = mp.mpf('0.00116')
lhs = (1 + r0) * (1 + r0 ** 2)
rhs = (1 + r0) ** 3
print("(1+r)(1+r^2) =", mp.nstr(lhs, 15), "(1+r)^3 =", mp.nstr(rhs, 15), "diff =", mp.nstr(lhs - rhs, 6))

# mu 子：同一几何比能否同时匹配
print("同一 r 给 g-2(mu) =", mp.nstr(g(rs), 10), " 实验 2a_mu =", mp.nstr(2 * amu, 10))
r_mu = mp.findroot(lambda r: g(r) - 2 * amu, mp.mpf('0.00116'))
print("mu 需要的 r   =", mp.nstr(r_mu, 12), "与电子 r* 相对差 =", mp.nstr(abs(r_mu - rs) / rs, 6))

# 346 第一極：f' = 1-2s ?
s = lambda r: r / (1 + r)
print("f'(r) - (1-2s) =", mp.nstr(fp(r0) - (1 - 2 * s(r0)), 8))
print("f(r)  - (1-s^2)=", mp.nstr(f(r0) - (1 - s(r0) ** 2), 8))
print("(1-s)^2        =", mp.nstr((1 - s(r0)) ** 2, 12), " 1-s^2 =", mp.nstr(1 - s(r0) ** 2, 12),
      " 1+s^2 =", mp.nstr(1 + s(r0) ** 2, 12))
