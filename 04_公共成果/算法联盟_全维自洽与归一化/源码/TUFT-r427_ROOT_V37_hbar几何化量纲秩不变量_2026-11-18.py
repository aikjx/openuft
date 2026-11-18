# -*- coding: utf-8 -*-
# r427 / algorithm alliance -- ROOT V37 hbar-geometrization dimensional-rank no-go (2026-11-18)
# Pure stdlib. Read-only AST scan of V37; Fraction quadruple dimensions (M,L,T,Q).
# Core theorem: the geometric basis {c,omega,kappa,tau,l0,a0,A0,omega_max} has M-component
# identically 0, so no rational-power monomial can span [hbar]=M L^2 T^-1. This closes the
# manuscript's own "direction A" (postulate a minimum length / maximum frequency).
# Also machine-checks the hbar=l_P^2 c^3/G <-> l_P=sqrt(hbar G/c^3) round-trip identity,
# catches the manuscript's alpha^9.6 arithmetic slip, and prices every exit.
import os
import sys
import io
import json
import ast
import hashlib
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
getcontext().prec = 220

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-18'
STEM = 'TUFT-r427_ROOT_V37_hbar几何化量纲秩不变量_2026-11-18'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
V37 = os.path.join(OPENUFT, '90_历史归档', '来源语料_utf_20261009', '语料',
                   '大统一场论_算法联盟最高权限', 'v2',
                   'V37_ℏ几何化_时空离散性涌现.py')
F_R426 = os.path.join(PUB, '判定_TUFT-r426-ROOT_V55_pi_sqrtphi联合预言W3门禁审计_2026-11-18.md')
F_R424 = os.path.join(PUB, '判定_TUFT-r424-ROOT_V77_G与c全维关系审计_2026-11-17.md')
F_R421 = os.path.join(PUB, '判定_TUFT-r421-突破点W3验收器_双锚点与L3四门禁机器化_2026-11-17.md')

VERDICT = ('V37-HBAR-GEOMETRIZATION--DIMENSIONAL-RANK-NO-GO--'
           'GEOMETRIC-BASIS-M-COMPONENT-IDENTICALLY-ZERO--DIRECTION-A-CLOSED--'
           'HBAR-LP-ROUNDTRIP-IDENTITY-NEEDS-EXTERNAL-G--'
           'ALPHA-9P6-SLIP-ACTUAL-10P47--HBAR-OVER-A0SQ-C-IS-MASS-PER-LENGTH--'
           'HBAR-C-ELASTIC-MODULUS-OFF-BY-L4--NO-W3-CANDIDATE--0OF6-UNCHANGED')

RED = {
    'completion_0_of_6': True, 'coverage_0_of_22': True, 'UFT3_zero': True,
    'L3_zero': True, 'validated_zero': True,
    'gravity_four_force_correct_equations_zero': True, 'L3_not_implies_L4': True,
}

LINES = []
ENTRIES = []
GUARDS = []
CONTEXT = {}


def emit(s=''):
    LINES.append(str(s))
    print(s)


def add(uid, verdict, claim, reading):
    ENTRIES.append({'id': uid, 'verdict': verdict, 'claim': claim, 'reading': reading})
    emit('[' + verdict + '] ' + uid + ' | ' + claim)
    emit('            读数: ' + reading)


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'pass': bool(ok), 'detail': detail})
    emit(('  [GUARD PASS] ' if ok else '  [GUARD FAIL] ') + name +
         (' | ' + detail if detail else ''))


def sha256_file(path):
    if not path or not os.path.exists(path):
        return 'ABSENT'
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def rel(a, b):
    a = D(a); b = D(b)
    den = max(abs(a), abs(b), D('1e-250'))
    return abs(a - b) / den


def dstr(x):
    if x == 0:
        return '0.0000000000000000000000000E+0'
    return format(x, '.25E')


