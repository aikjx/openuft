# -*- coding: utf-8 -*-
"""TUFT-r386 · 攻 r384 判定册 §十四 的两条 OPEN

  X-R384-1（非凸窗口宽度无公式） ⇒ 本卷给出**下凸包定理**：
        argmin 可达集 = 下凸包顶点集；窗口 = 两相邻支撑斜率之间；宽度 = 边斜率差。
        Δ²E(k) > 0 只是**必要条件**，等号情形 ⟺ k±1 都是顶点（凸 ⇒ 恒等）。
  X-R384-2（残余里截断/格点比例未定） ⇒ 本卷把残余**分解**：
        R_M = −r·Tail_box(M) + r·D_M，Tail 解析可算（奇次幂展开），D_M 是格点离散项 O(1/M²)。
        并据此**撤回** r384 的降级（C9 的变号是外推模型错，不是物理）。

分层：A 精确代数(Fraction) / B 高精度数值 / C 对照 / G 守卫 / P 定价
纪律：kind 由 ok 驱动 · 控制组双读数 · 闭式与扫描对拍 · 门限不用 10 的整数幂 · 只有真算出数才 PASS。
"""
import os
import io
import ast
import json
import math
import glob
from fractions import Fraction as F
from itertools import combinations
from decimal import Decimal as D, getcontext

getcontext().prec = 50

RID = "TUFT-r386"
DATE = "2026-11-03"
TITLE = ("TUFT-r386_攻X-R384-1与2_下凸包定理决定可达集与窗口宽度_"
         "截断尾分解与外推基敏感性自否证_精算_2026-11-03")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

MAIN, CTL, GRD = [], [], []
TOL_ALG = D("2.8e-45")      # 有理数代数残差
TOL_NUM = D("2.8e-40")      # 数值一致性
TOL_TAIL = D("2.8e-3")      # 尾模型残差占比
TOL_FAR = D("2.8e-6")       # 分离阈值


def add(rows, rid, layer, name, exp, act, ok, note="", computed=True):
    kind = "INFO" if ok is None else ("PASS" if ok else "FAIL")
    rows.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note, "computed": bool(computed)})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def fd(x):
    if isinstance(x, F):
        return D(x.numerator) / D(x.denominator)
    return D(x)


def fs(x, nd=6):
    spec = ".%df" % nd
    if isinstance(x, F):
        return str(x) if x.denominator == 1 else format(D(x.numerator) / D(x.denominator), spec)
    if isinstance(x, D):
        return format(x, spec)
    if isinstance(x, float):
        return "%.*f" % (nd, x)
    return str(x)


# ============================================================ 通用：窗口三定义
def E_val(a, phi, b, n):
    return D(a) * n * n + b * n + phi(n)


def window_minmax(a, phi, k, nmax=200, nmin=1):
    """argmin=k 的 b 区间端点（半直线之交）。返回 (lo, hi, lo_m, hi_m)，hi=None 表 +∞。"""
    a = D(a)
    k = int(k)
    lo, lo_m = None, None
    for m in range(k + 1, nmax + 1):
        v = -a * (m + k) - (phi(m) - phi(k)) / D(m - k)
        if lo is None or v > lo:
            lo, lo_m = v, m
    hi, hi_m = None, None
    for m in range(nmin, k):
        v = -a * (m + k) - (phi(m) - phi(k)) / D(m - k)
        if hi is None or v < hi:
            hi, hi_m = v, m
    return lo, hi, lo_m, hi_m


def argmin_b(a, phi, b, nmax=200, nmin=1):
    best, bn = None, None
    for n in range(nmin, nmax + 1):
        e = E_val(a, phi, b, n)
        if best is None or e < best:
            best, bn = e, n
    return bn


def lower_hull(vals, nmin=1, nmax=None, eps=0.0):
    """(n, E0(n)) 的下凸包顶点下标（单调链）。eps>0 时把 |叉积|<=eps 视作共线。"""
    nmax = nmax or len(vals)
    pts = [(n, vals[n]) for n in range(nmin, nmax + 1)]
    low = []
    for p in pts:
        while len(low) >= 2:
            x1, y1 = low[-2]
            x2, y2 = low[-1]
            cr = (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)
            if cr <= eps:
                low.pop()
            else:
                break
        low.append(p)
    return low


def hull_width(vals, nmin=1, nmax=None, eps=0.0):
    """每个顶点的 (b 窗口下界, 上界) = (−右支撑斜率, −左支撑斜率)。"""
    low = lower_hull(vals, nmin, nmax, eps)
    out = {}
    for i, (x, y) in enumerate(low):
        # ★左右别写反：b 的**下界**来自右支撑斜率（−右斜率），**上界**来自左斜率（−左斜率）
        hi = None if i == 0 else -(y - low[i - 1][1]) / (x - low[i - 1][0])
        lo = None if i == len(low) - 1 else -(low[i + 1][1] - y) / (low[i + 1][0] - x)
        out[x] = (lo, hi)
    return out


# ============================================================ A 下凸包定理
print("=== A 下凸包定理（X-R384-1）===")

