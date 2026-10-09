# -*- coding: utf-8 -*-
"""
43_αG口径混淆修复_解开
算法联盟 ROOT 最高权限 · 解开 26/40号 α_G 数值混淆并给出修复值
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from mpmath import mp, mpf
mp.dps = 80

# 常数
HBAR = mpf('1.054571817e-34')
C    = mpf('299792458')
G    = mpf('6.67430e-11')
ME   = mpf('9.1093837015e-31')
MP   = (HBAR*C/G)**0.5          # 普朗克质量 (sqrt(hbar c / G))
ALPHA= mpf(1)/mpf('137.035999084')
KE   = mpf('1')/(4*mpf('3.141592653589793')*mpf('8.8541878128e-12'))  # 1/4pi eps0
E_CHG= mpf('1.602176634e-19')

def line(s): print(s)

line("="*70)
line("解开 α_G 数值混淆 · 全维分析修复")
line("="*70)

# 1) 几何定义 α_G = (m_e/m_P)^2
alpha_G_geo = (ME/MP)**2
line(f"\n[真值1] 几何定义 α_G = (m_e/m_P)² = {alpha_G_geo}")
line(f"          m_P = sqrt(hbar c / G) = {MP}")

# 2) 标准物理 电子-电子 库仑力/引力 比
ratio_eg = (KE*E_CHG**2)/(G*ME**2)
line(f"\n[真值2] 电子-电子 库仑/引力 = ke²/(G m_e²) = {ratio_eg}")
line(f"          = 1/α_G 与 (e²/4πε₀)/(ℏc) 的组合 = 4π/α · (m_P/m_e)² 量级一致")

# 3) 26/40号写的 3.85e-15 到底是什么？
line(f"\n[解开] 26/40号写 'α_G≈3.85e-15' 的来源追查:")
val_rep = mpf('3.85e-15')
# 假设它 = 1/(Fs/Fg)，Fs/Fg=2.6e14 (26号)
FsFg_rep = mpf('2.6e14')
line(f"   若 α_G_rep = 1/(Fs/Fg)_report = 1/{FsFg_rep} = {1/FsFg_rep}")
line(f"   => 3.85e-15 实为 '报告内 强/引力 比的倒数'，非 (m_e/m_P)²")
line(f"   且 '双电子' 标签错误：电子不参与强相互作用，与强子比无意义")
# 与几何真值比
line(f"\n   量级错位：α_G_geo / α_G_rep = {alpha_G_geo/val_rep}")
line(f"   = (m_e/m_P)² / (1/(Fs/Fg)) ，二者相差 ~30 个数量级，确非同量")

# 4) 正确修复值：用几何 α_G=(m_e/m_P)²，并给出 Fe/Fg 真值
FeFg_geo = ALPHA/alpha_G_geo
FsFg_geo = mpf(1)/alpha_G_geo   # α_S≈1
line(f"\n[修复值] 用 α_G_geo 重算层级:")
line(f"   Fe/Fg (几何真值) = α_E/α_G = {FeFg_geo}")
line(f"   Fs/Fg (几何真值, α_S≈1) = 1/α_G = {FsFg_geo}")
line(f"   与标准物理 e-e 库仑/引力 {ratio_eg} 同量级 ✅")

# 5) 双口径对照表
line(f"\n[双口径对照]")
line(f"   口径A(几何权威): α_G=(m_e/m_P)²={alpha_G_geo}, Fe/Fg={FeFg_geo}")
line(f"   口径B(26号旧):   α_G≈3.85e-15 (=1/FsFg), Fe/Fg≈1.9e12")
line(f"   => 26号旧 α_G 标签'双电子'为误称；应改为口径A并注明口径B仅作内部比参照")

line(f"\n[结论] α_G 数值混淆已解开：3.85e-15 是报告内部强/引力比倒数(误标'双电子')，")
line(f"       与几何定义 (m_e/m_P)²=1.75e-45 相差30量级。修复采用几何权威值。")
