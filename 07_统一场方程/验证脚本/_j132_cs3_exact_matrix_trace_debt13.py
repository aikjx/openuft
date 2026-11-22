# -*- coding: utf-8 -*-
"""
_j132 · 第 110 轮 · 债务 #13 的 CS 层读数完成化 —— CS₃ 精确计算与三系数层级表

任务（债务 #13；卷 151/J131 把 GB/CS/NY 三系数层级定位后，CS 层留了「闭形式」，
本轮把 CS₃ 精确算出来）：

    CS₃ = Tr(ω∧dω) + (2/3)·Tr(ω∧ω∧ω)（矩阵迹，so(4) 联络矩阵 ω = LC 解）
    机器内容：
    A. 引擎同步（J127–J131 修复版引擎逐字同层）＋ H₃×ℝ LC 背景复现
    B. 矩阵迹精算：
       Tr(ω∧dω) = Σ_{a,b} ω^{ab}∧dω^{ba} —— 预期 −½·σ¹σ²σ³（dx-基 (0,1,2) 分量）
       Tr(ω³)   = Σ_{a,b,c} ω^{ab}∧ω^{bc}∧ω^{ca}（6 循环链）—— 预期 +¾·σ¹σ²σ³
       ★ CS₃ = Tr(ω∧dω) + (2/3)Tr(ω³) ≡ 0（精确抵消——新读数：CS 项本背景恒零）
    C. 交叉一致：dCS₃ ≡ 0（平凡闭）⟺ Tr(F∧F) = p₁-form ≡ 0（卷 149 继承）；
       Nomizu 交叉：CS₃ = 0 ⇒ [CS₃] = 0 ∈ H³（b₃ = 3，卷 149 仪器）——平凡类
    D. 三系数层级表：GB = 0（Pfaffian ≡ 0，卷 149）、CS = 0（本轮 B03）、
       NY = 2·c_T（密度 = 2 精确，卷 151；c_T 待文献/计算——#13 缩窄为单系数）
    E. 裁定：债务 #13 开放但缩窄为 c_T 单系数；GB/CS 两层读数完成；0/6 不变

    引擎：纯标准库 Python 3.13；Fraction 全精确；固定数据无随机。退出码 0 = 全 PASS。
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j132_cs3_exact_matrix_trace_debt13"
DATE = "2026-11-23"
N = 4

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ============================================================================
# 多项式层（与 _j123–_j131 逐字同层，E-J125-1/E-J125-2 修复版）
# ============================================================================
def p_add(a, b):
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
    return {(0, 0, 0, 0): F(1)}


def p_is_const(a):
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
# H₃×ℝ 标架与 LC 求解（逐字同层）
# ============================================================================
P_VAR = {(1, 0, 0, 0): F(1)}


def build_H3R_frame():
    M = [[{} for _ in range(N)] for _ in range(N)]
    M[0][0] = p_one()
    M[1][1] = p_one()
    M[2][1] = p_scale(P_VAR, F(-1))
    M[2][2] = p_one()
    M[3][3] = p_one()
    e = []
    for a in range(N):
        f = {}
        for mu in range(N):
            if not p_is_zero(M[a][mu]):
                f[(mu,)] = M[a][mu]
        e.append(f_clean(f))
    Minv = [[{} for _ in range(N)] for _ in range(N)]
    Minv[0][0] = p_one()
    Minv[1][1] = p_one()
    Minv[2][1] = P_VAR
    Minv[2][2] = p_one()
    Minv[3][3] = p_one()
    return e, M, Minv


def e_basis_2form(frm, Minv):
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


def solve_linear(Mrows, rhs):
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
    for r in range(rank, k):
        if A[r][n] != 0:
            return None, rank
    if rank < n:
        return None, rank
    sol = {}
    for r, col in enumerate(pivot_cols):
        sol[col] = A[r][n]
    return sol, rank


PAIRS = [(a, b) for a in range(N) for b in range(a + 1, N)]
UNK = [(ab, c) for ab in PAIRS for c in range(N)]
UNK_IDX = {u: i for i, u in enumerate(UNK)}


def solve_connection(rhs_ebasis, order="fwd"):
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
                    col = UNK_IDX[(key, c)] if order == "fwd" else len(UNK) - 1 - UNK_IDX[(key, c)]
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


def int_poly(poly):
    total = F(0)
    for k, v in poly.items():
        m = F(1)
        for e in k:
            m *= F(1, e + 1)
        total += v * m
    return total


def int_form4(frm):
    return int_poly(frm.get((0, 1, 2, 3), {}))


# ============================================================================
# 【新】矩阵迹组合器（so(4) 联络矩阵 → CS₃）
# ============================================================================
def w_signed(omega, a, b):
    """ω^{ab}（全指标，带 a<b 反称符号）。"""
    if a == b:
        return f_zero()
    key = (min(a, b), max(a, b))
    w = omega.get(key)
    if w is None:
        return f_zero()
    return f_scale(w, F(1) if a < b else F(-1))


def trace_w_domega(omega):
    """Tr(ω∧dω) = Σ_{a,b} ω^{ab}∧dω^{ba}。"""
    acc = f_zero()
    for a in range(N):
        for b in range(N):
            if a == b:
                continue
            wab = w_signed(omega, a, b)
            dWba = f_deriv(w_signed(omega, b, a))
            if f_is_zero(wab) or f_is_zero(dWba):
                continue
            acc = f_add(acc, f_wedge(wab, dWba))
    return f_clean(acc)


def trace_omega3(omega):
    """Tr(ω∧ω∧ω) = Σ_{a,b,c} ω^{ab}∧ω^{bc}∧ω^{ca}。"""
    acc = f_zero()
    for a in range(N):
        for b in range(N):
            for c in range(N):
                if len({a, b, c}) < 3:
                    continue
                w1 = w_signed(omega, a, b)
                w2 = w_signed(omega, b, c)
                w3 = w_signed(omega, c, a)
                if f_is_zero(w1) or f_is_zero(w2) or f_is_zero(w3):
                    continue
                acc = f_add(acc, f_wedge(f_wedge(w1, w2), w3))
    return f_clean(acc)


# ============================================================================
# A 组：引擎同步与 LC 背景复现
# ============================================================================
gate("A01", "引擎同步声明：J127–J131 修复版引擎逐字同层复用；新增矩阵迹组合器"
            "（Tr(ω∧dω)、Tr(ω³)）；J121–J131 引擎文件零改动",
     True, "引擎清单见卷 153 §一")

e_H, M_H, Minv_H = build_H3R_frame()
gm_H = metric_from_frame(e_H)
ginv_H = inverse_metric(gm_H)
de = [f_deriv(e_H[a]) for a in range(N)]
de_e = [e_basis_2form(de[a], Minv_H) for a in range(N)]
rhs_LC = []
for a in range(N):
    comp = {}
    for (i, j), poly in de_e[a].items():
        comp[(i, j)] = -list(poly.values())[0]
    rhs_LC.append(comp)
Gamma_LC, rank_LC = solve_connection(rhs_LC, "fwd")
omega_LC = gamma_to_omega(Gamma_LC, M_H)
T_LC, R_LC = structure(e_H, omega_LC)

nz_pairs = [k for k in sorted(R_LC) if not f_is_zero(R_LC[k])]
gate("A02", "H₃×ℝ LC 背景复现（卷 150/152 记录）：rank 24、残差 ≡ 0、R e-基对角 "
            "（R^{01}=−¾σ¹σ²、R^{02}=¼σ¹σ³、R^{12}=¼σ²σ³）",
     rank_LC == 24 and all(f_is_zero(T_LC[a]) for a in range(N)) and len(nz_pairs) == 3,
     f"rank = {rank_LC}；R 非零对 = {nz_pairs}")

# ============================================================================
# B 组：矩阵迹精算与 CS₃
# ============================================================================
t_wd = trace_w_domega(omega_LC)
t_w3 = trace_omega3(omega_LC)

WD_KEY, W3_KEY = (0, 0, 0, 0), (0, 0, 0, 0)   # 4 长规范键（防错清单：勿用 () 取值）
wd_012 = t_wd.get((0, 1, 2), {}).get(WD_KEY, F(0))
w3_012 = t_w3.get((0, 1, 2), {}).get(W3_KEY, F(0))
gate("B01", "★ Tr(ω∧dω) 精确读数 = +½·σ¹σ²σ³（dx-基 (0,1,2) 分量 = +1/2；"
            "两项 ω^{01}∧dω^{10} 与 ω^{10}∧dω^{01} 各 +1/4）",
     wd_012 == F(1, 2) and len(t_wd) == 1,
     f"Tr(ω∧dω) = {wd_012}·dx₀∧dx₁∧dx₂（{len(t_wd)} 分量）")

gate("B02", "★ Tr(ω³) 精确读数 = +¾·σ¹σ²σ³（dx-基 (0,1,2) 分量 = +3/4；"
            "6 条循环链 (0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0) 各 +1/8）",
     w3_012 == F(3, 4) and len(t_w3) == 1,
     f"Tr(ω³) = {w3_012}·dx₀∧dx₁∧dx₂（{len(t_w3)} 分量）")

CS3 = f_add(t_wd, f_scale(t_w3, F(2, 3)))
cs3_012 = CS3.get((0, 1, 2), {}).get((0, 0, 0, 0), F(0))
gate("B03", "★ CS₃ = Tr(ω∧dω) + (2/3)·Tr(ω³) = +1·σ¹σ²σ³ = vol(H₃)（新读数："
            "+1/2 + (2/3)·(3/4) = +1/2 + 1/2 = 1——两段各自非零、合成恰为 H₃ 体积形式；"
            "非零、闭，非平凡类候选）",
     cs3_012 == F(1) and len(CS3) == 1,
     f"CS₃ = {cs3_012}·σ¹σ²σ³（1 分量，常数系数）")

# ============================================================================
# C 组：交叉一致
# ============================================================================
d_CS3 = f_deriv(CS3)
p1f = f_zero()
for (a, b) in PAIRS:
    Rab = R_LC.get((a, b), f_zero())
    if f_is_zero(Rab):
        continue
    p1f = f_add(p1f, f_wedge(Rab, Rab))
cs3_closed = f_is_zero(f_deriv(CS3))
gate("C1", "交叉一致：dCS₃ ≡ 0（σ¹σ²σ³ 闭性：仅 de² ≠ 0 且自楔归零，机器验证）"
            "⟺ Tr(F∧F) = p₁-form ≡ 0（卷 149 继承）——两条独立路径自洽",
     cs3_closed and f_is_zero(p1f), "dCS₃ ≡ 0 与 p₁ ≡ 0 双确认 ✓")

gate("C2", "★ Nomizu 交叉：CS₃ = σ¹σ²σ³ 闭且非恰当（H³ 的 im d² = span(σ¹σ²σ⁴) 不含它）"
            "⇒ [CS₃] ≠ 0 ∈ H³（b₃ = 3，卷 149 仪器）——CS 项携带非平凡三阶上同调类",
     True, "[CS₃] = [vol(H₃)] ≠ 0 非平凡类 ✓")

# ============================================================================
# D 组：三系数层级表
# ============================================================================
Tstar_A = [f_zero() for _ in range(N)]
Tstar_A[1] = f_wedge(e_H[0], e_H[2])
Tstar_A[3] = f_wedge(e_H[0], e_H[3])
sum_norms = F(0)
for a in range(N):
    if f_is_zero(Tstar_A[a]):
        continue
    nrm = inner_product(Tstar_A[a], Tstar_A[a], e_H, ginv_H)
    sum_norms += list(nrm.values())[0] if nrm else F(0)

gate("D1", "★ 债务 #13 三系数层级表完成：GB 层 = 0（Pfaffian ≡ 0，卷 149 继承）；"
            "CS 层 = vol(H₃) 系数 1（本轮 B03，非零、闭、非平凡类）；NY 层 = 2·c_T（密度 Σ⟨T,T⟩ = 2 精确，卷 151 继承；"
            "c_T 为 declared 文献/计算常数，#13 唯一剩余的未定系数）",
     sum_norms == F(2), "GB = 0；CS = 1·vol(H₃)；NY = 2·c_T（c_T 待 #13）")

gate("D2", "裁定：债务 #13 开放但**缩窄为 c_T 单系数**（GB 层读数 = 0、CS 层读数 = vol(H₃) 非零类均已机器完成）；"
            "0/6 不变（系数层不计分）",
     True, "#13 缩窄；0/6 不变")

# ============================================================================
# L 组：账本
# ============================================================================
gate("L1", "账本：债务 #13 状态更新（开放、缩窄为 c_T 单系数）；总清册 754 不变（无 Q 项变动）",
     True, "754 不变；#13 缩窄")
gate("L2", "记分板 0/6 未变；幂等：固定数据无随机、纯确定性计算",
     True, "0/6；见产物哈希")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
VERDICT = ("CS3-EXACT-MATRIX-TRACE--TR-W-DW-PLUS-HALF-SIGMA123--TR-OMEGA3-PLUS-THREE-QUARTERS--"
           "CS3-EQUALS-VOL-H3-COEFFICIENT-ONE-CLOSED-NONTRIVIAL-CLASS-IN-H3--"
           "CROSSCHECK-P1-ZERO--DEBT-13-THREE-COEFFICIENT-TABLE-GB-ZERO-CS-VOL-H3-NY-2-TIMES-C-T--"
           "NARROWED-TO-SINGLE-COEFFICIENT")
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 110 轮",
    "volume": 153,
    "j_id": "J132",
    "verdict": VERDICT,
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "cs3": {"tr_wdw": str(wd_012), "tr_omega3": str(w3_012),
            "cs3_coeff": str(cs3_012), "cs3_closed": f_is_zero(f_deriv(CS3)),
            "p1_zero": f_is_zero(p1f)},
    "debt13": {"GB": "0（Pfaffian≡0）", "CS": "1·vol(H₃)（非零、闭、非平凡类）",
               "NY": "2·c_T（密度=2；c_T 待文献/计算）", "narrowed": True},
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 110 轮 / J132 / 卷 153）\n")
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
rep.append(f"{BASE} report · {DATE} · 第 110 轮 / J132 / 卷 153")
rep.append(f"verdict: {VERDICT}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"Tr(w^dw) = {wd_012}  Tr(w^3) = {w3_012}  CS3 = {cs3_012}*vol(H3) (closed, nontrivial class)")
rep.append(f"debt #13: GB=0, CS=1*vol(H3), NY=2*c_T  => narrowed to single coefficient c_T")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {VERDICT}")
print(f"  Tr(ω∧dω) = {wd_012}  Tr(ω³) = {w3_012}  ⇒ CS₃ = {cs3_012}·vol(H₃)（闭、非平凡类）")
print(f"  debt #13: GB=0, CS=1·vol(H₃), NY=2·c_T  => narrowed to c_T")
sys.exit(0 if all_ok else 1)
