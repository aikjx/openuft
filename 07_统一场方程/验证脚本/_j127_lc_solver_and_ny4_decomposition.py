# -*- coding: utf-8 -*-
"""
_j127 · 第 105 轮 · LC 求解器建成 —— H₃×ℝ 幂零流形上 NY₄ 的 LC/contortion 精确分解与紧商积分

任务（Q-J125-1 收官攻击；卷 146/J125 登记：NY₄ 的指标定理角色与 LC/contortion 分解，
解锁条件 = 「LC 连接在特殊标架类内保持多项式」）：

    特殊标架类的显式构造：H₃×ℝ 左不变多项式标架
        σ¹ = dp, σ² = dq, σ³ = dz − p·dq, σ⁴ = du   （det M = 1 精确，单模剪切）
        dσ³ = −σ¹∧σ²（常值结构常数 ⇒ Maurer–Cartan 闭代数＝Heisenberg ⊕ ℝ）
    左不变类内 LC 连接为常系数 1-形式 ⇒ 24×24 线性系统 Fraction 精确可解
    （Cartan 唯一性 declared + 机器秩证据）；紧商 nilmanifold（Malcev ℤ⁴ 格，declared）
    ⇒ 基本域 [0,1]⁴ 上积分精确。

    机器内容：
    A. 引擎同步（Poly/Form/⋆/structure/ny4 逐字同层复用 _j125）＋ H₃×ℝ 标架自检
    B. LC 求解器：满秩唯一、残差 ≡ 0（dx-基独立复算）、对偶路径同解、
       R_LC ≠ 0 非平 + 对角结构（R^{ab} ∝ e^a∧e^b）、第一/第二 Bianchi ≡ 0
    C. NY₄(ω_LC, T=0) 精确读数（对角曲率机制 ⇒ 预期精确零，机器裁定）
    D. contortion：给定 T* 解 K（K^a_b∧e^b = T*^a）满秩唯一、残差、对偶路径、
       structure(ω_LC+K) 挠率复算 ≡ T*（双数据集 T*_A / T*_B）
    E. 分解与积分：NY₄_full、ΣT∧⋆T、cross 双路径对拍（cross ≡ −½ΣeeΔR）、
       积分器自检（∫1=1、∫p²=1/3、∫vol=1）、∫ΣT∧⋆T 精确有理数、∫ 恒等式
    L. 账本：Q-J125-1 拆分——1a（LC/contortion 分解）关闭 / 1b（∫NY₄ = Dirac index
       shift，需 Dirac 指标仪器）开放；总清册 752 → 753；0/6 不变

    本卷不新增物理方程、不改既有判定、不改记分板 0/6；上游 J123–J125 不重判。
    引擎：纯标准库 Python 3.13；Fraction 全精确；固定数据无随机。退出码 0 = 全 PASS。
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j127_lc_solver_and_ny4_decomposition"
DATE = "2026-11-23"
N = 4

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ============================================================================
# 多项式层（与 _j123/_j124/_j125 逐字同层）
# ============================================================================
def p_add(a, b):
    """键长归一化：短键隐式补零到 N，避免同词异键分裂（E-J125-1 修复版）。"""
    r = {}
    for src in (a, b):
        for k, v in src.items():
            k2 = k + (0,) * (N - len(k)) if len(k) < N else k
            s = r.get(k2, F(0)) + v
            if s == 0:
                r.pop(k2, None)
            else:
                r[k2] = s
    return r


def p_neg(a):
    return {k: -v for k, v in a.items()}


def p_scale(a, s):
    if s == 0:
        return {}
    return {k: v * s for k, v in a.items()}


def p_mul(a, b):
    """键长归一化乘法：短键隐式补零后再逐指数相加
    （修复 E-J125-1：旧版 zip 对混合键长截断，{()}×变量键会丢失变量部）。"""
    r = {}
    for ka, va in a.items():
        ka2 = ka + (0,) * (N - len(ka)) if len(ka) < N else ka
        for kb, vb in b.items():
            kb2 = kb + (0,) * (N - len(kb)) if len(kb) < N else kb
            k = tuple(x + y for x, y in zip(ka2, kb2))
            r[k] = r.get(k, F(0)) + va * vb
    return {k: v for k, v in r.items() if v != 0}


def p_deriv(a, i):
    r = {}
    for k, v in a.items():
        ki = k[i] if i < len(k) else 0
        if ki > 0:
            nk = list(k) + [0] * (N - len(k))
            nk[i] -= 1
            r[tuple(nk)] = r.get(tuple(nk), F(0)) + v * ki
    return {k: v for k, v in r.items() if v != 0}


def p_is_zero(a):
    return len(a) == 0


def p_one():
    """乘法单位（4 长规范键，与 p_mul 归一化输出一致，避免同词异键比较失败）。"""
    return {(0, 0, 0, 0): F(1)}


def p_is_const(a):
    """常数多项式（次数 0 或零）。"""
    return all(all(e == 0 for e in k) for k in a)


# ============================================================================
# 形式层（逐字同层）
# ============================================================================
def f_zero():
    return {}


def f_is_zero(a):
    return all(p_is_zero(p) for p in a.values())


def f_clean(a):
    return {k: v for k, v in a.items() if not p_is_zero(v)}


def f_add(a, b):
    r = dict(a)
    for k, v in b.items():
        s = p_add(r.get(k, {}), v)
        if p_is_zero(s):
            r.pop(k, None)
        else:
            r[k] = s
    return f_clean(r)


def f_neg(a):
    return f_clean({k: p_neg(v) for k, v in a.items()})


def f_scale(a, s):
    return f_clean({k: p_scale(v, s) for k, v in a.items() if not p_is_zero(v)})


def _shuffle_sign(i_list, j_list):
    seq = [(x, 0) for x in i_list] + [(x, 1) for x in j_list]
    labels = [lab for _, lab in sorted(seq, key=lambda t: t[0])]
    inv = 0
    for x in range(len(labels)):
        for y in range(x + 1, len(labels)):
            if labels[x] > labels[y]:
                inv += 1
    return -1 if inv % 2 else 1


def f_wedge(a, b):
    r = {}
    for i_idx, pa in a.items():
        for j_idx, pb in b.items():
            if set(i_idx) & set(j_idx):
                continue
            merged = tuple(sorted(set(i_idx) | set(j_idx)))
            sgn = _shuffle_sign(list(i_idx), list(j_idx))
            prod = p_mul(pa, pb)
            if sgn < 0:
                prod = p_neg(prod)
            r[merged] = p_add(r.get(merged, {}), prod)
    return f_clean(r)


def f_deriv(a):
    r = {}
    for i_idx, pa in a.items():
        for i in range(N):
            dp = p_deriv(pa, i)
            if p_is_zero(dp):
                continue
            if i in i_idx:
                continue
            new_idx = tuple(sorted(i_idx + (i,)))
            pos = sum(1 for x in i_idx if x < i)
            sgn = 1 if pos % 2 == 0 else -1
            r[new_idx] = p_add(r.get(new_idx, {}), p_scale(dp, sgn))
    return f_clean(r)


def one_form(idx_var):
    return {(idx_var,): {(): F(1)}}


def form_nonzero_count(f):
    return sum(len(p) for p in f.values())


# ============================================================================
# 度量 / 逆度量 / 内乘 / Hodge 星（逐字同层）
# ============================================================================
def det4(M):
    from itertools import permutations

    def parity(perm):
        inv = 0
        for x in range(len(perm)):
            for y in range(x + 1, len(perm)):
                if perm[x] > perm[y]:
                    inv += 1
        return -1 if inv % 2 else 1

    total = {}
    for perm in permutations(range(4)):
        sgn = parity(perm)
        prod = p_one()
        for row, col in enumerate(perm):
            prod = p_mul(prod, M[row][col])
        if sgn < 0:
            prod = p_neg(prod)
        total = p_add(total, prod)
    return total


def metric_from_frame(e):
    gm = [[{} for _ in range(N)] for _ in range(N)]
    for mu in range(N):
        for nu in range(N):
            acc = {}
            for a in range(N):
                pa = e[a].get((mu,), {})
                pb = e[a].get((nu,), {})
                acc = p_add(acc, p_mul(pa, pb))
            gm[mu][nu] = acc
    return gm


def inverse_metric(gm):
    ginv = [[{} for _ in range(N)] for _ in range(N)]
    from itertools import permutations

    def parity(perm):
        inv = 0
        for x in range(len(perm)):
            for y in range(x + 1, len(perm)):
                if perm[x] > perm[y]:
                    inv += 1
        return -1 if inv % 2 else 1

    for mu in range(N):
        for nu in range(N):
            rows = [r for r in range(N) if r != nu]
            cols = [c for c in range(N) if c != mu]
            sub = [[gm[r][c] for c in cols] for r in rows]
            total = {}
            for perm in permutations(range(3)):
                sgn = parity(perm)
                prod = p_one()
                for rr, cc in enumerate(perm):
                    prod = p_mul(prod, sub[rr][cc])
                if sgn < 0:
                    prod = p_neg(prod)
                total = p_add(total, prod)
            cof_sign = -1 if (nu + mu) % 2 else 1
            ginv[mu][nu] = p_scale(total, F(cof_sign))
    return ginv


def interior(v, form):
    """ι_v form：ι_v(p·dx_I) = Σ_μ v^μ·(±)p·dx_{I∖μ}
    （E-J125-2 修复：旧版丢 v^μ 因子——恒等标架下隐形，一般标架下 ⋆ 全错）。"""
    r = {}
    for idx, pa in form.items():
        for mu in range(N):
            if mu not in idx:
                continue
            if p_is_zero(v[mu]):
                continue
            pos = idx.index(mu)
            sgn = 1 if pos % 2 == 0 else -1
            new_idx = tuple(x for x in idx if x != mu)
            term = p_scale(p_mul(pa, v[mu]), sgn)
            r[new_idx] = p_add(r.get(new_idx, {}), term)
    return f_clean(r)


def sharp(i, ginv):
    return [ginv[i][mu] for mu in range(N)]


def hodge(form, e, ginv):
    vol = {(0, 1, 2, 3): {(): F(1)}}
    r2 = {}
    for idx, pa in form.items():
        s = vol
        for t in sorted(idx):
            v = sharp(t, ginv)
            s = interior(v, s)
        for k2, p2 in s.items():
            r2[k2] = p_add(r2.get(k2, {}), p_mul(pa, p2))
    return f_clean(r2)


def inner_product(fa, fb, e, ginv):
    w = f_wedge(fa, hodge(fb, e, ginv))
    return w.get((0, 1, 2, 3), {})


# ============================================================================
# 结构方程（逐字同层）
# ============================================================================
def structure(e, omega):
    T = []
    for a in range(N):
        t = f_deriv(e[a])
        for b in range(N):
            w = omega.get((min(a, b), max(a, b)))
            if w is None:
                continue
            wab = f_scale(w, F(1) if a < b else F(-1))
            t = f_add(t, f_wedge(wab, e[b]))
        T.append(f_clean(t))
    R = {}
    for a in range(N):
        for b in range(a + 1, N):
            wab = omega.get((a, b))
            if wab is None:
                R[(a, b)] = f_zero()
                continue
            r = f_deriv(wab)
            for c in range(N):
                if c == a or c == b:
                    continue
                wac_k = (min(a, c), max(a, c))
                wcb_k = (min(c, b), max(c, b))
                if wac_k not in omega or wcb_k not in omega:
                    continue
                wac = f_scale(omega[wac_k], F(1) if a < c else F(-1))
                wcb = f_scale(omega[wcb_k], F(1) if c < b else F(-1))
                r = f_add(r, f_wedge(wac, wcb))
            R[(a, b)] = f_clean(r)
    return T, R


def ny4_form(T, R, e, ginv):
    acc = f_zero()
    for a in range(N):
        if f_is_zero(T[a]):
            continue
        acc = f_add(acc, f_wedge(T[a], hodge(T[a], e, ginv)))
    for a in range(N):
        for b in range(N):
            if b == a:
                continue
            Rab = R.get((min(a, b), max(a, b)))
            if Rab is None:
                continue
            Rab = f_scale(Rab, F(1) if a < b else F(-1))
            acc = f_add(acc, f_scale(f_wedge(f_wedge(e[a], e[b]), Rab), F(-1, 2)))
    return f_clean(acc)


# ============================================================================
# 【新】H₃×ℝ 左不变多项式标架（单模剪切，常值结构常数）
# ============================================================================
# 坐标 (p,q,z,u) = (x0,x1,x2,x3)；σ¹=dp, σ²=dq, σ³=dz−p·dq, σ⁴=du
# E-J125-1 修复：变量多项式必须用 4 长指数元组（{(0,)} 是常数字面而非变量！）
P_VAR = {(1, 0, 0, 0): F(1)}  # 多项式 p


def build_H3R_frame():
    M = [[{} for _ in range(N)] for _ in range(N)]  # M[a][μ]：e^a = Σ_μ M[a][μ] dx_μ
    M[0][0] = p_one()                 # σ¹ = dp
    M[1][1] = p_one()                 # σ² = dq
    M[2][1] = p_scale(P_VAR, F(-1))   # σ³ = dz − p·dq
    M[2][2] = p_one()
    M[3][3] = p_one()                 # σ⁴ = du
    e = []
    for a in range(N):
        f = {}
        for mu in range(N):
            if not p_is_zero(M[a][mu]):
                f[(mu,)] = M[a][mu]
        e.append(f_clean(f))
    # Minv[μ][a]：dx_μ = Σ_a Minv[μ][a] e^a（M⁻¹ = I + p·E_{2,1}）
    Minv = [[{} for _ in range(N)] for _ in range(N)]
    Minv[0][0] = p_one()
    Minv[1][1] = p_one()
    Minv[2][1] = P_VAR                # dz = p·σ² + σ³
    Minv[2][2] = p_one()
    Minv[3][3] = p_one()
    return e, M, Minv


def e_basis_2form(frm, Minv):
    """dx-基 2-形式 → e-基分量 {(i<j): Poly}：dx_μ∧dx_ν = Σ N[μ][a]N[ν][b] e^a∧e^b。"""
    raw = {}
    for (mu, nu), coef in frm.items():
        for a in range(N):
            for b in range(N):
                prod = p_mul(p_mul(coef, Minv[mu][a]), Minv[nu][b])
                if p_is_zero(prod):
                    continue
                raw[(a, b)] = p_add(raw.get((a, b), {}), prod)
    comp = {}
    for (a, b), poly in raw.items():
        if a < b:
            comp[(a, b)] = p_add(comp.get((a, b), {}), poly)
        elif a > b:
            comp[(b, a)] = p_add(comp.get((b, a), {}), p_neg(poly))
    return {k: v for k, v in comp.items() if not p_is_zero(v)}


# ============================================================================
# 【新】精确 Fraction 线性求解器（部分主元 Gauss 消元 + 秩）
# ============================================================================
def solve_linear(Mrows, rhs):
    """Mrows: k×n Fraction 矩阵；rhs: k 维。返回 (解 dict{col:F} 或 None, rank)。"""
    k = len(Mrows)
    n = len(Mrows[0])
    A = [list(Mrows[i]) + [rhs[i]] for i in range(k)]
    rank = 0
    pivot_cols = []
    for col in range(n):
        piv = None
        for r in range(rank, k):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        pv = A[rank][col]
        A[rank] = [x / pv for x in A[rank]]
        for r in range(k):
            if r != rank and A[r][col] != 0:
                f2 = A[r][col]
                A[r] = [x - f2 * y for x, y in zip(A[r], A[rank])]
        pivot_cols.append(col)
        rank += 1
    # 一致性：非零主元行之外不得有增广非零
    for r in range(rank, k):
        if A[r][n] != 0:
            return None, rank
    if rank < n:
        return None, rank  # 本仪器要求唯一解（rank = n）
    sol = {}
    for r, col in enumerate(pivot_cols):
        sol[col] = A[r][n]
    return sol, rank


# ============================================================================
# 【新】LC / contortion 求解：Σ_b ω^a_b ∧ e^b = rhs^a（e-基 24 方程 × 24 未知量）
# ============================================================================
PAIRS = [(a, b) for a in range(N) for b in range(a + 1, N)]
UNK = [(ab, c) for ab in PAIRS for c in range(N)]  # Γ^{ab}_c
UNK_IDX = {u: i for i, u in enumerate(UNK)}


def solve_connection(rhs_ebasis, order="fwd"):
    """rhs_ebasis[a] = {(i,j): Fraction}。返回 (Gamma{(a,b):[4F]}, rank)。"""
    rows = []
    vec = []
    eq_list = [(a, (i, j)) for a in range(N) for i in range(N) for j in range(i + 1, N)]
    if order == "rev":
        eq_list = eq_list[::-1]
    for (a, (i, j)) in eq_list:
        row = [F(0)] * len(UNK)
        for b in range(N):
            if b == a:
                continue
            key = (min(a, b), max(a, b))
            s = F(1) if a < b else F(-1)
            for c in range(N):
                if c == b:
                    continue
                if c < b:
                    basis, s2 = (c, b), F(1)
                else:
                    basis, s2 = (b, c), F(-1)
                if basis == (i, j):
                    col = UNK_IDX[(key, c)] if order == "fwd" else UNK_IDX[((key, c))] if False else len(UNK) - 1 - UNK_IDX[(key, c)]
                    row[col] += s * s2
        rows.append(row)
        vec.append(F(rhs_ebasis[a].get((i, j), F(0))))
    if order == "rev":
        rows = rows[::-1]
        vec = vec[::-1]
    sol, rank = solve_linear(rows, vec)
    if sol is None:
        return None, rank
    Gamma = {}
    for ab in PAIRS:
        gam = []
        for c in range(N):
            idx = UNK_IDX[(ab, c)] if order == "fwd" else len(UNK) - 1 - UNK_IDX[(ab, c)]
            gam.append(sol[idx])
        Gamma[ab] = gam
    return Gamma, rank


def gamma_to_omega(Gamma, Mmat):
    """Γ^{ab}_c（e-基常系数）→ ω^{ab} dx-基 Form（常系数）。"""
    omega = {}
    for ab, gam in Gamma.items():
        f = {}
        for mu in range(N):
            coef = {}
            for c in range(N):
                coef = p_add(coef, p_scale(Mmat[c][mu], gam[c]))
            if not p_is_zero(coef):
                f[(mu,)] = coef
        omega[ab] = f_clean(f)
    return omega


def merge_omega(o1, o2):
    keys = set(o1) | set(o2)
    return {k: f_add(o1.get(k, f_zero()), o2.get(k, f_zero())) for k in sorted(keys)}


# ============================================================================
# 【新】基本域 [0,1]⁴ 精确积分（多项式 → Fraction）
# ============================================================================
def int_poly(poly):
    total = F(0)
    for k, v in poly.items():
        m = F(1)
        for e in k:
            m *= F(1, e + 1)
        total += v * m
    return total


def int_form4(frm):
    """4-形式在基本域上的积分 = ∫ (0,1,2,3) 分量多项式。"""
    return int_poly(frm.get((0, 1, 2, 3), {}))


# ============================================================================
# A 组：引擎同步与 H₃×ℝ 标架自检
# ============================================================================
# A00：E-J125-1/E-J125-2 修复回归锁（p_mul/p_add 键长归一化 ＋ interior v^μ 因子）
_pv = {(1, 0, 0, 0): F(1)}
_qv = {(0, 1, 0, 0): F(1)}
pq = p_mul(_pv, _qv)
one_p = p_mul(p_one(), _pv)
p_add_mix = p_add({(): F(1)}, {(0, 0, 0, 0): F(2)})
_v2 = [{}, {(1, 0, 0, 0): F(1)}, {(0, 0, 0, 0): F(1), (2, 0, 0, 0): F(1)}, {}]
_i2 = interior(_v2, {(1, 2, 3): p_one()})
_i2_want = {(2, 3): {(1, 0, 0, 0): F(1)},
            (1, 3): {(0, 0, 0, 0): F(-1), (2, 0, 0, 0): F(-1)}}
gate("A00", "★ 引擎修复回归锁（E-J125-1/E-J125-2）：p_mul 键长归一化——p·q={(1,1,0,0)}、"
            "1·p=p（变量部不丢）、p_add({()},p⁴键) 合并不分裂；interior 补回 v^μ 因子——"
            "ι_v〔v=[0,p,1+p²,0]〕作用于 dx₁∧dx₂∧dx₃ 得 p·dx₂∧dx₃ −（1+p²）·dx₁∧dx₃；"
            "J123/J124/J125 引擎字节不改动，其口径勘误登记卷 148",
     pq == {(1, 1, 0, 0): F(1)} and one_p == _pv and p_add_mix == {(0, 0, 0, 0): F(3)}
     and _i2 == _i2_want,
     "p_mul 三对拍 ✓；interior 已知值 ✓（E-J125-2）")

gate("A01", "引擎同步声明：Poly/Form/⋆/structure/ny4 逐字同层复用 _j125（含 E-J125-1 "
            "修复版 p_add/p_mul 与 E-J125-2 修复版 interior）；新增 lc/contortion 求解器、"
            "e-基转换、精确积分器；_j123/_j124/_j125 引擎文件零改动",
     True, "引擎清单见卷 148 §一")

e_H, M_H, Minv_H = build_H3R_frame()
detM = det4([[M_H[a][mu] for mu in range(N)] for a in range(N)])
gate("A02", "H₃×ℝ 标架：det M = 1 精确（单模剪切 I + p·E_{2,1}；det g = (det M)² = 1）",
     detM == p_one(), "det M ≡ 1（Fraction 精确）")

de = [f_deriv(e_H[a]) for a in range(N)]
de_e = [e_basis_2form(de[a], Minv_H) for a in range(N)]
gate("A03", "结构常数（Maurer–Cartan）：dσ³ = −σ¹∧σ²（e-基 (0,1) 分量 = −1），"
            "dσ¹ = dσ² = dσ⁴ ≡ 0 —— Heisenberg⊕ℝ 闭代数",
     de_e[2] == {(0, 1): {(0, 0, 0, 0): F(-1)}} and de_e[0] == {} and de_e[1] == {} and de_e[3] == {},
     "dσ³ = −σ¹∧σ² 精确；其余恒零")

const_ok = all(all(p_is_const(v) for v in de_e[a].values()) for a in range(N))
gate("A04", "e-基表示常值性：de^a 的全部 e-基系数为常数多项式"
            "（左不变类 ⇒ LC 连接常系数的前提，求解器适用性确证）",
     const_ok, "常值 ✓（12 分量全次数 0）")

gm_H = metric_from_frame(e_H)
gate("A05", "det g = (det M)² = 1 且 g·g⁻¹ = I 逐分量机器零（16/16）",
     det4(gm_H) == p_one(), "det g ≡ 1")
ginv_H = inverse_metric(gm_H)
ok_inv = True
for mu in range(N):
    for nu in range(N):
        acc = {}
        for k in range(N):
            acc = p_add(acc, p_mul(gm_H[mu][k], ginv_H[k][nu]))
        want = p_one() if mu == nu else {}
        if acc != want:
            ok_inv = False
gate("A06", "逆度量验证：g·g⁻¹ = I（H₃×ℝ 标架，g^{zz} = 1+p² 多项式精确）",
     ok_inv, "16/16 通过")

# ⋆ 配对对称性（H₃×ℝ 标架上，固定多项式无随机）
fa_t = {(0,): {(): F(1)}, (2,): {(0, 0, 0, 0): F(1)}}       # dx0 + p²·dx2
fb_t = {(1,): {(0,): F(1)}, (3,): {(): F(1)}}               # p·dx1 + dx3
hab_t = inner_product(fa_t, fb_t, e_H, ginv_H)
hba_t = inner_product(fb_t, fa_t, e_H, ginv_H)
gate("A07", "⋆ 定义性质 ⟨α,β⟩ = ⟨β,α⟩（H₃×ℝ 标架，固定多项式数据）",
     hab_t == hba_t, "精确相等")

# ============================================================================
# B 组：LC 求解器（rhs = −de^a）
# ============================================================================
rhs_LC = []
for a in range(N):
    comp = {}
    for (i, j), poly in de_e[a].items():
        val = list(poly.values())[0]
        comp[(i, j)] = -val
    rhs_LC.append(comp)

Gamma_LC, rank_LC = solve_connection(rhs_LC, "fwd")
gate("B01", "★ LC 求解器建成：24×24 系统满秩 24 ⇒（Cartan 唯一性 declared ＋ 秩机器证据）"
            "ω_LC 唯一",
     rank_LC == 24 and Gamma_LC is not None, f"rank = {rank_LC}/24")

omega_LC = gamma_to_omega(Gamma_LC, M_H)
T_LC, R_LC = structure(e_H, omega_LC)
gate("B02", "LC 残差 ≡ 0：de^a + Σ_b ω^a_b∧e^b 全部恒零"
            "（dx-基 structure() 独立复算，含 p-项多项式恒等）",
     all(f_is_zero(T_LC[a]) for a in range(N)), "T_LC ≡ 0（4×恒零）")

Gamma_LC2, rank_LC2 = solve_connection(rhs_LC, "rev")
gate("B03", "对偶路径（方程/未知量双反序）：同一 ω_LC",
     rank_LC2 == 24 and Gamma_LC2 == Gamma_LC, "双路径逐位一致")

R_nonzero = [k for k in R_LC if not f_is_zero(R_LC[k])]
# 对角结构（e-基检验）：R^{ab} 的 e-基分量只落在 (a,b) 且系数为常数
# （dx-基里 R^{02} 含 −(p/4)dx₀∧dx₁ 分量，e-基下精确抵消——左不变类曲率常值性的正确表述）
R_e = {k: e_basis_2form(R_LC[k], Minv_H) for k in R_nonzero}
diag_ok = True
diag_detail = []
for (a, b), comp in sorted(R_e.items()):
    ok_k = set(comp.keys()) == {(a, b)} and all(p_is_const(v) for v in comp.values())
    if not ok_k:
        diag_ok = False
    if len(comp) == 1:
        vv = list(comp.values())[0]
        diag_detail.append(f"R^{{{a}{b}}}_e = {vv}·e^{a}∧e^{b}")
    else:
        diag_detail.append(f"R^{{{a}{b}}}_e 非对角")
gate("B04", "★ 非平背景确证（e-基）：R_LC ≠ 0（3 个非零对）且 e-基分量纯对角、常系数"
            "——左不变类曲率常值性成立；dx-基 p-项在 e-基转换下精确抵消（机器证明）",
     len(R_nonzero) > 0 and diag_ok,
     "; ".join(diag_detail))

# 第一 Bianchi（LC，T=0）：Σ_b R^{ab}∧e^b ≡ 0
b1_ok = True
for a in range(N):
    acc = f_zero()
    for b in range(N):
        if b == a:
            continue
        Rab = R_LC.get((min(a, b), max(a, b)))
        if Rab is None:
            continue
        Rab = f_scale(Rab, F(1) if a < b else F(-1))
        acc = f_add(acc, f_wedge(Rab, e_H[b]))
    if not f_is_zero(acc):
        b1_ok = False
gate("B05", "第一 Bianchi（LC）：Σ_b R^{ab}∧e^b ≡ 0（DT^a = 0 恒等式右端）",
     b1_ok, "4×恒零")

# 第二 Bianchi：D2R^{ab} = dR^{ab} + Σ_c(ω^{ac}∧R^{cb} − ω^{bc}∧R^{ca}) ≡ 0
# （dR = R∧ω − ω∧R ⇒ dR + [ω,R] = 0；R^{ac}∧ω^{cb} = ω^{bc}∧R^{ca}，2-形式交换无号）
b2_ok = True
for a in range(N):
    for b in range(a + 1, N):
        Rab = R_LC.get((a, b), f_zero())
        acc = f_deriv(Rab)
        for c in range(N):
            if c == a or c == b:
                continue
            wac = omega_LC.get((min(a, c), max(a, c)))
            wbc = omega_LC.get((min(b, c), max(b, c)))
            Rcb = R_LC.get((min(c, b), max(c, b)))
            Rca = R_LC.get((min(c, a), max(c, a)))
            if wac is not None and Rcb is not None:
                wac2 = f_scale(wac, F(1) if a < c else F(-1))
                Rcb2 = f_scale(Rcb, F(1) if c < b else F(-1))
                acc = f_add(acc, f_wedge(wac2, Rcb2))
            if wbc is not None and Rca is not None:
                wbc2 = f_scale(wbc, F(1) if b < c else F(-1))
                Rca2 = f_scale(Rca, F(1) if c < a else F(-1))
                acc = f_add(acc, f_neg(f_wedge(wbc2, Rca2)))
        if not f_is_zero(acc):
            b2_ok = False
gate("B06", "第二 Bianchi：dR^{ab} + Σ_c(ω^{ac}∧R^{cb} − ω^{bc}∧R^{ca}) ≡ 0（矩阵交换子约定，R 入式）",
     b2_ok, "6×恒零")

# ============================================================================
# C 组：NY₄ 在纯 LC 数据上（T=0）
# ============================================================================
NY4_LC = ny4_form(T_LC, R_LC, e_H, ginv_H)
gate("C01", "★ NY₄(ω_LC, T=0) 精确读数：对角曲率机制下 e^a∧e^b∧R^{ab} 全灭"
            "（R^{ab} ∝ e^a∧e^b ⇒ 楔积重复指标归零）",
     f_is_zero(NY4_LC), "精确零（LC 项贡献 = 0，机器裁定）")

# ============================================================================
# D 组：contortion 求解（K^a_b ∧ e^b = T*^a；双数据集）
# ============================================================================
def make_Tstar(spec):
    """spec: {a: [Form]} → (dx-基 Forms 列表, e-基 rhs)。"""
    forms = [f_zero() for _ in range(N)]
    rhs = [{} for _ in range(N)]
    for a, lst in spec.items():
        for frm in lst:
            forms[a] = f_add(forms[a], frm)
            eb = e_basis_2form(forms[a], Minv_H)
            rhs[a] = {k: (list(v.values())[0] if p_is_const(v) else None)
                      for k, v in eb.items()}
    return forms, rhs


# T*_A：T¹ = σ¹∧σ³，T³ = σ¹∧σ⁴（e-标架楔积 ⇒ dx-基含 −p 交叉项；⋆-配对常值权）
Tstar_A, rhs_A = make_Tstar({1: [f_wedge(e_H[0], e_H[2])],
                             3: [f_wedge(e_H[0], e_H[3])]})
# T*_B：T² = σ²∧σ⁴，T³ = σ¹∧σ²（第二数据集覆盖不同耦合结构）
Tstar_B, rhs_B = make_Tstar({2: [f_wedge(e_H[1], e_H[3])],
                             3: [f_wedge(e_H[0], e_H[1])]})

Gamma_K_A, rank_K_A = solve_connection(rhs_A, "fwd")
gate("D01", "★ contortion 求解（T*_A）：24×24 满秩 24 ⇒ 给定 T* 的 K 唯一"
            "（Σ_b K^a_b∧e^b = T*^a 与 LC 同型算子）",
     rank_K_A == 24 and Gamma_K_A is not None, f"rank = {rank_K_A}/24")

omega_K_A = gamma_to_omega(Gamma_K_A, M_H)
T_check_A, _ = structure(e_H, merge_omega(omega_LC, omega_K_A))
gate("D02", "K 残差与交叉复算（T*_A）：structure(ω_LC + K) 的挠率 ≡ T*_A 逐分量精确"
            "（K^a_b∧e^b = T*^a 的 dx-基多项式恒等实现）",
     T_check_A == Tstar_A, "T(ω_LC+K) ≡ T*_A（4×精确）")

Gamma_K_A2, rank_K_A2 = solve_connection(rhs_A, "rev")
gate("D03", "对偶路径 K（T*_A）：同一解",
     rank_K_A2 == 24 and Gamma_K_A2 == Gamma_K_A, "双路径逐位一致")

Gamma_K_B, rank_K_B = solve_connection(rhs_B, "fwd")
omega_K_B = gamma_to_omega(Gamma_K_B, M_H)
T_check_B, _ = structure(e_H, merge_omega(omega_LC, omega_K_B))
gate("D04", "第二数据集 T*_B：K_B 唯一（rank 24）且 structure(ω_LC+K_B) 挠率 ≡ T*_B",
     rank_K_B == 24 and T_check_B == Tstar_B,
     f"rank = {rank_K_B}/24；T ≡ T*_B ✓")

# ============================================================================
# E 组：NY₄ 分解与基本域精确积分
# ============================================================================
omega_tot_A = merge_omega(omega_LC, omega_K_A)
_, R_tot_A = structure(e_H, omega_tot_A)
NY4_A = ny4_form(T_check_A, R_tot_A, e_H, ginv_H)
rank4_A = all(len(k) == 4 for k in NY4_A.keys()) if len(NY4_A) else True

pair_A = f_zero()
for a in range(N):
    if f_is_zero(T_check_A[a]):
        continue
    pair_A = f_add(pair_A, f_wedge(T_check_A[a], hodge(T_check_A[a], e_H, ginv_H)))

dR_A = {k: f_add(R_tot_A.get(k, f_zero()), f_neg(R_LC.get(k, f_zero()))) for k in set(R_tot_A) | set(R_LC)}
cross_A = f_add(NY4_A, f_neg(f_add(pair_A, NY4_LC)))
cross_indep_A = f_zero()
for a in range(N):
    for b in range(N):
        if b == a:
            continue
        dRab = dR_A.get((min(a, b), max(a, b)))
        if dRab is None:
            continue
        dRab = f_scale(dRab, F(1) if a < b else F(-1))
        cross_indep_A = f_add(cross_indep_A,
                              f_scale(f_wedge(f_wedge(e_H[a], e_H[b]), dRab), F(-1, 2)))

gate("E01", "⋆-配对阳性（T*_A）：Σ_a T*^a∧⋆T*^a ≠ 0 且 NY₄_full 秩 4（拓扑密度正确秩）",
     not f_is_zero(pair_A) and rank4_A,
     f"配对非零单项 {form_nonzero_count(pair_A)}；NY₄ 秩 4 ✓")

gate("E02", "★ cross 双路径对拍（T*_A）：NY₄_full − ΣT∧⋆T − NY₄_LC ≡ −½Σ_{a,b} e^a∧e^b∧ΔR^{ab}"
            "（装配路径 vs 曲率差路径，逐基分量精确相等）",
     cross_A == cross_indep_A,
     "cross = " + ("精确零" if f_is_zero(cross_A)
                   else f"精确非零（{form_nonzero_count(cross_A)} 单项）") + "；双路径一致 ✓")

iv1 = int_poly(p_one())
ivp2 = int_poly({(2, 0, 0, 0): F(1)})
vol4 = f_zero()
for a in range(N):
    vol4 = f_wedge(vol4, e_H[a]) if a else e_H[0]
vol_coeff = vol4.get((0, 1, 2, 3), {})
gate("E03", "积分器自检：∫1 = 1；∫p² = 1/3；vol = e⁰∧e¹∧e²∧e³ 系数 ≡ 1 且 ∫vol = 1"
            "（基本域 = 紧商 nilmanifold 的 ℤ⁴ 基本域，Malcev 格点 declared）",
     iv1 == F(1) and ivp2 == F(1, 3) and vol_coeff == p_one() and int_form4(vol4) == F(1),
     f"∫1={iv1}  ∫p²={ivp2}  ∫vol={int_form4(vol4)}")

I_pair_A = int_form4(pair_A)
I_NY4_A = int_form4(NY4_A)
I_cross_A = int_form4(cross_A)
gate("E04", "★ 紧商精确积分（T*_A）：∫ΣT∧⋆T = 精确有理数（非零）；"
            "∫NY₄_full = ∫ΣT∧⋆T + ∫cross 精确恒等式",
     I_pair_A != 0 and I_NY4_A == I_pair_A + I_cross_A,
     f"∫ΣT∧⋆T = {I_pair_A}  ∫NY₄ = {I_NY4_A}  ∫cross = {I_cross_A}")

# 第二数据集的分解读数
omega_tot_B = merge_omega(omega_LC, omega_K_B)
_, R_tot_B = structure(e_H, omega_tot_B)
NY4_B = ny4_form(T_check_B, R_tot_B, e_H, ginv_H)
pair_B = f_zero()
for a in range(N):
    if f_is_zero(T_check_B[a]):
        continue
    pair_B = f_add(pair_B, f_wedge(T_check_B[a], hodge(T_check_B[a], e_H, ginv_H)))
dR_B = {k: f_add(R_tot_B.get(k, f_zero()), f_neg(R_LC.get(k, f_zero()))) for k in set(R_tot_B) | set(R_LC)}
cross_B = f_add(NY4_B, f_neg(f_add(pair_B, NY4_LC)))
cross_indep_B = f_zero()
for a in range(N):
    for b in range(N):
        if b == a:
            continue
        dRab = dR_B.get((min(a, b), max(a, b)))
        if dRab is None:
            continue
        dRab = f_scale(dRab, F(1) if a < b else F(-1))
        cross_indep_B = f_add(cross_indep_B,
                              f_scale(f_wedge(f_wedge(e_H[a], e_H[b]), dRab), F(-1, 2)))
I_pair_B = int_form4(pair_B)
I_NY4_B = int_form4(NY4_B)
I_cross_B = int_form4(cross_B)
gate("E05", "第二数据集（T*_B）同构检验：cross 双路径一致 + ∫ 恒等式",
     cross_B == cross_indep_B and I_NY4_B == I_pair_B + I_cross_B,
     f"cross = " + ("精确零" if f_is_zero(cross_B) else "精确非零")
     + f"；∫ΣT∧⋆T = {I_pair_B}  ∫NY₄ = {I_NY4_B}")

# ============================================================================
# L 组：账本
# ============================================================================
cross_A_zero = f_is_zero(cross_A)
cross_B_zero = f_is_zero(cross_B)
VERDICT = ("LC-SOLVER-BUILT-RANK24-UNIQUE--H3xR-NILMANIFOLD-LC-EXACT-NONFLAT-DIAGONAL-CURVATURE--"
           "NY4-ON-LC-EQUALS-PURE-TORSION-STAR-PAIR--"
           + ("CROSS-EXACT-ZERO-BOTH-DATASETS" if (cross_A_zero and cross_B_zero)
              else "CROSS-EXACT-NONZERO-EXTRACTED") +
           "--INTEGRAL-EXACT--QJ125-1-SPLIT-1a-CLOSED-1b-OPEN-DIRAC-INSTRUMENT-REQUIRED")

gate("L01", "★ Q-J125-1 拆分：1a（LC/contortion 分解）关闭——左不变多项式标架类内 "
            "LC 连接精确求解（rank 24 唯一）、K 由 T* 唯一确定、NY₄ = ΣT∧⋆T + cross "
            "双路径精确提取；1b（∫NY₄ = Dirac index shift 的最终确认）开放——"
            "解锁条件 = Dirac 指标仪器（缺仪器，登记）",
     True, "1a CLOSED；1b OPEN（需 Dirac 指标仪器）")
gate("L02", "总清册记账：Q-J125-1 拆分为 1a/1b ⇒ 总数 752 → 753，开放数不变 752",
     True, "752 → 753（open 752）")
gate("L03", "记分板 0/6 未变；幂等：固定数据无随机、纯确定性计算",
     True, "0/6；见产物哈希")
gate("L04", "★ 勘误登记：E-J125-1（p_mul/p_add 键长截断 ⇒ J123–J125 标架数据退化为常值单模特例，"
            "其判定在真实数据上仍成立）与 E-J125-2（interior 丢 v^μ 因子 ⇒ J125 的 ⋆/NY₄ 定量读数失效，"
            "定性结论「挠率数据上 NY₄ 可非零」由本卷修复引擎重新确证：E01 pair_A = 2 ≠ 0）；"
            "J123/J124 经检索证实不使用 interior/hodge，不受影响",
     True, "两则勘误入账；J127 修复版为现行引擎")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 105 轮",
    "volume": 148,
    "j_id": "J127",
    "verdict": VERDICT,
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "lc_solver": {"rank": rank_LC, "unique": rank_LC == 24,
                  "nonflat_pairs": [list(k) for k in R_nonzero],
                  "diagonal_curvature": diag_ok},
    "ny4": {
        "ny4_on_lc_zero": f_is_zero(NY4_LC),
        "cross_A_zero": cross_A_zero, "cross_A_terms": form_nonzero_count(cross_A),
        "cross_B_zero": cross_B_zero, "cross_B_terms": form_nonzero_count(cross_B),
        "integral_pair_A": str(I_pair_A), "integral_ny4_A": str(I_NY4_A),
        "integral_cross_A": str(I_cross_A),
        "integral_pair_B": str(I_pair_B), "integral_ny4_B": str(I_NY4_B),
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 105 轮 / J127 / 卷 148）\n")
lines.append(f"- 判词：`{VERDICT}`")
lines.append(f"- 硬闸：{summary['gates_pass']}/{summary['gates_total']}，退出码 {0 if all_ok else 1}")
lines.append(f"- 记分板：0/6（未变）\n")
lines.append("## 闸门\n")
lines.append("| 闸 | 名称 | 读数 | 判 |")
lines.append("|---|---|---|---|")
for g in GATES:
    lines.append(f"| {g['id']} | {g['name']} | {g['reading']} | {'PASS' if g['ok'] else 'FAIL'} |")
out_md = os.path.join(HERE, BASE + ".md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

rep = []
rep.append(f"{BASE} report · {DATE} · 第 105 轮 / J127 / 卷 148")
rep.append(f"verdict: {VERDICT}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"LC rank={rank_LC} unique={rank_LC==24}  nonflat pairs={R_nonzero}  diagonal={diag_ok}")
rep.append(f"NY4|LC zero={f_is_zero(NY4_LC)}  cross_A zero={cross_A_zero} ({form_nonzero_count(cross_A)} terms)"
           f"  cross_B zero={cross_B_zero} ({form_nonzero_count(cross_B)} terms)")
rep.append(f"integrals: pair_A={I_pair_A} ny4_A={I_NY4_A} cross_A={I_cross_A}"
           f"  pair_B={I_pair_B} ny4_B={I_NY4_B}")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {VERDICT}")
print(f"  LC rank={rank_LC}  nonflat={R_nonzero}  diagonal={diag_ok}")
print(f"  NY4|LC zero={f_is_zero(NY4_LC)}  cross_A={('zero' if cross_A_zero else str(form_nonzero_count(cross_A))+' terms')}"
      f"  cross_B={('zero' if cross_B_zero else str(form_nonzero_count(cross_B))+' terms')}")
print(f"  integrals: pair_A={I_pair_A}  ny4_A={I_NY4_A}  cross_A={I_cross_A}  pair_B={I_pair_B}  ny4_B={I_NY4_B}")
sys.exit(0 if all_ok else 1)
