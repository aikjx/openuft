# -*- coding: utf-8 -*-
"""只精确暂存 r437 产物与 README，不碰并发会话半成品与辅助脚本。"""
import subprocess
BASE = '04_公共成果/本项目_全维自洽与归一化'
NAME = 'TUFT-r437_E2修法后果与分类学开放性定理_实证完备非逻辑完备与出口闭合性再审计_精算_2026-11-21'
files = [
    BASE + '/源码/' + NAME + '.py',
    BASE + '/数据/' + NAME + '.json',
    BASE + '/数据/' + NAME + '.md',
    BASE + '/数据/' + NAME + '_report.txt',
    BASE + '/判定/判定_' + NAME + '.md',
    BASE + '/_bak_README_pre_r437.md',
    BASE + '/README.md',
]
r = subprocess.run(['git', 'add', '--'] + files, capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
print('git add rc:', r.returncode)
out = subprocess.run(['git', 'status', '--porcelain', '--'] + files,
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
for l in out.split('\n'):
    if l.strip():
        print('  ', l[:2], l[3:][:88])
allout = subprocess.run(['git', 'status', '--porcelain'],
                        capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
staged = [l for l in allout.split('\n') if l.strip() and l[0] in 'AMDR']
print('staged total:', len(staged))
print('unexpected staged (not r437/README/bak):',
      [l[3:][:70] for l in staged if 'r437' not in l and 'README.md' not in l][:10])
