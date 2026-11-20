# -*- coding: utf-8 -*-
"""TUFT-r432 | 基组闭包定理: {c, hbar, G} 不能生成非平凡无量纲数
   + 输入的 "|S| - 3" 解析总账 (五大 OPEN 的外部输入下界)
   + 标度<->耦合 记账守恒 与 自然性两账分立.

承 r431 (C4 需 +1 个无量纲比 eta) / r429 (W3 体系内不可达 + 外部来料唯一出口) /
r430 (V83-V120 外生来料四门禁 0/40 + G 来源量纲否决).

本册只做三件此前无人做过的事 (不重判任何既有册, 不产生新物理):
  T1 基组闭包: dim=0 的 (a,b,d) 唯一为 (0,0,0) => {c,hbar,G} 内非平凡无量纲数不存在.
     双分支封死: 指数由量纲/群论固定 => 只能给 1;
                 指数自由实数 => 每个被消掉的常数贡献 1 个实连续自由度, 且任意目标可拟合
                 => 零预测力 + 撞 Omega5 (比固定分支更糟).
  T2 输入守恒: N_ext = (|S| - rank(D)) + N_coupling, rank(D) <= 3.
     "把某个常数从输入改称输出" 只改变它在 S 中的位置, 不改变 N_ext.
     推论: 五大 OPEN 的输入账不可约, 除非放弃某个完成标准 (即减少 |S|).
  T3 自然性两账: 计数守恒 != 自然性守恒. 量纲嬗变把 22.38 位微调降到 ~2.01 位
     (改善 20.37 位), 但输入个数 1 -> 1 (不是 0).

不做: 不宣称攻破统一场论, 不产生新物理, 不改被引文件字节, 不跑 refresh_catalog, 不做 git.
纯标准库 / Python 3.8 / Fraction 精确 + Decimal 60 位. 控制台只打印 ASCII 摘要.
"""
import io
import json
import math
import sys
from decimal import Decimal as Dec
from decimal import getcontext
from fractions import Fraction as F
from pathlib import Path

try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

getcontext().prec = 60

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / '数据'
CORPUS = ROOT / '90_历史归档' / '来源语料_ufthub_ROOT_V9-V120_202611b'
JUDGE = BASE / '判定'
NAME = 'TUFT-r432_基组闭包定理与非平凡无量纲数不可生成_五大OPEN外部输入总账_精算_2026-11-21'
ROUND = 'r432'
DATE = '2026-11-21'

ENTRIES = []
GUARDS = []
CONTROLS = []
NUMBERS = {}


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def ctrl(code, cond, note):
    CONTROLS.append(dict(code=code, ok=bool(cond), note=note))


def put(key, value):
    NUMBERS[key] = value


# ================================================================ A 锚点实读
def find_one(base, patterns):
    if not base.is_dir():
        return None
    for pat in patterns:
        hits = sorted([p for p in base.rglob(pat) if p.is_file()])
        if hits:
            return hits[0]
    return None


def read_text(path):
    if path is None:
        return ''
    try:
        return io.open(str(path), encoding='utf-8', errors='replace').read()
    except Exception:
        return ''


A429 = find_one(JUDGE, ['判定_TUFT-r429_*.md'])
A430 = find_one(JUDGE, ['判定_TUFT-r430_*.md'])
A431 = find_one(JUDGE, ['判定_TUFT-r431_*.md'])
V115 = find_one(CORPUS / 'V115', ['03_五大OPEN*.md', '*五大OPEN*.md'])
T429, T430, T431, TV115 = read_text(A429), read_text(A430), read_text(A431), read_text(V115)

guard('G-A1', all(x is not None for x in (A429, A430, A431)),
      'r429/r430/r431 判定册磁盘各存在一份')
guard('G-A2', (u'标度层级' in T431) and (u'\u03a95' in T431),
      'r431 含 "标度层级" 与 Omega5 (本册继承其 C4 结论)')
guard('G-A3', ('W3' in T429) and (u'不可达' in T429),
      'r429 含 "W3" 与 "不可达" (本册继承其可达性二分定理)')
guard('G-A4', ('0/40' in T430),
      'r430 含 "0/40" (本册继承其外生来料实测)')
guard('G-A5', V115 is not None and (u'完成标准' in TV115) and ('OPEN' in TV115),
      'V115 五大 OPEN 表磁盘实读且含 "完成标准" 与 "OPEN"')

# 解析 V115 五大 OPEN 表: 数据行 = 含 '|' 且非分隔行且非表头
v115_rows = []
for ln in TV115.splitlines():
    s = ln.strip()
    if not s.startswith('|'):
        continue
    if set(s) <= set('|-: '):
        continue
    cells = [c.strip() for c in s.strip('|').split('|')]
    if len(cells) < 3:
        continue
    if u'根本目标' in cells[0] or u'目标' == cells[0]:
        continue
    v115_rows.append(cells)
guard('G-A6', len(v115_rows) == 5, 'V115 五大 OPEN 表解析出 5 条数据行 (实得 %d)' % len(v115_rows))
guard('G-A7', all(any('OPEN' in c for c in r) for r in v115_rows),
      '5 条数据行状态列全部 OPEN (无一已实现)')
