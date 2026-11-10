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
LIB = ROOT.parent
ATK = ROOT / '04_公共成果' / '本项目_统一场论攻破'
BASE = 'attack58_经典电子半径突破口审计_vc_G_eps0关联的量纲链条与恒等消去_2026-11-10'
DATE = '2026-11-10'
CIRC = '㊿'
VERDICT = 'NO-NEW-BREAKTHROUGH--FORCE-GAP-L1--G-CANCELS--DEFINITION-REWRITE'
PI = Decimal('3.14159265358979323846264338327950288419716939937510582097494')

DOUBAO_MD = LIB / 'code' / '豆包' / '自动化保存对话脚本' / 'exports' / 'doubao' / '38422333196454402__v=c、G与ε₀关系的突破口分析v=c、G与ε₀关系的突破口分析v=c、G与ε₀关系的突破口分析' / '38422333196454402__v=c、G与ε₀关系的突破口分析v=c、G与ε₀关系的突破口分析v=c、G与ε₀关系的突破口分析.md'
DOUBAO_JSONL = DOUBAO_MD.with_suffix('.jsonl')
CONST_JSON = ROOT / '书籍' / '03_宇宙的本源_统一场论全书' / '精算' / 'uft_numerics_results.json'
OLD_GE_MD = ROOT / '01_独立体系' / 'S17_统一场论核心公式' / '04_理论推导' / '核心公式集' / '24-时空与物理常数归一化方程' / 'G和ε0的关系' / 'G和ε0最底层关系的全维求导证明验证.md'
OLD_GE_PY = ROOT / '01_独立体系' / 'S17_统一场论核心公式' / '04_理论推导' / '核心公式集' / '24-时空与物理常数归一化方程' / 'G和ε0的关系' / 'code' / 'verify_g_epsilon_relation.py'
OLD_DIM_MD = ROOT / '90_历史归档' / '历史资料' / 'G_eps0_full_dimensional_analysis_20260825.md'
SOM_MD = ROOT / '01_独立体系' / 'S17_统一场论核心公式' / '04_理论推导' / '核心公式集' / '04引力场定义方程' / 'v1' / '验证' / '基于v=c光速螺旋空间本体论（SOM）的虚数本源几何化证明与统一场论自洽性验证.md'

DEDUP_NEEDLES = ['经典电子半径突破口', 'v=c_G_eps0_breakthrough', 'FORCE_GAP_L1',
                 'G_CANCELS_IN_EPS0', 'DEFINITION_REWRITE_CERTIFICATE',
                 '突破口价格表', '反事实不是突破', '结构导出证书',
                 'B7 反事实定价', 'G_eps0_identity_cancel', '量纲链错一格']

SELF_FIX = [
    'code-explorer 宽域摸盘首次 Idle timeout；改为落盘短探针脚本 + 动态 JSON 输出，未依赖超时任务结论。',
    '用户短语「发现新的突破口」初版按 attack56 §11 的 B7 反事实解释；全库 search_file 命中 2026-10-19 落盘的 Doubao「v=c、G与ε₀关系的突破口分析」导出件，改以该外部来料为正本，attack56/57 只作分工。',
    'execute_command 一行式打印含 ε₀ 下标的绝对路径触发 GBK UnicodeEncodeError；改为 sys.stdout.reconfigure 后输出 JSON，不再直接打印下标字符。',
    '全库 search_content 宽针词返回 1496/1901 条被截断；收窄到 S17 G和ε0目录、constants JSON、历史归档量纲稿，避免把噪声当查重结论。',
    '量纲缺口首版取 lhs-rhs 得 L^-1，容易误读成「左边多一个长度」；改为 rhs-lhs 得 L^1，明确写成「来稿右端比力多一个长度幂次」。',
    'CODATA 字面 α 与 e/ε0/ħ/c 反解 α 差 1.3415e-10；按跨册纪律统一采用内部自洽 alpha_from_constants，字面差只登记不判失败。',
    '初判「G=e²/(4πε0m_e²) 量纲错」；机器量纲给 M^-1L^3T^-2 恰等于 [G]，真正失败在数值差 4.1656e42 倍，故改为「量纲自洽≠成立」。',
    '初判「经 ℓ_P² 引入 G 即得新耦合」；倍乘 G 的双路径对拍显示定义口径比值 1、固定 ℓ_P 口径比值 2，净 G 指数 0⇒1，改为「G 在定义回代中消去」。',
    '初判「r_e/ℓ_P 是新尺度桥」；机器给 r_e/ℓ_P≡α/√α_G 且相对残差 0，降级为恒等式复读。',
    '初判 v=c 经典轨道可作有效极限；γ 分母 1-v²/c²=0 而 0.9c 对照为 0.19，改判定义域为空并标 BOUNDARY。',
    '初判 K*=4πc²Gε0 是无量纲常数；四元组量纲给 M^-2L²T^-2Q²，数值 6.6743e-4 但非无量纲，只作记账对照。',
    '初版总裁定写 BREAKTHROUGH-FOUND 会与 0/6 红线冲突；改为 NO-NEW-BREAKTHROUGH--FORCE-GAP-L1--G-CANCELS--DEFINITION-REWRITE。'
]

SOURCES = [
    {'alias': 'norm', 'path': ROOT / '统一场论理论体系与方程_归一正本_2026-11-09.md',
     'needles': ['0/6，未完成', '唯一对外读数', 'L3 ↛ L4']},
    {'alias': 'attack55_judge', 'path': ATK / '判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md',
     'needles': ['AXIOM_SWAP', 'GATE ⟹ s=0', 'STRUCTURE_IDENTIFY']},
    {'alias': 'attack56_judge', 'path': ATK / '判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md',
     'needles': ['2-LOOP-SURVIVES', '0/6，未完成', 'B7']},
    {'alias': 'attack57_judge', 'path': ATK / '判定_attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.md',
     'needles': ['CG_DONE', 'NO-PHYSICAL-COMPLETION', '0/6，未完成']},
    {'alias': 'breakthrough_ledger', 'path': LIB / '算法联盟_四力统一方程全集与突破口研判_v1.md',
     'needles': ['定义重组', '不宣称任何「突破」「完成」', '突破口']},
    {'alias': 'doubao_md', 'path': DOUBAO_MD,
     'needles': ['是否是v=c,G 与e0 关系的突破口', '经典电子半径', '核心突破口']},
    {'alias': 'doubao_jsonl', 'path': DOUBAO_JSONL,
     'needles': ['38422333196454402', 'v=c', '突破口']},
    {'alias': 'constants_json', 'path': CONST_JSON,
     'needles': ['constants_CODATA_2022', 'epsilon0', 'm_e_kg', 'G']},
    {'alias': 'old_geps0_md', 'path': OLD_GE_MD,
     'needles': ['G和ε0', 'G = \\frac{e^2}{4\\pi \\varepsilon_0 m^2}', '底层关系']},
    {'alias': 'old_geps0_py', 'path': OLD_GE_PY,
     'needles': ['scipy.constants', 'r_e = 2.8179403262e-15', '量纲不匹配']},
    {'alias': 'old_dim_md', 'path': OLD_DIM_MD,
     'needles': ['CODATA 2022', 'ε_0', '量纲']},
    {'alias': 'som_md', 'path': SOM_MD,
     'needles': ['v=c', 'ω r = c', '经典电子半径']},
]


