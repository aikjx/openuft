import math
from scipy.constants import hbar, e, c, epsilon_0, alpha

def calculate_Z_prime(version='corrected'):
    """
    计算张祥前统一场论中的Z'常数。
    参数:
        version: 'proposed'（文档提议的Z'=hbar/(2e^2)）或 'corrected'（修正的Z'=c/(8*pi*epsilon_0)）
    返回:
        数值和单位字符串。
    """
    if version == 'proposed':
        # 文档中提议的公式: Z' = hbar / (2 * e^2)
        Z_prime_value = hbar / (2 * e**2)
        units = "kg·m²·s⁻¹·C⁻²"
    elif version == 'corrected':
        # 修正公式: Z' = c / (8 * pi * epsilon_0)
        Z_prime_value = c / (8 * math.pi * epsilon_0)
        units = "kg·m⁴·s⁻³·C⁻²"
    else:
        raise ValueError("版本选择无效，请使用 'proposed' 或 'corrected'")
    
    return Z_prime_value, units

# 示例使用
if __name__ == "__main__":
    Z_proposed, units_proposed = calculate_Z_prime('proposed')
    Z_corrected, units_corrected = calculate_Z_prime('corrected')
    
    print(f"文档提议的Z'值: {Z_proposed:.2e} {units_proposed}")
    print(f"修正后的Z'值: {Z_corrected:.2e} {units_corrected}")
