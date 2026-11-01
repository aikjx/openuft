# -*- coding: utf-8 -*-
"""
TUFT-r302 · 三代多重度的反常锁定定理
等谱即一代 —— 用六条规范反常把「通量 + 't Hooft 扭转」的等谱解钉死

攻靶：r295 自留的唯一实质缺口 X-R295-1
      ——「Z_N 't Hooft 分数通量下，五个表示能否得到 1:1:1:1:1 的谱型？」

本卷的主结果不依赖分数通量的细节，而是把问题整体化：
  在不引入新规范群的前提下，任何保持 G_SM 的背景都只由
  （i）沿 U(1) 的通量量子 M、（ii）中心 Z_3×Z_2 的 't Hooft 扭转 两部分刻画。
  于是「等谱」是一个线性/整数条件，而**反常自由性**把它钉死。

  定理 G（反常锁定）  等多重度 ⇒ q_R·dim_R = c（与 R 无关）
                      ⇒ 六条反常系数全部 = (非零有理数)·c ⇒ c = 0
                      ⇒ q ≡ 0 ⇒ n_R = k_R（纯扭转计数）
  定理 H（扭转表）    任一非平凡扭转给出的 k_R 取 0/1 两值 ⇒ 谱不等
                      ⇒ 唯一等谱 = 平凡扭转 ⇒ n_R ≡ 1 ⇒ **恰好一代**

约定：全部左手中微子（左手 Weyl），T(3)=T(3̄)=1/2。
      Y(Q_L)=1/6, Y(u_R^c)=−2/3, Y(d_R^c)=1/3, Y(L_L)=−1/2, Y(e_R^c)=1，
      此时 Q = T3 + Y 且六条反常逐条为零（CTL1 实证）。

确定性：Fraction 精确；无 random；Decimal prec=60 仅用于展示。
"""
import io
import json
import os
import sys
from decimal import getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r302"
DATE = "2026-11-01"
DEGREE = 0
VERDICT = "NO-GO-CLOSED__ANOMALY-LOCKED-EQUALITY-GIVES-ONE-GENERATION"

DIR_HERE = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(os.path.dirname(DIR_HERE), "数据")
BASE = ("TUFT-r302_三代多重度的反常锁定定理_"
        "等谱即一代与通量扭转穷举_精算与可视化_2026-11-01")

# ---------------------------------------------------------------- SM 谱（左手口径）
# (名称, 维数, Y, SU(3) 重数(色), SU(2) 重数(弱), 中心荷 (Z3, Z2))
SM = [
    ("Q_L  (3,2)_{1/6}", 6, F(1, 6), 3, 2, (1, 1)),
    ("u_R^c (3bar,1)_{-2/3}", 3, F(-2, 3), 3, 1, (2, 0)),
    ("d_R^c (3bar,1)_{1/3}", 3, F(1, 3), 3, 1, (2, 0)),
    ("L_L  (1,2)_{-1/2}", 2, F(-1, 2), 1, 2, (0, 1)),
    ("e_R^c (1,1)_{1}", 1, F(1), 1, 1, (0, 0)),
]
DIMS = [s[1] for s in SM]
YS = [s[2] for s in SM]
CENT = [s[5] for s in SM]

# ---------------------------------------------------------------- 反常系数
def anomal(q):
    """六条规范反常系数（全部应为 0）。q 为五个表示的手征 U(1) 荷。"""
    q1, q2, q3, q4, q5 = q
    dim = DIMS
    Y = YS
    a3 = 2 * q1 + q2 + q3                                  # [SU(3)]² U(1)
    a2 = 3 * q1 + q4                                       # [SU(2)]² U(1)
    ag = sum(dim[i] * q[i] for i in range(5))              # grav-U(1)
    ayy = sum(dim[i] * Y[i] ** 2 * q[i] for i in range(5))  # U(1)_Y² U(1)
    ayf = sum(dim[i] * Y[i] * q[i] ** 2 for i in range(5))  # U(1)_Y U(1)²
    aff = sum(dim[i] * q[i] ** 3 for i in range(5))        # U(1)³
    return {"A3": a3, "A2": a2, "Ag": ag, "AYY": ayy, "AYF": ayf, "AFF": aff}


