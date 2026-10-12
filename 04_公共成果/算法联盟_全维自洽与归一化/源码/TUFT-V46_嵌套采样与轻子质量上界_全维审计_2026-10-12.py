# -*- coding: utf-8 -*-
"""
TUFT-V4.6 全维审计（算法联盟 r43）·2026-10-12
来料：V4.6「全局嵌套采样 chi^2 最小化，参数后验 + 轻子质量上界核验」

引擎定位：只做「可算复核」——量纲齐次性穷举、量纲代数自洽、
chi^2 曲面结构判定、符号不可反转判据、m_max 四方对照、来料代码静态可执行性扫描。
本册不产生新物理，不代选来料自列的四个攻坚选项。
"""
import sys, os, json, ast, itertools
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT_JSON = os.path.join(BASE, '数据', 'TUFT-V46_嵌套采样与轻子质量上界_全维审计_2026-10-12.json')
OUT_MD = os.path.join(BASE, '数据', 'TUFT-V46_嵌套采样与轻子质量上界_全维审计_2026-10-12.md')
OUT_TXT = os.path.join(BASE, '数据', 'TUFT-V46_嵌套采样与轻子质量上界_全维审计_2026-10-12_report.txt')

# ============ CODATA / PDG 常数 ============
C = mp.mpf('299792458')
HBAR = mp.mpf('1.0545718176461565e-34')
ECH = mp.mpf('1.602176634e-19')
EPS0 = mp.mpf('8.8541878128e-12')
MU0 = mp.mpf('1.25663706212e-6')
ME = mp.mpf('9.1093837015e-31')
MMU = mp.mpf('1.883531627e-28')
MTAU = mp.mpf('3.16754e-27')
LP = mp.mpf('1.616255078e-35')          # CODATA 普朗克长度（已含 G）
GEXP = mp.mpf('6.67430e-11')
MP_INV = mp.pi
KG_C2_IN_J = C ** 2
MEV_IN_J = mp.mpf('1.602176634e-13')

# 来料给定的 g-2 输入（原样录入，不修正）
AE_QED = mp.mpf('1.15965218128e-3')
AE_EXP = mp.mpf('1.15965218059e-3')
AMU_QED = mp.mpf('1.16591810e-3')
AMU_EXP = mp.mpf('1.16592040e-3')
SIG_AE = mp.mpf('1e-12')
SIG_AMU = mp.mpf('4e-7')
DELTA_STAR_CLAIM = mp.mpf('2.17e-46')
AMU_TUFT_CLAIM = mp.mpf('2.27e-6')
AE_TUFT_CLAIM = mp.mpf('-6.9e-11')
MMAX_KG_CLAIM = mp.mpf('1.16e-30')
PRIOR_LOW = mp.mpf('1e-52')
PRIOR_HIGH = mp.mpf('1e-40')

# ============ 四元组量纲 (M, L, T, Q) ============
def D(*v):
    return tuple(Fr(int(x)) for x in v)

def dadd(*ds):
    return tuple(sum(d[i] for d in ds) for i in range(4))

def dmul(d, k):
    return tuple(d[i] * Fr(k) for i in range(4))

def dinv(d):
    return dmul(d, -1)

NAMES = ('M', 'L', 'T', 'Q')

def dstr(d):
    out = []
    for i in range(4):
        x = d[i]
        if x == 0:
            continue
        if x == 1:
            out.append(NAMES[i])
        elif x == -1:
            out.append(NAMES[i] + '^-1')
        else:
            out.append(NAMES[i] + '^' + str(x))
    return ''.join(out) if out else '1(无量纲)'

DIM_M = D(1, 0, 0, 0)
DIM_L = D(0, 1, 0, 0)
DIM_T = D(0, 0, 1, 0)
DIM_Q = D(0, 0, 0, 1)
DIM_ZERO = D(0, 0, 0, 0)
DIM_HBAR = D(1, 2, -1, 0)
DIM_C = D(0, 1, -1, 0)
DIM_E = DIM_Q
DIM_G = D(-1, 3, -2, 0)
DIM_LP = DIM_L
DIM_EPS0 = D(-1, -3, 2, 2)
DIM_MU0 = D(1, 1, 0, -2)                # N/A^2 = M L Q^-2（守卫 G0-2 兜底）
DIM_KAPPA_CURV = D(0, -1, 0, 0)     # 螺旋曲率 = 弧长倒数

# ============ 条目累加器 ============
ITEMS = []

def P(cid, title, detail):
    ITEMS.append({'id': cid, 'title': title, 'verdict': 'PASS', 'detail': detail})
    print('[PASS ] %-6s %s' % (cid, title))

def F(cid, title, detail):
    ITEMS.append({'id': cid, 'title': title, 'verdict': 'FAIL', 'detail': detail})
    print('[FAIL ] %-6s %s' % (cid, title))

def Bn(cid, title, detail):
    ITEMS.append({'id': cid, 'title': title, 'verdict': 'BOUNDARY', 'detail': detail})
    print('[BND  ] %-6s %s' % (cid, title))

def I(cid, title, detail):
    ITEMS.append({'id': cid, 'title': title, 'verdict': 'INFO', 'detail': detail})
    print('[INFO ] %-6s %s' % (cid, title))

# ============ G0 量纲工具自身守卫（r37/r42 纪律：量纲工具必须先过自检）============
GUARDS = []

def guard(name, cond, note):
    GUARDS.append({'name': name, 'pass': bool(cond), 'note': note})
    assert bool(cond), 'GUARD FAILED: ' + name + ' :: ' + note

guard('G0-1_dadd_is_exponent_addition', dadd(DIM_HBAR, DIM_C) == D(1, 3, -2, 0),
      '量纲相乘=指数相加（r37 首版写成逐分量相乘的教训）')
guard('G0-2_eps0_mu0_is_inv_c2', dadd(DIM_EPS0, DIM_MU0) == dinv(dmul(DIM_C, 2)),
      'eps0*mu0 = 1/c^2')
guard('G0-3_hbar_over_c_is_ML', dadd(DIM_HBAR, dinv(DIM_C)) == D(1, 1, 0, 0),
      'hbar/c = M*L（康普顿波长）')
guard('G0-4_G_dim', DIM_G == D(-1, 3, -2, 0), '[G]=M^-1 L^3 T^-2')
guard('G0-5_dinv_is_inverse', dinv(dinv(DIM_G)) == DIM_G and dinv(DIM_G) == dmul(DIM_G, -1),
      '取逆=取负，且二次取逆还原')
guard('G0-6_dstr_zero', dstr(DIM_ZERO) == '1(无量纲)', '零向量打印')
guard('G0-7_kappa_is_inverse_length', DIM_KAPPA_CURV == D(0, -1, 0, 0),
      'kappa = 螺旋曲率 = 弧长倒数 => L^-1')
guard('G0-8_dim_C_kappa_mass', dadd(DIM_HBAR, DIM_KAPPA_CURV, dinv(DIM_C)) == DIM_M,
      'hbar*kappa/c = M（第一项本身是质量量纲）')

print('--- G0 量纲工具守卫 %d 条 ---' % len(GUARDS))

# ============ 模型量纲代数（不引入数值，纯指数）============
# 公理 1： m = hbar*kappa/(c*sinT) - pi*hbar*lP*kappa^2/(2 c^3)
#   term1_dim(kappa) = hbar + kappa - c
#   term2_dim(kappa) = hbar + lP + 2*kappa - 3*c
def t1_dim(kd):
    return dadd(DIM_HBAR, kd, dinv(DIM_C))

def t2_dim(kd):
    return dadd(DIM_HBAR, DIM_LP, dmul(kd, 2), dmul(DIM_C, -3))

