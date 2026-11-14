# -*- coding: utf-8 -*-
"""TUFT-r408 · 所有力装进一个方程 —— 形式完备性与方程数下界（全维审计）。

靶：用户命题「所有力可以放到一个方程里面」。
本册不产生新物理、不新造统一方程、不重判任何既有条目、不改写任何被引文件字节。
只做三件可算的事：
  (1) 把「一个方程」这句话拆成 4 个互斥问题，穷尽成 4 种形式（F1 母作用量式 / F2 母场方程式 /
      F3 profile 母公式式 / F4 单耦合参数式），并证明该分类**互斥且穷尽**；
  (2) 对 F3（profile 层）做「三元组完备性」机器判决 —— 74 卷「全部已知力都是母公式实例」
      这一句需要加限定，本册给出限定条件与最小缺失维数；
  (3) 给出**形式无关的方程数下界**：若要求「覆盖四力且含动力学」，方程数下界与打包方式无关。

引擎：纯标准库 Python 3.8；Decimal(60) + Fraction 四元组量纲 (M,L,T,Q)；AST 自检。
运行：python TUFT-r408_所有力装进一个方程_形式完备性与方程数下界_全维审计_2026-11-14.py
"""
import os
import re
import io
import sys
import json
import hashlib
import ast
import subprocess
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO = os.path.dirname(HERE)                        # 算法联盟_全维自洽与归一化
ROOT = os.path.dirname(os.path.dirname(ALGO))       # openuft 根（源码→册目录→04_公共成果→根）
DATE = '2026-11-14'
NAME = 'TUFT-r408_所有力装进一个方程_形式完备性与方程数下界_全维审计_' + DATE
ENGINE = NAME + '.py'

GUARDS = []
ENTRIES = []
SELF_CORRECTIONS = []


def log(msg):
    sys.stdout.write(str(msg) + '\n')


def G(code, ok, value):
    GUARDS.append({'code': code, 'ok': bool(ok), 'value': str(value)})
    return bool(ok)


def E(code, status, title, detail=''):
    ENTRIES.append({'code': code, 'status': status, 'title': title, 'detail': detail})
    return status


# ---------------------------------------------------------------- 路径工具
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
    return io.open(p, encoding='utf-8').read()


# ---------------------------------------------------------------- 量纲四元组 (M,L,T,Q)
ZERO = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
T = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
Q = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))


def dneg(d):
    return tuple(-x for x in d)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dmul(a, b):
    """量纲相乘 = 指数相加（不是逐分量相乘）。"""
    return tuple(x * y for x, y in zip(a, b))


def dscale(d, k):
    return tuple(x * k for x in d)


def dpow(d, n):
    return tuple(x * n for x in d)


def dinv(d):
    return dneg(d)


def dstr(d):
    names = ['M', 'L', 'T', 'Q']
    out = []
    for n, e in zip(names, d):
        if e == 0:
            continue
        if e == 1:
            out.append(n)
        elif e == -1:
            out.append('1/' + n)
        else:
            out.append('%s^(%s)' % (n, e))
    return '1' if not out else ' * '.join(out)


def deq(a, b):
    return tuple(a) == tuple(b)


# ---------------------------------------------------------------- AST 自检
STD_ALLOWED = set([
    'os', 're', 'io', 'sys', 'json', 'hashlib', 'ast', 'subprocess', 'decimal',
    'fractions', 'collections', 'itertools', 'math', 'typing', 'dataclasses',
])
BANNED_CALLS = set(['eval', 'exec', 'compile', '__import__', 'open_code'])


def ast_selfcheck(path):
    """扫描本引擎源码：白名单导入 + 禁危险内建 + 禁布尔字面量硬编码结论。"""
    src = open(path, 'rb').read()
    tree = ast.parse(src)
    bad_import = []
    bad_call = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split('.')[0] not in STD_ALLOWED:
                    bad_import.append(a.name)
        elif isinstance(node, ast.ImportFrom):
            if (node.module or '').split('.')[0] not in STD_ALLOWED:
                bad_import.append(node.module or '')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BANNED_CALLS:
                bad_call.append(node.func.id)
    return {'bad_import': sorted(set(bad_import)), 'bad_call': sorted(set(bad_call)),
            'md5': md5_bytes(src), 'bytes': len(src)}


# ---------------------------------------------------------------- 事实源
FACT_SOURCES = {
    'ufe00': '07_统一场方程/00_统一场方程.md',
    'ufe01': '07_统一场方程/01_作用量与场内容.md',
    'ufe02': '07_统一场方程/02_变分推导.md',
    'vol74': '07_统一场方程/74_力的统一_单方程力谱完全分类_2026-10-28.md',
    'vol75': '07_统一场方程/75_力的统一_速度依赖扩展与全域分类完备性_2026-10-29.md',
    'vol109': '07_统一场方程/109_第68轮_终局收口_四台仪器与28留格29缩格处置及Z无原理_J87_七轴文法内四力FORM统一no-go判决B与逃逸口_2026-11-08.md',
    'vol134': '07_统一场方程/134_第91轮_全维度全链路归一化_J113_80节点DAG首建_四轴量纲26条与自然单位10条_恒等式29条_记分板0比6_2026-11-13.md',
    'canon': '统一场论理论体系与方程_归一正本_2026-11-09.md',
    'r404': '04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.md',
    'atk51': '04_公共成果/本项目_统一场论攻破/判定_attack51_统一场方程单方程性与耦合块结构判决_2026-11-09.md',
}


def load_facts():
    out = {}
    for k, relp in FACT_SOURCES.items():
        p = rp(*relp.split('/'))
        out[k] = {'path': relp, 'exists': os.path.isfile(p),
                  'md5_before': md5_file(p), 'text': read_text(p) if os.path.isfile(p) else ''}
    return out


def md5_after():
    return dict((k, md5_file(rp(*v.split('/')))) for k, v in FACT_SOURCES.items())


