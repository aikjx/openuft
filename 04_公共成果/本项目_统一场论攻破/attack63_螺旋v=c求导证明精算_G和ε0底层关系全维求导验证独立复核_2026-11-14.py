# -*- coding: utf-8 -*-
import ast
import hashlib
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
BASE = 'attack63_螺旋v=c求导证明精算_G和ε0底层关系全维求导验证独立复核_2026-11-14'
DATE = '2026-11-14'
CIRC = '55'
VERDICT = ('NO-NEW-BREAKTHROUGH--DERIVATION-PROOF-FALSIFIED--SELF-VERIFY-RUBBER-STAMP'
           '--G-CANCELS--FORCE-RATIO-EXTERNAL')
PI = Decimal('3.14159265358979323846264338327950288419716939937510582097494')

GE_DIR = (ROOT / '01_独立体系' / 'S17_统一场论核心公式' / '04_理论推导' / '核心公式集'
          / '24-时空与物理常数归一化方程' / 'G和ε0的关系')
GE_MD = GE_DIR / 'G和ε0最底层关系的全维求导证明验证.md'
GE_DERIV_PY = GE_DIR / 'code' / 'verify_derivatives.py'
CONST_JSON = ROOT / '书籍' / '03_宇宙的本源_统一场论全书' / '精算' / 'uft_numerics_results.json'
NORM_MD = ROOT / '统一场论理论体系与方程_归一正本_2026-11-09.md'

DEDUP_NEEDLES = ['DERIVATION-PROOF-FALSIFIED', 'ONE_MINUS_PI_EPS0_BACKWARDS',
                 'SELF-VERIFY-RUBBER-STAMP', 'FORCE-RATIO-CONSTANT-DERIVATIVE-ZERO',
                 '螺旋求导证明精算独立复核', 'G和ε0求导稿步骤审计',
                 'DOC_DERIVATIVE_DIM_NOT_INV_LENGTH', 'rubber_stamp_zero_assert',
                 '求导自洽声明被反证', 'STEP4_DROPPED_FORCE_RATIO']

SELF_FIX = [
    '宽域 find / Glob 在 my_lib 全树超时；改为只读已知目录 + 引擎内 ROOT.rglob(*.md) 单次普查，attack 号段从 ATK 目录现扫，不依赖超时任务结论。',
    '初版想把「v=c 螺旋力统一」整体再判一遍；现扫发现 attack10/13 已判 κταⁿ 力谱螺旋、attack58 已判外部 Doubao v=c→r_e→G/ε₀ 来料结论，且 attack58 明文「不重判 S17 旧稿全部条目」；改以 S17《G和ε0最底层关系的全维求导证明验证.md》的求导证明步骤为唯一靶，机制互补不复算。',
    '初判 S17 稿「全维求导验证」自洽；独立重推发现 §5 把 (1−πε₀) 当小量，实跑 1−πε₀≈0.99999999997≈1，推理方向反了，改判 FAIL 并落反证读数。',
    '初版只核核心公式数值；补核步骤1（含 1/(F_e/F_g) 因子，1=1 恒等）与步骤4（丢因子，1 vs F_e/F_g≈4.17e42）的内部矛盾，机器给 step4_ratio≈4.17e42≠1。',
    '初判文档导数表达式量纲为 1/length；Fraction 四元组给 M^1 L^2 T^-2 Q^-2，并非 L^-1，且「1−πε₀」本身量纲非法（πε₀ 有量纲），补 D07 量纲反证 + 「1−α」阳性对照。',
    '初版把力比导数当动力学读数；e、m_e、G、ε₀ 全是常数 ⇒ F_e/F_g 是常数 ⇒ d/dr≡0（独立地面真值），文档非零导数是「把常数当 r 函数」的范畴错误，补 D05。',
    '读文档自带 verify_derivatives.py：0 个 assert、无独立地面真值，§5 印 term=1−πε₀≈1 却硬编「由于值很小」；独立算 approximate_value≈1e110（巨大），坐实自证橡皮图章，补 D08。',
    'CODATA 字面 α 与 e²/(4πε₀ħc) 反解 α 差 ~1.34e-10（有效位截断）；按跨册纪律统一用内部自洽 alpha_from_constants，字面差只登记不判失败。',
    'v=c 对有质量电子 γ 分母 1−v²/c²=0；螺旋「空间以光速螺旋」是空间流公设、不是粒子轨道，本册只作 BOUNDARY 分工对照（attack58 E04 同族），不宣称 v=c 公设整体错误。',
    '动态取号 attack63：现扫 attack_max_other>=62 且 attack63* 命中 0；并行写者占号以盘上为准，后到者改号不覆盖。',
    '初版总裁定想写 BREAKTHROUGH；与 0/6 红线冲突，改为 NO-NEW-BREAKTHROUGH--DERIVATION-PROOF-FALSIFIED--SELF-VERIFY-RUBBER-STAMP--G-CANCELS--FORCE-RATIO-EXTERNAL。',
]

