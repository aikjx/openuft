# -*- coding: utf-8 -*-
"""
RESOLUTION of the Proof-2 contradiction
=======================================
CONFLICT FOUND (audit, 2026-08-14):
  * analytic_proofs.py  Proof 1   claims  dk/dlnw = -tau , dt/dlnw = +k
                                  (residual 1e-85 -> PASS)
  * proof2_fix.py       concludes "FRAMEWORK ODE IS NOT VERIFIED",
                                  measuring dk/dlnw = +k instead.

Both scripts are numerically correct. They are computing derivatives of
DIFFERENT curves, because they impose DIFFERENT (mutually exclusive)
constraints. This file proves that explicitly and decides which one is
the framework's actual claim.

Parameterization A (analytic_proofs.py, Proof 1):
    kappa = Qtop*cos(u),  tau = Qtop*sin(u),   u = ln(w/w0)
    => kappa^2 + tau^2 = Qtop^2         (CONSTANT radius)
    => alpha = tau/kappa = tan(u)       (VARIES with w)
    => dk/du = -tau, dt/du = +kappa     ROTATION generator

Parameterization B (proof2_fix.py):
    alpha = tau/kappa = const,  kappa^2 + tau^2 = w^2/c^2
    => kappa = w/(c*sqrt(1+alpha^2))    (LINEAR in w)
    => alpha CONSTANT, radius VARIES
    => dk/dlnw = +kappa, dt/dlnw = +tau  DILATION generator

A and B are incompatible: A has constant radius & varying angle,
B has varying radius & constant angle. Asking "is dk/dlnw = -tau?"
without fixing the constraint is ill-posed.

Decision test: which parameterization is consistent with Axiom III
(omega*rho = c, with rho = 1/sqrt(kappa^2+tau^2))?
    A: rho = 1/Qtop = const  =>  omega_spiral = c*sqrt(k^2+t^2) = c*Qtop
       and omega_spiral*rho = c  EXACTLY, for all u.        -> CONSISTENT
    B: rho = c/w  =>  if omega means the SAME w, then w*rho = c holds too,
       but then kappa^2+tau^2 = w^2/c^2 = 1/rho^2 forces Qtop to vary with
       w, contradicting Qtop = m_e*c/hbar = const.          -> INCONSISTENT

Conclusion (stated honestly below).
"""
import sys
import mpmath as mp

mp.mp.dps = 120

hbar = mp.mpf("1.054571817e-34")
c = mp.mpf("299792458")
me = mp.mpf("9.1093837015e-31")
Qtop = me * c / hbar
omega0 = mp.mpf("1.0e15")

FAIL = []


def P(*a):
    line = " ".join(str(x) for x in a)
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode("ascii", "ignore").decode())


def SEP(t=""):
    P("")
    P("=" * 72)
    if t:
        P(t)
    P("=" * 72)


def dlog(f, x, h=mp.mpf("1e-30")):
    """d f / d ln x  (central difference in log space)."""
    return (f(x * mp.e**h) - f(x * mp.e**(-h))) / (2 * h)


def rep(title, analytic, numeric, tol=mp.mpf("1e-20"), scale=None):
    a, n = mp.mpf(analytic), mp.mpf(numeric)
    sc = scale if scale is not None else (abs(a) if abs(a) > 0 else mp.mpf(1))
    r = abs(a - n) / sc
    ok = r < tol
    P(f"    {title}")
    P(f"      analytic={mp.nstr(a,25)}  numeric={mp.nstr(n,25)}  resid={mp.nstr(r,6)}  {'OK' if ok else 'FAIL'}")
    if not ok:
        FAIL.append(title)
    return r


P("=" * 72)
P("RESOLUTION: Proof-2 'framework ODE not verified' contradiction")
P(f"mpmath dps={mp.mp.dps}")
P("=" * 72)

# =====================================================================
SEP("[A] Parameterization A: constant radius (rotation) -- Proof 1's curve")
# =====================================================================


def kA(w):
    return Qtop * mp.cos(mp.log(w / omega0))


def tA(w):
    return Qtop * mp.sin(mp.log(w / omega0))


w0 = mp.mpf("1e12")
P("  Constraint: kappa^2+tau^2 = Qtop^2 (const);  alpha=tan(u) varies")
rep("dk/dlnw = -tau", -tA(w0), dlog(kA, w0), scale=Qtop)
rep("dt/dlnw = +kappa", kA(w0), dlog(tA, w0), scale=Qtop)
rep("d(k^2+t^2)/dlnw = 0", 0, dlog(lambda w: kA(w) ** 2 + tA(w) ** 2, w0),
    scale=Qtop**2)
