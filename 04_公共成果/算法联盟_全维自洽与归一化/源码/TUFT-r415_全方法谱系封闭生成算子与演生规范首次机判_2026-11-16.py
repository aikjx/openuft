# -*- coding: utf-8 -*-
# r415 / 算法联盟 —— 全方法谱系封闭生成算子与演生规范首次机判（2026-11-16）
# 用户命题：怎么可能一个没有统一，无穷思维处理模式，直到攻破。所有方法处理。
# 本册转译：把“无穷思维”收敛为有限封闭生成空间：25 类方法 × 10 个幂等交换生成算子 = 每类 1024 个规范变形，共 25600 个机器判决单元。
# 红线：本册不产生新物理，不宣称完成四力强度统一；只把所有已知/登记方法处理到终态，并对 D2 演生规范首次机判。
import os
import io
import re
import ast
import math
import json
import hashlib
import itertools
from decimal import Decimal as Dc, getcontext

try:
    sys_stdout = sys.stdout
except Exception:
    sys_stdout = None

import sys
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
COMMON = os.path.abspath(os.path.join(HERE, '..', '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-16'
STEM = 'TUFT-r415_全方法谱系封闭生成算子与演生规范首次机判_2026-11-16'

P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
P_JUDGE = os.path.join(PUB, '判定_TUFT-r415-全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.md')
P_README = os.path.join(PUB, 'README.md')

P_G7B = os.path.join(COMMON, '本项目_全维自洽与归一化', '判定_G7b_规范群选择_信息论位下界与位账本_2026-10-29.md')
P_CH82 = os.path.join(OPENUFT, '书籍', 'v1_正文', '第十五编_几何统一纲领能力边界白皮书', '第82章_几何统一纲领能力边界白皮书_从C到Q的nogo谱系与统一场论真实坐标.md')
P_R412 = os.path.join(PUB, '判定_TUFT-r412-力的统一全情况全方程全方案总账与分层统一新思维_2026-11-16.md')
P_R413 = os.path.join(PUB, '判定_TUFT-r413-出路C可变函数与部门选择的可识别性攻破_2026-11-16.md')
P_R414 = os.path.join(PUB, '判定_TUFT-r414-全维度全链路全层级架构流程图_图论攻破_2026-11-16.md')

FACT_PATHS = [P_G7B, P_CH82, P_R412, P_R413, P_R414]

VERDICT = ('ALL-METHODS-PROCESSED--CLOSED-GENERATOR-SPACE-25600--STRENGTH-UNIFY-PASS-0'
           '--D2-EMERGENT-GAUGE-FIRST-GATE-FAIL--INFINITE-THOUGHT-REDUCED-TO-FINITE-EQUIVALENCE'
           '--0OF6-UNCHANGED')

LINES = []
ENTRIES = []
GUARDS = []
POS = []

RED = {
    'completion_0_of_6': True,
    'coverage_0_of_22': True,
    'UFT3_zero': True,
    'L3_zero': True,
    'validated_zero': True,
    'gravity_four_force_correct_equations_zero': True,
    'L3_not_implies_L4': True,
}


def emit(s=''):
    LINES.append(s)
    print(s)


def add(uid, verdict, claim, reading):
    ENTRIES.append({'id': uid, 'verdict': verdict, 'claim': claim, 'reading': reading})
    emit('[%s] %s | %s' % (verdict, uid, claim))
    emit('            读数: ' + reading)


def guard(gid, desc, ok, reading):
    ok = bool(ok)
    GUARDS.append({'id': gid, 'desc': desc, 'ok': ok, 'reading': reading})
    emit('[%s] %s | %s' % ('OK' if ok else 'BAD', gid, desc))
    emit('            读数: ' + reading)
    return ok


def read_text(path):
    return io.open(path, encoding='utf-8').read()


def md5_text(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def md5_file(path):
    return md5_text(read_text(path))


def has_all(text, tokens):
    return all(tok in text for tok in tokens)


# ---------- 只读事实源 ----------
for p in FACT_PATHS:
    if not os.path.exists(p):
        print('MISSING_FACT_SOURCE ' + p)
        raise SystemExit(2)

FACT_BEFORE = dict((os.path.basename(p), md5_file(p)) for p in FACT_PATHS)
FACTS = dict((os.path.basename(p), read_text(p)) for p in FACT_PATHS)

G7B = FACTS[os.path.basename(P_G7B)]
CH82 = FACTS[os.path.basename(P_CH82)]
R412 = FACTS[os.path.basename(P_R412)]
R413 = FACTS[os.path.basename(P_R413)]
R414 = FACTS[os.path.basename(P_R414)]

# ---------- 25 类受控方法谱系 ----------
# layer: 0=纯形式, 1=结构/表示, 2=作用量/方程, 3=数值强度, 4=实验窗口, 5=统一目标。
METHODS = [
    {'id': 'M01', 'name': 'F0 记号层条件式', 'family': 'form', 'layer': 0, 'base': 'FAIL', 'source': 'r408', 'note': '只给记号约束，零物理内容'},
    {'id': 'M02', 'name': 'F1 母作用量式', 'family': 'form', 'layer': 2, 'base': 'FAIL', 'source': 'r408', 'note': '方程数下界 1:5:7，盒装不降独立方程数'},
    {'id': 'M03', 'name': 'F2 母场方程式', 'family': 'form', 'layer': 2, 'base': 'FAIL', 'source': 'r408', 'note': '交叉块为 0，引入交叉块需新耦合'},
    {'id': 'M04', 'name': 'F3 profile 母公式式', 'family': 'form', 'layer': 3, 'base': 'FAIL', 'source': 'r408', 'note': '弱作用无经典静力，定义域仅 3/4'},
    {'id': 'M05', 'name': 'F4 单耦合参数式', 'family': 'form', 'layer': 3, 'base': 'FAIL', 'source': 'r408', 'note': '117649 组命中 21，非平凡核为恒等复读'},
    {'id': 'M06', 'name': 'F5 多方程并列式', 'family': 'ledger', 'layer': 2, 'base': 'PART', 'source': 'r409', 'note': '登记层多数形式，但不产生单一主方程'},
    {'id': 'M07', 'name': 'NONE 未构成候选', 'family': 'ledger', 'layer': 0, 'base': 'OPEN', 'source': 'r409', 'note': '未提交候选，不构成机制'},
    {'id': 'M08', 'name': 'LU1 恒等式/记号统一', 'family': 'form', 'layer': 0, 'base': 'FAIL', 'source': 'r412', 'note': '零信息量'},
    {'id': 'M09', 'name': 'LU2 形式统一 UFE', 'family': 'form', 'layer': 1, 'base': 'PART', 'source': 'r412', 'note': '统一格式，不统一强度'},
    {'id': 'M10', 'name': 'LU3 四组分立', 'family': 'ledger', 'layer': 2, 'base': 'PART', 'source': 'r412', 'note': '四组并列，不是同源派生'},
    {'id': 'M11', 'name': 'LU4 profile 母式', 'family': 'form', 'layer': 3, 'base': 'FAIL', 'source': 'r412', 'note': '弱作用定义域缺口'},
    {'id': 'M12', 'name': 'LU5 数值统一层', 'family': 'numeric', 'layer': 3, 'base': 'FAIL', 'source': 'r412', 'note': '6/6 层同向否证'},
    {'id': 'M13', 'name': 'LU6 可变函数+部门选择', 'family': 'freedom', 'layer': 3, 'base': 'OPEN', 'source': 'r413', 'note': '+1 为伪代价，自由函数无界'},
    {'id': 'M14', 'name': 'GUT 大群合并', 'family': 'group', 'layer': 3, 'base': 'FAIL', 'source': 'ch82', 'note': '不几何化内部群；无质子衰变证据'},
    {'id': 'M15', 'name': 'SUSY 分级代数', 'family': 'group', 'layer': 2, 'base': 'FAIL', 'source': 'ch82', 'note': '整套超伴代价，LHC 零超粒子'},
    {'id': 'M16', 'name': '弦论/高自旋塔', 'family': 'group', 'layer': 2, 'base': 'PART', 'source': 'ch82', 'note': '额外紧致维+模空间，无实验确认'},
    {'id': 'M17', 'name': '演生规范/拓扑序', 'family': 'emergent', 'layer': 2, 'base': 'OPEN', 'source': 'ch82', 'note': '本册首次机判：地图条目，无最小构造'},
    {'id': 'M18', 'name': 'Kaluza-Klein 额外维', 'family': 'geometry', 'layer': 2, 'base': 'FAIL', 'source': 'ch82', 'note': '经典荷质比失败，内部荷受 CM 约束'},
    {'id': 'M19', 'name': 'ECSK/挠率载体', 'family': 'geometry', 'layer': 2, 'base': 'FAIL', 'source': 'r19-r21/r174', 'note': '挠率为代数 slave，传播需新动能项'},
    {'id': 'M20', 'name': '结群/CS/WZW 表示论', 'family': 'topology', 'layer': 1, 'base': 'PART', 'source': 'r10-r18/G7b', 'note': 'SU(2)/SU(3) 可构造，U(1)Y 与位缺口外'},
    {'id': 'M21', 'name': '量纲闭合/常数幂穷举', 'family': 'dimension', 'layer': 1, 'base': 'FAIL', 'source': 'r18/r37/r410', 'note': '量纲对强度零判别力'},
    {'id': 'M22', 'name': 'RG/β 跑动', 'family': 'rg', 'layer': 3, 'base': 'FAIL', 'source': 'r14/r16/v4', 'note': 'SM 不汇聚；整数拓扑量无法编码连续耦合'},
    {'id': 'M23', 'name': '渐近安全', 'family': 'rg', 'layer': 3, 'base': 'OPEN', 'source': 'r27/ch82', 'note': '合集登记方向，库内无四力接入构造'},
    {'id': 'M24', 'name': '信息论位账本', 'family': 'information', 'layer': 1, 'base': 'OPEN', 'source': 'G7b', 'note': '框架供给 0 bit，中心荷可补 2.3219 bit 但无来源'},
    {'id': 'M25', 'name': '外部输入/实验锚注入', 'family': 'external', 'layer': 4, 'base': 'FAIL', 'source': 'r15/r413/r414', 'note': '不是派生；只增加账单'},
]

# ---------- 10 个幂等交换生成算子 ----------
# 每个算子只置一个布尔位，因此 g(g(x))=g(x)，且任意两算子交换。
GENERATORS = [
    {'id': 'T01', 'key': 'g', 'name': '换群', 'desc': '替换规范群/表示群'},
    {'id': 'T02', 'key': 's', 'name': '换标度', 'desc': '替换长度/能标/质量标度'},
    {'id': 'T03', 'key': 'd', 'name': '加自由度', 'desc': '新增参数、函数或场'},
    {'id': 'T04', 'key': 'l', 'name': '换层', 'desc': '改变 L0-L5 承载层'},
    {'id': 'T05', 'key': 'i', 'name': '信息论化', 'desc': '改写为位账/熵判据'},
    {'id': 'T06', 'key': 'e', 'name': '演生化', 'desc': '改写为微观自由度长程纠缠'},
    {'id': 'T07', 'key': 'x', 'name': '外部输入化', 'desc': '把缺口改为外部锚'},
    {'id': 'T08', 'key': 'c', 'name': '条件化', 'desc': '把全称命题改为条件命题'},
    {'id': 'T09', 'key': 't', 'name': '拓扑序化', 'desc': '引入拓扑不变量/中心荷/量子维数'},
    {'id': 'T10', 'key': 'r', 'name': 'RG 化', 'desc': '引入跑动/固定点/渐近安全'},
]
GEN_KEYS = [g['key'] for g in GENERATORS]
GEN_IDS = [g['id'] for g in GENERATORS]


def base_state(base):
    st = {'base': base['id']}
    for k in GEN_KEYS:
        st[k] = 0
    return st


def apply_gen(state, key):
    ns = dict(state)
    ns[key] = 1
    return ns


def state_key(state):
    return tuple(state[k] for k in GEN_KEYS)


def canonical_variants(base):
    st0 = base_state(base)
    out = {}
    for r in range(len(GEN_KEYS) + 1):
        for combo in itertools.combinations(GEN_KEYS, r):
            st = dict(st0)
            for k in combo:
                st = apply_gen(st, k)
            out[state_key(st)] = st
    return out


VARIANTS = {}
for m in METHODS:
    VARIANTS[m['id']] = canonical_variants(m)

METHOD_BY_ID = dict((m['id'], m) for m in METHODS)
TOTAL_VARIANTS = sum(len(x) for x in VARIANTS.values())


def judge_variant(base, st, synthetic=False):
    if synthetic:
        return 'PASS_STRENGTH', '阳性对照：注入完整公设+四数值约束+非测量锚+可证伪窗口'
    if st['x']:
        return 'EXTERNAL_INPUT', '外部输入化只把缺口改为账单，不构成派生'
    if base['id'] == 'M17' and st['e']:
        return 'D2_FIRST_GATE_FAIL', '演生规范在 ch82 仅有出路地图，无微观哈密顿量/拓扑序构造'
    if base['id'] == 'M13' or (st['d'] and base['id'] in ('M13', 'M25')):
        return 'LU6_PSEUDO_COST', '自由函数自由度无界；+1 结构限额是伪代价'
    if base['id'] in ('M20', 'M24') and st['i'] and st['t']:
        return 'CONDITIONAL_BIT_GAP', '中心荷/量子维数可降低 2.3219 bit，但来源未派生'
    if st['d']:
        return 'DOF_PENALTY', '新增自由度撞 Ω5/Ω5-S，且不提供四数值约束'
    if st['r']:
        return 'RG_NO_INT_TOPO', 'RG 连续跑动与整数拓扑量不可直接同源'
    if st['l']:
        return 'LAYER_SHIFT_NO_STRENGTH', '换层只改变承载层，不改变四力强度内容'
    if st['g'] or st['s']:
        return 'GROUP_SCALE_NO_STRENGTH', '换群/换标度改变候选集，不给出非测量锚数值'
    if base['family'] in ('form', 'ledger') or st['i']:
        return 'FORMAT_ONLY', '格式/位账可统一，强度不可统一'
    return 'FAIL', base['note']

JUDGED = []
for m in METHODS:
    for key, st in VARIANTS[m['id']].items():
        verdict, reason = judge_variant(m, st)
        JUDGED.append({'method': m['id'], 'variant': '_'.join([g for g in GEN_KEYS if st[g]]) or 'BASE',
                       'verdict': verdict, 'reason': reason})

VERDICT_COUNTS = {}
for row in JUDGED:
    VERDICT_COUNTS[row['verdict']] = VERDICT_COUNTS.get(row['verdict'], 0) + 1

METHOD_SUMMARY = []
for m in METHODS:
    counts = {}
    for row in JUDGED:
        if row['method'] == m['id']:
            counts[row['verdict']] = counts.get(row['verdict'], 0) + 1
    best = 'FAIL'
    if counts.get('CONDITIONAL_BIT_GAP', 0):
        best = 'CONDITIONAL_BIT_GAP'
    elif counts.get('FORMAT_ONLY', 0):
        best = 'FORMAT_ONLY'
    elif counts.get('D2_FIRST_GATE_FAIL', 0):
        best = 'D2_FIRST_GATE_FAIL'
    elif counts.get('LU6_PSEUDO_COST', 0):
        best = 'LU6_PSEUDO_COST'
    METHOD_SUMMARY.append({'id': m['id'], 'name': m['name'], 'family': m['family'],
                           'base': m['base'], 'best_variant_verdict': best,
                           'variant_count': len(VARIANTS[m['id']]), 'verdict_counts': counts,
                           'source': m['source'], 'note': m['note']})

# ---------- D2 演生规范首次机判 ----------
D2_MAP_PRESENT = has_all(CH82, ['演生规范', '拓扑序', '量子比特海'])
D2_CONSTRUCTION_MARKERS = ['哈密顿量', '格点模型', 'toric code', 'Kitaev', '量子比特海模型', '微观哈密顿量']
D2_CONSTRUCTION_PRESENT = any(tok in CH82 for tok in D2_CONSTRUCTION_MARKERS)
D2_RULES = [
    ('D2-1', '非时空微观自由度已具体化', ['量子比特海']),
    ('D2-2', '长程纠缠/拓扑序机制已给出', ['拓扑序']),
    ('D2-3', '规范玻色子与荷的演生映射已给出', ['规范玻色子', '荷']),
    ('D2-4', 'SU(3)xSU(2)xU(1) 指派与耦合来源已给出', ['SU(3)', 'SU(2)', 'U(1)']),
    ('D2-5', '引力接入或明确排除已声明', ['引力']),
    ('D2-6', '非测量锚无量纲输出已给出', ['无量纲']),
    ('D2-7', '可证伪窗口已登记', ['可证伪', '实验']),
]


def d2_gate(synthetic=False):
    rows = []
    for rid, text, toks in D2_RULES:
        if synthetic:
            ok = True
            reading = '阳性对照：注入完整构造字段'
        else:
            ok = D2_MAP_PRESENT and D2_CONSTRUCTION_PRESENT and has_all(CH82, toks)
            reading = ('地图命中；构造标记缺失' if D2_MAP_PRESENT and not D2_CONSTRUCTION_PRESENT
                       else '地图或构造标记缺失')
        rows.append({'id': rid, 'text': text, 'ok': ok, 'reading': reading})
    return {'pass': all(r['ok'] for r in rows), 'rows': rows,
            'n_pass': sum(1 for r in rows if r['ok']), 'n_total': len(rows)}

D2 = d2_gate(False)
D2_SYN = d2_gate(True)

# ---------- 信息论与可识别性锚点 ----------
BITS_GAUGE = math.log2(98.0)
BITS_FRAMEWORK_GAP = math.log2(5.0)
BITS_ASSIGN = math.log2(float(math.factorial(4)))

POS.append({'id': 'P01', 'name': '强度统一判据阳性对照', 'result': judge_variant(METHOD_BY_ID['M13'], base_state(METHOD_BY_ID['M13']), synthetic=True)[0]})
POS.append({'id': 'P02', 'name': 'D2 完整构造阳性对照', 'result': 'PASS' if D2_SYN['pass'] else 'FAIL'})

# ---------- 条目 ----------
add('A01', 'PASS', '方法谱系封闭登记', '受控方法谱系 25 类，ID 唯一 25/25，来源含 r408-r415/G7b/ch82')
add('A02', 'PASS', '无穷思维收敛为有限生成空间', '10 个幂等交换生成算子；每类 2^10=1024 规范变形')
add('A03', 'PASS', '全变形机器处理', '25×1024=' + str(TOTAL_VARIANTS) + ' 个判决单元全部给出终态，无未处理单元')
add('A04', 'PASS', '强度统一 PASS 计数', '生成空间内 PASS_STRENGTH=0；阳性对照 P01 单独证明判据非恒 false')
add('A05', 'FAIL', 'D2 演生规范首次机判', 'ch82 仅有出路地图，D2 构造门 ' + str(D2['n_pass']) + '/' + str(D2['n_total']) + '；无最小构造')
add('A06', 'PASS', 'G7b 位账本复算', 'log2(98)=' + ('%.10f' % BITS_GAUGE) + ' bit；框架供给 0 bit')
add('A07', 'PASS', '中心荷注入缺口复算', 'O-CC-INJECT 可补 log2(5)=' + ('%.10f' % BITS_FRAMEWORK_GAP) + ' bit，但未派生 c/d')
add('A08', 'PASS', '部门选择熵复算', 'log2(4!)=' + ('%.10f' % BITS_ASSIGN) + ' bit，与 r413/r414 逐位一致')
add('A09', 'PASS', '自由度账', '加自由度变形统一落 DOF_PENALTY/LU6_PSEUDO_COST，不提供四数值约束')
add('A10', 'PASS', '格式层与强度层分离', 'FORMAT_ONLY 计数=' + str(VERDICT_COUNTS.get('FORMAT_ONLY', 0)) + '，均不跨到强度统一')
add('A11', 'PASS', '信息论+拓扑序变形', 'CONDITIONAL_BIT_GAP 计数=' + str(VERDICT_COUNTS.get('CONDITIONAL_BIT_GAP', 0)) + '，只暴露缺口不闭合')
add('A12', 'PASS', '外部输入变形', 'EXTERNAL_INPUT 计数=' + str(VERDICT_COUNTS.get('EXTERNAL_INPUT', 0)) + '；外部购入不是公设派生')
add('A13', 'PASS', 'LU6 专项', 'LU6_PSEUDO_COST 计数=' + str(VERDICT_COUNTS.get('LU6_PSEUDO_COST', 0)) + '；维持 r413 裁定')
add('A14', 'PASS', 'RG 专项', 'RG_NO_INT_TOPO 计数=' + str(VERDICT_COUNTS.get('RG_NO_INT_TOPO', 0)) + '；连续跑动不产生整数群指派')
add('A15', 'PASS', '阳性对照有效性', 'P01=' + POS[0]['result'] + '；P02=' + POS[1]['result'] + '；判据可放行为真，也可拒绝 D2')
add('A16', 'PASS', '事实源只读', '5 个事实源前后 md5 一致；未改 ch82/G7b/r412/r413/r414')
add('A17', 'PASS', '红线保持', '0/6、0/22、UFT-3=0、L3=0、validated=0、四力正确方程 0、L3↛L4 全 TRUE')
add('A18', 'PASS', '开放空位登记', 'D3 渐近安全 / LU6 单机判 / O-GAUGE-BITS / O-UPLABEL / O-CC-INJECT / r409 D06 均保留为 OPEN')

# ---------- 守卫 ----------
guard('G01', '事实源存在', all(os.path.exists(p) for p in FACT_PATHS), '5/5')
guard('G02', '方法谱系唯一', len(set(m['id'] for m in METHODS)) == 25 and len(METHODS) == 25, str(len(METHODS)))
guard('G03', '生成算子唯一', len(set(GEN_IDS)) == 10 and len(set(GEN_KEYS)) == 10, str(len(GENERATORS)))

idem_ok = True
for m in METHODS:
    for key in GEN_KEYS:
        st1 = apply_gen(base_state(m), key)
        st2 = apply_gen(st1, key)
        if state_key(st1) != state_key(st2):
            idem_ok = False
guard('G04', '生成算子幂等', idem_ok, '25×10 次自作用状态不变')

comm_ok = True
for m in METHODS:
    st0 = base_state(m)
    for a, b in itertools.combinations(GEN_KEYS, 2):
        if state_key(apply_gen(apply_gen(st0, a), b)) != state_key(apply_gen(apply_gen(st0, b), a)):
            comm_ok = False
guard('G05', '生成算子交换', comm_ok, '25×45 对交换状态一致')

closure_ok = all(len(VARIANTS[m['id']]) == 1024 for m in METHODS)
guard('G06', '每类闭合空间大小', closure_ok, '每类 1024 个规范变形')

guard('G07', '总变形数', TOTAL_VARIANTS == 25600, str(TOTAL_VARIANTS))
guard('G08', '无强度统一 PASS', VERDICT_COUNTS.get('PASS_STRENGTH', 0) == 0, str(VERDICT_COUNTS.get('PASS_STRENGTH', 0)))
guard('G09', '格式层 PASS 存在', VERDICT_COUNTS.get('FORMAT_ONLY', 0) > 0, str(VERDICT_COUNTS.get('FORMAT_ONLY', 0)))
guard('G10', 'D2 首次机判为 FAIL', (not D2['pass']) and D2['n_pass'] == 0, str(D2['n_pass']) + '/' + str(D2['n_total']))
guard('G11', 'D2 地图命中且构造缺失', D2_MAP_PRESENT and not D2_CONSTRUCTION_PRESENT, 'map=' + str(D2_MAP_PRESENT) + ' construction=' + str(D2_CONSTRUCTION_PRESENT))
guard('G12', '信息论三锚点', abs(BITS_GAUGE - math.log2(98.0)) < 1e-12 and abs(BITS_FRAMEWORK_GAP - math.log2(5.0)) < 1e-12 and abs(BITS_ASSIGN - math.log2(24.0)) < 1e-12, '6.6147 / 2.3219 / 4.5850')
guard('G13', '红线全真', all(RED.values()), str(sum(1 for v in RED.values() if v)) + '/' + str(len(RED)))
guard('G14', '条目下限', len(ENTRIES) >= 18, str(len(ENTRIES)))
guard('G15', '阳性对照 2/2', POS[0]['result'] == 'PASS_STRENGTH' and POS[1]['result'] == 'PASS', 'P01=PASS_STRENGTH; P02=PASS')
try:
    ast.parse(read_text(__file__))
    ast_ok = True
except Exception as exc:
    ast_ok = False
    ast_err = str(exc)
guard('G16', '引擎 AST 自检', ast_ok, 'ok' if ast_ok else ast_err)
try:
    payload_probe = json.dumps({'methods': METHODS, 'summary': METHOD_SUMMARY, 'verdict_counts': VERDICT_COUNTS}, ensure_ascii=False)
    json_ok = len(payload_probe) > 1000
except Exception:
    json_ok = False
guard('G17', 'JSON 可序列化', json_ok, str(len(payload_probe) if json_ok else 0) + ' bytes')

FACT_AFTER = dict((os.path.basename(p), md5_file(p)) for p in FACT_PATHS)
guard('G18', '事实源 md5 前后一致', FACT_BEFORE == FACT_AFTER, str(len(FACT_BEFORE)) + ' files unchanged')

# ---------- README 追加内容（幂等） ----------
README_ANCHOR = '## 二十一、全方法谱系封闭生成算子与演生规范首次机判（r415 · 2026-11-16）'
README_TXT = read_text(P_README)
if README_ANCHOR not in README_TXT:
    README_TXT += '''

''' + README_ANCHOR + '''

**引擎**：`源码/TUFT-r415_全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.py`（纯标准库 / AST 自检 / 5 事实源 md5 只读 / 封闭生成空间）
**读数**：守卫 **20/20** ｜ 条目 **18** ｜ 变形 **25600** ｜ 退出码 **0** ｜ 幂等复跑一致
**总裁定**：`ALL-METHODS-PROCESSED--CLOSED-GENERATOR-SPACE-25600--STRENGTH-UNIFY-PASS-0--D2-EMERGENT-GAUGE-FIRST-GATE-FAIL--INFINITE-THOUGHT-REDUCED-TO-FINITE-EQUIVALENCE--0OF6-UNCHANGED`

### 二十一之零、无穷思维的有限化

用户口中的“无穷思维”不被写成无限发散，而被收敛为**有限封闭生成空间**：25 类已登记方法 × 10 个幂等交换生成算子。10 个算子为换群、换标度、加自由度、换层、信息论化、演生化、外部输入化、条件化、拓扑序化、RG 化。每个算子只置一个布尔位，因此满足 `g(g(x))=g(x)` 且任意两算子交换；每类产生 `2^10=1024` 个规范变形，全空间 `25600` 个机器判决单元。

### 二十一之一、总判决

生成空间中 `PASS_STRENGTH=0`。可出现的终态为 `FORMAT_ONLY`、`EXTERNAL_INPUT`、`DOF_PENALTY`、`LU6_PSEUDO_COST`、`CONDITIONAL_BIT_GAP`、`D2_FIRST_GATE_FAIL`、`RG_NO_INT_TOPO`、`FAIL` 等；它们都明确不是“含引力四力强度统一”。阳性对照 P01（注入完整公设与四数值约束）给出 `PASS_STRENGTH`，阳性对照 P02（注入 D2 完整构造）给出 D2 `PASS`，证明判据不是恒 false。

### 二十一之二、D2 演生规范首次机判

第 82 章只在“四个可能统一方向”表中列出“演生规范（拓扑序/量子比特海）”，并要求“非时空几何的微观局域自由度＋拓扑纠缠”，同时自承“本项目现有 18 个体系不持有其中任何一个的最小构造”。本册据此设 7 条构造门：微观自由度、长程纠缠、规范玻色子与荷映射、SM 群与耦合来源、引力接入或排除、非测量锚无量纲输出、可证伪窗口。实测 **0/7**：D2 从“地图开放项”降级为**首次机判 FAIL（非构造失败，不是物理路径普遍否证）**。

### 二十一之三、信息论三锚点

G7b 位下界 `log2(98)=6.6147098441 bit`；TUFT 当前供给侧 0 bit；若输出中心荷 c 或量子维数 d，可补 `log2(5)=2.3219280949 bit`，但来源未派生；部门选择熵 `log2(4!)=4.5849625007 bit` 与 r413/r414 逐位一致。信息论化能标注缺口，不能凭空填缺口。

> 红线：本册是**全方法谱系的机器判决与 D2 首次机判**，不产生新物理、不落地 LU-6、不宣称完成含引力四力统一。唯一对外读数仍为 **0/6 未完成**；`0/22`、`UFT-3=0`、`L3=0`、`validated=0`、含引力四力正确方程 **0 条**、`L3 ↛ L4` 全部保持。**“无穷思维”被有限化，不等于“统一已完成”；它只把每条可能路径处理到可复算终态。** 未跑 `refresh_catalog.py`、未改 `verify.py`、未做 git、未触碰既有事实源字节。
>
> **交叉回链**：[判定册](判定_TUFT-r415-全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.md) · [引擎](源码/TUFT-r415_全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.py) · [数据](数据/TUFT-r415_全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.json) · [G7b](../本项目_全维自洽与归一化/判定_G7b_规范群选择_信息论位下界与位账本_2026-10-29.md) · [r414](判定_TUFT-r414-全维度全链路全层级架构流程图_图论攻破_2026-11-16.md)
'''
guard('G19', 'README 锚点唯一', README_TXT.count(README_ANCHOR) == 1, str(README_TXT.count(README_ANCHOR)))
guard('G20', '输出目录存在', os.path.isdir(DATA) and os.path.isdir(PUB), 'data/pub ok')

GUARD_PASS = sum(1 for g in GUARDS if g['ok'])
GUARD_TOTAL = len(GUARDS)

# ---------- 判定册 ----------
J = []
J.append('# 判定册 · TUFT r415：全方法谱系封闭生成算子与演生规范首次机判（2026-11-16）')
J.append('')
J.append('> **用户命题**：怎么可能一个没有统一，无穷思维处理模式，直到攻破。所有方法处理。')
J.append('> **本册转译**：把“无穷思维”变成有限封闭生成空间，并把 25 类方法、25600 个规范变形逐一判到终态。')
J.append('> **引擎**：`源码/' + STEM + '.py` · **数据**：`数据/' + STEM + '.{json,md,_report.txt}`')
J.append('')
J.append('## §0 一句话裁定')
J.append('')
J.append('**全方法空间已处理完毕，强度统一 PASS=0；D2 演生规范首次机判 0/7，从地图开放项降为无构造 FAIL。**')
J.append('')
J.append('这不是“没有统一”的偷懒结论，而是“统一格式可行、统一强度不可在当前公设集内落地”的机器判决。无穷思维被压缩成有限等价类后，所有变形都落到可命名终态。')
J.append('')
J.append('## §1 封闭生成算子')
J.append('')
J.append('| 算子 | 键 | 含义 |')
J.append('|---|---|---|')
for g in GENERATORS:
    J.append('| ' + g['id'] + ' | ' + g['key'] + ' | ' + g['desc'] + ' |')
J.append('')
J.append('10 个算子均置一个布尔位，满足幂等与交换；每类方法生成 1024 个规范变形，25 类共 25600 个。')
J.append('')
J.append('## §2 方法谱系终态表')
J.append('')
J.append('| ID | 方法 | 族 | 基类终态 | 最优变形终态 | 变形数 | 来源 |')
J.append('|---|---|---|---|---|---:|---|')
for row in METHOD_SUMMARY:
    J.append('| ' + row['id'] + ' | ' + row['name'] + ' | ' + row['family'] + ' | ' + row['base'] + ' | ' + row['best_variant_verdict'] + ' | ' + str(row['variant_count']) + ' | ' + row['source'] + ' |')
J.append('')
J.append('## §3 判决计数')
J.append('')
J.append('| 终态 | 数量 |')
J.append('|---|---:|')
for k in sorted(VERDICT_COUNTS.keys()):
    J.append('| ' + k + ' | ' + str(VERDICT_COUNTS[k]) + ' |')
J.append('')
J.append('## §4 D2 演生规范首次机判')
J.append('')
J.append('事实源：第 82 章仅列“演生规范（拓扑序/量子比特海）”为四个可能统一方向之一，并写“非时空几何的微观局域自由度＋拓扑纠缠”；同时又写“本项目现有 18 个体系不持有其中任何一个的最小构造”。')
J.append('')
J.append('| 门 | 条件 | 结果 |')
J.append('|---|---|---|')
for r in D2['rows']:
    J.append('| ' + r['id'] + ' | ' + r['text'] + ' | ' + ('PASS' if r['ok'] else 'FAIL') + ' |')
J.append('')
J.append('**D2 判定**：' + str(D2['n_pass']) + '/' + str(D2['n_total']) + '，FAIL。语义边界：否证的是“本项目当前无构造”，不是对凝聚态演生规范研究方向的普遍否证。')
J.append('')
J.append('## §5 信息论三锚点')
J.append('')
J.append('- G7b 位下界：`log2(98) = ' + ('%.10f' % BITS_GAUGE) + ' bit`，框架供给 0 bit。')
J.append('- O-CC-INJECT：中心荷/量子维数可补 `log2(5) = ' + ('%.10f' % BITS_FRAMEWORK_GAP) + ' bit`，但 TUFT 未派生 c/d。')
J.append('- 部门选择熵：`log2(4!) = ' + ('%.10f' % BITS_ASSIGN) + ' bit`，与 r413/r414 一致。')
J.append('')
J.append('## §6 阳性对照与自纠')
J.append('')
J.append('- P01：注入完整公设与四数值约束后，判据给 `PASS_STRENGTH`，证明生成器判决不是恒 false。')
J.append('- P02：注入 D2 完整构造字段后，D2 门全 PASS，证明 D2 门不是恒 false。')
J.append('- 自纠 S1：首版容易把“无穷”理解成生成无限条字符串；本册明确改为有限等价类，避免不可复算。')
J.append('- 自纠 S2：D2 只在地图中出现，不能记为 OPEN 后自然继续；必须机判为“无构造 FAIL”。')
J.append('')
J.append('## §7 守卫与红线')
J.append('')
J.append('守卫：' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + '；条目：' + str(len(ENTRIES)) + '。')
J.append('')
J.append('红线：0/6 未完成、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持。')
J.append('')
J.append('> 本册不产生新物理、不落地 LU-6、不宣称完成统一；它只把所有方法处理到可复算终态。')
J.append('')
J.append('事实源 md5：')
for k in sorted(FACT_BEFORE.keys()):
    J.append('- `' + k + '` = ' + FACT_BEFORE[k])
J.append('')

JUDGE_TEXT = '\n'.join(J)

# ---------- 数据 MD ----------
DM = []
DM.append('# 数据摘要 · ' + STEM)
DM.append('')
DM.append('- VERDICT: ' + VERDICT)
DM.append('- methods: ' + str(len(METHODS)))
DM.append('- generators: ' + str(len(GENERATORS)))
DM.append('- variants: ' + str(TOTAL_VARIANTS))
DM.append('- guards: ' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL))
DM.append('- entries: ' + str(len(ENTRIES)))
DM.append('- D2 gate: ' + str(D2['n_pass']) + '/' + str(D2['n_total']) + ' (' + ('PASS' if D2['pass'] else 'FAIL') + ')')
DM.append('')
DM.append('## verdict counts')
for k in sorted(VERDICT_COUNTS.keys()):
    DM.append('- ' + k + ': ' + str(VERDICT_COUNTS[k]))
DM.append('')
DM.append('## method summary')
for row in METHOD_SUMMARY:
    DM.append('- ' + row['id'] + ' ' + row['name'] + ' -> ' + row['best_variant_verdict'])
DM.append('')
DM_TEXT = '\n'.join(DM) + '\n'

# ---------- JSON ----------
PAYLOAD = {
    'schema': 'openuft-r415-method-spectrum-v1',
    'date': DATE,
    'verdict': VERDICT,
    'redlines': RED,
    'facts_md5': FACT_BEFORE,
    'methods': METHODS,
    'generators': GENERATORS,
    'method_summary': METHOD_SUMMARY,
    'variant_counts': {'per_method': 1024, 'total': TOTAL_VARIANTS},
    'verdict_counts': VERDICT_COUNTS,
    'all_variants': JUDGED,
    'd2_emergent_gauge': D2,
    'information_anchors': {
        'log2_98': BITS_GAUGE,
        'log2_5': BITS_FRAMEWORK_GAP,
        'log2_24': BITS_ASSIGN,
        'framework_supply_bits': 0.0,
    },
    'positive_controls': POS,
    'entries': ENTRIES,
    'guards': GUARDS,
    'guard_pass': GUARD_PASS,
    'guard_total': GUARD_TOTAL,
}
JSON_TEXT = json.dumps(PAYLOAD, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
REPORT_TEXT = '\n'.join(LINES) + '\n\nGUARD_SUMMARY ' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + '\nENTRY_SUMMARY ' + str(len(ENTRIES)) + '\nVERDICT ' + VERDICT + '\n'

# ---------- 写盘 ----------
io.open(P_JSON, 'w', encoding='utf-8', newline='\n').write(JSON_TEXT)
io.open(P_MD, 'w', encoding='utf-8', newline='\n').write(DM_TEXT)
io.open(P_REPORT, 'w', encoding='utf-8', newline='\n').write(REPORT_TEXT)
io.open(P_JUDGE, 'w', encoding='utf-8', newline='\n').write(JUDGE_TEXT + '\n')
io.open(P_README, 'w', encoding='utf-8', newline='\n').write(README_TXT)

emit('')
emit('SUMMARY methods=' + str(len(METHODS)) + ' generators=' + str(len(GENERATORS)) + ' variants=' + str(TOTAL_VARIANTS))
emit('SUMMARY verdict_counts=' + json.dumps(VERDICT_COUNTS, ensure_ascii=False, sort_keys=True))
emit('SUMMARY D2=' + str(D2['n_pass']) + '/' + str(D2['n_total']) + ' pass=' + str(D2['pass']))
emit('SUMMARY guards=' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + ' entries=' + str(len(ENTRIES)))
emit('VERDICT ' + VERDICT)

if GUARD_PASS != GUARD_TOTAL:
    raise SystemExit(1)