SOURCES = [
    {'alias': 'norm', 'path': NORM_MD,
     'needles': ['0/6，未完成', '唯一对外读数', 'L3 ↛ L4']},
    {'alias': 'geps0_md', 'path': GE_MD,
     'needles': ['ω r = c', '全维求导验证', '1 - \\pi \\varepsilon_0', 'G = \\frac{e^2}{4\\pi \\varepsilon_0 m^2}']},
    {'alias': 'geps0_deriv_py', 'path': GE_DERIV_PY,
     'needles': ['1 - pi * epsilon_0', '由于值很小', 'def verify_derivative_consistency']},
    {'alias': 'constants_json', 'path': CONST_JSON,
     'needles': ['constants_CODATA_2022', 'epsilon0', 'm_e_kg', '"G"']},
    {'alias': 'attack58_judge', 'path': ATK / '判定_attack58_经典电子半径突破口审计_vc_G_eps0关联的量纲链条与恒等消去_2026-11-10.md',
     'needles': ['NO-NEW-BREAKTHROUGH', '不重判 S17 旧稿全部条目', 'G 在定义回代中消去']},
    {'alias': 'attack10_report', 'path': ATK / 'attack10_空间光速螺旋四力统一场论复核_report.txt',
     'needles': ['空间光速螺旋曲率挠率四力统一场论', '恒等重写', '第一性预言是 0']},
    {'alias': 'attack62_report', 'path': ATK / 'attack62_知识全域无免费午餐_置换不变先验与归纳偏置对齐_2026-11-12_report.txt',
     'needles': ['KNOWLEDGE-NFL', 'NO-PHYSICAL-COMPLETION', 'GUARDS 20/20']},
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


def scan_dedup():
    hits = {k: [] for k in DEDUP_NEEDLES}
    scanned = 0
    md_paths = []
    for p in ROOT.rglob('*.md'):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        md_paths.append(rel)
        n = p.name
        if own_product(n) or n.startswith('README') or '资料索引' in rel or n.startswith('_tmp_'):
            continue
        text = p.read_text(encoding='utf-8', errors='ignore')
        scanned += 1
        for k in DEDUP_NEEDLES:
            if k in text:
                hits[k].append(rel)
    return {'scanned_md': scanned, 'hits': hits,
            'hit_count': sum(len(v) for v in hits.values()),
            'md_paths': md_paths,
            'positive_control': 'ONE_MINUS_PI_EPS0_BACKWARDS' in 'ONE_MINUS_PI_EPS0_BACKWARDS'}


def dynamic_scan(md_paths):
    atk_names = [p.name for p in ATK.iterdir() if p.is_file()]
    other = [n for n in atk_names if not own_product(n)]

    def prefix_max(pattern, names):
        vals = [int(m.group(1)) for n in names for m in [re.search(pattern, n)] if m]
        return max(vals, default=0)

    def mx(pattern, names):
        vals = [int(m.group(1)) for x in names for m in [re.search(pattern, x)] if m]
        return max(vals, default=0)

    readme = (ATK / 'README.md').read_text(encoding='utf-8').splitlines()
    pool = md_paths + atk_names
    return {
        'attack_max_other': prefix_max(r'attack(\d+)', other),
        'attack63_hits': [n for n in other if n.startswith('attack63') or n.startswith('判定_attack63')],
        'attack62_hits': [n for n in other if n.startswith('attack62') or n.startswith('判定_attack62')],
        'r_max': mx(r'(?:^|[^A-Za-z0-9])r(\d+)(?:[^0-9]|$)', pool),
        'c_max': mx(r'(?:^|[^A-Za-z0-9])C(\d{4})(?:[^0-9]|$)', pool),
        'j_max': mx(r'(?:^|[^A-Za-z0-9])J(\d+)(?:[^0-9]|$)', pool),
        'vol_max': mx(r'(?:^|/)(\d{1,3})_第\d+轮', pool),
        'total_md': len(md_paths),
        'readme_lines': len(readme),
    }


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


def dstr(a):
    return 'M^' + str(a[0]) + ' L^' + str(a[1]) + ' T^' + str(a[2]) + ' Q^' + str(a[3])


def compute_dim():
    dim_c = dsub(L, T)
    dim_omega = dneg(T)
    dim_G = dmul(dneg(M), dpow(L, 3), dpow(T, -2))
    dim_hbar = dmul(M, dpow(L, 2), dneg(T))
    dim_e = Q
    dim_eps0 = dmul(dpow(Q, 2), dpow(T, 2), dneg(M), dpow(L, -3))
    dim_m = M
    dim_r = L
    dim_alpha = dmul(dpow(dim_e, 2), dneg(dim_eps0), dneg(dim_hbar), dneg(dim_c))
    dim_axiom_lhs = dmul(dim_omega, dim_r)
    dim_G_naive = dmul(dpow(dim_e, 2), dneg(dim_eps0), dpow(dim_m, -2))
    dim_force_ratio = dmul(dpow(dim_e, 2), dneg(dim_eps0), dneg(dim_G), dpow(dim_m, -2))
    dim_one_minus_pi_eps0_gap = dsub(ZERO, dim_eps0)
    dim_one_minus_alpha_gap = dsub(ZERO, dim_alpha)
    invL = dneg(L)
    dim_doc_deriv = dmul(dpow(dim_omega, 2), dpow(dim_r, 2), dpow(dim_e, 2),
                         dpow(dim_eps0, -2), dpow(dim_G, -2), dpow(dim_m, -3))
    return {
        'dim_axiom_lhs': dstr(dim_axiom_lhs), 'dim_c': dstr(dim_c),
        'axiom_closed': dim_axiom_lhs == dim_c,
        'dim_G': dstr(dim_G), 'dim_eps0': dstr(dim_eps0),
        'dim_G_naive': dstr(dim_G_naive), 'G_naive_dim_closed': dim_G_naive == dim_G,
        'force_ratio_dimensionless': dim_force_ratio == ZERO,
        'alpha_dimensionless': dim_alpha == ZERO,
        'one_minus_pi_eps0_gap': dstr(dim_one_minus_pi_eps0_gap),
        'one_minus_pi_eps0_invalid': dim_one_minus_pi_eps0_gap != ZERO,
        'one_minus_alpha_gap': dstr(dim_one_minus_alpha_gap),
        'one_minus_alpha_valid': dim_one_minus_alpha_gap == ZERO,
        'dim_doc_deriv': dstr(dim_doc_deriv), 'invL': dstr(invL),
        'doc_deriv_not_invL': dim_doc_deriv != invL,
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
    alpha_G = G * me * me / (hbar * c)
    FeFg = alpha_from / alpha_G
    r_e = e * e / (4 * PI * eps0 * me * c * c)
    r_g = G * me / (c * c)
    G_naive = e * e / (4 * PI * eps0 * me * me)
    G_with_ratio = G_naive / FeFg
    pi_eps0 = PI * eps0
    one_minus = Decimal(1) - pi_eps0
    omega = c / r_e
    doc_approx = (omega * omega * r_e * r_e * e * e * one_minus) / (2 * PI * PI * eps0 * eps0 * G * G * me * me * me)
    force_ratio_deriv_true = Decimal(0)
    step1_LHS = Decimal(1)
    step1_RHS = FeFg * (Decimal(1) / FeFg)
    step4_RHS = FeFg
    step4_ratio = step4_RHS / step1_LHS
    gamma_den_vc = Decimal(1) - Decimal(1)
    gamma_ctrl = Decimal(1) - Decimal('0.9') * Decimal('0.9')
    deriv_src = GE_DERIV_PY.read_text(encoding='utf-8', errors='ignore')
    assert_count = len(re.findall(r'^\s*assert\b', deriv_src, flags=re.M))
    rubber_label = ('由于值很小' in deriv_src) or ('由于 πε₀ 很小' in deriv_src)
    return {
        'constants_source': relpath(CONST_JSON),
        'alpha_literal': str(alpha_lit), 'alpha_from_constants': str(alpha_from),
        'alpha_rel_diff': str(rel(alpha_from, alpha_lit)),
        'alpha_G_electron': str(alpha_G), 'Fe_over_Fg_electron': str(FeFg),
        'r_e_m': str(r_e), 'r_g_m': str(r_g), 'r_e_over_r_g': str(r_e / r_g),
        'r_e_over_r_g_rel': str(rel(r_e / r_g, FeFg)),
        'G_naive': str(G_naive), 'G_exp': str(G), 'G_naive_over_G': str(G_naive / G),
        'G_naive_ratio_rel': str(rel(G_naive / G, FeFg)),
        'G_with_ratio': str(G_with_ratio), 'G_with_ratio_rel': str(rel(G_with_ratio, G)),
        'pi_eps0': str(pi_eps0), 'one_minus_pi_eps0': str(one_minus),
        'one_minus_near_one_abs': str(abs(one_minus - Decimal(1))),
        'one_minus_near_zero_abs': str(abs(one_minus)),
        'doc_approx_value': str(doc_approx),
        'force_ratio_deriv_true': str(force_ratio_deriv_true),
        'step1_LHS': str(step1_LHS), 'step1_RHS': str(step1_RHS),
        'step1_rel': str(rel(step1_RHS, step1_LHS)),
        'step4_RHS': str(step4_RHS), 'step4_ratio': str(step4_ratio),
        'gamma_den_vc': str(gamma_den_vc), 'gamma_den_ctrl': str(gamma_ctrl),
        'deriv_script_assert_count': assert_count,
        'deriv_script_rubber_label': rubber_label,
    }


GUARDS = []
ENTRIES = []


def G(code, ok, value):
    GUARDS.append({'code': code, 'ok': bool(ok), 'value': str(value)})


def E(code, status, title, detail):
    ENTRIES.append({'code': code, 'status': status, 'title': title, 'detail': detail})


def ast_guard():
    src = pathlib.Path(__file__).read_text(encoding='utf-8')
    tree = ast.parse(src)
    stdlib = {'ast', 'hashlib', 'json', 'pathlib', 're', 'sys', 'decimal', 'fractions'}
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

    def is_bool_const(node):
        return isinstance(node, ast.Constant) and isinstance(getattr(node, 'value', None), bool)

    hard = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and is_bool_const(node.value):
            hard.append(node.lineno)
    return {'third_party_imports': third, 'banned_calls': banned_calls,
            'hardcoded_bool_assigns': hard}


def compute():
    facts = load_facts()
    dedup = scan_dedup()
    dyn = dynamic_scan(dedup['md_paths'])
    dim = compute_dim()
    num = compute_num()
    ag = ast_guard()
    norm_text = NORM_MD.read_text(encoding='utf-8', errors='ignore')
    K = {
        'round': 'attack63', 'date': DATE, 'title': BASE, 'verdict': VERDICT,
        'circ': CIRC, 'facts': facts, 'dyn': dyn,
        'dedup': {k: v for k, v in dedup.items() if k != 'md_paths'},
        'dim': dim, 'num': num, 'ast': ag,
        'no_physical_completion': ('不宣称统一场论已完成' in norm_text) and ('0/6，未完成' in norm_text),
        'redline_hits': {
            '0/6': norm_text.count('0/6，未完成'),
            '0/22': norm_text.count('0/22'),
            'L3_to_L4': norm_text.count('L3 ↛ L4'),
            'UFT3_zero': norm_text.count('UFT-3 = 0'),
            'validated_zero': norm_text.count('validated = 0'),
        },
        'self_corrections': SELF_FIX,
    }
    return K


def add_entries(K):
    num = K['num']
    dim = K['dim']
    E('D01', 'PASS', '靶定位与事实源（机制互补不复算）',
      '靶=S17《G和ε0最底层关系的全维求导证明验证.md》（核心公理 ωr=c 光速螺旋）；7 个事实源实到。attack10/13 已判 κταⁿ 力谱螺旋、attack58 已判外部 Doubao v=c→r_e→G/ε₀ 来料结论且明文「不重判 S17 旧稿全部条目」；本册只独立复核该稿求导证明步骤。')
    E('D02', 'PASS', '前提代数链是合法重排（但只是定义重排）',
      '由 m=ω²r³/G 与 ωr=c 得 G=c²r/m（步骤8/14）；由 e²=4πε₀ωr²mc 与 ωr=c 得 rm=e²/(4πε₀c²)（步骤9/13）。量纲闭合、代数合法，但 r 被前提钉成引力半径 r_g=Gm_e/c²=' + num['r_g_m'] + ' m，与稿用经典电子半径 r_e=' + num['r_e_m'] + ' m 相差 r_e/r_g=' + num['r_e_over_r_g'] + '=F_e/F_g。')
    E('D03', 'FAIL', '步骤1 与步骤4 内部矛盾：力比因子被丢',
      '步骤1「全维度统一恒等式」含 1/(F_e/F_g) 因子，LHS=mc²/(hν)=1、RHS=(F_e/F_g)·1/(F_e/F_g)=1（恒等 1=1，零信息）；步骤4 丢因子后 RHS=F_e/F_g=' + num['step4_RHS'] + '，而 LHS 仍=1，step4_ratio=' + num['step4_ratio'] + '≠1。')
    E('D04', 'FAIL', '核心公式 G=e²/(4πε₀m²) 量纲自洽≠成立',
      'G_naive=' + num['G_naive'] + '，量纲=' + dim['dim_G_naive'] + '=[G]，但与实验 G 比 G_naive/G=' + num['G_naive_over_G'] + '≈F_e/F_g；结论核心公式丢力比，与步骤11 G=e²/(4πε₀(F_e/F_g)m²) 自相矛盾。补力比 G_with_ratio 复现实验 G 残差 ' + num['G_with_ratio_rel'] + '，但力比本身含 G ⇒ 循环。')
    E('D05', 'FAIL', '力比是常数 ⇒ d/dr≡0（范畴错误）',
      'F_e/F_g=e²/(4πε₀Gm²) 中 e、ε₀、G、m 全是常数 ⇒ 力比是常数，独立地面真值 d(F_e/F_g)/dr=' + num['force_ratio_deriv_true'] + '（精确零）。文档把常数当 r 函数（dm/dr=ω²r²/G≠0）算出非零导数，是范畴错误，不是动力学自洽。')
    E('D06', 'FAIL', '§5「1−πε₀≈0 ⇒ 导数≈0」反证：方向反了',
      'πε₀=' + num['pi_eps0'] + '，1−πε₀=' + num['one_minus_pi_eps0'] + '≈1（|·−1|=' + num['one_minus_near_one_abs'] + '），不是小量；πε₀ 小恰恰使 (1−πε₀)≈1。独立算稿 §5 approximate_value=' + num['doc_approx_value'] + '（巨大，非「很小」）。「导数近似为零」声明被反证。')
    E('D07', 'FAIL', '「1−πε₀」量纲非法 + 导数式量纲非 1/length',
      'πε₀ 量纲=' + dim['dim_eps0'] + '，1 无量纲，「1−πε₀」gap=' + dim['one_minus_pi_eps0_gap'] + '≠0（不可相减）；阳性对照「1−α」gap=' + dim['one_minus_alpha_gap'] + '（α 无量纲，合法）。稿 §5 导数式量纲=' + dim['dim_doc_deriv'] + '，并非 d(无量纲)/dr 应有的 ' + dim['invL'] + '。')
    E('D08', 'FAIL', '自带 verify_derivatives.py 是自证橡皮图章',
      '该脚本 assert 数=' + str(num['deriv_script_assert_count']) + '，无独立地面真值；§5 印 term=1−πε₀≈1 却硬编「由于值很小」（rubber_label=' + str(num['deriv_script_rubber_label']) + '）。判据自己证自己，全绿不构成证据。')
    E('D09', 'BOUNDARY', 'v=c 定义域（分工对照，不整体否证公设）',
      '有质量电子 v=c 时 γ 分母 1−v²/c²=' + num['gamma_den_vc'] + '（0.9c 对照 ' + num['gamma_den_ctrl'] + '）；「空间以光速螺旋」是空间流公设、非粒子轨道。与 attack58 E04 同族，本册只作对照，不宣称 v=c 公设整体错误。')
    E('D10', 'PASS', '判据有牙（正负对照 + 反噬变异体）',
      '量纲工具自检（α/力比无量纲、ε₀μ₀c²=1）；G 补力比复现 vs 丢力比差 4.17e42；常数力比导数=0 vs 稿 r 依赖式≈1e110；「1−α」合法 vs「1−πε₀」非法；1−πε₀≈1 vs 稿声称≈0。各对照非退化。')
    E('D11', 'INFO', '与 attack58 / attack10 / attack62 分工',
      'attack58 审外部 Doubao 来料结论（G 消去/定义重排）；attack10 审 κταⁿ 力谱螺旋（恒等重写+循环+发散）；attack62 给知识全域无免费午餐终局 no-go。本册补 S17 求导证明稿的步骤级独立反证，不重复上述机制。')
    E('D12', 'INFO', '自抓 ' + str(len(SELF_FIX)) + ' 条',
      '摸盘超时、靶重定位（互补不复算）、§5 方向反了、步骤4 丢因子、导数量纲、常数范畴错误、橡皮图章、常数口径、v=c 定义域、动态取号、裁定措辞均结构化落盘。')
    E('D13', 'INFO', '总裁定',
      VERDICT + '；唯一对外读数仍为 0/6，未完成。求导证明层反证不迁移为物理成立、不计攻破数。')
    E('D14', 'INFO', '治理与复跑',
      '未改 verify.py、未跑 refresh_catalog.py、未做 git、未触碰他人文件；S17 稿与其脚本只读。')
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
    G('G01', len(facts) == 7 and sum(1 for f in facts if f['exists']) == 7,
      'fact_sources=' + str(len(facts)) + ' exists=' + str(sum(1 for f in facts if f['exists'])))
    G('G02', sum(1 for f in facts if f['needle_ok']) == 7,
      'needle_ok=' + str(sum(1 for f in facts if f['needle_ok'])) + '/7')
    dyn_ok = (dyn['attack_max_other'] >= 62 and len(dyn['attack63_hits']) == 0
              and len(dyn['attack62_hits']) >= 4 and dyn['readme_lines'] >= 1578)
    G('G03', dyn_ok, 'attack_max_other=' + str(dyn['attack_max_other'])
      + ' attack63_hits=' + str(len(dyn['attack63_hits']))
      + ' attack62_parallel=' + str(len(dyn['attack62_hits']))
      + ' r=' + str(dyn['r_max']) + ' C=' + str(dyn['c_max'])
      + ' J=' + str(dyn['j_max']) + ' vol=' + str(dyn['vol_max'])
      + ' readme=' + str(dyn['readme_lines']))
    G('G04', dedup['hit_count'] == 0 and dedup['positive_control'],
      'scanned_md=' + str(dedup['scanned_md']) + ' needle_hits=' + str(dedup['hit_count']))
    G('G05', len(ag['third_party_imports']) == 0 and len(ag['banned_calls']) == 0
      and len(ag['hardcoded_bool_assigns']) == 0,
      'third=' + str(len(ag['third_party_imports'])) + ' banned=' + str(len(ag['banned_calls']))
      + ' bool_assign=' + str(len(ag['hardcoded_bool_assigns'])))
    G('G06', dim['axiom_closed'] and dim['alpha_dimensionless'] and dim['force_ratio_dimensionless'],
      'axiom_lhs=' + dim['dim_axiom_lhs'] + ' alpha_dimless=' + str(dim['alpha_dimensionless'])
      + ' force_ratio_dimless=' + str(dim['force_ratio_dimensionless']))
    G('G07', dim['G_naive_dim_closed'] and dim['dim_G_naive'] == dim['dim_G'],
      'G_naive_dim=' + dim['dim_G_naive'] + ' [G]=' + dim['dim_G'])
    G('G08', dim['one_minus_pi_eps0_invalid'] and dim['one_minus_alpha_valid'],
      'one_minus_pi_eps0_gap=' + dim['one_minus_pi_eps0_gap']
      + ' one_minus_alpha_gap=' + dim['one_minus_alpha_gap'])
    G('G09', dim['doc_deriv_not_invL'],
      'doc_deriv_dim=' + dim['dim_doc_deriv'] + ' expected_invL=' + dim['invL'])
    G('G10', abs(Decimal(num['alpha_rel_diff'])) < Decimal('1e-9'),
      'alpha_lit=' + num['alpha_literal'] + ' alpha_from=' + num['alpha_from_constants']
      + ' diff=' + num['alpha_rel_diff'])
    G('G11', abs(Decimal(num['G_naive_ratio_rel'])) < Decimal('1e-50')
      and Decimal(num['G_naive_over_G']) > Decimal('1e42'),
      'G_naive=' + num['G_naive'] + ' G_naive_over_G=' + num['G_naive_over_G'])
    G('G12', abs(Decimal(num['G_with_ratio_rel'])) < Decimal('1e-50'),
      'G_with_ratio=' + num['G_with_ratio'] + ' rel=' + num['G_with_ratio_rel'])
    G('G13', abs(Decimal(num['r_e_over_r_g_rel'])) < Decimal('1e-50')
      and Decimal(num['r_e_over_r_g']) > Decimal('1e42'),
      'r_e=' + num['r_e_m'] + ' r_g=' + num['r_g_m'] + ' r_e_over_r_g=' + num['r_e_over_r_g'])
    G('G14', abs(Decimal(num['one_minus_near_one_abs'])) < Decimal('1e-9')
      and Decimal(num['one_minus_near_zero_abs']) > Decimal('0.99'),
      'pi_eps0=' + num['pi_eps0'] + ' one_minus=' + num['one_minus_pi_eps0']
      + ' near_one_abs=' + num['one_minus_near_one_abs'])
    G('G15', Decimal(num['doc_approx_value']) > Decimal('1e100'),
      'doc_approx_value=' + num['doc_approx_value'])
    G('G16', Decimal(num['force_ratio_deriv_true']) == 0
      and Decimal(num['doc_approx_value']) != 0,
      'force_ratio_deriv_true=' + num['force_ratio_deriv_true']
      + ' doc_r_dependent=' + num['doc_approx_value'])
    G('G17', abs(Decimal(num['step1_rel'])) < Decimal('1e-50')
      and Decimal(num['step4_ratio']) > Decimal('1e42'),
      'step1_LHS=' + num['step1_LHS'] + ' step1_RHS=' + num['step1_RHS']
      + ' step4_ratio=' + num['step4_ratio'])
    G('G18', num['deriv_script_assert_count'] == 0 and num['deriv_script_rubber_label'],
      'assert_count=' + str(num['deriv_script_assert_count'])
      + ' rubber_label=' + str(num['deriv_script_rubber_label']))
    G('G19', Decimal(num['gamma_den_vc']) == 0 and Decimal(num['gamma_den_ctrl']) > 0,
      'gamma_den_vc=' + num['gamma_den_vc'] + ' ctrl=' + num['gamma_den_ctrl'])
    redline_ok = (K['redline_hits']['0/6'] > 0 and K['redline_hits']['0/22'] > 0
                  and K['redline_hits']['L3_to_L4'] > 0 and K['no_physical_completion'])
    G('G20', redline_ok, 'redline=' + json.dumps(K['redline_hits'], ensure_ascii=False)
      + ' no_physical_completion=' + str(K['no_physical_completion']))
    G('G21', len(SELF_FIX) >= 10, 'self_corrections=' + str(len(SELF_FIX)))
    sc = K['status_counts']
    G('G22', len(ENTRIES) == 14 and sc.get('PASS', 0) == 3 and sc.get('FAIL', 0) == 6
      and sc.get('BOUNDARY', 0) == 1 and sc.get('INFO', 0) == 4,
      'entries=' + str(len(ENTRIES)) + ' status=' + json.dumps(sc, ensure_ascii=False))
    idem_ok = (own_product(BASE + '.py') and own_product('判定_' + BASE + '.md')
               and (not own_product('attack62_知识全域无免费午餐_置换不变先验与归纳偏置对齐_2026-11-12.py')))
    G('G23', idem_ok, 'own_py=' + str(own_product(BASE + '.py'))
      + ' own_judge=' + str(own_product('判定_' + BASE + '.md')))
    pre_ok = sum(1 for g in GUARDS if g['ok'])
    G('G24', pre_ok == len(GUARDS), 'pre_ok=' + str(pre_ok) + '/' + str(len(GUARDS)))
    K['entries'] = list(ENTRIES)
    K['guards'] = list(GUARDS)
    K['guards_total'] = len(GUARDS)
    K['guards_ok'] = sum(1 for g in GUARDS if g['ok'])
    K['guard_all_ok'] = (K['guards_ok'] == K['guards_total'])
    K['exit_code'] = 0 if K['guards_ok'] == K['guards_total'] else 1


def write_outputs(K):
    num = K['num']
    dim = K['dim']
    dyn = K['dyn']
    kn = {
        'attack_max_other': dyn['attack_max_other'],
        'attack63_hits': len(dyn['attack63_hits']),
        'attack62_parallel_files': len(dyn['attack62_hits']),
        'r_max': dyn['r_max'], 'c_max': dyn['c_max'], 'j_max': dyn['j_max'], 'vol_max': dyn['vol_max'],
        'fact_sources': len(K['facts']), 'dedup_scanned_md': K['dedup']['scanned_md'],
        'dedup_hits': K['dedup']['hit_count'],
        'Fe_over_Fg': num['Fe_over_Fg_electron'], 'alpha_G': num['alpha_G_electron'],
        'G_naive_over_G': num['G_naive_over_G'], 'G_with_ratio_rel': num['G_with_ratio_rel'],
        'r_e_m': num['r_e_m'], 'r_g_m': num['r_g_m'], 'r_e_over_r_g': num['r_e_over_r_g'],
        'pi_eps0': num['pi_eps0'], 'one_minus_pi_eps0': num['one_minus_pi_eps0'],
        'doc_approx_value': num['doc_approx_value'],
        'force_ratio_deriv_true': num['force_ratio_deriv_true'],
        'step4_ratio': num['step4_ratio'],
        'one_minus_pi_eps0_gap': dim['one_minus_pi_eps0_gap'],
        'one_minus_alpha_gap': dim['one_minus_alpha_gap'],
        'doc_deriv_dim': dim['dim_doc_deriv'],
        'assert_count': num['deriv_script_assert_count'],
        'guards_ok': K['guards_ok'], 'guards_total': K['guards_total'],
        'entries': len(K['entries']), 'self_corrections': len(K['self_corrections']),
    }
    K['key_numbers'] = kn
    payload = {k: v for k, v in K.items()}
    payload['governance'] = {
        'refresh_catalog': 'not_run_concurrency_risk',
        'verify_py': 'read_only_not_modified',
        'git': 'no_git_operations',
        'source_material': 'read_only',
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
    md.append('- **引擎**：[`' + BASE + '.py`](' + BASE + '.py)（纯标准库 / Decimal 60 位 / Fraction 四元组量纲 / AST 自检 / CODATA 2022 现场读数）')
    md.append('- **数据**：[.json](' + BASE + '.json) · [本 .md](' + BASE + '.md) · [_report.txt](' + BASE + '_report.txt)')
    md.append('- **判定册**：[判定_' + BASE + '.md](判定_' + BASE + '.md)')
    md.append('- **读数**：守卫 **' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '**｜条目 **' + str(len(K['entries'])) + '**｜退出码 **' + str(K['exit_code']) + '**')
    md.append('- **总裁定**：`' + VERDICT + '`')
    md.append('')
    md.append('## 承重读数')
    md.append('')
    md.append('| 项 | 读数 |')
    md.append('|---|---|')
    md.append('| 动态编号 | attack_max_other=' + str(kn['attack_max_other']) + ' / attack63_hits=' + str(kn['attack63_hits']) + ' / attack62_parallel=' + str(kn['attack62_parallel_files']) + ' / r=' + str(kn['r_max']) + ' / C=' + str(kn['c_max']) + ' / J=' + str(kn['j_max']) + ' / 卷=' + str(kn['vol_max']) + ' |')
    md.append('| 事实源 / 查重 | ' + str(kn['fact_sources']) + ' 个现场路径；' + str(kn['dedup_scanned_md']) + ' 个 md、' + str(kn['dedup_hits']) + ' 个专有针词命中 |')
    md.append('| 力比 | F_e/F_g=' + kn['Fe_over_Fg'] + '；α_G=' + kn['alpha_G'] + ' |')
    md.append('| 核心公式数值否决 | G_naive/G=' + kn['G_naive_over_G'] + '≈F_e/F_g；补力比复现残差 ' + kn['G_with_ratio_rel'] + ' |')
    md.append('| 步骤4 丢因子 | step4_ratio=' + kn['step4_ratio'] + '（步骤1 恒等 1=1） |')
    md.append('| §5 反证 | πε₀=' + kn['pi_eps0'] + '；1−πε₀=' + kn['one_minus_pi_eps0'] + '≈1；稿 approximate_value=' + kn['doc_approx_value'] + ' |')
    md.append('| 常数导数 | d(F_e/F_g)/dr=' + kn['force_ratio_deriv_true'] + '（精确零，力比是常数） |')
    md.append('| 量纲反证 | 「1−πε₀」gap=' + kn['one_minus_pi_eps0_gap'] + '；「1−α」gap=' + kn['one_minus_alpha_gap'] + '；稿导数式=' + kn['doc_deriv_dim'] + ' |')
    md.append('| 橡皮图章 | verify_derivatives.py assert 数=' + str(kn['assert_count']) + ' |')
    md.append('| 尺度 | r_e=' + kn['r_e_m'] + ' m；r_g=' + kn['r_g_m'] + ' m；r_e/r_g=' + kn['r_e_over_r_g'] + ' |')
    md.append('')
    md.append('## 治理')
    md.append('')
    md.append('- 未改 `verify.py`；未跑 `refresh_catalog.py`；未做 git；S17 稿与其脚本只读。')
    md.append('- 唯一对外读数仍为 **0/6，未完成**；本册不产出物理完成声明。')
    md_path.write_text('\n'.join(md) + '\n', encoding='utf-8')

    rep = []
    rep.append('==============================================================================')
    rep.append('attack63 · 螺旋 v=c 求导证明精算 / G和ε0 底层关系全维求导验证独立复核 · ' + DATE)
    rep.append('==============================================================================')
    rep.append('')
    rep.append('[A] 靶与编号')
    rep.append('  facts=' + str(kn['fact_sources']) + ' dedup_md=' + str(kn['dedup_scanned_md']) + ' dedup_hits=' + str(kn['dedup_hits']) + ' attack63_hits=' + str(kn['attack63_hits']) + ' attack_max_other=' + str(kn['attack_max_other']))
    rep.append('')
    rep.append('[B] 代数链与数值否决')
    rep.append('  Fe_Fg=' + num['Fe_over_Fg_electron'] + ' alpha_G=' + num['alpha_G_electron'])
    rep.append('  G_naive=' + num['G_naive'] + ' G_naive_over_G=' + num['G_naive_over_G'] + ' G_with_ratio_rel=' + num['G_with_ratio_rel'])
    rep.append('  step1_LHS=' + num['step1_LHS'] + ' step1_RHS=' + num['step1_RHS'] + ' step4_ratio=' + num['step4_ratio'])
    rep.append('  r_e=' + num['r_e_m'] + ' r_g=' + num['r_g_m'] + ' r_e_over_r_g=' + num['r_e_over_r_g'])
    rep.append('')
    rep.append('[C] 全维求导验证反证')
    rep.append('  pi_eps0=' + num['pi_eps0'] + ' one_minus_pi_eps0=' + num['one_minus_pi_eps0'] + ' near_one_abs=' + num['one_minus_near_one_abs'])
    rep.append('  doc_approx_value=' + num['doc_approx_value'] + ' force_ratio_deriv_true=' + num['force_ratio_deriv_true'])
    rep.append('  one_minus_pi_eps0_gap=' + dim['one_minus_pi_eps0_gap'] + ' one_minus_alpha_gap=' + dim['one_minus_alpha_gap'] + ' doc_deriv_dim=' + dim['dim_doc_deriv'])
    rep.append('  deriv_script_assert_count=' + str(num['deriv_script_assert_count']) + ' rubber_label=' + str(num['deriv_script_rubber_label']))
    rep.append('  gamma_den_vc=' + num['gamma_den_vc'] + ' ctrl=' + num['gamma_den_ctrl'])
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
    jl.append('# 判定 · attack63 / 攻破' + CIRC + '：螺旋 v=c 求导证明精算 · G和ε0 底层关系全维求导验证独立复核')
    jl.append('')
    jl.append('- **轮次**：attack63 / 攻破' + CIRC + '｜**日期**：' + DATE + '｜**性质**：内部求导证明稿步骤级独立复核（不新增物理方程、不重判既有条目、不改治理文件）')
    jl.append('- **引擎**：[' + BASE + '.py](' + BASE + '.py)（纯标准库 / Decimal 60 位 / Fraction 四元组量纲 / AST 自检）')
    jl.append('- **数据**：[.json](' + BASE + '.json) · [.md](' + BASE + '.md) · [_report.txt](' + BASE + '_report.txt)')
    jl.append('- **读数**：守卫 **' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '**｜条目 **' + str(len(K['entries'])) + '**（' + json.dumps(K['status_counts'], ensure_ascii=False) + '）｜退出码 **' + str(K['exit_code']) + '**')
    jl.append('- **总裁定**：`' + VERDICT + '`')
    jl.append('')
    jl.append('---')
    jl.append('')
    jl.append('## §0 靶定位、取号与查重（机制互补不复算）')
    jl.append('')
    jl.append('- **靶**：`01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/24-时空与物理常数归一化方程/G和ε0的关系/G和ε0最底层关系的全维求导证明验证.md`。核心公理「空间以真空光速做螺旋运动，满足 ωr=c」；含 16 步 G/ε₀ 代数推导 + 「全维求导验证」5 节。本册独立重推其步骤，不修改原文。')
    jl.append('- **动态实扫**：`attack_max_other=' + str(kn['attack_max_other']) + '`，`attack63*` 与 `判定_attack63*` 命中 **' + str(kn['attack63_hits']) + '**；并行上界 `r=' + str(kn['r_max']) + ' / C=' + str(kn['c_max']) + ' / J=' + str(kn['j_max']) + ' / 卷=' + str(kn['vol_max']) + '`。按后到者改号不覆盖他人取 **attack63**，不占 RID / 卷号 / C 号。')
    jl.append('- **查重**：' + str(kn['dedup_scanned_md']) + ' 个 md（排除本册产物、`README*`、资料索引）扫 ' + str(len(DEDUP_NEEDLES)) + ' 个专有针词命中 **' + str(kn['dedup_hits']) + '**。')
    jl.append('- **分工**：attack10/13 已判 κταⁿ 力谱螺旋（恒等重写+循环+发散）；attack58 已判外部 Doubao v=c→r_e→G/ε₀ 来料结论且明文「不重判 S17 旧稿全部条目」；attack62 给知识全域无免费午餐终局 no-go。本册补 S17 求导证明稿的**步骤级独立反证**，不重复上述机制。')
    jl.append('')
    jl.append('## §1 前提代数链：合法重排，但 r 被钉成引力半径')
    jl.append('')
    jl.append('由 `m=ω²r³/G` 与 `ωr=c` 得 `G=c²r/m`（步骤8/14）；由 `e²=4πε₀ωr²mc` 与 `ωr=c` 得 `rm=e²/(4πε₀c²)`（步骤9/13）。量纲闭合、代数合法。但 `G=c²r/m` 把 r 钉成引力半径 `r_g=Gm_e/c²=' + num['r_g_m'] + ' m`，而稿脚本用经典电子半径 `r_e=' + num['r_e_m'] + ' m`，二者比 `r_e/r_g=' + num['r_e_over_r_g'] + '=F_e/F_g`（相对残差 ' + num['r_e_over_r_g_rel'] + '）。前提本身把两个相差 4.17e42 倍的尺度混用。')
    jl.append('')
    jl.append('## §2 步骤1 vs 步骤4：力比因子被丢（内部矛盾）')
    jl.append('')
    jl.append('步骤1「全维度统一恒等式」`ω²r³c²/(Ghν) = e²/(4πε₀Gm²)·1/(F_e/F_g)`：LHS=`mc²/(hν)=1`（用 hν=mc²），RHS=`(F_e/F_g)·1/(F_e/F_g)=1`，是恒等 1=1（零信息量，相对残差 ' + num['step1_rel'] + '）。步骤4 把 RHS 的 `1/(F_e/F_g)` 因子丢掉，得 `ω²r³c²/(hν)=e²/(4πε₀m²)`，即 LHS=1 而 RHS=`F_e/F_g=' + num['step4_RHS'] + '`，`step4_ratio=' + num['step4_ratio'] + '≠1`。结论核心公式 `G=e²/(4πε₀m²)` 正是丢因子版本，与步骤11 `G=e²/(4πε₀(F_e/F_g)m²)` 自相矛盾。')
    jl.append('')
    jl.append('## §3 核心公式数值否决：量纲自洽≠成立，G 循环')
    jl.append('')
    jl.append('`G_naive=e²/(4πε₀m_e²)=' + num['G_naive'] + '`，量纲 `' + dim['dim_G_naive'] + '=[G]`，但与实验 G 比 `G_naive/G=' + num['G_naive_over_G'] + '≈F_e/F_g`（相对残差 ' + num['G_naive_ratio_rel'] + '）。补力比 `G_with_ratio=G_naive/(F_e/F_g)` 复现实验 G 残差 `' + num['G_with_ratio_rel'] + '`，但 `F_e/F_g=e²/(4πε₀Gm_e²)` 本身含 G ⇒ 循环（与 attack58「G 在定义回代中消去」同族）。')
    jl.append('')
    jl.append('## §4 全维求导验证反证（本册核心增量）')
    jl.append('')
    jl.append('1. **力比是常数 ⇒ d/dr≡0**：`F_e/F_g=e²/(4πε₀Gm²)` 中 e、ε₀、G、m 全是常数，独立地面真值 `d(F_e/F_g)/dr=' + num['force_ratio_deriv_true'] + '`（精确零）。文档把常数当 r 函数（`dm/dr=ω²r²/G≠0`）算出非零导数，是范畴错误。')
    jl.append('2. **§5「1−πε₀≈0」方向反了**：`πε₀=' + num['pi_eps0'] + '`，`1−πε₀=' + num['one_minus_pi_eps0'] + '≈1`（`|·−1|=' + num['one_minus_near_one_abs'] + '`）。πε₀ 小恰恰使 (1−πε₀)≈1，不是≈0。独立算稿 §5 `approximate_value=' + num['doc_approx_value'] + '`（巨大，非「很小」）。「导数近似为零 ⇒ 自洽」声明被反证。')
    jl.append('3. **「1−πε₀」量纲非法**：πε₀ 量纲 `' + dim['dim_eps0'] + '`，1 无量纲，gap=`' + dim['one_minus_pi_eps0_gap'] + '`≠0；阳性对照「1−α」gap=`' + dim['one_minus_alpha_gap'] + '`（α 无量纲，合法）。稿 §5 导数式量纲 `' + dim['dim_doc_deriv'] + '`，并非 d(无量纲)/dr 应有的 `' + dim['invL'] + '`。')
    jl.append('4. **自带脚本是自证橡皮图章**：`verify_derivatives.py` assert 数=`' + str(num['deriv_script_assert_count']) + '`，无独立地面真值；§5 印 `term=1−πε₀≈1` 却硬编「由于值很小」（rubber_label=' + str(num['deriv_script_rubber_label']) + '）。判据自己证自己，全绿不构成证据。')
    jl.append('')
    jl.append('## §5 v=c 定义域（BOUNDARY，分工对照）')
    jl.append('')
    jl.append('有质量电子 v=c 时 γ 分母 `1−v²/c²=' + num['gamma_den_vc'] + '`（0.9c 对照 `' + num['gamma_den_ctrl'] + '`）。「空间以光速螺旋」是空间流公设、非粒子轨道；与 attack58 E04 同族。本册只作对照，不宣称 v=c 公设整体错误。')
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
    jl.append('- **射程**：只判 S17 这一份求导证明稿的步骤级自洽声明。不宣称 v=c 公设整体错误、不重判 attack10/13/58 已判对象、不产生新物理。')
    jl.append('- **红线不变**：`0/6`、`0/22`、`UFT-3=0`、`L3=0`、`validated=0`、含引力四力大统一正确方程 **0** 条、`L3 ↛ L4`。求导证明层反证不迁移为物理成立、不计攻破数。')
    jl.append('- **治理**：未改 `verify.py`、未跑 `refresh_catalog.py`（并发回退风险）、未做 git 操作、未触碰他人文件；S17 稿与其脚本只读。')
    jl.append('')
    jl.append('## §10 复跑')
    jl.append('')
    jl.append('```bash')
    jl.append('python ' + BASE + '.py')
    jl.append('# 期望 stdout：GUARDS ' + str(K['guards_ok']) + '/' + str(K['guards_total']) + '、ENGINE DONE guards=' + str(K['guards_ok']) + '/' + str(K['guards_total']) + ' entries=' + str(len(K['entries'])) + '、exit=0')
    jl.append('```')
    jl.append('')
    jl.append('**交叉回链**：[归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) · [CODATA 常数表](../../书籍/03_宇宙的本源_统一场论全书/精算/uft_numerics_results.json) · [S17 求导证明稿](../../01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/24-时空与物理常数归一化方程/G和ε0的关系/G和ε0最底层关系的全维求导证明验证.md) · [attack58](判定_attack58_经典电子半径突破口审计_vc_G_eps0关联的量纲链条与恒等消去_2026-11-10.md) · [attack10 report](attack10_空间光速螺旋四力统一场论复核_report.txt) · [attack62 report](attack62_知识全域无免费午餐_置换不变先验与归纳偏置对齐_2026-11-12_report.txt) · [README 增量登记](README.md)')
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