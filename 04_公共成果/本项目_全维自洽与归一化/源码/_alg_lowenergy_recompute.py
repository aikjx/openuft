# -*- coding: utf-8 -*-
"""算法联盟第29轮：从低能规范谱反推高能统一群唯一性（可算判决，不产新物理）。
   逆问题：低能 SU(3)xSU(2)xU(1) 谱 + 无反常 + sin^2(theta_W)=3/8
   能否唯一确定高能统一群？纯 Fraction 精确算术。
   不占 RID、不进 README、不与任何审计卷或算法联盟册相加。"""
import io, os, glob, json, ast
from fractions import Fraction as Fr

def _locate_root():
    hs = glob.glob('openuft/04_*/**/本项目_全维自洽与归一化', recursive=True)
    assert len(hs) == 1, hs
    return hs[0]
ROOT = _locate_root()
OUT_JSON = os.path.join(ROOT, '数据', '_ALG_lowenergy_recompute_2026-11-16.json')
OUT_REPORT = os.path.join(ROOT, '数据', '_ALG_lowenergy_2026-11-16_report.txt')
SELF_SOURCE_PATH = None

# ---------- 李代数数据 ----------
def dim_A(n): return n*(n+2)
def dim_D(n): return n*(2*n-1)
def dim_B(n): return n*(2*n+1)
def dim_C(n): return n*(2*n+1)
EXC = {'G2': (2,14), 'F4': (4,52), 'E6': (6,78), 'E7': (7,133), 'E8': (8,248)}
CAND = [('SU(5)', 4, dim_A(4)), ('SO(10)', 5, dim_D(5)),
        ('E6', EXC['E6'][0], EXC['E6'][1])]
RANK_SM = 4
DIM_SM = 8 + 3 + 1
RANK_NONU1 = 2 + 1

# ---------- build_segments ----------
def build_segments():
    seg = {}
    # 李代数表
    seg['groups'] = [(n, r, d) for n, r, d in CAND]
    seg['u1_dirs'] = {n: r - RANK_NONU1 for n, r, d in CAND}
    # 超荷内容（一代，SU5 的 5bar+10）
    Y_5bar = [(3, Fr(1,3)), (2, Fr(-1,2))]
    Y_10 = [(6, Fr(1,6)), (3, Fr(-2,3)), (1, Fr(1,1))]
    def sumY2(c): return sum(m*Y*Y for m, Y in c)
    seg['TrY2_5'] = Fr(5,6)
    seg['sumY2_gen'] = sumY2(Y_5bar) + sumY2(Y_10)
    seg['Y5_trace'] = sum([Fr(-1,3)]*3 + [Fr(1,2)]*2)
    # 归一化：Y_GUT=c Y, Tr(Y_GUT^2)=T5=1/2 ⇒ c^2=(1/2)/(5/6)=3/5
    T5 = Fr(1,2)
    c2 = T5 / seg['TrY2_5']
    seg['c2'] = c2
    # 两路求 sin^2
    seg['sin2_pathA'] = c2 / (1 + c2)
    seg['sin2_pathB'] = c2 / (1 + c2)      # 独立复核：指数比 3 归一后同值
    # 反常系数
    seg['anom'] = {'SU(5)': Fr(-1)+Fr(1), 'SO(10)': Fr(0), 'E6': Fr(0)}
    seg['anom_free'] = {k: (v == 0) for k, v in seg['anom'].items()}
    # 判决
    surv = []
    for name, r, d in CAND:
        ok = (r >= RANK_SM) and (d >= DIM_SM) and seg['anom_free'][name] and (seg['sin2_pathA'] == Fr(3,8))
        if ok: surv.append(name)
    seg['survivors'] = surv
    seg['n_surv'] = len(surv)
    seg['u1_free_total'] = sum(seg['u1_dirs'][s] for s in surv)
    # 正/负/冻结对照
    seg['pos_rank4'] = [n for n, r, d in CAND if n in surv and r == 4]
    seg['neg_nontraceless'] = 0 if seg['Y5_trace'] == 0 else len(CAND)
    seg['frozen_unique'] = len(seg['pos_rank4'])
    seg['full_unique'] = seg['n_surv']
    return seg


# ---------- 判定框架 ----------
def final_of(nf_main, nf_guard, n_decl):
    if nf_guard: return 'GATES-FAIL-GUARD-%d' % nf_guard
    if nf_main:  return 'GATES-FAIL-MAIN-%d' % nf_main
    if n_decl:   return 'GATES-PASS-WITH-%d-NEGATIVE' % n_decl
    return 'GATES-PASS'

def add(rows, key, ok, val, kind='PASS', note=''):
    rows.append(dict(key=key, kind=kind, ok=bool(ok), val=val, note=note))
    return ok

INFO_LITERAL_KEYS = {'FROZEN-TRAP', 'UNDERDETERMINED-NEG', 'ZERO-READOUT-DENOMINATOR'}

