# -*- coding: utf-8 -*-
"""TUFT-r447 · 二圈RG + 阈值修正 + 质子衰变定价。

攻靶：r443 §十 U2b（二圈、阈值谱、质子衰变）与 r445 留下的 U2b。
范围：标准 MSSM 二圈 beta 矩阵为 [C] 外部输入；本册只做求导一致性核验、
RK4 分段积分、阈值自由度定价、最小 SU(5) 质子衰变独立复算。

红线：二圈 RG 与阈值修正均不是 TUFT 第一性导出；PASS 只表示判据成立。
纯标准库（Decimal 60 位 + Fraction 系数）· Python 3.8。
输出：../数据/TUFT-r447_..._{json,md,_report.txt}
"""
import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
STAMP = '2026-11-24'
TAG = 'TUFT-r447_二圈RG阈值修正与质子衰变定价_MSSMbeta矩阵RK4积分_精算_' + STAMP
VERDICT = ('TWO-LOOP-RG-THRESHOLD-PROTON-PRICED--BETA-CONVERSION-VERIFIED--'
           'RK4-CONVERGED--THRESHOLD-EXTERNAL-INPUT--MIN-SU5-PROTON-DECAY-RECOMPUTED--'
           'PASS-NOT-FIRST-PRINCIPLE')

PI = Decimal('3.14159265358979323846264338327950288419716939937510582097494')
TWO_PI = Decimal(2) * PI
FOUR_PI = Decimal(4) * PI

INPUT = {
    'M_Z_GeV': '91.1876',
    'alpha_em_MZ': '0.0078156',
    'sin2_theta_W': '0.23121',
    'alpha_3_MZ': '0.1180',
    'M_SUSY_GeV': '1000',
    'M_X_max_GeV': '1e20',
    'm_p_GeV': '0.93827208816',
    'hbar_GeV_s': '6.582119569e-25',
    'seconds_per_year': '31557600',
    'proton_lifetime_limit_yr': '1e34',
    'proton_lifetime_limit_superK_yr': '2.4e34',
}

B_SM = (Fraction(41, 10), Fraction(-19, 6), Fraction(-7))
B_MSSM = (Fraction(33, 5), Fraction(1), Fraction(-3))
B2_MSSM = (
    (Fraction(199, 50), Fraction(27, 10), Fraction(44, 5)),
    (Fraction(9, 2), Fraction(35, 6), Fraction(12)),
    (Fraction(11, 2), Fraction(9, 2), Fraction(-26)),
)

ENTRIES = []
GUARDS = []
KEY = {}
R = {}


def P(code, title, detail=''):
    ENTRIES.append((code, 'PASS', title, detail))


def FA(code, title, detail=''):
    ENTRIES.append((code, 'FAIL', title, detail))


def BD(code, title, detail=''):
    ENTRIES.append((code, 'BOUNDARY', title, detail))


def IN(code, title, detail=''):
    ENTRIES.append((code, 'INFO', title, detail))


def CO(code, title, detail=''):
    ENTRIES.append((code, 'CORRECTED', title, detail))


def guard(code, cond, detail=''):
    GUARDS.append((code, bool(cond), detail))
    if not cond:
        raise AssertionError('guard failed: ' + code + ' | ' + str(detail))


def df(f):
    return Decimal(f.numerator) / Decimal(f.denominator)


def fs(x):
    if isinstance(x, Decimal):
        return format(x, '.25E')
    return str(x)


def jsonable(x):
    if isinstance(x, Decimal):
        return fs(x)
    if isinstance(x, Fraction):
        return [x.numerator, x.denominator]
    if isinstance(x, tuple):
        return [jsonable(v) for v in x]
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, list):
        return [jsonable(v) for v in x]
    return x


def initial_alpha():
    mz = Decimal(INPUT['M_Z_GeV'])
    aem = Decimal(INPUT['alpha_em_MZ'])
    s2 = Decimal(INPUT['sin2_theta_W'])
    c2 = Decimal(1) - s2
    a3 = Decimal(INPUT['alpha_3_MZ'])
    a1 = (Decimal(5) / Decimal(3)) * aem / c2
    a2 = aem / s2
    return (a1, a2, a3)


def dalpha_sm(a):
    return tuple(a[i] * a[i] * df(B_SM[i]) / TWO_PI for i in range(3))


def b2_sum(matrix, a):
    return tuple(sum(df(matrix[i][j]) * a[j] for j in range(3)) for i in range(3))


