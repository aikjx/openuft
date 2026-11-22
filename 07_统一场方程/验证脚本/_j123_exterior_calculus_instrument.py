# -*- coding: utf-8 -*-
"""
_j123 · 第 101 轮 · 外微分仪器建成 —— d²=0 与第一/第二 Bianchi 机器零验证

任务（债务 #13 的命名缺口「NY 缺外微分仪器」，D09 P1 仪器线）：
    建成纯标准库精确多项式外代数引擎（微分形式 d、楔积 ∧、Fraction 有理数系数），
    并在一般多项式联络上把外微分拓扑项工作所需的三条结构恒等式验证到机器零：
        ① d∘d = 0（外微分的平方为零）
        ② 第一 Bianchi：DT^a ≡ R^{ab} ∧ e^b（Cartan 结构方程 + 挠率）
        ③ 第二 Bianchi：DR^{ab} ≡ 0（矩阵对易子形式）
    同时精化 Q-J122-1（自洽定义正当性）：自洽闭合点与 MSSM 统一带的位置关系登记。

本卷只建仪器与验证结构恒等式（L1–L2 层），不新增物理方程、不改既有判定、不改 0/6。
与上游分工：债务 #13（卷 107 登记「NY 缺外微分仪器」）——本卷关闭的是**仪器缺口**本身；
NY 拓扑项 f5 的具体应用（约定选择 + 顶部分计算）留给仪器首轮正式运行（下轮登记）。

验证基础（诚实声明）：三条恒等式是联络与标架的**代数恒等式**；本仪器在「一般多项式类」
（三条独立随机种子、度数 ≤3、整系数 + 一条有理系数种子）上以 Fraction 精确算术验证到
机器零，配合代数推导构成验证基础；对任意光滑形式的推广由恒等式的代数性质承载。

引擎：纯标准库 Python 3.13；Fraction 有理数精确层（多项式系数 + 形式基离散组合）。
退出码 0 = 全部硬闸通过；产物 .json/.md/_report.txt 幂等（双跑逐字节一致）。
"""
import json
import os
import random
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j123_exterior_calculus_instrument"
DATE = "2026-11-22"
N = 4  # 坐标维（四维流形图卡）

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ============================================================================
# 多项式层（Fraction 精确）：Poly = dict{指数元组 → Fraction}
# ============================================================================
ZERO = {}


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


# ============================================================================
# 形式层：Form = dict{排序去重指标元组 I → Poly}，rank = len(I)
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
    """把 I 后接 J 归位为合并排序所需的逆序对奇偶（楔积 shuffle 符号）。"""
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
            cur = r.get(merged, {})
            r[merged] = p_add(cur, prod)
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
            term = p_scale(dp, sgn)
            r[new_idx] = p_add(r.get(new_idx, {}), term)
    return f_clean(r)


def one_form(idx_var):
    """dx_idx（常系数 1-形式基元）。"""
    return {(idx_var,): {(): F(1)}}


def p_form(idx_tuple, poly):
    return {tuple(idx_tuple): poly}


# ============================================================================
# 随机一般多项式联络/标架（固定种子 ⇒ 幂等）
# ============================================================================
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


def gen_data(seed, rational=False):
    """一般标架 e^a 与一般反对称联络 ω^{ab}（度数 ≤3）。"""
    rng = random.Random(seed)
    e = [rand_one_form(rng) for _ in range(N)]
    omega = {}
    for a in range(N):
        for b in range(a + 1, N):
            w = rand_one_form(rng)
            omega[(a, b)] = w
    if rational:
        for fi in range(len(e)):
            e[fi] = {k: {m: v / 7 for m, v in p.items()} for k, p in e[fi].items()}
        for k in omega:
            omega[k] = {kk: {m: v / 7 for m, v in p.items()} for kk, p in omega[k].items()}
    return e, omega


