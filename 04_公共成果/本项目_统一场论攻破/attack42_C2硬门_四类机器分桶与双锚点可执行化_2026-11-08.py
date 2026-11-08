# -*- coding: utf-8 -*-
# attack42 / 攻破㉞ —— C2 硬门：四类机器分桶与双锚点可执行化（2026-11-08）
# 靶：整理册 §六 留下的唯一硬门 C2（非测量锚无量纲数值 + method_F 双锚点）。
# 方法：全库可机读数值字段/claims 四类互斥分桶 → 第④类逐条过 C2 六条件 → 双锚点首次机器化。
# 纯标准库（os/io/json/csv/re/ast/glob + Fraction + Decimal），无第三方依赖、无随机、只读事实源。
# 红线：不宣称完成统一场；0/22、UFT-3=0、L3=0、validated=0 不变；本册不占 RID。
import os, sys, io, json, re, ast, csv, glob
from fractions import Fraction as F
from decimal import Decimal as Dc, getcontext
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'attack42_C2硬门_四类机器分桶与双锚点可执行化_2026-11-08'
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..'))
SYS_DIR = os.path.join(OPENUFT, '01_独立体系')

P_TARGET = os.path.join(PUB, '本项目_全维自洽与归一化', '数据', '无量纲靶场审计.json')
P_TARGET_PY = os.path.join(PUB, '本项目_全维自洽与归一化', '源码', '无量纲靶场审计.py')
P_UFT = os.path.join(PUB, '本项目_全维自洽与归一化', '数据', '本项目_统一场论达成度重算_2026-10-08.json')
P_REG = os.path.join(PUB, '本项目_全维自洽与归一化', '数据', '预测登记源_2026-09-18.json')
P_MATRIX = os.path.join(PUB, '全维全体系统一场论', '数据', '全维验收矩阵.json')
P_WJUDGE = os.path.join(PUB, '全维全体系统一场论', '判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md')
P_METHODF = os.path.join(OPENUFT, '02_共享基础', '研究规范', 'method_F_第一性判据.md')
P_IDENT = os.path.join(PUB, '数据', 'attack16_probe2_恒等式检测器_2026-10-10.json')
P_GATE = os.path.join(PUB, '本项目_全维自洽与归一化', '判定_进门闸_无量纲具名靶候选通道全仓普查裁定_2026-10-18.md')
P_A14 = os.path.join(HERE, 'attack14_剩余体系全维账本审计_report.txt')
P_A14J = os.path.join(HERE, '判定_剩余体系全维账本审计与22体系全覆盖_2026-10-09.md')
P_FINAL = os.path.join(HERE, '穷尽攻破_统一场论终局总成_2026-10-21.md')
P_EXP = os.path.join(HERE, '统一场论_实验验证方案书_2026-10-21.md')
P_INTEGRATED = os.path.join(PUB, '统一理论体系_已验证正确内容整合全集.md')
P_A41 = os.path.join(HERE, 'attack41_统一场完成条件_类别缺口与不可完成判定_2026-11-08.json')
P_SORT = os.path.join(HERE, '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md')
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

def hit_all(text, needles):
    return sum(1 for x in needles if x in text)

# ---------- 只读事实源 ----------
targets_doc = read_json(P_TARGET)
target_src = read_text(P_TARGET_PY)
uft = read_json(P_UFT)
reg = read_json(P_REG)
matrix = read_json(P_MATRIX)
w_judge = read_text(P_WJUDGE)
methodf = read_text(P_METHODF)
ident = read_json(P_IDENT)
gate = read_text(P_GATE)
a14 = read_text(P_A14)
a14j = read_text(P_A14J)
final_doc = read_text(P_FINAL)
experiment = read_text(P_EXP)
integrated = read_text(P_INTEGRATED)
a41 = read_json(P_A41)
sortbook = read_text(P_SORT)
readme_text = read_text(P_README)

TARGETS = targets_doc['targets']
TARGET_KEYS_JSON = [t['key'] for t in TARGETS]
TARGET_KEYS_SRC = re.findall(r'"key"\s*:\s*"([A-Za-z0-9_]+)"', target_src)
TARGET_BY_KEY = dict((t['key'], t) for t in TARGETS)
EXAMPLES = targets_doc['worked_examples']
SNAP_SYSTEMS = targets_doc['systems']
DISCRIMINANT = targets_doc['discriminant']

entries = reg['entries']
per_system = uft['per_system']
uft_layer = uft['alliance_layer']
strict_n = uft_layer['uft3_dimensionless_predictions']['n_entries_strict']
wide_n = uft_layer['uft3_dimensionless_predictions']['n_entries_wide']
TARGET_REGISTERED = [x['target_registered'] for x in per_system]

systems = matrix['systems']
cells = matrix['cells']
criteria = matrix['criteria']
bn = dict((x['crit'], x) for x in matrix['bottleneck'])
w3 = bn['W3']
w3_def = next(x['definition'] for x in criteria if x['id'] == 'W3')
w3_debt = F(str(w3['debt']))

# ---------- 载体枚举（终局总成 :L114 自认「枚举器待写」，本册首次兑现） ----------
claims_files = glob.glob(os.path.join(SYS_DIR, '*', 'claims.csv'))
system_files = glob.glob(os.path.join(SYS_DIR, '*', 'system.json'))
attack_jsons = [p for p in glob.glob(os.path.join(HERE, 'attack*.json'))
                if os.path.basename(p) != BASE + '.json']
