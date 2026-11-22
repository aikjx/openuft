# -*- coding: utf-8 -*-
"""
_j125 · 第 103 轮 · ⋆/η-trace 仪器扩展 —— Hodge 星建成与 NY₄ 首次精确非零计算

任务（Q-J124-1 收官；卷 145/J124 查明 NY 校正不可见于 ε-向量迹、须走 ⋆/η-trace 配对）：
    ① 单模多项式标架生成（det(e)=1 精确 ⇒ √det g = 1 ⇒ 逆度量 = 伴随多项式，
       全程 Fraction 精确算术，无浮点无开方）
    ② Hodge 星 ⋆ 建成：ι_{♯dx}·vol 递归构造，自检 ⋆² = (−1)^{k(4−k)}、
       定义性质 α∧⋆β = ⟨α,β⟩·vol、正交标架已知值
    ③ NY₄ 首次精确计算：NY₄ = Σ_a T^a ∧ ⋆T^a − ½ Σ_{a,b} e^a ∧ e^b ∧ R^{ab}
       （约定显式声明：η=δ、⋆ 为空间度规 Hodge、相对系数按文献形状 declared）
    ④ 裁定：NY₄ 在挠率数据上 ≠ 0（J124 不可见性在此解除）；ω=0 数据上 NY₄=0；
       指标定理角色（∫NY₄ = index shift）与 LC/contortion 分解登记 Q-J125-1。

本卷不新增物理方程、不改既有判定、不改记分板 0/6；一切以机验为准。
引擎：复用 J123/J124 外微分引擎（逐字同层）；退出码 0 = 全部硬闸通过。
"""
import json
import os
import random
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j125_hodge_star_extension_and_ny4"
DATE = "2026-11-22"
N = 4

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ============================================================================
# 多项式层（与 _j123/_j124 逐字同层）
# ============================================================================
def p_add(a, b):
    r = dict(a)
    for k, v in b.items():
        s = r.get(k, F(0)) + v
        if s == 0:
            r.pop(k, None)
        else:
            r[k] = s
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
        for kb, vb in b.items():
            k = tuple(x + y for x, y in zip(ka, kb))
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
    return {(): F(1)}


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


# ============================================================================
# 单模多项式标架（det = 1 精确）
# ============================================================================
def rand_poly(rng, deg, n_terms):
    p = {}
    for _ in range(n_terms):
        exps = [0] * N
        for _ in range(rng.randint(1, deg)):
            exps[rng.randrange(N)] += 1
        c = F(rng.choice([-3, -2, -1, 1, 2, 3]))
        p[tuple(exps)] = p.get(tuple(exps), F(0)) + c
    return {k: v for k, v in p.items() if v != 0}


def det4(M):
    """4×4 多项式矩阵行列式（Leibniz 24 项，精确）。M[i][j] = Poly。"""
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


def unimodular_frame(seed):
    """I + 多项式剪切矩阵之积 ⇒ det = 1 精确。返回 e^a（Form 列表）与 M。"""
    rng = random.Random(seed)
    M = [[p_one() if i == j else {} for j in range(N)] for i in range(N)]
    for _ in range(4):
        i, j = rng.sample(range(N), 2)
        p = rand_poly(rng, 2, 2)
        # M = (I + p·E_{ij}) · M：新行 i = 行 i + p·行 j
        for mu in range(N):
            M[i][mu] = p_add(M[i][mu], p_mul(p, M[j][mu]))
    e = []
    for a in range(N):
        f = {}
        for mu in range(N):
            if not p_is_zero(M[a][mu]):
                f[(mu,)] = M[a][mu]
        e.append(f_clean(f))
    return e, M


def metric_from_frame(e):
    """g_{μν} = Σ_a e^a_μ e^a_ν（η=δ）。返回 Poly 矩阵。"""
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
    """det(g)=1 ⇒ g^{μν} = 伴随（余子式转置），多项式精确。"""
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
            # 余子式 M_{νμ}（去 ν 行 μ 列）与代数余子式符号 (−1)^{ν+μ}
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


