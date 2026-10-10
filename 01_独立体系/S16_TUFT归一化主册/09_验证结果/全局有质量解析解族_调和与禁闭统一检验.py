# -*- coding: utf-8 -*-
"""
全局有质量解析解族：在「位形复场全纯」约束下统一 短程汤川 + 线性禁闭

关键复分析事实：
  f(z) 全纯（除孤立极点） ⟹ log|f(z)| 在无奇点处调和：∇² log|f| = 0
  取势 V(z) = -g log|f(z)|：
    - f 在 z0 有极点 f~1/(z-z0)  ⇒ log|f| ~ -log r ⇒ V ~ +g log r   (二维库仑/汤川核)
    - f 在无穷远线性 f~z         ⇒ log|f| ~ log r   ⇒ 大 r 行为由亚调和项给
  三维对应：用全纯结构组织 Re/Im 保证 ∇κ⊥∇τ；径向包络交给径向 ODE
    (∇²−μ²)u=0 球对称 ⇒ u=(q/r)e^{−μr}（汤川，短程）
    禁闭由全纯函数模的亚调和线性项 σr 承载（路线B已证 CR 不约束模）

本脚本数值核验：
  (1) 全纯 f=1/(z-a) 与 f=z 的 log|f| 调和性（∇²≈0，避开奇点）
  (2) 复合解族  Φ(r) = q e^{-μr}/r + σ r   同时含短程衰减与长程线性
  (3) Re/Im 取自全纯 f=z（CR），径向乘包络不改 CR（可分离径向因子）
"""
import numpy as np

h=1e-4
def lap2(g,X,Y):
    return ((g(X+h,Y)-2*g(X,Y)+g(X-h,Y))/h**2 +
            (g(X,Y+h)-2*g(X,Y)+g(X,Y-h))/h**2)

N=240
x=np.linspace(-3,3,N); y=np.linspace(-3,3,N)
X,Y=np.meshgrid(x,y)
R=np.sqrt(X**2+Y**2)
# 避开 f=1/z 的原点与 f=z 的零点（同为原点）
mask=(R>0.6)

# (1) log|1/z| = -log r 调和；log|z|=log r 调和
g_log_inv=lambda x,y:-0.5*np.log(x**2+y**2)
g_log_z  =lambda x,y: 0.5*np.log(x**2+y**2)
l1=np.max(np.abs(lap2(g_log_inv,X,Y)[mask]))
l2=np.max(np.abs(lap2(g_log_z,X,Y)[mask]))
print(f"(1) 调和性  ∇²log|1/z| max|.|={l1:.3e} ; ∇²log|z| max|.|={l2:.3e}  (避开奇点≈0)")

# (2) 三维径向：汤川短程 + 禁闭线性
q,mu,sigma=1.0,2.0,0.3
rr=np.linspace(0.05,4,400)
yuk=q*np.exp(-mu*rr)/rr
conf=sigma*rr
Phi=yuk+conf
# 短程主导判定：近原点 yuk>>conf；远场 conf 主导且 yuk→0
near=np.argmin(np.abs(rr-0.2)); far=np.argmin(np.abs(rr-3.0))
print(f"(2) r=0.2: 汤川={yuk[near]:.3f} 禁闭={conf[near]:.3f}  (短程汤川主导)")
print(f"    r=3.0: 汤川={yuk[far]:.3e} 禁闭={conf[far]:.3f}  (禁闭主导, 汤川衰减)")
cross=rr[np.argmin(np.abs(yuk-conf))]
print(f"    两分量交叉点 r*≈{cross:.3f}")

# (3) CR：κ=Re(f)·R(r), τ=Im(f)·R(r)，f=z，R 为纯径向包络
# ∂xκ−∂yτ 等在可分离 R(r)·(x,y) 结构下核验
def Renv(xx,yy): return q*np.exp(-mu*np.sqrt(xx**2+yy**2))/np.sqrt(xx**2+yy**2)+sigma*np.sqrt(xx**2+yy**2)
def kap(xx,yy): return xx*Renv(xx,yy)/ (np.sqrt(xx**2+yy**2))  # 方向余弦 x/r × 径向包络
def tau(xx,yy): return yy*Renv(xx,yy)/ (np.sqrt(xx**2+yy**2))  # 方向余弦 y/r × 径向包络
def grad(ff,xx,yy):
    return ((ff(xx+h,yy)-ff(xx-h,yy))/(2*h),(ff(xx,yy+h)-ff(xx,yy-h))/(2*h))
kx,ky=grad(kap,X,Y); tx,ty=grad(tau,X,Y)
CR1=np.max(np.abs(kx-ty)[mask]); CR2=np.max(np.abs(ky+tx)[mask])
print(f"(3) 径向包络×单位方向场  CR残差 max=({CR1:.3e},{CR2:.3e})")
print("    说明：纯径向包络乘 (x/r,y/r) 给出的 κ,τ 一般不满足直角CR；")
print("    垂直原理须由复全纯相位(角度)与径向振幅分离构造——见文档结论。")
