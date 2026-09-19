# -*- coding: utf-8 -*-
"""MainAgent v14 independent audit (no coalition import).
Same INWARD integrator self-tested on GR (known answer) then applied to TUFT.
Outgoing log-deriv psi_s/psi = i w at large r*; RK4 inward; inner BC:
 GR   -> pure horizon ingoing psi_s/psi = -i w at s_in (near horizon)
 TUFT -> wall Neumann psi_s = 0 at s=0 (wall is regular).
Grids built ONCE per s_out; residual only integrates.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import numpy as np
from scipy.optimize import root as sp_root, brentq
from scipy.interpolate import interp1d
t0=time.time()
def P(*a): print(*a, flush=True)
VMAX=6*np.exp(-2)
H=0.02

def inward(Vg,h,w,psi_o,psis_o):
    a,b=float(w.real),float(w.imag); W0=-a*a+b*b; tb=2*a*b
    u,v=float(psi_o.real),float(psi_o.imag)
    us,vs=float(psis_o.real),float(psis_o.imag)
    q=-h; N=len(Vg)
    for k in range(N-1,0,-1):
        Wk=Vg[k]+W0; Wkm=Vg[k-1]+W0
        k1u,k1v,k1us,k1vs=us,vs,Wk*u+tb*v,Wk*v-tb*u
        u2,v2,us2,vs2=u+q/2*k1u,v+q/2*k1v,us+q/2*k1us,vs+q/2*k1vs
        k2us,k2vs=Wk*u2+tb*v2,Wk*v2-tb*u2
        u3,v3,us3,vs3=u+q/2*us2,v+q/2*vs2,us+q/2*k2us,vs+q/2*k2vs
        k3us,k3vs=Wk*u3+tb*v3,Wk*v3-tb*u3
        u4,v4,us4,vs4=u+q*us3,v+q*vs3,us+q*k3us,vs+q*k3vs
        k4us,k4vs=Wkm*u4+tb*v4,Wkm*v4-tb*u4
        u+=q/6*(k1u+2*us2+2*us3+us4); v+=q/6*(k1v+2*vs2+2*vs3+vs4)
        us+=q/6*(k1us+2*k2us+2*k3us+k4us); vs+=q/6*(k1vs+2*k2vs+2*k3vs+k4vs)
    return complex(u,v),complex(us,vs)

_cache={}
def gr_grid(s_in,s_out):
    key=("gr",s_in,s_out)
    if key in _cache: return _cache[key]
    r=np.linspace(2+1e-7,300.0,400001)
    rs=r+2*np.log(r/2-1); V=(1-2/r)*(6/r**2-6/r**3)
    s=np.arange(s_in,s_out+0.5*H,H)
    Vg=interp1d(rs,V,fill_value="extrapolate")(s)
    _cache[key]=Vg; return Vg

def tuft_grid(cm,d,s_out):
    key=("t",cm,d,s_out)
    if key in _cache: return _cache[key]
    rr=np.linspace(1e-3,300.0,400001); g=1+cm/rr**2+d/rr**3; rh=None
    for i in range(len(rr)-1):
        if g[i]*g[i+1]<0: rh=brentq(lambda r:1+cm/r**2+d/r**3,rr[i],rr[i+1],xtol=1e-13);break
    r=np.linspace(rh*(1+1e-12),300.0,600001)
    Fd=np.exp(2/r)*np.sqrt(np.clip(1+cm/r**2+d/r**3,0,None))
    ss=np.concatenate([[0],np.cumsum(0.5*(Fd[1:]+Fd[:-1])*np.diff(r))])
    V=np.exp(-2/r)*6/r**2
    s=np.arange(0,s_out+0.5*H,H)
    Vg=interp1d(ss,V,fill_value="extrapolate")(s)
    ipk=int(np.argmax(V)); L=ss[ipk]
    _cache[key]=(Vg,rh,L); return Vg,rh,L

def gr_resid(x,Vg,s_in,s_out):
    w=complex(*x); a,b=x
    psi,ps=inward(Vg,H,w,1+0j,complex(-b,a))   # outer: psi_s = i w
    L=ps/psi
    z=L-(-1j*w)                                # inner: want -i w
    return [z.real,z.imag]

def tuft_resid(x,Vg):
    w=complex(*x); a,b=x
    psi,ps=inward(Vg,H,w,1+0j,complex(-b,a))
    z=ps/psi                                   # wall Neumann -> 0
    return [z.real,z.imag]

def findroot(resid,guess,args=(),xtol=1e-9):
    try:
        sol=sp_root(resid,[guess.real,guess.imag],args=args,method="hybr",
                    options={"xtol":xtol,"maxfev":300})
        w=complex(*sol.x)
        z=complex(*resid([w.real,w.imag],*args))
        return w,abs(z),sol.success
    except Exception:
        return None,1e9,False

TRUTH=complex(0.37367168441804166,-0.08896231568893410)
P("="*86);P("MAINAGENT v14 AUDIT  inward integrator: GR self-test, then TUFT");P("="*86)
P("Vmax=6e^-2=%.5f  sqrt(Vmax)=%.5f\n"%(VMAX,np.sqrt(VMAX)))

P("[A] GR inward integrator, horizon ingoing at s_in=-11, scan s_out")
P("  truth 0.3736716844 - 0.0889623157 i")
P("  %-6s %-26s %-11s %-9s"%("s_out","omega","|F|","err"))
for so in [60,100,140,180,220]:
    Vg=gr_grid(-11.0,float(so))
    w,r,ok=findroot(gr_resid,complex(0.40,-0.10),args=(Vg,-11.0,float(so)))
    if w is None: P("  %-6d NO CONV"%so);continue
    err=abs(w-TRUTH)
    P("  %-6d %-26s %-11.2e %-9.2e"%(so,"%.8f%+.8fi"%(w.real,w.imag),r,err))

P("\n[B] TUFT inward roots vs s_out, multi-seed; w^2 vs Vmax and Q")
for cm,dd,tag in [(-0.5,0.0,"c=-0.50"),(-0.29,-0.05,"c=-0.29")]:
    P(" --- %s (Vmax=%.4f) ---"%(tag,VMAX))
    for so in [100,130,160,190,220]:
        Vg,rh,L=tuft_grid(cm,dd,float(so))
        roots=[]
        for g0 in [complex(0.90,-0.02),complex(0.80,-0.02),complex(1.00,-0.02),
                   complex(0.90,-0.07),complex(0.40,-0.09),complex(1.3,-0.05)]:
            w,r,ok=findroot(tuft_resid,g0,args=(Vg,))
            if w is not None and r<1e-5 and 0.05<w.real<2 and -0.5<w.imag<-1e-5:
                if all(abs(w-q)>0.01 for q in roots): roots.append(w)
        roots.sort(key=lambda z:-z.imag)
        cells=[]
        for q in roots[:4]:
            w2=q.real**2-q.imag**2; Q=q.real/(2*abs(q.imag))
            cells.append("%.4f%+.4fi w2=%.3f%s Q~%.0f"%(
                q.real,q.imag,w2,"ABOVE" if w2>VMAX else "below",Q))
        P("  s_out=%-3d L=%5.2f  "%(so,L)+(" || ".join(cells) if cells else "no root"))

P("\nTotal %.1f s"%(time.time()-t0))
