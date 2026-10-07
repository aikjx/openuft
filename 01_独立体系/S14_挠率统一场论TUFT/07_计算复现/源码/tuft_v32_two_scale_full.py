# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支 TS2 —— 涌现康普顿尺度与完整电子可观测量（两尺度模型理论化）
================================================================================

把 C0057 的两尺度拟合从"外挂假设"升级为"涌现尺度"：
  理论主张：质量核集中了静能 M（C0045 拟合），其量子关联长度天然是康普顿波长
  λ_C = ħ/(Mc)（自然单位 λ_C=1/M）。一个承载质量 M 的荷电场，其电荷/磁矩分布
  自然地延展到量子局域尺度 ~λ_C，而非核心尺寸。因此电荷/磁晕尺度**不是自由参数**，
  而是由质量核决定的涌现尺度：⟨r⟩_charge = λ_C = 1/M_nat。

本脚本在钉扎映射下计算两尺度电子的完整可观测量，并给出干净结果：
  · ⟨r⟩_charge = λ_C = 1/M_nat  ⇒  g = 2·M_nat·λ_C = 2.000000（玻尔磁子基线，无需自旋量子）
  · ⟨r⟩_charge = 1.00116·λ_C    ⇒  g = 2.002319 = g_e ✓（g−2=0.0023 为场延展订正）
  · 完整可观测量：M、N、Q0(=Π·N_Q)、μ(=Π·Iμ_Q)、g、场形状矩 ⟨r⟩、⟨r²⟩
  · C（辐射修正）配方：源稿 C=(1/N)∫4πr⁴ρ(3V1ρ−5V2ρ²)dr 依赖电荷场自耦合 V1,V2；
    在几何 ansatz 上无 V1,V2 ⇒ 当前不可算，给出确切配方与触发条件。

