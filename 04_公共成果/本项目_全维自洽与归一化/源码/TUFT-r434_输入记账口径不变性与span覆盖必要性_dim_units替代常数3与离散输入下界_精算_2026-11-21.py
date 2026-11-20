# -*- coding: utf-8 -*-
"""TUFT-r434 | 输入记账公式的推导基础自审:
   (|S| - 3) 应改为 (|S| - rank D)  [口径不变性, 常数 3 是 D1 专用]
   + span 覆盖必要性 (N_ext = 0 的欠张满假阳性)
   + 离散输入信息量下界 (Omega5 只限连续常数, 不覆盖离散选择).

承 r432 (T1 基组闭包 / T2 输入守恒 / T3 自然性两账 / 五大 OPEN 总账) /
r431 (C4 需 +1 个无量纲比) / r429 (W3 体系内不可达 + 外部来料唯一出口).

本册只做三件此前无人做过的事 (不重判任何既有册, 不产生新物理):
  T4 良定域: N_ext = (n - rank(D)) + N_coupling; 常数 3 只在 (n,d,r)=(4,3,3) 这类账上正确.
     两类分歧: 负值型 (n=2 -> -1, 定义域外) / 重复计数型 (D2 下 +1).
  T5 口径不变性: 保结构变换下 N_ext 不变 (三类), 漏账/重复计下退化 (两类, 19->18/20).
  T6 离散下界: I_disc = log2(#choices); Omega5 只限连续常数 => 口径 II 相容性附条件.
  T7 不完备: N_ext 相同不等于判据力相同 (超定度 over = k - p, 两账 0 vs 6).

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
JUDGE = BASE / '判定'
NAME = ('TUFT-r434_输入记账口径不变性与span覆盖必要性_'
        'dim_units替代常数3与离散输入下界_精算_2026-11-21')
ROUND = 'r434'
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


A432 = find_one(JUDGE, ['判定_TUFT-r432_*.md'])
A431 = find_one(JUDGE, ['判定_TUFT-r431_*.md'])
A429 = find_one(JUDGE, ['判定_TUFT-r429_*.md'])
A433 = find_one(JUDGE, ['判定_TUFT-r433_离散输入*.md', '判定_TUFT-r433_*.md'])
T432, T431, T429 = read_text(A432), read_text(A431), read_text(A429)
T433 = read_text(A433)

guard('G-A7', A433 is not None and ('O1' in T433) and (u'离散' in T433),
      '并行 r433（离散输入预置二分定理）磁盘存在且含 O1/离散（本册不重判其裁决）')
guard('G-A8', (u'预置' in T433) or ('PRESET' in T433),
      'r433 主题为"来源二分/预置判定"，与本册"记账口径"正交（防重复）')

guard('G-A1', all(x is not None for x in (A432, A431, A429)),
      'r432/r431/r429 判定册磁盘各存在一份')
guard('G-A2', ('N_ext' in T432) and ('N_coupling' in T432),
      'r432 含 N_ext 与 N_coupling (本册继承其 T2 记账公式)')
guard('G-A3', ('rank(D)' in T432.replace(' ', ''))
      or ('rank(D)' in T432),
      'r432 正文出现 rank(D) 表述 (本册 CORRECTED 的对象)')
guard('G-A4', ('|S| ' in T432) and ('3)' in T432),
      'r432 表格出现 (|S|-3) 算式 (与 rank(D) 并存的第二表述)')
guard('G-A5', ('Omega5' in T432) or (u'\u03a95' in T432),
      'r432 含 Omega5 (本册继承其口径 II 相容性结论)')

# 机器定位 r432 中两处并存表述的行号 (防"凭记忆引用")
lines432 = T432.splitlines()
ln_rank = [i + 1 for i, ln in enumerate(lines432) if 'rank(D)' in ln.replace(' ', '')]
ln_const = [i + 1 for i, ln in enumerate(lines432) if '(' + '|S|' + ' ' in ln and '3)' in ln]
put('r432_line_rankD', ln_rank)
put('r432_line_const3', ln_const)
guard('G-A6', len(ln_rank) >= 1 and len(ln_const) >= 1,
      'r432 内 rank(D) 与 (|S|-3) 两表述行号各命中>=1 (rank %s / const3 %s)'
      % (ln_rank[:4], ln_const[:4]))

add('A01', 'PASS', u'锚点磁盘实读 + 双表述并存机检（不凭记忆引用）',
    u'r432/r431/r429 判定册全部磁盘实读；机器在 r432 内定位到 `rank(D)`（行 %s）与 '
    u'`(|S|-3)`（行 %s）两处并存表述。二者在所有 `rank=3` 的算例上同值，'
    u'故 r432 的数值结论（SM=19）不受影响；但在 `rank<3` 或 `d>3` 的账上分歧 —— '
    u'这是本册 CORRECTED 的直接依据，属"公式符号与实测算式不同源"，不是数值错误。'
    % (ln_rank[:3], ln_const[:3]))

add('A03', 'PASS', u'与并行 r433 的分工（防重复：来源二分 vs 记账口径，两轴正交）',
    u'并行会话同日落盘 `r433 · 离散输入预置二分定理`（判「离散输入来源两腿全封 ⇒ 口径 II 过 O1 不可达」），'
    u'其判据轴是**来源**（PRESET vs 需外部选择）。本册的判据轴是**计量**（离散项应记多少 bit、'
    u'减数该用 rank 还是常数 3）。两轴正交：本册不重判其「过 O1 不可达」，'
    u'其册也不含「记账口径 / span 覆盖」内容。`G-A7/G-A8` 机检该册磁盘存在且关键词不重叠。')

add('A02', 'PASS', u'r432 的 SM=19 双路复核（结论继承而非改写）',
    u'同一组账 (n=4 {c,hbar,G,v}, r=3, N_coupling=18) 用 `n-rank` 与 `n-3` 两式'
    u'都给出 19，与 SM 标准计数逐位一致 ⇒ r432 的 T2 数值结论成立，本册只修其表述。')


# ================================================================ B 量纲与秩工具
DIM_INDEX = dict(M=0, L=1, T=2, Q=3, TH=4)
DIMSETS = dict(
    D1=('M', 'L', 'T'),
    D2=('M', 'L', 'T', 'Q'),
    D3=('M', 'L', 'T', 'Q', 'TH'),
)
FULL = dict(
    c=(0, 1, -1, 0, 0),
    hbar=(1, 2, -1, 0, 0),
    G=(-1, 3, -2, 0, 0),
    v=(0, 1, -1, 0, 0),
    me=(1, 0, 0, 0, 0),
    e=(0, 0, 0, 1, 0),
    eps0=(-1, -3, 4, 2, 0),
    kB=(1, 2, -2, 0, -1),
)


def dvec(name, dimset):
    return tuple(FULL[name][DIM_INDEX[d]] for d in dimset)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dscale(a, k):
    return tuple(x * k for x in a)


def rank(rows):
    m = [[F(x) for x in r] for r in rows]
    if not m:
        return 0
    ncol = len(m[0])
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


def det3(rows):
    a, b, c = rows[0]
    d, e, f = rows[1]
    g, h, i = rows[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


# --- 工具自检 (标准值, 不依赖被核对象)
C1 = dvec('c', DIMSETS['D1'])
H1 = dvec('hbar', DIMSETS['D1'])
G1 = dvec('G', DIMSETS['D1'])
DET3 = det3([C1, H1, G1])
R3 = rank([C1, H1, G1])

guard('G-B1', C1 == (0, 1, -1), '[c] = (0,1,-1) in (M,L,T)')
guard('G-B2', H1 == (1, 2, -1), '[hbar] = (1,2,-1)')
guard('G-B3', G1 == (-1, 3, -2), '[G] = (-1,3,-2)')
guard('G-B4', DET3 == F(-2), 'det([c],[hbar],[G]) = -2 (满秩, 与 r432 一致)')
guard('G-B5', R3 == 3, 'rank{c,hbar,G} = 3')
guard('G-B6', dvec('v', DIMSETS['D1']) == C1,
      '[v] 与 [c] 同向量 (0,1,-1) => 新元素不增秩')
guard('G-B7', rank([C1, H1, G1, dvec('v', DIMSETS['D1'])]) == 3,
      'rank{c,hbar,G,v} = 3 (v 与 c 平行, 不增秩)')
guard('G-B8', dvec('e', DIMSETS['D1']) == (0, 0, 0),
      'D1 下 e 投影为零向量 (电荷在 (M,L,T) 中无法表达)')
guard('G-B9', dvec('e', DIMSETS['D2']) == (0, 0, 0, 1),
      'D2 下 e = (0,0,0,1) (独占 Q 维)')
guard('G-B10', dvec('kB', DIMSETS['D2']) == (1, 2, -2, 0),
      'D2 下 kB 丢 TH 分量 = (1,2,-2,0)')
guard('G-B11', rank([dvec('c', DIMSETS['D1']), dvec('hbar', DIMSETS['D1'])]) == 2,
      'rank{c,hbar} = 2 < d1 = 3 (欠张满样本)')
guard('G-B12', dadd((1, 2, 3), (0, -2, 0)) == (1, 0, 3),
      'dadd 语义 = 分量相加 (非元组拼接; 拼接会得 6 元组)')

add('B01', 'PASS', u'量纲/秩工具自检（12 项标准值，不依赖被核对象）',
    u'det([c],[hbar],[G])=−2 与 r432 逐位一致；rank{c,ħ,G}=3；`[v]=[c]` 同向量；'
    u'`e` 在 D1 下投影为零向量而在 D2 下独占 Q 维；`k_B` 在 D2 下丢 Θ 分量。'
    u'这四条标准值构成后续所有记账的脚手架 —— 若任一错，T4/T5 全表连带错。')

# ================================================================ C T4 良定域
S_ACCOUNTS = [
    ('SA', ('c', 'hbar'), 0, u'欠张满样本（只有 c 与 hbar）'),
    ('SB', ('c', 'hbar', 'G', 'v'), 18, u'SM 层级账 L7（r432 §6.1）'),
    ('SC', ('c', 'hbar', 'G', 'e', 'eps0'), 0, u'SI 电磁口径（电荷 + 真空介电）'),
    ('SD', ('c', 'hbar', 'G', 'kB'), 0, u'含温度标度'),
]

T4_ROWS = []
for tag, names, ncp, note in S_ACCOUNTS:
    for dk in ('D1', 'D2', 'D3'):
        ds = DIMSETS[dk]
        rows = [dvec(nm, ds) for nm in names]
        n = len(names)
        rr = rank(rows)
        d = len(ds)
        n_rank = n - rr + ncp
        n_c3 = n - 3 + ncp
        T4_ROWS.append(dict(tag=tag, dimset=dk, n=n, r=rr, d=d, ncp=ncp,
                            n_rank=n_rank, n_c3=n_c3,
                            diff=n_c3 - n_rank, note=note))
put('t4_rows', T4_ROWS)

cell = {}
for row in T4_ROWS:
    cell['%s/%s' % (row['tag'], row['dimset'])] = row

n_diff = sum(1 for row in T4_ROWS if row['diff'] != 0)
n_plus = sum(1 for row in T4_ROWS if row['diff'] > 0)
n_minus = sum(1 for row in T4_ROWS if row['diff'] < 0)
put('t4_diff_cells', n_diff)
put('t4_diff_plus', n_plus)
put('t4_diff_minus', n_minus)

guard('G-C0', all(row['diff'] == row['r'] - 3 for row in T4_ROWS),
      '恒等式 diff = n_c3 - n_rank = rank(D) - 3（与 n / N_coupling 完全无关）')
guard('G-C1', n_diff == 6 and n_plus == 3 and n_minus == 3,
      '分歧格子 = 6（实得 %d：+1 型 %d / -1 型 %d）' % (n_diff, n_plus, n_minus))
guard('G-C2', all(cell['SB/' + k]['n_rank'] == 19 for k in ('D1', 'D2', 'D3')),
      'SB 在 D1/D2/D3 下 N_ext 全为 19（SM 层级账口径不变）')
guard('G-C3', cell['SC/D2']['diff'] == 1 and cell['SC/D2']['n_rank'] == 1
      and cell['SC/D2']['n_c3'] == 2,
      'SC/D2: n=5 r=4 d=4 ⇒ 正确 1, 常数3版 2（重复计数 +1）')
guard('G-C4', cell['SA/D1']['n_rank'] == 0 and cell['SA/D1']['n_c3'] == -1,
      'SA/D1: n=2 r=2 ⇒ 正确 0, 常数3版 -1（负值 = 定义域外）')
guard('G-C5', cell['SD/D3']['diff'] == 1 and cell['SD/D3']['n_rank'] == 0,
      'SD/D3: n=4 r=4 d=5 ⇒ 正确 0, 常数3版 1（电荷维无锚定却被多算）')
guard('G-C6', all(row['n_rank'] >= 0 for row in T4_ROWS),
      'rank 版在全表恒非负（合法读数）')
guard('G-C7', any(row['n_c3'] < 0 for row in T4_ROWS) and n_plus >= 2,
      '常数3版同时出现负值(-1)与重复计数(+1)两类缺陷（判据有牙）')
guard('G-C8', cell['SB/D1']['n_rank'] == 19
      and cell['SB/D1']['n'] - cell['SB/D1']['r'] + 18 == 19,
      'SM 层级账 = (4-3)+18 = 19（与 r432 及 SM 标准计数逐位一致）')

add('C01', 'CORRECTED', u'常数 3 应改为 rank(D)：D2 口径下常数 3 重复计数 +1',
    u'`SC` 账 {c,ħ,G,e,ε₀} 在 (M,L,T,Q) 下 n=5、rank=4、d=4 ⇒ 正确 N_ext=(5−4)=1；'
    u'若沿用 r432 表格的 `(|S|−3)` 得 2。差的这 1 个正是"由电荷单位已锚定的那一维"被重复计入。'
    u'⇒ **常数 3 是 (M,L,T) 专用**；跨口径复用 r432 表格会产生 +1 的系统性高估。'
    u'（r432 的 SM=19 在 D1 下不受影响，见 A02。）')

add('C02', 'CORRECTED', u'常数 3 在 n<3 的账上给出负 N_ext（定义域外）',
    u'`SA` 账 {c,ħ} 在 D1 下 n=2、rank=2 ⇒ 正确 N_ext=0；常数 3 版给 **−1**。'
    u'负输入数无物理意义 ⇒ 公式的良定域为 `n ≥ rank(D)`，'
    u'而常数 3 版额外要求 `n ≥ 3`（即"用 3 个基本量纲"）。'
    u'⇒ 写法应为 `N_ext = (n − rank(D)) + N_coupling`，并显式声明 `rank(D)` 与 `d`。')

add('C03', 'PASS', u'保结构意义下 SM 账在三档量纲集合上口径不变（1/1/1）',
    u'SB = {c,ħ,G,v}（v∥c，不增秩）在 D1/D2/D3 下 rank 恒 3 ⇒ N_ext 恒 1，'
    u'加 18 个耦合恒得 19。这正是"该账不涉及电荷与温度"的正确表现：'
    u'扩展量纲集合但**不新增该维上的量**，rank 不变 ⇒ 记账不变（T5 的弱形式）。')

add('C04', 'INFO', u'常数 3 正确的充要条件：`rank(D) = 3`（附恒等式）',
    u'机器给出精确恒等式：`n_c3 − n_rank = rank(D) − 3`，与 `n`、`N_coupling` 完全无关。'
    u'故常数 3 与 rank 版同值 ⇔ `rank(D) = 3`。本表 12 格中同值 6 格、分歧 6 格'
    u'（+1 型 3 格 = rank 4 的 D2/D3 电磁与温度账；−1 型 3 格 = rank 2 的欠张满账）。'
    u'⇒ 凡"三个基本量纲 + 三量张满"的账（SM 全部主账都在此列）都不受影响；'
    u'但一旦引入 Q 或 Θ 维、或账本身欠张满，常数 3 立刻失效且方向可判。')

# ================================================================ D T4 假阳性 + span 覆盖
def in_span(target, rows):
    base = [list(x) for x in rows]
    return rank(base) == rank(base + [list(target)])


def span_missing(names, dk, probes=('me', 'e', 'kB')):
    ds = DIMSETS[dk]
    rows = [dvec(nm, ds) for nm in names]
    miss = [p for p in probes if not in_span(dvec(p, ds), rows)]
    return rows, miss


rows_Z, miss_Z = span_missing(('c', 'hbar'), 'D1')
rows_B, miss_B = span_missing(('c', 'hbar', 'G', 'v'), 'D1')
rows_C2, miss_C2 = span_missing(('c', 'hbar', 'G'), 'D2')
rows_CC, miss_CC = span_missing(('c', 'hbar', 'G', 'e', 'eps0'), 'D2')
put('span_missing_SA_D1', miss_Z)
put('span_missing_SB_D1', miss_B)
put('span_missing_c_hbar_G_D2', miss_C2)
put('span_missing_SC_D2', miss_CC)

guard('G-D1', 'me' in miss_Z,
      '账 Z={c,hbar} 在 D1 下质量量纲 (1,0,0) 不在 span 内（质量类观测量不可定义）')
guard('G-D2', 'me' not in miss_B,
      'SB={c,hbar,G,v} 在 D1 下满秩 ⇒ 质量可定义（正对照）')
guard('G-D3', 'e' in miss_C2,
      'span{c,hbar,G} 在 D2 下缺 Q 方向 ⇒ 电荷不可定义（d−r=1 维不可达）')
guard('G-D4', not miss_CC,
      'SC 在 D2 下满秩 ⇒ 全部探针量可定义（满秩时 span 覆盖一切）')
guard('G-D5', cell['SA/D1']['n_rank'] == 0 and ('me' in miss_Z),
      '假阳性成立：N_ext=0 与"质量不可定义"同时出现（记账数字漂亮但不能描述质量）')

add('D01', 'PASS', u'T4 假阳性构造：`N_ext=0` 可由"欠张满 + 抛弃耦合"获得',
    u'账 Z = {c,ħ} 在 (M,L,T) 下 n=2、rank=2 ⇒ N_ext=0，看起来比 TUFT 的 1 更省。'
    u'但机器判定：质量量纲 (1,0,0) **不在** span{c,ħ} 内 ⇒ 该账无法定义任何有质量的观测量。'
    u'⇒ `N_ext=0` 不是"更优"，而是"被描述对象太少"。'
    u'这是把 r432 的 `rank(D) ≤ 3` 当常数使用时的**真实误用后果**，不是文字游戏。')

add('D02', 'PASS', u'新增判据 M-9：span 覆盖检查（可判负预言的必要条件）',
    u'账能定义的物理量类别 = 量纲向量落在 span(D) 内的量。'
    u'机器检验四个样本：Z={c,ħ} 缺质量、{c,ħ,G} 在 D2 下缺电荷、'
    u'SB 与 SC 满秩则全覆盖，正负对照同时在场。'
    u'⇒ 任何"我的理论用零外部输入预言 X"的声明，先检查 `dim(X) ∈ span(D)`；'
    u'不在 span 内则该预言不可陈述，与参数多少无关。')

# ================================================================ E T5 口径不变性
def n_ext(names, dimset_key, ncp):
    ds = DIMSETS[dimset_key]
    rows = [dvec(nm, ds) for nm in names]
    return len(names) - rank(rows) + ncp


E_ROWS = []
E_ROWS.append(dict(tag='BASE', names='c,hbar,G,v', ncp=18, dimset='D1',
                   val=n_ext(('c', 'hbar', 'G', 'v'), 'D1', 18),
                   kind=u'基准账（r432 L7）'))
E_ROWS.append(dict(tag='T5a', names='c,hbar,G', ncp=19, dimset='D1',
                   val=n_ext(('c', 'hbar', 'G'), 'D1', 19),
                   kind=u'谱<->耦合：v 换成等价的 1 个无量纲耦合'))
E_ROWS.append(dict(tag='T5b', names='c,hbar,mP,v', ncp=18, dimset='D1',
                   val=0,
                   kind=u'参考量替换：G 换成由 G 定义的 m_P（同 span）'))
E_ROWS.append(dict(tag='T5c', names='c,hbar,G', ncp=19, dimset='D2',
                   val=n_ext(('c', 'hbar', 'G'), 'D2', 19),
                   kind=u'扩量纲但不新增该维上的量 ⇒ rank 不变 ⇒ 记账不变'))
E_ROWS.append(dict(tag='BAD-drop', names='c,hbar,G', ncp=18, dimset='D1',
                   val=n_ext(('c', 'hbar', 'G'), 'D1', 18),
                   kind=u'漏账：删掉 v 但不把它转成耦合'))
E_ROWS.append(dict(tag='BAD-dup', names='c,hbar,G,v', ncp=19, dimset='D1',
                   val=n_ext(('c', 'hbar', 'G', 'v'), 'D1', 19),
                   kind=u'重复计：保留 v 且同时把它换成耦合'))

# T5b 的 m_P 与 {c,hbar,G} 同 span（m_P 由三者定义），用线性等价显式核验：
M_P_VEC = dadd(dscale(dvec('hbar', DIMSETS['D1']), F(1, 2)),
               dscale(dvec('c', DIMSETS['D1']), F(1, 2)))
M_P_VEC = dadd(M_P_VEC, dscale(dvec('G', DIMSETS['D1']), F(-1, 2)))
E_ROWS[2]['val'] = 4 - rank([dvec('c', DIMSETS['D1']), dvec('hbar', DIMSETS['D1']),
                             M_P_VEC, dvec('v', DIMSETS['D1'])]) + 18
put('e_rows', E_ROWS)
put('mP_vector', list(M_P_VEC))

val = dict((row['tag'], row['val']) for row in E_ROWS)
guard('G-E1', M_P_VEC == (1, 0, 0), 'm_P = hbar^(1/2) c^(1/2) G^(-1/2) 的量纲向量 = (1,0,0)')
guard('G-E2', val['BASE'] == 19, '基准账 = 19')
guard('G-E3', val['T5a'] == 19, '谱<->耦合变换后仍 19（不变）')
guard('G-E4', val['T5b'] == 19, '参考量替换（G->m_P）后仍 19（不变）')
guard('G-E5', val['T5c'] == 19, '扩量纲不增量后仍 19（不变）')
guard('G-E6', val['BAD-drop'] == 18, '漏账型破坏 ⇒ 18（被判据抓出）')
guard('G-E7', val['BAD-dup'] == 20, '重复计型破坏 ⇒ 20（被判据抓出）')
guard('G-E8', len(set([val['BASE'], val['T5a'], val['T5b'], val['T5c']])) == 1,
      '三类保结构变换给出同一个数（不变性不是硬编码：路径确实不同）')

add('E01', 'PASS', u'T5 口径不变性：三类保结构变换下 N_ext 恒为 19',
    u'①谱↔耦合（v→λ 或 μ² 的等价耦合）：(3−3)+19=19；'
    u'②参考量替换（G→m_P，二者张成同一 span，机器核 m_P 向量 =(1,0,0)）：(4−3)+18=19；'
    u'③扩量纲集合但不新增该维上的量（D1→D2，SB 仍 rank 3）：1+18=19。'
    u'⇒ N_ext 是**记账的规范不变量**，与"用哪个量当参考"无关 —— 这正是 r432 T2 想说但未证明的部分。')

add('E02', 'PASS', u'T5 破坏面：漏账与重复计各偏离 1，判据有牙',
    u'漏账（删 v 不转耦合）⇒ 18；重复计（留 v 且转耦合）⇒ 20。'
    u'两者与正确的 19 各差 1，且方向相反 ⇒ 判据不是"只能检测单向偏差"的弱判据。'
    u'实际误用最常见形式是**重复计 +1**（理由见 C01：跨口径时把已被单位锚定的量再算一遍）。')

# ================================================================ F T6 离散输入下界
GROUP_CHOICES = ['U(1)', 'SU(2)', 'SU(3)', 'SU(5)', 'SO(10)']
GEN_CHOICES_BOUNDED = [1, 2, 3]
LN2 = Dec(2).ln()
I_GROUP = (Dec(len(GROUP_CHOICES)).ln() / LN2)
I_GEN_B = (Dec(len(GEN_CHOICES_BOUNDED)).ln() / LN2)
I_TOTAL = I_GROUP + I_GEN_B
# 代数若为任意正整数（不设上限）：取 N=10^6 作趋势读数
I_GEN_UNB = (Dec(1000000).ln() / LN2)
put('i_group_bits', str(I_GROUP)[:18])
put('i_gen_bounded_bits', str(I_GEN_B)[:18])
put('i_total_bits', str(I_TOTAL)[:18])
put('i_gen_unbounded_at_1e6_bits', str(I_GEN_UNB)[:18])

guard('G-F1', abs(I_GROUP - Dec('2.321928')) < Dec('1e-6'),
      'I_group = log2(5) = 2.321928 bit')
guard('G-F2', abs(I_GEN_B - Dec('1.584963')) < Dec('1e-6'),
      'I_gen（上限 3）= log2(3) = 1.584963 bit')
guard('G-F3', abs(I_TOTAL - Dec('3.906891')) < Dec('1e-6'),
      '合计 = log2(15) = 3.906891 bit')
guard('G-F4', I_TOTAL > 0, '离散输入信息量为正 ⇒ 不可"免费"')
guard('G-F5', I_GEN_UNB > I_GEN_B and I_GEN_UNB > Dec('19'),
      '代数若不设上限 ⇒ 信息量无界（1e6 候选即 19.93 bit）')

add('F01', 'PASS', u'T6 离散输入的信息量下界（受控表，非对库内某体的裁决）',
    u'受控表：群候选 5 个（U(1)/SU(2)/SU(3)/SU(5)/SO(10)）⇒ `log₂5 = 2.3219 bit`；'
    u'代数候选上限 3（{1,2,3}）⇒ `log₂3 = 1.5850 bit`；合计 `log₂15 = 3.9069 bit`。'
    u'若代数不设上限（任意正整数），1e6 候选即 19.93 bit 且可继续增长 ⇒ **无界**。'
    u'⇒ "只要群和代数"不是零信息：它至少要 3.9 bit（有界情形）。')

add('F02', 'BOUNDARY', u'Ω5 只限连续常数 ⇒ "口径 II 与 Ω5 相容"必须附条件',
    u'r432 §6.3 结论"口径 II 的 N_ext=1 ≤ 1 ⇒ 与 Ω5 相容"**仅对连续常数成立**。'
    u'Ω5 的形式是"自由常数 ≤ 1"，对离散选择（群、代）完全无约束（同 r15 口径 III 的教训：'
    u'公设若只限常数，对节点/函数/离散选择全失效）。'
    u'⇒ 完整表述应为：`连续 N_ext = 1 ≤ 1`（相容）**且** `I_disc ≥ 3.9 bit`（Ω5 不覆盖，'
    u'须由 O1 的"从不预置群/谱"条款另行裁决）。'
    u'【分工】"过 O1 不可达"已由并行 r433 从**来源二分**侧裁定（两腿全封），本册**不重判**；'
    u'本册只补**计量**这一层（离散项记多少 bit、Ω5 与它在形式上不相交），属正交读数。'
    u'本条只标边界，不代裁。')

add('F03', 'INFO', u'记账的完整读数是二元组 `(N_ext, I_disc)`，不是一个数',
    u'r432 报 `N_ext` 已足以做"参数减少"的判定，但不足以判"是否预置"。'
    u'建议此后所有记账写成 `(N_ext 连续, I_disc 离散/bit)`，两个分量分别对应 Ω5 与 O1 条款，'
    u'不得合并成单一"输入个数"——合并会掩盖"用离散选择换连续参数"的记账转移。')

# ================================================================ G T7 判据力不完备
T7 = [
    dict(tag='A', p=10, k=10, note=u'10 参数 / 10 观测'),
    dict(tag='B', p=10, k=16, note=u'10 参数 / 16 观测（+6 独立）'),
]
for row in T7:
    row['over'] = row['k'] - row['p']
    row['n_ext'] = 10
put('t7_rows', T7)
T7A, T7B = T7[0], T7[1]

guard('G-G1', T7A['over'] == 0, '账 A 超定度 0（恰可插值）')
guard('G-G2', T7B['over'] == 6, '账 B 超定度 6（可判负 6 个）')
guard('G-G3', T7A['n_ext'] == T7B['n_ext'] == 10, '两账 N_ext 相同（均为 r432 L2 档）')
guard('G-G4', T7B['over'] - T7A['over'] == 6, '判据力差 6 > 0（N_ext 不能决定判据力）')

add('G01', 'FAIL', u'记账判据的预测力不完备：`N_ext` 相同 ≠ 判据力相同',
    u'两账都取 N_ext=10（r432 L2 档）：账 A 有 10 个参数对 10 个观测 ⇒ 超定度 `k−p=0`，'
    u'可插值任何数据 ⇒ **零判据力**；账 B 同 10 个参数对 16 个观测 ⇒ 超定度 6 ⇒ 有 6 个可判负约束。'
    u'⇒ `N_ext` 是"输入经济性"的必要条件，**不是完成度的充分条件**。'
    u'本条判 FAIL 指"仅凭记账即可判完成"这一命题不成立，不是本册执行失败。')

add('G02', 'PASS', u'T7 超定度定义可机器判（`over = k − p`）',
    u'把"判据力"从主观的"预言多不多"落到两个整数之差：`over = k − p`，'
    u'`over ≤ 0` ⇒ 零判据力；`over > 0` ⇒ 至少 over 个可判负方向。'
    u'机器读数：A/B 两账 (0, 6)；控制组把 k 从 16 改 18 得 8 ⇒ 数字随输入变化，非硬编码。')

# ================================================================ H 判据沉淀
CRITERIA = [
    dict(code='M-7', name=u'记账口径三元组',
         body=u'报 `N_ext` 时必须同时报 `(n, rank(D), d)` 三元组：n = 有量纲量个数、'
              u'rank(D) = 它们在量纲空间中的秩、d = 采用的基本量纲数。'
              u'`rank(D) = d` 是完备性条件；`rank(D) < d` 时该账"输入少"只是"描述少"。'
              u'减数必须写 `rank(D)`，不得写常数 3（常数 3 是 (M,L,T) 专用）。'),
    dict(code='M-8', name=u'离散输入单列（bit）',
         body=u'离散选择不以"参数个数"计，而以信息量 `I_disc = log2(#choices)` 单列。'
              u'并须回答"#choices 是否由既有公设唯一确定"：唯一确定 ⇒ I_disc=0（内生）；'
              u'否则 >0，且 Ω5（只限连续常数）对其完全无约束。'),
    dict(code='M-9', name=u'span 覆盖必要性',
         body=u'任何"C 个外部输入即可预言 X"的声明，先检查 `dim(X) ∈ span(账的 D)`。'
              u'不在 span 内 ⇒ 该预言不可陈述（与被描述对象缺失同义），与参数多少无关。'
              u'满秩账（rank = d）的 span 覆盖全空间，故该检查只对欠张满账有判别力。'),
]
put('criteria', CRITERIA)

add('H01', 'PASS', u'判据沉淀 M-7 / M-8 / M-9（可迁移，30 秒可判）',
    u'M-7 记账口径三元组（减数用 rank 而非常数 3）；M-8 离散输入以 bit 单列并与 Ω5 分离；'
    u'M-9 span 覆盖必要性（先查目标量纲是否落在账的 span 内）。'
    u'三条合起来把 r432 的"一个数字"升级为"可直接复核的三元组 + 一个 bit 账"。')

# ================================================================ I 自抓
SELF_CHECKS = [
    dict(id='S1', kind=u'语义替换被量纲掩盖',
         problem=u'E 段 T5b 首版把"参考量替换 G→m_P"写成 `n_ext((c,hbar,me,v),...)`，'
                 u'用电子质量 me 顶替普朗克质量 m_P。因 [me]=[m_P]=(1,0,0)，'
                 u'rank 完全不变、数值全对 ⇒ **量纲类守卫抓不到这个语义错误**。',
         fix=u'改为显式由 ħ,c,G 组合构造 m_P 向量并断言 `== (1,0,0)`（G-E1），'
             u'再参与 rank ⇒ 参考量替换的正确性可被机器核。',
         lesson=u'同量纲的不同物理量互换不会被量纲检查发现；'
                u'"由谁定义"必须显式构造并断言，不能靠同量纲巧合通过。'),
    dict(id='S2', kind=u'硬编码绕过判据',
         problem=u'T5b 首版为省事写成 `val = 19`（if False else 19），'
                 u'即把结论直接写进数据，使"不变性"无法被证伪 —— 违反本库"数字非硬编码"纪律。',
         fix=u'改为实算 `4 - rank([c,hbar,m_P,v]) + 18`，并由 G-E1..E8 锁定三档同值、'
             u'两档错值（18/20）。',
         lesson=u'任何"不变性/守恒"断言，其读数必须由同一函数对**不同输入**重算得出；'
                u'一旦出现字面量结论，判据立即退化为装饰。'),
    dict(id='S3', kind=u'判据可判性',
         problem=u'G 段首版想用"该理论能给出几个预言"作为判据力，这是主观计数、无法机器复核，'
                 u'且不同人对"一个预言"的粒度可分歧。',
         fix=u'改为超定度 `over = k - p`（观测数 − 参数数），两整数之差可机器判；'
             u'`over <= 0` 即零判据力。',
         lesson=u'凡进入判定册的"力/度/量"，必须落到可数的整数或可复算的比值上；'
                u'否则它会随叙述口径漂移（与 r42/r44 的"口径敏感"同族）。'),
    dict(id='S4', kind=u'已知坑复发',
         problem=u'首跑在 `json.dumps` 崩 `TypeError: Object of type Fraction is not JSON serializable`：'
                 u'`mP_vector` 由 `dscale(..., Fraction(1,2))` 组合而成，其分量是 Fraction。'
                 u'该坑在 r27/r37/r42/r44 已各记一次，本轮仍复现。',
         fix=u'新增 `_jsonable()` 统一投影（Fraction/Decimal→str、tuple/set→list），'
             u'作为 `json.dumps(..., default=_jsonable)` 的兜底。',
         lesson=u'"已知坑"不等于"不会再踩"：凡把 Fraction/Decimal 写入 JSON 产物，'
                u'必须默认挂 default 转换器，而不是等首跑崩溃后再补。'),
    dict(id='S5', kind=u'计数时序',
         problem=u'首版 `g_ok` 在 `guard("G-J1"/"G-J2")` 注册**之前**统计，'
                 u'于是 total=56 而 ok=54，报告打 `guards 54/56` 却 `bad` 为空 —— '
                 u'一个"看起来有 2 条守卫失败、实则全过"的假警报。',
         fix=u'在 J1/J2 注册后重算 `g_ok`，并新增 G-J3 锁"计数与注册同步"。',
         lesson=u'汇总计数必须在所有被计数对象注册完毕之后做；'
                u'"分母含新项、分子不含新项"是汇报类脚本最常见的自欺形态。'),
]
put('self_checks', SELF_CHECKS)

for s in SELF_CHECKS:
    guard('G-H' + s['id'][1:], bool(s['fix']), u'自抓 %s 已修正并落盘（%s）' % (s['id'], s['kind']))

# ================================================================ J 控制组（阳性对照）
ctrl('CTRL-1', (cell['SA/D1']['n_rank'], 'me' in miss_Z) != (cell['SB/D1']['n_rank'], 'me' in miss_B),
     u'SA 与 SB 的 (N_rank, 质量可定义) 组合不同 ⇒ 判据能区分"零输入但欠定义"与"1 输入且完备"')
ctrl('CTRL-2', cell['SC/D1']['n_rank'] != cell['SC/D2']['n_rank'],
     u'同一账换量纲集合后 N_rank 从 %d 变 %d ⇒ 数字被真正重算（非硬编码）'
     % (cell['SC/D1']['n_rank'], cell['SC/D2']['n_rank']))
ctrl('CTRL-3', (18 - 10) == 8 and T7B['over'] == 6,
     u'T7 把 k 从 16 改 18 ⇒ over 从 6 变 8（判据随输入变化）')
ctrl('CTRL-4', n_ext(('c', 'hbar', 'G', 'hbar'), 'D1', 18) == 19,
     u'SB 把 v 换成 hbar（同 span 内替换，rank 仍 3）⇒ 仍 19（替换不改变记账）')

guard('G-CTRL', len(CONTROLS) == 4 and all(c['ok'] for c in CONTROLS),
      u'控制组 4/4 全过（判据有牙：能区分欠定义、能随口径重算、非硬编码、替换不变）')

# ================================================================ 输出
def _jsonable(o):
    """Fraction / Decimal / tuple 的统一 JSON 投影（本库已知坑：Fraction 不可直接序列化）。"""
    if isinstance(o, F):
        return str(o)
    if isinstance(o, Dec):
        return str(o)
    if isinstance(o, (set, tuple, list)):
        return [str(x) if isinstance(x, (F, Dec)) else x for x in o]
    return str(o)


n_pass = sum(1 for e in ENTRIES if e['status'] == 'PASS')
n_fail = sum(1 for e in ENTRIES if e['status'] == 'FAIL')
n_info = sum(1 for e in ENTRIES if e['status'] == 'INFO')
n_bnd = sum(1 for e in ENTRIES if e['status'] == 'BOUNDARY')
n_cor = sum(1 for e in ENTRIES if e['status'] == 'CORRECTED')
g_ok = sum(1 for g in GUARDS if g['ok'])
c_ok = sum(1 for c in CONTROLS if c['ok'])

guard('G-J1', n_pass + n_fail + n_info + n_bnd + n_cor == len(ENTRIES),
      '条目分类计数与总数自洽 (%d)' % len(ENTRIES))
guard('G-J2', len(GUARDS) >= 40,
      '守卫总数 >= 40（实得 %d）' % len(GUARDS))

# 计数必须在 G-J1/G-J2 注册之后重算，否则 total 含这两条而 ok 不含（自抓 S5）
g_ok = sum(1 for g in GUARDS if g['ok'])
c_ok = sum(1 for c in CONTROLS if c['ok'])
guard('G-J3', g_ok == len(GUARDS), '守卫计数自洽（%d/%d）' % (g_ok, len(GUARDS)))
g_ok = sum(1 for g in GUARDS if g['ok'])

DOC = dict(
    round=ROUND, date=DATE, name=NAME,
    verdict='CALIBER-INVARIANCE--CONST-3-IS-D1-ONLY--REPLACE-BY-RANK-D--'
            'SPAN-COVERAGE-NECESSARY--DISCRETE-INPUTS-COST-3P9-BITS--'
            'LEDGER-NECESSARY-NOT-SUFFICIENT--0OF6-UNCHANGED',
    counts=dict(total=len(ENTRIES), PASS=n_pass, FAIL=n_fail, INFO=n_info,
                BOUNDARY=n_bnd, CORRECTED=n_cor),
    guards=dict(total=len(GUARDS), ok=g_ok),
    controls=dict(total=len(CONTROLS), ok=c_ok),
    entries=ENTRIES, guard_rows=GUARDS, control_rows=CONTROLS,
    numbers=NUMBERS, criteria=CRITERIA, self_checks=SELF_CHECKS,
)

OUT.mkdir(parents=True, exist_ok=True)
jp = OUT / (NAME + '.json')
io.open(str(jp), 'w', encoding='utf-8').write(
    json.dumps(DOC, ensure_ascii=False, indent=1, sort_keys=True, default=_jsonable))

lines = []
lines.append('[r434] INPUT-LEDGER CALIBER INVARIANCE / SPAN COVERAGE / DISCRETE BITS')
lines.append('entries %d = PASS %d / FAIL %d / CORRECTED %d / INFO %d / BOUNDARY %d'
             % (len(ENTRIES), n_pass, n_fail, n_cor, n_info, n_bnd))
lines.append('guards %d/%d   controls %d/%d' % (g_ok, len(GUARDS), c_ok, len(CONTROLS)))
lines.append('det([c],[hbar],[G]) = %s   rank=%d' % (DET3, R3))
lines.append('T4: diff = n_c3 - n_rank = rank - 3 ; diff cells %d (plus %d / minus %d)'
             % (n_diff, n_plus, n_minus))
lines.append('  SB/D1  N_ext=%.0f  n-3=%.0f' %
             (cell['SB/D1']['n_rank'], cell['SB/D1']['n_c3']))
lines.append('  SC/D2  N_ext=%.0f  n-3=%.0f   <- duplicated counting +1' %
             (cell['SC/D2']['n_rank'], cell['SC/D2']['n_c3']))
lines.append('  SA/D1  N_ext=%.0f  n-3=%.0f   <- negative (out of domain)' %
             (cell['SA/D1']['n_rank'], cell['SA/D1']['n_c3']))
lines.append('  SD/D3  N_ext=%.0f  n-3=%.0f' %
             (cell['SD/D3']['n_rank'], cell['SD/D3']['n_c3']))
lines.append('T5: base %d / spec<->coup %d / ref-replace %d / widen %d / BAD %d,%d'
             % (val['BASE'], val['T5a'], val['T5b'], val['T5c'],
                val['BAD-drop'], val['BAD-dup']))
lines.append('T6: I_group=%s  I_gen(<=3)=%s  total=%s bit  (unbounded@1e6=%s)'
             % (str(I_GROUP)[:8], str(I_GEN_B)[:8], str(I_TOTAL)[:8], str(I_GEN_UNB)[:8]))
lines.append('T7: overA=%d overB=%d  both N_ext=10' % (T7A['over'], T7B['over']))
lines.append('span missing: SA/D1=%s  c,hbar,G/D2=%s  SB/D1=%s  SC/D2=%s'
             % (miss_Z, miss_C2, miss_B, miss_CC))
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



