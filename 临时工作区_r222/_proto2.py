# -*- coding: utf-8 -*-
"""r222 原型二：lambda 反解 + 多行星一致性检验 + 数值收敛性。"""
import math
from _proto import GM_SUN, C0, PLANETS, gr_precession, yukawa_precession

a_m, e_m = PLANETS[0][1], PLANETS[0][2]
tgt = gr_precession(a_m, e_m)

# --- 1) 收敛性：步数加倍 ---
print("== 收敛性 (Mercury, lam=1e14) ==")
prev = None
for n in (200000, 400000, 800000, 1600000):
    d = yukawa_precession(a_m, e_m, 1e14, nstep=n)
    print("  nstep=%-8d domega=%.8e  diff=%s" % (n, d, "%.2e" % (d - prev) if prev else "-"))
    prev = d

print("== 收敛性 (Mercury, lam=inf 应回到 0) ==")
for n in (200000, 800000):
    print("  nstep=%-8d domega=%.4e" % (n, yukawa_precession(a_m, e_m, None, nstep=n)))

# --- 2) 反解 lambda：二分使 domega == GR(Mercury) ---
print("== 反解 lambda_fit (拟合水星 GR 进动 %.6e rad/rev) ==" % tgt)
lo, hi = 5e13, 5e14
for _ in range(60):
    mid = math.sqrt(lo * hi)
    d = yukawa_precession(a_m, e_m, mid, nstep=400000)
    if d > tgt:
        lo = mid
    else:
        hi = mid
lam_fit = math.sqrt(lo * hi)
d_fit = yukawa_precession(a_m, e_m, lam_fit, nstep=800000)
print("  lambda_fit = %.6e m = %.1f AU" % (lam_fit, lam_fit / 1.495978707e11))
print("  domega(lam_fit) = %.6e  (target %.6e, rel %.2e)"
      % (d_fit, tgt, abs(d_fit - tgt) / tgt))

# --- 3) 用同一 lambda_fit 预测其余行星，与 GR(=观测)对比 ---
print("== 同一 lambda_fit 下的多行星一致性 ==")
print("  %-8s %-14s %-14s %-10s" % ("planet", "GR(=obs)", "Yukawa", "ratio"))
for nm, a, e in PLANETS:
    g = gr_precession(a, e)
    y = yukawa_precession(a, e, lam_fit, nstep=800000)
    print("  %-8s %.6e   %.6e   %.3f" % (nm, g, y, y / g))

# --- 4) 有效力修正的符号：r<<lam 展开的常数项 ---
print("== r<<lam 展开常数项符号 ==")
lam = lam_fit
for r in (5.79e10, 1.082e11):
    x = r / lam
    exact = (1.0 + x) * math.exp(-x)
    series = 1.0 - 0.5 * x * x
    print("  r=%.4e  x=%.3e  (1+x)e^-x=%.12f  1-x^2/2=%.12f  diff=%.2e"
          % (r, x, exact, series, exact - series))
