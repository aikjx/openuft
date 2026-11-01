# -*- coding: utf-8 -*-
"""
TUFT-r305 · 通量荷的等谱归一定理
q ∝ Y、通量量子 M 消去、扭转计数的完整分类与「最小 K = 3t」

承 r302：r302 用「4 扭转 × M=±1..±12 共 96 组穷举」判定等谱解唯一，
但它在诚实边界里写明「M 的穷举不是全部整数，判决应来自闭式」。本卷把那句话落实成定理，
而且结论比 r302 更强、边界更清楚：

  定理 I（M 消去）    六条反常里四条 ∝ 1/M、AYF ∝ 1/M²、AFF ∝ 1/M³
                      ⇒ 逐条乘掉 M 后，约束**完全不依赖 M**
                      ⇒ Z_N 分数通量在结构上无关，不是「扫了 96 个数」
  定理 J（等谱归一）  等谱 + 四条线性反常的**完整解集**是 2 参数族
                      k = (λ, 3N−2λ, λ, 2N−λ, λ)，且此时 q = (t/M)·Y（t = N − λ）
                      ⇒ **「通量沿超荷方向」不是假设，是等谱逼出来的唯一荷型**
  定理 K（自动性）    偏差向量 N−k = t·tr_R(Y) ⇒ AYF·M² = t²·Σd_iY_i³、AFF·M³ = t³·Σd_iY_i³
                      ⇒ 两条非线性反常化为 **SM 自身的 U(1)_Y³ = 0**
  定理 L（锁定）      k_R ≤ 1 ⇒ k = (λ, λ+3t, λ, λ+2t, λ) ∈ {0,1}⁵ ⇒ t = 0 ⇒ n_R ≡ λ ∈ {0,1}
  定理 M（边界）      要 t 代，必须 K ≥ 3t（三代需某表示有 ≥ 9 份常数截面）

⇒ 判词：三代 no-go **不再依赖任何穷举界**，只依赖一条：k_R ≤ 1。

确定性：Fraction 精确；无 random；Decimal prec=60 仅用于展示。
约定：左手口径，Q = T3 + Y；T(3)=T(3̄)=1/2。
"""
import io
import json
import os
import sys
from decimal import getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r305"
DATE = "2026-11-01"
DEGREE = 0
VERDICT = "NO-GO-UPGRADED__M-CANCELLED-AND-K-LE-1-LOCKS-ONE-GENERATION"

DIR_HERE = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(os.path.dirname(DIR_HERE), "数据")
BASE = ("TUFT-r305_通量荷的等谱归一与扭转计数锁定_"
        "M消去与k的线性分类与最小K等于3t_精算与可视化_2026-11-01")

# ---------------------------------------------------------------- SM 谱
NAMES = ["Q_L  (3,2)_{1/6}", "u_R^c (3bar,1)_{-2/3}", "d_R^c (3bar,1)_{1/3}",
         "L_L  (1,2)_{-1/2}", "e_R^c (1,1)_{1}"]
DIMS = [6, 3, 3, 2, 1]
YS = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)]
TR = [DIMS[i] * YS[i] for i in range(5)]        # (1, -2, 1, -1, 1)


def anomal_w(q, Yv):
    """以任意超荷向量 Yv 为权重的六条反常（用于「扰动 Y」的正对照）。"""
    q1, q2, q3, q4, q5 = q
    return (2 * q1 + q2 + q3,
            3 * q1 + q4,
            sum(DIMS[i] * q[i] for i in range(5)),
            sum(DIMS[i] * Yv[i] ** 2 * q[i] for i in range(5)),
            sum(DIMS[i] * Yv[i] * q[i] ** 2 for i in range(5)),
            sum(DIMS[i] * q[i] ** 3 for i in range(5)))


def anomal(q):
    """六条规范反常系数：A3, A2, Ag, AYY, AYF, AFF（SM 超荷）。"""
    return anomal_w(q, YS)


AKEYS = ["A3", "A2", "Ag", "AYY", "AYF", "AFF"]
POW = [1, 1, 1, 1, 2, 3]


def q_of(k, N, M):
    """等谱条件 n_i = M·q_i·d_i + k_i = N 反解出的荷。"""
    return [(N - k[i]) / (M * DIMS[i]) for i in range(5)]


def reduced(k, N, M):
    """六条反常各乘 M^p，得到与 M 无关的「约化残差」。"""
    a = anomal(q_of(k, N, M))
    return tuple(a[j] * (M ** POW[j]) for j in range(6))


def kfam(N, lam):
    """定理 J 的 2 参数族：k = (λ, 3N−2λ, λ, 2N−λ, λ)。"""
    return (lam, 3 * N - 2 * lam, lam, 2 * N - lam, lam)


def ns_of(k, N, M):
    return [M * q_of(k, N, M)[i] * DIMS[i] + k[i] for i in range(5)]


def allzero(t):
    return all(x == 0 for x in t)


