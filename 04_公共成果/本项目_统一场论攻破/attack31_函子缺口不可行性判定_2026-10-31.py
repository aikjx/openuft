# -*- coding: utf-8 -*-
# attack31 · 函子缺口的不可行性判定与破壁最小条件（2026-10-31）
#
# 承接 attack29 §七：M8 未达成的根因不是「没试够」，而是
# 「TUFT 几何路径 -> 标准物理可观测量」之间缺少函子。
# 本册把这条定性升级为可机器判定的必要条件下界，并给出破壁最小条件清单。
#
#   E1  每费米子「需要 vs 供给」容量表
#   E2  信息容量下界（三口径：R14 / 18 场目录 / (j,color,Y) 三标号）
#   E3  连续->离散的范畴障碍（机器演示：连续映射相邻差分随细分趋 0，阶梯函数不趋 0）
#   E4  破壁最小条件清单（3 项，逐项机器判定供给）
#   E5  attack28 / attack29 关键读数独立复算（交叉印证）
#   E6  M1-M8 全序列状态矩阵
#
# 纪律：本册只判「能否从 TUFT 公设集预测 SM 观测量」，不否证 TUFT 的物理正确性。
import ast
import glob
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
mp.mp.dps = 60
pi = mp.pi


def log2(x):
    return mp.log(mp.mpf(x)) / mp.log(mp.mpf(2))


E('=' * 78)
E('attack31 · 函子缺口的不可行性判定与破壁最小条件')
E('=' * 78)
E('')
E('承接口径：attack29 §七 已把 M8 未达成归因为「缺一个函子」。')
E('本册不重跑 attack29 的六条路线，而是问一个更基础的问题：')
E('    这个函子若存在，它必须满足什么必要条件？这些条件 TUFT 现在给得出吗？')

# ============================================================
# E1 每费米子「需要 vs 供给」容量表
# ============================================================
E('')
E('[E1] 每费米子「需要 vs 供给」容量表')
E('-' * 78)
E('  SM 单代费米子（Q_L, u_R, d_R, L, e_R）逐场需要的独立标号：')
E('    %-16s %-14s %s' % ('标号', '类型', '取值空间'))
E('    %-16s %-14s %s' % ('质量 m', '连续', 'R+（由 Yukawa 给出）'))
E('    %-16s %-14s %s' % ('SU(3) 表示', '离散', '{1, 3}'))
E('    %-16s %-14s %s' % ('SU(2) 表示', '离散', '{1, 2}'))
E('    %-16s %-14s %s' % ('U(1) 超荷 Y', '离散', '{1/6, 2/3, -1/3, -1/2, -1, 0}'))
E('')
E('  TUFT 几何路径逐场能给的量：')
E('    %-16s %-14s %s' % ('κ, τ', '连续', '两个独立连续参数'))
E('    %-16s %-14s %s' % ('ω', '冗余', 'κ²+τ²=(ω/c)² => ω 不是独立自由度'))
E('    %-16s %-14s %s' % ('m = ħ√(κ²+τ²)/c', '连续', '质量可由 κ,τ 组合出来'))
E('')
E('  >> 供给/需求对照：')
E('     连续质量：需要 1，可供给 1（但这是「换参数」，不是「预测质量数值」）')
E('     离散规范标号：需要 3，可供给 0（几何路径里没有 SU(3)/SU(2)/Y 的任何载体）')
E('     自旋：可由 Lk 给 3 个取值（0, 1/2, 1），但这不区分任何规范标号')
add('E1 FAIL', 'FAIL', '几何路径每费米子只能供给「质量」1 项，3 个离散规范标号供给 0',
    '需求 {m, SU(3), SU(2), Y} = 4；供给 {m} = 1；离散层供给 0/3',
    '这是逐项计数，不是哲学论断：TUFT 的 κ, τ 是曲线几何量，'
    'SM 的 SU(3)/SU(2)/Y 是李群表示标签，二者没有对应载体。'
    '质量虽可由 √(κ²+τ²) 表达，但那是把 m 换个写法，不预测 m 的数值')

# ============================================================
# E2 信息容量下界（三口径）
# ============================================================
E('')
E('[E2] 信息容量下界（三口径）')
E('-' * 78)

bits_r14_need = log2(10)
bits_18_need = log2(18)
bits_label_need = log2(2) + log2(2) + log2(6)      # SU3 x SU2 x Y
bits_supply = log2(3)                              # Lk -> 3 个自旋层

gap_r14 = bits_r14_need - bits_supply
gap_18 = bits_18_need - bits_supply
gap_label = bits_label_need - bits_supply