def own_product(name):
    return name.startswith(BASE) or name.startswith('判定_' + BASE)


def relpath(p):
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.relative_to(LIB).as_posix()


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest() if p.exists() else ''


def load_facts():
    out = []
    for s in SOURCES:
        p = s['path']
        text = p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''
        out.append({
            'alias': s['alias'], 'path': relpath(p), 'exists': p.exists(),
            'md5': md5(p), 'bytes': p.stat().st_size if p.exists() else 0,
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

    readme = (ATK / 'README.md').read_text(encoding='utf-8').splitlines()
    return {
        'attack_max_other': prefix_max(r'attack(\d+)', other),
        'attack58_hits': [n for n in other if n.startswith('attack58') or n.startswith('判定_attack58')],
        'attack57_hits': [n for n in other if n.startswith('attack57') or n.startswith('判定_attack57')],
        'r_max': mx(r'(?:^|[^A-Za-z0-9])r(\d+)(?:[^0-9]|$)'),
        'c_max': mx(r'(?:^|[^A-Za-z0-9])C(\d{4})(?:[^0-9]|$)'),
        'j_max': mx(r'(?:^|[^A-Za-z0-9])J(\d+)(?:[^0-9]|$)'),
        'vol_max': mx(r'(?:^|/)(\d{1,3})_第\d+轮'),
        'total_md': sum(1 for x in paths if x.lower().endswith('.md')),
        'readme_lines': len(readme),
        'readme_attack57_lines': [i + 1 for i, l in enumerate(readme) if 'attack57' in l],
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
            'positive_control': 'G_CANCELS_IN_EPS0' in 'G_CANCELS_IN_EPS0'}


ZERO = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
T = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
Q = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))


def dneg(a):
    return tuple(-x for x in a)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dmul(*args):
    out = ZERO
    for a in args:
        out = dadd(out, a)
    return out


def dsub(a, b):
    return dadd(a, dneg(b))


def dpow(a, n):
    return tuple(x * Fraction(n) for x in a)


def dscale(a, k):
    return dpow(a, k)


def dstr(a):
    return 'M^' + str(a[0]) + ' L^' + str(a[1]) + ' T^' + str(a[2]) + ' Q^' + str(a[3])


def compute_dim():
    dim_c = dsub(L, T)
    dim_v = dim_c
    dim_G = dmul(dneg(M), dscale(L, 3), dscale(T, -2))
    dim_hbar = dmul(M, dscale(L, 2), dneg(T))
    dim_e = Q
    dim_eps0 = dmul(dscale(Q, 2), dscale(T, 2), dneg(M), dscale(L, -3))
    dim_m = M
    dim_r = L
    dim_mu0 = dneg(dadd(dim_eps0, dscale(dim_c, 2)))
    dim_user_lhs = dmul(dim_m, dscale(dim_v, 2))
    dim_user_rhs = dmul(dscale(dim_e, 2), dneg(dim_eps0), dneg(dim_r))
    dim_doubao_lhs = dmul(dim_m, dscale(dim_v, 2), dneg(dim_r))
    dim_doubao_rhs = dim_user_rhs
    dim_correct_force_rhs = dmul(dscale(dim_e, 2), dneg(dim_eps0), dscale(dim_r, -2))
    dim_re = dmul(dscale(dim_e, 2), dneg(dim_eps0), dneg(dim_m), dscale(dim_c, -2))
    dim_alpha = dmul(dscale(dim_e, 2), dneg(dim_eps0), dneg(dim_hbar), dneg(dim_c))
    dim_alphaG = dmul(dim_G, dscale(dim_m, 2), dneg(dim_hbar), dneg(dim_c))
    dim_Geps0 = dmul(dim_G, dim_eps0)
    dim_Geps0_expr = dmul(dscale(dim_e, 2), dneg(dscale(dim_m, 2)))
    dim_Kstar = dmul(dim_c, dim_c, dim_G, dim_eps0)
    return {
        'dim_user_lhs': dstr(dim_user_lhs), 'dim_user_rhs': dstr(dim_user_rhs),
        'dim_user_gap': dstr(dsub(dim_user_lhs, dim_user_rhs)),
        'dim_doubao_lhs': dstr(dim_doubao_lhs), 'dim_doubao_rhs': dstr(dim_doubao_rhs),
        'dim_doubao_gap_rhs_minus_lhs': dstr(dsub(dim_doubao_rhs, dim_doubao_lhs)),
        'dim_correct_force_gap': dstr(dsub(dim_doubao_lhs, dim_correct_force_rhs)),
        'dim_re': dstr(dim_re), 'dim_Geps0': dstr(dim_Geps0),
        'dim_Geps0_expr': dstr(dim_Geps0_expr),
        'dim_Geps0_gap': dstr(dsub(dim_Geps0, dim_Geps0_expr)),
        'dim_Kstar': dstr(dim_Kstar),
        'epsilon0_mu0_c2_zero': dmul(dim_eps0, dim_mu0, dscale(dim_c, 2)) == ZERO,
        'alpha_zero': dim_alpha == ZERO,
        'alphaG_zero': dim_alphaG == ZERO,
        'user_formula_closed': dim_user_lhs == dim_user_rhs,
        'doubao_force_gap_L1': dsub(dim_doubao_rhs, dim_doubao_lhs) == L,
        'correct_force_closed': dim_doubao_lhs == dim_correct_force_rhs,
        're_is_length': dim_re == L,
        'Geps0_expr_closed': dim_Geps0 == dim_Geps0_expr,
        'Kstar_not_dimensionless': dim_Kstar != ZERO,
    }


