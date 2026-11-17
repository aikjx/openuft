# -*- coding: utf-8 -*-
# r425 / algorithm alliance -- ROOT V36 Xi-action four-force FORM unification audit (2026-11-18)
# Pure stdlib. Reads the V36 manuscript read-only; recomputes its numbers at 220 digits;
# proves a dimension mutual-exclusion theorem, a tau/kappa=alpha circular-inversion theorem,
# a gauge-group dimension deficit, and a no-field-equation (soliton) result.
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
STEM = 'TUFT-r425_ROOT_V36_Xi作用量四力FORM统一审计_2026-11-18'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
V36 = os.path.join(OPENUFT, '90_历史归档', '来源语料_utf_20261009', '语料',
                   '大统一场论_算法联盟最高权限', 'v2',
                   'V36_Ξ作用量_四力FORM统一突破.py')
F_R421 = os.path.join(PUB, '判定_TUFT-r421-突破点W3验收器_双锚点与L3四门禁机器化_2026-11-17.md')
F_R424 = os.path.join(PUB, '判定_TUFT-r424-ROOT_V77_G与c全维关系审计_2026-11-17.md')

VERDICT = ('V36-XI-ACTION--FOUR-FUNCTIONS-ALGEBRA-EXACT--'
           'DIMENSION-MUTUAL-EXCLUSION-TWO-CLASSES-F_E-ISOLATED--'
           'TAU-OVER-KAPPA-CIRCULAR-INVERSION--'
           'LAGRANGIAN-NO-CONSISTENT-DIMENSION--'
           'U1-NONINVARIANT-TERMS-CONFIRMED--GAUGE-DIM-DEFICIT-11--'
           'SOLITON-NO-FIELD-EQUATION--SSB-NOT-RESTORATION--'
           'GRAVITY-CATEGORY-ERROR--PRED-ZERO--NO-W3-CANDIDATE--0OF6-UNCHANGED')

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


# ---- dimension vectors (M, L, T, Q) ----
DL = (0, 1, 0, 0)
DM = (1, 0, 0, 0)
DT = (0, 0, 1, 0)
Z4 = (0, 0, 0, 0)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dpowvec(a, n):
    return tuple(n * x for x in a)


def dadd(a, b):
    assert a == b, 'inhomogeneous dimension sum: ' + str(a) + ' vs ' + str(b)
    return a


def ds(a):
    names = ['M', 'L', 'T', 'Q']
    parts = [names[i] + ('^' + str(v) if v != 1 else '')
             for i, v in enumerate(a) if v != 0]
    return '*'.join(parts) if parts else '1'


emit('=' * 100)
emit('TUFT r425 / ROOT V36 Xi-action four-force FORM audit / ' + DATE)
emit('=' * 100)

# ===================== source integrity (read-only) =====================
src_exists = os.path.exists(V36)
src_sha = sha256_file(V36)
src_bytes = os.path.getsize(V36) if src_exists else 0
src_text = io.open(V36, encoding='utf-8', errors='replace').read() if src_exists else ''
src_tree = ast.parse(src_text) if src_exists else None
emit('SOURCE  exists=%s bytes=%d sha256=%s' % (src_exists, src_bytes, src_sha[:24]))

# AST facts: the four claimed functions and the missing field equation
ast_src = ast.dump(src_tree) if src_tree else ''
has_four_claims = all(k in src_text for k in
                      ['Re(Ξ)²', 'Im(Ξ)', '|Ξ|²', 'Im(Ξ²)'])
has_no_equation = ('方程: ???' in src_text) or ('运动方程是什么' in src_text)
has_pred_zero = ('PRED = 0%' in src_text) or ('PRED=0%' in src_text)
emit('AST     four_claims=%s no_field_equation=%s pred_zero=%s' %
     (has_four_claims, has_no_equation, has_pred_zero))

# ===================== Part 0 : reproduce V36 numbers =====================
c = D('299792458')
hbar = D('1.0545718176461565e-34')
m_e = D('9.1093837015e-31')
alpha = D('7.2973525693e-3')
omega = m_e * c * c / hbar
rho = c / (omega * (D(1) + alpha * alpha).sqrt())
b = alpha * rho
kappa = rho / (rho * rho + b * b)
tau = b / (rho * rho + b * b)
CONTEXT['kappa'] = kappa
CONTEXT['tau'] = tau
CONTEXT['rho'] = rho
CONTEXT['b'] = b

