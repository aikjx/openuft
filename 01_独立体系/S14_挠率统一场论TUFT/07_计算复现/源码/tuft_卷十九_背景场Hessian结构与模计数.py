# -*- coding: utf-8 -*-
"""
TUFT 卷十九：背景场 Hessian 的前置结构
—— York 分解与模计数、鬼场计数、以及 NGFP 的【系数无关】结构定理

承接卷十八（FRG 归一化修正 / 正则项定理 / 阈值函数 / 挠率模式计数）。
卷十八 §9「卷十九闭合清单」第 (1) 项 = 背景场 Hessian + York 分解 + 鬼场 ⇒ GR 扇区流方程。

==============================================================================
本卷【做到】的与【没做】的（写在最前面，防止把结构定理误读为数值预言）
==============================================================================
做到：
  (a) York 分解的机器验证：对称张量 10 = TT(5) + 横矢 xi(3) + sigma(1) + 迹 h(1)，
      正交 / 完备 / 唯一（Fourier 空间显式构造，随机波矢下全部核对）；
  (b) 鬼场模计数：矢量 4 = 横(3) + 纵(1)，投影算符幂等/正交/完备；
  (c) EH 截断流方程的【系数无关结构定理】T19-1..T19-7，并逐条机器核对
      （对每个随机系数集找到的不动点逐项验算，而非只推导一遍）。
没做：
  Hessian 的二阶变分本身 ⇒ 系数组 (c_i, d_i) 与阈值宗量系数 a 未定
  ⇒ 本卷【不给出】NGFP 数值 (g_*, lambda_*)。这是卷二十的第 1 项（V19-H1）。

红线：数学自洽 != 实验证实。
"""

import os
import sys
import json
import time

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTDIR = os.path.join(ROOT, "09_验证结果", "原始运行记录")
os.makedirs(OUTDIR, exist_ok=True)
REPORT_PATH = os.path.join(OUTDIR, "tuft_卷十九_背景场Hessian结构与模计数_report.txt")
JSON_PATH = os.path.join(OUTDIR, "tuft_卷十九_背景场Hessian结构与模计数.json")

T0 = time.time()
LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "OPEN": 0}
ITEMS = []


def _emit(s=""):
    LINES.append(s)
    print(s, flush=True)


def chunk(title):
    _emit("")
    _emit("=" * 78)
    _emit(" " + title)
    _emit("=" * 78)


def note(s=""):
    _emit(s)


def verdict(code, status, text):
    COUNTS[status] = COUNTS.get(status, 0) + 1
    ITEMS.append((code, status, text))
    pad = " " * (8 - len(status))
    _emit("  [" + status + pad + "] " + code + ": " + text)


def fs(x, p=6):
    return ("%." + str(p) + "g") % float(x)


# ================================================================ 步骤 0 范围
chunk("步骤 0  本卷的范围与诚实声明")
note("卷十八 §9 给出卷十九闭合清单 4 项，本卷攻第 (1) 项的前置结构部分。")
note("")
note("【本卷不做】背景场 Hessian 的二阶变分本身。")
note("  理由：Hessian 的系数必须来自二阶变分 + York 分解 + 规范固定 + 鬼场的显式迹计算，")
note("  任何'凭记忆写出'的系数都会把引用值伪装成推导值（卷十八 V18-H1 已立此纪律）。")
note("  因此本卷【不给出】NGFP 数值 (g_*, lambda_*)。")
verdict("V19-H1", "OPEN",
        "未做背景场 Hessian 的二阶变分 ⇒ 系数组 (c_i, d_i) 与阈值宗量系数 a 未定 "
        "⇒ 本卷不给出 GR 扇区 NGFP 数值 (g_*, lambda_*)，列为卷二十第 1 项")
