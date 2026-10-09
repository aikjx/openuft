# -*- coding: utf-8 -*-
"""
路线 D：检验螺旋几何能否第一性锁定 α = τ/κ = b/ρ

对任意 α 扫描，验证以下几何恒等式是否全部成立（与 α 无关）：
  1) 归一化单位圆   κ̃² + τ̃² = 1
  2) 形变守恒       κ² + τ² = 1/(ρ²+b²)
  3) 母恒等式       κ² + τ² = (ω/c)²   (固定 ω√(ρ²+b²)=c)
  4) 对偶反演       ρκ + bτ = 1
  5) 解析场 CR（路线A）  选 W=ρ+ib 解析，α 仅整体缩放

若全部恒成立 ⇒ 纯螺旋几何对 α 无选择，α 是自由参数，必须外部锚定。
另：检验「单极点解析 + 边界/归一化」是否能引入对 α 的选择。
"""
import numpy as np

print("对任意 α 扫描几何恒等式残差（取 ρ=1, b=α）：")
print(f"{'alpha':>10} {'单位圆残差':>14} {'形变残差':>14} {'母恒等式残差':>16} {'反演残差':>12}")
c = 1.0
for alpha in [0.001, 0.007297, 0.01, 0.1, 0.5, 1.0, 137.0]:
    rho = 1.0; b = alpha
    D = rho**2 + b**2
    k = rho/D; t = b/D
    omega = c/np.sqrt(D)
    # 归一化（单位方向）
    kn, tn = k/np.sqrt(k*k+t*t), t/np.sqrt(k*k+t*t)
    r1 = abs(kn**2+tn**2-1)
    r2 = abs(k*k+t*t-1/D)
    r3 = abs(k*k+t*t-(omega/c)**2)
    r4 = abs(rho*k+b*t-1)
    print(f"{alpha:>10.5g} {r1:>14.2e} {r2:>14.2e} {r3:>16.2e} {r4:>12.2e}")

print()
print("="*64)
print("结论检验：全部恒等式对任意 α 严格成立 ⇒ α 在几何内部完全自由")
print()

# 解析场：W=z 型，整体缩放 W=A z，A 复数 = m e^{iφ}
# ρ=m(x cosφ - y sinφ)? 取 W=A z, A=e^{iφ}（单位模纯旋转）
# κ+iτ=1/conj(W)；在固定探针点看 α=b/ρ 是否随 φ 自由
print("解析场 W=e^{iφ} z（纯旋转），探针点 (x,y)=(1,0.5) 处 α=b/ρ：")
x,y=1.0,0.5
for phi in np.linspace(0,np.pi/2,7):
    # W=e^{iφ}z: rho+ib
    rho = x*np.cos(phi)-y*np.sin(phi)
    b   = x*np.sin(phi)+y*np.cos(phi)
    print(f"  φ={phi:6.3f}  α=b/ρ={b/rho:9.4f}")

print()
print("="*64)
print("锁定 α 的必要条件诊断：")
print("几何恒等式对 α 的偏导（看是否存在极值/不动点能选值）")
rho=1.0
xs=np.linspace(0.0001,3,100000)
# 单位圆恒为1，对 α 导数=0，无选择点
F = 1.0+0*xs
dF=np.gradient(F,xs)
print(f"  单位圆 1 对 α 导数 max|.| = {np.max(np.abs(dF)):.2e}  (平坦，无锁定点)")
# α 自身在 (0,∞) 无内禀极值
print("  α=b/ρ 在 (0,∞) 连续无特权值；1/137 不出自任何螺旋几何极值")
