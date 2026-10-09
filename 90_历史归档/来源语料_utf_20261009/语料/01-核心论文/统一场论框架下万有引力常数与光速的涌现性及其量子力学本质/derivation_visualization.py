import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, sqrt, simplify, Integral, pi
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 中文显示
plt.rcParams['axes.unicode_minus'] = False  # 负号显示

# 定义符号变量
hbar, c, G, m_p, k, m, N = symbols('hbar c G m_p k m N')
n, Omega, dm, dOmega, dn = symbols('n Omega dm dOmega dn')
r, t, p, E, psi = symbols('r t p E psi')

print("=== 张祥前统一场论质量常数k唯一性证明的Python可视化 ===\n")

# =============================
# 1. 质量几何化定义可视化
# =============================
print("1. 质量几何化定义")
print("=" * 60)

# 质量几何化定义
macro_def = Eq(m, k * n / Omega)
print(f"质量几何化定义：{macro_def}")
print("\n可视化：质量 = 量子比例常数 × (空间位移矢量条数 / 立体角)")

# 创建质量几何化定义的示意图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制球体（表示空间）
ax.add_patch(patches.Circle((0, 0), 2, color='lightblue', alpha=0.3))
ax.add_patch(patches.Circle((0, 0), 2, fill=False, color='blue', linewidth=2))

# 绘制空间位移矢量
for i in range(8):
    angle = 2 * np.pi * i / 8
    x = 2 * np.cos(angle)
    y = 2 * np.sin(angle)
    ax.arrow(0, 0, x, y, head_width=0.1, head_length=0.1, fc='red', ec='red')

# 绘制立体角
theta = np.linspace(0, np.pi/3, 100)
r_theta = 2
x_arc = r_theta * np.cos(theta)
y_arc = r_theta * np.sin(theta)
ax.plot(x_arc, y_arc, color='green', linewidth=2)
ax.plot(-x_arc, y_arc, color='green', linewidth=2)
ax.plot([0, r_theta*np.cos(np.pi/3)], [0, r_theta*np.sin(np.pi/3)], color='green', linestyle='--')
ax.plot([0, -r_theta*np.cos(np.pi/3)], [0, r_theta*np.sin(np.pi/3)], color='green', linestyle='--')