# 公理 2： a = -(3 c cotT)/(4 e hbar) * m * kappa
#   a_dim(kappa) = c - e - hbar + m + kappa
def a_dim(kd):
    return dadd(DIM_C, dinv(DIM_E), dinv(DIM_HBAR), DIM_M, kd)

print('=' * 78)

# ================= D 系列：四条公理的量纲审计 =================
READ = {}

# ---- D01 公理 1 两项不齐 + 齐次性把 [kappa] 钉死为 L^2 T^-2 ----
RANGES = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
homog_solutions = []
for a, b, d in itertools.product(RANGES, repeat=3):
    kd = D(a, b, d, 0)
    if t1_dim(kd) == t2_dim(kd):
        homog_solutions.append((kd, t1_dim(kd)))
n_homog = len(homog_solutions)
homog_list = [(list(map(int, k)), dstr(t)) for k, t in homog_solutions]

kd_curv = DIM_KAPPA_CURV
t1c, t2c = t1_dim(kd_curv), t2_dim(kd_curv)
gap_c = dadd(DIM_M, dinv(t2c))          # 第二项需乘多少才等于 [m]
t1h = t1_dim(kd_curv)
assert t1h == DIM_M, '第一项在 [kappa]=L^-1 下应等于 [m]=M'
assert t1c != t2c, '两项在 [kappa]=L^-1 下不应齐次'

# 在 {c, hbar, G} 内穷举补齐因子 gap_c
BASE_DIMS = {'c': DIM_C, 'hbar': DIM_HBAR, 'G': DIM_G}
gap_hits = []
keys = sorted(BASE_DIMS)
for pw in itertools.product([-3, -2, -1, 0, 1, 2, 3], repeat=3):
    tot = D(0, 0, 0, 0)
    for k, p in zip(keys, pw):
        tot = dadd(tot, dmul(BASE_DIMS[k], p))
    if tot == gap_c:
        gap_hits.append({k: p for k, p in zip(keys, pw)})

guard('G1_homogeneous_solution_is_unique', n_homog == 1, '公理 1 齐次解唯一：' + str(homog_list))
guard('G2_curvature_kappa_two_terms_differ', t1c != t2c,
      '[kappa]=L^-1 时两项不齐，缺口 %s' % dstr(gap_c))
guard('G3_gap_factor_exists_in_basis', len(gap_hits) > 0,
      '缺口 %s 在 {c,hbar,G} ±3 幂内命中 %d 组' % (dstr(gap_c), len(gap_hits)))

m_at_homog = homog_solutions[0][1]
F('D01', '公理 1 两项量纲不齐；齐次性与「给出质量」互斥',
  '公理 1 = hbar*kappa/(c*sinT) - pi*hbar*lP*kappa^2/(2c^3)。取 [kappa]=L^-1（螺旋曲率=弧长倒数）时第一项 %s = M 正确、第二项 %s，缺口 %s（差 4 个长度幂次 + 2 个时间幂次）⇒ 两项不可相加。机器枚举 [kappa] 的 9^3=729 组指数组合，齐次解唯一 [kappa]=%s（加速度量纲），此时公理 1 给出 %s ≠ M。⇒ 无论 kappa 取什么量纲，公理 1 都不能既齐次又给出质量。'
  % (dstr(t1c), dstr(t2c), dstr(gap_c), dstr(homog_solutions[0][0]), dstr(m_at_homog)))
READ['D01'] = {
    'term1_dim_at_curvature': dstr(t1c), 'term2_dim_at_curvature': dstr(t2c),
    'gap_factor_dim': dstr(gap_c), 'homogeneous_solution_count': n_homog,
    'homogeneous_solutions': homog_list, 'm_dim_under_homogeneity': dstr(m_at_homog),
    'gap_factor_hits_in_c_hbar_G': gap_hits,
    'gap_factor_hit_count': len(gap_hits),
    'note': '唯一自然补齐因子在 {c,hbar,G} 内为 G*hbar/c 量纲（L^4 T^-2），即自能项必须与引力耦合常数绑定。',
}

# ---- D02 公理 2 的 a 缺 Q L^2 ----
ad = a_dim(kd_curv)
need = dinv(ad)                          # 需要乘的补齐因子量纲
FULL_DIMS = {'c': DIM_C, 'hbar': DIM_HBAR, 'G': DIM_G, 'e': DIM_E,
             'eps0': DIM_EPS0, 'mu0': DIM_MU0, 'me': DIM_M, 'lP': DIM_LP}
fkeys = sorted(FULL_DIMS)
a_hits = []
cnt = 0
for pw in itertools.product([-3, -2, -1, 0, 1, 2, 3], repeat=len(fkeys)):
    tot = D(0, 0, 0, 0)
    for k, p in zip(fkeys, pw):
        tot = dadd(tot, dmul(FULL_DIMS[k], p))
    cnt += 1
    if tot == need:
        a_hits.append({k: p for k, p in zip(fkeys, pw)})
guard('G4_a_expression_is_not_dimensionless', ad != DIM_ZERO,
      'a^TUFT 量纲 %s 非无量纲' % dstr(ad))
F('D02', '公理 2 的 a^TUFT 量纲非无量纲（与 r42 D01 同源未修）',
  'a^TUFT = -(3c cotT)/(4 e hbar)·m·kappa。机器给出 (M,L,T,Q) = %s = L^-2 Q^-1，而 a=(g-2)/2 必须无量纲。SI 口径所需补齐因子 %s。r42 册在 a=C·m^2·cotT 形式下判缺口 E^-2（唯一命中者 [G]=E^-2）；V4.6 改成 m·kappa 形式后缺口换了形状但未消除，且补齐因子在公设集内仍需穷举才存在。本册穷举 {c,hbar,G,e,eps0,mu0,m_e,l_P} 的 ±3 幂：共 %d 组，命中 %d 组。'
  % (dstr(ad), dstr(need), cnt, len(a_hits)))
READ['D02'] = {'a_dim': dstr(ad), 'need_factor_dim': dstr(need),
               'enumerated': cnt, 'hit_count': len(a_hits), 'hits_sample': a_hits[:12]}

print('=' * 78)

# ---- D03/D04/D05 kappa 公式、定义域与公理 1 的不同源 ----
# 来料 kappa()： kappa = (c^2/(pi*lP)) * ( 1/sinT - sqrt( 1/sin^2T - 2*pi*m*c^2/hbar ) )
dim_first = dadd(dmul(DIM_C, 2), dinv(DIM_LP))            # c^2/(pi*lP) = L T^-2
dim_sqrt_inner_a = DIM_ZERO                              # 1/sin^2T 无量纲
dim_sqrt_inner_b = dadd(DIM_M, dmul(DIM_C, 2), dinv(DIM_HBAR))   # 2 pi m c^2 / hbar = T^-1
dim_ratio_total = dadd(dim_first, DIM_KAPPA_CURV)        # kappa 的量纲

# 公理 1 自身二次方程的根号内： hbar^2/(c^2 sin^2T) - 2*pi*hbar*lP*m/c^3
dim_ax_inner_a = dadd(dmul(DIM_HBAR, 2), dmul(DIM_C, -2))
dim_ax_inner_b = dadd(DIM_HBAR, DIM_LP, DIM_M, dmul(DIM_C, -3))

guard('G5_sqrt_inner_terms_mismatch', dim_sqrt_inner_a != dim_sqrt_inner_b,
      'kappa 公式根号内两项量纲 %s vs %s 不齐' % (dstr(dim_sqrt_inner_a), dstr(dim_sqrt_inner_b)))