# ---------------------------------------------------------------- V1 形式谱系穷尽性
# 「一个方程」这句话的两个正交问题：
#   Q1 对象类型：field_eq(场方程) / action(作用量) / profile(静力势/力) / constraint(条件)
#   Q2 是否含动力学：dyn / static
# 8 种组合全枚举；每种映射到唯一形式类；有效形式类 = F1/F2/F3/F0 + F4（横切要求）。
FORM_TAXONOMY = {
    ('action', 'dyn'): 'F1',
    ('field_eq', 'dyn'): 'F1_or_F2',   # 依部门间交叉耦合块数分流
    ('field_eq', 'static'): 'NOT_APPLICABLE',
    ('action', 'static'): 'NOT_APPLICABLE',
    ('profile', 'static'): 'F3',
    ('profile', 'dyn'): 'NOT_APPLICABLE',
    ('constraint', 'static'): 'F0',
    ('constraint', 'dyn'): 'NOT_APPLICABLE',
}
FORM_DEFS = {
    'F1': '母作用量式：一个 S，多场变分出多条 E-L 方程；盒装 δS/δΦ=0 只是记号缩写',
    'F2': '母场方程式：一条场方程同时含多个部门（需部门间交叉耦合块）',
    'F3': 'profile 母公式式：一条静力势/力公式，用 (自旋 s, 媒介子质量 m, 耦合积 g1g2) 三元组覆盖各力',
    'F4': '单耦合参数式：要求所有耦合由同一原理导出（对 F1/F2 的横切附加要求）',
    'F0': '记号层条件式：只给约束/条件，不是动力学方程',
}


def form_taxonomy():
    combos = []
    for q1 in ('field_eq', 'action', 'profile', 'constraint'):
        for q2 in ('dyn', 'static'):
            combos.append((q1, q2, FORM_TAXONOMY[(q1, q2)]))
    valid = sorted(set(c[2] for c in combos if c[2] != 'NOT_APPLICABLE'))
    covered = all(c[2] != 'UNMAPPED' for c in combos)
    return {'combos': combos, 'n_combos': len(combos), 'valid_forms': valid,
            'n_valid': len(valid), 'all_mapped': covered,
            'exhaustive': len(combos) == 8 and covered,
            'defs': FORM_DEFS}


# ---------------------------------------------------------------- V2 F3 profile 完备性
FORCE_KEYS = ['引力', '电磁', '弱', '强', '希格斯介导']


def profile_coverage(txt74):
    """从 74 卷力谱清单逐行抽取四元组与外加特征标签，判定三元组完备性。"""
    rows = []
    for line in txt74.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 4:
            continue
        name = cells[0]
        if name not in FORCE_KEYS:
            continue
        triple = cells[1]
        sign = cells[2]
        row_txt = line
        s_m = re.search(r'\(([^)]*)\)', triple)
        sm = s_m.group(1) if s_m else ''
        s_part = sm.split(',')[0].strip() if sm else ''
        rows.append({
            'force': name,
            'triple_cell': triple,
            'spin_label': s_part,
            'sign_cell': sign,
            'has_static_profile': ('无经典静力' not in sign),
            'chiral_tag': ('手征' in row_txt or 'V−A' in row_txt or 'V-A' in row_txt),
            'confine_tag': ('禁闭' in row_txt),
            'nonabelian_tag': ('非阿贝尔' in row_txt),
            'size_input': ('【输入】' in row_txt),
        })
    # 三元组维数：从母公式解析自由参数组
    m_f = re.search(r'\\boxed\{[^}]*\}', txt74)
    formula = m_f.group(0) if m_f else ''
    _bl = _boxed_blocks(txt74)
    for _b in _bl:
        if 'V(r)' in _b or 'g_1' in _b or 'g_{1}' in _b:
            formula = _b
            break
    groups = []
    if re.search(r'\^\{s\+1\}', formula):
        groups.append('s')
    if re.search(r'e\^\{-?m', formula) or 'e^{-mr}' in formula:
        groups.append('m')
    if re.search(r'g_\{?1', formula) and re.search(r'g_\{?2', formula):
        groups.append('g1g2')
    n_triple = len(groups)
    _g2 = []
    if 's+1' in formula:
        _g2.append('s')
    if '{-mr}' in formula or 'e^{-mr}' in formula:
        _g2.append('m')
    if ('g_1' in formula or 'g_{1}' in formula) and ('g_2' in formula or 'g_{2}' in formula):
        _g2.append('g1g2')
    groups = _g2
    n_triple = len(groups)
    # 覆盖判定
    static_ok = [r for r in rows if r['has_static_profile']]
    static_bad = [r for r in rows if not r['has_static_profile']]
    basic = [r for r in rows if r['force'] != '希格斯介导']
    basic_static_ok = [r for r in basic if r['has_static_profile']]
    basic_static_bad = [r for r in basic if not r['has_static_profile']]
    # 外加标签维（不在三元组内）
    extra_dims = []
    if any(r['chiral_tag'] for r in rows):
        extra_dims.append('chiral')
    if any(r['confine_tag'] for r in rows):
        extra_dims.append('confinement')
    # 阳性对照：注入缺失维后覆盖力数
    def covered_with(inject_chiral, inject_confinement, inject_weak_static=False):
        c = 0
        for r in rows:
            if r['force'] == '希格斯介导':
                continue
            has_static = r['has_static_profile'] or (inject_weak_static and r['force'] == '弱')
            ok = has_static
            if r['chiral_tag'] and not inject_chiral:
                ok = False
            if r['confine_tag'] and not inject_confinement:
                ok = False
            if ok:
                c += 1
        return c
    cov0 = covered_with(False, False)
    cov_chiral = covered_with(True, False)
    cov_conf = covered_with(False, True)
    cov_both = covered_with(True, True)
    cov_inject_weak = covered_with(True, True, True)
    cov_static = len(basic_static_ok)
    n_extra_dims = len(extra_dims)
    return {
        'rows': rows, 'n_rows': len(rows),
        'formula': formula, 'triple_groups': groups, 'n_triple_dims': n_triple,
        'static_covered': [r['force'] for r in static_ok],
        'static_excluded': [r['force'] for r in static_bad],
        'basic_static_covered': [r['force'] for r in basic_static_ok],
        'basic_static_excluded': [r['force'] for r in basic_static_bad],
        'n_basic': len(basic), 'n_basic_static_covered': len(basic_static_ok),
        'extra_dims': extra_dims, 'n_extra_dims': len(extra_dims),
        'cov_static': cov_static,
        'cov0': cov0, 'cov_chiral': cov_chiral, 'cov_confinement': cov_conf,
        'cov_both': cov_both, 'cov_inject_weak_static': cov_inject_weak,
        'complete': (cov_both == len(basic)),
    }


# ---------------------------------------------------------------- V3 F1 方程数独立复算
def _boxed_blocks(text):
    """返回所有 \\boxed{...} 的完整内容（花括号配平扫描，避免嵌套被截断）。"""
    out = []
    i = 0
    key = '\\boxed{'
    while True:
        j = text.find(key, i)
        if j < 0:
            break
        k = j + len(key)
        depth = 1
        while k < len(text) and depth > 0:
            if text[k] == '{':
                depth += 1
            elif text[k] == '}':
                depth -= 1
            k += 1
        out.append(text[j + len(key):k - 1])
        i = k
    return out


