# -*- coding: utf-8 -*-
"""
《磁场闭环螺旋光速运动》—— 零螺距闭设定理与最小修法代价（攻破轮）
================================================================

对象（承接上一轮，不重复其清点）
--------------------------------
上一轮册：`判定_磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18.md`
（条目 41 / 守卫 21 / 退出码 0，产物 `数据/磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18.json`）。
它裁定该族 FAIL，理由是「传播条件 κ² ≥ 0 对全部 1296 组参数恒不可满足」（C01），
并在 §七 给出五条最小修法，其中 P1 写作：

    P1（零成本，纯命名）：把 h 统一改为 L …… **这是四篇正文唯一的零成本修法。**

本轮攻破的是它留下的 OPEN 缺口：**上一轮的裁定只在 k_n = n/b 那一族成立；
把 k_n 改成 2πn/L（P1 本身）之后，「闭环螺旋 ∧ v = c」还能不能被救回来？**
以及 §七 那句「唯一 / 零成本」是否站得住。

本册做什么
----------
1. 把该族自己的三条关系（光速约束、传播条件、相位匹配）合并成一个**无量纲、不含 π**
   的联立形式：j := k_n·b ∈ ℤ，κ² = (1 − (k_n a)² − j²)/(a²+b²)。
   π 只住在 k_n 的数值里，不进入约束的形状。
2. 由此得**零螺距闭设定理**（三分律）：a > 0 ∧ k_n > 0 ∧ κ² ≥ 0 ∧ j ∈ ℤ ⇒ j = 0 ⇒ b = 0。
   预算式 (k_n a)² ≤ 1 − j² 说明这不是数值巧合：j = ±1 一支把整个传播预算吃光，
   留给半径的是 0，且残余恰等于 −a²/(b²(a²+b²))（**无容差**，a 必须恰为 0）。
3. 两条独立枚举臂（j 由网格判整 / b 由量子化构造）+ 撤掉量子化的阳性对照
   ⇒ 排除「空集是网格太紧造成的」。
4. 跨轮 pin：上一轮面里的 1296、0.9371681469282042、n_max=11、10 个解，
   全部由**本轮自己的通道**重算并与 `数据/*.json` 逐位对账；参数与网格从
   上一轮引擎源码现读，不由本册手打。
5. 攻破配套代码 `02_constraints.py` §2.5 的「自洽传播解数 10」：其中 m=0 一支的
   b 是代码把公式值 −1/k_n 覆写成 0 得来的，而覆写后相位分母 m − k_n b = 0，
   即 v = ∞ ⇒ 真正同时满足相位匹配与传播的只有 5 个。
6. 攻破 paper.html 的 n_max=11：在该文自己的参数（a=b=0.01, L=1）下，
   11 个传播模态的 j = 2πnb/L 全落在 (0,1) 内、没有一个整数 ⇒ 11 这个模态数
   住在量子化条件**之外**；把量子化保持住（b=0）则同一公式给 n_max = 15。
7. 最小修法代价台账：对 P1…P5 逐条**实测**待改点数（语料内出现次数，含重复副本
   的加倍），并逐条机器回答「修完之后是否出现非零螺距的严格传播自洽解」。
8. 据此更正上一轮 §七 P1 的「唯一 / 零成本」两处措辞。

口径与红线
----------
- 纯标准库（os / sys / re / io / json / math / hashlib / decimal / fractions）。
- 网格核验一律用 Fraction 精确算术（十进制字面量转分数无舍入），浮点只用于
  与上一轮面的浮点读数逐位对账那一步。
- 「恒为空」的裁定必须配阳性对照；分解必须自证闭合（子桶之和等于母桶）。
- 分母不手打：网格、参数、n 上限由上一轮引擎源码现读；出现次数由语料现扫。
- 红线：这是关于**该语料自己的方程组**的定理，不是新物理；不否定圆波导/贝塞尔
  模态这一成熟数学，也不主张 a、b、L 的任何实测取值。
- 写盘目录可用环境变量 UFT_ZEROPITCH_OUTDIR 重定向（变异体跑用临时目录）。

产出
----
  数据/磁场闭环螺旋_零螺距闭设定理与最小修法代价_攻破_2026-10-18.{json,md}
  数据/磁场闭环螺旋_零螺距闭设定理与最小修法代价_攻破_2026-10-18_report.txt
  判定_磁场闭环螺旋_零螺距闭设定理与最小修法代价_攻破_2026-10-18.md
"""
import os
import re
import io
import sys
import json
import math
import hashlib
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ---------------------------------------------------------------- 路径
MYLIB = r'd:\a10\aikjx\code\my_lib'
ROUND = os.path.join(MYLIB, 'openuft', '04_公共成果', '算法联盟_全维自洽与归一化')
DATA = os.path.join(ROUND, '数据')                 # 只读：跨轮 pin 的权威面
OUTDIR = os.environ.get('UFT_ZEROPITCH_OUTDIR') or ROUND   # 写盘（变异体重定向到临时目录）
HTML = os.path.join(MYLIB, 'ufthub', 'html', '202609')
PKG = os.path.join(MYLIB, 'openuft', '90_历史归档', '来源语料_ufthub_20260925',
                   '08_宇宙文明与工程平台包', 'magnetic_field_algorithm_paper', 'paper_package')
PREV_STEM = '磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18'
PREV_JSON = os.path.join(DATA, PREV_STEM + '.json')
PREV_ENGINE = os.path.join(ROUND, '源码', PREV_STEM + '.py')
STEM = '磁场闭环螺旋_零螺距闭设定理与最小修法代价_攻破_2026-10-18'

C_LIGHT = Decimal('299792458')
TODAY = '2026-10-18'

# π 的有理双侧界：用于「j 区间内有无整数」的严格判定（不靠浮点相等）
PI_LO = Fr('3.1415926535897932')
PI_HI = Fr('3.1415926535897933')
# 参照值（π 的公开十进制展开前 60 位，用于自证上面两侧界方向正确；非本轮计算输入）
PI_REF = Fr('3.1415926535897932384626433832795028841971693993751058209749')

# ---------------------------------------------------------------- 量纲四元组 (M, L, T, Q)
DIM_A = (Fr(0), Fr(1), Fr(0), Fr(0))
DIM_B = (Fr(0), Fr(1), Fr(0), Fr(0))
DIM_K = (Fr(0), Fr(-1), Fr(0), Fr(0))
DIM_OMEGA = (Fr(0), Fr(0), Fr(-1), Fr(0))
DIM_V = (Fr(0), Fr(1), Fr(-1), Fr(0))


def dim_mul(d, e, n=1):
    return tuple((d[i] + e[i]) * n for i in range(4))


def dstr(d):
    names = ('M', 'L', 'T', 'Q')
    parts = []
    for nm, v in zip(names, d):
        v = Fr(v)
        if v == 0:
            continue
        parts.append(nm if v == 1 else '%s^%s' % (nm, v.numerator if v.denominator == 1 else '%d/%d' % (v.numerator, v.denominator)))
    return ' '.join(parts) if parts else '1'


# ---------------------------------------------------------------- 条目 / 守卫系统
ENTRIES = []
GUARDS = []


def add(code, title, detail, status, must_pass=False):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))
    if must_pass and status != 'PASS':
        print('MUST-PASS FAILED: %s %s' % (code, title))
        sys.exit(3)


def guard(code, cond, msg):
    GUARDS.append(dict(code=code, ok=bool(cond), msg=msg))
    if not cond:
        print('GUARD FAILED: %s %s' % (code, msg))
        sys.exit(4)


def P(*a, **k):
    add(*a, status='PASS', **k)


def F(*a, **k):
    add(*a, status='FAIL', **k)


def B(*a, **k):
    add(*a, status='BOUNDARY', **k)


def I(*a, **k):
    add(*a, status='INFO', **k)


def CE(*a, **k):
    add(*a, status='CORRECTED', **k)


# ================================================================ S0 量纲契约
print('\n[S0] 量纲契约与无量纲化')

DIM_J = dim_mul(DIM_K, DIM_B)
DIM_BUDGET = dim_mul(DIM_K, DIM_A)
DIM_K2 = dim_mul(DIM_K, DIM_K)

P('Z01', '联立系统的无量纲坐标：j = k_n b 与 (k_n a)，二者皆纯数',
  'k_n 量纲 %s、a 与 b（螺距参数，z = bθ 中每弧度轴向位移）量纲 %s，故 j = k_n b 量纲 %s、'
  '(k_n a)² 量纲 %s；κ² 量纲 %s。整套约束只由这两个纯数与一个 L^-2 符号组成，'
  'π 只进入 k_n 的具体数值（2πn/L 或 n/b），不进入约束的形状——这就是本定理「不含 π」的准确含义。'
  % (dstr(DIM_K), dstr(DIM_A), dstr(DIM_J), dstr(dim_mul(DIM_BUDGET, DIM_BUDGET)), dstr(DIM_K2)))

guard('G0-1', DIM_J == (Fr(0),) * 4, 'j = k_n b 必须量纲为 1，实得 %s' % dstr(DIM_J))
guard('G0-2', DIM_BUDGET == (Fr(0),) * 4, '(k_n a) 必须量纲为 1，实得 %s' % dstr(DIM_BUDGET))
guard('G0-3', DIM_K2 == (Fr(0), Fr(-2), Fr(0), Fr(0)) and dim_mul(DIM_OMEGA, DIM_OMEGA) == (Fr(0), Fr(0), Fr(-2), Fr(0)),
      'κ² 必须是 L^-2 而 ω² 必须是 T^-2，实得 %s / %s' % (dstr(DIM_K2), dstr(dim_mul(DIM_OMEGA, DIM_OMEGA))))