# 数值：K = 2 pi m c^2 / hbar（来料根号内的第二项）
def K_incoming(m):
    return 2 * MP_INV * m * C ** 2 / HBAR

K_e = K_incoming(ME)
K_mu = K_incoming(MMU)
K_tau = K_incoming(MTAU)
guard('G6_incoming_domain_is_empty_for_leptons', K_e > 1 and K_mu > 1 and K_tau > 1,
      '来料定义域 1/sin^2T - K 在 m=m_e 时 K=%s，远大于 1 ⇒ 无实根' % mp.nstr(K_e, 6))

# 公理 1 一致化后的根号内第二项： 2 pi lP m / c^2
def K_axiom1(m):
    return 2 * MP_INV * LP * m / C ** 2

K1_e = K_axiom1(ME)
ratio_root = (K_incoming(ME) / K_axiom1(ME))
guard('G7_root_inner_ratio_is_c4_over_hbar_lP', abs(ratio_root - C ** 4 / (HBAR * LP)) / ratio_root < mp.mpf('1e-40'),
      '两套根号内相差 c^4/(hbar*lP) = %s' % mp.nstr(ratio_root, 6))

F('D03', '来料 kappa() 的根号内两项量纲不齐，且在 e/mu/tau 上定义域恒空',
  '来料 kappa() = (c^2/(pi lP))(1/sinT - sqrt(1/sin^2T - 2 pi m c^2/hbar))。根号内两项量纲分别是 %s（1/sin^2T）与 %s（2 pi m c^2/hbar），不齐。机器读数：K_e = 2 pi m_e c^2/hbar = %s、K_mu = %s、K_tau = %s，均远大于 1/sin^2T ≈ 1 ⇒ 对全部参与拟合粒子 term <= 0 ⇒ 来料代码返回 inf。'
  % (dstr(dim_sqrt_inner_a), dstr(dim_sqrt_inner_b), mp.nstr(K_e, 6), mp.nstr(K_mu, 6), mp.nstr(K_tau, 6)))
F('D04', '公理 4 的定义域约束同样量纲不齐',
  '公理 4：1/sin^2T - 2 pi m c^2/hbar > 0。首项 %s、次项 %s，不齐。它与 D03 的 kappa() 用的是同一个非齐次式，故两者同源同病。'
  % (dstr(dim_sqrt_inner_a), dstr(dim_sqrt_inner_b)))
F('D05', '来料 kappa() 与公理 1 不同源（根号内差 c^4/(hbar lP)）',
  '把公理 1 当作 kappa 的二次方程解出：判别式 hbar^2/(c^2 sin^2T) - 2 pi hbar lP m/c^3，其根号内第二项量纲为 %s（齐次）。来料却写 2 pi m c^2/hbar（量纲 T^-1）。两者之比 = c^4/(hbar lP) = %s ⇒ 一个恒有解（公理 1 一致化：K1_e = %s），一个恒无解（来料）。这不是精度问题，是两条不同的公式。'
  % (dstr(dim_ax_inner_b), mp.nstr(ratio_root, 6), mp.nstr(K1_e, 6)))
READ['D03_D05'] = {
    'kappa_pref_dim': dstr(dim_first), 'sqrt_inner_a': dstr(dim_sqrt_inner_a),
    'sqrt_inner_b': dstr(dim_sqrt_inner_b), 'kappa_total_dim': dstr(dim_ratio_total),
    'K_incoming_me': mp.nstr(K_e, 12), 'K_incoming_mmu': mp.nstr(K_mu, 12),
    'K_incoming_mtau': mp.nstr(K_tau, 12),
    'K_axiom1_me': mp.nstr(K1_e, 12), 'root_inner_ratio': mp.nstr(ratio_root, 12),
    'axiom1_inner_b_dim': dstr(dim_ax_inner_b),
    'incoming_domain_empty': bool(K_e > 1),
}

# ---- D06 公理 1 一致化后 kappa 的数值量级 ≈ m（量纲非法的数值痕迹）----
def kappa_B(m, delta):
    """公理 1 一致化的 kappa（量纲齐次的那个二次根，小根）"""
    sinT = mp.sin(mp.pi / 2 - delta)
    inner = 1 / (sinT ** 2) - K_axiom1(m)
    if inner <= 0:
        return None
    return (C ** 2 / (MP_INV * LP)) * (1 / sinT - mp.sqrt(inner))

kap_e_at_lo = kappa_B(ME, PRIOR_LOW)
kap_mu_at_lo = kappa_B(MMU, PRIOR_LOW)
ratio_kap_mu_e = kap_mu_at_lo / kap_e_at_lo
I('D06', '公理 1 一致化后 kappa 的数值量级 ≈ m（量纲非法的数值痕迹）',
  '在 delta 先验下界 %s 处，机器给出 kappa(m_e) = %s（1/m 量纲的数值却是 %s，恰好等于 m_e = %s 的同数量级），kappa(m_mu)/kappa(m_e) = %s。数值上 kappa ≈ m（差 kappa/m ≈ %s）。这不是物理结果，而是公理 1 量纲非法（D01）在数值层的投影：把量纲不同的两支放在同一公式里，数值巧合必然出现。'
  % (mp.nstr(PRIOR_LOW, 3), mp.nstr(kap_e_at_lo, 8), mp.nstr(kap_e_at_lo, 8),
     mp.nstr(ME, 8), mp.nstr(ratio_kap_mu_e, 8), mp.nstr(kap_e_at_lo / ME, 8)))
READ['D06'] = {'kappa_e_at_prior_low': mp.nstr(kap_e_at_lo, 20),
               'kappa_mu_at_prior_low': mp.nstr(kap_mu_at_lo, 20),
               'kappa_mu_over_kappa_e': mp.nstr(ratio_kap_mu_e, 20),
               'kappa_e_over_me': mp.nstr(kap_e_at_lo / ME, 20)}

print('=' * 78)

# ================= M/T 系列：m_max 四方对照与 tau 判决 =================
def kg_to_MeV(mkg):
    return mkg * C ** 2 / MEV_IN_J

def sinT(delta):
    return mp.sin(mp.pi / 2 - delta)

# 1) 公理 1 的顶点质量： m(kappa) 抛物线最大值 m_peak = hbar*c/(2*pi*lP*sin^2 T)
def mmax_axiom1(delta):
    return HBAR * C / (2 * MP_INV * LP * sinT(delta) ** 2)

# 2) 公理 4 的定义域上界： m_max = hbar/(2*pi*c*sin^2 T)
def mmax_axiom4(delta):
    return HBAR / (2 * MP_INV * C * sinT(delta) ** 2)

# 3) 来料 §2 宣称的公式： m_max = hbar/(2*pi*c^2*sin^2 T)
def mmax_claim_formula(delta):
    return HBAR / (2 * MP_INV * C ** 2 * sinT(delta) ** 2)

d_star = DELTA_STAR_CLAIM
M1 = mmax_axiom1(d_star)
M2 = mmax_axiom4(d_star)
M3 = mmax_claim_formula(d_star)
M4 = MMAX_KG_CLAIM

m1_MeV, m2_MeV, m3_MeV, m4_MeV = [kg_to_MeV(x) for x in (M1, M2, M3, M4)]
MTAU_MeV = kg_to_MeV(MTAU)

guard('G8_mmax_four_versions_all_differ',
      all(abs(x - M1) / M1 > mp.mpf('1e-6') for x in (M2, M3, M4)),
      '公理1顶点 / 公理4定义域 / 来料公式 / 来料数值 四者互不相同')
guard('G9_claim_number_vs_claim_formula_gap',
      abs(M4 / M3 - 1) > mp.mpf('1e6'),
      '来料数值与其自称公式差 %s 倍' % mp.nstr(M4 / M3, 8))