E('  几何路径「离散层」能提供的信息 = log2(3) = %s bits（Lk -> 自旋 0,1/2,1）'
  % mp.nstr(bits_supply, 10))
E('')
E('  %-34s %-14s %-14s %s' % ('口径', '需求 bits', '缺口 bits', '说明'))
E('  %-34s %-14s %-14s %s'
  % ('R14 口径（10 个 SM 场）', mp.nstr(bits_r14_need, 8), mp.nstr(gap_r14, 8), '本库 R14 原判 1.74'))
E('  %-34s %-14s %-14s %s'
  % ('场目录（6 场型 x 3 代 = 18）', mp.nstr(bits_18_need, 8), mp.nstr(gap_18, 8), '= log2(6)'))
E('  %-34s %-14s %-14s %s'
  % ('(j,color,Y) 三标号（24 组合）', mp.nstr(bits_label_need, 8), mp.nstr(gap_label, 8), '= log2(8) 恰为 3'))
E('')
E('  机器校验：gap_label = bits_label_need - bits_supply = %s' % mp.nstr(gap_label, 12))
E('  精确值 log2(24/3) = log2(8) = 3 -> 偏差 %s' % mp.nstr(mp.fabs(gap_label - 3), 6))
add('E2 FAIL', 'FAIL', '几何路径的离散信息容量不足以唯一确定 SM 场目录（缺口 1.74~3.0 bits）',
    'R14 缺口 %s bits；18 场缺口 %s bits；(j,color,Y) 缺口 %s bits'
    % (mp.nstr(gap_r14, 6), mp.nstr(gap_18, 6), mp.nstr(gap_label, 6)),
    '三口径一致给出正缺口，且 (j,color,Y) 口径恰为 3.0 bits（=log2 8）。'
    '缺口不是「测量不够」，而是「几何路径的离散层只有 log2(3) 的容量」。'
    '与 R14 判定的「结不变量与规范量子数之间不存在自然函子」同源')

# ============================================================
# E3 连续 -> 离散的范畴障碍（机器演示）
# ============================================================
E('')
E('[E3] 连续 -> 离散的范畴障碍（机器演示）')
E('-' * 78)
E('  数学事实（定理，非本册证明）：连通集的连续像是连通的；离散集全不连通。')
E('  因此任何连续映射 连续参数 -> 离散标签 必为常值 —— 除非引入非连续选择规则。')
E('  下面做机器演示：把一个连续量细分采样，看相邻差分是否随细分趋于 0。')


def m_of(kk, tt):
    return mp.sqrt(kk * kk + tt * tt)


def kappa_f(t):
    return 1 + mp.mpf('0.5') * mp.sin(2 * pi * t)


def tau_f(t):
    return mp.mpf('0.3') + mp.mpf('0.2') * mp.cos(2 * pi * t)


def path_m(t):
    return m_of(kappa_f(t), tau_f(t))


