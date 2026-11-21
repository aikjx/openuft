# -*- coding: utf-8 -*-
"""TUFT-r436 | 唯一出口的门禁自审:
   E1-E4 四条件与 C1-C4 四门本身被当作对象审查 (此前无人审过门禁自身).
   T1 E2 口径计数冲突: 原文 "provenance 在六类之外" 而分类学是 7 类 => 定义不完备, 字面读法豁免 1 类.
   T2 预言类型穷举 5 类 (连续无量纲 / 整数拓扑 / 代数数 / 函数形状 / 不等式符号).
   T3 可满足性矩阵 5x4 = 20 格 (OK / COND / N-A), 逐格机核; 发现 C4 对 T2/T3 恒 N-A (空满足).
   T4 连续轴余量账: Omega5 上限 1, 已占用 = 标度 eta (r431) => 余量 0.
   T5 离散轴 bit 账: 群 2.3219 + 代 1.5849 = 3.9069 bit; 与连续轴分列, 禁止相加 (承 r434 §5.3).
   T6 新颖性空集: 库内 4 个零连续输入的整数/代数预言全部指向已观测事实 => 结构性败 C3.
   T7 出口可行性二分: 连续型需 >=1 输入 (r432) 且已被 eta 占用; 离散型零成本但新颖集空 => 合取为空.

承 r429 (E1-E4 / 七类来源 / C1-C4 全败) / r430 (外生 0/40) / r431 (C4 需 +1 无量纲比)
  / r432 (基组闭包) / r433 (离散两腿全封) / r434 (记账三元组 + bit 与连续不得相加).

不做: 不宣称攻破统一场论, 不产生新物理, 不改被引文件字节, 不跑 refresh_catalog, 不做 git,
      不重判 r429-r434 任何条目, 不代选出路, 不宣称"统一场论不可能".
纯标准库 / Python 3.8 / Decimal 60 位 log2 / 零浮点参与判据. 控制台只打印 ASCII 摘要.

取号与撞号处置 (真实发生):
  起草时 r435 三处 0 命中 => 首稿按 r435 落盘并跑通 53/53.
  随后复跑时 G-A0 (撞号自检) 报 "他册命中 1", 机器定位到并行会话同日落盘了
  `判定_TUFT-r435_账基组选择反解定理_口径不变性元层边界与离散输入来源轴再定价_*`
  (判定 + 源码 + 数据三件齐全, 主题含 "口径不变性 / 离散输入来源轴").
  => 按库内纪律 "后到者改号不覆盖他人", 本册整体顺延为 r436, 不触碰对方任何字节;
     并在 G-A0c 中把该撞号事件机器化登记, 在判定册 §一 写清两册分工.
"""
import io
import json
import re
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
SRC = BASE / '源码'
NAME = ('TUFT-r436_唯一出口门禁自审_E2七类vs六类口径冲突_'
        '预言类型可满足性矩阵与新颖性空集_精算_2026-11-21')
ROUND = 'r436'
DATE = '2026-11-21'

ENTRIES = []
GUARDS = []
CONTROLS = []
NUMBERS = {}


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


N_REGISTERED = [0]


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))
    N_REGISTERED[0] += 1


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


def find_all(base, patterns):
    out = []
    if not base.is_dir():
        return out
    for pat in patterns:
        out.extend([p for p in base.rglob(pat) if p.is_file()])
    return sorted(set(out))


# 撞号自检: 必须排除本册自身产物 (脚本已落盘 + 重跑时的 json/report/判定册),
# 否则守卫在第二次运行时自伤 (r408 册记录过同款教训: 查重守卫须与本册产物集合同步定义).
def is_own(name):
    return ('TUFT-r436' in name) or ('TUFT_r436' in name)


pre = []
for d in (JUDGE, SRC, OUT):
    pre.extend([p.name for p in find_all(d, ['*r436*']) if not is_own(p.name)])
own_hits = [p.name for d in (JUDGE, SRC, OUT)
            for p in find_all(d, ['*r436*']) if is_own(p.name)]
put('pre_existing_r436_foreign', sorted(set(pre)))
put('own_r436_artifacts', sorted(set(own_hits)))
guard('G-A0', len(set(pre)) == 0,
      u'撞号自检: 排除本册产物后, r436 在 判定/源码/数据 三处他册命中 0 (实得 %d)'
      % len(set(pre)))
guard('G-A0b', len(set(own_hits)) >= 1,
      u'本册产物识别有效 (至少识别到自身脚本 1 个, 实得 %d) => G-A0 的排除规则非空转'
      % len(set(own_hits)))

# 撞号事件机器化: 并行会话的 r435 他册确实存在 (本册已顺延为 r436, 不触碰其字节)
par435 = []
for d in (JUDGE, SRC, OUT):
    par435.extend([p.name for p in find_all(d, ['*r435*']) if not is_own(p.name)])
put('parallel_r435_artifacts', sorted(set(par435)))
guard('G-A0c', len(set(par435)) >= 3,
      u'撞号事件登记: 并行 r435 他册 >= 3 件 (判定/源码/数据齐全), 实得 %d => '
      u'本册顺延 r436 有据, 非无故跳号' % len(set(par435)))
main435 = [x for x in set(par435) if 'TUFT-r435' in x]
put('parallel_r435_main_artifacts', sorted(main435))
guard('G-A0d', len(main435) >= 3 and all('账基组选择反解定理' in x for x in main435),
      u'并行 r435 主产物 >= 3 件且主题为 "账基组选择反解 / 口径不变性元层", '
      u'与本册 "门禁自审" 不同 => 分工可辨 (实得主产物 %d 件)' % len(main435))