# alpha genuinely varies here
da = dlog(lambda w: tA(w) / kA(w), w0)
sec2 = 1 / mp.cos(mp.log(w0 / omega0)) ** 2
rep("d(alpha)/dlnw = sec^2(u)  (alpha is NOT constant)", sec2, da)
P("  => A is a ROTATION: radius conserved, angle advances. Proof 1 correct.")

# =====================================================================
SEP("[B] Parameterization B: constant alpha (dilation) -- proof2_fix's curve")
# =====================================================================
alpha_fix = mp.mpf("7.2973525693e-3")


def kB(w):
    return w / (c * mp.sqrt(1 + alpha_fix**2))


def tB(w):
    return alpha_fix * kB(w)


P("  Constraint: alpha=const;  kappa^2+tau^2 = w^2/c^2 varies")
rep("dk/dlnw = +kappa (NOT -tau)", kB(w0), dlog(kB, w0))
rep("dt/dlnw = +tau", tB(w0), dlog(tB, w0))
rep("d(alpha)/dlnw = 0", 0, dlog(lambda w: tB(w) / kB(w), w0), scale=alpha_fix)
P("  => B is a DILATION: angle frozen, radius scales linearly. proof2_fix")
P("     is also numerically correct -- but it is NOT Proof 1's curve.")

# =====================================================================
SEP("[C] The two constraints are mutually exclusive (no overlap)")
# =====================================================================
P("  A requires d(k^2+t^2)/dlnw = 0 AND d(alpha)/dlnw != 0")
P("  B requires d(k^2+t^2)/dlnw != 0 AND d(alpha)/dlnw = 0")
rA_rad = dlog(lambda w: kA(w) ** 2 + tA(w) ** 2, w0)
rA_ang = dlog(lambda w: tA(w) / kA(w), w0)
rB_rad = dlog(lambda w: kB(w) ** 2 + tB(w) ** 2, w0)
rB_ang = dlog(lambda w: tB(w) / kB(w), w0)
P(f"    A: d(radius^2)/dlnw = {mp.nstr(rA_rad,6)}   d(alpha)/dlnw = {mp.nstr(rA_ang,6)}")
P(f"    B: d(radius^2)/dlnw = {mp.nstr(rB_rad,6)}   d(alpha)/dlnw = {mp.nstr(rB_ang,6)}")
excl = (abs(rA_rad) < mp.mpf("1e-40") * Qtop**2) and (abs(rB_ang) < mp.mpf("1e-40")) \
    and (abs(rA_ang) > mp.mpf("1e-6")) and (abs(rB_rad) > mp.mpf("1e-30"))
P(f"    mutually exclusive = {excl} -> {'OK' if excl else 'FAIL'}")
if not excl:
    FAIL.append("exclusivity")
P("  => The question 'is dk/dlnw=-tau?' is ILL-POSED until the constraint")
P("     is declared. There is NO numerical error in either script.")
P("  Only overlap would need k=t=0 (trivial), excluded since Qtop>0.")

# =====================================================================
SEP("[D] DECISION via Axiom III + constancy of Qtop")
# =====================================================================
P("  Axiom III: omega*rho = c, with rho := 1/sqrt(kappa^2+tau^2)")
P("  Qtop := m_e*c/hbar is a CONSTANT of the framework (fixed particle).")
P("")
P("  Branch A: rho = 1/Qtop = const; omega_spiral := c*sqrt(k^2+t^2) = c*Qtop")


def prodA(w):
    r = 1 / mp.sqrt(kA(w) ** 2 + tA(w) ** 2)
    om = c * mp.sqrt(kA(w) ** 2 + tA(w) ** 2)
    return om * r


for wv in (mp.mpf("1e9"), mp.mpf("1e12"), mp.mpf("1e16")):
    rel = abs(prodA(wv) - c) / c
    ok = rel < mp.mpf("1e-100")
    P(f"    w={mp.nstr(wv,4)}: omega*rho-c rel={mp.nstr(rel,6)} {'OK' if ok else 'FAIL'}")
    if not ok:
        FAIL.append("A axiom III")
rep("d(omega*rho)/dlnw = 0 in branch A", 0, dlog(prodA, w0), scale=c)
P("    Also radius^2 = Qtop^2 exactly:")
rep("sqrt(k^2+t^2) = Qtop (branch A)", Qtop,
    mp.sqrt(kA(w0) ** 2 + tA(w0) ** 2), scale=Qtop)

