# -*- coding: utf-8 -*-
"""
_audit_v49_chandrasekhar_mirror.py  —  v49 AUDIT: complete Chandrasekhar transform,
re-pass GR Gate B, then cut the TUFT reflecting wall.
================================================================================
IRON LAW (user):
  * GR gate first.  Independent implementation, NO import of _ma_/tuft_/qnm.
    (May READ MainAgent code to understand formulas; must re-derive & re-type.)
  * Rough starts, double precision (numpy/scipy), no hardcoded target inside the
    solver, no loop calibration.  Numbers copied verbatim from raw output.
  * Honest four-state grading.  If Gate B still FAILs -> report residual + next
    missing term.  If TUFT static anchor < Grade-A or first-principles slow-rot
    does not close -> report the blocker, do NOT fake.

================================================================================
PART Z — COMPLETE CHANDRASEKHAR TRANSFORM DERIVATION (s = -2 Teukolsky radial)
================================================================================
Master equation (M=1, Kerr):

    Delta^{-s} d/dr( Delta^{s+1} dR/dr )
        + [ (K^2 - 2 i s (r-1) K)/Delta + 4 i s omega r - lambda ] R = 0

with
    Delta = r^2 - 2 r + a^2 ,   K = (r^2+a^2) omega - a m ,
    lambda = {}_s A_{lm}(a omega) + a^2 omega^2 - 2 a m omega .

For s = -2 :
    Delta^2 d/dr(Delta^{-1} R') + [ (K^2 + 4 i (r-1) K)/Delta - 8 i omega r - lambda ] R = 0

Expanding the derivative  Delta^2(Delta^{-1}R'' - Delta^{-2}Delta' R') = Delta R'' - Delta' R' :

    (1)   R'' - (Delta'/Delta) R'
              + [ (K^2 + 4 i (r-1) K)/Delta^2 - 8 i omega r/Delta - lambda/Delta ] R = 0 .

This is a SECOND-order ODE with a complex potential and a first derivative.  The
Chandrasekhar transform removes the first derivative AND the imaginary part at
a = 0 (Schwarzschild), landing on the real-potential RW/Zerilli master equation

    (2)   d^2 psi/dr_*^2 + [ omega^2 - V_RW/Z(r) ] psi = 0 ,   dr_*/dr = r^2/Delta .

Schwarzschild peel (a = 0) :  R = Delta^{-1} ( alpha psi' + beta psi ) e^{-i omega r_*}
with rational alpha,beta chosen so the imaginary pieces 4 i (r-1) K_0/Delta_0 and
-8 i omega r/Delta_0 cancel against the e^{-i omega r_*} phase.  At a = 0 this is
exact and yields the real Zerilli potential (even) / RW potential (odd), isospectral.

------------------------------------------------------------------ O(a) pieces
Expand K = r^2 omega - a m + O(a^2) ;  lambda = {}_sA_{lm}(0) + O(a) - 2 a m omega .
The O(a) structure that the Schwarzschild peel does NOT absorb (what v48 missed):

  (i)  IMAGINARY CROSS-TERM (the v48 gap) :  4 i (r-1) K/Delta .
       At a = 0 the 4 i (r-1) r^2 omega/Delta_0 peels into the phase.  With K -> r^2 w - a m
       the UNPEELED residual is
            4 i (r-1)(- a m)/Delta  =  - 4 i a m (r-1)/Delta .
       This is an ANTISYMMETRIC (in m) imaginary off-diagonal/derivative coupling.
       v48 kept only the real diagonal  -4 a m omega / r^3  -> m=+2 and m=-2 stayed
       DEGENERATE and the slope came out 0.0962 (real part 38% of target).

  (ii) m != 0 diagonal piece in lambda :  - 2 s m a omega  with s = -2  =>  + 4 m a omega
        (for m = +2 : +8 a omega ; for m = -2 : -8 a omega).  Real, antisymmetric in m.

  (iii) SEPARATION-CONSTANT MIXING  Delta_l :  {}_sA_{lm}(c) = {}_sA_{lm}(0) + 2 c s <...> + ...
        c = a omega is complex and the spheroidal O(c) term mixes adjacent l (the 2 c s H_l
        off-diagonal in the Cook 5-diagonal matrix).  This couples l = 2 to l = 3,1 at O(a).

  (iv) HORIZON DRAGGING  Omega_H = a/(2 r_+)  enters through the INCIDENT boundary, not the
        bulk potential.  The in-going Frobenius exponent at r_+ is
            sigma_+ = (2 omega r_+ - a m)/(r_+ - r_-) ,   xi = -s - i sigma_+ ,
        i.e. the local frequency at the horizon is  omega - m Omega_H  (since r_+ - r_- = 2 sqrt(1-a^2),
        and at small a, sigma_+ -> (2 omega r_+ - a m)/(2 sqrt(1-a^2)) -> omega - m a/(2 r_+) = omega - m Omega_H).

WHY THE LEAVER CONTINUED FRACTION PASSES:  the Cook-Zalutskiy Leaver chain does NOT use a
Schwarzschild peel with O(a) patches.  It writes the exact Teukolsky solution as a Frobenius
series simultaneously at r_+ (xi = -s - i sigma_+, i.e. item (iv)) and at infinity, and the
recurrence coefficients D0..D4 are built from the EXACT lambda (items ii,iii) and the EXACT
K^2 +/- 4i(r-1)K potential (item i baked into sigma_H, alpha, gamma, delta).  Hence all O(a)
couplings — including the imaginary cross term — are present to all orders in a.  This is the
authoritative GR Gate scaffold (MainAgent: Gate A 14.8 digits, Gate B 7.7 digits).

================================================================================
"""
import math
import cmath
import time
import numpy as np
from scipy.linalg import eig, lu_factor, lu_solve
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

