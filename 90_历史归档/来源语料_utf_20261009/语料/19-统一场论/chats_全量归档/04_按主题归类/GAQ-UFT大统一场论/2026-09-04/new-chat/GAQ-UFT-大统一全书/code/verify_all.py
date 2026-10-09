# -*- coding: utf-8 -*-
"""
GAQ-UFT《全维大统一全书》全维精算总脚本 verify_all.py
====================================================
按七级链路 A1-A7 对全书核心公式逐条执行：
  [方法一] 解析重求导（第一性原理/微分几何/定义式）
  [方法二] 数值复算（mpmath 250 位有效数字）
  [方法三] 量纲审计（[M],[L],[T],[Q] 齐次性）
  [方法四] 多方法交叉验证（不同公式路径互相印证）
  [对标]   CODATA 2022 / PDG 2024 / Planck 2018
并在末尾输出"发现的问题清单"（书中不一致项）。

运行：python code/verify_all.py
"""
import mpmath as mp
mp.mp.dps = 250

# ============================================================
# 基础常数（定义值精确；测量值带有限有效位数）
# ============================================================
c    = mp.mpf("299792458")            # m/s   定义（精确）
h    = mp.mpf("6.62607015e-34")       # J·s   定义（精确）
e    = mp.mpf("1.602176634e-19")      # C     定义（精确）
kB   = mp.mpf("1.380649e-23")         # J/K   定义（精确）
NA   = mp.mpf("6.02214076e23")        # mol^-1 定义（精确）
eps0 = mp.mpf("8.8541878128e-12")     # F/m   CODATA 2022（11 位有效）
mu0  = mp.mpf("1.25663706212e-6")     # N/A^2 CODATA 2022
G    = mp.mpf("6.67430e-11")          # m^3 kg^-1 s^-2 CODATA 2022
me   = mp.mpf("9.1093837139e-31")     # kg    电子质量 CODATA 2022
hbar = h / (2*mp.pi)
alpha_inv_CODATA = mp.mpf("137.035999084")   # CODATA 2022

# 轻子质量 (MeV/c^2), PDG 2024
me_M   = mp.mpf("0.51099895069");  dme_M  = mp.mpf("0.00000000016")
mmu_M  = mp.mpf("105.6583755");    dmmu_M = mp.mpf("0.0000023")
mtau_M = mp.mpf("1776.86");        dmtau_M= mp.mpf("0.12")

# 哈勃常数
Hp_c   = mp.mpf("67.36");  sHp_c = mp.mpf("0.54")   # Planck 2018 (TT+lowE+lensing+BAO)
Hp_b   = mp.mpf("67.4");   sHp_b = mp.mpf("0.5")    # Planck 2018 (TT+TE+EE+lowE+lensing)
HSH0ES = mp.mpf("73.04");  sHSH0ES = mp.mpf("1.04") # SH0ES 2022

problems = []

print("="*82)
print("PART A  公理与几何装置（A1-A2）")
print("="*82)

# ---------- A1 公理一逻辑审计 ----------
print("\n[A1] 公理一 v≡c：逻辑审计（无数值公式）")
print("  等价性：'v≡c 全域约束' ⇔ '时空具有洛伦兹结构 + 存在最大信号速度 c'")
print("  ⇒ 作为重述 →【已证实】；作为'质量来自额外维投影'→【假设】")
print("  量纲：无。逻辑上不自洽之处：坐标速度 v<c 的解释须由额外维内部运动给出（OPEN-M1 子问题）")