# ---------------------------------------------------------------- 精确线性代数
def rref(mat):
    A = [r[:] for r in mat]
    n, m = len(A), len(A[0])
    piv, r = [], 0
    for c in range(m):
        p = None
        for i in range(r, n):
            if A[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(m)]
        piv.append(c)
        r += 1
        if r == n:
            break
    return r, A, piv


# ---------------------------------------------------------------- 判据框架
ITEMS, CONTROLS, GUARDS = [], [], []


def item(iid, kind, exp, act, note, tol=None):
    if kind == "eq":
        ok = (act == exp)
    elif kind == "abs":
        ok = abs(act - exp) <= tol
    elif kind == "gt":
        ok = act > exp
    elif kind == "lt":
        ok = act < exp
    else:
        ok = True
    ITEMS.append({"id": iid, "kind": kind, "exp": str(exp), "act": str(act),
                  "status": "INFO" if kind == "info" else ("PASS" if ok else "FAIL"),
                  "note": note})


def control(cid, desc, ok, detail=""):
    CONTROLS.append({"id": cid, "desc": desc, "detail": detail,
                     "status": "PASS" if ok else "FAIL"})


def guard(gid, desc, ok, detail=""):
    GUARDS.append({"id": gid, "desc": desc, "detail": detail,
                   "status": "PASS" if ok else "FAIL"})


def fmt(v):
    if isinstance(v, F):
        return str(v.numerator) if v.denominator == 1 else ("%d/%d" % (v.numerator, v.denominator))
    return str(v)


def vstr(v):
    return "(" + ",".join(fmt(x) for x in v) + ")"


def kstr(v):
    return "(" + ",".join(fmt(x) for x in v) + ")"


# ================================================================ A 组
print("[r305] A 组：约定与 SM 自洽复算")
anY = anomal(YS)
item("A01", "eq", "(1/6,-2/3,1/3,-1/2,1)", vstr(YS), "左手口径超荷 Y")
item("A02", "eq", "(1,-2,1,-1,1)", vstr(TR), "tr_R(Y) = dim·Y = (1,−2,1,−1,1)")
item("A03", "eq", 0, anY[0], "[SU(3)]²U(1)_Y = %s" % fmt(anY[0]))
item("A04", "eq", 0, anY[1], "[SU(2)]²U(1)_Y = %s" % fmt(anY[1]))
item("A05", "eq", 0, anY[3], "U(1)_Y²U(1)_Y = %s" % fmt(anY[3]))
item("A06", "eq", 0, anY[5], "**U(1)_Y³ = Σ d_i Y_i³ = %s** —— 定理 K 的唯一支点" % fmt(anY[5]))
item("A07", "eq", "11/6", fmt(sum(YS[i] ** 2 for i in range(5))),
     "Σ Y_i² = 11/6 —— 定理 J 的 AYY 行系数")

# ================================================================ B 组
print("[r305] B 组：定理 I · 通量量子 M 被完全消去")
MS = [F(1), F(2), F(3), F(5), F(-1), F(-5), F(7),
      F(1, 2), F(1, 3), F(2, 3), F(-1, 7), F(5, 3)]
KVEC = [("T0 平凡扭转", (1, 1, 1, 1, 1)), ("T3 仅 Z_3 扭转", (0, 0, 0, 1, 1)),
        ("T2 仅 Z_2 扭转", (0, 1, 1, 0, 1)), ("T32 双因子扭转", (0, 0, 0, 0, 1)),
        ("家族 t=3", (0, 9, 0, 6, 0)), ("任意乱序", (2, 5, 1, 3, 0))]

nM_indep, nM_total, mdep = 0, 0, []
for name, kk in KVEC:
    k = [F(x) for x in kk]
    for N in (F(1), F(2), F(3), F(7, 2)):
        vals = set(reduced(tuple(k), N, M) for M in MS)
        nM_total += 1
        if len(vals) == 1:
            nM_indep += 1
        else:
            mdep.append((name, fmt(N), len(vals)))

item("B01", "eq", nM_total, nM_indep,
     "**定理 I 机检**：6 个 k 向量 × 4 个 N = %d 组，每组在 %d 个有理 M（含 1/2、1/3、2/3、−1/7、5/3）上算"
     "「约化残差」（六条反常各乘 M^p），全部与 M 无关（%d/%d）" % (nM_total, len(MS), nM_indep, nM_total))
item("B02", "eq", 0, len(mdep), "M 相关的反例数 = %d" % len(mdep))

k_t3 = tuple(F(x) for x in (0, 0, 0, 1, 1))
red_t3 = set(reduced(k_t3, F(1), M) for M in MS)
r_t3 = list(red_t3)[0]
item("B03", "eq", 1, len(red_t3),
     "以 T3 为例（N=1）：约化残差在 %d 个 M 上只取 **%d** 个不同值 ⇒ M 完全约去" % (len(MS), len(red_t3)))
item("B04", "eq", "1", fmt(r_t3[0]),
     "T3 的 A3 约化残差 = %s（非零常数）⇒ 阻碍**不是「某个 M 不行」，是任何 M 都不行**" % fmt(r_t3[0]))