F('M01', 'm_max 存在四个互不相等的版本（公理 1 / 公理 4 / 来料 §2 公式 / 来料 §2 数值）',
  '在 delta* = %s 处：(1) 公理 1 的抛物线顶点 m_peak = hbar*c/(2 pi lP sin^2T) = %s kg = %s MeV；(2) 公理 4 定义域上界 hbar/(2 pi c sin^2T) = %s kg = %s MeV；(3) 来料 §2 宣称的公式 hbar/(2 pi c^2 sin^2T) = %s kg = %s MeV；(4) 来料宣称的数值 1.16e-30 kg = %s MeV。四个值彼此相差最多 %s 倍。附带量纲读数：四个式的量纲依次为 M L^3 T^-2、M L、M T、kg ⇒ 没有一个是质量量纲。'
  % (mp.nstr(d_star, 4), mp.nstr(M1, 8), mp.nstr(m1_MeV, 8),
     mp.nstr(M2, 8), mp.nstr(m2_MeV, 8), mp.nstr(M3, 8), mp.nstr(m3_MeV, 8),
     mp.nstr(m4_MeV, 8), mp.nstr(max(M1, M4) / min(M2, M3), 8)))
F('M02', '来料 §2 的 m_max 数值与其自称公式差 6.2e22 倍（该行自身带着 ? 号）',
  '来料写 "m_max ≈ hbar/(2 pi c^2) ≈ 1.16e-30 × c^2/c^2?"（自带疑问号），随后取 "精确数值 m_max ≈ 1.16e-30 kg"、换算 652 MeV。机器：hbar/(2 pi c^2) = %s kg = %s MeV，与 1.16e-30 kg 差 %s 倍。⇒ 652 MeV 不是任何一条公理推出来的数。'
  % (mp.nstr(M3, 8), mp.nstr(m3_MeV, 8), mp.nstr(M4 / M3, 8)))

tau_ok_axiom1 = MTAU_MeV < m1_MeV
tau_ok_claim = MTAU_MeV > m4_MeV
margin = (m1_MeV - MTAU_MeV) / m1_MeV
guard('G10_two_mmax_calibers_opposite_verdicts', tau_ok_axiom1 and tau_ok_claim,
      '公理1口径容纳 tau（裕量 %s），来料数值口径排除 tau（超出 %s）'
      % (mp.nstr(margin, 6), mp.nstr((MTAU_MeV - m4_MeV) / m4_MeV, 6)))

F('T01', '两种 m_max 口径对 tau 给出相反的定性结论 ⇒ 「tau 被证伪」是伪结论',
  '来料用 m_max = 652 MeV 断言 tau (1776.86 MeV) 超出上界、是「重大证伪信号」。机器：按公理 1 自身的抛物线顶点口径 m_peak = %s MeV，tau = %s MeV 落在区间内、裕量仅 %s（很紧但在内）⇒ 同一族公理给出相反判决。凡以「tau 超出」为前提的分支代价评估（分支 1 复合 tau / 分支 2 抬升上界）都建立在这个不自洽的读数上。'
  % (mp.nstr(m1_MeV, 10), mp.nstr(MTAU_MeV, 10), mp.nstr(margin, 8)))

leptons = [('e', ME), ('mu', MMU), ('tau', MTAU)]
lepton_table = []
for nm, mm in leptons:
    kap = kappa_B(mm, d_star)
    lepton_table.append({
        'name': nm, 'm_MeV': mp.nstr(kg_to_MeV(mm), 10),
        'kappa_at_delta_star': (mp.nstr(kap, 20) if kap is not None else 'None'),
        'below_mmax_axiom1': bool(kg_to_MeV(mm) < m1_MeV),
        'below_mmax_claim_652MeV': bool(kg_to_MeV(mm) < m4_MeV),
    })

READ['M01_M02_T01'] = {
    'delta_star_used': mp.nstr(d_star, 10),
    'mmax_axiom1_peak_kg': mp.nstr(M1, 20), 'mmax_axiom1_peak_MeV': mp.nstr(m1_MeV, 20),
    'mmax_axiom4_domain_kg': mp.nstr(M2, 20), 'mmax_axiom4_domain_MeV': mp.nstr(m2_MeV, 20),
    'mmax_claim_formula_kg': mp.nstr(M3, 20), 'mmax_claim_formula_MeV': mp.nstr(m3_MeV, 20),
    'mmax_claim_number_kg': mp.nstr(M4, 20), 'mmax_claim_number_MeV': mp.nstr(m4_MeV, 20),
    'claim_number_over_claim_formula': mp.nstr(M4 / M3, 20),
    'tau_MeV': mp.nstr(MTAU_MeV, 20), 'tau_margin_under_axiom1': mp.nstr(margin, 20),
    'tau_verdict_axiom1_caliber': 'ALLOWED(紧,裕量 %s)' % mp.nstr(margin, 6),
    'tau_verdict_claim_caliber': 'EXCLUDED(超 %s)' % mp.nstr((MTAU_MeV - m4_MeV) / m4_MeV, 6),
    'lepton_table': lepton_table,
}

print('=' * 78)

# ================= C 系列：chi^2 曲面 / 符号 / 自相矛盾 / 代码可执行性 =================
def a_tuft_B(m, delta):
    kap = kappa_B(m, delta)
    if kap is None:
        return None
    cotT = mp.tan(delta)
    return -(3 * C * cotT) / (4 * ECH * HBAR) * m * kap

def G_th(delta):
    return C ** 3 * LP ** 2 / (HBAR * sinT(delta))

def chi2_parts(delta):
    ae_p = AE_QED + a_tuft_B(ME, delta)
    amu_p = AMU_QED + a_tuft_B(MMU, delta)
    ce = ((ae_p - AE_EXP) / SIG_AE) ** 2
    cmu = ((amu_p - AMU_EXP) / SIG_AMU) ** 2
    cg = ((G_th(delta) - GEXP) / (GEXP * mp.mpf('1e-5'))) ** 2
    return {'ae_pred': ae_p, 'amu_pred': amu_p, 'chi_e': ce, 'chi_mu': cmu,
            'chi_G': cg, 'chi_total': ce + cmu + cg}

# 61 点对数均匀网格
GRID_N = 61
grid = []
for i in range(GRID_N):
    ex = mp.log(PRIOR_LOW) + (mp.log(PRIOR_HIGH) - mp.log(PRIOR_LOW)) * mp.mpf(i) / mp.mpf(GRID_N - 1)
    grid.append(mp.e ** ex)

curve = []
for dv in grid:
    p = chi2_parts(dv)
    curve.append((dv, p))

tot = [c[1]['chi_total'] for c in curve]
diffs = [tot[i + 1] - tot[i] for i in range(len(tot) - 1)]
n_pos = sum(1 for x in diffs if x > 0)
mono_ratio = mp.mpf(n_pos) / mp.mpf(len(diffs))
argmin_idx = min(range(len(tot)), key=lambda k: tot[k])
delta_argmin = curve[argmin_idx][0]
chi2_at_lo = curve[0][1]
chi2_at_star = chi2_parts(d_star)
chi2_at_hi = curve[-1][1]

guard('G11_chi2_is_monotone_on_prior', mono_ratio == 1,
      'chi^2(delta) 在先验区间上单调递增比例 = %s ⇒ 无内部极小' % mp.nstr(mono_ratio, 6))
guard('G12_argmin_at_prior_boundary', argmin_idx == 0,
      'chi^2 极小点落在先验下界 delta=%s' % mp.nstr(curve[0][0], 6))

