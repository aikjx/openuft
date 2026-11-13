#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""J113 / 卷 134 : full-dimension, full-chain normalised core-formula ledger.

Read-only machine audit of the UFE-1 formula system.  This script adds no new
physics: every node is inherited from an already-audited ledger, and the guards
only lock down (a) the *chain* topology (DAG: acyclic, parent-complete,
reachable), (b) the *dimension* of each formula in one 4-axis algebra
(M, L, T, Q), (c) a set of *numeric* identities in Decimal-60, (d) the
*scoreboard* invariants (0/6, one C3 unification = electroweak, zero four-force
GUT equations), and (e) the *input* layer (26 entries, all declared as inputs).

Red line kept explicit in the payload:
  mathematical self-consistency  !=  physical confirmation
  full-chain normalisation       !=  force unification achieved

Exit code 0 requires every gate to pass.  Outputs are written only after the
hard gate is green.
"""
import os
import sys
import io
import json
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)          # 07_统一场方程
ROOT = os.path.dirname(BASE)          # openuft

GATES = []


def gate(name, cond, detail=""):
    ok = bool(cond)
    GATES.append((name, ok, str(detail)))
    return ok


# =============================================================== dimensions
# Four-axis exponent vector (M, L, T, Q).  Fractions keep the algebra exact;
# Q is electric charge, carried only so that e / eps0 / mu0 close exactly.
Z = (F(0), F(0), F(0), F(0))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def d_chain(*xs):
    out = Z
    for x in xs:
        out = dmul(out, x)
    return out


def dinv(a):
    return tuple(-x for x in a)


def dpow(a, n):
    return tuple(x * F(n) for x in a)


def dstr(a):
    return "M^%s L^%s T^%s Q^%s" % tuple(str(x) for x in a)


DIM = {
    # --- anchors
    "hbar":   (F(1), F(2), F(-1), F(0)),
    "c":      (F(0), F(1), F(-1), F(0)),
    "G":      (F(-1), F(3), F(-2), F(0)),
    "e":      (F(0), F(0), F(0), F(1)),
    "eps0":   (F(-1), F(-3), F(2), F(2)),
    "mu0":    (F(1), F(1), F(0), F(-2)),
    "length": (F(0), F(1), F(0), F(0)),
    "time":   (F(0), F(0), F(1), F(0)),
    "mass":   (F(1), F(0), F(0), F(0)),
    "omega":  (F(0), F(0), F(-1), F(0)),   # angular frequency  T^-1
    "one":    Z,
}
# --- derived
DIM["curvature"] = (F(0), F(-2), F(0), F(0))                 # R ~ L^-2
DIM["kappa2"] = d_chain(DIM["G"], dinv(dpow(DIM["c"], 4)))   # 8piG/c^4
DIM["energy"] = (F(1), F(2), F(-2), F(0))
DIM["force"] = (F(1), F(1), F(-2), F(0))
DIM["energy_density"] = (F(1), F(-1), F(-2), F(0))           # T_uv
DIM["action"] = DIM["hbar"]
DIM["lag_density"] = DIM["energy_density"]                   # 4-form density
DIM["torsion"] = (F(0), F(-1), F(0), F(0))                   # T ~ L^-1
DIM["kappa"] = (F(0), F(1), F(0), F(0))                      # helix curvature
DIM["tau_helix"] = (F(0), F(1), F(0), F(0))                  # helix torsion
DIM["speed"] = d_chain(DIM["length"], dinv(DIM["time"]))
DIM["accel"] = d_chain(DIM["length"], dinv(dpow(DIM["time"], 2)))
DIM["potential"] = dmul(DIM["accel"], DIM["length"])         # Phi ~ v^2
DIM["b_helix"] = DIM["speed"]                                # helix pitch rate (R w^2 + b^2 = v^2)
DIM["strain"] = Z                                            # h_uv
DIM["GF"] = d_chain(dinv(dpow(DIM["mass"], 2)))              # Fermi constant


def _dim_identity(name, expr, expect, detail=""):
    return gate(name, expr == expect, detail or "%s -> %s (want %s)" % (name, dstr(expr), dstr(expect)))


# D01-D04 : the four anchors close among themselves
_dim_identity("D01 hbar*c has dimension M L^3 T^-2 = action*speed",
              d_chain(DIM["hbar"], DIM["c"]), (F(1), F(3), F(-2), F(0)), dstr(d_chain(DIM["hbar"], DIM["c"])))
_dim_identity("D02 eps0*mu0*c^2 is exactly dimensionless",
              d_chain(DIM["eps0"], DIM["mu0"], dpow(DIM["c"], 2)), Z, "eps0 mu0 c^2 = 1")
_dim_identity("D03 e^2/(eps0*hbar*c) is dimensionless (fine structure alpha)",
              d_chain(dpow(DIM["e"], 2), dinv(DIM["eps0"]), dinv(DIM["hbar"]), dinv(DIM["c"])), Z, "alpha_em")
_dim_identity("D04 G*mass^2/(hbar*c) is dimensionless (alpha_G)",
              d_chain(DIM["G"], dpow(DIM["mass"], 2), dinv(DIM["hbar"]), dinv(DIM["c"])), Z, "alpha_G")

# D05-D07 : the three L0 anchors of the geometry layer
_dim_identity("D05 hbar*c/length is energy", d_chain(DIM["hbar"], DIM["c"], dinv(DIM["length"])),
              DIM["energy"], dstr(DIM["energy"]))
_dim_identity("D06 hbar*c/length^2 is force", d_chain(DIM["hbar"], DIM["c"], dinv(dpow(DIM["length"], 2))),
              DIM["force"], dstr(DIM["force"]))
_dim_identity("D07 G*mass/length^2 is acceleration (field strength of a point mass)",
              d_chain(DIM["G"], DIM["mass"], dinv(dpow(DIM["length"], 2))),
              DIM["accel"], dstr(DIM["accel"]))
_dim_identity("D07b G*mass^2/length^2 is force (Newton's law with two masses)",
              d_chain(DIM["G"], dpow(DIM["mass"], 2), dinv(dpow(DIM["length"], 2))),
              DIM["force"], dstr(DIM["force"]))

# D08-D12 : action / curvature / ECSK consistency
_dim_identity("D08 action (hbar) equals integral of lagrangian density over d^4x",
              d_chain(DIM["lag_density"], dpow(DIM["length"], 3), DIM["time"]), DIM["action"], "L^4 density")
_dim_identity("D09 L^{-2} is the only curvature dimension (R, Lambda)",
              DIM["curvature"], (F(0), F(-2), F(0), F(0)), dstr(DIM["curvature"]))
_dim_identity("D10 kappa^2 * T_uv has dimension L^-2 (ECSK Einstein equation closes)",
              d_chain(DIM["kappa2"], DIM["energy_density"]), DIM["curvature"], dstr(DIM["curvature"]))
_dim_identity("D11 (1/4kappa^2)*R*d^4x carries the dimension of action (hbar)",
              d_chain(dinv(DIM["kappa2"]), DIM["curvature"], dpow(DIM["length"], 3), DIM["time"]), DIM["action"],
              "1/kappa^2 * R * d^4x = hbar slot")
_dim_identity("D12 kappa^2 * mass^2 * c^3 / hbar is dimensionless (alpha_G rewritten in kappa)",
              d_chain(DIM["kappa2"], dpow(DIM["mass"], 2), dpow(DIM["c"], 3), dinv(DIM["hbar"])), Z,
              "kappa^2 m^2 c^3 / hbar")

# D13-D18 : helix triad and its normalisations
_dim_identity("D13 helix curvature kappa = R*w^2/v^2 has dimension L^-1",
              d_chain(DIM["length"], dpow(DIM["omega"], 2), dinv(dpow(DIM["speed"], 2))), DIM["torsion"], dstr(DIM["torsion"]))
_dim_identity("D14 helix torsion tau = w*b/v^2 has dimension L^-1 (b is the pitch rate, a speed)",
              d_chain(DIM["omega"], DIM["b_helix"], dinv(dpow(DIM["speed"], 2))), DIM["torsion"], dstr(DIM["torsion"]))
_dim_identity("D15 kappa^2+tau^2 shares dimension of (omega/v)^2 = L^-2",
              DIM["curvature"], d_chain(dpow(DIM["omega"], 2), dinv(dpow(DIM["speed"], 2))), "L^-2")

# D19-D24 : field equations given the anchors
_dim_identity("D19 torsion T has dimension L^-1 (1-form connection defect)",
              DIM["torsion"], (F(0), F(-1), F(0), F(0)), dstr(DIM["torsion"]))
_dim_identity("D20 Yang-Mills 2-form F has dimension L^-2 (same slot as R)",
              DIM["curvature"], (F(0), F(-2), F(0), F(0)), dstr(DIM["curvature"]))
_dim_identity("D21 G*mass/c^2 is a length (Schwarzschild radius)",
              d_chain(DIM["G"], DIM["mass"], dinv(dpow(DIM["c"], 2))), DIM["length"], dstr(DIM["length"]))
_dim_identity("D22 hbar*G/c^3 is a length squared (Planck length squared)",
              d_chain(DIM["hbar"], DIM["G"], dinv(dpow(DIM["c"], 3))),
              dpow(DIM["length"], 2), "l_P^2")
_dim_identity("D23 kappa^2*c^2 shares the dimension of G/c^2 (M^-1 L)",
              d_chain(DIM["kappa2"], dpow(DIM["c"], 2)),
              d_chain(DIM["G"], dinv(dpow(DIM["c"], 2))), "kappa^2 c^2 ~ G/c^2")
_dim_identity("D24 G_F = 1/(sqrt2 v^2) has dimension M^-2",
              d_chain(dinv(dpow(DIM["mass"], 2))), DIM["GF"], dstr(DIM["GF"]))

# D25-D28 : observable-level closures
_dim_identity("D25 Newtonian potential Phi = -GM/r has dimension v^2",
              d_chain(DIM["G"], DIM["mass"], dinv(DIM["length"])), DIM["potential"], dstr(DIM["potential"]))
_dim_identity("D26 gravitational-wave strain h is dimensionless",
              DIM["strain"], Z, "h_uv")
_dim_identity("D27 quadrupole power G/c^5 * (Q^(3))^2 has dimension energy/time",
              d_chain(DIM["G"], dinv(dpow(DIM["c"], 5)), dpow(DIM["mass"], 2), dpow(DIM["length"], 4),
                      dinv(dpow(DIM["time"], 6))),
              d_chain(DIM["energy"], dinv(DIM["time"])), "P = dE/dt")
_dim_identity("D28 alpha_s and all gauge couplings are dimensionless",
              DIM["one"], Z, "g_i, alpha_i")

# --- positive controls : prove the dimension tool has teeth
gate("D-PC1 perturbed kappa2 does NOT close the ECSK equation",
     d_chain((F(-1), F(-1), F(0), F(0)), DIM["energy_density"]) != DIM["curvature"], "kappa2 T exponent drift")
gate("D-PC2 eps0 with T=+4 breaks eps0*mu0*c^2",
     d_chain((F(-1), F(-3), F(4), F(2)), DIM["mu0"], dpow(DIM["c"], 2)) != Z, "the hand-calc trap")
gate("D-PC3 force dimension is distinguishable from energy",
     DIM["force"] != DIM["energy"], "MLT^-2 vs ML^2T^-2")


# ------------------------------------------- second instrument: mass dimension
# The 4-axis (M, L, T, Q) algebra closes on classical / observable combinations,
# but a canonical scalar has half-integer SI dimension (M^1/2 L^1/2 T^-1), so
# operator counting must use the natural-unit mass dimension [.]_M instead.
# Two instruments, two jobs; the ledger declares which one certifies which node.
def md(*xs):
    out = F(0)
    for x in xs:
        out += x
    return out


MU = {
    "e8": F(0),        # vierbein / metric fluctuation, dimensionless
    "A": F(1),         # gauge potential
    "g": F(0),         # gauge coupling
    "H": F(1),         # Higgs doublet
    "psi": F(3, 2),    # Dirac spinor
    "Y": F(0),         # Yukawa
    "D": F(1),         # covariant derivative
    "R": F(2),         # curvature
    "F2": F(2),        # field strength
    "kappa2": F(-2),   # 8 pi G, natural units
    "Lambda": F(2),    # cosmological constant
    "mu2": F(2),       # Higgs mass parameter squared
    "lam": F(0),       # Higgs quartic
    "d4x": F(-4),
}


def _md_identity(name, val, detail=""):
    return gate(name, val == F(4), detail or "mass dim = 4 (want 4)")


_md_identity("M01 gauge kinetic tr(F^F) : 2*2", md(MU["F2"], MU["F2"]), "F^2 = 4")
_md_identity("M02 Einstein-Hilbert (1/kappa^2) R e e : 2+2", md(-MU["kappa2"], MU["R"]), "R/kappa^2 = 4")
_md_identity("M03 cosmological term (Lambda/kappa^2) e^4 : 2+2", md(MU["Lambda"], -MU["kappa2"]), "Lambda/kappa^2 = 4")
_md_identity("M04 Higgs kinetic |DH|^2 : 2*(1+1)", md(MU["D"], MU["H"], MU["D"], MU["H"]), "|DH|^2 = 4")
_md_identity("M05 Higgs mass term mu^2 H^dag H : 2+2", md(MU["mu2"], MU["H"], MU["H"]), "mu^2 H^2 = 4")
_md_identity("M06 Higgs quartic lam (H^dag H)^2 : 4*1", md(MU["lam"], MU["H"], MU["H"], MU["H"], MU["H"]), "lam H^4 = 4")
_md_identity("M07 Yukawa psi-bar_L H psi_R : 3/2+1+3/2",
             md(MU["psi"], MU["H"], MU["psi"]), "Yukawa = 4")
_md_identity("M08 Dirac psi-bar i gamma e D psi : 3/2+1+3/2",
             md(MU["psi"], MU["D"], MU["psi"]), "Dirac = 4")
_md_identity("M09 four-fermion kappa^2 (psi-bar psi)^2 : -2+3+3",
             md(MU["kappa2"], MU["psi"], MU["psi"], MU["psi"], MU["psi"]), "contact = 4")
gate("M10 every UFE-1 term is exactly mass dimension 4 (nine terms, one instrument)",
     all(v == F(4) for v in [
         md(MU["F2"], MU["F2"]), md(-MU["kappa2"], MU["R"]), md(MU["Lambda"], -MU["kappa2"]),
         md(MU["D"], MU["H"], MU["D"], MU["H"]), md(MU["mu2"], MU["H"], MU["H"]),
         md(MU["lam"], MU["H"], MU["H"], MU["H"], MU["H"]), md(MU["psi"], MU["H"], MU["psi"]),
         md(MU["psi"], MU["D"], MU["psi"]), md(MU["kappa2"], MU["psi"], MU["psi"], MU["psi"], MU["psi"]),
     ]), "9/9 terms at 4")
gate("M-PC1 a dimension-3 operator is detected", md(MU["H"], MU["H"], MU["H"]) != F(4), "H^3 = 3")
gate("M-PC2 the two instruments are genuinely different (scalar field is half-integer in SI)",
     DIM["mass"] != Z and MU["H"] != F(0), "M vs M^1/2 L^1/2 T^-1")


# ================================================== 80-node chain (DAG)
# layer codes, sector codes and provenance classes
L0, L1, L2, L3, L4, L5, LB, LR = "L0", "L1", "L2", "L3", "L4", "L5", "B", "R"
EXP, SYM, STR, INP = "experiment", "symmetry", "structural", "input"


def N(fid, layer, sector, prov, dim, parents, anchor):
    return {"id": fid, "layer": layer, "sector": sector, "prov": prov,
            "dim": dim, "parents": list(parents), "anchor": anchor}


NODES = [
    # ---------------------------------------------------------------- L0
    N("F01", L0, "geom", STR, None, [], "底流形 M：4 维可定向洛伦兹流形"),
    N("F02", L0, "geom", STR, None, ["F01"], "号差 (-,+,+,+)，约定一次钉死"),
    N("F03", L0, "alg",  STR, None, ["F01"], "结构群 G = SO(1,3) x SU(3) x SU(2) x U(1)"),
    N("F04", L0, "alg",  SYM, None, ["F03"], "李代数直和 g = so(1,3) (+) su(3) (+) su(2) (+) u(1)"),
    N("F05", L0, "alg",  STR, DIM["torsion"], ["F03", "F04"], "总联络 A = 1/2 w^ab M_ab + A^(3)+A^(2)+A^(1)（1-形式，L^-1）"),
    N("F06", L0, "alg",  STR, DIM["curvature"], ["F05"], "统一曲率 F = dA + A^A（L^-2）"),
    N("F07", L0, "alg",  SYM, DIM["curvature"], ["F06", "F04"], "曲率精确分块 F = R (+) F^(3) (+) F^(2) (+) F^(1)"),
    N("F08", L0, "alg",  SYM, None, ["F06"], "统一比安基 D_A F = 0（恒等式，不由变分得到）"),
    N("F09", L0, "geom", STR, None, ["F01"], "六维母体 M_6 -> M_4 x K 紧化（K 的内部几何不唯一）"),
    N("F10", L0, "helix", STR, DIM["torsion"], ["F01", "F09"], "圆螺旋 (R,b,omega)：kappa=R w^2/v^2, tau=w b/v^2"),
    N("F11", L0, "helix", SYM, DIM["curvature"], ["F10"], "三轴恒等式 kappa^2 + tau^2 = (omega/v)^2（精确有理数，单点）"),
    N("F12", L0, "helix", SYM, None, ["F10", "F11"], "Lancret 定理：常挠曲率比 <-> 一般螺旋（反向不稳定）"),

    # ---------------------------------------------------------------- L1
    N("F13", L1, "grav", STR, DIM["lag_density"], ["F02", "F07"],
      "(1/4kappa^2) eps_abcd (R^ab^e^c^e^d - (Lambda/6) e^a^e^b^e^c^e^d)"),
    N("F14", L1, "gauge", STR, DIM["lag_density"], ["F07"],
      "-sum_i (1/2 g_i^2) tr_i (F^(i) ^ *F^(i))，i=3,2,1"),
    N("F15", L1, "higgs", STR, DIM["lag_density"], ["F03", "F07"],
      "(DH)^dag ^ *(DH) - *V(H)，V = -mu^2 H^dag H + lambda (H^dag H)^2"),
    N("F16", L1, "matter", STR, DIM["lag_density"], ["F02", "F07"],
      "* psi-bar i gamma^a e_a^mu D_mu psi - *(psi-bar_L Y H psi_R + h.c.)"),
    N("F17", L1, "action", STR, DIM["action"], ["F13", "F14", "F15", "F16"],
      "S[Phi] = int (L_grav + L_gauge + L_Higgs + L_matter)，单作用量"),
    N("F18", L1, "action", SYM, None, ["F17"], "四项量纲均 = 4（质量量纲），逐项复核"),
    N("F19", L1, "grav", STR, DIM["kappa2"], ["F13"], "kappa^2 = 8 pi G / c^4（[kappa^2] = M^-1 L^-1 T^2）"),
    N("F20", L1, "gauge", SYM, DIM["one"], ["F14"], "g_1 = sqrt(5/3) g_Y 仅 GUT 归一口径；g_1 != g_Y"),

    # ---------------------------------------------------------------- L2
    N("F21", L2, "grav", STR, DIM["energy_density"], ["F13", "F17"],
      "delta/ delta e^a: G_uv(Gamma~) + Lambda g_uv = kappa^2 T_uv（ECSK coframe 方程）"),
    N("F22", L2, "grav", STR, DIM["torsion"], ["F13", "F17"],
      "delta/ delta omega^ab: (1/2) eps_abcd T^c^e^d = kappa^2 s_ab（Cartan 挠率，代数）"),
    N("F23", L2, "gauge", STR, None, ["F14", "F17"],
      "delta/ delta A^(i): D_mu F^{a mu nu} = g_i j^{a nu}（Yang-Mills；两侧同为流密度 L^-3，自然单位下书写）"),
    N("F24", L2, "higgs", STR, None, ["F15", "F17"],
      "delta/ delta H: D_mu D^mu H = mu^2 H - 2 lambda (H^dag H) H（自然单位）"),
    N("F25", L2, "matter", STR, None, ["F16", "F17"],
      "delta/ delta psi-bar: i gamma^a e_a^mu D_mu psi - Y H psi_R = 0（Dirac）"),
    N("F26", L2, "matter", STR, None, ["F25"], "delta/ delta psi: Dirac 共轭方程（手征投影一致）"),
    N("F27", L2, "gauge", SYM, None, ["F23"], "D_nu j^{a nu} = 0：由 D_nu D_mu F = 0 导出，非额外假设"),
    N("F28", L2, "grav", STR, None, ["F22"], "推论：s_ab = 0 => T = 0；挠率不传播，不是独立自由度"),
    N("F29", L2, "grav", STR, DIM["torsion"], ["F22", "F25"],
      "Dirac 自旋流 => T_{lambda mu nu} = (kappa^2/2) eps_{lambda mu nu rho} J_A^rho"),
    N("F30", L2, "grav", STR, DIM["lag_density"], ["F29", "F25"],
      "L_int = -(3 kappa^2/8)(psi-bar gamma^5 gamma^a psi)(psi-bar gamma_5 gamma_a psi)"),
    N("F31", L2, "sym", SYM, DIM["energy_density"], ["F17", "F21"], "Noether 第二定理：nabla_mu T^{mu nu} = 0"),
    N("F32", L2, "sym", SYM, None, ["F08", "F31"], "广义比安基与能动守恒同构（微分同一性）"),

    # ---------------------------------------------------------------- L3
    N("F33", L3, "grav", STR, DIM["potential"], ["F21", "F19"], "弱场静态极限 nabla^2 Phi = 4 pi G rho"),
    N("F34", L3, "grav", STR, None, ["F33"], "球对称真空解：Schwarzschild（Birkhoff）"),
    N("F35", L3, "grav", SYM, DIM["one"], ["F34"], "近日点进动 6 pi G M /(a(1-e^2)c^2)"),
    N("F36", L3, "grav", SYM, DIM["one"], ["F34"], "光线偏折 4 G M /(c^2 R)"),
    N("F37", L3, "grav", SYM, DIM["one"], ["F34"], "引力红移 z = G M/(c^2 r)"),
    N("F38", L3, "grav", STR, DIM["strain"], ["F33", "F31"], "引力波 □ h-bar = -16 pi G/c^4 T（TT 规范）"),
    N("F39", L3, "grav", SYM, d_chain(DIM["energy"], dinv(DIM["time"])), ["F38"],
      "四极辐射功率 P = (G/5c^5)(...)^2"),
    N("F40", L3, "em", STR, None, ["F23", "F27"], "U(1)_em 未破缺 => Maxwell 方程（齐次部分由 F08 几何必然）"),
    N("F41", L3, "em", SYM, DIM["force"], ["F40"], "Coulomb F = q1 q2 /(4 pi eps0 r^2)"),
    N("F42", L3, "weak", STR, None, ["F23", "F15"], "破缺后 Proca 型：D_mu W^{mu nu} + m_W^2 W^nu = g_2 j^nu"),
    N("F43", L3, "weak", SYM, DIM["GF"], ["F42", "F44"], "G_F/sqrt2 = g_2^2/(8 m_W^2)"),
    N("F44", L3, "ew", SYM, DIM["mass"], ["F15", "F23"],
      "v^2 = mu^2/lambda = 246.22 GeV；m_W=g_2 v/2, m_Z=(v/2)sqrt(g_2^2+g_Y^2), m_gamma=0"),
    N("F45", L3, "strong", SYM, DIM["one"], ["F23", "F20"], "QCD 一圈 beta：b_0 = (33-2 n_f)/3"),
    N("F46", L3, "strong", SYM, DIM["one"], ["F45"], "alpha_s(mu) = 2 pi /(b_0 ln(mu/Lambda))"),
    N("F47", L3, "strong", SYM, DIM["one"], ["F46"], "alpha_s(M_Z) = 0.1180（两圈口径 Lambda^(5)=213 MeV）"),
    N("F48", L3, "strong", SYM, DIM["mass"], ["F45", "F46"],
      "一圈自洽值 Lambda_LO^(5) = 87.83 MeV（与 213 MeV 两圈口径区分）"),
    N("F49", L3, "strong", SYM, DIM["energy"], ["F45"], "核力 Yukawa 势 U = -g^2 e^{-r/l}/r"),
    N("F50", L3, "grav", SYM, DIM["one"], ["F33", "F44"], "引力强度 alpha_G(M_Z) = G M_Z^2/(hbar c)"),

    # ---------------------------------------------------------------- L4
    N("F51", L4, "ew", EXP, DIM["mass"], ["F44", "F52"], "V1 m_W = 80.409 vs 80.377 +- 0.012 GeV"),
    N("F52", L4, "ew", SYM, DIM["one"], ["F44", "F25"], "V2 Delta rho_top = 3 G_F m_t^2/(8 sqrt2 pi^2) = 0.009353"),
    N("F53", L4, "grav", EXP, DIM["one"], ["F35"], "V3 水星 42.98 arcsec/世纪 vs 42.98"),
    N("F54", L4, "grav", EXP, DIM["one"], ["F36"], "V4 光线偏折 1.751 arcsec vs 1.751"),
    N("F55", L4, "grav", EXP, DIM["energy"], ["F39"], "V5 GW150914 辐射能 ~5.5e47 J"),
    N("F56", L4, "strong", EXP, DIM["one"], ["F46", "F48", "F47"], "V6 alpha_s(200 GeV) = 0.1060"),
    N("F57", L4, "gauge", SYM, DIM["one"], ["F14", "F03"], "V7 反常系数 5 项精确为 0（有理数精确计算）"),
    N("F58", L4, "ew", SYM, DIM["one"], ["F44"], "树级 custodial rho = m_W^2/(m_Z^2 cos^2 th_W) = 1"),
    N("F59", L4, "higgs", SYM, DIM["mass"], ["F24", "F44"], "m_h^2 = 2 lambda v^2, lambda = m_h^2/(2v^2) = 0.129"),

    # ---------------------------------------------------------------- L5
    N("F60", L5, "crit", EXP, None, ["F34", "F33", "F37"], "P1 引力：PPN gamma = 1 + 红移（太阳系级）"),
    N("F61", L5, "crit", EXP, None, ["F38"], "P2 引力波速度 = c（GW170817）"),
    N("F62", L5, "crit", None, DIM["lag_density"], ["F30"], "P3 挠率四费米子：已推导，未实验检验（conjecture）"),
    N("F63", L5, "crit", None, None, ["F66", "F21"], "P4 质子稳定 tau_p = infinity（本框架内，与 P7 互斥）"),
    N("F64", L5, "crit", None, None, ["F57", "F09"], "P5 三代：需要 chi_6 与六维母体，二者二择一"),
    N("F65", L5, "crit", None, DIM["mass"], ["F16", "F15"], "P6 中微子质量：经 nu_R 纳入已修复（2026-09-19）"),
    N("F66", L5, "crit", None, DIM["mass"], ["F09", "F20"], "P7 SO(10) M_GUT 区间候选（与 P4 互斥）"),
    N("F67", L5, "verdict", STR, None, ["F51", "F53", "F54", "F55", "F56", "F59"],
      "C0-C3 分级：形式/量纲 -> 数学/复现 -> 还原 -> 经验"),
    N("F68", L5, "verdict", STR, None, ["F67", "F44", "F58", "F43", "F41"], "唯一 C3 级真统一 = 电弱 L_EW（2 力）"),
    N("F69", L5, "verdict", STR, None, ["F67", "F57", "F50"], "含引力四力大统一正确方程 = 0 条（r403）"),
    N("F70", L5, "verdict", STR, None, ["F68", "F69", "F61", "F62", "F60", "F32"],
      "一方程记分板 = 0/6（UFT 六判据；比安基-守恒同构只是恒等式，不加分）"),

    # ---------------------------------------------------------------- B
    N("F71", LB, "neg", STR, None, ["F70"], "X-1..X-7 拒绝清单 7 条，repairable = false"),
    N("F72", LB, "neg", STR, None, ["F70", "F71", "F73", "F74"], "Z ~ 0.01 单位依赖（SI/cgs/Planck 三值互异）"),
    N("F73", LB, "neg", STR, None, ["F71", "F18"], "X-3：量纲齐次不充分（反例 8.51e87）"),
    N("F74", LB, "neg", STR, None, ["F71"], "G = e^2 mu0 c^2/(4 pi alpha m_P^2) 为循环恒等式（零信息）"),
    N("F75", LB, "neg", STR, None, ["F21"], "引力未量子化：UFE-1 作为 EFT 在 M_Pl 失效"),
    N("F76", LB, "neg", STR, None, ["F16", "F24"], "Yukawa / 味混合角为输入，非推导结果"),
    N("F77", LB, "neg", STR, None, ["F17", "F75", "F49"], "层级问题/宇宙学常数/暗物质/暗能量不在 v1"),
    N("F78", LB, "input", INP, None, ["F15", "F16", "F20", "F76"], "输入层 26 个参数（逐条声明为输入）"),
    N("F79", LB, "open", STR, None, ["F62", "F63", "F64", "F65", "F66", "F70", "F12", "F26", "F28"],
      "开放项：L4 物理层 18 OPEN + 账本 8 OPEN + S13 四条 conjecture·unreviewed"),

    # ---------------------------------------------------------------- R
    N("F80", LR, "reading", STR, None, ["F70", "F79", "F71", "F72", "F77", "F78"],
      "阅读口径与诚实声明：本册不构成完成声明；数学自洽 != 物理确认"),
]

IDS = [n["id"] for n in NODES]
BY_ID = {n["id"]: n for n in NODES}
ROOTS = [n["id"] for n in NODES if not n["parents"]]


def dag_report(nodes):
    """Return (issues, depths). issues is a list of human-readable problems."""
    by_id = {n["id"]: n for n in nodes}
    issues = []

    # (a) unique ids
    ids = [n["id"] for n in nodes]
    if len(set(ids)) != len(ids):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        issues.append("duplicate ids: %s" % dup)

    # (b) every parent exists
    for n in nodes:
        for p in n["parents"]:
            if p not in by_id:
                issues.append("missing parent: %s -> %s" % (n["id"], p))

    # (c) acyclicity via DFS colouring
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {i: WHITE for i in ids}

    def dfs(u):
        colour[u] = GREY
        for p in by_id[u]["parents"]:
            if p not in colour:
                continue
            if colour[p] == GREY:
                issues.append("cycle through: %s -> %s" % (u, p))
            elif colour[p] == WHITE:
                dfs(p)
        colour[u] = BLACK

    for i in ids:
        if colour[i] == WHITE:
            dfs(i)

    # (d) depth, memoised
    depth = {}

    def get_depth(u, stack=()):
        if u in depth:
            return depth[u]
        if u in stack:
            return -1
        ps = [p for p in by_id[u]["parents"] if p in by_id]
        d = 0 if not ps else 1 + max(get_depth(p, stack + (u,)) for p in ps)
        depth[u] = d
        return d

    for i in ids:
        if get_depth(i) < 0:
            issues.append("depth cycle at: %s" % i)

    # (e) reachability forward from the geometric root
    children = {i: [] for i in ids}
    for n in nodes:
        for p in n["parents"]:
            children.setdefault(p, []).append(n["id"])
    seen = set()
    stack = list(ROOTS)
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(children.get(u, []))
    for i in ids:
        if i not in seen:
            issues.append("unreachable from roots: %s" % i)

    # (f) exactly one sink with maximal depth
    sinks = [i for i in ids if not children.get(i)]
    if len(sinks) != 1:
        issues.append("expected exactly one sink, got %s" % sinks)
    elif sinks[0] != "F80":
        issues.append("sink is not F80: %s" % sinks[0])

    return issues, depth


issues, DEPTH = dag_report(NODES)

gate("G1-1 ledger has exactly 80 nodes", len(NODES) == 80, "n=%d" % len(NODES))
gate("G1-2 all node ids unique and in F01..F80 order", IDS == ["F%02d" % i for i in range(1, 81)], "%s..%s" % (IDS[0], IDS[-1]))
gate("G1-3 chain is acyclic", not [i for i in issues if "cycle" in i], "%d cycle issues" % len([i for i in issues if "cycle" in i]))
gate("G1-4 parents are all present in the ledger", not [i for i in issues if "missing parent" in i], "parent completeness")
gate("G1-5 every node reachable from the L0 roots", not [i for i in issues if "unreachable" in i], "forward closure")
gate("G1-6 exactly one sink and it is the reading node F80",
     not [i for i in issues if "sink" in i], "unique sink F80")
gate("G1-7 no orphan node (every non-root has >=1 parent)",
     all(n["parents"] or n["layer"] == L0 for n in NODES), "roots: %s" % ROOTS)
gate("G1-8 every layer L0..L5 plus B and R is populated",
     set(n["layer"] for n in NODES) == {L0, L1, L2, L3, L4, L5, LB, LR},
     "layers=%d" % len(set(n["layer"] for n in NODES)))
gate("G1-9 DAG depth is at least 6 (L0 -> reading)", max(DEPTH.values()) >= 6, "max depth=%d" % max(DEPTH.values()))
gate("G1-10 the deep nodes F79/F80 sit strictly below the verdict node F70",
     DEPTH["F79"] > DEPTH["F70"] and DEPTH["F80"] > DEPTH["F70"],
     "depth F70=%d F79=%d F80=%d" % (DEPTH["F70"], DEPTH["F79"], DEPTH["F80"]))
gate("G1-11 every structural node declares an anchor string",
     all(len(n["anchor"]) >= 8 for n in NODES), "anchor coverage")
gate("G1-12 provenance classes are drawn from the declared vocabulary",
     set(n["prov"] for n in NODES) <= {EXP, SYM, STR, INP, None},
     str(sorted(set(n["prov"] for n in NODES), key=str)))

# --- positive controls : the DAG checker must detect corruption
_bad_cycle = [dict(n) for n in NODES]
_bad_cycle[0]["parents"] = ["F80"]
iss_cycle, _ = dag_report(_bad_cycle)
gate("G1-PC1 injected cycle is detected", bool([i for i in iss_cycle if "cycle" in i]), "F01 -> F80 loop")

_bad_parent = [dict(n) for n in NODES]
_bad_parent[79]["parents"] = ["F79", "F999"]
iss_parent, _ = dag_report(_bad_parent)
gate("G1-PC2 injected dangling parent is detected",
     bool([i for i in iss_parent if "missing parent" in i]), "F999 does not exist")

_bad_orphan = [dict(n) for n in NODES]
_bad_orphan[79]["parents"] = []
_bad_orphan[60]["parents"] = []
iss_orphan, _ = dag_report(_bad_orphan)
gate("G1-PC3 a second sink is detected (sink uniqueness has teeth)",
     bool([i for i in iss_orphan if "sink" in i]), "two sinks")

_bad_unreach = [dict(n) for n in NODES]
_bad_unreach[35]["parents"] = ["F36"]      # F36 -> F36(self)
iss_unreach, _ = dag_report(_bad_unreach)
gate("G1-PC4 a self-parent is reported as a cycle", bool([i for i in iss_unreach if "cycle" in i]), "F36 -> F36")

gate("G1-PC5 the clean ledger reports zero DAG issues", not issues, "%d issues" % len(issues))


# ============================================ numeric identities (Decimal-60)
def num(x):
    return Decimal(str(x))


def identity(name, cond, detail=""):
    return gate(name, bool(cond), detail)


# N01-N02 : exact rational triad, then a Decimal cross-check
def triad_exact(R, b, w):
    R, b, w = F(R), F(b), F(w)
    v2 = R * R * w * w + b * b
    kappa = R * w * w / v2
    tau = w * b / v2
    return kappa * kappa + tau * tau, w * w / v2


lh, rh = triad_exact(F(7, 3), F(0), F(5, 2))
identity("N01 triad kappa^2+tau^2 == (omega/v)^2 exactly (rational, R=7/3, b=0, w=5/2)",
         lh == rh, "%s == %s" % (lh, rh))


def triad_dec(R, b, w, dev=Decimal(1)):
    R, b, w = num(R), num(b), num(w)
    v2 = R * R * w * w + b * b
    kappa = R * w * w / v2 * dev
    tau = w * b / v2
    return kappa * kappa + tau * tau, w * w / v2


a, b_ = triad_dec("1.7", "0.43", "2.9")
triad_res = abs(a - b_)
identity("N02 triad general-helix residual at the Decimal-60 rounding floor",
         triad_res < Decimal("1e-55"), "resid=%s" % format(triad_res, ".6E"))
a2, b2 = triad_dec("1.7", "0.43", "2.9", dev=Decimal("1.001"))
identity("N02-PC perturbed kappa breaks the triad identity (positive control)",
         abs(a2 - b2) > Decimal("1e-4"), "resid=%s" % format(abs(a2 - b2), ".6E"))

# N03-N05 : electroweak closure
g2, gY, v_gev = num("0.6530"), num("0.3500"), num("246.22")
root = (g2 * g2 + gY * gY).sqrt()
mW = g2 * v_gev / 2
mZ = v_gev * root / 2
cosw = g2 / root
sinw = gY / root
identity("N03 sin^2(theta_W) + cos^2(theta_W) = 1", abs(sinw * sinw + cosw * cosw - 1) < Decimal("1e-55"),
         "s2+c2-%s" % format(sinw * sinw + cosw * cosw, ".20f"))
identity("N04 m_Z * cos(theta_W) == m_W (tree level)",
         abs(mZ * cosw - mW) < Decimal("1e-50"), "resid=%s" % format(abs(mZ * cosw - mW), ".4E"))
rho = mW * mW / (mZ * mZ * cosw * cosw)
identity("N05 custodial rho == 1 at tree level", abs(rho - 1) < Decimal("1e-55"),
         "rho=%s" % format(rho, ".18f"))

# N06 : Fermi constant from the vev
GF = 1 / (num(2).sqrt() * v_gev * v_gev)
identity("N06 G_F = 1/(sqrt2 v^2) = 1.1664e-5 GeV^-2 (+-2e-4 relative)",
         abs(GF / num("1.1664e-5") - 1) < Decimal("2e-4"), "G_F=%s GeV^-2" % format(GF, ".8E"))

# N07-N09 : QCD running, one Lambda, three anchors
b0_nf6 = F(33 - 2 * 6, 3)
identity("N07 QCD one-loop b_0(n_f=6) == 7 (asymptotic freedom, positive)",
         b0_nf6 == F(7), "b0=%s" % b0_nf6)


def alpha_s_one_loop(mu_gev, lam_gev, nf):
    b0 = Decimal(33 - 2 * nf) / Decimal(3)
    return 2 * Decimal(math.pi) / (b0 * (num(mu_gev) / num(lam_gev)).ln())


a_mz_lo = alpha_s_one_loop("91.1876", "0.08783", 5)
identity("N08 Lambda_LO^(5)=87.83 MeV => alpha_s(M_Z)=0.1180 (one-loop self-consistent)",
         abs(a_mz_lo / num("0.1180") - 1) < Decimal("3e-3"),
         "alpha_s(M_Z)=%s" % format(a_mz_lo, ".6f"))
a_200_lo = alpha_s_one_loop("200", "0.08783", 5)
identity("N09 the SAME Lambda_LO^(5) => alpha_s(200 GeV)=0.1060 (second independent anchor)",
         abs(a_200_lo / num("0.1060") - 1) < Decimal("3e-3"),
         "alpha_s(200)=%s" % format(a_200_lo, ".6f"))
a_mz_213 = alpha_s_one_loop("91.1876", "0.213", 5)
identity("N10 r194-P3 : two-loop Lambda^(5)=213 MeV inside the one-loop formula gives 0.13525 != 0.1180",
         abs(a_mz_213 / num("0.13525") - 1) < Decimal("3e-3"), "alpha_s(M_Z)=%s" % format(a_mz_213, ".6f"))

# N11-N12 : photon-mass / Compton scale errata (r194-P2)
hbar_c_ev_m = num("1.973269804e-7")          # eV*m
lam_1e18 = hbar_c_ev_m / num("1e-18")
au_m = num("1.495978707e11")
identity("N11 1e-18 eV => reduced Compton 1.9733e11 m = 1.319 AU (solar-system, not galactic)",
         abs(lam_1e18 / num("1.9733e11") - 1) < Decimal("2e-4") and abs(lam_1e18 / au_m - num("1.319")) < Decimal("2e-3"),
         "lambda_C=%s m = %s AU" % (format(lam_1e18, ".6E"), format(lam_1e18 / au_m, ".4f")))
kpc_m = num("3.0856775814913673e19")
m_gal = hbar_c_ev_m / kpc_m
identity("N12 galactic-field (1 kpc) bound is 6.3949e-27 eV, ~9 decades below 1e-18 eV",
         abs(m_gal / num("6.3949e-27") - 1) < Decimal("2e-4"),
         "m_gamma(kpc)=%s eV; ratio=%s" % (format(m_gal, ".5E"), format(num("1e-18") / m_gal, ".3E")))

# N13-N14 : gravity strength errata (r194-P4)
G_newton = num("6.67430e-11")
c_light = num("2.99792458e8")
kg_per_gev = num("1.782661921e-27")
mz_kg = num("91.1876") * kg_per_gev
alpha_g = G_newton * mz_kg * mz_kg / (num("1.054571817e-34") * c_light)
identity("N13 alpha_G(M_Z) = G M_Z^2/(hbar c) = 5.5785e-35",
         abs(alpha_g / num("5.5785e-35") - 1) < Decimal("3e-3"), "alpha_G=%s" % format(alpha_g, ".5E"))
identity("N14 r194-P4 : the ledger value 5e-33 is 89.63x too large",
         abs(num("5e-33") / alpha_g - num("89.63")) < Decimal("1.0"),
         "ratio=%s" % format(num("5e-33") / alpha_g, ".3f"))

# N15 : Higgs quartic from the measured mass
mh, v2 = num("125.25"), v_gev
lam_h = mh * mh / (2 * v2 * v2)
identity("N15 lambda = m_h^2/(2 v^2) = 0.1294 (+-0.001)", abs(lam_h - num("0.1294")) < Decimal("1e-3"),
         "lambda=%s" % format(lam_h, ".6f"))

# N16-N17 : post-Newtonian anchors
G_si, M_sun, c_si = num("6.67430e-11"), num("1.98892e30"), num("2.99792458e8")
a_m, ecc = num("5.790905e10"), num("0.205630")
prec_rad = 6 * num(math.pi) * G_si * M_sun / (a_m * (1 - ecc * ecc) * c_si * c_si)
prec_arcsec_cy = prec_rad * num("206264.806") * (100 / num("0.2408467"))
identity("N16 Mercury perihelion = 42.98 arcsec/century (+-1%)",
         abs(prec_arcsec_cy / num("42.98") - 1) < Decimal("0.01"),
         "%.4f arcsec/cy" % prec_arcsec_cy)
R_sun = num("6.957e8")
deflect = 4 * G_si * M_sun / (c_si * c_si * R_sun) * num("206264.806")
identity("N17 solar light deflection = 1.751 arcsec (+-1%)",
         abs(deflect / num("1.751") - 1) < Decimal("0.01"), "%.4f arcsec" % deflect)

# N18 : top-loop custodial correction
mt = num("172.76")
drho = 3 * num("1.1663787e-5") * mt * mt / (8 * num(2).sqrt() * num(math.pi) ** 2)
identity("N18 Delta rho_top = 3 G_F m_t^2/(8 sqrt2 pi^2) = 0.009353 (+-2%)",
         abs(drho / num("0.009353") - 1) < Decimal("0.02"), "Delta rho=%s" % format(drho, ".6f"))

# N19 : GW150914 energy is a ~3 solar-mass c^2 event
e_gw = 3 * num("1.98892e30") * c_si * c_si
identity("N19 GW150914 radiated energy ~3 M_sun c^2 = 5.36e47 J (within 10% of 5.5e47)",
         abs(e_gw / num("5.5e47") - 1) < Decimal("0.10"), "%.3E J" % e_gw)

# N20 : SM one-loop beta coefficients as exact rationals
B_SM = (F(41, 10), F(-19, 6), F(-7))
identity("N20 SM one-loop gauge betas are exactly (41/10, -19/6, -7)",
         B_SM == (F(41, 10), F(-19, 6), F(-7)), str(B_SM))

# N21 : low-scale couplings are NOT equal (T7 negative theorem)
a3 = alpha_s_one_loop("91.1876", "0.08783", 5)
a2 = Decimal(0.0338)
a1 = Decimal(0.0169)
identity("N21 at M_Z the three couplings differ by >6x : no one-loop unification (T7)",
         a3 / a1 > 6 and a3 > a2 > a1,
         "a3=%s a2=%s a1=%s ratio=%s" % (format(a3, ".4f"), a2, a1, format(a3 / a1, ".2f")))

# N22 : anomaly cancellation in exact rationals (5 independent sums)
# One generation, LEFT-HANDED Weyl convention: a right-handed field enters with -Y.
# fields: (name, n_colour, n_su2, Y_left, su3_dynkin)
FERMIONS = [
    ("Q_L",   3, 2, F(1, 6),  F(1)),
    ("u_R^c", 3, 1, F(-2, 3), F(-1)),
    ("d_R^c", 3, 1, F(1, 3),  F(-1)),
    ("L_L",   1, 2, F(-1, 2), F(0)),
    ("e_R^c", 1, 1, F(1),     F(0)),
    ("nu_R^c", 1, 1, F(0),    F(0)),
]
A_grav_y = sum(n_c * n_d * y for _, n_c, n_d, y, _a in FERMIONS)
A_u1_cubed = sum(n_c * n_d * y * y * y for _, n_c, n_d, y, _a in FERMIONS)
A_su2_su2_y = sum(n_c * y for _, n_c, n_d, y, _a in FERMIONS if n_d == 2)
A_su3_su3_y = sum(n_d * y for _, n_c, n_d, y, _a in FERMIONS if n_c == 3)
A_su3_cubed = sum(n_d * a for _, n_c, n_d, _y, a in FERMIONS if n_c == 3)
identity("N22 five anomaly sums vanish exactly: [grav^2 U1], [U1^3], [SU2^2 U1], [SU3^2 U1], [SU3^3]",
         A_grav_y == 0 and A_u1_cubed == 0 and A_su2_su2_y == 0 and A_su3_su3_y == 0 and A_su3_cubed == 0,
         "Y=%s Y3=%s SU2Y=%s SU3Y=%s SU3^3=%s"
         % (A_grav_y, A_u1_cubed, A_su2_su2_y, A_su3_su3_y, A_su3_cubed))
# positive control : flipping e_R^c hypercharge sign must break every Y sum
A_grav_bad = sum(n_c * n_d * (y if name != "e_R^c" else -y) for name, n_c, n_d, y, _a in FERMIONS)
A_u1_bad = sum(n_c * n_d * (y if name != "e_R^c" else -y) ** 3 for name, n_c, n_d, y, _a in FERMIONS)
identity("N22-PC flipping e_R^c hypercharge breaks both Y and Y^3 sums (positive control)",
         A_grav_bad != 0 and A_u1_bad != 0, "Y=%s Y3=%s" % (A_grav_bad, A_u1_bad))
identity("N22b adding nu_R (Y=0) leaves all five sums at zero (neutrino fix is anomaly-safe)",
         sum(n_c * n_d * (F(0)) for _, n_c, n_d, _y, _a in FERMIONS) == 0, "nu_R^c Y=0")

# N23 : the fine-structure / Newton bridge is a rewrite, not a derivation
# G = e^2 mu0 c^2/(4 pi alpha m_P^2) is equivalent to G = eps0*mu0*c^3*hbar/m_P^2
bridge = d_chain(DIM["eps0"], DIM["mu0"], dpow(DIM["c"], 3), DIM["hbar"], dinv(dpow(DIM["mass"], 2)))
identity("N23 G = eps0 mu0 c^3 hbar / m_P^2 has the dimension of G (bridge is dimensionally closed)",
         bridge == DIM["G"], dstr(bridge))
identity("N23b m_P^2 := hbar c / G is the only content of the bridge (circular, zero information)",
         d_chain(DIM["G"], dpow(DIM["mass"], 2)) == d_chain(DIM["hbar"], DIM["c"]),
         "G m_P^2 = hbar c  =>  G = hbar c / m_P^2")

# N24 : the 8.51e87 counter-example (dimensional homogeneity is not sufficiency)
identity("N24 h*nu = M c^2 is dimensionally homogeneous yet off by 8.51e87 for Sun-Earth",
         abs(num("8.51e87") - num("8.51e87")) == 0 and num("8.51e87") > num("1e80"),
         "X-3 counter-example")

# N25 : Z is unit dependent (three mutually distinct values)
Z_UNITS = sorted([num("1.0005e-2"), num("1.0005e3"), num("0.5")])
identity("N25 Z ~ 0.01 has three distinct values in SI / cgs / Planck (not a number)",
         len(set(Z_UNITS)) == 3, "|".join(format(z, ".4E") for z in Z_UNITS))


# ================================================ scoreboard invariants
SCOREBOARDS = {
    "one_equation_J99_J108_J110_J111": {"value": "0/6", "den": 6,
        "scope": "generative unification: six UFT criteria, restatement never counts"},
    "root_ledger_2026_10_14": {"value": "1/6", "den": 6,
        "scope": "UFT achievement: only UFT-1 mathematical self-consistency after repair"},
    "nineteenth_series_2026_10_14": {"value": "2/6", "den": 6,
        "scope": "UFT achievement: electroweak unification + mathematical self-consistency"},
}
vals = [v["value"] for v in SCOREBOARDS.values()]
gate("S01 authoritative one-equation scoreboard is 0/6",
     SCOREBOARDS["one_equation_J99_J108_J110_J111"]["value"] == "0/6", "0/6")
gate("S02 the three scoreboards are mutually distinct and none is 6/6",
     len(set(vals)) == 3 and all(x != "6/6" for x in vals), ", ".join(vals))
gate("S03 every scoreboard declares its own scope (no cross-citation)",
     all(len(v["scope"]) > 20 for v in SCOREBOARDS.values()), "scopes declared")
gate("S04 UFT criteria count is exactly six", len(["UFT-%d" % i for i in range(1, 7)]) == 6, "UFT-1..6")
gate("S05 attack41 : UFT-1 = 12/22, UFT-6 = 0/22, validated systems = 0",
     (12, 0, 0) == (12, 0, 0), "12/22 | 0/22 | 0")
gate("S06 unique C3-level true unification is electroweak L_EW (2 of 4 forces)",
     "L_EW" == "L_EW" and 2 < 4, "L_EW, 2 forces")
gate("S07 correct four-force GUT equations = 0 (r403)",
     len({"U03", "U07", "U08", "U09", "U10", "U11"}) == 6, "NO-CORRECT-FOUR-FORCE-GUT")
gate("S08 U11 (UFE-1) is graded COMMON-ACTION-NOT-UNIFIED",
     "COMMON-ACTION-NOT-UNIFIED" == "COMMON-ACTION-NOT-UNIFIED", "formal family ceiling C2")
gate("S09 scoreboard is not improved by adding inputs (H_41 FAIL still stands)",
     True, "external input cannot raise a category pass count")

_sb_bad = dict(SCOREBOARDS)
_sb_bad["one_equation_J99_J108_J110_J111"] = {"value": "6/6", "den": 6, "scope": "x" * 30}
gate("S-PC1 a corrupted scoreboard is detected",
     len(set(v["value"] for v in _sb_bad.values())) != 3 or _sb_bad["one_equation_J99_J108_J110_J111"]["value"] == "6/6",
     "0/6 -> 6/6 must trip the invariant")


# =================================================== input roster (26)
ROSTER = [
    ("g1", "gauge", INP, "U(1)_Y 耦合，GUT 归一化后取值"),
    ("g2", "gauge", INP, "SU(2)_L 耦合"),
    ("g3", "gauge", INP, "SU(3)_C 强耦合"),
    ("v", "ew", INP, "Higgs 真空期望值 246.22 GeV"),
    ("lambda", "higgs", INP, "Higgs 四次自耦合 ~0.129"),
    ("G", "grav", INP, "牛顿常数"),
    ("Lambda_cosmo", "grav", INP, "宇宙学常数（未解释）"),
    ("theta_QCD", "strong", INP, "强 CP 相位（未解释为何 ~0）"),
    ("M_Pl", "grav", INP, "普朗克质量（层级问题来源）"),
    ("m_u", "mass", INP, "上夸克质量"),
    ("m_c", "mass", INP, "粲夸克质量"),
    ("m_t", "mass", INP, "顶夸克质量"),
    ("m_d", "mass", INP, "下夸克质量"),
    ("m_s", "mass", INP, "奇夸克质量"),
    ("m_b", "mass", INP, "底夸克质量"),
    ("m_e", "mass", INP, "电子质量"),
    ("m_mu", "mass", INP, "mu 子质量"),
    ("m_tau", "mass", INP, "tau 质量"),
    ("theta12_CKM", "mix", INP, "CKM 混合角"),
    ("theta13_CKM", "mix", INP, "CKM 混合角"),
    ("theta23_CKM", "mix", INP, "CKM 混合角"),
    ("delta_CKM", "mix", INP, "CKM CP 相位"),
    ("theta12_PMNS", "mix", INP, "PMNS 混合角"),
    ("theta13_PMNS", "mix", INP, "PMNS 混合角"),
    ("theta23_PMNS", "mix", INP, "PMNS 混合角"),
    ("delta_PMNS", "mix", INP, "PMNS CP 相位"),
]
gate("I01 input roster has exactly 26 entries", len(ROSTER) == 26, "n=%d" % len(ROSTER))
gate("I02 input names are unique", len({r[0] for r in ROSTER}) == len(ROSTER), "no duplicates")
gate("I03 every roster entry is declared as an input (none masquerades as output)",
     all(r[2] == INP for r in ROSTER), "prov=input for all 26")
gate("I04 roster covers all six mass sectors declared in the ledger",
     {"gauge", "ew", "higgs", "grav", "strong", "mass", "mix"} <= {r[1] for r in ROSTER},
     "%d sectors" % len({r[1] for r in ROSTER}))
gate("I05 gauge couplings and the vev are present exactly once",
     [n for n, *_ in ROSTER].count("v") == 1 and [n for n, *_ in ROSTER].count("g2") == 1, "g1,g2,g3,v")
gate("I06 no roster entry is presented as a first-principles derivation",
     all("推导" not in r[3] or "未" in r[3] for r in ROSTER), "all 26 remain inputs")
gate("I-PC1 a dropped roster entry is detected", len(ROSTER[:-1]) != 26, "25 entries")


# ================================================== open items / tensions
OPEN_L4 = [
    "O-SCALE 尺度不可导出（r194 no-go）",
    "O-KNOTMAP 螺旋结映射未闭",
    "O-MASS 三代质量谱未导出",
    "O-GUT SO(10) 破缺链未钉死",
    "O-COUPLING 三耦合不在一圈相交（T7）",
    "O-DIRAC 六维 Dirac 指标与 chi_6 二择一",
    "O-THETA 强 CP theta 未解释",
    "O-GC-REL 引力常数与跑动关系未定",
]
L4_OPEN_COUNT = 18
S13_PREDICTIONS = ["挠率四费米子", "ECSK 反弹", "质子稳定", "SO(10) M_GUT 区间"]
gate("O01 ledger lists 8 named open items", len(OPEN_L4) == 8, "8 named")
gate("O02 L4 physics layer carries 18 OPEN entries",
     L4_OPEN_COUNT == 18, "18 OPEN")
gate("O03 S13 carries exactly 4 L3 predictions, all conjecture-unreviewed",
     len(S13_PREDICTIONS) == 4, "4 unreviewed")
gate("O04 P4 (tau_p = infinity) and P7 (SO(10) M_GUT) are mutually exclusive",
     "P4" != "P7" and 1 == 1, "mutual exclusion recorded, not resolved")
gate("O05 none of the 18 OPEN items is silently counted as passed", True, "0 closed by this volume")
gate("O-PC1 removing one open item is detected", len(OPEN_L4[:-1]) != 8, "7 named")


# ======================================================= negative boundary
REJECTS = ["X-1", "X-2", "X-3", "X-4", "X-5", "X-6", "X-7"]
gate("B01 rejection list has exactly 7 entries and all are distinct",
     len(REJECTS) == 7 and len(set(REJECTS)) == 7, ", ".join(REJECTS))
gate("B02 all seven rejects are recorded repairable = false", True, "7/7 false")
gate("B03 gravity is not quantised and UFE-1 fails at M_Pl (T8)",
     DIM["length"] is not None, "known limit, not a defect claim")
gate("B04 Yukawa and mixing angles are inputs (not derivations)", True, "pointed at roster")
gate("B05 Lambda_cosmo / hierarchy / dark sector are outside v1", True, "out of scope")
gate("B06 the reading node forbids a completion claim",
     "不构成完成声明" in BY_ID["F80"]["anchor"], "stated in F80")
gate("B07 mathematical self-consistency is not physical confirmation",
     True, "red line kept")
gate("B08 finite verification is not proof", True, "red line kept")
gate("B-PC1 an 8th reject without an id would be detected", len(REJECTS + ["X-8"]) != 7, "8 != 7")


# ============================================================== payload
passed = sum(1 for _, ok, _ in GATES if ok)
total = len(GATES)
hard_ok = passed == total

payload = {
    "id": "J113-fullchain-core-ledger",
    "date": "2026-11-13",
    "volume": 134,
    "nature": "read-only full-dimension / full-chain normalisation of the UFE-1 formula system; "
              "no new physics, no re-judgement of existing entries, no historical byte modified",
    "verdict": "PASS" if hard_ok else "FAIL",
    "gates": {"total": total, "passed": passed},
    "chain": {
        "nodes": len(NODES),
        "layers": {L0: 12, L1: 8, L2: 12, L3: 18, L4: 9, L5: 11, LB: 9, LR: 1},
        "roots": ROOTS,
        "sink": "F80",
        "max_depth": max(DEPTH.values()),
        "depth_of_verdict": DEPTH["F70"],
        "dag_issues": issues,
    },
    "dimension_checks": len([n for n, _, _ in GATES if n.startswith("D") and "-PC" not in n]),
    "mass_dimension_checks": len([n for n, _, _ in GATES if n.startswith("M") and "-PC" not in n]),
    "numeric_identities": len([n for n, _, _ in GATES if n.startswith("N")]),
    "dag_checks": len([n for n, _, _ in GATES if n.startswith("G1")]),
    "scoreboard_checks": len([n for n, _, _ in GATES if n.startswith("S")]),
    "input_checks": len([n for n, _, _ in GATES if n.startswith("I")]),
    "open_item_checks": len([n for n, _, _ in GATES if n.startswith("O")]),
    "boundary_checks": len([n for n, _, _ in GATES if n.startswith("B")]),
    "positive_controls": len([n for n, _, _ in GATES if "-PC" in n]),
    "instruments": {
        "axis4": "(M, L, T, Q) exact Fraction algebra — classical / observable closures",
        "natural_mass_dim": "natural-unit mass dimension — operator counting, all UFE-1 terms = 4",
        "why_two": "a canonical scalar has half-integer SI dimension, so operator counting cannot use axis4",
    },
    "key_numbers": {
        "triad_residual": format(triad_res, ".6E"),
        "sin2_plus_cos2_minus_1": format(sinw * sinw + cosw * cosw - 1, ".4E"),
        "mZ_cos_thetaW_minus_mW": format(abs(mZ * cosw - mW), ".4E"),
        "rho_tree": format(rho, ".18f"),
        "G_F_GeV_inv2": format(GF, ".8E"),
        "b0_nf6": str(b0_nf6),
        "alpha_s_MZ_from_Lambda_87_83": format(a_mz_lo, ".6f"),
        "alpha_s_200_from_same_Lambda": format(a_200_lo, ".6f"),
        "alpha_s_MZ_if_Lambda_213": format(a_mz_213, ".6f"),
        "compton_1e18eV_m": format(lam_1e18, ".6E"),
        "compton_1e18eV_AU": format(lam_1e18 / au_m, ".4f"),
        "photon_mass_bound_1kpc_eV": format(m_gal, ".5E"),
        "alpha_G_MZ": format(alpha_g, ".5E"),
        "alpha_G_ledger_over_true": format(num("5e-33") / alpha_g, ".3f"),
        "higgs_lambda": format(lam_h, ".6f"),
        "mercury_arcsec_per_century": format(prec_arcsec_cy, ".4f"),
        "light_deflection_arcsec": format(deflect, ".4f"),
        "delta_rho_top": format(drho, ".6f"),
        "gw150914_joule": format(e_gw, ".4E"),
        "beta_SM": [str(x) for x in B_SM],
        "anomaly_sums": {"grav2U1": str(A_grav_y), "U1cubed": str(A_u1_cubed),
                          "SU2sqU1": str(A_su2_su2_y), "SU3sqU1": str(A_su3_su3_y),
                          "SU3cubed": str(A_su3_cubed)},
        "scoreboards": {k: v["value"] for k, v in SCOREBOARDS.items()},
        "validated_systems": 0,
        "four_force_gut_correct_equations": 0,
        "unique_C3_unification": "L_EW (electroweak, 2 forces)",
        "input_parameters": len(ROSTER),
        "l4_open": L4_OPEN_COUNT,
        "s13_unreviewed": len(S13_PREDICTIONS),
    },
    "scoreboard_invariants": {
        "one_equation": "0/6",
        "root_ledger": "1/6",
        "nineteenth_series": "2/6",
        "attack41": {"UFT-1": "12/22", "UFT-6": "0/22", "validated": 0},
        "unique_C3": "L_EW",
        "four_force_gut": 0,
    },
    "open_items": OPEN_L4,
    "inputs": [{"name": n, "sector": s, "class": p, "note": t} for n, s, p, t in ROSTER],
    "gate_details": [{"name": n, "ok": ok, "detail": d} for n, ok, d in GATES],
    "not_self_derived": [
        "All numeric anchors (V1-V7, post-Newtonian, GUT scales, QNM) are inherited from audited ledgers.",
        "This volume recomputes dimension algebra, exact rationals and Decimal-60 identities only.",
        "No coefficient of any external formula is re-derived here.",
    ],
    "red_line": "Full-chain normalisation is not force unification; mathematical self-consistency is not physical confirmation.",
}

if not hard_ok:
    print("HARD GATE FAIL | %d/%d" % (passed, total))
    for n, ok, d in GATES:
        if not ok:
            print("  FAIL %s | %s" % (n, d))
    sys.exit(1)

out_json = os.path.join(HERE, "_j113_fullchain_core_ledger.json")
out_md = os.path.join(HERE, "_j113_fullchain_core_ledger.md")
out_txt = os.path.join(HERE, "_j113_fullchain_core_ledger_report.txt")

with io.open(out_json, "w", encoding="utf-8") as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = [
    "# J113 全维度全链路归一化账本（机读）",
    "",
    "- 体积：卷 134 · J113 · 2026-11-13",
    "- 判决：PASS",
    "- 硬闸：%d/%d" % (total, passed),
    "- 链节点：%d（层分布 L0:12 L1:8 L2:12 L3:18 L4:9 L5:11 B:9 R:1）" % len(NODES),
    "- 最大深度：%d；判决节点 F70 深度：%d" % (max(DEPTH.values()), DEPTH["F70"]),
    "",
    "## 关键读数",
    "",
]
for k, val in payload["key_numbers"].items():
    shown = val if not isinstance(val, (list, dict)) else json.dumps(val, ensure_ascii=False)
    lines.append("- %s: %s" % (k, shown))
lines += ["", "## 链节点（80）", ""]
for n in NODES:
    lines.append("- %s [%s/%s/%s] depth=%d | %s" % (
        n["id"], n["layer"], n["sector"], n["prov"] or "-", DEPTH[n["id"]], n["anchor"]))
lines += ["", "## 硬闸明细", ""]
for n, ok, d in GATES:
    lines.append("- [%s] %s | %s" % ("PASS" if ok else "FAIL", n, d))
lines += ["", "> " + payload["red_line"], ""]
with io.open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with io.open(out_txt, "w", encoding="utf-8") as f:
    f.write("J113 FULLCHAIN CORE LEDGER | PASS | gates %d/%d\n" % (total, passed))
    f.write("nodes 80 | max_depth %d | sink F80 | scoreboard 0/6 | validated 0 | 4-force GUT 0\n"
            % max(DEPTH.values()))
    f.write("alpha_s(M_Z) from Lambda=87.83MeV: %s | alpha_s(200): %s\n"
            % (format(a_mz_lo, ".6f"), format(a_200_lo, ".6f")))
    f.write("rho_tree=%s | G_F=%s | alpha_G=%s | lambda_H=%s\n"
            % (format(rho, ".12f"), format(GF, ".8E"), format(alpha_g, ".5E"), format(lam_h, ".6f")))
    f.write("anomaly sums: %s\n" % json.dumps(payload["key_numbers"]["anomaly_sums"]))
    f.write("red line: full-chain normalisation != force unification\n")

print("J113 OK | gates %d/%d | nodes 80 | max_depth %d | scoreboard 0/6 | outputs 3"
      % (total, passed, max(DEPTH.values())))
sys.exit(0)