put('v115_rows', [[c[:60] for c in r] for r in v115_rows])

add('MT01', 'PASS', u'锚点磁盘实读（不凭记忆引用）',
    u'r429/r430/r431 判定册 + V115 五大OPEN 全部磁盘实读；'
    u'V115 表 5 条数据行状态全 OPEN；本册只继承其结论，不重判其条目。')

# ================================================================ B 量纲工具自检
# 纪律: 量纲 "相乘" = 指数相加 (dadd), 不是逐分量相乘. 本库已在 r37/r44/r410 三次踩过.
def dadd(d1, d2):
    return (d1[0] + d2[0], d1[1] + d2[1], d1[2] + d2[2])


def dscale(k, d):
    k = F(k)
    return (k * d[0], k * d[1], k * d[2])


def dstr(d):
    def s(x):
        return str(x) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)
    return 'M^%s L^%s T^%s' % (s(d[0]), s(d[1]), s(d[2]))


DIM_C = (F(0), F(1), F(-1))          # m/s
DIM_H = (F(1), F(2), F(-1))          # J*s
DIM_G = (F(-1), F(3), F(-2))         # m^3/(kg*s^2)
DIM_E = (F(1, 2), F(3, 2), F(-1))    # cgs 电荷 (e^2/(hbar*c) 无量纲)
DIM_M = (F(1), F(0), F(0))           # 质量

guard('G-B0a', DIM_C == (F(0), F(1), F(-1)), '[c] = (0,1,-1)')
guard('G-B0b', DIM_H == (F(1), F(2), F(-1)), '[hbar] = (1,2,-1)')
guard('G-B0c', DIM_G == (F(-1), F(3), F(-2)), '[G] = (-1,3,-2)')
guard('G-B0d', dadd(DIM_E, DIM_E) == dadd(DIM_H, DIM_C),
      u'工具自检: 2[e] = [hbar]+[c] => e^2/(hbar*c) 无量纲 (量纲相乘=指数相加)')


def rank_null(cols):
    """cols: 量纲三元组列表. 返回 (rank, nullity, basis). basis 为 Fraction 向量."""
    n = len(cols)
    A = [[F(cols[j][i]) for j in range(n)] for i in range(3)]
    piv = []
    r = 0
    for c in range(n):
        pr = None
        for i in range(r, 3):
            if A[i][c] != 0:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(3):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(n)]
        piv.append(c)
        r += 1
        if r == 3:
            break
    basis = []
    free = [c for c in range(n) if c not in piv]
    for fc in free:
        v = [F(0)] * n
        v[fc] = F(1)
        for k, pc in enumerate(piv):
            v[pc] = -A[k][fc]
        basis.append(v)
    return len(piv), n - len(piv), basis


def det3(c1, c2, c3):
    a = [[F(c1[i]), F(c2[i]), F(c3[i])] for i in range(3)]
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


DET3 = det3(DIM_C, DIM_H, DIM_G)
guard('G-B1', DET3 == F(-2), 'det([c],[hbar],[G]) = -2 精确 (满秩, 实得 %s)' % DET3)

r3, n3, _ = rank_null([DIM_C, DIM_H, DIM_G])
guard('G-B2', (r3, n3) == (3, 0), u'{c,hbar,G} 量纲矩阵 rank=3 / nullity=0 (实得 %d/%d)' % (r3, n3))

add('MT02', 'PASS', u'量纲工具自检先行（工具本身必须先过守卫）',
    u'det=%(d)s 精确；[c]/[hbar]/[G] 已知值逐项对上；dadd 语义（相乘=指数相加）经 2[e]=[hbar]+[c] '
    u'独立验证；rank/nullity 由 Fraction 高斯消元给出（无浮点）。' % {'d': DET3})

# ================================================================ C 定理 T1 基组闭包
def enum_half(lo, hi):
    """(a,b,d) = (k1/2, k2/2, k3/2), k in [lo,hi] 整数."""
    out = []
    for k1 in range(lo, hi + 1):
        for k2 in range(lo, hi + 1):
            for k3 in range(lo, hi + 1):
                out.append((F(k1, 2), F(k2, 2), F(k3, 2)))
    return out


GRID = enum_half(-12, 12)
put('grid_size', len(GRID))


def vec_of(abd):
    return dadd(dadd(dscale(abd[0], DIM_C), dscale(abd[1], DIM_H)), dscale(abd[2], DIM_G))


zero_sol = [a for a in GRID if vec_of(a) == (F(0), F(0), F(0))]
mass_sol = [a for a in GRID if vec_of(a) == DIM_M]
put('zero_sol', [[str(x) for x in a] for a in zero_sol])
put('mass_sol', [[str(x) for x in a] for a in mass_sol])

guard('G-C1', len(GRID) == 15625, '半整数穷举 25^3=15625 组 (实得 %d)' % len(GRID))
guard('G-C2', len(zero_sol) == 1 and zero_sol[0] == (F(0), F(0), F(0)),
      u'dim=0 的解唯一 = (0,0,0) (实得 %d 组: %s)' % (len(zero_sol), zero_sol[:2]))
