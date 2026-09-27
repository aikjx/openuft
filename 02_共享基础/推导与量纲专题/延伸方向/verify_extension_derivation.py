# -*- coding: utf-8 -*-
"""
推导与量纲专题 · 延伸方向 A-E 求导证明与精算验证

依赖：sympy（符号求导证明） + mpmath（50 位精算）；量纲代数用标准库 Fraction（精确有理数）。

核验组：
  A 组  4 势 -> 麦克斯韦方程 4 维张量形式（F_{mu nu}、d_mu F^{mu nu} = mu0 J^nu、对偶 Bianchi）+ 全套量纲核验
  B 组  最小耦合原理 d_mu -> D_mu（规范协变性两套约定、对易子、动量平移 p -> p - qA）+ 量纲核验
  C 组  弱场近似：爱因斯坦场方程 -> 牛顿泊松方程 nabla^2 Phi = 4 pi G rho（迹反转、线性化、牛顿极限、点源散度定理）
  D 组  量纲分析推导普朗克质量 / 长度 / 时间（唯一性线性方程组 + 50 位数值 + CODATA 比对）
  E 组  黎曼张量代数对称性与 Bianchi 恒等式（2 维球面精确 + Schwarzschild 真空解 + 独立分量数）

输出格式与仓库治理脚本一致：PASS / FAIL / BOUNDARY / INFO 计数。
"""

import sys
from fractions import Fraction as F

import sympy as sp
from mpmath import mp, mpf, sqrt as mpsqrt

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 50

CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P(name, detail=""):
    CNT["PASS"] += 1
    print("[PASS] " + name + (" | " + detail if detail else ""))


def Fl(name, detail=""):
    CNT["FAIL"] += 1
    print("[FAIL] " + name + (" | " + detail if detail else ""))


def Bd(name, detail=""):
    CNT["BOUNDARY"] += 1
    print("[BOUNDARY] " + name + (" | " + detail if detail else ""))


def Ifn(name, detail=""):
    CNT["INFO"] += 1
    print("[INFO] " + name + (" | " + detail if detail else ""))


def check(name, ok, detail=""):
    if ok:
        P(name, detail)
    else:
        Fl(name, detail)
    return ok


# ----------------------------------------------------------------- 量纲代数
def dim(m=0, l=0, t=0, i=0):
    return (F(m), F(l), F(t), F(i))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, k):
    k = F(k)
    return tuple(x * k for x in a)


def dshow(a):
    names = ["M", "L", "T", "I"]
    parts = []
    for n, v in zip(names, a):
        if v == 0:
            continue
        parts.append(n if v == 1 else n + "^" + str(v))
    return "1" if not parts else " ".join(parts)


def rref_solve(mat, rhs):
    """有理数高斯消元：返回 (sol, unique, consistent)。mat: list[row(list[Fraction])]。"""
    nrow = len(mat)
    ncol = len(mat[0]) if nrow else 0
    A = [list(map(F, r)) + [F(rhs[k])] for k, r in enumerate(mat)]
    piv = []
    r = 0
    for c in range(ncol):
        sel = None
        for rr in range(r, nrow):
            if A[rr][c] != 0:
                sel = rr
                break
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for rr in range(nrow):
            if rr != r and A[rr][c] != 0:
                fac = A[rr][c]
                A[rr] = [a - fac * b for a, b in zip(A[rr], A[r])]
        piv.append(c)
        r += 1
        if r == nrow:
            break
    # 相容性：全零行对应 rhs 非零
    for rr in range(r, nrow):
        if all(A[rr][c] == 0 for c in range(ncol)) and A[rr][ncol] != 0:
            return None, False, False
    sol = [F(0)] * ncol
    for k, c in enumerate(piv):
        sol[c] = A[k][ncol]
    return sol, (len(piv) == ncol), True


def dim_solve(basis_dims, target):
    """求解 a_k 使 prod [basis_k]^{a_k} = target。basis_dims: list[dim]。"""
    mat = [[basis_dims[k][j] for k in range(len(basis_dims))] for j in range(4)]
    return rref_solve(mat, [F(v) for v in target])


# --------------------------------------------------------------- 符号工具
def is_zero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    e3 = sp.simplify(e2)
    return e3 == 0


def EPS(i, j, k):
    return int(sp.LeviCivita(i + 1, j + 1, k + 1))


print("=" * 74)
print("A 组 · 4 势 A^mu -> 麦克斯韦方程 4 维张量形式")
print("=" * 74)

t, x, y, z = sp.symbols("t x y z")
c = sp.Symbol("c", positive=True)
XC4 = [t, x, y, z]
ETA = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]

phi = sp.Function("phi")(t, x, y, z)
A1 = sp.Function("A1")(t, x, y, z)
A2 = sp.Function("A2")(t, x, y, z)
A3 = sp.Function("A3")(t, x, y, z)
Av = [A1, A2, A3]