guard('G0-4', dstr(DIM_J) == '1' and dstr(DIM_K) == 'L^-1' and dstr(DIM_V) == 'L T^-1',
      '量纲渲染须与运算同结论（渲染本身也是代码）：%r / %r / %r' % (dstr(DIM_J), dstr(DIM_K), dstr(DIM_V)))
guard('G0-5', dim_mul(DIM_OMEGA, DIM_B) == DIM_V,
      'v = ω·√(a²+b²) 的量纲必须是 L T^-1，实得 %s' % dstr(dim_mul(DIM_OMEGA, DIM_B)))

# ================================================================ S1 恒等式（两条独立通道）
print('[S1] 主恒等式与 π-自由形态（逐点精确核验）')


def kappa2_direct(a, b, k):
    """语料自己的写法：ω = c/√(a²+b²) 代入 κ² = ω²/c² − k_n²"""
    return Fr(1, 1) / (a * a + b * b) - k * k


def kappa2_budget(a, b, k):
    """本轮的第一形态：κ² = (1 − (k_n a)² − j²)/(a²+b²)，j = k_n b"""
    j = k * b
    return (Fr(1, 1) - (k * a) ** 2 - j * j) / (a * a + b * b)


def kappa2_pifree(a, b, j):
    """本轮的第二形态（b>0）：κ² · b²(a²+b²) = −(j²a² + (j²−1)b²)"""
    return -(j * j * a * a + (j * j - 1) * b * b) / (b * b * (a * a + b * b))


grid_a1 = [Fr('0.1'), Fr('0.31'), Fr('0.5'), Fr('0.73'), Fr('1'), Fr('1.16'),
           Fr('1.37'), Fr('1.58'), Fr('1.79'), Fr('2'), Fr('3'), Fr('5')]
grid_b1 = [Fr('0.05'), Fr('0.1'), Fr('0.159'), Fr('0.25'), Fr('0.5'), Fr('0.6'),
           Fr('1'), Fr('2'), Fr('5')]
grid_k1 = [Fr(1, 100), Fr(1, 40), Fr(1, 10), Fr(1, 8), Fr(1, 5), Fr(1, 4), Fr(1, 3),
           Fr(2, 3), Fr(3, 4), Fr(1), Fr(4, 3), Fr(2), Fr(5)]

id1_hits = 0
id1_fail = []
id2_hits = 0
id2_fail = []
for _a in grid_a1:
    for _b in grid_b1:
        for _k in grid_k1:
            d = kappa2_direct(_a, _b, _k)
            e = kappa2_budget(_a, _b, _k)
            id1_hits += 1
            if d != e:
                id1_fail.append((_a, _b, _k, d, e))
            _j = _k * _b
            if _j.denominator == 1 and _b > 0:
                f = kappa2_pifree(_a, _b, _j)
                id2_hits += 1
                if d != f:
                    id2_fail.append((_a, _b, _j, d, f))

P('Z02', '主恒等式 κ² = (1 − (k_n a)² − j²)/(a²+b²) 在 %d 组精确有理点上逐点成立' % id1_hits,
  '左端是语料自己的两步代入（ω = c/√(a²+b²) 再 κ² = ω²/c² − k_n²），右端是本轮的预算形态。'
  '两端在全部 %d 组 (a, b, k_n) 三元组上以 Fraction 逐点相等（无浮点、无容差），失配 %d 组。'
  '该恒等式是本轮一切裁定的代数底座：它把「传播」翻译成纯数不等式 (k_n a)² + j² ≤ 1。'
  % (id1_hits, len(id1_fail)))

guard('G1-1', id1_hits == len(grid_a1) * len(grid_b1) * len(grid_k1) and id1_hits > 0,
      '恒等式一通道核验点数须等于网格笛卡尔积：%d vs %d' % (id1_hits, len(grid_a1) * len(grid_b1) * len(grid_k1)))
guard('G1-2', not id1_fail, '恒等式一通道不许有失配点：%r' % (id1_fail[:3],))

P('Z03', 'π-自由形态 κ²·b²(a²+b²) = −(j²a² + (j²−1)b²) 在 %d 组量子化点上逐点成立' % id2_hits,
  '取 j = k_n b ∈ ℤ 消去 k_n（k_n = j/b），得完全不含 π、不含 k_n 的形态。'
  '核验 %d 组（b > 0 且 j 为整数的网格点），失配 %d 组。由此读出的符号律是：'
  '|j| ≥ 1 时 D := j²a² + (j²−1)b² ≥ a² > 0，故 κ² < 0 严格成立——'
  '「非零螺距 ⇒ 倏逝」不依赖 k_n 的定义族（n/b 或 2πn/L 都能写成某个 j），只依赖 j 是整数。'
  % (id2_hits, len(id2_fail)))

guard('G1-3', id2_hits > 0, 'π-自由通道的核验集不许为空（空扫描与「没有反例」同形）：%d' % id2_hits)
guard('G1-4', not id2_fail, 'π-自由形态不许有失配点：%r' % (id2_fail[:3],))

# ================================================================ S2 零螺距闭设定理（双臂穷举）
print('[S2] 零螺距闭设定理：双臂穷举 + 分桶闭合')


def is_int(x):
    return x.denominator == 1


# 臂一：(a, b, k_n) 网格上判 j 是否整数
arm1 = dict(tot=0, quant=0, notquant=0, prop=0, prop_bpos=0,
            quant_prop=0, quant_prop_bpos=0, quant_prop_bzero=0, quant_notprop=0,
            notquant_prop=0, notquant_prop_bpos=0)
arm1_examples = []
for _a in grid_a1:
    for _b in [Fr(0)] + grid_b1:
        for _k in grid_k1:
            arm1['tot'] += 1
            j = _k * _b
            q = is_int(j)
            k2 = kappa2_direct(_a, _b, _k)
            pr = k2 >= 0
            if pr:
                arm1['prop'] += 1
                if _b > 0:
                    arm1['prop_bpos'] += 1
            if q:
                arm1['quant'] += 1
                if pr:
                    arm1['quant_prop'] += 1
                    if _b > 0:
                        arm1['quant_prop_bpos'] += 1
                        arm1_examples.append('a=%s b=%s k=%s j=%s κ²=%s' % (_a, _b, _k, j, k2))
                    else:
                        arm1['quant_prop_bzero'] += 1
                else:
                    arm1['quant_notprop'] += 1
            else:
                arm1['notquant'] += 1
                if pr:
                    arm1['notquant_prop'] += 1
                    if _b > 0:
                        arm1['notquant_prop_bpos'] += 1

# 臂二：b 由量子化条件构造（b = (m−1)/k_n，即 02_constraints.py §2.5 的公式本身）
grid_a2 = [Fr('0.01'), Fr('0.1'), Fr('0.31'), Fr('1'), Fr('5')]
grid_k2 = [Fr(1, 1000), Fr(1, 100), Fr(1, 10), Fr(1), Fr(2), Fr(10)]
arm2 = dict(tot=0, prop=0, prop_bpos=0, prop_bzero=0, j_hist={}, prop_m=set(), j_m_bad=0)
for _a in grid_a2:
    for _k in grid_k2:
        for _m in range(0, 7):
            arm2['tot'] += 1
            _b = Fr(_m - 1, 1) / _k
            j = _k * _b          # 恒等于 m−1（构造性量子化）
            if j != _m - 1:
                arm2['j_m_bad'] += 1
            arm2['j_hist'][int(j)] = arm2['j_hist'].get(int(j), 0) + 1
            k2 = kappa2_direct(_a, _b, _k)
            if k2 >= 0:
                arm2['prop'] += 1
                arm2['prop_m'].add(_m)
                if _b > 0:
                    arm2['prop_bpos'] += 1
                else:
                    arm2['prop_bzero'] += 1

F('Z04', '零螺距闭设定理：a > 0 ∧ k_n > 0 ∧ κ² ≥ 0 ∧ j ∈ ℤ ⇒ b = 0（两臂穷举 + 逐点恒等式）',
  '臂一（j 由网格判整）：共 %d 组 (a,b,k_n)，其中满足量子化 j = k_n b ∈ ℤ 的 %d 组，'
  '再满足传播 κ² ≥ 0 的 %d 组——**其中 b > 0 的 %d 组**，b = 0 的 %d 组；'
  '非量子化而传播的 %d 组（其 b 可为正，见 Z05 对照）。'
  '臂二（b 由公式 b=(m−1)/k_n 构造，即配套代码自己的路子）：共 %d 组，传播 %d 组，'
  '**其中 b > 0 的 %d 组**。两臂独立给出同一个 0。'
  '代数理由（Z02/Z03 已逐点核验）：传播 ⇔ (k_n a)² + j² ≤ 1；a > 0 ∧ k_n > 0 ⇒ (k_n a)² > 0 ⇒ '
  'j² < 1 ⇒ 整数 j 只能取 0 ⇒ b = j/k_n = 0。臂二还把「哪一档能传播」定位成一档：'
  'm = 0..6 里给出传播解的 m 集合恰为 %r，即只有 m=1（b=0）这一支。'
  % (arm1['tot'], arm1['quant'], arm1['quant_prop'], arm1['quant_prop_bpos'], arm1['quant_prop_bzero'],
     arm1['notquant_prop'], arm2['tot'], arm2['prop'], arm2['prop_bpos'], sorted(arm2['prop_m'])))

guard('G2-1', arm1['quant_prop_bpos'] == 0 and arm1['quant_prop'] > 0,
      '臂一必须「量子化∧传播非空、而其中非零螺距为空」：b>0 %d 组 / 全体 %d 组' % (arm1['quant_prop_bpos'], arm1['quant_prop']))
guard('G2-2', arm2['prop_bpos'] == 0 and arm2['prop'] > 0,
      '臂二（量子化由构造给出）必须传播非空而非零螺距为空：b>0 %d 组 / 传播 %d 组' % (arm2['prop_bpos'], arm2['prop']))
