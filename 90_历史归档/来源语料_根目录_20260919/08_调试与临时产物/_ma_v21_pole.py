# -*- coding: utf-8 -*-
"""
MainAgent v21 独立复算（修正路线）：TUFT 反射核 modified-QNM
====================================================================
勘误#18/#19/E430 教训：任何积分型 Wronskian/打靶匹配在亚垒复根附近都
病态（波函数带 e^{+/-积分kappa} 指数因子，条件数极差；Muller 跑飞已实证）。
E430 指定的"解析 Frobenius / Leaver 全局 ansatz"在【数值势】上的正确对应是
全域谱配点 + 二次特征值问题（QEP）：一次离散、无打靶、无匹配点、边界隐式包含。

  ODE:  psi''(x) + [w^2 - V(x)] psi = 0
  GR  : x=r* in [-R,R];  视界端入射 psi'=-i w psi ; 无穷端出射 psi'=+i w psi
  TUFT: x=s  in [0,R];   反射核 Neumann psi'=0    ; 无穷端出射 psi'=+i w psi
  Chebyshev 配点 D；线性映射 D_x；组装
     (A2 w^2 + A1 w + A0) psi = 0
  线性化 companion -> 2N 广义特征值；在目录附近选模。

GR 自洽门：必须复现 0.373671684-0.088962316i（Leaver E436-438 已给10位真值）。
收敛判据（v13/v14 缺失，本次强制）：模须随 N、域 R 稳定 <1e-6。
过门才换 TUFT 严格面积 odd 势 + Neumann，并加近壁起点/映射收敛。
几何单位 G=c=M=1；e^{-iwt}，QNM w=w_r-i|w_i|。
"""
import sys, numpy as np
from scipy.linalg import eig
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

def log(*a):
    print(" ".join(str(x) for x in a), flush=True); sys.stdout.flush()

CATALOG=0.3736716844-0.0889623157j

def cheb(N):
    """Trefethen cheb D；点 y 从 +1 降到 -1（index0=+1 外端, indexN=-1 内端）。"""
    if N==0: return np.array([[0.]]), np.array([1.])
    y=np.cos(np.pi*np.arange(N+1)/N)
    c=np.r_[2.0,np.ones(N-1),2.0]*(-1.0)**np.arange(N+1)
    Y=np.tile(y,(N+1,1)); dY=Y-Y.T
    D=(c[:,None]/c[None,:])/(dY+np.eye(N+1))
    D=D-np.diag(D.sum(1))
    return D,y

def solve_qep(Vcol, Dx, bc_inner, bc_outer, target=CATALOG, k_keep=12):
    """
    Vcol: 配点上 V(x)（长度 N+1）。Dx: d/dx 谱矩阵。
    bc_inner/outer: ('robin', s)  psi'=s*i*w*psi ; 或 ('neumann',) psi'=0
    返回距 target 最近的 k 个下半平面特征值。
    """
    n=len(Vcol); I=np.eye(n); Z=np.zeros((n,n))
    D2=Dx@Dx
    A2=I.copy(); A1=np.zeros((n,n),complex); A0=D2-np.diag(Vcol)
    # 外端 index0；内端 index n-1
    for idx,bc in ((0,bc_outer),(n-1,bc_inner)):
        A0[idx,:]=Dx[idx,:]
        A2[idx,:]=0.0
        if bc[0]=='robin':
            s=bc[1]                      # psi' = s i w psi  ->  Dx psi - s i w psi=0
            A1[idx,idx]=-s*1j
        else:                            # neumann psi'=0
            A1[idx,idx]=0.0
    # companion: [A0 A1;0 I] z = w [0 -A2; I 0] z
    top=np.hstack([A0,A1]); bot=np.hstack([Z,I])
    Bb=np.hstack([Z,-A2]); Cc=np.hstack([I,Z])
    Av=np.vstack([top,bot]); Bv=np.vstack([Bb,Cc])
    w,_=eig(Av,Bv,check_finite=False,right=True)
    w=np.asarray(w).ravel()
    w=w[np.isfinite(w.real)&np.isfinite(w.imag)]
    w=w[(w.real>0.05)&(w.real<1.5)&(w.imag<0)&(w.imag>-1.5)]
    w=w[np.argsort(np.abs(w-target))]
    return w[:k_keep]