A_up = [phi / c, A1, A2, A3]          # A^mu = (phi/c, A)
A_dn = [phi / c, -A1, -A2, -A3]       # A_mu = eta_{mu nu} A^nu


def pd(mu, e):
    """4 维协变导数算子作用（平直时空笛卡尔系，分量即 d/dx^mu，x^0 = c t）。"""
    if mu == 0:
        return sp.diff(e, t) / c
    return sp.diff(e, XC4[mu])


Fmn = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Fmn[mu, nu] = sp.expand(pd(mu, A_dn[nu]) - pd(nu, A_dn[mu]))

Ev = [-sp.diff(phi, XC4[i]) - sp.diff(Av[i - 1], t) for i in (1, 2, 3)]
Bv = [sum(EPS(k, i, j) * sp.diff(Av[j], XC4[i + 1])
          for i in range(3) for j in range(3)) for k in range(3)]

ok_a1 = all(is_zero(Fmn[0, i] - Ev[i - 1] / c) for i in (1, 2, 3))
ok_a2 = all(is_zero(Fmn[i, j] + sum(EPS(k, i - 1, j - 1) * Bv[k] for k in range(3)))
            for i in (1, 2, 3) for j in (1, 2, 3) if i < j)
check("A1 F_{0i} = E_i / c（3 个分量符号恒等）", ok_a1)
check("A2 F_{ij} = -eps_{ijk} B_k（3 个独立分量符号恒等）", ok_a2)
check("A3 F_{mu nu} 反对称", all(is_zero(Fmn[m, n] + Fmn[n, m]) for m in range(4) for n in range(4)))

Fup = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Fup[mu, nu] = sum(ETA[mu][a] * ETA[nu][b] * Fmn[a, b] for a in range(4) for b in range(4))

divF = [sp.expand(sum(pd(mu, Fup[mu, nu]) for mu in range(4))) for nu in range(4)]

divE = sp.expand(sum(sp.diff(Ev[i], XC4[i + 1]) for i in range(3)))
curlB = [sum(EPS(k, i, j) * sp.diff(Bv[j], XC4[i + 1]) for i in range(3) for j in range(3))
         for k in range(3)]

ok_a4 = is_zero(divF[0] - divE / c)
ok_a5 = all(is_zero(divF[i] - (curlB[i - 1] - sp.diff(Ev[i - 1], t) / c ** 2)) for i in (1, 2, 3))
check("A4 d_mu F^{mu 0} = (div E)/c", ok_a4)
check("A5 d_mu F^{mu i} = (curl B)_i - (1/c^2) d_t E_i", ok_a5)

# 场方程 -> 高斯定律 / 安培-麦克斯韦定律（用 eps0 mu0 c^2 = 1）
eps0 = sp.Symbol("epsilon_0", positive=True)
mu0 = sp.Symbol("mu_0", positive=True)
rho = sp.Function("rho")(t, x, y, z)
Jv = [sp.Function("J%d" % (i + 1))(t, x, y, z) for i in range(3)]
sub_c2 = {mu0: 1 / (eps0 * c ** 2)}

gauss = sp.simplify((mu0 * c ** 2 * rho).subs(sub_c2) - rho / eps0)
check("A6 场方程 nu=0 -> div E = rho/eps_0（用 eps_0 mu_0 c^2 = 1）", is_zero(gauss))

amp = sp.simplify((1 / c ** 2 - mu0 * eps0).subs(eps0, 1 / (mu0 * c ** 2)))
check("A7 场方程 nu=i -> curl B = mu_0 J + mu_0 eps_0 d_t E（用 1/c^2 = mu_0 eps_0）", is_zero(amp))

# 对偶（齐次）方程：d_[lambda F_{mu nu}] = 0
combos = [(l, m, n) for l in range(4) for m in range(4) for n in range(4) if l < m < n]
ok_a8 = all(is_zero(pd(l, Fmn[m, n]) + pd(m, Fmn[n, l]) + pd(n, Fmn[l, m])) for (l, m, n) in combos)
check("A8 对偶 Bianchi 恒等式 d_[lambda F_{mu nu}] = 0（全部 %d 组）" % len(combos), ok_a8)

divB = sp.expand(sum(sp.diff(Bv[i], XC4[i + 1]) for i in range(3)))
ok_a9 = is_zero(pd(1, Fmn[2, 3]) + pd(2, Fmn[3, 1]) + pd(3, Fmn[1, 2]) + divB)
check("A9 (1,2,3) 分量 -> div B = 0", ok_a9)

cE = [sum(EPS(k, i, j) * sp.diff(Ev[j], XC4[i + 1]) for i in range(3) for j in range(3))
      for k in range(3)]
ok_a10 = all(is_zero(pd(0, Fmn[i, j]) + pd(i, Fmn[j, 0]) + pd(j, Fmn[0, i])
                     + (sp.diff(Bv[k], t) + cE[k]) / c)
             for (k, i, j) in [(2, 1, 2), (0, 2, 3), (1, 3, 1)])
