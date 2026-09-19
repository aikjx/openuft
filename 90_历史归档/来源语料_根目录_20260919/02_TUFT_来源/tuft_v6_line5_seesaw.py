# -*- coding: utf-8 -*-
"""
TUFT v6 线一：Type-I seesaw 嵌入 + 汤川耦合跨度量级论证
MainAgent 独立数值复核
"""
import numpy as np

# ============================================================
# 0. 物理常数（CODATA / 粒子数据组 2024-2025）
# ============================================================
l_Pl   = 1.616255e-35      # m
M_Pl   = 1.22089e19        # GeV (reduced-ish; 1.22e19)
hbar_c = 197.3269804e-3    # GeV * fm  (=197.327 MeV*fm = 0.1973 GeV*fm)
hbar_c_SI = 1.054571817e-34 * 2.99792458e8  # J*m = eV*m / 1e9
# = 3.161527e-26 J*m = 1.97327e-7 eV*m
hbar_c_eV_m = 1.973269804e-7  # eV * m  (exact: hbar*c in eV*m)

v_EW   = 246.0             # GeV, SM Higgs vev
# 汤川耦合 (MSbar 或 Pole, 表中用质量/v 粗略)
m_e, m_mu, m_t = 0.511e-3, 0.10566, 173.0   # GeV
y_e  = m_e  / (v_EW/np.sqrt(2))
y_mu = m_mu / (v_EW/np.sqrt(2))
y_t  = m_t  / (v_EW/np.sqrt(2))
print("="*70)
print("0. 汤川耦合 (y = m/(v/sqrt2))")
print(f"   y_e  = {y_e:.3e}")
print(f"   y_mu = {y_mu:.3e}")
print(f"   y_t  = {y_t:.3e}")
print(f"   跨度 y_t/y_e = {y_t/y_e:.3e}  (= 3.4e5 量级)")
print(f"   跨度 y_t/y_mu = {y_t/y_mu:.3e}")

# ============================================================
# 1. seesaw 反推 M_N
# ============================================================
print("\n" + "="*70)
print("1. Type-I seesaw: m_nu = y_nu^2 v^2 / (2 M_R)")
print("   反推 M_R = y_nu^2 v^2 / (2 m_nu)")
print("-"*70)

for mnu in [0.05e-9, 0.0086e-9, 0.05e-9, 0.05e-9]:  # GeV: 0.05 eV, 8.6 meV
    pass

# 用两个有意义的 m_nu: atmospheric 0.05 eV, solar 0.0086 eV
for mnu_eV, label in [(0.05, "m_nu ~ 0.05 eV (atmospheric scale)"),
                      (0.0086, "m_nu ~ 8.6 meV (solar scale)")]:
    mnu = mnu_eV * 1e-9  # GeV
    print(f"\n   {label}:")
    for ynu in [0.01, 0.1, 0.4, 1.0, 2.0]:
        M_R = ynu**2 * v_EW**2 / (2*mnu)
        print(f"     y_nu = {ynu:5.2f}  ->  M_R = {M_R:.3e} GeV")

# ============================================================
# 2. TUFT R_perp 能量标度
# ============================================================
print("\n" + "="*70)
print("2. TUFT R_perp 能量标度")
print("-"*70)
R_perp_m = 59 * l_Pl
E_Rperp = hbar_c_eV_m / R_perp_m / 1e9  # GeV
print(f"   R_perp = 59 l_Pl = {R_perp_m:.3e} m")
print(f"   1/R_perp 对应能量 = hbar*c/R_perp = {E_Rperp:.3e} GeV")
print(f"   M_Pl / R_perp(Pl) = M_Pl/59 = {M_Pl/59:.3e} GeV")
print(f"   GUT 标度 ~ 2e16 GeV ; seesaw GUT-scale ~ 1e14 GeV")
print(f"   比值 E_Rperp / M_seesaw(1e14) = {E_Rperp/1e14:.2f}")
print(f"   比值 E_Rperp / M_GUT(2e16)   = {E_Rperp/2e16:.2f}")

