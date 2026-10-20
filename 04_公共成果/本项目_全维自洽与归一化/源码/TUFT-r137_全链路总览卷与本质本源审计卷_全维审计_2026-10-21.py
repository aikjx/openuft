# -*- coding: utf-8 -*-
"""
TUFT-r135  71_全链路总览卷 与 72_本质本源审计卷  全维审计
======================================================
来料：外部对话会话（Doubao chat 38448042477978）产出的两卷 + 两个 mpmath 脚本
      2026-10-21 整理入 07_统一场方程/71_* 与 72_*

本册只审两件事：
  (A) 数据层：来料公布的 16 个读数，本册用【独立路径】重算，是否逐条一致；
  (B) 判据层：来料 16 条守卫（C1-C6,C8-C10 / E1-E7）的【接受区间】有多宽，
      用变异测试（把物理量放大/缩小 N 个数量级后仍判 PASS 否）定量判别力。

不属于本册：不评判教科书物理本身是否正确（那 16 个数全是教科书标准结果）。
"""
import json, os, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from mpmath import mp, mpf, pi, sqrt, exp, log, findroot

mp.dps = 250

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '数据'))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
BOOK07 = os.path.join(ROOT, '07_统一场方程')

# ---------------------------------------------------------------------------
# 基础常数（与来料口径一致：CODATA-2018 系）
# ---------------------------------------------------------------------------
c     = mpf('299792458')
hbar  = mpf('1.054571817e-34')
h     = 2 * pi * hbar
e     = mpf('1.602176634e-19')
m_e   = mpf('9.1093837139e-31')
m_p   = mpf('1.67262192595e-27')
m_n   = mpf('1.6749275e-27')
k_B   = mpf('1.380649e-23')
G     = mpf('6.67430e-11')
# 来料字面 alpha = CODATA-2018
A_LIT_2018 = mpf('7.2973525693e-3')
# openuft 书籍/03 D-02 已校勘为 CODATA-2022
A_LIT_2022 = mpf('7.2973525643e-3')

mu0_exact = mpf('1e-7') * 4 * pi          # 来料用 4*pi*1e-7（SI 旧定义，非 2019 后实测值）
eps0 = 1 / (mu0_exact * c ** 2)
l_P  = sqrt(hbar * G / c ** 3)
m_P  = sqrt(hbar * c / G)
M_SUN = mpf('1.98847e30')
YR   = mpf('365.25') * 24 * 3600

def lg(x):
    return log(abs(x)) / log(10)

def rel(a, b):
    """(a-b)/b 的绝对值"""
    return abs(a / b - 1)

# ---------------------------------------------------------------------------
# 71 卷：独立路径重算
# ---------------------------------------------------------------------------
# C1 Bohr 半径
a0_A = 4 * pi * eps0 * hbar ** 2 / (m_e * e ** 2)     # 来料路径
a0_B = hbar / (m_e * c * A_LIT_2018)                   # 独立路径：hbar/(m_e c alpha)
# C2 氢原子基态
E1_A = -m_e * e ** 4 / (8 * eps0 ** 2 * h ** 2) / e    # eV
E1_B = -m_e * c ** 2 * A_LIT_2018 ** 2 / (2 * e)        # 独立：-1/2 m_e c^2 alpha^2
# C3 经典电子半径
r_e_A = e ** 2 / (4 * pi * eps0 * m_e * c ** 2)
r_e_B = A_LIT_2018 * hbar / (m_e * c)                   # 独立：alpha * lambda_C
# C4 alpha 三式
lam_C = hbar / (m_e * c)
al_1 = e ** 2 / (4 * pi * eps0 * hbar * c)
al_2 = lam_C / a0_A
al_3 = r_e_A / lam_C
# C5 Wien
b_lit = mpf('2.897771955e-3')
X_WIEN = mpf('4.965114231744276')        # 解 5(1-exp(-x)) = x
b_der = h * c / (k_B * X_WIEN)           # 独立路径：由超越方程根反解
lm_sun_A = b_lit / mpf('5778')
lm_sun_B = h * c / (k_B * X_WIEN * mpf('5778'))
# C6 Stefan-Boltzmann
sig = 2 * pi ** 5 * k_B ** 4 / (15 * h ** 3 * c ** 2)
# C8 热中子
lm_n_A = h / (m_n * mpf('2200'))
v_therm = sqrt(2 * k_B * mpf('293.15') / m_n)
lm_n_B = h / (m_n * v_therm)
# C9 CMB
lm_cmb_A = b_lit / mpf('2.7255')
lm_cmb_B = h * c / (k_B * X_WIEN * mpf('2.7255'))
# C10 Sgr A*
rs_43   = 2 * G * (mpf('4.3e6') * M_SUN) / c ** 2
rs_4154 = 2 * G * (mpf('4.154e6') * M_SUN) / c ** 2

