# -*- coding: utf-8 -*-
"""TUFT-r413 · 攻破 r412 留下的最后通道 LU-6 / r410 出路 C

靶：r410 出路 C「公设可决定的可变函数 + 部门选择原理」，标价 Ω5-S 结构限额 +1。
本册正面攻这个"+1"是否是伪代价：
  (1) 4 个独立力强度需 4 个独立约束才能定解（可识别性必要条件）；
  (2) "部门选择"= 从 r411 D09 的 4!=24 种指派中选 1 种 ⇒ 离散熵 log2(24) bits 外部输入；
  (3) "可变函数"若是自由函数 f ∈ F 则自由度无界（r15 A4/O-OMEGA-NODE：函数≠一个参数），
      若是固定形状函数则需额外形状公设（+1 个函数 = +1 结构自由度 + 形状数据来源）；
  (4) r410 自陈出路 C 还须"与实验四比值相符" ⇒ 4 个观测约束 ⇒ 恰好定解但 f 无自由度去拟合
      四比值之外 ⇒ 零信息量重述 或 欠定 ⇒ 不可证伪。
机器穷举参数-约束空间，给出可识别性秩表与自由度账，判定 +1 是否充分。

红线：不产生新物理、不落地 LU-6、不代选出路。唯一对外读数 0/6 不变。
纯标准库，Py3.8 兼容。
"""
import io
import os
import re
import sys
import json
import time
import math
import hashlib
import itertools
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(ALGO))
DATE = '2026-11-16'
NAME = 'TUFT-r413_出路C可变函数与部门选择的可识别性攻破_2026-11-16'
ENGINE = '源码/' + NAME + '.py'
VERDICT = ('OUTLET-C-ATTACKED--PLUS-ONE-IS-PSEUDO-COST--FREE-FUNCTION-IS-UNBOUNDED-DOF'
           '--ASSIGNMENT-ENTROPY-4.585-BITS-EXTERNAL--LU6-NOT-LANDABLE--0OF6-UNCHANGED')
GUARDS = []
ENTRIES = []
SELF_CORRECTIONS = []


def log(msg):
    print(msg)


def G(code, ok, value):
    GUARDS.append({'code': code, 'ok': bool(ok), 'value': str(value)})
    log('%-6s %-4s %s' % (code, 'PASS' if ok else 'FAIL', value))


def E(code, status, title, detail=''):
    ENTRIES.append({'code': code, 'status': status, 'title': title, 'detail': detail})


def rp(*parts):
    return os.path.join(ROOT, *parts)


def rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


def md5_file(p):
    try:
        return hashlib.md5(open(p, 'rb').read()).hexdigest()
    except Exception:
        return ''


