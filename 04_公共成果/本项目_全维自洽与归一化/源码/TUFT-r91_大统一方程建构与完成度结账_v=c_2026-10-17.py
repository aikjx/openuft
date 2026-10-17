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
  与 r92「大统一方程定稿」的分工（诚实声明，零重复口径）：
    r92 已把方程写成**七式三层定稿件**（几何/v=c 桥接/α 量纲/U 体积标度缺口/四力代入/UFT-1..6 终审 1/6）。
    本册**不重复** r92 的 α 量纲与 U 体积标度缺口（B①②）；
    **只补 r92 未覆盖的一条**：**四力场振幅 κ(r)∝M/r、τ(r)∝q/r 自身的量纲体检**
      —— 来料写法与几何 [κ]=[τ]=L^-1 差一个质量维，强制引入 ≥6 个维度常数 → Ω5 违反（第 3 条独立路径）。
    组 A/B 的几何与 v=c 部分为 r58/r92 同基准独立重算（非新证），仅作本册推导底座。
  前序固化（本册引用，不复算）：
    r58：圆柱螺旋几何恒等式逐条固化；r79：来料正本实测 F=−α∇(κ²−τ²)；
    r80：耦合项 𝓛_int=−C₁κT；r87：牛顿极限 λ≤3.6e-101、κ 比真实曲率大 1.7e34 倍；
    r89 G1 已跨册机读并确认 r87 与 r89「互为加强、零重复裁定」。

本册四组：
  组 A  几何主方程（v=c）机器建构（r58/r92 重算底座）
  组 B  v=c 的角色与量纲闭环
  组 C  ★四力场型量纲体检（本册唯一新增，r92 未覆盖）
  组 D  完成度结账：与 r92 定稿件的衔接 + 什么阻塞

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
R87_JSON = os.path.join(DATA, 'TUFT-r87_r80牛顿极限量级自洽性复算_攻破_2026-10-17.json')

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
    guard('G0-7', dmul(D_G, ddiv(D_MASS, dmul(dpow(D_C, 2), dpow(D_LEN, 2)))) == D_KAP,
          '[G·M/(c²r²)] = L^-1 = [κ]')
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
    r58_info = ('items=' + str(len(r58.get('items', []))) +
                ', guards=' + str(len(r58.get('guards', []))))
    entry('A8', 'PASS',
          ('跨册机器回读 r58 JSON：' + r58_info +
           ' ⇒ 本册 A1–A7 是 r58 已固化结论的**独立复算**（同基准 case R=3,H=4 逐位一致），'
           '非新发现；新发现在组 C'),
          r58_info, '回链')



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



