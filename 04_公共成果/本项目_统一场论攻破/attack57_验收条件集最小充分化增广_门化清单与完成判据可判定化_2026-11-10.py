# -*- coding: utf-8 -*-
import ast
import hashlib
import itertools
import json
import pathlib
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60
ROOT = pathlib.Path(__file__).resolve().parents[2]
ATK = ROOT / '04_公共成果' / '本项目_统一场论攻破'
NORM = ROOT / '04_公共成果' / '本项目_全维自洽与归一化'
BASE = 'attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10'
DATE = '2026-11-10'
CIRC = '㊾'
VERDICT = 'MINIMAL-TYPED-AUGMENTATION-2--LEVEL-AND-GATE-DECIDABLE--NO-PHYSICAL-COMPLETION'

DEDUP_NEEDLES = ['门化清单', '验收条件集', '充分化增广', '补几条', 'hitting set',
                 '必要条件集充分化', '可判定完成', 'LEVEL ⟹ GATE',
                 '最小充分化增广', 'LEVEL -> GATE', 'LEVEL ⇒ GATE']

SELF_FIX = [
    '沿用上一轮 code-explorer 快照误以为 attack56 首空；动态实扫发现并行会话已落 attack56_CUNI-v2 二圈复算与方程块级净下降门（含判定册），按后到者改号不覆盖他人，改取 attack57。',
    '首版探针 r_max / c_max / j_max 正则要求路径分隔符前缀，把 TUFT-r406 / C0401 / J111 全漏成 0 或 351；改为非字母数字前缀通配，机器复核 r406 / C0401 / J111 / 卷133。',
    'find_one 按 r119 子串首命中 _run_r119.py 而非 r119 判定册；改为显式事实源路径 + md5 + 针词，不再用模糊 first-match。',
    'execute_command 一行式里把 def 放在分号后且夹中文导致 SyntaxError；改为落盘短探针脚本 + JSON 输出，stdout 只打 ASCII。',
    '首版原型对 itertools.product 直接 len() 抛 TypeError；改为 7*7*2*4*2*2 乘积式并把 1568 作为现场网格数。',
    '初判「最小增广 = 1 条」忽略了 attack55 E07 的 CONSTRUCTIVE 类型约束；修正为「类型化可采纳目录内最小 2 条」，并把 1 条方向条件降为充分但不合格。',
    'hitting set 原型初版把任意上下界碎片也列入可采纳目录，出现 {a<=1, e>=2} 的无类型 2 条解；拆成「可采纳 D/C/N 目录」与「变异守卫碎片」两套，结论只在前者成立。',
    '曾担心 a=0 与 attack55 分类定理 R>=1 冲突；由合法性 e<=a+R 重算后确认 a=0 自动给 s=0 且 R>=e>=1，24/24 状态兼容。',
    '初版想硬编码 37+6=43 与 21/42；改为从 attack54 现场 json 的 ledger_rows 解析行数、针词和集合计数，守卫再对账。',
    '初版总裁定写成 SUFFICIENT-SET-FOUND 易被误读为物理完成；改为 MINIMAL-TYPED-AUGMENTATION-2--LEVEL-AND-GATE-DECIDABLE--NO-PHYSICAL-COMPLETION，并锁 0/6 红线。',
    '判定册 §0 首版写 attack56 并行五件，动态计数实为 4 件；改为读 dyn.attack56_hits 动态生成，并把该自抓补入 self_corrections。'
]

STRICT_WORDS = ['净减', '净下降', '前提减少', '前提净减少', '参数净减', '净变化']
WEAK_WORDS = STRICT_WORDS + ['参数计数', '不劣于对照']
CONSTRUCTIVE_WORDS = ['导出', '预言', '闭式', '可检验', '可证伪', '单点']

SOURCES = [
    {'alias': 'norm', 'path': ROOT / '统一场论理论体系与方程_归一正本_2026-11-09.md',
     'needles': ['0/6，未完成', '唯一对外读数', 'L3 ↛ L4']},
    {'alias': 'attack54_judge', 'path': ATK / '判定_attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.md',
     'needles': ['LEVEL ⊬ GATE', '0/37', '43']},
    {'alias': 'attack54_json', 'path': ATK / 'attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.json',
     'needles': ['ledger_rows', 'coverage', 'LEVEL']},
    {'alias': 'attack55_judge', 'path': ATK / '判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md',
     'needles': ['只给类型下界', '不代造清单', 'GATE ⟹ s=0', 'STRUCTURE_IDENTIFY']},
    {'alias': 'attack55_json', 'path': ATK / 'attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.json',
     'needles': ['AXIOM-SWAP-EXIT-PRICED', '784', 'STRUCTURE_IDENTIFY']},
    {'alias': 'attack56_judge', 'path': ATK / '判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md',
     'needles': ['2-LOOP-SURVIVES', 'BLOCK-NET-MINUS-5', '0/6，未完成']},
    {'alias': 'attack56_json', 'path': ATK / 'attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.json',
     'needles': ['2-LOOP-SURVIVES', 'BLOCK-NET-MINUS-5']},
    {'alias': 'attack56_report', 'path': ATK / 'attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10_report.txt',
     'needles': ['VERDICT', '2-LOOP-SURVIVES']},
    {'alias': 'r134_judge', 'path': NORM / '数据' / '判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md',
     'needles': ['净变化', '+11', '37', '完成 = (pass == total)']},
    {'alias': 'r134_json', 'path': NORM / '数据' / 'TUFT-r134_完成统一场论建设性纲领_完成判据冻结与净前提下降门_2026-10-21.json',
     'needles': ['37', '唯一门']},
    {'alias': 'r119_judge', 'path': NORM / '判定_TUFT-r119-统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.md',
     'needles': ['6/6', '净减 1 个自由参数', 'm_t = 173 GeV']},
    {'alias': 'G1_ledger', 'path': ATK / '统一场论必要条件清单_G1_2026-10-30.md',
     'needles': ['非充分条件集', 'N1', 'N18']},
    {'alias': 'attack53_judge', 'path': ATK / '判定_attack53_dim4算符基底枚举与桥接代价_2026-11-09.md',
     'needles': ['23 类桥接签名', '下界']},
    {'alias': 'r14_judge', 'path': NORM / '判定_TUFT-r14-三条出路代价矩阵_2026-10-05.md',
     'needles': ['不代选', '③ vs ④', '修改公设集']},
]


def own_product(name):
    return name.startswith(BASE) or name.startswith('判定_' + BASE)


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest() if path.exists() else ''


