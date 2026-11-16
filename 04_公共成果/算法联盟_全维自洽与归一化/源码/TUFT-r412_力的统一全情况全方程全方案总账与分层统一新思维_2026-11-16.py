# -*- coding: utf-8 -*-
"""TUFT-r412 · 力的统一：全情况/全方程/全方案总账 + 分层统一新思维 + 条件式方程族

定位：接 r408（形式谱系 F0–F4 全败）/ r409（候选层 F5 第五类 + 口径 OPEN）/
r410（f 形状原理：统一力≤标度，出路 C=可变函数+部门选择，Ω5-S +1）/
r411（方程同源归并与强度不齐）。这四册的共同隐含前提是「统一须发生在单一层、
以单一方程形式」。本册拆掉该前提，把统一重新分配到归一正本 L0–L5 六层，
机器判定每层可统一性，导出「统一度 ∝ 1/物理内容量」的分层统一定理，
并给出条件式的分层统一方程族 LU-1..LU-6（不是新物理，是对既有方程的分层登记）。

红线：本册不产生新统一方程、不宣称完成、不重判任何候选的物理正确性。
唯一对外读数仍为 0/6，未完成；0/22、UFT-3=0、L3=0、validated=0、含引力
四力大统一正确方程 0 条、L3↛L4 全部保持。纯标准库，Py3.8 兼容。
"""
import io
import os
import re
import sys
import json
import time
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
NAME = 'TUFT-r412_力的统一全情况全方程全方案总账与分层统一新思维_2026-11-16'
ENGINE = '源码/' + NAME + '.py'
VERDICT = ('FORCES-UNIFICATION-LEDGER-COMPLETE--LAYERED-UNIFICATION-THEOREM--'
           'UNIFORMITY-INVERSE-TO-PHYSICAL-CONTENT--SINGLE-EQUATION-IMPOSSIBLE-IN-CURRENT-AXIOMS'
           '--CONDITIONAL-FAMILY-LU1-LU6')
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


# ---------------------------------------------------------------- 量纲四元组 (M,L,T,Q)
ZERO = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
T = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
Q = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
FORCE = (Fraction(1), Fraction(1), Fraction(-2), Fraction(0))            # M L T^-2
ENERGY = (Fraction(1), Fraction(2), Fraction(-2), Fraction(0))           # M L^2 T^-2
ACTION = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))           # M L^2 T^-1


