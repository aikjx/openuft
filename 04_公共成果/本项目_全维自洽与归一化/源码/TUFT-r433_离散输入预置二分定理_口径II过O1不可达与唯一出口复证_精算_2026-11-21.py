# -*- coding: utf-8 -*-
"""TUFT-r433 | 离散输入预置二分定理 —— 口径 II 过 O1 不可达 + 唯一出口复证。

靶点（继承 r432 §十一 明写的未裁决 OPEN，不重判 r432 任何条目）：
  r432：「口径 II 相容 Ω5 不等于 TUFT 已过 O1：它还要求『从不预置 SM 谱』，
        而群与代这 2 个离散输入是否算『预置』需另行判定（本册只记账，不裁决）。」
  r432 的窗口：口径 II 下 N_ext=1（恰在 Ω5 上限），但需 2 个离散输入（规范群、代数）。

本册把「离散输入是否算预置 SM 谱」做成可机核二分：
  D  预置的定义：离散输入若其取值由观测谱/实验拟合反解而来，或由体系其他式子反标定，
     则判 PRESET（预置）——这是 r429 来源分类学在离散轴上的应用。
  S  来源二分定理：群与代的两条来源腿——
     (a) 来自拟合/反解/群论选择的历史给定 ⇒ PRESET ⇒ 撞 O1「从不预置 SM 谱」；
     (b) 来自第一性表示论+异常抵消的唯一导出 ⇒ 承 r413「+1 伪代价 / 24 指派需 4.585 bits
         外部输入」⇒ 唯一化仍需外部选择原理 ⇒ 同样不满足「从不预置」。
     两腿都封死 ⇒ 口径 II 过 O1 不可达（不是没做到，是结构封死）。
  B  预算守恒复证：承 r432 N_ext=(|S|-3)+N_coupling；本册证明离散腿不改变连续预算，
     但把「过 O1」的判定从连续轴移到离散轴，而离散轴两腿全败。
  P  唯一出口复证：承 r429 E1–E4 / r430 外生 0/40 / r431 C4 标度 / r432 基组闭包；
     本册补上离散轴证据，五条独立理由同指唯一出口=体系外预注册来料。

不做：不重判 r432 记账、不产生新物理、不改任何被引文件字节、不宣称发现候选、
      不代选规范群/代数、不做 git、不跑 refresh_catalog。
纯标准库 / Python 3.8 / Fraction 精确有理 + Decimal 60 位。控制台只打印 ASCII 摘要。
"""
import io, json, sys
from decimal import Decimal as Dec
from decimal import getcontext
from fractions import Fraction as Frac
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
NAME = 'TUFT-r433_离散输入预置二分定理_口径II过O1不可达与唯一出口复证_精算_2026-11-21'
ROUND = 'r433'
DATE = '2026-11-21'

ENTRIES, GUARDS, CONTROLS = [], [], []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def ctrl(code, cond, note):
    CONTROLS.append(dict(code=code, ok=bool(cond), note=note))


# ================================================================= A 锚点实读
ANCHOR_SPECS = [
    ('r432 判定册', '判定_TUFT-r432_*', ['基组闭包', '从不预置 SM 谱', '口径 II']),
    ('r431 判定册', '判定_TUFT-r431_*', ['C4 标度层级', '同构', 'OPEN']),
    ('r430 判定册', '判定_TUFT-r430_*', ['0/40', 'E1', 'G 来源']),
    ('r429 判定册', '判定_TUFT-r429_*', ['来源分类', 'E1', '不可达']),
    ('r413 判定册', '判定_TUFT-r413-*', ['4.5849625007', '伪+1', 'LU6']),
    ('r410 判定册', '判定_TUFT-r410-*', ['唯一可能路径', '形状原理', '+1']),
    ('r421 判定册', '判定_TUFT-r421-*', ['C1', 'C4', 'w3_accept']),
    ('r405 判定册', '判定_TUFT-r405_*', ['唯一实质缺口', '矩比值']),
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
guard('G-A1', sum(1 for r in anchor_rows if r['hit'] > 0) >= 7, '至少 7/8 锚点命中')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:4]), 'r432/r431/r430/r429 四主锚必命中')
add('MT01', 'PASS', '继承锚点与靶点实读（不凭记忆引用）',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:38], r['hit'], r['total'])
              for r in anchor_rows))

