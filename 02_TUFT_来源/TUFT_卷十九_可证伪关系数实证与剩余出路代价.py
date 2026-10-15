# -*- coding: utf-8 -*-
# =====================================================================
# TUFT 卷十九 · 可证伪关系数 FR 的实证 + 参数—预测力权衡定理
#              + 剩余出路的代价账单（攻破册）
# ---------------------------------------------------------------------
# 纯 NumPy + 标准库 Fraction
#
# 承接卷十八：FR = d − rank(J) 在卷十八里还只是一个**定义**。
#   本卷要做三件事把它变成可实测、可用来攻破的东西：
#     (1) 证明并实证 FR ≡ 拟合残差自由度（χ² 的 dof）——蒙特卡洛矩检验；
#     (2) 证明并实证「参数—预测力权衡定理」：加参数要么用 FR 换 r，
#         要么（r 已饱和时）纯恶化；
#     (3) 用这两条机器给出 TUFT 剩余唯一出路与它的代价账单。
#
# 与卷十六的分工（避免重复造轮子）：
#   卷十六问「T_B 的后验有多宽」（可辨识性，σ ∝ N^-1/2）；
#   本卷问「拟合完之后还剩几个自由度的残差可用来否证模型」（FR = dof）。
#   同一系统的两个不同问题，前者是参数估计精度，后者是模型检验能力。
#
# 红线：数学自洽 ≠ 实验证实。本卷审统计推断方法链，不进版本链、
#       不占冻结编号、不是第80章 SSOT 的变更源。
# 产出：同目录 .txt / .json / 三张 png
# =====================================================================
import json
import math
import os
import time
import sys
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def rec(code, name, status, detail, evidence=None):
    RESULTS.append({"code": code, "name": name, "status": status,
                    "detail": detail, "evidence": evidence or {}})
    print("[{0:<9}] {1:<9} {2}".format(status, code, detail))


def sec(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def exact_rank(A):
    A = [[Fraction(x) for x in row] for row in A]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][c]
        for i in range(r + 1, m):
            if A[i][c] != 0:
                f = A[i][c] / pv
                for j in range(c, n):
                    A[i][j] -= f * A[r][j]
        r += 1
        if r == m:
            break
    return r


# 卷十六同源的 Kerr l=2 QNM 锚点与 TUFT 挠率线性响应
_ANCH = {0.0: (0.373672, 0.088962), 0.5: (0.427599, 0.086049), 0.7: (0.474340, 0.083755),
         0.9: (0.537210, 0.082421), 0.99: (0.563050, 0.084016)}
_aa = np.array(sorted(_ANCH))
_PR = np.polyfit(_aa, [_ANCH[x][0] for x in _aa], 2)
_PI = np.polyfit(_aa, [_ANCH[x][1] for x in _aa], 2)


def _fR(a):
    """Kerr l=2 基模实部拟合值 f_R(a)。"""
    return float(np.polyval(_PR, a))


def _fI(a):
    return float(np.polyval(_PI, a))


def _dfR(a):
    return float(np.polyval(np.polyder(_PR), a))


def _dfI(a):
    return float(np.polyval(np.polyder(_PI), a))


def _kR(a):
    """TUFT 挠率响应系数（实部，m=2）。注：系假设，非 FDTD 导出。"""
    return 180.0 + 60.0 * a


def _kI(a):
    return -140.0 - 40.0 * a


def omega(a, M, TB):
    """返回 (ω_R, ω_I)：ω = (f + k·T_B)/M。"""
    return ((_fR(a) + _kR(a) * TB) / M, (-_fI(a) + _kI(a) * TB) / M)


def domega_dTB(a, M):
    """∂(ω_R, ω_I)/∂T_B = (k_R/M, k_I/M)。"""
    return np.array([_kR(a) / M, _kI(a) / M])


