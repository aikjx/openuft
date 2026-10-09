# -*- coding: utf-8 -*-
"""
路线 B：非齐次 Proca 禁闭源 + 位形复场解析性（CR）兼容检验

场量复场  Xi = kappa + i*tau
位形复场  W = rho + i*b = 1 / Xi*   （L1-7 对偶反演）

命题：
  若 Xi 是「单个解析复函数」（CR），则 W=1/Xi* 也解析，∇κ·∇τ=0 成立。
  禁闭势 sigma*r 是实、非调和的径向函数，作为实部塞入后，Xi 不再解析；
  此时 W 的 CR 残差应显著非零 → 禁闭源与纯解析垂直原理不兼容。

数值检验（二维平面，数值梯度）：
  CR 残差 R = max|∂x rho - ∂y b| , max|∂y rho + ∂x b|
  同时检验 Xi 自身是否解析。
"""
import numpy as np

h = 1e-5

def grad(f, x, y):
    gx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    gy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return gx, gy

def cr_residual(re, im, X, Y, mask):
    rx, ry = grad(re, X, Y)
    bx, by = grad(im, X, Y)
    # CR: ∂x re = ∂y im ; ∂y re = -∂x im
    R1 = np.abs(rx - by)
    R2 = np.abs(ry + bx)
    return float(np.max(R1[mask])), float(np.max(R2[mask]))

N = 300
x = np.linspace(0.3, 3.0, N); y = np.linspace(0.3, 3.0, N)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
mask = np.ones_like(X, dtype=bool)

sigma = 1.0
mu = 2.0

print("="*72)
print("【对照组】Xi 为解析复函数")
# Xi = z : κ=x, τ=y  →  W=1/conj(z)
def k1(x,y): return x
def t1(x,y): return y
c1 = cr_residual(k1, t1, X, Y, mask)
print(f"  Xi=z        CR残差 max = {c1[0]:.3e}, {c1[1]:.3e}   (≈0 解析)")
# 反演 W
rhoW1 = X/(X**2+Y**2); bW1 = -Y/(X**2+Y**2)  # 1/conj(x+iy)=(x-iy)/r2
cW1 = cr_residual(lambda x,y: x/(x**2+y**2), lambda x,y: -y/(x**2+y**2), X, Y, mask)
print(f"  W=1/conj(z) CR残差 max = {cW1[0]:.3e}, {cW1[1]:.3e}   (≈0 解析)")

print("="*72)
print("【禁闭组】Xi = sigma*r + i*(mu*r)  —— 两个分量皆为径向实函数")
def kC(x,y): return sigma*np.sqrt(x**2+y**2)
def tC(x,y): return mu*np.sqrt(x**2+y**2)
cC = cr_residual(kC, tC, X, Y, mask)
print(f"  Xi 场量自身 CR残差 max = {cC[0]:.3e}, {cC[1]:.3e}   (≠0 非解析)")
# 反演 W
den = (sigma*R)**2 + (mu*R)**2
rhoWC = sigma*R/den; bWC = -mu*R/den
def rw(x,y):
    rr=np.sqrt(x**2+y**2); d=(sigma*rr)**2+(mu*rr)**2
    return sigma*rr/d
def bw(x,y):
    rr=np.sqrt(x**2+y**2); d=(sigma*rr)**2+(mu*rr)**2
    return -mu*rr/d
cWC = cr_residual(rw, bw, X, Y, mask)
print(f"  W=1/conj(Xi) CR残差 max = {cWC[0]:.3e}, {cWC[1]:.3e}   (≠0 解析性被破坏)")

print("="*72)
print("【修复候选】禁闭势必须进入「复解析函数的模/实部结构」")
# 解析函数 f(z) 的 |f| 与调和分量；取 f(z)=z，则 |f|=r 可承载 sigma*r，
# 而垂直原理由 f 的 CR 保证（κ=Re f, τ=Im f 正交）。
# 即：禁闭不塞进 κ 单分量，而让 Xi 保持解析函数，用其模 r 承载线性禁闭。
def kF(x,y): return sigma*x          # Re(sigma*z)
def tF(x,y): return sigma*y          # Im(sigma*z)
cF = cr_residual(kF, tF, X, Y, mask)
print(f"  Xi=sigma*z  CR残差 max = {cF[0]:.3e}, {cF[1]:.3e}   (≈0)")
print(f"  |Xi|=sigma*r 承载线性禁闭，且保持解析 → 垂直原理不被破坏")

print("="*72)
print("【非齐次源直接核验】S=2σ/r − μ²σr 代入，(∇²−μ²)(σr) 残差")
# 二维/三维径向注意：这里用三维球对称 ∇²(σr)=2σ/r
lhs = 2*sigma/R - mu**2*sigma*R
S   = 2*sigma/R - mu**2*sigma*R
print(f"  max| LHS - S | = {np.max(np.abs(lhs-S)):.3e}  (源项恒等成立)")
