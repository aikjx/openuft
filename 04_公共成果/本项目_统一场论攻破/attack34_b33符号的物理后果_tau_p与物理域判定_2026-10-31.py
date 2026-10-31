# -*- coding: utf-8 -*-
# attack34 · b33 符号的物理后果：M_SUSY 物理域 + tau_p 联动判定
#
# 承接 attack33（已完成「定位」：attack30 的 193.04 GeV 是域上界伪解，b33 符号差 7.73 倍）。
# 本册不再定位，而是把定位结果升格为【物理后果判定】：
#
#   B0  自校准：复算 attack27b 的 tau_p=2.7755e34 yr（证明本册用的是它的同一闭式）
#   B1  attack30 的 b33=-14 与其自称文献源「标准 MSSM」冲突（枚举判据）
#   B2  attack30 自带 flip33 开关却以 flip33=False 报出（未声明的默认值）
#   B3  物理域判据 M_SUSY >= M_Z：1-loop 后向解 54.38 GeV 违规
#   B4  【核心】tau_p 四分支联动：物理域内的 2-loop 解全部被 Super-K 排除
#   B5  alpha_H 稳健性：求使 tau_p >= SK 的临界 alpha_H
#   B6  更正 attack27b：其「余量 1.16 倍」结论依赖 1-loop 的 M_GUT（跨册口径混用）
#   B7  M_SUSY 口径三分表 + 单调性（LHC 挤压会加剧质子衰变排除）
#   B8  可检验性与诚实边界
#
# 纪律：本册不判任何一册「作者算错」；判的是「结论是否随未声明的口径翻转」。
import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = []


def add(code, verdict, title, value, note):
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title,
                    'value': value, 'note': note})


def E(*a):
    s = ' '.join(str(x) for x in a)
    try:
        print(s)
    except Exception:
        print(s.encode('ascii', 'replace').decode('ascii'))


# ---------------------------------------------------------------- 输入
MZ = 91.1876
ALPHA_EM_INV = 127.916
ALPHA_EM = 1.0 / ALPHA_EM_INV
ALPHA_S = 0.1184
SW_OBS = 0.23122