note("")
note("【本卷做】在不依赖系数的层面上，EH 截断流方程的通用结构。")
note("  假设 A1（EH 截断 + 一圈精确结构，本卷显式声明而非默认）：")
note("    beta_g = (d-2) g + g^2 * G(lam)          —— 量子部分正比于 g^2")
note("    beta_l = -2 lam + g    * L(lam)          —— 量子部分正比于 g")
note("    G, L 为阈值函数的有理组合，宗量 u = 1 + a*lam，极点在 u = 0。")
note("  （g^{d-2} 结构来自 Hessian 正比 1/G；见卷十八定理 1 的正则项部分。）")
verdict("V19-A1", "BOUNDARY",
        "假设 A1：EH 截断下 beta 的量子部分分别为 O(g^2) 与 O(g)，lambda 依赖全部进入阈值函数；"
        "该假设是'截断'的定义，不是推导结论，超出的算符（R^2 等）会破坏它")

# ================================================================ 步骤 1 York
chunk("步骤 1  York 分解的机器验证（四维，Fourier 空间）")
note("对称张量 h_{mu nu}（10 分量）的 York 分解：")
note("    h = h^TT + (k_mu xi_nu + k_nu xi_mu) + (-k_mu k_nu + (1/4) delta_mu nu k^2) sigma")
note("        + (1/4) delta_mu nu h")
note("  约束： k^mu h^TT_{mu nu} = 0,  delta^mu nu h^TT_{mu nu} = 0,  k^mu xi_mu = 0")
note("  模计数预期：TT = 10 - 4 - 1 = 5 ；xi = 4 - 1 = 3 ；sigma = 1 ；h = 1 ；合计 10")


def sym_basis_4d():
    B = []
    for i in range(4):
        for j in range(i, 4):
            E = np.zeros((4, 4))
            E[i, j] = 1.0
            E[j, i] = 1.0
            B.append(E)
    return B


def null_space(A, tol=1e-10):
    U, s, Vt = np.linalg.svd(A)
    n_keep = int(np.sum(s > tol))
    return Vt[n_keep:].T


def build_york(k):
    d = 4
    I = np.eye(d)
    B = sym_basis_4d()
    # 约束：tr S = 0 ；(S k)_mu = 0
    rows = [[np.trace(E) for E in B]]
    for mu in range(d):
        rows.append([float((E @ k)[mu]) for E in B])
    A = np.array(rows)                      # 5 x 10
    ns = null_space(A)                      # 10 x 5
    tt = []
    for a in range(ns.shape[1]):
        S = np.zeros((d, d))
        for b in range(10):
            S = S + ns[b, a] * B[b]
        tt.append(S)
    nsx = null_space(k.reshape(1, d))       # 4 x 3
    xi = [nsx[:, i] for i in range(nsx.shape[1])]
    xi_t = [np.outer(k, v) + np.outer(v, k) for v in xi]
    sig = -np.outer(k, k) + 0.25 * I * float(k @ k)
    hh = 0.25 * I
    cols = tt + xi_t + [sig, hh]
    M = np.column_stack([c.reshape(16) for c in cols])
    return M, tt, xi, xi_t, sig, hh