# ---- Fraction quadruple dimension (M,L,T,Q) ----
Z4 = (F(0), F(0), F(0), F(0))
DIM = {
    'c':        (F(0), F(1), F(-1), F(0)),   # L T^-1
    'omega':    (F(0), F(0), F(-1), F(0)),   # T^-1
    'kappa':    (F(0), F(-1), F(0), F(0)),   # L^-1
    'tau':      (F(0), F(-1), F(0), F(0)),   # L^-1
    'l0':       (F(0), F(1), F(0), F(0)),    # L  (manuscript's minimum length)
    'a0':       (F(0), F(1), F(0), F(0)),    # L  (lattice constant)
    'A0':       (F(0), F(2), F(0), F(0)),    # L^2
    'omega_max':(F(0), F(0), F(-1), F(0)),   # T^-1 = c/l0
    'rho0':     (F(1), F(-3), F(0), F(0)),   # M L^-3 (spacetime mass density)
    'hbar':     (F(1), F(2), F(-1), F(0)),   # M L^2 T^-1
    'G':        (F(-1), F(3), F(-2), F(0)),  # L^3 M^-1 T^-2
    'm':        (F(1), F(0), F(0), F(0)),    # M
    'lp':       (F(0), F(1), F(0), F(0)),    # L
}


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dscale(k, a):
    k = F(k)
    return tuple(k * x for x in a)


def rank4(vectors):
    m = [list(v) for v in vectors if any(x != 0 for x in v)]
    r = 0
    for col in range(4):
        piv = None
        for i in range(r, len(m)):
            if m[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][col]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][col] != 0:
                f = m[i][col]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


def dstr_dim(a):
    names = ['M', 'L', 'T', 'Q']
    parts = []
    for nm, e in zip(names, a):
        if e == 0:
            continue
        parts.append(nm if e == 1 else (nm + '^' + str(e)))
    return '*'.join(parts) if parts else '1'


emit('=' * 100)
emit('TUFT r427 / ROOT V37 hbar-geometrization dimensional-rank no-go / ' + DATE)
emit('=' * 100)

src_exists = os.path.exists(V37)
src_sha = sha256_file(V37)
src_bytes = os.path.getsize(V37) if src_exists else 0
src_text = io.open(V37, encoding='utf-8', errors='replace').read() if src_exists else ''
src_tree = ast.parse(src_text) if src_exists else None
emit('SOURCE  exists=%s bytes=%d sha256=%s' % (src_exists, src_bytes, src_sha[:24]))

# self-admitted failures (the manuscript is unusually honest)
self_no_M = ('没有 [M]' in src_text) or ('不能产生质量量纲' in src_text)
self_circular = ('循环论证' in src_text)
self_overclaim = ('过度宣称' in src_text) or ('推荐: 方向 B 或 C' in src_text)
self_dirA = ('方向 A' in src_text) and ('公理 IV' in src_text)
self_alpha96 = ('α^{9.6}' in src_text) or ('9.6' in src_text)
emit('AST     no_M=%s circular=%s overclaim=%s directionA=%s alpha96=%s' %
     (self_no_M, self_circular, self_overclaim, self_dirA, self_alpha96))

add('V01', 'PASS',
    '手稿诚实面成立：自承 ℏ 不可纯几何构造、认循环论证、自撤过度宣称、推荐接受 ℏ',
    'AST 命中 无[M]=%s / 循环论证=%s / 过度宣称=%s / 方向A存在=%s；本册不重复否证其自承，'
    '只把它分散的自承压缩成可复跑的硬定理并给剩余出路定价' %
    (self_no_M, self_circular, self_overclaim, self_dirA))

# ---- core theorem: geometric basis has M-component identically zero ----
GEO_KEYS = ['c', 'omega', 'kappa', 'tau', 'l0', 'a0', 'A0', 'omega_max']
GEO = [DIM[k] for k in GEO_KEYS]
m_components = [v[0] for v in GEO]
m_all_zero = all(x == 0 for x in m_components)
rank_geo = rank4(GEO)
rank_with_rho = rank4(GEO + [DIM['rho0']])
HBAR = DIM['hbar']
# reachability: is HBAR in the rational span of GEO plus a mass-bearing input?
rank_with_mass = rank4(GEO + [DIM['m']])
reachable_with_mass = (rank4(GEO + [DIM['m'], HBAR]) == rank_with_mass)
reachable_with_rho = (rank4(GEO + [DIM['rho0'], HBAR]) == rank_with_rho)
reachable_geo = (rank4(GEO + [HBAR]) == rank_geo)
add('V02', 'FAIL' if (m_all_zero and not reachable_geo) else 'PASS',
    '★量纲秩不变量定理：几何基组 {c,ω,κ,τ,l₀,a₀,A₀,ω_max} 的 M 分量恒 0，无法张成 [ℏ]',
    '基组 M 分量=%s（全零=%s）；rank(几何基)=%d；加入 [ℏ] 后 rank=%d（可达=%s）；'
    '外加任一质量标度后 rank=%d 且可达 [ℏ]=%s ⇒ 几何基不含 M，质量输入是必要外部项，'
    '非“尝试失败”而是“张成空间不含目标”' %
    ([str(x) for x in m_components], m_all_zero, rank_geo,
     rank4(GEO + [HBAR]), reachable_geo, rank_with_mass, dstr_dim(HBAR)))

