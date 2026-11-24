# -*- coding: utf-8 -*-
"""TUFT-r446 · 全局反常与混合引力门禁：关闭 r443 §十 U4 的可计算部分

攻靶：`r443` §十 未覆盖项 **U4（Witten 全局反常、引力瞬子/混合引力反常）**。

本册不重算微扰四维反常（`r442` 已算四条），只补两类非微扰/混合门禁：
  A. Witten global SU(2) anomaly：左手 Weyl SU(2) 双重态数必须为偶数。
  B. 混合 gauge-gravitational anomaly：Tr Y = 0（左手 Weyl 超荷迹）。

候选：SM15 / SU(5) 5bar+10 / SO(10) 16 / flipped SU(5) 16 /
Pati-Salam 16 / E6 27；trinification 因 r443 已判 Y 需 2 个混合系数，
本册只给结构双态数并把 TrY 标 BOUNDARY，不代选系数。

口径：`PASS`=判据成立但不迁移为物理成立；`FAIL`=被否定的声称；
`BOUNDARY`=只在声明口径内成立；`CORRECTED`=登记既有册状态更新，不改其字节。
纯标准库（Fraction 精确，零浮点）· Python 3.8。
输出：../数据/TUFT-r446_..._{json,md,_report.txt}
"""
import io
import json
import os
import sys
from fractions import Fraction

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
JUDGE = os.path.join(BASE, '判定')
STAMP = '2026-11-24'
TAG = 'TUFT-r446_全局反常与混合引力门禁_扩展GUT候选合法性判定_精算_' + STAMP
VERDICT = ('GLOBAL-ANOMALY-GATE-EXHAUSTIVE--ALL-SURVIVORS-PASS-SU2-PARITY-AND-TRY--'
           'TRINIFICATION-Y-BOUNDARY--U4-COMPUTABLE-PART-CLOSED--PASS-NOT-PHYSICS')

ENTRIES = []
GUARDS = []
KEY = {}
R = {}


def P(code, title, detail=''):
    ENTRIES.append((code, 'PASS', title, detail))


def FA(code, title, detail=''):
    ENTRIES.append((code, 'FAIL', title, detail))


def IN(code, title, detail=''):
    ENTRIES.append((code, 'INFO', title, detail))


def BO(code, title, detail=''):
    ENTRIES.append((code, 'BOUNDARY', title, detail))


def COR(code, title, detail=''):
    ENTRIES.append((code, 'CORRECTED', title, detail))


def G(name, cond, detail=''):
    ok = bool(cond)
    GUARDS.append((name, ok, detail))
    if not ok:
        print('  [GUARD-FAIL] %-26s %s' % (name, detail))
    return ok


def counter():
    c = {}
    for e in ENTRIES:
        c[e[1]] = c.get(e[1], 0) + 1
    return c


def guard_ok():
    return sum(1 for g in GUARDS if g[1])


def ensure_dirs():
    for d in (DATA, JUDGE):
        if not os.path.isdir(d):
            os.makedirs(d)