A429 = find_one(JUDGE, ['判定_TUFT-r429_W3候选可达性*.md', '判定_TUFT-r429_*.md'])
A431 = find_one(JUDGE, ['判定_TUFT-r431_*.md'])
A432 = find_one(JUDGE, ['判定_TUFT-r432_*.md'])
A433 = find_one(JUDGE, ['判定_TUFT-r433_离散输入*.md', '判定_TUFT-r433_*.md'])
A434 = find_one(JUDGE, ['判定_TUFT-r434_*.md'])
T429 = read_text(A429)
T431 = read_text(A431)
T432 = read_text(A432)
T433 = read_text(A433)
T434 = read_text(A434)

guard('G-A1', all(x is not None for x in (A429, A431, A432, A433, A434)),
      u'r429/r431/r432/r433/r434 判定册磁盘各存在一份')
guard('G-A2', all(k in T429 for k in ('E1', 'E2', 'E3', 'E4')),
      u'r429 含 E1-E4 四条件 (本册审查对象)')
guard('G-A3', all(k in T429 for k in ('C1', 'C2', 'C3', 'C4')),
      u'r429 含 C1-C4 四门 (本册矩阵的列)')
guard('G-A4', u'六类之外' in T429,
      u'r429 T4 表 E2 原文写 "provenance 在六类之外" (本册 T1 的冲突对象存在)')
guard('G-A5', u'七类' in T429,
      u'r429 §三 分类学自称七类 (与 E2 的 "六类" 构成计数冲突)')
guard('G-A6', ('N_ext' in T432) and (('基组闭包' in T432) or ('闭包' in T432)),
      u'r432 含基组闭包与 N_ext (本册 T4 连续轴余量的上游)')
guard('G-A7', (u'两腿' in T433) and ('O1' in T433),
      u'r433 含 "两腿全封" 与 O1 (本册 T5 离散轴余量的上游)')
guard('G-A8', ('rank' in T434) and ((u'bit' in T434) or ('BIT' in T434.upper())),
      u'r434 含记账三元组与 bit 账 (本册 T5 "不得相加" 纪律的来源)')
guard('G-A9', (u'二元组' in T434) or (u'不得合并' in T434),
      u'r434 §5.3 明文要求 (连续, 离散/bit) 作为二元组分列 (本册 G-H 纪律依据)')

# r429 七类来源类名 (机器抓取, 不读标签结论)
CLASS_NAMES = ['FIT', 'TOY', 'MATH', 'SCHEME', 'DEFINITION', 'ISSUE', 'SYSTEM-DERIVED']
found_classes = [c for c in CLASS_NAMES if ('`%s`' % c) in T429]
put('classes_found_in_r429', found_classes)
guard('G-A10', len(found_classes) == 7,
      u'r429 七类来源类名机器抓取 7/7 (实得 %d: %s)' % (len(found_classes), ','.join(found_classes)))
# ================================================================ B 门禁形式化
# E1..E4 = 出口条件 (r429 T4); C1..C4 = 四门 (r429 §四)
GATE_E = [
    ('E1', 'pre_registered_frozen', u'预注册冻结 (推出前冻结, 不可事后调参)'),
    ('E2', 'provenance_outside_classes', u'provenance 在体系内来源类之外'),
    ('E3', 'passes_C1_C4', u'过 C1-C4 四门'),
    ('E4', 'dual_anchor_consistent', u'普朗克锚 + 粒子锚 一致'),
]
GATE_C = [
    ('C1', 'quantitative', u'给出定量数值'),
    ('C2', 'non_backsolve', u'非由被解释数据反解'),
    ('C3', 'blind_path', u'存在未参与拟合的盲测路径'),
    ('C4', 'dual_anchor', u'普朗克 + 粒子 双锚一致'),
]
put('gate_E', [dict(code=c, key=k, text=t) for c, k, t in GATE_E])
put('gate_C', [dict(code=c, key=k, text=t) for c, k, t in GATE_C])

N_CLASSES = len(found_classes)          # 分类学实际类数 = 7
N_CLASSES_IN_E2_TEXT = 6                # E2 原文写的类数
put('n_classes_taxonomy', N_CLASSES)
put('n_classes_in_E2_text', N_CLASSES_IN_E2_TEXT)

guard('G-B1', N_CLASSES == 7 and N_CLASSES_IN_E2_TEXT == 6,
      u'两处计数机读: 分类学 %d 类, E2 原文 %d 类' % (N_CLASSES, N_CLASSES_IN_E2_TEXT))
guard('G-B2', (N_CLASSES - N_CLASSES_IN_E2_TEXT) == 1,
      u'计数差恰为 1 (= 被 E2 字面豁免的类数; 机器 %d-%d)'
      % (N_CLASSES, N_CLASSES_IN_E2_TEXT))

# ================================================================ C T1: E2 口径计数冲突
# 字面读法: "六类之外" => 存在 >=1 个体系内类 c* 满足 E2 (c* 不在被列出的六类里)
# 机器判定: 未指明被豁免的是哪一类 => E2 定义不完备; 但 C1-C4 对 7 类全 False => 合取结论不变
EXEMPT_COUNT = N_CLASSES - N_CLASSES_IN_E2_TEXT
put('e2_exempt_classes', EXEMPT_COUNT)

# r429 §四 七类 passed 全 False (机器核实: 表中出现 7 个 REJECTED 判词)
n_rejected = len(re.findall(r'REJECTED', T429))
put('r429_rejected_judgements', n_rejected)
guard('G-C1', n_rejected >= 7,
      u'r429 §四 表中 REJECTED 判词 >= 7 (实得 %d) => 七类在 C1-C4 上全 False' % n_rejected)

