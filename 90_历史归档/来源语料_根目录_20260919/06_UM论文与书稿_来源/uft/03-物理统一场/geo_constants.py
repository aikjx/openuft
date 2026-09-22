import mpmath as mp
mp.mp.dps = 80

hbar=mp.mpf('1.054571817e-34'); c=mp.mpf('299792458'); G=mp.mpf('6.67430e-11')
me=mp.mpf('9.1093837015e-31'); e=mp.mpf('1.602176634e-19')
eps0=mp.mpf('8.8541878128e-12'); mu0=mp.mpf('1.25663706212e-6')
alpha=mp.mpf('7.2973525693e-3')
H0=mp.mpf('67.4')*1000/mp.mpf('3.085677581e22')
kf=mp.mpf('3.162277660168379e-4'); tauf=mp.mpf('2.307625500826972e-6')
Qtop=me*c/hbar; lp=mp.sqrt(hbar*G/c**3)
# K = hbar/c * 1/lP_from_kappa  BUT correct: K is not defined from kappa
# hbar = K * c * (1/kappa_something) - let's find the correct K
# From framework: K = 3.5176728e-43 [L M T^-1]
# K^2 = hbar*G/c^3  (Planck constant geometric form)
K_val = mp.sqrt(hbar*G/c**3)
Phi_T=mp.mpf(2)**(-3.5); mP=mp.sqrt(hbar*c/(8*mp.pi*G))

out = []
def p(s):
    out.append(s)

p("=" * 72)
p("FULL GEOMETRICIZATION - ALL CONSTANTS")
p("=" * 72)
p("K = sqrt(hbar*G/c^3) [L M T^-1]")
p("K = %.6e" % K_val)

# -- mu0 --
p("\n[1] mu_0 = 4*pi*kappa^2")
mu0_g = 4*mp.pi*kf**2
p("mu0_geom = %.10e" % mu0_g)
p("mu0_exp  = %.10e" % mu0)
p("ratio    = %.12f" % (mu0_g/mu0))

# -- eps0 --
p("\n[2] eps_0 = tau^2/(4*pi*hbar*c)")
eps0_g = tauf**2/(4*mp.pi*hbar*c)
p("eps0_geom = %.10e" % eps0_g)
p("eps0_exp  = %.10e" % eps0)
p("ratio     = %.12f" % (eps0_g/eps0))

# -- Z0 --
p("\n[3] Z_0 = 4*pi*kappa^2*c^2")
Z0_g = 4*mp.pi*kf**2*c**2
Z0_exp = mu0*c
p("Z0_geom = %.10f" % Z0_g)
p("Z0_exp  = %.10f" % Z0_exp)
p("ratio   = %.12e" % (Z0_g/Z0_exp))

# -- alpha --
p("\n[4] alpha = tau/kappa")
p("tau/kappa = %.12f" % (tauf/kf))
p("alpha_exp = %.12f" % alpha)
p("rel_err   = %.12e" % ((tauf/kf - alpha)/alpha))

# -- e --
p("\n[5] e = sqrt(4*pi*K^2*tau*c^2)")
e_g = mp.sqrt(4*mp.pi*K_val**2*tauf*c**2)
p("e_geom  = %.10e" % e_g)
p("e_exp   = %.10e" % e)
p("ratio   = %.10f" % (e_g/e))

# -- hbar --
p("\n[6] hbar = K*c/sqrt(kappa*tau)")
hbar_g = K_val*c/mp.sqrt(kf*tauf)
p("hbar_geom = %.10e" % hbar_g)
p("hbar_exp  = %.10e" % hbar)
p("ratio     = %.10f" % (hbar_g/hbar))

# -- me --
p("\n[7] m_e = K*tau*c")
me_g = K_val*tauf*c
p("me_geom  = %.10e" % me_g)
p("me_exp   = %.10e" % me)
p("ratio    = %.10f" % (me_g/me))
me_alt = hbar*Qtop/c
p("me=hbar*Qtop/c = %.10e  ratio=%.10f" % (me_alt, me_alt/me))

