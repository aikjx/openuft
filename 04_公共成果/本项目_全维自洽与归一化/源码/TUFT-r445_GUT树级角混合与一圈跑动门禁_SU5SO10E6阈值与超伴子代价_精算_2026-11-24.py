# -*- coding: utf-8 -*-
"""TUFT-r445 · GUT 树级角混合与一圈跑动门禁：关闭 r443 §十 U2

攻靶：`r443` §十 未覆盖项 **U2（RG 跑动与阈值，sin²θ_W=3/8 为树级结论、未重算）**。

本册只做可机器复核的一圈门禁：
  1. 验证 SU(5) GUT 归一的树级 `sin²θ_W = 3/(3+5) = 3/8`，与实验中心值对拍；
  2. 用外部输入的 M_Z 耦合做 SM 一圈 RGE，检查三线交点是否重合；
  3. 反解让 b1/b2 交点与 b3 对齐所需的 α_s，判断中心值能否救回；
  4. 以 M_SUSY=1 TeV 为门槛做 SM→MSSM 两段跑动，验证超伴子确实给出汇聚；
  5. 给阈值修正与超伴子扇区定价，不把「加了超伴子」误记为 TUFT 预言。

口径：`PASS`=判据成立但不迁移为物理成立；`FAIL`=被否定的声称；
`BOUNDARY`=只在声明口径内成立；`CORRECTED`=登记 r443 U2 状态更新，不改其字节。
纯标准库（Decimal 60 位 + Fraction 系数）· Python 3.8。
输出：../数据/TUFT-r445_..._{json,md,_report.txt}
"""
import io
import json
import os
import sys
from decimal import Decimal, localcontext
from fractions import Fraction

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
JUDGE = os.path.join(BASE, '判定')
STAMP = '2026-11-24'
TAG = 'TUFT-r445_GUT树级角混合与一圈跑动门禁_SU5SO10E6阈值与超伴子代价_精算_' + STAMP
VERDICT = ('TREE-ANGLE-3-8-EXCLUDED--SM-1LOOP-NONUNIFICATION--MSSM-UNIFIES-ONLY-WITH-EXTERNAL-SPARTNERS--'
           'THRESHOLD-IS-FREE-INPUT--U2-CLOSED-AT-1LOOP--PASS-NOT-PHYSICS')

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


def D(x):
    return x if isinstance(x, Decimal) else Decimal(str(x))


def dec_frac(f):
    return D(f.numerator) / D(f.denominator)


def fm(x, n=10):
    x = D(x)
    return format(x, '.' + str(n) + 'E')


# ---------------------------------------------------------------- 外部输入 [C]
# M_Z 处电磁耦合、弱混合角、强耦合均取外部中心值；本册不重新拟合 PDG。
INPUT = {
    'M_Z_GeV': '91.1876',
    'alpha_em_MZ': '0.0078156',
    'sin2_theta_W': '0.23121',
    'alpha_3_MZ': '0.1180',
    'M_SUSY_GeV': '1000',
}
B_SM = (Fraction(41, 10), Fraction(-19, 6), Fraction(-7))
B_MSSM = (Fraction(33, 5), Fraction(1), Fraction(-3))
TREE_SIN2 = Fraction(3, 8)
UNIFY_TOL_EFOLD = D('1.00')   # 一圈门禁：三交点跨度超过 1 e-fold（约 e 倍能标）判不汇聚


def slopes(bs):
    pi = D('3.1415926535897932384626433832795028841971693993751058209749445923078164')
    return tuple(-dec_frac(b) / (D(2) * pi) for b in bs)


def run_inv(a_inv, bs, L):
    s = slopes(bs)
    L = D(L)
    return tuple(D(a_inv[i]) + s[i] * L for i in range(3))


def inter_L(a_inv, bs, i, j):
    s = slopes(bs)
    return (D(a_inv[j]) - D(a_inv[i])) / (s[i] - s[j])


def spread(vals):
    vals = [D(v) for v in vals]
    return max(vals) - min(vals)


def jsonable(x):
    if isinstance(x, Decimal):
        return format(x, '.30E')
    if isinstance(x, Fraction):
        return [x.numerator, x.denominator]
    if isinstance(x, tuple):
        return [jsonable(v) for v in x]
    if isinstance(x, list):
        return [jsonable(v) for v in x]
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    return x


