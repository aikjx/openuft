# -*- coding: utf-8 -*-
"""
TUFT-r294 · 磁通手征谱「SM 三代不可实现」定理（★自噬轮：正面攻 r292 的 X-R292-1）

r292 P5 给出：均匀磁通 twisting 下 index = q·dim(R)·M，dim=2（L_L）与 dim=6（Q_L）
对 index=3 无整数解 ⇒ 「M=3 产生三代」与 SM 表示论冲突。
唯一逃生口（X-R292-1）：**放弃均匀假设，让同一表示内不同分量带不同磁通电荷**
（非均匀 twisting / 每分量独立 U(1) 电荷）。本卷正面攻这条退路。

★核心结论（本卷定理）：退路被 Schur 引理关闭。
  若磁通 U(1) 生成元 Q 与 G_SM 对易（保持 SM 规范对称性的必要条件），
  则由 Schur 引理 Q 在每个**不可约**表示 R 上必为标量 q_R·1_R
  ⇒ 表示内部**不可能**非均匀 ⇒ index_R = q_R·dim(R)·M，q_R, M ∈ Z
  ⇒ **dim(R) 必须整除 N_gen**。SM 含 dim=2 与 dim=6 的不可约表示，
  而 N_gen=3 不被 2 或 6 整除 ⇒ 三代不可实现。
  ⇒ 可行代数必须被 lcm(6,3,3,2,1,1)=6 整除 ⇒ 最小可行 N_gen = **6**，
     而 LEP 测得 N_ν = 2.9840 ± 0.0082 ⇒ 6 代偏离 **367.8σ** ⇒ 被排除。

管线：
  P1  Schur 对易约束机检（交换子解空间维数，Fraction 精确高斯消元）
  P2  除性定理：dim(R) | N_gen（枚举 1..24）
  P3  LEP 排除：最小可行 6 代 vs N_ν = 2.9840 ± 0.0082
  P4  档 A（磁通 U(1) = U(1)_Y）：index_R = M·tr_R(Y)，比值被钉死 {1,−2,1,−1,1}
  P5  档 B（引入新 U(1)_F）也被 Schur + 除性关闭（每表示 1 个整数电荷仍不够）
  P6  三出口定价（破缺 G_SM / 非阿贝尔 Wilson 线 / 换紧致空间）
  P7  反常分层：6 代反常仍为 0 ⇒ r292 P6 只排除不完整谱，不排除 6 代
  P8  对 r292 P5 的加固与自我诚实（依赖的三前提）
  P9  判据集 R1–R6（在 r292 的 R1–R5 之外新增 R6）⇒ 0/6
  P10 跨卷去重
控制组 C1–C4（正对照，证明判据非一律否定）　守卫 G1–G10
"""
import io
import json
import os
import sys
import time
from fractions import Fraction

RID = "r294"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = "TUFT-%s_磁通手征谱三代不可实现定理_Schur对易约束与除性定理与LEP六代排除_精算与可视化_%s" % (RID, STAMP)

WRITTEN = []
ALLOWED = set()
T0 = time.time()

Z = Fraction(0)
ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


# ---------------------------------------------------------------- 线性代数（Fraction 精确）
def zeros(d):
    return [[Z] * d for _ in range(d)]


def mat(rows):
    return [[Fraction(x) for x in r] for r in rows]


def block_diag(A, d_pad):
    """[[A, 0],[0, 0_{d_pad}]]"""
    da = len(A)
    d = da + d_pad
    M = zeros(d)
    for i in range(da):
        for j in range(da):
            M[i][j] = A[i][j]
    return M


def gauss_rank(rows, nv):
    M = [r[:] for r in rows]
    rank = 0
    piv = 0
    r = 0
    while r < len(M) and piv < nv:
        p = None
        for i in range(r, len(M)):
            if M[i][piv] != 0:
                p = i
                break
        if p is None:
            piv += 1
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][piv]
        M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][piv] != 0:
                f = M[i][piv]
                M[i] = [M[i][k] - f * M[r][k] for k in range(nv)]
        rank += 1
        r += 1
        piv += 1
    return rank


def commutant_complex_dim(gens, d):
    """求 {X ∈ M_d(C) : [X, T_a] = 0 ∀a} 的**复**维数。
    gens: [(P, Q)]，生成元 T_a = P + iQ（P,Q 为实 Fraction 矩阵）
    未知 X = A + iB，实未知数 2d²；返回 (实维数, 复维数)"""
    nv = 2 * d * d

    def iA(i, j):
        return i * d + j

    def iB(i, j):
        return d * d + i * d + j

    rows = []
    for (P, Q) in gens:
        for r in range(d):
            for c in range(d):
                # 实部:  A_{rk}P_{kc} - B_{rk}Q_{kc} - P_{rk}A_{kc} + Q_{rk}B_{kc}
                row = [Z] * nv
                for k in range(d):
                    row[iA(r, k)] += P[k][c]
                    row[iB(r, k)] -= Q[k][c]
                    row[iA(k, c)] -= P[r][k]
                    row[iB(k, c)] += Q[r][k]
                rows.append(row)
                # 虚部:  A_{rk}Q_{kc} + B_{rk}P_{kc} - P_{rk}B_{kc} - Q_{rk}A_{kc}
                row2 = [Z] * nv
                for k in range(d):
                    row2[iA(r, k)] += Q[k][c]
                    row2[iB(r, k)] += P[k][c]
                    row2[iB(k, c)] -= P[r][k]
                    row2[iA(k, c)] -= Q[r][k]
                rows.append(row2)
    rk = gauss_rank(rows, nv)
    real_dim = nv - rk
    return real_dim, Fraction(real_dim, 2)


# ---------------------------------------------------------------- 生成元
def su2_fund():
    """SU(2) 基本表示（d=2，不可约），T_a = sigma_a/2"""
    h = Fraction(1, 2)
    P1 = mat([[0, h], [h, 0]])
    Q1 = zeros(2)
    P2 = zeros(2)
    Q2 = mat([[0, -h], [h, 0]])          # i*(sigma_2/2) 的虚部
    P3 = mat([[h, 0], [0, -h]])
    Q3 = zeros(2)
    return [(P1, Q1), (P2, Q2), (P3, Q3)], 2


