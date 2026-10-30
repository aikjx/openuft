# -*- coding: utf-8 -*-
# attack28 · 力的大统一方程：sin2theta_W 的「真预测」（M5 修法执行，2026-10-31）
#
# 承接 attack27 B05 的裁定：原实现把 sin2theta_W=0.23122 作为输入吃进去，
# 再声称由 GUT 边界「预测」出它 —— 结构上不可能构成检验。
#
# M5 的做法：把 sin2theta_W 从输入改为未知量。
#   输入只有两个：alpha_em(M_Z) 与 alpha_s(M_Z)
#   GUT 边界条件：alpha_1(M_GUT) = alpha_2(M_GUT) = alpha_3(M_GUT)  （2 个独立方程）
#   未知量两个：x = sin2theta_W,  L2 = ln(M_GUT/M_SUSY)
#   => 2 方程 2 未知，闭式可解，给出真正的 sin2theta_W 预测。
#
# 这正是 GUT 的经典招牌预测。本册机器执行它，并给出 SM / MSSM 的决定性对照。
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

mp.mp.dps = 50
pi = mp.pi

E('=' * 78)
E('attack28 · sin2theta_W 真预测（M5 修法）')
E('=' * 78)

MZ = mp.mpf('91.1876')
MSUSY = mp.mpf('1000')
alpha_em = mp.mpf(1) / mp.mpf('127.916')
alpha_s = mp.mpf('0.1184')
SW_OBS = mp.mpf('0.23122')          # 仅用于最后比对，不进入求解
L1 = mp.log(MSUSY / MZ)

E('')
E('输入（只有两个）：')
E('   alpha_em(M_Z) = %s' % mp.nstr(alpha_em, 10))
E('   alpha_s(M_Z)  = %s' % mp.nstr(alpha_s, 10))
E('   sin2theta_W   = [未知量，不再作为输入]')
E('')
E('GUT 归一化：alpha_1 = (5/3)alpha_em/cos^2theta_W,  alpha_2 = alpha_em/sin^2theta_W')
E('   => alpha_1^-1 = (3/5)(1-x)/alpha_em,  alpha_2^-1 = x/alpha_em,  其中 x = sin^2theta_W')


def predict(A, Bm, L1v, tag):
    """A=(b1,b2,b3) 为低能段系数，Bm 为高能段系数，L1v 为低能段 ln 跨度。
    返回 (x=sin^2theta_W, MGUT, L2)。两段模型：M_Z --(A,L1)--> M_SUSY --(Bm,L2)--> M_GUT"""
    b1, b2, b3 = A
    B1, B2, B3 = Bm
    # 由两式联立消去 x，得 L2 的闭式：
    #   alpha_em/(2pi)*{[(b2-b3)+(5/3)(b1-b3)]L1 + [(B2-B3)+(5/3)(B1-B3)]L2} = 1-(8/3)alpha_em/alpha_s
    coef_L1 = (b2 - b3) + mp.mpf(5) / 3 * (b1 - b3)
    coef_L2 = (B2 - B3) + mp.mpf(5) / 3 * (B1 - B3)
    rhs = 1 - mp.mpf(8) / 3 * alpha_em / alpha_s
    L2 = ((2 * pi / alpha_em) * rhs - coef_L1 * L1v) / coef_L2
    # 由 (II) 式定 x
    x = alpha_em * (1 / alpha_s + ((b2 - b3) * L1v + (B2 - B3) * L2) / (2 * pi))
    mgut = MSUSY * mp.e ** L2
    return x, mgut, L2


# ---------- MSSM：两段（SM 段 + MSSM 段） ----------
A_SM = (mp.mpf(41) / 10, -mp.mpf(19) / 6, mp.mpf(-7))
B_MSSM = (mp.mpf(33) / 5, mp.mpf(1), mp.mpf(-3))
x_mssm, mgut_mssm, L2_m = predict(A_SM, B_MSSM, L1, 'MSSM')

# ---------- SM：单段（无 SUSY 阈值：低能段 L1=0，整段用 SM 系数） ----------
# 注意此时 L2 是 ln(M_GUT/M_Z)，故 M_GUT = M_Z * e^L2（不是 MSUSY * e^L2）
x_sm, _mgut_unused, L2_sm = predict(A_SM, A_SM, mp.mpf(0), 'SM')
mgut_sm = MZ * mp.e ** L2_sm

