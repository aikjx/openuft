# -*- coding: utf-8 -*-
"""临时补丁：把 r59 判定册中的条目号与报告产物实际编号对齐（每处须唯一命中）"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

P = (r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/'
     u'判定_TUFT-r59-圆柱螺旋增量复核与作用量系数_全维审计_2026-10-13.md')

PAIRS = [
    (u'**A09（INFO，本册新增延伸）**', u'**A10（INFO，本册新增延伸）**'),
    (u'**A10（BOUNDARY，与库内 O-SCALE / M02 同构）**', u'**A11（BOUNDARY，与库内 O-SCALE / M02 同构）**'),
    (u'**A11（FAIL＝来料判断成立）**', u'**A12（FAIL＝来料判断成立）**'),
    (u'**A12（FAIL——假选项，本册对来料的唯一实质性反驳）**', u'**A13（FAIL——假选项，本册对来料的唯一实质性反驳）**'),
    (u'**A14（本册新增，PASS）**', u'**A15（本册新增，PASS）**'),
    (u'**A15（FAIL——归因不成立）**', u'**A16（FAIL——归因不成立）**'),
    (u'**A16（PASS，交叉印证）**', u'**A17（PASS，交叉印证）**'),
    (u'**A23（INFO）**：「逗号代替乘号」', u'**A24（INFO）**：「逗号代替乘号」'),
    (u'**A24（INFO）**：来料 §1 称第 2 组', u'**A25（INFO）**：来料 §1 称第 2 组'),
    (u'### A27–A28 回归与阳性对照', u'### A27–A28 阳性对照与回归'),
    (u'**A27（PASS）**：本册 ', u'**A28（PASS）**：本册 '),
    (u'**A28（PASS）**：**阳性对照**', u'**A27（PASS）**：**阳性对照**'),
]

t = io.open(P, encoding='utf-8').read()
total = 0
for a, b in PAIRS:
    c = t.count(a)
    total += c
    flag = 'OK' if c == 1 else ('MISS' if c == 0 else 'DUP%d' % c)
    print('%s  %s' % (flag, a[:56]))
    t = t.replace(a, b)
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('total_hits=%d' % total)