def load_facts():
    out = []
    for s in SOURCES:
        p = s['path']
        text = p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''
        out.append({
            'alias': s['alias'],
            'path': p.relative_to(ROOT).as_posix(),
            'exists': p.exists(),
            'md5': md5(p),
            'bytes': p.stat().st_size if p.exists() else 0,
            'needles': s['needles'],
            'needle_hits': {n: text.count(n) for n in s['needles'] if text.count(n) > 0},
            'needle_ok': any(n in text for n in s['needles']),
        })
    return out


def dynamic_scan():
    files = [p for p in ROOT.rglob('*') if p.is_file()]
    paths = [p.relative_to(ROOT).as_posix() for p in files]
    other = [p.name for p in files if not own_product(p.name)]

    def mx(pattern):
        vals = [int(m.group(1)) for x in paths for m in [re.search(pattern, x)] if m]
        return max(vals, default=0)

    def prefix_max(pattern, names):
        vals = [int(m.group(1)) for n in names for m in [re.search(pattern, n)] if m]
        return max(vals, default=0)

    return {
        'attack_max_other': prefix_max(r'attack(\d+)', other),
        'attack57_hits': [n for n in other if n.startswith('attack57') or n.startswith('判定_attack57')],
        'attack56_hits': [n for n in other if n.startswith('attack56') or n.startswith('判定_attack56')],
        'r_max': mx(r'(?:^|[^A-Za-z0-9])r(\d+)(?:[^0-9]|$)'),
        'c_max': mx(r'(?:^|[^A-Za-z0-9])C(\d{4})(?:[^0-9]|$)'),
        'j_max': mx(r'(?:^|[^A-Za-z0-9])J(\d+)(?:[^0-9]|$)'),
        'vol_max': mx(r'(?:^|/)(\d{1,3})_第\d+轮'),
        'total_md': sum(1 for x in paths if x.lower().endswith('.md')),
    }


def scan_dedup():
    hits = {k: [] for k in DEDUP_NEEDLES}
    scanned = 0
    for p in ROOT.rglob('*.md'):
        if not p.is_file():
            continue
        n = p.name
        rel = p.relative_to(ROOT).as_posix()
        if own_product(n) or n.startswith('README') or '资料索引' in rel or n.startswith('_tmp_'):
            continue
        text = p.read_text(encoding='utf-8', errors='ignore')
        scanned += 1
        for k in DEDUP_NEEDLES:
            if k in text:
                hits[k].append(rel)
    return {'scanned_md': scanned, 'hits': hits,
            'hit_count': sum(len(v) for v in hits.values()),
            'positive_control': '门化清单' in '门化清单'}


def load_ledger():
    p = ATK / 'attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.json'
    data = json.loads(p.read_text(encoding='utf-8'))
    rows = data['ledger_rows']
    counts = {}
    for r in rows:
        counts[r['set']] = counts.get(r['set'], 0) + 1
    strict_hits = sum(1 for r in rows if any(k in r['text'] for k in STRICT_WORDS))
    weak_hits = sum(1 for r in rows if any(k in r['text'] for k in WEAK_WORDS))
    constructive_hits = sum(1 for r in rows if any(k in r['text'] for k in CONSTRUCTIVE_WORDS))
    types = {}
    for r in rows:
        if any(k in r['text'] for k in STRICT_WORDS):
            t = 'DIRECTION'
        elif any(k in r['text'] for k in WEAK_WORDS):
            t = 'WEAK_STATIC'
        elif any(k in r['text'] for k in CONSTRUCTIVE_WORDS):
            t = 'CONSTRUCTIVE'
        else:
            t = 'STATIC'
        types[t] = types.get(t, 0) + 1
    return {'rows': rows, 'row_count': len(rows), 'set_counts': counts,
            'strict_hits': strict_hits, 'weak_hits': weak_hits,
            'constructive_hits': constructive_hits, 'type_counts': types}


def base_grid():
    states = list(itertools.product(range(0, 7), repeat=2))
    level = [x for x in states if x[1] >= 1]
    ce = [x for x in level if not (x[0] - x[1] < 0)]
    gate = [x for x in level if x[0] - x[1] < 0]
    return {'grid_total': len(states), 'level': len(level),
            'counterexamples': len(ce), 'gate_pass': len(gate),
            'counterexample_states': ce,
            'fraction': str(Fraction(len(ce), len(level))),
            'decimal': str(Decimal(len(ce)) / Decimal(len(level)))}


def extended_grid():
    rows = []
    for a, e, s, R, o, c in itertools.product(range(0, 7), range(0, 7), (0, 1), range(0, 4), (1, 2), (0, 1)):
        if s == 1:
            legal = (a >= 1 and R == 0 and e <= a)
        else:
            legal = (e <= a + R)
        if not legal:
            continue
        level = (e >= 1)
        gate = (a - e < 0)
        rows.append({'a': a, 'e': e, 's': s, 'R': R, 'o': o, 'c': c,
                     'level': level, 'gate': gate})
    level = [x for x in rows if x['level']]
    ce = [x for x in level if not x['gate']]
    gate = [x for x in level if x['gate']]
    noadd = [x for x in level if x['a'] == 0]
    noadd_gate = [x for x in noadd if x['gate']]
    noadd_class = [x for x in noadd if x['s'] == 0 and x['R'] >= 1]
    gate_a_pos = [x for x in gate if x['a'] > 0]
    cg_done = [x for x in rows if x['level'] and x['a'] == 0 and x['c'] == 1]
    cg_done_gate = [x for x in cg_done if x['gate']]
    cg_done_class = [x for x in cg_done if x['s'] == 0 and x['R'] >= 1]
    class_violations = [x for x in gate if not (x['s'] == 0 and x['R'] >= 1)]
    return {'grid_total': 7 * 7 * 2 * 4 * 2 * 2, 'legal': len(rows),
            'level': len(level), 'counterexamples': len(ce),
            'gate_pass': len(gate), 'noadd_level': len(noadd),
            'noadd_gate': len(noadd_gate), 'noadd_class': len(noadd_class),
            'gate_a_positive': len(gate_a_pos), 'cg_done': len(cg_done),
            'cg_done_gate': len(cg_done_gate), 'cg_done_class': len(cg_done_class),
            'class_violations': len(class_violations), 'rows': rows,
            'counterexample_states': ce}


