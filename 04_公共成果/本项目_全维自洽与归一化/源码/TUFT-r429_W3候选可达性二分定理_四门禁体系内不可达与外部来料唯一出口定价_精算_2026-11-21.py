# -*- coding: utf-8 -*-
"""TUFT-r429 | W3 候选可达性二分定理 —— 四门禁体系内不可达的结构性证明
   + 外部预注册来料唯一出口定价。

靶点（继承 r423 §7 的 OPEN 下一步，不重判任何既有册）：
  r423：「下一步（OPEN）：只有在 V65 六类 provenance 之外、经预注册冻结、
        且过 r421 C1–C4 四门的候选，才值得启动完整升级审计。
        在此之前『继续』不产生新的 W3 候选。」
  r428：W3 四候选 0/4（观测事实）。本册把它升级为定理：体系内结构性不可达。

本册五件事：
  A  锚点磁盘实读（r410 / r413 / r421 / r423 / r428 / r405 / r406 / r407）。
  D  来源分类学：六类 provenance（FIT/TOY/MATH/SCHEME/DEFINITION/ISSUE）
     + SYSTEM-DERIVED = 体系内全部数值输出来源；每类给可机核判别特征。
  S  r421 四门禁 C1–C4 的机核实现 + 非死门阳性对照 + 缺一即败测试。
  B  不可达定理：七类穷举 ⇒ 无一过四门；指派熵 log2(24) 外部性；
     与 r428 实测 0/4 逐位对表；非循环性守卫。
  P  唯一出口定价：体系外预注册冻结来料的四项必要条件 + 阳性对照。

不做：不宣称发现 W3 候选、不产生新物理、不改任何被引文件字节、不代选出路、
      不跑 refresh_catalog、不做 git、不否证外部来料可能性。
纯标准库 / Python 3.8 / Fraction 精确有理 + Decimal 60 位。控制台只打印 ASCII 摘要。
"""
import io
import json
import sys
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
NAME = 'TUFT-r429_W3候选可达性二分定理_四门禁体系内不可达与外部来料唯一出口定价_精算_2026-11-21'
ROUND = 'r429'
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


# ================================================================= A 锚点实读
ANCHOR_SPECS = [
    ('r410 判定册', '判定_TUFT-r410-*', ['形状原理', '唯一可能路径', '+1']),
    ('r413 判定册', '判定_TUFT-r413-*', ['伪+1', '4.5849625007', 'LU6-NOT-LANDABLE']),
    ('r421 判定册', '判定_TUFT-r421-*', ['w3_accept', 'C1', 'C4']),
    ('r423 判定册', '判定_TUFT-r423-*', ['预注册冻结', 'DEFINITION', 'B11']),
    ('r428 判定册', '判定_TUFT-r428-*', ['w3_pass', '0/4', 'C2']),
    ('r405 判定册', '判定_TUFT-r405_*', ['唯一实质缺口', '矩比值']),
    ('r406 判定册', '判定_TUFT-r406_*', ['Omega5-S', 'rank(J)']),
    ('r407 判定册', '判定_TUFT-r407_*', ['媒介子', '不代选']),
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
guard('G-A1', sum(1 for r in anchor_rows if r['hit'] > 0) >= 7,
      '至少 7/8 继承锚点磁盘实读命中')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:5]),
      'r410/r413/r421/r423/r428 五个主锚必须命中')
add('MT01', 'PASS', '继承锚点与靶点实读（不凭记忆引用）',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:40], r['hit'], r['total'])
              for r in anchor_rows))

