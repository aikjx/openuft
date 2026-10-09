import math

# CODATA 2018 constants
c = 299792458  # Speed of light in vacuum, m/s
epsilon0 = 8.8541878128e-12  # Vacuum permittivity, F/m
e = 1.602176634e-19  # Elementary charge, C
hbar = 1.054571817e-34  # Reduced Planck constant, J·s
G = 6.67430e-11  # Gravitational constant, m^3/(kg·s^2)
m_p = 1.67262192369e-27  # Proton mass, kg
m_e = 9.1093837015e-31  # Electron mass, kg

# Task 1: Verify Z' calculation
print("\n=== Task 1: Verify Z' calculation ===")
print(f"c = {c} m/s")
print(f"epsilon0 = {epsilon0} F/m")
print(f"8π = {8 * math.pi}")

# Calculate denominator: 8π*epsilon0
denominator = 8 * math.pi * epsilon0
print(f"Denominator (8π*epsilon0) = {denominator}")

# Calculate Z'
Z_prime = c / denominator
print(f"Z' = c/(8π*epsilon0) = {Z_prime:.11e} kg·m^4·s^-5·A^-2")

# Compare with paper result
paper_Z_prime = 1.34695441555e18
print(f"Paper Z' = {paper_Z_prime:.11e} kg·m^4·s^-5·A^-2")
print(f"Difference = {abs(Z_prime - paper_Z_prime):.11e}")
print(f"Relative difference = {abs(Z_prime - paper_Z_prime)/paper_Z_prime:.2e}")

# Task 2: Verify alpha calculation
print("\n=== Task 2: Verify alpha calculation ===")
print(f"e = {e} C")
print(f"hbar = {hbar} J·s")
print(f"c^2 = {c**2:.11e} m²/s²")

# Calculate numerator: 2*e²*Z'
numerator = 2 * e**2 * Z_prime
print(f"Numerator (2*e²*Z') = {numerator:.11e}")

# Calculate denominator: hbar*c²
denominator_alpha = hbar * c**2
print(f"Denominator (hbar*c²) = {denominator_alpha:.11e}")

# Calculate alpha
alpha_calc = numerator / denominator_alpha
print(f"alpha_calc = {alpha_calc:.11e}")

# Compare with CODATA 2018 value
codata_alpha = 0.0072973525693
print(f"CODATA 2018 alpha = {codata_alpha:.11e}")
print(f"Difference = {abs(alpha_calc - codata_alpha):.11e}")
print(f"Relative difference = {abs(alpha_calc - codata_alpha)/codata_alpha:.2e}")

# Task 3: Verify Z'/Z calculation
print("\n=== Task 3: Verify Z'/Z calculation ===")
print(f"G = {G} m³/(kg·s²)")

# Calculate Z = G*c/2
Z = G * c / 2
print(f"Z = G*c/2 = {Z:.11e} m^4/(kg·s^3)")

# Calculate Z'/Z
Z_ratio = Z_prime / Z
print(f"Z'/Z = {Z_ratio:.11e}")

# Compare with paper result
paper_Z_ratio = 1.346e20
print(f"Paper Z'/Z ~ {paper_Z_ratio:.1e}")
print(f"Difference = {abs(Z_ratio - paper_Z_ratio):.11e}")
print(f"Relative difference = {abs(Z_ratio - paper_Z_ratio)/paper_Z_ratio:.2e}")

# Task 4: Verify force strength ratios for different particle combinations
print("\n=== Task 4: Verify force strength ratios ===")
print(f"Proton mass (m_p) = {m_p} kg")
print(f"Electron mass (m_e) = {m_e} kg")

# Calculate charge-to-mass ratios
q_over_m_p = e / m_p
q_over_m_e = e / m_e
print(f"Proton charge-to-mass ratio (e/m_p) = {q_over_m_p:.11e} C/kg")
print(f"Electron charge-to-mass ratio (e/m_e) = {q_over_m_e:.11e} C/kg")

# 1. Proton-proton system
print("\n1. Proton-proton system:")
q_ratio_pp = (q_over_m_p) ** 2
force_ratio_pp = Z_ratio * q_ratio_pp
print(f"(q_p/m_p)^2 = {q_ratio_pp:.11e} C²/kg²")
print(f"Force ratio (F_e/F_g) = {force_ratio_pp:.11e} ~ 10^{math.log10(force_ratio_pp):.0f}")

# 2. Proton-electron system
print("\n2. Proton-electron system:")
q_ratio_pe = q_over_m_p * q_over_m_e
force_ratio_pe = Z_ratio * q_ratio_pe
print(f"(q_p/m_p)*(q_e/m_e) = {q_ratio_pe:.11e} C²/kg²")
print(f"Force ratio (F_e/F_g) = {force_ratio_pe:.11e} ~ 10^{math.log10(force_ratio_pe):.0f}")

# 3. Electron-electron system
print("\n3. Electron-electron system:")
q_ratio_ee = (q_over_m_e) ** 2
force_ratio_ee = Z_ratio * q_ratio_ee
print(f"(q_e/m_e)^2 = {q_ratio_ee:.11e} C²/kg²")
print(f"Force ratio (F_e/F_g) = {force_ratio_ee:.11e} ~ 10^{math.log10(force_ratio_ee):.0f}")

print("\n=== Verification Complete ===")
