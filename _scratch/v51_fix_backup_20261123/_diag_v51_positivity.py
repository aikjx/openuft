# -*- coding: utf-8 -*-
"""Diagnostic: for V51 attack B, recompute all 40 x-samples and report
how many have a negative eigenvalue (non-physical mass-squared matrix),
how many are positive-definite, and how many of the PD ones violate.
Uses sympy exact rationals -> 30-digit evalf. No writes."""
import glob
import os
from sympy import Matrix, Rational, Symbol, Poly

BASE = os.path.dirname(os.path.abspath(__file__))
# locate source constants by reading the attack script text (no execution)
HITS = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_V51攻破_*", "v51_attack_recompute.py"))
assert len(HITS) == 1
src = open(HITS[0], encoding="utf-8").read()
assert 'ME = Decimal("0.51099895")' in src
assert 'MMU = Decimal("105.6583755")' in src
assert 'MTAU = Decimal("1776.86")' in src

me = Rational("0.51099895")
d0 = Rational("1776.86")
d1 = me
d2 = Rational("105.6583755")

pd, nonpd, pd_viol = [], [], []
for k in range(1, 41):
    x = k * me
    M = Matrix([[d0, x, x], [x, d1, x], [x, x, d2]])
    lam = Symbol("lam")
    ev = sorted(float(v) for v in Poly(M.charpoly(lam).as_expr(), lam).nroots(n=30))
    if ev[0] > 0:
        pd.append(k)
        r = ev[1] ** 2 / (4 * ev[0] * ev[2])
        if r > 1:
            pd_viol.append((k, r, ev))
    else:
        nonpd.append((k, ev[0]))

print("total=40 positive_definite=%d non_positive=%d" % (len(pd), len(nonpd)))
print("pd_indices=%s" % pd)
print("nonpd_first=%s" % nonpd[:5])
print("pd_violations=%d" % len(pd_viol))
print("pd_viol_details=%s" % [(k, round(r, 4)) for k, r, _ in pd_viol])
