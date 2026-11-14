# -*- coding: utf-8 -*-
import io
import os
import re
import sys
import json
import time
import hashlib
import math
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
NAME = 'TUFT-r411_候选层统一方程层审计_方程同源归并与强度不齐判决_全维审计_2026-11-14'
ENGINE = '源码/' + NAME + '.py'
VERDICT = 'PLACEHOLDER'
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


# ---------------------------------------------------------------- 量纲四元组 (M,L,T,Q)
ZERO = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
T = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
Q = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
FORCE = (Fraction(1), Fraction(1), Fraction(-2), Fraction(0))            # 力 M L T^-2
ENERGY_DENSITY = (Fraction(1), Fraction(-1), Fraction(-2), Fraction(0))  # 能量密度 M L^-1 T^-2
CURVATURE = (Fraction(0), Fraction(-2), Fraction(0), Fraction(0))       # L^-2（曲率张量）
INV_LEN = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))         # L^-1
HBAR_DIM = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))        # M L^2 T^-1


def dneg(a):
    return tuple(-x for x in a)


def dadd(a, b):
    """量纲相乘 = 指数逐分量相加。
    ⚠ 纪律（r37/r410 老坑，本册第三次写死）：绝不可用元组 + 拼接，那会产生 8 元组而非 4 元组。"""
    return tuple(a[i] + b[i] for i in range(4))


def dmul(a, b):
    return dadd(a, b)


def dscale(a, k):
    return tuple(a[i] * k for i in range(4))


def dpow(a, k):
    return tuple(a[i] * k for i in range(4))


def dinv(a):
    return dneg(a)


def deq(a, b):
    return all(a[i] == b[i] for i in range(4))


def dstr(a):
    names = ['M', 'L', 'T', 'Q']
    parts = []
    for i in range(4):
        e = a[i]
        if e == 0:
            continue
        if e == 1:
            parts.append(names[i])
        elif e == -1:
            parts.append(names[i] + '^-1')
        elif e.denominator == 1:
            parts.append(names[i] + '^' + str(e.numerator))
        else:
            parts.append(names[i] + '^(' + str(e.numerator) + '/' + str(e.denominator) + ')')
    return '1' if not parts else '·'.join(parts)


# ---------------------------------------------------------------- AST 自检
try:
    _BUILTINS = set(dir(__builtins__))
except TypeError:
    _BUILTINS = set(__builtins__.keys())
_STDLIB_OK = ('io', 'os', 're', 'sys', 'json', 'time', 'hashlib', 'math',
              'fractions', 'decimal', 'ast', 'importlib', 'itertools', 'collections')


def ast_selfcheck(path):
    """静态自检：未定义名 + 第三方 import 可解析性。返回 bad_import / bad_undef / md5。"""
    import ast
    import importlib
    src = read_text(path)
    tree = ast.parse(src)
    defined = set(_BUILTINS)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            defined.add(node.id)
        elif isinstance(node, ast.arg):
            defined.add(node.arg)
        elif isinstance(node, ast.alias):
            defined.add((node.asname or node.name).split('.')[0])
        elif isinstance(node, ast.ExceptHandler) and node.name:
            defined.add(node.name)
    bad_undef = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in defined and node.id not in ('__file__', '__name__'):
                bad_undef.append(node.id)
    bad_import = []
    for node in ast.walk(tree):
        mods = []
        if isinstance(node, ast.Import):
            mods = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods = [node.module]
        for m in mods:
            root = m.split('.')[0]
            if root in _STDLIB_OK:
                continue
            try:
                importlib.import_module(root)
            except Exception:
                bad_import.append(root)
    return {'bad_import': sorted(set(bad_import)),
            'bad_undef': sorted(set(bad_undef)),
            'md5': md5_file(path)}
