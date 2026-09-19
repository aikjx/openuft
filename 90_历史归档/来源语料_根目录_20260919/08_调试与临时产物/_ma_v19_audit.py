# -*- coding: utf-8 -*-
"""
MainAgent v19 独立审计：复现联盟 tuft_v19_waveform_distortion.py 并判决 E422 伪极点。
不引用联盟数值结论，只复刻其构造，独立检验三件事：
 (1) 复现它报告的 w_TU=0.3835 / tau_TU=10.17（确认我跑通它的逻辑）；
 (2) r_echo=.211 是否为冗余中间量（被 h_GR(t-nT) 的 e^{+nT/tau} 抵消，净公比=.729）；
 (3) 单指数 curve_fit 多回声瞬态串 => 拟合“极点”随窗口漂移（非稳健），
     而在所有回声都已启动后的稳态晚窗口，拟合必回 w_GR/tau_GR（真实极点不动）。
"""
import numpy as np
from scipy.optimize import curve_fit

wr, wi = 0.37367, 0.08896
tau = 1.0/wi
T = 13.9390
R2 = 0.5314
Rbarr = np.sqrt(R2)
echo_frac = np.exp(-T/tau)
r_echo = Rbarr*echo_frac

print("="*80)
print("v19 audit  w_GR=%.5f-%.5fi tau_GR=%.4f  T=2L=%.4f  T/tau=%.4f"%(wr,wi,tau,T,T/tau))
print("Rbarr=sqrt(.5314)=%.5f ; e^{-T/tau}=%.5f ; r_echo(claimed)=%.5f"%(Rbarr,echo_frac,r_echo))

# ---- (2) 公比抵消检验 ----
print("\n[2] 第 n 回声真实权重 = r_echo^n * e^{nT/tau}（h_GR(t-nT) 自带的增长）")
for n in range(5):
    w_claimed = r_echo**n
    w_actual  = r_echo**n * np.exp(n*T/tau)
    print("  n=%d  r_echo^n=%.5f   x e^{nT/tau}=%.5f   Rbarr^n=%.5f"%(
        n, w_claimed, w_actual, Rbarr**n))
print("  => r_echo^n e^{nT/tau} = (Rbarr e^{-T/tau})^n e^{nT/tau} = Rbarr^n ；.289 精确抵消。")
print("     波形真实公比 = Rbarr = %.4f（仍含吸收视界，双侧 r_b 未做 => OPEN）。"%Rbarr)

# ---- 构造回声串（与联盟完全相同）----
t = np.linspace(0.0, 12.0*tau, 20000)
def hGR(tt): return np.exp(-tt/tau)*np.cos(wr*tt)*(tt>=0)
N_echo=6
htu = np.zeros_like(t)
for n in range(N_echo+1):
    htu += r_echo**n * hGR(t-n*T)

def model(tt,A,tauT,wT,phi): return A*np.exp(-tt/tauT)*np.cos(wT*tt+phi)
def fit_window(a,b):
    m=(t>a*tau)&(t<b*tau)
    tt,hh=t[m],htu[m]
    try:
        p,_=curve_fit(model,tt,hh,p0=[np.max(np.abs(hh)),tau,wr,0.0],maxfev=40000)
        return abs(p[2]),abs(p[1])
    except Exception as e:
        return np.nan,np.nan

# ---- (1) 复现联盟窗口 ----
wF,tauF = fit_window(2.5,8.0)
print("\n[1] 复现联盟窗口 [2.5tau,8tau]:  w_fit=%.5f (delta %+.2f%%)  tau_fit=%.3f (delta %+.2f%%)"%(
    wF,100*(wF-wr)/wr, tauF,100*(tauF-tau)/tau))
print("    联盟报告 w=0.38354(+2.64%%) tau=10.170(-9.53%%)；复刻一致即说明其数字来自此拟合。")

# ---- (3a) 窗口漂移：伪极点不稳健 ----
print("\n[3a] 扫描单指数拟合窗口 => 所谓极点随窗口大幅漂移（拍频瞬态伪影）")
print("%18s %10s %10s %10s %10s"%("window/tau","w_fit","dw%","tau_fit","dtau%"))
for (a,b) in [(1.5,5),(2.0,6),(2.5,8),(3.0,9),(4.0,10),(5.0,11),(6.0,12)]:
    wF,tauF=fit_window(a,b)
    print("%18s %10.5f %+9.2f%% %10.3f %+9.2f%%"%(
        "[%.1f,%.1f]"%(a,b),wF,100*(wF-wr)/wr,tauF,100*(tauF-tau)/tau))

# ---- (3b) 稳态晚窗口：所有回声(n=0..6, 最晚 6T=83.6M=7.44tau)启动后 ----
print("\n[3b] 稳态窗口 t>6T=%.1fM=%.2ftau（7 条回声全部已启动）拟合："%(6*T,6*T/tau))
for (a,b) in [(7.5,12),(8.0,12),(8.5,12),(9.0,12)]:
    wF,tauF=fit_window(a,b)
    print("   [%.1f,%.1f]tau  w_fit=%.5f (dw %+.2f%%)  tau_fit=%.3f (dtau %+.2f%%)"%(
        a,b,wF,100*(wF-wr)/wr,tauF,100*(tauF-tau)/tau))
print("   => 稳态晚窗拟合回到 w_GR/tau_GR：回声串只改复留数，真实复极点不动。")

# ---- (3c) 解析稳态：去衰减后信号趋于纯 w_GR 振荡（复常数 C）----
g = htu*np.exp(t/tau)
late = t>7.5*tau
gl = g[late]
# 拟合纯余弦 B cos(w t+phi)（无衰减）
def pure(tt,B,wT,phi): return B*np.cos(wT*tt+phi)
try:
    p,_=curve_fit(pure,t[late],gl,p0=[1.0,wr,0.0],maxfev=40000)
    print("\n[3c] 去 GR 包络后晚窗纯振荡频率 = %.6f（w_GR=%.6f，偏差 %.2e）"%(p[1],wr,abs(p[1]-wr)/wr))
except Exception as e:
    print("pure fit fail",e)
# 理论稳态复留数
C=sum((r_echo*np.exp(T/tau))**n * np.exp(-1j*wr*n*T) for n in range(N_echo+1))
print("     理论稳态复因子 |C|=%.4f arg=%.3f rad（与 t 无关 => 单一指数 w_GR）"%(abs(C),np.angle(C)))

print("\n[判决] E422 的 +2.64%%/-9.53%% 是【瞬态多回声串强拟合单指数】的窗口伪影，")
print("       非复极点移动；且反射腔物理应使 tau 增大（挡回能量），它报 tau 减小，方向亦反。")
print("       真极点偏移需双侧出射 r_b(w) + 自洽 D0(w)=a e^{iwT}（Leaver/时域），本脚本未做 => OPEN。")