def analyse():
    with localcontext() as ctx:
        ctx.prec = 60
        mz = D(INPUT['M_Z_GeV'])
        ms = D(INPUT['M_SUSY_GeV'])
        aem = D(INPUT['alpha_em_MZ'])
        s2 = D(INPUT['sin2_theta_W'])
        a3 = D(INPUT['alpha_3_MZ'])

        a2 = aem / s2
        a1 = D(5) / D(3) * aem / (D(1) - s2)
        a_inv = (D(1) / a1, D(1) / a2, D(1) / a3)

        tree = D(TREE_SIN2.numerator) / D(TREE_SIN2.denominator)
        tree_rel = (tree - s2) / s2

        # SM-only 一圈交点
        L12 = inter_L(a_inv, B_SM, 0, 1)
        L13 = inter_L(a_inv, B_SM, 0, 2)
        L23 = inter_L(a_inv, B_SM, 1, 2)
        sm_spread = spread((L12, L13, L23))
        sm_unify = sm_spread <= UNIFY_TOL_EFOLD

        # 让 b3 在 L12 与 b1/b2 同点所需的 α_s(M_Z)
        s_sm = slopes(B_SM)
        common_12 = D(a_inv[0]) + s_sm[0] * L12
        a3req_inv = common_12 - s_sm[2] * L12
        a3req = D(1) / a3req_inv
        a3gap_inv = a3req_inv - D(a_inv[2])

        # 若允许 GUT 阈值修正 δA3，把 SM-only 在 L12 的 A3 抬到公共值
        a3_at_l12 = D(a_inv[2]) + s_sm[2] * L12
        delta_a3_inv_gut = common_12 - a3_at_l12
        threshold_factor = (delta_a3_inv_gut / s_sm[2]).exp() if delta_a3_inv_gut > 0 else D(0)

        # MSSM 两段跑动：MZ→M_SUSY 用 SM，M_SUSY→GUT 用 MSSM
        Ls = (ms / mz).ln()
        a_susy = run_inv(a_inv, B_SM, Ls)
        m12 = inter_L(a_susy, B_MSSM, 0, 1)
        m13 = inter_L(a_susy, B_MSSM, 0, 2)
        m23 = inter_L(a_susy, B_MSSM, 1, 2)
        mssm_spread = spread((m12, m13, m23))
        mssm_unify = mssm_spread <= UNIFY_TOL_EFOLD
        mssm_L = (m12 + m13 + m23) / D(3)
        a_gut_mssm = run_inv(a_susy, B_MSSM, mssm_L)
        alpha_gut_mssm = D(1) / ((a_gut_mssm[0] + a_gut_mssm[1] + a_gut_mssm[2]) / D(3))
        m_gut = ms * mssm_L.exp()

        # 变异测试：改变 b3 或 α_s 必须改变 SM-only 交点跨度读数
        b_mut = list(B_SM)
        b_mut[2] = Fraction(-6)
        mut_b_spread = spread((inter_L(a_inv, tuple(b_mut), 0, 1),
                               inter_L(a_inv, tuple(b_mut), 0, 2),
                               inter_L(a_inv, tuple(b_mut), 1, 2)))
        a_inv_mut = (a_inv[0], a_inv[1], D(1) / D('0.2000'))
        mut_a_spread = spread((inter_L(a_inv_mut, B_SM, 0, 1),
                               inter_L(a_inv_mut, B_SM, 0, 2),
                               inter_L(a_inv_mut, B_SM, 1, 2)))
        mut_detected = [
            abs(mut_b_spread - sm_spread) > D('0.01'),
            abs(mut_a_spread - sm_spread) > D('0.01'),
        ]

        R.update({
            'a_inv': a_inv,
            'a1': a1, 'a2': a2, 'a3': a3,
            'tree': tree, 'tree_rel': tree_rel,
            'L12': L12, 'L13': L13, 'L23': L23, 'sm_spread': sm_spread,
            'sm_unify': sm_unify,
            'a3req': a3req, 'a3req_inv': a3req_inv, 'a3gap_inv': a3gap_inv,
            'delta_a3_inv_gut': delta_a3_inv_gut, 'threshold_factor': threshold_factor,
            'Ls': Ls, 'a_susy': a_susy,
            'm12': m12, 'm13': m13, 'm23': m23, 'mssm_spread': mssm_spread,
            'mssm_unify': mssm_unify, 'mssm_L': mssm_L,
            'a_gut_mssm': a_gut_mssm, 'alpha_gut_mssm': alpha_gut_mssm, 'm_gut': m_gut,
            'mut_b_spread': mut_b_spread, 'mut_a_spread': mut_a_spread,
            'mut_detected': mut_detected,
        })

        # ---------------- 条目
        IN('I01', '外部耦合输入 [C]', 'alpha_em=%s, sin2=%s, alpha3=%s, MZ=%s GeV' %
           (fm(aem, 8), fm(s2, 8), fm(a3, 8), mz))
        P('I02', 'SU(5) GUT 归一给树级 sin²θ_W=3/8', '%s = 0.375，归一因子 sqrt(5/3) 双端同源' % fm(tree, 12))
        FA('I03', '树级 3/8 与实验中心值冲突', 'rel=%s（62.19%%），不是小修正' % fm(tree_rel, 8))
        P('I04', '一圈 β 系数符号自检', 'b_SM=(41/10,-19/6,-7)：b1>0、b2/b3<0；MSSM=(33/5,1,-3)')
        P('I05', 'SM-only 三条两两交点机器派生', 'L12=%s, L13=%s, L23=%s e-fold' %
           (fm(L12, 8), fm(L13, 8), fm(L23, 8)))
        FA('I06', 'SM-only 一圈不汇聚', 'ΔL=%s e-fold > 容差 %s' % (fm(sm_spread, 8), fm(UNIFY_TOL_EFOLD, 2)))
        P('I07', '中心值 α_s 无法救回 b1/b2 交点', '需 alpha3=%s（现 %s），Δ(alpha3^-1)=%s' %
           (fm(a3req, 8), fm(a3, 8), fm(a3gap_inv, 8)))
        BO('I08', 'GUT 阈值修正可形式对齐但成为自由输入', 'delta(A3^-1)=%s 对应阈值分裂因子约 %s' %
           (fm(delta_a3_inv_gut, 8), fm(threshold_factor, 4)))
        P('I09', 'MSSM 两段一圈跑动汇聚', 'L12=%s, L13=%s, L23=%s，ΔL=%s' %
           (fm(m12, 8), fm(m13, 8), fm(m23, 8), fm(mssm_spread, 8)))
        FA('I10', 'MSSM 汇聚的物理代价未被 TUFT 派生', '需加入整套超伴子谱；这是新扇区，不是一个可调常数')
        P('I11', 'SU(5)/SO(10)/E6 共享同一树级角归一', '只要第一步按 SU(5) 归一，g1/g2 比相同，树级仍 3/8')
        P('I12', '变异测试抓住假阴性', '改 b3=%s 得 ΔL=%s；改 alpha3=0.2 得 ΔL=%s' %
           (str(b_mut[2]), fm(mut_b_spread, 8), fm(mut_a_spread, 8)))
        COR('I13', '登记 r443 §十 U2 状态更新', '未重算 → 一圈门禁已执行；不改 r443 字节')
        IN('I14', 'MSSM 汇聚尺度读数', 'M_GUT≈%s GeV，alpha_GUT≈%s' %
           (fm(m_gut, 6), fm(alpha_gut_mssm, 8)))
        BO('I15', '二圈、阈值谱与质子衰变未纳入', '本册一圈门禁只关 U2 的一圈部分，不宣称完整 GUT 排除')

        # ---------------- 守卫
        G('G0-1', abs(tree - D('0.375')) < D('1e-30'), '树级 3/8')
        G('G0-2', tree_rel > D('0.6'), '树级相对偏差 >60%')
        G('G0-3', B_SM[0] > 0 and B_SM[1] < 0 and B_SM[2] < 0, 'SM β 符号')
        G('G0-4', B_MSSM[0] > 0 and B_MSSM[1] > 0 and B_MSSM[2] < 0, 'MSSM β 符号')
        G('G1-1', L12 > 0 and L13 > 0 and L23 > 0, '三条交点均在 MZ 之上')
        G('G1-2', sm_spread > D('3'), 'SM 交点跨度 >3 e-fold')
        G('G1-3', not sm_unify, 'SM-only 判不汇聚')
        G('G1-4', a3req < a3 and a3gap_inv > 0, '需更低 alpha_s')
        G('G1-5', delta_a3_inv_gut > 0 and threshold_factor > 1, '阈值修正方向与因子')
        G('G2-1', Ls > 0, 'MZ→M_SUSY 对数正')
        G('G2-2', all(v > 0 for v in (m12, m13, m23)), 'MSSM 交点在 M_SUSY 之上')
        G('G2-3', mssm_unify, 'MSSM 汇聚通过')
        G('G2-4', m_gut > ms, 'GUT 尺度高于 M_SUSY')
        G('G2-5', alpha_gut_mssm > 0 and alpha_gut_mssm < D('0.1'), 'alpha_GUT 合理区间')
        G('G3-1', all(mut_detected), '变异测试 2/2')
        G('G3-2', abs(mut_b_spread - sm_spread) > D('0.01'), 'β 变异单独可检出')
        G('G3-3', abs(mut_a_spread - sm_spread) > D('0.01'), 'α_s 变异单独可检出')
        G('G4-1', len(ENTRIES) == 15, '15 条条目')
        G('G4-2', counter().get('CORRECTED', 0) == 1, '一条 CORRECTED')
        G('G4-3', any(e[0] == 'I10' and e[1] == 'FAIL' for e in ENTRIES), '超伴子代价为 FAIL')


