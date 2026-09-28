# -*- coding: utf-8 -*-
"""
_audit_v52_twodomain_refine.py
  v52: THREE REFINEMENTS to the robust two-domain QNM assembly, target >=11.6
  hard digits on the TUFT static fundamental (Beyn <-> GEP mutual).
  INDEPENDENT re-implementation (read v51 for structure; NO import of v51/v50).
  mpmath dps>=50.

REFINEMENTS (per v51 report / task):
  R1. Explicit interface C1 row (Q0-only).  Replace the v51 "interface row =
      domain-A PDE residual" by the explicit derivative-continuity row
          G1'(s1) - G2'(s1)/F1(s1) + (F1'/F1)(s1) G1(s1) = 0
      which is w-INDEPENDENT after folding C0 (G2[0]=F1 G1(s1)); hence it lives
      ONLY in Q0, carries ZERO Q1, and replaces the domain-A interface PDE row.
  R2. Domain-A wall nodes -> Gauss-Chebyshev SECOND-kind INTERIOR nodes (roots
      of U_p1, no endpoints).  The wall Robin BC G'(0)+i w G(0)=0 becomes a
      separate row0 evaluated by EXTRAPOLATION to xi=-1 (it does NOT consume an
      interpolation node).  This removes the endpoint-interpolation error of the
      Lobatto wall Robin row.
  R3. Far-field truncation L_t = 4/6/8 scan; check outgoing-boundary convergence
      and whether the spurious root ~0.44+0.008i clears.

GR GATE FIRST (iron law): the SAME two-domain assembly, on the Schwarzschild
  RW potential, must reproduce n0 = 0.3736716844-0.0889623157i to >=11.6
  digits before any TUFT reading is trusted.  If it fails, localize the bad
  residual (wall row / interface C1 / far truncation / pencil discretization).

Honest four-state grading; no fake closure; numbers verbatim from raw run.
"""
import time, random
import numpy as np
from scipy.linalg import eig as sp_eig
import mpmath as mp
mp.dps = 55
MPC = mp.mpc; MPF = mp.mpf; j = mp.mpc(1j)
OUT = []
def out(s=""):
    print(s, flush=True); OUT.append(str(s))

# =====================================================================
# TUFT geometry (verbatim SSOT)
# =====================================================================
cm = MPF('-0.29'); dc = MPF('-0.05')
BETA = (1+mp.sqrt(1+MPF('4')/3))/2; MU = MPF('2')/3
RHO_H = mp.findroot(lambda r: r**3+cm*r+dc, MPF('0.61'))
HP = -2*cm/RHO_H**3-3*dc/RHO_H**4
K_ASC = ((MPF('1.5'))/(mp.exp(2/RHO_H)*mp.sqrt(HP)))**(MPF('2')/3)
B_OPT = MPC(MPF('3.5'), MPF('1.5'))
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

FROB_A = None

# =====================================================================
# Spectral primitives (independent)
# =====================================================================
def chebU_nodes(p):
    """Gauss-Chebyshev 2nd-kind (roots of U_p): interior, NO endpoints.
       returns xi sorted ascending (index0 ~ -1 wall, index p-1 ~ +1 intf)."""
    xi=[mp.cos(mp.pi*k/(p+1)) for k in range(1,p+1)]
    xi=xi[::-1]
    return xi

def bary_weights(xi):
    p=len(xi); w=[]
    for k in range(p):
        pr=MPF(1)
        for j in range(p):
            if j!=k: pr*=(xi[k]-xi[j])
        w.append(1/pr)
    return w

def chebU_diff(xi):
    """collocation derivative D1[i,k]=d/dxi at node i wrt nodal values; D2=D1^2."""
    p=len(xi); w=bary_weights(xi)
    D=mp.matrix(p,p)
    for i in range(p):
        for k in range(p):
            if i==k: continue
            D[i,k]=(w[k]/w[i])/(xi[i]-xi[k])
        D[i,i]=-sum(D[i,x] for x in range(p) if x!=i)
    return D, D*D

