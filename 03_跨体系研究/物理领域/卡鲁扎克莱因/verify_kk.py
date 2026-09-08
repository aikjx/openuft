# -*- coding: utf-8 -*-
"""
verify_kk.py —— Kaluza-Klein 约化符号验证（5 维 -> 4 维）
验证目标：KK ansatz  ds^2 = g_munu dx^mu dx^nu + phi (dy + A_mu dx^mu)^2
的 5 维 Ricci 标量 R5 精确约化为：
    R5 = R4 - (1/4) phi F_munu F^{munu} + (1/2)(∂phi)^2/phi^2 - (1/phi) box_4 phi
即证明：5 维纯引力 = 4 维引力 + U(1) 规范场 + dilaton 标量场。
分三阶段：
  S1 标量场区段（A=0，g4=FLRW，phi=phi(t)）→ 锁定 dilaton 项系数
  S2 规范场区段（g4=Minkowski，phi=常数，A 非零分量）→ 验证 -(phi/4)F^2
  S3 全耦合（g4=Minkowski，phi、A 均非平凡）→ 验证无交叉项、系数一致
"""
import sympy as sp
import numpy as np
from gr_toolkit import christoffel, ricci_tensor, ricci_scalar

# =====================================================================
# S1：标量场区段 —— 5 维 diag(-1, a^2, a^2, a^2, phi(t))
# =====================================================================
print("=" * 72)
print("S1：5 维 diag(-1, a(t)^2, a(t)^2, a(t)^2, phi(t)) —— dilaton 区段")
t = sp.symbols('t')
a = sp.Function('a')(t)
ph = sp.Function('phi')(t)
x5 = [t, x, y, z, w] = [t, sp.symbols('x'), sp.symbols('y'), sp.symbols('z'), sp.symbols('w')]
g5 = sp.Matrix(sp.diag(-1, a**2, a**2, a**2, ph))
gi5 = g5.inv()
G5 = christoffel(x5, g5, gi5)
Ric5 = ricci_tensor(x5, g5, gi5, G5)
R5 = ricci_scalar(x5, g5, gi5, Ric5)

g4 = sp.Matrix(sp.diag(-1, a**2, a**2, a**2))
gi4 = g4.inv()
G4 = christoffel(x5[:4], g4, gi4)
Ric4 = ricci_tensor(x5[:4], g4, gi4, G4)
R4 = ricci_scalar(x5[:4], g4, gi4, Ric4)
box4 = -(sp.diff(ph, t, 2) + 3 * sp.diff(a, t) * sp.diff(ph, t) / a)
dphi2 = -sp.diff(ph, t)**2

Fdiff = sp.simplify(R5 - R4)

A, B, C, F, G, H = sp.symbols('A B C F G H')
sub = {a: A, sp.diff(a, t): B, sp.diff(a, t, 2): C,
       ph: F, sp.diff(ph, t): G, sp.diff(ph, t, 2): H}
F_expr = sp.expand(Fdiff.subs(sub))
B1 = sp.simplify(box4.subs(sub) / F)
B2 = sp.simplify(dphi2.subs(sub) / F**2)

pts = [(2, 1, 3, 5, 4, 7), (3, 2, 5, 7, 6, 1), (5, 1, 2, 11, 3, 13), (1, 3, 2, 2, 5, 4)]
M = np.zeros((len(pts), 2)); rhs = np.zeros(len(pts))
for i, (a0, b0, c0, f0, g0, h0) in enumerate(pts):
    val = dict(zip([A, B, C, F, G, H], [a0, b0, c0, f0, g0, h0]))
    M[i, 0] = float(B1.subs(val)); M[i, 1] = float(B2.subs(val))
    rhs[i] = float(F_expr.subs(val))
c1, c2 = np.linalg.lstsq(M, rhs, rcond=None)[0]
resid = M @ np.array([c1, c2]) - rhs
print("拟合 dilaton 项系数：c1 =", repr(c1), " c2 =", repr(c2), " 残差max =",
      np.max(np.abs(resid)))