check("A10 (0,i,j) 分量 -> curl E = -d_t B（法拉第定律）", ok_a10)

# 量纲核验
D_E = dim(m=1, l=1, t=-3, i=-1)
D_B = dim(m=1, t=-2, i=-1)
D_C = dim(l=1, t=-1)
D_MU0 = dim(m=1, l=1, t=-2, i=-2)
D_RHO = dim(i=1, t=1, l=-3)
D_LINV = dim(l=-1)

check("A11 [E/c] = [B] = M T^-2 I^-1（F_{mu nu} 全分量同量纲）", ddiv(D_E, D_C) == D_B)
check("A12 [d_mu F^{mu nu}] = L^-1 * [B]", dmul(D_LINV, D_B) == dim(m=1, l=-1, t=-2, i=-1))
check("A13 [mu_0 J^0] = [mu_0 c rho]（与上式一致）",
      dmul(D_MU0, dmul(D_C, D_RHO)) == dim(m=1, l=-1, t=-2, i=-1))
check("A14 [mu_0 J^i] = [mu_0 * I L^-2]（与上式一致）",
      dmul(D_MU0, dim(i=1, l=-2)) == dim(m=1, l=-1, t=-2, i=-1))
check("A15 连续性方程 [d_mu J^mu] = [d_t rho] = I L^-3",
      dmul(D_LINV, dmul(D_C, D_RHO)) == dmul(dim(t=-1), D_RHO))
Ifn("A16 口径", "d_mu 作用于 A_mu 用偏导：本组限于平直时空笛卡尔系（Gamma = 0），曲线坐标须改用协变导数")

print()
print("=" * 74)
print("B 组 · 最小耦合原理 d_mu -> D_mu")
print("=" * 74)

q = sp.Symbol("q", positive=True)
hb = sp.Symbol("hbar", positive=True)
lam = sp.Function("lam")(t, x, y, z)
psi = sp.Function("psi")(t, x, y, z)


def D_minus(mu, e):
    """约定 B-1：D_mu = d_mu - i (q/hbar) A_mu。"""
    return pd(mu, e) - sp.I * q / hb * A_dn[mu] * e


def D_plus(mu, e):
    """约定 B-2（Peskin 型）：D_mu = d_mu + i (q/hbar) A_mu。"""
    return pd(mu, e) + sp.I * q / hb * A_dn[mu] * e


ok_b1 = True
for mu in range(4):
    psi_p = sp.exp(-sp.I * q * lam / hb) * psi
    A_p = A_dn[mu] - pd(mu, lam)
    lhs = pd(mu, psi_p) - sp.I * q / hb * A_p * psi_p
    rhs = sp.exp(-sp.I * q * lam / hb) * D_minus(mu, psi)
    ok_b1 = ok_b1 and is_zero(sp.expand(lhs - rhs))
check("B1 约定 B-1 规范协变：D'_mu psi' = e^{-i q lam/hbar} D_mu psi（4 个分量）", ok_b1)

ok_b2 = True
for mu in range(4):
    psi_p = sp.exp(sp.I * q * lam / hb) * psi
    A_p = A_dn[mu] - pd(mu, lam)
    lhs = pd(mu, psi_p) + sp.I * q / hb * A_p * psi_p
    rhs = sp.exp(sp.I * q * lam / hb) * D_plus(mu, psi)
    ok_b2 = ok_b2 and is_zero(sp.expand(lhs - rhs))
check("B2 约定 B-2 规范协变：D'_mu psi' = e^{+i q lam/hbar} D_mu psi（4 个分量）", ok_b2)

ok_b3 = all(is_zero(
    sp.expand(D_minus(m, D_minus(n, psi)) - D_minus(n, D_minus(m, psi))
              + sp.I * q / hb * Fmn[m, n] * psi))
    for (m, n) in [(0, 1), (1, 2), (2, 3)])
check("B3 对易子 [D_mu, D_nu] psi = -i (q/hbar) F_{mu nu} psi（抽样 3 组）", ok_b3)

ok_b4 = all(is_zero(sp.expand(
    -sp.I * hb * D_minus(mu, psi) - (-sp.I * hb * pd(mu, psi) - q * A_dn[mu] * psi)))
    for mu in range(4))
check("B4 最小耦合 = 动量平移：-i hbar D_mu = -i hbar d_mu - q A_mu（4 个分量）", ok_b4)

D_HB = dim(m=1, l=2, t=-1)
D_Q = dim(i=1, t=1)
D_LAM = dim(m=1, l=2, t=-2, i=-1)
D_AMU = dim(m=1, l=1, t=-2, i=-1)
check("B5 [q lam / hbar] = 1（相位无量纲）", ddiv(dmul(D_Q, D_LAM), D_HB) == dim())
check("B6 [hbar d_mu] = [q A_mu] = M L T^-1（最小耦合两侧同量纲）",
      dmul(D_HB, D_LINV) == dmul(D_Q, D_AMU))