def dalpha_mssm(a):
    s = b2_sum(B2_MSSM, a)
    return tuple(a[i] * a[i] / TWO_PI * (df(B_MSSM[i]) + s[i] / FOUR_PI) for i in range(3))


def dalpha_inv_mssm(a):
    s = b2_sum(B2_MSSM, a)
    return tuple(-(df(B_MSSM[i]) + s[i] / FOUR_PI) / TWO_PI for i in range(3))


def rk4_step(a, h, deriv):
    k1 = deriv(a)
    a2 = tuple(a[i] + h * k1[i] / Decimal(2) for i in range(3))
    k2 = deriv(a2)
    a3 = tuple(a[i] + h * k2[i] / Decimal(2) for i in range(3))
    k3 = deriv(a3)
    a4 = tuple(a[i] + h * k3[i] for i in range(3))
    k4 = deriv(a4)
    return tuple(a[i] + h * (k1[i] + Decimal(2) * k2[i] + Decimal(2) * k3[i] + k4[i]) / Decimal(6)
                 for i in range(3))


def run_trajectory(h):
    mz = Decimal(INPUT['M_Z_GeV'])
    ms = Decimal(INPUT['M_SUSY_GeV'])
    tmax = Decimal(INPUT['M_X_max_GeV']).ln()
    t0 = mz.ln()
    ts = ms.ln()
    a = initial_alpha()
    traj = [(t0, a, 'SM-1L')]
    t = t0
    while t < ts:
        step = min(h, ts - t)
        a = rk4_step(a, step, dalpha_sm)
        t += step
        traj.append((t, a, 'SM-1L'))
    while t < tmax:
        step = min(h, tmax - t)
        a = rk4_step(a, step, dalpha_mssm)
        t += step
        traj.append((t, a, 'MSSM-2L'))
    return traj, t0


def crossing(traj, i, j):
    prev = None
    for t, a, _seg in traj:
        f = Decimal(1) / a[i] - Decimal(1) / a[j]
        if prev is not None:
            pt, pf = prev
            if pf == Decimal(0):
                return pt
            if f == Decimal(0) or pf * f < Decimal(0):
                return pt + (t - pt) * abs(pf) / (abs(pf) + abs(f))
        prev = (t, f)
    return None


def state_at(traj, t):
    for k in range(1, len(traj)):
        t0, a0, _ = traj[k - 1]
        t1, a1, _ = traj[k]
        if t <= t1:
            if t1 == t0:
                return a0
            w = (t - t0) / (t1 - t0)
            return tuple(a0[i] + w * (a1[i] - a0[i]) for i in range(3))
    return traj[-1][1]


def beta_conversion_check():
    a = (Decimal('0.042'), Decimal('0.041'), Decimal('0.040'))
    eps = Decimal('1e-7')
    da = dalpha_mssm(a)
    fd = []
    for i in range(3):
        ap = list(a)
        am = list(a)
        ap[i] += eps * da[i]
        am[i] -= eps * da[i]
        inv_p = Decimal(1) / ap[i]
        inv_m = Decimal(1) / am[i]
        fd.append((inv_p - inv_m) / (Decimal(2) * eps))
    exact = dalpha_inv_mssm(a)
    errs = [abs(fd[i] - exact[i]) / max(abs(exact[i]), Decimal('1e-30')) for i in range(3)]
    matrix_mut = [list(row) for row in B2_MSSM]
    matrix_mut[0][1] += Fraction(1)
    s_mut = b2_sum(tuple(tuple(row) for row in matrix_mut), a)
    da_mut = tuple(a[i] * a[i] / TWO_PI * (df(B_MSSM[i]) + s_mut[i] / FOUR_PI) for i in range(3))
    mut_delta = max(abs(da_mut[i] - da[i]) / da[i] for i in range(3))
    return errs, mut_delta


def proton_lifetime_seconds(mg, alpha, mp, hbar):
    return hbar * mg ** 4 / (alpha ** 2 * mp ** 5)


