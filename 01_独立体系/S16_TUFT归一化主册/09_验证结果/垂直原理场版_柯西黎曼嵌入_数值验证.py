# -*- coding: utf-8 -*-
"""
四力统一 BOUNDARY 攻坚数值验证：
命题  ∇κ · ∇τ = 0  ⟺  位形复场 W = ρ + ib 解析（满足柯西-黎曼方程）

场定义：
    κ = ρ/D,  τ = b/D,  D = ρ² + b²
    ∇κ·∇τ = (1/D⁴)[ 2ρb(ρ²−b²)(|∇b|²−|∇ρ|²) + (−ρ⁴+6ρ²b²−b⁴)∇ρ·∇b ]

预期：
    全纯 W（CR成立：∇ρ·∇b=0 且 |∇ρ|=|∇b|）  →  ∇κ·∇τ ≈ 0
    非全纯 W                                  →  ∇κ·∇τ ≠ 0
"""
import numpy as np

def grad(f, x, y, h=1e-6):
    fx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    fy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return fx, fy

def kappa_tau_dot(rho, b, X, Y, h=1e-6):
    def kap(x, y):
        r = rho(x, y); bt = b(x, y); D = r * r + bt * bt
        return r / D
    def tau(x, y):
        r = rho(x, y); bt = b(x, y); D = r * r + bt * bt
        return bt / D
    krx, kry = grad(kap, X, Y, h)
    trx, try_ = grad(tau, X, Y, h)
    return krx * trx + kry * try_

N = 300
x = np.linspace(-2, 2, N); y = np.linspace(-2, 2, N)
X, Y = np.meshgrid(x, y)
mask = (X**2 + Y**2) > 0.5   # 避开原点奇点

def report(name, rho, b):
    d = kappa_tau_dot(rho, b, X, Y)
    d = d[mask]
    print(f"{name:38s}  max|dot|={np.max(np.abs(d)):.3e}   mean|dot|={np.mean(np.abs(d)):.3e}")

print("全纯（CR 成立，预期≈0）：")
report("A  W=z        (rho=x,  b=y)",      lambda x, y: x,          lambda x, y: y)
report("B  W=z^2      (rho=x^2-y^2,b=2xy)", lambda x, y: x**2 - y**2, lambda x, y: 2 * x * y)
report("D  W=exp(z)   (rho=e^x cos y, b=e^x sin y)",
       lambda x, y: np.exp(x) * np.cos(y), lambda x, y: np.exp(x) * np.sin(y))
print()
print("非全纯（CR 不成立，预期≠0）：")
report("C  rho=x, b=y^2",                   lambda x, y: x,          lambda x, y: y**2)
report("E  rho=x^2, b=y^2",                 lambda x, y: x**2,       lambda x, y: y**2)
report("F  rho=x+y, b=x-y (等模但梯度不⊥? 检查)", lambda x, y: x + y, lambda x, y: x - y)

# 附加：直接验证 CR 约束项 与 点积 的对应
print()
print("CR 约束诊断（A 情形应满足 ∇ρ·∇b=0 且 |∇ρ|=|∇b|）：")
def cr_diag(rho, b, X, Y, h=1e-6):
    rx, ry = grad(rho, X, Y, h); bx, by = grad(b, X, Y, h)
    return rx * bx + ry * by, (rx**2 + ry**2) - (bx**2 + by**2)
g0, m0 = cr_diag(lambda x, y: x, lambda x, y: y, X, Y)
print(f"  A:  ∇ρ·∇b max|.|={np.max(np.abs(g0[mask])):.3e},  |∇ρ|²−|∇b|² max|.|={np.max(np.abs(m0[mask])):.3e}")
g1, m1 = cr_diag(lambda x, y: x, lambda x, y: y**2, X, Y)
print(f"  C:  ∇ρ·∇b max|.|={np.max(np.abs(g1[mask])):.3e},  |∇ρ|²−|∇b|² max|.|={np.max(np.abs(m1[mask])):.3e}")