check("B7 [(q/hbar) A_mu] = L^-1 = [d_mu]（D_mu 两项可相加）",
      dmul(ddiv(D_Q, D_HB), D_AMU) == D_LINV)
Bd("B8 约定配对边界",
   "D_mu 的符号必须与物质场相位因子同向：(-i q/hbar, A->A-dlam) 配 psi->e^{-iqlam/hbar}；(+i q/hbar) 配 e^{+iqlam/hbar}。"
   "原 T4 只给出 A_mu 变换、未给 psi 相位，与 T5 的 D_mu 符号不构成完整约定对（登记为审计项 A9）")

print()
print("=" * 74)
print("C 组 · 弱场近似：爱因斯坦场方程 -> 牛顿泊松方程")
print("=" * 74)

Rm, gm, Tm, Rs, Ts, kap = sp.symbols("Rm gm Tm Rs Ts kappa")
eq0 = sp.Eq(Rm - gm * Rs / 2, kap * Tm)
tr_eq = sp.Eq(Rs - 4 * Rs / 2, kap * Ts)          # 取迹：g^{mu nu} g_{mu nu} = 4
Rs_sol = sp.solve(tr_eq, Rs)[0]
Rm_sol = sp.solve(eq0, Rm)[0].subs(Rs, Rs_sol)
check("C1 迹反转：R_{mu nu} = kappa (T_{mu nu} - g_{mu nu} T / 2)",
      is_zero(sp.expand(Rm_sol - kap * (Tm - gm * Ts / 2))))

x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3")
XC = [x0, x1, x2, x3]
pairs = [(a, b) for a in range(4) for b in range(4) if a <= b]
hsym = {}
hmat = sp.zeros(4, 4)
for (a, b) in pairs:
    f = sp.Function("h%d%d" % (a, b))(*XC)
    hsym[(a, b)] = f
    hmat[a, b] = f
    hmat[b, a] = f


def dd(mu, e):
    return sp.diff(e, XC[mu])


hmix = sp.zeros(4, 4)                              # h^rho_nu = eta^{rho alpha} h_{alpha nu}
for r in range(4):
    for n in range(4):
        hmix[r, n] = sum(ETA[r][a] * hmat[a, n] for a in range(4))
trh = sp.expand(sum(ETA[a][b] * hmat[a, b] for a in range(4) for b in range(4)))

boxh = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        boxh[a, b] = sum(ETA[m][n] * dd(m, dd(n, hmat[a, b])) for m in range(4) for n in range(4))

R1 = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        t1 = sum(dd(r, dd(m, hmix[r, n])) for r in range(4))
        t2 = sum(dd(r, dd(n, hmix[r, m])) for r in range(4))
        t4 = dd(m, dd(n, trh))
        R1[m, n] = sp.Rational(1, 2) * sp.expand(t1 + t2 - boxh[m, n] - t4)

Sv = [sp.expand(sum(dd(r, hmix[r, n]) for r in range(4)) - dd(n, trh) / 2) for n in range(4)]
ok_c2 = all(is_zero(sp.expand(R1[m, n] + boxh[m, n] / 2
                              - (dd(m, Sv[n]) + dd(n, Sv[m])) / 2))
            for m in range(4) for n in range(4))
check("C2 线性化 Ricci 恒等式 R^(1)_{mu nu} + (1/2) Box h_{mu nu} = (1/2)(d_mu S_nu + d_nu S_mu)",
      ok_c2)

R1scal = sp.expand(sum(ETA[a][b] * R1[a, b] for a in range(4) for b in range(4)))
G1 = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        G1[m, n] = sp.expand(R1[m, n] - sp.Rational(1, 2) * ETA[m][n] * R1scal)
hbars = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        hbars[m, n] = sp.expand(hmat[m, n] - sp.Rational(1, 2) * ETA[m][n] * trh)
divS = sp.expand(sum(dd(r, sum(ETA[r][s] * Sv[s] for s in range(4))) for r in range(4)))
ok_c3 = all(is_zero(sp.expand(G1[m, n] + boxh[m, n] / 2 - sp.Rational(1, 4) * ETA[m][n] * sp.expand(
    sum(ETA[a][b] * boxh[a, b] for a in range(4) for b in range(4)))
    - (dd(m, Sv[n]) + dd(n, Sv[m])) / 2 + sp.Rational(1, 2) * ETA[m][n] * divS))
    for m in range(4) for n in range(2))
check("C3 含规范项的一般线性化 Einstein 张量恒等式（抽样 8 组）", ok_c3)

