# -*- coding: utf-8 -*-
"""只精确暂存本次我创建的 r433 产物，不碰并发会话的半成品与归档。"""
import subprocess
BASE = '04_公共成果/本项目_全维自洽与归一化'
NAME = 'TUFT-r433_离散输入预置二分定理_口径II过O1不可达与唯一出口复证_精算_2026-11-21'
files = [
    BASE + '/源码/' + NAME + '.py',
    BASE + '/数据/' + NAME + '.json',
    BASE + '/数据/' + NAME + '.md',
    BASE + '/数据/' + NAME + '_report.txt',
    BASE + '/判定/判定_' + NAME + '.md',
    BASE + '/_bak_README_pre_r433.md',
    BASE + '/README.md',
]
# 不含 _reg_r433.py / _verify_r433.py / _gitstat.py（一次性辅助脚本，按项目惯例不入库）
r = subprocess.run(['git', 'add', '--'] + files, capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
print('git add rc:', r.returncode)
if r.stderr:
    print('stderr:', r.stderr[:500])
# 校验这些文件确已 staged
out = subprocess.run(['git', 'status', '--porcelain', '--'] + files,
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
for l in out.split('\n'):
    if l.strip():
        print('  ', l[:2], l[3:][:100])