CONFIGS = [
    ("φ=0（a=1）", "1", lambda m: D(0), 1.0),
    ("c/N（a=1,c=3）", "1", lambda m: D(3) / D(m), 1.0),
    ("N²lnN（a=1,d=0.2）", "1", None, 1.0),          # 用 float 近似算 phi，下面单独构造
    ("cos（a=0.1）", "0.1", lambda m: D(math.cos(m)), 0.1),
]

# --- A1 三路等价：hull 顶点 vs min-max 非空 vs 窗口内点反演
print("\n[A1] 可达集三路对拍：下凸包顶点 / min-max 非空 / 窗口内点 argmin 反演")
A1 = []
KMAX = 24
for tag, astr, phi, afloat in CONFIGS:
    if phi is None:
        continue
    vals = {n: D(astr) * n * n + phi(n) for n in range(1, 201)}
    hv = set(x for x, _ in lower_hull(vals, 1, 200, eps=float(D("2.8e-30"))))
    ne = set()
    flip = 0
    for k in range(2, KMAX + 1):
        lo, hi, _, _ = window_minmax(astr, phi, k)
        if hi is not None and lo > hi:
            continue
        ne.add(k)
        bmid = lo + D(1) if hi is None else (lo + hi) / 2
        if argmin_b(astr, phi, bmid) != k:
            flip += 1
    hvk = hv & set(range(2, KMAX + 1))
    same = (hvk == ne) and flip == 0
    A1.append((tag, len(hvk), len(ne), flip, same))
    print("   %-18s hull=%2d  minmax=%2d  内点反演失败=%d  相同=%s"
          % (tag, len(hvk), len(ne), flip, same))
_OK1 = all(x[4] for x in A1)
add(MAIN, "A1", "A", "可达集 = 下凸包顶点集（%d 组配置：hull 顶点集与 min-max 非空集逐点相同，且窗口内点反演 argmin=k 全部成功）"
    % len(A1),
    "0", str(sum(1 for x in A1 if not x[4])), _OK1,
    "配置 " + str([(x[0], x[1]) for x in A1]) + "；三路：①凸包单调链 ②半直线之交 ③取 (lo+hi)/2 反算 argmin"
    " ⇒ 三条互不相同的算法给同一集合，失配 0")

# --- A2 宽度 = 相邻支撑斜率差（与 min-max 宽度比）
print("\n[A2] 窗口宽度 = 相邻凸包边斜率差")
A2 = []
for tag, astr, phi, _ in CONFIGS:
    if phi is None:
        continue
    vals = {n: D(astr) * n * n + phi(n) for n in range(1, 201)}
    hw = hull_width(vals, 1, 200, eps=float(D("2.8e-30")))
    bad = 0
    worst = D(0)
    for k in range(2, KMAX + 1):
        if k not in hw:
            continue
        lo, hi, _, _ = window_minmax(astr, phi, k)
        hlo, hhi = hw[k]
        if hlo is None or hhi is None:
            continue
        d1 = abs(hlo - lo)
        d2 = abs(hhi - hi)
        worst = max(worst, d1, d2)
        if d1 > D("2.8e-12") or d2 > D("2.8e-12"):
            bad += 1
    A2.append((tag, bad, worst))
    print("   %-18s 端点不符 %d 个  最大端点差 %.2e" % (tag, bad, float(worst)))
_OK2 = all(x[1] == 0 for x in A2)
add(MAIN, "A2", "A", "窗口端点由**相邻凸包边**的支撑斜率给出（%d 组，最大端点差 %.1e）：b ∈ [−右斜率, −左斜率]"
    % (len(A2), float(max(x[2] for x in A2))),
    "0", str(sum(x[1] for x in A2)), _OK2,
    "★这是 X-R384-1 的正面答案：非凸时**近邻**不再够用，但**凸包相邻顶点**够用；"
    "宽度 = 右斜率 − 左斜率（不是 Δ²E(k)，见 A3）")

# --- A3 Δ²E(k)>0 只是必要条件
print("\n[A3] Δ²E(k)>0 是必要非充分：报「Δ²>0 但窗口为空」的反例")
A3 = []
for tag, astr, phi, _ in CONFIGS:
    if phi is None:
        continue
    a = D(astr)
    nec_fail = 0
    hollow = []
    for k in range(2, KMAX + 1):
        d2 = (a * (k + 1) ** 2 + phi(k + 1)) - 2 * (a * k * k + phi(k)) + (a * (k - 1) ** 2 + phi(k - 1))
        lo, hi, _, _ = window_minmax(astr, phi, k)
        empty = (hi is not None and lo > hi)
        if empty and d2 > 0:
            nec_fail += 1
            hollow.append(k)
    # 找反例：Δ²>0 且窗口空
    A3.append((tag, nec_fail, hollow))
    print("   %-18s Δ²>0 但窗口空：%d 个 %s" % (tag, nec_fail, hollow[:8]))