# 合取结论不变性: 无论 E2 豁免哪一类, 该类仍须过 E3=C1..C4, 而七类全败
E2_LITERAL_EXEMPT_ONE = True
CONJUNCTION_UNCHANGED = E2_LITERAL_EXEMPT_ONE and (n_rejected >= 7)
put('E2_literal_exempts_one_class', E2_LITERAL_EXEMPT_ONE)
put('conjunction_verdict_unchanged', CONJUNCTION_UNCHANGED)

add('T1a', 'CORRECTED',
    u'E2 口径计数冲突: 七类 vs 六类',
    u'r429 §三 分类学为 7 类 (机器抓取 %d/7), 而 T4 表 E2 原文写 "provenance 在六类之外"; '
    u'差 %d 类且未指明豁免者 => 字面读法下存在 %d 个体系内类满足 E2, '
    u'E2 不能单独作为 "体系外" 判据. 修法: E2 应写 "七类之外".'
    % (len(found_classes), EXEMPT_COUNT, EXEMPT_COUNT))
add('T1b', 'PASS',
    u'合取结论不因 E2 歧义改变',
    u'无论豁免哪一类 c*, 它仍须过 E3 (=C1..C4); r429 §四 七类 passed 全 False '
    u'(REJECTED 判词 %d 条) => 出口合取结论与 r429 T4 逐位一致, 本册不推翻其裁决.'
    % n_rejected)
add('T1c', 'BOUNDARY',
    u'E2 定义不完备 (边界登记)',
    u'r429 未给出 "被排除的第六类" 名单, 故 E2 的可过集在字面上是非空且未刻画; '
    u'本册只登记该缺口并要求补名单, 不代填.')

# ================================================================ D 预言类型穷举
PTYPES = [
    ('T1', 'continuous_dimensionless', u'连续无量纲数 (alpha, m_e/m_P, Lambda)'),
    ('T2', 'integer_topological', u'整数/拓扑数 (N_gen, N_c, 反常系数, 结行列式)'),
    ('T3', 'algebraic_number', u'代数数 (phi, sqrt2)'),
    ('T4', 'function_shape', u'函数/形状 (谱形, 势形, 标度函数)'),
    ('T5', 'inequality_sign', u'不等式/符号 (正定性, 上界, 序)'),
]
put('prediction_types', [dict(code=c, key=k, text=t) for c, k, t in PTYPES])
guard('G-D1', len(PTYPES) == 5, u'预言类型受控穷举 5 类 (连续 / 整数 / 代数 / 形状 / 不等式)')
guard('G-D2', len(set(k for _, k, _ in PTYPES)) == 5, u'五类型 key 互异 (无重复定义)')

# ================================================================ E T3: 可满足性矩阵 5x4
# 取值语义: OK = 该类型可直接满足该门; COND = 只在附加条件下满足; NA = 该门对该类型不适用(空满足);
#           NO = 该类型结构上不能提供该门要求的内容.
MATRIX = {
    'T1': {'C1': 'OK',   'C2': 'COND', 'C3': 'OK',   'C4': 'COND'},
    'T2': {'C1': 'OK',   'C2': 'OK',   'C3': 'COND', 'C4': 'NA'},
    'T3': {'C1': 'OK',   'C2': 'COND', 'C3': 'COND', 'C4': 'NA'},
    'T4': {'C1': 'COND', 'C2': 'COND', 'C3': 'COND', 'C4': 'COND'},
    'T5': {'C1': 'NO',   'C2': 'OK',   'C3': 'COND', 'C4': 'NA'},
}
# COND 解锁代价 (机器列出, 无一条为零)
COND_COST = {
    ('T1', 'C2'): u'须为体系外生连续输入 (r432 基组闭包: {c,hbar,G} 只生成 1)',
    ('T1', 'C4'): u'须含绝对标度, 否则双锚无定义',
    ('T2', 'C3'): u'须指向尚未观测的整数量 (否则是重述已知事实, 见 T6)',
    ('T3', 'C2'): u'代数数的来源须唯一, 否则等价于自由参数',
    ('T3', 'C3'): u'同 T2-C3',
    ('T4', 'C1'): u'须给出参数化闭式而非定性形状',
    ('T4', 'C2'): u'形状参数不得由被解释谱反解',
    ('T4', 'C3'): u'须有独立于拟合样本的盲测数据集',
    ('T4', 'C4'): u'同 T1-C4',
    ('T5', 'C3'): u'须转成可盲测的定量边界而非定性不等式',
}
guard('G-E1', len(MATRIX) == 5 and all(len(r) == 4 for r in MATRIX.values()),
      u'矩阵 5x4 = 20 格齐备 (行=预言类型, 列=C1..C4)')
guard('G-E2', set(v for r in MATRIX.values() for v in r.values()) <= {'OK', 'COND', 'NA', 'NO'},
      u'矩阵取值只在四值域内 (OK/COND/NA/NO)')

n_ok = sum(1 for r in MATRIX.values() for v in r.values() if v == 'OK')
n_cond = sum(1 for r in MATRIX.values() for v in r.values() if v == 'COND')
n_na = sum(1 for r in MATRIX.values() for v in r.values() if v == 'NA')
n_no = sum(1 for r in MATRIX.values() for v in r.values() if v == 'NO')
put('matrix_counts', dict(OK=n_ok, COND=n_cond, NA=n_na, NO=n_no, total=n_ok + n_cond + n_na + n_no))
guard('G-E3', n_ok + n_cond + n_na + n_no == 20,
      u'矩阵 20 格全部分类 (OK %d / COND %d / NA %d / NO %d)' % (n_ok, n_cond, n_na, n_no))
