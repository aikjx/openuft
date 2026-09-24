# -*- coding: utf-8 -*-
r"""R11 选择定则的**外部**变异核验：从引擎外面改那几条算术，看谁变红。

为什么要有这个脚本：R11 的判据（$N\mid 3Q$）此前只在引擎内部被自己的门禁对照过，
"把它写错会不会有人发现"只存在于某一次对话的口头里 —— 而一个没人能重跑的读数等于没人看守。
本脚本把 `验证脚本/so10_reps.py` 连同它的依赖 `so10_chain.py` 整份复制进临时目录，
在副本上植入缺陷，再重跑整台引擎（副本的产出只落在它自己的目录里，不碰仓库那份报告），
要求三件事同时成立：

  * 基线（未植入）全绿，且它打印的门禁总数与磁盘上 `SO10表示论报告.json` 里的 `tests`
    条数**相等** —— 这条不是装饰：引擎的层是短路接线的（`sel_ok = run_selection_layer() if res_ok`），
    依赖缺失时它会只跑前几层就退出，若只要求"退出码非 0"就会把这种夹具塌陷当成捕获；
  * 每个变异体都必须被**点名到 R11.x** 的 FAIL 抓住（崩溃不算捕获），且它打印的读数至少动一个
    —— 门禁 PASS 数、或报告 §10 那句"允许 X 条、禁戒 Y 条"。这一条不是形式：只动三条路径里
    浮点那条的滑倒**不动**判决表（甲/乙仍然同意），动的是"甲乙丙一致"那条断言 $\\Rightarrow$
    同一个数为什么要三台互不共享算术的机器各跑一遍，这里有一次实测读数；
  * 一条良性改动（只补尾注释，语义不动）不得误报，否则这台仪器是"永远红"而不是"能红"。

用法：python 维护脚本/check_r11_mutation.py    （约数分钟：一台引擎 = 一次完整自检）
产出：与维护脚本同目录的 check_r11_mutation.json（本脚本是唯一写入者）
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, '..', '验证脚本'))
TARGET = os.path.join(ENGINE, 'so10_reps.py')
DEPS = ('so10_chain.py', 'so10_reps.py')
OUT = os.path.join(HERE, 'check_r11_mutation.json')

TOTAL_RE = re.compile(r'（(\d+) 项，PASS (\d+)）')
FAIL_RE = re.compile(r'\[FAIL\]\s+(R\d+\.\d+[a-z]*)')
PAIR_RE = re.compile(r'允许 (\d+) 条、禁戒 (\d+) 条')
BLOCK = '低能算符的选择规则（R11）'

# 锚点：每条都必须在源文件里**恰好出现一次**，否则整轮判 INVALID（锚点漂了不等于没植入）。
A_JIA = (b'    return int(t3) % n == 0', b'    return int(t3 / 3) % n == 0')
A_BING = (b'        ang = 2.0 * math.pi * float(a) * float(q)',
          b'        ang = math.pi * float(a) * float(q)')
A_T3Q = (b'    return sum(3 * f_bl(f) for f in fl)', b'    return 3 * f_bl(fl[0])')
A_HIT = (b"    hit4 = [x for x in c4 if x['singlet'] > 0]",
         b"    hit4 = [x for x in c4 if x['zero'] > 0]")
A_OK = (b'    return None if t3.denominator != 1 else int(t3) % 3',
        b'    return None if t3.denominator != 1 else int(t3) % 3  # inert: benign case')

CASES = [
    ('ctl', '基线：不植入', 'baseline', None),
    ('m1', '甲：同余式右移一位，把 N|3Q 写成 N|Q（只动三条路径里的整除那条）', 'mutant', A_JIA),
    ('m2', '丙：浮点那条把 2pi 周期写成 pi 半周期（只动三条路径里的浮点那条）', 'mutant', A_BING),
    ('m3', '荷账丢掉求和号：sum_k 3(B-L)_k 写成只取第一条场', 'mutant', A_T3Q),
    ('m4', '枚举改用 R11.1 那个错 projector 的零权当筛选条件', 'mutant', A_HIT),
    ('b1', '良性：给 f_tri 补一条尾部注释（语义不动）', 'benign', A_OK),
]


def read_source():
    with open(TARGET, 'rb') as fh:
        return fh.read()


def engine_json_tests():
    """磁盘上那份报告 JSON 的 tests 条数：基线打印的门禁数必须与它相等，否则夹具塌陷。"""
    p = os.path.join(ENGINE, 'SO10表示论报告.json')
    if not os.path.exists(p):
        return None
    with io.open(p, encoding='utf-8') as fh:
        return len(json.load(fh).get('tests') or [])


def build(tag, patch):
    """临时目录 = 整台引擎的一份可跑副本；patch 为 None 时是基线。"""
    d = os.path.join(tempfile.mkdtemp(prefix='am_r11_%s_' % tag), 'engine')
    os.makedirs(d)
    hits = 0
    for f in DEPS:
        src = os.path.join(ENGINE, f)
        with open(src, 'rb') as fh:
            b = fh.read()
        if f == 'so10_reps.py' and patch:
            hits = b.count(patch[0])
            b = b.replace(patch[0], patch[1])
        with open(os.path.join(d, f), 'wb') as fh:
            fh.write(b)
    return d, hits


def run(d):
    r = subprocess.run([sys.executable, os.path.join(d, 'so10_reps.py')], cwd=d,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode('utf-8', 'replace')
    rep = ''
    rp = os.path.join(d, 'SO10表示论报告.md')
    if os.path.exists(rp):
        with io.open(rp, encoding='utf-8') as fh:
            rep = fh.read()
    m = TOTAL_RE.search(out)
    return {'exit': r.returncode,
            'gates': int(m.group(1)) if m else None,
            'pass': int(m.group(2)) if m else None,
            'fail_ids': FAIL_RE.findall(out),
            'r11_fail_ids': [x for x in FAIL_RE.findall(out) if x.startswith('R11')],
            'printed_r11_block': BLOCK in out,
            'report_pairs': sorted(set(tuple(int(x) for x in t) for t in PAIR_RE.findall(rep))),
            'traceback': 'Traceback' in out}


def judge(case, res, base):
    kind = case[2]
    clean = (res['exit'] == 0 and res['pass'] == res['gates'] and not res['fail_ids']
             and not res['traceback'] and res['printed_r11_block'] and bool(res['report_pairs']))
    if kind in ('baseline', 'benign'):
        return clean and (kind == 'baseline'
                          or (res['report_pairs'] == base['report_pairs']
                              and res['pass'] == base['pass']))
    moved = [k for k, v in (('report_pairs', res['report_pairs'] != base['report_pairs']),
                            ('gates_pass', res['pass'] != base['pass'])) if v]
    res['moved'] = moved
    return res['exit'] != 0 and bool(res['r11_fail_ids']) and not res['traceback'] and bool(moved)


def main():
    src = read_source()
    anchors = {}
    for _, _, _, patch in CASES:
        if patch:
            anchors[patch[0].decode()] = src.count(patch[0])
    tests_on_disk = engine_json_tests()

    res = {}
    for tag, name, kind, patch in CASES:
        d, hits = build(tag, patch)
        try:
            r = run(d)
        finally:
            shutil.rmtree(os.path.dirname(d), ignore_errors=True)
        r.update({'id': tag, 'claim': name, 'kind': kind, 'anchor_hits': hits if patch else 0})
        r['expect_caught'] = kind == 'mutant'
        res[tag] = r
        print('[case] %s %-14s exit=%s gates=%s/%s r11fail=%s pairs=%s' %
              (tag, kind, r['exit'], r['pass'], r['gates'], r['r11_fail_ids'], r['report_pairs']))

    anchor_bad = [k for k, v in anchors.items() if v != 1]
    fixture_bad = (res['ctl']['gates'] is None or (tests_on_disk is not None
                   and res['ctl']['gates'] != tests_on_disk))
    for tag, r in res.items():
        r['ok'] = (not anchor_bad and not fixture_bad) and judge(
            next(c for c in CASES if c[0] == tag), r, res['ctl'])
        if r['expect_caught']:
            print('[moved] %s %s' % (tag, r.get('moved')))
    missed = [t for t, r in res.items() if r['expect_caught'] and not r['ok']]
    false_alarm = [t for t, r in res.items() if not r['expect_caught'] and not r['ok']]
    verdict = 'CAUGHT' if not missed and not false_alarm and not anchor_bad and not fixture_bad \
        else 'INVALID'
    payload = {'script': 'check_r11_mutation.py', 'target': '验证脚本/so10_reps.py',
               'target_bytes': len(src), 'engine_json_tests': tests_on_disk,
               'anchor_counts': anchors, 'fixture_ok': not fixture_bad,
               'cases_total': len(CASES), 'mutants': sum(1 for c in CASES if c[2] == 'mutant'),
               'benign': sum(1 for c in CASES if c[2] == 'benign'),
               'caught': sum(1 for t, r in res.items() if r['expect_caught'] and r['ok']),
               'missed': missed, 'false_alarm': false_alarm,
               'baseline_pairs': res['ctl']['report_pairs'], 'verdict': verdict,
               'cases': [res[t] for t, _, _, _ in CASES]}
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print('结论：%s ｜ %d 例（变异体 %d、良性 %d）｜ 基线报告读数 %s ｜ 台账 %s' %
          (verdict, len(CASES), payload['mutants'], payload['benign'],
           res['ctl']['report_pairs'], os.path.basename(OUT)))
    print('自检：%s（%d 例，PASS %d）' %
          ('全部通过' if verdict == 'CAUGHT' else '存在未捕获或误报', len(CASES),
           sum(1 for r in res.values() if r['ok'])))
    return 0 if verdict == 'CAUGHT' else 1


if __name__ == '__main__':
    sys.exit(main())
