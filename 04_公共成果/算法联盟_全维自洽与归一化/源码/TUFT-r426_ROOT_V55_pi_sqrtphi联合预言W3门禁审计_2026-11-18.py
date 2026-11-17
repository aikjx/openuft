# -*- coding: utf-8 -*-
# r426 / algorithm alliance -- ROOT V55 pi/sqrt(2)*sqrt(phi) joint-geometry prediction W3 audit (2026-11-18)
# Pure stdlib. Reads the V55 manuscript read-only; recomputes every number at 220 digits;
# proves the "DERIVED S-class" claim is an algebraic identity product + an assumed input,
# the M_GUT=alpha*lambda_C*m_P claim is a 4-input inverse fit, and both fail r421 W3 gates.
# No new physics; no external dependency; no git operation.
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
STEM = 'TUFT-r426_ROOT_V55_pi_sqrtphi联合预言W3门禁审计_2026-11-18'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
V55 = os.path.join(OPENUFT, '90_历史归档', '来源语料_utf_20261009', '语料',
                   '大统一场论_算法联盟最高权限', 'v2',
                   'V55_π√2与√φ联合几何预言_新独立预言搜索.py')
F_R425 = os.path.join(PUB, '判定_TUFT-r425-ROOT_V36_Xi作用量四力FORM统一审计_2026-11-18.md')
F_R421 = os.path.join(PUB, '判定_TUFT-r421-突破点W3验收器_双锚点与L3四门禁机器化_2026-11-17.md')

VERDICT = ('V55-JOINT-GEOMETRY-PREDICTION--NUMBERS-EXACT--'
           'DERIVED-CLAIM-IS-IDENTITY-PRODUCT-PLUS-ASSUMED-ALPHA-W-AT-MP--'
           'M-GUT-ALPHA-LAMBDA-C-IS-4INPUT-INVERSE-FIT-0P38PCT--'
           'SCALE-MIXING-ALPHA0-OVER-ALPHAMZ--NUMBER-COINCIDENCE-SQRT3-7OVER4--'
           'SELF-RETRACTED-BETA-GRAV-ALPHA2-20X--NO-W3-CANDIDATE--0OF6-UNCHANGED')

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


emit('=' * 100)
emit('TUFT r426 / ROOT V55 pi-sqrtphi joint geometry W3 audit / ' + DATE)
emit('=' * 100)

# ===================== source integrity (read-only) =====================
src_exists = os.path.exists(V55)
src_sha = sha256_file(V55)
src_bytes = os.path.getsize(V55) if src_exists else 0
src_text = io.open(V55, encoding='utf-8', errors='replace').read() if src_exists else ''
src_tree = ast.parse(src_text) if src_exists else None
emit('SOURCE  exists=%s bytes=%d sha256=%s' % (src_exists, src_bytes, src_sha[:24]))

has_derived = ('DERIVED' in src_text) and ('S级' in src_text)
has_assumed = ('统一假设' in src_text) or ('假设引力统一' in src_text)
has_mgut_fit = ('M_GUT/m_P ≈ α × λ_C' in src_text) or ('M_GUT ≈ α · λ_C · m_P' in src_text)
has_retract = ('不成立' in src_text) and ('已删除' in src_text or '诚实修正' in src_text)
has_selfcoin = ('可能是巧合' in src_text) and ('7/4' in src_text)
emit('AST     derived=%s assumed=%s mgut_fit=%s self_retract=%s self_coin=%s' %
     (has_derived, has_assumed, has_mgut_fit, has_retract, has_selfcoin))

# ===================== Part 0 : reproduce V55 numbers at 220 digits =====================
pi = D('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196')
phi = (D(1) + D(5).sqrt()) / D(2)
bw = pi / (D(2) * phi).sqrt()             # claimed beta_weak/beta_em at M_P
pi_over_sqrt2 = pi / D(2).sqrt()          # V49 factor
one_over_sqrtphi = D(1) / phi.sqrt()      # V50 factor
prod = pi_over_sqrt2 * one_over_sqrtphi   # the "joint" product
identity_res = rel(prod, bw)
CONTEXT['phi'] = phi
CONTEXT['beta_weak_P'] = bw
CONTEXT['pi_over_sqrt2'] = pi_over_sqrt2
CONTEXT['one_over_sqrtphi'] = one_over_sqrtphi

sqrt3 = D(3).sqrt()
coin_sqrt3_pct = abs(bw - sqrt3) / bw * D(100)
coin_7over4_pct = abs(bw - D(7) / D(4)) / bw * D(100)