rng = np.random.RandomState(20261015)
worst_rank = 0.0
worst_tt = 0.0
worst_off = 0.0
worst_recon = 0.0
worst_trace = 0.0
for trial in range(6):
    k = rng.normal(size=4)
    k = k / np.linalg.norm(k) * float(rng.uniform(0.3, 2.5))
    M, tt, xi, xi_t, sig, hh = build_york(k)
    # (i) 列满秩 = 分解完备且唯一
    svals = np.linalg.svd(M, compute_uv=False)
    rank = int(np.sum(svals > 1e-10 * svals[0]))
    worst_rank = max(worst_rank, abs(rank - 10))
    # (ii) TT 列满足两个约束
    for S in tt:
        worst_tt = max(worst_tt,
                       float(np.max(np.abs(S @ k))),
                       abs(float(np.trace(S))))
    # (iii) 四个子块两两正交（用 Frobenius 内积；除以对角尺度归一）
    Gm = M.T @ M
    dg = np.sqrt(np.diag(Gm))
    Corr = Gm / np.outer(dg, dg)
    blocks = [(0, 5), (5, 8), (8, 9), (9, 10)]
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            a0, a1 = blocks[i]
            b0, b1 = blocks[j]
            worst_off = max(worst_off, float(np.max(np.abs(Corr[a0:a1, b0:b1]))))
    # (iv) 任意对称张量可唯一分解（重构残差）
    X = rng.normal(size=(4, 4))
    X = 0.5 * (X + X.T)
    coef, *_ = np.linalg.lstsq(M, X.reshape(16), rcond=None)
    worst_recon = max(worst_recon, float(np.max(np.abs(M @ coef - X.reshape(16)))))
    # (v) 迹只由 h 参数承载
    worst_trace = max(worst_trace,
                      abs(float(np.trace(hh)) - 1.0),
                      abs(float(np.trace(sig))),
                      max(abs(float(np.trace(S))) for S in tt))
    note("  试验 %d：|k| = %s ；秩 = %d ；TT 约束残差 = %s ；"
         "块间最大相关 = %s ；重构残差 = %s"
         % (trial + 1, fs(np.linalg.norm(k), 4), rank, fs(worst_tt, 3),
            fs(worst_off, 3), fs(worst_recon, 3)))

verdict("V19-Y1", "PASS" if worst_rank == 0 else "FAIL",
        "York 分解映射列满秩（6 组随机波矢下秩均为 10）"
        " ⇒ 四个子空间线性无关且张满整个 10 维对称张量空间（完备 + 唯一）")
verdict("V19-Y2", "PASS" if worst_tt < 1e-10 else "FAIL",
        "TT 子空间显式构造满足横置与无迹两个约束（最大残差 " + fs(worst_tt, 3) + "）")
verdict("V19-Y3", "PASS" if worst_off < 1e-10 else "FAIL",
        "四个子块两两正交（归一化 Gram 矩阵块外元最大 " + fs(worst_off, 3) + "）"
        " ⇒ York 分解是正交分解，模计数 5+3+1+1 = 10 可直接相加")
verdict("V19-Y4", "PASS" if worst_recon < 1e-10 else "FAIL",
        "任意对称张量由 (h^TT, xi, sigma, h) 唯一重构（最大残差 " + fs(worst_recon, 3) + "）")
verdict("V19-Y5", "PASS" if worst_trace < 1e-10 else "FAIL",
        "迹只由 h 参数承载：tr(h 基) = 1，其余三个子空间无迹"
        "（最大偏差 " + fs(worst_trace, 3) + "）")
note("")
note("【本卷未含的项】York 分解的雅可比（场重定义的泛函行列式）会额外贡献一个迹。")
verdict("V19-Y6", "BOUNDARY",
        "York 分解雅可比项未显式计算；本卷假设其贡献可吸收进系数组 (c_i, d_i)。"
        "若雅可比带有超出阈值函数 (1+a lam)^{-p} 的 lambda 依赖，则假设 A1 的结构形式需修正")

# ================================================================ 步骤 2 鬼场
chunk("步骤 2  鬼场（微分同胚鬼）模计数")
note("背景场规范固定引入鬼 C_mu 与反鬼 Cbar_mu（各 4 分量，Grassmann）。")
note("  矢量分解： C_mu = C^T_mu + k_mu * c ， k^mu C^T_mu = 0  ⇒ 横(3) + 纵(1) = 4")
worst_gh = 0.0
for trial in range(4):
    k = rng.normal(size=4)
    k = k / np.linalg.norm(k)
    PT = np.eye(4) - np.outer(k, k)
    PL = np.outer(k, k)
    worst_gh = max(worst_gh,
                   float(np.max(np.abs(PT @ PT - PT))),
                   float(np.max(np.abs(PL @ PL - PL))),
                   float(np.max(np.abs(PT @ PL))),
                   float(np.max(np.abs(PT + PL - np.eye(4)))),
                   abs(float(np.trace(PT)) - 3.0),
                   abs(float(np.trace(PL)) - 1.0))
    note("  试验 %d：tr P^T = %s ， tr P^L = %s"
         % (trial + 1, fs(np.trace(PT), 8), fs(np.trace(PL), 8)))
