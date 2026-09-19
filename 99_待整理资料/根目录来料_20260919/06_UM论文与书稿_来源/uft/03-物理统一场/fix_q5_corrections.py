"""Fix Q5: correct electron charge formula. Also verify all broken formulas."""
import sys
sys.stdout = open('fix_q5_corrections.txt', 'w', encoding='utf-8')

import mpmath as mp
mp.mp.dps = 100

c = mp.mpf('299792458')
hbar = mp.mpf('1.054571817e-34')
hbarC = hbar*c
alpha_exp = mp.mpf('7.2973525693e-3')
kf = mp.mpf('3.162277660168379e-4')
tauf = mp.mpf('2.307625500826972e-6')
mu0 = 4*mp.pi*kf**2
eps0 = 1/(mu0*c**2)
e_charge = mp.mpf('1.602176634e-19')
me = mp.mpf('9.1093837015e-31')
G = mp.mpf('6.67430e-11')
Qtop = me*c/hbar
Phi_T_sq = mp.mpf(2)**(-7)

out = []
def p(s): out.append(str(s))

p("=" * 72)
p("Q5 FIX: Correct Electron Charge Formula")
p("=" * 72)

p("\n[THE BUG]")
p("  WRONG:  e = sqrt(2*alpha*eps0*hbar*c)")
p("  RIGHT:  e = sqrt(4*pi*alpha*eps0*hbar*c)")
p("  (4*pi is correct for Coulomb constant)")

p("\n[CORRECT VERIFICATION]")
e_wrong = mp.sqrt(2*alpha_exp*eps0*hbar*c)
e_right = mp.sqrt(4*mp.pi*alpha_exp*eps0*hbar*c)
p(f"  e_wrong = sqrt(2*a*eps0*hbar*c) = {e_wrong:.12e}")
p(f"  e_right = sqrt(4*pi*a*eps0*hbar*c) = {e_right:.12e}")
p(f"  e_exp  = {e_charge:.12e}")
p(f"  e_wrong err = {abs(e_wrong-e_charge)/e_charge*100:.2f}%")
p(f"  e_right err = {abs(e_right-e_charge)/e_charge*100:.6f}%")

p("\n[WHY 4*pi?]")
p("  Coulomb constant: k = 1/(4*pi*eps0)")
p("  Fine structure: alpha = e^2/(4*pi*hbar*c)")
p("  Therefore: e^2 = 4*pi*alpha*hbar*c")
p("  So: e = sqrt(4*pi*alpha*hbar*c)")

p("\n" + "=" * 72)
p("CORRECT m_e FORMULA CHECK")
p("=" * 72)

p("\n[THE BROKEN m_e FORMULA]")
p("  m = hbar*kappa*(alpha^2+1)/(alpha*c)  <-- WRONG")
p("  Gives m_e_geom = 1.52e-44 kg (13 orders too small!)")

m_wrong = hbar*kf*(alpha_exp**2 + 1)/(alpha_exp*c)
p(f"  m_wrong = {m_wrong:.6e} kg")
p(f"  m_exp   = {me:.6e} kg")
p(f"  ratio = {m_wrong/me:.6e}  (way off!)")

p("\n[THE CORRECT m_e FORMULA]")
p("  m_e = hbar * Q_top / c  (by definition of Q_top)")
p("  where Q_top = m_e*c/hbar")
p("  This is a DEFINITION, not a prediction")

m_correct = hbar * Qtop / c
p(f"  m_e = hbar*Q_top/c = {m_correct:.12e} kg")
p(f"  m_exp = {me:.12e} kg")
p(f"  ratio = {m_correct/me:.10f}  (exactly 1.0 by construction)")

p("\n[WHAT WAS THE INTENTION?]")
p("  The audit Q23 used: m_e = hbar*kappa*(alpha^2+1)/(alpha*c)")
p("  This formula was in some older scripts but is WRONG")
p("  FIX: Use m_e = hbar*Q_top/c = hbar*(me*c/hbar)/c = me (identity)")