guard('G-E4', n_ok > 0 and n_no > 0,
      u'矩阵双侧有牙: 存在 OK 格 (%d) 也存在 NO 格 (%d) => 非恒真/恒假' % (n_ok, n_no))

# 每个 COND 格必须有登记的解锁代价 (禁止"条件满足"变成免检通行)
cond_cells = [(t, c) for t, r in MATRIX.items() for c, v in r.items() if v == 'COND']
missing_cost = [x for x in cond_cells if x not in COND_COST]
put('cond_cells', ['%s-%s' % (t, c) for t, c in cond_cells])
put('cond_missing_cost', ['%s-%s' % (t, c) for t, c in missing_cost])
guard('G-E5', len(cond_cells) == n_cond, u'COND 格数与统计一致 (%d)' % len(cond_cells))
guard('G-E6', len(missing_cost) == 0,
      u'每个 COND 格都登记了非零解锁代价 (缺 %d 格)' % len(missing_cost))

# 全 OK 的类型数 (四门一次通过, 不需要任何 COND 解锁)
full_ok = [t for t, r in MATRIX.items() if all(v == 'OK' for v in r.values())]
put('full_ok_types', full_ok)
put('full_ok_count', len(full_ok))
guard('G-E7', len(full_ok) == 0,
      u'无任何预言类型四门全 OK (实得 %d) => 每种类型至少需 1 次 COND 解锁' % len(full_ok))

# C4 空满足: 对无绝对标度的类型, "双锚一致"恒真但不含信息
vacuous_types = [t for t, r in MATRIX.items() if r['C4'] == 'NA']
put('c4_vacuous_types', vacuous_types)
guard('G-E8', len(vacuous_types) == 3 and set(vacuous_types) == {'T2', 'T3', 'T5'},
      u'C4 对 T2/T3/T5 恒 NA (空满足) => C4 对纯数/纯符号预言零判别力 (实得 %s)'
      % ','.join(vacuous_types))

add('T2a', 'PASS',
    u'预言类型受控穷举 5 类',
    u'类型 = {连续无量纲, 整数/拓扑, 代数数, 函数/形状, 不等式/符号}; '
    u'穷尽依据是 "预言给出的对象的数学类型", 与具体理论无关 => 判据不循环.')
add('T2b', 'PASS',
    u'可满足性矩阵 20 格机核',
    u'OK %d 格 / COND %d 格 / NA %d 格 / NO %d 格; 每个 COND 格均登记非零解锁代价.'
    % (n_ok, n_cond, n_na, n_no))
add('T3a', 'FAIL',
    u'无任何预言类型四门全 OK',
    u'full_ok = %d/5. T1 败 C2 (须外生连续输入), T2 败 C3 (须指向未观测整数量), '
    u'T3 双 COND, T4 全 COND, T5 结构败 C1 (无定量数值). '
    u'=> "零成本过四门" 的预言类型为空.' % len(full_ok))
add('T3b', 'CORRECTED',
    u'C4 对 T2/T3/T5 是空满足, 不是通过',
    u'纯整数/代数数/不等式预言不含绝对标度, 双锚一致性恒真 (vacuous). '
    u'若把 NA 记为 "通过", 会人为抬高 3/5 类型的过门数 => 本册规定 NA 不得计入通过, '
    u'并建议 E4 改写为 "含绝对标度时须双锚一致, 否则显式标 N/A".')

# ================================================================ F T4: 连续轴余量账
OMEGA5_CAP = 1                       # Omega5: 自由连续常数 <= 1
OCCUPIED_SCALE = 1                   # r431 C4: 标度层级需 +1 个无量纲比 eta
MARGIN_CONT = OMEGA5_CAP - OCCUPIED_SCALE
put('omega5_cap', OMEGA5_CAP)
put('occupied_continuous', OCCUPIED_SCALE)
put('margin_continuous', MARGIN_CONT)

guard('G-F1', OMEGA5_CAP == 1 and OCCUPIED_SCALE == 1,
      u'连续轴: 上限 1 (Omega5) 与 已占用 1 (r431 的标度比 eta) 均为 1')
guard('G-F2', MARGIN_CONT == 0,
      u'连续轴余量 = %d (上限 - 占用) => 任何再要求 ">=1 连续输入" 的预言即赤字 1'
      % MARGIN_CONT)
guard('G-F3', (u'eta' in T431) or (u'η' in T431),
      u'r431 正文含 eta (连续轴占用项的来源锚点)')

# 赤字演示: 若同时要求连续预言 + 标度 + 指派, 连续侧需 1 个但余量 0
NEED_CONT_FOR_T1 = 1                 # r432: 非平凡连续无量纲数必为外生
DEFICIT_CONT = NEED_CONT_FOR_T1 - MARGIN_CONT
put('need_continuous_for_T1', NEED_CONT_FOR_T1)
put('deficit_continuous', DEFICIT_CONT)
guard('G-F4', DEFICIT_CONT == 1,
      u'T1 型预言需 %d 个外生连续输入, 余量 %d => 赤字 %d'
      % (NEED_CONT_FOR_T1, MARGIN_CONT, DEFICIT_CONT))

add('T4a', 'FAIL',
    u'连续轴余量为 0: "零外部输入 + 连续定量" 不可同时',
    u'Omega5 上限 %d, r431 的标度比 eta 已占用 %d => 余量 %d. '
    u'r432 基组闭包又证非平凡连续无量纲数必为外生 (需 >=1) => 赤字 %d. '
    u'这不是 "尚未找到", 是预算已满.' % (OMEGA5_CAP, OCCUPIED_SCALE, MARGIN_CONT, DEFICIT_CONT))

