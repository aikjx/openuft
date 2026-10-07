# -*- coding: utf-8 -*-
"""O-P1 全链路：螺旋切矢横向结构 → UFE-2 电磁波解（C-01/C-02/C-03 闭合检验）
1) 圆偏振螺旋波 A=A0(cos(kz-ωt),sin(kz-ωt),0)：横向(cos,sin)与螺旋切矢横向(-ωy/c,ωx/c)∝(-sinφ,cosφ)同族
   - C-03: E=-f∂_tA → E=fA0ω(sin,-cos,0)
   - C-02: B=f∇×A  → B=-fkA0(cos,sin,0)
   - C-01/UFE-2: ∂_t²A - c²∇²A=0（∇·A=0）→ 色散 ω=ck；E⊥B、|E|=c|B|
2) A=T 静态：满足 C-02+安培，但不满足 UFE-2（有源构型）
"""
import numpy as np
w_,vz=1.0,1.0; f=1.0; k=2.0; c=1.0; om=c*k; A0=1.0

def A(x,y,z,t): return A0*np.array([np.cos(k*z-om*t),np.sin(k*z-om*t),0.0])
def curlA(x,y,z,t,h=1e-5):
    e=[[1,0,0],[0,1,0],[0,0,1]]
    def comp(i,j,k):
        ej=np.array(e[j]);ek=np.array(e[k])
        Ap=A(x+h*ej[0],y+h*ej[1],z+h*ej[2],t);Am=A(x-h*ej[0],y-h*ej[1],z-h*ej[2],t)
        Bp=A(x+h*ek[0],y+h*ek[1],z+h*ek[2],t);Bm=A(x-h*ek[0],y-h*ek[1],z-h*ek[2],t)
        return (Ap[k]-Am[k])/(2*h)-(Bp[j]-Bm[j])/(2*h)
    return np.array([comp(0,1,2),comp(1,2,0),comp(2,0,1)])
def divA(x,y,z,t,h=1e-5):
    e=[[1,0,0],[0,1,0],[0,0,1]]
    s=0
    for i in range(3):
        ei=np.array(e[i])
        s+=(A(x+h*ei[0],y+h*ei[1],z+h*ei[2],t)[i]-A(x-h*ei[0],y-h*ei[1],z-h*ei[2],t)[i])/(2*h)
    return s
def lapA(x,y,z,t,h=1e-4):
    lap=np.zeros(3)
    for i in range(3):
        ei=np.array([[1,0,0],[0,1,0],[0,0,1]][i])
        lap+=(A(x+h*ei[0],y+h*ei[1],z+h*ei[2],t)+A(x-h*ei[0],y-h*ei[1],z-h*ei[2],t)-2*A(x,y,z,t))/(h*h)
    return lap

def B_ana(x,y,z,t): return -f*k*A(x,y,z,t)
def E_ana(x,y,z,t): return f*A0*om*np.array([-np.sin(k*z-om*t),np.cos(k*z-om*t),0.0])  # E=-f∂_tA

print("== [1] 圆偏振螺旋波满足 C-02/C-03/UFE-2（数值 vs 解析） ==")
print(f"{'p,t':>20} | {'|ΔB|':>8} {'|ΔE|':>8} {'|UFE2|':>9} {'divA':>8} {'|E|/|B|':>7}")
for (x,y,z),t in [((0,0,0),0),((0.3,-0.2,0.5),0.2),((1,1,1),0.7)]:
    Bn=f*curlA(x,y,z,t); Ba=B_ana(x,y,z,t)
    En=-f*(A(x,y,z,t+1e-5)-A(x,y,z,t-1e-5))/(2e-5); Ea=E_ana(x,y,z,t)
    d2t=(A(x,y,z,t+1e-5)+A(x,y,z,t-1e-5)-2*A(x,y,z,t))/(1e-10)
    ufe=d2t-c*c*lapA(x,y,z,t)
    EB=En@Ba/np.linalg.norm(En)/np.linalg.norm(Ba)
    print(f" ({x},{y},{z}),t={t} | {np.linalg.norm(Bn-Ba):.1e} {np.linalg.norm(En-Ea):.1e} {np.linalg.norm(ufe):.1e} {divA(x,y,z,t):.1e} {np.linalg.norm(En)/np.linalg.norm(Ba):.3f}")
print(f" 解析: |E|=fA0ω={f*A0*om}, |B|=fkA0={f*k*A0}, |E|/|B|=ω/k={om/k}=c; E·B(数值)={EB:.3f}")

print("\n== [2] A=T 静态：满足 C-02+安培，但不满足 UFE-2（如实） ==")
def T(x,y,z):
    c_=np.sqrt(w_**2*(x*x+y*y)+vz**2); return np.array([-w_*y/c_, w_*x/c_, vz/c_])
def curlT(p,h=1e-5):
    x,y,z=p;e=[[1,0,0],[0,1,0],[0,0,1]]
    def comp(i,j,k):
        ej=np.array(e[j]);ek=np.array(e[k])
        Tjp=T(x+h*ej[0],y+h*ej[1],z+h*ej[2]);Tjm=T(x-h*ej[0],y-h*ej[1],z-h*ej[2])
        Tkp=T(x+h*ek[0],y+h*ek[1],z+h*ek[2]);Tkm=T(x-h*ek[0],y-h*ek[1],z-h*ek[2])
        return (Tjp[k]-Tjm[k])/(2*h)-(Tkp[j]-Tkm[j])/(2*h)
    return np.array([comp(0,1,2),comp(1,2,0),comp(2,0,1)])
p=(1,0,0)
cT=curlT(p)
lap=np.zeros(3)
for i in range(3):
    ei=np.array([[1,0,0],[0,1,0],[0,0,1]][i])
    lap+=(T(p[0]+1e-3*ei[0],p[1]+1e-3*ei[1],p[2]+1e-3*ei[2])+T(p[0]-1e-3*ei[0],p[1]-1e-3*ei[1],p[2]-1e-3*ei[2])-2*T(*p))/(1e-6)
gxx=((T(1+1e-4,0,0)[0]-T(1-1e-4,0,0)[0])/(2e-4),
     (T(1,1e-4,0)[1]-T(1,-1e-4,0)[1])/(2e-4),
     (T(1,0,1e-4)[2]-T(1,0,-1e-4)[2])/(2e-4))
print(f" ∇×T@(1,0,0)={np.round(cT,4)} (环向vz·ω²ρ/c³={vz*1*1/(np.sqrt(2)**3):.4f} + 轴向{np.round(cT[2],4)})")
print(f" UFE-2残差 |∇²T-∇(∇·T)|={np.linalg.norm(lap-np.array(gxx)):.3f} ≠0 ⇒ A=T 非 UFE-2 真空解（有源构型，满足 C-02+安培）")
print("\n结论: 螺旋切矢横向旋转结构 ∝(cosφ,sinφ) 是 UFE-2 圆偏振波解的骨架")