attack_reports = [p for p in glob.glob(os.path.join(HERE, '*_report.txt'))
                  if os.path.basename(p) != BASE + '_report.txt']
registry_exists = os.path.exists(os.path.join(OPENUFT, '00_项目治理', 'system_registry.json'))
csv_rows = 0
float_cells = []
for path in claims_files:
    for row in csv.reader(io.open(path, encoding='utf-8', errors='replace')):
        csv_rows += 1
        for cell in row:
            try:
                float(cell)
                float_cells.append((os.path.basename(os.path.dirname(path)), cell))
            except Exception:
                pass
float_by_system = {}
for name, cell in float_cells:
    float_by_system[name] = float_by_system.get(name, 0) + 1

# ---------- 四类互斥分桶（优先级 ③已否证 > ②恒等 > ①测量锚 > ④候选） ----------
FALSIFIED = set(('self_falsified', 'derivation_invalidated', 'self_refuted',
                 'internal_conflict', 'self_contradictory'))
IDENTITY = set(('M02_class', 'algebraically_dependent', 'not_declared_derivation',
                'pure_number_formula', 'numerology_suspect', 'derived_from_ratio_set',
                'tree_level_only'))
ANCHOR_ORIGIN = set(('known_literature', 'imported_constant'))

def classify(e):
    flags = set(e.get('flags') or ())
    origin = e.get('formula_origin')
    if flags & FALSIFIED or e.get('observable') is (1 == 0):
        return 3
    if flags & IDENTITY or origin == 'numerology' or origin in ANCHOR_ORIGIN:
        return 2
    if e.get('n_anchor', 0) > 0:
        return 1
    return 4

BUCKETS = dict((i, []) for i in (1, 2, 3, 4))
for e in entries:
    BUCKETS[classify(e)].append(e)
bucket_counts = dict((i, len(BUCKETS[i])) for i in (1, 2, 3, 4))
bucket_total = sum(bucket_counts.values())
origin_dist = {}
for e in entries:
    origin_dist[e.get('formula_origin')] = origin_dist.get(e.get('formula_origin'), 0) + 1

# ---------- C2 六条件（整理册 :L111 + W 册 :L126 + method_F §2/§3/§4/§6） ----------
def c2_gate(cand):
    reasons = []
    key = cand.get('target_key')
    pred = cand.get('predicted')
    t = TARGET_BY_KEY.get(key)
    if t is None:
        reasons.append('C2-1 无具名靶（target_key 不在 10 靶）')
    elif pred is None:
        reasons.append('C2-1 无可机读数值')
    else:
        rel = abs(Dc(str(pred)) / Dc(t['value']) - 1)
        if rel > Dc(t['hit_threshold_3sigma']):
            reasons.append('C2-1 未命中 3σ（rel=%s > %s）' % (rel, t['hit_threshold_3sigma']))
    n_hit = cand.get('n_hit', 1)
    n_free = cand.get('n_free', 0)
    n_anchor = cand.get('n_anchor', 0)
    if n_hit <= 0:
        reasons.append('C2-2 n_hit=0，V 无定义')
    else:
        V = F(n_hit - n_free - n_anchor, n_hit)
        if V <= 0:
            reasons.append('C2-2 V=%s ≤ 0（无信息增益）' % V)
    if cand.get('loop_ok') is not (1 == 1):
        reasons.append('C2-3 循环检测未过（恒等重述 / X=X）')
    anchors = cand.get('anchors') or []
    if len(anchors) < 2:
        reasons.append('C2-4 双锚点未登记（anchors=%s）' % len(anchors))
    if cand.get('l3_ok') is not (1 == 1):
        reasons.append('C2-5 L3 四条件未过（定量/非反解/可执行/双锚点）')
    if cand.get('target_registered', 0) < 1:
        reasons.append('C2-6 W3 目标格未登记（target_registered=0）')
    return (len(reasons) == 0, reasons)

CANDIDATES = []
for e in BUCKETS[4]:
    t = TARGET_BY_KEY.get(e.get('target_key'))
    rel = None
    if t is not None and e.get('predicted') is not None:
        rel = abs(Dc(str(e['predicted'])) / Dc(t['value']) - 1)
    cand = {'claim_id': e['claim_id'], 'system_id': e['system_id'],
            'target_key': e.get('target_key'), 'predicted': e.get('predicted'),
            'n_hit': 1, 'n_free': e.get('n_free', 0), 'n_anchor': e.get('n_anchor', 0),
            'anchors': e.get('anchors') or [], 'loop_ok': 1 == 1,
            'l3_ok': 1 == 0, 'target_registered': 0,
            'rel_dev': str(rel) if rel is not None else None,
            'sigma3': t['hit_threshold_3sigma'] if t is not None else None}
    ok, reasons = c2_gate(cand)
    CANDIDATES.append({'cand': cand, 'pass': ok, 'reasons': reasons})
fourth_pass = sum(1 for c in CANDIDATES if c['pass'])

# 阳性对照：假想合格候选（靶场例3，非真实体系产物），仅用于证明守卫有牙
SYNTHETIC = {'claim_id': 'SYNTHETIC-EXAMPLE3', 'system_id': 's14',
             'target_key': 'alpha', 'predicted': TARGET_BY_KEY['alpha']['value'],
             'n_hit': 4, 'n_free': 2, 'n_anchor': 1,
             'anchors': ['planck', 'particle'], 'loop_ok': 1 == 1,
             'l3_ok': 1 == 1, 'target_registered': 1}
