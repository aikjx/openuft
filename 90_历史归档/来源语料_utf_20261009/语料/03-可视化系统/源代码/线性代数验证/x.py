import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform

class Arrow3D(FancyArrowPatch):
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._xyz = (x,y,z)
        self._dxdydz = (dx,dy,dz)

    def draw(self, renderer):
        x1,y1,z1 = self._xyz
        dx,dy,dz = self._dxdydz
        x2,y2,z2 = (x1+dx, y1+dy, z1+dz)
        
        xs, ys, zs = proj_transform([x1,x2], [y1,y2], [z1,z2], self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

def arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)

# 创建图形
fig = plt.figure(figsize=(20, 15))

# 1. 基本向量表示
ax1 = fig.add_subplot(231, projection='3d')
ax1.set_title('1. 空间位移向量 R 和光速向量 C\n(基本向量表示)', fontsize=12, pad=20)

# 原点（质点位置）
ax1.scatter(0, 0, 0, color='red', s=100, label='质点 O')

# 空间位移向量 R
arrow3D(ax1, 0, 0, 0, 3, 2, 4, mutation_scale=20, arrowstyle="-|>", color="blue", label='R: 空间位移向量')
ax1.text(1.5, 1, 2, 'R', color='blue', fontsize=12)

# 光速向量 C
arrow3D(ax1, 0, 0, 0, 2, 3, 1, mutation_scale=20, arrowstyle="-|>", color="green", label='C: 光速向量')
ax1.text(1, 1.5, 0.5, 'C', color='green', fontsize=12)

ax1.set_xlim([-1, 5])
ax1.set_ylim([-1, 5])
ax1.set_zlim([-1, 5])
ax1.legend()

# 2. 圆柱状螺旋运动
ax2 = fig.add_subplot(232, projection='3d')
ax2.set_title('2. 空间圆柱状螺旋运动\n(时空基本运动模式)', fontsize=12, pad=20)

t = np.linspace(0, 4*np.pi, 100)
z = t
x = np.cos(t)
y = np.sin(t)

ax2.plot(x, y, z, 'b-', linewidth=2, label='空间点运动轨迹')
ax2.scatter(0, 0, 0, color='red', s=100, label='质点 O')

# 显示旋转和直线分量
arrow3D(ax2, 0, 0, 2, 0.5, 0, 0, mutation_scale=15, arrowstyle="-|>", color="red", label='旋转分量')
arrow3D(ax2, 0, 0, 2, 0, 0, 0.5, mutation_scale=15, arrowstyle="-|>", color="green", label='直线分量')

ax2.legend()

# 3. 向量运算：动量 P = m(C - V)
ax3 = fig.add_subplot(233, projection='3d')
ax3.set_title('3. 动量向量运算: P = m(C - V)\n(线性代数运算)', fontsize=12, pad=20)

# 光速向量 C
arrow3D(ax3, 0, 0, 0, 4, 0, 0, mutation_scale=20, arrowstyle="-|>", color="green", label='C: 光速向量')

# 物体速度向量 V
arrow3D(ax3, 0, 0, 0, 1, 2, 0, mutation_scale=20, arrowstyle="-|>", color="orange", label='V: 物体速度')

# 相对速度向量 (C - V)
arrow3D(ax3, 0, 0, 0, 3, -2, 0, mutation_scale=20, arrowstyle="-|>", color="red", label='C - V: 相对速度')

ax3.text(2, 0, 0, 'C', color='green', fontsize=12)
ax3.text(0.5, 1, 0, 'V', color='orange', fontsize=12)
ax3.text(1.5, -1, 0, 'P ∝ (C-V)', color='red', fontsize=12)

ax3.set_xlim([-3, 5])
ax3.set_ylim([-3, 5])
ax3.legend()

# 4. 场向量运算：磁场 B = ∇ × A
ax4 = fig.add_subplot(234, projection='3d')
ax4.set_title('4. 磁场定义: B = ∇ × A\n(旋度运算)', fontsize=12, pad=20)

# 创建旋度场的示例
x = np.linspace(-2, 2, 6)
y = np.linspace(-2, 2, 6)
z = np.linspace(-2, 2, 6)
X, Y, Z = np.meshgrid(x, y, z)

# 引力场 A (径向场)
U = X  # x分量
V = Y  # y分量  
W = Z  # z分量