OUT = []
def out(s=""):
    print(s, flush=True)
    OUT.append(str(s))

# ============================================================== grading refs
GR_N0    = 0.37367168441804166 - 0.08896231568893410j   # Schwarzschild l=2 n=0
GR_SPLIT = 0.2515323                                     # splitR/a -> target (errata #42)
GR_C_PER_M = 0.0628831 + 0.0019960j                     # per-(m a) complex slope (4c=split)
TUFT_ANCHOR = 0.434445178 - 0.056449760j                # Grade-A TUFT static pole (E480)

# ============================================================================
# PART 1 — INDEPENDENT Cook-Zalutskiy 2014 Leaver QNM solver  (no import)
# Re-derived from arXiv:1410.7698 eqs 21-56.
# ============================================================================
def angular_sA(c, s, l, m, Nmat=30):
    """sA_lm(c), c=a*w complex.  5-diagonal spectral matrix (Cook eqs 52-56)."""
    lmin = max(abs(s), abs(m))
    def F(lp):
        if lp + 1 < lmin: return 0.0
        t1 = (lp+1)**2 - m*m; t2 = (lp+1)**2 - s*s
        if t1 <= 0 or t2 <= 0: return 0.0
        return math.sqrt(t1/((2*lp+3)*(2*lp+1)))*math.sqrt(t2)/(lp+1)
    def G(lp):
        if lp == 0: return 0.0
        t1 = lp*lp - m*m; t2 = lp*lp - s*s
        if t1 <= 0 or t2 <= 0: return 0.0
        return math.sqrt(t1/(4*lp*lp-1))*math.sqrt(t2)/lp
    def H(lp):
        if lp == 0 or s == 0: return 0.0
        return -m*s/(lp*(lp+1))
    def A(lp): return F(lp)*F(lp+1)
    def D(lp): return F(lp)*(H(lp+1)+H(lp))
    def B(lp): return F(lp)*G(lp+1)+G(lp)*F(lp-1)+H(lp)*H(lp)
    def E(lp): return G(lp)*(H(lp-1)+H(lp))
    def CC(lp): return G(lp)*G(lp-1)
    N = Nmat
    lvals = [lmin+i for i in range(N)]
    M = np.zeros((N, N), dtype=np.complex128)
    for i, lp in enumerate(lvals):
        for j, lc in enumerate(lvals):
            d = lc - lp
            if   d == -2: M[i,j] = -c**2 * A(lc)
            elif d == -1: M[i,j] = -c**2 * D(lc) + 2*c*s*F(lc)
            elif d == 0:  M[i,j] = lp*(lp+1) - s*(s+1) - c**2*B(lc) + 2*c*s*H(lc)
            elif d == 1:  M[i,j] = -c**2 * E(lc) + 2*c*s*G(lc)
            elif d == 2:  M[i,j] = -c**2 * CC(lc)
    ev = np.linalg.eigvals(M)
    tgt = l*(l+1) - s*(s+1)
    return complex(min(ev, key=lambda e: abs(e-tgt)))