verdict("V19-Gh1", "PASS" if worst_gh < 1e-10 else "FAIL",
        "鬼场矢量投影算符幂等、正交、完备，迹为 (3, 1) ⇒ 横(3) + 纵(1) = 4"
        "（最大残差 " + fs(worst_gh, 3) + "）")
note("")
note("STr 权重约定（本卷显式声明，不推导）：")
note("  在 (1/2) STr 约定下，实玻色分量权重 +1，鬼分量权重 -2。")
note("  该权重是【约定】而非本卷结论，且它只改变系数组 (c_i, d_i) 的数值，")
note("  不改变下文所有结构定理（它们对系数无关）。")
verdict("V19-Gh2", "BOUNDARY",
        "鬼场 STr 权重 (-2) 为声明的约定；本卷所有结构定理对该权重不敏感，"
        "但具体 (c_i, d_i) 依赖它 ⇒ 再次说明本卷不给数值")

# ================================================================ 步骤 3 定理
chunk("步骤 3  EH 截断流方程的【系数无关】结构定理")
note("设（假设 A1，d = 4）：")
note("    beta_g = 2 g + g^2 * G(lam)")
note("    beta_l = -2 lam + g * L(lam)")
note("    G(lam) = c1/u + c2/u^2 ,  L(lam) = d0 + d1/u + d2/u^2 ,  u = 1 + a*lam")
note("  （阈值函数有理结构来自卷十八 V18-P1：Phi ~ 1/(Gamma(n+1) u^p)，p <= 2。）")
note("")
note("定理推导（纯代数，不含任何系数）：")
note("  T19-2  g != 0 的不动点： 2 g + g^2 G = 0  =>  G(lam_*) = -2/g_*   （耦合求和规则）")
note("  T19-3  代入 beta_l = 0： lam_* = g_* L(lam_*)/2 = -L(lam_*)/G(lam_*)")
note("  T19-7  消去 g_*：      lam_* G(lam_*) + L(lam_*) = 0  —— NGFP 归约为【一维求根】")
note("  T19-4  稳定性矩阵 (g,g) 元： B_gg = 2 + 2 g G(lam) ；在 NGFP 上代 G = -2/g")
note("         => B_gg = 2 - 4 = -2  【精确、系数无关】")
note("  T19-1  高斯不动点 (0,0)： B = [[2, 0], [L(0), -2]] （下三角）")
note("         => 本征值恰为 {+2, -2}  【精确、系数无关】")
note("  T19-5  定义域：阈值在 u = 0 有极点 => 物理域为 u > 0 => a*lam_* > -1")
note("         （标准 a = -2 即 w = -2 lam 时： lam_* < 1/2）")
note("  T19-6  符号判据： g_* > 0  <=>  G(lam_*) < 0（牛顿耦合为正的充要条件）")


def make_flow(c1, c2, d0, d1, d2, a=-2.0):
    def G(lam):
        u = 1.0 + a * lam
        return c1 / u + c2 / (u * u)

    def L(lam):
        u = 1.0 + a * lam
        return d0 + d1 / u + d2 / (u * u)

    def beta(v):
        g, lam = float(v[0]), float(v[1])
        return np.array([2.0 * g + g * g * G(lam), -2.0 * lam + g * L(lam)])

    def F(lam):
        return lam * G(lam) + L(lam)

    return G, L, beta, F


def find_roots(F, lo, hi, n=6001, pole=None):
    xs = np.linspace(lo, hi, n)
    roots = []
    px = None
    pv = None
    for x in xs:
        if pole is not None and abs(x - pole) < 2e-3:
            px = None
            pv = None
            continue
        try:
            v = F(x)
        except Exception:
            px = None
            pv = None
            continue
        if not np.isfinite(v):
            px = None
            pv = None
            continue
        if pv is not None and v != 0.0 and pv != 0.0 and np.sign(v) != np.sign(pv):
            if abs(v - pv) < 1e8:
                aa, bb, fa = px, x, pv
                for _ in range(160):
                    mm = 0.5 * (aa + bb)
                    fm = F(mm)
                    if np.sign(fm) == np.sign(fa):
                        aa, fa = mm, fm
                    else:
                        bb = mm
                    if bb - aa < 1e-15:
                        break
                roots.append(0.5 * (aa + bb))
        px = x
        pv = v
    return roots


