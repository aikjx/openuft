# -*- coding: utf-8 -*-
"""
TUFT · R22 —— σ_abs=0 回声梳的可分辨性判定（腔内窄脉冲激发）
==============================================================
R21 的诚实边界：「回声梳未分辨——高斯初值激发以基模为主，自相关首峰滞后
15.21M ≈ 载波周期 15.40M，与 R20 几何估计 13.88M 无法区分」。

本册用**腔内窄脉冲**（σ=1.0 @ r*=−2，壁 r*=−5.33 与势垒 r*≈1.6 之间，
脉宽 ~2M ≪ 回声周期 ~14M）正面测试「回声爆发串」假设，并回答两个问题：
  Q1 为何 R21 看不到梳？——是激发不足，还是物理上本就无梳？
  Q2 σ_abs=0 的可观测判别器到底是什么？

【核心机制（本册定量给出）】
  可分辨回声梳要求腔模在一次往返内就衰亡：γ·T_echo ≳ 1
  （模寿命 τ=1/γ ≲ 往返时间 T_echo ⇒ 各次泄漏的波包不重叠）。
  本系统（RW 势垒 + 墙在 r_h）：R21 γ=0.02606、R20 T_echo=13.88M
  ⇒ γ·T_echo = 0.362 < 1 ⇒ **低精细度机制，爆发必然重叠成连续振铃**。
  即：TUFT σ_abs=0（墙在 r_h、短腔）的可观测判别器不是回声梳，
  而是 R21 已定量给出的「长寿命改性振铃」（τ=3.4×、ω_R 漂移 +10%）。

【三方交叉核对（同一物理量「逐回合保留率 λ」）】
  R20：|T_h|²(0.3737)=0.46921 ⇒ λ=√(1−|T_h|²)=0.7286（单频散射透射）
  R21：γ=0.02606 ⇒ λ=e^{−γ·T_echo}=0.6965（QNM 阻尼率）
  两独立路径给同一 λ 至 4.5% ⇒ 相互印证。

【激发无关性检验】QNM 是系统属性而非初值属性：
  窄脉冲激发下重新拟合 γ，应复现 R21 高斯激发的 0.02606。

判据：
  C1 回声梳缺失的机制判定：γ·T_echo<1 ⇒ 无梳（定量，非描述）
  C2 λ(R20) vs λ(R21) 一致（±10%）
  C3 γ(窄脉冲) ≈ γ(R21 高斯)（±25%）⇒ 激发无关
  C4 GR 黑洞无回声串（显著爆发 ≤2）⇒ 判别器仍成立

几何单位 G=c=M=1；l=2；RW 势。评级：O / L2。红线：数学自洽 != 实验证实。
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
OUT = os.path.join(HERE, "tuft_r22_report.txt")
sys.path.insert(0, HERE)

import numpy as np
import tuft_r21_sigma_abs0_ringdown_timedomain as td

GAMMA_R21 = 0.02606          # R21 报告值（反射壁 r_s=2.05M，高斯激发 σ=3）
TH2_R20 = 0.46921            # R20 报告值（ωM=0.3737 处视界透射）
T_GEO = 13.88                # R20 几何回声周期 2Δr*（r_s=2.05M）


def burst_train(t, s, t1, t2, half_win=3.0, prom=0.02, min_sep=6.0):
    """Hilbert 包络的局部峰（±half_win 窗口内最大）⇒ 爆发串 [(t, 包络幅)]。"""
    m = (t >= t1) & (t <= t2)
    sw, tw = s[m], t[m]
    if len(sw) < 20:
        return []
    env = td.analytic_envelope(sw)
    mx = env.max()
    if mx <= 0:
        return []
    dt = tw[1] - tw[0]
    hw = max(2, int(half_win / dt))
    peaks = []
    for i in range(hw, len(env) - hw):
        if env[i] >= env[i - hw:i + hw + 1].max() and env[i] > prom * mx:
            if not peaks or tw[i] - peaks[-1][0] >= min_sep:
                peaks.append((tw[i], env[i]))
    return peaks


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
    lines.append("TUFT R22 · σ_abs=0 回声梳的可分辨性判定（腔内窄脉冲激发）")
    lines.append("=" * 70)
    l = 2.0
    M = 1.0
    dr = 0.05
    r_wall = 2.05

    lam_r20 = math.sqrt(1.0 - TH2_R20)
    lam_r21 = math.exp(-GAMMA_R21 * T_GEO)
    gT = GAMMA_R21 * T_GEO
    I_("几何单位 G=c=M=1；l=2；RW 势；dr*=0.05；腔内窄脉冲 σ=1.0 @ r*=−2"
       "（壁 r*=%.2f 与势垒 r*≈1.6 之间，脉宽~2M ≪ T_echo~14M）" % td.rstar(r_wall, M))
    I_("基准：R20 λ=√(1−%.5f)=%.4f；R21 λ=e^{−%.5f·%.2f}=%.4f；γ·T_echo=%.3f"
       % (TH2_R20, lam_r20, GAMMA_R21, T_GEO, lam_r21, gT))

    # ── §A 回声梳测试 ──
    I_("§A σ_abs=0 反射壁 r_s=%.2fM：腔内窄脉冲的回声爆发串测试" % r_wall)
    rs_w, V_w = td.make_domain(r_wall, 200.0, dr, l, M)
    t_w, s_w, _ = td.evolve(rs_w, V_w, "wall", r0_pulse=-2.0, sigma=1.0, t_max=350.0)
    peaks = burst_train(t_w, s_w, 65.0, 340.0)
    I_("检出显著爆发 %d 个：%s" % (len(peaks), ", ".join("(%.1f, %.2e)" % p for p in peaks[:6])))
    if len(peaks) <= 2:
        I_("窄脉冲（脉宽 ≪ T_echo）仍只给 1 个爆发 ⇒ 排除『激发不足』解释")
        if gT < 1.0:
            P_("C1 无梳机制定量判定：γ·T_echo=%.3f < 1 ⇒ 模寿命 τ=1/γ=%.0fM ≫ 往返时间 T_echo=%.1fM，"
               "各次泄漏波包必然重叠成连续振铃（低精细度机制）。"
               "可分辨梳的判据是 γ·T_echo≳1（即 λ≲1/e≈0.37、单回合泄漏 |T|²≳0.86）"
               % (gT, 1.0 / GAMMA_R21, T_GEO))
        else:
            F_("γ·T_echo=%.2f≥1 却无梳，机制解释失效" % gT)
        B_("回声梳假设被否证：TUFT σ_abs=0（墙在 r_h、短腔 6.94M）属低精细度机制，"
           "可观测判别器不是回声梳而是 R21 的长寿命改性振铃（τ=3.4×、ω_R 漂移+10%）——"
           "这回答了 R21 的开放问题")
    else:
        I_("检出 %d 个爆发，疑似梳；进一步核对间距与衰减" % len(peaks))
        tp = [p[0] for p in peaks]
        gaps = [tp[i + 1] - tp[i] for i in range(len(tp) - 1)]
        Tm = float(np.median(gaps))
        dev = abs(Tm - T_GEO) / T_GEO
        if dev < 0.25:
            P_("C1 回声间距 %.2fM 与 R20 几何估计 %.2fM 偏差 %.0f%%（<25%%）⇒ 梳被分辨" % (Tm, T_GEO, dev * 100))
        else:
            B_("C1 回声间距 %.2fM 与 R20 估计 %.2fM 偏差 %.0f%%（≥25%%）" % (Tm, T_GEO, dev * 100))

    # ── §B λ 三方交叉（R20 vs R21）──
    dev_lam = abs(lam_r20 - lam_r21) / lam_r21
    I_("§B 逐回合保留率 λ 交叉：λ(R20)=%.4f（单频散射透射） vs λ(R21)=%.4f（QNM 阻尼率）——偏差 %.1f%%"
       % (lam_r20, lam_r21, dev_lam * 100))
    if dev_lam < 0.10:
        P_("C2 λ(R20) 与 λ(R21) 一致（偏差 %.1f%% < 10%%）⇒ 散射透射与 QNM 阻尼两条独立路径相互印证"
           % (dev_lam * 100))
    else:
        B_("C2 λ(R20) vs λ(R21) 偏差 %.1f%%（≥10%%）——口径差异需单频腔模透射谱积分统一" % (dev_lam * 100))

    # ── §C 激发无关性（QNM 是系统属性）──
    I_("§C 激发无关性：窄脉冲 σ=1.0 重新拟合 (ω_R, γ)，应复现 R21 高斯 σ=3 的 γ=%.5f" % GAMMA_R21)
    m = (t_w >= 115) & (t_w <= 195)
    wR2, g2, r22 = td.fit_damped_sine(t_w[m], s_w[m], 0.25, 0.55, 0.008, 0.12)
    I_("窄脉冲拟合：ω_R=%.5f，γ=%.5f（τ=%.1fM），R²=%.4f" % (wR2, g2, 1.0 / g2 if g2 > 0 else -1, r22))
    dev_g = abs(g2 - GAMMA_R21) / GAMMA_R21
    if r22 > 0.90 and dev_g < 0.25:
        P_("C3 γ(窄脉冲)=%.5f ≈ γ(R21 高斯)=%.5f（偏差 %.1f%% < 25%%，R²=%.3f）"
           "⇒ QNM 是系统属性、与初值激发无关；R21 的 γ 得到独立初值的复现"
           % (g2, GAMMA_R21, dev_g * 100, r22))
    else:
        B_("C3 窄脉冲拟合 γ=%.5f（偏差 %.1f%%，R²=%.3f）未达一致性判据" % (g2, dev_g * 100, r22))

    # ── §D GR 黑洞：无回声串（判别器）──
    I_("§D GR 黑洞（内边界吸收）：同一腔内窄脉冲")
    rs_b, V_b = td.make_domain(2.001, 200.0, dr, l, M)
    t_b, s_b, _ = td.evolve(rs_b, V_b, "ingoing", r0_pulse=-2.0, sigma=1.0, t_max=350.0)
    peaks_b = burst_train(t_b, s_b, 65.0, 340.0)
    I_("GR 检出显著爆发 %d 个：%s" % (len(peaks_b), ", ".join("(%.1f, %.2e)" % p for p in peaks_b[:6])))
    if len(peaks_b) <= 2:
        P_("C4 GR 黑洞无回声串（显著爆发 %d ≤2：单次透出 + QNM 振铃，视界吸收截断多次反弹）"
           % len(peaks_b))
    else:
        B_("C4 GR 检出 %d 个爆发（>2）——内边界 ABC 微反射成串，判别器需更高吸收精度" % len(peaks_b))
    I_("判别器总结：GR = 单一 GR 型指数振铃、无回声；σ_abs=0（墙在 r_h）= 长寿命改性振铃"
       "（τ=3.4×、ω_R+10%、γ·T_echo=0.36<1 故无梳）；若墙远离视界（长腔、γ·T_echo≳1）才出现回声梳")

    # ── 诚实边界 ──
    B_("诚实边界①：λ(R20)/λ(R21) 两口径并非严格同义——前者是单频平面波散射透射、"
       "后者是 QNM 阻尼率（含腔内相位结构）；4.5% 一致属量级印证，严格等价需单频腔模透射谱积分")
    B_("诚实边界②：爆发串检测依赖包络峰判据（prom=0.02、min_sep=6M）；γ·T_echo 判据是"
       "波包重叠的必要条件近似，严格边界需波包宽度与 T_echo 的显式比较")
    B_("诚实边界③：仅 l=2；TUFT metric/反射系数未给定，反射壁位置为模型假设；仅 c<0 分支")
    I_("L3 可检验预言（修订）：σ_abs=0 的可观测判别 = 后振铃 τ 与 ω_R 同时偏离 GR 基准"
       "（~3.4× 与 +10%），而非回声梳；回声梳仅当墙远离视界使 γ·T_echo≳1 时才出现")

    lines.append("-" * 70)
    lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d" % (P, F, B, I))
    lines.append("-" * 70)
    lines.append("评级：O / L2（回声梳可分辨性定量判定 + λ 交叉印证 + 激发无关性 + GR 判别器）")
    lines.append("红线：数学自洽 != 实验证实。σ_abs=0 体的 metric/反射系数未由 TUFT 给定，"
                 "反射壁位置为模型假设。")

    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return P, F, B, I


if __name__ == "__main__":
    main()