def boundary_rows(xi, xb):
    """Lagrange value row L_k(xb) and derivative row L'_k(xb) at off-node xb,
       via barycentric formula."""
    p=len(xi); w=bary_weights(xi)
    S=MPC(0); Sp=MPC(0)
    terms=[]
    for k in range(p):
        t=w[k]/(xb-xi[k]); terms.append(t); S+=t; Sp+=w[k]/(xb-xi[k])**2
    Lval=mp.matrix(p,1); Lder=mp.matrix(p,1)
    for k in range(p):
        Lval[k,0]=terms[k]/S
        Lder[k,0]=-w[k]/(xb-xi[k])**2/S + Lval[k,0]*Sp/S
    return Lval, Lder

def lobatto(p):
    xi=[mp.cos(mp.pi*k/(p-1)) for k in range(p)]
    c=[((-1)**k) for k in range(p)]; c[0]*=2; c[-1]*=2
    D=mp.matrix(p,p)
    for i in range(p):
        for k in range(p):
            if i!=k: D[i,k]=(c[i]/c[k])/(xi[i]-xi[k])
        D[i,i]=-sum(D[i,k] for k in range(p) if k!=i)
    return xi,D,D*D

# =====================================================================
# TUFT two-domain assembly (v52 refinements R1+R2 built in)
#   C1_on : explicit Q0-only C1 row replaces domain-A interface PDE row
#   node_type: 'chebu' (R2 interior) or 'lobatto' (v51 endpoints, for scan)
# =====================================================================
def build_tuft(t1, p1, p2, L_t, C1_on=True, node_type='chebu'):
    b=B_OPT
    # ---- domain A reference nodes ----
    if node_type=='chebu':
        xiA=chebU_nodes(p1)                 # interior, no endpoints
    else:
        xiA,_,_=lobatto(p1)
        xiA=xiA[::-1]                       # index0=-1 wall node, index p1-1=+1 intf node
    D1A,D2A=chebU_diff(xiA)
    z1=(t1-1)/(t1+1); az=(z1+1)/2
    zA=[-1+az*(x+1) for x in xiA]
    tA=[(1+zz)/(1-zz) for zz in zA]
    sA=[b*t for t in tA]
    # Jacobian gA = d xi / ds  (chain rule, INDEPENDENTLY derived)
    gA=[(1-zz)**2/(2*b*az) for zz in zA]
    gpA=[-(1-zz)/b for zz in zA]            # d gA / d xi
    # boundary extrapolation rows at wall xi=-1 and interface xi=+1
    Lw_val,Lw_der=boundary_rows(xiA,-MPF(1))
    Li_val,Li_der=boundary_rows(xiA, MPF(1))
    gA_wall=(MPF(1)-(-MPF(1)))**2/(2*b*az)   # gA at xi=-1
    gA_intf=(MPF(1)-z1)**2/(2*b*az)          # gA at xi=+1
    # ---- domain B: Lobatto drop e=+1 (infinity) ----
    etaB,DB1,DB2=lobatto(p2)
    etaB=etaB[1:][::-1]; DB1=DB1[1:,1:][::-1,::-1]; DB2=DB2[1:,1:][::-1,::-1]
    p2e=len(etaB)                            # etaB[0]=-1 interface
    tB=[t1+L_t*(1+e)/(1-e) for e in etaB]
    sB=[b*t for t in tB]
    gB=[(1-e)**2/(2*b*L_t) for e in etaB]
    gpB=[-(1-e)/(b*L_t) for e in etaB]
    # ---- rho / V ----
    allt=list(tA)+list(tB)
    tbl=rho_at_nodes(allt)
    rhoA=[tbl[t] for t in tA]; rhoB=[tbl[t] for t in tB]
    VA=[V_of(rho)-1/(3*s**2) for rho,s in zip(rhoA,sA)]
    VB=[V_of(rho) for rho,s in zip(rhoB,sB)]
    # ---- F1 at interface ----
    def peel_at(si):
        P=MPF(0); Pp=MPF(0); Ppp=MPF(0)
        for k,ak in enumerate(FROB_A):
            pm=k*MU; P+=ak*si**pm
            if k>=1:
                Pp+=ak*pm*si**(pm-1); Ppp+=ak*pm*(pm-1)*si**(pm-2)
        C10=2*BETA/si+2*Pp/P
        C00=Ppp/P+2*BETA*Pp/(si*P)
        F=si**BETA*P
        return C10,C00,F,Pp,P
    s1_node=sA[p1-1]
    C10_1,C00_1,F1s1,Pp1,P1=peel_at(s1_node)
    F1prime_over_F1 = BETA/s1_node + Pp1/P1
    # ---- global matrix ----
    n=p1+(p2e-1)
    Q0=mp.matrix(n,n); Q1=mp.matrix(n,n)
    # row0: wall Robin G'(0) + i w G(0)=0 (c=1 for TUFT reflecting wall)
    for k in range(p1):
        Q0[0,k]=gA_wall*Lw_der[k,0]
        Q1[0,k]=j*Lw_val[k,0]
    # domain-A PDE rows. With C1_on, the interface node/row is REPLACED by C1.
    # node_type='chebu': interior nodes i=1..p1-2 carry PDE; row p1-1 = C1.
    # node_type='lobatto': v51 style rows 1..p1-1 PDE (interface PDE at p1-1);
    #   if C1_on, row p1-1 becomes C1 (interface PDE dropped).
    last_pde = p1-2 if C1_on else p1-1
    for i in range(1,last_pde+1):
        si=sA[i]; Ui=VA[i]; gi=gA[i]; gpi=gpA[i]
        C10i,C00i,_F,_Pp,_P=peel_at(si)
        C00i=C00i-Ui
        grow=i
        for k in range(p1):
            Q0[grow,k]=gi**2*D2A[i,k]+(gpi+C10i*gi)*D1A[i,k]
            Q1[grow,k]=j*2*gi*D1A[i,k]
        Q0[grow,i]+=C00i
        Q1[grow,i]+=j*C10i
    if C1_on:
        # row p1-1 = explicit C1 (Q0-only), replaces domain-A interface PDE row
        grow=p1-1
        for k in range(p1):
            Q0[grow,k]=gA_intf*Li_der[k,0]+Li_val[k,0]*(-gB[0]*DB1[0,0]+F1prime_over_F1)
            Q1[grow,k]=0
        for kk in range(1,p2e):
            gc=p1+(kk-1)
            Q0[grow,gc]=-gB[0]*DB1[0,kk]/F1s1
            Q1[grow,gc]=0
    # domain-B interior rows kk=1..p2e-1 (kk=0 interface folded)
    for kk in range(1,p2e):
        grow=p1+(kk-1)
        gk=gB[kk]; gpk=gpB[kk]; Vk=VB[kk]
        for jj in range(1,p2e):
            gc=p1+(jj-1)
            Q0[grow,gc]=gk**2*DB2[kk,jj]+gk*gpk*DB1[kk,jj]
            Q1[grow,gc]=j*2*gk*DB1[kk,jj]
        Q0[grow,grow]-=Vk
        # fold G2[0]=F1(s1) G1(s1)  -> G1(s1)=sum Li_val G1
        fold0_Q0=(gk**2*DB2[kk,0]+gk*gpk*DB1[kk,0])*F1s1
        fold0_Q1=j*2*gk*DB1[kk,0]*F1s1
        for k in range(p1):
            Q0[grow,k]+=fold0_Q0*Li_val[k,0]
            Q1[grow,k]+=fold0_Q1*Li_val[k,0]
    return Q0,Q1,sA,sB

