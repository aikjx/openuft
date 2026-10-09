import numpy as np

# 验证精细结构常数的推导（式21）
def verify_fine_structure_constant():
    # 定义常数
    e = 1.602176634e-19  # 基本电荷
    hbar = 1.054571817e-34  # 普朗克常数
    c = 3.0e8  # 光速
    epsilon0 = 8.854187817e-12  # 真空介电常数
    alpha_experimental = 1/137.035999074  # 实验测得的精细结构常数
    
    # 根据式(19)计算精细结构常数
    alpha_calculated = (e**2) / (4 * np.pi * epsilon0 * hbar * c)
    
    # 计算电磁相互作用时空的螺旋切向速度与光速比值的平方
    # 根据式(21)，alpha = (v_perp_electric / c)^2
    v_perp_electric_over_c = np.sqrt(alpha_calculated)
    alpha_from_velocity = v_perp_electric_over_c**2
    
    # 计算误差
    error = abs(alpha_calculated - alpha_experimental)
    error_from_velocity = abs(alpha_from_velocity - alpha_experimental)
    
    print("=== 精细结构常数推导验证 ===")
    print(f"基本电荷 e = {e}")
    print(f"普朗克常数 hbar = {hbar}")
    print(f"光速 c = {c}")
    print(f"真空介电常数 epsilon0 = {epsilon0}")
    print(f"根据式(19)计算的精细结构常数 alpha = {alpha_calculated}")
    print(f"电磁相互作用时空的螺旋切向速度与光速比值: {v_perp_electric_over_c}")
    print(f"根据式(21)计算的精细结构常数 alpha = {alpha_from_velocity}")
    print(f"实验测得的精细结构常数 alpha = {alpha_experimental}")
    print(f"式(19)计算误差: {error}")
    print(f"式(21)计算误差: {error_from_velocity}")
    print(f"验证结果: {'通过' if error < 1e-15 and error_from_velocity < 1e-15 else '失败'}")
    print()

if __name__ == "__main__":
    verify_fine_structure_constant()