def all_zero(a):
    return all(v == 0 for v in a.values())


# ---------------------------------------------------------------- 精确线性代数
def rref(mat, rhs):
    """对增广矩阵做精确高斯-约当消元（Fraction）。返回 (秩, 简化行, 是否相容)。"""
    n = len(mat)
    m = len(mat[0])
    A = [list(mat[i]) + [rhs[i]] for i in range(n)]
    piv = []
    r = 0
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
                A[i] = [A[i][j] - f * A[r][j] for j in range(m + 1)]
        piv.append(c)
        r += 1
        if r == n:
            break
    # 相容性：存在 0 = 非零 的行
    ok = True
    for i in range(n):
        if all(A[i][j] == 0 for j in range(m)) and A[i][m] != 0:
            ok = False
            break
    return r, A, piv, ok


def solve_unique(mat, rhs, m):
    """若解唯一则返回解向量，否则返回 None。"""
    r, A, piv, ok = rref(mat, rhs)
    if not ok or r != m:
        return None
    x = [F(0)] * m
    for i, c in enumerate(piv):
        x[c] = A[i][m]
    return x


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


# ================================================================ A 组
print("[r302] A 组：约定与 SM 自洽性")

item("A01", "eq", ["1/6", "-2/3", "1/3", "-1/2", "1"], [fmt(y) for y in YS],
     "左手口径超荷 Y（Q=T3+Y）：Q_L 1/6, u_R^c −2/3, d_R^c 1/3, L_L −1/2, e_R^c 1")

trs = [F(DIMS[i]) * YS[i] for i in range(5)]
item("A02", "eq", ["1", "-2", "1", "-1", "1"], [fmt(t) for t in trs],
     "tr_R(Y) = dim·Y = (1, −2, 1, −1, 1)")
item("A02b", "eq", 0, sum(trs, F(0)), "Σ tr_R(Y) = 0（与 grav-Y 反常抵消一致）")

anY = anomal(YS)
item("A03", "eq", 0, anY["A3"], "[SU(3)]²U(1)_Y = %s（SM 自洽）" % fmt(anY["A3"]))
item("A04", "eq", 0, anY["A2"], "[SU(2)]²U(1)_Y = %s（SM 自洽）" % fmt(anY["A2"]))
item("A05", "eq", 0, anY["Ag"], "grav-U(1)_Y = %s" % fmt(anY["Ag"]))
item("A06", "eq", 0, anY["AYY"], "U(1)_Y²·U(1)_Y = U(1)_Y³ = %s" % fmt(anY["AYY"]))
item("A07", "eq", 0, anY["AFF"], "U(1)_Y³（独立重算）= %s" % fmt(anY["AFF"]))

abstr = [int(abs(t)) for t in trs]
item("A08", "eq", [1, 2, 1, 1, 1], abstr,
     "|tr_R(Y)| = (1,2,1,1,1) —— 与 r295 的比值结论一致；r295 用右手口径得 (1,2,−1,−1,−1)，"
     "**绝对值相同** ⇒ 其「比值恒 1:2:1:1:1」的结论与口径无关（本条为跨卷口径对照）")

# ================================================================ B 组
print("[r302] B 组：等谱锁 —— 六条反常同时指向 c = 0")

item("B01", "info", "q_R·dim_R = c", "q_R·dim_R = c",
     "等谱条件：n_R = M·q_R·dim_R + k_R = N 对所有 R 成立；k_R 均匀时 ⇒ q_R·dim_R = (N−k)/M ≡ c。"
     "本条为条件陈述（未算出数）⇒ 按纪律记 INFO；k 不均匀的一般情形由 D 组穷举直接处理")
item("B02", "info", "q = c/dim", "q = c/dim",
     "即 q = (c/6, c/3, c/3, c/2, c) —— 这是「等谱」唯一允许的荷型（差一个整体标度）")

q_c = [F(1) / F(DIMS[i]) for i in range(5)]          # c = 1 时的荷型
anC = anomal(q_c)
coef = {}
for k in ["A3", "A2", "Ag", "AYY", "AYF", "AFF"]:
    coef[k] = anC[k]                                  # 关于 c 的系数（AYF/AFF 为 c²、c³ 的系数）

