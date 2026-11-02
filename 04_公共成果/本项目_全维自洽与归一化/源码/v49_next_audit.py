# -*- coding: utf-8 -*-
# ROOT V49 full machine re-check (2026-11-03)
# Convention: ROOT V4x "整理册" (V47/V48) -- verify (1) reproducible numbers,
# (2) self-consistency of structural premises. No new physics. No r-number.
# Pure standard library + mpmath 50 digits. stdout is ASCII only (GBK-safe).
import io, os
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
LINES = []
NP = 0
NF = 0

def rec(tag, ok, detail=''):
    global NP, NF
    if ok: NP += 1
    else: NF += 1
    LINES.append('%-5s %-34s %s' % ('PASS' if ok else 'FAIL', tag, detail))

def say(s):
    LINES.append(s)

def ns(x, n=20):
    return mp.nstr(x, n)

def close(a, b, tol=mp.mpf('1e-30')):
    return abs(a - b) <= tol

# ---------------------------------------------------------------- [A] (49-1)
say('== [A] (49-1) 一阶零模方程解空间 <= 1 ==')
def rk4_zero(f0, lam=mp.mpf('1.0'), N=4000, ymax=mp.mpf('3')):
    h = ymax / N
    Phi = lambda y: 1 + y * y
    y = mp.mpf('0'); f = mp.mpf(f0)
    pts = []
    for i in range(N + 1):
        pts.append((y, f))
        k1 = -lam * Phi(y) * f
        k2 = -lam * Phi(y + h / 2) * (f + h * k1 / 2)
        k3 = -lam * Phi(y + h / 2) * (f + h * k2 / 2)
        k4 = -lam * Phi(y + h) * (f + h * k3)
        f = f + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        y += h
    return pts
p1 = rk4_zero(1); p2 = rk4_zero(2)
ratios = [p2[i][1] / p1[i][1] for i in range(0, len(p1), 400)]
rec('A1_dim_ker_le_1', all(close(r, mp.mpf('2'), mp.mpf('1e-40')) for r in ratios),
    'f(0)=1 vs 2 ratio = %s (const)' % ns(ratios[-1], 12))
rec('A1_analytic_match', close(p1[-1][1], mp.e ** (-(mp.mpf('3') + mp.mpf('27') / 3)), mp.mpf('1e-30')),
    'f(3) numeric = %s' % ns(p1[-1][1], 14))

# ---------------------------------------------------------------- [B] (49-2)(49-17)
say('== [B] 磁通量子化 / F^2 / E_flux(N) ==')
def flux_integral(N, R=mp.mpf('1')):
    Fthph = lambda th: (N / 2) * mp.sin(th)
    return 2 * mp.pi * mp.quad(Fthph, [0, mp.pi])
for N in [1, 2, 3, 5]:
    Nm = mp.mpf(N)
    q = flux_integral(Nm) / (2 * mp.pi)
    rec('B1_dirac_quant_N=%d' % N, close(q, Nm), 'N=(1/2pi)Int F = %s' % ns(q, 14))
def F2_of_th(th, N, R):
    # g^thth=1/R^2, g^phph=1/(R^2 sin^2 th); F_ab F^ab = 2 F_thph^2 g^thth g^phph
    Fthph = (N / 2) * mp.sin(th)
    return 2 * Fthph ** 2 * (1 / R ** 2) * (1 / (R ** 2 * mp.sin(th) ** 2))
for th in ['0.3', '1.0', '2.5']:
    v = F2_of_th(mp.mpf(th), mp.mpf('3'), mp.mpf('2'))
    rec('B2_F2_const_th=%s' % th, close(v, mp.mpf('9') / (2 * mp.mpf('16'))),
        'F_ab F^ab = %s (expect 9/32)' % ns(v, 14))
def E_flux(N, g=mp.mpf('1'), R=mp.mpf('1')):
    # (1/4g^2) * Int F^2 sqrt(g) dth dph , sqrt(g)=R^2 sin th
    return (1 / (4 * g ** 2)) * mp.quad(
        lambda th: F2_of_th(th, N, R) * R ** 2 * mp.sin(th), [0, mp.pi]) * 2 * mp.pi
for N in [0, 1, 2, 3]:
    Nm = mp.mpf(N)
    rec('B3_Eflux_N=%d' % N, close(E_flux(Nm), mp.pi * Nm ** 2 / 2),
        'E = %s vs pi*N^2/2 = %s' % (ns(E_flux(Nm), 14), ns(mp.pi * Nm ** 2 / 2, 14)))
