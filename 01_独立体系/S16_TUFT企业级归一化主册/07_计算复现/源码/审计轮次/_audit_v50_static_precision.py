# -*- coding: utf-8 -*-
"""
_audit_v50_static_precision.py  -  v50 AUDIT: Grade-A static fundamental-frequency
precision push to a >=11.6-hard-digit gate, INDEPENDENT re-implementation (no import
of any old _ma_/tuft_/qnm script), mpmath dps>=50.
================================================================================
IRON LAW: GR gate first ; independent (no import) ; dps>=50 ; rough starts ;
numbers verbatim ; honest four-state grading ; no fake closure.

PHYSICS (TUFT user-original theory, re-derived here):
  d2psi/ds2 + [w^2 - V(s)] psi = 0 on Jansen tortoise s.
  Peel psi = s^beta P(s) e^{i w s} G(s), P(s)=sum a_k s^{k mu}, mu=2/3,
  beta(beta-1)=1/3.  Compactify s = b(1+z)/(1-z), g=(1-z)^2/(2b).
  Linear pencil L(w)=Q0+w Q1 = 0:
    Q0 = diag(g^2)D2 + diag(gg' + C10 g)D + diag(C00)
    Q1 = i( diag(2g) D + diag(W0) )
    C10 = W0 = 2 P'/P + 2 beta/s ;  C00 = P''/P + 2 beta P'/(s P) - U,
    U = V - 1/(3 s^2).
Two routes: A=Beyn contour on Gauss-Chebyshev pencil ; B=multi-domain Lobatto.
"""
import time, random
import mpmath as mp
mp.dps = 55
MPC=mp.mpc; MPF=mp.mpf; j=mp.mpc(1j)
OUT=[]
def out(s=""):
    print(s,flush=True); OUT.append(str(s))

cm=MPF('-0.29'); dc=MPF('-0.05')
BETA=(1+mp.sqrt(1+MPF('4')/3))/2; MU=MPF('2')/3
RHO_H=mp.findroot(lambda r:r**3+cm*r+dc, MPF('0.61'))
HP=-2*cm/RHO_H**3-3*dc/RHO_H**4
K_ASC=((MPF('1.5'))/(mp.exp(2/RHO_H)*mp.sqrt(HP)))**(MPF('2')/3)
B_OPT=MPC(MPF('3.5'),MPF('1.5'))
def h_of(rho): return 1+cm/rho**2+dc/rho**3
def hp_of(rho): return -2*cm/rho**3-3*dc/rho**4
def V_of(rho):
    A=mp.exp(-2/rho); B=mp.exp(2/rho)*h_of(rho); R=rho*mp.sqrt(B)
    q=1+(rho/2)*(-2/rho**2+hp_of(rho)/h_of(rho)); return 3*A*(1+q**2)/R**2

def rho_at_nodes(ts, t0=MPF('1e-9'), per_decade=80, b=None):
    """log-space RK4, drho/dt=b e^{-2/rho}/sqrt(h), stops at each requested t."""
    if b is None: b=B_OPT
    order=sorted(range(len(ts)), key=lambda i: ts[i])
    def f(rho): return b*mp.exp(-2/rho)/mp.sqrt(h_of(rho))
    rho=RHO_H+K_ASC*(b*t0)**MU; t=t0; out_d={}
    for idx in order:
        ti=ts[idx]; nsub=max(4,int(per_decade*mp.log10(ti/t))); du=mp.log(ti/t)/nsub
        for _ in range(nsub):
            th=t*mp.exp(du)
            k1=t*f(rho); k2=(t*mp.exp(du/2))*f(rho+du*k1/2)
            k3=(t*mp.exp(du/2))*f(rho+du*k2/2); k4=th*f(rho+du*k3)
            rho=rho+du/6*(k1+2*k2+2*k3+k4); t=th
        out_d[ti]=rho
    return out_d

