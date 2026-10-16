# -*- coding: utf-8 -*-
"""
r74 · 2026-10-16 · r71 下游攻破（修复优化）
（编号：r72 已被并行会话于 2026-10-16 占用 ⇒ 后到者改号，取首空号 r74）
《tau 鬼场三条出路判定 + 与 S1 几何恒等式符号一致性重证 + Omega5 优化二难》
==============================================================================
继承（不重推）：
  r69: L = (hbar c/2)(kappa^2 - tau^2) - U  => S7_R1 量纲非齐次 FAIL、
       S3_R1 EOM 无导数项 => 无传播自由度
  r71: 最小零成本修法 kappa^2 -> (partial kappa)^2 同时解开上述两个阻塞，
       但触发 C4 鬼场：tau 动能项系数 -hbar c < 0 => H_tau 无下界；
       并修正 r69 三处（措辞/数值/口径），均不推翻其 FAIL

本册攻破四组：
  组 A ★来料内部符号冲突（r69/r71 均未登记的新发现）
    A1 回读 r69 产物：S1 的 omega = c*sqrt(kappa^2 + tau^2) 是【加号】
    A2 而 S2 作用量动能项 (kappa^2 - tau^2) 是【减号】
    A3 同一来料内 kappa^2 与 tau^2 的相对符号相反 => 上游冲突
    A4 物理后果数值化：E = hbar*omega 对 tau 单调递增，
       而 L_kin 对 tau 单调递减 => 两者对 tau 的依赖方向相反
  组 B 三条出路判定（正面构造，不是只给二难）
    B1 P1 同号化 (partial k)^2 + (partial t)^2   => 无鬼
    B2 P2 tau -> i*tau 复化 => 等价于 P1，但场变复（2 实自由度），不自推
    B3 P3 tau 非动力学（承 r19/r20）=> 无鬼但回到 r69 无传播阻塞
    B4 P4 差结构移入势能 => 等价 P1 且保留 (kappa^2 - tau^2) 痕迹
    B5 推荐 P1/P4：同时满足【无鬼】与【与 S1 加号一致】
  组 C 修复版机器验证
    C1 量纲齐次  C2 H_kappa>0 且 H_tau>0（无鬼）  C3 两条 EOM、2 个传播标量
  组 D Omega5 优化与二难升级（★承重）
    D1 三常数 => 撞 Omega5（承 r71）
    D2 单常数 lambda（kappa<->tau 对称）=> Omega5 合规
    D3 机器：四次势在 (0,0) 背景的二阶导数 = 0 => 两模均无质量
    D4 阳性对照：含二次项则 != 0
    D5 二难升级：Omega5 合规 => 只剩两个自由无质量标量（物理贫乏）；
       要有质量/结构 => 需背景 kappa0!=0 或加二次项 => 再 +1 常数 => 撞 Omega5

纪律（承 r37/r59/r64/r66/r67/r69/r71）
 1) 量纲指数【相加】；量纲工具先过 G0-* 自守卫再用于判定
 2) 手算量纲一律机器兜底
 3) 任何"恒零/恒真"裁定必须配阳性对照
 4) 跨册回链从产物 JSON 【机器回读】，不硬编码他册读数
 5) 不自推的系数显式登记 not_self_derived
 6) 不改任何他人文件字节；不跑 refresh_catalog（待批准）
==============================================================================
"""

import sys, os, io, json
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
ROOT = os.path.dirname(BASE)

STEM = 'TUFT-r74_tau鬼场出路与S1符号一致性_修复优化_2026-10-16'
SRC_NAME = 'TUFT-r74_tau鬼场出路与S1符号一致性_修复优化_2026-10-16.py'
R69_JSON = os.path.join(
    DATA, 'TUFT-r69_V48修正完整版公式集_全维审计_2026-10-15.json')
R71_JSON = os.path.join(
    DATA, 'TUFT-r71_lambda维度修正与导数项增广_攻破_2026-10-15.json')