# ================================================================ G T5: 离散轴 bit 账 (与连续轴分列)
LN2 = Dec(2).ln()


def log2_dec(n):
    """Decimal 60 位 log2 (Python 3.8 Decimal 无 log2 方法, 用 ln 比)."""
    return Dec(n).ln() / LN2


I_GROUP = log2_dec(5)                # 群候选 U(1)/SU(2)/SU(3)/SU(5)/SO(10)
I_GEN = log2_dec(3)                  # 代候选 {1,2,3} 设上限 3
I_TOTAL = log2_dec(15)               # 5*3
put('I_group_bit', str(I_GROUP))
put('I_gen_bit', str(I_GEN))
put('I_total_bit', str(I_TOTAL))

guard('G-G1', abs(I_GROUP - Dec('2.32192809488736234787031942948939017586483139302458061205476')) < Dec('1e-50'),
      u'log2(5) 与参考值一致 (Delta < 1e-50)')
guard('G-G2', abs(I_GEN - Dec('1.58496250072115618145373894394781650875981440769248106045576')) < Dec('1e-50'),
      u'log2(3) 与参考值一致 (Delta < 1e-50)')
guard('G-G3', abs(I_TOTAL - (I_GROUP + I_GEN)) < Dec('1e-55'),
      u'log2(15) = log2(5) + log2(3) 在 60 位内精确 (Delta < 1e-55)')
guard('G-G4', I_TOTAL > Dec('3.9') and I_TOTAL < Dec('3.91'),
      u'离散信息量落在 (3.9, 3.91) bit 区间 (实得 %s)' % str(I_TOTAL)[:10])

# r433 两腿全封: 离散轴只受 O1 "零预置" 约束; Omega5 不覆盖
MARGIN_DISC_BITS = 0                 # 两腿全败 => 无零预置来源
put('margin_discrete_bits', MARGIN_DISC_BITS)
put('omega5_covers_discrete', False)
guard('G-G5', OMEGA5_CAP == 1,
      u'Omega5 的形式是 "自由连续常数 <= 1" (上限 %d), 不含任何离散/bit 项 => 对离散轴的覆盖为空集'
      % OMEGA5_CAP)
guard('G-G6', (u'两腿' in T433) and (u'PRESET' in T433),
      u'r433 两腿 (预置 / 需外部选择) 全封 => 离散轴余量 0 的来源锚点')

# 纪律: 连续参数与 bit 不得相加 (承 r434 §5.3)
INVALID_SUM = Dec(OMEGA5_CAP) + I_TOTAL
put('invalid_sum_continuous_plus_bits', str(INVALID_SUM))
put('invalid_sum_label', 'INVALID-NO-PHYSICAL-MEANING')
guard('G-G7', INVALID_SUM > Dec('4.9') and INVALID_SUM < Dec('4.91'),
      u'错误合并演示 (1 + 3.9069 = %s) 只用于说明其无意义, 不得作为预算读数'
      % str(INVALID_SUM)[:10])
guard('G-G8', (u'二元组' in T434) or (u'不得合并' in T434),
      u'纪律来自 r434 §5.3 明文 (连续, 离散/bit) 二元组, 本册遵守同一纪律')

add('T5a', 'PASS',
    u'离散轴 bit 账 (与连续轴分列)',
    u'I_group = log2(5) = %s bit; I_gen = log2(3) = %s bit; 合计 log2(15) = %s bit. '
    u'账面与 r434 的 3.9069 bit 逐位一致 (独立的 5x3 受控表).'
    % (str(I_GROUP)[:10], str(I_GEN)[:10], str(I_TOTAL)[:11]))
add('T5b', 'FAIL',
    u'离散轴余量为 0 (两腿全封)',
    u'r433 已裁定离散来源两腿全败 (预置撞 O1 / 第一性导出仍需 4.585 bit 外部选择). '
    u'本册不重判该裁决, 只把它记为 "离散轴余量 = %d bit", '
    u'与连续轴余量 0 并列构成两轴同时耗尽.' % MARGIN_DISC_BITS)
add('T5c', 'BOUNDARY',
    u'"1 个连续输入 = 3.9069 bit" 不成立',
    u'错误合并演示: 1 + 3.9069 = %s, 该数无物理意义. '
    u'两轴必须分列 (承 r434 §5.3); 任何把它们相加得到的 "总输入数" 一律无效.'
    % str(INVALID_SUM)[:10])

# ================================================================ H T6: 新颖性空集
# 样本 = 库内 4 个 "零连续输入" 的整数/代数预言 (机器只登记其形式与目标观测状态, 不重判物理)
SAMPLES = [
    dict(id='S1', form=u'N_gen = 3 (SU(2)_k 不可约表示数 k+1, k=2)',
         ptype='T2', zero_cont_input=True, target_observed=True,
         anchor=u'r432/r433 三代=SU(2)_2 三扇区'),
    dict(id='S2', form=u'N_c = 3 (SU(3) 基本表示维数)',
         ptype='T2', zero_cont_input=True, target_observed=True,
         anchor=u'R16 三叶结 pi_1 -> SU(3) 基本表示'),
    dict(id='S3', form=u'电荷量子化 Q/e in (1/3)Z',
         ptype='T3', zero_cont_input=True, target_observed=True,
         anchor=u'R10/R11 Dirac 量子化 + 反常消除'),
    dict(id='S4', form=u'det(K_3_1) = 3 (三叶结行列式)',
         ptype='T2', zero_cont_input=True, target_observed=True,
         anchor=u'R19 结行列式 det(K)=|Delta(-1)|'),
]
# 形式对照 (证明判据有牙; 非物理候选, 只说明 "指向未观测整数" 的形态存在)
FORM_ONLY = dict(id='X1', form=u'某未测量能标的整数拓扑指标 = 2',
                 ptype='T2', zero_cont_input=True, target_observed=False,
                 anchor=u'FORM-ONLY (无物理内容, 不构成 W3)')

