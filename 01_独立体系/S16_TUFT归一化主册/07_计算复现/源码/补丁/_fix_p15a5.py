# -*- coding: utf-8 -*-
"""P15a 提速：λ_t 表 9 点 + shallowest_root 减网格"""
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


rep('    LTS = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70,\n'
    '           0.75, 0.80, 0.85, 0.90, 0.95, 1.00]',
    '    LTS = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]',
    'λ_t 表 9 点')
rep('    grid = np.linspace(lo_e, -0.005, 51)',
    '    grid = np.linspace(lo_e, -0.005, 41)',
    'det 网格 41')
rep('            fine = np.linspace(a, b, 17)',
    '            fine = np.linspace(a, b, 13)',
    '细扫 13 点')
rep('                    for _ in range(40):',
    '                    for _ in range(30):',
    '二分 30 次')

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('saved')
