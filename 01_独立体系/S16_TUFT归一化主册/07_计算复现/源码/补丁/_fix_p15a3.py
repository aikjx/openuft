# -*- coding: utf-8 -*-
"""P15a 修复 3：shallowest_root 扫描上界 −0.005（排除 ε=0 假过零根）"""
import io

p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
t = io.open(p, 'r', encoding='utf-8').read()


def rep(old, new, label):
    global t
    c = t.count(old)
    if c == 0:
        print('NOT FOUND:', label)
    else:
        t = t.replace(old, new)
        print('OK x%d:' % c, label)


rep('    grid = np.linspace(lo_e, 0.0, 51)',
    '    grid = np.linspace(lo_e, -0.005, 51)',
    '扫描上界 -0.005（排除假过零）')

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('saved')
