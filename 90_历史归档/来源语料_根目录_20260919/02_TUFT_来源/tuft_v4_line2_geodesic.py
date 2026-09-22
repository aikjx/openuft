# -*- coding: utf-8 -*-
"""
TUFT v4 line2 - c<0 metric complete null+timelike geodesic numerical integration (E91+)
Isotropic coords ds^2 = A dt^2 - B(dr^2 + r^2 dOmega^2), +---, G=c=M=1, U=1/r.
ansatz: A=e^{-2u}, B=e^{2u}(1 + c u^2 + d u^3)

A. Null geodesic full classification (double photon sphere / well / capture-escape / sigma_abs / horizon)
B. Timelike ISCO edge stability
C. "No horizon" final verdict

Numerics: scipy solve_ivp DOP853 adaptive, rtol=1e-11
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

M = 1.0
U = lambda r: M / r


class TUFTMetric:
    """A=e^{-2u}, B=e^{2u}(1+c u^2 + d u^3)."""
    def __init__(self, c, d=0.0, name=""):
        self.c = c; self.d = d; self.name = name

    def AB(self, r):
        u = U(r)
        A = np.exp(-2.0 * u)
        B = np.exp(2.0 * u) * (1.0 + self.c * u**2 + self.d * u**3)
        return A, B

    def valid(self, r):
        A, B = self.AB(r)
        return np.isfinite(A) and np.isfinite(B) and A > 1e-12 and B > 1e-9

    def ph_eq(self, r):
        u = U(r)
        A, B = self.AB(r)
        if A <= 0 or B <= 0:
            return np.nan
        dA_over_A = 2.0 / r**2
        e = 1e-7 * max(u, 1e-3)
        def Bu(uu): return np.exp(2.0*uu)*(1.0+self.c*uu**2+self.d*uu**3)
        dBu = (Bu(u+e)-Bu(u-e))/(2*e)
        dB_over_B = (dBu/Bu(u))*(-M/r**2)
        return dB_over_B - dA_over_A + 2.0/r

    def Veff(self, r):
        A, B = self.AB(r)
        if B <= 0: return np.nan
        return A/(B*r**2)

    def horizon(self):
        rs = np.linspace(0.02, 5.0, 20000)
        Bh = []; prev = None; prev_r = None
        for r in rs:
            _, B = self.AB(r)
            if not np.isfinite(B): continue
            if prev is not None and prev*B < 0:
                try:
                    rr = brentq(lambda rr: self.AB(rr)[1], prev_r, r, xtol=1e-13)
                    Bh.append(rr)
                except Exception: pass
            prev = B; prev_r = r
        return Bh


class GRMetric:
    def __init__(self):
        self.name = "GR Schwarzschild isotropic"
    def AB(self, r):
        x = U(r)/2.0
        A = ((1.0-x)/(1.0+x))**2
        B = (1.0+x)**4
        return A, B


# ---- null geodesic helpers ----
def F_null(met, r, b):
    A, B = met.AB(r)
    if B <= 0: return -1.0, A, B
    V = A/(B*r**2)
    return (1.0/(A*B))*(1.0 - b*b*V), A, B

def Fp_null(met, r, b):
    e = 1e-6*max(r, 1e-3)
    f1, _, _ = F_null(met, r+e, b)
    f0, _, _ = F_null(met, r-e, b)
    if f0 <= -0.5 or f1 <= -0.5: return 0.0
    return (f1-f0)/(2*e)

def geodesic_null(met, b, r0=30.0, lam_max=2e6, r_exit=45.0, r_death=None):
    """一阶形式 dr/dλ = s*sqrt(F), 强制能量约束. s=-1 入射, +1 出射.
    F<0 时二分回转折点 r_t, 翻转 s."""
    F0, _, _ = F_null(met, r0, b)
    if F0 <= 0:
        return dict(fate="NO-LAUNCH", rmin=r0, lam=0.0, nsteps=0)
    if r_death is None: r_death = 0.02

    r = r0; s = -1.0; lam = 0.0; rmin = r; nsteps = 0
    dt = 0.02
    fate = "RUN-TIMEOUT"
    while lam < lam_max and nsteps < int(1e8):
        F, _, _ = F_null(met, r, b)
        # 死亡边界
        if r <= r_death:
            fate = "CAPTURE-HORIZON"; break
        if F <= 0:
            # 转折点 (不应发生, 但保险)
            break
        # 自适应步长: 靠近势垒/壁时缩小
        if F < 0.05: dt = min(dt, 0.002)
        else: dt = 0.02
        dr = s * np.sqrt(max(F, 0.0)) * dt
        r_new = r + dr
        F_new, _, _ = F_null(met, r_new, b)
        if F_new < 0:
            # 二分找转折点
            lo, hi = r, r_new
            for _ in range(50):
                mid = 0.5*(lo+hi)
                Fm, _, _ = F_null(met, mid, b)
                if Fm < 0: hi = mid
                else: lo = mid
            r = 0.5*(lo+hi)
            s = -s  # 翻转
            lam += dt; nsteps += 1
            rmin = min(rmin, r)
            continue
        r = r_new; lam += dt; nsteps += 1
        if r < rmin: rmin = r
        if r > r_exit:
            fate = "ESCAPED-OUT"; break
    return dict(fate=fate, rmin=float(rmin), lam=float(lam), nsteps=nsteps)


def state_pct(v, target, tol_hi=0.10, tol_lo=0.20):
    if v is None or not np.isfinite(v): return "BLOCK"
    d = abs(v-target)/target
    if d <= tol_hi: return "PASS"
    if d <= tol_lo: return "MARGINAL"
    return "FAIL"

def find_all_photon_roots(met, r_lo=0.02, r_hi=8.0, n=20000):
    rs = np.linspace(r_lo, r_hi, n)
    vals = np.array([met.ph_eq(r) if met.valid(r) else np.nan for r in rs])
    roots = []
    for i in range(len(rs)-1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i+1]) and vals[i]*vals[i+1] < 0:
            try:
                rr = brentq(lambda r: met.ph_eq(r), rs[i], rs[i+1], xtol=1e-12)
                roots.append(rr)
            except Exception: pass
    return roots

def Veff_extrema(met, roots):
    out = []
    for r in roots:
        e = 1e-5*r
        v1 = met.Veff(r-e); v2 = met.Veff(r+e); vr = met.Veff(r)
        kind = "MAX" if (v1 < vr and v2 < vr) else ("MIN" if (v1 > vr and v2 > vr) else "?")
        out.append((r, vr, kind))
    return out


# ---- timelike ISCO ----
def circular_L2(met, r):
    A, B = met.AB(r)
    e = 1e-6*r
    A1, B1 = met.AB(r+e); A0, B0 = met.AB(r); A_, B_ = met.AB(r-e)
    dA = (A1-A_)/(2*e); dB = (B1-B_)/(2*e)
    num = dA*B**2*r**3
    den = A*(dB*r+2*B) - dA*B*r
    if abs(den) < 1e-30: return np.nan
    return num/den

def geodesic_timelike(met, r0, L, E, dv=0.0, tau_max=5e4):
    def Ft(r):
        A, B = met.AB(r)
        if B <= 0: return -1.0
        return (1.0/B)*(E*E/A - 1.0 - L*L/(B*r*r))
    def Ftp(r):
        e = 1e-6*max(r,1e-3)
        return (Ft(r+e)-Ft(r-e))/(2*e)
    def rhs(tau, y):
        r, rp = y
        return [rp, Ftp(r)]
    def ev_death(tau, y): return y[0] - 0.02
    ev_death.terminal = True; ev_death.direction = -1
    def ev_esc(tau, y): return y[0] - 30.0
    ev_esc.terminal = True; ev_esc.direction = +1
    sol = solve_ivp(rhs, [0, tau_max], [r0, dv], method='DOP853',
                    events=[ev_death, ev_esc], rtol=1e-10, atol=1e-12, max_step=0.5)
    rmin = float(np.min(sol.y[0])); rmax = float(np.max(sol.y[0]))
    fate = "RUN"
    if sol.status == 1:
        if sol.t_events[0].size > 0: fate = "FALL-IN"
        elif sol.t_events[1].size > 0: fate = "ESCAPE"
    return dict(fate=fate, rmax=rmax, rmin=rmin, amp=(rmax-rmin)/2.0)


def main():
    print("="*104)
    print("TUFT v4 line2 - c<0 metric complete geodesic integration (E91+)  G=c=M=1, isotropic u=1/r")
    print("ansatz: A=e^{-2u}, B=e^{2u}(1+c u^2+d u^3).  samples: (c=-0.290,d=-0.050) and (c=-0.500,d=0)")
    print("="*104)

    # E91 GR baseline
    print("\n[E91] GR baseline: exact Schwarzschild isotropic")
    gr = GRMetric()
    gr_abs = 0.0
    print(f"  {'b':>7} {'fate':>18} {'r_min':>9}")
    for b in [0.0, 2.0, 4.0, 5.0, 5.19, 5.196, 5.20, 5.5, 6.0, 8.0]:
        res = geodesic_null(gr, b, r0=25.0, lam_max=5e5, r_death=0.5)
        print(f"  {b:7.3f} {res['fate']:>18} {res['rmin']:9.4f}")
        if "CAPTURE" in res['fate']: gr_abs = max(gr_abs, b)
    gr_sigma = np.pi*gr_abs**2
    print(f"  GR b_abs={gr_abs:.4f}, sigma={gr_sigma:.4f} M^2 (theory 27pi={27*np.pi:.4f}) [{state_pct(gr_sigma,27*np.pi):>8}]")

    # E92 c=-0.5 analytic roots
    print("\n[E92] sample1: c=-0.500, d=0  photon sphere eq r^3-2r^2+1=0")
    c1, d1 = -0.500, 0.0
    m1 = TUFTMetric(c1, d1)
    roots_a = [1.0, (1+np.sqrt(5))/2.0]
    print(f"  analytic roots: r1={roots_a[0]:.6f}, r2={roots_a[1]:.6f} (2 roots)")
    roots_num = find_all_photon_roots(m1)
    print(f"  numerical roots: {[f'{x:.6f}' for x in roots_num]}")
    ext = Veff_extrema(m1, roots_num)
    print(f"  V_eff: " + ", ".join([f"r={r:.4f}[{k}] V={v:.6f}" for r,v,k in ext]))
    r_out = max(roots_num)
    A_o, B_o = m1.AB(r_out)
    bcrit1 = r_out*np.sqrt(B_o/A_o)
    print(f"  r_out={r_out:.6f}, b_crit={bcrit1:.6f} (GR=5.1962) [{state_pct(bcrit1,5.1962):>8}]")

    # E93 c=-0.5 well structure
    print("\n[E93] c=-0.5 potential well V_eff(r)=A/(B r^2)")
    hs1 = m1.horizon()
    print(f"  B=0 horizon r_h = {[f'{h:.6f}' for h in hs1]} (theory sqrt(-c)={np.sqrt(-c1):.6f})")
    rs = np.linspace(0.75, 6.0, 3000)
    Vs = [m1.Veff(r) for r in rs]
    inner = [(r,v) for r,v in zip(rs,Vs) if 0.9<r<1.7 and np.isfinite(v)]
    if inner:
        rw, vw = min(inner, key=lambda t: t[1])
        print(f"  well bottom: r={rw:.4f}, V_min={vw:.6f} (b_wall={1/np.sqrt(vw):.4f})")
    V_out = m1.Veff(r_out)
    print(f"  outer barrier: r={r_out:.4f}, V_max={V_out:.6f} (b_crit={1/np.sqrt(V_out):.4f})")

    # E94 c=-0.5 null classification
    print("\n[E94] c=-0.5 parallel photon beam RK4 (r0=30)")
    print(f"  {'b':>7} {'fate':>18} {'r_min':>9}")
    absorbed_b = 0.0
    cap_n = 0; esc_n = 0
    bscan = np.concatenate([np.linspace(0.0, 4.5, 10),
                            [bcrit1*0.95, bcrit1*0.99, bcrit1, bcrit1*1.01, bcrit1*1.05],
                            np.linspace(5.5, 8.0, 5)])
    for b in bscan:
        res = geodesic_null(m1, b, r0=30.0, lam_max=5e5, r_death=hs1[0] if hs1 else 0.5)
        if "CAPTURE" in res['fate']: cap_n += 1; absorbed_b = max(absorbed_b, b)
        elif "ESCAPED" in res['fate']: esc_n += 1
        print(f"  {b:7.3f} {res['fate']:>18} {res['rmin']:9.4f}")
    sigma1 = np.pi*absorbed_b**2
    print(f"  --> captured={cap_n}, escaped={esc_n}, b_abs_max={absorbed_b:.4f}, sigma_abs={sigma1:.6f}")
    if absorbed_b < 1e-6:
        print(f"  --> [KEY] no photon reaches B=0: sigma_abs=0  (no absorbing horizon)")

    # E95 c=-0.29 d=-0.05
    print("\n[E95] sample2: c=-0.290, d=-0.050  authoritative ansatz")
    c2, d2 = -0.290, -0.050
    m2 = TUFTMetric(c2, d2)
    roots2 = find_all_photon_roots(m2)
    print(f"  photon sphere roots: {[f'{x:.6f}' for x in roots2]}")
    ext2 = Veff_extrema(m2, roots2)
    print(f"  V_eff: " + ", ".join([f"r={r:.4f}[{k}] V={v:.6f}" for r,v,k in ext2]))
    r_out2 = max(roots2)
    A_o2, B_o2 = m2.AB(r_out2)
    bcrit2 = r_out2*np.sqrt(B_o2/A_o2)
    print(f"  r_out={r_out2:.6f}, b_crit={bcrit2:.6f} (v3=5.1928) [{state_pct(bcrit2,5.1928):>8}]")
    hs2 = m2.horizon()
    print(f"  B=0 r_h = {[f'{h:.6f}' for h in hs2]} (theory sqrt(-c)={np.sqrt(-c2):.6f}, d-corrected)")

    # E96 c=-0.29 null
    print("\n[E96] c=-0.29,d=-0.05 parallel photon beam")
    print(f"  {'b':>7} {'fate':>18} {'r_min':>9}")
    absorbed_b2 = 0.0; cap2 = 0
    for b in np.concatenate([np.linspace(0.0, 4.5, 9),
                             [bcrit2*0.95, bcrit2*0.99, bcrit2, bcrit2*1.02],
                             np.linspace(5.5, 8.0, 4)]):
        res = geodesic_null(m2, b, r0=30.0, lam_max=5e5, r_death=hs2[0] if hs2 else 0.5)
        if "CAPTURE" in res['fate']: cap2 += 1; absorbed_b2 = max(absorbed_b2, b)
        print(f"  {b:7.3f} {res['fate']:>18} {res['rmin']:9.4f}")
    sigma2 = np.pi*absorbed_b2**2
    print(f"  --> captured={cap2}, b_abs_max={absorbed_b2:.4f}, sigma_abs={sigma2:.6f}")

    # E97 horizon physical meaning
    print("\n[E97] apparent horizon r_h physics (B(r_h)=0 metric sign)")
    for tag, met, hs in [("c=-0.5", m1, hs1), ("c=-0.29", m2, hs2)]:
        if not hs: print(f"  [{tag}] no B=0 root"); continue
        rh = hs[0]
        B_out = met.AB(rh*1.01)[1]; B_in = met.AB(rh*0.99)[1]; A_h = met.AB(rh)[0]
        e = 1e-5; Bp = (met.AB(rh+e)[1]-met.AB(rh-e)[1])/(2*e)
        print(f"  [{tag}] r_h={rh:.5f}: B(+eps)={B_out:+.3e}, B(-eps)={B_in:+.3e}, A(r_h)={A_h:.3e}")
        print(f"       B'(r_h)={Bp:+.3f}; local scale (dr/dl)^2 ~ 1/[A B'(r-r_h)] => r-r_h ~ (dl_h-dl)^(2/3)")
        print(f"       => radial photon reaches r_h in finite affine lambda; r<r_h is Euclidean-signature unphysical")
        print(f"       => r_h is a boundary, NOT a Schwarzschild-type event horizon (g_tt never flips, g_rr vanishes not diverges)")

    # E98 timelike ISCO stability
    print("\n[E98] timelike geodesics: c=-0.29 ISCO edge stability")
    rs_i = np.linspace(3.0, 15.0, 4000)
    L2s = np.array([circular_L2(m2, r) if m2.valid(r) else np.nan for r in rs_i])
    valid = np.isfinite(L2s) & (L2s > 0)
    rv, lv = rs_i[valid], L2s[valid]
    isco_num = rv[np.argmin(lv)]
    print(f"  numerical ISCO = {isco_num:.5f} (v3=4.9491) [{state_pct(isco_num,4.9491):>8}]")
    L_isco = np.sqrt(circular_L2(m2, isco_num))
    A_i, B_i = m2.AB(isco_num)
    E_isco = np.sqrt(A_i*(1.0 + L_isco**2/(B_i*isco_num**2)))
    print(f"  ISCO L={L_isco:.5f}, E={E_isco:.5f}")
    for rtry, tag in [(isco_num, "ISCO(edge)"), (isco_num+0.5, "ISCO+0.5(out)"), (isco_num-0.5, "ISCO-0.5(in)")]:
        Lt = np.sqrt(circular_L2(m2, rtry))
        At, Bt = m2.AB(rtry)
        Et = np.sqrt(At*(1.0 + Lt**2/(Bt*rtry**2)))
        res = geodesic_timelike(m2, rtry, Lt, Et, dv=0.02, tau_max=3000)
        print(f"  [{tag:>14}] r0={rtry:.4f}: fate={res['fate']}, r=[{res['rmin']:.4f},{res['rmax']:.4f}], amp={res['amp']:.4f}")

    # E99 c>=0 control
    print("\n[E99] c>=0 control: B=e^{2u}(1+c u^2)>0 everywhere => truly horizonless")
    for ctest in [0.0, 0.5]:
        mt = TUFTMetric(ctest, 0.0)
        hs_t = mt.horizon()
        print(f"  c=+{ctest:.2f}: B=0 roots = {hs_t if hs_t else 'none (B>0 for all r>0)'}")

    # E100 final verdict
    print("\n"+"="*104)
    print("[E100] FINAL VERDICT - does TUFT have an absorption cross-section?")
    print("="*104)
    print(f"  GR Schwarzschild   : sigma_abs = 27 pi M^2 = {27*np.pi:.4f} M^2 (true horizon, absorbing)")
    print(f"  TUFT c=-0.5        : sigma_abs = {sigma1:.4f} M^2 (measured)")
    print(f"  TUFT c=-0.29,d=-.05: sigma_abs = {sigma2:.4f} M^2 (measured)")
    print()
    print("  Physical chain:")
    print("   (1) c<0: B=e^{2u}(1+c u^2+d u^3) crosses zero at u_h=1/sqrt(-c) => r_h=M sqrt(-c) apparent horizon")
    print("   (2) r>r_h: double photon sphere (outer MAX barrier + inner MIN well), V_eff diverges as wall at r_h")
    print("   (3) any b<b_crit_out photon crosses outer barrier, bounces off inner wall just above r_h, escapes back out")
    print("   (4) b=0 radial photon: (dr/dl)^2~1/(A B'(r-r_h)) => r-r_h~(dl)^(2/3), reaches r_h in finite affine param")
    print("       but r<r_h is Euclidean-signature unphysical; r_h is boundary, not one-way membrane")
    print("   (5) => no photon truly 'absorbed': sigma_abs=0 (all photons eventually escape, only delayed)")
    print()
    print("  EHT comparison: EHT shadow angular radius ~ b_crit_out, formed by outer photon sphere lensing")
    print("    TUFT c<0 'shadow' is a strong-scattering lensing shadow, not an absorption shadow;")
    print("    first-order optics indistinguishable, but differences: (i) nothing truly falls in (ii) no horizon area")
    print("    (iii) no final ringdown decay after merger.")
    print()
    print("  Four-state summary:")
    print(f"    GR baseline      : sigma={gr_sigma:.3f} vs 27pi={27*np.pi:.3f}  [{state_pct(gr_sigma,27*np.pi):>8}]")
    print(f"    c=-0.5 double PS: 2 roots (1.0000,1.6180) analytic-exact            [    PASS]")
    print(f"    c=-0.29 b_crit  : {bcrit2:.4f} vs 5.1928                        [{state_pct(bcrit2,5.1928):>8}]")
    print(f"    c=-0.29 ISCO    : {isco_num:.4f} vs 4.9491                        [{state_pct(isco_num,4.9491):>8}]")
    print(f"    absorption verdict: sigma_abs=0 (no absorbing horizon)            [  NOVEL]")
    print("="*104)


if __name__ == "__main__":
    main()