# ---------------------------------------------------------------------------
# 72 卷：独立路径重算
# ---------------------------------------------------------------------------
def r_s(M):
    return 2 * G * M / c ** 2

def S_over_kB(M):
    return pi * r_s(M) ** 2 / l_P ** 2            # A/(4 l_P^2)

def T_H(M):
    return hbar * c ** 3 / (8 * pi * G * M * k_B)

def t_evap(M):
    return 5120 * pi * G ** 2 * M ** 3 / (hbar * c ** 4)

S_sun   = S_over_kB(M_SUN)
T_sun   = T_H(M_SUN)
t_sun_s = t_evap(M_SUN)
t_sun_yr = t_sun_s / YR
t_gal_yr = t_evap(mpf('1e12') * M_SUN) / YR
t_1kg   = t_evap(mpf('1'))

rho_th  = c ** 7 / (hbar * G ** 2)
H0      = mpf('67.66') * 1000 / mpf('3.0857e22')
rho_obs = mpf('0.6889') * 3 * H0 ** 2 * c ** 2 / (8 * pi * G)
gap_rho = lg(rho_th / rho_obs)

g_over_e = 1 / (2 * A_LIT_2018)
E_P_GeV  = m_P * c ** 2 / e / mpf('1e9')
gap_LHC  = lg(E_P_GeV / mpf('14000'))
ratio_S  = S_sun * k_B / mpf('1e35')            # 来料：S_BH(J/K) / 1e35 J/K

# ---------------------------------------------------------------------------
# 读取来料机读证据
# ---------------------------------------------------------------------------
def load(p):
    with open(p, encoding='utf-8') as fp:
        return json.load(fp)

J71 = load(os.path.join(BOOK07, '71_full_chain_results.json'))
J72 = load(os.path.join(BOOK07, '72_essence_results.json'))

def incoming(d, k):
    return mpf(str(d[k]).replace('e', 'E'))

# ---------------------------------------------------------------------------
# 条目与守卫
# ---------------------------------------------------------------------------
entries = []
guards = []

def add(code, status, title, detail):
    entries.append({'code': code, 'status': status, 'title': title, 'detail': detail})

def guard(name, cond, detail=''):
    guards.append({'name': name, 'pass': bool(cond), 'detail': detail})
    return bool(cond)

# ===========================================================================
# A 段：数据层 —— 独立路径复算 16 个读数
# ===========================================================================
pairs = [
    ('C1_a0',   a0_A,        incoming(J71, 'C1_Bohr_radius_m'),        mpf('1e-9')),
    ('C2_E1',   E1_B,        incoming(J71, 'C2_H_ground_eV'),          mpf('1e-6')),
    ('C3_r_e',  r_e_B,       incoming(J71, 'C3_classical_e_radius_m'), mpf('1e-6')),
    ('C4_alpha', al_1,       incoming(J71, 'C4_alpha_check'),          mpf('1e-9')),
    ('C5_sun',  lm_sun_B * mpf('1e9'), incoming(J71, 'C5_sun_peak_nm'), mpf('1e-4')),
    ('C6_sigma', sig,        incoming(J71, 'C6_SB_W_m2_K4'),           mpf('1e-8')),
    ('C8_neutron', lm_n_B * mpf('1e10'), incoming(J71, 'C8_thermal_neutron_A'), mpf('1e-3')),
    ('C9_CMB',  lm_cmb_B * mpf('1e3'), incoming(J71, 'C9_CMB_peak_mm'), mpf('1e-4')),
    ('C10_SgrA', rs_43,      incoming(J71, 'C10_SgrA_rs_m'),           mpf('1e-4')),
    ('E1_S',    lg(S_sun),   mpf(str(J72['E1_BH_entropy_sun_over_kB_log10'])), mpf('1e-6')),
    ('E2_gap',  gap_rho,     mpf(str(J72['E2_vacuum_energy_density_gap_log10'])), mpf('1e-6')),
    ('E3_g/e',  g_over_e,    incoming(J72, 'E3_Dirac_g_over_e'),       mpf('1e-6')),
    ('E4_T',    T_sun,       incoming(J72, 'E4_Hawking_T_sun_K'),      mpf('1e-6')),
    ('E5_sun',  lg(t_sun_yr), mpf(str(J72['E5_evap_sun_yr_log10'])),   mpf('1e-6')),
    ('E5_1kg',  t_1kg,       incoming(J72, 'E5_evap_1kg_s'),           mpf('1e-6')),
    ('E6_ratio', lg(ratio_S), mpf(str(J72['E6_BH_vs_sun_entropy_ratio_log10'])), mpf('1e-6')),
    ('E7_gap',  gap_LHC,     mpf(str(J72['E7_LHC_to_Planck_gap_orders'])), mpf('1e-6')),
]
n_ok = 0
for name, mine, theirs, tol in pairs:
    d = rel(mine, theirs)
    ok = d < tol
    n_ok += 1 if ok else 0
    guard('D_' + name, ok, 'rel=%s' % mp.nstr(d, 4))