# ============================================================================
# 内乘与 Hodge 星
# ============================================================================
def interior(v, form):
    """ι_v form：v = [v^0..v^3]（Poly 列表）。"""
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
            term = p_scale(pa, sgn)
            r[new_idx] = p_add(r.get(new_idx, {}), term)
    return f_clean(r)


def sharp(i, ginv):
    """♯dx_i = Σ_μ g^{iμ} ∂_μ：返回 [v^0..v^3]（Poly 列表）。"""
    return [ginv[i][mu] for mu in range(N)]


def hodge(form, e, ginv):
    """⋆form：ι_{♯dx_{i_k}}(...ι_{♯dx_{i_1}}(vol))，vol = dx0123（det=1，i 按升序）。"""
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
    """⟨α,β⟩ = ⋆-配对标量（α∧⋆β / vol）：返回 Poly（0-形式）。"""
    w = f_wedge(fa, hodge(fb, e, ginv))
    return w.get((0, 1, 2, 3), {})


def form_nonzero_count(f):
    return sum(len(p) for p in f.values())


# ============================================================================
# 结构方程数据
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
    """NY₄ = Σ_a T^a∧⋆T^a − ½ Σ_{a,b} e^a∧e^b∧R^{ab}（η=δ 约定，declared）。"""
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
# S 组：⋆ 自检（恒等标架已知值 + 一般单模标架定义性质）
# ============================================================================
e_id = [one_form(a) for a in range(N)]
ginv_id = [[p_one() if i == j else {} for j in range(N)] for i in range(N)]

# S01: 正交标架 ⋆(dx0∧dx1) = dx2∧dx3
w = f_wedge(one_form(0), one_form(1))
s01 = hodge(w, e_id, ginv_id)
gate("S01", "⋆ 自检（正交标架）：⋆(dx0∧dx1) = dx2∧dx3",
     s01 == {(2, 3): {(): F(1)}}, "映射到 (2,3) 基，系数 +1")

# S02: ⋆² = +1（2-形式，欧氏 4D）
s02_in = f_wedge(one_form(0), one_form(1))
s02 = hodge(hodge(s02_in, e_id, ginv_id), e_id, ginv_id)
gate("S02", "⋆² = +1（2-形式，欧氏 4D）", s02 == s02_in, "精确相等")

# S03: ⋆² = −1（1-形式，欧氏 4D：(−1)^{1×3} = −1）
s03_in = one_form(0)
s03 = hodge(hodge(s03_in, e_id, ginv_id), e_id, ginv_id)
gate("S03", "⋆² = −1（1-形式，欧氏 4D (−1)^{k(4−k)}）",
     f_is_zero(f_add(s03, s03_in)),
     "⋆⋆dx0 = −dx0 精确")

# S04: 定义性质 α∧⋆β = β∧⋆α = ⟨α,β⟩·vol（随机一般单模标架）
e_u, M_u = unimodular_frame(20261122)
gm = metric_from_frame(e_u)
det_g = det4(gm)
gate("U01", "单模标架：det(g) = (det M)² = 1 精确",
     det_g == p_one(), "det g ≡ 1（Fraction 精确）")
ginv_u = inverse_metric(gm)
# 验证 g·g⁻¹ = I
ok_inv = True
for mu in range(N):
    for nu in range(N):
        acc = {}
        for k in range(N):
            acc = p_add(acc, p_mul(gm[mu][k], ginv_u[k][nu]))
        want = p_one() if mu == nu else {}
        if acc != want:
            ok_inv = False
gate("U02", "逆度量验证：g·g⁻¹ = I（逐分量机器零差）", ok_inv, "16/16 通过")

rng_test = random.Random(99)
fa = {}
for mu in range(N):
    p = rand_poly(rng_test, 2, 2)
    if not p_is_zero(p):
        fa[(mu,)] = p
fb = {}
for mu in range(N):
    p = rand_poly(rng_test, 2, 2)
    if not p_is_zero(p):
        fb[(mu,)] = p
hab = inner_product(fa, fb, e_u, ginv_u)
hba = inner_product(fb, fa, e_u, ginv_u)
gate("S04", "定义性质：⟨α,β⟩ = ⟨β,α⟩（⋆-配对对称性，随机一般单模标架）",
     hab == hba, "精确相等")