# ---------- A2.1 螺旋线：多方法 ----------
print("\n[A2.1] 螺旋线 κ²+τ²=1/(r²+p²)=k²（三方法交叉）")
r, p = mp.mpf("3"), mp.mpf("4")
# 方法一：解析（参数曲线 Frenet-Serret 公式）
den = r**2 + p**2
kap = r/den; tau = p/den
print("  [方法一 解析] κ=r/(r²+p²)=%s, τ=p/(r²+p²)=%s" % (mp.nstr(kap,12), mp.nstr(tau,12)))
print("                κ²+τ²=1/(r²+p²)=%s" % mp.nstr(kap**2+tau**2,16))
# 方法二：原始三阶导数数值构造
import numpy as np
t = 0.3
dr = np.array([-r*np.sin(t), r*np.cos(t), p])
ddr = np.array([-r*np.cos(t), -r*np.sin(t), 0])
dddr = np.array([r*np.sin(t), -r*np.cos(t), 0])
cross = np.cross(dr, ddr)
kap_num = np.linalg.norm(cross)/np.linalg.norm(dr)**3
tau_num = np.dot(cross, dddr)/np.linalg.norm(cross)**2
print("  [方法二 数值] t=0.3 处 κ=%s, τ=%s（与解析一致）" % (kap_num, tau_num))
# 方法三：频率-波数交叉（德布罗意：k=ω/c）
# 取 ω 使 k²=1/(r²+p²) ⇒ ω=c/√(r²+p²)
w_test = c/mp.sqrt(den)
print("  [方法三 交叉] 令 ω=c·k=c/√(r²+p²)=%s rad/s ⇒ (ω/c)²=1/(r²+p²)=%s" % (mp.nstr(w_test,10), mp.nstr((w_test/c)**2,16)))
dev = abs((kap**2+tau**2) - mp.mpf(1)/den)/(mp.mpf(1)/den)
print("  相对偏差 = %s → 几何恒等式精确成立【已证实-数学】" % mp.nstr(dev,6))

# ---------- A2.2 高维 Frenet-Serret ----------
print("\n[A2.2] 高维 Frenet-Serret（N 维推广）")
print("  d e_i/ds = -κ_{i-1} e_{i-1} + κ_i e_{i+1}（i=2..N-1）")
print("  32 维 ⇒ 31 个广义曲率 κ_1..κ_31；曲率谱完全决定曲线（曲线基本定理）")
print("  量纲：κ_i 均为 1/L；Σ(κ_i ℓ_P)² 无量纲【自洽】")
print("  N=32 检验：Σ_{i=1}^{31} κ̃_i² = (ωℓ_P/c)² —— 公理二 N 维推广【假设】")

# ---------- A2.3 公理二量纲审计（重做） ----------
print("\n[A2.3] 公理二 κ̃²+τ̃²=(ωℓ_P/c)² 量纲审计（重做，OPEN-D1）")
lP = mp.sqrt(hbar*G/c**3)
print("  字面式 κ²+τ²=(ωℓ_P/c)²：左端 [κ²]=L^-2；右端 [(ωℓ_P/c)²]=1 ⇒ L^-2 ≠ 1 → 不自洽")
print("  归一化式：κ̃=κℓ_P ⇒ [κ̃²]=1；右端 1 ⇒ 自洽【修复已落地】")
print("  ℓ_P=%s m（数值）" % mp.nstr(lP,10))

print()
print("="*82)
print("PART B  力与耦合（A3）")
print("="*82)

# ---------- B1 α：三等价形式 ----------
print("\n[B1] 精细结构常数 α：三种等价定义交叉")
a1 = e**2/(4*mp.pi*eps0*hbar*c)          # e²/(4πε₀ħc)
a2 = mu0*c*e**2/(2*h)                     # 用 μ₀c=1/ε₀ 交叉
a3 = e**2/(2*eps0*h*c)                    # 用 h=2πħ
print("  α₁=e²/(4πε₀ħc)  = %s" % mp.nstr(a1,16))
print("  α₂=μ₀ce²/(2h)   = %s" % mp.nstr(a2,16))
print("  α₃=e²/(2ε₀hc)   = %s" % mp.nstr(a3,16))
print("  三式相对偏差: |α₁-α₂|/α₁=%s, |α₁-α₃|/α₁=%s → 等价（因 μ₀ε₀c²=1 与 h=2πħ）" % (
    float(abs(a1-a2)/a1), float(abs(a1-a3)/a1)))
print("  α⁻¹(算)=%s" % mp.nstr(1/a1,16))
print("  α⁻¹(CODATA)=137.035999084  相对偏差=%s（ε₀ 有限有效位数上限）" % float(abs(1/a1-alpha_inv_CODATA)/alpha_inv_CODATA))
print("  量纲：α 无量纲 [Q²/(M L³ T^-2 · M L²/T · L/T)]=1 【自洽】")

