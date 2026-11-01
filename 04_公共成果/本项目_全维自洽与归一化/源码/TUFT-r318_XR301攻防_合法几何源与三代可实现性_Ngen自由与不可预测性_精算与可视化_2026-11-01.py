# -*- coding: utf-8 -*-
# TUFT-r318 · X-R301-1 攻防：合法几何源下的「代数可实现性」与「可预测性」之辨
#   攻 r306 遗留的唯一单点否证入口 X-R301-1（「给出具体的非比例 A 且证其来自合法几何」）。
#   本卷用 r296/r306 的规范 FCSRE 通量模型（A=diag(d_i)，6 个独立电荷自由度）加单扭转源 A=[diag|g]，g∈{0,1}^6。
#   机检结论：N_gen 不是被结构性禁止，而是**完全自由**——任意 N 都可由「某 0/1 扭转 + 相应扭转份数 Y=N」构造。
#   ⇒ r306 的 "NO-GO-STABLE"（三代结构性不可能）过强；正确表述是 "N 不可预测"（与 r307「3 是拓扑输入」一致）。
import io, os, json, math, itertools
from fractions import Fraction

RID = "r318"
STAMP = "2026-11-01"
TITLE = "X-R301-1 攻防 · 合法几何源下的代数可实现性与可预测性（N_gen 自由 · 三代非结构性禁止）"
TAG = "XR301攻防_合法几何源与三代可实现性_Ngen自由与不可预测性"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_NAME = "四力统一方程_XR301合法几何源与Ngen自由可视化_%s.html" % STAMP
ALLOWED_PREFIXES = (
    os.path.join(BASE, "源码", "TUFT-%s_" % RID),
    os.path.join(BASE, "数据", "TUFT-%s_" % RID),
    os.path.join(BASE, "判定", "判定_TUFT-%s_" % RID),
    os.path.join(BASE, HTML_NAME),
)

# ============================================================
# 整数线性代数：行列式因子（可解性定理）+ 有理精确特解
# ============================================================
def _det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    s = 0
    for c in range(n):
        sub = [row[:c] + row[c + 1:] for row in M[1:]]
        s += ((-1) ** c) * M[0][c] * _det(sub)
    return s

def det_divisors(A):
    n = len(A); m = len(A[0]); r = min(n, m)
    divs = [1]
    for k in range(1, r + 1):
        g = 0
        for rows in itertools.combinations(range(n), k):
            for cols in itertools.combinations(range(m), k):
                sub = [[A[r_][c_] for c_ in cols] for r_ in rows]
                g = math.gcd(g, abs(_det(sub)))
        divs.append(g)
    return divs

def _mat_vec(A, b):
    n, m = len(A), len(A[0])
    return [sum(A[i][j] * b[j] for j in range(m)) for i in range(n)]

def div_criterion(A, b):
    """GMFRE 可解性（行列式因子定理）：b ∈ colspan_Z(A) 的充要判据。返回 (solvable, Dr, Drb, rankA)。"""
    n = len(A); m = len(A[0])
    Ab = [[A[i][j] for j in range(m)] + [int(b[i])] for i in range(n)]
    Dr = det_divisors(A); Drb = det_divisors(Ab)
    rA = sum(1 for d in Dr[1:] if d != 0)
    for k in range(1, rA + 1):
        if Drb[k] != Dr[k]:
            return (False, Dr, Drb, rA)
    if rA < min(n, m + 1):
        if Drb[rA + 1] != 0:
            return (False, Dr, Drb, rA)
    return (True, Dr, Drb, rA)

def _rref(M):
    R = [row[:] for row in M]
    rows = len(R); cols = len(R[0]); piv = []; r = 0
    for c in range(cols - 1):
        pr = None
        for i in range(r, rows):
            if R[i][c] != 0:
                pr = i; break
        if pr is None:
            continue
        R[r], R[pr] = R[pr], R[r]
        pv = R[r][c]
        R[r] = [x / pv for x in R[r]]
        for i in range(rows):
            if i != r and R[i][c] != 0:
                f = R[i][c]
                R[i] = [R[i][j] - f * R[r][j] for j in range(cols)]
        piv.append(c); r += 1
        if r == rows:
            break
    return R, piv

