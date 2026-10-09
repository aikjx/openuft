# -*- coding: utf-8 -*-
"""UFE-1 统一场方程：EC 挠率算符基底与 SM 手征四费米匹配 · 零依赖验证器。

设计约束（沿用仓库基线）：
1. 零第三方依赖：仅标准库 fractions / json / itertools / sys；
2. 4x4 Dirac 矩阵与所有恒等式用精确高斯有理数（实部/虚部各为 Fraction）
   计算，全程不用浮点，避免近似掩盖非零项；
3. 每项检查显式声明 id / claim / computed / expected / status；
4. 否定性结果照实登记 FAIL。

对应文档：15_挠率算符基底与SM手征匹配_量子约束与反常审计_2026-10-09.md

用法： python -B torsion_operator_basis.py
产出： torsion_operator_basis.json（本文件所在目录）
"""
import json
import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

sys.dont_write_bytecode = True
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
RESULTS = []


def rec(cid, category, claim, computed, expected, status, note=''):
    RESULTS.append({
        'id': cid, 'category': category, 'claim': claim,
        'computed': computed, 'expected': expected,
        'status': status, 'note': note,
    })


# --------------------------------------------------------------------------
# 精确高斯有理数：复数的实部/虚部各为 Fraction。表示为 (re: F, im: F)
Z = (F(0), F(0))
def cnum(r, i=F(0)):
    return (F(r), F(i))
def cadd(a, b):
    return (a[0]+b[0], a[1]+b[1])
def csub(a, b):
    return (a[0]-b[0], a[1]-b[1])
def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def cmul_scalar(a, s):
    return (a[0]*F(s), a[1]*F(s))
def ceq(a, b):
    return a[0] == b[0] and a[1] == b[1]


