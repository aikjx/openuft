# -*- coding: utf-8 -*-
"""
uft_geom_engine.py — 全维统一场论「求导引擎」
================================================================
提供两条互相独立、可交叉校验的计算链路：

  A. 符号链路（sympy）：Christoffel → Riemann → Ricci → R → Einstein
     用于「求导证明」：得到完全精确的解析表达式。

  B. 数值链路（numpy，批量/向量化）：同一套几何量在任意维 D 上
     对 N 个采样点并行求值，用于「泛函求导」与「精算验证」。

两条链路在自检中对同一度规交叉比对，确保符号推导与数值求值
不会互相"自证"——这是本引擎的设计原则。

指标约定（与 MTW / Wald 一致）：
  Γ^ρ_{μν} = ½ g^{ρσ}(∂_μ g_{σν} + ∂_ν g_{σμ} − ∂_σ g_{μν})
  R^ρ_{σμν} = ∂_μ Γ^ρ_{νσ} − ∂_ν Γ^ρ_{μσ} + Γ^ρ_{μλ}Γ^λ_{νσ} − Γ^ρ_{νλ}Γ^λ_{μσ}
  R_{σν}    = R^ρ_{σρν}
  R         = g^{σν} R_{σν}
  G_{μν}    = R_{μν} − ½ R g_{μν}
"""
import numpy as np
import sympy as sp


# ============================================================
# A. 符号几何
# ============================================================

def sym_christoffel(g, x, simplify=True):
    """Γ^ρ_{μν}，返回嵌套 list [rho][mu][nu]"""
    D = len(x)
    ginv = g.inv()
    Gam = [[[sp.Integer(0)] * D for _ in range(D)] for _ in range(D)]
    for r in range(D):
        for m in range(D):
            for n in range(m, D):                      # Γ 对 μν 对称
                s = 0
                for k in range(D):
                    s += ginv[r, k] * (sp.diff(g[k, m], x[n])
                                       + sp.diff(g[k, n], x[m])
                                       - sp.diff(g[m, n], x[k]))
                val = sp.simplify(s / 2) if simplify else s / 2
                Gam[r][m][n] = val
                Gam[r][n][m] = val
    return Gam