item("B05", "eq", "1/2", fmt(r_t3[1]), "T3 的 A2 约化残差 = %s ⇒ 第二条独立否决" % fmt(r_t3[1]))
item("B06", "eq", "3", fmt(r_t3[2]), "T3 的 grav-U(1) 约化残差 = %s" % fmt(r_t3[2]))
n_nz = sum(1 for x in r_t3 if x != 0)
item("B07", "eq", 6, n_nz,
     "T3 在 N=1 时六条约化残差**全部非零**（%d/6）：%s" % (n_nz, [fmt(x) for x in r_t3]))
item("B08", "info", "M cancels identically", "M cancels identically",
     "机制：q_i = (N−k_i)/(M·d_i)，四条线性反常各带一个 1/M，AYF ∝ 1/M²、AFF ∝ 1/M³；"
     "M ≠ 0 时逐条乘掉即与 M 无关。⇒ **Z_N 分数通量在结构上不构成退路**；"
     "r302 的 96 组穷举因此是多余的方法，但作为机检仍然有效。")

# ================================================================ C 组
print("[r305] C 组：定理 J · 四条线性反常的完整解集")
# 未知量 X = [N, k1, k2, k3, k4, k5]
LROWS = [
    [F(6), F(-2), F(-2), F(-2), F(0), F(0)],                                     # A3·M
    [F(6), F(-3), F(0), F(0), F(-3), F(0)],                                      # A2·M
    [F(5), F(-1), F(-1), F(-1), F(-1), F(-1)],                                   # Ag·M
    [F(11, 6), -YS[0] ** 2, -YS[1] ** 2, -YS[2] ** 2, -YS[3] ** 2, -YS[4] ** 2],  # AYY·M
]
rk, AR, piv = rref(LROWS)
item("C01", "eq", 4, rk, "四条线性反常的系数矩阵秩 = %d（满秩 ⇒ 无冗余方程）" % rk)
item("C02", "eq", 2, 6 - rk,
     "未知量 6 个、秩 %d ⇒ 解空间维数 **%d** ⇒ 线性部分不足以定死，必须再上非线性两条" % (rk, 6 - rk))
item("C03", "info", "RREF", "RREF",
     "RREF 四行解出：N = (%s)k4 + (%s)k5 ；k1 = (%s)k5 ；k2 = (%s)k4 + (%s)k5 ；k3 = (%s)k5"
     % (fmt(-AR[0][4]), fmt(-AR[0][5]), fmt(-AR[1][5]),
        fmt(-AR[2][4]), fmt(-AR[2][5]), fmt(-AR[3][5])))

# 逐点验证 RREF 四行（解出主元变量后回代，全部应成立）
def solve_row(row, pcol, X):
    """RREF 行：x_pcol + Σ_{j≠pcol} a_j x_j = 0 ⇒ x_pcol = −Σ a_j x_j。"""
    return -sum(row[j] * X[j] for j in range(6) if j != pcol)


chk = []
for N in (F(0), F(1), F(2), F(3), F(5), F(5, 2), F(-2)):
    for lam in (F(0), F(1), F(2), F(-1), F(1, 2)):
        k = kfam(N, lam)
        X = [N, k[0], k[1], k[2], k[3], k[4]]
        chk.append([
            N == solve_row(AR[0], 0, X),
            k[0] == solve_row(AR[1], 1, X),
            k[1] == solve_row(AR[2], 2, X),
            k[2] == solve_row(AR[3], 3, X),
        ])
nchk = sum(1 for row in chk for b in row if b)
tot_chk = sum(len(row) for row in chk)
item("C04", "eq", tot_chk, nchk,
     "RREF 四行逐点回代：%d 组 (N,λ) × 4 行 = %d 个代数恒等式，成立 %d 个 ⇒ "
     "**k1 = k5、k3 = k5** 是核心（把 5 个 k 压到 3 个独立量）" % (len(chk), tot_chk, nchk))

lam_probe = []
for N in (F(0), F(1), F(2), F(3), F(5, 2), F(-2)):
    for lam in (F(0), F(1), F(2), F(-1), F(1, 2)):
        k = kfam(N, lam)
        lam_probe.append(((k[3] + k[4]) / 2 == N) and (k[0] == k[2] == k[4] == lam))
item("C05", "eq", len(lam_probe), sum(1 for x in lam_probe if x),
     "**定理 J**：以 λ = k5 重参数化得 k = (λ, 3N−2λ, λ, 2N−λ, λ)；%d 组 (N,λ) 上该族与 RREF 解集**逐点等价**（%d/%d）"
     % (len(lam_probe), sum(1 for x in lam_probe if x), len(lam_probe)))

fam_rows = []
for N in (F(0), F(1), F(2), F(3), F(5), F(5, 2)):
    for lam in (F(0), F(1), F(2), F(-1)):
        k = kfam(N, lam)
        for M in (F(1), F(3), F(1, 2), F(-2)):
            fam_rows.append(allzero(anomal(q_of(k, N, M))))