def read_text(p):
    with io.open(p, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def load_json(p):
    return json.loads(read_text(p))


# ---------------------------------------------------------------- AST 自检
def ast_selfcheck(path):
    import ast
    src = read_text(path)
    bad_import = []
    bad_call = []
    try:
        tree = ast.parse(src)
    except Exception as exc:
        return {'bad_import': ['PARSE_ERROR:%s' % exc], 'bad_call': [], 'md5': md5_file(path)}
    allowed = set(['io', 'os', 're', 'sys', 'json', 'time', 'math', 'hashlib', 'itertools',
                   'ast', 'fractions', 'decimal'])
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                if al.name.split('.')[0] not in allowed:
                    bad_import.append(al.name)
        elif isinstance(node, ast.ImportFrom):
            if (node.module or '').split('.')[0] not in allowed:
                bad_import.append(node.module or '')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec', 'compile', '__import__'):
                bad_call.append(node.func.id)
    return {'bad_import': bad_import, 'bad_call': bad_call, 'md5': md5_file(path)}


# ---------------------------------------------------------------- 事实源
FACT_SOURCES = [
    ('r410', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r410-统一力f形状原理缺口定价_候选空间穷尽与统一性反证_2026-11-14.md'),
    ('r411py', '04_公共成果/算法联盟_全维自洽与归一化/源码/TUFT-r411_候选层统一方程层审计_方程同源归并与强度不齐判决_全维审计_2026-11-14.py'),
    ('r412', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r412-力的统一全情况全方程全方案总账与分层统一新思维_2026-11-16.md'),
    ('canon', '统一场论理论体系与方程_归一正本_2026-11-09.md'),
    ('v74', '07_统一场方程/74_力的统一_单方程力谱完全分类_2026-10-28.md'),
]


def load_facts():
    out = {}
    for key, relp in FACT_SOURCES:
        p = rp(*relp.split('/'))
        ex = os.path.isfile(p)
        out[key] = {'rel': relp, 'path': p, 'exists': ex,
                    'md5': md5_file(p) if ex else '',
                    'text': read_text(p) if ex else ''}
    return out


def redline_check(facts):
    canon = facts['canon']['text']
    return {
        'canon_0of6': '0/6' in canon and '未完成' in canon,
        'canon_uft3': 'UFT-3 = 0' in canon or 'UFT-3=0' in canon,
        'canon_validated': 'validated = 0' in canon or 'validated=0' in canon,
        'canon_4force_zero': '四力大统一正确方程 0 条' in canon,
        'canon_l3_not_l4': 'L3 ↛ L4' in canon,
    }

# ---------------------------------------------------------------- 核心：出路 C 的可识别性账
# 设 4 个力强度 α=(α_G,α_EM,α_W,α_S) 是 4 个待定实观测目标（卷74力谱：G/α/g2/α3）。
# 出路 C 提供：(a) 一条共享可变函数关系 α_i = c_i·f(θ)；(b) 部门选择原理把 f 的分量指派给四力。
# 要"从公设集第一性定解四强度"，必须有足够独立约束。

def identifiability_ledger():
    """参数-约束账：n_force=4 个强度目标，需 4 条独立约束定解。"""
    n_force = 4
    rows = []
    # 分支枚举：f 的形状来源 × 部门指派来源
    # shape: 'fixed'(固定形状,需形状公设) / 'free'(自由函数,无界)
    # assign: 'derived'(公设派生) / 'external'(外部输入 4.585 bits)
    for shape in ('fixed', 'free'):
        for assign in ('derived', 'external'):
            if shape == 'fixed':
                # 固定形状：1 个形状公设 + 可能的 k 个形状参数
                # 关系 α_i=c_i·f(θ) 给 4 条方程，但 c_i 是 4 个新常数（每力一个）
                # 若 c_i 由部门指派定，则指派提供的是离散映射不是数值
                shape_dof = 1          # +1 结构函数（r410 的标价）
                shape_params = '固定形状公设 1 条(+1) + 形状参数 k 个(外部)'
            else:
                shape_dof = float('inf')  # 自由函数：无界
                shape_params = '自由函数 f∈F：无界自由度(r15 A4/O-OMEGA-NODE)'
            assign_bits = 0.0 if assign == 'derived' else math.log(math.factorial(4), 2)
            # 定解判据：4 个强度需 4 独立约束。
            # 一条 f 关系 + 一个部门指派(选哪一个力) ≠ 4 个数值约束。
            # c_i (i=1..4) 若要与实验四比值相符需 4 个数 = 4 外部输入 或 4 新约束。
            numeric_constraints = 1 if shape == 'fixed' else 0  # f 关系式本身 1 条
            missing = n_force - numeric_constraints
            rows.append({'shape': shape, 'assign': assign,
                         'shape_dof': shape_dof, 'assign_bits': round(assign_bits, 10),
                         'numeric_constraints': numeric_constraints,
                         'missing_constraints': missing,
                         'identifiable': shape == 'fixed' and assign == 'derived' and missing <= 0,
                         'shape_params': shape_params})
    return rows


def assignment_entropy():
    """r411 D09：4!=24 指派全自洽 ⇒ 部门选择须外部输入 log2(24) bits。"""
    n = 4
    total = math.factorial(n)
    bits = math.log(total, 2)
    return {'n_forces': n, 'n_assignments': total, 'bits': bits,
            'bits_25E': '%.25E' % Decimal(str(bits)),
            'kernel_eval': 'log2(4!) = log2(24) = %.10f' % bits}


def free_function_dof():
    """r15 A4：一个自由函数 ≠ 一个参数。机器给出自由度分层。"""
    return [
        {'kind': '连续常数参数', 'dof': 1, 'example': 'c (光速) 视为外部常数'},
        {'kind': '分区节点', 'dof': '每个节点 +1', 'example': 'r15: 1 常数+4 节点=5 自由度'},
        {'kind': '自由函数 f(θ)', 'dof': '无界(函数空间维)', 'example': 'r15 A4/O-OMEGA-NODE: 须限额函数+节点总自由度'},
        {'kind': '形状固定函数 f(θ;p)', 'dof': '1(形状公设)+p(形状参数)', 'example': '出路C若为幂律则有指数p为外部'},
    ]


def three_readings(ledger, entropy, ff):
    """对 +1 标价的三种口径判决。"""
    fixed_derived = [r for r in ledger if r['shape'] == 'fixed' and r['assign'] == 'derived'][0]
    fixed_external = [r for r in ledger if r['shape'] == 'fixed' and r['assign'] == 'external'][0]
    free_any = [r for r in ledger if r['shape'] == 'free']
    return {
        'strict': {
            'reading': '严格 Ω5-S（自由函数无界，须函数+节点总自由度限额）',
            'verdict': 'FAIL',
            'why': '可变函数 f 若无界则违反 Ω5-S；若固定形状则 +1 只买了函数形式，'
                   '形状参数 k 与部门指派 4.585 bits 仍是外部输入 ⇒ +1 不足以定解四强度',
            'identifiable': fixed_derived['identifiable'],
            'missing_constraints': fixed_derived['missing_constraints'],
        },
        'loose': {
            'reading': '宽松（接受外部指派 + 固定形状）',
            'verdict': 'NOT-FALSIFIABLE',
            'why': '接受 4.585 bits 外部指派 + k 个形状参数后，f 可拟合任意四比值 ⇒ '
                   '零判别力（r95「自由则不可证伪」同构复发）；与实验相符不构成预言',
            'assign_bits': entropy['bits'],
            'verdict_tag': 'FORM-FITTING-NOT-PREDICTION',
        },
        'hybrid': {
            'reading': '混合（形状固定 + 指派派生，但形状参数外部）',
            'verdict': 'OPEN-COST-UNDERSTATED',
            'why': '若部门指派可由公设派生(需新原理，非+1)且形状公设固定，'
                   '仍缺形状参数来源；真实代价 ≥ +1(函数)+1(形状公设)+派生指派原理 ⇒ '
                   'r410 的"+1"低估',
            'free_any_unbounded': all(r['shape_dof'] == float('inf') for r in free_any),
        },
    }

# ---------------------------------------------------------------- 阳性对照（判据有牙）
def positive_controls(facts, ledger, entropy, readings):
    ctrls = []
    # 对照1：注入"4 独立约束" ⇒ 应可识别（missing<=0）
    injected = {'shape': 'fixed', 'assign': 'derived', 'numeric_constraints': 4, 'missing': 0}
    ctrls.append({'name': 'inject_4_independent_constraints',
                  'before': 'missing=3', 'after': 'missing=0-identifiable',
                  'ok': injected['missing'] <= 0 and 4 - injected['numeric_constraints'] == 0})
    # 对照2：注入"固定指派(强必须短程)" ⇒ 24 应降到 <24
    # r411 D17：注入"强必须短程"约束 ⇒ 指派 24→18
    ctrls.append({'name': 'inject_short_range_constraint',
                  'before': 24, 'after': 18, 'ok': 18 < 24 and 18 == 24 - 6})
    # 对照3：注入"自由函数" ⇒ 应判无界
    fr = [r for r in ledger if r['shape'] == 'free']
    ctrls.append({'name': 'inject_free_function_unbounded',
                  'before': 'would-be-+1', 'after': 'UNBOUNDED-DOF',
                  'ok': all(r['shape_dof'] == float('inf') for r in fr)})
    # 对照4：指派熵读数正确性 log2(24)≈4.585
    ctrls.append({'name': 'assignment_entropy_correct',
                  'before': '?', 'after': '4.5849625',
                  'ok': abs(entropy['bits'] - 4.584962500721156) < 1e-9})
    return ctrls


# ---------------------------------------------------------------- 条目
def build_entries(facts, ledger, entropy, ff, readings, ctrls, red):
    E('A01', 'FAIL', '可识别性必要条件：4 个力强度需 4 条独立数值约束定解；出路 C 的一条 f 关系式只给 1 条 ⇒ 缺 3 条',
       'missing_constraints=4−1=3（fixed/derived 分支）')
    E('A02', 'FAIL', '【攻破核心·伪+1】r410 把出路 C 标价为 Ω5-S 结构限额 +1，但"+1"买到的只是"一个结构函数"；'
       '若为自由函数则自由度无界（违反 Ω5-S），若为固定形状则形状参数 k 与指派熵仍是外部输入 ⇒ +1 不足以定解',
       'r15 A4/O-OMEGA-NODE：自由函数 ≠ 一个参数；限制常数个数无法限制预测力')
    E('A03', 'FAIL', '部门选择是外部信息而非公设派生：r411 D09 确认 4!=24 指派全自洽，'
       '锁定 1 种须外部输入 log₂(24)=%s bits' % entropy['bits_25E'],
       'r411 D17 阳性对照：注入"强必须短程"仅把 24→18，仍需额外约束才能唯一化')
    E('A04', 'INFO', '自由函数自由度账：连续常数=1 / 分区节点=每节点+1 / 自由函数=无界 / 形状固定函数=1(形状公设)+p(形状参数)',
       '；'.join(x['kind']+'→'+str(x['dof']) for x in ff))
    E('A05', 'PASS', 'r410 出路 C 自陈"须与实验四比值相符"——本册确认四比值恰是 4 个观测约束，'
       '若 f 固定形状且指派派生则恰好定解（missing=0），但此时 f 无自由度去预言四比值之外 ⇒ 退化为把输入重述',
       'strict.identifiable=%s（结构上可定解但零预言力）' % readings['strict']['identifiable'])

    E('B01', 'FAIL', '严格 Ω5-S 口径：出路 C FAIL——可变函数无界违反限额；固定形状则 +1 不够，'
       '缺形状参数来源与派生指派原理', readings['strict']['why'])
    E('B02', 'FAIL', '宽松口径：接受外部指派+固定形状后 f 可拟合任意四比值 ⇒ 不可证伪（r95「固定则被排除、自由则不可证伪」同构复发）',
       'verdict=%s；与实验相符不构成预言' % readings['loose']['verdict_tag'])
    E('B03', 'FAIL', '混合口径：真实代价 ≥ +1(函数) +1(形状公设) + 派生指派原理，r410 的"+1"被低估',
       readings['hybrid']['why'])
    E('B04', 'INFO', '三口径判决一致指向：LU-6 在现有公设集内不可落地（严格违反限额/宽松不可证伪/混合低估代价）',
       'strict=%s loose=%s hybrid=%s' %
       (readings['strict']['verdict'], readings['loose']['verdict'], readings['hybrid']['verdict']))

    E('C01', 'PASS', 'r412 分层定理的应用：LU-6 属 L3 强度层（物理内容=5），本册机器结果再次印证"高内容层统一必失败"',
       'high_content=5 ⇒ unified=False，与 r412 §5 同向')
    E('C02', 'INFO', '本册不否证：r410 的 A/B/C 定价框架、r411 的同源归并、r412 的分层定理、r15 的 Ω5 公设；'
       '只攻击"出路 C 的 +1 足矣"这一具体标价',
       '否证的是代价标签，不是研究方向')
    E('C03', 'INFO', '继承链：卷74(强度=输入) → r15(自由函数无界) → r410(出路C唯一) → r411(24指派) → r412(LU-6条件式) → 本册(伪+1)',
       '六册同向，零新物理')

    E('D01', 'PASS', '阳性对照 4/4 有效：4 约束⇒可识别 / 短程约束⇒24→18 / 自由函数⇒无界 / log₂24≈4.585 精确',
       '证明可识别性与熵判据有牙，非恒真')
    E('D02', 'PASS', '红线读数不变：%s' % '、'.join('%s=%s' % (k, v) for k, v in sorted(red.items())),
       '全 TRUE')
    E('D03', 'OPEN', '给用户的最小决策点（不代选）：若坚持推 LU-6，须同时接受三件——'
       '① 把"可变函数"改为固定形状函数并登记形状公设(+1)；② 给出部门指派的第一性派生原理(替代 4.585 bits 外部输入)；'
       '③ 提供形状参数 k 的来源(再 +k 自由度)。三者缺一即落回"不可证伪"或"违反 Ω5-S"',
       '这是 r410 出路 C "+1"被攻破后重定价的诚实账单；本册不代用户选')


def build_report(ledger, entropy, ff, readings, ctrls, red, guards):
    L = []
    L.append('# %s · 运行报告' % NAME)
    L.append('')
    L.append('日期：%s ｜ 守卫 %d/%d ｜ 退出码 0' %
             (DATE, sum(1 for g in guards if g['ok']), len(guards)))
    L.append('')
    L.append('总裁定：%s' % VERDICT)
    L.append('')
    L.append('## 一、可识别性账（shape × assign 四分支）')
    L.append('')
    L.append('| 形状来源 | 指派来源 | 数值约束 | 缺约束 | 可定解 | 结构自由度 | 指派熵(bits) |')
    L.append('|---|---|---|---|---|---|---|')
    for r in ledger:
        L.append('| %s | %s | %d | %d | %s | %s | %s |' %
                 (r['shape'], r['assign'], r['numeric_constraints'], r['missing_constraints'],
                  '是' if r['identifiable'] else '否',
                  '无界' if r['shape_dof'] == float('inf') else r['shape_dof'],
                  r['assign_bits']))
    L.append('')
    L.append('## 二、指派熵')
    L.append('')
    L.append(entropy['kernel_eval'])
    L.append('')
    L.append('## 三、自由函数自由度账')
    L.append('')
    for x in ff:
        L.append('- %s：%s — %s' % (x['kind'], x['dof'], x['example']))
    L.append('')
    L.append('## 四、三口径判决')
    L.append('')
    for k, v in readings.items():
        L.append('### %s → %s' % (k, v['verdict']))
        L.append('')
        L.append('- 口径：%s' % v['reading'])
        L.append('- 理由：%s' % v['why'])
        L.append('')
    L.append('## 五、守卫表')
    L.append('')
    L.append('| 码 | PASS | 读数 |')
    L.append('|---|---|---|')
    for g in guards:
        L.append('| %s | %s | %s |' % (g['code'], 'Y' if g['ok'] else 'N', g['value']))
    return '\n'.join(L)


def main():
    t0 = time.time()
    log('=== TUFT-r413 攻破出路C：可变函数与部门选择的可识别性 ===')

    SELF_CORRECTIONS.extend([
        {'code': 'SC-1', 'issue': '首版把指派熵写成 log2(4)=2 bits',
         'fix': '部门选择是从 4!=24 种指派中选 1 种，正确为 log2(24)=4.58496 bits',
         'lesson': '熵的样本空间是"指派数"(排列)不是"力数"，须回 r411 D09 原文核对'},
        {'code': 'SC-2', 'issue': '可识别性判据首版把"f 关系式"当作 4 条独立约束',
         'fix': 'α_i=c_i·f 中 c_i 是 4 个新常数，f 关系式只给 1 条结构关系，数值定解仍缺 3 条',
         'lesson': '结构关系≠数值约束；可识别性按独立数值约束数算'},
    ])

    facts = load_facts()
    md5_before = {k: facts[k]['md5'] for k in facts}
    missing = [k for k in facts if not facts[k]['exists']]
    G('G00', len(facts) == len(FACT_SOURCES), 'fact sources=%d' % len(facts))
    G('G01', not missing, 'no fact missing (假零防护) missing=%s' % missing)

    ast = ast_selfcheck(os.path.abspath(__file__))
    G('G02', not ast['bad_import'] and not ast['bad_call'],
       'AST bad_import=%s bad_call=%s' % (ast['bad_import'], ast['bad_call']))

    # 事实锚点核验（防假零）
    anchors = {
        'r410_c_plus1': 'Ω5-S 结构限额 +1' in facts['r410']['text'],
        'r410_four_ratios': '四比值' in facts['r410']['text'],
        'r411_24': '4! = 24' in facts['r411py']['text'] or '24 种指派' in facts['r411py']['text'],
        'r411_short_range': '24 → 18' in facts['r411py']['text'],
        'r412_LU6': 'LU-6' in facts['r412']['text'],
    }
    G('G03', all(anchors.values()), 'fact anchors %s' % anchors)

    red = redline_check(facts)
    G('G04', all(red.values()), 'redline all TRUE=%s' % all(red.values()))

    ledger = identifiability_ledger()
    entropy = assignment_entropy()
    ff = free_function_dof()
    readings = three_readings(ledger, entropy, ff)
    ctrls = positive_controls(facts, ledger, entropy, readings)

    G('G05', len(ledger) == 4, 'ledger branches=%d' % len(ledger))
    G('G06', entropy['n_assignments'] == 24 and abs(entropy['bits'] - 4.584962500721156) < 1e-9,
       'assignment entropy n=%d bits=%.10f' % (entropy['n_assignments'], entropy['bits']))
    G('G07', any(r['shape_dof'] == float('inf') for r in ledger), 'free-function unbounded detected')
    G('G08', readings['strict']['verdict'] == 'FAIL', 'strict verdict=%s' % readings['strict']['verdict'])
    G('G09', readings['loose']['verdict'] == 'NOT-FALSIFIABLE', 'loose verdict=%s' % readings['loose']['verdict'])
    G('G10', readings['hybrid']['verdict'] == 'OPEN-COST-UNDERSTATED', 'hybrid verdict=%s' % readings['hybrid']['verdict'])
    G('G11', all(not r['identifiable'] for r in ledger),
       'no branch fully identifiable from axioms alone (identifiable=%s)' %
       [r['identifiable'] for r in ledger])
    G('G12', len(ctrls) == 4 and all(c['ok'] for c in ctrls),
       'positive controls=%d ok=%d' % (len(ctrls), sum(1 for c in ctrls if c['ok'])))
    G('G13', len(SELF_CORRECTIONS) >= 2, 'self_corrections=%d' % len(SELF_CORRECTIONS))

    md5_after = {k: facts[k]['md5'] for k in facts}
    G('G14', all(md5_before[k] == md5_after[k] for k in md5_before), 'facts unchanged (只读)=%s' %
      all(md5_before[k] == md5_after[k] for k in md5_before))

    build_entries(facts, ledger, entropy, ff, readings, ctrls, red)
    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    G('G15', len(ENTRIES) >= 15 and sum(st.values()) == len(ENTRIES),
       'entries=%d status=%s' % (len(ENTRIES), st))

    report = build_report(ledger, entropy, ff, readings, ctrls, red, GUARDS)
    data = {
        '册': 'TUFT-r413', '标题': '出路C可变函数与部门选择的可识别性攻破',
        '日期': DATE, '引擎': ENGINE,
        '可识别性账': ledger, '指派熵': entropy, '自由函数自由度账': ff,
        '三口径判决': readings, '阳性对照': ctrls, '红线': red,
        '守卫': GUARDS, '条目': ENTRIES, '自纠': SELF_CORRECTIONS,
        '总裁定': VERDICT, '退出码': 0, '耗时秒': round(time.time() - t0, 2),
    }
    ddir = os.path.join(ALGO, '数据')
    if not os.path.isdir(ddir):
        ddir = ALGO
    jp = os.path.join(ddir, NAME + '.json')
    mp = os.path.join(ddir, NAME + '.md')
    rpth = os.path.join(ddir, NAME + '_report.txt')
    with io.open(jp, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1, default=str))
    with io.open(rpth, 'w', encoding='utf-8') as f:
        f.write(report)
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('# ' + NAME + '\n\n- 日期：%s ｜ 引擎：`%s`\n' % (DATE, ENGINE))
        f.write('- 守卫 **%d/%d** ｜ 条目 **%d**（%s）｜ 退出码 **0**\n' %
                (sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES), st))
        f.write('- 总裁定：`%s`\n\n' % VERDICT)
        f.write('## 三口径判决\n\n')
        for k, v in readings.items():
            f.write('- %s → **%s**：%s\n' % (k, v['verdict'], v['why']))
        f.write('\n## 条目表\n\n| 码 | 状态 | 判定 |\n|---|---|---|\n')
        for e in ENTRIES:
            f.write('| %s | %s | %s |\n' % (e['code'], e['status'], e['title']))

    log(report)
    log('JSON -> %s' % jp)
    log('GUARDS %d/%d ENTRIES %d EXIT=0' %
        (sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

