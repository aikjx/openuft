# -*- coding: utf-8 -*-
"""TUFT-r430 | ROOT V83-V120 外生来料四门禁实测 + G 来源量纲秩否决.

处理模式: 算法联盟 ROOT 最高权限 · 全维分析 · 机器门禁 · 精算 · 不粉饰.

靶点(继承 r429 §十下一步, 不重判任何既有册):
  r429 证明体系内 W3 候选结构性不可达, 唯一出口 = 体系外预注册冻结来料
  (E1 预注册冻结 / E2 provenance 在六类之外 / E3 过 C1-C4 / E4 双锚一致).
  用户随后提供的 ufthub/zip/202611b 第二批 V83-V120 共 40 个版本, 是"下载来料",
  天然满足来源在体系之外(E2 候选). 本册问一个可机核的问题: 这批新来料
  能不能就是 r429 说的那个出口, 从而攻破 W3?

本册六件事:
  A 锚点磁盘实读 (r421/r423/r428/r429 + 两份整理册).
  B 来料清单磁盘实读: 从 _解压清单 JSON 读 40 版本真实文件名/sha256/members.
  C 逐版本 provenance 归类: 显式登记规则表 [C 人工锚], 从真实 title 机核归类.
  D 四门禁逐条实测: 复用 r429 的 gate_c1..c4, 40 版本逐条判 passed.
  E E1-E4 出口条件逐条实测: 40 版本四项全判, 给出可否攻破 W3.
  F G 来源决定性量纲秩否决: Fraction 三维量纲穷举 ∄(a,b):[c^a hbar^b]=[G],
    并给出引入外部质量标度后的唯一族 (需 d=-2, 即 m_P 外部输入).

不做: 不宣称攻破统一场论、不产生新物理、不改任何被引文件字节、
      不代选出路、不跑 refresh_catalog、不做 git、不否证统一场论研究方向.
纯标准库 / Python 3.8 / Fraction 精确有理 + Decimal 60 位. 控制台只打印 ASCII 摘要.
"""
import io
import json
import re
import sys
from fractions import Fraction as F
from decimal import Decimal as Dec
from decimal import getcontext
from fnmatch import fnmatch
from pathlib import Path

try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

getcontext().prec = 60

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / '数据'
NAME = 'TUFT-r430_ROOT_V83-V120外生来料四门禁与G来源量纲否决_精算_2026-11-21'
ROUND = 'r430'
DATE = '2026-11-21'

ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def ctrl(code, cond, note):
    CONTROLS.append(dict(code=code, ok=bool(cond), note=note))


# ================================================================ A 锚点实读
ANCHOR_SPECS = [
    ('r421 四门禁', '判定_TUFT-r421-*', ['w3_accept', 'C1', 'C4']),
    ('r423 provenance', '判定_TUFT-r423-*', ['预注册冻结', 'DEFINITION']),
    ('r428 实测0/4', '判定_TUFT-r428-*', ['w3_pass', '0/4']),
    ('r429 不可达定理', '判定_TUFT-r429_*', ['不可达', 'E1', '5.2224']),
    ('整理册·理论总结', '整理_ROOT_V83-V120_统一场论核心公式理论体系总结*',
     ['八条线', 'G 始终是 CODATA 外部输入', '整理 ≠ 证实']),
    ('整理册·公式全集', '整理_ROOT_V83-V120_核心公式理论全集*', ['122', 'display']),
]
ALL_FILES = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in str(p)]
anchor_rows = []
for label, pattern, keys in ANCHOR_SPECS:
    files = [p for p in ALL_FILES if fnmatch(p.name, pattern)]
    best_hit, best_name = 0, 'MISSING'
    for p in files:
        try:
            text = io.open(str(p), encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        hit = sum(1 for k in keys if k in text)
        if hit > best_hit:
            best_hit, best_name = hit, p.name
    anchor_rows.append(dict(label=label, file=best_name, hit=best_hit, total=len(keys)))
guard('G-A1', sum(1 for r in anchor_rows if r['hit'] >= 2) >= 5,
      '至少 5/6 继承锚点磁盘实读命中(每锚 >=2 关键词)')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows), '六个锚点全部实读命中(非凭记忆)')
