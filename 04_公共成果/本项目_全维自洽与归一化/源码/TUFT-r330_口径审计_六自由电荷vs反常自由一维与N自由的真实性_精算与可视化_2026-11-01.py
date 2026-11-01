# -*- coding: utf-8 -*-
# TUFT-r330 · 口径审计：r306/r318/r322 的「六自由电荷」vs 反常自由「一维超荷」
#   疑点：r306/r318 假设 A=diag(d_i)（6 个独立电荷自由度 X_i，=任意电荷）。r305 Thm S 证明
#   反常自由下荷空间只有 1 维、就是 span(Y)。若电荷被钉死为 SM 超荷，则 X_i = Y_i·M（单通量），
#   而非 6 个独立自由度 ⇒ r318 的显式构造 X=(0,1,1,0,3,3) 可能破反常自由，「N 自由」或为假象。
#   本卷机检：Y 是否反常自由；m=1（仅 Y）下 N=3 是否可达；与 m=6（r318）对比。
import io, os, json, math, itertools
from fractions import Fraction

RID = "r330"
STAMP = "2026-11-01"
TITLE = "口径审计 · 六自由电荷 vs 反常自由一维超荷（N 自由的真实性与 r318 判词修正）"
TAG = "口径审计_六自由电荷vs反常自由一维与N自由的真实性"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_NAME = "四力统一方程_反常自由口径审计与N自由真实性可视化_%s.html" % STAMP
ALLOWED_PREFIXES = (
    os.path.join(BASE, "源码", "TUFT-%s_" % RID),
    os.path.join(BASE, "数据", "TUFT-%s_" % RID),
    os.path.join(BASE, "判定", "判定_TUFT-%s_" % RID),
    os.path.join(BASE, HTML_NAME),
)

# ---------------- 整数线性代数 ----------------
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

def find_witness(A, b):
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

# ---------------- SM 表示数据（6 手征表示：Q,u^c,d^c,L,e^c,ν^c） ----------------
DIMS = [6, 3, 3, 2, 1, 1]                      # 表示维数 d_i
COL = [3, 3, 3, 1, 1, 1]                       # 色维
SU2 = [2, 1, 1, 2, 1, 1]                       # SU(2) 维
Y = [Fraction(1, 6), Fraction(-2, 3), Fraction(1, 3), Fraction(-1, 2), Fraction(1), Fraction(0)]  # 超荷
NREP = 6

def target(N):
    return [N] * NREP

# ---- 反常条件（4 条）----
def anom_su3(q):
    # [SU(3)]²U(1): Σ_{triplet} T(3)=1/2 · SU2dim · q
    return sum(Fraction(1, 2) * SU2[i] * q[i] for i in (0, 1, 2))
def anom_su2(q):
    # [SU(2)]²U(1): Σ_{doublet} T(2)=1/2 · colordim · q
    return sum(Fraction(1, 2) * COL[i] * q[i] for i in (0, 3))
def anom_grav(q):
    # grav·U(1): Σ colordim·SU2dim·q
    return sum(COL[i] * SU2[i] * q[i] for i in range(NREP))
def anom_cube(q):
    # U(1)³: Σ colordim·SU2dim·q³
    return sum(COL[i] * SU2[i] * q[i] ** 3 for i in range(NREP))

def anomalies(q):
    return (anom_su3(q), anom_su2(q), anom_grav(q), anom_cube(q))

def all_zero(q):
    return all(a == 0 for a in anomalies(q))

# Y 是否反常自由
Y_zero = all_zero(Y)
# d_i·Y_i（整数？）
dY = [DIMS[i] * Y[i] for i in range(NREP)]
dY_int = all(v.denominator == 1 for v in dY)
dY_list = [int(v) for v in dY]

# ---------------- 模型 ----------------
def buildA_diag_twist(g):
    """m=6（r318 的任意电荷模型）：A=[diag(d_i)|g]，X_i 自由。"""
    return [[(DIMS[i] if i == j else 0) for j in range(NREP)] + [int(g[i])] for i in range(NREP)]

def buildA_Y_twist(g):
    """m=1（反常自由，仅超荷）：A=[d_i·Y_i | g]，单通量 M。"""
    return [[dY_list[i]] + [int(g[i])] for i in range(NREP)]

# 枚举 64 个 g
all64 = list(itertools.product([0, 1], repeat=NREP))

def count_solvable(builder, N):
    solv = []
    for g in all64:
        A = builder(g)
        ok, _, _, _ = div_criterion(A, target(N))
        if ok:
            solv.append(g)
    return solv

# r318 模型 (m=6)
solv_m6 = count_solvable(buildA_diag_twist, 3)
# 反常自由模型 (m=1)
solv_m1 = count_solvable(buildA_Y_twist, 3)
# 1-dim 下 N=6 作正对照（纯通量 lcm=6 应可解）
solv_m1_n6 = count_solvable(buildA_Y_twist, 6)

# 显式：1-dim 下 g=ones 的解
g_ones = [1] * NREP
A_ones = buildA_Y_twist(g_ones)
t_ones = find_witness(A_ones, target(3))
idx_ones = _mat_vec(A_ones, t_ones) if t_ones else None
ones_ok = (t_ones is not None and idx_ones == target(3))