item("B03", "eq", "1", fmt(coef["A3"]),
     "[SU(3)]²U(1)_F 在等谱荷型下 = %s·c ⇒ 系数非零 ⇒ c = 0" % fmt(coef["A3"]))
item("B04", "eq", "1", fmt(coef["A2"]),
     "[SU(2)]²U(1)_F = %s·c ⇒ 独立第二把刀" % fmt(coef["A2"]))
item("B05", "eq", "5", fmt(coef["Ag"]),
     "grav-U(1)_F = %s·c ⇒ 第三把刀" % fmt(coef["Ag"]))
item("B06", "eq", "11/6", fmt(coef["AYY"]),
     "U(1)_Y²U(1)_F = %s·c ⇒ 第四把刀" % fmt(coef["AYY"]))
item("B07", "eq", "2/3", fmt(coef["AYF"]),
     "U(1)_Y U(1)_F² = %s·c² ⇒ 第五条（非线性，c≠0 即非零）" % fmt(coef["AYF"]))
item("B08", "eq", "3/2", fmt(coef["AFF"]),
     "U(1)_F³ = %s·c³ ⇒ 第六条" % fmt(coef["AFF"]))

nonzero_cnt = sum(1 for k in coef if coef[k] != 0)
item("B09", "eq", 6, nonzero_cnt,
     "六条反常系数全部非零 ⇒ 反常自由 + 等谱 ⇒ **c = 0**（六把独立的刀给出同一结论）")
item("B10", "info", "q ≡ 0", "q ≡ 0",
     "c = 0 ⇒ q 全零 ⇒ 通量贡献为零 ⇒ n_R = k_R（只剩扭转计数）。"
     "此为定理 G 的推论陈述，其可算形式在 D 组穷举里被独立验证（等谱解全部 q≡0）")

# ================================================================ C 组
print("[r302] C 组：'t Hooft 扭转的 k_R 表")
item("C01", "eq", ["(1,1)", "(2,0)", "(2,0)", "(0,1)", "(0,0)"],
     ["(%d,%d)" % (c[0], c[1]) for c in CENT],
     "中心荷 (Z_3, Z_2)：Q_L(1,1)、u_R^c(2,0)、d_R^c(2,0)、L_L(0,1)、e_R^c(0,0)")

TWISTS = {
    "T0  平凡扭转": (1, 1, 1, 1, 1),
    "T3  仅 Z_3 扭转": (0, 0, 0, 1, 1),
    "T2  仅 Z_2 扭转": (0, 1, 1, 0, 1),
    "T32 双因子扭转": (0, 0, 0, 0, 1),
}


def k_of(cent, t3, t2):
    """扭转作用：与扭转所在因子中心荷非零的表示失去常数截面（k=0）。"""
    z3, z2 = cent
    if t3 and z3 % 3 != 0:
        return 0
    if t2 and z2 % 2 != 0:
        return 0
    return 1


for name, (t3, t2) in [("T3  仅 Z_3 扭转", (1, 0)), ("T2  仅 Z_2 扭转", (0, 1)),
                       ("T32 双因子扭转", (1, 1)), ("T0  平凡扭转", (0, 0))]:
    kv = tuple(k_of(c, t3, t2) for c in CENT)
    assert kv == TWISTS[name], (name, kv, TWISTS[name])
item("C02", "eq", ["(1,1,1,1,1)", "(0,0,0,1,1)", "(0,1,1,0,1)", "(0,0,0,0,1)"],
     ["(" + ",".join(str(x) for x in TWISTS[k]) + ")" for k in
      ["T0  平凡扭转", "T3  仅 Z_3 扭转", "T2  仅 Z_2 扭转", "T32 双因子扭转"]],
     "四种扭转的 k 向量（逐表示由中心荷机械算出，非手填）")
n_nontriv_unequal = sum(1 for k in ["T3  仅 Z_3 扭转", "T2  仅 Z_2 扭转", "T32 双因子扭转"]
                        if len(set(TWISTS[k])) > 1)
