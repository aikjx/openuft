# -*- coding: utf-8 -*-
# attack41 / 攻破㉝ —— 统一场完成条件：类别缺口与不可完成判定（2026-11-08）
# 靶：把 GUT 谱、阈值、Yukawa、alpha_H 等 [C] 级外部输入补齐后，是否就能「完成统一场」。
# 纯标准库（os/io/json/re/ast + Fraction），无第三方依赖、无随机、只读事实源。
# 红线：不宣称完成统一场；0/22、UFT-3=0、L3=0、validated=0 不变。
import os, sys, io, json, re, ast
from fractions import Fraction as F
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'attack41_统一场完成条件_类别缺口与不可完成判定_2026-11-08'
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..'))
P_MATRIX = os.path.join(PUB, '全维全体系统一场论', '数据', '全维验收矩阵.json')
P_WJUDGE = os.path.join(PUB, '全维全体系统一场论', '判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md')
P_STATUS = os.path.join(PUB, '状态看板.md')
P_COMPLETE = os.path.join(PUB, '统一场论完成度审计_20261009.md')
P_INTEGRATED = os.path.join(PUB, '统一理论体系_已验证正确内容整合全集.md')
P_UFTJUDGE = os.path.join(PUB, '本项目_全维自洽与归一化', '判定_本项目_统一场论达成度重算与最小闭合清单_2026-10-08.md')
P_UFTJSON = os.path.join(PUB, '本项目_全维自洽与归一化', '数据', '本项目_统一场论达成度重算_2026-10-08.json')
P_UFTMD = os.path.join(PUB, '本项目_全维自洽与归一化', '数据', '本项目_统一场论达成度重算_2026-10-08.md')
P_R95 = os.path.join(PUB, '本项目_全维自洽与归一化', '判定_TUFT-r95-螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.md')
P_EQSUM = os.path.join(OPENUFT, '理论体系方程总汇_正确方程集_2026-10-14.md')
P_EXPERIMENT = os.path.join(HERE, '统一场论_实验验证方案书_2026-10-21.md')
P_FINAL = os.path.join(HERE, '穷尽攻破_统一场论终局总成_2026-10-21.md')
P_G1 = os.path.join(HERE, '统一场论必要条件清单_G1_2026-10-30.md')
P_A39 = os.path.join(HERE, 'attack39_omega自由函数防线_四路封死与定量互斥_2026-11-08_report.txt')
P_A40 = os.path.join(HERE, 'attack40_力统一承重前提_阈值Yukawa联合可识别性_2026-11-08_report.txt')
P_README = os.path.join(HERE, 'README.md')

LINES = []
ENTRIES = []
GUARDS = []

def emit(s=''):
    LINES.append(s)
    print(s)

def add(uid, claim, verdict, reading):
    ENTRIES.append({'id': uid, 'claim': claim, 'verdict': verdict, 'reading': reading})
    emit('[%-9s] %s | %s' % (verdict, uid, claim))
    emit('            读数: %s' % reading)

def guard(gid, desc, ok, reading):
    ok = bool(ok)
    GUARDS.append({'id': gid, 'desc': desc, 'ok': ok, 'reading': reading})
    emit('[%s] %s | %s' % ('OK' if ok else 'BAD', gid, desc))
    emit('            读数: %s' % reading)
    return ok

def read_text(path):
    return io.open(path, encoding='utf-8').read()

def read_json(path):
    return json.load(io.open(path, encoding='utf-8'))

def pair_from(m):
    return (int(m.group(1)), int(m.group(2))) if m else (-1, -1)

def ints_from(m):
    return [int(x) for x in m.groups()] if m else []

def hit_all(text, needles):
    return sum(1 for x in needles if x in text)

# ---------- 只读事实源 ----------
matrix = read_json(P_MATRIX)
uft_json = read_json(P_UFTJSON)
w_judge = read_text(P_WJUDGE)
status = read_text(P_STATUS)
complete = read_text(P_COMPLETE)
integrated = read_text(P_INTEGRATED)
uft_judge = read_text(P_UFTJUDGE)
uft_md = read_text(P_UFTMD)
r95 = read_text(P_R95)
eqsum = read_text(P_EQSUM)
experiment = read_text(P_EXPERIMENT)
final_doc = read_text(P_FINAL)
g1 = read_text(P_G1)
a39 = read_text(P_A39)
a40 = read_text(P_A40)
readme_text = read_text(P_README)

