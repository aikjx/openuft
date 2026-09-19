# -*- coding: utf-8 -*-
"""
TUFT v2 strong-field numerical calculation.
Isotropic metric ds^2 = A dt^2 - B(dr^2 + r^2 dOmega^2), +--- signature, G=c=M=1.
  U = 1/r
  A(r) = exp(-2U)
  B(r) = exp(+2U)(1 + c U^2)
  exact: A*B = 1 + c U^2;  B/A = exp(4U)(1+cU^2)

Null geodesic (equatorial):
  E = A dt/dlambda, L = B r^2 dphi/dlambda, b = L/E
  (dr/dphi)^2 = B r^4/(A b^2) - r^2
  dphi/dr = sqrt(A/B) b / [ r sqrt(r^2 - (A/B) b^2) ]
Photon sphere: d ln(B/A)/dr = -2/r
ISCO: d L^2/dr = 0, L^2 = A' B^3 r^3 / [2A(B'r+B) - A'B r]
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

M = 1.0


def AB(c, r):
    U = M / r
    A = np.exp(-2.0 * U)
    B = np.exp(2.0 * U) * (1.0 + c * U * U)
    return A, B


def dAB(c, r):
    U = M / r
    A = np.exp(-2.0 * U)
    B = np.exp(2.0 * U) * (1.0 + c * U * U)
    dUdr = -M / r ** 2
    dA = A * (-2.0 * dUdr)
    dB = B * dUdr * (2.0 + 2.0 * c * U / (1.0 + c * U * U))
    return A, B, dA, dB


# ---- E26: photon sphere ----
def ph_eq(c, r):
    A, B, dA, dB = dAB(c, r)
    return dB / B - dA / A + 2.0 / r


def find_rph(c):
    r_lo = M * 0.3
    if c < 0:
        r_lo = M / np.sqrt(-1.0 / c) * 1.001
    rs = np.linspace(r_lo, M * 50, 80000)
    vals = []
    for r in rs:
        try:
            vals.append(ph_eq(c, r))
        except Exception:
            vals.append(np.nan)
    vals = np.array(vals)
    roots = []
    for i in range(len(rs) - 1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i+1]) and vals[i] * vals[i+1] < 0:
            try:
                rr = brentq(lambda r: ph_eq(c, r), rs[i], rs[i+1], xtol=1e-12)
                roots.append(rr)
            except Exception:
                pass
    return roots


# ---- E27: ISCO ----
def L2_of_r(c, r):
    A, B, dA, dB = dAB(c, r)
    num = dA * B ** 3 * r ** 3
    den = 2.0 * A * (dB * r + B) - dA * B * r
    if abs(den) < 1e-30:
        return np.nan
    return num / den


def find_isco(c):
    r_lo = M * 0.3
    if c < 0:
        r_lo = M / np.sqrt(-1.0 / c) * 1.01
    rs = np.linspace(r_lo, M * 300, 60000)
    L2 = np.array([L2_of_r(c, r) for r in rs])
    valid = np.isfinite(L2) & (L2 > 0)
    rv, lv = rs[valid], L2[valid]
    mins = []
    for i in range(1, len(rv) - 1):
        if lv[i] < lv[i-1] and lv[i] < lv[i+1]:
            mins.append(rv[i])
    if not mins:
        return None
    r0 = min(mins)
    idx = np.argmin(np.abs(rv - r0))
    lo = rv[max(0, idx-10)]
    hi = rv[min(len(rv)-1, idx+10)]
    def dL2(r):
        e = 1e-7 * r
        return (L2_of_r(c, r+e) - L2_of_r(c, r-e)) / (2*e)
    try:
        return brentq(dL2, lo, hi, xtol=1e-12)
    except Exception:
        return r0


# ---- E28: deflection angle ----
def find_rmin(c, b, rmax=1e6):
    def f(r):
        A, B, _, _ = dAB(c, r)
        return r*r - (A/B)*b*b
    r_lo = M*0.3
    if c < 0:
        r_lo = M/np.sqrt(-1.0/c)*1.01
    # scan downward from b to find first sign change
    r_try = b*1.5
    while r_try > r_lo and f(r_try) >= 0:
        r_try *= 0.9
    if f(r_try) >= 0:
        return None
    return brentq(f, r_try, b*1.5, xtol=1e-12)


def deflection(c, b, rmax=1e6):
    rmin = find_rmin(c, b, rmax)
    if rmin is None:
        return np.nan
    def integ(r):
        A, B, _, _ = dAB(c, r)
        s = A/B
        return np.sqrt(s)*b / (r*np.sqrt(max(r*r - s*b*b, 1e-30)))
    val, _ = quad(integ, rmin, rmax, limit=300, epsabs=1e-11)
    return 2.0*val - np.pi


# ---- E29: critical impact parameter ----
def b_crit(c, rph):
    A, B, _, _ = dAB(c, rph)
    return rph * np.sqrt(B/A)


# ---- GR isotropic coordinate check ----
def gr_iso(r):
    x = M/(2.0*r)
    A = ((1-x)/(1+x))**2
    B = (1+x)**4
    dx = -M/(2.0*r**2)
    dA = A*(2*(-dx)/(1-x) - 2*dx/(1+x))
    dB = B*4*dx/(1+x)
    return A, B, dA, dB


def gr_tests():
    print("="*74)
    print("GR isotropic-coordinate check (G=c=M=1)")
    print("="*74)
    x_ph = 2.0 - np.sqrt(3.0)
    rph_iso = M/(2.0*x_ph)
    print(f"  GR isotropic r_ph = {rph_iso:.6f} M (Schwarzschild coord 3M)")
    A, B, _, _ = gr_iso(rph_iso)
    bc_iso = rph_iso*np.sqrt(B/A)
    print(f"  GR isotropic b_crit = {bc_iso:.6f} M (Schwarzschild coord 3sqrt(3)={3*np.sqrt(3):.6f})")
    y_isco = brentq(lambda y: y*(1+1/(2*y))**2 - 6, 1, 20)
    print(f"  GR isotropic ISCO = {y_isco:.6f} M (Schwarzschild coord 6M)")
    def defl_gr(b):
        def f(r):
            A,B,_,_ = gr_iso(r)
            return r*r - (A/B)*b*b
        rmin = brentq(f, 1.0, 1e6, xtol=1e-12)
        def integ(r):
            A,B,_,_ = gr_iso(r)
            s=A/B
            return np.sqrt(s)*b/(r*np.sqrt(r*r-s*b*b))
        val,_ = quad(integ, rmin, 1e6, limit=300, epsabs=1e-11)
        return 2*val-np.pi
    print(f"  GR deflection @ b=10M = {defl_gr(10.0):.6f} rad (1PN=0.400000)")
    print(f"  GR deflection @ b=100M = {defl_gr(100.0):.6f} rad (1PN=0.040000)")
    print()


def main():
    gr_tests()
    cs = [0.0, -0.25, -0.5, -1.0, +0.5]
    print("="*74)
    print("TUFT v2 scan (natural units G=c=M=1)")
    print("="*74)
    print(f"{'c':>8} {'r_ph':>10} {'ISCO':>10} {'b_crit':>10} {'defl@10M':>10}  note")
    print("-"*74)
    R = {}
    for c in cs:
        roots = find_rph(c)
        rph = roots[0] if roots else None
        ri = find_isco(c)
        bc = b_crit(c, rph) if rph else None
        df = deflection(c, 10.0) if rph else (0.0 if c == 0 else np.nan)
        notes = []
        if c < 0:
            r_h = M/np.sqrt(-1.0/c)
            notes.append(f"B=0 horizon r_h={r_h:.3f}M")
        else:
            notes.append("no horizon (B>0)")
        if rph is None:
            notes.append("no photon sphere")
        rp_s = f"{rph:.4f}" if rph else "  N/A "
        ri_s = f"{ri:.4f}" if ri else "  N/A "
        bc_s = f"{bc:.4f}" if bc else "  N/A "
        df_s = f"{df:.6f}" if np.isfinite(df) else " nan "
        print(f"{c:>+8.3f} {rp_s:>10} {ri_s:>10} {bc_s:>10} {df_s:>10}  {'; '.join(notes)}")
        R[c] = dict(rph=rph, ri=ri, bc=bc, df=df)

    print("\n"+"="*74)
    print("Detailed values")
    print("="*74)
    for c in cs:
        r = R[c]
        print(f"\n--- c={c:+.3f} ---")
        if r['rph']:
            print(f"  r_ph    = {r['rph']:.8f} M")
            print(f"  b_crit  = {r['bc']:.8f} M")
        else:
            print(f"  r_ph: does not exist")
        if r['ri']:
            print(f"  ISCO    = {r['ri']:.8f} M")
        if np.isfinite(r['df']):
            print(f"  deflect@b=10M = {r['df']:.8f} rad")

    # ---- EHT fine scan: find c range consistent with observation ----
    print("\n"+"="*74)
    print("EHT fine scan: c range for 1-sigma consistency")
    print("="*74)
    G = 6.674e-11; cspeed = 2.998e8; Msun = 1.989e30
    pc = 3.086e16
    Mbh = 6.5e9*Msun; D = 16.8e6*pc
    Rs = G*Mbh/cspeed**2
    theta_gr = 2*3*np.sqrt(3)*Rs/D * 206265*1e6
    # EHT M87* observed ~40 uas, 1-sigma ~ +/-10% (roughly 36-44 uas)
    print(f"  M87*: GR={theta_gr:.1f} uas, EHT obs ~40 uas (1-sigma ~36-44 uas)")
    print(f"  {'c':>8} {'b_crit':>10} {'theta(uas)':>10} {'dev%':>8} {'in1sig?'}")
    cscan = np.linspace(-0.8, 0.8, 65)
    good = []
    for cc in cscan:
        roots = find_rph(cc)
        if not roots:
            continue
        rph = roots[0]
        bc = b_crit(cc, rph)
        th = 2*bc*Rs/D * 206265*1e6
        dev = (th-theta_gr)/theta_gr*100
        in1 = "YES" if abs(th-40.0) < 4.0 else ""
        if in1: good.append(cc)
        if abs(cc) < 0.01 or abs(cc+0.5)<0.01 or abs(cc-0.5)<0.01 or in1:
            print(f"  {cc:>+8.3f} {bc:>10.4f} {th:>10.2f} {dev:>+8.1f} {in1}")
    if good:
        print(f"\n  c in 1-sigma (|theta-40|<4 uas): [{min(good):.3f}, {max(good):.3f}]")

    # weak-field expansion check
    print("\n"+"="*74)
    print("Weak-field 1PN/2PN check (b=100M)")
    print("="*74)
    for c in [0.0, -0.25, -0.5, 0.5]:
        df = deflection(c, 100.0)
        print(f"  c={c:+.2f}: deflect@b=100M = {df:.6f} rad  (GR 1PN=0.040000)")


if __name__ == "__main__":
    main()