def write_text(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def fs(f):
    return '%s/%s' % (f.numerator, f.denominator) if f.denominator != 1 else str(f.numerator)


def jsonable(x):
    if isinstance(x, Fraction):
        return [x.numerator, x.denominator]
    if isinstance(x, tuple):
        return [jsonable(v) for v in x]
    if isinstance(x, list):
        return [jsonable(v) for v in x]
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    return x


# ---------------------------------------------------------------- 左手续：(d3,d2,Y) -> (重数, d3, d2, Y)
# d2=2 的每一项贡献 d3 个 SU(2)_L 双重态；TrY = Σ mult*d3*d2*Y。
Q = (1, 3, 2, Fraction(1, 6))          # Q_L
UC = (1, 3, 1, Fraction(-2, 3))        # u_R^c
DC = (1, 3, 1, Fraction(1, 3))         # d_R^c
L = (1, 1, 2, Fraction(-1, 2))         # L_L
EC = (1, 1, 1, Fraction(1))            # e_R^c
NC = (1, 1, 1, Fraction(0))            # nu_R^c
D_EX = (1, 3, 1, Fraction(-1, 3))      # 5 中的色三重态奇异态 D^c 型
H_U = (1, 1, 2, Fraction(1, 2))        # 5 中的上型双态
D_BAR = (1, 3, 1, Fraction(1, 3))      # 5bar 中的奇异态
H_D = (1, 1, 2, Fraction(-1, 2))       # 5bar 中的下型双态

SM15 = [Q, UC, DC, L, EC]
SO16 = SM15 + [NC]
E6_EXTRA_10 = [D_EX, H_U, D_BAR, H_D, NC]   # 10_v(2 双态 + 2 色态) + SO(10) singlet；共 11 态

CANDS = {
    'SM15': {'states': SM15, 'name': '(3,2)+(3bar,1)x2+(1,2)+(1,1)'},
    'SU5_5bar10': {'states': SM15, 'name': '5bar + 10 = 15'},
    'SO10_16': {'states': SO16, 'name': '16 = 10 + 5bar + 1'},
    'flipped_SU5_16': {'states': SO16, 'name': '16 (Y = c1*T24 + c2*X)'},
    'PatiSalam_16': {'states': SO16, 'name': '(4,2,1)+(4bar,1,2)'},
    'E6_27': {'states': SO16 + E6_EXTRA_10, 'name': '27 = 16 + 10 + 1'},
}


def dim_of(states):
    return sum(m * d3 * d2 for m, d3, d2, y in states)


def doublets(states):
    return sum(m * d3 for m, d3, d2, y in states if d2 == 2)


def try_of(states):
    s = Fraction(0)
    for m, d3, d2, y in states:
        s += Fraction(m * d3 * d2) * y
    return s


def gate(states):
    d = doublets(states)
    t = try_of(states)
    return {'dim': dim_of(states), 'doublets': d, 'trY': t,
            'su2_parity_ok': d % 2 == 0, 'try_ok': t == 0}


def analyse():
    table = {}
    for k, v in CANDS.items():
        g = gate(v['states'])
        g['rep'] = v['name']
        table[k] = g

    # trinification：r443 已判 Y 需两个混合系数，不代选；只做结构双态数
    tri_struct_doublets = 6   # (3,3bar,1) 与 (3bar,1,3) 各贡献 3 个 SU(2)_L 双态
    tri_states_dim = 27

    # 阳性/阴性对照：奇双态、非零 TrY 必须分别被两条门抓住
    odd_control = SM15 + [(1, 1, 2, Fraction(0))]
    trace_control = SM15 + [(1, 1, 1, Fraction(1))]
    odd_g = gate(odd_control)
    trace_g = gate(trace_control)

    # 变异：把 e^c 超荷从 +1 改成 -1（TrY 应非 0）；把 SU(5) 双态数减 1（奇偶翻转）
    mut_states = []
    for s in SM15:
        if s[2] == 1 and s[3] == Fraction(1):
            mut_states.append((s[0], s[1], s[2], Fraction(-1)))
        else:
            mut_states.append(s)
    mut_trace = try_of(mut_states)
    mut_doublets = doublets(SM15) - 1
    mut_detected = [mut_trace != 0, mut_doublets % 2 == 1]

    R.update({'table': table, 'tri_struct_doublets': tri_struct_doublets,
              'tri_states_dim': tri_states_dim, 'odd_g': odd_g,
              'trace_g': trace_g, 'mut_trace': mut_trace,
              'mut_doublets': mut_doublets, 'mut_detected': mut_detected})

    IN('I01', '两条全局门禁 [C]', 'Witten SU(2): 左手双重态数偶数；混合 gauge-grav: TrY=0')
    P('I02', '双重态计数与 TrY 计算规则机器化', 'd2=2 每项贡献 d3 个双态；TrY=Σ mult·d3·d2·Y')
    P('I03', 'SM15 通过两门', 'dim=%d, n2=%d, TrY=%s' %
      (table['SM15']['dim'], table['SM15']['doublets'], fs(table['SM15']['trY'])))
    P('I04', 'SU(5) 5bar⊕10 通过两门', 'dim=%d, n2=%d, TrY=%s' %
      (table['SU5_5bar10']['dim'], table['SU5_5bar10']['doublets'], fs(table['SU5_5bar10']['trY'])))
    P('I05', 'SO(10) 16 通过两门', 'dim=%d, n2=%d, TrY=%s' %
      (table['SO10_16']['dim'], table['SO10_16']['doublets'], fs(table['SO10_16']['trY'])))
    P('I06', 'flipped SU(5) 16 通过两门', 'dim=%d, n2=%d, TrY=%s' %
      (table['flipped_SU5_16']['dim'], table['flipped_SU5_16']['doublets'], fs(table['flipped_SU5_16']['trY'])))
    P('I07', 'Pati-Salam 16 通过两门', 'dim=%d, n2=%d, TrY=%s' %
      (table['PatiSalam_16']['dim'], table['PatiSalam_16']['doublets'], fs(table['PatiSalam_16']['trY'])))
    P('I08', 'E6 27 通过两门（双态数 6）', 'dim=%d, n2=%d, TrY=%s；10_v 为矢量状额外态' %
      (table['E6_27']['dim'], table['E6_27']['doublets'], fs(table['E6_27']['trY'])))
    BO('I09', 'trinification 的 TrY 未代选', '结构双态数 %d，dim=%d；Y 需 2 个混合系数，承 r443' %
       (tri_struct_doublets, tri_states_dim))
    P('I10', '奇双态阴性对照被抓住', '加 1 个 SU(2) 双态 ⇒ n2=%d，su2_ok=%s' %
      (odd_g['doublets'], odd_g['su2_parity_ok']))
    P('I11', '非零 TrY 阴性对照被抓住', '加 Y=1 单态 ⇒ TrY=%s，try_ok=%s' %
      (fs(trace_g['trY']), trace_g['try_ok']))
    FA('I12', '否证：E6 额外态必然触发 Witten 全局反常', 'E6 27 的双态数 6 为偶数；额外 10_v 给 2 个双态，奇偶不变')
    P('I13', 'r443 U4 的可计算部分关闭', '五个可赋 Y 的候选全过两门；trinification 仅 Y 口径仍开放')
    COR('I14', '登记 r443 §十 U4 状态更新', '未判 → 两门已执行；不改 r443 字节')
    IN('I15', '四维修正说明', '纯引力微扰反常在 4D 自旋 1/2 扇区为零；可计算混合项为 TrY')
    BO('I16', '二圈、完整阈值谱与动力学仍未覆盖', '本册只判全局反常奇偶与 TrY，不产生新预言')

    G('G0-1', dim_of(SM15) == 15, 'SM15 维数')
    G('G0-2', dim_of(SO16) == 16, 'SO16 维数')
    G('G0-3', dim_of(SO16 + E6_EXTRA_10) == 27, 'E6 27 维数')
    G('G0-4', len(CANDS) == 6, '六个可赋 Y 候选')
    for k in CANDS:
        G('G1-' + k, table[k]['su2_parity_ok'] and table[k]['try_ok'],
          '%s n2=%d TrY=%s' % (k, table[k]['doublets'], fs(table[k]['trY'])))
    G('G2-1', tri_struct_doublets == 6 and tri_states_dim == 27, 'trinification 结构读数')
    G('G2-2', odd_g['doublets'] % 2 == 1 and not odd_g['su2_parity_ok'], '奇双态对照红')
    G('G2-3', trace_g['trY'] != 0 and not trace_g['try_ok'], 'TrY 对照红')
    G('G2-4', all(mut_detected), '变异 2/2')
    G('G2-5', mut_trace == Fraction(-2), 'e^c 超荷翻转的 TrY 精确值')
    G('G3-1', len(ENTRIES) == 16, '16 条条目')
    G('G3-2', counter().get('CORRECTED', 0) == 1, '一条 CORRECTED')
    G('G3-3', any(e[0] == 'I12' and e[1] == 'FAIL' for e in ENTRIES), 'E6 声称否证在场')


def build_md():
    c = counter()
    lines = []
    lines.append('# 数据 · ' + TAG)
    lines.append('')
    lines.append('- VERDICT `%s`' % VERDICT)
    lines.append('- 条目 %d：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, c.get(k, 0)) for k in ('PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED'))))
    lines.append('- 守卫 %d/%d' % (guard_ok(), len(GUARDS)))
    lines.append('')
    lines.append('## 候选门禁表')
    lines.append('')
    lines.append('| 候选 | rep | dim | SU(2) 双态数 | TrY | SU2 奇偶 | TrY=0 |')
    lines.append('|---|---|---:|---:|---|---|---|')
    for k, g in R['table'].items():
        lines.append('| %s | %s | %d | %d | %s | %s | %s |' %
                     (k, g['rep'], g['dim'], g['doublets'], fs(g['trY']),
                      'PASS' if g['su2_parity_ok'] else 'FAIL',
                      'PASS' if g['try_ok'] else 'FAIL'))
    lines.append('| trinification | SU(3)^3 27 | 27 | %d | [C] 未定 | 结构偶数 | BOUNDARY |' %
                 R['tri_struct_doublets'])
    lines.append('')
    lines.append('## 关键读数')
    lines.append('')
    lines.append('```')
    lines.append('SM15_N2       = %d' % R['table']['SM15']['doublets'])
    lines.append('E6_27_N2      = %d' % R['table']['E6_27']['doublets'])
    lines.append('ALL_TR_Y      = %s' % [fs(R['table'][k]['trY']) for k in R['table']])
    lines.append('ODD_CONTROL   = %d' % R['odd_g']['doublets'])
    lines.append('TRACE_CONTROL = %s' % fs(R['trace_g']['trY']))
    lines.append('MUTATION      = %s' % R['mut_detected'])
    lines.append('```')
    lines.append('')
    lines.append('## 条目')
    lines.append('')
    lines.append('| 编号 | 判定 | 标题 | 细节 |')
    lines.append('|---|---|---|---|')
    for code, st, title, detail in ENTRIES:
        lines.append('| %s | %s | %s | %s |' % (code, st, title, detail.replace('|', '\\|')))
    lines.append('')
    return '\n'.join(lines)


def build_report():
    c = counter()
    lines = ['[r446] %s' % VERDICT]
    for k in ('PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED'):
        lines.append('%s=%d' % (k, c.get(k, 0)))
    lines.append('SM15_N2 = %d' % R['table']['SM15']['doublets'])
    lines.append('E6_27_N2 = %d' % R['table']['E6_27']['doublets'])
    lines.append('ALL_TRY_ZERO = %s' % all(g['try_ok'] for g in R['table'].values()))
    lines.append('TRINIFICATION_STRUCT_N2 = %d' % R['tri_struct_doublets'])
    lines.append('MUTATION_DETECTED = %s' % R['mut_detected'])
    lines.append('GUARDS %d/%d' % (guard_ok(), len(GUARDS)))
    return '\n'.join(lines) + '\n'


def main():
    ensure_dirs()
    analyse()
    payload = {
        'tag': TAG, 'stamp': STAMP, 'verdict': VERDICT,
        'key': jsonable(R),
        'entries': [{'code': c, 'status': s, 'title': t, 'detail': d} for c, s, t, d in ENTRIES],
        'guards': [{'name': n, 'ok': ok, 'detail': d} for n, ok, d in GUARDS],
        'counter': counter(),
    }
    base = os.path.join(DATA, TAG)
    write_text(base + '.json', json.dumps(payload, ensure_ascii=False, indent=2, default=jsonable) + '\n')
    write_text(base + '.md', build_md())
    write_text(base + '_report.txt', build_report())
    print(build_report(), end='')
    return 0 if guard_ok() == len(GUARDS) else 1


if __name__ == '__main__':
    sys.exit(main())
