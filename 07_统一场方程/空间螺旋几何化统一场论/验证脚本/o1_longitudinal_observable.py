# -*- coding: utf-8 -*-
"""O-P1 全链路（续）：UFE-2 纵波的可观测特征（L3 试金石）
对比纵波 vs 横波的电磁观测量：
  纵波 A=A0cos(kz-ωt)ẑ:  B=0, E纵向, S=0(无能量流), u∝E², 色散ω=v_z·k
  横波 A=A0(cos,sin,0):  B≠0, E⊥B, S≠0(辐射), 色散ω=c·k
可区分预言（不依赖未知参数 f,A0）：纵波 S=0、B=0、v_z<c；横波 S≠0、B≠0、速度c
"""
import numpy as np
c_=1.0; f=1.0; A0=1.0; k=2.0; eps0=1.0; mu0=1.0
vz=0.6*c_            # 纵波速度（电荷轴向速度）
om_l=vz*k            # 纵波色散
om_h=c_*k            # 横波色散

def Along(x,y,z,t): return A0*np.cos(k*z-om_l*t)*np.array([0,0,1.0])
def Ahor(x,y,z,t): return A0*np.array([np.cos(k*z-om_h*t),np.sin(k*z-om_h*t),0.0])
def curl(Af,p,t,h=1e-5):
    x,y,z=p;e=[[1,0,0],[0,1,0],[0,0,1]]
    def comp(i,j,k):
        ej=np.array(e[j]);ek=np.array(e[k])
        Tjp=Af(x+h*ej[0],y+h*ej[1],z+h*ej[2],t);Tjm=Af(x-h*ej[0],y-h*ej[1],z-h*ej[2],t)
        Tkp=Af(x+h*ek[0],y+h*ek[1],z+h*ek[2],t);Tkm=Af(x-h*ek[0],y-h*ek[1],z-h*ek[2],t)
        return (Tjp[k]-Tjm[k])/(2*h)-(Tkp[j]-Tkm[j])/(2*h)
    return np.array([comp(0,1,2),comp(1,2,0),comp(2,0,1)])

print("== 纵波 vs 横波 可观测对比（数值） ==")
print(f"{'波':>6} | {'t':>5} {'|E|':>7} {'|B|':>7} {'|S|(坡印廷)':>10} {'u(能量密度)':>11} {'传播速度':>8}")
for name,Af,om in [("纵波",Along,om_l),("横波",Ahor,om_h)]:
    for t in [0.4,0.8]:
        x,y,z=0,0,0
        Bn=curl(Af,(x,y,z),t)
        En=-f*(Af(x,y,z,t+1e-5)-Af(x,y,z,t-1e-5))/(2e-5)
        S=np.cross(En,Bn)/mu0
        u=0.5*eps0*np.sum(En*En)+0.5*np.sum(Bn*Bn)/mu0
        v=om/k
        print(f"{name} | {t:.1f} {np.linalg.norm(En):.3f} {np.linalg.norm(Bn):.3f} {np.linalg.norm(S):.3f} {u:.3f} {v:.3f}")

print("\n== 色散与传播速度 ==")
print(f" 纵波: ω=v_z·k={om_l:.2f}, v=ω/k=v_z={vz:.2f}c < c  (慢波, 电荷轴向速度)")
print(f" 横波: ω=c·k  ={om_h:.2f}, v=ω/k=c ={c_:.2f}c      (光速横波, 标准电磁辐射)")

print("\n== 可区分预言（不依赖未知参数 f,A0,ε0,μ0 的相对结构） ==")
print(" ① 纵波 B=0、坡印廷 S=0（无电磁能流）—— 标准横电磁波 B≠0、S≠0（辐射）")
print(" ② 纵波以电荷轴向速度 v_z<c 传播（慢纵波）；横波以 c 传播")
print(" ③ 纵波 E 沿传播方向（纵向）；横波 E⊥传播方向（横向）")
print(" ⇒ 在电荷螺旋运动系统中，若存在 UFE-2 纵波，应观测到 B=0、S=0 的慢纵向电场波；这是与标准电动力学可区分的候选 L3 预言")