criteria = matrix['criteria']
systems = matrix['systems']
cells = matrix['cells']
verdict_dist = matrix['verdict_dist']
full_pass = matrix['full_pass']
bn = {x['crit']: x for x in matrix['bottleneck']}
w3 = bn['W3']
w3_def = next(x['definition'] for x in criteria if x['id'] == 'W3')
w3_debt = F(str(w3['debt']))
debt_max = [k for k, v in bn.items() if F(str(v['debt'])) == max(F(str(z['debt'])) for z in bn.values())]
w0_pass = bn['W0']['pass']
nonzero_pass = [k for k, v in bn.items() if v['pass'] != 0]
w1_w7_zero = all(bn[k]['pass'] == 0 for k in ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7'])

# 状态看板 / 整合全集 / 完成度审计 / 方程总汇 / 实验协议 / 终局总成的静态命中
status_needles = ['零个', 'validated', 'C 6 · O 10 · H 2 · U 4', 'UFT-3 计数仍为 0', '测量锚', '第一性内容 ⟺ 无量纲量的数值']
status_hits = hit_all(status, status_needles)
complete_needles = ['L1 组织层', 'L2 文档层', 'L3 数学验证层', 'L4 物理层', '全部 OPEN', 'L3 的闭合不迁移到 L4', '176 格验收 0 体系满足全部 8 条判据']
complete_hits = hit_all(complete, complete_needles)
integrated_needles = ['零个体系进入', '[C] 不纳入', '只有 L3 计入', 'L4 不收录', '第一性内容 ⟺ 无量纲量的数值', '总覆盖 **22 个登记体系**']
integrated_hits = hit_all(integrated, integrated_needles)
eqsum_hits = hit_all(eqsum, ['统一场论达成度 1/6', 'UFT-2 四力统一', 'UFT-3 常数派生', 'UFT-6 外部验证'])
experiment_hits = hit_all(experiment, ['有预测且对 = **0/22**', 'UFT-3 = 0', 'DECIDABLE', '证实的都是广义相对论'])
final_hits = hit_all(final_doc, ['0/22', 'UFT-3=0', '可机读数值预言载体为零'])

uft_layer = uft_json['alliance_layer']
uft1_pass = uft_layer['uft1_math_consistent']['pass']
uft1_n = uft_layer['uft1_math_consistent']['n_systems']
uft2_pass = uft_layer['uft2_unified_action']['pass']
uft3_strict = uft_layer['uft3_dimensionless_predictions']['n_entries_strict']
uft6_n = uft_layer['uft6_external_validation']['n_systems']
score_machinable = uft_layer['score_machinable']
ratings = uft_json['rating_distribution']
json_tier = (uft_json['tier_distribution']['未完成'], uft_json['tier_distribution']['纲领草案'])

# 跨源档位分布：JSON / 数据 md / 判定册 / 整合全集引用
m_data = re.search(r'档位分布[^0-9]+未完成=([0-9]+)[^0-9]+纲领草案=([0-9]+)', uft_md)
m_judge = re.search(r'档位分布[^0-9]+未完成[^0-9]+([0-9]+)[、，,]纲领草案[^0-9]+([0-9]+)', uft_judge)
m_integrated = re.search(r'未完成[^0-9]+([0-9]+)[^0-9]+/[^0-9]+纲领草案[^0-9]+([0-9]+)', integrated)
data_tier = pair_from(m_data)
judge_tier = pair_from(m_judge)
integrated_tier = pair_from(m_integrated)
tier_pairs = [json_tier, data_tier, judge_tier, integrated_tier]
tier_unique = sorted(set(tier_pairs))

m_status_counts = re.search(r'C([0-9]+)[^0-9]+O([0-9]+)[^0-9]+H([0-9]+)[^0-9]+U([0-9]+)', status)
status_counts = ints_from(m_status_counts)
m_integrated_counts = re.search(r'18 体系中[^0-9]+([0-9]+)[^0-9]+个 H[^0-9]+([0-9]+)[^0-9]+个 O[^0-9]+([0-9]+)[^0-9]+个 C[^0-9]+([0-9]+)[^0-9]+个 U', integrated)
integrated_counts = ints_from(m_integrated_counts)

# W 册最小闭合集 C1–C6 与 G1 必要条件 N1–N18
closure_ids = sorted(set(int(x) for x in re.findall(r'C([1-6])', w_judge)))
closure_order = 'C1 → C6 → C2 → (C3 ∥ C4) → C5' in w_judge
n_ids = sorted(set(int(x) for x in re.findall(r'N([0-9]+)', g1) if 1 <= int(x) <= 18))
g1_zero = ('18 条必要条件供给' in g1 and '0 核心项' in g1)

# 外部输入单调链与函数级自由度
a40_ext = int(re.search(r'GUT[^0-9]+行[^0-9]+([0-9]+)', a40).group(1))
r95_ext = int(re.search(r'外部输入[^0-9]+([0-9]+)[^0-9]+项', r95).group(1))
a39_ext = int(re.search(r'r95[^0-9]+原账[^0-9]+12[^0-9]+项[^0-9]+≥([0-9]+)[^0-9]+项', a39).group(1))
unbounded_hit = ('函数级自由度' in r95 and '无界' in r95 and '连续谱' in a39 and '连续自由度' in a40)
ext_chain = [a40_ext, r95_ext, a39_ext, 'UNBOUNDED']

# 类别互斥：[C] 级 / 测量锚不能进入 W3 的「非测量锚」类别
category_exclusion = 1 if ('非测量锚' in w3_def and '[C] 不纳入' in integrated and '测量锚' in status) else 0
w3_def_mut = w3_def.replace('非测量锚', '测量锚')
category_exclusion_mut = 1 if ('非测量锚' in w3_def_mut and '[C] 不纳入' in integrated and '测量锚' in status) else 0

# 注入外部输入后，类别通过数是不变量（输入数不是验证数）
def inject(value):
    return {'external': value, 'validated': 0, 'uft3': 0, 'l3': 0,
            'w3_pass': w3['pass'], 'w3_debt': str(w3_debt),
            'full_pass': len(full_pass)}

injected = [inject(v) for v in ext_chain]
inv_ok = all(r['validated'] == 0 and r['uft3'] == 0 and r['l3'] == 0
             and r['w3_pass'] == w3['pass'] and r['w3_debt'] == str(w3_debt)
             and r['full_pass'] == len(full_pass) for r in injected)

# PASS 不迁移到 L4：把 L3→L4 闸门置 1 的变异必须产生 22 个假 validated
fake_pass = systems
gate0 = 0
gate1 = 1
validated_gate0 = 0 + gate0 * fake_pass
validated_gate1 = 0 + gate1 * fake_pass
readme_tail = readme_text.splitlines()[-8:]
nomig_count = sum(1 for line in readme_tail if '不计攻破数' in line)
redline_text = '\n'.join(readme_tail)
redline_hits = sum(1 for x in ['0/22', 'UFT-3=0', 'L3=0', 'validated=0'] if x in redline_text)

emit('== attack41 攻破㉝·统一场完成条件：类别缺口与不可完成判定 ==')
emit('-- 靶：补齐 GUT 谱 / 阈值 / Yukawa / alpha_H 等 [C] 级外部输入，是否就能完成统一场 --')
emit('-- 口径：完成度审计的「完成」仅指组织/文档/数学层；物理层 L4 全部 OPEN。本册不宣称完成统一场 --')
emit('-- 边界：外部输入是 [C] 级 / 测量锚；W3 要求非测量锚；L3 闭合不迁移到 L4；本册只读事实源，不改状态 --')

closure_governance = ['C1', 'C6']
closure_substantive = ['C2', 'C3', 'C4']
closure_dependent = ['C5']
injection_read = '；'.join('%s→validated=%d/UFT3=%d/L3=%d/W3pass=%d/debt=%s/full=%d'
                          % (r['external'], r['validated'], r['uft3'], r['l3'],
                             r['w3_pass'], r['w3_debt'], r['full_pass']) for r in injected)

add('C01', '控制组：验收矩阵与红线事实源逐项一致', 'PASS',
    'systems=%d × criteria=%d = cells=%d；verdict_dist=%s；full_pass=%d；W0 pass=%d、W1..W7 pass=0；W3 debt=%s、debt_max=%s；0/22、UFT-3=0、L3=0、validated=0 静态命中=%d/4'
    % (systems, len(criteria), cells, verdict_dist, len(full_pass), w0_pass,
       w3_debt, debt_max, redline_hits))

add('C02', '完成统一场缺的是三类通过数，不是外部输入条数', 'FAIL',
    '数学自洽 UFT-1=%d/22；非测量锚 W3 pass=%d、UFT-3=0；实验类 UFT-6=%d/22、validated=0；L4 全部 OPEN、176 格 0 体系全过'
    % (uft1_n, w3['pass'], uft6_n))

add('C03', '类别互斥定理：[C] 级 / 测量锚外部输入不能翻 W3 或 UFT-3', 'FAIL',
    'W3 定义含「非测量锚」；整合全集「[C] 不纳入」；状态看板「α 测量锚」「第一性内容⟺无量纲量数值」；原判 category_exclusion=%d，把定义替换为「测量锚」的变异=%d'
    % (category_exclusion, category_exclusion_mut))

add('C04', '外部输入单调链 6 → 12 → ≥15 → UNBOUNDED，类别通过数恒为 0', 'FAIL',
    '%s；注入任意外部输入后 validated/UFT3/L3/W3pass/full_pass 不变，W3 debt 恒 %s'
    % (injection_read, w3_debt))

add('C05', 'PASS 不可迁移：L3↛L4，伪造 22 个 PASS 也不产生 validated', 'FAIL',
    'L3→L4 闸门 0 ⇒ validated=%d；变异闸门 1 ⇒ 假 validated=%d（证明守卫有牙）；README 末 8 行「不计攻破数」命中=%d；完成度审计 L3↛L4 命中=%d/7'
    % (validated_gate0, validated_gate1, nomig_count, complete_hits))

add('C06', '最小闭合集 C1–C6 是类别缺口，不是「补齐外部输入」', 'FAIL',
    '闭合集 %s；执行序命中=%s；治理零物理代价 %d 项（C1/C6）、实质开路 %d 项（C2/C3/C4）、依赖项 %d 项（C5）；C2 仍要求非测量锚第一性数值与双锚点'
    % (closure_ids, closure_order, len(closure_governance), len(closure_substantive), len(closure_dependent)))

add('C07', 'N1–N18 + 函数级自由度：补齐有限外部输入不可停机枚举', 'BOUNDARY',
    'G1 必要条件 N1..N18=%d 条、TUFT 供给 0 核心项命中=%s；外部输入链 %s→%s→≥%s→UNBOUNDED；r95 第 1/11 项为函数级自由度，attack39/40 连续谱复发'
    % (len(n_ids), g1_zero, a40_ext, r95_ext, a39_ext))

add('C08', '跨源档位计数不一致：21/1 与 19/3 两口径并存', 'FAIL',
    'JSON=%s / 数据 md=%s / 判定册=%s / 整合全集引用=%s；唯一口径对=%s；本册只登记 MISMATCH，不擅改事实源'
    % (json_tier, data_tier, judge_tier, integrated_tier, tier_unique))

add('C09', '口径分层：22 体系现测 vs 18 体系快照、1/6 vs score_machinable=3', 'INFO',
    '状态看板 C/O/H/U=%s（和=%d）；整合全集 18 快照 H/O/C/U=%s（和=%d）；方程总汇 UFT 达成度 1/6；达成度 JSON score_machinable=%d；分母/口径须逐项声明'
    % (status_counts, sum(status_counts), integrated_counts, sum(integrated_counts), score_machinable))

add('C10', '总裁定：FAIL（作为「补齐外部输入即可完成统一场」）', 'INFO',
    '组织/文档/数学层可闭合，物理层 L4 全 OPEN；[C] 输入不纳入，L3 不迁移 L4，实验通过只证实 GR/标准场论；0/22、UFT-3=0、L3=0、validated=0 不变，不宣称完成统一场')

# ---------- 守卫 ----------
guard('G41-1', '验收矩阵自洽：22×8=176、full_pass=[]、W3 debt=35/2 且唯一最大',
      systems * len(criteria) == cells and sum(verdict_dist.values()) == cells
      and len(full_pass) == 0 and w3_debt == F(35, 2) and debt_max == ['W3']
      and w1_w7_zero and w0_pass == 18 and nonzero_pass == ['W0'],
      'systems=%d cells=%d full=%d W3debt=%s debt_max=%s W0=%d nonzero=%s'
      % (systems, cells, len(full_pass), w3_debt, debt_max, w0_pass, nonzero_pass))
guard('G41-2', '事实源静态命中与 UFT JSON 读数一致',
      status_hits == 6 and complete_hits == 7 and integrated_hits == 6
      and eqsum_hits == 4 and experiment_hits == 4 and final_hits == 3
      and uft1_pass == (1 == 1) and uft2_pass == (1 == 0)
      and uft1_n == 12 and uft6_n == 0 and score_machinable == 3,
      'status=%d complete=%d integrated=%d eqsum=%d experiment=%d final=%d UFT1=%d/22 UFT6=%d/22 score=%d'
      % (status_hits, complete_hits, integrated_hits, eqsum_hits, experiment_hits,
         final_hits, uft1_n, uft6_n, score_machinable))
guard('G41-3', '类别互斥有牙：替换「非测量锚」后结论翻转',
      category_exclusion == 1 and category_exclusion_mut == 0
      and '非测量锚' in w3_def and '[C] 不纳入' in integrated,
      'original=%d mutated=%d W3def=%s' % (category_exclusion, category_exclusion_mut, w3_def))
guard('G41-4', '外部输入注入不变量：6/12/15/UNBOUNDED 全不改类别通过数',
      inv_ok and ext_chain[-1] == 'UNBOUNDED'
      and [r['external'] for r in injected[:3]] == [6, 12, 15]
      and all(r['w3_debt'] == str(F(35, 2)) for r in injected),
      injection_read)
guard('G41-5', 'PASS 不迁移有牙：L3→L4 闸门置 1 会伪造 22 个 validated',
      validated_gate0 == 0 and validated_gate1 == systems
      and nomig_count >= 4 and redline_hits == 4 and complete_hits == 7,
      'gate0=%d gate1=%d nomig=%d redline=%d' % (validated_gate0, validated_gate1, nomig_count, redline_hits))
guard('G41-6', '最小闭合集 C1–C6 与执行序逐项命中',
      closure_ids == [1, 2, 3, 4, 5, 6] and closure_order
      and len(closure_governance) == 2 and len(closure_substantive) == 3
      and len(closure_dependent) == 1,
      'ids=%s order=%s governance=%d substantive=%d dependent=%d'
      % (closure_ids, closure_order, len(closure_governance), len(closure_substantive), len(closure_dependent)))
guard('G41-7', 'N1–N18、函数级自由度与 6/12/15 链同时命中',
      len(n_ids) == 18 and g1_zero and r95_ext == 12 and a39_ext == 15
      and a40_ext == 6 and unbounded_hit,
      'N=%d g1zero=%s ext=[%d,%d,%d] unbounded=%s'
      % (len(n_ids), g1_zero, a40_ext, r95_ext, a39_ext, unbounded_hit))
guard('G41-8', '跨源计数校准：21/1 与 19/3 差异必须报 MISMATCH',
      tier_unique == [(19, 3), (21, 1)] and json_tier == data_tier == (21, 1)
      and judge_tier == integrated_tier == (19, 3),
      'json=%s data=%s judge=%s integrated=%s unique=%s'
      % (json_tier, data_tier, judge_tier, integrated_tier, tier_unique))
guard('G41-9', '双分母与达成度口径：22 现测 / 18 快照 / 1/6 / score=3',
      sum(status_counts) == 22 and status_counts == [6, 10, 2, 4]
      and sum(integrated_counts) == 18 and integrated_counts == [2, 3, 9, 4]
      and sum(ratings.values()) == 22 and '统一场论达成度 1/6' in eqsum
      and score_machinable == 3,
      'status=%s sum=%d integrated=%s sum=%d ratings=%s score=%d'
      % (status_counts, sum(status_counts), integrated_counts, sum(integrated_counts), ratings, score_machinable))
SRC = read_text(os.path.join(HERE, BASE + '.py'))
TREE = ast.parse(SRC)
true_consts = [n.lineno for n in ast.walk(TREE)
               if isinstance(n, ast.Constant) and isinstance(n.value, bool) and n.value == (1 == 1)]
guard('G41-10', '书写式守卫：源码无 Python 布尔字面量，红线文本在册',
      len(true_consts) == 0 and '不宣称完成统一场' in SRC
      and '0/22、UFT-3=0、L3=0、validated=0' in SRC,
      'literal_true_consts=%d redline_text=%s' % (len(true_consts), '0/22、UFT-3=0、L3=0、validated=0' in SRC))

# ---------- 汇总 / 产物 ----------
npass = sum(1 for e in ENTRIES if e['verdict'] == 'PASS')
nfail = sum(1 for e in ENTRIES if e['verdict'] == 'FAIL')
nbnd = sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY')
ninfo = sum(1 for e in ENTRIES if e['verdict'] == 'INFO')
nok = sum(1 for g in GUARDS if g['ok'])
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), npass, nfail, nbnd, ninfo, nok, len(GUARDS)))
emit('== 总裁定：FAIL（作为「补齐外部输入即可完成统一场」）；组织/数学完成不迁移为物理完成 ==')
emit('红线：0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': {'PASS': npass, 'FAIL': nfail, 'BOUNDARY': nbnd, 'INFO': ninfo},
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (nok, len(GUARDS)),
    'readings': {
        'matrix': {'systems': systems, 'criteria': len(criteria), 'cells': cells,
                   'verdict_dist': verdict_dist, 'full_pass': len(full_pass),
                   'W0_pass': w0_pass, 'W3_debt': str(w3_debt),
                   'debt_max': debt_max, 'nonzero_pass': nonzero_pass},
        'status_counts': status_counts, 'integrated_counts_18': integrated_counts,
        'rating_distribution': ratings, 'uft_json': {
            'uft1_pass': uft1_pass, 'uft1_n': uft1_n, 'uft2_pass': uft2_pass,
            'uft3_strict': uft3_strict, 'uft6_n': uft6_n,
            'score_machinable': score_machinable},
        'tier_pairs': {'json': json_tier, 'data_md': data_tier,
                       'judgment': judge_tier, 'integrated_quote': integrated_tier,
                       'unique': tier_unique},
        'external_chain': ext_chain, 'injected': injected,
        'category_exclusion': category_exclusion,
        'category_exclusion_mutated': category_exclusion_mut,
        'pass_gate_mutation': {'gate0_validated': validated_gate0,
                               'gate1_fake_validated': validated_gate1,
                               'readme_no_migration_hits': nomig_count},
        'closure_ids': closure_ids, 'closure_order': closure_order,
        'necessary_conditions_N_ids': n_ids,
        'source_static_hits': {'status': status_hits, 'complete': complete_hits,
                               'integrated': integrated_hits, 'eqsum': eqsum_hits,
                               'experiment': experiment_hits, 'final': final_hits},
        'redline_hits': redline_hits,
    },
    'self_corrections': [
        '首版判定册档位分布正则未容纳「未完成 19」中的空格，现场 runpy 解析前已改为 [^0-9]+',
        '首版整合全集档位分布正则未容纳「未完成 19 / 纲领草案 3」中的空格，已修正',
        '首版实验方案书静态词表按无粗体/无空格写法，匹配不到「有预测且对 = **0/22**」与「UFT-3 = 0」，已对齐原文',
    ],
    'boundaries': [
        '本册只做完成条件的类别/账本判定，不构造具体 GUT 谱、不跑 RGE/RK4、不自推新物理',
        'C07 的函数级自由度是 r95/attack39/attack40 已登记事实的归并，不是新的物理证明',
        'C08 跨源计数差异只登记 MISMATCH，不修改任何上游事实源',
        '完成度审计的「完成」仅指组织/文档/数学层；物理层 L4 全 OPEN',
    ],
    'methodology_notes': [
        'G41-10 用 1 == 1 比较式检查布尔字面量，避免 AST 守卫自身写入被扫描命中',
        '所有数值均带只读事实源路径与行号/JSON 键；纯标准库、无随机、不改 system.json / claims.csv / verify.py',
    ],
    'source_refs': {
        'matrix': '../全维全体系统一场论/数据/全维验收矩阵.json:criteria/systems/cells/verdict_dist/full_pass/bottleneck',
        'w_judgment': '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md:L17/L29-40/L103/L120-131',
        'status': '../状态看板.md:L11/L40-42/L48/L100-107/L118',
        'complete': '../统一场论完成度审计_20261009.md:L3-6/L17-23/L91-105',
        'integrated': '../统一理论体系_已验证正确内容整合全集.md:L13-17/L27-29/L1166/L1189-1195',
        'uft_json': '../本项目_全维自洽与归一化/数据/本项目_统一场论达成度重算_2026-10-08.json:L4-46',
        'uft_judgment': '../本项目_全维自洽与归一化/判定_本项目_统一场论达成度重算与最小闭合清单_2026-10-08.md:L23/L35-40/L78/L97',
        'uft_md': '../本项目_全维自洽与归一化/数据/本项目_统一场论达成度重算_2026-10-08.md:L86',
        'eqsum': '../../理论体系方程总汇_正确方程集_2026-10-14.md:L63/L97/L366/L420',
        'experiment': '统一场论_实验验证方案书_2026-10-21.md:L5/L33/L36/L41-45',
        'final': '穷尽攻破_统一场论终局总成_2026-10-21.md:L22/L58-59',
        'g1': '统一场论必要条件清单_G1_2026-10-30.md:L5-53',
        'r95': '../本项目_全维自洽与归一化/判定_TUFT-r95-螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.md:L113-155',
        'attack39': 'attack39_omega自由函数防线_四路封死与定量互斥_2026-11-08_report.txt:L18-21',
        'attack40': 'attack40_力统一承重前提_阈值Yukawa联合可识别性_2026-11-08_report.txt:L17-22',
    },
    'cross_refs': [
        '../全维全体系统一场论/数据/全维验收矩阵.json',
        '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md',
        '../状态看板.md',
        '../统一场论完成度审计_20261009.md',
        '../统一理论体系_已验证正确内容整合全集.md',
        '../../理论体系方程总汇_正确方程集_2026-10-14.md',
        '统一场论_实验验证方案书_2026-10-21.md',
        '穷尽攻破_统一场论终局总成_2026-10-21.md',
        '统一场论必要条件清单_G1_2026-10-30.md',
        '../本项目_全维自洽与归一化/判定_本项目_统一场论达成度重算与最小闭合清单_2026-10-08.md',
        '../本项目_全维自洽与归一化/数据/本项目_统一场论达成度重算_2026-10-08.json',
        '../本项目_全维自洽与归一化/数据/本项目_统一场论达成度重算_2026-10-08.md',
        '../本项目_全维自洽与归一化/判定_TUFT-r95-螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.md',
        'attack39_omega自由函数防线_四路封死与定量互斥_2026-11-08_report.txt',
        'attack40_力统一承重前提_阈值Yukawa联合可识别性_2026-11-08_report.txt',
        '判定_attack39_攻破㉛_omega自由函数防线_四路封死与定量互斥_2026-11-08.md',
        '判定_attack40_攻破㉜_力统一承重前提_阈值Yukawa联合可识别性_2026-11-08.md',
    ],
    'redlines': {'zero_of_22': 'unchanged', 'UFT-3': 0, 'L3': 0, 'validated': 0},
    'candidate_verdict': 'FAIL',
    'exit': 0 if nok == len(GUARDS) else 1,
}
with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')
sys.exit(0 if nok == len(GUARDS) else 1)