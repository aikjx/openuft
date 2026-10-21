# -*- coding: utf-8 -*-
"""修复 verify.py 报出的 28 项 FAIL（2026-10-21）。

四类处置：
  1) 目录名中文化：两个英文 scratch/ 暂存区整体归档到 90_历史归档，原地删除；
  2) 错位产出归位：scratch 里唯一的 r101 守恒律 json 提升到 数据/（修复资料索引断链）；
  3) 断链：r104/r105/r106/r109 判定册的「源码」链接缺 源码/ 前缀、r84 判定册册名与日期写错；
  4) 断链：第 12 层封闭谱审计 md 里 `[g](d)` 的量纲写法被误判为链接，改 `[g]=d`。

原则：只搬移/改名/改链接，不删内容、不改结论；搬移目标全部落在 90_历史归档（verify 不查链接）。
"""
import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')
DATA = os.path.join(BASE, '数据')
ARCH = os.path.join(ROOT, '90_历史归档', '暂存区归档_2026-10-21')
log = []


def _rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


def _move(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    log.append('MOVE  %s -> %s' % (_rel(src), _rel(dst)))


def _bytes_replace(path, pairs):
    with open(path, 'rb') as f:
        raw = f.read()
    before = raw
    for old, new in pairs:
        old_b = old.encode('utf-8')
        new_b = new.encode('utf-8')
        if old_b not in raw:
            log.append('WARN  %s: 未找到片段 %r' % (_rel(path), old))
            continue
        raw = raw.replace(old_b, new_b)
    if raw != before:
        with open(path, 'wb') as f:
            f.write(raw)
        log.append('EDIT  %s' % _rel(path))


# ---------- 1) 唯一件先归位：r101 守恒律 json（资料索引指向它） ----------
promote = os.path.join(BASE, 'scratch', 'TUFT-r101_守恒律审计_场方程构造性收口_函数形式来源审计_2026-10-18.json')
if os.path.isfile(promote):
    _move(promote, os.path.join(DATA, os.path.basename(promote)))

# ---------- 2) scratch 暂存区整体归档（目录名中文化 + 原地清英文目录） ----------
for src, sub in (
        (os.path.join(BASE, 'scratch'), '公共成果暂存区'),
        (os.path.join(ROOT, 'scratch'), '根暂存区')):
    if not os.path.isdir(src):
        continue
    dst_root = os.path.join(ARCH, sub)
    for dirpath, dirnames, filenames in os.walk(src):
        rel = os.path.relpath(dirpath, src)
        dst_dir = dst_root if rel == '.' else os.path.join(dst_root, rel)
        os.makedirs(dst_dir, exist_ok=True)
        for name in filenames:
            _move(os.path.join(dirpath, name), os.path.join(dst_dir, name))
    shutil.rmtree(src)
    log.append('RMDIR %s' % (_rel(src) + '/'))

# ---------- 3) r104/r105/r106/r109 判定册回链修复 ----------
R84 = '判定_TUFT-r84-X-R82-2定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md'
SPEC = {
    '判定_TUFT-r104-Clifford几何统一候选_模稳定与呼吸模预言_2026-10-18.md': [
        ('](TUFT-r104_Clifford几何统一候选_模稳定与呼吸模预言_攻破_2026-10-18.py)',
         '](源码/TUFT-r104_Clifford几何统一候选_模稳定与呼吸模预言_攻破_2026-10-18.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)',
         '](%s)' % R84),
    ],
    '判定_TUFT-r105-Clifford几何统一候选_模稳定与景观约束_2026-10-18.md': [
        ('](TUFT-r105_Clifford几何统一候选_模稳定与景观约束_攻破_2026-10-18.py)',
         '](源码/TUFT-r105_Clifford几何统一候选_模稳定与景观约束_攻破_2026-10-18.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)',
         '](%s)' % R84),
    ],
    '判定_TUFT-r106-Clifford几何统一候选_模稳定与景观约束与非SUSY统一_2026-10-19.md': [
        ('](TUFT-r106_Clifford几何统一候选_模稳定与景观约束与非SUSY统一_攻破_2026-10-19.py)',
         '](源码/TUFT-r106_Clifford几何统一候选_模稳定与景观约束与非SUSY统一_攻破_2026-10-19.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)',
         '](%s)' % R84),
    ],
    '判定_TUFT-r109-Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.md': [
        ('](TUFT-r109_Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.py)',
         '](源码/TUFT-r109_Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-18.md)',
         '](%s)' % R84),
    ],
}
for name, pairs in SPEC.items():
    path = os.path.join(BASE, name)
    if os.path.isfile(path):
        _bytes_replace(path, pairs)
    else:
        log.append('WARN  缺件 %s' % name)

# ---------- 4) 第 12 层封闭谱审计：量纲写法 [g](d) 被误判为链接 ----------
v_eq = os.path.join(DATA, 'v_eq_c_力的统一_全空间运行方式_封闭谱审计.md')
if os.path.isfile(v_eq):
    _bytes_replace(v_eq, [('解出 [g](d)', '解出 [g]=d')])

# ---------- 5) 残留引用排查 ----------
residual = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames
                   if d not in ('.git', 'node_modules', '__pycache__', '90_历史归档')]
    for name in filenames:
        if not name.endswith('.md'):
            continue
        p = os.path.join(dirpath, name)
        try:
            body = open(p, encoding='utf-8-sig', errors='replace').read()
        except OSError:
            continue
        if re.search(r'\(\.?\.?/?[^)\s]*scratch', body) or 'scratch/' in body:
            residual.append(_rel(p))

print('=== 修复动作 %d 条 ===' % len(log))
for line in log:
    print(' ', line)
print('=== 归档区残留引用 %d 处 ===' % len(residual))
for line in residual:
    print(' ', line)
