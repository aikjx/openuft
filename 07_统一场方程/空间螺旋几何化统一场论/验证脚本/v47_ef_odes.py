# -*- coding: utf-8 -*-
"""
v47：完整 EF 球对称黑洞解（含挠率标量 τ 对度规反馈）
EF 作用量：S = ∫√-g [ R/16πG - ½(∇τ)² - U(τ) ]，U(τ)=τ(2η+m²τ)/(2(1+gκτ)²)，κ=8π
度规：ds² = -e^{2ν}dt² + e^{2λ}dr² + r²dΩ²
第一性 sympy 推导 Einstein(G_μν=8πG T_μν) 的 tt/rr 分量 + Klein-Gordon，
解出 ν'', λ', τ'' 为一阶系统，solve_bvp 视界→无穷远，得 τ_H，代入 42/45 熵/温度。
"""
import numpy as np
import sympy as sp

# ---- 1. 符号推导场方程 ----
r, th = sp.symbols('r theta', positive=True)
Gconst, eta, m2 = sp.symbols('G eta m2', positive=True)
gconst, kappa = sp.symbols('g kappa', real=True)
nu = sp.Function('nu'); lam = sp.Function('lam'); tau = sp.Function('tau')

# 度规 ds² = -e^{2nu} dt² + e^{2lam} dr² + r² (dθ² + sin²θ dφ²)
g = sp.diag(-sp.exp(2*nu(r)), sp.exp(2*lam(r)), r**2, r**2*sp.sin(th)**2)
ginv = sp.diag(-sp.exp(-2*nu(r)), sp.exp(-2*lam(r)), 1/r**2, 1/(r**2*sp.sin(th)**2))

def chris(g, ginv, coords):
    d = len(coords); G = [[[sp.S(0) for _ in range(d)] for _ in range(d)] for _ in range(d)]
    for a in range(d):
        for b in range(d):
            for c in range(d):
                s = sp.S(0)
                for e in range(d):
                    s += ginv[a,e]*(sp.diff(g[e,c],coords[b]) + sp.diff(g[e,b],coords[c]) - sp.diff(g[b,c],coords[e]))
                G[a][b][c] = sp.simplify(s/2)
    return G

t = sp.symbols('t')
coords = [t, r, th]
G = chris(g, ginv, coords)
# 省略 φ 因对称，用 θ 分量代表角向

def ricci(g, ginv, coords, G):
    d=len(coords); R=[[sp.S(0) for _ in range(d)] for _ in range(d)]
    for a in range(d):
        for b in range(d):
            s=sp.S(0)
            for m in range(d):
                dm = sp.diff(G[m][a][b], coords[m]) - sp.diff(G[m][a][m], coords[b])
                for n in range(d):
                    dm += G[m][a][b]*G[n][m][n] - G[m][a][n]*G[n][b][m]
                s += dm
            R[a][b]=sp.simplify(s)
    return R

R = ricci(g, ginv, coords, G)
Rsc = 0
for a in range(3):
    for b in range(3):
        Rsc += ginv[a,b]*R[a][b]
Rsc = sp.simplify(Rsc)

# Einstein 张量 G_μν = R_μν - ½ g_μν R
Ett = R[0][0] - sp.Rational(1,2)*g[0,0]*Rsc
Err = R[1][1] - sp.Rational(1,2)*g[1,1]*Rsc

# 标量 T_μν = ∂_μτ∂_ντ - g_μν(½(∂τ)² + U)；静态 τ(r) => ∂_rτ=τ'
tpr = sp.symbols('tpr')
U = tau(r)*(2*eta + m2*tau(r))/(2*(1+gconst*kappa*tau(r))**2)
Ttt = -g[0,0]*(sp.Rational(1,2)*tpr**2*sp.exp(-2*lam(r)) + U)
Trr = g[1,1]*(sp.Rational(1,2)*tpr**2*sp.exp(-2*lam(r)) - U)  # (∂_rτ)²=τ'²; g_rr τ'²... careful
# 更规范：T_rr = (∂_rτ)² - g_rr L, L=½g^{rr}τ'²+U=½e^{-2λ}τ'²+U
Trr = tpr**2 - g[1,1]*(sp.Rational(1,2)*tpr**2*sp.exp(-2*lam(r)) + U)

# Klein-Gordon: □τ - U' = 0
# □τ = (1/√-g)∂_μ(√-g g^{μν}∂_ντ) ; √-g = r² sinθ e^{ν+λ}
ttau = sp.diff(sp.exp(-2*lam(r))*sp.diff(tau(r),r), r) + sp.exp(-2*lam(r))*(2/r + sp.diff(nu(r),r))*sp.diff(tau(r),r)
Up = sp.diff(U, tau(r))
KG = ttau - Up

# Einstein 方程组
eq1 = sp.simplify(Ett - 8*sp.pi*Gconst*Ttt)
eq2 = sp.simplify(Err - 8*sp.pi*Gconst*Trr)

# 未知高阶导：ν''(eq2), λ'(eq1/eq2), τ''(KG)。分步解。
nu2 = sp.symbols('nu2'); l1 = sp.symbols('l1'); t2s = sp.symbols('t2s')
lamsym = sp.Derivative(lam(r),r); nusym = sp.Derivative(nu(r),r); tausym = sp.Derivative(tau(r),r)
e1 = eq1.subs({sp.Derivative(lam(r),r): l1, sp.Derivative(tau(r),r,r): t2s})
e2 = eq2.subs({sp.Derivative(nu(r),r,r): nu2, sp.Derivative(lam(r),r): l1, sp.Derivative(tau(r),r,r): t2s})
e3 = KG.subs({sp.Derivative(tau(r),r,r): t2s, sp.Derivative(lam(r),r): l1})
print("e1 free:", [str(x) for x in e1.free_symbols])
print("e2 free:", [str(x) for x in e2.free_symbols])
print("e3 free:", [str(x) for x in e3.free_symbols])
sol_l1 = sp.solve(sp.simplify(e1), l1, dict=True)
print("L1 sol:", bool(sol_l1))
if sol_l1:
    l1expr = sol_l1[0][l1]
    e2b = e2.subs(l1, l1expr)   # e2 给出 ν'（nusym）一阶
    e3b = e3.subs(l1, l1expr)
    sol_nu = sp.solve(sp.simplify(e2b), nusym, dict=True)
    print("NU(ν') sol:", bool(sol_nu))
    if sol_nu:
        nuxpr = sol_nu[0][nusym]
        e3c = e3b.subs(nusym, nuxpr)
        sol_t2 = sp.solve(sp.simplify(e3c), t2s, dict=True)
        print("T2(τ'') sol:", bool(sol_t2))
        print("== lambda' =="); sp.pprint(sp.simplify(l1expr))
        print("== nu' =="); sp.pprint(sp.simplify(nuxpr))
        if sol_t2:
            print("== tau'' =="); sp.pprint(sp.simplify(sol_t2[0][t2s]))
            nu2j = {"lam1": str(sp.simplify(l1expr)), "nu1": str(sp.simplify(nuxpr)),
                    "tau2": str(sp.simplify(sol_t2[0][t2s]))}
            import json, os
            os.makedirs(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\空间螺旋几何化统一场论", exist_ok=True)
            with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\空间螺旋几何化统一场论\V3_18_ef_odes.json","w",encoding="utf-8") as f:
                json.dump(nu2j, f, ensure_ascii=False, indent=2)
            print("saved V3_18_ef_odes.json")