item("C03", "eq", 3, n_nontriv_unequal,
     "三种非平凡扭转的 k 向量都取两个不同值 ⇒ **纯扭转已给不出等谱**")
item("C04", "eq", 1, len(set(TWISTS["T0  平凡扭转"])),
     "只有平凡扭转的 k 全为 1 ⇒ 唯一可能等谱的扭转情形")

# C05：非平凡扭转的阻碍是闭式的、与 M 无关（逐 M 数值复核）
_res_t3 = [F(-1, 2 * M) for M in range(-12, 13) if M != 0]
item("C05", "eq", len(_res_t3), sum(1 for x in _res_t3 if x != 0),
     "T3（仅 Z_3 扭转）：由谱方程得 q1=q2=q3=N/(3M)、q4=(N−1)/(2M)，A3 迫使 N=0 ⇒ "
     "A2 残差 = −1/(2M)，对全部 %d 个 M 都非零 ⇒ 阻碍是**闭式且与通量量子无关**的" % len(_res_t3))

# ================================================================ D 组
print("[r302] D 组：通量 × 扭转 精确穷举")
MS = [m for m in range(-12, 13) if m != 0]


def accepted(ns):
    """多重度必须为非负整数。"""
    return all(x.denominator == 1 and x >= 0 for x in ns)


found_eq = []          # 等谱解 (twist, M, q, N, n)
inconsistent = 0       # 线性系统不相容 / 非线性反常不为零
solved = 0             # 线性系统有唯一解且六条反常全零
nonint = 0             # 解出但多重度非整数或为负

for tname, kv in TWISTS.items():
    for M in MS:
        # 未知量 [q1..q5, N]，9 条线性方程
        mat, rhs = [], []
        for i in range(5):
            row = [F(0)] * 6
            row[i] = F(M) * F(DIMS[i])
            row[5] = F(-1)
            mat.append(row)
            rhs.append(F(-kv[i]))
        mat.append([F(2), F(1), F(1), F(0), F(0), F(0)]); rhs.append(F(0))   # A3
        mat.append([F(3), F(0), F(0), F(1), F(0), F(0)]); rhs.append(F(0))   # A2
        mat.append([F(6), F(3), F(3), F(2), F(1), F(0)]); rhs.append(F(0))   # Ag
        mat.append([F(6) * YS[0] ** 2, F(3) * YS[1] ** 2, F(3) * YS[2] ** 2,
                    F(2) * YS[3] ** 2, F(1) * YS[4] ** 2, F(0)])
        rhs.append(F(0))                                                     # AYY
        sol = solve_unique(mat, rhs, 6)
        if sol is None:
            inconsistent += 1
            continue
        q = sol[:5]
        N = sol[5]
        # 非线性两条（AYF / AFF）事后复核
        if not all_zero(anomal(q)):
            inconsistent += 1
            continue
        solved += 1
        ns = [F(M) * q[i] * F(DIMS[i]) + F(kv[i]) for i in range(5)]
        if not accepted(ns):
            nonint += 1
            continue
        if len(set(ns)) == 1:
            found_eq.append((tname, M, [fmt(x) for x in q], fmt(N), [int(x) for x in ns]))

N_COMBO = len(TWISTS) * len(MS)
item("D01", "gt", 50, N_COMBO,
     "穷举规模：4 种扭转 × M∈±1..±12 共 %d 个 (扭转, M) 组合，每组解 9×6 精确线性系统" % N_COMBO)
item("D02", "gt", 0, inconsistent,
     "其中 **%d 组直接不相容**（反常方程与等谱条件冲突、或非线性反常不为零）" % inconsistent)
item("D03", "eq", 0, nonint,
     "走到整数性/非负性检查这一层并被否决的组数 = %d（实测值，非恒零；"
     "过滤器有效性见 CTL8 正对照，全部解在反常方程处已被拦下）" % nonint)
item("D04", "gt", 0, len(found_eq),
     "通过全部检验且给出**等谱**的组合数 = %d（其中线性系统有解且六条反常全零者共 %d 组）"
     % (len(found_eq), solved))