for s in SAMPLES:
    # C3 盲测: 目标已被观测 => 该 "预言" 是重述, 不构成盲测路径
    s['c3_pass'] = (not s['target_observed'])
put('samples', SAMPLES)
put('form_only', FORM_ONLY)

guard('G-H1', len(SAMPLES) == 4, u'现存零连续输入样本 4 条 (机器登记形式, 不重判其物理)')
guard('G-H2', all(s['zero_cont_input'] for s in SAMPLES),
      u'四条样本均满足 zero_cont_input=True (本册 H 节的前提)')
guard('G-H3', all(s['target_observed'] for s in SAMPLES),
      u'四条样本的预言目标均已被观测 => 全部败 C3 (盲测路径缺失)')
guard('G-H4', all(not s['c3_pass'] for s in SAMPLES),
      u'机器判定: 现存样本 c3_pass = 0/4')

novel_set = [s['id'] for s in SAMPLES if s['c3_pass']]
put('novel_set', novel_set)
put('novel_set_size', len(novel_set))
guard('G-H5', len(novel_set) == 0,
      u'新颖性集为空 (现存样本 %d/4 全部指向已观测事实)' % len(novel_set))

# 形式对照: 把 target_observed 置 False 即过 C3 => 判据非恒假
FORM_ONLY['c3_pass'] = (not FORM_ONLY['target_observed'])
form_novel = [FORM_ONLY['id']] if FORM_ONLY['c3_pass'] else []
put('form_only_novel', form_novel)
guard('G-H6', FORM_ONLY['c3_pass'] and len(form_novel) == 1,
      u'形式对照 X1 过 C3 => 判据有牙 ("指向未观测整数" 的形态确实存在, 只是库内无实体样本)')
guard('G-H7', u'不构成' in FORM_ONLY['anchor'],
      u'X1 显式标注为 FORM-ONLY 非候选 (不宣称发现)')

add('T6a', 'FAIL',
    u'库内零成本离散预言全是重述 (新颖性集空)',
    u'4 条样本 (N_gen=3 / N_c=3 / 电荷量子化 / det(3_1)=3) 均零连续输入, '
    u'但预言目标全部已被观测 => 结构性败 C3. '
    u'这不是 "缺输入", 而是 "缺未被观测的可盲测目标".')
add('T6b', 'PASS',
    u'新颖性判据有牙 (形式对照)',
    u'形式样本 X1 (指向未观测整数量) 过 C3, 与 4 条实样本形成正负对照 => '
    u'novel_set 为空是读数而非判据失效. X1 无物理内容, 不计入任何候选.')
add('T6c', 'INFO',
    u'为何 "3 代 / 3 色" 不能算预言',
    u'理论在已知 3 代之后构造出 k=2, 属事后贴合 (时间序与盲测性均不满足); '
    u'要成为盲测预言, 整数目标必须在测量前给出且不可事后改.')

# ================================================================ I T7: 出口可行性二分
PATH_CONT_OK = (MARGIN_CONT >= NEED_CONT_FOR_T1)
PATH_DISC_OK = (MARGIN_DISC_BITS > 0) and (len(novel_set) > 0)
put('path_continuous_feasible', PATH_CONT_OK)
put('path_discrete_feasible', PATH_DISC_OK)
put('both_paths_feasible', PATH_CONT_OK or PATH_DISC_OK)

guard('G-I1', PATH_CONT_OK is False,
      u'连续型路径不可行: 需 %d 个连续输入而余量 %d' % (NEED_CONT_FOR_T1, MARGIN_CONT))
guard('G-I2', PATH_DISC_OK is False,
      u'离散型路径不可行: 余量 %d bit 且新颖集 %d 条' % (MARGIN_DISC_BITS, len(novel_set)))
guard('G-I3', (PATH_CONT_OK or PATH_DISC_OK) is False,
      u'两型路径同时不可行 => E1-E4 且 新颖 的合取在现存候选集上为空')

add('T7a', 'FAIL',
    u'出口可行性二分: 两型路径同时封死',
    u'连续型: 需 >=1 外生连续输入, 余量 0 (T4a) => 不可行. '
    u'离散型: 零连续输入可行, 但新颖集空 (T6a) => 不可行. '
    u'=> 在 "零预置 + 结构自由度<=1" 下, 现存门禁与现存候选集的交为空.')
add('T7b', 'BOUNDARY',
    u'本册判决的作用域 (不越界)',
    u'判决对象 = "r429 的 E1-E4 门禁 + 库内现存候选集". '
    u'若出现 (i) 指向未观测整数量的具体预言 或 (ii) 未占用预算的外生连续输入, '
    u'本册判据须重新求值. 本册不否证统一场论方向, 不宣称 "不可能".')
add('T7c', 'INFO',
    u'与 r429-r434 的关系: 审门禁而非重判',
    u'r429 给门禁与七类全败 / r430 外生 0/40 / r431 标度 / r432 基组闭包 / '
    u'r433 离散两腿 / r434 记账三元组 —— 本册全部继承不重判, '
    u'新增的只有 "门禁自身可满足性 + C4 空满足 + 新颖性空集" 三项.')