# 磁场 B = ∇ × A (旋度)
# 简化示例：旋度场围绕z轴旋转
for i in range(len(x)):
    for j in range(len(y)):
        for k in range(len(z)):
            if X[i,j,k]**2 + Y[i,j,k]**2 > 0.5:  # 避免中心点
                # 旋度场的箭头（围绕z轴）
                arrow3D(ax4, X[i,j,k], Y[i,j,k], Z[i,j,k], 
                       -Y[i,j,k]*0.3, X[i,j,k]*0.3, 0, 
                       mutation_scale=10, arrowstyle="-|>", color="purple", alpha=0.6)

ax4.scatter(0, 0, 0, color='red', s=100, label='源点')
ax4.text(0, 0, 2.5, 'B = ∇ × A', color='purple', fontsize=14, ha='center')
ax4.legend()

# 5. 坐标系变换
ax5 = fig.add_subplot(235, projection='3d')
ax5.set_title('5. 参考系变换的线性表示\n(矩阵变换)', fontsize=12, pad=20)

# 原坐标系
arrow3D(ax5, 0, 0, 0, 3, 0, 0, mutation_scale=20, arrowstyle="-|>", color="red", label='X轴')
arrow3D(ax5, 0, 0, 0, 0, 3, 0, mutation_scale=20, arrowstyle="-|>", color="green", label='Y轴')
arrow3D(ax5, 0, 0, 0, 0, 0, 3, mutation_scale=20, arrowstyle="-|>", color="blue", label='Z轴')

# 新坐标系（旋转后的）
theta = np.pi/4  # 45度旋转
arrow3D(ax5, 0, 0, 0, 3*np.cos(theta), 3*np.sin(theta), 0, 
        mutation_scale=20, arrowstyle="-|>", color="red", linestyle='--', label='X\'轴')
arrow3D(ax5, 0, 0, 0, -3*np.sin(theta), 3*np.cos(theta), 0, 
        mutation_scale=20, arrowstyle="-|>", color="green", linestyle='--', label='Y\'轴')
arrow3D(ax5, 0, 0, 0, 0, 0, 3, 
        mutation_scale=20, arrowstyle="-|>", color="blue", linestyle='--', label='Z\'轴')

ax5.text(1.5, 0, 0, '原坐标系', color='black', fontsize=10)
ax5.text(2, 2, 0, '新坐标系', color='black', fontsize=10)
ax5.legend()

# 6. 场方程的统一表示
ax6 = fig.add_subplot(236, projection='3d')
ax6.set_title('6. 统一场方程: F = dP/dt\n(力的统一描述)', fontsize=12, pad=20)

# 质点
ax6.scatter(0, 0, 0, color='red', s=100, label='受力物体')

# 各种力向量的表示
forces = {
    '电场力 Cdm/dt': (2, 1, 0, 'blue'),
    '磁场力 Vdm/dt': (1, -1, 1, 'green'), 
    '惯性力 mdV/dt': (-1, 2, 0, 'orange'),
    '核力 mdC/dt': (0, 1, 2, 'purple')
}

for i, (label, (dx, dy, dz, color)) in enumerate(forces.items()):
    arrow3D(ax6, 0, 0, 0, dx, dy, dz, 
            mutation_scale=15, arrowstyle="-|>", color=color, label=label)

# 合力
arrow3D(ax6, 0, 0, 0, 2, 3, 3, 
        mutation_scale=20, arrowstyle="-|>", color="red", linewidth=3, label='合力 F')

ax6.text(1, 1.5, 1.5, 'F = Σ各分力', color='red', fontsize=12)
ax6.legend()

plt.tight_layout()
plt.show()

# 补充：二维示意图显示线性代数的矩阵运算
fig2, axes = plt.subplots(2, 2, figsize=(15, 12))

# 7. 向量加法：力的合成
ax7 = axes[0, 0]
ax7.set_title('7. 向量加法：力的合成\n(线性叠加原理)', fontsize=12)

# 两个分力
ax7.arrow(0, 0, 3, 1, head_width=0.2, head_length=0.2, fc='blue', ec='blue', label='力 F1')
ax7.arrow(0, 0, 1, 3, head_width=0.2, head_length=0.2, fc='green', ec='green', label='力 F2')

# 合力
ax7.arrow(0, 0, 4, 4, head_width=0.2, head_length=0.2, fc='red', ec='red', linewidth=2, label='合力 F')

ax7.text(1.5, 0.5, 'F1', fontsize=12, color='blue')
ax7.text(0.5, 1.5, 'F2', fontsize=12, color='green')
ax7.text(2, 2, 'F = F1 + F2', fontsize=12, color='red')

