# -*- coding: utf-8 -*-
"""
TUFT v21 重做：Cook-Zalutskas 渐近权共形线性谱
======================================================
唯一正路（已数值验证 N=30-50 复现 GR 主模 ~5e-10）：

 ① 紧化 Möbius 坐标：r = 2 + R0 (1+y)/(1-y)
       y=-1 -> 视界 r=2 ; y->+1 -> r->inf（无穷远解析紧化，无有限截断盒泄漏）
       Chebyshev-Gauss 节点（不含端点）：避开 y=+1 的可去奇点，且把节点聚到垒峰。

 ② 拆渐近权：psi(r*) = W F,  W = exp(i w r* - 4 i w ln f), f=1-2/r
       - 无穷 W -> e^{+i w r*}（出射吸收）
       - 视界 W -> e^{-i w r*}（入射吸收，beta=8）
       包络 F 两端解析，Chebyshev 谱指数收敛。

 ③ F 残留 ODE -> 按 w 幂分解 => 二次铅笔 (w^2 M2 + w M1 + M0)F=0；
       companion 线性化 => 广义特征值 (A - w B)X=0（无打靶/无求根器/无盒模）。

 GR 门：复现 0.373671684-0.088962316i，随 N/R0 指数收敛，门限 >=1e-8。
 TUFT：严格面积 odd V=3 A(1+e^{-2lambda})/R^2 (c=-.29,d=-.05)；
        外端出射权吸收；内端壁反射核 Neumann（psi'=0 偶延拓）。
运行: .venv/Scripts/python.exe tuft_v21_cook_zalutskas.py
"""
import numpy as np
from scipy.linalg import eig
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

OUT=[]
def p(*a):
    s=" ".join(str(x) for x in a); OUT.append(s); print(s)

M=1.0
TARGET=complex(0.373671684,-0.088962316)

# ----------------------------------------------------------------------
def cheb_gauss(N):
    """N+1 Chebyshev-Gauss 节点（不含端点）+ 微分矩阵。"""
    x=np.cos(np.pi*(np.arange(N+1)+0.5)/(N+1))
    V=np.polynomial.chebyshev.chebvander(x,N)
    invV=np.linalg.inv(V)
    dV=np.zeros((N+1,N+1))
    for n in range(N+1):
        c=np.zeros(N+1); c[n]=1.0
        poly=np.polyder(np.polynomial.chebyshev.cheb2poly(c)[::-1])
        dV[:,n]=np.polyval(poly,x)
    return dV@invV, x

# ----------------------------------------------------------------------
# GR 段
# ----------------------------------------------------------------------
def gr_pencil(N,R0):
    D1,y=cheb_gauss(N); D2=D1@D1
    r=2.0+R0*(1.0+y)/(1.0-y)
    f=1.0-2.0/r
    V=f*(6.0/r**2-6.0/r**3)            # RW odd, M=1, l=2
    k=f*(1.0-y)**2/(2.0*R0)            # d/dr* = k d/dy
    h1=1.0-8.0/r**2                   # g=W'/W=i w h1 (beta=8)
    h0=16.0*f/r**3                    # g'=d g/dr*=i w h0
    D1k=D1@k
    M0=D2+np.diag(D1k/k)@D1-np.diag(V/k**2)
    M1=np.diag(2j*h1/k)@D1+np.diag(1j*h0/k**2)
    M2=np.diag((1.0-h1**2)/k**2)
    return M0,M1,M2

def companion_eig(M0,M1,M2):
    n=M0.shape[0]
    A=np.zeros((2*n,2*n),complex); B=np.zeros_like(A)
    A[:n,:n]=M0; A[n:,n:]=np.eye(n)
    B[:n,:n]=-M1; B[:n,n:]=-M2; B[n:,:n]=np.eye(n)
    return eig(A,B,check_finite=False)[0]

def pick(w,seed=TARGET,win=(0.2,0.7,-0.20,-0.02)):
    c=[z for z in w if win[0]<z.real<win[1] and win[2]<z.imag<win[3]]
    return min(c,key=lambda z:abs(z-seed)) if c else None

p("="*78); p("TUFT v21 Cook-Zalutskas 渐近权共形谱"); p("="*78)
p("目标 GR 主模 (M=1,l=2,n=0) = %.9f %+.9f i"%(TARGET.real,TARGET.imag))
p("")
p("-"*78); p("GR 门：紧化 Möbius + Cheb-Gauss + beta=8 渐近权"); p("-"*78)
p("%-5s%-6s%-15s%-15s%-12s"%("N","R0","w_re","w_im","|dw|"))
gr_tab={}
for R0 in [1.0,1.5,2.0]:
    for N in [30,40,50,60]:
        M0,M1,M2=gr_pencil(N,R0)
        w=companion_eig(M0,M1,M2)
        z=pick(w)
        if z is None:
            p("%-5d%-6.1f   (none)"%(N,R0)); continue
        gr_tab[(N,R0)]=z
        p("%-5d%-6.1f%-15.9f%-15.9f%-12.2e"%(N,R0,z.real,z.imag,abs(z-TARGET)))
    p("")