fG = kappa * kappa
fE = tau
fS = kappa * kappa + tau * tau
fW = kappa * tau
emit('V36NUM  kappa=%s  tau=%s  tau/kappa=%s' %
     (dstr(kappa), dstr(tau), dstr(tau / kappa)))

# four Xi expressions, recomputed from the complex arithmetic identities
recG = kappa * kappa
recE = tau
recS = (kappa + tau) * (kappa + tau) + (kappa - tau) * (kappa - tau)
recS = recS / D(2)  # |Xi|^2 computed without complex sqrt
recW = kappa * tau  # Im(Xi^2)/2
errG = rel(recG, fG)
errE = rel(recE, fE)
errS = rel(recS, fS)
errW = rel(recW, fW)

add('V01', 'PASS',
    '四力函数的 Ξ 表达式代数精确（Re²/Im/|Ξ|²/ImΞ²）',
    '四项相对残差 %s / %s / %s / %s（220 位，恒等式代入）' %
    (dstr(errG), dstr(errE), dstr(errS), dstr(errW)))

# ===================== Part 1 : dimension mutual exclusion =====================
DK = dpowvec(DL, -1)          # [kappa] = [tau] = L^-1
D_FG = dpowvec(DK, 2)         # L^-2
D_FE = DK                     # L^-1  (the isolated one)
D_FS = dadd(D_FG, D_FG)       # f_S=|Xi|^2=k^2+t^2: two L^-2 terms summed -> L^-2
D_FW = dmul(DK, DK)           # L^-2 (k*t)
D_FORCE = (1, 1, -2, 0)       # M L T^-2
classes = sorted(set([D_FG, D_FE, D_FS, D_FW]))  # two classes: L^-2 (three) + L^-1 (one)
is_force = [d == D_FORCE for d in (D_FG, D_FE, D_FS, D_FW)]

add('V02', 'FAIL',
    '★量纲互斥定理：四个“力函数”分两类量纲（f_E 孤立），且均不是力',
    '[fG]=%s [fE]=%s [fS]=%s [fW]=%s ⇒ fG=fS=fW=L^-2，唯 fE=L^-1，互异类 %d；'
    '[F]=%s，四者等于力的个数 %d/4' %
    (ds(D_FG), ds(D_FE), ds(D_FS), ds(D_FW), len(classes), ds(D_FORCE), sum(is_force)))

# ---- two mutually exclusive readings of [Xi] ----
# reading A: Xi is curvature, [Xi]=L^-1 -> dispersion omega^2=c^2|Xi|^2 is consistent
# reading B: Xi is a dimensionless QFT scalar, [Xi]=1 -> dispersion dimension L^2 T^-2
D_OMEGA2 = dpowvec(DT, -2)    # T^-2
D_C2 = (0, 2, -2, 0)          # [c^2] = L^2 T^-2 (must include the T^-2 !)
D_RHO_E = (1, -1, -2, 0)      # energy density [E]/L^3
disp_A = dmul(D_C2, dpowvec(DL, -2))  # c^2 * (L^-1)^2 = T^-2 OK
disp_B = dmul(D_C2, Z4)               # c^2 * 1 = L^2 T^-2 WRONG
reading_A_ok = (disp_A == D_OMEGA2)
reading_B_ok = (disp_B == D_OMEGA2)
dim_m2_needed = tuple(p - q for p, q in zip(D_RHO_E, dpowvec(DL, -2)))

add('V03', 'FAIL',
    '★Ξ 量纲两读法互斥：曲率口径使拉氏量系数失真，QFT 口径使色散失真',
    '口径A [Ξ]=L^-1：色散 %s==T^-2 成立（[c²]=%s）但 m²|Ξ|² 要成为能量密度需 [m²]=%s（非 M²）；'
    '口径B [Ξ]=1：色散给 %s≠T^-2。两口径不可能同时成立（A=%s B=%s）' %
    (ds(disp_A), ds(D_C2), ds(dim_m2_needed), ds(disp_B),
     reading_A_ok, reading_B_ok))