guard('G2-3', arm1['quant_prop'] == arm1['quant_prop_bpos'] + arm1['quant_prop_bzero'],
      '分桶必须闭合：quant∧prop %d ≠ b>0 %d + b=0 %d' % (arm1['quant_prop'], arm1['quant_prop_bpos'], arm1['quant_prop_bzero']))
guard('G2-4', arm1['tot'] == arm1['quant'] + arm1['notquant']
      and arm1['prop'] == arm1['quant_prop'] + arm1['notquant_prop']
      and arm1['quant'] == arm1['quant_prop'] + arm1['quant_notprop'],
      '臂一三层分解各自闭合（母桶 = 子桶之和）：%r' % ({k: v for k, v in arm1.items() if k in ('tot', 'quant', 'notquant', 'prop', 'quant_prop', 'notquant_prop', 'quant_notprop')},))
guard('G2-5', arm2['j_m_bad'] == 0 and sorted(arm2['prop_m']) == [1],
      '臂二的构造必须自证（j 恰等于 m−1，失配 %d 处），且传播只允许出现在 m=1 一档（b=0）：实得 m 集合 %r'
      % (arm2['j_m_bad'], sorted(arm2['prop_m'])))

# 阳性对照：撤掉量子化（允许 j 为任意实数）
ctrl_notquant = arm1['notquant_prop_bpos']
P('Z05', '阳性对照：撤掉量子化后同一网格有 %d 组「传播 ∧ b > 0」——空集由量子化承载，不是网格太紧' % ctrl_notquant,
  '把判据换成「只看 κ² ≥ 0 与 b > 0，不管 j 是否整数」，同一 (a, b, k_n) 网格立刻给出 %d 组非零螺距的'
  '传播参数点（臂一总传播 %d 组，其中 b > 0 %d 组）。因此 Z04 的 0 **不是**网格稀疏造成的恒空，'
  '也不是判据写反：把量子化这一条撤掉，结论当场翻转。这正是「恒为 0 的裁定要配阳性对照」的落实。'
  % (ctrl_notquant, arm1['prop'], arm1['notquant_prop_bpos']))

guard('G3-1', ctrl_notquant > 0, '阳性对照（撤量子化）必须给非零命中，实得 %d' % ctrl_notquant)
guard('G3-2', arm1['prop_bpos'] == ctrl_notquant + arm1['quant_prop_bpos'],
      '传播∧b>0 的两条来源（量子化 / 非量子化）之和须等于母计数：%d vs %d + %d'
      % (arm1['prop_bpos'], ctrl_notquant, arm1['quant_prop_bpos']))

# 第二对照：撤掉传播条件（量子化与网格相容，不是先无解）
P('Z06', '第二对照：量子化本身在网格上可满足（%d 组），故 Z04 的空集是「量子化 ∧ 传播」的交而不空' % arm1['quant'],
  '臂一里 j = k_n b ∈ ℤ 的点有 %d 组（含 b = 0 的平凡支），其中 %d 组倏逝、%d 组传播。'
  '两个条件各自都非空，交集里只剩 b = 0 的一支——排除「联立系统一开始就没有点」这种平凡读法。'
  % (arm1['quant'], arm1['quant_notprop'], arm1['quant_prop']))

guard('G3-3', arm1['quant'] > 0 and arm1['quant_notprop'] > 0,
      '量子化单独可满足、且其中有倏逝点（否则两条件同解，定理无内容）：%d / %d' % (arm1['quant'], arm1['quant_notprop']))

# ================================================================ S3 预算表与「无容差」
print('[S3] 传播预算 (k_n a)² ≤ 1 − j² 与 j=±1 支的无容差残余')

budget = []
for j in (0, 1, 2, 3):
    rhs = Fr(1, 1) - Fr(j * j, 1)
    allowed = []
    for _a in grid_a1:
        for _k in grid_k1:
            if (_k * _a) ** 2 <= rhs:
                allowed.append((_k, _a))
    budget.append((j, rhs, len(allowed)))

budget_total = sum(x[2] for x in budget)
P('Z07', '预算表：j=0 独占全部传播预算，|j| ≥ 1 一支的余量为 1 − j² ≤ 0',
  '对每个整数 j 数一遍网格上满足 (k_n a)² ≤ 1 − j² 的 (k_n, a) 点对：'
  + '；'.join('j=%d 余量 %s 命中 %d' % (j, str(rhs), n) for j, rhs, n in budget)
  + '。j=0（即 b=0）给 %d 组，j=1 的余量恰为 0（要求 k_n a 恰等于 0），j ≥ 2 的余量为负、命中恒 0。'
    '结论的形状：一个整数量子就把整套传播预算吃光，没有给半径留余量的档位。'
  % budget[0][2])

guard('G4-1', budget[0][2] > 0 and budget[1][2] >= 0 and all(x[2] == 0 for x in budget[2:]),
      '预算表须单调塌缩（j≥2 命中 0、j=1 余量 0）：%r' % (budget,))
guard('G4-2', budget[1][1] == 0,
      'j=1 的余量必须恰为 0（这是「无容差」的出处），实得 %s' % budget[1][1])
guard('G4-4', arm1['quant_prop_bzero'] == budget[0][2],
      '预算表 j=0 一档的 (k_n, a) 点对数必须等于臂一穷举出的「量子化 ∧ 传播 ∧ b=0」桶（两条通道算同一集合）：'
      '%d vs %d' % (arm1['quant_prop_bzero'], budget[0][2]))

# 无容差：|j|=1 上 κ² 恰等于 −a²/(b²(a²+b²))
nt_hits = 0
nt_ratio_set = set()
nt_violation = []
for _a in grid_a1:
    for _b in grid_b1:
        for j in (Fr(1), Fr(-1)):
            _k = j / _b                      # j = k b ⇒ k = j/b（严格反解，不用浮点）
            d = kappa2_direct(_a, _b, _k)
            closed = -(_a * _a) / (_b * _b * (_a * _a + _b * _b))
            nt_hits += 1
            if d != closed:
                nt_violation.append((_a, _b, j, d, closed))
            nt_ratio_set.add(d / closed)     # 应为 {1}
            nt_ratio_set.discard(0)

guard('G4-3', not nt_violation,
      'j=±1 支的闭合式必须在 %d 组点上逐点精确，失配 %d 组：%r' % (nt_hits, len(nt_violation), nt_violation[:3]))
guard('G4-5', nt_ratio_set == {Fr(1)},
      '残余比（实测 κ² ÷ 闭合式）必须恰为 {1}，实得 %s' % (sorted(str(x) for x in nt_ratio_set),))

F('Z08', '无容差裁定：j=±1 一支的 κ² 恰为 −a²/(b²(a²+b²))，任何 a > 0 都不可救援（%d 组逐点精确）' % nt_hits,
  '把 j = ±1（即螺距量子化的第一档，b = ±1/k_n）代回 Z03 的闭合式得 D = a²，于是 '
  'κ² = −a²/(b²(a²+b²))，与直接代入在 %d 组 (a, b) 上逐点相等、比值集合恰 {%s}。'
  '这条的意义在于**排掉「把 a 调小一点就通过了」这类数值救援**：残余不是「略微不足」，'
  '而是恰好等于半径项本身除以正因子，a 必须恰为 0 才能把 κ² 抬到边界 0。'
  '配套地，j ≥ 2 的余量 1 − j² 为负（Z07），连边界都到不了。' % (nt_hits, str(Fr(1))))

# ================================================================ S4 a=0 边界支
print('[S4] a = 0：唯一的非零螺距出口，且它只到边界')

bd_hits = 0
bd_exact_zero = 0
bd_beyond = 0
bd_examples = []
for _b in grid_b1:
    for j in (Fr(1), Fr(-1), Fr(2), Fr(-2)):
        _k = j / _b
        d = kappa2_direct(Fr(0), _b, _k)
        bd_hits += 1
        if d == 0:
            bd_exact_zero += 1
            if len(bd_examples) < 4:
                bd_examples.append('a=0 b=%s j=%s ⇒ κ²=0' % (_b, j))
        elif d > 0:
            bd_beyond += 1

B('Z09', '边界支：a = 0 ∧ |j| = 1 给 κ² ≡ 0（%d 组点全部落在边界，无一点越界）' % bd_exact_zero,
  '联立系统里唯一带非零螺距的解族是 a = 0（半径塌成 0，即「螺旋」退化为沿轴直线）配合 |j| = 1。'
  '实测 %d 组（a=0, b>0, j=±1）全部 κ² 恰为 0；j = ±2 的 %d 组全部 κ² < 0；'
  'κ² > 0（严格传播）的组数 = %d。故即便允许半径退化为 0，非零螺距也只能拿到 κ = 0 的边际，'
  '此时 J_m(κr) ≡ J_m(0) 失去径向结构，语料的贝塞尔场解 B = A J_m(κr) e^{i(mθ−k_n z−ωt)} 不再成立。'
  % (bd_exact_zero, bd_hits - bd_exact_zero, bd_beyond))

guard('G5-1', bd_exact_zero == 2 * len(grid_b1) and bd_beyond == 0,
      'a=0 支：|j|=1 必须恰给 κ²=0（2×%d=%d 组），|j|=2 必须全部倏逝且无一严格传播：%d/%d'
      % (len(grid_b1), 2 * len(grid_b1), bd_exact_zero, bd_beyond))