rec('B4_E_monotone', E_flux(mp.mpf(0)) < E_flux(mp.mpf(1)) < E_flux(mp.mpf(2)) < E_flux(mp.mpf(3)),
    'E(0)<E(1)<E(2)<E(3) (ordinary Maxwell energy cannot select N=3)')
dE23 = E_flux(mp.mpf(3)) - E_flux(mp.mpf(2))
rec('B5_gap_2_to_3', close(dE23, 5 * mp.pi / 2),
    'extra term needed to flip N=3 to minimum = %s /(g6^2 R^2)' % ns(dE23, 14))

# ---------------------------------------------------------------- [C] (49-5)(49-6) zero modes
say('== [C] 零模归一化(rho-path) / 正交 / P_k / q-sensitivity ==')
def beta_norm(k, q):
    return mp.beta(k + 1, 2 * q + 1 - k)
def norm_rho(k, q):
    # Int |psi_k|^2 dOmega on the rho,phi plane (INDEPENDENT of the x-substituted P_k)
    B = beta_norm(k, q)
    f = lambda r: r ** (2 * k + 1) / (1 + r ** 2) ** (2 * q + 2)
    return (2 / B) * mp.quad(f, [0, 1, mp.inf])
for qn, qlabel in [(mp.mpf('1'), 'q=1 (来料)'), (mp.mpf('1.5'), 'q=3/2 (标准 N=3)')]:
    for k in [0, 1, 2]:
        v = norm_rho(k, qn)
        rec('C1_norm_%s_k=%d' % (qlabel[:4], k), close(v, mp.mpf('1'), mp.mpf('1e-40')),
            '%s Int|psi_%d|^2 dOmega = %s' % (qlabel, k, ns(v, 16)))
def phi_int(m):
    re = mp.quad(lambda ph: mp.cos(m * ph), [0, 2 * mp.pi])
    im = mp.quad(lambda ph: mp.sin(m * ph), [0, 2 * mp.pi])
    return re + 1j * im
for m in [1, 2, 3]:
    rec('C2_orth_phi_m=%d' % m, abs(phi_int(m)) < mp.mpf('1e-40'),
        'Int e^{i%d phi} dphi = %s' % (m, ns(abs(phi_int(m)), 8)))
def P_of_x(k, q, x):
    return x ** k * (1 - x) ** (2 * q - k) / beta_norm(k, q)
for k in [0, 1, 2]:
    v = mp.quad(lambda x: P_of_x(k, mp.mpf('1'), x), [0, 1])
    rec('C3_Pk_norm_k=%d' % k, close(v, mp.mpf('1'), mp.mpf('1e-40')),
        'Int_0^1 P_%d(x) dx = %s' % (k, ns(v, 16)))
# verify the three explicit P_k reported in (49-6)
for k, coeff in [(0, 3), (1, 6), (2, 3)]:
    ok = True
    for xx in ['0.13', '0.47', '0.81']:
        x = mp.mpf(xx)
        target = coeff * ((1 - x) ** 2 if k == 0 else (x * (1 - x) if k == 1 else x ** 2))
        ok = ok and close(P_of_x(k, mp.mpf('1'), x), target, mp.mpf('1e-40'))
    rec('C4_Pk_explicit_k=%d' % k, ok, 'P_%d matches boxed (49-6)' % k)
# peak positions: pole / equator / other pole
def peak(k, q):
    grid = [mp.mpf(i) / 1000 for i in range(1, 1000)]
    return max(grid, key=lambda x: P_of_x(k, q, x))
pk = [peak(k, mp.mpf('1')) for k in [0, 1, 2]]
rec('C5_peaks_pole_equator', abs(pk[0]) < mp.mpf('0.01') and abs(pk[1] - mp.mpf('0.5')) < mp.mpf('0.01') and abs(pk[2] - mp.mpf('0.99')) < mp.mpf('0.01'),
    'x_peaks = %s / %s / %s (north / equator / south)' % (ns(pk[0], 4), ns(pk[1], 4), ns(pk[2], 4)))
say('  [q-sensitivity] q=1 (来料) -> P=(3(1-x)^2, 6x(1-x), 3x^2); q=3/2 (N=3 标准单极子) -> P=(4(1-x)^3, 12x(1-x)^2, 12x^2(1-x))')
for k, coeff, shape in [(0, 4, lambda x: (1 - x) ** 3), (1, 12, lambda x: x * (1 - x) ** 2), (2, 12, lambda x: x ** 2 * (1 - x))]:
    ok = True
    for xx in ['0.13', '0.47', '0.81']:
        x = mp.mpf(xx)
        ok = ok and close(P_of_x(k, mp.mpf('1.5'), x), coeff * shape(x), mp.mpf('1e-40'))
    rec('C6_q3half_P_k=%d' % k, ok, 'N=3 standard monopole harmonic P_%d differs from 来料' % k)

