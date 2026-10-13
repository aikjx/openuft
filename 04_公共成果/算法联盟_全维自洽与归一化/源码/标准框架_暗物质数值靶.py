# -*- coding: utf-8 -*-
"""二十二期·标准框架攻坚 暗物质数值靶（WIMP 热遗迹 + 轴子窗口）（2026-10-14）
热遗迹丰度反推 ⟨σv⟩；WIMP 直接探测约束对比；轴子 m_a-f_a-g_aγ 窗口与 ADMX 上限。
公式为标准近似/公开数值（A 级）。mpmath 250 位。
"""
import mpmath as mp
mp.mp.dps = 250
mp.pretty = True

# ---- 输入（A 级公开）----
Omega_obs = mp.mpf("0.12")          # 观测暗物质丰度 Ωχh²（Planck 2018 区间）
sigma_thermal = mp.mpf("3e-26")     # cm³/s：标准热遗迹交叉截面（⟨σv⟩~3e-26 给出 Ωh²~0.1）
alpha = mp.mpf(1) / mp.mpf("137.035999084")
fa_ref = mp.mpf("1e12")             # GeV：轴子衰变常数参考
ma_ref = mp.mpf("5.7e-6")           # eV：m_a = 5.7 μeV × (1e12 GeV/f_a)

print("===== 暗物质数值靶（250 位）=====")

# ① 热遗迹丰度（近似：Ωχh² ≈ 0.1×(3e-26/⟨σv⟩)）
print("\n① 热遗迹丰度反推（标准近似 Ωχh² ≈ 0.1·(3e-26 cm³/s / ⟨σv⟩)）")
for sv in (mp.mpf("1e-27"), mp.mpf("3e-26"), mp.mpf("1e-25"), mp.mpf("1e-24")):
    Oh2 = mp.mpf("0.1") * sigma_thermal / sv
    print("  ⟨σv⟩=%.0e cm³/s → Ωχh² = %.4f（观测 0.12：%s）" % (sv, Oh2, "符合" if abs(Oh2-Omega_obs)<mp.mpf("0.02") else "不符"))
sv_needed = sigma_thermal * mp.mpf("0.1") / Omega_obs
print("  匹配 Ωh²=0.12 所需 ⟨σv⟩ = %.4e cm³/s（= %.2f × 3e-26）" % (sv_needed, sv_needed/sigma_thermal))

# ② WIMP 直接探测约束（XENONnT/LZ 公开上限）
print("\n② WIMP 直接探测（XENONnT 2023-2024 上限，A 级）")
xenon = [(mp.mpf("6"), mp.mpf("1.7e-46")), (mp.mpf("50"), mp.mpf("2.6e-47")), (mp.mpf("1000"), mp.mpf("7e-44"))]
print("  m_χ(GeV)   σ_SI上限(cm²)")
for m, s in xenon:
    print("  %8d   %.2e" % (m, s))
print("  判据：WIMP 若为热遗迹（⟨σv⟩=3e-26），其 SI 截面需 ≤ 上限——50 GeV 处已达 2.6e-47 cm² 灵敏度")

# ③ 轴子（QCD 轴子：m_a-f_a、g_aγ、ADMX 窗口）
print("\n③ QCD 轴子窗口")
print("  m_a = 5.70 μeV × (10¹² GeV/f_a)")
for fa in (mp.mpf("1e10"), mp.mpf("1e11"), mp.mpf("1e12"), mp.mpf("1e13")):
    ma = ma_ref * fa_ref / fa
    print("  f_a=%.0e GeV → m_a = %.6f μeV" % (fa, ma*mp.mpf("1e6")))
C_KSVZ = mp.mpf("0.97"); C_DFSZ = mp.mpf("0.72")
for name, C in (("KSVZ", C_KSVZ), ("DFSZ", C_DFSZ)):
    g_KSVZ = alpha/(2*mp.pi*fa_ref) * C
    print("  %s：g_aγ(f_a=1e12) = %.4e GeV⁻¹（ADMX 灵敏度 ~1.6e-15 GeV⁻¹ 在 3-4 μeV——f_a 需 ~1e12 可及）" % (name, g_KSVZ))
print("  ADMX 现状（A 级）：已扫描 2.86-4.32 μeV 部分；g_aγ<1.6e-15 GeV⁻¹（2024-2025 更新）——未探测")

# ④ 与统一框架能标交叉
print("\n④ 能标交叉（暗物质 ↔ 统一框架）")
print("  PQ 破缺能标 f_a ~ 1e11-1e12 GeV（轴子窗口）比 M_GUT=2.3792e16 GeV 低 4-5 个数量级")
print("  WIMP TeV 标度 ↔ 超对称 sfermion 标度（未发现——B 线生死线关联）")
print("  暗物质与引力/量子引力无直接耦合证据——统一场论功能 F1-F5 均不覆盖暗物质（C 级开放）")

print("\n-- 结论 --")
print("暗物质数值靶落地：热遗迹 ⟨σv⟩=2.5e-26 cm³/s（匹配 Ωh²=0.12）；XENONnT 50 GeV 上限 2.6e-47 cm²；")
print("轴子窗口 f_a~1e12 GeV ↔ m_a~5.7 μeV、g_aγ~1.2e-15 GeV⁻¹ 处 ADMX 灵敏度边缘；均未探测（C 级）。")