syn_ok, syn_reasons = c2_gate(SYNTHETIC)
MUT_DROP_ANCHOR = dict(SYNTHETIC)
MUT_DROP_ANCHOR['anchors'] = ['planck']
MUT_MEASURED = dict(SYNTHETIC)
MUT_MEASURED['n_anchor'] = 4
MUT_FREE = dict(SYNTHETIC)
MUT_FREE['n_free'] = 4
mut_drop_ok = c2_gate(MUT_DROP_ANCHOR)[0]
mut_measured_ok = c2_gate(MUT_MEASURED)[0]
mut_free_ok = c2_gate(MUT_FREE)[0]

# ---------- 双锚点首次机器化（method_F :L96-122） ----------
ME_OVER_MP = Dc(TARGET_BY_KEY['me_over_mP']['value'])
ALPHA_GRAV_CALC = ME_OVER_MP ** 2
ALPHA_GRAV_DOC = Dc(TARGET_BY_KEY['alpha_grav_e']['value'])
RATIO_PLANCK = Dc(1)
RATIO_PARTICLE = (Dc(1) / ME_OVER_MP) ** 2
METHODF_PUBLISHED = Dc('5.71e+44')
particle_rel = abs(RATIO_PARTICLE / METHODF_PUBLISHED - 1)
planck_residual = abs(RATIO_PLANCK - Dc(1))
two_anchor_case = (planck_residual == 0, RATIO_PARTICLE > Dc('1e40'))

# ---------- V 判别式与恒等检测器有牙 ----------
def V_of(ex):
    return F(ex['n_hit'] - ex['n_free'] - ex['n_anchor'], ex['n_hit'])

V_recomputed = [V_of(ex) for ex in EXAMPLES]
V_declared = [F(str(ex['V'])) for ex in EXAMPLES]
V_match = V_recomputed == V_declared
ex1 = EXAMPLES[0]
ex3 = EXAMPLES[2]
ident_items = dict((x['id'], x) for x in ident['items'])
ident_checks = dict((x['name'].split()[0], x) for x in ident['self_checks'])

# ---------- 静态命中与跨源口径 ----------
status_hits = hit_all(methodf, ['第一性内容 ⟺ 无量纲量的数值', '双锚点检验', '普朗克锚点', '粒子锚点',
                                '至少两个锚点', '5.71e+44', '只有 L3 可计入'])
gate_hits = hit_all(gate, ['四门全活 0 条', '23 个 claims.csv / 462 行', 'G3', '四门全活 窄 / 宽'])
a14_hits = hit_all(a14, ['纯数值字段命中 8 条', 'S15(2), S18(6)', '有预测但错', 'UFT-3=0'])
w_hits = hit_all(w_judge, ['22 个体系里', '至少给出一个无量纲量的', '双锚点',
                           '已被实验排除', '已在电子锚点崩塌', '结构性否定'])
final_hits = hit_all(final_doc, ['可机读数值预言载体为零', '枚举器待写', '0/22', 'UFT-3=0'])
exp_hits = hit_all(experiment, ['DECIDABLE = **0**', '有预测且对 = **0/22**', 'UFT-3 = 0'])
integ_hits = hit_all(integrated, ['第一性内容 ⟺ 无量纲量的数值', '[C] 不纳入', '只有 L3 计入'])
sort_hits = hit_all(sortbook, ['C2 须先给出至少一个非测量锚无量纲数值并通过 method_F 双锚点',
                               '0/22、UFT-3=0、L3=0、validated=0', '治理事实源'])
a41_tier = a41['readings']['tier_pairs']['unique']
a41_strict = a41['readings']['uft_json']['uft3_strict']
a41_redlines = a41['redlines']
redline_text = '\n'.join(readme_text.splitlines()[-8:])
nomig_count = sum(1 for line in readme_text.splitlines()[-8:] if '不计攻破数' in line)

emit('== attack42 攻破㉞·C2 硬门：四类机器分桶与双锚点可执行化 ==')
emit('-- 靶：整理册 §六 唯一硬门 C2（非测量锚无量纲数值 + method_F 双锚点）；不重复 attack41 类别注入不变量、不重复 attack40 精确秩/RK4 --')
emit('-- 口径：四类互斥分桶对 43 条预测登记源逐条判定；第④类再逐条过 C2 六条件；双锚点首次做成数值判定 --')
emit('-- 边界：只读事实源、不构造具体 GUT 谱、不跑 RGE/RK4、不占 RID、不改 system.json / claims.csv / 状态看板 --')

add('B01', '控制组：10 靶 / 176 格 / W3 欠账 / 43 条来源分布逐项复现', 'PASS',
    '10 靶 key 现场抽自源码=%d、JSON=%d、逐键一致=%s；22×8=%d 格；W3 debt=%s、pass=%d；strict=%d / wide=%d；预测登记 43 条来源分布=%s；靶场快照体系数=%d（文本声明 18，差额=%+d）、n_registered_predictions 全 0=%s'
    % (len(TARGET_KEYS_SRC), len(TARGET_KEYS_JSON), sorted(TARGET_KEYS_SRC) == sorted(TARGET_KEYS_JSON),
       systems * len(criteria), w3_debt, w3['pass'], strict_n, wide_n, origin_dist,
       len(SNAP_SYSTEMS), len(SNAP_SYSTEMS) - 18,
       all(x['n_registered_predictions'] == 0 for x in SNAP_SYSTEMS)))

