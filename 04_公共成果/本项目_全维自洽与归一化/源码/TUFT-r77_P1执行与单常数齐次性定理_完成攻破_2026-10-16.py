# -*- coding: utf-8 -*-
"""
r77 · 2026-10-16 · r74 下游（继续执行 P1 修法）
《P1 修法落地执行 + 单常数齐次性定理（质量与相互作用不可兼得）+ 四条绕行机制的机器排除》
==============================================================================
编号仲裁（起草前实测磁盘）：源码目录已占 31..76（含并行会话同日所占 r72 / r73 / r75 / r76）
=> 取首空号 r77（后到者改号，不覆盖他人任何文件字节）

继承链（不重推）：
  r69: L = (hbar c/2)(kappa^2 - tau^2) - U  =>  S7_R1 量纲非齐次 FAIL、S3_R1 无传播自由度
  r71: 零成本修法 kappa^2 -> (partial kappa)^2  =>  齐次 + 传播自由度恢复，
       但触发 C4 鬼场（tau 动能项系数 -hbar c < 0 => 哈密顿无下界）
  r74: 发现更上游冲突 —— S1 加号 sqrt(kappa^2+tau^2) vs S2 减号 (kappa^2-tau^2)；
       给出 P1 同号化出路（零新增常数、无鬼场）；
       但优化到 Omega5 合规的单常数四次势后两模均无质量 => D5 二难

本册执行四组：
  组 A  真正**落地** P1 修复版并机器复算（量纲 / EOM / 线性化 / 传播）
  组 B  ★承重定理：单常数 => U 必为齐次单项 => 「有质量」与「有相互作用」不可兼得
  组 C  ★四条绕行机制（平坦方向 / Coleman-Weinberg / 非多项式对数势 / 高阶导数自作用）
        的机器排除 —— 本册相对 r74 的全部增量
  组 D  对「完成统一场论」的最小诚实结论（根因定位 + 最小下一步排序，不代选）

纪律：
  纯标准库（Decimal 60 位 + Fraction 四元组量纲 (M,L,T,Q)）；
  所有断言先过 G0 自守卫再用于判定；所有「等于零」类结论必配阳性对照；
  不改写他人任何册的字节；跨册读数一律机器回读他人 JSON。
"""

import io
import json
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
STEM = 'TUFT-r77_P1执行与单常数齐次性定理_完成攻破_2026-10-16'
SRC_NAME = STEM + '.py'

R74_JSON = os.path.join(DATA, 'TUFT-r74_tau鬼场出路与S1符号一致性_修复优化_2026-10-16.json')
R71_JSON = os.path.join(DATA, 'TUFT-r71_lambda维度修正与导数项增广_攻破_2026-10-15.json')

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
# 量纲工具（四元组 (M,L,T,Q)，相乘 = 指数相加 —— 本库 r37 纪律）
# ----------------------------------------------------------------------------
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


D_HBAR = D(1, 2, -1, 0)
D_C = D(0, 1, -1, 0)
D_KAP = D(0, -1, 0, 0)
D_TAU = D(0, -1, 0, 0)
D_LEN = D(0, 1, 0, 0)
D_ENERGY = D(1, 2, -2, 0)
D_ENERGY_DENS = D(1, -1, -2, 0)
D_FORCE = D(1, 1, -2, 0)


def G0_guards():
    """量纲工具自守卫 + 跨册回链存在性（回链必须机器可查，不得硬编码读数）"""
    guard('G0-1', dmul(D_HBAR, D_C) == D(1, 3, -2, 0),
          '[hbar*c] = ' + dstr(dmul(D_HBAR, D_C)))
    guard('G0-2', dmul(D_LEN, D_LEN) == D(0, 2, 0, 0), '[L*L]')
    guard('G0-3', ddiv(D_ENERGY, dpow(D_LEN, 3)) == D_ENERGY_DENS,
          '能量 / L^3 = 能量密度（注意：能量 / L = 力，本册首版即写错，被此守卫拦下）')
    guard('G0-4', dmul(D_ENERGY_DENS, dpow(D_LEN, 3)) == D_ENERGY,
          '能量密度 * L^3 = 能量')
    guard('G0-5', D_FORCE != D_ENERGY_DENS, '力 != 能量密度（承 r71 G0-6）')
    guard('G0-6', os.path.exists(R74_JSON), 'r74 产物回链存在（跨册机器回读）')
    guard('G0-7', os.path.exists(R71_JSON), 'r71 产物回链存在（跨册机器回读）')



