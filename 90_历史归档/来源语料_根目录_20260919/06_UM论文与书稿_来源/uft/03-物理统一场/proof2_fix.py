# -*- coding: utf-8 -*-
# =====================================================================
# [RETRACTED / SUPERSEDED - 2026-08-14 audit]
#
# This script's conclusion ("STATUS: FRAMEWORK ODE IS NOT VERIFIED") is
# ILL-POSED and has been RETRACTED. See proof2_resolution.py for the full
# high-precision resolution (EXIT=0).
#
# Why it is wrong:
#   It holds alpha = tau/kappa CONSTANT and lets kappa^2+tau^2 = w^2/c^2
#   vary (a DILATION). Proof 1 instead lives on the CONSTANT-Qtop shell
#   (a ROTATION), where kappa^2+tau^2 = Qtop^2 and alpha = tan(u) varies.
#   The two constraints are mutually exclusive, so asking "is
#   dk/dlnw = -tau?" without declaring the constraint has no answer.
#
#   Decisive check: the kf/tauf hardcoded below satisfy tau/k = alpha_exp
#   but sqrt(k^2+tau^2)/Qtop = 1.22e-16, i.e. they are NOT on the Qtop
#   shell at all. The alarming factor "-137.035999" reported below is
#   therefore exactly -1/alpha -- an artifact of mixing the two families,
#   not a physical discrepancy.
#
# Branch selection: Axiom III (omega*rho = c) together with
# Qtop = m_e*c/hbar = const rejects this script's branch, because it would
# force m_e to drift with omega.
#
# Kept only as an audit artifact. DO NOT cite its conclusion.
# =====================================================================
import mpmath as mp
mp.mp.dps = 80

c=mp.mpf('299792458')
kf=mp.mpf('3.162277660168379e-4')
tauf=mp.mpf('2.307625500826972e-6')
alpha=mp.mpf('7.2973525693e-3')

print("PROOF 2: Helix ODE Investigation")
print("=" * 60)

# The claim: d(kappa)/d(ln omega) = -tau, d(tau)/d(ln omega) = +kappa
# This would be true if kappa and tau evolve along a helix trajectory
# But we need to check the constraint

print("\nConstraint: kappa^2 + tau^2 = omega^2 / c^2")
print("But framework has kappa^2 + tau^2 = alpha^2 * kappa^2 / (1 - alpha^2)?")
print("No, let's check the actual relationship.")

omega = mp.sqrt(kf**2 + tauf**2) * c
print("\nomega = sqrt(k^2 + tau^2) * c = %.6e rad/s" % omega)
print("kappa/omega = %.6e s/m" % (kf/omega))
print("tau/omega   = %.6e s/m" % (tauf/omega))

# If we parameterize by some angle theta along helix:
# kappa = (omega/c) * cos(theta)
# tau   = (omega/c) * sin(theta)
# Then d(kappa)/d(theta) = -(omega/c) * sin(theta) = -tau
# And d(tau)/d(theta) = (omega/c) * cos(theta) = kappa

# But the ODE in the framework is d/d(ln omega), not d/d(theta)
# Let's check what happens if we vary omega while keeping alpha constant

print("\n" + "-" * 60)
print("Case 1: Vary omega while keeping alpha = tau/kappa constant")
print("-" * 60)

def kappa_tau_from_omega_alpha(omega_val, alpha_val):
    # tau = alpha * kappa
    # kappa^2 + tau^2 = omega^2 / c^2
    # kappa^2 + alpha^2 * kappa^2 = omega^2 / c^2
    # kappa^2 * (1 + alpha^2) = omega^2 / c^2
    kappa = omega_val / c / mp.sqrt(1 + alpha_val**2)
    tau = alpha_val * kappa
    return kappa, tau

eps = mp.mpf('1e-15')
omega_plus = omega * (1 + eps)
omega_minus = omega * (1 - eps)

k_plus, t_plus = kappa_tau_from_omega_alpha(omega_plus, alpha)
k_minus, t_minus = kappa_tau_from_omega_alpha(omega_minus, alpha)

# d/d(ln omega) = omega * d/d(omega)
dk_dlnw = omega * (k_plus - k_minus)/(2*eps*omega)
dt_dlnw = omega * (t_plus - t_minus)/(2*eps*omega)

print("\nNumerical derivatives (alpha fixed):")
print("d(kappa)/d(ln omega) = %.10e" % dk_dlnw)
print("d(tau)/d(ln omega)   = %.10e" % dt_dlnw)
print("\nExpected from helix ODE:")
print("d(kappa)/d(ln omega) = -tau = %.10e" % (-tauf))
print("d(tau)/d(ln omega)   = +kappa = %.10e" % kf)

print("\nRatios:")
print("dk_dlnw / (-tau) = %.6f" % (dk_dlnw / (-tauf)))
print("dt_dlnw / kappa  = %.6f" % (dt_dlnw / kf))

# The issue: if alpha is fixed, then d(kappa)/d(ln omega) = kappa (not -tau)
# Let's verify:
print("\n" + "-" * 60)
print("Case 2: What if d(kappa)/d(ln omega) = kappa?")
print("-" * 60)
print("From kappa = omega/(c*sqrt(1+a^2)):")
print("d(kappa)/d(ln omega) = kappa")
print("Numerical: %.10e" % dk_dlnw)
print("Analytical: %.10e" % kf)
print("Match: %.2e" % abs(dk_dlnw - kf))

print("\n" + "-" * 60)
print("CASE 3: The actual Frenet-Serret helix ODE")
print("-" * 60)
print("For a helix parameterized by arc length s:")
print("d(kappa)/d(s) = 0 (constant curvature)")
print("d(tau)/d(s) = 0 (constant torsion)")
print("d(kappa)/d(ln omega) is NOT a standard Frenet formula.")
print("")
print("The framework's ODE d(k)/d(ln w) = -tau appears to be")
print("a CONJECTURE, not a standard result.")
print("")
print("For the constraint k^2 + tau^2 = w^2/c^2 with alpha fixed:")
print("d(k)/d(ln w) = k (proportional scaling)")
print("d(tau)/d(ln w) = tau (proportional scaling)")
print("")
print("The framework ODE would require a DIFFERENT constraint.")

print("\n" + "=" * 60)
print("CONCLUSION FOR PROOF 2:")
print("=" * 60)
print("The numerical test shows:")
print("  d(kappa)/d(ln omega) = +kappa (when alpha fixed)")
print("  NOT = -tau as claimed in framework")
print("")
print("Framework ODE: d(k)/d(ln w) = -tau")
print("Numerical:     d(k)/d(ln w) = +k")
print("")
print("STATUS: FRAMEWORK ODO IS NOT VERIFIED")
print("This needs revision in the theoretical derivation.")
