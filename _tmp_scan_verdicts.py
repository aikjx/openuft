# -*- coding: utf-8 -*-
"""扫描攻坚线全部判定册，抽取编号、标题与结论行，供总总结卷引用。"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')

KEY = re.compile(r'(总裁定|元判定|完成度|最终裁定|结论|本册判定|裁定：|判定：|DEAD|ALIVE|'
                 r'新物理、?|机读|守卫 \d|判据 \d+ 条|PASS \d+|FAIL \d+)')

rows = []
for name in sorted(os.listdir(BASE)):
    if not name.startswith('判定_') or not name.endswith('.md'):
        continue
    m = re.search(r'判定_(TUFT-)?(r\d+)', name)
    num = m.group(2) if m else '??'
    body = io.open(os.path.join(BASE, name), encoding='utf-8-sig', errors='replace').read()
    hits = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith('#') or s.startswith('|') or not s:
            continue
        if KEY.search(s):
            hits.append(s[:230])
        if len(hits) >= 4:
            break
    rows.append((num, name[len('判定_'):-3], hits))


def _k(n):
    return int(re.sub(r'\D', '', n) or 0)


rows.sort(key=lambda r: _k(r[0]))
for num, title, hits in rows:
    print('## %s | %s' % (num, title))
    for h in hits:
        print('    - ' + h)
print('TOTAL', len(rows))