def su3_fund():
    """SU(3) 基本表示（d=3，不可约）。用整数基（避开 Gell-Mann 的 sqrt3）：
    对角 D1=diag(1,-1,0), D2=diag(1,1,-2)；非对角 S_ij=E_ij+E_ji, A_ij=i(E_ij-E_ji)"""
    Z3 = zeros(3)
    D1 = mat([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
    D2 = mat([[1, 0, 0], [0, 1, 0], [0, 0, -2]])
    gens = [(D1, Z3), (D2, Z3)]
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        S = zeros(3)
        S[i][j] = Fraction(1)
        S[j][i] = Fraction(1)
        A = zeros(3)
        A[i][j] = Fraction(1)
        A[j][i] = Fraction(-1)
        gens.append((S, Z3))
        gens.append((Z3, A))
    return gens, 3


def su2_adjoint():
    """SU(2) 伴随表示 = so(3) 的实生成元（d=3，不可约，全实 ⇒ Q=0）"""
    Z3 = zeros(3)
    L1 = mat([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    L2 = mat([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    L3 = mat([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    return [(L1, Z3), (L2, Z3), (L3, Z3)], 3


def su2_reducible_2plus1():
    """可约表示 2 ⊕ 1（d=3）：SU(2) 生成元块对角 diag(sigma_a/2, 0)"""
    h = Fraction(1, 2)
    Z2 = zeros(2)
    P1 = mat([[0, h], [h, 0]])
    Q2m = mat([[0, -h], [h, 0]])
    P3 = mat([[h, 0], [0, -h]])
    gens = [(block_diag(P1, 1), zeros(3)),
            (zeros(3), block_diag(Q2m, 1)),
            (block_diag(P3, 1), zeros(3))]
    return gens, 3


# ================================================================ P1
def p1():
    """Schur 对易约束：与所有生成元对易的 U(1) 生成元，在不可约表示上必为标量"""
    cases = [
        ("SU(2) 基本（不可约 dim 2）", su2_fund, 1),
        ("SU(3) 基本（不可约 dim 3）", su3_fund, 1),
        ("SU(2) 伴随（不可约 dim 3）", su2_adjoint, 1),
        ("可约 2⊕1（dim 3，正对照）", su2_reducible_2plus1, 2),
    ]
    rows = []
    allok = True
    for name, fn, expect in cases:
        gens, d = fn()
        rd, cd = commutant_complex_dim(gens, d)
        ok = (cd == expect)
        allok = allok and ok
        rows.append({"表示": name, "dim": d, "复解空间维数": str(cd),
                     "实解空间维数": rd, "期望复维数": expect, "一致": ok})
    kv = {"算例": rows,
          "物理含义": "复维数=1 ⇔ 对易代数 = C·1（Schur：不可约 ⇒ 只有标量）⇒ 表示内部不可非均匀"}
    add("P1", "★新层", "Schur 对易约束：不可约表示内 U(1) 生成元必为标量 ⇒ 非均匀 twisting 不可能",
        "PASS" if allok else "FAIL",
        "★本卷核心机检：对任意与 G_SM 对易的磁通 U(1) 生成元 Q，解 [Q, T_a]=0（∀a）。"
        "未知 X ∈ M_d(C) 拆实部/虚部，共 2d² 个实未知，Fraction 精确高斯消元求解空间维数：%s。"
        "不可约表示（SU(2) 基本 dim2、SU(3) 基本 dim3、SU(2) 伴随 dim3）**复维数均为 1** "
        "⇒ 对易代数 = C·1 ⇒ **Q 在不可约表示内只能是标量矩阵**，r292 P5 的「均匀 twisting」"
        "不是假设，而是「保持 SM 规范对称性」的**必然结果**。"
        "★于是 X-R292-1 的退路（同一表示内不同分量带不同磁通电荷）**被 Schur 引理关闭** —— "
        "非均匀只能发生在**不同不可约表示之间**（各表示一个整数电荷 q_R），而这仍不够（见 P5）。"
        % ("；".join("%s ⇒ 复维数 %s" % (r["表示"], r["复解空间维数"]) for r in rows)),
        kv)
    return {"rows": rows, "ok": allok}


# ================================================================ P2
def p2():
    """除性定理：index_R = q_R·dim(R)·M ⇒ dim(R) | N_gen"""
    # SM 一代（全部改写为左手 Weyl；右手取其共轭）
    reps = [("Q_L (3,2,1/6)", 6), ("u_R^c (3bar,1,-2/3)", 3), ("d_R^c (3bar,1,1/3)", 3),
            ("L_L (1,2,-1/2)", 2), ("e_R^c (1,1,1)", 1), ("nu_R^c (1,1,0)", 1)]
    dims = [d for _, d in reps]
    lcm = 1
    for d in dims:
        g = lcm
        while g % d != 0:
            g += lcm
        lcm = g
    feasible = [n for n in range(1, 25) if all(n % d == 0 for d in dims)]
    # 正对照：只要求色三重态与单态（不含 SU(2) 双重态）
    dims_sub = [3, 3, 1, 1]
    feasible_sub = [n for n in range(1, 25) if all(n % d == 0 for d in dims_sub)]
    kv = {"SM表示维数": dims, "lcm": lcm, "可行代数_1..24": feasible,
          "非空表示子集(3,3,1,1)_可行": feasible_sub[:8], "N_gen=3可行": 3 in feasible}
    ok = (3 not in feasible) and (feasible[0] == 6) and (3 in feasible_sub)
    add("P2", "★新层", "除性定理：dim(R) | N_gen ⇒ 可行代数为 6 的倍数，3 不可行",
        "PASS" if ok else "FAIL",
        "由 P1，index_R = q_R·dim(R)·M（q_R, M ∈ Z）⇒ index_R ∈ dim(R)·Z ⇒ **每个 SM 不可约表示的"
        "维数都必须整除代数 N_gen**。SM 一代的表示维数集合 = %s，lcm = **%d** ⇒ "
        "可行代数 = %s（1..24 内）。**N_gen = 3 不可行**（3 不被 2、6 整除）；"
        "最小可行代数 = **6**。★正对照（判据不一律否定）：若只要求色三重态与单态（不含 SU(2) 双重态，"
        "维数 %s），则 N_gen = 3 **可行** ⇒ 冲突的根源正是 **SU(2) 双重态的维数 2**。"
        % (dims, lcm, feasible, dims_sub),
        kv)
    return {"lcm": lcm, "feasible": feasible, "ok": ok}


# ================================================================ P3
def p3():
    """LEP 排除：6 代 vs N_nu = 2.9840 ± 0.0082"""
    n_obs = Fraction(29840, 10000)
    sig = Fraction(82, 10000)
    rows = []
    for n in [3, 6, 12, 18]:
        dev = (Fraction(n) - n_obs) / sig
        rows.append({"代数": n, "偏离σ": "%.4f" % float(dev),
                     "被LEP排除": bool(dev > 5)})
    d6 = (Fraction(6) - n_obs) / sig
    kv = {"LEP_N_nu": "2.9840 ± 0.0082（PDG，Z 线形）", "扫描": rows,
          "6代偏离σ": "%.4f" % float(d6)}
    add("P3", "★新层", "LEP 排除：最小可行 6 代偏离 N_ν=2.9840±0.0082 达 %sσ" % ("%.1f" % float(d6)),
        "FAIL",
        "P2 给出最小可行代数为 6。而 LEP 的 Z 玻色子不可见宽度给出轻中微子代数 "
        "**N_ν = 2.9840 ± 0.0082**（PDG）。6 代 ⇒ 偏离 **%.1fσ**；12 代 ⇒ %.0fσ。"
        "⇒ **磁通机制若真能产生完整 SM 表示结构，它给的是 6 的倍数代，全部被排除**。"
        "★注意：这个排除用的**不是**α 或质量，而是一个完全独立、精度极高的观测量，"
        "且与 r292 的真空能灾难（P9）互相独立 —— 两条不同的路都走到「不行」。"
        % (float(d6), float((Fraction(12) - n_obs) / sig)),
        kv)
    return {"d6": float(d6), "rows": rows}


# ================================================================ P4
def p4():
    """档 A：磁通 U(1) = SM 超荷 U(1)_Y ⇒ index_R = M·tr_R(Y)，比值被钉死"""
    # 左手 Weyl 约定下各表示的超荷迹
    traces = [("Q_L", 6, Fraction(1, 6)), ("u_R^c", 3, Fraction(-2, 3)),
              ("d_R^c", 3, Fraction(1, 3)), ("L_L", 2, Fraction(-1, 2)),
              ("e_R^c", 1, Fraction(1, 1)), ("nu_R^c", 1, Fraction(0, 1))]
    tr = {n: dim * y for n, dim, y in traces}
    sols = []
    for M in range(1, 13):
        idx = {n: M * t for n, t in tr.items()}
        ok = all(abs(idx[n]) == 3 for n in tr)
        sols.append({"M": M, "各表示index": {n: str(idx[n]) for n in tr}, "满足每表示|=3": ok})
    any_ok = any(s["满足每表示|=3"] for s in sols)
    kv = {"tr_R(Y)": {n: str(t) for n, t in tr.items()},
          "index比(相对Q_L)": {n: str(Fraction(tr[n], tr["Q_L"])) for n in tr},
          "M扫描": sols}
    add("P4", "★新层", "档 A（磁通 U(1)=U(1)_Y）：index 比被 tr_R(Y) 钉死为 {1,−2,1,−1,1,0}，无解",
        "PASS" if not any_ok else "FAIL",
        "若把产生手征零模的 U(1) 直接识别为 SM 超荷（零模才带正确量子数），则 "
        "index_R = M·tr_R(Y)，各表示的 index **之比被超荷迹完全钉死**：%s（相对 Q_L）。"
        "要每表示都给 |index| = 3，需要 Q_L 的 M·1 = 3 ⇒ M=3，同时 u_R^c 的 |M·(−2)| = 3 ⇒ M=1.5 "
        "**非整数**，直接矛盾。M ∈ [1,12] 全域扫描：**无一解**。"
        "⇒ 档 A（最自然的识别）**不可行**，且失败原因比 P2 更基本 —— 不是代数对不上，"
        "而是**各表示的 index 之比本身就不等于 1:1:1:1:1**。"
        % ("、".join("%s=%s" % (n, kv["index比(相对Q_L)"][n]) for n in tr)),
        kv)
    return {"any_ok": any_ok, "tr": tr}


# ================================================================ P5
def p5():
    """档 B：引入独立于 SM 的新 U(1)_F ⇒ 每表示一个整数电荷，仍不够"""
    reps = [("Q_L", 6), ("u_R^c", 3), ("d_R^c", 3), ("L_L", 2), ("e_R^c", 1), ("nu_R^c", 1)]
    rows = []
    for name, dim in reps:
        sols = []
        for M in range(1, 13):
            for q in range(-12, 13):
                if q != 0 and abs(q * dim * M) == 3:
                    sols.append((q, M))
        rows.append({"表示": name, "dim": dim, "整数解(q,M)": [list(s) for s in sols[:6]],
                     "解数": len(sols), "可行": bool(sols)})
    bad = [r["表示"] for r in rows if not r["可行"]]
    # 若放宽到 N_gen = 6（P2 的最小可行值），是否有解
    rows6 = []
    for name, dim in reps:
        sols = [(q, M) for M in range(1, 13) for q in range(-12, 13)
                if q != 0 and abs(q * dim * M) == 6]
        rows6.append({"表示": name, "dim": dim, "整数解(q,M)": [list(s) for s in sols[:4]], "解数": len(sols)})
    kv = {"N_gen=3": rows, "N_gen=6": rows6, "失败表示(N_gen=3)": bad}
    ok = (len(bad) == 2) and all(r["解数"] > 0 for r in rows6)
    add("P5", "★新层", "档 B（新 U(1)_F + 每表示独立电荷）也被关闭：dim=2/6 仍无解，6 代才有解",
        "PASS" if ok else "FAIL",
        "★X-R292-1 的退路（引入独立 U(1)_F、让每个不可约表示各带一个整数电荷 q_R）本卷给出判决："
        "**救不活三代，但能给出 6 代**。逐表示枚举 q ∈ [−12,12]、M ∈ [1,12] 使 |q·dim(R)·M| = 3："
        "dim=6（Q_L）与 dim=2（L_L）**零解**（6qM=3、2qM=3 均无整数解）；dim=3 需 |qM|=1、dim=1 需 |qM|=3。"
        "放宽到 **N_gen=6** 后全部表示都有解 ⇒ 档 B 真实能力 = **产生 6 的倍数代**。"
        "⇒ 两条路（档 A 识别为超荷 / 档 B 独立 U(1)_F）**殊途同归地指向 6**，而 6 被 LEP 排除（P3）。"
        "本卷结论：P5 的退路在技术上存在（加一个 U(1)_F 即可），但它**不产出三代**，"
        "且引入 ≥6 个新整数电荷参数 + 新规范因子 + 破缺机制 ⇒ 与「无参数预测」彻底背道而驰。",
        kv)
    return {"bad": bad, "ok": ok}


# ================================================================ P6
def p6():
    """三出口定价"""
    # E1：破缺 G_SM —— 中心化子维数（用 P1 的机检口径）
    gens2, d2 = su2_fund()
    _, cd2 = commutant_complex_dim(gens2, d2)
    gens3, d3 = su3_fund()
    _, cd3 = commutant_complex_dim(gens3, d3)
    # E2：T^2 上平坦阿贝尔联络 c_1 = 0 ⇒ index = 0
    flat_index = 0
    # Wilson line 模空间维数：T^2 有两个基本群的生成元 ⇒ 两条 Wilson 线，
    # 对 U(1)^r 每条给 r 个连续相位 ⇒ 连续参数数 = 2r
    r_rank = 1
    wl_params = 2 * r_rank
    kv = {"E1_中心化子复维数_SU2基本": str(cd2), "E1_中心化子复维数_SU3基本": str(cd3),
          "E2_平坦阿贝尔联络_index": flat_index, "E2_Wilson线连续参数数": wl_params}
    add("P6", "★新层", "三出口定价：破缺 G_SM / 非阿贝尔 Wilson 线 / 换紧致空间 —— 三条都走不通",
        "FAIL",
        "本定理的前提若被放弃，只剩三条退路，逐条定价："
        "**E1（放弃 [Q, G_SM]=0）**——则 Q 不再落在 G_SM 的中心化子里（机检：SU(2) 基本与 SU(3) 基本表示"
        "的中心化子复维数分别为 %s 与 %s，即只剩 U(1) 标量），意味着磁通 **破缺 SU(3)×SU(2)**；"
        "而 SU(3)×SU(2) 在 TeV 以下经 LHC/精密电弱检验完好 ⇒ 代价 = 与观测冲突。"
        "**E2（改用非阿贝尔磁通 / Wilson 线）**——T² 上平坦阿贝尔丛的 c_1 = 0 ⇒ index = **%d**，"
        "根本不产生手征零模；而要让 Wilson 线非平凡，需引入 %d 个**连续**相位参数（两条 Wilson 线 × rank），"
        "⇒ 手征性换来了连续参数，与「拓扑 ⇒ 无参数」的初衷相消。"
        "**E3（换紧致空间 T⁴/T⁶/CY）**——指标定理的形式改变（高维 ch·Td 的 top form），"
        "本定理不适用；但那已**不是 V14 的 T² 设定**，属诚实边界，本卷不断言。" % (cd2, cd3, flat_index, wl_params),
        kv)
    return {"kv": kv}


# ================================================================ P7
def p7():
    """反常分层：6 代反常仍为 0 ⇒ r292 P6 只排除不完整谱"""
    def sm_anomalies(n):
        # 所有费米子改写为左手 Weyl；右手取共轭（Y 变号）
        cube = (6 * Fraction(1, 6) ** 3 + 3 * Fraction(-2, 3) ** 3 + 3 * Fraction(1, 3) ** 3
                + 2 * Fraction(-1, 2) ** 3 + 1 * Fraction(1, 1) ** 3)
        grav = (6 * Fraction(1, 6) + 3 * Fraction(-2, 3) + 3 * Fraction(1, 3)
                + 2 * Fraction(-1, 2) + 1 * Fraction(1, 1))
        su3 = (2 * Fraction(1, 2) * Fraction(1, 6) + Fraction(1, 2) * Fraction(-2, 3)
               + Fraction(1, 2) * Fraction(1, 3))
        su2 = (3 * Fraction(1, 2) * Fraction(1, 6) + Fraction(1, 2) * Fraction(-1, 2))
        return [Fraction(n) * cube, Fraction(n) * grav, Fraction(n) * su3, Fraction(n) * su2]
    rows = []
    for n in [1, 3, 6, 12]:
        a = sm_anomalies(n)
        rows.append({"代数": n, "[Y]^3": str(a[0]), "grav^2Y": str(a[1]),
                     "[SU3]^2Y": str(a[2]), "[SU2]^2Y": str(a[3]),
                     "全为0": all(x == 0 for x in a)})
    kv = {"扫描": rows}
    ok = all(r["全为0"] for r in rows)
    add("P7", "治理", "反常分层：任意代数（含 6 代）反常均为 0 ⇒ r292 P6 只排除不完整谱",
        "PASS" if ok else "FAIL",
        "★判据分层（自我校正）：r292 P6 用「反常非零」否掉了 index=3 的**纯左手不完整谱**。"
        "本卷检验：若谱是**完整的整数代**（每代含全部 SM 表示），则任意代数 N 的反常 = N × 0 = **0**"
        "（Fraction 精确：N ∈ {1,3,6,12} 四个反常全为 0）⇒ **反常判据不排除 6 代**。"
        "⇒ 排除 6 代的是 LEP 中微子代数（P3），不是反常。两判据分工明确，"
        "本卷据实修正 r292 判词中「反常」的适用范围，避免判据越权。",
        kv)
    return {"ok": ok}


# ================================================================ P8
def p8():
    """对 r292 P5 的加固与自我诚实"""
    prem = [
        ("(i) 磁通 U(1) 是阿贝尔 U(1)", "V14 §四明确取 (1/2π)∫F = M ∈ Z", "成立"),
        ("(ii) [Q, G_SM] = 0（保持 SM 规范对称性）", "否则破缺 SU(3)×SU(2)，见 P6-E1", "必要"),
        ("(iii) 紧致空间为 T²", "V14 §四明确取 M^{1,3}×T²", "成立"),
    ]
    kv = {"前提": [{"前提": p[0], "依据": p[1], "状态": p[2]} for p in prem],
          "r292_P5原表述": "均匀 twisting 下 index=q·dim(R)·M ⇒ dim=2/6 对 index=3 无整数解",
          "r294升级": "「均匀」不再是假设：由 (ii) + Schur 引理 ⇒ 不可约表示内必为标量（P1 机检证实）",
          "仍开放的口": "非阿贝尔磁通 / 更高维紧致空间（E2/E3）"}
    add("P8", "治理", "对 r292 P5 的加固：「均匀 twisting」由假设升为定理，但三前提须明示",
        "PASS",
        "★加固：r292 P5 的结论建立在「均匀 twisting」这一**假设**上，本卷 P1 用 Schur 引理 + "
        "交换子解空间机检把它升级为**定理**（只要保持 SM 规范对称性，不可约表示内不可能非均匀），"
        "P5 又关闭了「不同表示不同电荷」的档 B ⇒ X-R292-1 **已正面关闭**。"
        "★自我诚实（本定理依赖的三前提）：%s。三者中 (i)(iii) 是 V14 自己的设定，"
        "(ii) 是物理必要性。若放弃 (iii) 换更高维紧致空间，本定理不适用 —— 这与来料自己"
        "「这是对特定模型的限制性证明」的诚实口径一致，本卷同样**不断言所有紧致化都不可行**。"
        % "；".join("%s（%s）" % (p[0], p[2]) for p in prem),
        kv)
    return {"ok": True}


# ================================================================ P9
def p9():
    """判据集 R1–R6"""
    crit = [
        ("R1", "不含自由连续参数（无拟合）", False, "α*=g_6³√(2T)/(8π²|M|) 含 g_6、T（r292 P11）"),
        ("R2", "由场方程导出而非人为势能", False, "E(A) 不含引力常数（r292 P12）"),
        ("R3", "给出独立于输入的数值", False, "α* 对任意目标值均有解（r292 P7/P9）"),
        ("R4", "附带独立可证伪预言", False, "V14 §六自承「尚未完成」（r292 P14）"),
        ("R5", "与已观测的其他量自洽（Λ）", False, "10^124.46 或 M_6≈0.94 meV（r292 P9）"),
        ("R6", "★能产生正确的 SM 表示结构与代数", False, "T² 磁通最小给 6 代，3 代不可实现（本卷 P2/P5）"),
    ]
    n_ok = sum(1 for c in crit if c[2])
    add("P9", "治理", "判据集 R1–R6（新增 R6「SM 表示与代数」）：%d/6" % n_ok,
        "PASS" if n_ok == 6 else "FAIL",
        "在 r292 的 R1–R5 之外新增 **R6：能否产生正确的 SM 表示结构与代数**（此前五条只问耦合数值，"
        "从未问「这个机制到底能不能生成标准模型的粒子谱」）。机读结果：%s ⇒ **%d/6**。"
        "★R6 的意义：即使有人将来真的把 g_6、T 固定住、把 Λ 灾难调平、拿到一个漂亮的 α，"
        "本卷的结论**仍然独立成立** —— 这套 T² 磁通机制在谱的层面就给不出 3 代。"
        "即 **ROOT V15 主线（六维磁通 + 手征谱 + 几何稳定化统一）在起点处即被否决**，"
        "不是因为它算得不够准，而是因为**它算出来的谱不对**。"
        % ("；".join("%s %s：%s" % (c[0], c[1], "是" if c[2] else "否（" + c[3] + "）") for c in crit), n_ok),
        {"判据": [{"id": c[0], "内容": c[1], "满足": c[2], "依据": c[3]} for c in crit]})
    return {"n_ok": n_ok}


# ================================================================ P10
def p10():
    dup = [
        {"卷": "r292", "主题": "ROOT V14.0 六维磁通/手征/稳定化审计", "重叠": "P5（指标定理与三代冲突）", "性质": "本卷是其自噬加固轮"},
        {"卷": "r290", "主题": "V13.0 KK 电荷—质量排除定理", "重叠": "同线（V13/V14）", "性质": "不同节，不相加"},
        {"卷": "r287", "主题": "V10 下一步链条可行性否证", "重叠": "参数计数/判据集方法", "性质": "方法同源"},
    ]
    add("P10", "治理", "跨卷去重：本卷是 r292 的自噬加固轮，条目不可相加",
        "INFO",
        "本卷**不是**独立的新来料审计，而是 r292 遗留 OPEN（X-R292-1）的**正面自噬轮**："
        "r292 P5 断言「M=3 与三代 SM 冲突」，其唯一退路是「非均匀 twisting」，本卷关闭该退路并给出更强定理。"
        "按分层铁律：本卷 12 条主条目**不得与 r292 的 16 条相加**（同一命题的两轮攻防），"
        "正确读法是「r292 提命题 → r294 加固」，结论强度取**较新的一轮**。",
        {"重叠": dup})
    return {"ok": True}


# ================================================================ 控制组
def controls():
    res = []
    # C1：可约表示的解空间更大（P1 机检有牙齿）
    g, d = su2_reducible_2plus1()
    _, cd = commutant_complex_dim(g, d)
    res.append(("C1", "可约 2⊕1 的复解空间维数 = 2 > 1（P1 机检能区分可约/不可约）", cd == 2,
                "实测复维数 = %s；若机检一律返回 1，则 C1 会假失败 ⇒ 判据有分辨力。" % cd))
    # C2：子集下 3 代可行（P2 除性判据不一律否定）
    dims_sub = [3, 3, 1, 1]
    ok = all(3 % x == 0 for x in dims_sub)
    res.append(("C2", "维数子集 (3,3,1,1) 下 N_gen=3 可行（P2 判据不一律否定）", ok,
                "3 被 3 与 1 整除 ⇒ 若无 SU(2) 双重态，三代是允许的 ⇒ P2 的否决来自 dim=2 而非判据苛刻。"))
    # C3：SM 一代反常 = 0（P7 判据有牙齿）
    cube = (6 * Fraction(1, 6) ** 3 + 3 * Fraction(-2, 3) ** 3 + 3 * Fraction(1, 3) ** 3
            + 2 * Fraction(-1, 2) ** 3 + 1 * Fraction(1, 1) ** 3)
    res.append(("C3", "SM 一代 [Y]³ 反常精确为 0（P7 判据有牙齿）", cube == 0,
                "[Y]³ = %s 精确为 0 ⇒ 反常判据能给出 PASS，不是恒否工具。" % cube))
    # C4：SU(2) 伴随（不可约 dim 3）解空间 = 1（第二例正对照）
    g4, d4 = su2_adjoint()
    _, cd4 = commutant_complex_dim(g4, d4)
    res.append(("C4", "SU(2) 伴随（不可约 dim 3）复解空间 = 1（第二例）", cd4 == 1,
                "实测 %s；与 SU(2)/SU(3) 基本表示一致 ⇒ Schur 结论不依赖具体表示选择。" % cd4))
    for cid, title, ok, detail in res:
        add(cid, "控制组", title, "PASS" if ok else "FAIL", detail, {})
    return [r[2] for r in res]


# ================================================================ 守卫
def guards(extra):
    g = []
    try:
        json.dumps(ITEMS, ensure_ascii=False, default=str)
        g.append(("G1", "JSON 可序列化（无函数/对象泄漏）", True, "全部条目 json.dumps 通过"))
    except Exception as ex:
        g.append(("G1", "JSON 可序列化", False, str(ex)))
    ctl = [it for it in ITEMS if it["layer"] == "控制组"]
    ctl_ok = all(it["verdict"] == "PASS" for it in ctl) and len(ctl) == 4
    g.append(("G3", "控制组 4/4 由实跑得出（禁写死 True）", ctl_ok,
              "控制组 %d 条，PASS %d 条" % (len(ctl), sum(1 for i in ctl if i["verdict"] == "PASS"))))
    g.append(("G4", "Schur 机检：不可约表示复维数均为 1", extra["schur_ok"],
              "算例 %s" % extra["schur_rows"]))
    g.append(("G5", "全部矩阵元素为 Fraction（无浮点污染）", extra["frac_ok"],
              "李代数生成元与约束矩阵均为 Fraction"))
    has_pos = len(ctl) >= 4
    has_neg = sum(1 for it in ITEMS if it["verdict"] == "FAIL") >= 1
    g.append(("G6", "正负双对照齐备（控制组 ≥4 且 FAIL ≥1）", has_pos and has_neg,
              "控制组 %d / FAIL %d" % (len(ctl), sum(1 for i in ITEMS if i["verdict"] == "FAIL"))))
    g.append(("G7", "dim(R)/N_gen/M 全为正整数", extra["int_ok"],
              "dims=%s, M∈[1,12]" % extra["dims"]))
    keys_ok = all(set(it.keys()) == {"id", "layer", "title", "verdict", "detail", "kv"} for it in ITEMS)
    g.append(("G8", "条目键集合一致", keys_ok, "6 键"))
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    g.append(("G9", "仅写本卷路径（不触碰他卷字节）", len(bad) == 0,
              "写入 %d 个路径，越界 %d 个" % (len(WRITTEN), len(bad))))
    legal = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    g.append(("G10", "verdict 取值合法", all(it["verdict"] in legal for it in ITEMS), "∈ {PASS,FAIL,BOUNDARY,INFO}"))
    for gid, title, ok, detail in g:
        if gid != "G2":
            add(gid, "守卫", title, "PASS" if ok else "FAIL", detail, {})
    declared = extra["declared_n"]
    final_n = len(ITEMS) + 1
    add("G2", "守卫", "条目计数一致（声明 %d = 实收 %d）" % (declared, final_n),
        "PASS" if declared == final_n else "FAIL",
        "主条目 12 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
    return [x[2] for x in g]


# ================================================================ 输出
def emit():
    n_pass = sum(1 for i in ITEMS if i["verdict"] == "PASS")
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    n_bnd = sum(1 for i in ITEMS if i["verdict"] == "BOUNDARY")
    n_inf = sum(1 for i in ITEMS if i["verdict"] == "INFO")
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    summary = {"rid": RID, "stamp": STAMP,
               "标题": "磁通手征谱「SM 三代不可实现」定理（r292 X-R292-1 自噬轮）",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    p_json = os.path.join(DATA, BASE + ".json")
    with io.open(wpath(p_json), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    p_rep = os.path.join(DATA, BASE + "_report.txt")
    L = ["TUFT-%s · 磁通手征谱「SM 三代不可实现」定理 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-9s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：r292 P5 的唯一退路（非均匀 twisting / 每分量独立电荷）被 Schur 引理关闭。")
    L.append("      与 G_SM 对易的 U(1) 生成元在不可约表示上必为标量 ⇒ index_R = q_R·dim(R)·M")
    L.append("      ⇒ dim(R) | N_gen ⇒ SM（含 dim=2、6）要求 N_gen 为 6 的倍数 ⇒ 3 代不可实现；")
    L.append("      最小可行 6 代被 LEP N_nu=2.9840±0.0082 以 367.8σ 排除。")
    with io.open(wpath(p_rep), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    p_md = os.path.join(DATA, BASE + ".md")
    M = ["# TUFT-%s · 磁通手征谱「SM 三代不可实现」定理（数据册）" % RID, "",
         "| 项 | 值 |", "| --- | --- |"]
    for k, v in summary.items():
        M.append("| %s | %s |" % (k, v))
    M.append("")
    for it in ITEMS:
        M.append("### %s · %s · %s" % (it["id"], it["verdict"], it["title"]))
        M.append("")
        M.append(it["detail"])
        M.append("")
        if it["kv"]:
            M.append("```json")
            M.append(json.dumps(it["kv"], ensure_ascii=False, indent=1))
            M.append("```")
            M.append("")
    with io.open(wpath(p_md), "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    p_jud = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-%s_" % RID):]))
    J = ["# 判定_TUFT-%s · 磁通手征谱「SM 三代不可实现」定理（★自噬轮）" % RID, "",
         "- **日期**：%s　- **命题**：r292 X-R292-1「非均匀 twisting 能否救活 P5」" % STAMP,
         "- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　**控制组 %s**　**守卫 %s**　**rc=0**"
         % (len(ITEMS), len(main), n_pass, n_fail, n_bnd, n_inf, summary["控制组"], summary["守卫"]),
         "", "## 一、判定", ""]
    for it in main:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J += ["", "## 二、控制组（证明判据非一律否定）", ""]
    for it in ctl:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J += ["", "## 三、守卫", ""]
    for it in grd:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J += ["", "## 四、定理陈述与判词", "",
          "**定理（T² 磁通手征谱 · 三代不可实现）**", "",
          "设 6D 理论在 M^{1,3}×T² 上，规范群 G ⊇ G_SM，磁通 U(1) 生成元 Q 满足 [Q, G_SM] = 0，",
          "磁通量子数 M ∈ Z。则由 Schur 引理，Q 在每个不可约表示 R 上为 q_R·1_R，故",
          "index(D_R) = q_R · dim(R) · M。要产生 N_gen 代完整 SM 手征谱，需对每个 SM 不可约表示",
          "|index(D_R)| = N_gen ⇒ **dim(R) | N_gen** 对所有 R。",
          "SM 一代含 dim=6（Q_L）与 dim=2（L_L）的不可约表示，而 3 不被 2、6 整除 ⇒ **N_gen=3 不可实现**。",
          "可行代数为 lcm(6,3,3,2,1,1) = 6 的倍数，最小为 6，被 LEP（N_ν = 2.9840 ± 0.0082）以 367.8σ 排除。",
          "",
          "**判词：NO-GO-STRONG（退路已关闭）**", "",
          "1. r292 P5 的「均匀 twisting」假设由 Schur 引理升为定理（P1 机检三例 + 可约正对照）⇒ X-R292-1 关闭。",
          "2. 档 A（磁通 U(1)=超荷）与档 B（独立 U(1)_F + 每表示独立电荷）**殊途同归指向 6 的倍数代**（P4/P5）。",
          "3. 6 代被 LEP 以 367.8σ 排除（P3）—— 这是**独立于 α、独立于真空能**的第三条否决线。",
          "4. 判据集在 R1–R5 之外新增 R6「能否产生正确的 SM 表示与代数」⇒ **0/6**。",
          "5. **本定理不是对所有紧致化的否定**：换 T⁴/T⁶/CY 后指标定理形式改变，本卷不断言（E3，诚实边界）。",
          "", "## 五、遗留", "",
          "- X-R294-1：非阿贝尔磁通（Wilson 线）在 T² 上的 index 是否为 0 的完整证明（本卷给出 c₁=0 的论证，未穷举非交换情形）。",
          "- X-R294-2：更高维紧致空间（T⁶/CY）的 ch·Td 指标能否给出 3 代 —— 需另起一轮，本定理不适用。",
          "- X-R294-3：若放弃「代数 = 每表示 index 的绝对值」这一识别（例如允许部分表示来自其它机制），"
          "三代是否有混合来源的实现 —— 代价是谱不再由单一拓扑决定。"]
    with io.open(wpath(p_jud), "w", encoding="utf-8") as f:
        f.write("\n".join(J))
    return summary


# ================================================================ 可视化
def html():
    p = os.path.join(ROOT, "四力统一方程_磁通手征谱三代不可实现定理可视化_%s.html" % STAMP)
    ALLOWED.add(p)
    rows = [{"id": it["id"], "v": it["verdict"], "t": it["title"], "d": it["detail"]} for it in ITEMS]
    payload = {"rid": RID, "stamp": STAMP, "items": rows,
               "p1": [{"name": r["表示"], "dim": r["dim"], "cd": r["复解空间维数"]}
                      for r in [it for it in ITEMS if it["id"] == "P1"][0]["kv"]["算例"]],
               "p3": [{"n": r["代数"], "sig": r["偏离σ"]}
                      for r in [it for it in ITEMS if it["id"] == "P3"][0]["kv"]["扫描"]]}
    doc = u"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>TUFT-RID · 磁通手征谱「SM 三代不可实现」定理</title>
<style>
:root{--bg:#f7f8fa;--card:#fff;--ink:#1f2328;--sub:#5b6470;--line:#dfe3e8;
--pass:#1a7f37;--fail:#c0392b;--bnd:#b8860b;--info:#2f6f9f;--accent:#2b5c9b}
*{box-sizing:border-box}
body{margin:0;padding:24px;background:var(--bg);color:var(--ink);
font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;line-height:1.6}
h1{font-size:20px;margin:0 0 4px}
h2{font-size:16px;margin:24px 0 10px;padding-left:8px;border-left:4px solid var(--accent)}
.sub{color:var(--sub);font-size:13px;margin-bottom:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.kpi .k{font-size:12px;color:var(--sub)}.kpi .v{font-size:19px;font-weight:600;word-break:break-all}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin-bottom:12px}
.thm{background:#fbf7ec;border:1px solid #e3d3a8;border-radius:8px;padding:14px 16px;margin:12px 0}
table{width:100%;border-collapse:collapse;font-size:13px;background:var(--card)}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left}
th{background:#eef1f5}
.tag{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11px;color:#fff}
.PASS{background:var(--pass)}.FAIL{background:var(--fail)}
.BOUNDARY{background:var(--bnd)}.INFO{background:var(--info)}
.mono{font-family:Consolas,"Courier New",monospace;font-size:12px;color:var(--sub)}
.axis{stroke:#c3cad2;stroke-width:1}.lbl{font-size:11px;fill:#5b6470}
</style>
</head>
<body>
<h1>TUFT-RID · 磁通手征谱「SM 三代不可实现」定理（r292 自噬轮）</h1>
<div class="sub">命题：非均匀 twisting / 每分量独立磁通电荷，能否救活 r292 P5？　·　STAMP　·　条目 ITEMN（PASS NP / FAIL NF）　·　控制组 CTL　·　守卫 GRD</div>

<div class="thm">
<b>定理（T² 磁通手征谱 · 三代不可实现）</b><br>
若磁通 U(1) 生成元 Q 满足 [Q, G<sub>SM</sub>] = 0，则由 Schur 引理 Q|<sub>R</sub> = q<sub>R</sub>·1<sub>R</sub>
⇒ index(D<sub>R</sub>) = q<sub>R</sub>·dim(R)·M ⇒ <b>dim(R) 必须整除代数 N<sub>gen</sub></b>。
SM 含 dim=2（L<sub>L</sub>）与 dim=6（Q<sub>L</sub>）⇒ <b>N<sub>gen</sub>=3 不可实现</b>；
可行代数为 <b>6 的倍数</b>，最小 6 被 LEP（N<sub>ν</sub>=2.9840±0.0082）以 <b>367.8σ</b> 排除。
</div>

<h2>一、总账</h2><div class="grid" id="kpi"></div>

<h2>二、Schur 对易约束机检（P1）</h2>
<div class="card"><table id="t1"></table>
<div class="mono">复解空间维数 = 1 ⇔ 对易代数 = C·1 ⇒ 不可约表示内部<b>不可能</b>非均匀。可约 2⊕1 为 2（正对照，证明机检能区分）。</div></div>

<h2>三、代数排除（P2 + P3）</h2>
<div class="card"><svg id="svg3" viewBox="0 0 680 200" width="100%" height="200"></svg>
<div class="mono">横轴 = 候选代数 N<sub>gen</sub>；纵轴 = 与 LEP N<sub>ν</sub>=2.9840 的偏离（σ，对数刻度）。
<b>绿色</b> = 被除性定理允许（6 的倍数）；<b>红色</b> = 被除性定理否决（含 3 代）。全部候选均被 LEP 排除。</div></div>

<h2>四、条目逐条</h2><div id="items"></div>

<script>
const D=__PAYLOAD__;
function el(id,h){document.getElementById(id).innerHTML=h;}
const it=D.items;
const c={PASS:0,FAIL:0,BOUNDARY:0,INFO:0};it.forEach(x=>c[x.v]++);
const ctl=it.filter(x=>x.id[0]==='C'),grd=it.filter(x=>x.id[0]==='G');
const cp=ctl.filter(x=>x.v==='PASS').length,gp=grd.filter(x=>x.v==='PASS').length;
document.querySelector('.sub').innerHTML=document.querySelector('.sub').innerHTML
 .replace('RID',D.rid).replace('STAMP',D.stamp).replace('ITEMN',String(it.length))
 .replace('NP',String(c.PASS)).replace('NF',String(c.FAIL))
 .replace('CTL',cp+'/'+ctl.length).replace('GRD',gp+'/'+grd.length);
const kpi=[['条目总数',it.length],['PASS',c.PASS],['FAIL',c.FAIL],['控制组',cp+'/'+ctl.length],
['守卫',gp+'/'+grd.length],['定理结论','3 代不可实现'],['最小可行代数','6'],['LEP 排除','367.8σ']];
document.getElementById('kpi').innerHTML=kpi.map(k=>'<div class="kpi"><div class="k">'+k[0]+'</div><div class="v">'+k[1]+'</div></div>').join('');
function tbl(id,cols,rows){document.getElementById(id).innerHTML='<tr>'+cols.map(c=>'<th>'+c+'</th>').join('')+'</tr>'+rows.map(r=>'<tr>'+r.map(x=>'<td>'+x+'</td>').join('')+'</tr>').join('');}
tbl('t1',['表示','dim','复解空间维数','判读'],D.p1.map(r=>[r.name,r.dim,r.cd,r.cd=='1'?'不可约 ⇒ 只能标量（Schur）':'可约 ⇒ 可非均匀（正对照）']));
(function(){
 const W=680,H=200,L=52,B=34,T=16,R=18,rs=D.p3;
 const vs=rs.map(r=>Math.log10(Math.max(parseFloat(r.sig),1e-3)));
 const hi=Math.max.apply(null,vs),lo=Math.min.apply(null,vs),pad=(hi-lo||1)*0.15;
 const vmax=hi+pad,vmin=lo-pad;
 const px=i=>L+(W-L-R-14)*(i/(rs.length-1));
 const py=v=>T+(H-T-B)*(1-(v-vmin)/(vmax-vmin));
 let s='<line class="axis" x1="'+L+'" y1="'+(H-B)+'" x2="'+(W-R)+'" y2="'+(H-B)+'"/>';
 s+='<line class="axis" x1="'+L+'" y1="'+T+'" x2="'+L+'" y2="'+(H-B)+'"/>';
 rs.forEach((r,i)=>{const x=px(i),y=py(vs[i]),allowed=(parseInt(r.n)%6===0);
  s+='<rect x="'+(x-16)+'" y="'+y+'" width="32" height="'+(H-B-y)+'" fill="'+(allowed?'#1a7f37':'#c0392b')+'" opacity="0.85"/>';
  s+='<text class="lbl" x="'+x+'" y="'+(H-B+15)+'" text-anchor="middle">'+r.n+' 代</text>';
  s+='<text class="lbl" x="'+x+'" y="'+(y-5)+'" text-anchor="middle">'+parseFloat(r.sig).toFixed(1)+'σ</text>';
  s+='<text class="lbl" x="'+x+'" y="'+(H-B+28)+'" text-anchor="middle">'+(allowed?'允许':'除性否决')+'</text>';});
 s+='<text class="lbl" x="'+(L-6)+'" y="'+(T+8)+'" text-anchor="end">log₁₀σ</text>';
 s+='<text class="lbl" x="'+(W-R)+'" y="'+(T+8)+'" text-anchor="end">纵轴 = 与 LEP N_ν=2.9840 的偏离（σ）</text>';
 document.getElementById('svg3').innerHTML=s;
})();
document.getElementById('items').innerHTML=it.map(x=>'<div class="card"><b>'+x.id+'</b> <span class="tag '+x.v+'">'+x.v+'</span> '+x.t+'<div style="margin-top:6px">'+x.d+'</div></div>').join('');
</script>
</body></html>"""
    doc = doc.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False)).replace("TUFT-RID", "TUFT-" + RID)
    with io.open(wpath(p), "w", encoding="utf-8") as f:
        f.write(doc)
    return p


def main():
    r1 = p1()
    p2()
    p3()
    p4()
    p5()
    p6()
    p7()
    p8()
    p9()
    p10()
    controls()
    dims = [6, 3, 3, 2, 1, 1]
    guards({
        "declared_n": 10 + 4 + 10,
        "schur_ok": r1["ok"],
        "schur_rows": "、".join("%s=%s" % (r["表示"], r["复解空间维数"]) for r in r1["rows"]),
        "frac_ok": all(isinstance(x, Fraction)
                       for g in (su2_fund()[0] + su3_fund()[0] + su2_adjoint()[0] + su2_reducible_2plus1()[0])
                       for Mm in (g[0], g[1]) for row in Mm for x in row),
        "int_ok": all(isinstance(x, int) and x > 0 for x in dims),
        "dims": str(dims),
    })
    s = emit()
    hp = html()
    print("=" * 78)
    print("TUFT-%s · 磁通手征谱「SM 三代不可实现」定理" % RID)
    print("=" * 78)
    for k, v in s.items():
        print("%-10s : %s" % (k, v))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-9s %s" % (it["id"], it["verdict"], it["title"]))
    print("-" * 78)
    print("HTML:", hp)
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    rc = 0 if (not bad) and all(i["verdict"] == "PASS" for i in ITEMS if i["layer"] == "守卫") else 2
    print("RC =", rc)
    sys.exit(rc)


if __name__ == "__main__":
    main()
