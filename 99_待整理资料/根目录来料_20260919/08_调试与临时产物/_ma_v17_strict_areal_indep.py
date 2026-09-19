# -*- coding: utf-8 -*-
# MainAgent v17 严格面积 odd 势独立复算 v2（全向量化；修正 GR 导数 + 外垒/亚垒选段）
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
import sympy as sp

OUT=open("_ma_v17_strict_areal_indep_out.txt","w",encoding="utf-8")
def log(s=""): print(s); OUT.write(str(s)+"\n"); OUT.flush()

def tuft_geom(r,cm,d):
    r=np.asarray(r,float); A=np.exp(-2/r); h=1+cm/r**2+d/r**3; B=np.exp(2/r)*h
    q=-2/r**2+(-2*cm/r**3-3*d/r**4)/h          # d lnB/dr
    sB=np.sqrt(B); J=sB*(1+0.5*r*q); R=r*sB; em2=(J/sB)**2
    return A,B,R,J,em2,3*A*(1+em2)/R**2
def gr_geom(r):
    r=np.asarray(r,float)
    A=((2*r-1)/(2*r+1))**2; B=((2*r+1)/(2*r))**4
    q=-4/(r*(2*r+1))                            # d ln[(1+1/2r)^4]/dr  （v1 曾写错）
    sB=np.sqrt(B); J=sB*(1+0.5*r*q); R=r*sB; em2=(J/sB)**2
    return A,B,R,J,em2,3*A*(1+em2)/R**2
def Vrw(R): return (1-2/R)*(6/R**2-6/R**3)
def outer_peak(geomf,args,rlo,rhi,N=2_000_001):
    r=np.linspace(rlo,rhi,N); *_,V=geomf(r,*args)
    ii=np.where((V[1:-1]>V[:-2])&(V[1:-1]>V[2:]))[0]+1   # 所有局部峰
    R=geomf(r,*args)[2]
    k=ii[np.argmax(R[ii])]                                # 外垒=面积半径最大的峰
    return r[k],R[k],V[k]

log("① 真 GR 门：Schwarzschild 各向同性 -> 面积管道（导数已修正）")
r=np.linspace(0.50005,400,3_000_001); R=gr_geom(r)[2]; V=gr_geom(r)[5]
m=R>=2.001
err=np.max(np.abs(V[m]-Vrw(R[m]))/Vrw(R[m]))
Rp,Vp=outer_peak(gr_geom,(),0.5001,400)[1:]
Rex=(9+np.sqrt(17))/4
Vex=Vrw(np.array([Rex]))[0]
log("  数值外垒 R=%.5f Vmax=%.8f sqrt=%.8f"%(Rp,Vp,np.sqrt(Vp)))
log("  解析驻点 R=%.6f V=%.8f sqrt=%.8f"%(Rex,Vex,np.sqrt(Vex)))
log("  逐点最大相对误差 = %.3e -> GR 门 %s"%(err,"PASS" if err<1e-6 else "FAIL"))
log("  V(3)=4/27=%.6f（sqrt %.4f），比真极值低 %.2f%%，非垒顶"%(4/27,np.sqrt(4/27),100*(Vex-4/27)/Vex))

log(""); log("② TUFT 外部支外垒（取面积半径最大的局部峰）")
for cm,d,lo,tag in [(0,0,1.02,"c=0   "),(-0.5,0,0.74,"c=-.5 "),(-0.29,-0.05,0.65,"c=-.29")]:
    rp,Rp,Vp=outer_peak(tuft_geom,(cm,d),lo,80)
    log("  %s rho_pk=%.4f R_pk=%.4f Vmax=%.6f sqrt=%.4f"%(tag,rp,Rp,Vp,np.sqrt(Vp)))
rr=np.linspace(0.9995,1.0005,4001); log("  c=0 颈 R_min=%.5f（解析 e=2.71828）"%tuft_geom(rr,0,0)[2].min())
for cm,d,tag in [(-0.5,0,"c=-.5 "),(-0.29,-0.05,"c=-.29")]:
    rh=brentq(lambda x:x**3+cm*x+d,1e-4,5,xtol=1e-14)
    A,B,R,J,e2,V=tuft_geom(np.array([rh*1.00002]),cm,d)
    s,_=quad(lambda x:np.sqrt(tuft_geom(np.array([x]),cm,d)[1][0]/tuft_geom(np.array([x]),cm,d)[0][0]),
             rh*1.00002,3.0,limit=300)
    log("  %s 壁 rho_h=%.4f 近壁 R=%.5f(->0) e^-2lambda=%.2e(g_RR->0) V~1/R2=%.2e；龟坐标到R3有限=%.2f M"
        %(tag,rh,R[0],e2[0],V[0],s))

log(""); log("③ c=-.29 严格 WKB：外垒亚垒段（按面积半径最大选段，非连核段）")
cm,d=-0.29,-0.05
rh=brentq(lambda x:x**3+cm*x+d,1e-4,5,xtol=1e-14)
rho=np.linspace(rh*1.00002,80,3_000_000); A,B,R,J,e2,V=tuft_geom(rho,cm,d)
ds=np.sqrt(B/A); s=np.concatenate([[0],np.cumsum(0.5*(ds[1:]+ds[:-1])*np.diff(rho))])
for w in [0.30,0.35,0.374,0.40]:
    msk=V>w**2
    if not msk.any(): log("  w=%.3f above barrier"%w); continue
    bd=np.where(np.diff(msk.astype(int))!=0)[0]
    segs=np.split(np.arange(len(rho)),bd+1) if msk[0] else np.split(np.arange(len(rho)),bd+1)
    pos=[g for g in segs if V[g].mean()>0 and msk[g].all()]
    pos=[g for g in pos if (V[g]-w**2).max()>0]
    if not pos: log("  w=%.3f above barrier"%w); continue
    g=max(pos,key=lambda g:R[g].mean())                 # 外垒段=平均面积半径最大
    K=np.trapz(np.sqrt(np.clip(V[g]-w**2,0,None)),s[g])
    log("  w=%.3f 外垒亚垒 s[%5.2f..%5.2f] K=%.3f 单通~e^-2K=%.3f"%(w,s[g[0]],s[g[-1]],K,np.exp(-2*K)))
valley=V[(s>3)&(s<6)].min()
log("  外垒与核间腔谷 Vmin=%.4f < .374^2=%.4f：%s（主频 O(1) 入腔）"%(valley,0.374**2,"YES" if valley<0.374**2 else "NO"))
log("END")
OUT.close()
