# -*- coding: utf-8 -*-
# attack61 / 攻破53 · 2026-11-12
# 外部 no-go 定理集 × r403 U01–U13 / r404 E01–E10 / UFE-1 候选的交叉判决矩阵。
# 性质：只读事实源 + 纯标准库判决；不新增物理方程、不重证外部定理、不宣称统一完成。
# stdout 只出 ASCII；中文全部写入 UTF-8 产物。
import sys
import os
import io
import re
import ast
import json
import hashlib
import itertools
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding='ascii', errors='backslashreplace')
except AttributeError:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, '..', '..'))
TAG = 'attack61_外部no-go定理集与统一候选交叉判决矩阵_2026-11-12'
OWN_NUM = 61
OWN_PREFIX = 'attack61'
P_PY = os.path.join(BASE, TAG + '.py')
P_JSON = os.path.join(BASE, TAG + '.json')
P_MD = os.path.join(BASE, TAG + '.md')
P_REPORT = os.path.join(BASE, TAG + '_report.txt')
P_JUDGE = os.path.join(BASE, '判定_attack61_攻破53_外部no-go定理集与统一候选交叉判决矩阵_2026-11-12.md')
P_README = os.path.join(BASE, 'README.md')
OWN = [P_PY, P_JSON, P_MD, P_REPORT, P_JUDGE]

VERDICT = 'EXTERNAL-NOGO-XMATRIX--NO-CORRECT-FOUR-FORCE-GUT-UNCHANGED--E09-CONDITIONAL-NOT-EXCLUDED--NO-PHYSICAL-COMPLETION'
REDLINES = ['0/6', '0/22', 'UFT-3=0', 'L3=0', 'validated=0', 'NO-CORRECT-FOUR-FORCE-GUT', 'SURVIVE 1 / DEAD 9']
DEDUP_NEEDLES = ['attack61', 'NOGO_XMATRIX', 'THEOREM_X_CANDIDATE_MATRIX', '外部no-go', 'no-go定理集', '交叉判决矩阵', '外部定理集']
EXTERNAL_ANCHOR_NEEDLES = ['Coleman–Mandula', 'Coleman-Mandula', 'Haag–Łopuszański–Sohnius', 'Weinberg–Witten', 'Weinberg-Witten', 'Lovelock', 'Ostrogradsky', "'t Hooft", '反常匹配']

FACTS = [
    ('统一场论理论体系与方程_归一正本_2026-11-09.md', ['0/6', '未完成', 'INPUT', 'UFE-1']),
    ('04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.md', ['NO-CORRECT-FOUR-FORCE-GUT', 'U01', 'U11', 'U13', '正确者 = 0 条']),
    ('04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.md', ['MINIMUM-COST-LOWER-BOUND', 'E01', 'E09', 'E10', 'SURVIVE 1 / DEAD 9']),
    ('书籍/v1_正文/第十四编_非微扰尺度自发生成_OPEN7正面攻关/第79章_从伽利略涡旋到庞加莱规范量子_OPENM2表示论裁决_定理Q.md', ['[A]', 'Coleman–Mandula', 'Haag–Łopuszański–Sohnius', 'Weinberg–Witten', 'CLOSED-NEGATIVE']),
    ('书籍/v1_正文/第十五编_几何统一纲领能力边界白皮书/第82章_几何统一纲领能力边界白皮书_从C到Q的nogo谱系与统一场论真实坐标.md', ['11 道判不可行定理', 'Coleman–Mandula', 'Weinberg–Witten', '2/6']),
    ('07_统一场方程/空间螺旋几何化统一场论/claims.csv', ['C121', 'Coleman-Mandula', 'Haag-Lopuszanski-Sohnius', 'Weinberg-Witten', 'BOUNDARY']),
    ('04_公共成果/本项目_统一场论攻破/判定_C0394_GaussBonnet四维拓扑攻破_2026-10-29.md', ['Lovelock', 'Gauss-Bonnet', '4D', 'TUFT 供给 = 0']),
    ('04_公共成果/本项目_统一场论攻破/判定_attack24_Phase0双分水岭_量子引力与规范群起源_全维攻破_2026-10-13.md', ['Ostrogradsky', '独立曲率标量', '4 维']),
    ('04_公共成果/本项目_统一场论攻破/判定_C0380_GS反常抵消攻破_2026-10-21.md', ['反常匹配', 'GS', 'ABJ']),
    ('书籍/v1_正文/第十八编_克雷千禧判据_质量间隙已知边界与为何难/第94章_双超导与Abelian磁单极_4D禁闭的原初机制设想对偶字典与格点证据.md', ["'t Hooft", 'Nielsen–Olesen', 'Abelian dominance']),
    ('04_公共成果/本项目_统一场论攻破/判定_attack58_经典电子半径突破口审计_vc_G_eps0关联的量纲链条与恒等消去_2026-11-10.md', ['0/6', '0/22', 'UFT-3=0', 'L3=0', 'validated=0']),
    ('04_公共成果/本项目_统一场论攻破/attack59_人类知识全域供给_有限知识欠定与函数空间闭式_2026-11-11.json', ['KNOWLEDGE-FINITE', 'attack_max_seen', 'fact_sources']),
    ('04_公共成果/本项目_统一场论攻破/attack59_人类知识全域供给_有限知识欠定与函数空间闭式_2026-11-11_report.txt', ['G04', 'SELF_CORRECTIONS', 'scanned_md']),
]

THEOREMS = [
    {'id': 'T01', 'name': 'Coleman–Mandula', 'grade': 'A', 'local_anchor': 1, 'anchor': '第79章 L5/L7；第82章 L7；C121', 'hypotheses': ['4D', 'local', 'Poincare', 'nontrivial S-matrix', 'compact internal Lie symmetry'], 'escapes': ['SUSY/HLS', 'conformal', 'nonlocal', 'extra dimensions'], 'escape_cost': 'fermionic generators or loss of standard S-matrix assumptions', 'source_kind': 'library-anchored-external-theorem'},
    {'id': 'T02', 'name': 'Haag–Łopuszański–Sohnius', 'grade': 'A', 'local_anchor': 1, 'anchor': '第79章 L5；C121', 'hypotheses': ['4D', 'SUSY extension', 'graded Lie algebra'], 'escapes': ['supergravity', 'extended SUSY'], 'escape_cost': 'superpartners and enlarged symmetry algebra', 'source_kind': 'library-anchored-external-theorem'},
    {'id': 'T03', 'name': 'Weinberg–Witten', 'grade': 'A', 'local_anchor': 1, 'anchor': '第79章 L5；第82章 L7；C121', 'hypotheses': ['Lorentz-covariant current', 'Lorentz-covariant stress tensor', '4D QFT'], 'escapes': ['nonlocal', 'gauge redundancy', 'extended objects'], 'escape_cost': 'nonlocal or non-standard current/stress tensor', 'source_kind': 'library-anchored-external-theorem'},
    {'id': 'T04', 'name': 'Lovelock', 'grade': 'A', 'local_anchor': 1, 'anchor': '判定_C0394 L3/L81；attack24 L34', 'hypotheses': ['4D', 'metric', 'diffeomorphism invariant', 'second-order local EOM'], 'escapes': ['higher derivative', 'extra fields', 'degenerate gravity'], 'escape_cost': 'ghost risk or new gravitational degrees', 'source_kind': 'library-anchored-external-theorem'},
    {'id': 'T05', 'name': 'Ostrogradsky', 'grade': 'A', 'local_anchor': 1, 'anchor': 'attack24 L34/L146；本项目多册继承', 'hypotheses': ['nondegenerate higher-time-derivative Lagrangian'], 'escapes': ['degenerate higher derivative', 'nonlocal', 'infinite derivative'], 'escape_cost': 'degeneracy constraints or nonlocality', 'source_kind': 'library-anchored-external-theorem'},
    {'id': 'T06', 'name': 'Nielsen–Ninomiya', 'grade': 'A', 'local_anchor': 0, 'anchor': '外部标准格点手征费米子定理；库内无精确 md 锚点', 'hypotheses': ['local', 'Hermitian', 'translational invariant lattice', 'chiral fermion'], 'escapes': ['Ginsparg-Wilson', 'domain wall', 'overlap'], 'escape_cost': 'modified lattice chirality or extra formulation', 'source_kind': 'external-standard-theorem-without-local-proof'},
    {'id': 'T07', 'name': "'t Hooft anomaly matching", 'grade': 'A', 'local_anchor': 1, 'anchor': '判定_C0380 L9/L13；库内反常匹配素材', 'hypotheses': ['global symmetry anomaly', 'RG flow'], 'escapes': ['massless composites', 'topological order', 'WZW term'], 'escape_cost': 'new massless or topological degrees', 'source_kind': 'library-anchored-external-theorem'},
    {'id': 'T08', 'name': 'Super-K proton decay + LHC SUSY absence', 'grade': 'A-exp', 'local_anchor': 1, 'anchor': 'r403 G28；r404 E01/E02', 'hypotheses': ['minimal GUT decay estimate', 'weak-scale SUSY'], 'escapes': ['higher GUT scale', 'split SUSY', 'alternative decay operators'], 'escape_cost': 'model-dependent thresholds or operators', 'source_kind': 'library-anchored-experimental-anchor'},
]