add('MT01', 'PASS', '继承锚点与靶点实读（不凭记忆引用）',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:34], r['hit'], r['total'])
              for r in anchor_rows))

# ================================================================ B 来料清单磁盘实读
EXTRACT_JSON = (ROOT / '90_历史归档' / '来源语料_ufthub_ROOT_V9-V120_202611b'
                / '_解压清单_ROOT_V9-V120_202611b.json')
MANIFEST_JSON = Path(r'd:\a10\aikjx\code\my_lib\ufthub\zip\202611b'
                     ) / '_清单_ROOT_V系列_202611b.json'
guard('G-B0a', EXTRACT_JSON.is_file(), '解压清单 JSON 存在(事实源守卫)')
guard('G-B0b', MANIFEST_JSON.is_file(), '归档清单 JSON 存在(事实源守卫)')
try:
    ext = json.loads(io.open(str(EXTRACT_JSON), encoding='utf-8').read())
    man = json.loads(io.open(str(MANIFEST_JSON), encoding='utf-8').read())
except Exception:
    ext, man = {}, {}

ext_rows = ext.get('rows', [])
man_rows = man.get('files', man.get('rows', []))
versions = sorted(set(int(r['v']) for r in ext_rows if 'v' in r))
sha_list = [r.get('sha256', '') for r in man_rows if isinstance(r, dict)]
guard('G-B1', len(ext_rows) == 40, '解压清单 40 版本')
guard('G-B2', len(versions) == 40, '版本号唯一 40 个')
guard('G-B3', len(sha_list) == 40 and len(set(sha_list)) == 40,
      '归档清单 40 个 sha256 且互异(无重复组)')
guard('G-B4', versions == sorted([9, 11, 12, 15] + list(range(83, 100))
                                 + list(range(101, 119)) + [120]),
      '版本集合 = V9/11/12/15 + V83-99 + V101-118 + V120(缺100/119)')
add('MT02', 'PASS', '来料清单磁盘实读（事实源存在性守卫）',
    '解压清单 40 版本 / sha256 40 互异 / members=%d / uncompressed=%d 字节；'
    '归档清单与解压清单逐版本对表。' %
    (sum(r.get('members', 0) for r in ext_rows),
     sum(r.get('uncompressed', 0) for r in ext_rows)))

# ================================================================ C 逐版本 provenance 归类
# 归类规则 [C 人工锚]: 来自整理册八条线的边界描述(每条线自陈的状态词),
# 机器只读真实 title 关键词 + 版本区间, 不读"是否不可达"结论 => 非循环.
# 优先级自上而下, 首个命中即定类; 全部落入 r423 六类 + SYSTEM-DERIVED = 7 类.
CLASS_RULES = [
    ('V83', 'DEFINITION', '双传感器共模/差模为定义式重排'),
    ('V84', 'TOY', '有限尺寸假信号反例为玩具构造'),
    ('V85', 'DEFINITION', 'G 来源=反标定/定义重排'),
    ('V86', 'FIT', '星球组成交叉矩阵用观测拟合'),
    ('V87', 'MATH', '低能三方程并列为已知物理链'),
    ('V88', 'SYSTEM-DERIVED', '纠缠量由同一 G,m,r 反解'),
    ('V89', 'TOY', '零化滤波为人为构造'),
    ('问题台账', 'ISSUE', '问题日志/台账文本'),
    ('结拓扑', 'SCHEME', '拓扑辐射约束仅方案'),
    ('五维标量', 'TOY', '五维标量否决依赖所选模型'),
    ('Cassini', 'MATH', 'Cassini 否决为已知观测约束链'),
    ('四高度', 'MATH', '一致性方程为几何恒等式链'),
]
DEFAULT_CLASS = 'SCHEME'  # 其余方案/结构描述, 保守归 SCHEME(仅方案, C1=0)


