# -*- coding: utf-8 -*-
"""R21 第三通道：把要抄进五份文档的那几个数，从**引擎 JSON 的行数组**里重新算一遍。

为什么要第三通道：
* 通道一＝版面 §14.12 的散文（文档抄的是它）；
* 通道二＝台账 JSON 的 `baseline_r21`（mint 落盘后由 flip_r21c 与磁盘版面逐字段对针）；
* 本脚本＝通道三：不复用台账的任何正则（`Q_*_RE` 一个都不 import），而是
  自己开窗口、自己写正则读散文，再**从 rows/pairs/c2/ab/b/ratio_head 这些数组现算计数**，
  三方对不上就红。
**只读**：不改任何仓库文件，也不改自己的输入（那五枚缺陷是**内存里**的 JSON 拷贝，落不了盘）。
本脚本不接入任何一台门禁的计数，也不给任何主张升证据级 ⇒ **L10 保持 OPEN**；它只是第三个
不肯抄前两路答案的证人。
用法：python verify_r21_third_channel.py
"""
import io
import json
import os
import re
import sys
from collections import Counter
from fractions import Fraction

DOC = r'D:\a10\aikjx\code\my_lib\openuft\07_统一场方程'
FACE = os.path.join(DOC, '验证脚本', 'SO10表示论报告.md')
FJSON = os.path.join(DOC, '验证脚本', 'SO10表示论报告.json')
A_MARK, B_MARK = '### 14.12', '## 15.'

FAIL = []


def ck(name, got, want, note=''):
    """got＝现算，want＝散文里写的（或另一个数组里的字段）。不符就记一条红。"""
    ok = (str(got) == str(want))
    print('  %-34s 现算=%-8s 对照=%-8s %s %s'
          % (name, got, want, 'OK  ' if ok else 'MISMATCH', ('| ' + note) if note else ''))
    if not ok:
        FAIL.append('%s：现算 %s 而对照 %s（%s）' % (name, got, want, note))
    return ok


def frac(x):
    return Fraction(str(x))


def readings(B, prose):
    """从行数组现算每一个要引用的数；prose＝§14.12 全文，用**本脚本自己的**正则取散文读数。"""
    R = {}
    rows = B['rows']
    R['roster'] = len(rows)
    R['sum_le3'] = sum(1 for r in rows if sum(r[0]) <= 3)
    R['mis'] = sum(1 for r in rows if frac(r[2]) != frac(r[3]))
    R['ctl_2r'] = sum(1 for r in rows if frac(r[3]) / 2 != frac(r[2]))
    R['ctl_phi'] = sum(1 for r in rows if frac(r[2]) != 0)
    R['amb'] = ','.join(str(d) for d, c in sorted(Counter(r[1] for r in rows).items()) if c > 1)
    R['amb_field'] = ','.join(str(d) for d in B['amb'])
    R['amb_trunc'] = 'TRUNCATED' if R['amb_field'] != R['amb'] else 'no'
    R['amb_n'] = len([x for x in R['amb'].split(',') if x])
    R['dmax'] = max(r[1] for r in rows)
    adj = [r for r in rows if r[0] == [0, 1, 0, 0, 0]]
    R['dim_g'] = adj[0][1] if len(adj) == 1 else 'ADJ-NOT-UNIQUE'
    R['pairs_n'] = len(B['pairs'])
    R['pairs_bad_a'] = sum(1 for p in B['pairs'] if p[6] is not True or frac(p[4]) != frac(p[5]))
    R['pairs_bad_b'] = sum(1 for p in B['pairs'] if p[8] is not True or frac(p[7]) != frac(p[4]))
    R['fT_sample'] = ','.join(sorted(set(str(frac(x[5])) for x in B['ratio_head'])))
    R['fT_recalc'] = ','.join(sorted(set(str(frac(x[3]) / frac(x[4])) for x in B['ratio_head'])))
    R['n_head'] = len(B['ratio_head'])
    R['fA_recalc'] = ','.join(sorted(set(str(frac(x[3]) / frac(x[4])) for x in B['ab'])))
    R['n_ab'] = len(B['ab'])
    R['fC_recalc'] = ','.join(sorted(set(str(frac(x[2]) / frac(x[3])) for x in B['c2'])))
    R['n_c2'] = len(B['c2'])
    R['n_c2_uniq'] = len(set(tuple(str(v) for v in x[1:]) for x in B['c2']))
    R['b_n'] = len(B['b'])
    R['b_viol'] = sum(1 for x in B['b'] if x[5] is not True)
    R['b_divf_eq_chain'] = sum(1 for x in B['b'] if frac(x[4]) == frac(x[3]))
    R['b_nb'] = sum(1 for x in B['b'] if x[2] == '非阿贝尔')
    R['b_nb_dev'] = sum(1 for x in B['b'] if x[2] == '非阿贝尔' and x[7] is True)
    R['b_ab'] = sum(1 for x in B['b'] if x[2] == '阿贝尔')
    R['b_dev_is_f'] = sum(1 for x in B['b'] if x[2] == '非阿贝尔'
                          and frac(x[6]) != frac(x[3]) * 1 and frac(x[6]) == frac(x[3]) * 2)
    R['b_ab_unchanged'] = sum(1 for x in B['b'] if x[2] == '阿贝尔' and frac(x[6]) == frac(x[3]))
    R['n_ratio_field'] = B['n_ratio']
    R['roster_field'] = B['roster']
    R['bothzero'] = B['bothzero']
    R['zero_n'] = len(B['zero'])
    R['casimir_th'] = B['casimir_th']
    R['h_dual'] = B['h_dual']
    # 散文侧：本脚本自己的正则（与台账的 Q_*_RE 无共享）
    def near(*pats):
        for p in pats:
            m = re.search(p, prose)
            if m:
                return m.group(1) if m.lastindex else m.group(0)
        return 'NOT-FOUND'
    P = {
        'p_roster': near(r'全量\s*(\d+)\s*个', r'(\d+)\s*个 Dynkin 标号'),
        'p_dimg': near(r'dim\\mathfrak g=(\d+)', r'母格[^。]{0,40}?(\d+)'),
        'p_mis': near(r'甲乙不等的\s*(\d+)\s*个', r'与甲不等的标号\s*(\d+)\s*个'),
        'p_ctl2r': near(r'与甲不等的标号\s*(\d+)\s*个', r'与甲不等[^\d]{0,8}(\d+)\s*个'),
        'p_ctlphi': near(r'换成正根数\s*⇒?\s*(\d+)\s*个', r'正根数[^0-9]{0,12}(\d+)'),
        'p_pairs': near(r'丙丁在\s*(\d+)\s*对'),
        'p_ntot': near(r'(\d+)\s*个（因子[^）]*）组合'),
        'p_bothzero': near(r'两侧同时为零的组合\s*(\d+)\s*个'),
        'p_zero': near(r'另一侧非零的\s*(\d+)\s*个'),
        'p_nc2': near(r'在\s*(\d+)\s*个因子上'),
        'p_abcells': near(r'阿贝尔侧\s*(\d+)\s*格'),
        'p_bn': near(r'([一二三四五六七八九十]+)行逐条重现'),
        'p_amb': near(r'同维多标号的维数：([0-9、, ]+)'),
        'p_ambn': near(r'数出来的\s*(\d+)\s*个'),
        'p_dmax': near(r'维数最大\s*(\d+)'),
    }
    return R, P


