# -*- coding: utf-8 -*-
# Diagnostic (organizer): settle free-phase factor & branch convention between
# original real-phase output and sub-agent A's independent re-derivation.
import numpy as np

def build(cm, dd, SMAX=150.0, Nr=600000):
    roots = np.roots([1.0, 0.0, cm, dd])
    rh = min(x.real for x in roots if abs(x.imag) < 1e-8 and x.real > 0)
    r = np.linspace(rh, SMAX, Nr + 1)
    q = np.sqrt(np.maximum(1 + cm / r**2 + dd / r**3, 0.0))
    dsdr = np.exp(2 / r) * q
    dr = r[1] - r[0]
    s = np.concatenate([[0.0], np.cumsum(0.5 * (dsdr[1:] + dsdr[:-1]) * dr)])
    V = np.exp(-2 / r) * 6 / r**2
    L = s[np.argmin(np.abs(r - 1.0))]
    return rh, s, V, L

def integrate(s, V, w, s_out, DS=0.02):
    n = int(round(s_out / DS))
    sg = np.linspace(0, n * DS, n + 1)
    Vg = np.interp(sg, s, V)
    x, y = 1.0, 0.0
    w2 = w * w
    X = np.array([x, y])
    for k in range(n):
        a1, a2 = w2 - Vg[k], w2 - Vg[k + 1]
        k1 = np.array([X[1], a1 * X[0]])
        u2 = X + 0.5 * DS * k1; k2 = np.array([u2[1], a1 * u2[0]])
        u3 = X + 0.5 * DS * k2; k3 = np.array([u3[1], a1 * u3[0]])
        u4 = X + DS * k3;       k4 = np.array([u4[1], a2 * u4[0]])
        X = X + DS / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return X[0], X[1]

def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi

for tag, (cm, dd) in [("W1 -0.5/0", (-0.5, 0.0)), ("W2 -0.29/-0.05", (-0.29, -0.05))]:
    rh, s, V, L = build(cm, dd)
    print(f"\n=== {tag}: rh={rh:.4f} L={L:.3f} 2L={2*L:.3f}")
    print(f"{'w':>6} {'arg r80':>9} {'arg r120':>9} {'raw diff':>9} {'corr80':>9} {'corr120':>9} {'corr diff':>10}  ||r|-1|80")
    for w in [0.15, 0.30, 0.37, 0.45, 0.60, 0.80, 0.90, 1.00, 1.20]:
        psi80, p80 = integrate(s, V, w, 80.0)
        psi120, p120 = integrate(s, V, w, 120.0)
        r80 = ((psi80 + p80 / (1j * w)) / 2) / ((psi80 - p80 / (1j * w)) / 2)
        r120 = ((psi120 + p120 / (1j * w)) / 2) / ((psi120 - p120 / (1j * w)) / 2)
        a80, a120 = np.angle(r80), np.angle(r120)
        corr80, corr120 = wrap(a80 - 2 * w * 80.0), wrap(a120 - 2 * w * 120.0)
        print(f"{w:6.3f} {a80:9.4f} {a120:9.4f} {a80-a120:9.4f} {corr80:9.4f} {corr120:9.4f} {corr80-corr120:10.4f}  {abs(r80)-1:9.2e}")
