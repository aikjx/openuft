# -*- coding: utf-8 -*-
"""修补 find_lam_t 边界逻辑"""
import io
p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
s = io.open(p, encoding='utf-8').read()
old = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"""联合重标定：反解 λ_t 使最浅（S 主导）束缚态 ε = eps_target。
    ε(λ_t) 单调递减（λ_t↑ 吸引↑ ε↓）→ 二分；无束缚时快退。\"""
    lo, hi = 0.30, 2.00
    e_hi = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_hi is None:
        return None  # 最强吸引也无束缚
    if e_hi > eps_target:
        return None  # 最强吸引也达不到目标深度"""
new = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"""联合重标定：反解 λ_t 使最浅（S 主导）束缚态 ε = eps_target。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。λ_t=0.3 端深、λ_t=2.0 端浅（或无束缚）。\"""
    lo, hi = 0.30, 2.00
    e_shallow = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is not None and e_shallow < eps_target:
        return None  # 连最弱吸引都过深（异常）"""
assert old in s, 'old not found'
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched OK')