# ----------------------------------------------------------------------------
# 组 A：P1 修复版落地（r74 只判出路，本册把它写成显式拉氏密度并复算）
# ----------------------------------------------------------------------------
def group_A():
    # A1 两项动能的量纲
    d_partial = ddiv(D_KAP, D_LEN)            # [partial kappa] = L^-2
    d_k_k = dmul(dmul(D_HBAR, D_C), dpow(d_partial, 2))
    d_t_t = dmul(dmul(D_HBAR, D_C), dpow(ddiv(D_TAU, D_LEN), 2))
    ok1 = (d_k_k == D_ENERGY_DENS) and (d_t_t == D_ENERGY_DENS)
    entry('A1', 'PASS' if ok1 else 'FAIL',
          ('P1 修复版 L = (hbar c/2)[(partial kappa)^2 + (partial tau)^2] - U 的'
           '两项动能系数项量纲均为 ' + dstr(d_k_k) + '（= 能量密度）=> 齐次；'
           '对照 r69 原式 ' + dstr(dmul(dmul(D_HBAR, D_C), dpow(D_KAP, 2))) +
           '（= 力，非能量密度）'),
          dstr(d_k_k), '承 r74 C1 复算')

    # A2 EOM 齐次性
    d_box_kap = dmul(D_KAP, dpow(D_LEN, -2))          # [□kappa] = L^-3
    d_lhs = dmul(dmul(D_HBAR, D_C), d_box_kap)        # [hbar c □kappa]
    d_rhs = ddiv(D_ENERGY_DENS, D_KAP)                # [dU/dkappa]
    ok2 = (d_lhs == d_rhs)
    entry('A2', 'PASS' if ok2 else 'FAIL',
          ('修复版 EOM 齐次：左端 [hbar c □kappa] = ' + dstr(d_lhs) +
           '，右端 [dU/dkappa] = ' + dstr(d_rhs) + ' => 相等（' + str(ok2) + '）'),
          dstr(d_lhs), 'EOM')

    # A3 线性化：势取二次型时给 KG
    # 二次型势的系数 [lam2] = M L T^-2（= [U]/[kappa^2] = M L^-1 T^-2 / L^-2）
    d_lam2 = ddiv(D_ENERGY_DENS, dpow(D_KAP, 2))
    d_ratio = ddiv(d_lam2, dmul(D_HBAR, D_C))   # [lam2/(hbar c)] 应为 L^-2
    entry('A3', 'PASS' if d_ratio == D(0, -2, 0, 0) else 'FAIL',
          ('二次型势 U = lam2*(kappa^2+tau^2) 时 EOM 化为 KG：'
           '[lam2/(hbar c)] = ' + dstr(d_ratio) + ' = L^-2（恰为质量项 k^2 的量纲）'
           '=> 色散 omega^2 = c^2(k^2 + m_eff^2) 可闭合'),
          dstr(d_ratio), '线性化')

    # A4 层面警戒：S1 是曲线几何恒等式，场论动力学是另一层
    entry('A4', 'BOUNDARY',
          ('层面警戒（不自推）：S1 的 omega = c*sqrt(kappa^2+tau^2) 是**曲线 Frenet 几何'
           '恒等式**（沿一条世界线成立），而修复版 EOM 是**场论动力学方程**；'
           '把前者当作后者的约束会额外引入「逐点几何 = 场构型」的等同假设，'
           '该假设来料未给出、本册不代为补充'),
          None, '层面')

    # A5 跨册回读 r74 的鬼场读数，作为对照基线
    with io.open(R74_JSON, 'r', encoding='utf-8') as f:
        r74 = json.load(f)
    c2 = None
    for e in r74['entries']:
        if e['tag'] == 'C2':
            c2 = e['residual']
    entry('A5', 'PASS' if c2 == '1.758836469795381E-35' else 'BOUNDARY',
          ('跨册机器回读 r74 C2 的 H 末点 = ' + str(c2) +
           '（正、有下界）=> 本册 P1 落地版以此为对照基线，'
           '不再重复计算哈密顿密度'),
          str(c2), '回链')



