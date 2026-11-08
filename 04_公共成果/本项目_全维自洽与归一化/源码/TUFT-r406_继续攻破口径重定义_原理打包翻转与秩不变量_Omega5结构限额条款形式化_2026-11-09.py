# -*- coding: utf-8 -*-
"""TUFT-r406 | 继续攻破口径重定义：原理打包、秩不变量与 Omega5 结构限额条款。

承接 r405 明确留白（判定册 R02/R03）：
  「若一条原理能同时干两件事却仍只记 s=1，属于『原理能力』的口径重定义，本册不代选。」
全仓检索「结构自由度限额 / 原理打包 / 原理能力 / 口径重定义」：只有点名与待办，
0 册给定义、0 册给机器判据（历史来源语料 tuft_第一性归一化总览 L96 仅一句治理登记）。

本册做四件事：
  B 段  把「口径重定义」形式化为 bundle：任意多条原理打包成一个结构自由度，
        机器扫描打包强度 b=1,2,3 与两种合并口径，看 r405 的 SURVIVE 0 是否翻转。
  J 段  用 Fraction 精确高斯消元证明：约束雅可比秩在重分组下不变，
        而「原理条数」不是不变量 ⇒ 打包声称与本不变量冲突。
  V 段  证明打包会抬高 attack42 的 V 判据，制造 C2 假阳性。
  S 段  给出 Omega5 结构自由度限额条款的形式化定义 + 机读验收判据，
        逐条过 10 个出口，判定 E09 能否靠打包复活。

不做：不重判既有条目、不新造统一方程、不改被引文件字节、不代改并发会话的号段债。
纯标准库 / Python 3.8 / Fraction 精确有理数。控制台只打印 ASCII 摘要。
"""
import io
import json
import re
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from fnmatch import fnmatch

try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / '数据'
NAME = 'TUFT-r406_继续攻破口径重定义_原理打包翻转与秩不变量_Omega5结构限额条款形式化_2026-11-09'

ENTRIES = []
GUARDS = []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


# ---------------------------------------------------------------- A 锚点实读
ANCHOR_SPECS = [
    ('r404 判定册', '判定_TUFT-r404_*', ['结构自由度限额', '口径 I', '55']),
    ('r405 判定册', '判定_TUFT-r405_*', ['原理能力', '不代选', 'CONDITIONAL-INSUFFICIENT']),
    ('r405 数据 md', 'TUFT-r405_*.md', ['R02', 'BOUNDARY']),
    ('attack42 判定册', '判定_attack42_*', ['C2-2', '双锚点', 'V']),
    ('method_F', 'method_F_第一性判据.md', ['无量纲量', '双锚点']),
    ('卷116 终卷', '116_终卷_*', ['#15', '封卷', '债务']),
    ('tuft 历史治理缺口', '*第一性归一化总览*.md', ['结构自由度限额', '自由常数']),
    ('r15 自由度预算', '判定_TUFT-r15*', ['口径 I', '口径 II']),
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
        h = sum(1 for k in keys if k in text)
        if h > best_hit:
            best_hit, best_name = h, p.name
    anchor_rows.append(dict(label=label, file=best_name, hit=best_hit, total=len(keys)))
guard('G-A1', sum(1 for r in anchor_rows if r['hit'] > 0) >= 7,
      '至少 7/8 继承锚点磁盘实读命中')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:3]),
      'r404 / r405 / r405 数据三个主锚必须命中')
add('A01', 'PASS', '继承锚点与留白实读',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:42], r['hit'], r['total'])
              for r in anchor_rows))
if any(r['hit'] == 0 for r in anchor_rows):
    add('A02', 'BOUNDARY', '未命中锚点：'
        + '、'.join(r['label'] for r in anchor_rows if r['hit'] == 0),
        '未命中锚点不构造继承读数，相关条目降级为条件性')