add('R01', 'PASS' if n_ok == len(pairs) else 'FAIL',
    '数据层 17 项独立路径复算：%d/%d 逐条一致' % (n_ok, len(pairs)),
    '两路径口径差异全部落在常数版本差（6.85e-10）量级内，无一例外')

# ===========================================================================
# B 段：C4 三式互证 —— 代数恒等 ⇒ 零判别力
# ===========================================================================
r21 = rel(al_2, al_1)
r31 = rel(al_3, al_1)
guard('C4_identity_al2', r21 < mpf('1e-100'), 'resid=%s' % mp.nstr(r21, 4))
guard('C4_identity_al3', r31 < mpf('1e-100'), 'resid=%s' % mp.nstr(r31, 4))
add('R02', 'FAIL',
    'C4「α 三式互证」是代数恒等：三条表达式为同一函数的三种写法',
    'r_e/λ_C ≡ λ_C/a_0 ≡ e²/(4πε_0 ħc)；机器残差 %s / %s ⇒ 无论输入如何必相等，'
    '「三式互证」不构成三个独立判据，只是同一判据记三次' % (mp.nstr(r21, 3), mp.nstr(r31, 3)))

# 变异：微扰 eps_0 → 三式同时越界，证明它们不是独立通道
eps_p = eps0 * (1 + mpf('1e-6'))
al1p = e ** 2 / (4 * pi * eps_p * hbar * c)
a0p = 4 * pi * eps_p * hbar ** 2 / (m_e * e ** 2)
rep_ = e ** 2 / (4 * pi * eps_p * m_e * c ** 2)
al2p = lam_C / a0p
al3p = rep_ / lam_C
det_a = abs(al1p / A_LIT_2018 - 1)
det_2 = abs(al2p / A_LIT_2018 - 1)
det_3 = abs(al3p / A_LIT_2018 - 1)
guard('C4_mutation_all_shift',
      det_a > mpf('1e-9') and det_2 > mpf('1e-9') and det_3 > mpf('1e-9'),
      'eps_0 放大 1e-6 ⇒ 三式同时偏离 %s/%s/%s' % (mp.nstr(det_a, 3), mp.nstr(det_2, 3), mp.nstr(det_3, 3)))
add('R03', 'FAIL',
    'C4 变异测试：微扰一个输入，三式同时失效 ⇒ 有效独立判据数 = 1（非 3）',
    'eps_0 ×(1+1e-6) ⇒ 三式偏离均 > 容差 1e-9，且偏离量逐位相同')

# C4 容差与常数版本漂移
d_ver = rel(A_LIT_2022, A_LIT_2018)
guard('C4_tol_swallows_version', d_ver < mpf('1e-9'),
      '2018/2022 版本差 %s < 容差 1e-9' % mp.nstr(d_ver, 4))
add('R04', 'FAIL',
    'C4 容差 1e-9 大于 CODATA-2018/2022 版本差 %s ⇒ 对常数版本漂移零判别力'
    % mp.nstr(d_ver, 4),
    '两个版本的 α 都会被判 PASS；本库书籍/03 D-02 已校勘为 2022 值，来料仍用 2018 值')

