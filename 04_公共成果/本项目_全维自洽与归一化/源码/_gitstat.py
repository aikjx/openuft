# -*- coding: utf-8 -*-
import subprocess
out = subprocess.run(['git', 'status', '--porcelain'],
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
lines = [l for l in out.split('\n') if l.strip()]
staged = [l for l in lines if l[0] in 'AMDR']
unstaged = [l for l in lines if l[1] in 'MDR' or l[:2] == '??']
print('total status lines:', len(lines))
print('staged (index):', len(staged))
print('unstaged/untracked:', len(unstaged))
cats = {}
for l in staged:
    path = l[3:].strip('"')
    top = path.split('/')[0] if '/' in path else path
    cats[top] = cats.get(top, 0) + 1
print('--- staged by top dir ---')
for k, v in sorted(cats.items(), key=lambda x: -x[1]):
    print(' ', k, v)
r433 = [l for l in lines if 'r433' in l]
print('--- r433 status lines:', len(r433))
for l in r433[:14]:
    print('  ', l[0:2], l[3:][:95])
# 归档解压规模
arch = [l for l in staged if '90_历史归档' in l or '来源语料_ufthub' in l]
print('--- staged archive/unzip files:', len(arch))