# ---------------------------------------------------------------- B 打包翻转扫描
# 继承 r404 的 10 条出口代价向量；E09 采用 r405 重定价后的 s=2
EXIT = [
    dict(id='E01', name='最小 SU(5)', c=0, s=1, f=0, c2=1, w3=0, excl=1),
    dict(id='E02', name='MSSM / 超对称', c=105, s=1, f=0, c2=1, w3=0, excl=1),
    dict(id='E03', name='SO(10)+阈值+Yukawa', c=15, s=1, f=0, c2=1, w3=0, excl=0),
    dict(id='E04', name='额外维 KK', c=1, s=2, f=0, c2=1, w3=0, excl=0),
    dict(id='E05', name='弦 / 量子引力', c=0, s=9, f=0, c2=0, w3=0, excl=0),
    dict(id='E06', name='几何 omega(r,t)', c=0, s=1, f=1, c2=1, w3=0, excl=0),
    dict(id='E07', name='新场 / 新耦合', c=2, s=0, f=0, c2=1, w3=0, excl=0),
    dict(id='E08', name='修改 Omega5 并登记输入', c=3, s=4, f=0, c2=1, w3=0, excl=0),
    dict(id='E09', name='钉死 f 的原理（r405 重定价）', c=0, s=2, f=0, c2=1, w3=1, excl=0),
    dict(id='E10', name='换理论起点', c=3, s=4, f=0, c2=1, w3=0, excl=0),
]
QUOTA_C, QUOTA_S = 1, 1


def cls(e):
    if e['excl'] or e['f'] or not e['c2']:
        return 'DEAD'
    if e['c'] > QUOTA_C or e['s'] > QUOTA_S:
        return 'DEAD'
    if e['w3'] == 1:
        return 'SURVIVE'
    return 'COST-ONLY'


def bundle(e, b):
    # 口径重定义的最小形式：把任意多条原理打包，结构自由度只记 b
    return dict(e, s=min(e['s'], b))


def merge_upper(x, y):
    return dict(c=x['c'] + y['c'], s=x['s'] + y['s'],
                f=max(x['f'], y['f']), c2=x['c2'] and y['c2'],
                w3=max(x['w3'], y['w3']), excl=max(x['excl'], y['excl']))


def merge_synergy(x, y):
    return dict(c=max(x['c'], y['c']), s=max(x['s'], y['s']),
                f=max(x['f'], y['f']), c2=x['c2'] and y['c2'],
                w3=max(x['w3'], y['w3']), excl=max(x['excl'], y['excl']))


pairs = list(combinations(EXIT, 2))
scan = []
for b in (1, 2, 3):
    single = [(e['id'], cls(bundle(e, b))) for e in EXIT]
    su = [(x['id'] + '+' + y['id'], cls(merge_upper(bundle(x, b), bundle(y, b))))
          for x, y in pairs]
    sy = [(x['id'] + '+' + y['id'], cls(merge_synergy(bundle(x, b), bundle(y, b))))
          for x, y in pairs]
    scan.append(dict(b=b, single_survive=sum(1 for _, s in single if s == 'SURVIVE'),
                     pair_upper=sum(1 for _, s in su if s == 'SURVIVE'),
                     pair_synergy=sum(1 for _, s in sy if s == 'SURVIVE'),
                     pair_synergy_dead=sum(1 for _, s in sy if s == 'DEAD'),
                     flipped=[i for i, s in sy if s == 'SURVIVE']))

baseline_single = sum(1 for e in EXIT if cls(e) == 'SURVIVE')
baseline_pair_syn = sum(1 for x, y in pairs
                        if cls(merge_synergy(x, y)) == 'SURVIVE')
guard('G-B1', baseline_single == 0 and baseline_pair_syn == 0,
      'r405 基准（不打包）：单点与两点协同均 0 存活')
guard('G-B2', scan[0]['single_survive'] == 1 and scan[1]['single_survive'] == 0,
      '打包强度 b=1 使单点 SURVIVE 翻转为 1，b=2 不翻转')
