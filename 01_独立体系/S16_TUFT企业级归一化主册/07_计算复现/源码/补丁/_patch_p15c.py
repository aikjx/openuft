# -*- coding: utf-8 -*-
"""修复 shallowest_root：收集所有根，按 P_d 选 S 主导（分支选择）"""
import io
p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
s = io.open(p, encoding='utf-8').read()
old = """def shallowest_root(lam_t, lam_om, lam_T, rho_c, lo_e=-3.0, rho_max=30.0):
    \"\"\"从 ε=0 向下找最浅束缚根：粗网定位 + 细网确认 + 二分。\"\"\"
    grid = np.linspace(lo_e, 0.0, 41)
    Fs = [match_det(lam_t, lam_om, lam_T, rho_c, e, rho_max) for e in grid]
    for i in range(len(grid) - 1):
        if Fs[i] * Fs[i + 1] < 0:
            a, b = grid[i], grid[i + 1]
            fa = Fs[i]
            # 细网确认（防止假过零）
            fine = np.linspace(a, b, 17)
            Ff = [match_det(lam_t, lam_om, lam_T, rho_c, e, rho_max) for e in fine]
            for j in range(len(fine) - 1):
                if Ff[j] * Ff[j + 1] < 0:
                    a2, b2 = fine[j], fine[j + 1]
                    fa2 = Ff[j]
                    for _ in range(40):
                        m = 0.5 * (a2 + b2)
                        if match_det(lam_t, lam_om, lam_T, rho_c, m, rho_max) * fa2 < 0:
                            b2 = m
                        else:
                            a2 = m
                    return 0.5 * (a2 + b2)
            # 粗网过零但细网无 → 奇异点，跳过
    return None"""
new = """def shallowest_root(lam_t, lam_om, lam_T, rho_c, lo_e=-3.0, rho_max=30.0):
    \"\"\"扫描 [lo_e, 0] 内全部束缚根，按 P_d 排序返回 S 主导（P_d 最小）根。
    解决强耦合下 D 主导浅根与 S 主导深根的分支选择问题。\"\"\"
    grid = np.linspace(lo_e, 0.0, 41)
    Fs = [match_det(lam_t, lam_om, lam_T, rho_c, e, rho_max) for e in grid]
    raw = []
    for i in range(len(grid) - 1):
        if Fs[i] * Fs[i + 1] < 0:
            a, b = grid[i], grid[i + 1]
            fa = Fs[i]
            fine = np.linspace(a, b, 17)
            Ff = [match_det(lam_t, lam_om, lam_T, rho_c, e, rho_max) for e in fine]
            for j in range(len(fine) - 1):
                if Ff[j] * Ff[j + 1] < 0:
                    a2, b2 = fine[j], fine[j + 1]
                    fa2 = Ff[j]
                    for _ in range(40):
                        m = 0.5 * (a2 + b2)
                        if match_det(lam_t, lam_om, lam_T, rho_c, m, rho_max) * fa2 < 0:
                            b2 = m
                        else:
                            a2 = m
                    raw.append(0.5 * (a2 + b2))
                    break
    if not raw:
        return None
    scored = []
    for r in raw:
        Pd, _, _, _, _ = observables(lam_t, lam_om, lam_T, rho_c, r)
        scored.append((r, Pd))
    scored.sort(key=lambda x: x[1])
    return scored[0][0]"""
assert old in s, 'old not found'
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched OK')