# 高精度复核系数
import mpmath as mp
mp.mp.dps = 40
pts_hi = [(7, 5, 11, 13, 8, 3), (2, 7, 3, 5, 11, 6)]
for (a0, b0, c0, f0, g0, h0) in pts_hi:
    val = {A: mp.mpf(a0), B: mp.mpf(b0), C: mp.mpf(c0), F: mp.mpf(f0),
           G: mp.mpf(g0), H: mp.mpf(h0)}
    lhs_hi = sp.expand(F_expr).subs(val)
    rhs_hi = c1 * sp.expand(B1).subs(val) + c2 * sp.expand(B2).subs(val)
    print("高精度残差 @", (a0, b0, c0, f0, g0, h0), "=", abs(float(lhs_hi) - float(rhs_hi)))

print("→ S1 结论：R5 = R4 + c1·(box_4 phi)/phi + c2·(∂phi)^2/phi^2，c1=%.4f, c2=%.4f"
      % (c1, c2))

# =====================================================================
# S2：规范场区段 —— g4 = Minkowski, phi = 常数, A=(0, A1, A2, 0)
# =====================================================================
print("=" * 72)
print("S2：g4=Minkowski，phi=const，A=(0,A1,A2,0) —— 规范场区段")
T, X, Y, Z = sp.symbols('T X Y Z')
x5b = [T, X, Y, Z, W] = [T, X, Y, Z, sp.symbols('W')]
phi0 = sp.symbols('phi0')
A1 = sp.Function('A1')(T, X, Y)
A2 = sp.Function('A2')(T, X, Y)
As = [0, A1, A2, 0]
eta = sp.Matrix(sp.diag(-1, 1, 1, 1))
g5b = sp.Matrix(sp.zeros(5, 5))
for i in range(4):
    for j in range(4):
        g5b[i, j] = eta[i, j] + phi0 * As[i] * As[j]
    g5b[i, 4] = phi0 * As[i]
    g5b[4, i] = phi0 * As[i]
g5b[4, 4] = phi0
gi5b = g5b.inv()
G5b = christoffel(x5b, g5b, gi5b, mode='fast')
Ric5b = ricci_tensor(x5b, g5b, gi5b, G5b, mode='fast')
R5b = ricci_scalar(x5b, g5b, gi5b, Ric5b, mode='fast')

Fmunu = [[0] * 4 for _ in range(4)]
for mu in range(4):
    for nu in range(4):
        if As[mu] != 0 or As[nu] != 0:
            Fmunu[mu][nu] = sp.diff(As[mu], x5b[nu]) - sp.diff(As[nu], x5b[mu])
F2 = 0
for mu in range(4):
    for nu in range(4):
        F2 += eta.inv()[mu, mu] * eta.inv()[nu, nu] * Fmunu[mu][nu] * Fmunu[mu][nu]
F2 = sp.expand(F2)
diffS2 = sp.simplify(sp.expand(R5b) + sp.Rational(1, 4) * phi0 * F2)
print("R5 - (-phi/4 F^2) 差（应恒为 0）:", diffS2)

# =====================================================================
# S3：全耦合 —— g4 = Minkowski，phi 一般，A=(0,A1,A2,0)
# =====================================================================
print("=" * 72)
print("S3：g4=Minkowski，phi、A 均非平凡 —— 交叉项检查")
phB = sp.Function('phi')(T, X, Y)
g5c = sp.Matrix(sp.zeros(5, 5))
for i in range(4):
    for j in range(4):
        g5c[i, j] = eta[i, j] + phB * As[i] * As[j]
    g5c[i, 4] = phB * As[i]
    g5c[4, i] = phB * As[i]
g5c[4, 4] = phB
gi5c = g5c.inv()
G5c = christoffel(x5b, g5c, gi5c, mode='fast')
Ric5c = ricci_tensor(x5b, g5c, gi5c, G5c, mode='fast')
R5c = ricci_scalar(x5b, g5c, gi5c, Ric5c, mode='fast')

box4c = 0
for mu in range(4):
    box4c += eta.inv()[mu, mu] * sp.diff(phB, x5b[mu], 2)
dphi2c = 0
for mu in range(4):
    dphi2c += eta.inv()[mu, mu] * sp.diff(phB, x5b[mu])**2
guess = sp.Rational(-1, 4) * phB * F2 + sp.Rational(1, 2) * dphi2c / phB**2 - box4c / phB
diffS3 = sp.simplify(sp.expand(R5c) - sp.expand(guess))
print("R5 - [-(phi/4)F^2 + (1/2)(∂phi)^2/phi^2 - box phi / phi] 差（应恒为 0）:",
      diffS3)

print("\nS1/S2/S3 验证完成。")