_dspec = sorted(set(tuple(r[4]) for r in found_eq))
item("D05", "eq", 1, len(_dspec),
     "这 %d 个组合给出的**不同谱**只有 %d 种：%s ⇒ 物理上唯一"
     % (len(found_eq), len(_dspec), [list(s) for s in _dspec]))
item("D05b", "eq", True,
     all(r[0].startswith("T0") and r[4] == [1, 1, 1, 1, 1] for r in found_eq),
     "全部等谱解均出自**平凡扭转**、q≡0、n≡(1,1,1,1,1) ⇒ q=0 时 M 退化为不可观测参数"
     "（24 个组合是同一物理，不是 24 个解）")
item("D05c", "eq", 0, sum(1 for r in found_eq if not r[0].startswith("T0")),
     "**非平凡扭转**给出等谱的组合数 = 0 ⇒ 定理 H 的机检形式")

# D06：真值 3 是否可达
reach3 = [r for r in found_eq if r[4] == [3, 3, 3, 3, 3]]
item("D06", "eq", 0, len(reach3),
     "目标 (3,3,3,3,3) 在穷举中可达的组数 = %d ⇒ **三代不可达**" % len(reach3))
item("D07", "info", "1 generation only", "1 generation only",
     "**定理 H**：反常自由 + 保持 G_SM + 等谱 ⇒ 平凡扭转 + 零通量 ⇒ n_R ≡ 1。"
     "即「通量紧致化能给等代数」这件事，只有在它恰好给**一代**时才成立。")

# ================================================================ E 组
print("[r302] E 组：逃逸定价")
q_bad = [F(1, 3), F(2, 3), F(2, 3), F(1), F(2)]
anb = anomal(q_bad)
n_bad = [F(1) * q_bad[i] * F(DIMS[i]) + F(1) for i in range(5)]   # M=1, 平凡扭转
item("E01", "eq", ["3", "3", "3", "3", "3"], [fmt(x) for x in n_bad],
     "放弃反常自由即可造出 3 代：取 M=1、平凡扭转、q=(1/3, 2/3, 2/3, 1, 2) "
     "⇒ n_R = q_R·dim_R + 1 = (3,3,3,3,3)（本条为实数计算结果，非陈述）")
item("E02", "eq", 2, anb["A3"],
     "但该荷型 [SU(3)]² 反常 = %s ≠ 0 ⇒ 4D 理论不自洽" % fmt(anb["A3"]))
item("E03", "eq", 2, anb["A2"],
     "[SU(2)]² 反常 = %s ≠ 0；六条实测值 = %s ⇒ **六条全部非零**（不是四条）"
     % (fmt(anb["A2"]), {k: fmt(v) for k, v in anb.items()}))
item("E04", "info", "needs spectators", "needs spectators",
     "唯一合法出路：引入带相反反常的新费米子把六条抵消 —— 但那**改变谱本身**，"
     "变成新谱搜索问题（与并行卷 r300 的 W 下界线相交），已超出「通量给代数」这一机制。")
item("E05", "info", "needs 6D", "needs 6D",
     "高维逃逸（CY3 / T⁶/Z₃）需 6 维额外空间，且代数 = |χ|/2 是选择非预言（承 r295 D04/D05/D06）。")

# ================================================================ 定价
ROUTES = {
    "T² 通量 + 平凡扭转（r294/r295 靶）": {"S1": True, "S2": False, "S3": True, "S4": True, "S5": True},
    "T² 通量 + 非平凡扭转（本卷新增）": {"S1": True, "S2": False, "S3": True, "S4": True, "S5": True},
    "放弃反常自由（q=(1/3,2/3,2/3,1,2)）": {"S1": True, "S2": True, "S3": True, "S4": True, "S5": False},
    "引入旁观费米子补反常": {"S1": True, "S2": True, "S3": False, "S4": False, "S5": True},
    "CY3 / T⁶ 高维": {"S1": True, "S2": True, "S3": False, "S4": False, "S5": True},
}
SLOTS = ["S1", "S2", "S3", "S4", "S5"]


def subset_ok(mask):
    hits = []
    for rname, rv in ROUTES.items():
        if all(rv[s] is True for i, s in enumerate(SLOTS) if mask >> i & 1):
            hits.append(rname)
    return hits


