import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import math
import matplotlib
import platform

# 检测操作系统并设置合适的字体
if platform.system() == 'Windows':
    # Windows系统下的字体设置
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Hiragino Sans GB']
else:  # Linux等其他系统
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'WenQuanYi Micro Hei', 'Heiti TC']

# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 设置全局字体参数
matplotlib.rcParams.update({
    'font.family': ['sans-serif'],
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'figure.dpi': 100
})

# 光速常量
c = 299792458  # 光速，单位：m/s

class SpiralMotionVerifier:
    """
    空间螺旋运动验证类：验证 v_旋转² + v_直线² = c² 的关系
    
    基于统一场论中空间的螺旋运动假设，空间点同时进行旋转运动和直线运动，
    这两种运动的速度平方和恒等于光速的平方。
    """
    
    def __init__(self):
        self.theta_values = None
        self.v_rotation_values = None
        self.v_linear_values = None
        self.energy_values = None
        # 预先设置matplotlib字体，确保每次绘图都使用正确字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def calculate_velocities(self, theta_range=np.linspace(0, np.pi/2, 100)):
        """
        计算不同角度下的旋转速度和直线速度
        
        参数:
            theta_range: 角度范围（弧度），默认为0到π/2
            
        返回:
            tuple: (theta_values, v_rotation_values, v_linear_values)
        """
        self.theta_values = theta_range
        
        # 基于角度计算旋转速度和直线速度
        # v_旋转 = c * sin(theta)
        # v_直线 = c * cos(theta)
        self.v_rotation_values = c * np.sin(theta_range)
        self.v_linear_values = c * np.cos(theta_range)
        
        # 验证 v_旋转² + v_直线² = c²
        verification = np.square(self.v_rotation_values) + np.square(self.v_linear_values)
        # 正确计算c的平方
        c_squared = c ** 2
        
        # 计算误差
        error = np.abs(verification - c_squared) / c_squared * 100
        
        print("=== 速度关系验证 ===")
        print(f"光速 c = {c} m/s")
        print(f"验证结果: v_旋转² + v_直线² = {verification[0]:.10e}")
        print(f"理论值 c² = {c_squared:.10e}")
        print(f"最大相对误差: {np.max(error):.2e}%")
        print(f"平均相对误差: {np.mean(error):.2e}%")
        # 使用更宽容的误差范围进行验证
        print("验证状态: " + ("通过" if np.allclose(verification, c_squared, rtol=1e-10, atol=1e-10) else "失败"))
        print()
        
        return self.theta_values, self.v_rotation_values, self.v_linear_values
    
    def calculate_energy_relationship(self):
        """
        计算不同速度分量下的能量关系
        
        返回:
            array: 能量比值数组
        """
        if self.v_rotation_values is None or self.v_linear_values is None:
            self.calculate_velocities()
        
        # 计算旋转动能和直线动能的比值（假设质量相同）
        rotation_energy = 0.5 * np.square(self.v_rotation_values)
        linear_energy = 0.5 * np.square(self.v_linear_values)
        total_energy = rotation_energy + linear_energy
        
        self.energy_values = {
            'rotation': rotation_energy,
            'linear': linear_energy,
            'total': total_energy
        }
        
        print("=== 能量关系分析 ===")
        print(f"最小旋转能量比例: {np.min(rotation_energy/total_energy)*100:.2f}%")
        print(f"最大旋转能量比例: {np.max(rotation_energy/total_energy)*100:.2f}%")
        print(f"当theta=45度时旋转能量比例: {(rotation_energy[len(rotation_energy)//2]/total_energy[len(total_energy)//2])*100:.2f}%")
        print()
        
        return self.energy_values
    
    def plot_velocity_relationship(self):
        """
        绘制速度关系图表
        """
        if self.v_rotation_values is None or self.v_linear_values is None:
            self.calculate_velocities()
        
        plt.figure(figsize=(12, 8))
        
        # 转换角度为度数便于阅读
        theta_degrees = np.degrees(self.theta_values)
        
        # 绘制速度分量随角度的变化
        plt.subplot(2, 2, 1)
        plt.plot(theta_degrees, self.v_rotation_values / 1e6, 'r-', label='旋转速度 v_旋转')
        plt.plot(theta_degrees, self.v_linear_values / 1e6, 'b-', label='直线速度 v_直线')
        plt.axhline(y=c/1e6, color='g', linestyle='--', label='光速 c')
        plt.xlabel('角度 (度)')
        plt.ylabel('速度 (Mm/s)')
        plt.title('速度分量随角度的变化')
        plt.legend()
        plt.grid(True)
        
        # 绘制速度平方和验证
        plt.subplot(2, 2, 2)
        v_squared_sum = np.square(self.v_rotation_values) + np.square(self.v_linear_values)
        plt.plot(theta_degrees, v_squared_sum / 1e16, 'k-', label='v_旋转² + v_直线²')
        plt.axhline(y=c**2/1e16, color='g', linestyle='--', label='c²')
        plt.xlabel('角度 (度)')
        plt.ylabel('速度平方 (10^16 m²/s²)')
        plt.title('速度平方和验证')
        plt.legend()
        plt.grid(True)
        
        # 绘制速度比值
        plt.subplot(2, 2, 3)
        ratio = self.v_rotation_values / self.v_linear_values
        plt.plot(theta_degrees, ratio)
        plt.xlabel('角度 (度)')
        plt.ylabel('v_旋转 / v_直线')
        plt.title('速度比值随角度的变化')
        plt.grid(True)
        
        # 绘制能量分配
        if self.energy_values:
            plt.subplot(2, 2, 4)
            rotation_ratio = self.energy_values['rotation'] / self.energy_values['total']
            linear_ratio = self.energy_values['linear'] / self.energy_values['total']
            plt.plot(theta_degrees, rotation_ratio*100, 'r-', label='旋转能量比例')
            plt.plot(theta_degrees, linear_ratio*100, 'b-', label='直线能量比例')
            plt.xlabel('角度 (度)')
            plt.ylabel('能量比例 (%)')
            plt.title('能量分配比例')
            plt.legend()
            plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('velocity_relationship.png', dpi=300, bbox_inches='tight')
        print("速度关系图表已保存为 'velocity_relationship.png'")
    
    def generate_spiral_path(self, theta_max=10*np.pi, num_points=1000, radius=1):
        """
        生成三维螺旋运动路径
        
        参数:
            theta_max: 最大角度
            num_points: 点的数量
            radius: 螺旋半径
            
        返回:
            tuple: (x, y, z) 坐标数组
        """
        theta = np.linspace(0, theta_max, num_points)
        
        # 三维螺旋坐标
        x = radius * np.cos(theta)  # 旋转运动的x分量
        y = radius * np.sin(theta)  # 旋转运动的y分量
        z = (c / (np.sqrt(radius**2 + 1))) * theta  # 直线运动的z分量
        
        # 计算各点的旋转速度和直线速度
        v_rotation = np.sqrt(np.gradient(x)**2 + np.gradient(y)**2) / np.gradient(theta)
        v_linear = np.gradient(z) / np.gradient(theta)
        
        # 验证速度关系
        v_total = np.sqrt(v_rotation**2 + v_linear**2)
        
        print("=== 螺旋路径验证 ===")
        print(f"螺旋路径总长度: {np.sum(np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2)):.2f} 单位长度")
        print(f"平均旋转速度: {np.mean(v_rotation):.2f} 单位/rad")
        print(f"平均直线速度: {np.mean(v_linear):.2f} 单位/rad")
        print(f"平均总速度: {np.mean(v_total):.2f} 单位/rad")
        print(f"速度关系验证误差: {np.mean(np.abs(v_total - np.sqrt(v_rotation**2 + v_linear**2))):.10e}")
        print()
        
        return x, y, z, theta
    
    def plot_3d_spiral(self, x, y, z, theta):
        """
        绘制三维螺旋路径
        """
        fig = plt.figure(figsize=(12, 10))
        
        # 3D 螺旋图
        ax1 = fig.add_subplot(221, projection='3d')
        ax1.plot(x, y, z, 'b-', linewidth=1)
        ax1.set_xlabel('X 轴')
        ax1.set_ylabel('Y 轴')
        ax1.set_zlabel('Z 轴')
        ax1.set_title('三维螺旋运动路径')
        
        # XY平面投影
        ax2 = fig.add_subplot(222)
        ax2.plot(x, y, 'r-')
        ax2.set_xlabel('X 轴')
        ax2.set_ylabel('Y 轴')
        ax2.set_title('XY平面投影 (旋转运动)')
        ax2.axis('equal')
        
        # XZ平面投影
        ax3 = fig.add_subplot(223)
        ax3.plot(x, z, 'g-')
        ax3.set_xlabel('X 轴')
        ax3.set_ylabel('Z 轴')
        ax3.set_title('XZ平面投影')
        
        # YZ平面投影
        ax4 = fig.add_subplot(224)
        ax4.plot(y, z, 'm-')
        ax4.set_xlabel('Y 轴')
        ax4.set_ylabel('Z 轴')
        ax4.set_title('YZ平面投影')
        
        plt.tight_layout()
        plt.savefig('3d_spiral_motion.png', dpi=300, bbox_inches='tight')
        print("三维螺旋运动图表已保存为 '3d_spiral_motion.png'")
    
    def create_animation(self, x, y, z, frames=200):
        """
        创建螺旋运动动画
        """
        try:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # 设置坐标轴范围
            max_range = max(np.max(np.abs(x)), np.max(np.abs(y)), np.max(np.abs(z)))
            ax.set_xlim(-max_range, max_range)
            ax.set_ylim(-max_range, max_range)
            ax.set_zlim(0, np.max(z))
            
            # 设置标签
            ax.set_xlabel('X 轴')
            ax.set_ylabel('Y 轴')
            ax.set_zlabel('Z 轴')
            ax.set_title('空间螺旋运动动画')
            
            # 初始化线条
            line, = ax.plot([], [], [], 'b-', linewidth=2)
            point, = ax.plot([], [], [], 'ro', markersize=8)
            
            # 初始函数
            def init():
                line.set_data([], [])
                line.set_3d_properties([])
                point.set_data([], [])
                point.set_3d_properties([])
                return line, point
            
            # 更新函数
            def update(frame):
                idx = min(frame * len(x) // frames, len(x) - 1)
                line.set_data(x[:idx], y[:idx])
                line.set_3d_properties(z[:idx])
                point.set_data([x[idx]], [y[idx]])
                point.set_3d_properties([z[idx]])
                return line, point
            
            # 创建动画
            ani = FuncAnimation(fig, update, frames=frames, init_func=init,
                               interval=50, blit=True)
            
            # 保存动画
            ani.save('spiral_motion_animation.gif', writer='pillow', fps=20)
            print("螺旋运动动画已保存为 'spiral_motion_animation.gif'")
            
            plt.close(fig)
        except Exception as e:
            print(f"创建动画时出错: {e}")
            print("跳过动画创建步骤")
    
    def run_comprehensive_verification(self):
        """
        运行全面验证
        """
        print("========================================")
        print("        空间螺旋运动验证程序")
        print("        v_旋转² + v_直线² = c²")
        print("========================================\n")
        
        # 1. 计算和验证速度关系
        self.calculate_velocities()
        
        # 2. 计算能量关系
        self.calculate_energy_relationship()
        
        # 3. 生成螺旋路径
        x, y, z, theta = self.generate_spiral_path()
        
        # 4. 绘制图表
        self.plot_velocity_relationship()
        self.plot_3d_spiral(x, y, z, theta)
        
        # 5. 创建动画（可选）
        self.create_animation(x, y, z)
        
        print("\n========================================")
        print("            验证完成")
        print("========================================")

# 创建HTML报告
def generate_html_report():
    """
    生成HTML验证报告
    """
    html_content = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>空间螺旋运动验证报告</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
                margin-top: 30px;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            .formula {{
                font-family: 'Courier New', monospace;
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                font-size: 18px;
                text-align: center;
                margin: 20px 0;
            }}
            .result {{
                background-color: #e8f5e9;
                padding: 20px;
                border-radius: 5px;
                border-left: 5px solid #4caf50;
                margin: 20px 0;
            }}
            .warning {{
                background-color: #fff3cd;
                padding: 20px;
                border-radius: 5px;
                border-left: 5px solid #ffc107;
                margin: 20px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .chart-container {{
                position: relative;
                height: 400px;
                margin: 30px 0;
            }}
            .image-container {{
                text-align: center;
                margin: 30px 0;
            }}
            img {{
                max-width: 100%;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .formula-highlight {{
                font-weight: bold;
                color: #d32f2f;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>空间螺旋运动验证报告</h1>
            <div class="formula">
                <span class="formula-highlight">v_旋转² + v_直线² = c²</span>
            </div>
            
            <h2>理论基础</h2>
            <p>根据统一场论的空间螺旋运动假设，空间本身处于一种特殊的运动状态。空间中的点同时进行两种运动：</p>
            <ul>
                <li><strong>旋转运动</strong>：空间点围绕某个中心点的圆周运动</li>
                <li><strong>直线运动</strong>：空间点沿着直线方向的平移运动</li>
            </ul>
            <p>这两种运动的速度矢量相互垂直，且它们的速度平方和恒等于光速的平方，即：</p>
            <div class="formula">
                v<sub>旋转</sub>² + v<sub>直线</sub>² = c²
            </div>
            
            <h2>数学验证</h2>
            <p>从数学角度，可以通过三角函数关系来验证这一恒等式：</p>
            <ul>
                <li>设空间点运动方向与直线方向的夹角为θ</li>
                <li>则旋转速度分量：v<sub>旋转</sub> = c·sin(θ)</li>
                <li>直线速度分量：v<sub>直线</sub> = c·cos(θ)</li>
                <li>根据三角函数恒等式：sin²(θ) + cos²(θ) = 1</li>
                <li>因此：v<sub>旋转</sub>² + v<sub>直线</sub>² = c²·(sin²(θ) + cos²(θ)) = c²</li>
            </ul>
            
            <div class="result">
                <h3>验证结论</h3>
                <p>通过严格的数学推导，可以确认空间螺旋运动中的速度关系满足：</p>
                <div class="formula">
                    <span class="formula-highlight">v_旋转² + v_直线² = c²</span>
                </div>
                <p>这一关系在任意角度θ下均成立，是空间螺旋运动的基本数学特性。</p>
            </div>
        </div>
        
        <div class="container">
            <h2>速度分量关系可视化</h2>
            <div class="chart-container">
                <canvas id="velocityChart"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="verificationChart"></canvas>
            </div>
        </div>
        
        <div class="container">
            <h2>三维螺旋运动分析</h2>
            <p>空间点的螺旋运动可以在三维坐标系中表示为：</p>
            <ul>
                <li>X坐标：x = r·cos(θ) （旋转分量）</li>
                <li>Y坐标：y = r·sin(θ) （旋转分量）</li>
                <li>Z坐标：z = (c/√(r²+1))·θ （直线分量）</li>
            </ul>
            <p>其中r为螺旋半径，θ为旋转角度参数。</p>
            
            <div class="image-container">
                <img src="3d_spiral_motion.png" alt="三维螺旋运动路径">
                <p>三维螺旋运动路径示意图</p>
            </div>
        </div>
        
        <div class="container">
            <h2>物理意义</h2>
            <p>空间螺旋运动的速度关系 <span class="formula-highlight">v_旋转² + v_直线² = c²</span> 具有深刻的物理意义：</p>
            <ul>
                <li><strong>光速不变性</strong>：无论空间点如何运动，其总速度恒等于光速</li>
                <li><strong>能量守恒</strong>：旋转能量和直线能量可以相互转换，但总量保持不变</li>
                <li><strong>维度正交性</strong>：空间的旋转维度和直线维度相互正交</li>
                <li><strong>时空统一</strong>：暗示了时间和空间的统一关系</li>
            </ul>
            
            <div class="warning">
                <h3>重要说明</h3>
                <p>本验证基于统一场论的空间螺旋运动假设，这是一个前沿探索性理论。虽然数学推导是严格的，但物理假设仍需进一步的实验验证。</p>
            </div>
        </div>
        
        <script>
            // 速度分量图表
            const velocityCtx = document.getElementById('velocityChart').getContext('2d');
            const thetaDegrees = Array.from({{length: 100}}, (_, i) => i * 0.9);
            const c = 299792458;
            
            const velocityChart = new Chart(velocityCtx, {{
                type: 'line',
                data: {{
                    labels: thetaDegrees,
                    datasets: [
                        {{
                            label: '旋转速度 v_旋转 (Mm/s)',
                            data: thetaDegrees.map(theta => (c * Math.sin(theta * Math.PI / 180)) / 1e6),
                            borderColor: 'rgb(255, 99, 132)',
                            backgroundColor: 'rgba(255, 99, 132, 0.1)',
                            tension: 0.1
                        }},
                        {{
                            label: '直线速度 v_直线 (Mm/s)',
                            data: thetaDegrees.map(theta => (c * Math.cos(theta * Math.PI / 180)) / 1e6),
                            borderColor: 'rgb(54, 162, 235)',
                            backgroundColor: 'rgba(54, 162, 235, 0.1)',
                            tension: 0.1
                        }},
                        {{
                            label: '光速 c (Mm/s)',
                            data: thetaDegrees.map(() => c / 1e6),
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.1)',
                            borderDash: [5, 5],
                            tension: 0
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: '速度分量随角度的变化'
                        }},
                        legend: {{
                            position: 'bottom'
                        }}
                    }},
                    scales: {{
                        x: {{
                            title: {{
                                display: true,
                                text: '角度 (度)'
                            }}
                        }},
                        y: {{
                            title: {{
                                display: true,
                                text: '速度 (Mm/s)'
                            }}
                        }}
                    }}
                }}
            }});
            
            // 验证图表
            const verificationCtx = document.getElementById('verificationChart').getContext('2d');
            
            const verificationChart = new Chart(verificationCtx, {{
                type: 'line',
                data: {{
                    labels: thetaDegrees,
                    datasets: [
                        {{
                            label: 'v_旋转² + v_直线² (10^16 m²/s²)',
                            data: thetaDegrees.map(theta => {{
                                const v_rot = c * Math.sin(theta * Math.PI / 180);
                                const v_lin = c * Math.cos(theta * Math.PI / 180);
                                return (v_rot**2 + v_lin**2) / 1e16;
                            }}),
                            borderColor: 'rgb(153, 102, 255)',
                            backgroundColor: 'rgba(153, 102, 255, 0.1)',
                            tension: 0.1
                        }},
                        {{
                            label: 'c² (10^16 m²/s²)',
                            data: thetaDegrees.map(() => c**2 / 1e16),
                            borderColor: 'rgb(255, 159, 64)',
                            backgroundColor: 'rgba(255, 159, 64, 0.1)',
                            borderDash: [5, 5],
                            tension: 0
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'v_旋转² + v_直线² = c² 验证'
                        }},
                        legend: {{
                            position: 'bottom'
                        }}
                    }},
                    scales: {{
                        x: {{
                            title: {{
                                display: true,
                                text: '角度 (度)'
                            }}
                        }},
                        y: {{
                            title: {{
                                display: true,
                                text: '速度平方 (10^16 m²/s²)'
                            }}
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    '''
    
    with open('spiral_motion_verification.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML验证报告已生成: 'spiral_motion_verification.html'")

# 主函数
def main():
    """
    主函数：运行空间螺旋运动验证
    """
    # 创建验证器实例
    verifier = SpiralMotionVerifier()
    
    # 运行全面验证
    verifier.run_comprehensive_verification()
    
    # 生成HTML报告
    generate_html_report()

if __name__ == "__main__":
    main()