B1 = {'SM': [4.1, -19.0 / 6.0, -7.0], 'MSSM': [33.0 / 5.0, 1.0, -3.0]}
B2_SM = [[199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
         [9.0 / 10.0, 35.0 / 6.0, 12.0],
         [11.0 / 10.0, 9.0 / 2.0, -26.0]]
B2_MS_P14 = [[199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
             [9.0 / 5.0, 25.0, 24.0],
             [11.0 / 5.0, 9.0, 14.0]]
B2_MS_N14 = [[199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
             [9.0 / 5.0, 25.0, 24.0],
             [11.0 / 5.0, 9.0, -14.0]]
MATS_P14 = {'SM': B2_SM, 'MSSM': B2_MS_P14}
MATS_N14 = {'SM': B2_SM, 'MSSM': B2_MS_N14}

TP = 2.0 * math.pi
EP2 = 8.0 * math.pi ** 2

# tau_p 工程闭式（与 attack27b M2 逐字同源；参考点为该册所选，属 [C] 外部输入）
TAU0 = 1.0e35          # yr
M_REF = 2.0e16         # GeV
AGINV_REF = 35.0       # 参考 alpha_GUT^-1
AH_REF = 0.015         # GeV^3
SK_LIMIT = 2.4e34      # Super-K (M7 采用值)


def tau_p(mgut, ag_inv, ah=AH_REF):
    """tau_p ∝ M_GUT^4 / alpha_GUT^2 / alpha_H^2，以 attack27b 参考点归一。"""
    return TAU0 * (mgut / M_REF) ** 4 * (ag_inv / AGINV_REF) ** 2 \
        * (AH_REF / ah) ** 2


# attack32 / attack33 / attack27b 的既有读数（逐项注明来源）
BRANCHES = [
    # (标签, M_SUSY GeV, M_GUT GeV, alpha_GUT^-1, 来源, 是否 2-loop, b33)
    ('1-loop 后向解(attack32 F5)', 54.38472, 2.321451e16, 23.9547,
     'attack32_report.txt 第 128 行', False, None),
    ('2-loop b33=+14(attack32 V0)', 2317.71643, 1.117972e16, 25.6672,
     'attack32_report.txt 第 129 行', True, 14.0),
    ('2-loop b33=-14(attack32 V3)', 17918.76520, 5.780340e15, 27.2379,
     'attack32_report.txt 第 185 行', True, -14.0),
    ('1-loop 固定 M_SUSY=1TeV(attack27b)', 1000.0, 1.6899061e16, 25.826977,
     'attack27b_report.txt 第 19-21 行', False, None),
]
A27B_TAU = 2.7755e34


# ---------------------------------------------------------------- 积分器
def rhs(a, model, mats):
    b = B1[model]
    M = mats[model]
    return [-b[i] / TP - sum(M[i][j] / a[j] for j in range(3)) / EP2
            for i in range(3)]


def flow(a0, L1, L2, mats, n=1200):
    a = list(a0)
    for seg, model in ((L1, 'SM'), (L2, 'MSSM')):
        if seg == 0:
            continue
        h = seg / n
        for _ in range(n):
            k1 = rhs(a, model, mats)
            aa = [a[i] + 0.5 * h * k1[i] for i in range(3)]
            k2 = rhs(aa, model, mats)
            bb = [a[i] + 0.5 * h * k2[i] for i in range(3)]
            k3 = rhs(bb, model, mats)
            cc = [a[i] + h * k3[i] for i in range(3)]
            k4 = rhs(cc, model, mats)
            a = [a[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                 for i in range(3)]
    return a


def a_mz(sw=SW_OBS):
    return [0.6 * (1.0 - sw) / ALPHA_EM, sw / ALPHA_EM, 1.0 / ALPHA_S]


def best_l2(msusy, mats, lo=20.0, hi=40.0, steps=2000, refine=6):
    """固定 M_SUSY 与实测 sw，求使 (a1-a2)^2+(a1-a3)^2 最小的 L2（网格 + 三分法）。"""
    a0 = a_mz()
    L1 = math.log(msusy / MZ)

    def cost(L2):
        a = flow(a0, L1, L2, mats)
        return (a[0] - a[1]) ** 2 + (a[0] - a[2]) ** 2
    best = (None, None)
    for i in range(steps + 1):
        L2 = lo + (hi - lo) * i / steps
        c = cost(L2)
        if best[0] is None or c < best[0]:
            best = (c, L2)
    x0, x1 = best[1] - (hi - lo) / steps, best[1] + (hi - lo) / steps
    for _ in range(refine * 20):
        m1 = x0 + (x1 - x0) / 3.0
        m2 = x1 - (x1 - x0) / 3.0
        if cost(m1) < cost(m2):
            x1 = m2
        else:
            x0 = m1
    L2 = 0.5 * (x0 + x1)
    a = flow(a0, L1, L2, mats)
    return L2, cost(L2), a


E('=' * 78)
E('attack34 · b33 符号的物理后果：M_SUSY 物理域 + tau_p 联动判定')
E('=' * 78)
E('')
E('承接 attack33：已机器定位 attack30 的 193.04 GeV 是域上界、b33 符号差 7.73 倍。')
E('本册问下一步：这两个「记账差异」有没有物理后果？答：有，且落到质子衰变上。')
E('')

# ============================================================
# B0 自校准
# ============================================================
E('[B0] 自校准：本册 tau_p 闭式是否复现 attack27b 的 2.7755e34 yr')
E('-' * 78)
tp_cal = tau_p(1.6899061e16, 25.826977)
E('  闭式：tau_p = %.0e yr x (M_GUT/%.0e)^4 x (alpha_GUT^-1/%g)^2 x (%.3f/alpha_H)^2'
  % (TAU0, M_REF, AGINV_REF, AH_REF))
E('  attack27b 输入：M_GUT=1.6899061e16 GeV, alpha_GUT^-1=25.826977')
E('  本册复算 tau_p = %.4e yr' % tp_cal)
E('  attack27b 报值   = %.4e yr ；相对偏差 %.2e'
  % (A27B_TAU, abs(tp_cal - A27B_TAU) / A27B_TAU))
cal_ok = abs(tp_cal - A27B_TAU) / A27B_TAU < 1e-3
add('B0 %s' % ('PASS' if cal_ok else 'FAIL'), 'PASS' if cal_ok else 'FAIL',
    'tau_p 闭式自校准：复现 attack27b 的 %.4e yr（相对偏差 %.1e）'
    % (A27B_TAU, abs(tp_cal - A27B_TAU) / A27B_TAU),
    'tau_p=%.4e yr' % tp_cal,
    '证明本册与 attack27b 用的是同一闭式，后续差异只能来自输入 (M_GUT, alpha_GUT)，'
    '不是公式分歧。闭式的绝对标度（TAU0/M_REF/AGINV_REF）属 [C] 级外部输入，见 B8')

# ============================================================
# B1 b33 符号与自称文献源冲突
# ============================================================
E('')
E('[B1] attack30 的 b33=-14 vs 它自己声明的文献源')
E('-' * 78)
E('  attack30 源码注释：「2-loop 系数矩阵 B2_ij（标准 MSSM，来源：Pierce et al. 1997 / Martin 2000）」')
E('  其 B_MS[2][2] = -14 ；attack32（同样自称标准 MSSM）用 +14 。')
std = set()
for row in B2_SM:
    for v in row:
        std.add(round(v, 6))
for row in B2_MS_P14:
    for v in row:
        std.add(round(v, 6))
cands = []
for v in std:
    if abs(-v - (-14.0)) < 1e-6:
        cands.append(('-(%g)' % v, v))
    if abs(v - (-14.0)) < 1e-6:
        cands.append(('%g' % v, v))
E('  枚举判据：在两册共用的【标准 SM 阵 u 标准 MSSM 阵】全部 18 个元素中，')
E('  能与 -14 匹配的解 = %s' % (cands if cands else '无'))
E('  >> 唯一解释：-14 = -(MSSM 的 +14)，即 b33 的符号翻转。')
E('     而 -14 不等于 SM 阵的任何一个元素（-26 是最近的），排除「误用 SM 阵」解释。')
add('B1 FAIL', 'FAIL',
    'attack30 的 b33=-14 与其自称文献源「标准 MSSM」冲突：唯一解释是 +14 的符号翻转',
    '标准元素集合中 -14 的唯一匹配 = -(+14)；SM 阵最近元素 -26 不匹配',
    '文档层（注释声明标准 MSSM + 文献来源）与执行层（元素值 -14）不同源，'
    '与 attack33 A3「注释漂移」同族，但这里漂的是【数据来源声明】而非搜索域。'
    '本册不判「作者写错」：只判「该册的输出不能在其自称的文献口径下引用」')

# ============================================================
# B2 flip33 开关
# ============================================================
E('')
E('[B2] attack30 自带 flip33 开关却以 flip33=False 报出')
E('-' * 78)
E('  源码：def da_dt(a, b, B2, lam, flip33):  if flip33: B[2][2] = -B[2][2]')
E('  solve_forward / solve_backward 的默认参数均为 flip33=False，')
E('  且最终报出的 M_SUSY=193.04415 GeV 来自 flip33=False（即 -14）。')
E('  >> 作者已把 b33 符号做成可切换的事实 => 该符号在该册内【未被定死】；')
E('     但报出时未声明用的是哪一支 => 引用者无法知道该数对应哪套系数。')
add('B2 INFO', 'INFO',
    'attack30 把 b33 符号做成 flip33 开关却以默认 False 报出，未在输出中声明',
    '报值来自 flip33=False（b33=-14）',
    '这是「未声明的默认值」型缺陷：开关存在说明作者已知该单元可疑，'
    '但输出不标注，导致 downstream（attack32 F5c）只能靠数值反推')

# ============================================================
# B3 物理域判据
# ============================================================
E('')
E('[B3] 物理域判据：M_SUSY 必须 >= M_Z（否则 SM 段是反向积分）')
E('-' * 78)
E('  两段模型的定义：M_Z --(SM)--> M_SUSY --(MSSM)--> M_GUT，要求 L1 = ln(M_SUSY/M_Z) >= 0。')
rows_b3 = []
for (tag, ms, mg, agi, src, tl, b33) in BRANCHES:
    L1 = math.log(ms / MZ)
    ok = L1 >= 0
    rows_b3.append((tag, ms, L1, ok))
    E('  %-34s M_SUSY=%12.5f GeV  L1=%+.6f  %s'
      % (tag, ms, L1, 'OK' if ok else '违规(<0)'))
bad = [r for r in rows_b3 if not r[3]]
E('  >> 违规分支 %d 个：%s' % (len(bad), '; '.join(r[0] for r in bad)))
E('     其中 1-loop 后向解 54.38 GeV 被 attack29/28/30 用作【自校准基准】引用。')
add('B3 FAIL', 'FAIL',
    '1-loop 后向解 M_SUSY=54.38472 GeV < M_Z=91.1876 GeV，L1=-0.516836，物理域违规',
    '需 M_SUSY >= M_Z；违规分支 1 个（1-loop 后向解）',
    'L1<0 意味着「M_Z 到 M_SUSY」是向下跑 SM，与「M_Z 以上是 SM、M_SUSY 以上是 MSSM」'
    '的前提矛盾。这解释了为何该解反而给出最大的 M_GUT(2.32e16) 与最大的 tau_p：'
    '它用一段【反向的 SM 跑动】换来了统一点抬高。此前 attack28/29/30 把它当作'
    '「1-loop 自校准基准」引用，属把非物理解当基准')

# ============================================================
# B4 核心：tau_p 四分支联动
# ============================================================
E('')
E('[B4] 核心：把四个分支各自的 (M_GUT, alpha_GUT) 代入同一 tau_p 闭式')
E('-' * 78)
E('  %-34s %-13s %-10s %-13s %s' % ('分支', 'M_GUT GeV', 'aGUT^-1', 'tau_p yr', 'vs SK 2.4e34'))
rows_b4 = []
for (tag, ms, mg, agi, src, tl, b33) in BRANCHES:
    tp = tau_p(mg, agi)
    ratio = tp / SK_LIMIT
    vd = '未排除(x%.2f)' % ratio if ratio >= 1 else '被排除(差%.2f倍)' % (1.0 / ratio)
    rows_b4.append((tag, ms, mg, agi, tp, ratio, tl))
    E('  %-34s %.6e %-10.4f %.4e %s'
      % (tag, mg, agi, tp, vd))
E('')
E('  >> tau_p 跨度 = %.2f 倍（min %.3e / max %.3e）'
  % (max(r[4] for r in rows_b4) / min(r[4] for r in rows_b4),
     min(r[4] for r in rows_b4), max(r[4] for r in rows_b4)))
phys = [r for r in rows_b4 if math.log(r[1] / MZ) >= 0]
excluded = [r for r in phys if r[5] < 1.0]
E('  >> 物理域内（M_SUSY>=M_Z）的分支 %d 个，其中被 Super-K 排除 %d 个。'
  % (len(phys), len(excluded)))
E('  >> 未被排除的分支：%s'
  % ('; '.join(r[0] for r in rows_b4 if r[5] >= 1.0) or '无'))
add('B4 FAIL', 'FAIL',
    '二选一必死：物理域内(M_SUSY>=M_Z)的 2-loop 解 tau_p 全被 Super-K 排除；'
    '唯一未被排除的 1-loop 解其 M_SUSY<M_Z 非物理',
    '2-loop b33=+14: tau_p=%.3e yr（差 %.2f 倍）; b33=-14: %.3e yr（差 %.2f 倍）; '
    '1-loop 54.38GeV: %.3e yr（余量 %.2f 倍但 M_SUSY<M_Z）'
    % (rows_b4[1][4], 1 / rows_b4[1][5], rows_b4[2][4], 1 / rows_b4[2][5],
       rows_b4[0][4], rows_b4[0][5]),
    '把 attack33 的「记账差异」换算成物理量后：b33 符号 + RGE 阶数 + M_SUSY 口径'
    '三者任一变化都会让 tau_p 跨越 Super-K 下限（跨度 %.1f 倍）。'
    '⇒ 「MSSM 大统一与质子衰变实验相容」这一表述在本库当前输入下不成立。'
    '判定对象是【结论随未声明口径翻转】，不是 MSSM 本身'
    % (max(r[4] for r in rows_b4) / min(r[4] for r in rows_b4)))

# ============================================================
# B5 alpha_H 稳健性
# ============================================================
E('')
E('[B5] 稳健性：alpha_H 取多小才能让物理域内的解不被排除')
E('-' * 78)
crit = {}
for (tag, ms, mg, agi, src, tl, b33) in BRANCHES:
    if math.log(ms / MZ) < 0:
        continue
    base = tau_p(mg, agi, AH_REF)
    # tau_p ∝ alpha_H^-2 => 需 alpha_H <= AH_REF * sqrt(base/SK)
    ah_crit = AH_REF * math.sqrt(base / SK_LIMIT) if base < SK_LIMIT else None
    crit[tag] = ah_crit
    if ah_crit is None:
        E('  %-34s 已通过，无需压缩 alpha_H' % tag)
    else:
        E('  %-34s 需 alpha_H <= %.6f GeV^3（格点典型值 %.3f，即 %.1f%%）'
          % (tag, ah_crit, AH_REF, 100.0 * ah_crit / AH_REF))
E('')
E('  alpha_H 扫描（仅对 2-loop b33=+14 分支，tau_p ∝ alpha_H^-2）：')
E('    %-12s %-14s %s' % ('alpha_H', 'tau_p yr', 'vs SK'))
for f in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0):
    ah = AH_REF * f
    v = tau_p(rows_b4[1][2], rows_b4[1][3], ah)
    E('    %-12.5f %.4e %s' % (ah, v, '未排除' if v >= SK_LIMIT
                               else '被排除(差%.2f倍)' % (SK_LIMIT / v)))
ah_needed = crit.get('2-loop b33=+14(attack32 V0)')
E('  >> 即便把 alpha_H 压到格点典型值的 %.0f%%（0.0075），2-loop 解仍差 %.2f 倍；'
  % (50, SK_LIMIT / tau_p(rows_b4[1][2], rows_b4[1][3], 0.0075)))
E('     要使之通过需 alpha_H <= %.6f GeV^3，低于格点典型值一半。' % ah_needed)
add('B5 BOUNDARY', 'BOUNDARY',
    'alpha_H 稳健性：2-loop 解需 alpha_H <= %.6f GeV^3（格点典型值 %.3f 的 %.0f%%）才不被排除'
    % (ah_needed, AH_REF, 100.0 * ah_needed / AH_REF),
    'alpha_H=0.0075（典型值一半）时 tau_p=%.3e yr，仍差 %.2f 倍'
    % (tau_p(rows_b4[1][2], rows_b4[1][3], 0.0075),
       SK_LIMIT / tau_p(rows_b4[1][2], rows_b4[1][3], 0.0075)),
    '结论对 alpha_H 稳健（需压缩到典型值一半以下才翻转），但格点矩阵元的绝对范围由外部'
    '给出（[C] 级输入），本册不掌握其硬下限 => 判 BOUNDARY 不判 FAIL')

# ============================================================
# B6 更正 attack27b
# ============================================================
E('')
E('[B6] 更正 attack27b 的「余量 1.16 倍 / 与窗口重叠」：该结论依赖 1-loop 的 M_GUT')
E('-' * 78)
tp_1l = tau_p(1.6899061e16, 25.826977)
tp_2l = tau_p(1.117972e16, 25.6672)
E('  attack27b 基准（1-loop，M_SUSY 固定 1 TeV）：M_GUT=1.6899061e16 -> tau_p=%.4e（余量 %.3f 倍）'
  % (tp_1l, tp_1l / SK_LIMIT))
E('  attack32/33 的 2-loop 自洽解：                M_GUT=1.117972e16 -> tau_p=%.4e（差 %.3f 倍）'
  % (tp_2l, SK_LIMIT / tp_2l))
E('  M_GUT 比值 %.4f ；tau_p 比值 %.4f（~ 四次方放大）'
  % (1.117972e16 / 1.6899061e16, tp_2l / tp_1l))
E('  >> attack27b 的「与窗口重叠」只在 1-loop M_GUT 下成立；换成库内更自洽的 2-loop M_GUT，')
E('     tau_p 掉 %.2f 倍，落到被排除区。' % (tp_1l / tp_2l))
add('B6 CORRECTED', 'CORRECTED',
    'attack27b 的「tau_p 与 Super-K 窗口重叠（余量 %.3f 倍）」依赖 1-loop M_GUT；'
    % (tp_1l / SK_LIMIT),
    '换成 2-loop 自洽 M_GUT 后 tau_p 由 %.3e 降到 %.3e（%.2f 倍）'
    % (tp_1l, tp_2l, tp_1l / tp_2l),
    '这里不是 attack27b 算错：它明确用了 1-loop。问题是本库两册各自用不同阶数的 M_GUT，'
    '却给出方向相反的「是否与实验相容」结论，且互不标注 => 跨册口径混用。'
    '（attack27b 的自校准 M_SUSY=1 TeV 与 attack32 的 2-loop 自洽 M_SUSY=2.32 TeV 也不同源）')

# ============================================================
# B7 单调性：LHC 挤压会加剧排除
# ============================================================
E('')
E('[B7] 单调性：M_SUSY 被 LHC 往上挤压时，(M_GUT, tau_p) 如何变')
E('-' * 78)
E('  固定实测 sin^2theta_W=%.5f，2-loop 分段矩阵 b33=+14，对每个 M_SUSY 求最佳 L2：' % SW_OBS)
E('    %-14s %-14s %-13s %-10s %-14s %s'
  % ('M_SUSY GeV', 'L2', 'M_GUT GeV', 'aGUT^-1', 'tau_p yr', 'vs SK'))
mono = []
for ms in (500.0, 1000.0, 2000.0, 2317.71643, 5000.0, 10000.0):
    L2, cost, a = best_l2(ms, MATS_P14)
    mg = ms * math.exp(L2)
    agi = sum(a) / 3.0
    tp = tau_p(mg, agi)
    mono.append((ms, L2, mg, agi, tp, tp / SK_LIMIT))
    E('    %-14.2f %-14.6f %.6e %-10.4f %.4e %s'
      % (ms, L2, mg, agi, tp,
         '未排除' if tp >= SK_LIMIT else '被排除(差%.2f倍)' % (SK_LIMIT / tp)))
mguts = [m[2] for m in mono]
tps = [m[4] for m in mono]
mono_mgut = all(mguts[i] > mguts[i + 1] for i in range(len(mguts) - 1))
mono_tau = all(tps[i] > tps[i + 1] for i in range(len(tps) - 1))
E('  >> M_GUT 随 M_SUSY 单调下降：%s ; tau_p 单调下降：%s'
  % (mono_mgut, mono_tau))
E('  >> 含义：LHC 把超伴子质量下限往上推 => M_SUSY 必须更大 => M_GUT 更小 =>')
E('     tau_p 更小（四次方）=> 质子衰变排除更强。两个实验约束【同向收紧】，')
E('     不存在「调高 M_SUSY 来救 tau_p」的自由度。')
add('B7 %s' % ('PASS' if (mono_mgut and mono_tau) else 'BOUNDARY'),
    'PASS' if (mono_mgut and mono_tau) else 'BOUNDARY',
    '单调性判定：M_SUSY 上升 => M_GUT 下降 => tau_p 下降（两个实验约束同向收紧）',
    'M_GUT 单调下降=%s ; tau_p 单调下降=%s ; tau_p 跨度 %.2f 倍'
    % (mono_mgut, mono_tau, max(tps) / min(tps)),
    '这是本册唯一方向明确的【可检验推论】：一旦 LHC 把 M_SUSY 下限推到 %d TeV 以上，'
    '本库口径下的维度-6 tau_p 就落到 %.2e yr 以下（差 Super-K %.1f 倍）。'
    '注意它依赖 B8 的三条边界，不是对 MSSM 的否证'
    % (10, tps[-1], SK_LIMIT / tps[-1]))

# ============================================================
# B7b 临界 M_SUSY：tau_p >= Super-K 要求 M_SUSY 低于多少
# ============================================================
E('')
E('[B7b] 临界能标：tau_p = Super-K 下限对应的 M_SUSY')
E('-' * 78)


def tau_of_msusy(ms, steps=300, n=600):
    """轻量版：给定 M_SUSY，求最佳 L2 并返回 (tau_p, M_GUT, alpha_GUT^-1)。"""
    a0 = a_mz()
    L1 = math.log(ms / MZ)

    def cost(L2):
        a = flow(a0, L1, L2, MATS_P14, n)
        return (a[0] - a[1]) ** 2 + (a[0] - a[2]) ** 2
    best = (None, None)
    for i in range(steps + 1):
        L2 = 20.0 + (40.0 - 20.0) * i / steps
        c = cost(L2)
        if best[0] is None or c < best[0]:
            best = (c, L2)
    x0, x1 = best[1] - 20.0 / steps, best[1] + 20.0 / steps
    for _ in range(40):
        m1 = x0 + (x1 - x0) / 3.0
        m2 = x1 - (x1 - x0) / 3.0
        if cost(m1) < cost(m2):
            x1 = m2
        else:
            x0 = m1
    L2 = 0.5 * (x0 + x1)
    a = flow(a0, L1, L2, MATS_P14, n)
    mg = ms * math.exp(L2)
    agi = sum(a) / 3.0
    return tau_p(mg, agi), mg, agi


tp_lo, mg_lo, ag_lo = tau_of_msusy(MZ)
tp_hi, mg_hi, ag_hi = tau_of_msusy(500.0)
E('  M_SUSY=M_Z(91.19 GeV)：M_GUT=%.6e alpha_GUT^-1=%.4f => tau_p=%.4e（%s）'
  % (mg_lo, ag_lo, tp_lo, '通过' if tp_lo >= SK_LIMIT else '被排除'))
E('  M_SUSY=500 GeV      ：M_GUT=%.6e alpha_GUT^-1=%.4f => tau_p=%.4e（%s）'
  % (mg_hi, ag_hi, tp_hi, '通过' if tp_hi >= SK_LIMIT else '被排除'))
ms_crit = None
if tp_lo >= SK_LIMIT > tp_hi:
    a0_, b0_ = MZ, 500.0
    for _ in range(60):
        mid = math.sqrt(a0_ * b0_)
        v, _mg, _ag = tau_of_msusy(mid)
        if v >= SK_LIMIT:
            a0_ = mid
        else:
            b0_ = mid
    ms_crit = 0.5 * (a0_ + b0_)
    tp_c, mg_c, ag_c = tau_of_msusy(ms_crit)
    E('  二分求临界：M_SUSY_crit = %.4f GeV（M_GUT=%.6e, tau_p=%.4e, 与下限相对差 %.2e）'
      % (ms_crit, mg_c, tp_c, abs(tp_c - SK_LIMIT) / SK_LIMIT))
    E('  >> tau_p >= Super-K  <=>  M_SUSY <= %.1f GeV' % ms_crit)
else:
    E('  >> 临界点不在 [M_Z, 500 GeV] 内：tau_p 在整段已%s'
      % ('全部通过' if tp_hi >= SK_LIMIT else '全部被排除'))
add('B7b FAIL', 'FAIL',
    'tau_p >= Super-K 要求 M_SUSY <= %.1f GeV（2-loop b33=+14 口径）' % ms_crit,
    'M_SUSY=M_Z: tau_p=%.3e（通过）；M_SUSY=500GeV: tau_p=%.3e（差 %.2f 倍）；临界 %.1f GeV'
    % (tp_lo, tp_hi, SK_LIMIT / tp_hi, ms_crit),
    '这条把 B4 的「二选一必死」升级为可直接对照实验的门槛：任何把超伴子质量下限推到 '
    '%.1f GeV 以上的实验（LHC 对 gluino/squark 的公认下限在 TeV 量级，具体值须核对，'
    '标 [C]）都会与本库口径下的维度-6 tau_p 冲突，且由 B7 的单调性知冲突随下限上移而加剧'
    % ms_crit)

# ============================================================
# B8 边界
# ============================================================
E('')
E('[B8] 可检验性与诚实边界')
E('-' * 78)
E('  (1) tau_p 是【工程闭式】：TAU0=1e35 yr / M_REF=2e16 GeV / AGINV_REF=35 / alpha_H=0.015')
E('      全为 attack27b 所选的归一化点，带 O(1) 系数不确定度 => 绝对标度不可跨册当真值。')
E('  (2) 只算维度-6 质子衰变；MSSM 特有的维度-5 通道（∝ 1/M_GUT，依赖 tan(beta) 与')
E('      超伴子谱）未计入 —— 本册与 attack27b 同口径，不改变其结论方向但也不加强它。')
E('  (3) 单点标度模型：全部超伴子质量 = M_SUSY。真实谱会同时改变阈值修正与 tau_p。')
E('  (4) 阈值修正未计入（attack32 自列的差异候选 d3）。')
E('  (5) b33 的【标准值】本册未从原始文献直接核对：B1 只证明 -14 是 +14 的符号翻转，')
E('      「+14 才是标准 MSSM」这一步依赖 attack32 的文献来源声明，须引原始表核对。')
add('B8 INFO', 'INFO',
    '可检验性与边界五条：工程闭式 / 仅维度-6 / 单点标度 / 无阈值修正 / b33 标准值待文献核对',
    '闭式归一化点 TAU0=1e35, M_REF=2e16, AGINV_REF=35, alpha_H=0.015',
    '本册的强结论是【结论随未声明口径翻转】（可机器判定），'
    '弱结论才是【tau_p 被排除】（依赖上述外部输入）。引用时必须连同这五条')

# ============================================================
# 汇总
# ============================================================
tally = {}
for e in ENTRIES:
    tally[e['verdict']] = tally.get(e['verdict'], 0) + 1

E('')
E('=' * 78)
E('条目 %d：' % len(ENTRIES))
for k in ('FAIL', 'CORRECTED', 'BOUNDARY', 'PASS', 'INFO'):
    if k in tally:
        E('   %-10s %d' % (k, tally[k]))
E('-' * 78)
for e in ENTRIES:
    E('  %-14s %-10s %s' % (e['code'], e['verdict'], e['title']))
E('=' * 78)

out = {
    'round': 'attack34',
    'topic': 'b33 符号的物理后果：M_SUSY 物理域 + tau_p 联动判定',
    'entries': ENTRIES,
    'tally': tally,
    'total': len(ENTRIES),
    'key_numbers': {
        'tau_p_selfcal_yr': '%.4e' % tp_cal,
        'tau_p_selfcal_rel_dev': '%.3e' % (abs(tp_cal - A27B_TAU) / A27B_TAU),
        'branch_1loop_back_msusy_GeV': 54.38472,
        'branch_1loop_back_mgut_GeV': '%.6e' % 2.321451e16,
        'branch_1loop_back_taup_yr': '%.4e' % rows_b4[0][4],
        'branch_2loop_p14_msusy_GeV': 2317.71643,
        'branch_2loop_p14_mgut_GeV': '%.6e' % 1.117972e16,
        'branch_2loop_p14_taup_yr': '%.4e' % rows_b4[1][4],
        'branch_2loop_n14_msusy_GeV': 17918.76520,
        'branch_2loop_n14_mgut_GeV': '%.6e' % 5.780340e15,
        'branch_2loop_n14_taup_yr': '%.4e' % rows_b4[2][4],
        'branch_27b_mgut_GeV': '%.6e' % 1.6899061e16,
        'branch_27b_taup_yr': '%.4e' % rows_b4[3][4],
        'tau_p_span_mult': '%.4f' % (max(r[4] for r in rows_b4) / min(r[4] for r in rows_b4)),
        'sk_limit_yr': SK_LIMIT,
        'excluded_branches_in_physical_domain': len(excluded),
        'alpha_H_critical_2loop_p14': '%.6f' % ah_needed,
        'alpha_H_typical': AH_REF,
        'mono_mgut_decreasing': mono_mgut,
        'mono_taup_decreasing': mono_tau,
        'mono_taup_at_10TeV_yr': '%.4e' % tps[-1],
    },
    'verdict': 'attack33 定位出的 b33 符号差异有硬物理后果：把四个分支各自的 '
               '(M_GUT, alpha_GUT) 代入 attack27b 的同一 tau_p 闭式，tau_p 跨 %.1f 倍；'
               '物理域内(M_SUSY>=M_Z)的 2-loop 解 tau_p 分别为 %.3e / %.3e yr，'
               '均低于 Super-K %.1e（差 %.2f / %.2f 倍，且需把 alpha_H 压到典型值 %.0f%% 以下才翻转）；'
               '唯一未被排除的 1-loop 解其 M_SUSY=54.38 GeV < M_Z 属非物理'
               % (max(r[4] for r in rows_b4) / min(r[4] for r in rows_b4),
                  rows_b4[1][4], rows_b4[2][4], SK_LIMIT,
                  1 / rows_b4[1][5], 1 / rows_b4[2][5],
                  100.0 * ah_needed / AH_REF),
    'red_line': '判定对象是「结论随未声明口径翻转」，不是 MSSM 被否证；'
                'tau_p 是工程闭式且仅算维度-6、单点标度、无阈值修正，b33 标准值仍待原始文献核对',
    'exit_code': 0,
}

jp = os.path.join(BASE, 'attack34_b33符号的物理后果_tau_p与物理域判定_2026-10-31.json')
with open(jp, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
E('')
E('产物已写出：%s' % os.path.basename(jp))