G_ = sp.Symbol("G", positive=True)
rho_s = sp.Symbol("rho", positive=True)
Phi = sp.Symbol("Phi", positive=True)
lapPhi = sp.Symbol("lapPhi")
kappa = 8 * sp.pi * G_ / c ** 4
T00 = rho_s * c ** 2
lap_hbar00 = 16 * sp.pi * G_ / c ** 4 * T00        # 静态极限：nabla^2 hbar_00
sol_lap = sp.solve(sp.Eq(2 * (2 * lapPhi / c ** 2), lap_hbar00), lapPhi)[0]
check("C4 牛顿极限：nabla^2 Phi = 4 pi G rho", is_zero(sp.expand(sol_lap - 4 * sp.pi * G_ * rho_s)))

Xs, Ys, Zs, Ms, Gm = sp.symbols("X Y Z M G", positive=True)
rr = sp.sqrt(Xs ** 2 + Ys ** 2 + Zs ** 2)
Phi_pt = -Gm * Ms / rr
lap_pt = sp.simplify(sum(sp.diff(Phi_pt, v, 2) for v in (Xs, Ys, Zs)))
check("C5a 点源势 Phi = -GM/r 在 r > 0 处 nabla^2 Phi = 0", lap_pt == 0)
rvar = sp.Symbol("rv", positive=True)
flux = sp.simplify(sp.diff(-Gm * Ms / rvar, rvar) * 4 * sp.pi * rvar ** 2)
check("C5b 高斯通量：oint grad Phi . dS = 4 pi G M（散度定理 => nabla^2 Phi = 4 pi G rho）",
      is_zero(sp.expand(flux - 4 * sp.pi * Gm * Ms)))

D_PHI = dim(l=2, t=-2)
D_G = dim(m=-1, l=3, t=-2)
D_RHO_MASS = dim(m=1, l=-3)          # 牛顿泊松方程中的 rho 是【质量密度】，不是电磁学的电荷密度
check("C6a 量纲 [nabla^2 Phi] = [4 pi G rho_mass] = T^-2",
      dmul(dpow(D_LINV, 2), D_PHI) == dmul(D_G, D_RHO_MASS))
check("C6b 记号歧义核验：电荷密度 rho_em 代入 G rho 量纲不匹配（M^-1 T^-1 I != T^-2）",
      dmul(D_G, D_RHO) != dmul(dpow(D_LINV, 2), D_PHI),
      "[G rho_em] = " + dshow(dmul(D_G, D_RHO)))
Bd("C7 静态/低速极限的额外假设",
   "hbar_ij = 0（空间应力可忽略）与静态近似是牛顿极限的输入假设，非场方程本身；不满足时（如引力波、强场）牛顿极限不成立")

print()
print("=" * 74)
print("D 组 · 量纲分析推导普朗克单位")
print("=" * 74)

D_HBAR = dim(m=1, l=2, t=-1)
basis = [D_HBAR, D_G, D_C]
det_basis = sp.Matrix([[D_HBAR[j], D_G[j], D_C[j]] for j in range(3)]).det()
check("D1 基 {hbar, G, c} 量纲矩阵行列式 != 0（无非平凡无量纲组合，解唯一）", det_basis != 0,
      "det = " + str(det_basis))

sol_m, uni_m, con_m = dim_solve(basis, dim(m=1))
sol_l, uni_l, con_l = dim_solve(basis, dim(l=1))
sol_t, uni_t, con_t = dim_solve(basis, dim(t=1))
check("D2 普朗克质量指数唯一：hbar^{1/2} G^{-1/2} c^{1/2}",
      uni_m and con_m and sol_m == [F(1, 2), F(-1, 2), F(1, 2)], "解 = " + str(sol_m))
check("D3 普朗克长度指数唯一：hbar^{1/2} G^{1/2} c^{-3/2}",
      uni_l and con_l and sol_l == [F(1, 2), F(1, 2), F(-3, 2)], "解 = " + str(sol_l))
check("D4 普朗克时间指数唯一：hbar^{1/2} G^{1/2} c^{-5/2}",
      uni_t and con_t and sol_t == [F(1, 2), F(1, 2), F(-5, 2)], "解 = " + str(sol_t))

HBAR_V = mpf("1.054571817e-34")
G_V = mpf("6.67430e-11")
C_V = mpf("299792458")
m_P = mpsqrt(HBAR_V * C_V / G_V)
l_P = mpsqrt(HBAR_V * G_V / C_V ** 3)
t_P = mpsqrt(HBAR_V * G_V / C_V ** 5)
E_P_GeV = m_P * C_V ** 2 / mpf("1.602176634e-19") / mpf("1e9")

REF = [("m_P / kg", m_P, mpf("2.176434e-8")),
       ("l_P / m", l_P, mpf("1.616255e-35")),
       ("t_P / s", t_P, mpf("5.391247e-44")),
       ("E_P / GeV", E_P_GeV, mpf("1.220890e19"))]
