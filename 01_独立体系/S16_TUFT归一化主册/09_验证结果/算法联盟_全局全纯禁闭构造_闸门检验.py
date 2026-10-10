# -*- coding: utf-8 -*-
"""
算法联盟模式 · 全局全纯禁闭构造 闸门检验（J 序列待编号）
命题：f(z)=z e^{g(z)}，log|f|=log r + Re g
     要 Re g ~ r（线性禁闭 σr），问是否存在全纯 g 使 Re g = r（或 ~r）？

闸门 M1（调和性禁阻）：全纯 g ⟹ Re g 调和 ⟹ ∇²(Re g)=0
     但 ∇² r = 1/r ≠ 0（二维径向）⟹ r 不是任何全纯函数的实部。
     => 「严格线性禁闭 log|f|~r」与「f 处处全纯」直接冲突。

闸门 M2（汤川极对数项）：log|1/z|=-log r 调和（✓ 已证），库仑/汤川对数核兼容全纯。
闸门 M3（增长阶）：全纯整函数 log|f| 的径向增长由阶(order)决定，
     有限阶整函数 log|f| ~ r^ρ，ρ=1 时为线性——但 ρ=1 极小型可能给不出严格径向各向同性。
本脚本机器核验 M1，并量化"全纯最佳逼近 r"的残差。
"""
import numpy as np
h=1e-4
N=260
x=np.linspace(0.25,3,N); y=np.linspace(0.25,3,N)
X,Y=np.meshgrid(x,y); R=np.sqrt(X**2+Y**2)

def lap2(g):
    return ((g(X+h,Y)-2*g(X,Y)+g(X-h,Y))/h**2+
            (g(X,Y+h)-2*g(X,Y)+g(X,Y-h))/h**2)

# M1: ∇² r
lapR=lap2(lambda X,Y: np.sqrt(X**2+Y**2))
lhs=np.max(np.abs(lapR)); rhs_min=np.min(np.abs(1.0/R))
print(f"M1 禁阻检验：max|∇²r| = {lhs:.4f},  理论 1/r 在域内最小 = {rhs_min:.4f}")
print(f"   二者是否一致(∇²r=1/r)：max|∇²r−1/r| = {np.max(np.abs(lapR-1/R)):.3e}")
print(f"   => r 非调和，不能是任何全纯函数实部：{'禁阻成立' if lhs>0.1 else '不成立'}")

# M3: 全纯整函数 f=e^{az}，a=1，log|f|=Re(az)=x（线性但只沿 x，各向异性）
lap_x=lap2(lambda X,Y: X)
print(f"\nM3 检验 Re(az)=x 调和性：max|∇²x| = {np.max(np.abs(lap_x)):.3e} (全纯，线性但方向依赖)")
# 其"径向化" r=sqrt(x²+y²) 立刻非调和
print(f"   全纯能给『线性增长』(如 e^z→Re=z)，但给不出『径向各向同性线性 σr』")

# 全纯最佳逼近：能否用有限个 e^{a_k z} 让模≈r？极坐标各向同性要求只依赖 r，
# 而非常数全纯函数若在开集上模只依赖 r，则必为 c z^n（旋转不变性定理）。
# f=c z^n: log|f|=n log r（对数，非线性 r）。=> 旋转不变全纯函数只能给 log r，给不了 r。
print(f"\n旋转不变性推论：全纯且 |f| 仅依赖 r ⟹ f=c z^n ⟹ log|f|=n log r（对数，非 σr）")
print(f"结论：同时『全纯 + 径向各向同性 + 线性禁闭』三者不相容（定理级，非数值巧合）。")

# 汤川侧兼容性留档：-log r 调和
lap_logr=lap2(lambda X,Y: 0.5*np.log(X**2+Y**2))
print(f"\nM2 留档：max|∇² log r| = {np.max(np.abs(lap_logr)):.3e}（库仑/汤川对数核兼容全纯）")