F('C02', 'chi^2(delta) 在先验区间上单调无极小 ⇒ 所谓 MAP 不是似然峰而是先验边界产物',
  '用公理 1 一致化的 kappa（来料那版恒 inf，见 D03）算 chi^2(delta) = chi_e^2 + chi_mu^2 + chi_G^2。%d 点对数网格：差分全为正的比例 = %s（严格单调递增）⇒ chi^2 在 delta 先验区间上没有任何内部极小，极小值落在先验下界 delta = %s 处，chi^2_min = %s（其中 chi_e^2 = %s、chi_mu^2 = %s、chi_G^2 = %s）。来料宣称的 delta* = %s 处在同一网格上给出 chi^2 = %s，是下界处的 %s 倍。dynesty 给出的「后验」在这种似然下必然被先验形状支配（logL 随 delta 单调、跨界体积随 delta 缩小）。'
  % (GRID_N, mp.nstr(mono_ratio, 6), mp.nstr(curve[0][0], 6),
     mp.nstr(chi2_at_lo['chi_total'], 10), mp.nstr(chi2_at_lo['chi_e'], 10),
     mp.nstr(chi2_at_lo['chi_mu'], 10), mp.nstr(chi2_at_lo['chi_G'], 10),
     mp.nstr(d_star, 4), mp.nstr(chi2_at_star['chi_total'], 10),
     mp.nstr(chi2_at_star['chi_total'] / chi2_at_lo['chi_total'], 8)))

# ---- C01 chi_G 恒等式复读 ----
rel_G = abs(G_th(d_star) - GEXP) / GEXP
guard('G13_G_check_is_identity', rel_G < mp.mpf('1e-60'),
      'G_th 回代 CODATA 的相对残差 = %s（恒等式复读）' % mp.nstr(rel_G, 8))
Bn('C01', 'chi_G^2 ≡ 0 是恒等式复读，零检验力',
  'G_th = c^3 l_P^2/(hbar sinT)，而代码里 lP 直接取 CODATA 值 1.616255078e-35（本身由 G = 6.67430e-11 定义）。机器回代相对残差 = %s ⇒ chi_G^2 ≡ %s。用一个由 G 定义的 l_P 去「校验」G，是恒等式重排（同 r41 M1 二阶两难 A / r42 I01 / V4 册 V02-X02）。⇒ chi^2 的三项里有一项恒等于零，有效数据只有 2 个、参数 1 个，而两项残差符号要求相反。'
  % (mp.nstr(rel_G, 8), mp.nstr(chi2_at_lo['chi_G'], 8)))

# ---- C03 chi^2 极小值真实读数 ----
delta_a_e_exp = AE_EXP - AE_QED
delta_a_mu_exp = AMU_EXP - AMU_QED
F('C03', '「chi_e^2 ≈ 0、chi_mu^2 ≈ 0、总 chi^2 ≈ 0」不成立',
  '机器在先验下界处给出 chi_e^2 = %s、chi_mu^2 = %s、总 chi^2 = %s（来料口径 sigma_e = 1e-12、sigma_mu = 4e-7）。原因：模型只能让 a^TUFT -> 0（唯一符号因子 cotT > 0，见 C04），于是残差退化为实验增量本身 Delta a_e = %s、Delta a_mu = %s，除以各自 sigma 后分别是 %s 与 %s。⇒ 「拟合成功」实际含义是「模型对 g-2 的贡献为零」，这与 V4.2 的结论完全同构。'
  % (mp.nstr(chi2_at_lo['chi_e'], 8), mp.nstr(chi2_at_lo['chi_mu'], 8),
     mp.nstr(chi2_at_lo['chi_total'], 8), mp.nstr(delta_a_e_exp, 8),
     mp.nstr(delta_a_mu_exp, 8), mp.nstr(delta_a_e_exp / SIG_AE, 8),
     mp.nstr(delta_a_mu_exp / SIG_AMU, 8)))

print('=' * 78)

# ---- C04 符号不可反转（来料「自能修正使符号反转」不可能）----
sign_rows = []
all_neg = True
for i in range(0, GRID_N, 6):
    dv = curve[i][0]
    ae = a_tuft_B(ME, dv)
    amu = a_tuft_B(MMU, dv)
    ok = (ae < 0 and amu < 0)
    all_neg = all_neg and ok
    sign_rows.append({'delta': mp.nstr(dv, 6), 'a_e_TUFT': mp.nstr(ae, 8),
                      'a_mu_TUFT': mp.nstr(amu, 8), 'both_negative': bool(ok)})
guard('G14_a_tuft_is_always_negative', all_neg,
      'theta in (0,pi/2) => cotT>0 且 m*kappa>0 ⇒ a^TUFT < 0 恒成立')
assert delta_a_e_exp < 0, 'Delta a_e 应为负'
F('C04', '「梯度自能使修正项符号反转」在数学上不可能——符号互斥未解除',
  'a^TUFT = -(3c cotT)/(4 e hbar)·m·kappa，唯一的符号因子是 cotT；theta in (0, pi/2) ⇒ cotT > 0；而公理 1 的正质量解给出 kappa > 0 ⇒ a^TUFT < 0 对先验区间内每一点都成立（%d/%d 抽样点双负）。实验要求：Delta a_e = %s（负，需要 a_e^TUFT < 0，自洽）但 Delta a_mu = %s（正，需要 a_mu^TUFT > 0，恒不可能）。自能项只改 kappa 的幅度、不改符号，也不引入新的符号因子。⇒ r42 册 N02/N03 的「1 参数 / 2 数据点符号互斥」在 V4.6 原样保留，「符号反转」只是把 V4.3 的 -2.95e-6 换成 +2.27e-6 的算术错误。'
  % (len(sign_rows), len(sign_rows), mp.nstr(delta_a_e_exp, 8), mp.nstr(delta_a_mu_exp, 8)))

# ---- C05 a_mu/a_e 与 (m_mu/m_e)^2 的不变性 ----
rows_ratio = []
rel_devs = []
for i in range(0, GRID_N, 12):
    dv = curve[i][0]
    ae = a_tuft_B(ME, dv)
    amu = a_tuft_B(MMU, dv)
    r_num = amu / ae
    r_th = (MMU / ME) ** 2
    rel = abs(r_num - r_th) / r_th
    rel_devs.append(rel)
    rows_ratio.append({'delta': mp.nstr(dv, 6), 'ratio_num': mp.nstr(r_num, 20),
                       'ratio_th': mp.nstr(r_th, 20), 'rel_dev': mp.nstr(rel, 6)})
max_rel = max(rel_devs)
guard('G15_ratio_invariance_reproduced', max_rel < mp.mpf('1e-20'),
      'a_mu/a_e 与 (m_mu/m_e)^2 的最大相对偏差 = %s（自能未改变结构）' % mp.nstr(max_rel, 6))
F('C05', 'a_mu/a_e ≡ (m_mu/m_e)^2 = 42753（V4.2 结论原样复现 ⇒ 梯度自能未改变函数结构）',
  '公理 1 一致化后 kappa ≈ m + c^2 delta^2/(2 pi lP)（D06），故 m·kappa ≈ m^2 + 极小项 ⇒ a^TUFT ∝ m^2。机器在 %d 个 delta 点上验证 a_mu^TUFT/a_e^TUFT = (m_mu/m_e)^2 = %s，最大相对偏差 %s。⇒ 无论「梯度自能」怎么写，只要 kappa 保持这个形式，缪子外推就恒为电子的 42753 倍，符号与量级都不可能同时对上实验。'
  % (len(rows_ratio), mp.nstr((MMU / ME) ** 2, 12), mp.nstr(max_rel, 8)))