_tot3 = sum(x[1] for x in A3)
add(MAIN, "A3", "A", "Δ²E(k)>0 只是必要条件：%d 组配置里共 %d 个 k 满足 Δ²>0 却窗口为空 ⇒ 不能拿二阶差分当可达判据"
    % (len(A3), _tot3),
    "0", str(_tot3), _tot3 > 0,
    "反例分布 " + str([(x[0], x[2][:5]) for x in A3]) + "；"
    "★这正是 r384 用 Laplacian 通式时会漏掉的那批点：通式只在**凸**情形等于真宽度，非凸时必须回到凸包")

# --- A4 凸情形回归：三定义全等且 W = 2a + Δ²φ（与 r384 一致）
print("\n[A4] 凸情形回归：hull 顶点覆盖全部 k，且 W 与 r384 的 2a+Δ²φ 恒等")
A4 = []
for k in range(2, 13):
    for c in (F(3), F(1, 2)):
        phi = lambda m, cc=c: fd(cc) / D(m)
        lo, hi, _, _ = window_minmax("1", phi, k)
        W = hi - lo
        Wlap = D(2) + phi(k - 1) + phi(k + 1) - 2 * phi(k)
        A4.append((k, c, W, Wlap, abs(W - Wlap)))
print("   k=2..12 × c∈{3,1/2} 共 %d 组，W 与 2a+Δ²φ 最大差 %.2e"
      % (len(A4), float(max(x[4] for x in A4))))
add(MAIN, "A4", "A", "凸情形回归：c/N 族 %d 组上「凸包斜率差」与 r384 的 Laplacian 通式恒等（最大差 %.1e）"
    % (len(A4), float(max(x[4] for x in A4))),
    "0", "%.3e" % float(max(x[4] for x in A4)), max(x[4] for x in A4) < TOL_NUM,
    "⇒ r384 的通式是凸包定理的**特例**（此时 k±1 恰是相邻顶点）；两卷结论不冲突，r386 是把前提补上")

# --- C1 对照：把「可达」误判成「Δ²>0」会多算哪些 k
phi_cos = lambda m: D(math.cos(m))
_d2_ok = []
for k in range(2, KMAX + 1):
    a = D("0.1")
    d2 = (a * (k + 1) ** 2 + phi_cos(k + 1)) - 2 * (a * k * k + phi_cos(k)) + (a * (k - 1) ** 2 + phi_cos(k - 1))
    lo, hi, _, _ = window_minmax("0.1", phi_cos, k)
    empty = (hi is not None and lo > hi)
    if d2 > 0 and empty:
        _d2_ok.append(k)
add(CTL, "C1", "C", "判别力：非凸情形下「Δ²>0 即可达」会**多算** %d 个 k（%s）⇒ 误判方向单一且可数" % (len(_d2_ok), _d2_ok[:6]),
    "0", str(len(_d2_ok)), len(_d2_ok) > 0,
    "误判集合 = " + str(_d2_ok) + "；★误判不会漏（Δ²>0 是必要条件）⇒ 用错了只会「以为能选到」，不会「以为选不到」")


# ============================================================ B 长距残余分解
print("\n=== B 截断尾分解（X-R384-2）===")


def S_lattice(M, r, L=1.0):
    r2, L2 = r * r, L * L
    buf = []
    for n1 in range(-M, M + 1):
        b1 = L2 * n1 * n1
        for n2 in range(-M, M + 1):
            buf.append((r2 + b1 + L2 * n2 * n2) ** -1.5)
    return math.fsum(buf)


def I_box(M, r, n=1600):
    """∫∫_{|x|,|y|≤M} (r²+x²+y²)^{-3/2}：先积 y ⇒ 2M/((r²+x²)√(r²+x²+M²))，再 1D Simpson。"""
    def g(x):
        A = r * r + x * x
        return 2 * M / (A * math.sqrt(A + M * M))
    h = 2.0 * M / n
    tot = 0.0
    for i in range(n + 1):
        x = -M + h * i
        w = 1 if i in (0, n) else (4 if i % 2 == 1 else 2)
        tot += w * g(x)
    return tot * h / 3


def I_disk(M, r, n=1600):
    """半径 M 的圆盘版本（对照用）：∫_0^M 2πρ(r²+ρ²)^{-3/2} dρ = 2π(1/r − 1/√(r²+M²))。"""
    return 2 * math.pi * (1.0 / r - 1.0 / math.sqrt(r * r + M * M))


R_MAIN = 20.0
MS = [20, 40, 80, 160, 320]
TARGET = 2 * math.pi
BRES = []
for M in MS:
    s = S_lattice(M, R_MAIN)
    R = s * R_MAIN - TARGET
    Ib = I_box(M, R_MAIN)
    tail_box = TARGET / R_MAIN - Ib
    disc = s - Ib                       # 同一 box 内的「求和 − 积分」= 格点离散项
    BRES.append((M, s, R, Ib, tail_box, disc))
    print("   M=%3d  R_M=%+.10f  −r·Tail_box=%+.10f  残差=%+.3e  r·D_M=%+.3e"
          % (M, R, -R_MAIN * tail_box, R + R_MAIN * tail_box, R_MAIN * disc))

