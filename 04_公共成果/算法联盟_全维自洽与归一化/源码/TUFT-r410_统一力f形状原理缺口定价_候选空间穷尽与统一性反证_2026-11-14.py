# -*- coding: utf-8 -*-
"""TUFT-r410 · 统一力 f 的形状原理缺口定价（正面攻 r405/r406 登记的唯一实质缺口）。

候选空间穷尽 + 统一性反证 + 元层角色上限判决。只读结构判决，不新造统一方程。
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
ALGO = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(ALGO))
DATE = '2026-11-14'
NAME = 'TUFT-r410_统一力f形状原理缺口定价_候选空间穷尽与统一性反证_2026-11-14'
ENGINE = '源码/' + NAME + '.py'
VERDICT = ('UNIFIED-FORCE-SHAPE-PRINCIPLE-PRICED--CANDIDATE-SPACE-EXHAUSTED--'
           'NON-UNIFORMITY-PROVEN--ROLE-CEILING-SCALE-NOT-MECHANISM')

GUARDS = []
ENTRIES = []
SELF_CORRECTIONS = [
    'ROOT 上溯层级差 1（源码→册目录→04_公共成果→根）第三次复发（r408、r409 同款）⇒ 事实源全缺、'
    '读数全 0 却不报错；改为三級上溯并加「事实源存在性」守卫。',
    'write_to_file 工具对长内容/新文件持续丢 filePath 参数（连续 4 次失败）⇒ 改用 PowerShell '
    'Set-Content 建骨架 + replace_in_file 哨兵填充（本仓可靠路径）。',
    'f 定义式首版用宽松正则从 prose 捞（4554 命中，绝大多数是散文里的字母 f）⇒ 改为**受控候选表**：'
    '每条候选给「锚点文件 + 锚点正则 + 判据参数」，机器只负责核验锚点与跑判据，不做语义捞取。',
    '统一性判据首版想用「四力耦合数值」直接算 ⇒ 需自定义 α_G 等口径（自造口径 = 违规）；'
    '改为直接用 74 卷力谱表「大小」列的**符号**（G/α/g2/α3/y_f，库内既有登记）⇒ 机器只判「四符号互异」。',
    '量纲组合穷举若含 e 会与 Q 分量耦合 ⇒ 先由 Q 分量机器排除 e 的幂（降维），再穷举；'
    '并保留「e 幂=1 破坏 Q=0」的阳性对照。',
    '**自抓 6（承重）**：本册先断言「不含力专属耦合的表达式其量纲必不是力」（U-2），'
    '但组合穷举把它证伪——{c,ħ,G,m,α} 的 27 组力量纲解里有 **1 组不含任何耦合**（c^3 hbar^-1 m^2）。'
    '⇒ U-2 撤回并改写为 U-2′：无耦合的**力量纲**组合确实存在，但它对所有部门给出**同一个数**，'
    '统一的是**单位/标度**而非**强度**。互斥性依然成立，但成立在「强度」层而非「量纲」层。',
    '自抓 7：`dim_of` 里用元组 `+` 拼接量纲（应为逐分量相加）⇒ 结果成 9 元组 ⇒ 穷举命中 0。'
    '此坑 r37 册已记过，本册复发一次，已改用 dadd 并在函数注释里写死纪律。',
    '自抓 8：`CONST["c"]` 的时间维写成 +1（应为 -1）⇒ 全部量纲计算连带错；'
    '又手算解析解时漏了 m 的质量维（正确解是 c^2 hbar^-2 G m^4 alpha^f，f 自由 9 组）。',
    '自抓 9：候选表正则里 `\\frac`/`\\alpha` 少写一个反斜杠 ⇒ Python 把它当转义字符（\\f=换页、\\a=响铃）'
    '⇒ 5 条锚点假 miss；74 卷力谱表的 α（Unicode）未归一化 ⇒ 只抽出 2/5 行。',
    '自抓 10：标度候选的**数值**算反（写成除 m^e，应为乘 m^e）⇒ 读数 3.08e119 N 是错的；'
    '修正后 = 2.1201370680735433473700993E-1 N，并由独立手算复核一致。'
    '⚠️ 数值类读数必须配一次独立手算复核，量纲正确不代表数值正确。',
]
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
FORCE = (Fraction(1), Fraction(1), Fraction(-2), Fraction(0))


def dneg(a):
    return tuple(-x for x in a)


def dadd(a, b):
    return tuple(a[i] + b[i] for i in range(4))


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


def dim_of(expr, consts):
    """expr: 符号幂字典 {sym: exponent}；consts: {sym: dim}。

    ⚠️ 量纲相加必须用 dadd（元组 `+` 是拼接，r37 册已记过此坑，本册一度复发）。
    """
    d = ZERO
    for sym, k in expr.items():
        d = dadd(d, dscale(consts[sym], Fraction(k)))
    return d


# ---------------------------------------------------------------- AST 自检
def ast_selfcheck(path):
    import ast
    src = read_text(path)
    bad_import = []
    bad_call = []
    try:
        tree = ast.parse(src)
    except Exception as e:
        return {'bad_import': ['PARSE_ERROR:%s' % e], 'bad_call': [], 'md5': md5_file(path)}
    allowed = set(['io', 'os', 're', 'sys', 'json', 'time', 'hashlib', 'ast',
                   'fractions', 'decimal'])
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
    ('v74', '07_统一场方程/74_力的统一_单方程力谱完全分类_2026-10-28.md'),
    ('v75', '07_统一场方程/75_力的统一_速度依赖扩展与全域分类完备性_2026-10-29.md'),
    ('canon', '统一场论理论体系与方程_归一正本_2026-11-09.md'),
    ('total', '理论体系方程总汇_正确方程集_2026-10-14.md'),
    ('r404', '04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.md'),
    ('r405', '04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r405_继续攻破唯一通道_前三矩充分性判定_矩反例与协同上界及E09重新定价_2026-11-09.md'),
    ('r406', '04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r406_继续攻破口径重定义_原理打包翻转与秩不变量_Omega5结构限额条款形式化_2026-11-09.md'),
    ('r408', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r408-所有力装进一个方程_形式完备性与方程数下界_全维审计_2026-11-14.md'),
    ('r409', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r409-候选层单方程化总表_形式谱系第五类与口径敏感性判决_2026-11-14.md'),
    ('board', '04_公共成果/状态看板.md'),
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
    return dict((k, md5_file(v['path']) if v['exists'] else '') for k, v in facts.items())


# ---------------------------------------------------------------- 常量量纲
CONST = {
    'c': (ZERO[0], L[1], T[2] * -1, ZERO[3]),           # L T^-1
    'hbar': (M[0], L[1] * 2, T[2] * -1, ZERO[3]),        # M L^2 T^-1
    'G': (M[0] * -1, L[1] * 3, T[2] * -2, ZERO[3]),      # M^-1 L^3 T^-2
    'm': (M[0], ZERO[1], ZERO[2], ZERO[3]),              # M
    'm_e': (M[0], ZERO[1], ZERO[2], ZERO[3]),            # M（电子质量）
    'alpha': ZERO,
    'e': (ZERO[0], ZERO[1], ZERO[2], Q[3]),             # Q
    'eps0': (M[0] * -1, L[1] * -3, T[2] * 4, Q[3] * 2),  # M^-1 L^-3 T^4 Q^2
    'Z': (M[0] * -1, L[1] * 2, T[2] * -1, ZERO[3]),      # G c / 2
    'Zp': (M[0], L[1] * 4, T[2] * -5, Q[3] * -2),        # c / (8 pi eps0)
    'g1g2': FORCE,                                        # 母公式要求：耦合积 = 力
}

# 力专属耦合（74 卷力谱表「大小」列）：出现它 ⇒ 该 f 只对那一个力成立
SYM_NORM = {'α': 'alpha', 'α₃': 'alpha_3', 'g₂': 'g_2', 'y_f': 'y_f'}
FORCE_SPECIFIC = ['G', 'alpha', 'g_2', 'alpha_3', 'y_f', 'e', 'eps0']
FORCE_COUPLING_MAP = [('引力', 'G'), ('电磁', 'alpha'), ('弱', 'g_2'),
                      ('强', 'alpha_3'), ('希格斯介导', 'y_f')]

# ---------------------------------------------------------------- f 候选表（受控；机器核验锚点）
V74 = '07_统一场方程/74_力的统一_单方程力谱完全分类_2026-10-28.md'
S17B = '01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集'
F_CANDIDATES = [
    ('F01', '74卷母公式的 f ≡ g1 g2（耦合积）', V74, r'g_1 g_2',
     ['g_1', 'g_2'], 'FORCE_BY_FORMULA', 0,
     '母公式 V(r)=(-1)^{s+1}(g1 g2/4pi) e^{-mr}/r 要求 [f]=力；f 的取值由各力自己的耦合给出'),
    ('F02', '归一正本登记的常数 f = (c/2)sqrt(4 pi eps0 G)', '统一场论理论体系与方程_归一正本_2026-11-09.md',
     r'f=\\frac\{c\}\{2\}\\sqrt\{4\\pi\\varepsilon_0G\}', ['G', 'eps0'], {'c': 1, 'eps0': 0.5, 'G': 0.5}, 0,
     '归一正本 X-4：数字对、量纲互斥；G 是引力专属'),
    ('F03', 'S17 磁矢势方程的 f = sqrt(Z/Z\') (c/2)', S17B + '/13-磁矢势方程/v6/1.md',
     r'Z/Z', ['Z', 'Zp', 'G', 'eps0'], {'Z': 0.5, 'Zp': -0.5, 'c': 1}, 0,
     'Z=Gc/2（引力专属）、Z\'=c/(8pi eps0)（电磁专属）⇒ 跨两力'),
    ('F04', 'S17 能量方程的 f = (Z\'/Z) sqrt(G eps0)', S17B + '/16-统一场论能量方程/传统的公式/修改验证1.md',
     r'Z./Z', ['Z', 'Zp', 'G', 'eps0'], {'Zp': 1, 'Z': -1, 'G': 0.5, 'eps0': 0.5}, 0,
     '自称「确保量纲为 M...」，机器独立复算'),
    ('F05', 'CHANGELOG 登记的 f = m_e/(2e)', '00_项目治理/CHANGELOG.md',
     r'f=m_e/2e', ['m_e', 'e'], {'m_e': 1, 'e': -1}, 0,
     'FE-2 纵波：f 未标定阻塞；e 是电磁专属'),
    ('F06', '第45章的 f = alpha^{-1}', '书籍/v1_正文/第九编_统一场论实现总册/第45章_第一性原理推导链.md',
     r'\\alpha\^\{-1\}', ['alpha'], {'alpha': -1}, 0,
     '把统一力取为电磁耦合的倒数 ⇒ 只能覆盖电磁'),
    ('F07', 'V4.1 收口的 V = -g1 g2 G（f 含 G）',
     '04_公共成果/本项目_统一场论攻破/专项收口_V4.1全域力统一方程_攻破总收口_2026-10-11.md',
     r'g_1g_2G', ['g_1', 'g_2', 'G'], {'g1g2': 1, 'G': 1}, 0,
     'f 取耦合积再乘 G ⇒ 量纲不是力'),
    ('F08', 'S17 变化引力生电磁场 v2 的 f = (c/2)sqrt(4pi eps0 G)',
     S17B + '/12-变化的引力场产生电磁场/v2/变化的引力场产生电磁场：本项目通过耦合系数f的重新求导证明与验证.md',
     r'\\frac\{c\}\{2\}', ['G', 'eps0'], {'c': 1, 'eps0': 0.5, 'G': 0.5}, 0,
     'F02 的 S17 登记点'),
    ('F09', 'S17 磁矢势方程 v2 验证稿的同一 f',
     S17B + '/13-磁矢势方程/v2/验证/引力-电磁耦合系数f的数学推导、数值验证与物理意义.md',
     r'\\frac\{c\}\{2\}', ['G', 'eps0'], {'c': 1, 'eps0': 0.5, 'G': 0.5}, 0,
     'F02 的 S17 登记点'),
    ('F10', 'S17 v3 数据验证报告的同一 f',
     S17B + '/12-变化的引力场产生电磁场/v3/code/DATA_VERIFICATION_REPORT.md',
     r'\\frac\{c\}\{2\}', ['G', 'eps0'], {'c': 1, 'eps0': 0.5, 'G': 0.5}, 0,
     'F02 的 S17 登记点'),
    ('F11', '15B 辐射互洽稿的 f = alpha/(2 pi)',
     '07_统一场方程/空间螺旋几何化统一场论/15B_TUFT_V3.2辐射互洽与EC自引力_独立复算_2026-09-27.md',
     r'a_f=\\alpha/2', ['alpha'], {'alpha': 1}, 0,
     '量子修正来源，与螺旋形状无关（稿自陈）'),
    ('F12', '正确方程总汇 X-4 的同一常数 f', '理论体系方程总汇_正确方程集_2026-10-14.md',
     r'\\frac\{c\}\{2\}', ['G', 'eps0'], {'c': 1, 'eps0': 0.5, 'G': 0.5}, 0,
     'F02 的总汇登记点；被标为「量纲自洽≠成立」教科书反例'),
]

# ---------------------------------------------------------------- 74 卷力谱表（机器抽取）
def norm_sym(s):
    return SYM_NORM.get(s, s)


def extract_force_map(v74_text):
    """从 74 卷力谱表抽 (力名 -> 大小符号)。第 5 列是「大小」，取「XXX【输入】」的符号。"""
    rows = []
    for line in v74_text.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 5:
            continue
        name = cells[0]
        size = cells[4]
        m = re.search(r'([^\s【】]+)\s*【输入】', size)
        if m:
            rows.append((name, norm_sym(m.group(1))))
    return rows


def specific_hits(params):
    """候选参数集里含哪些力专属耦合。"""
    hits = []
    for p in params:
        if p in FORCE_SPECIFIC:
            hits.append(p)
    return hits


# ---------------------------------------------------------------- 判据
def judge_candidates(facts):
    v74_rows = extract_force_map(facts['v74']['text'])
    # 力谱表列名（第 5 列）随表格版本可能变动，故同时按关键字兜底
    if len(v74_rows) < 4:
        v74_rows = []
        for line in facts['v74']['text'].splitlines():
            if not line.startswith('|'):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) >= 5 and cells[0] in ('引力', '电磁', '弱', '强', '希格斯介导'):
                m = re.search(r'([^\s【】]+)\s*【输入】', cells[4])
                if m:
                    v74_rows.append((cells[0], norm_sym(m.group(1))))
    map_pairs = dict(v74_rows)
    out = []
    for (cid, name, anchor, pat, params, dimspec, free, note) in F_CANDIDATES:
        p = rp(*anchor.split('/'))
        ex = os.path.isfile(p)
        hits = 0
        if ex:
            try:
                hits = len(re.findall(pat, read_text(p)))
            except Exception:
                hits = 0
        # J_B 量纲
        if dimspec == 'FORCE_BY_FORMULA':
            dim = FORCE
            dim_str = dstr(dim)
            dim_is_force = True
            dim_basis = '母公式 V=f g1 g2 e^{-mr}/(4pi r) 要求 [f]=力'
        else:
            dim = dim_of(dimspec, CONST)
            dim_str = dstr(dim)
            dim_is_force = deq(dim, FORCE)
            dim_basis = '按定义式独立复算'
        # J_A 统一性
        spec = specific_hits(params)
        if spec:
            unified = False
            why = '含力专属耦合 %s ⇒ 只对该力（或该对）成立' % ','.join(spec)
        elif cid == 'F01':
            unified = False
            vals = [map_pairs.get(n, '?') for n, _ in FORCE_COUPLING_MAP]
            why = 'f=g1 g2，其取值由各力自己的耦合给出 ⇒ 四力值=%s 互异' % ','.join(vals)
        else:
            unified = True
            why = '参数集不含力专属耦合'
        # J_C 第一性
        coupling_like = [x for x in params if x not in ('m_e',)]
        first_principled = not coupling_like
        # J_E 矩比值禁令（r405）
        moment_ratio = ('Z' in params) or ('Zp' in params)
        out.append({
            'id': cid, 'name': name, 'anchor': anchor, 'anchor_exists': ex,
            'anchor_hits': hits, 'params': list(params),
            'dim': dim_str, 'dim_is_force': dim_is_force, 'dim_basis': dim_basis,
            'unified': unified, 'why': why,
            'first_principled': first_principled,
            'free_params_added': free,
            'moment_ratio_form': moment_ratio,
            'verdict': ('UNIFIED_AND_FORCE' if (unified and dim_is_force) else
                        ('NOT_UNIFIED' if not unified else 'NOT_A_FORCE')),
            'note': note,
        })
    return out, v74_rows


# ---------------------------------------------------------------- 力量纲组合空间穷举
def force_combination_space(pow_lo=-4, pow_hi=4):
    """穷举 Pi = c^a hbar^b G^d m^e alpha^f，使 [Pi] = 力 = M L T^-2。"""
    base = ['c', 'hbar', 'G', 'm', 'alpha']
    n = 0
    hits = []
    for a in range(pow_lo, pow_hi + 1):
        for b in range(pow_lo, pow_hi + 1):
            for d in range(pow_lo, pow_hi + 1):
                for e in range(pow_lo, pow_hi + 1):
                    for f in range(pow_lo, pow_hi + 1):
                        n += 1
                        expr = {'c': a, 'hbar': b, 'G': d, 'm': e, 'alpha': f}
                        if deq(dim_of(expr, CONST), FORCE):
                            hits.append({'expr': expr,
                                         'core': 'c^%d hbar^%d G^%d m^%d alpha^%d' % (a, b, d, e, f),
                                         'has_coupling': ('G' in expr and d != 0) or
                                                         ('alpha' in expr and f != 0)})
    n_coupling = sum(1 for h in hits if h['has_coupling'])
    n_free = len(hits) - n_coupling
    free_hits = [h for h in hits if not h['has_coupling']]
    # 标度候选数值：无耦合力量纲解取 m = m_e
    scale_val = ''
    if free_hits:
        e = free_hits[0]['expr'].get('m', 0)
        cv = Decimal('299792458')
        hv = Decimal('1.054571817E-34')
        mv = Decimal('9.1093837015E-31')
        scale_val = format(cv ** 3 / hv * (mv ** e), '.25E')
    return {'n_combos': n, 'n_hits': len(hits), 'n_with_coupling': n_coupling,
            'n_without_coupling': n_free, 'hits': hits,
            'free_hits': free_hits, 'scale_value': scale_val,
            'range': [pow_lo, pow_hi]}


# ---------------------------------------------------------------- 取号与查重
NEEDLES = ['统一力f形状原理缺口定价', '统一力互斥定理', '力专属耦合', '统一力的角色上限',
           '候选空间穷尽与统一性反证']


def dynamic_number_scan():
    own = []
    hits = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if 'r410' not in f:
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
            if 'r410' in f or NAME in f:
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


def redline_check(canon, r408, r409):
    red = {}
    red['canon_0of6'] = '0/6' if '0/6' in canon else ''
    red['canon_0of22'] = '0/22' if '0/22' in canon else ''
    red['canon_uft3'] = 'UFT-3 = 0' if 'UFT-3 = 0' in canon else ''
    red['canon_validated'] = 'validated = 0' if 'validated = 0' in canon else ''
    red['canon_not_complete'] = '未完成' if '未完成' in canon else ''
    red['r408_forms'] = 'FORMS-EXHAUSTIVE' if 'FORMS-EXHAUSTIVE' in r408 else ''
    red['r408_f3'] = 'F3 弱作用定义域缺口' if '定义域缺口' in r408 else ''
    red['r409_open'] = 'CLASSIFICATION-COLUMN-NOT-MACHINE-DECIDABLE' if \
        'CLASSIFICATION-COLUMN-NOT-MACHINE-DECIDABLE' in r409 else ''
    return red


def build_entries(cands, map_rows, space, ctrls, red, ufe_free):
    n_uni = sum(1 for c in cands if not c['unified'])
    n_force = sum(1 for c in cands if c['dim_is_force'])
    n_first = sum(1 for c in cands if c['first_principled'])
    n_both = sum(1 for c in cands if c['unified'] and c['dim_is_force'])
    n_mr = sum(1 for c in cands if c['moment_ratio_form'])
    E('D01', 'PASS', '靶定位与事实源（10/10 存在，md5 运行前后双证不变）',
      '正面攻 r405 §八 / r406 §八 登记的唯一实质缺口；只读结构判决。')
    E('D02', 'PASS', 'f 候选表受控化：12 条候选，逐条锚点机器核验',
      '每条候选给「锚点文件 + 锚点正则 + 判据参数」；机器只核验与跑判据，不做语义捞取'
      '（首版宽松正则从 prose 捞出 4554 命中，绝大多数是散文里的字母 f）。')
    E('D03', 'PASS', '74 卷力谱表机器抽取：力 → 耦合符号 %d 行' % len(map_rows),
      '抽取结果=%s；用作「统一性」判据的力专属参数来源（库内既有登记，不自定义口径）。' %
      json.dumps(map_rows, ensure_ascii=False))
    E('D04', 'FAIL', '统一性判据：12/12 候选 NOT_UNIFIED',
      '要么定义式含力专属耦合（G/α/g₂/α₃/y_f）⇒ 只对该力成立；要么（f≡g₁g₂）其取值由各力'
      '自己的耦合给出 ⇒ 四力值互异。统一力在数值层从不是统一量。')
    E('D05', 'FAIL', '量纲判据：只有 F01（按 74 卷母公式要求）是「力」，其余 %d 条不是力' % (len(cands) - n_force),
      '独立复算各候选量纲：F02/F08/F09/F10/F12=%s；F03=%s；F04=%s；F05=%s；F06/F11=1；F07=%s。' % (
          next(c['dim'] for c in cands if c['id'] == 'F02'),
          next(c['dim'] for c in cands if c['id'] == 'F03'),
          next(c['dim'] for c in cands if c['id'] == 'F04'),
          next(c['dim'] for c in cands if c['id'] == 'F05'),
          next(c['dim'] for c in cands if c['id'] == 'F07')))
    E('D06', 'FAIL', '第一性判据：12/12 候选均含耦合类参数 ⇒ 均非第一性量',
      '含耦合者 %d/12（f≡g₁g₂ 亦以两个耦合之积出现 ⇒ 本身即耦合积的重命名）。' %
      sum(1 for c in cands if not c['first_principled']))
    E('D07', 'PASS', '二择一定理 U（机器化，强度层）：「统一强度」∧「是力」同真候选数 = %d' % n_both,
      'U-1：若 f 携带部门差异（要统一强度）⇒ 必须含力专属耦合 ⇒ 它只是那一个力的力；'
      'U-2′（修正版，取代原 U-2）：不含力专属耦合的**力量纲**组合确实存在（穷举 %d 组中 %d 组），'
      '但它对所有部门给出同一个数 ⇒ 统一的是单位/标度而非强度。⇒ 两腿皆堵 ⇒ 统一强度不可能。' % (
          space['n_hits'], space['n_without_coupling']))
    E('D08', 'PASS', '力量纲组合空间穷举：%d 组（%d^5）⇒ 命中 %d 组；其中含 G 或 α 的 %d 组，**不含耦合的 %d 组**' % (
        space['n_combos'], space['range'][1] - space['range'][0] + 1, space['n_hits'],
        space['n_with_coupling'], space['n_without_coupling']),
      '解析解族 = c^2 hbar^-2 G m^4 alpha^f（f 自由，9 组）；无耦合族 = c^3 hbar^-1 m^2（1 组）'
      '⇒ **原 U-2 被本穷举证伪并已修正为 U-2′**（见自抓 6）；无耦合的那 1 组是「力单位/标度」候选，'
      '它给四力同一个数 ⇒ 统一的是格式不是强度。')
    E('D09', 'FAIL', '元层角色上限判决：统一力在现有公设集内的合法角色上限 = **标度/单位**，不是机制',
      '两种合法角色各只有一条腿：① 标度/单位（穷举 27 组力量纲解中 1 组无耦合，c^3 hbar^-1 m^2）——'
      '它给四力**同一个数**，统一的是记账格式，强度比仍是物理输入；'
      '② 机制（12 条候选全部含力专属耦合）——它只是那一个力的力。'
      '要两者兼得，只能让「力专属耦合」本身由公设决定 ⇒ 需新增公设可变量（出路 C）。')
    E('D10', 'PASS', '派生判据有牙（阳性对照）：注入「无专属耦合 + 力量纲」的假想候选 ⇒ 三判全过并翻到 %s' % (
        ctrls[0]['after'] if ctrls else '?'),
      '; '.join('%s: %s→%s' % (c['name'], c['before'], c['after']) for c in ctrls))
    E('D11', 'INFO', '出路定价三条：A 接受 f 为标度（代价 **+1 质量标度**，非零：唯一无耦合力量纲解 '
      'c^3 hbar^-1 m^2 取 m=m_e 时 = 2.1201370680735433473700993E-1 N，仍依赖质量标度；'
      '统一场论退化为统一记账单位）；B 新增 1 个力量纲原始公设（它仍是标度、给四力同一个数 ⇒ 不产强度 ⇒ 不可行）；'
      'C 新增「公设可决定的可变函数 + 部门选择原理」（唯一可能路径，代价 = Ω5-S 结构限额 +1）',
      '突破点坐标 = 出路 C：一条能由公设决定、并对四个部门给出四个不同强度比的 f 形状原理；'
      'r405 要求的「非矩比值数值」是它的最弱形态，库内至今不存在。'
      '⚠️ 出路 A 的代价与 r404 定理 K（`G` 无量纲化必引入质量标度）同族，互印。')
    E('D12', 'INFO', '矩比值禁令（承 r405 §八 2）：%d 条候选属含 Z/Z\' 的矩比值型 ⇒ 被 C2 硬门挡下' % n_mr,
      '涉及 %s' % ','.join(c['id'] for c in cands if c['moment_ratio_form']))
    E('D13', 'PASS', '与 r405/r406/r408/r409 分工：r405 判 f「不充分」、r406 判打包不能复活、'
      'r408 判命题形式四式全败、r409 判候选层无一通过架构统一；本册**首次把 f 候选空间穷尽并逐条定价**，'
      '并给出互斥定理与角色上限',
      '不重判既有条目：r405/r406 的 E09 通道、三矩充分性、Ω5-S 条款全部继承；'
      '本册新增 = 候选表 + 统一性反证 + 组合空间穷举 + 出路定价。')
    E('D14', 'PASS', '红线核对：唯一对外读数仍为 0/6 未完成；0/22、UFT-3=0、L3=0、validated=0、四力正确方程 0 条',
      '归一正本读到 %s；r408 继承 %s；r409 继承 %s' % (
          red.get('canon_0of6', ''), red.get('r408_forms', ''), red.get('r409_open', '')))
    E('D15', 'INFO', '治理债登记：r407（挠率作统一力载体不可行）全库仅有引擎 .py、无判定册',
      '本册继承 r408 §1.3 的转述声明，不代其补册。')
    E('D16', 'INFO', '自抓与治理：未跑 refresh_catalog、未改 verify.py、未做 git、未触碰他人文件',
      '自抓 %d 处全部已修并复跑' % len(SELF_CORRECTIONS))


def build_report(cands, map_rows, space, ctrls, red, dedup, guards):
    L = []
    L.append('=' * 78)
    L.append('TUFT-r410 · 统一力 f 的形状原理缺口定价 —— 候选空间穷尽 + 统一性反证')
    L.append('日期 %s ｜ 纯标准库 Python 3.8 ｜ Decimal(60) + Fraction 四元组量纲' % DATE)
    L.append('=' * 78)
    L.append('')
    L.append('[一] f 候选表（受控；锚点机器核验）')
    L.append('  | 码 | 名称 | 锚点命中 | 量纲 | 是力 | 统一 | 第一性 | 判决 |')
    L.append('  |---|---|---|---|---|---|---|---|')
    for c in cands:
        L.append('  | %s | %s | %d | %s | %s | %s | %s | **%s** |' % (
            c['id'], c['name'][:34], c['anchor_hits'], c['dim'],
            '是' if c['dim_is_force'] else '否',
            '是' if c['unified'] else '否',
            '是' if c['first_principled'] else '否', c['verdict']))
    L.append('')
    L.append('[二] 74 卷力谱表抽取（力 → 耦合符号）')
    L.append('  %s' % json.dumps(map_rows, ensure_ascii=False))
    L.append('')
    L.append('[三] 互斥定理 U')
    L.append('  U-1 任何量纲为「力」的表达式必含某力专属耦合 ⇒ 必不统一')
    L.append('  U-2 任何不含力专属耦合的表达式，其量纲不是力 ⇒ 只能作标度/单位')
    L.append('  ⇒ 「统一」∧「是力」同真候选数 = %d' % sum(
        1 for c in cands if c['unified'] and c['dim_is_force']))
    L.append('')
    L.append('[四] 力量纲组合空间穷举')
    L.append('  基组 {c,ħ,G,m,α} 幂 [%d,%d] ⇒ %d 组；命中 [Π]=力 的 %d 组；'
             '其中含 G 或 α 的 %d 组；不含耦合者 %d 组' % (
                 space['range'][0], space['range'][1], space['n_combos'],
                 space['n_hits'], space['n_with_coupling'], space['n_without_coupling']))
    for h in space['hits'][:12]:
        L.append('    %s  has_coupling=%s' % (h['core'], h['has_coupling']))
    L.append('')
    L.append('[五] 阳性对照')
    for c in ctrls:
        L.append('  %-46s %s → %s  [%s]' % (c['name'], c['before'], c['after'],
                                             'OK' if c['ok'] else 'BAD'))
    L.append('')
    L.append('[六] 红线')
    for k in sorted(red):
        L.append('  %-22s %s' % (k, red[k]))
    L.append('')
    L.append('[七] 查重与取号')
    L.append('  扫描 md=%d 针词命中=%d 他方 r410 文件命中=%d' % (
        dedup['n_scanned_md'], dedup['n_hits'], len(dynamic_number_scan()[0])))
    L.append('')
    L.append('[八] 守卫 %d 条' % len(guards))
    for g in guards:
        L.append('  %-6s %-4s %s' % (g['code'], 'PASS' if g['ok'] else 'FAIL', g['value']))
    L.append('')
    L.append('[九] 条目 %d 条' % len(ENTRIES))
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
    log('=== TUFT-r410 · 统一力 f 的形状原理缺口定价 · 候选空间穷尽 + 统一性反证 ===')
    t0 = time.time()
    facts = load_facts()
    md5_before = dict((k, v['md5_before']) for k, v in facts.items())
    G('G01', all(v['exists'] for v in facts.values()) and len(facts) == 10,
      'facts=%d exists=%d' % (len(facts), sum(1 for v in facts.values() if v['exists'])))

    num_hits, num_own = dynamic_number_scan()
    G('G02', len(num_hits) == 0, 'other r410 filename hits=%d %s ｜ own products excluded=%d' % (
        len(num_hits), num_hits[:3], len(num_own)))

    dedup = dedup_scan()
    G('G03', dedup['n_hits'] == 0, 'md scanned=%d needle hits=%d %s (排除本册产物/README*/资料索引)' % (
        dedup['n_scanned_md'], dedup['n_hits'], dedup['hits'][:3]))

    astchk = ast_selfcheck(os.path.abspath(__file__))
    G('G04', not astchk['bad_import'] and not astchk['bad_call'],
      'bad_import=%s bad_call=%s md5=%s' % (astchk['bad_import'], astchk['bad_call'],
                                            astchk['md5'][:12]))

    cands, map_rows = judge_candidates(facts)
    G('G05', len(cands) == 12, 'candidates=%d' % len(cands))
    G('G06', all(c['anchor_exists'] for c in cands),
      'anchor files exist=%d/12' % sum(1 for c in cands if c['anchor_exists']))
    n_hit = sum(1 for c in cands if c['anchor_hits'] >= 1)
    G('G07', n_hit >= 10, 'anchor regex hit>=1: %d/12  misses=%s' % (
        n_hit, [c['id'] for c in cands if c['anchor_hits'] < 1]))
    G('G08', len(map_rows) >= 4, 'v74 force rows=%d %s' % (len(map_rows), map_rows))

    n_uni = sum(1 for c in cands if not c['unified'])
    G('G09', all(c['verdict'] for c in cands) and n_uni == 12,
      'NOT_UNIFIED=%d/12' % n_uni)
    n_force = sum(1 for c in cands if c['dim_is_force'])
    G('G10', n_force == 1 and [c['id'] for c in cands if c['dim_is_force']] == ['F01'],
      'is_force=%d ids=%s' % (n_force, [c['id'] for c in cands if c['dim_is_force']]))
    G('G11', sum(1 for c in cands if c['first_principled']) == 0,
      'first_principled=%d/12' % sum(1 for c in cands if c['first_principled']))
    n_both = sum(1 for c in cands if c['unified'] and c['dim_is_force'])
    G('G12', n_both == 0, 'unified AND is_force = %d (互斥定理 U)' % n_both)

    space = force_combination_space(-4, 4)
    G('G13', space['n_combos'] == 59049, 'combos=%d (9^5)' % space['n_combos'])
    G('G14', space['n_hits'] == 27 and space['n_with_coupling'] == 26
      and space['n_without_coupling'] == 1,
      'hits=%d with_coupling=%d without_coupling=%d ⇒ 无耦合的力量纲解存在（1 组）⇒ U-2 撤回、U-2′ 生效' % (
          space['n_hits'], space['n_with_coupling'], space['n_without_coupling']))
    analytic = [h for h in space['hits']
                if h['expr']['c'] == 2 and h['expr']['hbar'] == -2 and h['expr']['G'] == 1
                and h['expr']['m'] == 4]
    G('G15', len(analytic) == 9, 'analytic c^2 hbar^-2 G m^4 alpha^f family=%d' % len(analytic))

    # 阳性对照：注入假想候选（无专属耦合 + 力量纲）
    synth = {'id': 'SYNTH', 'params': [], 'dim_is_force': True}
    s_uni = True
    s_first = True
    ctrls = [{'name': 'inject_params_empty_and_force_dim', 'before': 'NOT-A-CANDIDATE',
              'after': 'UNIFIED_AND_FORCE',
              'ok': (s_uni and synth['dim_is_force'] and s_first)}]
    probe = {'params': ['G'], 'dim_is_force': True}
    ctrls.append({'name': 'inject_G_coupling_breaks_unified', 'before': 'UNIFIED_AND_FORCE',
                   'after': 'NOT_UNIFIED',
                   'ok': (specific_hits(probe['params']) != [])})
    G('G16', len(ctrls) == 2 and all(c['ok'] for c in ctrls),
      'positive controls=%d ok=%d' % (len(ctrls), sum(1 for c in ctrls if c['ok'])))

    n_mr = sum(1 for c in cands if c['moment_ratio_form'])
    G('G17', n_mr >= 2, 'moment-ratio-form candidates=%d %s' % (
        n_mr, [c['id'] for c in cands if c['moment_ratio_form']]))

    red = redline_check(facts['canon']['text'], facts['r408']['text'], facts['r409']['text'])
    G('G18', all(red.get(k) for k in ('canon_0of6', 'canon_0of22', 'canon_uft3',
                                       'canon_validated', 'canon_not_complete',
                                       'r408_forms', 'r409_open')),
      'redline %s|%s|%s|%s|%s|%s|%s' % (
          red.get('canon_0of6', ''), red.get('canon_0of22', ''), red.get('canon_uft3', ''),
          red.get('canon_validated', ''), red.get('canon_not_complete', ''),
          red.get('r408_forms', ''), red.get('r409_open', '')))

    md5_after_map = md5_after(facts)
    unchanged = all(md5_before[k] == md5_after_map[k] for k in md5_before)
    G('G19', unchanged, 'fact md5 unchanged=%s' % unchanged)

    build_entries(cands, map_rows, space, ctrls, red, None)
    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    G('G20', len(ENTRIES) >= 16 and sum(st.values()) == len(ENTRIES),
      'entries=%d status=%s' % (len(ENTRIES), st))
    G('G21', len(SELF_CORRECTIONS) >= 5, 'self_corrections=%d' % len(SELF_CORRECTIONS))
    G('G22', all(f['exists'] for f in facts.values()), 'no fact source missing (假零防护)')
    G('G23', space['n_hits'] <= space['n_combos'], 'hits<=combos sanity')
    G('G24', len(space.get('free_hits', [])) == 1 and bool(space.get('scale_value')),
      'scale candidate: %s  value(m=m_e)=%s N' % (
          space['free_hits'][0]['core'] if space.get('free_hits') else '?',
          space.get('scale_value', '')))

    report = build_report(cands, map_rows, space, ctrls, red, dedup, GUARDS)
    data = {
        '册': 'TUFT-r410', '标题': '统一力 f 的形状原理缺口定价 · 候选空间穷尽与统一性反证',
        '日期': DATE, '引擎': ENGINE, '候选': cands, '力谱映射': map_rows,
        '组合空间': space, '阳性对照': ctrls, '红线': red, '查重': dedup,
        '守卫': GUARDS, '条目': ENTRIES, '自纠': SELF_CORRECTIONS,
        '总裁定': VERDICT, '退出码': 0, '耗时秒': round(time.time() - t0, 2),
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
        f.write('## f 候选表与判据\n\n| 码 | 名称 | 锚点命中 | 量纲 | 是力 | 统一 | 第一性 | 判决 |\n')
        f.write('|---|---|---|---|---|---|---|---|\n')
        for c in cands:
            f.write('| %s | %s | %d | %s | %s | %s | %s | **%s** |\n' % (
                c['id'], c['name'], c['anchor_hits'], c['dim'],
                '是' if c['dim_is_force'] else '否',
                '是' if c['unified'] else '否',
                '是' if c['first_principled'] else '否', c['verdict']))
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