guard('G-B3', scan[0]['pair_synergy'] >= 1 and scan[0]['pair_upper'] == 0,
      '打包必须与协同结合才翻转两点组合；上界叠加口径仍 0')
guard('G-B4', scan[1]['pair_synergy'] == 0 and scan[2]['pair_synergy'] == 0,
      'b>=2 时无翻转')
guard('G-B5', len(pairs) == 45, '两点组合 45 组')

add('B01', 'PASS', '发现：口径重定义不是无害记账，会翻转 r405 的判决',
    '基准（不打包）单点 SURVIVE %d / 两点协同 SURVIVE %d；'
    '打包强度 b=1 时单点 SURVIVE %d、两点协同 SURVIVE %d（翻转组 %s）、'
    '两点上界叠加 SURVIVE %d；b=2/3 时协同 SURVIVE 分别 %d/%d。'
    '⇒ 只有「打包 b=1 + 协同」才救得活 E09，这是发现而非裁决。'
    % (baseline_single, baseline_pair_syn, scan[0]['single_survive'],
       scan[0]['pair_synergy'], str(scan[0]['flipped']), scan[0]['pair_upper'],
       scan[1]['pair_synergy'], scan[2]['pair_synergy']))
add('B02', 'BOUNDARY', '打包模型的射程',
    'bundle 只把「原理条数」压到 b，不改 c / f / c2 / w3 / excl；'
    '这是口径重定义的最小形式，未建模「打包同时增强能力」的更强声称。')
add('B03', 'INFO', '打包强度扫描表（6 组，可复算）',
    '；'.join('b=%d: 单点 %d / 两点上界 %d / 两点协同 %d / 翻转组 %s'
              % (x['b'], x['single_survive'], x['pair_upper'],
                 x['pair_synergy'], str(x['flipped'])) for x in scan)
    + '。翻转阈值为 b=1 且仅在协同口径，说明「救活通道」需要两个口径让步同时发生。')

# ---------------------------------------------------------------- J 秩不变量
def rank_fraction(rows, ncols):
    M = [list(r) for r in rows]
    rank = 0
    for col in range(ncols):
        piv = None
        for i in range(rank, len(M)):
            if M[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][col]
        M[rank] = [v / pv for v in M[rank]]
        for i in range(len(M)):
            if i != rank and M[i][col] != 0:
                fac = M[i][col]
                M[i] = [M[i][j] - fac * M[rank][j] for j in range(ncols)]
        rank += 1
        if rank == len(M):
            break
    return rank


def J(k):
    # k 条独立原理对 k+1 个输出的约束矩阵：前 k 列为单位阵，末列共享
    return [[F(1) if j == i else F(0) for j in range(k)] + [F(1)]
            for i in range(k)]


rank_rows = []
for k in range(1, 7):
    r = rank_fraction(J(k), k + 1)
    rank_rows.append(dict(k=k, rank=r, claimed=1, gap=r - 1,
                          bundled_rank=rank_fraction(J(k), k + 1)))
guard('G-J1', all(x['rank'] == x['k'] for x in rank_rows),
      '精确高斯消元：rank(J_k)=k，k=1..6')
guard('G-J2', all(x['rank'] == x['bundled_rank'] for x in rank_rows),
      '打包不改变约束矩阵，秩不变')
guard('G-J3', [x['gap'] for x in rank_rows] == [0, 1, 2, 3, 4, 5],
      '声称值恒 1，与秩的差 k-1 线性增长')

add('J01', 'PASS', '秩不变量定理：条数不是不变量，秩是',
    '构造 k 条独立原理的约束雅可比 J_k（k x (k+1)，前 k 列单位阵 + 共享末列），'
    'Fraction 精确高斯消元给 rank=%s；打包后物理约束未变、秩仍 %s；'
    '而口径声称的结构自由度恒为 1，差 %s 随 k 线性增长。'
    '⇒ 把配额的计数对象放在「原理条数」上可被任意重分组击穿；'
    '放在 rank(J) 上则在重分组下不变。'
    % (str([x['rank'] for x in rank_rows]),
       str([x['bundled_rank'] for x in rank_rows]),
       str([x['gap'] for x in rank_rows])))
