# -*- coding: utf-8 -*-
# attack27b · CUNI-v2「零代价修法」修正引擎（2026-10-30）
#
# 承接 attack27 的裁定（K1-K6 实际 2/6），执行其中零代价的修法：
#   M1 删除 ok 字面量守卫 -> P2(b-tau 统一) 改为 Yukawa RGE 真实跑动
#   M2 tau_p 改为由 M_GUT / alpha_GUT / alpha_H 实算（恢复与模型参数的耦合）
#   M4 汇聚判据显式化，并并行报告线性能标跨度
#   M6 「低能预言偏差」正名为「三点不共交自洽残差」
#   M7 Super-K 下限采用 2.4e34 yr
#
# 纪律：本册不修改 E1/E2/E3/D0 任何字节（保持历史基线可追溯，r67 体例）；
#       只提供「若执行修法会得到什么」，供后续决定是否替换。
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = []
_CODES = {}


def add(code, verdict, title, value, note):
    _CODES[code.split()[0]] = verdict
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title,
                    'value': value, 'note': note})


def E(*a):
    s = ' '.join(str(x) for x in a)
    try:
        print(s)
    except Exception:
        print(s.encode('ascii', 'replace').decode('ascii'))


import mpmath as mp

mp.mp.dps = 40
pi = mp.pi

E('=' * 78)
E('attack27b · 零代价修法修正引擎（M1/M2/M4/M6/M7）')
E('=' * 78)

# ---------- 公共输入（与 E2 同源，保证可比） ----------
MZ = mp.mpf('91.1876')
MSUSY = mp.mpf('1000')
alpha_em = mp.mpf(1) / mp.mpf('127.916')
sw2 = mp.mpf('0.23122')
a1_in = alpha_em / (1 - sw2) * mp.mpf(5) / 3
a2_in = alpha_em / sw2
a3_in = mp.mpf('0.1184')

b1s, b2s, b3s = mp.mpf(41) / 10, -mp.mpf(19) / 6, mp.mpf(-7)
b1m, b2m, b3m = mp.mpf(33) / 5, mp.mpf(1), mp.mpf(-3)

I = [1 / a1_in - b1s * mp.log(MSUSY / MZ) / (2 * pi),
     1 / a2_in - b2s * mp.log(MSUSY / MZ) / (2 * pi),
     1 / a3_in - b3s * mp.log(MSUSY / MZ) / (2 * pi)]
B = [b1m, b2m, b3m]


def cross(i, j):
    ln_m = (I[j] - I[i]) * 2 * pi / (B[j] - B[i])
    return ln_m, I[i] - B[i] * ln_m / (2 * pi)


L12, I12 = cross(0, 1)
L13, I13 = cross(0, 2)
L23, I23 = cross(1, 2)
M12, M13, M23 = MSUSY * mp.e ** L12, MSUSY * mp.e ** L13, MSUSY * mp.e ** L23
MGUT = (M12 + M13 + M23) / 3
AG_INV = (I12 + I13 + I23) / 3
AG = 1 / AG_INV
spread = M23 / M12

# ============================================================
# M4：汇聚判据显式化 —— 同时报告 ln 判据与线性能标跨度
# ============================================================
E('')
E('[M4] 汇聚判据显式化')
E('-' * 78)
E('  ln 判据 |lnM12-lnM13|/lnM13 = %s' % mp.nstr(mp.fabs(L12 - L13) / L13, 6))
E('  ln 判据 |lnM13-lnM23|/lnM23 = %s' % mp.nstr(mp.fabs(L13 - L23) / L23, 6))
E('  线性能标跨度 M23/M12         = %s 倍' % mp.nstr(spread, 6))
E('  M_GUT(三点算术平均)          = %s GeV' % mp.nstr(MGUT, 8))
E('  alpha_GUT^-1                 = %s' % mp.nstr(AG_INV, 8))
E('')
E('  修正后的诚实表述：三点并不共交，最大与最小相差 %s 倍；'
  % mp.nstr(spread, 4))