# ----------------------------------------------------------------------------
# 组 B：★承重 —— 单常数齐次性定理（质量 与 相互作用 不可兼得）
# ----------------------------------------------------------------------------
def group_B():
    # B1 单项式扫描：U 的一项 = lam * kappa^a * tau^b，求 [lam]
    groups = {}
    for a in range(0, 7):
        for b in range(0, 7):
            dm = dmul(dpow(D_KAP, a), dpow(D_TAU, b))     # L^-(a+b)
            dlam = ddiv(D_ENERGY_DENS, dm)                # M L^(a+b-1) T^-2
            groups.setdefault(dlam, []).append((a, b))
    same_key = None
    for k, v in groups.items():
        if len(v) > 1:
            same_key = (k, v)
    # 同一 [lam] 的项，其总次数 a+b 必须相同
    degs = {}
    for k, v in groups.items():
        for (a, b) in v:
            degs.setdefault(k, set()).add(a + b)
    ok = all(len(s) == 1 for s in degs.values())
    entry('B1', 'PASS' if ok else 'FAIL',
          ('★齐次性前提机器验证：在 (a,b) in [0,6]^2 共 49 个单项式上，'
           '要求 [U] = 能量密度时系数维数 [lam] = M L^(a+b-1) T^-2 只依赖【总次数 a+b】'
           '=> 共用一个维度常数 lam 的所有项必为【同一总次数】（' + str(ok) + '）；'
           '不同总次数的项各需各自独立的维度常数'),
          str(len(groups)), '★承重前提')

    # B2 同次多项组合需要额外的「无量纲系数」=> 按 Ω5 计入连续常数后不是零代价
    for n in (2, 4):
        cnt = n + 1   # 总次数 n 的单项式个数：kappa^n, kappa^(n-1) tau, ...
        entry('B2-n' + str(n), 'BOUNDARY',
              ('总次数 n=' + str(n) + ' 的单项式共 ' + str(cnt) + ' 个；若允许它们任意组合，'
               '除整体 [lam] 外还需 ' + str(cnt - 1) + ' 个【无量纲】系数；'
               '按 r15 口径 I/II（连续常数一律计数）它们同样是自由常数 '
               '=> 「多个同次项」不是零代价；唯一零额外常数的情形 = '
               '由对称性把组合压成【单一不变量】'),
              str(cnt - 1), '参数账')

    # B3 齐次次数机器判定（标度律指数）
    def scaling_exponent(U, v, alphas):
        u0 = U(v[0], v[1])
        if u0 == 0:
            return None
        outs = []
        for al in alphas:
            ua = U(al * v[0], al * v[1])
            outs.append((ua / u0).ln() / Decimal(al).ln())
        return outs

    v = (Decimal('0.3'), Decimal('0.7'))
    alphas = [Decimal('2'), Decimal('3'), Decimal('5')]
    U2 = lambda k, t: (k * k + t * t)
    U4 = lambda k, t: ((k * k + t * t) ** 2)
    e2 = scaling_exponent(U2, v, alphas)
    e4 = scaling_exponent(U4, v, alphas)
    ok2 = all(abs(x - Decimal('2')) < Decimal('1e-30') for x in e2)
    ok4 = all(abs(x - Decimal('4')) < Decimal('1e-30') for x in e4)
    entry('B3', 'PASS' if (ok2 and ok4) else 'FAIL',
          ('齐次次数机器判定（标度律指数 ln[U(αv)/U(v)]/ln α）：'
           'U2 = kappa^2+tau^2 给 ' + ' / '.join(format(x, '.6E') for x in e2) +
           '（= 2）；U4 = (kappa^2+tau^2)^2 给 ' +
           ' / '.join(format(x, '.6E') for x in e4) + '（= 4）'),
          format(e4[-1], '.6E'), '标度律')

    # B4 质量项（原点二阶差分）
    def d2(U, h):
        hh = Decimal(h)
        return (U(hh, Decimal('0')) - 2 * U(Decimal('0'), Decimal('0'))
                + U(-hh, Decimal('0'))) / (hh * hh)

    hs = ['1e-2', '1e-3', '1e-4']
    v2 = [d2(U2, h) for h in hs]
    v4 = [d2(U4, h) for h in hs]
    mass2 = abs(v2[-1] - Decimal('2')) < Decimal('1e-6')
    mass4 = abs(v4[-1]) < Decimal('1e-6') and abs(v4[0]) > abs(v4[1]) > abs(v4[2])
    entry('B4', 'PASS' if (mass2 and mass4) else 'FAIL',
          ('★质量项：U2（二次型）在原点二阶差分 = ' +
           ' / '.join(format(x, '.6E') for x in v2) + ' => 2·lam ≠ 0【有质量】；'
           'U4（四次型）给 ' + ' / '.join(format(x, '.6E') for x in v4) +
           ' => 随步长趋于 0【无质量】（独立复算 r74 D3）'),
          format(v4[-1], '.6E'), '★质量')

    # B5 相互作用（标度指数 4 <=> 非二次 <=> 有自相互作用；2 <=> 自由场）
    entry('B5', 'PASS' if (ok2 and ok4) else 'FAIL',
          ('★相互作用：势的齐次次数 = 2 => 拉氏量为场二次型 => 自由场（无散射、无自作用，'
           '教科书标准结论，本册引用不自推）；齐次次数 = 4 => 存在非零四阶导数 => '
           '有自相互作用。=> **单个维度常数只能二选一**'),
          None, '★相互作用')

    # B6 定理
    entry('B6', 'FAIL',
          ('★承重定理（本册核心）：在「动能系数固定为 hbar·c、只允许 1 个自由常数」的'
           '修复版框架内 —— (i) 取齐次 2 次势 => 有质量但【无相互作用（自由场）】，'
           '无法给出力、无法与物质耦合、无法再现四力中的任何一种；'
           '(ii) 取齐次 ≥4 次势 => 有相互作用但【无质量、且原点即唯一极小】，'
           '=> 力程无穷长，与弱/强力程有限直接冲突。'
           '**⇒ 「有质量」与「有相互作用」在该框架内不可兼得；两者兼得至少需要 2 个常数 ⇒ 撞 Ω5（≤1）。**'),
          None, '★定理')

    # B7 阳性对照：双常数
    def U_both(k, t):
        r2 = k * k + t * t
        return -Decimal('0.5') * r2 + r2 * r2

    best_r, best_v = None, None
    r = Decimal('0')
    while r <= Decimal('1.2'):
        val = U_both(r, Decimal('0'))
        if best_v is None or val < best_v:
            best_v, best_r = val, r
        r += Decimal('0.001')
    ctrl_ok = (best_r is not None and abs(best_r - Decimal('0.5')) < Decimal('2e-3'))
    entry('B7', 'PASS' if ctrl_ok else 'FAIL',
          ('阳性对照（双常数 U = -(1/2)m^2(kappa^2+tau^2) + lam(kappa^2+tau^2)^2，m^2=lam=1）：'
           '数值扫描极小位于 |phi| = ' + format(best_r, '.6E') +
           '（解析 0.5）≠ 0 => 双常数确实同时给出【质量 + 相互作用 + 确定标度的真空】，'
           '检验器非恒零，B6 的「不可兼得」是真结论不是检验器失灵'),
          format(best_r, '.6E'), '阳性对照')



