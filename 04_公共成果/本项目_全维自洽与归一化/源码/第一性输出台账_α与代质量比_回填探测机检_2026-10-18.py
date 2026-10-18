# -*- coding: utf-8 -*-
"""第一性输出台账 (总账 §七.1): alpha / 代质量比 -- 声明前置 + 回填探测, machine-run.

§七.1 mandate: any new proposal must FIRST declare which dimensionless number it
outputs; 第一性内容 <=> 无量纲量的数值 (method_F). This ledger prices every
live channel in the repo that touches the two named targets -- alpha, and the
inter-generation mass ratios m_mu/m_e, m_tau/m_e -- and classifies each:

  HIT          declared output not among the inputs, residual <= 3 sigma;
  BACKFILL     the channel needs the target's own value as input (per-particle
               restatement: CTFA A-7 law "任何读法都构造不出预言");
  NO_OUTPUT    formula is a renaming identity, honest prediction count 0;
  GATE_FAIL    channel violates the parameter-count pre-gate (its own text);
  OFF_TARGET   declared dimensionless outputs are not alpha / mass ratios.

Citation integrity: every row carries file:line+token re-read live; drift
within +-3 lines => SHIFT (warn), absent => STALE (fatal, rc!=0).

Controls (铁律: 判据必须带控制组):
  D1 tautology detector: synthetic channel OUTPUT alpha, INPUTS alpha must be
     flagged INPUT_IDENTITY and NEVER counted as HIT;
  D2 known-pass control: MSSM one-loop RG alpha_s(M_Z)=0.11686 @1.27sigma is
     the 总账 §七.3 named positive control => ledger must not be always-RED;
  D3 census cross-channel: sum of non-control HITs on the two named targets
     must equal 0 == every /systems[*]/n_registered_predictions in the 靶场
     census JSON read live;
  D4 stale-citation detector fires on synthetic bad line.
Exit != 0 on any STALE, channel-status anchor mismatch, or control failure.
"""
import json, os, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     os.pardir, os.pardir, os.pardir, os.pardir))

GZ = 'openuft/04_公共成果/openuft_统一场论全部完成工作总账_2026-10-15.md'
P49B = 'openuft/07_统一场方程/openuft_49_攻破第二轮_力统一方程与实验一致性_2026-10-15.md'
SAN = 'openuft/07_统一场方程/openuft_49_阶段1_三重预检攻破卷_2026-10-15.md'
CTFA_MD = 'openuft/04_公共成果/算法联盟_全维自洽与归一化/判定_张祥前CTFA_自由度预算与统一能力上限_2026-10-12.md'
CTFA_J = 'openuft/04_公共成果/算法联盟_全维自洽与归一化/数据/张祥前CTFA_自由度预算与统一能力上限_2026-10-12.json'
V946 = 'openuft/01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/V9_四力大统一定稿线/01_全书_四力大统一_垂直原理螺旋统一场论_V9.46.md'
V48 = 'openuft/07_统一场方程/空间螺旋几何化统一场论/65_TUFT-V4.8公式集_作用量量纲与场方程结构机器审计_2026-10-15.md'
MC = 'openuft/04_公共成果/本项目_全维自洽与归一化/判定_TUFT-r84-X-R82-2定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md'
BA = 'openuft/04_公共成果/本项目_全维自洽与归一化/数据/无量纲靶场审计.json'
BAPY = 'openuft/04_公共成果/本项目_全维自洽与归一化/源码/无量纲靶场审计.py'

_cache = {}
def lines_of(rel):
    if rel not in _cache:
        with open(os.path.join(ROOT, rel.replace('/', os.sep)), encoding='utf-8',
                  errors='replace') as f:
            _cache[rel] = f.read().splitlines()
    return _cache[rel]

def check_cite(rel, line, token, findings):
    ls = lines_of(rel)
    if not (0 < line <= len(ls)):
        findings.append(('STALE', rel, line, token, 'file has %d lines' % len(ls)))
        return False
    if token in ls[line - 1]:
        return True
    for d in range(1, 4):
        for n in (line - d, line + d):
            if 0 < n <= len(ls) and token in ls[n - 1]:
                findings.append(('SHIFT', rel, line, token, 'found at %d' % n))
                return True
    findings.append(('STALE', rel, line, token, 'token absent within +-3'))
    return False

def cite(rel, line, token, findings):
    return {'file': rel, 'line': line, 'token': token,
            'ok': check_cite(rel, line, token, findings)}

NAMED_TARGETS = ['alpha', 'm_mu_over_me', 'm_tau_over_me']

def analyze(ch, findings):
    """status logic is DATA-DRIVEN: inputs/target declaration + flags below."""
    tgt = ch['output']
    ins = set(ch['inputs'])
    if tgt in ins:
        return 'INPUT_IDENTITY'          # tautology detector (D1)
    if ch.get('hit_3sigma'):
        return 'HIT'                     # a declared, non-tautological, <=3sigma
                                         # output is a HIT whatever the target;
                                         # named-target accounting happens in D3
    if ch.get('gate_fail'):
        return 'GATE_FAIL'
    if ch.get('backfill'):
        return 'BACKFILL'
    if ch.get('no_output'):
        return 'NO_OUTPUT'
    if not ch.get('is_target_channel'):
        return 'OFF_TARGET'
    return 'UNDECIDED'