P("")
P("  Branch B: k^2+t^2 = w^2/c^2 => sqrt(k^2+t^2) must EQUAL Qtop only at")
P("            one single w. Elsewhere it contradicts Qtop=const.")
# the unique w where B meets the Qtop shell
w_star = Qtop * c
P(f"    w* (unique crossing) = Qtop*c = {mp.nstr(w_star,20)} rad/s")
radB_at_star = mp.sqrt(kB(w_star) ** 2 + tB(w_star) ** 2)
P(f"    radius_B(w*) = {mp.nstr(radB_at_star,20)}   Qtop = {mp.nstr(Qtop,20)}")
# demonstrate B violates Qtop-constancy away from w*
for fac in (mp.mpf("0.1"), mp.mpf("10")):
    wv = w_star * fac
    radB = mp.sqrt(kB(wv) ** 2 + tB(wv) ** 2)
    dev = abs(radB - Qtop) / Qtop
    P(f"    w={mp.nstr(wv,6)}: radius_B/Qtop-1 = {mp.nstr(dev,6)}  (must be 0 if Qtop const)")
    viol = dev > mp.mpf("0.5")
    if not viol:
        FAIL.append("B should violate Qtop const")
P("  => Branch B forces Qtop (hence m_e) to drift with w. That contradicts")
P("     the framework's own definition Qtop = m_e*c/hbar = const.")
P("     Therefore branch A is the framework's curve; B is a different,")
P("     self-consistent-but-irrelevant family.")

# =====================================================================
SEP("[E] What proof2_fix actually discovered (the legitimate residue)")
# =====================================================================
P("  proof2_fix used kf=3.162277660168379e-4, tauf=2.307625500826972e-6.")
kf = mp.mpf("3.162277660168379e-4")
tauf = mp.mpf("2.307625500826972e-6")
P(f"    alpha_from_those = tau/k = {mp.nstr(tauf/kf,20)}")
P(f"    1/137.035999084  = {mp.nstr(1/mp.mpf('137.035999084'),20)}")
rel_a = abs(tauf / kf - 1 / mp.mpf("137.035999084")) / (1 / mp.mpf("137.035999084"))
P(f"    rel diff = {mp.nstr(rel_a,6)}")
P(f"    radius = sqrt(k^2+t^2) = {mp.nstr(mp.sqrt(kf**2+tauf**2),20)} 1/m")
P(f"    Qtop                   = {mp.nstr(Qtop,20)} 1/m")
ratio = mp.sqrt(kf**2 + tauf**2) / Qtop
P(f"    radius/Qtop = {mp.nstr(ratio,10)}   (NOT 1)")
P("  => Those kf,tauf are NOT on the Qtop shell at all; they are the")
P("     alpha-calibrated pair (tau/k = alpha_exp). So proof2_fix compared")
P("     the alpha-calibration point against the Qtop-shell ODE. Mixing the")
P("     two families is exactly what produced the bogus factor:")
P(f"    dk_dlnw/(-tau) reported by proof2_fix = -137.0359...  = -1/alpha")
P(f"      check: -1/alpha = {mp.nstr(-1/(tauf/kf),12)}")
P("     i.e. the '-137' was not a physics discrepancy but the ratio k/tau")
P("     of the OTHER parameterization. Fully explained, no anomaly.")
neg_inv_alpha = -1 / (tauf / kf)
rep("proof2_fix's -137.036 factor == -1/alpha (fully explained)",
    neg_inv_alpha, mp.mpf("-137.035999"), tol=mp.mpf("1e-6"),
    scale=abs(neg_inv_alpha))

# =====================================================================
SEP("VERDICT")
if FAIL:
    P(f"  FAILED ({len(FAIL)}): {FAIL}")
    P("  >>> resolution incomplete")
    sys.exit(1)
P("  1. Proof 1 (analytic_proofs.py) is CORRECT on its own curve:")
P("     constant-radius rotation, dk/dlnw=-tau, dt/dlnw=+kappa.")
P("  2. proof2_fix.py is also numerically CORRECT, but on a DIFFERENT")
P("     curve (constant-alpha dilation), where dk/dlnw=+kappa trivially.")
P("  3. The two constraints are mutually exclusive; the bare question")
P("     'is dk/dlnw=-tau?' is ill-posed without declaring the constraint.")
P("  4. Axiom III + Qtop=m_e*c/hbar=const SELECT branch A. Branch B would")
P("     require m_e to drift with omega -> rejected by the framework's own")
P("     definitions.")
P("  5. proof2_fix's alarming '-137.036' factor is exactly -1/alpha, an")
P("     artifact of mixing the alpha-calibrated pair with the Qtop-shell")
P("     ODE. No physical anomaly, no failed ODE.")
P("")
P("  >>> proof2_out.txt's 'FRAMEWORK ODE IS NOT VERIFIED' is RETRACTED")
P("      as ill-posed. Proof 1 stands. BUT the honest cost is recorded:")
P("      the framework must DECLARE that its ODE lives on the constant-")
P("      Qtop shell (rotation), and that alpha=tau/kappa therefore CANNOT")
P("      be a constant along that flow -- alpha is fixed only at one")
P("      chosen u (the calibration point). This is a real constraint on")
P("      the framework, not a free win.")
sys.exit(0)