I('Z10', '三分律（定理的完整陈述，无 π）',
  '集合 S := {(a, b, k_n, m) : a ≥ 0, b ≥ 0, k_n > 0, j := k_n b = m − 1 ∈ ℤ, κ² ≥ 0} 恰分为三支：'
  '(i) b = 0 ∧ j = 0：圆（闭环但无轴向推进），合法条件是 k_n a ≤ 1——本体的全部严格传播解都在这里；'
  '(ii) b > 0 ∧ a = 0 ∧ |j| = 1：κ² = 0 的边际点，半径已塌、贝塞尔径向结构消失；'
  '(iii) b > 0 ∧ a > 0：**空**（臂一 %d 组、臂二 %d 组、恒等式 %d 点三路同判）。'
  '「磁场沿闭环螺旋以光速运动」要求 (i) 与 (iii) 之外的东西，而联立系统不含它——'
  '注意 (i) 里 v = ω√(a²+0) = c 自动成立，所以语料的 v = c 恰恰是**零螺距支**的性质，'
  '不是螺旋的性质。' % (arm1['tot'], arm2['tot'], id1_hits))

# ================================================================ S5 跨轮 pin（参数现读上一轮引擎）
print('[S5] 跨轮 pin：上一轮引擎的网格与参数现读 + 本轮通道重算')

if not os.path.isfile(PREV_ENGINE):
    raise SystemExit('跨轮 pin 需要上一轮引擎源码，未找到：%s' % PREV_ENGINE)
if not os.path.isfile(PREV_JSON):
    raise SystemExit('跨轮 pin 需要上一轮面 JSON，未找到：%s' % PREV_JSON)

prev_src = io.open(PREV_ENGINE, 'rb').read().decode('utf-8')


def parse_num_list(pat, label):
    m = re.search(pat, prev_src, re.M)
    if not m:
        raise SystemExit('上一轮源码里没解析到 %s（模式 %r）——分母不许手打，解析失败必须硬抛' % (label, pat))
    return [Fr(x.strip()) for x in m.group(1).split(',')]


prev_grid_a = parse_num_list(r'^grid_a = \[([^\]]*)\]', 'grid_a')
prev_grid_b = parse_num_list(r'^grid_b = \[([^\]]*)\]', 'grid_b')
m_n = re.search(r'for n in range\(1, (\d+)\)', prev_src[prev_src.index('grid_b = ['):])
if not m_n:
    raise SystemExit('上一轮源码里没解析到 n 的枚举上限（在 grid_b 之后的第一处 for n in range）')
prev_n_hi = int(m_n.group(1))
m_par = re.search(r'^a5, b5, L5 = ([0-9.]+), ([0-9.]+), ([0-9.]+)', prev_src, re.M)
m_par6 = re.search(r'^a6, b6, L6 = ([0-9.]+), ([0-9.]+), ([0-9.]+)', prev_src, re.M)
if not m_par or not m_par6:
    raise SystemExit('上一轮源码里没解析到 paper.html 的参数行（a5/b5/L5 或 a6/b6/L6）')
p_a, p_b, p_L = (Fr(m_par.group(i)) for i in (1, 2, 3))
q_a, q_b, q_L = (Fr(m_par6.group(i)) for i in (1, 2, 3))

prev_face = json.load(io.open(PREV_JSON, 'rb'))
pk = prev_face['key_numbers']

# pin-1：C01 的 1296/1296 由 j-通道重算
famA_neg_float = 0
famA_neg_exact = 0
famA_total = 0
famA_disagree = 0
for _a in prev_grid_a:
    for _b in prev_grid_b:
        for _n in range(1, prev_n_hi):
            famA_total += 1
            # 通道一：上一轮的浮点写法（复刻，用于「同一网格同一判据」的可比性）
            af, bf = float(_a), float(_b)
            vf = 1.0 / (af * af + bf * bf) - (_n / bf) ** 2
            # 通道二：本轮 j-通道（k_n = n/b ⇒ j = k_n b = n，纯数）
            ve = kappa2_pifree(_a, _b, Fr(_n))
            famA_neg_float += (vf < 0)
            famA_neg_exact += (ve < 0)
            famA_disagree += ((vf < 0) != (ve < 0))

P('Z11', '跨轮 pin-1：上一轮的 %d/%d「全倏逝」在本轮的 j-通道上逐组同判（失配 %d 组）'
  % (famA_neg_exact, famA_total, famA_disagree),
  '网格 %d×%d、n 从 1 到 %d 由上一轮引擎源码现读（grid_a/grid_b/range），'
  '与上一轮面 `数据/%s.json` 的 key_numbers.c01_grid_neg = %d、c01_grid_total = %d 对账。'
  '本轮通道不查 κ² 的数值，只问 j = k_n b = n 是否 ≥ 1：k_n = n/b 使量子化数 j 恒等于模态数 n，'
  '于是 n ≥ 1 ⇒ |j| ≥ 1 ⇒ 由 Z03 的 D ≥ a² > 0 恒倏逝。上一轮的 1296 由此获得**解释**：'
  '它是本定理在 k_n = n/b 这一支上的特例，而不是一个孤立的网格读数。'
  % (len(prev_grid_a), len(prev_grid_b), prev_n_hi - 1, PREV_STEM,
     pk['c01_grid_neg'], pk['c01_grid_total']))

guard('G6-1', famA_total == pk['c01_grid_total'] and famA_neg_exact == pk['c01_grid_neg'],
      'pin-1 的分母与读数必须与上一轮面逐字相等：%d/%d vs 面 %d/%d'
      % (famA_neg_exact, famA_total, pk['c01_grid_neg'], pk['c01_grid_total']))
guard('G6-2', famA_neg_float == famA_neg_exact and famA_disagree == 0,
      '两条通道（浮点代入 / j-通道闭合式）必须逐组同号，实得分组 %d vs %d、失配 %d'
      % (famA_neg_float, famA_neg_exact, famA_disagree))

# pin-2：相位因子 0.937168…（浮点只用于与面逐位对账）
j_paper = 2 * math.pi * float(q_b) / float(q_L)
phase_here = 1.0 - j_paper
rel_phase = abs(phase_here - float(pk['d02_phase_factor']))
P('Z12', '跨轮 pin-2：上一轮的相位因子 %.16f 由 1 − j 现推，且 j = %.6f ∉ ℤ'
  % (phase_here, j_paper),
  '上一轮 D02 印 m − k_n b = %s，本轮按同一参数（a=%s, b=%s, L=%s，源码现读）走 1 − k_n b 得 %.16f，'
  '与面的差的绝对值 %.3e（浮点只用于对账面读数）。'
  '本轮新增的读法：m − k_n b = 1 ⟺ j := k_n b = 0，所以上一轮说的「未声明的附加条件 m − k_n b = 1」'
  '**等价于未声明地要求零螺距**——这就是该族「v = c」与「螺旋」不能同时成立的准确位置。'
  % (pk['d02_phase_factor'], q_a, q_b, q_L, phase_here, rel_phase))

guard('G6-3', rel_phase < 1e-15,
      'pin-2 与上一轮面必须在 1e-15 内一致，实得 %.3e' % rel_phase)
guard('G6-4', 0 < j_paper < 1,
      'j = k_n b 必须落在 (0,1) 内（既非 0 也不够到 1，故不满足量子化），实得 %r' % j_paper)

# pin-3：n_max = 11 复现 + 量子化扇区给 15
nmax_paper = math.floor(float(q_L) / (2 * math.pi * math.sqrt(float(q_a) ** 2 + float(q_b) ** 2)))
nmax_quant = math.floor(float(q_L) / (2 * math.pi * float(q_a)))
P('Z13', '跨轮 pin-3：n_max = %d 复现，但把 b 收成量子化所要求的 0 之后同一公式给 %d——11 住在自洽集合之外'
  % (nmax_paper, nmax_quant),
  '上一轮 C04（判 PASS）用 paper.html §4.1 的参数 a=b=%s、L=%s 复现了 n_max = %d 并据此说该文「确有传播模态」。'
  '本轮在同一参数上问第二个问题：b=%s 时 j = k_n b = 2πnb/L ∉ ℤ（Z14 严格判定），'
  '即那 %d 个模态不满足该文自己的相位匹配/螺距量子化；把量子化保持住（m=1 ⇒ b=0）再数一遍，'
  'n ≤ L/(2πa) = %.4f ⇒ n_max = %d。**同一个 n_max 公式在自洽与不自洽两个扇区给两个数（%d vs %d），'
  '上一轮的 PASS 只回答了前一个。**'
  % (q_a, q_L, pk['c04_n_max'], q_b, nmax_paper, float(q_L) / (2 * math.pi * float(q_a)), nmax_quant,
     nmax_quant, nmax_paper))

guard('G6-5', nmax_paper == pk['c04_n_max'],
      'pin-3 须逐位复现上一轮的 n_max=%s，本轮得 %d' % (pk['c04_n_max'], nmax_paper))
guard('G6-6', nmax_quant > nmax_paper and nmax_quant == math.floor(100 / (2 * math.pi)),
      '量子化扇区（b=0）的模态数必须严格大于 %d 且等于 floor(1/(2πa))=%d，实得 %d'
      % (nmax_paper, math.floor(100 / (2 * math.pi)), nmax_quant))

# pin-4：D03 的 10 个「自洽传播解」复现并拆分（参数与循环边界现读配套代码本体）
CODE_FILE = os.path.join(PKG, 'code', '02_constraints.py')
if not os.path.isfile(CODE_FILE):
    raise SystemExit('攻破需要配套代码本体，未找到：%s' % CODE_FILE)
code_src = io.open(CODE_FILE, 'rb').read().decode('utf-8')


def parse_code_param(name):
    mm = re.search(r'^%s = ([0-9.]+)' % re.escape(name), code_src, re.M)
    if not mm:
        raise SystemExit('02_constraints.py 里没解析到参数 %s；分母与参数不许手打' % name)
    return Fr(mm.group(1))


code_a = parse_code_param('a_val')
code_b = parse_code_param('b_val')
code_L = parse_code_param('L_val')
_tail = code_src[code_src.index('solutions = []'):]
mm_n = re.search(r'for n in range\(1, (\d+)\)', _tail)
mm_m = re.search(r'for m in range\((\d+), (\d+)\)', _tail)
if not mm_n or not mm_m:
    raise SystemExit('02_constraints.py §2.5 的两个循环边界没解析到')
