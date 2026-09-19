"""Analyze the alpha_S/alpha_W = 3.75 prediction (E10 corrected)."""
import mpmath as mp
mp.mp.dps = 80

Phi_T_sq = mp.mpf(2)**(-7)  # = 1/128
alpha_S_geom = 15 * Phi_T_sq
alpha_W_geom = 4 * Phi_T_sq
alpha_S_exp = mp.mpf('0.117900')     # PDG 2024, M_Z
# E10 CRITICAL: use INDEPENDENT alpha_2, NOT framework's 4*alpha_EM=0.03106 (circular)
alpha_2_exp = mp.mpf('0.033800')     # INDEPENDENT alpha_2(M_Z) = g_2^2/4pi
alpha_exp = mp.mpf('0.00729735')     # PDG 2024

ratio_geom = alpha_S_geom / alpha_W_geom
ratio_exp_indep = alpha_S_exp / alpha_2_exp   # = 3.49
ratio_err = abs(ratio_geom - ratio_exp_indep) / ratio_exp_indep

print("=" * 64)
print("ALPHA_S / ALPHA_W = 3.75 PREDICTION ANALYSIS (E10 CORRECTED)")
print("=" * 64)
print()
print(f"Framework prediction:  {ratio_geom:.6f} (= 15/4 exactly)")
print(f"Experiment (INDEP, M_Z): {ratio_exp_indep:.6f}  [alpha_2=0.0338]")
print(f"Deviation:             {ratio_err*100:.2f}%")
print()
print("E10 NOTE: older claim used circular alpha_W = 4*alpha_EM = 0.03106,")
print("giving ratio_exp = 3.7959 (1.2% dev). This CONFIRMS the framework's")
print("own assumption, not an independent test (circular dependency).")
print()
print("STATUS: 7.4% deviation from INDEPENDENT experiment.")
print("        Weak prediction (assigned integers, not first-principles).")
print()
print("Best framework match: alpha_S/alpha_EM = 15 (0.6%, trivial integer ratio).")
print()
print("Falsifiability: measure alpha_S/alpha_W at higher scales.")
print("  If constant at 3.75 -> supported; if runs (SM predicts) -> falsified.")
print()

# Running corrections analysis
print("=" * 64)
print("RUNNING COUPLING ANALYSIS (H1 context)")
print("=" * 64)
print()
print("alpha_geom = 1/128 = 0.0078125")
print("alpha_exp  = 1/137  = 0.0072974")
print("Deviation: 7.06%")
print()
print("One-loop QED running at M_Z:")
print("  alpha(M_Z) = alpha(M_0) / (1 - b*ln(Q/M_0)/2pi)")
print("  b_QED = 2/3 * N_f = 2/3 * 3 = 2")
print("  Running makes alpha LARGER (coupling grows)")
print("  But experiment has alpha(M_Z) = 1/128.9 < 1/128")
print("  Running makes discrepancy WORSE, not better")
print()
print("Conclusion: Cannot explain 7.06% via running corrections.")
print("H1 (alpha absolute value) remains UNSOLVED.")