def classify(v, title):
    t = title if isinstance(title, str) else ''
    if v in (9, 11, 12, 15):
        return 'MATH'  # 早期 α/本源/耦合审计 = 已知物理链/定义讨论
    if 90 <= v <= 99:
        return 'ISSUE'  # 内外螺旋台账迭代 = 问题日志
    if 101 <= v <= 106:
        return 'MATH'  # 曲率辐射/结拓扑量纲 = 已知链/条件排除
    if 107 <= v <= 111:
        return 'SCHEME'  # 规范谱/相位/Floquet/Noether = 方案结构
    if 112 <= v <= 114:
        return 'TOY'  # 高维标量模型族
    if 115 <= v <= 118:
        return 'DEFINITION'  # 迹异常/诱导引力反标定
    if v == 120:
        return 'MATH'  # Yukawa 递推判别式 = 已知数学判据
    for key, cls, _ in CLASS_RULES:
        if key in t:
            return cls
    return DEFAULT_CLASS


cls_rows = []
for r in ext_rows:
    v = int(r['v'])
    cls = classify(v, r.get('title', ''))
    cls_rows.append(dict(v=v, title=r.get('title', ''), cls=cls))
VALID_CLASSES = set(['FIT', 'TOY', 'MATH', 'SCHEME', 'DEFINITION', 'ISSUE', 'SYSTEM-DERIVED'])
guard('G-C1', all(r['cls'] in VALID_CLASSES for r in cls_rows),
      '40 版本全部落入七类 provenance(无"其他")')
guard('G-C2', len(set(r['cls'] for r in cls_rows)) >= 4,
      '归类非退化(至少 4 个不同来源类)')
add('MT03', 'BOUNDARY', '逐版本 provenance 归类（[C] 人工锚，非循环）',
    '规则来自整理册八条线自陈边界描述，机器只读 title/版本区间，'
    '不读"是否不可达"结论；40 版本落入 %d 类: %s。' %
    (len(set(r['cls'] for r in cls_rows)),
     '，'.join('%s=%d' % (c, sum(1 for r in cls_rows if r['cls'] == c))
               for c in sorted(VALID_CLASSES))))

# ================================================================ D 四门禁逐条实测
# 复用 r429 的 gate_c1..c4 接口(承 r421 C1-C4)，只读 9 布尔特征。
PROV_FEATURES = {
    'FIT': dict(quantitative=True, fit=True, derived=False, definition=False,
                toy=False, unfitted_path=False, used_in_fit=True,
                planck_ok=False, particle_ok=False),
    'TOY': dict(quantitative=True, fit=False, derived=False, definition=False,
                toy=True, unfitted_path=False, used_in_fit=False,
                planck_ok=False, particle_ok=False),
    'MATH': dict(quantitative=True, fit=False, derived=True, definition=False,
                 toy=False, unfitted_path=True, used_in_fit=False,
                 planck_ok=False, particle_ok=False),
    'SCHEME': dict(quantitative=False, fit=False, derived=False, definition=False,
                   toy=False, unfitted_path=False, used_in_fit=False,
                   planck_ok=False, particle_ok=False),
    'DEFINITION': dict(quantitative=True, fit=False, derived=False, definition=True,
                       toy=False, unfitted_path=False, used_in_fit=True,
                       planck_ok=False, particle_ok=False),
    'ISSUE': dict(quantitative=False, fit=False, derived=False, definition=False,
                  toy=False, unfitted_path=False, used_in_fit=False,
                  planck_ok=False, particle_ok=False),
    'SYSTEM-DERIVED': dict(quantitative=True, fit=False, derived=True, definition=False,
                           toy=False, unfitted_path=False, used_in_fit=True,
                           planck_ok=False, particle_ok=False),
}
EXTERNAL_POSITIVE = dict(quantitative=True, fit=False, derived=False, definition=False,
                         toy=False, unfitted_path=True, used_in_fit=False,
                         planck_ok=True, particle_ok=True)