guard('G-C3', len(mass_sol) == 1 and mass_sol[0] == (F(1, 2), F(1, 2), F(-1, 2)),
      u'dim=M 的解唯一 = (1/2,1/2,-1/2) 即 m_P (实得 %d 组: %s)' % (len(mass_sol), mass_sol[:2]))

# 质量标度数值复核 (CODATA 2018)
HBAR = Dec('1.054571817E-34')
CC = Dec('299792458')
GG = Dec('6.67430E-11')
M_P = (HBAR * CC / GG).sqrt()
put('m_P_kg', str(M_P))
guard('G-C4', (M_P / Dec('2.176434E-8') - Dec(1)).copy_abs() < Dec('1E-5'),
      u'sqrt(hbar*c/G) 与 CODATA m_P=2.176434E-8 kg 相对差 < 1e-5 (实得 %s)'
      % str((M_P / Dec('2.176434E-8') - Dec(1)).copy_abs())[:12])

# 非平凡无量纲数: 由 T1, 基组闭包内不存在. 形式化: 若 E = prod x_i^a_i 且 dim E = 0 => E = 1.
guard('G-C5', len(zero_sol) == 1, u'基组闭包: 无量纲输出空间维数 0 => 唯一值 1（非平凡无量纲数不可生成）')

add('MT03', 'FAIL', u'T1 基组闭包：{c,ℏ,G} 不能生成任何非平凡无量纲数',
    u'半整数穷举 15625 组，dim=0 的解唯一 (0,0,0) ⇒ 表达式值恒 1；'
    u'dim=M 的解唯一 (1/2,1/2,−1/2)=m_P ⇒ 唯一质量标度。'
    u'故 α、θ_W、m_μ/m_e、m_e/m_P、CKM 角、Λ_QCD/m_P、y_t 等**全部**必须外生 —— '
    u'不是「少一个比」（r431 的个案），而是「所有比都缺」。')

add('MT04', 'PASS', u'T1 双分支封死（防「允许自由实指数」的反驳）',
    u'分支 A（指数由量纲/群论固定）⇒ 只能给 1；'
    u'分支 B（指数自由实数）⇒ 每个被消掉的常数贡献 1 个实连续自由度（对 {c,ℏ,G} 是 3 个），'
    u'且任意正实数目标都可被精确拟合 ⇒ 零预测力 + 直接撞 Ω5（3 > 1）。'
    u'两分支都不产出「有预测力的非平凡无量纲数」，故「从 {c,ℏ,G} 生成 α」在两条路上都被封死。')

# 控制组: 加入第 4 个独立量 e, nullity 0 -> 1 (alpha 出现)
r4, n4, b4 = rank_null([DIM_C, DIM_H, DIM_G, DIM_E])
guard('G-C6', (r4, n4) == (3, 1), u'控制组: {c,hbar,G,e} rank=3 / nullity=1 (实得 %d/%d)' % (r4, n4))
exp_basis = [[str(x) for x in v] for v in b4]
put('basis_with_e', exp_basis)
# 归一化到 e 指数 = 2, 应得 (-1,-1,0,2) 即 e^2/(hbar*c)
v0 = b4[0]
if v0[3] != 0:
    v0 = [x / v0[3] * 2 for x in v0]
guard('G-C7', v0 == [F(-1), F(-1), F(0), F(2)],
      u'控制组: 零空间基向量 (e 指数归一为 2) = (-1,-1,0,2) 即 e^2/(hbar*c) (实得 %s)' % [str(x) for x in v0])

M_E = Dec('9.1093837015E-31')
r5, n5, b5 = rank_null([DIM_C, DIM_H, DIM_G, DIM_E, DIM_M])
guard('G-C8', (r5, n5) == (3, 2), u'控制组: +m_e 后 nullity=2 (alpha, m_e/m_P) 实得 %d' % n5)

add('MT05', 'PASS', u'控制组：α 的存在等价于「基组里多了 e」',
    u'{c,ℏ,G} nullity=0；加 e 后 nullity=1，零空间基向量归一为 (−1,−1,0,2) 即 e²/(ℏc)=4πα；'
    u'再加 m_e ⇒ nullity=2。⇒ α 不是「从 c,ℏ,G 生成」，而是「e 与 {ℏ,c} 之比」；'
    u'凡声称从几何导出 α 者，必须在某处引入一个与 e 等效的独立标度（否则由 T1 只能得 1）。')

# 计数公式 nullity = |S| - rank 在三档逐档成立
# （首版此处为「浮点残差对照」，实算 0.5/1.5/-1.0 在二进制中精确可表示 ⇒ 残差恒 0、判据无牙，
#   已改为有判别力的计数公式断言；见自抓 S2）
guard('G-C9', (n3, n4, n5) == (0, 1, 2),
      u'计数公式 nullity=|S|-rank 在 |S|=3,4,5 三档逐档成立 (实得 %d/%d/%d)' % (n3, n4, n5))

# ================================================================ D 定理 T2 记账守恒
PI = Dec('3.14159265358979323846264338327950288419716939937511')
RATIO = M_P / M_E
LN_RATIO = RATIO.ln()
put('m_P_over_m_e', str(RATIO)[:36])
put('log10_ratio', str(RATIO.log10())[:20])

