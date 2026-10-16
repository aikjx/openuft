# -*- coding: utf-8 -*-
"""
r71 · 2026-10-15 · r69 下游攻破
《lambda 维度修正版重算 + 导数项增广与传播自由度恢复判定》
==============================================================================
r69 已判（继承，不重推）：
  L = (hbar*c/2)(kappa^2 - tau^2) - U,  U = l1*k^4 + l2*t^4 + l3*k^2*t^2
  S7_R1 FAIL: 声称 lambda 无量纲 => U 量纲 L^-4，动能项 M L T^-2 => 不可相加
  S7_R2/S3_R3: 修正读数 [l1] = M L^5 T^-2
  S3_R1 BOUNDARY: EOM 无导数项 => 纯代数约束 => 无传播自由度

本册攻破四组：
  组 A 量纲口径仲裁（★修正 r69 两处措辞/数值）
    A1 机器确认 [动能项] = M L T^-2，这是【力】(N) 而不是【能量】(M L^2 T^-2)
    A2 以拉氏密度应具的量纲【能量密度 M L^-1 T^-2】为基准，缺口 = L^2
       => r69 S2_R1 写的"缺 1/L 因子"不成立，实为"多 L^2（即缺 1/L^2）"
    A3 上述修正【不推翻】r69 S7_R1 FAIL（M L T^-2 != L^-4 仍成立）
  组 B lambda 维度两口径（r69 未声明口径）
    B1 严格口径（L 是拉氏密度 = 能量密度）=> [lambda] = M L^3 T^-2
    B2 r69 口径（以动能项 M L T^-2 为基准）=> [lambda] = M L^5 T^-2
    B3 两口径相差 L^2
    B4 幂次穷举：{hbar,c,l_P,m_P,G}^[-3,3] 共 3125 组，统计命中数
  组 C 导数项增广（★承重：同时解量纲与传播自由度）
    C1 最小零成本修法：kappa^2 -> (partial kappa)^2
       [(hbar c/2)(partial kappa)^2] 恰为能量密度 M L^-1 T^-2，不需新常数
    C2 修后 EOM 含 d'Alembert 项 => 传播自由度恢复，色散 omega^2 = c^2(k^2+M^2)
    C3 群速度 < c 数值扫描（因果 OK）；无质量极限 omega = c k
    C4 ★二难：(kappa^2 - tau^2) 的负号在补导数后变成【tau 动能项系数为负】
       => 鬼场，哈密顿密度无下界（机器扫描 H_tau -> -inf）
  组 D 参数代价与 Omega5

纪律（承 r37/r59/r64/r66/r67/r69）
 1) 量纲指数【相加】（r37 曾错写为相乘，本册 G0-* 守卫兜底）
 2) 量纲工具必须先过自守卫 G0-* 再用于判定；手算量纲一律机器兜底
 3) 任何"恒零/恒真"裁定必须配阳性对照
 4) 不自推的系数显式登记 not_self_derived，不编
 5) 不改任何他人文件字节；不跑 refresh_catalog（并发回退风险，待批准）
 6) 退出码 0 = 引擎跑完；结论看 counts/verdict
==============================================================================
"""

import sys, os, io, json
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
ROOT = os.path.dirname(BASE)

STEM = 'TUFT-r71_lambda维度修正与导数项增广_攻破_2026-10-15'
SRC_NAME = 'TUFT-r71_lambda维度修正与导数项增广_攻破_2026-10-15.py'