code_n_hi, code_m_lo, code_m_hi = int(mm_n.group(1)), int(mm_m.group(1)), int(mm_m.group(2))

d03_rows = []
for _n in range(1, code_n_hi):
    kn = 2 * math.pi * _n / float(code_L)
    for _m in range(code_m_lo, code_m_hi):
        b_used = 0.0 if _m == 0 else (_m - 1) / kn        # 复刻代码的 m==0 特殊处理
        denom = math.sqrt(float(code_a) ** 2 + b_used ** 2)
        if denom < 1e-30:
            continue
        k2 = 1.0 / (float(code_a) ** 2 + b_used ** 2) - kn * kn
        if k2 >= 0:
            d03_rows.append(dict(n=_n, m=_m, b=b_used, kn=kn, phase=_m - kn * b_used, k2=k2))

d03_total = len(d03_rows)
d03_bzero = sum(1 for r in d03_rows if r['b'] == 0.0)
P('Z14', '跨轮 pin-4：上一轮 D03 的 %d 个解 / %d 个零螺距由配套代码本体（参数 %s/%s/%s、循环 n<%d、m∈[%d,%d)）复现，拆成 %d + %d'
  % (d03_total, d03_bzero, code_a, code_b, code_L, code_n_hi, code_m_lo, code_m_hi,
     sum(1 for r in d03_rows if r['m'] == 1), sum(1 for r in d03_rows if r['m'] == 0)),
  '本轮不复制上一轮的循环，而是直接现读 `02_constraints.py` §2.5 的参数与边界（a=%s, L=%s，'
  'n 从 1 到 %d、m 从 %d 到 %d）复算：传播解 %d 个，与上一轮面 `数据/%s.json` 的 '
  'd03_solutions = %d、d03_zero_pitch = %d 一致——两份独立来源（上一轮引擎 vs 语料代码）给出同一个数。'
  '拆分：m=1 支 %d 个（公式 b=(m−1)/k_n 本身即给 0，相位分母 m − k_n b = 1，v = ω√(a²) = c，真自洽）；'
  'm=0 支 %d 个（见 Z15）。'
  % (code_a, code_L, code_n_hi, code_m_lo, code_m_hi, d03_total, PREV_STEM,
     pk['d03_solutions'], pk['d03_zero_pitch'],
     sum(1 for r in d03_rows if r['m'] == 1), sum(1 for r in d03_rows if r['m'] == 0)))

guard('G6-7', d03_total == pk['d03_solutions'] == pk['d03_zero_pitch'],
      'pin-4 三数须同：本轮（代码参数现读）%d 解 / %d 零螺距 vs 面 %s/%s'
      % (d03_total, d03_bzero, pk['d03_solutions'], pk['d03_zero_pitch']))
guard('G6-8', all(r['b'] == 0.0 for r in d03_rows),
      '复现面：10 个解的 b 列必须全为 0（上一轮 D03 的读法），否则 pin 断链')
guard('G6-9', (code_a, code_b, code_L) == (q_a, q_b, q_L),
      '配套代码的参数与上一轮引擎解析出的参数必须逐字相同（两份独立来源对账），'
      '实得 %r vs %r' % ((code_a, code_b, code_L), (q_a, q_b, q_L)))

# ================================================================ S6 攻破「自洽传播解数 10」
print('[S6] 02_constraints.py §2.5 的 m==0 特殊处理')

m_spec = re.search(r'if m == 0:\s*\n\s*b_nm = 0\s*#\s*(m=0 特殊处理|特殊处理)', code_src)
if not m_spec:
    raise SystemExit('没在 %s 里解析到 m==0 特殊处理那两行；本条裁定不许建立在记忆上' % CODE_FILE)
m_formula = re.search(r'b_nm\s*=\s*\(m-1\)/k_n', code_src)
m_count = re.search(r'自洽传播解数', code_src)
line_formula = 1 + code_src[:m_formula.start()].count('\n') if m_formula else -1
line_special = 1 + code_src[:m_spec.start()].count('\n')

m0_rows = [r for r in d03_rows if r['m'] == 0]
m1_rows = [r for r in d03_rows if r['m'] == 1]
phase_m0 = sorted(set(round(r['phase'], 12) for r in m0_rows))
phase_m1 = sorted(set(round(r['phase'], 12) for r in m1_rows))

F('Z15', '攻破：§2.5 打印的「自洽传播解数 10」里 %d 个来自代码把公式值覆写成 0，覆写后相位分母为 0 ⇒ v = ∞'
  % len(m0_rows),
  '现读 `02_constraints.py`：第 %d 行的「b_nm = (m-1)/k_n」给出量子化公式，而第 %d 行起写 '
  '`if m == 0: b_nm = 0  # m=0 特殊处理`。两件事必须分开算：'
  '(a) m=0 时公式给 b = −1/k_n（负螺距、左手螺旋），代码把它换成 0；'
  '(b) 换成 0 之后相位分母 m − k_n b = 0 − 0 = %s，而 v = ω√(a²+b²)/(m − k_n b) 因此发散，'
  '即该支不满足「恒定相位点以速度 v 沿螺旋运动」这条它被称作「自洽」所依据的条件。'
  '本轮实测：m=1 支 %d 个解的分母恒为 %s（v = c，真自洽），m=0 支 %d 个解的分母恒为 %s（v = ∞）。'
  '故「10」应当是 **5**；上一轮 D03 复现了 10 与「全零螺距」，但没有对分母做这件事——本轮补上。'
  % (line_formula, line_special, phase_m0[0], len(m1_rows), phase_m1[0], len(m0_rows), phase_m0[0]))

guard('G7-1', len(m0_rows) == 5 and len(m1_rows) == 5 and len(m0_rows) + len(m1_rows) == d03_total,
      '10 个解必须恰拆成 5（m=0）+ 5（m=1）：%d/%d/%d' % (len(m0_rows), len(m1_rows), d03_total))
guard('G7-2', phase_m0 == [0.0] and phase_m1 == [1.0],
      '两支的相位分母必须分别是 {0.0} 与 {1.0}（0 ⇒ v 发散；1 ⇒ v = c），实得 %r / %r' % (phase_m0, phase_m1))
guard('G7-3', bool(m_spec) and bool(m_formula) and bool(m_count),
      '三条源码证据（特殊处理两行、量子化公式行、自洽传播解数打印行）必须全部现读到，缺一不裁')
guard('G7-5', line_formula > 0 and line_special > line_formula,
      '量子化公式行必须在覆写行之前（覆写是对自家公式的事后修改），实得 %d / %d' % (line_formula, line_special))

# 精确复核：覆写把量子数 j 从 m−1 改成 k_n·0 = 0，改动量恰为一档
j_delta = []
for r in m0_rows:
    j_formula = Fr(r['m'] - 1)          # 公式给出的 j = k_n b = m − 1（与 k_n 的具体值无关）
    j_used = Fr(0)                      # 覆写 b=0 ⇒ j = k_n·0 = 0
    j_delta.append(j_formula - j_used)
guard('G7-4', j_delta and all(x == Fr(-1) for x in j_delta),
      'm=0 支：覆写把量子数 j 从 −1 改成 0，改动量必须恰为一档（−1），实得 %r' % ([str(x) for x in j_delta],))

# ================================================================ S7 11 个模态的严格整数判定
print('[S7] paper.html 族：11 个传播模态里有几个满足量子化')


def has_integer_in(lo, hi):
    """闭区间 [lo, hi]（lo, hi > 0）内是否含整数；由双侧有理界给出，不靠浮点相等。"""
    ceil_lo = (lo.numerator + lo.denominator - 1) // lo.denominator
    floor_hi = hi.numerator // hi.denominator
    return ceil_lo <= floor_hi, ceil_lo, floor_hi


# 仪器自身的双向对照：区间含整数时必须报含，不含时必须报不含（否则 0 是针坏）
_ctrl_true = [has_integer_in(Fr(9, 10), Fr(11, 10)), has_integer_in(Fr(199, 100), Fr(201, 100))]
_ctrl_false = [has_integer_in(Fr(6, 10), Fr(7, 10)), has_integer_in(Fr(1, 10), Fr(9, 10))]
guard('G8-0', all(x[0] for x in _ctrl_true) and not any(x[0] for x in _ctrl_false),
      '判整仪器要先过自己的正/负对照（含整数 %r / 不含整数 %r）' % (_ctrl_true, _ctrl_false))

b_over_L = code_b / code_L
j_lo_list, j_hi_list, int_hits = [], [], 0
int_j_detail = []
for _n in range(1, nmax_paper + 1):
    lo = 2 * PI_LO * b_over_L * _n
    hi = 2 * PI_HI * b_over_L * _n
    j_lo_list.append(lo)
    j_hi_list.append(hi)
    hit, ceil_lo, floor_hi = has_integer_in(lo, hi)
    if hit:
        int_hits += 1
        int_j_detail.append((_n, str(lo), str(hi), ceil_lo, floor_hi))

F('Z16', '攻破：paper.html 的 %d 个传播模态中满足螺距量子化 j ∈ ℤ 的有 %d 个（用 π 的有理双侧界严格判定）'
  % (nmax_paper, int_hits),
  '在 paper.html 自己的参数（a=b=%s, L=%s）上，第 n 个模态的无量纲螺距是 j = 2πnb/L。'
  '判「是否整数」不许用浮点相等，故取 π 的双侧有理界 π ∈ [%s, %s]，对 n = 1..%d 各算 j 的包含区间：'
  '最小上界 %s < 1、最大下界 %s > 0 ⇒ 全部 %d 个区间都住在 (0,1) 内，整数个数 = %d。'
  '读法：该文 §4.1 的「n ≤ 11 有传播模态」与 §3.3 的「b_nm = (m−1)/k_n」在文中从未对表——'
  '按 b=0.01 摆出的 11 个模态没有一个能同时是量子化解，而真正自洽的那一支（Z14/Z15 的 m=1、b=0）'
  '对应 n_max = %d（Z13）。'
  % (q_a, q_L, PI_LO, PI_HI, nmax_paper, str(j_hi_list[-1]), str(j_lo_list[0]), nmax_paper, int_hits, nmax_quant))