# =====================================================================
# Beyn contour + direct GEP
# =====================================================================
def beyn_extract(Q0,Q1,center,radius,nc,seed=1):
    n=Q0.rows; rng=random.Random(seed); V=mp.matrix(n,1)
    for i in range(n): V[i,0]=MPC(rng.gauss(0,1),rng.gauss(0,1))
    M0=mp.matrix(n,1); M1=mp.matrix(n,1)
    for k in range(nc):
        th=2*mp.pi*k/nc; zk=center+radius*mp.exp(j*th); wt=radius*mp.exp(j*th)/nc
        X=mp.lu_solve(Q0+zk*Q1,V)
        for i in range(n):
            M0[i,0]+=X[i,0]*wt; M1[i,0]+=zk*X[i,0]*wt
    lam=(M0.T.conjugate()*M1)[0,0]/(M0.T.conjugate()*M0)[0,0]
    return lam

def gep_nearest(Q0,Q1,anchor):
    """Generalized eig (scipy) tolerating a SINGULAR Q1 (the Q0-only C1 row
    introduces one all-zero Q1 row; a plain Q1^-1 companion is impossible).
    Solves (-Q0) v = w Q1 v ; keeps finite eigenvalues nearest anchor."""
    n=Q0.rows
    A=np.zeros((n,n),dtype=complex); B=np.zeros((n,n),dtype=complex)
    for i in range(n):
        for k in range(n):
            A[i,k]=complex(Q0[i,k]); B[i,k]=complex(Q1[i,k])
    with np.errstate(all='ignore'):
        ev=sp_eig(-A, B, overwrite_a=True, overwrite_b=True, check_finite=False)[0]
    anch=complex(anchor)
    cand=[complex(e) for e in ev
          if np.isfinite(e.real) and np.isfinite(e.imag)
          and abs(e.real)<1e4 and abs(e.imag)<1e4]
    if not cand:
        return MPC(0,0)
    wg=min(cand,key=lambda e:abs(e-anch))
    return MPC(wg)

