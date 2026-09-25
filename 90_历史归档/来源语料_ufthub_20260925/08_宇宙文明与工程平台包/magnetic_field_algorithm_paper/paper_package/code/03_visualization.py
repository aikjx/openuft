"""
Part 3: 可视化生成
  图1: 3D 闭环螺旋磁场轨迹
  图2: 贝塞尔函数 J_m(κr) 径向分布
  图3: 模态频谱 κ² vs n (传播/倏逝分界)
  图4: 横向磁场强度分布 |B(r,θ)|
  图5: 推导流程图
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy import special
import matplotlib.font_manager as fm

# 中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

OUT = '/home/user/Doubao/chats/38442004002046210/'

# 物理参数
a = 0.01
b = 0.01
L = 1.0
c = 2.99792458e8
ds = np.sqrt(a**2 + b**2)
omega = c / ds

# ============================================================
# 图1: 3D 闭环螺旋磁场轨迹
# ============================================================
fig = plt.figure(figsize=(14, 10))

# (a) 螺旋轨迹
ax1 = fig.add_subplot(221, projection='3d')
theta = np.linspace(0, 6*np.pi, 500)
r_helix = a
z_helix = b * theta
x_h = r_helix * np.cos(theta)
y_h = r_helix * np.sin(theta)
ax1.plot(x_h*100, y_h*100, z_helix*100, 'b-', linewidth=2, label='Helix path')
ax1.set_xlabel('x [cm]')
ax1.set_ylabel('y [cm]')
ax1.set_zlabel('z [cm]')
ax1.set_title('(a) Closed-loop helix trajectory\nr=a, z=bθ, ds=√(a²+b²)dθ')
ax1.legend(fontsize=8)

# (b) 螺旋上的场相位
ax2 = fig.add_subplot(222, projection='3d')
# 取 m=1, n=1 模态
m_val = 1
n_val = 1
kn = 2*np.pi*n_val/L
kappa = np.sqrt(1/(a**2+b**2) - kn**2)
# 沿螺旋的场强 (取实部)
B_helix = np.cos(m_val*theta - kn*z_helix)
colors = cm.coolwarm((B_helix - B_helix.min())/(B_helix.max()-B_helix.min()))
for i in range(len(theta)-1):
    ax2.plot(x_h[i:i+2]*100, y_h[i:i+2]*100, z_helix[i:i+2]*100,
             color=colors[i], linewidth=2.5)
ax2.set_xlabel('x [cm]')
ax2.set_ylabel('y [cm]')
ax2.set_zlabel('z [cm]')
ax2.set_title(f'(b) Field phase on helix\nm={m_val}, n={n_val}, B∝cos(mθ-kz)')

# (c) 弧长元示意
ax3 = fig.add_subplot(223)
theta2 = np.linspace(0, 2*np.pi, 200)
z2 = b * theta2
ax3.plot(theta2, z2*100, 'b-', linewidth=1.5)
# 标注一个弧长元
i_mid = 100
ax3.annotate('', xy=(theta2[i_mid+5], z2[i_mid+5]*100),
             xytext=(theta2[i_mid], z2[i_mid]*100),
             arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax3.text(theta2[i_mid]+0.3, z2[i_mid]*100+0.1, 'ds=√(a²+b²)dθ',
         color='red', fontsize=10)
ax3.set_xlabel('θ [rad]')
ax3.set_ylabel('z [cm]')
ax3.set_title('(c) Helix pitch: z=bθ')
ax3.grid(True, alpha=0.3)

# (d) 闭环条件示意
ax4 = fig.add_subplot(224)
ax4.set_xlim(-1.5, 1.5)
ax4.set_ylim(-1.5, 1.5)
circle = plt.Circle((0,0), 1, fill=False, color='blue', linewidth=2)
ax4.add_patch(circle)
# 标注
ax4.annotate('', xy=(0.95, 0.31), xytext=(0.95, -0.31),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
ax4.text(1.05, 0, 'm·2π\ninteger\nclosure', color='red', fontsize=9)
ax4.text(-1.4, 1.2, r'Angular closure:  e$^{im(θ+2π)}$=e$^{imθ}$', fontsize=10)
ax4.text(-1.4, 1.0, r'⇒ m ∈ ℤ', fontsize=10, color='blue')
ax4.text(-1.4, -1.2, r'Longitudinal closure: e$^{ik_n(z+L)}$=e$^{ik_nz}$', fontsize=10)
ax4.text(-1.4, -1.4, r'⇒ k$_n$ = 2πn/L', fontsize=10, color='blue')
ax4.set_aspect('equal')
ax4.set_title('(d) Double closure conditions')
ax4.axis('off')

plt.tight_layout()
plt.savefig(OUT + 'fig1_helix.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig1_helix.png 已生成")

# ============================================================
# 图2: 贝塞尔函数 J_m(κr) 径向分布
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

r_plot = np.linspace(0, 0.05, 500)  # 0-5 cm
kappa_demo = 70.0  # 典型 κ 值 [1/m]
r_dimless = kappa_demo * r_plot

ax = axes[0]
for m in range(4):
    Jm = special.jv(m, r_dimless)
    ax.plot(r_plot*100, Jm, linewidth=1.8, label=f'J_{m}(κr)')
ax.axhline(0, color='k', linewidth=0.5)
ax.set_xlabel('r [cm]')
ax.set_ylabel('J$_m$(κr)')
ax.set_title(f'(a) Bessel functions J$_m$ (κ={kappa_demo:.0f} m$^{{-1}}$)')
ax.legend()
ax.grid(True, alpha=0.3)

# 径向本征值谱
ax = axes[1]
n_range = np.arange(1, 16)
kn_vals = 2*np.pi*n_range/L
kappa2_vals = 1/(a**2+b**2) - kn_vals**2
colors_bar = ['#2196F3' if k >= 0 else '#F44336' for k in kappa2_vals]
ax.bar(n_range, kappa2_vals, color=colors_bar, edgecolor='black', linewidth=0.5)
ax.axhline(0, color='k', linewidth=1)
ax.axvline(11.5, color='green', linestyle='--', linewidth=1.5, label='Cutoff n=11')
ax.set_xlabel('Mode number n')
ax.set_ylabel('κ$_n^2$ [m$^{-2}$]')
ax.set_title('(b) Propagation spectrum: κ$_n^2$ vs n')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
ax.text(5, 2000, 'Propagating\nκ²≥0', ha='center', color='#2196F3', fontsize=10)
ax.text(13, -2000, 'Evanescent\nκ²<0', ha='center', color='#F44336', fontsize=10)

plt.tight_layout()
plt.savefig(OUT + 'fig2_bessel_spectrum.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig2_bessel_spectrum.png 已生成")

# ============================================================
# 图3: 横向磁场强度分布 |B(r,θ)|
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

m_vals_plot = [0, 1, 2]
for idx, m_val in enumerate(m_vals_plot):
    ax = axes[idx]
    # 网格
    N = 200
    r_grid = np.linspace(0.001, 0.04, N)
    th_grid = np.linspace(0, 2*np.pi, N)
    R, TH = np.meshgrid(r_grid, th_grid)
    X = R * np.cos(TH)
    Y = R * np.sin(TH)
    
    # |B| = |J_m(κr)| (取 n=1 模态)
    n_val = 1
    kn = 2*np.pi*n_val/L
    kappa = np.sqrt(1/(a**2+b**2) - kn**2)
    B_amp = np.abs(special.jv(m_val, kappa*R))
    
    # 极坐标画
    im = ax.pcolormesh(X*100, Y*100, B_amp, cmap='viridis', shading='auto')
    # 标注螺旋半径
    circle = plt.Circle((0,0), a*100, fill=False, color='red', linewidth=2, linestyle='--')
    ax.add_patch(circle)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect('equal')
    ax.set_xlabel('x [cm]')
    ax.set_ylabel('y [cm]')
    ax.set_title(f'|B| transverse, m={m_val}, n={n_val}\n(red dashed = helix radius a={a*100:.0f}cm)')
    plt.colorbar(im, ax=ax, label='|B| [A.U.]')

plt.tight_layout()
plt.savefig(OUT + 'fig3_field_pattern.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig3_field_pattern.png 已生成")

# ============================================================
# 图4: 推导流程图 + 约束关系图
# ============================================================
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# 流程框
boxes = [
    (1, 7.5, "Maxwell\nequations\n(no sources)", '#E3F2FD'),
    (4, 7.5, "Faraday curl\n+ ∇·E=0\n→ wave eq.", '#E8F5E9'),
    (7, 7.5, "Harmonic field\n→ Helmholtz\n∇²B̃+k₀²B̃=0", '#FFF3E0'),
    (10, 7.5, "Cylindrical\nseparation\nR(r)Θ(θ)Z(z)", '#F3E5F5'),
    (13, 7.5, "Bessel eq.\n→ J_m(κr)", '#FFEBEE'),
]
for x, y, text, color in boxes:
    rect = plt.Rectangle((x, y), 2.5, 1.2, facecolor=color, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x+1.25, y+0.6, text, ha='center', va='center', fontsize=9, fontweight='bold')

# 箭头
for x in [3.5, 6.5, 9.5, 12.5]:
    ax.annotate('', xy=(x+0.5, 8.1), xytext=(x, 8.1),
               arrowprops=dict(arrowstyle='->', lw=2))

# 分支条件
branches = [
    (2.5, 5.5, "Angular closure\nm∈Z\n(e^{i2πm}=1)", '#E8EAF6'),
    (7, 5.5, "Longitudinal closure\nk_n=2πn/L\n(period L)", '#E0F2F1'),
    (11.5, 5.5, "Light-speed constraint\nv=ω√(a²+b²)=c\n→ ω=c/√(a²+b²)", '#FFF8E1'),
]
for x, y, text, color in branches:
    rect = plt.Rectangle((x, y), 2.8, 1.3, facecolor=color, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x+1.4, y+0.65, text, ha='center', va='center', fontsize=9, fontweight='bold')

# 从主流程到分支
ax.annotate('', xy=(3.8, 6.8), xytext=(2.5, 7.5),
           arrowprops=dict(arrowstyle='->', lw=1.5, color='#555'))
ax.annotate('', xy=(7, 6.8), xytext=(7, 7.5),
           arrowprops=dict(arrowstyle='->', lw=1.5, color='#555'))
ax.annotate('', xy=(11.5, 6.8), xytext=(13, 7.5),
           arrowprops=dict(arrowstyle='->', lw=1.5, color='#555'))

# 最终方程
rect_final = plt.Rectangle((4.5, 2.5), 7, 1.5, facecolor='#FFF9C4', edgecolor='red', linewidth=2.5)
ax.add_patch(rect_final)
ax.text(8, 3.55, "B_{n,m} = A_{n,m} · J_m(κ_{n,m} r) · e^{i(mθ - k_n z - ω_n t)}",
        ha='center', va='center', fontsize=13, fontweight='bold')
ax.text(8, 2.9, "κ² = ω²/c² - k_n² ≥ 0  (propagation condition)",
        ha='center', va='center', fontsize=10, style='italic')

# 箭头到最终方程
for x in [3.9, 8.4, 12.9]:
    ax.annotate('', xy=(8, 4.0), xytext=(x, 5.5),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#888'))

# 底部: 与传统对比
ax.text(8, 1.5, "vs. Traditional circular waveguide:  κ quantized by wall J_m(κR)=0;  k continuous;  v_p≠c",
        ha='center', fontsize=10, color='#B71C1C', fontweight='bold')
ax.text(8, 0.8, "Novel:  k_n=2πn/L discrete;  ω=c/√(a²+b²) fixed;  closed-loop spiral light-speed flow",
        ha='center', fontsize=10, color='#1B5E20', fontweight='bold')

ax.set_title('Derivation & Constraint Flowchart', fontsize=14, fontweight='bold', pad=10)
plt.savefig(OUT + 'fig4_flowchart.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig4_flowchart.png 已生成")

# ============================================================
# 图5: 传统 vs 本算法 对比
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)

# 标题
ax.text(6, 7.5, 'Traditional Circular Waveguide vs. Closed-Loop Spiral Algorithm',
        ha='center', fontsize=14, fontweight='bold')

# 表格
col_labels = ['Dimension', 'Traditional waveguide', 'This algorithm']
rows = [
    ['Radial quantization', 'J_m(κR)=0 (wall)', 'No wall, κ free'],
    ['Angular quantization', 'm∈Z', 'm∈Z (same)'],
    ['Longitudinal k', 'continuous', 'k_n=2πn/L (discrete)'],
    ['Frequency relation', 'ω²=c²(k²+κ²)', 'ω=c/√(a²+b²) (fixed)'],
    ['Helix pitch', 'N/A', 'b=(m-1)/k_n (quantized)'],
    ['Cutoff', 'f>f_c propagates', 'n≤L/(2π√(a²+b²))'],
    ['Physical picture', 'Guided wave', 'Closed-loop c-speed flow'],
]

# 画表格
y_start = 6.5
row_h = 0.7
for j, label in enumerate(col_labels):
    x_pos = 0.5 + j * 3.8
    ax.text(x_pos + 1.5, y_start + 0.3, label, ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#37474F', edgecolor='none'))
    ax.texts[-1].set_color('white')

for i, row in enumerate(rows):
    y = y_start - (i+1)*row_h
    for j, cell in enumerate(row):
        x_pos = 0.5 + j * 3.8
        bg = '#F5F5F5' if i % 2 == 0 else '#FFFFFF'
        if j == 2:
            bg = '#E8F5E9'
        ax.text(x_pos + 1.5, y, cell, ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.2', facecolor=bg, edgecolor='#BDBDBD', linewidth=0.5))

plt.savefig(OUT + 'fig5_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig5_comparison.png 已生成")

print("\n所有可视化图已生成完毕。")
