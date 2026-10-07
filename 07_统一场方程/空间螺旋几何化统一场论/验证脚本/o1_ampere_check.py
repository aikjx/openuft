# -*- coding: utf-8 -*-
"""O-P1 攻破（续）：验证 A=T 时静态安培自洽 ∇×(∇×T)=μ₀J，并检验磁场形态（环向螺线管=轴向电流）
数值中心差分（独立于解析），对比解析闭式。
"""
import numpy as np
w, vz = 1.0, 1.0
def T(x,y,z):
    c=np.sqrt(w**2*(x*x+y*y)+vz**2)
    return np.array([-w*y/c, w*x/c, vz/c])
def curl(Tf,p,h=1e-5):
    x,y,z=p
    def comp(i,j,k):
        e=[[1,0,0],[0,1,0],[0,0,1]]
        ej=np.array(e[j]); ek=np.array(e[k])
        Tjp=Tf(x+h*ej[0],y+h*ej[1],z+h*ej[2]); Tjm=Tf(x-h*ej[0],y-h*ej[1],z-h*ej[2])
        Tkp=Tf(x+h*ek[0],y+h*ek[1],z+h*ek[2]); Tkm=Tf(x-h*ek[0],y-h*ek[1],z-h*ek[2])
        return (Tjp[k]-Tjm[k])/(2*h)-(Tkp[j]-Tkm[j])/(2*h)
    return np.array([comp(0,1,2),comp(1,2,0),comp(2,0,1)])

def J_num(p):
    # ∇×(∇×T) = μ₀J，数值
    B=lambda x,y,z: curl(T,(x,y,z),1e-4)
    return curl(B,p,1e-3)

def J_ana(x,y,z):
    r=np.sqrt(x*x+y*y); c=np.sqrt(w**2*r*r+vz**2)
    # ∇×B, B=(Bφ,0,Bz): (∇×B)φ = -∂_ρ B_z ; (∇×B)z = (1/ρ)∂_ρ(ρBφ)
    dphirho = w**3*(4*r/c**3 - 3*w**2*r**3/c**5)          # (∇×B)_φ
    dzz     = vz*w**2*(2*c**2-3*w**2*r**2)/c**5           # (∇×B)_z
    ph=np.array([-y/r,x/r,0]); zz=np.array([0,0,1])
    return dphirho*ph+dzz*zz

print("验证 ∇×(∇×T) = μ₀J（静态安培）数值 vs 解析：")
print(f"{'点(ρ)':>8} | {'μ₀J_数值':>26} | {'μ₀J_解析':>26} | 残差")
for (x,y,z) in [(0.5,0,0),(1,0,0),(2,0,0),(1,1,0),(1,0,0.5)]:
    jn=J_num((x,y,z)); ja=J_ana(x,y,z)
    r=np.sqrt(x*x+y*y); res=np.linalg.norm(jn-ja)
    print(f" ρ={r:>5.2f} | {np.round(jn,4)} | {np.round(ja,4)} | {res:.2e}")
print("\n磁场形态: B = (vz·ω²ρ/c³)φ̂ + (2ω/c - ω³ρ²/c³)ẑ")
print("  φ̂ 环向分量 ∝ vz·ω²ρ/c³ > 0  ⇒ 螺线管型（轴向电流磁场）；ẑ 轴向分量 ≈2ω/c(ρ→0)")
print("  源 μ₀J = ∇×(∇×T) 非零，由螺旋几何确定 ⇒ A=T 是 C-02 的静态可行实现（满足安培自洽）")
