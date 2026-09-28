# -*- coding: utf-8 -*-
"""P15a 脚本修复 2：find_lam_t 入口检查语义（None=无束缚≠失败，继续二分）"""
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


old = """    lo, hi = 0.30, 2.00
    e_shallow, Pd_sh = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is None:
        return None  # 最弱吸引端也无束缚
    if Pd_sh > 0.3:
        return None  # 最弱吸引端已 D 主导坍缩"""
new = """    lo, hi = 0.30, 2.00
    e_shallow, Pd_sh = shallowest_root(hi, lam_om, lam_T, rho_c)
    if e_shallow is not None and Pd_sh > 0.3:
        return None  # 最弱吸引端已 D 主导坍缩 → 全区无 S 基态"""
rep(old, new, '入口检查修正')

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('saved')
