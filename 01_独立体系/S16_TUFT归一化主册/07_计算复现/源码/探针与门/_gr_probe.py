# -*- coding: utf-8 -*-
import mpmath as mp
mp.dps=40
MPC=mp.mpc; MPF=mp.mpf; j=mp.mpc(1j)

# Schwarzschild r, tortoise s* = r + 2 ln(r/2 - 1), f=1-2/r
def fof(r): return 1-2/r
def sstar_of_r(r): return r + 2*mp.log(r/2-1)

# map a reference point on s*: we will sample s* directly via r nodes.
# RW potential candidates (l=2)
def V_rw1(r):  # f*(6/r2 - 6f/r)
    return fof(r)*(6/r**2 - 6*fof(r)/r)
def V_rw2(r):  # f*(6/r2 - 6/r)
    return fof(r)*(6/r**2 - 6/r)
def V_zerr(r): # Zerilli proper
    lam=2.0
    return fof(r)*(lam**2*(lam+1)*r**2+3*lam*r+9)/(r**2*(lam*r+3)**2)

# Chebyshev-Lobatto nodes on [-1,1] (with endpoints)
def lobatto(p):
    xi=[mp.cos(mp.pi*k/(p-1)) for k in range(p)]
    c=[(-1)**k for k in range(p)]; c[0]*=2; c[-1]*=2
    D=mp.matrix(p,p)
    for i in range(p):
        for k in range(p):
            if i!=k: D[i,k]=(c[i]/c[k])/(xi[i]-xi[k])
        D[i,i]=-sum(D[i,x] for x in range(p) if x!=i)
    return xi,D,D*D

# Build single-domain GEP on s* in [s_a, s_b]. Factor psi=e^{i w s*} G.
# horizon (s_a, r->2): ingoing => G'_a + 2 i w G_a = 0 (row0)
# far (s_b): outgoing G'=0 natural (we just collocate; last node near s_b, V small)
def probe(Vof, p=40, s_a=-20.0, s_b=30.0, hsign=+1):
    xi,D1,D2=lobatto(p)
    s=[s_a+(s_b-s_a)*(x+1)/2 for x in xi]
    # drop FAR node (index p-1); keep nodes i=0..p-2 (horizon .. near-far)
    m=p-1
    ds_dxi=(s_b-s_a)/2
    g=MPF(1)/ds_dxi
    def r_of_s(sv):
        lo=MPF(2.0001); hi=MPF(100)
        for _ in range(200):
            mid=(lo+hi)/2
            if sstar_of_r(mid) < sv: lo=mid
            else: hi=mid
        return (lo+hi)/2
    Q0=mp.matrix(m,m); Q1=mp.matrix(m,m)
    for i in range(m):
        si=s[i]; ri=r_of_s(si); Vi=Vof(ri)
        for k in range(m):
            Q0[i,k]=g*g*D2[i,k] - (0 if k!=i else Vi)
            Q1[i,k]=j*2*g*D1[i,k]
    # row0 = horizon ingoing: G'_a + hsign*2 i w G_a =0
    for k in range(m):
        Q0[0,k]=g*D1[0,k]
        Q1[0,k]=hsign*2*j*(1 if k==0 else MPF(0))
    A=Q1**-1*(-Q0)
    ev=mp.eig(A)[0]
    cand=[e for e in ev if 0.15<e.real<0.65]
    cand=sorted(cand,key=lambda e:e.real)
    return [(e.real,e.imag) for e in cand]

for name,V in [('rw1',V_rw1),('rw2',V_rw2),('zerr',V_zerr)]:
    for hsign in (+1,-1):
        try:
            evs=probe(V,hsign=hsign)
            print(name,'hsign=%+d'%hsign, [('%.4f%+.4fi'%(a,b)) for a,b in evs])
        except Exception as e:
            print(name,'hsign=%+d FAIL'%(hsign),e)