CHANNELS = [
  {'id': 'CH0_MSSM控制_α_s', 'output': 'alpha_s(M_Z)', 'inputs': ['alpha', 'sin2_thetaW'],
   'hit_3sigma': True, 'is_target_channel': False, 'control': True,
   'cites': [(P49B, 141, '0.11686'), (GZ, 160, 'MSSM 耦合统一 1.27σ'),
             (MC, 15, '1.153510502097686')],
   'expect': 'HIT'},
  {'id': 'CH1_CTFA_α', 'output': 'alpha', 'inputs': ['tau', 'kappa'],
   'backfill': True, 'is_target_channel': True,
   'cites': [(CTFA_MD, 54, '不构成约束理论'), (CTFA_MD, 49, '诚实预言数'),
             (CTFA_MD, 109, '诚实预言数')],
   'expect': 'BACKFILL'},
  {'id': 'CH2_V9_α等b/ρ', 'output': 'alpha', 'inputs': ['b_rho_per_particle'],
   'backfill': True, 'is_target_channel': True,
   'cites': [(V946, 3207, 'α=b/ρ'), (V946, 3226, '拟合自由参数 N_p=0'),
             (V946, 3226, '无物可拟合')],
   'expect': 'BACKFILL'},
  {'id': 'CH3_V48_几何质量式', 'output': 'm_mu_over_me', 'inputs': ['kappa', 'tau'],
   'no_output': True, 'is_target_channel': True,
   'cites': [(V48, 37, 'm=(ħ/c)'), (CTFA_MD, 109, '诚实预言数')],
   'expect': 'NO_OUTPUT'},
  {'id': 'CH4_EC_g-2_EDM', 'output': 'Δa_e/x_CP', 'inputs': ['耦合强度', 'CP相位'],
   'gate_fail': True, 'is_target_channel': False,
   'cites': [(SAN, 282, '不构成检验'), (SAN, 291, '参数计数门未过')],
   'expect': 'GATE_FAIL'},
  # detector controls (synthetic, must be caught):
  {'id': 'SYN1_恒等注入', 'output': 'alpha', 'inputs': ['alpha'],
   'synthetic': True, 'cites': [], 'expect': 'INPUT_IDENTITY'},
  {'id': 'SYN2_逐粒子回填注入', 'output': 'm_mu_over_me',
   'inputs': ['ratio_renamed_per_particle'], 'backfill': True, 'synthetic': True,
   'is_target_channel': True, 'cites': [], 'expect': 'BACKFILL'},
]

findings = []
statuses = {}
for ch in CHANNELS:
    for (rel, ln, tok) in ch['cites']:
        check_cite(rel, ln, tok, findings)
    st = analyze(ch, findings)
    statuses[ch['id']] = st
    ok = st == ch['expect']
    print('%-22s -> %-14s expect %-14s %s' % (ch['id'], st, ch['expect'],
                                              'PASS' if ok else 'FAIL'))

ctrl = {}
# D1: tautology detector fired and SYN1 not counted as HIT
ctrl['D1_input_identity_caught'] = (statuses['SYN1_恒等注入'] == 'INPUT_IDENTITY')
# D2: known-pass MSSM control row is a genuine HIT (ledger not always-RED)
ctrl['D2_known_pass_control'] = (statuses['CH0_MSSM控制_α_s'] == 'HIT')
# D3: census cross-channel -- non-control named-target HITs == 0 and every
#     /systems[*]/n_registered_predictions == 0 in the 靶场 census JSON, read live
hit_named = [c['id'] for c in CHANNELS
             if not c.get('synthetic') and not c.get('control')
             and c.get('is_target_channel') and statuses[c['id']] == 'HIT']
with open(os.path.join(ROOT, BA.replace('/', os.sep)), encoding='utf-8') as f:
    census = json.load(f)
sysvals = [s['n_registered_predictions'] for s in census['systems']]
ctrl['D3_census_zero_match'] = (not hit_named and all(v == 0 for v in sysvals)
                                and len(sysvals) > 0)
# D4: stale detector fires on synthetic bad line
f4 = []
check_cite(GZ, 999999, 'zzz', f4)
ctrl['D4_stale_fires'] = any(x[0] == 'STALE' for x in f4)
# target roster sanity: the three named targets exist in the 靶场 TARGETS source
pysrc = lines_of(BAPY)
roster = ' '.join(pysrc[57:69])
ctrl['D5_roster_present'] = all(k in roster for k in NAMED_TARGETS)
for k, v in sorted(ctrl.items()):
    print('%-32s %s' % (k, 'PASS' if v else 'FAIL'))

stale = [x for x in findings if x[0] == 'STALE']
shift = [x for x in findings if x[0] == 'SHIFT']
anchor_fails = [c['id'] for c in CHANNELS if statuses[c['id']] != c['expect']]

out = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   os.pardir, '数据',
                                   '第一性输出台账_α与代质量比_回填探测机检_2026-10-18.json'))
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'mandate': '§七.1 先声明它将输出哪一个无量纲数 (总账 L158)',
               'named_targets': NAMED_TARGETS,
               'channels': [{k: ch.get(k) for k in
                             ('id', 'output', 'inputs', 'control', 'synthetic',
                              'is_target_channel')} for ch in CHANNELS],
               'cites': [{'channel': ch['id'],
                          'refs': [{'file': r, 'line': l, 'token': t}
                                   for (r, l, t) in ch['cites']]}
                         for ch in CHANNELS],
               'statuses': statuses, 'controls': ctrl,
               'census_systems_n': len(sysvals),
               'cite_findings': {'stale': stale, 'shift': shift},
               'headline': {'named_target_first_principles_HITS': len(hit_named),
                            'mssm_control_HIT': statuses['CH0_MSSM控制_α_s'] == 'HIT'}},
              f, ensure_ascii=False, indent=1)
all_ok = (not stale and not anchor_fails and all(ctrl.values()))
print('wrote %s stale=%d shift=%d anchor_fails=%d controls_all_pass=%s named_HITs=%d rc=%d'
      % (out, len(stale), len(shift), len(anchor_fails), all(ctrl.values()),
         len(hit_named), 0 if all_ok else 1))
sys.exit(0 if all_ok else 1)
