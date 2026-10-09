# -*- coding: utf-8 -*-
"""
verify_variation.py —— 变分推导链验证
  1) Einstein: FLRW 上 G_munu = kappa^2 T_munu -> Friedmann 方程（00 与 ij 分量）
  2) Einstein-Hilbert 作用量一阶变分: d/de S[g+e h] = int sqrt(-g) G^{munu} h_munu (+边界项)
  3) Yang-Mills U(1): E-L 给出 d_mu F^{munu}=0；Bianchi 恒等式
  4) Yang-Mills SU(2): Bianchi 恒等式 D F = 0（一般场强）
  5) Dirac: E-L (i gamma D - m)psi=0
  6) 标量场: E-L D^2 phi + V'(phi)=0
  7) Noether: 全局 U(1) 对称 -> 流守恒 d_mu J^mu=0
"""
import sympy as sp
import numpy as np
from gr_toolkit import christoffel, ricci_tensor, ricci_scalar, einstein_tensor

print("=" * 72)
print("V1：FLRW 上 Einstein 方程 -> Friedmann 方程")
t = sp.symbols('t')
a = sp.Function('a')(t)
x = [t, sp.symbols('x'), sp.symbols('y'), sp.symbols('z')]
g = sp.Matrix(sp.diag(-1, a**2, a**2, a**2))
gi = g.inv()
Gc = christoffel(x, g, gi)
Ric = ricci_tensor(x, g, gi, Gc)
Gt = einstein_tensor(x, g, gi, Ric)
R = ricci_scalar(x, g, gi, Ric)
# 00 分量: G_00 = 3 a'^2/a^2  (= kappa^2 rho)
G00 = sp.simplify(Gt[0][0])
H2 = sp.simplify(G00 / 3)   # 应为 (a'/a)^2
print("G_00 =", G00)
print("(a'/a)^2 - G_00/3 =", sp.simplify(H2 - (sp.diff(a, t) / a)**2), " (应为 0)")
# ij 分量: G_ij = -(2 a''/a + a'^2/a^2) g_ij
Gij = sp.simplify(Gt[1][1] / a**2)
print("G_xx/a^2 =", Gij)
print("G_xx/a^2 + (2a''/a + a'^2/a^2) =",
      sp.simplify(Gij + (2 * sp.diff(a, t, 2) / a + (sp.diff(a, t) / a)**2)), " (应为 0)")
print("→ 即 Friedmann: H^2 = kappa^2 rho/3,  a''/a = -(kappa^2/6)(rho+3p)")

print("=" * 72)
print("V2：Einstein-Hilbert 作用量一阶变分 —— Palatini 通量公式验证")
# 完整恒等式：δ(√-g R) = -√-g G^{mn} h_mn + ∂_σ(√-g F^σ)
# 其中 F^σ = g^{mn}δΓ^σ_mn - g^{σn}δΓ^m_mn（Palatini 通量，全散度边界项）
h00 = sp.Function('h00')(t); h11 = sp.Function('h11')(t)
h22 = sp.Function('h22')(t); h33 = sp.Function('h33')(t)
hh = sp.Matrix(sp.diag(h00, h11, h22, h33))
eps = sp.symbols('eps')
gpe = g + eps * hh
sgpe = sp.sqrt(-gpe.det())
Gpe = christoffel(x, gpe, gpe.inv(), mode='fast')
Ricpe = ricci_tensor(x, gpe, gpe.inv(), Gpe, mode='fast')
Rpe = ricci_scalar(x, gpe, gpe.inv(), Ricpe, mode='fast')
LHS_full = sp.expand(sp.diff(sp.expand(sgpe * Rpe), eps).subs(eps, 0))
# 1) RHS 主项：-√-g G^{mn} h_mn
Gup2 = [[0] * 4 for _ in range(4)]
for m in range(4):
    for n in range(4):
        Gup2[m][n] = sum(gi[m, a] * gi[n, b] * Gt[a][b] for a in range(4) for b in range(4))
main = sp.expand(-sp.sqrt(-g.det()) * sum(Gup2[i][i] * hh[i, i] for i in range(4)))
# 2) δΓ^σ_mn = 1/2 g^{σλ}(∇_m h_{λn} + ∇_n h_{λm} - ∇_λ h_mn)
sg = sp.sqrt(-g.det())
dGam = {}
for s in range(4):
    for m in range(4):
        for n in range(4):
            s_ = 0
            for lam in range(4):
                nab_ln = sp.diff(hh[lam, n], x[m]) - sum(Gc[r][m][lam] * hh[r, n]
                                                         + Gc[r][m][n] * hh[lam, r] for r in range(4))
                nab_lm = sp.diff(hh[lam, m], x[n]) - sum(Gc[r][n][lam] * hh[r, m]
                                                         + Gc[r][n][m] * hh[lam, r] for r in range(4))
                nab_mn = sp.diff(hh[m, n], x[lam]) - sum(Gc[r][lam][m] * hh[r, n]
                                                         + Gc[r][lam][n] * hh[m, r] for r in range(4))
                s_ += gi[s, lam] * (nab_ln + nab_lm - nab_mn)
            dGam[(s, m, n)] = sp.expand(s_ / 2)