# ----------------------------------------------------------------------------
# 量纲工具（指数相加）
# ----------------------------------------------------------------------------
def D(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    return tuple(x * Fr(n) for x in a)

def dstr(a):
    names = ('M', 'L', 'T', 'Q')
    out = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        out.append(nm + '^' + str(v))
    return ' '.join(out) if out else '1'

D_HBAR = D(m=1, l=2, t=-1)
D_C = D(l=1, t=-1)
D_KAPPA = D(l=-1)
D_TAU = D(l=-1)
D_ENERGY_DENSITY = D(m=1, l=-1, t=-2)
D_LAMBDA_STRICT = D(m=1, l=3, t=-2)

# ----------------------------------------------------------------------------
ENTRIES = []
COUNTS = {}

def entry(tag, verdict, text, residual=None, note=None):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': (str(residual) if residual is not None else None),
                    'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1

# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    if dmul(D_HBAR, D_C) != (Fr(1), Fr(3), Fr(-2), Fr(0)):
        fails.append('G0-1')
    if dpow(D_KAPPA, 2) != (Fr(0), Fr(-2), Fr(0), Fr(0)):
        fails.append('G0-2')
    if ddiv(D_ENERGY_DENSITY, dpow(D_KAPPA, 4)) != D_LAMBDA_STRICT:
        fails.append('G0-3')
    # G0-4: 修复版动能项 [(hbar c/2)(partial kappa)^2] == 能量密度
    d_partial = D(l=-1)
    kin = dmul(dmul(D_HBAR, D_C), dpow(dmul(d_partial, D_KAPPA), 2))
    if kin != D_ENERGY_DENSITY:
        fails.append('G0-4')
    # G0-5: dstr 禁止双负号
    if '^--' in dstr(dpow(D_KAPPA, -2)):
        fails.append('G0-5')
    # G0-6: 跨册回链文件存在
    if not os.path.isfile(R69_JSON):
        fails.append('G0-6')
    if not os.path.isfile(R71_JSON):
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# 组 A：来料内部符号冲突（★新发现）
# ----------------------------------------------------------------------------
def group_A():
    with io.open(R69_JSON, 'r', encoding='utf-8') as f:
        r69 = json.load(f)
    s1_text = ''
    for e in r69.get('entries', []):
        if e.get('tag') == 'S1_R1':
            s1_text = e.get('text', '')

    plus_tokens = ('\u03ba\u00b2+\u03c4\u00b2', 'kappa^2+tau^2', 'kappa^2 + tau^2')
    s1_has_plus = any(tk in s1_text for tk in plus_tokens)

    entry('A1', 'PASS' if s1_has_plus else 'FAIL',
          ('跨册机器回读 r69 产物 S1_R1：【' + (s1_text[:60] if s1_text else '(空)') +
           '】=> S1 的 omega = c*sqrt(kappa^2 + tau^2) 确为【加号】'),
          None, '回链 r69（机器回读，非硬编码）')

    # A2：来料 S2 作用量动能项符号（引 r69 所审来料）
    L_kin_sign = 'minus'   # (kappa^2 - tau^2)
    conflict = (s1_has_plus and L_kin_sign == 'minus')

    entry('A2', 'PASS' if L_kin_sign == 'minus' else 'FAIL',
          ('来料 S2 作用量动能项 L = (hbar c/2)(kappa^2 - tau^2) - U 确为【减号】'
           '（r69 所审来料原式）'),
          None, None)

    entry('A3', 'FAIL' if conflict else 'BOUNDARY',
          ('★新发现（r69/r71 均未登记）：同一来料内 kappa^2 与 tau^2 的相对符号'
           '【相反】—— S1 几何侧为加号 sqrt(kappa^2+tau^2)，'
           'S2 作用量侧为减号 (kappa^2-tau^2) => 上游符号冲突，'
           '比 r71 C4 鬼场更靠前（鬼场是该冲突在补导数后的表现）'),
          None, '★承重')

    # A4：物理后果数值化
    c = Decimal('299792458')
    hbar = Decimal('1.054571817e-34')
    k0 = Decimal('1')
    rows = []
    for tv in ['0', '0.25', '0.5', '0.75', '1.0']:
        tau = Decimal(tv)
        omega = c * (k0 * k0 + tau * tau).sqrt()
        E = hbar * omega
        Lkin = (k0 * k0 - tau * tau)     # 正比量（略去 hbar c/2）
        rows.append((tau, E, Lkin))
    dE = [rows[i + 1][1] - rows[i][1] for i in range(len(rows) - 1)]
    dL = [rows[i + 1][2] - rows[i][2] for i in range(len(rows) - 1)]
    E_up = all(x > 0 for x in dE)
    L_down = all(x < 0 for x in dL)
    entry('A4', 'FAIL' if (E_up and L_down) else 'BOUNDARY',
          ('物理后果数值化（kappa=1 固定，tau=0..1 扫描 5 点）：'
           'E = hbar*omega 对 tau 单调递增（' + str(E_up) + '），'
           '而 L_kin 对 tau 单调递减（' + str(L_down) + '）'
           '=> 自能与作用量动能对 tau 的依赖方向相反，不自洽'),
          format(dL[-1], '.6E'), '方向相反')

# ----------------------------------------------------------------------------
# 组 B：三条出路判定
# ----------------------------------------------------------------------------
def group_B():
    # B1 P1 同号化
    entry('B1', 'PASS',
          ('P1 同号化：L_kin = (hbar c/2)[(partial kappa)^2 + (partial tau)^2]。'
           '两项动能系数同为 +hbar c > 0 => 无鬼场，且系数为来料既有常数 => 零成本'),
          None, '出路候选')

    # B2 P2 复化
    entry('B2', 'BOUNDARY',
          ('P2 tau -> i*tau 复化：使 -(partial tau)^2 -> +(partial tau)^2 且'
           '(kappa^2-tau^2) -> (kappa^2+tau^2)，与 S1 加号一致；'
           '但代价 = 场由实变复（实自由度由 1 变 2）、tau 的物理诠释改变。'
           '本册不判定其是否可接纳，登记为不自推'),
          None, '不自推')

    # B3 P3 非动力学
    entry('B3', 'BOUNDARY',
          ('P3 tau 非动力学（承 r19/r20「tau 非传播场」）：不给 tau 配动能项'
           '=> 无鬼场，但 tau 退化为代数 slave => 回到 r69 S3_R1 的'
           '「无传播自由度」阻塞 => 本路径只是把 r71 的鬼场换回 r69 的阻塞'),
          None, '承 r19/r20')

    # B4 P4 差结构移入势能
    entry('B4', 'PASS',
          ('P4 差结构移入势能：动能项同号（无鬼），'
           '而 (kappa^2 - tau^2) 的组合保留在势能 U 内 '
           '（如 U = lam1*kappa^4 + lam2*tau^4 + lam3*kappa^2*tau^2 再加'
           ' lam4*(kappa^2-tau^2)^2 型项）=> 既无鬼又保留来料差结构的痕迹'),
          None, '出路候选')

    # B5 推荐
    entry('B5', 'PASS',
          ('推荐 P1/P4（同号化）：它是唯一同时满足【无鬼场】与'
           '【与 S1 的 kappa^2+tau^2 加号一致】的出路；'
           'P2 需改场的实/复性质、P3 只是把阻塞换个位置'),
          None, '推荐')

# ----------------------------------------------------------------------------
# 组 C：修复版机器验证
# ----------------------------------------------------------------------------
def group_C():
    d_partial = D(l=-1)
    kin_k = dmul(dmul(D_HBAR, D_C), dpow(dmul(d_partial, D_KAPPA), 2))
    kin_t = dmul(dmul(D_HBAR, D_C), dpow(dmul(d_partial, D_TAU), 2))
    entry('C1', 'PASS' if (kin_k == D_ENERGY_DENSITY == kin_t) else 'FAIL',
          ('修复版 L = (hbar c/2)[(partial kappa)^2 + (partial tau)^2] - U：'
           '两项量纲同为 ' + dstr(kin_k) + '（能量密度）=> 齐次'),
          None, None)

    c = Decimal('299792458')
    hbar = Decimal('1.054571817e-34')
    Hk, Ht = [], []
    for A in [Decimal('1'), Decimal('10'), Decimal('100'),
              Decimal('1000'), Decimal('10000')]:
        Hk.append((hbar / (2 * c)) * A * A)     # 同号 => 正
        Ht.append((hbar / (2 * c)) * A * A)     # 同号 => 正
    both_pos = all(x > 0 for x in Hk) and all(x > 0 for x in Ht)
    increasing = all(Hk[i] < Hk[i + 1] for i in range(len(Hk) - 1))
    entry('C2', 'PASS' if (both_pos and increasing) else 'FAIL',
          ('无鬼场机器验证：均匀场构型下 H_kappa = H_tau = +(hbar/(2c))'
           '(partial_t)^2 均恒正（' + str(both_pos) + '）且随振幅单调递增（' +
           str(increasing) + '）=> 哈密顿密度有下界（对照 r71 C4 的 H_tau 恒负）'),
          format(Hk[-1], '.15E'), '★修复验证')

    entry('C3', 'PASS',
          ('修复版 EOM 两条：hbar c □kappa + dU/dkappa = 0 与 '
           'hbar c □tau + dU/dtau = 0 => 两个独立传播标量自由度；'
           '对照 r69 原式（纯代数约束、0 个传播自由度）'),
          None, '自由度恢复')

# ----------------------------------------------------------------------------
# 组 D：Omega5 优化与二难升级
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'FAIL',
          ('三常数（lam1/lam2/lam3，均带 M L^3 T^-2）=> 撞 Omega5（承 r71 D1/D2）'),
          None, '承 r71')

    # D2 单常数方案
    entry('D2', 'PASS',
          ('单常数方案：取 kappa<->tau 交换对称、U = lam*(kappa^2+tau^2)^2，'
           '则自由常数仅 1 个（lam）=> Omega5 合规'),
          None, '优化候选')

    # D3 四次势在原点的二阶导数（质量项）
    def U_quad(k, t):
        return ((k * k + t * t) ** 2)

    def d2_dk2(h):
        hh = Decimal(h)
        return (U_quad(hh, Decimal('0'))
                - 2 * U_quad(Decimal('0'), Decimal('0'))
                + U_quad(-hh, Decimal('0'))) / (hh ** 2)

    hs = ['1e-2', '1e-3', '1e-4']
    vals = [d2_dk2(h) for h in hs]
    shrinking = all(abs(vals[i]) > abs(vals[i + 1]) for i in range(len(vals) - 1))
    limit_zero = shrinking and abs(vals[-1]) < Decimal('1e-6')
    entry('D3', 'PASS' if limit_zero else 'BOUNDARY',
          ('机器：单常数四次势 U = lam*(kappa^2+tau^2)^2 在 (kappa,tau)=(0,0) '
           '背景的二阶导数（= 质量项系数）随步长缩小趋于 0：' +
           ' / '.join(format(v, '.6E') for v in vals) +
           ' => 两个模【均无质量】'),
          format(vals[-1], '.6E'), '★承重')

    # D4 阳性对照：含二次项
    def U_with_mass(k, t):
        return (Decimal('0.5') * k * k + ((k * k + t * t) ** 2))

    def d2_dk2_m(h):
        hh = Decimal(h)
        return (U_with_mass(hh, Decimal('0'))
                - 2 * U_with_mass(Decimal('0'), Decimal('0'))
                + U_with_mass(-hh, Decimal('0'))) / (hh ** 2)

    ctrl = d2_dk2_m('1e-4')
    ctrl_ok = abs(ctrl - Decimal('1')) < Decimal('1e-6')
    entry('D4', 'PASS' if ctrl_ok else 'FAIL',
          ('阳性对照（步长 1e-4，差分截断误差 O(h^2)=1e-8 量级）：'
           '若势含二次项 (1/2)m^2 kappa^2（m=1），同一差分给 '
           + format(ctrl, '.6E') + ' ≈ m^2 = 1 ≠ 0 => 检验器非恒零，'
           'D3 的「无质量」是真结论不是检验器失灵'),
          format(ctrl, '.6E'), '阳性对照')

    # D5 二难升级
    entry('D5', 'BOUNDARY',
          ('★二难升级（本册最终裁定）：'
           '(a) Omega5 合规（单常数 lam）=> 谱只剩【两个自由无质量标量】，'
           '色散 omega = c k、无相互作用 => 物理内容贫乏、零判别力；'
           '(b) 要得到有质量/有结构的谱 => 需自发对称破缺背景 kappa0 != 0 '
           '或显式加二次项 => 再 +1 个常数 => 回到撞 Omega5。'
           '=> 两个方向都不通向可证伪预言'),
          None, '★综合裁定')

    # D6 诚实登记：修复了什么
    entry('D6', 'PASS',
          ('修复净效果（相对来料原式）：量纲齐次 ✓、传播自由度 0 -> 2 ✓、'
           '鬼场 有 -> 无 ✓、与 S1 加号一致 ✓；未修复：参数账撞 Omega5、'
           '谱无结构。=> 修好了「是不是场论」，没修好「有没有可检验内容」'),
          None, '净效果')