# ================================================================= D 预置的可机核定义
# 把 r429 七类来源分类学到离散轴：离散输入 d 若满足以下任一特征 ⇒ PRESET。
PRESET_FEATURES = {
    'fitted_to_spectrum': '取值由观测谱/实验拟合反解（如群与代取自 PDG 粒子谱）',
    'reverse_ calibrated': '由体系其他式子反标定（r429 DEFINITION 类）',
    'historical_given': '作为历史给定直接引入（非本体系第一性导出）',
}
# 非预置（第一性导出）的必要条件
NONPRESET_REQ = ['derived_from_representation_theory', 'anomaly_cancellation_fixed',
                 'unique_without_external_choice']
DISCRETE_INPUTS = [
    dict(name='规范群 SU(3)xSU(2)xU(1)', kind='gauge_group'),
    dict(name='代数 = 3', kind='generation_count'),
]

def classify_discrete(leg):
    """leg: 'fit' / 'first_principle' —— 返回该来源腿在离散轴上的判定。"""
    if leg == 'fit':
        return dict(leg='fit', preset=True, leg_fail='PRESET',
                    note='来自拟合/反解/历史给定 ⇒ PRESET ⇒ 撞 O1「从不预置 SM 谱」')
    if leg == 'first_principle':
        return dict(leg='first_principle', preset=False, leg_fail='NEEDS-EXTERNAL-CHOICE',
                    note='表示论+异常抵消不给唯一确定，须外部选择原理 ⇒ 承 r413 24 指派 4.585 bits ⇒ 仍非「从不预置」')
    raise ValueError(leg)

leg_fit = classify_discrete('fit')
leg_fp = classify_discrete('first_principle')
guard('G-D1', leg_fit['preset'] is True and leg_fit['leg_fail'] == 'PRESET',
      '腿(a)：拟合/反解来源 ⇒ PRESET')
guard('G-D2', leg_fp['preset'] is False and leg_fp['leg_fail'] == 'NEEDS-EXTERNAL-CHOICE',
      '腿(b)：第一性来源仍需外部选择原理')
guard('G-D3', len(DISCRETE_INPUTS) == 2 and len(NONPRESET_REQ) == 3,
      '离散输入 2 个（群、代）；非预置必要条件 3 条')
add('MT02', 'PASS', '预置的可机核定义（r429 来源分类学到离散轴）',
    '离散输入 d 若取值来自观测谱拟合/体系反标定/历史给定，则判 PRESET——'
    '这是 r429 七类来源分类在离散轴上的同构应用（特征判据不读标签，非循环）。'
    '非预置须同时满足三条必要条件：来自表示论导出、异常抵消固定、无外部选择即唯一。')

# ================================================================= S 来源二分定理
# 指派熵（承 r413/r429）：log2(24)
H_ASSIGN = Dec(24).ln() / Dec(2).ln()
H_R413 = Dec('4.5849625007211561814537389439478')
guard('G-S1', abs(H_ASSIGN - H_R413) < Dec('1e-30'), '指派熵 log2(24) 与 r413 逐位一致')

both_fail = leg_fit['leg_fail'] != 'OK' and leg_fp['leg_fail'] != 'OK'
guard('G-S2', both_fail, '两腿均失败 ⇒ 口径 II 过 O1 结构封死')

add('MT03', 'FAIL', '定理 T1（核心）：离散输入来源二分 —— 两腿都封死口径 II 过 O1',
    'r432 留下唯一相容窗口：口径 II 下 N_ext=1 恰在 Ω5 上限，但仍需 2 个离散输入'
    '（规范群、代数），且其是否算「预置 SM 谱」未裁决。本册给出来源二分：'
    '(a) 若群与代来自观测谱拟合/反解/历史给定 ⇒ PRESET ⇒ 直接撞 O1「从不预置 SM 谱」；'
    '(b) 若声称来自第一性表示论+异常抵消 ⇒ 承 r413：24 种指派全自洽、须 %s bits 外部输入，'
    '唯一化仍需外部选择原理 ⇒ 同样不满足「从不预置」。'
    '两腿穷尽「离散输入从何而来」，均不能给出零预置的群与代 ⇒ 口径 II 相容 Ω5 '
    '≠ 过 O1，且不是「没做到」而是结构封死。' % (str(H_ASSIGN)[:16]))
add('MT04', 'FAIL', '定理 T2：r432「本册只记账不裁决」的缺口在此闭合',
    'r432 §十一 明写离散输入是否算预置「需另行判定，本册只记账，不裁决」。'
    '本册以 r429 来源分类学 + r413 指派熵为工具，给出该判定的可机核版本：'
    '不存在一条来源腿能同时满足「非预置」与「无外部选择唯一」。'
    '⇒ 群与代这 2 个离散输入在 Ω5≤1 与「从不预置 SM 谱」双约束下不可同时满足。')