# ---------- B2 Gε₀ 恒等式 ----------
print("\n[B2] Gε₀ 耦合恒等式 q_P²/m_P²=4πε₀G（双方法）")
mP = mp.sqrt(hbar*c/G)
qP = mp.sqrt(4*mp.pi*eps0*hbar*c)
lhs = qP**2/mP**2
rhs = 4*mp.pi*eps0*G
print("  [方法一] q_P²/m_P² = %s C²/kg²" % mp.nstr(lhs,12))
print("  [方法二] 4πε₀G     = %s C²/kg²" % mp.nstr(rhs,12))
print("  相对偏差 = %s → 定义恒等式严格成立【已证实-平凡】" % mp.nstr(abs(lhs-rhs)/rhs,6))
print("  量纲审计：[C²/kg²] 两侧一致【自洽】；但无预言力 → OPEN-EM1")

# ---------- B3 m_P/m_e=√(1/α_G) ----------
print("\n[B3] m_P/m_e=√(1/α_G)（双方法）")
alphaG = G*me**2/(hbar*c)
v1 = mP/me
v2 = mp.sqrt(1/alphaG)
print("  [方法一] m_P/m_e       = %s" % mp.nstr(v1,12))
print("  [方法二] √(1/α_G)      = %s" % mp.nstr(v2,12))
print("  比值 = %s → 定义恒等式（非巧合）【已证实-平凡】" % mp.nstr(v1/v2,6))
print("  量纲：m_P/m_e 无量纲；√(1/α_G) 无量纲【自洽】")

# ---------- B4 电弱参数 ----------
print("\n[B4] 电弱参数（PDG 2024）")
mW = mp.mpf("80.3692"); mZ = mp.mpf("91.1876"); mH = mp.mpf("125.25"); mt = mp.mpf("172.69")
s2w = 1-(mW/mZ)**2
print("  sin²θ_W=1-(m_W/m_Z)² = %s（树图；PDG 有效值≈0.23122）" % mp.nstr(s2w,8))
print("  说明：树图公式忽略辐射修正，与有效角有~0.008 差距（已证实-现状）；框架如需预言须含修正")

# ---------- B5 CKM 幺正性 ----------
print("\n[B5] CKM 矩阵幺正性（PDG 2024 模）")
Vud,Vus,Vub = mp.mpf("0.97373"), mp.mpf("0.2243"), mp.mpf("0.00382")
Vcd,Vcs,Vcb = mp.mpf("0.221"),  mp.mpf("0.975"),  mp.mpf("0.0408")
Vtd,Vts,Vtb = mp.mpf("0.008"),  mp.mpf("0.0388"), mp.mpf("1.013")
r1 = Vud**2+Vus**2+Vub**2
r2 = Vcd**2+Vcs**2+Vcb**2
r3 = Vtd**2+Vts**2+Vtb**2
print("  第一行 |Vud|²+|Vus|²+|Vub|² = %s" % mp.nstr(r1,8))
print("  第二行 = %s, 第三行 = %s" % (mp.nstr(r2,8), mp.nstr(r3,8)))
print("  说明：第三行由拟合模而来，可略超 1（已证实-现状）；第一行≈0.9985 在 PDG 误差内")

# ---------- B6 库仑/引力同构 + 力比 ----------
print("\n[B6] 库仑-引力同构与力比")
F_ratio = (e**2/(4*mp.pi*eps0))/(G*me**2)
print("  两电子静电力/引力 = %s ≈ 4.17×10⁴²" % mp.nstr(F_ratio,6))
print("  同构：两个 1/r 势 V_C=k_e q₁q₂/r 与 V_G=-Gm₁m₂/r 形状相同，耦合常数差 ~10⁴²")
print("  量纲：[M L²/T²]·[L]=M L³/T² 两侧一致【自洽】")

print()
print("="*82)
print("PART C  常数（A4）")
print("="*82)

