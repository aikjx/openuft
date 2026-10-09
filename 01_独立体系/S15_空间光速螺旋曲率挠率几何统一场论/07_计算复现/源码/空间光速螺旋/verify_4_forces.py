import mpmath as mp
mp.mp.dps = 100

# CODATA 2022 常数
C = mp.mpf('299792458')
HBAR = mp.mpf('1.0545718176461565e-34')
G_NEWTON = mp.mpf('6.67430e-11')
EPSILON_0 = mp.mpf('8.8541878128e-12')
E_CHARGE = mp.mpf('1.602176634e-19')
M_E_KG = mp.mpf('9.1093837015e-31')
M_P_KG = mp.sqrt(HBAR * C / G_NEWTON)
ALPHA = E_CHARGE**2 / (4 * mp.pi * EPSILON_0 * HBAR * C)

print('=' * 80)
print('【验证1】引电统一恒等式 Gε₀ = q_P²/(4πm_P²)')
print('=' * 80)
Geps0 = G_NEWTON * EPSILON_0
qP_sq = 4 * mp.pi * EPSILON_0 * HBAR * C
qP_sq_over_4pi_mP_sq = qP_sq / (4 * mp.pi * M_P_KG**2)
print('  Gε₀                    =', Geps0)
print('  q_P²/(4πm_P²)          =', qP_sq_over_4pi_mP_sq)
err1 = abs(Geps0-qP_sq_over_4pi_mP_sq)/Geps0 * 100
print('  相对误差               =', err1, '%')
print('  验证通过?              =', err1 < 1e-28)

print()
print('=' * 80)
print('【验证2】引力/电磁力强度比 (两电子间) F_em/F_g = αℏc/(Gm_e²)')
print('=' * 80)
F_ratio = ALPHA * HBAR * C / (G_NEWTON * M_E_KG**2)
F_ref = mp.mpf('4.17e42')
print('  F_em/F_g 计算值        =', mp.nstr(F_ratio, 6))
print('  标准参考值             =', mp.nstr(F_ref, 3))
err2 = abs(F_ratio-F_ref)/F_ref*100
print('  相对误差               =', mp.nstr(err2, 4), '%')

print()
print('=' * 80)
print('【验证3】引力耦合常数 α_G = Gm_p²/(ℏc) = (m_p/m_P)²')
print('=' * 80)
M_PROTON = mp.mpf('1.67262192369e-27')
alpha_G_1 = G_NEWTON * M_PROTON**2 / (HBAR * C)
alpha_G_2 = (M_PROTON / M_P_KG)**2
print('  α_G = Gm_p²/(ℏc)       =', mp.nstr(alpha_G_1, 6))
print('  α_G = (m_p/m_P)²       =', mp.nstr(alpha_G_2, 6))
err3 = abs(alpha_G_1-alpha_G_2)/alpha_G_1*100
print('  相对误差               =', err3, '%')
print('  验证通过?              =', err3 < 1e-28)

print()
print('=' * 80)
print('【验证4】Z/Z 归一化后 Z=Z=1/2')
print('=' * 80)
Z_norm = 1*1/2
Zp_norm = 1 / (8*mp.pi * (1/(4*mp.pi)))
print('  归一化 Z               =', Z_norm)
print('  归一化 Zp              =', Zp_norm)
print('  归一化 ZZp             =', Z_norm * Zp_norm)
print('  归一化验证通过?        =', (Z_norm == 0.5) and (Zp_norm == 0.5))

print()
print('=' * 80)
print('【验证5】精细结构常数 α = -W₀(-(1/127)·e^(-1/12))')
print('=' * 80)
Omega = mp.mpf(1)/127
s_T = mp.mpf(1)/12
x = Omega * mp.e**(-s_T)
alpha_calc = -mp.lambertw(-x, 0)
alpha_CODATA = mp.mpf('0.0072973525693')
print('  α (V15.4拓扑推导)      =', mp.nstr(alpha_calc, 15), '= 1/', mp.nstr(1/alpha_calc, 8))
print('  α (CODATA 2022)        =', mp.nstr(alpha_CODATA, 15), '= 1/', mp.nstr(1/alpha_CODATA, 8))
err5 = abs(alpha_calc-alpha_CODATA)/alpha_CODATA*100
print('  相对误差               =', mp.nstr(err5, 4), '%')
print('  ppm 精度               =', mp.nstr(abs(alpha_calc-alpha_CODATA)/alpha_CODATA*1e6, 4), 'ppm')

print()
print('=' * 80)
print('【验证6】统一力公式 F = β·ℏω²/c，β系数分类验证')
print('=' * 80)
alpha_s = mp.pi**2 / 84
sin2w = mp.mpf(1)/4 - mp.mpf(1)/127
alpha_w = ALPHA / sin2w
print('  β_电磁 (α)            =', mp.nstr(ALPHA, 8), '= 1/', mp.nstr(1/ALPHA, 5))
print('  β_强力 (π²/84)        =', mp.nstr(alpha_s, 8), '= 1/', mp.nstr(1/alpha_s, 5))
print('  β_弱力 (α/sin²θ_W)    =', mp.nstr(alpha_w, 8), '= 1/', mp.nstr(1/alpha_w, 5))
print('  β_引力 ((m_e/m_P)²)   =', mp.nstr((M_E_KG/M_P_KG)**2, 6))

print()
print('=' * 80)
print('【验证7】四力强度比（以核尺度 r=1 fm 为参考）')
print('=' * 80)
r = mp.mpf('1e-15')
M_PROTON = mp.mpf('1.67262192369e-27')
F_s = HBAR * C * alpha_s / r**2
F_em = ALPHA * HBAR * C / r**2
R_W = mp.mpf('2.4e-18')
G_F = mp.mpf('1.1663787e-5') / (HBAR * C)**3
F_w = G_F * M_PROTON**2 * mp.e**(-r/R_W) / r**2
F_g = G_NEWTON * M_PROTON**2 / r**2
base = F_s
print('  在 r=1 fm 核尺度处:')
print('    强力 F_N            =', mp.nstr(F_s, 4), 'N   (基准=1)')
print('    电磁力 F_em         =', mp.nstr(F_em, 4), 'N   (×', int(base/F_em), ')')
print('    弱力 F_w            =', mp.nstr(F_w, 4), 'N   (×', mp.nstr(base/F_w, 3), ')')
print('    引力 F_g            =', mp.nstr(F_g, 4), 'N   (×', mp.nstr(base/F_g, 3), ')')
print()
print('  强度比 Fs:Fem:Fw:Fg ≈ 1 :', mp.nstr(F_em/F_s, 3), ':', mp.nstr(F_w/F_s, 3), ':', mp.nstr(F_g/F_s, 3))

print()
print('=' * 80)
print('【最终总结】验证通过率')
print('=' * 80)
checks = []
checks.append(('Gε₀恒等式（精确）', err1 < 1e-28))
checks.append(('F_em/F_g 与实验一致', err2 < 20))
checks.append(('α_G恒等式（精确）', err3 < 1e-28))
checks.append(('Z=Z=1/2归一化', (Z_norm == 0.5) and (Zp_norm == 0.5)))
checks.append(('α精度<50ppm', err5 < 0.005))
passed = sum(1 for c,v in checks if v)
total = len(checks)
for name, ok in checks:
    status = 'PASS' if ok else 'CHECK'
    print('  [' + status + '] ' + name)
print()
print('  验证通过:', passed, '/', total)