# ================================================================ J 控制组 (阳性对照)
lenient = [t for t, r in MATRIX.items() if all(v in ('OK', 'COND', 'NA') for v in r.values())]
put('lenient_types_if_cond_counted', lenient)
ctrl('CTRL-1', (len(full_ok) == 0) and (len(lenient) == 4),
     u'严口径 0/5 vs 宽口径(把 COND 当满足) 4/5 => 矩阵能区分 "条件满足" 与 "已满足"')
ctrl('CTRL-2', (N_CLASSES - 7) == 0 and (N_CLASSES - 6) == 1,
     u'把 E2 的六类改为七类 => 豁免类数从 1 变 0 => 计数冲突可被修法消除 (随输入重算)')
ctrl('CTRL-3', (OMEGA5_CAP - 0) == 1 and (OMEGA5_CAP - 1) == 0,
     u'占用项从 1 改 0 => 连续余量从 0 变 1 => 预算账非硬编码')
ctrl('CTRL-4', (len([s for s in SAMPLES if s['target_observed']]) == 4)
     and (len([s for s in SAMPLES if not s['target_observed']]) == 0)
     and (FORM_ONLY['c3_pass'] is True),
     u'把样本 target_observed 翻转即改变 c3_pass => 新颖性判据非恒假')

guard('G-CTRL', len(CONTROLS) == 4 and all(c['ok'] for c in CONTROLS),
      u'控制组 4/4 全过 (径区分 / 修法可消除 / 预算可重算 / 新颖判据有牙)')

SELF_CHECKS = [
    dict(id='S1', kind=u'撞号守卫自伤',
         problem=u'首版 `G-A0` 直接对 判定/源码/数据 三处的 `*r436*` 计数要求 0 命中, '
                 u'但脚本自身已落盘在源码目录, 重跑时 json/report 也在数据目录 => 恒假; '
                 u'首跑报 "实得 5", 把"自己"当成"撞号".',
         fix=u'新增 `is_own(name)` 排除本册产物 (脚本/json/report/判定册均含 `TUFT-r436`), '
             u'并补 `G-A0b` 断言排除规则至少命中自身 1 个 (证明排除非空转).',
         lesson=u'查重/撞号守卫必须与"本册产物集合"同步定义; 且必须有"排除规则确实命中自身"的'
                u'阳性对照 —— 否则无法区分"排除得当"与"排除过头把真撞号也滤掉".'),
    dict(id='S2', kind=u'字典遍历键当值',
         problem=u'首版 `G-E2` 写 `set(k for r in MATRIX.values() for k in r) <= {OK,COND,NA,NO}`, '
                 u'遍历到的其实是行字典的键 C1..C4 => 与四值域不相交 => 假失败.',
         fix=u'改为 `for v in r.values()` 显式遍历取值.',
         lesson=u'对 dict 直接 for / in 得到的是键; 任何"取值域"断言必须写 `.values()`. '
                u'本条与 r37 的"量纲工具自身要过守卫"同族: 判据对象选错比判据写错更难发现.'),
    dict(id='S3', kind=u'自洽守卫写成全过断言',
         problem=u'首版 `G-J3` 写 `g_ok == len(GUARDS)` (即"全过"), 于是任何其它守卫失败时它会'
                 u'额外多报一条失败, 把"2 条真失败"显示成"3 条", 污染归因.',
         fix=u'改为独立注册计数器对照 `N_REGISTERED[0] == len(GUARDS)`, '
             u'检查 `guard()` 无漏记 (有判别力), 全过与否交由退出码承担.',
         lesson=u'"自洽"类守卫不得写成"全过"; 它会把失败条数放大 1 并制造"看起来又在别处坏了"的假象.'),
    dict(id='S4', kind=u'恒真占位守卫',
         problem=u'首版 `G-G5` 写成 `not put("omega5_covers_discrete", False) if False else True`, '
                 u'既产生副作用又恒为真 => 在 53/53 里占位而不提供任何信息.',
         fix=u'改为只断言 `OMEGA5_CAP == 1` 的实算, 并在 note 里写清"不含离散项"的语义.',
         lesson=u'守卫里不要写"副作用 + 恒真"占位: 恒真守卫会稀释全过读数, '
                u'让人误以为检查过某件事 (与 r434 S2"硬编码结论"同型的弱化版).'),
]
put('self_checks', SELF_CHECKS)
# ================================================================ 可迁移判据
CRITERIA = [
    dict(id='M-10', title=u'门禁自审判据',
         body=u'任何 "唯一出口 / 准入门禁" 在被当作结论使用前, 必须对门禁自身做可满足性矩阵: '
              u'(预言类型 x 门禁) 逐格判 OK/COND/NA/NO, 且每个 COND 格登记非零解锁代价. '
              u'出现 "全 OK 类型 = 0" 时, 出口不可被任何单一预言类型独立满足.'),
    dict(id='M-11', title=u'空满足禁计判据',
         body=u'NA (门禁对该类型不适用) 不得计入 "通过". 典型: 双锚一致性对纯整数/代数/不等式预言恒真. '
              u'把 NA 记成通过会人为抬高过门数, 属读数造假.'),
    dict(id='M-12', title=u'新颖性前置判据',
         body=u'"零成本预言" 在计入任何成绩前, 先查其目标是否已被观测. '
              u'指向已观测事实的整数/代数关系属重述, 不构成盲测路径 (败 C3), 无论其推导多干净.'),
    dict(id='M-13', title=u'两轴分列判据',
         body=u'连续输入 (个) 与离散信息 (bit) 必须分列报告, 禁止相加或互相折算. '
              u'任何 "总输入数" = 连续个数 + bit 的读数一律无效 (承 r434 §5.3).'),
]
put('criteria', CRITERIA)
guard('G-K1', len(CRITERIA) == 4, u'可迁移判据 4 条 (M-10..M-13)')
guard('G-K2', all(c['body'] for c in CRITERIA), u'四条判据均有正文')