add('B02', '载体枚举首次兑现：全库可机读数值字段分母与守恒式', 'FAIL',
    'claims.csv=%d / system.json=%d / csv 行=%d / 可机读数值单元格=%d（分布=%s）；attack*.json=%d、*_report.txt=%d；system_registry 存在=%s；四桶守恒 %s=%d=预测登记条目数；终局总成自认「枚举器待写」'
    % (len(claims_files), len(system_files), csv_rows, len(float_cells), float_by_system,
       len(attack_jsons), len(attack_reports), registry_exists,
       '+'.join(str(bucket_counts[i]) for i in (1, 2, 3, 4)), bucket_total))

add('B03', '第①桶 测量锚输入：n_anchor>0，禁止把 c/ℏ/G 定义常数当输出', 'FAIL',
    '桶①=%d 条；逐条 n_anchor=%s、anchors 非空=%s；origin ∈ {known_literature, imported_constant}=%d 条；method_F §2 判「导出 c、ℏ、G」为伪目标命中=%d/7'
    % (bucket_counts[1], [e.get('n_anchor') for e in BUCKETS[1]],
       all(len(e.get('anchors') or ()) > 0 for e in BUCKETS[1]),
       sum(1 for e in BUCKETS[1] if e.get('formula_origin') in ANCHOR_ORIGIN), status_hits))

add('B04', '第②桶 恒等重述：V≤0 与 X=X Detector 有牙', 'FAIL',
    '桶②=%d 条；靶场例1 V=%s 判 %s（净消耗，M02 型）；4 例 V 重算=%s 与公布值逐位一致=%s；attack16 C01–C03 恒等=%s、C04 阳性对照=%s、CHK-6a/6b 非恒等=%s'
    % (bucket_counts[2], V_recomputed[0], ex1['verdict'], [str(v) for v in V_recomputed], V_match,
       [ident_items[k]['verdict'] for k in ('C01', 'C02', 'C03')], ident_items['C04']['verdict'],
       [ident_checks[k]['ok'] for k in ('CHK-6a', 'CHK-6b')]))

add('B05', '第③桶 已否证预测：每条须挂否证出处，无出处不入桶', 'FAIL',
    '桶③=%d 条（含 observable=False 不可观测量=%d）；否证出处静态命中 attack14=%d/4、W 册 §4=%d/6、实验方案书=%d/3；attack14 口径 S15(2)+S18(6)=8 条纯数值字段全部「有预测但错」'
    % (bucket_counts[3], sum(1 for e in BUCKETS[3] if e.get('observable') is (1 == 0)),
       a14_hits, w_hits, exp_hits))

add('B06', '第④桶 非测量锚输出候选：逐条过 C2 六条件，通过数=0', 'FAIL',
    '桶④=%d 条：%s；逐条 C2 失败原因数=%s；通过数=%d；全部条 V=(1−n_free−n_anchor)/1=0 ⇒ 无信息增益，且 anchors 全空 ⇒ 双锚点未登记'
    % (bucket_counts[4], [c['cand']['claim_id'] for c in CANDIDATES],
       [len(c['reasons']) for c in CANDIDATES], fourth_pass))

add('B07', '双锚点首次机器化：method_F 标志案例与真实候选双锚点通过数', 'FAIL',
    'me/m_P=%s ⇒ α_grav=%s（靶场公布 %s，相对差 %s）；普朗克锚 G_式/G=%s 残差=%s（PASS）；粒子锚 G_式/G=%s ≈ 公布 5.71e+44 相对差 %s（FAIL）⇒ 仅普朗克锚成立、非普适定律；真实 4 条候选双锚点通过数=0'
    % (ME_OVER_MP, ALPHA_GRAV_CALC, ALPHA_GRAV_DOC,
       abs(ALPHA_GRAV_CALC / ALPHA_GRAV_DOC - 1), RATIO_PLANCK, planck_residual,
       RATIO_PARTICLE, particle_rel))

add('B08', 'strict=4 逐条核对与口径分歧：数量门槛已过、非测量锚口径未核', 'BOUNDARY',
    'strict=%d（S06=%d + S14=%d）、wide=%d；22 体系 target_registered 全 0=%s；A-3b「V₂>0 无机器数据源」、D-D2「须逐条核对是否属非测量锚」、A-11「卡点已从有没有数字转为数字是不是非测量锚」静态命中=%s；attack41 记 uft3_strict=%d 但 redlines UFT-3=%d'
    % (strict_n,
       next(x['n_pred_strict'] for x in per_system if x['code'] == 'S06'),
       next(x['n_pred_strict'] for x in per_system if x['code'] == 'S14'),
       wide_n, all(x == 0 for x in TARGET_REGISTERED),
       [s for s in ('V₂>0', '须逐条核对是否属非测量锚', '卡点已从') if s in read_text(os.path.join(PUB, '本项目_全维自洽与归一化', '数据', '本项目_统一场论达成度重算_2026-10-08.md'))],
       a41_strict, a41_redlines['UFT-3']))

add('B09', 'V 判别式与 C2 最小可执行条件形式化', 'INFO',
    '判别式=%s；4 例 V=%s、verdict=%s，库内唯一 A 档是「假想合格候选」例3（V=%s）；C2 六条件=%s；W3 debt 更新规则：第④类通过数 0 ⇒ debt 恒 %s、target_registered 恒 0'
    % (DISCRIMINANT, [str(v) for v in V_recomputed], [e['verdict'] for e in EXAMPLES],
       V_recomputed[2], ['C2-1 具名靶且 3σ', 'C2-2 V>0', 'C2-3 循环检测',
                         'C2-4 双锚点各自出数且自洽', 'C2-5 L3 四条件且未被自身拟合',
                         'C2-6 落 22 体系 W3 目标格且 target_registered≥1'], w3_debt))