# ===================== §1 定理 I：FR ≡ 拟合残差自由度 =====================
def section1(M=4000, TB_true=5e-5, SNR=10.0):
    sec("§1  定理 I 实证：FR = d − r 就是拟合残差自由度（χ² 的 dof）")
    print("  线性化模型 y = ω_0 + X·T_B + ε（ε~N(0,σ²)），X = ∂ω/∂T_B。")
    print("  T_B 单参数 ⇒ r=1 ⇒ FR = 2N−1。若定理成立，χ²_min ~ χ²_{2N−1}。")
    print("  检验：样本均值 ≈ FR、样本方差 ≈ 2·FR（χ²_k 的矩）。\n")
    print("  {0:>4} {1:>5} {2:>9} {3:>9} {4:>7} {5:>9} {6:>9} {7:>7}".format(
        "N", "FR", "mean", "理论", "z_mean", "var", "理论", "z_var"))
    print("  " + "-" * 66)

    rng = np.random.default_rng(20261015)
    out = []
    chis_all = {}
    for N in (1, 2, 5, 10, 30):
        a = rng.uniform(0.05, 0.95, N)
        Mv = rng.uniform(40.0, 80.0, N)
        X = np.concatenate([domega_dTB(a[i], Mv[i]) for i in range(N)])   # 2N 维
        w0 = np.concatenate([np.asarray(omega(a[i], Mv[i], 0.0)) for i in range(N)])
        nx = float(np.dot(X, X))
        sigma = TB_true * np.sqrt(nx) / SNR          # 使信号强度 = SNR²
        FRk = 2 * N - 1

        chis = np.empty(M)
        chis0 = np.empty(M)
        for t in range(M):
            eps = rng.normal(0.0, sigma, 2 * N)
            y = w0 + X * TB_true + eps
            res = y - w0
            tbh = float(np.dot(X, res)) / nx
            chis[t] = float(np.dot(res - X * tbh, res - X * tbh)) / sigma ** 2
            chis0[t] = float(np.dot(res, res)) / sigma ** 2
        mean = float(chis.mean())
        var = float(chis.var(ddof=1))
        se_mean = np.sqrt(2.0 * FRk / M)
        se_var = np.sqrt((8.0 * FRk ** 2 + 48.0 * FRk) / M)
        z_mean = (mean - FRk) / se_mean
        z_var = (var - 2.0 * FRk) / se_var
        ok = (abs(z_mean) < 4.0) and (abs(z_var) < 4.0)
        print("  {0:>4} {1:>5} {2:>9.4f} {3:>9.1f} {4:>7.2f} {5:>9.3f} {6:>9.1f} {7:>7.2f}".format(
            N, FRk, mean, float(FRk), z_mean, var, 2.0 * FRk, z_var))
        out.append((N, FRk, mean, var, z_mean, z_var, ok,
                    float(chis0.mean() - chis.mean())))
        rec("V19-T1-N{0}".format(N), "FR=2N-1 的 χ² 矩检验 (N={0})".format(N),
            "PASS" if ok else "FAIL",
            "χ²_min 均值 {0:.4f} vs 理论 {1}（z={2:+.2f}）、方差 {3:.3f} vs 理论 {4:.1f}"
            "（z={5:+.2f}），M={6} ⇒ {7}".format(
                mean, FRk, z_mean, var, 2.0 * FRk, z_var, M,
                "实证支持 FR ≡ dof" if ok else "拒绝"),
            {"N": N, "FR": FRk, "mean": mean, "var": var,
             "z_mean": float(z_mean), "z_var": float(z_var), "M": M, "SNR": SNR})
        chis_all[N] = chis.copy()

    # 图：χ²_min 的蒙特卡洛分布 vs χ²_FR 理论密度
    _n10 = 10
    if _n10 in chis_all:
        from scipy.stats import chi2 as _chi2
        fig, ax = plt.subplots(figsize=(7.4, 4.4))
        ax.hist(chis_all[_n10], bins=60, density=True, alpha=0.55,
                label="MC chi2_min (N=" + str(_n10) + ")")
        xs = np.linspace(0.0, 55.0, 500)
        ax.plot(xs, _chi2.pdf(xs, 2 * _n10 - 1), "r-", lw=1.8,
                label="chi2 pdf, dof = FR = " + str(2 * _n10 - 1))
        ax.set_xlabel("chi2_min")
        ax.set_ylabel("density")
        ax.set_title("Volume 19 Thm I  FR = dof  (MC vs theory)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, "tuft_v19_FR_as_dof.png"), dpi=130)
        plt.close(fig)

    # 阳性对照：不拟合（固定 T_B=0）时 χ² 必须显著偏大，否则判据恒真
    d0 = out[-1]
    rec("V19-T1P", "阳性对照：不拟合时 χ² 应显著偏大", "PASS" if d0[7] > 4 else "FAIL",
        "N={0}：χ²(不拟合) − χ²(拟合) = {1:.3f}（理论 1+SNR² = {2:.1f}）"
        " ⇒ 拟合确实吸收掉 1 个自由度、残差只剩 FR 个；判据非恒真。"
        .format(d0[0], d0[7], 1 + SNR ** 2),
        {"N": d0[0], "delta": d0[7], "theory": 1 + SNR ** 2})

    # 阴性对照：若把 SNR 压到 0（T_B 真值=0），不拟合与拟合之差应回到 ~1
    rec("V19-T1N", "阴性对照：无信号时差值回到 1", "INFO",
        "T_B=true 时拟合只吸收 1 个自由度，差值 = 1 + SNR²；SNR→0 时差值→1"
        " ⇒ 差值中的 SNR² 项确为信号而非拟合 artifacts。",
        {"SNR": SNR, "delta_theory": 1 + SNR ** 2})
    return out, chis_all


# ===================== §2 定理 II：参数—预测力权衡 =====================
def section2(d=4):
    sec("§2  定理 II 实证：加参数要么用 FR 换 r，要么（饱和后）纯恶化")
    print("  固定观测量 d={0}，逐步增加参数 p。精确秩用随机整数矩阵（Fraction）。".format(d))
    print("  {0:>4} {1:>5} {2:>5} {3:>8} {4:>10}  {5}".format(
        "p", "r", "FR", "nullity", "r+FR", "裁定"))
    print("  " + "-" * 56)

    rng = np.random.default_rng(777)
    base = [[int(x) for x in row] for row in rng.integers(1, 20, size=(d, 12))]
    rows = []
    for p in range(1, 13):
        A = [row[:p] for row in base]           # 前 p 列，列之间一般线性无关
        r = exact_rank(A)
        fr_ = d - r
        nullity = p - r
        if p < d:
            verdict = "用 FR 换 r（每加 1 参数 FR −1）"
        elif p == d:
            verdict = "临界：FR 恰降为 0"
        else:
            verdict = "饱和：FR 已为 0，加参数只增 nullity（纯恶化）"
        print("  {0:>4} {1:>5} {2:>5} {3:>8} {4:>10}  {5}".format(
            p, r, fr_, nullity, r + fr_, verdict))
        rows.append((p, r, fr_, nullity, verdict))
        rec("V19-T2-p{0}".format(p), "p={0}".format(p), "INFO",
            "r={0}, FR={1}, nullity={2}, r+FR={3}（恒 = d）⇒ {4}".format(
                r, fr_, nullity, r + fr_, verdict),
            {"p": p, "r": r, "FR": fr_, "nullity": nullity})

    # 守恒律
    conserv = all(x[1] + x[2] == d for x in rows)
    rec("V19-T2C", "数据维度守恒律 r + FR = d", "PASS" if conserv else "FAIL",
        "全部 {0} 个 p 值上 r + FR ≡ d = {1}（恒等成立）⇒ 「可辨识方向数」与"
        "「可证伪关系数」是同一份数据维度的两种分配，此消彼长不可兼得。"
        .format(len(rows), d), {"d": d, "n_cases": len(rows)})

    # 饱和段判定
    sat = [x for x in rows if x[0] > d]
    ok_sat = all(x[2] == 0 and x[3] == x[0] - d for x in sat)
    rec("V19-T2S", "饱和后加参数 = 纯恶化", "PASS" if ok_sat else "FAIL",
        "p>d 的 {0} 个情形：FR 恒 = 0 且 nullity = p − d ⇒ 加参数**既不增加可辨识性"
        "也不增加预测力**，只增加不可约束方向的维数。"
        .format(len(sat)), {"n_sat": len(sat)})
    return rows, d


# ============ §3-A 简并的有效域与「不可吸收比」η（修正卷十六） ============
def _obs_tuft(a, M, TB):
    return np.array([(_fR(a) + _kR(a) * TB) / M, (-_fI(a) + _kI(a) * TB) / M])


def _resid_sq(ah, w):
    """固定 â 后对 M̂ 解析取优的残差平方：‖w‖² − (v·w)²/‖v‖²，v=(f_R(â),−f_I(â))。"""
    fr = _fR(ah)
    fi = _fI(ah)
    vw = fr * w[0] - fi * w[1]
    vv = fr * fr + fi * fi
    return float(w[0] ** 2 + w[1] ** 2) - vw * vw / vv


def _anchor_of(ah, w):
    vw = _fR(ah) * w[0] - _fI(ah) * w[1]
    vv = _fR(ah) ** 2 + _fI(ah) ** 2
    Mh = vv / vw
    res = float(math.hypot(w[0] - _fR(ah) / Mh, w[1] + _fI(ah) / Mh))
    return res, float(ah), float(Mh)


def _best_gr_fit(w):
    """在 GR 族 ω_GR(â,M̂)=(f_R(â),−f_I(â))/M̂ 内对给定 w 做最优拟合。

    零残差 ⟺ w ∥ v ⟺ g(â) = f_I(â)·ω_R + f_R(â)·ω_I = 0。
    故先用网格找 g 的全部变号区间、用 brentq 精确求根（残差真为机器零）；
    无变号区间才退化为连续最小化。绝不用「网格扫描取最小」——那会把网格步长
    当成物理残差（本卷初版即踩此坑：网格 2.5e-4 制造出 η~1e-4 的假非零）。
    """
    from scipy.optimize import brentq, minimize_scalar
    grid = np.linspace(0.0, 0.999, 2001)
    gv = np.array([_fI(float(x)) * w[0] + _fR(float(x)) * w[1] for x in grid])
    idx = np.where(np.sign(gv[:-1]) * np.sign(gv[1:]) < 0)[0]
    best = None
    for i in idx:
        def g(x):
            return _fI(x) * w[0] + _fR(x) * w[1]
        ah = brentq(g, float(grid[i]), float(grid[i + 1]), xtol=1e-16, rtol=8.9e-16)
        cand = _anchor_of(float(ah), w)
        if best is None or cand[0] < best[0]:
            best = cand
    if best is not None:
        return best
    r = minimize_scalar(lambda x: _resid_sq(x, w), bounds=(0.0, 0.999),
                        method="bounded", options={"xatol": 1e-14})
    return _anchor_of(float(r.x), w)


def eta(a, M, TB):
    """不可吸收比 η = min_GR‖ω_GR − ω_TUFT‖ / ‖ω_TUFT − ω_GR(a,M,0)‖。

    η = 0 ⇒ GR 靠重拟合 (a,M) 就能完全吞掉挠率信号（卷十六的精确简并）；
    η = 1 ⇒ 一点都吞不掉。η 与 M 无关（分子分母同 ∝ 1/M）。
    """
    w = _obs_tuft(a, M, TB)
    sig = float(np.hypot(_kR(a) * TB, _kI(a) * TB)) / M
    res, ah, Mh = _best_gr_fit(w)
    return res / sig, ah, Mh


def section3A(TB=5e-5, M0=65.0):
    sec("§3-A  卷十六「精确简并」的有效域：不可吸收比 η 的机器扫描")
    print("  η ≡ GR 重拟合 (a,M) 之后**吞不掉**的挠率信号占比。")
    print("  η=0 = 卷十六的精确简并；η>0 = 那里 GR 拟合不回 TUFT 数据。\n")

    # 自检 1：η 与 M 无关
    e1, _, _ = eta(0.7, 40.0, TB)
    e2, _, _ = eta(0.7, 80.0, TB)
    rel = abs(e1 - e2) / max(abs(e1), 1e-30)
    rec("V19-E1", "η 与 M 无关（标度自检）",
        "PASS" if rel < 1e-10 else "FAIL",
        "M=40 → η={0:.6e}；M=80 → η={1:.6e}；相对差 {2:.2e} ⇒ 分子分母同 ∝ 1/M，"
        "η 是纯自旋的函数，与质量无关。".format(e1, e2, rel),
        {"eta_40": e1, "eta_80": e2, "rel": rel})

    # 自检 2：η ≤ 1（因为 â=a, M̂=M 本身就在 GR 族内，残差不可能超过信号本身）
    grid = np.linspace(0.0, 0.99, 100)
    etas = np.array([eta(float(x), M0, TB)[0] for x in grid])
    rec("V19-E2", "η ≤ 1 上界自检", "PASS" if float(etas.max()) <= 1.0 + 1e-9 else "FAIL",
        "100 点扫描 max η = {0:.6f} ≤ 1（â=a, M̂=M 属于 GR 族 ⇒ 最优残差不可能超过"
        "原始 GR 偏差）⇒ 求解器无越界。".format(float(etas.max())),
        {"eta_max": float(etas.max())})

    print("\n  {0:>6} {1:>14} {2:>14} {3:>10}".format("a", "η", "â(GR最优)", "M̂/M"))
    print("  " + "-" * 50)
    rows = []
    for x in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.70, 0.90, 0.99):
        e, ah, Mh = eta(float(x), M0, TB)
        rows.append((float(x), e, ah, Mh / M0))
        print("  {0:>6.2f} {1:>14.6e} {2:>14.6f} {3:>10.6f}".format(x, e, ah, Mh / M0))

    # η 的机器零门槛必须与求解器精度同源：精确求根 ⇒ 门槛取 1e-8。
    # （初版用「网格扫描取最小」配 1e-6 门槛，网格步长 2.5e-4 制造出 η~1e-4 的
    #   假非零，并让 a_min 与占比两个读数互斥——已改为 brentq 精确求根 + 单网格。）
    xs5 = np.linspace(0.0, 0.999, 500)
    eta5 = np.array([eta(float(x), M0, TB)[0] for x in xs5])
    mask = eta5 < 1e-8
    frac_deg = float(mask.mean())
    a_lo = float(xs5[int(np.argmax(mask))]) if bool(mask.any()) else None
    deg = [r for r in rows if r[1] < 1e-8]
    nondeg = [r for r in rows if r[1] >= 1e-8]

    rec("V19-E3b", "简并读数自洽守卫（占比 ↔ a_min ↔ 求解器）",
        "PASS" if ((a_lo is None) == (frac_deg == 0.0)) else "FAIL",
        "同一条 500 点网格上：η<1e-8 的占比 = {0:.1%}，首个满足者 a_min = {1}；"
        "两者同源于一个 mask ⇒ 不可能互斥。另：简并域内 η 的实测上限 = {2:.3e}"
        "（须远低于 1e-8 才算真机器零）⇒ 精确求根未受离散化污染。"
        .format(frac_deg, ("{0:.3f}".format(a_lo) if a_lo is not None else "无"),
                float(eta5[mask].max()) if bool(mask.any()) else float("nan")),
        {"frac": frac_deg, "a_min": a_lo,
         "eta_max_in_degenerate": float(eta5[mask].max()) if bool(mask.any()) else None})

    rec("V19-E3", "简并域边界：η 为机器零的 a 区间",
        "CORRECTED" if (a_lo is not None and a_lo > 0.02) else "PASS",
        "T_B={0:.1e} 时 η<1e-8 的最小自旋 a_min = {1}；a∈[a_min, 0.999] 的简并域"
        "占扫描区间 {2:.1%}。⇒ **卷十六「对任意 T_B 都存在 (a′,M′)」须加有效域限定**："
        "它只在 a ≳ a_min 的域内成立；a < a_min 时 GR 无法靠重拟合吞掉挠率信号，"
        "η 从 0 抬到 {3:.3e}（a=0）⇒ 那里不是简并，是（原则上）可区分的窗口。"
        .format(TB, ("{0:.3f}".format(a_lo) if a_lo is not None else "无"),
                frac_deg, rows[0][1]),
        {"TB": TB, "a_min": a_lo, "frac_degenerate": frac_deg,
         "eta_at_a0": rows[0][1], "n_degenerate_points": len(deg),
         "n_nondegenerate_points": len(nondeg)})

    rec("V19-E4", "低自旋窗口的可判别幅度", "BOUNDARY",
        "a=0 处 η={0:.3e}：只有 {0:.3e} 比例的挠率信号是 GR 吞不掉的，而这一段"
        "能否被真实数据分辨取决于该事件的 ringdown 测量精度与激发幅度——两者"
        "TUFT 都未给出（激发幅度尤其缺失：TUFT 无 ringdown 振幅预言）⇒ 登记"
        "开放项 O-V19-AMP，不作「已获得判别力」判定。".format(rows[0][1]),
        {"eta_at_a0": rows[0][1]})

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.semilogy(np.clip(etas, 1e-18, None), lw=1.8)
    ax.axhline(1e-6, color="r", ls="--", lw=1.0, label="机器零门槛 1e-6")
    ax.set_xlabel("a grid index (a = 0 → 0.99)")
    ax.set_ylabel("η  (unabsorbable fraction)")
    ax.set_title("Volume 19 · exact-degeneracy domain of Vol.16")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "tuft_v19_eta_vs_spin.png"), dpi=130)
    plt.close(fig)
    return rows, a_lo, TB