add('V03', 'FAIL' if (not reachable_geo and self_dirA) else 'PASS',
    '★手稿自留“方向 A：公理 IV 最小长度 l₀ / 公理 V 最大频率 ω_max”也被定理关闭',
    'l₀=(%s)、ω_max=(%s) 的 M 分量仍为 0，纳入基组后 rank 仍=%d；'
    '引入 l₀/ω_max 只增加 L/T 方向，永远补不出 M ⇒ 手稿列为“可能突破”的方向 A 实为死路' %
    (dstr_dim(DIM['l0']), dstr_dim(DIM['omega_max']), rank_geo))

add('V04', 'FAIL' if reachable_with_rho else 'PASS',
    'ρ₀（时空质量密度）能补 [M]，但它本身就是 ℏ 的换名：两个外部输入换一个 ℏ，零净收益',
    '手稿 Part 2.4 写 ℏ=ρ₀·c·l₀⁴；量纲 [ρ₀·c·l₀⁴]=%s = [ℏ](%s) ✓；'
    '但 [ρ₀]=%s 自带 M，且手稿自问“ρ₀ 是什么/如何从几何确定”无答 ⇒ '
    '引入 ρ₀ 等于把 ℏ 的质量量纲从外部挪进来，非涌现' %
    (dstr_dim(dadd(dadd(DIM['rho0'], DIM['c']), dscale(4, DIM['l0']))),
     dstr_dim(HBAR), dstr_dim(DIM['rho0'])))

# ---- constants and numerical cross-checks ----
HB = D('1.054571817e-34')
CC = D('299792458')
GG = D('6.67430e-11')
ALPHA = D('7.2973525693e-3')
ME = D('9.1093837015e-31')
MP = (HB * CC / GG).sqrt()
ME_OVER_MP = ME / MP
LN_ALPHA = ALPHA.ln()
EXP_ACTUAL = (ME_OVER_MP.ln() / LN_ALPHA)
R_HAND = (LN_ALPHA * D('9.6')).exp()
SLIP_EXP_REL = abs(EXP_ACTUAL - D('9.6')) / EXP_ACTUAL
SLIP_RATIO = R_HAND / ME_OVER_MP

D_ROUND = dadd(dadd(dscale(2, DIM['lp']), dscale(3, DIM['c'])), dscale(-1, DIM['G']))
D_MQ_BAD = dsub(HBAR, dadd(dscale(2, DIM['a0']), DIM['c']))
D_MQ_GOOD = dsub(HBAR, dadd(DIM['a0'], DIM['c']))
D_HBARC = dadd(HBAR, DIM['c'])
D_STRESS = (F(1), F(-1), F(-2), F(0))
D_MOD_GAP = dsub(D_HBARC, D_STRESS)

CONTEXT.update({
    'alpha': ALPHA, 'm_e_over_m_P': ME_OVER_MP, 'exp_actual': EXP_ACTUAL,
    'r_hand_alpha96': R_HAND, 'slip_exp_rel': SLIP_EXP_REL,
    'slip_ratio': SLIP_RATIO, 'rank_geo': D(rank_geo),
    'rank_with_mass': D(rank4(GEO + [DIM['m']])),
    'rank_with_rho': D(rank_with_rho),
})

self_extG = ('G 仍是外部常数' in src_text)
self_holo = ('需要假设全息原理本身' in src_text)
self_w3_open = ('Koide' in src_text) and ('需要构建' in src_text)

add('V05', 'FAIL' if not self_extG else 'PASS',
    'ℏ=l_P²c³/G 与 l_P=√(ℏG/c³) 是同一定义式往返，G 仍是外部输入，不是 ℏ 的几何涌现',
    '往返左端量纲=%s，[ℏ]=%s，逐项相等=%s；手稿自承「G 仍是外部常数」=%s；'
    '把 G 换成 c³/(ρ_info ℏ) 也要先有 ℏ，闭环仍外部' %
    (dstr_dim(D_ROUND), dstr_dim(HBAR), D_ROUND == HBAR, self_extG))