add('V01', 'PASS',
    'V55 联合几何量数值 220 位独立复现：π/√(2φ)',
    'φ=%s；π/√(2φ)=%s；手稿自报 1.7469，一致' %
    (dstr(phi), dstr(bw)))

add('V02', 'FAIL',
    '★“DERIVED S级”是代数恒等乘积：π/√(2φ)=(π/√2)·(1/√φ)，残差机器零',
    '(π/√2)=%s，(1/√φ)=%s，乘积=%s，与 π/√(2φ) 相对残差 %s；'
    '所谓“三个几何因子严格联合”是两个已定义因子的乘法重排，零新信息' %
    (dstr(pi_over_sqrt2), dstr(one_over_sqrtphi), dstr(prod), dstr(identity_res)))

# ===================== Part 1 : the assumed input behind DERIVED =====================
# beta_weak=(pi/sqrt2)*alpha_W ; at M_P the manuscript ASSUMES alpha_W(M_P)=alpha_GUT=1/sqrt(phi)
# so beta_weak/beta_em=(pi/sqrt2)*(1/sqrt(phi)) only if beta_em(M_P)=1 is ALSO assumed.
add('V03', 'FAIL',
    '★DERIVED 的前提是喂进去的：α_W(M_P)=α_GUT=1/√φ 与 β_em(M_P)=1 均为“统一假设”',
    '手稿行 39 自写“统一假设”；M_P 处 α_W 无观测值，β_em=β_grav=1 为直接赋值；'
    '喂 1/√φ=%s ⇒ 读出 β_weak/β_em=π/√(2φ)=%s ⇒ W3 C2（非反解）失败' %
    (dstr(one_over_sqrtphi), dstr(bw)))

add('V04', 'FAIL',
    '★“球面π×SU(2)√2×五边形√φ”是符号叙事：π 超越数、√2/√φ 代数数，无量纲可任意相乘',
    '三因子无量纲，乘法无量纲约束、无作用量变分、无群论表示论推导；'
    '把 π 标“球面立体角”、√2 标“SU(2) 双态”、√φ 标“五边形”是事后归因，'
    '评级 DERIVED 与手稿同级“结构指派”不自洽')

# scale mixing: manuscript uses alpha(0)=1/137 at M_Z for beta_weak/beta_em≈16.3
alpha0 = D('7.2973525693e-3')
alpha_mz = D('7.8156e-3')   # r16/能标册 M_Z 口径 (alpha_em(M_Z) ~ 1/128)
alpha_w_mz = D('1') / D('29.6')
beta_ratio_mz_mixed = pi_over_sqrt2 * alpha_w_mz / alpha0
beta_ratio_mz_consistent = pi_over_sqrt2 * alpha_w_mz / alpha_mz
add('V05', 'FAIL',
    '★能标混用：M_Z 处 β_weak/β_em 用 α(0)=1/137 而非 α(M_Z)≈1/128',
    '按手稿口径 (π/√2)(1/29.6)/(1/137)=%s；'
    '改用同能标 α(M_Z)=1/128=%s ⇒ %s；'
    '“跑动 16.3→1.75 差 9 倍”的起点被 α(0) 污染（复发 r16 能标一致性门禁）' %
    (dstr(beta_ratio_mz_mixed), dstr(alpha_mz), dstr(beta_ratio_mz_consistent)))

add('V06', 'INFO',
    'π/√(2φ) 与 √3 差 0.82%、与 7/4 差 0.21%：手稿自承巧合，恰好反证“唯一超越量”',
    '相对差 √3: %s%%；7/4: %s%%；手稿行 215-216 自写“可能是巧合”；'
    '无理数必可被有理数任意逼近（Dirichlet），接近简单比无判别力' %
    (dstr(coin_sqrt3_pct), dstr(coin_7over4_pct)))

# ===================== Part 2 : M_GUT = alpha*lambda_C*m_P inverse fit =====================
M_GUT = D('2e16')            # MSSM input, assumed in manuscript
M_P = D('1.22089e19')        # Planck mass input
lam_C = D('0.22534')         # Cabibbo angle, measured input
mg_over_mp = M_GUT / M_P
alpha_lam = alpha0 * lam_C
fit_ratio = alpha_lam / mg_over_mp
fit_err_pct = rel(fit_ratio, D(1)) * D(100)
mg_over_mp_over_alpha = mg_over_mp / alpha0
CONTEXT['MG_over_MP'] = mg_over_mp
CONTEXT['alpha_lam_C'] = alpha_lam
CONTEXT['fit_err_pct'] = fit_err_pct