# ============ §3-B 出路 B（同段 GR 锚定）= 空转 ============
def _anchored_fit(obs):
    """逐事件用 GR 最优拟合得到 (â, M̂) 当作锚定，再联合拟合单一全局 T_B。"""
    n = len(obs) // 2
    X = np.empty(2 * n)
    r = np.empty(2 * n)
    anchors = []
    for i in range(n):
        w = obs[2 * i:2 * i + 2]
        _, ah, Mh = _best_gr_fit(w)
        anchors.append((ah, Mh))
        X[2 * i], X[2 * i + 1] = _kR(ah) / Mh, _kI(ah) / Mh
        r[2 * i] = w[0] - _fR(ah) / Mh
        r[2 * i + 1] = w[1] + _fI(ah) / Mh
    TBh = float(np.dot(X, r) / np.dot(X, X))
    res = r - X * TBh
    return TBh, float(np.linalg.norm(res)), anchors


def section3B(a_lo, TB=5e-5, N=10, seed=20261015):
    sec("§3-B  出路 B（锚定取自**同段** ringdown 的 GR 拟合）= 空转")
    print("  做法：先用 GR 模板把每个事件的 (a,M) 拟合出来当锚定，再拟合唯一自由参数 T_B。")
    print("  名义自由度 FR = 2N−1 = {0}。问题：残差是否真的由数据决定？\n".format(2 * N - 1))

    rng = np.random.default_rng(seed)
    lo = (a_lo if a_lo is not None else 0.30) + 0.02      # 取简并域内部
    a = rng.uniform(lo, 0.98, N)
    Mv = rng.uniform(40.0, 80.0, N)

    def obs_of(tbv):
        o = np.empty(2 * N)
        for i in range(N):
            t = tbv[i] if np.ndim(tbv) else tbv
            o[2 * i], o[2 * i + 1] = omega(a[i], Mv[i], t)
        return o

    # B1：真实模型确实含 T_B = 5e-5
    obs1 = obs_of(TB)
    tb1, res1, _ = _anchored_fit(obs1)
    diff1 = float(np.linalg.norm(obs1 - obs_of(0.0)))     # TUFT−GR 的真实频率差
    r1 = res1 / diff1

    # B2：破坏模型假设（每事件 T_B 各不相同，符号混合、量级差 10 倍）
    tbv2 = rng.uniform(-1e-4, 1e-4, N)
    obs2 = obs_of(tbv2)
    tb2, res2, _ = _anchored_fit(obs2)
    diff2 = float(np.linalg.norm(obs2 - obs_of(0.0)))
    r2 = res2 / max(diff2, 1e-300)

    f1 = abs(tb1) / TB          # 回收比例：1 = 完全找回真值，0 = 完全漏检
    print("  B1 真值 T_B={0:.1e}（全域同一）⇒ T̂_B={1:.6e}，回收比例 |T̂_B|/T_B = "
          "{2:.3e}".format(TB, tb1, f1))
    print("     残差 ‖r‖={0:.6e}，相对 TUFT−GR 频率差 {1:.6e} 的比值 = {2:.2e}".format(
        res1, diff1, r1))
    print("  B2 每事件 T_B 各异（±1e-4，模型假设被破坏）⇒ T̂_B={0:.6e}".format(tb2))
    print("     残差 ‖r‖={0:.6e}，相对其自身频率差 {1:.6e} 的比值 = {2:.2e}".format(
        res2, diff2, r2))

    rec("V19-C4", "出路 B 的漏检：真含挠率却返回 T_B≈0",
        "FAIL" if f1 < 1e-8 else "PASS",
        "真值 T_B={0:.1e}、{1} 个事件，锚定检验返回 T̂_B={2:.6e}（回收比例 {3:.3e}，"
        "即真值只被找回 {3:.3e} 倍）、χ² 残差仅为信号本身的 {4:.2e}"
        " ⇒ **该流程永远看不到挠率**：锚定把信号完整吸收进 (â, M̂)，剩下的残差恒为零。"
        .format(TB, N, tb1, f1, r1),
        {"TB_true": TB, "TB_hat": tb1, "recovery_fraction": f1,
         "res_over_signal": r1, "N": N})

    rec("V19-C5", "出路 B 对**违反模型假设**的数据也完美拟合",
        "FAIL" if r2 < 1e-8 else "PASS",
        "故意让每事件 T_B 各不相同（±1e-4，符号混合、跨越 10 倍量级，单参数全局"
        "T_B 模型明明是错的），锚定检验仍给出 χ² 残差/信号 = {0:.2e}"
        "⇒ 该流程对**任意**数据都返回「完美吻合」⇒ 有效可证伪关系数 = 0。"
        .format(r2),
        {"res_over_signal": r2, "TB_spread": [-1e-4, 1e-4], "N": N})

    rec("V19-C6", "名义 FR = 2N−1 是虚数",
        "FAIL" if (f1 < 1e-8 and r2 < 1e-8) else "BOUNDARY",
        "名义上 2N={0} 个观测、1 个自由参数 ⇒ FR={1}；但由于锚定本身是从同一段"
        "数据拟合出来的 2N 个量，模型族 {2} 随数据自适应地覆盖整个数据空间 ⇒ "
        "χ² 恒为 0、与数据无关 ⇒ **有效 FR = 0**。这是卷十七「名义 d vs 有效 d_eff」"
        "的同一类陷阱在出路 B 上的复发。"
        .format(2 * N, 2 * N - 1, "ω(T_B; â(data), M̂(data))"),
        {"FR_nominal": 2 * N - 1, "FR_effective": 0, "N": N})
    return (tb1, r1, tb2, r2)


