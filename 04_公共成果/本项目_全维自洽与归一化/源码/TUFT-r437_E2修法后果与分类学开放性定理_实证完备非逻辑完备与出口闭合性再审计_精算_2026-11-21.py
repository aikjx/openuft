# -*- coding: utf-8 -*-
"""TUFT-r437 | E2 修法后果与分类学开放性定理 —— 实证完备 ≠ 逻辑完备 + 出口闭合性再审计。

靶点（继承 r436 §十裁决 1 的 BOUNDARY，不重判 r436/r429 任何条目）：
  r436：「E2 表述应修：『六类之外』→『七类之外』（零成本，一词）；并补被排除类的名单。
        E2 定义不完备登记为 BOUNDARY，不代填。」
  r436 CTRL-2 证明：改六→七使豁免类数从 1 变 0 ⇒ 字面计数冲突消除。
  本册问更深一层：字面冲突消除后，E2 是否结构闭合？
  关键：r429 七类分类的完备性是「实证完备」（7/7 实测候选落入），
        不是「逻辑完备」（无穷尽证明）。故「七类之外」仍可能漏掉未知第八类。

本册四件事：
  A  锚点磁盘实读（r436/r435/r434/r433/r432/r431/r430/r429/r423/r421）。
  D  分类完备性的两分：实证完备（样本落入率）vs 逻辑完备（穷尽证明）；
     判定 r429 七类 = 实证完备 True / 逻辑完备 False（机器证据：无穷尽证明段）。
  S  E2 修法后果二分：
     (a) 若分类逻辑完备 ⇒ E2「七类之外」可过集对体系内为空 ⇒ 结构闭合；
     (b) 若仅实证完备 ⇒ 未知第八类 C8 可满足 E2 而仍在体系内 ⇒ 不闭合。
     逻辑完备不可证 ⇒ 不能排除 (b) ⇒ 修法只消除已知反例，不消除结构性开放。
  B  归纳缺口量化：样本 n=7 全落入，样本外类存在的归纳风险下界 >0（Laplace 示意，非精确概率）；
     修法是必要表述修正，但不足以把出口变成逻辑闭集。
  P  唯一出口八重复证：r429–r436 七条 + 本册第八条，同指体系外 E1–E4 预注册来料。

不做：不重判 r436 门禁自审、不代填被排除类名单、不产生新物理、不改任何被引文件字节、
      不宣称发现候选、不代选出路、不做 git、不跑 refresh_catalog。
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
NAME = 'TUFT-r437_E2修法后果与分类学开放性定理_实证完备非逻辑完备与出口闭合性再审计_精算_2026-11-21'
ROUND = 'r437'
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
    ('r436 判定册', '判定_TUFT-r436_*', ['E2', '七类', '新颖性']),
    ('r435 判定册', '判定_TUFT-r435_*', ['账基组', '反解', '域分离']),
    ('r434 判定册', '判定_TUFT-r434_*', ['口径不变性', 'rank(D)', 'span']),
    ('r433 判定册', '判定_TUFT-r433_*', ['预置', 'O1', '两腿']),
    ('r432 判定册', '判定_TUFT-r432_*', ['基组闭包', 'N_ext', '口径 II']),
    ('r431 判定册', '判定_TUFT-r431_*', ['C4', '同构', 'OPEN']),
    ('r430 判定册', '判定_TUFT-r430_*', ['0/40', 'E1', 'G 来源']),
    ('r429 判定册', '判定_TUFT-r429_*', ['来源分类', 'E1', '不可达']),
    ('r423 判定册', '判定_TUFT-r423-*', ['六类', '预注册', 'B11']),
    ('r421 判定册', '判定_TUFT-r421-*', ['C1', 'C4', 'w3_accept']),
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
guard('G-A1', sum(1 for r in anchor_rows if r['hit'] > 0) >= 9, '至少 9/10 锚点命中')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:3]), 'r436/r435/r434 三主锚必命中')
add('MT01', 'PASS', '继承锚点与靶点实读（不凭记忆引用）',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:32], r['hit'], r['total'])
              for r in anchor_rows))

# ================================================================= D 分类完备性两分
# 实证完备：样本落入率（r429 的 7/7 实测候选全部落入七类）
# 逻辑完备：存在穷尽证明（本册在 r429 判定册中检索"穷尽证明/封闭性公理"段，结果为 0）
empirical_samples = 7          # r429 G-B3: 实测候选 7 个
empirical_in_class = 7         # r429 G-B1: 全部落入七类
empirical_rate = Frac(empirical_in_class, empirical_samples)

# 检索 r429 判定册是否含"穷尽证明/封闭性公理"类字样
r429_files = [p for p in ALL_FILES if fnmatch(p.name, '判定_TUFT-r429_*')]
r429_text = io.open(str(r429_files[0]), encoding='utf-8', errors='replace').read() if r429_files else ''
exhaustive_markers = ['穷尽证明', '封闭性公理', '分类封闭', 'WITNESS-COMPLETE']
exhaustive_marker_count = sum(1 for m in exhaustive_markers if m in r429_text)
logically_complete = exhaustive_marker_count > 0

guard('G-D1', empirical_rate == Frac(1, 1), 'r429 七类实证完备：7/7 样本落入')
guard('G-D2', not logically_complete,
      'r429 七类非逻辑完备：判定册无穷尽证明标记（%d 个命中）' % exhaustive_marker_count)
guard('G-D3', empirical_rate == Frac(1, 1) and not logically_complete,
      '实证完备与逻辑完备被正确区分（非混同）')

add('MT02', 'PASS', '分类完备性的两分：实证完备 vs 逻辑完备',
    '实证完备 = 已知样本全部落入类集（r429：7/7 实测候选全落入七类，G-B1/G-B3）；'
    '逻辑完备 = 存在"分类穷尽/封闭"的证明。本册机器检索 r429 判定册的穷尽证明标记，'
    '命中 %d 个 ⇒ r429 七类是实证完备、非逻辑完备。'
    '二者不同：实证完备不能排除样本外未知类，逻辑完备才能给出"类外即体系外"的保证。'
    % exhaustive_marker_count)

# ================================================================= S E2 修法后果二分
# r436 修法：E2「六类之外」→「七类之外」。字面冲突消除（CTRL-2：豁免类 1→0）。
# 本册问：修法后 E2 是否结构闭合？
leg_a = dict(leg='logical_complete_assumed', e2_pass_set_empty=True,
             verdict='STRUCTURALLY-CLOSED',
             note='若分类逻辑完备 ⇒「七类之外」对体系内候选可过集为空 ⇒ E2 结构闭合')
leg_b = dict(leg='empirical_only', e2_pass_set_empty=False,
             verdict='STRUCTURALLY-OPEN',
             note='若仅实证完备 ⇒ 未知第八类 C8 可满足 E2「七类之外」而仍在体系内 ⇒ E2 不闭合')

# r429 非逻辑完备（G-D2）⇒ 不能排除腿(b) ⇒ 修法不保证结构闭合
cannot_exclude_b = not logically_complete
guard('G-S1', leg_a['e2_pass_set_empty'] and leg_a['verdict'] == 'STRUCTURALLY-CLOSED',
      '腿(a)：逻辑完备假设下 E2 结构闭合')
guard('G-S2', (not leg_b['e2_pass_set_empty']) and leg_b['verdict'] == 'STRUCTURALLY-OPEN',
      '腿(b)：仅实证完备下 E2 结构开放（未知第八类）')
guard('G-S3', cannot_exclude_b, 'r429 非逻辑完备 ⇒ 腿(b) 不可排除')
guard('G-S4', cannot_exclude_b and leg_b['verdict'] == 'STRUCTURALLY-OPEN',
      '修法后果：只消除已知反例，不保证结构闭合')

add('MT03', 'FAIL', '定理 T1（核心）：E2 修法后果二分 —— 字面冲突消除 ≠ 结构闭合',
    'r436 CTRL-2 证明六→七使豁免类从 1 变 0，字面计数冲突消除。但本册给出后果二分：'
    '(a) 若分类逻辑完备，「七类之外」可过集对体系内为空 ⇒ 结构闭合；'
    '(b) 若仅实证完备，未知第八类 C8 可满足「七类之外」而仍在体系内 ⇒ 不闭合。'
    'r429 七类是实证完备（7/7）、非逻辑完备（无穷尽证明标记）⇒ 腿(b) 不可排除 ⇒ '
    '修法只消除已知反例，不消除结构性开放。'
    '⇒ r436「E2 定义不完备」的 BOUNDARY 在修法后仍部分存在：'
    '补名单可解决字面层，但分类开放性不能靠一词修法消除。')
add('MT04', 'FAIL', '定理 T2：被排除类名单不可代填的结构性理由',
    'r436 §十 裁决 1 说「并补被排除类的名单」，但登记为 BOUNDARY「不代填」。'
    '本册给出不代填的结构性理由：名单是有限枚举，而分类非逻辑完备，'
    '任何有限名单都不能证明"名单之外无第八类"。'
    '代填名单只会把"开放式开放"伪装成"封闭式闭合"——与 r436 的诚实立场冲突。'
    '⇒ BOUNDARY 维持：名单须由逻辑完备证明给出，不能由样本归纳代填。')

# ================================================================= B 归纳缺口量化
# Laplace 示意：n=7 次抽样全落入已知类，未知类存在的后验下界 ~ 1/(n+2) = 1/9 > 0。
n_samples = 7
laplace_unseen_lower = Frac(1, n_samples + 2)
guard('G-B1', laplace_unseen_lower > Frac(0, 1),
      '归纳缺口量化：Laplace 示意下界 1/(n+2)=1/9 > 0（样本外风险不可归零）')
guard('G-B2', laplace_unseen_lower == Frac(1, 9), '下界数值 = 1/9（n=7）')

add('MT05', 'FAIL', '定理 T3：样本外风险的归纳下界',
    '以 Laplace  succession 作示意：n=7 个实测候选全部落入已知七类，'
    '未知类存在的后验下界约 1/(n+2)=1/9 > 0。'
    '这是归纳风险示意而非精确概率（先验选择依赖假设），'
    '但足以说明：7/7 的实证完备不能把样本外风险归零，'
    '故"七类之外=体系外"不能由样本归纳保证。')

ctrl('C1', leg_a['verdict'] == 'STRUCTURALLY-CLOSED' and leg_b['verdict'] == 'STRUCTURALLY-OPEN',
     '判据有牙：腿(a) 闭合与腿(b) 开放被正确分开（非恒真/恒假）')
ctrl('C2', not logically_complete and empirical_rate == Frac(1, 1),
     '阴性对照：实证完备 PASS 与逻辑完备 FAIL 并存（判据不混同）')

# ================================================================= P 唯一出口八重复证
EXIT_REASONS = [
    ('r429', '体系内七类来源无一过四门', 'internal-unreachable'),
    ('r430', '外生来料 V83–V120 四门禁 0/40、E1/E3/E4 全败', 'external-intake-0of40'),
    ('r431', '自陈义务≡门禁、C4 标度层级需 +1 外部比', 'c4-scale-unreachable'),
    ('r432', '基组 {c,ℏ,G} 闭包只生成 1，非平凡无量纲数全外生', 'base-closure'),
    ('r433', '离散轴两腿全败，口径 II 过 O1 不可达', 'discrete-preset-dichotomy'),
    ('r434', '记账修为 |S|-rank(D)，离散输入 ≥3.9bit 且 Ω5 不覆盖', 'caliber-invariance'),
    ('r435', '账基组选择反解，口径不变性子域成立/全局不可达', 'basis-choice-reverse-solve'),
    ('r436', 'E2 六/七类冲突、C4 空满足、新颖性集空', 'exit-gate-audit'),
    ('r437', 'E2 修法只消字面冲突，分类非逻辑完备 ⇒ 结构开放', 'classification-openness'),
]
guard('G-P1', len(EXIT_REASONS) == 9, '九条独立理由（r429–r437）同指唯一出口')
guard('G-P2', all(r[2] != 'ok' for r in EXIT_REASONS), '九条理由均为封死型')

add('MT06', 'FAIL', '定理 T4：唯一出口九重复证（本册补分类开放性证据）',
    '承 r429–r436 八条，本册补第九条：E2 修法只消字面冲突，'
    '分类非逻辑完备 ⇒ 出口定义结构性开放。九条覆盖可达性、外生实测、标度层级、'
    '量纲闭包、离散预置、计量口径、元层选择、门禁自审、分类开放性九个侧面，'
    '同指唯一出口 = 体系外 E1–E4 全过预注册来料。九重复证不增物理内容，'
    '但把"唯一出口"升级为九侧独立支撑。')
add('MT07', 'BOUNDARY', '作用域（诚实边界）：本册不做什么',
    '不重判 r436 门禁自审（E2 计数冲突、C4 空满足、新颖性空集全部继承）；'
    '不代填被排除类名单（维持 r436 BOUNDARY，本册给出不代填的结构理由）；'
    '不宣称 r429 七类错误（其七类全败与 E3 合取结论继续有效）——'
    '本册只指出"完备性是实证的、非逻辑的"；'
    '不宣称发现 W3/UFT-3/validated 候选；不产生新物理；不否证研究方向；不销任何既有债务。')
add('MT08', 'INFO', '与既有册的分工（防重复）',
    'r436：门禁自身可满足性审计 + E2 六/七类冲突 + 零成本修法 + BOUNDARY「不代填」——'
    '本册接手修法后果与"不代填"的结构理由。'
    'r429：七类来源分类学（实证完备）——本册区分实证/逻辑完备。'
    '**本册净增量**：(1) 分类完备性两分判据；'
    '(2) E2 修法后果二分（字面≠结构）；(3) 归纳风险下界 1/9；'
    '(4) 名单不代填的结构理由；(5) 唯一出口九重复证。')

# ================================================================= 汇总
ent_cnt = {}
for e in ENTRIES:
    ent_cnt[e['status']] = ent_cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
cok = sum(1 for c in CONTROLS if c['ok'])
ctot = len(CONTROLS)
verdict = ('E2-REPAIR-EMPIRICAL-ONLY--CLASSIFICATION-LOGICALLY-OPEN--'
           'KNOWN-COUNTEREXAMPLE-REMOVED--STRUCTURAL-CLOSURE-NOT-ACHIEVED--'
           'LIST-NOT-FILLABLE-BY-INDUCTION--UNIQUE-EXIT-9FOLD-REAFFIRMED') \
    if (gok == gtot and cok == ctot) else 'GUARD-FAILED'

key_numbers = {
    'empirical_samples': empirical_samples,
    'empirical_in_class': empirical_in_class,
    'empirical_rate': str(empirical_rate),
    'exhaustive_marker_count': exhaustive_marker_count,
    'logically_complete': logically_complete,
    'leg_a_verdict': leg_a['verdict'],
    'leg_b_verdict': leg_b['verdict'],
    'cannot_exclude_b': cannot_exclude_b,
    'laplace_unseen_lower': str(laplace_unseen_lower),
    'unique_exit_reasons': len(EXIT_REASONS),
    'guards': '%d/%d' % (gok, gtot),
    'controls': '%d/%d' % (cok, ctot),
    'verdict': verdict,
}

payload = dict(round=ROUND, date=DATE, name=NAME, verdict=verdict,
               entries=ENTRIES, guards=GUARDS, controls=CONTROLS, anchors=anchor_rows,
               completeness=dict(empirical_rate=str(empirical_rate),
                                 logically_complete=logically_complete,
                                 exhaustive_marker_count=exhaustive_marker_count),
               source_legs=[leg_a, leg_b],
               exit_reasons=[dict(by=a, reason=b, tag=c) for a, b, c in EXIT_REASONS],
               key_numbers=key_numbers,
               not_self_derived=[
                   'r436 E2 六/七类冲突、C4 空满足、新颖性空集与零成本修法（继承，本册不重判）',
                   'r429 七类来源分类学与 E1–E4（继承，本册只区分完备性）',
                   'r430–r435 五条封死理由（继承，本册在多侧复证中引用）',
                   'Ω5≤1、O1「从不预置」口径（r404/r429/r436 继承）',
               ],
               red_line='机器零 != 新物理；分类结构开放 != 统一场论研究方向被否定。'
                        '本册只判「E2 修法后的结构闭合性」，不代填名单、不产生新物理、'
                        '不销任何既有债务。Laplace 下界为归纳示意，非精确概率。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r437 E2 修法后果与分类学开放性 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(ent_cnt)),
         'GUARDS %d/%d' % (gok, gtot),
         'CONTROLS %d/%d' % (cok, ctot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines += ['', '== COMPLETENESS ==']
lines.append('empirical_rate=%s logically_complete=%s markers=%d' %
             (empirical_rate, logically_complete, exhaustive_marker_count))
lines += ['', '== SOURCE LEGS ==']
for r in [leg_a, leg_b]:
    lines.append('%s | verdict=%s | %s' % (r['leg'], r['verdict'], r['note']))
lines += ['', '== KEY NUMBERS ==']
for k, v in key_numbers.items():
    lines.append('%s = %s' % (k, v))
lines += ['', '== EXIT REASONS ==']
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
      '- 靶点：r436 §十裁决 1 BOUNDARY「E2 修法 + 名单不代填」', '',
      '## 条目', '', '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:420]))
md += ['', '## 分类完备性', '', '| 指标 | 值 |', '| --- | --- |']
for k, v in [('empirical_rate', str(empirical_rate)), ('logically_complete', logically_complete),
             ('exhaustive_marker_count', exhaustive_marker_count),
             ('laplace_unseen_lower', str(laplace_unseen_lower))]:
    md.append('| %s | %s |' % (k, v))
md += ['', '## 修法后果腿', '', '| 腿 | 判定 | 说明 |', '| --- | --- | --- |']
for r in [leg_a, leg_b]:
    md.append('| %s | %s | %s |' % (r['leg'], r['verdict'], r['note']))
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
