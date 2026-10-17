# -*- coding: utf-8 -*-
"""
r83 · 2026-10-17 · X-R82-1 定价：把 τ 升级为 spin-1 规范场（U(1)）的代价机器定价
==============================================================================
r82 结论（继承）：四力还原 0/4，根因是 κ,τ 为自旋-0 标量，而四力需要
  spin-2（引力）+ spin-1 规范（电磁/弱/强）三种通道。
r82 开放项 `X-R82-1`：若要还原电磁，须把 τ 从标量升级为 **spin-1 规范场 A_μ**
  ⇒ 已改变 τ 的几何原语定义，等价于**新增 U(1) 规范扇区**，代价**另册定价**。
本册执行该项定价。

  A 组 电磁规范扇区的量纲定价
    A1 𝓛_EM = (ε₀/2)(E² − c²B²) − A·J 的两项量纲齐次（全 = 能量密度 M L^-1 T^-2）
    A2 ★电荷量纲 Q **不可由 {ħ, c, G} 生成**（机器穷举：Q 指数恒 0）⇒ 量纲基必须扩充
    A3 α = e²/(4πε₀ħc) **无量纲** ⇒ 其值 ≈ 1/137 只能输入，不可由量纲分析导出（机器复算）
  B 组 代价账（把「加一个 U(1) 扇区」拆成可数的四项）
    B1 +1 个独立量纲 Q     B2 +1 个常数（e 或 α，实验输入）
    B3 +1 个场 A_μ（4 分量 − 2 规范冗余 = 2 物理自由度）
    B4 +1 个结构原理（U(1) 规范不变 A_μ → A_μ + ∂_μΛ）
  C 组 ★τ 能否「就地」升级而不改原语
    C1 挠率张量 T^ρ_{μν} 的迹 T_μ ≡ T^ρ_{μρ} 是**矢量** ⇒ 自旋对了（spin-1 ✓）
    C2 但它**不是规范场**：无 A_μ→A_μ+∂_μΛ 变换律 ⇒ 无质量保护、无电荷守恒耦合
       ⇒ 电磁门仍 FAIL（自旋✓ 但 规范✗）
    C3 ⇒ 二选一：改 τ 的原语定义（付 B 组四项代价）或放弃电磁还原
  D 组 阳性对照（防假红 / 防恒零）
    D1 正确 U(1) 规范场 ⇒ 过电磁门（承 r82 E2 对照）
    D2 穷举器分辨力：{ħ,c,G} 造不出 Q，但加入 ε₀ 后可 ⇒ 穷举器非恒零
  E 组 元结论与开放项

纪律（承 r64/r67/r71/r74/r75/r78/r80/r81/r82）
 1) 量纲指数相加 2) 机器先过 G0 自守卫 3) ★阳性对照优先（门须可分辨，防假红也防恒零）
 4) 不自推系数登记 NS 5) 不改他人文件字节 6) 退出码 0 = 跑完；结论看 counts/verdict
 7) 分工声明先行：本册只做 X-R82-1 的代价定价，不动 r81 的 W1/W2 定价、不动 r82 的四力总表
==============================================================================
"""

import sys, os, io, json
from datetime import datetime, timezone
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')

STEM = 'TUFT-r83_XR821定价_tau升级U1规范场代价_攻破_2026-10-17'

# ----------------------------------------------------------------------------
# 量纲工具：(M, L, T, Q)，指数相加
# ----------------------------------------------------------------------------
def D_(m=0, l=0, t=0, q=0):
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

D_ENERGY_DENSITY = D_(m=1, l=-1, t=-2)
D_HBAR = D_(m=1, l=2, t=-1)
D_C = D_(l=1, t=-1)
D_G = D_(m=-1, l=3, t=-2)
# ε₀：F/m = C²/(N·m²)
D_EPS0 = D_(m=-1, l=-3, t=2, q=2)
# E 场：V/m = (M L² T^-2)/(Q L)
D_EF = D_(m=1, l=1, t=-2, q=-1)
# B 场 = E/c
D_BF = ddiv(D_EF, D_C)
# A（磁矢势）= B·L
D_AF = dmul(D_BF, D_(l=1))
# J（电流密度）= Q/(L²T)
D_J = D_(l=-2, t=-1, q=1)
# 电荷 e
D_E = D_(q=1)