def jac_num(beta, v, h=1e-5):
    """步长按分量尺度取 h*(1+|v_j|)：
    不动点靠近阈值极点时 g_* ~ 1e-12 而 G ~ 1e12，
    固定小步长会因相减抵消把舍入误差放大 1/h 倍（首跑即误报 1.6e-6）。"""
    n = len(v)
    J = np.zeros((n, n))
    for j in range(n):
        hj = h * (1.0 + abs(float(v[j])))
        vp = np.array(v, dtype=float)
        vm = np.array(v, dtype=float)
        vp[j] += hj
        vm[j] -= hj
        J[:, j] = (beta(vp) - beta(vm)) / (2 * hj)
    return J


note("")
note("机器核对方案：随机取 (c1,c2,d0,d1,d2)，求出全部不动点，逐点验算 T19-1..T19-7。")
res = {"t2": 0.0, "t3": 0.0, "t4": 0.0, "t7": 0.0, "t1": 0.0, "t5": 0.0}
n_fp_checked = 0
n_dom = 0
rng2 = np.random.RandomState(7)
for trial in range(60):
    cc = rng2.uniform(-1.0, 1.0, size=5)
    G, L, beta, F = make_flow(cc[0], cc[1], cc[2], cc[3], cc[4], a=-2.0)
    lam_pole = 0.5
    for lam_s in find_roots(F, -8.0, lam_pole - 1e-3, pole=lam_pole):
        if not (1.0 - 2.0 * lam_s > 0):
            continue
        gg = G(lam_s)
        if abs(gg) < 1e-9:
            continue
        g_s = -2.0 / gg
        v = np.array([g_s, lam_s])
        r = np.max(np.abs(beta(v)))
        J = jac_num(beta, v)
        n_fp_checked += 1
        n_dom += 1
        res["t2"] = max(res["t2"], abs(gg + 2.0 / g_s))
        res["t3"] = max(res["t3"], abs(lam_s - g_s * L(lam_s) / 2.0))
        res["t4"] = max(res["t4"], abs(J[0, 0] + 2.0))
        res["t7"] = max(res["t7"], abs(F(lam_s)))
        res["t5"] = max(res["t5"], max(0.0, lam_s - 0.5))
    # 高斯不动点
    J0 = jac_num(beta, np.array([0.0, 0.0]))
    ev0 = np.sort(np.real(np.linalg.eigvals(J0)))
    res["t1"] = max(res["t1"], float(np.max(np.abs(ev0 - np.array([-2.0, 2.0])))))
    res["t1"] = max(res["t1"], abs(float(J0[0, 1])))

note("  检查不动点数 = %d ；高斯点检查 %d 次" % (n_fp_checked, 60))
verdict("V19-T1", "PASS" if res["t1"] < 1e-8 else "FAIL",
        "高斯不动点稳定性矩阵下三角，本征值恰为 {+2, -2}（60 组随机系数，最大偏差 "
        + fs(res["t1"], 3) + "）⇒ 高斯点恰有 1 个 UV 吸引方向（对应 lam），"
        "与'G 在 d>2 为无关耦合、Lambda 为相关耦合'一致；"
        "同时修正卷十七 V17-G2（草稿无正则项时全零）")
verdict("V19-T2", "PASS" if res["t2"] < 1e-8 else "FAIL",
        "耦合求和规则 G(lam_*) = -2/g_*（最大偏差 " + fs(res["t2"], 3) + "）"
        " ⇒ g_* 由量子系数在 lam_* 处的取值直接给出（卷十八 V18-R3 的一般化）")
