# -*- coding: utf-8 -*-
"""
第74章 弱相互作用的本源（SU(2)_L x U(1)_Y 电弱统一·手征 V-A·Higgs 质量生成）——精算复现脚本
纯标准库。常数取 PDG/CODATA。用法: python weak_source_ladder.py
"""
import math

hcbar=0.1973269804     # GeV·fm
hbars=6.582119569e-25  # GeV·s
alpha=1/137.035999084
e=math.sqrt(4*math.pi*alpha)

def L(k,v): print(f"{k:48s} = {v}")

print("==== 1. 电弱规范群与媒介玻色子（[A]）====")
mW=80.377; mZ=91.1876   # GeV
L("规范群", "SU(2)_L x U(1)_Y，4 个生成元 -> W1,W2,W3,B")
L("带电弱玻色子 W± 质量 (GeV)", f"{mW:.3f}")
L("中性弱玻色子 Z 质量 (GeV)", f"{mZ:.3f}")
L("光子", "A = B cosθW + W3 sinθW，破缺后仍严格无质量 -> 电磁仍长程")

print("\n==== 2. 弱混合角（树级 on-shell）====")
s2=1-(mW/mZ)**2
L("sin^2 θW = 1 - mW^2/mZ^2 (on-shell)", f"{s2:.4f}  (~0.223；MSbar~0.231)")
L("sin θW, cos θW", f"{math.sqrt(s2):.4f}, {math.sqrt(1-s2):.4f}")
L("mW = mZ cosθW 检验", f"{mZ*math.sqrt(1-s2):.3f} vs {mW:.3f}")

print("\n==== 3. Higgs 真空期望值 v（由费米常数）====")
GF=1.1663787e-5  # GeV^-2
v=1/math.sqrt(math.sqrt(2)*GF)
L("G_F (GeV^-2)", f"{GF:.4e}")
L("v = (√2 G_F)^(-1/2) (GeV)", f"{v:.3f}  (~246)")
g=2*mW/v
L("SU(2) 耦合 g = 2 mW/v", f"{g:.4f}")
gp=g*math.sqrt(s2)/math.sqrt(1-s2)
L("U(1)_Y 耦合 g'", f"{gp:.4f}")
L("树级 e = g sinθW", f"{g*math.sqrt(s2):.5f}  vs 实测 √4πα={e:.5f}（差~1.8%=辐射修正 [A]）")
L("mZ = √(g²+g'²) v/2 检验 (GeV)", f"{math.sqrt(g*g+gp*gp)*v/2:.3f} vs {mZ:.3f}")

print("\n==== 4. 极短力程（重玻色子）====")
rW=hcbar/mW; rZ=hcbar/mZ
L("W 力程 ħc/mW (fm)", f"{rW:.5f}  = {rW*1e-15:.3e} m (~1/400 质子直径)")
L("Z 力程 ħc/mZ (fm)", f"{rZ:.5f}")
L("对比：π核力程 1.4 fm / 电磁 ∞", "弱力比核力还短 ~600 倍 -> 低能极弱")

print("\n==== 5. μ 衰变与费米常数（[A]，弱作用的标定）====")
mmu=0.1056583745  # GeV
# Γ(mu -> e ν ν) = G_F^2 m_mu^5 /(192 π^3)（树级，忽略极小辐射修正）
Gamma=GF**2*mmu**5/(192*math.pi**3)   # GeV
tau=hbars/Gamma
L("m_mu (GeV)", mmu)
L("Γ = G_F² mμ⁵/(192π³) (GeV)", f"{Gamma:.3e}")
L("τμ = ħ/Γ (s)", f"{tau:.3e}  (实测 2.197e-6)")
L("相对偏差", f"{(tau-2.1969811e-6)/2.1969811e-6:.2e}（树级，未含~辐射修正）")

print("\n==== 6. 为什么低能下弱力这么弱：重媒介压低 (E/mW)² ====")
for E in (0.000511, 0.1057, 91.188):
    supp=(E/mW)**2
    tag="电子能标" if E<0.001 else ("μ能标" if E<1 else "Z 能标(共振)")
    L(f"相对压低 (E/mW)² @ E={E:>8.5f} GeV [{tag}]", f"{supp:.2e}")
L("结论", "低能弱作用被 mW 巨大质量压成 ~10^-13；并非裸耦合小（g≈0.65 > e≈0.30）")

print("\n==== 7. 手征：弱作用只看左手（V−A）====")
L("左手投影 P_L=(1-γ5)/2", "W 只耦合 P_L ψ；右手反中微子不参与带电流")
L("中微子", "仅左手（粒子）/右手（反粒子）被观测 -> 最大宇称破坏（吴健雄 1956 [A]）")

print("\n==== 8. Higgs 给基本费米子质量：Yukawa 耦合等级 ====")
mH=125.10
L("Higgs 玻色子质量 (GeV)", mH)
for name,mf in [("电子",0.000510999),("μ",0.105658),("顶夸克",172.76)]:
    y=math.sqrt(2)*mf/v
    L(f"y_{name} = √2 m_{name}/v", f"{y:.4e}")
L("关键", "m_f = y_f v/√2：基本粒子质量来自 Yukawa 耦合×vev；但 y_f 本身仍是输入（味等级问题 OPEN）")
L("普通物质质量占比", "Higgs→流夸克仅 0.74%；99.26% 仍来自 QCD（见第73章）")

print("\n精算完成。")