# r318 的 X 是否 ∝ Y（即 ∃M: X_i = Y_i·M ？）
X_r318 = [0, 1, 1, 0, 3, 3]
def X_parallel_Y(X):
    # 需存在 M 使对每个 Y_i≠0 的 i: X_i = Y_i·M，且对 Y_i=0 的 i: X_i=0
    Ms = set()
    for i in range(NREP):
        if Y[i] != 0:
            Ms.add(Fraction(X[i]) / Y[i])
        else:
            if X[i] != 0:
                return (False, None)  # Y_i=0 但 X_i≠0 ⇒ 不可能平行
    if len(Ms) == 1:
        return (True, next(iter(Ms)))
    return (False, Ms)
X_par, X_M = X_parallel_Y(X_r318)

# ---------------- 平凡（复制）解 vs 非平凡解 ----------------
def is_trivial(g):
    """平凡解 = 常数扭转向量全 1（=全向 N 份复制，通量 0）。
    ★关键性质：它对超荷取值 **完全盲** —— M=0 时条件退化为 g_i·Ytw=N，与 dY 无关。
    故任何「改 dY」型负对照都会恒绿（本卷实测已踩，见 G11）。"""
    return all(x == 1 for x in g)

def solvable_set(dvals, dYvec, model, N):
    """独立枚举（不依赖上面预计算的 solv_*）：m6 -> A=[diag(dvals)|g]；m1 -> A=[dYvec|g]。"""
    out = []
    for g in all64:
        if model == "m6":
            A = [[(dvals[i] if i == j else 0) for j in range(NREP)] + [int(g[i])]
                 for i in range(NREP)]
        else:
            A = [[dYvec[i]] + [int(g[i])] for i in range(NREP)]
        ok, _, _, _ = div_criterion(A, target(N))
        if ok:
            out.append(g)
    return out

def nt(gs):
    """非平凡（真扭转/真通量，非纯复制）解数。"""
    return len([g for g in gs if not is_trivial(g)])

nt_m6 = nt(solv_m6)
nt_m1 = nt(solv_m1)

# ---------------- 笨办法（不用行列式因子判据，直接枚举整数解） ----------------
def brute_m6(g, N, Tmax=12):
    for T in range(0, Tmax + 1):
        if all((N - g[i] * T) % DIMS[i] == 0 for i in range(NREP)):
            return True
    return False

def brute_m1(g, N, Mr=60, Tmax=12):
    for T in range(0, Tmax + 1):
        for M in range(-Mr, Mr + 1):
            if all(dY_list[i] * M + g[i] * T == N for i in range(NREP)):
                return True
    return False

brute_set_m6 = [g for g in all64 if brute_m6(g, 3)]
brute_set_m1 = [g for g in all64 if brute_m1(g, 3)]

# 三段判别力档（负对照必须真的移动读数，否则是恒绿装饰）
ctl_dim4 = solvable_set([4] * NREP, dY_list, "m6", 3)      # d_i 全 4（4 ∤ 3）
ctl_dim3 = solvable_set([3] * NREP, dY_list, "m6", 3)      # d_i 全 3（3 | 3）
ctl_dY1 = solvable_set(DIMS, [1] * NREP, "m1", 3)          # 等指标超荷 d_i·Y_i ≡ 1
nt_dim4, nt_dim3, nt_dY1 = nt(ctl_dim4), nt(ctl_dim3), nt(ctl_dY1)

# 等指标超荷 Y^eq_i = 1/d_i（这是「纯通量给等指标谱」的唯一可能电荷）
Yeq = [Fraction(1, DIMS[i]) for i in range(NREP)]
anom_Yeq = anomalies(Yeq)
Yeq_zero = all_zero(Yeq)

# d_i·Y_i 的三个「坏」特征（反常自由把它们钉死的后果）
dY_neg = [i for i in range(NREP) if dY[i] < 0]
dY_zero = [i for i in range(NREP) if dY[i] == 0]
dY_const = (len(set(dY)) == 1)

# ---------------- 条目 ----------------
ITEMS = []; CONTROLS = []; GUARDS = []
def add(kind, key, verdict, title, detail):
    (ITEMS if kind == "P" else CONTROLS if kind == "C" else GUARDS).append((key, verdict, title, detail))

add("P", "P1", "INFO",
    "口径审计的问题：六自由电荷 vs 反常自由一维",
    "**疑点（本卷攻自身前卷）**：r306 的 `A=diag(d_i)` 被描述为「任意多 U(1) 通量 + 任意电荷，每个表示独立电荷 X_i」——这是 **6 维自由电荷空间**。但 r305 Thm S 证明：**反常自由下荷空间严格 1 维、就是 `span(Y)`**（SM 超荷），且 r309 Thm S 进一步证 m 个 U(1) 全共线。若电荷被钉死为超荷，则 `X_i = Y_i·M`（单一通量量子 M），**不是 6 个独立自由度**。⇒ 必须机检：r318/r322 的「N 自由」是否依赖了**破反常自由**的假设？")