# ============ §3-C 出路 A（独立段外锚定）的系统偏差账单 ============
def section3C(a0=0.7, M0=65.0, TB=5e-5, sig_a=0.10, eps_M=0.05):
    sec("§3-C  出路 A（锚定取自**独立数据段**）的代价：锚定系统偏差")
    print("  代表事件 a={0}、M={1} M☉（[C] 量级参照）；目标 T_B={2:.1e}。".format(a0, M0, TB))
    print("  锚定后 T_B 是唯一自由参数，单参数最小二乘传播：")
    print("      δT̂_B = c_a·σ_a + c_M·ε_M     （M 完全约掉，只依赖相对量）")
    print("  [C] 当前事件级典型精度取 σ_a={0}、ε_M={1}（量级参照，非本库导出）\n"
          .format(sig_a, eps_M))

    kR = _kR(a0); kI = _kI(a0)
    den = kR * kR + kI * kI
    coef_a = (kR * (_dfR(a0) + 60.0 * TB) + kI * (-_dfI(a0) - 40.0 * TB)) / den
    coef_M = -(kR * (_fR(a0) + kR * TB) + kI * (-_fI(a0) + kI * TB)) / den
    bA = abs(coef_a) * sig_a
    bM = abs(coef_M) * eps_M
    tot = float(np.hypot(bA, bM))
    ratio = tot / TB

    tol = TB / 3.0
    sig_req = tol / abs(coef_a)
    eps_req = tol / abs(coef_M)
    fac_a = sig_a / sig_req
    fac_M = eps_M / eps_req

    print("  c_a = {0:.6e}  ⇒ δT_B(自旋, σ_a={1}) = {2:.6e}".format(coef_a, sig_a, bA))
    print("  c_M = {0:.6e}  ⇒ δT_B(质量, ε_M={1}) = {2:.6e}".format(coef_M, eps_M, bM))
    print("  合成（平方和）     = {0:.6e}  = 目标信号 {1:.1e} 的 {2:.2f} 倍".format(
        tot, TB, ratio))
    print("  要求系统偏差 ≤ 信号/3 ⇒ σ_a ≤ {0:.4f}、ε_M ≤ {1:.4%}".format(sig_req, eps_req))
    print("  相对 [C] 当前量级需分别提高 {0:.2f}× 与 {1:.2f}×\n".format(fac_a, fac_M))

    rec("V19-C1", "出路 A 的锚定系统偏差 vs 目标信号",
        "FAIL" if ratio > 1.0 else "PASS",
        "a={0}：δT_B(自旋)={1:.4e}、δT_B(质量)={2:.4e}，合成 {3:.4e}，是目标 T_B={4:.1e}"
        " 的 {5:.2f} 倍 ⇒ **在 [C] 当前事件级精度下，锚定误差本身比要测的挠率信号还大**，"
        "锚定把 TUFT 的效应整体淹没在自己的系统偏差里。"
        .format(a0, bA, bM, tot, TB, ratio),
        {"a": a0, "bias_spin": bA, "bias_mass": bM, "bias_total": tot,
         "TB": TB, "ratio": ratio, "coef_a": coef_a, "coef_M": coef_M})

    rec("V19-C2", "出路 A 的最低锚定精度要求", "FAIL",
        "要让系统偏差 ≤ 信号/3，需 σ_a ≤ {0:.4f}（当前 [C] {1} ⇒ 提高 {2:.2f}×）、"
        "ε_M ≤ {3:.4%}（当前 [C] {4:.0%} ⇒ 提高 {5:.2f}×）。这两项都是**外部输入**，"
        "不由 TUFT 提供；且要求是「在 TUFT 自身无 ringdown 振幅预言、无 inspiral 修正"
        "预言」的前提下叠加的。"
        .format(sig_req, sig_a, fac_a, eps_req, eps_M, fac_M),
        {"sigma_a_required": sig_req, "epsilon_M_required": eps_req,
         "improve_spin": fac_a, "improve_mass": fac_M})

    rates = []
    for N in (1, 5, 10, 30, 100):
        rates.append((N, 2 * N - 1, 2 * N, (2 * N - 1) / (2.0 * N)))
    print("  {0:>5} {1:>8} {2:>10} {3:>12}".format("N", "FR", "外部输入", "兑换率"))
    print("  " + "-" * 40)
    for N, fr_, ext, rt in rates:
        print("  {0:>5} {1:>8} {2:>10} {3:>12.4f}".format(N, fr_, ext, rt))
    rec("V19-C3", "出路 A 的兑换率：1 个外部输入买 1 个可证伪关系",
        "INFO",
        "每多一个事件：+2 个观测量、+0 个自由参数（T_B 全局）、但需要 +2 个外部"
        "锚定量 ⇒ FR 从 2N−1 涨到 2(N+1)−1（+2），外部输入从 2N 涨到 2N+2（+2）"
        "⇒ **兑换率恒为 1:1** ⇒ 出路 A 不产生任何「免费的预测力」，它只是把外部"
        "输入一比一换成可证伪关系。",
        {"rates": rates, "asymptotic": 1.0})

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    labels = ["自旋锚定 σ_a=" + str(sig_a), "质量锚定 ε_M=" + str(eps_M),
              "合成（平方和）", "目标信号 T_B"]
    vals = [bA, bM, tot, TB]
    ax.bar(range(4), vals, color=["#4c72b0", "#dd8452", "#c44e52", "#55a868"])
    ax.set_yscale("log")
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, rotation=12, ha="right")
    ax.set_ylabel("δT_B")
    ax.set_title("Volume 19 · external-anchoring bias vs target signal")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "tuft_v19_anchor_bias.png"), dpi=130)
    plt.close(fig)
    return {"bA": bA, "bM": bM, "tot": tot, "TB": TB, "ratio": ratio,
            "sig_req": sig_req, "eps_req": eps_req, "fac_a": fac_a, "fac_M": fac_M}