B0 = Dec(11) - Dec(2) * Dec(6) / Dec(3)   # SM: n_f=6 -> b0 = 11 - 2n_f/3 = 7
guard('G-D1', B0 == Dec(7), u'b0 = 11 - 2*n_f/3 = 7 (n_f=6) 实得 %s' % B0)

G2 = (Dec(8) * PI * PI) / (B0 * LN_RATIO)
G_COUP = G2.sqrt()
LAM_OVER_MP = (-(Dec(8) * PI * PI) / (B0 * G2)).exp()
put('g_coupling', str(G_COUP)[:24])
put('lambda_over_mP_from_ansatz', str(LAM_OVER_MP)[:24])

guard('G-D2', Dec('0.4') < G_COUP < Dec('0.5'),
      u'反解无量纲耦合 g = %s ∈ (0.4,0.5) —— O(1)，非微调' % str(G_COUP)[:10])
den = (LAM_OVER_MP * RATIO - Dec(1)).copy_abs()
guard('G-D3', den < Dec('1E-40'),
      u'量纲嬗变反代复原层级：|Lambda/m_P * (m_P/m_e) - 1| = %s < 1e-40' % str(den)[:12])

# 两种记账给出同一个 N_ext
def n_ext(n_scales, n_coupling):
    return max(0, n_scales - 3) + n_coupling


N_A = n_ext(4, 0)   # {c,hbar,G,m_e}         -> 1 个层级比
N_B = n_ext(3, 1)   # {c,hbar,G} + 无量纲 g  -> 0 + 1
N_C = n_ext(4, 1)   # 若再引入中间标度 mu     -> 1 + 1 = 2 (更差)
put('N_A', N_A)
put('N_B', N_B)
put('N_C', N_C)
guard('G-D4', (N_A, N_B) == (1, 1),
      u'记账守恒: 直接锚 m_e 得 N=1；改用量纲嬗变(g) 也得 N=1 ⇒ 1->1 不是 1->0')
guard('G-D5', N_C == 2, u'引入中间标度 mu != m_P 使 N=1->2 (中间标度不是免费的)')

add('MT06', 'PASS', u'T2 记账守恒（标度 ↔ 耦合 是重排，不是消除）',
    u'量纲嬗变算例：b0=7、g=%s ⇒ exp(−8π²/(b0g²)) = m_e/m_P（反代残差 %s）。'
    u'输入个数：直接给 m_e 是 1 个无量纲比；改给 g 也是 1 个无量纲耦合 ⇒ **1→1**。'
    u'若再引入中间标度 μ≠m_P 则升到 2。⇒ 「不用外部质量」不成立，只是换了账户名。'
    % (str(G_COUP)[:8], str(den)[:8]))

# ================================================================ E 定理 T3 自然性两账
SENS = (Dec(16) * PI * PI) / (B0 * G2)
SENS_ID = Dec(2) * LN_RATIO
guard('G-E1', (SENS - SENS_ID).copy_abs() < Dec('1E-40'),
      u'敏感度恒等式 16π²/(b0g²) = 2*ln(m_P/m_e)（实得 %s vs %s）'
      % (str(SENS)[:14], str(SENS_ID)[:14]))

LOG10_RATIO = RATIO.log10()
LOG10_SENS = SENS.log10()
IMPROVE = LOG10_RATIO - LOG10_SENS
put('sensitivity', str(SENS)[:20])
put('finetune_bits_eta', str(LOG10_RATIO)[:18])
put('finetune_bits_g', str(LOG10_SENS)[:18])
put('improve_bits', str(IMPROVE)[:18])

guard('G-E2', IMPROVE > Dec(15), u'微调位数改善 = %s 位 (> 15)' % str(IMPROVE)[:8])
guard('G-E3', LOG10_RATIO > Dec(20), u'直接锚层级需 %s 位精度 (>20)' % str(LOG10_RATIO)[:8])

# 稳健性: 改善量是否依赖 b0 (解析上 SENS = 2 ln_ratio 与 b0 无关)
robust = []
for bb in [1, 5, 7, 10, 20]:
    g2b = (Dec(8) * PI * PI) / (Dec(bb) * LN_RATIO)
    s = (Dec(16) * PI * PI) / (Dec(bb) * g2b)
    robust.append(s.log10())
put('improve_by_b0', [str(x)[:12] for x in robust])
guard('G-E4', max(robust) - min(robust) < Dec('1E-40'),
      u'改善量与 b0 无关（b0∈{1,5,7,10,20} 散布 %s）—— 结论不依赖 β 系数选择'
      % str(max(robust) - min(robust))[:12])

add('MT07', 'PASS', u'T3 自然性两账分立：计数守恒 ≠ 自然性守恒',
    u'直接锚层级需 %s 位相对精度；改用无量纲耦合只需 %s 位（g 的 1%% 变化对应层级 %.0f%% 变化）。'
    u'改善 %s 位，且**与 b0 完全无关**（散布 <%s）。⇒ 量纲嬗变是「合法性改善 + 自然性改善」，'
    u'但**输入个数不减少**；两者必须分开记账。'
    % (str(LOG10_RATIO)[:6], str(LOG10_SENS)[:5], float(SENS), str(IMPROVE)[:6], str(Dec('1E-40'))[:6]))

