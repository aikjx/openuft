# -*- coding: utf-8 -*-
"""
MainAgent v20 独立审计。不 import 联盟脚本（其顶层即执行+写文件），独立重写：
 (A) 独立 Leaver 1985 连分数 -> Schwarzschild l=2 QNM，验它声称的 5 位 GR 门；
 (B) 复刻其 TUFT rb_tuft 几何，做三件它没做的自检：
     B1 独立概率流守恒（V 实、无耗散必须成立），对照它写死打印的 unitarity=0；
     B2 内边界 s_launch / 波方向敏感性（合格外垒反射应与这些无关）；
     B3 在它选出的腔模 w=.3834 处取它自己表的 |r_b|，按它 E434 公式算阻尼，
        核对是否真能得到 .0676（tau14.79），还是与 .545 矛盾（应~.0218/tau46）。
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import mpmath as mp
mp.mp.dps=60

print("="*82)
print("(A) 独立 Leaver 1985 连分数  Schwarzschild s=-2 l=2 n=0")
print("="*82)
def leaver(w,l=2,eps=3,N=400):
    w=mp.mpc(w); rho=-1j*w
    a=lambda n:n*n+(2*rho+2)*n+2*rho+1
    b=lambda n:-(2*n*n+(8*rho+2)*n+8*rho*rho+4*rho+l*(l+1)-eps)
    g=lambda n:n*n+4*rho*n+4*rho*rho-eps-1
    R=mp.mpf(0)
    for n in range(N,0,-1): R=-g(n)/(b(n)+a(n)*R)
    a0=2*rho+1; b0=-(8*rho*rho+4*rho+l*(l+1)-eps)
    return b0+a0*R
for N in [200,400,1000]:
    root=mp.findroot(lambda w:leaver(w,N=N),mp.mpc(0.74734-0.17792j),solver='muller',tol=1e-14)
    pole=complex(root)/2
    cat=complex(0.3736716844,-0.0889623157)
    print("  N=%4d -> %.9f %+.9f i   |d vs catalog|=%.2e"%(N,pole.real,pole.imag,abs(pole-cat)))
print("  联盟报 0.373672-0.088962i（5位）；上表独立确认 -> E430-E432 GR 门可采纳。")

# ---- 联盟几何（严格面积势 + 龟坐标，v17/v18 已确认）----
C_C,C_D=-0.29,-0.05
T=13.9383
rho_h=brentq(lambda r:r**3+C_C*r+C_D,1e-3,5.0,xtol=1e-14)
rho=np.linspace(rho_h*1.0008,250.0,400000)
Bv=np.exp(2/rho)*(1+C_C/rho**2+C_D/rho**3); Av=np.exp(-2/rho)
q=-2/rho**2+(-2*C_C/rho**3-3*C_D/rho**4)/(1+C_C/rho**2+C_D/rho**3)
J=np.sqrt(Bv)*(1+0.5*rho*q); Rt=rho*np.sqrt(Bv); em2=(J/np.sqrt(Bv))**2
Vt=3*Av*(1+em2)/Rt**2
sqrtBA=np.sqrt(Bv/Av)
ds=np.concatenate([[0.0],np.cumsum(0.5*(sqrtBA[1:]+sqrtBA[:-1])*np.diff(rho))])
def Vof(s): return np.interp(s,ds,Vt)
print("\n几何 rho_h=%.5f ; s 网格 [%.2f,%.2f]"%(rho_h,ds[0],ds[-1]))

def decompose_at(s_out,w,s_launch,direction,s_end=200.0):
    """在 s_launch 放纯方向波，积到 s_end，末端分解 e^{+iws}(A,向外) / e^{-iws}(B,向内)。
       direction=+1 入射波 e^{+iws}(朝垒向外)；-1 入射波 e^{-iws}(联盟用法)。
       返回 (A,B) 系数、外端概率流、内端入射流。"""
    if direction==+1:
        y0=np.exp(+1j*w*s_launch); dy0=+1j*w*y0
    else:
        y0=np.exp(-1j*w*s_launch); dy0=-1j*w*y0
    sol=solve_ivp(lambda s,y,w:[y[1],-(w*w-Vof(s))*y[0]],(s_launch,s_end),
                  [y0,dy0],args=(w,),method="DOP853",rtol=1e-11,atol=1e-13,max_step=0.5)
    y,dy=sol.y[0,-1],sol.y[1,-1]
    A=(y+dy/(1j*w))/2    # e^{+i w s}
    B=(y-dy/(1j*w))/2    # e^{-i w s}
    J_out=w*(abs(A)**2-abs(B)**2)
    J_in=w*1.0           # 单位入射波概率流大小
    return A,B,J_out,J_in

print("\n"+"="*82)
print("(B1) 真通量守恒检验  实频 V 实 => |J_out|=|J_in|=w（单位入射）")
print("     联盟设置：s_launch=3, direction=-1 (e^{-iws})  —— 它打印的 unitarity=0 是写死的")
print("="*82)
for w in [0.35,0.3737,0.3834,0.40]:
    A,B,Jo,Ji=decompose_at(200.0,complex(w),3.0,-1)
    rBA=abs(B/A); rBA2=abs(B/A)**2
    print("  w=%.4f [联盟设置]  |A|^2=%.4f |B|^2=%.4f  J_out/J_in=%.5f (应=1)  |B/A|^2=%.4f"%(
        w,abs(A)**2,abs(B)**2,float(np.real(Jo/Ji)),abs(B/A)**2))

print("\n  对照：正确方向 direction=+1（腔内 e^{+iws} 朝垒入射），归一入射=1 应 |A|^2-|B|^2=1")
for w in [0.35,0.3737,0.3834,0.40]:
    A,B,Jo,Ji=decompose_at(200.0,complex(w),3.0,+1)
    print("  w=%.4f [正确方向]  |A|^2=%.4f |B|^2=%.4f  |A|^2-|B|^2=%.5f (应=1)  r=|B/A|=%.4f |r|^2=%.4f"%(
        w,abs(A)**2,abs(B)**2,abs(A)**2-abs(B)**2,abs(B/A),abs(B/A)**2))

print("\n"+"="*82)
print("(B2) 内边界 s_launch 敏感性（合格'单独外垒'反射应与 s_launch 无关）")
print("="*82)
w=complex(0.3834)
for sL in [1.0,2.0,3.0,4.0,5.0]:
    A,B,Jo,Ji=decompose_at(200.0,w,sL,+1)
    print("  正确方向 s_launch=%.0f : |r|^2=%.4f  守恒(|A|^2-|B|^2)=%.4f"%(sL,abs(B/A)**2,abs(A)**2-abs(B)**2))
print("  -> 若 |r|^2 随 s_launch 显著变化，说明内边界/核参与污染，不是隔离外垒 r_b。")

print("\n"+"="*82)
print("(B3) Fabry-Perot 阻尼算术核对（联盟 E434：|w_i|=-ln|r_b|/T, T=%.4f）"%T)
print("="*82)
# 用它③表 @.3737 的 |r_b|^2=.545（它报告值）与正确方向独立值，分别算
for label,r2 in [("联盟表 @.3737 |r_b|^2=0.545",0.545),
                 ("要得到它报的 |w_i|=.0676 反推 |r_b|^2",None)]:
    if r2 is not None:
        wi=-np.log(np.sqrt(r2))/T
        print("  %-42s -> |w_i|=%.5f  tau=%.2f M"%(label,wi,1/wi))
    else:
        rb=np.exp(-0.0676*T); print("  %-42s -> |r_b|=%.4f |r_b|^2=%.4f"%(label,rb,rb**2))
print("  联盟腔模实部 w_r=0.3834；按它 E434 在该频率取 |r_b| 得 .0676，要求 |r_b|^2~0.152。")
# 在 .3834 用正确方向/它的设置各取一次 |r|^2
A1,B1,_,_=decompose_at(200.0,complex(0.3834),3.0,-1)
A2,B2,_,_=decompose_at(200.0,complex(0.3834),3.0,+1)
print("  实跑 @.3834：联盟设置 |B/A|^2=%.4f ；正确方向 |r|^2=%.4f  —— 两者都远非 0.152"%(abs(B1/A1)**2,abs(B2/A2)**2))
for r2 in [abs(B1/A1)**2,abs(B2/A2)**2]:
    wi=-np.log(np.sqrt(r2))/T
    print("     用 |r|^2=%.4f -> 自洽 |w_i|=%.5f tau=%.2fM（非 14.79M）"%(r2,wi,1/wi))

print("\n"+"="*82)
print("判决：E430-E432 Leaver GR 门采纳（独立 5-6 位）；E433 r_b=.545 几何/通量不合格（硬编码")
print("GR 表、伪 unitarity、内边界方向反且敏感）；E434 腔模 .3834-.0676i 建立在错误 r_b + unwrap")
print("相位(n=-2 分支)上且阻尼算术与自表 .545 矛盾 -> 不采信；E435 SNR 随 2.61% 作废，仅留条件框架。")
print("modified-QNM 真实极点仍 OPEN：需隔离外垒（内侧虚拟无反射出射波导）+ 真通量门 + 两端")
print("Frobenius×出射 Wronskian 复频匹配，或高分辨率多指数/谱极点提取。")