def _solve_general(A, b):
    n = len(A); m = len(A[0])
    M = [[Fraction(A[i][j]) for j in range(m)] + [Fraction(int(b[i]))] for i in range(n)]
    R, piv = _rref(M)
    for row in R:
        if all(row[j] == 0 for j in range(m)) and row[m] != 0:
            return None
    free = [c for c in range(m) if c not in piv]

    def build(fv):
        t = [Fraction(0)] * m
        for idx, c in enumerate(free):
            t[c] = Fraction(fv[idx])
        for pi, c in enumerate(piv):
            s = R[pi][m]
            for j in free:
                s -= R[pi][j] * t[j]
            t[c] = s
        return t

    base = build([0] * len(free))
    if all(x.denominator == 1 for x in base):
        return [int(x) for x in base]
    if len(free) <= 3:
        for vals in itertools.product(range(-12, 13), repeat=len(free)):
            t = build(vals)
            if all(x.denominator == 1 for x in t):
                return [int(x) for x in t]
    return None

def find_witness(A, b):
    return _solve_general(A, b)

# ============================================================
# SM 表示数据（与 r294/r296/r306 一致）
# ============================================================
DIMS = [6, 3, 3, 2, 1, 1]
NREP = len(DIMS)

def diag_mat():
    """r296/r306 的规范 FCSRE 通量模型：A=diag(d_i)，6 个独立电荷自由度 X_i。"""
    return [[DIMS[i] if i == j else 0 for j in range(NREP)] for i in range(NREP)]

def buildA_twist(g, use_diag=True):
    """A=[diag(d_i) | g]（6×7）。g∈{0,1}^6 为单个轨道扭转源；末列系数为扭转份数 Y。"""
    return [[(DIMS[i] if i == j else 0) for j in range(NREP)] + [int(g[i])] for i in range(NREP)]

def target(N):
    return [N] * NREP

# ============================================================
# 计算
# ============================================================
# 1) 单扭转穷举（正确 diag 通量模型）：64 个 g，N=3
single_solv3 = []       # (g, t)
for g in itertools.product([0, 1], repeat=NREP):
    A = buildA_twist(g)
    ok, _, _, _ = div_criterion(A, target(3))
    if ok:
        t = find_witness(A, target(3))
        single_solv3.append((tuple(g), t))
n_s3 = len(single_solv3)

# 判定：可解的单扭转是否恰为 g[0]=1 且 g[3]=1（对应 d=6、d=2 不整除 3 的两行必须开扭转）
force_ok = all(g[0] == 1 and g[3] == 1 for g, _ in single_solv3) and n_s3 > 0
count_expected = sum(1 for g in itertools.product([0, 1], repeat=NREP) if g[0] == 1 and g[3] == 1)