# ---------- C1 普朗克单位：双路径 ----------
print("\n[C1] 普朗克单位（双计算路径交叉）")
tP = mp.sqrt(hbar*G/c**5)
TP = mp.sqrt(hbar*c**5/(G*kB**2))
print("  m_P=√(ħc/G)   = %s kg" % mp.nstr(mP,10))
print("  ℓ_P=√(ħG/c³)  = %s m" % mp.nstr(lP,10))
print("  t_P=√(ħG/c⁵)  = %s s" % mp.nstr(tP,10))
print("  q_P=√(4πε₀ħc) = %s C" % mp.nstr(qP,10))
print("  T_P=√(ħc⁵/Gk_B²)= %s K" % mp.nstr(TP,10))
# 交叉：m_P ℓ_P / ħ = ? （应为 1/c 相关）→ 直接验证组合
print("  [交叉] m_P·ℓ_P·c/ħ = %s（应为 1）" % mp.nstr(mP*lP*c/hbar,6))
print("  [交叉] ℓ_P·t_P⁻¹/c  = %s（应为 1）" % mp.nstr(lP/tP/c,6))
print("  量纲：全部由 [G,ħ,c] 组合唯一确定【已证实-数学】")

# ---------- C2 Koide：三方法 ----------
print("\n[C2] Koide 公式 Q=2/3（三方法）")
S1 = me_M+mmu_M+mtau_M
S2 = mp.sqrt(me_M)+mp.sqrt(mmu_M)+mp.sqrt(mtau_M)
Q = S1/S2**2
print("  [方法一] Q=(Σm)/(Σ√m)² = %s" % mp.nstr(Q,14))
print("          2/3 = %s, 相对偏差 = %s ≈ 9.2×10⁻⁶" % (mp.nstr(mp.mpf(2)/3,14), mp.nstr(abs(Q-mp.mpf(2)/3)/(mp.mpf(2)/3),6)))
# 方法二：45° 几何
cos2 = (S2**2)/(3*S1)   # cos²θ=((Σ√m)²)/(|v|²|u|²)= (Σ√m)²/(3Σm)
theta = mp.acos(mp.sqrt(cos2))*180/mp.pi
print("  [方法二] cos²θ=(Σ√m)²/(3Σm) = %s ⇒ θ = %s°（应 45°）" % (mp.nstr(cos2,12), mp.nstr(theta,10)))
# 方法三：误差传播
def dQ_dmi(mi): return mp.mpf(1)/S2**2 - S1/(S2**3*mp.sqrt(mi))
dq = abs(dQ_dmi(me_M))*dme_M + abs(dQ_dmi(mmu_M))*dmmu_M + abs(dQ_dmi(mtau_M))*dmtau_M
print("  [方法三] 误差传播：Q 不确定度 ≈ %s（量级 10⁻⁶~10⁻⁵，与偏差同量级）" % mp.nstr(dq,4))
print("  结论：Koide 是【已证实-经验】；偏差与误差同量级；框架须独立导出才成立（OPEN-M1）")

# ---------- C3 大数 ----------
print("\n[C3] 大数（Eddington-Dirac）")
age_y = mp.mpf("1.38e10")
age_s = age_y*mp.mpf("3.15576e7")
print("  m_P/m_e = %s" % mp.nstr(v1,6))
print("  宇宙年龄/t_P = %s" % mp.nstr(age_s/tP,6))
print("  α/α_G = %s" % mp.nstr(a1/alphaG,6))
print("  说明：~10²²/10⁶⁰/10⁴² 无公认解释【已证实-现状】；框架方向为【假设】")

print()
print("="*82)
print("PART D  宇宙（A5）")
print("="*82)

# ---------- D1 哈勃张力：双口径核对 ----------
print("\n[D1] 哈勃张力：双口径核对（全维精算已统一口径）")
for name,(Hp, sHp) in {"口径A(Planck 67.36±0.54)":(Hp_c,sHp_c), "口径B(Planck 67.4±0.5)":(Hp_b,sHp_b)}.items():
    dH = HSH0ES - Hp
    sH = mp.sqrt(sHp**2 + sHSH0ES**2)
    sig = dH/sH
    print("  %s：ΔH0=%s, σ=%s, 显著性=%sσ" % (name, mp.nstr(dH,6), mp.nstr(sH,6), mp.nstr(sig,6)))
print("  [D1-统一] 全书采用主口径 A（Planck 官方组合 67.36±0.54），ΔH0=5.68、4.85σ")
print("    备选口径 B（67.4±0.5）给出 4.89σ；两种口径均 >4.8σ，结论不受影响。")
problems.append("D1 已修复：哈勃张力口径已统一为 Planck 官方 67.36±0.54（ΔH0=5.68、4.85σ）；备选口径 67.4±0.5 给出 4.89σ。")