GR_N0=MPC(MPF('0.37367168441804166'),MPF('-0.08896231568893410'))
ANCHOR=MPC(MPF('0.434445178'),MPF('-0.056449760'))
def digs(e): return -mp.log10(e) if e>0 else MPF(99)

# =====================================================================
# Independent Leaver (GR gate A) -- carried from v51 SSOT, rewritten here
# =====================================================================
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
    lv=[lmin+i for i in range(Nmat)]; M=mp.matrix(Nmat,Nmat)
    for i,lp in enumerate(lv):
        for j,lc in enumerate(lv):
            d=lc-lp
            M[i,j]=(-c**2*F(lc)*F(lc+1) if d==-2
                else -c**2*(F(lc)*(H(lc+1)+H(lc)))+2*c*s*F(lc) if d==-1
                else lp*(lp+1)-s*(s+1)-c**2*(F(lc)*G(lc+1)+G(lc)*F(lc-1)+H(lc)**2)+2*c*s*H(lc) if d==0
                else -c**2*(G(lc)*(H(lc-1)+H(lc)))+2*c*s*G(lc) if d==1
                else -c**2*(G(lc)*G(lc-1)) if d==2 else MPF(0))
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

# =====================================================================
# GR gate B: SAME two-domain assembly on Schwarzschild RW potential.
#   Near boundary = horizon ingoing (row0 G'+2 i w G=0, c=2).
#   Domain A near horizon (F=1 peel), domain B far outgoing, C0/C1 match.
# =====================================================================
def rw_V(r):
    f=1-2/r
    return f*(6/r**2-6*f/r)     # l=2 positive barrier

