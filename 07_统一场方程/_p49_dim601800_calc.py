# -*- coding: utf-8 -*-
"""openuft#49 | machine dimensional adjudication for formulae 601-800 (module 5).

Pure standard library. Physical quadruple (M, L, T, Q) with Fraction exponents;
natural-unit mass dimension  mdim = M - L - T  (hbar = c = 1).

Scope: the 11 items registered as [dengji] in
    openuft/07_统一场方程/openuft_49_1000_core_formulae.md  section 三.
No physics claim is invented here: every entry is a dimension computation or a
solution of a dimension-matching equation. Where several minimal repairs exist,
all are enumerated and NONE is selected on the author's behalf.
"""
from fractions import Fraction as F
import json, io, sys

# ---------- dimension algebra ----------
def dmul(a, b):           return tuple(x + y for x, y in zip(a, b))
def ddiv(a, b):           return tuple(x - y for x, y in zip(a, b))
def dpow(a, n):           return tuple(F(n) * x for x in a)
def dsqrt(a):             return tuple(x / F(2) for x in a)
def mdim(a):              return a[0] - a[1] - a[2]
def dstr(a):              return "M^%s L^%s T^%s Q^%s" % tuple(str(x) for x in a)

ZERO = (F(0), F(0), F(0), F(0))
MASS = (F(1), F(0), F(0), F(0))
LEN  = (F(0), F(1), F(0), F(0))
TIME = (F(0), F(0), F(1), F(0))
CHG  = (F(0), F(0), F(0), F(1))

HBAR = (F(1), F(2), F(-1), F(0))     # M L^2 T^-1
CC   = (F(0), F(1), F(-1), F(0))     # L T^-1
GG   = (F(-1), F(3), F(-2), F(0))    # M^-1 L^3 T^-2

ELL_P = dsqrt(ddiv(dmul(HBAR, GG), dpow(CC, 3)))
M_P   = dsqrt(ddiv(dmul(HBAR, CC), GG))
T_P   = dsqrt(ddiv(dmul(HBAR, GG), dpow(CC, 5)))
E_P   = dsqrt(ddiv(dmul(HBAR, dpow(CC, 5)), GG))

KAPPA = ddiv(ZERO, LEN)              # 1/L   curvature scalar
TAU   = ddiv(ZERO, LEN)              # 1/L   torsion scalar
OMEGA = ddiv(ZERO, TIME)             # 1/T   geometric angular frequency
CURV2 = ddiv(ZERO, dpow(LEN, 2))     # 1/L^2 Riemann / Ricci components
LDEN  = ddiv(HBAR, dmul(dpow(LEN, 3), TIME))   # lagrangian density
VOL4  = dpow(LEN, 4)                 # 4-volume / 4-simplex volume
KWAVE = ddiv(ZERO, LEN)              # wave number k
DELTA3 = dpow(LEN, 3)                # delta^(3)(k)

GUARDS = []
FINDINGS = []

def guard(gid, name, got, want):
    ok = (F(got) == F(want))
    GUARDS.append(dict(id=gid, name=name, got=str(F(got)), want=str(F(want)), ok=ok))
    return ok

def finding(fid, formulas, statement, computed, verdict, repairs=None):
    FINDINGS.append(dict(id=fid, formulas=formulas, statement=statement,
                         computed=computed, verdict=verdict,
                         repairs=repairs or []))

# ---------- self-checks (guards) ----------
guard("G1", "mdim(G)", mdim(GG), -2)
guard("G2", "mdim(ell_P)", mdim(ELL_P), -1)
guard("G3", "mdim(m_P)", mdim(M_P), 1)
guard("G4", "mdim(t_P)", mdim(T_P), -1)
guard("G5", "mdim(E_P)", mdim(E_P), 1)
guard("G6", "mdim(L_density) = mdim(hbar/(L^3 T))", mdim(LDEN), 4)
guard("G7", "mdim(kappa^2+tau^2) vs mdim(omega^2)",
      mdim(dmul(KAPPA, KAPPA)), mdim(dmul(OMEGA, OMEGA)))
guard("G8", "mdim(curvature 2-form)", mdim(CURV2), 2)
guard("G9", "mdim(torsion)", mdim(TAU), 1)
guard("G10", "spinor canonical dim: 2*mdim(psi)+1 = 4", 2 * F(3, 2) + 1, 4)
guard("G11", "gauge field: 2*mdim(A)=2 -> mdim(A)", 4 - 2, 2)
guard("G12", "delta^(3)(k) mass dim", mdim(DELTA3), -3)

# ---------- F1 : 612 parameter vector ----------
vec = [("alpha", 0), ("alpha_s(M_Z)", 0), ("sin^2 theta_W", 0), ("m_e", 1),
       ("m_u", 1), ("m_d", 1), ("m_tau", 1), ("m_t", 1), ("tau_0", 1),
       ("omega_0", 1), ("alpha", 0)]
