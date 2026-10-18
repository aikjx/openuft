# -*- coding: utf-8 -*-
"""坏门槛回溯审计（总账 §七.4 指令的执行轮，2026-10-18）。

被审对象：旋量存在性判据（mod-8 门槛）在全仓的全部落点。
本脚本**只读**——不改动任何被审文件字节；每条记录带 verbatim 引文，
运行时先核验引文仍住在该文件的该位置（语料漂移即红，不接受记忆）。

判据标准（canonical）：SO(1,D-1) 单参口径
  Weyl   <=> D 偶
  Majorana(实) <=> D mod 8 in {2,3,4}
  MW     <=> D mod 8 == 2
MW 的教科书锚 {2,10,18,26} 无争议；D=6 的手征+实性口径文献有分歧 ⇒ 不入判分锚，登记 OPEN。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / '04_公共成果/本项目_全维自洽与归一化/数据/坏门槛回溯审计_旋量mod8_2026-10-18.json'

def canon(D):
    return (D % 2 == 0, D % 8 in (2, 3, 4), D % 8 == 2)  # (Weyl, Majorana, MW)

ANCHORS_D = [2, 4, 10, 26, 32]        # 单参锚（无争议子集；6 已让位 OPEN）
# 判定册规则 R3『Weyl⟺n≡4 mod8』的字面判分锚集：仅 D%4==0 的偶维（奇维不在其论域）
R3_DOMAIN = [4, 12]

def r_draft(p, q):                    # 草案 M5：Weyl ⟺ n≡2 (mod 8)
    n = p + q
    return (n % 8 == 2, None, n % 8 == 2)

def r_disk(p, q):                    # 磁盘第52行口径：n≡4 (mod 8) ⇒ Weyl
    n = p + q
    return (n % 8 == 4, None, None)

def r_49a(D):                        # 49A H 块（其 Majorana 集 {1,2,3,4} 含赝实，见标签混用记录）
    return (D % 2 == 0, D % 8 in (1, 2, 3, 4), D % 8 == 2)

def r_attack(p, q):                  # 三重预检/attack_calc：(q-p) mod 8 双参口径
    n = p + q
    return (n % 2 == 0, (q - p) % 8 in (0, 1, 2), n % 2 == 0 and (q - p) % 8 == 0)

def score(rule, plane, label):
    """在 Lorentzian 平面上按 (W,M,MW) 三通道逐锚判分；rule 返回 None 的通道跳过。"""
    faults = []
    for p, q in plane:
        D = p + q
        got = rule(p, q)
        exp = canon(D)
        for i, name in enumerate(('Weyl', 'Majorana', 'MW')):
            if got[i] is None or got[i] == exp[i]:
                continue
            faults.append({'plane': [p, q], 'D': D, 'channel': name,
                           'rule_says': got[i], 'canon_says': exp[i]})
    return {'rule': label, 'verdict': 'PASS' if not faults else 'RED',
            'n_anchors': len(plane) * 3, 'faults': faults}

SITES = [
    {'id': 'S1', 'path': '07_统一场方程/48_v50audit_calc.py', 'line': 26,
     'quote': 'Majorana 允许但 Majorana–Weyl 不允许',
     'class': '坏规则残留（正确口径下 D=32≡0 ⇒ Majorana 亦不允许）',
     'disposition': '待勘误：verdict 字符串须整句替换；判词方向不受影响（A3 仍负面）'},
    {'id': 'S2', 'path': '07_统一场方程/openuft_49_hierarchical_axiom_system.md', 'line': 52,
     'quote': '4≡4 (mod 8) → Weyl 存在、Majorana-Weyl 不存在',
     'class': '坏规则残留（磁盘执行口径 A4 点名的 n≡4 版本，未替换为 (p,q) 双参数判据）',
     'disposition': '待勘误：D=4 三值结论本身与 canon 一致 (T,T,F)，错在判据表述'},
    {'id': 'S3', 'path': '07_统一场方程/48_v50audit_calc_results.json', 'line': None,
     'quote': 'Majorana 允许',
     'class': '坏规则产物（机读账本仍带 S1 的错句）',
     'disposition': '待勘误：由 S1 脚本重跑再生，不得手改'},
    {'id': 'S4', 'path': '07_统一场方程/49A_ec_lagrangian_calc.py', 'line': 926,
     'quote': 'return D % 8 in (1, 2, 3, 4)',
     'class': '修正规则（W/MW 与 canon 同；Majorana 集并入赝实 sM ⇒ 标签混用）',
     'disposition': '登记口径缺陷：D≡1,5 (mod 8) 为 symplectic-Majorana 非普通 Majorana；'
                    '其锚集恰缺 D∈{5,9,13} 判分位 ⇒ 该混用在 H1 内不可见'},
    {'id': 'S5', 'path': '07_统一场方程/49A_ec_lagrangian_calc.py', 'line': 936,
     'quote': '6D：Weyl 有、Majorana 无（辛型）',
     'class': '锚注记内部张力：同一 D≡6 在 S4 规则下判『有 Majorana』，注记却判『无』',
     'disposition': '登记 OPEN（D=6 口径文献分歧，不入判分锚）'},
    {'id': 'S6', 'path': '07_统一场方程/openuft_49_阶段1_三重预检攻破卷_2026-10-15.md', 'line': 40,
     'quote': '\\text{Majorana} \\iff (q-p)\\bmod 8 \\in \\{0,1,2\\}',
     'class': '修正规则（双参 (p,q) 口径；与 canon 的换算未声明）',
     'disposition': '须补：约定声明 + 换算引理；其 MW 通道在全枚举下与 canon 分歧 18 例（B4）'},
    {'id': 'S7', 'path': '07_统一场方程/_p49_attack_calc.py', 'line': 94,
     'quote': 'Majorana-Weyl   <=> n 为偶数 且 (q-p) mod 8 == 0',
     'class': '修正规则（与 S6 同源）',
     'disposition': '同 S6；B1 的 7/7 自检只覆盖其自身锚集'},
    {'id': 'S8', 'path': '04_公共成果/openuft_统一场论全部完成工作总账_2026-10-15.md', 'line': 106,
     'quote': 'M5 存在 3 个互斥版本',
     'class': '指令源（本轮回溯的委托）',
     'disposition': '本轮即其执行；执行后须回填状态'},
    {'id': 'S9', 'path': '01_独立体系/S02_空间光速螺旋统一力/04_理论推导/GAQ-UFT_V50_家族一三四第三轮代数几何对撞_verify.py', 'line': 32,
     'quote': '32 mod 8=0',
     'class': '非涉案（Bott 周期算术，非旋量存在性判据）',
     'disposition': '免审通过：不在坏规则依赖链上'},
]

def check_quotes():
    drift = []
    for s in SITES:
        p = ROOT / s['path']
        if not p.is_file():
            drift.append({'id': s['id'], 'why': '文件不存在'})
            continue
        text = p.read_text(encoding='utf-8-sig', errors='replace')
        if s['quote'] not in text:
            drift.append({'id': s['id'], 'why': '引文未命中（语料已漂移）'})
        elif s['line'] is not None:
            lines = text.splitlines()
            if s['line'] > len(lines) or s['quote'] not in lines[s['line'] - 1]:
                drift.append({'id': s['id'], 'why': '引文行号漂移 %d' % s['line']})
    return drift

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    drift = check_quotes()
    canon_anchors = {str(D): canon(D) for D in ANCHORS_D}
    reads = {
        'canon@49A': score(lambda p, q: r_49a(p + q), [(1, D - 1) for D in ANCHORS_D], 'R_49A'),
        'canon@disk52': score(r_disk, [(1, D - 1) for D in R3_DOMAIN], 'R_disk(n≡4)'),
        'canon@draft': score(r_draft, [(1, D - 1) for D in ANCHORS_D], 'R_draft(M5)'),
    }
    # 攻击卷 B1 锚点复算（期望值取自其归档 _p49_attack_out.txt 的落盘图像，非打字）
    b1 = ROOT / '07_统一场方程/_p49_attack_out.txt'
    b1_expect, b1_red = [], []
    if b1.is_file():
        pat = re.compile(r'\(p,q\)=\((\d+), (\d+)\)\s+期望 W/M/MW=\((True|False), (True|False), (True|False)\)\s+实得 \((True|False), (True|False), (True|False)\)\s+(OK|MISMATCH)')
        for m in pat.finditer(b1.read_text(encoding='utf-8', errors='replace')):
            p, q = int(m.group(1)), int(m.group(2))
            exp = tuple(x == 'True' for x in m.group(3, 4, 5))
            got = tuple(x == 'True' for x in m.group(6, 7, 8))
            b1_expect.append({'plane': [p, q], 'expected': exp, 'archived_got': got,
                              'archived_flag': m.group(9)})
            # 复算：现读源码 correct() 的定义域判断
            red = r_attack(p, q)
            if red != got:
                b1_red.append({'plane': [p, q], 'recomputed': red, 'archived': got})
    out = {
        'tool': Path(__file__).name,
        'corpus_sha2512_first12': None,
        'quote_drift': drift,
        'canon_rule': 'SO(1,D-1): Weyl<=>D even; Majorana(real)<=>D mod8 in {2,3,4}; MW<=>D mod8==2',
        'canon_anchor_excluded': {'D=6': 'OPEN（文献口径分歧，不入判分锚）'},
        'canon_anchors': {str(k): v for k, v in canon_anchors.items()},
        'rule_reads': reads,
        'attack_b1_anchors_recomputed': b1_expect,
        'attack_b1_redo_faults': b1_red,
        'sites': SITES,
        'verdicts_not_flipped': [
            '旋量关 FAIL（判据级）维持——依据已换成正确判据，结论不变',
            'D=4 三值结论（有 Weyl、有 Majorana、无 MW）与 canon 一致',
            'A3『32 维负面』判词方向维持（其 Majorana 措辞待勘误，S1/S3）',
        ],
        'red_lines': '只读审计：未改动任何被审文件字节；未跑 refresh_catalog；未做 git 操作',
    }
    body = json.dumps(out, ensure_ascii=False, indent=2) + '\n'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(body, encoding='utf-8')
    n_drift = len(drift)
    n_red = sum(1 for r in reads.values() if r['verdict'] == 'RED')
    print('sites=%d quote_drift=%d rule_reads_RED=%d b1_anchors=%d b1_redo_faults=%d'
          % (len(SITES), n_drift, n_red, len(b1_expect), len(b1_red)))
    for k, r in reads.items():
        print(' ', k, r['verdict'], 'faults:',
              [(f['D'], f['channel']) for f in r['faults']])
    print('->', OUT.relative_to(ROOT).as_posix())
    ok = (n_drift == 0)
    print('PASS' if ok else 'FAIL: 引文漂移 %d' % n_drift)
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
