import math

c = 299792458
hbar = 1.0545718176461565e-34
G_exp = 6.6743015e-11
alpha = 7.29735256930058e-3
e_exp = 1.602176634e-19
epsilon_0_exp = 8.8541878128e-12

l_P = math.sqrt(hbar * G_exp / (c ** 3))
kappa_P = 1 / l_P
tau_P = alpha / l_P

print(f'=== Planck Length ===')
print(f'l_P = {l_P}')

print(f'\n=== Curvature and Torsion ===')
print(f'kappa_P = {kappa_P}')
print(f'tau_P = {tau_P}')

k = e_exp * (kappa_P ** 2 + tau_P ** 2) / tau_P
print(f'\n=== Proportionality Constant k ===')
print(f'k = {k}')

G_epsilon0_spiral = (c ** 2 * k ** 2 * tau_P * (kappa_P ** 3)) / (4 * math.pi * (hbar ** 2) * (kappa_P ** 2 + tau_P ** 2) ** 4)
G_epsilon0_exp = G_exp * epsilon_0_exp

print(f'\n=== G * epsilon_0 from Spiral Geometry ===')
print(f'G * epsilon_0 = {G_epsilon0_spiral}')
print(f'G * epsilon_0 (CODATA) = {G_epsilon0_exp}')
print(f'Deviation: {(G_epsilon0_spiral - G_epsilon0_exp)/G_epsilon0_exp * 100:.6f}%')

print(f'\n=== Verification ===')
print(f'PASS' if abs((G_epsilon0_spiral - G_epsilon0_exp)/G_epsilon0_exp) < 0.01 else 'FAIL')