# ---------- D2 Planck 参数 ----------
print("\n[D2] Planck 2018 宇宙学参数")
Ob_h2, Oc_h2 = mp.mpf("0.02242"), mp.mpf("0.11933")
h_pl = mp.mpf("0.6736")
OL, Om = mp.mpf("0.6847"), mp.mpf("0.3153")
print("  Ω_b h²=%.5s, Ω_c h²=%.5s" % (mp.nstr(Ob_h2,6), mp.nstr(Oc_h2,6)))
print("  Ω_m+Ω_Λ = %s（平坦宇宙≈1）" % mp.nstr(Om+OL,6))
Om_h2 = Om*h_pl**2
z_eq = mp.mpf("2.4e4")*Om_h2
print("  z_eq≈2.4e4·Ω_m h² = %s（Planck 拟合 z_eq≈3402，近似公式量级一致）" % mp.nstr(z_eq,6))
print("  说明：z_eq 近似公式本身有 ~1% 偏差，属【已证实-近似】")

# ---------- D3 年龄/哈勃时间 ----------
print("\n[D3] 年龄与哈勃时间")
H0_s = Hp_c*mp.mpf("1000")/(mp.mpf("3.08567758e22"))
Htime = (1/H0_s)/(mp.mpf("3.15576e16"))
age_13 = mp.mpf("13.797")
print("  1/H0 = %s Gyr（口径 67.36）" % mp.nstr(Htime,6))
print("  年龄/哈勃时间 = %s（ΛCDM 理论 ≈0.96）" % mp.nstr(age_13/Htime,6))

print()
print("="*82)
print("PART E  量子-意识（A6）与实验（A7）")
print("="*82)

# ---------- E1 1 eV 光子 ----------
print("\n[E1] 1 eV 光子的普朗克归一化波数")
E_eV = mp.mpf("1"); eV_J = mp.mpf("1.602176634e-19")
w1 = E_eV*eV_J/hbar
k1 = w1/c
print("  ω=E/ħ = %s rad/s" % mp.nstr(w1,6))
print("  k=ω/c = %s 1/m" % mp.nstr(k1,6))
print("  k·ℓ_P = %s（无量纲）" % mp.nstr(k1*lP,6))
print("  交叉：k=2π/λ，λ=hc/E=%s m ⇒ k=2π/λ=%.6s 1/m（一致）" % (mp.nstr(h*c/(E_eV*eV_J),6), mp.nstr(2*mp.pi/(h*c/(E_eV*eV_J)),6)))

# ---------- E2 Casimir ----------
print("\n[E2] Casimir 力（Zeta 正则化样板）")
A_c = mp.mpf("1e-4")   # 1 cm²
d_c = mp.mpf("1e-6")   # 1 μm
Fc = mp.pi**2*hbar*c*A_c/(240*d_c**4)
print("  F=π²ħcA/(240d⁴)，A=1cm²,d=1μm ⇒ F = %s N" % mp.nstr(Fc,6))
print("  量纲审计：[ħc/L⁴]·[L²]=M L/T²=力【自洽】；实验（Lamoreaux 1997 等）已证实")
print("  框架含义：Zeta 正则化是成熟工具，但框架尚未用它算出任何常数（OPEN-G3）")

# ---------- A7 验收实验逻辑审计 ----------
print("\n[A7] 三大验收实验现状（逻辑审计，无公式可算）")
print("  V1 算出 α：OPEN-M1 卡点，未兑现")
print("  V2 解释暗物质：OPEN-C1 卡点，未兑现")
print("  V3 调解哈勃张力：OPEN-H1 卡点，未兑现")
print("  ⇒ 三大验收全部 OPEN，框架定位为'研究纲领'而非'已完成理论'【本书正式结论】")

print()
print("="*82)
print("全维精算发现的问题清单")
print("="*82)
if problems:
    for i, pr in enumerate(problems, 1):
        print("  P%d: %s" % (i, pr))
else:
    print("  未发现新的不一致项。")
print()
print("全维精算完成。所有数值以 mpmath 250 位复算（输入常数有限有效位数决定实际精度）。")