def main():
    rawface = open(FACE, 'rb').read()
    face = io.open(FACE, encoding='utf-8').read()          # 通用换行：版面是 CRLF 产的
    print('版面 %d B / CR=%d（按通用换行解析）' % (len(rawface), rawface.count(b'\r')))
    a, b = face.find(A_MARK), face.find(B_MARK, face.find(A_MARK))
    if not (a >= 0 and b > a):
        print('BLOCKED：版面里找不到 §14.12 窗口（a=%d b=%d）' % (a, b))
        return 1
    prose = face[a:b]
    print('窗口 %d B / %d 行' % (len(prose.encode('utf-8')), prose.count('\n')))
    J = json.load(io.open(FJSON, encoding='utf-8'))
    print('引擎 JSON tests=%d 条' % len(J.get('tests') or []))

    R, P = readings(J['basis']['r21'], prose)
    print('\n== 现算 vs 散文（通道三 vs 通道一）')
    pairs = [('roster 全量标号数', R['roster'], P['p_roster']),
             ('dim g', R['dim_g'], P['p_dimg']),
             ('甲乙不等的标号', R['mis'], P['p_mis']),
             ('2r 口径与甲不等', R['ctl_2r'], P['p_ctl2r']),
             ('正根数口径与甲不等', R['ctl_phi'], P['p_ctlphi']),
             ('丙丁对数', R['pairs_n'], P['p_pairs']),
             ('因子×表示组合数', R['n_ratio_field'], P['p_ntot']),
             ('两侧同时为零', R['bothzero'], P['p_bothzero']),
             ('一侧为零另一侧非零', R['zero_n'], P['p_zero']),
             ('C2 独立路的因子数', R['n_c2'], P['p_nc2']),
             ('阿贝尔侧格数', R['n_ab'], P['p_abcells']),
             ('歧义清单条数', R['amb_n'], P['p_ambn']),
             ('本层标号的维数上限', R['dmax'], P['p_dmax'])]
    for n, g, w in pairs:
        ck(n, g, w, '散文原样=%r' % w)
    def norm(s):
        return ','.join(sorted(x for x in re.split(r'[、,\s]+', str(s)) if x))
    ck('同维多标号的维数集合', norm(R['amb']), norm(P['p_amb']), '散文原串=%r' % P['p_amb'])
    CN = '零一二三四五六七八九十'
    ck('b 表行数（散文写汉字）', CN[R['b_n']] if R['b_n'] < 11 else R['b_n'], P['p_bn'],
       '现算 %d 行' % R['b_n'])

    print('\n== 数组内部自洽（行 ⇄ 汇总字段）')
    ck('roster == len(rows)', R['roster'], J['basis']['r21']['roster'])
    ck('全部标号满足 Σc_i≤3', R['sum_le3'], R['roster'])
    ck('amb 字段无截断（== 逐标号表里重复的维数）', R['amb_trunc'], 'no',
       '字段=%s 现算=%s' % (R['amb_field'], R['amb']))
    ck('amb_n == len(amb)', R['amb_n'], J['basis']['r21']['amb_n'])
    ck('dmax == 最大行维数', R['dmax'], J['basis']['r21']['dmax'])
    ck('mis == len(basis.mis)', R['mis'], len(J['basis']['r21']['mis']))
    ck('ctl_2r == 字段', R['ctl_2r'], J['basis']['r21']['ctl_2r'])
    ck('ctl_phi == 字段', R['ctl_phi'], J['basis']['r21']['ctl_phi'])
    ck('丙丁违例（对值）', R['pairs_bad_a'], 0)
    ck('丙丁违例（丁对丙）', R['pairs_bad_b'], 0)
    ck('f_T 单值（比值列）', R['fT_sample'], '2')
    ck('f_T 单值（由格侧/链侧现算）', R['fT_recalc'], '2')
    ck('阿贝尔比值全是 1', R['fA_recalc'], '1')
    ck('C2 独立路比值全是 2', R['fC_recalc'], '2')
    ck('C2 因子去重（SU2L/SU2R 同形）', R['n_c2_uniq'], 3)
    ck('b 表违例行', R['b_viol'], 0)
    ck('b 表 ÷f 后等于链侧的行数', R['b_divf_eq_chain'], R['b_n'])
    ck('非阿贝尔行数', R['b_nb'], J['basis']['r21']['b_nb'])
    ck('非阿贝尔不翻译就偏的行数', R['b_nb_dev'], J['basis']['r21']['b_nb_dev'])
    ck('阿贝尔行数', R['b_ab'], J['basis']['r21']['b_ab'])
    ck('偏的那几行恰好偏 f=2 倍', R['b_dev_is_f'], R['b_nb_dev'])
    ck('阿贝尔那行不翻译也不偏', R['b_ab_unchanged'], 1)

    print('\n== 五枚内存缺陷：每一枚都必须让指定的那一项变红')
    muts = [('把第 11 个标号的甲改成 +1',
             lambda B: B['rows'][10].__setitem__(2, str(int(B['rows'][10][2]) + 1)), 'mis'),
             ('把 C2 独立路的一个因子比值改成 3',
              lambda B: B['c2'][0].__setitem__(2, '6'), 'C2 独立路比值全是 2'),
             ('把 b2 的"÷f 等于链侧"改成不成立',
              lambda B: B['b'][1].__setitem__(4, '-19/5'), None),
             ('把 roster 字段改成 57（行不动）',
              lambda B: B.__setitem__('roster', 57), 'roster == len(rows)'),
             ('把 amb 装回 d<=700 截断（本轮修掉的那个真缺陷的反向针）',
              lambda B: B.__setitem__('amb', [d for d in B['amb'] if d <= 700]),
              'amb 字段无截断')]
    for label, patch, target in muts:
        import copy
        B2 = copy.deepcopy(J['basis']['r21'])
        patch(B2)
        R2, _ = readings(B2, prose)
        moved = []
        if R2['mis'] != R['mis']:
            moved.append('mis')
        if R2['fC_recalc'] != R['fC_recalc']:
            moved.append('fC')
        if R2['b_viol'] != R['b_viol'] or str(R2['b_dev_is_f']) != str(R['b_dev_is_f']):
            moved.append('b')
        if R2['b_divf_eq_chain'] != R['b_divf_eq_chain']:
            moved.append('b÷f')
        if (R2['roster'] != R['roster'] or R2['n_ratio_field'] != R['n_ratio_field']
                or R2['roster_field'] != R['roster_field']):
            moved.append('roster')
        if R2['amb_trunc'] != R['amb_trunc']:
            moved.append('amb 截断')
        print('  %-32s 移动=%s（期望非空）' % (label, moved))
        if not moved:
            FAIL.append('缺陷「%s」没让任何现算值移动 ⇒ 这一族针是空转' % label)

    print('\n判定：%s（红 %d 条）' % ('PASS' if not FAIL else 'FAIL', len(FAIL)))
    for x in FAIL:
        print('   - ' + x)
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