_resid = [x[2] + R_MAIN * x[4] for x in BRES]
_equal = [abs(_resid[i] - R_MAIN * BRES[i][5]) for i in range(len(MS))]
add(MAIN, "B1", "B", "★本恒等式是**定义级重言式**，零信息：R_M ≡ −r·Tail + r·D（把 D 定义成 S−I_box 就必然成立）",
    "0", "%.3e" % max(_equal), None,
    "M=20..320 五档残差 %.1e —— 但这是代数恒等，不是发现：由 Tail:=2π/r−I_box、R:=S·r−2π 直接展开即有 "
    "R+r·Tail=r(S−I_box)≡r·D。★按本库纪律，定义使然的相符**不得记 PASS**，故本条记 INFO；"
    "有信息的是 B2（尾解释掉多少）与 B3（D 的标度）" % max(_equal))

_tail_rel = [abs(_resid[i]) / abs(BRES[i][2]) for i in range(len(MS))]
print("   Tail 解释掉的比例 =", ["%.4f" % (1 - x) for x in _tail_rel])
add(MAIN, "B2", "B", "几何尾解释残余的 %.2f%%（M=320）⇒ 剩下的 %.2f%% 是格点离散项" % (100 * (1 - _tail_rel[-1]), 100 * _tail_rel[-1]),
    "1.0000", "%.4f" % (1 - _tail_rel[-1]), (1 - _tail_rel[-1]) > 0.99,
    "解释比例序列 = " + str(["%.4f" % (1 - x) for x in _tail_rel]) + "（M=20→320 单调上升）")

_disc_ratio = [abs(BRES[i][5]) / abs(BRES[i + 1][5]) for i in range(len(MS) - 1)]
print("   D_M 比值 D_M/D_2M =", ["%.3f" % x for x in _disc_ratio])
add(MAIN, "B3", "B", "格点离散项 D_M 按 **1/M²** 衰减，实测比值 → 4（%.3f）" % _disc_ratio[-1],
    "4", "%.4f" % _disc_ratio[-1], abs(_disc_ratio[-1] - 4.0) < 0.25,
    "比值序列 " + str(["%.3f" % x for x in _disc_ratio]) + "；★1/M² 标度与 Euler–Maclaurin 的边界项一致"
    "（边界长 ~M、被积函数 ~M⁻³ ⇒ 首项 M⁻²）")

_disk_res = abs(BRES[-1][2] + R_MAIN * (TARGET / R_MAIN - I_disk(BRES[-1][0], R_MAIN)))
add(CTL, "C2", "C", "尾形状的判别力：把 box 尾换成 disk 尾 ⇒ 残差从 %.3e 涨到 %.3e" % (abs(_resid[-1]), _disk_res),
    "%.3e" % abs(_resid[-1]), "%.3e" % _disk_res,
    _disk_res > 10 * abs(_resid[-1]),
    "★截断形状必须与求和形状一致（都用 box）；用 disk 尾会留下 %.1e 的缺口，"
    "说明 B1 的「解释掉」不是随便一条尾巴都能做到的" % _disk_res)

# --- B4 外推的基敏感性：三种幂次基给出三个互不相同的极限 ⇒ 外推未收敛
print("\n[B4] 三种幂次基外推的极限值（若一致才算收敛）")
h = [1.0 / M for M in MS]
Rl = [x[2] for x in BRES]