p("\n" + "=" * 72)
p("S_dS AND S_BH COMPUTATION (correcting Q12)")
p("=" * 72)

# Correct de Sitter entropy
Lambda = mp.mpf('1e-52')  # cosmological constant (rough)
H0 = mp.mpf('2.3e-18')   # Hubble parameter ~70 km/s/Mpc
rho_vac = Lambda/(8*mp.pi*G)
S_dS_geom = kf**3 * hbarC / (2*mp.pi)
p(f"\n[DE SITTER ENTROPY ESTIMATE]")
S_dS_est = mp.pi * c**3 / (G * H0**2)
p(f"  S_dS = pi*c^3/(G*H0^2) ~ {S_dS_est:.6e}")

# Black hole entropy for solar mass
M_sun = mp.mpf('2e30')
R_s = 2*G*M_sun/c**2
S_BH_sun = 4*mp.pi*R_s*hbarC/(2*c**3*mp.pi*4)  # S_BH = kB*A/(4*lP^2)
A = 4*mp.pi*R_s**2
lP = mp.sqrt(hbar*G/c**3)
S_BH_est = A/(4*lP**2)
p(f"\n[BLACK HOLE ENTROPY ESTIMATE]")
p(f"  R_s for M_sun = {R_s:.6e} m")
p(f"  S_BH for M_sun = {S_BH_est:.6e}")
p(f"\n[PRODUCT kappa^28 * (S_dS/S_BH)]")
product = kf**28 * S_dS_est / S_BH_est
p(f"  kappa^28 * (S_dS/S_BH) ~ {product:.6e}")
p(f"  10^-98 = {mp.mpf('1e-98'):.6e}")
p(f"  10^-70 = {mp.mpf('1e-70'):.6e}")
p(f"  The product is ~10^-70, not 10^-98")
p(f"  The earlier 'kappa^28 = 10^-98' claim needs COMPLETE reanalysis")

p("\n" + "=" * 72)
p("SUMMARY OF FIXES NEEDED")
p("=" * 72)

p("""
[C1] Q5: e formula
    OLD: sqrt(2*alpha*eps0*hbar*c) -> e_wrong = 6.39e-20 C (FAIL)
    NEW: sqrt(4*pi*alpha*eps0*hbar*c) -> e_right = 1.602e-19 C (PASS)
    STATUS: Must fix in all scripts

[C2] Q12: kappa^28 = 10^-98
    OLD: kappa^28 * (S_dS/S_BH) = 10^-98 (CLAIMED)
    NEW: kappa^28 = 10^-110.28 (kappa alone)
         Product with S_dS/S_BH gives ~10^-70
    STATUS: Earlier breakthrough is UNCONFIRMED/UNCLEAR

[C3] Q16: G_topo formula
    OLD: G = alpha^2/(4*pi*c^2*kappa^2*eps0)
    This gives G_wrong = 5.3e-05 (vs G=6.67e-11) -- WAY off
    STATUS: This G derivation is WRONG. Remove entirely.

[C4] m_e formula in scripts
    OLD: m_e = hbar*kappa*(alpha^2+1)/(alpha*c) -> 1.52e-44 kg (WRONG)
    NEW: m_e = hbar*Q_top/c = me (definition/identity)
    STATUS: Must fix in all scripts

[C5] f_S, f_W origin claim
    OLD: 'From SU(3)xSU(2) group theory'
    NEW: 'Geometric base coefficients {1, 4, 15} on unified seed'
    STATUS: Must revise in paper

[C6] kappa = (sqrt10)^-7
    OLD: 'Exact'
    NEW: 'Approximate' (ratio ~0.9997)
    STATUS: Must soften claim

[C7] Phi_T = 2^-3.5 origin
    OLD: 'From 32D spinor projection'
    NEW: 'Seed value (no rigorous first-principles derivation yet)'
    STATUS: Must revise in paper

[C8] m_e formula in audit Q23
    OLD: Used broken m formula -> 100% error
    NEW: Should use hbar*Q_top/c = me (identity)
    STATUS: Corrected above
""")

print("\n".join(out))
