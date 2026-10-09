# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\验证脚本')
import torsion_operator_basis as tb
from fractions import Fraction as F

print("=== T4 ===")
T = tb.make_generic_torsion()
K = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
for lam in range(4):
    for mu in range(4):
        for nu in range(4):
            K[lam][mu][nu] = F(1,2)*(T[lam][mu][nu]+T[mu][lam][nu]-T[nu][lam][mu])
def raise_first(M):
    return [[[sum(tb.MET[a]*M[a][mu][nu] for a in range(4) if a==lam)
              for nu in range(4)] for mu in range(4)] for lam in range(4)]
K1 = raise_first(K); T1 = raise_first(T)
ok_rt = all(T1[la][mu][nu] == K1[la][mu][nu]-K1[la][nu][mu] for la in range(4) for mu in range(4) for nu in range(4))
print("roundtrip:", ok_rt)
t = tb.torsion_trace(T)
Ktr = [sum(K1[a][a][mu] for a in range(4)) for mu in range(4)]
print("t:", t)
print("Ktr:", Ktr)
print("trace rel:", all(t[mu]==Ktr[mu] for mu in range(4)))

print("=== T5 ===")
def inv(T_):
    t_=tb.torsion_trace(T_); S_=tb.torsion_axial(T_); q_=tb.torsion_tensor_part(T_,t_,S_)
    U=tb.raise3(T_)
    t2=sum(tb.MET[i]*t_[i]*t_[i] for i in range(4))
    S2=sum(tb.MET[i]*S_[i]*S_[i] for i in range(4))
    q2=tb.full_contract3(q_,q_)
    T2=sum(T_[a][b][c]*U[a][b][c] for a in range(4) for b in range(4) for c in range(4))
    return t2,S2,q2,T2
for name,gen in [("g1",tb.make_generic_torsion),("g2",tb.make_generic_torsion2),("g3",tb.make_generic_torsion3)]:
    t2,S2,q2,T2 = inv(gen())
    print(name, "T2=",T2," 2/3t2-1/6S2+q2=",F(2,3)*t2-F(1,6)*S2+q2, "match", T2==F(2,3)*t2-F(1,6)*S2+q2)

print("=== T6 ===")
def antisym3(x,y,z):
    return tb.mscalar(tb.madd(tb.madd(tb.mmul(tb.mmul(tb.GAM[x],tb.GAM[y]),tb.GAM[z]),
                                      tb.mmul(tb.mmul(tb.GAM[y],tb.GAM[z]),tb.GAM[x])),
                              tb.mmul(tb.mmul(tb.GAM[z],tb.GAM[x]),tb.GAM[y])), F(1,6))
def rhs_g(la,mu,nu):
    R=tb.mzero()
    for rho in range(4):
        R=tb.madd(R, tb.mscalar(tb.mmul(tb.G5,tb.GAM[rho]), tb.eps_upper(la,mu,nu,rho)))
    return R
G0=antisym3(0,1,2); R0=rhs_g(0,1,2)
print("Gam012 nonzero?", any(not tb.ceq(G0[i][j],tb.Z) for i in range(4) for j in range(4)))
print("Rhs012 nonzero?", any(not tb.ceq(R0[i][j],tb.Z) for i in range(4) for j in range(4)))
# ratio
cc=None
for i in range(4):
    for j in range(4):
        if not tb.ceq(R0[i][j],tb.Z):
            re=R0[i][j][0]; im=R0[i][j][1]; den=re*re+im*im
            cc=((G0[i][j][0]*re+G0[i][j][1]*im)/den,(G0[i][j][1]*re-G0[i][j][0]*im)/den)
            break
    if cc is not None: break
print("cc:", cc)
okuni=True
for la in range(4):
    for mu in range(4):
        for nu in range(4):
            if la==mu or mu==nu or la==nu: continue
            if not tb.meq(antisym3(la,mu,nu), tb.mscalar(rhs_g(la,mu,nu),cc)):
                okuni=False; print("mismatch",la,mu,nu)
print("c uniform:", okuni)

print("=== T7 LL self-Fierz ===")
GPL=[tb.mmul(tb.GAM[m],tb.PL) for m in range(4)]
GlPL=[tb.mmul(tb.g_low(m),tb.PL) for m in range(4)]
mism=0
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                M=tb.Z; N=tb.Z
                for m in range(4):
                    M=tb.cadd(M, tb.cmul(GPL[m][a][b],GlPL[m][c][d]))
                    N=tb.cadd(N, tb.cmul(GPL[m][a][d],GlPL[m][c][b]))
                if not tb.ceq(M,N): mism+=1
print("LL mismatches:", mism)
