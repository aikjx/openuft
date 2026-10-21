# -*- coding: utf-8 -*-
import io, re, sys

ROOT = 'D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_统一场论攻破'
STAGING = ROOT + '/Top1000_分片'
OUT = ROOT + '/布局_物理Top1000难题攻破清单_2026-10-21.md'

parts = [
    STAGING + '/_母册主体.md',
    STAGING + '/_母册引言.md',
    STAGING + '/域G_引力与时空扩展_T101-T220.md',
    STAGING + '/域H_粒子物理与统一扩展_T221-T380.md',
    STAGING + '/域I_宇宙学扩展_T381-T500.md',
    STAGING + '/域J_量子基础扩展_T501-T590.md',
    STAGING + '/域K_凝聚态与复杂扩展_T591-T730.md',
    STAGING + '/域L_数学物理与理论框架扩展_T731-T810.md',
    STAGING + '/域MNO_核物理AMO天体交叉_T811-T1000.md',
    STAGING + '/_母册收尾.md',
]

buf = []
for p in parts:
    with io.open(p, encoding='utf-8') as f:
        buf.append(f.read())

with io.open(OUT, 'w', encoding='utf-8', newline='') as f:
    f.write(''.join(buf))
print('merged OK ->', OUT)

# ---- verification ----
txt = io.open(OUT, encoding='utf-8').read()
rows = re.findall(r'^\| T(\d{3}) ', txt, re.M)
nums = [int(x) for x in rows]
print('rows=', len(nums), 'min=', min(nums), 'max=', max(nums), 'dups=', len(nums) - len(set(nums)))
missing = [n for n in range(1, 1001) if n not in set(nums)]
print('missing_count=', len(missing), 'missing_sample=', missing[:20])