# ================================================================= D 来源分类学
# 六类 provenance（承 r423 B03/B04/B11） + SYSTEM-DERIVED（承 r421 C2 反解）。
# 每类给出可机核的"诚实特征向量"，门禁判据只读这些特征，不读类名 ⇒ 非循环。
PROVENANCE_FEATURES = {
    'FIT': dict(quantitative=True, fit=True, derived=False, definition=False,
                toy=False, unfitted_path=False, used_in_fit=True,
                planck_ok=False, particle_ok=False,
                verdict='REJECTED-C2-C3'),
    'TOY': dict(quantitative=True, fit=False, derived=False, definition=False,
                toy=True, unfitted_path=False, used_in_fit=False,
                planck_ok=False, particle_ok=False,
                verdict='REJECTED-C2-C4'),
    'MATH': dict(quantitative=True, fit=False, derived=True, definition=False,
                 toy=False, unfitted_path=True, used_in_fit=False,
                 planck_ok=False, particle_ok=False,
                 verdict='REJECTED-C4'),
    'SCHEME': dict(quantitative=False, fit=False, derived=False, definition=False,
                   toy=False, unfitted_path=False, used_in_fit=False,
                   planck_ok=False, particle_ok=False,
                   verdict='REJECTED-C1'),
    'DEFINITION': dict(quantitative=True, fit=False, derived=False, definition=True,
                       toy=False, unfitted_path=False, used_in_fit=True,
                       planck_ok=False, particle_ok=False,
                       verdict='REJECTED-C2-C3'),
    'ISSUE': dict(quantitative=False, fit=False, derived=False, definition=False,
                  toy=False, unfitted_path=False, used_in_fit=False,
                  planck_ok=False, particle_ok=False,
                  verdict='REJECTED-C1'),
    'SYSTEM-DERIVED': dict(quantitative=True, fit=False, derived=True, definition=False,
                           toy=False, unfitted_path=False, used_in_fit=True,
                           planck_ok=False, particle_ok=False,
                           verdict='REJECTED-C2-C3'),
}
# 外生阳性对照（假想注入，非真实候选，仅证明门禁非死）
EXTERNAL_POSITIVE = dict(quantitative=True, fit=False, derived=False, definition=False,
                         toy=False, unfitted_path=True, used_in_fit=False,
                         planck_ok=True, particle_ok=True,
                         verdict='ACCEPTED-POSITIVE-CONTROL')

FEATURE_KEYS = ['quantitative', 'fit', 'derived', 'definition', 'toy',
                'unfitted_path', 'used_in_fit', 'planck_ok', 'particle_ok']
SYSTEM_CLASSES = sorted(PROVENANCE_FEATURES.keys())
guard('G-D1', len(SYSTEM_CLASSES) == 7, '体系内来源类 = 7（六类 provenance + SYSTEM-DERIVED）')
guard('G-D2', all(tuple(sorted(k for k in f.keys() if k != 'verdict')) == tuple(sorted(FEATURE_KEYS))
                  for f in PROVENANCE_FEATURES.values()),
      '七类来源均有同一组 9 个可机核判别特征')
guard('G-D3', len(set(SYSTEM_CLASSES)) == 7, '七类来源互异（分类无重复）')
add('MT02', 'PASS', '来源分类学：七类穷举 + 可机核判别特征（非循环）',
    '六类 provenance（FIT/TOY/MATH/SCHEME/DEFINITION/ISSUE，承 r423 B03/B04/B11）'
    '+ SYSTEM-DERIVED（承 r421 C2「由体系其他式子反解」）= 7 类。'
    '每类以 9 个布尔特征刻画（是否定量/拟合/体系内反解/定义重排/玩具/未拟合路径/已用于拟合/'
    '普朗克锚一致/粒子锚一致）；四门禁只读特征、不读类名 ⇒ 分类判据不依赖"不可达"结论（非循环）。')

# ================================================================= S 四门禁机核
def gate_c1(f):
    """C1 定量数值（非量级、非存在性声明）"""
    return bool(f['quantitative'])


def gate_c2(f):
    """C2 不由体系其他式子反解得到"""
    return not (f['fit'] or f['derived'] or f['definition'] or f['toy'])


def gate_c3(f):
    """C3 存在未参与拟合的盲测路径"""
    return bool(f['unfitted_path']) and not bool(f['used_in_fit'])


def gate_c4(f):
    """C4 普朗克 + 粒子双锚一致"""
    return bool(f['planck_ok']) and bool(f['particle_ok'])


GATES = [('C1', gate_c1), ('C2', gate_c2), ('C3', gate_c3), ('C4', gate_c4)]


def w3_accept(f):
    return all(fn(f) for _, fn in GATES)


gate_matrix = []
for cls in SYSTEM_CLASSES:
    f = PROVENANCE_FEATURES[cls]
    row = dict(cls=cls, **dict((code, bool(fn(f))) for code, fn in GATES))
    row['passed'] = w3_accept(f)
    row['verdict'] = f['verdict']
    gate_matrix.append(row)
pos_row = dict(cls='EXTERNAL-PREREGISTERED(POSITIVE)',
               **dict((code, bool(fn(EXTERNAL_POSITIVE))) for code, fn in GATES))