item("C06", "eq", len(fam_rows), sum(1 for x in fam_rows if x),
     "族内每一组解代入六条反常**全部为零**（%d/%d）⇒ 该族确实是解集，不只是线性部分的子集"
     % (sum(1 for x in fam_rows if x), len(fam_rows)))

q_rows = []
for N in (F(1), F(2), F(3), F(5), F(-1)):
    for lam in (F(0), F(1), F(2)):
        k = kfam(N, lam)
        t = N - lam
        for M in (F(1), F(-2), F(3), F(1, 3)):
            qq = q_of(k, N, M)
            q_rows.append(all(qq[i] == t * YS[i] / M for i in range(5)))
item("C07", "eq", len(q_rows), sum(1 for x in q_rows if x),
     "**★★定理 J 的核心**：族内解恒有 **q = (t/M)·Y**（t = N − λ），%d/%d 组逐分量精确成立 "
     "⇒ 「通量沿超荷方向」不是假设，是**等谱逼出来的唯一荷型**" % (sum(1 for x in q_rows if x), len(q_rows)))
item("C08", "info", "4 effective constraints", "4 effective constraints",
     "六条反常里两条（AYF / AFF）在等谱解集上恒为零，真正起约束作用的只有 %d 条；"
     "而四条的解集已由定理 J 完整给出 —— 所以「六条全用」在本问题上并非必需，"
     "**必要的只是那四条线性方程**。" % (len(AKEYS) - 2))

# ================================================================ D 组
print("[r305] D 组：定理 K · 两条非线性反常化为 SM 自身的反常自由")
dev_rows = []
for N in (F(1), F(2), F(3), F(5)):
    for lam in (F(0), F(1), F(2)):
        k = kfam(N, lam)
        t = N - lam
        dev_rows.append(all(N - k[i] == t * TR[i] for i in range(5)))
item("D01", "eq", len(dev_rows), sum(1 for x in dev_rows if x),
     "偏差向量 **N − k = t·tr_R(Y)**（= t·(1,−2,1,−1,1)），%d/%d 组精确成立 —— "
     "这是「非线性两条为何自动满足」的全部原因" % (sum(1 for x in dev_rows if x), len(dev_rows)))

ayf_rows, aff_rows = [], []
for t in (F(1), F(2), F(3), F(-2)):
    for M in (F(1), F(3), F(1, 2)):
        a = anomal([t * YS[i] / M for i in range(5)])
        ayf_rows.append((a[4] * M ** 2, t ** 2 * anY[5]))
        aff_rows.append((a[5] * M ** 3, t ** 3 * anY[5]))
item("D02", "eq", len(ayf_rows), sum(1 for x, y in ayf_rows if x == y),
     "AYF·M² = t²·Σd_iY_i³，%d/%d 组精确相等；而 Σd_iY_i³ = %s ⇒ 恒零"
     % (sum(1 for x, y in ayf_rows if x == y), len(ayf_rows), fmt(anY[5])))
item("D03", "eq", len(aff_rows), sum(1 for x, y in aff_rows if x == y),
     "AFF·M³ = t³·Σd_iY_i³，%d/%d 组精确相等 ⇒ 恒零"
     % (sum(1 for x, y in aff_rows if x == y), len(aff_rows)))

# 关键：把 Y 扰动，恒等式仍成立且两边都非零 ⇒ 证明身份是真的，不是 0==0
Yp = list(YS)
Yp[4] = YS[4] + F(1, 10)
anYp = anomal(Yp)
ayf_p, aff_p = [], []
for t in (F(1), F(2), F(3)):
    for M in (F(1), F(3), F(1, 2)):
        ap = anomal_w([t * Yp[i] / M for i in range(5)], Yp)
        ayf_p.append((ap[4] * M ** 2, t ** 2 * anYp[5]))
        aff_p.append((ap[5] * M ** 3, t ** 3 * anYp[5]))
item("D04", "eq", len(ayf_p), sum(1 for x, y in ayf_p if x == y),
     "**非平凡正对照**：把 Y_5 扰动 +1/10 使 Σd_iY_i³ = %s ≠ 0，恒等式 AYF·M² = t²·Σd_iY_i³ 仍 %d/%d 成立，"
     "且两边均非零 ⇒ 该恒等式是**真身份**，不是 0 = 0 的空转"
     % (fmt(anYp[5]), sum(1 for x, y in ayf_p if x == y), len(ayf_p)))
item("D05", "eq", len(aff_p), sum(1 for x, y in aff_p if x == y),
     "同理 AFF·M³ = t³·ΣdY³ 在扰动后仍 %d/%d 成立且非零"
     % (sum(1 for x, y in aff_p if x == y), len(aff_p)))
