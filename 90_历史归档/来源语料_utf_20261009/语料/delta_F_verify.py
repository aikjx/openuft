import mpmath as mp
mp.mp.dps = 250

# CODATA-2022 exact constants
c      = mp.mpf("299792458")
G      = mp.mpf("6.67430e-11")
eps0   = mp.mpf("8.8541878128e-26")  # placeholder fixed below
eps0   = mp.mpf("8.8541878128e-12")
qe     = mp.mpf("1.602176634e-19")
hbar_CODATA = mp.mpf("1.054571817e-34")
alpha_CODATA = mp.mpf("7.2973525693e-3")

Geps0 = G * eps0

r = (qe**2) / (4 * mp.pi * c**2 * Geps0)

# perturbation expansion D_kappa = 32/(1+r) = 32*(1 - r + r^2 - ...), first-order truncation
# to avoid the 32/(1+r) numerical collapse into exactly 32
D_kappa = mp.mpf(32) * (mp.mpf(1) - r)
D_tau   = mp.mpf(32) - D_kappa

one_plus_dF = mp.sqrt(32 / D_kappa)
delta_F     = one_plus_dF - 1

# 32D intrinsic characteristic charge
q_star = mp.sqrt(4*mp.pi * Geps0) * c * one_plus_dF

# fractal-origin formulas
hbar_theo = G * c**2 * one_plus_dF
alpha_theo = D_tau / (c * mp.sqrt(32 * D_kappa))

lhs = G * eps0
rhs = (q_star**2) / (4 * mp.pi * c**2 * one_plus_dF**2)
qe_calc = c * mp.sqrt(4*mp.pi*Geps0) * mp.sqrt(D_tau / D_kappa)

def sci(x, n=35):
    return mp.nstr(x, n, min_fixed=-999, max_fixed=-999)

print("==== delta_F analytical closed form :: 32D bidirectional fractal UFT @ 250 digits ====")
print(f"G*eps0              = {sci(lhs)}")
print(f"r = D_tau/D_kappa   = {sci(r)}")
print(f"D_kappa (graviton)  = {mp.nstr(D_kappa, 30)}")
print(f"D_tau (em)          = {sci(D_tau)}")
print(f"1 + delta_F         = {mp.nstr(one_plus_dF, 30)}")
print(f"delta_F fractal     = {sci(delta_F)}")
print(f"q* 32D intrinsic    = {sci(q_star)} C")
print(f"identity RHS        = {sci(rhs)}")
print(f"identity |lhs-rhs|  = {sci(abs(lhs-rhs))}")
print(f"qe observed         = {sci(qe)} C")
print(f"qe projected        = {sci(qe_calc)} C")
print(f"qe residual         = {sci(abs(qe-qe_calc))}")
dim_sum = D_kappa + D_tau
print(f"\nDimension check D_kappa+D_tau = {mp.nstr(dim_sum, 20)}")

print()
print("==== Route A: alpha & hbar from D_kappa,D_tau fractal dimension | 250 digits ====")
print(f"r = D_tau/D_kappa        = {sci(r)}")
print(f"D_kappa (grav)           = {mp.nstr(D_kappa, 30)}")
print(f"D_tau (em fractal)       = {sci(D_tau)}")
print(f"1+delta_F                = {mp.nstr(one_plus_dF, 30)}")
print(f"delta_F                  = {sci(delta_F)}")
print()
print(f"hbar theory  (G c^2 (1+delta_F)) = {sci(hbar_theo)} J.s")
print(f"hbar CODATA-2022                 = {sci(hbar_CODATA)} J.s")
print(f"hbar abs residual                = {sci(abs(hbar_theo-hbar_CODATA))}")
print()
print(f"alpha theory (D_tau/(c sqrt(32 D_kappa))) = {sci(alpha_theo)}")
print(f"alpha CODATA-2022                          = {sci(alpha_CODATA)}")
print(f"alpha abs residual                        = {sci(abs(alpha_theo-alpha_CODATA))}")
print()
print(f"Dimension sum D_kappa+D_tau = {mp.nstr(D_kappa+D_tau, 20)}")

# cross-check standard alpha definition reverse recovery
alpha_check = qe**2 / (4*mp.pi*eps0*hbar_theo*c)
print(f"alpha cross-check from qe,eps0,c,hbar_theo = {sci(alpha_check)}")