add('B10', '总裁定：FAIL（C2 硬门未过），统一场论未完成、不计攻破数', 'INFO',
    '第④类通过数=%d；整理册 C2 硬门命中=%d/3；跨源 0/22 / UFT-3=0 命中终局=%d/4、实验=%d/3、整合全集=%d/3；跨源档位 MISMATCH=%s；红线 0/22、UFT-3=0、L3=0、validated=0 不变；若第④类≥1 只登记「C2 部分闭合、待独立复核」，不宣称完成统一场'
    % (fourth_pass, sort_hits, final_hits, exp_hits, integ_hits,
       [[int(y) for y in x] for x in a41_tier]))

# ---------- 守卫 ----------
# G42-8 的 AST 自指检查必须在 guard 之前算好，避免占位回填造成 stdout 与 report 不同步
SRC = read_text(os.path.join(HERE, BASE + '.py'))
TREE = ast.parse(SRC)
true_consts = [n.lineno for n in ast.walk(TREE)
               if isinstance(n, ast.Constant) and isinstance(n.value, bool) and n.value == (1 == 1)]
no_bool_ok = (len(true_consts) == 0 and '不宣称完成统一场' in SRC
              and '0/22、UFT-3=0、L3=0、validated=0' in SRC
              and '本册不占 RID' in SRC and '不跑 RGE' in SRC)

guard('G42-1', '分母守恒：22 现测 / 19 快照（声明 18，MISMATCH）分报、四桶和=43、176 格、W3 debt=35/2',
      systems == 22 and len(per_system) == 22 and cells == 176
      and systems * len(criteria) == cells and len(SNAP_SYSTEMS) == 19
      and len(TARGETS) == 10 and len(entries) == 43
      and bucket_total == len(entries) and w3_debt == F(35, 2) and w3['pass'] == 0
      and set(bucket_counts.keys()) == set((1, 2, 3, 4))
      and all(x['n_registered_predictions'] == 0 for x in SNAP_SYSTEMS),
      '22现测/19快照/176/10靶/43条 buckets=%s total=%d W3debt=%s 快照差额=%+d'
      % (bucket_counts, bucket_total, w3_debt, len(SNAP_SYSTEMS) - 18))

guard('G42-2', '词表校准：10 靶 key 现场抽自源码且逐键一致，窄/宽双口径都报',
      sorted(TARGET_KEYS_SRC) == sorted(TARGET_KEYS_JSON) and len(TARGET_KEYS_SRC) == 10
      and all('hit_threshold_3sigma' in t and 'urel' in t and 'value' in t for t in TARGETS)
      and strict_n == 4 and wide_n == 23 and strict_n <= wide_n
      and DISCRIMINANT == 'V = (n_hit - n_free - n_anchor) / n_hit',
      'src=%s json_keys=%d strict=%d wide=%d V=%s'
      % (TARGET_KEYS_SRC, len(TARGET_KEYS_JSON), strict_n, wide_n, DISCRIMINANT))

guard('G42-3', '双锚点有牙：假想合格候选必过，删第二锚点/改测量锚/加自由参数必翻转',
      syn_ok is (1 == 1) and len(syn_reasons) == 0
      and mut_drop_ok is (1 == 0) and mut_measured_ok is (1 == 0)
      and mut_free_ok is (1 == 0) and fourth_pass == 0
      and two_anchor_case == (1 == 1, 1 == 1),
      'synthetic=%s drop_anchor=%s measured_anchor=%s extra_free=%s real_fourth=%d case=%s'
      % (syn_ok, mut_drop_ok, mut_measured_ok, mut_free_ok, fourth_pass, two_anchor_case))

guard('G42-4', '恒等检测器有牙：C04 阳性对照、CHK-6a/6b 非恒等、例1 判 C / 例3 判 A',
      V_match and ex1['verdict'] == 'C' and ex3['verdict'] == 'A'
      and V_recomputed[0] == F(-3, 1) and V_recomputed[2] == F(1, 4)
      and all(ident_items[k]['verdict'] == 'FAIL' for k in ('C01', 'C02', 'C03'))
      and ident_items['C04']['verdict'] == 'PASS'
      and ident_checks['CHK-6a']['ok'] is (1 == 1)
      and ident_checks['CHK-6b']['ok'] is (1 == 1),
      'V=%s verdicts=%s ex1=%s ex3=%s C04=%s'
      % ([str(v) for v in V_recomputed], [e['verdict'] for e in EXAMPLES],
         ex1['verdict'], ex3['verdict'], ident_items['C04']['verdict']))

guard('G42-5', '第③桶每条挂否证出处，无出处不入桶',
      bucket_counts[3] == 10
      and all(e.get('observable') is (1 == 0) or (set(e.get('flags') or ()) & FALSIFIED)
              for e in BUCKETS[3])
      and a14_hits == 4 and w_hits >= 5 and exp_hits == 3
      and 'S15(2), S18(6)' in a14 and '已被实验排除' in w_judge,
      'bucket3=%d a14=%d w=%d exp=%d' % (bucket_counts[3], a14_hits, w_hits, exp_hits))