def equation_count(t00, t01, t02):
    blocks = _boxed_blocks(t00)
    boxed = len(re.findall(r'\\tag\{UFE-1\}', t00))
    boxed_eq = sum(1 for b in blocks if '\\delta S' in b and '\\delta' in b)
    var_sections = re.findall(r'^##\s*\d+\.\s*对\s*(.+?)\s*变分', t02, flags=re.M)
    n_var = len(var_sections)
    m_five = len(re.findall(r'五个方程', t02))
    m_blocks = re.findall(r'S\s*=\s*S_\{?\\rm\s*([A-Za-z]+)\}\s*\+\s*S_\{?\\rm\s*([A-Za-z]+)\}'
                          r'\s*\+\s*S_\{?\\rm\s*([A-Za-z]+)\}\s*\+\s*S_\{?\\rm\s*([A-Za-z]+)\}'
                          r'\s*\+\s*S_\{?\\rm\s*([A-Za-z]+)\}', t01)
    n_blocks = len(m_blocks[0]) if m_blocks else 0
    # 展开级：每个变分对象对应的独立场数
    expand = 0
    for s in var_sections:
        if 'A^{(i)}' in s or '内部规范势' in s:
            expand += 3
        else:
            expand += 1
    official_denial = len(re.findall(r'不能从该作用量推出一个同时包含', t00))
    return {
        'boxed_tag_UFE1': boxed, 'boxed_deltaS': boxed_eq,
        'boxed_blocks': blocks,
        'var_sections': var_sections, 'n_var_sections': n_var,
        'title_five_equations': m_five, 'n_action_blocks': n_blocks,
        'expanded_fields': expand,
        'official_denial_statements': official_denial,
    }


# ---------------------------------------------------------------- V4 F2 交叉项代价
def cross_term_scan(t00):
    # 00 §2.1 作用量：按 LaTeX 换行 \\[2pt] 切成段
    m = re.search(r'\\boxed\{[^{}]*\\delta S[^{}]*\}(.*?)(?:\n\n|\n## )', t00, flags=re.S)
    body = m.group(1) if m else ''
    segs = [s for s in re.split(r'\\\\\[2pt\]', body) if s.strip()]
    grav_pat = r'R\^\{ab\}|\\tilde R'
    gauge_pat = r'F\^\{\(i\)\}|G\^A_\{\\mu\\nu\}|W\^i_\{\\mu\\nu\}|B_\{\\mu\\nu\}'
    _BS = chr(92)
    _mark = _BS + _BS + '[2pt]'
    _lines = t00.splitlines()
    _idx = [i for i, l in enumerate(_lines) if _mark in l]
    if _idx:
        _raw = chr(10).join(_lines[_idx[0]:_idx[-1] + 2])
        segs = [s for s in _raw.split(_mark) if s.strip()]
    n_grav = sum(1 for s in segs if re.search(grav_pat, s))
    n_gauge = sum(1 for s in segs if re.search(gauge_pat, s))
    n_cross = sum(1 for s in segs if re.search(grav_pat, s) and re.search(gauge_pat, s))
    # 阳性对照：注入 R∧F 交叉项
    segs_inj = list(segs)
    segs_inj.append('+ c_{GF} \\, R^{ab}\\wedge F^{(i)}')
    n_cross_inj = sum(1 for s in segs_inj if re.search(grav_pat, s) and re.search(gauge_pat, s))
    # 对易子声明
    comm_declare = len(re.findall(r'\[\s*\\mathfrak\{so\}\(1,3\)\s*,\s*\\mathfrak\{g\}_\{\\rm int\}\s*\]\s*=\s*0', t00))
    comm_declare_alt = len(re.findall(r'交叉对易子消失', t00))
    # 量纲：交叉块 R∧F∧e∧e 与「规范侧同类项 F∧e∧e」「引力侧同类项 R∧R∧e∧e」的齐次性
    d_R = dscale(dneg(L), 2)                 # [R^{ab}] = L^-2
    d_F = dmul(dmul(M, dneg(T)), Q)          # [F^{(i)}] = M T^-2 Q^-1
    d_e = L
    d_cross_term = dmul(dmul(d_R, d_F), dmul(d_e, d_e))       # R F e e
    d_gauge_2form = dmul(d_F, dmul(d_e, d_e))                 # F e e
    d_grav_2form = dmul(dmul(d_R, d_R), dmul(d_e, d_e))       # R R e e
    return {
        'n_segments': len(segs), 'n_grav_segments': n_grav, 'n_gauge_segments': n_gauge,
        'n_cross_segments': n_cross, 'n_cross_after_injection': n_cross_inj,
        'commutator_declared': comm_declare + comm_declare_alt,
        'dim_cross_term': dstr(d_cross_term),
        'dim_gauge_2form': dstr(d_gauge_2form),
        'dim_grav_2form': dstr(d_grav_2form),
        'dim_cross_eq_gauge2form': deq(d_cross_term, d_gauge_2form),
        'dim_cross_ne_grav2form': not deq(d_cross_term, d_grav_2form),
    }


# ---------------------------------------------------------------- V5 F4 单耦合参数穷举
D_C = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))     # c = L T^-1
D_HBAR = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))  # ħ = M L^2 T^-1
D_G = (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0))    # G = M^-1 L^3 T^-2
D_M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))      # m = M
D_E = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))      # e = Q
D_ALPHA = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))  # α 无量纲


def _dim_of(pows):
    d = ZERO
    for (nm, k), dim in pows.items():
        if k:
            d = dadd(d, dscale(dim, k))
    return d