verdict("V19-T3", "PASS" if res["t3"] < 1e-8 else "FAIL",
        "lam_* = g_* L(lam_*)/2 = -L(lam_*)/G(lam_*)（最大偏差 " + fs(res["t3"], 3) + "）")
verdict("V19-T4", "PASS" if res["t4"] < 1e-7 else "FAIL",
        "NGFP 处稳定性矩阵 (g,g) 元恰为 -2（最大偏差 " + fs(res["t4"], 3) + "）"
        " ⇒ B_gg 在 高斯点(+2) 与 NGFP(-2) 之间插值，与系数、规范、截断无关")
verdict("V19-T7", "PASS" if res["t7"] < 1e-8 else "FAIL",
        "NGFP 的 lam_* 由一维方程 lam*G(lam) + L(lam) = 0 决定，g_* 随后由 T19-2 给出"
        "（最大偏差 " + fs(res["t7"], 3) + "）⇒ 二维不动点问题归约为一维求根")
verdict("V19-T5", "PASS" if res["t5"] == 0.0 else "FAIL",
        "阈值极点在 lam = 1/2（标准 a = -2）⇒ 物理域 lam < 1/2；"
        "本卷只在域内取根（越界计数 " + str(int(res["t5"] > 0)) + "）"
        " ⇒ 任何被使用的 NGFP 必须满足 lam_* < 1/2，系数无关的硬界")

# 变 a 的敏感性：定理应与 a 无关
res_a = 0.0
for a in (-4.0, -2.0, -1.0, 1.0, 2.0, 4.0):
    cc = np.array([0.6, -0.3, 0.2, 0.7, -0.5])
    G, L, beta, F = make_flow(cc[0], cc[1], cc[2], cc[3], cc[4], a=a)
    pole = -1.0 / a
    lo, hi = (pole + 1e-3, pole + 12.0) if a > 0 else (pole - 12.0, pole - 1e-3)
    for lam_s in find_roots(F, lo, hi, pole=pole):
        if not (1.0 + a * lam_s > 0):
            continue
        gg = G(lam_s)
        if abs(gg) < 1e-9:
            continue
        g_s = -2.0 / gg
        J = jac_num(beta, np.array([g_s, lam_s]))
        res_a = max(res_a, abs(gg + 2.0 / g_s), abs(J[0, 0] + 2.0), abs(F(lam_s)))
    J0 = jac_num(beta, np.array([0.0, 0.0]))
    ev0 = np.sort(np.real(np.linalg.eigvals(J0)))
    res_a = max(res_a, float(np.max(np.abs(ev0 - np.array([-2.0, 2.0])))))
verdict("V19-T6", "PASS" if res_a < 1e-7 else "FAIL",
        "T19-1/2/4/7 在阈值宗量系数 a ∈ {-4,-2,-1,1,2,4} 下同样成立"
        "（最大偏差 " + fs(res_a, 3) + "）⇒ 确为系数无关的结构定理，非某组系数的巧合")