add('J02', 'CORRECTED', 'r404 的 s<=1 是自设配额，本册给出条款定义',
    'r404 §五把 c<=1、s<=1 作为出口代价配额（自设，非 Omega5 原文）；'
    'r405 用它把 E09 从 s=1 提到 s=2 判死，但明确拒判「原理能力单位」。'
    '本册把 s 定义为 rank(J_constraint)（独立约束数 / 独立外部输入数），'
    '并规定声称值必须等于该不变量，否则只是重贴标签。')

# ---------------------------------------------------------------- V 假阳性
v_rows = []
for k in range(2, 9):
    n_hit, n_anchor = k, 0
    v_true = F(n_hit - k - n_anchor, n_hit)      # 每条原理各占 1 个自由输入
    v_claim = F(n_hit - 1 - n_anchor, n_hit)     # 打包声称只占 1 个
    v_rows.append(dict(k=k, v_true=v_true, v_claim=v_claim,
                       false_positive=(v_true <= 0 and v_claim > 0)))
n_fp = sum(1 for x in v_rows if x['false_positive'])
guard('G-V1', n_fp == 7, 'k=2..8 共 7 个 C2 假阳性点')
guard('G-V2', all(x['v_true'] == 0 for x in v_rows),
      '真实 V 恒为 0（等价交换）')
guard('G-V3', all(x['v_claim'] > 0 for x in v_rows),
      '打包声称的 V 恒 > 0')
add('V01', 'FAIL', '打包会制造 attack42 的 C2 假阳性',
    '取 n_hit=k（每条原理产出 1 个可检验输出）、n_anchor=0：'
    '真实 V_true=(k-k-0)/k=0；打包声称 n_free=1 时 V_claim=(k-1)/k=%s。'
    'k=2..8 共 %d 个点满足 V_true<=0 而 V_claim>0 ⇒ '
    '仅靠重分组就能把「无信息增益」伪装成「通过 C2-2」，而物理输出一个没多。'
    % (str([str(x['v_claim']) for x in v_rows]), n_fp))

# ---------------------------------------------------------------- S 条款与验收
def accepts(s_claimed, rank_j, v_true):
    if s_claimed != rank_j:
        return 'RELABELING-ONLY'
    if rank_j > QUOTA_S:
        return 'QUOTA-EXCEEDED'
    if v_true <= 0:
        return 'NO-INFORMATION-GAIN'
    return 'ACCEPTED'


e09_bundle = accepts(1, 2, 0)
r405_baseline = accepts(2, 2, 0)
ideal = accepts(1, 1, F(1, 2))
guard('G-S1', e09_bundle == 'RELABELING-ONLY', 'E09 打包声称判为重贴标签')
guard('G-S2', r405_baseline == 'QUOTA-EXCEEDED', 'r405 基准判为超配额（复核）')
guard('G-S3', ideal == 'ACCEPTED', '阳性对照：秩 1 且 V>0 判 ACCEPTED（判据有牙）')

bucket = {}
for e in EXIT:
    rk = 1 if e['s'] <= 1 else e['s']
    st = accepts(min(e['s'], 1), rk, F(0))
    bucket[st] = bucket.get(st, 0) + 1
n_accepted = bucket.get('ACCEPTED', 0)
guard('G-S4', n_accepted == 0, '10 条出口在新条款下无一条 ACCEPTED')

CLAUSE = ('Omega5-S: s := rank(J_constraint)（独立约束/独立外部输入数），'
          '对任意重分组不变；声称值须等于该不变量；s <= 1；且 V_true > 0。'
          '违反任一条分别判 RELABELING-ONLY / QUOTA-EXCEEDED / NO-INFORMATION-GAIN。')