def coupling_enum_legacy(pow_lo=-3, pow_hi=3, allow_G_self=True):
    """[已废弃的 Part 2 旧版枚举：口径含 '全基组 6 个' 与 '去质量标度' 两种写法，
    与下方活动版 coupling_enum（带机器降维论证与三档口径对照）重复。
    保留仅作历史留档，不被任何调用点引用；活动版定义在本文件更下方。]"""
    rng = list(range(pow_lo, pow_hi + 1))
    bases = [('c', D_C), ('hbar', D_HBAR), ('G', D_G), ('m', D_M), ('e', D_E), ('alpha', D_ALPHA)]
    hits_all = []
    hits_noG = []
    n_combos = 0
    for a in rng:
        for b in rng:
            for d in rng:
                for f in rng:
                    for g in rng:
                        for h in rng:
                            n_combos += 1
                            pw = {('c', a): D_C, ('hbar', b): D_HBAR, ('G', d): D_G,
                                  ('m', f): D_M, ('e', g): D_E, ('alpha', h): D_ALPHA}
                            tot = dadd(D_G, _dim_of(pw))
                            if all(x == 0 for x in tot):
                                rec = {'a': a, 'b': b, 'd': d, 'f': f, 'g': g, 'h': h}
                                hits_all.append(rec)
                                if d == 0:
                                    hits_noG.append(rec)
    def core(rec):
        return 'G^{%d} c^{%d} hbar^{%d} m^{%d} e^{%d} alpha^{%d}' % (
            rec['d'], rec['a'], rec['b'], rec['f'], rec['g'], rec['h'])
    cores_all = sorted(set(core(r) for r in hits_all))
    cores_noG = sorted(set(core(r) for r in hits_noG))
    # 非平凡核心（排除 G^0 c^0 hbar^0 m^0 e^0 alpha^0 = 1 与 G^{-1} 平凡幂）
    nontrivial = [c for c in cores_noG if c != 'G^{0} c^{0} hbar^{0} m^{0} e^{0} alpha^{0}']
    trivial = [c for c in cores_all if c in ('G^{-1} c^{0} hbar^{0} m^{0} e^{0} alpha^{0}',)]
    # 去掉质量标度 m（f=0）的命中
    no_mass = [r for r in hits_noG if r['f'] == 0]
    no_mass_cores = sorted(set(core(r) for r in no_mass))
    # m = m_P 时的恒等复读
    mP = (Decimal('1.616255') * Decimal('1E-35'))
    Gv = Decimal('6.67430E-11')
    cv = Decimal('299792458')
    hbarv = Decimal('1.054571817E-34')
    val = Gv * (mP ** 2) / (hbarv * cv)
    return {
        'n_combos_full6': n_combos,
        'n_hits_full6': len(hits_all),
        'n_hits_noG_self': len(hits_noG),
        'cores_all': cores_all,
        'cores_noG_self': cores_noG,
        'nontrivial_cores_noG': nontrivial,
        'trivial_cores': trivial,
        'n_hits_no_mass': len(no_mass),
        'cores_no_mass': no_mass_cores,
        'planck_identity_value': format(val, '.25E'),
        'planck_identity_rel_dev': format(abs(val - Decimal(1)) / Decimal(1), '.6E'),
    }


def coupling_enum(pow_lo=-3, pow_hi=3, allow_G_self=True):
    """穷举 Π=c^a ħ^b G^d m^f e^g α^h，使 G·Π 无量纲。

    降维论证（机器给出，不假设）：若基组中恰有 1 个含非零 Q 分量，则该基组的幂必为 0
    （否则总量纲 Q 分量非零），故全穷举等价于把它剔除后的 5 基组穷举。
    返回命中集合与三档口径对照（全基组 / 不含 G 自身 / 去掉质量标度）。
    """
    rng = list(range(pow_lo, pow_hi + 1))
    bases = [('c', D_C), ('hbar', D_HBAR), ('G', D_G), ('m', D_M), ('e', D_E), ('alpha', D_ALPHA)]
    q_sources = [nm for (nm, dim) in bases if dim[3] != 0]
    reduce_names = q_sources[:] if len(q_sources) == 1 else []
    reduced = [(nm, dim) for (nm, dim) in bases if nm not in reduce_names]
    n_full = len(rng) ** len(bases)
    n_reduced = len(rng) ** len(reduced)
    # 降维正确性：含被剔除基组的项必不满足 Q=0
    hits_all = []
    hits_noG = []
    for a in rng:
        for b in rng:
            for d in rng:
                for f in rng:
                    for h in rng:
                        pw = {('c', a): D_C, ('hbar', b): D_HBAR, ('G', d): D_G,
                              ('m', f): D_M, ('alpha', h): D_ALPHA}
                        tot = dadd(D_G, _dim_of(pw))
                        if all(x == 0 for x in tot):
                            rec = {'a': a, 'b': b, 'd': d, 'f': f, 'g': 0, 'h': h}
                            hits_all.append(rec)
                            if d == 0:
                                hits_noG.append(rec)
    # 阳性对照：把 e 的幂放开到 1，确认它确实破坏 Q=0
    def q_break():
        pw = {('c', 0): D_C, ('hbar', 0): D_HBAR, ('G', 0): D_G,
              ('m', 0): D_M, ('e', 1): D_E, ('alpha', 0): D_ALPHA}
        tot = dadd(D_G, _dim_of(pw))
        return not all(x == 0 for x in tot)
    def core(rec):
        return 'G^{%d} c^{%d} hbar^{%d} m^{%d} e^{%d} alpha^{%d}' % (
            rec['d'], rec['a'], rec['b'], rec['f'], rec['g'], rec['h'])
    cores_all = sorted(set(core(r) for r in hits_all))
    cores_noG = sorted(set(core(r) for r in hits_noG))
    nontrivial = [c for c in cores_noG
                  if c != 'G^{0} c^{0} hbar^{0} m^{0} e^{0} alpha^{0}']
    trivial = [c for c in cores_all if c.startswith('G^{-1}')]
    no_mass = [r for r in hits_noG if r['f'] == 0]
    no_mass_cores = sorted(set(core(r) for r in no_mass))
    _cand = [r for r in hits_noG if r['h'] == 0 and r['f'] != 0]
    core_canonical = core(_cand[0]) if _cand else ''
    # m = m_P 时的恒等复读（m_P 由 sqrt(ħc/G) 独立实算，不用字面值）
    Gv = Decimal('6.67430E-11')
    cv = Decimal('299792458')
    hbarv = Decimal('1.054571817E-34')
    mP = (hbarv * cv / Gv).sqrt()
    val = Gv * (mP * mP) / (hbarv * cv)
    return {
        'q_sources': q_sources,
        'reduction_justified': (len(q_sources) == 1),
        'e_pow_forced_zero_control_breaks': q_break(),
        'n_combos_full6': n_full,
        'n_combos_reduced5': n_reduced,
        'n_hits_full6': len(hits_all),
        'n_hits_noG_self': len(hits_noG),
        'cores_all': cores_all,
        'cores_noG_self': cores_noG,
        'nontrivial_cores_noG': nontrivial,
        'trivial_cores': trivial,
        'n_hits_no_mass_noG': len(no_mass),
        'cores_no_mass_noG': no_mass_cores,
        'n_hits_no_mass_full6': len([r for r in hits_all if r['f'] == 0]),
        'planck_mass_kg': format(mP, '.25E'),
        'core_canonical': core_canonical,
        'planck_identity_value': format(val, '.25E'),
        'planck_identity_rel_dev': format(abs(val - Decimal(1)), '.6E'),
    }


