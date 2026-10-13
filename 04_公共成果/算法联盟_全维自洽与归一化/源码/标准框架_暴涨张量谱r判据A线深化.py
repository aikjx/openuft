# -*- coding: utf-8 -*-
"""十七期·标准框架攻坚 线A深化 暴涨张量谱 r 与 B 模式偏振数值靶（2026-10-14）
r ↔ 张量功率谱 ↔ 通胀能标 H_inf ↔ GUT 能标交叉判据；B 模式探测门槛。
公式与常数均为标准公开值（Planck 2018 / BK18 / CMB-S4 Science Book）。mpmath 250 位。
"""
import mpmath as mp
mp.mp.dps = 250

# ---- 标准常数与观测锚点（A 级公开）----
As = mp.mpf("2.1e-9")          # Planck 2018 标量功率谱振幅（k*=0.05/Mpc）
M_Pl_GeV = mp.mpf("2.435e18")  # 约化 Planck 质量 (ħc/G)^(1/2) = 2.435e18 GeV
pi = mp.pi
r_BK18 = mp.mpf("0.036")       # BICEP/Keck Array XVIII：r<0.036 @95%（A 级）
r_CMBS4 = mp.mpf("0.001")      # CMB-S4 目标 σ(r)（A 级，Science Book）
M_GUT = mp.mpf("2.3792e16")    # 十二期 MSSM 交汇靶（GeV）

print("===== 线A深化 暴涨张量谱 r 数值靶（250 位）=====")

# ① 张量-标量比与张量功率谱
print("\n① r ↔ 张量功率谱（Δ²_t = r·A_s，k*=0.05/Mpc，A_s=2.1e-9）")
print("  r=0.036（BK18 上限）: Δ²_t = %.6e" % (r_BK18*As))
print("  r=0.001（CMB-S4 目标）: Δ²_t = %.6e" % (r_CMBS4*As))

# ② 通胀能标 H_inf（单场慢滚：H_inf = π·M_Pl·sqrt(r·A_s/2)）
def Hinf(r):
    return pi * M_Pl_GeV * mp.sqrt(r * As / 2)
print("\n② 通胀哈勃能标 H_inf（单场慢滚）")
rows = []
for r in (mp.mpf("0.1"), mp.mpf("0.036"), mp.mpf("0.01"), mp.mpf("0.003"), mp.mpf("0.001")):
    H = Hinf(r)
    rows.append((r, H))
    print("  r=%.3f → H_inf = %.6e GeV（= %.3e M_GUT）" % (r, H, H/M_GUT))

# ③ 慢滚一致性：张量谱指数 n_t = -r/8
print("\n③ 慢滚一致性 n_t = −r/8")
print("  r=0.036: n_t = %.6f | r=0.001: n_t = %.6f" % (-r_BK18/8, -r_CMBS4/8))

# ④ B 模式探测门槛与前景
print("\n④ B 模式探测门槛")
print("  BK18 现状（2021，A 级）: r < 0.036 @95% CL（BICEP/Keck Array XVIII）")
print("  透镜 B 模式等效噪声: σ(r)_lens ≈ 0.01-0.02（需 delensing 才能达 0.001）")
print("  CMB-S4 目标: σ(r) ≈ 0.001（Science Book）；LiteBIRD 目标 r < 0.001-0.002")
print("  判决条件: 若 CMB-S4 探测 r ≥ 3σ（即 r ≥ 0.003）→ 首次直接观测量子引力/高能标窗口")

# ⑤ 与 GUT 能标交叉判据（统一场论核心连接）
print("\n⑤ GUT 交叉判据（H_inf vs M_GUT=%.4e GeV）" % M_GUT)
print("  r=0.036 → H_inf=%.3e GeV，比 M_GUT 低 %.1f 个数量级" % (Hinf(r_BK18), mp.log10(M_GUT/Hinf(r_BK18))))
print("  r=0.001 → H_inf=%.3e GeV，比 M_GUT 低 %.1f 个数量级" % (Hinf(r_CMBS4), mp.log10(M_GUT/Hinf(r_CMBS4))))
print("  解读：r 探测触及 1e13-1e14 GeV 能标（量子引力预物理窗口），但低于 GUT 3-4 个数量级；")
print("  若未来 r 高值（>0.01）被证实，通胀发生在接近统一能标处——两线交叉验证的统一场靶")

print("\n-- 结论 --")
print("线A深化数值靶落地（250 位可复现）：r 门槛（BK18<0.036 → CMB-S4 0.001）、通胀能标谱（7.8e12-7.8e13 GeV）、")
print("n_t 一致性、B 模式门槛、GUT 交叉比（低 3-4 量级）。诚实：r 尚未探测（上限 0.036），统一未完成。")