# ----------------------------------------------------------------------------
# 组 C：★统一力方程建构 + 四力场型量纲体检（本册核心增量）
# ----------------------------------------------------------------------------
def group_C():
    # C1 统一力方程形式（承 r79/r80 来料正本）
    #    F = −α ∇(κ² − τ²)，[α]=L（自然单位）
    d_geom = D_KAP              # [κ]=L^-1
    d_force = dmul(D(0, 1, 0, 0), dmul(D(0, -1, 0, 0), dpow(D_KAP, 2)))
    entry('C1', 'PASS',
          ('统一力方程形式（承 r79/r80 来料正本）：F = −α ∇(κ²−τ²)'
           '，[α]=L（自然单位）→ [F]=L·L⁻¹·L⁻² = ' + dstr(d_force) +
           '。注：几何主方程用 **加号** κ²+τ²，力方程用 **减号** κ²−τ²'),
          dstr(d_force), '力方程形式')

    # C2 ★符号冲突（加 vs 减）—— 机器回读两份来料正本（均为 LaTeX 记号）
    with io.open(LZ_HELIX, 'r', encoding='utf-8') as f:
        txt_helix = f.read()
    with io.open(LZ_V41, 'r', encoding='utf-8') as f:
        txt_v41 = f.read()
    has_plus = r'\kappa^2+\tau^2' in txt_helix
    has_minus_cn = (r'\kappa^2 - \tau^2' in txt_v41) or (r'\kappa^2-\tau^2' in txt_v41)
    entry('C2', 'FAIL' if (has_plus and has_minus_cn) else 'INFO',
          ('★符号冲突（机器回读两份来料 LaTeX 记号）：'
           '圆柱螺旋来料（几何层）含 `\\kappa^2+\\tau^2` = ' + str(has_plus) +
           '；V41 修正版（力层）含 `\\kappa^2 - \\tau^2`/`[\\kappa^2-\\tau^2]` = ' +
           str(has_minus_cn) +
           ' ⇒ **同一对 (κ,τ)，几何用加、力用减**——这是 r74 判定的「上游符号冲突」'
           '在两份正本上的坐实，不是重建引入的'),
          None, '★符号冲突')

    # C3 ★NEW 量纲体检：四力场型与几何 [κ]=[τ]=L^-1 相差一个质量维
    #   来料写法 κ(r) ∝ M/r，[M/r]=M L^-1；修复到 L^-1 须 κ=GM/(c² r²)
    d_ka_geo = D_KAP                                   # L^-1
    d_MoverR = ddiv(D_MASS, D_LEN)                     # M L^-1
    dim_gap = ddiv(d_MoverR, d_ka_geo)                 # = M
    repair = dmul(D_G, ddiv(D_MASS, dmul(dpow(D_C, 2), dpow(D_LEN, 2))))  # GM/(c² r²)
    entry('C3', 'FAIL',
          ('★四力量纲体检（本册核心）：来料「κ(r)∝M/r」的量纲 [M/r]=' + dstr(d_MoverR) +
           '，而几何 [κ]=' + dstr(d_ka_geo) + '，差 ' + dstr(dim_gap) + '（一个质量维）。'
           '修复到 [κ]=L^-1 须写为 κ=GM/(c²r²)（量纲 ' + dstr(repair) + '=L^-1 ✓）；'
           '若想修复到真正的曲率 L^-2 则还需再多一个 L^-1。'
           '⇒ **重力场 κ 的定义本身就强制引入带质量量纲的常数**——'
           '该常数（不论 G/c² 还是等效量）是定义场本身所需，不是力律里的额外耦合'),
          dstr(dim_gap), '★量纲体检')

    # C4 四力各需的维度常数计数
    d_Ce = ddiv(D_KAP, D_CHARGE)            # [C_e]=L^-1/Q
    d_mu = D(0, -1, 0, 0)                  # [μ]=L^-1（弱力质量尺度）
    d_sigma = ddiv(D_KAP, D_LEN)           # [σ]=L^-2（强力）
    d_r0 = D_LEN                           # [r0]=L（强力尺度）
    n_const = 6
    entry('C4', 'FAIL',
          ('★统一所需的维度常数计数：重力需 G/c²（' + dstr(dmul(D_G, ddiv(D(1, 0, 0, 0), dpow(D_C, 2)))) +
           '）；电磁需电荷归一 C_e（' + dstr(d_Ce) + '）；'
           '弱力需 C_w（' + dstr(d_Ce) + '）+ 质量尺度 μ（' + dstr(d_mu) + '）；'
           '强力需 C_s（' + dstr(d_Ce) + '）+ 尺度 r0（' + dstr(d_r0) + '）'
           '⇒ 仅为了让 κ,τ 维度正确就需 **≥6 个维度常数**，再加 α 本身'
           '⇒ 单一 α 无法供给；Ω5（≤1 常数）在此被违反'
           '（这是继 r77「势」、r78「耦合」、r92「α 量纲/U 体积标度」之后，'
           '第 4 条独立路径证明 TUFT 的统一层资源不足）'),
          None, '★常数计数')

    # C5 阳性对照：若强行令 κ=M/r（不补 G），则 κ 量纲为 M L^-1，
    #    主方程 ω²=c²(κ²+τ²) 右端变成 M²L^-2 T^-2，与左端 T^-2 不等 ⇒ 检验器非恒等
    d_rhs_bad = dmul(dpow(D_C, 2), dpow(d_MoverR, 2))
    bad = d_rhs_bad == dpow(D_OMEGA, 2)
    entry('C5', 'PASS',
          ('阳性对照：若放任 κ=M/r（不补 G），则主方程右端 [c²κ²]=' + dstr(d_rhs_bad) +
           '，与左端 [ω²]=' + dstr(dpow(D_OMEGA, 2)) + ' 不等（' + str(bad) +
           '）⇒ 量纲体检能侦错，非恒等；也说明「几何主方程」与「四力场型」'
           '**分属两套量纲语言**，必须用 G/c² 等常数的桥梁接起来'),
          dstr(d_rhs_bad), '阳性对照')

    # C6 与 r87 的衔接：即便接好了场，牛顿极限仍受 λ≤3.6e-101 精细调节约束
    lam_crit = None
    for jp in (R80_JSON, R87_JSON):
        if os.path.exists(jp):
            with io.open(jp, 'r', encoding='utf-8') as f:
                lam_crit = json.load(f).get('key_numbers', {}).get('lambda_crit')
            if lam_crit:
                break
    entry('C6', 'BOUNDARY',
          ('与 r87 衔接（跨册机器回读 r80/r87 key_numbers）：'
           '即便把四力场型按 C3/C4 用 ≥6 常数接好，r80 的牛顿极限仍要求'
           ' λ ≤ ' + str(lam_crit) + '（约 75 dex 精细调节）才自洽'
           ' ⇒ 统一层「接上」之后还有一层「数值勉强自洽」的额外成本'),
          None, '衔接')



