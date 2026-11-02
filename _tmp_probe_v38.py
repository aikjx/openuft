# -*- coding: utf-8 -*-
import os, glob, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = os.path.join(r'd:\a10\aikjx\code\my_lib\openuft', '04_公共成果', '本项目_全维自洽与归一化')
src = os.path.join(BASE, '源码')
jud = sorted(glob.glob(os.path.join(BASE, '判定_*.md')))
print('judge count', len(jud))
for x in jud[-8:]:
    print('  J', os.path.basename(x))
rs = []
for f in glob.glob(os.path.join(src, '*.py')):
    b = os.path.basename(f)
    m = re.match(r'TUFT-r(\d+)_', b)
    if m:
        rs.append((int(m.group(1)), b))
rs.sort()
print('max r =', rs[-1][0] if rs else None)
for a, b in rs[-12:]:
    print('  S', a, b)
# 检查 V38 主题是否已有
hits = []
for f in glob.glob(os.path.join(BASE, '**', '*.md'), recursive=True):
    try:
        t = open(f, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    for kw in ('圆偏振', '椭圆偏振', 'pp-wave', 'pp 波', 'ROOT V38', 'V38'):
        if kw in t:
            hits.append((os.path.basename(f), kw))
            break
print('V38/偏振/pp-wave 命中文件数:', len(hits))
for h in hits[:25]:
    print('  H', h)
