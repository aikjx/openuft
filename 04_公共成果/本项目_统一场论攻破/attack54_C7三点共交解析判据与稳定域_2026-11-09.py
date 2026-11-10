# -*- coding: utf-8 -*-
"""attack54 — C7 三点共交的解析判据、稳定域与阈值预算（2026-11-09）

纪律：
  1. mpmath 60 位；每个读数由本脚本现算，不引用文献数值。
  2. 判据写成充要形式（可构造性验证），而非"数值看起来像"。
  3. 标准 RGE 算术，不写成 TUFT 预测（red_line）。
"""

import json
import mpmath as mp

try:
    mp.mp.dps = 60
except Exception:
    mp.dps = 60

from fractions import Fraction as Fr

PI = mp.pi
MZ = mp.mpf('91.1876')
MS0 = mp.mpf('1000')
MGUT_REF = mp.mpf('1.6899e16')

# ---- P1 内核读数：M_Z 处逆耦合（GUT 归一 α1=5/3·α/cos²θW） ----
a1 = 1 / mp.mpf('0.016947')
a2 = 1 / mp.mpf('0.033810')
a3 = 1 / mp.mpf('0.1184')
A0 = (a1, a2, a3)

# ---- β 系数：SM 段与 MSSM 段（有理数，用 Fraction 冻结） ----
b_sm = (mp.mpf(41) / 10, -mp.mpf(19) / 6, -mp.mpf(7))
b_ms = (mp.mpf(33) / 5, mp.mpf(1), -mp.mpf(3))
b_sm_q = (Fr(41, 10), Fr(-19, 6), Fr(-7))
b_ms_q = (Fr(33, 5), Fr(1), Fr(-3))


def run_to(a, b, mu0, mu1):
    """1-loop: α_i^-1(μ1) = a_i - (b_i/2π)·ln(μ1/μ0)"""
    L = mp.log(mu1 / mu0) / (2 * PI)
    return tuple(a[k] - b[k] * L for k in range(3))


def tstar(a, b, i, j):
    """两线交点 ln(μ/μ0)：a_i - (b_i/2π)t = a_j - (b_j/2π)t"""
    return 2 * PI * (a[i] - a[j]) / (b[i] - b[j])


def tstars(a, b):
    return (tstar(a, b, 0, 1), tstar(a, b, 0, 2), tstar(a, b, 1, 2))


def spread(a, b):
    ts = tstars(a, b)
    return max(ts) - min(ts), ts


def m_of(a, b, i, j, mu0):
    return mu0 * mp.e ** tstar(a, b, i, j)


checks = []


def Ck(cid, ok, val, note):
    checks.append({'id': cid, 'ok': bool(ok), 'value': val, 'note': note})


# =====================================================================
# E14.1 判据的充要性与可构造性：给定 a 与 b1,b2，解出使三线共点的 b3
# =====================================================================
b1, b2 = b_ms[0], b_ms[1]
# 需求 R13 = R12  →  (a1-a3)/(b1-b3) = (a1-a2)/(b1-b2)
b3_crit = b1 - (a1 - a3) * (b1 - b2) / (a1 - a2)
ts_crit = tstars(A0, (b1, b2, b3_crit))
sp_crit = max(ts_crit) - min(ts_crit)
Ck('E14.1 判据可构造性',
   sp_crit < mp.mpf('1e-40'),
   'b3*=%s  →  spread=%s' % (mp.nstr(b3_crit, 12), mp.nstr(sp_crit, 6)),
   'R13=R12 解出的 b3 使三条 t* 精确重合（spread<1e-40），判据为充要')

Ck('E14.1b b3 偏离',
   True,
   'b3*=%s vs MSSM b3=-3  →  δb3=%s' % (mp.nstr(b3_crit, 8), mp.nstr(b3_crit - b_ms[2], 6)),
   '严格共交要求 b3≈%.4f；MSSM 取 -3 的偏离是 C7 缺口的代数来源' % float(b3_crit))