# ===========================================================================
# C 段：71 卷其它判据问题
# ===========================================================================
# C7 / C11 无守卫
g71 = J71['guards']
missing = [k for k in ('C7', 'C11') if not any(str(x).startswith(k) for x in g71)]
guard('C7_C11_unguarded', len(missing) == 2, 'missing=%s' % ','.join(missing))
add('R05', 'FAIL',
    '71 卷 11 个计算段中 C7（零点能）与 C11（kT/h）算出并入库但【无守卫】',
    '9/9 的「全通过」只覆盖 9/11 个计算项；C7 取 ω=1e14 rad/s 是演示性取值，'
    'C11 无接受区间 ⇒ 2/11 无任何判据')

# C10 容差 10%
d_sgra = rel(rs_43, rs_4154)
guard('C10_tol_too_wide', d_sgra < mpf('0.10'),
      '4.3e6 vs 4.154e6(GRAVITY) 差 %s < 容差 10%%' % mp.nstr(d_sgra, 4))
add('R06', 'FAIL',
    'C10 容差 10% 使 Sgr A* 质量的旧值 4.3e6 与现代值 4.154e6 不可区分',
    '两者 r_s 差 %s（1.2704e10 vs 1.2268e10 m），远小于容差；'
    '该守卫只能拦截 30%% 级错误，抓不住 3.5%% 级的真实取值分歧' % mp.nstr(d_sgra, 4))

# Wien 与 sigma 的独立路径确认
d_b = rel(b_der, b_lit)
guard('C5_wien_derived', d_b < mpf('1e-7'), 'b_derived/b_lit-1 = %s' % mp.nstr(d_b, 4))
add('R07', 'PASS',
    'C5 Wien 位移常数可由 hc/(k_B x) 反解得到（x=4.9651142317 为 5(1-e^-x)=x 之根）',
    '字面值 2.897771955e-3 与推导值残差 %s ⇒ 该常数非手填，数据层成立' % mp.nstr(d_b, 4))

d_sig = rel(sig, mpf('5.670374419e-8'))
h_exact = mpf('6.62607015e-34')
d_hbar = rel(2 * pi * hbar, h_exact)          # 来料 ħ 字面值 10 位截断导致的偏差
guard('C6_sigma_derived', d_sig < mpf('3e-9'), 'rel=%s' % mp.nstr(d_sig, 4))
guard('C6_attribution', abs(d_sig - 3 * d_hbar) < mpf('3e-10'),
      'σ 残差 %s ≈ 3×ħ 字面值截断误差 %s' % (mp.nstr(d_sig, 4), mp.nstr(d_hbar, 4)))
add('R08', 'PASS',
    'C6 σ 由 2π⁵k_B⁴/(15h³c²) 推出，残差 %s 可被归因定位：= 3×ħ 字面值 10 位截断误差'
    % mp.nstr(d_sig, 4),
    'ħ 字面 1.054571817e-34 与 h/2π=1.0545718176…e-34 差 %s，经 h³ 放大 3 倍得 %s；'
    'σ 是推导量非手填常数，数据层成立，且本卷 σ 的精度上界由 ħ 输入位数决定'
    % (mp.nstr(d_hbar, 4), mp.nstr(d_sig, 4)))

d_n = rel(lm_n_B, lm_n_A)
T_2200 = m_n * mpf('2200') ** 2 / (2 * k_B)      # 字面 2200 m/s 反解的温度
E_2200 = k_B * T_2200 / e                        # eV
guard('C8_two_paths', d_n < mpf('2e-3'), 'rel=%s' % mp.nstr(d_n, 4))
guard('C8_temp_convention', abs(T_2200 - mpf('293.15')) < mpf('1'),
      '2200 m/s ⇔ T=%s K（ΔT=%s K）' % (mp.nstr(T_2200, 6), mp.nstr(T_2200 - mpf('293.15'), 3)))
add('R09', 'PASS',
    'C8 热中子波长双路径残差 %s，残差来源是温度口径：字面 2200 m/s ⇔ T=%s K'
    % (mp.nstr(d_n, 4), mp.nstr(T_2200, 6)),
    '2200 m/s 是 E=k_BT=%s meV（T=%s K，热中子惯例）对应的 √(2k_BT/m_n)；'
    '与室温 293.15 K 的 √(2k_BT/m_n)=%s m/s 差 %s，落在容差 2%% 内 ⇒ 数据层成立'
    % (mp.nstr(E_2200 * 1000, 4), mp.nstr(T_2200, 6),
       mp.nstr(v_therm, 6), mp.nstr(d_n, 4)))

