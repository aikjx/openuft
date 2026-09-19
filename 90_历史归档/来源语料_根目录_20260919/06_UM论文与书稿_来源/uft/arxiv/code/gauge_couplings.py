"""Gauge coupling analysis for Perpendicular Mode Geometry (E10 corrected)."""
import mpmath as mp
mp.mp.dps = 80

Phi_T_sq = mp.mpf(2)**(-7)  # = 1/128
alpha_S_geom = 15 * Phi_T_sq
alpha_W_geom = 4 * Phi_T_sq
alpha_EM_geom = 1 * Phi_T_sq

alpha_S_exp = mp.mpf("0.117900")
# E10: use INDEPENDENT alpha_2, NOT 0.03106 = 4*alpha_EM (circular)
alpha_2_exp = mp.mpf("0.033800")   # INDEPENDENT alpha_2(M_Z) = g_2^2/4pi
alpha_exp = mp.mpf("0.00729735")

print("Gauge Coupling Analysis (E10 corrected)")
print("=" * 50)
print(f"Framework: alpha_EM={alpha_EM_geom:.6f}, alpha_W={alpha_W_geom:.6f}, alpha_S={alpha_S_geom:.6f}")
print(f"Experiment: alpha_EM={alpha_exp:.6f}, alpha_2={alpha_2_exp:.6f}, alpha_S={alpha_S_exp:.6f}")
print()
print(f"Integer ratio: alpha_S : alpha_W : alpha_EM = 15 : 4 : 1")
ratio_g = alpha_S_geom/alpha_W_geom
ratio_e = alpha_S_exp/alpha_2_exp
print(f"alpha_S/alpha_W = {ratio_g:.4f} (framework) vs {ratio_e:.4f} (exp, INDEP)")
print(f"Deviation: {abs(ratio_g - ratio_e)/ratio_e*100:.2f}% (was falsely 1.2% via circular alpha_W)")
print()
print("NOTE (E10): alpha_S/alpha_W=3.75 is a WEAK prediction (assigned integers).")
print("Best match: alpha_S/alpha_EM=15 (0.6%, trivial). Other deviations involve H1.")