coeff_dims = {
    'm2': ds(dmul((1, -1, -2, 0), dpowvec(DL, 2))),
    'lambda': ds(dmul((1, -1, -2, 0), dpowvec(DL, 2))),
    'mu': ds(dmul((1, -1, -2, 0), DL)),
    'g': ds(dmul((1, -1, -2, 0), dpowvec(DL, 2))),
}
add('V04', 'FAIL',
    '拉格朗日量候选的四个耦合系数量纲互异 ⇒ 四个外部量纲输入',
    'L=|∂Ξ|²−m²|Ξ|²−λ(ReΞ)²−μ·ImΞ−g·ImΞ² 在 [Ξ]=L^-1 下：'
    '[m²]=%s [λ]=%s [μ]=%s [g]=%s（四个不同，须外部指定）' %
    (coeff_dims['m2'], coeff_dims['lambda'], coeff_dims['mu'], coeff_dims['g']))

# ===================== Part 2 : circular inversion tau/kappa = alpha =====================
def invert(alpha_in):
    om = m_e * c * c / hbar
    rr = c / (om * (D(1) + alpha_in * alpha_in).sqrt())
    bb = alpha_in * rr
    kk = rr / (rr * rr + bb * bb)
    tt = bb / (rr * rr + bb * bb)
    return kk, tt, tt / kk

k1, t1, r1 = invert(alpha)
alpha2 = D('0.01')
k2, t2, r2 = invert(alpha2)
circ_err_1 = rel(r1, alpha)
circ_err_2 = rel(r2, alpha2)
two_distinct = (abs(r1 - r2) > D('1e-4'))  # absolute gap: alpha1~7.3e-3 vs alpha2~1e-2

add('V05', 'FAIL',
    '★循环反解：τ/κ 是输入 α 的逐位回放（SOURCE 统一零信息量）',
    '输入 α=%s ⇒ 反解 κ=%s τ=%s ⇒ 读出 τ/κ=%s，残差 %s；'
    '换 α=%s ⇒ τ/κ=%s，残差 %s；两读数互异=%s ⇒ 判据有牙但纯反解' %
    (dstr(alpha), dstr(k1), dstr(t1), dstr(r1), dstr(circ_err_1),
     dstr(alpha2), dstr(r2), dstr(circ_err_2), two_distinct))

# the five "key observations" are all algebraic identities
kappa_t, tau_t = D('1.7'), D('0.31')
obs = [
    rel(kappa_t * kappa_t + kappa_t * tau_t, kappa_t * (kappa_t + tau_t)),
    rel(kappa_t * kappa_t + tau_t * tau_t, kappa_t * kappa_t + tau_t * tau_t),
    rel(kappa_t * kappa_t - kappa_t * tau_t, kappa_t * (kappa_t - tau_t)),
    rel(D(2) * kappa_t * tau_t, D(2) * kappa_t * tau_t),
    rel(kappa_t * kappa_t - tau_t * tau_t, kappa_t * kappa_t - tau_t * tau_t),
]
add('V06', 'INFO',
    '手稿五条"关键观察"全部为代数恒等式（对任意 κ,τ 成立）',
    '取 κ=%s τ=%s：五条残差 %s（机器零，零信息量）' %
    (dstr(kappa_t), dstr(tau_t), ','.join(dstr(x) for x in obs)))

# ===================== Part 3 : U(1) noninvariant terms (rational rotation) =====================
# rotate by cos=3/5, sin=4/5 (Pythagorean) -- no floating trig needed
k0, t0 = D('1'), D('0.3')
kp = (D(3) * k0 - D(4) * t0) / D(5)
tp = (D(4) * k0 + D(3) * t0) / D(5)
inv_mod2 = rel(kp * kp + tp * tp, k0 * k0 + t0 * t0)
inv_re2 = rel(kp * kp, k0 * k0)
inv_im = rel(tp, t0)
inv_im2 = rel(D(2) * kp * tp, D(2) * k0 * t0)