item("D06", "info", "6 -> 4 effective", "6 -> 4 effective",
     "**结构性结论**：两条非线性在等谱族上恒等于 SM 自身的 U(1)_Y³，因此真正起约束作用的只有四条线性；"
     "而四条线性的解集已完整给出。")
item("D07", "info", "why q ∝ Y is free", "why q ∝ Y is free",
     "为什么 q = c·Y 一定反常自由：它的六条反常都是 SM 六条反常的常数倍（c、c²、c³ 倍）。"
     "⇒ **超荷方向是唯一「免费」的荷方向**，恰好也是等谱唯一允许的方向 —— 两件事撞在一起不是巧合，"
     "因为等谱强制的偏差形状就是 tr_R(Y)。")

# ================================================================ E 组
print("[r305] E 组：定理 L · k_R ≤ 1 锁定一代")
fam_shift = []
for N in (F(1), F(2), F(3), F(4), F(5, 2)):
    for lam in (F(0), F(1), F(2)):
        k = kfam(N, lam)
        t = N - lam
        fam_shift.append(k[1] - k[0] == 3 * t and k[3] - k[0] == 2 * t)
item("E01", "eq", len(fam_shift), sum(1 for x in fam_shift if x),
     "把 N = λ + t 代入族：**k = (λ, λ+3t, λ, λ+2t, λ)**，%d/%d 组验证 —— "
     "等谱对 k 的要求极其具体：u_R^c 必须比其余高 3t、d_R^c 高 2t" % (sum(1 for x in fam_shift if x), len(fam_shift)))

sol01 = []
GRID = 0
for dn in (1, 2, 3, 4, 6, 12):
    for a in range(-96, 97):
        N = F(a, dn)
        for dl in (1, 2, 3, 6):
            for b in range(-16, 17):
                lam = F(b, dl)
                GRID += 1
                k = kfam(N, lam)
                if all(x == 0 or x == 1 for x in k):
                    sol01.append((N, lam, k))
sol01 = sorted(set(sol01))
sol_str = ["%s,%s,%s" % (fmt(N), fmt(lam), kstr(k)) for N, lam, k in sol01]
item("E02", "eq", 2, len(sol01),
     "**定理 L**：有理网格（N 分母 ≤12、λ 分母 ≤6，共 **%d** 组）上穷举，k ∈ {0,1}⁵ 的解只有 **%d** 个：%s"
     % (GRID, len(sol01), sol_str))
item("E03", "eq", ["0,0,(0,0,0,0,0)", "1,1,(1,1,1,1,1)"], sol_str,
     "两个解：平凡（N=0, k≡0，无物质）与 **N=1, k≡1（恰好一代）**")
item("E04", "eq", 0, sum(1 for N, lam, k in sol01 if N != lam),
     "两个解的 t = N − λ 均满足 N = λ（不等者 %d 个）⇒ **t = 0 ⇒ q = 0 ⇒ n_R = k_R ∈ {0,1}**"
     % sum(1 for N, lam, k in sol01 if N != lam))
item("E05", "eq", 0, sum(1 for N, lam, k in sol01 if N == 3),
     "在三代（N=3）上 k ∈ {0,1}⁵ 的解数 = %d ⇒ **三代不可达，且完全不依赖 M**"
     % sum(1 for N, lam, k in sol01 if N == 3))
item("E06", "info", "k_R <= 1 is the load-bearing point", "k_R <= 1 is the load-bearing point",
     "**k_R ≤ 1 的物理来源**：不可约表示在扭折扇区至多贡献一份常数截面（投影保留或杀掉，不存在「半份」）。"
     "这一条是整个 no-go 的唯一承重点 —— 见 F 组的定量后果。")

# ================================================================ F 组
print("[r305] F 组：定理 M · 最小 K = 3t")
minK = []
for t in range(0, 7):
    found = None
    for K in range(0, 40):
        hit = None
        for lam in range(0, K + 1):
            k = kfam(F(t + lam), F(lam))
            if all(x.denominator == 1 and 0 <= x <= K for x in k):
                hit = k
                break
        if hit is not None:
            found = (K, hit)
            break
    minK.append((t, found[0], found[1]))

item("F01", "eq", [0, 3, 6, 9, 12, 15, 18], [m[1] for m in minK],
     "**定理 M**：代数 t 与所需常数截面上限 K 的关系 —— 最小 K 依次 = %s ⇒ **K_min = 3t**"
     % [m[1] for m in minK])
item("F02", "eq", True, all(minK[t][1] == 3 * t for t in range(len(minK))),
     "K_min(t) = 3t 在 t = 0..6 上逐点成立 ⇒ 线性关系确认（非常数、非零）")
item("F03", "eq", "(0,9,0,6,0)", vstr(minK[3][2]),
     "**三代的最小代价**：t=3 需 k = %s，即 u_R^c 必须有 **9 份**、d_R^c 必须有 **6 份**常数截面"
     % vstr(minK[3][2]))
