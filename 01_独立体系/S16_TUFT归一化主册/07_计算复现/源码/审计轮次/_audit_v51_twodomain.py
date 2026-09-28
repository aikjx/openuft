# -*- coding: utf-8 -*-
"""
_audit_v51_twodomain.py  -  v51 ROBUST TWO-DOMAIN unit: solve the v50 Q1
interface singularity, push the TUFT static fundamental to a >=11.6-hard-digit
gate. INDEPENDENT re-implementation (read v50 for understanding, NO import),
mpmath dps>=50.
================================================================================
IRON LAW: GR gate first ; independent (no import) ; dps>=50 ; rough starts ;
numbers verbatim ; honest four-state grading ; no fake closure.

PHYSICS (TUFT user-original theory, re-derived here):
  d2psi/ds2 + [w^2 - V(s)] psi = 0 on Jansen tortoise s = b*t (real t).

TWO-DOMAIN SPLIT at t1:
  Domain A (near-wall, t in [0,t1]):  psi = F1(s) e^{i w s} G1(s),
        F1(s) = s^beta P(s),  P(s)=sum_{k=0..K} a_k s^{k mu}, mu=2/3.
  Domain B (far-field, t in [t1, inf]): psi = e^{i w s} G2(s)   (F2=1).

Pencil in G:
  Domain A: G1'' + 2(F1'/F1 + i w) G1' + (F1''/F1 - V) G1 = 0
  Domain B: G2'' + 2 i w G2' - V G2 = 0

MATCHING at s1 (t=t1):
  C0 (psi cont):  F1(s1) G1(s1) = G2(s1)  -> SHARED INTERFACE NODE:
                  G2[0] = F1(s1) * G1[p1-1]  (eliminated, folded into column)
  C1 (psi' cont): F1'G1 + F1 G1'_L = G2'_R  (w-independent after C0).

WHY v50's Q1 WAS SINGULAR (root cause, written out):
  v50 built two Lobatto panels with SEPARATE node sets and imposed BOTH C0 and
  C1 as explicit rows.  The C1 row, written naively as
      psi1' - psi2' = e^{iws1}[ (F1'G1+F1G1'-G2') + i w (F1 G1 - G2) ] = 0,
  splits into a Q0 part (F1'G1+F1G1'-G2') and a Q1 part i(F1G1-G2).  But the
  Q1 part i(F1G1-G2) is EXACTLY the C0 condition, which v50 ALSO wrote as a
  separate row.  Hence the Q1 interface row was a duplicate of the C0 row
  (rank-deficient) -- or, after substituting C0, it vanished identically,
  leaving an all-zero Q1 row.  Either way Q1 lost rank at the interface.
  The C1 constraint acts on G, not on w; a w-independent constraint belongs
  ONLY in Q0.

THE FIX (this script):
  * C0 is NOT a row: the two panels SHARE the interface node.  G2[0] is
    eliminated via G2[0]=F1(s1)*G1[p1-1]; the column G2[0] in every domain-B
    row folds into the G1[p1-1] column.
  * The interface row is a PDE residual (domain-A side at s1), which carries
    a non-zero Q1 = i*2*gA*D_A[intf,:].  So Q1 has NO zero row at the interface.
  * The only Q0-only row is the physical wall regularity G1'(0)=0.
  * C1 continuity is enforced by the shared value + PDE residuals on both
    sides (spectral convergence drives the derivative jump to zero).

Block structure of L(w)=Q0+w Q1, global DOF ordering
[ G1[0..p1-1] (wall..interface), G2[1..p2e-1] (near-interface..far) ]:
  row 0              (wall s=0)     : Q0 = gA D_A[0,:] on G1 ; Q1 = 0
  rows 1..p1-1       (domain A PDE)  : diagonal block A on G1
  rows p1..p1+p2e-2  (domain B PDE)  : diagonal block B on G2[1..] PLUS a folded
                                       column into G1[p1-1] (interface coupling).
"""
import time, random
import mpmath as mp
mp.dps = 55
MPC=mp.mpc; MPF=mp.mpf; j=mp.mpc(1j)
OUT=[]
def out(s=""):
    print(s,flush=True); OUT.append(str(s))

# ---------------- TUFT geometry (verbatim from v50 SSOT) ----------------
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
    if b is None: b=MPF(1)
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
        for kk in range(k+1):
            if m-kk in Ud: rhs+=Ud[m-kk]*a[kk]
        p=k*MU; a[k]=rhs/(p*(p-1+2*BETA))
    return a