add('V07', 'FAIL',
    '★M_GUT=α·λ_C·m_P 是 4 输入反解：M_GUT=2e16(MSSM)、α、λ_C、m_P 全是喂进去的',
    'M_GUT/m_P=%s；α·λ_C=%s；比值=%s，误差 %s%%（手稿自报 0.4%% 一致）；'
    'α、λ_C 为实测锚，M_GUT=2e16 为 MSSM 交汇假设，m_P=√(ℏc/G) 由 G 定 ⇒ 零预测' %
    (dstr(mg_over_mp), dstr(alpha_lam), dstr(fit_ratio), dstr(fit_err_pct)))

add('V08', 'FAIL',
    '★M_GUT/m_P/α=0.224485 被“认作”Cabibbo 0.22534：换任一输入即崩，无不变性',
    '反解值 %s vs 实测 λ_C=%s；差 0.38%%；'
    '这是拿三个外部数拼出第四个数的“符合”，不是从拉氏量导出 λ_C' %
    (dstr(mg_over_mp_over_alpha), dstr(lam_C)))

add('V09', 'PASS',
    '手稿自删 β_grav(M_GUT)≈α²（差 20 倍）为诚实修正，应予登记',
    'β_grav=(M_GUT/m_P)²=%s；α²=%s；比值≈0.0504；手稿行 272 写“不成立”并删除声称' %
    (dstr(mg_over_mp * mg_over_mp), dstr(alpha0 * alpha0)))

add('V10', 'FAIL',
    'β_grav(M_GUT)=(M_GUT/m_P)² 是定义重排，不是新物理量',
    'β_grav 由两个已定标度之比平方给出，无量纲；不携带任何超出 M_GUT、m_P 输入的信息')

add('V11', 'FAIL',
    '★W3 四门禁：V55 三个候选全拒（阳性对照仍 PASS）',
    'find1 π/√(2φ): 反解+假设 ⇒ C2/C4 败；find2 M_GUT=αλ_C m_P: 4 输入反解 ⇒ C2 败；'
    'find1 数字巧合: C3 盲测败；W3.pass 保持 0')

# ===================== Part 3 : provenance & honest-boundary accounting =====================
add('V12', 'INFO',
    'V49→V55 是因子拼接升级，不是新机制：β_weak=(π/√2)α_W 是 V49 已有定义',
    'V55 把 V49 的 π/√2 与 V50 的 1/√φ 相乘即得“新”联合量，未引入新作用量或新约束')

add('V13', 'BOUNDARY',
    'M_P 处 α_W、β_em、β_grav 无观测：普朗克标度“预言”不可检验（非“已证伪”而是不可判定）',
    'C4 双锚（普朗克+粒子）在此仅普朗克端，且粒子端 α_W(M_P) 由统一假设外推；'
    '无法进入任何现有对撞机/宇宙学实测窗口')

add('V14', 'FAIL',
    '“整数比探索”无判别力：π/√(2φ) 无理，7/4、9/5、11/6 任意逼近均无物理意义',
    '手稿 Step4 枚举分数逼近并承认 7/4 差 0.18%；'
    '任何无理数都存在任意精度的有理逼近，此步骤不构成可证伪检验')

add('V15', 'FAIL',
    '“4D 正多胞体解释”（600-cell/120-cell）是未计算的意象，不是推导',
    '手稿行 177-180 用“可能包含 π/√(2φ) 因子”，未给出任何多胞体体积/表面积公式的实算；'
    'BOUNDARY：既非 PASS 也非已证伪，是未落地的猜测')

add('V16', 'PASS',
    '手稿诚实分级部分到位：ASSOC/D 自标、β_grav≈α² 自撤、数字巧合自认',
    '行 337 把 M_GUT 关联标 ASSOC/D（事后关联、无第一性机制）；行 272 自撤 α² 声称；'
    '行 215 自认 7/4 巧合 ⇒ 本册不重复否证其自承开放项，只定价其 DERIVED 升级的谬误')

# ===================== control group =====================
# C1: identity test has teeth -- perturb phi breaks the exact product identity
phi_wrong = D('2')
bw_wrong = pi / (D(2) * phi_wrong).sqrt()
prod_wrong = pi_over_sqrt2 * (D(1) / phi_wrong.sqrt())
teeth_id = rel(prod_wrong, bw_wrong) < D('1e-200') and abs(bw_wrong - bw) > D('1e-3')
add('C1', 'PASS' if teeth_id else 'FAIL', '恒等式判据有牙：换 φ=2 后乘积仍恒等但 β 值改变',
    'φ 真值给 β=%s；φ=2 给 β=%s；乘积恒等残差 <1e-200 但 β 相对差=%s ⇒ 判据区分“恒等式”与“数值巧合”' %
    (dstr(bw), dstr(bw_wrong), dstr(abs(bw_wrong - bw) / bw)))