names = [v[0] for v in vec]
dup = sorted({n for n in names if names.count(n) > 1})
finding("F1", "612", "parameter vector mixes dimensionless and mass-dim-1 entries",
        "entries=11 unique=10; dimensionless=4 mass-dim-1=7; duplicated name(s)=%s" % (dup or "none"),
        "BOUNDARY", ["口径登记：向量本身非方程，无齐次性要求；重复项 alpha 由作者裁定是否为笔误"])

# ---------- F2 : 662 torsion PN phase ----------
md_tau0, md_Mbh = mdim(TAU), mdim(MASS)
n_solve = -md_tau0 / md_Mbh
finding("F2", "662", "Delta Phi_tau ~ tau_0 * M^n must be dimensionless",
        "mdim(tau_0)=%d, mdim(M)=%d => 1+n=0 => n=%s" % (md_tau0, md_Mbh, n_solve),
        "FAIL(as written)", ["CORRECTED: n = -1, i.e. Delta Phi_tau ~ tau_0 / M",
                             "or declare an extra scale: Delta Phi_tau ~ tau_0 M^n / Lambda^(n+1)"])

# ---------- F3 : 682 three-point function ----------
md_Rk = mdim(KWAVE) * -3            # R(k) = Fourier of dimensionless R(x): L^3
md_3pt = 3 * md_Rk
md_B = md_3pt - mdim(DELTA3)
md_P = 2 * md_Rk - mdim(DELTA3)
finding("F3", "680/682", "bispectrum / power spectrum dimension under Fourier convention",
        "mdim(R(k))=%d ; <RRR>=%d ; delta^(3)=%d => mdim(B_R)=%d ; mdim(P_R)=%d"
        % (md_Rk, md_3pt, mdim(DELTA3), md_B, md_P),
        "PASS(internal consistency)",
        ["登记解除条件：须显式声明 Fourier 约定 R(k)=int d^3x e^{-ikx} R(x)"])

# ---------- F4 : 645 / 751 densities depend on parameterisation ----------
finding("F4", "645/751", "posterior density and parameter-space volume",
        "dimensionless theta => mdim(P(theta|D))=0, mdim(Omega)=0; with dimensionful theta_i of mdim d_i: "
        "mdim(P) = -Sigma d_i",
        "BOUNDARY", ["无参数化声明则不可裁定；属常规约定，备查"])

# ---------- F5 : 701 / 703 amplitude & propagator normalisation ----------
md_prop = -2 * mdim(TAU)                    # <T T> for canonical dim-1 field
finding("F5", "701/703", "2->2 amplitude and torsion propagator normalisation",
        "standard convention S = 1 + i(2pi)^4 delta^(4)(sum p) M => mdim(M)=0 ; "
        "canonical kinetic (dT)^2 => mdim(T)=1 => mdim(D_T) = %d" % md_prop,
        "BOUNDARY", ["登记解除条件：作者须声明振幅归一化；标准口径下 [M]=M^0, [D_T]=M^-2"])

# ---------- F6 : 710 / 712 / 713 topological term ----------
md_TR = mdim(TAU) + mdim(CURV2)
need_xi = mdim(LDEN) - md_TR
md_TT = 2 * mdim(TAU)
finding("F6", "710/712/713", "L_top = zeta*P + xi*(T wedge R)",
        "mdim(P)=%d ; mdim(T wedge R)=%d ; required %d => mdim(zeta)=0, mdim(xi)=%d"
        % (mdim(CURV2) * 2, md_TR, mdim(LDEN), need_xi),
        "FAIL(dimensionless xi as written)",
        ["repair-a: xi -> xi_hat * m_P  (xi_hat dimensionless; +0 new constants but m_P enters explicitly)",
         "repair-b: replace by Nieh-Yan form T^a wedge T_a - R_ab wedge e^a wedge e^b "
         "(mdim=%d, coefficient mdim=%d, e.g. m_P^2)" % (md_TT, mdim(LDEN) - md_TT),
         "repair-c: keep T wedge R and declare xi dimensionful (mdim=1)"])
finding("F6b", "713", "zeta, xi declared dimensionless",
        "conflicts with F6 (difference of one mass power)",
        "FAIL(conditional: fails only if 712 keeps T wedge R)")

# ---------- F7 : 728 / 729 operator dimension ----------
md_psibarpsi = 2 * F(3, 2)
d1 = md_psibarpsi + mdim(CURV2)
d2 = md_psibarpsi + mdim(TAU)
finding("F7", "728/729", "'6-dim / 8-dim' labels vs mass-dimension counting of 727",
        "mdim(psi-bar psi)=%s ; operator-1 = %s + %d = %s ; operator-2 = %s + %d = %s"
        % (md_psibarpsi, md_psibarpsi, mdim(CURV2), d1, md_psibarpsi, mdim(TAU), d2),
        "MISMATCH(口径冲突)",
        ["mass-dimension counting gives 5 and 4, not 6 and 8",
         "'6 / 8' equals the index count (3+3 / 3+3+2); the two counting rules must not be mixed in one section"])

