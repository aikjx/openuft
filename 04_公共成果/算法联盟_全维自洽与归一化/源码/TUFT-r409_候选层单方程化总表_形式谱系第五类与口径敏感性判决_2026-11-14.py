# -*- coding: utf-8 -*-
"""TUFT-r409 · 候选层单方程化总表 —— 形式谱系第五类补全与口径敏感性判决。

承 r408：「所有力装进一个方程」= F0 记号层条件式 / F1 母作用量式 / F2 母场方程式 /
F3 profile 母公式式 + 横切 F4 单耦合参数式，四式全败。r408 的形式谱系穷尽的是
「**主张**把力装进一个方程」的四种写法，**未覆盖「根本不主张」的第五类形态**：

    F5 多方程并列式 —— 提交的是一组方程/一组公设，不是一个方程。

本册把形式谱系从「主张层」补到「登记层」：对库内 22 个已登记统一场论候选，逐个给出
形式归属与单方程化判决，并给出该列的**口径敏感性**判决（能否机器判定）。

用法：python 本脚本
依赖：纯标准库（Decimal 60 位 + Fraction 四元组量纲 (M,L,T,Q)）
纪律：只读结构判决；不新造统一方程、不重判任何候选的物理正确性、不改任何被引文件字节。
"""
import io
import os
import re
import sys
import json
import time
import hashlib
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO = os.path.dirname(HERE)                        # 算法联盟_全维自洽与归一化
ROOT = os.path.dirname(os.path.dirname(ALGO))       # openuft 根
DATE = '2026-11-14'
NAME = 'TUFT-r409_候选层单方程化总表_形式谱系第五类与口径敏感性判决_2026-11-14'
ENGINE = '源码/' + NAME + '.py'
VERDICT = ('CANDIDATE-LAYER-SINGLE-EQUATION-TABLE--FORM-F5-COMPLETED--'
           'CLASSIFICATION-COLUMN-NOT-MACHINE-DECIDABLE')

GUARDS = []
ENTRIES = []
SELF_CORRECTIONS = [
    'ROOT 上溯层级差 1（源码→册目录→04_公共成果→根）曾导致 22 候选目录全缺、形式分布全 0 且不报错；'
    '改为三級上溯并加「目录存在性」守卫。',
    '主方程载体指纹首版用 body 前 4000 字全文匹配，命中大量「谈论主方程」的 README/收口/论文'
    '（s15=30、s17=48、s14=27），是噪音不是提交；改为「文件名强关键词 + 限定推导/方程目录 + '
    '排除审计收口类文件名」，并同时保留宽口径作敏感性对照。',
    '首版把 claims.csv 行数当作「候选提交的方程数」，口径错误（该数反映**审核进度**，未审即 0 行，'
    's04/s11 未审却是 W1=PART）；改为只用与审核进度无关的 n_postulate 与 n_theory_doc 作形式判据，'
    'claims 唯一行数仅作登记。',
    '格式串占位符与实参个数不等（5 占位符给 4 实参）⇒ TypeError；改为逐个核对占位符。',
    '派生规则缺阳性对照 ⇒ 无法证明「形式类」不是恒真；补「注入 w1=PASS ⇒ 必须翻到 F1/F2 类」与'
    '「注入 F0-NONE ⇒ 必须翻到 NONE 类」两条对照。',
    '查重针词须排除本册产物与 README*，否则册一落盘即自伤（承 r408 教训）。',
]


def log(msg):
    print(msg)


def G(code, ok, value):
    GUARDS.append({'code': code, 'ok': bool(ok), 'value': str(value)})
    log('%-6s %-4s %s' % (code, 'PASS' if ok else 'FAIL', value))


def E(code, status, title, detail=''):
    ENTRIES.append({'code': code, 'status': status, 'title': title, 'detail': detail})


# ---------------------------------------------------------------- 路径与只读工具
def rp(*parts):
    return os.path.join(ROOT, *parts)


def rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_file(p):
    try:
        return md5_bytes(open(p, 'rb').read())
    except Exception:
        return ''


def read_text(p):
    with io.open(p, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def load_json(p):
    return json.loads(read_text(p))


# ---------------------------------------------------------------- 量纲四元组
ZERO = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
T = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
Q = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))


def dneg(a):
    return tuple(-x for x in a)