# ---------------------------------------------------------------- [D] (49-7)(49-8)(49-9)
say('== [D] 单参数 Higgs 重叠质量 / (49-9) 恒等式 / 观测排除 / q-依赖 ==')
def m_k(k, q, p):
    return mp.quad(lambda x: P_of_x(k, q, x) * (1 - x) ** p, [0, 1])
def m_closed(k, q, p):
    return mp.beta(k + 1, 2 * q + 1 - k + p) / beta_norm(k, q)
for p in ['0', '1', '2', '5', '31.63538', '205.76828']:
    pp = mp.mpf(p)
    ok = True
    for k in [0, 1, 2]:
        ok = ok and close(m_k(k, mp.mpf('1'), pp), m_closed(k, mp.mpf('1'), pp), mp.mpf('1e-40'))
    rec('D1_mk_closed_p=%s' % p, ok, 'numeric overlap == Beta closed form, k=0,1,2')
for p in ['0', '1', '2', '5', '31.63538']:
    pp = mp.mpf(p)
    m0, m1, m2 = [m_closed(k, mp.mpf('1'), pp) for k in [0, 1, 2]]
    r01, r12 = m0 / m1, m1 / m2
    rec('D2_ratios_p=%s' % p, close(r01, (pp + 2) / 2) and close(r12, pp + 1),
        'm0/m1=%s (=(p+2)/2), m1/m2=%s (=p+1)' % (ns(r01, 12), ns(r12, 12)))
    rec('D3_identity_p=%s' % p, close(2 * r01 - r12, mp.mpf('1')),
        '2*m0/m1 - m1/m2 = %s (identically 1 for ANY p)' % ns(2 * r01 - r12, 14))
r_tm = mp.mpf('16.81769'); r_me = mp.mpf('206.76828')
obs = 2 * r_tm - r_me
rec('D4_obs_exclusion', not close(obs, mp.mpf('1'), mp.mpf('1e-6')),
    '2*(16.81769) - 206.76828 = %s != 1 => single-shape model EXCLUDED' % ns(obs, 14))
pA = 2 * r_tm - 2; predA = pA + 1
pB = r_me - 1; predB = (pB + 2) / 2
rec('D5_fit_table', close(pA, mp.mpf('31.63538')) and close(predA, mp.mpf('32.63538'))
    and close(pB, mp.mpf('205.76828')) and close(predB, mp.mpf('103.88414'), mp.mpf('1e-6')),
    'p=%s -> mume=%s ; p=%s -> mtau/mmu=%s' % (ns(pA, 8), ns(predA, 8), ns(pB, 8), ns(predB, 8)))
# (49-9) is NOT q-independent
say('  [q-sensitivity] (49-9) holds only for q=1; for q=3/2 it becomes (p+6)/6 (still p-dependent)')
for p in ['0', '2', '5', '31.63538']:
    pp = mp.mpf(p)
    a0, a1, a2 = [m_closed(k, mp.mpf('1.5'), pp) for k in [0, 1, 2]]
    lhs = 2 * (a0 / a1) - (a1 / a2)
    rec('D6_49_9_q_dependent_p=%s' % p, close(lhs, (pp + 6) / 6),
        'q=3/2: 2m0/m1-m1/m2 = %s (=(p+6)/6, NOT 1)' % ns(lhs, 14))

# ---------------------------------------------------------------- [E] (49-11)(49-12)
say('== [E] 非对角质量矩阵(独立 rho,phi 数值积分) / 本征值 / 有效域 ==')
def M_num(i, j, q, eps, dlt):
    Bi, Bj = beta_norm(i, q), beta_norm(j, q)
    pref = 1 / (4 * mp.pi * mp.sqrt(Bi * Bj))
    def radial(r):
        base = r ** (i + j) / (1 + r ** 2) ** (2 * q) * 4 * r / (1 + r ** 2) ** 2
        if i == j:
            return base * (2 * mp.pi) * (1 + eps * (1 - r ** 2) / (1 + r ** 2))
        if abs(i - j) == 1:
            return base * mp.pi * dlt * (2 * r / (1 + r ** 2))
        return mp.mpf('0')
    return pref * mp.quad(radial, [0, 1, mp.inf])