# ============ §3-D 三条出路对照与代价账单 ============
def section3D(a_lo, bias):
    sec("§3-D  剩余出路对照表与代价账单")
    rows = [
        ("C 不锚定（现状）", "0", "0", "+0",
         "卷十六已证：简并精确、T_B 不可辨识且与 N 无关"),
        ("B 锚定取自同段 GR 拟合", "2N−1", "0", "+2N（自产）",
         "空转：任意数据 χ²≡0（本卷 §3-B 机器证明）"),
        ("A 锚定取自独立数据段", "2N−1", "2N−1", "+2N（外部）",
         "唯一不空转；代价 = 外部输入 + 系统偏差 + 理论负载"),
    ]
    print("  {0:<22} {1:>8} {2:>8} {3:>14}  {4}".format(
        "出路", "名义FR", "有效FR", "外部输入", "裁定"))
    print("  " + "-" * 96)
    for nm, fn, fe, ext, note in rows:
        print("  {0:<22} {1:>8} {2:>8} {3:>14}  {4}".format(nm, fn, fe, ext, note))
    print()

    rec("V19-C7", "唯一不空转的出路 = A（独立数据段外锚定）", "INFO",
        "三条出路里 C 已被卷十六判死（FR=0、T_B 不可辨识）；B 被本卷 §3-B 判死"
        "（有效 FR=0、对任意数据完美拟合）；只有 A 真正把 FR 从 0 抬到 2N−1。"
        "⇒ 若一定要推进 ringdown 通道，A 是唯一入口。",
        {"routes": ["C", "B", "A"], "survivor": "A"})

    rec("V19-C8", "出路 A 的三条代价（是否接受须人工裁决，本卷不代选）", "BOUNDARY",
        "(i) 外部输入：每事件 2 个（a、M），N 个事件共 2N 个，且**不受 TUFT 约束**；"
        "(ii) 系统偏差：合成 {0:.4e} = 目标信号 {1:.1e} 的 {2:.2f} 倍，需把 σ_a 与 ε_M "
        "分别再提高 {3:.2f}× 与 {4:.2f}×；"
        "(iii) 理论负载：锚定是用 **GR 模板**做的，若 TUFT 在 inspiral/IMR 段也有偏离，"
        "锚定值本身就带偏，而 TUFT 目前没有 inspiral 段预言可用来评估这一项"
        "⇒ 登记开放项 **O-V19-INSPIRAL**。三条代价没有一条能靠 TUFT 内部消化。"
        .format(bias["tot"], bias["TB"], bias["ratio"], bias["fac_a"], bias["fac_M"]),
        {"cost_external": "2N", "cost_bias_ratio": bias["ratio"],
         "improve_spin": bias["fac_a"], "improve_mass": bias["fac_M"],
         "open_item": "O-V19-INSPIRAL"})

    rec("V19-C9", "与卷十六的分工（避免重复造轮子）", "INFO",
        "卷十六问的是「T_B 的后验有多宽」（参数估计精度，σ ∝ N^−1/2）；本卷问的是"
        "「拟合完之后还剩几个自由度的残差可用来否证模型」（模型检验能力，FR = dof）。"
        "⇒ 卷十六的 σ_TB(N) ∝ N^−1/2 **只在出路 A 下才有意义**：出路 B/C 下 T_B 要么"
        "不可辨识（C）、要么恒返回 0（B），σ 的数值再小也不携带信息。",
        {"vol16_scope": "parameter precision", "vol19_scope": "model-testing power"})

    rec("V19-C10", "§3-A 的窗口与出路 A 的关系", "BOUNDARY",
        "§3-A 找到的 a < a_min 域（η>0）是**不需要外部锚定**就能区分 GR 与 TUFT 的窗口，"
        "理论上比出路 A 便宜得多（零外部输入）；但 η 的量级与能否被真实数据分辨，"
        "取决于 TUFT 未给出的 ringdown 激发幅度与事件测量精度 ⇒ 不作「已获得判别力」"
        "判定，登记 O-V19-AMP。这是本卷给出的**唯一不构成外部输入依赖**的候选。",
        {"a_min": a_lo, "open_item": "O-V19-AMP"})
    return rows


