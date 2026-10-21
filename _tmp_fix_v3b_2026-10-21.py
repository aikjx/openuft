# -*- coding: utf-8 -*-
"""v3 修复续作：根暂存区归档 + 归档内英文子目录改名 + 判定册断链与量纲写法修复。

上一版在删除中文路径 scratch/ 时被运行环境的回收站钩子截断（FileNotFoundError），
本版改为「先搬空、再 os.rmdir」，并补跑未执行的链接编辑。
"""
import os
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


# ---------- 1) 归档区内英文子目录改名（verify 只对 90_历史归档/来源语料_* 豁免命名） ----------
RENAMES = [
    (os.path.join(ARCH, '公共成果暂存区', '_misr104'), os.path.join(ARCH, '公共成果暂存区', 'r104_错位件')),
    (os.path.join(ARCH, '公共成果暂存区', '_misr109'), os.path.join(ARCH, '公共成果暂存区', 'r109_错位件')),
]
for old, new in RENAMES:
    if os.path.isdir(old):
        os.rename(old, new)
        log.append('RENAME %s -> %s' % (_rel(old), _rel(new)))

# ---------- 2) 根暂存区归档 ----------
src = os.path.join(ROOT, 'scratch')
if os.path.isdir(src):
    dst_root = os.path.join(ARCH, '根暂存区')
    for dirpath, dirnames, filenames in os.walk(src):
        rel = os.path.relpath(dirpath, src)
        sub = 'r129_错位产出_2026-10-20' if rel == 'r129_misplaced_outputs_2026-10-20' else rel
        dst_dir = dst_root if rel == '.' else os.path.join(dst_root, sub)
        os.makedirs(dst_dir, exist_ok=True)
        for name in filenames:
            s = os.path.join(dirpath, name)
            d = os.path.join(dst_dir, name)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.move(s, d)
            log.append('MOVE  %s -> %s' % (_rel(s), _rel(d)))
    for dirpath, dirnames, filenames in os.walk(src, topdown=False):
        try:
            os.rmdir(dirpath)
            log.append('RMDIR %s' % (_rel(dirpath) + '/'))
        except OSError as exc:
            log.append('WARN  无法删除 %s：%s' % (_rel(dirpath), exc))

# ---------- 3) r104/r105/r106/r109 判定册回链修复 ----------
R84 = '判定_TUFT-r84-X-R82-2定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md'
SPEC = {
    '判定_TUFT-r104-Clifford几何统一候选_模稳定与呼吸模预言_2026-10-18.md': [
        ('](TUFT-r104_Clifford几何统一候选_模稳定与呼吸模预言_攻破_2026-10-18.py)',
         '](源码/TUFT-r104_Clifford几何统一候选_模稳定与呼吸模预言_攻破_2026-10-18.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)', '](%s)' % R84),
    ],
    '判定_TUFT-r105-Clifford几何统一候选_模稳定与景观约束_2026-10-18.md': [
        ('](TUFT-r105_Clifford几何统一候选_模稳定与景观约束_攻破_2026-10-18.py)',
         '](源码/TUFT-r105_Clifford几何统一候选_模稳定与景观约束_攻破_2026-10-18.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)', '](%s)' % R84),
    ],
    '判定_TUFT-r106-Clifford几何统一候选_模稳定与景观约束与非SUSY统一_2026-10-19.md': [
        ('](TUFT-r106_Clifford几何统一候选_模稳定与景观约束与非SUSY统一_攻破_2026-10-19.py)',
         '](源码/TUFT-r106_Clifford几何统一候选_模稳定与景观约束与非SUSY统一_攻破_2026-10-19.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)', '](%s)' % R84),
    ],
    '判定_TUFT-r109-Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.md': [
        ('](TUFT-r109_Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.py)',
         '](源码/TUFT-r109_Clifford几何统一候选_模稳定与景观约束与非SUSY统一构造_2026-10-19.py)'),
        ('](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-18.md)', '](%s)' % R84),
    ],
}


def _bytes_replace(path, pairs):
    with open(path, 'rb') as f:
        raw = f.read()
    before = raw
    for old, new in pairs:
        o, n = old.encode('utf-8'), new.encode('utf-8')
        if o not in raw:
            log.append('WARN  %s: 未找到片段 %r' % (_rel(path), old))
            continue
        raw = raw.replace(o, n)
    if raw != before:
        with open(path, 'wb') as f:
            f.write(raw)
        log.append('EDIT  %s' % _rel(path))


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

print('=== 修复动作 %d 条 ===' % len(log))
for line in log:
    print(' ', line)
print('--- 复核 ---')
print('根 scratch 存在:', os.path.isdir(os.path.join(ROOT, 'scratch')))
print('公共成果 scratch 存在:', os.path.isdir(os.path.join(BASE, 'scratch')))