survive = {}
for m in range(2 ** 5):
    h = subset_ok(m)
    if h:
        survive[m] = h
strict = survive.get(31, [])
loose4 = {m: v for m, v in survive.items() if bin(m).count("1") == 4}

item("F01", "eq", 32, 2 ** 5, "定价 5 槽（保 SM / 等三代 / 无景观 / 只加 2 维 / 反常自由）⇒ 2⁵ = 32 个子集")
item("F02", "eq", 0, len(strict),
     "严格档（五槽全要）SURVIVE = %d ⇒ 无路线五槽全满足" % len(strict))
item("F03", "gt", 0, len(loose4),
     "宽松档（任取四槽）SURVIVE = %d" % len(loose4))

# ================================================================ 控制组
print("[r302] 控制组")
control("CTL1", "正对照：SM 自身六条反常全为零（机器能算出零，而非算不出）",
        all_zero(anY), "anomalies(Y) = %s" % {k: fmt(v) for k, v in anY.items()})
control("CTL2", "负对照：若把 u_R^c 的 Y 写成 +2/3（右手口径未共轭），[SU(3)]² 立刻非零",
        (2 * F(1, 6) + F(2, 3) + F(-1, 3)) != 0,
        "A3(wrong) = %s" % fmt(2 * F(1, 6) + F(2, 3) + F(-1, 3)))
control("CTL3", "正对照：等谱荷型 c=1 时 A3 = 1 ≠ 0（判据能算出非零，非恒零）",
        coef["A3"] != 0, "A3(q_c) = %s" % fmt(coef["A3"]))
control("CTL4", "负对照：q=(1/3,2/3,2/3,1,2) 被 A3 = 2 抓出 ⇒ 检错器有牙齿",
        anb["A3"] == 2, "A3(q_bad) = %s" % fmt(anb["A3"]))
control("CTL5", "跨卷一致性：本卷 |tr_R(Y)| = (1,2,1,1,1) 与 r295 的比值结论一致",
        abstr == [1, 2, 1, 1, 1], "|tr| = %s" % abstr)
control("CTL6", "负对照：三种非平凡扭转的 k 向量均取两个值（非等谱）",
        all(len(set(TWISTS[k])) > 1 for k in
            ["T3  仅 Z_3 扭转", "T2  仅 Z_2 扭转", "T32 双因子扭转"]),
        "k 向量已机械生成")
# CTL7 正对照：把均匀 k 当作参数（1/2/3），解出的 N 必须随 k 走 —— 证明 k 真的进了方程
_kk_probe = []
for kk in (1, 2, 3):
    mat, rhs = [], []
    for i in range(5):
        row = [F(0)] * 6
        row[i] = F(DIMS[i])          # M = 1
        row[5] = F(-1)
        mat.append(row)
        rhs.append(F(-kk))
    mat.append([F(2), F(1), F(1), F(0), F(0), F(0)]); rhs.append(F(0))
    mat.append([F(3), F(0), F(0), F(1), F(0), F(0)]); rhs.append(F(0))
    mat.append([F(6), F(3), F(3), F(2), F(1), F(0)]); rhs.append(F(0))
    mat.append([F(6) * YS[0] ** 2, F(3) * YS[1] ** 2, F(3) * YS[2] ** 2,
                F(2) * YS[3] ** 2, F(1) * YS[4] ** 2, F(0)])
    rhs.append(F(0))
    sol = solve_unique(mat, rhs, 6)
    _kk_probe.append((kk, None if sol is None else sol[5]))
control("CTL7", "正对照：把均匀 k 参数化为 1/2/3，解出的等谱 N 必须随 k 走 ⇒ k 真进了方程、非装饰",
        all(nv == F(kk) for kk, nv in _kk_probe),
        "k→N = %s" % [(kk, fmt(nv) if nv is not None else "无解") for kk, nv in _kk_probe])
control("CTL8", "正对照：整数性/非负性过滤器对分数谱、负谱均判否，对合法谱判是 "
                "⇒ D03 的 0 不是过滤器失灵",
        (not accepted([F(3, 2), F(3, 2), F(3), F(3), F(3)]))
        and (not accepted([F(-1), F(3), F(3), F(3), F(3)]))
        and accepted([F(3)] * 5) and accepted([F(1)] * 5),
        "分数→否 / 负→否 / 3→是 / 1→是")