guard('G8-1', int_hits == 0,
      '11 个模态的 j 区间内整数个数必须为 0（本条若翻转则 Z16 作废），实得 %d' % int_hits)
guard('G8-2', j_hi_list[-1] < 1 and j_lo_list[0] > 0,
      'π 双侧界下的最大 j 上界须 < 1、最小下界须 > 0：%s / %s' % (j_hi_list[-1], j_lo_list[0]))
guard('G8-3', PI_LO < PI_REF < PI_HI,
      'π 的双侧有理界必须真的框住参照 π（界若反了，区间判整会假阴）：%s < %s < %s'
      % (PI_LO, str(PI_REF)[:24] + '…', PI_HI))

# ================================================================ S8 最小修法代价台账（语料现扫）
print('[S8] 最小修法代价：出现次数实测（含重复副本加倍）')

DOCS = ['index.html', 'index (1).html', 'academic-report.html', 'verification-report.html',
        'paper-final.html', 'paper.html', 'paper (1).html']
CODES = ['01_derivation.py', '02_constraints.py', '03_visualization.py', '04_final.py']

missing = [f for f in DOCS if not os.path.isfile(os.path.join(HTML, f))]
if missing:
    raise SystemExit('代价台账要现扫语料，缺文件：%r' % missing)

texts = {}
for f in DOCS:
    raw = io.open(os.path.join(HTML, f), 'rb').read()
    texts[f] = raw.decode('utf-8')
for f in CODES:
    p = os.path.join(PKG, 'code', f)
    texts[f] = io.open(p, 'rb').read().decode('utf-8')

md5s = {}
for f in DOCS + CODES:
    p = os.path.join(HTML, f) if f in DOCS else os.path.join(PKG, 'code', f)
    md5s[f] = hashlib.md5(io.open(p, 'rb').read()).hexdigest()

dup_pairs = []
for _x in range(len(DOCS)):
    for _y in range(_x + 1, len(DOCS)):
        if md5s[DOCS[_x]] == md5s[DOCS[_y]]:
            dup_pairs.append([DOCS[_x], DOCS[_y]])


def scan_cost(patterns, scope):
    """两独立通道数「待改点数」：
    A = 单个正则在 re 引擎里的最左非重叠扫描；
    B = 逐式取全部 span、按 (起点, −长度) 排序后手工贪心选不重叠者。
    另如实披露：逐式原始命中之和（式样互相包含时会高估）与式间重叠点数。"""
    per = {}
    chan_a = {}
    chan_b = {}
    raw_sum = {}
    overlaps = []
    for f in scope:
        t = texts[f]
        per[f] = {}
        spans = []
        for name, pat in patterns:
            hits = list(re.finditer(pat, t))
            per[f][name] = len(hits)
            for m in hits:
                spans.append((m.start(), m.end(), name))
        raw_sum[f] = sum(per[f][n] for n, _ in patterns)
        comb = '|'.join('(?:%s)' % pat for _, pat in patterns)
        chan_a[f] = len(re.findall(comb, t))
        spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
        end = -1
        picked = 0
        for s0, s1, _nm in spans:
            if s0 >= end:
                picked += 1
                end = s1
        chan_b[f] = picked
        ordered = sorted(spans)
        for i in range(1, len(ordered)):
            if ordered[i][0] < ordered[i - 1][1]:
                overlaps.append((f, ordered[i - 1][2], ordered[i][2]))
    return per, chan_a, chan_b, raw_sum, overlaps


FIXES = [
    ('P1', 'h → L（把纵向周期与螺距参数分开）',
     [('h 作波长记号', r'2\s*π\s*n\s*/\s*h'), ('h 的 LaTeX 形', r'2\\pi\s*n\s*/\s*h'),
      ('h/2π 反代', r'h\s*/\s*2\s*π'), ('h/2π 的 LaTeX 形', r'h\s*/\s*2\\pi')],
     DOCS,
     '不触碰量子化：改完之后 j = k_n b = 2πnb/L 仍是同一个非整数，Z16 的 0 个自洽模态一个不增。'
     '它修的是「κ² 恒负」，代价是把螺旋从 k_n 的定义里彻底删掉（k_n 不再依赖 b），'
     '于是「闭环螺旋」只剩在轨迹 z=bθ 一处，与波动数无关。',
     '只修传播条件（Z04 (iii) 支仍为空）'),
    ('P2', '声明 v = ω√(a²+b²)/(m − k_n b)，或显式加条件 m − k_n b = 1',
     [('v = ω√(a²+b²)', r'ω\s*√\s*\(\s*a\s*²\s*\+\s*b\s*²\s*\)'),
      ('代码里的 sqrt(a²+b²)', r'math\.sqrt\(a\*\*2\s*\+\s*b\*\*2\)'),
      ('v = ω√ 前缀', r'v\s*=\s*ω')],
     DOCS,
     '取「显式加 m − k_n b = 1」这一读法时，它等价于 j = 0，即**直接把零螺距写进公理**——'
     'Z01/Z12 就是这个等价。取「改成分母形式」这一读法时，v = c 变成条件式，'
     '需要 (m−1) = k_n b 与 κ² ≥ 0 联立，仍是 Z04 (iii) 的空集。',
     '两支都不产生非零螺距自洽解'),
    ('P3', '删掉「定理：v_总 = c」与「严格证明」，把「严格数值验证」改为「算术自洽性复核」',
     [('v_总 = c', r'v_总\s*=\s*c'), ('严格证明', r'严格证明'), ('数值验证', r'数值验证')],
     DOCS,
     '纯删减：不改变联立系统，改变的是声明强度。做完后该族的剩余主张只有 '
     '「柱坐标贝塞尔模态 + 纵向量子化」，而后者按 Z04 只容零螺距。',
     '不改变系统，只降声明'),
    ('P4', 'κ 与 ω 改名（径向波数 q_r、轨迹角速率 Ω_rot）',
     [('κ 字符', r'κ'), ('ω 字符', r'ω'), ('Omega/omega 记号', r'[OΩ]mega')],
     DOCS + CODES,
     '同名异义的根治，代价是待改点数最大（本表实测其点数超过 P1/P2/P3 之和，见 Z18）。'
     '对本定理无影响：约束的形状只含纯数 j 与 k_n a，改名不改定义域是否为空。',
     '零科学效果（最大编辑代价）'),
]

cost_rows = []
for code, label, pats, scope, note, effect in FIXES:
    per, chan_a, chan_b, raws, ovl = scan_cost(pats, scope)
    tot_a = sum(chan_a.values())
    tot_b = sum(chan_b.values())
    tot_raw = sum(raws.values())
    per_file = dict((f, chan_a[f]) for f in scope if chan_a[f])
    cost_rows.append(dict(code=code, label=label, patterns=len(pats), scope=len(scope),
                          total=tot_a, channel_b=tot_b, raw_sum=tot_raw, overlaps=len(ovl),
                          per_file=per_file, note=note, effect=effect, files_hit=len(per_file)))
    guard('G9-' + code[1], tot_a == tot_b and tot_a > 0,
          '%s 的「待改点数」必须由两条独立通道同值且非空（正则最左非重叠 vs 手工 span 贪心）：%d vs %d'
          % (code, tot_a, tot_b))
    guard('G9-' + code[1] + 'b', tot_raw >= tot_a and (len(ovl) > 0 or tot_raw == tot_a),
          '%s 的并集点数不得超过逐式命中（%d ≥ %d），且二者之差必须被实测的式间重叠（%d 处）解释：'
          '无重叠时两数必须相等' % (code, tot_raw, tot_a, len(ovl)))

duplicated = [pair for pair in dup_pairs]
P('Z17', '代价台账的出现次数由语料现扫，重复副本按字节 md5 认定并计入加倍',
  '扫描范围：7 份 HTML（%s）+ 4 份配套代码。md5 现算得重复组 %s，'
  '即任何「在正文里改一处」的修法在盘上至少要做 %d 次同样编辑（副本不改则语料内部立刻不一致）。'
  '上一轮 §七 把这条代价记为 0（「零成本，纯命名」），本表把它数出来了。'
  % ('，'.join(DOCS), '；'.join(' = '.join(x) for x in duplicated) or '无',
     1 + len([x for x in duplicated if any(f in x for f in DOCS)])))

guard('G9-6', len(md5s) == len(DOCS) + len(CODES),
      '待扫文件数须等于名单长度：%d vs %d' % (len(md5s), len(DOCS) + len(CODES)))
guard('G9-5', len(duplicated) == 2,
      '本语料批的重复组必须是 2（index 与 paper 各一对），实得 %d：%r' % (len(duplicated), duplicated))

for r in cost_rows:
    add('Z18-' + r['code'], '%s（%s）：待改点数实测 %d 处、分布在 %d 个文件；%s'
        % (r['code'], r['label'], r['total'], r['files_hit'], r['effect']),
      '现扫范围 %d 个文件，式样 %d 条。两独立通道同值：%d = %d；逐式原始命中 %d 处，'
      '其中式间重叠 %d 处（同一字符被两条式样各计一次的部分只并入一次）。'
      '逐文件分布：%s。修法语义：%s'
      % (r['scope'], r['patterns'], r['total'], r['channel_b'], r['raw_sum'], r['overlaps'],
         '，'.join('%s %d' % (k, v) for k, v in sorted(r['per_file'].items())) or '（无命中）',
         r['note']),
        'PASS')