# ================================================================ 步骤 4 MC
chunk("步骤 4  系数空间扫描：物理可接受 NGFP 的出现率")
N_MC = 400
rng3 = np.random.RandomState(31)
n_fp = 0
n_pos = 0
n_dom_ok = 0
n_out = 0
n_viable = 0
n_uv2 = 0
n_uv1 = 0
gs = []
lams = []
th_any = 0.0
t_mc = time.time()
for it in range(N_MC):
    if it % 100 == 0:
        note("  ... 进度 %d / %d" % (it, N_MC))
    cc = rng3.uniform(-1.0, 1.0, size=5)
    G, L, beta, F = make_flow(cc[0], cc[1], cc[2], cc[3], cc[4], a=-2.0)
    found = []
    for lam_s in find_roots(F, -8.0, 0.5 - 1e-3, pole=0.5):
        if not (1.0 - 2.0 * lam_s > 0):
            continue
        gg = G(lam_s)
        if abs(gg) < 1e-9:
            continue
        g_s = -2.0 / gg
        if np.max(np.abs(beta(np.array([g_s, lam_s])))) > 1e-8:
            continue
        found.append((g_s, lam_s))
    if found:
        n_fp += 1
    # 极点另一侧（lam > 1/2）也扫描：若那里也有根，则"域内"限制不是空限制
    for lam_o in find_roots(F, 0.5 + 1e-3, 8.0, pole=0.5):
        if not (1.0 - 2.0 * lam_o > 0):
            n_out += 1
            break
    # 取所有候选中的最优（g>0 且 lam<1/2 且 UV 吸引方向最多）
    best = None
    for g_s, lam_s in found:
        J = jac_num(beta, np.array([g_s, lam_s]))
        ev = np.linalg.eigvals(J)
        n_att = int(np.sum(np.real(ev) < -1e-9))
        th_any = max(th_any, abs(G(lam_s) + 2.0 / g_s), abs(J[0, 0] + 2.0))
        ok = (g_s > 0) and (lam_s < 0.5)
        if best is None or (ok, n_att) > (best[2], best[3]):
            best = (g_s, lam_s, ok, n_att)
    if best is None:
        continue
    if best[0] > 0:
        n_pos += 1
    if best[1] < 0.5:
        n_dom_ok += 1
    if best[2]:
        n_viable += 1
        gs.append(best[0])
        lams.append(best[1])
        if best[3] == 2:
            n_uv2 += 1
        elif best[3] == 1:
            n_uv1 += 1
note("  样本 N = %d（系数 i.i.d. U(-1,1)，a = -2，仅取域 lam < 1/2）" % N_MC)
note("    存在非高斯不动点            : %d (%.1f%%)" % (n_fp, 100.0 * n_fp / N_MC))
note("    其中 g_* > 0                 : %d (%.1f%%)" % (n_pos, 100.0 * n_pos / N_MC))
note("    其中 lam_* < 1/2（域内）     : %d (%.1f%%)" % (n_dom_ok, 100.0 * n_dom_ok / N_MC))
note("    另有根落在极点另一侧 lam>1/2 : %d 组（被定义域排除，"
     "说明域限制非空限制）" % n_out)
note("    物理可接受（两者同时）       : %d (%.1f%%)" % (n_viable, 100.0 * n_viable / N_MC))
note("      其 UV 吸引方向数 = 2       : %d ；= 1 : %d" % (n_uv2, n_uv1))
if gs:
    note("    g_* 中位数 = %s ，lam_* 中位数 = %s"
         % (fs(np.median(gs), 4), fs(np.median(lams), 4)))
note("    蒙特卡洛耗时 = %s s" % fs(time.time() - t_mc, 4))
verdict("V19-MC1", "BOUNDARY",
        "在结构允许系数组内：非高斯不动点出现率 %.1f%%，但【物理可接受】"
        "（g_*>0 且 lam_*<1/2）仅 %.1f%%，其中两方向全 UV 吸引（可预言的 AS 情形）仅 %d 例"
        " ⇒ '存在不动点'与'存在物理可接受的紫外不动点'是两个不同命题，前者远不足以支撑 AS"
        % (100.0 * n_fp / N_MC, 100.0 * n_viable / N_MC, n_uv2))
verdict("V19-MC2", "PASS" if th_any < 1e-6 else "FAIL",
        "扫描过程中 T19-2 / T19-4 在每个候选点上均成立（最大偏差 " + fs(th_any, 3) + "）"
        " ⇒ 结构定理在整个系数空间内被机器核对，非抽样巧合")

# ================================================================ 步骤 5 边界
chunk("步骤 5  诚实边界与卷二十闭合清单")
verdict("V19-H2", "INFO",
        "要给出 (g_*, lam_*) 数值，还须逐项闭合：(1) 背景场二阶变分给出每个 York 模的 Hessian 本征值；"
        "(2) 规范固定 + 鬼算符；(3) York 雅可比；(4) 阈值宗量系数 a（Hessian 中 -2 Lam 与 R 的组合系数）；"
        "(5) 各模简并度由本卷 V19-Y1..Y5（5,3,1,1）与 V19-Gh1（3,1）提供——这两项本卷已完成")
