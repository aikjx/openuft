# -*- coding: utf-8 -*-
# 修正诊断：正确 Lorentzian 谱；均匀 vs 加权 tail 份额；并精确复现 v17_audit(D)
import numpy as np
from scipy.integrate import quad, trapezoid
GM=4.9256e-6; Msec=60*GM
wR,wI=0.3736716844,0.0889623157
wb=0.702
w=np.linspace(1e-4,4.0,4_000_001)
S=1.0/((w-wR)**2+wI**2)                 # 修正：一行赋值
f=w/(2*np.pi*Msec)
Sn=1e-46*((100/f)**4+2+(f/200)**2)
tail=w>=wb
def frac(g):
    lo=np.trapezoid(S[~tail]*g[~tail],w[~tail]); hi=np.trapezoid(S[tail]*g[tail],w[tail])
    return hi/(lo+hi)
print("[w-grid] uniform tail =",round(frac(np.ones_like(w)),4),
      " weighted 1/Sn tail =",round(frac(1/Sn),4))

# 精确复现 v17_audit(D)：f 网格 + 复谱 hRD（与联盟同构造）
f2=np.linspace(30.0,2000.0,200000)
h0=5e-22; tau=11.24*Msec
f_RD=wR/(2*np.pi*Msec)
h=h0/((1/tau)+1j*2*np.pi*(f2-f_RD))
Sn2=1e-46*((100/f2)**4+2+(f2/200)**2)
win=2*np.pi*f2*Msec
T4=np.where(win>=wb,1.0,0.0)
rRD=4*np.trapezoid(np.abs(h)**2/Sn2,f2)
rEC=4*np.trapezoid((T4*np.abs(h))**2/Sn2,f2)
print("[f-grid exact D] weighted echo/RD =",round(float(np.sqrt(rEC/rRD)),4))
# 均匀版（去 Sn）
uRD=np.trapezoid(np.abs(h)**2,f2); uEC=np.trapezoid((T4*np.abs(h))**2,f2)
print("[f-grid uniform ] echo/RD =",round(float(np.sqrt(uEC/uRD)),4))
# 解析核对（quad，单边 0..50）
num=quad(lambda x:1/((x-wR)**2+wI**2),wb,50)[0]
den=quad(lambda x:1/((x-wR)**2+wI**2),0,50)[0]
print("[quad analytic uniform] =",round(num/den,4))