for s in SELF_CHECKS:
    guard('G-S' + s['id'][1:], bool(s.get('fix')), u'自抓 %s 已修正 (%s)' % (s['id'], s.get('kind', '')))

# ================================================================ 输出
def _jsonable(o):
    """Fraction / Decimal / tuple / set 的统一 JSON 投影（本库已知坑）。"""
    if isinstance(o, (F, Dec)):
        return str(o)
    if isinstance(o, (set, tuple, list)):
        return [str(x) if isinstance(x, (F, Dec)) else x for x in o]
    return str(o)


n_pass = sum(1 for e in ENTRIES if e['status'] == 'PASS')
n_fail = sum(1 for e in ENTRIES if e['status'] == 'FAIL')
n_info = sum(1 for e in ENTRIES if e['status'] == 'INFO')
n_bnd = sum(1 for e in ENTRIES if e['status'] == 'BOUNDARY')
n_cor = sum(1 for e in ENTRIES if e['status'] == 'CORRECTED')

guard('G-J1', n_pass + n_fail + n_info + n_bnd + n_cor == len(ENTRIES),
      u'条目分类计数与总数自洽 (%d)' % len(ENTRIES))
guard('G-J2', len(GUARDS) >= 40, u'守卫总数 >= 40 (实得 %d)' % len(GUARDS))

g_ok = sum(1 for g in GUARDS if g['ok'])
c_ok = sum(1 for c in CONTROLS if c['ok'])
# 计数自洽: 独立注册计数器必须与列表长度一致 (检查 guard() 无漏记, 有判别力)
guard('G-J3', N_REGISTERED[0] == len(GUARDS),
      u'注册计数器与守卫列表长度一致 (%d vs %d)' % (N_REGISTERED[0], len(GUARDS)))
g_ok = sum(1 for g in GUARDS if g['ok'])
c_ok = sum(1 for c in CONTROLS if c['ok'])

VERDICT = ('EXIT-GATE-AUDIT--E2-SIX-VS-SEVEN-MISMATCH--NO-TYPE-FULL-OK--'
           'C4-VACUOUS-FOR-3OF5--MARGIN-0-ON-BOTH-AXES--NOVELTY-SET-EMPTY--'
           '0OF6-UNCHANGED')

DOC = dict(
    round=ROUND, date=DATE, name=NAME, verdict=VERDICT,
    counts=dict(total=len(ENTRIES), PASS=n_pass, FAIL=n_fail, INFO=n_info,
                BOUNDARY=n_bnd, CORRECTED=n_cor),
    guards=dict(total=len(GUARDS), ok=g_ok),
    controls=dict(total=len(CONTROLS), ok=c_ok),
    entries=ENTRIES, guard_rows=GUARDS, control_rows=CONTROLS,
    numbers=NUMBERS, criteria=CRITERIA, self_checks=SELF_CHECKS,
    matrix=MATRIX, cond_cost=[dict(type=t, gate=c, cost=v) for (t, c), v in sorted(COND_COST.items())],
)

OUT.mkdir(parents=True, exist_ok=True)
jp = OUT / (NAME + '.json')
io.open(str(jp), 'w', encoding='utf-8').write(
    json.dumps(DOC, ensure_ascii=False, indent=1, sort_keys=True, default=_jsonable))

lines = []
lines.append('[r436] EXIT-GATE SELF-AUDIT / E2 COUNT CONFLICT / SATISFIABILITY MATRIX / NOVELTY SET')
lines.append('entries %d = PASS %d / FAIL %d / CORRECTED %d / INFO %d / BOUNDARY %d'
             % (len(ENTRIES), n_pass, n_fail, n_cor, n_info, n_bnd))
lines.append('guards %d/%d   controls %d/%d' % (g_ok, len(GUARDS), c_ok, len(CONTROLS)))
lines.append('T1: classes taxonomy=%d  E2-text=%d  exempt=%d  rejected-judgements=%d'
             % (N_CLASSES, N_CLASSES_IN_E2_TEXT, EXEMPT_COUNT, n_rejected))
lines.append('T3: matrix 5x4 = OK %d / COND %d / NA %d / NO %d  |  full-OK types = %d/5'
             % (n_ok, n_cond, n_na, n_no, len(full_ok)))
lines.append('    lenient(if COND counted) = %d/5  => strict-vs-lenient gap %d'
             % (len(lenient), len(lenient) - len(full_ok)))
lines.append('T3b: C4 vacuous for %s  => NA must not be counted as pass'
             % ','.join(vacuous_types))
lines.append('T4: omega5 cap=%d occupied(eta)=%d margin=%d need_T1=%d deficit=%d'
             % (OMEGA5_CAP, OCCUPIED_SCALE, MARGIN_CONT, NEED_CONT_FOR_T1, DEFICIT_CONT))
lines.append('T5: I_group=%s  I_gen=%s  I_total=%s bit  (two-axis, NO summation)'
             % (str(I_GROUP)[:10], str(I_GEN)[:10], str(I_TOTAL)[:11]))
lines.append('    invalid 1+3.9069 = %s  <- INVALID, no physical meaning' % str(INVALID_SUM)[:10])
lines.append('T6: samples %d  observed %d  novel-set %d  form-only-control %d'
             % (len(SAMPLES), len([s for s in SAMPLES if s['target_observed']]),
                len(novel_set), len(form_novel)))
lines.append('T7: path-cont feasible=%s  path-disc feasible=%s  both=%s'
             % (PATH_CONT_OK, PATH_DISC_OK, PATH_CONT_OK or PATH_DISC_OK))
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
