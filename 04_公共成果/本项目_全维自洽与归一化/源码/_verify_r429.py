# -*- coding: utf-8 -*-
"""r429 交付一致性自检。"""
import io, os, re
BASE = r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化'
NAME = 'TUFT-r429_W3候选可达性二分定理_四门禁体系内不可达与外部来料唯一出口定价_精算_2026-11-21'
P = BASE + '/README.md'
BAK = BASE + '/_bak_README_pre_r429.md'

with io.open(P, encoding='utf-8', newline='') as f:
    raw = f.read()
with io.open(BAK, encoding='utf-8', newline='') as f:
    bak = f.read()
L = raw.split('\n')
print('EOL unchanged:', ('\r' in raw) == ('\r' in bak), '| lines:', len(L))
assert ('\r' in raw) == ('\r' in bak)

py_hits = [i+1 for i, l in enumerate(L) if NAME + '.py' in l]
md_hits = [i+1 for i, l in enumerate(L) if '判定_' + NAME + '.md' in l]
print('README py rows:', py_hits, ' md rows:', md_hits)
assert len(py_hits) == 1 and len(md_hits) == 1
assert 'TUFT-r407_EC挠率源媒介子替代性二分' in L[py_hits[0]-2]
assert '判定_TUFT-r407_EC挠率源媒介子替代性二分' in L[md_hits[0]-2]
print('py/md rows immediately after r407: OK')

for rel in ['源码/'+NAME+'.py', '数据/'+NAME+'.json', '数据/'+NAME+'.md',
            '数据/'+NAME+'_report.txt', '判定/判定_'+NAME+'.md']:
    fp = os.path.join(BASE, rel.replace('/', os.sep))
    print('DISK', 'OK ' if os.path.isfile(fp) else 'MISS', rel, os.path.getsize(fp) if os.path.isfile(fp) else '')

jd = os.path.join(BASE, '判定')
with io.open(os.path.join(jd, '判定_'+NAME+'.md'), encoding='utf-8') as f:
    jt = f.read()
links = re.findall(r'\]\(([^)]+)\)', jt)
bad = [lk for lk in links if not os.path.isfile(os.path.normpath(os.path.join(jd, lk)))]
print('判定册 links:', len(links), 'bad:', bad)
assert not bad

rep = os.path.join(BASE, '数据', NAME+'_report.txt')
with io.open(rep, encoding='utf-8') as f:
    rt = f.read()
verdict = [l.split(' ',1)[1].strip() for l in rt.split('\n') if l.startswith('VERDICT ')][0]
print('VERDICT matches 判定册:', verdict in jt, '| README:', verdict in raw)
print('ALL OK')