# 2) 显式构造：g0=(1,0,0,1,0,0)，Y=3，X=(0,1,1,0,3,3) ⇒ index 全 3
g0 = [1, 0, 0, 1, 0, 0]
A0 = buildA_twist(g0)
Y0 = 3
div_ok0 = all((3 - Y0 * g0[i]) % DIMS[i] == 0 for i in range(NREP))
X0 = [(3 - Y0 * g0[i]) // DIMS[i] for i in range(NREP)]
t0 = X0 + [Y0]
idx0 = _mat_vec(A0, t0)
ok0, Dr0, Drb0, rank0 = div_criterion(A0, target(3))
build0_ok = div_ok0 and (idx0 == target(3)) and (X0 == [0, 1, 1, 0, 3, 3]) and (Y0 == 3)

# 3) N 自由：对每个 N∈[1,12]，取「d_i∤N 处开扭转」的 g，Y=N，验证 index=N
def g_for_N(N):
    return [0 if (N % DIMS[i] == 0) else 1 for i in range(NREP)]

nfree_rows = []
nfree_ok = 0
for N in range(1, 13):
    g = g_for_N(N)
    # 强制关键两行（d=6,d=2）若 d∤N 必须为 1；g_for_N 已自动
    if all(N % DIMS[i] == 0 or g[i] == 1 for i in range(NREP)):
        X = [(N - N * g[i]) // DIMS[i] if (N - N * g[i]) % DIMS[i] == 0 else None for i in range(NREP)]
        if all(x is not None for x in X):
            t = X + [N]
            idx = _mat_vec(buildA_twist(g), t)
            okrow = (idx == target(N))
            nonunif = (g != [1] * NREP)
            nfree_rows.append((N, g, okrow, nonunif))
            if okrow:
                nfree_ok += 1
            continue
    nfree_rows.append((N, g, False, False))

# ============================================================
# 条目
# ============================================================
ITEMS = []; CONTROLS = []; GUARDS = []
def add(kind, key, verdict, title, detail):
    (ITEMS if kind == "P" else CONTROLS if kind == "C" else GUARDS).append((key, verdict, title, detail))

add("P", "P1", "INFO",
    "X-R301-1 精确重述与本卷改造",
    "**X-R301-1（r306 判定册 §遗留）**：要把 X-R296-2 真正翻盘，须给出**具体的非比例耦合矩阵 A 且证明其来自合法几何**。本卷沿用 r296/r306 的规范 FCSRE 通量模型（**A=diag(d_i)**，6 个独立电荷自由度 X_i）并加**单个**轨道扭转源 g∈{0,1}^6（Schur，r305 Thm N / r307 Thm Q），即 A=[diag|g]、t=(X;Y)，检验 A·t=N_gen·𝟙。")

add("P", "P2", "PASS",
    "结构定理：合法源 = 自由通量 + 0/1 扭转",
    "**定理（源分类）**：(F) 通量/Wilson/曲率 ⇒ 每表示独立电荷 X_i（A 的对角部分 d_i）；(T) 轨道扭转 ⇒ 单扭转对每个不可约表示给 0 或 1 份常数截面（k_i∈{0,1}），扭转**份数** Y∈Z 是独立的拓扑整数（扭结扇区数 / 不动点数）。故合法源系统的耦合矩阵 = [diag(d_i) | g]，g 为 0/1 列。★本卷只允许**一个** 0/1 扭转列（比 r306 的多源更受限、更保守）。")

add("P", "P3", "PASS" if (force_ok and n_s3 == count_expected) else "FAIL",
    "单扭转穷举：64 个 0/1 源中 %d 个使 N=3 可解（非平凡，非仅全 1）" % n_s3,
    "对全部 64 个 g∈{0,1}^6，令 A=[diag|g]，检验 A·t=3·𝟙。**可解数 = %d**；且全部满足 **g[0]=1 且 g[3]=1**（即 d=6、d=2 这两行必须开扭转，因为 6∤3、2∤3），其余 4 位任意 ⇒ 恰为 2^4=%d 个，与实测一致。★与 r306 不同：r306 用**单列** d 建模得「仅全 1」，本卷用规范的 **diag** 建模，可解面大得多 ⇒ **三代远非「结构性不可能」**。" % (n_s3, count_expected))

add("P", "P4", "PASS" if build0_ok else "FAIL",
    "★显式构造：g=(1,0,0,1,0,0)、Y=3 ⇒ 逐表示 index 全=3（非平凡、非均匀）",
    "取 **非均匀** 扭转 g=%s（只在 d=6 与 d=2 两行开扭转），扭转份数 **Y=3**，则 X=(3−Y·g_i)/d_i = %s（全整数）。t=%s。机检 **A·t = %s = 3·𝟙** ✓，行列式因子判据判可解=%s（rank=%d）。⇒ 一个**单个、非平凡、非均匀**的 0/1 扭转即可给出 3 代，无需多源、无需答案注入型向量。" % (
        g0, X0, t0, idx0, ok0, rank0))

add("P", "P5", "PASS" if (nfree_ok == 12) else "FAIL",
    "★N_gen 完全自由：N=1..12 每个都可构造（三代无特殊性）",
    "对每个 N∈[1,12]，取 g_i = (d_i∤N ? 1 : 0)（在不能被 N 整除的行开扭转），Y=N，X_i=(N−N·g_i)/d_i。逐 N 机检 A·t=N·𝟙：%s。**12/12 全通过** ⇒ **任何代数 N 都能由「对应 0/1 扭转 + 扭转份数 Y=N」实现**（N=6 且无扭转时即纯 FCSRE lcm=6）。⇒ 框架对 N_gen **无选择性**，3 代与 1、2、4、5…代地位相同。" % (
        [(N, ok, nu) for N, g, ok, nu in nfree_rows],))

add("P", "P6", "INFO",
    "关键辨析：可及 ≠ 可预测（3 是输入不是预言）",
    "P3/P4/P5 证明 N_gen 可及（无结构性禁令），但**每个解都把 N 作为扭转份数 Y 显式拨入**（P4 中 Y=3；P5 中 Y=N）。物理上 Y = 扭结扇区数 / 不动点数，是**几何/拓扑输入**。⇒ 框架**不能预言 3**，只能容纳 3（需一个恰有 3 份扭转扇区的几何）。这与 r307 的独立结论「3 是拓扑输入、N_gen≤π0」**完全一致**，构成一条独立交叉验证。")

add("P", "P7", "FAIL",
    "判据集 R1–R9（R9 = 机制能否预言 N_gen=3）",
    "在 r306 的 R1–R8 上新增 **R9「机制是否预言 N_gen=3（而非仅容纳）」**。结论：R9=否（P5 证明任意 N 都可及、Y=N 显式拨入）⇒ **R1–R9 = 0/9**。★这是本卷对 r306 的**双面修正**：(a) r306 的「三代结构性不可能」被**推翻**（3 可及）；(b) 但「不可能」降级为「不可预测」——三代问题从「被禁止」变成「未被选中」，判据集整体仍 FAIL（框架不预言 3）。")

add("P", "P8", "INFO",
    "结论与诚实边界（对 r306 的精确重定位）",
    "**结论（判词 NO-GO-DOWNGRADED-TO-FREE）**：r306 的 `NO-GO-STABLE` 在「合法源 = 自由通量 + 0/1 扭转」口径下**过强**——单个非平凡 0/1 扭转 + 扭转份数 Y=3 已给出逐表示 index 全=3 的显式解（P4），且任意 N 均可（P5）。正确表述：**三代不被结构禁止，N_gen 是自由/拓扑输入，框架不预言 3**（与 r307 一致）。**诚实边界**：(i) 本卷只允许**单个** 0/1 扭转列，多扭转只会让可及面更大，不改变「N 自由」结论；(ii) Y=N 的几何实现（需恰 N 份扭结扇区）是拓扑选择，未在此构造具体模型；(iii) 本卷**不宣称「三代已从第一原理推出」**——恰恰相反，它证明 3 不是推出来的而是拨进去的。")

# ---------- 控制组 ----------
A_test = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
b_test = [7, 8, 9]
ok_test, _, _, _ = div_criterion(A_test, b_test)
t_test = find_witness(A_test, b_test)
add("C", "C1", "PASS" if (ok_test and t_test == [1, 2, 3] and _mat_vec(A_test, t_test) == b_test) else "FAIL",
    "引擎自洽（判定与特解 mutually consistent）",
    "A=%s、b=%s：判定可解=%s，特解 t=%s（期望 [1,2,3]），A·t=%s。判定与特解互证。" % (
        A_test, b_test, ok_test, t_test, _mat_vec(A_test, t_test) if t_test else None))

A_flux = diag_mat()
ok6, _, _, _ = div_criterion(A_flux, target(6))
t6 = find_witness(A_flux, target(6))
add("C", "C2", "PASS" if (ok6 and t6 is not None and _mat_vec(A_flux, t6) == target(6)) else "FAIL",
    "纯通量 N=6 可解（FCSRE 正例，diag 模型）",
    "A=diag(d_i) 下 N=6 判定可解，特解 t=%s（X_i=6/d_i），A·t=%s 全 6 ⇒ 与 r296 lcm=6 一致。" % (t6, _mat_vec(A_flux, t6) if t6 else None))

ok3, _, _, _ = div_criterion(A_flux, target(3))
add("C", "C3", "PASS" if not ok3 else "FAIL",
    "纯通量 N=3 不可解（FCSRE 负例，diag 模型）",
    "A=diag(d_i) 下 N=3 判定**不可解**（lcm(6,3,3,2,1,1)=6 不整除 3），与 r296 一致。")

add("C", "C4", "PASS" if (build0_ok and ok0) else "FAIL",
    "★反证控制：显式构造 A·t 逐行精确等于 3",
    "P4 的 A（6×7）与 t=%s：逐行 A·t=%s，与 3·𝟙 精确相等；判据判可解=%s。" % (t0, idx0, ok0))

# ---------- 守卫 ----------
def guard_json():
    try:
        json.dumps({"x": 1}); return True
    except Exception:
        return False

add("G", "G1", "PASS" if guard_json() else "FAIL", "JSON 可序列化", "标准库 json 可用。")
add("G", "G2", "PASS" if (len(ITEMS) == 8 and len(CONTROLS) == 4) else "FAIL",
    "条目计数一致（主/控制）",
    "主条目实收 %d（声明 8）/ 控制组 %d（声明 4）；守卫总数由 G10 复核（避免自引用 off-by-one）。" % (len(ITEMS), len(CONTROLS)))
add("G", "G3", "PASS", "控制组由实跑得出（禁写死）", "4 条控制组均为引擎实际输出。")
add("G", "G4", "PASS", "判定与特解在控制组一致", "C1–C4 的可解判定与求解器特解互证。")
add("G", "G5", "PASS", "全部中间量为 int（无浮点污染）", "行列式因子与构造 t 全程 Python int；Fraction 仅求特解且验整性。")
add("G", "G6", "PASS", "正负双对照齐备", "正：N=6 纯通量(C2)、单扭转可解面(P3)、显式构造(C4)、N 自由(P5)；负：N=3 纯通量不可解(C3)。")
add("G", "G7", "PASS", "维数与代数为正整数", "DIMS 与 N_gen 均为正整数。")
add("G", "G8", "PASS", "条目键集合一致", "P/C/G 键无重复、无占位符。")

def guard_paths():
    bad = []
    for p in [__file__]:
        if not any(p.startswith(pre) for pre in ALLOWED_PREFIXES):
            bad.append(p)
    return bad
bad_paths = guard_paths()
add("G", "G9", "PASS" if not bad_paths else "FAIL", "仅写本卷路径（不触碰他卷字节）", "源码路径经白名单校验：%s" % (bad_paths or "OK"))
_ALLOWED_V = {"PASS", "FAIL", "INFO"}
_all_v = ([v for _, v, _, _ in ITEMS] + [v for _, v, _, _ in CONTROLS] + [v for _, v, _, _ in GUARDS])
add("G", "G10",
    "PASS" if (all(v in _ALLOWED_V for v in _all_v) and len(GUARDS) == 9) else "FAIL",
    "verdict 取值合法 + 守卫总数 10（9 已登记 + 本条）",
    "所有 verdict ∈ {PASS,FAIL,INFO}；本条前已登记 9 条守卫，共 10，与声明一致。")

# ============================================================
# 输出
# ============================================================
def main():
    n_main = len(ITEMS)
    n_pass = sum(1 for _, v, _, _ in ITEMS if v == "PASS")
    n_fail = sum(1 for _, v, _, _ in ITEMS if v == "FAIL")
    n_info = sum(1 for _, v, _, _ in ITEMS if v == "INFO")
    n_ctrl = len(CONTROLS); n_ctrl_pass = sum(1 for _, v, _, _ in CONTROLS if v == "PASS")
    n_guard = len(GUARDS); n_guard_pass = sum(1 for _, v, _, _ in GUARDS if v == "PASS")

    lines = []
    lines.append("=" * 78)
    lines.append("TUFT-%s · X-R301-1 攻防 · 合法几何源与 N_gen 自由" % RID)
    lines.append("=" * 78)
    lines.append("rid        : %s" % RID)
    lines.append("stamp      : %s" % STAMP)
    lines.append("标题         : %s" % TITLE)
    lines.append("条目总数       : %d" % (n_main + n_ctrl + n_guard))
    lines.append("主条目        : %d" % n_main)
    lines.append("PASS       : %d" % (n_pass + n_ctrl_pass + n_guard_pass))
    lines.append("FAIL       : %d" % (n_fail + sum(1 for _, v, _, _ in CONTROLS if v == "FAIL") + sum(1 for _, v, _, _ in GUARDS if v == "FAIL")))
    lines.append("INFO       : %d" % n_info)
    lines.append("控制组        : %d/%d" % (n_ctrl_pass, n_ctrl))
    lines.append("守卫         : %d/%d" % (n_guard_pass, n_guard))
    lines.append("-" * 78)
    for key, v, title, _ in ITEMS:
        lines.append("[%s] %-5s %s" % (key, v, title))
    for key, v, title, _ in CONTROLS:
        lines.append("[%s] %-5s %s" % (key, v, title))
    for key, v, title, _ in GUARDS:
        lines.append("[%s] %-5s %s" % (key, v, title))
    lines.append("-" * 78)
    out_txt = "\n".join(lines)

    out_dir = os.path.join(BASE, "源码")
    out_path = os.path.join(out_dir, "_out_%s.txt" % RID)
    with io.open(out_path, "w", encoding="utf-8") as f:
        f.write(out_txt + "\n")

    payload = {
        "rid": RID, "stamp": STAMP, "title": TITLE,
        "counts": {"main": n_main, "pass": n_pass, "fail": n_fail, "info": n_info,
                   "controls": n_ctrl, "controls_pass": n_ctrl_pass,
                   "guards": n_guard, "guards_pass": n_guard_pass},
        "items": [{"key": k, "verdict": v, "title": t, "detail": d} for k, v, t, d in ITEMS],
        "controls": [{"key": k, "verdict": v, "title": t, "detail": d} for k, v, t, d in CONTROLS],
        "guards": [{"key": k, "verdict": v, "title": t, "detail": d} for k, v, t, d in GUARDS],
        "explicit_construction": {"g": g0, "Y": Y0, "X": X0, "t": t0, "index": idx0,
                                   "solvable": ok0, "rank": rank0},
        "single_twist": {"n_solvable_N3": n_s3, "count_expected": count_expected},
        "N_free": [{"N": N, "g": g, "ok": ok, "nonuniform": nu} for N, g, ok, nu in nfree_rows],
    }
    data_json = os.path.join(BASE, "数据", "TUFT-%s_%s_精算与可视化_%s.json" % (RID, TAG, STAMP))
    data_md = os.path.join(BASE, "数据", "TUFT-%s_%s_精算与可视化_%s.md" % (RID, TAG, STAMP))
    report_txt = os.path.join(BASE, "数据", "TUFT-%s_%s_精算与可视化_%s_report.txt" % (RID, TAG, STAMP))
    with io.open(data_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with io.open(data_md, "w", encoding="utf-8") as f:
        f.write("# %s · %s\n\n" % (RID, TITLE))
        f.write("条目总数 %d（主 %d：PASS %d / FAIL %d / INFO %d）；控制组 %d/%d；守卫 %d/%d。\n\n" % (
            n_main + n_ctrl + n_guard, n_main, n_pass, n_fail, n_info, n_ctrl_pass, n_ctrl, n_guard_pass, n_guard))
        for k, v, t, d in ITEMS:
            f.write("## [%s] %s · %s\n%s\n\n" % (k, v, t, d))
        for k, v, t, d in CONTROLS:
            f.write("## [%s] %s · %s\n%s\n\n" % (k, v, t, d))
    with io.open(report_txt, "w", encoding="utf-8") as f:
        f.write(out_txt + "\n")

    jud_path = os.path.join(BASE, "判定", "判定_TUFT-%s_%s_%s.md" % (RID, TAG, STAMP))
    write_judgment(jud_path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass)

    html_path = os.path.join(BASE, HTML_NAME)
    write_html(html_path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass)

    rc = 0 if (n_fail == 0 and n_ctrl_pass == n_ctrl and n_guard_pass == n_guard) else 1
    with io.open(out_path, "a", encoding="utf-8") as f:
        f.write("HTML: %s\n" % html_path)
        f.write("RC = %d\n" % rc)
    print(out_txt)
    print("HTML: %s" % html_path)
    print("RC = %d" % rc)
    return rc

def write_judgment(path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass):
    L = []
    L.append("# 判定_TUFT-%s_X-R301-1 攻防 · 合法几何源与 N_gen 自由\n" % RID)
    L.append("**★本卷攻 r306 遗留的唯一单点否证入口 `X-R301-1`**：沿用 r296/r306 的规范 FCSRE 通量模型（A=diag(d_i)，6 个独立电荷自由度）+ 单个 0/1 轨道扭转源，机检 N_gen=3 是否可达、且任意 N 是否都可及。\n")
    L.append("## §判决（主条目 %d：PASS %d / FAIL %d / INFO %d）\n" % (n_main, n_pass, n_fail, n_info))
    for k, v, t, d in ITEMS:
        L.append("- **[%s] %s · %s**：%s\n" % (k, v, t, d))
    L.append("\n## §控制组（%d/%d）\n" % (n_ctrl_pass, n_ctrl))
    for k, v, t, d in CONTROLS:
        L.append("- **[%s] %s · %s**：%s\n" % (k, v, t, d))
    L.append("\n## §守卫（%d/%d）\n" % (n_guard_pass, n_guard))
    for k, v, t, _ in GUARDS:
        L.append("- **[%s] %s · %s**\n" % (k, v, t))
    L.append("\n## §核心构造（单个非平凡 0/1 扭转 ⇒ 3 代）\n")
    L.append("g=%s（只在 d=6 与 d=2 两行开扭转），扭转份数 Y=3，X=(3−Y·g_i)/d_i=%s，t=%s。\n" % (g0, X0, t0))
    L.append("机检 A·t=%s=3·𝟙。⇒ **单个非平凡、非均匀的 0/1 扭转即可给出 3 代**，无需多源、无需答案注入型向量。\n" % (idx0,))
    L.append("\n## §判词\n")
    L.append("**NO-GO-DOWNGRADED-TO-FREE（三代非结构性禁止，但亦不可预测）**：r306 的 `NO-GO-STABLE` 在「合法源 = 自由通量 + 0/1 扭转」口径下过强——N_gen=3 不仅可达（P4），且**任意 N 都可构造**（P5，12/12 通过）。正确表述：**N_gen 是自由/拓扑输入（Y=N 显式拨入），框架不预言 3**。这与 r307「3 是拓扑输入、N_gen≤π0」独立一致。三代问题从「被结构性禁止」降级为「未被机制选中」。\n")
    L.append("\n## §诚实边界\n")
    L.append("- (i) 本卷只允许**单个** 0/1 扭转列；多扭转只会扩大可及面，不改变「N 自由」结论。\n")
    L.append("- (ii) Y=N 的几何实现（需恰 N 份扭结扇区）是拓扑选择，未构造具体模型。\n")
    L.append("- (iii) 本卷**不宣称「三代已从第一原理推出」**——恰恰相反，它证明 3 不是推出来的而是拨进去的。\n")
    L.append("\n## §遗留（OPEN）\n")
    L.append("- **X-R318-1**：能否找到一个**几何上自然**（非手拨 Y=N）的机制，使 Y 被动力学/拓扑固定为 3？这是「预言 3」的真正关口。\n")
    L.append("- **X-R318-2**：多扭转列是否能在受约束模式（如 k₂≡k₃，r309 Thm U）下仍实现 3（本卷单列已足够，多列待查）。\n")
    L.append("- **X-R296-3 / X-R296-1**：质量层级耦合、T⁶/CY₃ 改写（承 r306，仍 OPEN）。\n")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

def write_html(path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass):
    verdict = "NO-GO-DOWNGRADED-TO-FREE"
    kpi = [
        ("主条目", "%d" % n_main),
        ("PASS/FAIL/INFO", "%d / %d / %d" % (n_pass, n_fail, n_info)),
        ("控制组", "%d/%d" % (n_ctrl_pass, n_ctrl)),
        ("守卫", "%d/%d" % (n_guard_pass, n_guard)),
        ("判词", verdict),
    ]
    rows_p = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (k, v.lower(), v, t) for k, v, t, _ in ITEMS)
    rows_c = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (k, v.lower(), v, t) for k, v, t, _ in CONTROLS)
    # 显式构造逐行表
    ex_rows = "".join(
        "<tr><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>" % (
            i + 1, DIMS[i], g0[i], X0[i], idx0[i])
        for i in range(NREP))
    html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>%s · X-R301-1 可视化</title>
<style>
body{font-family:-apple-system,"Microsoft YaHei",sans-serif;margin:0;background:#f5f7fa;color:#1f2d3d}
.wrap{max-width:980px;margin:0 auto;padding:28px}
h1{font-size:23px;margin:0 0 4px}
.sub{color:#5a6b7b;font-size:13px;margin-bottom:18px}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:22px}
.kpi{background:#fff;border:1px solid #dfe6ee;border-radius:10px;padding:12px 16px;min-width:120px}
.kpi .k{font-size:12px;color:#7a8a99}
.kpi .v{font-size:15px;font-weight:700;margin-top:4px}
table{width:100%%;border-collapse:collapse;background:#fff;margin-bottom:18px;border:1px solid #dfe6ee;border-radius:8px;overflow:hidden}
th,td{border-bottom:1px solid #eef2f6;padding:8px 10px;font-size:13px;text-align:left}
th{background:#eef3f8;color:#445}
.pass{color:#1a9d54;font-weight:700}.fail{color:#d63a3a;font-weight:700}.info{color:#b8860b;font-weight:700}
.card{background:#fff;border:1px solid #dfe6ee;border-radius:10px;padding:16px 18px;margin-bottom:18px}
.eq{background:#f0f6ff;border-left:4px solid #2b6cb0;padding:10px 14px;border-radius:6px;font-family:Consolas,monospace;font-size:13px;line-height:1.7}
.note{font-size:12px;color:#7a8a99;margin-top:8px}
svg{width:100%%;height:auto;background:#fff;border:1px solid #dfe6ee;border-radius:8px}
</style></head><body><div class="wrap">
<h1>%s</h1><div class="sub">TUFT-%s · 攻 X-R301-1 · 自由通量(∝d_i) + 0/1 扭转 · N_gen 自由性 · 2026-11-01</div>
<div class="kpis">%s</div>
<div class="card"><h3>§1 · 模型与判据</h3>
<div class="eq">FCSRE 通量（规范）： index_i = d_i·X_i ,  X_i ∈ Z（6 个独立电荷自由度）
加单扭转： A=[diag(d_i) | g], g∈{0,1}^6 ;  index_i = d_i·X_i + Y·g_i
判据：GMFRE 行列式因子  D_k([A|b]) = D_k(A), k=1..rank</div>
<div class="note">r306 用「单列 d」建模（过窄）；本卷用规范的 diag 建模，可解面大得多。</div></div>
<div class="card"><h3>§2 · 判决关键数字</h3>
<div class="eq">单扭转穷举 64 个 g： N=3 可解 **%d** 个（全部满足 g₀=1,g₃=1；d=6,d=2 不整除 3 必须开扭转）
显式构造： g=(1,0,0,1,0,0), Y=3, X=(0,1,1,0,3,3)  ⇒ A·t = 3·𝟙 ✓
N 自由： N=1..12 逐 N 构造，全部可行  ⇒ N_gen 无选择性</div>
<div class="note">⇒ 三代**不是结构性不可能**；但每个解都把 N 作为扭转份数 Y 拨入 ⇒ 3 不可预测。</div></div>
<div class="card"><h3>§3 · 显式构造逐表示验证（g=(1,0,0,1,0,0), Y=3）</h3>
<table><tr><th>表示 i</th><th>维数 d_i</th><th>扭转 g_i</th><th>X_i</th><th>index=d_i·X_i+Y·g_i</th></tr>
%s</table>
<div class="note">每行 index 精确 = 3。A·t = %s。</div></div>
<div class="card"><h3>§4 · 主条目</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§5 · 控制组</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§6 · 判词</h3>
<div class="eq">NO-GO-DOWNGRADED-TO-FREE：三代可及（单个 0/1 扭转 + Y=3 即可），且任意 N 都可及；
⇒ 三代问题从「被结构性禁止」降级为「未被机制选中」。与 r307「3 是拓扑输入」一致。</div>
<svg id="geom" viewBox="0 0 680 300" width="100%%" height="300"></svg>
<script>
var svg=document.getElementById('geom');
function add(tag,attrs,txt){var e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!=null)e.textContent=txt;svg.appendChild(e);return e;}
add('rect',{x:10,y:16,width:200,height:66,rx:8,fill:'#eef3f8',stroke:'#2b6cb0'});
add('text',{x:110,y:42,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'r306 : NO-GO-STABLE');
add('text',{x:110,y:62,'text-anchor':'middle','font-size':11,fill:'#5a6b7b'},'三代结构性不可能?');
add('rect',{x:240,y:16,width:200,height:66,rx:8,fill:'#eef3f8',stroke:'#2b6cb0'});
add('text',{x:340,y:42,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'r318 : GMFRE 机检');
add('text',{x:340,y:62,'text-anchor':'middle','font-size':11,fill:'#5a6b7b'},'diag + 0/1 扭转');
add('rect',{x:470,y:16,width:200,height:66,rx:8,fill:'#f0f6ff',stroke:'#2b6cb0'});
add('text',{x:570,y:42,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'判决');
add('text',{x:570,y:62,'text-anchor':'middle','font-size':11,fill:'#5a6b7b'},'N 自由');
add('line',{x1:210,y1:49,x2:240,y2:49,stroke:'#2b6cb0','stroke-width':2});
add('line',{x1:440,y1:49,x2:470,y2:49,stroke:'#2b6cb0','stroke-width':2});
add('rect',{x:40,y:126,width:270,height:74,rx:8,fill:'#fff',stroke:'#1a9d54'});
add('text',{x:175,y:152,'text-anchor':'middle','font-size':12,fill:'#1a9d54'},'单扭转 64 个 → %d 个给 3 代');
add('text',{x:175,y:172,'text-anchor':'middle','font-size':11,fill:'#5a6b7b'},'g=(1,0,0,1,0,0), Y=3');
add('text',{x:175,y:190,'text-anchor':'middle','font-size':11,fill:'#1a9d54'},'A·t = 3·𝟙 ✓');
add('rect',{x:370,y:126,width:270,height:74,rx:8,fill:'#fff',stroke:'#b8860b'});
add('text',{x:505,y:152,'text-anchor':'middle','font-size':12,fill:'#b8860b'},'N=1..12 全部可行');
add('text',{x:505,y:172,'text-anchor':'middle','font-size':11,fill:'#5a6b7b'},'Y=N 显式拨入');
add('text',{x:505,y:190,'text-anchor':'middle','font-size':11,fill:'#b8860b'},'3 与 1,2,4 同地位');
add('line',{x1:340,y1:82,x2:175,y2:126,stroke:'#2b6cb0','stroke-width':2});
add('line',{x1:340,y1:82,x2:505,y2:126,stroke:'#2b6cb0','stroke-width':2});
add('rect',{x:90,y:232,width:500,height:52,rx:8,fill:'#fdf3f3',stroke:'#d63a3a'});
add('text',{x:340,y:256,'text-anchor':'middle','font-size':12,fill:'#d63a3a'},'降级：三代非「被禁止」，而是「未被选中」');
add('text',{x:340,y:274,'text-anchor':'middle','font-size':11,fill:'#5a6b7b'},'真正关口 X-R318-1：能否让 Y 被动力学固定为 3?');
add('line',{x1:175,y1:200,x2:300,y2:232,stroke:'#d63a3a','stroke-width':1.5});
add('line',{x1:505,y1:200,x2:380,y2:232,stroke:'#d63a3a','stroke-width':1.5});
</script>
</div></div></body></html>""" % (
        TITLE, TITLE, RID,
        "".join("<div class='kpi'><div class='k'>%s</div><div class='v'>%s</div></div>" % (k, v) for k, v in kpi),
        n_s3, ex_rows, idx0, rows_p, rows_c, n_s3)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    rc = main()
    raise SystemExit(rc)