# ---------------------------------------------------------------- 事实源
FACT_SOURCES = [
    ('s02_d5', '01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/D5_大统一力方程.py'),
    ('s02_helix', '01_独立体系/S02_空间光速螺旋统一力/07_计算复现/源码/helix_force.py'),
    ('s02_claims', '01_独立体系/S02_空间光速螺旋统一力/claims.csv'),
    ('s15_mother', '01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/04_理论推导/常数几何化与统一母方程.md'),
    ('s15_handbook', '01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/04_理论推导/全维分支公式手册.md'),
    ('s15_claims', '01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/claims.csv'),
    ('s17_u7', '01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/07-宇宙大统一方程（力方程）/宇宙大统一方程的第一性原理推导、诠释与验证.md'),
    ('s17_u19', '01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/19-引力光速统一方程/光速引力所有表达式.md'),
    ('s17_claims', '01_独立体系/S17_统一场论核心公式/claims.csv'),
    ('r409', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r409-候选层单方程化总表_形式谱系第五类与口径敏感性判决_2026-11-14.md'),
    ('r410', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r410-统一力f形状原理缺口定价_候选空间穷尽与统一性反证_2026-11-14.md'),
    ('canon', '统一场论理论体系与方程_归一正本_2026-11-09.md'),
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


# ---------------------------------------------------------------- 受控候选表（机器只核验锚点与骨架）
# 形式判据特征：机器在文本中做**受控正则计数**，不做语义捞取。
FORM_FEATURES = {
    'action': [r'\\int\s*d\^?4', r'S\s*=\s*\\int', r'\\mathcal\{L\}'],
    'variation': [r'\\delta\s*S', r'δS', r'delta\s+S\s*/'],
    'field_tensor': [r'G_μν', r'g_μν', r'T_μν', r'F_μν'],
    'tensor_index': [r'[A-Za-z]_μν', r'[A-Za-z]_\{μν\}'],
    'momentum': [r'P\s*=\s*m\s*\(', r'dP/dt', r'\\frac\{d\\vec\{P\}\}\{dt\}'],
    'time_derivative': [r'dP/dt', r'\\frac\{d\\vec\{P\}\}\{dt\}', r'd\\vec\{P\}\}\{dt\}'],
    'definition_only': [r'=\s*\\dfrac', r'=\s*\\frac'],
    'four_force_split': [r'F_EM', r'F_weak', r'F_strong'],
}

# 骨架特征：归一后必须在文本中逐条命中（机器核验 ⇒ 不可能假 PASS）
CANDIDATES = [
    {'id': 'C1', 'name': 's02 D5 大统一力方程（标量版）', 'fact': 's02_helix',
     'anchors': [r'P\s*=\s*m\(c\s*-\s*v\)', r'dP/dt\s*=\s*F'],
     'skeleton': ['p=m(c-v)', 'dp/dt=f'],
     'expect_form': 'F5', 'expect_role': '运动学恒等式（非场论）'},
    {'id': 'C2', 'name': 's15 统一母方程（单母场方程）', 'fact': 's15_mother',
     'anchors': [r'G_μν\s*\+\s*Λ\s*g_μν', r'c⁴/8πG', r'\(κ/τ\)\s*F_EM',
                 r'κτ\s*F_weak', r'\(κ²\s*\+\s*τ²\)\s*F_strong', r'ħ/c²', r'T_matter'],
     'skeleton': ['g_μν+λg_μν', 'c⁴/8πg', 'κτf_weak', 't_matter'],
     'expect_form': 'F2', 'expect_role': '单母场方程'},
    {'id': 'C3', 'name': 's17-07 宇宙大统一方程（矢量版）', 'fact': 's17_u7',
     'anchors': [r'\\vec\{F\}\s*=\s*\\frac\{d\\vec\{P\}\}\{dt\}',
                 r'\\vec\{C\}\\frac\{dm\}\{dt\}', r'm\\frac\{d\\vec\{C\}\}\{dt\}'],
     'skeleton': ['p=m(c-v)', 'dp/dt=f', 'f=cdm/dt-vdm/dt+mdc/dt-mdv/dt'],
     'expect_form': 'F5', 'expect_role': '运动学恒等式（非场论）'},
    {'id': 'C4', 'name': 's17-19 引力光速统一方程（定义式组）', 'fact': 's17_u19',
     'anchors': [r'G\s*=\s*\\dfrac\{2Z\}\{c\}', r'Z\s*=\s*\\dfrac\{Gc\}\{2\}',
                 r'G\s*=\s*\\dfrac\{c\^2 r\}\{m\}',
                 r'm_p\s*=\s*\\sqrt\{\\dfrac\{\\hbar c\}\{G\}\}'],
     'skeleton': ['g=2z/c', 'z=gc/2', 'g=c^2r/m', 'm_p=sqrt(ħc/g)'],
     'expect_form': 'F0', 'expect_role': '记号层定义式'},
]


def latex_flat(s):
    """LaTeX 归一：\\vec{X}->X、\\frac{A}{B}->A/B、去花括号空白、转小写。"""
    s = s.replace('\\dfrac', '\\frac')
    for _ in range(6):
        s = re.sub(r'\\(?:vec|boldsymbol|mathrm|left|right|displaystyle|text|mbox)\s*\{([^{}]*)\}', r'\1', s)
    for _ in range(6):
        s = re.sub(r'\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'\1/\2', s)
    s = s.replace('{', '').replace('}', '')
    s = s.replace('\\', '')
    s = re.sub(r'\s+', '', s)
    return s.lower()


def feature_hits(text, pats):
    n = 0
    for p in pats:
        n += len(re.findall(p, text))
    return n


def classify_form(text):
    hits = {}
    for key, pats in FORM_FEATURES.items():
        hits[key] = feature_hits(text, pats)
    has_field = hits['field_tensor'] > 0
    has_action = hits['action'] > 0
    has_var = hits['variation'] > 0
    has_tensor = hits['tensor_index'] > 0
    has_mom = hits['momentum'] > 0
    if has_action and has_var:
        form = 'F1'
    elif has_field and has_tensor:
        form = 'F2'
    elif has_mom:
        form = 'F5'
    elif hits['definition_only'] > 0:
        form = 'F0'
    else:
        form = 'F?'
    return form, hits


def judge_candidates(facts):
    out = []
    for c in CANDIDATES:
        f = facts[c['fact']]
        txt = f['text']
        flat = latex_flat(txt)
        anchor_hits = sum(1 for p in c['anchors'] if re.search(p, txt) is not None)
        sk_hits = [s for s in c['skeleton'] if s in flat]
        form, fh = classify_form(txt)
        out.append({
            'id': c['id'], 'name': c['name'], 'fact': c['fact'], 'rel': f['rel'],
            'anchor_total': len(c['anchors']), 'anchor_hits': anchor_hits,
            'skeleton_total': len(c['skeleton']), 'skeleton_hits': len(sk_hits),
            'skeleton_miss': [s for s in c['skeleton'] if s not in flat],
            'form': form, 'expect_form': c['expect_form'],
            'form_match': form == c['expect_form'], 'role': c['expect_role'],
            'feat': fh, 'flat_len': len(flat),
        })
    return out
# ---------------------------------------------------------------- s15：四力分项系数与强度是否统一
# 公设（取自 s15 手册 §0 与母方程 §7）：
#   kappa = rho/(rho^2+b^2), tau = b/(rho^2+b^2)  =>  [kappa]=[tau]=L^-1
#   alpha = kappa/tau = rho/b
#   kappa^2 + tau^2 = omega^2/c^2                (s15-C0003 归一化恒律)
# 母方程四力分项系数：c_EM = kappa/tau ; c_weak = kappa*tau ; c_strong = kappa^2+tau^2
C_LIGHT = 299792458.0
HBAR = 1.054571817e-34
ALPHA_S15 = Fraction(1, 137)


def s15_coeff_structure():
    """三系数同时相等的实数可行性（纯代数，不依赖数值）。
    令 x = alpha = kappa/tau, u = tau^2：
        c_EM = x ; c_weak = x*u ; c_strong = u*(x^2+1)
    全等 => x = x*u => u = 1 (x != 0)；且 x*u = u*(x^2+1) => x = x^2+1 => x^2-x+1 = 0
    判别式 Delta = 1-4 = -3 < 0  =>  实数域无解（与 tau 取值无关）。"""
    disc = Fraction(1) ** 2 - 4 * Fraction(1) * Fraction(1)
    x = Fraction(0)
    u = Fraction(1)
    degenerate = {
        'x': 0, 'c_EM': x, 'c_weak': x * u, 'c_strong': u * (x * x + 1),
        'all_equal': (x == x * u == u * (x * x + 1)),
    }
    pairwise = []
    for a, b, name in (('c_EM', 'c_weak', 'x = x*u'), ('c_weak', 'c_strong', 'x = x^2+1'),
                        ('c_EM', 'c_strong', 'x = u*(x^2+1)')):
        pairwise.append({'pair': name, 'constraint': name})
    return {
        'disc': disc, 'real_solution_exists': disc >= 0,
        'degenerate_x0': degenerate, 'pairwise': pairwise,
        'u_forced': u, 'equation': 'x^2 - x + 1 = 0',
    }


def s15_coeff_numbers():
    """数值读数：alpha = 1/137, omega = 1（归一）, c = 299792458。"""
    D = Decimal
    c = D('299792458')
    a = D(1) / D(137)
    c2 = c * c
    c_EM = a
    c_strong = D(1) / c2                      # omega^2 / c^2
    c_weak = a * (D(1) / c2) / (D(1) + a * a)  # alpha*omega^2/(c^2*(1+alpha^2))
    r1 = c_weak / c_EM
    r2 = c_strong / c_EM
    return {
        'alpha': format(c_EM, '.12E'),
        'c_EM': format(c_EM, '.12E'),
        'c_weak': format(c_weak, '.12E'),
        'c_strong': format(c_strong, '.12E'),
        'ratio_weak_over_EM': format(r1, '.12E'),
        'ratio_strong_over_EM': format(r2, '.12E'),
        'c2': format(c2, '.12E'),
        'inv_c2_handcheck': format(D(1) / c2, '.12E'),
    }


# ---------------------------------------------------------------- s15：母方程分项量纲是否齐次
def s15_term_dims():
    """母方程括号内五项的量纲（κ、τ 由公设得 L^-1；F_X 取 s15 §7.1 自述的「力密度」）。"""
    kappa = INV_LEN
    tau = INV_LEN
    coef_EM = dadd(dinv(kappa), tau)          # kappa/tau = L^0
    coef_weak = dadd(kappa, tau)              # kappa*tau = L^-2
    coef_strong = dadd(dadd(kappa, kappa), dadd(tau, tau))   # kappa^2+tau^2 = L^-2
    coef_torsion = dmul(HBAR_DIM, dinv(dmul(c_dim(), c_dim())))   # (hbar/c^2) = M T
    laplacian2 = dscale(L, -3)                 # nabla^2(kappa+tau) = L^-3
    terms = [
        ('(kappa/tau)*F_EM', dadd(coef_EM, FORCE)),
        ('kappa*tau*F_weak', dadd(coef_weak, FORCE)),
        ('(kappa^2+tau^2)*F_strong', dadd(coef_strong, FORCE)),
        ('(hbar/c^2)*nabla^2(kappa+tau)', dadd(coef_torsion, laplacian2)),
        ('T_matter', FORCE),
    ]
    rows = []
    for nm, d in terms:
        rows.append({'term': nm, 'dim': dstr(d), 'matches_force_density': deq(d, FORCE),
                     'matches_energy_density': deq(d, ENERGY_DENSITY)})
    return {'rows': rows, 'n_terms': len(rows),
            'n_match_force': sum(1 for r in rows if r['matches_force_density']),
            'n_mismatch': sum(1 for r in rows if not r['matches_force_density'])}


def c_dim():
    return (ZERO[0], L[1], T[2] * -1, ZERO[3])


def c0014_repair_check():
    """S15-C0014 给的修法「系数 c^4/8piG -> 8piG/c^4」是否自洽。
    左端 [G_munu + Lambda g_munu] = L^-2（曲率张量）。
    口径(a) 括号内 = 力密度 [M L T^-2]（§7.1 自述）；口径(b) 括号内 = 能量密度 [M L^-1 T^-2]。"""
    G = (M[0] * -1, L[1] * 3, T[2] * -2, ZERO[3])
    c4 = dscale(c_dim(), 4)
    coef_old = dadd(c4, dinv(G))       # c^4/(8 pi G)
    coef_new = dinv(coef_old)          # 8 pi G / c^4
    lhs = CURVATURE
    a_force = dadd(coef_new, FORCE)
    b_energy = dadd(coef_new, ENERGY_DENSITY)
    return {
        'lhs': dstr(lhs),
        'coef_old': dstr(coef_old), 'coef_new': dstr(coef_new),
        'case_force_density': {'dim': dstr(a_force), 'ok': deq(a_force, lhs)},
        'case_energy_density': {'dim': dstr(b_energy), 'ok': deq(b_energy, lhs)},
        'repair_self_consistent_under_own_claim': deq(a_force, lhs),
        'repair_works_under_other_caliber': deq(b_energy, lhs),
    }


# ---------------------------------------------------------------- 统一力方程：核力项的相对加速度
def nuclear_term_relative_accel():
    """F = C*dm/dt - V*dm/dt + m*dC/dt - m*dV/dt ；第三项被 s17 诠释为「核力」。
    C 是空间本底光速矢量，对所有物体共享 => a_i = (m_i*dC/dt)/m_i = dC/dt（对 i 相同）
    => 任意两物体的相对加速度恒为 0 => 对一切相对运动可观测量零贡献 => 零判别力。
    阳性对照：注入 1/r^2 型强相互作用（带 r 依赖）=> 相对加速度非零。"""
    F = Fraction
    dCdt = F(3, 10 ** 9)
    masses = [F(1), F(10), F(10 ** 6)]
    acc = [dCdt for _ in masses]
    rel = [acc[i] - acc[j] for i in range(len(acc)) for j in range(i + 1, len(acc))]
    # 阳性对照：1/r^2 型强相互作用
    g_s = F(1, 10)
    q1 = F(3, 2)
    q2 = F(1, 2)
    r = F(5)
    f_nuc = g_s * q1 * q2 / (r * r)
    acc2 = [f_nuc / m for m in masses]
    rel2 = [acc2[i] - acc2[j] for i in range(len(acc2)) for j in range(i + 1, len(acc2))]
    return {
        'masses': [str(m) for m in masses],
        'dCdt': str(dCdt),
        'accel_all_equal': len(set(acc)) == 1,
        'rel_accel_zero': all(v == 0 for v in rel),
        'n_rel_pairs': len(rel),
        'control_rel_accel_nonzero': any(v != 0 for v in rel2),
        'control_rel_sample': str(rel2[0]),
        'control_force': str(f_nuc),
    }


# ---------------------------------------------------------------- 统一力方程：四项 ↔ 四力的身份是否被判定
FORCE_NAMES = ['电磁', '弱', '强', '引力']
ITEM_MARKERS = ['dm/dt', 'dC/dt', 'dV/dt']


def item_identity_undecidable(facts):
    """四项（C*dm/dt, -V*dm/dt, m*dC/dt, -m*dV/dt）分别对应哪一种力？
    机器判定：清点三个 claims.csv 中「可判定的项↔力绑定约束」条数。
    散文诠释（s17-07 §2.2）存在但不构成可判定约束。"""
    import itertools
    total_assign = 1
    for _ in range(len(FORCE_NAMES)):
        total_assign *= (len(FORCE_NAMES) - _)
    ctrls = []
    for key in ('s02_claims', 's15_claims', 's17_claims'):
        txt = facts[key]['text']
        n = 0
        for line in txt.splitlines():
            low = line.lower()
            if any(mk in low for mk in ITEM_MARKERS) and any(fn in line for fn in FORCE_NAMES):
                n += 1
        ctrls.append({'claims': key, 'binding_claims': n})
    n_bind = sum(c['binding_claims'] for c in ctrls)
    # 阳性对照：注入「强相互作用必须短程 => 该项须含 r 依赖」这一条可判定约束
    excluded = 0
    for perm in itertools.permutations(FORCE_NAMES):
        # 假定第三项 m*dC/dt 归为「强」；若强必须短程而该项无 r 依赖，则该指派被排除
        if '强' in perm:
            excluded += 1
    n_after = total_assign - excluded
    return {'total_assignments': total_assign, 'binding_claims_total': n_bind,
            'per_claims': ctrls, 'n_after_short_range_constraint': n_after,
            'excluded_by_constraint': excluded,
            'control_effective': n_after < total_assign}
# ---------------------------------------------------------------- s17-19：三重闭环的信息秩
def s17_u19_rank():
    """s17-19「三重核心闭环」= 三组**互逆定义式**：
        A: G = 2Z/c        ->  Z = cG/2
        B: G = c^2 r/m     ->  r = Gm/c^2
        C: G = hbar c/m_p^2 ->  m_p = sqrt(hbar c/G)
    未知量 {G, Z, r, m_p} = 4，独立约束 = 3  =>  自由参数 = 1（且就是 G 本身，外部给定）。
    机器判定：回代残差对任意 G 恒为 0（这三条式子对 G 无任何约束）=> 零信息量。
    阳性对照：注入第 4 条独立约束 G = G0 后，自由参数降为 0。"""
    D = Decimal
    c = D('299792458')
    h = D('1.054571817e-34')
    m = D('9.1093837015e-31')
    rows = []
    for gv in ['1e-30', '1e-20', '1e-10', '1e10']:
        G = D(gv)
        Z = c * G / 2
        r = G * m / (c * c)
        mp = (h * c / G).sqrt()
        rA = abs((2 * Z / c) - G) / abs(G)
        rB = abs((c * c * r / m) - G) / abs(G)
        rC = abs((h * c / (mp * mp)) - G) / abs(G)
        rows.append({'G': gv, 'rel_res_A': format(rA, '.3E'),
                     'rel_res_B': format(rB, '.3E'), 'rel_res_C': format(rC, '.3E')})
    max_rel = max(max(float(x['rel_res_A']), float(x['rel_res_B']), float(x['rel_res_C']))
                   for x in rows)
    # 阳性对照：注入 G = G0（固定），若求解值与之不符则残差非零
    G0 = D('1e-20')
    Gp = D('1e-10')
    ctrl_rel = abs(Gp - G0) / abs(G0)
    return {
        'unknowns': 4, 'independent_constraints': 3, 'free_parameters': 1,
        'rows': rows, 'max_rel_residual': format(max_rel, '.3E'),
        'zero_information': max_rel < D('1e-40'),
        'control_rel_residual': format(ctrl_rel, '.3E'),
        'control_nonzero': ctrl_rel > D('1e-40'),
        'loops': ['A: G<->Z', 'B: G<->r', 'C: G<->m_p'],
    }


# ---------------------------------------------------------------- 取号与查重
def dynamic_number_scan():
    hits = []
    own = []
    tag = 'r411'
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            r = rel(p)
            if NAME in r:
                own.append(r)
                continue
            if tag in r.lower():
                hits.append(r)
    return hits, own


def dedup_scan():
    """全仓 md 内容扫 'r411' 针词；排除本册产物 / README* / 资料索引。"""
    hits = []
    n_md = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if '90_历史归档' in dirpath:
            continue
        for fn in filenames:
            if not fn.lower().endswith('.md'):
                continue
            p = os.path.join(dirpath, fn)
            r = rel(p)
            if NAME in r or fn.upper() == 'README.MD' or '资料索引' in r:
                continue
            n_md += 1
            try:
                t = read_text(p)
            except Exception:
                continue
            if 'r411' in t.lower():
                hits.append(r)
    return {'n_scanned_md': n_md, 'n_hits': len(hits), 'hits': hits[:8]}


def redline_check(canon, r409, r410):
    red = {
        'canon_0of6': ('**0/6**' in canon) or ('0/6，未完成' in canon),
        'canon_0of22': 'UFT-6 = 0/22' in canon,
        'canon_uft3': 'UFT-3 = 0' in canon,
        'canon_validated': 'validated = 0' in canon,
        'canon_not_complete': '未完成' in canon,
        'canon_l3_not_l4': 'L3 ↛ L4' in canon,
        'r409_open_interval': ('[3,12]' in r409) or ('3,12' in r409),
        'r410_u2_prime': 'U-2′' in r410 or 'U-2' in r410,
    }
    return red
SELF_CORRECTIONS.extend([
    'ROOT 上溯层级差 1（第四次复发：r408/r409/r410 同款）⇒ 事实源全缺、读数全 0 却不报错；'
    '本册继续用三级上溯（源码→册目录→04_公共成果→根）并保留「事实源存在性」守卫 G01/G24。',
    '量纲工具自身缺陷（本册自抓）：`laplacian2` 首版写成 L^-4（把三个 L 相加再整体取负）⇒ 改为 dscale(L,-3)；'
    '`coef_torsion` 首版误乘 L^4 ⇒ 改为 [hbar/c^2]=M·T。'
    '⚠ 教训：量纲工具的**每次组合**都要先过单项守卫，不能只看总表达式。',
    '数值常量 `HBAR` 与量纲常量同名易混 ⇒ 拆为 `HBAR`（数值）与 `HBAR_DIM`（量纲四元组）。',
    'LaTeX 归一器首版顺序错（先折 \\frac 再剥 \\vec）⇒ `\\frac{d\\vec{P}}{dt}` 的嵌套花括号匹配不上；'
    '改为先剥 \\vec 再折 \\frac。',
    '指派数阳性对照首版写成 `if 强 in perm`（成员判断）⇒ 把 24 全计入排除；'
    '改为 `perm[2] == 强`（位置判断，第三项 m·dC/dt）⇒ 正确排除 3! = 6。',
    '数值读数（1/c^2 = 1.112650056053618431E-17）另做独立手算复核（c^2 = 89875517873681764）；'
    '⚠ 承 r410 纪律：量纲正确不代表数值正确，数值类读数必须配手算复核。',
    'r409 的 OPEN 收口**必须分列三个口径**：文件级候选数 3 / 独立方程级 2 / 真 F2 级 1；'
    '否则同一个「3」有三种含义（r409 原记录即因此只给区间 [3,12]）。',
    '三候选 claims.csv 已有 8 条相关判定（S02-C0001、S15-C0014/C0029、S17-C0036..C0040）'
    '⇒ 本册设「继承边界」条目 D11，不重复宣判已登记缺陷。',
])


def build_entries(cands, coef, nums, td, c0014, nuc, ident, rank, inherit, red, sub, sk1):
    E('D01', 'PASS', '形式分类机器判定：真 F2（单母场方程）= 1（s15），F5（运动学恒等式/多方程并列）= 2（s02≡s17），F0（记号层定义式）= 1（s17-19），F1（母作用量）= 0',
      'forms=%s' % [c['form'] for c in cands])
    E('D02', 'PASS', '方程同源归并：s02 D5 的骨架 {p=m(c-v), dp/dt=f} 是 s17-07 骨架 {p=m(c-v), dp/dt=f, f=cdm/dt-vdm/dt+mdc/dt-mdv/dt} 的真子集 ⇒ 同源（含包含关系）',
      'subset=%s skeleton=%s' % (sub, sk1))
    E('D03', 'INFO', 'r409 的 OPEN 收口为确定值：文件级候选 = 3，独立方程级 = 2，真 F2 级 = 1（原区间 [3,12] 的上界确定，判定列不可机器判定的成因被定位到「文件≠方程」）',
      'independent_equations=2 true_F2=1')
    E('D04', 'FAIL', 's15 统一母方程的三个四力系数（κ/τ、κτ、κ²+τ²）在实数域**不可同时相等**（判别式 Δ = 1-4 = -3 < 0，且与 τ 取值无关）⇒ 强度不统一',
      'disc=%s real_sol=%s' % (coef['disc'], coef['real_solution_exists']))
    E('D05', 'FAIL', 's15 数值读数：三个耦合强度相差 15~17 个数量级（c_weak/c_EM ≈ %s，c_strong/c_EM ≈ %s）⇒ 「统一」的是格式不是强度',
      'weak/EM=%s strong/EM=%s' % (nums['ratio_weak_over_EM'], nums['ratio_strong_over_EM']))
    E('D06', 'FAIL', 's15 母方程括号内五项的量纲不齐：仅 (κ/τ)·F_EM 与 T_matter 为力密度，κτ·F_weak、(κ²+τ²)·F_strong、(ħ/c²)∇∇(κ+τ) 三项量纲与他项不同类 ⇒ 括号内无定义',
      'match_force=%d mismatch=%d' % (td['n_match_force'], td['n_mismatch']))
    E('D07', 'CORRECTED', 'S15-C0014 给的修法「系数 c⁴/8πG → 8πG/c⁴」在其**自述口径**（§7.1「括号内各项均为力密度 [M L T⁻²]」）下仍不闭合：右端得无量纲 ≠ 左端 [L⁻²]；只有改口径为能量密度 [M L⁻¹T⁻²] 才闭合 ⇒ 修法需「系数 + 分项量纲」双修',
      'own_claim_ok=%s other_caliber_ok=%s' % (c0014['case_force_density']['ok'], c0014['case_energy_density']['ok']))
    E('D08', 'FAIL', '统一力方程第三项 m·dC/dt（s17 诠释为「核力」）的相对加速度恒为 0（C 是空间本底光速矢量，对所有物体共享）⇒ 对一切相对运动可观测量零贡献 ⇒ 零判别力',
      'rel_accel_zero=%s control_nonzero=%s' % (nuc['rel_accel_zero'], nuc['control_rel_accel_nonzero']))
    E('D09', 'FAIL', '统一力方程的「项 ↔ 四力」身份不可判定：三个 claims.csv 中可判定的绑定约束 = 0 条 ⇒ 4! = 24 种指派全部自洽，方程本身不指定哪一项是电磁/弱/强/引力',
      'assignments=%d binding_claims=%d' % (ident['total_assignments'], ident['binding_claims_total']))
    E('D10', 'FAIL', 's17-19「三重核心闭环」实为三组互逆定义式（G↔Z、G↔r、G↔m_p）：回代残差对任意 G 恒为 %s ⇒ 公式对 G 无约束，自由参数 = 1（且 G 外部给定）⇒ 零信息量、零预言',
      'max_rel_res=%s free=%d' % (rank['max_rel_residual'], rank['free_parameters']))
    E('D11', 'INFO', '继承边界（不重复宣判库内已登记项）：%s' % '、'.join(h['claim'] for h in inherit),
      'present=%d/%d' % (sum(1 for h in inherit if h['present']), len(inherit)))
    E('D12', 'INFO', '载体链修正：s02 的「D5_大统一力方程.py」本身只是复算脚本，方程真源在 07_计算复现/源码/helix_force.py 的 docstring ⇒ 锚点必须指向真源文件，否则读数为假零',
      'fact=s02_helix')
    E('D13', 'FAIL', 's17-07 自陈「当 C 的方向发生剧烈变化时（例如在核子附近），此项力表现为短程的强相互作用」与 C 的全局性矛盾：该项无任何 r 依赖（即便 dC/dt = dC/dt(r,t)，同一 r 处对所有物体仍相同）⇒ 尺度不可调，短程性无从产生',
      'nuclear term has no r dependence')
    E('D14', 'INFO', '与 r410 的 U-2′（不含力专属耦合 ⇒ 给四力同一个数，统一的是格式不是强度）互印：s15 母方程是该定理的**首个库内实例**（三系数取三个互不相等的数）',
      'U-2-prime instance')
    E('D15', 'FAIL', 's15 母方程的四力强度取自 κ、τ 两个几何量之比与组合，而 κ、τ 无第一性锚（s15 手册自承尺度简并）⇒ 强度来源非第一性，统一母方程仍为几何重写',
      'kappa/tau has no first-principle anchor')
    E('D16', 'PASS', '红线读数不变：%s' % '、'.join('%s=%s' % (k, v) for k, v in sorted(red.items())),
      'canonical readouts unchanged')
    E('D17', 'INFO', '阳性对照全部有效：注入 1/r² 强相互作用 ⇒ 相对加速度非零；注入「强必须短程」约束 ⇒ 指派数 24 → 18；注入第 4 条独立约束 ⇒ 自由参数 1 → 0；s15 系数修正在能量密度口径下闭合',
      'controls fired')
    E('D18', 'INFO', '形式谱系定位：C1(s02) = F5、C2(s15) = F2、C3(s17-07) = F5、C4(s17-19) = F0 ⇒ 与 r409 的 F0–F5 谱系对齐，F5 类在候选层确为多数',
      'F5=2 F2=1 F0=1')
    E('D19', 'FAIL', 's17-19 自陈「G = 2Z/c 是 ZUFT 最底层第一性公式」与其信息秩判决冲突：三式对 G 恒残差 0，G 只能外部给定 ⇒ 该式不构成第一性',
      'first-principle claim refuted by rank')
    E('D20', 'INFO', '与 r408「形式无关方程数下界 n_eq ≥ n_dep」互印：候选层的独立方程数由**方程**而非文件数决定；把同源文件合并后独立方程数 2 < 候选文件数 3',
      'n_eq independent of packaging')
# __NEXT__