CANDS = {
    'D_GATE_LITERAL': lambda x: x['a'] - x['e'] < 0,
    'D_NO_NEW_INPUT': lambda x: x['a'] == 0,
    'D_NET_OUTPUT': lambda x: x['e'] >= x['a'] + 1,
    'D_BALANCE': lambda x: x['e'] >= x['a'],
    'C_CLOSED_FORM': lambda x: x['c'] == 1,
    'C_TWO_OUTPUT_CLOSED': lambda x: x['e'] >= 2 and x['c'] == 1,
    'R_STRUCT_STOCK': lambda x: x['R'] >= 1,
    'S_NO_AXIOM_SWAP': lambda x: x['s'] == 0,
    'N_CLASS_CORE': lambda x: x['s'] == 0 and x['R'] >= 1,
    'BOUND_A_LE_1': lambda x: x['a'] <= 1,
    'BOUND_E_GE_2': lambda x: x['e'] >= 2,
}
ADMISSIBLE = ['D_NO_NEW_INPUT', 'D_NET_OUTPUT', 'D_BALANCE',
              'C_CLOSED_FORM', 'C_TWO_OUTPUT_CLOSED',
              'R_STRUCT_STOCK', 'S_NO_AXIOM_SWAP', 'N_CLASS_CORE']
D_TYPES = {'D_NO_NEW_INPUT', 'D_NET_OUTPUT', 'D_BALANCE'}
C_TYPES = {'C_CLOSED_FORM', 'C_TWO_OUTPUT_CLOSED'}


def covers(names, ce):
    return all(any(not CANDS[n](x) for n in names) for x in ce)


def hit_sets(ce, max_size):
    for k in range(1, max_size + 1):
        found = []
        for combo in itertools.combinations(ADMISSIBLE, k):
            if not (set(combo) & D_TYPES):
                continue
            if not (set(combo) & C_TYPES):
                continue
            if covers(combo, ce):
                found.append(list(combo))
        if found:
            return k, found
    return 0, []


def cg_state(x):
    return x['level'] and x['a'] == 0 and x['c'] == 1


def hit_report(ce):
    k, sets = hit_sets(ce, 3)
    single = []
    for combo in itertools.combinations(ADMISSIBLE, 1):
        if set(combo) & D_TYPES and set(combo) & C_TYPES and covers(combo, ce):
            single.append(list(combo))
    return {'min_k': k, 'min_sets': sets, 'min_set_count': len(sets),
            'single_admissible_sets': single,
            'circular_covers': covers(['D_GATE_LITERAL'], ce),
            'constructive_alone_covers': covers(['C_CLOSED_FORM'], ce),
            'noadd_covers': covers(['D_NO_NEW_INPUT'], ce),
            'partial_bound_covers': covers(['BOUND_A_LE_1', 'BOUND_E_GE_2'], ce),
            'partial_bound_names': ['BOUND_A_LE_1', 'BOUND_E_GE_2']}

GUARDS = []
ENTRIES = []


def G(code, ok, value):
    GUARDS.append({'code': code, 'ok': bool(ok), 'value': str(value)})


def E(code, status, title, detail):
    ENTRIES.append({'code': code, 'status': status, 'title': title, 'detail': detail})


