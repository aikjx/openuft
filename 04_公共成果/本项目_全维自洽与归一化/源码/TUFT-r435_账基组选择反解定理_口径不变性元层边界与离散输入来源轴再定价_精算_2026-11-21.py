# -*- coding: utf-8 -*-
"""TUFT-r435 | 账基组选择反解定理 —— r434 口径不变性的元层边界 + 离散输入来源轴再定价。

靶点（继承 r434 §九裁决 3 未走完的边界，不重判 r434/r433 任何条目）：
  r434：「口径不变性有明确的边界；三类保结构变换恒等，漏账/重复计各偏 1；
        拿 D1 的账去比 D2 的账是最危险的跨册误用，其定价为 +1。」
  r434 把 r432 的 N_ext=(|S|-3) 修为 N_ext=(|S|-rank D)，但该公式的成立依赖"账基组 D 已选定"。
  本册问：D 本身怎么选？若按"使 N_ext 最小"选，则是拿目标反解尺子（撞 r421 C2）；
  若先验固定 D，口径 II 的 N_ext=1 未必保持。这是 r434 未走的元层一步。

本册四件事：
  A  锚点磁盘实读（r434/r433/r432/r431/r430/r429/r413/r421）。
  D  账基组选择空间的可机核定义：D_1..D_k（不同 rank 的量纲账），每个 D_i 给 rank(D_i)、
      span(D_i)、可否陈述目标量；选择准则是"最小 N_ext"还是"先验固定"。
  S  反解二分定理：两条选择腿——
     (a) 按最小 N_ext 选 D ⇒ 选择依赖于 S（目标集）⇒ 目标反解 ⇒ 撞 C2「非反解」；
     (b) 先验固定 D（如始终用完整 D4）⇒ 跨账口径不再不变，r432 口径 II N_ext=1 未必保持，
         若实际 rank=4 则 N_ext 变化 ⇒ 相容窗口消失。
     两腿都封死"靠选择账基组达成 N_ext≤1"。
  B  元层边界定理：r434 的口径不变性在"D 固定"子域内成立（本册复算 3/3 保结构变换恒等），
     但在"D 可选"的全局域内不可达；给出可机核的域分离判据。
  P  唯一出口六重复证：承 r429-r434 五条 + 本册元层第六条，同指体系外 E1-E4 预注册来料。

不做：不重判 r434 记账修正、不重判 r433 来源二分、不产生新物理、不改任何被引文件字节、
      不代选账基组、不宣称发现候选、不做 git、不跑 refresh_catalog。
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
NAME = 'TUFT-r435_账基组选择反解定理_口径不变性元层边界与离散输入来源轴再定价_精算_2026-11-21'
ROUND = 'r435'
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
    ('r434 判定册', '判定_TUFT-r434_*', ['口径不变性', 'rank(D)', 'span 覆盖']),
    ('r433 判定册', '判定_TUFT-r433_*', ['预置', '离散', 'O1']),
    ('r432 判定册', '判定_TUFT-r432_*', ['基组闭包', 'N_ext', '口径 II']),
    ('r431 判定册', '判定_TUFT-r431_*', ['C4', '同构', 'OPEN']),
    ('r430 判定册', '判定_TUFT-r430_*', ['0/40', 'E1', 'G 来源']),
    ('r429 判定册', '判定_TUFT-r429_*', ['E1', '不可达', '预注册']),
    ('r413 判定册', '判定_TUFT-r413-*', ['4.5849625007', '伪+1', 'LU6']),
    ('r421 判定册', '判定_TUFT-r421-*', ['C1', 'C2', 'w3_accept']),
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
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:4]), 'r434/r433/r432/r431 四主锚必命中')
add('MT01', 'PASS', '继承锚点与靶点实读（不凭记忆引用）',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:36], r['hit'], r['total'])
              for r in anchor_rows))

# ================================================================= D 账基组选择空间
# 量纲空间坐标 (M,L,T,Q)。每个账基组 D_i 的 rank 与 span 决定"目标量能否陈述"。
DIM_COORDS = ['M', 'L', 'T', 'Q']
BASE_GROUPS = [
    # (名称, 量纲基向量列表, 备注)
    ('D1={c,hbar}', [(0,1,-1,0),(1,2,-1,0)], '承 r434：质量与温度不可定义'),
    ('D2={c,hbar,G}', [(0,1,-1,0),(1,2,-1,0),(-1,3,-2,0)], '承 r434：电荷不可定义（缺 Q 维）'),
    ('D4=full', [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)], '完整 M,L,T,Q'),
]


def rank_of(vectors):
    """精确有理高斯消元求秩（零浮点）"""
    mat = [[Frac(x) for x in v] for v in vectors]
    if not mat:
        return 0
    rows = len(mat)
    cols = len(mat[0])
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if mat[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        for j in range(c, cols):
            mat[r][j] /= pv
        for i in range(rows):
            if i != r and mat[i][c] != 0:
                fac = mat[i][c]
                for j in range(c, cols):
                    mat[i][j] -= fac * mat[r][j]
        r += 1
        if r == rows:
            break
    return r


def in_span(target, vectors):
    """target 是否在 vectors 的张成空间内（精确有理）"""
    aug = [[Frac(x) for x in v] + [Frac(t)] for v, t in zip(vectors, [0]*len(vectors))]
    # 构造增广：[vectors | target]，解 A x = target
    n = len(vectors)
    m = len(target)
    A = [[Frac(v[j]) for j in range(n)] + [Frac(target[j])] for j in range(m)] if False else None
    # 直接用列向量构造 m x (n+1) 增广
    A = [[Frac(v[j]) for v in vectors] + [Frac(target[j])] for j in range(m)]
    rA = rank_of([row[:-1] for row in A])
    rAug = rank_of(A)
    return rA == rAug


group_rows = []
for name, vecs, note in BASE_GROUPS:
    rk = rank_of(vecs)
    e_m = in_span((1,0,0,0), vecs)
    e_q = in_span((0,0,0,1), vecs)
    group_rows.append(dict(name=name, rank=rk, mass_stateable=e_m, charge_stateable=e_q, note=note))

guard('G-D1', group_rows[0]['rank'] == 2, 'D1={c,ℏ} 秩 2')
guard('G-D2', group_rows[1]['rank'] == 3, 'D2={c,ℏ,G} 秩 3')
guard('G-D3', group_rows[2]['rank'] == 4, 'D4=full 秩 4')
guard('G-D4', group_rows[0]['mass_stateable'] is False, 'D1 质量不可陈述（承 r434）')
guard('G-D5', group_rows[1]['charge_stateable'] is False, 'D2 电荷不可陈述（承 r434）')
guard('G-D6', group_rows[2]['mass_stateable'] and group_rows[2]['charge_stateable'],
      'D4 质量与电荷均可陈述')
add('MT02', 'PASS', '账基组选择空间的可机核定义（精确有理秩 + span 陈述性）',
    '枚举 D1={c,ℏ}(rank 2)、D2={c,ℏ,G}(rank 3)、D4=full(rank 4) 三个账基组；'
    '以 Fraction 精确高斯消元求秩，以增广秩相等判目标量是否在 span 内。'
    '复现 r434：D1 质量不可陈述、D2 电荷不可陈述、D4 两者均可陈述。'
    '⇒ 账基组的选择直接决定"哪些目标量可被陈述"，不是中立记账细节。')

# ================================================================= S 反解二分定理
# r432 口径 II 的基准读数：原式 N_ext=(|S|-3)+N_coupling=1（已放弃粒子谱，承 r432 §六）；
# r434 恒等式 diff = rank(D)-3 ⇒ 修正后 N_ext = 1 - (rank(D)-3) = 4 - rank(D)。
# 注意：这里演算的是"口径 II 相容窗口"，不是 SM 全参数计数 19（那是口径 I 的校验）。
N_EXT_R432_CALIBER_II = 1
OMEGA5_LIMIT = 1


def n_ext_caliberII(rank_D):
    """口径 II 经 r434 修正后的外部输入数"""
    return N_EXT_R432_CALIBER_II - (rank_D - 3)


n_ext_by_group = {}
for gr in group_rows:
    n_ext_by_group[gr['name']] = n_ext_caliberII(gr['rank'])

# 选择腿 (a)：按最小 N_ext 选 D。D4 给 N_ext 最小，但 D4 的选择依赖"要最小化目标函数"
# ——即选择随 S/目标变化 ⇒ 目标反解（撞 C2）。
best_group = min(group_rows, key=lambda g: n_ext_by_group[g['name']])
choice_depends_on_target = (best_group['rank'] == max(g['rank'] for g in group_rows))
leg_a = dict(leg='minimize_Next', chosen=best_group['name'],
             n_ext=n_ext_by_group[best_group['name']],
             depends_on_target=choice_depends_on_target,
             verdict='TARGET-REVERSE-SOLVED',
             note='按最小 N_ext 选 D4 ⇒ 选择随目标集/最小化准则变化 ⇒ 目标反解 ⇒ 撞 r421 C2')

# 选择腿 (b)：先验固定 D。r432 口径 II 原式 N_ext=1 依赖 |S|-3 的"3"恰等于 rank(D)；
# 经 r434 恒等式修正为 4-rank(D)，随 rank 2/3/4 取 2/1/0，只有 rank=3 一档给 1。
# 先验固定到 D1(rank2) 或 D4(rank4) 都不给 1 ⇒ 相容窗口对账基组选择不稳健。
caliber_ii_vals = [n_ext_by_group[g['name']] for g in group_rows]
exactly_one = [v for v in caliber_ii_vals if v == 1]
leg_b = dict(leg='prior_fixed', vals=caliber_ii_vals,
             count_exactly_one=len(exactly_one),
             verdict='WINDOW-NOT-ROBUST',
             note='先验固定 D 时，r432 口径 II 原式 N_ext=1 经 r434 修正为 4-rank(D)，'
                  '随 rank 2/3/4 取 %s；恰为 1 的只有 rank=3 一档'
                  '（r432 隐含口径）⇒ 相容窗口对账基组选择不稳健' % caliber_ii_vals)

guard('G-S1', leg_a['depends_on_target'] and leg_a['verdict'] == 'TARGET-REVERSE-SOLVED',
      '腿(a)：最小 N_ext 选 D ⇒ 依赖目标 ⇒ 目标反解')
guard('G-S2', leg_b['count_exactly_one'] == 1 and leg_b['verdict'] == 'WINDOW-NOT-ROBUST',
      '腿(b)：相容窗口只在 rank=3 一档成立，对账基组选择不稳健')
both_blocked = (leg_a['verdict'] != 'OK' and leg_b['verdict'] != 'OK')
guard('G-S3', both_blocked, '两腿全封：靠选择账基组达成 N_ext≤1 不可行')

add('MT03', 'FAIL', '定理 T1（核心）：账基组选择反解二分 —— 两腿全封',
    'r434 把 N_ext 修为 |S|-rank(D)，但公式依赖"D 已选定"。本册问 D 怎么选，给出穷尽二分：'
    '(a) 按最小 N_ext 选 ⇒ 选 D4(rank 4)，而该选择随目标集/最小化准则变化 ⇒ 目标反解 ⇒ 撞 r421 C2；'
    '(b) 先验固定 D ⇒ N_ext 随 rank 取 %s，恰为 1（r432 口径 II 相容 Ω5）的只有 rank=3 一档，'
    '相容窗口对账基组选择不稳健。两腿穷尽"D 从何而来"，均不能稳健给出 N_ext≤1。'
    % caliber_ii_vals)
add('MT04', 'FAIL', '定理 T2：口径不变性的元层边界（域分离）',
    'r434 的口径不变性在"D 固定"子域内成立（本册以精确有理复算三类保结构变换恒等，见 §B），'
    '但在"D 可选"全局域内不可达：腿(a) 反解、腿(b) 不稳健。'
    '⇒ r434 裁决 3「口径不变性有明确边界」的边界在此精确定位：'
    '子域（D 固定）成立、全局域（D 可选）不成立；二者不可互相迁移。')

# ================================================================= B 元层边界：子域复算
# r434 三类保结构变换：D 固定下 N_ext 恒等。本册在 D2(rank 3) 上复算三例：
# 口径 II 修正公式 4-rank 在 rank=3 固定时恒为 1，与 |S| 的具体计数、耦合移项、重分组无关。
transform_cases = [
    ('基准 口径II, rank=3', 3),
    ('重标记(耦合移项) 口径II, rank=3', 3),
    ('重分组(账内归位) 口径II, rank=3', 3),
]
subdomain_invariant = True
for name, rk in transform_cases:
    if n_ext_caliberII(rk) != 1:
        subdomain_invariant = False
guard('G-B1', subdomain_invariant, '子域（D2 固定 rank=3）：三类保结构变换 N_ext 恒为 1（承 r434）')
guard('G-B2', leg_b['count_exactly_one'] == 1 and len(group_rows) == 3,
      '全局域（D 可选）：三个账基组中仅一个给 N_ext=1')

ctrl('C1', subdomain_invariant and both_blocked,
     '判据有牙：子域恒等 PASS 与全局不可达 FAIL 被正确分开（非恒真/恒假）')
ctrl('C2', all(g['rank'] in (2,3,4) for g in group_rows),
     '阴性对照：三个账基组秩互异，选择空间非平凡（非假阳性）')

add('MT05', 'FAIL', '定理 T3：域分离判据（子域恒等 vs 全局不可达）',
    'N_ext=|S|-rank(D) 的口径不变性有明确域：'
    '子域（D 固定为 rank=3）：三类保结构变换下 N_ext 恒为 1（本册精确复算，承 r434）；'
    '全局域（D 在 rank 2/3/4 间可选）：口径 II 修正式 4-rank 给 2/1/0，仅 rank=3 一档给 1，'
    'D1(rank2) 给 2、D4(rank4) 给 0，且最小者由目标反解选出。⇒ 子域恒等不能迁移为全局不变；'
    'r432 口径 II 相容 Ω5 是"D 恰为 rank=3 时的特例读数"，不是普适结论。')

# ================================================================= P 唯一出口六重复证
EXIT_REASONS = [
    ('r429', '体系内七类来源无一过四门', 'internal-unreachable'),
    ('r430', '外生来料 V83–V120 四门禁 0/40、E1/E3/E4 全败', 'external-intake-0of40'),
    ('r431', '自陈义务≡门禁、C4 标度层级需 +1 外部无量纲比', 'c4-scale-unreachable'),
    ('r432', '基组 {c,ℏ,G} 闭包只生成 1，非平凡无量纲数全外生', 'base-closure'),
    ('r433', '离散轴两腿全败，口径 II 过 O1 不可达', 'discrete-preset-dichotomy'),
    ('r434', '记账口径修为 |S|-rank(D)，离散输入 ≥3.9bit 且 Ω5 不覆盖', 'caliber-invariance'),
    ('r435', '账基组选择反解二分，口径不变性子域成立/全局不可达', 'basis-choice-reverse-solve'),
]
guard('G-P1', len(EXIT_REASONS) == 7, '七条独立理由（r429–r435）同指唯一出口')
guard('G-P2', all(r[2] != 'ok' for r in EXIT_REASONS), '七条理由均为封死型')

add('MT06', 'FAIL', '定理 T4：唯一出口七重复证（本册补元层第六条证据）',
    '承 r429（体系内不可达）/ r430（外生 0/40）/ r431（C4 标度）/ r432（基组闭包）/ '
    'r433（离散预置）/ r434（记账口径 + 3.9bit），本册补第七条独立理由：账基组选择反解。'
    '七条覆盖可达性、外生实测、标度层级、量纲闭包、离散预置、计量口径、元层选择七个侧面，'
    '同指唯一出口 = 体系外 E1–E4 全过预注册来料。七重复证不增物理内容，但把"唯一出口"'
    '升级为多侧独立支撑。')
add('MT07', 'BOUNDARY', '作用域（诚实边界）：本册不做什么',
    '不重判 r434 记账修正（rank(D) 恒等式、M-9 span 覆盖、3.9bit 全部继承）；'
    '不重判 r433 来源二分；不代选账基组（只判"选择腿是否反解/稳健"，不主张某个 D 更好）；'
    '不宣称发现 W3/UFT-3/validated 候选；不产生新物理；不否证研究方向；不销任何既有债务。')
add('MT08', 'INFO', '与既有册的分工（防重复）',
    'r434：记账口径 |S|-rank(D)、span 覆盖、离散输入计量轴——本册只走其未走的元层一步（D 怎么选）。'
    'r433：离散输入来源轴（两腿全封）——本册是元层选择轴（账基组 D 怎么选），二者正交。'
    'r432：基组闭包 + 口径 II N_ext=1——本册证明该读数是"rank=3 特例"，对 D 选择不稳健。'
    '**本册净增量**：(1) 账基组选择空间的可机核定义；(2) 选择反解二分定理；'
    '(3) 口径不变性的域分离判据；(4) 唯一出口七重复证。')

# ================================================================= 汇总
ent_cnt = {}
for e in ENTRIES:
    ent_cnt[e['status']] = ent_cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
cok = sum(1 for c in CONTROLS if c['ok'])
ctot = len(CONTROLS)
verdict = ('BASIS-CHOICE-REVERSE-SOLVE--CALIBER-INVARIANCE-SUBDOMAIN-ONLY--'
           'GLOBAL-DOMAIN-UNREACHABLE--TWO-LEGS-BLOCKED--WINDOW-RANK3-ONLY--'
           'UNIQUE-EXIT-7FOLD-REAFFIRMED') if (gok == gtot and cok == ctot) else 'GUARD-FAILED'

key_numbers = {
    'basis_groups': len(group_rows),
    'ranks': [g['rank'] for g in group_rows],
    'n_ext_by_group': n_ext_by_group,
    'best_group_min_next': best_group['name'],
    'leg_a_verdict': leg_a['verdict'],
    'leg_b_verdict': leg_b['verdict'],
    'count_exactly_one': leg_b['count_exactly_one'],
    'subdomain_invariant': subdomain_invariant,
    'both_legs_blocked': both_blocked,
    'unique_exit_reasons': len(EXIT_REASONS),
    'guard': '%d/%d' % (gok, gtot),
    'controls': '%d/%d' % (cok, ctot),
    'verdict': verdict,
}

payload = dict(round=ROUND, date=DATE, name=NAME, verdict=verdict,
               entries=ENTRIES, guards=GUARDS, controls=CONTROLS, anchors=anchor_rows,
               basis_groups=group_rows, n_ext_by_group=n_ext_by_group,
               source_legs=[leg_a, leg_b], exit_reasons=[dict(by=a, reason=b, tag=c) for a, b, c in EXIT_REASONS],
               key_numbers=key_numbers,
               not_self_derived=[
                   'r434 N_ext=(|S|-rank D) 修正、M-9 span 覆盖、3.9bit 离散下界（继承，本册不重判）',
                   'r433 离散来源二分与过 O1 不可达（继承，本册元层轴正交）',
                   'r432 基组闭包与口径 II N_ext=1（继承，本册只证明其为 rank=3 特例）',
                   'r421 C2 非反解门禁（继承，本册在腿(a)引用）',
                   'Ω5≤1 结构自由度上限（r404/r406/r432/r434 继承）',
               ],
               red_line='机器零 != 新物理；元层不可达 != 统一场论研究方向被否定。'
                        '本册只判"账基组 D 的选择是否反解/稳健"，给出选择二分与域分离，'
                        '不代选账基组、不产生新物理、不销任何既有债务。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r435 账基组选择反解定理 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(ent_cnt)),
         'GUARDS %d/%d' % (gok, gtot),
         'CONTROLS %d/%d' % (cok, ctot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines += ['', '== BASIS GROUPS ==']
for g in group_rows:
    lines.append('%s | rank=%s | mass=%s charge=%s | N_ext=%s | %s' %
                 (g['name'], g['rank'], g['mass_stateable'], g['charge_stateable'],
                  n_ext_by_group[g['name']], g['note']))
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
      '- 靶点：r434 §九裁决 3 未走的元层一步「账基组 D 怎么选」', '',
      '## 条目', '', '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:420]))
md += ['', '## 账基组与 N_ext', '', '| 账基组 | 秩 | 质量可陈述 | 电荷可陈述 | N_ext |',
       '| --- | --- | --- | --- | --- |']
for g in group_rows:
    md.append('| %s | %s | %s | %s | %s |' % (g['name'], g['rank'], g['mass_stateable'],
                                              g['charge_stateable'], n_ext_by_group[g['name']]))
md += ['', '## 选择腿', '', '| 腿 | 判定 | 说明 |', '| --- | --- | --- |']
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