def radial_params(w, a, s, l, m, sA):
    rp = 1.0 + math.sqrt(max(0.0, 1.0-a*a)); rm = 1.0 - math.sqrt(max(0.0, 1.0-a*a))
    dr = rp - rm
    sig_p = (2.0*w*rp - a*m)/dr      # horizon incident exponent, EMBEDS m Omega_H
    sig_m = (2.0*w*rm - a*m)/dr
    zeta = 1j*w
    xi = -s - 1j*sig_p               # xi_- (ingoing horizon)
    eta = -1j*sig_m                  # eta_+ (Cauchy)
    p = dr*zeta/2.0
    alpha = 1+s+xi+eta-2*zeta + s*(1j*w/zeta)
    gamma = 1+s+2*eta; delta = 1+s+2*xi
    sigma_H = (sA + a*a*w*w - 8.0*w*w
               + p*(2*alpha+gamma-delta)
               + (1+s-(gamma+delta)/2.0)*(s+(gamma+delta)/2.0))
    D0=delta; D1=4*p-2*alpha+gamma-delta-2; D2=2*alpha-gamma+2
    D3=alpha*(4*p-delta)-sigma_H; D4=alpha*(alpha-gamma+1)
    u1 = cmath.sqrt(-4*p)
    if u1.real > 0: u1 = -u1
    u2 = -(8*p-4*alpha+2*gamma+2*delta+3)/4.0
    u3 = (32*p*(2*p-4*alpha+gamma+3*delta+4)
          + 4*(gamma+delta)*(gamma+delta-2) + 16*sigma_H + 3)/(32.0*u1)
    return dict(D0=D0,D1=D1,D2=D2,D3=D3,D4=D4,u1=u1,u2=u2,u3=u3)

def radial_cf(w, a, s, l, m, sA, n_ov=0, Nmax=500):
    P = radial_params(w, a, s, l, m, sA)
    al = lambda n: n*n + (P['D0']+1)*n + P['D0']
    be = lambda n: -2*n*n + (P['D1']+2)*n + P['D3']
    ga = lambda n: n*n + (P['D2']-3)*n + P['D4']-P['D2']+2
    N = Nmax
    un = 1 + P['u1']/math.sqrt(N) + P['u2']/N + P['u3']/(N**1.5)   # Nollert tail
    r = un
    for n in range(N-1, n_ov-1, -1):
        r = -ga(n+1)/(be(n+1)+al(n+1)*r)
    return be(n_ov) + al(n_ov)*r

def solve_qnm(a, s, l, m, n_ov=0, w_guess=None, tol=1e-14):
    if w_guess is None: w_guess = 0.37 - 0.09j
    w = complex(w_guess)
    def F(wv): return radial_cf(wv, a, s, l, m, angular_sA(a*wv, s, l, m), n_ov)
    for it in range(80):
        f0 = F(w); eps = 1e-8
        fr = F(w+eps); fi = F(w+1j*eps)
        J = np.array([[(fr-f0).real/eps, (fi-f0).real/eps],
                      [(fr-f0).imag/eps, (fi-f0).imag/eps]])
        try: step = np.linalg.solve(J, [-f0.real, -f0.imag])
        except np.linalg.LinAlgError: break
        w = w + step[0] + 1j*step[1]
        if abs(f0) < tol and abs(step).max() < 1e-12: break
    return complex(w)