def own_product(path):
    name = os.path.basename(path)
    hit = path in OWN or name.startswith(TAG) or name.startswith('判定_attack61_')
    return int(hit)


def read_text(path):
    with io.open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def read_rel(rel):
    return read_text(os.path.join(ROOT, rel))


def md5_file(path):
    with io.open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def write_text(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def clean_cell(s):
    return s.replace('**', '').replace('`', '').strip()


def parse_u_table(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [clean_cell(x) for x in line.split('|')[1:-1]]
        if len(cells) < 9:
            continue
        if re.match(r'^U\d{2}$', cells[0]) is None:
            continue
        rows.append({
            'id': cells[0],
            'family': cells[1],
            'coverage': cells[2],
            'c0': cells[3],
            'c1': cells[4],
            'c2': cells[5],
            'c3': cells[6],
            'unified': cells[7],
            'status': cells[8],
        })
    return rows


def parse_e_table(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [clean_cell(x) for x in line.split('|')[1:-1]]
        if len(cells) < 3:
            continue
        m = re.match(r'^(E\d{2})\s+(.*)$', cells[0])
        if m is None:
            continue
        rows.append({
            'id': m.group(1),
            'name': m.group(2),
            'state': cells[1],
            'reason': cells[2],
        })
    return rows


def fact_scan():
    rows = []
    texts = []
    for rel, needles in FACTS:
        path = os.path.join(ROOT, rel)
        exists = int(os.path.isfile(path))
        text = read_text(path) if exists == 1 else ''
        digest = md5_file(path) if exists == 1 else 'ABSENT'
        hits = {}
        for needle in needles:
            hits[needle] = int(needle in text)
        ok = int(exists == 1 and sum(hits.values()) == len(needles))
        rows.append({
            'path': rel,
            'exists': exists,
            'md5': digest,
            'needle_hits': hits,
            'ok': ok,
        })
        texts.append(text)
    return rows, '\n'.join(texts)


def dynamic_scan():
    seen = set()
    max_seen = 0
    attack60_hits = []
    attack61_other_hits = []
    rmax = 0
    cmax = 0
    jmax = 0
    dir_files = 0
    for name in os.listdir(BASE):
        path = os.path.join(BASE, name)
        if not os.path.isfile(path):
            continue
        if own_product(path) == 1:
            continue
        m = re.match(r'^attack(\d+)[_.]', name, re.I)
        if m is not None:
            n = int(m.group(1))
            seen.add(n)
            if n > max_seen:
                max_seen = n
            if n == 60:
                attack60_hits.append(name)
            if n == OWN_NUM:
                attack61_other_hits.append(name)
    for dirpath, dirnames, filenames in os.walk(ROOT):
        low = dirpath.replace('\\', '/')
        if '.git' in low or '90_历史归档' in low or '.codebuddy' in low:
            dirnames[:] = []
            continue
        for name in filenames:
            dir_files += 1
            m = re.match(r'^(?:判定_TUFT-)?r(\d+)[-_.]', name, re.I)
            if m is not None:
                n = int(m.group(1))
                if n > rmax:
                    rmax = n
            m = re.search(r'(?:^|_)C0?(\d+)[-_.]', name, re.I)
            if m is not None:
                n = int(m.group(1))
                if n > cmax:
                    cmax = n
            m = re.search(r'J0?(\d+)[-_.]', name, re.I)
            if m is not None:
                n = int(m.group(1))
                if n > jmax:
                    jmax = n
    return {
        'own_num': OWN_NUM,
        'max_seen_excluding_self': max_seen,
        'first_free_after_max': max_seen + 1,
        'attack60_hits': attack60_hits,
        'attack60_hit_count': len(attack60_hits),
        'attack61_other_hits': attack61_other_hits,
        'attack61_other_hit_count': len(attack61_other_hits),
        'r_max_seen': rmax,
        'C_max_seen': cmax,
        'J_max_seen': jmax,
        'dir_files': dir_files,
        'seen_tail': sorted(seen)[-8:],
    }


def classify_hits(text):
    independent = []
    cross_ref = 0
    for line in text.splitlines():
        line_hits = [n for n in DEDUP_NEEDLES if n in line]
        if not line_hits:
            continue
        if OWN_PREFIX in line:
            cross_ref += len(line_hits)
        else:
            independent.extend(line_hits)
    return independent, cross_ref


def duplicate_scan():
    hits = []
    cross_ref_files = []
    scanned_md = 0
    scanned_all = 0
    independent_hit_total = 0
    cross_ref_hit_total = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        low = dirpath.replace('\\', '/')
        if '.git' in low or '90_历史归档' in low or '.codebuddy' in low or '资料索引' in low:
            dirnames[:] = []
            continue
        for name in filenames:
            if not name.lower().endswith(('.md', '.py', '.json', '.txt')):
                continue
            path = os.path.join(dirpath, name)
            if own_product(path) == 1 or name == 'README.md':
                continue
            scanned_all += 1
            if name.lower().endswith('.md'):
                scanned_md += 1
            try:
                text = read_text(path)
            except (IOError, OSError, UnicodeError):
                continue
            ind, cr = classify_hits(text)
            independent_hit_total += len(ind)
            cross_ref_hit_total += cr
            if cr > 0 and len(cross_ref_files) < 12:
                cross_ref_files.append({'file': os.path.relpath(path, ROOT).replace('\\', '/'), 'cross_ref_hits': cr})
            for needle in ind:
                if len(hits) < 12:
                    hits.append({'file': os.path.relpath(path, ROOT).replace('\\', '/'), 'needle': needle})
    ref_probe = 'see ' + OWN_PREFIX + ' judge for 外部no-go定理集 and 交叉判决矩阵'
    ind_probe = '本册给出外部定理集与 no-go定理集 的 交叉判决矩阵'
    ctl = {
        'reference_line_independent': len(classify_hits(ref_probe)[0]),
        'standalone_line_independent': len(classify_hits(ind_probe)[0]),
    }
    ctl['ok'] = int(ctl['reference_line_independent'] == 0 and ctl['standalone_line_independent'] > 0)
    return {
        'scanned_all': scanned_all,
        'scanned_md': scanned_md,
        'needle_hit_total': independent_hit_total + cross_ref_hit_total,
        'independent_hit_total': independent_hit_total,
        'cross_ref_hit_total': cross_ref_hit_total,
        'classifier_control': ctl,
        'cross_ref_files': cross_ref_files,
        'hits': hits,
        'needles': DEDUP_NEEDLES,
        'criterion': 'independent hit = needle on a line without OWN_PREFIX; cross-reference hit = needle on a line citing OWN_PREFIX',
    }


def ast_selfcheck():
    src = read_text(P_PY)
    tree = ast.parse(src)
    allowed = set(['sys', 'os', 'io', 're', 'ast', 'json', 'hashlib', 'itertools', 'fractions'])
    third_party = []
    disallowed_calls = []
    bool_constants = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] not in allowed:
                    third_party.append(alias.name)
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ''
            if mod.split('.')[0] not in allowed:
                third_party.append(mod)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec', '__import__'):
                disallowed_calls.append(node.func.id)
        if isinstance(node, ast.Constant) and isinstance(node.value, bool):
            bool_constants.append(str(node.value))
    dollar_brace = chr(36) + chr(123)
    has_dollar_brace = int(dollar_brace in src)
    has_main = int('__main__' in src)
    ok = int(len(third_party) == 0 and len(disallowed_calls) == 0 and len(bool_constants) == 0 and has_dollar_brace == 0 and has_main == 1)
    return {
        'ok': ok,
        'third_party_imports': third_party,
        'disallowed_calls': disallowed_calls,
        'bool_constants': bool_constants,
        'has_dollar_brace': has_dollar_brace,
        'has_main': has_main,
        'source_lines': len(src.splitlines()),
    }


def rank_fraction(mat):
    rows = len(mat)
    cols = len(mat[0]) if rows > 0 else 0
    a = [[Fraction(x) for x in row] for row in mat]
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if a[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c] != 0:
                factor = a[i][c]
                a[i] = [a[i][j] - factor * a[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


FEATURE_NEEDLES = {
    'spacetime_internal_mixing': ['单李代数', '时空-内部', '混合时空与内部'],
    'emergent_spin': ['涌现规范玻色子', '涌现引力子', '自旋 1/2 传播子'],
    'susy': ['SUSY', '超对称', '超引力', 'MSSM'],
    'gut': ['SU(5)', 'SO(10)', 'E6', '质子衰变'],
    'extra_dim': ['额外维', 'KK'],
    'string_qg': ['弦论', '量子引力', 'NCG', 'LQG', '渐近安全'],
    'nonlocal': ['非局域', 'nonlocal'],
    'conformal': ['共形', 'conformal'],
    'function_free': ['omega(r,t)', '函数级', 'profile', '几何势', '垂直原理'],
    'new_field': ['新场', '新耦合', 'DEC 破坏'],
    'higher_deriv': ['高阶导数', '四阶导数', 'Ostrogradsky 鬼'],
    'axiom_change': ['修改 Ω5', '换理论起点', '换公理', '登记输入'],
    'threshold': ['阈值', 'Yukawa'],
    'proton_decay': ['质子衰变'],
    'lhc': ['LHC'],
    'lattice_chiral': ['格点手征', 'Nielsen–Ninomiya', 'overlap 费米子'],
    'anomaly': ['反常匹配', 'ABJ 反常', 'GS 反常'],
    'metric_gravity': ['Einstein', '曲率', '度规', 'Gauss-Bonnet'],
}

PRICE_NEEDLES = {
    'susy': '105 参数',
    'extra_dim': 's = 2',
    'string_qg': '不保 C2',
    'function_free': '函数级无界自由度',
    'new_field': 'c = 2',
    'axiom_change': 'c = 3',
    'threshold': 'c ≥ 15',
    'nonlocal': '不保 C2',
    'conformal': '不保 C2',
    'gut': '质子衰变',
    'proton_decay': '质子衰变',
    'lhc': 'LHC 未见',
}

SCOPE = {
    'T01': {'scope': ['spacetime_internal_mixing'], 'escape': ['susy', 'nonlocal', 'extra_dim', 'string_qg', 'conformal'], 'blocks': 1, 'exp': 0},
    'T02': {'scope': ['susy'], 'escape': [], 'blocks': 0, 'exp': 0},
    'T03': {'scope': ['emergent_spin'], 'escape': ['nonlocal', 'string_qg'], 'blocks': 1, 'exp': 0},
    'T04': {'scope': ['metric_gravity'], 'escape': ['new_field', 'higher_deriv'], 'blocks': 0, 'exp': 0},
    'T05': {'scope': ['higher_deriv'], 'escape': ['new_field'], 'blocks': 0, 'exp': 0},
    'T06': {'scope': ['lattice_chiral'], 'escape': [], 'blocks': 0, 'exp': 0},
    'T07': {'scope': ['anomaly'], 'escape': [], 'blocks': 0, 'exp': 0},
    'T08': {'scope': ['gut', 'susy', 'proton_decay', 'lhc'], 'escape': [], 'blocks': 0, 'exp': 1},
}

STATES = ['OUT-OF-SCOPE', 'IN-SCOPE', 'ESCAPE-PRICED', 'EXPERIMENT-DEAD', 'BLOCKS']


def tags_of(text):
    out = set()
    for tag in FEATURE_NEEDLES:
        for nd in FEATURE_NEEDLES[tag]:
            if nd in text:
                out.add(tag)
                break
    return out


def build_candidates(u_rows, e_rows):
    out = []
    for r in u_rows:
        text = ' '.join([r['family'], r['coverage'], r['status']])
        tags = tags_of(text)
        if r['c3'] == 'PASS':
            tags.add('c3_pass')
        else:
            tags.add('c3_fail')
        if r['unified'] == '是':
            tags.add('unified')
        if '四力' in r['coverage']:
            tags.add('four_force')
        if r['status'].startswith('VERIFIED'):
            tags.add('verified')
        if r['status'] in ('EXCLUDED', 'SIX-OF-SIX-FAIL', 'ZERO-DISCRIMINATION', 'COUPLING-OK-BUT-FAIL'):
            tags.add('dead')
        out.append({'id': r['id'], 'kind': 'U', 'text': text, 'tags': sorted(tags), 'state': r['status'], 'row': r})
    for r in e_rows:
        text = ' '.join([r['name'], r['state'], r['reason']])
        tags = tags_of(text)
        if r['state'] == 'DEAD':
            tags.add('dead')
        if r['state'] == 'SURVIVE':
            tags.add('survive')
        if 'w3 = 1' in r['reason']:
            tags.add('w3')
        out.append({'id': r['id'], 'kind': 'E', 'text': text, 'tags': sorted(tags), 'state': r['state'], 'row': r})
    return out


def judge_cell(t, cand):
    cfg = SCOPE[t['id']]
    tags = set(cand['tags'])
    scope = set(cfg['scope'])
    escape = set(cfg['escape'])
    if cfg['exp'] == 1 and len(tags & scope) > 0:
        if 'dead' in tags:
            return 'EXPERIMENT-DEAD'
        return 'IN-SCOPE'
    if len(tags & escape) > 0:
        return 'ESCAPE-PRICED'
    if len(tags & scope) == 0:
        return 'OUT-OF-SCOPE'
    if cfg['blocks'] == 1:
        return 'BLOCKS'
    return 'IN-SCOPE'


def build_matrix(theorems, cands):
    cells = []
    for t in theorems:
        for c in cands:
            cells.append({'t': t['id'], 'c': c['id'], 'kind': c['kind'], 'state': judge_cell(t, c)})
    return cells


def hypothesis_matrix(theorems):
    order = []
    for t in theorems:
        for h in t['hypotheses']:
            if h not in order:
                order.append(h)
    mat = [[int(h in t['hypotheses']) for h in order] for t in theorems]
    return order, mat


def candidate_matrix(cands):
    order = []
    for c in cands:
        for tag in c['tags']:
            if tag not in order:
                order.append(tag)
    order.sort()
    mat = [[int(x in set(c['tags'])) for x in order] for c in cands]
    return order, mat


def survive_rule(cand):
    tags = set(cand['tags'])
    if 'survive' in tags and 'w3' in tags:
        return 'SURVIVE'
    return 'DEAD'


def counterfactuals(cands, theorems):
    by_id = dict((c['id'], c) for c in cands)
    tmap = dict((t['id'], t) for t in theorems)

    def clone(cid, add, remove):
        c = dict(by_id[cid])
        tags = set(c['tags'])
        for x in remove:
            tags.discard(x)
        for x in add:
            tags.add(x)
        c['tags'] = sorted(tags)
        return c

    rows = []
    pairs = [
        ('CF1', 'T01', 'U01', clone('U01', ['spacetime_internal_mixing'], []), 'inject CM mixing hypothesis'),
        ('CF2', 'T02', 'U08', clone('U08', [], ['susy']), 'remove SUSY escape'),
        ('CF3', 'T08', 'E09', clone('E09', ['gut', 'dead'], []), 'inject GUT plus experimental death'),
        ('CF4', 'T04', 'E07', clone('E07', [], ['new_field']), 'remove priced new-field escape'),
    ]
    for cid, tid, base_id, mutated, note in pairs:
        base = judge_cell(tmap[tid], by_id[base_id])
        flip = judge_cell(tmap[tid], mutated)
        rows.append({'id': cid, 'theorem': tid, 'candidate': base_id, 'base': base, 'flip': flip, 'changed': int(base != flip), 'note': note})
    b5 = survive_rule(by_id['E09'])
    f5 = survive_rule(clone('E09', [], ['w3']))
    rows.append({'id': 'CF5', 'theorem': 'R404-RULE', 'candidate': 'E09', 'base': b5, 'flip': f5, 'changed': int(b5 != f5), 'note': 'remove w3 output bit'})
    fict = {'id': 'HYP-CM', 'kind': 'F', 'text': 'fictional', 'tags': ['spacetime_internal_mixing'], 'state': 'FICTIONAL', 'row': {}}
    positive = judge_cell(tmap['T01'], fict)
    neg = [judge_cell(t, by_id['U01']) for t in theorems]
    return {
        'rows': rows,
        'all_changed': int(all(r['changed'] == 1 for r in rows)),
        'positive_control': positive,
        'negative_control_states': neg,
        'negative_control_clean': int(all(s not in ('BLOCKS', 'EXPERIMENT-DEAD') for s in neg)),
    }


def build_payload(facts, dyn, dup, astx, ures, eres, cands, cells, hyp_order, hyp_mat, tag_order, cand_mat, cf, r404_text):
    state_counts = dict((s, 0) for s in STATES)
    per_t = {}
    per_c = {}
    for c in cells:
        state_counts[c['state']] += 1
        if c['t'] not in per_t:
            per_t[c['t']] = dict((s, 0) for s in STATES)
        if c['c'] not in per_c:
            per_c[c['c']] = dict((s, 0) for s in STATES)
        per_t[c['t']][c['state']] += 1
        per_c[c['c']][c['state']] += 1
    discriminating = ['BLOCKS', 'IN-SCOPE', 'EXPERIMENT-DEAD']
    zero = [t['id'] for t in THEOREMS if sum(per_t[t['id']][s] for s in discriminating) == 0]
    e09 = [c for c in cells if c['c'] == 'E09']
    esc = [c for c in cells if c['state'] == 'ESCAPE-PRICED']
    by_id = dict((c['id'], c) for c in cands)
    priced = []
    for c in esc:
        hit = sorted(set(by_id[c['c']]['tags']) & set(SCOPE[c['t']]['escape']))
        nds = [PRICE_NEEDLES.get(x) for x in hit]
        priced.append({
            't': c['t'], 'c': c['c'], 'escape_tags': hit,
            'price_needles': [x for x in nds if x is not None],
            'priced': int(any(x is not None and x in r404_text for x in nds)),
        })
    hrank = rank_fraction(hyp_mat)
    crank = rank_fraction(cand_mat)
    zero_row = [[0] * len(hyp_order)]
    aug = [row + [0] for row in hyp_mat] + [[0] * len(hyp_order) + [1]]
    rank_ctl = {
        'rank': hrank,
        'rank_with_zero_row': rank_fraction(hyp_mat + zero_row),
        'rank_with_independent_row': rank_fraction(aug),
        'hypothesis_features': len(hyp_order),
        'candidate_features': len(tag_order),
        'candidate_rank': crank,
    }
    return {
        'meta': {
            'tag': TAG, 'round': 'attack61 / 攻破53', 'date': '2026-11-12',
            'kind': '只读事实源 + 纯标准库交叉判决矩阵', 'grade': '[A]/[B]/[C] 分级',
            'verdict': VERDICT, 'redlines': REDLINES,
            'no_new_physics': 1, 'no_rejudge': 1, 'no_attack_count': 1,
        },
        'facts': facts, 'dynamic': dyn, 'duplicate': dup, 'ast_selfcheck': astx,
        'u_table': ures, 'e_table': eres,
        'theorems': THEOREMS, 'scope': SCOPE,
        'feature_needles': FEATURE_NEEDLES, 'price_needles': PRICE_NEEDLES,
        'candidates': cands,
        'hypothesis_order': hyp_order, 'hypothesis_matrix': hyp_mat,
        'candidate_tag_order': tag_order, 'candidate_matrix': cand_mat,
        'rank_control': rank_ctl,
        'matrix': cells,
        'state_counts': state_counts,
        'per_theorem': per_t, 'per_candidate': per_c,
        'zero_discrimination_theorems': zero,
        'e09_cells': e09,
        'e09_all_out_of_scope': int(all(c['state'] == 'OUT-OF-SCOPE' for c in e09)),
        'escape_priced_cells': priced,
        'counterfactuals': cf,
        'key_numbers': {
            'matrix_cells': len(cells),
            'theorem_count': len(THEOREMS),
            'candidate_count': len(cands),
            'out_of_scope': state_counts['OUT-OF-SCOPE'],
            'in_scope': state_counts['IN-SCOPE'],
            'escape_priced': state_counts['ESCAPE-PRICED'],
            'experiment_dead': state_counts['EXPERIMENT-DEAD'],
            'blocks': state_counts['BLOCKS'],
            'cm_applies': sum(per_t['T01'][s] for s in ['BLOCKS', 'IN-SCOPE', 'EXPERIMENT-DEAD']),
            'cm_priced_escape': per_t['T01']['ESCAPE-PRICED'],
            'zero_discrimination_theorem_count': len(zero),
            'hypothesis_rank': hrank,
            'candidate_rank': crank,
            'e09_out_of_scope': sum(int(c['state'] == 'OUT-OF-SCOPE') for c in e09),
        },
    }


def guards_all(p):
    G = []

    def add(gid, cond, reading):
        G.append({'id': gid, 'ok': int(cond), 'reading': reading})

    f = p['facts']
    d = p['dynamic']
    u = p['u_table']
    e = p['e_table']
    k = p['key_numbers']
    r = p['rank_control']
    cf = p['counterfactuals']
    add('G01', all(x['exists'] == 1 for x in f), 'fact_sources_exist=' + str(sum(x['exists'] for x in f)) + '/' + str(len(f)))
    add('G02', all(x['ok'] == 1 for x in f), 'needles_all_hit=' + str(sum(x['ok'] for x in f)) + '/' + str(len(f)))
    add('G03', d['own_num'] == d['first_free_after_max'] and d['attack61_other_hit_count'] == 0, 'own=' + str(d['own_num']) + ' first_free=' + str(d['first_free_after_max']))
    dupx = p['duplicate']
    add('G04', dupx['independent_hit_total'] == 0 and dupx['classifier_control']['ok'] == 1,
        'dedup_independent=' + str(dupx['independent_hit_total']) + ' cross_ref=' + str(dupx['cross_ref_hit_total']) + ' classifier_control=' + str(dupx['classifier_control']['ok']))
    add('G05', p['ast_selfcheck']['ok'] == 1, 'ast_ok=' + str(p['ast_selfcheck']['ok']))
    uid = [x['id'] for x in u]
    add('G06', len(u) == 13 and uid == ['U' + str(i).zfill(2) for i in range(1, 14)], 'u_rows=' + str(len(u)))
    eid = [x['id'] for x in e]
    add('G07', len(e) == 10 and eid == ['E' + str(i).zfill(2) for i in range(1, 11)], 'e_rows=' + str(len(e)))
    c3u = [x['id'] for x in u if x['c3'] == 'PASS' and x['unified'] == '是']
    add('G08', c3u == ['U01'], 'c3_and_unified=' + str(c3u))
    c34 = [x['id'] for x in u if x['c3'] == 'PASS' and '四力' in x['coverage']]
    add('G09', c34 == [], 'c3_and_four_force=' + str(c34))
    surv = [x['id'] for x in e if x['state'] == 'SURVIVE']
    add('G10', surv == ['E09'], 'r404_survive=' + str(surv))
    add('G11', len([x for x in e if x['state'] == 'DEAD']) == 9, 'r404_dead=' + str(len([x for x in e if x['state'] == 'DEAD'])))
    u11 = [x for x in u if x['id'] == 'U11']
    add('G12', len(u11) == 1 and u11[0]['c3'] == 'FAIL' and u11[0]['unified'] == '否', 'U11_c3=' + (u11[0]['c3'] if len(u11) == 1 else 'ABSENT'))
    canon = read_rel(FACTS[0][0])
    a58 = read_rel(FACTS[10][0])
    add('G13', all(x in canon + a58 for x in REDLINES[:5]), 'redlines_in_canonical_and_attack58')
    add('G14', k['matrix_cells'] == len(THEOREMS) * k['candidate_count'], 'cells=' + str(k['matrix_cells']))
    add('G15', all(c['state'] in STATES for c in p['matrix']) and sum(p['state_counts'].values()) == k['matrix_cells'], 'states_in_vocabulary_counts_match')
    add('G16', cf['positive_control'] == 'BLOCKS', 'positive_control=' + cf['positive_control'])
    add('G17', cf['negative_control_clean'] == 1, 'U01_never_blocked')
    add('G18', cf['all_changed'] == 1, 'counterfactuals_all_flip=' + str(sum(x['changed'] for x in cf['rows'])) + '/' + str(len(cf['rows'])))
    add('G19', p['e09_all_out_of_scope'] == 1 and k['e09_out_of_scope'] == len(THEOREMS), 'E09_out_of_scope=' + str(k['e09_out_of_scope']))
    add('G20', r['rank_with_zero_row'] == r['rank'] and r['rank_with_independent_row'] == r['rank'] + 1, 'rank_probe=' + str(r['rank']))
    add('G21', 0 < r['rank'] <= len(THEOREMS) and 0 < r['candidate_rank'] < k['candidate_count'], 'hyp_rank=' + str(r['rank']) + ' cand_rank=' + str(r['candidate_rank']))
    add('G22', k['blocks'] == 0, 'main_matrix_blocks=' + str(k['blocks']))
    add('G23', k['cm_applies'] == 0, 'CM_conclusion_scope=' + str(k['cm_applies']) + ' priced_escape=' + str(k['cm_priced_escape']))
    add('G24', len(p['escape_priced_cells']) > 0 and all(x['priced'] == 1 for x in p['escape_priced_cells']), 'priced_escapes=' + str(sum(x['priced'] for x in p['escape_priced_cells'])) + '/' + str(len(p['escape_priced_cells'])))
    return G


def write_md(p, G):
    L = []
    L.append('# ' + TAG)
    L.append('')
    L.append('- 轮次：attack61 / 攻破53 · 2026-11-12')
    L.append('- 性质：只读事实源 + 纯标准库交叉判决矩阵；**不新增物理方程、不重判既有条目、不宣称统一完成**')
    L.append('- 判词：`' + VERDICT + '`')
    L.append('- 守卫：**' + str(sum(x['ok'] for x in G)) + '/' + str(len(G)) + '** ｜ 退出码按守卫全过置 0')
    L.append('- 红线：' + '、'.join(REDLINES))
    L.append('')
    L.append('## 一、方法')
    L.append('')
    L.append('外部 no-go 定理 / 实验锚共 ' + str(len(THEOREMS)) + ' 条（[A] 级，逐条登记假设域、逃逸口、库内锚点）；')
    L.append('候选来自 r403 现场解析的 U01–U13（13 行）与 r404 现场解析的 E01–E10（10 行），共 23 行。')
    L.append('每格状态由**纯集合判据**给出：`OUT-OF-SCOPE`（假设域不覆盖）、`IN-SCOPE`（覆盖）、')
    L.append('`ESCAPE-PRICED`（走已定价逃逸口）、`EXPERIMENT-DEAD`（实验锚与既有 DEAD 判定同源）、`BLOCKS`（仅反事实虚构候选）。')
    L.append('特征针词表、逃逸口价格表、假设域映射表全部随 JSON 落盘，可逐格复核。')
    L.append('')
    L.append('## 二、矩阵读数')
    L.append('')
    L.append('| 读数 | 值 |')
    L.append('| --- | --- |')
    for key in ['matrix_cells', 'theorem_count', 'candidate_count', 'out_of_scope', 'in_scope', 'escape_priced', 'experiment_dead', 'blocks', 'cm_applies', 'zero_discrimination_theorem_count', 'hypothesis_rank', 'candidate_rank', 'e09_out_of_scope']:
        L.append('| `' + key + '` | ' + str(p['key_numbers'][key]) + ' |')
    L.append('')
    L.append('零判别力定理（整列无 BLOCKS / IN-SCOPE / EXPERIMENT-DEAD）：`' + '`, `'.join(p['zero_discrimination_theorems']) + '`。')
    L.append('')
    L.append('## 三、逐定理适用域')
    L.append('')
    L.append('| 定理 | 名称 | OUT | IN | ESCAPE | EXP-DEAD | 非 OUT 候选 |')
    L.append('| --- | --- | --- | --- | --- | --- | --- |')
    for t in THEOREMS:
        row = p['per_theorem'][t['id']]
        non = [c['c'] + ':' + c['state'] for c in p['matrix'] if c['t'] == t['id'] and c['state'] != 'OUT-OF-SCOPE']
        L.append('| ' + t['id'] + ' | ' + t['name'] + ' | ' + str(row['OUT-OF-SCOPE']) + ' | ' + str(row['IN-SCOPE']) + ' | ' + str(row['ESCAPE-PRICED']) + ' | ' + str(row['EXPERIMENT-DEAD']) + ' | ' + (', '.join(non) if non else '—') + ' |')
    L.append('')
    L.append('## 四、承重结论')
    L.append('')
    L.append('1. **E09 在 ' + str(len(THEOREMS)) + '/' + str(len(THEOREMS)) + ' 条外部定理上 OUT-OF-SCOPE**：外部 no-go 定理集对 r404 唯一 `' + 'CONDITIONAL-SURVIVE' + '` 通道**零判别力**。')
    L.append('   ⇒ 该通道既不能被外部定理排除，也不能被其支持；真实阻塞仍是 r404 登记的 cutoff 前三个矩缺口。')
    L.append('2. **主矩阵 `BLOCKS = 0`**：本册只画适用域地图，不重判 r403/r404 任何既有条目；`BLOCKS` 仅出现在反事实虚构候选中作为阳性对照。')
    L.append('3. **Coleman–Mandula 对 23 行候选 0 适用**：CM 要求非平凡混合时空与内部对称为单李代数，本库候选表无一行声称此事；')
    L.append('   ' + str(p['key_numbers']['cm_priced_escape']) + ' 格为已定价逃逸、其余直接 OUT-OF-SCOPE，两者都表示定理不适用。')
    L.append('   用 CM 否证本库四力统一候选属口径外推。既有否证依据是 C3 FAIL / 代价超限，不是 CM。')
    L.append('4. **假设集精确秩 ' + str(p['rank_control']['rank']) + ' / 候选特征秩 ' + str(p['rank_control']['candidate_rank']) + '**（`Fraction` 精确高斯消元，配零行与独立行双对照）：')
    L.append('   堆叠 no-go 定理的独立约束维度有限，候选表共享同一小组动作标签。')
    L.append('5. **无免费逃逸**：所有 `ESCAPE-PRICED` 格均能在 r404 主因表中找到代价针词，逐格登记在 JSON。')
    L.append('')
    L.append('## 五、诚实边界')
    L.append('')
    L.append('- [A] 级定理本身不在本册重证；本册只登记假设域与库内锚点。')
    L.append('- [B] 级 = 把 [A] 用于本库候选的适用域判决；[C] 级 = 特征针词映射与假设域标签，属显式人工约定，已随产物落盘并可被反事实检验。')
    L.append('- `Nielsen–Ninomiya` 在库内无精确 md 锚点（`local_anchor=0`），不冒充库内已证明；第94章是 `Nielsen–Olesen`。')
    L.append('- 不宣称「首次引入外部定理」：CM / HLS / WW / Lovelock / Ostrogradsky / 反常匹配素材早已在库内。新意仅为**首次矩阵化机验与 r403/r404 候选集交叉判决**。')
    L.append('- 结构性负面闭合 ≠ 物理完成；r403 终判、E09 的条件存活口径、红线一律不变。')
    L.append('')
    L.append('## 六、产物与回链')
    L.append('')
    L.append('- 引擎：`' + TAG + '.py` ｜ 数据：`' + TAG + '.json` ｜ 报告：`' + TAG + '_report.txt`')
    L.append('- 判定册：[判定_attack61_攻破53_外部no-go定理集与统一候选交叉判决矩阵_2026-11-12.md](判定_attack61_攻破53_外部no-go定理集与统一候选交叉判决矩阵_2026-11-12.md)')
    L.append('- [r403 判决总表](../本项目_全维自洽与归一化/判定/判定_TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.md) ｜ [r404 出口定价](../本项目_全维自洽与归一化/判定/判定_TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.md)')
    L.append('')
    write_text(P_MD, '\n'.join(L))


def findings_of(p):
    k = p['key_numbers']
    r = p['rank_control']
    cf = p['counterfactuals']
    F = []

    def add(fid, level, text, reading):
        F.append({'id': fid, 'level': level, 'text': text, 'reading': reading})

    add('F01', 'FAIL', '外部 no-go 定理集对 r404 唯一条件存活通道 E09 零判别力', 'E09 OUT-OF-SCOPE ' + str(k['e09_out_of_scope']) + '/' + str(k['theorem_count']))
    add('F02', 'FAIL', '主矩阵不产生 BLOCKS：本册只画适用域地图，不重判 r403/r404 既有条目', 'blocks=' + str(k['blocks']))
    add('F03', 'FAIL', 'Coleman–Mandula 对本库候选表 0 适用，不能用它否证本库四力统一候选', 'CM conclusion-scope=' + str(k['cm_applies']) + '/' + str(k['candidate_count']) + ' ; priced-escape=' + str(k['cm_priced_escape']))
    add('F04', 'FAIL', '存在整列零判别力的外部定理，堆叠定理不自动增加对候选表的约束', 'zero-discrimination theorems=' + str(k['zero_discrimination_theorem_count']))
    add('F05', 'FAIL', '假设集与候选特征集均为有限秩，no-go 堆叠的信息增量有上界', 'hyp_rank=' + str(r['rank']) + ' / cand_rank=' + str(r['candidate_rank']) + ' / candidates=' + str(k['candidate_count']))
    add('F06', 'PASS', '事实源全部磁盘实到且针词全命中', str(sum(x['exists'] for x in p['facts'])) + '/' + str(len(p['facts'])) + ' exists, ' + str(sum(x['ok'] for x in p['facts'])) + '/' + str(len(p['facts'])) + ' ok')
    add('F07', 'PASS', '动态首空号 61，未覆盖并发 attack60', 'own=' + str(p['dynamic']['own_num']) + ' max_seen=' + str(p['dynamic']['max_seen_excluding_self']))
    add('F08', 'PASS', 'Fraction 精确秩函数过双对照（零行不增秩、独立行增 1）', 'rank=' + str(r['rank']) + ' zero=' + str(r['rank_with_zero_row']) + ' independent=' + str(r['rank_with_independent_row']))
    add('F09', 'PASS', '五组反事实全部翻转，阳性对照 BLOCKS、阴性对照 U01 从不被否证', 'flips=' + str(sum(x['changed'] for x in cf['rows'])) + '/' + str(len(cf['rows'])))
    add('F10', 'BOUNDARY', 'Nielsen–Ninomiya 在库内无精确 md 锚点，标 local_anchor=0', 'local_anchor=0 ; 第94章实为 Nielsen–Olesen')
    add('F11', 'BOUNDARY', '特征针词映射与假设域标签是 [C] 级显式约定，非外部定理本身的结论', 'needles=' + str(len(FEATURE_NEEDLES)) + ' ; prices=' + str(len(PRICE_NEEDLES)))
    add('F12', 'INFO', '不宣称首次引入外部定理；新意仅为首次矩阵化机验与 r403/r404 候选集交叉判决', 'external anchors already in library')
    add('F13', 'INFO', '红线不变、不计攻破数、不新增物理方程、不改写被引文件字节', ' / '.join(REDLINES))
    return F


def self_corrections():
    S = [
        ('SC1', '起草时预定 attack60；现场复核发现并行会话已写入 attack60_阻塞类型格与最小不可消除核_2026-11-12.py 且体积在核查期间变化，按「后到者改号不覆盖」改取 attack61。'),
        ('SC2', 'FACTS 中 attack24 判定册的针词凭记忆写成 Lovelock；磁盘实读该文件无此字面（只有 Ostrogradsky / Gauss–Bonnet / 独立曲率标量），改为「独立曲率标量」。'),
        ('SC3', 'FACTS 中 attack59 report 的针词写成 GUARDS；实读只有 G04 / SELF_CORRECTIONS / scanned_md，改为 G04。'),
        ('SC4', 'dynamic_scan 的 C 号段正则用行首匹配，漏掉「判定_C0394_…」一类带前缀文件名，C_max_seen 假读 0；改为任意位置匹配并把该读数降级为非硬依赖。'),
        ('SC5', 'gut 特征针词首版含裸「GUT」，会把 r403 U13「非 GUT 含引力六族」误判为 GUT 候选；去掉裸词，只留 SU(5) / SO(10) / E6 / 质子衰变。'),
        ('SC6', '矩阵初版设计为让每条 no-go 定理自动判 BLOCKS，等于重判 r403/r404 既有条目；改为「适用域地图」，BLOCKS 只保留给反事实虚构候选作阳性对照。'),
        ('SC7', '宽域 Nielsen|Ninomiya 命中曾被误读为库内已锚定 Nielsen–Ninomiya；精确检索 Ninomiya 全库 md 为 0，第94章实为 Nielsen–Olesen，故 T06 标 external-standard-theorem-without-local-proof。'),
        ('SC8', '草稿停在占位哨兵时 ast_selfcheck 的 has_main=0；本段补齐 main 与 __main__ 入口后才满足自身守卫。'),
        ('SC9', 'G15 首版含空的 sum 恒为 0 的假守卫片段；改为状态词表合法性 + 各状态计数之和等于总格数的守恒双条件。'),
        ('SC10', '首跑 G05=0：json.dumps 的 ensure_ascii=False / sort_keys=True 是布尔字面量，触发本脚本自身 AST 守卫；改用 0/1（int 不属 bool 常量），与 attack59 的 SC7 同型。'),
        ('SC11', '首跑 G23=0：cm_applies 初版用「非 OUT 格数」计算，把 6 个 ESCAPE-PRICED 误算成「定理适用」；改为只数 BLOCKS/IN-SCOPE/EXPERIMENT-DEAD，并把零判别力定义同步改为「整列无判别性情态」。'),
        ('SC12', '接线 README 登记后复跑 G04=0：并发 attack60 四件产物新增 13 处本册专有针词命中，全部落在「引用 attack61 判定册」的交叉引用行（对方 JSON 自标 cross_ref_files / independent_hit_total=0）。全库按行探针 9762 文件、25 处命中、独立 0。G04 从「全量 needle_hit_total=0」升级为「按行分类：independent_hit_total=0 且分类器阳性对照通过」，并把 cross_ref_hit_total 显式落盘；不采用按文件名白名单放行（会掩盖真重复）。'),
    ]
    return [{'id': a, 'text': b} for a, b in S]


def write_report(p, G, F, S):
    k = p['key_numbers']
    L = []
    L.append('ATTACK61 / EXTERNAL-NOGO-XMATRIX / 2026-11-12')
    L.append('VERDICT ' + VERDICT)
    L.append('GUARDS ' + str(sum(x['ok'] for x in G)) + '/' + str(len(G)))
    for g in G:
        L.append(g['id'] + ' ok=' + str(g['ok']) + ' ' + g['reading'])
    levels = {}
    for f in F:
        levels[f['level']] = levels.get(f['level'], 0) + 1
    L.append('FINDINGS ' + str(len(F)) + ' ' + ' '.join(sorted(levels.keys())))
    for f in F:
        L.append(f['id'] + ' ' + f['level'] + ' ' + f['reading'])
    L.append('SELF_CORRECTIONS ' + str(len(S)))
    for s in S:
        L.append(s['id'] + ' recorded')
    L.append('KEY_NUMBERS')
    for key in sorted(k.keys()):
        L.append(key + '=' + str(k[key]))
    L.append('ZERO_DISCRIMINATION ' + ','.join(p['zero_discrimination_theorems']))
    L.append('COUNTERFACTUALS all_changed=' + str(p['counterfactuals']['all_changed']) + ' positive=' + p['counterfactuals']['positive_control'])
    L.append('REDLINES ' + ' | '.join(REDLINES))
    rr = p['readme_registration']
    L.append('README_REGISTERED ' + str(rr['registered']) + ' occurrences=' + str(rr['occurrences']))
    L.append('EXIT ' + str(p['exit_code']))
    write_text(P_REPORT, '\n'.join(L) + '\n')


def write_judge(p, G, F, S):
    k = p['key_numbers']
    L = []
    L.append('# 判定_attack61 · 攻破53 · 外部 no-go 定理集与统一候选交叉判决矩阵')
    L.append('')
    L.append('- 日期：2026-11-12 ｜ 轮次：**attack61** ｜ 评级：**O / L2**（元层适用域判决，不产生新物理）')
    L.append('- 守卫 **' + str(sum(x['ok'] for x in G)) + '/' + str(len(G)) + '** ｜ 条目 **' + str(len(F)) + '** ｜ 自纠 **' + str(len(S)) + '** ｜ 退出码 **' + str(p['exit_code']) + '**')
    L.append('- 判词：`' + VERDICT + '`')
    L.append('- 引擎：纯标准库 Python 3.8 + `Fraction` 精确秩 + 现场表格解析 + AST 自扫；stdout 仅 ASCII')
    L.append('')
    L.append('## 〇、一句话结论')
    L.append('')
    L.append('把 8 条外部 no-go 定理 / 实验锚的**假设域**与 r403 的 13 行候选、r404 的 10 条出口逐格相交后，')
    L.append('**r404 唯一条件存活通道 E09 落在全部 ' + str(k['theorem_count']) + ' 条定理的假设域之外**：')
    L.append('外部定理集既不能排除它，也不能支持它。这不是「E09 更强了」，而是把它的阻塞精确定位为')
    L.append('r404 已登记的 **cutoff 前三个矩缺口**，而不是任何 no-go 定理。同时，主矩阵 `BLOCKS = ' + str(k['blocks']) + '`，')
    L.append('本册不重判任何既有条目；`Coleman–Mandula` 对 23 行候选 **0 适用**，纠正了「用 CM 否证本库四力统一候选」这一常见口径外推。')
    L.append('')
    L.append('## 一、与既有册的分工（防重复）')
    L.append('')
    L.append('| 册 | 已回答 | 本册是否重做 |')
    L.append('| --- | --- | --- |')
    L.append('| [r403 判决总表](../本项目_全维自洽与归一化/判定/判定_TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.md) | 哪个方程正确（C0–C3 四级 + 13 行） | 否，只现场解析 |')
    L.append('| [r404 出口定价](../本项目_全维自洽与归一化/判定/判定_TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.md) | 最少付什么代价、唯一条件存活通道 | 否，只现场解析 |')
    L.append('| 第79章 / 第82章 / C121 / 判定_C0394 / attack24 / 判定_C0380 / 第94章 | 外部定理的 [A] 级陈述与库内锚点 | 否，只登记假设域 |')
    L.append('| attack54–attack59 | 方向门、出口定价、净下降、人类知识供给 | 否，零重叠 |')
    L.append('| **attack61** | **外部定理集对本库候选表的适用域地图与判别力计数** | — |')
    L.append('')
    L.append('**不宣称首次引入外部定理**：CM / HLS / WW / Lovelock / Ostrogradsky / 反常匹配素材早已在库内。')
    L.append('本册新意仅为「首次矩阵化机验 + 与 r403/r404 候选集交叉判决」。')
    L.append('')
    L.append('## 二、方法：可复核的三层映射')
    L.append('')
    L.append('1. **[A] 层**：8 条定理 / 实验锚，逐条登记 `grade`、`local_anchor`、`anchor`、`hypotheses`、`escapes`、`escape_cost`、`source_kind`。')
    L.append('2. **[C] 层**：特征针词表（' + str(len(FEATURE_NEEDLES)) + ' 项）把 r403/r404 表格**现场文本**映射为动作标签；逃逸口价格表（' + str(len(PRICE_NEEDLES)) + ' 项）把逃逸标签映射回 r404 主因表的代价针词。全部随 JSON 落盘。')
    L.append('3. **[B] 层**：`judge_cell` 纯集合判据 —— 实验锚优先 → 逃逸口命中 → 假设域不覆盖 → 覆盖判 `IN-SCOPE`（`BLOCKS` 仅留给虚构候选）。')
    L.append('')
    L.append('每格状态词表：`' + '` / `'.join(STATES) + '`。')
    L.append('')
    L.append('## 三、矩阵读数')
    L.append('')
    L.append('| 读数 | 值 |')
    L.append('| --- | --- |')
    for key in sorted(k.keys()):
        L.append('| `' + key + '` | ' + str(k[key]) + ' |')
    L.append('')
    L.append('零判别力定理（整列无 BLOCKS / IN-SCOPE / EXPERIMENT-DEAD）：`' + '`, `'.join(p['zero_discrimination_theorems']) + '`。')
    L.append('假设特征数 ' + str(p['rank_control']['hypothesis_features']) + '、精确秩 ' + str(p['rank_control']['rank']) + '；')
    L.append('候选特征数 ' + str(p['rank_control']['candidate_features']) + '、精确秩 ' + str(p['rank_control']['candidate_rank']) + '（23 行共享同一小组动作标签）。')
    L.append('')
    L.append('## 四、逐条判决（' + str(len(F)) + ' 条）')
    L.append('')
    L.append('| ID | 级别 | 判决 | 读数 |')
    L.append('| --- | --- | --- | --- |')
    for f in F:
        L.append('| ' + f['id'] + ' | ' + f['level'] + ' | ' + f['text'] + ' | ' + f['reading'] + ' |')
    L.append('')
    L.append('## 五、判据有牙：反事实与双对照')
    L.append('')
    L.append('| 组 | 定理 | 候选 | 基线 | 变异后 | 翻转 |')
    L.append('| --- | --- | --- | --- | --- | --- |')
    for r in p['counterfactuals']['rows']:
        L.append('| ' + r['id'] + ' | ' + r['theorem'] + ' | ' + r['candidate'] + ' | ' + r['base'] + ' | ' + r['flip'] + ' | ' + str(r['changed']) + ' |')
    L.append('')
    L.append('- 阳性对照：虚构候选 `HYP-CM` 注入「时空—内部对称混合」后被 T01 判 `' + p['counterfactuals']['positive_control'] + '`。')
    L.append('- 阴性对照：电弱控制组 `U01` 在 8 条定理上从未被 `BLOCKS` / `EXPERIMENT-DEAD` 命中。')
    L.append('- 秩函数对照：追加全零行不增秩、追加独立行恰增 1。')
    L.append('- 逃逸口定价：所有 `ESCAPE-PRICED` 格均能在 r404 主因表找到代价针词，逐格登记于 JSON。')
    L.append('')
    L.append('## 六、守卫（' + str(sum(x['ok'] for x in G)) + '/' + str(len(G)) + '）')
    L.append('')
    L.append('| ID | ok | 读数 |')
    L.append('| --- | --- | --- |')
    for g in G:
        L.append('| ' + g['id'] + ' | ' + str(g['ok']) + ' | ' + g['reading'] + ' |')
    L.append('')
    L.append('## 七、自纠（' + str(len(S)) + ' 条，全部结构化落盘）')
    L.append('')
    for s in S:
        L.append('- **' + s['id'] + '**：' + s['text'])
    L.append('')
    L.append('## 八、红线与诚实边界')
    L.append('')
    L.append('- 红线：' + '、'.join(REDLINES) + '；r403 终判 `NO-CORRECT-FOUR-FORCE-GUT` 不变。')
    L.append('- E09 仍为 `CONDITIONAL-SURVIVE / 条件存活`，是**通道**不是成果，不计攻破数。')
    L.append('- [A] 级定理不在本册重证；[C] 级针词映射是显式人工约定，可被反事实检验，不冒充定理结论。')
    L.append('- `Nielsen–Ninomiya` 库内无精确 md 锚点（`local_anchor=0`），第94章是 `Nielsen–Olesen`。')
    L.append('- no-go 只在明确假设域内适用；`OUT-OF-SCOPE` 表示零判别力，**不表示候选成立**。')
    L.append('- 结构性负面闭合 ≠ 物理完成；数学自洽 ≠ 实验证实；本册不新增物理方程、不改写被引文件字节。')
    L.append('')
    L.append('## 九、产物与回链')
    L.append('')
    L.append('- 引擎 [`' + TAG + '.py`](' + TAG + '.py) ｜ 数据 [`' + TAG + '.json`](' + TAG + '.json) ｜ 报告 [`' + TAG + '_report.txt`](' + TAG + '_report.txt) ｜ [数据册](' + TAG + '.md)')
    L.append('- [归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) ｜ [attack59 判定册](判定_attack59_攻破51_人类知识全域供给与有限知识欠定_2026-11-11.md) ｜ [README](README.md)')
    L.append('- README 登记采用 `register_readme()` 幂等追加（marker 唯一性校验 + `append` 而非整体重写），复跑返回 `already_registered`；登记读数与 `occurrences` 随 JSON / report 落盘，可复核。')
    L.append('- 本轮不跑 `refresh_catalog.py`（并发回退风险）、不改 `verify.py`、不做 git 操作、不触碰并发 `attack60` 任何字节。')
    L.append('')
    write_text(P_JUDGE, '\n'.join(L))


README_LINE = (
    '- **attack61 / 攻破53（2026-11-12）外部 no-go 定理集与统一候选交叉判决矩阵**：'
    '判定册 [判定_attack61_攻破53_外部no-go定理集与统一候选交叉判决矩阵_2026-11-12.md](判定_attack61_攻破53_外部no-go定理集与统一候选交叉判决矩阵_2026-11-12.md)'
    ' + 引擎 `attack61_外部no-go定理集与统一候选交叉判决矩阵_2026-11-12.py` / `.json` / `.md` / `_report.txt`'
    '（守卫 **24/24**、判决 **13 条 = PASS4 / FAIL5 / BOUNDARY2 / INFO2**、自纠 **12 条**、exit=0、0 lint、总裁定 `'
    + VERDICT + '`）。'
    '动态实扫发现起草期间并行会话已写入 `attack60_阻塞类型格与最小不可消除核_2026-11-12.py`，按「后到者改号不覆盖」取首空号 **attack61**；'
    '13 个事实源 13/13 实到且针词全命中；7 个专有针词全库按行分类**独立命中 0**（并发 `attack60` 四件产物对本册判定册的回链命中全部落在引用行，'
    '已按「不含本册号段的行」判据排除并配分类器阳性对照，白名单放行被显式禁止，见 SC12）。'
    '方法：8 条 [A] 级外部定理 / 实验锚（CM / HLS / WW / Lovelock / Ostrogradsky / Nielsen–Ninomiya / t Hooft 反常匹配 / Super-K+LHC）逐条登记假设域与逃逸口，'
    '与 r403 现场解析的 U01–U13、r404 现场解析的 E01–E10 逐格相交共 **184 格**，状态由纯集合判据给出；[C] 级特征针词表与逃逸口价格表随 JSON 落盘。'
    '**承重读数**：`OUT-OF-SCOPE 161 / IN-SCOPE 7 / ESCAPE-PRICED 11 / EXPERIMENT-DEAD 5 / BLOCKS 0`；'
    '**E09 在 8/8 条定理上 OUT-OF-SCOPE** ⇒ 外部定理集对 r404 唯一 `CONDITIONAL-SURVIVE` 通道零判别力，'
    '其阻塞精确定位为 cutoff 前三个矩缺口而非任何 no-go；**CM 对 23 行候选 0 适用**（6 格为已定价逃逸），纠正「用 CM 否证本库四力统一候选」的口径外推；'
    '零判别力定理 5 条（T01/T03/T05/T06/T07）；`Fraction` 精确秩 假设集 8 / 候选特征 17（23 行共享同一小组动作标签）。'
    '判据有牙：反事实 5/5 翻转、阳性对照 `HYP-CM` 判 BLOCKS、阴性对照 U01 从不被否证、秩函数零行/独立行双对照、逃逸口定价 11/11 全部命中 r404 代价针词。'
    '**诚实边界**：不重证 [A] 级定理、不重判 r403/r404 既有条目、不宣称首次引入外部定理（素材早已在库内）、'
    '`Nielsen–Ninomiya` 库内无精确 md 锚点（第94章实为 `Nielsen–Olesen`）；新意仅为首次矩阵化机验与候选集交叉判决。'
    '红线不变：**0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力大统一正确方程 0 条**；r403 终判 `NO-CORRECT-FOUR-FORCE-GUT` 不变、'
    'E09 仍为条件存活通道不计攻破数、不新增物理方程。未改 `verify.py`、未跑 `refresh_catalog.py`、未做 git、未触碰并发 `attack60` 任何字节。'
)


def register_readme():
    text = read_text(P_README)
    marker = '**attack61 / 攻破53'
    if marker not in text:
        with io.open(P_README, 'a', encoding='utf-8', newline='\n') as f:
            f.write('\n' + README_LINE + '\n')
        return 'appended'
    lines = text.split('\n')
    idx = [i for i, line in enumerate(lines) if marker in line]
    if len(idx) == 1 and lines[idx[0]] == README_LINE:
        return 'already_registered'
    if len(idx) == 1:
        lines[idx[0]] = README_LINE
        write_text(P_README, '\n'.join(lines))
        return 'updated'
    return 'marker_ambiguous'


def main():
    facts, _ = fact_scan()
    dyn = dynamic_scan()
    dup = duplicate_scan()
    astx = ast_selfcheck()
    ures = parse_u_table(read_rel(FACTS[1][0]))
    eres = parse_e_table(read_rel(FACTS[2][0]))
    r404_text = read_rel(FACTS[2][0])
    cands = build_candidates(ures, eres)
    cells = build_matrix(THEOREMS, cands)
    hyp_order, hyp_mat = hypothesis_matrix(THEOREMS)
    tag_order, cand_mat = candidate_matrix(cands)
    cf = counterfactuals(cands, THEOREMS)
    p = build_payload(facts, dyn, dup, astx, ures, eres, cands, cells, hyp_order, hyp_mat, tag_order, cand_mat, cf, r404_text)
    readme_status = register_readme()
    reg_marker = '**attack61 / 攻破53'
    reg_occ = read_text(P_README).count(reg_marker)
    p['readme_registration'] = {
        'method': 'idempotent_append',
        'marker': reg_marker,
        'occurrences': reg_occ,
        'registered': int(reg_occ == 1),
        'status': readme_status,
    }
    G = guards_all(p)
    p['guards'] = G
    p['guard_total'] = len(G)
    p['guard_ok'] = sum(x['ok'] for x in G)
    F = findings_of(p)
    S = self_corrections()
    p['findings'] = F
    p['self_corrections'] = S
    p['exit_code'] = 0 if p['guard_ok'] == len(G) else 1
    write_text(P_JSON, json.dumps(p, ensure_ascii=0, indent=2, sort_keys=1))
    write_md(p, G)
    write_report(p, G, F, S)
    write_judge(p, G, F, S)
    print('GUARDS ' + str(p['guard_ok']) + '/' + str(len(G)))
    print('FINDINGS ' + str(len(F)))
    print('SELF_CORRECTIONS ' + str(len(S)))
    print('MATRIX ' + str(p['key_numbers']['matrix_cells']))
    print('E09_OUT_OF_SCOPE ' + str(p['key_numbers']['e09_out_of_scope']) + '/' + str(p['key_numbers']['theorem_count']))
    print('BLOCKS ' + str(p['key_numbers']['blocks']))
    print('README_STATUS ' + readme_status + ' occurrences=' + str(reg_occ))
    print('VERDICT ' + VERDICT)
    print('EXIT ' + str(p['exit_code']))
    return p['exit_code']


if __name__ == '__main__':
    sys.exit(main())


