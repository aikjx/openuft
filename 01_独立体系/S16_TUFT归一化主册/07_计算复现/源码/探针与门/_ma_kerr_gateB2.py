# -*- coding: utf-8 -*-
"""
_ma_kerr_gateB2.py
GR 门 B v2：Richardson a^2 外推（splitR/a = c0 + c1 a^2 + c2 a^4）
目标：c0 -> 0.2515323（>=4 位）。网格取小 a。
"""
import math
import numpy as np
from _ma_kerr_leaver_full import solve_qnm

TARGET = 0.2515323

grid = [0.005, 0.01, 0.02, 0.04, 0.08]
w0 = 0.37367168441804166 - 0.08896231568893410j
res = {}
wp = None; wm = None
for a in grid:
    wp = solve_qnm(a, -2, 2, +2, 0, w_guess=wp or w0, tol=1e-14)
    wm = solve_qnm(a, -2, 2, -2, 0, w_guess=wm or w0, tol=1e-14)
    res[a] = (wp, wm)
    print(f"a={a:6.3f}: Re(w+2)={wp.real:+.10f} Re(w-2)={wm.real:+.10f} splitR/a={(wp.real-wm.real)/a:+.8f}")

aa = np.array(grid); ss = np.array([(res[a][0].real-res[a][1].real)/a for a in grid])
# O(a^2) 拟合：ss = c0 + c1 a^2
c2 = np.polyfit(aa**2, ss, 1)
c0 = c2[1]
# O(a^4) 四截断：用最小三个 a 做 Richardson 二次（ss = c0 + c1 a^2 + c2 a^4）
p4 = np.polyfit((aa**2)[:3], ss[:3], 2)
c0b = p4[2]
err = abs(c0 - TARGET); errb = abs(c0b - TARGET)
d = -math.log10(err) if err > 0 else 20
db = -math.log10(errb) if errb > 0 else 20
print(f"\na^2 线性外推: c0 = {c0:+.8f}  err={err:.2e}  {d:.1f} 位 ({'PASS' if d>=4 else 'FAIL'})")
print(f"a^4 四截断外推: c0 = {c0b:+.8f}  err={errb:.2e}  {db:.1f} 位 ({'PASS' if db>=4 else 'FAIL'})")

# per-m 斜率：取 a->0 极限 (Re w(a)-Re w(0))/a 的 a^2 外推
splus = [ (res[a][0].real-0.37367168441804166)/a for a in grid ]
sminus = [ (res[a][1].real-0.37367168441804166)/a for a in grid ]
sp = np.polyfit(aa**2, splus, 1)[1]
sm = np.polyfit(aa**2, sminus, 1)[1]
print(f"prograde dRe/da (a->0) = {sp:+.8f} (目标 +0.125766) err={abs(sp-0.125766):.2e}")
print(f"retrograde dRe/da (a->0)= {sm:+.8f} (目标 -0.125766) err={abs(sm+0.125766):.2e}")