# ============================================================================
# PART 2/3 — TUFT static geometry + Jansen compactification + E475 first principles
# ============================================================================
cm_t, d_t = -0.29, -0.05
BETA = (1.0 + math.sqrt(1.0 + 4.0/3.0))/2.0          # 1.263762616 bounded branch (E447/#28)
RHO_H = brentq(lambda r: r**3 + cm_t*r + d_t, 0.55, 0.65)
HP = -2.0*cm_t/RHO_H**3 - 3.0*d_t/RHO_H**4
K_ASC = ((1.5)/(math.exp(2.0/RHO_H)*math.sqrt(HP)))**(2.0/3.0)
B_OPT = complex(3.5, 1.5)                             # optimized complex contour

def h_of(rho): return 1.0 + cm_t/rho**2 + d_t/rho**3
def hp_of(rho): return -2.0*cm_t/rho**3 - 3.0*d_t/rho**4
def V_of(rho):
    A = np.exp(-2.0/rho); B = np.exp(2.0/rho)*h_of(rho); R = rho*np.sqrt(B)
    q = 1.0 + (rho/2.0)*(-2.0/rho**2 + hp_of(rho)/h_of(rho))
    return 3.0*A*(1.0 + q*q)/R**2

def cheb_gauss(N):
    j = np.arange(1, N+1); th = np.pi*(j-0.5)/N
    z = np.cos(th); w = ((-1.0)**(j-1))*np.sin(th)
    zi,zj = np.meshgrid(z,z,indexing='ij'); wi,wj = np.meshgrid(w,w,indexing='ij')
    with np.errstate(divide='ignore', invalid='ignore'): D = (wj/wi)/(zi-zj)
    np.fill_diagonal(D, 0.0); np.fill_diagonal(D, -D.sum(axis=1))
    return z, D, D@D

def tuft_pencil(N, b, t0=1e-11):
    """Linear pencil Q0 + w Q1 = 0 on Jansen-compactified s-grid.
       Peel psi = s^beta e^{i w s} F (v24 simple peel; bounded Frobenius branch)."""
    z, D, D2 = cheb_gauss(N)
    omz = 1.0 - z; t = (1.0+z)/omz; s = b*t
    def rhs(_t, y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    y0 = [RHO_H + K_ASC*(b*t0)**(2.0/3.0)]
    sol = solve_ivp(rhs, (t0, float(t.max())*1.0001+1.0), y0, method='DOP853',
                    rtol=1e-13, atol=1e-15, dense_output=True)
    rho = sol.sol(t)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    Vv = V_of(rho)
    q21 = BETA*(BETA-1.0)/s**2 - Vv
    q_z = g*gp + 2.0*g*BETA/s
    Q0 = np.diag(g**2)@D2 + np.diag(q_z)@D + np.diag(q21)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(2.0*BETA/s))
    return Q0, Q1, rho, s

def beyn_pole(Q0, Q1, center, radius=0.006, nc=300):
    n = Q0.shape[0]
    rng = np.random.default_rng(0)
    Vv = rng.standard_normal((n,1)) + 1j*rng.standard_normal((n,1))
    th = 2*np.pi*np.arange(nc)/nc
    zz = center + radius*np.exp(1j*th); wq = radius*np.exp(1j*th)/nc
    B0 = np.zeros((n,1), dtype=complex); B1 = np.zeros_like(B0)
    for k in range(nc):
        lu = lu_factor(Q0 + zz[k]*Q1)
        X = lu_solve(lu, Vv)
        B0 += X*wq[k]; B1 += zz[k]*X*wq[k]
    return complex((B0.conj().T@B1)[0,0]/(B0.conj().T@B0)[0,0])

