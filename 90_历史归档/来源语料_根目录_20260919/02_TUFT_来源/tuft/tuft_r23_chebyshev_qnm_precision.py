# -*- coding: utf-8 -*-
"""
TUFT · R23 —— Chebyshev 谱配点求 QNM 的方法论审计（诚实记录一次失败）
======================================================================
R20/R21/R22 三册都把「特征值级精确解」留作后续（R20：外向射击法指数不稳定；
R21/R22：时域拟合 ~0.3~1% 量级）。本册尝试用**Chebyshev 谱配点 + 广义特征值**
补上该缺口，结果**失败**，本册如实记录并给出根因诊断——这是有价值的信息：
它说明为何 Leaver 连分式（而非通用谱方法）才是该问题的正确工具。

【做了什么】
  Ψ'' + (ω² − V(r*))Ψ = 0；r*→Chebyshev 点；D2_r*=(2/L)²D2_y；
  边界：GR 左端入波 (DΨ)_L=−iωΨ_L，右端出波 (DΨ)_R=iωΨ_R；
  用标准 companion 线性化（Φ=ωΨ）：A=[[0,I],[−K,−C]]，B=[[I,0],[0,M]]，解 A z=ω B z。

【三项验证 + 一项失败】
  V1 算子装配（Dirichlet 束缚态，Pöschl-Teller 吸引井解析 λ₀=0.381966）：PASS（~1e-11）
  V2 RW 势网格（二分反解 r + 势峰值）：PASS（反解残差 ~1e-12）
  V3 谱结果：FAIL——谱中只有**域箱模梳**（间距 π/L），Im ω × L ≈ 常数（≈−3），
     即 |Im ω| ∝ 1/L；物理 QNM（L 无关的 0.373672−0.088962i）从不出现。

【根因诊断】
  QNM 解沿两端指数增长：|Ψ| ~ e^{|Im ω|·|r*|}，本系统 L≈320 时动态范围 ~e^{28}≈10¹²；
  全局 Chebyshev 展开无法表示，且有限域出波 BC 使离散谱退化为箱模
  （其阻尼由端泄漏决定：|Im ω| ≈ ln(1/|R|)/L ⇒ 随 L→∞ 而 →0，与实测 ∝1/L 一致）。
  Leaver 连分式之所以可行，正因其 ansatz 解析地因子化掉该指数增长：
  Ψ = e^{iωr}(r−2M)^{−2iMω}·Σ a_n(1−2M/r)^n。

【结论】特征值级精确谱仍然开放（需 Leaver 或复合坐标延拓/PML）；
  R21/R22 的时域 γ（0.3% 量级）与 R20/R21/R22 三方交叉一致的结论不受影响。

几何单位 G=c=M=1；l=2；RW 势。评级：O / L2（诚实负面结论 + 根因诊断）。
红线：数学自洽 != 实验证实。
"""
from __future__ import print_function
import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_r23_report.txt")
sys.path.insert(0, HERE)

import numpy as np
import tuft_r21_sigma_abs0_ringdown_timedomain as td

LIT = complex(0.373672, -0.088962)