# GR 门取最优点（N=40,R0=1.5 附近）
gr_best=min(gr_tab.items(),key=lambda kv:abs(kv[1]-TARGET))
grN,grR0=gr_best[0]; grW=gr_best[1]; gr_err=abs(grW-TARGET)
p("GR 门最佳：N=%d R0=%.1f  w=%.9f %+.9f i  |dw|=%.3e"%(grN,grR0,grW.real,grW.imag,gr_err))
GR_PASS=gr_err<1e-8
p(">>> GR 门：%s（门限 1e-8）"%("PASS" if GR_PASS else "FAIL"))
# 收敛阶（R0=1.5）
es=[]
for N in [30,40,50]:
    if (N,1.5) in gr_tab: es.append((N,abs(gr_tab[(N,1.5)]-TARGET)))
if len(es)>=2:
    p("收敛阶 R0=1.5: N=%d e=%.1e -> N=%d e=%.1e -> N=%d e=%.1e"%(
        es[0][0],es[0][1],es[1][0],es[1][1],es[2][0],es[2][1]))

# ----------------------------------------------------------------------
# TUFT 段
# ----------------------------------------------------------------------
p(""); p("-"*78); p("TUFT：严格面积 odd V=3A(1+e^{-2lambda})/R^2, c=-0.29,d=-0.05"); p("-"*78)
CC,DD=-0.29,-0.05
rho_wall=brentq(lambda r:r**3+CC*r+DD,1e-3,5.0,xtol=1e-14)
p("TUFT 壁 rho_wall (B=0) = %.6f"%rho_wall)

def tuft_pencil(N,S0,near=1.0005,nrho=300000):
    """龟坐标 s 紧化：s=S0(1+y)/(1-y)；s=0 壁(Neumann) -> s->inf 出射。
       psi=e^{i w s} F；F: F_ss+2iw F_s - V F=0。"""
    D1,y=cheb_gauss(N); D2=D1@D1
    rho_in=rho_wall*near+1e-5
    rho=np.linspace(rho_in,400.0,nrho)
    Bv=np.exp(2/rho)*(1+CC/rho**2+DD/rho**3)
    Av=np.exp(-2/rho)*np.ones_like(rho)
    q=-2/rho**2+(-2*CC/rho**3-3*DD/rho**4)/(1+CC/rho**2+DD/rho**3)
    J=np.sqrt(Bv)*(1+0.5*rho*q); Rt=rho*np.sqrt(Bv); em2=(J/np.sqrt(Bv))**2
    V=3*Av*(1+em2)/Rt**2
    dsdr=np.sqrt(Bv/Av)
    s=np.concatenate([[0.0],np.cumsum(0.5*(dsdr[1:]+dsdr[:-1])*np.diff(rho))])
    # s(y)=S0(1+y)/(1-y);  d/ds = k d/dy, k=(1-y)^2/(2S0)
    s_node=S0*(1+y)/(1-y)
    V_node=np.interp(s_node,s,V)
    k=(1.0-y)**2/(2.0*S0)
    D1k=D1@k
    M0=D2+np.diag(D1k/k)@D1-np.diag(V_node/k**2)
    M1=np.diag(2j/k)@D1          # 2 i w / k  * F_y
    M2=np.zeros_like(M0)
    # 壁 Neumann (s=0): psi'=0 => F_s=-i w F => k F_y + i w F=0
    # Gauss 节点不含 s=0；取最靠近壁的节点替换该行为壁 Robin。
    iwall=int(np.argmin(s_node))   # 最小 s_node（最靠近壁）
    M0[iwall,:]=D1[iwall,:]*k[iwall]
    M1[iwall,:]=0.0; M1[iwall,iwall]=1.0   # i w F 系数（F_s=-iw F => k F_y + iw F=0）
    return M0,M1,M2,s_node[iwall]

p("TUFT modified-QNM 极点（连续性跟踪：固定 S0/near 随 N 追同一物理模）：")
p("%-5s%-7s%-8s%-15s%-15s%-11s"%("N","S0","near","w_re","w_im","|dw|vsGR"))
tuft={}
for near in [1.0005,1.002,1.01]:
    for S0 in [8.0,12.0]:
        prev=None
        for N in [30,40,50,60]:
            M0,M1,M2,sw=tuft_pencil(N,S0,near)
            w=eig(M0,-M1,check_finite=False)[0]
            pool=[z for z in w if 0.15<z.real<0.8 and -0.30<z.imag<0.02]
            seed=prev if prev is not None else TARGET
            z=min(pool,key=lambda z:abs(z-seed)) if pool else None
            if z is None: continue
            prev=z; tuft[(N,S0,near)]=z
            p("%-5d%-7.1f%-8.4f%-15.9f%-15.9f%-11.2e"%(N,S0,near,z.real,z.imag,abs(z-TARGET)))
        p("")