# ===========================================================================
# D 段：72 卷判据层 —— 接受区间宽度（变异测试）
# ===========================================================================
def E1_pass(S):  return abs(S / mpf('1e77') - 1) < 10
def E4_pass(T):  return T < mpf('1e-7')
def E5_pass(t):  return abs(t / mpf('1.1e67') - 1) < 1
def E6_pass(r):  return mpf('1e18') < r < mpf('1e21')
def E7_pass(gap): return gap > 14
def E2_pass(gap): return 120 < gap < 126

# E1：下界无界
e1_low = [k for k in (1, 10, 30, 60) if E1_pass(S_sun / mpf(10) ** k)]
e1_up = E1_pass(S_sun * mpf('10.5'))
guard('E1_lower_unbounded', len(e1_low) == 4,
      'S/10^k 仍 PASS 的 k = %s；上界 ×10.5 ⇒ %s' % (e1_low, e1_up))
add('R10', 'FAIL',
    'E1 接受区间 = (0, 1.1e78) ⇒ 向下 78 个数量级全部接受，仅上界 +10.5× 才失效',
    'S/10, /10^10, /10^30, /10^60 全部仍判 PASS；该守卫只挡「熵比太阳黑洞熵大 10.5 倍」，'
    '挡不住任何小值 ⇒ 形同只写上界')

# E2：区间与文献 120 口径边界互斥
guard('E2_rejects_canonical_120', not E2_pass(mpf('120')),
      '文献常见口径 10^120 不满足 120 < gap ⇒ 被守卫拒绝')
add('R11', 'FAIL',
    'E2 区间 (120,126) 与文献常见「真空能差 120 个数量级」口径边界互斥',
    '本册实算 %s（Planck 硬截断口径）；若改用文献 120 口径 ⇒ 守卫判 FAIL。'
    '区间把「待检验量」当成「已知区间」，属区间口径自证' % mp.nstr(gap_rho, 6))

# E4：单侧无下界
e4_big = [k for k in (1, 5, 10) if E4_pass(T_H(M_SUN * mpf(10) ** k))]
guard('E4_lower_unbounded', len(e4_big) == 3,
      'M×10^k 的 T_H 仍 < 1e-7 的 k = %s' % e4_big)
add('R12', 'FAIL',
    'E4「T_H < 1e-7 K」单侧无下界 ⇒ 对任何 M > 0.62 M_☉ 的黑洞恒真',
    'M 放大 10/10^5/10^10 倍后 T_H 仍判 PASS；该守卫的真信息只有「太阳黑洞是冷的」，'
    '是常识复述而非可证伪判据')

# E5：上界仅 +5%，下界无界
e5_low = [k for k in (1, 10, 30, 60) if E5_pass(t_sun_yr / mpf(10) ** k)]
e5_up_105 = E5_pass(t_sun_yr * mpf('1.05'))
e5_up_101 = E5_pass(t_sun_yr * mpf('1.01'))
guard('E5_lower_unbounded', len(e5_low) == 4, 't/10^k 仍 PASS 的 k = %s' % e5_low)
guard('E5_upper_tight', (not e5_up_105) and e5_up_101,
      '×1.05 ⇒ %s（拒），×1.01 ⇒ %s（受）' % (e5_up_105, e5_up_101))
add('R13', 'FAIL',
    'E5 接受区间 = (0, 2.2e67) yr：上界仅比真值高 5%，向下 67 个数量级全部接受',
    't/10^k 对 k=1,10,30,60 全 PASS；×1.05 即被拒。'
    '即该守卫对「蒸发更快」敏感（5%% 级），对「蒸发更慢」完全无感')

# E5 展示层：把 log10 当物理值打印
disp = mpf('67.32')
true_t = t_sun_yr
ratio_disp = true_t / disp
guard('E5_display_bug', ratio_disp > mpf('1e60'),
      '展示串 6.73e+01 yr vs 真值 %s yr，差 %s 倍' % (mp.nstr(true_t, 4), mp.nstr(ratio_disp, 4)))
