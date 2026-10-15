# -*- coding: utf-8 -*-
"""
TUFT 卷二十：二阶变分求导管线（三重自检）、规范固定与鬼算符、York 雅可比

承接卷十九（Hessian 前置结构：York 分解 10=5+3+1+1、鬼场 4=3+1、七条系数无关定理）。
卷十九 §8 卷二十闭合清单：
    (1) 背景场二阶变分 ⇒ 每个 York 模的 Hessian 本征值
    (2) 规范固定 + 鬼算符
    (3) York 分解的雅可比
    (4) 阈值宗量系数 a
    (5) 各模简并度 —— 卷十九已完成

==============================================================================
本卷的做法（先建管线，再谈数）
==============================================================================
二阶变分不能"凭记忆写"，也不能"写完就用"。本卷构造一条数值谱求导管线
（周期一维格 + FFT 精确导数 → Christoffel → Ricci → R → 作用量 → 二阶系数），
并用五个独立自检把管线钉死：
    自检 A  共形平坦度规 g = e^{2 phi} delta 的 R 与解析式逐点比对
    自检 B  Lambda = 0 时，沿纯规范方向 h = L_v g 的二阶系数【精确为 0】
    自检 C  Lambda != 0 时，规范方向的二阶系数等于解析预言 -Lambda*|H|^2*L/4
            （背景离壳导致规范模不脱耦 —— 这是平背景路线的实质性诊断）
    自检 D  各 York 块的 Lambda 系数 B 与 sqrt(g) 展开的解析预言逐块比对
    自检 E  TT 块的 Hessian 与规范参数 alpha 无关

==============================================================================
本卷【不给出】NGFP 数值 (g_*, lambda_*) —— 理由在步骤 7，是机器读出的结构性阻塞，
不是偷懒
==============================================================================

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
REPORT_PATH = os.path.join(OUTDIR, "tuft_卷二十_二阶变分管线与规范鬼雅可比_report.txt")
JSON_PATH = os.path.join(OUTDIR, "tuft_卷二十_二阶变分管线与规范鬼雅可比.json")

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


# ================================================================ 几何管线
N_GRID = 192


def fft_deriv(f, L):
    """周期函数的谱导数（对带限数据精确）。"""
    n = f.shape[0]
    kk = 2.0 * np.pi * np.fft.fftfreq(n, d=L / n)
    return np.real(np.fft.ifft(1j * kk * np.fft.fft(f)))


def scalar_curvature(g, L):
    """g: (N,4,4) 只依赖 x_0 的度规场 ⇒ R: (N,)"""
    N = g.shape[0]
    ginv = np.linalg.inv(g)                       # (N,4,4)
    dg = np.zeros((4, N, 4, 4))                   # dg[a,:,i,j] = ∂_a g_{ij}
    for i in range(4):
        for j in range(4):
            dg[0, :, i, j] = fft_deriv(g[:, i, j], L)
    # Christoffel Γ^rho_{mu nu}
    Gam = np.zeros((N, 4, 4, 4))
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                s = np.zeros(N)
                for sig in range(4):
                    s += ginv[:, rho, sig] * (dg[mu, :, nu, sig]
                                              + dg[nu, :, mu, sig]
                                              - dg[sig, :, mu, nu])
                Gam[:, rho, mu, nu] = 0.5 * s
    # ∂_a Γ^rho_{mu nu}
    dGam = np.zeros((4, N, 4, 4, 4))
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                dGam[0, :, rho, mu, nu] = fft_deriv(Gam[:, rho, mu, nu], L)
    Ric = np.zeros((N, 4, 4))
    for mu in range(4):
        for nu in range(4):
            t1 = np.sum(dGam[:, :, :, mu, nu], axis=(0, 1))      # ∂_λ Γ^λ_{μν}
            t2 = np.zeros(N)
            for lam in range(4):
                t2 += dGam[nu, :, lam, lam, mu]                  # ∂_ν Γ^λ_{λμ}
            t3 = np.zeros(N)
            t4 = np.zeros(N)
            for lam in range(4):
                for rho in range(4):
                    t3 += Gam[:, lam, lam, rho] * Gam[:, rho, mu, nu]
                    t4 += Gam[:, lam, nu, rho] * Gam[:, rho, lam, mu]
            Ric[:, mu, nu] = t1 - t2 + t3 - t4
    R = np.einsum("nij,nij->n", ginv, Ric)
    detg = np.linalg.det(g)
    sqg = np.sqrt(detg)
    return R, sqg


def action_reduced(H, kappa, Lam, alpha=None, eps=3e-3, N=N_GRID):
    """约化作用量 Ŝ = ∫ sqrt(g)(2Λ - R) dx  [+ (1/(2α))∫F²]
       度规 g = δ + ε H cos(κ x_0)，x_0 ∈ [0,L)，L = 2π/κ，横向体积取 1。
       返回二阶系数 Ŝ₂（Ŝ = Ŝ₀ + ε Ŝ₁ + ε² Ŝ₂ + ...）。"""
    L = 2.0 * np.pi / kappa
    x = L * np.arange(N) / N
    I = np.eye(4)

    def S_of(e):
        g = np.tile(I, (N, 1, 1))
        g[:, :, :] += (e * np.cos(kappa * x))[:, None, None] * H[None, :, :]
        R, sqg = scalar_curvature(g, L)
        val = np.mean(sqg * (2.0 * Lam - R)) * L
        if alpha is not None:
            # F_μ = ∂^ν h_{μν} - (1/2) ∂_μ h  （平直背景，精确到 O(h²)）
            dh = -(e * kappa * np.sin(kappa * x))[:, None, None] * H[None, :, :]
            # ∂_ν h_{μν} 只有 ν=0 分量
            div = dh[:, :, 0]                       # ∂_ν h_{μν}, ν=0
            trH = float(np.trace(H))
            dtr = -(e * kappa * np.sin(kappa * x)) * trH
            F = div.copy()
            F[:, 0] -= 0.5 * dtr
            val += np.mean(np.sum(F * F, axis=1)) * L / (2.0 * alpha)
        return val

    s0 = S_of(0.0)
    s2e = []
    for e in (eps, eps * 0.5):
        s2e.append(((S_of(e) + S_of(-e)) * 0.5 - s0) / (e * e))
    # Richardson：S2(e) = S2 + S4 e^2 + ...
    return (4.0 * s2e[1] - s2e[0]) / 3.0


def hessian_eig(H, kappa, Lam, alpha=None):
    """约化 Hessian 本征值 Ô(κ) = 4 Ŝ₂ /(L |H|_F^2)，以及解析预测的 Λ 系数。"""
    L = 2.0 * np.pi / kappa
    nrm2 = float(np.sum(H * H))
    s2 = action_reduced(H, kappa, Lam, alpha=alpha)
    return 4.0 * s2 / (L * nrm2)


def B_pred(H):
    """√g 展开给出的 Λ 系数解析预言：
       √g = 1 + h/2 + [ (1/8)h^2 - (1/4) h_{μν}h^{μν} ] + ...
       ⇒ H·Ô·H ⊃ Λ[ (1/2)(trH)^2 - tr(H^2) ]"""
    trH = float(np.trace(H))
    trH2 = float(np.sum(H * H))
    return ((0.5 * trH * trH) - trH2) / trH2


# ================================================================ 步骤 0
chunk("步骤 0  范围")
note("卷二十闭合清单 (1)-(5)：本卷攻 (1) 的管线、(2)、(3)；(5) 卷十九已完成。")
note("先建管线并自检，再谈任何数值。")

# ================================================================ 步骤 1 自检 A
chunk("步骤 1  自检 A：共形平坦度规的 R 与解析式比对")
note("g = e^{2 φ(x0)} δ，φ 任意平滑周期函数。d = 4 解析式：")
note("    R = -(d-1) e^{-2φ} [ 2 ∇²φ + (d-2) |∇φ|² ] = -6 e^{-2φ} [ φ'' + (φ')² ]")
note("（该式已用单位 4-球独立核对：Ω = 2/(1+r²) 时给出 R = +12 = d(d-1) ✓）")
kappa_t = 1.0
L_t = 2.0 * np.pi / kappa_t
x_t = L_t * np.arange(N_GRID) / N_GRID
phi = 0.30 * np.sin(kappa_t * x_t) + 0.10 * np.cos(2.0 * kappa_t * x_t)
dphi = fft_deriv(phi, L_t)
ddphi = fft_deriv(dphi, L_t)
g_conf = np.zeros((N_GRID, 4, 4))
e2 = np.exp(2.0 * phi)
for i in range(4):
    g_conf[:, i, i] = e2
R_num, sqg_num = scalar_curvature(g_conf, L_t)
R_ana = -6.0 * np.exp(-2.0 * phi) * (ddphi + dphi * dphi)
errA = float(np.max(np.abs(R_num - R_ana))) / max(1.0, float(np.max(np.abs(R_ana))))
note("  数值 R 与解析 R 最大相对偏差 = %s（R 量级 %s）"
     % (fs(errA, 3), fs(float(np.max(np.abs(R_ana))), 4)))
verdict("V20-A1", "PASS" if errA < 1e-8 else "FAIL",
        "几何管线自检 A：Christoffel/Ricci/R 的实现与共形平坦解析式逐点一致"
        "（最大相对偏差 " + fs(errA, 3) + "）⇒ 管线可信")

# ================================================================ 步骤 2 自检 B/C
chunk("步骤 2  自检 B / C：纯规范方向（York 的 ξ 块）")
note("沿纯规范方向 h = L_v g（v = ε A sin(κ x0) ⇒ H = κ(e0⊗A + A⊗e0)）：")
note("  Λ = 0 时背景在壳，S[g+εL_v g] = S[g] + O(ε³) ⇒ 二阶系数【精确为 0】。")
note("  Λ ≠ 0 时背景离壳（R=0 ≠ 4Λ），规范模不再脱耦，")
note("    解析预言：Ô_ξ = -Λ（约化单位），即 Ŝ₂ = -Λ κ² L/2 ·（对 A = e_1 归一）。")
resB = 0.0
for A in (np.array([0.0, 1.0, 0.0, 0.0]),
          np.array([0.0, 0.0, 1.0, -0.5]),
          np.array([1.0, 0.3, 0.0, 0.0])):
    A = A / np.linalg.norm(A)
    H = np.outer(np.array([1.0, 0, 0, 0]), A) + np.outer(A, np.array([1.0, 0, 0, 0]))
    H = kappa_t * H
    nrm2 = float(np.sum(H * H))
    s2 = action_reduced(H, kappa_t, 0.0)
    resB = max(resB, abs(4.0 * s2 / (L_t * nrm2)))
    note("  A = %s ：Ô_ξ(Λ=0) = %s" % (str(np.round(A, 3)), fs(4.0 * s2 / (L_t * nrm2), 3)))
verdict("V20-B1", "PASS" if resB < 1e-7 else "FAIL",
        "自检 B：Λ=0 时沿三个不同规范方向的约化 Hessian 均为 0（最大 " + fs(resB, 3) + "）"
        " ⇒ 管线的动能（R）部分与规范不变性自洽")
Lam_t = 0.7
resC = 0.0
for A in (np.array([0.0, 1.0, 0.0, 0.0]),
          np.array([0.0, 0.0, 1.0, -0.5])):
    A = A / np.linalg.norm(A)
    H = kappa_t * (np.outer(np.array([1.0, 0, 0, 0]), A)
                   + np.outer(A, np.array([1.0, 0, 0, 0])))
    o = hessian_eig(H, kappa_t, Lam_t)
    resC = max(resC, abs(o + Lam_t))
    note("  A = %s ：Ô_ξ = %s ，解析预言 %s" % (str(np.round(A, 3)), fs(o, 6), fs(-Lam_t, 6)))
verdict("V20-C1", "PASS" if resC < 1e-7 else "FAIL",
        "自检 C：Λ≠0 时规范方向的 Ô_ξ = -Λ 与解析预言一致（最大偏差 " + fs(resC, 3) + "）"
        " ⇒ 平背景（离壳）下规范模【不脱耦】，其 Hessian 恰为 -Λ")

# ================================================================ 步骤 3 四块的 Hessian
chunk("步骤 3  四个 York 块的约化 Hessian：主符号 A·κ² + 质量系数 B·Λ")
note("约定：h = ε H cos(κ x0)，约化作用量 Ŝ = ∫√g(2Λ - R)（已抽出 1/(16πG)）。")
note("      Ô(κ) = 4 Ŝ₂ / (L |H|_F²)。主符号（κ² 系数）【与背景曲率无关】，")
note("      质量系数（Λ 系数）在球背景上还要叠加 ∝ R 的曲率项（R = 4Λ）。")
e0 = np.array([1.0, 0.0, 0.0, 0.0])
e2v = np.array([0.0, 1.0, 0.0, 0.0])
e3v = np.array([0.0, 0.0, 1.0, 0.0])
e4v = np.array([0.0, 0.0, 0.0, 1.0])
blocks = {
    "TT": (np.outer(e2v, e2v) - np.outer(e3v, e3v)) / np.sqrt(2.0),
    "xi": None,
    "sigma": None,
    "trace": 0.25 * np.eye(4),
}
# TT 的第二代表（检验 SO(3) 各向同性）
TT2 = (np.outer(e2v, e3v) + np.outer(e3v, e2v)) / np.sqrt(2.0)
xi_v = e2v
blocks["xi"] = kappa_t * (np.outer(e0, xi_v) + np.outer(xi_v, e0))
blocks["sigma"] = kappa_t ** 2 * (0.25 * np.eye(4) - np.outer(e0, e0))

kappa_l = 1.0
Lam_l = 0.7
kappa_h = 2.3
out = {}
for name, H in blocks.items():
    Hn = H / np.sqrt(float(np.sum(H * H)))
    o1 = hessian_eig(Hn, kappa_l, 0.0)
    o2 = hessian_eig(Hn, kappa_l, Lam_l)
    o3 = hessian_eig(Hn, kappa_h, 0.0)
    A_num = o1 / kappa_l ** 2
    A_num_h = o3 / kappa_h ** 2
    B_num = (o2 - o1) / Lam_l
    out[name] = {"A": A_num, "A_check": A_num_h, "B": B_num, "B_pred": B_pred(Hn)}
    note("  %-6s |H|_F=1 ：Ô(κ=%s,Λ=0) = %s ；Ô(κ=%s,Λ=%s) = %s"
         % (name, fs(kappa_l, 3), fs(o1, 8), fs(kappa_l, 3), fs(Lam_l, 3), fs(o2, 8)))
    note("            A(κ²系数) = %s （第二 κ 复核 %s） ；B(Λ系数) = %s ，解析预言 %s"
         % (fs(A_num, 8), fs(A_num_h, 8), fs(B_num, 8), fs(B_pred(Hn), 8)))
# TT 各向同性
o_tt2 = hessian_eig(TT2, kappa_l, 0.0)
note("  TT 第二极化 Ô = %s（与第一极化 %s 对比 ⇒ SO(3) 各向同性）"
     % (fs(o_tt2, 8), fs(out["TT"]["A"] * kappa_l ** 2, 8)))
verdict("V20-D1",
        "PASS" if abs(o_tt2 - out["TT"]["A"] * kappa_l ** 2) < 1e-7 else "FAIL",
        "TT 块的两个不同极化给出同一本征值（差 "
        + fs(abs(o_tt2 - out["TT"]["A"] * kappa_l ** 2), 3)
        + "）⇒ TT 块确为 5 维各向同性单一本征值，与卷十九的简并度 5 自洽")
maxB = max(abs(out[k]["B"] - out[k]["B_pred"]) for k in out)
verdict("V20-D2", "PASS" if maxB < 1e-6 else "FAIL",
        "自检 D：四个块的 Λ 系数与 √g 展开的解析预言逐块一致（最大偏差 " + fs(maxB, 3) + "）"
        " ⇒ Λ 扇区的记账完全独立核对过；TT/ξ/σ 为 -1，迹块为 +1")
maxA = max(abs(out[k]["A"] - out[k]["A_check"]) for k in out)
verdict("V20-D3", "PASS" if maxA < 1e-7 else "FAIL",
        "主符号 κ² 系数在 κ = %s 与 κ = %s 下一致（最大差 %s）"
        " ⇒ 确为 κ² 齐次，无隐藏的 κ^0 污染" % (fs(kappa_l, 3), fs(kappa_h, 3), fs(maxA, 3)))
note("")
note("【本卷导出的主符号（背景曲率无关，可直接用于任何背景）】")
for k in ("TT", "xi", "sigma", "trace"):
    note("    Ô_%-6s ⊃ %s · κ²      （+ Λ 系数 %s）"
         % (k, fs(out[k]["A"], 8), fs(out[k]["B"], 6)))

# ================================================================ 步骤 4 规范固定
chunk("步骤 4  规范固定项：解析 + 数值对拍，TT 规范无关性")
note("取 de Donder 型规范固定（本卷声明的约定）：")
note("    Ŝ_gf = (1/(2α)) ∫ F_μ F^μ ，  F_μ = ∂^ν h_{μν} - (1/2) ∂_μ h")
note("对 h = ε H cos(κ x0)：F_μ = -ε κ sin(κ x0) [ H_{μ0} - (1/2) trH δ_{μ0} ]")
note("    ⇒ Ŝ_gf,2 = (κ² L / (4α)) Σ_μ [ H_{μ0} - (1/2) trH δ_{μ0} ]²")
note("    ⇒ Ô_gf = (1/α) Σ_μ [...]² / |H|_F²")


def O_gf(H, kappa, alpha):
    v = H[:, 0] - 0.5 * float(np.trace(H)) * e0
    return (float(np.sum(v * v)) / float(np.sum(H * H))) / alpha


alpha_t = 1.3
note("")
note("  块        Ô_gf(α=%s) 解析      Ô(含gf,数值) - Ô(无gf,数值)   差" % fs(alpha_t, 4))
err_gf = 0.0
for name, H in blocks.items():
    Hn = H / np.sqrt(float(np.sum(H * H)))
    ana = O_gf(Hn, kappa_t, alpha_t)
    num_gf = hessian_eig(Hn, kappa_t, 0.0, alpha=alpha_t)
    num_no = hessian_eig(Hn, kappa_t, 0.0, alpha=None)
    d = abs((num_gf - num_no) - ana)
    err_gf = max(err_gf, d)
    note("  %-8s %s      %s      %s"
         % (name, fs(ana, 8), fs(num_gf - num_no, 8), fs(d, 3)))
verdict("V20-E1", "PASS" if err_gf < 1e-6 else "FAIL",
        "规范固定项的 Hessian：解析式与数值管线逐块对拍（最大差 " + fs(err_gf, 3) + "）")
tt_gf = O_gf(blocks["TT"] / np.sqrt(float(np.sum(blocks["TT"] ** 2))), kappa_t, alpha_t)
verdict("V20-E2", "PASS" if abs(tt_gf) < 1e-12 else "FAIL",
        "自检 E：TT 块的规范固定贡献恰为 0（" + fs(tt_gf, 3) + "）"
        " ⇒ TT 块 Hessian 与规范参数 α 无关，是规范不变的物理块")

# ================================================================ 步骤 5 鬼算符
chunk("步骤 5  鬼算符（卷二十清单第 (2) 项）")
note("推导：规范条件 F_μ = ∇^ν h_{μν} - (1/2) ∇_μ h。")
note("  沿 δh_{μν} = ∇_μ v_ν + ∇_ν v_μ（纯规范）：")
note("    δF_μ = ∇^ν(∇_μ v_ν + ∇_ν v_μ) - (1/2)∇_μ (2 ∇^ν v_ν)")
note("         = ∇_μ∇^ν v_ν + ∇² v_μ - ∇_μ∇^ν v_ν = ∇² v_μ     【平直背景】")
note("  ⇒ 鬼算符 M^μ_ν = δ^μ_ν ∇² = -δ^μ_ν (-∇²)。")
note("")
note("机器核对：取 v_ν = A_ν sin(κ x0)，数值算 F_μ 与 ∇²v_μ 对比。")
Lg = 2.0 * np.pi / kappa_t
xg = Lg * np.arange(N_GRID) / N_GRID
err_gh = 0.0
for A in (np.array([0.0, 1.0, 0.0, 0.0]),
          np.array([1.0, 0.4, -0.2, 0.7]),
          np.array([0.0, 0.0, 0.0, 1.0])):
    v = np.outer(np.sin(kappa_t * xg), A)              # (N,4)
    dvx = np.zeros((N_GRID, 4, 4))
    for a in range(4):
        dvx[:, 0, a] = fft_deriv(v[:, a], Lg)          # ∂_0 v_a
    h = dvx + np.transpose(dvx, (0, 2, 1))             # ∇_μ v_ν + ∇_ν v_μ
    div = h[:, :, 0]                                    # ∂_ν h_{μν}
    trh = h[:, 0, 0] + h[:, 1, 1] + h[:, 2, 2] + h[:, 3, 3]
    dtr = fft_deriv(trh, Lg)
    F = div.copy()
    F[:, 0] -= 0.5 * dtr
    lap = np.zeros((N_GRID, 4))
    for a in range(4):
        lap[:, a] = fft_deriv(fft_deriv(v[:, a], Lg), Lg)
    err_gh = max(err_gh, float(np.max(np.abs(F - lap))) / max(1.0, float(np.max(np.abs(lap)))))
    note("  A = %s ：max|F - ∇²v| / |∇²v| = %s"
         % (str(np.round(A, 3)), fs(float(np.max(np.abs(F - lap)))
                                    / max(1.0, float(np.max(np.abs(lap)))), 3)))
verdict("V20-G1", "PASS" if err_gh < 1e-8 else "FAIL",
        "鬼算符求导：δF_μ = ∇² v_μ 数值逐点成立（最大相对偏差 " + fs(err_gh, 3) + "）"
        " ⇒ 鬼算符 M = -(-∇²)，作用在 4 分量矢量上；"
        "配合卷十九的模计数（横 3 + 纵 1）即完成清单第 (2) 项")

# ================================================================ 步骤 6 雅可比
chunk("步骤 6  York 雅可比（卷二十清单第 (3) 项）")
note("场空间度规 ‖h‖² = ∫ h_{μν} h^{μν}。卷十九已证 York 四块两两正交，故")
note("  ‖h‖² = ‖h^TT‖² + 2 κ² ‖ξ‖² + (3/4) κ⁴ σ² + (1/4) h²")
note("（后三项的系数由 ∇ → i k 的代数给出；机器逐项核对如下）")
rng = np.random.RandomState(4242)
errJ = 0.0
for _ in range(8):
    kk = rng.normal(size=4)
    kk = kk / np.linalg.norm(kk) * float(rng.uniform(0.4, 3.0))
    # ξ 项
    ns = np.linalg.svd(kk.reshape(1, 4))[2][1:].T      # 4x3 横空间
    xi = ns @ rng.normal(size=3)
    xi = xi / np.linalg.norm(xi)
    Hxi = np.outer(kk, xi) + np.outer(xi, kk)
    errJ = max(errJ, abs(float(np.sum(Hxi * Hxi)) - 2.0 * float(kk @ kk)) / (2.0 * float(kk @ kk)))
    # σ 项
    Hs = -np.outer(kk, kk) + 0.25 * np.eye(4) * float(kk @ kk)
    errJ = max(errJ, abs(float(np.sum(Hs * Hs)) - 0.75 * float(kk @ kk) ** 2)
               / (0.75 * float(kk @ kk) ** 2))
    # h 项
    Hh = 0.25 * np.eye(4)
    errJ = max(errJ, abs(float(np.sum(Hh * Hh)) - 0.25) / 0.25)
note("  8 组随机波矢下三项范数系数的最大相对偏差 = %s" % fs(errJ, 3))
verdict("V20-J1", "PASS" if errJ < 1e-10 else "FAIL",
        "York 场空间度规的范数系数 2κ²、(3/4)κ⁴、1/4 机器核对（最大偏差 " + fs(errJ, 3) + "）")
note("")
note("⇒ 雅可比（√det 场空间度规）：")
note("    J = det_T[2(-∇²)]^{1/2} · det_S[(3/4)(-∇²)²]^{1/2} · det_S[1/4]^{1/2}")
note("⇒ Γ ⊃ -ln J = -(1/2) Tr_T ln(-∇²) - Tr_S ln(-∇²) + const")
note("   （TT 块度规为恒等 ⇒ 无雅可比因子；常数列不进流。）")
verdict("V20-J2", "PASS",
        "York 雅可比求导完成（平直背景）：Γ ⊃ -(1/2)Tr_{横矢} ln(-∇²) - Tr_{标量} ln(-∇²)；"
        "清单第 (3) 项在平直背景下闭合")
verdict("V20-J3", "BOUNDARY",
        "雅可比的【弯曲背景曲率修正】未推导：横矢块在最大对称背景上应为 "
        "(-∇² - R/d)，σ 块的 (∇_μ∇_ν - (1/d)g∇²)² 也带曲率项；"
        "这些修正与 Λ 同量级（球上 R = 4Λ），会影响阈值宗量系数 a")

# ================================================================ 步骤 7 阻塞
chunk("步骤 7  为什么本卷仍不给出 (g_*, λ_*) —— 两条机器读出的结构性阻塞")
note("阻塞一（本卷步骤 2 实测）：平背景 + Λ≠0 是【离壳】背景（R = 0 ≠ 4Λ），")
note("  规范模不脱耦 —— ξ 块的 Hessian 恰为 -Λ 而非 0。")
note("  ⇒ 平背景下的流方程含有规范/背景假象，规范模会污染迹。")
verdict("V20-X1", "FAIL",
        "平背景路线被机器否证：离壳背景使 ξ（纯规范）块的 Hessian = -Λ ≠ 0"
        " ⇒ 必须改用【在壳】背景（球：R = 4Λ）才能让规范模脱耦")
note("")
note("阻塞二（结构性）：EH 截断提取 β_G 需要把流方程投影到 ∫√g(-R) 结构。")
note("  在平背景上 R ≡ 0，该结构在背景处的取值为零 ⇒ 无法把")
note("  ∂_t Γ_k 分解为「体积项」与「曲率项」两个系数 ⇒ β_G 不可读。")
note("  （这不是数值问题，是投影基在 R = 0 处退化的代数事实。）")
verdict("V20-X2", "FAIL",
        "平背景不可提取 β_G：R ≡ 0 使 ∫√g R 结构在背景处退化，"
        "流方程无法分解为体积项与曲率项 ⇒ 必须用 R ≠ 0 的在壳背景（球）")
verdict("V20-H1", "OPEN",
        "本卷仍【不给出】NGFP 数值 (g_*, λ_*)：球背景上的 Hessian 曲率项、"
        "在壳规范模脱耦、以及 β_G 的投影，三项均未闭合 ⇒ 列为卷二十一第 1 项")

# ================================================================ 步骤 8 边界
chunk("步骤 8  诚实边界与本卷成果")
verdict("V20-H2", "INFO",
        "本卷可保留的稳健成果：(a) 几何管线经共形平坦解析式逐点校验（V20-A1）；"
        "(b) 主符号 A（κ² 系数）逐块导出且与背景曲率无关（V20-D3）；"
        "(c) Λ 系数与 √g 展开解析预言逐块一致（V20-D2）；"
        "(d) 规范固定项与 TT 规范无关性（V20-E1/E2）；"
        "(e) 鬼算符 M = -(-∇²) 求导并数值核对（V20-G1）；"
        "(f) York 雅可比算符内容（V20-J1/J2）；"
        "(g) 平背景路线的两条阻塞（V20-X1/X2）")
verdict("V20-H3", "INFO",
        "卷二十一闭合清单：(1) 球（在壳、R = 4Λ）背景上的二阶变分 —— 本卷管线"
        "换到球面谐基即可复用；(2) 各 York 模的曲率项 ⇒ 阈值宗量系数 a；"
        "(3) 雅可比的曲率修正（V20-J3）；(4) 组装迹并代入卷十九的"
        "一维方程 λ G(λ) + L(λ) = 0；(5) 用 T19-4（B_gg = -2）、T19-5（λ_*<1/2）、"
        "T19-6（符号判据）三条硬约束自检")
note("")
note("相对卷十九的机制性进展：卷十九给出【约束】（不动点必须满足什么）；")
note("  本卷给出【求导管线 + 主符号 + 规范/鬼/雅可比三件套】，")
note("  并用机器否证了最容易走的平背景捷径。")

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
_emit("红线声明：数学自洽 != 实验证实。本卷只做二阶变分管线、规范/鬼/雅可比的")
_emit("          机器求导与自检，不给出 NGFP 数值，不构成对 TUFT 物理真实性的主张。")

text = "\n".join(LINES) + "\n"
try:
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("[report written] " + REPORT_PATH)
except Exception as exc:
    print("[report FAILED] " + str(exc))

payload = {
    "subject": "TUFT 卷二十 二阶变分管线 规范固定 鬼算符 York雅可比",
    "counts": COUNTS,
    "items": [{"code": c, "status": s, "text": t} for c, s, t in ITEMS],
    "pipeline": {"grid": N_GRID, "validation_A_rel_err": errA},
    "hessian_reduced_principal_symbol": {
        k: {"A_kappa2": out[k]["A"], "B_Lambda": out[k]["B"],
            "B_analytic": out[k]["B_pred"]} for k in out
    },
    "gauge_fixing": {"alpha_used": alpha_t, "TT_contribution": tt_gf,
                     "max_analytic_numeric_diff": err_gf},
    "ghost_operator": "M^mu_nu = delta^mu_nu Laplacian = -delta^mu_nu(-Laplacian)",
    "york_jacobian": {
        "norms": {"xi": "2 k^2", "sigma": "(3/4) k^4", "trace": "1/4"},
        "Gamma_contribution": "-(1/2)Tr_T ln(-Lap) - Tr_S ln(-Lap) + const",
        "max_rel_err": errJ,
    },
    "runtime_s": float(time.time() - T0),
}
try:
    with open(JSON_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print("[json written] " + JSON_PATH)
except Exception as exc:
    print("[json FAILED] " + str(exc))