add('V06', 'FAIL' if dsub(HBAR, dadd(dscale(2, DIM['a0']), DIM['c'])) != DIM['m'] else 'PASS',
    '手稿 m_quantum=ℏ/(a₀²c) 的量纲不是质量，而是质量每长度',
    '[ℏ/(a₀²c)]=%s；[质量]=%s；正确 ℏ/(a₀c) 才是 %s；'
    '所以“基本质量量子”这一命名为量纲误读，不能支撑离散质量谱' %
    (dstr_dim(D_MQ_BAD), dstr_dim(DIM['m']), dstr_dim(D_MQ_GOOD)))

add('V07', 'FAIL' if D_MOD_GAP != Z4 else 'PASS',
    '“ℏc 是时空弹性模量”量纲错：ℏc 与应力/模量差 L⁴',
    '[ℏc]=%s；[弹性模量/应力]=%s；差=%s；'
    '手稿自承还需 ℏ 与 ω_C，属循环论证=%s' %
    (dstr_dim(D_HBARC), dstr_dim(D_STRESS), dstr_dim(D_MOD_GAP), self_circular))

add('V08', 'FAIL' if SLIP_EXP_REL > D('0.01') else 'PASS',
    '手稿 m_e/m_P≈α^9.6 是算术滑移：实际指数约 10.47，按 9.6 会高估约 77 倍',
    'm_e/m_P=%s；ln(m_e/m_P)/ln(α)=%s；手稿 9.6；指数相对偏差=%s；'
    'α^9.6/(m_e/m_P)=%s ⇒ 该句不仅非整数幂次证据，数值本身也不成立' %
    (dstr(ME_OVER_MP), dstr(EXP_ACTUAL), dstr(SLIP_EXP_REL), dstr(SLIP_RATIO)))

add('V09', 'FAIL' if (self_extG and self_holo) else 'PASS',
    '全息/信息密度路线把 ℏ 藏进 l_P²=ℏG/c³ 与“每面积一位”假设，仍是外部输入',
    '手稿自承「需要假设全息原理本身」=%s，且 l_P 路线自承 G 外部=%s；'
    'ρ_info=1/l_P²=c³/(ℏG) 含 ℏ，不能反向推出 ℏ' % (self_holo, self_extG))

add('V10', 'PASS' if ('∮ τ dκ' in src_text or '∮τdκ' in src_text) else 'INFO',
    '拓扑量子化路线被手稿自己用 [τdκ]=L⁻² 拦下：几何作用量面积不等于作用量量子',
    '∮τdκ 量纲=%s，[h]=%s；手稿原句「需要引入 ℏ 才能使量纲正确」命中=%s；'
    '这一条是手稿的诚实面，不重复判错' %
    (dstr_dim(dadd(DIM['tau'], DIM['kappa'])), dstr_dim(dadd(HBAR, dscale(0, HBAR))),
     '需要引入 ℏ' in src_text))

add('V11', 'FAIL' if self_w3_open else 'PASS',
    '质量谱/Koide 只是“需要构建”的下一步建议，没有输出过 W3 的数值预言',
    '手稿第 8/10 部分使用「可能解释」「需要构建」「这是一个约束问题，解的存在性未知」；'
    '没有代数模型 f_n、没有可盲测质量比、没有双锚一致表 ⇒ 不是候选，而是开放项登记' )

add('V12', 'CORRECTED' if self_overclaim else 'FAIL',
    'V37 的终态应改写为：方向 B/C 接受 ℏ 为输入，原命题“ℏ 几何化”已撤回',
    '手稿自承过度宣称/推荐方向 B 或 C=%s；本册不把诚实撤回当成新结果，'
    '只锁定方向 A 仍被量纲秩定理关闭，且 B/C 代价是外部输入 +1（ℏ）' % self_overclaim)

# ---- W3 four gates (r421 definition) ----
def w3_accept(cand):
    return bool(cand['numeric'] and cand['noninverse'] and cand['blind'] and cand['dual'])

candidates = [
    {'name': 'V37-A: ℏ=l_P²c³/G', 'numeric': False, 'noninverse': False,
     'blind': False, 'dual': False,
     'why': 'G 外部；无独立数值；由定义式反解'},
    {'name': 'V37-B: ℏ=ρ₀ c l₀⁴', 'numeric': False, 'noninverse': False,
     'blind': False, 'dual': False,
     'why': 'ρ₀ 自带 M；无独立数值；质量量纲外部挪入'},
    {'name': 'V37-C: m_e/m_P≈α^9.6 / Koide', 'numeric': True, 'noninverse': False,
     'blind': False, 'dual': False,
     'why': '用了已知 m_e、m_P、α；9.6 算术错；Koide 未建模'},
]
passed_w3 = [c['name'] for c in candidates if w3_accept(c)]
positive_candidate = {'name': 'POSITIVE-CONTROL', 'numeric': True, 'noninverse': True,
                      'blind': True, 'dual': True}