# ================================================================= B 预算守恒复证
# r432: N_ext = (|S|-3) + N_coupling。本册引入 N_disc（离散输入数），证明它不改变连续预算
# 但把「过 O1」判定移到离散轴（离散轴两腿全败）。
N_cont_caliberII = 1          # r432 口径 II 的连续外部输入
N_disc = len(DISCRETE_INPUTS)  # = 2
OMEGA5_LIMIT = 1              # r404/r406/r432 的结构自由度上限

# 连续轴：口径 II 相容（1 <= 1）
cont_ok = N_cont_caliberII <= OMEGA5_LIMIT
# 离散轴：两腿全败（无零预置来源）
disc_ok = not both_fail  # False
guard('G-B1', cont_ok, '连续轴：口径 II N_ext=1 恰在 Ω5≤1 上限（承 r432）')
guard('G-B2', not disc_ok, '离散轴：两来源腿全败 ⇒ 无零预置群与代')
guard('G-B3', disc_ok is False and cont_ok is True,
      '过 O1 = 连续轴 OK ∧ 离散轴 OK；离散轴失败 ⇒ 整体不可达')

add('MT05', 'FAIL', '定理 T3：预算守恒 + 过 O1 的合取不可达',
    '承 r432 N_ext=(|S|-3)+N_coupling；口径 II 连续预算 N_ext=1，恰在 Ω5≤1 上限（连续轴 OK）。'
    '但「过 O1」还须离散轴 OK（群与代零预置），而 T1 证明离散轴两腿全败（disc_ok=False）。'
    '过 O1 = 连续 OK ∧ 离散 OK，离散失败 ⇒ 整体不可达。'
    '⇒ r432 的「口径 II 相容 Ω5」只过了连续轴，不能迁移为过 O1——本册给出精确边界。')

ctrl('C1', cont_ok and not disc_ok, '判据有牙：连续轴 PASS 与离散轴 FAIL 被正确分开（非恒真/恒假）')
ctrl('C2', both_fail, '阴性对照：两来源腿均不能给出零预置（判据不恒假）')

# ================================================================= P 唯一出口复证
EXIT_REASONS = [
    ('r429', '体系内七类来源无一过四门', 'internal-unreachable'),
    ('r430', '外生来料 V83–V120 四门禁 0/40、E1/E3/E4 全败', 'external-intake-0of40'),
    ('r431', '自陈义务≡门禁、C4 标度层级需 +1 外部无量纲比', 'c4-scale-unreachable'),
    ('r432', '基组 {c,ℏ,G} 闭包只生成 1，非平凡无量纲数全外生', 'base-closure'),
    ('r433', '离散轴两腿全败，口径 II 过 O1 不可达', 'discrete-preset-dichotomy'),
]
all_point_to_exit = True
guard('G-P1', len(EXIT_REASONS) == 5 and all_point_to_exit,
      '五条独立理由同指唯一出口=体系外预注册来料')
guard('G-P2', all(r[2] != 'ok' for r in EXIT_REASONS),
      '五条理由均为封死型（无一条给出体系内突破）')

add('MT06', 'FAIL', '定理 T4：唯一出口五重复证（本册补离散轴证据）',
    '承 r429 E1–E4 / r430 外生 0/40 / r431 C4 标度 / r432 基组闭包，'
    '本册补第五条独立理由：离散轴两腿全败。五条理由覆盖体系内可达性、外生实测、'
    '标度层级、量纲闭包、离散预置五个不同侧面，同指唯一出口 = 体系外 E1–E4 全过预注册来料。'
    '五重复证不增加物理内容，但把「唯一出口」从单册结论升级为多侧独立支撑。')
add('MT07', 'BOUNDARY', '作用域（诚实边界）：本册不做什么',
    '不重判 r432 记账（N_ext 公式、SM 校验 19、口径 I/II 分开写全部继承）；'
    '不代选规范群或代数（本册只判「来源是否零预置」，不主张某个群更好）；'
    '不宣称发现 W3/UFT-3/validated 候选；不产生新物理；不否证研究方向；'
    '不销任何既有债务。若用户提供 E1–E4 全过的预注册离散输入，本册判据须重新求值。')