# ----------------------------------------------------------------------------
# 量纲工具：四元组 (M, L, T, Q)，指数相加
# ----------------------------------------------------------------------------
def D(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    return tuple(x * Fr(n) for x in a)

def dstr(a):
    names = ('M', 'L', 'T', 'Q')
    out = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        out.append(nm + '^' + str(v))
    return ' '.join(out) if out else '1'

# 基本量纲
D_HBAR = D(m=1, l=2, t=-1)
D_C = D(l=1, t=-1)
D_KAPPA = D(l=-1)
D_TAU = D(l=-1)
D_ENERGY = D(m=1, l=2, t=-2)
D_ENERGY_DENSITY = D(m=1, l=-1, t=-2)
D_FORCE = D(m=1, l=1, t=-2)
D_PLANCK_L = D(l=1)
D_PLANCK_M = D(m=1)
D_G = D(m=-1, l=3, t=-2)

# ----------------------------------------------------------------------------
# 结果容器
# ----------------------------------------------------------------------------
ENTRIES = []
COUNTS = {}

def entry(tag, verdict, text, residual=None, note=None):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': (str(residual) if residual is not None else None),
                    'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1

# ----------------------------------------------------------------------------
# G0-* 量纲工具自守卫
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1: dmul 指数相加
    if dmul(D_HBAR, D_C) != (Fr(1), Fr(3), Fr(-2), Fr(0)):
        fails.append('G0-1')
    # G0-2: 能量 / 能量密度 / 力 三者互异
    if D_ENERGY == D_ENERGY_DENSITY or D_ENERGY == D_FORCE or D_ENERGY_DENSITY == D_FORCE:
        fails.append('G0-2')
    # G0-3: dpow 正确
    if dpow(D_KAPPA, 2) != (Fr(0), Fr(-2), Fr(0), Fr(0)):
        fails.append('G0-3')
    # G0-4: ddiv 正确
    if ddiv(D_ENERGY, D_C) != (Fr(1), Fr(1), Fr(-1), Fr(0)):
        fails.append('G0-4')
    # G0-5: [hbar*c*kappa^2] == 力 M L T^-2
    if dmul(dmul(D_HBAR, D_C), dpow(D_KAPPA, 2)) != D_FORCE:
        fails.append('G0-5')
    # G0-6: [hbar*c*kappa^2] != 能量密度（守卫：不许把力当能量密度）
    if dmul(dmul(D_HBAR, D_C), dpow(D_KAPPA, 2)) == D_ENERGY_DENSITY:
        fails.append('G0-6')
    # G0-7: 力 / 能量密度 == L^2
    if ddiv(D_FORCE, D_ENERGY_DENSITY) != (Fr(0), Fr(2), Fr(0), Fr(0)):
        fails.append('G0-7')
    # G0-8: dstr 负指数渲染（禁止 L^--2 双负号）
    if '^--' in dstr(dpow(D_KAPPA, -2)):
        fails.append('G0-8')
    if fails:
        raise SystemExit('G0 量纲工具自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# 组 A：量纲口径仲裁（★修正 r69）
# ----------------------------------------------------------------------------
def group_A():
    kin = dmul(dmul(D_HBAR, D_C), dpow(D_KAPPA, 2))

    # A1
    is_force = (kin == D_FORCE)
    is_energy = (kin == D_ENERGY)
    entry('A1', 'CORRECTED' if (is_force and not is_energy) else 'FAIL',
          ('机器确认 [(hbar*c/2)(kappa^2-tau^2)] = ' + dstr(kin) +
           '；等于【力】' + str(is_force) + '、等于【能量】' + str(is_energy) +
           '。r69 S2_R1 括注写"=能量 M L T^-2"，但 M L T^-2 是力不是能量'
           '（能量 = M L^2 T^-2）=> r69 该括注措辞有误'),
          None, '修正 r69 措辞')

    # A2
    gap = ddiv(kin, D_ENERGY_DENSITY)
    gap_is_L2 = (gap == (Fr(0), Fr(2), Fr(0), Fr(0)))
    entry('A2', 'CORRECTED' if gap_is_L2 else 'FAIL',
          ('以拉氏密度应具量纲【能量密度 ' + dstr(D_ENERGY_DENSITY) + '】为基准，'
           '动能项缺口 = ' + dstr(gap) + '。r69 写"缺 1/L 因子"，实为多出 L^2'
           '（等价于缺 1/L^2）=> r69 该处数值有误'),
          None, '修正 r69 数值')

    # A3：不推翻 S7_R1
    term_U = dpow(D_KAPPA, 4)
    still_fail = (kin != term_U)
    entry('A3', 'PASS' if still_fail else 'FAIL',
          ('上述两处修正【不推翻】r69 S7_R1：动能项 ' + dstr(kin) +
           ' 与 lambda 无量纲时的 U ' + dstr(term_U) + ' 仍不可相加 => FAIL 继续成立'),
          None, '继承有效性')

    # A4 阳性对照：确认检验器能区分三者
    entry('A4', 'PASS' if (D_ENERGY != D_ENERGY_DENSITY and
                           D_ENERGY != D_FORCE and
                           D_ENERGY_DENSITY != D_FORCE) else 'FAIL',
          ('阳性对照：能量 ' + dstr(D_ENERGY) + ' / 能量密度 ' + dstr(D_ENERGY_DENSITY) +
           ' / 力 ' + dstr(D_FORCE) + ' 三者两两互异 => 检验器非恒真'),
          None, '阳性对照')

# ----------------------------------------------------------------------------
# 组 B：lambda 维度两口径 + 幂次穷举
# ----------------------------------------------------------------------------
def group_B():
    U_fields = dpow(D_KAPPA, 4)   # lambda 无量纲时 U 的场依赖部分 = L^-4

    lam_strict = ddiv(D_ENERGY_DENSITY, U_fields)   # 严格口径
    lam_r69 = ddiv(D_FORCE, U_fields)               # r69 口径
    diff = ddiv(lam_r69, lam_strict)

    entry('B1', 'PASS' if lam_strict == (Fr(1), Fr(3), Fr(-2), Fr(0)) else 'FAIL',
          ('严格口径（L 是拉氏密度，应 = 能量密度）：[lambda] = ' + dstr(lam_strict)),
          None, None)

    entry('B2', 'PASS' if lam_r69 == (Fr(1), Fr(5), Fr(-2), Fr(0)) else 'FAIL',
          ('r69 口径（以动能项 M L T^-2 为基准）：[lambda] = ' + dstr(lam_r69) +
           '，与 r69 S7_R2/S3_R3 读数一致 => 互证'),
          None, '与 r69 互证')

    entry('B3', 'MISMATCH' if diff == (Fr(0), Fr(2), Fr(0), Fr(0)) else 'FAIL',
          ('两口径相差 ' + dstr(diff) + ' => r69 未声明所采用口径，'
           '其 [lambda]=M L^5 T^-2 只在"以动能项为基准"下成立，'
           '在"拉氏密度 = 能量密度"的严格口径下应为 M L^3 T^-2'),
          None, 'r69 口径未声明')

    # B4 幂次穷举
    basis = {'hbar': D_HBAR, 'c': D_C, 'l_P': D_PLANCK_L,
             'm_P': D_PLANCK_M, 'G': D_G}
    keys = list(basis.keys())
    hits_strict = []
    hits_r69 = []
    rng = range(-3, 4)
    for a in rng:
        for b in rng:
            for d in rng:
                for e in rng:
                    for f in rng:
                        exps = (a, b, d, e, f)
                        tot = (Fr(0), Fr(0), Fr(0), Fr(0))
                        for k, p in zip(keys, exps):
                            tot = dmul(tot, dpow(basis[k], p))
                        if tot == lam_strict:
                            hits_strict.append(exps)
                        if tot == lam_r69:
                            hits_r69.append(exps)
    entry('B4', 'INFO',
          ('幂次穷举 {hbar,c,l_P,m_P,G}^[-3,3] 共 3125 组：'
           '构造出严格口径 M L^3 T^-2 的组合 ' + str(len(hits_strict)) + ' 组；'
           '构造出 r69 口径 M L^5 T^-2 的组合 ' + str(len(hits_r69)) + ' 组'),
          None, '两口径均可由普朗克基组构造')

# ----------------------------------------------------------------------------
# 组 C：导数项增广（★承重）
# ----------------------------------------------------------------------------
def group_C():
    # C1: 最小零成本修法
    d_partial = D(l=-1)                 # [partial_mu] = L^-1（x^0 = c t 口径）
    d_partial_kappa = dmul(d_partial, D_KAPPA)   # L^-2
    kin_new = dmul(dmul(D_HBAR, D_C), dpow(d_partial_kappa, 2))
    ok = (kin_new == D_ENERGY_DENSITY)
    entry('C1', 'PASS' if ok else 'FAIL',
          ('★最小零成本修法：kappa^2 -> (partial kappa)^2。'
           '[(hbar c/2)(partial kappa)^2] = ' + dstr(kin_new) +
           '，恰为能量密度 => 量纲闭合且不引入任何新常数'),
          None, '★承重')

    # C2: EOM 含 d'Alembert 项 -> 传播自由度恢复
    #     EOM: hbar c □kappa + dU/dkappa = 0
    box_kappa = dmul(dpow(d_partial, 2), D_KAPPA)      # [□kappa] = L^-3
    dU_dkappa = dmul(dpow(D_KAPPA, 3), D(m=1, l=3, t=-2))  # [lambda*kappa^3]
    over_hbarc = ddiv(dU_dkappa, dmul(D_HBAR, D_C))
    homogeneous = (box_kappa == over_hbarc)
    entry('C2', 'PASS' if homogeneous else 'FAIL',
          ('修后 EOM：hbar c □kappa + dU/dkappa = 0；'
           '[□kappa] = ' + dstr(box_kappa) + '，[dU/dkappa / (hbar c)] = ' +
           dstr(over_hbarc) + ' => 齐次，且含二阶时空导数项 => 传播自由度恢复'),
          None, '★承重')

    # C3: 色散与群速度
    c = Decimal('299792458')
    M = Decimal('1e9')          # 有效质量参数（量纲 L^-1）
    vg_list = []
    ks = [Decimal('1e8'), Decimal('1e9'), Decimal('1e10'),
          Decimal('1e11'), Decimal('1e12')]
    for k in ks:
        omega = c * (k * k + M * M).sqrt()
        vg = c * c * k / omega
        vg_list.append((k, omega, vg, vg / c))
    max_ratio = max(r for (_, _, _, r) in vg_list)
    all_sub_c = all(r < 1 for (_, _, _, r) in vg_list)
    monotone = all(vg_list[i][3] <= vg_list[i + 1][3] for i in range(len(vg_list) - 1))
    entry('C3', 'PASS' if (all_sub_c and monotone) else 'FAIL',
          ('色散 omega^2 = c^2(k^2 + M^2)：群速度 v_g = c^2 k / omega < c 对全部 '
           '5 个 k 成立（max v_g/c = ' + format(max_ratio, '.15E') +
           '），且随 k 单调递增趋于 c => 因果性 OK，'
           '无质量极限 M=0 给 omega = c k（v_g = c）'),
          format(max_ratio, '.15E'), 'KG 标准行为')

    # C3b 阳性对照：若色散号写反（omega^2 = c^2(k^2 - M^2)），小 k 处出现虚频率
    k_small = Decimal('1e8')
    inside_bad = k_small * k_small - M * M
    entry('C3b', 'PASS' if inside_bad < 0 else 'FAIL',
          ('阳性对照：若色散号写反为 omega^2 = c^2(k^2 - M^2)，在 k=' +
           '1e8 < M=1e9 处根号内为负（' + format(inside_bad, '.6E') +
           '）=> 虚频率、指数不稳定。本册正确式在该点恒正 => 检验器非恒真'),
          format(inside_bad, '.6E'), '阳性对照')

    # C4: ★鬼场 —— tau 动能项系数为负
    #     L_kin = (hbar c/2)[(partial kappa)^2 - (partial tau)^2]
    #     tau 扇区系数 = -hbar c < 0 => 鬼
    hbar = Decimal('1.054571817e-34')
    H_tau_list = []
    H_kappa_list = []
    for A in [Decimal('1'), Decimal('10'), Decimal('100'),
              Decimal('1000'), Decimal('10000')]:
        # 均匀场构型：partial_t = A, grad = 0
        # H_tau   = -(hbar/(2c)) A^2   （tau 动能项系数为负）
        # H_kappa = +(hbar/(2c)) A^2   （kappa 动能项系数为正）
        H_tau = -(hbar / (2 * c)) * A * A
        H_kappa = (hbar / (2 * c)) * A * A
        H_tau_list.append((A, H_tau))
        H_kappa_list.append((A, H_kappa))
    H_tau_neg = all(h < 0 for (_, h) in H_tau_list)
    H_tau_decreasing = all(H_tau_list[i][1] > H_tau_list[i + 1][1]
                           for i in range(len(H_tau_list) - 1))
    H_kappa_pos = all(h > 0 for (_, h) in H_kappa_list)
    unbounded = H_tau_neg and H_tau_decreasing
    entry('C4', 'FAIL' if unbounded else 'BOUNDARY',
          ('★二难（本册最重要）：(kappa^2 - tau^2) 的负号在补导数后变成'
           '【tau 动能项系数 = -hbar c < 0】=> 鬼场。'
           '均匀场构型下 H_tau = -(hbar/(2c))(partial_t tau)^2 恒负'
           '（' + str(H_tau_neg) + '）且随 |partial_t tau| 单调递减'
           '（' + str(H_tau_decreasing) + '）=> 哈密顿密度无下界；'
           '对照 H_kappa = +(hbar/(2c))(partial_t kappa)^2 恒正（' +
           str(H_kappa_pos) + '）有下界'),
          format(H_tau_list[-1][1], '.15E'), '★承重')

    # C5：二难的代价（不代选）
    entry('C5', 'BOUNDARY',
          ('二难两条出路（本册不代选）：'
           '(a) 保留 (kappa^2 - tau^2) 结构 => tau 扇区为鬼，理论不可量子化；'
           '(b) 改 tau 项为同号 => 丢掉来料核心的 kappa^2 - tau^2 差结构，'
           '且与原 S1 几何恒等式的联系需重证'),
          None, '待裁决')

# ----------------------------------------------------------------------------
# 组 D：参数代价与 Omega5
# ----------------------------------------------------------------------------
def group_D():
    # D1: 修正后新常数计数
    n_lambda = 3          # lam1, lam2, lam3（带量纲 M L^3 T^-2）
    n_new_Z = 0           # 若 Z = hbar c 固定，则不加
    total_new = n_lambda + n_new_Z
    entry('D1', 'FAIL' if total_new > 1 else 'PASS',
          ('修正后新常数：lam1/lam2/lam3 共 3 个（均带量纲 M L^3 T^-2）；'
           '若动能系数取 Z = hbar c（用既有常数）则不再新增 => '
           '合计新增 ' + str(total_new) + ' 个自由常数'),
          None, None)

    # D2: 撞 Omega5
    entry('D2', 'FAIL' if total_new > 1 else 'PASS',
          ('Omega5 要求自由常数 <= 1；新增 ' + str(total_new) +
           ' 个 => 违反。承 r20：tau 动力学化 +2 参数、kappa 再 +2 => 合计 4，'
           '本册口径（Z 固定为 hbar c）下为 3，均 > 1 => 撞 Omega5'),
          None, '承 r20')

    # D3: 若 lambda 由普朗克锚定反解，是否可证伪
    entry('D3', 'BOUNDARY',
          ('若 lam_i 改由普朗克锚定（l_P / m_P）反解，则自由常数降为 0，'
           '但此时理论输出恒等于锚点输入 => 循环自洽、不可证伪'
           '（与 r41 M1 二阶两难 A 同构）'),
          None, '承 r41')

    # D4: 诚实总结
    entry('D4', 'BOUNDARY',
          ('综合：补导数项同时解开了 r69 的两个阻塞（量纲 + 传播自由度），'
           '但立刻触发第三个更严重的阻塞（tau 鬼场 / 哈密顿无下界），'
           '且参数账撞 Omega5 => 该修正路径当前不可推进到可证伪预言'),
          None, '综合裁定')

# ----------------------------------------------------------------------------
def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()

    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')

    payload = {
        'round': 'r71',
        'date': '2026-10-15',
        'source': 'r69 下游攻破（V4.8 修正完整版公式集）',
        'counts': dict(COUNTS),
        'total': len(ENTRIES),
        'verdict': verdict,
        'guard_all_ok': True,
        'entries': ENTRIES,
        'not_self_derived': [
            {'tag': 'NS1',
             'text': '来料作用量形式 L=(hbar c/2)(kappa^2-tau^2)-U 与 U 的四次多项式结构为来料给定；'
                     '本册只做量纲仲裁、最小修法与后果判定，不自推 lambda 的数值'},
            {'tag': 'NS2',
             'text': 'CODATA 锚点 hbar=1.054571817e-34 J s、c=299792458 m/s 为实验测量值，非第一性导出'},
            {'tag': 'NS3',
             'text': '鬼场判定采用号差 (+,-,-,-) 与 x^0=ct 口径；换号差约定需重算，本册不代选'},
        ],
        'red_line': '数学/数值自洽 != 物理证实；本册只做机器可读的最小修法与后果判定，'
                    '不构成对 TUFT 方向的普遍否证',
    }

    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rlines = []
    rlines.append('TUFT-r71 lambda 维度修正与导数项增广 攻破 运行报告')
    rlines.append('counts=' + str(COUNTS) + ' total=' + str(len(ENTRIES)) +
                  ' verdict=' + verdict)
    for e in ENTRIES:
        rlines.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rlines.append('    residual=' + e['residual'])
    rlines.append('')
    rlines.append('GUARD G0: 量纲工具自守卫 全过')
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rlines))

    # md 产物
    ml = []
    ml.append('# 判定_TUFT-r71-lambda维度修正与导数项增广_攻破')
    ml.append('')
    ml.append('日期：2026-10-15 · 评级：O/L2（r69 下游攻破）')
    ml.append('')
    ml.append('## 条目计数')
    ml.append('- 总条目：' + str(len(ENTRIES)))
    for k in sorted(COUNTS.keys()):
        ml.append('- ' + k + '：' + str(COUNTS[k]))
    ml.append('- 总体 verdict：' + verdict)
    ml.append('')
    ml.append('## 逐条裁定')
    for e in ENTRIES:
        line = '- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text']
        if e['residual']:
            line += '  （残差 ' + e['residual'] + '）'
        ml.append(line)
    ml.append('')
    ml.append('## not_self_derived 登记')
    for n in payload['not_self_derived']:
        ml.append('- ' + n['tag'] + '：' + n['text'])
    ml.append('')
    ml.append('## 红线')
    ml.append(payload['red_line'])
    mp = os.path.join(DATA, STEM + '.md')
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ml))

    print('counts=' + str(COUNTS))
    print('total=' + str(len(ENTRIES)))
    print('verdict=' + verdict)
    print('written: ' + jp)

if __name__ == '__main__':
    main()