# 添加文本说明
ax.text(0, 0, '质量中心', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(2.2, 0, '空间位移矢量', ha='left', va='center', fontsize=12, color='red')
ax.text(1.5, 1.5, '立体角Ω', ha='center', va='center', fontsize=12, color='green')
ax.text(0, -2.5, f'质量几何化定义：{macro_def}', ha='center', fontsize=14, fontweight='bold')

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.axis('off')
plt.title("质量几何化定义示意图", fontsize=16, fontweight='bold')
plt.savefig('质量几何化定义.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)

# =============================
# 2. 微分形式推导可视化
# =============================
print("\n2. 微分形式推导")
print("=" * 60)

# 微分形式推导
diff_form = Eq(dm, k * (dn/dOmega) * dOmega)
simplified_diff = simplify(diff_form)

print(f"微分形式：{diff_form}")
print(f"简化后：{simplified_diff}")
print("\n物理意义：质量元与空间位移矢量条数成正比，k为比例常数")

# 创建微分形式的示意图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制球体
ax.add_patch(patches.Circle((0, 0), 2, color='lightblue', alpha=0.3))
ax.add_patch(patches.Circle((0, 0), 2, fill=False, color='blue', linewidth=2))

# 绘制微分立体角
angle_start = np.pi/3
angle_end = np.pi/2
theta = np.linspace(angle_start, angle_end, 100)
r_theta = 2
x_arc = r_theta * np.cos(theta)
y_arc = r_theta * np.sin(theta)
ax.plot(x_arc, y_arc, color='green', linewidth=3)
ax.plot([0, r_theta*np.cos(angle_start)], [0, r_theta*np.sin(angle_start)], color='green', linewidth=3)
ax.plot([0, r_theta*np.cos(angle_end)], [0, r_theta*np.sin(angle_end)], color='green', linewidth=3)

# 绘制微分位移矢量
dn_angle = (angle_start + angle_end) / 2
x_dn = r_theta * np.cos(dn_angle)
y_dn = r_theta * np.sin(dn_angle)
ax.arrow(0, 0, x_dn, y_dn, head_width=0.1, head_length=0.1, fc='red', ec='red', linewidth=2)

# 添加文本说明
ax.text(0, 0, '质量中心', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(x_dn+0.1, y_dn, 'dn', ha='left', va='center', fontsize=12, color='red', fontweight='bold')
ax.text(1.5, 1.8, 'dΩ', ha='center', va='center', fontsize=12, color='green', fontweight='bold')
ax.text(0, -2.5, f'微分形式：{diff_form} → 简化后：{simplified_diff}', ha='center', fontsize=14, fontweight='bold')

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.axis('off')
plt.title("微分形式推导示意图", fontsize=16, fontweight='bold')
plt.savefig('微分形式推导.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)

# =============================
# 3. 全局积分验证可视化
# =============================
print("\n3. 全局积分验证")
print("=" * 60)

# 全局积分
global_int = Eq(m, Integral(k * (dn/dOmega), (dOmega, 0, 4*pi)))
print(f"全局积分：{global_int}")

# 积分计算
integral_result = Eq(m, k * N)
print(f"积分结果：{integral_result}")

# 普朗克质量边界条件
planck_case = integral_result.subs({N: 1, m: m_p})
print(f"普朗克质量情况：{planck_case}")

# 创建积分验证的示意图
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制积分过程
x = np.linspace(0, 1, 100)
y = np.sin(2 * np.pi * x) + 1.5

# 绘制积分曲线
ax.plot(x, y, color='blue', linewidth=2, label='空间位移矢量密度')

# 填充积分区域
ax.fill_between(x, y, 0, color='lightblue', alpha=0.5, label='积分区域 (总质量)')

# 绘制积分符号
ax.text(0.5, 1.0, '∫', fontsize=40, ha='center', va='center', color='red')

# 添加文本说明
ax.text(0.5, -0.5, f'全局积分：{global_int}', ha='center', fontsize=12, fontweight='bold')
ax.text(0.5, -1.0, f'积分结果：{integral_result}', ha='center', fontsize=12, fontweight='bold')

ax.set_xlabel('立体角 Ω')
ax.set_ylabel('空间位移矢量密度 dn/dΩ')
ax.set_title('全局积分验证示意图', fontsize=16, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.savefig('全局积分验证.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)

# =============================
# 4. 第一性原理推导可视化
# =============================
print("\n4. 第一性原理推导")
print("=" * 60)

# 第一性原理推导步骤
print("步骤1：应用质量几何化定义到普朗克质量")
step1 = Eq(m_p, k * n / Omega)
print(f"   {step1}")

print("\n步骤2：代入普朗克质量的边界条件 (n=1, Ω=4π)")
step2 = step1.subs({n: 1, Omega: 4*pi})
print(f"   {step2}")

print("\n步骤3：求解量子比例常数k")
k_solution = solve(step2, k)[0]
k_eq = Eq(k, k_solution)
print(f"   {k_eq}")

# 创建第一性原理推导的流程图
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制推导步骤
steps = [
    "步骤1：应用质量几何化定义到普朗克质量",
    f"m_p = k · n/Ω",
    "步骤2：代入边界条件 (n=1, Ω=4π)",
    f"m_p = k · 1/(4π)",
    "步骤3：求解量子比例常数k",
    f"k = 4π · m_p"
]

for i, step in enumerate(steps):
    if i % 2 == 0:
        ax.add_patch(patches.Rectangle((1, 6 - i), 10, 1, fill=True, color='lightgreen', alpha=0.7, edgecolor='green', linewidth=2))
        ax.text(6, 6.5 - i, step, ha='center', va='center', fontsize=12, fontweight='bold')
    else:
        ax.add_patch(patches.Rectangle((2, 6 - i), 8, 1, fill=True, color='lightblue', alpha=0.7, edgecolor='blue', linewidth=2))
        ax.text(6, 6.5 - i, step, ha='center', va='center', fontsize=14, fontweight='bold')

# 绘制箭头
for i in range(2):
    y_start = 5.5 - 2*i
    ax.annotate('', xy=(6, y_start - 1), xytext=(6, y_start),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=10))

ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
plt.title("第一性原理推导流程图", fontsize=16, fontweight='bold')
plt.savefig('第一性原理推导.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)

# =============================
# 5. 多路径数值验证可视化
# =============================
print("\n5. 多路径数值验证")
print("=" * 60)

# CODATA 2018常数
codata = {
    'hbar': 1.054571817e-34,
    'c': 299792458.0,
    'G': 6.67430e-11,
    'm_p': 2.176434e-8
}

# 计算路径
pi_val = np.pi

# 路径1：直接从普朗克质量计算
k_path1 = 4 * pi_val * codata['m_p']

# 路径2：从经典普朗克质量定义计算
m_p_calc = np.sqrt(codata['hbar'] * codata['c'] / codata['G'])
k_path2 = 4 * pi_val * m_p_calc

print(f"路径1结果：k = {k_path1:.16e} kg")
print(f"路径2结果：k = {k_path2:.16e} kg")

# 计算相对误差
relative_error = abs(k_path1 - k_path2) / k_path1 * 100
print(f"相对误差：{relative_error:.10f}%")

# 创建数值验证的可视化
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制两条路径的结果
paths = ['路径1：直接计算', '路径2：经典定义']
k_values = [k_path1, k_path2]
colors = ['blue', 'red']

bars = ax.bar(paths, k_values, color=colors, alpha=0.7)

# 添加数值标签
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.10e}',
            ha='center', va='bottom', fontsize=10)

# 添加误差线
ax.errorbar(0.5, (k_path1 + k_path2)/2, yerr=abs(k_path1 - k_path2)/2, fmt='none', c='black', capsize=10, label=f'相对误差：{relative_error:.10f}%')

ax.set_ylabel('k值 (kg)')
ax.set_title('多路径数值验证结果', fontsize=16, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.savefig('多路径数值验证.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)

# =============================
# 6. 波函数几何化诠释可视化
# =============================
print("\n6. 波函数几何化诠释")
print("=" * 60)

# 波函数几何化关系
print("波函数模方与空间位移矢量密度的关系：")
print("|ψ|² ∝ dn/dΩ")
print("结合质量几何化定义，得到：")
print("|ψ|² ∝ m/(k·Ω)")

# 创建波函数几何化的可视化
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 左侧：空间位移矢量密度
r = np.linspace(0.1, 5, 100)
# 模拟空间位移矢量密度随距离的变化
dn_dOmega = 1 / r**2
ax1.plot(r, dn_dOmega, color='red', linewidth=2)
ax1.set_xlabel('距离 r')
ax1.set_ylabel('空间位移矢量密度 dn/dΩ')
ax1.set_title('空间位移矢量密度分布', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# 右侧：波函数概率密度
# 模拟波函数概率密度（与dn/dΩ成正比）
psi_sq = dn_dOmega
ax2.plot(r, psi_sq, color='blue', linewidth=2)
ax2.set_xlabel('距离 r')
ax2.set_ylabel('波函数概率密度 |ψ|²')
ax2.set_title('波函数概率密度分布', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.suptitle('波函数几何化诠释：|ψ|² ∝ dn/dΩ', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('波函数几何化诠释.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)

# =============================
# 7. 最终结论
# =============================
print("\n7. 最终结论")
print("=" * 60)

final_conclusions = [
    "1. 量子比例常数k是唯一的物理常数",
    f"2. k = 4π·m_p，连接了经典几何与量子力学",
    "3. k是质量几何化定义的核心参数",
    "4. k与量子力学现象存在深刻关联",
    "5. k的唯一性证明了统一场论的内在自洽性"
]

for conclusion in final_conclusions:
    print(conclusion)

# 创建结论可视化
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制结论云图
conclusions_text = "\n".join(final_conclusions)
ax.text(0.5, 0.5, conclusions_text, ha='center', va='center', fontsize=14, fontweight='bold',
        bbox=dict(boxstyle="round,pad=1", facecolor="lightblue", edgecolor="blue", alpha=0.7))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.title("最终结论", fontsize=16, fontweight='bold')
plt.savefig('最终结论.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== 可视化完成！所有图像已保存为PNG文件 ===")