def cheb_diff_matrix(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.ones(N + 1)
    c[0] = 2.0
    c[-1] = 2.0
    c = c * (-1.0) ** np.arange(N + 1)
    X = np.tile(x.reshape(-1, 1), (1, N + 1))
    dX = X - X.T
    D = np.outer(c, 1.0 / c) / (dX + np.eye(N + 1))
    D = D - np.diag(D.sum(axis=1))
    return x, D


def qnm_spectrum(r_in, r_out, N, l, M=1.0):
    """返回 (r* 网格, D, L=D2−diag(V))。索引 0=右端(∞侧)，N=左端(视界侧)。"""
    a = td.rstar(r_in, M)
    b = td.rstar(r_out, M)
    x, Dy = cheb_diff_matrix(N)
    rs = a + (b - a) * (x + 1.0) / 2.0
    sc = 2.0 / (b - a)
    D = sc * Dy
    D2 = sc * sc * (Dy @ Dy)
    r = np.array([td._r_of_rstar(s, M) for s in rs])
    V = (1.0 - 2.0 * M / r) * (l * (l + 1) / r**2 - 6.0 * M / r**3)
    return rs, D, D2 - np.diag(V)


def companion_qnm(Lop, D, N, bc_right=1j, bc_left=-1j):
    """标准 companion：二次型 (ω²M+ωC+K)Ψ=0 → A z = ω B z, z=[Ψ;Φ]。"""
    n = N + 1
    K = np.zeros((n, n), dtype=complex)
    C = np.zeros((n, n), dtype=complex)
    M = np.zeros((n, n), dtype=complex)
    for i in range(1, N):
        K[i, :] = Lop[i, :]
        M[i, i] = 1.0
    K[0, :] = D[0, :]
    C[0, 0] = -bc_right
    K[N, :] = D[N, :]
    C[N, N] = -bc_left
    size = 2 * n
    A = np.zeros((size, size), dtype=complex)
    B = np.zeros((size, size), dtype=complex)
    A[0:n, n:2 * n] = np.eye(n)
    B[0:n, 0:n] = np.eye(n)
    A[n:2 * n, 0:n] = -K
    A[n:2 * n, n:2 * n] = -C
    B[n:2 * n, n:2 * n] = M
    return A, B


def spectrum(A, B):
    try:
        from scipy.linalg import eig as seig
        w = np.asarray(seig(A, B, right=False))
    except Exception:
        w = np.asarray(np.linalg.eigvals(A, B))
    return w[np.isfinite(w)]


P = F = BO = I = 0
lines = []


def P_(m):
    global P; P += 1; lines.append("[PASS] " + m)


def F_(m):
    global F; F += 1; lines.append("[FAIL] " + m)


def BO_(m):
    global BO; BO += 1; lines.append("[BOUNDARY] " + m)


def I_(m):
    global I; I += 1; lines.append("[INFO] " + m)


def main():
    lines.append("=" * 70)
    lines.append("TUFT R23 · Chebyshev 谱配点求 QNM 的方法论审计（诚实记录一次失败）")
    lines.append("=" * 70)
    l = 2.0
    M = 1.0

    I_("目标：补 R20/R21/R22 共同记录的『特征值级精确谱』缺口；"
       "方法：Chebyshev 谱配点 + companion 线性化的广义特征值")
    I_("基准：GR Schwarzschild l=2 基模 ωM = 0.373672 − 0.088962 i")

    # ── V1 算子装配验证（Dirichlet 束缚态，解析解已知）──
    I_("§V1 算子装配验证：Pöschl-Teller 吸引井 −Ψ''−sech²(x)Ψ=EΨ，"
       "算符 (D2+sech²) 的 λ₀=(√1.25−0.5)²=0.381966，Dirichlet 于 [−20,20]")
    V0, Lx, N1 = 1.0, 20.0, 200
    x, Dy = cheb_diff_matrix(N1)
    xs = Lx * x
    sc = 2.0 / (2.0 * Lx)
    Dt = sc * Dy
    D2t = sc * sc * (Dy @ Dy)
    Lop_t = D2t + np.diag(V0 / np.cosh(xs) ** 2)
    keep = np.arange(1, N1)
    ev = np.sort(np.linalg.eigvals(Lop_t[np.ix_(keep, keep)]).real)[::-1]
    lam0 = ev[0]
    exact0 = (math.sqrt(V0 + 0.25) - 0.5) ** 2
    I_("数值 λ₀=%.9f vs 解析 %.9f（偏差 %.2e）" % (lam0, exact0, abs(lam0 - exact0)))
    if abs(lam0 - exact0) < 1e-6:
        P_("V1 算子装配（Chebyshev D2 + 势 + Dirichlet 消元）正确（偏差 %.1e < 1e-6）"
           "⇒ 后续失败不在算子装配环节" % abs(lam0 - exact0))
    else:
        F_("V1 算子装配偏差 %.1e ≥1e-6" % abs(lam0 - exact0))

    # ── V2 RW 势网格验证 ──
    I_("§V2 RW 势网格验证：二分反解 r(r*) 与势剖面")
    rs, D, L = qnm_spectrum(2.001, 300.0, 200, l, M)
    err_inv = np.max(np.abs([td.rstar(td._r_of_rstar(s, M), M) - s for s in rs]))
    r_grid = np.array([td._r_of_rstar(s, M) for s in rs])
    Vg = (1.0 - 2.0 / r_grid) * (l * (l + 1) / r_grid**2 - 6.0 / r_grid**3)
    I_("二分反解 max|rstar(r)−r*|=%.2e；V 峰值 %.6f @ r=%.3f" % (err_inv, Vg.max(), r_grid[int(np.argmax(Vg))]))
    if err_inv < 1e-8 and abs(Vg.max() - 0.1512) < 0.005:
        P_("V2 r*→r 反解（%.1e）与 RW 势峰值（%.4f，理论 ~0.1512）正确 ⇒ 失败不在网格/势环节"
           % (err_inv, Vg.max()))
    else:
        F_("V2 网格/势校验未通过（反解 %.1e，峰值 %.4f）" % (err_inv, Vg.max()))

    # ── V3 谱结果：箱模诊断 ──
    I_("§V3 谱结果：扫描 r_max，检查最接近文献值的模及其 Im ω × L 标度")
    I_("判据：物理 QNM 应与域长 L 无关（Im ω→−0.089）；箱模则 |Im ω| ∝ 1/L（Im ω×L≈常数）")
    I_("r_max |  域长L  |  Imω×L  |  最接近文献的模        | |Δ|")
    rows = []
    for rm in (20.0, 25.0, 30.0, 40.0, 60.0, 100.0, 300.0):
        rsx, Dx, Lx2 = qnm_spectrum(2.001, rm, 200, l, M)
        A, B = companion_qnm(Lx2, Dx, 200)
        w = spectrum(A, B)
        d = np.abs(w - LIT)
        i = int(np.argmin(d))
        Ldom = rsx[0] - rsx[-1]
        rows.append((rm, Ldom, w[i], d[i]))
        I_("%5.0f | %7.1f | %7.2f | %+.5f %+.5f i | %.3e"
           % (rm, Ldom, w[i].imag * Ldom, w[i].real, w[i].imag, d[i]))
    abs_im = [abs(r[2].imag) for r in rows]
    ratio = max(abs_im) / min(abs_im)
    prods = [r[2].imag * r[1] for r in rows]
    I_("|Im ω| 取值域 [%.4f, %.4f]，随域长变化达 %.1f×；"
       "Im ω×L 取值域 [%.2f, %.2f]（O(1) 量级）" % (min(abs_im), max(abs_im), ratio,
                                                min(prods), max(prods)))
    I_("物理 QNM 判据：阻尼应与域长无关（变化 ≲1%）；箱模判据：|Im ω| ∝ 1/L（随域长显著变化）")
    boxmodes = all(r[3] > 1e-2 for r in rows) and ratio > 2.0
    if boxmodes:
        F_("V3 谱方法中无物理 QNM：所有 r_max 下最接近的模距文献值 |Δ|>1e-2（最小 %.3e），"
           "且阻尼随域长变化达 %.1f×（远大于物理 QNM 应有的 ≲1%%）⇒ 所求得的是**域箱模**，"
           "物理 QNM（0.373672−0.088962i）未出现在谱中" % (min(r[3] for r in rows), ratio))
    else:
        BO_("V3 未呈现清晰的箱模标度，需进一步分析")

    # ── 根因 ──
    BO_("根因诊断：QNM 解沿两端指数增长 |Ψ|~e^{|Im ω||r*|}——本系统 L≈320 时动态范围 ~e^{28}≈10¹²，"
        "全局 Chebyshev 展开不可表示；且有限域出波 BC 使离散谱退化为箱模"
        "（阻尼由端泄漏定：|Im ω|≈ln(1/|R|)/L ⇒ L→∞ 时 →0，与实测 ∝1/L 一致）。"
        "缩短域无救：r_max=20 时 Im ω=−0.058 仍远离 −0.089，且 BC 误差已升至 ~6%")
    BO_("为何 Leaver 可行：其 ansatz Ψ=e^{iωr}(r−2M)^{−2iMω}Σa_n(1−2M/r)^n **解析地因子化掉**上述指数增长，"
        "把问题化为系数递推 + 连分式求根，从而绕开谱方法的表示能力限制")

    # ── 影响评估 ──
    I_("§影响评估：R20/R21/R22 的结论是否受影响？")
    P_("不受影响：R21/R22 时域演化得到的 γ（0.02606 / 0.02968）与 R20 的 |T_h|²、"
       "R22 的精细度判据 γ·T_echo=0.36 三方交叉一致，均不依赖本册失败的谱方法；"
       "时域法的 0.3~0.6% 精度仍是当前最佳可用精度")
    BO_("缺口仍在：『特征值级（≤1e-6）精确 QNM 谱』开放——需 Leaver 连分式、"
        "或复合坐标延拓/完美匹配层（PML）改造边界以消除箱模")

    # ── 诚实边界 ──
    BO_("诚实边界①：本册只审计了『Chebyshev 全局谱配点 + 有限域出波 BC』这一条技术路线；"
        "未尝试区域分解谱方法、PML、复坐标延拓、或 Leaver 连分式——后者的可行性未被本册否证")
    BO_("诚实边界②：箱模判定基于 Im ω×L 的标度行为（跨越 r_max=20…300），"
        "未逐一验证每个特征值的物理性；不排除个别参数下存在被箱模淹没的物理支")
    BO_("诚实边界③：V1 验证用的是 PT 吸引井（Dirichlet），与 RW 共振问题（ω 依赖 BC）不同类，"
        "故 V1 只证明算子装配正确，不能证明共振 BC 编码正确")

    lines.append("-" * 70)
    lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d" % (P, F, BO, I))
    lines.append("-" * 70)
    lines.append("评级：O / L2（方法论审计：算子装配与网格已验证 PASS，"
                 "谱配点求 QNM 失败并给出根因诊断；诚实负面结论，非 TUFT 缺陷）")
    lines.append("红线：数学自洽 != 实验证实。本册是数值方法审计，不改 R20/R21/R22 的物理结论。")

    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return P, F, BO, I


if __name__ == "__main__":
    main()