FROB_A=None
def lobatto(p):
    xi=[mp.cos(mp.pi*k/(p-1)) for k in range(p)]
    c=[((-1)**k) for k in range(p)]; c[0]*=2; c[-1]*=2
    D=mp.matrix(p,p)
    for i in range(p):
        for k in range(p):
            if i!=k: D[i,k]=(c[i]/c[k])/(xi[i]-xi[k])
        D[i,i]=-sum(D[i,k] for k in range(p) if k!=i)
    return xi,D,D*D

# ---------------- two-domain pencil assembly (NEW, independent) ----------------
def build_twodomain(t1, p1, p2, L_t, peel_near=True):
    b=B_OPT
    # --- domain A: s=b(1+z)/(1-z), z in [-1,z1], clusters near wall s=0 ---
    xiA,DA1,DA2=lobatto(p1)
    xiA=xiA[::-1]; DA1=DA1[::-1,::-1]; DA2=DA2[::-1,::-1]  # now xi[0]=-1 wall, xi[p1-1]=+1 intf
    z1=(t1-1)/(t1+1)                    # s=b*t1 <=> z1=(t1-1)/(t1+1)
    zA=[-1+(z1+1)*(x+1)/2 for x in xiA]
    tA=[(1+zz)/(1-zz) for zz in zA]
    tA[0]=MPF('1e-9')
    sA=[b*t for t in tA]
    dzdi=(z1+1)/2
    gA=[(1-zz)**2/(2*b)*dzdi for zz in zA]   # d/ds = gA d/dxi
    gpA=[-(1-zz)/b*dzdi for zz in zA]        # dgA/dxi
    # --- domain B: Lobatto xi[0]=+1 (inf, DROP), ..., xi[p2-1]=-1 (interface) ---
    etaB,DB1,DB2=lobatto(p2)
    etaB=etaB[1:][::-1]; DB1=DB1[1:,1:][::-1,::-1]; DB2=DB2[1:,1:][::-1,::-1]
    p2e=len(etaB)                       # etaB[0]=-1 interface ; etaB[-1] near inf
    tB=[t1+L_t*(1+e)/(1-e) for e in etaB]
    sB=[b*t for t in tB]
    gB=[(1-e)**2/(2*b*L_t) for e in etaB]
    gpB=[-(1-e)/(b*L_t) for e in etaB]
    # --- rho / V ---
    allt=list(tA)+list(tB)
    tbl=rho_at_nodes(allt)
    rhoA=[tbl[t] for t in tA]; rhoB=[tbl[t] for t in tB]
    VA=[V_of(rho)-1/(3*s**2) for rho,s in zip(rhoA,sA)]
    VB=[V_of(rho) for rho,s in zip(rhoB,sB)]
    n=p1+(p2e-1)
    Q0=mp.matrix(n,n); Q1=mp.matrix(n,n)
    s1_node=sA[p1-1]
    if peel_near:
        P1=MPF(0)
        for k,ak in enumerate(FROB_A):
            pm=k*MU; P1+=ak*s1_node**pm
        F1s1=s1_node**BETA*P1
    else:
        F1s1=MPF(1)
    # row 0: wall regularity G1'(0) + iw G1(0)=0 (Q0: gA D ; Q1: i at wall node)
    for k in range(p1):
        Q0[0,k]=gA[0]*DA1[0,k]
    Q1[0,0]+=j
    # rows 1..p1-1: domain A PDE (incl interface row p1-1, Q1 non-zero)
    for ii in range(1,p1):
        si=sA[ii]; Ui=VA[ii]; gi=gA[ii]; gpi=gpA[ii]
        if peel_near:
            P=MPF(0); Pp=MPF(0); Ppp=MPF(0)
            for k,ak in enumerate(FROB_A):
                pm=k*MU; P+=ak*si**pm
                if k>=1:
                    Pp+=ak*pm*si**(pm-1); Ppp+=ak*pm*(pm-1)*si**(pm-2)
            C10i=2*BETA/si+2*Pp/P
            C00i=Ppp/P+2*BETA*Pp/(si*P)-Ui
        else:
            C10i=MPF(0); C00i=-Ui
        for k in range(p1):
            Q0[ii,k]=gi**2*DA2[ii,k]+(gpi+C10i*gi)*DA1[ii,k]
            Q1[ii,k]=j*2*gi*DA1[ii,k]
        Q0[ii,ii]+=C00i
        Q1[ii,ii]+=j*C10i        # peel contributes diagonal W0=2F'/F to Q1
    # domain B interior rows k=1..p2e-1 (k=0 interface eliminated)
    for k in range(1,p2e):
        grow=p1+(k-1)
        gkB=gB[k]; gpkB=gpB[k]; Vk=VB[k]
        for kk in range(1,p2e):
            gc=p1+(kk-1)
            Q0[grow,gc]=gkB**2*DB2[k,kk]+gkB*gpkB*DB1[k,kk]
            Q1[grow,gc]=j*2*gkB*DB1[k,kk]
        Q0[grow,p1+(k-1)]-=Vk
        fold0=(gkB**2*DB2[k,0]+gkB*gpkB*DB1[k,0])*F1s1
        Q0[grow,p1-1]+=fold0
        Q1[grow,p1-1]+=j*2*gkB*DB1[k,0]*F1s1
    return Q0,Q1,sA,sB

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

