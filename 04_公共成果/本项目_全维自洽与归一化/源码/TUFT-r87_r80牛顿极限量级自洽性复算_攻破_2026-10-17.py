# -*- coding: utf-8 -*-
"""
r87 · 2026-10-17 · r80 下游攻破（跨会话一致性复算）
《r80 牛顿极限的量级自洽性复算：κ 不是曲率（1.7e34 倍差）+ 线性化要求 λ ≤ 3.6e-101 的荒谬精细调节》
==============================================================================
编号仲裁（起草前实测磁盘）：源码已占 31..86（并行会话同日推进 r80→r86 一整条定价链：
  耦合项补全 → W1/W2 定价 → 四力还原通道 → τ→U(1) → 弱强非阿贝尔 → 五门判定 → chameleon/Vainshtein 屏蔽）
=> 取首空号 r87（后到者改号，不覆盖他人任何文件字节）

动机（跨会话一致性检查，零重复）：
  我的链：r69 审计 → r71 补导数项 → r74 同号化消 τ 鬼场 → r77 齐次性定理 → r79 来料层差/tachyon
  并行链：r78 耦合门票 → r80 补 𝓛_int=−C₁κT 并称「场方程闭合、接到牛顿极限」→ r81–r86 定价 W1/W2
  —— **两链从未交叉**。r80 D2 的关键断言「牛顿极限：ħc∇²κ=C₁T，U 可略 ⇒ 接到牛顿引力」
     从未被人做过【量级自洽性】复算。本册补上，发现两个全新问题。

r80 已确认成立、本册不复算的部分（承 r80）：
  C1: C₁=√(4π)·ℓ_P ⇒ G_eff=C₁²c³/(4πħ)=G（重排非预言）
  D1: 场方程 ħc□κ+4λκ(κ²+τ²)=−C₁T
  E1: 纯标量 PPN γ=−1 ⇒ Cassini 排除 86956 倍

本册四组：
  组 A  独立复算牛顿解：κ(r)=−C₁Mc/(4πħr)，并核对 Φ_TUFT=C₁c²κ ≡ GM/r（G 复现）
  组 B  ★量级对照：κ 比真实时空曲率大 ~1.75e34 倍 ⇒ 「κ=曲率」的几何识别是装饰性的
  组 C  ★线性化自洽性：r80 D2 的「U 可略」只在 λ ≤ 3.57e-101（SI）时成立 ⇒ 100 位小数精细调节
  组 D  对 r80 的更正 + 与既有 dex 缺口登记的衔接 + 红线

纪律：纯标准库 Decimal 60 + Fraction 四元组量纲；所有「可忽略/=零/复现」结论配阳性对照；
      跨册读数机器回读他人产物（r80 JSON）。
"""

import io
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '源码')
DATA = os.path.join(ROOT, '数据')
STEM = 'TUFT-r87_r80牛顿极限量级自洽性复算_攻破_2026-10-17'
SRC_NAME = STEM + '.py'

R80_JSON = os.path.join(DATA, 'TUFT-r80_耦合项补全与场方程闭合_攻破_2026-10-17.json')

ENTRIES = []
COUNTS = {}
GUARDS = []


def entry(tag, verdict, text, residual=None, note=''):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': residual, 'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    if not ok:
        raise AssertionError('GUARD FAILED: ' + name + ' | ' + detail)



# ----------------------------------------------------------------------------
# 常量（CODATA 锚点，承 r80/r78，不自推其数值来源）
# ----------------------------------------------------------------------------
HBAR = Decimal('1.054571817e-34')          # M L^2 T^-1
C_LIGHT = Decimal('2.99792458e8')          # L T^-1
G_NEWT = Decimal('6.67430e-11')            # M^-1 L^3 T^-2
M_SUN = Decimal('1.98892e30')              # M
R_AU = Decimal('1.495978707e11')           # L

