"""
MainAgent v11 第三种独立方法：时域演化（time-domain ringdown）
与 Leaver 连分数、频率域打靶都无关。
  d2psi/dt2 - d2psi/dr*2 + V_l(r) psi = 0,  V=f*(l(l+1)/r^2 + 2/r^3), M=1
- 均匀 r* 网格，4 阶中心差分（空间误差 O(dx^4)），蛙跳时间积分
- 两端 cos² 海绵层吸收（无硬边界反射），中期提取窗内无回波
- 高斯波包初始；探测点记录 psi(t)
- 晚期 ringdown 取解析信号(FFT-Hilbert)，ln|z| 斜率给 -Im(w)、解卷绕相位斜率给 Re(w)
  对多个时间窗给结果 -> 选稳定平台。门禁：l=2 必须命中 0.483644-0.096759。
"""
import numpy as np

def build_grid(rstar_min=-150.0, rstar_max=450.0, dx=0.025):
    xs=np.arange(rstar_min,rstar_max+0.5*dx,dx)
    # r 网格 -> r*=r+2 ln(r/2-1)，单调；V 在 r 上算后 np.interp 到 xs
    r=np.linspace(2.0+1e-7, 400.0, 200_001)
    rs=r+2.0*np.log(r/2.0-1.0)
    return xs, r, rs

def potential(xs, r, rs, l):
    f=1.0-2.0/r
    V=f*(l*(l+1)/r**2 + 2.0/r**3)
    return np.interp(xs, rs, V)

def evolve(l, xs, V, dx, dt, tmax, rc=25.0, sig=4.0, xdet=40.0,
           sponge=60.0, gamma0=2.0):
    n=len(xs)
    # 海绵
    g=np.zeros(n)
    mL=xs<(xs[0]+sponge); mR=xs>(xs[-1]-sponge)
    g[mL]=gamma0*np.cos((xs[mL]-xs[0])/sponge*np.pi/2)**2
    g[mR]=gamma0*np.cos((xs[-1]-xs[mR])/sponge*np.pi/2)**2
    c2=(dt/dx)**2
    # 初值：高斯包，psi_t=0（用前两个半步一致初始化）
    psi=np.exp(-0.5*((xs-rc)/sig)**2)
    Lp=lap4(psi,dx,V)
    psi_m=psi-0.5*dt**2*Lp          # t=-dt 由 psi_tt=Lpsi、psi_t=0
    psi_p=np.empty_like(psi)
    idet=np.argmin(abs(xs-xdet))
    nsteps=int(tmax/dt)
    rec=np.empty(nsteps+1); rec[0]=psi[idet]
    t=np.empty(nsteps+1); t[0]=0.0
    pcur=psi; pprev=psi_m
    for k in range(1,nsteps+1):
        Lp=lap4(pcur,dx,V)
        # 含阻尼蛙跳：p^{+}=2p-p^- +dt2 Lp - 2 dt g (p-p^-)
        psi_p=2*pcur-pprev+dt**2*Lp-2*dt*g*(pcur-pprev)
        pprev,pcur=pcur,psi_p
        rec[k]=pcur[idet]; t[k]=k*dt
    return t,rec

def lap4(p,dx,V):
    out=np.empty_like(p)
    out[2:-2]=(-p[:-4]+16*p[1:-3]-30*p[2:-2]+16*p[3:-1]-p[4:])/(12*dx**2)-V[2:-2]*p[2:-2]
    out[:2]=out[2]; out[-2:]=out[-3]
    return out

def analytic(z):  # FFT Hilbert
    n=len(z); Z=np.fft.fft(z); h=np.zeros(n); h[0]=1
    if n%2==0: h[1:n//2]=2; h[n//2]=1
    else: h[1:(n+1)//2]=2
    return np.fft.ifft(Z*h)

def extract(t,sig,t0,t1):
    m=(t>=t0)&(t<=t1)
    zz=analytic(sig)[m]; tt=t[m]
    amp=np.log(np.abs(zz)+1e-300); ph=np.unwrap(np.angle(zz))
    # ln z = a - i w t ;  Im: amp = a + Im(w) t (w_I<0) ; phase = -Re(w) t
    ba=np.polyfit(tt,amp,1); bp=np.polyfit(tt,ph,1)
    wI=ba[0]; wR=-bp[0]
    # 拟合残差
    resid=np.std(amp-(ba[1]+ba[0]*tt))+np.std(ph-(bp[1]+bp[0]*tt))
    return wR,wI,resid

if __name__=="__main__":
    import time as _t
    dx=0.025; dt=0.02; tmax=400.0
    xs,r,rs=build_grid(dx=dx)
    canon={2:(0.4836439,-0.0967588),1:(0.2929363,-0.0976600),0:(0.1104557,-0.1048957)}
    windows={2:[(90,200),(110,240),(130,280),(150,320)],
             1:[(110,240),(140,300),(170,340)],
             0:[(150,300),(180,340),(210,370),(240,390)]}
    print(f"time-domain scalar ringdown  dx={dx} dt={dt} tmax={tmax} Ngrid={len(xs)}")
    for l in (2,1,0):
        t0=_t.time(); V=potential(xs,r,rs,l)
        tt,sig=evolve(l,xs,V,dx,dt,tmax)
        print(f"\nl={l}  (evolve {_t.time()-t0:.1f}s)  canon {canon[l][0]:.7f} {canon[l][1]:.7f}i")
        for a,b in windows[l]:
            wR,wI,res=extract(tt,sig,a,b)
            print(f"  win[{a:3d},{b:3d}]  w = {wR:.7f} {wI:+.7f} i   fitresid={res:.2e}")