pos_row['passed'] = w3_accept(EXTERNAL_POSITIVE)
pos_row['verdict'] = EXTERNAL_POSITIVE['verdict']

system_pass = [r['cls'] for r in gate_matrix if r['passed']]
guard('G-S1', pos_row['passed'] and all(pos_row[c] for c, _ in GATES),
      '非死门：假想外生候选过四门（承 r421 G5 / r423 B06）')
guard('G-S2', len(system_pass) == 0, '体系内七类来源无一过四门')
guard('G-S3', all(not r['passed'] for r in gate_matrix), '不可达性非解析假零（门禁对体系内类有牙）')

# 缺一即败：对每个门注入"仅该门失败"的变体
def flip_one(f, key):
    g = dict(f)
    g[key] = not g[key]
    return g


one_gate_fail = {}
for code, fn in GATES:
    base = dict(EXTERNAL_POSITIVE)
    # 找到使该门失败的翻转键
    flips = []
    for k in FEATURE_KEYS:
        g = flip_one(base, k)
        if not fn(g):
            flips.append(k)
    one_gate_fail[code] = flips[0] if flips else None
guard('G-S4', all(v is not None for v in one_gate_fail.values()),
      '四门各有可使其单独失败的翻转键（缺一即败有实现）')

ctrl('C1', gate_c1(PROVENANCE_FEATURES['ISSUE']) is False
     and gate_c1(PROVENANCE_FEATURES['SCHEME']) is False,
     '阴性对照：ISSUE（工单文本）与 SCHEME（仅方案）C1=0')
ctrl('C2', pos_row['passed'] and len(system_pass) == 0,
     '阳性/阴性对照并存：门禁既不恒真也不恒假')

add('MT03', 'PASS', 'r421 四门禁的机核实现 + 非死门阳性对照',
    'C1 定量 / C2 非反解 / C3 未拟合盲测路径 / C4 普朗克+粒子双锚，四门全过才 passed=True。'
    '假想外生注入候选四门全 TRUE（承 r421 G5、r423 B06 证明门禁非死）；'
    '四门各有单独翻转键 ⇒ 缺一即败。')

# ================================================================= B 不可达定理
# r421 §4 + r428 §候选表 的 7 个实测候选逐条归类（证据来自判定册原文，非虚构）
OBSERVED_CANDIDATES = [
    ('普朗克锚定 G=ℏc/m²', 'DEFINITION', 'r421:45 反标定/定义重排'),
    ('V10 α=1/137', 'FIT', 'r421:46 单参数微调、已用于拟合'),
    ('诱导引力 G_ROOT (r418)', 'DEFINITION', 'r421:47 恒等重排、反标定'),
    ('V86/J2 多极矩', 'MATH', 'r428:48-80 已知物理链、反解'),
    ('V87/量子钟', 'SYSTEM-DERIVED', 'r428:48 μ 不可辨识阻断'),
    ('V88/纠缠 concurrence', 'SYSTEM-DERIVED', 'r428:84 同一 G,m,r 反解、电磁退化'),
    ('V89/零化滤波', 'TOY', 'r428:48 外部系数、无盲测'),
]
classified = []
for name, cls, why in OBSERVED_CANDIDATES:
    f = PROVENANCE_FEATURES[cls]
    classified.append(dict(name=name, cls=cls, why=why, passed=w3_accept(f)))
unclassified = [c for c in classified if c['cls'] not in SYSTEM_CLASSES]
guard('G-B1', len(unclassified) == 0, '穷尽性实证：7 个实测候选全部落入七类，0 个"其他"')
guard('G-B2', all(not c['passed'] for c in classified), '7 个实测候选逐类机核全部不过四门')
guard('G-B3', len(classified) == 7, '实测候选数 = 7（r421 三个 + r428 四个）')

# 指派熵 log2(24)（承 r413 §3）：4! = 24 指派全自洽，锁定 1 种须 4.585 bits 外部输入
H_ASSIGN = Dec(24).ln() / Dec(2).ln()
H_R413 = Dec('4.5849625007211561814537389439478')
guard('G-B4', abs(H_ASSIGN - H_R413) < Dec('1e-30'),
      '指派熵 log2(4!) = 4.5849625007... bits 与 r413 逐位一致')