# ============================================================
# 3. 汤川跨度量级论证：各种几何量组合
# ============================================================
print("\n" + "="*70)
print("3. 汤川 y 跨度 3.4e5 的几何量组合检验")
print("-"*70)

alpha = 1.0/137.036
L_n_over_mn = 0.54   # E115 / P12 口径

# 目标: y_t/y_e = 3.45e5, 即 y_e/y_t = 2.9e-6
target = y_e/y_t
print(f"   目标 y_e/y_t = {target:.3e}")

# (a) 幂律 Q^{-p}: 三代 Q=1,2,3
print("\n   (a) 幂律 y ~ Q^{-p}, Q=1(e),2(mu),3(t) 或反向")
for Q_light, Q_heavy in [(1,3),(3,1),(1,2),(2,1)]:
    # y_light/y_heavy = (Q_light/Q_heavy)^(-p) => p = -ln(ratio)/ln(Q_light/Q_heavy)
    p = -np.log(target)/np.log(Q_light/Q_heavy)
    print(f"     Q_light={Q_light}, Q_heavy={Q_heavy}: p = {p:.2f}")
print("     -> p≈11.6 (E131 已知否决 Q^{3/4})")

# (b) (Lambda_n/m_n)^k
print("\n   (b) 几何量 (Lambda_n/m_n)^k, ratio = 0.54")
k = np.log(target)/np.log(L_n_over_mn)
print(f"     需要 k = {k:.2f}  (非 O(1))")

# (c) exp(-C/alpha) 指数压低
print("\n   (c) 指数压低 y ~ exp(-C/alpha), alpha=1/137")
C_need = -np.log(target)*alpha
print(f"     需要 C = {C_need:.4f}  (即 C≈0.10, 非 O(1) 整数)")
# 若 C 是整数(如 C_k 纽结交叉数):
for Ck in [1,2,3,4,5]:
    print(f"     C_k={Ck:2d}: exp(-C_k/alpha) = {np.exp(-Ck/alpha):.2e}  (需 y_e/y_t=2.9e-6)")

# (d) exp(-C*alpha) 反号
print("\n   (d) 反向 y ~ exp(-C*alpha) (C*alpha 小)")
for C in [1,10,100,1000]:
    print(f"     C={C:5d}: exp(-C*alpha) = {np.exp(-C*alpha):.4f}")

# (e) Froggatt-Nielsen epsilon^n
print("\n   (e) FN 型 y ~ epsilon^n")
for eps in [0.05, 0.1, 0.2, 0.25]:
    n = np.log(target)/np.log(eps)
    print(f"     eps={eps}: n_e = {n:.2f} 代")

# (f) 组合: 几何量乘积 (kappa*tau*Q*C_k) 最多 ~10^2
print("\n   (f) 几何量乘积 (E135 已估 ~10^2 上限)")
print(f"     10^2 << 3.4e5  差 3400 倍, 闭合失败")

# ============================================================
# 4. M_N 由 TUFT 标度自然导出？
# ============================================================
print("\n" + "="*70)
print("4. TUFT 能否自然给出 M_N ~ 1e14 GeV?")
print("-"*70)
M_seesaw_target = 1e14  # GeV
# 方案 1: M_N = M_Pl * (Lambda_n/m_n)^k
print("\n   (i) M_N = M_Pl * (Lambda_n/m_n)^k")
k_Pl = np.log(M_seesaw_target/M_Pl)/np.log(L_n_over_mn)
print(f"     k = {k_Pl:.2f}  (非 O(1))")
# 方案 2: M_N = (M_Pl/59) * (Lambda_n/m_n)^k
M_Rperp = M_Pl/59.0
print(f"\n   (ii) M_N = (M_Pl/59) * (Lambda_n/m_n)^k, M_Rperp={M_Rperp:.2e} GeV")
k_R = np.log(M_seesaw_target/M_Rperp)/np.log(L_n_over_mn)
print(f"     k = {k_R:.2f}  (非 O(1))")
# 方案 3: M_N = M_Pl * exp(-C/alpha)
print(f"\n   (iii) M_N = M_Pl * exp(-C/alpha)")
C_s = -np.log(M_seesaw_target/M_Pl)*alpha
print(f"     C = {C_s:.4f}  (≈0.023, 非 O(1) 整数)")
# 方案 4: 若强行 M_N = M_Rperp = 2.07e17, 反推 y_nu
print(f"\n   (iv) 若强行 M_N = M_Rperp = {M_Rperp:.2e} GeV:")
for mnu_eV in [0.05, 0.0086]:
    mnu = mnu_eV*1e-9
    ynu = np.sqrt(2*mnu*M_Rperp)/v_EW
    print(f"     m_nu={mnu_eV} eV -> y_nu = {ynu:.2f}  {'(非微扰!)' if ynu>3.5 else '(微扰)'}")