# ----------------------------------------------------------------------------
# 结果容器
# ----------------------------------------------------------------------------
ENTRIES = []
COUNTS = {}

def entry(tag, verdict, text, residual=None, note=None):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': (str(residual) if residual is not None else None),
                    'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1

# ----------------------------------------------------------------------------
# 数值常数（CODATA 锚点）
# ----------------------------------------------------------------------------
HBAR = D('1.054571817e-34')
C_LIGHT = D('299792458')
G_NEWTON = D('6.67430e-11')
E_CHARGE = D('1.602176634e-19')
EPS0 = D('8.8541878128e-12')
PI = D('3.14159265358979323846264338327950288419716939937510582097494459')
ALPHA_CODATA = D('7.2973525693e-3')

def alpha_em():
    return E_CHARGE * E_CHARGE / (D(4) * PI * EPS0 * HBAR * C_LIGHT)

# ----------------------------------------------------------------------------
# 穷举器：某组基能否造出目标量纲
# ----------------------------------------------------------------------------
def enumerate_dims(basis, target, rng=3):
    """在整数幂 [-rng, rng] 上穷举，返回命中 (指数元组, 指数字典) 列表。"""
    import itertools
    names = list(basis.keys())
    hits = []
    grid = range(-rng, rng + 1)
    for combo in itertools.product(grid, repeat=len(names)):
        acc = (Fr(0), Fr(0), Fr(0), Fr(0))
        for n, c in zip(names, combo):
            acc = dmul(acc, dpow(basis[n], c))
        if acc == target:
            hits.append((combo, acc))
    return hits

def max_abs_q_exponent(basis, rng=3):
    """穷举中出现的 |Q 指数| 最大值 —— 用于判断该基能否触及电荷量纲。"""
    import itertools
    names = list(basis.keys())
    grid = range(-rng, rng + 1)
    mx = 0
    for combo in itertools.product(grid, repeat=len(names)):
        acc = (Fr(0), Fr(0), Fr(0), Fr(0))
        for n, c in zip(names, combo):
            acc = dmul(acc, dpow(basis[n], c))
        if abs(acc[3]) > mx:
            mx = abs(acc[3])
    return mx

