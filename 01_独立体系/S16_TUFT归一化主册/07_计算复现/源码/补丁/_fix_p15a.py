# -*- coding: utf-8 -*-
"""P15a 脚本修复：shallowest_root/find_lam_t 最浅根语义（字节级替换，临时脚本）"""
import io

p = r'D:\a10\aikjx\code\my_lib\tuft_core_soft_combo.py'
t = io.open(p, 'r', encoding='utf-8').read()
nl = '\r\n' if '\r\n' in t else '\n'


def rep(old, new, label):
    global t
    c = t.count(old)
    if c == 0:
        print('NOT FOUND:', label)
    else:
        t = t.replace(old, new)
        print('OK x%d:' % c, label)


rep(
    'def shallowest_root(lam_t, lam_om, lam_T, rho_c, lo_e=-3.0, rho_max=30.0):',
    'def shallowest_root(lam_t, lam_om, lam_T, rho_c, lo_e=-6.0, rho_max=30.0):',
    '窗深 -6.0')
rep(
    '    grid = np.linspace(lo_e, 0.0, 33)',
    '    grid = np.linspace(lo_e, 0.0, 51)',
    '网格 51 点')

# shallowest_root 返回语义：P_d 最小 → 最浅根 + P_d 坍缩检测
old_sr = """    if not raw:
        return None
    scored = []
    for r in raw:
        Pd, _, _, _, _ = observables(lam_t, lam_om, lam_T, rho_c, r)
        scored.append((r, Pd))
    scored.sort(key=lambda x: x[1])
    return scored[0][0]"""
new_sr = """    if not raw:
        return (None, None)
    e_shallow = max(raw)
    Pd, _, _, _, _ = observables(lam_t, lam_om, lam_T, rho_c, e_shallow)
    return (e_shallow, Pd)"""
rep(old_sr, new_sr, '最浅根语义')

old_flt = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"\"\"联合重标定：反解 λ_t 使最浅（S 主导）束缚态 ε = eps_target。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。λ_t=0.3 端深、λ_t=2.0 端浅（或无束缚）。\"\"\"
    lo, hi = 0.50, 1.50
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
new_flt = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"\"\"联合重标定：反解 λ_t 使最浅束缚态（S 主导基态） ε = eps_target。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。
    任一 λ_t 处最浅根 P_d>0.3 → 基态坍缩 D 主导 → 该区标定失败。\"\"\"
    lo, hi = 0.30, 2.00
    e_shallow, Pd_sh = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is None:
        return None  # 最弱吸引端也无束缚
    if Pd_sh > 0.3:
        return None  # 最弱吸引端已 D 主导坍缩
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        e_mid, Pd_mid = shallowest_root(mid, lam_om, lam_T, rho_c)
        if e_mid is None:
            hi = mid  # 无束缚（ε 太浅）→ 需更强吸引 → λ_t 更小
        elif Pd_mid > 0.3:
            return None  # 该区基态已坍缩为 D 主导
        elif e_mid > eps_target:
            lo = mid
        else:
            hi = mid
        if hi - lo < 3e-4:
            break
    lam_t = 0.5 * (lo + hi)
    e_fin, Pd_fin = shallowest_root(lam_t, lam_om, lam_T, rho_c)
    if e_fin is None or Pd_fin > 0.3:
        return None
    return (lam_t, e_fin)"""
rep(old_flt, new_flt, 'find_lam_t 重写')

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('saved')
