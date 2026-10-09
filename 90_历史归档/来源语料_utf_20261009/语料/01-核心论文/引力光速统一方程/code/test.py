# 优化后的几何因子推导示例
import numpy as np

# 定义投影效率函数
def projection_efficiency(theta):
    """计算方向角theta对应的投影效率"""
    return np.abs(np.cos(theta))  # 在统一场论模型中，有效贡献与|cos(theta)|成正比（根据论文中的推导）

# 计算平均投影效率
def average_projection_efficiency():
    """通过数值积分计算平均投影效率"""
    # 使用数值积分计算所有方向的平均投影效率
    theta_values = np.linspace(0, np.pi, 1000)
    d_theta = np.pi / 999
    
    # 计算加权平均（权重为立体角元sin(theta)）
    numerator = np.sum(projection_efficiency(theta_values) * np.sin(theta_values) * d_theta)
    denominator = np.sum(np.sin(theta_values) * d_theta)
    
    return numerator / denominator

# 计算几何因子
avg_efficiency = average_projection_efficiency()
geometric_factor = 1 / avg_efficiency

print(f"平均投影效率: {avg_efficiency:.6f}")
print(f"几何因子: {geometric_factor:.6f}")
# 输出：
# 平均投影效率: 0.500000
# 几何因子: 2.000000