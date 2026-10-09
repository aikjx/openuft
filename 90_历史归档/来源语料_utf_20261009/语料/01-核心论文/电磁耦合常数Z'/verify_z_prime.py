import math

# CODATA 2018 常数
c = 299792458  # 光速，单位：m/s
epsilon_0 = 8.8541878128e-12  # 真空介电常数，单位：F/m

# 计算 Z' = c/(8π ε₀)
def calculate_z_prime():
    z_prime = c / (8 * math.pi * epsilon_0)
    print(f"Z' = c/(8π ε₀) = {z_prime:.6e} kg·m⁴·s⁻⁵·A⁻²")
    return z_prime

if __name__ == "__main__":
    calculate_z_prime()
