# -*- coding: utf-8 -*-
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化', '数据')
FILES = [
    'TUFT-r119_统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.json',
    'TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.json',
    'TUFT-r133_修补失敗元原理_修改逐个审计与结构不可修补定理_2026-10-20.json',
    'TUFT-r135_第一性原理突破尝试_无质量自旋2导出EH与SEP及净前提下降门机检_2026-10-21.json',
    'TUFT-r138_硬核审计_规范群与mu2符号的第一性原理可导出性精算_2026-10-21.json',
]


def walk(obj, prefix='', depth=0):
    if depth > 2:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            print('  ' * depth + '%s%s: %s' % (prefix, k, type(v).__name__))
            if isinstance(v, (dict, list)) and depth < 2:
                walk(v, '', depth + 1)
    elif isinstance(obj, list):
        print('  ' * depth + '[len=%d]' % len(obj))
        if obj and depth < 2:
            walk(obj[0], '', depth + 1)


for f in FILES:
    p = os.path.join(DATA, f)
    print('=' * 70)
    print(f[:60])
    try:
        d = json.loads(io.open(p, encoding='utf-8').read())
    except Exception as exc:
        print('LOAD FAIL', exc)
        continue
    walk(d)
