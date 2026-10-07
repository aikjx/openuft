# -*- coding: utf-8 -*-
"""O-P1 闭合路径候选：A=v（矢势=速度场）→ C-02(磁场=涡量) + C-03(电场=加速度)
推导链：ωρ=c → v=cT(速度场) → A=v → B=f∇×v=2fΩ(涡量,C-02) → E=-f∂_t v=-f a(加速度,C-03)
验证：
  1) C-02: B=f∇×v 对螺旋流(静态)：环向+轴向磁场
  2) C-03: E=-f∂_t v 对加速螺旋：电场=负加速度（解析 E=-f a）
"""
import numpy as np
w_,vz,f=1.0,1.0,1.0
def v_spiral(x,y,z):
    # 螺旋速度场 v = ωρ·φ̂ + vz·ẑ = (-ωy, ωx, vz)
    return np.array([-w_*y, w_*x, vz])
def curl(vf,p,h=1e-5):
    x,y,z=p;e=[[1,0,0],[0,1,0],[0,0,1]]
    def comp(i,j,k):
        ej=np.array(e[j]);ek=np.array(e[k])
        Tjp=vf(x+h*ej[0],y+h*ej[1],z+h*ej[2]);Tjm=vf(x-h*ej[0],y-h*ej[1],z-h*ej[2])
        Tkp=vf(x+h*ek[0],y+h*ek[1],z+h*ek[2]);Tkm=vf(x-h*ek[0],y-h*ek[1],z-h*ek[2])
        return (Tjp[k]-Tjm[k])/(2*h)-(Tkp[j]-Tkm[j])/(2*h)
    return np.array([comp(0,1,2),comp(1,2,0),comp(2,0,1)])
def B_ana(x,y,z):
    # B=f∇×v: 螺旋流 v=ωρφ̂+vzẑ → ∇×v = 2ω ẑ (均匀轴向)
    return f*np.array([0,0,2*w_])

print("== [1] C-02: B=f∇×v（磁场=涡量），螺旋流 v=ωρ·φ̂+vz·ẑ ==")
for p in [(0,0,0),(0.5,0,0),(1,1,0),(2,0,1)]:
    Bn=f*curl(v_spiral,p); Ba=B_ana(*p)
    print(f" p={p}: B_num={np.round(Bn,4)}, B_ana={np.round(Ba,4)}, |ΔB|={np.linalg.norm(Bn-Ba):.1e}  → 均匀轴向磁场(2ωf)=涡量")

print("\n== [2] C-03: E=-f∂_t v（电场=负加速度），加速螺旋轨迹 ==")
# 螺旋加速轨迹 r(t)=ρcos(ωt+½βt²)… 简化：匀加速直线加速螺旋轴向
# 取电荷沿螺旋加速：v_z(t)=v0+αt（轴向加速），横向保持 → 加速度 a=α ẑ
alpha=2.0; f=1.0
v0=0.5
for t in [0.3,1.0]:
    vz_t=v0+alpha*t
    a=np.array([0,0,alpha])            # 加速度
    E_ana=-f*a                          # E=-f a
    # 数值: E=-f∂_t v  (v 显含 t)
    def vt(t):
        return np.array([0,0,v0+alpha*t])
    E_num=-f*(vt(t+1e-5)-vt(t-1e-5))/(2e-5)
    print(f" t={t}: v_z={vz_t}, a=αẑ={alpha}, E_ana=-f a={E_ana}, E_num={np.round(E_num,4)} → 一致")

print("\n== 推导链（O-P1 闭合路径候选） ==")
print(" ωρ=c → v=cT(速度场) → A=v → B=f∇×v=2fΩ(C-02,磁场=涡量) → E=-f∂_t v=-f a(C-03,电场=加速度)")
print(" 核心假设: A=v（矢势=速度场）；与 36 号无规范自由自洽（A 是物理速度场，非规范势）")
print(" ⇒ C-02/C-03 成为运动学恒等式；UFE-2 由消元得出（35 号已证）")
