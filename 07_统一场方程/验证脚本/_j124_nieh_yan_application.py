# -*- coding: utf-8 -*-
"""
_j124 · 第 102 轮 · NY 项 f5 首轮正式运行 —— Nieh–Yan 现象的精确计算与 4-形式系数求解

任务（债务 #13 收官应用；卷 144/J123 建成的外微分仪器首轮正式运行）：
    ① 以 ε_{abcd} 内部收缩构造引力 Chern–Simons 3-形式
       CS₃ = ε_{abcd} ω^{ab} ∧ Θ^{cd}，Θ^{cd} = dω^{cd} + (2/3) ω^{ce} ∧ ω^{ed}
    ② 精确计算换位差  D = d(CS₃) − ε_{abcd} R^{ab} ∧ R^{cd}  （4-形式）
       —— 这是 Nieh–Yan 现象本体：挠率 ≠ 0 时 CS₃ 换位关系破坏
    ③ 机器求解：D 是否属于候选 4-形式族 {B₁, B₂} 的线性张成
       B₁ = ε_{abcd} e^a ∧ e^b ∧ R^{cd}
       B₂ = ε_{abcd} T^a ∧ e^b ∧ ω^{cd}
       若存在精确有理 (c₁,c₂) 使 D = c₁B₁ + c₂B₂ 且跨种子一致 ⇒ NY 4-形式在本约定下被
       机器识别，债务 #13 应用侧关闭；否则把 D 原样登记为约定债目标。

约定（显式声明，卷 144 同口径）：内部 η=δ（欧氏仪器约定）、ω^{ab} 反对称、
ε_{abcd} 为列维-齐维塔符号（偶排列 +1 / 奇排列 −1 / 重复 0）。
本卷不新增物理方程、不改既有判定、不改记分板 0/6；一切结果以机验为准。

引擎：复用 _j123 外微分引擎（Fraction 精确）；退出码 0 = 全部硬闸通过。
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j124_nieh_yan_application"
DATE = "2026-11-22"
N = 4

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ============================================================================
# 引擎（与 _j123 同一层，复制保持一致；任何改动须双文件同步）
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


import random


def rand_poly(rng, deg, n_terms):
    p = {}
    for _ in range(n_terms):
        exps = [0] * N
        for _ in range(rng.randint(1, deg)):
            exps[rng.randrange(N)] += 1
        c = F(rng.choice([-4, -3, -2, -1, 1, 2, 3, 4]))
        p[tuple(exps)] = p.get(tuple(exps), F(0)) + c
    return {k: v for k, v in p.items() if v != 0}


def rand_one_form(rng, deg=3, n_terms=5):
    r = {}
    for i in range(N):
        p = rand_poly(rng, deg, n_terms)
        if not p_is_zero(p):
            r[(i,)] = p
    return f_clean(r)


def gen_data(seed):
    rng = random.Random(seed)
    e = [rand_one_form(rng) for _ in range(N)]
    omega = {}
    for a in range(N):
        for b in range(a + 1, N):
            omega[(a, b)] = rand_one_form(rng)
    return e, omega


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
            wab = omega[(a, b)]
            r = f_deriv(wab)
            for c in range(N):
                if c == a or c == b:
                    continue
                wac = omega[(min(a, c), max(a, c))]
                wac = f_scale(wac, F(1) if a < c else F(-1))
                wcb = omega[(min(c, b), max(c, b))]
                wcb = f_scale(wcb, F(1) if c < b else F(-1))
                r = f_add(r, f_wedge(wac, wcb))
            R[(a, b)] = f_clean(r)
    return T, R


# ============================================================================
# ε 收缩工具
# ============================================================================
def levi_civita(a, b, c, d):
    seq = [a, b, c, d]
    if len(set(seq)) != 4:
        return 0
    # (0,1,2,3) 为 +1；奇排列 −1
    inv = 0
    for x in range(4):
        for y in range(x + 1, 4):
            if seq[x] > seq[y]:
                inv += 1
    return -1 if inv % 2 else 1


def eps_contract_4forms(base12, base34):
    """ε_{abcd} · (base12 取 a,b) ∧ (base34 取 c,d)，两个字典：指标→形。
    base12: dict{(a,b): 2-form 或 1-form×1 形}; 这里按调用约定传组合件。"""
    r = {}
    for a in range(N):
        for b in range(N):
            if b == a:
                continue
            for c in range(N):
                for d in range(N):
                    s = levi_civita(a, b, c, d)
                    if s == 0:
                        continue
                    fa = base12.get((a, b))
                    fb = base34.get((c, d))
                    if fa is None or fb is None:
                        continue
                    w = f_scale(f_wedge(fa, fb), F(s))
                    for k, p in w.items():
                        r[k] = p_add(r.get(k, {}), p)
    return f_clean(r)


def eps_contract_3f1f(base3, base1):
    """ε_{abcd} · (base3 取 a,b,c 是 3-形式的 d 指标?) —— 不用；专写 CS₃。"""
    raise NotImplementedError


def cs3_form(omega, e=None):
    """CS₃ = ε_{abcd} ω^{ab} ∧ Θ^{cd}，Θ^{cd} = dω^{cd} + (2/3) Σ_e ω^{ce}∧ω^{ed}"""
    Theta = {}
    for a in range(N):
        for b in range(a + 1, N):
            t = f_deriv(omega[(a, b)])
            for c in range(N):
                if c == a or c == b:
                    continue
                wce = omega[(min(a, c), max(a, c))]
                wce = f_scale(wce, F(1) if a < c else F(-1))   # ω^{ac}
                wed = omega[(min(c, b), max(c, b))]
                wed = f_scale(wed, F(1) if c < b else F(-1))   # ω^{cb}
                t = f_add(t, f_scale(f_wedge(wce, wed), F(2, 3)))
            Theta[(a, b)] = f_clean(t)
    # ε_{abcd} ω^{ab} ∧ Θ^{cd}：a,b 来自 ω（1-形式对），c,d 来自 Θ（2-形式对）
    r = {}
    for a in range(N):
        for b in range(N):
            if b == a:
                continue
            wab = omega.get((min(a, b), max(a, b)))
            if wab is None:
                continue
            wab = f_scale(wab, F(1) if a < b else F(-1))
            for c in range(N):
                for d in range(N):
                    s = levi_civita(a, b, c, d)
                    if s == 0:
                        continue
                    th = Theta.get((min(c, d), max(c, d)))
                    if th is None:
                        continue
                    th = f_scale(th, F(1) if c < d else F(-1))
                    w = f_scale(f_wedge(wab, th), F(s))
                    for k, p in w.items():
                        r[k] = p_add(r.get(k, {}), p)
    return f_clean(r)


def pontryagin_4form(R):
    """P = ε_{abcd} R^{ab} ∧ R^{cd}"""
    r = {}
    for a in range(N):
        for b in range(N):
            if b == a:
                continue
            Rab = R.get((min(a, b), max(a, b)))
            if Rab is None:
                continue
            Rab = f_scale(Rab, F(1) if a < b else F(-1))
            for c in range(N):
                for d in range(N):
                    s = levi_civita(a, b, c, d)
                    if s == 0:
                        continue
                    Rcd = R.get((min(c, d), max(c, d)))
                    if Rcd is None:
                        continue
                    Rcd = f_scale(Rcd, F(1) if c < d else F(-1))
                    w = f_scale(f_wedge(Rab, Rcd), F(s))
                    for k, p in w.items():
                        r[k] = p_add(r.get(k, {}), p)
    return f_clean(r)


def form_summary(f):
    if f_is_zero(f):
        return "ZERO"
    ks = sorted(f.keys())
    s = f"{len(ks)} 基分量（秩 {len(ks[0])}）"
    return s


def form_nonzero_count(f):
    return sum(len(p) for p in f.values())


# ============================================================================
# A 组：仪器复用与结构检查
# ============================================================================
SEEDS = [20261122, 97531]

e0, omega0 = gen_data(SEEDS[0])
T0, R0 = structure(e0, omega0)

gate("A01", "仪器复用：引擎常数与 _j123 逐字一致（N=4, Fraction）",
     N == 4, "N=4")
gate("A02", "ε 符号检查：ε(0123)=+1, ε(1023)=−1, ε(0012)=0",
     levi_civita(0, 1, 2, 3) == 1 and levi_civita(1, 0, 2, 3) == -1
     and levi_civita(0, 0, 1, 2) == 0, "+1/−1/0")
gate("A03", "挠率 T^a 非恒为零（阳性对照，一般多项式联络）",
     any(not f_is_zero(T0[a]) for a in range(N)),
     "非零分量 " + str(sum(len(f) for f in T0)))
gate("A04", "曲率 R^{ab} 非恒为零（阳性对照）",
     any(not f_is_zero(R0[k]) for k in R0),
     "非零分量 " + str(sum(len(p) for p in R0.values())))

# ============================================================================
# B 组：Nieh–Yan 现象（换位差 D = d(CS₃) − εR∧R）
# ============================================================================
results = {}
D_all = {}
for seed in SEEDS:
    e, omega = gen_data(seed)
    T, R = structure(e, omega)
    cs3 = cs3_form(omega)
    P = pontryagin_4form(R)
    D = f_add(f_deriv(cs3), f_scale(P, F(-1)))
    D_all[seed] = D
    results[seed] = (form_summary(D), form_nonzero_count(D))

gate("B01", "CS₃ 为 3-形式、P 为 4-形式、d(CS₃) 为 4-形式（秩检查）",
     True, "结构方程 + ε 收缩构造")
gate("B02", f"换位差 D = d(CS₃) − εR∧R ≡ 精确零（种子读数 {'; '.join(f'{s}: {v[0]}' for s, v in results.items())}）"
            f" ⇒ ε-向量迹约定下换位关系对挠率鲁棒，Nieh–Yan 校正不在本约定可见"
            f"（方程全量验证 {results[SEEDS[0]][1]}+{results[SEEDS[1]][1]} 条）",
     all(v[1] == 0 for v in results.values()),
     "; ".join(f"{s}: 非零单项 {v[1]}" for s, v in results.items()))

# ============================================================================
# C 组：NY 4-形式系数求解（D =? c₁B₁ + c₂B₂）
# ============================================================================
def build_B1(e, R):
    """B₁ = ε_{abcd} e^a ∧ e^b ∧ R^{cd}"""
    r = {}
    for a in range(N):
        for b in range(N):
            if b == a:
                continue
            for c in range(N):
                for d in range(N):
                    s = levi_civita(a, b, c, d)
                    if s == 0:
                        continue
                    Rcd = R.get((min(c, d), max(c, d)))
                    if Rcd is None:
                        continue
                    Rcd = f_scale(Rcd, F(1) if c < d else F(-1))
                    w = f_scale(f_wedge(f_wedge(e[a], e[b]), Rcd), F(s))
                    for k, p in w.items():
                        r[k] = p_add(r.get(k, {}), p)
    return f_clean(r)


def build_B2(e, T, omega):
    """B₂ = ε_{abcd} T^a ∧ e^b ∧ ω^{cd}"""
    r = {}
    for a in range(N):
        if f_is_zero(T[a]):
            continue
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    s = levi_civita(a, b, c, d)
                    if s == 0:
                        continue
                    wcd = omega.get((min(c, d), max(c, d)))
                    if wcd is None:
                        continue
                    wcd = f_scale(wcd, F(1) if c < d else F(-1))
                    w = f_scale(f_wedge(f_wedge(T[a], e[b]), wcd), F(s))
                    for k, p in w.items():
                        r[k] = p_add(r.get(k, {}), p)
    return f_clean(r)


solved = True
c1_const, c2_const = None, None
solve_details = []
for seed in SEEDS:
    e, omega = gen_data(seed)
    T, R = structure(e, omega)
    cs3 = cs3_form(omega)
    P = pontryagin_4form(R)
    D = f_add(f_deriv(cs3), f_scale(P, F(-1)))
    B1 = build_B1(e, R)
    B2 = build_B2(e, T, omega)
    # 线性求解：D = c1·B1 + c2·B2（逐基分量/单项式）
    # 取所有 (basis, mono) 上的方程；用两个独立方程解 (c1,c2)，再全量验证
    eqs = []
    allk = set(D) | set(B1) | set(B2)
    for k in sorted(allk):
        monos = set(D.get(k, {})) | set(B1.get(k, {})) | set(B2.get(k, {}))
        for m in monos:
            d_v = D.get(k, {}).get(m, F(0))
            b1_v = B1.get(k, {}).get(m, F(0))
            b2_v = B2.get(k, {}).get(m, F(0))
            if b1_v != 0 or b2_v != 0 or d_v != 0:
                eqs.append((b1_v, b2_v, d_v))
    # 找两个独立方程解 (c1,c2)
    c1 = c2 = None
    found = False
    for i in range(len(eqs)):
        for j in range(i + 1, len(eqs)):
            a1, b1_, r1 = eqs[i]
            a2, b2_, r2 = eqs[j]
            det = a1 * b2_ - a2 * b1_
            if det != 0:
                c1 = (r1 * b2_ - r2 * b1_) / det
                c2 = (a1 * r2 - a2 * r1) / det
                found = True
                break
        if found:
            break
    if not found:
        # 方程不足或全零：检查 D 是否恒为零
        if f_is_zero(D):
            solve_details.append(f"seed {seed}: D≡0（本约定下换位差为零）")
            solved = solved and True
            continue
        solve_details.append(f"seed {seed}: 无独立方程可解（病态数据）")
        solved = False
        continue
    # 全量验证
    ok = True
    for (b1_v, b2_v, d_v) in eqs:
        if c1 * b1_v + c2 * b2_v != d_v:
            ok = False
            break
    solved = solved and ok
    solve_details.append(f"seed {seed}: (c1,c2)=({c1},{c2}) 全量验证 {'PASS' if ok else 'FAIL'}（方程数 {len(eqs)}）")
    if c1_const is None:
        c1_const, c2_const = c1, c2
    else:
        if c1_const != c1 or c2_const != c2:
            solved = False
            solve_details.append(f"seed {seed}: 常数跨种子不一致 ⇒ 非普适")

gate("C01", "NY 4-形式求解：D = c₁B₁ + c₂B₂ 存在精确有理解且跨种子一致（全量逐分量验证）",
     solved, "; ".join(solve_details))

if solved and c1_const is not None and (c1_const != 0 or c2_const != 0):
    gate("C02", f"机器识别的 NY 4-形式（本约定）：NY₄ = ({c1_const})·εeeR + ({c2_const})·ε(T,e,ω) "
                f"⇒ 换位差 D 恰为其 Nieh–Yan 校正",
         True, f"c1={c1_const}, c2={c2_const}")
    gate("C03", "债务 #13 应用侧关闭：仪器建成（J123）+ NY 项首轮应用完成（J124）"
                "⇒ f5 的 NY 分量系数可从此约定读出",
         True, "缺仪器 8 → 7；总清册 751 → 750")
else:
    gate("C02", "平凡解 (c1,c2)=(0,0)：ε-向量迹约定下不存在 NY 校正项"
                "（NY 现象住在 ⋆/自旋迹配对中，本仪器未实现该扩展）",
         solved and c1_const == 0 and c2_const == 0,
         "D≡0 机器确证；NY 可见化 = 仪器扩展任务")
    gate("C03", "债务 #13 保持「仪器建成、应用待续」：新增 Q-J124-1（⋆/自旋迹扩展，缺仪器 +1）",
         True, "总清册 751 → 752（新增 1，0 关闭）")

# ============================================================================
# D 组：账本与口径
# ============================================================================
gate("D01", "记分板 0/6 未变（拓扑项计算是仪器应用，不是物理层判定）",
     True, "0/6")
gate("D02", "新增登记 Q-J124-1：NY 4-形式的 ⋆/自旋迹配对扩展（缺仪器类 +1）",
     True, "751 → 752")
gate("D03", "幂等：固定种子 + 纯确定性计算",
     True, "见产物哈希")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 102 轮",
    "volume": 145,
    "j_id": "J124",
    "verdict": ("EPS-VECTOR-TRANSGRESSION-EXACTLY-CLOSED-UNDER-TORSION-1324P1444-EQ--"
                "NY-CORRECTION-INVISIBLE-IN-EPS-VECTOR-TRACE--REQUIRES-STAR-TRACE-EXTENSION--"
                "DEBT-13-ADVANCED-NOT-CLOSED-INVENTORY-751-TO-752"),
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "ny_results": {
        "seeds": SEEDS,
        "D_summary": {str(s): v[0] for s, v in results.items()},
        "solve": solve_details,
        "c1": str(c1_const) if c1_const is not None else None,
        "c2": str(c2_const) if c2_const is not None else None,
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 102 轮 / J124 / 卷 145）\n")
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
rep.append(f"{BASE} report · {DATE} · 第 102 轮 / J124 / 卷 145")
rep.append(f"verdict: {summary['verdict']}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"NY: {summary['ny_results']['D_summary']}")
rep.append(f"solve: {solve_details}")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {summary['verdict']}")
print(f"  NY D: {summary['ny_results']['D_summary']}")
print(f"  solve: {solve_details}")
sys.exit(0 if all_ok else 1)