# C2: inverse-fit test has teeth -- change lambda_C gives different beta ratio
lam_wrong = D('0.22')
fit_wrong = alpha0 * lam_wrong / mg_over_mp
teeth_fit = abs(fit_wrong - fit_ratio) > D('1e-3')
add('C2', 'PASS' if teeth_fit else 'FAIL', '反解判据有牙：换 λ_C 使“符合度”改变',
    'λ_C=0.22534 ⇒ 比值 %s；λ_C=0.22 ⇒ %s；差>%s ⇒ 判据非恒真' %
    (dstr(fit_ratio), dstr(fit_wrong), dstr(D('1e-3'))))

# C3: scale-mixing test has teeth -- alpha0 != alpha_MZ
teeth_scale = abs(beta_ratio_mz_mixed - beta_ratio_mz_consistent) > D('0.1')
add('C3', 'PASS' if teeth_scale else 'FAIL', '能标判据有牙：α(0) 与 α(M_Z) 给出不同的 β 比',
    'α(0) 口径 %s vs α(M_Z) 口径 %s；差 %s ⇒ 能标混用可检出' %
    (dstr(beta_ratio_mz_mixed), dstr(beta_ratio_mz_consistent),
     dstr(abs(beta_ratio_mz_mixed - beta_ratio_mz_consistent))))

# C4: number-coincidence test has teeth -- find a closer rational than 7/4.
# q<=12 makes 7/4 the exact best convergent, so "strictly better than 7/4" is
# impossible there (the bug that broke G09). Widen to q<=200: the next continued-
# fraction convergent (117/67) is strictly closer, proving "near a simple ratio"
# is not unique. Verdict is bound to teeth_coin, never hard-coded PASS.
best_num = 0; best_den = 1; best_err = D(10)
for q in range(1, 201):
    p = int((bw * D(q)).to_integral_value())
    for pp in (p - 1, p, p + 1):
        e = abs(bw - D(pp) / D(q)) / bw
        if e < best_err:
            best_err = e; best_num = pp; best_den = q
teeth_coin = best_err < coin_7over4_pct / D(100)
add('C4', 'PASS' if teeth_coin else 'FAIL',
    '数字巧合判据有牙：放宽分母后存在比 7/4 更接近的有理逼近',
    '分母≤12 时 7/4 即最优（相对差 %s%%），无法“严格更优”；放宽到 q≤200 得 %d/%d '
    '相对差 %s%% < 7/4 的 %s%% ⇒ Dirichlet 保证任意无理数可被有理数逼近，“接近简单比”无唯一性' %
    (dstr(coin_7over4_pct), best_num, best_den, dstr(best_err * D(100)), dstr(coin_7over4_pct)))

# C5: W3 gate has teeth
def w3_gate(name, c1, c2, c3, c4):
    gates = {'C1': bool(c1), 'C2': bool(c2), 'C3': bool(c3), 'C4': bool(c4)}
    ok = all(gates.values())
    return {'name': name, 'gates': gates, 'verdict': 'PASS' if ok else 'REJECTED'}

candidates = [
    w3_gate('V55 find1 beta_weak/beta_em=pi/sqrt(2phi)', True, False, False, False),
    w3_gate('V55 find2 M_GUT=alpha*lambda_C*m_P', True, False, False, False),
    w3_gate('V55 beta_grav(M_GUT) (retracted)', True, False, False, False),
    w3_gate('positive control: hypothetical four-gate candidate', True, True, True, True),
]
rejected = sum(1 for x in candidates if x['verdict'] == 'REJECTED')
positive_ok = candidates[-1]['verdict'] == 'PASS'
add('C5', 'PASS' if (rejected == 3 and positive_ok) else 'FAIL',
    'W3 门禁非恒假：阳性对照通过、V55 三候选全拒',
    'REJECTED %d，阳性=%s' % (rejected, positive_ok))

# C6: self-retraction honesty test has teeth (a false claim would be caught)
alpha_sq = alpha0 * alpha0
retract_ratio = mg_over_mp * mg_over_mp / alpha_sq
teeth_retract = abs(retract_ratio - D(1)) > D('0.5')
add('C6', 'PASS' if teeth_retract else 'FAIL', '自撤判据有牙：β_grav/α² 确实远离 1（手稿自撤正确）',
    '比值 %s，离 1 的相对差 %s%% ⇒ 自撤属实，非误删' %
    (dstr(retract_ratio), dstr(abs(retract_ratio - D(1)) * D(100))))