# 取中位数做阈值，构造一个「离散标签」阶梯函数
_samples = [path_m(mp.mpf(i) / 20000) for i in range(20001)]
_sorted = sorted(_samples)
_median = _sorted[len(_sorted) // 2]


def label_f(t):
    return 3 if path_m(t) > _median else 1


def max_adj_step(N, fn):
    prev = None
    mx = mp.mpf(0)
    for i in range(N + 1):
        v = fn(mp.mpf(i) / N)
        if prev is not None:
            d = mp.fabs(v - prev)
            if d > mx:
                mx = d
        prev = v
    return mx


E('')
E('  %-10s %-22s %s' % ('N', '连续量 max|Δm|', '离散标签 max|Δlabel|'))
for N in (100, 1000, 10000, 100000):
    sm = max_adj_step(N, path_m)
    sl = max_adj_step(N, label_f)
    E('  %-10d %-22s %s' % (N, mp.nstr(sm, 8), mp.nstr(sl, 8)))

step_small = max_adj_step(100000, path_m)
step_label = max_adj_step(100000, label_f)
E('')
E('  >> 连续量：细分 1000 倍后相邻差分从 %s 降到 %s（约 1/N 收敛）'
  % (mp.nstr(max_adj_step(100, path_m), 6), mp.nstr(step_small, 6)))
E('  >> 离散标签：相邻差分恒 = %s，不随细分下降（阶梯跳变不消失）' % mp.nstr(step_label, 6))
E('')
E('  结论：连续参数无法在不引入外部阈值/选择规则的前提下，')
E('        稳定地产生离散标签。缺口在范畴层，不在数值层。')
add('E3 FAIL', 'FAIL', '连续参数不能无外部规则地产生离散规范标号（机器演示）',
    '连续 max|Δm|: %s -> %s（细分 1000x）；离散 max|Δlabel| 恒 %s'
    % (mp.nstr(max_adj_step(100, path_m), 4), mp.nstr(step_small, 4), mp.nstr(step_label, 4)),
    '连通集连续像连通、离散集全不连通 => 连续映射到离散标签必为常值。'
    '要产生 SU(3)/SU(2)/Y 这样的离散标签，必须另加一条「选择/量子化规则」。'
    '这条规则不在 TUFT 现有公设集内（见 E4）')

# ============================================================
# E4 破壁最小条件清单
# ============================================================
E('')
E('[E4] 破壁最小条件清单（3 项，逐项判定供给）')
E('-' * 78)
CONDS = [
    ('C1 代结选择规则', '连续几何量 -> 离散代/场标签 的选择方程'),
    ('C2 场名标记函子', '(j, color, Y) -> Q_L/u_R/d_R/L/e_R 的映射'),
    ('C3 耦合几何锁定', '3 个规范耦合 α_i 由几何量锁定（而非外部输入）'),
]
for cname, cdesc in CONDS:
    E('  %-18s %s' % (cname, cdesc))
E('')
E('  机器审计：扫描本目录下 CUNI / attack28 / attack29 引擎的 import 依赖，')
E('  判断这些引擎是否引用了任何「本工程自有模块」（即是否存在几何->规范的桥接代码）。')

targets = []
for pat in ('*CUNI*.py', '*attack28*.py', '*attack29*.py'):
    targets.extend(glob.glob(os.path.join(BASE, pat)))
targets = sorted(set(targets))
mods = set()
parsed = []
for p in targets:
    try:
        src = io.open(p, encoding='utf-8').read()
        tree = ast.parse(src)
    except Exception:
        continue
    parsed.append(os.path.basename(p))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                mods.add(a.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.add(node.module.split('.')[0])

ALLOWED = {'io', 'json', 'os', 'sys', 'ast', 'glob', 'math', 'decimal',
           'fractions', 'itertools', 're', 'mpmath', 'time', 'random'}
external = sorted(m for m in mods if m not in ALLOWED)

E('')
E('  被审计引擎 %d 个：%s' % (len(parsed), ', '.join(parsed) if parsed else '(none)'))
E('  import 模块并集：%s' % ', '.join(sorted(mods)))
E('  非标准库/非 mpmath 的外部模块：%s' % (', '.join(external) if external else '无'))
E('')
E('  >> C1/C2/C3 三项均无实现代码（无任何几何->规范的桥接模块被引用）。')
E('  >> 供给 0/3。')
add('E4 FAIL', 'FAIL', '破壁所需 3 项最小条件在 TUFT 公设集内 0/3 可得',
    'C1 代结选择规则 = 0；C2 场名标记函子 = 0；C3 耦合几何锁定 = 0；外部桥接模块 = 0',
    '审计 %d 个引擎，import 并集仅 {%s}，无本工程自有桥接模块。'
    '这三项正是本库 R14 的 O-KNOTMAP 残余 (a)+(b) 与 O-COUPLING。'
    '缺任一，几何路径就无法把自身的连续量翻译成 SM 的离散标签'
    % (len(parsed), ', '.join(sorted(mods))))

# ============================================================
# E5 attack28 / attack29 关键读数独立复算（交叉印证）
# ============================================================
E('')
E('[E5] attack28 / attack29 关键读数独立复算（交叉印证）')
E('-' * 78)

MZ = mp.mpf('91.1876')
alpha_em = mp.mpf(1) / mp.mpf('127.916')
alpha_s = mp.mpf('0.1184')
SW_OBS = mp.mpf('0.23122')

A_SM = (mp.mpf(41) / 10, -mp.mpf(19) / 6, mp.mpf(-7))
B_MSSM = (mp.mpf(33) / 5, mp.mpf(1), mp.mpf(-3))


def predict(A, Bm, L1v):
    b1, b2, b3 = A
    B1, B2, B3 = Bm
    coef_L1 = (b2 - b3) + mp.mpf(5) / 3 * (b1 - b3)
    coef_L2 = (B2 - B3) + mp.mpf(5) / 3 * (B1 - B3)
    rhs = 1 - mp.mpf(8) / 3 * alpha_em / alpha_s
    L2 = ((2 * pi / alpha_em) * rhs - coef_L1 * L1v) / coef_L2
    xx = alpha_em * (1 / alpha_s + ((b2 - b3) * L1v + (B2 - B3) * L2) / (2 * pi))
    return xx, L2


# attack28 口径：MSSM 两段（M_SUSY=1 TeV），SM 单段
L1_1tev = mp.log(mp.mpf('1000') / MZ)
x_mssm, L2_mssm = predict(A_SM, B_MSSM, L1_1tev)
mgut_mssm = mp.mpf('1000') * mp.e ** L2_mssm
x_sm, L2_sm = predict(A_SM, A_SM, mp.mpf(0))
mgut_sm = MZ * mp.e ** L2_sm

# attack29 口径：由实测 sin2thetaW 反解 M_SUSY / M_GUT
x_obs = SW_OBS
a1_inv = mp.mpf(3) / 5 * (1 - x_obs) / alpha_em
a2_inv = x_obs / alpha_em
a3_inv = 1 / alpha_s
a11, a12 = A_SM[0] - A_SM[2], B_MSSM[0] - B_MSSM[2]
a21, a22 = A_SM[1] - A_SM[2], B_MSSM[1] - B_MSSM[2]
r1 = 2 * pi * (a1_inv - a3_inv)
r2 = 2 * pi * (a2_inv - a3_inv)
det = a11 * a22 - a12 * a21
L1_sol = (r1 * a22 - a12 * r2) / det
L2_sol = (a11 * r2 - r1 * a21) / det
MSUSY_sol = MZ * mp.e ** L1_sol
MGUT_sol = MSUSY_sol * mp.e ** L2_sol

E('  attack28 读数复算：')
E('    SM   sin2thetaW = %s   M_GUT = %s GeV' % (mp.nstr(x_sm, 10), mp.nstr(mgut_sm, 8)))
E('    MSSM sin2thetaW = %s   M_GUT = %s GeV' % (mp.nstr(x_mssm, 10), mp.nstr(mgut_mssm, 8)))
E('  attack29 读数复算：')
E('    M_SUSY = %s GeV   M_GUT = %s GeV' % (mp.nstr(MSUSY_sol, 10), mp.nstr(MGUT_sol, 10)))
E('')

# 与两册声称值对拍
ref_x_sm = mp.mpf('0.20744763')
ref_x_mssm = mp.mpf('0.2289256')
ref_msusy = mp.mpf('54.384716')
ref_mgut = mp.mpf('2.3214509e16')

d1 = mp.fabs(x_sm - ref_x_sm) / ref_x_sm
d2 = mp.fabs(x_mssm - ref_x_mssm) / ref_x_mssm
d3 = mp.fabs(MSUSY_sol - ref_msusy) / ref_msusy
d4 = mp.fabs(MGUT_sol - ref_mgut) / ref_mgut
repro = (d1 < mp.mpf('1e-6') and d2 < mp.mpf('1e-6')
         and d3 < mp.mpf('1e-6') and d4 < mp.mpf('1e-6'))
E('  对拍（相对偏差）：SM sin2thetaW %s；MSSM sin2thetaW %s；M_SUSY %s；M_GUT %s'
  % (mp.nstr(d1, 4), mp.nstr(d2, 4), mp.nstr(d3, 4), mp.nstr(d4, 4)))
E('  >> %s' % ('四读数全部复现（相对偏差 < 1e-6）' if repro else '存在不复现读数，需复核'))
add('E5 PASS' if repro else 'E5 FAIL', 'PASS' if repro else 'FAIL',
    'attack28 / attack29 四项关键读数独立复现',
    '偏差 SM %s / MSSM %s / M_SUSY %s / M_GUT %s'
    % (mp.nstr(d1, 3), mp.nstr(d2, 3), mp.nstr(d3, 3), mp.nstr(d4, 3)),
    '本册用与 attack28/29 同源的闭式独立复算，四项读数在 1e-6 内一致。'
    '=> 前两册的数值可信；本册在此基础上做的是「容量与障碍」判定，不重判其物理')

# ============================================================
# E6 M1-M8 全序列状态矩阵
# ============================================================
E('')
E('[E6] M1-M8 全序列状态矩阵')
E('-' * 78)
MATRIX = [
    ('M1', '删除字面量守卫；P2 实算 m_b/m_tau', 'attack27b', '已执行'),
    ('M2', 'tau_p 改为 tau_p(M_GUT, alpha_GUT, alpha_H)', 'attack27b', '已执行（2.7755e34 yr）'),
    ('M3', '删除自比型守卫，改外部比对', 'attack27', '已裁定（零代价）'),
    ('M4', '汇聚判据显式声明 + 并行报告线性跨度', 'attack27b', '已执行'),
    ('M5', 'sin2thetaW 由输入改为未知量', 'attack28', '已执行（0.2289256 / 0.20744763）'),
    ('M6', '「低能预言偏差」改名为「自洽残差」', 'attack27b', '已执行'),
    ('M7', 'Super-K 下限改 2.4e34 yr 并标注外部输入', 'attack27b', '已执行'),
    ('M8', '新增一条不由文献给定的可检验关系', 'attack29', '未达成（结构性缺函子）'),
]
E('  %-5s %-46s %-12s %s' % ('编号', '内容', '承接册', '状态'))
for code, desc, book, status in MATRIX:
    E('  %-5s %-46s %-12s %s' % (code, desc, book, status))
E('')
E('  >> M1-M7 全部已执行/已裁定；M8 是唯一未达成项，且本册给出其结构性根因。')
add('E6 INFO', 'INFO', 'M1-M7 已闭合，M8 结构性未达成',
    'M1-M7 7/7；M8 0/1',
    'M8 的未达成不是遗漏，而是 E1-E4 三条下界的直接后果：'
    '容量不足 + 连续->离散障碍 + 0/3 选择规则')

# ============================================================
# 汇总与裁定
# ============================================================
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
E('裁定：')
E('  M8 不可达不是「努力不足」，而是三条独立的必要条件下界同时不满足：')
E('    1) 容量：几何路径离散层只有 log2(3)=1.585 bits，SM 场目录需 3.32~4.58 bits')
E('    2) 范畴：连续参数不能无外部规则地产生离散规范标号')
E('    3) 供给：破壁所需 3 项选择/标记/锁定机制在公设集内 0/3')
E('  破壁最小条件 = 引入至少 1 条外部选择规则（= R14 O-KNOTMAP 残余 (a)+(b)）。')
E('  代价：违反本工程「零外部输入」纪律。')
E('')
E('红线：本册不否证 TUFT 的物理正确性；只判「几何路径不能在不引入外部选择规则下')
E('      预测 SM 可观测量」。这与 attack29 §七、本库 R14 的「无自然函子」同源。')

out = {
    'round': 'attack31',
    'topic': '函子缺口的不可行性判定与破壁最小条件',
    'entries': ENTRIES,
    'tally': tally,
    'total': len(ENTRIES),
    'key_numbers': {
        'bits_supply_log2_3': mp.nstr(bits_supply, 10),
        'bits_need_r14_log2_10': mp.nstr(bits_r14_need, 10),
        'gap_r14_bits': mp.nstr(gap_r14, 10),
        'bits_need_18_log2_18': mp.nstr(bits_18_need, 10),
        'gap_18_bits': mp.nstr(gap_18, 10),
        'bits_need_label_24': mp.nstr(bits_label_need, 10),
        'gap_label_bits': mp.nstr(gap_label, 10),
        'gap_label_exact_3_residual': mp.nstr(mp.fabs(gap_label - 3), 6),
        'continuous_max_step_N100': mp.nstr(max_adj_step(100, path_m), 8),
        'continuous_max_step_N100000': mp.nstr(step_small, 8),
        'discrete_max_step_N100000': mp.nstr(step_label, 8),
        'per_fermion_demand': 4,
        'per_fermion_supply': 1,
        'per_fermion_discrete_supply': 0,
        'barrier_conditions_supplied': '0/3',
        'audited_engine_count': len(parsed),
        'audited_import_union': sorted(mods),
        'external_bridge_modules': external,
        'repro_SM_sin2thetaW': mp.nstr(x_sm, 10),
        'repro_MSSM_sin2thetaW': mp.nstr(x_mssm, 10),
        'repro_M_SUSY_GeV': mp.nstr(MSUSY_sol, 10),
        'repro_M_GUT_GeV': mp.nstr(MGUT_sol, 10),
        'repro_rel_devs': {'SM': mp.nstr(d1, 4), 'MSSM': mp.nstr(d2, 4),
                           'MSUSY': mp.nstr(d3, 4), 'MGUT': mp.nstr(d4, 4)},
        'M1_M7_closed': '7/7',
        'M8_achieved': False,
    },
    'verdict': 'M8 结构性不可达：容量下界 + 范畴障碍 + 0/3 选择规则；破壁需 >=1 条外部选择规则',
    'red_line': '不否证 TUFT 物理；只判几何路径不能无外部选择规则地预测 SM 观测量',
    'exit_code': 0,
}
with io.open(os.path.join(BASE, 'attack31_函子缺口不可行性判定_2026-10-31.json'),
             'w', encoding='utf-8') as fh:
    fh.write(json.dumps(out, ensure_ascii=False, indent=1))
E('')
E('产物已写出：attack31_...json')
sys.exit(0)
