    # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        import os
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
import numpy as np
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 三维螺旋时空方程: r(t) = r cos(ω t) i + r sin(ω t) j + h t k
# 参数说明:
# t: 时间变量
# r: 螺旋半径（常数，控制螺旋在XY平面上的投影大小）
# w: 角速度ω（控制螺旋在XY平面上的旋转快慢）
# h: 轴向移动系数（控制螺旋沿Z轴方向的移动速度）
# i, j, k: 分别为X、Y、Z轴的单位矢量
t = np.linspace(0, 4*np.pi, 100)  # 时间从0到4π，生成100个采样点
r, w, h = 2, 1, 0.3  # 设置螺旋半径、角速度和轴向移动系数

x = r * np.cos(w*t)
y = r * np.sin(w*t)
z = h * t

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, 'b-', linewidth=2, label='运动轨迹')
ax.quiver(0, 0, 0, r, 0, 0, color='r', linewidth=2, label='基矢量 i')
ax.quiver(0, 0, 0, 0, r, 0, color='g', linewidth=2, label='基矢量 j')
ax.quiver(0, 0, 0, 0, 0, h*4*np.pi, color='k', linewidth=2, label='基矢量 k')

ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴')
ax.set_title('三维螺旋时空方程 - 螺旋运动轨迹与速度分解', fontsize=14)
ax.legend()

# 添加matplotlib内置数学表达式渲染的完整公式

# 添加公式到图形中
equation_text = "三维螺旋时空方程: r(t) = r cos(ω t) i + r sin(ω t) j + h t k"
ax.text2D(0.05, 0.98, equation_text, transform=ax.transAxes, fontsize=12, 
          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))

# 添加专业级别的参数解释文本框，使用普通文本格式
params_text = "三维螺旋时空方程参数详解:\n" + \
              "1. t: 时间变量，描述质点运动状态随时间的演化过程\n" + \
              "2. r: 螺旋半径（常数），控制螺旋在XY平面上的投影圆半径大小\n" + \
              "3. ω: 角速度，决定质点在XY平面上做圆周运动的角频率\n" + \
              "4. h: 轴向移动系数，决定质点沿螺旋轴线（Z轴）方向的匀速运动速度\n" + \
              "5. i, j, k: 笛卡儿坐标系中X、Y、Z轴的单位矢量\n" + \
              "\n方程物理意义:\n" + \
              "- XY平面分量构成匀速圆周运动\n" + \
              "- Z轴分量构成匀速直线运动\n" + \
              "- 两者合成形成空间螺旋运动轨迹"
ax.text2D(0.05, 0.95, params_text, transform=ax.transAxes, fontsize=10, 
          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

plt.tight_layout()

# 保存图形为PNG文件
plt.savefig('./img/三维螺旋时空方程可视化.png', dpi=300, bbox_inches='tight')
print("三维螺旋时空方程可视化已保存为PNG文件")

# 在交互式环境中显示图形
try:
    plt.show()
except:
    print("在非交互式环境中运行，图形已保存但不显示")