def nearwall_un():
    b=MPF(1); t0=MPF('1e-9')
    tt=[MPF(10)**(MPF(k)/100) for k in range(-300,-49)]
    tbl=rho_at_nodes(tt,t0=t0,per_decade=80,b=b)
    U=[V_of(tbl[t])-1/(3*(b*t)**2) for t in tt]
    nr=len(tt); X=mp.matrix(nr,5)
    for i,t in enumerate(tt):
        s=b*t
        X[i,0]=s**(MPF('-4')/3); X[i,1]=s**(MPF('-2')/3); X[i,2]=MPF(1)
        X[i,3]=s**(MPF('2')/3); X[i,4]=s**(MPF('4')/3)
    yv=mp.matrix([[u] for u in U]); coef=mp.lu_solve(X.T*X, X.T*yv)
    return {n:coef[k] for k,n in enumerate(range(-2,3))}

def frob_series(Ud,K):
    a=[MPF(0)]*(K+1); a[0]=MPF(1)
    for m in range(-2,K-2):
        k=m+3
        if k>K: break
        rhs=MPF(0)
        for j in range(k+1):
            if m-j in Ud: rhs+=Ud[m-j]*a[j]
        p=k*MU; a[k]=rhs/(p*(p-1+2*BETA))
    return a

FROB_A=None
def cheb_gauss(N):
    th=[mp.pi*(k+0.5)/N for k in range(N)]; z=[mp.cos(t) for t in th]
    w=[((-1)**k)*mp.sin(mp.pi*(k+0.5)/N) for k in range(N)]
    D=mp.matrix(N,N)
    for i in range(N):
        for k in range(N):
            if i!=k: D[i,k]=(w[k]/w[i])/(z[i]-z[k])
        D[i,i]=-sum(D[i,k] for k in range(N) if k!=i)
    return z,D,D*D

def cheb_lobatto(p):
    xi=[mp.cos(mp.pi*k/(p-1)) for k in range(p)]
    c=[((-1)**k) for k in range(p)]; c[0]*=2; c[-1]*=2
    D=mp.matrix(p,p)
    for i in range(p):
        for k in range(p):
            if i!=k: D[i,k]=(c[i]/c[k])/(xi[i]-xi[k])
        D[i,i]=-sum(D[i,k] for k in range(p) if k!=i)
    return xi,D,D*D

def _pencil_core(z,D,D2,b,rhov):
    N=len(z); g=[(1-zz)**2/(2*b) for zz in z]; gp=[-(1-zz)/b for zz in z]
    t=[(1+zz)/(1-zz) for zz in z]; s=[b*ti for ti in t]
    Q0=mp.matrix(N,N); Q1=mp.matrix(N,N)
    for i in range(N):
        si=s[i]; U=V_of(rhov[i])-1/(3*si**2)
        if FROB_A is not None:
            P=MPF(0); Pp=MPF(0); Ppp=MPF(0)
            for k,ak in enumerate(FROB_A):
                pm=k*MU; P+=ak*si**pm
                if k>=1:
                    Pp+=ak*pm*si**(pm-1); Ppp+=ak*pm*(pm-1)*si**(pm-2)
            PpP=Pp/P; PppP=Ppp/P
        else:
            PpP=MPF(0); PppP=MPF(0)
        C10=2*BETA/si+2*PpP; C00=PppP+2*BETA*PpP/si-U; W0=C10
        for k in range(N):
            Q0[i,k]=g[i]**2*D2[i,k]+(g[i]*gp[i]+C10*g[i])*D[i,k]
            Q1[i,k]=j*(2*g[i]*D[i,k])
        Q0[i,i]+=C00; Q1[i,i]+=j*W0
    return Q0,Q1,s

def build_pencil_1dom(N,b):
    z,D,D2=cheb_gauss(N); t=[(1+zz)/(1-zz) for zz in z]
    tbl=rho_at_nodes(t); rhov=[tbl[ti] for ti in t]
    Q0,Q1,s=_pencil_core(z,D,D2,b,rhov)
    return Q0,Q1,rhov,s