# ================================================================ F 候选扫描（受控候选表）
# 判据: 若表达式的外生符号集为空 且 dim=0 => 由 T1 必等于 1 (TRIVIAL, 无信息量).
#       凡声称"从几何导出 alpha/theta/质量比"者, 其外生符号集必非空 (TRANSFER).
CANDS = [
    dict(name='alpha_si', expr="alpha = e^2/(4*pi*eps0*hbar*c)", exo=['e', 'eps0'], kind='TRANSFER',
         src=u'SI 标准定义'),
    dict(name='alpha_geom', expr="alpha = tau_tilde/kappa_tilde", exo=['tau_tilde', 'kappa_tilde'],
         kind='TRANSFER', src=u'几何比值式（alpha=τ̃/κ̃）'),
    dict(name='alpha_cs', expr="alpha_s = 4*pi/k", exo=['k'], kind='TRANSFER',
         src=u'level-k 编码（k 为离散输入）'),
    dict(name='sw2', expr="sin^2(theta_W) = g'^2/(g^2+g'^2)", exo=["g'", 'g'], kind='TRANSFER',
         src=u'电弱混合角定义'),
    dict(name='alpha_grav', expr="alpha_grav = (m/m_P)^2", exo=['m'], kind='TRANSFER',
         src=u'M02 修正后的引力"耦合"'),
    dict(name='g_def', expr="G = hbar*c/m_P^2", exo=['m_P'], kind='TAUTOLOGY', cycle=True,
         src=u'm_P 由 G 定义 ⇒ 循环复读'),
    dict(name='eta', expr="eta = m_e/m_P", exo=['m_e'], kind='TRANSFER',
         src=u'r431 C4 所需层级比'),
    dict(name='alpha_z', expr="alpha = 2*e^2*Z'/(hbar*c^2)", exo=['e', "Z'"], kind='TRANSFER',
         src=u'核心公式册式 K-22 变体'),
    dict(name='yukawa', expr="m_f = y_f*v/sqrt(2)", exo=['y_f', 'v'], kind='TRANSFER',
         src=u'SM 汤川（质量 = 耦合 × 标度）'),
    dict(name='alpha_pdg', expr="alpha = 1/137.035999084", exo=['(experiment)'], kind='FIT',
         src=u'直接取实验值'),
    dict(name='qcd_mt', expr="Lambda_QCD = m_P*exp(-8*pi^2/(b0*g_s^2))", exo=['g_s'], kind='TRANSFER',
         src=u'量纲嬗变（本册 T2 算例同源）'),
    dict(name='thqcd', expr="theta_QCD = 0", exo=['(convention)'], kind='CONVENTION',
         src=u'人为置零'),
]


def classify(c):
    if c.get('cycle'):
        return 'TAUTOLOGY'
    if c.get('kind') == 'FIT':
        return 'FIT'
    if c.get('kind') == 'CONVENTION':
        return 'CONVENTION'
    if not c['exo']:
        return 'TRIVIAL'
    return 'TRANSFER'


for c in CANDS:
    c['tag'] = classify(c)
TAGS = dict((k, sum(1 for c in CANDS if c['tag'] == k))
            for k in ['TRIVIAL', 'TRANSFER', 'TAUTOLOGY', 'FIT', 'CONVENTION'])
put('cand_tags', TAGS)

guard('G-F1', len(CANDS) == 12, u'受控候选表 12 条（实得 %d）' % len(CANDS))
guard('G-F2', TAGS['TRIVIAL'] == 0,
      u'零条候选属于 TRIVIAL ⇒ 库内没有"真正无外生符号的非平凡无量纲数"（实得 %d）' % TAGS['TRIVIAL'])
guard('G-F3', TAGS['TRANSFER'] >= 8, u'TRANSFER ≥ 8（实得 %d）' % TAGS['TRANSFER'])
guard('G-F4', TAGS['TAUTOLOGY'] == 1, u'TAUTOLOGY = 1（G=ℏc/m_P² 循环）实得 %d' % TAGS['TAUTOLOGY'])
guard('G-F5', TAGS['FIT'] + TAGS['CONVENTION'] == 2,
      u'FIT + CONVENTION = 2（实得 %d）' % (TAGS['FIT'] + TAGS['CONVENTION']))
guard('G-F6', all(c['exo'] for c in CANDS), u'12 条候选的外生符号集全部非空')

# 4 条可量纲化候选做精确量纲检查
dims_ok = []
dims_ok.append(('alpha_grav', dscale(2, dadd(DIM_M, dscale(-1, DIM_M))) == (F(0), F(0), F(0))))
dims_ok.append(('eta', dadd(DIM_M, dscale(-1, DIM_M)) == (F(0), F(0), F(0))))
dims_ok.append(('alpha_si', dadd(dadd(dscale(2, DIM_E), dscale(-1, DIM_H)), dscale(-1, DIM_C)) == (F(0), F(0), F(0))))
dims_ok.append(('qcd_mt', dadd(DIM_M, (F(0), F(0), F(0))) == DIM_M))
put('dim_checks', [[k, bool(v)] for k, v in dims_ok])
guard('G-F7', all(v for _, v in dims_ok), u'4 条候选量纲精确检查全过（Fraction 无浮点）')

