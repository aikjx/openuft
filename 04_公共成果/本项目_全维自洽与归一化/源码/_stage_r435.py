# -*- coding: utf-8 -*-
"""只精确暂存本次 r435 产物与 README，不碰并发会话半成品与辅助脚本。"""
import subprocess
BASE = '04_公共成果/本项目_全维自洽与归一化'
NAME = 'TUFT-r435_账基组选择反解定理_口径不变性元层边界与离散输入来源轴再定价_精算_2026-11-21'
files = [
    BASE + '/源码/' + NAME + '.py',
    BASE + '/数据/' + NAME + '.json',
    BASE + '/数据/' + NAME + '.md',
    BASE + '/数据/' + NAME + '_report.txt',
    BASE + '/判定/判定_' + NAME + '.md',
    BASE + '/_bak_README_pre_r435.md',
    BASE + '/README.md',
]
r = subprocess.run(['git', 'add', '--'] + files, capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
print('git add rc:', r.returncode)
out = subprocess.run(['git', 'status', '--porcelain', '--'] + files,
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
for l in out.split('\n'):
    if l.strip():
        print('  ', l[:2], l[3:][:90])
# 确认 index 里没有并发会话的半成品（r434 之后的其他 rNNN）
allout = subprocess.run(['git', 'status', '--porcelain'],
                        capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
staged = [l for l in allout.split('\n') if l.strip() and l[0] in 'AMDR']
print('staged total:', len(staged))
susp = [l for l in staged if ('ROOT_V119' in l or '_dim_units' in l or 'r433_量纲' in l)]
print('suspicious staged (should be 0):', len(susp))