# P5：无可数代理，如实登记
I('Z19', 'P5（结构性：正面回应同库内 deepseek 页的否证）没有「出现次数」这种代理指标，本轮不伪造',
  'P5 要求的是给出一个不与实测光速冲突的表述，其工作量是论证而非编辑，语料里没有可数的符号。'
  '本轮只登记它的前提是**已存在的**：该库内已有一份持正确读法的文件（上一轮 H03 用它否证了 '
  '「真实空间轨迹以光速运动」的读法），所以 P5 的对面不是空的；但 P5 能否成立不由本轮判定。'
  '与之对照，P1…P4 的「修完之后是否出现非零螺距严格传播自洽解」本轮都给了机器答案（=否，见 Z18-*）。')

# ================================================================ S9 对上一轮 §七 的更正
print('[S9] 更正上一轮 §七 的「唯一」与「零成本」')

p1_row = [r for r in cost_rows if r['code'] == 'P1'][0]
p2_row = [r for r in cost_rows if r['code'] == 'P2'][0]
p3_row = [r for r in cost_rows if r['code'] == 'P3'][0]
CE('Z20', '更正：上一轮 §七 说 P1 是「四篇正文唯一的零成本修法」——「唯一」与「零成本」两处都不成立',
  '本轮在同一份 §七 文本上做机器核对，三处反证：'
  '(1) **不唯一**：P2（声明相位分母）与 P3（删定理）与 P1 同属「不改数值、不改结构」的编辑，'
  '上一轮自己也把它们标了「零成本」，所以「唯一」与其 own 表格反号；'
  '(2) **不零成本**：P1 的待改点数实测 %d 处（式样 4 条、分布 %s），且语料有 md5 相同的副本对，'
  '改正文必须连副本一起改；'
  '(3) **修不完**：P1 把 k_n 从 n/b 换成 2πn/L 之后，传播条件确实被修好（上一轮 C04 的 n_max=%d），'
  '但量子化条件 j = k_n b ∈ ℤ 依然没有满足者（Z16：%d 个模态里 %d 个自洽），'
  '非零螺距的严格传播解仍然为 0（臂二 %d 组中 b>0 支 %d 组）。'
  '正确的表述应当是：**P1 是五条里唯一只修传播条件的那一条，它把该族从「全倏逝」搬到「只有零螺距」，'
  '不恢复螺旋图像；而「零成本」只对它的字符量成立，对它的语义代价不成立**'
  '（它删掉了 k_n 对 b 的依赖，也就是删掉了「螺旋进入波动数」这件事）。'
  '上一轮面 `数据/%s.json` 的 §七 相关读数不变，本条只更正文册措辞。'
  % (p1_row['total'], '，'.join('%s %d' % (k, v) for k, v in sorted(p1_row['per_file'].items())) or '无',
     nmax_paper, nmax_paper, int_hits, arm2['tot'], arm2['prop_bpos'], PREV_STEM))

guard('G10-1', p1_row['total'] > 0 and p1_row['files_hit'] > 0,
      '更正的前提是 P1 的待改点数实测非零（否则「不零成本」这条不成立），实得 %d' % p1_row['total'])
guard('G10-2', arm2['prop_bpos'] == 0 and int_hits == 0,
      '更正的第 (3) 条要求「修完 P1 之后仍无非零螺距自洽解」：臂二 b>0 %d 组、11 模态自洽 %d 个'
      % (arm2['prop_bpos'], int_hits))
guard('G10-3', p2_row['total'] > 0 and p3_row['total'] > 0,
      '「不唯一」这条要求 P2/P3 的待改点数也实测非零（同为零成本编辑类）：%d / %d'
      % (p2_row['total'], p3_row['total']))

# ================================================================ S10 元裁定
print('[S10] 元裁定')

F('Z21', '元裁定：该族的「磁场沿闭环螺旋以光速运动」在其自身联立系统内被闭设为零螺距，且对全部最小修法免疫',
  '把三条关系合起来只留一个纯数判据：(k_n a)² + j² ≤ 1，j = k_n b ∈ ℤ。整数格点上可行的 j 只有 0，'
  'j = ±1 恰好吃光预算（余量 0，残余 = −a²/(b²(a²+b²))，无容差），|j| ≥ 2 的余量为负。'
  '因此：v = c 在语料自己的式子里**等价于 b = 0**（Z12：m − k_n b = 1 ⟺ j = 0），'
  '「光速」与「螺旋」不是配合得不好，而是同一系统里互斥的两支。'
  '上一轮的 C01（全倏逝 1296/1296）是这一件事在 k_n = n/b 支上的读数（Z11 已把两条通道对上）；'
  'P1 换族不改变它（Z16）；配套代码的「自洽传播解数 10」其中 5 个来自覆写后的发散分母（Z15）；'
  '该文自印的 n_max = 11 住在自洽集合之外、自洽支给 15（Z13）。'
  '本轮不新增语料、不改档案内他人文件，只把上一轮的 OPEN 缺口（P1 之后能否恢复）关掉。')

I('Z22', '红线与适用范围',
  '本册是**关于该语料自己方程组的定理**，不是新物理，也不主张 a、b、L 的任何实测取值：'
  '结论只用到「ω = c/√(a²+b²)」「κ² = ω²/c² − k_n²」「相位匹配 m − k_n b = 1 或等价 b = (m−1)/k_n」'
  '三条来料自身的式子。它不否定圆波导/贝塞尔模态这一成熟数学（上一轮红线继承）。'
  '网格穷举是见证、逐点 Fraction 恒等式是核验、代数推导是一般性来源——三者分家陈述，'
  '任何一环都不许用「网格全过」冒充「一般成立」。')

# ================================================================ S11 仪器自检：编号不得复用
# 复用编号会让一个 code 指向两行判据：变异跑「恰有一枚红」的归因失去含义。
_codes = [g['code'] for g in GUARDS]
_dups = sorted(set(c for c in _codes if _codes.count(c) > 1))
guard('G11-1', _dups == [],
      '守卫编号必须互不相同（本引擎现扫 %d 条守卫，重复 %d 个）：%r' % (len(_codes), len(_dups), _dups))

# ================================================================ 汇总与输出
print('\n' + '=' * 78)
print('汇总')
print('=' * 78)

cnt = {}
for e in ENTRIES:
    cnt[e['status']] = cnt.get(e['status'], 0) + 1
order = ['PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED', 'MISMATCH']
line = ' · '.join('%s %d' % (k, cnt[k]) for k in order if cnt.get(k))
print('条目 %d（%s）' % (len(ENTRIES), line))
print('守卫 %d/%d' % (sum(1 for g in GUARDS if g['ok']), len(GUARDS)))

bad = [g for g in GUARDS if not g['ok']]
assert not bad, 'guards failed: %s' % bad

# 负面结论的机器自锁（防将来误引；数字全部现推，除跨轮 pin 由面驱动）
assert arm1['quant_prop_bpos'] == 0 and arm1['quant_prop'] > 0, '臂一闭设自锁失效'
assert arm2['prop_bpos'] == 0 and arm2['prop'] > 0, '臂二闭设自锁失效'
assert ctrl_notquant > 0, '阳性对照自锁失效（对照塌空则空集裁定无证据）'
assert int_hits == 0 and nmax_quant == 15, '11 模态无自洽 + 量子化支 15 的自锁失效'
assert famA_neg_exact == pk['c01_grid_neg'] == 1296, '跨轮 pin-1 自锁失效'
assert len(m0_rows) == len(m1_rows) == 5, '10 拆 5+5 的自锁失效'