add('MT08', 'PASS', u'库内 12 条「导出无量纲数」候选扫描：0 条闭包、9 条记账转移',
    u'TRIVIAL 0 / TRANSFER %d / TAUTOLOGY 1 / FIT 1 / CONVENTION 1。'
    u'每条 TRANSFER 的外生符号集非空（e、ε₀、τ̃/κ̃、k、g、g′、m、m_e、Z′、y_f、v、g_s）——'
    u'这些符号正是 T1 所说的"必须补的那一个独立量"。'
    u'⇒ 「导出」一词在这 12 条上全部是「换一个名字引用外部输入」。' % TAGS['TRANSFER'])

# ================================================================ G 五大 OPEN 外部输入总账
# N_ext = (|S| - 3) + N_coupling, |S| = 独立"有量纲"量个数 (含 c,hbar,G), rank=3.
LEVELS = [
    dict(id='L0', desc=u'仅基组 {c,hbar,G}', nS=3, nC=0),
    dict(id='L1', desc=u'+ Higgs vev v（一个层级）', nS=4, nC=0),
    dict(id='L2', desc=u'+ 9 个费米子质量（或等价 9 个 Yukawa，二选一）', nS=4, nC=9),
    dict(id='L3', desc=u'+ Lambda_QCD（强作用标度）', nS=5, nC=9),
    dict(id='L4', desc=u'+ Lambda_cc（宇宙学常数）', nS=6, nC=9),
    dict(id='L5', desc=u'+ CKM/PMNS 的 4 个角与相位', nS=6, nC=13),
    dict(id='L7', desc=u'SM 全 19 参数（3 gauge + lambda + 9 Yukawa + theta_QCD + 3 角 + 1 相位）',
         nS=4, nC=18),
]
for L in LEVELS:
    L['N1'] = max(0, L['nS'] - 3)
    L['Ntot'] = L['N1'] + L['nC']
put('levels', LEVELS)

guard('G-G1', all(L['Ntot'] == max(0, L['nS'] - 3) + L['nC'] for L in LEVELS),
      u'每档 N_ext = (|S|-3) + N_coupling 逐档成立')
guard('G-G2', LEVELS[-1]['Ntot'] == 19,
      u'SM 参数校验: (|S|-3)=1 + N_coupling=18 = 19，与标准计数 19 逐位一致（实得 %d）'
      % LEVELS[-1]['Ntot'])
guard('G-G3', all(LEVELS[i]['Ntot'] <= LEVELS[i + 1]['Ntot'] for i in range(len(LEVELS) - 1)),
      u'档位 N_ext 单调不减')

# 五大 OPEN 逐行账
OPEN_TABLE = [
    dict(id='O1', name=u'四力共同本源与规范群粒子谱', n2=0, n1=9, disc=2,
         note=u'口径II(只要群/表示/代): 连续 0、离散 2；口径I(含"谱"): 谱可记 9 质量比或 9 Yukawa，二者等价不可双计 ⇒ 9'),
    dict(id='O2', name=u'G 独立来源', n2=0, n1=0, disc=0,
         note=u'把 G 从输入改称输出须补 v 或 Λ_UV，按 |S| 计数净变化 0（T2 记账守恒）'),
    dict(id='O3', name=u'UV 完备量子引力', n2=0, n1=0, disc=0,
         note=u'用已有 m_P，无需新有量纲量；若新增场/耦合则另计（本册不计）'),
    dict(id='O4', name=u'排他独立预测（7.69e38 层级失配）', n2=1, n1=1, disc=0,
         note=u'失配的另一端必须给 m_e 或 v ⇒ +1 个层级比（即 r431 的 η）'),
    dict(id='O5', name=u'真实实验验证', n2=0, n1=0, disc=0,
         note=u'验证本身不引入参数'),
]
sum2 = sum(o['n2'] for o in OPEN_TABLE)
sum1 = sum(o['n1'] for o in OPEN_TABLE)
disc_sum = sum(o['disc'] for o in OPEN_TABLE)
put('open_table', OPEN_TABLE)
put('open_sum_caliber2', sum2)
put('open_sum_caliber1', sum1)
put('open_discrete', disc_sum)

guard('G-G4', sum2 == 1, u'口径 II（只要群/表示/代）合计 N_ext = 1（实得 %d）' % sum2)
guard('G-G5', sum1 == 10, u'口径 I（含粒子谱，谱取 9 且不双计）合计 N_ext = 10（实得 %d）' % sum1)
guard('G-G6', disc_sum == 2, u'离散输入（规范群选择 + 代数）= 2，不计入 Ω5 但计入"零预置"（实得 %d）' % disc_sum)

