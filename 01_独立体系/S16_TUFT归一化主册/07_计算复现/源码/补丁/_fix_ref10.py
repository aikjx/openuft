# -*- coding: utf-8 -*-
"""认证总览第 10 行引用修正（临时脚本）"""
import io

p2 = r'D:\a10\aikjx\code\my_lib\本项目_TUFT核力分支认证总览_v1.md'
t = io.open(p2, 'r', encoding='utf-8').read()

old = '| 10 | `tuft_core_soft_tensor.py` / `.png` | 张量短程软化机制测试（无斥心） | 弱耦合深束缚/强耦合坍缩——单 π 型不足 |'
new = '| 10 | `tuft_core_soft_tensor.py` | 张量短程软化机制测试（无斥心，数值见 §2.8/P15 结果 A；PNG 因环境中断未生成） | 弱耦合深束缚/强耦合坍缩——单 π 型不足 |'

c = t.count(old)
if c:
    t = t.replace(old, new)
    print('OK x%d' % c)
else:
    print('NOT FOUND')
io.open(p2, 'w', encoding='utf-8', newline='').write(t)
