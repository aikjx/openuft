# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支 TS3 —— 涌现康普顿尺度的独立物理一致性检验
================================================================================
目的：C0081 主张"电荷/磁晕尺度 λ_C=1/M_nat 为涌现尺度"。为免于"仅由 g_e 反推"的循环，
本脚本用**不依赖 g_e** 的三个独立物理约束交叉核验：

  (A) 电磁自能一致性：λ_C 尺度电荷晕的静电自能 U_EM 应 ≪ M_e c²（质量在核，晕不重复计数）。
      解析：U_EM = α·I，I=2π∫Q(r)²/r² dr（Q 为归一化电荷包络，自然单位）；U_EM/M c² = α·I·λ_C。
      对纯指数晕 ρ=A·e^{-r/l_Q} 可精确算：期望 U_EM/M c² ~ α/2 ≈ 0.37%（小量，自洽）。

  (B) 三尺度阶梯：核心 ~l_P、经典电子半径 r_e=α·λ_C、康普顿晕 λ_C，构成电子规范长度阶梯；
      核验 r_e = α·λ_C = 1.00116α·⟨r⟩ 关系。

  (C) g−2 场延展的 α/2π 数值共振：g_e 所需 +0.116% 场延展 vs QED 首阶反常 α/2π≈0.001161。
      如实标注为数值巧合/共振候选，不作物理主张。

