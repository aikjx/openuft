# -*- coding: utf-8 -*-
"""
TUFT v9 线一: Leaver(1985) 连分数 O(N) 秒级 QNM 管线
=====================================================
阶段1: Schwarzschild 标量 KG 径向 QNM (l=0/1/2 三模态打通)
阶段2: 引力 Regge-Wheeler s=-2 QNM (l=2, n=0/1)
阶段3: TUFT 混合边界

单位: M=1 (视界 r=2), 输出 omega*M. GM_sun/c^3 = 4.9256 us.
"""
import numpy as np
import time

GMUS = 4.9256
T0 = time.time()

# ============================================================================
# Leaver(1985) 连分数三项递推
# 径向解 Frobenius 幂级数:  u = exp(-i w r*) * sum a_n z^n,  z = 1 - 2/r
# 递推:  alpha_n a_{n+1} + beta_n a_n + gamma_n a_{n-1} = 0,  a_0=1, gamma_0=0
# 从大 N 向下递推 a_{n-1}/a_n, 特征函数 F(w) = 0 用 Muller 复根搜索
# ============================================================================

def leaver_cf_scalar(omega, l, N=200):
    """标量 KG Leaver 连分数特征函数 F(omega). 返回复数 F."""
    # 三项递推系数 (Schwarzschild 标量, M=1)
    # 向后递推:  R_n = a_n/a_{n-1} = -gamma_n / (alpha_n R_{n+1} + beta_n)
    R = 0.0 + 0.0j
    for n in range(N, 0, -1):
        alpha = (n+1)*(n+2*l+2)
        beta = -(n*n + (2*l+1)*n + l*(l+1) + 2*(1 - 4*omega**2))
        gamma = n*(n-1) + 2j*omega*(2*n - 1)
        R = -gamma / (alpha*R + beta)
    # n=0 特征: alpha_0 R_1 + beta_0 = 0
    alpha0 = 2*(l+1)
    beta0 = -(l*(l+1) + 2*(1 - 4*omega**2))
    return alpha0*R + beta0


def muller(f, x0, x1, x2, tol=1e-12, maxit=200):
    """Muller 复根搜索."""
    for _ in range(maxit):
        f0, f1, f2 = f(x0), f(x1), f(x2)
        h0, h1 = x1-x0, x2-x1
        d0 = (f1-f0)/h0
        d1 = (f2-f1)/h1
        a = (d1-d0)/(h1+h0)
        b = a*h1 + d1
        c = f2
        disc = np.sqrt(b*b - 4*a*c)
        den1, den2 = b+disc, b-disc
        den = den1 if abs(den1) >= abs(den2) else den2
        dx = -2*c/den
        x3 = x2 + dx
        if abs(dx) < tol*max(1.0, abs(x3)):
            return x3
        x0, x1, x2 = x1, x2, x3
    return x2


def find_root(f, guess, tol=1e-12):
    g = complex(guess)
    return muller(f, g+0.02, g-0.01+0.01j, g, tol=tol)


# ============================================================================
# 阶段 1: 标量 KG l=0/1/2
# ============================================================================
KNOWN = {
    0: complex(0.110456, -0.104899),
    1: complex(0.292936, -0.097660),
    2: complex(0.483644, -0.096759),
}

def stage1():
    out = []
    out.append("="*72)
    out.append("阶段 1: Schwarzschild 标量 KG QNM  (Leaver 连分数 O(N))")
    out.append("="*72)
    out.append("单位 M=1, 已知基准根 (>=6 位):")
    out.append("  l=0,n=0: 0.110456 - 0.104899 i")
    out.append("  l=1,n=0: 0.292936 - 0.097660 i")
    out.append("  l=2,n=0: 0.483644 - 0.096759 i")
    out.append("")
    out.append("N 收敛表 (Leaver 连分数截断阶数 N):")
    out.append("-"*72)
    for l in [0, 1, 2]:
        tgt = KNOWN[l]
        out.append(f"\n  l = {l}, 已知基准 wM = {tgt.real:.6f} {tgt.imag:+.6f} i")
        out.append(f"    {'N':>6} | {'wM 计算值':>26} | |dw|")
        for N in [100, 200, 400]:
            root = find_root(lambda w, ll=l: leaver_cf_scalar(w, ll, N), tgt)
            dw = abs(root - tgt)
            out.append(f"    {N:6d} | {root.real:12.6f} {root.imag:+.6f} i | {dw:.2e}")
    return out


# ============================================================================
# 阶段 2: 引力 Regge-Wheeler s=-2
# ============================================================================
def stage2():
    out = []
    out.append("\n" + "="*72)
    out.append("阶段 2: 引力 Regge-Wheeler s=-2 QNM")
    out.append("="*72)
    out.append("已知基准: l=2,n=0: 0.373672 - 0.088962 i")
    out.append("          l=2,n=1: 0.346710 - 0.273910 i")
    # RW 势: V = f [l(l+1)/r^2 - 6M/r^3]
    # 递推系数与标量不同, 需从 RW 方程严格推导
    out.append("")
    out.append("  [RW 迁移状态: 需独立推导 RW 递推系数]")
    out.append("  [门禁待开]")
    return out


# ============================================================================
# 阶段 3: TUFT 混合边界
# ============================================================================
def stage3():
    out = []
    out.append("\n" + "="*72)
    out.append("阶段 3: TUFT 混合边界")
    out.append("="*72)
    out.append("  度规 A=e^(-2/r), B=e^(2/r)(1+c_m/r^2+d/r^3)")
    out.append("  内壁 Neumann, 远场出射, c_m=-0.29, d=-0.05")
    out.append("  [引力门禁未过, 禁止报 TUFT 根]")
    return out


# ============================================================================
if __name__ == "__main__":
    lines = []
    lines.append("TUFT v9 线一: Leaver(1985) 连分数 QNM 管线")
    lines.append(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines += stage1()
    lines += stage2()
    lines += stage3()
    lines.append("")
    lines.append("="*72)
    lines.append(f"总耗时: {time.time()-T0:.2f} s")
    lines.append("GM_sun/c^3 = 4.9256 us")
    txt = "\n".join(lines)
    print(txt)
    with open("tuft_v9_line1_leaver_out.txt", "w", encoding="utf-8") as f:
        f.write(txt)