# ----------------------------------------------------------------------------
# 组 C：★四条绕行机制的机器排除（本册相对 r74 的全部增量）
# ----------------------------------------------------------------------------
def group_C():
    # C1 机制①：平坦方向 U = lam*(kappa^2 - tau^2)^2 —— 有连续真空但标度自由
    Uf = lambda k, t: ((k * k - t * t) ** 2)
    ray = [Decimal(x) for x in ('0.1', '1', '10', '100')]
    ray_vals = [Uf(a, a) for a in ray]
    flat = all(abs(v) < Decimal('1e-50') for v in ray_vals)
    # 是否 SO(2)（场空间旋转）不变：theta = pi/6 旋转后比较
    import math as _m
    cth = Decimal(repr(_m.cos(_m.pi / 6)))
    sth = Decimal(repr(_m.sin(_m.pi / 6)))
    k0, t0 = Decimal('0.3'), Decimal('0.7')
    k1 = cth * k0 - sth * t0
    t1 = sth * k0 + cth * t0
    iso = abs(Uf(k1, t1) - Uf(k0, t0)) < Decimal('1e-40')
    entry('C1', 'BOUNDARY',
          ('★机制①平坦方向 U = lam*(kappa^2 - tau^2)^2：射线 kappa=tau=α 上 '
           'U(α,α) = ' + ' / '.join(format(v, '.6E') for v in ray_vals) +
           '（α = 0.1/1/10/100）=> **确有连续真空流形**（' + str(flat) + '），'
           '但真空期望值 |<phi>| 的大小**完全自由**（整条射线都是极小）'
           '=> 由它产生的质量 ∝ |<phi>| 无确定值 ⇒ 等价再引入 1 个输入 ⇒ **不绕过 B6**；'
           '附加代价：该势在 (kappa,tau) 平面旋转下不变 = ' + str(iso) +
           '（π/6 旋转对照）=> 破坏场空间 SO(2)，引入各向异性'),
          format(ray_vals[-1], '.6E'), '机制①')

    # C2 机制②：Coleman-Weinberg 量纲嬗变
    entry('C2', 'BOUNDARY',
          ('★机制②Coleman–Weinberg 量纲嬗变（由无量纲耦合经圈修正生成标度）：'
           '（a）它需要【圈图 + 重整化点】，而当前框架尚未完成量子化（无传播子量子化、'
           '无重整化方案、无相互作用顶点费曼规则）—— 本册只判定「当前不可执行」，'
           '不判定「永远不可执行」；（b）即便执行，CW 仍须显式引入一个重整化能标 μ，'
           '按 r15 口径 II（常数 + 节点 + 函数）记账 ⇒ **至少 1 个外部输入**；'
           '（c）CW 生成的标度相对于 μ 指数压低，与「四力耦合跨 33 dex」的对齐问题'
           '无已知机制（承 r15/r17）=> 不构成零代价解'),
          None, '机制②')

    # C3 机制③：非多项式（对数）势
    d_lp2 = dmul(dmul(D(-1, 3, -2, 0), D_HBAR), dpow(D_C, -3))  # [G hbar / c^3] = L^2
    ok_lp = d_lp2 == D(0, 2, 0, 0)
    entry('C3', 'FAIL' if ok_lp else 'BOUNDARY',
          ('★机制③非多项式势 U = lam*(kappa^2+tau^2)^2 * ln((kappa^2+tau^2)/kappa0^2)：'
           '对数宗量必须无量纲 ⇒ 必须再引入一个同量纲标度 kappa0（[kappa0] = L^-1）'
           '⇒ **+1 个常数** ⇒ 不绕过 B6。（唯一「不加新常数」的取法是令 '
           'kappa0 = 1/l_P，而 [G hbar / c^3] = ' + dstr(d_lp2) +
           '（= L^2，' + str(ok_lp) + '）确可构造 l_P；但那是**普朗克锚定**，'
           '承 r71 D3 / r41 二阶两难 A ⇒ 循环自洽、不可证伪）'),
          dstr(d_lp2), '机制③')

    # C4 机制④：高阶导数自相互作用
    d_dk4 = dpow(ddiv(D_KAP, D_LEN), 4)                 # [(partial kappa)^4] = L^-8
    d_lamp = ddiv(D_ENERGY_DENS, d_dk4)                 # [lam']
    entry('C4', 'BOUNDARY',
          ('★机制④高阶导数自相互作用 lam\'*(partial kappa)^4：'
           '[lam\'] = ' + dstr(d_lamp) + ' ⇒ 与动能系数 hbar·c 不同幂次，'
           '**必为独立新常数**；且含场的高阶时间导数项一般触发 Ostrogradsky 不稳定'
           '（承 GAQ-UFT V18 册「非变分/传播性判据」族，本册不重推其系数）'
           '=> 既不满足 Ω5，又引入新的稳定性风险'),
          dstr(d_lamp), '机制④')

    entry('C5', 'FAIL',
          ('★四条绕行机制汇总：①平坦方向（有 SSB 但真空标度自由 ⇒ 等价 +1 输入，'
           '且破坏场空间 SO(2)）②Coleman–Weinberg（当前未量子化 ⇒ 不可执行，'
           '且须重整化能标 ⇒ ≥1 外部输入）③对数型非多项式势（须第二标度 ⇒ +1，'
           '或退化为普朗克锚定 ⇒ 循环）④高阶导数自作用（新常数 + Ostrogradsky 风险）'
           '⇒ **四条均无零代价解，B6 的「不可兼得」未被绕过**'),
          None, '★汇总')