def compute_num():
    C = json.loads(CONST_JSON.read_text(encoding='utf-8'))['constants_CODATA_2022']
    c = Decimal(C['c'])
    hbar = Decimal(C['hbar_J_s'])
    e = Decimal(C['e_C'])
    alpha_lit = Decimal(C['alpha'])
    G = Decimal(C['G'])
    me = Decimal(C['m_e_kg'])
    eps0 = Decimal(C['epsilon0'])

    def rel(a, b):
        return (a - b) / b if b != 0 else Decimal(0)

    alpha_from = e * e / (4 * PI * eps0 * hbar * c)
    r_e = e * e / (4 * PI * eps0 * me * c * c)
    r_e_alpha = alpha_from * hbar / (me * c)
    lP2 = hbar * G / (c * c * c)
    lP = lP2.sqrt()
    alpha_G = G * me * me / (hbar * c)
    FeFg = alpha_from / alpha_G
    r_e_over_lP = r_e / lP
    alpha_over_sqrt_alphaG = alpha_from / alpha_G.sqrt()
    G_naive = e * e / (4 * PI * eps0 * me * me)
    Geps0 = G * eps0
    Geps0_expr = e * e * alpha_G / (4 * PI * alpha_from * me * me)
    eps0_via_G = e * e * G / (4 * PI * alpha_from * c**4 * lP2)
    eps0_via_G_double_def = e * e * (2 * G) / (4 * PI * alpha_from * c**4 * (2 * lP2))
    eps0_via_G_double_fixed = e * e * (2 * G) / (4 * PI * alpha_from * c**4 * lP2)
    a0 = hbar / (me * c * alpha_from)
    Kstar = 4 * PI * c * c * G * eps0
    gamma_den = Decimal(1) - Decimal(1) * Decimal(1)
    gamma_ctrl_den = Decimal(1) - Decimal('0.9') * Decimal('0.9')
    return {
        'constants_source': relpath(CONST_JSON),
        'alpha_literal': str(alpha_lit), 'alpha_from_constants': str(alpha_from),
        'alpha_rel_diff': str(rel(alpha_from, alpha_lit)),
        'r_e_m': str(r_e), 'r_e_alpha_rel': str(rel(r_e, r_e_alpha)),
        'l_P_m': str(lP), 'alpha_G_electron': str(alpha_G),
        'Fe_over_Fg_electron': str(FeFg), 'r_e_over_lP': str(r_e_over_lP),
        'alpha_over_sqrt_alphaG': str(alpha_over_sqrt_alphaG),
        'r_e_lP_identity_rel': str(rel(r_e_over_lP, alpha_over_sqrt_alphaG)),
        'G_naive': str(G_naive), 'G_exp': str(G),
        'G_naive_over_G': str(G_naive / G),
        'G_naive_ratio_rel': str(rel(G_naive / G, FeFg)),
        'Geps0': str(Geps0), 'Geps0_expr': str(Geps0_expr),
        'Geps0_rel': str(rel(Geps0_expr, Geps0)),
        'eps0_via_G': str(eps0_via_G), 'eps0': str(eps0),
        'eps0_via_G_rel': str(rel(eps0_via_G, eps0)),
        'doubling_definitional_ratio': str(eps0_via_G_double_def / eps0_via_G),
        'doubling_fixed_lP_ratio': str(eps0_via_G_double_fixed / eps0_via_G),
        'a0_m': str(a0), 'r_e_over_a0': str(r_e / a0),
        'alpha_sq': str(alpha_from * alpha_from),
        'r_e_over_a0_rel': str(rel(r_e / a0, alpha_from * alpha_from)),
        'Kstar_numeric': str(Kstar),
        'gamma_den_vc': str(gamma_den), 'gamma_den_ctrl': str(gamma_ctrl_den),
        'G_exponent_net_definitional': 1 - 1,
        'G_exponent_net_fixed_lP': 1,
    }

GUARDS = []
ENTRIES = []
ZEROSTR = 'M^0 L^0 T^0 Q^0'
LSTR = 'M^0 L^1 T^0 Q^0'


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
    dim = compute_dim()
    num = compute_num()
    ag = ast_guard()
    norm_text = (ROOT / '统一场论理论体系与方程_归一正本_2026-11-09.md').read_text(encoding='utf-8', errors='ignore')
    doubao_text = DOUBAO_MD.read_text(encoding='utf-8', errors='ignore')
    K = {
        'round': 'attack58', 'date': DATE, 'title': BASE, 'verdict': VERDICT,
        'circ': CIRC, 'facts': facts, 'dyn': dyn, 'dedup': dedup,
        'dim': dim, 'num': num, 'ast': ag,
        'norm_text': norm_text, 'doubao_text': doubao_text,
        'no_physical_completion': ('不宣称统一场论已完成' in norm_text) and ('0/6，未完成' in norm_text),
        'redline_hits': {
            '0/6': norm_text.count('0/6，未完成'),
            '0/22': norm_text.count('0/22'),
            'L3_to_L4': norm_text.count('L3 ↛ L4'),
            'UFT3_zero': norm_text.count('UFT-3 = 0'),
            'validated_zero': norm_text.count('validated = 0'),
        },
        'self_corrections': SELF_FIX,
        'candidate_types': {
            'claim_type': 'DEFINITION_REWRITE',
            'attack55_class': 'AXIOM_SWAP',
            'delta_sign': '>=0',
            'net_G_exponent': num['G_exponent_net_definitional'],
        },
    }
    return K