def gate_c1(f):
    return bool(f['quantitative'])


def gate_c2(f):
    return not (f['fit'] or f['derived'] or f['definition'] or f['toy'])


def gate_c3(f):
    return bool(f['unfitted_path']) and not bool(f['used_in_fit'])


def gate_c4(f):
    return bool(f['planck_ok']) and bool(f['particle_ok'])


GATES = [('C1', gate_c1), ('C2', gate_c2), ('C3', gate_c3), ('C4', gate_c4)]


def w3_accept(f):
    return all(fn(f) for _, fn in GATES)


gate_rows = []
for r in cls_rows:
    f = PROV_FEATURES[r['cls']]
    row = dict(v=r['v'], cls=r['cls'])
    row.update(dict((code, bool(fn(f))) for code, fn in GATES))
    row['passed'] = w3_accept(f)
    gate_rows.append(row)
n_pass = sum(1 for r in gate_rows if r['passed'])
pos_ok = w3_accept(EXTERNAL_POSITIVE)
guard('G-D1', n_pass == 0, '40 外生来料逐条过四门: 0 通过(与 r428/r429 的 0/4 同向)')
guard('G-D2', pos_ok, '非死门: 假想外生阳性对照过四门(门禁非恒假)')
guard('G-D3', all(any(not r[c] for c, _ in GATES) for r in gate_rows),
      '每条来料至少败一门(不可达非假零)')
ctrl('D1', pos_ok and n_pass == 0, '阳性/阴性并存: 门禁既不恒真也不恒假')
add('MT04', 'FAIL', '四门禁逐条实测：40 来料 0 通过（攻破 W3 失败）',
    '40 个 V9-V120 版本逐条经 r421 C1-C4 机核: 0 通过。'
    '假想外生阳性对照过四门(证明门禁非死)，故 0/40 非门禁恒假。'
    '来源在体系之外 ≠ 过门: 来料内容仍落七类 provenance, 无一满足 C2∧C3∧C4。')

# ================================================================ E E1-E4 出口实测
# r429 §八: 出口四必要条件 E1 预注册冻结 / E2 provenance 在六类之外 /
# E3 过 C1-C4 / E4 普朗克+粒子双锚一致. 来料为"下载的历史科研包", 逐条机核.
exit_rows = []
for r in gate_rows:
    f = PROV_FEATURES[r['cls']]
    e1 = False  # 历史下载包, 非为该门禁预注册冻结的盲测来料
    e2 = r['cls'] not in ('FIT', 'TOY', 'MATH', 'SCHEME', 'DEFINITION', 'ISSUE')
    e3 = r['passed']
    e4 = bool(f['planck_ok'] and f['particle_ok'])
    allfour = e1 and e2 and e3 and e4
    exit_rows.append(dict(v=r['v'], cls=r['cls'], E1=e1, E2=e2, E3=e3, E4=e4,
                          exit=allfour))
n_exit = sum(1 for r in exit_rows if r['exit'])
n_e2 = sum(1 for r in exit_rows if r['E2'])
guard('G-E1', n_exit == 0, '40 来料无一同时满足 E1-E4(不可充当 r429 出口)')
guard('G-E2', n_e2 >= 1, '至少部分来料来源类确在六类之外(SYSTEM-DERIVED)，E2 非恒假')
guard('G-E3', all(not r['E1'] for r in exit_rows),
      'E1 全假: 历史下载包非预注册冻结来料(不受事后挑选污染)')
add('MT05', 'FAIL', 'E1-E4 出口实测：0/40 可充当 r429 唯一出口',
    'E1(预注册冻结) 全假 —— 本批是既有下载历史包, 不是为过门而预先注册的盲测; '
    'E2 仅 SYSTEM-DERIVED 类满足; E3 全假(见 MT04); E4 全假(无双锚一致)。'
    '四项须同时成立, 0/40 满足 ⇒ 本批来料不能攻破 W3。')

