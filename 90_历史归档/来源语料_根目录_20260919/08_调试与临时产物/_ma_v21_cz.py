# -*- coding: utf-8 -*-
"""
MainAgent v21：Cook-Zalutskas 型带渐近权的共形谱（GR 自洽门）
================================================================
无限龟坐标共形压缩  r* = L*artanh x,  x in (-1,1)（Gauss 配点，避开奇异端点）:
  视界 x->-1: e^{-i w r*} ~ (1+x)^{-i w L/2}
  无穷 x->+1: e^{+i w r*} ~ (1-x)^{-i w L/2}
双端渐近同时吸收进权  psi = (1-x^2)^{-i w L/2} F(x)，F 光滑有界。
代入 RW psi_{r*r*}+[w^2-V]psi=0，包络方程（M=1 几何单位）:
  (1-x^2)^2 F'' + 2x(1-x^2)(i w L -1) F'
   + (1-x^2)(w^2 L^2 + i w L) - L^2 V(x)] F = 0
=> (A2 w^2 + A1 w + A0) f = 0，companion 广义特征值；无打靶/无匹配点/无盒模。
必须 10 位复现 0.373671684-0.088962316（M=1），随 N、L 谱收敛。
"""
import numpy as np, sys
from scipy.linalg import eig
from scipy.interpolate import CubicSpline
def log(*a):
    print(" ".join(str(x) for x in a),flush=True);sys.stdout.flush()
CAT=0.3736716844-0.0889623157j

# ---- Schwarzschild M=1 ----
r=np.concatenate([np.linspace(2+1e-12,3.0,60000),np.linspace(3.0,10.0,60000),
                  np.linspace(10.0,2000.0,80000)])
r=np.unique(r); rs=r+2.0*np.log(r/2.0-1.0); f=1-2.0/r
V=f*(6.0/r**2-6.0/r**3)
o=np.argsort(rs); r_of_rs=CubicSpline(rs[o],r[o])      # r* -> r
rs_min,rs_max=float(rs[o][0]),float(rs[o][-1])
def V_of_rs(s):
    if s < rs_min+2.0: return 0.0          # 深视界 V~e^{r*}->0
    if s > rs_max:
        return 6.0/(s*s)                    # V~6/r*^2 远尾
    rr=float(r_of_rs(s)); ff=1-2/rr
    return ff*(6/rr**2-6/rr**3)

def gauss_points(N):
    return np.cos((2*np.arange(N)+1)*np.pi/(2*N))      # 不含端点

def cheb_diff_gauss(x):
    N=len(x)
    def Tn(n,z):
        return np.cos(n*np.arccos(z))
    def dTn(n,z):
        th=np.arccos(z); s=np.sin(th)
        if n==0: return np.zeros_like(z)
        return n*np.sin(n*th)/np.where(np.abs(s)>1e-12,s,1e-12)
    T=np.zeros((N,N)); Tp=np.zeros((N,N))
    for n in range(N):
        T[:,n]=Tn(n,x); Tp[:,n]=dTn(n,x)
    D=Tp@np.linalg.inv(T)
    return D

def gr_modes(N,L):
    x=gauss_points(N)
    rs=L*np.arctanh(x)
    Vcol=np.array([V_of_rs(s) for s in rs])
    D1=cheb_diff_gauss(x); D2=D1@D1
    one=1-x*x
    A2=(L**2)*np.diag(one)
    A1=2j*L*(np.diag(x*one)@D1) + 1j*L*np.diag(one)
    A0=np.diag(one**2)@D2 - 2.0*(np.diag(x*one)@D1) - (L**2)*np.diag(Vcol)
    n=N; I=np.eye(n); Z=np.zeros((n,n))
    M=np.vstack([np.hstack([A0,A1]),np.hstack([Z,I])])
    Bm=np.vstack([np.hstack([Z,-A2]),np.hstack([I,Z])])
    w,_=eig(M,Bm); w=np.asarray(w).ravel()
    w=w[np.isfinite(w.real)&np.isfinite(w.imag)]
    w=w[(w.real>0.15)&(w.real<0.9)&(w.imag>-0.35)&(w.imag<0)]
    w=w[np.argsort(np.abs(w-CAT))]
    return w[:14]

log("="*80); log("GR 门：Cook-Zalutskas 渐近权共形谱（固定截断 r*=±80，加密 N，模追踪）"); log("="*80)
RSTAR=80.0
def L_for_N(N):
    xm=np.cos(np.pi/(2*N))
    return RSTAR/float(np.arctanh(xm))
def track(seq):
    """从目录种子出发，每级 N 选与上一支最近的下半平面模，返回轨迹。"""
    prev=CAT; traj=[]
    for N in seq:
        ws=gr_modes(N,L_for_N(N))
        k=np.argmin(np.abs(ws-prev)); z=ws[k]; traj.append((N,z,abs(z-CAT)))
        prev=z
    return traj
seq=[50,70,90,120,160,220]
traj=track(seq)
for N,z,derr in traj:
    log("  N=%-3d L=%6.2f  追踪模=%.10f %+.10f i  |d|=%.3e"%(N,L_for_N(N),z.real,z.imag,derr))
zs=[t[1] for t in traj]; scatter=max(abs(z-np.mean(zs[-3:])) for z in zs[-3:])
log("  末三级 (N=120/160/220) 最大散布=%.3e"%scatter)
zfinal=traj[-1][1]
log("  判定: %s"%("GR 门 PASS（可进入 TUFT）" if abs(zfinal-CAT)<1e-6 and scatter<1e-6
                else "未达门限（仍跳模/平台，记录为方法不达标）"))