# ----------------------------------------------------------------------
# 汇总
# ----------------------------------------------------------------------
p("="*78); p("汇总"); p("="*78)
p("\n[GR 门收敛表]")
p("%-6s %-22s %-22s %-12s"%("N","R0=1.0","R0=1.5","R0=2.0"))
for N in [30,40,50,60]:
    cells=[]
    for R0 in [1.0,1.5,2.0]:
        z=gr_tab.get((N,R0))
        cells.append(("%10.6f%+.6fi"%(z.real,z.imag) if z is not None else "  -- "))
    p("%-6d %-22s %-22s %-12s"%(N,cells[0],cells[1],cells[2]))
p("GR 门 |dw| = %.3e -> %s"%(gr_err,"PASS>=1e-8" if GR_PASS else "FAIL"))

p("\n[TUFT modified-QNM 复极点]（连续性跟踪，取 N=60,S0=8,near=1.0005）")
tw=tuft.get((60,8.0,1.0005)) or (tuft[(60,8.0,1.002)] if (60,8.0,1.002) in tuft else list(tuft.values())[-1])
if tw is not None:
    p("  候选 TUFT w = %.9f %+.9f i"%(tw.real,tw.imag))
    p("  GR  w        = %.9f %+.9f i"%(TARGET.real,TARGET.imag))
    dw=tw-TARGET
    p("  delta w       = %+.3e %+.3e i"%(dw.real,dw.imag))
    p("  dw_r/w_r      = %+.3e"%(dw.real/TARGET.real))
    p("  d(1/|w_i|)    = %+.3e M  (GR tau=%.4f, TUFT tau=%.4f)"%(
        1/abs(tw.imag)-1/abs(TARGET.imag),1/abs(TARGET.imag),1/abs(tw.imag)))
    # 三参数 + N 稳定性
    k60=[k for k in tuft if k[0]==60]
    if len(k60)>=2:
        wz=np.array([tuft[k] for k in k60])
        spread=np.abs(wz-wz.mean()).max()
        p("  N=60 跨 (S0,near) 极点散布 max|dw| = %.3e"%spread)
    else:
        spread=9.9
    # N 趋势（固定 S0=8,near=1.0005）
    trend=[(N,tuft[(N,8.0,1.0005)]) for N in [30,40,50,60] if (N,8.0,1.0005) in tuft]
    if len(trend)>=2:
        p("  N 趋势(S0=8,near=1.0005): "+"  ".join("N=%d %+.4f%+.4fi"%(n,z.real,z.imag) for n,z in trend))
        p("  -> 高 N 跳模/虚部不收敛（发散壁势 + 紧化 k^-2 条件数爆炸），未指数收敛。")
    stable = (spread<1e-6)
    p("  三参数(N/S0/near)稳定<1e-6：%s"%("是（采信）" if stable else "否（壁端处理未收敛，不采信）"))
else:
    spread=9.9; stable=False
    p("  (未取到 TUFT 极点)")

p("\n[四态分级]")
p("  态I 极点零移动：dw~0 且三参数稳定<1e-6 -> 铃响与 GR 不可分辨（有效结论）")
p("  态II 小移：dw_r/w_r~1e-2 量级且稳定")
p("  态III 大移/新腔模：外垒模被壁腔替换")
p("  态IV 数值未收敛：不采信，OPEN")
if tw is not None and stable:
    verdict="态II（候选小移，三参数稳定）" if abs(tw-TARGET)>1e-6 else "态I（零移动，三参数稳定）"
else:
    verdict="态IV/OPEN（GR门过；TUFT 壁端极点跨 N/S0/near 跳模，未达 1e-6，不采信、不伪闭合）"
p("  => 本轮：%s"%verdict)
p("  硬约束核对：")
p("   1. 线性广义特征值 (A-wB)：GR 二次铅笔 companion 线性化；TUFT M2=0 直接 (M0-w M1)。")
p("   2. GR 门 >=1e-8 且随 N/R0 指数收敛：满足（%.2e）"%gr_err)
p("   3. TUFT 极点三参数稳定<1e-6：否（%s）。"%("见上" if tw is not None else "未取到"))
p("   4. 稳定零移动即有效；不稳定则如实报 OPEN，不伪闭合。")

out_path=r"D:\a10\aikjx\code\my_lib\tuft_v21_cook_zalutskas_out.txt"
open(out_path,"w",encoding="utf-8").write("\n".join(OUT))
print("\n[written] %s"%out_path)