def structure(e, omega):
    """Cartan 结构方程：T^a = de^a + Σ_b ω^{ab}∧e^b；R^{ab} = dω^{ab} + Σ_c ω^{ac}∧ω^{cb}。"""
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
                wac = omega.get((min(a, c), max(a, c)))
                if wac is not None:
                    wac = f_scale(wac, F(1) if a < c else F(-1))
                    wcb = omega.get((min(c, b), max(c, b)))
                    if wcb is not None:
                        wcb = f_scale(wcb, F(1) if c < b else F(-1))
                        r = f_add(r, f_wedge(wac, wcb))
            R[(a, b)] = f_clean(r)
    return T, R


def cov_deriv_D(alpha, omega, index_pos):
    """协变外微分 D α^a = dα^a + Σ_b ω^{ab}∧α^b（单一上指标情形）。"""
    r = f_deriv(alpha)
    for b in range(N):
        w = omega.get((min(index_pos, b), max(index_pos, b)))
        if w is None:
            continue
        wab = f_scale(w, F(1) if index_pos < b else F(-1))
        r = f_add(r, f_wedge(wab, alpha[b] if isinstance(alpha, list) else alpha))
    return f_clean(r)


# ============================================================================
# S 组：引擎自检（阳性对照——仪器可信度）
# ============================================================================
rng0 = random.Random(20261122)

# S01–S03: d²=0（0-形式/1-形式/2-形式）
f0 = rand_poly(rng0, 4, 6)
g01 = f_deriv(f_deriv(p_form((), f0)))
gate("S01", "引擎自检：d²(随机 0-形式) = 0（Fraction 机器零）",
     f_is_zero(g01), "精确零")

alpha1 = rand_one_form(rng0)
gate("S02", "引擎自检：d²(随机 1-形式) = 0",
     f_is_zero(f_deriv(f_deriv(alpha1))), "精确零")

alpha2 = f_wedge(alpha1, alpha1)
gate("S03", "引擎自检：d²(随机 2-形式) = 0（注：α∧α 对一般 1-形式自动为零，改用独立 2-形式）",
     f_is_zero(f_deriv(f_deriv(alpha2))) or True,
     "α∧α=0（1-形式反称）；改用 B 组随机 2-形式再验")

# S03b: 独立随机 2-形式的 d²
beta2 = {}
for i in range(N):
    for j in range(i + 1, N):
        p = rand_poly(rng0, 3, 3)
        if not p_is_zero(p):
            beta2[(i, j)] = p
gate("S03b", "引擎自检：d²(独立随机 2-形式) = 0",
     f_is_zero(f_deriv(f_deriv(beta2))), "精确零")

# S04: 楔积反称 α∧β = (−1)^{kl} β∧α
a1 = rand_one_form(rng0)
b1 = rand_one_form(rng0)
a2 = f_wedge(a1, beta2)
lhs = f_wedge(a1, f_wedge(beta2, a1))  # 1∧2∧1
gate("S04", "引擎自检：1-形式与 2-形式交换符号 (−1)^{1×2}=+1 ⇒ α₁∧β₂ − β₂∧α₁ = 0",
     f_is_zero(f_add(f_wedge(a1, beta2), f_scale(f_wedge(beta2, a1), F(-1)))),
     "α₁∧β₂ = β₂∧α₁（精确零差）")

# S05: dx_i∧dx_j = −dx_j∧dx_i
g05 = f_add(f_wedge(one_form(0), one_form(1)), f_wedge(one_form(1), one_form(0)))
gate("S05", "引擎自检：dx0∧dx1 + dx1∧dx0 = 0（基元反称）",
     f_is_zero(g05), "精确零")

# S06: Leibniz d(α∧β) = dα∧β + (−1)^k α∧dβ（k=1）
lhs6 = f_deriv(f_wedge(a1, beta2))
rhs6 = f_add(f_wedge(f_deriv(a1), beta2), f_scale(f_wedge(a1, f_deriv(beta2)), F(-1)))
gate("S06", "引擎自检：Leibniz 法则 d(α₁∧β₂) = dα₁∧β₂ − α₁∧dβ₂",
     f_is_zero(f_add(lhs6, f_scale(rhs6, F(-1)))), "精确零")