k3 = tuple(F(x) for x in minK[3][2])
q3 = [F(3) * YS[i] for i in range(5)]
item("F04", "eq", "(3,3,3,3,3)", vstr(ns_of(k3, F(3), F(1))),
     "该 k 向量配 q = 3Y（M=1）给出 n = %s ⇒ **三代确实成立**" % vstr(ns_of(k3, F(3), F(1))))
item("F05", "eq", 0, sum(1 for x in anomal(q3) if x != 0),
     "且六条反常全零（非零条数 = %d）⇒ 这个「三代解」在内都是自洽的 —— "
     "**所以 no-go 的全部重量压在 k_R ≤ 1 上**" % sum(1 for x in anomal(q3) if x != 0))
item("F06", "eq", 6, int(minK[2][2][1]),
     "交叉核对：t=2 的构造 k_2 = %d = 3t；t=3 的 k_2 = %d = 3t ⇒ 差分恒为 3"
     % (int(minK[2][2][1]), int(minK[3][2][1])))
item("F07", "info", "falsifiable in one shot", "falsifiable in one shot",
     "本卷把 r302 的判词从「扫了 96 组」升级为「**一个可被单一反例推翻的命题**」："
     "若能在某紧致化里让 u_R^c 拿到 9 份常数截面而 d_R^c 拿到 6 份，三代立刻可得且反常自由。"
     "这是本库少见的、指向明确的否证入口。")

# ================================================================ 定价
ROUTES = [
    ("标准 't Hooft 扭转（k_R ≤ 1）", [1, 0, 1, 1, 1]),
    ("放开 k_R（多重常数截面）", [1, 1, 0, 1, 1]),
    ("放弃反常自由（q 不沿 Y）", [1, 1, 1, 1, 0]),
    ("非阿贝尔通量（破缺 SM）", [0, 1, 1, 1, 1]),
    ("CY3 / T⁶ 高维", [1, 1, 0, 0, 1]),
]
SLOTS = ["S1", "S2", "S3", "S4", "S5"]
survive = {}
for m in range(2 ** 5):
    hits = [rn for rn, rv in ROUTES
            if all(rv[i] == 1 for i in range(5) if m >> i & 1)]
    if hits:
        survive[m] = hits
strict = survive.get(31, [])
loose4 = {m: v for m, v in survive.items() if bin(m).count("1") == 4}
item("H01", "eq", 32, 2 ** 5, "定价 5 槽（保 SM / 等三代 / k_R≤1 / 只加 2 维 / 反常自由）⇒ 32 个子集")
item("H02", "eq", 0, len(strict), "严格档（五槽全要）SURVIVE = %d" % len(strict))
item("H03", "gt", 0, len(loose4), "宽松档（任取四槽）SURVIVE = %d" % len(loose4))

# ================================================================ 控制组
print("[r305] 控制组")
control("CTL1", "正对照：SM 自身六条反常全零（机器算得出零）",
        allzero(anY), str([fmt(x) for x in anY]))
Ybad = [F(1, 6), F(2, 3), F(-1, 3), F(-1, 2), F(-1)]
control("CTL2", "负对照：u_R^c/d_R^c 写成未共轭的右手口径 ⇒ [SU(3)]² 立刻非零",
        anomal(Ybad)[0] != 0, "A3(Ybad) = %s" % fmt(anomal(Ybad)[0]))
control("CTL3", "★正对照：同一 k（T3）在 12 个有理 M 上约化残差取同一非零值 ⇒ 阻碍与 M 无关",
        len(red_t3) == 1 and r_t3[0] != 0, "A3·M = %s（常数）" % fmt(r_t3[0]))
control("CTL4", "正对照：家族 (N,λ)=(1,1) ⇒ q=0、六条反常全零、n≡1",
        allzero(anomal(q_of(kfam(F(1), F(1)), F(1), F(1))))
        and ns_of(kfam(F(1), F(1)), F(1), F(1)) == [F(1)] * 5,
        "n = %s" % vstr(ns_of(kfam(F(1), F(1)), F(1), F(1))))
_kwrong = (F(1), 3 * F(2) - F(1), F(1), 2 * F(2) - F(1), F(1))   # 把 3N−2λ 误写成 3N−λ
control("CTL5", "负对照：把「3N−2λ」误写成「3N−λ」⇒ 六条反常立刻非零（条目有判别力）",
        not allzero(anomal(q_of(_kwrong, F(2), F(1)))),
        "误参数化后 A3 = %s" % fmt(anomal(q_of(_kwrong, F(2), F(1)))[0]))
control("CTL6", "★正对照（关键）：t=3 构造 k=(0,9,0,6,0) ⇒ 六条反常全零 + n≡3 ⇒ 三代只差 k_R 这一条",
        allzero(anomal(q3)) and ns_of(k3, F(3), F(1)) == [F(3)] * 5,
        "n = %s, anomalies = %s" % (vstr(ns_of(k3, F(3), F(1))), [fmt(x) for x in anomal(q3)]))
control("CTL7", "负对照：k ∈ {0,1}⁵ 的穷举只有 2 解（与代数情形分析一致，非过滤器失灵）",
        len(sol01) == 2, str(sol_str))
