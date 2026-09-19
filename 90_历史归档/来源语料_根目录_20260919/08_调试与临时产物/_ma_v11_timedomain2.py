import numpy as np, time as _t, importlib.util
from scipy.optimize import curve_fit
spec=importlib.util.spec_from_file_location("td",r"D:\a10\aikjx\code\my_lib\_ma_v11_timedomain.py")
td=importlib.util.module_from_spec(spec); spec.loader.exec_module(td)

def fit_damped(t,y,t0,t1):
    m=(t>=t0)&(t<=t1); tt=t[m]; yy=y[m]
    def f(x,A,b,w,phi,c): return A*np.exp(b*x)*np.cos(w*x+phi)+c
    p0=[yy.max()*2,-0.097,0.48,0.0,0.0]
    try:
        popt,pcov=curve_fit(f,tt,yy,p0=p0,maxfev=40000)
        res=np.std(yy-f(tt,*popt))
        sig=np.sqrt(np.diag(pcov))
        return popt[2],popt[1],res,sig[2],sig[1]   # wR,wI,resid,sigwR,sigwI
    except Exception as e:
        return None

def run(l,win_list,rmin=-450.0,rmax=700.0,dx=0.02,tmax=500.0):
    dt=0.8*dx
    xs,r,rs=td.build_grid(rmin,rmax,dx); V=td.potential(xs,r,rs,l)
    t0=_t.time(); tt,sig=td.evolve(l,xs,V,dx,dt,tmax,sponge=80.0)
    print(f"\nl={l} N={len(xs)} dx={dx} dt={dt:.4f} evolve {_t.time()-t0:.1f}s")
    for a,b in win_list:
        o=fit_damped(tt,sig,a,b)
        if o: print(f"  win[{a},{b}] w = {o[0]:.7f} {o[1]:+.7f} i  resid={o[2]:.2e} sig(wR)={o[3]:.1e}")

if __name__=="__main__":
    # 门禁：l=2 须命中 0.4836439 -0.0967588
    run(2,[(105,200),(120,230),(140,260),(160,300),(120,300)])