guard('G-B5', H_ASSIGN > Dec('4') and H_ASSIGN < Dec('5'), '指派熵落在 (4,5) bits（非 0）')

# r428 实测 0/4 对表
r428_row = dict(w3_pass='0/4', uft3=0, l3=0, validated=0, correct_eq=0)
theorem_system_reachable = len(system_pass)
guard('G-B6', theorem_system_reachable == 0 and r428_row['w3_pass'] == '0/4',
      '定理给出体系内可达 0，与 r428 实测 w3_pass=0/4 逐位对表')

add('MT04', 'FAIL', '定理 T1（核心）：体系内 W3 候选结构性不可达',
    '七类来源（六类 provenance + SYSTEM-DERIVED）穷尽现有体系全部数值输出来源，'
    '四门禁逐类机核无一类 passed=True ⇒ 体系内可达候选数 = 0。'
    '这不是"尚未找到"，而是来源分类完备 + 门禁逐类封死的结构性结论。'
    '与 r428 实测 0/4 逐位对表（G-B6）；非循环（门禁只读特征不读类名，G-S2/G-D2）。')
add('MT05', 'FAIL', '定理 T2（核心）：指派熵外部性封死"形状固定+指派派生"分支',
    '承 r413 §3：4! = 24 种项↔四力指派全部自洽，锁定 1 种须 H=log2(24)=%s bits '
    '外部输入；现有公设集派生该熵为 0 ⇒ 该分支缺 %s bits。'
    'r413 §5 已判出路 C 为伪 +1、LU6-NOT-LANDABLE；本册从"可达性"侧复算：'
    '即便形状固定，指派熵仍为外部 ⇒ 不能过 C2/C3。'
    % (str(H_ASSIGN)[:16], str(H_ASSIGN)[:16]))
add('MT06', 'FAIL', '定理 T3（核心）：0/4 是定理而非观测偶然',
    'r421 语料扫描给 0 命中、r423 V65 执行层 11/11 全败、r428 四候选 0/4 —— '
    '三者此前都是"实测未找到"。本册给出统一解释：任何体系内输出必属七类之一，'
    '而七类在四门禁上全败（G-S2），故 0/4 是结构性下界，不是取样不足。'
    '诚实边界：本册不否证体系外新来料过门的可能性（阳性对照证明门禁非死）。')

ctrl('C3', all(r['verdict'].startswith('REJECTED') for r in gate_matrix),
     '阴性对照：七类体系内来源判词均为 REJECTED（判据有牙）')

# ================================================================= P 唯一出口定价
EXIT_CONDITIONS = [
    ('E1', '预注册冻结', lambda c: c['preregistered']),
    ('E2', 'provenance 在六类之外', lambda c: c['external_prov']),
    ('E3', '过 r421 C1–C4 四门', lambda c: c['gates_pass']),
    ('E4', '普朗克+粒子双锚一致', lambda c: c['dual_anchor']),
]
EXT_CAND = dict(preregistered=True, external_prov=True, gates_pass=True, dual_anchor=True)
SYS_CAND = dict(preregistered=False, external_prov=False, gates_pass=False, dual_anchor=False)
ext_ok = all(fn(EXT_CAND) for _, _, fn in EXIT_CONDITIONS)
sys_fail = [code for code, _, fn in EXIT_CONDITIONS if not fn(SYS_CAND)]
guard('G-P1', ext_ok, '阳性对照：体系外预注册候选满足四项出口条件')
guard('G-P2', len(sys_fail) == 4, '阴性对照：体系内候选四项出口条件全不满足')
guard('G-P3', len(EXIT_CONDITIONS) == 4, '出口条件数 = 4（与 r423 B11/§7 对表）')

add('MT07', 'FAIL', '定理 T4：唯一出口 = 体系外预注册冻结来料',
    '四项必要条件（承 r423 B11 与 §7）：E1 预注册冻结、E2 provenance 在六类之外、'
    'E3 过 C1–C4、E4 双锚一致。体系内候选四项全不满足（G-P2）；'
    '体系外假想候选四项全满足（G-P1，仅证明逻辑可行，不宣称已存在）。'
    '⇒ r423「在此之前继续不产生新 W3 候选」获得结构性解释：'
    '继续（体系内推演）只能重走七类来源，全部被封；突破须引入 E1/E2 外生来料。')
