# -*- coding: utf-8 -*-
"""
_ma_kerr_gateB.py
GR 门 B：Kerr 慢转 m 频裂 splitR/a -> 0.2515323（MainAgent 门常加固，勘误 #42）
在 a 网格解 l=2, m=+2/-2, n=0 QNM，验证：
  1. splitR/a = (Re w_{m=+2} - Re w_{m=-2})/a 在 a->0 收敛到 0.2515323（>=4 位）
  2. per-m 斜率 dRe/da 在 a->0 -> 0.125766（+m 模式）、-0.125766（-m 模式）
门未过 => TUFT 旋转极点一律 UNTRUSTED。
"""
import math
import numpy as np
from _ma_kerr_leaver_full import solve_qnm, angular_sep_const

TARGET = 0.2515323        # 门靶（勘误 #42，独立第三方值，非硬编码进求解器）
SLOPE  = 0.125766         # prograde dRe/da

grid = [0.02, 0.05, 0.10, 0.15, 0.20]
# 初值：a=0 的 Schwarzschild n0（求解器内部同样以此起步，属物理初值非门靶）
w0 = 0.37367168441804166 - 0.08896231568893410j

results = {}
w_plus = None
w_minus = None
for a in grid:
    w_plus  = solve_qnm(a, -2, 2, +2, 0, w_guess=w_plus  or w0, tol=1e-14)
    w_minus = solve_qnm(a, -2, 2, -2, 0, w_guess=w_minus or w0, tol=1e-14)
    results[a] = (w_plus, w_minus)
    split = (w_plus.real - w_minus.real) / a
    print(f"a={a:5.2f}: Re(w+2)={w_plus.real:+.10f} Re(w-2)={w_minus.real:+.10f} "
          f"splitR/a={split:+.8f}  (+m 斜率 dRe/da={(w_plus.real-0.37367168441804166)/a:+.8f})")

# 外推 a->0：对 splitR/a 用二次拟合（误差 O(a^2)）
aa = np.array(grid, dtype=float)
ss = np.array([(results[a][0].real - results[a][1].real)/a for a in grid], dtype=float)
# 加权小 a（O(a^2) 收敛：用 1/a^2 权重？直接线性外推最小二乘）
c = np.polyfit(aa, ss, 1)  # ss ~ c0 + c1*a
split0 = c[1]
err = abs(split0 - TARGET)
digits = -math.log10(err) if err > 0 else 20
print(f"\n外推 a->0: splitR/a = {split0:+.8f} (目标 {TARGET})")
print(f"|err| = {err:.2e}  有效位数 = {digits:.1f}  ({'PASS' if digits >= 4 else 'FAIL'})")

# per-m 斜率核对
splus = np.polyfit(aa, np.array([results[a][0].real for a in grid]), 1)[0]
sminus = np.polyfit(aa, np.array([results[a][1].real for a in grid]), 1)[0]
print(f"prograde dRe/da = {splus:+.8f} (目标 +{SLOPE})  err={abs(splus-SLOPE):.2e}")
print(f"retrograde dRe/da = {sminus:+.8f} (目标 -{SLOPE}) err={abs(sminus+SLOPE):.2e}")
