# -*- coding: utf-8 -*-
"""
_ma_t01_gate_verify.py
T01 硬规格第一关：GR 门双验证（MainAgent 第二独立实现正式证据）
================================================================================
实现：完整 Teukolsky + Cook-Zalutskiy 2014 Leaver 连分数（arXiv:1410.7698）
  - 角向：谱方法（式 52-56），径向：Leaver 连分数（式 21-27, 32a-e, 42-44），
    Nollert 截断（式 34/38 u1..u3），同步牛顿（式 59-60）。
  - 不 import qnm、无硬编码门靶（对照值仅输出用）、零自由常数。
门禁：
  门 A：a=0, l=2, m=2, n=0 基模 >= 11.6 位（靶 0.37367168441804166-0.08896231568893410i）
  门 B：splitR/a -> 0.2515323（>=4 位，Richardson a^2/a^4 外推）
门未全过 => TUFT 旋转极点一律 UNTRUSTED，禁读物理。
"""
import math
import numpy as np
from _ma_kerr_leaver_full import solve_qnm, radial_cf, angular_sep_const

print("="*72)
print("T01 门验证 · MainAgent 第二独立实现（完整 Teukolsky + Leaver）")
print("="*72)

# ---- 门 A：独立收敛（从偏离初值出发）----
print("\n[门 A] a=0, l=2, m=2, n=0（从偏离初值 0.3700-0.0900i 独立收敛）")
T_A = 0.37367168441804166 - 0.08896231568893410j
wA = solve_qnm(0.0, -2, 2, 2, 0, w_guess=0.3700-0.0900j, tol=1e-14)
errA = abs(wA - T_A)
digA = -math.log10(errA)
print(f"  独立解: w = {wA.real:.15f} {wA.imag:+.15f}i")
print(f"  靶    : {T_A.real:.15f} {T_A.imag:+.15f}i")
print(f"  |err| = {errA:.3e}  有效位数 = {digA:.1f}  ({'PASS >= 11.6' if digA >= 11.6 else 'FAIL'})")
# 连分数残留复核
f_check = radial_cf(wA, 0.0, -2, 2, 2, angular_sep_const(0.0, -2, 2, 2), 0)
print(f"  连分数残留 |Cf(w)| = {abs(f_check):.3e}")

# ---- 门 B：小 a m 频裂，Richardson 外推 ----
print("\n[门 B] splitR/a -> 0.2515323（Richardson a^2/a^4 外推）")
T_B = 0.2515323
grid = [0.005, 0.01, 0.02, 0.04, 0.08]
res = {}
wp = None; wm = None
for a in grid:
    wp = solve_qnm(a, -2, 2, +2, 0, w_guess=wp or T_A, tol=1e-14)
    wm = solve_qnm(a, -2, 2, -2, 0, w_guess=wm or T_A, tol=1e-14)
    res[a] = (wp, wm)
    print(f"  a={a:6.3f}: splitR/a={(wp.real-wm.real)/a:+.8f}")
aa = np.array(grid)
ss = np.array([(res[a][0].real-res[a][1].real)/a for a in grid])
c_lin = np.polyfit(aa**2, ss, 1)[1]
c_4   = np.polyfit((aa**2)[:3], ss[:3], 2)[2]
for name, c0 in [("a^2 线性", c_lin), ("a^4 四截断", c_4)]:
    err = abs(c0 - T_B)
    d = -math.log10(err) if err > 0 else 20
    print(f"  {name}外推: splitR/a = {c0:+.8f}  err={err:.2e}  {d:.1f} 位 ({'PASS >= 4' if d >= 4 else 'FAIL'})")

# 等价 per-m 斜率
sp = np.polyfit(aa**2, [(res[a][0].real-0.37367168441804166)/a for a in grid], 1)[1]
print(f"  per-m prograde dRe/da (a->0) = {sp:+.8f}（由 split=2*slope 等价应为 {c_4/2:+.8f}，"
      f"与 qnm c_rot.real=0.0628831 差 {abs(sp-c_4/2):.1e}）")

print("\n" + "="*72)
ok = digA >= 11.6 and (-math.log10(abs(c_4-T_B)) if abs(c_4-T_B)>0 else 20) >= 4
print(f"总判定: {'GR 门 A/B 双 PASS —— 求解器可信，可扩展 TUFT 反射壁' if ok else 'FAIL'}")
print("="*72)