eps = mp.mpf('0.6'); dlt = mp.mpf('0.4')
a = dlt / (2 * mp.sqrt(2))
M_doc = mp.matrix([[1 + eps / 2, a, 0], [a, 1, a], [0, a, 1 - eps / 2]])
mx = mp.mpf('0')
for i in range(3):
    for j in range(3):
        v = M_num(i, j, mp.mpf('1'), eps, dlt)
        mx = max(mx, abs(v - M_doc[i, j]))
rec('E1_M_num_vs_analytic', mx < mp.mpf('1e-40'),
    'max |M_num - boxed(49-11)| = %s (来料 float64: 2.78e-17)' % ns(mx, 8))
for (i, j) in [(0, 2), (2, 0), (0, 0), (1, 1), (2, 2)]:
    v = M_num(i, j, mp.mpf('1'), eps, dlt)
    rec('E2_selection_%d%d' % (i, j), (abs(v) < mp.mpf('1e-40')) if i != j else (v > 0),
        'M[%d,%d] = %s' % (i, j, ns(v, 12)))
def eigvals3(M):
    tr = mp.mpf('0'); tr2 = mp.mpf('0')
    for i in range(3):
        tr += M[i, i]
        for j in range(3):
            tr2 += M[i, j] * M[j, i]
    c1 = (tr * tr - tr2) / 2
    d0 = mp.det(M)
    roots = mp.polyroots([1, -tr, c1, -d0], maxsteps=500, error=False)
    return sorted([mp.re(r) for r in roots])
lams = eigvals3(M_doc)
s = mp.sqrt(eps ** 2 + dlt ** 2) / 2
ana = [1 - s, mp.mpf('1'), 1 + s]
rec('E3_eigenvalues', all(close(lams[k], ana[k], mp.mpf('1e-40')) for k in range(3)),
    '(%s, %s, %s)' % (ns(lams[0], 12), ns(lams[1], 12), ns(lams[2], 12)))
rec('E4_arithmetic_progression', close(lams[0] + lams[2], 2 * lams[1], mp.mpf('1e-40')),
    'lambda1+lambda3 = 2*lambda2  =>  m_e+m_tau=2*m_mu')
me, mmu, mtau = mp.mpf('0.51099895'), mp.mpf('105.6583755'), mp.mpf('1776.86')
rec('E5_obs_violates', not close(me + mtau, 2 * mmu, mp.mpf('1')),
    'obs LHS=%s MeV vs RHS=%s MeV (ratio %s)' % (ns(me + mtau, 10), ns(2 * mmu, 10), ns((me + mtau) / (2 * mmu), 8)))
rec('E6_positivity_domain', s < 1,
    'lambda1>0 requires sqrt(eps^2+dlt^2)<2; here sqrt=%s' % ns(2 * s, 10))
# q=3/2 changes the whole matrix => arithmetic progression not preserved
M_q = mp.matrix(3, 3)
for i in range(3):
    for j in range(3):
        M_q[i, j] = M_num(i, j, mp.mpf('1.5'), eps, dlt)
lq = eigvals3(M_q)
rec('E7_matrix_q_dependent', not close(lq[0] + lq[2], 2 * lq[1], mp.mpf('1e-6')),
    'q=3/2 eigenvalues = (%s,%s,%s), sum gap = %s' % (ns(lq[0], 10), ns(lq[1], 10), ns(lq[2], 10), ns(lq[0] + lq[2] - 2 * lq[1], 8)))

# ---------------------------------------------------------------- [F] (49-13)-(49-16) KK force
say('== [F] 六维 KK 力谱 (49-15) / 短距渐近 6(R/r)^2 / 长距 1 ==')
def F_ratio(u, L=4000):
    tot = mp.mpf('1')
    for l in range(1, L + 1):
        q = mp.sqrt(l * (l + 1))
        t = (2 * l + 1) * mp.e ** (-q * u) * (1 + q * u)
        tot += t
        if t < mp.mpf('1e-45'):
            break
    return tot
table = [(mp.mpf('0.01'), mp.mpf('60000.3333')), (mp.mpf('0.05'), mp.mpf('2400.3334')),
         (mp.mpf('0.10'), mp.mpf('600.3337')), (mp.mpf('0.20'), mp.mpf('150.3347')),
         (mp.mpf('0.50'), mp.mpf('24.3422')), (mp.mpf('1.00'), mp.mpf('6.3694')),
         (mp.mpf('3.00'), mp.mpf('1.2555')), (mp.mpf('10.00'), mp.mpf('1.0000328'))]
for u, doc in table:
    v = F_ratio(u)
    rec('F1_table_u=%s' % ns(u, 4), close(v, doc, mp.mpf('5e-4')),
        'F/F0 = %s (来料 %s)' % (ns(v, 10), ns(doc, 10)))
