# -*- coding: utf-8 -*-
"""
MA v15 gate experiment 3 (decisive for ill-posedness): SAME grid, SAME
s_in=-8, SAME s_out=150, SAME 45-digit precision, vary ONLY the Newton seed.
If different seeds land on different deep roots (all |F|~1e-40) and none is
0.373672-0.088962, the two-endpoint single-branch shooting F(w) has many
spurious zeros: sub-barrier exponential mixing makes it ill-posed regardless
of precision -> two-sided SERIES matching that never integrates a single
branch through the barrier is mandatory.
"""
import sys,io,time
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import mpmath as mp
mp.mp.dps=45
I=mp.mpc(0,1);t0=time.time()
def P(*a):print(*a,flush=True)
SIN=mp.mpf(-8); SOUTv=mp.mpf(150); H=mp.mpf("0.05")
n=int(mp.floor((SOUTv-SIN)/H))
NR=400001;rlo=mp.mpf(2)+mp.mpf("1e-9");rhi=mp.mpf(170)
rr=[rlo+(rhi-rlo)*k/NR for k in range(NR+1)]
ss=[r+2*mp.log(r/2-1) for r in rr]
s=[SIN+H*k for k in range(n+1)]
V=[];j=0
for sk in s:
    while j+1<len(ss) and ss[j+1]<sk:j+=1
    rk=rr[j]+(sk-ss[j])*(rr[j+1]-rr[j])/(ss[j+1]-ss[j]);f=1-2/rk
    V.append(f*(6/rk**2-6/rk**3))
P("grid N=%d ready %.1fs"%(n+1,time.time()-t0))
def shoot(z):
    a,b=z.real,z.imag;W0=-a*a+b*b;tb=2*a*b;q=-H
    Lout=I*z-3*I/(z*SOUTv**2)
    u,v,us,vs=mp.mpf(1),mp.mpf(0),Lout.real,Lout.imag
    for k in range(n,0,-1):
        def d(U,Vk):
            x,y,xs,ys=U;return(xs,ys,(Vk+W0)*x+tb*y,(Vk+W0)*y-tb*x)
        U=(u,v,us,vs)
        k1=d(U,V[k]);U2=tuple(U[j]+q/2*k1[j] for j in range(4));k2=d(U2,V[k])
        U3=tuple(U[j]+q/2*k2[j] for j in range(4));k3=d(U3,V[k])
        U4=tuple(U[j]+q*k3[j] for j in range(4));k4=d(U4,V[k-1])
        u,v,us,vs=(U[j]+q/6*(k1[j]+2*k2[j]+2*k3[j]+k4[j]) for j in range(4))
    return mp.mpc(u,v),mp.mpc(us,vs)
def F(z):
    psi,psis=shoot(z);return psis/psi+I*z
TRUTH=mp.mpc("0.37367168441804166","-0.08896231568893410")
P("truth %.12f %+.12f i\n%-14s %-30s %-10s %s"%(TRUTH.real,TRUTH.imag,"seed","root","|F|","err"))
for seed in [(0.40,-0.10),(0.30,-0.20),(0.55,-0.15),(0.3737,-0.0890)]:
    try:
        w=mp.findroot(F,mp.mpc(seed[0],seed[1]),tol=mp.mpf("1e-28"))
        r=abs(F(w));err=abs(w-TRUTH)
        P("%-14s %-30s %-10.1e %.2e"%(str(seed),"%.12f %+.12f i"%(w.real,w.imag),float(r),float(err)))
    except Exception as e:
        P("%-14s FAIL %s"%(str(seed),repr(e)[:50]))
P("\nTotal %.1fs"%(time.time()-t0))