# 四元组量纲（自检用）
def D(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = Fr(n)
    return tuple(x * n for x in a)


def dstr(a):
    out = []
    for sym, x in zip(('M', 'L', 'T', 'Q'), a):
        if x == 0:
            continue
        out.append(sym + '^' + str(x))
    return ' '.join(out) if out else '1'


def G0_guards():
    guard('G0-1', os.path.exists(R80_JSON), 'r80 产物回链存在（跨册机器回读）')
    guard('G0-2', dmul(D(1, 2, -1, 0), D(0, 1, -1, 0)) == D(1, 3, -2, 0),
          '[hbar*c] = ' + dstr(dmul(D(1, 2, -1, 0), D(0, 1, -1, 0))))
    guard('G0-3', dmul(D(0, 1, -1, 0), dpow(D(0, 1, -1, 0), 2)) == D(0, 3, -3, 0),
          'c^3 量纲')
    # [l_P^2] = L^2：机器复核（承 r80 G0-7）
    d_lp2 = dmul(dmul(D(-1, 3, -2, 0), D(1, 2, -1, 0)), dpow(D(0, 1, -1, 0), -3))
    guard('G0-4', d_lp2 == D(0, 2, 0, 0), '[G hbar / c^3] = ' + dstr(d_lp2) + ' 应为 L^2')
    # [C1] = L ⇒ [C1 kappa T] 应为能量密度
    d_C1 = D(0, 1, 0, 0)
    d_kap = D(0, -1, 0, 0)
    d_T = D(1, -1, -2, 0)
    guard('G0-5', dmul(dmul(d_C1, d_kap), d_T) == D(1, -1, -2, 0),
          '[C1*kappa*T] = 能量密度')
    # [lambda] = M L^3 T^-2（承 r77 B1：四次势系数）
    d_lam = D(1, 3, -2, 0)
    d_k4 = dpow(d_kap, 4)
    guard('G0-6', dmul(d_lam, d_k4) == D(1, -1, -2, 0),
          '[lambda*kappa^4] = 能量密度')



PI = Decimal(repr(math.pi))
L_P = (HBAR * G_NEWT / (C_LIGHT ** 3)).sqrt()
C1 = (Decimal(4) * PI).sqrt() * L_P


# ----------------------------------------------------------------------------
# 组 A：独立复算 r80 的牛顿解
# ----------------------------------------------------------------------------
def group_A():
    # A1 κ(r) = -C1 M c /(4π ħ r)
    kap = -(C1 * M_SUN * C_LIGHT) / (Decimal(4) * PI * HBAR * R_AU)
    entry('A1', 'PASS',
          ('★独立复算 r80 D2 牛顿解（太阳 M=' + format(M_SUN, '.4E') +
           ' kg，r=1 AU=' + format(R_AU, '.4E') + ' m）：'
           'κ(r) = −C₁Mc/(4πħr) = ' + format(kap, '.6E') + ' m^-1'
           '（C₁=√(4π)·ℓ_P=' + format(C1, '.6E') + ' m，ℓ_P=' + format(L_P, '.6E') + ' m）'),
          format(kap, '.6E'), '牛顿解')

    # A2 核对 Φ_TUFT = C1 c^2 κ ≡ GM/r（G 复现）
    phi_tuft = C1 * C_LIGHT * C_LIGHT * abs(kap)
    phi_newt = G_NEWT * M_SUN / R_AU
    rel = abs(phi_tuft - phi_newt) / phi_newt
    ok = rel < Decimal('1e-40')
    entry('A2', 'PASS' if ok else 'FAIL',
          ('核对 r80 的 G 复现：Φ_TUFT = C₁c²|κ| = ' + format(phi_tuft, '.6E') +
           '，GM/r = ' + format(phi_newt, '.6E') +
           '，相对偏差 ' + format(rel, '.6E') + '（机器零）'
           '⇒ **r80 D2 的「接到牛顿引力」在数值上确实成立**'
           '（= C₁²c³/(4πħ)≡G 的重排，承 r80 C1 非预言）'),
          format(rel, '.6E'), 'G 复现')

    # A3 阳性对照：C1 -> 2*C1 应给 4G（检验器非恒等）
    kap2 = -(Decimal(2) * C1 * M_SUN * C_LIGHT) / (Decimal(4) * PI * HBAR * R_AU)
    phi2 = Decimal(2) * C1 * C_LIGHT * C_LIGHT * abs(kap2)
    rel2 = abs(phi2 - phi_newt) / phi_newt
    entry('A3', 'PASS' if abs(rel2 - Decimal(3)) < Decimal('1e-30') else 'FAIL',
          ('阳性对照：C₁→2C₁ 时 Φ = ' + format(phi2, '.6E') +
           '，与 GM/r 相对偏差 ' + format(rel2, '.6E') + '（=3，即 4 倍）'
           '⇒ 检验器非恒等、有分辨力（与 r80 C2 一致）'),
          format(rel2, '.6E'), '阳性对照')



# ----------------------------------------------------------------------------
# 组 B：★量级对照 —— κ 不是时空曲率
# ----------------------------------------------------------------------------
def group_B():
    kap = -(C1 * M_SUN * C_LIGHT) / (Decimal(4) * PI * HBAR * R_AU)
    # B1 真实时空曲率（施瓦西外径向 Kretschmann 类标量的平方根尺度）
    kap_phys = G_NEWT * M_SUN / (C_LIGHT * C_LIGHT * R_AU)
    entry('B1', 'PASS',
          ('真实时空曲率尺度（施瓦西，太阳 1 AU）：κ_phys = GM/(c²r) = '
           + format(kap_phys, '.6E') + ' m^-1'
           '（这是 TUFT 声称 κ 所代表的「时空曲率」的量级）'),
          format(kap_phys, '.6E'), '真实曲率')

    # B2 比值
    ratio = abs(kap) / kap_phys
    entry('B2', 'FAIL',
          ('★量级对照：|κ_TUFT| / κ_phys = ' + format(kap, '.6E') + ' / '
           + format(kap_phys, '.6E') + ' = **' + format(ratio, '.6E') + ' 倍**'
           '⇒ 能复现牛顿引力的 κ 场，比它声称代表的时空曲率**大 34 个数量级**'
           '⇒ 「κ = 时空曲率」的几何识别在数值上是**装饰性**的：'
           'κ 是一个以 ℓ_P 归一化的标量代理，不是曲率本身'),
          format(ratio, '.6E'), '★dex 差')

    # B3 与 Planck 尺度对照（解释为何差 34 dex：C1 ∝ ℓ_P）
    inv_lp = Decimal(1) / L_P
    frac = abs(kap) / inv_lp
    entry('B3', 'INFO',
          ('根因解释：κ/ℓ_P⁻¹ = ' + format(frac, '.6E') +
           ' ⇒ κ 落在普朗克尺度附近（因 C₁=√(4π)ℓ_P ∝ ℓ_P）'
           '；而真实曲率被 G 压到 ' + format(kap_phys, '.6E') +
           ' m^-1。两者相差的正是 ℓ_P 与 GM/(c²r) 的尺度差 '
           '⇒ 34 dex 缺口不是计算误差，是**归一化选择的直接后果**'),
          format(frac, '.6E'), '根因')


# ----------------------------------------------------------------------------
# 组 C：★线性化自洽性 —— r80 D2 的「U 可略」要求 λ ≤ 3.6e-101
# ----------------------------------------------------------------------------
def group_C():
    kap = -(C1 * M_SUN * C_LIGHT) / (Decimal(4) * PI * HBAR * R_AU)
    # C1 线性项（源项）量级
    rho = M_SUN / (Decimal(4) / Decimal(3) * PI * R_AU ** 3)
    lin = C1 * rho * C_LIGHT * C_LIGHT
    entry('C1', 'PASS',
          ('线性项（源项）量级：|C₁T| ≈ C₁ρc² = ' + format(lin, '.6E') +
           '（ρ=太阳质量均摊于 1 AU 球壳 = ' + format(rho, '.6E') + ' kg/m³）'),
          format(lin, '.6E'), '线性项')

    # C2 λ 临界值（令非线性 = 线性）
    lam_crit = Decimal(12) * PI ** 2 * HBAR ** 3 / (C1 ** 2 * M_SUN ** 2 * C_LIGHT)
    entry('C2', 'FAIL',
          ('★线性化临界常数：令非线性项 4λκ³ = 线性项 C₁ρc²，解得 '
           'λ_crit = 12π²ħ³/(C₁²M²c) = **' + format(lam_crit, '.6E') +
           '（SI，[λ]=M L³T⁻²）**'
           '⇒ r80 D2 的「势能可略」只有在 **λ ≤ ' + format(lam_crit, '.3E') +
           '** 时才成立'),
          format(lam_crit, '.6E'), '★λ 临界')

    # C3 自洽核对：在 λ_crit 处非线性项应精确等于线性项
    nonlin = Decimal(4) * lam_crit * abs(kap) ** 3
    rel = abs(nonlin - lin) / lin
    entry('C3', 'PASS' if rel < Decimal('1e-40') else 'FAIL',
          ('自洽核对：λ=λ_crit 时非线性项 4λκ³ = ' + format(nonlin, '.6E') +
           '，线性项 = ' + format(lin, '.6E') + '，相对差 ' + format(rel, '.6E')
           + '（机器零）⇒ λ_crit 推导自洽'),
          format(rel, '.6E'), '自洽核对')

    # C4 λ_crit 的自然单位表述
    hc = HBAR * C_LIGHT
    frac = lam_crit / hc
    entry('C4', 'FAIL',
          ('★精细调节度量：λ_crit /(ħc) = ' + format(frac, '.6E') +
           '（ħc=' + format(hc, '.6E') + '）'
           '⇒ 要把牛顿极限保住，四次势系数必须被调到 ħc 的约 '
           + format(frac, '.2E') + ' 倍'
           '⇒ 这是一项 **约 75 个数量级的荒谬精细调节**，且必须对每个质量源分别成立'
           '（λ_crit ∝ 1/M²，M 换成地球/星系则更苛刻）'),
          format(frac, '.6E'), '★精细调节')

    # C5 阳性对照：λ = ħc（自然取值）时线性化灾难性失效
    lam_nat = hc
    ratio_nat = lam_nat / lam_crit
    entry('C5', 'PASS',
          ('阳性对照：若取「自然」量级 λ = ħc = ' + format(hc, '.6E') +
           '，则非线性/线性 = λ/λ_crit = **' + format(ratio_nat, '.6E') +
           '** ⇒ 线性化灾难性失效，r80 D2 的牛顿解完全不成立'
           '⇒ 检验器非恒零，「U 可略」是真问题不是仪器故障'),
          format(ratio_nat, '.6E'), '阳性对照')

    # C6 承重结论
    entry('C6', 'FAIL',
          ('★承重结论：r80 D2 断言「U 可略 ⇒ 场方程接到牛顿极限」'
           '**只在 λ ≤ ' + format(lam_crit, '.3E') + ' 时成立**，'
           '即要求一项约 75 dex 的外部精细调节；'
           '任何「自然」的 λ 都使四次项主导、牛顿解失效。'
           '⇒ r80 的「场方程闭合」是**条件性闭合**，条件是凭空多出来的一次精细调节'
           '（按 Ω5 / r15 口径 II 记账，这等价于 +1 个外部输入）'),
          None, '★承重')


# ----------------------------------------------------------------------------
# 组 D：对 r80 的更正 + 与既有 dex 缺口登记的衔接
# ----------------------------------------------------------------------------
def group_D():
    with io.open(R80_JSON, 'r', encoding='utf-8') as f:
        r80 = json.load(f)
    d2 = None
    e1 = None
    for e in r80['entries']:
        if e.get('tag') == 'D2':
            d2 = e
        if e.get('tag') == 'E1':
            e1 = e
    r80_verdict = r80.get('verdict')
    entry('D1', 'PASS',
          ('跨册机器回读 r80 JSON：r80 verdict=' + str(r80_verdict) +
           '，D2（牛顿极限）verdict=' + str(d2['verdict'] if d2 else None) +
           '，E1（Cassini 排除）verdict=' + str(e1['verdict'] if e1 else None) +
           ' ⇒ 本册不推翻 r80 的 FAIL 总判，只对其 D2 的**表述**作更正（见 D3）'),
          str(r80_verdict), '回链')

    entry('D2', 'INFO',
          ('与既有登记的衔接：34 dex 缺口（B2）与 r15/r17 已登记的'
           '「四力耦合跨 33 dex 对齐问题」是同一现象的两个面'
           '（耦合常数侧 vs 场量级侧）。**本册新增**的是把它钉到 r80 的牛顿解上：'
           '给出 κ_TUFT/κ_phys = 1.745361E+34 与 λ_crit = 3.567997E-101 两个可复算数字'),
          None, '衔接')

    entry('D3', 'BOUNDARY',
          ('★对 r80 D2 的更正（不推翻其 FAIL）：r80 原文「耦合项确实能把场方程接到牛顿极限上」'
           '应更正如：「**在 λ ≤ 3.6e-101 的精细调节下**，牛顿极限在形式上复现 Φ = GM/r'
           '（A2 机器确认）；但 (i) 该 κ 比真实曲率大 1.7e34 倍（B2），'
           '(ii) 线性化条件本身是一次 75 dex 的外部输入（C4/C6）。'
           '⇒ 「闭合」降格为「条件性闭合 + 一次精细调节」'),
          None, '★更正')

    entry('D4', 'FAIL',
          ('★综合：r80 的耦合项补全确实解掉了 I02/I08（形式/符号/归一化），'
           '本册证明它还**额外引入**一个此前未登记的条件——λ ≤ 3.6e-101 的精细调节；'
           '而即便满足该条件，四次项被压到可忽略 ⇒ 标量实质上是**自由场**'
           '⇒ PPN γ=−1、Cassini 排除 86956 倍（承 r80 E1）完全不变'
           '⇒ **这项调节买不到任何可证伪内容，只是让线性化在数值上勉强自洽**'),
          None, '★综合')

    entry('D5', 'BOUNDARY',
          ('不自推登记：'
           'NS1 λ_crit ∝ 1/M² 的推导假设「线性化须对同一 λ 在所有源上成立」，'
           '本册只用太阳做基准，未逐源核验；'
           'NS2 κ_phys 取 GM/(c²r) 作曲率尺度（施瓦西外径向曲率特征尺度），'
           '不同曲率不变量给不同数值因子，但 dex 结论不变；'
           'NS3 本册不复算 PPN γ=−1 与 Cassini 数值（承 r80 E1）。'
           '红线：数学／数值自洽 ≠ 物理证实；本册只做 r80 牛顿解的量级自洽性复算，'
           '不构成对 r80 其他结论或 TUFT 方向的普遍否证。'),
          None, '红线')


# ----------------------------------------------------------------------------
def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()

    verdict = 'FAIL' if COUNTS.get('FAIL') else (
        'BOUNDARY' if COUNTS.get('BOUNDARY') else 'PASS')

    payload = {
        'round': 'r87',
        'date': '2026-10-17',
        'source': SRC_NAME,
        'counts': COUNTS,
        'total': len(ENTRIES),
        'verdict': verdict,
        'guard_all_ok': all(g['ok'] for g in GUARDS),
        'guards': GUARDS,
        'entries': ENTRIES,
        'key_numbers': {
            'l_P': format(L_P, '.6E'),
            'C1': format(C1, '.6E'),
            'kappa_Sun_1AU': format(-(C1 * M_SUN * C_LIGHT) /
                                    (Decimal(4) * PI * HBAR * R_AU), '.6E'),
            'kappa_phys': format(G_NEWT * M_SUN / (C_LIGHT * C_LIGHT * R_AU), '.6E'),
            'ratio_kappa': '1.745361E+34',
            'lambda_crit': format(Decimal(12) * PI ** 2 * HBAR ** 3 /
                                  (C1 ** 2 * M_SUN ** 2 * C_LIGHT), '.6E'),
        },
        'not_self_derived': [
            {'tag': 'NS1', 'text': 'ħ、c、G 为 CODATA 实验锚点；G 为输入非输出（承 r80 C1）'},
            {'tag': 'NS2', 'text': 'r80 的场方程、C₁ 归一化、PPN γ=−1、Cassini 86956 倍均承 r80，本册不复算'},
            {'tag': 'NS3', 'text': 'κ_phys 取 GM/(c²r) 作曲率特征尺度，不同曲率不变量只改数值因子不改 dex 结论'},
            {'tag': 'NS4', 'text': 'λ_crit ∝ 1/M² 假设线性化须对所有源成立；本册仅以太阳为基准'},
        ],
        'red_line': ('数学／数值自洽 ≠ 物理证实；本册只做 r80 牛顿解的量级自洽性复算与'
                     '条件性闭合的更正，不构成对 r80 其他结论或 TUFT 方向的普遍否证'),
    }

    with io.open(os.path.join(DATA, STEM + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(payload, ensure_ascii=False, indent=1))

    rlines = ['TUFT-r87 r80 牛顿极限量级自洽性复算 运行报告',
              'counts=' + str(COUNTS) + ' total=' + str(len(ENTRIES)) +
              ' verdict=' + verdict, '']
    for e in ENTRIES:
        rlines.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rlines.append('    residual=' + e['residual'])
    rlines.append('')
    rlines.append('GUARD G0: ' + str(len(GUARDS)) + '/' + str(len(GUARDS)) + ' 全过')
    rlines.append('KEY l_P=' + format(L_P, '.6E') + ' C1=' + format(C1, '.6E'))
    with io.open(os.path.join(DATA, STEM + '_report.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rlines))

    ml = ['# 判定_TUFT-r87-r80牛顿极限量级自洽性复算', '',
          '日期：2026-10-17 · 评级：O/L2（r80 下游攻破·跨会话一致性复算）', '',
          '## 条目计数', '- 总条目：' + str(len(ENTRIES))]
    for k in sorted(COUNTS.keys()):
        ml.append('- ' + k + '：' + str(COUNTS[k]))
    ml.append('- 总体 verdict：' + verdict)
    ml.append('')
    ml.append('## 关键数值')
    for k, v in payload['key_numbers'].items():
        ml.append('- ' + k + ' = ' + v)
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
    print('')


if __name__ == '__main__':
    main()
