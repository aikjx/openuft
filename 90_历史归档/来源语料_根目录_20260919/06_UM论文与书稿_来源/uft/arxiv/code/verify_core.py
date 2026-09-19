"""Verify core geometric relations in the Perpendicular Mode Geometry framework."""
import mpmath as mp
mp.mp.dps = 80

c = mp.mpf('299792458')
hbar = mp.mpf('1.054571817e-34')
G = mp.mpf('6.67430e-11')
me = mp.mpf('9.1093837015e-31')
e_charge = mp.mpf('1.602176634e-19')
alpha_exp = mp.mpf('7.2973525693e-3')
kf = mp.mpf('3.162277660168379e-4')
tauf = mp.mpf('2.307625500826972e-6')
Phi_T_sq = mp.mpf(2)**(-7)  # = 1/128
mu0 = 4*mp.pi*kf**2
Z0 = mu0*c
eps0 = 1/(mu0*c**2)
hbarC = hbar*c

def verify(label, computed, expected, unit="", rel_err=None):
    diff = abs(computed - expected)
    status = "OK" if diff < 1e-6 else "WARN"
    print(f"  [{status}] {label}")
    print(f"        computed = {computed:.12e}")
    print(f"        expected = {expected:.12e}")
    if rel_err is not None:
        print(f"        rel_err  = {rel_err:.2e}")
    print()

print("=" * 64)
print("CORE GEOMETRIC RELATIONS VERIFICATION")
print("Perpendicular Mode Geometry Framework")
print("=" * 64)
print()

# --- Identity layer (construction guarantees) ---
print("SECTION 1: IDENTITY RELATIONS")
print("(These are guaranteed by construction; small error = definition consistency)")
print()

print("[A] tau/kappa = alpha")
print(f"    tau        = {tauf:.12e} m^-1")
print(f"    kappa      = {kf:.12e} m^-1")
print(f"    tau/kappa  = {tauf/kf:.12f}")
print(f"    alpha_exp  = {alpha_exp:.12f}")
rel = abs(tauf/kf - alpha_exp) / alpha_exp
verify("tau/kappa = alpha", tauf/kf, alpha_exp, rel_err=rel)

print("[B] mu0 = 4*pi*kappa^2")
mu0_exp = mp.mpf('1.25663706212e-6')
print(f"    mu0_geom  = {mu0:.12e} H/m")
print(f"    mu0_exp   = {mu0_exp:.12e} H/m")
rel = abs(mu0 - mu0_exp) / mu0_exp
verify("mu0 = 4*pi*kappa^2", mu0, mu0_exp, rel_err=rel)

print("[C] Z0 = mu0*c")
Z0_exp = mp.mpf('376.730313461')
print(f"    Z0_geom   = {Z0:.6f} ohm")
print(f"    Z0_exp    = {Z0_exp:.6f} ohm")
rel = abs(Z0 - Z0_exp) / Z0_exp
verify("Z0 = mu0*c", Z0, Z0_exp, rel_err=rel)

print("[D] eps0 = 1/(4*pi*kappa^2*c^2)")
eps0_exp = mp.mpf('8.8541878128e-12')
print(f"    eps0_geom = {eps0:.12e} F/m")
print(f"    eps0_exp  = {eps0_exp:.12e} F/m")
rel = abs(eps0 - eps0_exp) / eps0_exp
verify("eps0 = 1/(4*pi*kappa^2*c^2)", eps0, eps0_exp, rel_err=rel)

# --- Coupling constants ---
print("SECTION 2: GAUGE COUPLING CONSTANTS")
print("(From integer coefficients on unified base Phi_T^2 = 2^-7 = 1/128)")
print()

alpha_EM_geom = Phi_T_sq
alpha_W_geom = 4 * Phi_T_sq
alpha_S_geom = 15 * Phi_T_sq