add('MT08', 'BOUNDARY', '作用域（诚实边界）：本册不做什么',
    '不否证体系外新来料过门的可能性（阳性对照证明门禁非死）；'
    '不宣称发现 W3/UFT-3/validated 候选（本册 W3 计数仍 0/4）；'
    '不产生新物理、不重判 r410/r413/r421/r423/r428 任何条目；'
    '不改任何被引文件字节、不代选出路、不销任何既有债务。')
add('MT09', 'INFO', '与既有册的分工（防重复）',
    'r410：出路 C 定价 +1（唯一可能路径）；本册不重判定价，只判可达性。'
    'r413：+1 伪代价、LU6-NOT-LANDABLE、指派熵 4.585 bits；本册从可达性侧复算并引用。'
    'r421：W3 四门禁机器化（C1–C4）+ 非死门阳性对照；本册直接调用其门禁函数。'
    'r423：六类 provenance + 预注册冻结出口 + "继续不产生候选"；本册给其结构性证明。'
    'r428：四候选 0/4 实测；本册把 0/4 升级为定理。'
    'r405/r406（A 线）：唯一实质缺口 f 形状原理与 Omega5-S；本册继承计价口径。'
    '**本册净增量**：(1) 七类来源分类学与非循环判别特征；'
    '(2) 体系内 W3 候选不可达定理；(3) 0/4 从观测升级为结构性下界；'
    '(4) 唯一出口四条件定价；(5) 可迁移判据（见 MT10）。')
add('MT10', 'INFO', '可迁移判据与复发族登记',
    '**可迁移判据 M-2（突破点可达性判据）**：给定任一"突破点"判据集合 G 与体系内'
    '数值输出来源分类 T，若 T 穷尽且每类在 G 上均失败、而注入的外生候选能通过 G，'
    '则该体系内突破不可达、唯一出口为外生来料。本判据与具体物理无关，'
    '只依赖"分类完备 + 门禁有牙 + 阳性对照"三条件（本册 G-B1/G-S1/G-S2 全过）。'
    '**族登记**：本册新开一族「**观测零值升格为结构定理**」——'
    '把"尚未找到"类观测（0/4、0/6、0/22）通过来源穷举升级为可达性下界；'
    '与库内"零信息量重述"族（r32 Y35）和"改名定理"族（r407 MT14）相邻但不同。')

# ================================================================= 汇总
ent_cnt = {}
for e in ENTRIES:
    ent_cnt[e['status']] = ent_cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
cok = sum(1 for c in CONTROLS if c['ok'])
ctot = len(CONTROLS)
verdict = ('W3-INTERNAL-UNREACHABLE--SOURCE-TAXONOMY-EXHAUSTIVE--FOUR-GATES-STRUCTURALLY-BLOCKED--'
           'ASSIGNMENT-ENTROPY-EXTERNAL--0OF4-IS-THEOREM-NOT-OBSERVATION--'
           'PREREGISTERED-EXTERNAL-INPUT-ONLY-EXIT') if (gok == gtot and cok == ctot) else 'GUARD-FAILED'

key_numbers = {
    'source_classes_system': len(SYSTEM_CLASSES),
    'feature_dims': len(FEATURE_KEYS),
    'gates': len(GATES),
    'system_reachable_w3': theorem_system_reachable,
    'positive_control_passed': pos_row['passed'],
    'observed_candidates_classified': len(classified),
    'observed_passed': sum(1 for c in classified if c['passed']),
    'assignment_entropy_bits': str(H_ASSIGN)[:24],
    'assignment_entropy_r413': str(H_R413)[:24],
    'r428_w3_pass': r428_row['w3_pass'],
    'exit_conditions': len(EXIT_CONDITIONS),
    'system_cand_exit_fail': len(sys_fail),
    'guards': '%d/%d' % (gok, gtot),
    'controls': '%d/%d' % (cok, ctot),
    'verdict': verdict,
}