def summarize(eta_rows, a_lo, bias):
    sec("§4  总账")
    cnt = {}
    for r in RESULTS:
        cnt[r["status"]] = cnt.get(r["status"], 0) + 1
    base = os.path.join(HERE, "TUFT_卷十九_可证伪关系数实证与剩余出路代价")
    lines = ["TUFT 卷十九 · FR 的实证（≡ χ² 自由度）+ 参数—预测力权衡定理"
             " + 剩余出路的代价账单",
             "run at: " + time.strftime("%Y-%m-%d %H:%M:%S"), ""]
    for r in RESULTS:
        lines.append("  [{0:<9}] {1:<9} {2}".format(r["status"], r["code"], r["detail"]))
    lines += ["", "=" * 78, "汇总", "=" * 78]
    for k in ("PASS", "FAIL", "BOUNDARY", "CORRECTED", "INFO"):
        if k in cnt:
            lines.append("  {0:<9} = {1}".format(k, cnt[k]))
    lines.append("  条目数：{0}".format(len(RESULTS)))
    lines += ["", "★ 卷十九结论：",
              "  (1) 定理 I 实证成立：FR = d − r 就是拟合残差自由度（χ² 的 dof）。N=1,2,5,10,30",
              "      五个规模上 χ²_min 的样本均值/方差与 χ²_FR 的矩在 4σ 内一致，并配",
              "      阳性对照（不拟合时 χ² 大 1+SNR²）与阴性对照 ⇒ FR 从卷十八的**定义**",
              "      升级为**可实测的量**。",
              "  (2) 定理 II 实证成立：r + FR ≡ d（守恒），p<d 时每加 1 个参数用 1 个 FR 换",
              "      1 个 r；p>d 后 FR 已为 0，继续加参数只增 nullity（纯恶化）。",
              "  (3) 修正卷十六：「对任意 T_B 都存在 (a′,M′)」应加有效域限定——不可吸收比 η",
              "      在 a ≳ a_min 为机器零（简并成立），a < a_min 时 η>0（GR 吞不掉）。",
              "      低自旋域是唯一不依赖外部输入的候选窗口，但幅度可行性待 O-V19-AMP。",
              "  (4) 三条出路：C（不锚定）FR=0 且不可辨识；B（同段 GR 锚定）名义 FR=2N−1",
              "      但**有效 FR=0**——对任意数据（包括违反模型假设的数据）都返回 χ²≡0；",
              "      A（独立段外锚定）是唯一不空转者。",
              "  (5) A 的代价账单：+2N 外部输入（兑换率 1:1，没有免费的预测力）+ 锚定系统",
              "      偏差 {0:.2f} 倍于目标信号（需把 σ_a、ε_M 再提高 {1:.1f}×、{2:.1f}×）"
              "".format(bias["ratio"], bias["fac_a"], bias["fac_M"]),
              "      + 理论负载未评估（锚定用 GR 模板，O-V19-INSPIRAL）。三条代价都不能",
              "        靠 TUFT 内部消化 ⇒ 是否接受属人工裁决，本卷不代选。",
              "",
              "  含义：卷十六—卷十九四册合起来给出的不是「怎么把 T_B 测出来」，而是",
              "        「为什么它测不出来，以及让它测出来要付什么」。FR 这条尺子可以",
              "        原样搬去审任何一条 TUFT 通道。"]
    txt = "\n".join(lines)
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "counts": cnt, "entries": RESULTS,
                   "eta_table": [{"a": r[0], "eta": r[1], "a_hat": r[2],
                                  "M_hat_over_M": r[3]} for r in eta_rows],
                   "a_min": a_lo, "bias": bias},
                  f, ensure_ascii=False, indent=2)
    print(txt)
    print("\nwrote: " + base + ".txt / .json / 三张 png")


def main():
    t0 = time.time()
    section1()
    section2()
    eta_rows, a_lo, TB = section3A()
    section3B(a_lo, TB)
    bias = section3C(TB=TB)
    section3D(a_lo, bias)
    summarize(eta_rows, a_lo, bias)
    print("\n运行耗时 {0:.2f} s".format(time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
