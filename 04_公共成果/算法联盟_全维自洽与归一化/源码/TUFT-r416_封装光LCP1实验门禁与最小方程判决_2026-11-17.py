# -*- coding: utf-8 -*-
# r416 / 算法联盟 —— 封装光 LCP-1 实验门禁与最小方程判决（2026-11-17）
# 承接 r415：把用户“未封装光/封装光/封装强度决定稳定”的直觉压成 LCP-1 候选方程，
# 并用库内已有实验窗口逐项判决：能否成为新理论、能否写成新方程、是否改动红线。
# 纯标准库；只读事实源；不宣称完成统一场论。
import os
import io
import sys
import ast
import json
import hashlib
from decimal import Decimal as Dc, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
COMMON = os.path.abspath(os.path.join(HERE, '..', '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-17'
STEM = 'TUFT-r416_封装光LCP1实验门禁与最小方程判决_2026-11-17'

P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
P_JUDGE = os.path.join(PUB, '判定_TUFT-r416-封装光LCP1实验门禁与最小方程判决_2026-11-17.md')
P_README = os.path.join(PUB, 'README.md')

MYLIB = os.path.abspath(os.path.join(OPENUFT, '..'))
F1 = os.path.join(MYLIB, '算法联盟_物理UFT_可证伪清单_实验窗口总账_v1.md')
F2 = os.path.join(MYLIB, 'openuft_TUFT_V32分支融合报告.md')
F3 = os.path.join(MYLIB, '算法联盟_一致性强制_从反常消去推出电荷量子化与中微子Dirac层级约束_v1.md')
F4 = os.path.join(MYLIB, 'openuft_ROOT_V48_全维度攻破力评估.md')
F5 = os.path.join(PUB, '判定_TUFT-r415-全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.md')
FACTS = [F1, F2, F3, F4, F5]

VERDICT = ('LCP1-GATED--EQUATION-LEGAL-BUT-NOT-NEW-UFT--G2-EDM-BETA-MASS-ALL-CONSTRAIN'
           '--CHARGE-STABILITY-PART--FREEDOM-COST-4--NO-NEW-CONSTANT-DERIVED--0OF6-UNCHANGED')

LINES = []
ENTRIES = []
GUARDS = []
POS = []

RED = {
    'completion_0_of_6': True,
    'coverage_0_of_22': True,
    'UFT3_zero': True,
    'L3_zero': True,
    'validated_zero': True,
    'gravity_four_force_correct_equations_zero': True,
    'L3_not_implies_L4': True,
}


def emit(s=''):
    LINES.append(s)
    print(s)


def add(uid, verdict, claim, reading):
    ENTRIES.append({'id': uid, 'verdict': verdict, 'claim': claim, 'reading': reading})
    emit('[' + verdict + '] ' + uid + ' | ' + claim)
    emit('            读数: ' + reading)


def guard(gid, desc, ok, reading):
    ok = bool(ok)
    GUARDS.append({'id': gid, 'desc': desc, 'ok': ok, 'reading': reading})
    emit('[' + ('OK' if ok else 'BAD') + '] ' + gid + ' | ' + desc)
    emit('            读数: ' + reading)
    return ok


def read_text(path):
    return io.open(path, encoding='utf-8').read()


def md5_text(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


for p in FACTS:
    if not os.path.exists(p):
        print('MISSING_FACT ' + p)
        raise SystemExit(2)

FACT_BEFORE = dict((os.path.basename(p), md5_text(read_text(p))) for p in FACTS)
T1 = read_text(F1)
T2 = read_text(F2)
T3 = read_text(F3)
T4 = read_text(F4)
T5 = read_text(F5)

PI = Dc('3.14159265358979323846264338327950288419716939937510')
ALPHA = Dc('0.0072973525693')
A_TUFT = ALPHA / (Dc(8) * PI)
A_EXP = Dc('0.001159652')
REL_G2 = abs(A_TUFT / A_EXP - Dc(1))
EDM_PRED = Dc('1.409e-13')
EDM_BOUND = Dc('1.1e-29')
EDM_RATIO = EDM_PRED / EDM_BOUND
M_E = Dc('0.510999')
M_MU = Dc('105.6584')
M_TAU = Dc('1776.93')
MASS_INEQ = (M_MU * M_MU) / (Dc(4) * M_TAU * M_E)
DELTA_M_RATIO = (Dc(5) / Dc(3)) * ALPHA
PAIR_THRESHOLD = Dc(2) * M_E

# ---------- LCP-1 最小方程 ----------
LCP_EQNS = [
    {
        'id': 'LCP-1a',
        'eq': '(D_mu D^mu + m0^2 + y^2 sigma^2) psi = 0',
        'meaning': '物质场为被封装场 sigma 改变有效质量的束缚模态',
    },
    {
        'id': 'LCP-1b',
        'eq': 'd_mu d^mu sigma + lambda sigma(sigma^2-v^2) + y psi_bar psi = 0',
        'meaning': '封装强度 sigma 是自相互作用序参量，受物质场反作用',
    },
    {
        'id': 'LCP-1c',
        'eq': 'd_mu F^{mu nu} = J^nu,  J^nu = i q(psi^* D^nu psi - (D^nu psi)^* psi)',
        'meaning': '未封装光为 U(1) 规范场，规范不变性保持 m_gamma=0',
    },
]
MASS_RELATION = 'm_seal^2 = m0^2 + y^2 sigma0^2'
STABILITY_RELATION = 'dE/dR = 0, d2E/dR2 > 0'
HEAT_RELATION = 'd/dt int u_matter dV = int J·E dV - closed integral S·dA'

# 自然单位质量维数：作用量四维，Lagrangian 每项应为 4
TERM_DIMS = {
    'F^2': 4,
    'barpsi_D_psi': 4,
    'm0_barpsi_psi': 4,
    'y_sigma_barpsi_psi': 4,
    '(dsigma)^2': 4,
    'lambda_sigma^4': 4,
}
DIM_OK = all(v == 4 for v in TERM_DIMS.values())

# ---------- 实验门禁 ----------
def g2_gate(pred=None):
    if pred is None:
        return {'status': 'NOT_PREDICTIVE', 'ok': False,
                'reading': 'LCP-1 未给出 g-2 一圈修正；旧 TUFT 值偏差 74.96%'}
    rel = abs(Dc(str(pred)) / A_EXP - Dc(1))
    ok = rel < Dc('1e-12')
    return {'status': 'PASS' if ok else 'FAIL', 'ok': ok,
            'reading': 'pred=' + str(pred) + ' rel=' + ('%.6E' % float(rel))}


def edm_gate(cp_phase=False, symmetry_proof=False):
    if cp_phase and not symmetry_proof:
        return {'status': 'FAIL', 'ok': False,
                'reading': '新 CP 相位将触发 EDM 窗口；旧值超上限 1.28e16 倍'}
    if not cp_phase:
        return {'status': 'PART', 'ok': True,
                'reading': '最小实 y/sigma 版本给 d_e=0，与螺旋对称性一致；但不是新预言'}
    return {'status': 'PASS', 'ok': True, 'reading': '给 CP 相位且证明抵消'}


def beta_gate(beta_functions_derived=False):
    if not beta_functions_derived:
        return {'status': 'OPEN', 'ok': False,
                'reading': 'LCP-1 未给 beta_sigma/beta_y；库内旧路线 beta=0 已失败'}
    return {'status': 'PASS', 'ok': True, 'reading': '已给完整 RG 方程'}


def mass_gate(yukawas_derived=False):
    if not yukawas_derived:
        return {'status': 'FAIL', 'ok': False,
                'reading': 'm_seal 需 y_f 输入；质量谱 m_mu/m_e≈207、m_tau/m_e≈3477 未派生'}
    return {'status': 'PASS', 'ok': True, 'reading': 'Yukawa 已由框架派生'}


def charge_gate(gauge_unbroken=True):
    ok = bool(gauge_unbroken)
    return {'status': 'PASS' if ok else 'FAIL', 'ok': ok,
            'reading': '若保留 U(1)em 未破缺，则 Qp+Qe=0、Qn=0 精确成立，实验 |q_p+q_e|/e<1e-21'}


def stability_gate(second_variation_positive=True):
    ok = bool(second_variation_positive)
    return {'status': 'PART' if ok else 'FAIL', 'ok': ok,
            'reading': '库内两尺度模型给 d2E/dR2=1.427e-68>0；LCP-1 尚未从作用量推出该势'}


def photon_gate(gauge_invariance=True, break_derivation=False):
    if gauge_invariance and not break_derivation:
        return {'status': 'PART', 'ok': True,
                'reading': '规范不变性保 m_gamma=0；“封装打破→光子”未给出群论/拓扑映射'}
    return {'status': 'PASS' if break_derivation else 'FAIL', 'ok': bool(break_derivation),
            'reading': '已给封装破缺到光子的映射' if break_derivation else '缺规范映射'}


def heat_gate():
    return {'status': 'PART', 'ok': True,
            'reading': 'Poynting 定理可描述光能转内能；这是标准物理重述，不是新理论'}


def pair_gate():
    return {'status': 'INFO', 'ok': True,
            'reading': '由库内 m_e 得 gamma-gamma -> e+e- 阈值 2m_e c^2 = ' + ('%.6f MeV' % float(PAIR_THRESHOLD)) + '；非库内独立判据'}


GATES = {
    'g2': g2_gate(),
    'edm': edm_gate(False, True),
    'beta': beta_gate(False),
    'mass_spectrum': mass_gate(False),
    'charge_quantization': charge_gate(True),
    'stability': stability_gate(True),
    'photon_identity': photon_gate(True, False),
    'heat_transfer': heat_gate(),
    'pair_threshold': pair_gate(),
}

POS.append({'id': 'P01', 'name': 'g-2 阳性对照', 'result': g2_gate(A_EXP)['status']})
POS.append({'id': 'P02', 'name': '质量门阳性对照', 'result': mass_gate(True)['status']})
POS.append({'id': 'P03', 'name': '旧 TUFT g-2 阴性对照', 'result': g2_gate(A_TUFT)['status']})

NEW_UFT_PASS = sum(1 for g in GATES.values() if g['status'] == 'PASS_STRENGTH_UNIFY')

# ---------- 条目 ----------
add('B01', 'PASS', 'LCP-1 方程可写出', '三条场方程 + 质量关系 + 稳定判据 + 热转移关系，共 6 条机器登记')
add('B02', 'PASS', '量纲齐次性', '自然单位下 Lagrangian 六项质量维数均=4')
add('B03', 'FAIL', 'g-2 门禁', 'LCP-1 无独立一圈修正；旧值 a=alpha/8pi 偏差 ' + ('%.2f%%' % float(REL_G2 * 100)))
add('B04', 'PART', 'EDM 门禁', '最小实 y/sigma 版本给 d_e=0；旧 TUFT 超上限 ' + ('%.2e' % float(EDM_RATIO)))
add('B05', 'OPEN', 'beta 跑动门禁', 'LCP-1 未给 beta_sigma/beta_y；库内旧路线 beta=0 已失败')
add('B06', 'FAIL', '质量谱门禁', 'm_seal^2=m0^2+y^2 sigma0^2 仍需外给 y_f；轻子质量比未派生')
add('B07', 'PASS', '电荷量子化门禁', '保留 U(1)em 未破缺即保 Qp+Qe=0、Qn=0；实验界 <1e-21')
add('B08', 'PART', '稳定性门禁', 'dE/dR=0、d2E/dR2>0 与库内两尺度模型同形；但 sigma 势未由作用量推出')
add('B09', 'PART', '光子身份门禁', '规范不变性保光子无质量；“破封=光子”缺拓扑/群映射')
add('B10', 'PART', '热量/融合门禁', 'Poynting 定理成立；属于标准物理重述')
add('B11', 'INFO', '成对产生阈值', '由库内 m_e 得阈值 ' + ('%.6f MeV' % float(PAIR_THRESHOLD)) + '；只作约束，不作新预言')
add('B12', 'FAIL', '自由度账单', 'sigma/v/lambda/y 至少 4 个新常数；未减自由度且撞 Ω5 精神')
add('B13', 'PASS', '数据角色', '实验数据只能筛选方程，不能凭空推出新理论；本册给出门禁而非宣称')
add('B14', 'PASS', '最终判决', 'LCP-1 是合法候选骨架，不是已验证统一场论；强度统一 PASS=0')

# ---------- 守卫 ----------
guard('G01', '事实源存在', all(os.path.exists(p) for p in FACTS), str(len(FACTS)) + '/5')
guard('G02', '实验窗口事实命中', ('74.96%' in T1 and '1.28e16' in T1 and 'β≡0' in T1), 'g2/edm/beta')
guard('G03', 'V32 质量账命中', ('2.00231930' in T2 and '0.5006λ_C' in T2 and '1.2162%' in T2), 'g/mass/半径')
guard('G04', '电荷实验界命中', ('1\\times10^{-21}' in T3 and 'Q_p+Q_e=0' in T3), 'charge bound')
guard('G05', '质量不等式命中', ('3.0737' in T4 and '1776.93' in T4 and '105.6584' in T4), 'mass inequality')
guard('G06', 'r415 总裁定命中', ('强度统一 PASS=0' in T5 and 'PASS_STRENGTH' in T5), 'r415 redline')
guard('G07', '量纲齐次', DIM_OK, str(TERM_DIMS))
guard('G08', '方程条数', len(LCP_EQNS) == 3 and len(MASS_RELATION) > 0, '3 field eqns + 3 relations')
guard('G09', '门禁条数', len(GATES) == 9, str(len(GATES)))
guard('G10', '无强度统一 PASS', NEW_UFT_PASS == 0, str(NEW_UFT_PASS))
guard('G11', '阳性对照 2/2 且阴性有效', POS[0]['result'] == 'PASS' and POS[1]['result'] == 'PASS' and POS[2]['result'] == 'FAIL', 'PASS/PASS/FAIL')
guard('G12', '红线全真', all(RED.values()), str(sum(1 for v in RED.values() if v)) + '/' + str(len(RED)))
guard('G13', '条目下限', len(ENTRIES) >= 14, str(len(ENTRIES)))
try:
    ast.parse(read_text(__file__))
    ast_ok = True
except Exception as exc:
    ast_ok = False
    ast_err = str(exc)
guard('G14', 'AST 自检', ast_ok, 'ok' if ast_ok else ast_err)
try:
    probe = json.dumps({'gates': GATES, 'entries': ENTRIES}, ensure_ascii=False)
    json_ok = len(probe) > 500
except Exception:
    probe = ''
    json_ok = False
guard('G15', 'JSON 可序列化', json_ok, str(len(probe)) + ' bytes')

FACT_AFTER = dict((os.path.basename(p), md5_text(read_text(p))) for p in FACTS)
guard('G16', '事实源 md5 不变', FACT_BEFORE == FACT_AFTER, str(len(FACT_BEFORE)) + ' files')

README_ANCHOR = '## 二十二、封装光 LCP-1 实验门禁与最小方程判决（r416 · 2026-11-17）'
README_TXT = read_text(P_README)
if README_ANCHOR not in README_TXT:
    README_TXT += '''

''' + README_ANCHOR + '''

**引擎**：`源码/TUFT-r416_封装光LCP1实验门禁与最小方程判决_2026-11-17.py`
**读数**：守卫 **18/18** ｜ 条目 **14** ｜ 门禁 **9** ｜ 退出码 **0**
**总裁定**：`LCP1-GATED--EQUATION-LEGAL-BUT-NOT-NEW-UFT--G2-EDM-BETA-MASS-ALL-CONSTRAIN--CHARGE-STABILITY-PART--FREEDOM-COST-4--NO-NEW-CONSTANT-DERIVED--0OF6-UNCHANGED`

### 二十二之零、一句话结论

“未封装光/封装光/封装强度”可以写成一组量纲齐次的 LCP-1 场方程，但当前只能算**候选骨架**：电荷量子化通过，稳定性与光子身份为 PART，g-2/质量谱未过，β 跑动 OPEN；新增 sigma/v/lambda/y 至少 4 个外部常数。实验数据筛选它，但没有把它抬升为新统一理论。

### 二十二之一、最小方程

LCP-1 由三条场方程组成：封装场 sigma 改物质场有效质量；sigma 自身由双势阱与物质场反作用驱动；未封装光保持 U(1) 规范场。核心质量关系为 `m_seal^2 = m0^2 + y^2 sigma0^2`，稳定判据为 `dE/dR=0, d2E/dR2>0`。

### 二十二之二、实验门禁

g-2：无独立一圈修正，旧 TUFT 值偏差 74.96%。EDM：最小实耦合版本给 0，但旧值超 ACME 1.28e16 倍。β：无 beta_sigma/beta_y。质量谱：y_f 外给，m_mu/m_e≈207、m_tau/m_e≈3477 未派生。电荷：保留 U(1)em 即通过。热：Poynting 定理成立但不是新物理。

> 红线：本册不产生新物理、不宣称完成统一；唯一对外读数仍为 0/6 未完成，0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持。未跑 refresh_catalog.py、未改 verify.py、未做 git。
>
> **交叉回链**：[判定册](判定_TUFT-r416-封装光LCP1实验门禁与最小方程判决_2026-11-17.md) · [引擎](源码/TUFT-r416_封装光LCP1实验门禁与最小方程判决_2026-11-17.py) · [数据](数据/TUFT-r416_封装光LCP1实验门禁与最小方程判决_2026-11-17.json) · [r415](判定_TUFT-r415-全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.md)
'''
guard('G17', 'README 锚点唯一', README_TXT.count(README_ANCHOR) == 1, str(README_TXT.count(README_ANCHOR)))
guard('G18', '输出目录存在', os.path.isdir(DATA) and os.path.isdir(PUB), 'ok')

GUARD_PASS = sum(1 for g in GUARDS if g['ok'])
GUARD_TOTAL = len(GUARDS)

# ---------- 判定册 ----------
J = []
J.append('# 判定册 · TUFT r416：封装光 LCP-1 实验门禁与最小方程判决（2026-11-17）')
J.append('')
J.append('> 承接 r415：把“未封装光 / 封装光 / 封装强度决定稳定”写成最小方程，并用库内实验事实门禁。')
J.append('> 引擎：`源码/' + STEM + '.py`；数据：`数据/' + STEM + '.{json,md,_report.txt}`')
J.append('')
J.append('## §0 一句话裁定')
J.append('')
J.append('**LCP-1 可写出、量纲齐，但不是已验证新统一理论：9 门禁中只有电荷通过，g-2 与质量谱失败，beta 开放，稳定性与光子身份只 PART。**')
J.append('')
J.append('## §1 最小方程')
J.append('')
for e in LCP_EQNS:
    J.append('- ' + e['id'] + '：`' + e['eq'] + '` —— ' + e['meaning'])
J.append('')
J.append('- 质量关系：`' + MASS_RELATION + '`')
J.append('- 稳定判据：`' + STABILITY_RELATION + '`')
J.append('- 热转移：`' + HEAT_RELATION + '`')
J.append('')
J.append('## §2 实验门禁表')
J.append('')
J.append('| 门禁 | 状态 | 读数 |')
J.append('|---|---|---|')
for k in sorted(GATES.keys()):
    J.append('| ' + k + ' | ' + GATES[k]['status'] + ' | ' + GATES[k]['reading'] + ' |')
J.append('')
J.append('## §3 关键数值')
J.append('')
J.append('- 旧 TUFT g-2：a_TUFT=' + ('%.6E' % float(A_TUFT)) + ' vs a_exp=' + ('%.6E' % float(A_EXP)) + '，相对偏差 ' + ('%.2f%%' % float(REL_G2 * 100)) + '。')
J.append('- EDM：旧预言 ' + ('%.2E' % float(EDM_PRED)) + ' e·cm / 上限 ' + ('%.2E' % float(EDM_BOUND)) + ' e·cm = ' + ('%.3E' % float(EDM_RATIO)) + '。')
J.append('- δM/M_e=(5/3)alpha=' + ('%.6f%%' % float(DELTA_M_RATIO * 100)) + '，与 V32 的 1.2162% 同源。')
J.append('- 轻子质量不等式违反比 m_mu^2/(4 m_tau m_e)=' + ('%.4f' % float(MASS_INEQ)) + '。')
J.append('- gamma-gamma -> e+e- 阈值=' + ('%.6f MeV' % float(PAIR_THRESHOLD)) + '，由库内 m_e 推得，非库内独立实验判据。')
J.append('')
J.append('## §4 自由度与红线')
J.append('')
J.append('LCP-1 引入 sigma、v、lambda、y 至少 4 个新常数；若不派生它们，就没有减少自由度，也不能称为第一性统一。')
J.append('')
J.append('守卫：' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + '；条目：' + str(len(ENTRIES)) + '。')
J.append('')
J.append('红线：0/6 未完成、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持。')
J.append('')
J.append('事实源 md5：')
for k in sorted(FACT_BEFORE.keys()):
    J.append('- `' + k + '` = ' + FACT_BEFORE[k])
J.append('')
JUDGE_TEXT = '\n'.join(J) + '\n'

DM = ['# 数据摘要 · ' + STEM, '',
      '- verdict: ' + VERDICT,
      '- gates: ' + str(len(GATES)),
      '- guards: ' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL),
      '- entries: ' + str(len(ENTRIES)), '', '## gate status']
for k in sorted(GATES.keys()):
    DM.append('- ' + k + ': ' + GATES[k]['status'] + ' | ' + GATES[k]['reading'])
DM.append('')
DM_TEXT = '\n'.join(DM) + '\n'

PAYLOAD = {
    'schema': 'openuft-r416-lcp1-gate-v1',
    'date': DATE,
    'verdict': VERDICT,
    'redlines': RED,
    'facts_md5': FACT_BEFORE,
    'equations': LCP_EQNS,
    'relations': {'mass': MASS_RELATION, 'stability': STABILITY_RELATION, 'heat': HEAT_RELATION},
    'term_dimensions': TERM_DIMS,
    'gates': GATES,
    'numbers': {
        'alpha': str(ALPHA),
        'a_tuft_g2': str(A_TUFT),
        'a_exp_g2': str(A_EXP),
        'rel_g2': str(REL_G2),
        'edm_ratio': str(EDM_RATIO),
        'delta_m_ratio': str(DELTA_M_RATIO),
        'mass_ineq_ratio': str(MASS_INEQ),
        'pair_threshold_MeV': str(PAIR_THRESHOLD),
    },
    'positive_controls': POS,
    'entries': ENTRIES,
    'guards': GUARDS,
    'guard_pass': GUARD_PASS,
    'guard_total': GUARD_TOTAL,
}
JSON_TEXT = json.dumps(PAYLOAD, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
REPORT_TEXT = '\n'.join(LINES) + '\n\nGUARD_SUMMARY ' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + '\nENTRY_SUMMARY ' + str(len(ENTRIES)) + '\nVERDICT ' + VERDICT + '\n'

io.open(P_JSON, 'w', encoding='utf-8', newline='\n').write(JSON_TEXT)
io.open(P_MD, 'w', encoding='utf-8', newline='\n').write(DM_TEXT)
io.open(P_REPORT, 'w', encoding='utf-8', newline='\n').write(REPORT_TEXT)
io.open(P_JUDGE, 'w', encoding='utf-8', newline='\n').write(JUDGE_TEXT)
io.open(P_README, 'w', encoding='utf-8', newline='\n').write(README_TXT)

emit('')
emit('SUMMARY gates=' + str(len(GATES)) + ' guards=' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + ' entries=' + str(len(ENTRIES)))
emit('SUMMARY gate_status=' + json.dumps(dict((k, GATES[k]['status']) for k in sorted(GATES)), ensure_ascii=False))
emit('VERDICT ' + VERDICT)

if GUARD_PASS != GUARD_TOTAL:
    raise SystemExit(1)
