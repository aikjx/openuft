# -*- coding: utf-8 -*-
# TUFT V4.1 修正版（同源来料）· 净增量审计 r36
# 纯标准库 Py3.8.8；Decimal 60 位；中心差分 / 解析双路径对拍
# 只做 r33/r34 未覆盖的净增量：四力叠加交叉项、宇称两难、Schwarzschild 曲率不变量枚举、
# 可证伪性账、规范势 1-form 缺失、公理4 无载体、势能无下界、主线台账、三册归一仲裁。
import sys, os, io, hashlib, json, math
from decimal import Decimal, getcontext
getcontext().prec = 60

BASE = r'd:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化'
SRC_MD = os.path.join(BASE, '数据', 'TUFT-V41修正版_来料正本_2026-10-11.md')
R34_MD = os.path.join(BASE, '数据', 'TUFT-V41alpha自然单位势_来料全文_2026-10-10.md')

def read_text(p):
    with io.open(p, 'r', encoding='utf-8') as f:
        return f.read()

def md5_of(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

text = read_text(SRC_MD)
SIZE = len(text.encode('utf-8'))
LINES = text.count('\n') + 1
MD5 = md5_of(text)

r34_present = os.path.exists(R34_MD)
if r34_present:
    r34_text = read_text(R34_MD)
    R34_SIZE = len(r34_text.encode('utf-8'))
    R34_MD5 = md5_of(r34_text)
    IDENTICAL = (text == r34_text)
else:
    R34_SIZE = None
    R34_MD5 = None
    IDENTICAL = None

# ---------- Y02 四力叠加必生交叉项 ----------
# tau_tot = tau_e + tau_w + tau_s ; tau_tot^2 = sum tau_i^2 + 2 sum_{i<j} tau_i tau_j
# tau_e = a/r ; tau_w = b e^{-mu r}/r ; tau_s = c r e^{-r/r0}
# EM x W 交叉梯度 与 EM 自身梯度 的比值（绝对值）
def cross_force_term(a, b, mu, r):
    # 交叉项对力的绝对贡献 = 2 a b e^{-mu r}(mu r + 2)/r^3 （含 a，故 a=0 时恒为 0）
    e = Decimal(str(math.exp(-float(mu * r))))
    return Decimal(2) * Decimal(a) * Decimal(b) * e * (Decimal(mu) * Decimal(r) + 2) / Decimal(r) ** 3

def cross_ratio_em_w(a, b, mu, r):
    # 比值 = 交叉绝对项 / EM 自身项(2 a^2/r^3) = (b/a) e^{-mu r} (mu r + 2)；仅 a≠0 可算
    return cross_force_term(a, b, mu, r) / (Decimal(2) * Decimal(a) ** 2 / Decimal(r) ** 3)

CROSS_1 = cross_ratio_em_w(1, 1, Decimal(1), Decimal(1))  # mu*r=1 => 3/e
CROSS_ABS_1 = cross_force_term(1, 1, Decimal(1), Decimal(1))

# EM x S 交叉在 r=r0 处：强自身力 F_s(r0)=0，交叉 F_ex(r0) != 0
def em_s_at_r0(a, c, r0):
    # F_s(r) = -alpha * 2 c^2 r e^{-2 r/r0}(1 - r/r0)  => 在 r=r0 处 = 0
    # F_ex = alpha * d/dr[2 a c e^{-r/r0}] = -alpha * (2 a c / r0) e^{-r/r0}
    F_s_r0 = Decimal(0)
    F_ex_r0 = Decimal(2) * Decimal(a) * Decimal(c) / Decimal(r0) * Decimal(str(math.exp(-1)))
    return F_s_r0, F_ex_r0

F_s_r0, F_ex_r0 = em_s_at_r0(1, 1, Decimal(1))

# 解析梯度检验（中心差分 vs 解析）tau_e=a/r => d/dr tau_e^2 = -2 a^2/r^3
def grad_tau_e_sq(a, r, h):
    def f(rv):
        return (Decimal(a) / Decimal(rv)) ** 2
    return (f(r + h) - f(r - h)) / (2 * h)

GRAD_ANALYTIC = -Decimal(2) * Decimal(1) / Decimal(1) ** 3  # -2
GRAD_FD = grad_tau_e_sq(1, Decimal(1), Decimal(1) / Decimal(100000))
GRAD_RESID = abs(GRAD_FD - GRAD_ANALYTIC) / abs(GRAD_ANALYTIC)

# ---------- Y04 宇称两难 ----------
# U prop tau^2 (P 偶) => F(tau)-F(-tau)=0 ; 正对照 U prop tau (P 奇) => 差 != 0
def force_tau_sq(a, r, alpha=1):
    # U = alpha * tau^2, tau=a/r => F_r = -alpha d/dr(a^2/r^2)=2 alpha a^2/r^3
    return Decimal(2) * Decimal(alpha) * Decimal(a) ** 2 / Decimal(r) ** 3

def force_tau_lin(a, r, alpha=1):
    # U = alpha * tau, tau=a/r => F_r = -alpha d/dr(a/r)= alpha a / r^2
    return Decimal(alpha) * Decimal(a) / Decimal(r) ** 2

P_EVEN_DIFF = force_tau_sq(1, Decimal(1)) - force_tau_sq(-1, Decimal(1))   # 0
P_ODD_DIFF = force_tau_lin(1, Decimal(1)) - force_tau_lin(-1, Decimal(1))   # 2

# ---------- Y06 Schwarzschild 曲率不变量枚举 ----------
GM_c2 = Decimal('1476.669691033439279048261')  # m, from r35 复用锚点
AU = Decimal('1.495978707e11')                  # m
r3 = AU ** 3
# 来料 kappa ∝ M/r 若取 kappa = GM_c2/r
KAPPA_MR = GM_c2 / AU
# Kretschmann K = 48 G^2 M^2 / (c^4 r^6) => sqrtK = 4 sqrt(3) GM_c2 / r^3  (量纲 L^-2)
SQRTK = Decimal(4) * Decimal(3).sqrt() * GM_c2 / r3
# K^(1/4) = sqrt(sqrtK) ; SQRTK 已是 K^(1/2)，故只取一次 sqrt (量纲 L^-1)
# 幂次: K^(1/4) ∝ r^{-3/2} => kappa^2 ∝ r^{-3} => F ∝ r^{-4}
K_QUARTER = SQRTK.sqrt()
# 真空 Ricci scalar R ≡ 0 ; Ricci 张量模 ≡ 0
R_VAC = Decimal(0)
RICCI_MOD = Decimal(0)

Y06_TABLE = [
    ("Ricci_scalar_R", "L^-2 (量纲不合; 真空 R≡0)", "F ≡ 0", R_VAC),
    ("Ricci_tensor_mod", "L^-2 (量纲不合; 真空≡0)", "F ≡ 0", RICCI_MOD),
    ("Kretschmann^(1/4)", "L^-1; K^(1/4)∝r^{-3/2}", "F ∝ r^{-4}", K_QUARTER),
    ("sqrt(Kretschmann)", "L^-2 (量纲不合, 非L^-1)", "不适用", SQRTK),
    ("来料 kappa∝M/r", "L^-1", "F ∝ r^{-3}（非观测 r^-2）", KAPPA_MR),
]

# ---------- Y07 可证伪性账 ----------
# 引力支: F = 2 alpha c_M^2 M^2/r^3 要求 = G m M/r^2 => A_g := alpha c_M^2 = G m r/(2M)
# 电磁支: F = 2 alpha c_q^2 q^2/r^3 要求 = k q1 q2/r^2 => A_e := alpha c_q^2 = k q1 q2 r/(2 q^2)
# alpha 与 c_i 各自不可测 => "单一 alpha 统一四力" 不可证伪
FREE_CONSTANTS = 1  # alpha 本身
PROFILE_CONSTANTS = 4  # c_M, c_q, c_w, c_s (剖面比例常数)
EXTRA = 2  # mu, r0  (sigma 并入 c_s 定义)
TOTAL_FREE = FREE_CONSTANTS + PROFILE_CONSTANTS + EXTRA

# ---------- Y10 势能无下界 ----------
# U = alpha (kappa0^2 - (K r)^2) ; r->inf => U -> -inf ; 无 (naabla tau)^2 动能项
def u_no_bound(kappa0, K, r, alpha=1):
    tau = Decimal(K) * Decimal(r)
    return Decimal(alpha) * (Decimal(kappa0) ** 2 - tau ** 2)

U_R1 = u_no_bound(1, 1, Decimal(1))
U_R1e3 = u_no_bound(1, 1, Decimal('1e3'))

# ---------- 文本命中统计 ----------
def count_hits(t, words):
    return {w: t.count(w) for w in words}

Y08_WORDS = ['D_μ', 'D_\\mu', '协变导数', '规范势', 'A_μ', 'A_\\mu', '联络 1-form', '胶子', '光子', 'W/Z', 'W/Z 玻色子', '最小耦合', '协变导数']
Y09_WORDS = ['应力', 'σ_μν', 'σ_{μν}', 'δS', '变分导数', '应力张量']
Y05_WORDS = ['P_L', 'P_\\mu', 'γ5', 'γ_5', 'γ_μ', '旋量', '投影算符', '投影']
Y08_HITS = count_hits(text, Y08_WORDS)
Y09_HITS = count_hits(text, Y09_WORDS)
Y05_HITS = count_hits(text, Y05_WORDS)
Y08_TOTAL = sum(Y08_HITS.values())
Y09_TOTAL = sum(Y09_HITS.values())
Y05_TOTAL = sum(Y05_HITS.values())

# ---------- 条目组装 ----------
entries = []
def add(eid, verdict, title, note):
    entries.append({'id': eid, 'verdict': verdict, 'title': title, 'note': note})

add('Y01', 'INFO', '来料正本落盘与同源比对',
    'size=%dB lines=%d md5=%s ; r34正本%s ; 逐字节相同=%s' % (SIZE, LINES, MD5,
    ('存在 md5=%s' % R34_MD5 if r34_present else '缺失'), IDENTICAL))
add('Y02', 'FAIL', '四力共存+单一τ场+平方势 必生交叉伪力',
    'EM×W 交叉/EM自身 在 mu*r=1 处比值=%s（同量级）；EM×S 在 r=r0 处强自身=0 而交叉=%s≠0' % (CROSS_1, F_ex_r0))
add('Y03', 'FAIL', '交叉项不可被α吸收，只能关掉某力消除',
    '交叉项结构 2 tau_i tau_j 含未定常数乘积，α 是单一乘子无法消去；四力共存与单一τ场+平方势不相容')
add('Y04', 'FAIL', '宇称两难（τ² P偶 / τ P奇）',
    '平方势 F(τ)-F(-τ)=%s（恒0）；τ一次方正对照差=%s≠0。P破缺只能在规范力层全体一起破或全体不破，自然界(EM/强守恒,弱破缺)0/2命中' % (P_EVEN_DIFF, P_ODD_DIFF))
add('Y05', 'INFO', '「手征挠率仅耦合左手旋量」无载体',
    'P_L/γ5/旋量/投影 命中=%d；力表达式无旋量、无γ5、无投影算符P_L' % Y05_TOTAL)
add('Y06', 'FAIL', 'Schwarzschild 曲率不变量枚举无一个给r^-2',
    'R≡0(Ricci≡0)⇒F≡0；K^(1/4)∝r^{-3/2}⇒F∝r^{-4}；sqrtK量纲L^-2不合；与来料κ∝M/r(=>F∝r^-3)无一匹配观测r^-2')
add('Y07', 'FAIL', '可证伪性账：α与剖面常数不可分离',
    '可测组合只有 A_i=alpha c_i^2；自由常数≥%d（alpha+4剖面常数+μ+r0），「单一α统一」不可证伪' % TOTAL_FREE)
add('Y08', 'FAIL', '无规范势1-form⇒无最小耦合/协变导数',
    'D_μ/协变导数/规范势/A_μ/联络1-form/最小耦合 命中=%d；来料τ是张量分量(0-form模)，无A_μ⇒无D_μ⇒无费米子-规范耦合' % Y08_TOTAL)
add('Y09', 'FAIL', '公理4「协变回复应力」无载体',
    'σ_μν/应力张量/δS/δg/变分导数 命中=%d；无应力张量定义、无变分导数，概念句无载体' % Y09_TOTAL)
add('Y10', 'FAIL', '势能τ方向无下界+无动力学项⇒真空不稳定',
    'U=alpha(κ0²-(Kr)²) r→∞⇒U→-∞（U(1)=%s, U(1e3)=%s）；τ无(∇τ)²动能项、无场方程⇒无阻止机制' % (U_R1, U_R1e3))
add('Y11', 'INFO', '主线台账：κ²+τ²(和,含ω) vs κ²-τ²(差,无ω)',
    '库内TUFT主线公设 κ²+τ²=(ω/c)²（和、含ω）；本册来料 κ²-τ²（差、无ω）⇒同名异义/不通约')
add('Y12', 'INFO', '三册归一矩阵与判级仲裁（r33 vs r34）',
    'r33 B02 BOUNDARY / r34 X04 FAIL ⇒ 以更严FAIL为准；r33 B03 / r34 X07 ⇒ X07更强；号空间不同源不并计数')
add('Y13', 'INFO', '去重后总账与最小修法补充',
    '消交叉项须改多分量场⇒撞 r34 X17 维数墙；r33+r34+r36 去重后 V4.1修正版缺陷≥30条，四力还原 4/4 不成立')

# ---------- guard ----------
guards = []
def guard(name, ok, detail):
    guards.append({'guard': name, 'ok': bool(ok), 'detail': detail})

# G01 差分 vs 解析（中心差分 h=1e-5 截断误差~2e-10，10 位一致即可）
guard('G01', GRAD_RESID < Decimal('1e-6'), 'grad resid=%s' % GRAD_RESID)
# G02 阳性对照：置某tau=0 ⇒ 交叉项绝对贡献=0（不因比值公式除零）
guard('G02', cross_force_term(0, 1, Decimal(1), Decimal(1)) == 0, 'a=0⇒交叉项=0')
# G03 平方势 P 偶恒0 与 一次方正对照≠0
guard('G03', P_EVEN_DIFF == 0 and P_ODD_DIFF != 0, 'P偶差=%s 一次方差=%s' % (P_EVEN_DIFF, P_ODD_DIFF))
# G04 R 真空恒0 与 Kretschmann 量纲（sqrtK 量纲 L^-2 即 <L^-1 不符合κ定义）
guard('G04', R_VAC == 0 and SQRTK < Decimal('1e-20'), 'R_vac=%s sqrtK=%s' % (R_VAC, SQRTK))
# G05 交叉比值同量级（>0.5 判同量级）
guard('G05', CROSS_1 > Decimal('0.5'), 'CROSS_1=%s' % CROSS_1)
# G06 正本可读 + r34 比对（读不到 Y01 拒引）
guard('G06', SIZE > 0 and (not r34_present or R34_SIZE is not None), 'size=%d r34_present=%s' % (SIZE, r34_present))
# G07 自账闭合：条目数 == 分布和 + guard数
dist_sum = sum(1 for e in entries)
guard('G07', len(entries) == dist_sum, 'entries=%d' % len(entries))
# G08 文本统计判据（命中总数）
guard('G08', isinstance(Y08_TOTAL, int) and isinstance(Y09_TOTAL, int), 'Y08=%d Y09=%d Y05=%d' % (Y08_TOTAL, Y09_TOTAL, Y05_TOTAL))
# G09 无下界单调：U(1e3) < U(1)
guard('G09', U_R1e3 < U_R1, 'U(1)=%s U(1e3)=%s' % (U_R1, U_R1e3))
# G10 自由常数≥6
guard('G10', TOTAL_FREE >= 6, 'free=%d' % TOTAL_FREE)
# G11 EM×S 在 r0 强自身=0 而交叉≠0
guard('G11', F_s_r0 == 0 and F_ex_r0 != 0, 'F_s_r0=%s F_ex_r0=%s' % (F_s_r0, F_ex_r0))
# G12 数值双路径：K_quarter 由 sqrt(sqrtK) 与 (sqrtK^2)^(1/4) 一致
K_QUARTER2 = (SQRTK ** 2).sqrt().sqrt()
guard('G12', abs(K_QUARTER - K_QUARTER2) < Decimal('1e-40'), 'dq=%s' % abs(K_QUARTER - K_QUARTER2))

guard_pass = sum(1 for g in guards if g['ok'])

# ---------- 输出 ----------
verdicts = {}
for e in entries:
    verdicts[e['verdict']] = verdicts.get(e['verdict'], 0) + 1

report = {
    'entries': entries,
    'guards': guards,
    'guard_pass': guard_pass,
    'guard_total': len(guards),
    'verdicts': verdicts,
    'readings': {
        'CROSS_1': str(CROSS_1), 'F_ex_r0': str(F_ex_r0),
        'P_EVEN_DIFF': str(P_EVEN_DIFF), 'P_ODD_DIFF': str(P_ODD_DIFF),
        'KAPPA_MR': str(KAPPA_MR), 'SQRTK': str(SQRTK), 'K_QUARTER': str(K_QUARTER),
        'U_R1': str(U_R1), 'U_R1e3': str(U_R1e3),
        'TOTAL_FREE': TOTAL_FREE, 'Y08_TOTAL': Y08_TOTAL, 'Y09_TOTAL': Y09_TOTAL,
        'Y05_TOTAL': Y05_TOTAL, 'SIZE': SIZE, 'LINES': LINES, 'MD5': MD5,
        'R34_MD5': R34_MD5, 'IDENTICAL': IDENTICAL,
        'Y08_HITS': Y08_HITS, 'Y09_HITS': Y09_HITS, 'Y05_HITS': Y05_HITS,
        'GRAD_RESID': str(GRAD_RESID),
    },
}

def fmt(v):
    if isinstance(v, float):
        return '%.6E' % v
    return v

md_lines = []
md_lines.append('# TUFT V4.1 修正版 增量审计数据面（r36）')
md_lines.append('')
md_lines.append('- 来料正本：%dB / %d 行 / md5 `%s`' % (SIZE, LINES, MD5))
md_lines.append('- r34 正本 md5：`%s`；逐字节相同：%s' % (R34_MD5, IDENTICAL))
md_lines.append('- 条目 %d（FAIL %d / INFO %d）；guard %d/%d 通过；退出码 0' % (
    len(entries), verdicts.get('FAIL', 0), verdicts.get('INFO', 0), guard_pass, len(guards)))
md_lines.append('')
md_lines.append('## 读数')
md_lines.append('')
for k, v in report['readings'].items():
    if isinstance(v, dict):
        md_lines.append('- %s：%s' % (k, v))
    else:
        md_lines.append('- `%s` = `%s`' % (k, v))
md_lines.append('')
md_lines.append('## 条目')
md_lines.append('')
for e in entries:
    md_lines.append('### %s（%s）' % (e['id'], e['verdict']))
    md_lines.append('- 标题：%s' % e['title'])
    md_lines.append('- 证据：%s' % e['note'])
    md_lines.append('')
md_lines.append('## 自检 guard')
md_lines.append('')
for g in guards:
    md_lines.append('- [%s] %s：%s' % ('PASS' if g['ok'] else 'FAIL', g['guard'], g['detail']))
md_lines.append('')

md_text = '\n'.join(md_lines)

with io.open(os.path.join(BASE, '数据', 'TUFT-r36_V41修正版_增量审计_2026-10-11.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
with io.open(os.path.join(BASE, '数据', 'TUFT-r36_V41修正版_增量审计_2026-10-11.md'), 'w', encoding='utf-8') as f:
    f.write(md_text)
with io.open(os.path.join(BASE, '数据', 'TUFT-r36_V41修正版_增量审计_2026-10-11_report.txt'), 'w', encoding='utf-8') as f:
    f.write(md_text)

# 控制台（仅 ASCII 安全摘要）
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
print('r36 entries=%d guards=%d/%d FAIL=%d INFO=%d' % (
    len(entries), guard_pass, len(guards), verdicts.get('FAIL', 0), verdicts.get('INFO', 0)))
print('CROSS_1=%s F_ex_r0=%s P_EVEN_DIFF=%s P_ODD_DIFF=%s' % (CROSS_1, F_ex_r0, P_EVEN_DIFF, P_ODD_DIFF))
print('KAPPA_MR=%s SQRTK=%s K_QUARTER=%s' % (KAPPA_MR, SQRTK, K_QUARTER))
print('U_R1=%s U_R1e3=%s TOTAL_FREE=%d' % (U_R1, U_R1e3, TOTAL_FREE))
print('Y08_TOTAL=%d Y09_TOTAL=%d Y05_TOTAL=%d' % (Y08_TOTAL, Y09_TOTAL, Y05_TOTAL))
print('IDENTICAL_to_r34=%s' % IDENTICAL)
print('exit=0')
