# -*- coding: utf-8 -*-
"""
MA v15 gate experiment 2: localize the error source of the two-endpoint
log-derivative shooting. Far field already plateaus (s_out 60->180 unchanged),
so scan the HORIZON endpoint depth s_in: the bare -iw ingoing condition ignores
the regular inner Frobenius-series slope. If omega -> truth as s_in -> -inf,
that proves a full inner Frobenius series (not high precision / not a deeper
box) is mandatory. Fixed s_out=150.
"""
import sys, io, time
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import mpmath as mp
mp.mp.dps=45
I=mp.mpc(0,1); t0=time.time()
def P(*a): print(*a,flush=True)

SG_MIN=mp.mpf(-21); S_MAX=mp.mpf(150); H=mp.mpf("0.05")
n=int(mp.floor((S_MAX-SG_MIN)/H))
NR=400001
rlo=mp.mpf(2)+mp.mpf("1e-9"); rhi=mp.mpf(170)
rr=[rlo+(rhi-rlo)*k/NR for k in range(NR+1)]
ss=[r+2*mp.log(r/2-1) for r in rr]
s=[SG_MIN+H*k for k in range(n+1)]
V=[];j=0
for sk in s:
    while j+1<len(ss) and ss[j+1]<sk: j+=1
    rk=rr[j]+(sk-ss[j])*(rr[j+1]-rr[j])/(ss[j+1]-ss[j])
    f=1-2/rk; V.append(f*(6/rk**2-6/rk**3))
def idxof(x): return int(mp.floor((mp.mpf(x)-SG_MIN)/H))
iout=idxof(150); sout=s[iout]
P("grid N=%d ready %.1fs; fixed s_out=150"%(n+1,time.time()-t0))

def shoot(win,z,Lin,Lout):
    a,b=z.real,z.imag; W0=-a*a+b*b; tb=2*a*b; q=-H
    u,v,us,vs=mp.mpf(1),mp.mpf(0),Lout.real,Lout.imag
    for k in range(iout,win,-1):
        def d(U,Vk):
            x,y,xs,ys=U; return(xs,ys,(Vk+W0)*x+tb*y,(Vk+W0)*y-tb*x)
        U=(u,v,us,vs)
        k1=d(U,V[k]); U2=tuple(U[j]+q/2*k1[j] for j in range(4)); k2=d(U2,V[k])
        U3=tuple(U[j]+q/2*k2[j] for j in range(4)); k3=d(U3,V[k])
        U4=tuple(U[j]+q*k3[j] for j in range(4)); k4=d(U4,V[k-1])
        u,v,us,vs=(U[j]+q/6*(k1[j]+2*k2[j]+2*k3[j]+k4[j]) for j in range(4))
    return mp.mpc(u,v),mp.mpc(us,vs)

TRUTH=mp.mpc("0.37367168441804166","-0.08896231568893410")
P("truth %.15f %+.15f i\n"%(TRUTH.real,TRUTH.imag))
P("  %-7s %-12s %-30s %-9s %s"%("s_in","delta=r-2","omega","err","dig"))
guess=mp.mpc("0.40","-0.10")
for sin in [-8,-12,-16,-20]:
    win=idxof(sin)
    def F(z):
        Lout=I*z-3*I/(z*sout**2)
        psi,psis=shoot(win,z,None,Lout)
        return psis/psi-(-I*z)
    try:
        w=mp.findroot(F,guess,tol=mp.mpf("1e-25")); r=abs(F(w))
        err=abs(w-TRUTH); dig=max(0,int(-mp.floor(mp.log10(err))))
        # delta=r-2 at s_in: r*=r+2 ln(delta/2) ~ 2+2ln(delta/2) -> delta=2 exp((s-2)/2)
        delta=2*mp.exp((mp.mpf(sin)-2)/2)
        P("  %-7d %-12.2e %-30s %-9.2e %d  (|F|=%.1e)"%(sin,float(delta),
          "%.12f %+.12f i"%(w.real,w.imag),float(err),dig,float(r)))
        guess=w
    except Exception as e:
        P("  %-7d FAIL %s"%(sin,repr(e)[:60]))
P("\nTotal %.1fs"%(time.time()-t0))