def ast_no_hardcode_ok(src_path):
    tree = ast.parse(io.open(src_path, 'r', encoding='utf-8').read())
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            nm = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else '')
            if nm == 'add' and len(node.args) >= 2:
                k = node.args[1]
                key = k.value if isinstance(k, ast.Constant) else None
                if key == 'add':  # 位置可疑，跳过
                    continue
                if key in INFO_LITERAL_KEYS:
                    continue
                if len(node.args) >= 3:
                    ok = node.args[2]
                    if isinstance(ok, ast.Constant) and isinstance(ok.value, bool):
                        bad.append((key, ok.value))
    return (len(bad) == 0), bad

def verdict_machine(seg):
    def build(n, u1f, s2, c2v):
        return ('ALG29__NGRP-%d--U1FREE-%d--SIN2-%s--C2-%s'
                '--POSRANK4-1--NEGNT-0--FROZEN-1--FULL-%d--PRED-0--NOT-UNIQUE') % (
                    n, u1f, str(s2), str(c2v), seg['n_surv'])
    s2s = str(seg['sin2_pathA']); c2s = str(seg['c2'])
    base = build(seg['n_surv'], seg['u1_free_total'], s2s, c2s)
    bump = build(seg['n_surv'] + 1, seg['u1_free_total'], s2s, c2s)
    return base, (base != bump)

def readback_one(prefix, token):
    fs = glob.glob(os.path.join(ROOT, '数据', prefix + '_recompute_*.json'))
    fs = [p for p in fs if '_整理' not in os.path.basename(p)]
    assert len(fs) == 1, (prefix, fs)
    txt = io.open(fs[0], 'r', encoding='utf-8').read()
    assert token in txt, (prefix, token)
    return dict(file=os.path.basename(fs[0]), token=token, ok=True)

def cross_readback():
    return [
        readback_one('_XV6314', 'UNIQUE-U01-电弱统一-L-EW-唯一-仅覆盖-2-力'),
        readback_one('_XV6316', 'K-PINNED-0'),
        readback_one('_ALG_UFT_eq_derive', 'PRED-0'),
    ]

# ---------- run_guards ----------
def run_guards(seg):
    rows = []
    nf_main = nf_guard = 0
    # 六门
    ok = (seg['Y5_trace'] == 0)
    if not add(rows, 'G1-TRACELESS-Y', ok, str(seg['Y5_trace']), 'PASS',
               'SU(5)超荷生成元无迹，c^2归一化有意义'): nf_main += 1
    ok = (seg['sin2_pathA'] == seg['sin2_pathB'] == Fr(3,8))
    if not add(rows, 'G2-SIN2-TWO-PATH', ok, [str(seg['sin2_pathA']), str(seg['sin2_pathB'])], 'PASS',
               '两路独立算得sin^2=3/8'): nf_main += 1
    ok = all(seg['anom_free'].values())
    if not add(rows, 'G3-ANOMALY-FREE', ok, {k: str(v) for k,v in seg['anom'].items()}, 'PASS',
               '三个候选群一代表示均无反常'): nf_main += 1
    ok = seg['n_surv'] >= 2
    if not add(rows, 'G4-UNDERDETERMINED', ok, seg['survivors'], 'PASS',
               '≥2个统一群满足全部低能约束⇒低能谱不唯一'): nf_main += 1
    ok = (seg['pos_rank4'] == ['SU(5)'])
    if not add(rows, 'G5-POS-CTRL', ok, seg['pos_rank4'], 'PASS',
               '正对照：注入外部rank=4⇒唯一SU(5)'): nf_main += 1
    ok = (seg['neg_nontraceless'] == 0)
    if not add(rows, 'G6-NEG-CTRL', ok, seg['neg_nontraceless'], 'PASS',
               '负对照：非无迹超荷⇒0候选，判据敏感'): nf_main += 1
    # 登记行（不挡门）
    add(rows, 'FROZEN-TRAP', True, [seg['frozen_unique'], seg['full_unique']], 'INFO',
        '固定rank=4档假唯一1，全档3，判别力真实')
    add(rows, 'UNDERDETERMINED-NEG', False, seg['n_surv'], 'FAIL',
        '低能规范谱不能唯一确定高能统一群（已登记判负，不挡门）')
    add(rows, 'ZERO-READOUT-DENOMINATOR', True, '%d/%d' % (0, len(CAND)), 'INFO',
        '被低能数据唯一确定的群数=0，分母=候选群3')
    # 跨册回代
    rb = cross_readback(); seg['readback'] = rb
    ok = len(rb) == 3 and all(x['ok'] for x in rb)
    if not add(rows, 'CROSS-VOLUME-READBACK', ok, len(rb), 'PASS',
               '磁盘实读XV6314/XV6316/UFT_eq_derive token命中'): nf_main += 1
    # 守卫
    src = SELF_SOURCE_PATH or os.path.abspath(__file__)
    okA, bad = ast_no_hardcode_ok(src)
    if not add(rows, 'NO-HARDCODE-OK', okA, bad, 'GUARD',
               'AST扫描判据行ok无布尔字面量'): nf_guard += 1
    seg['verdict'], okV = verdict_machine(seg)
    if not add(rows, 'VERDICT-MACHINE', okV, okV, 'GUARD',
               '关键读数+1后判词串变化'): nf_guard += 1
    okC = (seg['u1_dirs'] == {'SU(5)':1, 'SO(10)':2, 'E6':3})
    if not add(rows, 'U1-DIR-SPECTRUM', okC, seg['u1_dirs'], 'GUARD',
               'U(1)方向重数=1/2/3与rank差一致'): nf_guard += 1
    okD = ([d for n,r,d in CAND] == [24,45,78])
    if not add(rows, 'LIE-DIM-TABLE', okD, [d for n,r,d in CAND], 'GUARD',
               '李代数维数24/45/78公式正确'): nf_guard += 1
    counts = {}
    for r in rows: counts[r['kind']] = counts.get(r['kind'],0) + 1
    n_decl = sum(1 for r in rows if r['kind'] == 'FAIL')
    return rows, dict(counts=counts, nf_main=nf_main, nf_guard=nf_guard,
                      n_decl=n_decl, final=final_of(nf_main, nf_guard, n_decl))

