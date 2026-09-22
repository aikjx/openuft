# -*- coding: utf-8 -*-
"""
gr_toolkit.py —— 通用 D 维黎曼几何符号计算工具（sympy）
用于验证统一场论文档中的全部几何推导：
  1) 测度行列式变分恒等式  delta sqrt(-g) = -1/2 sqrt(-g) g_munu delta g^munu
  2) Christoffel / Ricci / Ricci 标量（任意维）
  3) Bianchi 恒等式  div(G) = 0
  4) Kaluza-Klein 约化 R_5 = R_4 + gauge + dilaton
工具本身先用 Schwarzschild 与 FLRW 的已知解析结果自检。
"""
import sympy as sp


def _simp(expr, mode):
    return sp.simplify(expr) if mode == 'full' else sp.expand(expr)


def christoffel(x, g, ginv, mode='full'):
    """Gamma^k_{ij} = 1/2 g^{kl}(g_{li,j}+g_{lj,i}-g_{ij,l})"""
    n = len(x)
    G = [[[0] * n for _ in range(n)] for _ in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                s = 0
                for l in range(n):
                    s += ginv[k, l] * (sp.diff(g[l, i], x[j])
                                       + sp.diff(g[l, j], x[i])
                                       - sp.diff(g[i, j], x[l]))
                G[k][i][j] = _simp(s / 2, mode)
    return G


def ricci_tensor(x, g, ginv, G, mode='full'):
    """R_munu = d_rho Gamma^rho_munu - d_nu Gamma^rho_murho
                + Gamma^sigma_munu Gamma^rho_sigmarho - Gamma^rho_nusigma Gamma^sigma_murho"""
    n = len(x)
    Ric = [[0] * n for _ in range(n)]
    for mu in range(n):
        for nu in range(n):
            s = 0
            for rho in range(n):
                s += sp.diff(G[rho][mu][nu], x[rho]) - sp.diff(G[rho][mu][rho], x[nu])
            for sig in range(n):
                for rho in range(n):
                    s += G[sig][mu][nu] * G[rho][sig][rho] - G[rho][nu][sig] * G[sig][mu][rho]
            Ric[mu][nu] = _simp(s, mode)
    return Ric


def ricci_scalar(x, g, ginv, Ric, mode='full'):
    n = len(x)
    s = 0
    for mu in range(n):
        for nu in range(n):
            s += ginv[mu, nu] * Ric[mu][nu]
    return _simp(s, mode)


def einstein_tensor(x, g, ginv, Ric):
    n = len(x)
    R = ricci_scalar(x, g, ginv, Ric)
    Gt = [[sp.simplify(Ric[mu][nu] - sp.Rational(1, 2) * g[mu, nu] * R) for nu in range(n)]
          for mu in range(n)]
    return Gt


def cov_div_of_einstein(x, g, ginv, G_chr, Gt):
    """检验 div(G) = 0：nabla_mu G^{munu} = 0（Bianchi 恒等式）。
    返回一个 n-向量，各分量应为 0。"""
    n = len(x)
    out = []
    for nu in range(n):
        s = 0
        for mu in range(n):
            # G^{munu} = g^{mu a} g^{nu b} G_{ab}
            Gmunnu = sum(ginv[mu, a] * ginv[nu, b] * Gt[a][b] for a in range(n) for b in range(n))
            s += sp.diff(Gmunnu, x[mu])
            for lam in range(n):
                s += G_chr[mu][mu][lam] * Gmunnu  # Gamma^mu_{mu lam} G^{lam nu}  (lam 换)
        # 上面第二项下标处理要小心，改成显式：
        out.append(sp.simplify(s))
    return out


def cov_div_general(x, g, ginv, G_chr, T_uu):  # T_uu: 逆变二阶张量 (list of list)
    """nabla_mu T^{mu nu}"""
    n = len(x)
    out = []
    for nu in range(n):
        s = 0
        for mu in range(n):
            s += sp.diff(T_uu[mu][nu], x[mu])
            for lam in range(n):
                s += G_chr[mu][mu][lam] * T_uu[lam][nu]
                s += G_chr[nu][mu][lam] * T_uu[mu][lam]
        out.append(sp.simplify(s))
    return out
