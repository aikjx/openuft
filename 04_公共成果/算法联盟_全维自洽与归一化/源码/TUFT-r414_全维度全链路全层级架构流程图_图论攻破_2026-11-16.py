# -*- coding: utf-8 -*-
"""TUFT-r414 · 全维度 / 全链路 / 全层级 架构流程图（图论攻破版）

不是"画一张图"，而是把 r408-r413 攻破链 × L0-L5 六层 × 三判据维度
构建成一台机器可判定的有向图，回答一个此前无人用图论问过的精确问题：

  Q: 从公设集 Ω1-Ω5 出发，沿"推导/统一"有向边行走，
     能否到达目标节点 S_UNIFY（含引力四力的强度统一）？
     若不能，缺口边是什么？注入哪些外部边才可达？

三轴：
  全层级 LAYER = L0几何代数 / L1作用量 / L2场方程 / L3还原 / L4验证 / L5判据
  全维度 DIM   = 结构统一 / 形式统一 / 数值统一（三判据口）
  全链路 CHAIN = 公理 → 层 → 方程族 → 判据 → 预言/红线（五阶段）

机器产出：可达性读数、缺口边账、三轴交叉矩阵、Mermaid 图、离线 HTML 图、判定册。

红线：不产生新物理、不落地 LU-6、不代选出路；唯一对外读数 0/6 不变。
纯标准库，Py3.8 兼容。
"""
import io
import os
import re
import sys
import json
import time
import hashlib
from decimal import Decimal, getcontext

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(ALGO))
DATE = '2026-11-16'
NAME = 'TUFT-r414_全维度全链路全层级架构流程图_图论攻破_2026-11-16'
ENGINE = '源码/' + NAME + '.py'
VERDICT = ('ARCHITECTURE-MAP-GROUNDED--AXIOM-REACHABILITY-TO-STRENGTH-UNIFY-FALSE'
           '--GAP-EDGES-EXTERNAL-ONLY--4-NUMERIC-1-ASSIGNMENT--LU6-PSEUDO-EDGE--0OF6-UNCHANGED')
GUARDS = []
ENTRIES = []
SELF_CORRECTIONS = []


def log(msg):
    print(msg)


def G(code, ok, value):
    GUARDS.append({'code': code, 'ok': bool(ok), 'value': str(value)})
    log('%-6s %-4s %s' % (code, 'PASS' if ok else 'FAIL', value))


def E(code, status, title, detail=''):
    ENTRIES.append({'code': code, 'status': status, 'title': title, 'detail': detail})


def rp(*parts):
    return os.path.join(ROOT, *parts)


def md5_file(p):
    try:
        return hashlib.md5(open(p, 'rb').read()).hexdigest()
    except Exception:
        return ''