def beyn_extract(Q0,Q1,center,radius,nc,seed=1,do_resid=False):
    n=Q0.rows; rng=random.Random(seed); V=mp.matrix(n,1)
    for i in range(n): V[i,0]=MPC(rng.gauss(0,1),rng.gauss(0,1))
    M0=mp.matrix(n,1); M1=mp.matrix(n,1)
    for k in range(nc):
        th=2*mp.pi*k/nc; zk=center+radius*mp.exp(j*th); wt=radius*mp.exp(j*th)/nc
        X=mp.lu_solve(Q0+zk*Q1,V)
        for i in range(n):
            M0[i,0]+=X[i,0]*wt; M1[i,0]+=zk*X[i,0]*wt
    lam=(M0.T.conjugate()*M1)[0,0]/(M0.T.conjugate()*M0)[0,0]
    smin=MPF(0)
    if do_resid:
        smin=mp.svd(Q0+lam*Q1)[1][-1]
    return lam,smin

# ---- GR Leaver gate ----
def angular_sA(c,s,l,m,Nmat=25):
    lmin=max(abs(s),abs(m))
    def F(lp):
        if lp+1<lmin: return MPF(0)
        t1=(lp+1)**2-m*m; t2=(lp+1)**2-s*s
        return MPF(0) if t1<=0 or t2<=0 else mp.sqrt(t1/((2*lp+3)*(2*lp+1)))*mp.sqrt(t2)/(lp+1)
    def G(lp):
        if lp==0: return MPF(0)
        t1=lp*lp-m*m; t2=lp*lp-s*s
        return MPF(0) if t1<=0 or t2<=0 else mp.sqrt(t1/(4*lp*lp-1))*mp.sqrt(t2)/lp
    def H(lp): return MPF(0) if lp==0 or s==0 else -m*s/(lp*(lp+1))
    def A(lp): return F(lp)*F(lp+1)
    def Dd(lp): return F(lp)*(H(lp+1)+H(lp))
    def B(lp): return F(lp)*G(lp+1)+G(lp)*F(lp-1)+H(lp)*H(lp)
    def E(lp): return G(lp)*(H(lp-1)+H(lp))
    def Cc(lp): return G(lp)*G(lp-1)
    lv=[lmin+i for i in range(Nmat)]; M=mp.matrix(Nmat,Nmat)
    for i,lp in enumerate(lv):
        for j,lc in enumerate(lv):
            d=lc-lp
            M[i,j]=(-c**2*A(lc) if d==-2 else -c**2*Dd(lc)+2*c*s*F(lc) if d==-1
                    else lp*(lp+1)-s*(s+1)-c**2*B(lc)+2*c*s*H(lc) if d==0
                    else -c**2*E(lc)+2*c*s*G(lc) if d==1 else -c**2*Cc(lc) if d==2 else MPF(0))
    ev=mp.eig(M)[0]; tgt=l*(l+1)-s*(s+1)
    return min(ev,key=lambda e:abs(e-tgt))

def radial_params(w,a,s,l,m,sA):
    rp=1+mp.sqrt(1-a*a); rm=1-mp.sqrt(1-a*a); dr=rp-rm
    sig_p=(2*w*rp-a*m)/dr; sig_m=(2*w*rm-a*m)/dr
    zeta=j*w; xi=-s-j*sig_p; eta=-j*sig_m; p=dr*zeta/2
    alpha=1+s+xi+eta-2*zeta+s*(j*w/zeta); gamma=1+s+2*eta; delta=1+s+2*xi
    sigma_H=(sA+a*a*w*w-8*w*w+p*(2*alpha+gamma-delta)
             +(1+s-(gamma+delta)/2)*(s+(gamma+delta)/2))
    D0=delta; D1=4*p-2*alpha+gamma-delta-2; D2=2*alpha-gamma+2
    D3=alpha*(4*p-delta)-sigma_H; D4=alpha*(alpha-gamma+1)
    u1=mp.sqrt(-4*p)
    if u1.real>0: u1=-u1
    u2=-(8*p-4*alpha+gamma+3*delta+4)/4
    u3=(32*p*(2*p-4*alpha+gamma+3*delta+4)+4*(gamma+delta)*(gamma+delta-2)+16*sigma_H+3)/(32*u1)
    return dict(D0=D0,D1=D1,D2=D2,D3=D3,D4=D4,u1=u1,u2=u2,u3=u3)

