# -*- coding: utf-8 -*-
"""
MainAgent v15 high-precision gate (independent; does NOT import coalition).
GR Schwarzschild RW s=-2 l=2: does INWARD shooting converge at high precision
once far-field outgoing log-derivative includes O(1/s^2) (iw - 3i/(w s^2))?
Shared s-grid built once, truncated per s_out. Valid QNM solver must converge
monotonically to 0.3736716844 - 0.0889623157 i as s_out grows.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import mpmath as mp
mp.mp.dps = 40
I = mp.mpc(0,1)
t0=time.time()
def P(*a): print(*a, flush=True)

S_IN=mp.mpf(-8); S_MAX=mp.mpf(180); H=mp.mpf("0.05")
n=int(mp.floor((S_MAX-S_IN)/H))
P("building shared s grid N=%d ..."%(n+1))
# r(s) table
NR=300001
rlo=mp.mpf(2)+mp.mpf("1e-9"); rhi=mp.mpf(200)
rr=[rlo+(rhi-rlo)*k/NR for k in range(NR+1)]
ss=[r+2*mp.log(r/2-1) for r in rr]
s=[S_IN+H*k for k in range(n+1)]
V=[]; j=0
for sk in s:
    while j+1<len(ss) and ss[j+1]<sk: j+=1
    s0,s1=ss[j],ss[j+1]
    rk=rr[j]+(sk-s0)*(rr[j+1]-rr[j])/(s1-s0)
    f=1-2/rk
    V.append(f*(6/rk**2-6/rk**3))
P("grid ready %.1f s, s range [%s,%s]"%(time.time()-t0,s[0],s[-1]))

def rk4_inward(Nidx,w,Lo):
    a,b=w.real,w.imag
    u,v,us,vs=mp.mpf(1),mp.mpf(0),Lo.real,Lo.imag
    W0=-a*a+b*b; tb=2*a*b; q=-H
    for k in range(Nidx,0,-1):
        def d(U,Vk):
            x,y,xs,ys=U
            return (xs,ys,(Vk+W0)*x+tb*y,(Vk+W0)*y-tb*x)
        U=(u,v,us,vs)
        k1=d(U,V[k])
        U2=tuple(U[j]+q/2*k1[j] for j in range(4)); k2=d(U2,V[k])
        U3=tuple(U[j]+q/2*k2[j] for j in range(4)); k3=d(U3,V[k])
        U4=tuple(U[j]+q*k3[j] for j in range(4));   k4=d(U4,V[k-1])
        u,v,us,vs=(U[j]+q/6*(k1[j]+2*k2[j]+2*k3[j]+k4[j]) for j in range(4))
    return mp.mpc(u,v),mp.mpc(us,vs)

TRUTH=mp.mpc("0.37367168441804166","-0.08896231568893410")
def solve(s_out,guess):
    Nidx=int(mp.floor((mp.mpf(s_out)-S_IN)/H))
    so=s[Nidx]
    def F(z):
        Lo=I*z-3*I/(z*so**2)
        psi,psis=rk4_inward(Nidx,z,Lo)
        return psis/psi-(-I*z)
    root=mp.findroot(F,guess,tol=mp.mpf("1e-25"))
    return root,abs(F(root)),Nidx

P("="*84);P("MA v15 GR gate: inward, outgoing iw-3i/(w s^2), dps=%d"%mp.mp.dps);P("="*84)
P("truth %.15f %+.15f i\n"%(TRUTH.real,TRUTH.imag))
P("  %-6s %-6s %-30s %-10s %-9s"%("s_out","Ngrid","omega","|F|","err"))
guess=mp.mpc("0.40","-0.10")
for so in [40,60,90,130,180]:
    try:
        w,r,Ni=solve(so,guess)
        err=abs(w-TRUTH); dig=max(0,int(-mp.floor(mp.log10(err)))) if err>0 else 99
        P("  %-6d %-6d %-30s %-10.2e %-9.2e dig=%d"%(so,Ni+1,
          "%.12f %+.12f i"%(w.real,w.imag),float(r),float(err),dig))
        guess=w
    except Exception as e:
        P("  %-6d FAIL %s"%(so,repr(e)[:70]))
P("\nTotal %.1f s"%(time.time()-t0))
