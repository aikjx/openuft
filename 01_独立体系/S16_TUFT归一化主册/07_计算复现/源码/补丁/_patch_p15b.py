# -*- coding: utf-8 -*-
"""修复 find_lam_t：无束缚时二分方向应 hi=mid（需更强吸引）"""
import io
p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
s = io.open(p, encoding='utf-8').read()
old = """        e_mid = shallowest_root(mid, lam_om, lam_T, rho_c)
        if e_mid is None:
            lo = mid  # 无束缚 → 需更强吸引
        elif e_mid > eps_target:
            lo = mid"""
new = """        e_mid = shallowest_root(mid, lam_om, lam_T, rho_c)
        if e_mid is None:
            hi = mid  # 无束缚（ε 太浅）→ 需更强吸引 → λ_t 更小
        elif e_mid > eps_target:
            lo = mid"""
assert old in s, 'old not found'
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched OK')