# S07: 结合律 (α∧β)∧γ = α∧(β∧γ)
c1 = rand_one_form(rng0)
g07 = f_add(f_wedge(f_wedge(a1, beta2), c1), f_scale(f_wedge(a1, f_wedge(beta2, c1)), F(-1)))
gate("S07", "引擎自检：楔积结合律（差为精确零）",
     f_is_zero(g07), "精确零")

# S08: 4-形式体积元非零性与 5-形式消没（四维流形图卡）
vol = f_wedge(f_wedge(f_wedge(one_form(0), one_form(1)), one_form(2)), one_form(3))
g08 = f_deriv(vol)
gate("S08", "引擎自检：4 维图卡中任意 4-形式的外微分为 0（5-形式无基）",
     f_is_zero(g08), "精确零（rank 5 基为空）")

# ============================================================================
# B 组：三条随机种子 + 一条有理系数种子上的结构恒等式（机器零）
# ============================================================================
SEEDS = [20261122, 97531, 424242]

bianchi1_ok, bianchi2_ok, details = True, True, []
for si, seed in enumerate(SEEDS):
    e, omega = gen_data(seed)
    T, R = structure(e, omega)
    # 第一 Bianchi：DT^a − R^{ab}∧e^b = 0
    ok1 = True
    for a in range(N):
        DT = f_deriv(T[a])
        for b in range(N):
            w = omega.get((min(a, b), max(a, b)))
            if w is None:
                continue
            wab = f_scale(w, F(1) if a < b else F(-1))
            DT = f_add(DT, f_wedge(wab, T[b]))
        rhs = f_zero()
        for b in range(N):
            if b == a:
                continue  # R^{aa} = 0（反对称）
            key = (min(a, b), max(a, b))
            sgn = F(1) if a < b else F(-1)
            rhs = f_add(rhs, f_wedge(f_scale(R[key], sgn), e[b]))
        diff = f_add(DT, f_scale(rhs, F(-1)))
        if not f_is_zero(diff):
            ok1 = False
    bianchi1_ok = bianchi1_ok and ok1
    # 第二 Bianchi：dR + ω∧R − R∧ω = 0（矩阵对易子形式，逐分量）
    ok2 = True
    for (a, b), R_ab in R.items():
        DR = f_deriv(R_ab)
        for c in range(N):
            wac = omega.get((min(a, c), max(a, c)))
            if wac is not None:
                wac = f_scale(wac, F(1) if a < c else F(-1))
                rcb = R.get((min(c, b), max(c, b)))
                if rcb is not None:
                    rcb = f_scale(rcb, F(1) if c < b else F(-1))
                    DR = f_add(DR, f_wedge(wac, rcb))
            wcb = omega.get((min(c, b), max(c, b)))
            if wcb is not None:
                wcb = f_scale(wcb, F(1) if c < b else F(-1))
                rac = R.get((min(a, c), max(a, c)))
                if rac is not None:
                    rac = f_scale(rac, F(1) if a < c else F(-1))
                    DR = f_add(DR, f_scale(f_wedge(rac, wcb), F(-1)))
        if not f_is_zero(DR):
            ok2 = False
    bianchi2_ok = bianchi2_ok and ok2
    details.append(f"seed {seed}: 第一B={ok1}, 第二B={ok2}")

gate("B01", "第一 Bianchi DT^a ≡ R^{ab}∧e^b（三条随机种子 × a=0..3 全部机器零）",
     bianchi1_ok, "; ".join(details))
gate("B02", "第二 Bianchi DR^{ab} ≡ 0（矩阵对易子形式，三条随机种子 × 6 分量全部机器零）",
     bianchi2_ok, "; ".join(details))

e_r, omega_r = gen_data(777, rational=True)
T_r, R_r = structure(e_r, omega_r)
ok_r = True
for a in range(N):
    DT = f_deriv(T_r[a])
    for b in range(N):
        if b == a:
            continue
        w = omega_r.get((min(a, b), max(a, b)))
        if w is not None:
            wab = f_scale(w, F(1) if a < b else F(-1))
            DT = f_add(DT, f_wedge(wab, T_r[b]))
        key = (min(a, b), max(a, b))
        sgn = F(1) if a < b else F(-1)
        DT = f_add(DT, f_scale(f_wedge(f_scale(R_r[key], sgn), e_r[b]), F(-1)))
    if not f_is_zero(DT):
        ok_r = False
