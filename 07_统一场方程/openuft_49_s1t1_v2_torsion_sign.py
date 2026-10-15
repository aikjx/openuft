# -*- coding: utf-8 -*-
"""机器判定 R(Gamma)-R~(LC) 与挠率二次项的关系（3D，全反对称挠率）
轻量构造：g = diag(A^2,B^2,C^2) => sqrt(g)=ABC 为多项式；循环内不 simplify。"""
import itertools
import sympy as sp

x, y, z = sp.symbols('x y z')
co = [x, y, z]
n = 3

A = 1 + x**2 / sp.Integer(3)
B = 1 + y**2 / sp.Integer(4)
C = 1 + z**2 / sp.Integer(5)
g = sp.diag(A**2, B**2, C**2)
ginv = g.inv()
sqg = A * B * C                      # sqrt(det g)，多项式


def christoffel(gm, gi):
    Gm = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += gi[a, d] * (sp.diff(gm[d, b], co[c]) + sp.diff(gm[d, c], co[b])
                                     - sp.diff(gm[b, c], co[d]))
                Gm[a][b][c] = s / 2
    return Gm


def ricci_scalar(Gm, gi):
    # dG[a][b][c][dd] = d_c Gam^a_{b dd}
    dG = [[[[sp.diff(Gm[a][b][dd], co[c]) for dd in range(n)] for c in range(n)]
           for b in range(n)] for a in range(n)]
    # R_{bd} = sum_a [ d_a Gam^a_{bd} - d_d Gam^a_{ba}
    #                  + Gam^a_{ea} Gam^e_{bd} - Gam^a_{ed} Gam^e_{ba} ]
    tot = 0
    for b in range(n):
        for d in range(n):
            s = 0
            for a in range(n):
                v = dG[a][b][a][d] - dG[a][b][d][a]
                for e in range(n):
                    v += Gm[a][e][a] * Gm[e][b][d] - Gm[a][e][d] * Gm[e][b][a]
                s += v
            tot += gi[b, d] * s
    return tot


Gt = christoffel(g, ginv)
Rt = ricci_scalar(Gt, ginv)

E3 = [[[0] * n for _ in range(n)] for _ in range(n)]
for p in itertools.permutations(range(n)):
    inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
    E3[p[0]][p[1]][p[2]] = 1 if inv % 2 == 0 else -1


def run(phi, label, pt):
    # 全反对称（全部指标降下）：T_abc = phi * sqrt(g) * [abc]
    Tl = [[[phi * sqg * E3[a][b][c] for c in range(n)] for b in range(n)] for a in range(n)]
    # 全反对称 => K_abc = 1/2 T_abc
    K = [[[sum(ginv[a, d] * Tl[d][b][c] for d in range(n)) / 2
           for c in range(n)] for b in range(n)] for a in range(n)]
    Gf = [[[Gt[a][b][c] + K[a][b][c] for c in range(n)] for b in range(n)] for a in range(n)]
    Rf = ricci_scalar(Gf, ginv)
    T2 = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                up = sum(ginv[a, P] * ginv[b, Q] * ginv[c, Rr] * Tl[P][Q][Rr]
                         for P in range(n) for Q in range(n) for Rr in range(n))
                T2 += Tl[a][b][c] * up
    diff = sp.expand(Rf - Rt)
    T2e = sp.expand(T2)
    dnum = sp.N(diff.subs(pt), 30)
    tnum = sp.N(T2e.subs(pt), 30)
    rnum = sp.N(dnum / tnum, 25)
    print(f"[{label}]  R(Gamma)-R~ = {dnum}")
    print(f"[{label}]  T_abc T^abc  = {tnum}")
    print(f"[{label}]  比值 c_T     = {rnum}   (rational guess {sp.nsimplify(rnum, [sp.Rational(1,4), sp.Rational(1,2), sp.Rational(3,4)])} )")
    return rnum


pt = {x: sp.Rational(1, 2), y: sp.Rational(-1, 3), z: sp.Rational(2, 7)}
print("== 情形1：挠率振幅为常数 phi=1 ==")
run(sp.Integer(1), "常数挠率", pt)
print()
print("== 情形2：挠率振幅非恒定 phi=1+x+2y ==")
run(1 + x + 2 * y, "非恒定挠率", pt)
print()
print("预期（标准恒等式，全反对称挠率）：c_T = -1/4")