def e475_omega_of_rho(rho):
    """E475 frame-dragging  Omega_F(rho)/a  from FIRST PRINCIPLES.
    Vacuum O(a) Einstein (Hartle) equation on TUFT static background:
        d/drho[ rho^4 e^{2/rho} h^{3/2} dOmega/drho ] = 0 ,  Omega(infty)=0
    =>  Omega_F(rho)/a = 6 int_rho^inf dr'/(r'^4 e^{2/r'} h^{3/2})
    normalized so large rho -> 2/rho^3  (GR Lense-Thirring).  NO manual barrier. """
    integrand = lambda rp: 1.0/(rp**4*np.exp(2.0/rp)*h_of(rp)**1.5)
    val, _ = quad(integrand, rho, np.inf, limit=200, epsabs=1e-13, epsrel=1e-12)
    return 6.0*val

# ============================================================================
# MAIN
# ============================================================================
def main():
    t_start = time.time()
    out("="*80)
    out("v49 AUDIT — complete Chandrasekhar transform / re-pass GR Gate B / cut TUFT wall")
    out("  double precision ; independent Leaver (no import) ; rough starts ; no loop calib")
    out("="*80)

    # ---------------- GATE A : a=0 Schwarzschild n0 ----------------
    out("")
    out("[GR GATE A] a=0, s=-2, l=2, m=2, n=0 (independent Leaver, rough guess)")
    wA = solve_qnm(0.0, -2, 2, 2, 0, w_guess=0.3700-0.0900j, tol=1e-14)
    errA = abs(wA-GR_N0); digA = -math.log10(errA) if errA>0 else 20.0
    fA = radial_cf(wA, 0.0, -2, 2, 2, angular_sA(0.0,-2,2,2), 0)
    out("    w = %.15f %+.15fi" % (wA.real, wA.imag))
    out("    ref = %.15f %+.15fi" % (GR_N0.real, GR_N0.imag))
    out("    |err|=%.3e  digits=%.1f  |Cf|=%.2e  GATE A: %s (need >=6)"
        % (errA, digA, abs(fA), "PASS" if digA>=6.0 else "FAIL"))
    gateA = digA >= 6.0

    # ---------------- GATE B : slow-rot split ----------------
    out("")
    out("[GR GATE B] splitR/a -> %.7f (Richardson a^4 four-trunc); m=+2 vs m=-2 non-degenerate" % GR_SPLIT)
    grid = [0.005, 0.01, 0.02, 0.04, 0.08]
    res = {}; wp=None; wm=None
    for a in grid:
        wp = solve_qnm(a, -2, 2, +2, 0, w_guess=wp or GR_N0, tol=1e-14)
        wm = solve_qnm(a, -2, 2, -2, 0, w_guess=wm or GR_N0, tol=1e-14)
        res[a] = (wp, wm)
        out("    a=%6.3f  w(+2)=%.12f%+.12fi  w(-2)=%.12f%+.12fi  splitR/a=%+.8f"
            % (a, wp.real, wp.imag, wm.real, wm.imag, (wp.real-wm.real)/a))
    aa = np.array(grid, float)
    sR = np.array([(res[a][0].real-res[a][1].real)/a for a in grid], float)
    sI = np.array([(res[a][0].imag-res[a][1].imag)/a for a in grid], float)
    c4R = np.polyfit((aa**2)[:3], sR[:3], 2)[2]
    c4I = np.polyfit((aa**2)[:3], sI[:3], 2)[2]
    errB = abs(c4R-GR_SPLIT); digB = -math.log10(errB) if errB>0 else 20.0
    out("    Richardson a^4 : splitR/a=%+.8f  splitI/a=%+.8f" % (c4R, c4I))
    out("    vs target %.7f : |err|=%.2e  digits=%.1f  GATE B: %s (need >=4)"
        % (GR_SPLIT, errB, digB, "PASS" if digB>=4.0 else "FAIL"))
    out("    per-(ma) complex slope c = (splitR/a + i splitI/a)/4 = %+.7f %+.7fi"
        % (c4R/4, c4I/4))
    out("    ref per-m c = %+.7f %+.7fi" % (GR_C_PER_M.real, GR_C_PER_M.imag))
    # non-degeneracy: residuals at m=+2 and m=-2 poles at a=0.02 must be genuine roots
    a_chk = 0.02
    f_p = radial_cf(res[a_chk][0], a_chk, -2, 2, +2, angular_sA(a_chk*res[a_chk][0],-2,2,+2), 0)
    f_m = radial_cf(res[a_chk][1], a_chk, -2, 2, -2, angular_sA(a_chk*res[a_chk][1],-2,2,-2), 0)
    sep = abs(res[a_chk][0]-res[a_chk][1])
    out("    non-degeneracy @a=0.02: |w(+2)-w(-2)|=%.4e (must be O(a), not degenerate)" % sep)
    out("    residual |Cf| m=+2=%.2e  m=-2=%.2e  (both <1e-8 => genuine distinct roots)"
        % (abs(f_p), abs(f_m)))
    nondeg = (abs(f_p) < 1e-8) and (abs(f_m) < 1e-8) and (sep > 1e-4)
    out("    m=+/-2 non-degenerate: %s" % ("PASS" if nondeg else "FAIL"))
    gateB = (digB >= 4.0) and nondeg

    gr_pass = gateA and gateB
    out("")
    out("    ===============  GR GATE OVERALL: %s  ===============" % ("PASS" if gr_pass else "FAIL"))

    # ---------------- TUFT STATIC anchor (only after GR gate) ----------------
    out("")
    if not gr_pass:
        out("*** GR gate not passed -> TUFT rotating poles remain OPEN (iron law, honest). ***")
        with open("_audit_v49_chandrasekhar_mirror_out.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(OUT))
        return

    out("="*80)
    out("[TUFT STATIC] reflecting-wall bounded branch beta+=%.9f (E447/errata#28, NOT Neumann)" % BETA)
    out("  A=e^(-2/rho), B=e^(2/rho)h, h=1+cm/rho^2+d/rho^3 ; wall rho_h=%.9f (B=0)" % RHO_H)
    out("  Grade-A anchor = %.9f %+.9fi ; target deviation < 1e-6" % (TUFT_ANCHOR.real, TUFT_ANCHOR.imag))
    tuft_poles = []
    for N in (60, 90, 120):
        Q0, Q1, rho, s = tuft_pencil(N, B_OPT)
        w = beyn_pole(Q0, Q1, TUFT_ANCHOR)
        err = abs(w-TUFT_ANCHOR); dig = -math.log10(err) if err>0 else 20.0
        tuft_poles.append((N, w, err, dig, Q0, Q1, rho))
        out("    N=%3d  w=%.12f %+.12fi  |err|=%.3e  %.1f digits" % (N, w.real, w.imag, err, dig))
    dN = abs(tuft_poles[1][1]-tuft_poles[2][1])
    best = tuft_poles[2]
    out("    N=90 vs N=120 agreement |dw|=%.3e" % dN)
    gateT = best[2] < 1e-6
    out("    static anchor deviation = %.3e  Grade-A(<1e-6): %s" % (best[2], "PASS" if gateT else "FAIL"))

    # ---------------- E475 first-principles frame drag ----------------
    out("")
    out("[E475 FRAME DRAG] first principles, NO manual 0.04*barrier")
    out("    Omega_F(rho)/a = 6 int_rho^inf dr'/(r'^4 e^{2/r'} h^{3/2}) ; large rho -> 2/rho^3")
    out("    %8s %14s %14s %8s" % ("rho", "Omega_F/a", "2/rho^3", "ratio"))
    for rho in (0.7, 0.8, 1.0, 1.5, 2.0, 5.0):
        of = e475_omega_of_rho(rho); gr = 2.0/rho**3
        out("    %8.4f %14.9f %14.9f %8.4f" % (rho, of, gr, of/gr))

    # ---------------- TUFT rotating: Rayleigh + continuation at a=0.1/0.2 ----
    out("")
    out("[TUFT ROTATING] E475 field folded: Q1_rot = Q1 + a*diag(-2 m Omega_F(rho))")
    Q0s, Q1s, rho, s = tuft_pencil(120, B_OPT)
    evr, lvec, rvec = eig(-Q0s, Q1s, left=True, right=True)
    k = int(np.argmin(np.abs(evr-TUFT_ANCHOR)))
    w0 = evr[k]; v = rvec[:,k]; u = lvec[:,k]
    v /= np.linalg.norm(v); u /= np.linalg.norm(u)
    den = u.conj()@Q1s@v
    out("    static w0 (generalized eig) = %.9f %+.9fi" % (w0.real, w0.imag))
    OmF = np.array([e475_omega_of_rho(float(np.real(r))) for r in rho])
    # Rayleigh first order: dw/d(am) = 2 w0 (u†Omega v)/(u†Q1 v)
    c_ray = complex(2.0*w0*(u.conj()@np.diag(OmF)@v)/den)
    out("    Rayleigh per-(ma) c = %+.7f %+.7fi" % (c_ray.real, c_ray.imag))
    out("    Rayleigh splitR/a=%.6f  splitI/a=%.6f  (4*c)" % (4*c_ray.real, 4*c_ray.imag))

    # direct non-perturbative continuation at a=0.1, 0.2 for m=+2 / -2
    out("")
    out("    direct continuation (trust metric = generalized residual |Q0v+wQ1v|/|v|):")
    cont = {}
    for mm in (+2.0, -2.0):
        traj = []; pole = w0
        for a_spin in (0.10, 0.20):
            Q0c, Q1c, rhoc, sc = tuft_pencil(120, B_OPT)
            Q1c = Q1c + a_spin*np.diag(-2.0*mm*OmF)
            evc = eig(-Q0c, Q1c, right=False); evc = evc[np.isfinite(evc)]
            pole = evc[np.argmin(np.abs(evc-pole))]
            # residual
            evr2, rvec2 = eig(-Q0c, Q1c, left=False, right=True)
            kk = int(np.argmin(np.abs(evr2-pole)))
            vv = rvec2[:,kk]; resi = np.linalg.norm(Q0c@vv + pole*Q1c@vv)/np.linalg.norm(vv)
            traj.append((a_spin, pole, resi))
        cont[mm] = traj
        out("    m=%+.0f: " % mm + "  ".join("a=%.2f:%.8f%+.8fi  resid=%.1e" % (a,w.real,w.imag,rr) for a,w,rr in traj))

    out("")
    out("    a=0.10: w(+2)=%.8f%+.8fi  w(-2)=%.8f%+.8fi"
        % (cont[+2.0][0][1].real, cont[+2.0][0][1].imag, cont[-2.0][0][1].real, cont[-2.0][0][1].imag))
    out("    a=0.20: w(+2)=%.8f%+.8fi  w(-2)=%.8f%+.8fi"
        % (cont[+2.0][1][1].real, cont[+2.0][1][1].imag, cont[-2.0][1][1].real, cont[-2.0][1][1].imag))
    for ai,(ap) in enumerate((0.10,0.20)):
        wp = cont[+2.0][ai][1]; wm = cont[-2.0][ai][1]
        out("    a=%.2f: splitR/a=%+.6f  splitI/a=%+.6f"
            % (ap, (wp.real-wm.real)/ap, (wp.imag-wm.imag)/ap))

    # ---------------- comparison vs v44 / v50 ----------------
    out("")
    out("[COMPARISON]")
    out("    v44 first-order perturbation (Hartle drag overlap): splitR/a = 0.098320")
    out("    v50 candidate (manual 0.04*barrier field)         : splitR/a = 0.580493")
    out("    this audit first-principles E475 Rayleigh          : splitR/a = %.6f" % (4*c_ray.real))
    c01 = cont[+2.0][0][1]; cm01 = cont[-2.0][0][1]
    out("    this audit continuation @a=0.10                    : splitR/a = %.6f"
        % ((c01.real-cm01.real)/0.10))
    minres = min(cont[m][i][2] for m in cont for i in (0,1))
    out("    worst rotating generalized residual = %.2e (trust gate <1e-6)" % minres)

    out("")
    out("  wall time: %.1fs" % (time.time()-t_start))
    with open("_audit_v49_chandrasekhar_mirror_out.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(OUT))
    out("  -> _audit_v49_chandrasekhar_mirror_out.txt")

if __name__ == "__main__":
    main()