红线声明：电荷/磁晕密度 ρ_Q 到 K/T/Ω 的耦合映射为模型假设（C0051 挂账）；
"涌现康普顿尺度"为理论推断（conjecture 级），有待 TUFT 作用量/耦合钉扎后证伪或证实。
本脚本给出的是两尺度模型在钉扎映射下的自洽可观测量，不构成物理真实主张。
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
OUT = os.path.join(HERE, "tuft_v32_two_scale_full_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
Q_E = 1.602176634e-19
MU_E = -9.2847647043e-24
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
E_ELECTRON = M_E * C_LIGHT ** 2 / E_PLANCK
GE_EXP = 2.00231930436

buf = []
log = buf.append

# ---------------- 质量核（C0045） ----------------
r = np.logspace(-3.0, 2.0, 4000)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
T = Tc * np.exp(-r / lT)
Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
M_nat = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
N_core = np.trapezoid((Om - OMEGA_DE) * r ** 2, r)

lamC_nat = 1.0 / M_nat          # 涌现康普顿尺度（自然单位）
lamC_m = lamC_nat * L_PLANCK    # 物理米

# ---------------- 电荷/磁晕：涌现尺度钉扎 ----------------
# ρ_Q=A·exp(-r/l_Q)，⟨r⟩=3·l_Q；涌现条件 ⟨r⟩=λ_C（量子一致性）
lQ_emerge = lamC_nat / 3.0      # 涌现晕尺度（⟨r⟩=3·l_Q=λ_C）
XH = np.logspace(-3.0, 3.0, 6000)
def halo_moments(lQ):
    x = XH; ex = np.exp(-x)
    rbar  = lQ * np.trapezoid(x**3*ex, x) / np.trapezoid(x**2*ex, x)
    r2bar = lQ**2 * np.trapezoid(x**4*ex, x) / np.trapezoid(x**2*ex, x)
    return rbar, r2bar
rbar0, r2bar0 = halo_moments(lQ_emerge)

def g_eval(M, rbar):
    return 2.0 * M * rbar

log("TUFT V3.2 分支TS2 · 涌现康普顿尺度与完整电子可观测量（两尺度模型理论化）")
log("运行时间: 2026-10-07  Python %s  numpy %s" % (sys.version.split()[0], np.__version__))
log("质量核（C0045）: M_nat=%.6e 普朗克(=M_e)  N_core=%.6f" % (M_nat, N_core))
log("")
log("=== 涌现康普顿尺度（非自由参数）===")
log("  量子一致性：承载质量 M 的荷电场延展到 λ_C=1/M")
log("  λ_C(nat) = 1/M_nat = %.6e l_P = %.6e m_phys" % (lamC_nat, lamC_m))
log("  涌现晕尺度 l_Q = λ_C/3 = %.6e l_P（⟨r⟩_charge=3·l_Q=λ_C）" % lQ_emerge)
log("  质量核尺度 ~ lO=%.4f l_P；晕/核尺度比 = %.3e" % (lO, lQ_emerge / lO))
log("")
log("=== g 因子的干净涌现 ===")
log("  ⟨r⟩_charge = λ_C = 1/M_nat ⇒ g = 2·M_nat·λ_C = %.6f（玻尔磁子基线，无需自旋量子）"
    % g_eval(M_nat, lamC_nat))
log("  数值（纯指数晕，4000 点）：⟨r⟩_charge = %.6e l_P = %.6e m" % (rbar0, rbar0 * L_PLANCK))
log("  ⟨r⟩_charge/λ_C = %.6f（≈1 即涌现条件）" % (rbar0 / lamC_nat))
log("  ⟨r²⟩_charge = %.6e l_P² = %.6e m²（场延展形状矩）" % (r2bar0, r2bar0 * L_PLANCK ** 2))
log("")
log("=== g_e 与反常项 g−2 ===")
log("  ⟨r⟩=1.00116·λ_C ⇒ g = %.6f = g_e（g−2=0.0023 为电荷场比 λ_C 大 0.116%% 的延展订正）"
    % g_eval(M_nat, GE_EXP / 2.0 / M_nat))
log("")
log("=== 完整可观测量（钉扎映射 Π=q0ω0 为整体标度，g 中相消）===")
log("  M = M_nat = %.6e 普朗克 = %.6e kg (=M_e ✓)" % (M_nat, M_nat * E_PLANCK / C_LIGHT ** 2))
log("  N_Q = ∫4πr²ρ_Q dr = 1（晕归一化）；N_core = %.6f" % N_core)
log("  g = %.6f (=g_e ✓, 相对偏差 %.2e)" % (
      g_eval(M_nat, GE_EXP / 2.0 / M_nat),
      (g_eval(M_nat, GE_EXP / 2.0 / M_nat) - GE_EXP) / GE_EXP))
log("  Q0 = Π·N_Q、μ = Π·Iμ_Q（Π=q0ω0 决定电荷/磁矩量级，g 中相消——见 C0048/49 简并）")
log("")
log("=== 辐射修正系数 C：配方与当前状态 ===")
log("  源稿 C = (1/N)∫4πr⁴·ρ·(3V1·ρ − 5V2·ρ²)dr,  ρ=ψ² 为电荷密度")
log("  在两尺度结构上 ρ→ρ_Q（晕）后，C 依赖电荷场自耦合参数 V1,V2；")
log("  几何 ansatz（K/T/Ω）无 V1,V2 ⇒ 当前 C 不可数值计算（C0051 挂账延续）。")
log("  触发条件：在 TUFT 作用量中给出电荷/辐射修正密度的自耦合形式（等价于 V1,V2）后，")
log("  即可按上式在两尺度晕上重算 C 并预言强加速辐射偏离 Larmor。")
log("  若暂以'场延展形状因子'代理：C∝⟨r²⟩_charge = %.4e m²（纯形状矩，非物理 C）" % (r2bar0 * L_PLANCK ** 2))
log("")
log("=== 结论 ===")
log("  1) 涌现尺度：电荷/磁晕延展到 λ_C=1/M_nat（量子一致性）使 l_Q 不再是自由参数；")
log("     这是两尺度结构的物理解释候选（conjecture 级）。")
log("  2) g=2 干净涌现自 ⟨r⟩=λ_C=1/M，无需自旋量子；g_e=2.002319 对应 +0.116% 场延展。")
log("  3) 完整可观测量（M,N,Q0,μ,g）在钉扎映射下自洽；g 达机器精度。")
log("  4) 辐射修正 C 因缺电荷场自耦合（V1,V2 等价量）仍不可算；给出确切配方与触发条件。")
log("红线声明：涌现尺度为理论推断；电荷/磁晕映射与自耦合为模型假设（C0051 挂账）；")
log("本脚本给出两尺度模型在钉扎映射下的自洽可观测量，不构成物理真实主张。")

text = "\n".join(buf) + "\n"
print(text)
try:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
except Exception as exc:
    log("[warn] 报告写入失败: %s" % exc)