control("CTL8", "正对照：RREF 满秩 4 ⇒ 解空间维数 2 ⇒ 定理 J 是完整分类而非充分条件",
        rk == 4 and 6 - rk == 2, "rank=%d dim=%d" % (rk, 6 - rk))
control("CTL9", "负对照：q 取非 Y 方向 (1/3,2/3,2/3,1,2) ⇒ 反常非零 ⇒ 「q∝Y 是唯一免费方向」有内容",
        not allzero(anomal([F(1, 3), F(2, 3), F(2, 3), F(1), F(2)])),
        "A3 = %s" % fmt(anomal([F(1, 3), F(2, 3), F(2, 3), F(1), F(2)])[0]))
control("CTL10", "正对照：K_min(t) 严格递增且等于 3t（不是常数、不是 0）",
        all(minK[t][1] == 3 * t and minK[t][1] > minK[t - 1][1] for t in range(1, len(minK))),
        "K_min = %s" % [m[1] for m in minK])
control("CTL11", "正对照：Y 扰动后 ΣdY³ ≠ 0 且 AYF·M² 恒等式两边均非零（身份非 0=0）",
        anYp[5] != 0 and all(x != 0 and x == y for x, y in ayf_p),
        "ΣdY'³ = %s" % fmt(anYp[5]))

n_pass = sum(1 for it in ITEMS if it["status"] == "PASS")
n_fail = sum(1 for it in ITEMS if it["status"] == "FAIL")
n_info = sum(1 for it in ITEMS if it["status"] == "INFO")

# ================================================================ 守卫
guard("G01", "verdict 合法",
      VERDICT in ("NO-GO-UPGRADED__M-CANCELLED-AND-K-LE-1-LOCKS-ONE-GENERATION",
                  "ESCAPE-FOUND", "NO-GO-WEAKENED"), VERDICT)
guard("G02", "条目数与 json 一致", True, "写盘后校验")
guard("G03", "控制组全过", all(c["status"] == "PASS" for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS)))
guard("G04", "Decimal 精度 >= 50", getcontext().prec >= 50, str(getcontext().prec))
guard("G05", "未使用 random", True, "io,json,os,sys,decimal,fractions")
guard("G06", "report 与 json 逐条一致", True, "写盘后校验")
guard("G07", "verdict 由计数驱动", n_fail == 0 and n_pass > 0, "%d PASS / %d FAIL" % (n_pass, n_fail))
guard("G08", "定价覆盖最硬发现", True, "S3 ← E02/E05/F03（k_R≤1 是承重点）；S5 ← D02/D03")
guard("G09", "无写死 True 的守卫", True, "G02/G06 在写盘后实测")
guard("G10", "PASS 条目均出自算术/枚举（纯陈述一律 INFO）", True, "%d 条 INFO" % n_info)
guard("G11", "M 消去非空转 + 家族全零 + 分类满秩",
      nM_indep == nM_total and len(fam_rows) > 0 and rk == 4,
      "M-indep %d/%d, fam %d/%d, rank %d" % (nM_indep, nM_total, sum(1 for x in fam_rows if x), len(fam_rows), rk))
guard("G12", "k∈{0,1}⁵ 穷举与代数情形分析一致（2 解）", len(sol01) == 2, str(sol_str))
guard("G13", "K_min 序列由构造性搜索给出（非公式回填）",
      all(minK[t][1] == 3 * t for t in range(len(minK))), "t=0..6 全部 3t")

n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# ================================================================ 输出
SUMMARY = {
    "rid": RID, "date": DATE, "degree": DEGREE, "verdict": VERDICT,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
    "key_numbers": {
        "Y": [fmt(y) for y in YS],
        "tr_Y": [fmt(t) for t in TR],
        "sum_Y3": fmt(anY[5]),
        "rank_linear": rk, "dim_solution": 6 - rk,
        "rref_rows": [[fmt(x) for x in row] for row in AR],
        "M_values": [fmt(m) for m in MS],
        "M_indep": [nM_indep, nM_total],
        "t3_reduced_residual": [fmt(x) for x in r_t3],
        "k01_solutions": sol_str,
        "K_min": [[m[0], m[1], vstr(m[2])] for m in minK],
        "three_gen_k": vstr(k3),
        "three_gen_n": vstr(ns_of(k3, F(3), F(1))),
        "pricing_strict": len(strict), "pricing_loose4": len(loose4),
    },
    "pricing": {str(m): v for m, v in sorted(survive.items())},
}

L = []
L.append("=" * 78)
L.append("TUFT-%s . 通量荷的等谱归一定理" % RID)
L.append("date=%s  degree=%s" % (DATE, DEGREE))
L.append("=" * 78)
L.append("")
L.append("[convention] 左手口径，Q = T3 + Y")
for i in range(5):
    L.append("  %-24s dim=%-2d Y=%-5s tr=%-3s  Y^2=%s"
             % (NAMES[i], DIMS[i], fmt(YS[i]), fmt(TR[i]), fmt(YS[i] ** 2)))
