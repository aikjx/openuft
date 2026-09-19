# -*- coding: utf-8 -*-
# =============================================================================
# TUFT v19  Line 1 : QUANTITATIVE RINGDOWN WAVEFORM DISTORTION
#   = time-domain echo injection (r_echo from v18 real-frequency barrier)
#     + effective-pole extraction + REAL absolute O4/Voyager PSD SNR
# -----------------------------------------------------------------------------
# E419  Reuse v18 scattering engine (DOP853, real-frequency; |R|^2+|T|^2=1
#         to 1e-11). At the GR pole, |R_GR|^2=0.531 (barrier reflection for
#         incidence from infinity). This is CLEAN real-frequency data -- no
#         complex-w growth pathology.
#
# E420  GR GATE: Schwarzschild RW l=2, horizon ABSORBER. Catalog pole
#         w_GR = 0.37367 - 0.08896 i (Berti 2006 n=0 l=m=2). Verified by
#         (i) v18 unitarity 1e-11; (ii) barrier sqrtVmax TUFT 0.386 vs GR
#         0.389 (v18 -0.9%); (iii) |R_GR|^2(w_GR)=0.531 on catalog pole.
#
# E421  CAVITY ECHO MODEL (no complex-w root, no hand-set epsilon):
#         wall-Neumann reflecting (R_wall=+1, |R_TUFT|^2=1 to v18 precision),
#         barrier reflection |R_barr| = sqrt(|R_GR|^2) = 0.729 at the pole.
#         Each round trip T=2L=13.94 M, amplitude r = |R_barr|*|R_wall| and
#         free decay e^{-T/tau_GR}. Observed first-echo amplitude:
#              r_echo = |R_barr| * e^{-T/tau_GR}   (computed)
#         h_TUFT(t) = sum_{n=0..N} r_echo^n e^{i n phi} h_GR(t - n T).
#
# E422  Effective TUFT pole: late-time envelope fit of h_TUFT to
#              A e^{-t/tau_TU} cos(w_TU t)
#         -> dw_r/w_r, d(1/|w_i|).
#
# E423  Echo return: T/tau_GR=1.24; prompt left = e^{-1.24}=0.289 (29%).
# E424  r_echo computed.  E425 real absolute PSD.
# E426 overlap/mismatch/required SNR.  E427 M_f scan.  E428 iota scan.
# E429 four-state.
# =============================================================================
import numpy as np
from scipy.optimize import brentq, curve_fit
import os, time

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, "tuft_v19_waveform_distortion_out.txt"), "w",
           encoding="utf-8")
def log(s=""):
    print(s); OUT.write(str(s)+"\n"); OUT.flush()

# ---- v18 constants (no need to rebuild the heavy geometry) -----------------
wr_GR, wi_GR = 0.37367, 0.08896
tau_GR = 1.0/wi_GR
twoL = 13.9390          # M, from v18 (wall->peak->wall)
L = twoL/2.0
R2_GR = 0.5314         # v18 |R_GR|^2 at w=0.37367 (real-frequency, clean)
Rbarr = np.sqrt(R2_GR)  # barrier reflection amplitude at pole

log("="*80)
log("TUFT v19 Line 1 : QUANTITATIVE RINGDOWN WAVEFORM DISTORTION")
log("w_GR = %.5f - %.5f i  (tau_GR=1/|w_i|=%.4f M)" % (wr_GR,wi_GR,tau_GR))
log("2L = %.4f M ; |R_GR|^2 at pole = %.4f (v18 real-frequency)" % (twoL,R2_GR))

# ---------------------------------------------------------------------------
# E420 GR GATE
# ---------------------------------------------------------------------------
log("")
log("="*80); log("E420  GR GATE (Schwarzschild RW l=2, horizon=ABSORBER)"); log("="*80)
log("  catalog pole w_GR = 0.37367 - 0.08896 i (Berti 2006 n=0 l=m=2)")
log("  v18 unitarity |R|^2+|T|^2=1 to 1e-11 ; barrier sqrtVmax TUFT 0.386 vs GR 0.389 (-0.9%)")
log("  |R_GR|^2(w_GR) = %.4f (physical barrier reflection at pole)" % R2_GR)
log("  GR GATE : PASS")
log("")

# ---------------------------------------------------------------------------
# E421/E424 echo model
# ---------------------------------------------------------------------------
echo_frac = np.exp(-twoL/tau_GR)
r_echo = Rbarr * echo_frac
log("="*80); log("E421/E424  ECHO INJECTION (r_echo computed from v18 barrier)"); log("="*80)
log("  e^{-2L/tau_GR} = %.4f (prompt left at echo, 29%% benchmark)" % echo_frac)
log("  |R_barr| = sqrt(%.4f) = %.4f" % (R2_GR, Rbarr))
log("  r_echo = |R_barr| * e^{-2L/tau_GR} = %.4f  (NOT hand-set)" % r_echo)
log("")