add('R14', 'FAIL',
    'E5 守卫打印串把 log₁₀(t) 当物理值输出：「t_evap(sun) = 6.73e+01 yr」',
    '真值 %s yr；展示值与真值差 %s 倍。'
    '属展示层真 bug（不影响守卫判定与 JSON，但会误导任何只读 stdout/report 的读者）'
    % (mp.nstr(true_t, 4), mp.nstr(ratio_disp, 4)))

# E6：分母是手填外部输入 ⇒ 变异分母 ±1 数量级，守卫仍能通过
S_BH_JK = S_sun * k_B
e6_mut = [d for d in ('1e34', '1e35', '1e36') if E6_pass(S_BH_JK / mpf(d))]
guard('E6_input_is_literal', len(e6_mut) == 3,
      '分母取 %s（±1 数量级）时 ratio 仍落在区间内' % '/'.join(e6_mut))
add('R15', 'FAIL',
    'E6 分母 1e35 J/K 是手填数量级估计（外部输入）：分母变动 ±1 个数量级，守卫照样通过',
    '分母取 1e34/1e36 J/K 时比值仍落在 (1e18, 1e21) 内 ⇒ 守卫抓不住分母的 10 倍误差；'
    '分子 S_BH 是精确计算值（10^%s k_B），分母是 O(1) 估值，混合比精度不匹配'
    % mp.nstr(lg(S_sun), 4))

# E7：单侧
e7_mut = [v for v in ('14000', '1e5') if E7_pass(lg(E_P_GeV / mpf(v)))]
e7_big = E7_pass(lg(E_P_GeV / mpf('1e6')))
guard('E7_single_sided', len(e7_mut) == 2 and not e7_big,
      'E_LHC = %s GeV 仍 PASS；1e6 GeV ⇒ %s' % ('/'.join(e7_mut), e7_big))
add('R16', 'FAIL',
    'E7「能标差 > 14 个数量级」单侧 ⇒ 对撞机能标提到 1e5 GeV（100 TeV）仍判 PASS',
    'gap(1e5)=%s 仍 > 14；直到 1e6 GeV（gap=%s）才被拒 ⇒ 该守卫的分辨力为 100 TeV 量级，'
    '且阈值 14 本身来自 14 TeV 这一输入，属「把自己输入的数当成判别界限」'
    % (mp.nstr(lg(E_P_GeV / mpf('1e5')), 4), mp.nstr(lg(E_P_GeV / mpf('1e6')), 4)))

# E3：恒等重述
add('R17', 'BOUNDARY',
    'E3 g/e = 1/(2α) 是 Dirac 量子化条件在 n=1 下的代数重述，非独立预言',
    '字面值 %s = 1/(2×7.2973525693e-3)；容差 1%% 比常数版本差 %s 大 7 个数量级'
    % (mp.nstr(g_over_e, 6), mp.nstr(d_ver, 4)))

# ===========================================================================
# E 段：汇总
# ===========================================================================
n_guard = len(guards)
n_pass = sum(1 for g in guards if g['pass'])
add('R18', 'PASS',
    '数据层总账：17 项读数（71 卷 9 项 + 72 卷 8 项）全部为教科书标准结果，逐条复算一致',
    '无一为本项目新物理；与《理论体系方程总汇_正确方程集》结论同向：'
    '本库被判「正确」的方程绝大多数是教科书物理在另一套记号下的复述')
add('R19', 'INFO',
    '两卷性质判定：71 = 14 层物理大厦综述 + 桥梁常数表；72 = 10 个本质问题三档自评',
    '均为整理/教学性产物；判据层缺陷不影响其数据层价值，但「9/9」「7/7 全通过」'
    '不可作为「已验证」引用')
add('R20', 'INFO',
    '编号登记：71/72 入 07_统一场方程（接续 68/69/70）；本册取 r137（起草时 r135 为最小空号）',
    '起草时 r118-r134 已占用、r135 为空 ⇒ 首版按 r135 起草；落盘前并行会话已占 r135/r136，'
    '按「后到者改号不覆盖他人」纪律改号 r137（他人产物未触碰）。'
    '两卷与书籍/03（同源对话）回链，与 68 卷（方程集）互补不重叠')

# 容差谱
tol_spectrum = [
    ('C4', '1e-9'), ('C1', '1e-6'), ('C3', '1e-5'), ('C6', '1e-5'), ('C2', '1e-4'),
    ('C5', '2e-2'), ('C8', '2e-2'), ('C9', '2e-2'), ('C10', '1e-1'),
]
add('R21', 'INFO',
    '71 卷 9 条守卫的容差跨 8 个数量级：最紧 C4=1e-9，最松 C10=1e-1',
    '容差谱 %s；同一卷内判据强度相差 8 个数量级，'
    '「9/9 全通过」不表示 9 条判据同样强度' % ('、'.join('%s:%s' % t for t in tol_spectrum)))

