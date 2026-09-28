# -*- coding: utf-8 -*-
"""P15a 精确修补：λ_t 区间 [0.5,1.5]、二分 12 次、粗网 33 点"""
import io
p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
s = io.open(p, encoding='utf-8').read()

pairs = [
    ("lo, hi = 0.30, 2.00", "lo, hi = 0.50, 1.50"),
    ("    for _ in range(16):", "    for _ in range(12):"),
    ("grid = np.linspace(lo_e, 0.0, 41)", "grid = np.linspace(lo_e, 0.0, 33)"),
]
for old, new in pairs:
    assert old in s, 'NOT FOUND: ' + old
    s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched OK x%d' % len(pairs))
