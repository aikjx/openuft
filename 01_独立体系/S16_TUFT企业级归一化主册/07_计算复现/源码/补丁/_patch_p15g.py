# -*- coding: utf-8 -*-
"""P15a 修复：shallowest_root 返回全根中 P_d 最小（S 主导）者；坍缩判定基于它"""
import io
p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
s = io.open(p, encoding='utf-8').read()

# 1) shallowest_root：收集全部根 → 返回 (S 主导根, P_d)
old = """    if not raw:
        return (None, None)
    e_shallow = max(raw)
    Pd, _, _, _, _ = observables(lam_t, lam_om, lam_T, rho_c, e_shallow)
    return (e_shallow, Pd)"""
new = """    if not raw:
        return (None, None)
    scored = []
    for r in raw:
        Pd, _, _, _, _ = observables(lam_t, lam_om, lam_T, rho_c, r)
        scored.append((r, Pd))
    scored.sort(key=lambda x: x[1])  # P_d 最小 = S 主导
    return (scored[0][0], scored[0][1])"""
assert old in s, 'part1 not found'
s = s.replace(old, new)

# 2) find_lam_t：坍缩判定针对 S 主导根（注释更新；逻辑本身用 Pd_sh>0.3 即可）
old2 = """    \"\"\"联合重标定：反解 λ_t 使最浅束缚态（S 主导基态） ε = eps_target。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。
    任一 λ_t 处最浅根 P_d>0.3 → 基态坍缩 D 主导 → 该区标定失败。\"\"\" """
new2 = """    \"\"\"联合重标定：反解 λ_t 使 S 主导基态 ε = eps_target。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。
    任一 λ_t 处 S 主导根 P_d>0.3 → 基态坍缩 D 主导 → 该区标定失败。\"\"\" """
assert old2 in s, 'part2 not found'
s = s.replace(old2, new2)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('fixed OK')
