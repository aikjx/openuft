import math

# CODATA 2018 常数
c = 299792458  # 光速，单位：m/s
epsilon_0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
e = 1.602176634e-19  # 基本电荷，单位：C
hbar = 1.054571817e-34  # 约化普朗克常数，单位：J·s

# 计算 Z' = c/(8π ε₀)
def calculate_z_prime():
    z_prime = c / (8 * math.pi * epsilon_0)
    return z_prime

# 计算精细结构常数 α = 2e²Z'/(ħ c²)
def calculate_fine_structure():
    z_prime = calculate_z_prime()
    alpha = (2 * e**2 * z_prime) / (hbar * c**2)
    
    # CODATA 2018 推荐的 α 值
    alpha_codata = 0.0072973525693
    
    # 计算相对误差
    relative_error = abs((alpha - alpha_codata) / alpha_codata) * 100
    
    print(f"=== 精细结构常数 α 的验证 ===")
    print(f"计算得到的 α = {alpha:.12f}")
    print(f"CODATA 2018 推荐值 α = {alpha_codata:.12f}")
    print(f"相对误差 = {relative_error:.12f}%")
    print(f"误差量级 = {10**math.floor(math.log10(relative_error))}")
    
    if abs(alpha - alpha_codata) < 1e-9:
        print("验证通过：计算值与CODATA值高度吻合，误差在10^-9量级！")
        print(f"实际误差：{abs(alpha - alpha_codata):.15f}")
    else:
        print("验证失败：计算值与CODATA值存在显著差异。")
    
    return alpha

if __name__ == "__main__":
    calculate_fine_structure()
