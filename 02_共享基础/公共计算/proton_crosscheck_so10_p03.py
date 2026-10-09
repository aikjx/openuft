# -*- coding: utf-8 -*-
# 质子寿命 dim-6 归一 · 跨探针交叉验证（本项目 cross-check）
# E_P03 : p03_gut_2loop_proton_decay.py  C6=1e36 yr, a_ref=0.024
# E_SO10: 07_统一场方程/验证脚本/so10_chain.py  锚 1e29 yr @10^14.6, a0=1/41
import math
C6,a_ref=1.0e36,0.024
def tau_p03(M,a): return C6*(M/1e16)**4*(a_ref/a)**2
t0,M0,a0=1.0e29,10**14.6,1.0/41.0
def tau_anc(M,a): return t0*(M/M0)**4*(a0/a)**2
MX_RATIO=1.0/math.sqrt(2.0)   # so10_chain.py L632: 物理 X 质量 = M_GUT/sqrt(2)（破缺 VEV 约定）
SU5_A=41.0
def tau_exact(M,ai): return t0*((M*MX_RATIO)/M0)**4*(ai/SU5_A)**2
Kp=C6*(1e16**-4)*a_ref**2
Ks=t0*(M0**-4)*a0**2
print("K_P03/K_SO10 = %.2f"%(Kp/Ks))
cases=[("A fermions-only",1.990e17,47.82,2.12e39),
       ("B +bidoublet+triplet",5.298e16,46.35,1.00e37),
       ("C undoubled pair",2.293e16,45.42,3.38e35)]
print("%-22s%11s%8s%12s%12s%11s%12s%8s%8s%8s"%("case","M_GUT","aG^-1","tau_reg","tau_P03","tau_anc","tau_exact","P03/r","anc/r","ex/r"))
for n,M,ai,tr in cases:
    a=1.0/ai; tp=tau_p03(M,a); ts=tau_anc(M,a); te=tau_exact(M,ai)
    print("%-22s%11.3e%8.2f%12.2e%12.2e%11.2e%12.2e%8.1f%8.2f%8.2f"%(n,M,ai,tr,tp,ts,te,tp/tr,ts/tr,te/tr))
SK,HK=2.4e34,1.0e35
def Mp(t,a): return 1e16*((t/C6)*(a/a_ref)**2)**0.25
def Ms(t,a): return M0*((t/t0)*(a/a0)**2)**0.25
def Ms_exact(t,ai):  # so10 登记口径反解 M_GUT（含 mX=M_GUT/sqrt2）
    return (M0/MX_RATIO)*((t/t0)*(SU5_A/ai)**2)**0.25
print("\nM_GUT visible upper limits (tau=threshold):")
for n,M,ai,tr in cases:
    a=1.0/ai
    print("%-22s @HK %9.2e(P03 modern) %9.2e(SU5 anc) %9.2e(so10 exact) | M_GUT=%.2e -> %s/%s/%s"%(
        n,Mp(HK,a),Ms(HK,a),Ms_exact(HK,ai),M,
        "vis" if M<Mp(HK,a) else "INVIS",
        "vis" if M<Ms(HK,a) else "INVIS",
        "vis" if M<Ms_exact(HK,ai) else "INVIS"))
n,M,ai,tr=cases[2]; a=1.0/ai
tp=tau_p03(M,a); ts=tau_anc(M,a)
print("\nC fragility: tau_reg/HK=%.1f ; P03 x%.2f anc x%.2f ; span %.1f"%(
    tr/HK,tp/tr,ts/tr,max(tp,ts)/min(tp,ts)))
print("to reach HK lower M by factor %.2f -> M~%.2e (R3221 residual nonzero there)"%(
    (tr/HK)**0.25, M/(tr/HK)**0.25))
v=246.22; mnu=0.05e-9
for k,mr in (("A",1.299e10),("B",4.880e10),("C",1.127e11)):
    print("see-saw %s M_R=%.3e y_nu=%.2e (y_tau~1e-2)"%(k,mr,math.sqrt(2)*math.sqrt(mnu*mr)/v))