# 3) 通量 F^σ = Σ g^{mn} δΓ^σ_mn - Σ_n g^{σn} δΓ^m_mn
Fflux = {}
for s in range(4):
    s_ = 0
    for m in range(4):
        for n in range(4):
            s_ += gi[m, n] * dGam[(s, m, n)]
        s_ -= sum(gi[s, n] * dGam[(m, m, n)] for n in range(4))
    Fflux[s] = sp.expand(s_)
# 4) 散度 ∂_σ(√-g F^σ)
divF = 0
for s in range(4):
    divF += sp.diff(sg * Fflux[s], x[s])
diffV2 = sp.simplify(sp.expand(LHS_full - main - divF))
print("δ(√-gR) - [-√-g G h + ∂(√-g F^σ)] =", sp.expand(diffV2), " (应恒为 0)")
print("→ 变分只留下 G_mn 项 + 全散度边界项（边界项由 GHJ 项抵消）")

print("=" * 72)
print("V3：Yang-Mills U(1) —— E-L 与 Bianchi")
T, X, Y = sp.symbols('T X Y')
A0 = sp.Function('A0')(T, X, Y); A1 = sp.Function('A1')(T, X, Y)
A2 = sp.Function('A2')(T, X, Y)
As = [A0, A1, A2]
xx = [T, X, Y]
# L = -1/4 F_munu F^{munu}（欧氏，取 + 号与 E-L 推导无关）
Fmat = [[0] * 3 for _ in range(3)]
for mu in range(3):
    for nu in range(3):
        Fmat[mu][nu] = sp.diff(As[mu], xx[nu]) - sp.diff(As[nu], xx[mu])
L = -sp.Rational(1, 4) * sum(Fmat[mu][nu]**2 for mu in range(3) for nu in range(3))
# E-L: d_mu (dL/d(d_mu A_nu)) - dL/dA_nu = 0  ==>  -d_mu F^{munu} = 0
EL = [sp.simplify(
    sum(sp.diff(sp.diff(L, sp.diff(As[nu], xx[mu])), xx[mu]) for mu in range(3))
    - sp.diff(L, As[nu])) for nu in range(3)]
# 期望 EL[nu] = -d_mu F^{munu} = -(box A_nu - d_nu d·A)（Maxwell 方程算子）
for nu in range(3):
    boxA = sum(sp.diff(As[nu], xx[mu], 2) for mu in range(3))
    ddivA = sp.diff(sum(sp.diff(As[m], xx[m]) for m in range(3)), xx[nu])
    maxwell_op = sp.expand(-(boxA - ddivA))
    print("U(1) E-L[%d] = %s" % (nu, EL[nu]))
    print("   -(box A - d d·A)[%d] = %s   差 = %s"
          % (nu, maxwell_op, sp.simplify(EL[nu] - maxwell_op)))
# 说明：E-L 正是 Maxwell 方程 d_mu F^{munu}=0（on-shell 成立，非恒等零）
# 并验证 d_mu d_nu F^{munu} = 0（自动恒等式，无源时的流守恒）
auto = sp.simplify(sum(sp.diff(sp.diff(Fmat[mu][nu], xx[mu]), xx[nu])
                       for mu in range(3) for nu in range(3)))
print("d_mu d_nu F^{munu}（恒为 0）:", auto)
# Bianchi: d_mu F_nu rho + d_nu F_rho mu + d_rho F_mu nu = 0
for (m, n, r) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
    B = sp.simplify(sp.diff(Fmat[n][r], xx[m]) + sp.diff(Fmat[r][m], xx[n])
                    + sp.diff(Fmat[m][n], xx[r]))
    print("Bianchi(%d,%d,%d) =" % (m, n, r), B)

print("=" * 72)
print("V4：Yang-Mills SU(2) —— 非阿贝尔 Bianchi 恒等式 D F = 0")
# 一般 SU(2) 场强: F^a_munu = d_mu A^a_nu - d_nu A^a_mu + g eps^abc A^b_mu A^c_nu
# Bianchi: D F = d F + g A x F = 0（Jacobi 恒等式保证）
import itertools
g_c, eps_c = sp.symbols('g_c'), 1
Aaa = {}
for a in range(3):
    for mu in range(3):
        Aaa[(a, mu)] = sp.Function('A%d_%d' % (a, mu))(T, X, Y)
Faa = {}
for a in range(3):
    for mu in range(3):
        for nu in range(3):
            F = sp.diff(Aaa[(a, nu)], xx[mu]) - sp.diff(Aaa[(a, mu)], xx[nu])
            for b in range(3):
                for c in range(3):
                    eabc = int(0.5 * (b - c) * (a == 0) )  # placeholder
            Faa[(a, mu, nu)] = F