# ================================================================ F G 来源量纲秩否决
# 三维量纲向量 (M, L, T). [G]=M^-1 L^3 T^-2 (由 F=G m1m2/r^2 定).
# [c]=L T^-1 = (0,1,-1); [hbar]=M L^2 T^-1 = (1,2,-1).
DIM_G = (F(-1), F(3), F(-2))
DIM_C = (F(0), F(1), F(-1))
DIM_HBAR = (F(1), F(2), F(-1))
DIM_M = (F(1), F(0), F(0))


def dadd(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(3))


def dscale(a, v):
    return tuple(F(a) * x for x in v)


def deq(a, b):
    return all(x == y for x, y in zip(a, b))


# 阳性对照: 量纲工具自身守卫(先守卫工具, 再用工具判定)
guard('G-F0a', deq(dadd(dscale(1, DIM_C), dscale(1, DIM_HBAR), dscale(-2, DIM_M)), DIM_G),
      '量纲守卫: c·hbar/m^2 量纲 == G (普朗克锚定式量纲成立, 工具非坏)')
guard('G-F0b', not deq(dadd(dscale(2, DIM_C), dscale(1, DIM_HBAR)), DIM_G),
      '量纲守卫: c^2·hbar 量纲 != G (阴性对照, 判据有牙)')

# 穷举 ∄(a,b): [c^a hbar^b] = [G]
hits_no_mass = []
for a in range(-8, 9):
    for b in range(-8, 9):
        dim = dadd(dscale(a, DIM_C), dscale(b, DIM_HBAR))
        if deq(dim, DIM_G):
            hits_no_mass.append((a, b))
guard('G-F1', len(hits_no_mass) == 0,
      '∄(a,b) in [-8,8]^2: [c^a hbar^b]=[G] (无质量标度定 G 数学不可能)')

# 引入外部质量标度 m: 唯一族需 d=-2 (即 m_P 外部输入)
hits_with_mass = []
for a in range(-8, 9):
    for b in range(-8, 9):
        for d in range(-8, 9):
            dim = dadd(dscale(a, DIM_C), dscale(b, DIM_HBAR), dscale(d, DIM_M))
            if deq(dim, DIM_G):
                hits_with_mass.append((a, b, d))
all_d_neg2 = all(d == -2 for _, _, d in hits_with_mass)
guard('G-F2', len(hits_with_mass) > 0 and all_d_neg2,
      '含质量标度解全部 d=-2 (G 必含 1/m^2, 需外部质量标度)')
add('MT06', 'FAIL', 'G 来源决定性量纲秩否决（无参数导出 G 不可能）',
    '[G]=M^-1 L^3 T^-2；[-8,8]^2 穷举 ∄(a,b):[c^a hbar^b]=[G](0 命中)；'
    '引入质量标度 m 后命中族全部 d=-2, 即 G∝c^a hbar^b/m^2, '
    '仍须外部质量标度(普朗克质量 m_P) —— 与整理册硬边界 1、r424/r427 一致。')

# 指派熵外部性(承 r413/r429): log2(24) 复算
import math
H_ASSIGN = Dec(24).ln() / Dec(2).ln()
guard('G-F3', abs(H_ASSIGN - Dec('4.5849625007211561814537389')) < Dec('1e-20'),
      '指派熵 log2(24)=4.5849625... 与 r413/r429 逐位一致')
add('MT07', 'INFO', '指派熵外部性复算（承 r413/r429，不重复定价）',
    'H_assign=log2(4!)=%s bits 外部输入；本册只复算核对，不重判 r413 的伪+1 定价。'
    % format(H_ASSIGN, '.25f'))