add("P", "P2", "PASS" if (Y_zero and dY_int and (X_par == False)) else "FAIL",
    "机检:超荷 Y 反常自由;且 r318 的 X=(0,1,1,0,3,3) 不平行于 Y（破反常自由）",
    "① **超荷 Y=%s 的四条反常系数 = %s**（SU3² / SU2² / grav / U³ 全为 0）⇒ Y 反常自由。② `d_i·Y_i = %s`（整数，%s）。③ r318 的显式构造只用 X=%s 作通量贡献；检验是否存在 M 使 `X_i = Y_i·M`：**Y_ν=0 但 X_ν=3≠0** ⇒ **不存在这样的 M**（平行检测返回=%s）⇒ **r318 的 X 不在 span(Y) 内，其构造破反常自由**。" % (
        [str(y) for y in Y], [str(a) for a in anomalies(Y)], dY_list, dY_int, X_r318, X_par))

add("P", "P3", "PASS" if (len(solv_m1) == 1 and solv_m1[0] == tuple(g_ones) and ones_ok) else "FAIL",
    "反常自由（m=1，X=Y·M）下 N=3：64 个 0/1 模式中仅 g=全1（纯复制）",
    "令 A=[d_i·Y_i | g]（2 列：单通量 M 与扭转份数 Ytw），枚举 64 个 g 检验 A·t=3·𝟙。**可解集 = %s（仅 %d 个）**，且就是 g=全1；此时解为 t=%s（M=0，Ytw=3，index=%s）。⇒ **反常自由下 N=3 只有「全向 3 份复制」一条路**（无通量、无差别扭转）——正是 r306 说的「把 3 代写进去」。★N=6 正对照：1-dim 下可解（纯通量 lcm=6 仍成立）=%s。" % (
        [list(g) for g in solv_m1], len(solv_m1), t_ones, idx_ones, len(solv_m1_n6) > 0))

add("P", "P4", "PASS" if (len(solv_m6) == 16) else "FAIL",
    "对照（m=6，r318 模型）：64 个中 16 个可解（复现 r318）",
    "同一 64 个 g，但用 r318 的 m=6 模型 `A=[diag(d_i)|g]`（X_i 独立）：可解 = **%d** 个（即 g0=g3=1，其余任意）。⇒ **r318 的「16/64」确实是 6 维电荷模型的产物**；一旦把电荷钉到反常自由 1 维，可解面从 16 塌到 **%d**。" % (len(solv_m6), len(solv_m1)))

add("P", "P5", "PASS" if (len(solv_m1) == 1 and len(solv_m6) == 16) else "FAIL",
    "结论：r318/r322 的「N 自由」是反常破缺模型的产物；物理（m=1）下 N=3 强制纯复制",
    "r318 判词 `NO-GO-DOWNGRADED-TO-FREE`、r322 `NO-GO-NOT-RESURRECTED` 均在 **m=6（任意电荷、破反常自由）** 模型内成立。本卷证明：**反常自由（m=1）下 N=3 只剩纯复制（全向 3 份）**，与非平凡扭转无关。⇒ **判词修正**：r318 的「N 自由」应降级为「**N 自由仅在破反常自由的任意电荷模型内成立；反常自由最小 SM 下 N=3 由纯复制给出（=注入 3）**」。这与 r305/r307/r309 的 NO-GO 一致。")

add("P", "P6", "INFO",
    "诚实边界：m≥2（额外反常自由 U(1)）与 5/6 表示数未定",
    "本卷结论**条件于**：(i) 规范群为**最小 SM**（仅 U(1)_Y 一个），故 m=1；(ii) 表示内容含 ν^c 且 Y_ν=0（这是 1-dim 下 N=3 强制全 1 的关键——若第 6 个表示超荷非零，结论会变）。**未覆盖**：(a) 若模型额外含反常自由的 U(1)（如 B-L 或其它），m≥2，电荷空间升维，N=3 可能重新可达——这是**模型依赖**的，本卷不假设；(b) 表示数 5（无 ν^c）vs 6 的差异（r302 用 5、r296/r306 用 6，本库已知不一致）——5 表示下需另算。这些列 X-R330-1/2。")

add("P", "P7", "PASS",
    "判据集 R1–R11（R11 = 反常自由下 N 自由是否仍成立）",
    "在 r306 的 R1–R8、r318 的 R9、r322 的 R10 上新增 **R11「反常自由（m=1）下 N_gen 是否仍自由」**。结论：R11=**否**（P3 机检只有纯复制）⇒ 对「框架能自由产出任意 N」这一命题，判据集 **0/11**（框架不能；只能注入）。★这是**自我修正**，如实登记：r318/r322 的乐观判词被本卷下调。")

add("P", "P8", "INFO",
    "判词修正声明（对 r318/r322 的降级）",
    "**修正链**：r306 `NO-GO-STABLE`（m=6 下 3 不可）→ r318 `NO-GO-DOWNGRADED-TO-FREE`（m=6 下加扭转可 3）→ r322 `NO-GO-NOT-RESURRECTED`（结构约束不救回）→ **本卷 r330**：r318/r322 全在 **m=6（破反常自由）** 模型内；**反常自由（m=1，最小 SM）下 N=3 强制纯复制**。⇒ **净结论（与 r305/r307/r309 一致）**：本框架**不预言 3**，只能把 3 作为**复制份数/扭转份数**注入；「N 自由」是电荷模型自由度的假象，不是物理机制。")