def build_gr_two(t1star,p1,p2,Ltstar):
    """Two-domain on Schwarzschild tortoise s*. Domain A s* in [s_hor,s1],
       domain B s* in [s1,s_hi]. Reference xi interior (chebu) on A,
       Lobatto drop +inf on B. c=2 horizon ingoing."""
    s_hor=MPF(-20.0); s1=MPF(t1star)
    # domain A map: linear s* = s_hor + (s1-s_hor)*(xi+1)/2
    xiA=chebU_nodes(p1)
    D1A,D2A=chebU_diff(xiA)
    sA=[s_hor+(s1-s_hor)*(x+1)/2 for x in xiA]
    ds_dxi=(s1-s_hor)/2
    gA=[MPF(1)/ds_dxi for _ in xiA]
    gpA=[MPF(0) for _ in xiA]
    Lw_val,Lw_der=boundary_rows(xiA,-MPF(1))
    Li_val,Li_der=boundary_rows(xiA, MPF(1))
    gA_wall=MPF(1)/ds_dxi; gA_intf=MPF(1)/ds_dxi
    # domain B: s* = s1 + Ltstar*(1+e)/(1-e), drop e=+1
    etaB,DB1,DB2=lobatto(p2)
    etaB=etaB[1:][::-1]; DB1=DB1[1:,1:][::-1,::-1]; DB2=DB2[1:,1:][::-1,::-1]
    p2e=len(etaB)
    sB=[s1+Ltstar*(1+e)/(1-e) for e in etaB]
    gB=[MPF(1)/Ltstar*(1-e)**2/2 for e in etaB]
    gpB=[-(1-e)/Ltstar for e in etaB]
    # r from s* via bisection
    def r_of_s(sv):
        lo=MPF(2.00001); hi=MPF(200)
        for _ in range(120):
            mid=(lo+hi)/2; ssm=mid+2*mp.log(mid/2-1)
            if ssm<sv: lo=mid
            else: hi=mid
        return (lo+hi)/2
    VA=[rw_V(r_of_s(s)) for s in sA]
    VB=[rw_V(r_of_s(s)) for s in sB]
    n=p1+(p2e-1)
    Q0=mp.matrix(n,n); Q1=mp.matrix(n,n)
    # row0 horizon ingoing: G'(s_hor)+2 i w G=0  (c=2)
    for k in range(p1):
        Q0[0,k]=gA_wall*Lw_der[k,0]
        Q1[0,k]=2*j*Lw_val[k,0]
    # domain A PDE (F=1 peel: C10=0, C00=-V)
    last_pde=p1-2
    for i in range(1,last_pde+1):
        grow=i; gi=gA[i]
        for k in range(p1):
            Q0[grow,k]=gi**2*D2A[i,k]
            Q1[grow,k]=j*2*gi*D1A[i,k]
        Q0[grow,i]-=VA[i]
    # C1 row p1-1 (Q0-only). F1=1 -> F1s1=1, F1'/F1=0
    grow=p1-1
    for k in range(p1):
        Q0[grow,k]=gA_intf*Li_der[k,0]+Li_val[k,0]*(-gB[0]*DB1[0,0])
        Q1[grow,k]=0
    for kk in range(1,p2e):
        gc=p1+(kk-1)
        Q0[grow,gc]=-gB[0]*DB1[0,kk]
        Q1[grow,gc]=0
    # domain B interior
    for kk in range(1,p2e):
        grow=p1+(kk-1); gk=gB[kk]; gpk=gpB[kk]; Vk=VB[kk]
        for jj in range(1,p2e):
            gc=p1+(jj-1)
            Q0[grow,gc]=gk**2*DB2[kk,jj]+gk*gpk*DB1[kk,jj]
            Q1[grow,gc]=j*2*gk*DB1[kk,jj]
        Q0[grow,grow]-=Vk
        fold0=(gk**2*DB2[kk,0]+gk*gpk*DB1[kk,0])   # F1s1=1
        fold1=j*2*gk*DB1[kk,0]
        for k in range(p1):
            Q0[grow,k]+=fold0*Li_val[k,0]
            Q1[grow,k]+=fold1*Li_val[k,0]
    return Q0,Q1

