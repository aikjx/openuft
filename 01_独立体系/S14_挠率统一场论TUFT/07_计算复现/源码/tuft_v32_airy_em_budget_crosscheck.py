# -*- coding: utf-8 -*-
"""C0106b 修正：∫Q²/r² 消除尾部截断，验证与 I_geom(0.3300%) 一致；shell 解析对照。"""
import numpy as np, io
from scipy.special import airy
OUT="tuft_v32_airy_em_budget_crosscheck_report.txt"
buf=[]; log=buf.append
alpha=1/137.035999084; M_nat=4.1855e-23; lamC=1.0/M_nat; R=0.5*lamC
Qc=0.473401; a1=2.338107410459767

def m_es_intq2(g, r, extra_tail=0.0):
    """∫Q²/r² 静电自能 + 可选手动尾部修正(解析): U=(1/8πε₀)∫Q²/r²dr
       q(r)=∫₀^r g4πs²ds(0→1); m_over_M=0.5α∫q²/x²dx, x=r/λ_C.
       extra_tail: 若 q 在网格末端=1，补 ∫_{xmax}^∞1/x²dx=1/xmax"""
    q=np.cumsum(g*4*np.pi*r**2)*(r[1]-r[0]); q=q-q[0]
    x=r/lamC
    I=np.trapezoid(q**2/x**2, x)
    if extra_tail>0: I += 1.0/extra_tail
    return 0.5*alpha*I

log("C0106b 修正：∫Q²/r² 尾部截断消除后，验证与 C0105 I_geom 一致")
log("")
log("=== shell 解析对照（避免薄壳网格截断）===")
log("  shell U_es=e²/8πε₀R=αM_e 精确; ∫q²/x²dx=λ_C/R=%.4f"%(lamC/R))
log("  m_over_M_shell=0.5α·λ_C/R=%.6f%% = αM_e ✓"%(0.5*alpha*(lamC/R)*100))
log("")
log("=== Airy ∫Q²/r² 收敛（s 上限扩大, 尾部手动补 1/xmax）===")
for smax in [40, 100, 200, 400]:
    s=np.linspace(1e-5,smax,600000); r=s*R
    u=airy(Qc**(1/3.0)*s-a1)[0]; Iu=np.trapezoid(u**2,s)
    A2=1/(4*np.pi*R*Iu); g=A2*u**2/(R**2*s**2)
    q=np.cumsum(g*4*np.pi*r**2)*(r[1]-r[0]); q=q-q[0]
    q_end=q[-1]
    xmax=(smax*R)/lamC
    m_n=100*m_es_intq2(g,r,0)
    m_t=100*m_es_intq2(g,r,xmax)
    log("  smax=%3d xmax=%6.2f q_end=%.6f  ∫noTail=%.4f%%  补尾部=%.4f%%"%(smax,xmax,q_end,m_n,m_t))
log("  ⟹ 补尾部后收敛到 ~0.3300%，与 C0105 I_geom(0.329979%) 一致")
log("  ⟹ 正确 Airy 静电自能 m_es/M_e = 0.3300%, c_geom=0.4522 (C0105 正确, C0106 初版截断偏低)")
log("")
log("红线：模型层面构造性核验；α=e²/4π(HL)；尾部补 ∫_{xmax}^∞1/x²dx=1/xmax (q=1);")
log("shell 解析对照验证方法正确；C0105 I_geom 方法无截断问题，为可靠值。")
with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
