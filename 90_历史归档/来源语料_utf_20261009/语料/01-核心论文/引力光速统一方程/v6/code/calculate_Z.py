
import math

def calculate_Z():
    """
    计算空间光速螺旋本征阻抗常数 Z = Gc/2
    
    使用NIST/CODATA 2018推荐值:
    - c = 299792458 m/s (精确定义值)
    - G = 6.67430(15)×10^-11 m^3·kg^-1·s^-2
    """
    
    # NIST/CODATA 2018常数
    c = 299792458.0  # 真空中的光速 (m/s) - 精确定义值
    G = 6.67430e-11  # 牛顿引力常数 (m^3·kg^-1·s^-2)
    u_G = 1.5e-15    # G的标准不确定度
    
    # 计算Z
    Z = (G * c) / 2.0
    
    # 计算不确定度 (由于c是精确的，Z的不确定度完全来自G)
    u_Z = (c / 2.0) * u_G
    
    print("=" * 80)
    print("空间光速螺旋本征阻抗常数 Z = Gc/2 精算验证")
    print("=" * 80)
    print()
    
    print("输入常数:")
    print(f"  真空中的光速 c = {c} m/s (精确定义值)")
    print(f"  牛顿引力常数 G = {G:.10e} m^3·kg^-1·s^-2")
    print(f"  G的标准不确定度 u(G) = {u_G:.10e} m^3·kg^-1·s^-2")
    print()
    
    print("计算过程:")
    print(f"  Z = (G * c) / 2")
    print(f"    = ({G:.10e} * {c}) / 2")
    print(f"    = {G * c:.14e} / 2")
    print()
    
    print("计算结果:")
    print(f"  Z = {Z:.12e} m^4·kg^-1·s^-3")
    print(f"  Z = {Z:.12f} m^4·kg^-1·s^-3")
    print()
    
    print("不确定度分析:")
    print(f"  u(Z) = (c / 2) * u(G)")
    print(f"      = ({c} / 2) * {u_G:.10e}")
    print(f"      = {u_Z:.10e} m^4·kg^-1·s^-3")
    print(f"      = {u_Z:.10f} m^4·kg^-1·s^-3")
    print()
    
    print("最终结果:")
    print(f"  Z = {Z:.10f} +- {u_Z:.10f} m^4·kg^-1·s^-3")
    print()
    
    # 与论文结果对比
    paper_Z = 0.0100045240
    paper_u_Z = 0.0000002248
    
    print("与论文结果对比:")
    print(f"  论文结果: Z = {paper_Z} +- {paper_u_Z} m^4·kg^-1·s^-3")
    print(f"  计算结果: Z = {Z:.10f} +- {u_Z:.10f} m^4·kg^-1·s^-3")
    print(f"  Z值差异: {abs(Z - paper_Z):.16f}")
    print(f"  不确定度差异: {abs(u_Z - paper_u_Z):.16f}")
    print()
    
    # 验证量纲
    print("量纲验证:")
    print(f"  [G] = m^3·kg^-1·s^-2")
    print(f"  [c] = m·s^-1")
    print(f"  [Z] = [G]·[c] = (m^3·kg^-1·s^-2)·(m·s^-1) = m^4·kg^-1·s^-3")
    print("  [OK] 量纲一致")
    print()
    
    print("=" * 80)
    
    return Z, u_Z

def calculate_additional_quantities(Z):
    """
    计算额外相关物理量
    """
    c = 299792458.0
    G = 2 * Z / c  # 从Z反推G
    
    print("\n额外物理量计算:")
    print("-" * 80)
    print(f"  从Z反推G: G = 2Z/c = {G:.10e} m^3·kg^-1·s^-2")
    print(f"  与标准G的相对偏差: {(G - 6.67430e-11)/6.67430e-11 * 100:.10e}%")
    print()
    
    # 计算临界半径示例 (以太阳质量为例)
    M_sun = 1.989e30  # 太阳质量 (kg)
    r_c = math.sqrt((4 * math.pi * G * M_sun) / (c ** 2))  # 根据论文公式(95)
    R_s = (2 * G * M_sun) / (c ** 2)  # 史瓦西半径
    
    print(f"  以太阳质量(M = {M_sun:.3e} kg)为例:")
    print(f"    临界半径 r_c = {r_c:.6e} m")
    print(f"    史瓦西半径 R_s = {R_s:.6e} m")
    print(f"    比值 R_s/r_c = {R_s/r_c:.6f}")
    print("-" * 80)

if __name__ == "__main__":
    Z, u_Z = calculate_Z()
    calculate_additional_quantities(Z)