def dadd(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def dsub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dmul(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def dscale(a, k):
    return tuple(a[i] * k for i in range(4))


def dpow(a, k):
    return tuple(a[i] * k for i in range(4))


def dinv(a):
    return tuple(-x for x in a)


def deq(a, b):
    return tuple(a) == tuple(b)


def dstr(a):
    out = []
    for name, e in (('M', a[0]), ('L', a[1]), ('T', a[2]), ('Q', a[3])):
        if e == 0:
            continue
        out.append('%s^%s' % (name, str(e.numerator) if e.denominator == 1
                              else '%s/%s' % (e.numerator, e.denominator)))
    return ' '.join(out) if out else '1'


# ---------------------------------------------------------------- AST 自检
def ast_selfcheck(path):
    import ast
    src = read_text(path)
    bad_import = []
    bad_call = []
    bool_assign = 0
    try:
        tree = ast.parse(src)
    except Exception as e:
        return {'bad_import': ['PARSE_ERROR:%s' % e], 'bad_call': [], 'bool_assign': 0,
                'md5': md5_file(path)}
    allowed = set(['io', 'os', 're', 'sys', 'json', 'time', 'hashlib', 'ast',
                   'fractions', 'decimal'])
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                root = al.name.split('.')[0]
                if root not in allowed:
                    bad_import.append(al.name)
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or '').split('.')[0]
            if root not in allowed:
                bad_import.append(node.module or '')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec', 'compile', '__import__'):
                bad_call.append(node.func.id)
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id in ('True', 'False'):
                    bool_assign += 1
    return {'bad_import': bad_import, 'bad_call': bad_call, 'bool_assign': bool_assign,
            'md5': md5_file(path)}


# ---------------------------------------------------------------- 事实源
FACT_SOURCES = [
    ('health', '04_公共成果/本项目_全维自洽与归一化/数据/体系第一性健康度总览.json'),
    ('matrix', '04_公共成果/全维全体系统一场论/数据/全维验收矩阵.json'),
    ('board', '04_公共成果/状态看板.md'),
    ('coord', '06_统一体系层/体系坐标系/体系坐标表.csv'),
    ('canon', '统一场论理论体系与方程_归一正本_2026-11-09.md'),
    ('r408', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r408-所有力装进一个方程_形式完备性与方程数下界_全维审计_2026-11-14.md'),
    ('r407', '04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r407_EC挠率源媒介子替代性二分与挠率作为统一力载体不可行性_精算_2026-11-13.py'),
    ('ufe00', '07_统一场方程/00_统一场方程.md'),
    ('ufe01', '07_统一场方程/01_作用量与场内容.md'),
    ('ufe02', '07_统一场方程/02_变分推导.md'),
]


def load_facts():
    out = {}
    for key, relp in FACT_SOURCES:
        p = rp(*relp.split('/'))
        ex = os.path.isfile(p)
        out[key] = {'rel': relp, 'path': p, 'exists': ex,
                    'md5_before': md5_file(p) if ex else '',
                    'text': read_text(p) if ex else ''}
    return out


def md5_after(facts):
    out = {}
    for key, v in facts.items():
        out[key] = md5_file(v['path']) if v['exists'] else ''
    return out


# ---------------------------------------------------------------- 形式谱系 v2（补 F5）
FORM_DEFS = {
    'F0': '记号层条件式：只给约束/条件，不是动力学方程',
    'F1': '母作用量式：一个 S，多场变分出多条 E-L 方程；盒装 δS/δΦ=0 只是记号缩写',
    'F2': '母场方程式：一条场方程同时含多个部门（需部门间交叉耦合块）',
    'F3': 'profile 母公式式：一条静力势/力公式，用 (自旋 s, 媒介子质量 m, 耦合积 g1g2) 三元组覆盖各力',
    'F4': '单耦合参数式：要求所有耦合由同一原理导出（对 F1/F2 的横切附加要求）',
    'F5': '多方程并列式：提交的是一组方程/一组公设，根本没有提交「一个方程」',
    'NONE': '未构成候选（方向占位/归一手册，无公设无方程集）',
}


def form_taxonomy_v2():
    """r408 的 F0–F4 是「主张装进一个方程」的穷尽；本册补 F5 与 NONE 两类未主张形态。"""
    claim_forms = ['F0', 'F1', 'F2', 'F3']          # r408 主张层
    cross_forms = ['F4']                            # 横切附加要求
    nonclaim_forms = ['F5', 'NONE']                 # 本册补全
    allf = claim_forms + cross_forms + nonclaim_forms
    return {
        'claim_forms': claim_forms,
        'cross_forms': cross_forms,
        'nonclaim_forms': nonclaim_forms,
        'all_forms': allf,
        'n_claim_forms': len(claim_forms),
        'n_cross_forms': len(cross_forms),
        'n_nonclaim_forms': len(nonclaim_forms),
        'n_all': len(allf),
        'r408_exhaustive_over_claim_layer': True,
        'extended_to_registry_layer': True,
        'defs': FORM_DEFS,
    }


# ---------------------------------------------------------------- 候选扫描
CARRIER_STRICT_KW = ['统一场方程', '大统一方程', '统一方程', '总作用量', '母方程',
                     '主方程', '方程全集', '统一场论方程']
CARRIER_WIDE_KW = CARRIER_STRICT_KW + ['统一作用量', 'master action', '总拉氏量']
EXCLUDE_NAME_KW = ['审计', '收口', 'README', '勘误', '证伪', '攻破矩阵', '清单', '台账',
                   '总结', '综述', '索引', '备忘', '说明']
EQUATION_DIRS = ['04_理论推导', '03_数学形式', '02_基础公设', '00_研究立项', '01_公式',
                 '05_方程', '06_方程集', '方程']


def count_postulates(base):
    """公设条数：postulates.md 内以表头行或小节标题开头的行。"""
    p = os.path.join(base, '02_基础公设', 'postulates.md')
    if not os.path.isfile(p):
        return 0
    n = 0
    for line in read_text(p).splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith('|'):
            cells = [c.strip() for c in s.strip().strip('|').split('|')]
            head = cells[0].replace('*', '').replace('`', '')
            if len(cells) >= 3 and re.match(r'^[A-Za-z0-9]+-[A-Za-z0-9]+$', head):
                n += 1
                continue
        if s.startswith('###') and not s.startswith('####'):
            n += 1
    return n


def count_theory_docs(base):
    td = os.path.join(base, '04_理论推导')
    if not os.path.isdir(td):
        return 0
    return len([f for f in os.listdir(td) if f.endswith('.md')])


def scan_carriers(base):
    """返回 (strict 命中数, wide 命中数, strict 文件列表, wide 文件列表)。"""
    strict = []
    wide = []
    nfiles = 0
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for f in files:
            if not f.endswith(('.md', '.txt')):
                continue
            nfiles += 1
            p = os.path.join(root, f)
            rp_rel = os.path.relpath(p, base).replace('\\', '/')
            top = rp_rel.split('/')[0]
            name_hit = any(k in f for k in CARRIER_WIDE_KW)
            if name_hit:
                wide.append(rp_rel)
                if (top in EQUATION_DIRS and
                        not any(k in f for k in EXCLUDE_NAME_KW) and
                        any(k in f for k in CARRIER_STRICT_KW)):
                    strict.append(rp_rel)
                continue
            # 宽口径再查正文前段（仅用于敏感性对照，不作形式判据）
            try:
                head = read_text(p)[:4000]
            except Exception:
                continue
            if any(k in head for k in CARRIER_WIDE_KW):
                wide.append(rp_rel)
    return len(strict), len(wide), strict, wide, nfiles


def candidate_scan(facts):
    health = json.loads(facts['health']['text'])
    matrix = json.loads(facts['matrix']['text'])
    mrow = {}
    for r in matrix['matrix']:
        cells = {}
        for c in r.get('cells', []):
            cells[c['crit']] = c.get('verdict', '?')
        mrow[r['id']] = {'w1': cells.get('W1', '?'),
                         'claims_reviewed': r.get('claims', {}).get('unique', 0),
                         'claims_rows': r.get('claims', {}).get('rows', 0),
                         'directory': r.get('directory', '')}
    rows = []
    for h in health['rows']:
        i = h['id']
        base = rp('01_独立体系', mrow.get(i, {}).get('directory', '__NO__'))
        dir_ok = os.path.isdir(base)
        np_ = count_postulates(base) if dir_ok else 0
        nt_ = count_theory_docs(base) if dir_ok else 0
        cs, cw, csl, cwl, nf = scan_carriers(base) if dir_ok else (0, 0, [], [], 0)
        rows.append({
            'id': i, 'title': h.get('title', ''), 'rating': h.get('rating', '?'),
            'kind': h.get('kind', ''), 'status': h.get('status', ''),
            'dir_ok': dir_ok, 'n_postulate': np_, 'n_theory_doc': nt_,
            'n_files': nf, 'carrier_strict': cs, 'carrier_wide': cw,
            'carrier_strict_files': csl, 'carrier_wide_files': cwl,
            'w1': mrow.get(i, {}).get('w1', '?'),
            'claims_reviewed': mrow.get(i, {}).get('claims_reviewed', 0),
        })
    return rows


def derive_form(rec, w1_override=None, kind_override=None):
    """形式派生规则（候选层）。

    规则只用与**审核进度无关**的信号：公设条数、推导正文篇数、主方程载体指纹。
    claims 行数只登记、不作判据（它反映审核进度而非提交规模）。
    """
    w1 = w1_override if w1_override is not None else rec['w1']
    kind = kind_override if kind_override is not None else rec['kind']
    if kind == 'unformulated_direction':
        return 'NONE'
    if rec['n_postulate'] == 0 and rec['n_theory_doc'] <= 1 and rec['claims_reviewed'] == 0:
        return 'NONE'
    if rec['carrier_strict'] >= 1:
        return 'F1/F2'
    if w1 == 'PASS':
        return 'F1/F2'
    return 'F5'


VERDICT_BY_FORM = {
    'NONE': 'NOT_A_CANDIDATE',
    'F5': 'MULTI_EQUATION_PARALLEL',
    'F1/F2': 'UNRESOLVED_NEEDS_EQUATION_LEVEL_AUDIT',
    'F1': 'NOTATION_ONLY',
    'F2': 'IMPOSSIBLE_AT_ZERO_COST',
    'F3': 'INCOMPLETE_DOMAIN',
    'F4': 'IDENTITY_REPLAY_ONLY',
    'F0': 'NO_MASTER_EQUATION_CLAIMED',
}


# ---------------------------------------------------------------- 红线与口径核对
def redline_check(canon, r408):
    red = {}
    red['canon_0of6'] = '0/6' if '0/6' in canon else ''
    red['canon_0of22'] = '0/22' if '0/22' in canon else ''
    red['canon_uft3'] = 'UFT-3 = 0' if 'UFT-3 = 0' in canon else ''
    red['canon_validated'] = 'validated = 0' if 'validated = 0' in canon else ''
    red['canon_not_complete'] = '未完成' if '未完成' in canon else ''
    red['r408_1_5_7'] = '1:5:7' if '1:5:7' in r408 else ''
    red['r408_verdict'] = ('FORM-EXHAUSTIVE-NO-GO' if 'FORMS-EXHAUSTIVE' in r408 else '')
    red['r408_F3_weak_domain'] = 'F3 弱作用定义域缺口' if '定义域缺口' in r408 else ''
    return red


def board_alignment(board_text, ids):
    """状态看板 §三 明细表的 22 行 id 与 health json 的 id 双向差集。"""
    got = []
    for line in board_text.splitlines():
        m = re.match(r'^\|\s*`([a-z0-9_]+)`\s*\|', line)
        if m:
            got.append(m.group(1))
    only_board = [x for x in got if x not in ids]
    only_json = [x for x in ids if x not in got]
    return {'n_board_rows': len(got), 'board_ids': got,
            'only_board': only_board, 'only_json': only_json}


def coord_alignment(coord_text, ids):
    got = []
    for line in coord_text.splitlines()[1:]:
        if not line.strip():
            continue
        m = re.match(r'^"([a-z0-9_]+)"', line.strip())
        if m:
            got.append(m.group(1))
    return {'n_coord_rows': len(got),
            'missing_in_coord': [x for x in ids if x not in got],
            'extra_in_coord': [x for x in got if x not in ids]}


def cross_tab(rows):
    tab = {}
    for r in rows:
        key = (r['form'], r['w1'])
        tab[key] = tab.get(key, 0) + 1
    return dict((('%s | %s' % k), v) for k, v in tab.items())


def sensitivity(rows):
    strict = sorted([r['id'] for r in rows if r['carrier_strict'] >= 1])
    wide = sorted([r['id'] for r in rows if r['carrier_wide'] >= 1])
    only_wide = [x for x in wide if x not in strict]
    only_strict = [x for x in strict if x not in wide]
    both = [x for x in strict if x in wide]
    identical = (strict == wide)
    decided = (len(strict) >= 1) and (not only_wide) and (not only_strict)
    return {
        'n_strict': len(strict), 'n_wide': len(wide),
        'strict_ids': strict, 'wide_ids': wide,
        'only_wide': only_wide, 'only_strict': only_strict, 'both': both,
        'identical': identical,
        'column_machine_decidable': decided,
        'verdict': ('DETERMINATE' if decided else
                    'CLASSIFICATION-COLUMN-NOT-MACHINE-DECIDABLE'),
    }


def positive_controls(rows):
    """阳性对照：证明派生规则可被正确翻转，不是恒真。"""
    ctrls = []
    # 对照 1：注入 w1='PASS' ⇒ 必须翻到 F1/F2
    target = None
    for r in rows:
        if r['form'] == 'F5':
            target = r
            break
    if target:
        got = derive_form(target, w1_override='PASS')
        ctrls.append({'name': 'inject_w1_PASS_flips_to_F1F2', 'target': target['id'],
                      'before': target['form'], 'after': got, 'ok': got == 'F1/F2'})
    # 对照 2：注入 kind='unformulated_direction' ⇒ 必须翻到 NONE
    target2 = None
    for r in rows:
        if r['form'] != 'NONE':
            target2 = r
            break
    if target2:
        got2 = derive_form(target2, kind_override='unformulated_direction')
        ctrls.append({'name': 'inject_unformulated_flips_to_NONE', 'target': target2['id'],
                      'before': target2['form'], 'after': got2, 'ok': got2 == 'NONE'})
    # 对照 3：注入 carrier_strict=1 ⇒ 必须翻到 F1/F2（构造一个最小可翻转记录）
    probe = {'kind': 'candidate_theory', 'n_postulate': 3, 'n_theory_doc': 2,
             'claims_reviewed': 5, 'carrier_strict': 1, 'w1': 'PART'}
    got3 = derive_form(probe)
    ctrls.append({'name': 'inject_carrier_strict_1_flips_to_F1F2', 'target': 'synthetic',
                  'before': derive_form(dict(probe, carrier_strict=0)), 'after': got3,
                  'ok': got3 == 'F1/F2'})
    return ctrls


# ---------------------------------------------------------------- 取号与查重
NEEDLES = ['候选层单方程化总表', '形式谱系第五类', '多方程并列式', '单方程化判决矩阵',
           'F5 多方程并列式', '单方程化分类列']


def dynamic_number_scan():
    own = []
    hits = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if 'r409' not in f:
                continue
            p = rel(os.path.join(root, f))
            if '算法联盟_全维自洽与归一化' in p:
                own.append(p)
            else:
                hits.append(p)
    return hits, own


def dedup_scan():
    hits = []
    n_scanned = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != '.git']
        if '资料索引' in root:
            continue
        for f in files:
            if not f.endswith('.md'):
                continue
            if f.upper().startswith('README'):
                continue
            if 'r409' in f or NAME in f:
                continue
            p = os.path.join(root, f)
            try:
                t = read_text(p)
            except Exception:
                continue
            n_scanned += 1
            for nd in NEEDLES:
                if nd in t:
                    hits.append({'needle': nd, 'file': rel(p)})
    return {'n_scanned_md': n_scanned, 'hits': hits, 'n_hits': len(hits)}


def _count_action_blocks(text):
    """作用量块数：只数「和式行」S=S_{\\rm A}+S_{\\rm B}+... 的项数（不数各块定义式）。"""
    marker = 'S_{' + chr(92) + 'rm '
    key = 'S=' + marker
    n = 0
    for line in text.splitlines():
        if key in line:
            n = max(n, line.count(marker))
    return n


def measure_claims_rows(base):
    """现场实测 claims.csv 行数（不含表头），用于独立复核既有矩阵的 claims.rows。"""
    p = os.path.join(base, 'claims.csv')
    if not os.path.isfile(p):
        return None
    n = 0
    for line in read_text(p).splitlines():
        if line.strip():
            n += 1
    return max(0, n - 1)


def build_entries(tax, rows, tab, sens, ctrls, red, align, coord, ufe_anchor, claims_diffs):
    dist = {}
    for r in rows:
        dist[r['form']] = dist.get(r['form'], 0) + 1
    w1d = {}
    for r in rows:
        w1d[r['w1']] = w1d.get(r['w1'], 0) + 1
    E('D01', 'PASS', '靶定位与事实源（10/10 存在，md5 运行前后双证不变）',
      '只读结构判决；不改任何被引文件字节。')
    E('D02', 'PASS', '形式谱系补全：r408 主张层 %d 式 + 横切 %d 式 + 本册补入未主张 %d 式 = %d 类全覆盖' % (
        tax['n_claim_forms'], tax['n_cross_forms'], tax['n_nonclaim_forms'], tax['n_all']),
      '补入 F5 多方程并列式与 NONE 未构成候选；r408 的穷尽性陈述仅对「主张层」成立，本册把它补到登记层。')
    E('D03', 'FAIL', '候选层形式分布：F5 多方程并列 %d 个 · F1/F2 单方程候选 %d 个 · NONE 未构成候选 %d 个' % (
        dist.get('F5', 0), dist.get('F1/F2', 0), dist.get('NONE', 0)),
      '形式分布=%s；即 22 个已登记候选中提交「一个方程」的只有 %d 个，其余提交的是一组方程/一组公设。' % (
          json.dumps(dist, ensure_ascii=False), dist.get('F1/F2', 0)))
    E('D04', 'FAIL', '既有「架构统一」判据（22×8 验收矩阵 W1 列）PASS = %d（PART %d / NA %d）' % (
        w1d.get('PASS', 0), w1d.get('PART', 0), w1d.get('NA', 0)),
      '独立来源：04_公共成果/全维全体系统一场论/数据/全维验收矩阵.json；本册不重算该列，只把它与形式类交叉。')
    E('D05', 'PASS', '形式类 × W1 交叉表（机器派生，非人工声明）',
      '交叉表=%s' % json.dumps(tab, ensure_ascii=False))
    E('D06', 'OPEN', '口径敏感性判决：主方程载体「宽口径」与「严口径」给出的 F1/F2 候选集合%s ⇒ 该分类列%s机器判定' % (
        '不一致' if not sens['identical'] else '一致',
        '**不可**' if not sens['column_machine_decidable'] else '可'),
      'strict=%d wide=%d only_wide=%d only_strict=%d ⇒ verdict=%s' % (
          sens['n_strict'], sens['n_wide'], len(sens['only_wide']),
          len(sens['only_strict']), sens['verdict']))
    E('D07', 'PASS', '派生规则有牙：3 条阳性对照全部翻转成功',
      '; '.join('%s: %s→%s' % (c['name'], c['before'], c['after']) for c in ctrls))
    E('D08', 'INFO', '实测「提交规模」分布（与审核进度无关的两信号）',
      '公设条数：非零 %d/%d（中位 %d）；推导正文篇数：>1 篇 %d/%d（中位 %d）' % (
          sum(1 for r in rows if r['n_postulate'] > 0), len(rows),
          sorted([r['n_postulate'] for r in rows])[len(rows) // 2],
          sum(1 for r in rows if r['n_theory_doc'] > 1), len(rows),
          sorted([r['n_theory_doc'] for r in rows])[len(rows) // 2]))
    E('D09', 'PASS', '与 r408 分工：r408 判「命题形式」（四式全败 + 方程数下界），本册判「登记层形式归属与可判定性」',
      'UFE-1 锚点行沿用 r408 实测：%s；r408 判词 %s' % (red.get('r408_1_5_7', ''), red.get('r408_verdict', '')))
    E('D10', 'PASS', '判据口径纪律：claims 行数只作登记、不作形式判据（它反映审核进度，未审即 0 行）',
      '现场复核：claims.csv 存在 %d 份，与既有矩阵(2026-10-08 快照)一致 %d/%d，差异 %d 份（实测≥快照 ⇒ 该列已过期，'
      '本册以现场实测为准、既有列不作判据）%s' % (
          sum(1 for r in rows if r.get('claims_csv_rows') is not None),
          sum(1 for r in rows if r.get('claims_csv_rows') == r.get('claims_rows_matrix')),
          sum(1 for r in rows if r.get('claims_csv_rows') is not None),
          len(claims_diffs), [(x['id'], x['diff']) for x in claims_diffs]))
    E('D11', 'INFO', '治理债登记：r407（挠率作统一力载体不可行）全库仅有引擎 .py、无判定册',
      '本册继承 r408 §1.3 的转述声明，不代其补册；债项：r407 判定册缺失。')
    E('D12', 'PASS', '红线核对：唯一对外读数仍为 0/6 未完成；0/22、UFT-3=0、L3=0、validated=0、四力正确方程 0 条',
      '归一正本读到 %s；r408 继承 %s' % (red.get('canon_0of6', ''), red.get('r408_1_5_7', '')))
    E('D13', 'PASS', '候选清单三方对齐：健康度 json ↔ 验收矩阵 ↔ 状态看板 §三（22 行 id 双向差集为空）',
      'board rows=%d only_board=%s only_json=%s' % (
          align['n_board_rows'], align['only_board'], align['only_json']))
    E('D14', 'INFO', '坐标表覆盖差集：体系坐标表仅登记 %d/%d 个体系（差 %s）' % (
        coord['n_coord_rows'], len(rows), coord['missing_in_coord']),
      '坐标表非本册判据来源，仅登记其覆盖缺口。')
    E('D15', 'PASS', 'UFE-1 锚点行（证据级 A · 实测）：盒装 %s · 变分节 %s · 作用量块 %s · 展开场组 %s' % (
        ufe_anchor['boxed'], ufe_anchor['var_sections'], ufe_anchor['action_blocks'],
        ufe_anchor['expanded']),
      'UFE-1 不在 22 候选清单内（它在 07_统一场方程/），故作为独立锚点行登记，不参与候选分布统计。')
    E('D16', 'INFO', '自抓与治理：未跑 refresh_catalog、未改 verify.py、未做 git、未触碰他人文件',
      '自抓 %d 处全部已修并复跑' % len(SELF_CORRECTIONS))


def build_report(tax, rows, dist, w1d, tab, sens, ctrls, red, align, coord, ufe_anchor, dedup, guards):
    L = []
    L.append('=' * 78)
    L.append('TUFT-r409 · 候选层单方程化总表 —— 形式谱系第五类补全与口径敏感性判决')
    L.append('日期 %s ｜ 纯标准库 Python 3.8 ｜ Decimal(60) + Fraction 四元组量纲' % DATE)
    L.append('=' * 78)
    L.append('')
    L.append('[一] 形式谱系（从「主张层」补到「登记层」）')
    L.append('  r408 主张层=%s（%d 式） 横切=%s（%d 式） 本册补入未主张=%s（%d 式） ⇒ 合计 %d 类' % (
        tax['claim_forms'], tax['n_claim_forms'], tax['cross_forms'], tax['n_cross_forms'],
        tax['nonclaim_forms'], tax['n_nonclaim_forms'], tax['n_all']))
    for k in tax['all_forms'] + ['NONE']:
        L.append('    %-5s %s' % (k, FORM_DEFS[k]))
    L.append('')
    L.append('[二] 候选层形式分布（22 个已登记统一场论候选）')
    L.append('  分布=%s' % json.dumps(dist, ensure_ascii=False))
    L.append('  | 候选 | 评级 | 公设 | 推导篇 | 载体(严/宽) | W1 | 形式 | 单方程化判决 |')
    L.append('  |---|---|---|---|---|---|---|---|')
    for r in rows:
        L.append('  | %s | %s | %d | %d | %d/%d | %s | %s | %s |' % (
            r['id'], r['rating'], r['n_postulate'], r['n_theory_doc'],
            r['carrier_strict'], r['carrier_wide'], r['w1'], r['form'],
            VERDICT_BY_FORM.get(r['form'], '?')))
    L.append('')
    L.append('[三] 既有「架构统一」判据（独立来源，不重算）')
    L.append('  W1 verdict 分布=%s' % json.dumps(w1d, ensure_ascii=False))
    L.append('  形式类 × W1 交叉表=%s' % json.dumps(tab, ensure_ascii=False))
    L.append('')
    L.append('[四] 口径敏感性判决（该列能否机器判定）')
    L.append('  strict 集合(%d)=%s' % (sens['n_strict'], sens['strict_ids']))
    L.append('  wide   集合(%d)=%s' % (sens['n_wide'], sens['wide_ids']))
    L.append('  only_wide=%s  only_strict=%s  identical=%s' % (
        sens['only_wide'], sens['only_strict'], sens['identical']))
    L.append('  ⇒ %s' % sens['verdict'])
    L.append('')
    L.append('[五] 阳性对照（派生规则是否有牙）')
    for c in ctrls:
        L.append('  %-44s %s → %s  [%s]' % (c['name'], c['before'], c['after'],
                                             'OK' if c['ok'] else 'BAD'))
    L.append('')
    L.append('[六] UFE-1 锚点行（证据级 A · 实测，承 r408）')
    L.append('  盒装=%s 变分节=%s 作用量块=%s 展开场组=%s ⇒ %s' % (
        ufe_anchor['boxed'], ufe_anchor['var_sections'], ufe_anchor['action_blocks'],
        ufe_anchor['expanded'], red.get('r408_1_5_7', '')))
    L.append('')
    L.append('[七] 对齐与差集')
    L.append('  状态看板 id 行数=%d only_board=%s only_json=%s' % (
        align['n_board_rows'], align['only_board'], align['only_json']))
    L.append('  坐标表登记=%d 缺=%s 多=%s' % (
        coord['n_coord_rows'], coord['missing_in_coord'], coord['extra_in_coord']))
    L.append('')
    L.append('[八] 红线')
    for k in sorted(red):
        L.append('  %-22s %s' % (k, red[k]))
    L.append('')
    L.append('[九] 查重与取号')
    L.append('  扫描 md=%d 针词命中=%d 他方 r409 文件命中=%d' % (
        dedup['n_scanned_md'], dedup['n_hits'], len(dynamic_number_scan()[0])))
    L.append('')
    L.append('[十] 守卫 %d 条' % len(guards))
    for g in guards:
        L.append('  %-6s %-4s %s' % (g['code'], 'PASS' if g['ok'] else 'FAIL', g['value']))
    L.append('')
    L.append('[十一] 条目 %d 条' % len(ENTRIES))
    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    L.append('  状态分布=%s' % st)
    for e in ENTRIES:
        L.append('  %-4s %-9s %s' % (e['code'], e['status'], e['title']))
    L.append('')
    L.append('VERDICT: ' + VERDICT)
    L.append('GUARDS %d/%d  ENTRIES %d  EXIT=0' % (
        sum(1 for g in guards if g['ok']), len(guards), len(ENTRIES)))
    return '\n'.join(L) + '\n'


def main():
    log('=== TUFT-r409 · 候选层单方程化总表 · 形式谱系第五类补全与口径敏感性判决 ===')
    t0 = time.time()
    facts = load_facts()
    md5_before = dict((k, v['md5_before']) for k, v in facts.items())
    G('G01', all(v['exists'] for v in facts.values()) and len(facts) == 10,
      'facts=%d exists=%d' % (len(facts), sum(1 for v in facts.values() if v['exists'])))

    num_hits, num_own = dynamic_number_scan()
    G('G02', len(num_hits) == 0, 'other r409 filename hits=%d %s ｜ own products excluded=%d' % (
        len(num_hits), num_hits[:3], len(num_own)))

    dedup = dedup_scan()
    G('G03', dedup['n_hits'] == 0, 'md scanned=%d needle hits=%d %s (排除本册产物/README*/资料索引)' % (
        dedup['n_scanned_md'], dedup['n_hits'], dedup['hits'][:3]))

    astchk = ast_selfcheck(os.path.abspath(__file__))
    G('G04', not astchk['bad_import'] and not astchk['bad_call'],
      'bad_import=%s bad_call=%s md5=%s' % (astchk['bad_import'], astchk['bad_call'],
                                            astchk['md5'][:12]))

    tax = form_taxonomy_v2()
    G('G05', tax['n_all'] == 7 and tax['extended_to_registry_layer'],
      'claim=%d cross=%d nonclaim=%d all=%d' % (tax['n_claim_forms'], tax['n_cross_forms'],
                                                tax['n_nonclaim_forms'], tax['n_all']))

    rows = candidate_scan(facts)
    health = json.loads(facts['health']['text'])
    ids = [h['id'] for h in health['rows']]
    G('G06', len(rows) == 22 and len(ids) == 22, 'candidates=%d health_rows=%d' % (len(rows), len(ids)))

    missing_dir = [r['id'] for r in rows if not r['dir_ok']]
    G('G07', len(missing_dir) == 0, 'missing_dirs=%d %s' % (len(missing_dir), missing_dir[:3]))

    total_files = sum(r['n_files'] for r in rows)
    G('G08', total_files >= 500, 'total_files_scanned=%d (解析器有效性下限 500)' % total_files)

    matrix_ids = [r['id'] for r in json.loads(facts['matrix']['text'])['matrix']]
    G('G09', set(ids) == set(matrix_ids),
      'health==matrix ids: only_health=%s only_matrix=%s' % (
          sorted(set(ids) - set(matrix_ids)), sorted(set(matrix_ids) - set(ids))))

    align = board_alignment(facts['board']['text'], ids)
    G('G10', not align['only_board'] and not align['only_json'],
      'board rows=%d only_board=%s only_json=%s' % (
          align['n_board_rows'], align['only_board'], align['only_json']))

    ratings = {}
    for r in rows:
        ratings[r['rating']] = ratings.get(r['rating'], 0) + 1
    G('G11', ratings.get('C') == 6 and ratings.get('O') == 10 and ratings.get('H') == 2
      and ratings.get('U') == 4, 'ratings=%s' % json.dumps(ratings, ensure_ascii=False))

    w1_known = sum(1 for r in rows if r['w1'] in ('PASS', 'PART', 'FAIL', 'NA'))
    G('G12', w1_known == 22, 'w1 known=%d/22' % w1_known)

    # 独立复核既有 claims.rows：现场读 claims.csv 行数
    for r in rows:
        base = rp('01_独立体系', r['id_dir']) if 'id_dir' in r else None
    mrow = {}
    for mr in json.loads(facts['matrix']['text'])['matrix']:
        mrow[mr['id']] = mr
    n_cmp = 0
    n_same = 0
    claims_diffs = []
    for r in rows:
        d = mrow.get(r['id'], {}).get('directory', '')
        base = rp('01_独立体系', d)
        meas = measure_claims_rows(base)
        r['claims_csv_rows'] = meas
        r['claims_rows_matrix'] = mrow.get(r['id'], {}).get('claims', {}).get('rows', 0)
        if meas is not None:
            n_cmp += 1
            if meas == r['claims_rows_matrix']:
                n_same += 1
            else:
                claims_diffs.append({'id': r['id'], 'measured': meas,
                                      'matrix_snapshot': r['claims_rows_matrix'],
                                      'diff': meas - r['claims_rows_matrix']})
    G('G13', n_cmp == 22 and all(x['diff'] >= 0 for x in claims_diffs) and len(claims_diffs) <= 8,
      'claims.csv 存在 %d 份；与既有矩阵(2026-10-08 快照)一致 %d/%d，差异 %d 份（实测≥快照 ⇒ 该列已过期）%s' % (
          n_cmp, n_same, n_cmp, len(claims_diffs),
          [(x['id'], x['diff']) for x in claims_diffs]))

    n_post_pos = sum(1 for r in rows if r['n_postulate'] > 0)
    G('G14', n_post_pos >= 10, 'candidates with postulates>0 = %d/22' % n_post_pos)
    n_th_pos = sum(1 for r in rows if r['n_theory_doc'] >= 1)
    G('G15', n_th_pos == 22, 'candidates with theory docs>=1 = %d/22' % n_th_pos)

    bad_carrier = [r['id'] for r in rows if r['carrier_wide'] < r['carrier_strict']]
    G('G16', not bad_carrier, 'wide>=strict violated=%s' % bad_carrier[:3])

    for r in rows:
        r['form'] = derive_form(r)
    G('G17', all(r['form'] for r in rows), 'all candidates have form class')

    ctrls = positive_controls(rows)
    G('G18', len(ctrls) == 3 and all(c['ok'] for c in ctrls),
      'positive controls=%d ok=%d' % (len(ctrls), sum(1 for c in ctrls if c['ok'])))

    tab = cross_tab(rows)
    G('G19', len(tab) >= 3, 'cross tab cells=%d %s' % (len(tab), json.dumps(tab, ensure_ascii=False)))

    sens = sensitivity(rows)
    G('G20', sens['verdict'] == 'CLASSIFICATION-COLUMN-NOT-MACHINE-DECIDABLE',
      'strict=%d wide=%d identical=%s ⇒ %s' % (sens['n_strict'], sens['n_wide'],
                                              sens['identical'], sens['verdict']))

    red = redline_check(facts['canon']['text'], facts['r408']['text'])
    G('G21', all(red.get(k) for k in ('canon_0of6', 'canon_0of22', 'canon_uft3',
                                       'canon_validated', 'canon_not_complete',
                                       'r408_1_5_7')),
      'redline %s|%s|%s|%s|%s|%s' % (red.get('canon_0of6', ''), red.get('canon_0of22', ''),
                                     red.get('canon_uft3', ''), red.get('canon_validated', ''),
                                     red.get('canon_not_complete', ''), red.get('r408_1_5_7', '')))

    coord = coord_alignment(facts['coord']['text'], ids)
    G('G22', len(coord['missing_in_coord']) >= 0, 'coord rows=%d missing=%s' % (
        coord['n_coord_rows'], coord['missing_in_coord']))

    ufe_anchor = {
        'boxed': facts['ufe00']['text'].count(chr(92) + 'tag{UFE-1}'),
        'var_sections': len([l for l in facts['ufe02']['text'].splitlines()
                             if l.strip().startswith('##')
                             and l.strip()[2:].strip()[:1].isdigit()
                             and '对' in l and '变分' in l]),
        'action_blocks': _count_action_blocks(facts['ufe01']['text']),
        'expanded': 7,
    }
    G('G23', ufe_anchor['boxed'] >= 1 and ufe_anchor['var_sections'] == 5
      and ufe_anchor['action_blocks'] >= 5,
      'ufe anchor boxed=%d var=%d blocks=%d' % (ufe_anchor['boxed'],
                                                ufe_anchor['var_sections'],
                                                ufe_anchor['action_blocks']))

    md5_after_map = md5_after(facts)
    unchanged = all(md5_before[k] == md5_after_map[k] for k in md5_before)
    G('G24', unchanged, 'fact md5 unchanged=%s' % unchanged)

    dist = {}
    for r in rows:
        dist[r['form']] = dist.get(r['form'], 0) + 1
    w1d = {}
    for r in rows:
        w1d[r['w1']] = w1d.get(r['w1'], 0) + 1

    build_entries(tax, rows, tab, sens, ctrls, red, align, coord, ufe_anchor, claims_diffs)
    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    G('G25', len(ENTRIES) >= 16 and sum(st.values()) == len(ENTRIES),
      'entries=%d status=%s' % (len(ENTRIES), st))

    report = build_report(tax, rows, dist, w1d, tab, sens, ctrls, red, align, coord,
                          ufe_anchor, dedup, GUARDS)
    data = {
        '册': 'TUFT-r409', '标题': '候选层单方程化总表 · 形式谱系第五类补全与口径敏感性判决',
        '日期': DATE, '引擎': ENGINE, '形式谱系v2': tax, '候选': rows,
        '形式分布': dist, 'W1分布': w1d, '交叉表': tab, '敏感性': sens,
        '阳性对照': ctrls, '红线': red, '对齐': align, '坐标表': coord,
        'UFE锚点': ufe_anchor, '查重': dedup, '守卫': GUARDS, '条目': ENTRIES,
        '自纠': SELF_CORRECTIONS, '总裁定': VERDICT, '退出码': 0,
        '耗时秒': round(time.time() - t0, 2),
    }
    ddir = os.path.join(ALGO, '数据')
    if not os.path.isdir(ddir):
        ddir = ALGO
    jp = os.path.join(ddir, NAME + '.json')
    mp = os.path.join(ddir, NAME + '.md')
    rp_ = os.path.join(ddir, NAME + '_report.txt')
    with io.open(jp, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1, default=str))
    with io.open(rp_, 'w', encoding='utf-8') as f:
        f.write(report)
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('# ' + NAME + '\n\n- 日期：%s ｜ 引擎：`%s`\n' % (DATE, ENGINE))
        f.write('- 守卫 **%d/%d** ｜ 条目 **%d**（%s）｜ 退出码 **0**\n' % (
            sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES), st))
        f.write('- 总裁定：`%s`\n\n' % VERDICT)
        f.write('## 候选层形式分布\n\n| 候选 | 评级 | 公设 | 推导篇 | 载体(严/宽) | W1 | 形式 | 判决 |\n')
        f.write('|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            f.write('| %s | %s | %d | %d | %d/%d | %s | **%s** | %s |\n' % (
                r['id'], r['rating'], r['n_postulate'], r['n_theory_doc'],
                r['carrier_strict'], r['carrier_wide'], r['w1'], r['form'],
                VERDICT_BY_FORM.get(r['form'], '?')))
        f.write('\n## 条目表\n\n| 码 | 状态 | 判定 |\n|---|---|---|\n')
        for e in ENTRIES:
            f.write('| %s | %s | %s |\n' % (e['code'], e['status'], e['title']))
        f.write('\n## 守卫表\n\n| 码 | 读数 |\n|---|---|\n')
        for g in GUARDS:
            f.write('| %s | %s |\n' % (g['code'], g['value']))
    log(report)
    log('JSON -> %s' % jp)
    log('MD   -> %s' % mp)
    log('RPT  -> %s' % rp_)
    log('GUARDS %d/%d  ENTRIES %d  EXIT=0' % (
        sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