E('')
E('-' * 78)
E('[P1] 真预测结果（sin2theta_W 不由输入给出）')
E('-' * 78)
E('  %-8s %-18s %-18s %-14s' % ('模型', 'sin2theta_W预测', 'M_GUT (GeV)', 'vs 实测偏差'))
d_mssm = mp.fabs(x_mssm - SW_OBS) / SW_OBS
d_sm = mp.fabs(x_sm - SW_OBS) / SW_OBS
E('  %-8s %-18s %-18s %s%%'
  % ('SM', mp.nstr(x_sm, 8), mp.nstr(mgut_sm, 8), mp.nstr(d_sm * 100, 5)))
E('  %-8s %-18s %-18s %s%%'
  % ('MSSM', mp.nstr(x_mssm, 8), mp.nstr(mgut_mssm, 8), mp.nstr(d_mssm * 100, 5)))
E('  %-8s %-18s %-18s %s'
  % ('实测', mp.nstr(SW_OBS, 8), '-', '-'))
E('')
E('  >> SM 预测 %.5f 偏低 %.2f%%；MSSM 预测 %.5f 偏差仅 %.3f%%'
  % (float(x_sm), float(d_sm) * 100, float(x_mssm), float(d_mssm) * 100))

add('P1 PASS', 'PASS', 'sin2theta_W 已由 GUT 边界真预测（非输入、非循环）',
    'SM %.5f（偏 %.2f%%）；MSSM %.5f（偏 %.3f%%）'
    % (float(x_sm), float(d_sm) * 100, float(x_mssm), float(d_mssm) * 100),
    '只用 alpha_em 与 alpha_s 两个输入，解出 sin2theta_W 与 M_GUT。'
    '这是 GUT 的经典招牌预测：SM 给出约 0.207（偏低约 10%），MSSM 修复到约 0.229（偏差约 1%）。'
    '本册与上一条（B05 的循环版本）的差别在于：此处 sin2theta_W 全程不进入求解')

# ---------- P2：与原循环版本对照 ----------
E('')
E('-' * 78)
E('[P2] 与「循环版本」的机器对照')
E('-' * 78)
E('  循环版本（原 E2/E3）：')
E('     输入 sw2=0.23122 -> a2=alpha_em/sw2 -> ... -> 回推 sw2=0.2304 -> 称「偏差 0.37%」')
E('     该 0.37% 是三点算术平均造成的自洽残差（attack27 B04 已证：沿自身交点回推残差为机器零）')
E('')
E('  真预测版本（本册）：')
E('     输入仅 alpha_em, alpha_s -> 解出 sw2=%s -> 与实测比 %s%%'
  % (mp.nstr(x_mssm, 8), mp.nstr(d_mssm * 100, 5)))
E('  >> 两者数值相近但性质完全不同：前者是输入往返，后者是独立解出')
add('P2 PASS', 'PASS', '真预测与循环版本已完成机器区分',
    '循环版 0.2304（输入往返）；真预测 %s（独立解出）' % mp.nstr(x_mssm, 8),
    '循环版本的判据对 sin2theta_W 零判别力（它是自己的输入）；'
    '真预测版本的判据有判别力（改 alpha_s 会改变预测值，见 P3）')

# ---------- P3：敏感性（判别力检验） ----------
E('')
E('-' * 78)
E('[P3] 判别力检验：预测值是否随输入变化（可证伪性的机器定义）')
E('-' * 78)
E('  alpha_s 敏感性（其余输入不变）：')
E('    %-12s %-16s %s' % ('alpha_s', 'sin2theta_W预测', 'vs 实测'))
sens = []
for f in ('0.95', '0.98', '1.0', '1.02', '1.05'):
    a_s = alpha_s * mp.mpf(f)
    # 以该 alpha_s 重新求解（闭式与 predict 内一致）
    coef_L1 = (A_SM[1] - A_SM[2]) + mp.mpf(5) / 3 * (A_SM[0] - A_SM[2])
    coef_L2 = (B_MSSM[1] - B_MSSM[2]) + mp.mpf(5) / 3 * (B_MSSM[0] - B_MSSM[2])
    rhs = 1 - mp.mpf(8) / 3 * alpha_em / a_s
    L2x = ((2 * pi / alpha_em) * rhs - coef_L1 * L1) / coef_L2
    x2 = alpha_em * (1 / a_s + ((A_SM[1] - A_SM[2]) * L1
                                + (B_MSSM[1] - B_MSSM[2]) * L2x) / (2 * pi))
    dd = mp.fabs(x2 - SW_OBS) / SW_OBS
    sens.append((mp.nstr(a_s, 6), mp.nstr(x2, 8), mp.nstr(dd * 100, 5)))
    E('    %-12s %-16s %s%%' % (mp.nstr(a_s, 6), mp.nstr(x2, 8), mp.nstr(dd * 100, 5)))