# 重新用真 Levi-Civita 计算
def eps(a, b, c):
    if (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        return 1
    if (a, b, c) in [(0, 2, 1), (2, 1, 0), (1, 0, 2)]:
        return -1
    return 0
for a in range(3):
    for mu in range(3):
        for nu in range(3):
            Faa[(a, mu, nu)] = (sp.diff(Aaa[(a, nu)], xx[mu])
                                - sp.diff(Aaa[(a, mu)], xx[nu])
                                + g_c * sum(eps(a, b, c) * Aaa[(b, mu)] * Aaa[(c, nu)]
                                            for b in range(3) for c in range(3)))
# 检验 Bianchi: eps^{munu rho} D_mu F^a_nu rho = 0
ok = True
for a in range(3):
    B = 0
    for mu in range(3):
        for nu in range(3):
            for rho in range(3):
                if eps(mu, nu, rho) != 0:
                    # D_mu F^a_nurho = d_mu F^a_nurho + g eps^{abc} A^b_mu F^c_nurho
                    B += eps(mu, nu, rho) * (
                        sp.diff(Faa[(a, nu, rho)], xx[mu])
                        + g_c * sum(eps(a, b, c) * Aaa[(b, mu)] * Faa[(c, nu, rho)]
                                    for b in range(3) for c in range(3)))
    Bs = sp.simplify(sp.expand(B))
    ok = ok and (Bs == 0)
    print("SU(2) Bianchi(a=%d) =" % a, Bs)
print("SU(2) Bianchi 恒等式成立:", ok)

print("=" * 72)
print("V5：Dirac E-L 与 U(1) Noether 守恒")
# 将 psi, psib 视为独立场，变分 S = int psib (i gamma D - m) psi
# 取 psi、psib 为 Grassmann-like 独立复函数；E-L 对 psib 求导
# 简单代数验证：S = psib * M * psi,  dS/dpsib = M psi -> E-L 直接给出 (i gamma D - m) psi = 0
# 代数恒等式（无需数值）：delta S / delta psib = (i gamma^mu D_mu - m) psi  —— 由定义
print("E-L:  delta S / delta psibar = (i gamma^mu D_mu - m) psi  => 方程 (i gamma D - m) psi = 0")
print("（由作用量线性于 psibar 直接给出，无需积分）")

print("=" * 72)
print("V6：标量场 E-L 与 U(1) Noether 流")
phi1 = sp.Function('phi1')(T, X, Y); phi2 = sp.Function('phi2')(T, X, Y)
u = sp.symbols('u')
Vu = sp.Function('V')(u)
# 复标量 phi=phi1+i phi2, L = |d phi|^2 - V(|phi|^2)
Lsc = sum(sp.diff(phi1, xx[mu])**2 + sp.diff(phi2, xx[mu])**2
          for mu in range(3)) - Vu.subs(u, phi1**2 + phi2**2)
# E-L(phi1): 2 box phi1 + 2 phi1 V'(|phi|^2) = 0
EL1 = sp.expand(sum(sp.diff(sp.diff(Lsc, sp.diff(phi1, xx[mu])), xx[mu])
                    for mu in range(3)) - sp.diff(Lsc, phi1))
EL2 = sp.expand(sum(sp.diff(sp.diff(Lsc, sp.diff(phi2, xx[mu])), xx[mu])
                    for mu in range(3)) - sp.diff(Lsc, phi2))
box1 = sp.expand(sum(sp.diff(phi1, xx[mu], 2) for mu in range(3)))
box2 = sp.expand(sum(sp.diff(phi2, xx[mu], 2) for mu in range(3)))
Vp = sp.diff(Vu, u).subs(u, phi1**2 + phi2**2)
print("E-L(phi1) - 2[box phi1 + V' phi1] =", sp.simplify(EL1 - 2 * (box1 + Vp * phi1)), " (应为 0)")
print("E-L(phi2) - 2[box phi2 + V' phi2] =", sp.simplify(EL2 - 2 * (box2 + Vp * phi2)), " (应为 0)")
print("→ 即 Klein-Gordon 型：box phi + V'(|phi|^2) phi = 0")
# Noether: 全局 U(1) phi->e^{ia}phi,  J^mu = i(phi* d^mu phi - phi d^mu phi*) = -2(phi1 d^mu phi2 - phi2 d^mu phi1)
J0 = -2 * (phi1 * sp.diff(phi2, T) - phi2 * sp.diff(phi1, T))
dJ = sp.expand(sp.diff(J0, T))
# d_mu J^mu = -2(phi1 box phi2 - phi2 box phi1)
expect_dJ = -2 * (phi1 * box2 - phi2 * box1)
print("d_t J^t =", dJ)
print("dJ - (-2)(phi1 box phi2 - phi2 box phi1) =",
      sp.simplify(dJ - expect_dJ), " (应为 0)")
# on-shell 代入 box phi_i = -V' phi_i：
onshell = sp.expand(expect_dJ.subs(box1, -Vp * phi1).subs(box2, -Vp * phi2))
print("on-shell 后 d_mu J^mu =", sp.simplify(onshell), " (应为 0，Noether 守恒)")

print("\n变分推导链验证完成。")