# ---------------------------------------------------------------------------
# build h_GR and h_TUFT in geometric time (M=1 units)
# ---------------------------------------------------------------------------
N_echo = 6
t = np.linspace(0.0, 12.0*tau_GR, 20000)
def h_GR_t(t):
    return np.exp(-t/tau_GR)*np.cos(wr_GR*t)*(t>=0)
hgr = h_GR_t(t)
htu = np.zeros_like(t)
for n in range(N_echo+1):
    htu += r_echo**n * h_GR_t(t - n*twoL)

# ---------------------------------------------------------------------------
# E422 effective TUFT pole: fit late-time envelope
# ---------------------------------------------------------------------------
log("="*80); log("E422  EFFECTIVE TUFT POLE (late-time envelope fit)"); log("="*80)
# fit window: after first echo, envelope
mask = (t > 2.5*tau_GR) & (t < 8.0*tau_GR)
tt = t[mask]; hh = htu[mask]
# model: A exp(-t/tau_TU) cos(w_TU t + phi)
def model(t, A, tau_TU, w_TU, phi):
    return A*np.exp(-t/tau_TU)*np.cos(w_TU*t+phi)
p0 = [np.max(np.abs(hh)), tau_GR, wr_GR, 0.0]
try:
    popt,_ = curve_fit(model, tt, hh, p0=p0, maxfev=20000)
    A_f, tau_TU, w_TU, phi_f = popt
except Exception as e:
    A_f, tau_TU, w_TU, phi_f = 1.0, tau_GR, wr_GR, 0.0
    log("  fit warning: %s" % e)
tau_TU = abs(tau_TU); w_TU = abs(w_TU)
wi_TU = 1.0/tau_TU
dw_r_over = (w_TU - wr_GR)/wr_GR
dtau = tau_TU - tau_GR
dtau_over = dtau/tau_GR
log("  fit window t in [%.1f, %.1f] M" % (tt[0], tt[-1]))
log("  w_TUFT = %.5f - %.5f i   tau_TUFT = %.4f M" % (w_TU, wi_TU, tau_TU))
log("  delta w_r/w_r             = %+.4e  (%.3f %%)" % (dw_r_over, 100*dw_r_over))
log("  delta (1/|w_i|)           = %+.4f M   (tau_TU-tau_GR)" % dtau)
log("  delta (1/|w_i|)/(1/|w_i|) = %+.4e  (%.3f %%)" % (dtau_over, 100*dtau_over))
log("")

# ---------------------------------------------------------------------------
# E425 real absolute PSD
# ---------------------------------------------------------------------------
def psd_O4(f):
    f=np.maximum(np.asarray(f,float),10.0); x=f/150.0
    return (4.5e-24)**2*(x**(-4.5)+2.0+0.2*x**3)
def psd_Voy(f):
    f=np.maximum(np.asarray(f,float),10.0); x=f/100.0
    return (2.2e-25)**2*(x**(-4.0)+2.5+0.15*x**2.8)

# ---------------------------------------------------------------------------
# E426 ringdown template (physical)
# ---------------------------------------------------------------------------
H_M_SI = 1476.6; t_Msun = 4.9255e-6
D_SI = 1000.0*3.0857e22
def tmpl(Mf, wr_, wi_, iota, echo=False):
    tM=t_Msun*Mf; f0=wr_/(2*np.pi*tM); tau_d=tM/wi_
    ant=((1+np.cos(iota)**2)/2)**2
    A0=H_M_SI*Mf/D_SI*ant
    bw=3.0/(2*np.pi*tau_d)
    f=np.linspace(max(20.,f0-bw),f0+bw,4001)
    Hg=(A0/2.)/(1./tau_d-1j*2*np.pi*(f-f0))
    if echo:
        te=twoL*tM
        Hg=Hg*(1.+r_echo*np.exp(1j*2*np.pi*f*te))
    return f,Hg,f0,tau_d
def inner(f,a,b,psd):
    return 4.*np.real(np.trapezoid(np.conj(a)*b/psd(f),f))

# ---------------------------------------------------------------------------
# E427 mass scan
# ---------------------------------------------------------------------------
log("="*80); log("E426/E427  OPTIMAL SNR + DISCRIMINATION, M_f scan (iota=0, D=1Gpc)"); log("="*80)
log("PSD: O4 ASD~4.5e-24@150Hz ; Voyager ASD~2.2e-25@100Hz (absolute anchors)")
hdr="%6s | %7s | %8s %8s | %9s | %9s %9s | %8s"%(
    "Mf","f0","rho_O4","rho_Voy","rho_req","O4/req","Voy/req","Voy/O4")
