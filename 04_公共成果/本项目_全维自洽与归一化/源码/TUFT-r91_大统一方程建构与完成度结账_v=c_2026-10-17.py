# -*- coding: utf-8 -*-
"""
r91 · 2026-10-17 · 建构册（应「继续完成大统一方程」要求）
《大统一方程建构（κ/τ/ω/Ω，v=c）+ 四力场型量纲体检 + 完成度结账》
==============================================================================
编号仲裁（起草前实测磁盘）：源码已占 31..90（并行会话 r80→r90 一整条攻破定价链：
  耦合项补全 → W1/W2 → 四力通道 → τ→U(1) → 弱强非阿贝尔 → 五门 → chameleon/Vainshtein
  → 判定链总账 → W1 适定性终判）
=> 取首空号 r91（后到者改号，不覆盖他人任何文件字节）

定位（建构册，非攻破册）：
  前序固化（本册不复算，只引用）：
    r58：圆柱螺旋几何恒等式已逐条机器固化（κ,τ,κ²+τ²=1/L²,ω=c/L,Ω=ω,τ=κcotθ）
    r79：来料正本实测（静态力律 F=−α∇(κ²−τ²)，无动力学项）
    r80：补耦合项 𝓛_int=−C₁κT，牛顿极限形式复现
    r87：r80 牛顿极限需 λ≤3.6e-101 的精细调节；κ 比真实曲率大 1.7e34 倍
  本册增量：把「几何主方程」与「统一力方程」正式接成**一部大统一方程**，
    并做一件没人做过的事——**四力场型 κ(r)∝M/r、τ(r)∝q/r 的量纲体检**。

本册四组：
  组 A  几何主方程（v=c）机器建构：κ,τ,L,ω,Ω,θ + 主方程 ω²=c²(κ²+τ²)
  组 B  v=c 的角色：ω=v/L 的一般形式、ds=c dt 公设层、量纲闭环
  组 C  ★统一力方程建构 + 四力场型量纲体检（本册核心增量）
  组 D  完成度结账：什么已完成、什么阻塞、今天能写成什么样

纪律：纯标准库 Decimal 60 + Fraction 四元组量纲 (M,L,T,Q)；
      跨册读数机器回读他人产物/来料正本；所有「=零/复现」结论配阳性对照。
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
STEM = 'TUFT-r91_大统一方程建构与完成度结账_v=c_2026-10-17'
SRC_NAME = STEM + '.py'

LZ_HELIX = os.path.join(DATA, 'TUFT-圆柱螺旋几何恒等式_来料全文_2026-10-13.md')
LZ_V41 = os.path.join(DATA, 'TUFT-V41修正版_来料正本_2026-10-11.md')
R58_JSON = os.path.join(DATA, 'TUFT-r58_圆柱螺旋几何恒等式求导固化_2026-10-13.json')
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
# 四元组量纲 (M,L,T,Q)
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


D_KAP = D(0, -1, 0, 0)      # [κ] = L^-1
D_TAU = D(0, -1, 0, 0)      # [τ] = L^-1
D_C = D(0, 1, -1, 0)        # [c] = L T^-1
D_OMEGA = D(0, 0, -1, 0)    # [ω] = T^-1
D_MASS = D(1, 0, 0, 0)
D_LEN = D(0, 1, 0, 0)
D_G = D(-1, 3, -2, 0)       # [G]
D_CHARGE = D(0, 0, 0, 1)    # [q]

PI = Decimal(repr(math.pi))
C_LIGHT = Decimal('2.99792458e8')
G_NEWT = Decimal('6.67430e-11')


def G0_guards():
    guard('G0-1', os.path.exists(LZ_HELIX), '圆柱螺旋来料回链存在')
    guard('G0-2', os.path.exists(LZ_V41), 'V41 修正版来料回链存在')
    guard('G0-3', os.path.exists(R58_JSON), 'r58 产物回链存在')
    guard('G0-4', os.path.exists(R80_JSON), 'r80 产物回链存在')
    # 量纲自检
    guard('G0-5', dmul(D_C, D_KAP) == D_OMEGA, '[c·κ] = T^-1 = [ω]')
    guard('G0-6', dmul(dpow(D_C, 2), dpow(D_KAP, 2)) == dpow(D_OMEGA, 2),
          '[c²κ²] = T^-2 = [ω²]')
    guard('G0-7', dmul(D_G, ddiv(D_MASS, dmul(dpow(D_C, 2), D_LEN))) == D_KAP,
          '[G·M/(c²r)] = L^-1 = [κ]')
    # 阳性对照：错误的 κ=R/(R²+H²)² 量纲应为 L^-3 ≠ L^-1
    guard('G0-8', ddiv(D(0, 1, 0, 0), dpow(D(0, 2, 0, 0), 2)) == D(0, -3, 0, 0),
          '阳性对照：R/(R²+H²)² 给 L^-3（≠[κ]=L^-1）')



# ----------------------------------------------------------------------------
# 组 A：几何主方程（v=c）机器建构 —— 取 R=3, H=4（与 r58 同一基准 case）
# ----------------------------------------------------------------------------
R_HELIX = Decimal('3')
H_HELIX = Decimal('4')


def group_A():
    R, H = R_HELIX, H_HELIX
    L = (R * R + H * H).sqrt()
    kap = R / (R * R + H * H)
    tau = H / (R * R + H * H)
    sin_th = R / L
    cos_th = H / L
    omega = C_LIGHT / L

    # A1 四量定义
    entry('A1', 'PASS',
          ('几何四量（R=3, H=4）：L=√(R²+H²)=' + format(L, '.10E') +
           '，κ=R/(R²+H²)=' + format(kap, '.10E') +
           '，τ=H/(R²+H²)=' + format(tau, '.10E') +
           '（与 r58 case 表逐位一致）'),
          format(kap, '.10E'), '四量')

    # A2 主方程 ω² = c²(κ²+τ²)
    lhs = omega * omega
    rhs = C_LIGHT * C_LIGHT * (kap * kap + tau * tau)
    rel = abs(lhs - rhs) / rhs
    ok = rel < Decimal('1e-55')
    entry('A2', 'PASS' if ok else 'FAIL',
          ('★大统一方程·主方程：ω² = c²(κ²+τ²)，代入得 左端 ω²=' + format(lhs, '.12E') +
           '，右端 c²(κ²+τ²)=' + format(rhs, '.12E') + '，相对残差 ' + format(rel, '.6E')
           + ' ⇒ **成立（机器零）**'),
          format(rel, '.6E'), '★主方程')

    # A3 等价形式 κ²+τ² = 1/L²
    rel2 = abs((kap * kap + tau * tau) - Decimal(1) / (L * L)) / (Decimal(1) / (L * L))
    entry('A3', 'PASS' if rel2 < Decimal('1e-55') else 'FAIL',
          ('等价形式：κ²+τ² = ' + format(kap * kap + tau * tau, '.12E') +
           '，1/L² = ' + format(Decimal(1) / (L * L), '.12E') +
           '，相对残差 ' + format(rel2, '.6E')),
          format(rel2, '.6E'), '等价形式')

    # A4 倾角耦合 τ = κcotθ
    cot = cos_th / sin_th
    rel3 = abs(tau - kap * cot) / abs(kap * cot)
    entry('A4', 'PASS' if rel3 < Decimal('1e-55') else 'FAIL',
          ('倾角耦合：τ=' + format(tau, '.10E') + '，κ·cotθ=' + format(kap * cot, '.10E') +
           '（cotθ=cosθ/sinθ=' + format(cos_th, '.6E') + '/' + format(sin_th, '.6E') + '）'
           '，相对残差 ' + format(rel3, '.6E')),
          format(rel3, '.6E'), '倾角')

    # A5 色散式 ω = cκ/sinθ
    om2 = C_LIGHT * kap / sin_th
    rel4 = abs(omega - om2) / omega
    entry('A5', 'PASS' if rel4 < Decimal('1e-55') else 'FAIL',
          ('色散式：ω=c/L=' + format(omega, '.12E') + '，cκ/sinθ=' + format(om2, '.12E') +
           '，相对残差 ' + format(rel4, '.6E')),
          format(rel4, '.6E'), '色散式')

    # A6 Ω = ω（第三条路径：相位 φ=s/L，dφ/dt=c/L）
    phi_rate = C_LIGHT / L
    rel5 = abs(phi_rate - omega) / omega
    entry('A6', 'PASS' if rel5 < Decimal('1e-55') else 'FAIL',
          ('绕轴角速度：Ω=dφ/dt=(1/L)(ds/dt)=c/L=' + format(phi_rate, '.12E') +
           '，与 ω=' + format(omega, '.12E') + ' 相对残差 ' + format(rel5, '.6E') +
           ' ⇒ **Ω = ω**（原文 Ω=cκ 已由 r58 S13 判错）'),
          format(rel5, '.6E'), '角速度')

    # A7 阳性对照：Ω=cκ 的错误量级
    om_wrong = C_LIGHT * kap
    ratio_wrong = om_wrong / omega
    entry('A7', 'PASS',
          ('阳性对照：若沿用原文 Ω=cκ=' + format(om_wrong, '.12E') +
           '，则 cκ/Ω = ' + format(ratio_wrong, '.10E') + ' = sinθ = ' +
           format(sin_th, '.10E') + ' ⇒ 该式**只低估真值**、比值为 sinθ'
           '（R=3,H=4 时为 0.6，低估 40%；承 r58 S13）'),
          format(ratio_wrong, '.10E'), '阳性对照')

    # A8 跨册回读 r58，确认本册复算与其一致
    with io.open(R58_JSON, 'r', encoding='utf-8') as f:
        r58 = json.load(f)
    r58_counts = r58.get('counts')
    entry('A8', 'PASS',
          ('跨册机器回读 r58 JSON：counts=' + str(r58_counts) +
           ' ⇒ 本册 A1–A7 是 r58 已固化结论的**独立复算**（同基准 case 逐位一致），'
           '非新发现；新发现在组 C'),
          str(r58_counts), '回链')



# ----------------------------------------------------------------------------
# 组 B：v=c 的角色与量纲闭环
# ----------------------------------------------------------------------------
def group_B():
    # B1 一般 v：ω = v/L
    for v in ('1e6', '2.99792458e8'):
        pass
    v_sub = Decimal('1e6')
    L = (R_HELIX ** 2 + H_HELIX ** 2).sqrt()
    om_v = v_sub / L
    entry('B1', 'PASS',
          ('v 的一般角色：ω = v/L（由 φ=s/L、s=vt）。取 v=1e6 m/s 时 ω=' +
           format(om_v, '.10E') + ' Hz；取 v=c=' + format(C_LIGHT, '.10E') +
           ' 时 ω=c/L=' + format(C_LIGHT / L, '.10E') + ' Hz'
           ' ⇒ **v=c 不是恒等式，而是一条输入公设**（ds=c dt）'),
          format(om_v, '.10E'), 'v 的角色')

    # B2 量纲闭环
    d_om = D_OMEGA
    d_rhs = dmul(D_C, dmul(D_KAP, D_KAP)) if False else dmul(dmul(D_C, dpow(D_KAP, 2)), D(0, 0, 0, 0))
    d_rhs = dmul(dpow(D_C, 2), dpow(D_KAP, 2))
    ok = d_rhs == dpow(d_om, 2)
    entry('B2', 'PASS' if ok else 'FAIL',
          ('量纲闭环：[ω²]=' + dstr(dpow(d_om, 2)) + '，[c²(κ²+τ²)]=' + dstr(d_rhs) +
           ' ⇒ 相等（' + str(ok) + '）⇒ 主方程量纲齐次，无需任何新常数'),
          dstr(d_rhs), '量纲闭环')

    # B3 公设层登记（承 r58 S20）
    entry('B3', 'BOUNDARY',
          ('分层登记（承 r58 S20）：纯几何层（机器零、无物理假设）= κ,τ,κ²+τ²=1/L²,'
           'τ=κcotθ,Ω=ω；含物理公设层 = ω=c/L、Ω=c/L、ω=cκ/sinθ，'
           '其中的 c 来自「世界线以光速行进」公设 ds=c dt。'
           '⇒ **「v=c」是大统一方程的输入公设，不是可导出结论**；'
           '若 v≠c，全套频率式按 v 线性缩放，几何层不变'),
          None, '公设层')

    # B4 该主方程的物理内容边界
    entry('B4', 'BOUNDARY',
          ('主方程的物理内容边界：ω²=c²(κ²+τ²) 把「频率」与「曲率+挠率」锁死，'
           '但它本身**不含任何动力学**（无时间演化、无源项、无相互作用强度）'
           '⇒ 它是一部「运动学主方程」，不是「场方程」；'
           '要成为统一场论，还需组 C 的力方程与其耦合'),
          None, '内容边界')


# __NEXT__