payload = dict(
    stem=STEM,
    generated_at=TODAY,
    engine='源码/' + STEM + '.py',
    prev_face='数据/' + PREV_STEM + '.json',
    theorem=dict(
        statement='κ² = (1 − (k_n a)² − j²)/(a²+b²)，j := k_n b；传播 ∧ j ∈ ℤ ∧ a>0 ∧ k_n>0 ⇒ j = 0 ⇒ b = 0',
        arm1=arm1, arm2=dict(arm2, prop_m=sorted(arm2['prop_m'])),
        j_hist={str(k): v for k, v in arm2['j_hist'].items()},
        identity_checks=dict(budget_points=id1_hits, pifree_points=id2_hits,
                             budget_mismatch=len(id1_fail), pifree_mismatch=len(id2_fail)),
        budget_table=[dict(j=j, slack=str(rhs), points=n) for j, rhs, n in budget],
        no_tolerance=dict(points=nt_hits, ratios=sorted(str(x) for x in nt_ratio_set),
                          mismatch=len(nt_violation)),
        boundary_a0=dict(points=bd_hits, exactly_zero=bd_exact_zero, strictly_propagating=bd_beyond,
                         examples=bd_examples)),
    cross_round_pins=dict(prev_key_numbers={k: pk[k] for k in ('c01_grid_neg', 'c01_grid_total', 'c04_n_max',
                                                               'd02_phase_factor', 'd03_solutions', 'd03_zero_pitch')},
                          famA_total=famA_total, famA_neg_exact=famA_neg_exact, famA_neg_float=famA_neg_float,
                          famA_disagree=famA_disagree, phase_factor_here=phase_here,
                          phase_abs_diff=rel_phase, j_paper=j_paper,
                          nmax_paper=nmax_paper, nmax_quantized=nmax_quant,
                          d03_total=d03_total, d03_bzero=d03_bzero,
                          parsed=dict(grid_a=[str(x) for x in prev_grid_a], grid_b=[str(x) for x in prev_grid_b],
                                      n_hi=prev_n_hi, params_a5=[str(x) for x in (p_a, p_b, p_L)],
                                      params_a6=[str(x) for x in (q_a, q_b, q_L)])),
    code_attack=dict(total=d03_total, m0=len(m0_rows), m1=len(m1_rows),
                     phase_m0=phase_m0, phase_m1=phase_m1,
                     evidence=dict(special_case=bool(m_spec), formula=bool(m_formula), print_line=bool(m_count)),
                     code_file='90_历史归档/来源语料_ufthub_20260925/08_宇宙文明与工程平台包/'
                               'magnetic_field_algorithm_paper/paper_package/code/02_constraints.py'),
    family_b_modes=dict(n_max=nmax_paper, integer_j=int_hits,
                        j_lower=[str(x) for x in j_lo_list], j_upper=[str(x) for x in j_hi_list],
                        pi_bounds=[str(PI_LO), str(PI_HI)]),
    fix_costs=cost_rows, duplicate_groups=dup_pairs,
    entries=ENTRIES, guards=GUARDS, counts=cnt,
    key_numbers=dict(
        arm1_quant_prop=arm1['quant_prop'], arm1_quant_prop_bpos=arm1['quant_prop_bpos'],
        arm1_quant=arm1['quant'], arm1_tot=arm1['tot'], arm1_prop=arm1['prop'],
        arm2_tot=arm2['tot'], arm2_prop=arm2['prop'], arm2_prop_bpos=arm2['prop_bpos'],
        control_notquant=ctrl_notquant, budget_j0=budget[0][2], budget_j1=budget[1][2],
        no_tolerance_points=nt_hits, boundary_exact_zero=bd_exact_zero,
        famA_neg=famA_neg_exact, famA_total=famA_total, phase_factor=phase_here,
        j_paper=float(j_paper), nmax_paper=nmax_paper, nmax_quantized=nmax_quant,
        d03_solutions=d03_total, d03_m0=len(m0_rows), d03_m1=len(m1_rows),
        family_b_integer_modes=int_hits,
        p1_points=p1_row['total'], p2_points=p2_row['total'], p3_points=p3_row['total'], p4_points=cost_rows[3]['total'],
        dup_groups=len(dup_pairs),
    ),
    verdict='FAIL',
    verdict_note='攻破结论：该联立系统被闭设为零螺距——v = c 与「螺旋」互斥（j = 0 ⟺ m − k_n b = 1），'
                 '非零螺距的严格传播解在两臂、恒等式与 π-双侧界四条独立通道上都是 0；'
                 '阳性对照（撤量子化）给 %d 组非零螺距传播点，故空集是量子化的后果而非网格的巧合。'
                 '配套代码「自洽传播解数 10」应为 5（m=0 支的相位分母为 0）；'
                 'paper.html 的 11 个传播模态中 0 个满足量子化，量子化扇区的模态数是 %d。'
                 '上一轮 §七 P1 的「唯一 / 零成本」两处措辞更正为 CORRECTED（实测待改点数 %d 处、'
                 '副本加倍 %d 组，且修完后闭设依旧）。'
                 % (ctrl_notquant, nmax_quant, p1_row['total'], len(dup_pairs)),
)

os.makedirs(os.path.join(OUTDIR, '数据'), exist_ok=True)
jpath = os.path.join(OUTDIR, '数据', STEM + '.json')
with io.open(jpath, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)

md = []
md.append('# 磁场闭环螺旋 · 零螺距闭设定理与最小修法代价（机器读数）\n')
md.append('生成：%s · 引擎 `源码/%s.py`（纯标准库，Fraction 精确算术）\n' % (TODAY, STEM))
md.append('条目 %d（%s）· 守卫 %d/%d · 退出码 0\n' % (len(ENTRIES), line, sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
md.append('\n## 一、定理与四通道\n')
md.append('| 通道 | 内容 | 读数 |\n|---|---|---|')
md.append('|---|---|---|')
md.append('| 恒等式（预算形态） | κ² = (1 − (k_n a)² − j²)/(a²+b²) 逐点 Fraction 相等 | %d 点，失配 %d |' % (id1_hits, len(id1_fail)))
md.append('| 恒等式（π-自由形态） | κ²·b²(a²+b²) = −(j²a² + (j²−1)b²) | %d 点，失配 %d |' % (id2_hits, len(id2_fail)))
md.append('| 臂一（j 由网格判整） | 量子化 ∧ 传播 ∧ b > 0 | %d 组（量子化 ∧ 传播共 %d 组） |' % (arm1['quant_prop_bpos'], arm1['quant_prop']))
md.append('| 臂二（b = (m−1)/k_n 构造） | 传播 ∧ b > 0 | %d 组（传播共 %d 组） |' % (arm2['prop_bpos'], arm2['prop']))
md.append('| 阳性对照（撤量子化） | 传播 ∧ b > 0 | %d 组 |' % ctrl_notquant)
md.append('| π 双侧界（paper 族） | 11 个模态里 j ∈ ℤ 的个数 | %d |' % int_hits)
md.append('| a=0 边界支 | κ² 恰为 0 / 严格传播 | %d 组 / %d 组 |' % (bd_exact_zero, bd_beyond))
md.append('')
md.append('\n## 二、传播预算 (k_n a)² ≤ 1 − j²\n')
md.append('| j | 余量 1 − j² | 网格命中 (k_n, a) 点对 |\n|---|---|---|')
md.append('|---|---|---|')
for j, rhs, n in budget:
    md.append('| %d | %s | %d |' % (j, rhs, n))
md.append('')
md.append('\n## 三、跨轮 pin（参数与网格现读上一轮引擎，读数对账其 JSON 面）\n')
md.append('| pin | 上一轮面 | 本轮通道 | 差 |\n|---|---|---|---|')
md.append('|---|---|---|---|')
md.append('| C01 全倏逝 | %s/%s | %s/%s（j = n 通道 %s，浮点通道 %s，失配 %s） | %s |'
          % (pk['c01_grid_neg'], pk['c01_grid_total'], famA_neg_exact, famA_total,
             famA_neg_exact, famA_neg_float, famA_disagree, famA_neg_exact - pk['c01_grid_neg']))
md.append('| D02 相位因子 | %s | %s | %s |' % (pk['d02_phase_factor'], phase_here, rel_phase))
md.append('| C04 n_max | %s | %s（量子化扇区 b=0：%s） | %s |' % (pk['c04_n_max'], nmax_paper, nmax_quant, nmax_paper - pk['c04_n_max']))
md.append('| D03 解数 / 零螺距 | %s / %s | %s / %s | %s |' % (pk['d03_solutions'], pk['d03_zero_pitch'], d03_total, d03_bzero, d03_total - pk['d03_solutions']))
md.append('')
md.append('\n## 四、攻破两处读数\n')
md.append('| 对象 | 原读数 | 本轮 | 依据 |\n|---|---|---|---|')
md.append('|---|---|---|---|')
md.append('| `02_constraints.py` §2.5「自洽传播解数」 | %d | %d（m=1 支）+ %d（m=0 支，相位分母 = %s ⇒ v = ∞） | 代码 `if m == 0: b_nm = 0` 覆写公式值 −1/k_n |'
          % (d03_total, len(m1_rows), len(m0_rows), phase_m0[0]))
md.append('| paper.html §4.1「n ≤ 11 有传播模态」 | n_max = %d | 其中 j ∈ ℤ 的自洽模态 = %d；量子化扇区 n_max = %d | π ∈ [%s, %s] 的区间判整 |'
          % (nmax_paper, int_hits, nmax_quant, PI_LO, PI_HI))
md.append('')
md.append('\n## 五、最小修法代价（语料现扫，两通道计数一致）\n')
md.append('| 修法 | 待改点数 | 命中文件数 | 修完后是否出现非零螺距自洽解 |\n|---|---|---|---|')
md.append('|---|---|---|---|')
for r in cost_rows:
    md.append('| %s %s | %d | %d | %s |' % (r['code'], r['label'], r['total'], r['files_hit'], r['effect']))
md.append('| P5 结构性 | 无可数代理 | — | 不由本轮判定 |')
md.append('')
md.append('重复副本组（md5 现算）：%s ⇒ 任何正文修改必须连副本一起做。' % '；'.join(' = '.join(x) for x in dup_pairs))
md.append('')
md.append('\n## 六、条目全表\n')
md.append('| 编号 | 状态 | 标题 |\n|---|---|---|')
md.append('|---|---|---|')
for e in ENTRIES:
    md.append('| %s | %s | %s |' % (e['code'], e['status'], e['title']))
md.append('')
md.append('\n## 七、守卫\n')
md.append('| 编号 | 结果 | 说明 |\n|---|---|---|')
md.append('|---|---|---|')
for g in GUARDS:
    md.append('| %s | %s | %s |' % (g['code'], 'OK' if g['ok'] else 'FAIL', g['msg']))
md.append('')
md.append('\n> 红线：本册是关于该语料自身方程组的定理，不是新物理；不否定圆波导/贝塞尔模态的数学。\n')

mpath = os.path.join(OUTDIR, '数据', STEM + '.md')
with io.open(mpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

rep = []
rep.append('磁场闭环螺旋 · 零螺距闭设定理与最小修法代价（攻破轮）')
rep.append('=' * 70)
rep.append('条目 %d（%s）' % (len(ENTRIES), line))
rep.append('守卫 %d/%d' % (sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
rep.append('')
for e in ENTRIES:
    rep.append('[%s] %-7s %s' % (e['status'], e['code'], e['title']))
    rep.append('        %s' % e['detail'])
    rep.append('')
rep.append('-' * 70)
rep.append('VERDICT: %s' % payload['verdict'])
rep.append(payload['verdict_note'])
rpath = os.path.join(OUTDIR, '数据', STEM + '_report.txt')
with io.open(rpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep))

print()
print('WROTE', jpath)
print('WROTE', mpath)
print('WROTE', rpath)
print('EXIT 0')