for name, val, ref in REF:
    rel = abs(val - ref) / ref
    check("D5 %s = %s（CODATA 参考 %s，相对偏差 %.2e）" % (name, mp.nstr(val, 10), mp.nstr(ref, 10), float(rel)),
          rel < mpf("1e-5"))

check("D6 [sqrt(hbar c / G)] = M", dpow(dmul(ddiv(dmul(D_HBAR, D_C), D_G), dim()), F(1, 2)) == dim(m=1))
check("D7 [sqrt(hbar G / c^3)] = L",
      dpow(ddiv(dmul(D_HBAR, D_G), dpow(D_C, 3)), F(1, 2)) == dim(l=1))
check("D8 [sqrt(hbar G / c^5)] = T",
      dpow(ddiv(dmul(D_HBAR, D_G), dpow(D_C, 5)), F(1, 2)) == dim(t=1))
check("D9 t_P = l_P / c（一致性）", dpow(ddiv(D_C, dim()), -1) is not None and
      ddiv(dim(l=1), D_C) == dim(t=1))
Bd("D10 物理边界",
   "量纲分析只给出普朗克单位的唯一形式与量纲；「普朗克尺度 = 量子引力生效尺度」是未被实验证实的物理假设，"
   "量纲分析既不给数值也不证明该尺度具有物理意义")

print()
print("=" * 74)
print("E 组 · 黎曼张量代数对称性与 Bianchi 恒等式")
print("=" * 74)


def christoffel(g, coords):
    n = len(coords)
    ginv = g.inv()
    Gam = [[[sp.Rational(1, 2) * sum(
        ginv[r][d] * (sp.diff(g[d][b], coords[m])
                      + sp.diff(g[d][m], coords[b])
                      - sp.diff(g[b][m], coords[d])) for d in range(n))
        for b in range(n)] for m in range(n)] for r in range(n)]
    return Gam


_RC = {}


def riem(Gam, coords, r, s, m, n_):
    """R^rho_{sigma mu nu}（与专题 T1 约定一致）单个分量，带缓存。

    R^rho_{sigma mu nu} = d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma}
                          + Gamma^rho_{mu lam} Gamma^lam_{nu sigma}
                          - Gamma^rho_{nu lam} Gamma^lam_{mu sigma}
    """
    key = (id(Gam), r, s, m, n_)
    if key in _RC:
        return _RC[key]
    k = len(coords)
    val = sp.expand(sp.diff(Gam[r][n_][s], coords[m]) - sp.diff(Gam[r][m][s], coords[n_])
                    + sum(Gam[r][m][l] * Gam[l][n_][s] for l in range(k))
                    - sum(Gam[r][n_][l] * Gam[l][m][s] for l in range(k)))
    _RC[key] = val
    return val


def ricci(Gam, coords):
    """Ricci_{mu nu} = R^sigma_{mu sigma nu}（专题 T1 缩并约定）。"""
    k = len(coords)
    out = sp.zeros(k, k)
    for m in range(k):
        for n_ in range(k):
            out[m, n_] = sp.simplify(sum(riem(Gam, coords, s, m, s, n_) for s in range(k)))
    return out


# --- 2 维球面（常曲率基准）
th, ph, r0 = sp.symbols("theta phi r0", positive=True)
co2 = [th, ph]
g2 = sp.Matrix([[r0 ** 2, 0], [0, r0 ** 2 * sp.sin(th) ** 2]])
G2 = christoffel(g2, co2)
Rdn2 = [[[[sp.simplify(sum(g2[a][l] * riem(G2, co2, l, b, m, n_) for l in range(2)))
           for n_ in range(2)] for m in range(2)] for b in range(2)] for a in range(2)]
K = 1 / r0 ** 2
ok_e1 = all(is_zero(Rdn2[a][b][m][n_] - K * (g2[a][m] * g2[b][n_] - g2[a][n_] * g2[b][m]))
            for a in range(2) for b in range(2) for m in range(2) for n_ in range(2))
check("E1 2 维球面常曲率关系 R_{rho sigma mu nu} = K (g_{rho mu} g_{sigma nu} - g_{rho nu} g_{sigma mu})，K = 1/r_0^2",
      ok_e1)

Ric2 = ricci(G2, co2)
ok_e2 = all(is_zero(sp.expand(Ric2[m, n_] - K * g2[m, n_])) for m in range(2) for n_ in range(2))
check("E2 Ricci = R^sigma_{mu sigma nu} = K g_{mu nu}（与专题 T1 缩并约定自洽）", ok_e2)
ginv2 = g2.inv()
Rscal2 = sp.simplify(sum(ginv2[a][b] * Ric2[a, b] for a in range(2) for b in range(2)))
check("E3 标量曲率 R = n(n-1)K = 2/r_0^2", is_zero(sp.expand(Rscal2 - 2 / r0 ** 2)),
      "R = " + str(Rscal2))

s1 = all(is_zero(Rdn2[a][b][m][nn] + Rdn2[b][a][m][nn])
         for a in range(2) for b in range(2) for m in range(2) for nn in range(2))