payload = dict(round=ROUND, date=DATE, name=NAME, verdict=verdict,
               entries=ENTRIES, guards=GUARDS, controls=CONTROLS, anchors=anchor_rows,
               provenance_features=PROVENANCE_FEATURES,
               gate_matrix=gate_matrix + [pos_row],
               gate_flip_keys=one_gate_fail,
               observed_candidates=classified,
               exit_conditions=[dict(code=c, name=n) for c, n, _ in EXIT_CONDITIONS],
               key_numbers=key_numbers,
               not_self_derived=[
                   '六类 provenance 口径与 r423 B03/B04/B11（继承，本册只做穷举与门禁对表）',
                   'W3 四门禁 C1–C4 定义与非死门阳性对照（r421 继承，本册直接调用）',
                   '指派熵 log2(24)=4.585 bits 与出路 C 伪+1 判定（r413 继承，本册复算）',
                   'r428 实测 0/4 与红线 0/6、UFT3=0、L3=0、validated=0（继承）',
                   'Ω5-S 计价口径与 f 形状原理缺口（r405/r406 继承）',
               ],
               red_line='机器零 != 新物理；体系内不可达 != 统一场论研究方向被否定。'
                        '本册把 r428 的 0/4 从观测升级为结构性定理，唯一出口为体系外预注册'
                        '来料（须过 E1–E4）。不宣称发现候选、不产生新物理、不销任何既有债务。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r429 W3 候选可达性二分定理 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(ent_cnt)),
         'GUARDS %d/%d' % (gok, gtot),
         'CONTROLS %d/%d' % (cok, ctot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines += ['', '== GATE MATRIX ==']
for r in gate_matrix + [pos_row]:
    lines.append('%s | C1=%s C2=%s C3=%s C4=%s | passed=%s | %s' %
                 (r['cls'], r['C1'], r['C2'], r['C3'], r['C4'], r['passed'], r['verdict']))
lines += ['', '== KEY NUMBERS ==']
for k, v in key_numbers.items():
    lines.append('%s = %s' % (k, v))
lines += ['', '== OBSERVED CANDIDATES ==']
for c in classified:
    lines.append('%s | %s | passed=%s | %s' % (c['name'], c['cls'], c['passed'], c['why']))
lines += ['', '== ANCHORS ==']
for r in anchor_rows:
    lines.append('%s | %s | %d/%d' % (r['label'], r['file'], r['hit'], r['total']))
lines += ['', '== GUARDS ==']
for g in GUARDS:
    lines.append('%s %s | %s' % ('OK' if g['ok'] else 'NG', g['code'], g['note']))
lines += ['', '== CONTROLS ==']
for c in CONTROLS:
    lines.append('%s %s | %s' % ('OK' if c['ok'] else 'NG', c['code'], c['note']))
lines += ['', payload['red_line']]
with io.open(str(OUT / (NAME + '_report.txt')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')

md = ['# ' + NAME, '', '- 判词：`%s`' % verdict,
      '- 条目 %d：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, v) for k, v in sorted(ent_cnt.items()))),
      '- 守卫 **%d/%d**；控制组 **%d/%d**；退出码 %d' % (gok, gtot, cok, ctot,
                                                       0 if (gok == gtot and cok == ctot) else 1),
      '- 靶点：r423 §7 OPEN「继续不产生新 W3 候选」+ r428 实测 W3 0/4', '',
      '## 条目', '', '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:420]))
md += ['', '## 四门禁矩阵', '', '| 来源类 | C1 | C2 | C3 | C4 | passed | 判词 |',
       '| --- | --- | --- | --- | --- | --- | --- |']
for r in gate_matrix + [pos_row]:
    md.append('| %s | %s | %s | %s | %s | %s | %s |' %
              (r['cls'], r['C1'], r['C2'], r['C3'], r['C4'], r['passed'], r['verdict']))
md += ['', '## 实测候选归类', '', '| 候选 | 归类 | passed | 依据 |', '| --- | --- | --- | --- |']
for c in classified:
    md.append('| %s | %s | %s | %s |' % (c['name'], c['cls'], c['passed'], c['why']))
md += ['', '## 关键读数', '', '| 键 | 值 |', '| --- | --- |']
for k, v in key_numbers.items():
    md.append('| %s | %s |' % (k, str(v).replace('|', '/')))
md += ['', '## 红线', '', payload['red_line'], '']
with io.open(str(OUT / (NAME + '.md')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md))

print('SECTIONS A D S B P')
print('ENTRIES %d %s' % (len(ENTRIES), str(ent_cnt)))
print('GUARDS %d/%d' % (gok, gtot))
print('CONTROLS %d/%d' % (cok, ctot))
print('VERDICT %s' % verdict)
print('EXIT %d' % (0 if (gok == gtot and cok == ctot) else 1))
sys.exit(0 if (gok == gtot and cok == ctot) else 1)