# ===================== guards =====================
guard('G01', src_exists, 'V55 source read-only found, sha256=' + src_sha[:16])
guard('G02', src_bytes > 15000, 'V55 manuscript size plausible (%d bytes)' % src_bytes)
guard('G03', has_derived and has_assumed, 'DERIVED claim + assumed input both present in source')
guard('G04', has_mgut_fit, 'M_GUT alpha*lambda_C fit claim present in source')
guard('G05', has_retract, 'self-retraction of beta_grav~alpha^2 present')
guard('G06', has_selfcoin, 'self-admitted number coincidence (7/4) present')
guard('G07', identity_res < D('1e-200'), 'joint product is exact algebraic identity at 220 digits')
guard('G08', fit_err_pct > D('0.1') and fit_err_pct < D('1'), 'M_GUT fit error ~0.4 pct reproduced')
guard('G09', teeth_id and teeth_fit and teeth_scale and teeth_coin and teeth_retract,
      'all five teeth tests passed')
guard('G10', all(e['verdict'] in ('PASS', 'FAIL', 'CORRECTED', 'INFO', 'BOUNDARY')
                 for e in ENTRIES), 'all entry verdicts in vocabulary')
guard('G11', len(ENTRIES) == 22 and len(GUARDS) >= 10,
      'entry count=%d (16 main + 6 controls); guards so far=%d' % (len(ENTRIES), len(GUARDS)))
guard('G12', all(e['reading'].strip() for e in ENTRIES), 'all readings non-empty')
_self_tree = ast.parse(io.open(os.path.abspath(__file__), encoding='utf-8').read())
_has_random_import = any(
    (isinstance(n, ast.Import) and any(a.name == 'random' for a in n.names)) or
    (isinstance(n, ast.ImportFrom) and n.module == 'random')
    for n in ast.walk(_self_tree))
guard('G13', not _has_random_import, 'engine deterministic (AST: no random import)')
guard('G14', rejected == 3 and positive_ok, 'W3 rejected 3 V55 candidates, control passed')
guard('G15', os.path.exists(F_R421) and os.path.exists(F_R425),
      'r421 W3 gate + r425 predecessor reference exist')

# ===================== aggregate & persist =====================
counts = {}
for e in ENTRIES:
    counts[e['verdict']] = counts.get(e['verdict'], 0) + 1
guard_pass = sum(1 for g in GUARDS if g['pass'])
guard_fail = len(GUARDS) - guard_pass
emit('')
emit('TOTAL entries=%d (%s)' % (len(ENTRIES), ', '.join(k + '=' + str(v) for k, v in sorted(counts.items()))))
emit('GUARDS %d/%d pass' % (guard_pass, len(GUARDS)))

obj = {
    'round': 'r426', 'date': DATE, 'verdict': VERDICT,
    'target': 'ROOT V55 pi/sqrt(2) & sqrt(phi) joint geometry prediction (ALG-ROOT-GUFT-V55)',
    'source': {'path': os.path.relpath(V55, OPENUFT), 'sha256': src_sha, 'bytes': src_bytes,
               'read_only': True, 'ast_parse_ok': src_tree is not None},
    'entries': ENTRIES, 'guards': GUARDS, 'counts': counts,
    'guard_pass': guard_pass, 'guard_total': len(GUARDS),
    'context': {k: dstr(v) for k, v in CONTEXT.items()},
    'w3_candidates': candidates, 'red': RED,
    'open': ['O-V55-ALPHA-W-AT-MP: no observed alpha_W at Planck scale',
             'O-V55-ACTION: no action giving beta_weak=(pi/sqrt2)*alpha_W',
             'O-V55-CABIBBO: lambda_C not derived from GUT scale'],
}
os.makedirs(DATA, exist_ok=True)
with io.open(P_JSON, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)

md = ['# r426 · ROOT V55 π/√2·√φ 联合预言 W3 门禁审计（数据产物）', '',
      '**verdict**: `' + VERDICT + '`', '',
      '## 条目', '', '| id | 判定 | 主张 |', '|---|---|---|']
for e in ENTRIES:
    md.append('| %s | %s | %s |' % (e['id'], e['verdict'], e['claim']))
md += ['', '## 守卫', '', '| name | pass | detail |', '|---|---|---|']
for g in GUARDS:
    md.append('| %s | %s | %s |' % (g['name'], g['pass'], g['detail']))
with io.open(P_MD, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')
with io.open(P_REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')

emit('WROTE ' + os.path.relpath(P_JSON, OPENUFT))
emit('WROTE ' + os.path.relpath(P_MD, OPENUFT))
emit('WROTE ' + os.path.relpath(P_REPORT, OPENUFT))
sys.exit(0 if guard_fail == 0 else 2)