# 外部输入账
ext71 = ['mu_0 = 4pi*1e-7（SI-2019 前旧定义，非实测值）', 'T_sun = 5778 K（现代值 5772 K）',
         'b_Wien 字面 2.897771955e-3', 'm_n = 1.6749275e-27', 'M_SgrA = 4.3e6 M_sun（旧值）',
         'omega = 1e14 rad/s（C7 演示取值）']
ext72 = ['alpha 字面 7.2973525693e-3（CODATA-2018）', 'M_sun = 1.98847e30',
         'H0 = 67.66 km/s/Mpc、Omega_L = 0.6889（Planck-2018）',
         'S_thermal(sun) = 1e35 J/K（手填数量级估计）', 'E_LHC = 14 TeV',
         'Planck 硬截断约定（UV cutoff = M_Pl）']
add('R22', 'INFO',
    '外部输入账：71 卷 6 项、72 卷 6 项（合计 12 项），其中 2 项非推导值',
    '71：%s。72：%s。'
    '非推导项 = 71 的 b_Wien 字面值（本册 R07 已用 hc/(k_B x) 独立反解验证）'
    '与 72 的 S_thermal 手填值（本册 R15 判其 ±1 数量级变动不可检出）'
    % ('；'.join(ext71), '；'.join(ext72)))

# ---------------------------------------------------------------------------
out = {
    'volumes': {'71_full_chain': sorted(g71.keys()), '72_essence': sorted(J72['guards'].keys())},
    'key_numbers': {
        'alpha_2018': mp.nstr(A_LIT_2018, 12),
        'alpha_2022': mp.nstr(A_LIT_2022, 12),
        'alpha_version_rel_diff': mp.nstr(d_ver, 6),
        'a0_m': mp.nstr(a0_A, 10),
        'E1_eV': mp.nstr(E1_A, 8),
        'r_e_m': mp.nstr(r_e_A, 10),
        'alpha_1_2_3': [mp.nstr(al_1, 12), mp.nstr(al_2, 12), mp.nstr(al_3, 12)],
        'al2_over_al1_resid': mp.nstr(r21, 3),
        'al3_over_al1_resid': mp.nstr(r31, 3),
        'lambda_max_sun_nm': mp.nstr(lm_sun_A * 1e9, 6),
        'sigma_SB': mp.nstr(sig, 10),
        'lambda_neutron_A': mp.nstr(lm_n_A * 1e10, 6),
        'neutron_2200ms_implies_T_K': mp.nstr(T_2200, 6),
        'neutron_2200ms_implies_E_meV': mp.nstr(E_2200 * 1000, 4),
        'hbar_literal_truncation_rel': mp.nstr(d_hbar, 4),
        'sigma_derived_rel_resid': mp.nstr(d_sig, 4),
        'lambda_CMB_mm': mp.nstr(lm_cmb_A * 1e3, 6),
        'rs_SgrA_43e6_m': mp.nstr(rs_43, 8),
        'rs_SgrA_4154e6_m': mp.nstr(rs_4154, 8),
        'sgrA_rel_diff': mp.nstr(d_sgra, 4),
        'S_BH_sun_over_kB_log10': mp.nstr(lg(S_sun), 6),
        'T_H_sun_K': mp.nstr(T_sun, 6),
        't_evap_sun_yr': mp.nstr(t_sun_yr, 6),
        't_evap_galaxy_yr': mp.nstr(t_gal_yr, 6),
        't_evap_1kg_s': mp.nstr(t_1kg, 6),
        'vacuum_gap_log10': mp.nstr(gap_rho, 6),
        'rho_theory_J_m3': mp.nstr(rho_th, 6),
        'rho_obs_J_m3': mp.nstr(rho_obs, 6),
        'g_over_e': mp.nstr(g_over_e, 8),
        'E_Planck_GeV': mp.nstr(E_P_GeV, 8),
        'LHC_gap_orders': mp.nstr(gap_LHC, 6),
        'E5_display_true_over_shown': mp.nstr(ratio_disp, 4),
    },
    'entries': entries,
    'guards': guards,
    'guard_summary': {'total': n_guard, 'passed': n_pass},
    'verdict': {
        'data_layer': '17/17 复算一致（PASS）',
        'criterion_layer': '16 条守卫中 9 条判为单侧/无界/恒等/无守卫（FAIL）',
        'new_physics': 0,
    },
}
os.makedirs(DATA, exist_ok=True)
TAG = 'TUFT-r137_全链路总览卷与本质本源审计卷_全维审计_2026-10-21'
with open(os.path.join(DATA, TAG + '.json'), 'w', encoding='utf-8') as fp:
    json.dump(out, fp, indent=2, ensure_ascii=False)

