import numpy as np
import matplotlib.pyplot as plt

# ---------------------- 理论参数设定（符合统一场论定义） ----------------------
k = 1.0          # 质量公式比例常数（理论未给出具体值，设为1简化计算）
Omega = 4 * np.pi# 单位立体角（球面立体角）
n0 = 100.0       # 初始空间位移矢量条数密度（初始质量的决定因素）
a_plus = 10.0    # 正引力场加速度大小 (m/s²)
a_minus = 10.0   # 反引力场加速度大小 (m/s²)
k1 = 1.0         # 正引力场下n的变化率系数
k2 = 1.0         # 反引力场下n的变化率系数
t_range = np.linspace(0, 20, 100)  # 时间范围（0-20秒）

# ---------------------- 数值计算 ----------------------
# 1. 正引力场下：n随时间递增，计算质量m_plus
n_plus = n0 + k1 * a_plus * t_range
m_plus = (k / Omega) * n_plus

# 2. 反引力场下：n随时间递减至零，计算质量m_minus（n≤0时设为0，对应质量归零）
n_minus = n0 - k2 * a_minus * t_range
n_minus[n_minus < 0] = 0  # 线条密度不能为负，归零后保持为0
m_minus = (k / Omega) * n_minus

# 3. 计算反引力场下质量归零的时间点
zero_time = n0 / (k2 * a_minus) if k2 * a_minus != 0 else np.inf

# ---------------------- 可视化结果（符合“电影级”视觉需求的图表设计） ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12, 6), dpi=150)

# 子图1：n（线条密度）随时间变化
plt.subplot(1, 2, 1)
plt.plot(t_range, n_plus, 'r-', linewidth=2.5, label=f'正引力场（a₊={a_plus} m/s²）', alpha=0.8)
plt.plot(t_range, n_minus, 'b-', linewidth=2.5, label=f'反引力场（a₋={a_minus} m/s²）', alpha=0.8)
plt.axvline(x=zero_time, color='green', linestyle='--', linewidth=2, label=f'质量归零时间：t={zero_time:.1f}s')
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('单位立体角线条密度 n', fontsize=12)
plt.title('正反引力场对空间位移线条密度的影响', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# 子图2：质量m随时间变化
plt.subplot(1, 2, 2)
plt.plot(t_range, m_plus, 'r-', linewidth=2.5, label=f'正引力场（质量递增）', alpha=0.8)
plt.plot(t_range, m_minus, 'b-', linewidth=2.5, label=f'反引力场（质量递减至零）', alpha=0.8)
plt.axvline(x=zero_time, color='green', linestyle='--', linewidth=2, label=f'质量归零时间：t={zero_time:.1f}s')
plt.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5, label='质量归零线')
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('物体质量 m (相对单位)', fontsize=12)
plt.title('正反引力场对物体质量的影响', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('正反引力场质量影响模拟.png', dpi=300, bbox_inches='tight')
plt.show()

# ---------------------- 输出关键结论 ----------------------
print(f"初始质量：m0 = {k * n0 / Omega:.2f}（相对单位）")
print(f"正引力场下，t=20s时质量：m_plus = {m_plus[-1]:.2f}（相对单位）（递增）")
print(f"反引力场下，质量归零时间：t0 = {zero_time:.1f}s")
print(f"反引力场下，t≥t0时质量：m_minus = 0（相对单位）（符合光速飞行条件）")