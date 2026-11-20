# -*- coding: utf-8 -*-
"""r407 交付一致性自检：README 两处树登记、文件名对盘、判定册相对链接、行尾。"""
import io
import os
import re

BASE = r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化'
P = BASE + '/README.md'
NAME = 'TUFT-r407_EC挠率源媒介子替代性二分与挠率作为统一力载体不可行性_精算_2026-11-13'

with io.open(P, encoding='utf-8', newline='') as f:
    raw = f.read()
BAK = BASE + '/_bak_README_pre_r407.md'
with io.open(BAK, encoding='utf-8', newline='') as f:
    bak = f.read()
L = raw.split('\n')
eol = '\r\n' if '\r\n' in bak else '\n'
print('EOL style unchanged:', ('\r' in raw) == ('\r' in bak), '| style:', repr(eol), '| lines:', len(L))
assert ('\r' in raw) == ('\r' in bak)

py_hits = [(i + 1, l) for i, l in enumerate(L) if NAME + '.py' in l]
md_hits = [(i + 1, l) for i, l in enumerate(L) if '判定_' + NAME + '.md' in l]
print('README py rows:', [i for i, _ in py_hits], ' md rows:', [i for i, _ in md_hits])
assert len(py_hits) == 1 and len(md_hits) == 1

# 登记行必须紧跟对应的 r406 行（前一行）
py_prev = L[py_hits[0][0] - 2]
md_prev = L[md_hits[0][0] - 2]
print('py row immediately after r406 py:', 'TUFT-r406_继续攻破口径重定义' in py_prev)
print('md row immediately after r406 md:', '判定_TUFT-r406_继续攻破口径重定义' in md_prev)
assert 'TUFT-r406_继续攻破口径重定义' in py_prev
assert '判定_TUFT-r406_继续攻破口径重定义' in md_prev

# 文件名对盘
for rel in ['源码/' + NAME + '.py', '数据/' + NAME + '.json',
            '数据/' + NAME + '.md', '数据/' + NAME + '_report.txt',
            '判定/判定_' + NAME + '.md']:
    fp = os.path.join(BASE, rel.replace('/', os.sep))
    print('DISK', 'OK ' if os.path.isfile(fp) else 'MISS', rel,
          os.path.getsize(fp) if os.path.isfile(fp) else '')

# 判定册相对链接
jd = os.path.join(BASE, '判定')
jf = os.path.join(jd, '判定_' + NAME + '.md')
with io.open(jf, encoding='utf-8') as f:
    jt = f.read()
links = re.findall(r'\]\(([^)]+)\)', jt)
bad = []
for lk in links:
    tgt = os.path.normpath(os.path.join(jd, lk))
    if not os.path.isfile(tgt):
        bad.append(lk)
print('判定册相对链接:', len(links), '失效:', bad)
assert not bad

# 引用判词一致性
rep = os.path.join(BASE, '数据', NAME + '_report.txt')
with io.open(rep, encoding='utf-8') as f:
    rt = f.read()
verdict = [l.split(' ', 1)[1].strip() for l in rt.split('\n') if l.startswith('VERDICT ')][0]
print('VERDICT in report == 判定册:', verdict in jt, '| == README:', verdict in raw)
print('ALL OK')
