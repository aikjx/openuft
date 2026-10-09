# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\验证脚本')
import torsion_operator_basis as tb
from fractions import Fraction as F

print("=== raise3 fix check ===")
# 期望：T^{abc} = MET[a]MET[b]MET[c]·T[abc]
T = tb.make_generic_torsion()
U = tb.raise3(T)
ok = all(U[a][b][c] == tb.MET[a]*tb.MET[b]*tb.MET[c]*T[a][b][c] for a in range(4) for b in range(4) for c in range(4))
print("raise3==diag*T?", ok)

print("=== T6 lowered gamma ===")
def antisym3(x,y,z):
    return tb.mscalar(tb.madd(tb.madd(tb.mmul(tb.mmul(tb.GAM[x],tb.GAM[y]),tb.GAM[z]),
                                      tb.mmul(tb.mmul(tb.GAM[y],tb.GAM[z]),tb.GAM[x])),
                              tb.mmul(tb.mmul(tb.GAM[z],tb.GAM[x]),tb.GAM[y])), F(1,6))
def rhs_low(la,mu,nu):
    R=tb.mzero()
    for rho in range(4):
        # 用降指标 γ_ρ = MET[ρ]·γ^ρ
        g_low = tb.mscalar(tb.GAM[rho], tb.MET[rho])
        R=tb.madd(R, tb.mscalar(tb.mmul(tb.G5, g_low), tb.eps_upper(la,mu,nu,rho)))
    return R
for (triple, form) in [((0,1,2),"012"), ((1,2,3),"123")]:
    G=antisym3(*triple); R=rhs_low(*triple)
    # ratio
    cc=None
    for i in range(4):
        for j in range(4):
            if not tb.ceq(R[i][j],tb.Z):
                re=R[i][j][0]; im=R[i][j][1]; den=re*re+im*im
                cc=((G[i][j][0]*re+G[i][j][1]*im)/den,(G[i][j][1]*re-G[i][j][0]*im)/den)
                break
        if cc is not None: break
    print(form, "cc(lowered g)", cc)

print("=== T7 completeness ===")
pairs=tb.basis_pairs()
okcomp=True
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                acc=tb.Z
                for GA,Gup in pairs:
                    acc=tb.cadd(acc, tb.cmul(GA[a][b],Gup[c][d]))
                tgt=(F(4),F(0)) if (a==d and c==b) else tb.Z
                if not tb.ceq(acc,tgt): okcomp=False
print("completeness == 4 δαδ δγβ :", okcomp)

print("=== T7 LL mismatch locations ===")
GPL=[tb.mmul(tb.GAM[m],tb.PL) for m in range(4)]
GlPL=[tb.mmul(tb.g_low(m),tb.PL) for m in range(4)]
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                M=tb.Z; N=tb.Z
                for m in range(4):
                    M=tb.cadd(M, tb.cmul(GPL[m][a][b],GlPL[m][c][d]))
                    N=tb.cadd(N, tb.cmul(GPL[m][a][d],GlPL[m][c][b]))
                if not tb.ceq(M,N):
                    print("LL mismatch at", (a,b,c,d), "M=",M,"N=",N)