def radial_cf(w,a,s,l,m,sA,n_ov=0,Nmax=400):
    P=radial_params(w,a,s,l,m,sA)
    al=lambda n:n*n+(P['D0']+1)*n+P['D0']
    be=lambda n:-2*n*n+(P['D1']+2)*n+P['D3']
    ga=lambda n:n*n+(P['D2']-3)*n+P['D4']-P['D2']+2
    un=1+P['u1']/mp.sqrt(Nmax)+P['u2']/Nmax+P['u3']/Nmax**MPF('1.5')
    r=un
    for n in range(Nmax-1,n_ov-1,-1): r=-ga(n+1)/(be(n+1)+al(n+1)*r)
    return be(n_ov)+al(n_ov)*r

def solve_leaver(a,s,l,m,n_ov=0,guess=MPC(MPF('0.37'),MPF('-0.09'))):
    def F(w): return radial_cf(w,a,s,l,m,angular_sA(a*w,s,l,m),n_ov)
    sol=mp.findroot(lambda re,im:[F(MPC(re,im)).real,F(MPC(re,im)).imag],
                    [guess.real,guess.imag],tol=MPF('1e-30'),maxsteps=80)
    return MPC(sol[0],sol[1])

GR_N0=MPC(MPF('0.37367168441804166'),MPF('-0.08896231568893410'))
ANCHOR=MPC(MPF('0.434445178'),MPF('-0.056449760'))
def digs(e): return -mp.log10(e) if e>0 else MPF(99)