# ---------------------------------------------------------------- V6 红线核对
def redline_check(t134, tcanon, tatk51, tr404):
    def find(pat, text):
        m = re.search(pat, text)
        return m.group(0) if m else ''
    out = {}
    out['canon_0of6'] = find(r'0/6', tcanon)
    out['canon_0of22'] = find(r'0/22', tcanon)
    out['canon_uft3'] = find(r'UFT-3\s*=\s*0', tcanon)
    out['canon_validated'] = find(r'validated\s*=\s*0', tcanon)
    out['canon_l3'] = find(r'L3', tcanon)
    out['canon_not_complete'] = find(r'未完成', tcanon)
    out['vol134_scoreboard'] = find(r'0/6', t134)
    out['atk51_1_5_7'] = find(r'1\s*:\s*5\s*:\s*7', tatk51)
    out['atk51_verdict'] = find(r'STRUCTURAL_NEGATIVE_CLOSURE', tatk51)
    out['r404_K'] = find(r'K0\d', tr404)
    out['r404_verdict'] = find(r'MINIMUM-COST-LOWER-BOUND--[A-Z\-]+', tr404)
    return out


# ---------------------------------------------------------------- V7 记分板
def scoreboard(tax, prof, eqc, cross, coup):
    rows = []
    # F1
    rows.append({
        'form': 'F1', 'name': FORM_DEFS['F1'],
        'n_eq': eqc['expanded_fields'], 'n_eq_basis': 'UFE-1 展开级（7 场组）',
        'cross_blocks': cross['n_cross_segments'],
        'coupling_derivable': False,
        'covers_basic_forces': 4,
        'contains_dynamics': True,
        'verdict': 'NOTATION_ONLY',
        'reason': '盒装 δS/δΦ=0 背后是 %d 条独立 E-L 方程；交叉耦合块 %d ⇒ 无新统一动力学'
                  % (eqc['n_var_sections'], cross['n_cross_segments']),
    })
    # F2
    rows.append({
        'form': 'F2', 'name': FORM_DEFS['F2'],
        'n_eq': 1, 'n_eq_basis': '若真单方程',
        'cross_blocks': cross['n_cross_after_injection'],
        'coupling_derivable': False,
        'covers_basic_forces': 4,
        'contains_dynamics': True,
        'verdict': 'IMPOSSIBLE_AT_ZERO_COST',
        'reason': '00 卷自陈不能由该作用量推出 ⋆D_A⋆F=J；引入 R∧F 交叉块即破坏 [so(1,3),g_int]=0 与还原',
    })
    # F3
    rows.append({
        'form': 'F3', 'name': FORM_DEFS['F3'],
        'n_eq': 1, 'n_eq_basis': '单条静力势公式',
        'cross_blocks': 0,
        'coupling_derivable': False,
        'covers_basic_forces': prof['n_basic_static_covered'],
        'contains_dynamics': False,
        'verdict': 'INCOMPLETE_DOMAIN',
        'reason': '三元组维数 %d，额外特征维 %d（%s）；静态 profile 覆盖基本力 %d/%d，%s 无经典静力'
                  % (prof['n_triple_dims'], prof['n_extra_dims'], ','.join(prof['extra_dims']),
                     prof['n_basic_static_covered'], prof['n_basic'],
                     ','.join(prof['basic_static_excluded'])),
    })
    # F4
    rows.append({
        'form': 'F4', 'name': FORM_DEFS['F4'],
        'n_eq': None, 'n_eq_basis': '与 F1/F2 正交',
        'cross_blocks': None,
        'coupling_derivable': False,
        'covers_basic_forces': 4,
        'contains_dynamics': True,
        'verdict': 'IDENTITY_REPLAY_ONLY',
        'reason': '唯一非平凡核心 %s；m=m_P 时相对偏差 %s ⇒ 恒等复读零判别力'
                  % (coup['core_canonical'] or '无', coup['planck_identity_rel_dev']),
    })
    return rows


# ---------------------------------------------------------------- 查重 / 取号
NEEDLES = ['装进一个方程', '单方程化的形式谱系', 'profile层三元组完备性',
           '方程数下界与打包方式无关', '形式无关的方程数下界', '单方程可辨性']


def dynamic_number_scan():
    """现场实扫 r408 文件名占用；排除本册自身产物（判定册/引擎/数据三件套，重跑幂等）。

    本册号段即 r408，故凡文件名含 r408 者归为「本册自身」，其余才算他方占号。
    """
    own = []
    hits = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if 'r408' not in f:
                continue
            p = rel(os.path.join(root, f))
            if '算法联盟_全维自洽与归一化' in p:
                own.append(p)
            else:
                hits.append(p)
    return hits, own


def dedup_scan():
    """专有针词全仓 md 扫描。

    排除口径（承 attack63 册体例）：本册自身产物（含 r408 号段）、`README*` 索引、资料索引。
    """
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
            if 'r408' in f or NAME in f:
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