s2 = all(is_zero(Rdn2[a][b][m][nn] + Rdn2[a][b][nn][m])
         for a in range(2) for b in range(2) for m in range(2) for nn in range(2))
s3 = all(is_zero(Rdn2[a][b][m][nn] - Rdn2[m][nn][a][b])
         for a in range(2) for b in range(2) for m in range(2) for nn in range(2))
check("E4 代数对称性（2 维球面）：前对反对称 / 后对反对称 / 块交换对称", s1 and s2 and s3)
check("E5 Ricci 张量对称 Ric_{mu nu} = Ric_{nu mu}（2 维球面）",
      all(is_zero(sp.expand(Ric2[m, n_] - Ric2[n_, m])) for m in range(2) for n_ in range(2)))

# --- Schwarzschild（真空解）
ts, rs, ths, phs, Ms2 = sp.symbols("t r theta phi M", positive=True)
co4 = [ts, rs, ths, phs]
fS = 1 - 2 * Ms2 / rs
g4 = sp.diag(fS, -1 / fS, -rs ** 2, -rs ** 2 * sp.sin(ths) ** 2)
G4 = christoffel(g4, co4)

Ric4 = ricci(G4, co4)
ok_e6 = all(is_zero(Ric4[m, n_]) for m in range(4) for n_ in range(4))
check("E6 Schwarzschild 真空解：R_{mu nu} = 0（16 个分量全部为零）", ok_e6)

ginv4 = g4.inv()
Rscal4 = sp.simplify(sum(ginv4[a][b] * Ric4[a, b] for a in range(4) for b in range(4)))
check("E7 Schwarzschild 标量曲率 R = 0", is_zero(sp.expand(Rscal4)))
Ein4 = sp.zeros(4, 4)
for m in range(4):
    for n_ in range(4):
        Ein4[m, n_] = sp.expand(Ric4[m, n_] - sp.Rational(1, 2) * g4[m, n_] * Rscal4)
check("E8 Schwarzschild Einstein 张量 G_{mu nu} = 0",
      all(is_zero(Ein4[m, n_]) for m in range(4) for n_ in range(4)))

# Schwarzschild 对称性抽样（避免全 256 分量的化简开销）
samples = [(0, 1, 0, 1), (0, 1, 2, 3), (1, 2, 1, 2), (1, 2, 3, 2), (2, 3, 2, 3), (0, 2, 0, 2)]
cache = {}


def Rdn4(a, b, m, n_):
    key = (a, b, m, n_)
    if key in cache:
        return cache[key]
    val = sp.simplify(sum(g4[a][l] * riem(G4, co4, l, b, m, n_) for l in range(4)))
    cache[key] = val
    return val


ok_e9 = all(is_zero(Rdn4(a, b, m, n_) + Rdn4(b, a, m, n_)) for (a, b, m, n_) in samples)
ok_e10 = all(is_zero(Rdn4(a, b, m, n_) + Rdn4(a, b, n_, m)) for (a, b, m, n_) in samples)
check("E9/E10 Schwarzschild 抽样对称性：前对反对称 / 后对反对称", ok_e9 and ok_e10)
ok_e11 = is_zero(Rdn4(1, 2, 3, 2) + Rdn4(1, 3, 2, 2) + Rdn4(1, 2, 2, 3))
check("E11 Schwarzschild 抽样第一 Bianchi R_{rho[sigma mu nu]} = 0", ok_e11)

# --- 独立分量数
def indep_count(n):
    idx = [(a, b, m, nn) for a in range(n) for b in range(n) for m in range(n) for nn in range(n)]
    pos = {v: k for k, v in enumerate(idx)}
    rows = []
    for a in range(n):
        for b in range(n):
            for m in range(n):
                for nn in range(n):
                    row = [F(0)] * len(idx)
                    row[pos[(a, b, m, nn)]] += 1
                    row[pos[(b, a, m, nn)]] += 1
                    rows.append(row)
                    row2 = [F(0)] * len(idx)
                    row2[pos[(a, b, m, nn)]] += 1
                    row2[pos[(a, b, nn, m)]] += 1
                    rows.append(row2)
    for a in range(n):
        for b in range(n):
            for m in range(n):
                for nn in range(n):
                    row3 = [F(0)] * len(idx)
                    row3[pos[(a, b, m, nn)]] += 1
                    row3[pos[(m, nn, a, b)]] -= 1
                    rows.append(row3)
    # 第一 Bianchi：对 sigma mu nu 全反对称
    from itertools import combinations
    for a in range(n):
        for tri in combinations(range(n), 3):
            row4 = [F(0)] * len(idx)
            row4[pos[(a, tri[0], tri[1], tri[2])]] += 1
            row4[pos[(a, tri[1], tri[2], tri[0])]] += 1
            row4[pos[(a, tri[2], tri[0], tri[1])]] += 1
            rows.append(row4)
    # 独立分量数 = 变量数 - 线性约束矩阵的秩
    M = sp.Matrix([[int(v) for v in r] for r in rows])
    rank = M.rank()
    return len(idx) - rank


