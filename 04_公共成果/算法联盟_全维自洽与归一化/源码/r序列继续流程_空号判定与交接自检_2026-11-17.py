# -*- coding: utf-8 -*-
# r 序列继续流程：找最新完整册、读取 next_target、验证下一号是否可用。
# 用法：
#   python -B 源码/r序列继续流程_空号判定与交接自检_2026-11-17.py
#   python -B 源码/r序列继续流程_空号判定与交接自检_2026-11-17.py --r r417
#   python -B 源码/r序列继续流程_空号判定与交接自检_2026-11-17.py --json
# 纯标准库；只读，不写仓内文件；不改动任何 r 册。
import os
import io
import re
import sys
import ast
import json
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.path.join(PUB, '数据')
SRC = os.path.join(PUB, '源码')
README = os.path.join(PUB, 'README.md')

R_PATTERN = re.compile(r'(?<![0-9])r([0-9]+)(?=[-_])')
DATE = '2026-11-17'


def read_text(path):
    return io.open(path, encoding='utf-8').read()


def find_one(folder, prefix, suffixes=None):
    if not os.path.isdir(folder):
        return None
    for name in sorted(os.listdir(folder)):
        if not name.startswith(prefix):
            continue
        if suffixes is None or any(name.endswith(s) for s in suffixes):
            return os.path.join(folder, name)
    return None


def scan_occupied():
    occupied = set()
    for folder in (PUB, SRC, DATA):
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            for m in R_PATTERN.finditer(name):
                occupied.add(int(m.group(1)))
    return occupied


def record_for(rnum):
    rr = 'r' + str(rnum)
    judge = find_one(PUB, '判定_TUFT-' + rr + '-', ['.md'])
    engine = find_one(SRC, 'TUFT-' + rr + '_', ['.py'])
    js = find_one(DATA, 'TUFT-' + rr + '_', ['.json'])
    dm = find_one(DATA, 'TUFT-' + rr + '_', ['.md'])
    report = find_one(DATA, 'TUFT-' + rr + '_', ['_report.txt'])
    paths = {'judge': judge, 'engine': engine, 'json': js, 'md': dm, 'report': report}
    complete = all(p and os.path.isfile(p) for p in paths.values())
    return {'r': rr, 'number': rnum, 'paths': paths, 'complete': complete}


def latest_complete(occupied):
    records = []
    for n in sorted(occupied):
        rec = record_for(n)
        if rec['complete']:
            records.append(rec)
    if not records:
        return None
    return records[-1]


def r_number(value):
    if value is None:
        return None
    m = re.search(r'([0-9]+)', str(value))
    return int(m.group(1)) if m else None


def next_free(start, occupied):
    n = start
    while n in occupied:
        n += 1
    return n


def check_source(path):
    try:
        ast.parse(read_text(path))
        return True, 'ok'
    except Exception as exc:
        return False, str(exc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--r', help='指定要检查的册号，如 r417；缺省取最新完整册')
    ap.add_argument('--json', action='store_true', help='输出机器可读 JSON')
    args = ap.parse_args()

    occupied = scan_occupied()
    if args.r:
        wanted = r_number(args.r)
        if wanted is None:
            print('BAD_R_ARG ' + str(args.r))
            raise SystemExit(2)
        current = record_for(wanted)
    else:
        current = latest_complete(occupied)

    checks = []
    def ck(name, ok, reading):
        checks.append({'name': name, 'ok': bool(ok), 'reading': str(reading)})

    if current is None or not current['complete']:
        print('NO_COMPLETE_RECORD')
        raise SystemExit(2)

    paths = current['paths']
    ck('五件套完整', current['complete'], current['r'])

    engine_ok, engine_reading = check_source(paths['engine'])
    ck('引擎 AST', engine_ok, engine_reading)

    payload = {}
    json_ok = False
    try:
        payload = json.loads(read_text(paths['json']))
        json_ok = True
    except Exception as exc:
        json_ok = False
        engine_reading = str(exc)
    ck('JSON 可解析', json_ok, engine_reading if not json_ok else payload.get('schema', 'ok'))

    verdict = str(payload.get('verdict', ''))
    guard_pass = payload.get('guard_pass')
    guard_total = payload.get('guard_total')
    ck('守卫闭环', guard_pass == guard_total and guard_total is not None, str(guard_pass) + '/' + str(guard_total))

    report_txt = read_text(paths['report'])
    expected_summary = 'GUARD_SUMMARY ' + str(guard_pass) + '/' + str(guard_total)
    ck('报告守卫读数一致', expected_summary in report_txt, expected_summary)

    judge_txt = read_text(paths['judge'])
    ck('判定册含 verdict', verdict in judge_txt and len(verdict) > 20, str(len(verdict)))

    readme_txt = read_text(README)
    ck('README 含 verdict', verdict in readme_txt and len(verdict) > 20, str(len(verdict)))

    next_target = payload.get('next_target') or {}
    ck('next_target 存在', bool(next_target), next_target.get('r', 'MISSING'))

    target_num = r_number(next_target.get('r'))
    if target_num is None:
        target_num = current['number'] + 1
    target_free = target_num not in occupied
    ck('目标号未占用', target_free, 'r' + str(target_num) + (' free' if target_free else ' occupied'))
    recommended = next_free(target_num, occupied)

    bad_token = chr(36) + '{'
    self_src = read_text(__file__)
    ck('无禁用占位符语法', bad_token not in self_src, '0')

    handoff = {
        'date': DATE,
        'current_r': current['r'],
        'current_verdict': verdict,
        'guards': str(guard_pass) + '/' + str(guard_total),
        'files': paths,
        'next_target': next_target,
        'recommended_r': 'r' + str(recommended),
        'occupied_count': len(occupied),
        'max_occupied_r': 'r' + str(max(occupied)),
        'checks': checks,
        'all_ok': all(c['ok'] for c in checks),
    }

    if args.json:
        print(json.dumps(handoff, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print('CURRENT_R ' + current['r'])
        print('VERDICT ' + verdict)
        print('GUARDS ' + str(guard_pass) + '/' + str(guard_total))
        print('NEXT_TARGET ' + str(next_target.get('r', 'UNKNOWN')) + ' | ' + str(next_target.get('topic', 'UNKNOWN')))
        print('RECOMMENDED_R r' + str(recommended))
        print('MAX_OCCUPIED r' + str(max(occupied)) + ' OCCUPIED_COUNT ' + str(len(occupied)))
        for c in checks:
            print(('[OK] ' if c['ok'] else '[BAD] ') + c['name'] + ' | ' + c['reading'])
        print('HANDOFF_OK ' + str(handoff['all_ok']))

    if not handoff['all_ok']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