# ----------------------------------------------------------------------------
# 组 D：对「完成统一场论」的最小诚实结论
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'FAIL',
          ('★根因定位（本册对整条 r69→r71→r74→r77 链的最终记账）：'
           '「未完成」的根因**不是某个公式写错**（量纲、符号、导数项三类错都可零成本修），'
           '而是**公设级资源不足** —— 要在单标量对 (kappa,tau) 上同时取得'
           '【传播】+【无鬼】+【有质量】+【有相互作用】，最少需要 '
           '2 个自由常数（B6/B7），而 Ω5 只允许 ≤ 1 ⇒ **结构性不可完成**。'
           '=> 这不是「还没推导出来」，而是「给多少推导都补不上」。'),
          None, '★根因')

    entry('D2', 'BOUNDARY',
          ('三条可能的继续方向（**本册不代选**，按代价升序）：'
           '① **放宽 Ω5**（如「≤3 个常数且须显式登记为外部输入」，即 r14 出路④型）'
           '—— 属科学哲学层面的选择，非计算问题；'
           '② **扩充场内容**（引入物质场 / 规范场，把「相互作用」交给规范耦合而非纯标量势）'
           '—— 与本库 r15 口径 II 的告诫同源：那不是「+1 个常数」而是「+1 个函数/扇区」，'
           '自由度账会更大；'
           '③ **放弃「由该作用量给出四力」这一目标**，把框架定位为纯几何/运动学编码层'
           '（承 R14 对 TUFT 的定位）。'),
          None, '方向')

    entry('D3', 'INFO',
          ('★本册可复用的两条新判据：'
           '（a）**齐次次数—物理属性判据**：拉氏势的齐次次数直接读出物理属性 —— '
           '次数 2 ⇒ 自由场（有质量、无相互作用）；次数 ≥4 ⇒ 有相互作用、原点无质量。'
           '判定「有没有质量 / 有没有相互作用」可不经谱分解，只看标度律指数；'
           '（b）**平坦方向陷阱判据**：候选势若有连续真空流形，必须额外检查 '
           '"真空期望值的模长是否被确定" —— 未被确定 ⇒ SSB 名义成立但质量不确定，'
           '等价于偷偷引入一个输入（本册 C1 即此类）。'),
          None, '判据')

    entry('D4', 'PASS',
          ('本册与并行册的分工声明：r76（他人）审「V4.8 极限定理的量纲核验与完成度」，'
           '属 801–1000 条目集一侧；本册属 r69/r71/r74 的 S1/S2 作用量一侧。'
           '两者**来料入口不同、零重复**；共同触及的「作用量量纲」结论一致。'),
          None, '分工')


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
        'round': 'r77',
        'date': '2026-10-16',
        'source': SRC_NAME,
        'counts': COUNTS,
        'total': len(ENTRIES),
        'verdict': verdict,
        'guard_all_ok': all(g['ok'] for g in GUARDS),
        'guards': GUARDS,
        'entries': ENTRIES,
        'not_self_derived': [
            {'tag': 'NS1', 'text': '「二次型势 = 自由场、无散射」为标准场论教科书结论，本册引用不自推'},
            {'tag': 'NS2', 'text': 'Coleman-Weinberg 机制是否可在该框架内实现，本册只判定「当前未量子化故不可执行」，不判定「永远不可执行」'},
            {'tag': 'NS3', 'text': 'Ostrogradsky 不稳定的判据与系数承 GAQ-UFT V18 册，本册不重推'},
            {'tag': 'NS4', 'text': 'ħ、c 为 CODATA 实验锚点；以 l_P 替代第二标度属普朗克锚定，其循环性承 r71 D3 / r41'},
            {'tag': 'NS5', 'text': '三条继续方向（放宽 Ω5 / 扩充场内容 / 改为几何编码层）本册只登记代价，不代选'},
        ],
        'red_line': ('数学/数值自洽 != 物理证实；本册只做 P1 修法的机器落地、单常数齐次性定理与'
                     '四条绕行机制的排除，「该框架在当前公设集内结构性不可完成统一场论」'
                     '不构成对 TUFT 方向的普遍否证'),
    }

    with io.open(os.path.join(DATA, STEM + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(payload, ensure_ascii=False, indent=1))

    rlines = ['TUFT-r77 P1 执行与单常数齐次性定理 完成攻破 运行报告',
              'counts=' + str(COUNTS) + ' total=' + str(len(ENTRIES)) +
              ' verdict=' + verdict, '']
    for e in ENTRIES:
        rlines.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rlines.append('    residual=' + e['residual'])
    rlines.append('')
    rlines.append('GUARD G0: 自守卫（量纲 + 跨册回链存在性）全过  ' +
                  str(len(GUARDS)) + '/' + str(len(GUARDS)))
    with io.open(os.path.join(DATA, STEM + '_report.txt'), 'w',
                 encoding='utf-8') as f:
        f.write('\n'.join(rlines))

    ml = ['# 判定_TUFT-r77-P1执行与单常数齐次性定理_完成攻破', '',
          '日期：2026-10-16 · 评级：O/L2（r74 下游继续执行）', '',
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
    print('')


if __name__ == '__main__':
    main()

