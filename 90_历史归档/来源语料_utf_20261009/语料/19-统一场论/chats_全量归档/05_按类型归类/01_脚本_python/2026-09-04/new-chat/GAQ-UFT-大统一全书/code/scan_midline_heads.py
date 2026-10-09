# -*- coding: utf-8 -*-
"""扫描所有非行首位置出现的 ## / ### 标题标记（粘连在正文行中间）。"""
import io, glob, os, re

MS = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书\manuscript'

pat = re.compile(r'(#{2,3})\s+([^\n]{0,60})')
total = 0
for p in sorted(glob.glob(os.path.join(MS, 'ch*.md'))):
    with io.open(p, encoding='utf-8') as f:
        lines = f.read().split('\n')
    for i, ln in enumerate(lines):
        # 行首本身是标题（## / ### 开头）则跳过；只查行中间的
        stripped = ln.lstrip()
        if stripped.startswith(('#', '>', '|', '-', '*', '`')):
            continue
        for m in pat.finditer(ln):
            if m.start() == 0:
                continue
            # 若该标记前紧邻的是另一个 #（如 #####）则忽略
            if m.start() > 0 and ln[m.start()-1] == '#':
                continue
            total += 1
            pre = ln[max(0, m.start()-15):m.start()]
            print(f'{os.path.basename(p)[:6]} L{i+1} ...{pre}||{m.group(0)[:55]}')
print('--- mid-line headings:', total)