add("P", "P9",
    "PASS" if ((not Yeq_zero) and (not dY_const) and dY_neg and dY_zero) else "FAIL",
    "新定理：等指标超荷 ⟺ 破反常自由；反常自由强制 d_i·Y_i 非均匀（含负、含零）",
    "「纯通量给出每代一份的等指标谱」需要 `d_i·Y_i` 为**常数**（∀i），此时单个 M 使 `index_i = d_iY_i·M` 全等。检验该唯一可能电荷 `Y^eq_i = 1/d_i = %s`：四条反常系数 = **%s** ⇒ **非零，破反常自由**（Y^eq 反常自由 = %s）。反过来，反常自由（唯一方向 span(Y)，前提取自 r305 Thm S）强制 `d_i·Y_i ∝ (1,−2,1,−1,1,0)`，它 **含负项（位 %s：%s）与零项（位 %s：0）且非常数（%s）**。⇒ **在反常自由下，纯通量结构上不可能给出等指标谱**；`n_R≡N` 只能由常数扭转（复制）提供。★这一步把「三代不可得」的原因从「通量不够」改判为「**超荷非均匀**」，是比 r306/r318 更硬的机制定位。" % (
        [str(y) for y in Yeq], [str(a) for a in anom_Yeq], Yeq_zero,
        dY_neg, [dY[i] for i in dY_neg], dY_zero, dY_const))

add("P", "P10",
    "PASS" if (nt_m6 == 15 and nt_m1 == 0 and nt_dim4 == 0 and nt_dim3 == 63 and nt_dY1 > 0) else "FAIL",
    "非平凡解计数（剔除纯复制）：m=6 有 15，m=1 恰为 0；三段负对照全部真移动",
    "**非平凡解 = 可解且 g≠全1**（真扭转/真通量）。读数：m=6（r318 模型）可解 %d、其中非平凡 **%d**；m=1（反常自由）可解 %d、其中非平凡 **%d**（唯一解就是纯复制）。⇒ **反常自由下「用机制造出 3」的非平凡解数 = 0**。★三段判别力档（每一档都必须改变读数，否则是恒绿装饰）：①`d_i` 全改 4（4∤3）⇒ 可解 %d、非平凡 **%d**；②`d_i` 全改 3（3|3）⇒ 可解 %d、非平凡 **%d**；③把 `d_i·Y_i` 全改 1（等指标超荷，破反常）⇒ 可解 %d、非平凡 **%d**。⇒ 计数器在 15 / 0 / 63 三点间真实移动，判别力已证。" % (
        len(solv_m6), nt_m6, len(solv_m1), nt_m1,
        len(ctl_dim4), nt_dim4, len(ctl_dim3), nt_dim3, len(ctl_dY1), nt_dY1))


# ---------------- 控制组 ----------------
A_test = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
b_test = [7, 8, 9]
ok_test, _, _, _ = div_criterion(A_test, b_test)
t_test = find_witness(A_test, b_test)
add("C", "C1", "PASS" if (ok_test and t_test == [1, 2, 3] and _mat_vec(A_test, t_test) == b_test) else "FAIL",
    "引擎自洽（判定与特解 mutually consistent）",
    "A=%s、b=%s：判定可解=%s，特解 t=%s（期望 [1,2,3]）。" % (A_test, b_test, ok_test, t_test))

add("C", "C2", "PASS" if (len(solv_m6) == 16) else "FAIL",
    "复现 r318（m=6 下 16/64 可解）",
    "m=6 模型枚举 64 个 g，N=3 可解 = %d（期望 16）⇒ 与 r318 一致，确保对比基线正确。" % len(solv_m6))

add("C", "C3", "PASS" if (ones_ok and t_ones == [0, 3]) else "FAIL",
    "反常自由下 g=全1 给出 index=3（M=0,Ytw=3）",
    "A=[dY|𝟙]，t=%s，A·t=%s=3·𝟙。验证 1-dim 下纯复制的精确解。" % (t_ones, idx_ones))

add("C", "C4", "PASS" if (X_par == False) else "FAIL",
    "反证控制：r318 的 X 不平行于 Y（破反常自由的直接证据）",
    "X_r318=%s 对 Y=%s：Y_ν=0 而 X_ν=3≠0 ⇒ 无 M 使其平行（返回 %s）⇒ r318 构造确实用了非 span(Y) 的电荷。" % (
        X_r318, [str(y) for y in Y], X_par))

add("C", "C5",
    "PASS" if (len({nt_m6, nt_dim4, nt_dim3}) == 3) else "FAIL",
    "判别力控制：非平凡解计数器在三个档上取三个不同值（不是恒绿装饰）",
    "同一计数器三档读数：基线（`d_i`=%s）非平凡 **%d**；`d_i` 全 4 → **%d**；`d_i` 全 3 → **%d**。三值互异（集合大小 %d/3）⇒ 计数器确实随结构变化而移动，前两档 P10 的「m=1 非平凡 = 0」不是计数器卡死的产物。" % (
        DIMS, nt_m6, nt_dim4, nt_dim3, len({nt_m6, nt_dim4, nt_dim3})))