# ======================================================================
# 势：GR Schwarzschild l=2 s=-2
# ======================================================================
ell=2
def build_GR(rmin=2.0+1e-14, rmax=400.0, n=120000):
    r=np.concatenate([np.linspace(rmin,3.0,n//3),
                      np.linspace(3.0,10.0,n//3),
                      np.linspace(10.0,rmax,n-2*n//3)])
    r=np.unique(r)
    rst=r+2.0*np.log(r/2.0-1.0)
    f=1-2.0/r
    V=f*(ell*(ell+1)/r**2-6.0/r**3)
    o=np.argsort(rst)
    return CubicSpline(rst[o],V[o]),rst,r,V

Vspl,rst_gr,r_gr,Vg=build_GR()
ipk=np.argmax(Vg)
log("="*82)
log("GR 门（全域 Chebyshev QEP，非打靶）  垒顶 r=%.5f r*=%.5f sqrtV=%.6f"%(
    r_gr[ipk],rst_gr[ipk],np.sqrt(Vg[ipk])))
log("="*82)

def gr_mode(N,R):
    D,y=cheb(N)                 # y:+1(外,r*=+R) ... -1(内,r*=-R)
    x=R*y
    Dx=D/R
    Vcol=np.array([float(Vspl(float(xi))) if abs(xi)<=float(rst_gr[-1]) else 0.0 for xi in x])
    Vcol=np.clip(Vcol,0,None)
    ws=solve_qep(Vcol,Dx,('robin',-1.0),('robin',+1.0))   # 内入射 s=-1,外出射 s=+1
    return ws[0],ws

log("\n  GR 收敛表（N=点数-1, R=截断 r*）：")
gr_tab={}
for (N,R) in [(300,60.0),(400,80.0),(500,80.0),(500,120.0),(700,100.0)]:
    w0,_=gr_mode(N,R); gr_tab[(N,R)]=w0
    log("   N=%-3d R=%-5.0f  w=%.9f %+.9f i  |d-catalog|=%.2e"%(
        N,R,w0.real,w0.imag,abs(w0-CATALOG)))
zvals=list(gr_tab.values())
gr_scatter=max(abs(z-np.mean(zvals)) for z in zvals)
zgr=gr_tab[(500,80.0)]
gr_gate=(abs(zgr-CATALOG)<1e-5) and (gr_scatter<1e-5)
log("  GR 最大散布=%.3e ; 门判定: %s"%(gr_scatter,"PASS"%() if gr_gate else "FAIL"))
if not gr_gate:
    log("[STOP] GR 谱门未过，不进入 TUFT（可能需加密中段配点/改映射）。")
    sys.exit(0)

# ======================================================================
# TUFT 严格面积 odd 势，x=s 龟坐标 ∈[0,R]；壁端 Neumann，外端出射
# ======================================================================
CM,CD=-0.29,-0.05
rho_h=brentq(lambda r:r**3+CM*r+CD,1e-3,5.0,xtol=1e-14)
log("\n"+"="*82); log("TUFT 反射核（Chebyshev QEP）  rho_h=%.7f"%rho_h); log("="*82)

def build_TUFT(rlo_factor=1.0008,rho_big=400.0,n=200000):
    rlo=rho_h*rlo_factor
    rho=np.concatenate([np.linspace(rlo,1.5,n//2),
                        np.linspace(1.5,8.0,n//4),
                        np.linspace(8.0,rho_big,n-3*n//4)])
    rho=np.unique(rho)
    A=np.exp(-2/rho)
    Bb=1+CM/rho**2+CD/rho**3
    B=np.exp(2/rho)*Bb
    Bpb=-2*CM/rho**3-3*CD/rho**4
    logBp=-2/rho**2+Bpb/Bb+2/rho
    J=np.sqrt(B)*(1+0.5*rho*logBp)
    em2=(J/np.sqrt(B))**2
    Rarr=rho*np.sqrt(B)
    V=3*A*(1+em2)/Rarr**2
    dsdr=np.sqrt(B/A)
    s=np.concatenate([[0.0],np.cumsum(0.5*(dsdr[1:]+dsdr[:-1])*np.diff(rho))])
    o=np.argsort(s)
    return CubicSpline(s[o],V[o]),s,Rarr,V,rho

Vtu,st,Rt,Vt,rhot=build_TUFT()
iout=np.where(Rt>2.5)[0]; ip2=iout[int(np.argmax(Vt[iout]))]
log("  外垒峰 R=%.5f sqrtV=%.6f s_peak=%.5f  L=%.5f 2L=%.5f  Vwall=%.2e"%(
    Rt[ip2],np.sqrt(Vt[ip2]),st[ip2],st[ip2],2*st[ip2],Vt[0]))

def tuft_mode(N,R,rlo=1.0008,target=zgr,vspl=None):
    if vspl is None: vspl=Vtu
    D,y=cheb(N)                 # y:+1 -> s=R(外); y:-1 -> s=0(壁)
    s=R*(y+1.0)/2.0
    Ds=(2.0/R)*D
    smax=float(st[-1])
    Vcol=np.array([float(vspl(float(si))) if si<=smax else 0.0 for si in s])
    Vcol=np.clip(Vcol,0,None)
    ws=solve_qep(Vcol,Ds,('neumann',),('robin',+1.0),target=target)
    return ws[0],ws

log("\n  TUFT 收敛表（N / R / 近壁离壁因子）：")
tu_tab={}
configs=[(400,80.0,1.0008),(500,80.0,1.0008),(600,100.0,1.0008),
         (500,140.0,1.0008),(500,80.0,1.0004),(500,80.0,1.002)]
for (N,R,rlo) in configs:
    vs=None
    if rlo!=1.0008:
        vs,_,_,_,_=build_TUFT(rlo_factor=rlo)
    w0,_=tuft_mode(N,R,rlo,vspl=vs)
    tu_tab[(N,R,rlo)]=w0
    log("   N=%-3d R=%-5.0f rlo=%-7s w=%.9f %+.9f i  dw=%.2e"%(
        N,R,str(rlo),w0.real,w0.imag,abs(w0-zgr)))
mc=np.mean(list(tu_tab.values()))
tu_scatter=max(abs(z-mc) for z in tu_tab.values())
zt=tu_tab[(500,80.0,1.0008)]
conv=tu_scatter<1e-5
log("  TUFT 最大散布=%.3e  收敛: %s"%(tu_scatter,"CONVERGED" if conv else "NOT-CONVERGED"))

log("\n"+"-"*82)
dwr=(zt.real-CATALOG.real)/CATALOG.real
tau_g=-1/CATALOG.imag; tau_t=-1/zt.imag
log("  GR   %.6f%+.6fi tau=%.4f M"%(CATALOG.real,CATALOG.imag,tau_g))
log("  TUFT %.6f%+.6fi tau=%.4f M"%(zt.real,zt.imag,tau_t))
log("  dw_r/w_r=%+.4f%%   dtau=%+.4f M"%(100*dwr,tau_t-tau_g))
if not conv:
    log("  => 未通过多重收敛，modified-QNM 极点是否移动维持 OPEN（不伪闭合）。")
elif abs(dwr)<1e-3:
    log("  => 态I：极点移动~0，铃响与 GR 不可分辨（有效结论）。")
elif abs(dwr)<0.05:
    log("  => 态II：小移 %+.2f%%，寿命%+.2f M（待 GW/EHT）。"%(100*dwr,tau_t-tau_g))
else:
    log("  => 态III：大移 %+.2f%%。"%(100*dwr))
log("="*82)