positive_ok = w3_accept(positive_candidate)

add('V13', 'FAIL' if passed_w3 else 'PASS',
    'W3 四门禁：V37 三条可能路线 0/3 通过，不能计为突破点',
    'C1 定量 / C2 非反解 / C3 盲测未拟合 / C4 双锚一致；通过数=%d；'
    '阳性对照（虚构全过候选）=%s ⇒ 门禁非恒假' % (len(passed_w3), positive_ok))

add('V14', 'INFO' if (os.path.exists(F_R421) and os.path.exists(F_R424) and
                      os.path.exists(F_R426)) else 'FAIL',
    '跨册分工：r421 提供 W3 验收器；r424/r426 已分别定价 G/c 与独立预言口径；本册只审 V37',
    'r421=%s r424=%s r426=%s；红线与 L3↛L4 保持不变' %
    (os.path.exists(F_R421), os.path.exists(F_R424), os.path.exists(F_R426)))

# ---- positive controls: every detector must have teeth ----
lp2 = HB * GG / (CC * CC * CC)
hbar_back = lp2 * CC * CC * CC / GG
round_res = rel(hbar_back, HB)
alpha_back = (LN_ALPHA * EXP_ACTUAL).exp()
alpha_back_res = rel(alpha_back, ME_OVER_MP)

controls = [
    {'name': 'C1-dimension-mass-detector',
     'pass': bool(D_MQ_GOOD == DIM['m'] and D_MQ_BAD != DIM['m']),
     'detail': 'ℏ/(a₀c)=M 能识别；ℏ/(a₀²c)=M/L 必被拒'},
    {'name': 'C2-rank-extension-by-external-mass',
     'pass': bool(rank_geo < rank_with_mass and reachable_with_mass),
     'detail': '几何基秩 %d；外加质量标度后秩 %d 且可达 ℏ' % (rank_geo, rank_with_mass)},
    {'name': 'C3-hbar-lp-roundtrip-identity',
     'pass': bool(round_res < D('1e-180')),
     'detail': 'l_P²=ℏG/c³ 回代 ℏ 残差 %s' % dstr(round_res)},
    {'name': 'C4-alpha-exponent-calculator',
     'pass': bool(alpha_back_res < D('1e-50') and SLIP_EXP_REL > D('0.01')),
     'detail': '实指数回代残差 %s；手稿 9.6 相对偏差 %s' %
               (dstr(alpha_back_res), dstr(SLIP_EXP_REL))},
    {'name': 'C5-W3-gate-not-rigged',
     'pass': bool(positive_ok and len(passed_w3) == 0 and len(candidates) == 3),
     'detail': '虚构全过候选 PASS；V37 三候选全拒'},
    {'name': 'C6-source-self-admission-detector',
     'pass': bool(self_no_M and self_circular and self_overclaim),
     'detail': '无 M / 循环论证 / 过度宣称三类自承全部命中'},
]
for c in controls:
    emit('  [CONTROL %s] %s | %s' % ('PASS' if c['pass'] else 'FAIL', c['name'], c['detail']))
controls_ok = all(c['pass'] for c in controls)

# ---- guards ----
_has_random_import = False
if src_tree is not None:
    for n in ast.walk(src_tree):
        if isinstance(n, ast.Import) and any(a.name == 'random' for a in n.names):
            _has_random_import = True
        if isinstance(n, ast.ImportFrom) and n.module == 'random':
            _has_random_import = True

verdict_by_id = dict((e['id'], e['verdict']) for e in ENTRIES)
guard('G01', src_exists and src_bytes > 1000,
      'source exists and nontrivial (%d bytes)' % src_bytes)
guard('G02', src_tree is not None,
      'source parsed by AST without importing/executing')
guard('G03', self_no_M and self_circular and self_overclaim and self_dirA,
      'source self-admissions and direction-A text detected')
guard('G04', m_all_zero,
      'all geometric-basis M components are exactly zero')
guard('G05', rank_geo < 4 and (not reachable_geo),
      'geometric basis cannot span hbar')
