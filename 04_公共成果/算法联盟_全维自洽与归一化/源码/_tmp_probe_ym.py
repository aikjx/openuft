# -*- coding: utf-8 -*-
import time
import sympy as sp

x0, x1, x2, x3 = sp.symbols('x0 x1 x2 x3')
X = [x0, x1, x2, x3]
g = sp.symbols('g')
A = [[sp.Function('A' + str(a + 1) + '_' + str(m))(*X) for m in range(4)] for a in range(3)]
sgn = [1, -1, -1, -1]


def F(a, m, n):
    if m == n:
        return sp.Integer(0)
    s = sum(int(sp.LeviCivita(a, b, c)) * A[b][m] * A[c][n] for b in range(3) for c in range(3))
    return sp.expand(sp.diff(A[a][n], X[m]) - sp.diff(A[a][m], X[n]) + g * s)


t0 = time.time()
L = -(sp.Integer(1) / 4) * sum(F(a, m, n) * sgn[m] * sgn[n] * F(a, m, n)
                               for a in range(3) for m in range(4) for n in range(4))
print('buildL %.1fs terms=%d' % (time.time() - t0, len(sp.Add.make_args(sp.expand(L)))))
t0 = time.time()
eq = sp.euler_equations(L, [A[0][0]], X)
print('EL one field %.1fs' % (time.time() - t0))
print(sp.simplify(eq[0].lhs))