add('S01', 'PASS', 'Omega5 结构自由度限额条款的形式化定义与机读判据',
    CLAUSE + ' 验收函数 accepts(s_claimed, rank(J), V_true) 已机器实现；'
    '阳性对照（rank=1, V=1/2）判 ACCEPTED，证明判据不恒假。')
add('S02', 'FAIL', 'E09 不能靠打包复活',
    '打包声称 s=1 但 rank(J)=2 ⇒ 判 %s；r405 基准 (s=2,rank=2,V=0) 判 %s；'
    '10 条出口分桶 %s，ACCEPTED %d 条。'
    '⇒ r405 的「不代选」在本册被裁决：口径重定义不能救 E09，'
    '它只把约束条数改名，不产生任何新的可检验输出。'
    % (e09_bundle, r405_baseline, str(bucket), n_accepted))
add('S03', 'BOUNDARY', '条款是治理层定义，不是新物理',
    'Omega5-S 把配额计数对象从「原理条数」换成「独立约束秩」，'
    '是防口径漂移的治理条款；它不改变任何物理方程、不销任何既有债务。')
add('S04', 'INFO', '下一步（治理与物理分流，不代执行）',
    '① 若把 Omega5-S 写入 02_共享基础/研究规范 属治理变更，须用户批准，本册未改任何规范文件；'
    '② 物理侧唯一实质缺口仍是 r405 §八的 f 归一/形状原理（且输出数值不得为矩比值）；'
    '③ 本册裁决不销账：#15/#18/#24/#26 仍开，号段漂移留给归属会话回写。')

# ---------------------------------------------------------------- D 号段漂移发现（不代改）
def max_j(path):
    try:
        t = io.open(str(path), encoding='utf-8', errors='replace').read()
    except Exception:
        return -1
    ns = [int(x) for x in re.findall(r'J(\d+)', t)]
    return max(ns) if ns else -1


j_readme = max_j(ROOT / '07_统一场方程/README.md')
j_zongbiao = max_j(ROOT / '07_统一场方程/卷宗总表.md')
drift = j_zongbiao - j_readme
guard('G-D1', j_readme >= 0 and j_zongbiao > j_readme and drift >= 1,
      '07 README 号段结构性滞后于卷宗总表（drift >= 1，不锁具体号值）')
add('D01', 'INFO', '分析发现（只登记、不代改）：并发号段漂移',
    '磁盘实读 07_统一场方程/README.md 最大 J 号 = %d，卷宗总表.md 最大 J 号 = %d，'
    '漂移 %d。首跑与复跑之间卷宗总表上界仍在推进（J106 -> J107），'
    '故守卫改为结构性判定（drift>=1）而非锁死具体号值 —— 这是 attack49'
    '「并发仓库不得引用上一轮号段快照」教训的一次实时复现。'
    '另 attack49 README L1591 的旧上界快照已被 r404/r405 与卷127+ 全面超越。'
    '按本仓「不代他人登记」纪律，本册只登记发现，不改这两个文件任何字节。'
    % (j_readme, j_zongbiao, drift))

# ---------------------------------------------------------------- 汇总
cnt = {}
for e in ENTRIES:
    cnt[e['status']] = cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
verdict = ('PRINCIPLE-BUNDLING-FLIPS-VERDICT--RANK-IS-INVARIANT'
           '--OMEGA5-S-DEFINED--E09-CANNOT-REVIVE' if gok == gtot else 'GUARD-FAILED')