def build_md():
    c = counter()
    lines = []
    lines.append('# 数据 · ' + TAG)
    lines.append('')
    lines.append('- VERDICT `%s`' % VERDICT)
    lines.append('- 条目 %d：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, c.get(k, 0)) for k in ('PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED'))))
    lines.append('- 守卫 %d/%d' % (guard_ok(), len(GUARDS)))
    lines.append('')
    lines.append('## 关键读数')
    lines.append('')
    lines.append('```')
    lines.append('SIN2_TREE       = %s' % fm(R['tree'], 12))
    lines.append('SIN2_EXP        = %s' % fm(D(INPUT['sin2_theta_W']), 12))
    lines.append('TREE_REL_ERROR  = %s' % fm(R['tree_rel'], 8))
    lines.append('SM_L12          = %s' % fm(R['L12'], 8))
    lines.append('SM_L13          = %s' % fm(R['L13'], 8))
    lines.append('SM_L23          = %s' % fm(R['L23'], 8))
    lines.append('SM_DELTA_L      = %s' % fm(R['sm_spread'], 8))
    lines.append('ALPHA3_REQ      = %s' % fm(R['a3req'], 8))
    lines.append('MSSM_DELTA_L    = %s' % fm(R['mssm_spread'], 8))
    lines.append('M_GUT_GEV       = %s' % fm(R['m_gut'], 6))
    lines.append('MUTATION        = %s' % R['mut_detected'])
    lines.append('```')
    lines.append('')
    lines.append('## 条目')
    lines.append('')
    lines.append('| 编号 | 判定 | 标题 | 细节 |')
    lines.append('|---|---|---|---|')
    for code, st, title, detail in ENTRIES:
        lines.append('| %s | %s | %s | %s |' % (code, st, title, detail.replace('|', '\\|')))
    lines.append('')
    lines.append('## 守卫')
    lines.append('')
    for name, ok, detail in GUARDS:
        lines.append('- %s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    lines.append('')
    return '\n'.join(lines)


def build_report():
    c = counter()
    lines = []
    lines.append('[r445] %s' % VERDICT)
    for k in ('PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED'):
        lines.append('%s=%d' % (k, c.get(k, 0)))
    lines.append('SIN2_TREE = %s' % fm(R['tree'], 12))
    lines.append('SM_DELTA_L = %s' % fm(R['sm_spread'], 8))
    lines.append('MSSM_DELTA_L = %s' % fm(R['mssm_spread'], 8))
    lines.append('ALPHA3_REQ = %s' % fm(R['a3req'], 8))
    lines.append('M_GUT_GEV = %s' % fm(R['m_gut'], 6))
    lines.append('MUTATION_DETECTED = %s' % R['mut_detected'])
    lines.append('GUARDS %d/%d' % (guard_ok(), len(GUARDS)))
    return '\n'.join(lines) + '\n'


def main():
    ensure_dirs()
    analyse()
    payload = {
        'tag': TAG,
        'stamp': STAMP,
        'verdict': VERDICT,
        'inputs': INPUT,
        'betas': {'SM': B_SM, 'MSSM': B_MSSM},
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