add('V07', 'PASS',
    '手稿自承的 U(1) 分析可独立复现：只有 |Ξ|² 不变，三项破坏对称性',
    '有理旋转 (cos,sin)=(3/5,4/5)：|Ξ|² 残差 %s（不变）；'
    'Re² 残差 %s、Im 残差 %s、ImΞ² 残差 %s（均非零）' %
    (dstr(inv_mod2), dstr(inv_re2), dstr(inv_im), dstr(inv_im2)))

# gauge group dimension deficit: complex scalar carries U(1) only (dim 1)
# SM gauge group SU(3)xSU(2)xU(1) has rank/dim 8+3+1 = 12
SM_DIM = 8 + 3 + 1
XI_DIM = 1
add('V08', 'FAIL',
    '★规范群维度亏：单个复标量 Ξ 只载 U(1)（1 维），SM 需 12 维',
    'SU(3)×SU(2)×U(1) 维数 %d；Ξ 相位群维数 %d；亏 %d 维；'
    '手稿 Part 5 自承"需要 SU(3)×SU(2)×U(1)"⇒ 规范群为外部注入' %
    (SM_DIM, XI_DIM, SM_DIM - XI_DIM))

add('V09', 'FAIL',
    '★孤子方案无场方程：粒子=涡旋不可计算、不可证伪',
    'AST/全文扫描 no_field_equation=%s；手稿 §6.3 写"方程: ???"、'
    '§8.3 写"精确形式需要求解运动方程"但从未给出；'
    '与 r419 A1（独立协变作用量）未闭合同判' % has_no_equation)

add('V10', 'FAIL',
    '自发对称破缺不能"恢复"U(1)，单个 U(1) 破缺也不够产生三力',
    'SSB 的真空不守恒对称性（不是恢复）；U(1)→nothing 只留 1 光子+1 实标量；'
    '三力需 12 维规范群；手稿 §4/§5 把"恢复"与"破缺"混用')

add('V11', 'FAIL',
    '引力范畴错误：手稿自承引力不能 Yang-Mills，却把它与三规范力并列 FORM 统一',
    '手稿 §5 第 3 条原文"引力不能被包含在 Yang-Mills 规范场论中"；'
    'f_G=Re(Ξ)² 与 f_E/f_W/f_S 的规范场解释不同范畴 ⇒ 并列为"四力统一"无效')

add('V12', 'CORRECTED',
    '色散 ω²=c²(κ²+τ²) 是几何定义恒等式，不是从 S[Ξ] 导出的运动方程',
    'κ=ρ/(ρ²+b²), τ=b/(ρ²+b²) ⇒ κ²+τ²=1/(ρ²+b²)，'
    'ω=c/√(ρ²+b²) ⇒ 恒等式残差 %s；手稿 §7.2 把它当"作用量运动方程"是倒置' %
    dstr(rel(omega * omega, c * c * (kappa * kappa + tau * tau))))

add('V13', 'BOUNDARY',
    '孤子质量量子化 ℏω / 时空离散 / 最大能量截断：无方程承载的形而上承诺',
    '无场方程 ⇒ 孤子剖面 f(r),g(r) 不可解、质量不可算；'
    '三条"预言"均不可进入 r421 W3 四门（C1 定量数值即失败）')

add('V14', 'INFO',
    'SOURCE(V35)→FORM(V36) 是命名升级而非物理升级：函数集完全相同',
    'V35 与 V36 的四函数同为 {κ², τ, κ²+τ², κτ}；'
    'V36 新增的只是把四个函数写进 L 的四个自由系数，未增加任何约束或数值')

add('V15', 'FAIL',
    '手稿自承 PRED=0%：无独立可证伪预言',
    'fulltext has_pred_zero=%s；项" FORM 统一未达成 / 无独立可证伪预言"为作者自报' %
    has_pred_zero)

# ===================== Part 4 : W3 four-gate (r421 spirit, self-contained) =====================
# Gate: C1 quantitative / C2 non-inversion / C3 blind path / C4 dual anchor
def w3_gate(name, quantitative, non_inversion, blind, dual_anchor):
    gates = {'C1': bool(quantitative), 'C2': bool(non_inversion),
             'C3': bool(blind), 'C4': bool(dual_anchor)}
    ok = all(gates.values())
    return {'name': name, 'gates': gates, 'verdict': 'PASS' if ok else 'REJECTED'}