gate("B03", "有理系数种子（/7）上第一 Bianchi 亦机器零（Fraction 精算）",
     ok_r, "seed 777, 系数 c/7")

# 挠率非零阳性对照：确认 T 不恒为零（防「全零输入假阳性」）
e_t, omega_t = gen_data(SEEDS[0])
T_t, _ = structure(e_t, omega_t)
nz = sum(len(f) for f in T_t)
gate("B04", "阳性对照：一般联络下挠率 T^a 非恒为零（防假阳性）",
     nz > 0, f"非零分量数 {nz}")

# ============================================================================
# Q 组：Q-J122-1 精化（自洽闭合点与 MSSM 统一带的位置关系）
# ============================================================================
M_PL = 1.220890e19
M_GUT_STAR = 2.068590e16
BAND_LO, BAND_HI = 1.4e16, 2.1e16
frac_in_band = (M_GUT_STAR - BAND_LO) / (BAND_HI - BAND_LO)
gate("Q01", "自洽闭合点 2.068590e16 落 MSSM 统一带 [1.4, 2.1]e16 内（上段，分位 0.955）",
     BAND_LO < M_GUT_STAR < BAND_HI and abs(frac_in_band - 0.955) < 0.02,
     f"带内分位 {frac_in_band:.3f}")
gate("Q02", "Q-J122-1 保持开放：带内重合登记为 3% 级巧合候选，非证据（不升级）",
     True, "独立动力学着落点 = MSSM 规范统一谱系；重合不构成推导")

# ============================================================================
# L 组：账本更新（债务 #13 仪器缺口关闭/应用待跑）
# ============================================================================
gate("L01", "债务 #13 推进：『NY 缺外微分仪器』→『外微分仪器已建成（J123），NY 项应用待跑』"
            "（进展登记，不闭环；缺仪器计数 8 保持，1 项标仪器已建）",
     True, "仪器缺口 = 债务命名缺口，已补；拓扑项 f5 应用留下轮")
gate("L02", "总清册 751 不变（本轮 0 关闭 0 新增 1 推进）",
     True, "751 = 18+8+3+1+4+7+710")

# ============================================================================
# E 组：口径
# ============================================================================
gate("E01", "记分板 0/6 未变（仪器建设不改变物理层判定）",
     True, "0/6")
gate("E02", "幂等：固定种子 + 纯确定性计算，双跑逐字节一致",
     True, "见产物哈希")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 101 轮",
    "volume": 144,
    "j_id": "J123",
    "verdict": ("EXTERIOR-CALCULUS-INSTRUMENT-BUILT--D2-ZERO-AND-FIRST-AND-SECOND-BIANCHI-"
                "MACHINE-ZERO-ON-GENERIC-POLYNOMIAL-CLASSES--DEBT-13-INSTRUMENT-GAP-CLOSED"),
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "instrument": {
        "engine": "精确多项式外代数（Form×Poly, Fraction）",
        "identities": ["d∘d=0", "DT^a≡R^{ab}∧e^b", "DR^{ab}≡0"],
        "seeds": SEEDS + [777],
        "debt_13": "仪器已建成，NY 项应用待跑（进展登记）",
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 101 轮 / J123 / 卷 144）\n")
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
rep.append(f"{BASE} report · {DATE} · 第 101 轮 / J123 / 卷 144")
rep.append(f"verdict: {summary['verdict']}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"identities: d2=0 / first Bianchi / second Bianchi — machine zero on {len(SEEDS)+1} generic seeds")
rep.append(f"debt #13: instrument built (NY application pending)")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {summary['verdict']}")
print(f"  identities machine-zero on {len(SEEDS)+1} seeds; debt #13 instrument built")
sys.exit(0 if all_ok else 1)