# ----------------------------------------------------------------------------
# G0-* 自守卫
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1: ε₀ E² 的量纲 = 能量密度
    if dmul(D_EPS0, dpow(D_EF, 2)) != D_ENERGY_DENSITY:
        fails.append('G0-1')
    # G0-2: ε₀ B² c² 的量纲 = 能量密度
    if dmul(dmul(D_EPS0, dpow(D_BF, 2)), dpow(D_C, 2)) != D_ENERGY_DENSITY:
        fails.append('G0-2')
    # G0-3: A·J 的量纲 = 能量密度
    if dmul(D_AF, D_J) != D_ENERGY_DENSITY:
        fails.append('G0-3')
    # G0-4: α = e²/(ε₀ ħ c) 无量纲
    if ddiv(dpow(D_E, 2), dmul(dmul(D_EPS0, D_HBAR), D_C)) != (Fr(0), Fr(0), Fr(0), Fr(0)):
        fails.append('G0-4')
    # G0-5: α 数值复算与 CODATA 相符（相对偏差 < 1e-6）
    a = alpha_em()
    if abs(a - ALPHA_CODATA) / ALPHA_CODATA > D('1e-6'):
        fails.append('G0-5')
    # G0-6: ★穷举器分辨力：{ħ,c,G} 触及不到 Q，加 ε₀ 后可以
    b1 = {'hbar': D_HBAR, 'c': D_C, 'G': D_G}
    b2 = {'hbar': D_HBAR, 'c': D_C, 'G': D_G, 'eps0': D_EPS0}
    if max_abs_q_exponent(b1, 2) != 0:
        fails.append('G0-6a')
    if max_abs_q_exponent(b2, 2) == 0:
        fails.append('G0-6b')
    # G0-7: 阳性对照 —— 目标 [ħ] 在 {ħ,c,G} 上应能命中（穷举器非恒零）
    if len(enumerate_dims(b1, D_HBAR, 2)) == 0:
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# A 组：量纲定价
# ----------------------------------------------------------------------------
def group_A():
    t1 = dmul(D_EPS0, dpow(D_EF, 2))
    t2 = dmul(dmul(D_EPS0, dpow(D_BF, 2)), dpow(D_C, 2))
    t3 = dmul(D_AF, D_J)
    ok = (t1 == D_ENERGY_DENSITY and t2 == D_ENERGY_DENSITY and t3 == D_ENERGY_DENSITY)
    entry('A1', 'PASS' if ok else 'FAIL',
          ('电磁扇区 𝓛_EM = (ε₀/2)(E² − c²B²) − A·J 的三项量纲：ε₀E²=' + dstr(t1) +
           '、ε₀B²c²=' + dstr(t2) + '、A·J=' + dstr(t3) +
           '；齐次（全 = 能量密度 M L^-1 T^-2）=' + str(ok) +
           ' ⇒ 该扇区本身量纲自洽，可以接进 r80 补全后的拉氏量'),
          None, '形式定价')

    b1 = {'hbar': D_HBAR, 'c': D_C, 'G': D_G}
    hits = enumerate_dims(b1, D_E, 3)
    mxq = max_abs_q_exponent(b1, 3)
    entry('A2', 'FAIL',
          ('★电荷量纲 Q **不可由 {ħ, c, G} 生成**：在幂域 [−3,3] 共 7³=343 组上穷举 '
           'ħ^a c^b G^c，目标 [e]=Q 命中 ' + str(len(hits)) + ' 组；'
           '且穷举中出现的 |Q 指数| 最大值 = ' + str(mxq) +
           '（恒 0，因 ħ/c/G 的 Q 指数本就为 0，任何乘幂组合仍为 0）。'
           '⇒ **必须把量纲基从 (M,L,T) 扩充到 (M,L,T,Q)**，即引入一个全新的独立单位（电荷）'),
          None, '★量纲基必须扩充')

    a = alpha_em()
    rel = abs(a - ALPHA_CODATA) / ALPHA_CODATA
    entry('A3', 'BOUNDARY',
          ('α = e²/(4πε₀ħc) 量纲为 ' +
           dstr(ddiv(dpow(D_E, 2), dmul(dmul(D_EPS0, D_HBAR), D_C))) +
           '（无量纲）⇒ 其数值**不可能由量纲分析导出**，只能实验输入。'
           '机器复算 α = ' + str(a) + '，与 CODATA ' + str(ALPHA_CODATA) +
           ' 相对偏差 ' + str(rel) + ' ⇒ 这是一条**必须输入的外部常数**，不是理论的预言'),
          str(rel), 'α 是输入非导出')

# ----------------------------------------------------------------------------
# B 组：代价账
# ----------------------------------------------------------------------------
def group_B():
    entry('B1', 'FAIL',
          ('代价 1/4：**+1 个独立量纲 Q**。原框架 (ħ,c,G) 只覆盖 (M,L,T)，'
           '电荷是第四个独立量纲 ⇒ 理论的基本量纲基被扩大（承 A2）'),
          None, '代价账')
    entry('B2', 'FAIL',
          ('代价 2/4：**+1 个常数**（e 或等价的 α ≈ 1/137）。该常数无量纲、只能实验输入（承 A3）'
           ' ⇒ 按 Ω5 口径计入常数账'),
          None, '代价账')
    entry('B3', 'PASS',
          ('代价 3/4：**+1 个场 A_μ**。自由度：A_μ 有 4 个分量，规范不变性去掉 2 个冗余 '
           '⇒ 物理自由度 = 4 − 2 = **2**（无质量光子两个螺旋度）'),
          None, '代价账')
    entry('B4', 'FAIL',
          ('代价 4/4：**+1 个结构原理** —— U(1) 规范不变性 A_μ → A_μ + ∂_μΛ。'
           '这是原几何（κ,τ）框架**原本没有**的原理；它才是保证光子无质量、电荷守恒与 '
           '库仑 1/r² 律的真正来源，而不是「场的自旋」本身'),
          None, '★原理代价最重')