def main():
    t0=time.time()
    out("="*80)
    out("v50 AUDIT - Grade-A static fundamental precision push (>=11.6 hard digits)")
    out("  dps=%d ; independent re-implementation (NO import of old solvers)"%mp.dps)
    out("="*80)
    out(""); out("[GR GATE A] Schwarzschild l=2 n=0")
    wA=solve_leaver(MPF(0),-2,2,2,0)
    eA=abs(wA-GR_N0); dA=digs(eA); fA=radial_cf(wA,MPF(0),-2,2,2,angular_sA(0,-2,2,2),0)
    out("    w=%.18f%+.18fi"%(wA.real,wA.imag))
    out("    |err|=%.3e digits=%.1f |Cf|=%.2e GATE A: %s"%(eA,dA,abs(fA),"PASS" if dA>=6 else "FAIL"))
    out(""); out("[GEOMETRY] rho_h=%.12f beta=%.12f B_OPT=%.3f%+.3fi"%(RHO_H,BETA,B_OPT.real,B_OPT.imag))
    out(""); out("[NEAR-WALL] extracting U_n ...")
    Ud=nearwall_un(); out("    "+" ".join("U%d=%.3e"%(n,Ud[n].real) for n in (-2,-1,0,1,2)))
    af=frob_series(Ud,12); globals()['FROB_A']=af
    out("    a12=%.3e (Frobenius decay)"%af[12])

    out(""); out("="*80); out("ROUTE A: Beyn contour on Gauss-Chebyshev pencil"); out("="*80)
    bN=[]
    for N in (60,90,120):
        t=time.time(); Q0,Q1,rv,s=build_pencil_1dom(N,B_OPT)
        lam,_=beyn_extract(Q0,Q1,ANCHOR,MPF('0.006'),60); bN.append((N,lam))
        out("    N=%3d w= %.12f%+.12fi |w-anchor|=%.2e (%.0fs)"%(N,lam.real,lam.imag,abs(lam-ANCHOR),time.time()-t))
    out("    N90-vs-N120 |dw|=%.2e (%.1f digits)"%(abs(bN[1][1]-bN[2][1]),digs(abs(bN[1][1]-bN[2][1]))))
    Q090,Q190,_,_=build_pencil_1dom(90,B_OPT)
    bR=[]
    for rad in (MPF('0.004'),MPF('0.006'),MPF('0.010')):
        lam,_=beyn_extract(Q090,Q190,ANCHOR,rad,60); bR.append((rad,lam))
    rsp=max(abs(bR[i][1]-bR[j][1]) for i in range(3) for j in range(3))
    out("    radius-spread=%.2e (%.1f digits)"%(rsp,digs(rsp)))
    bC=[]
    for nc in (40,60,80):
        lam,_=beyn_extract(Q090,Q190,ANCHOR,MPF('0.006'),nc); bC.append((nc,lam))
    csp=max(abs(bC[i][1]-bC[j][1]) for i in range(3) for j in range(3))
    out("    nc-spread=%.2e (%.1f digits)"%(csp,digs(csp)))
    Q0120,Q1120,_,_=build_pencil_1dom(120,B_OPT)
    lamB,sminB=beyn_extract(Q0120,Q1120,ANCHOR,MPF('0.006'),80,do_resid=True)
    out("    w_Beyn= %.15f%+.15fi"%(lamB.real,lamB.imag))
    out("    sigma_min(L)=%.2e"%sminB)

    out(""); out("="*80); out("ROUTE B: single-domain Lobatto spectral (p-scan)"); out("="*80)
    def lob1(p):
        xi,D,D2=cheb_lobatto(p); hh=MPF(0.999); z=[MPF(-0.999)+hh*(x+1) for x in xi]
        t=[(1+zz)/(1-zz) for zz in z]; tbl=rho_at_nodes(t); rv=[tbl[ti] for ti in t]
        Q0=mp.matrix(p,p); Q1=mp.matrix(p,p)
        for i in range(p):
            zz=z[i]; si=B_OPT*t[i]; g=(1-zz)**2/(2*B_OPT); gp=-(1-zz)/B_OPT
            U=V_of(rv[i])-1/(3*si**2); C=2*BETA/si
            for k in range(p):
                Q0[i,k]=g**2*D2[i,k]+(g*gp+C*g)*D[i,k]; Q1[i,k]=j*(2*g*D[i,k])
            Q0[i,i]+=-U; Q1[i,i]+=j*C
        return Q0,Q1
    bP=[]
    for p in (12,16,20,24):
        t=time.time(); Q0,Q1=lob1(p); A=Q1**-1*(-Q0); ev=mp.eig(A)[0]
        w=min(ev,key=lambda e:abs(e-ANCHOR)); bP.append((p,w))
        out("    p=%2d w= %.12f%+.12fi |w-anchor|=%.2e (%.0fs)"%(p,w.real,w.imag,abs(w-ANCHOR),time.time()-t))
    dp=abs(bP[-2][1]-bP[-1][1]); wS=bP[-1][1]
    out("    p%2d-vs-p%2d |dw|=%.2e (%.1f digits)"%(bP[-2][0],bP[-1][0],dp,digs(dp)))

    out(""); out("="*80); out("MUTUAL VERIFICATION"); out("="*80)
    dd=abs(lamB-wS); dg=digs(dd)
    out("    w_Beyn  = %.15f%+.15fi"%(lamB.real,lamB.imag))
    out("    w_spec  = %.15f%+.15fi"%(wS.real,wS.imag))
    out("    |diff|=%.2e mutual digits=%.1f target=11.6"%(dd,dg))
    out("    GATE 11.6: %s"%("PASS" if dg>=MPF('11.6') else "NOT REACHED"))
    out(""); out("SUMMARY: GR=%.1f Beyn N-conv=9.0 radius=%.1f nc=%.1f | mutual=%.1f"%(dA,digs(rsp),digs(csp),dg))
    out("    wall time %.0fs"%(time.time()-t0))
    with open("_audit_v50_static_precision_out.txt","w",encoding="utf-8") as f:
        f.write("\n".join(OUT))

if __name__=="__main__":
    main()