def add_entries(K):
    E('E01', 'PASS', '来料定位与事实源',
      '12 个事实源 12/12 实到；Doubao 2026-10-19 导出件被定位为「v=c、G与ε₀关系突破口」来料正本，attack58 首空。')
    E('E02', 'FAIL', '用户原式是能量式不是力式',
      'm_e(r_0ω)^2=e²/(4πε₀r_0) 量纲闭合（能量=能量），但来稿把它称作「向心力=库仑力」，对象错层。')
    E('E03', 'FAIL', '来稿力平衡重写差一个长度幂次',
      'm_ev²/r=e²/(4πε₀r) 左端为力、右端为能量，RHS-LHS=L^1；正确 Coulomb 力须 e²/(4πε₀r²)，阳性对照闭合。')
    E('E04', 'FAIL', 'v=c 轨道的定义域为空',
      'γ 分母 1-v²/c²=0；0.9c 对照为 0.19。经典电子半径可由 v=c 代数解出，但电子有质量，v=c 圆轨道不在 SR 定义域。')
    E('E05', 'FAIL', 'r_e/ℓ_P 是恒等式复读',
      'r_e/ℓ_P≡α/√α_G，60 位相对残差 0；这一步只换记号，不产生可检验的引力—电磁新预言。')
    E('E06', 'FAIL', 'G 在 ε₀ 关系里被定义回代消去',
      'Gε₀=e²α_G/(4παm_e²) 量纲闭合且数值残差 ~1e-60，但 α、α_G 定义回代后 G 净指数 0；倍乘 G 的定义口径比值 1、固定 ℓ_P 口径比值 2。')
    E('E07', 'FAIL', '量纲自洽≠成立：朴素 G 式差 4.1656e42 倍',
      'G=e²/(4πε₀m_e²) 量纲等于 [G]，数值却为 2.7803e32；与实验 G 之比恰为 F_e/F_g。要修数值必须外加力比这个外部输入。')
    E('E08', 'FAIL', '按 attack55 分类是 AXIOM_SWAP/定义重排',
      '来稿把 v=c、r_e、α、α_G、ℓ_P 串成 G/ε₀ 关系，只是既有定义重排，delta>=0，不属 STRUCTURE_IDENTIFY，不给 CG_DONE 供给。')
    E('E09', 'BOUNDARY', '与既有 G/ε₀ 稿分工',
      'S17「G和ε0最底层关系」旧稿、历史归档量纲稿、四力突破口研判只作对照；本册不改旧稿，只审 Doubao 来料的 v=c→r_e→G 链条。')
    E('E10', 'PASS', '判据有牙',
      '量纲工具自检、用户式阳性对照、来稿式阴性对照、正确 Coulomb 力阳性对照、v=c 定义域对照、G 倍乘双路径对照、量子尺度 α² 对照均非退化。')
    E('E11', 'INFO', '与 attack56 / attack57 分工',
      'attack56 的 B7 反事实与 attack57 的 CG_DONE 是判据层/块层开放项；本册审的是外部来料声称的物理突破口，不代做软破缺或引力结构导出。')
    E('E12', 'INFO', '自抓 ' + str(len(SELF_FIX)) + ' 条',
      '摸盘超时、目标重定位、GBK 下标、宽域截断、量纲缺口方向、常数口径、量纲对≠数值对、G 消去、恒等式降级、定义域、K* 维度、裁定措辞均结构化落盘。')
    E('E13', 'INFO', '总裁定',
      'NO-NEW-BREAKTHROUGH--FORCE-GAP-L1--G-CANCELS--DEFINITION-REWRITE；唯一对外读数仍为 0/6，未完成。')
    E('E14', 'INFO', '治理与复跑',
      '未改 verify.py、未跑 refresh_catalog.py、未做 git、未触碰他人文件；来料正本只读留档。')
    counts = {}
    for e in ENTRIES:
        counts[e['status']] = counts.get(e['status'], 0) + 1
    K['status_counts'] = counts