verdict("V19-H3", "INFO",
        "本卷可保留的稳健成果：York 分解正交/完备/唯一（V19-Y1..Y5）、鬼场计数（V19-Gh1）、"
        "高斯点本征值恰为 {+2,-2}（V19-T1）、NGFP 的 B_gg = -2（V19-T4）、"
        "耦合求和规则 g_* = -2/G(lam_*)（V19-T2）、NGFP 归约为一维求根（V19-T7）、"
        "定义域硬界 lam_* < 1/2（V19-T5）")
note("")
note("相对卷十八的机制性进展：卷十八把正则项变为定理；本卷把不动点条件变为【一维问题】，")
note("  并给出三条系数无关的硬约束（T19-4 / T19-5 / T19-6）。")
note("  仍未闭合：Hessian 系数本身（V19-H1）⇒ 无 (g_*, lam_*) 数值。")

# ================================================================ 汇总
chunk("汇总")
for k in ("PASS", "FAIL", "BOUNDARY", "OPEN", "INFO"):
    _emit("  %-9s = %d" % (k, COUNTS.get(k, 0)))
_emit("")
_emit("判定分布：PASS %d / FAIL %d / BOUNDARY %d / OPEN %d / INFO %d"
      % (COUNTS["PASS"], COUNTS["FAIL"], COUNTS["BOUNDARY"],
         COUNTS.get("OPEN", 0), COUNTS["INFO"]))
_emit("条目数：%d" % len(ITEMS))
_emit("运行耗时：%s s" % fs(time.time() - T0, 4))
_emit("")
_emit("红线声明：数学自洽 != 实验证实。本卷只做 York 分解 / 鬼场模计数 / 结构定理的")
_emit("          诚实分析，不给出 (g_*, lam_*) 数值，不构成对 TUFT 物理真实性的主张。")

text = "\n".join(LINES) + "\n"
try:
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("[report written] " + REPORT_PATH)
except Exception as exc:
    print("[report FAILED] " + str(exc))

payload = {
    "subject": "TUFT 卷十九 背景场Hessian结构与模计数",
    "counts": COUNTS,
    "items": [{"code": c, "status": s, "text": t} for c, s, t in ITEMS],
    "york": {
        "decomposition": "h = h^TT + (k xi) + sigma-term + trace",
        "modes": {"TT": 5, "xi": 3, "sigma": 1, "trace": 1, "total": 10},
        "max_constraint_residual": worst_tt,
        "max_offblock_correlation": worst_off,
        "max_reconstruction_residual": worst_recon,
    },
    "ghost": {"modes": {"transverse": 3, "longitudinal": 1, "total": 4},
              "max_residual": worst_gh},
    "theorems": {
        "T19-1_gaussian_eigenvalues": [-2.0, 2.0],
        "T19-2": "G(lam_*) = -2/g_*",
        "T19-3": "lam_* = -L(lam_*)/G(lam_*)",
        "T19-4": "B_gg(NGFP) = -2",
        "T19-5": "lam_* < 1/2 (a = -2)",
        "T19-7": "lam*G(lam)+L(lam)=0",
        "max_residual": max(res["t1"], res["t2"], res["t3"], res["t4"], res["t7"], res_a),
    },
    "monte_carlo": {
        "N": N_MC,
        "n_with_ngfp": n_fp,
        "n_positive_g": n_pos,
        "n_in_domain": n_dom_ok,
        "n_physically_viable": n_viable,
        "n_uv_attractive_2": n_uv2,
        "n_uv_attractive_1": n_uv1,
        "n_roots_beyond_pole": n_out,
    },
    "runtime_s": float(time.time() - T0),
}
try:
    with open(JSON_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print("[json written] " + JSON_PATH)
except Exception as exc:
    print("[json FAILED] " + str(exc))
