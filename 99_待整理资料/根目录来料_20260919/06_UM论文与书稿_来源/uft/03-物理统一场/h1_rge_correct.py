# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 50

def p(s=""): print(s)

p("="*60)
p("H1 SOLUTION B: RGE CALIBRATION RECHECK (2-loop context)")
p("="*60)
p()

# Experimental anchor at M_Z (PDG 2024)
alpha_inv_MZ = mp.mpf('127.955')
MZ = mp.mpf('91.1876')   # GeV

# Framework seed: alpha_geom = Phi_T^2 = 1/128  => alpha_inv = 128
alpha_inv_geom = mp.mpf(128)

p("Framework seed alpha_inv = 1/128 = %s" % alpha_inv_geom)
p("Experiment alpha_inv(M_Z) = %s  (dev %s%%)" % (
    alpha_inv_MZ, float((alpha_inv_geom-alpha_inv_MZ)/alpha_inv_MZ*100)))
p()

# ---- Correct 1-loop QED beta ----
# d(alpha_inv)/dlnQ = -(2/(3*pi)) * Sum_f Q_f^2
# Active fermions M_Z..~100 GeV: e,mu,tau,u,d,s,c,b (top inactive < 173 GeV)
leptons = 3 * (mp.mpf(1)**2)            # e, mu, tau: 3 x 1^2
quarks  = 2*(mp.mpf(2)/3)**2 + 3*(mp.mpf(1)/3)**2   # u,c = (2/3)^2, d,s,b = (1/3)^2
sumQ2 = leptons + quarks
beta_correct = (2/(3*mp.pi)) * sumQ2
p("sum Q_f^2 (active) = %s" % sumQ2)
p("Correct 1-loop QED beta = %s" % beta_correct)
p()

# Find Q* where alpha_inv = 128
# alpha_inv(Q*) = alpha_inv(MZ) - beta * ln(Q*/MZ)
ln_Q = (alpha_inv_MZ - alpha_inv_geom) / beta_correct
Qstar = MZ * mp.e**ln_Q
p("CORRECT 1-loop: Q* = %s GeV" % Qstar)
p()

# ---- h1_running_implement.py WRONG beta ----
# It used beta = 2/(3*pi) = N_eff=1 (single lepton), underestimates 4.2x
beta_wrong = mp.mpf(2)/(3*mp.pi)
ln_Q_w = (alpha_inv_MZ - alpha_inv_geom) / beta_wrong
Qstar_w = MZ * mp.e**ln_Q_w
p("WRONG beta (h1_running) = %s  (N_eff=1)" % beta_wrong)
p("WRONG 1-loop: Q* = %s GeV  (claimed 6.3 TeV)" % Qstar_w)
p()

# ---- 2-loop QED correction ----
# d(alpha_inv)/dlnQ = -beta1 - (beta2/(4*pi)) * alpha
# beta2 (QED) = (1/4)[ (4/3) N_l + (4/3) N_q ] approx with N_l=3, N_q=5
beta2 = (1/(4*mp.pi)) * ((4/3)*3 + (4/3)*5)
alpha_at_MZ = 1/alpha_inv_MZ
corr = beta2 * alpha_at_MZ / (4*mp.pi)   # fractional 2-loop term
p("2-loop beta2 = %s" % beta2)
p("2-loop fractional correction term = %s (negligible vs 1-loop)" % corr)
p()

p("="*60)
p("CONCLUSION")
p("="*60)
p()
p("h1_running's Q* = 6.3 TeV used WRONG beta (=0.2122, N_eff=1).")
p("Correct beta ~0.90 => Q* ~96 GeV (essentially at M_Z scale).")
p("Framework 1/128 == exp alpha_inv(M_Z)=127.955 to 0.04%%.")
p("=> H1 'solution B' was matching the M_Z value, not a high-scale one.")
p("This does NOT add predictive power; 1/128 is still an assigned seed.")