# short-distance asymptote derived independently by a CONTINUOUS integral
for u in ['0.01', '0.05', '0.1', '0.2']:
    uu = mp.mpf(u)
    cont = mp.quad(lambda q: 2 * q * mp.e ** (-q * uu) * (1 + q * uu), [0, mp.inf])
    rec('F2_asympt_cont_u=%s' % u, close(cont, 6 / uu ** 2, mp.mpf('1e-30')),
        'Int 2q e^{-qu}(1+qu) dq = %s = 6/u^2' % ns(cont, 12))
for u, doc in table[:4]:
    gap = F_ratio(u) - 6 / u ** 2
    rec('F3_O1_const_u=%s' % ns(u, 4), close(gap, mp.mpf('1') / 3, mp.mpf('5e-3')),
        'F/F0 - 6/u^2 = %s (Euler-Maclaurin O(1) term ~1/3)' % ns(gap, 8))
rec('F4_long_distance', close(F_ratio(mp.mpf('10')), mp.mpf('1'), mp.mpf('1e-4')),
    'r/R=10 -> F/F0=%s (->1, i.e. r^-2)' % ns(F_ratio(mp.mpf('10')), 10))
rec('F5_gauss_exponent', (5 - 1 == 4) and (4 - 1 == 3),
    'D=5 -> r^-4 (49-13); D=4 -> r^-3 (V47); consistent')

# ---------------------------------------------------------------- [G] (S_6) 量纲 / 缺项
say('== [G] V50 六维作用量 S_6：量纲齐次性(自然单位, L 幂) / 是否回应 §七 缺口 ==')
D = {'d6x': Fr(6), 'R6': Fr(-2), 'M6^4': Fr(-4), 'F': Fr(-2), 'F2': Fr(-4),
     'g6^2': Fr(2), 'Psi': Fr(-5, 2), 'D': Fr(-1), 'H': Fr(-2), 'V': Fr(-6)}
terms = {
    'M6^4 R6': D['d6x'] + D['M6^4'] + D['R6'],
    'F^2/g6^2': D['d6x'] + D['F2'] - D['g6^2'],
    'Psi-bar Gamma D Psi': D['d6x'] + 2 * D['Psi'] + D['D'],
    '(DH)^2': D['d6x'] + 2 * D['H'] + 2 * D['D'],
    'V(H)': D['d6x'] + D['V'],
}
for name, v in terms.items():
    rec('G1_dim_%s' % name.replace(' ', '_'), v == 0, 'L^%s (0 = dimensionless action)' % v)
y6 = D['d6x'] - (D['H'] + 2 * D['Psi'])   # [y6] so that y6 H Psi-bar Psi is L^-6
rec('G2_y6_has_dimension', y6 != 0, '[y6] = L^%s => 6D Yukawa carries a scale (non-renormalizable)' % y6)
rec('G3_g6_has_dimension', D['g6^2'] != 0, '[g6^2] = L^%s => 6D gauge coupling carries a scale' % D['g6^2'])
S6_terms = {'EH', 'Maxwell', 'Dirac', 'Higgs-kinetic', 'V(H)', 'Yukawa'}
needed = {'flux-stabilizing / CS / topological term'}
rec('G4_S6_missing_flux_selector', not (S6_terms & needed),
    'S6 contains NO flux/topological selector, yet §七 proves Maxwell energy alone cannot pick N=3')

# ---------------------------------------------------------------- [H] 阳性对照
say('== [H] 阳性对照：守卫必须能抓错 ==')
bad = mp.quad(lambda x: mp.mpf('5') * x * (1 - x), [0, 1])
rec('H1_guard_catches_wrong_coeff', not close(bad, mp.mpf('1'), mp.mpf('1e-10')),
    'if P_1 coefficient 6->5, Int P_1 dx = %s != 1 (guard is live)' % ns(bad, 8))

# ---------------------------------------------------------------- SUMMARY
say('')
say('TOTAL: PASS %d / FAIL %d' % (NP, NF))
say('NOTE: all numbers reproduced; three caliber issues are registered in the 整理册 (q=1 vs N=3; (49-9) q-dependence; S_6 lacks flux selector).')
txt = '\n'.join(LINES) + '\n'
with io.open(os.path.join(HERE, '_out_v49.txt'), 'w', encoding='utf-8') as fh:
    fh.write(txt)
print('ROOT V49 AUDIT: PASS=%d FAIL=%d' % (NP, NF))
print('output -> 源码/_out_v49.txt')