# -- mP --
p("\n[8] m_Planck = c^2*sqrt(G*hbar/c^3)/G = c^2*K/G")
mP_g = c**2*K_val/G
p("mP_geom = %.10e" % mP_g)
p("mP_exp  = %.10e" % mP)
p("ratio   = %.10f" % (mP_g/mP))

# -- G candidates --
p("\n[9] G candidates")
p("G_exp  = %.10e" % G)
G1 = c**3*K_val/Qtop**2
G2 = c*K_val/kf**2
G3 = c*K_val**2/(Qtop*tauf)
G4 = c**5*K_val**2/(Qtop**4)
p("G1=c^3*K/Qtop^2    = %.10e  ratio=%.8f" % (G1, G1/G))
p("G2=c*K/kappa^2     = %.10e  ratio=%.8f" % (G2, G2/G))
p("G3=c*K^2/(Qtop*tau)= %.10e  ratio=%.8f" % (G3, G3/G))
p("G4=c^5*K^2/Qtop^4  = %.10e  ratio=%.8f" % (G4, G4/G))

# -- alpha_w, alpha_s --
p("\n[10] Weak/strong couplings")
p("Phi_T = 2^-3.5 = %.10f" % Phi_T)
p("alpha_w = Phi_T^2*4 = %.10f" % (Phi_T**2*4))
p("alpha_s = Phi_T^2*15 = %.10f" % (Phi_T**2*15))
aw_e = mp.mpf('0.03106'); as_e = mp.mpf('0.1179')
p("alpha_w_exp = %.5f   err = %.6e" % (aw_e, (Phi_T**2*4-aw_e)/aw_e))
p("alpha_s_exp = %.5f   err = %.6e" % (as_e, (Phi_T**2*15-as_e)/as_e))
p("alpha_s/alpha_w = %.4f (geom 15/4)  %.4f (exp)" % (15/4.0, as_e/aw_e))

# -- K check --
p("\n[11] K consistency")
p("K = sqrt(hbar*G/c^3) = %.6e" % K_val)
p("K_check = hbar*kappa/c = %.6e" % (hbar*kf/c))
p("ratio = %.8f" % (K_val*c/(hbar*kf)))

# -- summary --
p("\n[SUMMARY]")
p("Const   Geom_Form                   Geom_Value      Exp_Value       Ratio")
p("-" * 80)
p("mu_0    4*pi*k^2                   %.6e   %.6e   %.8f" % (mu0_g, mu0, mu0_g/mu0))
p("eps_0   tau^2/(4*pi*hc)            %.6e   %.6e   %.8f" % (eps0_g, eps0, eps0_g/eps0))
p("Z_0     4*pi*k^2*c^2               %.6e   %.6e   %.12f" % (Z0_g, mu0*c, Z0_g/(mu0*c)))
p("alpha   tau/kappa                  %.6e   %.6e   %.12e" % (tauf/kf, alpha, (tauf/kf-alpha)/alpha))
p("e       sqrt(4pi*K^2*tau*c^2)      %.6e   %.6e   %.8f" % (e_g, e, e_g/e))
p("hbar    K*c/sqrt(k*tau)            %.6e   %.6e   %.8f" % (hbar_g, hbar, hbar_g/hbar))
p("m_e     K*tau*c                    %.6e   %.6e   %.8f" % (me_g, me, me_g/me))
p("m_P     c^2*K/G                    %.6e   %.6e   %.8f" % (mP_g, mP, mP_g/mP))

p("\n[SCORE]")
p("PURE KAPPA:     mu_0, Z_0")
p("PURE TAU:       eps_0")
p("RATIO:          alpha")
p("K + TAU:        e, m_e")
p("K + sqrt(k*tau): hbar")
p("NEEDS G:        m_P")
p("NOT TOPO:       G")

print("\n".join(out))