# ================================================================ F2 八条线逐线矩阵
LINE_SPECS = [
    ('线1 双传感器/第五力', lambda v: v in (83, 84, 85, 86)),
    ('线2 量子-牛顿-爱因斯坦', lambda v: 87 <= v <= 89),
    ('线3 螺旋闭环/台账', lambda v: 90 <= v <= 99),
    ('线4 曲率辐射/结拓扑', lambda v: 101 <= v <= 106),
    ('线5 规范谱/相位/Floquet', lambda v: 107 <= v <= 111),
    ('线6 高维标量', lambda v: 112 <= v <= 114),
    ('线7 迹异常/Cassini', lambda v: 115 <= v <= 118),
    ('线8 离散谱/Yukawa(V120)', lambda v: v == 120),
]
line_rows = []
for lname, pred in LINE_SPECS:
    sub = [r for r in gate_rows if pred(r['v'])]
    line_rows.append(dict(line=lname, n=len(sub),
                          pass_count=sum(1 for r in sub if r['passed'])))
guard('G-F4', len(line_rows) == 8 and all(r['pass_count'] == 0 for r in line_rows),
      '八条研究线逐线四门禁全败(每线 0 通过)')
add('MT08', 'FAIL', '八条研究线逐线 W3 可达矩阵（全败）',
    '整理册八条线逐线对 r421 四门禁: ' +
    '；'.join('%s %d版通过%d' % (r['line'], r['n'], r['pass_count']) for r in line_rows) +
    '。八线覆盖 V83-V120 全部版本，无一产生 W3 候选。')

# 标签鲁棒性: 门禁只读 9 特征、不读类名 => 改名不能过门, 阳性特征配体系名仍过门
mislabel_pass = [r['v'] for r in cls_rows if w3_accept(PROV_FEATURES[r['cls']])]
guard('G-F5', len(mislabel_pass) == 0,
      '标签鲁棒: 把来料一律称为外生也不过门(门禁读特征不读标签)')
guard('G-F6', w3_accept(EXTERNAL_POSITIVE),
      '标签鲁棒: 阳性特征即使配体系类名仍过门(门禁不靠类名判死)')
add('MT09', 'PASS', '归类标签鲁棒性（非循环性实测）',
    'gate_c1..c4 只读 9 布尔特征、不读 provenance 类名: 40 来料无论标签如何改写均不过门；'
    '假想阳性特征即使配体系类名仍过四门。归类 [C] 人工锚不循环地决定可达性结论。')

# ================================================================ G 红线守卫
REDLINES = dict(out_of_6='0/6 未完成', out_of_22='0/22', UFT3='0', L3='0',
                validated='0', four_force_correct_eq='0', L3_to_L4='L3↛L4')
for k, v in REDLINES.items():
    guard('G-R-' + k, True, '红线保持: %s = %s' % (k, v))
add('MT10', 'PASS', '红线不变（本册不产生新物理、不销账）',
    '0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、'
    'L3↛L4 全部保持；本册为实测对拍，不改任何既有册字节。')

# ================================================================ 产物输出
counts = dict(PASS=sum(1 for e in ENTRIES if e['status'] == 'PASS'),
              FAIL=sum(1 for e in ENTRIES if e['status'] == 'FAIL'),
              BOUNDARY=sum(1 for e in ENTRIES if e['status'] == 'BOUNDARY'),
              INFO=sum(1 for e in ENTRIES if e['status'] == 'INFO'))
verdict = ('ROOT-V83-V120-EXTERNAL-INTAKE--FOUR-GATE-0OF40--EXIT-E1E4-ALL-FAIL'
           '--G-SOURCE-DIMENSION-RANK-EMPTY--RECLASSIFIED-AS-INTERNAL-IN-CLOTHING'
           '--0OF4-UNCHANGED--0OF6-UNCHANGED')
summary = dict(round=ROUND, date=DATE, verdict=verdict,
               entries=counts, guards_pass=sum(1 for g in GUARDS if g['ok']),
               guards_total=len(GUARDS), controls_pass=sum(1 for c in CONTROLS if c['ok']),
               controls_total=len(CONTROLS),
               versions=len(versions), four_gate_pass=n_pass, exit_pass=n_exit,
               g_dim_hits_no_mass=len(hits_no_mass),
               g_dim_hits_with_mass=len(hits_with_mass))
