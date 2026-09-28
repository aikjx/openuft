import math

# CODATA 2018 values
c = 299792458  # m/s
epsilon_0 = 8.8541878128e-12  # F/m
hbar = 1.054571817e-34  # J·s

# Calculate Planck charge q_p
q_p = math.sqrt(4 * math.pi * epsilon_0 * hbar * c)
print(f"Planck charge q_p: {q_p:.6e} C")

# Calculate k'
k_prime = q_p / c
print(f"Constant k': {k_prime:.6e} C·s/kg")

# Verify with document's expected value
expected_k_prime = 6.25e-27
print(f"Expected k' from document: {expected_k_prime:.6e} C·s/kg")
print(f"Difference: {abs(k_prime - expected_k_prime):.6e} C·s/kg")
print(f"Relative difference: {abs((k_prime - expected_k_prime)/expected_k_prime)*100:.6f}%")

# Additional verification: Calculate using intermediate steps as in the document
hbar_c = hbar * c
print(f"\nIntermediate steps verification:")
print(f"ħc: {hbar_c:.6e} J·m")

four_pi_epsilon_0 = 4 * math.pi * epsilon_0
print(f"4πε₀: {four_pi_epsilon_0:.6e} F/m")

product = four_pi_epsilon_0 * hbar_c
print(f"(4πε₀)(ħc): {product:.6e} C²")

q_p_verify = math.sqrt(product)
print(f"q_p (verified): {q_p_verify:.6e} C")

k_prime_verify = q_p_verify / c
print(f"k' (verified): {k_prime_verify:.6e} C·s/kg")