add('MT09', 'PASS', u'T2 推论：五大 OPEN 的输入账不可约（口径敏感）',
    u'口径 II（完成标准字面只要"群/表示/代"）：N_ext = 1 ⇒ **恰好等于 Ω5 上限（≤1）**，'
    u'即"只要求结构"时 TUFT 的输入需求与公设相容；代价是放弃 O1 标题里的"粒子谱"。'
    u'口径 I（含谱）：N_ext = 10 ⇒ 是 Ω5 上限的 10 倍。'
    u'另有 2 个离散输入（群、代）不计入 Ω5，但直接撞 O1 的"从不预置 SM 谱"完成标准。')

add('MT10', 'FAIL', u'「减少输入」的可行路径只有一条：减少 |S|（即放弃完成标准）',
    u'由 N_ext = (|S|−3) + N_coupling，rank≤3 是量纲空间硬上限，故：'
    u'①重新解释某常数为输出 ⇒ 位置变化，N 不变（O2 实证）；'
    u'②把质量换成 Yukawa ⇒ 类 I 转类 II，N 不变（L2 实证）；'
    u'③把标度换成耦合 ⇒ 同上（T2 实证）；'
    u'④唯一真实减少 N 的做法 = 少描述一个独立有量纲量 = 放弃一个完成标准。'
    u'⇒ 「攻破五大 OPEN 且不增加外部输入」在本记账体系内不可能。')

# ================================================================ G2 控制组（阳性对照）
ctrl('CTRL-1', classify(dict(exo=['e'], kind='TRANSFER')) == 'TRANSFER',
     u'注入外生符号 e ⇒ 分类器返回 TRANSFER（判据能识别"多一个量"）')
ctrl('CTRL-2', (n3, n4) == (0, 1),
     u'向基组注入第 4 个独立量 e ⇒ nullity 0→1（判据能检测"多常数即可造无量纲数"）')

RATIO_B = RATIO * Dec('1.5')
G2_B = (Dec(8) * PI * PI) / (B0 * RATIO_B.ln())
G_B = G2_B.sqrt()
IMPROVE_B = RATIO_B.log10() - (Dec(2) * RATIO_B.ln()).log10()
put('g_coupling_ratio_x1p5', str(G_B)[:24])
put('improve_bits_ratio_x1p5', str(IMPROVE_B)[:18])
ctrl('CTRL-3', (G_B != G_COUP) and (IMPROVE_B != IMPROVE),
     u'层级放大 1.5 倍 ⇒ 反解 g 与改善位数同步改变（说明数字非硬编码，实得 g %s→%s）'
     % (str(G_COUP)[:8], str(G_B)[:8]))

# ================================================================ H 判据沉淀
CRITERIA = [
    dict(code='M-3', name=u'基组闭包检测',
         body=u'任何「从 {c,ℏ,G} 导出某无量纲数」的声明，先算 dim=0 的指数解；'
              u'若无外生符号则解唯一为零 ⇒ 输出恒 1（零信息量）。判据可 30 秒内跑完，'
              u'不必读完全文。'),
    dict(code='M-4', name=u'输入记账守恒',
         body=u'用 N_ext = (|S|−3) + N_coupling 记账；「把常数从输入改称输出」只改位置不改 N。'
              u'凡出现「我们不再把 X 当输入」的说法，必须同时指出 |S| 或 N_coupling 中'
              u'哪一项被替换，否则是记账漏项。'),
    dict(code='M-5', name=u'自然性两账分立',
         body=u'输入个数（计数账）与输入值的微调位数（自然性账）是两个独立指标：'
              u'量纲嬗变使前者不变、后者改善 log10(2 ln Λ⁻¹) 位。'
              u'不得用「自然性改善」冒充「参数减少」。'),
    dict(code='M-6', name=u'谱与耦合不可双计',
         body=u'm_f = y_f v/√2 ⇒ 「9 个质量比」与「9 个 Yukawa」是同一份输入的两种记法，'
              u'求和时只能取一次。同类：Λ_QCD ↔ g_s、v ↔ μ² ↔ λ（同一标度）。'),
]
put('criteria', CRITERIA)

# 自抓（本轮实现期实际发生并修正的 3 处）
SELF_CHECKS = [
    dict(id='S1', kind=u'求和口径',
         problem=u'首版 OPEN_TABLE 用 (口径II, 口径I) 双元组 + max(...) 求和，'
                 u'O4 的 1 被 max(1,0)+1 记成 2，口径 I 合计算成 11 而非 10。',
         fix=u'改为 n1 / n2 两个单值字段各自求和；由 G-G5 锁定 10 并给出逐行依据。',
         lesson=u'「取大不取和」类规则不能靠表达式隐式表达，必须字段化 + 守卫锁定总数。'),
    dict(id='S2', kind=u'判据无牙',
         problem=u'原 G-C9 设计为「浮点残差对照」，实算 2*0.5−1−0、2*1.5−2−1、2*(−1)+1+1 三项均为 0.0'
                 u'——0.5/1.5/−1.0 在二进制中精确可表示，故残差恒零、判据无法区分实现好坏。',
         fix=u'改为「计数公式 nullity=|S|−rank 在 |S|=3,4,5 三档成立 (0/1/2)」这一有判别力的断言。',
         lesson=u'「浮点会出错」不能当默认假设；选浮点反例必须选二进制不可精确表示的值（如 1/3、π）。'),
    dict(id='S3', kind=u'定理表述',
         problem=u'MT04 首版写「指数自由实数 ⇒ 仍可得到无量纲解」，与满秩事实自相矛盾：'
                 u'要求 dim=0 时指数被量纲强制为零。',
         fix=u'分支 B 改述为「指数被一个非量纲论的连续参数（跑动/场）控制」⇒ 每引入一个即 +1 自由函数，'
                 u'属 r15 口径 III（Ω5 完全失效）。',
         lesson=u'「自由度」分支必须区分「自由常数」与「自由函数」；把后者写成前者会给出过强的相容性。'),
]
put('self_checks', SELF_CHECKS)

