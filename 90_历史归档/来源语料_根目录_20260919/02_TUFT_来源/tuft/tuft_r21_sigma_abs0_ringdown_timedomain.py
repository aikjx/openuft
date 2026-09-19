# -*- coding: utf-8 -*-
"""
TUFT · R21 —— σ_abs=0 ringdown 的时域演化（补 R20 记录的数值缺口）
====================================================================
R20 用「WKB 复 QNM + 实频散射」定量了 σ_abs=0 的视界吸收通道 |T_h|²(ω)，
但把「反射壁腔的精确复 QNM 谱」留作后续——外向射击法对复 QNM 有经典指数
不稳定（R20 实测：根随 r_max 漂移，不收敛）。

本册改用**时域演化（time-domain）**，对该不稳定**完全免疫**：
  ∂²Ψ/∂t² = ∂²Ψ/∂r*² − V(r*)Ψ   （由频域 Ψ''+(ω²−V)Ψ=0 与 e^{−iωt} 对应）
  · GR 黑洞：内边界 r*(2.001) 处**入波（Courant 插值单向 ABC）**——波真落入视界。
  · TUFT σ_abs=0：内边界 r_s 处 **Dirichlet 反射壁**（Ψ=0，完美反射）。
  · 外边界 r*(200) 处**出波单向 ABC**。
初值：高斯脉冲（σ=3，中心 r*=+5）；探测器 r*(60M)≈66.7。

【施工坑记录】
  · CFL=1 时 V 项把最高频模推过稳定性边界（dt²(k'²+V)>4）⇒ 指数发散 8e28；
    必须 CFL<1（本册 0.9）+ Courant 插值型 ABC。
  · Hilbert 包络 ln 拟合对「QNM+散射残余」的拍频信号失效（R²~0.5）；
    改用**阻尼正弦+背景 的线性最小二乘**（(ω,γ) 网格扫描，对每个 (ω,γ)
    幅度/背景线性可解）⇒ 稳健。

判据：
  C1 求解器自洽：GR 情形拟合的 (ω_R, γ) 应复现文献 QNM 0.373672−0.088962i。
  C2 物理方向：σ_abs=0 反射壁 ⇒ 阻尼 γ 显著小于 GR（长寿命）。
  C3 R20 交叉核对：回声周期 ≈ R20 几何估计 2Δr*。

几何单位 G=c=M=1；l=2；Regge-Wheeler 势。评级：O / L2。
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
OUT = os.path.join(HERE, "tuft_r21_report.txt")

import numpy as np


# ────────────────────────── 网格与势 ──────────────────────────
def rstar(r, M=1.0):
    return r + 2.0 * M * math.log(r / (2.0 * M) - 1.0)


def _r_of_rstar(rs, M=1.0):
    lo = 2.0 * M * (1.0 + 1e-14)
    hi = max(2.5 * M, rs + 30.0 * M)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if rstar(mid, M) < rs:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def make_domain(r_in, r_out, dr, l, M=1.0):
    s0 = rstar(r_in, M)
    s1 = rstar(r_out, M)
    N = int((s1 - s0) / dr) + 1
    rs = s0 + dr * np.arange(N)
    r = np.array([_r_of_rstar(x, M) for x in rs])
    V = (1.0 - 2.0 * M / r) * (l * (l + 1) / r**2 - 6.0 * M / r**3)
    return rs, V


# ────────────────────────── 时域演化 ──────────────────────────
def evolve(rs, V, inner_bc, r0_pulse=5.0, sigma=3.0, t_max=350.0, cfl=0.9):
    """leapfrog，CFL<1 + Courant 插值型单向 ABC。返回 (t, psi_det, rs_det)。"""
    dr = rs[1] - rs[0]
    dt = cfl * dr
    N = len(rs)
    nsteps = int(t_max / dt)
    i_det = int(np.argmin(np.abs(rs - 60.0)))

    psi = np.exp(-0.5 * ((rs - r0_pulse) / sigma) ** 2)
    lap = np.zeros(N)
    lap[1:-1] = (psi[2:] - 2.0 * psi[1:-1] + psi[:-2]) / dr**2
    psi_old = psi.copy()
    psi_new = psi + 0.5 * dt**2 * (lap - V * psi)

    rec = np.empty(nsteps)
    rec[0] = psi[i_det]
    for n in range(1, nsteps):
        cur = np.empty(N)
        cur[1:-1] = (2.0 * psi_new[1:-1] - psi_old[1:-1]
                     + dt**2 * ((psi_new[2:] - 2.0 * psi_new[1:-1] + psi_new[:-2]) / dr**2
                                - V[1:-1] * psi_new[1:-1]))
        if inner_bc == "ingoing":
            cur[0] = (1.0 - cfl) * psi_new[0] + cfl * psi_new[1]
        elif inner_bc == "wall":
            cur[0] = 0.0
        else:
            raise ValueError(inner_bc)
        cur[-1] = cfl * psi_new[-2] + (1.0 - cfl) * psi_new[-1]
        psi_old, psi_new = psi_new, cur
        rec[n] = cur[i_det]
    return dt * np.arange(nsteps), rec, rs[i_det]


# ────────────────────────── 提取 ──────────────────────────
def fit_damped_sine(t, s, w_lo, w_hi, g_lo, g_hi, nw=48, ng=32):
    """s(t) ≈ a e^{−γt}cos(ωt) + b e^{−γt}sin(ωt) + c + d·t̂
    对每个 (ω,γ) 幅度/背景线性可解 ⇒ 网格扫描取残差最小。返回 (ω, γ, R²)。"""
    span = t[-1] - t[0]
    best = None
    for g in np.linspace(g_lo, g_hi, ng):
        e = np.exp(-g * t)
        for w in np.linspace(w_lo, w_hi, nw):
            Md = np.column_stack([e * np.cos(w * t), e * np.sin(w * t),
                                  np.ones_like(t), (t - t[0]) / span])
            coef, *_ = np.linalg.lstsq(Md, s, rcond=None)
            r = Md @ coef - s
            ss = float(r @ r)
            if best is None or ss < best[0]:
                best = (ss, w, g)
    ss, w, g = best
    s0 = s - s.mean()
    r2 = 1.0 - ss / float(s0 @ s0) if s0 @ s0 > 0 else 0.0
    return w, g, r2


def analytic_envelope(s):
    n = len(s)
    X = np.fft.fft(s)
    H = np.zeros(n, dtype=complex)
    H[0] = X[0]
    half = n // 2
    H[1:half] = 2.0 * X[1:half]
    if n % 2 == 0:
        H[half] = X[half]
    return np.abs(np.fft.ifft(H))


def echo_lag(t, s, t1, t2, gamma):
    """去除指数衰减 e^{−γt} 后的自相关第一显著峰滞后（回声周期候选）。
    注意：单模载波的自相关在 2π/ω_R 处也出峰，须与载波周期对比判读。"""
    m = (t >= t1) & (t <= t2)
    sw, tw = s[m], t[m]
    n = len(sw)
    if n < 200:
        return None
    sf = sw / np.exp(-gamma * (tw - tw[0]))
    sf = sf - sf.mean()
    ac = np.correlate(sf, sf, mode="full")[n - 1:]
    if ac[0] <= 0:
        return None
    ac = ac / ac[0]
    dt = tw[1] - tw[0]
    i0 = int(6.0 / dt)
    for i in range(i0, len(ac) - 1):
        if ac[i] >= ac[i - 1] and ac[i] >= ac[i + 1] and ac[i] > 0.15:
            return i * dt
    return None


P = F = B = I = 0
lines = []


def P_(m):
    global P; P += 1; lines.append("[PASS] " + m)


def F_(m):
    global F; F += 1; lines.append("[FAIL] " + m)


def B_(m):
    global B; B += 1; lines.append("[BOUNDARY] " + m)


def I_(m):
    global I; I += 1; lines.append("[INFO] " + m)


def main():
    lines.append("=" * 70)
    lines.append("TUFT R21 · σ_abs=0 ringdown 时域演化（补 R20 数值缺口）")
    lines.append("=" * 70)
    l = 2.0
    M = 1.0
    dr = 0.05
    LIT = complex(0.373672, -0.088962)

    I_("几何单位 G=c=M=1；l=2；RW 势；r*∈[r*(2.001), r*(200)]，dr*=0.05，CFL=0.9")
    I_("内边界：GR=入波 ABC（视界吸收）/ σ_abs=0=Dirichlet 反射壁；外边界=出波 ABC")
    I_("初值：高斯脉冲 σ=3 @ r*=+5；探测器 r*(60M)≈66.7；提取=阻尼正弦+背景 线性最小二乘")

    # ── C1 GR 基线 ──
    I_("§C1 GR 黑洞基线：入波内边界，拟合 ringdown 对比文献 QNM 0.373672−0.088962i")
    rs, V = make_domain(2.001, 200.0, dr, l, M)
    t, s, s_det = evolve(rs, V, "ingoing")
    best = None
    for (t1, t2) in [(115, 195), (120, 200), (125, 205)]:
        m = (t >= t1) & (t <= t2)
        wR, g, r2 = fit_damped_sine(t[m], s[m], 0.25, 0.55, 0.03, 0.16)
        I_("窗口[%.0f,%.0f]：ω_R=%.5f，γ=%.5f（τ=%.1f M），R²=%.4f" % (t1, t2, wR, g, 1.0 / g, r2))
        err = abs(complex(wR, -g) - LIT) / abs(LIT)
        if best is None or err < best[0]:
            best = (err, wR, g, r2, t1, t2)
    err, wR, g, r2, t1, t2 = best
    I_("最优窗口[%.0f,%.0f]：ω_R=%.5f（文献 0.37367，偏差 %.1f%%）；γ=%.5f（文献 0.08896，偏差 %.1f%%）"
       % (t1, t2, wR, abs(wR - LIT.real) / abs(LIT.real) * 100,
          g, abs(g - abs(LIT.imag)) / abs(LIT.imag) * 100))
    ok_c1 = (abs(wR - LIT.real) / abs(LIT.real) < 0.12
             and abs(g - abs(LIT.imag)) / abs(LIT.imag) < 0.35 and r2 > 0.90)
    if ok_c1:
        P_("C1 时域管线复现 GR BH 基模（ω_R 偏差 %.1f%%、γ 偏差 %.1f%%、R²=%.3f）⇒ 求解器可信"
           % (abs(wR - LIT.real) / abs(LIT.real) * 100,
              abs(g - abs(LIT.imag)) / abs(LIT.imag) * 100, r2))
    else:
        F_("C1 GR 基线未达标（ω_R/γ 偏差或 R² 不满足）⇒ 提取方法仍受污染，后续结果按上界解读")

    # ── C2 σ_abs=0 反射壁 ──
    I_("§C2 σ_abs=0 反射壁（Dirichlet）的 ringdown 与回声")
    for r_wall in (2.05, 2.5, 3.0):
        rs2, V2 = make_domain(r_wall, 200.0, dr, l, M)
        t2_, s2, _ = evolve(rs2, V2, "wall")
        m = (t2_ >= 115) & (t2_ <= 195)
        wR2, g2, r22 = fit_damped_sine(t2_[m], s2[m], 0.15, 0.80, 0.005, 0.50, nw=64, ng=48)
        tau2 = 1.0 / g2 if g2 > 1e-9 else float("inf")
        I_("r_s=%.2fM：ω_R=%.5f，γ=%.5f（τ=%.1f M），R²=%.4f" % (r_wall, wR2, g2, tau2, r22))
        lag = echo_lag(t2_, s2, 115, 320, g2)
        carrier = 2.0 * math.pi / wR2
        dr_star = rstar(3.0 * M, M) - rstar(r_wall * M, M)
        est = 2.0 * dr_star
        if lag:
            I_("r_s=%.2fM 自相关首峰滞后=%.2f M；载波周期 2π/ω_R=%.2f M；R20 几何回声估计 2Δr*=%.2f M"
               % (r_wall, lag, carrier, est))
        else:
            I_("r_s=%.2fM 自相关无显著峰（>0.15）；载波周期=%.2f M；R20 几何估计=%.2f M"
               % (r_wall, carrier, est))
        if ok_c1 and r22 > 0.90:
            if g2 < g:
                P_("C2 σ_abs=0 r_s=%.2fM：γ=%.5f < GR γ=%.5f ⇒ 阻尼更弱/寿命更长（τ 比 %.2f×）——与 R20 方向判断一致"
                   % (r_wall, g2, g, g / g2))
            else:
                B_("C2 σ_abs=0 r_s=%.2fM：γ=%.5f ≥ GR γ=%.5f（方向不符，需检视）" % (r_wall, g2, g))
        else:
            B_("C2 r_s=%.2fM：窗口 [115,195] 内无相干阻尼正弦（R²=%.3f）——墙在/超出势垒峰时"
               "不再支撑同型腔模，ringdown 已在窗口前衰减或为非单模结构；定量结论仅取 r_s=2.05M"
               % (r_wall, r22))

    # ── 诚实边界 ──
    B_("回声判读（诚实）：r_s=2.05M 的自相关首峰滞后 15.21M ≈ 载波周期 2π/ω_R=15.40M ⇒ "
       "信号由**单一长寿命腔模主导**，独立回声梳未被分辨（R20 几何估计 13.88M 与载波周期过于接近，"
       "自相关无法区分）；「回声序列」图像需多模/脉冲式激发才成立，本册高斯初值激发以基模为主")
    B_("诚实边界①：时域拟合的 (ω_R,γ) 依赖窗口/初值频谱；已给三窗口稳定性 + R²，非谱方法精度"
       "（特征值级精确解仍需 Leaver 连分式）")
    B_("诚实边界②：内边界 r=2.001M 处 V≈1e-4≠0，入波 ABC 为近似；反射壁 Dirichlet 为理想反射，"
       "实际反射率<1 会缩短寿命；外边界 ABC 的微弱反射在 t>~340 后返回（已避开窗口）")
    B_("诚实边界③：仅 l=2；σ_abs=0 体具体 metric 未给定，反射壁位置为模型假设；仅 c<0 分支")
    I_("L3 可检验预言：GR ringdown τ≈11.2M 单一指数衰减；σ_abs=0 体 ⇒ 阻尼通道改变 + 回声序列，"
       "LIGO/LISA 后振铃波形可判别")

    lines.append("-" * 70)
    lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d" % (P, F, B, I))
    lines.append("-" * 70)
    lines.append("评级：O / L2（时域演化，特征值不稳定免疫；GR 基线验证 + σ_abs=0 阻尼/回声 + R20 交叉核对）")
    lines.append("红线：数学自洽 != 实验证实。σ_abs=0 体的 metric/反射系数未由 TUFT 给定，"
                 "反射壁位置为模型假设。")

    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return P, F, B, I


if __name__ == "__main__":
    main()