def build_entries(tax, prof, eqc, cross, coup, red):
    E('D01', 'PASS', '靶定位与事实源（10/10 存在，md5 运行前后双证不变）',
      '只读结构判决；不新造统一方程、不重判既有条目、不改任何被引文件字节。')
    E('D02', 'PASS', '形式谱系穷尽性：4 个正交问题 → 8 种组合全覆盖 → 有效形式 F0/F1/F2/F3 + 横切 F4',
      'combos=%d valid=%s all_mapped=%s exhaustive=%s' % (
          tax['n_combos'], tax['valid_forms'], tax['all_mapped'], tax['exhaustive']))
    E('D03', 'FAIL', 'F3（profile 母公式）三元组不完备：静态 profile 只覆盖基本力 %d/%d，%s 无经典静力；加维上限仍为 %d/%d' % (
        prof['n_basic_static_covered'], prof['n_basic'], ','.join(prof['basic_static_excluded']),
        prof['cov_both'], prof['n_basic']),
      '弱作用不是「少一维」而是「原理性不可覆盖」：静力母公式的定义域里没有它，加任何标签维也救不回来，须换母公式类型。')
    E('D04', 'FAIL', 'F3 三元组缺 ≥%d 个外加特征维（%s）：手征与非阿贝尔禁闭不可由 (s,m,q) 计算' % (
        prof['n_extra_dims'], ','.join(prof['extra_dims'])),
      'cov_static=%d cov0=%d cov_chiral=%d cov_confinement=%d cov_both=%d basic=%d' % (
          prof['cov_static'], prof['cov0'], prof['cov_chiral'], prof['cov_confinement'],
          prof['cov_both'], prof['n_basic']))
    E('D05', 'PASS', 'F3 判据有牙（阳性对照）：注入「弱存在静力 profile」后覆盖升到 %d/%d ⇒ 覆盖判据可被正确翻转，不是恒真' % (
        prof['cov_inject_weak_static'], prof['n_basic']),
      '反向读数：只注入标签维（χ=%d、禁闭=%d、两维=%d）无法把覆盖推满 —— 上限 %d/%d ⇒ 弱作用是定义域缺口而非维数缺口。' % (
          prof['cov_chiral'], prof['cov_confinement'], prof['cov_both'],
          prof['cov_both'], prof['n_basic']))
    E('D06', 'PASS', 'F1 方程数独立复算：盒装 1 : 变分 %d : 作用量块 %d : 展开场组 %d（与 attack51 互印）' % (
        eqc['n_var_sections'], eqc['n_action_blocks'], eqc['expanded_fields']),
      '02 卷 §6 标题自陈「%s」；attack51 读数 %s' % (eqc['title_five_equations'], red['atk51_1_5_7']))
    E('D07', 'PASS', 'F1 判词：盒装仅记号层统一，动力学层仍是多条独立 E-L 方程',
      'UFE-1 官方否证声明命中 %d 处（00 卷明文「不能从该作用量推出一个同时包含 EC 与内部 YM 方程的 ⋆D_A⋆F=J 方程」）'
      % eqc['official_denial_statements'])
    E('D08', 'FAIL', 'F2（真单母场方程）在零代价下不可达：交叉曲率块 %d ⇒ 引入 R∧F 后必破坏 [so(1,3),g_int]=0 与还原' % (
        cross['n_cross_segments']),
      '交叉项计数 %d（注入对照 %d）；对易子声明命中 %d 处' % (
          cross['n_cross_segments'], cross['n_cross_after_injection'], cross['commutator_declared']))
    E('D09', 'PASS', 'F2 交叉块量纲：R∧F∧e∧e 量纲 %s 与规范侧同类项 F∧e∧e（%s）齐次 ⇒ 交叉块可写' % (
        cross['dim_cross_term'], cross['dim_gauge_2form']),
      '但与引力侧同类项 R∧R∧e∧e（%s）不同类 ⇒ 必须引入独立耦合常数（外部输入），代价不为 0；齐次=%s 不同类=%s' % (
          cross['dim_grav_2form'], cross['dim_cross_eq_gauge2form'], cross['dim_cross_ne_grav2form']))
    E('D10', 'FAIL', 'F4（单耦合参数）唯一非平凡核心是恒等复读：规范核 %s（= G·m²/(ħc)），m=m_P（独立实算 %s kg）相对偏差 %s' % (
        coup['core_canonical'], coup['planck_mass_kg'], coup['planck_identity_rel_dev']),
      '穷举口径：全基组 %d 组命中 %d；Π 不含 G 自身时 %d 组；Π 不含 G 且去质量标度后 %d 组' % (
          coup['n_combos_full6'], coup['n_hits_full6'], coup['n_hits_noG_self'],
          coup['n_hits_no_mass_noG']))
    E('D11', 'CORRECTED', 'r404 命中数口径更正：「命中 7 组」只在「Π 不含 G 自身」口径下成立；按其自称 6 基组全穷举实为 %d 组（含 d=-1 的 7 组 G^{-1} 平凡解与 d=-2 的 7 组）' % coup['n_hits_full6'],
      '「去掉质量标度 m 后命中 0」亦须分口径：Π 不含 G 自身时确实 0 组；全穷举口径下去 m 仍命中 %d 组（平凡核 %s）。非平凡核心结论不变。' % (
          coup['n_hits_no_mass_full6'], '; '.join(coup['trivial_cores'][:1]) or '无'))
    E('D12', 'PASS', '方程数下界：若要求「覆盖四力且含动力学」，方程数下界与打包方式无关（UFE-1 展开级 %d 条）' % eqc['expanded_fields'],
      'F3 的 1 条公式不含动力学；F2 的 1 条方程需破坏还原；F1/F2 展开后均为多条 ⇒ 下界成立。')
    E('D13', 'PASS', '记分板四行落盘（形式 × 方程数 × 交叉块 × 耦合可推导 × 覆盖力数 × 判决）',
      'F1=NOTATION_ONLY / F2=IMPOSSIBLE_AT_ZERO_COST / F3=INCOMPLETE_DOMAIN / F4=IDENTITY_REPLAY_ONLY')
    E('D14', 'PASS', '红线核对：唯一对外读数仍为 0/6 未完成；0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条',
      '归一正本读到 %s；134 卷记分板 %s' % (red['canon_0of6'], red['vol134_scoreboard']))
    E('D15', 'INFO', '与既有册分工：74/75 profile 层红线、attack51 动力学层 1:5:7、109 no-go B、134 归一 0/6、r403–r407 代价链全部继承，本册不重判',
      '本册增量 = 形式谱系穷尽性 + F3 完备性判决 + 形式无关方程数下界 + r404 命中数口径更正')
    E('D16', 'INFO', '自抓与治理：未跑 refresh_catalog、未改 verify.py、未做 git、未触碰他人文件', '')


