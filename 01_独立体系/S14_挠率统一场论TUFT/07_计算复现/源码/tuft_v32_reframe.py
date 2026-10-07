# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支 TS8 —— 证伪后理论重定位：合法贡献 vs 已证伪部分切割
================================================================================
承接 C0091 证伪，做建设性重定位。核心洞察：

  模型复现 g_e 的"空间延展" ⟨r⟩/λ_C − 1，数值上恰好等于 QED 反常磁矩 a_e：
        ⟨r⟩/λ_C = 1 + a_e ,   a_e = α/2π − 0.328α²/π² + 1.18α³/π³ − ...
  ⇒ "以延展复现 g_e"本质是把 QED 的 α/π 量子修正折叠进几何；
    C0091 证伪正确地拒绝把它当作真实电荷空间延展。

  重定位（合法贡献切割）：
    (S1) 涌现 λ_C 处，几何自然给出 狄拉克 g=2（C0081：g=2 干净涌现，无需自旋量子）✓ 保留
    (S2) 反常部分 (g_e−2)/2 = a_e = QED α/2π − …，非空间延展 ⇒ 归还标准 QED ✓ 切割
    (S3) 经典可观测量（M,N,Q,μ,a_0,R_H）由 {M_e,α} 统一复现 ⇒ 保留（与反常无关）
    (S4) C0085 形状因子 C(ω) 在电子尺度被证伪 ⇒ 仅可作为亚电子尺度模型预言，非电子实态

  结论：TUFT 合法范围 = 两尺度几何统一经典/原子可观测量 + 涌现狄拉克 g=2；
        反常磁矩 α/π 属 QED 量子修正，非空间延展。原"无需量子圈"主张放弃。
================================================================================
"""
from __future__ import print_function
import os, sys, math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_reframe_report.txt")

ALPHA = 1.0 / 137.035999084

# QED 反常磁矩 a_e = α/2π − 0.328411 α²/π² + 1.181 α³/π³ − ...（Schwinger + 高阶）
a_e = ALPHA/(2*math.pi) - 0.328411*(ALPHA**2)/(math.pi**2) + 1.181*(ALPHA**3)/(math.pi**3)
g_e_qed = 2.0 + 2.0*a_e
g_e_codata = 2.00231930436

# 模型延展（C0057/81 拟合 g_e 的 ⟨r⟩/λ_C）
rbar_over_lC = g_e_codata / 2.0          # 由 g=2⟨r⟩/λ_C 反推
ext_model = rbar_over_lC - 1.0           # 模型所需延展

# 比值：模型延展 vs QED a_e（应 ≈1）
ratio = ext_model / a_e

buf = []
log = buf.append
log("TUFT V3.2 分支TS8 · 证伪后理论重定位：合法贡献 vs 已证伪部分切割")
log("运行时间: 2026-10-07  Python %s" % sys.version.split()[0])
log("")
log("=== 核心洞察：延展 = QED 反常磁矩 ===")
log("  QED a_e = α/2π − 0.328α²/π² + 1.181α³/π³ = %.10f" % a_e)
log("  QED g_e = 2 + 2a_e = %.10f (vs CODATA %.10f)" % (g_e_qed, g_e_codata))
log("  模型所需延展 ⟨r⟩/λ_C − 1 = g_e/2 − 1 = %.10f" % ext_model)
log("  比值 (⟨r⟩/λ_C−1)/a_e = %.4f" % ratio)
log("  ⇒ 模型延展在数值上 == QED a_e（比值≈1）⇒ '延展复现 g_e'= 把 α/π 折叠进几何")
log("")
log("=== 重定位（合法贡献切割）===")
log("  S1 涌现 λ_C 处几何给 狄拉克 g=2（C0081，无需自旋量子）—— 保留 ✓")
log("  S2 反常部分 a_e 为 QED α/π 量子修正，非空间延展 —— 归还标准 QED ✓")
log("  S3 经典可观测量 M,N,Q,μ,a_0,R_H 由 {M_e,α} 统一复现 —— 保留 ✓（与反常无关）")
log("  S4 C0085 形状因子 C(ω) 在电子尺度被证伪 —— 仅作亚电子尺度模型预言，非电子实态")
log("")
log("=== 结论 ===")
log("  TUFT 合法范围 = 两尺度几何统一经典/原子可观测量 + 涌现狄拉克 g=2；")
log("  反常磁矩 α/π 属 QED 量子修正，非空间延展。原'无需量子圈'主张放弃。")
log("  诚实分级：S1/S3 保留（与证伪无关）；S2 切割（归还 QED）；S4 降级为亚尺度预言。")

text = "\n".join(buf) + "\n"
print(text)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(text)