E('  M_GUT 是三个不共交点的算术平均，不是唯一统一点。')
add('M4 BOUNDARY', 'BOUNDARY', '汇聚判据修正后：三点不共交为既成事实，须显式声明',
    'ln 判据 1.36%%/1.87%%；线性能标跨度 %s 倍' % mp.nstr(spread, 5),
    '修法不是换判据，而是同时报告两个口径并声明阈值无物理依据。'
    'MSSM 相对 SM 的改善（9809.99 倍 -> %s 倍）依然成立且重要' % mp.nstr(spread, 4))

# ============================================================
# M6：「低能预言偏差」正名
# ============================================================
E('')
E('[M6] 低能偏差正名')
E('-' * 78)


def back(mgut, ag_inv, i, b_sm, b_msm):
    inv_mz = ag_inv + b_sm * mp.log(MSUSY / MZ) / (2 * pi) \
        + b_msm * mp.log(mgut / MSUSY) / (2 * pi)
    return 1 / inv_mz


own = back(M13, I13, 2, b3s, b3m)
avg = back(MGUT, AG_INV, 2, b3s, b3m)
E('  alpha_s: 沿自身交点回推 %s（残差 %s）'
  % (mp.nstr(own, 8), mp.nstr(mp.fabs(own - a3_in) / a3_in, 3)))
E('  alpha_s: 沿平均点回推   %s（残差 %s）'
  % (mp.nstr(avg, 8), mp.nstr(mp.fabs(avg - a3_in) / a3_in, 4)))
E('  >> 正名为「三点不共交自洽残差」，不再表述为「预言与实测吻合」')
add('M6 PASS', 'PASS', '偏差已正名（零代价，仅改语义）',
    '自身交点残差 %s；平均点残差 %s'
    % (mp.nstr(mp.fabs(own - a3_in) / a3_in, 3), mp.nstr(mp.fabs(avg - a3_in) / a3_in, 4)),
    '修法完成：同一数字不再被表述为预言的证据。'
    '该残差此后只用于度量三点不共交的程度')

# ============================================================
# M2：tau_p 由 M_GUT / alpha_GUT / alpha_H 实算
# ============================================================
E('')
E('[M2] tau_p 改为实算（恢复与模型参数的耦合）')
E('-' * 78)
# 维度-6 质子衰变工程闭式（带 O(1) 系数不确定度）
TAU0 = mp.mpf('1.0e35')     # yr, 参考标度
M_REF = mp.mpf('2.0e16')    # GeV
AGINV_REF = mp.mpf('35')    # 参考 alpha_GUT^-1
AH_REF = mp.mpf('0.015')    # GeV^3, 格点典型强子矩阵元


def tau_p_of(mgut, ag_inv, ah):
    """tau_p ∝ M_GUT^4 / alpha_GUT^2 / alpha_H^2  -> 以参考点归一"""
    ag = 1 / ag_inv
    ag_ref = 1 / AGINV_REF
    return TAU0 * (mgut / M_REF) ** 4 * (ag_ref / ag) ** 2 * (AH_REF / ah) ** 2


SK = mp.mpf('2.4e34')   # M7：Super-K 实际下限
tp = tau_p_of(MGUT, AG_INV, AH_REF)
E('  M_GUT = %s GeV, alpha_GUT^-1 = %s' % (mp.nstr(MGUT, 8), mp.nstr(AG_INV, 8)))
E('  tau_p(alpha_H=0.015) = %s yr' % mp.nstr(tp, 6))
E('  vs 声称硬写值 3.51e34 yr -> 相对差 %s'
  % mp.nstr(mp.fabs(tp - mp.mpf('3.51e34')) / mp.mpf('3.51e34'), 4))