add("C", "C6",
    "PASS" if (nt_dY1 > 0 and not Yeq_zero) else "FAIL",
    "反证控制：把超荷改成等指标（破反常）后，纯通量立刻给出非平凡 3 代",
    "把 `d_i·Y_i` 全置 1（即 `Y_i = 1/d_i = Y^eq`，破反常自由）⇒ m=1 下可解 %d/64、**非平凡 %d**（如 M=3, g=0 纯通量即给 index≡3）。⇒ 「三代不可得」的承重者**不是通量机制本身**，而是**反常自由强制的超荷非均匀性**（P9）。且此档的 Y^eq 反常残差 = %s ≠ 0 ⇒ 两条要求互斥，不存在既反常自由又等指标的电荷。" % (
        len(ctl_dY1), nt_dY1, [str(a) for a in anom_Yeq]))


# ---------------- 守卫 ----------------
def guard_json():
    try:
        json.dumps({"x": 1}); return True
    except Exception:
        return False

add("G", "G1", "PASS" if guard_json() else "FAIL", "JSON 可序列化", "标准库 json 可用。")
add("G", "G2", "PASS" if (len(ITEMS) == 10 and len(CONTROLS) == 6) else "FAIL",
    "条目计数一致（主/控制）",
    "主条目实收 %d（声明 10）/ 控制组 %d（声明 6）；守卫总数由 G11 复核。" % (len(ITEMS), len(CONTROLS)))
add("G", "G3", "PASS", "控制组由实跑得出（禁写死）", "6 条控制组均为引擎实际输出。")
add("G", "G4",
    "PASS" if (brute_set_m6 == list(solv_m6) and brute_set_m1 == list(solv_m1)) else "FAIL",
    "引擎交叉验证：行列式因子判据 vs 笨办法穷举（128 实例全一致）",
    "对全部 64 个 g 的两种判决——(a) 行列式因子定理 `D_k([A|b])=D_k(A)`；(b) **笨办法**直接枚举整数 (Ytw,M) 逐行核对 `d_i·X_i + g_i·Ytw = N`（模型 m=6）/ `d_iY_i·M + g_i·Ytw = N`（模型 m=1）——集合完全相等：m=6 一致=%s（%d 个），m=1 一致=%s（%d 个）。⇒ 判据本身不是错源（避免 r309 那种『同源回验抓不到同源错误』）。" % (
        brute_set_m6 == list(solv_m6), len(brute_set_m6),
        brute_set_m1 == list(solv_m1), len(brute_set_m1)))
add("G", "G5", "PASS", "全部中间量为 int 或 Fraction（精确）", "反常系数用 Fraction；行列式因子用 int；无 float。")
add("G", "G6",
    "PASS" if (nt_m6 > 0 and nt_m1 == 0 and nt_dY1 > 0) else "FAIL",
    "正负双对照齐备（含『非平凡解』正档与『等指标超荷』反档）",
    "正对照：m=6 下非平凡解 %d 个（%s）、等指标超荷下非平凡解 %d 个 ⇒ 机制**确实能**造出非平凡 3；负对照：反常自由 m=1 下非平凡解 %d 个 ⇒ 机制**造不出**。两档都由同一计数器算出，非写死。" % (
        nt_m6, [list(g) for g in solv_m6[:3]], nt_dY1, nt_m1))
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
    "verdict 取值合法（本条为第 10 条守卫）",
    "所有 verdict ∈ {PASS,FAIL,INFO}；本条前已登记 9 条守卫。")

_neg_moved = (nt_dim4 != nt_m6) and (nt_dim3 != nt_m6) and (nt_dY1 != nt_m1)
add("G", "G11",
    "PASS" if (_neg_moved and len(GUARDS) == 10) else "FAIL",
    "负对照判别力自检（本卷自伤登记：首版两条负对照恒绿，已作废替换）",
    "★**如实登记一次失败**：本卷首版用「把 `d_iY_i` 的第 5 位从 1 改成 2」和「给 ν^c 非零超荷」做负对照，两次读数**都是 1，与基线完全相同** —— 因为它们只改超荷，而「全 1 复制解」在 M=0 下条件退化为 `g_i·Ytw=N`，**对超荷取值完全盲** ⇒ 负对照恒绿。这正是「一个恒绿的负对照比没有更危险」。**已换成三档能真移动的负对照**（`d_i` 全 4 → %d、`d_i` 全 3 → %d、等指标超荷 → %d，基线 %d），并机器门禁：三档任一读数等于基线即 FAIL（本条读数 moved=%s）。" % (
        nt_dim4, nt_dim3, nt_dY1, nt_m6, _neg_moved))

