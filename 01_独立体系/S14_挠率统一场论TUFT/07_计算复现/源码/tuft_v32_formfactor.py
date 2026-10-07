# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支 TS4 —— 两尺度电子的弹性形状因子与辐射修正 C(omega)
================================================================================
目标：闭合源稿三观测量(M,Q,mu)+g 之外最后一个未完成项：辐射修正 C（C0051 挂账）。

源稿 C=(1/N)∫4πr⁴ρ(3V1ρ−5V2ρ²)dr 依赖电荷场自耦合 V1,V2（几何 ansatz 无此量 ⇒ 不可算）。
本脚本给出物理动机明确、由涌现结构唯一确定的辐射修正：

  两尺度电子的电荷/磁晕 ρ_Q=A·e^{-r/l_Q}（涌现尺度，⟨r⟩_charge=1.00116·λ_C，C0081）。
  其弹性形状因子 F(q)=∫ρ e^{iq·r} d³r = [1/(1+(q·l_Q)²)]²（exp 晕的 3D Fourier）。
  辐射修正（相对点电荷 Larmor）：C(w) = |F(q)|²,  q=w/c
        C(w) = [1/(1+(w·l_Q/c)²)]^4
  · w→0：C→1（Larmor 恢复，总电荷守恒保证软光子不变）
  · w~c/λ_C（康普顿频率）：形状延展开始压制辐射 ⇒ 偏离 Larmor
  · 小 q 展开：F(q)≈1−⟨r²⟩_charge q²/6（连接形状矩 ⟨r²⟩=12·l_Q²）

与源稿 C 的关系（如实）：源稿 C 是依赖 V1,V2 的抽象积分（其孤子本身不可归一化，C0039–47 已证伪）；
本 C(w) 以可计算、可观测的形式兑现源稿"强加速粒子辐射偏离 Larmor"的物理意图，是两尺度结构的
可测预言，而非对源稿公式的字面复算。

红线声明：电荷/磁晕映射仍为模型假设（C0051）；本 C(w) 为两尺度模型的可观测预言，非物理真实主张。
================================================================================
"""
from __future__ import print_function
import os, sys, math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_formfactor_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
GE_EXP = 2.00231930436
OMEGA_DE = 0.6875

import numpy as np
r = np.logspace(-3.0, 2.0, 4000)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
T = Tc * np.exp(-r / lT)
Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
M_nat = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
lamC_nat = 1.0 / M_nat
lamC_m = lamC_nat * L_PLANCK

# 电荷晕：⟨r⟩_charge=1.00116·λ_C（g_e 一致，C0081），exp 晕 ⟨r⟩=3·l_Q
rbar = 1.00116 * lamC_m
l_Q = rbar / 3.0
lamC_freq = C_LIGHT / lamC_m          # 康普顿圆频率
r2bar = 12.0 * l_Q ** 2               # exp 晕 ⟨r²⟩=12 l_Q²

def F(q):                              # 弹性形状因子 F(q)=[1/(1+(q l_Q)²)]²
    x = q * l_Q
    return 1.0 / (1.0 + x * x) ** 2

def Cw(w):                             # 辐射修正 C(ω)=|F(ω/c)|²
    return F(w / C_LIGHT) ** 2

buf = []
log = buf.append

log("TUFT V3.2 分支TS4 · 两尺度电子弹性形状因子与辐射修正 C(w)")
log("运行时间: 2026-10-07  Python %s" % sys.version.split()[0])
log("质量核 M_nat=%.6e 普朗克(=M_e)；λ_C=%.6e m；电荷晕 l_Q=%.6e m（⟨r⟩=1.00116λ_C）" % (M_nat, lamC_m, l_Q))
log("")
log("=== 弹性形状因子 F(q) = [1/(1+(q l_Q)^2)]^2 ===")
log("  形状矩 ⟨r²⟩_charge = 12·l_Q² = %.6e m²" % r2bar)
log("  小 q 展开：F(q) ≈ 1 − ⟨r²⟩ q²/6 = 1 − %.4e q²（对应均方半径）" % (r2bar / 6.0))
f1, f2, f3 = F(1.0 / l_Q), F(2.0 / l_Q), F(3.0 / l_Q)
log("  F(q=1/l_Q) = %.4f ; F(q=2/l_Q) = %.4f ; F(q=3/l_Q) = %.4f" % (f1, f2, f3))
log("")
log("=== 辐射修正 C(w) = |F(w/c)|^2 = [1/(1+(w l_Q/c)^2)]^4 ===")
log("  康普顿圆频率 w_C = c/λ_C = %.4e rad/s" % lamC_freq)
log("  C(w→0) = 1.000000（Larmor 恢复，总电荷守恒）")
log("  C(w=w_C) = %.6f（w_C·l_Q/c = l_Q/λ_C = %.4f ⇒ 偏离 %.4f%%）"
    % (Cw(lamC_freq), l_Q / lamC_m, (1 - Cw(lamC_freq)) * 100))
log("  C(w=2w_C) = %.6f（偏离 %.2f%%）" % (Cw(2 * lamC_freq), (1 - Cw(2 * lamC_freq)) * 100))
log("  C(w=3w_C) = %.6f（偏离 %.2f%%）" % (Cw(3 * lamC_freq), (1 - Cw(3 * lamC_freq)) * 100))
log("  C(w=10w_C) = %.6f（偏离 %.4f%%）" % (Cw(10 * lamC_freq), (1 - Cw(10 * lamC_freq)) * 100))
from scipy.optimize import brentq
wh = brentq(lambda w: Cw(w) - 0.5, 0, 50 * lamC_freq)
log("  半功率点：C(w_½)=1/2 于 w_½ = %.4f·w_C（辐射功率减半的频率）" % (wh / lamC_freq))
log("")
log("=== 结论（两尺度电子的可测辐射预言）===")
log("  1) C(w) 由涌现结构唯一确定（无 V1,V2 假设）：F(q) 为 exp 晕的 3D Fourier。")
log("  2) 低频 C→1（Larmor 恢复）；辐射偏离从康普顿频率起显著：C(w_C)=%.4f、C(3w_C)=%.4f。"
    % (Cw(lamC_freq), Cw(3 * lamC_freq)))
log("  3) 特征偏离频率 w_C=c/λ_C = c·M/ħ（质量定标）⇒ 强加速辐射偏离 Larmor 的量表是康普顿频率。")
log("  4) 小 q 形状因子由 ⟨r²⟩ 定（连接 C0082 形状矩）；这是可被 e-p 散射/高能辐射检验的预言。")
log("  5) 源稿 C（V1,V2 抽象积分）不可算（C0051 挂账）；本 C(w) 以可观测形式兑现其物理意图，")
log("     非对源稿公式字面复算。")
log("红线声明：电荷/磁晕映射为模型假设（C0051）；本 C(w) 为两尺度模型可观测预言，非物理真实主张。")

text = "\n".join(buf) + "\n"
print(text)
try:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
except Exception as exc:
    log("[warn] 报告写入失败: %s" % exc)
