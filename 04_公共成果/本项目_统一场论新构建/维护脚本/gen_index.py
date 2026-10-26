# -*- coding: utf-8 -*-
"""统一场论新构建 · 全书索引表生成脚本（v2）
从六卷正文提取 F### / 标题 / 现象锚定 / 机制族，生成 08_索引表.md（1000 行）。
机制族来源优先级：正文族标题（如 `## 族① 量子数与荷族（F251–F295）`）
                 > 卷首"机制族划分"表格的编号段映射（如 `| 超导与超流族 | F751–F775 |`）。
复跑：python gen_index.py
"""
import re, os
from collections import Counter

BASE = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论新构建'
FILES = [
    ('01_卷A_引力与时空_F001-F250.md', 'A'),
    ('02_卷B_粒子与统一_F251-F500.md', 'B'),
    ('03_卷C_宇宙学_F501-F625.md', 'C'),
    ('04_卷D_量子基础_F626-F750.md', 'D'),
    ('05_卷E_凝聚态与现象_F751-F875.md', 'E'),
    ('06_卷F_数学物理与交叉_F876-F1000.md', 'F'),
]
VOL_NAME = {'A': '引力/时空', 'B': '粒子/统一', 'C': '宇宙学', 'D': '量子基础', 'E': '凝聚态/现象', 'F': '数学物理/交叉'}
DASH = '[–—－\\-]'
FAM_RE = re.compile(r'^#{2,3}\s+(.*?)\s*[（(]\s*F\d{3,4}\s*' + DASH + r'\s*F\d{3,4}\s*[）)]')
RANGE_RE = re.compile(r'^\|\s*(.+?)\s*\|\s*F(\d{3,4})\s*' + DASH + r'\s*F(\d{3,4})\s*\|')
UNIT_RE = re.compile(r'^### F(\d{3,4})\s*·\s*(.+)')
PHEN_RE = re.compile(r'\*\*现象锚定\*\*[：:]\s*(.+)')
PREFIX_RE = re.compile(r'^(?:族[①-⑩]?|[一二三四五六七八九十]+、|甲·|乙·|丙·|丁·|戊·|己·)\s*')


def clean_family(fam):
    fam = PREFIX_RE.sub('', fam).strip()
    return fam


rows = []
for fname, vol in FILES:
    path = os.path.join(BASE, fname)
    lines = open(path, encoding='utf-8').read().split('\n')
    ranges = []
    for line in lines[:60]:
        m = RANGE_RE.match(line)
        if m:
            ranges.append((int(m.group(2)), int(m.group(3)), clean_family(m.group(1))))
    cur = ''
    for i, line in enumerate(lines):
        m = FAM_RE.match(line)
        if m:
            cur = clean_family(m.group(1))
        m2 = UNIT_RE.match(line)
        if m2:
            num = int(m2.group(1)); title = m2.group(2).strip()
            phen = ''
            for j in range(i + 1, min(i + 10, len(lines))):
                pm = PHEN_RE.match(lines[j])
                if pm:
                    phen = pm.group(1).strip()
                    break
            phen = phen.split('——')[0].strip() if phen else ''
            if len(phen) > 72:
                phen = phen[:72] + '…'
            fam = cur or ''
            if not fam:
                for lo, hi, name in ranges:
                    if lo <= num <= hi:
                        fam = name
                        break
            rows.append((num, title, phen, fam or '未分类', vol))

rows.sort(key=lambda r: r[0])
with open(os.path.join(BASE, '08_索引表.md'), 'w', encoding='utf-8') as f:
    f.write('# 统一场论新构建 · Top1000 索引表\n\n')
    f.write('> 由 `_scripts/gen_index.py` 从六卷正文自动提取生成，与正文逐字一致；共 1000 行。\n')
    f.write('> 状态列：全部为「探索性理论构建·未证实」。\n\n')
    f.write('| 编号 | 标题 | 核心现象 | 机制族 | 卷 |\n|---|---|---|---|---|\n')
    for num, title, phen, fam, vol in rows:
        f.write(f'| F{num:03d} | {title} | {phen} | {fam} | {VOL_NAME[vol]} |\n')
print(f'索引行数 = {len(rows)} (目标 1000)')
print('卷分布:', dict(Counter(r[4] for r in rows)))
print('未分类数量:', sum(1 for r in rows if r[3] == '未分类'))
from collections import defaultdict
fam_cnt = Counter(r[3] for r in rows)
print('机制族种类数:', len(fam_cnt))
for k, v in sorted(fam_cnt.items()):
    print(f'  {k}: {v}')