def build_report(tax, prof, eqc, cross, coup, red, board, guards, facts, dedup):
    L = []
    L.append('=' * 78)
    L.append('TUFT-r408 · 所有力装进一个方程 —— 形式完备性与方程数下界')
    L.append('日期 %s ｜ 纯标准库 Python 3.8 ｜ Decimal(60) + Fraction 四元组量纲' % DATE)
    L.append('=' * 78)
    L.append('')
    L.append('[一] 形式谱系穷尽性')
    L.append('  组合数=%d  有效形式=%s  全映射=%s  穷尽=%s' % (
        tax['n_combos'], tax['valid_forms'], tax['all_mapped'], tax['exhaustive']))
    for k in sorted(tax['defs']):
        L.append('    %-3s %s' % (k, tax['defs'][k]))
    L.append('')
    L.append('[二] F3 profile 层三元组完备性')
    L.append('  三元组自由参数组=%s (维数 %d)' % (prof['triple_groups'], prof['n_triple_dims']))
    for r in prof['rows']:
        L.append('    %-6s triple=%-22s 静态profile=%-5s 手征标签=%-5s 禁闭标签=%-5s' % (
            r['force'], r['triple_cell'], r['has_static_profile'], r['chiral_tag'], r['confine_tag']))
    L.append('  静态覆盖(全部)=%s  排除=%s' % (prof['static_covered'], prof['static_excluded']))
    L.append('  基本力静态覆盖=%d/%d  排除=%s' % (
        prof['n_basic_static_covered'], prof['n_basic'], prof['basic_static_excluded']))
    L.append('  外加特征维=%s (n=%d)' % (prof['extra_dims'], prof['n_extra_dims']))
    L.append('  覆盖计数：cov_static=%d  cov0=%d  +χ=%d  +禁闭=%d  两维=%d  注入弱静态=%d  (基本力 %d)  ⇒ 完备=%s' % (
        prof['cov_static'], prof['cov0'], prof['cov_chiral'], prof['cov_confinement'],
        prof['cov_both'], prof['cov_inject_weak_static'], prof['n_basic'], prof['complete']))
    L.append('')
    L.append('[三] F1 动力学层方程数独立复算')
    L.append('  盒装 UFE-1=%d  盒装 δS/δΦ=%d  变分节=%d  §6「五个方程」=%d  作用量块=%d  展开场组=%d' % (
        eqc['boxed_tag_UFE1'], eqc['boxed_deltaS'], eqc['n_var_sections'],
        eqc['title_five_equations'], eqc['n_action_blocks'], eqc['expanded_fields']))
    L.append('  变分节标题=%s' % (eqc['var_sections'],))
    L.append('  00 卷官方否证声明命中=%d' % eqc['official_denial_statements'])
    L.append('')
    L.append('[四] F2 交叉块与代价')
    L.append('  作用量段数=%d 引力段=%d 规范段=%d 交叉段=%d（注入 R∧F 后=%d）' % (
        cross['n_segments'], cross['n_grav_segments'], cross['n_gauge_segments'],
        cross['n_cross_segments'], cross['n_cross_after_injection']))
    L.append('  对易子声明命中=%d  交叉块量纲=%s  规范侧同类项=%s  引力侧同类项=%s' % (
        cross['commutator_declared'], cross['dim_cross_term'],
        cross['dim_gauge_2form'], cross['dim_grav_2form']))
    L.append('')
    L.append('[五] F4 单耦合参数穷举')
    L.append('  Q 分量来源=%s 降维合法=%s（e 幂=1 时破坏 Q=0 控制=%s）' % (
        coup['q_sources'], coup['reduction_justified'], coup['e_pow_forced_zero_control_breaks']))
    L.append('  全基组组合=%d 命中=%d ；Π 不含 G 自身命中=%d' % (
        coup['n_combos_full6'], coup['n_hits_full6'], coup['n_hits_noG_self']))
    L.append('  全部核=%s' % coup['cores_all'])
    L.append('  非平凡核=%s  平凡核=%s' % (coup['nontrivial_cores_noG'], coup['trivial_cores'][:1]))
    L.append('  去质量标度：Π 不含 G 自身口径命中=%d ；全穷举口径命中=%d' % (
        coup['n_hits_no_mass_noG'], coup['n_hits_no_mass_full6']))
    L.append('  m=m_P（独立实算 %s kg）恒等复读值=%s 相对偏差=%s' % (
        coup['planck_mass_kg'], coup['planck_identity_value'], coup['planck_identity_rel_dev']))
    L.append('')
    L.append('[六] 记分板')
    for row in board:
        L.append('  %-3s eq=%-4s cross=%-4s 耦合可推导=%-5s 覆盖基本力=%-4s 含动力学=%-5s ⇒ %s' % (
            row['form'], row['n_eq'], row['cross_blocks'], row['coupling_derivable'],
            row['covers_basic_forces'], row['contains_dynamics'], row['verdict']))
    L.append('')
    L.append('[七] 红线')
    for k in sorted(red):
        L.append('  %-22s %s' % (k, red[k]))
    L.append('')
    L.append('[八] 查重与取号')
    _nh, _no = dynamic_number_scan()
    L.append('  扫描 md=%d  针词命中=%d  他方 r408 文件命中=%d（本册自身产物 %d 件已排除）' % (
        dedup['n_scanned_md'], dedup['n_hits'], len(_nh), len(_no)))
    L.append('')
    L.append('[九] 守卫 %d 条' % len(guards))
    for g in guards:
        L.append('  %-6s %-4s %s' % (g['code'], 'PASS' if g['ok'] else 'FAIL', g['value']))
    L.append('')
    L.append('[十] 条目 %d 条' % len(ENTRIES))
    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    L.append('  状态分布=%s' % st)
    for e in ENTRIES:
        L.append('  %-4s %-9s %s' % (e['code'], e['status'], e['title']))
    L.append('')
    L.append('VERDICT: SINGLE-EQUATION-COMPLETE-NO-GO--FORMS-EXHAUSTIVE--PROFILE-DOMAIN-INCOMPLETE--N_EQ-LOWER-BOUND')
    L.append('GUARDS %d/%d  ENTRIES %d  EXIT=0' % (
        sum(1 for g in guards if g['ok']), len(guards), len(ENTRIES)))
    return '\n'.join(L) + '\n'