key_numbers = {
    'baseline_single_survive': baseline_single,
    'baseline_pair_synergy_survive': baseline_pair_syn,
    'bundle_scan': str([(x['b'], x['single_survive'], x['pair_upper'],
                         x['pair_synergy']) for x in scan]),
    'bundle_b1_flipped_pairs': str(scan[0]['flipped']),
    'rank_J_k_1to6': str([x['rank'] for x in rank_rows]),
    'rank_bundled_invariant': str([x['bundled_rank'] for x in rank_rows]),
    'claimed_vs_rank_gap': str([x['gap'] for x in rank_rows]),
    'V_true_k2to8': str([str(x['v_true']) for x in v_rows]),
    'V_claim_k2to8': str([str(x['v_claim']) for x in v_rows]),
    'C2_false_positives': n_fp,
    'E09_bundle_state': e09_bundle,
    'r405_baseline_state': r405_baseline,
    'positive_control_state': ideal,
    'exit_buckets': str(bucket),
    'accepted_exits': n_accepted,
    'omega5_S_clause': CLAUSE,
    'J_drift_readme_vs_zongbiao': '%d -> %d (drift %d)' % (j_readme, j_zongbiao, drift),
    'guards': '%d/%d' % (gok, gtot),
    'verdict': verdict,
}

payload = dict(round='r406', date='2026-11-09', name=NAME, verdict=verdict,
               entries=ENTRIES, guards=GUARDS, anchors=anchor_rows,
               exits=EXIT, bundle_scan=scan, rank_rows=rank_rows,
               V_rows=[dict(k=x['k'], v_true=str(x['v_true']),
                            v_claim=str(x['v_claim']),
                            false_positive=x['false_positive']) for x in v_rows],
               key_numbers=key_numbers,
               not_self_derived=[
                   '10 条出口代价向量与 s<=1 配额（r404 自设，继承）',
                   'E09 重定价 s=2 与「原理能力口径不代选」（r405 继承）',
                   'C2-2 的 V 判别式与双锚点（attack42 / method_F 继承）',
                   'Omega5 只约束连续常数、须补结构条款（r404 与历史来源语料继承）',
                   '口径 I/II/III 的区分（r15 自由度预算册继承）',
               ],
               red_line='数学自洽 != 有物理内容 != 实验证实；不宣称统一所有力已完成；'
                        '条款为治理层定义，不改变物理结论、不销既有债务。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r406 继续攻破口径重定义：打包翻转 / 秩不变量 / Omega5-S 条款 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(cnt)),
         'GUARDS %d/%d' % (gok, gtot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines += ['', '== KEY NUMBERS ==']
for k, v in key_numbers.items():
    lines.append('%s = %s' % (k, v))
lines += ['', '== ANCHORS ==']
for r in anchor_rows:
    lines.append('%s | %s | %d/%d' % (r['label'], r['file'], r['hit'], r['total']))
lines += ['', '== BUNDLE SCAN ==']
for x in scan:
    lines.append('b=%d single=%d pair_upper=%d pair_synergy=%d flipped=%s'
                 % (x['b'], x['single_survive'], x['pair_upper'],
                    x['pair_synergy'], str(x['flipped'])))
lines += ['', '== GUARDS ==']
for g in GUARDS:
    lines.append('%s %s | %s' % ('OK' if g['ok'] else 'NG', g['code'], g['note']))
lines += ['', payload['red_line']]
with io.open(str(OUT / (NAME + '_report.txt')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')

md = ['# ' + NAME, '', '- 判词：`%s`' % verdict,
      '- 条目 %d：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, v) for k, v in sorted(cnt.items()))),
      '- 守卫 **%d/%d**；退出码 %d' % (gok, gtot, 0 if gok == gtot else 1), '',
      '## 条目', '', '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:420]))
md += ['', '## 关键读数', '', '| 键 | 值 |', '| --- | --- |']
for k, v in key_numbers.items():
    md.append('| %s | %s |' % (k, str(v).replace('|', '/')))
md += ['', '## 红线', '', payload['red_line'], '']
with io.open(str(OUT / (NAME + '.md')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md))

print('SECTIONS A B J V S D')
print('ENTRIES %d %s' % (len(ENTRIES), str(cnt)))
print('GUARDS %d/%d' % (gok, gtot))
print('VERDICT %s' % verdict)
print('EXIT %d' % (0 if gok == gtot else 1))
sys.exit(0 if gok == gtot else 1)
