import numpy as np

# 验证基本电荷的推导（式18）
def verify_electric_charge():
    # 定义常数
    hbar = 1.054571817e-34  # 普朗克常数
    c = 3.0e8  # 光速
    epsilon0 = 8.854187817e-12  # 真空介电常数
    e_experimental = 1.602176634e-19  # 实验测得的基本电荷
    
    # 根据式(18)计算基本电荷
    e_calculated = np.sqrt((np.pi * hbar * c) / epsilon0)
    
    # 计算误差
    error = abs(e_calculated - e_experimental)
    
    print("=== 基本电荷推导验证 ===")
    print(f"普朗克常数 hbar = {hbar}")
    print(f"光速 c = {c}")
    print(f"真空介电常数 epsilon0 = {epsilon0}")
    print(f"根据式(18)计算的基本电荷 e = {e_calculated}")
    print(f"实验测得的基本电荷 e = {e_experimental}")
    print(f"误差: {error}")
    print(f"验证结果: {'通过' if error < 1e-25 else '失败'}")
    print()

if __name__ == "__main__":
    verify_electric_charge()