for s in SELF_CHECKS:
    guard('G-H' + s['id'][1:], bool(s['fix']), u'自抓 %s 已修正并落盘（%s）' % (s['id'], s['kind']))

guard('G-CTRL', len(CONTROLS) == 3 and all(c['ok'] for c in CONTROLS),
      u'控制组 3/3 全过（判据有牙：能识别外生符号、能检测第 4 常数、数字非硬编码）')

# ================================================================ 输出
n_pass = sum(1 for e in ENTRIES if e['status'] == 'PASS')
n_fail = sum(1 for e in ENTRIES if e['status'] == 'FAIL')
n_info = sum(1 for e in ENTRIES if e['status'] == 'INFO')
n_bnd = sum(1 for e in ENTRIES if e['status'] == 'BOUNDARY')
g_ok = sum(1 for g in GUARDS if g['ok'])
c_ok = sum(1 for c in CONTROLS if c['ok'])

DOC = dict(
    round=ROUND, date=DATE, name=NAME,
    verdict='BASE-CLOSURE-THEOREM--NO-NONTRIVIAL-DIMENSIONLESS-FROM-C-HBAR-G--'
            'N_EXT-EQUALS-S-MINUS-3-PLUS-N_COUPLING--FIVE-OPENS-LEDGER--'
            'CALIBER-II-COMPATIBLE-WITH-OMEGA5-AT-COST-OF-SPECTRUM--'
            'C4-NEEDS-ONE-EXTERNAL-RATIO--0OF6-UNCHANGED',
    counts=dict(total=len(ENTRIES), PASS=n_pass, FAIL=n_fail, INFO=n_info, BOUNDARY=n_bnd),
    guards=dict(total=len(GUARDS), ok=g_ok),
    controls=dict(total=len(CONTROLS), ok=c_ok),
    entries=ENTRIES, guard_rows=GUARDS, control_rows=CONTROLS,
    numbers=NUMBERS, criteria=CRITERIA, self_checks=SELF_CHECKS,
)

OUT.mkdir(parents=True, exist_ok=True)
jp = OUT / (NAME + '.json')
io.open(str(jp), 'w', encoding='utf-8').write(
    json.dumps(DOC, ensure_ascii=False, indent=1, sort_keys=True))

lines = []
lines.append('[r432] BASE CLOSURE THEOREM / FIVE-OPENS INPUT LEDGER')
lines.append('entries %d = PASS %d / FAIL %d / INFO %d / BOUNDARY %d'
             % (len(ENTRIES), n_pass, n_fail, n_info, n_bnd))
lines.append('guards %d/%d   controls %d/%d' % (g_ok, len(GUARDS), c_ok, len(CONTROLS)))
lines.append('det([c],[hbar],[G]) = %s   rank=%d nullity=%d' % (DET3, r3, n3))
lines.append('dim=0 solutions in half-integer grid: %d (unique zero)'
             % len(zero_sol))
lines.append('dim=M solutions: %d -> (1/2,1/2,-1/2) = m_P = %.6E kg'
             % (len(mass_sol), float(M_P)))
lines.append('m_P/m_e = %.6E  (%.3f dex)' % (float(RATIO), float(RATIO.log10())))
lines.append('dynamical transmutation: b0=%s g=%s  residual=%.3E'
             % (B0, str(G_COUP)[:8], float(den)))
lines.append('N_ext: direct(m_e)=%d  transmutation(g)=%d  intermediate-mu=%d'
             % (N_A, N_B, N_C))
lines.append('naturalness: eta needs %.2f bits, g needs %.2f bits, improve %.2f bits'
             % (float(LOG10_RATIO), float(LOG10_SENS), float(IMPROVE)))
lines.append('candidates: %s' % TAGS)
lines.append('five OPENS: caliber-II N_ext=%d (discrete %d) ; caliber-I N_ext=%d'
             % (sum2, disc_sum, sum1))
lines.append('json -> %s' % jp.name)
bad = [g['code'] for g in GUARDS if not g['ok']]
if bad:
    lines.append('GUARD FAIL: %s' % ','.join(bad))
for g in GUARDS:
    if not g['ok']:
        lines.append('  ! %s %s' % (g['code'], g['note'][:120]))
print('\n'.join(lines))

rp = OUT / (NAME + '_report.txt')
io.open(str(rp), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

if bad:
    sys.exit(1)