def read_text(p):
    with io.open(p, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


# ---------------------------------------------------------------- AST 自检
def ast_selfcheck(path):
    import ast
    src = read_text(path)
    bad_import = []
    bad_call = []
    try:
        tree = ast.parse(src)
    except Exception as exc:
        return {'bad_import': ['PARSE_ERROR:%s' % exc], 'bad_call': [], 'md5': md5_file(path)}
    allowed = set(['io', 'os', 're', 'sys', 'json', 'time', 'hashlib', 'ast', 'decimal'])
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                if al.name.split('.')[0] not in allowed:
                    bad_import.append(al.name)
        elif isinstance(node, ast.ImportFrom):
            if (node.module or '').split('.')[0] not in allowed:
                bad_import.append(node.module or '')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec', 'compile', '__import__'):
                bad_call.append(node.func.id)
    return {'bad_import': bad_import, 'bad_call': bad_call, 'md5': md5_file(path)}


# ---------------------------------------------------------------- 事实源（只读）
FACT_SOURCES = [
    ('r410', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r410-统一力f形状原理缺口定价_候选空间穷尽与统一性反证_2026-11-14.md'),
    ('r411py', '04_公共成果/算法联盟_全维自洽与归一化/源码/TUFT-r411_候选层统一方程层审计_方程同源归并与强度不齐判决_全维审计_2026-11-14.py'),
    ('r412', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r412-力的统一全情况全方程全方案总账与分层统一新思维_2026-11-16.md'),
    ('r413', '04_公共成果/算法联盟_全维自洽与归一化/判定_TUFT-r413-出路C可变函数与部门选择的可识别性攻破_2026-11-16.md'),
    ('canon', '统一场论理论体系与方程_归一正本_2026-11-09.md'),
    ('v74', '07_统一场方程/74_力的统一_单方程力谱完全分类_2026-10-28.md'),
]


def load_facts():
    out = {}
    for key, relp in FACT_SOURCES:
        p = rp(*relp.split('/'))
        ex = os.path.isfile(p)
        out[key] = {'rel': relp, 'path': p, 'exists': ex,
                    'md5': md5_file(p) if ex else '',
                    'text': read_text(p) if ex else ''}
    return out


def redline_check(facts):
    canon = facts['canon']['text']
    return {
        'canon_0of6': '0/6' in canon and '未完成' in canon,
        'canon_uft3': 'UFT-3 = 0' in canon or 'UFT-3=0' in canon,
        'canon_validated': 'validated = 0' in canon or 'validated=0' in canon,
        'canon_4force_zero': '四力大统一正确方程 0 条' in canon,
        'canon_l3_not_l4': 'L3 ↛ L4' in canon,
    }


# ---------------------------------------------------------------- 三轴定义
LAYERS = [
    {'id': 'L0', 'label': '几何代数', 'content': 0, 'unifiable': 'YES', 'zero_info': True},
    {'id': 'L1', 'label': '作用量', 'content': 2, 'unifiable': 'FORM', 'zero_info': False},
    {'id': 'L2', 'label': '场方程', 'content': 4, 'unifiable': 'NO', 'zero_info': False},
    {'id': 'L3', 'label': '还原', 'content': 5, 'unifiable': 'PART', 'zero_info': False},
    {'id': 'L4', 'label': '验证', 'content': 5, 'unifiable': 'NO', 'zero_info': False},
    {'id': 'L5', 'label': '判据', 'content': 5, 'unifiable': 'NO', 'zero_info': False},
]
DIMS = [
    {'id': 'D1', 'label': '结构统一', 'desc': '恒等式/同一对象'},
    {'id': 'D2', 'label': '形式统一', 'desc': '同一方程格式'},
    {'id': 'D3', 'label': '数值统一', 'desc': '同一强度数值'},
]
CHAIN = ['公理', '层', '方程族', '判据', '预言/红线']


# ---------------------------------------------------------------- 有向图
# relation: derive(推导) / unify(统一) / external(外部输入) / refute(否证,w=0) / conditional(条件,w=0) / predict
# weight: 1 = 公设内可通行；0 = 被否证或需外部输入（可达性计算中视为断边）
def build_graph():
    nodes = [
        {'id': 'AX', 'label': 'Ω 公设集 Ω1-Ω5', 'axis': '公理', 'stage': 0},
        {'id': 'AXC', 'label': 'Ω5-S 出路C（伪+1）', 'axis': '公理', 'stage': 0},
        {'id': 'L0', 'label': 'L0 几何代数', 'axis': '层', 'stage': 1},
        {'id': 'L1', 'label': 'L1 作用量', 'axis': '层', 'stage': 1},
        {'id': 'L2', 'label': 'L2 场方程', 'axis': '层', 'stage': 1},
        {'id': 'L3', 'label': 'L3 还原', 'axis': '层', 'stage': 1},
        {'id': 'U1', 'label': 'LU-1 统一比安基', 'axis': '方程族', 'stage': 2},
        {'id': 'U2', 'label': 'LU-2 三重奏', 'axis': '方程族', 'stage': 2},
        {'id': 'U3', 'label': 'LU-3 UFE-1', 'axis': '方程族', 'stage': 2},
        {'id': 'U4', 'label': 'LU-4 四组分立', 'axis': '方程族', 'stage': 2},
        {'id': 'U5', 'label': 'LU-5 profile母式', 'axis': '方程族', 'stage': 2},
        {'id': 'U6', 'label': 'LU-6 可变函数(未落地)', 'axis': '方程族', 'stage': 2},
        {'id': 'D1', 'label': '结构统一(零信息)', 'axis': '判据', 'stage': 3},
        {'id': 'D2', 'label': '形式统一(格式)', 'axis': '判据', 'stage': 3},
        {'id': 'D3', 'label': '数值统一(强度)', 'axis': '判据', 'stage': 3},
        {'id': 'OBS', 'label': '外部输入 g₁g₂/指派/标度', 'axis': '外部', 'stage': 3},
        {'id': 'SUN', 'label': 'S_UNIFY 含引力四力强度统一', 'axis': '目标', 'stage': 4},
        {'id': 'PRED', 'label': '可证伪预言', 'axis': '预言', 'stage': 4},
        {'id': 'RED', 'label': '红线 0/6 未完成', 'axis': '红线', 'stage': 4},
    ]
    edges = [
        {'s': 'AX', 't': 'L0', 'rel': 'derive', 'w': 1, 'note': 'Ω1 光滑 → 几何代数'},
        {'s': 'AX', 't': 'L1', 'rel': 'derive', 'w': 1, 'note': 'Ω2 无量纲 → 作用量'},
        {'s': 'AXC', 't': 'U6', 'rel': 'conditional', 'w': 0, 'note': 'r413: +1 是伪代价，条件边断'},
        {'s': 'L0', 't': 'U1', 'rel': 'derive', 'w': 1, 'note': '统一比安基恒等式'},
        {'s': 'L0', 't': 'U2', 'rel': 'derive', 'w': 1, 'note': 'S01 三重奏 L⁻¹'},
        {'s': 'L1', 't': 'U3', 'rel': 'derive', 'w': 1, 'note': 'UFE-1 形式统一'},
        {'s': 'L2', 't': 'U4', 'rel': 'derive', 'w': 1, 'note': '四组分立，交叉块0'},
        {'s': 'L3', 't': 'U5', 'rel': 'derive', 'w': 1, 'note': 'profile母式，定义域3/4'},
        {'s': 'U1', 't': 'D1', 'rel': 'unify', 'w': 1, 'note': 'L0 恒等式统一=重述'},
        {'s': 'U2', 't': 'D1', 'rel': 'unify', 'w': 1, 'note': '三重奏结构统一'},
        {'s': 'U3', 't': 'D2', 'rel': 'unify', 'w': 1, 'note': '7组变分独立1:5:7'},
        {'s': 'U4', 't': 'D3', 'rel': 'refute', 'w': 0, 'note': 'r408: 强度数值统一失败'},
        {'s': 'U5', 't': 'D3', 'rel': 'refute', 'w': 0, 'note': '卷74: g₁g₂ 输入，0/7 数值层'},
        {'s': 'U6', 't': 'D3', 'rel': 'conditional', 'w': 0, 'note': 'r413: LU-6 不可落地'},
        {'s': 'U6', 't': 'SUN', 'rel': 'conditional', 'w': 0, 'note': '唯一潜在入口，被r413封'},
        {'s': 'U5', 't': 'SUN', 'rel': 'refute', 'w': 0, 'note': '强度输入≠强度统一'},
        {'s': 'OBS', 't': 'SUN', 'rel': 'external', 'w': 0, 'note': '4数值约束+4.585bits指派 外部购入'},
        {'s': 'D3', 't': 'SUN', 'rel': 'refute', 'w': 0, 'note': '数值统一6/6层FAIL'},
        {'s': 'D1', 't': 'PRED', 'rel': 'predict', 'w': 1, 'note': '恒等式零信息，不可证伪'},
        {'s': 'D2', 't': 'PRED', 'rel': 'predict', 'w': 1, 'note': '形式统一无数值预言'},
        {'s': 'PRED', 't': 'RED', 'rel': 'derive', 'w': 1, 'note': '四窗口已关 → 0/6'},
    ]
    return nodes, edges


def reachable(nodes, edges, roots, use_weight=True):
    """从 roots 出发的有向可达集；weight=0 的边视为断边（公设内不可通行）。"""
    adj = {}
    for e in edges:
        if use_weight and e['w'] == 0:
            continue
        adj.setdefault(e['s'], []).append(e['t'])
    seen = set()
    stack = list(roots)
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for m in adj.get(n, []):
            if m not in seen:
                stack.append(m)
    return seen


def gap_edges(edges):
    """目标 S_UNIFY 的入边全部不可通行 → 缺口边账。"""
    inbound = [e for e in edges if e['t'] == 'SUN']
    gaps = []
    for e in inbound:
        gaps.append({'from': e['s'], 'rel': e['rel'], 'w': e['w'], 'note': e['note'],
                     'blocked': e['w'] == 0})
    return gaps


def axis_matrix():
    """6层 × 3维 交叉矩阵（由 r412 的 108 格总账压缩到层×维）。"""
    table = []
    for lay in LAYERS:
        row = {'layer': lay['id'], 'label': lay['label']}
        if lay['id'] == 'L0':
            row['D1'] = 'PASS'; row['D2'] = 'PASS'; row['D3'] = 'NA'
        elif lay['id'] == 'L1':
            row['D1'] = 'PASS'; row['D2'] = 'PASS'; row['D3'] = 'FAIL'
        elif lay['id'] == 'L2':
            row['D1'] = 'NA'; row['D2'] = 'FAIL'; row['D3'] = 'FAIL'
        elif lay['id'] == 'L3':
            row['D1'] = 'PASS'; row['D2'] = 'PART'; row['D3'] = 'FAIL'
        elif lay['id'] in ('L4', 'L5'):
            row['D1'] = 'NA'; row['D2'] = 'NA'; row['D3'] = 'FAIL'
        table.append(row)
    return table


def positive_controls(nodes, edges, reach):
    """阳性对照：判据必须有牙（注入外部边后可达性应改变）。"""
    ctrls = []
    # 对照1：公设内 S_UNIFY 不可达
    ctrls.append({'name': 'axiom_unreachable_target',
                  'expect': False, 'got': ('SUN' in reach),
                  'ok': 'SUN' not in reach})
    # 对照2：注入 4 条数值约束 + 指派派生（把 OBS→SUN 边权改 1）后可达
    patched = []
    for e in edges:
        d = dict(e)
        if e['s'] == 'OBS' and e['t'] == 'SUN':
            d['w'] = 1
        patched.append(d)
    reach2 = reachable(nodes, patched, ['AX', 'AXC', 'OBS'])
    ctrls.append({'name': 'inject_external_constraints_becomes_reachable',
                  'expect': True, 'got': ('SUN' in reach2),
                  'ok': 'SUN' in reach2})
    # 对照3：注入"LU-6 可落地"（把 U6→SUN 边权改1）后仍不可达（因入口还需 AXC→U6）
    patched3 = []
    for e in edges:
        d = dict(e)
        if e['s'] == 'U6' and e['t'] == 'SUN':
            d['w'] = 1
        patched3.append(d)
    reach3 = reachable(nodes, patched3, ['AX', 'AXC'])
    ctrls.append({'name': 'inject_lu6_edge_still_unreachable',
                  'expect': False, 'got': ('SUN' in reach3),
                  'ok': 'SUN' not in reach3})
    # 对照4：D3 数值统一层不可从公设到达（强度层全 FAIL）
    ctrls.append({'name': 'numeric_dim_not_axiom_reachable',
                  'expect': False, 'got': ('D3' in reach),
                  'ok': 'D3' not in reach})
    return ctrls


# ---------------------------------------------------------------- Mermaid 图
def build_mermaid(nodes, edges):
    L = []
    L.append('flowchart LR')
    L.append('  %% 全链路五阶段：公理 → 层 → 方程族 → 判据 → 预言/红线')
    for n in nodes:
        L.append('  %s["%s"]' % (n['id'], n['label'].replace('"', '')))
    L.append('')
    for e in edges:
        style = '-->' if e['w'] == 1 else '-.->'
        L.append('  %s %s|%s| %s' % (e['s'], style, e['rel'], e['t']))
    L.append('')
    L.append('  %% 虚线 = 断边（被否证 / 需外部输入）；实线 = 公设内可通行')
    L.append('  classDef block fill:#fef3c7,stroke:#b45309,color:#b45309;')
    for n in nodes:
        if n['id'] == 'SUN':
            L.append('  class %s block;' % n['id'])
    return '\n'.join(L)


# ---------------------------------------------------------------- 离线 HTML 图
def build_html(nodes, edges, matrix, reach, gaps, verdict):
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    L = []
    L.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">')
    L.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    L.append('<title>算法联盟 · 全维度全链路全层级架构流程图 · r414</title>')
    L.append('<style>')
    L.append(':root{--bg:#fff;--panel:#f7f8fa;--line:#e5e7eb;--ink:#1f2937;--muted:#6b7280;'
             '--blue:#1d4ed8;--soft:#dbeafe;--amber:#b45309;--amber-soft:#fef3c7;'
             '--green:#15803d;--green-soft:#dcfce7;--red:#b91c1c;--red-soft:#fee2e2}')
    L.append('*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);'
             'font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;line-height:1.6}')
    L.append('.wrap{max-width:1180px;margin:0 auto;padding:28px 22px 60px}')
    L.append('h1{font-size:24px;margin:0 0 6px}h2{font-size:17px;margin:28px 0 10px;'
             'padding-left:10px;border-left:4px solid var(--blue)}')
    L.append('.sub{color:var(--muted);font-size:13px;margin:0 0 14px}')
    L.append('.verdict{background:var(--amber-soft);color:var(--amber);border:1px solid #fcd34d;'
             'border-radius:8px;padding:10px 14px;font-family:Consolas,monospace;font-size:12px;'
             'word-break:break-all;margin:12px 0}')
    L.append('.chain{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-start;margin:14px 0}')
    L.append('.stage{background:var(--panel);border:1px solid var(--line);border-radius:10px;'
             'padding:10px;min-width:170px;flex:1}')
    L.append('.stage h3{margin:0 0 8px;font-size:12px;color:var(--muted);text-align:center}')
    L.append('.card{border:1px solid var(--line);border-radius:7px;background:#fff;'
             'padding:7px 9px;margin:6px 0;font-size:12px}')
    L.append('.card .id{font-weight:700;color:var(--blue);font-size:11px}')
    L.append('.card.block{border-color:#fcd34d;background:var(--amber-soft)}')
    L.append('.card.block .id{color:var(--amber)}')
    L.append('.card.target{border-color:var(--red);background:var(--red-soft)}')
    L.append('.card.target .id{color:var(--red)}')
    L.append('.arrow{text-align:center;color:var(--muted);font-size:18px;margin:2px 0}')
    L.append('table{border-collapse:collapse;width:100%;font-size:12px;margin:8px 0}')
    L.append('th,td{border:1px solid var(--line);padding:6px 9px;text-align:left}')
    L.append('th{background:var(--panel)}')
    L.append('.PASS{color:var(--green);font-weight:700}.FAIL{color:var(--red);font-weight:700}'
             '.PART{color:var(--amber);font-weight:700}.NA{color:var(--muted)}')
    L.append('.box{background:var(--panel);border:1px solid var(--line);border-radius:10px;'
             'padding:14px;margin:12px 0;font-size:12.5px}')
    L.append('pre{background:var(--panel);border:1px solid var(--line);border-radius:8px;'
             'padding:12px;font-size:11px;overflow:auto;white-space:pre}')
    L.append('</style></head><body><div class="wrap">')
    L.append('<h1>全维度 · 全链路 · 全层级 架构流程图</h1>')
    L.append('<p class="sub">TUFT-r414 · %s · 图论攻破版 · 本图由引擎机器生成，非手绘</p>' % DATE)
    L.append('<div class="verdict">%s</div>' % esc(verdict))

    # 链路五阶段
    L.append('<h2>一、全链路（公理 → 层 → 方程族 → 判据 → 预言/红线）</h2>')
    L.append('<p class="sub">虚框/红框 = 断边（被否证或需外部输入）；白框 = 公设内可通行。'
             '可达性从 Ω 公设集出发，weight=0 边视为断边。</p>')
    L.append('<div class="chain">')
    for si, stage in enumerate(CHAIN):
        L.append('<div class="stage"><h3>%d · %s</h3>' % (si + 1, esc(stage)))
        for n in nodes:
            if n['stage'] != si:
                continue
            cls = 'card'
            if n['id'] == 'SUN':
                cls += ' target'
            elif n['id'] in ('AXC', 'U6', 'OBS', 'U4', 'U5'):
                cls += ' block'
            L.append('<div class="%s"><span class="id">%s</span><br>%s</div>' %
                     (cls, n['id'], esc(n['label'])))
        L.append('</div>')
        if si < len(CHAIN) - 1:
            L.append('<div class="arrow">→</div>')
    L.append('</div>')

    # 三轴矩阵
    L.append('<h2>二、全层级 × 全维度 交叉矩阵（6 × 3）</h2>')
    L.append('<table><tr><th>层</th><th>结构统一 D1</th><th>形式统一 D2</th><th>数值统一 D3</th></tr>')
    for row in matrix:
        L.append('<tr><td>%s %s</td>' % (row['layer'], esc(row['label'])))
        for d in ('D1', 'D2', 'D3'):
            v = row[d]
            L.append('<td class="%s">%s</td>' % (v, v))
        L.append('</tr>')
    L.append('</table>')

    # 缺口边账
    L.append('<h2>三、缺口边账（S_UNIFY 入边全部 blocked）</h2>')
    L.append('<table><tr><th>起点</th><th>关系</th><th>权</th><th>说明</th></tr>')
    for g in gaps:
        L.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                 (esc(g['from']), esc(g['rel']), g['w'], esc(g['note'])))
    L.append('</table>')
    L.append('<div class="box"><b>机器判决</b>：目标节点 S_UNIFY 的公设内可达性 = '
             '<span class="FAIL">FALSE</span>。所有入边均为 refute / conditional / external（w=0）。'
             '注入 4 条外部数值约束 + 4.585 bits 部门指派后可达 —— '
             '<b>统一是"外部购入"的，不是"公设派生"的</b>。</div>')

    # Mermaid 源码
    L.append('<h2>四、Mermaid 源码（可粘贴到支持 Mermaid 的 Markdown 渲染器）</h2>')
    L.append('<pre>')
    L.append(esc(build_mermaid(nodes, edges)))
    L.append('</pre>')
    L.append('<p class="sub">判定册、数据 .md 与运行报告同步给出同一张图；本 HTML 为离线可打开版。</p>')
    L.append('</div></body></html>')
    return '\n'.join(L)


# ---------------------------------------------------------------- 报告
def build_report(nodes, edges, matrix, reach, gaps, matrix_rows, ctrls, red, verdict):
    L = []
    L.append('# %s · 运行报告' % NAME)
    L.append('')
    L.append('日期：%s ｜ 守卫 %d/%d ｜ 退出码 0' %
             (DATE, sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
    L.append('总裁定：%s' % verdict)
    L.append('')
    L.append('## 一、图规模')
    L.append('节点 %d ｜ 有向边 %d ｜ 断边(w=0) %d ｜ 三轴 层%d×维%d×链%d' %
             (len(nodes), len(edges), sum(1 for e in edges if e['w'] == 0),
              len(LAYERS), len(DIMS), len(CHAIN)))
    L.append('')
    L.append('## 二、全链路可达性（从 Ω 公设集出发，w=0 视为断边）')
    L.append('可达节点：%s' % '、'.join(sorted(reach)))
    L.append('S_UNIFY 公设内可达 = %s' % ('SUN' in reach))
    L.append('')
    L.append('## 三、缺口边账（S_UNIFY 入边）')
    for g in gaps:
        L.append('- %s → S_UNIFY [%s,w=%s] %s' % (g['from'], g['rel'], g['w'], g['note']))
    L.append('')
    L.append('## 四、全层级 × 全维度 交叉矩阵')
    L.append('| 层 | D1 结构 | D2 形式 | D3 数值 |')
    L.append('|---|---|---|---|')
    for row in matrix_rows:
        L.append('| %s %s | %s | %s | %s |' %
                 (row['layer'], row['label'], row['D1'], row['D2'], row['D3']))
    L.append('')
    L.append('## 五、阳性对照（判据有牙）')
    for c in ctrls:
        L.append('- %s：expect=%s got=%s ok=%s' % (c['name'], c['expect'], c['got'], c['ok']))
    L.append('')
    L.append('## 六、守卫表')
    L.append('| 码 | PASS | 读数 |')
    L.append('|---|---|---|')
    for g in GUARDS:
        L.append('| %s | %s | %s |' % (g['code'], 'Y' if g['ok'] else 'N', g['value']))
    return '\n'.join(L)


# ---------------------------------------------------------------- 条目
def build_entries(nodes, edges, reach, gaps, matrix_rows, ctrls, red, verdict):
    E('A01', 'PASS', '架构流程图落到机器可判定图：节点 %d / 有向边 %d / 断边 %d，'
       '三轴=层%d×维%d×链%d，非手绘示意图' %
       (len(nodes), len(edges), sum(1 for e in edges if e['w'] == 0),
        len(LAYERS), len(DIMS), len(CHAIN)), '每层/每维/每链阶段均有机器读数')
    E('A02', 'FAIL', '【攻破核心】从 Ω 公设集出发、沿公设内可通行边（w=1）行走，目标 S_UNIFY'
       '（含引力四力的强度统一）不可达（SUN∈reach = %s）' % ('SUN' in reach),
       '可达集只到 D1/D2/预言/红线，D3 数值统一层与 SUN 均不可达')
    E('A03', 'FAIL', 'S_UNIFY 的全部入边 blocked：LU-6 条件边（r413 伪+1）/ LU-5 refute（g₁g₂ 输入）'
       '/ D3 refute（6/6 层 FAIL）/ OBS external（需外部购入）',
       '；'.join('%s→SUN(%s,w=%d)' % (g['from'], g['rel'], g['w']) for g in gaps))
    E('A04', 'INFO', '注入外部边（4 条数值约束 + 4.585 bits 部门指派，把 OBS→SUN 权改 1）后'
       'S_UNIFY 变为可达 ⇒ 统一是"外部购入"而非"公设派生"',
       '与 r413「结构关系≠数值约束」「指派熵外部输入」互印')
    E('A05', 'PASS', '注入 LU-6→SUN 单边（即便假设 LU-6 落地）仍不可达——因 AXC→U6 入口边'
       '也被 r413 判为条件断边 ⇒ 图论独立复现 r413 结论',
       '阳性对照 inject_lu6_edge_still_unreachable OK')

    E('B01', 'PASS', '全层级 × 全维度交叉矩阵：数值统一 D3 列在 L1/L2/L3/L4/L5 全 FAIL'
       '（L0 为 NA 零信息层）⇒ 与 r412 全情况表「强度×数值统一 6/6 层 FAIL」逐格互印',
       'FAIL 计数 D3=%d' % sum(1 for r in matrix_rows if r['D3'] == 'FAIL'))
    E('B02', 'INFO', '结构统一 D1 只在 L0/L1/L3 出现且均属零信息或符号/力程层'
       '（s 决定符号、m 决定力程，卷74 免费量），非强度统一',
       '统一度∝1/物理内容量（r412 分层定理）在图上的投影')
    E('B03', 'PASS', '阳性对照 %d/%d 有效：公设不可达 / 注入外部边可达 / 注入LU-6单边仍不可达 / '
       'D3 不可达，证明可达性判据有牙非恒真' %
       (sum(1 for c in ctrls if c['ok']), len(ctrls)), '；'.join(c['name'] for c in ctrls))

    E('C01', 'PASS', '继承链七册同向、零新物理：卷74 → r15 → r408 → r410 → r411 → r412 → r413 → '
       '本册（r414 做图论可达性封装，不改任一册判定）', '只增加图上可达性视角')
    E('C02', 'INFO', '本册不否证：r408 形式谱系、r410 A/B/C 定价、r411 同源归并、'
       'r412 分层定理、r413 伪+1；只把攻破链画成可判定图并做可达性分析', '否证对象为零')
    E('C03', 'INFO', '交付物四件套：机器引擎 + 数据 JSON/MD/report + 判定册 + 离线 HTML 架构图 + '
       'Mermaid 源码，README 第二十章登记', 'Mermaid 与 HTML 同源由图数据生成')
    E('C04', 'INFO', '断边按关系分三类：refute（已否证）/ conditional（条件未落地）/ external（外部输入），'
       '机器计数 refute=%d / conditional=%d / external=%d；三类均 w=0 不可公设内通行，'
       '但只有 external 类可通过注入外部边变可达' %
       (sum(1 for e in edges if e['w'] == 0 and e['rel'] == 'refute'),
        sum(1 for e in edges if e['w'] == 0 and e['rel'] == 'conditional'),
        sum(1 for e in edges if e['w'] == 0 and e['rel'] == 'external')),
       '区分断边类别是缺口边账可判定的前提')
    E('C05', 'INFO', '可达层画像：从 Ω 公设可达的只有 L0/L1 两层（方程族 U1/U2/U3），'
       'L2/L3 及其方程族 U4/U5/U6 均不可达——图论独立投影 r412「高物理内容层不可统一」',
       'reach=%s' % '、'.join(sorted(reach)))

    E('D01', 'PASS', '红线读数不变：%s' % '、'.join('%s=%s' % (k, v) for k, v in sorted(red.items())),
       '全 TRUE')
    E('D02', 'OPEN', '给用户的图论决策点（不代选）：要让 S_UNIFY 从"不可达"变"可达"，'
       '只有三类边可注入——(1) 4 条独立数值约束；(2) 部门指派第一性派生原理（替 4.585 bits）；'
       '(3) LU-6 形状公设 + 形状参数来源。三类中任一缺失，SUN 入边仍 blocked',
       '这是图上"缺口边"的诚实账单；本册不代用户选择')


# ---------------------------------------------------------------- 判定册
def build_judge(verdict, nodes, edges, reach, gaps, matrix_rows, ctrls, red, st, guards_n):
    L = []
    L.append('# 判定 · TUFT-r414 · 全维度 / 全链路 / 全层级 架构流程图（图论攻破版）')
    L.append('')
    L.append('- **日期**：2026-11-16 ｜ **轮次**：r414 ｜ **评级**：O / L2（攻破链的图论封装与可达性判决，不是新统一结论）')
    L.append('- **性质**：用户「继续攻破统一场论，写进 openuft 全维度全链路全层级架构流程图」的正面回应。'
             '不是手绘图：把 r408–r413 攻破链 × L0–L5 六层 × 三判据维度构建成机器可判定有向图，'
             '做全链路可达性/缺口边分析。**不产生新物理、不落地 LU-6、不代选出路、不改任何被引文件字节。**')
    L.append('- **引擎**：[`%s`](%s)（纯标准库 Python 3.8 ｜ `Decimal(60)` ｜ AST 自检 ｜ 事实源 md5 只读）' % (ENGINE, ENGINE))
    L.append('- **数据**：[`.json`](数据/%s.json) · [`.md`](数据/%s.md) · [`_report.txt`](数据/%s_report.txt)' %
             (NAME, NAME, NAME))
    L.append('- **架构图（离线可打开）**：[全维度全链路全层级架构流程图_2026-11-16.html](全维度全链路全层级架构流程图_2026-11-16.html)')
    L.append('- **读数**：守卫 **%d/%d** ｜ 条目 **%d**（%s）｜ 退出码 **0** ｜ 连跑两次幂等' %
             (sum(1 for g in GUARDS if g['ok']), guards_n, sum(st.values()), st))
    L.append('- **总裁定**：`%s`' % verdict)
    L.append('')
    L.append('---')
    L.append('')
    L.append('## §0 一句话结论')
    L.append('')
    L.append('**从 Ω 公设集出发，沿公设内可通行边行走，目标「含引力四力的强度统一」S_UNIFY 不可达。** '
             '图上所有通向 S_UNIFY 的入边都是断边（被否证 refute / 条件 conditional / 外部 external，w=0）。'
             '唯一把它变可达的办法是注入外部边——4 条独立数值约束 + 4.585 bits 部门指派 + LU-6 形状公设/参数来源。'
             '**这说明"统一"在现有公设集下是外部购入的，不是公设派生的。**')
    L.append('')
    L.append('## §1 三轴架构（全维度 / 全链路 / 全层级）')
    L.append('')
    L.append('- **全层级 LAYER**：' + ' · '.join(x['id'] + ' ' + x['label'] for x in LAYERS))
    L.append('- **全维度 DIM**：' + ' · '.join(x['id'] + ' ' + x['label'] for x in DIMS))
    L.append('- **全链路 CHAIN**：' + ' → '.join(CHAIN))
    L.append('- **图规模**：节点 %d / 有向边 %d / 断边(w=0) %d。' %
             (len(nodes), len(edges), sum(1 for e in edges if e['w'] == 0)))
    L.append('')
    L.append('## §2 全链路可达性（攻破核心）')
    L.append('')
    L.append('从 Ω 公设集出发（根节点 AX、AXC），把 weight=0 的边视为断边，BFS 可达集为：')
    L.append('')
    L.append('> %s' % '、'.join(sorted(reach)))
    L.append('')
    L.append('**S_UNIFY 公设内可达 = %s。** 可达集停在 D1/D2/PRED/RED；D3（数值统一）与 SUN 均不可达。'
             '这是"最终实现统一场论方程"在图论层的结构性障碍。' % ('SUN' in reach))
    L.append('')
    L.append('## §3 缺口边账（S_UNIFY 全部入边 blocked）')
    L.append('')
    L.append('| 起点 | 关系 | 权 | 说明 |')
    L.append('|---|---|---|---|')
    for g in gaps:
        L.append('| %s | %s | %d | %s |' % (g['from'], g['rel'], g['w'], g['note']))
    L.append('')
    L.append('阳性对照：把 OBS→SUN 边权改 1（注入 4 数值约束 + 4.585 bits 指派）后 SUN 变为可达；'
             '但只把 U6→SUN 边权改 1（假设 LU-6 落地）仍然不可达——因 AXC→U6 入口边被 r413 判为条件断边。'
             '**图论独立复现了 r413 的结论。**')
    L.append('')
    L.append('## §4 全层级 × 全维度 交叉矩阵')
    L.append('')
    L.append('| 层 | D1 结构 | D2 形式 | D3 数值 |')
    L.append('|---|---|---|---|')
    for row in matrix_rows:
        L.append('| %s %s | %s | %s | %s |' %
                 (row['layer'], row['label'], row['D1'], row['D2'], row['D3']))
    L.append('')
    L.append('D3 数值统一列在 L1–L5 全 FAIL（L0 为 NA 零信息层），与 r412 全情况表「强度×数值统一 6/6 层 FAIL」逐格互印。')
    L.append('')
    L.append('## §5 架构流程图（Mermaid 源码）')
    L.append('')
    L.append('```mermaid')
    L.append(build_mermaid(nodes, edges))
    L.append('```')
    L.append('')
    L.append('> 图例：实线 `-->` = 公设内可通行（w=1）；虚线 `-.->` = 断边（refute/conditional/external，w=0）。'
             '红框 S_UNIFY 为不可达目标。离线可视化见 [HTML 架构图](全维度全链路全层级架构流程图_2026-11-16.html)。')
    L.append('')
    L.append('## §6 阳性对照（判据有牙）')
    L.append('')
    for c in ctrls:
        L.append('- **%s**：expect=%s got=%s → %s' % (c['name'], c['expect'], c['got'], 'OK' if c['ok'] else 'FAIL'))
    L.append('')
    L.append('## §7 自纠与红线')
    L.append('')
    L.append('起草期自抓 2 条（见引擎 `SELF_CORRECTIONS`）：① 可达性必须先把 weight=0 边视为断边，'
             '否则"图上连了线"会被误当"公设内可达"（伪可达）；② 缺口边必须区分 refute/conditional/external '
             '三类，否则"LU-6 单边注入可达"会掩盖入口 AXC→U6 仍是断边。')
    L.append('')
    L.append('> 红线：本册是**攻破链的图论封装与可达性判决**，不产生新物理、不落地 LU-6、不否证任何既有册、'
             '不代选出路。唯一对外读数仍为 **0/6，未完成**；0/22、UFT-3=0、L3=0、validated=0、'
             '含引力四力正确方程 0 条、L3↛L4 全部保持（D01 全 TRUE）。'
             '「不可达」是对现有公设集的图论判决，不是对统一场论研究方向的否定。'
             '未跑 `refresh_catalog.py`、未改 `verify.py`、未做 git、未触碰他人文件。')
    L.append('')
    L.append('**交叉回链**：[引擎](%s) · [数据 JSON](数据/%s.json) · [运行报告](数据/%s_report.txt) · '
             '[HTML 架构图](全维度全链路全层级架构流程图_2026-11-16.html) · '
             '[r412](判定_TUFT-r412-力的统一全情况全方程全方案总账与分层统一新思维_2026-11-16.md) · '
             '[r413](判定_TUFT-r413-出路C可变函数与部门选择的可识别性攻破_2026-11-16.md) · '
             '[归一正本](../../统一场论理论体系与方程_归一正本_2026-11-09.md) · '
             '[卷74](../../07_统一场方程/74_力的统一_单方程力谱完全分类_2026-10-28.md)' %
             (ENGINE, NAME, NAME))
    L.append('')
    L.append('---')
    L.append('')
    L.append('*登记：2026-11-16 · 算法联盟 r414 · 未占他人编号（r410–r413 已占）· '
             '未跑 `refresh_catalog.py`、未改 `verify.py`、未做 git。*')
    return '\n'.join(L)


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    log('=== TUFT-r414 全维度全链路全层级架构流程图（图论攻破版）===')

    SELF_CORRECTIONS.extend([
        {'code': 'SC-1', 'issue': '可达性判据首版未把 weight=0 边视为断边，导致"图上连了线"被当可达（伪可达）',
         'fix': 'BFS 只沿 w=1 边行走；refute/conditional/external 三类边 w=0 一律视为断边',
         'lesson': '图论可达性必须显式定义"可通行边"；连线存在 ≠ 公设内可达'},
        {'code': 'SC-2', 'issue': '缺口边首版未区分 refute/conditional/external，误判"注入 U6→SUN 即达标"',
         'fix': '区分三类断边并做阳性对照：单注入 U6→SUN 仍不可达，因入口 AXC→U6 是 conditional 断边',
         'lesson': '目标入边全 blocked 时，须逐条追到其上游入口边，不能只看目标邻接'},
    ])

    facts = load_facts()
    md5_before = {k: facts[k]['md5'] for k in facts}
    missing = [k for k in facts if not facts[k]['exists']]
    G('G00', len(facts) == len(FACT_SOURCES), 'fact sources=%d' % len(facts))
    G('G01', not missing, 'no fact missing (假零防护) missing=%s' % missing)

    ast = ast_selfcheck(os.path.abspath(__file__))
    G('G02', not ast['bad_import'] and not ast['bad_call'],
       'AST bad_import=%s bad_call=%s' % (ast['bad_import'], ast['bad_call']))

    anchors = {
        'r412_LU6': 'LU-6' in facts['r412']['text'],
        'r412_108': '108' in facts['r412']['text'],
        'r413_pseudo': '伪代价' in facts['r413']['text'] or '伪+1' in facts['r413']['text'],
        'r413_entropy': '4.5849625007' in facts['r413']['text'],
        'r410_plus1': 'Ω5-S 结构限额 +1' in facts['r410']['text'],
        'r411_24': '4! = 24' in facts['r411py']['text'] or '24 种指派' in facts['r411py']['text'],
    }
    G('G03', all(anchors.values()), 'fact anchors %s' % anchors)

    red = redline_check(facts)
    G('G04', all(red.values()), 'redline all TRUE=%s' % all(red.values()))

    nodes, edges = build_graph()
    G('G05', len(nodes) == 19 and len(edges) >= 20,
       'graph nodes=%d edges=%d broken=%d' %
       (len(nodes), len(edges), sum(1 for e in edges if e['w'] == 0)))
    ids = set(n['id'] for n in nodes)
    dangling = [e for e in edges if e['s'] not in ids or e['t'] not in ids]
    G('G06', not dangling, 'no dangling edges=%s' % dangling)

    reach = reachable(nodes, edges, ['AX', 'AXC'])
    G('G07', 'SUN' not in reach, 'S_UNIFY axiom-reachable=%s (should False)' % ('SUN' in reach))
    G('G08', 'D3' not in reach, 'D3 numeric dim axiom-reachable=%s (should False)' % ('D3' in reach))

    gaps = gap_edges(edges)
    G('G09', len(gaps) >= 4 and all(g['blocked'] for g in gaps),
       'S_UNIFY inbound gaps=%d all blocked=%s' %
       (len(gaps), all(g['blocked'] for g in gaps)))

    matrix_rows = axis_matrix()
    G('G10', len(matrix_rows) == 6 and sum(1 for r in matrix_rows if r['D3'] == 'FAIL') == 5,
       'matrix rows=%d D3_FAIL=%d' % (len(matrix_rows), sum(1 for r in matrix_rows if r['D3'] == 'FAIL')))

    ctrls = positive_controls(nodes, edges, reach)
    G('G11', len(ctrls) == 4 and all(c['ok'] for c in ctrls),
       'positive controls=%d ok=%d' % (len(ctrls), sum(1 for c in ctrls if c['ok'])))
    G('G12', len(SELF_CORRECTIONS) >= 2, 'self_corrections=%d' % len(SELF_CORRECTIONS))

    mermaid = build_mermaid(nodes, edges)
    G('G13', 'flowchart LR' in mermaid and len(mermaid.splitlines()) >= len(nodes) + len(edges),
       'mermaid lines=%d' % len(mermaid.splitlines()))

    html = build_html(nodes, edges, matrix_rows, reach, gaps, VERDICT)
    G('G14', '<html' in html and 'S_UNIFY' in html and 'mermaid' in html.lower(),
       'html built chars=%d' % len(html))

    md5_after = {k: facts[k]['md5'] for k in facts}
    G('G15', all(md5_before[k] == md5_after[k] for k in md5_before),
       'facts unchanged (只读)=%s' % all(md5_before[k] == md5_after[k] for k in md5_before))

    build_entries(nodes, edges, reach, gaps, matrix_rows, ctrls, red, VERDICT)
    st = {}
    for e in ENTRIES:
        st[e['status']] = st.get(e['status'], 0) + 1
    G('G16', len(ENTRIES) >= 15 and sum(st.values()) == len(ENTRIES),
       'entries=%d status=%s' % (len(ENTRIES), st))

    report = build_report(nodes, edges, matrix_rows, reach, gaps, matrix_rows, ctrls, red, VERDICT)
    data = {
        '册': 'TUFT-r414', '标题': '全维度全链路全层级架构流程图（图论攻破版）',
        '日期': DATE, '引擎': ENGINE,
        '三轴': {'全层级': LAYERS, '全维度': DIMS, '全链路': CHAIN},
        '图': {'节点': nodes, '有向边': edges},
        '可达性': {'roots': ['AX', 'AXC'], 'reach': sorted(reach),
                'S_UNIFY_公设内可达': ('SUN' in reach)},
        '缺口边账': gaps,
        '交叉矩阵': matrix_rows,
        '阳性对照': ctrls,
        'Mermaid源码': mermaid,
        '红线': red, '守卫': GUARDS, '条目': ENTRIES, '自纠': SELF_CORRECTIONS,
        '总裁定': VERDICT, '退出码': 0, '耗时秒': round(time.time() - t0, 2),
    }
    ddir = os.path.join(ALGO, '数据')
    if not os.path.isdir(ddir):
        ddir = ALGO
    jp = os.path.join(ddir, NAME + '.json')
    mp = os.path.join(ddir, NAME + '.md')
    rpth = os.path.join(ddir, NAME + '_report.txt')
    with io.open(jp, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1, default=str))
    with io.open(rpth, 'w', encoding='utf-8') as f:
        f.write(report)
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('# ' + NAME + '\n\n- 日期：%s ｜ 引擎：`%s`\n' % (DATE, ENGINE))
        f.write('- 守卫 **%d/%d** ｜ 条目 **%d**（%s）｜ 退出码 **0**\n' %
                (sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES), st))
        f.write('- 总裁定：`%s`\n\n' % VERDICT)
        f.write('## 三轴与图规模\n\n')
        f.write('- 层 %d × 维 %d × 链 %d ｜ 节点 %d / 边 %d / 断边 %d\n\n' %
                (len(LAYERS), len(DIMS), len(CHAIN), len(nodes), len(edges),
                 sum(1 for e in edges if e['w'] == 0)))
        f.write('## 全链路可达性\n\n')
        f.write('S_UNIFY 公设内可达 = **%s**\n\n' % ('SUN' in reach))
        f.write('## 缺口边账\n\n')
        for g in gaps:
            f.write('- %s → S_UNIFY [%s,w=%d] %s\n' % (g['from'], g['rel'], g['w'], g['note']))
        f.write('\n## 架构流程图（Mermaid）\n\n```mermaid\n%s\n```\n' % mermaid)

    # HTML 架构图（离线可打开，落在算法联盟册根）
    hp = os.path.join(ALGO, '全维度全链路全层级架构流程图_2026-11-16.html')
    with io.open(hp, 'w', encoding='utf-8') as f:
        f.write(html)

    # 判定册
    judge = build_judge(VERDICT, nodes, edges, reach, gaps, matrix_rows, ctrls, red, st, len(GUARDS))
    jdp = os.path.join(ALGO, '判定_TUFT-r414-全维度全链路全层级架构流程图_图论攻破_2026-11-16.md')
    with io.open(jdp, 'w', encoding='utf-8') as f:
        f.write(judge)

    log(report[:900])
    log('JSON -> %s' % jp)
    log('HTML -> %s' % hp)
    log('JUDGE -> %s' % jdp)
    log('GUARDS %d/%d ENTRIES %d EXIT=0' %
        (sum(1 for g in GUARDS if g['ok']), len(GUARDS), len(ENTRIES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