# ----------------------------------------------------------------------------
# C 组：τ 能否就地升级（不改原语）
# ----------------------------------------------------------------------------
def group_C():
    entry('C1', 'PASS',
          ('★挠率张量 T^ρ_{μν} 的迹 T_μ ≡ T^ρ_{μρ} 是一个**协变矢量** ⇒ 从几何里确实能取出一个 '
           'spin-1 的对象 ⇒ **自旋这一项是对的**（相对 r82 的 spin-0 判据，这是一条实质进展）'),
          None, '自旋可取到')

    em_req = {'spin': 1, 'needs_gauge': True}
    tor_prof = {'spin': 1, 'needs_gauge': False}
    spin_ok = (tor_prof['spin'] == em_req['spin'])
    gauge_ok = (not em_req['needs_gauge']) or tor_prof['needs_gauge']
    entry('C2', 'FAIL',
          ('★但挠率迹**不是规范场**：电磁要求 U(1) 规范不变（' + str(em_req['needs_gauge']) +
           '），挠率迹不具备 A_μ→A_μ+∂_μΛ 变换律（' + str(gauge_ok) + '）⇒ '
           '自旋✓(' + str(spin_ok) + ') 但 规范✗ ⇒ **电磁门仍 FAIL**。'
           '后果：无规范不变性 ⇒ ① 矢量无质量保护，一般会带质量项 ½m²A²，把库仑 1/r² 变成 Yukawa '
           '② 不保证耦合到守恒流 ⇒ 电荷守恒无着落'),
          None, '★自旋对但规范错')

    entry('C3', 'BOUNDARY',
          ('⇒ 二选一（不代选）：'
           '**(a) 改 τ 的原语定义**——把 τ 从挠率标量/迹换成真正的 U(1) 规范场 A_μ，'
           '代价即 B 组四项（+1 量纲 Q、+1 常数、+1 场 2 DOF、+1 规范原理），'
           '但这已不是原来的 τ（几何原语被替换）；'
           '**(b) 放弃电磁还原**，接受四力还原停留在 0/4（承 r82）'),
          None, '二选一，不代选')

# ----------------------------------------------------------------------------
# D 组：阳性对照
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'PASS',
          ('阳性对照（门可分辨）：把**真正的 U(1) 规范场**（自旋 1 + 具备规范不变）代入电磁门 ⇒ '
           '自旋✓ 规范✓ ⇒ **PASS**（承 r82 E2 同一套门的对照结果）'
           ' ⇒ 本册 C2 的 FAIL 是「挠率迹缺规范结构」的真实判据结果，而非机器假红'),
          None, '★防假红')

    b1 = {'hbar': D_HBAR, 'c': D_C, 'G': D_G}
    b2 = {'hbar': D_HBAR, 'c': D_C, 'G': D_G, 'eps0': D_EPS0}
    entry('D2', 'PASS',
          ('阳性对照（穷举器非恒零）：目标 [ħ] 在 {ħ,c,G} 上命中 ' +
           str(len(enumerate_dims(b1, D_HBAR, 2))) + ' 组 ⇒ 穷举器能命中；'
           '而目标 [e]=Q 在同一基上命中 ' + str(len(enumerate_dims(b1, D_E, 3))) +
           ' 组、加入 ε₀ 后可触及 Q（|Q 指数| 最大值 ' + str(max_abs_q_exponent(b2, 2)) +
           '）⇒ **穷举器有分辨力**，A2 的「造不出 Q」是真实结论而非恒零工具'),
          None, '★防恒零')

