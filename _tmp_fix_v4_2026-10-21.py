# -*- coding: utf-8 -*-
"""v4 修复：资料索引指向已归档暂存区的旧路径、判定册括号链接截断、r109 源码册名、
71/72 卷的 ../ 层数与书籍 README 缺失。"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')
log = []


def _rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


def _repl(path, pairs):
    if not os.path.isfile(path):
        log.append('WARN 缺件 %s' % _rel(path))
        return
    with open(path, 'rb') as f:
        raw = f.read()
    before = raw
    for old, new in pairs:
        o, n = old.encode('utf-8'), new.encode('utf-8')
        if o not in raw:
            log.append('WARN %s 未找到 %r' % (_rel(path), old[:60]))
            continue
        raw = raw.replace(o, n)
    if raw != before:
        with open(path, 'wb') as f:
            f.write(raw)
        log.append('EDIT %s' % _rel(path))


# 1) 资料索引：暂存区已归档，旧路径整体改写
cat = os.path.join(ROOT, '00_项目治理', '资料索引', 'material_catalog.md')
_repl(cat, [
    ('../../04_公共成果/本项目_全维自洽与归一化/scratch/_misr104/',
     '../../90_历史归档/暂存区归档_2026-10-21/公共成果暂存区/r104_错位件/'),
    ('../../04_公共成果/本项目_全维自洽与归一化/scratch/_misr109/',
     '../../90_历史归档/暂存区归档_2026-10-21/公共成果暂存区/r109_错位件/'),
    ('../../04_公共成果/本项目_全维自洽与归一化/scratch/',
     '../../90_历史归档/暂存区归档_2026-10-21/公共成果暂存区/'),
    ('../../scratch/r129_misplaced_outputs_2026-10-20/',
     '../../90_历史归档/暂存区归档_2026-10-21/根暂存区/r129_错位产出_2026-10-20/'),
    ('../../scratch/', '../../90_历史归档/暂存区归档_2026-10-21/根暂存区/'),
])

# 2) r104 判定册：册名含 Cl(1,11)，裸括号被 markdown 在首个 ) 处截断链接
_repl(os.path.join(BASE, '判定_TUFT-r104-Clifford几何统一候选_模稳定与呼吸模预言_2026-10-18.md'), [
    ('](判定_TUFT-r102-Clifford几何统一候选_κτ拓扑不变量化与Cl(1,11)广义联络_2026-10-18.md)',
     '](<判定_TUFT-r102-Clifford几何统一候选_κτ拓扑不变量化与Cl(1,11)广义联络_2026-10-18.md>)'),
])

# 3) r109 判定册：源码册名漏了 _攻破
_repl(os.path.join(BASE, '判定_TUFT-r109-Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.md'), [
    ('源码/TUFT-r109_Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.py',
     '源码/TUFT-r109_Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_攻破_2026-10-19.py'),
])

# 4) 71/72 卷：位于 07_统一场方程/ 一层深处，回上层只需一个 ../
for name in ('71_全链路总览卷_2026-10-20.md', '72_本质本源审计卷_2026-10-20.md'):
    _repl(os.path.join(ROOT, '07_统一场方程', name), [
        ('](../../04_公共成果/本项目_全维自洽与归一化/判定_TUFT-r137-全链路总览卷与本质本源审计卷_全维审计_2026-10-21.md)',
         '](../04_公共成果/本项目_全维自洽与归一化/判定_TUFT-r137-全链路总览卷与本质本源审计卷_全维审计_2026-10-21.md)'),
        ('](../../书籍/03_宇宙的本源_统一场论全书/README.md)',
         '](../书籍/03_宇宙的本源_统一场论全书/00_卷首.md)'),
    ])

print('=== 修复动作 %d 条 ===' % len(log))
for line in log:
    print(' ', line)