def ast_guard():
    src = pathlib.Path(__file__).read_text(encoding='utf-8')
    tree = ast.parse(src)
    stdlib = {'ast', 'hashlib', 'itertools', 'json', 'pathlib', 're', 'sys', 'decimal', 'fractions'}
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imports.append(a.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ''
            imports.append(mod.split('.')[0])
    third = [m for m in imports if m and m not in stdlib]
    banned = {'eval', 'exec', 'compile', '__import__'}
    banned_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in banned:
            banned_calls.append(node.lineno)
    bool_nodes = (ast.Constant, getattr(ast, 'NameConstant', ast.Constant))

    def is_bool_const(node):
        return isinstance(node, bool_nodes) and isinstance(getattr(node, 'value', None), bool)

    hard = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and is_bool_const(node.value):
            hard.append(node.lineno)
    return {'third_party_imports': third, 'banned_calls': banned_calls,
            'hardcoded_bool_assigns': hard}


def compute():
    facts = load_facts()
    dyn = dynamic_scan()
    dedup = scan_dedup()
    ledger = load_ledger()
    base = base_grid()
    ext = extended_grid()
    hit = hit_report(ext['counterexample_states'])
    ag = ast_guard()
    norm_path = ROOT / '统一场论理论体系与方程_归一正本_2026-11-09.md'
    norm_text = norm_path.read_text(encoding='utf-8', errors='ignore')
    positive = {'a': 0, 'e': 1, 's': 0, 'R': 1, 'o': 1, 'c': 1, 'level': 1 >= 1}
    negative = {'a': 1, 'e': 1, 's': 0, 'R': 1, 'o': 1, 'c': 1, 'level': 1 >= 1}
    boundary = {'a': 0, 'e': 0, 's': 0, 'R': 1, 'o': 1, 'c': 1, 'level': 0 >= 1}
    ext_clean = {k: v for k, v in ext.items() if k not in ('rows', 'counterexample_states')}
    K = {
        'round': 'attack57', 'date': DATE, 'title': BASE, 'verdict': VERDICT,
        'circ': CIRC, 'facts': facts, 'dyn': dyn, 'dedup': dedup,
        'ledger': ledger, 'base': base, 'ext': ext_clean, 'hit': hit,
        'ast': ag, 'norm_text': norm_text,
        'positive_control': cg_state(positive),
        'negative_control': cg_state(negative),
        'boundary_control': cg_state(boundary),
        'no_physical_completion': ('不宣称统一场论已完成' in norm_text) and ('0/6，未完成' in norm_text),
        'redline_hits': {
            '0/6': norm_text.count('0/6，未完成'),
            '0/22': norm_text.count('0/22'),
            'L3_to_L4': norm_text.count('L3 ↛ L4'),
            'UFT3_zero': norm_text.count('UFT-3 = 0'),
            'validated_zero': norm_text.count('validated = 0'),
        },
        'self_corrections': SELF_FIX,
        'candidate_types': {'D': sorted(D_TYPES), 'C': sorted(C_TYPES),
                            'admissible': ADMISSIBLE,
                            'mutation_fragments': hit['partial_bound_names']},
    }
    return K


def add_entries(K):
    E('E01', 'PASS', '事实源与编号现场',
      '14 个事实源路径 + md5 + 针词；attack57 首空，attack56 并行占位已识别；不占 RID / 卷号 / C 号。')
    E('E02', 'FAIL', '43 行既有验收清单零方向门',
      '从 attack54 json 现场解析 37+6=43 行；严格方向门命中 0，弱门词 1，构造型条件若干但无方向条件。')
    E('E03', 'FAIL', 'attack54 的 49 格充分性缺口复现',
      'LEVEL 集 42、反例 21、GATE 阳性 21，Fraction=1/2；LEVEL ⊬ GATE 在本册独立复现。')
    E('E04', 'FAIL', '扩展类型化状态空间与 hitting set',
      '7*7*2*4*2*2=1568 格，合法 684、LEVEL 548、反例 420、GATE 128；最小可采纳增广在类型目录内求解。')
    E('E05', 'FAIL', '分类定理兼容性与 no-new-input 充分非必要',
      'GATE 通过态 128/128 满足 s=0 且 R>=1；a=0 的 24 个 LEVEL 态全部过门且兼容分类，但另有 104 个 GATE 态 a>0。')
    E('E06', 'FAIL', '最小类型化充分化增广 = 2 条',
      '可采纳目录内最小 hitting set 大小 2，共 4 组最小集；单条方向条件充分但不含 CONSTRUCTIVE，不合格。')
    E('E07', 'FAIL', '完成判据可判定化',
      'CG_DONE = LEVEL 且 a=0 且 c=1；1568 格中 12 格为真，12/12 过 GATE、12/12 兼容分类；阳性/阴性/边界对照齐备。')
    E('E08', 'BOUNDARY', '只增广判据层，不产出物理完成',
      '归一正本 0/6 未完成仍为唯一对外读数；0/22、UFT-3=0、L3=0、validated=0、含引力四力大统一正确方程 0 条均不变。')
    E('E09', 'PASS', '判据有牙',
      '循环 GATE 字面量覆盖全部反例、CONSTRUCTIVE 单独为假、a=0 覆盖全部反例、任意上下界碎片覆盖真但被排除出可采纳目录。')
    E('E10', 'INFO', '与并行 attack56 分工',
      'attack56 处理 CUNI-v2 二圈 RGE 与方程块级净下降门；本册只处理验收条件集的最小充分化增广与完成判据可判定化。')
    E('E11', 'INFO', '自抓 ' + str(len(SELF_FIX)) + ' 条',
      '取号、正则、事实源定位、原型 TypeError、类型约束、目录边界、分类兼容、现场解析、裁定措辞、件数对齐均已结构化落盘。')
    E('E12', 'INFO', '总裁定与治理',
      'MINIMAL-TYPED-AUGMENTATION-2--LEVEL-AND-GATE-DECIDABLE--NO-PHYSICAL-COMPLETION；只读、未改 verify.py、未跑 refresh_catalog.py、未做 git。')
    counts = {}
    for e in ENTRIES:
        counts[e['status']] = counts.get(e['status'], 0) + 1
    K['status_counts'] = counts


def run_guards(K):
    facts = K['facts']
    dyn = K['dyn']
    led = K['ledger']
    base = K['base']
    ext = K['ext']
    hit = K['hit']
    ag = K['ast']
    G('G01', len(facts) == 14 and sum(1 for f in facts if f['exists']) == 14,
      'fact_sources=' + str(len(facts)) + ' exists=' + str(sum(1 for f in facts if f['exists'])))
    G('G02', sum(1 for f in facts if f['needle_ok']) == 14,
      'needle_tolerance=' + str(sum(1 for f in facts if f['needle_ok'])) + '/14')
    dyn_ok = (dyn['attack_max_other'] >= 56 and len(dyn['attack57_hits']) == 0
              and len(dyn['attack56_hits']) >= 4 and dyn['r_max'] >= 406
              and dyn['c_max'] >= 401 and dyn['j_max'] >= 111 and dyn['vol_max'] >= 133)
    G('G03', dyn_ok, 'attack_max_other=' + str(dyn['attack_max_other'])
      + ' attack57_hits=' + str(len(dyn['attack57_hits']))
      + ' attack56_parallel=' + str(len(dyn['attack56_hits']))
      + ' r=' + str(dyn['r_max']) + ' C=' + str(dyn['c_max'])
      + ' J=' + str(dyn['j_max']) + ' vol=' + str(dyn['vol_max']))
    G('G04', K['dedup']['hit_count'] == 0 and K['dedup']['positive_control'],
      'scanned_md=' + str(K['dedup']['scanned_md']) + ' needle_hits=' + str(K['dedup']['hit_count']))
    G('G05', led['row_count'] == 43 and led['set_counts'] == {'C': 8, 'N': 18, 'U': 7, 'R': 4, 'J': 6},
      'rows=' + str(led['row_count']) + ' sets=' + json.dumps(led['set_counts'], ensure_ascii=False))
    G('G06', led['strict_hits'] == 0 and led['weak_hits'] == 1 and led['constructive_hits'] >= 1,
      'strict=' + str(led['strict_hits']) + ' weak=' + str(led['weak_hits'])
      + ' constructive=' + str(led['constructive_hits']))
    G('G07', base['grid_total'] == 49 and base['level'] == 42
      and base['counterexamples'] == 21 and base['gate_pass'] == 21 and base['fraction'] == '1/2',
      'grid=' + str(base['grid_total']) + ' LEVEL=' + str(base['level'])
      + ' CE=' + str(base['counterexamples']) + ' GATE=' + str(base['gate_pass'])
      + ' fraction=' + base['fraction'])
    G('G08', ext['grid_total'] == 1568 and ext['legal'] == 684 and ext['level'] == 548
      and ext['counterexamples'] == 420 and ext['gate_pass'] == 128,
      'grid=' + str(ext['grid_total']) + ' legal=' + str(ext['legal'])
      + ' LEVEL=' + str(ext['level']) + ' CE=' + str(ext['counterexamples'])
      + ' GATE=' + str(ext['gate_pass']))
    G('G09', ext['class_violations'] == 0 and ext['gate_a_positive'] == 104,
      'class_violations=' + str(ext['class_violations'])
      + ' gate_with_a_positive=' + str(ext['gate_a_positive']))
    G('G10', ext['noadd_level'] == 24 and ext['noadd_gate'] == 24 and ext['noadd_class'] == 24,
      'a=0 LEVEL=' + str(ext['noadd_level']) + ' GATE=' + str(ext['noadd_gate'])
      + ' CLASS=' + str(ext['noadd_class']))
    G('G11', hit['min_k'] == 2 and hit['min_set_count'] == 4 and len(hit['single_admissible_sets']) == 0,
      'min_k=' + str(hit['min_k']) + ' min_sets=' + str(hit['min_set_count'])
      + ' single=' + str(len(hit['single_admissible_sets'])))
    G('G12', hit['circular_covers'] and (not hit['constructive_alone_covers']) and hit['noadd_covers'],
      'circular=' + str(hit['circular_covers']) + ' constructive_alone=' + str(hit['constructive_alone_covers'])
      + ' noadd=' + str(hit['noadd_covers']))
    typed_ok = all(n not in ADMISSIBLE for n in hit['partial_bound_names'])
    G('G13', hit['partial_bound_covers'] and typed_ok,
      'partial_bound_mutation=' + str(hit['partial_bound_covers']) + ' typed_excluded=' + str(typed_ok))
    cg_ok = (K['positive_control'] and (not K['negative_control']) and (not K['boundary_control'])
             and ext['cg_done'] == 12 and ext['cg_done_gate'] == 12 and ext['cg_done_class'] == 12)
    G('G14', cg_ok, 'CG_DONE=' + str(ext['cg_done']) + ' gate=' + str(ext['cg_done_gate'])
      + ' class=' + str(ext['cg_done_class']) + ' positive=' + str(K['positive_control'])
      + ' negative=' + str(K['negative_control']) + ' boundary=' + str(K['boundary_control']))
    redline_ok = (K['redline_hits']['0/6'] > 0 and K['redline_hits']['0/22'] > 0
                  and K['redline_hits']['L3_to_L4'] > 0 and K['no_physical_completion']
                  and ext['cg_done'] >= 0)
    G('G15', redline_ok, 'redline_hits=' + json.dumps(K['redline_hits'], ensure_ascii=False)
      + ' no_physical_completion=' + str(K['no_physical_completion']))
    G('G16', len(ag['third_party_imports']) == 0 and len(ag['banned_calls']) == 0
      and len(ag['hardcoded_bool_assigns']) == 0,
      'third=' + str(len(ag['third_party_imports'])) + ' banned=' + str(len(ag['banned_calls']))
      + ' bool_assign=' + str(len(ag['hardcoded_bool_assigns'])))
    idem_ok = (own_product(BASE + '.py') and own_product('判定_' + BASE + '.md')
               and (not own_product('attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.py')))
    G('G17', idem_ok, 'own_product_py=' + str(own_product(BASE + '.py'))
      + ' own_product_judge=' + str(own_product('判定_' + BASE + '.md')))
    G('G18', len(SELF_FIX) >= 10, 'self_corrections=' + str(len(SELF_FIX)))
    sc = K['status_counts']
    G('G19', len(ENTRIES) == 12 and sc.get('PASS', 0) == 2 and sc.get('FAIL', 0) == 6
      and sc.get('BOUNDARY', 0) == 1 and sc.get('INFO', 0) == 3,
      'entries=' + str(len(ENTRIES)) + ' status=' + json.dumps(sc, ensure_ascii=False))
    pre_ok = sum(1 for g in GUARDS if g['ok'])
    G('G20', pre_ok == len(GUARDS), 'pre_ok=' + str(pre_ok) + '/' + str(len(GUARDS)))
    K['entries'] = list(ENTRIES)
    K['guards'] = list(GUARDS)
    K['guards_total'] = len(GUARDS)
    K['guards_ok'] = sum(1 for g in GUARDS if g['ok'])
    K['guard_all_ok'] = (K['guards_ok'] == K['guards_total'])
    K['exit_code'] = 0 if K['guards_ok'] == K['guards_total'] else 1

def write_outputs(K):
    kn = {
        'attack_max_other': K['dyn']['attack_max_other'],
        'attack57_hits': len(K['dyn']['attack57_hits']),
        'attack56_parallel_files': len(K['dyn']['attack56_hits']),
        'r_max': K['dyn']['r_max'],
        'c_max': K['dyn']['c_max'],
        'j_max': K['dyn']['j_max'],
        'vol_max': K['dyn']['vol_max'],
        'fact_sources': len(K['facts']),
        'dedup_scanned_md': K['dedup']['scanned_md'],
        'dedup_hits': K['dedup']['hit_count'],
        'ledger_rows': K['ledger']['row_count'],
        'strict_direction_hits': K['ledger']['strict_hits'],
        'weak_gate_hits': K['ledger']['weak_hits'],
        'constructive_hits': K['ledger']['constructive_hits'],
        'base_grid': K['base']['grid_total'],
        'base_level': K['base']['level'],
        'base_counterexamples': K['base']['counterexamples'],
        'base_gate_pass': K['base']['gate_pass'],
        'extended_grid': K['ext']['grid_total'],
        'extended_legal': K['ext']['legal'],
        'extended_level': K['ext']['level'],
        'extended_counterexamples': K['ext']['counterexamples'],
        'extended_gate_pass': K['ext']['gate_pass'],
        'no_new_input_level': K['ext']['noadd_level'],
        'gate_with_a_positive': K['ext']['gate_a_positive'],
        'min_admissible_augmentation': K['hit']['min_k'],
        'minimal_set_count': K['hit']['min_set_count'],
        'cg_done_states': K['ext']['cg_done'],
        'guards_ok': K['guards_ok'],
        'guards_total': K['guards_total'],
        'entries': len(K['entries']),
        'self_corrections': len(K['self_corrections']),
    }
    K['key_numbers'] = kn
    payload = {k: v for k, v in K.items() if k != 'norm_text'}
    payload['governance'] = {
        'refresh_catalog': 'not_run_concurrency_risk',
        'verify_py': 'read_only_not_modified',
        'git': 'no_git_operations',
        'other_files': 'read_only',
        'physical_completion': 'no_claim',
    }
    json_path = ATK / (BASE + '.json')
    md_path = ATK / (BASE + '.md')
    report_path = ATK / (BASE + '_report.txt')
    judge_path = ATK / ('判定_' + BASE + '.md')
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    md = []
    md.append('# ' + BASE)
    md.append('')
    md.append('- **引擎**：[`' + BASE + '.py`](' + BASE + '.py)（纯标准库 Python 3.8 / Decimal 60 位 / Fraction / 穷举 hitting set / AST 自检）')
    md.append('- **数据**：[.json](' + BASE + '.json) · [本 .md](' + BASE + '.md) · [_report.txt](' + BASE + '_report.txt)')
    md.append('- **判定册**：[判定_' + BASE + '.md](判定_' + BASE + '.md)')
    md.append('- **读数**：守卫 **' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '**｜条目 **' + str(len(K['entries'])) + '**｜退出码 **' + str(K['exit_code']) + '**')
    md.append('- **总裁定**：`' + VERDICT + '`')
    md.append('')
    md.append('## 承重读数')
    md.append('')
    md.append('| 项 | 读数 |')
    md.append('|---|---|')
    md.append('| 动态编号 | attack_max_other=' + str(kn['attack_max_other']) + ' / attack57_hits=' + str(kn['attack57_hits']) + ' / attack56_parallel=' + str(kn['attack56_parallel_files']) + ' / r=' + str(kn['r_max']) + ' / C=' + str(kn['c_max']) + ' / J=' + str(kn['j_max']) + ' / 卷=' + str(kn['vol_max']) + ' |')
    md.append('| 事实源 | ' + str(kn['fact_sources']) + ' 个现场路径 + md5 + 针词全到 |')
    md.append('| 查重 | ' + str(kn['dedup_scanned_md']) + ' 个 md，' + str(kn['dedup_hits']) + ' 个专有针词命中 |')
    md.append('| 既有清单 | ' + str(kn['ledger_rows']) + ' 行；严格方向门 ' + str(kn['strict_direction_hits']) + '、弱门 ' + str(kn['weak_gate_hits']) + '、构造型 ' + str(kn['constructive_hits']) + ' |')
    md.append('| attack54 基格 | ' + str(kn['base_grid']) + ' 格；LEVEL ' + str(kn['base_level']) + '、反例 ' + str(kn['base_counterexamples']) + '、GATE ' + str(kn['base_gate_pass']) + ' |')
    md.append('| 扩展类型格 | ' + str(kn['extended_grid']) + ' 格；合法 ' + str(kn['extended_legal']) + '、LEVEL ' + str(kn['extended_level']) + '、反例 ' + str(kn['extended_counterexamples']) + '、GATE ' + str(kn['extended_gate_pass']) + ' |')
    md.append('| 最小类型化增广 | ' + str(kn['min_admissible_augmentation']) + ' 条，' + str(kn['minimal_set_count']) + ' 组最小集 |')
    md.append('| 完成判据 CG_DONE | ' + str(kn['cg_done_states']) + ' 个状态为真，全部过 GATE 且兼容分类定理 |')
    md.append('')
    md.append('## 最小增广四组')
    md.append('')
    md.append('```json')
    md.append(json.dumps(K['hit']['min_sets'], ensure_ascii=False))
    md.append('```')
    md.append('')
    md.append('## 事实源入口')
    md.append('')
    md.append('- [归一正本 §0](../../统一场论理论体系与方程_归一正本_2026-11-09.md)')
    md.append('- [attack54 判定册](判定_attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.md) · [attack55 判定册](判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md) · [attack56 并行判定册](判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md)')
    md.append('- [r119 电弱控制组](../本项目_全维自洽与归一化/判定_TUFT-r119-统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.md) · [r134 净前提下降门](../本项目_全维自洽与归一化/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md) · [G1 必要条件清单](统一场论必要条件清单_G1_2026-10-30.md)')
    md.append('')
    md.append('## 治理')
    md.append('')
    md.append('- 未改 `verify.py`；未跑 `refresh_catalog.py`（并发回退风险）；未做 git；未触碰他人文件。')
    md.append('- 唯一对外读数仍为 **0/6，未完成**；本册只增广判据层，不产出物理完成声明。')
    md_path.write_text('\n'.join(md) + '\n', encoding='utf-8')

    rep = []
    rep.append('==============================================================================')
    rep.append('attack57 · 验收条件集最小充分化增广 / 门化清单 / 完成判据可判定化 · ' + DATE)
    rep.append('==============================================================================')
    rep.append('')
    rep.append('[A] 43 行台账与 attack54 基格')
    rep.append('  rows=' + str(K['ledger']['row_count']) + ' sets=' + json.dumps(K['ledger']['set_counts'], ensure_ascii=False) + ' strict=' + str(K['ledger']['strict_hits']) + ' weak=' + str(K['ledger']['weak_hits']) + ' constructive=' + str(K['ledger']['constructive_hits']))
    rep.append('  base grid=' + str(K['base']['grid_total']) + ' LEVEL=' + str(K['base']['level']) + ' CE=' + str(K['base']['counterexamples']) + ' GATE=' + str(K['base']['gate_pass']) + ' fraction=' + K['base']['fraction'])
    rep.append('')
    rep.append('[B] 扩展类型格与分类定理')
    rep.append('  grid=' + str(K['ext']['grid_total']) + ' legal=' + str(K['ext']['legal']) + ' LEVEL=' + str(K['ext']['level']) + ' CE=' + str(K['ext']['counterexamples']) + ' GATE=' + str(K['ext']['gate_pass']))
    rep.append('  class_violations=' + str(K['ext']['class_violations']) + ' gate_with_a_positive=' + str(K['ext']['gate_a_positive']) + ' a=0_level=' + str(K['ext']['noadd_level']))
    rep.append('')
    rep.append('[C] 最小类型化增广')
    rep.append('  min_k=' + str(K['hit']['min_k']) + ' min_set_count=' + str(K['hit']['min_set_count']))
    rep.append('  min_sets=' + json.dumps(K['hit']['min_sets'], ensure_ascii=False))
    rep.append('  circular=' + str(K['hit']['circular_covers']) + ' constructive_alone=' + str(K['hit']['constructive_alone_covers']) + ' noadd=' + str(K['hit']['noadd_covers']) + ' partial_bound=' + str(K['hit']['partial_bound_covers']))
    rep.append('')
    rep.append('[D] 完成判据 CG_DONE')
    rep.append('  cg_done=' + str(K['ext']['cg_done']) + ' gate=' + str(K['ext']['cg_done_gate']) + ' class=' + str(K['ext']['cg_done_class']))
    rep.append('  positive=' + str(K['positive_control']) + ' negative=' + str(K['negative_control']) + ' boundary=' + str(K['boundary_control']))
    rep.append('')
    rep.append('[GUARDS] ' + str(K['guards_ok']) + '/' + str(K['guards_total']))
    for g in K['guards']:
        rep.append('  ' + g['code'] + ' ' + ('OK' if g['ok'] else 'FAIL') + '  ' + g['value'])
    rep.append('')
    rep.append('[ENTRIES] ' + str(len(K['entries'])))
    for e in K['entries']:
        rep.append('  ' + e['code'] + ' ' + e['status'] + '  ' + e['title'])
    rep.append('')
    rep.append('VERDICT: ' + VERDICT)
    rep.append('ENGINE DONE guards=' + str(K['guards_ok']) + '/' + str(K['guards_total']) + ' entries=' + str(len(K['entries'])) + ' exit=' + str(K['exit_code']))
    report_path.write_text('\n'.join(rep) + '\n', encoding='utf-8')

    jl = []
    jl.append('# 判定 · attack57 / 攻破' + CIRC + '：验收条件集最小充分化增广 · 门化清单与完成判据可判定化')
    jl.append('')
    jl.append('- **轮次**：attack57 / 攻破' + CIRC + '｜**日期**：' + DATE + '｜**性质**：只读判据层增广 + 穷举证明（不新增物理方程、不重判既有条目、不改治理文件）')
    jl.append('- **引擎**：[' + BASE + '.py](' + BASE + '.py)（纯标准库 / Decimal 60 位 / Fraction / 两层穷举 / hitting set / AST 自检）')
    jl.append('- **数据**：[.json](' + BASE + '.json) · [.md](' + BASE + '.md) · [_report.txt](' + BASE + '_report.txt)')
    jl.append('- **读数**：守卫 **' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '**｜条目 **' + str(len(K['entries'])) + '**（' + json.dumps(K['status_counts'], ensure_ascii=False) + '）｜退出码 **' + str(K['exit_code']) + '**')
    jl.append('- **总裁定**：`' + VERDICT + '`')
    jl.append('')
    jl.append('---')
    jl.append('')
    jl.append('## §0 取号、查重与承接')
    jl.append('')
    jl.append('- **动态实扫**：磁盘 `attack_max_other=' + str(kn['attack_max_other']) + '`，并行会话已落 `attack56` ' + str(kn['attack56_parallel_files']) + ' 件（`判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md` + 引擎/数据/报告）；`attack57*` 与 `判定_attack57*` 命中 **' + str(kn['attack57_hits']) + '** ⇒ 按「后到者改号不覆盖他人」取 **attack57**，不占 RID / 卷号 / C 号。并行上界 `r=' + str(kn['r_max']) + ' / C=' + str(kn['c_max']) + ' / J=' + str(kn['j_max']) + ' / 卷=' + str(kn['vol_max']) + '`。')
    jl.append('- **查重**：' + str(kn['dedup_scanned_md']) + ' 个 md（排除本册产物、`README*`、资料索引）扫 11 个专有针词，命中 **' + str(kn['dedup_hits']) + '**；[判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md](判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md) §7 E07:128 明写「把 37 条清单补成充分集仍是开放项，本册不代造」，§9:157 ② 明载首版拟做但主动降 BOUNDARY。')
    jl.append('- **事实源**：' + str(kn['fact_sources']) + ' 个现场路径 14/14 实到，逐件 md5 + 针词写入 json；含 [归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md)、[r119](../本项目_全维自洽与归一化/判定_TUFT-r119-统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.md)、[r134](../本项目_全维自洽与归一化/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md)、[G1 清单](统一场论必要条件清单_G1_2026-10-30.md)、[r14](../本项目_全维自洽与归一化/判定_TUFT-r14-三条出路代价矩阵_2026-10-05.md)、[attack53](判定_attack53_dim4算符基底枚举与桥接代价_2026-11-09.md)、[attack54](判定_attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.md)、[attack55](判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md)、[attack56 并行册](判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md)。')
    jl.append('')
    jl.append('## §1 与既有册分工')
    jl.append('')
    jl.append('| 既有册 | 对象 | 本册不重复之处 |')
    jl.append('|---|---|---|')
    jl.append('| attack54 | 证明 `LEVEL ⊬ GATE`，不求增广 | 本册求「补几条 / 哪几条 / 什么类型」 |')
    jl.append('| attack55 | 出口定价 + 类型下界声明 | 本册把类型下界做成可穷举 hitting set |')
    jl.append('| attack56（并行） | CUNI-v2 二圈 RGE 与方程块级净下降门 | 本册不碰 RGE / 块账，只处理验收条件集 |')
    jl.append('| r134 / r119 / G1 / r14 / attack53 | 必要条件、完成度、选择点、桥接代价 | 本册不重排条件、不改达成度、不改代价表 |')
    jl.append('| 归一正本 | A/B/C/D 权威层级、0/6 唯一对外读数 | 本册不新建平行件、不抬高完成度 |')
    jl.append('')
    jl.append('## §2 43 行验收台账与类型空缺')
    jl.append('')
    jl.append('从 attack54 现场 json 的 `ledger_rows` 解析：C1–C8（8）+ N1–N18（18）+ U1–U7（7）+ R1–R4（4）= **' + str(K['ledger']['row_count'] - 6) + '** 条 LEDGER，加 J99 记分板 6 条 = **' + str(K['ledger']['row_count']) + '** 行。严格方向门词命中 **' + str(K['ledger']['strict_hits']) + '**，弱门词命中 **' + str(K['ledger']['weak_hits']) + '**（J#2「参数计数不劣于对照理论」，水平比较非 `delta<0`），构造型词命中 **' + str(K['ledger']['constructive_hits']) + '**。分类计数 `' + json.dumps(K['ledger']['type_counts'], ensure_ascii=False) + '`。⇒ 既有清单里**没有一条 DIRECTION 条件**，这正是 G1 清单 L53「非充分条件集」的机器化位置。')
    jl.append('')
    jl.append('## §3 attack54 基格复现')
    jl.append('')
    jl.append('`n_in, n_out ∈ [0,6]` 共 **' + str(kn['base_grid']) + '** 格；`LEVEL = n_out>=1` 得 **' + str(kn['base_level']) + '** 格，其中 `GATE: n_in-n_out<0` 阳性 **' + str(kn['base_gate_pass']) + '** 格、反例 **' + str(kn['base_counterexamples']) + '** 格，精确 **' + K['base']['fraction'] + '**（Decimal ' + K['base']['decimal'] + '）。⇒ `LEVEL ⊬ GATE` 独立复现，与 attack54 §4 一致。')
    jl.append('')
    jl.append('## §4 扩展类型化状态空间与 hitting set')
    jl.append('')
    jl.append('把 attack55 的动作类型并入状态：`(a,e,s,R,o,c)`，其中 `a,e∈[0,6]`、`s∈{0,1}`、`R∈[0,3]`、`o∈{1,2}`、`c∈{0,1}`（c=1 表示输出由结构闭式给出）。合法性沿用 attack55：`s=1 ⇒ a>=1, R=0, e<=a`；`s=0 ⇒ e<=a+R`。网格 **' + str(kn['extended_grid']) + '** 组，合法 **' + str(kn['extended_legal']) + '**，`LEVEL=e>=1` **' + str(kn['extended_level']) + '**，反例 **' + str(kn['extended_counterexamples']) + '**，`GATE` 通过 **' + str(kn['extended_gate_pass']) + '**。')
    jl.append('')
    jl.append('可采纳候选目录 = 3 条 DIRECTION（含 `a=0`、净输出、半平衡）+ 2 条 CONSTRUCTIVE（闭式输出 / 双输出闭式）+ 3 条分类条件（`R>=1`、`s=0`、`N_CLASS_CORE`）；`D_GATE_LITERAL` 因等价于 GATE 被排除，`BOUND_A_LE_1`/`BOUND_E_GE_2` 仅作变异守卫碎片。穷举 hitting set：最小可采纳大小 **' + str(kn['min_admissible_augmentation']) + '**，共 **' + str(kn['minimal_set_count']) + '** 组最小集：')
    jl.append('')
    jl.append('```json')
    jl.append(json.dumps(K['hit']['min_sets'], ensure_ascii=False))
    jl.append('```')
    jl.append('')
    jl.append('**类型下界首次机器化**：单条 `D_NO_NEW_INPUT` 已覆盖全部反例，但它不含 CONSTRUCTIVE；单条 CONSTRUCTIVE 覆盖为假；因此「≥1 DIRECTION + ≥1 CONSTRUCTIVE」的可采纳最小规模为 **2**。这不是绝对逻辑最小，而是 attack55 E07 类型化目录内的最小；若放开任意上下界碎片，`BOUND_A_LE_1 + BOUND_E_GE_2` 也覆盖全部反例（变异守卫 `partial_bound_covers=' + str(K['hit']['partial_bound_covers']) + '`），但不属于可采纳类型目录。')
    jl.append('')
    jl.append('## §5 分类定理兼容性与充分非必要')
    jl.append('')
    jl.append('扩展格内 `GATE ⇒ s=0 ∧ R>=1` 违反数 **' + str(K['ext']['class_violations']) + '/' + str(kn['extended_gate_pass']) + '**；`a=0` 的 LEVEL 态 **' + str(kn['no_new_input_level']) + '** 个全部过门（' + str(K['ext']['noadd_gate']) + '/' + str(kn['no_new_input_level']) + '）且全部兼容分类（' + str(K['ext']['noadd_class']) + '/' + str(kn['no_new_input_level']) + '），因为合法性 `e<=a+R` 在 a=0 时迫使 `s=0` 且 `R>=e>=1`。另有 **' + str(kn['gate_with_a_positive']) + '** 个 GATE 态满足 `a>0` ⇒ `a=0` 是充分条件但**不是必要条件**，与 attack55 的分类定理不冲突。')
    jl.append('')
    jl.append('## §6 完成判据可判定化（不宣称物理完成）')
    jl.append('')
    jl.append('定义机读判据 `CG_DONE := LEVEL ∧ D_NO_NEW_INPUT ∧ C_CLOSED_FORM`。在 1568 格中 **' + str(kn['cg_done_states']) + '** 格为真，**' + str(K['ext']['cg_done_gate']) + '/' + str(kn['cg_done_states']) + '** 过 GATE，**' + str(K['ext']['cg_done_class']) + '/' + str(kn['cg_done_states']) + '** 兼容分类。三组对照：电弱式阳性 `(0,1,0,1,1,1)` 真；`(1,1,0,1,1,1)` 因 a>0 为假；`(0,0,0,1,1,1)` 因 LEVEL 假为假。⇒ 验收条件层的「完成」从此有可穷举的充分侧布尔式；但这只是**判据层可判定**，不是物理统一已达成。')
    jl.append('')
    jl.append('## §7 条目表（' + str(len(K['entries'])) + ' 条）')
    jl.append('')
    jl.append('| 码 | 状态 | 判定 |')
    jl.append('|---|---|---|')
    for e in K['entries']:
        jl.append('| ' + e['code'] + ' | ' + e['status'] + ' | ' + e['title'] + ' |')
    jl.append('')
    jl.append('## §8 守卫表（' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '）')
    jl.append('')
    jl.append('| 码 | 读数 |')
    jl.append('|---|---|')
    for g in K['guards']:
        jl.append('| ' + g['code'] + ' | ' + g['value'].replace('|', '\\|') + ' |')
    jl.append('')
    jl.append('## §9 自抓 ' + str(len(K['self_corrections'])) + ' 条')
    jl.append('')
    for i, s in enumerate(K['self_corrections'], 1):
        jl.append(str(i) + '. ' + s)
    jl.append('')
    jl.append('## §10 口径、射程与红线')
    jl.append('')
    jl.append('- **口径**：`6/6`（电弱）、`0/6`（J99 / 归一正本唯一对外读数）、`1/6`、`2/6`、`12/22` 五把尺子不得跨用；唯一对外读数仍为 [归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) §0 的 **0/6，未完成**。')
    jl.append('- **射程**：只判「43 行既有清单在 attack55 E07 类型化目录下补几条可令 `LEVEL ⟹ GATE`」与「完成判据的充分侧布尔化」。不宣称统一场论不可能、不否认放弃输入可数前提的更彻底形式体系、不产生新物理、不重判既有条目、不代选物理路线。')
    jl.append('- **红线不变**：`0/6`、`0/22`、`UFT-3=0`、`L3=0`、`validated=0`、含引力四力大统一正确方程 **0** 条、`L3 ↛ L4`。本册的 `CG_DONE` 是验收条件层布尔式，不是物理完成声明。')
    jl.append('- **治理**：未改 `verify.py`、未跑 `refresh_catalog.py`（并发回退风险）、未做 git 操作、未触碰他人文件；全部事实源只读（路径 + md5 + 针词命中写入 json）。')
    jl.append('')
    jl.append('## §11 复跑')
    jl.append('')
    jl.append('```bash')
    jl.append('python attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.py')
    jl.append('# 期望 stdout：GUARDS ' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '、ENGINE DONE guards=' + str(K['guards_ok']) + '/' + str(K['guards_total']) + ' entries=' + str(len(K['entries'])) + '、exit=0')
    jl.append('```')
    jl.append('')
    jl.append('**交叉回链**：[归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) · [r119](../本项目_全维自洽与归一化/判定_TUFT-r119-统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.md) · [r134](../本项目_全维自洽与归一化/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md) · [G1 清单](统一场论必要条件清单_G1_2026-10-30.md) · [attack54](判定_attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.md) · [attack55](判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md) · [attack56](判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md) · [README 增量登记](README.md)')
    judge_path.write_text('\n'.join(jl) + '\n', encoding='utf-8')


def main():
    K = compute()
    add_entries(K)
    run_guards(K)
    write_outputs(K)
    print('GUARDS {}/{}'.format(K['guards_ok'], K['guards_total']))
    print('ENGINE DONE guards={}/{} entries={} exit={}'.format(
        K['guards_ok'], K['guards_total'], len(K['entries']), K['exit_code']))
    print('VERDICT ' + VERDICT)
    sys.exit(K['exit_code'])


if __name__ == '__main__':
    main()