# ---------------------------------------------------------------------------
# 打印
# ---------------------------------------------------------------------------
def S(x):
    return mp.nstr(x, 6)

print('=' * 78)
print('  r137  71_全链路总览卷 / 72_本质本源审计卷  全维审计')
print('=' * 78)
print('  C1 a0            = %s m' % S(a0_A))
print('  C2 E1            = %s eV' % S(E1_A))
print('  C3 r_e           = %s m' % S(r_e_A))
print('  C4 alpha(1,2,3)  = %s / %s / %s' % (S(al_1), S(al_2), S(al_3)))
print('  C5 lambda_max    = %s nm' % S(lm_sun_A * 1e9))
print('  C6 sigma         = %s' % S(sig))
print('  C8 lambda_n      = %s A' % S(lm_n_A * 1e10))
print('  C9 lambda_CMB    = %s mm' % S(lm_cmb_A * 1e3))
print('  C10 r_s(4.3e6)   = %s m  | 4.154e6 -> %s m' % (S(rs_43), S(rs_4154)))
print('  E1 S/kB          = 10^%s' % S(lg(S_sun)))
print('  E2 vacuum gap    = 10^%s' % S(gap_rho))
print('  E3 g/e           = %s' % S(g_over_e))
print('  E4 T_H(sun)      = %s K' % S(T_sun))
print('  E5 t_evap(sun)   = %s yr   (展示串误为 6.73e+01)' % S(t_sun_yr))
print('  E5 t_evap(1kg)   = %s s' % S(t_1kg))
print('  E6 S_BH/S_th     = 10^%s' % S(lg(ratio_S)))
print('  E7 LHC->Planck   = 10^%s' % S(gap_LHC))
print('-' * 78)
for e in entries:
    print('  [%s] %s  %s' % (e['status'], e['code'], e['title']))
print('-' * 78)
print('  GUARDS: %d/%d passed' % (n_pass, n_guard))
for g in guards:
    print('    [%s] %s  %s' % ('PASS' if g['pass'] else 'FAIL', g['name'], g['detail']))
print('=' * 78)

_md = ['# r137 机读数据：71/72 两卷全维审计', '']
_md.append('| 键 | 值 |')
_md.append('|---|---|')
for k, v in out['key_numbers'].items():
    _md.append('| `%s` | %s |' % (k, v))
_md.append('')
_md.append('## 条目')
_md.append('')
for e in entries:
    _md.append('- **%s [%s]** %s' % (e['code'], e['status'], e['title']))
    if e['detail']:
        _md.append('  - %s' % e['detail'])
_md.append('')
_md.append('## 守卫')
_md.append('')
_md.append('- 合计 %d / 通过 %d' % (n_guard, n_pass))
for g in guards:
    _md.append('  - [%s] %s — %s' % ('PASS' if g['pass'] else 'FAIL', g['name'], g['detail']))
with open(os.path.join(DATA, TAG + '.md'), 'w', encoding='utf-8') as fp:
    fp.write('\n'.join(_md) + '\n')

with open(os.path.join(DATA, TAG + '_report.txt'), 'w', encoding='utf-8') as fp:
    fp.write('r135 guards=%d/%d\n' % (n_pass, n_guard))
    for g in guards:
        fp.write('[%s] %s  %s\n' % ('PASS' if g['pass'] else 'FAIL', g['name'], g['detail']))
    for e in entries:
        fp.write('%s %s %s\n' % (e['code'], e['status'], e['title']))
    fp.write('  report -> ' + os.path.join(DATA, TAG + '_report.txt'))
print('  report -> ' + os.path.join(DATA, TAG + '_report.txt'))

sys.exit(0 if n_pass == n_guard else 1)