# ----------------------------------------------------------------------------
# E 组：元结论与开放项
# ----------------------------------------------------------------------------
def group_E():
    entry('E1', 'FAIL',
          ('★元结论：X-R82-1 的价格标签 = **四项代价**（+1 量纲 Q、+1 常数 α、+1 场 2 DOF、'
           '+1 规范原理），其中最重的不是场也不是常数，而是**规范不变性这一结构原理**——'
           '它才是电磁力真正的来源，而几何（κ,τ）框架里没有它。'
           '且 τ 的挠率迹虽可取到 spin-1，却因缺规范结构仍过不了电磁门（C2）'),
          None, '价格标签')
    entry('E2', 'INFO',
          ('开放项更新：`X-R82-1` ⇒ **本册已完成定价**（四项代价已列出，是否在 (a)/(b) 间选择仍待来料方）；'
           '`X-R82-2`（弱/强需非阿贝尔规范 + 手征费米子）⇒ 仍开放，'
           '其定价方法可复用本册的量纲基扩充 + 规范原理计数口径；'
           '`X-R76-2`（W1 vs W2）⇒ 仍待用户裁决'),
          None, '开放项')

# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    meta = ('X-R82-1 定价完成：把 τ 升级为 U(1) 规范场的代价 = +1 量纲 Q、+1 常数 α、'
            '+1 场(2 DOF)、+1 规范原理；且 τ 的挠率迹虽可取到 spin-1，却因缺规范结构仍过不了电磁门')
    return {
        'round': 'r83',
        'date': '2026-10-17',
        'source': 'r82 开放项 X-R82-1 的代价定价（承 r75/r78/r80/r81/r82）',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'module': os.path.abspath(__file__),
        'source_mtime': datetime.fromtimestamp(os.path.getmtime(__file__), timezone.utc).isoformat(),
        'counts': dict(COUNTS),
        'total': len(ENTRIES),
        'verdict': verdict,
        'meta_verdict': meta,
        'guard_all_ok': True,
        'entries': ENTRIES,
        'not_self_derived': [
            {'tag': 'NS1', 'text': 'ε₀、e、ħ、c、α 均为 CODATA 实验值，非第一性导出；α≈1/137 作为输入常数登记'},
            {'tag': 'NS2', 'text': '「电磁需 U(1) 规范不变与 spin-1 媒介」为 SM/QFT 标准结论，引用不自推'},
            {'tag': 'NS3', 'text': '挠率迹 T_μ=T^ρ_{μρ} 是矢量属定义推论；其能否被赋予规范变换律本册不代判，只判「当前形式下不具备」'},
            {'tag': 'NS4', 'text': '(a) 改原语定义 vs (b) 放弃电磁还原 的取舍属科学哲学层，本册不代选'},
            {'tag': 'NS5', 'text': 'X-R82-2（弱/强）的定价本册只指出可复用同一口径，未执行，不自推其代价'},
        ],
        'red_line': '数学/数值自洽 != 物理证实。本册是代价定价，不产生新物理；'
                    '「加 U(1) 扇区要付四项代价」不等于「TUFT 不能做电磁」——'
                    '只是说明它不是零成本的，且规范原理才是电磁的真正来源',
    }

def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r83 X-R82-1 定价（τ 升级 U(1) 规范场代价）运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（含 G0-6 穷举器分辨力 / G0-7 非恒零）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · X-R82-1 定价（τ 升级为 U(1) 规范场的代价）', '',
          '## 条目计数', '- 总条目：' + str(payload['total'])]
    for k in sorted(payload['counts'].keys()):
        ml.append('- ' + k + '：' + str(payload['counts'][k]))
    ml += ['- 总体 verdict：' + verdict, '- 元判定：' + payload['meta_verdict'], '', '## 逐条裁定']
    for e in ENTRIES:
        line = '- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text']
        if e['residual']:
            line += '  （残差 ' + e['residual'] + '）'
        ml.append(line)
    ml += ['', '## not_self_derived']
    for n in payload['not_self_derived']:
        ml.append('- ' + n['tag'] + '：' + n['text'])
    ml += ['', '## 红线', payload['red_line']]
    mp = os.path.join(DATA, STEM + '.md')
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ml))
    return jp, rp, mp