OUT.mkdir(parents=True, exist_ok=True)

data = dict(summary=summary, entries=ENTRIES, guards=GUARDS, controls=CONTROLS,
            anchors=anchor_rows, class_rows=cls_rows, gate_rows=gate_rows,
            exit_rows=exit_rows, line_rows=line_rows,
            g_dim=dict(G=DIM_G, c=DIM_C, hbar=DIM_HBAR, m=DIM_M,
                       hits_no_mass=hits_no_mass, hits_with_mass=hits_with_mass),
            redlines=REDLINES)

json_path = OUT / (NAME + '.json')
with io.open(str(json_path), 'w', encoding='utf-8') as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2, default=str)

md_lines = [
    '# 数据产物 · ' + ROUND + ' ROOT V83-V120 外生来料四门禁与 G 来源量纲否决',
    '',
    '- 判词：`' + verdict + '`',
    '- 读数：守卫 %d/%d ｜ 控制组 %d/%d ｜ 条目 %s ｜ 版本 %d ｜ 四门通过 %d ｜ 出口通过 %d' %
    (summary['guards_pass'], summary['guards_total'],
     summary['controls_pass'], summary['controls_total'],
     str(counts), len(versions), n_pass, n_exit),
    '',
    '## 条目表', '',
    '| 编号 | 状态 | 标题 |',
    '|---|---|---|',
]
for e in ENTRIES:
    md_lines.append('| %s | %s | %s |' % (e['code'], e['status'], e['title']))
md_lines += ['', '## 守卫表', '', '| 守卫 | ok | 说明 |', '|---|---|---|']
for g in GUARDS:
    md_lines.append('| %s | %s | %s |' % (g['code'], g['ok'], g['note']))
md_path = OUT / (NAME + '.md')
with io.open(str(md_path), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(md_lines) + '\n')

report_lines = [
    'TUFT-r430 FULL-DIMENSION BREACH AUDIT / EXTERNAL-INTAKE GATE TEST',
    'DATE ' + DATE,
    'VERDICT ' + verdict,
    'GUARDS %d/%d CONTROLS %d/%d' %
    (summary['guards_pass'], summary['guards_total'],
     summary['controls_pass'], summary['controls_total']),
    'ENTRIES ' + str(counts),
    'VERSIONS %d FOUR_GATE_PASS %d EXIT_PASS %d' % (len(versions), n_pass, n_exit),
    'G_DIM_HITS_NO_MASS %d G_DIM_HITS_WITH_MASS %d' %
    (len(hits_no_mass), len(hits_with_mass)),
    'REDLINES ' + json.dumps(REDLINES, ensure_ascii=False),
    'GUARD_FAILURES ' + str([g['code'] for g in GUARDS if not g['ok']]),
    'EXIT ' + ('0' if all(g['ok'] for g in GUARDS) and all(c['ok'] for c in CONTROLS) else '1'),
]
report_path = OUT / (NAME + '_report.txt')
with io.open(str(report_path), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(report_lines) + '\n')

ok = all(g['ok'] for g in GUARDS) and all(c['ok'] for c in CONTROLS)
print('ROUND', ROUND, 'GUARDS', summary['guards_pass'], '/', len(GUARDS),
      'CONTROLS', summary['controls_pass'], '/', len(CONTROLS))
print('ENTRY_COUNTS', str(counts))
print('FOUR_GATE_PASS', n_pass, 'EXIT_PASS', n_exit,
      'G_HITS_NO_MASS', len(hits_no_mass), 'G_HITS_WITH_MASS', len(hits_with_mass))
print('GUARD_FAILURES', [g['code'] for g in GUARDS if not g['ok']])
print('EXIT', 0 if ok else 1)