ax7.set_xlim(-1, 5)
ax7.set_ylim(-1, 5)
ax7.set_aspect('equal')
ax7.legend()
ax7.grid(True, alpha=0.3)

# 8. 矩阵变换：坐标变换
ax8 = axes[0, 1]
ax8.set_title('8. 矩阵变换：参考系变换\n(线性变换)', fontsize=12)

# 原向量
ax8.arrow(0, 0, 3, 2, head_width=0.2, head_length=0.2, fc='blue', ec='blue', label='原向量 v')

# 变换后的向量（旋转45度）
theta = np.pi/4
vx_new = 3*np.cos(theta) - 2*np.sin(theta)
vy_new = 3*np.sin(theta) + 2*np.cos(theta)

ax8.arrow(0, 0, vx_new, vy_new, head_width=0.2, head_length=0.2, fc='red', ec='red', linestyle='--', label='变换后 v\'')

ax8.text(1.5, 1, 'v', fontsize=12, color='blue')
ax8.text(0.5, 3, "v' = M·v", fontsize=12, color='red')

ax8.set_xlim(-1, 4)
ax8.set_ylim(-1, 4)
ax8.set_aspect('equal')
ax8.legend()
ax8.grid(True, alpha=0.3)

# 9. 点积运算：功的计算
ax9 = axes[1, 0]
ax9.set_title('9. 点积运算：功 W = F·d\n(投影关系)', fontsize=12)

# 力向量
ax9.arrow(0, 0, 4, 2, head_width=0.2, head_length=0.2, fc='blue', ec='blue', label='力 F')

# 位移向量
ax9.arrow(0, 0, 3, 0, head_width=0.2, head_length=0.2, fc='green', ec='green', label='位移 d')

# 投影
ax9.plot([3, 3], [0, 2], 'k--', alpha=0.5)
ax9.plot([0, 3], [2, 2], 'k--', alpha=0.5)

ax9.text(2, 1, 'F', fontsize=12, color='blue')
ax9.text(1.5, -0.3, 'd', fontsize=12, color='green')
ax9.text(3.1, 1, 'F·cosθ', fontsize=10, color='black')

ax9.set_xlim(-1, 5)
ax9.set_ylim(-1, 3)
ax9.set_aspect('equal')
ax9.legend()
ax9.grid(True, alpha=0.3)

# 10. 叉积运算：力矩计算
ax10 = axes[1, 1]
ax10.set_title('10. 叉积运算：力矩 τ = r × F\n(垂直关系)', fontsize=12)

# 位置向量
ax10.arrow(0, 0, 2, 1, head_width=0.2, head_length=0.2, fc='blue', ec='blue', label='位置 r')

# 力向量
ax10.arrow(2, 1, 1, -2, head_width=0.2, head_length=0.2, fc='green', ec='green', label='力 F')

# 力矩方向（垂直纸面向外）
ax10.scatter(2, 1, color='red', s=100)
ax10.text(2.2, 0.8, 'τ = r × F\n(垂直向外)', fontsize=10, color='red')

ax10.text(1, 0.5, 'r', fontsize=12, color='blue')
ax10.text(2.5, 0, 'F', fontsize=12, color='green')

ax10.set_xlim(-1, 4)
ax10.set_ylim(-2, 2)
ax10.set_aspect('equal')
ax10.legend()
ax10.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 打印关键公式的文本表示
print("="*80)
print("张祥前统一场论中线性代数应用的关键公式")
print("="*80)

formulas = {
    "时空同一化方程": "R = C t",
    "动量定义": "P = m (C - V)", 
    "力方程（统一形式）": "F = dP/dt = C dm/dt - V dm/dt + m dC/dt - m dV/dt",
    "磁场定义": "B = ∇ × A",
    "电场与引力场关系": "E = -f dA/dt",
    "质量几何定义": "m = k n / Ω",
    "电荷定义": "q = k' dΩ/dt",
    "参考系变换": "x' = M x (线性变换)"
}

print("\n核心物理量的向量表示：")
for name, formula in formulas.items():
    print(f"• {name}: {formula}")

print("\n线性代数运算的物理意义：")
operations = {
    "向量加法": "物理量的叠加（如力的合成）",
    "数乘": "物理量的缩放",
    "点积": "功、能量等标量的计算", 
    "叉积": "力矩、磁场等向量的计算",
    "梯度∇": "场的变化率",
    "散度∇·": "场的源强度",
    "旋度∇×": "场的旋转程度",
    "矩阵乘法": "参考系变换"
}

for op, meaning in operations.items():
    print(f"• {op}: {meaning}")