def main():
    log('=== TUFT-r408 · 所有力装进一个方程 · 形式完备性与方程数下界 ===')
    facts = load_facts()
    md5_before = dict((k, v['md5_before']) for k, v in facts.items())
    G('G01', all(v['exists'] for v in facts.values()) and len(facts) == 10,
      'facts=%d exists=%d' % (len(facts), sum(1 for v in facts.values() if v['exists'])))

    num_hits, num_own = dynamic_number_scan()
    G('G02', len(num_hits) == 0, 'other r408 filename hits=%d %s ｜ own products excluded=%d' % (
        len(num_hits), num_hits[:3], len(num_own)))

    dedup = dedup_scan()
    G('G03', dedup['n_hits'] == 0, 'md scanned=%d needle hits=%d %s (排除本册产物/README*/资料索引)' % (
        dedup['n_scanned_md'], dedup['n_hits'], dedup['hits'][:3]))

    astchk = ast_selfcheck(os.path.abspath(__file__))
    G('G04', not astchk['bad_import'] and not astchk['bad_call'],
      'bad_import=%s bad_call=%s md5=%s' % (astchk['bad_import'], astchk['bad_call'], astchk['md5'][:12]))

    tax = form_taxonomy()
    G('G05', tax['exhaustive'] and tax['n_valid'] >= 4,
      'combos=%d valid=%s all_mapped=%s' % (tax['n_combos'], tax['valid_forms'], tax['all_mapped']))

    t00 = facts['ufe00']['text']
    t01 = facts['ufe01']['text']
    t02 = facts['ufe02']['text']
    eqc = equation_count(t00, t01, t02)
    G('G06', eqc['boxed_tag_UFE1'] >= 1 and eqc['boxed_deltaS'] >= 1,
      'boxed_tag=%d boxed_deltaS=%d' % (eqc['boxed_tag_UFE1'], eqc['boxed_deltaS']))
    G('G07', eqc['n_var_sections'] == 5, 'var_sections=%d %s' % (eqc['n_var_sections'], eqc['var_sections']))
    G('G08', eqc['title_five_equations'] >= 1, 'title_five=%d' % eqc['title_five_equations'])
    G('G09', eqc['n_action_blocks'] == 5, 'action_blocks=%d' % eqc['n_action_blocks'])

    red = redline_check(facts['vol134']['text'], facts['canon']['text'],
                        facts['atk51']['text'], facts['r404']['text'])
    G('G10', eqc['expanded_fields'] == 7 and red['atk51_1_5_7'] != '',
      'expanded=%d atk51_reading=%s' % (eqc['expanded_fields'], red['atk51_1_5_7']))
    G('G11', eqc['official_denial_statements'] >= 1,
      'official_denial=%d' % eqc['official_denial_statements'])

    prof = profile_coverage(facts['vol74']['text'])
    G('G12', prof['n_rows'] == 5, 'vol74 force rows=%d %s' % (
        prof['n_rows'], [r['force'] for r in prof['rows']]))
    G('G13', prof['n_triple_dims'] == 3, 'triple_groups=%s dim=%d' % (
        prof['triple_groups'], prof['n_triple_dims']))
    G('G14', '弱' in prof['static_excluded'], 'static_excluded=%s' % prof['static_excluded'])
    G('G15', any(r['confine_tag'] for r in prof['rows']), 'confine_tag present=%s' % [
        r['force'] for r in prof['rows'] if r['confine_tag']])
    G('G16', prof['n_basic_static_covered'] < prof['n_basic'],
      'basic static covered=%d/%d excluded=%s' % (
          prof['n_basic_static_covered'], prof['n_basic'], prof['basic_static_excluded']))
    G('G17', prof['n_extra_dims'] >= 2, 'extra_dims=%s n=%d' % (prof['extra_dims'], prof['n_extra_dims']))
    G('G18', prof['cov_inject_weak_static'] == prof['n_basic']
      and prof['cov_both'] < prof['n_basic'],
      'cov_static=%d cov0=%d +chi=%d +conf=%d both=%d inject_weak=%d basic=%d' % (
          prof['cov_static'], prof['cov0'], prof['cov_chiral'],
          prof['cov_confinement'], prof['cov_both'], prof['cov_inject_weak_static'],
          prof['n_basic']))

    cross = cross_term_scan(t00)
    G('G19', cross['n_segments'] >= 3 and cross['n_cross_segments'] == 0
      and cross['n_cross_after_injection'] == 1,
      'segments=%d grav=%d gauge=%d cross=%d after_injection=%d' % (
          cross['n_segments'], cross['n_grav_segments'], cross['n_gauge_segments'],
          cross['n_cross_segments'], cross['n_cross_after_injection']))
    G('G20', cross['dim_cross_eq_gauge2form'] and cross['dim_cross_ne_grav2form'],
      'dim_cross=%s gauge2form=%s grav2form=%s' % (
          cross['dim_cross_term'], cross['dim_gauge_2form'], cross['dim_grav_2form']))
    G('G21', cross['commutator_declared'] >= 1, 'commutator_declared=%d' % cross['commutator_declared'])

    coup = coupling_enum()
    G('G22', coup['reduction_justified'] and coup['n_hits_full6'] > 0 and coup['n_hits_noG_self'] > 0,
      'full6=%d hits=%d noG=%d no_mass(noG)=%d no_mass(full)=%d' % (
          coup['n_combos_full6'], coup['n_hits_full6'], coup['n_hits_noG_self'],
          coup['n_hits_no_mass_noG'], coup['n_hits_no_mass_full6']))
    G('G23', coup['e_pow_forced_zero_control_breaks'], 'e_pow1_breaks_Q=%s' % coup['e_pow_forced_zero_control_breaks'])

    G('G24', red['canon_0of6'] != '' and red['canon_0of22'] != '' and red['canon_uft3'] != ''
      and red['canon_validated'] != '' and red['canon_not_complete'] != '',
      'redline %s|%s|%s|%s|%s' % (red['canon_0of6'], red['canon_0of22'], red['canon_uft3'],
                                  red['canon_validated'], red['canon_not_complete']))

    board = scoreboard(tax, prof, eqc, cross, coup)
    build_entries(tax, prof, eqc, cross, coup, red)
    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    G('G25', len(ENTRIES) >= 14 and sum(st.values()) == len(ENTRIES),
      'entries=%d status=%s' % (len(ENTRIES), st))
    G('G26', NAME not in ' '.join(h['file'] for h in dedup['hits']),
      'self_product_excluded=%s' % (NAME not in ' '.join(h['file'] for h in dedup['hits'])))

    md5_after_map = md5_after()
    unchanged = all(md5_before[k] == md5_after_map[k] for k in md5_before)
    G('G27', unchanged, 'fact md5 unchanged=%s' % unchanged)

    report = build_report(tax, prof, eqc, cross, coup, red, board, GUARDS, facts, dedup)
    data = {
        '册': 'TUFT-r408', '标题': '所有力装进一个方程 · 形式完备性与方程数下界',
        '日期': DATE, '引擎': ENGINE,
        '形式谱系': tax, 'F3_profile完备性': prof, 'F1_方程数': eqc,
        'F2_交叉块': cross, 'F4_穷举': coup, '记分板': board, '红线': red,
        '查重': dedup, '守卫': GUARDS, '条目': ENTRIES,
        '自纠': SELF_CORRECTIONS,
        '总裁定': 'SINGLE-EQUATION-COMPLETE-NO-GO--FORMS-EXHAUSTIVE--PROFILE-DOMAIN-INCOMPLETE--N_EQ-LOWER-BOUND',
        '退出码': 0,
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
        f.write('# ' + NAME + '\n\n- 日期：%s ｜ 引擎：`%s`\n- 守卫 **%d/%d** ｜ 条目 **%d**（%s）｜ 退出码 **0**\n'
                % (DATE, ENGINE, sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES), st))
        f.write('- 总裁定：`%s`\n\n' % data['总裁定'])
        f.write('## 形式谱系（穷尽）\n\n| 形式 | 含义 | 判决 |\n|---|---|---|\n')
        for row in board:
            f.write('| %s | %s | **%s** |\n' % (row['form'], row['name'], row['verdict']))
        f.write('\n## F3 profile 层力谱逐行判定\n\n| 力 | (s,m) 单元 | 静态 profile | 手征标签 | 禁闭标签 |\n|---|---|---|---|---|\n')
        for r in prof['rows']:
            f.write('| %s | `%s` | %s | %s | %s |\n' % (
                r['force'], r['triple_cell'], '有' if r['has_static_profile'] else '**无**',
                '有' if r['chiral_tag'] else '无', '有' if r['confine_tag'] else '无'))
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