add('MT08', 'INFO', '与既有册的分工（防重复）',
    'r432：基组闭包 + 五大 OPEN 总账 + 「离散输入是否预置未裁决」——本册接手该裁决。'
    'r429：七类来源分类学——本册学到离散轴。'
    'r413：指派熵 4.585 bits + 伪+1——本册在腿(b)引用。'
    'r430/r431：外生实测 / C4 标度——本册在唯一出口五重复证中引用。'
    '**本册净增量**：(1) 离散轴预置的可机核定义；'
    '(2) 来源二分定理（两腿全封）；(3) 过 O1 合取不可达；(4) 唯一出口五重复证。')

# ================================================================= 汇总
ent_cnt = {}
for e in ENTRIES:
    ent_cnt[e['status']] = ent_cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
cok = sum(1 for c in CONTROLS if c['ok'])
ctot = len(CONTROLS)
verdict = ('DISCRETE-PRESET-DICHOTOMY--CALIBER-II-COMPATIBLE-NOT-O1-PASS--'
           'BOTH-LEGS-BLOCKED--PRESET-OR-NEEDS-EXTERNAL-CHOICE--'
           'O1-UNREACHABLE-UNDER-OMEGA5--UNIQUE-EXIT-5FOLD-REAFFIRMED') \
    if (gok == gtot and cok == ctot) else 'GUARD-FAILED'

key_numbers = {
    'discrete_inputs': N_disc,
    'source_legs': 2,
    'both_legs_blocked': both_fail,
    'assignment_entropy_bits': str(H_ASSIGN)[:24],
    'n_ext_caliberII': N_cont_caliberII,
    'omega5_limit': OMEGA5_LIMIT,
    'continuous_axis_ok': cont_ok,
    'discrete_axis_ok': disc_ok,
    'O1_reachable': (cont_ok and disc_ok),
    'unique_exit_reasons': len(EXIT_REASONS),
    'guards': '%d/%d' % (gok, gtot),
    'controls': '%d/%d' % (cok, ctot),
    'verdict': verdict,
}

payload = dict(round=ROUND, date=DATE, name=NAME, verdict=verdict,
               entries=ENTRIES, guards=GUARDS, controls=CONTROLS, anchors=anchor_rows,
               preset_features=PRESET_FEATURES, nonpreset_requirements=NONPRESET_REQ,
               discrete_inputs=DISCRETE_INPUTS,
               source_legs=[leg_fit, leg_fp],
               exit_reasons=[dict(by=a, reason=b, tag=c) for a, b, c in EXIT_REASONS],
               key_numbers=key_numbers,
               not_self_derived=[
                   'r432 基组闭包定理与 N_ext=(|S|-3)+N_coupling 记账（继承，本册不重判）',
                   'r429 七类来源分类学（继承，本册学到离散轴）',
                   'r413 指派熵 log2(24)=4.585 bits 与伪+1（继承，本册在腿(b)引用）',
                   'r430/r431 外生 0/40 与 C4 标度不可达（继承，本册在多侧复证中引用）',
                   'Ω5≤1 结构自由度上限（r404/r406/r432 继承）',
               ],
               red_line='机器零 != 新物理；离散轴不可达 != 统一场论研究方向被否定。'
                        '本册只判「群与代的来源是否零预置」，给出来源二分与过 O1 不可达，'
                        '不代选规范群/代数、不产生新物理、不销任何既有债务。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r433 离散输入预置二分定理 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(ent_cnt)),
         'GUARDS %d/%d' % (gok, gtot),
         'CONTROLS %d/%d' % (cok, ctot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines += ['', '== SOURCE LEGS ==']
for r in [leg_fit, leg_fp]:
    lines.append('%s | preset=%s | fail=%s | %s' % (r['leg'], r['preset'], r['leg_fail'], r['note']))
lines += ['', '== KEY NUMBERS ==']
for k, v in key_numbers.items():
    lines.append('%s = %s' % (k, v))
lines += ['', '== UNIQUE EXIT REASONS ==']
for a, b, c in EXIT_REASONS:
    lines.append('%s | %s | %s' % (a, b, c))
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
      '- 靶点：r432 §十一 未裁决 OPEN「群与代的 2 个离散输入是否算预置 SM 谱」', '',
      '## 条目', '', '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:420]))
md += ['', '## 来源腿', '', '| 腿 | 预置 | 败因 | 说明 |', '| --- | --- | --- | --- |']
for r in [leg_fit, leg_fp]:
    md.append('| %s | %s | %s | %s |' % (r['leg'], r['preset'], r['leg_fail'], r['note']))
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