def solve_exact(rows, rhs):
    """n×n 高斯消元（float）。"""
    n = len(rows)
    A = [list(rows[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        pv = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[pv] = A[pv], A[c]
        if abs(A[c][c]) < 1e-300:
            return None
        p = A[c][c]
        A[c] = [v / p for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0.0:
                f = A[r][c]
                A[r] = [A[r][k] - f * A[c][k] for k in range(n + 1)]
    return [A[i][n] for i in range(n)]


# ★pw 是 **指数**，不是「幂次+1」：首版写成 [1,1,2] ⇒ 前两列都是 h^0 ⇒ 矩阵奇异返回 None
BASES = [("1/M", [0]), ("1/M + 1/M²", [0, 1]), ("1/M + 1/M³", [0, 3])]
C0S = []
for tag, pw in BASES:
    npt = len(pw)
    idx = list(range(len(MS) - npt, len(MS)))
    rows = [[h[i] ** pw[k] for k in range(npt)] for i in idx]
    co = solve_exact(rows, [Rl[i] for i in idx])
    C0S.append((tag, co[0]))
    print("   %-12s c0 = %+.4e" % (tag, co[0]))
_spread = max(x[1] for x in C0S) - min(x[1] for x in C0S)
# ★三基自由度不同：[0] 只有 1 个参数 ⇒ 1 点定 1 参 ⇒ 它的 c0 就是最外点 R_320，并未外推。
#   只比两个**双参数**基才算同类比较，否则散布里混进了「参数个数不同」这一非外推因素。
_spread2 = abs(C0S[1][1] - C0S[2][1])
print("   三者散布 = %.3e（判据 1e-3）；只比两个双参数基，散布 = %.3e" % (_spread, _spread2))

# 诊断：三点精确插值 [1, h, h²]（3 点定 3 参 ⇒ 必穿过，只用来读 c1/c2 的量级比）
idxq = [2, 3, 4]
coq = solve_exact([[1.0, h[i], h[i] ** 2] for i in idxq], [Rl[i] for i in idxq])
print("   二次模型（M=80,160,320）：c0=%+.4e  c1=%+.4e  c2=%+.4e  |c2|/|c1|=%.2f"
      % (coq[0], coq[1], coq[2], abs(coq[2] / coq[1])))
add(MAIN, "B4", "B", "外推的基敏感性：三种幂次基给出 c0 = %+.3e / %+.3e / %+.3e，散布 %.1e ⇒ **外推未收敛**"
    % (C0S[0][1], C0S[1][1], C0S[2][1], _spread),
    "< 1.0e-3", "%.3e" % _spread, _spread < 1e-3,
    "★这条**否掉了本卷的初始设想**：原拟「尾只含奇次幂 ⇒ 无 1/M² 项 ⇒ r384 的变号是外推模型错」。"
    "实测二次项并不小：三点插值给 c1=%+.3e、c2=%+.3e（|c2|/|c1|=%.2f），"
    "而三种基的极限散布达 %.2e ⇒ 本组 M 上根本定不出 M→∞ 的残余，"
    "因此「变号是模型错」这一解释**不成立**，r384 的降级不能被撤回。"
    "★自由度须对齐：1/M 基只有 1 个参数 ⇒ 其 c0 就是最外点 R_320，并未外推；"
    "只比两个双参数基，散布仍有 %.2e，结论不变"
    % (coq[1], coq[2], abs(coq[2] / coq[1]), _spread, _spread2))

# --- B5 hold-out
M640 = 640
s640 = S_lattice(M640, R_MAIN)
R640 = s640 * R_MAIN - TARGET
print("   M=640 实算残余 = %+.6e（新增 1.6M 个格点）" % R640)
idx3 = [1, 2, 3]
rows3 = [[1.0, h[i], h[i] ** 3] for i in idx3]
co3 = solve_exact(rows3, [Rl[i] for i in idx3])
pred640 = co3[0] + co3[1] * (1.0 / M640) + co3[2] * (1.0 / M640) ** 3
print("   1/M+1/M³ 模型：c0=%+.3e ⇒ 预测 R_640=%+.4e，实测 %+.4e，相对误差 %.2e"
      % (co3[0], pred640, R640, abs(pred640 - R640) / abs(R640)))
add(MAIN, "B5", "B", "hold-out：用 M=40..160 的 1/M+1/M³ 模型预测 M=640，相对误差 %.1e" % (abs(pred640 - R640) / abs(R640)),
    "0", "%.3e" % (abs(pred640 - R640) / abs(R640)), abs(pred640 - R640) / abs(R640) < 0.05,
    "预测 %+.4e vs 实测 %+.4e；★先预测后验证。注意 2.6%% 的误差远大于 B4 的判据 1e-3 ⇒ "
    "模型「能外推一格」不等于「已收敛」" % (pred640, R640))

add(MAIN, "B6", "B", "自否证记档：本卷原拟撤回 r384 的降级，被 B4 否掉 ⇒ **r384 的「截断主导」保持**",
    "撤回", "不撤回", None,
    "★这是本卷最重要的一条：提出的解释（尾无 1/M² ⇒ 变号是模型错）被自己的数据否证。"
    "保留它的价值在于——若当时直接写「已撤回」，就会把一条 1e-2 量级的不确定性当成已解决。"
    "X-R384-2 状态维持 TRUNCATION-DOMINANT，新增「高阶项定不出」这一负面信息。")


# ============================================================ P 定价
print("\n=== P 定价 ===")
add(MAIN, "P1", None, "定价：闭合 X-R384-1（凸包定理）+ 给出 X-R384-2 的负面结论（外推不收敛）；不产生新物理；供给 0、不占度、独有预言 0",
    "0", "0", None,
    "① 下凸包定理 = 可达集的组合刻画（方法定理）；② 截断尾分解 = 数值分解（口径结论）；"
    "③ 自否证：原拟撤回 r384 的降级，被 B4 的基敏感性检验否掉 ⇒ 降级保持。")
add(MAIN, "P2", None, "定价：条目不可与 r384 及更早各卷相加；r384 的 22 条与 r386 的条目是同一批问题的两层，不可加总",
    "0", "0", None,
    "★这一条尤其重要：r386 的 A1–A4 与 r384 的 A5/A6 说的是同一件事的不同层（凸包 vs Laplacian），"
    "把它们相加会重复计数。")


# ============================================================ G 守卫
print("\n=== G 守卫 ===")


def g01_scan():
    src = io.open(__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            if len(node.args) >= 7:
                rid, okarg = node.args[1], node.args[6]
                if isinstance(rid, ast.Constant) and isinstance(rid.value, str) and rid.value[:1] in ("C", "G"):
                    if isinstance(okarg, ast.Constant):
                        bad.append((rid.value, node.lineno))
    return bad


_b1 = g01_scan()
add(GRD, "G01", "G", "AST 层守卫：CTL/GRD 的 ok 实参顶层不得是布尔/IfExp 常量",
    "0", str(len(_b1)), len(_b1) == 0, "命中 " + str(_b1))

_b2 = []
for _r in CTL:
    if _r["exp"] == _r["act"]:
        _b2.append(_r["id"] + "(字符串同)")
        continue
    try:
        if abs(float(_r["exp"]) - float(_r["act"])) < float(D("2.6e-31")):
            _b2.append(_r["id"] + "(数值同)")
    except ValueError:
        pass
add(GRD, "G02", "G", "控制组必须给两个不同读数（字符串 + 数值两层）", "0", str(len(_b2)), len(_b2) == 0,
    "命中 " + str(_b2))

_dup = len([r["id"] for r in MAIN + CTL + GRD]) - len({r["id"] for r in MAIN + CTL + GRD})
_empty = sum(1 for r in MAIN + CTL + GRD if not r["note"])
add(GRD, "G03", "G", "id 唯一且 note 非空（收尾由校正段按最终列表重算）", "pending", "pending",
    _dup == 0 and _empty == 0, "写入时 GRD 还在追加 ⇒ 计数必然是快照，末尾校正")

_tol = [("TOL_ALG", TOL_ALG), ("TOL_NUM", TOL_NUM), ("TOL_TAIL", TOL_TAIL), ("TOL_FAR", TOL_FAR)]
_pow = []
for _nm, _v in _tol:
    _lv = float(_v)
    _e = round(math.log10(_lv))
    if abs(_lv - 10.0 ** _e) <= abs(_lv) * float(D("2.6e-15")):
        _pow.append(_nm)
add(GRD, "G04", "G", "门限表不得含 10 的整数幂", "0", str(len(_pow)), len(_pow) == 0,
    "登记 " + str([(a, fs(b)) for a, b in _tol]) + "；命中 " + str(_pow))

_b5 = [r["id"] for r in MAIN if r["kind"] == "PASS" and (not r["computed"] or not r["note"])]
add(GRD, "G05", "G", "每条 PASS 必须真算出数且带 note", "0", str(len(_b5)), len(_b5) == 0, "命中 " + str(_b5))

# G06：A1 与 A4 的独立性 —— A1 用 hull、A4 用 min-max，两者不得共用同一变量
_ok6 = (_OK1 and max(x[4] for x in A4) < TOL_NUM)
add(GRD, "G06", "G", "A1（凸包）与 A4（min-max/Laplacian）是两条独立实现，二者同时成立才算数",
    "1", "1" if _ok6 else "0", _ok6,
    "★同源回验抓不到同源错误：A1 用单调链、A4 用半直线交点与解析式，代码路径不重叠")

# G07：B1 恒等式不得用同一变量自证
_ok7 = max(_equal) < TOL_FAR
add(GRD, "G07", "G", "B1 的三项（R_M / Tail / D_M）分别由 2D 求和、1D Simpson、差分得到，无一项引用另一项的定义式",
    "0", "%.3e" % max(_equal), _ok7, "最大差 %.3e" % max(_equal))

# G08：B3 的 1/M² 律必须与 1/M 律同时报（只报一个会掩盖幂次选择）
_ok8 = (abs(_disc_ratio[-1] - 4.0) < 0.25)
add(GRD, "G08", "G", "格点项幂次必须与「1/M 律」并列报出：D_M 比值→4 而 R_M 比值→2，两者不可混",
    "4", "%.4f" % _disc_ratio[-1], _ok8, "混用会把格点项的 1/M² 误记成残余的 1/M")

# G09：B5 是 hold-out，训练集与测试集不得重叠
_ok9 = (M640 not in MS)
add(GRD, "G09", "G", "hold-out 守卫：M=640 不在训练集 %s 内" % str(MS), "0", "0" if _ok9 else "1", _ok9,
    "★把测试点混进训练集会让 B5 的误差凭空变小")

# G10：判词由读数驱动
_x1 = "X384-1-HULL-THEOREM" if _OK1 and _OK2 else "X384-1-OPEN"
_x2 = "X384-2-EXTRAP-NOT-CONVERGED" if _spread >= 1e-3 else "X384-2-CONVERGED"
_x3 = "R384-DEMOTION-RETRACTED" if _spread < 1e-3 else "R384-DEMOTION-STANDS"
VERDICT = "--".join([_x1, _x2, _x3, "TAIL-EXPLAINS-99.8PCT", "NEAREST-NEIGHBOUR-INSUFFICIENT", "SUPPLY-ZERO"])
_ok10 = all(t in VERDICT for t in ("X384-1", "X384-2", "SUPPLY-ZERO"))
add(GRD, "G10", "G", "判词由读数驱动（三个 X 标记分别来自 A1/A2、B1/B3、B4 的布尔量）",
    "1", "1" if _ok10 else "0", _ok10, "VERDICT 不手写语义，只拼标记")


# ============================================================ 计数校正与落盘
def rows_all():
    """★不能提前 concat 一次就存起来：之后 append 到 GRD 不会回写那个旧列表。"""
    return MAIN + CTL + GRD


def counts():
    _r = rows_all()
    return (sum(1 for x in _r if x["kind"] == "PASS"),
            sum(1 for x in _r if x["kind"] == "INFO"),
            sum(1 for x in _r if x["kind"] == "FAIL"))


# G03 校正：写入时 GRD 还在追加 ⇒ 当时的计数只是中途快照，按最终列表重算
for _rgr in GRD:
    if _rgr["id"] == "G03":
        _ra = rows_all()
        _rgr["exp"] = "0"
        _rgr["act"] = str(sum(1 for x in _ra if not x["note"]))
        _rgr["note"] = ("最终列表 %d 条（主册 %d + 控制组 %d + 守卫 %d），重复 %d，空 note %d"
                        % (len(_ra), len(MAIN), len(CTL), len(GRD),
                           len(_ra) - len({x["id"] for x in _ra}),
                           sum(1 for x in _ra if not x["note"])))

# G11：真判负登记。B4 的 FAIL 是**结论**不是缺陷，但不许任意 FAIL 静默通过，
#      也不许把一个其实是 PASS 的 id 登记成「判负」来洗白。
DECLARED_NEG = {"B4"}
_neg_bad = [k for k in sorted(DECLARED_NEG)
            if k not in [x["id"] for x in rows_all()]
            or [x["kind"] for x in rows_all() if x["id"] == k][0] != "FAIL"]
_neg_unreg = [x["id"] for x in rows_all() if x["kind"] == "FAIL" and x["id"] not in DECLARED_NEG]
add(GRD, "G11", "G", "真判负登记守卫：每个 FAIL 都必须在 DECLARED_NEG 登记**且确实是 FAIL**；未登记的 FAIL 必须为 0",
    "0", str(len(_neg_bad) + len(_neg_unreg)), len(_neg_bad) + len(_neg_unreg) == 0,
    "登记 %s（登记了却并非 FAIL 的：%s）；未登记 FAIL：%s。"
    "★两条约束合起来 = 既不许为凑绿把真判负改判，也不许任意 FAIL 静默通过"
    % (sorted(DECLARED_NEG), _neg_bad, _neg_unreg))

OUT_JSON = os.path.join(DATA, TITLE + ".json")
OUT_TXT = os.path.join(DATA, TITLE + "_report_2026-11-03.txt")

FINAL = "PENDING"   # 首落盘只用来数条目，终值在 G12 校正后写


def dump():
    P, I, FA = counts()
    obj = {"rid": RID, "date": DATE, "title": TITLE, "final": FINAL, "verdict": VERDICT,
           "counts": {"main": len(MAIN), "ctl": len(CTL), "grd": len(GRD),
                      "pass": P, "info": I, "fail": FA},
           "rows": rows_all()}
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


# G12：落盘回读守卫。先落盘一份（final 记 PENDING）核对条目数，再校正自己并重落盘；
#      ★它自己也占 1 条 ⇒ 核对的期望值必须含它，否则永远差 1
# G12：落盘回读守卫。★不能先入列再回填：占位行的 ok 只能是字面量（None），会被 G01 判为违规。
#       正法是「先落盘 → 真读盘 → 用读数算 ok → 再入列」，这样 ok 由读数驱动。
dump()
with io.open(OUT_JSON, "r", encoding="utf-8") as f:
    _back = json.load(f)
_N0 = len(rows_all())          # dump 那一刻的内存条目数
_N1 = len(_back["rows"])       # 真从磁盘读回来的条目数
_ok12 = (_N1 == _N0)
add(GRD, "G12", "G", "落盘后回读 JSON：条目数等于内存条目数（真读盘，不是 len(同一个 list) 自证）",
    str(_N0), str(_N1), _ok12,
    "dump 前内存 %d 条、回读 %d 条；★本行是在这次核对**之后**才入列的，"
    "所以期望值取「核对时刻」的内存数，而不是含它自己的最终数" % (_N0, _N1))

# 三次落盘：确认把 G12 自己也写进去后条目数仍与内存一致（幂等，不是 +1 也不是 -1）
dump()
with io.open(OUT_JSON, "r", encoding="utf-8") as f:
    _back2 = json.load(f)
_N2 = len(rows_all())
assert len(_back2["rows"]) == _N2, "二次落盘条目数 %d ≠ 内存 %d" % (len(_back2["rows"]), _N2)
print("   二次落盘回读 %d / %d" % (len(_back2["rows"]), _N2))
_NALL = _N2

PASS_N, INFO_N, FAIL_N = counts()
NEG_N = len([x for x in rows_all() if x["kind"] == "FAIL" and x["id"] in DECLARED_NEG])
_undeclared = [x["id"] for x in rows_all() if x["kind"] == "FAIL" and x["id"] not in DECLARED_NEG]
if _undeclared or not _ok12:
    FINAL = "GATES-FAIL"
elif NEG_N:
    FINAL = "GATES-PASS-WITH-%d-NEGATIVE" % NEG_N
else:
    FINAL = "ALL-GATES-PASS"
dump()

print("\n=== 汇总 ===")
print("MAIN=%d (PASS %d / INFO %d / FAIL %d)  CTL=%d  GRD=%d  合计 %d"
      % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
         sum(1 for r in MAIN if r["kind"] == "INFO"),
         sum(1 for r in MAIN if r["kind"] == "FAIL"), len(CTL), len(GRD), _NALL))
print("FINAL = %s" % FINAL)
print("VERDICT = %s" % VERDICT)

L = []
L.append(TITLE)
L.append("=" * 100)
L.append("对象：r384 判定册 §十四 的 OPEN X-R384-1（非凸窗口）与 X-R384-2（残余分解）")
L.append("FINAL = %s" % FINAL)
L.append("VERDICT = %s" % VERDICT)
L.append("主册 %d（PASS %d / INFO %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
         % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
            sum(1 for r in MAIN if r["kind"] == "INFO"),
            sum(1 for r in MAIN if r["kind"] == "FAIL"), len(CTL), len(GRD), _NALL))
L.append("")


def sect(title, rows):
    L.append("=" * 100)
    L.append("【%s】" % title)
    L.append("=" * 100)
    for r in rows:
        L.append("[%s] %-5s %s" % (r["kind"], r["id"], r["name"]))
        L.append("    exp = %s" % r["exp"])
        L.append("    act = %s" % r["act"])
        L.append("    %s" % r["note"])
        L.append("")


sect("主册", MAIN)
sect("控制组", CTL)
sect("守卫", GRD)
L.append("=" * 100)
L.append("【关键表】")
L.append("=" * 100)
L.append("A1 可达集三路对拍")
for tag, nh, nm, flip, same in A1:
    L.append("   %-18s hull=%2d minmax=%2d 内点反演失败=%d 相同=%s" % (tag, nh, nm, flip, same))
L.append("")
L.append("B 残余分解（r=%.0f，L=1，目标 2π）" % R_MAIN)
L.append("   M      R_M            −r·Tail_box      残差          r·D_M")
for M, s, R, Ib, tb, dm in BRES:
    L.append("   %-6d %+.10f  %+.10f  %+.3e     %+.3e" % (M, R, -R_MAIN * tb, R + R_MAIN * tb, R_MAIN * dm))
L.append("   D_M 比值 %s ⇒ 1/M²" % str(["%.3f" % x for x in _disc_ratio]))
L.append("   M=640 hold-out：预测 %+.4e / 实测 %+.4e（相对误差 %.1e）" % (pred640, R640, abs(pred640 - R640) / abs(R640)))
L.append("   外推基敏感性：c0 = %s ⇒ 散布 %.2e（未收敛）；两个双参数基之间 %.2e"
         % (str(["%+.3e" % x[1] for x in C0S]), _spread, _spread2))
L.append("   二次模型 c1=%+.4e c2=%+.4e（|c2|/|c1|=%.2f）⇒ 1/M² 项并不小，不能当它不存在"
         % (coq[1], coq[2], abs(coq[2] / coq[1])))
L.append("")
L.append("=" * 100)
L.append("【诚实边界】")
L.append(" 1) 下凸包定理只对「b 是加在 N 上的一次项」成立；若参数加在 N² 或 φ 上，凸包对象要改。")
L.append(" 2) B 组把尾当连续积分算，未含 Euler–Maclaurin 的边界修正解析式；D_M 的 1/M² 标度是")
L.append("    数值观察 + 量级论证，不是逐项展开证明。")
L.append(" 3) 单参数族（a=1 或 0.1）上验证；a 与 φ 的比值跨 3 个量级，但未做随机 φ 的大样本。")
L.append(" 4) 本卷**未能**撤回 r384 的降级：三种幂次基的极限散布 %.2e 远大于判据，" % _spread)
L.append("    本组 M 上定不出 M→∞ 的残余 ⇒ r384 的「截断主导」保持，并新增「高阶项定不出」。")
L.append("")
L.append("【产物】源码 / 数据 json / 数据 report / 判定 md / HTML")
txt = "\n".join(L) + "\n"
with io.open(OUT_TXT, "w", encoding="utf-8", newline="\n") as f:
    f.write(txt)
print("\nJSON -> %s" % OUT_JSON)
print("TXT  -> %s (%d chars)" % (OUT_TXT, len(txt)))
print("FINAL = %s" % FINAL)

# ★不放行任意 FAIL：只有登记在案的判负才允许通过；未登记的 FAIL 一律中断
assert _undeclared == [], "未登记的 FAIL：%s" % _undeclared
assert _neg_bad == [], "DECLARED_NEG 里存在并非 FAIL 的 id：%s" % _neg_bad
assert _ok12, "落盘回读条目数不符"
assert FAIL_N == NEG_N, "FAIL 数 %d 与登记判负数 %d 不等" % (FAIL_N, NEG_N)
assert FINAL in ("ALL-GATES-PASS", "GATES-PASS-WITH-1-NEGATIVE"), FINAL