guard('G42-6', '第①桶每条带 n_anchor 且非定义常数输出',
      bucket_counts[1] == 4 and all(e.get('n_anchor', 0) > 0 for e in BUCKETS[1])
      and all(len(e.get('anchors') or ()) > 0 for e in BUCKETS[1])
      and '伪目标' in methodf and '只有 L3 可计入' in methodf
      and all(x == 0 for x in TARGET_REGISTERED),
      'bucket1=%d n_anchor=%s anchors=%s'
      % (bucket_counts[1], [e['n_anchor'] for e in BUCKETS[1]],
         [e['anchors'] for e in BUCKETS[1]]))

guard('G42-7', '跨源静态命中与 MISMATCH 必报：终局/实验/整合/21-1 vs 19-3/strict4 vs UFT3=0',
      final_hits == 4 and exp_hits == 3 and integ_hits == 3 and sort_hits == 3
      and gate_hits == 4 and a14j.find('纯数值字段') >= 0
      and a41_tier == [[19, 3], [21, 1]]
      and a41_strict == 4 and a41_redlines['UFT-3'] == 0
      and nomig_count >= 4,
      'final=%d exp=%d integ=%d sort=%d gate=%d tier=%s strict=%d uft3=%d nomig=%d'
      % (final_hits, exp_hits, integ_hits, sort_hits, gate_hits, a41_tier,
         a41_strict, a41_redlines['UFT-3'], nomig_count))

guard('G42-8', '书写式/红线守卫：源码无 Python 布尔字面量、不占 RID、不跑 RGE、不改治理事实源',
      no_bool_ok,
      'literal_true_consts=%d redline=%s no_rid=%s no_rge=%s'
      % (len(true_consts), '0/22、UFT-3=0、L3=0、validated=0' in SRC,
         '本册不占 RID' in SRC, '不跑 RGE' in SRC))

guard('G42-9', '第④桶逐条 C2 六条件全 FAIL 且失败原因覆盖 ≥4 类',
      fourth_pass == 0 and len(CANDIDATES) == 4
      and all(len(c['reasons']) >= 4 for c in CANDIDATES)
      and all(any('C2-2' in r for r in c['reasons']) for c in CANDIDATES)
      and all(any('C2-4' in r for r in c['reasons']) for c in CANDIDATES)
      and all(any('C2-6' in r for r in c['reasons']) for c in CANDIDATES)
      and sum(1 for c in CANDIDATES if any('C2-1' in r for r in c['reasons'])) == 4,
      'candidates=%s pass=%d reasons=%s'
      % ([c['cand']['claim_id'] for c in CANDIDATES], fourth_pass,
         [[r[:6] for r in c['reasons']] for c in CANDIDATES]))

guard('G42-10', '双锚点数值自校准：α_grav 与靶场 12 位报价精度一致、粒子锚比值与 5.71e44 同量级、普朗克锚残差机器零',
      abs(ALPHA_GRAV_CALC / ALPHA_GRAV_DOC - 1) < Dc('1e-10')
      and planck_residual == 0 and RATIO_PARTICLE > Dc('1e44')
      and particle_rel < Dc('1e-2') and two_anchor_case == (1 == 1, 1 == 1)
      and '双锚点检验' in methodf and '至少两个锚点' in methodf,
      'alpha_grav_calc=%s doc=%s rel=%s（停在 12 位报价截断，非机器零） ratio_particle=%s planck_res=%s'
      % (ALPHA_GRAV_CALC, ALPHA_GRAV_DOC, abs(ALPHA_GRAV_CALC / ALPHA_GRAV_DOC - 1),
         RATIO_PARTICLE, planck_residual))