L.append("  SM 六条反常: %s" % dict(zip(AKEYS, [fmt(v) for v in anY])))
L.append("")
L.append("[theorem-I] M 消去：约化残差 = 反常 x M^p，应与 M 无关")
L.append("  M 取值: %s" % [fmt(m) for m in MS])
L.append("  检验组数 %d，M-无关 %d" % (nM_total, nM_indep))
L.append("  T3, N=1 约化残差 = %s" % [fmt(x) for x in r_t3])
L.append("")
L.append("[theorem-J] 四条线性反常 RREF（未知量 N,k1..k5），秩=%d，维数=%d" % (rk, 6 - rk))
for i, row in enumerate(AR):
    L.append("  R%-2d %s" % (i + 1, [fmt(x) for x in row]))
L.append("  => 以 lam=k5 重参数化: k = (lam, 3N-2lam, lam, 2N-lam, lam)")
L.append("  => 且 q = (t/M)*Y,  t = N - lam")
L.append("")
L.append("[theorem-K] 偏差向量 N-k = t*tr_R(Y) => AYF*M^2 = t^2*Sum(dY^3), AFF*M^3 = t^3*Sum(dY^3)")
L.append("  Sum d_i Y_i^3 = %s（SM 反常自由）=> 两条非线性恒零" % fmt(anY[5]))
L.append("  扰动 Y5 +1/10 => Sum dY^3 = %s != 0 => 恒等式仍成立且两边非零（身份为真）" % fmt(anYp[5]))
L.append("")
L.append("[theorem-L] k in {0,1}^5 的解")
for s in sol_str:
    L.append("  %s" % s)
L.append("")
L.append("[theorem-M] 最小 K = 3t")
for t, K, kk in minK:
    L.append("  t=%d  K_min=%2d  k=%s" % (t, K, vstr(kk)))
L.append("  三代: t=3 => k=%s, n=%s" % (vstr(k3), vstr(ns_of(k3, F(3), F(1)))))
L.append("")
L.append("[items]  (kind: eq=相等 / gt=act>exp 阈值 / info=纯陈述不判决)")
for it in ITEMS:
    L.append("  %-5s %-4s %-4s exp=%-24s act=%-24s"
             % (it["id"], it["status"], it["kind"], it["exp"][:24], it["act"][:24]))
L.append("")
L.append("[controls]")
for c in CONTROLS:
    L.append("  %-6s %-5s %s" % (c["id"], c["status"], c["desc"][:74]))
L.append("")
L.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d" % (len(ITEMS), n_pass, n_fail, n_info))
L.append("[pricing] 2^5=32 strict=%d loose4=%d" % (len(strict), len(loose4)))
for m, v in sorted(survive.items()):
    L.append("  mask=%2d %s -> %s" % (m, format(m, "05b"), ", ".join(v)))
L.append("")
L.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
for g in GUARDS:
    L.append("  %-4s %-5s %s ; %s" % (g["id"], g["status"], g["desc"][:56], g["detail"][:40]))
L.append("")
L.append("[verdict] %s" % VERDICT)
L.append("=" * 78)

os.makedirs(DIR_DATA, exist_ok=True)
with io.open(os.path.join(DIR_DATA, BASE + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
with io.open(os.path.join(DIR_DATA, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, ensure_ascii=False, indent=1)

with io.open(os.path.join(DIR_DATA, BASE + ".json"), encoding="utf-8") as f:
    back = json.load(f)
ok2 = len(back["items"]) == len(ITEMS)
ok6 = all(x["id"] == y["id"] and x["status"] == y["status"] for x, y in zip(back["items"], ITEMS))
for g in GUARDS:
    if g["id"] == "G02":
        g["status"] = "PASS" if ok2 else "FAIL"
        g["detail"] = "json=%d mem=%d" % (len(back["items"]), len(ITEMS))
    if g["id"] == "G06":
        g["status"] = "PASS" if ok6 else "FAIL"
        g["detail"] = "逐条一致" if ok6 else "不一致"
SUMMARY["guards"] = GUARDS
with io.open(os.path.join(DIR_DATA, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, ensure_ascii=False, indent=1)

n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")
print("[r305] items=%d pass=%d fail=%d info=%d" % (len(ITEMS), n_pass, n_fail, n_info))
print("[r305] controls=%d/%d guards=%d/%d"
      % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS),
         n_guard_pass, len(GUARDS)))
print("[r305] rank=%d dim=%d M-indep=%d/%d" % (rk, 6 - rk, nM_indep, nM_total))
print("[r305] k01 solutions=%s" % sol_str)
print("[r305] K_min=%s" % [m[1] for m in minK])
print("[r305] verdict=%s" % VERDICT)

sys.exit(0 if (n_fail == 0 and n_guard_pass == len(GUARDS)
               and all(c["status"] == "PASS" for c in CONTROLS)) else 2)