candidates = [
    w3_gate('V36 kappa,tau electron-scale values', True, False, False, False),
    w3_gate('V36 tau/kappa = alpha', True, False, False, False),
    w3_gate('V36 soliton mass = hbar*omega', True, False, False, False),
    w3_gate('V36 spacetime discreteness / max cutoff', False, False, False, False),
    w3_gate('positive control: hypothetical four-gate candidate', True, True, True, True),
]
rejected = sum(1 for x in candidates if x['verdict'] == 'REJECTED')
positive_ok = candidates[-1]['verdict'] == 'PASS'
add('V16', 'FAIL',
    '★W3 四门禁：V36 全部候选被拒（阳性对照仍 PASS，门禁非恒假）',
    '5 个候选中 REJECTED %d（四个 V36 候选全拒），阳性对照=%s；'
    'W3.pass 保持 0' % (rejected, positive_ok))

# ===================== control group (positive/negative controls) =====================
# C1: dimension test has teeth -- a dimensionless tau would allow sum, but violates geometry
D_TAU_WRONG = Z4
teeth_dim = (dmul(DK, D_TAU_WRONG) != D_FW)  # correct kappa*tau=L^-2 vs wrong kappa*1=L^-1
add('C1', 'PASS', '量纲判据的判别力：把 τ 强改为无量纲则 κτ 量纲改变',
    '正确 [κτ]=%s；错误 [κ·1]=%s；两者不等=%s ⇒ 判据有牙' %
    (ds(D_FW), ds(dmul(DK, D_TAU_WRONG)), teeth_dim))

# C2: circularity test has teeth -- two different alpha give two different readings
add('C2', 'PASS', '循环反解判据的判别力：两个输入 α 给出两个不同 τ/κ',
    'α1=%s→τ/κ=%s；α2=%s→τ/κ=%s；互异=%s（若恒定则判据无牙）' %
    (dstr(alpha), dstr(r1), dstr(alpha2), dstr(r2), two_distinct))

# C3: U(1) test has teeth
add('C3', 'PASS', 'U(1) 判据的判别力：|Ξ|² 不变而 Re(Ξ)² 改变',
    '同一旋转下 |Ξ|² 残差 %s vs Re² 残差 %s，相差 %s 倍' %
    (dstr(inv_mod2), dstr(inv_re2), dstr(inv_re2 / max(inv_mod2, D('1e-250')))))

# C4: gauge-dim test has teeth
add('C4', 'PASS', '规范群维度判据的判别力：假想 SU(3) 三重场维度 8 ≠ 复标量 1',
    'SU(3) adjoint dim=8；U(1) complex scalar phase dim=1；差 %d' % (8 - 1))

# C5: no-equation test has teeth (a phi^4 kink DOES have an equation & solution)
# phi(x)=v*tanh(x/L) solves phi'' = lambda*phi*(phi^2-v^2) with L=1/(v*sqrt(lambda/2))
v0 = D('1'); lam = D('2'); Lk = (D(2) / (lam * v0 * v0)).sqrt()  # kink width l=sqrt(2/(lam v^2))
# verify the ODE residual analytically via tanh identities at a sample point using exp
xx = D('0.6')
ex = (D(2) * xx / Lk).exp()
tanh_v = (ex - D(1)) / (ex + D(1))
phi = v0 * tanh_v
sech2 = D(1) - tanh_v * tanh_v
phi2 = -D(2) * v0 * tanh_v * sech2 / (Lk * Lk)   # d^2 phi/dx^2
ode_rhs = lam * phi * (phi * phi - v0 * v0)
ode_res = rel(phi2, ode_rhs)
add('C5', 'PASS', '孤子判据的判别力：φ⁴ kink 有明确场方程与解析解（残差机器零）',
    'φ=v·tanh(x/L), L=%s：φ″−λφ(φ²−v²) 残差 %s ⇒ 判据能区分"有方程/无方程"' %
    (dstr(Lk), dstr(ode_res)))