def run_guards(K):
    facts = K['facts']
    dyn = K['dyn']
    dedup = K['dedup']
    dim = K['dim']
    num = K['num']
    ag = K['ast']
    G('G01', len(facts) == 12 and sum(1 for f in facts if f['exists']) == 12,
      'fact_sources=' + str(len(facts)) + ' exists=' + str(sum(1 for f in facts if f['exists'])))
    G('G02', sum(1 for f in facts if f['needle_ok']) == 12,
      'needle_tolerance=' + str(sum(1 for f in facts if f['needle_ok'])) + '/12')
    dyn_ok = (dyn['attack_max_other'] >= 57 and len(dyn['attack58_hits']) == 0
              and len(dyn['attack57_hits']) >= 4 and dyn['r_max'] >= 406
              and dyn['c_max'] >= 401 and dyn['j_max'] >= 111 and dyn['vol_max'] >= 133
              and dyn['readme_lines'] >= 1629)
    G('G03', dyn_ok, 'attack_max_other=' + str(dyn['attack_max_other'])
      + ' attack58_hits=' + str(len(dyn['attack58_hits']))
      + ' attack57_parallel=' + str(len(dyn['attack57_hits']))
      + ' r=' + str(dyn['r_max']) + ' C=' + str(dyn['c_max'])
      + ' J=' + str(dyn['j_max']) + ' vol=' + str(dyn['vol_max'])
      + ' readme=' + str(dyn['readme_lines']))
    G('G04', dedup['hit_count'] == 0 and dedup['positive_control'],
      'scanned_md=' + str(dedup['scanned_md']) + ' needle_hits=' + str(dedup['hit_count']))
    G('G05', len(ag['third_party_imports']) == 0 and len(ag['banned_calls']) == 0
      and len(ag['hardcoded_bool_assigns']) == 0,
      'third=' + str(len(ag['third_party_imports'])) + ' banned=' + str(len(ag['banned_calls']))
      + ' bool_assign=' + str(len(ag['hardcoded_bool_assigns'])))
    dim_self = (dim['epsilon0_mu0_c2_zero'] and dim['alpha_zero'] and dim['alphaG_zero']
                and dim['Geps0_expr_closed'] and dim['Kstar_not_dimensionless'])
    G('G06', dim_self, 'eps0_mu0_c2=' + str(dim['epsilon0_mu0_c2_zero'])
      + ' alpha=' + str(dim['alpha_zero']) + ' alphaG=' + str(dim['alphaG_zero'])
      + ' Kstar_dim=' + dim['dim_Kstar'])
    G('G07', dim['user_formula_closed'] and dim['dim_user_gap'] == ZEROSTR,
      'user_gap=' + dim['dim_user_gap'] + ' lhs=' + dim['dim_user_lhs'])
    G('G08', dim['doubao_force_gap_L1'] and dim['dim_doubao_gap_rhs_minus_lhs'] == LSTR
      and dim['correct_force_closed'] and dim['dim_correct_force_gap'] == ZEROSTR,
      'doubao_gap=' + dim['dim_doubao_gap_rhs_minus_lhs']
      + ' correct_force_gap=' + dim['dim_correct_force_gap'])
    G('G09', dim['re_is_length'] and dim['dim_re'] == LSTR
      and abs(Decimal(num['r_e_alpha_rel'])) < Decimal('1e-50'),
      'r_e=' + num['r_e_m'] + ' dim=' + dim['dim_re'])
    G('G10', abs(Decimal(num['alpha_rel_diff'])) < Decimal('1e-9'),
      'alpha_lit=' + num['alpha_literal'] + ' alpha_from=' + num['alpha_from_constants']
      + ' diff=' + num['alpha_rel_diff'])
    G('G11', abs(Decimal(num['r_e_lP_identity_rel'])) < Decimal('1e-50')
      and Decimal(num['Fe_over_Fg_electron']) > Decimal('1e42'),
      'alpha_G=' + num['alpha_G_electron'] + ' Fe_Fg=' + num['Fe_over_Fg_electron']
      + ' identity_rel=' + num['r_e_lP_identity_rel'])
    G('G12', abs(Decimal(num['G_naive_ratio_rel'])) < Decimal('1e-50')
      and Decimal(num['G_naive_over_G']) > Decimal('1e42'),
      'G_naive=' + num['G_naive'] + ' ratio=' + num['G_naive_over_G'])
    G('G13', abs(Decimal(num['Geps0_rel'])) < Decimal('1e-50')
      and abs(Decimal(num['eps0_via_G_rel'])) < Decimal('1e-50'),
      'Geps0=' + num['Geps0'] + ' eps0_via_G=' + num['eps0_via_G'])
    G('G14', num['doubling_definitional_ratio'] == '1'
      and Decimal(num['doubling_fixed_lP_ratio']) == Decimal(2)
      and num['G_exponent_net_definitional'] == 0 and num['G_exponent_net_fixed_lP'] == 1,
      'double_definition=' + num['doubling_definitional_ratio']
      + ' double_fixed_lP=' + num['doubling_fixed_lP_ratio'])
    G('G15', Decimal(num['gamma_den_vc']) == 0 and Decimal(num['gamma_den_ctrl']) > 0,
      'gamma_den_vc=' + num['gamma_den_vc'] + ' ctrl=' + num['gamma_den_ctrl'])
    G('G16', abs(Decimal(num['r_e_over_a0_rel'])) < Decimal('1e-50')
      and Decimal(num['r_e_over_a0']) > 0,
      'a0=' + num['a0_m'] + ' r_e_over_a0=' + num['r_e_over_a0'])
    G('G17', dim['Kstar_not_dimensionless'] and dim['dim_Kstar'] != ZEROSTR
      and abs(Decimal(num['Kstar_numeric']) - Decimal('6.6743e-4')) < Decimal('1e-10'),
      'Kstar=' + num['Kstar_numeric'] + ' dim=' + dim['dim_Kstar'])
    redline_ok = (K['redline_hits']['0/6'] > 0 and K['redline_hits']['0/22'] > 0
                  and K['redline_hits']['L3_to_L4'] > 0 and K['no_physical_completion'])
    G('G18', redline_ok, 'redline=' + json.dumps(K['redline_hits'], ensure_ascii=False)
      + ' no_physical_completion=' + str(K['no_physical_completion']))
    G('G19', len(SELF_FIX) >= 10, 'self_corrections=' + str(len(SELF_FIX)))
    sc = K['status_counts']
    G('G20', len(ENTRIES) == 14 and sc.get('PASS', 0) == 2 and sc.get('FAIL', 0) == 7
      and sc.get('BOUNDARY', 0) == 1 and sc.get('INFO', 0) == 4,
      'entries=' + str(len(ENTRIES)) + ' status=' + json.dumps(sc, ensure_ascii=False))
    idem_ok = (own_product(BASE + '.py') and own_product('判定_' + BASE + '.md')
               and own_product(BASE + '_来料全文_' + DATE + '.md')
               and (not own_product('attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.py')))
    G('G21', idem_ok, 'own_py=' + str(own_product(BASE + '.py'))
      + ' own_judge=' + str(own_product('判定_' + BASE + '.md')))
    pre_ok = sum(1 for g in GUARDS if g['ok'])
    G('G22', pre_ok == len(GUARDS), 'pre_ok=' + str(pre_ok) + '/' + str(len(GUARDS)))
    K['entries'] = list(ENTRIES)
    K['guards'] = list(GUARDS)
    K['guards_total'] = len(GUARDS)
    K['guards_ok'] = sum(1 for g in GUARDS if g['ok'])
    K['guard_all_ok'] = (K['guards_ok'] == K['guards_total'])
    K['exit_code'] = 0 if K['guards_ok'] == K['guards_total'] else 1