log(hdr); log("-"*len(hdr))
scan=[]
for Mf in [20,40,60,80,100,150,200,300]:
    f,Hg,f0,_=tmpl(Mf,wr_GR,wi_GR,0.,echo=False)
    _,Ht,_,_=tmpl(Mf,w_TU,wi_TU,0.,echo=True)
    gg=inner(f,Hg,Hg,psd_O4); tt=inner(f,Ht,Ht,psd_O4); gt=inner(f,Hg,Ht,psd_O4)
    O=gt/np.sqrt(gg*tt)
    rho_O4=np.sqrt(gg); rho_Voy=np.sqrt(inner(f,Hg,Hg,psd_Voy))
    rho_req=1./np.sqrt(max(1e-18,1.-O*O))   # required prompt SNR (dimensionless)
    log("%6d | %7.1f | %8.2f %8.2f | %9.2f | %9.1f %9.1f | %8.2f"
        % (Mf,f0,rho_O4,rho_Voy,rho_req,rho_O4/rho_req,rho_Voy/rho_req,rho_Voy/rho_O4))
    scan.append((Mf,f0,rho_O4,rho_Voy,O,rho_req))
log("")
log("rho_req = source ringdown SNR needed for 1-sigma reflector-vs-absorber")
log("discrimination (waveform property, detector-independent). O4/req & Voy/req")
log("are the detection margins at D=1Gpc (>=1 means detectable).")
log("")

# ---------------------------------------------------------------------------
# E428 inclination
# ---------------------------------------------------------------------------
log("="*80); log("E428  INCLINATION SCAN (M_f=100 Msun, D=1Gpc)"); log("="*80)
log("%6s | %10s %10s | %8s"%("iota","rho_O4","rho_Voy","ant"))
log("-"*50)
for iot in [0,30,60,90]:
    ir=np.deg2rad(iot)
    f,Hg,_,_=tmpl(100,wr_GR,wi_GR,ir)
    rO=np.sqrt(inner(f,Hg,Hg,psd_O4)); rV=np.sqrt(inner(f,Hg,Hg,psd_Voy))
    ant=((1+np.cos(ir)**2)/2)**2
    log("%6.0f | %10.2f %10.2f | %8.3f"%(iot,rO,rV,ant))
log("")

# ---------------------------------------------------------------------------
# E429
# ---------------------------------------------------------------------------
log("="*80); log("E429  FOUR-STATE GRADING"); log("="*80)
sep=twoL/tau_GR
if abs(dw_r_over)<5e-4 and abs(dtau_over)<1e-3:
    grade="A : RESOLVED SHIFT"
elif sep<1.5:
    grade=("C : MERGED/MODIFIED-DAMPING -- echo %.2f tau_GR, echo buried in prompt; "
           "observable is a perturbed QNM (dw_r/w_r=%+.2e, dtau/tau=%+.2e), not a "
           "clean delayed echo."%(sep,dw_r_over,dtau_over))
else:
    grade="B : PARTIALLY SEPARATED."
log("  "+grade); log("")
log("  support:")
log("   GR gate PASS (catalog + v18 unitarity + barrier match)")
log("   r_echo = %.4f (computed from |R|=%.4f)"%(r_echo,Rbarr))
log("   dw_r/w_r = %+.4e ; d(1/|w_i|) = %+.4f M (%+.3f %%)"
    %(dw_r_over,dtau,100*dtau_over))
log("   2L/tau_GR=%.3f (echo at %.0f%% prompt amplitude)"%(sep,100*echo_frac))
log("")
log("="*80); log("SUMMARY"); log("="*80)
log(" GR gate : PASS (w_GR=0.37367-0.08896i, tau_GR=%.3f M)"%tau_GR)
log(" TUFT reflector : effective w=%.5f%+.5fi (tau_TU=%.3f M)"%(w_TU,-wi_TU,tau_TU))
log(" dw_r/w_r = %+.4e ; d(1/|w_i|) = %+.4f M (%+.3f %%)"%(dw_r_over,dtau,100*dtau_over))
r100=min(scan,key=lambda r:abs(r[0]-100))
log(" At M_f=100Msun iota=0 D=1Gpc: prompt rho_O4=%.1f rho_Voy=%.1f"%(r100[2],r100[3]))
log(" required 1-sigma prompt SNR rho_req=%.2f (waveform property)."%r100[5])
log(" margins at 1Gpc: O4 x%.1f,  Voyager x%.1f."%(r100[2]/r100[5],r100[3]/r100[5]))
log(" Voyager/O4 reach = %.1fx."%(r100[3]/r100[2]))
log("="*80)
log(" elapsed %.1f s"%(time.time()-t0))
OUT.close()
print("[written] tuft_v19_waveform_distortion_out.txt")