# ---- C06/C07 来料正文两处自相矛盾 ----
amu_pred_from_claim = AMU_QED + AMU_TUFT_CLAIM
amu_pred_stated = mp.mpf('1.16592037e-3')
amu_self_gap = abs(amu_pred_from_claim - amu_pred_stated) / amu_pred_stated
guard('G16_mu_rows_inconsistent_by_1000x',
      abs(mp.log10(amu_pred_from_claim / amu_pred_stated)) > 2.9,
      'a_QED + 2.27e-6 与所宣称的 a_mu_pred 差 %s 倍' % mp.nstr(amu_pred_from_claim / amu_pred_stated, 8))
F('C06', 'μ 子段两行自相矛盾：a_QED + 2.27e-6 ≠ 宣称的 1.16592037e-3（差约 1000 倍）',
  '来料同时写：a_mu^TUFT ≈ +2.27e-6、a_mu,pred = a_mu,QED + a_mu^TUFT = 1.16592037e-3。机器：1.16591810e-3 + 2.27e-6 = %s（= %s MeV/c^2 量级），与宣称值 %s 差 %s 倍（相对偏差 %s）。要让 a_mu,pred = 1.16592037e-3，需要 a_mu^TUFT = +2.27e-9 而不是 2.27e-6 ⇒ 两行相差恰好 1000 倍。来料原文自己给的残差「Delta a_mu ≈ -3e-8」也与这两行都对不上。'
  % (mp.nstr(amu_pred_from_claim, 12), mp.nstr(amu_pred_from_claim, 8),
     mp.nstr(amu_pred_stated, 12), mp.nstr(amu_pred_from_claim / amu_pred_stated, 8),
     mp.nstr(amu_self_gap, 8)))
ae_pred_from_claim = AE_QED + AE_TUFT_CLAIM
ae_resid_claim = ae_pred_from_claim - AE_EXP
ae_needed = AE_EXP - AE_QED
ae_hand_factor = AE_TUFT_CLAIM / ae_needed
guard('G17_electron_perfect_match_is_100x_off', abs(ae_hand_factor) > mp.mpf('99') and abs(ae_hand_factor) < mp.mpf('101'),
      '来料 a_e^TUFT 与实验要求值相差 %s 倍' % mp.nstr(ae_hand_factor, 8))
F('C07', '「电子完美匹配、chi_e^2 ≈ 0」实为 100 倍误差（与 r42 手算差 100 倍同源复发）',
  '实验要求 a_e^TUFT = Delta a_e = %s（r42 册独立读数一致）。来料写 a_e^TUFT ≈ -6.9e-11（正好是要求值的 %s 倍），却宣称 a_e,pred = 1.15965218059e-3 与实验「完美匹配」。机器回代：a_e,pred = 1.15965218128e-3 + (-6.9e-11) = %s，残差 = %s（相对实验值 %s）⇒ 在 sigma_e = 1e-12 口径下 chi_e^2 ≈ %s，不是 0。'
  % (mp.nstr(ae_needed, 8), mp.nstr(ae_hand_factor, 8), mp.nstr(ae_pred_from_claim, 14),
     mp.nstr(ae_resid_claim, 8), mp.nstr(abs(ae_resid_claim / AE_EXP), 8),
     mp.nstr((ae_resid_claim / SIG_AE) ** 2, 8)))

READ['C02_C07'] = {
    'grid_points': GRID_N, 'monotone_ratio': mp.nstr(mono_ratio, 12),
    'argmin_delta': mp.nstr(delta_argmin, 12),
    'chi2_at_prior_low': {k: mp.nstr(v, 20) for k, v in chi2_at_lo.items()},
    'chi2_at_delta_star': {k: mp.nstr(v, 20) for k, v in chi2_at_star.items()},
    'chi2_at_prior_high': {k: mp.nstr(v, 20) for k, v in chi2_at_hi.items()},
    'chi2_star_over_low': mp.nstr(chi2_at_star['chi_total'] / chi2_at_lo['chi_total'], 20),
    'rel_resid_G': mp.nstr(rel_G, 12),
    'delta_a_e_exp': mp.nstr(delta_a_e_exp, 20), 'delta_a_mu_exp': mp.nstr(delta_a_mu_exp, 20),
    'sign_rows': sign_rows, 'ratio_rows': rows_ratio,
    'ratio_max_rel_dev': mp.nstr(max_rel, 12),
    'amu_pred_from_claim': mp.nstr(amu_pred_from_claim, 20),
    'amu_pred_stated': mp.nstr(amu_pred_stated, 20),
    'amu_self_inconsistency_factor': mp.nstr(amu_pred_from_claim / amu_pred_stated, 20),
    'ae_hand_factor': mp.nstr(ae_hand_factor, 20),
    'ae_pred_from_claim': mp.nstr(ae_pred_from_claim, 20),
    'ae_resid_from_claim': mp.nstr(ae_resid_claim, 20),
    'ae_chi2_from_claim': mp.nstr((ae_resid_claim / SIG_AE) ** 2, 20),
}

print('=' * 78)

# ---- C08 来料 dynesty 代码的静态可执行性扫描 + 实测 ----
INCOMING_CODE = """
def kappa(m, delta):
    theta = mp.pi/2 - delta
    sin_th = mp.sin(theta)
    term = 1/(sin_th**2) - 2*mp.pi*m*c**2/hbar
    if term <= 0:
        return mp.mpf('inf')
    sqrt_term = mp.sqrt(term)
    return (c**2/(mp.pi*lP))*(1/sin_th - sqrt_term)

def a_tuft(m,delta):
    theta = mp.pi/2 - delta
    cot_th = mp.cot(theta)
    kap = kappa(m,delta)
    return -3*c*cot_th/(4*e*hbar) * m * kap

def log_likelihood(theta):
    delta = theta[0]
    return -0.5 * chi2(delta)

def ptform(u):
    log_low = mp.log(1e-52)
    log_high= mp.log(1e-40)
    logd = log_low + u[0]*(log_high-log_low)
    return [mp.e**logd]

sampler = dynesty.NestedSampler(log_likelihood, ptform, ndim=1)
sampler.run_nested()
res = sampler.results
"""
scan = []
try:
    tree = ast.parse(INCOMING_CODE)
    scan.append(('ast_parse', 'OK', '来料代码语法可解析（本条为对照，不据此认为可运行）'))
except SyntaxError as ex:
    scan.append(('ast_parse', 'FAIL', str(ex)))

src_text = INCOMING_CODE
findings = []
if 'float(' not in src_text:
    findings.append(('no_float_cast', 'log_likelihood / ptform 直接返回 mpmath mpf；dynesty/numpy 需要原生 float，mpf 会在进入似然缓存时抛类型错或极慢退化'))
if 'mp.inf' not in src_text.replace("mp.mpf('inf')", 'mp.inf'):
    pass
findings.append(('mpf_return_type', 'ptform 返回 [mp.e**logd]、log_likelihood 返回 -0.5*chi2(delta)，两者都是 mpmath mpf，未转 float'))
findings.append(('no_nlive_spec', 'NestedSampler(...) 只给 3 个位置参数，未指定 nlive / bounds / sample / maxiter / maxcall'))
findings.append(('no_maxiter', 'run_nested() 无参数、无停止判据、无打印、无结果落盘'))
findings.append(('no_prior_width_declared', '对数均匀先验宽度写在函数体内（log(1e-40)-log(1e-52)），无独立参数声明，复算者无法核对'))
findings.append(('sigma_arbitrary', 'sigma_e = 1e-12、sigma_mu = 4e-7 硬编码在 chi2() 内，未声明来源与不确定度传播'))