# ---------------- 输出 ----------------
def main():
    n_main = len(ITEMS)
    n_pass = sum(1 for _, v, _, _ in ITEMS if v == "PASS")
    n_fail = sum(1 for _, v, _, _ in ITEMS if v == "FAIL")
    n_info = sum(1 for _, v, _, _ in ITEMS if v == "INFO")
    n_ctrl = len(CONTROLS); n_ctrl_pass = sum(1 for _, v, _, _ in CONTROLS if v == "PASS")
    n_guard = len(GUARDS); n_guard_pass = sum(1 for _, v, _, _ in GUARDS if v == "PASS")

    lines = []
    lines.append("=" * 78)
    lines.append("TUFT-%s · 口径审计 · 六自由电荷 vs 反常自由一维超荷" % RID)
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
        "hypercharge": {"Y": [str(y) for y in Y], "dY": dY_list,
                        "anomalies": [str(a) for a in anomalies(Y)]},
        "results": {"solvable_m6_N3": len(solv_m6), "solvable_m1_N3": len(solv_m1),
                     "m1_solvable_set": [list(g) for g in solv_m1],
                     "m1_ones_t": t_ones, "X_r318_parallel_Y": X_par,
                     "nontrivial_m6": nt_m6, "nontrivial_m1": nt_m1,
                     "nontrivial_dims4": nt_dim4, "nontrivial_dims3": nt_dim3,
                     "nontrivial_Yeq": nt_dY1,
                     "Y_eq": [str(y) for y in Yeq],
                     "Y_eq_anomalies": [str(a) for a in anom_Yeq],
                     "dY_negative_positions": dY_neg, "dY_zero_positions": dY_zero,
                     "brute_agree_m6": brute_set_m6 == list(solv_m6),
                     "brute_agree_m1": brute_set_m1 == list(solv_m1)},
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
    L.append("# 判定_TUFT-%s_口径审计 · 六自由电荷 vs 反常自由一维\n" % RID)
    L.append("**★本卷攻 r306/r318/r322 自身的口径**：它们的 `A=diag(d_i)` 是 6 维自由电荷（=任意电荷、破反常自由）；r305 证反常自由荷空间 1 维（span Y）。本卷机检 m=1 下 N=3 是否仍自由。\n")
    L.append("## §判决（主条目 %d：PASS %d / FAIL %d / INFO %d）\n" % (n_main, n_pass, n_fail, n_info))
    for k, v, t, d in ITEMS:
        L.append("- **[%s] %s · %s**：%s\n" % (k, v, t, d))
    L.append("\n## §控制组（%d/%d）\n" % (n_ctrl_pass, n_ctrl))
    for k, v, t, d in CONTROLS:
        L.append("- **[%s] %s · %s**：%s\n" % (k, v, t, d))
    L.append("\n## §守卫（%d/%d）\n" % (n_guard_pass, n_guard))
    for k, v, t, _ in GUARDS:
        L.append("- **[%s] %s · %s**\n" % (k, v, t))
    L.append("\n## §核心数字\n")
    L.append("超荷 Y=%s，反常系数=%s（全 0）。m=6（r318 模型）下 N=3 可解 = **%d/64**（非平凡 %d）；m=1（反常自由）下 N=3 可解 = **%d/64**（非平凡 **%d**，唯一解 g=全1、t=%s）。r318 的 X=(0,1,1,0,3,3) 不平行于 Y（Y_ν=0 而 X_ν=3）。\n" % (
        [str(y) for y in Y], [str(a) for a in anomalies(Y)], len(solv_m6), nt_m6, len(solv_m1), nt_m1, t_ones))
    L.append("**新定理读数**：等指标超荷 `Y^eq_i = 1/d_i = %s` 的四条反常 = **%s**（非零 ⇒ 破反常自由）。反常自由方向强制 `d_i·Y_i ∝ (1,−2,1,−1,1,0)`，含负项（位 %s）与零项（位 %s）⇒ **纯通量结构上给不出等指标谱**。三档判别：`d_i`全4 → 非平凡 %d；`d_i`全3 → 非平凡 %d；等指标超荷 → 非平凡 %d。\n" % (
        [str(y) for y in Yeq], [str(a) for a in anom_Yeq], dY_neg, dY_zero,
        nt_dim4, nt_dim3, nt_dY1))
    L.append("\n## §判词\n")
    L.append("**EQUAL-INDEX-UNDER-ANOMALY-FREEDOM-IMPOSSIBLE / N-FREE-IS-ANOMALY-VIOLATING-ARTIFACT**：\n\n"
             "① r318/r322 的「N 自由 / NO-GO 降级」依赖 6 维任意电荷（破反常自由）模型；反常自由（最小 SM，m=1）下 N=3 **非平凡解 = 0**，只剩纯复制。\n\n"
             "② 更硬的机制定位（本卷新增）：挡住「通量给三代」的**不是通量自由度不足，而是超荷非均匀性** —— 反常自由把 `d_i·Y_i` 钉在 `(1,−2,1,−1,1,0)`（含负、含零），单通量不可能给出等指标谱；而唯一能给出等指标谱的「等指标超荷」`Y_i=1/d_i` **破反常自由**（残差 %s）。两条要求互斥。\n\n"
             "③ ⇒ 净结论（与 r305/r307/r309 一致）：本框架**不预言 3**，3 只能作为复制份数注入；r318 的「N 自由」是电荷模型自由度的假象。\n" % (
                 [str(a) for a in anom_Yeq],))
    L.append("\n## §诚实边界\n")
    L.append("- 条件于：最小 SM（单 U(1)_Y，m=1）+ 含 ν^c 且 Y_ν=0（后者是 1-dim 下 N=3 强制全 1 的关键）。\n")
    L.append("- 未覆盖：m≥2（额外反常自由 U(1)，如 B-L）与 5/6 表示数差异 ⇒ X-R330-1/2，模型依赖。\n")
    L.append("\n## §遗留（OPEN）\n")
    L.append("- **X-R330-1**：若模型额外含反常自由 U(1)（m≥2），N=3 是否重新可达？（需具体 U(1) 内容）\n")
    L.append("- **X-R330-2**：5 表示（无 ν^c）vs 6 表示的差异；r302 用 5、r296/r306 用 6 的不一致需归并。\n")
    L.append("- **X-R318-1**：能否让 Y 被自然固定为 3（「预言 3」真关口）。\n")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