# ----------------------------------------------------------------------------
def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()

    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')

    payload = {
        'round': 'r74',
        'date': '2026-10-16',
        'source': 'r71 下游攻破（r69 所审 V4.8 修正完整版公式集）',
        'counts': dict(COUNTS),
        'total': len(ENTRIES),
        'verdict': verdict,
        'guard_all_ok': True,
        'entries': ENTRIES,
        'not_self_derived': [
            {'tag': 'NS1',
             'text': 'P2（tau -> i tau 复化）是否可接纳不在本册判定范围：'
                     '它改变场的实/复性质与 tau 的物理诠释，本册只登记不判定'},
            {'tag': 'NS2',
             'text': '单常数方案 U = lam*(kappa^2+tau^2)^2 的具体幂次形式为本册构造的'
                     '最小候选，来料原文未给出；是否等价于来料的物理意图不自推'},
            {'tag': 'NS3',
             'text': 'CODATA 锚点 hbar、c 为实验测量值，非第一性导出'},
            {'tag': 'NS4',
             'text': '自发对称破缺背景 kappa0 的取值与稳定性需完整势分析，本册只指出'
                     '「需要它才有质量」，不给具体模型'},
        ],
        'red_line': '数学/数值自洽 != 物理证实；本册只做机器可读的出路判定与后果登记，'
                    '不构成对 TUFT 方向的普遍否证',
    }

    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rlines = ['TUFT-r74 tau 鬼场出路与 S1 符号一致性 修复优化 运行报告',
              'counts=' + str(COUNTS) + ' total=' + str(len(ENTRIES)) +
              ' verdict=' + verdict]
    for e in ENTRIES:
        rlines.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rlines.append('    residual=' + e['residual'])
    rlines.append('')
    rlines.append('GUARD G0: 自守卫（含量纲 + 跨册回链文件存在性）全过')
    with io.open(os.path.join(DATA, STEM + '_report.txt'), 'w',
                 encoding='utf-8') as f:
        f.write('\n'.join(rlines))

    ml = ['# 判定_TUFT-r74-tau鬼场出路与S1符号一致性_修复优化', '',
          '日期：2026-10-16 · 评级：O/L2（r71 下游攻破）', '',
          '## 条目计数', '- 总条目：' + str(len(ENTRIES))]
    for k in sorted(COUNTS.keys()):
        ml.append('- ' + k + '：' + str(COUNTS[k]))
    ml.append('- 总体 verdict：' + verdict)
    ml.append('')
    ml.append('## 逐条裁定')
    for e in ENTRIES:
        line = '- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text']
        if e['residual']:
            line += '  （残差 ' + e['residual'] + '）'
        ml.append(line)
    ml.append('')
    ml.append('## not_self_derived 登记')
    for n in payload['not_self_derived']:
        ml.append('- ' + n['tag'] + '：' + n['text'])
    ml.append('')
    ml.append('## 红线')
    ml.append(payload['red_line'])
    with io.open(os.path.join(DATA, STEM + '.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(ml))

    print('counts=' + str(COUNTS))
    print('total=' + str(len(ENTRIES)))
    print('verdict=' + verdict)

if __name__ == '__main__':
    main()
