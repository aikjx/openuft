# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书\deliverables\final.md'
with io.open(p, encoding='utf-8') as f:
    txt = f.read()

checks = [
    ('137.035999084', 'CODATA alpha'),
    ('4.16561', '力比'),
    ('2.38922', 'mP/me'),
    ('0.666660511466', 'Koide Q'),
    ('4.847', 'Hubble sigma'),
    ('5.68', 'dH0'),
    ('0.9985', 'CKM 第一行'),
    ('0.2232', 'sin2thetaW'),
    ('0.02242', 'Omega_b'),
    ('0.11933', 'Omega_c'),
    ('67.36', 'H0'),
    ('13.797', '年龄'),
    ('3434', 'z_eq'),
    ('OPEN-D1', 'OPEN-D1'),
    ('OPEN-G1', 'OPEN-G1'),
    ('OPEN-M1', 'OPEN-M1'),
    ('B1', '断裂点 B1'),
    ('【审计框', '审计框'),
    ('【大白话', '大白话'),
    ('V1', '验收实验 V1'),
    ('V2', '验收实验 V2'),
    ('V3', '验收实验 V3'),
]
allok = True
for s, name in checks:
    found = s in txt
    if not found:
        allok = False
    print('  %s: %s' % (name, 'OK' if found else 'MISS'))
print('=== final.md 关键内容:', 'ALL OK' if allok else 'HAS MISSES')
print('final.md 大小:', len(txt.encode('utf-8')), 'bytes')
bad = sum(1 for ln in txt.split('\n')
          if re.match(r'^## \d+\.\d+ ', ln) and len(ln) > 105)
print('final.md 中超长标题行:', bad)
# 标题总数
heads = [ln for ln in txt.split('\n') if re.match(r'^(##|###) ', ln)]
print('final.md 标题总数:', len(heads))
