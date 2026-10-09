# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\验证脚本')
import torsion_operator_basis as tb
from fractions import Fraction as F

print("=== T1 detail ===")
ok_clifford = True
for mu in range(4):
    for nu in range(4):
        antic = tb.madd(tb.mmul(tb.GAM[mu], tb.GAM[nu]), tb.mmul(tb.GAM[nu], tb.GAM[mu]))
        target = tb.mscalar(tb.meye(), 2*tb.MET[mu] if mu == nu else 0)
        if not tb.meq(antic, target):
            ok_clifford = False
            print("clifford FAIL mu", mu, "nu", nu)
print("clifford", ok_clifford)
print("g5^2=I?", tb.meq(tb.mmul(tb.G5, tb.G5), tb.meye()))
print("g5 anticomm?", all(tb.meq(tb.madd(tb.mmul(tb.G5, tb.GAM[mu]), tb.mmul(tb.GAM[mu], tb.G5)), tb.mzero()) for mu in range(4)))
for mu in range(4):
    for nu in range(4):
        tr = tb.mtr(tb.mmul(tb.GAM[mu], tb.GAM[nu]))
        expect = tb.cmul_scalar(tb.cnum(4*tb.MET[mu]), 1) if mu == nu else tb.Z
        print("Tr(g%d g%d)=" % (mu, nu), tr, "expect", expect, "ok", tb.ceq(tr, expect))

print("=== T3 detail ===")
T = tb.make_generic_torsion()
t = tb.torsion_trace(T)
S = tb.torsion_axial(T)
q = tb.torsion_tensor_part(T, t, S)
print("t", t)
print("S", S)
anti = all(q[a][b][c] == -q[a][c][b] for a in range(4) for b in range(4) for c in range(4))
print("q antisym last-two:", anti)
trf = all(sum((tb.MET[a] if a == b else 0)*q[a][b][c] for a in range(4) for b in range(4)) == 0 for c in range(4))
print("q tracefree:", trf)
cyc = all(q[a][b][c] + q[b][c][a] + q[c][a][b] == 0 for a in range(4) for b in range(4) for c in range(4))
print("q cyclic:", cyc)
# reconstruction
rec_ok = True
for a in range(4):
    for b in range(4):
        for c in range(4):
            tp = (F(1,3))*(t[b]*(tb.MET[a] if a == c else 0) - t[c]*(tb.MET[a] if a == b else 0))
            ax = sum((F(-1,6))*tb.eps_index(a,b,c,i)*S[i] for i in range(4))
            if T[a][b][c] != tp + ax + q[a][b][c]:
                rec_ok = False
print("reconstruct:", rec_ok)

print("=== T5 detail ===")
tup = tb.raise3(T)
t2 = sum(tb.MET[i]*t[i]*t[i] for i in range(4))
S2 = sum(tb.MET[i]*S[i]*S[i] for i in range(4))
q2 = tb.full_contract3(q, q)
T2 = sum(T[a][b][c]*tup[a][b][c] for a in range(4) for b in range(4) for c in range(4))
Tcross = sum(T[a][b][c]*tup[b][a][c] for a in range(4) for b in range(4) for c in range(4))
print("t2", t2, "S2", S2, "q2", q2)
print("T2", T2, " claim 2/3t2-1/6S2+q2=", F(2,3)*t2 - F(1,6)*S2 + q2)
print("Tcross", Tcross, " claim -1/3t2-1/12S2-q2=", -F(1,3)*t2 - F(1,12)*S2 - q2)