# ---------- F8 : 734 unitarity bound ----------
gap = mdim(dpow(MASS, 2)) - 0
finding("F8", "734", "|M|^2 < 16 pi s",
        "mdim(|M|^2)=0 (standard 2->2 normalisation) ; mdim(16 pi s)=%d => mismatch %d"
        % (mdim(dpow(MASS, 2)), gap),
        "FAIL(as written)",
        ["rewrite in dimensionless form: partial wave |a_l| <= 1 (or |M|^2 <= 16 pi after partial-wave normalisation)",
         "or declare the amplitude normalisation explicitly"])

# ---------- F9 : 772 Regge action ----------
md_V4 = mdim(VOL4)
finding("F9", "772/773", "S_R^UFT = S_R + sum f(kappa,tau,omega) V_simplex",
        "mdim(S_R)=0 ; mdim(V_simplex)=%d => mdim(f) = %d" % (md_V4, -md_V4),
        "PASS(conditional)",
        ["f = omega^4  (mdim 4) OK", "f = (kappa^2+tau^2)^2 = omega^4 (mdim 4) OK",
         "f = kappa^2 + tau^2 (mdim 2) NOT OK"])

# ---------- F10 : 793 Breit-Wigner ----------
md_inv_k2 = -2 * mdim(KWAVE)
finding("F10", "793", "sigma_res ~ Gamma^2 / ((E-E_res)^2 + Gamma^2/4)",
        "mdim(sigma)=%d ; RHS as written=%d => deficit %d ; 1/k^2 supplies %d"
        % (-2, 0, -2, md_inv_k2),
        "CORRECTED",
        ["sigma_res ~ (1/k^2) * Gamma^2 / ((E-E_res)^2 + Gamma^2/4)  (relativistic: 4 pi (2l+1)/k^2 ...)"])

# ---------- F11 : 689 symbol ledger ----------
finding("F11", "689", "omega = vorticity vs omega = UFT geometric angular frequency",
        "both have mdim=%d ; the Raychaudhuri terms sigma^2, omega^2 are homogeneously mdim=%d"
        % (mdim(OMEGA), mdim(dmul(OMEGA, OMEGA))),
        "BOUNDARY(符号台账)",
        ["no dimensional defect; cross-chapter citation must declare which omega"])

# ---------- emit ----------
n_pass = sum(1 for f in FINDINGS if f["verdict"].startswith("PASS"))
n_fail = sum(1 for f in FINDINGS if f["verdict"].startswith("FAIL"))
n_corr = sum(1 for f in FINDINGS if f["verdict"].startswith("CORRECTED"))
n_mis  = sum(1 for f in FINDINGS if f["verdict"].startswith("MISMATCH"))
n_bnd  = sum(1 for f in FINDINGS if f["verdict"].startswith("BOUNDARY"))
guard_ok = sum(1 for g in GUARDS if g["ok"])

out = dict(
    artifact="openuft_49_1000_core_formulae.md",
    interval="601-800",
    method="Fraction quadruple (M,L,T,Q); mdim = M - L - T",
    guards=GUARDS, guards_ok=guard_ok, guards_total=len(GUARDS),
    findings=FINDINGS,
    counts=dict(PASS=n_pass, FAIL=n_fail, CORRECTED=n_corr, MISMATCH=n_mis, BOUNDARY=n_bnd),
)
with io.open("_p49_dim601800_data.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)

lines = []
lines.append("openuft#49 dimensional adjudication 601-800")
lines.append("guards: %d/%d" % (guard_ok, len(GUARDS)))
for g in GUARDS:
    lines.append("  [%s] %-45s got=%s want=%s" % ("OK" if g["ok"] else "BAD", g["name"], g["got"], g["want"]))
lines.append("")
lines.append("counts: PASS=%d FAIL=%d CORRECTED=%d MISMATCH=%d BOUNDARY=%d" % (n_pass, n_fail, n_corr, n_mis, n_bnd))
lines.append("")
for f in FINDINGS:
    lines.append("%-5s %-12s %s" % (f["id"], f["formulas"], f["verdict"]))
    lines.append("      stmt: %s" % f["statement"])
    lines.append("      calc: %s" % f["computed"])
    for r in f["repairs"]:
        lines.append("      fix : %s" % r)
    lines.append("")
txt = "\n".join(lines)
with io.open("_p49_dim601800_out.txt", "w", encoding="utf-8") as fh:
    fh.write(txt)
sys.stdout.write("guards %d/%d ; findings %d ; exit 0\n" % (guard_ok, len(GUARDS), len(FINDINGS)))
sys.exit(0)