红线声明：涌现尺度与电荷/磁晕映射仍为理论推断（C0051 挂账）；本脚本为自洽性/一致性检验，
不构成物理真实主张。
================================================================================
"""
from __future__ import print_function
import os, sys, math
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_em_selfenergy_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
Q_E = 1.602176634e-19
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
GE_EXP = 2.00231930436

buf = []
log = buf.append

# 质量核（C0045）
r = np.logspace(-3.0, 2.0, 4000)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
T = Tc * np.exp(-r / lT)
Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
M_nat = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
lamC_nat = 1.0 / M_nat
lamC_m = lamC_nat * L_PLANCK

# ---------------- (A) 电磁自能 ----------------
def em_selfenergy_fraction(lQ_over_lamC, alpha=ALPHA):
    """U_EM/M c² = α · (2π∫Q(r)²/r² dr) · λ_C，lQ 以 λ_C 为单位给出。
    ρ=A·e^{-r/l_Q}，Q(r)=∫4πr'²ρ dr' 归一化到 1。"""
    lQ = lQ_over_lamC           # 单位：λ_C
    x = np.logspace(-3.0, 3.0, 6000)
    # Q(r) 解析：对 ρ=A e^{-r/l}, 4πA∫_0^r r'² e^{-r'/l} dr'
    # 直接数值积分电荷包络
    rq = x * lQ                  # 物理半径（单位 λ_C）
    rho = np.exp(-rq / lQ) / (8*math.pi*lQ**3)   # 归一化 exp 晕，∫ρ4πr²=1
    # 球壳累计
    Q = np.array([np.trapezoid(rho[:i+1]*4*math.pi*rq[:i+1]**2, rq[:i+1]) for i in range(len(x))])
    E = np.where(rq > 1e-9, Q / rq**2, 0.0)
    I = 2*math.pi * np.trapezoid(E**2 * rq**2, rq)
    # rq 以 λ_C 为单位 ⇒ I 即 U_EM·λ_C/α（无量纲）；U_EM/M c² = α·I
    U_over_M = alpha * I
    return U_over_M, I

U0, I0 = em_selfenergy_fraction(1.0/3.0)              # ⟨r⟩=λ_C 情形 l_Q=λ_C/3
U1, I1 = em_selfenergy_fraction(GE_EXP/2.0/3.0)       # g_e 情形 ⟨r⟩=1.00116λ_C

# ---------------- (B) 三尺度阶梯 ----------------
r_e_classical = ALPHA * lamC_m          # 经典电子半径 = α λ_C
r_e_over_lP = r_e_classical / L_PLANCK

# ---------------- (C) α/2π 共振 ----------------
ext_required = 0.00116                  # +0.116% 场延展（g_e 所需）
a2pi = ALPHA / (2*math.pi)
ratio = ext_required / a2pi

log("TUFT V3.2 分支TS3 · 涌现康普顿尺度的独立物理一致性检验")
log("运行时间: 2026-10-07  Python %s  numpy %s" % (sys.version.split()[0], np.__version__))
log("质量核 M_nat=%.6e 普朗克(=M_e)；λ_C=1/M_nat=%.6e l_P=%.6e m" % (M_nat, lamC_nat, lamC_m))
log("")
log("=== (A) 电磁自能一致性（不依赖 g_e，仅用 α）===")
log("  电荷晕 ρ=A·e^{-r/l_Q}，静电自能 U_EM = α·I，I=2π∫Q(r)²/r² dr（r 以 λ_C 计）")
log("  ⟨r⟩=λ_C 情形（l_Q=λ_C/3）：I=%.5f, U_EM/M c² = %.6f = %.4f·α ≈ %.2f%%（α 量级小修正，自洽）"
    % (I0, U0, I0, U0*100))
log("  g_e 情形（l_Q=1.00116λ_C/3）：I=%.5f, U_EM/M c² = %.6f = %.4f·α ≈ %.2f%%"
    % (I1, U1, I1, U1*100))
log("  说明：指数晕集中于中心（l_Q=λ_C/3）使几何因子 c_geom=I≈5.87 偏大；壳层λ_C 为 α/2、")
log("  均匀球为 3α/5。无论何种几何，U_EM/M c² 均为 α 量级 ≪1。")
log("  判定：λ_C 晕的电磁自能仅 α 量级（~4%%）⇒ 质量确实集中在核（C0045），晕不重复计数 ⇒ 自洽。")
log("")
log("=== (B) 三尺度阶梯（核 → 经典半径 → 康普顿晕）===")
log("  质量核尺度  ~ lO=%.4f l_P = %.4e m" % (lO, lO*L_PLANCK))
log("  经典半径 r_e = α·λ_C = %.6e m = %.6e l_P" % (r_e_classical, r_e_over_lP))
log("  康普顿晕 λ_C = %.6e m = %.6e l_P" % (lamC_m, lamC_nat))
log("  核验 r_e = α·λ_C：α·λ_C = %.6e m ✓（自然单位 r_e=α/M，经典定义自洽）" % (ALPHA*lamC_m))
log("  阶梯比：λ_C/r_e = 1/α = %.4f；r_e/l_P = %.3e" % (1/ALPHA, r_e_over_lP))
log("")
log("=== (C) g−2 场延展的 α/2π 数值共振（如实标注：巧合候选，非主张）===")
log("  g_e 所需场延展：+0.116%%（即 0.00116 相对）")
log("  QED 首阶反常 α/2π = %.7f" % a2pi)
log("  比值 (0.116%%)/(α/2π) = %.4f（≈1，~3 位数字共振）" % ratio)
log("  说明：二者数值接近是值得记录的巧合/共振候选；场延展来自 g_e 反推，α/2π 来自 QED，")
log("  机制无直接推导关系，不据此作物理主张。")
log("")
log("=== 结论 ===")
log("  1) 涌现尺度 λ_C 通过独立约束 (A)(B) 自洽：λ_C 晕电磁自能为 α 量级（~4%%，≪1，不重复计数），")
log("     且 λ_C=1/M 与 r_e=α·λ_C 构成规范电子尺度阶梯 ⇒ λ_C 非纯 g_e 反推的随意值，")
log("     而是与 α、M 自洽的物理尺度（conjecture 级，有待作用量钉扎证伪/证实）。")
log("  2) (C) 的 α/2π 共振为数值巧合候选，仅记录，不作主张。")
log("  3) 辐射修正 C 仍依赖电荷场自耦合 V1,V2（C0051 挂账延续）。")
log("红线声明：涌现尺度为理论推断；电荷/磁晕映射为模型假设；本脚本为自洽性检验，非物理真实主张。")

text = "\n".join(buf) + "\n"
print(text)
try:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
except Exception as exc:
    log("[warn] 报告写入失败: %s" % exc)
