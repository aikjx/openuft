# -*- coding: utf-8 -*-
import os

B = os.path.dirname(os.path.abspath(__file__))
OLD = 'r72_tau鬼场出路与S1符号一致性_修复优化_2026-10-16'
NEW = 'r74_tau鬼场出路与S1符号一致性_修复优化_2026-10-16'
pairs = []
pairs.append((os.path.join(B, '源码', 'TUFT-' + OLD + '.py'),
              os.path.join(B, '源码', 'TUFT-' + NEW + '.py')))
for ext in ('.json', '.md', '_report.txt'):
    pairs.append((os.path.join(B, '数据', 'TUFT-' + OLD + ext),
                  os.path.join(B, '数据', 'TUFT-' + NEW + ext)))
pairs.append((os.path.join(B, '判定_TUFT-r72-tau鬼场出路与S1符号一致性_修复优化_2026-10-16.md'),
              os.path.join(B, '判定_TUFT-r74-tau鬼场出路与S1符号一致性_修复优化_2026-10-16.md')))
for a, b in pairs:
    if os.path.exists(a) and not os.path.exists(b):
        os.rename(a, b)
        print('OK', os.path.basename(a), '->', os.path.basename(b))
    else:
        print('SKIP', os.path.basename(a), os.path.exists(a), os.path.exists(b))