E('')
E('  alpha_H 不确定度扫描（tau_p ∝ alpha_H^-2）：')
E('    %-10s %-14s %s' % ('alpha_H', 'tau_p (yr)', 'vs SK 2.4e34'))
rows = []
for f in ('0.5', '0.7', '1.0', '1.4', '2.0'):
    ah = AH_REF * mp.mpf(f)
    v = tau_p_of(MGUT, AG_INV, ah)
    verdict = '未排除' if v >= SK else '被排除'
    rows.append((mp.nstr(ah, 4), mp.nstr(v, 6), verdict))
    E('    %-10s %-14s %s' % (mp.nstr(ah, 4), mp.nstr(v, 6), verdict))
E('')
E('  >> 关键：现在 tau_p 是 M_GUT 的函数')
for mult in ('0.5', '2.0'):
    v = tau_p_of(MGUT * mp.mpf(mult), AG_INV, AH_REF)
    E('     M_GUT x %-4s -> tau_p = %s yr（原实现下恒为 3.51e34，不动）'
      % (mult, mp.nstr(v, 6)))
add('M2 PASS', 'PASS', 'tau_p 已实算并恢复对 M_GUT/alpha_GUT/alpha_H 的依赖',
    'tau_p = %s yr（alpha_H=0.015）；与硬写值差 %s'
    % (mp.nstr(tp, 6), mp.nstr(mp.fabs(tp - mp.mpf('3.51e34')) / mp.mpf('3.51e34'), 3)),
    '可证伪性的最低要求已满足：改变 M_GUT 会改变 tau_p。'
    '但诚实读数是不确定性跨越实验下限两侧，故不能声称「未被排除」，只能说「与窗口重叠」')

# ============================================================
# M7：Super-K 下限
# ============================================================
E('')
E('[M7] Super-K 下限改用 2.4e34 yr')
E('-' * 78)
E('  原用 1.0e34 -> 改用 2.4e34（放宽倍数由 2.4 降为 1.0）')
E('  tau_p(中心值)/SK = %s  -> 余量仅 %s 倍'
  % (mp.nstr(tp / SK, 5), mp.nstr(tp / SK, 4)))
add('M7 PASS', 'PASS', 'Super-K 下限已改用真实值 2.4e34 yr',
    'tau_p/下限 = %s（余量 %s 倍）' % (mp.nstr(tp / SK, 4), mp.nstr(tp / SK, 4)),
    '零代价修正。修法后「恰在窗口之上」的修辞不再成立：'
    '中心值余量仅 %s 倍，而 alpha_H 不确定度本身即达数量级' % mp.nstr(tp / SK, 4))

# ============================================================
# M1：b-tau 统一由 MSSM 一阶 Yukawa RGE 实算（替代 ok=True）
# ============================================================
E('')
E('[M1] b-tau 统一：由 Yukawa RGE 实算（替代原 ok=True 写入）')
E('-' * 78)
E('  MSSM 一阶 RGE（t = ln(mu/M_Z)）：')
E('    16pi^2 dy_t/dt = y_t(6y_t^2 + y_b^2 - 13/15 g1^2 - 3 g2^2 - 16/3 g3^2)')
E('    16pi^2 dy_b/dt = y_b(6y_b^2 + y_t^2 + y_tau^2 - 7/15 g1^2 - 3 g2^2 - 16/3 g3^2)')
E('    16pi^2 dy_tau/dt = y_tau(4y_tau^2 + 3y_b^2 - 9/5 g1^2 - 3 g2^2)')
E('    16pi^2 dg_i/dt = b_i g_i^3,  b=(33/5, 1, -3)')

V = mp.mpf('246.22')
MT_POLE = mp.mpf('172.76')
MB_MB = mp.mpf('4.18')
MTAU = mp.mpf('1.77686')
K16 = 16 * pi ** 2


def yuk_init(tanb):
    """由 tan(beta) 与低能质量反推 M_Z 处 Yukawa（树级）"""
    tb = mp.mpf(tanb)
    sb = tb / mp.sqrt(1 + tb ** 2)
    cb = 1 / mp.sqrt(1 + tb ** 2)
    yt = MT_POLE * mp.sqrt(2) / (V * sb)
    yb = MB_MB * mp.sqrt(2) / (V * cb)
    ytau = MTAU * mp.sqrt(2) / (V * cb)
    return yt, yb, ytau