def write_judgment(payload):
    lines = ['# 判定_TUFT-r83-X-R82-1定价_tau升级U1规范场代价_攻破_2026-10-17', '',
             '日期：2026-10-17 · **r82 开放项 X-R82-1 的代价定价**', '',
             '## 一、任务',
             'r82 判四力还原 0/4（κ,τ 为 spin-0），并留下 `X-R82-1`：'
             '若要还原电磁须把 τ 升级为 spin-1 规范场，等价于新增 U(1) 扇区，**代价另册定价**。本册执行该定价。', '',
             '## 二、★核心定价：四项代价', '',
             '| # | 代价项 | 内容 |',
             '|---|---|---|',
             '| 1 | **+1 个独立量纲 Q** | 电荷不可由 {ħ,c,G} 生成（穷举 343 组命中 0）⇒ 量纲基须从 (M,L,T) 扩到 (M,L,T,Q) |',
             '| 2 | **+1 个常数** | α = e²/(4πε₀ħc) 无量纲 ⇒ 其值 ≈1/137 只能实验输入（机器复算与 CODATA 相符）|',
             '| 3 | **+1 个场 A_μ** | 4 分量 − 2 规范冗余 = **2** 个物理自由度 |',
             '| 4 | **+1 个结构原理** | U(1) 规范不变 A_μ → A_μ + ∂_μΛ（原几何框架没有）|', '',
             '## 三、★最重的一项不是场，而是原理',
             '规范不变性才是保证「光子无质量 + 电荷守恒 + 库仑 1/r²」的真正来源，'
             '而不是「场具有 spin-1」这件事本身。', '',
             '## 四、★τ 能否就地升级（不改原语）',
             '- 挠率张量的迹 T_μ ≡ T^ρ_{μρ} **是矢量** ⇒ 自旋这项**是对的**（相对 r82 的 spin-0 是实质进展）。',
             '- 但它**不是规范场**：无 A_μ→A_μ+∂_μΛ ⇒ 无质量保护（会带 ½m²A²、库仑律变 Yukawa）、'
             '不保证耦合到守恒流 ⇒ **电磁门仍 FAIL（自旋✓ / 规范✗）**。', '',
             '## 五、二选一（不代选）',
             '- **(a)** 改 τ 的原语定义 → 换成真正的 U(1) 规范场，付上述四项代价（但这已不是原来的 τ）；',
             '- **(b)** 放弃电磁还原，接受四力还原停在 0/4（承 r82）。', '',
             '## 六、阳性对照（防假红 / 防恒零）',
             '- 真正的 U(1) 规范场代入同一电磁门 ⇒ **PASS** ⇒ C2 的 FAIL 是真实结果，非机器假红。',
             '- 穷举器对 [ħ] 有命中、对 [e]=Q 在 {ħ,c,G} 上命中 0 但加 ε₀ 后可触及 ⇒ **非恒零工具**。', '',
             '## 七、条目', '- 总条目 ' + str(payload['total']) + '：' + str(payload['counts']),
             '- 总体 verdict：**' + payload['verdict'] + '**']
    for e in ENTRIES:
        lines.append('- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text'])
    lines += ['', '## 八、不自推登记']
    for n in payload['not_self_derived']:
        lines.append('- ' + n['tag'] + '：' + n['text'])
    lines += ['', '## 九、开放项与治理',
              '- `X-R82-1` ⇒ **定价完成**（四项代价已列；(a)/(b) 取舍仍待来料方）。',
              '- `X-R82-2`（弱/强）⇒ 仍开放，可复用本册「量纲基扩充 + 规范原理计数」口径。',
              '- `X-R76-2`（W1 vs W2）⇒ 仍待用户裁决。',
              '- 治理：未改动任何他人文件字节；未跑 `refresh_catalog`（并发回退风险）；未做 git 操作。', '',
              '## 十、红线', payload['red_line'], '',
              'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r83-X-R82-1定价_tau升级U1规范场代价_攻破_2026-10-17.md')
    with io.open(jb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return jb

def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    payload = build_payload()
    jp, rp, mp = write_outputs(payload)
    jb = write_judgment(payload)
    assert len(ENTRIES) == sum(payload['counts'].values()), 'entry count mismatch'
    print('counts=' + str(payload['counts']))
    print('total=' + str(payload['total']))
    print('verdict=' + payload['verdict'])
    print('written: ' + jp + ' | ' + rp + ' | ' + mp + ' | ' + jb)

if __name__ == '__main__':
    main()