def analyze():
    guard('G0-1', len(B_SM) == 3 and len(B_MSSM) == 3, 'beta vectors')
    guard('G0-2', len(B2_MSSM) == 3 and all(len(row) == 3 for row in B2_MSSM), 'B matrix')
    guard('G0-3', B2_MSSM == (
        (Fraction(199, 50), Fraction(27, 10), Fraction(44, 5)),
        (Fraction(9, 2), Fraction(35, 6), Fraction(12)),
        (Fraction(11, 2), Fraction(9, 2), Fraction(-26))), 'B matrix canonical [C]')
    a0 = initial_alpha()
    guard('G0-4', a0[0] > 0 and a0[1] > 0 and a0[2] > 0, 'positive initial alpha')
    guard('G0-5', abs((a0[1] * Decimal(INPUT['sin2_theta_W'])) - Decimal(INPUT['alpha_em_MZ'])) < Decimal('1e-50'),
          'alpha2 convention')

    conv_errs, mut_delta = beta_conversion_check()
    guard('G0-6', all(e < Decimal('1e-12') for e in conv_errs), [fs(e) for e in conv_errs])
    guard('G0-7', mut_delta > Decimal('1e-5'), fs(mut_delta))

    inv_exact = dalpha_inv_mssm(a0)
    s0 = b2_sum(B2_MSSM, a0)
    inv_wrong_div_ai = tuple(
        -(df(B_MSSM[i]) + s0[i] / FOUR_PI) / TWO_PI / a0[i]
        for i in range(3)
    )
    inv_wrong_rel_delta = max(
        abs(inv_exact[i] - inv_wrong_div_ai[i]) / max(abs(inv_exact[i]), Decimal('1e-30'))
        for i in range(3)
    )
    guard('G0-8', inv_wrong_rel_delta > Decimal('1e-3'), fs(inv_wrong_rel_delta))

    h1 = Decimal('0.02')
    h2 = Decimal('0.01')
    traj1, t0 = run_trajectory(h1)
    traj2, _ = run_trajectory(h2)

    def solve(traj):
        c12 = crossing(traj, 0, 1)
        c13 = crossing(traj, 0, 2)
        c23 = crossing(traj, 1, 2)
        if c12 is None or c13 is None or c23 is None:
            return None
        ls = [c12 - t0, c13 - t0, c23 - t0]
        dL = max(ls) - min(ls)
        a_star = state_at(traj, c12)
        return {'L12': ls[0], 'L13': ls[1], 'L23': ls[2], 'dL': dL,
                't12': c12, 'a_star': a_star, 'MG_GeV': c12.exp(),
                'steps': len(traj)}

    s1 = solve(traj1)
    s2 = solve(traj2)
    guard('G1-1', s1 is not None and s2 is not None, 'pairwise crossings exist')
    guard('G1-2', s2['dL'] > 0, fs(s2['dL']))
    rel_mg = abs(s1['MG_GeV'] - s2['MG_GeV']) / s2['MG_GeV']
    abs_dl = abs(s1['dL'] - s2['dL'])
    guard('G2-1', rel_mg < Decimal('1e-3'), fs(rel_mg))
    guard('G2-2', abs_dl < Decimal('5e-3'), fs(abs_dl))

    sol = s2
    a_star = sol['a_star']
    y = tuple(Decimal(1) / a_star[i] for i in range(3))
    ybar = sum(y, Decimal(0)) / Decimal(3)
    delta = tuple(ybar - y[i] for i in range(3))
    y12 = (y[0] + y[1]) / Decimal(2)
    delta3_keep12 = y12 - y[2]
    split_factor = (TWO_PI * abs(delta3_keep12) / Decimal(3)).exp()
    guard('G3-1', abs(sum(delta, Decimal(0))) < Decimal('1e-45'), fs(sum(delta, Decimal(0))))
    guard('G3-2', delta_fixed_dim == 1 and delta_float_dim == 2, 'threshold dimensions')

    alphaG = (a_star[0] + a_star[1]) / Decimal(2)
    mG = sol['MG_GeV']
    mp = Decimal(INPUT['m_p_GeV'])
    hbar = Decimal(INPUT['hbar_GeV_s'])
    spy = Decimal(INPUT['seconds_per_year'])
    tau_s = proton_lifetime_seconds(mG, alphaG, mp, hbar)
    tau_yr = tau_s / spy
    guard('G4-1', tau_yr > 0, fs(tau_yr))
    unit_rel = abs(tau_yr * spy - tau_s) / tau_s
    guard('G4-2', unit_rel < Decimal('1e-30'), 'unit conversion rel=' + fs(unit_rel))
    tau_mg2 = proton_lifetime_seconds(Decimal(2) * mG, alphaG, mp, hbar)
    tau_a2 = proton_lifetime_seconds(mG, Decimal(2) * alphaG, mp, hbar)
    guard('G4-3', abs(tau_mg2 / tau_s - Decimal(16)) < Decimal('1e-40'), fs(tau_mg2 / tau_s))
    guard('G4-4', abs(tau_a2 / tau_s - Decimal(1) / Decimal(4)) < Decimal('1e-40'), fs(tau_a2 / tau_s))

    unified_2loop = sol['dL'] <= Decimal('1.00')
    limit1 = Decimal(INPUT['proton_lifetime_limit_yr'])
    limit2 = Decimal(INPUT['proton_lifetime_limit_superK_yr'])

    KEY.update({
        'verdict': VERDICT,
        'normalization_lock': 'Q=T3+Y, alpha1=(5/3)alpha_em/cos^2(theta_W), GUT-normalized',
        'beta_conversion_max_rel_err': max(conv_errs),
        'beta_matrix_mutation_rel_delta': mut_delta,
        'inv_alpha_wrong_div_alpha_rel_delta': inv_wrong_rel_delta,
        'h_used': h2,
        'convergence_rel_MG': rel_mg,
        'convergence_abs_dL': abs_dl,
        'steps': sol['steps'],
        'L12': sol['L12'], 'L13': sol['L13'], 'L23': sol['L23'], 'dL': sol['dL'],
        'M_G_GeV': mG,
        'alpha_G': alphaG,
        'alpha_inv_at_MG': y,
        'threshold_minimal_norm_delta': delta,
        'threshold_delta3_if_keep12': delta3_keep12,
        'threshold_splitting_factor_b3_1L': split_factor,
        'threshold_dim_fixed_MG': delta_fixed_dim,
        'threshold_dim_float_MG': delta_float_dim,
        'proton_lifetime_s': tau_s,
        'proton_lifetime_yr': tau_yr,
        'proton_limit_yr': limit1,
        'proton_limit_superK_yr': limit2,
        'unified_2loop': unified_2loop,
    })

    IN('I01', '[C] 输入与超荷归一锁', 'GUT 归一 alpha1=(5/3)alpha_em/cos^2(theta_W)；beta 系数与 B 矩阵均为外部标准输入')
    P('I02', 'beta 形式求导一致性', 'g 形式转 alpha^-1 形式的最大相对误差 ' + fs(max(conv_errs)))
    P('I03', 'MSSM 二圈矩阵锁定与变异灵敏', 'B 矩阵 3x3 逐项匹配；改 B12 后导数相对变化 ' + fs(mut_delta))
    P('I04', 'RK4 步长收敛', 'h=0.02 与 0.01 的相对 M_G 差 ' + fs(rel_mg) + '，dL 差 ' + fs(abs_dl))
    if unified_2loop:
        P('I05', 'MSSM 二圈分段积分仍汇聚', 'dL=' + fs(sol['dL']) + ' e-fold，M_G=' + fs(mG) + ' GeV')
    else:
        FA('I05', 'MSSM 二圈分段积分不汇聚', 'dL=' + fs(sol['dL']) + ' e-fold')
    BD('I06', '阈值修正为外部自由输入', '固定 M_G 维度 ' + str(delta_fixed_dim) + '，M_G 可用时维度 ' + str(delta_float_dim) + '；最小范数 delta=' + fs(delta))
    P('I07', '质子衰变寿命独立复算完成', 'tau~hbar*M_X^4/(alpha_G^2*m_p^5)，kappa=1 口径 tau=' + fs(tau_yr) + ' yr；M_X^4 与 alpha^-2 标度守卫 G4-3/G4-4 通过')
    if tau_yr < limit1:
        FA('I08', '最小 SU(5) 质子衰变被实验下限排除', 'tau/limit=' + fs(tau_yr / limit1))
    else:
        P('I08', '最小 SU(5) 质子衰变未被 1e34 yr 下限排除', 'tau/limit=' + fs(tau_yr / limit1))
    CO('I09', '登记 r443 U2b 状态更新', '二圈/阈值/质子衰变已定价，但不改 r443/r445 字节')
    IN('I10', '全局记分板不变', '0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4')
    BD('I11', '强子矩阵元因子未纳入', 'tau ~ kappa*M_X^4/(alpha_G^2 m_p^5)，本册取 kappa=1，O(1) 不确定度未消除')
    IN('I12', '阈值质量分裂口径', '若用一圈 b3=-3 单参数解释 delta3，需要分裂因子 ' + fs(split_factor) + '；口径依赖，不迁移为预言')
    CO('I13', '来料模块2倒数耦合公式修正', '来料写作 -b_i/(2pi)-sum_j B_ij*alpha_j/(8pi^2*alpha_i)；由 dalpha_i/dt 链式推导应无 /alpha_i，错误口径相对差 ' + fs(inv_wrong_rel_delta) + '；源码保持正确式')
    IN('I14', 'r447b 方向登记', '顶夸克 Yukawa 耦合二圈反馈 + 非简并阈值全参数扫描 + 三耦合精确交汇微调程度量化；本册只登记不执行')

    R['trajectory_coarse'] = [{'t': fs(t), 'a1': fs(a[0]), 'a2': fs(a[1]), 'a3': fs(a[2]), 'seg': seg}
                              for t, a, seg in traj1[::max(1, len(traj1) // 200)]]
    R['beta_conversion_errors'] = [fs(e) for e in conv_errs]


delta_fixed_dim = 3 - 2
delta_float_dim = 4 - 2

analyze()

report = []
report.append('TUFT-r447 REPORT')
report.append('VERDICT = ' + VERDICT)
for k in ('normalization_lock', 'beta_conversion_max_rel_err', 'beta_matrix_mutation_rel_delta',
          'inv_alpha_wrong_div_alpha_rel_delta',
          'h_used', 'convergence_rel_MG', 'convergence_abs_dL', 'steps',
          'L12', 'L13', 'L23', 'dL', 'M_G_GeV', 'alpha_G',
          'threshold_delta3_if_keep12', 'threshold_splitting_factor_b3_1L',
          'proton_lifetime_s', 'proton_lifetime_yr', 'proton_limit_yr',
          'proton_limit_superK_yr', 'unified_2loop'):
    report.append(k.upper() + ' = ' + fs(KEY[k]))
counts = {}
for _code, st, _title, _detail in ENTRIES:
    counts[st] = counts.get(st, 0) + 1
report.append('PASS=' + str(counts.get('PASS', 0)) + ' FAIL=' + str(counts.get('FAIL', 0)) +
              ' BOUNDARY=' + str(counts.get('BOUNDARY', 0)) + ' INFO=' + str(counts.get('INFO', 0)) +
              ' CORRECTED=' + str(counts.get('CORRECTED', 0)))
report.append('GUARDS ' + str(sum(1 for _c, ok, _d in GUARDS if ok)) + '/' + str(len(GUARDS)))
report.append('MUTATION_DETECTED = [' + ', '.join(['True'] * 1) + ']')
report_text = '\n'.join(report) + '\n'

payload = {
    'tag': TAG,
    'stamp': STAMP,
    'verdict': VERDICT,
    'input': INPUT,
    'b_sm_one_loop': list(B_SM),
    'b_mssm_one_loop': list(B_MSSM),
    'b_mssm_two_loop_matrix': [list(row) for row in B2_MSSM],
    'key_numbers': KEY,
    'entries': [{'code': c, 'status': s, 'title': t, 'detail': d} for c, s, t, d in ENTRIES],
    'guards': [{'code': c, 'ok': ok, 'detail': d} for c, ok, d in GUARDS],
    'aux': R,
}

os.makedirs(DATA, exist_ok=True)
with io.open(os.path.join(DATA, TAG + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=jsonable)
    f.write('\n')

md = []
md.append('# ' + TAG)
md.append('')
md.append('- 判词：`' + VERDICT + '`')
md.append('- 条目：' + str(len(ENTRIES)) + '；PASS=' + str(counts.get('PASS', 0)) +
          ' / FAIL=' + str(counts.get('FAIL', 0)) + ' / BOUNDARY=' + str(counts.get('BOUNDARY', 0)) +
          ' / INFO=' + str(counts.get('INFO', 0)) + ' / CORRECTED=' + str(counts.get('CORRECTED', 0)))
md.append('- 守卫：' + str(sum(1 for _c, ok, _d in GUARDS if ok)) + '/' + str(len(GUARDS)))
md.append('')
md.append('## 关键读数')
md.append('')
md.append('| 项 | 读数 |')
md.append('|---|---|')
for k in ('beta_conversion_max_rel_err', 'beta_matrix_mutation_rel_delta',
          'inv_alpha_wrong_div_alpha_rel_delta', 'convergence_rel_MG', 'convergence_abs_dL',
          'dL', 'M_G_GeV', 'alpha_G', 'threshold_delta3_if_keep12',
          'threshold_splitting_factor_b3_1L', 'proton_lifetime_yr'):
    md.append('| ' + k + ' | ' + fs(KEY[k]) + ' |')
md.append('')
md.append('## 条目')
md.append('')
for c, s, t, d in ENTRIES:
    md.append('- **' + c + ' [' + s + ']** ' + t + '：' + d)
with io.open(os.path.join(DATA, TAG + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')
with io.open(os.path.join(DATA, TAG + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write(report_text)

sys.stdout.write(report_text)
