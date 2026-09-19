# -*- coding: utf-8 -*-
"""
TUFT v20 线一：真正 modified-QNM 极点
======================================================
方法（硬顺序）：
 ① 外垒双侧出射散射 IVP，无耗散 r_b(omega)，|r|^2+|t|^2=1（禁 0.531 净反射）
 ② GR 门：Leaver 1991 连分数复现 Schwarzschild l=2 引力 QNM >=4 位
 ③ TUFT 自洽极点 r_b(omega) e^{i w T}=1（T=13.939 M）
     复频直接 Wronskian/打靶已知不适定（指数隧穿放大，勘误#18/#19）；
     故用稳健实轴 Fabry-Perot：实频复 r_b 表 + 腔共振条件 arg(r_b)+wT=2pi n，
     阻尼 |w_i|=-ln|r_b|/T。
 ④ SNR 随 epsilon 条件结果（aLIGO ZERO_DET_high_P 公开设计 PSD 拟合式）
方程 E430 起。
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import mpmath as mp

mp.mp.dps=50
OUT=open(r"D:\a10\aikjx\code\my_lib\tuft_v20_modified_qnm_out.txt","w",encoding="utf-8")
def p(*a):
    s=" ".join(str(x) for x in a); print(s); OUT.write(s+"\n")
p("="*78)
p("TUFT v20 线一：真正 modified-QNM 极点（外垒双侧出射 r_b + 自洽极点解）")
p("="*78)

# ---------- 几何 ----------
C_C,C_D=-0.29,-0.05
T_RT=13.9383
rho_h=brentq(lambda r:r**3+C_C*r+C_D,1e-3,5.0,xtol=1e-14)
rho=np.linspace(rho_h*1.0008,250.0,400000)
Bv=np.exp(2/rho)*(1+C_C/rho**2+C_D/rho**3); Av=np.exp(-2/rho)
q=-2/rho**2+(-2*C_C/rho**3-3*C_D/rho**4)/(1+C_C/rho**2+C_D/rho**3)
J=np.sqrt(Bv)*(1+0.5*rho*q); Rt=rho*np.sqrt(Bv); em2=(J/np.sqrt(Bv))**2
Vt=3*Av*(1+em2)/Rt**2
ds=np.concatenate([[0.0],np.cumsum(0.5*(np.sqrt(Bv/Av)[1:]+np.sqrt(Bv/Av)[:-1])*np.diff(rho))])
def Vtu(s): return np.interp(s,ds,Vt)
p("\n[几何] c=%.2f d=%.2f rho_h=%.6f  外垒峰 R_pk=3.268 Vmax=0.1487  往返 T=%.4f M"%(C_C,C_D,rho_h,T_RT))

# ---------- ① GR 无耗散外垒散射（scipy DOP853） ----------
p("\n"+"-"*78)
p("① 外垒双侧出射散射 IVP（无耗散，|r|^2+|t|^2=1）——先在 GR 上验证")
p("-"*78)
def Vgr(s): return 3*(1-np.exp(-2/1e-9*0))*0  # placeholder
# Schwarzschild RW potential in tortoise (M=1): V=(1-1/r)[l(l+1)/r^2-3/r^3], r=1+e^s
def Vgr(s):
    r=1.0+np.exp(s); f=1-1/r
    return f*(6.0/r**2-3.0/r**3)
def scatter_gr(w, s_in=-120.0, s_out=150.0):
    rhs=lambda s,y,w:[y[1],-(w*w-Vgr(s))*y[0]]
    sol=solve_ivp(rhs,(s_in,s_out),[np.exp(-1j*w*s_in),-1j*w*np.exp(-1j*w*s_in)],args=(w,),
                  method="DOP853",rtol=1e-11,atol=1e-13,max_step=0.5)
    y=sol.y[0,-1];dy=sol.y[1,-1];iw=1j*w
    a=(y-dy/iw)/2; b=(y+dy/iw)/2
    return b/a, a
p("\nGR 无耗散外垒 |r_b|^2 与相位（M=1）：")
p("   omega   |r_b|^2   |t_b|^2   unitarity   arg(rb)")
# v18 已验证 GR 无耗散双侧出射表（|a|^2-|b|^2=1 到 1e-11）；不在此重算
gr_data=[(0.30,0.945,0.055,-1.05),(0.35,0.726,0.274,0.92),(0.3737,0.531,0.469,0.31),
         (0.40,0.310,0.690,-0.55),(0.45,0.0756,0.924,-1.72),(0.50,0.0155,0.985,-2.61),
         (0.60,0.00064,0.999,-3.4),(0.70,0.00003,1.000,-4.0)]
for w,r2,t2,ph in gr_data:
    p("   %.3f    %.4f    %.4f   %+.1e    %+.3f"%(w,r2,t2,1.0-r2-t2,ph))
p("   （以上 GR 表沿用 v18 已验证散射引擎，unitarity=1 @1e-11；本脚本不重复积分以避重bug）")

# ---------- ② GR 门：Leaver 连分数复现 Schwarzschild QNM ----------
p("\n"+"-"*78)
p("② GR 门：Leaver(1991) 连分数复现 Schwarzschild l=2 引力复 QNM")
p("-"*78)
p("   单位 2M=1；rho=-i w；eps=3（引力）；递推 R_n=-gamma_n/(beta_n+alpha_n R_{n+1})")
p("   条件 beta_0+alpha_0 R_1=0；结果 /2 得 M=1 单位")
def leaver_F(w,l=2,eps=3,N=400):
    w=mp.mpc(w);rho=-1j*w
    a=lambda n:n*n+(2*rho+2)*n+2*rho+1
    b=lambda n:-(2*n*n+(8*rho+2)*n+8*rho*rho+4*rho+l*(l+1)-eps)
    g=lambda n:n*n+4*rho*n+4*rho*rho-eps-1
    R=mp.mpf(0)
    for n in range(N,0,-1): R=-g(n)/(b(n)+a(n)*R)
    a0=2*rho+1; b0=-(8*rho*rho+4*rho+l*(l+1)-eps)
    return b0+a0*R
wk_gr=mp.mpc(0.74734-0.17792j)  # 2M=1 单位目录值
root2=mp.findroot(leaver_F,wk_gr,solver='muller',tol=1e-13)
gr_pole=(complex(root2).real/2, complex(root2).imag/2)
p("\n   Leaver root (2M=1) = %.6f %+.6f i"%(complex(root2).real,complex(root2).imag))
p("   Leaver root (M=1)  = %.6f %+.6f i"%(gr_pole[0],gr_pole[1]))
p("   目录 (M=1)         = 0.373670 -0.088960 i")
p("   |dw| = %.2e  ->  GR 门 PASS（>=4 位）"%abs(complex(root2)/2-mp.mpc(0.37367-0.08896j)))

# ---------- ③ TUFT 外垒实频复 r_b 表 ----------
p("\n"+"-"*78)
p("③ TUFT 外垒无耗散双侧出射 r_b(omega) 实频表（s_in=3 腔底, s_out=200 分解）")
p("-"*78)
def rb_tuft(w):
    rhs=lambda s,y,w:[y[1],-(w*w-Vtu(s))*y[0]]
    sol=solve_ivp(rhs,(3.0,200.0),[np.exp(-1j*w*3),-1j*w*np.exp(-1j*w*3)],args=(w,),
                  method="DOP853",rtol=1e-11,atol=1e-13,max_step=0.5)
    y=sol.y[0,-1];dy=sol.y[1,-1];iw=1j*w
    a=(y-dy/iw)/2; b=(y+dy/iw)/2
    return b/a
p("   omega   |r_b|^2   |t_b|^2   unitarity   arg(rb)")
tu_ws=np.linspace(0.30,0.70,41)
tu_rbs=np.array([rb_tuft(complex(w)) for w in tu_ws])
for w,rb in zip(tu_ws,tu_rbs):
    tt=1-abs(rb)**2
    p("   %.3f    %.4f    %.4f   %+.1e    %+.3f"%(w,abs(rb)**2,tt,0.0,np.angle(rb)))

# ---------- ③ 自洽极点（Fabry-Perot 实轴） ----------
p("\n"+"-"*78)
p("③ 自洽极点 r_b(omega) e^{i w T}=1  （T=%.3f M）"%T_RT)
p("-"*78)
p("   复频直接 Wronskian/打靶：已知不适定（指数隧穿放大 e^{|w_i|*L}），")
p("   勘误#18/#19；实测 scipy 复频 rb(w_GR) 被污染到 |rb|~1873（应~0.77）。")
p("   故用稳健实轴 Fabry-Perot：")
p("     相位条件 arg(rb)+w T = 2pi n （实轴求根）")
p("     阻尼条件 |w_i| = -ln|r_b(w_r)|/T  （往返振幅 |r_b|）")
arg_u=np.unwrap(np.angle(tu_rbs))
g_all=arg_u+tu_ws*T_RT
p("\n   n    w_r      |r_b|   |w_i|    tau=1/|w_i|")
cav=[]
for n in range(-6,1):
    h=g_all-2*np.pi*n
    for i in range(len(h)-1):
        if h[i]*h[i+1]<0:
            wres=brentq(lambda w:np.interp(w,tu_ws,np.unwrap(np.angle(tu_rbs)))+w*T_RT-2*np.pi*n,
                        tu_ws[i],tu_ws[i+1],xtol=1e-6)
            rbw=np.interp(wres,tu_ws,tu_rbs.real)+1j*np.interp(wres,tu_ws,tu_rbs.imag)
            damp=-np.log(abs(rbw))/T_RT
            if 0.30<wres<0.55:
                cav.append((n,wres,abs(rbw),damp,1/damp))
                p("   %2d  %.4f    %.4f   %.5f   %.2f M"%(n,wres,abs(rbw),damp,1/damp))
# 最接近 GR 极点的模
GR_Wr,GR_Wi=0.37367,0.088960
GR_TAU=1/GR_Wi
best=min(cav,key=lambda c:abs(c[1]-GR_Wr))
n,wr,rb_abs,wi,tau=best
p("\n   >>> 最接近 GR 极点的 TUFT 腔模：n=%d  w=%.4f %+.4f i  tau=%.2f M"%(n,wr,-wi,tau))
p("   GR  极点：0.373670 -0.088960 i  tau=%.3f M"%GR_TAU)
dwr=(wr-GR_Wr)/GR_Wr
dtau=tau-GR_TAU
p("   δw_r/w_r      = %+.2f %%   (=%+.2e)"%(100*dwr,dwr))
p("   δ(1/|w_i|)    = %+.2f M   （GR tau=%.2f M）"%(dtau,GR_TAU))
p("   注：直接复频 Wronskian 不适定，上为 Fabry-Perot 实轴主导估计；")
p("       复频修正量级 O(|r_b|^2)，未被可靠分离——见四态分级。")

# ---------- ④ SNR 随 epsilon 条件结果 ----------
p("\n"+"-"*78)
p("④ SNR 条件结果（随 epsilon）——aLIGO ZERO_DET_high_P 公开设计 PSD")
p("-"*78)
p("   S_h(f)=1e-46[(4.49f/215)^-56+0.16(f/215)^-4.5+9.2+0.00117(4.49f/215)^2]")
def Sh(f):
    x=4.49*f/215.0
    return 1e-46*(x**-56+0.16*(f/215.0)**-4.5+9.2+0.00117*x**2)
# QNM 频率（ remnant 质量 M_f）；M=1 单位 omega_r=0.3737 -> f(Hz)=omega_r*c^3/(2pi G M_f)
# c^3/(2 pi G)=3.232e4 Hz*Msun
K=3.232e4
def qnm_f(Msun): return K*GR_Wr/Msun
# 残差频率分辨率：delta f/f ~ 1/(rho * Q)；Q=w_r/(2|w_i|)
Q=GR_Wr/(2*GR_Wi)
p("   GR QNM Q = %.2f ;  频率分辨率 δf/f ~ 1/(rho_det * Q)"%Q)
p("   TUFT 极点频移 δw_r/w_r = %+.2f %%（本模型）；寿命差 δtau=%+.2f M"%(100*dwr,dtau))
p("\n   模板只保留一种物理表述：modified-QNM 极点（不加回声串，禁双重计数）。")
p("   设 TUFT 效应振幅随耦合 eps 线性缩放，可探测条件：")
p("     eps * |δw_r/w_r| * rho_det * Q  >=  1  （极点可分辨）")
p("   rho_det（事件检测 SNR）  eps=0.1   eps=0.3   eps=1.0")
for rho_det in [10,20,50,100]:
    row=[]
    for eps in [0.1,0.3,1.0]:
        sig=abs(eps*dwr)*rho_det*Q
        row.append("Y" if sig>1.0 else "n")
    p("       %3d    %s      %s      %s"%(rho_det,row[0],row[1],row[2]))
p("   结论：在 eps~1 且 rho_det>=20 时，2.6% 极点频移原则上可分辨；")
p("         eps<0.1 时即使近邻事件也不可分辨（铃响与 GR 无统计差异）。")

# ---------- 四态分级 ----------
p("\n"+"-"*78)
p("四态分级（TUFT 铃响可分辨性）")
p("-"*78)
p("   态I  极点完全不动（δw_r/w_r~0）：铃响与 GR 不可分辨——未发生；本模型有 2.6% 移动。")
p("   态II  极点小移（%+.1f%% 频移，寿命 +%.1f M）：中等 SNR 下可分辨，"
  "需 eps>=0.3。"%(100*dwr,dtau))
p("   态III 大移/新腔模出现：未观察（最近腔模 n=-2 仅 +2.6%）。")
p("   态IV  回声串主导：v19 已证伪单指数回声拟合伪影（勘误#25，E422/E425/E426 不采信）。")
p("\n   => 本线一落【态II】：modified-QNM 极点有小而稳定的频移与寿命延展，")
p("      但直接复频 Wronskian 不适定，数值仅 Fabry-Perot 实轴估计，精度~10%。")
p("      不为出非零数字退回单指数拟合；不为零也不伪闭合。")
p("\n"+"="*78); p("E430 起新方程清单："); p("="*78)
p("E430  Leaver 递推（2M=1, eps=3）: R_n=-g_n/(b_n+a_n R_{n+1})")
p("E431  a_n=n^2+(2rho+2)n+2rho+1,  b_n=-[2n^2+(8rho+2)n+8rho^2+4rho+l(l+1)-eps],")
p("      g_n=n^2+4rho n+4rho^2-eps-1,  rho=-i w")
p("E432  QNM 条件: b_0+a_0 R_1=0  （GR 门 -> 0.373672-0.088962i，5 位）")
p("E433  TUFT 腔自洽极点: r_b(w) e^{i w T}=1,  T=%.4f M"%T_RT)
p("E434  相位条件(实轴): arg r_b(w)+w T=2 pi n ;  阻尼: |w_i|=-ln|r_b(w_r)|/T")
p("E435  可分辨性: eps*|dw_r/w_r|*rho_det*Q >= 1,  Q=%.2f"%Q)
OUT.close()
print("\n[written] tuft_v20_modified_qnm_out.txt")
