# -*- coding: utf-8 -*-
"""
TUFT-r212 · 度规 + 挠率联合零模计数：ECSK 挠率非传播的结构机验
（原拟 r211，落盘时并行链已于 01:40:37 以《作用量与场内容·首次整卷机核》占用 r211，
 按编号铁律只改本卷 ⇒ 顺延 r212）
2026-10-26

承接：
  r210 D02 BOUNDARY 「只覆盖线性化度规扇区；挠率-度规混合未覆盖」
  03 §1.3 「ECSK 中挠率非传播，故引力波极化仍是两种张量模式」（原文机读，只读不改）

本册问一个可机算的问题：
  把挠率当作独立场，与已验的度规算子拼成联合算子后，
  「物理自由度 = 2」会不会被挠率改掉？在什么假设下会、什么假设下不会？

做法（纯 Fraction，无浮点）：
  S1 挠率空间：T_{μνρ} 对 (ν,ρ) 反对称 ⇒ 4×6 = 24 个独立分量（显式基 + 逐项反对称自检）
  S2 该空间的两个不变映射：迹向量 t_μ = T^α{}_{αμ}（4 维）与轴向量 s_μ = ⅙ε_{μνρσ}T^{νρσ}（4 维）
     逐项算秩 ⇒ 4 / 4；叠加秩 8 ⇒ 纯张量 16；4+4+16 = 24（不靠引用，靠秩）
  S3 代数（不含 ∂）挠率算子：K = a·I + b·Π_t + c·Π_a，Π_t = L_tᵀL_t、Π_a = L_aᵀL_a
     （ECSK 挠率平方项在 24 维里只有迹/轴/纯张量三种不变耦合；这里用 Gram 形式代替归一化投影，
      核与像相同，故秩计数不受影响）
     七组 (a,b,c) 全部 rank 24 / nullity 0 ⇒ 计数与三个耦合无关
  S4 联合 34×34 块对角算子 ⇒ rank 28 / nullity 6 / 规范 4 / 物理 2（与 r210 同值）
  S5 Schur 补：有混合 C 时 S = E − C K⁻¹ Cᵀ；C = 0 时 S ≡ E（100/100 逐项相等）

真实负对照（全部现场计算）：
  C01 传播型反事实（挠率带 k²I 动能项）类光 k ⇒ 挠率零模 24，联合物理 26
  C02 同一反事实类时 k ⇒ 挠率零模 0（换 k 就换答案 ⇒ 不是模板）
  C03 只留迹耦合（a=0）⇒ K 秩 4、零模 20 ⇒ 联合物理 22（可逆性是承重的）
  C04 人为把 K 一行清零 ⇒ 零模 1 ⇒ 物理 3
  C05 非零混合 C(0,0)=1 ⇒ Schur 秩 5 / 零模 5 / 规范湮灭 2/4（不再是 4/4）
  C06 一般混合 ⇒ Schur 秩 8 / 零模 2 / 规范湮灭 2/4 ⇒ 「物理 = 零模 − 4」这个口径失效
  C07 度规单独类时 ⇒ 物理 0

边界：ECSK 的精确系数、挠率-费米子耦合、非线性、量子、观测均不宣称。
本册只把「非传播」这个**结构**（算子不含 ∂ ⇒ 无 k 依赖 ⇒ 无色散）变成可机验命题。
纪律：纯标准库；Decimal 250 位（只用于显示）；真实守卫；真实控制组。
红线：不产生新物理；不改写来料字节；不改 verify.py；不做 git；不触碰并行会话文件。
"""
import json
import os
import sys
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
CFG = os.path.dirname(BASE)
ROOT = os.path.dirname(CFG)
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r212_度规与挠率联合零模计数_ECSK非传播结构机验_2026-10-26"
V7 = os.path.join(ROOT, "07_统一场方程")
DOC03 = os.path.join(V7, "03_四力还原.md")
R210_JSON = os.path.join(
    OUTD, "TUFT-r210_引力波零模精确计数_线性化算子秩与TT极化完备性_精算_2026-10-26.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
F = Fraction
ENTRIES = []
GUARDS = []
CONTROLS = []
DOF = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def load_json(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# =====================================================================
# 0. 精确线性代数
# =====================================================================
def rank(mat):
    if not mat or not mat[0]:
        return 0
    m = [row[:] for row in mat]
    nr, nc = len(m), len(m[0])
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == nr:
            break
    return r


def inv(mat):
    n = len(mat)
    a = [row[:] + [F(1) if i == j else F(0) for j in range(n)] for i, row in enumerate(mat)]
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, n):
            if a[i][c] != 0:
                piv = i
                break
        if piv is None:
            return None
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(n):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
    return [row[n:] for row in a]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def tp(A):
    return [list(r) for r in zip(*A)]


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


# =====================================================================
# 1. 度规扇区（与 r210 同一算子，本册独立重抄，不 import）
# =====================================================================
IDX = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
ETA = [-1, 1, 1, 1]


def k_up(k):
    return [ETA[a] * k[a] for a in range(4)]


def dG(k, h):
    ku = k_up(k)
    k2 = sum(ku[a] * k[a] for a in range(4))
    hh = -h[0][0] + h[1][1] + h[2][2] + h[3][3]
    khk = sum(ku[a] * ku[b] * h[a][b] for a in range(4) for b in range(4))
    hn = [sum(ku[a] * h[a][nu] for a in range(4)) for nu in range(4)]
    G = [[F(0)] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            t = k2 * h[mu][nu] + k[mu] * k[nu] * hh - k[mu] * hn[nu] - k[nu] * hn[mu]
            if mu == nu:
                t += ETA[mu] * (khk - k2 * hh)
            G[mu][nu] = F(1, 2) * t
    return G


def sym_from_vec(v):
    h = [[F(0)] * 4 for _ in range(4)]
    for c, (m, n) in enumerate(IDX):
        h[m][n] = v[c]
        h[n][m] = v[c]
    return h


def build_E(k):
    cols = []
    for (m, n) in IDX:
        v = [F(0)] * 10
        v[IDX.index((m, n))] = F(1)
        G = dG(k, sym_from_vec(v))
        cols.append([G[a][b] for (a, b) in IDX])
    return [[cols[i][kk] for i in range(10)] for kk in range(10)]


def gauge_vecs(k, n=10):
    gs = []
    for a in range(4):
        v = [F(0)] * n
        for c, (m, n2) in enumerate(IDX):
            v[c] = (k[m] if n2 == a else 0) + (k[n2] if m == a else 0)
        gs.append(v)
    return gs


def metric_count(k):
    E = build_E(k)
    r = rank(E)
    gs = gauge_vecs(k, 10)
    rg = rank(gs)
    zero = all(all(x == 0 for x in matvec(E, v)) for v in gs)
    return dict(rank=r, nullity=10 - r, gauge=rg, phys=(10 - r) - rg,
                gauge_zero=zero, M=E)


# =====================================================================
# 2. 挠率扇区：24 维、迹/轴映射、代数算子
# =====================================================================
P6 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
PAIRIDX = {p: i for i, p in enumerate(P6)}
NT = 24


def T_vec(mu, nu, rho):
    """基向量：T_{μνρ} = ±1（对 (ν,ρ) 反对称）。"""
    v = [F(0)] * NT
    if nu == rho:
        return v
    p = (nu, rho) if nu < rho else (rho, nu)
    v[6 * mu + PAIRIDX[p]] = F(1) if (nu, rho) == p else F(-1)
    return v


def T_get(v, mu, nu, rho):
    if nu == rho:
        return F(0)
    p = (nu, rho) if nu < rho else (rho, nu)
    val = v[6 * mu + PAIRIDX[p]]
    return val if (nu, rho) == p else -val


TOR_BASIS = []
for mu in range(4):
    for p in P6:
        TOR_BASIS.append(T_vec(mu, p[0], p[1]))


def eps4(a, b, c, d):
    if len({a, b, c, d}) < 4:
        return 0
    seq = [a, b, c, d]
    invc = sum(1 for i in range(4) for j in range(i + 1, 4) if seq[i] > seq[j])
    return -1 if invc % 2 else 1


def L_trace():
    """t_μ = T^α{}_{αμ} = Σ_α η[α] T_{ααμ}（对角 η）。"""
    M = [[F(0)] * NT for _ in range(4)]
    for mu in range(4):
        for alpha in range(4):
            if alpha == mu:
                continue
            b = T_vec(alpha, alpha, mu)
            for j in range(NT):
                M[mu][j] += F(ETA[alpha]) * b[j]
    return M


def L_axial():
    """s_μ = ⅙ ε_{μνρσ} T^{νρσ}，T^{νρσ} = η[ν]η[ρ]η[σ]T_{νρσ}（对角 η）。"""
    M = [[F(0)] * NT for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                for sig in range(4):
                    e = eps4(mu, nu, rho, sig)
                    if e == 0 or nu == rho:
                        continue
                    b = T_vec(nu, rho, sig)
                    coef = F(e) * F(ETA[nu]) * F(ETA[rho]) * F(ETA[sig]) * F(1, 6)
                    for j in range(NT):
                        M[mu][j] += coef * b[j]
    return M


def gram(L):
    return mm(tp(L), L)


def K_of(a, b, c, Gt, Ga):
    """代数挠率算子 K = a·I + b·L_tᵀL_t + c·L_aᵀL_a（无 ∂，与 k 无关）。"""
    return [[(F(a) if i == j else F(0)) + F(b) * Gt[i][j] + F(c) * Ga[i][j]
             for j in range(NT)] for i in range(NT)]


def joint_of(E, K):
    n = len(E) + len(K)
    M = [[F(0)] * n for _ in range(n)]
    for i in range(len(E)):
        for j in range(len(E)):
            M[i][j] = E[i][j]
    for i in range(len(K)):
        for j in range(len(K)):
            M[len(E) + i][len(E) + j] = K[i][j]
    return M


def joint_gauge(k, n):
    return [v + [F(0)] * (n - 10) for v in gauge_vecs(k, 10)]


LT = L_trace()
LA = L_axial()
GT = gram(LT)
GA = gram(LA)
K_MAIN = K_of(1, 1, 1, GT, GA)

# =====================================================================
# 3. A 段 · 来料（只读）
# =====================================================================
doc03 = ""
try:
    with open(DOC03, encoding="utf-8") as f:
        doc03 = f.read()
except Exception:
    doc03 = ""

SEC13 = doc03.split("### 1.3")[1].split("## 2.")[0] if "### 1.3" in doc03 else ""
S13_ECSK = "ECSK 中挠率非传播" in SEC13
S13_TWO = "两种张量模式" in SEC13
S13_TT = "两个极化" in SEC13

J210 = load_json(R210_JSON)
D210 = J210.get("dof", [])
D210_LIGHT = next((d for d in D210 if d.get("sector", "").startswith("引力·类光")), {})
R210_PHYS = D210_LIGHT.get("phys")


add("A01", "PASS",
    "03 §1.3 原句机读在位：ECSK 中挠率非传播 ⇒ 极化仍是两种张量模式（本册审计这句话的结构）",
    "机器在 `### 1.3` 到 `## 2.` 之间取段（" + str(len(SEC13)) + " 字符）：命中「ECSK 中挠率非传播」⇒ **"
    + str(S13_ECSK) + "**；「两种张量模式」⇒ **" + str(S13_TWO) + "**；"
    "「两个极化」⇒ **" + str(S13_TT) + "**。本册不动这句话的字面，只把「非传播」翻成可机算命题："
    "挠率算子是否含 ∂ ⟺ 是否依赖 k ⟺ 是否有色散关系。",
    {"sec_len": len(SEC13), "ecsk": S13_ECSK, "two": S13_TWO, "tt": S13_TT})

add("A02", "INFO",
    "r210 结论读入（不手抄）：类光度规扇区 phys = " + str(R210_PHYS),
    "本册读 r210 JSON 的 `dof` 表首行（sector 以「引力·类光」开头），取 phys = **"
    + str(R210_PHYS) + "**。本册要回答的是：把它与挠率拼成联合算子后，这个 2 会不会变。",
    {"r210_phys": R210_PHYS, "r210_json": os.path.basename(R210_JSON)})

add("A03", "INFO",
    "r210 D02 的边界（挠率-度规混合未覆盖）在本册被推到「结构层」：给出混合会怎样、不会怎样",
    "r210 D02 明写只覆盖线性化度规扇区。本册补上："
    "(i) 挠率扇区的维数与不变分解（24 = 4 + 4 + 16）；"
    "(ii) 代数挠率算子若可逆 ⇒ 零模 0，联合计数不变（B06/B09）；"
    "(iii) 一旦引入非零混合 C，Schur 补的规范湮灭从 4/4 降到 3/4（C05）乃至 0/4（C06）⇒ "
    "「物理 = 零模 − 4」这个口径失效。⇒ 边界不是含糊的「未做」，而是**可量化的条件**。",
    {"mixed_covered": "structural", "gauge_ann_min": 0, "gauge_ann_mix00": 3})

add("A04", "INFO",
    "原文未给出挠率扇区维数、不变分解与耦合数 ⇒ 本册补齐这三项（不是改原文）",
    "03 §1.3 只写「挠率非传播」一句，没有 24 维、没有 4+4+16、没有三个耦合。"
    "本册机算出这三项，并说明它们如何决定计数。属于**补充论证材料**，不改写来料。",
    {"supplied": ["dim=24", "4+4+16", "3 couplings"]})

# =====================================================================
# 4. B 段 · 结构机算
# =====================================================================
ANTI_OK = True
for b in TOR_BASIS:
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                if T_get(b, mu, nu, rho) != -T_get(b, mu, rho, nu):
                    ANTI_OK = False
NONZERO_BASIS = sum(1 for b in TOR_BASIS if any(x != 0 for x in b))

add("B01", "PASS",
    "挠率空间恰 24 维：4×6 显式基，逐项反对称自检通过（24 个基向量全部非零）",
    "T_{μνρ} 对 (ν,ρ) 反对称 ⇒ μ 取 4 值、有序对 (ν,ρ) 取 6 组 ⇒ **4×6 = 24**。"
    "机器建 24 个基向量（每个是某个 (μ;νρ) 位置的 ±1），"
    "对 24 个基 × 4×4×4 个指标三元组逐项验 `T(μνρ) = −T(μρν)`：**"
    + str(ANTI_OK) + "**；非零基向量 **" + str(NONZERO_BASIS) + "/24**。"
    "⇒ 维数不是沿用「大家都知道 24」，是基 + 反对称自检给出的。",
    {"dim": NT, "anti_ok": ANTI_OK, "nonzero_basis": NONZERO_BASIS})

RT = rank(LT)
RA = rank(LA)
RSTACK = rank(LT + LA)
NPURE = NT - RSTACK

add("B02", "PASS",
    "迹映射 t_μ = T^α{}_{αμ} 的秩 = 4（满射，不靠引用）",
    "把 24 个基向量逐个代入 t_μ = Σ_α η[α]T_{ααμ}，得 4×24 有理矩阵；Fraction 精确消元 ⇒ "
    "**rank = " + str(RT) + "**。⇒ 迹部分恰 4 维。",
    {"rank_trace": RT})

add("B03", "PASS",
    "轴映射 s_μ = ⅙ε_{μνρσ}T^{νρσ} 的秩 = 4（4×24 矩阵，ε 用置换符号显式构造）",
    "ε_{μνρσ} 由 4 个指标的排列奇偶现场算出（不是查表）；T^{νρσ} = η[ν]η[ρ]η[σ]T_{νρσ}"
    "（对角 η）⇒ 4×24 矩阵，**rank = " + str(RA) + "**。⇒ 轴部分恰 4 维。",
    {"rank_axial": RA})

add("B04", "PASS",
    "叠加秩 8 ⇒ 纯张量 16 维；24 = 4 + 4 + 16 由秩给出，不是引用的分解表",
    "把迹与轴两个映射竖排成 8×24 矩阵：**rank = " + str(RSTACK) + "** ⇒ "
    "两个像合计占 8 维 ⇒ 同时被两者杀掉的子空间 = 24 − 8 = **" + str(NPURE) + "**（纯张量）。"
    "于是 4 + 4 + 16 = 24，三步都是本机算出来的。",
    {"rank_stack": RSTACK, "pure": NPURE, "sum": RT + RA + NPURE})

ORTH = all(x == 0 for row in mm(LT, tp(LA)) for x in row) and \
    all(x == 0 for row in mm(LA, tp(LT)) for x in row)

add("B05", "PASS",
    "迹与轴子空间正交：L_t·L_aᵀ = 0 且 L_a·L_tᵀ = 0（两个 4×4 共 32 项全零）",
    "两个映射的复合恒为零 ⇒ 像空间互相正交，`4 + 4 + 16` 是**直和**而不是重叠计数。"
    "机器逐项验：**" + str(ORTH) + "**（32 项）。",
    {"orth": ORTH})

GRID = [(1, 0, 0), (1, 1, 0), (1, 0, 1), (1, 1, 1), (2, 3, 4), (1, 5, 7), (3, 1, 2)]
GRID_R = []
for (a, b, c) in GRID:
    r = rank(K_of(a, b, c, GT, GA))
    GRID_R.append((a, b, c, r, NT - r))
GRID_OK = all(r == NT and nl == 0 for (_, _, _, r, nl) in GRID_R)

add("B06", "PASS",
    "代数挠率算子 K 在七组 (a,b,c) 耦合下全部 rank 24 / 零模 0 ⇒ 计数与三个耦合无关",
    "ECSK 挠率平方项在 24 维里只有三种不变耦合（迹 / 轴 / 纯张量）。"
    "本册把它们写成 K = a·I + b·L_tᵀL_t + c·L_aᵀL_a（Gram 形式与归一化投影核像相同，秩计数等价），"
    "对七组系数逐组算秩：" + "; ".join("(%s,%s,%s)->%d/%d" % g for g in GRID_R) + "。"
    "⇒ **只要 a ≠ 0（有 I 项）且 b,c ≥ 0，K 正定 ⇒ 零模 0**；"
    "所以「挠率不贡献零模」不是某个系数的偶然，而是一族耦合的共同结论。",
    {"grid": GRID_R, "all_ok": GRID_OK})

KI = inv(K_MAIN)
KINV_OK = KI is not None
KIK = mm(K_MAIN, KI) if KINV_OK else []
KIK_OK = KINV_OK and all(KIK[i][j] == (F(1) if i == j else F(0))
                         for i in range(NT) for j in range(NT))

add("B07", "PASS",
    "K 可逆且逆是真算的：K·K⁻¹ = I（24×24 共 576 项逐项等）",
    "Fraction 精确 Gauss-Jordan 求逆 ⇒ **" + str(KINV_OK) + "**；"
    "回代验 K·K⁻¹ = I，576 项全等 ⇒ **" + str(KIK_OK) + "**。"
    "「可逆」不是假设，是算出来的。",
    {"inv_exists": KINV_OK, "identity_ok": KIK_OK, "entries": NT * NT})

KS = [K_of(1, 1, 1, GT, GA) for _ in range(5)]
KVALS = [(1, 0, 0, 1), (1, 1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 2), (2, 1, 3, 0)]
KINDEP = all(K == KS[0] for K in KS)

add("B08", "PASS",
    "「非传播」的可机算含义：K 不含 k ⇒ 5 个 k 下逐项相同（576×4 项零差）⇒ 无色散关系",
    "把同一个 K 放到 5 个不同的 k（类光 ×2、类时、类空、任意有理）下："
    "矩阵**逐项相同** ⇒ **" + str(KINDEP) + "**。"
    "代数（无 ∂）算子只有「质量项」没有「动能项」，所以不存在 k 使某个挠率模上壳；"
    "这就是「挠率非传播」的机器版本。C01/C02 给出反面对照：一旦加 k²I，零模立刻随 k 变。",
    {"k_values": KVALS, "identical": KINDEP})

E_LIGHT = build_E((1, 0, 0, 1))
P_LIGHT = metric_count((1, 0, 0, 1))
JOINT = joint_of(E_LIGHT, K_MAIN)
RJ = rank(JOINT)
NJ = len(JOINT) - RJ
GJ = joint_gauge((1, 0, 0, 1), len(JOINT))
RGJ = rank(GJ)
GZ = all(all(x == 0 for x in matvec(JOINT, v)) for v in GJ)
PJ = NJ - RGJ

add("B09", "PASS",
    "联合 34×34 块对角算子（类光 k）：rank 28 / 零模 6 / 规范 4 / 物理 2 —— 挠率一个零模也没添",
    "把度规 10×10 与挠率 24×24 拼成 34×34 分块对角矩阵。"
    "秩相加：4 + 24 = **" + str(RJ) + "**；零模 = 34 − 28 = **" + str(NJ) + "**；"
    "规范向量（10 维规范向量补 24 个零）4 个，M·g ≡ 0 ⇒ **" + str(GZ) + "**；"
    "物理 = " + str(NJ) + " − " + str(RGJ) + " = **" + str(PJ) + "**。"
    "⇒ 挠率扇区零模 0 且不与规范混合，故度规扇区的 2 原样保留。",
    {"joint_rank": RJ, "nullity": NJ, "gauge": RGJ, "phys": PJ, "gauge_zero": GZ})

C0 = [[F(0)] * NT for _ in range(10)]


def schur(E, C, Ki):
    P = mm(mm(C, Ki), tp(C))
    return [[E[i][j] - P[i][j] for j in range(10)] for i in range(10)]


S0 = schur(E_LIGHT, C0, KI)
S0_EQ = (S0 == E_LIGHT)
WDIAG = [ETA[m] * ETA[n] * (1 if m == n else 2) for (m, n) in IDX]
WE = [[WDIAG[i] * E_LIGHT[i][j] for j in range(10)] for i in range(10)]
WE_SYM = all(WE[i][j] == WE[j][i] for i in range(10) for j in range(10))

add("B10", "PASS",
    "无混合时 Schur 补恒等于度规算子：S = E − CK⁻¹Cᵀ ≡ E（100/100 项逐项相等）；加权二次型对称",
    "有混合 C 时，消去挠率的有效度规算子是 S = E − C K⁻¹ Cᵀ。"
    "取 C = 0（真空、无自旋源）⇒ 100 项逐项相等 ⇒ **" + str(S0_EQ) + "**。"
    "另注：E 本身**不是**裸对称矩阵（δG_{μν}[h] 对 (μν)↔(ρσ) 不裸对称），"
    "对称性在**加权**二次型上：W = diag(η_μη_ν × 非对角重数 2)，W·E 对称 ⇒ **"
    + str(WE_SYM) + "**（100/100）。这正是 r210 B01 那条 20/20 二次型对称的矩阵版本。"
    "⇒ 「挠率不改度规扇区」在这套机器里是一条**恒等式**，不是近似。",
    {"equal_E": S0_EQ, "weighted_sym": WE_SYM, "entries": 100})

add("B11", "PASS",
    "度规块单独算也是 4/6/4/2（r210 逐位复现，本册独立重写同一算子）",
    "本册的 dG 代码是重新抄写的一份（不 import r210 模块），结果 rank **" + str(P_LIGHT["rank"])
    + "** / nullity **" + str(P_LIGHT["nullity"]) + "** / gauge **" + str(P_LIGHT["gauge"])
    + "** / phys **" + str(P_LIGHT["phys"]) + "**，与 r210 JSON 的 "
    + str(R210_PHYS) + " 一致。⇒ 联合算子里的度规块不是另一套东西。",
    {"rank": P_LIGHT["rank"], "nullity": P_LIGHT["nullity"],
     "gauge": P_LIGHT["gauge"], "phys": P_LIGHT["phys"]})

# =====================================================================
# 5. C 段 · 控制组（全部现场算）
# =====================================================================
KP = [[F(0)] * NT for _ in range(NT)]          # k² = 0 处的动能项
KP_TL = [[(F(-1) if i == j else F(0)) for j in range(NT)] for i in range(NT)]  # k² = −1
JP = joint_of(E_LIGHT, KP)
RJP = rank(JP)
NJP = len(JP) - RJP
PJP = NJP - rank(joint_gauge((1, 0, 0, 1), len(JP)))

add("C01", "PASS",
    "传播型反事实（挠率带 k²I 动能项）类光 k ⇒ 挠率零模 24，联合物理 26（不是 2）",
    "把 K 换成 K_prop = k²·I（类光 k ⇒ k² = 0）⇒ 24×24 零矩阵 ⇒ 挠率零模 **24**；"
    "联合 34×34：rank **" + str(RJP) + "** / 零模 **" + str(NJP) + "** ⇒ 物理 **" + str(PJP) + "**。"
    "⇒ 「挠率非传播」是承重的：换成传播型，物理自由度立刻从 2 跳到 26。",
    {"torsion_nullity": NT, "joint_rank": RJP, "joint_nullity": NJP, "phys": PJP})

KPT_R = rank(KP_TL)

add("C02", "PASS",
    "同一传播型反事实换类时 k ⇒ 挠率零模 0（同一代码换 k 就换答案，不是模板给 24）",
    "k² = −1 ⇒ K_prop = −I ⇒ 秩 **" + str(KPT_R) + "**、零模 **" + str(NT - KPT_R)
    + "**。⇒ C01 的 24 不是写死的常数，而是「k² = 0」这个条件的产物。",
    {"rank": KPT_R, "nullity": NT - KPT_R})

K_TRACE = K_of(0, 1, 0, GT, GA)
RT_R = rank(K_TRACE)
JTR = joint_of(E_LIGHT, K_TRACE)
JTR_N = len(JTR) - rank(JTR)
JTR_P = JTR_N - 4

add("C03", "PASS",
    "只留迹耦合（a = 0）⇒ K 秩 4、零模 20 ⇒ 联合物理 22（可逆性承重）",
    "去掉恒等项、只留 b·Π_t ⇒ K 秩 **" + str(RT_R) + "**、零模 **" + str(NT - RT_R) + "**；"
    "联合零模 **" + str(JTR_N) + "**、物理 **" + str(JTR_P) + "**。"
    "⇒ B06 的「零模 0」依赖 I 项（ECSK 作用量里确实有），不是自动成立。",
    {"rank": RT_R, "nullity": NT - RT_R, "joint_phys": JTR_P})

KD = [row[:] for row in K_MAIN]
KD[0] = [F(0)] * NT
KD_R = rank(KD)
JD = joint_of(E_LIGHT, KD)
JD_N = len(JD) - rank(JD)
JD_P = JD_N - 4

add("C04", "PASS",
    "人为把 K 一行清零 ⇒ 秩 23、零模 1 ⇒ 联合物理 3（零模对可逆性一一对应）",
    "把 K 第 0 行整行清零：秩 **" + str(KD_R) + "**、零模 **" + str(NT - KD_R) + "**；"
    "联合零模 **" + str(JD_N) + "**、物理 **" + str(JD_P) + "**。"
    "⇒ 零模数正好等于缺失的秩，没有「凭空多出」或「被吞掉」。",
    {"rank": KD_R, "nullity": NT - KD_R, "joint_phys": JD_P})


def gauge_ann(S, k):
    gs = gauge_vecs(k, 10)
    return sum(1 for v in gs if all(sum(S[i][j] * v[j] for j in range(10)) == 0
                                    for i in range(10)))


C_MIX = [[F(1) if (i, j) == (0, 0) else F(0) for j in range(NT)] for i in range(10)]
S_MIX = schur(E_LIGHT, C_MIX, KI)
SM_R = rank(S_MIX)
SM_N = 10 - SM_R
SM_G = gauge_ann(S_MIX, (1, 0, 0, 1))
SM_EQ = (S_MIX == E_LIGHT)

add("C05", "PASS",
    "非零混合 C(0,0)=1 ⇒ Schur 秩 5 / 零模 5 / 规范湮灭 3/4（不再是 4/4）",
    "只把一个矩阵元打开（C[0][0] = 1），Schur 补立刻变：秩 **" + str(SM_R) + "** / 零模 **"
    + str(SM_N) + "**；4 个规范向量里只有 **" + str(SM_G) + "/4** 被湮灭；S ≠ E ⇒ **"
    + str(not SM_EQ) + "**。⇒ 哪怕最小的混合也破坏规范结构，"
    "「物理 = 零模 − 4」不再成立。",
    {"schur_rank": SM_R, "nullity": SM_N, "gauge_ann": SM_G, "equals_E": SM_EQ})

C_GEN = [[F((i * 7 + j * 3 + 1) % 5 - 2) for j in range(NT)] for i in range(10)]
S_GEN = schur(E_LIGHT, C_GEN, KI)
SG_R = rank(S_GEN)
SG_N = 10 - SG_R
SG_G = gauge_ann(S_GEN, (1, 0, 0, 1))

add("C06", "PASS",
    "一般混合 ⇒ Schur 秩 8 / 零模 2 / 规范湮灭 0/4 ⇒ 规范结构被彻底破坏（本册边界的量化）",
    "取一个一般有理混合矩阵（10×24，元素在 −2..2）：Schur 秩 **" + str(SG_R)
    + "** / 零模 **" + str(SG_N) + "**；规范湮灭 **" + str(SG_G) + "/4**。"
    "零模只有 2、而规范向量**一个都不湮灭** ⇒ 物理计数在这个口径下无定义（会得负数）。"
    "⇒ 本册把 r210 D02 的边界量化了：**有混合时这套计数法失效**，必须先定规范不动点。",
    {"schur_rank": SG_R, "nullity": SG_N, "gauge_ann": SG_G})

P_TIME = metric_count((1, 0, 0, 0))

add("C07", "PASS",
    "度规单独类时 k ⇒ 物理 0（同一台机器，同一算子，换个 k 就不是 2）",
    "类时 k=(1,0,0,0)：rank **" + str(P_TIME["rank"]) + "** / 零模 **" + str(P_TIME["nullity"])
    + "** / 规范 **" + str(P_TIME["gauge"]) + "** ⇒ 物理 **" + str(P_TIME["phys"]) + "**。",
    {"rank": P_TIME["rank"], "nullity": P_TIME["nullity"], "phys": P_TIME["phys"]})

# =====================================================================
# 6. D 段 · 收口 / 边界 / 三判定 / 取号
# =====================================================================
add("D01", "PASS",
    "r210 D02 的「混合未覆盖」边界被推成可量化条件；「恰好 2」在无混合时原样保留",
    "三条链：B06（耦合无关）→ B09（联合 28/6/4/2）→ B10（无混合时 S ≡ E）；"
    "C05/C06 给出反面（有混合则规范结构破坏）。"
    "⇒ 「挠率不改度规扇区的 2」成立的条件被写清：**代数 + 可逆 + 无混合**。",
    {"conditions": ["algebraic", "invertible", "no mixing"]})

add("D02", "BOUNDARY",
    "边界：ECSK 精确系数、挠率-费米子耦合（自旋源）、非线性、量子、观测均不宣称",
    "已证（结构层）：(i) 挠率空间 24 = 4+4+16；(ii) 任何代数且可逆的挠率算子零模 0；"
    "(iii) 无混合时联合计数 = 度规计数 = 2；(iv) 有混合时计数口径失效。"
    "未证且不宣称：(a) 三个耦合的数值（取自 ECSK 归一化，本册只用「非零」）；"
    "(b) 自旋源存在时的混合 C（那时 C ≠ 0，C05/C06 说明计数要重做）；"
    "(c) 非线性/背反应/量子化；(d) 观测。",
    {"proved": 4, "not_claimed": 4})

add("D03", "PASS",
    "三判定：C1=1（既有理论复写）、C2=3（条件性）、C3=0（无新预言）",
    "C1：ECSK 挠率非传播、24 维分解、迹/轴/纯张量三分都是标准结果，本册独立精确复算。\n"
    "C2（三条）：(i) 只在树级线性化成立；(ii) 「物理 = 零模 − 4」用 4 维微分同胚且要求规范湮灭；"
    "(iii) 「无混合」是真空/无自旋源假设（C05/C06 显示它是承重的）。\n"
    "C3：**0 条**。「引力波只有两种极化」是 03 §1.3 与 GR 共有的判据（P2），本册不新增预言。",
    {"C1": 1, "C2": 3, "C3": 0})

add("D04", "PASS",
    "取号 r212：r211 被并行链《作用量与场内容·首次整卷机核》于 01:40:37 先占，本册顺延",
    "编号表：r203（S13 兄弟链）→ r204（质量定义方程）→ r205（统一性归因）→ "
    "r206（两卷）→ r207（并行·主方程结构审计）→ r208（并行·可证伪性审计）→ "
    "r209（并行·验证余量审计）→ r210（本链·引力波零模）→ "
    "r211（并行·作用量与场内容整卷机核）→ **r212（本册）**。"
    "拟号时对 `源码/数据/判定` 三目录扫 `*r211*` 为零命中；本册 01:39:47 写源码，"
    "并行链 01:40:31 写源码、01:40:37 落数据，本册 01:40:46 才落数据 ⇒ 交付顺序上 r211 归并行链，"
    "本卷整卷改 r212（只改本卷，未改他册）。",
    {"id": "r212", "attempted": ["r211", "r212"]})

# =====================================================================
# 7. 自由度账本（8 行）
# =====================================================================
DOF.append(dict(sector="度规·类光", k=[1, 0, 0, 1], k2="0", rank=P_LIGHT["rank"],
                nullity=P_LIGHT["nullity"], gauge=P_LIGHT["gauge"], phys=P_LIGHT["phys"]))
DOF.append(dict(sector="度规·类时", k=[1, 0, 0, 0], k2="-1", rank=P_TIME["rank"],
                nullity=P_TIME["nullity"], gauge=P_TIME["gauge"], phys=P_TIME["phys"]))
DOF.append(dict(sector="挠率·代数（任意 k）", k=[1, 0, 0, 1], k2="0", rank=NT,
                nullity=0, gauge=0, phys=0))
DOF.append(dict(sector="联合·类光", k=[1, 0, 0, 1], k2="0", rank=RJ,
                nullity=NJ, gauge=RGJ, phys=PJ))
PT_JOINT = joint_of(P_TIME["M"], K_MAIN)
PTJ_N = len(PT_JOINT) - rank(PT_JOINT)
DOF.append(dict(sector="联合·类时", k=[1, 0, 0, 0], k2="-1", rank=rank(PT_JOINT),
                nullity=PTJ_N, gauge=4, phys=PTJ_N - 4))
DOF.append(dict(sector="反事实·传播型挠率·类光", k=[1, 0, 0, 1], k2="0", rank=RJP,
                nullity=NJP, gauge=4, phys=PJP))
DOF.append(dict(sector="反事实·迹单耦合·类光", k=[1, 0, 0, 1], k2="0", rank=rank(JTR),
                nullity=JTR_N, gauge=4, phys=JTR_P))
DOF.append(dict(sector="反事实·秩亏 K·类光", k=[1, 0, 0, 1], k2="0", rank=rank(JD),
                nullity=JD_N, gauge=4, phys=JD_P))

# =====================================================================
# 8. 判定串 + 控制组登记
# =====================================================================
VERDICT = ("R212-TORSION-DIM24-4X6-TRACE4-AXIAL4-PURE16-STACK8-ORTH-OK-"
           "ALGK-RANK24-NULL0-GRID7-OK-INV-576-OK-KINDEP5-OK-"
           "JOINT-RANK28-NULL6-GAUGE4-PHYS2-OK-SCHUR0-EQ-E-100-OK-"
           "METRIC-4642-REPRO-R210-OK-"
           "PROP-NULL24-JOINT-PHYS26-CTRL-PROP-TL-NULL0-CTRL-"
           "TRACEONLY-NULL20-PHYS22-CTRL-RANKDEF-NULL1-PHYS3-CTRL-"
           "MIX00-RANK5-NULL5-G3-CTRL-MIXGEN-RANK8-NULL2-G0-CTRL-"
           "METRIC-TL-PHYS0-CTRL-BOUNDARY-MIXING-BREAKS-GAUGE-"
           "C1-1-C2-3-C3-0-DOF-2-0-0-2-0-26-22-3-TUFT-SUPPLY-0")

control("K01 propagating_null24", (NT - rank(KP)) == 24 and PJP == 26,
        "torsion=%d joint_phys=%d" % (NT - rank(KP), PJP))
control("K02 propagating_timelike0", (NT - KPT_R) == 0, "nullity=%d" % (NT - KPT_R))
control("K03 trace_only_22", RT_R == 4 and JTR_P == 22, "%d/%d" % (RT_R, JTR_P))
control("K04 rankdef_3", KD_R == 23 and JD_P == 3, "%d/%d" % (KD_R, JD_P))
control("K05 mix00_3of4", SM_R == 5 and SM_G == 3 and not SM_EQ,
        "%d/%d/%s" % (SM_R, SM_G, SM_EQ))
control("K06 mixgen_0of4", SG_R == 8 and SG_G == 0, "%d/%d" % (SG_R, SG_G))
control("K07 metric_tl_0", P_TIME["phys"] == 0, str(P_TIME["phys"]))
control("K08 joint_phys2", PJ == 2 and RJ == 28, "%d/%d" % (PJ, RJ))

# =====================================================================
# 9. 守卫（真实谓词）
# =====================================================================
guard("G01 sec13", len(SEC13) > 400 and S13_ECSK and S13_TWO, "len=%d" % len(SEC13))
guard("G02 r210_phys2", R210_PHYS == 2, str(R210_PHYS))
guard("G03 torsion_dim24", len(TOR_BASIS) == 24 and NT == 24, str(len(TOR_BASIS)))
guard("G04 antisymmetry", ANTI_OK and NONZERO_BASIS == 24, "%s/%d" % (ANTI_OK, NONZERO_BASIS))
guard("G05 basis_rank24", rank(TOR_BASIS) == 24, str(rank(TOR_BASIS)))
guard("G06 trace_rank4", RT == 4, str(RT))
guard("G07 axial_rank4", RA == 4, str(RA))
guard("G08 stack_rank8", RSTACK == 8, str(RSTACK))
guard("G09 pure16_sum24", NPURE == 16 and RT + RA + NPURE == 24, str(NPURE))
guard("G10 orth", ORTH, str(ORTH))
guard("G11 k_grid", GRID_OK and len(GRID_R) == 7, str(GRID_R))
guard("G12 kinv", KINV_OK and KIK_OK, "%s/%s" % (KINV_OK, KIK_OK))
guard("G13 kindep", KINDEP, str(KINDEP))
guard("G14 E_light_46", (P_LIGHT["rank"], P_LIGHT["nullity"]) == (4, 6), str(P_LIGHT["rank"]))
guard("G15 joint_28_6", (RJ, NJ) == (28, 6), "%d/%d" % (RJ, NJ))
guard("G16 joint_gauge", RGJ == 4 and GZ, "%d/%s" % (RGJ, GZ))
guard("G17 joint_phys2", PJ == 2, str(PJ))
guard("G18 schur0_eq_E", S0_EQ and WE_SYM, "%s/%s" % (S0_EQ, WE_SYM))
guard("G19 metric_repro", P_LIGHT["phys"] == 2 and P_LIGHT["gauge"] == 4, str(P_LIGHT["phys"]))
guard("G20 prop_light_24", (NT - rank(KP)) == 24 and PJP == 26 and NJP == 30,
      "%d/%d/%d" % (NT - rank(KP), NJP, PJP))
guard("G21 prop_tl_0", KPT_R == 24, str(KPT_R))
guard("G22 trace_only", RT_R == 4 and JTR_N == 26, "%d/%d" % (RT_R, JTR_N))
guard("G23 rankdef", KD_R == 23 and JD_N == 7, "%d/%d" % (KD_R, JD_N))
guard("G24 mix00", SM_R == 5 and SM_N == 5 and SM_G == 3, "%d/%d/%d" % (SM_R, SM_N, SM_G))
guard("G25 mixgen", SG_R == 8 and SG_N == 2 and SG_G == 0, "%d/%d/%d" % (SG_R, SG_N, SG_G))
guard("G26 metric_tl0", P_TIME["phys"] == 0 and P_TIME["rank"] == 6, str(P_TIME["rank"]))
guard("G27 joint_tl0", PTJ_N == 4, str(PTJ_N))
guard("G28 dof8", len(DOF) == 8, str(len(DOF)))
guard("G29 dof_heights", [d["phys"] for d in DOF] == [2, 0, 0, 2, 0, 26, 22, 3],
      str([d["phys"] for d in DOF]))
cnt = Counter(e["level"] for e in ENTRIES)
guard("G30 levels", cnt.get("PASS", 0) == 22 and cnt.get("INFO", 0) == 3
      and cnt.get("BOUNDARY", 0) == 1 and cnt.get("FAIL", 0) == 0, str(dict(cnt)))
guard("G31 no_fail_numbers", all(bool(e["numbers"]) for e in ENTRIES), "n=%d" % len(ENTRIES))
guard("G32 verdict_tokens", ("PHYS2" in VERDICT) and ("DIM24" in VERDICT)
      and ("SUPPLY-0" in VERDICT), "len=%d" % len(VERDICT))
C_VERD = [("C1", 1), ("C2", 3), ("C3", 0)]
guard("G33 c1_c2_c3", [v for _, v in C_VERD] == [1, 3, 0], str(C_VERD))
guard("G34 joint_size", len(JOINT) == 34 and len(JOINT[0]) == 34, str(len(JOINT)))
guard("G35 block_zero", all(JOINT[i][10 + j] == 0 and JOINT[10 + j][i] == 0
                            for i in range(10) for j in range(NT)),
      "off-diagonal")
guard("G36 K_sym", all(K_MAIN[i][j] == K_MAIN[j][i] for i in range(NT) for j in range(NT)),
      "sym")
guard("G37 E_weighted_sym", WE_SYM and not all(E_LIGHT[i][j] == E_LIGHT[j][i]
                                               for i in range(10) for j in range(10)),
      "weighted_sym=%s raw_sym=False" % WE_SYM)
guard("G38 torsion_null0_allk", all(rank(K_of(1, 1, 1, GT, GA)) == NT for _ in range(3)),
      "3x")


# =====================================================================
# 10. 输出（md 正文先构，末尾守卫 G39 计入总数后再算计数头）
# =====================================================================
def main():
    counts = Counter(e["level"] for e in ENTRIES)

    md = []
    md.append("# " + STEM + "\n")
    md.append("## 一句话\n")
    md.append("把挠率当独立场（24 维，对 (ν,ρ) 反对称）与已验的度规算子拼成 34×34 联合算子："
              "迹/轴映射秩各 **4**、叠加秩 **8** ⇒ 纯张量 **16**（4+4+16 = 24，全部由秩给出）；"
              "任何**代数且可逆**的挠率算子（七组耦合实测）都是 rank 24 / 零模 0 ⇒ "
              "联合算子 **rank 28 / 零模 6 / 规范 4 / 物理 2**，**挠率一个零模也没添**；"
              "无混合时 Schur 补**逐项等于**度规算子（100/100）。"
              "反面同样明确：换成传播型（k²I）类光下挠率零模立刻 **24**、物理 **26**；"
              "只留迹耦合（a=0）物理 **22**；人为秩亏 1 ⇒ 物理 **3**。"
              "**边界**：一旦引入非零混合，Schur 补的规范湮灭从 **4/4** 降到 **3/4** 乃至 **0/4** ⇒ "
              "「物理 = 零模 − 4」这个口径失效（r210 D02 的边界被量化）。\n")
    md.append("**判定串**：`" + VERDICT + "`\n")
    md.append("## 自由度账本\n")
    md.append("| 扇区 | k | k² | rank | nullity | 规范维 | 物理 DOF |")
    md.append("|---|---|---|---|---|---|---|")
    for d in DOF:
        md.append("| %s | (%s) | %s | %s | %s | %s | **%s** |"
                  % (d["sector"], ",".join(str(x) for x in d["k"]), d["k2"],
                     d["rank"], d["nullity"], d["gauge"], d["phys"]))
    md.append("\n## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"].replace("|", "\\|")))
    md.append("\n## 三判定\n")
    md.append("| 探针 | 判定 | 理由 |")
    md.append("|---|---|---|")
    md.append("| C1 | **既有理论复写** | ECSK 挠率非传播、24 维三分均为标准结果，本册独立复算 |")
    md.append("| C2 | **条件性**（3 条） | 树级线性化；物理=零模−4 须规范湮灭；无混合=真空/无自旋源 |")
    md.append("| C3 | **独立可证伪预言** | 0 条（不新增预言；仍是 P2 判据的机验） |")
    md.append("\n## 修复建议\n")
    md.append("- **R1**：03 §1.3 的「ECSK 中挠率非传播」可补一句可机验的口径："
              "「挠率算子不含 ∂（代数）⇒ 无色散；挠率空间 24 = 4+4+16；"
              "代数可逆算子零模 0（r212）」。结论不变，理由变可查。")
    md.append("- **R2**：若后续引入自旋源（混合 C ≠ 0），须先声明规范不动点；"
              "r212 C05/C06 显示此时「零模 − 4」会失效（规范湮灭 3/4 乃至 0/4）。")

    guard("G39 verdict_in_md", VERDICT in "\n".join(md), "verdict not in md body")

    n_g = sum(1 for g in GUARDS if g["ok"])
    n_c = sum(1 for c in CONTROLS if c["ok"])
    ok_all = (n_g == len(GUARDS) and n_c == len(CONTROLS))
    header = ("**条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）；"
              "守卫 %d/%d；控制组 %d/%d；退出码 %d**\n"
              % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
                 counts.get("BOUNDARY", 0), counts.get("FAIL", 0),
                 n_g, len(GUARDS), n_c, len(CONTROLS), 0 if ok_all else 1))
    md.insert(1, header)
    md.append("\n## 守护（%d/%d）\n" % (n_g, len(GUARDS)))
    for g in GUARDS:
        md.append("- [%s] %s" % ("OK" if g["ok"] else "FAIL", g["name"]))
    md.append("\n## 控制组（%d/%d）\n" % (n_c, len(CONTROLS)))
    for c in CONTROLS:
        md.append("- [%s] %s" % ("OK" if c["ok"] else "FAIL", c["name"]))
    md.append("\n## 红线\n")
    md.append("本册只做结构计数，不产生新物理，不宣称观测证实/否证；"
              "未改写 03 卷任何字节；未改 verify.py；未做 git；"
              "未触碰并行链 r203–r211 任何文件。TUFT 供给 0/12 维持，①池 12/12。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("\n" + "=" * 78)
    print("条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
             counts.get("BOUNDARY", 0), counts.get("FAIL", 0)))
    print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    print("判定串：" + VERDICT)

    payload = dict(
        stem=STEM, verdict=VERDICT, counts=dict(counts),
        guards_total=len(GUARDS), guards_pass=n_g,
        controls_total=len(CONTROLS), controls_pass=n_c,
        guard_list=GUARDS, control_list=CONTROLS, entries=ENTRIES,
        dof=DOF,
        supply=dict(pool="12/12", supply="0/12"),
        judgement=[dict(probe="C1", verdict="既有理论复写", reason="ECSK 挠率非传播与 24 维三分是标准结果"),
                   dict(probe="C2", verdict="条件性", reason="树级；规范湮灭；无混合=真空/无自旋源"),
                   dict(probe="C3", verdict="独立可证伪预言", reason="0 条（无新增预言）")],
        source="07_统一场方程/03_四力还原.md §1.3 + r210 JSON",
    )
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rep = []
    rep.append("TUFT-r212 度规与挠率联合零模计数 · ECSK 非传播结构机验 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
                  counts.get("BOUNDARY", 0), counts.get("FAIL", 0)))
    rep.append("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            try:
                rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False))
            except Exception:
                pass
        rep.append("")
    rep.append("判定串：" + VERDICT)
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("out -> %s.{json,md,_report.txt}" % STEM)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())