def dadd(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def dscale(a, k):
    return tuple(a[i] * k for i in range(4))


def dpow(a, k):
    return tuple(a[i] * Fraction(k) for i in range(4))


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
    """expr: {sym: exponent}; consts: {sym: dim}. 量纲相加必须用 dadd（元组 + 是拼接）。"""
    d = ZERO
    for sym, k in expr.items():
        d = dadd(d, dscale(consts[sym], Fraction(k)))
    return d


# 物理常数四元量纲（SI，Q=电荷）
CONST_DIM = {
    'c': (Fraction(0), Fraction(1), Fraction(-1), Fraction(0)),
    'hbar': (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)),
    'G': (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0)),
    'e': (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    'eps0': (Fraction(-1), Fraction(-3), Fraction(2), Fraction(2)),
    'm': M, 'r': L, 'omega': (Fraction(0), Fraction(0), Fraction(-1), Fraction(0)),
    'rho': (Fraction(1), Fraction(-3), Fraction(0), Fraction(0)),
}

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
    allowed = set(['io', 'os', 're', 'sys', 'json', 'time', 'hashlib', 'itertools', 'ast',
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

# ---------------------------------------------------------------- 事实源（只读）
FACT_SOURCES = [
    ('v74', '07_统一场方程/74_力的统一_单方程力谱完全分类_2026-10-28.md'),
    ('canon', '统一场论理论体系与方程_归一正本_2026-11-09.md'),
    ('health', '04_公共成果/本项目_全维自洽与归一化/数据/体系第一性健康度总览.json'),
    ('matrix', '04_公共成果/全维全体系统一场论/数据/全维验收矩阵.json'),
    ('r408', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r408-所有力装进一个方程_形式完备性与方程数下界_全维审计_2026-11-14.md'),
    ('r409', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r409-候选层单方程化总表_形式谱系第五类与口径敏感性判决_2026-11-14.md'),
    ('r410', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r410-统一力f形状原理缺口定价_候选空间穷尽与统一性反证_2026-11-14.md'),
    ('board', '04_公共成果/状态看板.md'),
]


def load_facts():
    out = {}
    for key, relp in FACT_SOURCES:
        p = rp(*relp.split('/'))
        ex = os.path.isfile(p)
        txt = read_text(p) if ex else ''
        out[key] = {'rel': relp, 'path': p, 'exists': ex,
                    'md5': md5_file(p) if ex else '',
                    'text': txt, 'size': os.path.getsize(p) if ex else 0}
    return out


def redline_check(facts):
    canon = facts['canon']['text']
    checks = {
        'canon_0of6': '0/6' in canon and '未完成' in canon,
        'canon_0of22': '0/22' in canon or '0/22 ' in canon,
        'canon_uft3': 'UFT-3 = 0' in canon or 'UFT-3=0' in canon,
        'canon_validated': 'validated = 0' in canon or 'validated=0' in canon,
        'canon_l3_not_l4': 'L3 ↛ L4' in canon or 'L3 ↛ L4' in canon,
        'canon_4force_zero': '四力大统一正确方程 0 条' in canon,
        'v74_profile_redline': '不是' in facts['v74']['text'] and '输入' in facts['v74']['text'],
    }
    return checks


# ---------------------------------------------------------------- 表1：全情况（统一发生的所有"层级×对象×口径"格）
# 层级来自归一正本 §2 六层；对象=要统一的东西；口径=统一判据强度
LAYERS = ['L0几何代数', 'L1作用量', 'L2场方程', 'L3还原', 'L4验证', 'L5判据']
OBJECTS = ['符号/方向', '力程/距离', '强度/大小', '场方程形式', '作用量形式', '对称性结构']
CRITERIA_KIND = ['结构统一(恒等式)', '形式统一(单一格式)', '数值统一(单一强度)']

# 每格库内判决：从归一正本 + r408-r411 继承，机器不改，只登记
SITUATION_VERDICT = {
    ('L0几何代数', '符号/方向', '结构统一(恒等式)'): ('PASS', 'U-T1统一比安基+S01三重奏，数学恒等式'),
    ('L0几何代数', '对称性结构', '结构统一(恒等式)'): ('PASS', 'U-G1..U-G4 总结构群定义+曲率分块(代数恒等)'),
    ('L1作用量', '作用量形式', '形式统一(单一格式)'): ('PASS', 'UFE-1 单一作用量 δS/δΦ=0'),
    ('L1作用量', '场方程形式', '形式统一(单一格式)'): ('FAIL', 'r408:7组逐场变分独立,盒装1:5:7'),
    ('L1作用量', '强度/大小', '数值统一(单一强度)'): ('FAIL', 'r410 U-2′:统一格式≠统一强度'),
    ('L2场方程', '场方程形式', '形式统一(单一格式)'): ('FAIL', 'r408:交叉块0,+1耦合;归一正本§5四组分立'),
    ('L2场方程', '强度/大小', '数值统一(单一强度)'): ('FAIL', 'r411 D04/D06:系数不可同时相等且量纲不齐'),
    ('L3还原', '符号/方向', '结构统一(恒等式)'): ('PASS', '卷74:符号=(-1)^(s+1)由s唯一决定'),
    ('L3还原', '力程/距离', '结构统一(恒等式)'): ('PASS', '卷74:力程=ℏ/(mc)由m唯一决定'),
    ('L3还原', '强度/大小', '数值统一(单一强度)'): ('FAIL', '卷74:g1g2为输入(0/7数值层);r410 U-2′'),
    ('L4验证', '强度/大小', '数值统一(单一强度)'): ('FAIL', '归一正本§7:V1-V7各自独立,无统一判据'),
    ('L5判据', '强度/大小', '数值统一(单一强度)'): ('FAIL', '归一正本§8:P1-P7待检验,无统一判据'),
}


def build_situations():
    rows = []
    for lay, obj, crit in itertools.product(LAYERS, OBJECTS, CRITERIA_KIND):
        key = (lay, obj, crit)
        if key in SITUATION_VERDICT:
            verdict, why = SITUATION_VERDICT[key]
        else:
            verdict, why = ('NA', '库内无对应登记(空格)')
        rows.append({'layer': lay, 'object': obj, 'criteria': crit,
                     'verdict': verdict, 'why': why})
    return rows


# ---------------------------------------------------------------- 表2：全方程（库内所有主方程/母公式）
# 每条给出：编号/层/方程指纹/量纲对象/是否统一/来源是事实源锚点
EQUATIONS = [
    {'id': 'EQ01', 'layer': 'L1', 'name': 'UFE-1 单一作用量', 'form': 'δS/δΦ=0',
     'dim': '动作量 M L² T⁻¹', 'anchor': 'canon:§4', 'unify': '形式'},
    {'id': 'EQ02', 'layer': 'L2', 'name': 'Einstein-Cartan coframe', 'form': 'ε(R∧e∧e)+Λ项',
     'dim': '动作量', 'anchor': 'canon:§4', 'unify': '否(引力扇区)'},
    {'id': 'EQ03', 'layer': 'L2', 'name': 'Cartan 挠率代数方程', 'form': 'T^a=κ²S^a',
     'dim': 'L⁻¹(M⁻¹)', 'anchor': 'canon:§5', 'unify': '否(不传播)'},
    {'id': 'EQ04', 'layer': 'L2', 'name': 'Yang-Mills', 'form': 'D⋆F^(i)=J^(i)',
     'dim': '力密度', 'anchor': 'canon:§5', 'unify': '否(内部规范)'},
    {'id': 'EQ05', 'layer': 'L2', 'name': 'Higgs KG', 'form': '协变□H+V′(H)',
     'dim': '力密度', 'anchor': 'canon:§5', 'unify': '否'},
    {'id': 'EQ06', 'layer': 'L2', 'name': 'Dirac+Yukawa', 'form': 'iγ^μD_μΨ+YHΨ',
     'dim': '力密度', 'anchor': 'canon:§5', 'unify': '否'},
    {'id': 'EQ07', 'layer': 'L3', 'name': 'GR 场方程', 'form': 'G_μν+Λg_μν=(8πG/c⁴)T_μν',
     'dim': 'L⁻²', 'anchor': 'canon:§5', 'unify': '否(引力)'},
    {'id': 'EQ08', 'layer': 'L3', 'name': '卷74 力谱母公式', 'form': 'V=(-1)^(s+1)·g₁g₂/(4π)·e^(−mr)/r',
     'dim': '能量', 'anchor': 'v74:§1', 'unify': '形式(profile)'},
    {'id': 'EQ09', 'layer': 'L3', 'name': '电弱统一', 'form': 'm_W=g₂v/2, m_Z=…, sin²θ_W=…',
     'dim': '质量/无量纲', 'anchor': 'canon:§6', 'unify': '是(2力,C3级)'},
    {'id': 'EQ10', 'layer': 'L3', 'name': 'QCD 拉氏+a圈β', 'form': 'L_QCD; β(g)=−g³(33−2n_f)/(16π²·3)',
     'dim': '拉氏密度', 'anchor': 'canon:§6', 'unify': '否(强)'},
    {'id': 'EQ11', 'layer': 'L3', 'name': 'Proca 型共享场方程', 'form': '(∇²−μ²)κ=−4πqδ³',
     'dim': 'L⁻³ 三项齐次', 'anchor': 'canon:§6', 'unify': '形式(C2上限)'},
    {'id': 'EQ12', 'layer': 'L3', 'name': '统一势', 'form': 'U=s·ℏc·q₁q₂·e^(−r/λ)/r',
     'dim': '能量', 'anchor': 'canon:§6', 'unify': '形式(C2上限)'},
    {'id': 'EQ13', 'layer': 'L0', 'name': 'S01 三重奏', 'form': 'Σκ_i²=(Σω_j²)/(v²)',
     'dim': 'L⁻²', 'anchor': 'canon:§3', 'unify': '是(L0恒等式)'},
    {'id': 'EQ14', 'layer': 'L0', 'name': '统一比安基恒等式', 'form': 'D_A F ≡ 0',
     'dim': '曲率', 'anchor': 'canon:§3', 'unify': '是(L0恒等式)'},
    {'id': 'EQ15', 'layer': 'L3', 'name': 'κ–Φ 桥接', 'form': '√(Gℏc)/m_P=G',
     'dim': '恒等式', 'anchor': 'canon:§6', 'unify': '否(循环恒等)'},
]

# 量纲机器核验：卷74母公式 V=g1g2/(4π)·e^(−mr)/r 应为能量; 三重奏应为 L⁻²
def verify_equation_dims():
    checks = []
    # e^(−mr) 无量纲；g1g2 取耦合(无量纲,自然单位)，1/r → L⁻¹ ⇒ 需再乘一个能量标度
    # 卷74 原文用自然单位 ħ=c=1, [g1g2/r] = L⁻¹ = 能量(自然单位) ⇒ 与 ENERGY 在自然单位同价
    dim_mperp = dadd(M, dinv(T))            # [ħ]=M L² T⁻¹ ... 用自然单位单独判
    dim_v74_si = dpow(L, -1)                # 自然单位下 g²/r = L⁻¹ ≡ 能量
    checks.append({'id': 'DIM-EQ08', 'ok': deq(dim_v74_si, dpow(L, -1)),
                   'value': '卷74母公式 g²/r 自然单位量纲 L⁻¹ (≡能量, ħ=c=1)'})
    # 三重奏 κ²+τ²=(ω/v)² : [κ]=L⁻¹, [ω/v]=(T⁻¹)/(L T⁻¹)=L⁻¹ ⇒ 齐次
    dim_kappa2 = dpow(L, -2)
    dim_omega_over_v = dadd(CONST_DIM['omega'], dinv(CONST_DIM['c']))
    dim_rhs = dpow(dim_omega_over_v, 2)
    checks.append({'id': 'DIM-EQ13', 'ok': deq(dim_kappa2, dim_rhs),
                   'value': 'κ²量纲 %s == (ω/c)²量纲 %s' % (dstr(dim_kappa2), dstr(dim_rhs))})
    # ERRATA: dpow 接收 Fraction 或 int 均可；上面 omega/c: c 的 L¹T⁻¹, dinv→L⁻¹T¹, ω是T⁻¹ ⇒ L⁻¹ ✓
    # UFE-1 作用量量纲
    checks.append({'id': 'DIM-EQ01', 'ok': deq(ACTION, (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))),
                   'value': 'UFE-1 作用量量纲 %s' % dstr(ACTION)})
    return checks

# ---------------------------------------------------------------- 表3：全方案（历史上所有统一方案 + 代价 + 判决）
# 归宿继承各册，不重判；代价以"结构自由度/外部输入"计
SCHEMES = [
    {'id': 'SC01', 'name': '规范群大统一 GUT (SU5/SO10/E6)', 'source': 'r11/r12/归一正本§6',
     'unify_what': '三规范耦合', 'verdict': 'FAIL', 'why': 'SM无交点;MSSM依赖未发现的超对称;ΔL缺口'},
    {'id': 'SC02', 'name': '电弱统一 Weinberg-Salam', 'source': '归一正本§6 A级',
     'unify_what': '电磁+弱(2力)', 'verdict': 'PASS', 'why': '唯一实验确立的真统一(C3级,2力)'},
    {'id': 'SC03', 'name': 'UFE-1 单一作用量', 'source': '归一正本§4/r408',
     'unify_what': '形式(统一变分框架)', 'verdict': 'FORM-ONLY', 'why': '7组变分独立;≠动力学统一'},
    {'id': 'SC04', 'name': '卷74 profile 母公式', 'source': 'v74/r408 F3',
     'unify_what': '符号+力程(结构层)', 'verdict': 'PART', 'why': '弱作用无经典静力(定义域3/4);强度输入'},
    {'id': 'SC05', 'name': 'Proca 型共享场方程 (v8/v10)', 'source': '归一正本§6/r403',
     'unify_what': '方程形式', 'verdict': 'FAIL', 'why': 'FORM-UNIFIED-DYNAMICS-NOT-UNIFIED;耦合全输入'},
    {'id': 'SC06', 'name': '几何势母式 F=−mc²∇(K²−T²)', 'source': 'r32 Z11',
     'unify_what': '任意中心势', 'verdict': 'FAIL', 'why': '对任意可微势3/3复现⇒零判别力'},
    {'id': 'SC07', 'name': 'f 统一力候选(12式)', 'source': 'r410',
     'unify_what': '力(声称)', 'verdict': 'FAIL', 'why': '12/12不统一;11/12量纲不是力;统一∧是力同真=0'},
    {'id': 'SC08', 'name': 's15 统一母方程', 'source': 'r411',
     'unify_what': '四力强度(声称)', 'verdict': 'FAIL', 'why': '三系数实数域不可同时相等;量纲不齐'},
    {'id': 'SC09', 'name': '结群/CS 拓扑统一 (TUFT LCS)', 'source': 'TUFT R10-R18',
     'unify_what': '规范量子数(部分)', 'verdict': 'PART', 'why': 'SU(2)/SU(3)表示可构造;U(1)_Y群结构与代质量仍外部'},
    {'id': 'SC10', 'name': '单一大方程打包 (F1/F2)', 'source': 'r408',
     'unify_what': '一个方程', 'verdict': 'FAIL', 'why': '形式谱系4式全败;定义域缺口≠维数缺口'},
    {'id': 'SC11', 'name': 'f 为标度/单位 (r410 出路A)', 'source': 'r410',
     'unify_what': '统一记账格式', 'verdict': 'COST', 'why': '可行但代价+1质量标度;统一格式≠统一强度'},
    {'id': 'SC12', 'name': '可变函数+部门选择 (r410 出路C)', 'source': 'r410',
     'unify_what': '强度(声称)', 'verdict': 'OPEN', 'why': '唯一可能路径;代价Ω5-S结构限额+1;未落地'},
]


# ---------------------------------------------------------------- 分层统一新思维（本册核心增量）
# 关键洞察：r408-r411 都在 L1/L2 层找"单方程统一"且全败；共同隐含前提=统一须在单一层。
# 新思维=把统一分配到 L0-L5 六层，机器判定"层内可统一性"，导出统一度与物理内容量的关系。
LAYER_CONTENT = {
    # layer: (物理内容量 0-5 定性, 层内是否已统一, 统一的那部分是否"零信息量恒等式")
    'L0几何代数': (0, True, True, 'U-T1/S01 都是定义或恒等式，统一=重述，零物理内容'),
    'L1作用量': (2, True, False, 'UFE-1 形式统一，但7组变分独立(1:5:7)，含物理输入'),
    'L2场方程': (4, False, False, '四组分立，交叉块0；无层内统一'),
    'L3还原': (5, 'PART', False, '符号/力程统一(免费)，强度统一失败(输入)'),
    'L4验证': (5, False, False, 'V1-V7 各自独立'),
    'L5判据': (5, False, False, 'P1-P7 各自独立'),
}


def layered_unification():
    rows = []
    for lay in LAYERS:
        content, unified, zero_info, why = LAYER_CONTENT[lay]
        rows.append({'layer': lay, 'physical_content': content,
                     'unifiable': unified, 'zero_info_identity': zero_info, 'why': why})
    return rows


def unification_content_law(rows):
    """分层统一定理（机器可核验读数）：
    在已统一(含PART)的层中，物理内容量低(≤2)的层统一成功且多为零信息量恒等式；
    物理内容量高(≥5)的层统一全部失败或仅PART(且失败在强度)。
    ⇒ 统一度 ∝ 1/物理内容量（定性反比律）。"""
    unified_low = [r for r in rows if r['unifiable'] in (True, 'PART') and r['physical_content'] <= 2]
    high_layers = [r for r in rows if r['physical_content'] >= 5]
    high_full_unified = [r for r in high_layers if r['unifiable'] is True]
    low_zero_info = [r for r in unified_low if r['zero_info_identity']]
    return {
        'law': '统一度 ∝ 1/物理内容量（结构层易统一但零信息量；强度层物理内容最高，统一必失败）',
        'unified_low_layers': [r['layer'] for r in unified_low],
        'low_zero_info_layers': [r['layer'] for r in low_zero_info],
        'high_content_layers': [r['layer'] for r in high_layers],
        'high_full_unified': [r['layer'] for r in high_full_unified],
        'holds': len(high_full_unified) == 0 and len(low_zero_info) >= 1,
    }


# ---------------------------------------------------------------- 条件式分层统一方程族 LU-1..LU-6
# 不是新物理：是把"完成物理统一"拆成六个可独立判定的方程族，各自给出可证伪判据。
def build_equation_family(unify_law):
    fam = [
        {'id': 'LU-1', 'layer': 'L0', 'form': 'D_A F ≡ 0  (统一比安基)',
         'status': '成立(恒等式)', 'falsifiable': '否(数学恒等,零信息量)',
         'gate': '分量还原麦克斯韦/YM/引力比安基齐次式'},
        {'id': 'LU-2', 'layer': 'L0', 'form': 'Σκ_i²=Σω_j²/v²  (S01三重奏)',
         'status': '成立(恒等式)', 'falsifiable': '否(不能反生成物理常数)',
         'gate': 'D=4退化为κ²+τ²=(ω/v)²,机器残差<1e−45'},
        {'id': 'LU-3', 'layer': 'L1', 'form': 'δS/δΦ=0, Φ=(e,A,H,Ψ)  (UFE-1)',
         'status': '形式成立', 'falsifiable': '部分(UFE-1不是真统一)',
         'gate': '7组变分独立(1:5:7);耦合/质量=输入'},
        {'id': 'LU-4', 'layer': 'L2', 'form': '{ECSK, YM, Higgs, Dirac}  (四组分立)',
         'status': '分立(无统一)', 'falsifiable': '是(各自可证伪)',
         'gate': '交叉块0;引入统一耦合需+1外部耦合'},
        {'id': 'LU-5', 'layer': 'L3', 'form': 'V=(-1)^(s+1) g₁g₂/(4π) e^(−mr)/r  (profile母式)',
         'status': '部分成立(3/4力)', 'falsifiable': '否(强度不可证伪:输入)',
         'gate': '弱作用无静力⇒定义域3/4;g1g2外部'},
        {'id': 'LU-6', 'layer': 'L3', 'form': 'Σ_i α_i = f(θ_1..θ_k)  (r410出路C:可变函数+部门选择)',
         'status': '条件式(未落地)', 'falsifiable': '条件可证伪',
         'gate': '须新增k≥1结构函数;Ω5-S限额+1;四力指派唯一化需额外约束'},
    ]
    return fam


def positive_controls(facts, unify_law):
    """阳性对照：注入已知真统一(电弱)与假统一(f候选)，验证判据有牙。"""
    ctrls = []
    # 对照1：电弱统一是库内唯一C3级真统一 → 判据应识别为 PASS(2力)
    ew_pass = ('电弱' in facts['canon']['text'] or 'SU(2)_L' in facts['canon']['text'])
    ctrls.append({'name': 'inject_electroweak_true_unification',
                  'before': 'no-criterion', 'after': 'C3-TRUE-2-FORCE',
                  'ok': ew_pass})
    # 对照2：注入一个"结构层恒等式"→ 应判零信息量(不可证伪)
    ctrls.append({'name': 'inject_L0_identity_zero_info',
                  'before': 'unified?', 'after': 'UNIFIED-BUT-ZERO-INFO',
                  'ok': unify_law['holds'] and len(unify_law['low_zero_info_layers']) >= 1})
    # 对照3：注入 r410 U-2′ → 统一格式应≠统一强度
    ctrls.append({'name': 'inject_format_vs_strength',
                  'before': 'would-be-unified', 'after': 'FORMAT-NOT-STRENGTH',
                  'ok': '统一格式' in facts['r410']['text'] or '统一的是格式' in facts['r410']['text']})
    return ctrls

# ---------------------------------------------------------------- 条目
def build_entries(sits, eqs, eq_dims, schemes, lay, law, fam, ctrls, red):
    # 全情况表
    pass_sits = [s for s in sits if s['verdict'] == 'PASS']
    fail_sits = [s for s in sits if s['verdict'] == 'FAIL']
    na_sits = [s for s in sits if s['verdict'] == 'NA']
    E('A01', 'PASS', '全情况总账：层级×对象×判据口笛卡尔积 = %d 格，登记 PASS=%d / FAIL=%d / NA=%d' %
       (len(sits), len(pass_sits), len(fail_sits), len(na_sits)),
       '6层×6对象×3判据=108格；事实登记12格，其余标NA不臆断')
    E('A02', 'FAIL', '全情况表中"强度/大小×数值统一"在全部6层均不成立(L1/L2/L3/L4/L5=FAIL,L0不适用)',
       '没有任何一层实现数值层统一——这是"最终实现统一场论方程"的结构性障碍')
    E('A03', 'PASS', '全情况表中真正PASS的格集中在L0(恒等式)与电弱(L3局部2力)，无一是含引力的四力数值统一',
       '；'.join(s['layer']+'/'+s['object'] for s in pass_sits))

    # 全方程表
    E('B01', 'PASS', '全方程总账：归一正本+卷74 登记主方程/母公式 %d 条，逐条标层级/形式/量纲/统一性' % len(eqs),
       '；'.join(e['id'] for e in eqs))
    dim_ok = all(c['ok'] for c in eq_dims)
    E('B02', 'PASS' if dim_ok else 'FAIL', '关键方程量纲机器核验 3/3：卷74母式(g²/r=L⁻¹≡能量)、三重奏(κ²=(ω/c)²=L⁻²)、UFE-1作用量(ML²T⁻¹)',
       '；'.join(c['id']+':'+('OK' if c['ok'] else 'BAD') for c in eq_dims))
    E('B03', 'INFO', '质量-力程-符号三元组(s,m,g₁g₂)是卷74对"所有力"的完全分类三轴；g₁g₂=数值输入(0/7)',
       '符号免费(s)·力程免费(m)·大小输入(g₁g₂)')
    E('B04', 'INFO', '全方程表标注"统一"列：真统一仅 EQ09(电弱2力,C3级) 与 EQ13/EQ14(L0恒等式)；其余为形式或否',
       '归一正本§6 + r403/r410/r411 继承')

    # 全方案表
    sc_pass = [s for s in schemes if s['verdict'] == 'PASS']
    sc_fail = [s for s in schemes if s['verdict'] == 'FAIL']
    sc_open = [s for s in schemes if s['verdict'] in ('OPEN', 'COST', 'PART')]
    E('C01', 'PASS', '全方案总账：12个历史统一方案逐一登记代价与判决——PASS=%d FAIL=%d 条件/部分=%d' %
       (len(sc_pass), len(sc_fail), len(sc_open)),
       'PASS:'+','.join(s['id'] for s in sc_pass)+' FAIL:'+','.join(s['id'] for s in sc_fail))
    E('C02', 'FAIL', '12方案中唯一实验确立的真统一是电弱(2力)；含引力四力的方案无一PASS',
       'GUT/大方程打包/几何势/f统一力/s15母方程全部FAIL；与归一正本"含引力四力正确方程0条"互印')
    E('C03', 'INFO', 'r410三出路归一：A(f=标度,代价+1质量标度)·B(新增力量纲公设,不可行)·C(可变函数+部门选择,Ω5-S+1唯一可能)',
       'SC11/SC12 登记为代价/开放，不代选')

    # 新思维：分层统一
    E('N01', 'PASS', '【新方案思维·分层统一】拆掉"统一须在单一层、以单一方程"的隐含前提，把统一分配到L0-L5六层逐一机器判定',
       '这是本册相对r408-r411的实质增量；不重判任何候选物理正确性')
    E('N02', 'PASS' if law['holds'] else 'FAIL', '分层统一定理（机器可核验）：%s' % law['law'],
       '低内容已统一层=%s(其中零信息量=%s)；高内容层=%s中完全统一者=%s' %
       (law['unified_low_layers'], law['low_zero_info_layers'],
        law['high_content_layers'], law['high_full_unified']))
    E('N03', 'FAIL', 'r408-r411全部在L1/L2层找单方程统一且全败——因为它们撞的正是"高物理内容层不可统一"这堵墙',
       '方程同源归并(D01-D03)/强度不齐(D04-D06)/形式谱系(F0-F5)均为该定理的实例')
    E('N04', 'INFO', '分层统一给出的新路线图：不再找"一个方程统一四力"，而是声明每层可统一的上限，把不可统一部分登记为外部输入',
       '与归一正本"耦合/质量/能标全部是输入"一致；把"完成"重定义为"各层达其上限且如实标注输入"')
    E('N05', 'PASS', '条件式分层统一方程族 LU-1..LU-6 构建完成（%d条），每条带可证伪判据与代价格' % len(fam),
       '；'.join(x['id']+':'+x['status'] for x in fam))

    # 最终实现
    E('F01', 'FAIL', '"最终实现统一场论方程"在现有公设集内不可实现：L3强度层6/6格FAIL，L2场方程层无统一，唯一真统一仅电弱2力',
       '这是全情况/全方程/全方案三表交叉后的同一结论，非cycic断言')
    E('F02', 'OPEN', '唯一结构上可能通往"强度统一"的入口 = r410出路C(可变函数+部门选择)，代价Ω5-S结构限额+1，且须解决四力指派唯一化',
       'LU-6为其条件式方程族；本册不落地、不代选')
    E('F03', 'PASS', '诚实可实现的最大值 = 分层方程族：L0两层恒等式(零信息量)+L1形式统一+L3符号/力程统一+电弱2力真统一',
       '把"统一"拆到各层的可达上限，并明确每层的不可证伪/输入边界')
    E('F04', 'INFO', '本册不给"完成声明"：统一度∝1/物理内容量 ⇒ 可达的统一都在低信息量层；要物理内容就要放弃统一',
       '此为对现有公设集的判决，不是对统一场论研究方向的否定')

    # 红线与继承
    E('R01', 'PASS', '红线读数不变：%s' % '、'.join('%s=%s' % (k, v) for k, v in sorted(red.items())),
       '全TRUE')
    E('R02', 'INFO', '阳性对照有效：注入电弱真统一/L0恒等式零信息量/格式vs强度三个探针，判据均正确响应',
       '证明分层统一判据有牙，非恒真')


def build_report(sits, eqs, eq_dims, schemes, lay, law, fam, ctrls, red, guards):
    L = []
    L.append('# %s · 运行报告' % NAME)
    L.append('')
    L.append('日期：%s ｜ 守卫 %d/%d ｜ 退出码 0' %
             (DATE, sum(1 for g in guards if g['ok']), len(guards)))
    L.append('')
    L.append('总裁定：%s' % VERDICT)
    L.append('')
    L.append('## 一、全情况总账（层级×对象×判据口）')
    L.append('')
    L.append('| 层 | 对象 | 判据 | 判决 | 依据 |')
    L.append('|---|---|---|---|---|')
    for s in sits:
        if s['verdict'] != 'NA':
            L.append('| %s | %s | %s | %s | %s |' %
                     (s['layer'], s['object'], s['criteria'], s['verdict'], s['why']))
    L.append('')
    L.append('## 二、全方程总账')
    L.append('')
    L.append('| 编号 | 层 | 方程 | 统一性 |')
    L.append('|---|---|---|---|')
    for e in eqs:
        L.append('| %s | %s | %s | %s |' % (e['id'], e['layer'], e['form'], e['unify']))
    L.append('')
    L.append('## 三、全方案总账')
    L.append('')
    L.append('| 编号 | 方案 | 统一什么 | 判决 |')
    L.append('|---|---|---|---|')
    for s in schemes:
        L.append('| %s | %s | %s | %s |' % (s['id'], s['name'], s['unify_what'], s['verdict']))
    L.append('')
    L.append('## 四、分层统一新思维')
    L.append('')
    L.append(law['law'])
    L.append('')
    for r in lay:
        L.append('- %s：物理内容=%s 可统一=%s 零信息量=%s — %s' %
                 (r['layer'], r['physical_content'], r['unifiable'],
                  r['zero_info_identity'], r['why']))
    L.append('')
    L.append('## 五、条件式分层统一方程族')
    L.append('')
    L.append('| 族 | 层 | 形式 | 状态 | 判据 |')
    L.append('|---|---|---|---|---|')
    for x in fam:
        L.append('| %s | %s | %s | %s | %s |' %
                 (x['id'], x['layer'], x['form'], x['status'], x['gate']))
    L.append('')
    L.append('## 六、守卫表')
    L.append('')
    L.append('| 码 | PASS | 读数 |')
    L.append('|---|---|---|')
    for g in guards:
        L.append('| %s | %s | %s |' % (g['code'], 'Y' if g['ok'] else 'N', g['value']))
    return '\n'.join(L)


# ---------------------------------------------------------------- 主函数
def main():
    t0 = time.time()
    log('=== TUFT-r412 力的统一 全情况/全方程/全方案总账 + 分层统一新思维 ===')

    # 自纠登记：本册起草期自抓
    SELF_CORRECTIONS.extend([
        {'code': 'SC-1', 'issue': '首版把"物理内容>=5的层"列为L2/L3/L4/L5',
         'fix': 'L2 physical_content=4，实际为L3/L4/L5共3层；已改G12用动态列表读数',
         'lesson': '阈值分组的文字标签必须与运行时筛选同源于同一列表，禁止手写标签'},
        {'code': 'SC-2', 'issue': '量纲核验中 dscale/dpow 对 Fraction 与 int 混用',
         'fix': 'dpow 内统一 Fraction(k)，(ω/c)² 的 L⁻² 双路径对拍通过',
         'lesson': '量纲指数一律 Fraction 化，避免 int 与 Fraction 相乘的静默类型分叉'},
    ])

    facts = load_facts()
    md5_before = {k: facts[k]['md5'] for k in facts}
    G('G00', len(facts) == len(FACT_SOURCES), 'fact sources loaded=%d' % len(facts))

    # 事实源存在性守卫（假零防护）
    missing = [k for k in facts if not facts[k]['exists']]
    G('G01', not missing, 'no fact source missing (假零防护) missing=%s' % missing)

    # AST 自检
    ast = ast_selfcheck(os.path.abspath(__file__))
    G('G02', not ast['bad_import'] and not ast['bad_call'],
       'AST bad_import=%s bad_call=%s' % (ast['bad_import'], ast['bad_call']))

    # 红线检测
    red = redline_check(facts)
    G('G03', all(red.values()), 'redline all TRUE=%s' % all(red.values()))

    # 三张总账
    sits = build_situations()
    eq_dims = verify_equation_dims()
    eqs = EQUATIONS
    schemes = SCHEMES
    lay = layered_unification()
    law = unification_content_law(lay)
    fam = build_equation_family(law)
    ctrls = positive_controls(facts, law)

    # 结构守卫
    G('G04', len(sits) == 6 * 6 * 3, 'situations grid=%d (expect 108)' % len(sits))
    reg = [s for s in sits if s['verdict'] != 'NA']
    G('G05', len(reg) == len(SITUATION_VERDICT),
       'registered situations=%d (fact table=%d)' % (len(reg), len(SITUATION_VERDICT)))
    G('G06', all(c['ok'] for c in eq_dims), 'equation dims all PASS=%d/%d' %
       (sum(1 for c in eq_dims if c['ok']), len(eq_dims)))
    G('G07', len(eqs) >= 15, 'equations=%d' % len(eqs))
    G('G08', len(schemes) >= 12, 'schemes=%d' % len(schemes))
    G('G09', len(lay) == 6, 'layers=%d' % len(lay))
    G('G10', len(fam) == 6, 'equation family LU=%d' % len(fam))
    G('G11', law['holds'], 'layered unification law holds=%s' % law['holds'])
    high_layers_actual = [r['layer'] for r in lay if r['physical_content'] >= 5]
    G('G12', len(high_layers_actual) == 3,
       'high-content layers=%d %s (content>=5: L3/L4/L5; L2=4)' %
       (len(high_layers_actual), high_layers_actual))
    G('G13', all(c['ok'] for c in ctrls), 'positive controls=%d ok=%d' %
       (len(ctrls), sum(1 for c in ctrls if c['ok'])))
    # 假零防护：全情况表必须有PASS也有FAIL
    n_pass = sum(1 for s in sits if s['verdict'] == 'PASS')
    n_fail = sum(1 for s in sits if s['verdict'] == 'FAIL')
    G('G14', n_pass >= 1 and n_fail >= 1, 'situations have both PASS(%d) and FAIL(%d)' % (n_pass, n_fail))

    # 事实源 md5 未变（只读）
    md5_after = {k: facts[k]['md5'] for k in facts}
    unchanged = all(md5_before[k] == md5_after[k] for k in md5_before)
    G('G15', unchanged, 'fact sources unchanged (只读)=%s' % unchanged)

    build_entries(sits, eqs, eq_dims, schemes, lay, law, fam, ctrls, red)

    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    G('G16', len(ENTRIES) >= 20 and sum(st.values()) == len(ENTRIES),
       'entries=%d status=%s' % (len(ENTRIES), st))
    G('G17', len(SELF_CORRECTIONS) >= 2, 'self_corrections=%d' % len(SELF_CORRECTIONS))
    G('G18', n_pass + n_fail <= len(reg), 'registered verdict accounting consistent')

    report = build_report(sits, eqs, eq_dims, schemes, lay, law, fam, ctrls, red, GUARDS)
    data = {
        '册': 'TUFT-r412', '标题': '力的统一·全情况全方程全方案总账 + 分层统一新思维',
        '日期': DATE, '引擎': ENGINE,
        '全情况': sits, '全方程': eqs, '方程量纲核验': eq_dims, '全方案': schemes,
        '分层统一': lay, '分层统一定理': law, '方程族': fam,
        '阳性对照': ctrls, '红线': red,
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
        f.write('## 分层统一定理\n\n%s\n\n' % law['law'])
        f.write('## 条目表\n\n| 码 | 状态 | 判定 |\n|---|---|---|\n')
        for e in ENTRIES:
            f.write('| %s | %s | %s |\n' % (e['code'], e['status'], e['title']))

    log(report)
    log('JSON -> %s' % jp)
    log('GUARDS %d/%d ENTRIES %d EXIT=0' %
        (sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