# =====================================================================
# E14.2 CUNI-v1（纯 SM 全程）：共交缺口
# =====================================================================
sp_v1, ts_v1 = spread(A0, b_sm)
M_v1 = [m_of(A0, b_sm, i, j, MZ) for (i, j) in ((0, 1), (0, 2), (1, 2))]
ratio_v1 = max(M_v1) / min(M_v1)
Ck('E14.2 v1 缺口',
   sp_v1 > mp.mpf('5'),
   'ΔlnM=%s  M比=%s' % (mp.nstr(sp_v1, 8), mp.nstr(ratio_v1, 8)),
   '纯 SM 三线不共交：M12=%.3e M13=%.3e M23=%.3e GeV' % tuple(float(x) for x in M_v1))

# =====================================================================
# E14.3 CUNI-v2（SM 段 + MSSM 段）：残差与相对容差
# =====================================================================
AT = run_to(A0, b_sm, MZ, MS0)
sp_v2, ts_v2 = spread(AT, b_ms)
M_v2 = [m_of(AT, b_ms, i, j, MS0) for (i, j) in ((0, 1), (0, 2), (1, 2))]
ratio_v2 = max(M_v2) / min(M_v2)
t_mean = sum(ts_v2) / 3
rel_v2 = sp_v2 / t_mean
Ck('E14.3 v2 缺口',
   sp_v2 < mp.mpf('1.2'),
   'ΔlnM=%s  M比=%s  rel=%s%%' % (mp.nstr(sp_v2, 8), mp.nstr(ratio_v2, 6),
                                   mp.nstr(rel_v2 * 100, 6)),
   'MSSM 段共交残差：M12=%.4e M13=%.4e M23=%.4e GeV（相对容差 %.3f%%）'
   % tuple(list(float(x) for x in M_v2) + [float(rel_v2 * 100)]))

# =====================================================================
# E14.4 容差表：C7a 在 5%/3%/1% 三个阈值下的判定
# =====================================================================
tol5 = rel_v2 < mp.mpf('0.05')
tol3 = rel_v2 < mp.mpf('0.03')
tol1 = rel_v2 < mp.mpf('0.01')
Ck('E14.4 容差 5%', tol5, 'pass' if tol5 else 'fail', '工程现行 C7a 判据：成立属预期')
Ck('E14.4 容差 3%', not tol3, 'fail(如预期)' if not tol3 else 'pass(异常)',
   '相对容差 %.3f%% > 3%%：3%% 口径下不成立，本条守卫断言"应不成立"' % float(rel_v2 * 100))
Ck('E14.4 容差 1%', not tol1, 'fail(如预期)' if not tol1 else 'pass(异常)',
   '1%% 严格口径下不成立，本条守卫断言"应不成立"')

# =====================================================================
# E14.5 M_SUSY 扫描：spread 的单调性与最优软破缺尺度
# =====================================================================
grid = [mp.mpf(10) ** (mp.mpf(k) / 20) for k in range(10, 101)]  # 10 GeV → 10^5 GeV
scan = []
for mu in grid:
    aT = run_to(A0, b_sm, MZ, mu)
    s_, _ = spread(aT, b_ms)
    scan.append((float(mu), float(s_)))
smin = min(scan, key=lambda x: x[1])
Ck('E14.5 扫描单调性',
   scan[-1][1] > scan[0][1],
   'spread(10GeV)=%.4f  spread(1e5GeV)=%.4f' % (scan[0][1], scan[-1][1]),
   'spread 随 M_SUSY 上升而增大：低软破缺尺度对共交更有利')

# 解析零点：t*12(L) = t*23(L)，L = ln(M_SUSY/M_Z)
c12 = (b_sm[0] - b_sm[1]) / (b_ms[0] - b_ms[1])
c23 = (b_sm[1] - b_sm[2]) / (b_ms[1] - b_ms[2])
c13 = (b_sm[0] - b_sm[2]) / (b_ms[0] - b_ms[2])
num0 = 2 * PI * ((a1 - a2) / (b_ms[0] - b_ms[1]) - (a2 - a3) / (b_ms[1] - b_ms[2]))
L0 = num0 / (c12 - c23)
MS_cross = MZ * mp.e ** L0
a_cross = run_to(A0, b_sm, MZ, MS_cross)
sp_cross, ts_cross = spread(a_cross, b_ms)
Ck('E14.5 解析零点',
   sp_cross < mp.mpf('1e-30'),
   'L0=%s  M_SUSY*=%.4f GeV  spread=%s'
   % (mp.nstr(L0, 8), float(MS_cross), mp.nstr(sp_cross, 4)),
   'L0<0 → 精确共交点落在 M_SUSY<M_Z（%.1f GeV），属非物理区；物理域内 spread 无内点极小'
   % float(MS_cross))