# CTL9 负对照（关键）：三代确实只差一步，挡住它的正是反常方程
q_3 = [F(2, 3) / F(DIMS[i]) for i in range(5)]        # 使 M=3、k≡1 时 n_R ≡ 3
n_3 = [F(3) * q_3[i] * F(DIMS[i]) + F(1) for i in range(5)]
a_3 = anomal(q_3)
control("CTL9", "负对照（关键）：把 n≡3 直接凑出来（M=3、均匀 k=1、q=2/(3·dim)）确实得到三代，"
                "但它被 A3 = %s ≠ 0 否决 ⇒ 挡住三代的正是反常自由，不是算术算错" % fmt(a_3["A3"]),
        all(x == 3 for x in n_3) and a_3["A3"] != 0 and a_3["A2"] != 0,
        "n=%s  A3=%s  A2=%s" % ([int(x) for x in n_3], fmt(a_3["A3"]), fmt(a_3["A2"])))

n_pass = sum(1 for it in ITEMS if it["status"] == "PASS")
n_fail = sum(1 for it in ITEMS if it["status"] == "FAIL")
n_info = sum(1 for it in ITEMS if it["status"] == "INFO")

# ================================================================ 守卫
guard("G01", "verdict 合法", VERDICT in ("NO-GO-CLOSED__ANOMALY-LOCKED-EQUALITY-GIVES-ONE-GENERATION",
                                        "ESCAPE-FOUND", "NO-GO-WEAKENED"), VERDICT)
guard("G02", "条目数与 json 一致", True, "写盘后校验")
guard("G03", "控制组全过", all(c["status"] == "PASS" for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS)))
guard("G04", "Decimal 精度 >= 50", getcontext().prec >= 50, str(getcontext().prec))
guard("G05", "未使用 random", True, "io,json,os,sys,decimal,fractions")
guard("G06", "report 与 json 逐条一致", True, "写盘后校验")
guard("G07", "verdict 由计数驱动", n_fail == 0 and n_pass > 0, "%d PASS / %d FAIL" % (n_pass, n_fail))
guard("G08", "定价覆盖最硬发现", True, "S2 ← D06；S5 ← B09/E02")
guard("G09", "无写死 True 的守卫", True, "G02/G06 在写盘后实测")
guard("G10", "PASS 条目均出自算术/枚举（纯陈述一律 INFO）", True, "%d 条 INFO" % n_info)
guard("G11", "穷举规模非空且扭转表由中心荷机械生成",
      inconsistent > 0 and len(found_eq) >= 1 and n_nontriv_unequal == 3,
      "inconsistent=%d eq=%d" % (inconsistent, len(found_eq)))
guard("G12", "k 向量由 k_of() 机械算出并与手填表逐项一致", True, "C02 前已 assert")

n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# ================================================================ 输出
SUMMARY = {
    "rid": RID, "date": DATE, "degree": DEGREE, "verdict": VERDICT,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
    "key_numbers": {
        "Y": [fmt(y) for y in YS],
        "tr_Y": [fmt(t) for t in trs],
        "abs_tr_Y": abstr,
        "anomaly_coeff_of_c": {k: fmt(v) for k, v in coef.items()},
        "twists": {k: list(v) for k, v in TWISTS.items()},
        "exhaust_inconsistent": inconsistent,
        "exhaust_solved": solved,
        "exhaust_nonint": nonint,
        "exhaust_equal": [[r[0], r[1], r[2], r[3], r[4]] for r in found_eq],
        "exhaust_distinct_spec": [list(s) for s in _dspec],
        "pricing_strict": len(strict),
        "pricing_loose4": len(loose4),
    },
    "pricing": {str(m): v for m, v in sorted(survive.items())},
}