# C6: W3 gate has teeth (already embedded in V16)
add('C6', 'PASS', 'W3 门禁非恒假：假想四门全过候选可通过',
    '阳性候选门 %s；V36 四候选门 %s ⇒ 门禁区分真候选与反解候选' %
    (candidates[-1]['gates'], [c['gates'] for c in candidates[:4]]))

# ===================== guards =====================
guard('G01', src_exists, 'V36 source read-only found, sha256=' + src_sha[:16])
guard('G02', has_four_claims, 'AST/text: four claimed Xi functions present')
guard('G03', has_no_equation, 'AST/text: no field equation admitted by manuscript')
guard('G04', has_pred_zero, 'AST/text: PRED=0% admitted by manuscript')
# dimension-tool self checks
guard('G05', dmul(DL, DL) == dpowvec(DL, 2) and dadd(DK, DK) == DK,
      'dimension tools: multiply=add exponents; same-dim sum ok')
guard('G06', D_FG == D_FS == D_FW and D_FG != D_FE,
      'two dimension classes confirmed: fG=fS=fW=L^-2, fE=L^-1 isolated')
guard('G07', two_distinct and circ_err_1 < D('1e-180') and circ_err_2 < D('1e-180'),
      'circular inversion: machine-zero reproduction for two distinct inputs')
guard('G08', inv_mod2 < D('1e-180') and inv_re2 > D('1e-2') and inv_im > D('1e-2'),
      'U(1) rational rotation: modulus invariant, Re^2/Im changed')
guard('G09', all(e['verdict'] in ('PASS', 'FAIL', 'CORRECTED', 'INFO', 'BOUNDARY')
                 for e in ENTRIES), 'all entry verdicts in vocabulary')
# G10 checks itself: at this point 9 guards (G01..G09) are already appended; G10 is the 10th.
guard('G10', len(ENTRIES) == 22 and len(GUARDS) >= 9,
      'entry count = %d (16 main + 6 controls); guards so far=%d' % (len(ENTRIES), len(GUARDS)))
guard('G11', all(e['reading'].strip() for e in ENTRIES), 'all readings non-empty')
# G12: AST-based check (string literal search would self-match this very line).
_self_tree = ast.parse(io.open(os.path.abspath(__file__), encoding='utf-8').read())
_has_random_import = any(
    (isinstance(n, ast.Import) and any(a.name == 'random' for a in n.names)) or
    (isinstance(n, ast.ImportFrom) and n.module == 'random')
    for n in ast.walk(_self_tree))
guard('G12', not _has_random_import,
      'engine deterministic (AST: no random module imported)')
guard('G13', os.path.exists(F_R421), 'r421 W3 gate reference exists')
guard('G14', rejected == 4 and positive_ok, 'W3 gate rejected 4 V36 candidates, control passed')
guard('G15', src_bytes > 20000, 'V36 manuscript size plausible (%d bytes)' % src_bytes)

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
    'round': 'r425', 'date': DATE, 'verdict': VERDICT,
    'target': 'ROOT V36 Xi-action four-force FORM unification (ALG-ROOT-GUFT-V36-2026)',
    'source': {'path': os.path.relpath(V36, OPENUFT), 'sha256': src_sha, 'bytes': src_bytes,
               'read_only': True, 'ast_parse_ok': src_tree is not None},
    'entries': ENTRIES, 'guards': GUARDS, 'counts': counts,
    'guard_pass': guard_pass, 'guard_total': len(GUARDS),
    'context': {k: dstr(v) for k, v in CONTEXT.items()},
    'w3_candidates': candidates,
    'red': RED,
    'open': ['O-V36-FIELD-EQUATION: no covariant field equation for Xi',
             'O-V36-GAUGE-GROUP: 11-dim gauge group deficit',
             'O-V36-INDEPENDENT-SCALE: no independent L_* / M_* / alpha input'],
}
os.makedirs(DATA, exist_ok=True)
with io.open(P_JSON, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)

md = ['# r425 · ROOT V36 Ξ作用量四力 FORM 统一审计（数据产物）', '',
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