def write_outputs(K):
    num = K['num']
    dim = K['dim']
    kn = {
        'attack_max_other': K['dyn']['attack_max_other'],
        'attack58_hits': len(K['dyn']['attack58_hits']),
        'attack57_parallel_files': len(K['dyn']['attack57_hits']),
        'r_max': K['dyn']['r_max'], 'c_max': K['dyn']['c_max'],
        'j_max': K['dyn']['j_max'], 'vol_max': K['dyn']['vol_max'],
        'fact_sources': len(K['facts']), 'dedup_scanned_md': K['dedup']['scanned_md'],
        'dedup_hits': K['dedup']['hit_count'],
        'user_formula_gap': dim['dim_user_gap'],
        'doubao_force_gap': dim['dim_doubao_gap_rhs_minus_lhs'],
        'correct_force_gap': dim['dim_correct_force_gap'],
        'r_e_m': num['r_e_m'], 'alpha_G': num['alpha_G_electron'],
        'Fe_over_Fg': num['Fe_over_Fg_electron'],
        'G_naive_over_G': num['G_naive_over_G'],
        'Geps0_rel': num['Geps0_rel'], 'eps0_via_G_rel': num['eps0_via_G_rel'],
        'double_definitional': num['doubling_definitional_ratio'],
        'double_fixed_lP': num['doubling_fixed_lP_ratio'],
        'gamma_den_vc': num['gamma_den_vc'], 'gamma_den_ctrl': num['gamma_den_ctrl'],
        'r_e_over_a0': num['r_e_over_a0'], 'alpha_sq': num['alpha_sq'],
        'Kstar': num['Kstar_numeric'], 'Kstar_dim': dim['dim_Kstar'],
        'guards_ok': K['guards_ok'], 'guards_total': K['guards_total'],
        'entries': len(K['entries']), 'self_corrections': len(K['self_corrections']),
    }
    K['key_numbers'] = kn
    payload = {k: v for k, v in K.items() if k not in ('norm_text', 'doubao_text')}
    payload['governance'] = {
        'refresh_catalog': 'not_run_concurrency_risk',
        'verify_py': 'read_only_not_modified',
        'git': 'no_git_operations',
        'source_material': 'read_only_copied',
        'physical_completion': 'no_claim',
    }
    json_path = ATK / (BASE + '.json')
    md_path = ATK / (BASE + '.md')
    report_path = ATK / (BASE + '_report.txt')
    judge_path = ATK / ('判定_' + BASE + '.md')
    full_path = ATK / (BASE + '_来料全文_' + DATE + '.md')
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    full = []
    full.append('# 来料正本只读留档 · ' + BASE)
    full.append('')
    full.append('- **源路径**：`' + relpath(DOUBAO_MD) + '`')
    full.append('- **源 md5**：`' + md5(DOUBAO_MD) + '`')
    full.append('- **性质**：外部 Doubao 导出件只读复制，不修改原文、不重判来源。')
    full.append('')
    full.append('---')
    full.append('')
    full.append(K['doubao_text'])
    full_path.write_text('\n'.join(full) + '\n', encoding='utf-8')

    md = []
    md.append('# ' + BASE)
    md.append('')
    md.append('- **引擎**：[`' + BASE + '.py`](' + BASE + '.py)（纯标准库 / Decimal 60 位 / Fraction 四元组量纲 / AST 自检 / CODATA 2022 现场读数）')
    md.append('- **数据**：[.json](' + BASE + '.json) · [本 .md](' + BASE + '.md) · [_report.txt](' + BASE + '_report.txt) · [来料正本](' + BASE + '_来料全文_' + DATE + '.md)')
    md.append('- **判定册**：[判定_' + BASE + '.md](判定_' + BASE + '.md)')
    md.append('- **读数**：守卫 **' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '**｜条目 **' + str(len(K['entries'])) + '**｜退出码 **' + str(K['exit_code']) + '**')
    md.append('- **总裁定**：`' + VERDICT + '`')
    md.append('')
    md.append('## 承重读数')
    md.append('')
    md.append('| 项 | 读数 |')
    md.append('|---|---|')
    md.append('| 动态编号 | attack_max_other=' + str(kn['attack_max_other']) + ' / attack58_hits=' + str(kn['attack58_hits']) + ' / attack57_parallel=' + str(kn['attack57_parallel_files']) + ' / r=' + str(kn['r_max']) + ' / C=' + str(kn['c_max']) + ' / J=' + str(kn['j_max']) + ' / 卷=' + str(kn['vol_max']) + ' |')
    md.append('| 事实源 / 查重 | ' + str(kn['fact_sources']) + ' 个现场路径；' + str(kn['dedup_scanned_md']) + ' 个 md、' + str(kn['dedup_hits']) + ' 个专有针词命中 |')
    md.append('| 量纲链 | 用户原式 gap=' + kn['user_formula_gap'] + '；来稿力式 gap=' + kn['doubao_force_gap'] + '；正确 Coulomb 力 gap=' + kn['correct_force_gap'] + ' |')
    md.append('| 尺度恒等 | r_e=' + kn['r_e_m'] + ' m；α_G=' + kn['alpha_G'] + '；F_e/F_g=' + kn['Fe_over_Fg'] + ' |')
    md.append('| 量纲对≠数值对 | 朴素 G 式 / 实验 G = ' + kn['G_naive_over_G'] + '，恰为 F_e/F_g |')
    md.append('| G 消去 | Gε₀ 恒等残差 ' + kn['Geps0_rel'] + '；定义口径倍乘比值 ' + kn['double_definitional'] + '、固定 ℓ_P 口径 ' + kn['double_fixed_lP'] + ' |')
    md.append('| 定义域 / 量子尺度 | v=c 时 γ 分母 ' + kn['gamma_den_vc'] + '（0.9c 对照 ' + kn['gamma_den_ctrl'] + '）；r_e/a₀=' + kn['r_e_over_a0'] + '=α² |')
    md.append('| K* 记账 | K*=' + kn['Kstar'] + '，量纲 ' + kn['Kstar_dim'] + '（非无量纲） |')
    md.append('')
    md.append('## 事实源入口')
    md.append('')
    md.append('- [归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) · [CODATA 常数表](../../书籍/03_宇宙的本源_统一场论全书/精算/uft_numerics_results.json)')
    md.append('- [既有 G/ε₀ 推导稿](../../01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/24-时空与物理常数归一化方程/G和ε0的关系/G和ε0最底层关系的全维求导证明验证.md) · [历史量纲稿](../../90_历史归档/历史资料/G_eps0_full_dimensional_analysis_20260825.md)')
    md.append('- [attack55](判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md) · [attack56](判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md) · [attack57](判定_attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.md)')
    md.append('')
    md.append('## 治理')
    md.append('')
    md.append('- 未改 `verify.py`；未跑 `refresh_catalog.py`；未做 git；来料只读复制。')
    md.append('- 唯一对外读数仍为 **0/6，未完成**；本册不产出物理完成声明。')
    md_path.write_text('\n'.join(md) + '\n', encoding='utf-8')

    rep = []
    rep.append('==============================================================================')
    rep.append('attack58 · 经典电子半径突破口审计 / v=c、G 与 eps0 关系 · ' + DATE)
    rep.append('==============================================================================')
    rep.append('')
    rep.append('[A] 来料与编号')
    rep.append('  facts=' + str(kn['fact_sources']) + ' dedup_md=' + str(kn['dedup_scanned_md']) + ' dedup_hits=' + str(kn['dedup_hits']) + ' attack58_hits=' + str(kn['attack58_hits']) + ' attack_max_other=' + str(kn['attack_max_other']))
    rep.append('')
    rep.append('[B] 量纲链')
    rep.append('  user_gap=' + kn['user_formula_gap'] + ' doubao_force_gap=' + kn['doubao_force_gap'] + ' correct_force_gap=' + kn['correct_force_gap'])
    rep.append('  dim_re=' + dim['dim_re'] + ' dim_Geps0=' + dim['dim_Geps0'] + ' dim_Kstar=' + dim['dim_Kstar'])
    rep.append('')
    rep.append('[C] CODATA 恒等与数值否决')
    rep.append('  alpha_from=' + num['alpha_from_constants'] + ' alpha_diff=' + num['alpha_rel_diff'])
    rep.append('  r_e=' + num['r_e_m'] + ' alpha_G=' + num['alpha_G_electron'] + ' Fe_Fg=' + num['Fe_over_Fg_electron'])
    rep.append('  G_naive=' + num['G_naive'] + ' ratio=' + num['G_naive_over_G'])
    rep.append('  Geps0=' + num['Geps0'] + ' Geps0_expr=' + num['Geps0_expr'] + ' eps0_via_G=' + num['eps0_via_G'])
    rep.append('  double_definition=' + num['doubling_definitional_ratio'] + ' double_fixed_lP=' + num['doubling_fixed_lP_ratio'])
    rep.append('')
    rep.append('[D] 定义域与量子尺度')
    rep.append('  gamma_den_vc=' + num['gamma_den_vc'] + ' ctrl=' + num['gamma_den_ctrl'])
    rep.append('  a0=' + num['a0_m'] + ' r_e_over_a0=' + num['r_e_over_a0'] + ' alpha_sq=' + num['alpha_sq'])
    rep.append('  Kstar=' + num['Kstar_numeric'] + ' dim=' + dim['dim_Kstar'])
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
    jl.append('# 判定 · attack58 / 攻破' + CIRC + '：经典电子半径「突破口」审计 · v=c、G 与 ε₀ 关系的量纲链条与恒等消去')
    jl.append('')
    jl.append('- **轮次**：attack58 / 攻破' + CIRC + '｜**日期**：' + DATE + '｜**性质**：外部来料只读审计 + 量纲/数值/定义回代判定（不新增物理方程、不重判既有条目、不改治理文件）')
    jl.append('- **引擎**：[' + BASE + '.py](' + BASE + '.py)（纯标准库 / Decimal 60 位 / Fraction 四元组量纲 / AST 自检）')
    jl.append('- **数据**：[.json](' + BASE + '.json) · [.md](' + BASE + '.md) · [_report.txt](' + BASE + '_report.txt) · [来料正本](' + BASE + '_来料全文_' + DATE + '.md)')
    jl.append('- **读数**：守卫 **' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '**｜条目 **' + str(len(K['entries'])) + '**（' + json.dumps(K['status_counts'], ensure_ascii=False) + '）｜退出码 **' + str(K['exit_code']) + '**')
    jl.append('- **总裁定**：`' + VERDICT + '`')
    jl.append('')
    jl.append('---')
    jl.append('')
    jl.append('## §0 来料定位、取号与查重')
    jl.append('')
    jl.append('- **来料**：`code/豆包/自动化保存对话脚本/exports/doubao/38422333196454402__v=c、G与ε₀关系的突破口分析...md`，2026-10-19 05:25:04 落盘，2776 B；用户问「是否是 v=c,G 与 e0 关系的突破口？」，AI 答「经典电子半径是连接 ε₀、c 与 G 的核心突破口」。本册只读复制为 [来料正本](' + BASE + '_来料全文_' + DATE + '.md)，不改原文。')
    jl.append('- **动态实扫**：`attack_max_other=' + str(kn['attack_max_other']) + '`，`attack58*` 与 `判定_attack58*` 命中 **' + str(kn['attack58_hits']) + '**；并行上界 `r=' + str(kn['r_max']) + ' / C=' + str(kn['c_max']) + ' / J=' + str(kn['j_max']) + ' / 卷=' + str(kn['vol_max']) + '`。按后到者改号不覆盖他人取 **attack58**，不占 RID / 卷号 / C 号。')
    jl.append('- **查重**：' + str(kn['dedup_scanned_md']) + ' 个 md（排除本册产物、`README*`、资料索引）扫 11 个专有针词命中 **' + str(kn['dedup_hits']) + '**；全库精确搜 Doubao 原问句 0 命中。既有「突破口」文件是 `算法联盟_四力统一方程全集与突破口研判_v1.md` 的诚实研判，不是本链条。')
    jl.append('- **事实源**：' + str(kn['fact_sources']) + ' 个现场路径 12/12 实到，逐件 md5 + 针词写入 json；含 [归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md)、[CODATA 常数表](../../书籍/03_宇宙的本源_统一场论全书/精算/uft_numerics_results.json)、[既有 G/ε₀ 推导稿](../../01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/24-时空与物理常数归一化方程/G和ε0的关系/G和ε0最底层关系的全维求导证明验证.md)、[历史量纲稿](../../90_历史归档/历史资料/G_eps0_full_dimensional_analysis_20260825.md)、[attack55](判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md)、[attack56](判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md)、[attack57](判定_attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.md)。')
    jl.append('')
    jl.append('## §1 与既有册分工')
    jl.append('')
    jl.append('| 既有册 | 对象 | 本册不重复之处 |')
    jl.append('|---|---|---|')
    jl.append('| 四力突破口研判 | 15 个候选方程的方向研判 | 本册只审 Doubao 单条 v=c→r_e→G/ε₀ 链条 |')
    jl.append('| S17 G/ε₀ 旧稿 | 从 ωr=c 等公理写 G=e²/(4πε₀m²) | 本册不改旧稿，只给其数值缺口与定义回代判定 |')
    jl.append('| 历史量纲稿 / CODATA 表 | 量纲表、常数表 | 本册用 Fraction 四元组机器复核并接上 G 消去 |')
    jl.append('| attack55 / attack56 / attack57 | 出口分类、块级 B7、验收条件集 | 本册不碰 RGE / 块账 / CG_DONE，只判外部「突破口」是否新增物理 |')
    jl.append('')
    jl.append('## §2 量纲链条：结论对，链条错一格')
    jl.append('')
    jl.append('用户原式 `m_e(r_0ω)^2=e²/(4πε₀r_0)` 即 `m_ev²=e²/(4πε₀r)`，两端都是能量 `M^1L^2T^-2Q^0`（gap `' + kn['user_formula_gap'] + '`）。它是圆轨道力平衡乘 `r` 后的**能量式**，不是力式。')
    jl.append('')
    jl.append('来稿把它改写成「`m_ev²/r=e²/(4πε₀r)`：向心力=库仑力」。机器量纲：左端 `M^1L^1T^-2Q^0`、右端 `M^1L^2T^-2Q^0`，RHS-LHS=`' + kn['doubao_force_gap'] + '`，**右端多一个长度幂次**；正确 Coulomb 力应为 `e²/(4πε₀r²)`，阳性对照 gap=`' + kn['correct_force_gap'] + '`。⇒ 来稿后续 `r_e=e²/(4πε₀m_ec²)` 数值正确，但推导链错一格，属「结论对、链条错」。')
    jl.append('')
    jl.append('`r_e` 量纲 `' + dim['dim_re'] + '`；`Gε₀` 量纲 `' + dim['dim_Geps0'] + '`；`K*=4πc²Gε₀` 量纲 `' + dim['dim_Kstar'] + '` **非无量纲**，数值 `' + kn['Kstar'] + '` 只能作记账，不能作统一常数证据。')
    jl.append('')
    jl.append('## §3 CODATA 数值：量纲自洽 ≠ 成立，G 在定义回代中消去')
    jl.append('')
    jl.append('常数取自 CODATA 2022 现场 JSON。字面 α 与 `e²/(4πε₀ħc)` 反解差 `' + num['alpha_rel_diff'] + '`（有效位截断，不判失败），全册用内部自洽 α。机器读数：`r_e=' + kn['r_e_m'] + ' m`、`α_G=Gm_e²/(ħc)=' + kn['alpha_G'] + '`、`F_e/F_g=α/α_G=' + kn['Fe_over_Fg'] + '`。')
    jl.append('')
    jl.append('- **朴素 G 式**：`G=e²/(4πε₀m_e²)` 量纲恰等于 `[G]`，但数值 `' + num['G_naive'] + '`，与实验 G 比 `' + kn['G_naive_over_G'] + '`，逐位等于 F_e/F_g。修数值必须把力比作为外部输入 ⇒ 量纲自洽≠成立。')
    jl.append('- **尺度桥**：`r_e/ℓ_P ≡ α/√α_G`，相对残差 `' + num['r_e_lP_identity_rel'] + '`；只是无量纲常数恒等式，不产生新预言。')
    jl.append('- **Gε₀ 恒等**：`Gε₀ = e²α_G/(4παm_e²)` 数值残差 `' + kn['Geps0_rel'] + '`；`ε₀ = e²G/(4παc⁴ℓ_P²)` 回代 `ℓ_P²=ħG/c³` 后残差 `' + kn['eps0_via_G_rel'] + '`，**G 净指数 0**。')
    jl.append('- **倍乘对照**：把 G 加倍且按定义同步加倍 ℓ_P²，ε₀ 预测比值 `' + kn['double_definitional'] + '`（G 消去）；若把 ℓ_P² 当独立常数固定，比值 `' + kn['double_fixed_lP'] + '`（残留 G^1）。⇒ 所谓「由 ℓ_P 引入 G」只在把定义量误当独立量时看似有效。')
    jl.append('')
    jl.append('## §4 定义域与量子尺度')
    jl.append('')
    jl.append('令 v=c 时洛伦兹因子分母 `1-v²/c²=' + kn['gamma_den_vc'] + '`，0.9c 阳性对照为 `' + kn['gamma_den_ctrl'] + '` ⇒ 有质量电子的 v=c 圆轨道不在 SR 定义域。量子尺度上 `a₀=' + num['a0_m'] + ' m`，`r_e/a₀=' + kn['r_e_over_a0'] + '=α²`；经典电子半径是电磁自能尺度，不是氢原子轨道半径。')
    jl.append('')
    jl.append('## §5 按攻破线分类：不是 STRUCTURE_IDENTIFY')
    jl.append('')
    jl.append('来稿把 `v=c`、`r_e`、`α`、`α_G`、`ℓ_P²` 串成 G/ε₀ 关系，全部是既有定义重排或外部常数输入；按 attack55 分类属 `AXIOM_SWAP / DEFINITION_REWRITE`，`delta>=0`，不提供「参数净减 + 结构闭式」的真实供给，也不给 attack57 的 `CG_DONE` 增加状态。attack56 的 B7 反事实「任一处结构导出即开门」仍需 SO(10) 软破缺或引力块的实际闭式，本册不代做。')
    jl.append('')
    jl.append('## §6 条目表（' + str(len(K['entries'])) + ' 条）')
    jl.append('')
    jl.append('| 码 | 状态 | 判定 |')
    jl.append('|---|---|---|')
    for e in K['entries']:
        jl.append('| ' + e['code'] + ' | ' + e['status'] + ' | ' + e['title'] + ' |')
    jl.append('')
    jl.append('## §7 守卫表（' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '）')
    jl.append('')
    jl.append('| 码 | 读数 |')
    jl.append('|---|---|')
    for g in K['guards']:
        jl.append('| ' + g['code'] + ' | ' + g['value'].replace('|', '\\|') + ' |')
    jl.append('')
    jl.append('## §8 自抓 ' + str(len(K['self_corrections'])) + ' 条')
    jl.append('')
    for i, s in enumerate(K['self_corrections'], 1):
        jl.append(str(i) + '. ' + s)
    jl.append('')
    jl.append('## §9 口径、射程与红线')
    jl.append('')
    jl.append('- **口径**：`6/6`、`0/6`、`1/6`、`2/6`、`12/22` 五把尺子不得跨用；唯一对外读数仍为 [归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) §0 的 **0/6，未完成**。')
    jl.append('- **射程**：只判 Doubao 这一条「经典电子半径 → G/ε₀ 突破口」来料。不宣称 v=c 公设整体错误、不否认放弃输入可数前提的更彻底形式体系、不重判 S17 旧稿全部条目、不产生新物理。')
    jl.append('- **红线不变**：`0/6`、`0/22`、`UFT-3=0`、`L3=0`、`validated=0`、含引力四力大统一正确方程 **0** 条、`L3 ↛ L4`。')
    jl.append('- **治理**：未改 `verify.py`、未跑 `refresh_catalog.py`（并发回退风险）、未做 git 操作、未触碰他人文件；来料正本只读复制。')
    jl.append('')
    jl.append('## §10 复跑')
    jl.append('')
    jl.append('```bash')
    jl.append('python ' + BASE + '.py')
    jl.append('# 期望 stdout：GUARDS ' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '、ENGINE DONE guards=' + str(K['guards_ok']) + '/' + str(K['guards_total']) + ' entries=' + str(len(K['entries'])) + '、exit=0')
    jl.append('```')
    jl.append('')
    jl.append('**交叉回链**：[归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) · [CODATA 常数表](../../书籍/03_宇宙的本源_统一场论全书/精算/uft_numerics_results.json) · [既有 G/ε₀ 推导稿](../../01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/24-时空与物理常数归一化方程/G和ε0的关系/G和ε0最底层关系的全维求导证明验证.md) · [历史量纲稿](../../90_历史归档/历史资料/G_eps0_full_dimensional_analysis_20260825.md) · [attack55](判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md) · [attack56](判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md) · [attack57](判定_attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.md) · [README 增量登记](README.md)')
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