# =====================================================================
def main():
    t0=time.time()
    out("="*80)
    out("v52 TWO-DOMAIN REFINE - explicit C1 row / ChebU interior wall / L_t scan")
    out("  dps=%d ; independent re-implementation (NO import v51/v50)"%mp.dps)
    out("="*80)
    # --- GR gate A (Leaver) ---
    out(""); out("[GR GATE A] Schwarzschild l=2 n=0 independent Leaver")
    wA=solve_leaver(MPF(0),-2,2,2,0)
    eA=abs(wA-GR_N0)
    out("    w=%.18f%+.18fi"%(wA.real,wA.imag))
    out("    |err|=%.3e digits=%.1f GATE A: %s"%(eA,digs(eA),"PASS" if digs(eA)>=6 else "FAIL"))
    # --- near-wall Frobenius ---
    out(""); out("[NEAR-WALL] extracting U_n ...")
    Ud=nearwall_un(); out("    "+" ".join("U%d=%.3e"%(n,Ud[n].real) for n in (-2,-1,0,1,2)))
    globals()['FROB_A']=frob_series(Ud,16)
    out("    a16=%.3e (Frobenius decay)"%FROB_A[16])

    # --- GR gate B: two-domain assembly on Schwarzschild RW ---
    out(""); out("="*80)
    out("[GR GATE B] SAME two-domain assembly on Schwarzschild RW, reproduce n0")
    out("="*80)
    gr_b_status="NOT RUN"; gr_dig=MPF(0)
    try:
        for (t1s,p1s,p2s,Lts) in [(MPF(2.0),24,36,MPF(30.0)),
                                  (MPF(2.0),32,48,MPF(40.0)),
                                  (MPF(3.0),32,48,MPF(40.0))]:
            Q0g,Q1g=build_gr_two(t1s,p1s,p2s,Lts)
            wz=gep_nearest(Q0g,Q1g,GR_N0)
            eg=abs(wz-GR_N0); dg=digs(eg)
            out("    GR two-dom s1=%.1f p1=%d p2=%d Lt=%.0f  w=%.14f%+.14fi  |err|=%.3e digits=%.2f"%(
                t1s,p1s,p2s,Lts,wz.real,wz.imag,eg,dg))
            gr_dig=max(gr_dig,dg)
        gr_b_status="PASS" if gr_dig>=MPF('11.6') else "FAIL(diag)"
    except Exception as e:
        out("    GR GATE B EXCEPTION: %s"%e); gr_b_status="FAIL(exc)"
    out("    --> GR GATE B: %s (best digits=%.2f)"%(gr_b_status,gr_dig))

    # --- TUFT scans ---
    out(""); out("="*80)
    out("[TUFT] three-way scan: C1 on/off x node_type x L_t")
    out("="*80)
    # R1: C1 on/off (chebu wall)
    out("--- R1 C1 row ON vs OFF (chebu wall, L_t=6, t1=0.15) ---")
    for C1_on in (True,False):
        try:
            Q0,Q1,_,_=build_tuft(MPF('0.15'),32,48,MPF(6.0),C1_on=C1_on,node_type='chebu')
            zb=[r for r in range(Q0.rows) if max(abs(Q1[r,c]) for c in range(Q0.cols))<MPF('1e-60')]
            lamB=beyn_extract(Q0,Q1,ANCHOR,MPF('0.006'),60,seed=3)
            wg=gep_nearest(Q0,Q1,ANCHOR)
            out("    C1_on=%s p1=32 p2=48 Q1zr=%d Beyn=%.12f%+.12fi GEP=%.12f%+.12fi |diff|=%.2e"%(
                C1_on,len(zb),lamB.real,lamB.imag,wg.real,wg.imag,abs(lamB-wg)))
        except Exception as e:
            out("    C1_on=%s FAIL %s"%(C1_on,e))
    # R2: node type chebu vs lobatto (C1 on)
    out("--- R2 wall node chebu vs lobatto (C1 on, L_t=6, t1=0.15) ---")
    for nt in ('chebu','lobatto'):
        try:
            Q0,Q1,_,_=build_tuft(MPF('0.15'),32,48,MPF(6.0),C1_on=True,node_type=nt)
            # wall row residual at anchor
            row0=mp.matrix(1,Q0.rows)
            for c in range(Q0.rows): row0[0,c]=Q0[0,c]+ANCHOR*Q1[0,c]
            lamB=beyn_extract(Q0,Q1,ANCHOR,MPF('0.006'),60,seed=3)
            wg=gep_nearest(Q0,Q1,ANCHOR)
            out("    node=%s Beyn=%.12f%+.12fi GEP=%.12f%+.12fi |diff|=%.2e"%(
                nt,lamB.real,lamB.imag,wg.real,wg.imag,abs(lamB-wg)))
        except Exception as e:
            out("    node=%s FAIL %s"%(nt,e))
    # R3: L_t scan 4/6/8
    out("--- R3 far truncation L_t=4/6/8 (chebu, C1 on, t1=0.15, p1=32 p2=48) ---")
    for Lt in (MPF(4.0),MPF(6.0),MPF(8.0)):
        try:
            Q0,Q1,_,_=build_tuft(MPF('0.15'),32,48,Lt,C1_on=True,node_type='chebu')
            lamB=beyn_extract(Q0,Q1,ANCHOR,MPF('0.006'),60,seed=3)
            wg=gep_nearest(Q0,Q1,ANCHOR)
            # all finite GEP eigenvalues near the spurious 0.44+0.008i
            n=Q0.rows
            An=np.zeros((n,n),dtype=complex); Bn=np.zeros((n,n),dtype=complex)
            for ii in range(n):
                for kk in range(n):
                    An[ii,kk]=complex(Q0[ii,kk]); Bn[ii,kk]=complex(Q1[ii,kk])
            with np.errstate(all='ignore'):
                evall=sp_eig(-An,Bn,check_finite=False)[0]
            spurc=MPC(MPF('0.44'),MPF('0.008'))
            spur=[complex(e) for e in evall if np.isfinite(e.real)
                  and abs(complex(e)-complex(spurc))<MPF('0.03')]
            out("    L_t=%.0f Beyn=%.12f%+.12fi GEP=%.12f%+.12fi |diff|=%.2e near-spur=%s"%(
                Lt,lamB.real,lamB.imag,wg.real,wg.imag,abs(lamB-wg),
                ("%.4f%+.4fi"%(spur[0].real,spur[0].imag)) if spur else "NONE"))
        except Exception as e:
            out("    L_t=%.0f FAIL %s"%(Lt,e))
    # N/p convergence monotonicity (p1 sweep)
    out("--- N/p convergence monotonicity (chebu, C1 on, L_t=6, t1=0.15) ---")
    for p1v in (20,28,36,44):
        try:
            Q0,Q1,_,_=build_tuft(MPF('0.15'),p1v,48,MPF(6.0),C1_on=True,node_type='chebu')
            lamB=beyn_extract(Q0,Q1,ANCHOR,MPF('0.006'),60,seed=3)
            out("    p1=%2d Beyn=%.12f%+.12fi"%(p1v,lamB.real,lamB.imag))
        except Exception as e:
            out("    p1=%2d FAIL %s"%(p1v,e))

    out(""); out("="*80); out("SUMMARY"); out("="*80)
    out("    GR gate A (Leaver) ..... %.2f digits"%digs(eA))
    out("    GR gate B (assembly) ... %s best %.2f digits"%(gr_b_status,gr_dig))
    out("    wall time %.0fs"%(time.time()-t0))
    with open("_audit_v52_twodomain_refine_out.txt","w",encoding="utf-8") as f:
        f.write("\n".join(OUT))

if __name__=="__main__":
    main()
