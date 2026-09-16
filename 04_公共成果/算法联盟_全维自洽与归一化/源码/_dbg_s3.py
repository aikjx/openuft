# -*- coding: utf-8 -*-
import sympy as sp

x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3")
X = [x0, x1, x2, x3]
g_s = sp.symbols("g", real=True)
II = sp.I
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -II], [II, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
Tmat = [sx/2, sy/2, sz/2]


def make_mat(coeffs):
    out = sp.zeros(2, 2)
    for a in range(3):
        out = out + coeffs[a] * Tmat[a]
    return out


Af = [[sp.Function("A%d_%d" % (a+1, m))(*X) for m in range(4)] for a in range(3)]
Amat = [make_mat([Af[a][m] for a in range(3)]) for m in range(4)]
th = [sp.Function("theta" + str(a+1))(*X) for a in range(3)]
theta_mat = make_mat(th)
psi0 = sp.Function("psi0")(*X)
psi1 = sp.Function("psi1")(*X)
psi = sp.Matrix([psi0, psi1])


def Dact(mu, v):
    return sp.diff(v, X[mu]) - II * g_s * Amat[mu] * v


Aprime = []
for m in range(4):
    comm = II * g_s * (theta_mat * Amat[m] - Amat[m] * theta_mat)
    Aprime.append(sp.Matrix(2, 2, lambda i, j: sp.expand((Amat[m] + sp.diff(theta_mat, X[m]) + comm)[i, j])))

psi_prime = sp.Matrix(2, 1, lambda i, j: sp.expand((psi + II*g_s*theta_mat*psi)[i, 0]))
lhs = sp.Matrix(2, 1, lambda i, j: sp.expand((sp.diff(psi_prime, X[0]) - II*g_s*Aprime[0]*psi_prime)[i, 0]))
rhs = sp.Matrix(2, 1, lambda i, j: sp.expand(((sp.eye(2) + II*g_s*theta_mat) * Dact(0, psi))[i, 0]))
d5 = sp.Matrix(2, 1, lambda i, j: sp.expand((lhs - rhs)[i, 0]))

print("raw entry0 (before subs):", d5[0, 0])
# 用具体单项式代入
subs = {}
subs[Af[0][0]] = x0*x1 + 1
subs[Af[1][0]] = x0*x2 + 2
subs[Af[2][0]] = x0*x3 + 3
subs[Af[0][1]] = x1*x2 + 4
subs[Af[1][1]] = x1*x3 + 5
subs[Af[2][1]] = x2*x3 + 6
subs[Af[0][2]] = x1 + 7
subs[Af[1][2]] = x2 + 8
subs[Af[2][2]] = x3 + 9
subs[Af[0][3]] = x0 + 10
subs[Af[1][3]] = x1 + 11
subs[Af[2][3]] = x2 + 12
subs[th[0]] = x0 + 13
subs[th[1]] = x1 + 14
subs[th[2]] = x2 + 15
subs[psi0] = x1*x3 + 16
subs[psi1] = x0*x2 + 17
r0 = sp.expand(d5[0, 0].subs(subs))
r1 = sp.expand(d5[1, 0].subs(subs))
print("after subs entry0 =", r0)
print("after subs entry1 =", r1)
print("entry0 == 0?", r0 == 0)
print("entry1 == 0?", r1 == 0)
