import numpy as np
import matplotlib.pyplot as plt
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def zuft_evolve_formula_verification(R0=1.0, omega0=0.6, alpha=0.1, c=1.0, test_times=[0, 1, 2]):
    """验证新推导的ZUFT空间螺旋演化公式（合速度恒为光速c）"""
    print(f"=== ZUFT空间螺旋演化公式验证 ===")
    print(f"参数：R0={R0}, ω0={omega0}, α={alpha}, c={c}")
    
    # 遍历测试时间点
    for t in test_times:
        # 1. 计算演化后的角速度
        omega_t = omega0 * np.exp(alpha * t)
        # 验证约束：R0*omega_t ≤ c
        if R0 * omega_t > c:
            print(f"t={t}: 违反约束 R0*ω(t)={R0*omega_t:.4f} > c={c}，跳过")
            continue
        
        # 2. 计算速度分量（新公式2）
        vx = -R0 * omega0 * alpha * np.exp(alpha * t) * np.sin(omega0 * np.exp(alpha * t))
        vy = R0 * omega0 * alpha * np.exp(alpha * t) * np.cos(omega0 * np.exp(alpha * t))
        vz = np.sqrt(c**2 - (R0 * omega0 * np.exp(alpha * t))**2)
        
        # 3. 计算合速度
        v_total = np.sqrt(vx**2 + vy**2 + vz**2)
        
        # 输出结果
        print(f"t={t}:")
        print(f"  角速度ω(t)={omega_t:.4f}, 横向速度v⊥={R0*omega_t:.4f}")
        print(f"  速度分量：vx={vx:.4f}, vy={vy:.4f}, vz={vz:.4f}")
        print(f"  合速度={v_total:.4f} (预期c={c})")
        print("-"*50)

# 执行验证（α=0.1，角速度缓慢膨胀）
zuft_evolve_formula_verification(R0=1.0, omega0=0.6, alpha=0.1, c=1.0, test_times=[0, 1, 2])