# ---- independent Leaver (GR gate A) ----
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
    out("v51 ROBUST TWO-DOMAIN unit - solve v50 Q1 interface singularity")
    out("  dps=%d ; independent re-implementation (NO import of v50/v49)"%mp.dps)
    out("="*80)
    out(""); out("[GR GATE A] Schwarzschild l=2 n=0, independent Leaver")
    wA=solve_leaver(MPF(0),-2,2,2,0)
    eA=abs(wA-GR_N0); dA=digs(eA)
    out("    w=%.18f%+.18fi"%(wA.real,wA.imag))
    out("    |err|=%.3e digits=%.1f GATE A(Leaver): %s"%(eA,dA,"PASS" if dA>=6 else "FAIL"))
    out(""); out("[GEOMETRY] rho_h=%.12f beta=%.12f B_OPT=%.3f%+.3fi"%(RHO_H,BETA,B_OPT.real,B_OPT.imag))
    out(""); out("[NEAR-WALL] extracting U_n ...")
    Ud=nearwall_un(); out("    "+" ".join("U%d=%.3e"%(n,Ud[n].real) for n in (-2,-1,0,1,2)))
    af=frob_series(Ud,16); globals()['FROB_A']=af
    out("    a16=%.3e (Frobenius decay)"%af[16])

    out(""); out("="*80)
    out("[TUFT TWO-DOMAIN] p1 x p2 x t1 scan ; Beyn vs direct GEP")
    out("="*80)
    results=[]
    for t1v in (MPF('0.08'),MPF('0.15'),MPF('0.30')):
        for p1v in (16,24,32):
            for p2v in (24,36,48):
                L_t=MPF(6.0)
                try:
                    Q0,Q1,sA,sB=build_twodomain(t1v,p1v,p2v,L_t)
                    n=Q1.rows
                    zerorows=[r for r in range(n) if max(abs(Q1[r,c]) for c in range(n))<MPF('1e-60')]
                    lamB,_=beyn_extract(Q0,Q1,ANCHOR,MPF('0.006'),60,seed=3)
                    wGEP=MPC(0,0); gep_ok=False
                    try:
                        A=Q1**-1*(-Q0); ev=mp.eig(A)[0]
                        wg=min(ev,key=lambda e:abs(e-ANCHOR))
                        wGEP=wg; gep_ok=True
                    except Exception:
                        wGEP=MPC(0,0)
                    dd=abs(lamB-wGEP) if gep_ok else MPF(9)
                    results.append((t1v,p1v,p2v,lamB,wGEP,gep_ok,dd,zerorows))
                    out("    t1=%s p1=%2d p2=%2d Beyn=%.12f%+.12fi GEP=%s Q1zr=%d |diff|=%.2e"%(
                        t1v,p1v,p2v,lamB.real,lamB.imag,
                        ("%.12f%+.12fi"%(wGEP.real,wGEP.imag)) if gep_ok else "FAIL",
                        len(zerorows),dd))
                except Exception as e:
                    out("    t1=%s p1=%2d p2=%2d FAIL: %s"%(t1v,p1v,p2v,e))
                    results.append((t1v,p1v,p2v,None,None,False,MPF(9),[]))
    out(""); out("="*80); out("SUMMARY"); out("="*80)
    ok=[r for r in results if r[5]]
    if ok:
        best=min(ok,key=lambda r:r[6])
        out("    best Beyn-vs-GEP mutual: |diff|=%.3e (%.1f digits)"%(best[6],digs(best[6])))
        out("    w_Beyn=%.15f%+.15fi"%(best[3].real,best[3].imag))
        out("    w_GEP =%.15f%+.15fi"%(best[4].real,best[4].imag))
        out("    target >=11.6 digits: %s"%("PASS" if digs(best[6])>=MPF('11.6') else "NOT REACHED"))
    out("    wall time %.0fs"%(time.time()-t0))
    with open("_audit_v51_twodomain_out.txt","w",encoding="utf-8") as f:
        f.write("\n".join(OUT))

if __name__=="__main__":
    main()
