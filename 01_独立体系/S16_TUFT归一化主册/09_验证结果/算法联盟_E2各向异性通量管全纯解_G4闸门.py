# -*- coding: utf-8 -*-
"""
算法联盟 E2：各向异性通量管型全纯解 + G4 闸门审查

候选：f(z) = z * exp(a z),  a>0 取实数（通量管沿 x 轴）
  log|f| = log r + a x
  - 近 z=0：f~z，log|f|~log r（库仑/汤川核，旋转对称恢复）
  - 沿轴 x>0：log|f| ~ a x（线性增长，禁闭方向）
  - 横向 y：|f|=|y|e^{a·0}=|y|，轴线 x=0 处无指数抬升
  全部由全纯函数构成 ⟹ κ=Re f, τ=Im f 严格 CR ⟹ ∇κ⊥∇τ 保持

检验：
 (1) CR 残差（直接对 κ=Re f, τ=Im f 数值差分）
 (2) 沿轴 vs 横向 的 log|f| 增长（线性/受限）
 (3) 近原点旋转对称恢复（f~z）
 (4) G4：方向来自哪里——显式常数 a 沿 x（外选） vs 由两色荷连线 r12 自发定义
"""
import numpy as np
a=1.0
h=1e-5
N=260
g=np.linspace(-2.5,2.5,N)
X,Y=np.meshgrid(g,g)
Z=X+1j*Y
F=Z*np.exp(a*Z)
KAP=F.real; TAU=F.imag
LOGM=np.log(np.abs(F))

def arr_grad(A):
    gy,gx=np.gradient(A,g,g)  # np.gradient 先轴0=y
    return gx,gy
kx,ky=arr_grad(KAP); tx,ty=arr_grad(TAU)
CR1=np.max(np.abs(kx-ty)); CR2=np.max(np.abs(ky+tx))
print(f"(1) CR 残差 max = ({CR1:.3e},{CR2:.3e})  → 垂直原理保持")
# 梯度正交直接核验（内部点）
dot=kx*tx+ky*ty
norm=np.sqrt((kx**2+ky**2)*(tx**2+ty**2))+1e-30
ang=np.max(np.abs(dot/norm)[50:-50,50:-50])
print(f"    |∇κ·∇τ|/(|∇κ||∇τ|) max = {ang:.3e}  → 正交")

# (2) 沿轴 y=0, x>0 线性；横向 x=0
i0=np.argmin(np.abs(g))
xp=g[g>0.2]
logm_axis=np.log(np.abs(xp*np.exp(a*xp)))
slope=np.polyfit(xp,logm_axis,1)[0]
print(f"(2) 沿+x轴 log|f| 线性斜率 = {slope:.4f}（理论 a={a}）")
yp=g[np.abs(g)>0.2]
logm_trans=np.log(np.abs(yp*np.exp(0)))
print(f"    横向(x=0) log|f|=log|y|，无指数抬升；端点值 {logm_trans[0]:.3f}~{logm_trans[-1]:.3f}")

# (3) 近原点 f~z：比较 |f|/|z| → 1
near=np.abs(Z)<0.05
ratio=np.abs(F[near]/Z[near])
print(f"(3) 近原点 |f/z| → {np.mean(ratio):.4f}（库仑核旋转对称恢复）")

# (4) G4：常数 a 沿 x 是外选方向（显式破缺）；自发版本令 a 方向=两荷连线
print(f"(4) G4 审查：实数 a 沿固定 x = 外选优越方向（显式，撞G4）；")
print(f"    自发化：令 a-矢量 ∥ r12（夸克-反夸克连线），方向由源构型决定、无外部n0")
# 通量管平移到两荷之间：取 z=z' ，源在 z'=0 与 z'=L；方向 r12 旋转不变地定义
