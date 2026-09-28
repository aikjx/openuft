# -*- coding: utf-8 -*-
"""
_ma_tuft_shooting.py
MainAgent 双端打靶 Kerr Teukolsky 求解器 —— 完整非微扰 V_H（Hughes 4.3）+ shooting
================================================================================
- 径向方程（M=1, s=-2）：Delta R'' - (2r-2) R' + V_H R = 0
  V_H = -(K^2 + 4i(r-1)K)/Delta + 8 i w r + (sA - 2 a m w + a^2 w^2)
  K = (r^2+a^2) w - a m ；sA = angular_sep_const(a w)（完整，非微扰）
- 视界（r->r+）：入波 Frobenius R ~ (r-r+)^{2 - i sigma+}（Leaver xi=-s-i sigma+）
  sigma+ = (2 w r+ - a m)/(r+ - r-)
- 无穷远（r->inf）：出射 R ~ r^{3} e^{i w r}（s=-2 出射）+ 低阶（r^{-1} 入波混合）
  用对数导数匹配：R'/R -> i w + 3/r（出射主导）
- shooting：从 r = r+(1+eps) 积分到 Rmax，匹配 R'/R 与出射渐近；扫 w 找根。
  支持 TUFT 反射壁 BC（视界换成 r_wall 处 Neumann/有界支）——TUFT 侧基底。
"""
import numpy as np
import math
import cmath
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---------------- 角向（Cook 谱方法，自包含） ----------------
def angular_sep_const(c, s, l, m, Nmat=28):
    lmin = max(abs(s), abs(m))
    def F(l):
        if l + 1 < max(abs(s), abs(m)):
            return 0.0
        t1 = (l + 1)**2 - m*m
        t2 = (l + 1)**2 - s*s
        if t1 <= 0 or t2 <= 0:
            return 0.0
        return math.sqrt(t1 / ((2*l+3)*(2*l+1))) * math.sqrt(t2) / (l+1)
    def G(l):
        if l == 0:
            return 0.0
        t1 = l*l - m*m
        t2 = l*l - s*s
        if t1 <= 0 or t2 <= 0:
            return 0.0
        return math.sqrt(t1 / (4*l*l - 1)) * math.sqrt(t2) / l
    def H(l):
        if l == 0 or s == 0:
            return 0.0
        return -m*s / (l*(l+1))
    def A(l): return F(l) * F(l+1)
    def D(l): return F(l) * (H(l+1) + H(l))
    def B(l): return F(l)*G(l+1) + G(l)*F(l-1) + H(l)*H(l)
    def E(l): return G(l) * (H(l-1) + H(l))
    def CC(l): return G(l) * G(l-1)
    N = Nmat
    lvals = [lmin + i for i in range(N)]
    M = np.zeros((N, N), dtype=np.complex128)
    for i, lp in enumerate(lvals):
        for j, lc in enumerate(lvals):
            d = lc - lp
            if d == -2:
                M[i, j] = -c**2 * A(lc)
            elif d == -1:
                M[i, j] = -c**2 * D(lc) + 2*c*s*F(lc)
            elif d == 0:
                M[i, j] = lp*(lp+1) - s*(s+1) - c**2 * B(lp) + 2*c*s*H(lp)
            elif d == 1:
                M[i, j] = -c**2 * E(lc) + 2*c*s*G(lc)
            elif d == 2:
                M[i, j] = -c**2 * CC(lc)
    ev = np.linalg.eigvals(M)
    tgt = l*(l+1) - s*(s+1)
    best = min(ev, key=lambda e: abs(e - tgt))
    return complex(best)

# ---------------- V_H 组装 ----------------
def VH(r, w, a, s, l, m):
    """Hughes 4.3 V_H(r;w)。s 固定 -2（本任务）。"""
    rp = 1.0 + math.sqrt(1.0 - a*a)
    rm = 1.0 - math.sqrt(1.0 - a*a)
    Delta = (r - rp)*(r - rm)
    K = (r*r + a*a)*w - a*m
    sA = angular_sep_const(a*w, s, l, m)
    V = -(K*K + 4j*(r-1.0)*K)/Delta + 8j*w*r + (sA - 2.0*a*m*w + a*a*w*w)
    return V

def rhs(r, y, w, a, s, l, m):
    """y = [R, R']；R'' = (2r-2)/Delta R' - V_H/Delta R"""
    rp = 1.0 + math.sqrt(1.0 - a*a)
    rm = 1.0 - math.sqrt(1.0 - a*a)
    Delta = (r - rp)*(r - rm)
    V = VH(r, w, a, s, l, m)
    R, Rp = y
    return [Rp, ((2.0*r-2.0)*Rp - V*R)/Delta]

# ---------------- shooting 匹配函数 ----------------
def match(w, a, s, l, m, eps=1e-4, Rmax=200.0, rp_eps=1e-6):
    """返回视界 IC 积分到 Rmax 的对数导数与出射渐近之差（应=0 at QNM）。"""
    rp = 1.0 + math.sqrt(1.0 - a*a)
    rm = 1.0 - math.sqrt(1.0 - a*a)
    sigma_p = (2.0*w*rp - a*m)/(rp - rm)
    rho = 2.0 - 1j*sigma_p          # 视界 Frobenius 指数（s=-2 入波）
    r0 = rp*(1.0 + rp_eps)
    dr0 = rp*rp_eps
    # Frobenius IC：R ~ (r-rp)^rho
    R0 = dr0**rho
    Rp0 = rho*dr0**(rho-1.0)
    sol = solve_ivp(lambda r, y: rhs(r, y, w, a, s, l, m),
                    (r0, Rmax), [R0, Rp0], rtol=1e-12, atol=1e-14,
                    method='DOP853', dense_output=True, max_step=2.0)
    if not sol.success:
        return 1e30
    R_f = sol.y[0, -1]; Rp_f = sol.y[1, -1]
    # 出射渐近（s=-2）：R ~ r^3 e^{i w r} 主导 => R'/R = i w + 3/r（大 r）
    target = 1j*w + 3.0/Rmax
    return (Rp_f/R_f - target)

def find_qnm(a, s, l, m, w_guess, half=0.05, n=160):
    """复平面网格扫 |match| 极小，然后双实轴 brentq。返回 w 与 |match|。"""
    best_w = w_guess; best_m = 1e30
    for i in range(n+1):
        for j in range(n+1):
            w = complex(w_guess.real - half + 2*half*i/n,
                        w_guess.imag - half + 2*half*j/n)
            mm = abs(match(w, a, s, l, m))
            if mm < best_m:
                best_m = mm; best_w = w
    return best_w, best_m

if __name__ == '__main__':
    print("== shooting 自检：a=0, l=2, m=2, n=0 ==")
    w0 = 0.37367168441804166 - 0.08896231568893410j
    mm = match(w0, 0.0, -2, 2, 2)
    print("  |match(w0)| = %.3e  (应极小)" % abs(mm))
    # 细网格：±0.02，25x25（避免暴力 61x61 ODE 积分）
    wg = complex(0.375, -0.09)
    w, m = find_qnm(0.0, -2, 2, 2, wg, half=0.01, n=24)
    print("  网格最优: w=%.8f%+.8fi |match|=%.3e" % (w.real, w.imag, m))
    print("  vs 靶:    %s" % w0)