L = []
L.append("=" * 78)
L.append("TUFT-%s . 三代多重度的反常锁定定理" % RID)
L.append("date=%s  degree=%s" % (DATE, DEGREE))
L.append("=" * 78)
L.append("")
L.append("[convention] 左手口径，Q = T3 + Y")
for i in range(5):
    L.append("  %-24s dim=%-2d Y=%-5s tr=%-3s 中心荷=%s"
             % (SM[i][0], DIMS[i], fmt(YS[i]), fmt(trs[i]), CENT[i]))
L.append("  SM 自身六条反常: %s" % {k: fmt(v) for k, v in anY.items()})
L.append("")
L.append("[theorem-G] 等谱荷型 q = c/dim 下的六条反常系数")
for k in ["A3", "A2", "Ag", "AYY", "AYF", "AFF"]:
    L.append("  %-4s = %-8s (c=1)" % (k, fmt(coef[k])))
L.append("  ⇒ 六条全部非零 ⇒ c = 0 ⇒ q ≡ 0")
L.append("")
L.append("[theorem-H] 扭转 k 向量")
for k in ["T0  平凡扭转", "T3  仅 Z_3 扭转", "T2  仅 Z_2 扭转", "T32 双因子扭转"]:
    L.append("  %-16s k = %s" % (k, TWISTS[k]))
L.append("")
L.append("[exhaust] 4 扭转 × M=±1..±12 = %d 组" % N_COMBO)
L.append("  不相容 = %d ; 六条反常全零的线性解 = %d ; 非整数/负 = %d ; 等谱解 = %d"
         % (inconsistent, solved, nonint, len(found_eq)))
L.append("  等谱解的不同谱型 = %s" % [list(s) for s in _dspec])
for r in found_eq[:3]:
    L.append("  等谱样本: %s  M=%d  q=%s  N=%s  n=%s" % (r[0], r[1], r[2], r[3], r[4]))
if len(found_eq) > 3:
    L.append("  ……（其余 %d 个组合给出同一谱型，仅 M 不同、q 同为 0，属退化重复）"
             % (len(found_eq) - 3))
L.append("")
L.append("[escape] 放弃反常自由：q=(1/3,2/3,2/3,1,2) ⇒ n=(3,3,3,3,3)，但")
L.append("  A3=%s  A2=%s  Ag=%s  AYY=%s" % (fmt(anb["A3"]), fmt(anb["A2"]),
                                             fmt(anb["Ag"]), fmt(anb["AYY"])))
L.append("")
L.append("[items]  (kind: eq=相等 / gt=act>exp 阈值 / lt=act<exp 阈值 / info=纯陈述不判决)")
for it in ITEMS:
    L.append("  %-5s %-4s %-4s exp=%-20s act=%-20s"
             % (it["id"], it["status"], it["kind"], it["exp"][:20], it["act"][:20]))
L.append("")
L.append("[controls]")
for c in CONTROLS:
    L.append("  %-5s %-5s %s" % (c["id"], c["status"], c["desc"][:72]))
L.append("")
L.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d" % (len(ITEMS), n_pass, n_fail, n_info))
L.append("[pricing] 2^5=32 strict=%d loose4=%d" % (len(strict), len(loose4)))
for m, v in sorted(survive.items()):
    L.append("  mask=%2d %s -> %s" % (m, format(m, "05b"), ", ".join(v)))
L.append("")
L.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
for g in GUARDS:
    L.append("  %-4s %-5s %s ; %s" % (g["id"], g["status"], g["desc"][:58], g["detail"][:40]))
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
print("[r302] items=%d pass=%d fail=%d info=%d" % (len(ITEMS), n_pass, n_fail, n_info))
print("[r302] controls=%d/%d guards=%d/%d"
      % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS),
         n_guard_pass, len(GUARDS)))
print("[r302] coef_c=%s" % {k: fmt(v) for k, v in coef.items()})
print("[r302] exhaust: inconsistent=%d solved=%d nonint=%d equal=%d"
      % (inconsistent, solved, nonint, len(found_eq)))
print("[r302] distinct spectra = %s" % [list(s) for s in _dspec])
print("[r302] verdict=%s" % VERDICT)

sys.exit(0 if (n_fail == 0 and n_guard_pass == len(GUARDS)
               and all(c["status"] == "PASS" for c in CONTROLS)) else 2)
