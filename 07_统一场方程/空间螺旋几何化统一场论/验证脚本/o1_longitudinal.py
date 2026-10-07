# -*- coding: utf-8 -*-
"""O-P1 全链路（续）：UFE-2 纵向扇区 —— 数值验证 + 规范结构判定
纵波 A=A0·cos(kz-ωt)·ẑ, ∇·A≠0
解析：∂_t²A=-ω²A; ∇·A=-kA0sin; ∇(∇·A)=-k²A; ∂_t(∇·A)=ωkA0cos; ∇²A=-k²A
UFE-2 = -ω²A + Vz·ωk·A0cos·ẑ + c²(-k²A) - c²(-k²A) = (-ω²+Vzωk)A0cos·ẑ  ⇒ 色散 ω=Vz·k
"""
import numpy as np
c_=1.0; f=1.0; Vz=0.6*c_; A0=1.0; k=2.0; om=Vz*k
def A(x,y,z,t): return A0*np.cos(k*z-om*t)*np.array([0,0,1.0])
def curl(p,t,h=1e-5):
    x,y,z=p;e=[[1,0,0],[0,1,0],[0,0,1]]
    def comp(i,j,k):
        ej=np.array(e[j]);ek=np.array(e[k])
        Tjp=A(x+h*ej[0],y+h*ej[1],z+h*ej[2],t);Tjm=A(x-h*ej[0],y-h*ej[1],z-h*ej[2],t)
        Tkp=A(x+h*ek[0],y+h*ek[1],z+h*ek[2],t);Tkm=A(x-h*ek[0],y-h*ek[1],z-h*ek[2],t)
        return (Tjp[k]-Tjm[k])/(2*h)-(Tkp[j]-Tkm[j])/(2*h)
    return np.array([comp(0,1,2),comp(1,2,0),comp(2,0,1)])
def lap(p,t,h=1e-4):
    x,y,z=p;L=np.zeros(3)
    for i in range(3):
        ei=np.array([[1,0,0],[0,1,0],[0,0,1]][i])
        L+=(A(x+h*ei[0],y+h*ei[1],z+h*ei[2],t)+A(x-h*ei[0],y-h*ei[1],z-h*ei[2],t)-2*A(x,y,z,t))/(h*h)
    return L
def grad_divA(p,t,h=1e-4):
    x,y,z=p;g=np.zeros(3)
    for i in range(3):
        ei=np.array([[1,0,0],[0,1,0],[0,0,1]][i]);hh=1e-5
        def dv(q):
            x2,y2,z2=q;s=0
            for j in range(3):
                ej=np.array([[1,0,0],[0,1,0],[0,0,1]][j]);dh=1e-5
                s+=(A(x2+dh*ej[0],y2+dh*ej[1],z2+dh*ej[2],t)-A(x2-dh*ej[0],y2-dh*ej[1],z2-dh*ej[2],t))[j]/(2*dh)
            return s
        g[i]=(dv((x+h*ei[0],y+h*ei[1],z+h*ei[2]))-dv((x-h*ei[0],y-h*ei[1],z-h*ei[2])))/(2*h)
    return g

print(f"纵波 A=A0·cos(kz-ωt)·ẑ, V=Vz·ẑ, Vz={Vz}c, k={k}, ω=Vz·k={om:.2f}")
print(f"{'p,t':>20} | {'UFE2残差':>9} {'|B|':>6} {'E_z':>7} {'∇·E':>7} {'∇·A':>7}")
for (x,y,z),t in [((0,0,0),0),((0,0,0.5),0.3),((0.4,0.3,1),0.7)]:
    p=(x,y,z)
    d2t=(A(x,y,z,t+1e-5)+A(x,y,z,t-1e-5)-2*A(x,y,z,t))/(1e-10)
    # ∂_t(∇·A) 数值
    dtdiv=((A(x,y,z+1e-5,t+1e-5)[2]-A(x,y,z-1e-5,t+1e-5)[2])/(2e-5) - (A(x,y,z+1e-5,t-1e-5)[2]-A(x,y,z-1e-5,t-1e-5)[2])/(2e-5))/(2e-5)
    Vgrad=Vz*dtdiv*np.array([0,0,1.0])
    ufe=d2t+Vgrad+c_*c_*grad_divA(p,t)-c_*c_*lap(p,t)
    Bn=curl(p,t); En=-f*(A(x,y,z,t+1e-5)-A(x,y,z,t-1e-5))/(2e-5)
    divE=0
    for i in range(3):
        ei=np.array([[1,0,0],[0,1,0],[0,0,1]][i]);h=1e-4
        divE+= (En[0]*0+ (A(x+h*ei[0],y+h*ei[1],z+h*ei[2],t)[2]*0)) # placeholder
    # 直接: E=fA0ω sin·ẑ, ∇·E=∂_zE_z=fA0ω·k·cos(kz-ωt)
    divE_ana=f*A0*om*k*np.cos(k*z-om*t)
    divA_ana=-k*A0*np.sin(k*z-om*t)
    print(f" ({x},{y},{z}),t={t} | {np.linalg.norm(ufe):.1e} {np.linalg.norm(Bn):.0e} {En[2]:.3f} {divE_ana:.3f} {divA_ana:.3f}")

print("\n规范判定(解析): A→A+∇χ ⇒ B'=B(不变), E'=E-f∇χ̇(改变)；无标势 φ ⇒ 无规范自由")
print("⇒ UFE-2 纵向扇区(∇·A≠0)物理；纵波 B=0、E 纵向、∇·E∝cos≠0(电荷密度波)，非真空中性波")