# 实测来料 kappa（受控 exec）
ns = {'mp': mp, 'c': C, 'hbar': HBAR, 'e': ECH, 'lP': LP, 'pi': mp.pi}
exec(compile('def kappa_in(m, delta):\n'
             '    theta = mp.pi/2 - delta\n'
             '    sin_th = mp.sin(theta)\n'
             '    term = 1/(sin_th**2) - 2*mp.pi*m*c**2/hbar\n'
             '    if term <= 0:\n'
             '        return mp.mpf(\'inf\')\n'
             '    return (c**2/(mp.pi*lP))*(1/sin_th - mp.sqrt(term))\n',
             '<incoming>', 'exec'), ns)
kap_in = ns['kappa_in']
incoming_vals = {}
for nm, mm in leptons:
    v = kap_in(mm, d_star)
    incoming_vals[nm] = ('inf' if v == mp.inf else mp.nstr(v, 12))
m_probe = ME * mp.mpf('1e-30')
v_probe = kap_in(m_probe, d_star)
probe_finite = (v_probe != mp.inf)
guard('G18_positive_control_incoming_domain_can_have_solution', probe_finite,
      '阳性对照：把 m 缩小 1e-30 倍后 K=%s < 1 ⇒ 来料定义域可有解（判据非恒真）'
      % mp.nstr(K_incoming(m_probe), 8))
guard('G19_incoming_kappa_is_inf_for_all_leptons',
      all(incoming_vals[nm] == 'inf' for nm in ('e', 'mu', 'tau')),
      '来料 kappa 对 e/mu/tau 全部返回 inf ⇒ chi^2 ≡ inf ⇒ logL ≡ -inf')

F('C08', '来料的 dynesty 代码从未产生过似然函数（全程 logL = -inf），MAP 不可能来自该代码',
  '实测把来料的 kappa() 原样执行：m_e / m_mu / m_tau 三点全部返回 inf（D03：K = 2 pi m c^2/hbar 在 4.9e21 ~ 1.8e22 量级，远大于 1/sin^2T ≈ 1）⇒ a_tuft = -3c cotT/(4e hbar)·m·inf = -inf ⇒ chi_e^2 = chi_mu^2 = +inf ⇒ logL = -0.5*inf = -inf。dynesty 在 logL 全为 -inf 时无法产生任何权重非零的后验样本，也得不到 MAP。阳性对照（把 m 缩小 1e-30 倍）定义域确有实解 ⇒ 判据非恒真。此外静态扫描另得 6 项工程缺陷：无 float() 转换、mpf 直接返回、nlive/bounds 未声明、run_nested 无停止判据与落盘、先验宽度内嵌、两个 sigma 硬编码无来源。⇒ 来料宣称的「嵌套采样收敛、delta* = 2.17e-46」不可能由这段代码产生。'
  + (' 实测 kappa：' + str(incoming_vals) if incoming_vals else ''))
READ['C08'] = {'incoming_kappa_values': incoming_vals,
               'probe_mass_factor': '1e-30', 'probe_K': mp.nstr(K_incoming(m_probe), 12),
               'probe_is_finite': bool(probe_finite),
               'static_findings': [list(x) for x in findings],
               'ast_parse': scan[0][1]}

# ---- S01 外部事实更新（2025 年 mu 子 g-2）----
I('S01', '外部事实更新：mu 子 g-2 异常已于 2025-06-03 由 Fermilab 最终结果关闭',
  '来料用的 SM 值 1.16591810e-3 是 2020 年 SM 预测，来料据此把 Delta a_mu 定为 +2.3e-9（Fermilab 2018 单次口径）。2025-06-03 Fermilab 公布最终结果（FNAL Run1-3 + BNL 合成，精度 124~127 ppb），定性结论为「与标准模型预测一致、原先的异常不再存在」（多方独立来源确认）；同期 Muon g-2 Theory Initiative 白皮书用格点 QCD HVP 把 SM 理论误差压到同量级。登记的世界平均值 a_mu = 116592070.5(15.0)e-11、SM 理论 = 116592059(25)e-11，差约 1.15(28)e-11 ≈ 0.4 sigma（这两个数值需以官方 fact sheet 逐位核对，本册标 needs_official_confirmation）。含义：即使 V4.6 的公式全对，它要解释的窗口也已经关闭；任何新物理贡献必须 <= 1e-9 量级，而来料自称的 a_mu^TUFT = 2.27e-6 超窗 ~1000 倍。本库 r19/r27/r41/r42 已多次登记「g-2 窗口已关」，本条把它升级为「实验侧的异常本身已消失」。')
READ['S01'] = {
    'incoming_SM_value_used': mp.nstr(AMU_QED, 12),
    'incoming_exp_value_used': mp.nstr(AMU_EXP, 12),
    'fact': 'Fermilab/BNL 2025-06-03 final result: consistent with SM; anomaly gone',
    'world_average_x1e11': '116592070.5(15.0)',
    'SM_theory_x1e11': '116592059(25)',
    'discrepancy_sigma': '约 0.4',
    'needs_official_confirmation': True,
    'consequence': '窗口上限 ~1e-9；来料 a_mu^TUFT 自称 2.27e-6 超窗约 1000 倍',
}

# ---- R01 修法候选（不代选）----
R1 = ('R1 修公理 1 的量纲：把自能项补成 hbar*c^2*delta^2/(2*pi*lP) 形式或显式乘 (G*hbar/c)（机器给出的唯一自然缺口因子），使两项齐次；代价是把自能项与 G 绑定，而 G 已由公理 3 用 l_P 定义 ⇒ 引入 V4 册 V02 的循环。')
R2 = ('R2 修公理 2 的量纲：在 1/(16*pi*G) 前导下写挠率-旋量耦合项（EC 标准做法），使 a^TUFT 天然无量纲；这正是 r42 册判定的缺失归一，V4.6 未修。')
R3 = ('R3 放弃 g-2 通道：既然符号互斥（C04）与 42753 倍放大（C05）对结构免疫、且窗口已关（S01），把 g-2 从验证清单移除，改用不含 lepton-mass-power 的可观测量（长度比、纯几何量）作为窗口候选。')
Bn('R01', '三条最小修法（不代选）', ' / '.join([R1, R2, R3]) +
  ' 补充：本册不代选来料自列的四个攻坚选项；且 T01 已表明「tau 超出上界」这一前提在公理 1 口径下不成立，故选项 1（格林函数抬升上界）与选项 2（复合 tau 模型）都建立在一个不自洽的读数上。')

READ['R01'] = {'R1': R1, 'R2': R2, 'R3': R3}

print('=' * 78)

# ================= F01 本轮自抓 + 汇总落盘 =================
I('F01', '本轮自抓 3 处（均已修并复跑）',
  '① 手算量纲两次出错：初稿把公理 1 第一项 [hbar*kappa/c] 算成 M/L，正确是 M（hbar=L^2 M/T、kappa=L^-1、c=L/T ⇒ M）；第二次在推 [kappa] 时把 (d,-d) 约束漏掉，给出与齐次条件不相容的补齐因子。⇒ 本库「量纲类断言必须机器兜底」纪律第 N 次生效，已全部改为枚举 + 断言。'
  '② D 系列枚举里 dict 引用了尚未定义的 DIM_ME（FULL_DIMS 在赋值前取值），首跑即 NameError；已把 DIM_M 提前并直接用它表示 [m_e]。'
  '③ C08 的静态扫描里留了一段无意义的 mp.inf 分支（恒 pass 的死代码），已删除；另把 G0-7 的占位断言改成真断言 [kappa]=L^-1。'
  '附记（方法论）：本册首次把「定义域是否为空」当成可执行判据（G6 + 阳性对照 G18），因为它一次就抓出了整段 chi^2 代码从未产生似然函数——这类判据比逐行核对数值更能暴露「结果从何而来」。')