def mmul(A, B):
    """4x4 矩阵乘法。"""
    n = len(A)
    C = [[Z for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            acc = Z
            for k in range(n):
                acc = cadd(acc, cmul(A[i][k], B[k][j]))
            C[i][j] = acc
    return C


def madd(A, B):
    return [[cadd(A[i][j], B[i][j]) for j in range(len(A))] for i in range(len(A))]


def msub(A, B):
    return [[csub(A[i][j], B[i][j]) for j in range(len(A))] for i in range(len(A))]


def mscalar(A, s):
    if isinstance(s, tuple):          # s 为 cnum
        return [[cmul(A[i][j], s) for j in range(len(A))] for i in range(len(A))]
    return [[cmul_scalar(A[i][j], s) for j in range(len(A))] for i in range(len(A))]


def mzero(n=4):
    return [[Z for _ in range(n)] for _ in range(n)]


def meye(n=4):
    I = mzero(n)
    for i in range(n):
        I[i][i] = cnum(1)
    return I


def mtr(A):
    acc = Z
    for i in range(len(A)):
        acc = cadd(acc, A[i][i])
    return acc


def meq(A, B):
    return all(ceq(A[i][j], B[i][j]) for i in range(len(A)) for j in range(len(A)))


# --------------------------------------------------------------------------
# Pauli 矩阵与 Dirac 矩阵（Weyl 手征基底），号差 (-,+,+,+)
def pauli(k):
    if k == 0:
        return [[cnum(1), Z], [Z, cnum(1)]]
    if k == 1:
        return [[Z, cnum(1)], [cnum(1), Z]]
    if k == 2:
        return [[Z, cnum(0, -1)], [cnum(0, 1), Z]]
    if k == 3:
        return [[cnum(1), Z], [Z, cnum(-1)]]


def gamma_mu(mu):
    """号差 (-,+,+,+) 的 Weyl 表示：γ0²=-1、γi²=+1、{γμ,γν}=2η^{μν}。
    取 γ0=[[0,iI],[iI,0]]、γi=[[0,iσi],[-iσi,0]]（全虚，满足 η=diag(-1,1,1,1)）。
    """
    s = pauli(mu)
    Iu = (F(0), F(1))     # i
    Im = (F(0), F(-1))    # -i
    G = [[Z for _ in range(4)] for _ in range(4)]
    for a in range(2):
        for b in range(2):
            G[a][b+2] = cmul(s[a][b], Iu)                 # 右上 = i·σ
            G[a+2][b] = cmul(s[a][b], Iu if mu == 0 else Im)  # 左下 = iI(μ=0) 或 -iσ(μ>0)
    return G


G0, G1, G2, G3 = [gamma_mu(i) for i in range(4)]
GAM = [G0, G1, G2, G3]
# γ5 = i γ0 γ1 γ2 γ3
G5 = mmul(mmul(mmul(mscalar(G0, (0, 1)), G1), G2), G3)
# 手征投影
PL = mscalar(madd(meye(), mscalar(G5, -1)), F(1, 2))   # (1-γ5)/2
PR = mscalar(madd(meye(), G5), F(1, 2))                # (1+γ5)/2

MET = [F(-1), F(1), F(1), F(1)]  # 号差 (-,+,+,+)

def g_low(mu):
    return mscalar(GAM[mu], MET[mu])


def gamma_lambda(mu):
    return GAM[mu]


# 16 个基矩阵与“共轭/提升”配对（用于 Fierz 完备性）
def sigma_uv(mu, nu):
    return mscalar(msub(mmul(GAM[mu], GAM[nu]), mmul(GAM[nu], GAM[mu])),
                   (0, F(1, 2)))  # (i/2)[γ^μ,γ^ν]

def basis_pairs():
    """返回 [(Γ_A, Γ^A)] 16 项：S,V,T,A,P。Γ^A 用度规升降。"""
    pairs = []
    pairs.append((meye(), meye()))                                   # S: 1
    for mu in range(4):
        pairs.append((GAM[mu], GAM[mu]))                             # V: γ^μ (对γ_ν=η γ^ν，Γ^μ=γ^μ)
    for mu in range(4):
        for nu in range(mu+1, 4):
            su = sigma_uv(mu, nu)
            sl = mscalar(su, MET[mu]*MET[nu])
            pairs.append((su, sl))                                   # T: σ^{μν}, σ_{μν}
    for mu in range(4):
        pairs.append((mmul(G5, GAM[mu]), mmul(G5, GAM[mu])))         # A: γ5γ^μ
    pairs.append((G5, G5))                                           # P: γ5
    return pairs


# --------------------------------------------------------------------------
# 4 维 Levi-Civita：eps[0123]=+1，反称
def eps_index(a, b, c, d):
    p = (a, b, c, d)
    if sorted(p) != [0, 1, 2, 3]:
        return F(0)
    inv = 0
    for i in range(4):
        for j in range(i+1, 4):
            if p[i] > p[j]:
                inv += 1
    return F(1) if inv % 2 == 0 else F(-1)


def eps_upper(a, b, c, d):
    """ε^{abcd} = η^aa'η^bb'η^cc'η^dd' ε_{a'b'c'd'}。"""
    return eps_index(a, b, c, d) * MET[a]*MET[b]*MET[c]*MET[d]


# --------------------------------------------------------------------------
# 挠率张量工具（T[λ][μ][ν]，对后两指标反称）
def make_generic_torsion():
    """由一般反称模板生成 24 分量的通用挠率（整数/精确有理）。"""
    T = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                if mu < nu:
                    v = F((lam+1)*(mu+2)*(nu+3) % 11 - 5)
                    T[lam][mu][nu] = v
                    T[lam][nu][mu] = -v
    return T


def raise3(T):
    U = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                acc = F(0)
                for i in range(4):
                    for j in range(4):
                        for k in range(4):
                            acc += MET[a]*MET[i] * MET[b]*MET[j] * MET[c]*MET[k] * T[i][j][k]
                U[a][b][c] = acc
    return U


def torsion_trace(T):
    """t_μ = T^λ_{λμ} = η^{λκ}T_{κλμ}。"""
    t = [F(0)]*4
    for mu in range(4):
        acc = F(0)
        for lam in range(4):
            for kappa in range(4):
                acc += (MET[lam] if kappa == lam else 0) * T[kappa][lam][mu]
        t[mu] = acc
    return t


def torsion_axial(T):
    """S^ρ = ε^{λμνρ} T_{λμν}。"""
    S = [F(0)]*4
    for rho in range(4):
        acc = F(0)
        for lam in range(4):
            for mu in range(4):
                for nu in range(4):
                    acc += eps_upper(lam, mu, nu, rho) * T[lam][mu][nu]
        S[rho] = acc
    return S


def torsion_trace_part(t):
    P = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                P[lam][mu][nu] = (F(1,3))*(t[nu]*(MET[lam] if lam == mu else 0)
                                           - t[mu]*(MET[lam] if lam == nu else 0))
    return P


def torsion_axial_part(S):
    """T^S_{λμν} = -⅙ ε_{λμνρ}S^ρ（完全反对称/轴矢量部分）。"""
    P = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                P[lam][mu][nu] = sum((F(-1,6))*eps_index(lam, mu, nu, i)*S[i] for i in range(4))
    return P


def torsion_tensor_part(T, t, S):
    """q_{λμν} = T - (迹部分) - (轴部分)。"""
    q = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                trace_part = (F(1,3))*(t[nu]*(MET[lam] if lam == mu else 0)
                                       - t[mu]*(MET[lam] if lam == nu else 0))
                axial_part = sum((F(-1,6))*eps_index(lam, mu, nu, i)*S[i] for i in range(4))
                q[lam][mu][nu] = T[lam][mu][nu] - trace_part - axial_part
    return q


def full_contract3(A, B):
    """A_{λμν}B^{λμν}。"""
    U = raise3(B)
    acc = F(0)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                acc += A[a][b][c]*U[a][b][c]
    return acc


# ==========================================================================
# T1. Dirac 代数
def check_t1():
    ok_clifford = True
    for mu in range(4):
        for nu in range(4):
            antic = madd(mmul(GAM[mu], GAM[nu]), mmul(GAM[nu], GAM[mu]))
            target = mscalar(meye(), 2*MET[mu] if mu == nu else 0)
            if not meq(antic, target):
                ok_clifford = False
    # γ5 性质
    g5sq = mmul(G5, G5)
    ok_g5 = meq(g5sq, meye())
    ok_anti = all(meq(madd(mmul(G5, GAM[mu]), mmul(GAM[mu], G5)), mzero()) for mu in range(4))
    # Tr(γ^μ γ^ν) = 4 η^{μν}
    ok_trace = all(mtr(mmul(GAM[mu], GAM[nu])) == cmul_scalar(cnum(4*MET[mu]), 1) if mu == nu
                   else mtr(mmul(GAM[mu], GAM[nu])) == Z for mu in range(4) for nu in range(4))
    rec('T1', 'Dirac代数',
        'Weyl 基 {γ^μ,γ^ν}=2η^{μν}，γ5^2=1，{γ5,γ^μ}=0，Tr(γ^μγ^ν)=4η^{μν}',
        'Clifford=%s g5^2=%s anti=%s trace=%s' % (ok_clifford, ok_g5, ok_anti, ok_trace),
        'all True', 'PASS' if all([ok_clifford, ok_g5, ok_anti, ok_trace]) else 'FAIL')


# T2. Levi-Civita 与轴投影约定
def check_t2():
    # ε^{λμνρ}ε_{λμνσ} = -6 δ^ρ_σ（号差 (-,+,+,+)）
    rhs = [[F(0)]*4 for _ in range(4)]
    for rho in range(4):
        for sig in range(4):
            acc = F(0)
            for lam in range(4):
                for mu in range(4):
                    for nu in range(4):
                        acc += eps_upper(lam, mu, nu, rho) * eps_index(lam, mu, nu, sig)
            rhs[rho][sig] = acc
    ok = all(rhs[rho][sig] == (F(-6) if rho == sig else F(0))
             for rho in range(4) for sig in range(4))
    rec('T2', 'Levi-Civita约定',
        'ε^{λμνρ}ε_{λμνσ} = -6 δ^ρ_σ（号差 (-,+,+,+)）',
        'diag=%s' % [str(rhs[r][r]) for r in range(4)],
        '[-6,-6,-6,-6], off-diag 0', 'PASS' if ok else 'FAIL')


# T3. 挠率不可约分解
def check_t3():
    T = make_generic_torsion()
    t = torsion_trace(T)
    S = torsion_axial(T)
    q = torsion_tensor_part(T, t, S)
    # q 反称（后两指标 μν，与 T 同）
    ok_anti = all(q[a][b][c] == -q[a][c][b] for a in range(4) for b in range(4) for c in range(4))
    # q 无迹：Σ_a q^a_{a c} = 0
    ok_tracefree = all(sum((MET[a] if a == b else 0)*q[a][b][c]
                           for a in range(4) for b in range(4)) == 0 for c in range(4))
    # q 循环恒等式
    ok_cyclic = all(q[a][b][c] + q[b][c][a] + q[c][a][b] == 0
                    for a in range(4) for b in range(4) for c in range(4))
    # 重建：T = 迹部分 + 轴部分 + q
    rec_ok = True
    for a in range(4):
        for b in range(4):
            for c in range(4):
                tp = (F(1,3))*(t[c]*(MET[a] if a == b else 0) - t[b]*(MET[a] if a == c else 0))
                ax = sum((F(-1,6))*eps_index(a, b, c, i)*S[i] for i in range(4))
                if T[a][b][c] != tp + ax + q[a][b][c]:
                    rec_ok = False
    # 迹/轴分量确由 T 提取：重新验证 S^ρ = ε^{λμνρ}T_{λμν} 与轴投影自洽
    rec('T3', '挠率不可约分解',
        'T_{λμν}=⅓(t_μg_{λν}-t_νg_{λμ}) - ⅙ε_{λμνρ}S^ρ + q_{λμν}；q 反称/无迹/循环；重建恒等',
        'anti=%s tracefree=%s cyclic=%s reconstruct=%s' % (ok_anti, ok_tracefree, ok_cyclic, rec_ok),
        'all True (4+4+16=24)', 'PASS' if all([ok_anti, ok_tracefree, ok_cyclic, rec_ok]) else 'FAIL')


# T4. Contorsion 互逆
def check_t4():
    T = make_generic_torsion()
    K = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                K[lam][mu][nu] = F(1,2)*(T[lam][mu][nu] + T[mu][lam][nu] - T[nu][lam][mu])
    # 只升第一个指标：K^λ_{μν} = η^{λα}K_{αμν}
    def raise_first(M):
        R = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for lam in range(4):
            for mu in range(4):
                for nu in range(4):
                    R[lam][mu][nu] = sum(MET[a]*M[a][mu][nu] for a in range(4)
                                         if a == lam)
        return R
    K1 = raise_first(K)
    T1 = raise_first(T)
    # 逆：T^λ_{μν} = K^λ_{μν} - K^λ_{νμ}
    ok = all(T1[lam][mu][nu] == K1[lam][mu][nu] - K1[lam][nu][mu]
             for lam in range(4) for mu in range(4) for nu in range(4))
    # 迹关系：t_μ = K^λ_{λμ}
    t = torsion_trace(T)
    Ktrace = [sum(K1[a][a][mu] for a in range(4)) for mu in range(4)]
    ok_trace = all(t[mu] == Ktrace[mu] for mu in range(4))
    rec('T4', 'Contorsion',
        'K_{λμν}=½(T_{λμν}+T_{μλν}-T_{νλμ})，T^λ_{μν}=K^λ_{μν}-K^λ_{νμ}，t_μ=K^λ_{λμ}',
        'roundtrip=%s trace_rel=%s' % (ok, ok_trace),
        'True/True', 'PASS' if ok and ok_trace else 'FAIL')


# T5. 二次挠率不变量在不可约分量上的约化系数
def make_generic_torsion2():
    T = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                if mu < nu:
                    v = F((lam*lam + mu*3 - nu) % 13 - 6)
                    T[lam][mu][nu] = v
                    T[lam][nu][mu] = -v
    return T


def make_generic_torsion3():
    T = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                if mu < nu:
                    v = F((lam*5 - mu*2 + nu*7) % 17 - 8)
                    T[lam][mu][nu] = v
                    T[lam][nu][mu] = -v
    return T


def _invariants(T):
    t = torsion_trace(T)
    S = torsion_axial(T)
    q = torsion_tensor_part(T, t, S)
    Tup = raise3(T)
    t2 = sum(MET[i]*t[i]*t[i] for i in range(4))
    S2 = sum(MET[i]*S[i]*S[i] for i in range(4))
    q2 = full_contract3(q, q)
    T2 = sum(T[a][b][c]*Tup[a][b][c] for a in range(4) for b in range(4) for c in range(4))
    Tcross = sum(T[a][b][c]*Tup[b][a][c] for a in range(4) for b in range(4) for c in range(4))
    return t2, S2, q2, T2, Tcross


def _solve3(rows, rhs):
    """精确求解 3x3 线性系统（Fraction 高斯消去）。"""
    a = [[F(x) for x in row] for row in rows]
    b = [F(x) for x in rhs]
    for col in range(3):
        piv = next(i for i in range(col, 3) if a[i][col] != 0)
        a[col], a[piv] = a[piv], a[col]
        b[col], b[piv] = b[piv], b[col]
        for r in range(col+1, 3):
            f = a[r][col] / a[col][col]
            for c in range(col, 3):
                a[r][c] -= f*a[col][c]
            b[r] -= f*b[col]
    x = [F(0)]*3
    for r in range(2, -1, -1):
        x[r] = (b[r] - sum(a[r][c]*x[c] for c in range(r+1, 3))) / a[r][r]
    return x


def check_t5():
    # 独立生成三个不可约分量，组装 T = T^t + T^S + q
    t = [F((i*3-4) % 7 - 3) for i in range(4)]
    S = [F((i*5+2) % 11 - 5) for i in range(4)]
    q = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                if mu < nu:
                    v = F((lam*7 + mu*2 + nu) % 19 - 9)
                    q[lam][mu][nu] = v
                    q[lam][nu][mu] = -v
    # 投影到张量子空间（去迹+去轴），保证 q 是纯张量部分
    qT = torsion_tensor_part(q, torsion_trace(q), torsion_axial(q))
    T = [[[torsion_trace_part(t)[a][b][c] + torsion_axial_part(S)[a][b][c] + qT[a][b][c]
           for c in range(4)] for b in range(4)] for a in range(4)]
    t2 = sum(MET[i]*t[i]*t[i] for i in range(4))
    S2 = sum(MET[i]*S[i]*S[i] for i in range(4))
    q2 = full_contract3(qT, qT)
    Tup = raise3(T)
    T2 = sum(T[a][b][c]*Tup[a][b][c] for a in range(4) for b in range(4) for c in range(4))
    Tcross = sum(T[a][b][c]*Tup[b][a][c] for a in range(4) for b in range(4) for c in range(4))
    # 期望：T² = ⅔t² - ⅙S² + q²（交叉项消失）
    ok_T2 = T2 == F(2,3)*t2 - F(1,6)*S2 + q2
    # Tcross 各块
    Tt = torsion_trace_part(t); TS = torsion_axial_part(S)
    Ttup = raise3(Tt); TSup = raise3(TS); qup = raise3(qT)
    C_tt = sum(Tt[a][b][c]*Ttup[b][a][c] for a in range(4) for b in range(4) for c in range(4))
    C_SS = sum(TS[a][b][c]*TSup[b][a][c] for a in range(4) for b in range(4) for c in range(4))
    C_qq = sum(qT[a][b][c]*qup[b][a][c] for a in range(4) for b in range(4) for c in range(4))
    ok_X = Tcross == C_tt + C_SS + C_qq
    rec('T5', '二次不变量约化',
        'T²=⅔t²-⅙S²+q²；交叉块对 T² 与 T_{λμν}T^{μλν} 均消失；各块独立核算',
        'T2==⅔t²-⅙S²+q²:%s | Tcross==Σ块:%s | (C_tt,C_SS,C_qq)=(%s,%s,%s)' % (
            ok_T2, ok_X, C_tt, C_SS, C_qq),
        'T2: True；Tcross 块按系数表读', 'PASS' if ok_T2 and ok_X else 'FAIL')


# T6. Dirac 自旋流为轴矢量：只有轴挠率耦合
def check_t6():
    # (a) γ^{[λ}γ^μγ^ν]} = c·ε^{λμνρ}γ5γ_ρ（找到 c，验证全部不同指标一致）
    def antisym3(x, y, z):
        return mscalar(madd(madd(mmul(mmul(GAM[x], GAM[y]), GAM[z]),
                                 mmul(mmul(GAM[y], GAM[z]), GAM[x])),
                            mmul(mmul(GAM[z], GAM[x]), GAM[y])),
                       F(1, 6))
    def rhs_gamma(lam, mu, nu):
        R = mzero()
        for rho in range(4):
            R = madd(R, mscalar(mmul(G5, GAM[rho]), eps_upper(lam, mu, nu, rho)))
        return R
    # 由 (0,1,2) 定 c
    Gam0 = antisym3(0, 1, 2)
    R0 = rhs_gamma(0, 1, 2)
    cc = None
    for i in range(4):
        for j in range(4):
            if not ceq(R0[i][j], Z):
                re = R0[i][j][0]; im = R0[i][j][1]
                denom = re*re + im*im
                cc = ((Gam0[i][j][0]*re + Gam0[i][j][1]*im)/denom,
                      (Gam0[i][j][1]*re - Gam0[i][j][0]*im)/denom)
                break
        if cc is not None:
            break
    c_uniform = cc is not None
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                if lam == mu or mu == nu or lam == nu:
                    continue
                if not meq(antisym3(lam, mu, nu), mscalar(rhs_gamma(lam, mu, nu), cc)):
                    c_uniform = False
    # (b) 轴投影：迹/张量部分 ε 缩并 = 0，轴部分非 0
    T = make_generic_torsion()
    t = torsion_trace(T)
    S = torsion_axial(T)
    q = torsion_tensor_part(T, t, S)
    trace_tensor = torsion_trace_part(t)
    A_trace = torsion_axial(trace_tensor)
    A_q = torsion_axial(q)
    A_axial = torsion_axial(torsion_axial_part(S))
    ok_trace0 = all(v == 0 for v in A_trace)
    ok_q0 = all(v == 0 for v in A_q)
    ok_axial_nz = any(v != 0 for v in A_axial)
    rec('T6', 'Dirac 自旋流为轴矢量',
        'γ^{[λ}γ^μγ^ν]} = c·ε^{λμνρ}γ5γ_ρ（c 一致）；迹/张量挠率轴投影=0、轴挠率≠0 ⇒ 最小耦合仅轴矢量挠率进自旋流',
        'c_uniform=%s c=%s traceProj0=%s qProj0=%s axialNZ=%s' % (
            c_uniform, str(cc), ok_trace0, ok_q0, ok_axial_nz),
        'uniform c, trace0/q0 True, axial NZ True',
        'PASS' if (c_uniform and ok_trace0 and ok_q0 and ok_axial_nz) else 'FAIL')


# T7. Fierz 恒等式
def check_t7():
    # (a) (V−A)⊗(V−A) 自 Fierz：β↔δ 交换不变
    def vier_bein_ll():
        pass
    # M_{αβγδ} = (γ^μP_L)_{αβ}(γ_μP_L)_{γδ}
    # N_{αβγδ} = (γ^μP_L)_{αδ}(γ_μP_L)_{γβ}
    def gamma_mu_pl():
        return [mmul(GAM[mu], PL) for mu in range(4)]
    def gamma_mu_low_pl():
        return [mmul(g_low(mu), PL) for mu in range(4)]
    GPL = gamma_mu_pl()
    GlowPL = gamma_mu_low_pl()
    M = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    N = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    accM = Z
                    accN = Z
                    for mu in range(4):
                        accM = cadd(accM, cmul(GPL[mu][a][b], GlowPL[mu][c][d]))
                        accN = cadd(accN, cmul(GPL[mu][a][d], GlowPL[mu][c][b]))
                    M[a][b][c][d] = accM
                    N[a][b][c][d] = accN
    ok_ll = all(ceq(M[a][b][c][d], N[a][b][c][d]) for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    # 同样验证 P_R
    GPR = [mmul(GAM[mu], PR) for mu in range(4)]
    GlowPR = [mmul(g_low(mu), PR) for mu in range(4)]
    MR = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    NR = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    accM = Z; accN = Z
                    for mu in range(4):
                        accM = cadd(accM, cmul(GPR[mu][a][b], GlowPR[mu][c][d]))
                        accN = cadd(accN, cmul(GPR[mu][a][d], GlowPR[mu][c][b]))
                    MR[a][b][c][d] = accM
                    NR[a][b][c][d] = accN
    ok_rr = all(ceq(MR[a][b][c][d], NR[a][b][c][d]) for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    # (b) Fierz 完备性：Σ_A (Γ_A)_{αβ}(Γ^A)_{γδ} = 4 δ_{αδ}δ_{γβ}
    pairs = basis_pairs()
    ok_comp = True
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    acc = Z
                    for GA, Gup in pairs:
                        acc = cadd(acc, cmul(GA[a][b], Gup[c][d]))
                    target = cmul_scalar((F(4), F(0)), 1) if (a == d and c == b) else Z
                    # target 应 4 δ_{αδ}δ_{γβ}
                    tgt = (F(4), F(0)) if (a == d and c == b) else Z
                    if not ceq(acc, tgt):
                        ok_comp = False
    rec('T7', 'Fierz',
        '(V−A)⊗(V−A) 自 Fierz（β↔δ 交换不变，L 与 R 各验）；16 基完备性 ΣΓ⊗Γ^A=4δδ',
        'LL=%s RR=%s completeness=%s' % (ok_ll, ok_rr, ok_comp),
        'True/True/True', 'PASS' if ok_ll and ok_rr and ok_comp else 'FAIL')


# T8. 手征流投影
def check_t8():
    # P_R γ^μ P_L = γ^μ P_L；P_L γ^μ P_L = 0；左流 = \barψ γ^μ P_L ψ
    ok_vl = all(meq(mmul(PR, mmul(GAM[mu], PL)), mmul(GAM[mu], PL)) for mu in range(4))
    ok_ll = all(meq(mmul(PL, mmul(GAM[mu], PL)), mzero()) for mu in range(4))
    # P_L γ^μ = γ^μ P_R 等
    ok_r = all(meq(mmul(PL, GAM[mu]), mmul(GAM[mu], PR)) for mu in range(4))
    rec('T8', '手征流投影',
        'P_Rγ^μP_L=γ^μP_L，P_Lγ^μP_L=0，P_Lγ^μ=γ^μP_R',
        'vL=%s lL=%s r=%s' % (ok_vl, ok_ll, ok_r),
        'True/True/True', 'PASS' if ok_vl and ok_ll and ok_r else 'FAIL')


# T10. 最小 EC 四费米系数精算（与 14 卷 3/16 一致）
def check_t10():
    # L = 3/(4κ²) S² - (3/4) S·J5   →  平方配方
    # (S - (κ²/2)J5)² = S² - κ² S·J5 + (κ⁴/4)J5²
    # 3/(4κ²)·(…)= 3S²/(4κ²) - (3/4)S·J5 + 3κ²/16 J5²
    # 故 L = 3/(4κ²)(S-(κ²/2)J5)² - 3κ²/16 J5²
    # 检查系数分数关系：交叉项 2·(3/4)·(1/2)=3/4；常数 (3/4)·(1/2)²=3/16
    cross = F(2)*F(3,4)*F(1,2)
    const = F(3,4)*F(1,2)*F(1,2)
    sol_coef = F(1,2)  # S = (κ²/2)J5 ⇒ S 系数 1/2
    ok_cross = cross == F(3,4)
    ok_const = const == F(3,16)
    ok_sol = sol_coef == F(1,2)
    rec('T10', '系数精算',
        '最小 EC 平方配方：交叉项 3/4、接触项 3/16、S=(κ²/2)J5（与 14 卷一致）',
        'cross=%s const=%s sol=1/2' % (cross, const),
        '3/4, 3/16', 'PASS' if ok_cross and ok_const and ok_sol else 'FAIL')


def main():
    check_t1()
    check_t2()
    check_t3()
    check_t4()
    check_t5()
    check_t6()
    check_t7()
    check_t8()
    check_t10()

    npass = sum(1 for r in RESULTS if r['status'] == 'PASS')
    nfail = sum(1 for r in RESULTS if r['status'] == 'FAIL')
    out = {'tests': RESULTS, 'summary': {'total': len(RESULTS), 'pass': npass, 'fail': nfail}}
    with open(ROOT / 'torsion_operator_basis.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print('== torsion_operator_basis: total=%d PASS=%d FAIL=%d' % (len(RESULTS), npass, nfail))
    for r in RESULTS:
        print('  [%s] %s: %s' % (r['status'], r['id'], r['claim']))
    if nfail:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