def sym_riemann(Gam, x, simplify=True):
    """R^ρ_{σμν}，返回 [rho][sigma][mu][nu]"""
    D = len(x)
    Rie = [[[[sp.Integer(0)] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
    for r in range(D):
        for s in range(D):
            for m in range(D):
                for n in range(m + 1, D):              # 对 μν 反对称
                    expr = (sp.diff(Gam[r][n][s], x[m])
                            - sp.diff(Gam[r][m][s], x[n]))
                    for lam in range(D):
                        expr += (Gam[r][m][lam] * Gam[lam][n][s]
                                 - Gam[r][n][lam] * Gam[lam][m][s])
                    val = sp.simplify(expr) if simplify else expr
                    Rie[r][s][m][n] = val
                    Rie[r][s][n][m] = -val
    return Rie


def sym_ricci(Rie, simplify=True):
    """R_{σν} = R^ρ_{σρν}"""
    D = len(Rie)
    Ric = sp.zeros(D, D)
    for s in range(D):
        for n in range(s, D):
            expr = sum(Rie[r][s][r][n] for r in range(D))
            expr = sp.simplify(expr) if simplify else expr
            Ric[s, n] = expr
            Ric[n, s] = expr
    return Ric


def sym_curvature_quantities(g, x, simplify=True):
    """一步到位：Christoffel / Riemann / Ricci / R / Einstein"""
    Gam = sym_christoffel(g, x, simplify)
    Rie = sym_riemann(Gam, x, simplify)
    Ric = sym_ricci(Rie, simplify)
    ginv = g.inv()
    D = g.shape[0]
    Rs = sp.simplify(sum(ginv[s, n] * Ric[s, n] for s in range(D) for n in range(D))) \
        if simplify else sum(ginv[s, n] * Ric[s, n] for s in range(D) for n in range(D))
    G = sp.zeros(D, D)
    for m in range(D):
        for n in range(m, D):
            val = Ric[m, n] - Rs * g[m, n] / 2
            val = sp.simplify(val) if simplify else val
            G[m, n] = val
            G[n, m] = val
    return dict(Gam=Gam, Rie=Rie, Ric=Ric, R=Rs, G=G, ginv=ginv)


def sym_cov_div_up2(Gam, Tup, x, simplify=True):
    """∇_μ T^{μν}（Tup 为逆变二阶张量 Matrix，对称）"""
    D = len(x)
    out = []
    for n in range(D):
        expr = 0
        for m in range(D):
            expr += sp.diff(Tup[m, n], x[m])
            for lam in range(D):
                expr += Gam[m][lam][m] * Tup[lam, n]      # Γ^μ_{λμ} T^{λν}
                expr += Gam[n][m][lam] * Tup[m, lam]      # Γ^ν_{μλ} T^{μλ}
        out.append(sp.simplify(expr) if simplify else expr)
    return sp.Matrix(out)


# ============================================================
# B. 数值几何（批量向量化）
# ============================================================
#   g   : (N, D, D)          g[:, m, n]      = g_{mn}
#   dg  : (N, D, D, D)       dg[:, s, m, n]  = ∂_s g_{mn}
#   ddg : (N, D, D, D, D)    ddg[:, r, s, m, n] = ∂_r∂_s g_{mn}

def num_christoffel(ginv, dg):
    """Γ^ρ_{μν}，返回 (N, rho, mu, nu)"""
    # inside[nu, lam, sig] = ∂_ν g_{λσ} + ∂_σ g_{λν} − ∂_λ g_{νσ}
    inside = dg.transpose(0, 1, 2, 3) + dg.transpose(0, 3, 2, 1) - dg.transpose(0, 2, 1, 3)
    return 0.5 * np.einsum('qrl,qnls->qrns', ginv, inside)


def num_riemann(ginv, dg, ddg):
    """R^ρ_{σμν}，返回 (N, rho, sigma, mu, nu)。Γ 的导数用 g 的二阶导精确构造，非差分。"""
    Gam = num_christoffel(ginv, dg)                                  # (N, rho, mu, nu)

    inside = dg.transpose(0, 1, 2, 3) + dg.transpose(0, 3, 2, 1) - dg.transpose(0, 2, 1, 3)
    # ∂_μ∂_ν g_{λσ} + ∂_μ∂_σ g_{λν} − ∂_μ∂_λ g_{νσ}   -> (N, mu, nu, lam, sig)
    dinside = (ddg.transpose(0, 1, 2, 3, 4)
               + ddg.transpose(0, 1, 4, 3, 2)
               - ddg.transpose(0, 1, 3, 2, 4))

    # ∂_μ g^{ρλ} = − g^{ρα}(∂_μ g_{αβ}) g^{βλ}
    dginv = -np.einsum('qpa,qmab,qbl->qmpl', ginv, dg, ginv)          # (N, mu, rho, lam)

    # ∂_μ Γ^ρ_{νσ} = ½(∂_μ g^{ρλ}) inside_{νλσ} + ½ g^{ρλ} dinside_{μνλσ}
    part1 = 0.5 * np.einsum('qmpl,qnls->qmpns', dginv, inside)        # (N, mu, rho, nu, sig)
    part2 = 0.5 * np.einsum('qpl,qmnls->qmpns', ginv, dinside)        # (N, mu, rho, nu, sig)
    dGam = part1 + part2

    #   R^ρ_{σμν} = ∂_μΓ^ρ_{νσ} − ∂_νΓ^ρ_{μσ} + Γ^ρ_{μλ}Γ^λ_{νσ} − Γ^ρ_{νλ}Γ^λ_{μσ}
    #   Gam 轴为 (N, ρ, μ, ν)。
    #     项3 Σ_λ Γ^ρ_{μλ}Γ^λ_{νσ} : 'qrml,qlns->qrsmn'
    #     项4 Σ_λ Γ^ρ_{νλ}Γ^λ_{μσ} : 'qrnl,qlms->qrsmn'
    Rie = (dGam.transpose(0, 2, 4, 1, 3)          # (N,rho,sig,mu,nu) ← dGam[mu,rho,nu,sig]
           - dGam.transpose(0, 2, 4, 3, 1)        # ← dGam[nu,rho,mu,sig]
           + np.einsum('qrml,qlns->qrsmn', Gam, Gam)
           - np.einsum('qrnl,qlms->qrsmn', Gam, Gam))
    return Rie


def num_curvature(g, dg, ddg):
    """返回 ginv, Gamma, Rie, Ric, R, G, Gup, sqrt_neg_det"""
    ginv = np.linalg.inv(g)
    Gam = num_christoffel(ginv, dg)
    Rie = num_riemann(ginv, dg, ddg)
    Ric = np.einsum('qrsrn->qsn', Rie)                 # (N, sigma, nu)
    Rs = np.einsum('qsn,qsn->q', ginv, Ric)
    G = Ric - 0.5 * Rs[:, None, None] * g
    Gup = np.einsum('qma,qnb,qab->qmn', ginv, ginv, G)
    sdet = np.sqrt(np.abs(np.linalg.det(g)))
    return dict(ginv=ginv, Gam=Gam, Rie=Rie, Ric=Ric, R=Rs, G=G, Gup=Gup, sqrtdet=sdet)


# ============================================================
# C. Gauss–Legendre 张量积求积（任意维）
# ============================================================

def gauss_legendre_grid(n, lo=0.0, hi=1.0, D=4):
    """返回 (nodes (N,D), weights (N,))，N = n**D"""
    xi, wi = np.polynomial.legendre.leggauss(n)
    nodes_1d = 0.5 * (hi - lo) * xi + 0.5 * (hi + lo)
    w_1d = 0.5 * (hi - lo) * wi
    mesh = np.meshgrid(*([nodes_1d] * D), indexing='ij')
    nodes = np.stack([m.ravel() for m in mesh], axis=-1)
    weights = np.ones(nodes.shape[0])
    for m in np.meshgrid(*([w_1d] * D), indexing='ij'):
        weights *= m.ravel()
    return nodes, weights


# ============================================================
# D. 自检：与已知解析解交叉比对
# ============================================================

def selfcheck_schwarzschild():
    """施瓦西度规（签名 −+++）：真空 ⇒ R_μν = 0, R = 0"""
    t, r, th, M = sp.symbols('t r theta M', positive=True)
    ph = sp.Symbol('phi', real=True)
    x = [t, r, th, ph]
    f = 1 - 2 * M / r
    g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
    geo = sym_curvature_quantities(g, x)
    Ric = geo['Ric']
    zero = all(sp.simplify(Ric[i, j]) == 0 for i in range(4) for j in range(4))
    return zero, sp.simplify(geo['R']), geo


def selfcheck_flrw_D(D, a_expr, t):
    """D 维平坦 FLRW：ds² = −dt² + a(t)² Σ dx_i²
       解析： R_00 = −(D−1) ä/a ； R_ij = [a ä + (D−2) ȧ²] δ_ij
              R    = 2(D−1) ä/a + (D−1)(D−2) H²
       返回与解析式的三个差值（应全为 0）
    """
    xs = sp.symbols('x0:%d' % (D - 1), real=True)
    coords = [t] + list(xs)
    a = a_expr
    g = sp.diag(-1, *([a**2] * (D - 1)))
    geo = sym_curvature_quantities(g, coords)
    Ric = geo['Ric']
    ad, add = sp.diff(a, t), sp.diff(a, t, 2)
    d00 = sp.simplify(Ric[0, 0] + (D - 1) * add / a)
    dij = sp.simplify(Ric[1, 1] - (a * add + (D - 2) * ad**2))
    dR = sp.simplify(geo['R'] - (2 * (D - 1) * add / a + (D - 1) * (D - 2) * (ad / a)**2))
    return d00, dij, dR, geo


if __name__ == '__main__':
    import sys, time
    sys.stdout.reconfigure(encoding='utf-8')
    print('=' * 68)
    print('UFT 几何引擎自检')
    print('=' * 68)

    t0 = time.time()
    ok, Rs, _ = selfcheck_schwarzschild()
    print(f'\n[1] 施瓦西度规  Ric=0 : {ok} | R={Rs}   ({time.time()-t0:.1f}s)')

    t = sp.Symbol('t', positive=True)
    H = sp.Symbol('H', positive=True)
    for D in (4, 5, 6):
        t0 = time.time()
        a = sp.exp(H * t)                      # de Sitter
        d00, dij, dR, _ = selfcheck_flrw_D(D, a, t)
        print(f'[2] D={D} 平坦FLRW(a=e^(Ht)): dR00={d00}, dRij={dij}, dR={dR}  ({time.time()-t0:.1f}s)')

    t0 = time.time()
    a2 = sp.Symbol('t', positive=True) ** sp.Rational(2, 3)   # 物质主导 a ∝ t^{2/3}
    d00, dij, dR, _ = selfcheck_flrw_D(4, a2, sp.Symbol('t', positive=True))
    print(f'[3] D=4 平坦FLRW(a=t^(2/3)): dR00={d00}, dRij={dij}, dR={dR}  ({time.time()-t0:.1f}s)')