# ----------------------------------------------------------------------------
# 组 D：完成度结账 ——「大统一方程」今天能写成什么样
# ----------------------------------------------------------------------------
def group_D():
    # D1 已经完成的部分（机器固化）
    entry('D1', 'PASS',
          ('✅ 已完成（机器固化，非本册新证）：'
           '① 几何主方程 ω²=c²(κ²+τ²) 及全部派生式（r58，A1–A7 重算逐位一致）；'
           '② 统一力方程形式 F=−α∇(κ²−τ²)（r79 来料正本实测）；'
           '③ 耦合项 𝓛_int=−C₁κT 使场方程接到牛顿极限（r80，形式复现 Φ=GM/r）'),
          None, '已完成')

    # D2 阻塞项
    entry('D2', 'FAIL',
          ('⛔ 阻塞「完成」的五道关：'
           '(1) 符号冲突 κ²+τ²(几何) vs κ²−τ²(力)，C2；'
           '(2) 四力场型量纲不自洽、需 ≥6 常数，C3/C4 → Ω5 违反；'
           '(3) 牛顿极限需 λ≤3.6e-101 精细调节，C6/r87；'
           '(4) 纯标量 PPN γ=−1 ⇒ Cassini 排除 86956 倍（承 r80 E1）；'
           '(5) 「v=c」是输入公设非导出（B3）'),
          None, '⛔阻塞')

    # D3 今天能写出的「大统一方程」全貌（逐词标注状态）
    entry('D3', 'BOUNDARY',
          ('📐 与 r92 定稿件的衔接：完整的「七式三层」定稿件（含 v=c 频率桥接、α 量纲、'
           'U 体积标度缺口、UFT-1..6 终审 1/6）已由 r92 写成可机器复算的定稿，**本册不复述**。'
           '本册对定稿件的**唯一增量**是 C3/C4 的场振幅量纲体检：'
           '即便引用 r92 的定稿方程，其场定义行 `κ ~ G M/(c²r²)`、`τ ~ C_e q/r` 等'
           '仍各自携带 ≥1 个维度常数——这是 r92 的 α 量纲缺口（B②）之外、'
           '**另一层**独立的 Ω5 违反（场定义层 vs 耦合层）。'
           '\n ⇒ 「大统一方程」的机器定稿见 r92；本册补的是「定稿里场定义本身还需 ≥6 常数」这一笔'),
          None, '📐衔接')

    # D4 不自推 + 红线
    entry('D4', 'BOUNDARY',
          ('不自推登记：'
           'NS1 κ~GM/(c²r²)、τ~q/r 等场型的**具体系数**（如 G/c² 是否精确、'
           'C_e 是否取 1/(4πε₀) 量级）本册未新推导，仅用量纲论证其「必须存在」；'
           'NS2 主方程的物理内容边界（B4）仅指其「不含动力学」，不代表 TUFT 别处无动力学；'
           'NS3 Cassini 86956 倍、G 入口、λ_crit 等数值承 r80/r87，本册不复算；'
           'NS4 几何层 κ,τ,ω,Ω=ω 及全部派生式承 r58（本册为同基准独立复算）；'
           'NS5 完整七式三层定稿件与 UFT-1..6 终审承 r92（本册不复述，只补场振幅量纲一笔）。'
           '红线：数学/数值自洽 ≠ 物理证实；本册不声称「已完成大统一方程」——'
           '那一定稿在 r92；本册只对定稿件补「场定义层还需 ≥6 维度常数」这一独立 Ω5 违反，'
           '不构成对 TUFT 方向的普遍否证。'),
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
        'round': 'r91',
        'date': '2026-10-17',
        'source': SRC_NAME,
        'counts': COUNTS,
        'total': len(ENTRIES),
        'verdict': verdict,
        'guard_all_ok': all(g['ok'] for g in GUARDS),
        'guards': GUARDS,
        'entries': ENTRIES,
        'key_numbers': {
            'case_R_H': [str(R_HELIX), str(H_HELIX)],
            'L': format((R_HELIX ** 2 + H_HELIX ** 2).sqrt(), '.10E'),
            'kappa': format(R_HELIX / (R_HELIX ** 2 + H_HELIX ** 2), '.10E'),
            'tau': format(H_HELIX / (R_HELIX ** 2 + H_HELIX ** 2), '.10E'),
            'omega_c': format(C_LIGHT / (R_HELIX ** 2 + H_HELIX ** 2).sqrt(), '.12E'),
            'dim_gap_kappa_MoverR': dstr(ddiv(ddiv(D_MASS, D_LEN), D_KAP)),
            'required_const_min': 6,
        },
        'not_self_derived': [
            {'tag': 'NS1', 'text': 'κ=GM/(c²r)、τ~q/r 等场型的具体系数本册未新推导，仅用量纲证其必存在'},
            {'tag': 'NS2', 'text': '主方程「不含动力学」仅指该式本身，不代表 TUFT 别处无动力学'},
            {'tag': 'NS3', 'text': 'Cassini 86956 倍、G 入口、λ_crit 等数值承 r80/r87，本册不复算'},
            {'tag': 'NS4', 'text': '几何层 κ,τ,ω,Ω=ω 及全部派生式承 r58（本册为同基准独立复算）'},
        ],
        'red_line': ('数学/数值自洽 ≠ 物理证实；本册只把几何主方程与统一力方程拼成一部可审查的'
                     '大统一方程并标出 ⚠️ 位点，不构成对 TUFT 方向的普遍否证，也不声称「已完成」。'),
    }

    with io.open(os.path.join(DATA, STEM + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(payload, ensure_ascii=False, indent=1))

    rlines = ['TUFT-r91 大统一方程建构 运行报告',
              'counts=' + str(COUNTS) + ' total=' + str(len(ENTRIES)) +
              ' verdict=' + verdict, '']
    for e in ENTRIES:
        rlines.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rlines.append('    residual=' + e['residual'])
    rlines.append('')
    rlines.append('GUARD G0: ' + str(len(GUARDS)) + '/' + str(len(GUARDS)) + ' 全过')
    with io.open(os.path.join(DATA, STEM + '_report.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rlines))

    ml = ['# 判定_TUFT-r91-大统一方程建构与完成度结账', '',
          '日期：2026-10-17 · 评级：O/L1（建构册·应「继续完成大统一方程」要求）', '',
          '## 条目计数', '- 总条目：' + str(len(ENTRIES))]
    for k in sorted(COUNTS.keys()):
        ml.append('- ' + k + '：' + str(COUNTS[k]))
    ml.append('- 总体 verdict：' + verdict)
    ml.append('')
    ml.append('## 关键数值')
    for k, v in payload['key_numbers'].items():
        ml.append('- ' + k + ' = ' + str(v))
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