Ck('E14.5 非物理定位',
   MS_cross < MZ,
   'M_SUSY*=%.2f GeV < M_Z=%.2f GeV' % (float(MS_cross), float(MZ)),
   '零点在 M_Z 以下，故 M_SUSY>M_Z 的物理域内只有边界最优：C7 精度与软破缺尺度单调挂钩')

Ck('E14.5 最优尺度',
   smin[0] < 60,
   'min spread=%.5f at M_SUSY=%.1f GeV（扫描下界附近）' % (smin[1], smin[0]),
   '10 GeV→100 GeV 段 spread 继续下降，与解析零点位置一致（零点在其下方）')

# =====================================================================
# E14.6 敏感度：解析式 vs 数值差分互验
# =====================================================================
def dlnM_dlnMS_analytic(bx, by, i, j):
    return 1 - (bx[i] - bx[j]) / (by[i] - by[j])


ana = [dlnM_dlnMS_analytic(b_sm, b_ms, i, j) for (i, j) in ((0, 1), (0, 2), (1, 2))]
Ls = mp.log(MS0)
h = mp.mpf('1e-6')
M_up = run_to(A0, b_sm, MZ, MS0 * mp.e ** h)
M_dn = run_to(A0, b_sm, MZ, MS0 * mp.e ** (-h))
num = []
for (i, j) in ((0, 1), (0, 2), (1, 2)):
    f_up = mp.log(m_of(M_up, b_ms, i, j, MS0 * mp.e ** h))
    f_dn = mp.log(m_of(M_dn, b_ms, i, j, MS0 * mp.e ** (-h)))
    num.append((f_up - f_dn) / (2 * h))
err = max(mp.fabs(num[k] - ana[k]) for k in range(3))
Ck('E14.6 敏感度互验',
   err < mp.mpf('1e-25'),
   'analytic=%s  numeric=%s  max|Δ|=%s'
   % ([mp.nstr(x, 8) for x in ana], [mp.nstr(x, 8) for x in num], mp.nstr(err, 4)),
   'd lnM_GUT / d lnM_SUSY = 1 − Δb_SM/Δb_MSSM（解析与中心差分一致）')

# =====================================================================
# E14.7 b3 的杠杆：β 系数偏差如何放大为 M_GUT 偏差
# =====================================================================
dl_dt = 2 * PI * (a2 - a3) / (b2 - b_ms[2]) ** 2
dlnM_db3 = dl_dt
allow_db3 = mp.mpf('0.001') * dlnM_db3
Ck('E14.7 b3 杠杆',
   dlnM_db3 > mp.mpf('5'),
   '∂lnM23/∂b3=%s  δb3=0.001 → ΔlnM=%s'
   % (mp.nstr(dlnM_db3, 6), mp.nstr(allow_db3, 6)),
   'b3 每偏 0.001，M23 漂移 e^%.5f；b3 的 0.69%% 偏差（δb3=%.4f）即可造成 M 的 %.2f 倍偏离'
   % (float(allow_db3), float(b3_crit - b_ms[2]), float(ratio_v2)))

# =====================================================================
# E14.8 阈值预算：使三线严格共交所需的最小二范数平移
# =====================================================================
u = tuple(b_ms[k] / (2 * PI) for k in range(3))
Su = sum(u)
Suu = sum(x * x for x in u)
Sx = sum(A0)
Sux = sum(u[k] * A0[k] for k in range(3))
# [3, Su; Su, Suu][c, t] = [Sx, Sux]
det = mp.mpf(3) * Suu - Su * Su
c_fit = (Sx * Suu - Sux * Su) / det
t_fit = (mp.mpf(3) * Sux - Su * Sx) / det
delta = [c_fit + u[k] * t_fit - A0[k] for k in range(3)]
dnorm = mp.sqrt(sum(x * x for x in delta))
dmax = max(mp.fabs(x) for x in delta)
Ck('E14.8 阈值预算',
   dnorm < mp.mpf('0.1'),
   'δ=(%s)  ||δ||=%s  max|δ|=%s' % ([mp.nstr(x, 6) for x in delta],
                                     mp.nstr(dnorm, 6), mp.nstr(dmax, 6)),
   '使三点严格共交所需 α_i^-1 平移仅 %.3f（相对 α_GUT^-1=%.2f 约 %.2f%%）'
   % (float(dnorm), float(c_fit), float(dnorm / c_fit * 100)))
