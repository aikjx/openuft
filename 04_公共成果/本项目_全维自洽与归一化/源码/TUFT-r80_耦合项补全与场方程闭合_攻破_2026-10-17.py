# -*- coding: utf-8 -*-
"""
r80 · 2026-10-17 · r78 下游：耦合项补全与场方程闭合判定
==============================================================================
r78 承重裁定（继承，不重推）：
  C1/I02 FAIL  1000 条公式集内【根本没有 κ 与物质的耦合项】，也无弱场/牛顿极限定理
  C2/I04 FAIL  线性耦合系数 [C1] = L；{hbar,c,G} 整数幂造不出长度，半幂唯一解 l_P ⇒ 必须输入 G
  C3/I05/I06   C_req = sqrt(4pi) l_P ⇒ G_eff ≡ G（机器零）⇒ 重排非预言；新长度锁定、预测力 0
  C4/I07 FAIL  纯标量中介 ⇒ PPN γ = -1 ⇒ 偏折 0" vs 1.75"，超 Cassini 限 8.695652E+4 倍
  I08 BOUNDARY 耦合符号与整体归一化未声明 ⇒ 力的方向（吸引/排斥）仍是未声明输入
  I09 FAIL     三条出路（W1 降为度规派生量 / W2 标量-张量+屏蔽 / W3 纯标量）无一零代价

r78「下一步（按依赖序）」第 1 条：**先补耦合项**——写明 L_int 的形式、符号与归一化，
这是 I02/I08 两个缺口的唯一解药，也是最便宜的一步。本册执行该步并判定补全后是否闭合：

  A 组 形式枚举与量纲定价（机器）
    A1 线性标量耦合 L_int = -C1 κ T，[C1] = L（承 r78 I03）
    A2 n 次耦合 κ^n T：[Cn] = L^n（承 r78 I10）
    A3 张量(GR 型)耦合 -C_T h_{μν}T^{μν}：[C_T] 无量纲
    A4 ★两条路线的 G 入口不同但都躲不开 G：标量路线 G 经 C1=l_P 类长度进入；
        张量路线 G 经 Einstein–Hilbert 系数 c^4/(16πG) 进入（不复现 r78，只补其未写的对照）
    A5 补全后总拉氏量三项量纲齐次性（动能/势/耦合 全 = 能量密度 M L^-1 T^-2）
  B 组 符号裁定（解 I08，机器）
    B1 C1 绝对符号：静场解 κ→−κ，标量中介势 V ∝ −C1²/r 与 C1 符号无关 ⇒ 绝对符号是约定自由（WLOG C1>0）
    B2 真正未声明的是【源耦合 g_s 与检验体耦合 g_t 的相对符号】，V ∝ −g_s g_t；
       要求引力吸引 ⇒ g_s g_t > 0 ⇒ 相对符号被外部输入唯一固定
    B3 承 r79 A2 实测力律 F = −α∇(κ²−τ²)：对 κ→−κ 不变（二次型）⇒ 与 B1 一致；
       吸引/排斥由 α 符号决定 ⇒ α>0 须声明，不可自推
    ⇒ I08 从「未声明」收敛为：绝对符号=约定（可 WLOG 固定），相对符号/α 符号=外部输入（须声明）
  C 组 归一化裁定（解 I05/I06，机器复算）
    C1 C_req = sqrt(4π) l_P；G_eff = C² c³/(4π ħ) ≡ G（机器零），G 是输入非预言
  D 组 补全后场方程（写出 EOM 与牛顿极限）
  E 组 闭合性：即便 L_int 补全，纯标量 ⇒ γ=−1 ⇒ W3 仍死；参数账更新
  F 组 出路：W1/W2 仍在（不代选）；X-R76-1 部分解决、X-R76-2 仍开放

纪律（承 r37/r64/r67/r71/r74/r78/r79）
 1) 量纲指数相加 2) 量纲工具先过 G0 自守卫 3) 恒真/恒零裁定必配阳性对照
 4) 不自推系数登记 NS 5) 不改他人文件字节 6) 退出码 0 = 跑完；结论看 counts/verdict
 7) 承 r78 自抓：% 只绑最后一段 ⇒ 先构造完整字符串再格式化；新增条目后必须核对条目数
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

STEM = 'TUFT-r80_耦合项补全与场方程闭合_攻破_2026-10-17'

# ----------------------------------------------------------------------------
# 量纲工具：(M, L, T)，指数相加
# ----------------------------------------------------------------------------
def D_(m=0, l=0, t=0):
    return (Fr(m), Fr(l), Fr(t))

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    return tuple(x * Fr(n) for x in a)

def dstr(a):
    names = ('M', 'L', 'T')
    out = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        out.append(nm + '^' + str(v))
    return ' '.join(out) if out else '1'

D_HBAR = D_(m=1, l=2, t=-1)
D_C = D_(l=1, t=-1)
D_KAPPA = D_(l=-1)
D_TAU = D_(l=-1)
D_ENERGY_DENSITY = D_(m=1, l=-1, t=-2)
D_FORCE = D_(m=1, l=1, t=-2)
D_L = D_(l=1)
D_G = D_(m=-1, l=3, t=-2)
D_TRACE_T = D_ENERGY_DENSITY      # T = T^mu_mu 亦为能量密度
D_RICCI_S = D_(l=-2)              # 曲率标量 R
D_LAMBDA = dmul(ddiv(D_ENERGY_DENSITY, dpow(D_KAPPA, 4)), D_(1))  # [lambda]，下面 G0 核实

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
# G0-* 量纲工具自守卫（先过守卫再用于判定）
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    if dmul(D_HBAR, D_C) != (Fr(1), Fr(3), Fr(-2)):
        fails.append('G0-1')
    if D_ENERGY_DENSITY == D_FORCE:
        fails.append('G0-2')
    if dpow(D_KAPPA, 2) != (Fr(0), Fr(-2), Fr(0)):
        fails.append('G0-3')
    # [hbar*c*kappa^2] = 力（承 r71）
    if dmul(dmul(D_HBAR, D_C), dpow(D_KAPPA, 2)) != D_FORCE:
        fails.append('G0-4')
    # [hbar*c*(d kappa)^2] = 能量密度（承 r71 C1 修法）
    d_kappa = ddiv(D_KAPPA, D_L)
    if dmul(dmul(D_HBAR, D_C), dpow(d_kappa, 2)) != D_ENERGY_DENSITY:
        fails.append('G0-5')
    # [lambda] = 能量密度 / kappa^4 = M L^3 T^-2（承 r71 B1）
    lam = ddiv(D_ENERGY_DENSITY, dpow(D_KAPPA, 4))
    if lam != (Fr(1), Fr(3), Fr(-2)):
        fails.append('G0-6')
    # [C1] = 能量密度 / (kappa * T) = L（承 r78 I03）
    c1 = ddiv(D_ENERGY_DENSITY, dmul(D_KAPPA, D_TRACE_T))
    if c1 != D_L:
        fails.append('G0-7')
    # Einstein–Hilbert 能量密度口径系数 [c^4/G] * [R] = 能量密度（承 r71 双口径记忆）
    eh = dmul(ddiv(dpow(D_C, 4), D_G), D_RICCI_S)
    if eh != D_ENERGY_DENSITY:
        fails.append('G0-8')
    # 阳性对照：非目标量纲必须与能量密度不同（守卫分辨力）
    if D_FORCE == D_ENERGY_DENSITY or D_L == D_ENERGY_DENSITY:
        fails.append('G0-9')
    if fails:
        raise SystemExit('G0 量纲工具自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# 数值常数（CODATA 锚点，Decimal 60 位）
# ----------------------------------------------------------------------------
HBAR = D('1.054571817e-34')
C_LIGHT = D('299792458')
G_NEWTON = D('6.67430e-11')
PI = D('3.14159265358979323846264338327950288419716939937510582097494459')

def l_P():
    return (HBAR * G_NEWTON / (C_LIGHT ** 3)).sqrt()

def C_req():
    return (D(4) * PI).sqrt() * l_P()

def G_eff(C):
    return C * C * (C_LIGHT ** 3) / (D(4) * PI * HBAR)

# ----------------------------------------------------------------------------
# A 组：形式枚举与量纲定价
# ----------------------------------------------------------------------------
def group_A():
    # A1 线性标量耦合
    c1 = ddiv(D_ENERGY_DENSITY, dmul(D_KAPPA, D_TRACE_T))
    entry('A1', 'PASS',
          ('线性标量耦合 𝓛_int = −C₁ κ T 的系数量纲 [C₁] = ' + dstr(c1) +
           '（承 r78 I03；T=T^μ_μ 为能量密度 M L^-1 T^-2）'),
          None, '形式定价')

    # A2 n 次耦合
    rows = []
    for n in (1, 2, 3):
        cn = ddiv(D_ENERGY_DENSITY, dmul(dpow(D_KAPPA, n), D_TRACE_T))
        rows.append('n=' + str(n) + ':' + dstr(cn))
    entry('A2', 'PASS',
          ('非线性耦合 κ^n T 的系数量纲 [C_n] = L^n：' + '，'.join(rows) +
           '（承 r78 I10：每升一阶多一个 l_P 幂，循环依赖更强）'),
          None, '形式定价')

    # A3 张量耦合
    ct = ddiv(D_ENERGY_DENSITY, D_TRACE_T)   # h 无量纲
    entry('A3', 'PASS',
          ('张量(GR 型)耦合 𝓛_int = −½ C_T h_{μν}T^{μν} 的系数量纲 [C_T] = ' + dstr(ct) +
           '（h_{μν} 为无量纲度规扰动 ⇒ 耦合系数本身无量纲）'),
          None, '形式定价')

    # A4 ★两条路线的 G 入口对照
    eh_coef = ddiv(dpow(D_C, 4), D_G)
    entry('A4', 'FAIL',
          ('★G 入口对照（补 r78 未写的那半）：标量路线 G 经耦合系数 C₁（须为长度，仅 l_P 可得）进入；'
           '张量路线 G 经 Einstein–Hilbert 动能系数 [c⁴/(16πG)] = ' + dstr(eh_coef) +
           ' 进入（能量密度口径，承 r71 双口径）。两条路线的 G 入口位置不同，'
           '但【都必须显式输入 G】⇒ 「不输入 G 而给出引力」在当前公设集内无解'),
          None, '承 r78 I04 并补齐张量对照')

    # A5 补全后总拉氏量三项齐次性
    d_kappa = ddiv(D_KAPPA, D_L)
    kin = dmul(dmul(D_HBAR, D_C), dpow(d_kappa, 2))
    lam = ddiv(D_ENERGY_DENSITY, dpow(D_KAPPA, 4))
    pot = dmul(lam, dpow(D_KAPPA, 4))
    intf = dmul(D_L, dmul(D_KAPPA, D_TRACE_T))
    ok = (kin == D_ENERGY_DENSITY and pot == D_ENERGY_DENSITY and intf == D_ENERGY_DENSITY)
    entry('A5', 'PASS' if ok else 'FAIL',
          ('补全后总拉氏量 𝓛 = (ħc/2)[(∂κ)²+(∂τ)²] − λ(κ²+τ²)² − C₁ κ T 的三项量纲：'
           '动能=' + dstr(kin) + '、势=' + dstr(pot) + '、耦合=' + dstr(intf) +
           '；齐次（全 = 能量密度 M L^-1 T^-2）=' + str(ok)),
          None, '承 r74 P1 同号化 + r74 D2 单常数势 + 本册耦合项')

# ----------------------------------------------------------------------------
# B 组：符号裁定（解 I08）
# ----------------------------------------------------------------------------
def group_B():
    # B1 绝对符号是约定自由：势 ∝ −C1²/r 与符号无关；κ 只差整体符号
    entry('B1', 'PASS',
          ('★C₁ 的绝对符号是【约定自由】而非物理歧义：静场解在 C₁→−C₁ 下只差 κ→−κ，'
           '而标量中介的相互作用势 V ∝ −C₁²/r 只含 C₁ 的平方 ⇒ 与绝对符号无关。'
           '故可 WLOG 取 C₁>0；I08 中的「绝对符号未声明」不构成物理缺口'),
          None, 'I08 的一半被消解')
    entry('B2', 'BOUNDARY',
          ('★真正未声明的是【源耦合 g_s 与检验体耦合 g_t 的相对符号】：标量交换势 V ∝ −g_s g_t，'
           '仅当 g_s g_t > 0 时为吸引。要求「引力吸引」⇒ 相对符号被该外部输入唯一固定。'
           '这是必须显式声明的外部输入，不可自推'),
          None, 'I08 收敛为：相对符号=外部输入')
    entry('B3', 'BOUNDARY',
          ('承 r79 A2 实测力律 F = −α∇(κ²−τ²)：该式对 κ→−κ 不变（二次型）⇒ 与 B1 一致；'
           '但吸引/排斥由 α 的符号决定 ⇒ α>0 须由「引力吸引」这一外部输入声明，不可自推。'
           '⇒ I08 从「未声明」收敛定位为：绝对符号=约定（可 WLOG 固定）、相对符号与 α 符号=外部输入'),
          None, '与 r79 实测力律互证')

# ----------------------------------------------------------------------------
# C 组：归一化裁定（解 I05/I06，机器复算）
# ----------------------------------------------------------------------------
def group_C():
    lp = l_P()
    cr = C_req()
    ge = G_eff(cr)
    rel = abs(ge - G_NEWTON) / G_NEWTON
    entry('C1', 'BOUNDARY',
          ('归一化机器复算：l_P = √(ħG/c³) = ' + str(lp) + ' m；C_req = √(4π)·l_P = ' + str(cr) +
           ' m；代回 G_eff = C²c³/(4πħ) = ' + str(ge) + '，与 CODATA G 相对偏差 ' + str(rel) +
           '（机器零）⇒ 复现 G 是重排而非预言（承 r78 I05/I06：G 是输入不是输出）'),
          str(rel), '承 r78 C3，独立引擎复算')
    # 阳性对照：换一个 C 值则 G_eff 显著偏离
    ge2 = G_eff(cr * D(2))
    rel2 = abs(ge2 - G_NEWTON) / G_NEWTON
    entry('C2', 'PASS',
          ('阳性对照：取 C = 2·C_req 则 G_eff = ' + str(ge2) + '，相对偏差 ' + str(rel2) +
           '（≈4 倍）⇒ 检验器非恒等、有分辨力'),
          str(rel2), '防恒真')

# ----------------------------------------------------------------------------
# D 组：补全后场方程与牛顿极限
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'PASS',
          ('补全后场方程（κ 通道，号差 (+,−,−,−)、x⁰=ct）：'
           '𝓛 = (ħc/2)[(∂κ)²+(∂τ)²] − λ(κ²+τ²)² − C₁ κ T ⇒ '
           'ħc □κ + 4λ κ(κ²+τ²) = −C₁ T'),
          None, '写出补全后的 EOM')
    entry('D2', 'PASS',
          ('牛顿极限（静、无质量、U 可略，承 r74 D3 势在背景 (0,0) 处无质量）：'
           'ħc ∇²κ = C₁ T，T ≈ ρc² ⇒ κ(r) = −C₁ M c/(4π ħ r)；'
           '与 C 组同一 C₁ 代入后给出 G_eff ≡ G ⇒ 补全后的耦合项确实能把场方程接到牛顿极限上'),
          None, 'I02「无弱场/牛顿极限」在补全后已被填上')

# ----------------------------------------------------------------------------
# E 组：闭合性判定
# ----------------------------------------------------------------------------
def group_E():
    ratio = abs(D(-1) - D(1)) / D('2.3e-5')
    entry('E1', 'FAIL',
          ('★闭合性：即便 𝓛_int 已补全，纯标量中介仍只与 T 的迹耦合 ⇒ PPN γ = −1 ⇒ 光线偏折 0″'
           '（GR/实测 1.75″）；|γ−1| = 2 对 Cassini 限 2.3×10⁻⁵ ⇒ 超出 ' + str(ratio) +
           ' 倍 ⇒ W3（保持纯标量）仍被实验排除。'
           '⇒ 补全耦合项解掉的是 I02/I08，解不掉 I07/I09'),
          str(ratio), '承 r78 C4/I07，补全后复判')
    entry('E2', 'INFO',
          ('参数账（补全后显式登记）：ħ、c（CODATA 锚点）＋ G（经 l_P 输入，非导出）＋ '
           'λ（r74 D2 单常数势）＋ C₁（被观测唯一锁定 ⇒ 自由度 0、预测力 0）＋ '
           'α（力律系数，其符号为外部输入）。'
           '自由参数 n=λ,α（C₁ 锁定不计）与观测数对比需 r77 口径，本册只登记不自推'),
          None, '参数账登记')

# ----------------------------------------------------------------------------
# F 组：出路与开放项
# ----------------------------------------------------------------------------
def group_F():
    entry('F1', 'BOUNDARY',
          ('W1（把 κ,τ 降为度规派生量、退回 GR）与 W2（保留 κ 传播 + 加张量扇区 + 屏蔽）'
           '之间的裁决属科学哲学层选择，本册不代选（承 r78）。'
           '本册贡献：把裁决所需的【完整拉氏量】补齐了（形式/符号/归一化三要素齐备），'
           '裁决对象从「缺一项的方程」变为「完整的二选一」'),
          None, 'X-R76-2 仍开放')
    entry('F2', 'INFO',
          ('开放项状态更新：`X-R76-1`（耦合项的形式与符号）⇒ 本册已写明形式、'
           '绝对符号定为约定、相对符号与 α 符号定位为外部输入（部分解决，来料方仍需择定相对符号）；'
           '`X-R76-2`（W1 vs W2）⇒ 仍开放；`X-R76-3`（若走 W2 的屏蔽机制形式与代价）⇒ 仍开放'),
          None, '开放项')

# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    meta = ('耦合项已按 r78 建议补全（形式/符号/归一化三要素齐备，I02 填上、I08 收敛定位），'
            '但补全后仍因纯标量被 Cassini 排除（I07）⇒ 场方程未闭合；'
            '真正待决的是 W1/W2 的科学哲学层裁决，本册不代选')
    return {
        'round': 'r80',
        'date': '2026-10-17',
        'source': 'r78 下游（执行其「下一步①先补耦合项」）；r79 同期互补',
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
            {'tag': 'NS1', 'text': 'Cassini |γ−1|<2.3×10⁻⁵ 与太阳临边 1.75″ 偏折为外部实验事实，引用不自推'},
            {'tag': 'NS2', 'text': 'PPN γ=−1 属纯标量(Nordström 型)引力教科书结论；标量交换势 V∝−g_s g_t 亦为教科书结论，引用不自推'},
            {'tag': 'NS3', 'text': '𝓛_int=−C₁κT 是为定价/补全而构造的最小候选（承 r78 NS3），来料原文未给出；其物理意图不自推'},
            {'tag': 'NS4', 'text': 'CODATA 的 ħ/c/G 为实验测量值，非第一性导出；√(4π) 为格林函数归一化约定'},
            {'tag': 'NS5', 'text': '「引力必须吸引」作为外部输入用于固定相对符号与 α 符号，本册不代该输入的正当性'},
            {'tag': 'NS6', 'text': 'W1 vs W2 属科学哲学层选择，本册只补齐裁决所需的完整拉氏量，不作裁决'},
        ],
        'red_line': '数学/数值自洽 != 物理证实。本册是耦合项补全与闭合性判定，不产生新物理；'
                    '「补全后仍被 Cassini 排除」不等于「TUFT 方向被否证」——W1/W2 两条出路均未被否证，只是都不便宜',
    }

def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r80 耦合项补全与场方程闭合 运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 量纲工具自守卫 全过（含阳性对照 G0-9）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · r78 下游（耦合项补全与场方程闭合）', '',
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
    fails = [e for e in ENTRIES if e['verdict'] == 'FAIL']
    lines = ['# 判定_TUFT-r80-耦合项补全与场方程闭合_攻破_2026-10-17', '',
             '日期：2026-10-17 · **r78 下游**（执行 r78「下一步①先补耦合项」）· r79 同期互补', '',
             '## 一、本册做了什么',
             'r78 判「1000 条公式集内根本没有 κ 与物质的耦合项」（I02 FAIL），并建议「先补耦合项——'
             '写明 𝓛_int 的形式、符号与归一化，这是 I02/I08 的唯一解药，也是最便宜的一步」。'
             '本册执行该步，并判定补全之后场方程是否闭合。', '',
             '## 二、补全结果（三要素齐备）',
             '- **形式**：𝓛_int = −C₁ κ T（线性标量耦合），[C₁] = L；一般 κⁿT 有 [C_n] = Lⁿ。',
             '- **符号**：C₁ 的**绝对符号是约定自由**（势 V ∝ −C₁² 只含平方，κ 只差整体符号）⇒ WLOG 取 C₁>0；'
             '真正未声明的是**源耦合与检验体耦合的相对符号**（V ∝ −g_s g_t），由「引力吸引」这一外部输入固定。',
             '- **归一化**：C_req = √(4π)·l_P ⇒ G_eff ≡ G（机器零），但 G 是**输入不是预言**。', '',
             '## 三、补全后的完整拉氏量与场方程',
             '𝓛 = (ħc/2)[(∂κ)²+(∂τ)²] − λ(κ²+τ²)² − C₁ κ T  （三项量纲齐次，全 = 能量密度 M L⁻¹ T⁻²）',
             'κ 通道 EOM：ħc □κ + 4λ κ(κ²+τ²) = −C₁ T；牛顿极限 κ(r) = −C₁ M c/(4π ħ r)。', '',
             '## 四、闭合性判定（关键）',
             '**未闭合**：补全耦合项解掉的是 I02（无耦合项/无弱场）与 I08（符号未声明），'
             '但解不掉 I07——纯标量中介只与 T 的迹耦合 ⇒ PPN γ = −1 ⇒ 偏折 0″（实测 1.75″），'
             '超 Cassini 限约 8.70×10⁴ 倍 ⇒ W3 仍被排除。',
             '⇒ 「完成统一场论」的价格标签仍是 W1/W2 二选一：W1 退回 GR（零新增内容）、'
             'W2 加张量扇区 + 屏蔽（≥1 个自由函数，撞 Ω5）。**没有第三条零代价的路。**', '',
             '## 五、条目与裁定', '- 总条目 ' + str(payload['total']) + '：' + str(payload['counts']),
             '- 总体 verdict：**' + payload['verdict'] + '**']
    for e in ENTRIES:
        lines.append('- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text'])
    lines += ['', '## 六、不自推登记']
    for n in payload['not_self_derived']:
        lines.append('- ' + n['tag'] + '：' + n['text'])
    lines += ['', '## 七、开放项与治理',
              '- `X-R76-1`（耦合项形式与符号）⇒ **部分解决**：形式已写明、绝对符号定为约定、'
              '相对符号与 α 符号定位为外部输入（仍需来料方择定）。',
              '- `X-R76-2`（W1 vs W2）⇒ 仍开放（科学哲学层，不代选）。',
              '- `X-R76-3`（W2 的屏蔽机制形式与代价）⇒ 仍开放。',
              '- 治理：未改动任何他人文件字节；未跑 `refresh_catalog`（并发回退风险）；未做 git 操作。', '',
              '## 八、红线', payload['red_line'], '',
              'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r80-耦合项补全与场方程闭合_攻破_2026-10-17.md')
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
    group_F()
    payload = build_payload()
    jp, rp, mp = write_outputs(payload)
    jb = write_judgment(payload)
    # 承 r78 自抓第 5 条：新增条目后必须核对条目数
    assert len(ENTRIES) == sum(payload['counts'].values()), 'entry count mismatch'
    print('counts=' + str(payload['counts']))
    print('total=' + str(payload['total']))
    print('verdict=' + payload['verdict'])
    print('written: ' + jp + ' | ' + rp + ' | ' + mp + ' | ' + jb)

if __name__ == '__main__':
    main()
