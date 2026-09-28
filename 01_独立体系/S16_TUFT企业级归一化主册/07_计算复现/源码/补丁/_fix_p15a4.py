# -*- coding: utf-8 -*-
"""P15a 修复 4：find_lam_t 改为查表插值（扫 λ_t 表 → S 主导点 → 跨 target 线性插值）"""
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


old_flt = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"\"\"联合重标定：反解 λ_t 使最浅束缚态（S 主导基态） ε = eps_target。
    ε(λ_t) 单调：λ_t 小 → 吸引强 → ε 深。
    任一 λ_t 处最浅根 P_d>0.3 → 基态坍缩 D 主导 → 该区标定失败。\"\"\"
    lo, hi = 0.30, 2.00
    e_shallow, Pd_sh = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is not None and Pd_sh > 0.3:
        return None  # 最弱吸引端已 D 主导坍缩 → 全区无 S 基态
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

new_flt = """def find_lam_t(lam_om, lam_T, rho_c, eps_target=EPS_TARGET):
    \"\"\"联合重标定（查表插值）：扫描 λ_t 表记录 S 主导点 (ε, P_d<0.3)，
    找跨 eps_target 的相邻点线性插值 λ_t。
    λ_t<~0.7 时基态坍缩 D 主导（P_d→1，跳过）；λ_t>~1.05 无束缚。\"\"\"
    LTS = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70,
           0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    pts = []
    for lt in LTS:
        e, Pd = shallowest_root(lt, lam_om, lam_T, rho_c)
        if e is not None and Pd < 0.3:
            pts.append((lt, e))
    if not pts:
        return None
    for i in range(len(pts) - 1):
        lt1, e1 = pts[i]
        lt2, e2 = pts[i + 1]
        if (e1 - eps_target) * (e2 - eps_target) <= 0:
            lam_t = lt1 + (lt2 - lt1) * (eps_target - e1) / (e2 - e1)
            e_fin, Pd_fin = shallowest_root(lam_t, lam_om, lam_T, rho_c)
            if e_fin is not None and Pd_fin < 0.3:
                return (lam_t, e_fin)
    return None"""

rep(old_flt, new_flt, 'find_lam_t 查表插值')

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('saved')