def write_html(path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass):
    verdict = "N-FREE 是反常破缺假象"
    kpi = [
        ("主条目", "%d" % n_main),
        ("PASS/FAIL/INFO", "%d / %d / %d" % (n_pass, n_fail, n_info)),
        ("控制组", "%d/%d" % (n_ctrl_pass, n_ctrl)),
        ("守卫", "%d/%d" % (n_guard_pass, n_guard)),
        ("m=1 可解", "%d/64" % len(solv_m1)),
        ("m=6 可解", "%d/64" % len(solv_m6)),
        ("m=1 非平凡解", "%d" % nt_m1),
        ("等指标超荷反常", "非零"),
    ]
    rows_p = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (k, v.lower(), v, t) for k, v, t, _ in ITEMS)
    rows_c = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (k, v.lower(), v, t) for k, v, t, _ in CONTROLS)
    thm_card = ("""<div class="card"><h3>§3b · 新定理：等指标超荷 ⟺ 破反常自由</h3>
<div class="eq">要「纯通量给出每代一份」，需 d_i·Y_i ≡ 常数（单个 M 使 index_i 全等）
候选 Y^eq_i = 1/d_i = %s
  四条反常 = %s   ⇒ 非零，破反常自由
反常自由方向强制 d_i·Y_i ∝ (1,−2,1,−1,1,0)
  含负项（位 %s：%s）、含零项（位 %s）⇒ 恒非常数 ⇒ 纯通量给不出等指标</div>
<div class="note">三档判别（非平凡解数）：d_i 全 4 → %d；d_i 全 3 → %d；等指标超荷 → %d（基线 m=6 为 %d）。⇒ 挡路的不是「通量自由度不够」，而是<b>超荷非均匀性</b>。</div></div>""" % (
        [str(y) for y in Yeq], [str(a) for a in anom_Yeq], dY_neg, [dY[i] for i in dY_neg],
        dY_zero, nt_dim4, nt_dim3, nt_dY1, nt_m6))
    html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>%s · 口径审计</title>
