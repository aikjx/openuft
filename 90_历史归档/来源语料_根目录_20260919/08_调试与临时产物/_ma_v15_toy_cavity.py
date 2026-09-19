# -*- coding: utf-8 -*-
"""
Sensitivity control for the REAL standing-wave IVP engine used on the TUFT wall.
Toy single-sided leaky cavity with KNOWN Fabry-Perot modes:
  psi'(0)=0 (Neumann wall), V=0 for 0<s<L (cavity), V=Vb for L<s<L+Wb
  (finite outer barrier), V=0 beyond. Integrate the REAL standing solution to
  s_max, decompose C+/- , R=C+/C-. Lossless single-port -> |R|=1 but the phase
  must WIND by ~2pi and the Wigner delay tau=d(arg R)/dw must show a tall narrow
  peak at each leaky eigenmode w_n ~ n*pi/L (with small end correction).
L=2.93 (matches TUFT c_m=-0.29 wall->barrier length); expected modes near
  w~pi/L=1.072 (n=1), 2pi/L=2.144 (n=2). If the engine resolves these sharp
features but the real TUFT potential gives a flat phase, the TUFT null is real:
the reflecting core and the curvature barrier do NOT form a resonant cavity.
"""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
def P(*a):print(*a,flush=True)
L=2.93; WB=1.5; VB=3.0; SMAX=L+WB+25.0; DS=0.005
N=int(SMAX/DS); sg=np.arange(N+1)*DS
Vg=np.zeros_like(sg); Vg[(sg>=L)&(sg<=L+WB)]=VB
def toy_R(w):
    psi=1.0; p=0.0; w2=w*w
    for k in range(N):
        a1=w2-Vg[k]; a2=w2-Vg[k+1]
        k1=p; l1=a1*psi
        p2=p+0.5*DS*l1; x2=psi+0.5*DS*k1; k2=p2; l2=a1*x2
        p3=p+0.5*DS*l2; x3=psi+0.5*DS*k2; k3=p3; l3=a1*x3
        p4=p+DS*l3;     x4=psi+DS*k3;     k4=p4; l4=a2*x4
        psi=psi+DS/6*(k1+2*k2+2*k3+k4); p=p+DS/6*(l1+2*l2+2*l3+l4)
    Cp=(psi+p/(1j*w))/2; Cm=(psi-p/(1j*w))/2
    return Cp/Cm
P("Toy leaky cavity: L=%.2f, barrier Vb=%.2f thick %.2f ; FP modes near %.3f(n1), %.3f(n2)"%(
  L,VB,WB,np.pi/L,2*np.pi/L))
ws=np.linspace(0.4,2.6,441)
R=np.array([toy_R(w) for w in ws])
ph=np.unwrap(np.angle(R)); tau=np.gradient(ph,ws)
pk=np.argsort(np.abs(tau))[-6:][::-1]
P("\ntop |tau| peaks (w, tau in M, tau/(2L)):")
seen=[]
for i in pk:
    if all(abs(ws[i]-q)>0.1 for q in seen):
        seen.append(ws[i])
        P("  w=%.4f  tau=%.1f M   tau/2L=%.1f"%(ws[i],tau[i],tau[i]/(2*L)))
P("\nphase samples around the expected n=1 mode 1.072:")
P("  %-7s %-10s %-12s"%("w","arg unw","tau"))
for i in range(len(ws)):
    if abs(ws[i]-1.072)<0.30 and i%4==0:
        P("  %-7.3f %-10.3f %-12.2f"%(ws[i],ph[i],tau[i]))
P("\nVERDICT: a tall narrow tau peak (tau/2L >>1) + ~2pi winding at w~n*pi/L")
P("proves the engine RESOLVES a real wall-cavity resonance. Compare against the")
P("TUFT run whose |tau|/2L stayed <=0.04 with flat phase -> TUFT has no such mode.")
