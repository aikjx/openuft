# -*- coding: utf-8 -*-
"""优化 P15a：λ_t 区间收窄 + 二分次数 12 + 窄窗粗网"""
import io
p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
s = io.open(p, encoding='utf-8').read()

# 1) find_lam_t 二分区间与次数
old = """    lo, hi = 0.30, 2.00
    # 浅端（λ_t=2.0）：应为 None（无束缚）或 > target
    e_shallow = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is not None and e_shallow < eps_target:
        return None  # 连最弱吸引都过深（异常）
    for _ in range(16):"""
new = """    lo, hi = 0.50, 1.50
    # 浅端（λ_t=1.5）：应为 None（无束缚）或 > target
    e_shallow = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is not None and e_shallow < eps_target:
        return None  # 连最弱吸引都过深（异常）
    for _ in range(12):"""
assert old in s, 'part1 not found'
s = s.replace(old, new)

# 2) shallowest_root 粗网 41 → 33（步长 0.095），lo_e 保持 -3.0
old2 = """    grid = np.linspace(lo_e, 0.0, 41)"""
new2 = """    grid = np.linspace(lo_e, 0.0, 33)"""
assert old2 in s, 'part2 not found'
s = s.replace(old2, new2)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('optimized OK')