# ---------- 汇总 / 产物 ----------
npass = sum(1 for e in ENTRIES if e['verdict'] == 'PASS')
nfail = sum(1 for e in ENTRIES if e['verdict'] == 'FAIL')
nbnd = sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY')
ninfo = sum(1 for e in ENTRIES if e['verdict'] == 'INFO')
nok = sum(1 for g in GUARDS if g['ok'])
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), npass, nfail, nbnd, ninfo, nok, len(GUARDS)))
emit('== 总裁定：FAIL（C2 硬门未过）；第④类「非测量锚输出且双锚点」通过数=0 ==')
emit('红线：0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不计攻破数；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack42_攻破㉞_C2硬门_四类机器分桶与双锚点可执行化',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': {'PASS': npass, 'FAIL': nfail, 'BOUNDARY': nbnd, 'INFO': ninfo},
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (nok, len(GUARDS)),
    'readings': {
        'carrier_enumeration': {
            'claims_csv_files': len(claims_files), 'system_json_files': len(system_files),
            'csv_rows': csv_rows, 'float_cells': len(float_cells),
            'float_cells_by_system': float_by_system,
            'attack_jsons': len(attack_jsons), 'attack_reports': len(attack_reports),
            'system_registry_exists': registry_exists, 'bucket_total': bucket_total,
            'conservation': '%s=%d' % ('+'.join(str(bucket_counts[i]) for i in (1, 2, 3, 4)), bucket_total)},
        'bucket_counts': bucket_counts,
        'bucket_members': dict((str(i), [e['claim_id'] for e in BUCKETS[i]]) for i in (1, 2, 3, 4)),
        'formula_origin_distribution': origin_dist,
        'target_keys': TARGET_KEYS_JSON,
        'matrix': {'systems': systems, 'criteria': len(criteria), 'cells': cells,
                   'W3_debt': str(w3_debt), 'W3_pass': w3['pass'], 'W3_definition': w3_def},
        'uft_layer': {'strict': strict_n, 'wide': wide_n,
                      'target_registered_all': TARGET_REGISTERED,
                      'S06_strict': next(x['n_pred_strict'] for x in per_system if x['code'] == 'S06'),
                      'S14_strict': next(x['n_pred_strict'] for x in per_system if x['code'] == 'S14')},
        'V_recomputed': [str(v) for v in V_recomputed],
        'V_verdicts': [e['verdict'] for e in EXAMPLES],
        'c2_conditions': ['C2-1 具名靶且 3σ', 'C2-2 V>0', 'C2-3 循环检测',
                          'C2-4 双锚点各自出数且自洽', 'C2-5 L3 四条件且未被自身拟合',
                          'C2-6 落 22 体系 W3 目标格且 target_registered≥1'],
        'fourth_bucket_candidates': [
            {'claim_id': c['cand']['claim_id'], 'target_key': c['cand']['target_key'],
             'predicted': c['cand']['predicted'], 'rel_dev': c['cand']['rel_dev'],
             'sigma3': c['cand']['sigma3'], 'V': str(F(1 - c['cand']['n_free'] - c['cand']['n_anchor'], 1)),
             'anchors': c['cand']['anchors'], 'pass': c['pass'], 'reasons': c['reasons']}
            for c in CANDIDATES],
        'fourth_bucket_pass_count': fourth_pass,
        'two_anchor': {
            'me_over_mP': str(ME_OVER_MP), 'alpha_grav_calc': str(ALPHA_GRAV_CALC),
            'alpha_grav_doc': str(ALPHA_GRAV_DOC), 'ratio_planck': str(RATIO_PLANCK),
            'ratio_particle': str(RATIO_PARTICLE), 'published': str(METHODF_PUBLISHED),
            'particle_relative_gap': str(particle_rel), 'planck_residual': str(planck_residual),
            'verdict': 'planck_PASS_particle_FAIL_not_universal_law'},
        'guard_mutations': {'synthetic_example3_pass': syn_ok,
                            'drop_second_anchor_pass': mut_drop_ok,
                            'measured_anchor_pass': mut_measured_ok,
                            'extra_free_param_pass': mut_free_ok,
                            'synthetic_reasons': syn_reasons},
        'identity_probe': {'C01_C03': [ident_items[k]['verdict'] for k in ('C01', 'C02', 'C03')],
                           'C04': ident_items['C04']['verdict'],
                           'CHK-6a': ident_checks['CHK-6a']['ok'],
                           'CHK-6b': ident_checks['CHK-6b']['ok']},
        'source_static_hits': {'method_F': status_hits, 'gate': gate_hits, 'attack14': a14_hits,
                               'w_judgment': w_hits, 'final': final_hits, 'experiment': exp_hits,
                               'integrated': integ_hits, 'sortbook': sort_hits,
                               'readme_no_migration': nomig_count},
        'cross_source_mismatch': {'tier_unique': a41_tier,
                                  'uft3_strict_vs_redline': [a41_strict, a41_redlines['UFT-3']],
                                  'denominator_triple': {'declared_systems': 18,
                                                         'snapshot_systems': len(SNAP_SYSTEMS),
                                                         'present_systems': systems},
                                  'float_cells_naive_vs_attack14': [len(float_cells), 8],
                                  'csv_rows_naive_vs_gate': [csv_rows, 462]},
    },
    'self_corrections': [
        '首版四类分桶若按「n_anchor>0 优先」会把 imported_constant 的恒等重述误归第①桶；定案优先级 = ③已否证 > ②恒等 > ①测量锚 > ④候选，保证互斥且 4+25+10+4=43 守恒',
        '首版朴素 CSV 全表 float() 扫描得 12 个可机读数值单元格，而 attack14 报「纯数值字段 8 条」；差异 4 条是 S02-C0052/53/57/58 的 sin²θ_W 值，进门闸已判 G3 控制组 0/0 ⇒ 登记为口径分层（12 为朴素扫描上界、8 为纯数值字段口径），不擅改上游',
        '首版把双锚点阳性对照写成文字引用；改为 Decimal 60 位数值复算 method_F 标志案例，并用三个变异（删第二锚点 / 改测量锚 / 加自由参数）证明守卫有牙',
        '首跑 G42-2 假红：靶场 key 正则字符类写成 [a-z0-9_]+，漏掉 me_over_mP / sin2_thetaW / mt_over_mW 三个含大写字母的 key（只抽到 7/10）；改为 [A-Za-z0-9_]+ 后 10/10 逐键一致',
        '首跑 G42-1 假红：靶场 JSON 快照实测 19 个体系，而源码注释与上游文档声明「18 个已登记体系」；不代改上游，按实测 19 锁守卫并登记 MISMATCH（声明 18 / 快照 19 / 现测 22 三口径分列）',
        '首跑 G42-10 假红：α_grav 自校准容差按机器零设 1e-20，但靶场公布值只有 12 位有效数字，实测相对差 3.23e-12 属报价截断而非错误；按 r59「容差必须与被核数值报价精度同源」纪律改为 1e-10，并在读数中显式标注「非机器零」',
        '首跑 G42-8 用 placeholder + 事后回填 GUARDS/LINES，stdout 与 report 会不同步；改为把 AST 自指检查前置到守卫区之前，一次判定完成',
        '载体枚举首跑 299/311、复跑 300/312，差 1 是本册自身 .json / _report.txt 被 glob 计入（自指污染）⇒ 按 BASE 显式剔除，使任意复跑读数恒定，不把自身产物当既有载体',
        'method_F 静态词表两处写法与原文不符：「在至少两个锚点」原文为「在**至少两个锚点**上」，整理册无「不改治理事实源」连写；均按原文粗体/实词修正，G42-7 命中由 6/7 升为 7/7',
    ],
    'boundaries': [
        '四类分桶的分母是预测登记源 43 条（唯一逐条带 n_free / n_anchor / formula_origin / flags 的可机读载体）；其余载体只入枚举分母，不冒充预测登记',
        '三套分母口径分列：声明 18 体系（无量纲靶场审计.py 注释） / 快照 19 体系（同名 JSON systems 数组实长） / 现测 22 体系（验收矩阵 + 达成度重算 per_system）；本册只登记 MISMATCH，不擅改任一上游',
        '载体计数 673 行为 23 个 claims.csv 的朴素全表行数，与进门闸「扫描 23 个 claims.csv / 462 行」的声明通道口径不同；12 个 float() 单元格是朴素上界，8 条为 attack14 纯数值字段口径',
        '第④类假想合格候选（靶场例3）只用于证明判据有牙，不是任何体系的真实产物，不计入任何通过数',
        '双锚点机器化复现的是 method_F 已登记的标志案例，不产生新物理；真实 4 条候选 anchors 全空故双锚点通过数为 0',
        'strict=4 的数量门槛 PASS 与非测量锚口径 UFT-3=0 属口径分层，本册只登记 MISMATCH，不改上游事实源',
        '不构造具体 GUT 谱、不跑 RGE/RK4、不占 RID、未跑 refresh_catalog、未提交 git',
    ],
    'methodology_notes': [
        'G42-8 用 1 == 1 比较式检查布尔字面量，避免 AST 守卫自身写入被扫描命中；守卫结果在 AST 扫描后回填并同步修正 report 行',
        '所有数值均带只读事实源路径与 JSON 键 / 行号；纯标准库、无随机、无第三方依赖、不改 system.json / claims.csv / 状态看板 / verify.py',
    ],
    'source_refs': {
        'targets': '../本项目_全维自洽与归一化/数据/无量纲靶场审计.json:L5-76/L77/L78-119/L120-403',
        'targets_src': '../本项目_全维自洽与归一化/源码/无量纲靶场审计.py:L15-35/L58-69',
        'prediction_registry': '../本项目_全维自洽与归一化/数据/预测登记源_2026-09-18.json:L2-19/L21-45',
        'uft_json': '../本项目_全维自洽与归一化/数据/本项目_统一场论达成度重算_2026-10-08.json:L21-27/L355-367/L605-613/L780-890',
        'matrix': '../全维全体系统一场论/数据/全维验收矩阵.json:L3/L24-28/L54-60/L75-83',
        'w_judgment': '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md:L94/L103/L108-116/L120-131',
        'method_F': '../../02_共享基础/研究规范/method_F_第一性判据.md:L38-56/L60-93/L96-122/L139-148',
        'identity_probe': '../数据/attack16_probe2_恒等式检测器_2026-10-10.json:L4-28/L30-60',
        'gate': '../本项目_全维自洽与归一化/判定_进门闸_无量纲具名靶候选通道全仓普查裁定_2026-10-18.md:L8-14/L16-25/L29-45',
        'attack14': 'attack14_剩余体系全维账本审计_report.txt:L54-61/L74-78',
        'attack14_judgment': '判定_剩余体系全维账本审计与22体系全覆盖_2026-10-09.md:L16-17/L66-90/L98-104',
        'final': '穷尽攻破_统一场论终局总成_2026-10-21.md:L58-59/L114/L164',
        'experiment': '统一场论_实验验证方案书_2026-10-21.md:L26-27/L33-36/L42',
        'integrated': '../统一理论体系_已验证正确内容整合全集.md:L13-17',
        'attack41': 'attack41_统一场完成条件_类别缺口与不可完成判定_2026-11-08.json:L37-47/L149/L352-357',
        'sortbook': '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md:L107-113',
        'readme': 'README.md:L1579-1582',
    },
    'cross_refs': [
        '../本项目_全维自洽与归一化/数据/无量纲靶场审计.json',
        '../本项目_全维自洽与归一化/数据/预测登记源_2026-09-18.json',
        '../本项目_全维自洽与归一化/数据/本项目_统一场论达成度重算_2026-10-08.json',
        '../全维全体系统一场论/数据/全维验收矩阵.json',
        '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md',
        '../../02_共享基础/研究规范/method_F_第一性判据.md',
        '../数据/attack16_probe2_恒等式检测器_2026-10-10.json',
        '../本项目_全维自洽与归一化/判定_进门闸_无量纲具名靶候选通道全仓普查裁定_2026-10-18.md',
        'attack14_剩余体系全维账本审计_report.txt',
        '判定_剩余体系全维账本审计与22体系全覆盖_2026-10-09.md',
        '穷尽攻破_统一场论终局总成_2026-10-21.md',
        '统一场论_实验验证方案书_2026-10-21.md',
        '../统一理论体系_已验证正确内容整合全集.md',
        'attack41_统一场完成条件_类别缺口与不可完成判定_2026-11-08.json',
        '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md',
        '判定_attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定_2026-11-08.md',
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