# ============================================================
# 5. 振荡参数拓扑导出检验
# ============================================================
print("\n" + "="*70)
print("5. 振荡参数 (NuFIT 6.0 / JUNO 2025)")
print("-"*70)
dm2_21 = 7.49e-5    # eV^2
dm2_31 = 2.51e-3    # eV^2 (NO)
print(f"   Delta m^2_21 = {dm2_21:.3e} eV^2")
print(f"   |Delta m^2_31| = {dm2_31:.3e} eV^2")
print(f"   比值 dm2_31/dm2_21 = {dm2_31/dm2_21:.2f}")
# 若 m_nu ~ y_nu^2 v^2 /(2 M_R), 则 dm2 ~ y_nu^4 v^4 /(4 M_R^2)
# 比值 dm2_31/dm2_21 = (y_nu3/y_nu1)^4 (若 M_R 近似)
print(f"   若 M_R 简并, 比值 = (y_nu3/y_nu1)^4 -> y_nu3/y_nu1 = {(dm2_31/dm2_21)**0.25:.3f}")
print(f"   实验上 sin^2(theta_12)=0.309, theta_23~45 deg, 大混合")
print(f"   TUFT 拓扑量 (Q,C_k) 无自然大混合偏好 -> 开放")

# 质量本征值 (NO, hierarchical limit)
m1 = 0.0
m2 = np.sqrt(dm2_21)
m3 = np.sqrt(dm2_31)
print(f"\n   NO hierarchical: m1~0, m2={m2*1e3:.2f} meV, m3={m3*1e3:.2f} meV")
print(f"   sum m_nu ~ {(m1+m2+m3)*1e3:.2f} meV")

# ============================================================
# 6. 三方案拓扑对应
# ============================================================
print("\n" + "="*70)
print("6. N_R 三方案拓扑对应量纲核查")
print("-"*70)
# 方案 A: Q=0 真空纽结
print("   方案 A: N_R = Q=0 真空纽结")
print(f"     E24: m(Q=0) = m_Pl*mu0*0^{{3/4}}*e^0 = 0  -> 零质量, 无法给 M_N~1e14")
# 方案 B: 轴矢量挠率
print("   方案 B: N_R = 轴矢量挠率拓扑荷 (E72)")
print("     E71-73: 轴矢挠率=进动, 轨道力恒零; 是 spin-1 场分量, 不是 singlet Weyl 费米子")
# 方案 C: n 场重拓扑激发
print("   方案 C: N_R = n 场重拓扑激发 (Q 大, k_EM=k_c=0)")
print(f"     E24: m(Q) ~ m_Pl*mu0*Q^{{3/4}}*exp(-gamma Q)")
print(f"     Q 大 -> exp(-gamma Q) 主导 -> m 趋零; Q=1 -> m~m_Pl*mu0 (TeV 量级, D13)")
print(f"     无法自然给出 1e14 GeV; 需 mu0~1e-5 (微调)")

print("\n" + "="*70)
print("数值复核完成")
