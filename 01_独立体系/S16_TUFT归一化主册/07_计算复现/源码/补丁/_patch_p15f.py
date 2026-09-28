# -*- coding: utf-8 -*-
"""P15a 重构：s_roots 分支跟踪（最接近 eps_prev 的根）+ find_lam_t 连续性二分"""
import io
p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
s = io.open(p, encoding='utf-8').read()

# ---- 1) 替换 s_roots：取最接近 eps_prev 的根（分支跟踪语义）----
old_sroots = """def s_roots(lam_t, lam_om, lam_T, rho_c, eps_prev, rho_max=30.0):
    \"\"\"S 主导分支根（P_d 最小者为 S 主导 → 排序后取第一个）。窄窗两级扫描。\"\"\"
    lo, hi = eps_prev - 0.5, eps_prev + 0.02
    grid = np.linspace(lo, hi, 61)
    Fs = np.array([match_det(lam_t, lam_om, lam_T, rho_c, e, rho_max) for e in grid])
    roots = []
    for i in range(len(grid) - 1):
        if Fs[i] * Fs[i + 1] < 0:
            a, b = grid[i], grid[i + 1]
            fa = Fs[i]
            for _ in range(40):
                m = 0.5 * (a + b)
                if match_det(lam_t, lam_om, lam_T, rho_c, m, rho_max) * fa < 0:
                    b = m
                else:
                    a = m
            roots.append(0.5 * (a + b))
    if not roots:
        return []
    # 用 P_d 排序，取 S 主导（P_d 最小）
    scored = []
    for r in roots:
        Pd, _, _, _, _ = observables(lam_t, lam_om, lam_T, rho_c, r)
        scored.append((r, Pd))
    scored.sort(key=lambda x: x[1])
    return [scored[0][0]]"""
new_sroots = """def s_roots(lam_t, lam_om, lam_T, rho_c, eps_prev, rho_max=30.0):
    \"\"\"分支跟踪：在 [eps_prev-0.5, eps_prev+0.02] 内找全部根，取最接近 eps_prev 者。
    eps_prev 由相邻 λ 点的解提供 → 连续跟踪 S 主导分支（P13 已验证方法）。\"\"\"
    lo, hi = eps_prev - 0.5, eps_prev + 0.02
    grid = np.linspace(lo, hi, 61)
    Fs = np.array([match_det(lam_t, lam_om, lam_T, rho_c, e, rho_max) for e in grid])
    roots = []
    for i in range(len(grid) - 1):
        if Fs[i] * Fs[i + 1] < 0:
            a, b = grid[i], grid[i + 1]
            fa = Fs[i]
            for _ in range(40):
                m = 0.5 * (a + b)
                if match_det(lam_t, lam_om, lam_T, rho_c, m, rho_max) * fa < 0:
                    b = m
                else:
                    a = m
            roots.append(0.5 * (a + b))
    if not roots:
        return []
    roots.sort(key=lambda r: abs(r - eps_prev))
    return [roots[0]]"""
assert old_sroots in s, 's_roots NOT FOUND'
s = s.replace(old_sroots, new_sroots)

# ---- 2) 替换 find_lam_t：从浅端 λ_t=1.5 起步的连续性二分 ----
old_find = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"\"\"联合重标定：反解 λ_t 使最浅（S 主导）束缚态 ε = eps_target。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。λ_t=0.3 端深、λ_t=2.0 端浅（或无束缚）。\"\"\"
    lo, hi = 0.50, 1.50
    # 浅端（λ_t=1.5）：应为 None（无束缚）或 > target
    e_shallow = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is not None and e_shallow < eps_target:
        return None  # 连最弱吸引都过深（异常）
    for _ in range(12):
        mid = 0.5 * (lo + hi)
        e_mid = shallowest_root(mid, lam_om, lam_T, rho_c)
        if e_mid is None:
            hi = mid  # 无束缚（ε 太浅）→ 需更强吸引 → λ_t 更小
        elif e_mid > eps_target:
            lo = mid
        else:
            hi = mid
        if hi - lo < 3e-4:
            break
    lam_t = 0.5 * (lo + hi)
    eps = shallowest_root(lam_t, lam_om, lam_T, rho_c)
    return (lam_t, eps) if eps is not None else None"""
new_find = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"\"\"联合重标定（分支跟踪版）：λ_t 从浅端 1.5 起，ε 用上一步作种子连续跟踪。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。\"\"\"
    lo, hi = 0.50, 1.50
    # 起点：λ_t=1.5 的 S 根（浅束缚区，分支清晰）
    eps_prev = shallowest_root(hi, lam_om, lam_T, rho_c, lo_e=-1.0)
    if eps_prev is None:
        eps_prev = -0.05  # 无束缚则给一个浅种子，向下探测
    for _ in range(12):
        mid = 0.5 * (lo + hi)
        roots = s_roots(mid, lam_om, lam_T, rho_c, eps_prev)
        if not roots:
            # 窗内无根：向更深探测（张量/中心共同深移）
            roots = s_roots(mid, lam_om, lam_T, rho_c, eps_prev - 1.0)
            if not roots:
                roots = s_roots(mid, lam_om, lam_T, rho_c, eps_prev - 2.0)
                if not roots:
                    return None  # 无束缚
        eps = roots[0]
        eps_prev = eps
        if eps > eps_target:
            lo = mid
        else:
            hi = mid
        if hi - lo < 3e-4:
            break
    lam_t = 0.5 * (lo + hi)
    roots = s_roots(lam_t, lam_om, lam_T, rho_c, eps_prev)
    if not roots:
        roots = s_roots(lam_t, lam_om, lam_T, rho_c, eps_prev - 1.0)
    return (lam_t, roots[0]) if roots else None"""
assert old_find in s, 'find_lam_t NOT FOUND'
s = s.replace(old_find, new_find)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('refactored OK')