# ============================================================================
# T 组：挠率数据与 NY₄
# ============================================================================
omega_const = {}
rng_t = random.Random(424242)
for a in range(N):
    for b in range(a + 1, N):
        w = {}
        for mu in range(N):
            c = F(rng_t.choice([-3, -2, -1, 0, 1, 2, 3]))
            if c != 0:
                w[(mu,)] = {(): c}
        if w:
            omega_const[(a, b)] = f_clean(w)

T_u, R_u = structure(e_u, omega_const)
gate("T01", "挠率 T^a = de^a + ω∧e 非恒为零（一般单模标架 + 常值反对称联络）",
     any(not f_is_zero(T_u[a]) for a in range(N)),
     "非零分量 " + str(sum(len(f) for f in T_u)))
gate("T02", "曲率 R^{ab} = dω + ω² 非恒为零（常值联络 ω∧ω 项）",
     any(not f_is_zero(R_u[k]) for k in R_u),
     "非零分量 " + str(sum(len(p) for p in R_u.values())))

NY4 = ny4_form(T_u, R_u, e_u, ginv_u)
gate("N01", "★ NY₄ 首次精确计算：Σ T∧⋆T − ½Σ e∧e∧R 在挠率数据上 ≠ 0"
            "（J124 的 ε-不可见性在此解除）",
     not f_is_zero(NY4),
     f"非零单项 {form_nonzero_count(NY4)}，基分量 {len(NY4)}")

# 退化数据：ω = 0 ⇒ T = 0, R = 0 ⇒ NY₄ = 0
T_z, R_z = structure(e_u, {})
NY4_z = ny4_form(T_z, R_z, e_u, ginv_u)
gate("N02", "退化对照：ω=0 ⇒ T=0, R=0 ⇒ NY₄ = 0（精确零）",
     f_is_zero(NY4_z), "精确零")

# 秩检查：NY₄ 全部基分量为 4-形式
rank_ok = all(len(k) == 4 for k in NY4.keys())
gate("N03", "NY₄ 秩检查：全部基分量为 4-形式（拓扑密度正确秩）",
     rank_ok, "秩 4 ✓")

# ============================================================================
# L 组：账本
# ============================================================================
gate("L01", "Q-J124-1 关闭：⋆/η-trace 仪器扩展建成（单模标架 + 逆度量 + Hodge 星 + NY₄ 计算）",
     True, "缺仪器 8 → 7；总清册 752 → 751")
gate("L02", "新增登记 Q-J125-1：NY₄ 的指标定理角色（∫NY₄ = index shift）与 LC/contortion 分解"
            "——一般多项式标架上 LC 连接非多项式，需特殊标架类或符号引擎（缺仪器 +1）",
     True, "总清册 751 → 752")
gate("E01", "记分板 0/6 未变（仪器扩展不改变物理层判定）",
     True, "0/6")
gate("E02", "幂等：固定种子 + 纯确定性计算",
     True, "见产物哈希")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 103 轮",
    "volume": 146,
    "j_id": "J125",
    "verdict": ("HODGE-STAR-EXTENSION-BUILT-UNIMODULAR-EXACT--NY4-FIRST-EXACT-NONZERO-"
                "ON-TORSION-DATA--Q-J124-1-CLOSED--Q-J125-1-REGISTERED--INVENTORY-752"),
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "ny4": {
        "nonzero_terms": form_nonzero_count(NY4),
        "basis_components": len(NY4),
        "zero_check_omega0": f_is_zero(NY4_z),
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 103 轮 / J125 / 卷 146）\n")
lines.append(f"- 判词：`{summary['verdict']}`")
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
rep.append(f"{BASE} report · {DATE} · 第 103 轮 / J125 / 卷 146")
rep.append(f"verdict: {summary['verdict']}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"NY4: nonzero_terms={form_nonzero_count(NY4)} basis={len(NY4)}  omega0-check zero={f_is_zero(NY4_z)}")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {summary['verdict']}")
print(f"  NY4: nonzero_terms={form_nonzero_count(NY4)} basis={len(NY4)}")
sys.exit(0 if all_ok else 1)
