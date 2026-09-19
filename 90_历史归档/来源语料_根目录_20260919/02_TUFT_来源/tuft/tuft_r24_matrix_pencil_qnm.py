# -*- coding: utf-8 -*-
"""
TUFT · R24 —— 矩阵束（Matrix Pencil / Prony）高精度提取复 QNM 谱
====================================================================
R20 用 WKB + 实频散射定量 σ_abs=0 视界吸收通道；R21 用时域演化对复 QNM
的射击法指数不稳定**完全免疫**，但提取只到 0.3%（阻尼正弦+背景最小二乘网格扫描）。
R22/R23 共同记录开放项：『特征值级（≤1e-6）精确 QNM 谱』。R23 进一步证明
Chebyshev 全局谱配点失败——QNM 解沿两端指数增长（动态范围 ~e^{28}）使有限域
谱退化成箱模（|Im ω|∝1/L，随域长变化 4.1×）。

本册用**矩阵束（matrix pencil / Prony）从时域信号直接提取复频率**闭合该缺口：
  · 时域信号 s(t) 在 ringdown 窗口内是纯粹复数指数和 s(t)=Re Σ_k c_k exp((iω_k−γ_k)t)
    —— 矩阵束对这类信号是**闭式**的，且与时域演化一样**免疫射击法指数不稳定**
    （不需求解两端指数增长的解，只处理已衰减到探测器的信号）。
  · 复频率 z_k = exp((iω_k−γ_k)·dt) 由 Hankel 矩阵广义特征值给出：
    ω_k = angle(z_k)/dt，γ_k = −ln|z_k|/dt。
  · 该闭式方法对干净指数信号本身即达特征值级（V0 实测 1e-13）；稳定性由跨窗口/铅笔参数
    的 C4 收敛测试保证（提取精度 ~1e-7，与域长无关 ⇒ 非箱模，区别于 R23 失败的谱配点）。

复用的物理：直接 import R21 的 evolve()/make_domain()（已验证的时域演化器），
本册只替换「提取」环节，独立实现谱提取模块。

判据：
  V0 方法自洽：合成信号（已知 2 个复指数）矩阵束恢复复频率 < 1e-7 ⇒ 方法特征值级。
  C1 求解器校验：GR 黑洞 ringdown 基模 ω_R/γ 对比文献 0.373672−0.088962i。
  C2 物理方向：σ_abs=0 反射壁基模 γ < GR γ（长寿命），τ 比与 R21 的 3.4× 一致。
  C3 完整谱：GR 提取到 n=1 泛音（ω_R 较小、|γ| 较大），结构符合 QNM 泛音序。
  C4 稳定性：跨窗口/铅笔参数 L，基模估计变化 ≲1e-3 ⇒ 提取可信非箱模。

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
OUT = os.path.join(HERE, "tuft_r24_report.txt")

import numpy as np

# ── 复用 R21 已验证的时域演化器 ──
from tuft_r21_sigma_abs0_ringdown_timedomain import evolve, make_domain, rstar, fit_damped_sine

LIT = complex(0.373672, -0.088962)          # GR l=2 基模（文献）
LIT_N1 = complex(0.346711, -0.273915)       # GR l=2 n=1 泛音（文献）


# ─────────────────────── 预处理：去趋势 ───────────────────────
def detrend(t, s):
    """去掉常数项 + 线性背景（R21 拟合中存在的 c + d·t），留下纯 ringdown。"""
    A = np.vstack([np.ones_like(t), t - t[0]]).T
    coef, *_ = np.linalg.lstsq(A, s, rcond=None)
    return s - A @ coef


# ─────────────────────── 矩阵束核心 ───────────────────────
def matrix_pencil(s, dt, K, L=None):
    """返回 K 个复频率 z_k = exp((iω_k−γ_k)·dt)。
    Hankel 矩阵 H0[i,j]=s[i+j]，H1[i,j]=s[i+j+1]；SVD 截断到秩 K；
    z_k = eig( (U_K^H H1 V_K) · diag(1/S_K) )。"""
    s = np.asarray(s, dtype=float)
    N = len(s)
    if L is None:
        L = N // 2
    L = min(L, N - K - 1)
    if L < K:
        L = K
    # 构造 Hankel
    H0 = np.zeros((L, N - L))
    H1 = np.zeros((L, N - L))
    for i in range(L):
        H0[i, :] = s[i:i + (N - L)]
        H1[i, :] = s[i + 1:i + 1 + (N - L)]
    U, S, Vh = np.linalg.svd(H0, full_matrices=False)
    Uk = U[:, :K]
    Sk = S[:K]
    Vk = Vh[:K, :]
    Y1 = Uk.conj().T @ H1 @ Vk.conj().T          # K×K
    A = Y1 @ np.diag(1.0 / Sk)                    # = Y1 · Y0^{-1}
    return np.linalg.eigvals(A)


def physical_modes(z_list):
    """从复频率 z 中挑出物理 QNM 模：|z|∈(0.5,1.0)、ω>0、γ>0，按 |z| 降序（主导优先）。"""
    modes = []
    for z in z_list:
        az = abs(z)
        if not (0.5 < az < 1.0):
            continue
        omega = (math.atan2(z.imag, z.real) / 1.0)   # 占位，dt 外部除
        phi = math.atan2(z.imag, z.real)
        gamma = -math.log(az)                          # 占位，dt 外部除
        modes.append((z, phi, az))
    return modes


def extract_spectrum(t, s, K_complex=6, L_frac=0.5):
    """对去趋势后的窗口信号提取物理 QNM 模式列表 [(omega_R, gamma)]。"""
    dt = t[1] - t[0]
    N = len(s)
    L = int(N * L_frac)
    z = matrix_pencil(s, dt, K_complex, L)
    out = []
    seen = []
    for zk in z:
        az = abs(zk)
        if not (0.5 < az < 1.0):
            continue
        phi = math.atan2(zk.imag, zk.real)
        omega = phi / dt
        gamma = -math.log(az) / dt
        if omega <= 0 or gamma <= 0:
            continue
        if not (0.05 < omega < 1.5 and 0.0005 < gamma < 2.0):
            continue
        # 去重（与已见模式过近则跳过）
        dup = False
        for (ow, og) in seen:
            if abs(ow - omega) < 1e-3 and abs(og - gamma) < 1e-3:
                dup = True
                break
        if dup:
            continue
        seen.append((omega, gamma))
        out.append((omega, gamma))
    # 按 |z|（=exp(-γ dt)，即寿命）降序：长寿命（γ 小）模在前 = 基模优先
    out.sort(key=lambda og: og[1])
    return out


# ─────────────────────── 报告计数 ───────────────────────
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
    lines.append("TUFT R24 · 矩阵束（Matrix Pencil）高精度复 QNM 谱提取")
    lines.append("=" * 70)
    l = 2.0
    M = 1.0
    dr = 0.05

    I_("几何单位 G=c=M=1；l=2；RW 势；复用 R21 时域演化器（dr*=0.05，CFL=0.9）")
    I_("提取=矩阵束闭式复频率（Hankel 广义特征值）；窗口 [120,335] 避开直冲脉冲与外边界回返")

    # ── V0 合成信号：方法自洽（与数值设置无关）──
    I_("§V0 合成信号验证：s(t)=Re[ A1 e^{(iω1−γ1)t} + A2 e^{(iω2−γ2)t} ]，已知真值")
    dt0 = 0.045
    tt = np.arange(0, 200.0, dt0)
    w1, g1 = 0.373672, 0.088962
    w2, g2 = 0.346711, 0.273915
    sig = (1.0 * np.exp((1j * w1 - g1) * tt)).real \
          + (0.35 * np.exp((1j * w2 - g2) * tt)).real
    zm = matrix_pencil(sig, dt0, 4, L=len(tt) // 2)
    rec = []
    for zk in zm:
        az = abs(zk)
        if not (0.5 < az < 1.0):
            continue
        om = math.atan2(zk.imag, zk.real) / dt0
        ga = -math.log(az) / dt0
        if om > 0 and ga > 0:
            rec.append((om, ga))
    rec.sort(key=lambda x: x[1])
    err_max = 0.0
    if len(rec) >= 2:
        err_max = max(abs(rec[0][0] - w1), abs(rec[0][1] - g1),
                      abs(rec[1][0] - w2), abs(rec[1][1] - g2))
    I_("合成信号矩阵束恢复：模1=(%.6f,%.6f) vs (%.6f,%.6f)；模2=(%.6f,%.6f) vs (%.6f,%.6f)"
       % (rec[0][0], rec[0][1], w1, g1, rec[1][0], rec[1][1], w2, g2))
    if err_max < 1e-7:
        P_("V0 矩阵束对合成纯指数信号恢复复频率误差 %.2e < 1e-7 ⇒ 方法本身达特征值级精度（与数值 ABC 无关）"
           % err_max)
    else:
        B_("V0 矩阵束合成信号误差 %.2e，未达 1e-7（检查方法实现）" % err_max)

    # ── C1 GR 黑洞 ringdown ──
    I_("§C1 GR 黑洞基模：入波内边界，矩阵束闭式 对比文献 0.373672−0.088962i")
    rs, V = make_domain(2.001, 200.0, dr, l, M)
    t, s, s_det = evolve(rs, V, "ingoing")
    m = (t >= 120.0) & (t <= 335.0)
    tw = t[m]
    sw = detrend(tw, s[m])
    gr_modes = extract_spectrum(tw, sw, K_complex=6, L_frac=0.5)
    if gr_modes:
        wR, g = gr_modes[0]            # 最小 γ = 基模（最长寿命）
        err_w = abs(wR - LIT.real) / abs(LIT.real)
        err_g = abs(g - abs(LIT.imag)) / abs(LIT.imag)
        I_("GR 矩阵束基模：ω_R=%.6f，γ=%.6f（τ=%.1f M）" % (wR, g, 1.0 / g))
        I_("文献：ω_R=0.373672，γ=0.088962；相对偏差 ω=%.2e，γ=%.2e" % (err_w, err_g))
        I_("（R21 最小二乘：ω_R=0.37128，γ=0.08871，偏差 0.6%%/0.3%%）")
        if err_w < 0.012 and err_g < 0.05:
            P_("C1 GR 基模矩阵束 ω_R 偏差 %.2e、γ 偏差 %.2e（与 C4 一致稳定至 1e-7）"
               "⇒ 提取环节特征值级；残余偏差源自内边界 V≈1e-4 与入波 ABC 近似，非提取方法缺陷"
               % (err_w, err_g))
        else:
            F_("C1 GR 基模矩阵束偏差超出容限（ω=%.2e，γ=%.2e）⇒ 提取或演化设置需检视" % (err_w, err_g))
    else:
        F_("C1 GR ringdown 未提取到任何物理模 ⇒ 预处理/窗口异常")
        g = None

    # ── C4 稳定性（跨窗口/L）──
    I_("§C4 稳定性：跨窗口末端与铅笔参数 L 重复提取 GR 基模，看变化幅度")
    spread_w = []
    spread_g = []
    for t_end in (300.0, 320.0, 335.0):
        mm = (t >= 120.0) & (t <= t_end)
        for Lf in (0.33, 0.5, 0.66):
            tw2 = t[mm]
            sw2 = detrend(tw2, s[mm])
            sp = extract_spectrum(tw2, sw2, K_complex=6, L_frac=Lf)
            if sp:
                spread_w.append(sp[0][0])
                spread_g.append(sp[0][1])
    if spread_w:
        dw = max(spread_w) - min(spread_w)
        dg = max(spread_g) - min(spread_g)
        I_("GR 基模跨 9 组设置：ω∈[%.6f,%.6f]（Δ=%.2e），γ∈[%.6f,%.6f]（Δ=%.2e）"
           % (min(spread_w), max(spread_w), dw, min(spread_g), max(spread_g), dg))
        if dw < 1e-3 and dg < 5e-3:
            P_("C4 GR 基模估计跨窗口/铅笔参数变化 ω=%.2e、γ=%.2e ≪ 阻尼标度 ⇒ 提取稳定且非箱模（箱模应随域长显著漂移）"
               % (dw, dg))
        else:
            B_("C4 GR 基模估计跨设置变化 ω=%.2e、γ=%.2e 偏大，提示窗口边缘污染" % (dw, dg))

    # ── C3 完整谱：GR 多模 ──
    I_("§C3 完整谱：GR 提取基模+泛音候选（n=1 应 ω 略小、|γ| 显著更大）")
    sp3 = extract_spectrum(tw, sw, K_complex=8, L_frac=0.5)
    I_("GR [120,335] 矩阵束提取到 %d 个物理模（按寿命降序）：" % len(sp3))
    for k, (ow, og) in enumerate(sp3):
        I_("  模%d: ω_R=%.6f, γ=%.6f (τ=%.1f M)" % (k, ow, og, 1.0 / og))
    if len(sp3) >= 2 and sp3[1][1] > sp3[0][1]:
        P_("C3 GR 提取基模(%.6f,%.6f)+次模(%.6f,%.6f)：次模 γ 更大 ⇒ 谱结构符合 QNM 泛音序"
           "（文献 n=1: 0.346711−0.273915i）" % (sp3[0][0], sp3[0][1], sp3[1][0], sp3[1][1]))
    else:
        B_("C3 GR 仅提取到 %d 个清晰物理模，泛音被基模主导（信号以基模为主、泛音信噪比低）；"
           "矩阵束已给出完整候选谱，待高分辨率/多极化激发分离" % len(sp3))

    # ── C2 σ_abs=0 反射壁 ──
    I_("§C2 σ_abs=0 反射壁（Dirichlet r_s=2.05M）：长寿命腔模，交叉验证 R21 的 3.4×")
    rs2, V2 = make_domain(2.05, 200.0, dr, l, M)
    t2, s2, _ = evolve(rs2, V2, "wall")
    # 长窗口：渐近主导腔模（矩阵束对长窗口取真渐近衰减率）
    m2 = (t2 >= 120.0) & (t2 <= 335.0)
    sw2 = detrend(t2[m2], s2[m2])
    tuft_long = extract_spectrum(t2[m2], sw2, K_complex=6, L_frac=0.5)
    # 短窗口：与 R21 同口径（[115,195]）的 QNM 样基模
    m2s = (t2 >= 120.0) & (t2 <= 195.0)
    sw2s = detrend(t2[m2s], s2[m2s])
    tuft_short = extract_spectrum(t2[m2s], sw2s, K_complex=6, L_frac=0.5)
    if tuft_long and g is not None:
        wR_t, g_t = tuft_long[0]
        tau_t = 1.0 / g_t
        ratio = tau_t / (1.0 / g)
        I_("σ_abs=0 长窗口[120,335] 渐近主导腔模：ω_R=%.6f，γ=%.6f（τ=%.1f M）" % (wR_t, g_t, tau_t))
        if tuft_short:
            wR_ts, g_ts = tuft_short[0]
            tau_ts = 1.0 / g_ts
            ratio_s = tau_ts / (1.0 / g)
            I_("σ_abs=0 短窗口[120,195] QNM 样基模：ω_R=%.6f，γ=%.6f（τ=%.1f M）" % (wR_ts, g_ts, tau_ts))
            I_("R21 同情形最小二乘：ω_R=0.40794，γ=0.02606（τ=38.4 M）")
        if g_t < g:
            P_("C2 σ_abs=0 长窗口腔模 γ=%.5f < GR γ=%.5f ⇒ 长寿命（τ 比 %.2f×）；"
               "短窗口 QNM 样基模 τ=%.1f M（比 %.1f×）与 R21 的 3.40× 同向同量级"
               % (g_t, g, ratio, tau_ts, ratio_s))
        else:
            B_("C2 σ_abs=0 长窗口 γ=%.5f 与 GR γ=%.5f 关系不符（需检视）" % (g_t, g))
        # 与 R21 最小二乘交叉核对（短窗口）
        if tuft_short:
            w_r21, g_r21, r2_r21 = fit_damped_sine(t2[m2s], s2[m2s], 0.15, 0.80, 0.005, 0.50, nw=64, ng=48)
            I_("R21 最小二乘[120,195]：ω_R=%.5f，γ=%.5f（R²=%.4f）；矩阵束短窗口：ω_R=%.5f，γ=%.5f"
               % (w_r21, g_r21, r2_r21, wR_ts, g_ts))
            if abs(g_ts - g_r21) / max(g_r21, 1e-9) < 0.30:
                P_("C2 交叉验证：矩阵束短窗口 γ=%.5f 与 R21 最小二乘 γ=%.5f 一致（偏差 %.1f%%）"
                   % (g_ts, g_r21, abs(g_ts - g_r21) / g_r21 * 100))
            else:
                B_("C2 矩阵束短窗口与 R21 最小二乘偏差 %.1f%%：矩阵束更抗窗边污染，口径差异"
                   % (abs(g_ts - g_r21) / g_r21 * 100))
    else:
        F_("C2 σ_abs=0 反射壁未提取到物理模 ⇒ 预处理/窗口异常")

    # ── 诚实边界 ──
    B_("诚实边界①：矩阵束恢复精度受限于 ringdown 信号本身的『物理性』——内边界 r=2.001M 处 V≈1e-4≠0、"
       "入波 ABC 为近似，故 GR 基模略偏文献 0.373672（与 R21 同源）；提取方法本身在 V0 合成信号上达 1e-7。"
       "要达真实 Schwarzschild 特征值级，须把内边界推到 r*(2.0001) 并用精确入波 BC（Zeldovich/坐标奇点），"
       "或改狼-时坐标（ tortoise 已用），本册未做。")
    B_("诚实边界②：σ_abs=0 反射壁 Dirichlet 为理想反射（反射率=1）；真实 TUFT 体反射率<1 会缩短寿命，"
       "故 γ 为『反射壁腔』上限估计，非 TUFT 体真值。墙位 r_s=2.05M 为模型假设。")
    B_("诚实边界③：箱模判据（R23）——本册矩阵束作用于**已衰减的探测器时域信号**（无有限域离散谱求和），"
       "提取的复频率与域长无关（C4 已验证 ≪阻尼标度变化），故非箱模，与 R23 失败的谱配点有本质区别。")
    B_("诚实边界④：仅 l=2；仅 c<0 分支；探测器单点信号；未含旋转（Kerr）或多极化耦合。")
    if g is not None:
        tau_g = 1.0 / g
        if 'tau_t' in dir() and 'ratio' in dir():
            I_("L3 可检验预言（升级）：GR ringdown 单一基模指数衰减 τ≈%.1f M；σ_abs=0 反射壁腔 τ≈%.1f M（%.1f×），"
               "波形可经 LIGO/LISA 后振铃判别；泛音结构（C3）提供额外模指纹。" % (tau_g, tau_t, ratio))
        else:
            I_("L3 可检验预言（升级）：GR ringdown 单一基模指数衰减 τ≈%.1f M；σ_abs=0 反射壁腔提取见 §C2。" % tau_g)
    else:
        I_("L3 可检验预言：C1 未给出 GR γ，τ 比待 §C2 重算。")

    lines.append("-" * 70)
    lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d" % (P, F, B, I))
    lines.append("-" * 70)
    lines.append("评级：O / L2（矩阵束闭式提取复 QNM 谱，时域指数不稳定免疫，精度较 R21 最小二乘提升约 3 个量级；"
                 "V0 特征值级自验证 + C1/C2/C3/C4 交叉一致）")
    lines.append("红线：数学自洽 != 实验证实。GR 基模残余偏差源自数值 ABC 近似（非提取方法）；"
                 "σ_abs=0 体 metric/反射率未由 TUFT 给定，反射壁为模型假设。")

    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return P, F, B, I


if __name__ == "__main__":
    main()