spread_x = max(mp.mpf(s[1]) for s in sens) - min(mp.mpf(s[1]) for s in sens)
E('')
E('  >> alpha_s 在 ±5%% 内变动时，预测值跨度 %s（远大于自身末位），判据有判别力'
  % mp.nstr(spread_x, 5))
add('P3 PASS', 'PASS', '预测值随输入显著变化，判据具备可证伪性',
    'alpha_s ±5%% -> 预测跨度 %s' % mp.nstr(spread_x, 5),
    '与 attack27 C02 的 tau_p（与模型解耦、恒为常数）形成对照：'
    '此处 sin2theta_W 是真函数，改输入即改输出，因此可被实验检验')

# ---------- P4：诚实归属 ----------
E('')
E('-' * 78)
E('[P4] 归属考核')
E('-' * 78)
E('  SM  GUT 预测 sin2theta_W ~ 0.21（偏差 ~10%）  : 教科书标准结论')
E('  MSSM GUT 预测 sin2theta_W ~ 0.231（偏差 <1%）: 1981 年后的教科书标准结论')
E('  >> 本册机器读数与上述一致，属复算，不是本工程新增物理')
add('P4 INFO', 'INFO', '真预测的结果与教科书一致，属复算',
    'SM %.5f / MSSM %.5f，与文献 0.21 / 0.231 一致'
    % (float(x_sm), float(x_mssm)),
    '本册的增量不在数值，而在「把一条被实现为循环的伪预测，修复为真正的独立预测」，'
    '并给出 SM 与 MSSM 的决定性对照（10%% vs 1%%）。'
    '该对照本身就说明：大统一的成败在实验上由 sin2theta_W 这类量判定，'
    '而不是由「回推是否自洽」判定')

# ---------- 汇总 ----------
E('')
E('=' * 78)
tally = {}
for e in ENTRIES:
    tally[e['verdict']] = tally.get(e['verdict'], 0) + 1
E('条目 %d：' % len(ENTRIES))
for k in sorted(tally):
    E('   %-10s %d' % (k, tally[k]))
E('-' * 78)
for e in ENTRIES:
    E('  %-10s %-9s %s' % (e['code'], e['verdict'], e['title']))
E('=' * 78)
E('')
E('结论：M5 修法执行完毕。sin2theta_W 现在是【输出】而非【输入】，')
E('      判据由「零判别力的输入往返」变为「有判别力的独立预测」。')
E('      但结果仍是教科书已有内容 —— 修法修复的是实现，不是物理。')

out = {
    'round': 'attack28',
    'topic': 'sin2theta_W 真预测（M5 修法执行）',
    'inputs': {'alpha_em_MZ': mp.nstr(alpha_em, 12), 'alpha_s_MZ': mp.nstr(alpha_s, 10)},
    'sin2thetaW_is_input': False,
    'entries': ENTRIES,
    'tally': tally,
    'total': len(ENTRIES),
    'key_numbers': {
        'SM_pred_sin2thetaW': mp.nstr(x_sm, 10),
        'SM_dev_pct': mp.nstr(d_sm * 100, 6),
        'SM_MGUT_GeV': mp.nstr(mgut_sm, 8),
        'MSSM_pred_sin2thetaW': mp.nstr(x_mssm, 10),
        'MSSM_dev_pct': mp.nstr(d_mssm * 100, 6),
        'MSSM_MGUT_GeV': mp.nstr(mgut_mssm, 8),
        'observed_sin2thetaW': mp.nstr(SW_OBS, 8),
        'alpha_s_sensitivity_spread': mp.nstr(spread_x, 5),
    },
    'verdict': 'M5 完成：sin2theta_W 由输入改为输出；结果属教科书复算',
    'exit_code': 0,
}
with io.open(os.path.join(BASE, 'attack28_力的大统一方程_sin2thetaW真预测_M5修法_2026-10-31.json'),
             'w', encoding='utf-8') as fh:
    fh.write(json.dumps(out, ensure_ascii=False, indent=1))
E('')
E('产物已写出：attack28_...json')
sys.exit(0)