guard('G06', reachable_with_rho and DIM['rho0'][0] == 1,
      'external rho0 adds M and reaches hbar (shows the price)')
guard('G07', D_ROUND == HBAR and self_extG,
      'hbar-lP-G roundtrip is dimensional identity with G external')
guard('G08', D_MQ_BAD == (F(1), F(-1), F(0), F(0)) and D_MQ_GOOD == DIM['m'],
      'mass-per-length slip detected against correct mass combination')
guard('G09', D_MOD_GAP == (F(0), F(4), F(0), F(0)) and self_circular,
      'hbar*c elastic modulus gap is exactly L^4 and circularity admitted')
guard('G10', EXP_ACTUAL > D('10') and SLIP_EXP_REL > D('0.01') and SLIP_RATIO > D('10'),
      'alpha^9.6 slip is numerical, not cosmetic')
guard('G11', len(passed_w3) == 0 and positive_ok,
      'W3 rejects 3 V37 routes; positive control passes')
guard('G12', controls_ok,
      'all 6 positive controls passed')
guard('G13', not _has_random_import,
      'engine/source deterministic (AST: no random import)')
guard('G14', all(verdict_by_id.get(k) == 'FAIL' for k in
                 ['V02', 'V03', 'V04', 'V06', 'V07', 'V08', 'V09', 'V11']),
      'core negative verdicts are explicitly FAIL, not generated by accident')
guard('G15', os.path.exists(F_R421) and os.path.exists(F_R424) and os.path.exists(F_R426)
      and all(RED.values()),
      'r421/r424/r426 references exist and red lines unchanged')

# ===================== aggregate & persist =====================
counts = {}
for e in ENTRIES:
    counts[e['verdict']] = counts.get(e['verdict'], 0) + 1
guard_pass = sum(1 for g in GUARDS if g['pass'])
guard_fail = len(GUARDS) - guard_pass
emit('')
emit('TOTAL entries=%d (%s)' % (len(ENTRIES), ', '.join(k + '=' + str(v) for k, v in sorted(counts.items()))))
emit('GUARDS %d/%d pass' % (guard_pass, len(GUARDS)))
emit('VERDICT ' + VERDICT)

obj = {
    'round': 'r427', 'date': DATE, 'verdict': VERDICT,
    'target': 'ROOT V37 hbar geometrization / spacetime discreteness (ALG-ROOT-GUFT-V37)',
    'source': {'path': os.path.relpath(V37, OPENUFT), 'sha256': src_sha, 'bytes': src_bytes,
               'read_only': True, 'ast_parse_ok': src_tree is not None},
    'entries': ENTRIES, 'guards': GUARDS, 'counts': counts,
    'guard_pass': guard_pass, 'guard_total': len(GUARDS),
    'context': {k: dstr(v) for k, v in CONTEXT.items()},
    'controls': controls, 'w3_candidates': candidates, 'red': RED,
    'open': ['O-V37-HBAR: hbar remains external input under directions B/C',
             'O-V37-MASS-SPECTRUM: Koide/three-generation geometric model not constructed',
             'O-V37-SOURCE-OF-G: even hbar=lP^2 c^3/G requires external G'],
}
os.makedirs(DATA, exist_ok=True)
with io.open(P_JSON, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)

md = ['# r427 · ROOT V37 ℏ 几何化量纲秩不变量（数据产物）', '',
      '**verdict**: `' + VERDICT + '`', '',
      '## 条目', '', '| id | 判定 | 主张 |', '|---|---|---|']
for e in ENTRIES:
    md.append('| %s | %s | %s |' % (e['id'], e['verdict'], e['claim']))
md += ['', '## 守卫', '', '| name | pass | detail |', '|---|---|---|']
for g in GUARDS:
    md.append('| %s | %s | %s |' % (g['name'], g['pass'], g['detail']))
md += ['', '## 阳性对照', '', '| name | pass | detail |', '|---|---|---|']
for c in controls:
    md.append('| %s | %s | %s |' % (c['name'], c['pass'], c['detail']))
with io.open(P_MD, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')
with io.open(P_REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')

emit('WROTE ' + os.path.relpath(P_JSON, OPENUFT))
emit('WROTE ' + os.path.relpath(P_MD, OPENUFT))
emit('WROTE ' + os.path.relpath(P_REPORT, OPENUFT))
sys.exit(0 if guard_fail == 0 else 2)