def deriv(y):
    yt, yb, ytau, g1, g2, g3 = y
    dyt = yt * (6 * yt ** 2 + yb ** 2 - mp.mpf(13) / 15 * g1 ** 2
                - 3 * g2 ** 2 - mp.mpf(16) / 3 * g3 ** 2) / K16
    dyb = yb * (6 * yb ** 2 + yt ** 2 + ytau ** 2 - mp.mpf(7) / 15 * g1 ** 2
                - 3 * g2 ** 2 - mp.mpf(16) / 3 * g3 ** 2) / K16
    dytau = ytau * (4 * ytau ** 2 + 3 * yb ** 2
                    - mp.mpf(9) / 5 * g1 ** 2 - 3 * g2 ** 2) / K16
    dg1 = mp.mpf(33) / 5 * g1 ** 3 / K16
    dg2 = mp.mpf(1) * g2 ** 3 / K16
    dg3 = mp.mpf(-3) * g3 ** 3 / K16
    return [dyt, dyb, dytau, dg1, dg2, dg3]


def rk4(y, h):
    k1 = deriv(y)
    y2 = [y[i] + h / 2 * k1[i] for i in range(6)]
    k2 = deriv(y2)
    y3 = [y[i] + h / 2 * k2[i] for i in range(6)]
    k3 = deriv(y3)
    y4 = [y[i] + h * k3[i] for i in range(6)]
    k4 = deriv(y4)
    return [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(6)]


g1_0 = mp.sqrt(4 * pi * a1_in)
g2_0 = mp.sqrt(4 * pi * a2_in)
g3_0 = mp.sqrt(4 * pi * a3_in)

E('')
E('  %-8s %-14s %-14s %-12s %s' % ('tan(beta)', 'y_b(M_GUT)', 'y_tau(M_GUT)', 'y_b/y_tau', 'b-tau 统一'))
BLOWUP = mp.mpf('100')     # Yukawa 超过此值判为一阶 RGE 失稳（Landau 型）
scan = []
diverged = []
for tanb in (2, 5, 10, 20, 30, 50):
    yt, yb, ytau = yuk_init(tanb)
    y = [yt, yb, ytau, g1_0, g2_0, g3_0]
    T = mp.log(MGUT / MZ)
    n = 600
    h = T / n
    blown = False
    for _ in range(n):
        y = rk4(y, h)
        if y[1] > BLOWUP or y[2] > BLOWUP:
            blown = True
            break
    if blown:
        diverged.append(tanb)
        scan.append((tanb, None, None, None, False))
        E('  %-8s %-14s %-14s %-12s %s'
          % (tanb, '>100(失稳)', '>100(失稳)', 'n/a', '一阶RGE发散'))
        continue
    ratio = y[1] / y[2]
    ok = mp.fabs(ratio - 1) < mp.mpf('0.30')
    scan.append((tanb, y[1], y[2], ratio, ok))
    E('  %-8s %-14s %-14s %-12s %s'
      % (tanb, mp.nstr(y[1], 6), mp.nstr(y[2], 6), mp.nstr(ratio, 6),
         '成立' if ok else '不成立'))

valid = [r for r in scan if r[3] is not None]
best = min(valid, key=lambda r: mp.fabs(r[3] - 1))
E('')
E('  >> 最接近统一的 tan(beta) = %s，此时 y_b/y_tau = %s'
  % (best[0], mp.nstr(best[3], 6)))
E('  >> 关键：结果依赖 tan(beta)，而 tan(beta) 是 MSSM 的自由参数')
if diverged:
    E('  >> 数值失稳：tan(beta) = %s 处一阶 Yukawa RGE 发散（y_b,y_tau 超过 100）'
      % diverged)
    E('     属一阶近似的适用边界，非本册缺陷；该区域需高阶或微扰性重估')