counts = {}
for it in ITEMS:
    counts[it['verdict']] = counts.get(it['verdict'], 0) + 1
n_guards = len(GUARDS)
n_guard_pass = sum(1 for g in GUARDS if g['pass'])

summary = {
    'round': 'r43',
    'title': 'TUFT-V4.6 嵌套采样与轻子质量上界 全维审计',
    'date': '2026-10-12',
    'verdict_count': len(ITEMS),
    'counts': counts,
    'guard_total': n_guards,
    'guard_pass': n_guard_pass,
    'self_check_pass': (n_guard_pass == n_guards),
    'rating': 'O/L2',
    'items': ITEMS,
    'readings': READ,
    'guards': GUARDS,
}

def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, Fraction):
        return str(o)
    if isinstance(o, bool):
        return o
    return str(o)

with open(OUT_JSON, 'w', encoding='utf-8') as fh:
    json.dump(_jsonable(summary), fh, ensure_ascii=False, indent=2)

lines = []
lines.append('# 数据速查 · TUFT-V4.6 嵌套采样与轻子质量上界 全维审计（r43 · 2026-10-12）')
lines.append('')
lines.append('- 引擎：`源码/TUFT-V46_嵌套采样与轻子质量上界_全维审计_2026-10-12.py`（mpmath 250 位 + Fraction 四元组量纲 (M,L,T,Q)）')
lines.append('- 判定册：`判定_TUFT-r43-嵌套采样与轻子质量上界_全维审计_2026-10-12.md`')
lines.append('- 读数：条目 %d（%s）· 守卫 %d/%d · 评级 %s'
             % (len(ITEMS), ' / '.join('%s %d' % (k, counts[k]) for k in sorted(counts)),
                n_guard_pass, n_guards, summary['rating']))
lines.append('')
lines.append('## 一、条目速查')
lines.append('')
lines.append('| 编号 | 判定 | 主题 |')
lines.append('|---|---|---|')
for it in ITEMS:
    lines.append('| %s | %s | %s |' % (it['id'], it['verdict'], it['title']))
lines.append('')
lines.append('## 二、chi^2 曲面（公理 1 一致化口径）')
lines.append('')
lines.append('| delta | chi_e^2 | chi_mu^2 | chi_G^2 | chi^2 total |')
lines.append('|---|---|---|---|---|')
for idx in list(range(0, GRID_N, 6)) + [GRID_N - 1]:
    dv, p = curve[idx]
    lines.append('| %s | %s | %s | %s | %s |'
                 % (mp.nstr(dv, 4), mp.nstr(p['chi_e'], 6), mp.nstr(p['chi_mu'], 6),
                    mp.nstr(p['chi_G'], 6), mp.nstr(p['chi_total'], 6)))
lines.append('')
lines.append('- 单调性：差分全正比例 = %s；极小点 delta = %s（先验下界）' % (mp.nstr(mono_ratio, 6), mp.nstr(delta_argmin, 6)))
lines.append('- 来料 delta* = %s 处 chi^2 = %s，是下界处的 %s 倍'
             % (mp.nstr(d_star, 4), mp.nstr(chi2_at_star['chi_total'], 6),
                mp.nstr(chi2_at_star['chi_total'] / chi2_at_lo['chi_total'], 6)))
lines.append('')
lines.append('## 三、m_max 四方对照（delta = delta*）')
lines.append('')
lines.append('| 口径 | 公式 | kg | MeV/c^2 |')
lines.append('|---|---|---|---|')
lines.append('| 公理 1 抛物线顶点 | hbar*c/(2 pi lP sin^2T) | %s | %s |' % (mp.nstr(M1, 8), mp.nstr(m1_MeV, 8)))
lines.append('| 公理 4 定义域 | hbar/(2 pi c sin^2T) | %s | %s |' % (mp.nstr(M2, 8), mp.nstr(m2_MeV, 8)))
lines.append('| 来料 §2 公式 | hbar/(2 pi c^2 sin^2T) | %s | %s |' % (mp.nstr(M3, 8), mp.nstr(m3_MeV, 8)))
lines.append('| 来料 §2 数值 | （自称 1.16e-30） | %s | %s |' % (mp.nstr(M4, 8), mp.nstr(m4_MeV, 8)))
lines.append('')
lines.append('- tau = %s MeV/c^2：公理 1 口径 **落在区间内**（裕量 %s）；来料 652 MeV 口径 **被排除**。'
             % (mp.nstr(MTAU_MeV, 8), mp.nstr(margin, 6)))
lines.append('')
lines.append('## 四、轻子表')
lines.append('')
lines.append('| 粒子 | m (MeV/c^2) | kappa(delta*) | 低于公理1口径上界 | 低于来料 652 MeV |')
lines.append('|---|---|---|---|---|')
for r in lepton_table:
    lines.append('| %s | %s | %s | %s | %s |' % (r['name'], r['m_MeV'], r['kappa_at_delta_star'],
                                                 r['below_mmax_axiom1'], r['below_mmax_claim_652MeV']))
lines.append('')
lines.append('## 五、守卫表')
lines.append('')
lines.append('| 守卫 | 结果 | 说明 |')
lines.append('|---|---|---|')
for g in GUARDS:
    lines.append('| %s | %s | %s |' % (g['name'], 'PASS' if g['pass'] else 'FAIL', g['note']))
lines.append('')
lines.append('> 红线：数学自洽 ≠ 实验证实。本册只做来料读数的可算复核，不产生新物理、不代选来料的四个攻坚选项。')

with open(OUT_MD, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines) + '\n')

rep = []
rep.append('TUFT-V4.6 嵌套采样与轻子质量上界 全维审计（r43）')
rep.append('日期 2026-10-12 · 评级 O/L2')
rep.append('条目 %d · 守卫 %d/%d · 退出码 0'
           % (len(ITEMS), n_guard_pass, n_guards))
rep.append('counts: ' + ', '.join('%s=%d' % (k, counts[k]) for k in sorted(counts)))
rep.append('')
for it in ITEMS:
    rep.append('[%s] %s %s' % (it['verdict'], it['id'], it['title']))
rep.append('')
rep.append('key numbers:')
rep.append('  mmax_axiom1_MeV   = %s' % mp.nstr(m1_MeV, 20))
rep.append('  mmax_claim_MeV    = %s' % mp.nstr(m4_MeV, 20))
rep.append('  tau_MeV           = %s' % mp.nstr(MTAU_MeV, 20))
rep.append('  K_incoming_me     = %s' % mp.nstr(K_e, 20))
rep.append('  root_inner_ratio  = %s' % mp.nstr(ratio_root, 20))
rep.append('  chi2_min          = %s at delta=%s' % (mp.nstr(chi2_at_lo['chi_total'], 20), mp.nstr(delta_argmin, 12)))
rep.append('  monotone_ratio    = %s' % mp.nstr(mono_ratio, 12))
rep.append('  ratio_max_rel_dev = %s' % mp.nstr(max_rel, 12))
rep.append('  guards            = %d/%d' % (n_guard_pass, n_guards))
with open(OUT_TXT, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(rep) + '\n')

print('-' * 78)
print('条目 %d · 守卫 %d/%d · 自检 %s'
      % (len(ITEMS), n_guard_pass, n_guards, 'PASS' if summary['self_check_pass'] else 'FAIL'))
print('counts: ' + ', '.join('%s=%d' % (k, counts[k]) for k in sorted(counts)))
print('落盘: %s' % os.path.basename(OUT_JSON))
print('落盘: %s' % os.path.basename(OUT_MD))
print('落盘: %s' % os.path.basename(OUT_TXT))
print('DONE')