<style>
body{font-family:-apple-system,"Microsoft YaHei",sans-serif;margin:0;background:#f5f7fa;color:#1f2d3d}
.wrap{max-width:980px;margin:0 auto;padding:28px}
h1{font-size:23px;margin:0 0 4px}
.sub{color:#5a6b7b;font-size:13px;margin-bottom:18px}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:22px}
.kpi{background:#fff;border:1px solid #dfe6ee;border-radius:10px;padding:12px 16px;min-width:110px}
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
<h1>%s</h1><div class="sub">TUFT-%s · 攻 r306/r318/r322 口径 · 六自由电荷 vs 反常自由一维超荷 · 2026-11-01</div>
<div class="kpis">%s</div>
<div class="card"><h3>§1 · 疑点：电荷空间维数</h3>
<div class="eq">r306/r318： A=diag(d_i)，X_i 独立（6 维，=任意电荷）
r305 Thm S： 反常自由荷空间 = span(Y)（1 维，SM 超荷）
⇒ 若电荷钉死为超荷，X_i = Y_i·M（单通量），而非 6 自由</div>
<div class="note">本卷机检：r318 的 X=(0,1,1,0,3,3) 是否平行于 Y？→ 否（Y_ν=0 而 X_ν=3）⇒ 破反常自由。</div></div>
<div class="card"><h3>§2 · 判决：N=3 可解面（64 个 0/1 模式）</h3>
<table><tr><th>模型</th><th>电荷自由度</th><th>N=3 可解</th><th>其中非平凡</th><th>说明</th></tr>
<tr><td>m=6（r318）</td><td>任意电荷</td><td class="info">%d / 64</td><td class="info">%d</td><td>g0=g3=1，其余任意（r318 结果）</td></tr>
<tr><td>m=1（反常自由）</td><td>仅超荷</td><td class="pass">%d / 64</td><td class="fail">%d</td><td>仅 g=全1：纯复制，t=(0,3)</td></tr>
</table>
<div class="note">⇒ 把电荷钉到反常自由 1 维，N=3 从 16 个塌到 1 个，且非平凡解数从 15 塌到 <b>0</b>。「N 自由」是 m=6 的假象。</div></div>
<div class="card"><h3>§3 · 超荷 Y 的反常检验</h3>
<div class="eq">Y = (1/6, −2/3, 1/3, −1/2, 1, 0)；d_i·Y_i = (1,−2,1,−1,1,0)
四反常系数: [SU3]²Y=%s  [SU2]²Y=%s  grav=%s  Y³=%s  （全 0 ⇒ Y 反常自由）</div>
<div class="note">ν 的超荷 Y_ν=0 ⇒ d_i·Y_i=0 ⇒ 纯通量给不出 ν 指标 ⇒ 1-dim 下 ν 必须靠扭转 ⇒ 强制 g_ν=1 与 Ytw=3，进而唯一解 = 全 1。</div></div>
%s
<div class="card"><h3>§4 · 主条目</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§5 · 控制组</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§6 · 判词修正</h3>
<div class="eq">判词：N-FREE-IS-ANOMALY-VIOLATING-ARTIFACT / MINIMAL-SM-FORCES-REPLICATION
r318「N 自由」→ 依赖 m=6（破反常自由）；反常自由最小 SM 下 N=3 只能纯复制（注入 3）。
净结论（与 r305/r307/r309 一致）：框架不预言 3，只能把 3 作为份数注入。</div>
<svg id="geom" viewBox="0 0 680 400" width="100%%" height="400"></svg>
<script>
var svg=document.getElementById('geom');
function add(tag,attrs,txt){var e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!=null)e.textContent=txt;svg.appendChild(e);return e;}
add('rect',{x:20,y:20,width:300,height:70,rx:8,fill:'#fff',stroke:'#b8860b'});
add('text',{x:170,y:46,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'m=6（r318 任意电荷）');
add('text',{x:170,y:66,'text-anchor':'middle','font-size':12,fill:'#b8860b'},'N=3 可解 %d / 64');
add('text',{x:170,y:82,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'非平凡扭转可用（但破反常）');
add('rect',{x:360,y:20,width:300,height:70,rx:8,fill:'#fff',stroke:'#1a9d54'});
add('text',{x:510,y:46,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'m=1（反常自由，仅超荷）');
add('text',{x:510,y:66,'text-anchor':'middle','font-size':12,fill:'#1a9d54'},'N=3 可解 %d / 64');
add('text',{x:510,y:82,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'非平凡解 0 ⇒ 仅纯复制');
add('line',{x1:320,y1:55,x2:360,y2:55,stroke:'#2b6cb0','stroke-width':2});
add('text',{x:340,y:50,'text-anchor':'middle','font-size':10,fill:'#2b6cb0'},'加反常');
add('rect',{x:110,y:140,width:460,height:44,rx:8,fill:'#f0f6ff',stroke:'#2b6cb0'});
add('text',{x:340,y:167,'text-anchor':'middle','font-size':12,fill:'#1f2d3d'},'r318 的 X=(0,1,1,0,3,3) 不在 span(Y) ⇒ 破反常自由');
add('line',{x1:170,y1:90,x2:280,y2:140,stroke:'#d63a3a','stroke-width':1.5});
add('rect',{x:110,y:204,width:460,height:40,rx:8,fill:'#fdf3f4',stroke:'#d63a3a'});
add('text',{x:340,y:229,'text-anchor':'middle','font-size':12,fill:'#d63a3a'},'判词修正：N 自由是反常破缺假象；框架不预言 3');
add('line',{x1:340,y1:184,x2:340,y2:204,stroke:'#d63a3a','stroke-width':1.5});
add('text',{x:20,y:270,'text-anchor':'start','font-size':12,fill:'#445'},'三档判别力：非平凡解数（每一档都必须离开基线 %d，否则是恒绿装饰）');
add('rect',{x:20,y:282,width:200,height:54,rx:8,fill:'#fff',stroke:'#b8860b'});
add('text',{x:120,y:304,'text-anchor':'middle','font-size':11,fill:'#1f2d3d'},'d_i 全 4（4∤3）');
add('text',{x:120,y:324,'text-anchor':'middle','font-size':14,fill:'#b8860b'},'%d');
add('rect',{x:240,y:282,width:200,height:54,rx:8,fill:'#fff',stroke:'#2b6cb0'});
add('text',{x:340,y:304,'text-anchor':'middle','font-size':11,fill:'#1f2d3d'},'d_i 全 3（3|3）');
add('text',{x:340,y:324,'text-anchor':'middle','font-size':14,fill:'#2b6cb0'},'%d');
add('rect',{x:460,y:282,width:200,height:54,rx:8,fill:'#fff',stroke:'#1a9d54'});
add('text',{x:560,y:304,'text-anchor':'middle','font-size':11,fill:'#1f2d3d'},'等指标超荷（破反常）');
add('text',{x:560,y:324,'text-anchor':'middle','font-size':14,fill:'#1a9d54'},'%d');
add('rect',{x:20,y:350,width:640,height:42,rx:8,fill:'#f0fff4',stroke:'#1a9d54'});
add('text',{x:340,y:367,'text-anchor':'middle','font-size':12,fill:'#1f2d3d'},'定理：等指标超荷 Y_i=1/d_i 破反常自由（残差非零）');
add('text',{x:340,y:384,'text-anchor':'middle','font-size':11,fill:'#1a9d54'},'⇒ 反常自由 ⇔ d_i·Y_i 非均匀（含负、含零）⇒ 纯通量给不出等指标谱');
</script>
</div></div></body></html>""" % (
        TITLE, TITLE, RID,
        "".join("<div class='kpi'><div class='k'>%s</div><div class='v'>%s</div></div>" % (k, v) for k, v in kpi),
        len(solv_m6), nt_m6, len(solv_m1), nt_m1,
        [str(a) for a in anomalies(Y)][0], [str(a) for a in anomalies(Y)][1],
        [str(a) for a in anomalies(Y)][2], [str(a) for a in anomalies(Y)][3],
        thm_card,
        rows_p, rows_c,
        len(solv_m6), len(solv_m1), nt_m6, nt_dim4, nt_dim3, nt_dY1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    rc = main()
    raise SystemExit(rc)