add('M1 PASS', 'PASS', 'b-tau 统一已实算，且暴露对 tan(beta) 的依赖',
    'tan(beta)=%s 时 y_b/y_tau=%s；有效区间内跨 %s；失稳点 %s'
    % (best[0], mp.nstr(best[3], 5),
       mp.nstr(max(r[3] for r in valid) / min(r[3] for r in valid), 4),
       diverged),
    '修法完成：不再是 ok=True 的写入式守卫。'
    '诚实发现一：b-tau 统一的成立与否依赖 tan(beta) 这一自由参数，'
    '故它不是零参数预言，原实现把该自由度完全隐藏了。'
    '诚实发现二：tan(beta)>=%s 处一阶 Yukawa RGE 数值发散，'
    '说明所谓「b-tau 统一成立」仅在有限参数区间内可谈' % (diverged[0] if diverged else 'n/a'))

# ============================================================
# 汇总
# ============================================================
E('')
E('=' * 78)
tally = {}
for e in ENTRIES:
    tally[e['verdict']] = tally.get(e['verdict'], 0) + 1
E('修法后条目 %d：' % len(ENTRIES))
for k in sorted(tally):
    E('   %-10s %d' % (k, tally[k]))
E('-' * 78)
for e in ENTRIES:
    E('  %-10s %-9s %s' % (e['code'], e['verdict'], e['title']))
E('=' * 78)
E('')
E('修法后剩余的真实内容（诚实读数）：')
E('  1. 一份正确的 MSSM 一阶 RGE 三点计算（算术无误，attack27 B01 已确认）')
E('  2. MSSM 相对 SM 三点跨度改善：9809.99 倍 -> %s 倍' % mp.nstr(spread, 5))
E('  3. b-tau 统一在 tan(beta)~%s 附近成立（依赖自由参数）' % best[0])
E('  4. tau_p ~ %s yr（数量级不确定），与 Super-K 窗口重叠' % mp.nstr(tp, 5))
E('')
E('  以上四条均为标准教科书内容（DRW 1981 / SO(10) 1974-75 / seesaw 1977-80），')
E('  本工程贡献 = 复算，不是攻破。')

out = {
    'round': 'attack27b',
    'topic': 'CUNI-v2 零代价修法（M1/M2/M4/M6/M7）修正引擎',
    'entries': ENTRIES,
    'tally': tally,
    'total': len(ENTRIES),
    'key_numbers': {
        'M12_GeV': mp.nstr(M12, 10), 'M13_GeV': mp.nstr(M13, 10),
        'M23_GeV': mp.nstr(M23, 10),
        'spread_linear': mp.nstr(spread, 8),
        'MGUT_avg_GeV': mp.nstr(MGUT, 8),
        'alpha_GUT_inv': mp.nstr(AG_INV, 8),
        'tau_p_computed_yr': mp.nstr(tp, 8),
        'SK_limit_real_yr': mp.nstr(SK, 4),
        'tau_p_over_SK': mp.nstr(tp / SK, 6),
        'btau_best_tanbeta': best[0],
        'btau_best_ratio': mp.nstr(best[3], 8),
        'btau_ratio_range': mp.nstr(max(r[3] for r in valid) / min(r[3] for r in valid), 6),
        'btau_diverged_tanbeta': diverged,
    },
    'remaining_content': [
        'MSSM 一阶 RGE 三点计算（算术正确）',
        'MSSM 相对 SM 收敛改善 %s 倍' % mp.nstr(mp.mpf('9809.99') / spread, 6),
        'b-tau 统一依赖于自由参数 tan(beta)',
        'tau_p 与 Super-K 窗口重叠（非「未被排除」）',
    ],
    'verdict': '修法执行完毕；剩余内容为标准教科书复算，非本工程新增',
    'exit_code': 0,
}
with io.open(os.path.join(BASE, 'attack27b_力的大统一方程_零代价修法修正引擎_2026-10-30.json'),
             'w', encoding='utf-8') as fh:
    fh.write(json.dumps(out, ensure_ascii=False, indent=1))
E('')
E('产物已写出：attack27b_...json')
sys.exit(0)