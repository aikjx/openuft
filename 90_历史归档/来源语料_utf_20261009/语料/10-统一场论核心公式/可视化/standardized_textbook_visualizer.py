import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any

# 设置全局中文字体和绘图参数
plt.rcParams.update({
    "font.family": ["SimHei", "Microsoft YaHei", "SimSun", "Arial"],
    "axes.unicode_minus": False,
    "text.usetex": False,
    "mathtext.fontset": "cm",
    "font.sans-serif": ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC'],
    "figure.figsize": (14, 12),
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12
})

class StandardizedTextbookVisualizer:
    """
    标准化的教科书级别可视化器
    为统一场论中的每个公式生成高质量的可视化
    """
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, "standardized_textbook_visualizations")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 定义所有公式的信息
        self.formula_info = {
            "01-时空同一化方程": {
                "name": "时空同一化方程",
                "equation": "x = ct",
                "description": "时空本质的数学表达",
                "parameters": [
                    {"symbol": "x", "name": "空间坐标", "description": "描述物体在空间中的位置"},
                    {"symbol": "c", "name": "光速", "description": "宇宙中信息传播的最大速度"},
                    {"symbol": "t", "name": "时间坐标", "description": "描述事件发生的顺序"}
                ],
                "physical_meaning": "揭示了空间和时间的本质联系，它们是同一物理实体的不同表现形式。在高速运动或强引力场中，空间和时间会相互转化。"
            },
            "02三维螺旋时空方程": {
                "name": "三维螺旋时空方程",
                "equation": "r(t) = r cos(ω t) i + r sin(ω t) j + h t k",
                "description": "空间运动的螺旋本质",
                "parameters": [
                    {"symbol": "r(t)", "name": "位置矢量", "description": "描述物体在三维空间中的运动轨迹"},
                    {"symbol": "r", "name": "螺旋半径", "description": "描述圆周运动的规模"},
                    {"symbol": "ω", "name": "角速度", "description": "描述圆周运动的快慢"},
                    {"symbol": "h", "name": "轴向移动系数", "description": "描述轴向运动的速度"},
                    {"symbol": "t", "name": "时间变量", "description": "描述运动的时间进程"},
                    {"symbol": "i, j, k", "name": "单位矢量", "description": "三维空间的基矢量"}
                ],
                "physical_meaning": "描述了空间中物体运动的本质形式。所有物质在空间中都以螺旋轨迹运动，这是统一场论中空间基本属性的体现。"
            },
            "03质量定义方程": {
                "name": "质量定义方程",
                "equation": "m = k · dn/dΩ",
                "description": "质量的空间本质",
                "parameters": [
                    {"symbol": "m", "name": "物体的质量", "description": "物体惯性和引力属性的量度"},
                    {"symbol": "k", "name": "比例常数", "description": "与空间基本属性相关的系数"},
                    {"symbol": "dn/dΩ", "name": "空间运动量密度", "description": "单位立体角内的空间运动量变化率"},
                    {"symbol": "Ω", "name": "立体角", "description": "描述空间方向的量度，单位为球面度(sr)"}
                ],
                "physical_meaning": "从空间几何角度重新定义了质量，揭示了质量是空间运动量分布特征的表现。质量并非物体的固有属性，而是空间运动效应的结果。"
            },
            "04引力场定义方程": {
                "name": "引力场定义方程",
                "equation": "F_g = G · m₁m₂/r²",
                "description": "引力场的数学表达",
                "parameters": [
                    {"symbol": "F_g", "name": "引力", "description": "物体间的引力相互作用"},
                    {"symbol": "G", "name": "引力常数", "description": "描述引力强度的常数"},
                    {"symbol": "m₁, m₂", "name": "物体质量", "description": "两个相互作用物体的质量"},
                    {"symbol": "r", "name": "距离", "description": "两个物体质心之间的距离"}
                ],
                "physical_meaning": "描述了物体间引力相互作用的规律，是牛顿万有引力定律的数学表达式。"
            },
            "05静止动量方程": {
                "name": "静止动量方程",
                "equation": "p₀ = m₀c",
                "description": "静止物体的动量",
                "parameters": [
                    {"symbol": "p₀", "name": "静止动量", "description": "静止物体的动量"},
                    {"symbol": "m₀", "name": "静止质量", "description": "物体静止时的质量"},
                    {"symbol": "c", "name": "光速", "description": "宇宙中信息传播的最大速度"}
                ],
                "physical_meaning": "揭示了静止物体也具有动量，这是相对论的重要结论，表明质量和能量是等价的。"
            },
            "06运动动量方程": {
                "name": "运动动量方程",
                "equation": "p = γm₀v",
                "description": "运动物体的动量",
                "parameters": [
                    {"symbol": "p", "name": "动量", "description": "运动物体的动量"},
                    {"symbol": "γ", "name": "洛伦兹因子", "description": "相对论效应的修正因子"},
                    {"symbol": "m₀", "name": "静止质量", "description": "物体静止时的质量"},
                    {"symbol": "v", "name": "速度", "description": "物体的运动速度"}
                ],
                "physical_meaning": "描述了相对论效应下运动物体的动量，当速度接近光速时，动量会显著增加。"
            },
            "07宇宙大统一方程": {
                "name": "宇宙大统一方程",
                "equation": "F = ma + ∇·(mφ)",
                "description": "宇宙中所有力的统一表达",
                "parameters": [
                    {"symbol": "F", "name": "合力", "description": "作用在物体上的所有力的矢量和"},
                    {"symbol": "m", "name": "质量", "description": "物体的质量"},
                    {"symbol": "a", "name": "加速度", "description": "物体的加速度"},
                    {"symbol": "∇·", "name": "散度", "description": "描述场的发散程度"},
                    {"symbol": "φ", "name": "场势", "description": "描述场的势函数"}
                ],
                "physical_meaning": "试图统一描述宇宙中所有的力，包括引力、电磁力、强核力和弱核力。"
            },
            "08三维空间波动方程": {
                "name": "三维空间波动方程",
                "equation": "∂²L/∂x² + ∂²L/∂y² + ∂²L/∂z² = (1/c²) ∂²L/∂t²",
                "description": "空间波动的数学表达",
                "parameters": [
                    {"symbol": "L", "name": "波函数", "description": "描述波的振幅分布"},
                    {"symbol": "c", "name": "波速", "description": "波的传播速度"},
                    {"symbol": "t", "name": "时间", "description": "时间变量"},
                    {"symbol": "x, y, z", "name": "空间坐标", "description": "三维空间坐标"}
                ],
                "physical_meaning": "描述了波在三维空间中的传播规律，适用于电磁波、声波等各种波动现象。"
            },
            "09引力场与旋转速度关系": {
                "name": "引力场与旋转速度关系",
                "equation": "v² = G M / r",
                "description": "天体旋转速度与引力场的关系",
                "parameters": [
                    {"symbol": "v", "name": "旋转速度", "description": "天体的旋转速度"},
                    {"symbol": "G", "name": "引力常数", "description": "描述引力强度的常数"},
                    {"symbol": "M", "name": "中心天体质量", "description": "中心天体的质量"},
                    {"symbol": "r", "name": "距离", "description": "到中心天体的距离"}
                ],
                "physical_meaning": "描述了天体在引力场中的旋转速度规律，解释了星系旋转曲线等天文现象。"
            },
            "10电场定义方程": {
                "name": "电场定义方程",
                "equation": "E = F/q",
                "description": "电场强度的定义",
                "parameters": [
                    {"symbol": "E", "name": "电场强度", "description": "描述电场的强度"},
                    {"symbol": "F", "name": "电场力", "description": "电场对电荷的作用力"},
                    {"symbol": "q", "name": "电荷", "description": "检验电荷的电量"}
                ],
                "physical_meaning": "定义了电场强度，描述了电场对电荷的作用力特性。"
            },
            "11磁场定义方程": {
                "name": "磁场定义方程",
                "equation": "B = F/(qv)",
                "description": "磁感应强度的定义",
                "parameters": [
                    {"symbol": "B", "name": "磁感应强度", "description": "描述磁场的强度"},
                    {"symbol": "F", "name": "洛伦兹力", "description": "磁场对运动电荷的作用力"},
                    {"symbol": "q", "name": "电荷", "description": "运动电荷的电量"},
                    {"symbol": "v", "name": "速度", "description": "电荷的运动速度"}
                ],
                "physical_meaning": "定义了磁感应强度，描述了磁场对运动电荷的作用力特性。"
            },
            "12电磁场能量方程": {
                "name": "电磁场能量方程",
                "equation": "u = (1/2)ε₀E² + (1/2)μ₀B²",
                "description": "电磁场的能量密度",
                "parameters": [
                    {"symbol": "u", "name": "能量密度", "description": "电磁场的能量密度"},
                    {"symbol": "ε₀", "name": "真空介电常数", "description": "描述真空电特性的常数"},
                    {"symbol": "E", "name": "电场强度", "description": "电场的强度"},
                    {"symbol": "μ₀", "name": "真空磁导率", "description": "描述真空磁特性的常数"},
                    {"symbol": "B", "name": "磁感应强度", "description": "磁场的强度"}
                ],
                "physical_meaning": "描述了电磁场的能量密度，是麦克斯韦方程组的重要推论。"
            },
            "13能量方程": {
                "name": "能量方程",
                "equation": "E = mc²",
                "description": "质量与能量的等价关系",
                "parameters": [
                    {"symbol": "E", "name": "能量", "description": "物体的能量"},
                    {"symbol": "m", "name": "质量", "description": "物体的质量"},
                    {"symbol": "c", "name": "光速", "description": "宇宙中信息传播的最大速度"}
                ],
                "physical_meaning": "爱因斯坦质能方程，揭示了质量和能量的等价关系，是核能利用的理论基础。"
            },
            "14动量能量方程": {
                "name": "动量能量方程",
                "equation": "E² = p²c² + m₀²c⁴",
                "description": "动量与能量的关系",
                "parameters": [
                    {"symbol": "E", "name": "能量", "description": "物体的总能量"},
                    {"symbol": "p", "name": "动量", "description": "物体的动量"},
                    {"symbol": "c", "name": "光速", "description": "宇宙中信息传播的最大速度"},
                    {"symbol": "m₀", "name": "静止质量", "description": "物体静止时的质量"}
                ],
                "physical_meaning": "描述了相对论效应下物体动量与能量的关系，是相对论力学的重要公式。"
            },
            "15时空波动方程": {
                "name": "时空波动方程",
                "equation": "∂²gₐᵦ/∂xᵘ∂xᵛ = Tₐᵦ",
                "description": "时空曲率与能量动量的关系",
                "parameters": [
                    {"symbol": "gₐᵦ", "name": "时空度规", "description": "描述时空曲率的张量"},
                    {"symbol": "∂²/∂xᵘ∂xᵛ", "name": "二阶偏导数", "description": "时空度规的二阶偏导数"},
                    {"symbol": "Tₐᵦ", "name": "能量动量张量", "description": "描述能量动量分布的张量"}
                ],
                "physical_meaning": "爱因斯坦场方程的简化形式，描述了时空曲率与能量动量分布的关系，是广义相对论的核心方程。"
            },
            "16时间的本质方程": {
                "name": "时间的本质方程",
                "equation": "t = ∫ds/c",
                "description": "时间的积分表达",
                "parameters": [
                    {"symbol": "t", "name": "时间", "description": "时间变量"},
                    {"symbol": "∫ds", "name": "积分路径", "description": "沿路径的线积分"},
                    {"symbol": "c", "name": "光速", "description": "宇宙中信息传播的最大速度"}
                ],
                "physical_meaning": "从路径积分的角度描述了时间的本质，揭示了时间与空间的内在联系。"
            },
            "17电荷定义方程": {
                "name": "电荷定义方程",
                "equation": "q = ∫ρ dV",
                "description": "电荷的积分定义",
                "parameters": [
                    {"symbol": "q", "name": "电荷量", "description": "物体的电荷量"},
                    {"symbol": "∫ρ dV", "name": "体积分", "description": "电荷密度的体积分"},
                    {"symbol": "ρ", "name": "电荷密度", "description": "单位体积的电荷量"},
                    {"symbol": "V", "name": "体积", "description": "积分的体积范围"}
                ],
                "physical_meaning": "从电荷密度的角度定义了电荷量，描述了电荷在空间中的分布。"
            }
        }
        
        print("=" * 60)
        print("统一场论公式标准化教科书级别可视化器")
        print(f"基础目录: {self.base_dir}")
        print(f"输出目录: {self.output_dir}")
        print(f"支持 {len(self.formula_info)} 个公式")
        print("=" * 60)
    
    def _create_standard_visualization(self, formula_key: str, info: Dict[str, Any]) -> str:
        """
        为指定公式创建标准化的教科书级别可视化
        """
        try:
            # 创建可视化目录
            formula_output_dir = os.path.join(self.output_dir, formula_key)
            os.makedirs(formula_output_dir, exist_ok=True)
            
            print(f"\n正在处理: {info['name']}")
            
            # 创建2D可视化
            fig_2d = self._create_2d_visualization(info)
            fig_2d_path = os.path.join(formula_output_dir, f"{formula_key}_2D可视化.png")
            fig_2d.savefig(fig_2d_path, dpi=300, bbox_inches='tight')
            plt.close(fig_2d)
            
            # 创建3D可视化（如果适用）
            fig_3d = self._create_3d_visualization(info)
            fig_3d_path = os.path.join(formula_output_dir, f"{formula_key}_3D可视化.png")
            fig_3d.savefig(fig_3d_path, dpi=300, bbox_inches='tight')
            plt.close(fig_3d)
            
            print(f"  ✓ {info['name']} 可视化完成")
            
            return formula_output_dir
            
        except Exception as e:
            print(f"  ✗ {info['name']} 可视化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _create_2d_visualization(self, info: Dict[str, Any]) -> plt.Figure:
        """
        创建标准化的2D可视化
        """
        fig = plt.figure(figsize=(14, 10))
        
        # 添加标题
        plt.title(f"{info['name']}", fontsize=18, fontweight='bold', pad=20)
        
        # 添加公式
        plt.figtext(0.5, 0.02, f"公式: {info['equation']}", ha='center', fontsize=16, 
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # 添加参数解释
        param_text = "参数说明:\n"
        for param in info['parameters']:
            param_text += f"  • {param['symbol']}: {param['name']} - {param['description']}\n"
        
        plt.figtext(0.02, 0.05, param_text, fontsize=12, 
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
                   ha='left', va='bottom')
        
        # 添加物理意义
        plt.figtext(0.5, 0.92, f"物理意义: {info['physical_meaning']}", ha='center', fontsize=14, 
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))
        
        # 根据公式类型创建不同的可视化
        if info['name'] == "时空同一化方程":
            # 时空同一化方程可视化
            t = np.linspace(0, 10, 100)
            c = 3e8  # 光速
            x = c * t
            
            ax = fig.add_subplot(111)
            ax.plot(t, x, 'b-', linewidth=2, label='x = ct')
            ax.set_xlabel('时间 t (s)', fontsize=14)
            ax.set_ylabel('空间距离 x (m)', fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=12)
            
        elif info['name'] == "质量定义方程":
            # 质量定义方程可视化
            omega = np.linspace(0, 4*np.pi, 100)
            k = 1.0
            
            # 空间运动量密度分布
            mu = 2*np.pi
            sigma = np.pi/3
            dn_domega = np.exp(-0.5 * ((omega - mu) / sigma) ** 2) * 10
            mass = k * dn_domega
            
            ax = fig.add_subplot(111)
            ax.plot(omega, mass, 'r-', linewidth=2, label='m = k · dn/dΩ')
            ax.set_xlabel('立体角 Ω (球面度, sr)', fontsize=14)
            ax.set_ylabel('质量 m', fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=12)
            
        else:
            # 默认可视化模板
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"{info['name']} 可视化", ha='center', va='center', fontsize=18)
            ax.axis('off')
        
        plt.tight_layout(rect=[0.15, 0.15, 0.95, 0.85])
        
        return fig
    
    def _create_3d_visualization(self, info: Dict[str, Any]) -> plt.Figure:
        """
        创建标准化的3D可视化
        """
        fig = plt.figure(figsize=(14, 12))
        
        # 添加标题
        plt.title(f"{info['name']} - 3D可视化", fontsize=18, fontweight='bold', pad=20)
        
        # 添加公式
        plt.figtext(0.5, 0.02, f"公式: {info['equation']}", ha='center', fontsize=16, 
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # 根据公式类型创建不同的3D可视化
        if info['name'] == "三维螺旋时空方程":
            # 三维螺旋时空方程可视化
            t = np.linspace(0, 6*np.pi, 200)
            r, w, h = 2, 1, 0.3
            
            x = r * np.cos(w*t)
            y = r * np.sin(w*t)
            z = h * t
            
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(x, y, z, 'b-', linewidth=2.5, label='螺旋轨迹')
            
            # 添加坐标轴标签
            ax.set_xlabel('X轴', fontsize=14)
            ax.set_ylabel('Y轴', fontsize=14)
            ax.set_zlabel('Z轴', fontsize=14)
            
            # 设置视角
            ax.view_init(elev=30, azim=45)
            ax.legend(fontsize=12)
            
        elif info['name'] == "质量定义方程":
            # 质量在空间立体角上的分布
            theta = np.linspace(0, np.pi, 30)
            phi = np.linspace(0, 2*np.pi, 30)
            theta, phi = np.meshgrid(theta, phi)
            
            # 球坐标到直角坐标的转换
            x = np.sin(theta) * np.cos(phi)
            y = np.sin(theta) * np.sin(phi)
            z = np.cos(theta)
            
            # 计算质量分布
            k = 1.0
            omega = np.sqrt(x**2 + y**2 + z**2) * np.pi
            mu = np.pi
            sigma = np.pi/3
            dn_domega = np.exp(-0.5 * ((omega - mu) / sigma) ** 2) * 10
            mass = k * dn_domega
            
            ax = fig.add_subplot(111, projection='3d')
            scatter = ax.scatter(x, y, z, c=mass, cmap='viridis', s=100, alpha=0.7)
            
            # 添加颜色条
            cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
            cbar.set_label('质量 m', fontsize=14)
            
            # 设置坐标轴标签
            ax.set_xlabel('X轴', fontsize=14)
            ax.set_ylabel('Y轴', fontsize=14)
            ax.set_zlabel('Z轴', fontsize=14)
            
            # 设置视角
            ax.view_init(elev=30, azim=45)
            
        else:
            # 默认3D可视化模板
            ax = fig.add_subplot(111, projection='3d')
            ax.text(0.5, 0.5, 0.5, f"{info['name']} 3D可视化", ha='center', va='center', fontsize=18)
            ax.axis('off')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        return fig
    
    def _create_html_report(self):
        """
        创建统一的HTML报告
        """
        print("\n" + "=" * 60)
        print("创建统一的HTML报告")
        print("=" * 60)
        
        # 生成HTML内容
        html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>统一场论核心公式 - 教科书级别可视化</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: "SimHei", "Microsoft YaHei", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 40px;
            font-size: 2.8em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .header-info {
            text-align: center;
            margin-bottom: 40px;
            font-size: 1.2em;
            color: #666;
        }
        
        h2 {
            color: #3498db;
            margin-top: 60px;
            margin-bottom: 30px;
            font-size: 2.2em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }
        
        .formula-section {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            padding: 40px;
            margin-bottom: 50px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .formula-section:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        .formula-title {
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 20px;
            color: #2c3e50;
        }
        
        .formula-equation {
            font-size: 1.6em;
            font-weight: bold;
            text-align: center;
            margin: 30px 0;
            padding: 25px;
            background: linear-gradient(135deg, #e8f4f8 0%, #d4edf7 100%);
            border-radius: 10px;
            border-left: 5px solid #3498db;
            border-right: 5px solid #3498db;
        }
        
        .visualization-container {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            margin: 40px 0;
            justify-content: center;
        }
        
        .visualization-item {
            flex: 1;
            min-width: 500px;
            max-width: 600px;
            border: 1px solid #ddd;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        
        .visualization-item img {
            width: 100%;
            height: auto;
            display: block;
        }
        
        .visualization-caption {
            padding: 20px;
            background-color: #f9f9f9;
            text-align: center;
            font-size: 1.1em;
            font-weight: bold;
            color: #555;
        }
        
        .parameter-explanation {
            background-color: #f8f9fa;
            border-left: 6px solid #3498db;
            padding: 30px;
            margin: 30px 0;
            border-radius: 0 10px 10px 0;
        }
        
        .parameter-explanation h3 {
            margin-bottom: 20px;
            color: #3498db;
            font-size: 1.5em;
        }
        
        .parameter-explanation ul {
            margin-left: 30px;
        }
        
        .parameter-explanation li {
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        
        .parameter-symbol {
            font-weight: bold;
            color: #2c3e50;
            margin-right: 10px;
        }
        
        .parameter-name {
            font-weight: bold;
            color: #3498db;
            margin-right: 10px;
        }
        
        .physical-meaning {
            background: linear-gradient(135deg, #e8f8f5 0%, #d5f5e3 100%);
            border: 2px solid #27ae60;
            border-radius: 10px;
            padding: 30px;
            margin: 30px 0;
        }
        
        .physical-meaning h3 {
            margin-bottom: 20px;
            color: #27ae60;
            font-size: 1.5em;
        }
        
        .physical-meaning p {
            font-size: 1.1em;
            line-height: 1.8;
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>统一场论核心公式 - 教科书级别可视化</h1>
        <div class="header-info">
            <p>标准化的统一场论核心公式可视化，包含2D和3D可视化，详细的参数解释和物理意义说明</p>
        </div>
        
        <div id="formula-content">
        """
        
        # 为每个公式生成HTML内容
        formula_count = 1
        for formula_key, info in self.formula_info.items():
            html_content += f"""
        <div class="formula-section">
            <h2>{formula_count}. {info['name']}</h2>
            <div class="formula-title">{info['description']}</div>
            <div class="formula-equation">{info['equation']}</div>
            
            <div class="parameter-explanation">
                <h3>参数说明</h3>
                <ul>
        """
            
            for param in info['parameters']:
                html_content += f"""
                    <li>
                        <span class="parameter-symbol">{param['symbol']}</span>
                        <span class="parameter-name">{param['name']}</span>
                        <span class="parameter-description">{param['description']}</span>
                    </li>
                """
            
            html_content += f"""
                </ul>
            </div>
            
            <div class="physical-meaning">
                <h3>物理意义</h3>
                <p>{info['physical_meaning']}</p>
            </div>
            
            <div class="visualization-container">
                <div class="visualization-item">
                    <img src="{formula_key}/{formula_key}_2D可视化.png" alt="{info['name']} 2D可视化">
                    <div class="visualization-caption">{info['name']} 2D可视化</div>
                </div>
                <div class="visualization-item">
                    <img src="{formula_key}/{formula_key}_3D可视化.png" alt="{info['name']} 3D可视化">
                    <div class="visualization-caption">{info['name']} 3D可视化</div>
                </div>
            </div>
        </div>
        """
            
            formula_count += 1
        
        # 结束HTML内容
        html_content += f"""
        </div>
    </div>
</body>
</html>
        """
        
        # 保存HTML报告
        html_path = os.path.join(self.output_dir, "standardized_textbook_visualizations.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n统一HTML报告已生成: {html_path}")
    
    def run(self):
        """
        运行可视化器，生成所有公式的教科书级别可视化
        """
        print("开始生成所有公式的标准化教科书级别可视化...")
        
        # 为每个公式创建可视化
        for formula_key, info in self.formula_info.items():
            self._create_standard_visualization(formula_key, info)
        
        # 生成统一的HTML报告
        self._create_html_report()
        
        print("\n" + "=" * 60)
        print("所有可视化生成完成！")
        print(f"输出目录: {self.output_dir}")
        print("=" * 60)

if __name__ == "__main__":
    visualizer = StandardizedTextbookVisualizer()
    visualizer.run()