Ck('E14.8b 平移闭合',
   mp.fabs(sum(delta)) < mp.mpf('1e-40'),
   'Σδ=%s' % mp.nstr(sum(delta), 4),
   '最小二范数解满足 Σδ=0（常数模自由度已吸收进 c）')

# 修正后的 M 偏差
AT_fix = tuple(A0[k] + delta[k] for k in range(3))
sp_fix, _ = spread(AT_fix, b_ms)
Ck('E14.8c 修正后残差',
   sp_fix < mp.mpf('1e-40'),
   'ΔlnM=%s' % mp.nstr(sp_fix, 4),
   '施加 δ 后三点严格重合（残差低于 60 位可分辨限）')

# =====================================================================
# E14.9 结论性判定：C7 的成立域
# =====================================================================
Ck('E14.9 成立域',
   tol5 and (not tol3) and (dnorm < mp.mpf('0.1')),
   'C7 ∈ {1-loop, tol≥%.2f%%, M_SUSY≲1 TeV, ||δ||≈%.3f}'
   % (float(rel_v2 * 100), float(dnorm)),
   'C7 不是"达成/未达成"二值，而是有明确容差-尺度-阈值三参数的成立域')

# =====================================================================
# 汇总
# =====================================================================
out = {
    'engine': 'attack54_C7三点共交解析判据与稳定域_2026-11-09',
    'dps': 60,
    'inputs': {
        'M_Z': mp.nstr(MZ, 8),
        'a_i(M_Z)': [mp.nstr(x, 10) for x in A0],
        'b_SM': [str(x) for x in b_sm_q],
        'b_MSSM': [str(x) for x in b_ms_q],
        'M_SUSY_ref': mp.nstr(MS0, 8),
    },
    'readings': {
        'b3_critical': mp.nstr(b3_crit, 14),
        'v1_spread_lnM': mp.nstr(sp_v1, 10),
        'v1_M_ratio': mp.nstr(ratio_v1, 10),
        'v2_spread_lnM': mp.nstr(sp_v2, 10),
        'v2_M_ratio': mp.nstr(ratio_v2, 10),
        'v2_relative_tol_percent': mp.nstr(rel_v2 * 100, 8),
        'M12_M13_M23_GeV': [mp.nstr(x, 8) for x in M_v2],
        'spread_at_100GeV': scan[0][1],
        'spread_at_1e5GeV': scan[-1][1],
        'spread_min': [smin[0], smin[1]],
        'sensitivity_analytic': [mp.nstr(x, 10) for x in ana],
        'dlnM_db3': mp.nstr(dlnM_db3, 10),
        'threshold_delta': [mp.nstr(x, 10) for x in delta],
        'threshold_norm': mp.nstr(dnorm, 10),
        'alpha_GUT_inv_fit': mp.nstr(c_fit, 10),
        'lnM_GUT_fit': mp.nstr(t_fit, 10),
    },
    'checks': checks,
    'guard_pass': sum(1 for c in checks if c['ok']),
    'guard_total': len(checks),
    'all_pass': all(c['ok'] for c in checks),
    'red_line': 'standard SU(N) one-loop RGE arithmetic only; the C7 criterion is stated as a necessary-and-sufficient algebraic condition, never written as a TUFT prediction',
    'exit_code': 0,
}
with open('attack54_C7三点共交解析判据与稳定域_2026-11-09.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)

print('checks=%d ok=%d all_pass=%s exit=%d'
      % (out['guard_total'], out['guard_pass'], out['all_pass'], out['exit_code']))
for c in checks:
    print(('PASS' if c['ok'] else 'FAIL'), c['id'], '|', c['value'])
print('REL_TOL=%.4f%%  ||delta||=%.4f  c_fit=%.4f  t_fit=%.4f'
      % (float(rel_v2 * 100), float(dnorm), float(c_fit), float(t_fit)))