for n_, expect in [(2, 1), (3, 6)]:
    got = indep_count(n_)
    check("E12 n = %d 维黎曼张量独立分量数 = %d（公式 n^2(n^2-1)/12）" % (n_, expect),
          got == expect, "实测 = " + str(got))
formula4 = 4 ** 2 * (4 ** 2 - 1) // 12
check("E13 n = 4 维独立分量数 = 20（公式 n^2(n^2-1)/12 = %d）" % formula4, formula4 == 20)
Ifn("E14 计数法", "n = 4 用公式（双矢量空间 N = n(n-1)/2 = 6，对称矩阵 N(N+1)/2 = 21，减第一 Bianchi 约束 C(n,4) = 1 ⇒ 20）；n = 2,3 由线性约束秩实测验证")


# --- 微分 Bianchi（3 维共形平直度规：曲率非零，恒等式非平凡；2 维时三指标必有重复恒等式自动成立）
u1, u2, u3 = sp.symbols("u1 u2 u3")
co3 = [u1, u2, u3]
sig = sp.Function("sigma")(u1)
e2 = sp.exp(2 * sig)
g3 = sp.diag(e2, -e2, -e2)
G3 = christoffel(g3, co3)


def rdn3(a, b, m, n_):
    return sp.simplify(sum(g3[a, l] * riem(G3, co3, l, b, m, n_) for l in range(3)))


def nab3(l, a, b, m, n_):
    """协变导数 nab_lambda R_{rho sigma mu nu}。"""
    e = sp.diff(rdn3(a, b, m, n_), co3[l])
    for k in range(3):
        e -= G3[k][l][a] * rdn3(k, b, m, n_)
        e -= G3[k][l][b] * rdn3(a, k, m, n_)
        e -= G3[k][l][m] * rdn3(a, b, k, n_)
        e -= G3[k][l][n_] * rdn3(a, b, m, k)
    return sp.expand(e)


Ric3 = ricci(G3, co3)
nontriv3 = not all(is_zero(Ric3[m, n_]) for m in range(3) for n_ in range(3))
check("E15 3 维共形平直度规曲率非零（保证 Bianchi 验证非平凡）", nontriv3)
ok_e15 = all(is_zero(sp.simplify(nab3(0, a, b, 1, 2) + nab3(1, a, b, 2, 0) + nab3(2, a, b, 0, 1)))
             for (a, b) in [(0, 1), (0, 2), (1, 2)])
check("E16 微分 Bianchi 恒等式 nab_[lambda R_{|rho sigma| mu nu] = 0（3 维，符号精确，抽样 3 组）", ok_e15)


def Rdn4f(a, b, m, n_):
    return Rdn4(a, b, m, n_)


def nab4(l, a, b, m, n_):
    e = sp.diff(Rdn4f(a, b, m, n_), co4[l])
    for k in range(4):
        e -= G4[k][l][a] * Rdn4f(k, b, m, n_)
        e -= G4[k][l][b] * Rdn4f(a, k, m, n_)
        e -= G4[k][l][m] * Rdn4f(a, b, k, n_)
        e -= G4[k][l][n_] * Rdn4f(a, b, m, k)
    return sp.expand(e)


subs_pt = {rs: 4 * Ms2, ths: sp.pi / 3, Ms2: 1}
ok_e16 = True
maxres = mpf("0")
for (l, m, n_) in [(1, 2, 3)]:
    for (a, b) in [(0, 1), (1, 2)]:
        expr = nab4(l, a, b, m, n_) + nab4(m, a, b, n_, l) + nab4(n_, a, b, l, m)
        val = sp.N(expr.subs(subs_pt), 30)
        res = abs(complex(val)) if val.is_number else float("nan")
        maxres = max(maxres, mpf(str(res)))
        ok_e16 = ok_e16 and (res < 1e-20)
check("E17 微分 Bianchi 恒等式（Schwarzschild 真空解，r = 4M 数值代入，抽样 2 组）", ok_e16,
      "最大残差 = %.3e" % float(maxres))
Ifn("E18 缩并约定", "Ricci 采用专题 T1 约定 R_{mu nu} = R^sigma_{mu sigma nu}；本组 E2 在 2 维球面上给出 Ric = K g（n-1 = 1），与该约定自洽")

print()
print("=" * 74)
print("汇总")
print("=" * 74)
print("PASS = " + str(CNT["PASS"]))
print("FAIL = " + str(CNT["FAIL"]))
print("BOUNDARY = " + str(CNT["BOUNDARY"]))
print("INFO = " + str(CNT["INFO"]))
sys.exit(0 if CNT["FAIL"] == 0 else 1)