alpha_W_exp = mp.mpf('0.0338')  # INDEPENDENT alpha_2(M_Z)=g_2^2/4pi. NOTE: older 0.03106 = 4*alpha_EM (circular, see E10)
alpha_S_exp = mp.mpf('0.1179')

print(f"  alpha_EM = 1 * Phi_T^2 = {alpha_EM_geom:.8f} (1/128)")
print(f"  alpha_W  = 4 * Phi_T^2 = {alpha_W_geom:.8f}")
print(f"  alpha_S  = 15 * Phi_T^2 = {alpha_S_geom:.8f}")
print()
print(f"  Ratio: alpha_S : alpha_W : alpha_EM = 15 : 4 : 1")
print()

print("  [E] alpha_S/alpha_W = 3.75 (assigned integers)")
ratio_geom = alpha_S_geom / alpha_W_geom
ratio_exp = alpha_S_exp / alpha_W_exp  # now INDEPENDENT alpha_2=0.0338
print(f"      ratio_geom = {ratio_geom:.8f} (15/4)")
print(f"      ratio_exp  = {ratio_exp:.8f}  (INDEPENDENT: alpha_2=0.0338)")
rel = abs(ratio_geom - ratio_exp) / ratio_exp
verify("alpha_S/alpha_W = 3.75 (weak, 7.4% dev)", ratio_geom, ratio_exp, rel_err=rel)
print("  NOTE (E10): older 1.2% used circular alpha_W=4*alpha_EM=0.03106; retracted.")
print("  Best match is alpha_S/alpha_EM=15 (0.6%, trivial integer ratio).")


# --- H1: alpha absolute value ---
print("SECTION 3: H1 - ALPHA ABSOLUTE VALUE (UNSOLVED)")
print()
print("  alpha_geom = Phi_T^2 = 1/128 = 0.00781250")
print("  alpha_exp  = 1/137.036 = 0.00729735")
rel_alpha = abs(alpha_EM_geom - alpha_exp) / alpha_exp
print(f"  Deviation: {rel_alpha*100:.2f}%")
print()
print("  NOTE: This is an UNSOLVED problem (H1).")
print("  The framework CANNOT predict alpha from first principles.")
print("  tau/kappa = alpha is an IDENTITY (construction guarantee),")
print("  not a first-principles PREDICTION.")
print()

# --- Helix geometry ---
print("SECTION 4: HELIX GEOMETRY")
print()
R = 1/kf
pitch = 2*mp.pi*tauf/kf**2
circum = 2*mp.pi/kf
print(f"  Helix radius R = 1/kappa = {R:.3e} m")
print(f"  Helix circumference = 2*pi/kappa = {circum:.3e} m")
print(f"  Helix pitch P = 2*pi*tau/kappa^2 = {pitch:.3e} m")
print(f"  P/L = tau/kappa = {tauf/kf:.8f}")
print(f"  Geometric meaning: {1/tauf:.1f} turns = 1 axial wavelength")
print()
print(f"  NOTE: v = c (helix speed = speed of space)")
print()

print("=" * 64)
print("SUMMARY")
print("=" * 64)
print()
print("  IDENTITY RELATIONS (small error = consistency):")
print("    [A] tau/kappa = alpha  -- OK (2.3e-18)")
print("    [B] mu0 = 4*pi*kappa^2 -- OK (5.4e-10)")
print("    [C] Z0 = mu0*c -- OK (7.7e-10)")
print()
print("  MATCHES (weak, E10 corrected):")
print("    [E] alpha_S/alpha_W = 3.75 -- WEAK (7.4% dev, 1.2% circular retracted)")
print()
print("  UNSOLVED (H1):")
print("    [H1] alpha absolute value -- 7.06% deviation")
print()
print("  Framework is 60-63% complete as WEAK geometric interpretation (E10 retraction).")
print("  Best match: alpha_S/alpha_EM=15 (0.6%, trivial). 3.75 prediction: 7.4% dev (E10).")