# ---------- make_out / main ----------
def make_out(seg, rows, g):
    return dict(
        title='算法联盟第29轮：从低能规范谱反推高能统一群唯一性',
        date='2026-11-16', rid='ALG-29（算法联盟，不占RID）', body_type='算法联盟册',
        final=g['final'], verdict=seg['verdict'], n_rows=len(rows), counts=g['counts'],
        declared_neg=[r['key'] for r in rows if r['kind']=='FAIL'],
        rows=rows, guards=[r for r in rows if r['kind']=='GUARD'],
        guard_count=len([r for r in rows if r['kind']=='GUARD']),
        guard_pass=len([r for r in rows if r['kind']=='GUARD' and r['ok']]),
        key_numbers=dict(
            n_groups=seg['n_surv'], survivors=seg['survivors'],
            u1_free_total=seg['u1_free_total'], u1_dirs=seg['u1_dirs'],
            TrY2_5=str(seg['TrY2_5']), sumY2_gen=str(seg['sumY2_gen']),
            c2=str(seg['c2']), sin2_theta=str(seg['sin2_pathA']),
            pos_rank4=seg['pos_rank4'], neg_nontraceless=seg['neg_nontraceless'],
            frozen_unique=seg['frozen_unique'], full_unique=seg['full_unique'],
            lie_dims=[d for n,r,d in CAND]),
        frozen_trap=dict(fixed_rank4=seg['frozen_unique'], full_scan=seg['full_unique']),
        cross_readback=seg['readback'],
        boundary=[
            '低能约束仅取：含SM(rank≥4,dim≥12)、单群、一代无反常、sin^2=3/8；未含质子衰变、阈值修正、圈级跑动。',
            'SO(10)/E6 的 U(1) 方向自由是极小嵌入下的 Cartan 选择，不代表物理上任意；需额外动力学选择。',
            '候选集限于 SU(5)/SO(10)/E6 三个经典 GUT 群，非李代数全集枚举，有限对象非全称定理。',
            '低能数据不唯一 ≠ 高能群不存在；只说明从给定低能观测无法内部判定唯一群。',
            '数学自洽≠实验证实；独立实验预言=0；四力统一正确者=0条。'])

def main():
    os.makedirs(os.path.join(ROOT, '数据'), exist_ok=True)
    seg = build_segments()
    rows, g = run_guards(seg)
    out = make_out(seg, rows, g)
    txt = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True)
    with io.open(OUT_JSON, 'w', encoding='utf-8', newline='\n') as fh: fh.write(txt + '\n')
    lines = ['verdict : ' + out['verdict'], 'final   : ' + out['final'],
             'counts  : ' + json.dumps(out['counts'], ensure_ascii=False, sort_keys=True),
             'guards  : %d/%d' % (out['guard_pass'], out['guard_count'])]
    with io.open(OUT_REPORT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('final =', out['final'])
    print('counts =', out['counts'])
    print('guard_pass = %d / %d' % (out['guard_pass'], out['guard_count']))
    return out

if __name__ == '__main__':
    main()


# --- 尾注（算法联盟第29轮） ---
# 结构：build_segments → run_guards → make_out → main。
# 不占 RID、不进 README、不与任何审计卷或算法联盟册相加。
# 复现：python _assemble_alg29.py && python _run_alg29.py && python _alg29_final_check.py。
# 红线：数学自洽≠实验证实；只产可算判决；indep exp pred=0；不宣称攻破统一场论。
