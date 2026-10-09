import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False

class GeometricFactorVerification:
    """几何因子详细验证类"""
    
    def __init__(self):
        """初始化"""
        self.c = 299792458  # 光速，单位：m/s
        self.G_codata = 6.67430e-11  # CODATA 2018 万有引力常数
    
    def calculate_hemisphere_projection(self):
        """重新计算半球面上的平均投影效率"""
        print("=== 半球面平均投影效率计算 ===")
        
        # 方法1：使用球面坐标积分（正确的三维计算）
        def projection_integrand(theta, phi):
            # theta: 极角 (0到π)
            # phi: 方位角 (0到2π)
            # 投影效率为 cos(theta)，因为我们考虑的是相对于某个方向的投影
            return np.cos(theta) * np.sin(theta)  # sin(theta) 是球面坐标的雅可比行列式因子
        
        # 在半球面上积分 (theta从0到π/2，phi从0到2π)
        result_3d, error_3d = integrate.dblquad(
            projection_integrand,
            0, 2*np.pi,  # phi的范围
            lambda phi: 0, lambda phi: np.pi/2  # theta的范围
        )
        
        # 半球面的面积元素积分结果应该是 2π
        hemisphere_area = 2 * np.pi
        
        # 平均投影效率 = 积分结果 / 半球面面积
        avg_projection_3d = result_3d / hemisphere_area
        
        print(f"三维半球面积分结果: {result_3d:.10f}")
        print(f"半球面面积: {hemisphere_area:.10f}")
        print(f"三维平均投影效率: {avg_projection_3d:.10f}")
        print(f"理论值 (1/2): {0.5:.10f}")
        print(f"误差: {abs(avg_projection_3d - 0.5) / 0.5 * 100:.10f}%")
        print()
        
        # 方法2：使用一维极角积分（考虑对称性）
        def theta_integrand(theta):
            return np.cos(theta) * 2 * np.pi * np.sin(theta)  # 2πsin(theta)dtheta 是球壳面积元素
        
        result_1d, error_1d = integrate.quad(theta_integrand, 0, np.pi/2)
        avg_projection_1d = result_1d / hemisphere_area
        
        print(f"一维极角积分结果: {result_1d:.10f}")
        print(f"一维平均投影效率: {avg_projection_1d:.10f}")
        print(f"理论值 (1/2): {0.5:.10f}")
        print(f"误差: {abs(avg_projection_1d - 0.5) / 0.5 * 100:.10f}%")
        print()
        
        # 计算几何因子
        geometric_factor_3d = 1 / avg_projection_3d
        geometric_factor_1d = 1 / avg_projection_1d
        
        print(f"三维几何因子 (1/平均投影效率): {geometric_factor_3d:.10f}")
        print(f"一维几何因子 (1/平均投影效率): {geometric_factor_1d:.10f}")
        print(f"预期几何因子: {2.0:.10f}")
        print(f"三维计算误差: {abs(geometric_factor_3d - 2.0) / 2.0 * 100:.10f}%")
        print(f"一维计算误差: {abs(geometric_factor_1d - 2.0) / 2.0 * 100:.10f}%")
        
        return avg_projection_3d, geometric_factor_3d
    
    def analyze_previous_result(self):
        """分析之前计算结果的问题"""
        print("\n=== 之前计算结果分析 ===")
        
        # 之前的结果
        prev_avg_efficiency = 0.636620  # 从终端输出获取
        prev_geometric_factor = 1.570796  # 从终端输出获取
        
        print(f"之前计算的平均投影效率: {prev_avg_efficiency:.10f}")
        print(f"之前计算的几何因子: {prev_geometric_factor:.10f}")
        print(f"注意：这个值等于 π/2 ≈ {np.pi/2:.10f}")
        print(f"与预期几何因子2.0的误差: {abs(prev_geometric_factor - 2.0) / 2.0 * 100:.10f}%")
        print()
        
        # 分析问题原因
        print("问题分析:")
        print("1. 之前的计算可能只在0到π/2的角度范围内积分，没有正确考虑球面坐标的权重因子")
        print("2. 正确的半球面平均投影效率应该是1/2，几何因子应该是2.0")
        print("3. 这是因为在半球面上，各个方向的权重应该由球面坐标的雅可比行列式决定")
        print()
        
        # 验证G=2Z/c方程
        print("=== G=2Z/c方程验证 ===")
        
        # 使用正确的几何因子2.0计算
        Z_correct = (self.G_codata * self.c) / 2
        G_calculated = (2 * Z_correct) / self.c
        
        print(f"使用几何因子2.0:")
        print(f"Z常量 = (G * c) / 2 = ({self.G_codata:.10e} * {self.c}) / 2 = {Z_correct:.10e}")
        print(f"计算G值 = 2Z/c = 2 * {Z_correct:.10e} / {self.c} = {G_calculated:.10e}")
        print(f"与CODATA值的误差: {abs(G_calculated - self.G_codata) / self.G_codata * 100:.10f}%")
        print()
        
        # 使用之前的几何因子计算
        Z_incorrect = (self.G_codata * self.c) / prev_geometric_factor
        G_incorrect = (prev_geometric_factor * Z_incorrect) / self.c
        
        print(f"使用几何因子{prev_geometric_factor:.10f}:")
        print(f"Z常量 = (G * c) / 几何因子 = ({self.G_codata:.10e} * {self.c}) / {prev_geometric_factor:.10f} = {Z_incorrect:.10e}")
        print(f"计算G值 = 几何因子 * Z/c = {prev_geometric_factor:.10f} * {Z_incorrect:.10e} / {self.c} = {G_incorrect:.10e}")
        print(f"与CODATA值的误差: {abs(G_incorrect - self.G_codata) / self.G_codata * 100:.10f}%")
    
    def visualize_projection(self):
        """可视化投影效率分布"""
        plt.figure(figsize=(12, 8))
        
        # 生成极角数据
        theta = np.linspace(0, np.pi/2, 100)
        
        # 投影效率
        projection = np.cos(theta)
        
        # 球面权重因子
        weight = np.sin(theta)
        
        # 加权投影效率
        weighted_projection = projection * weight
        
        plt.subplot(2, 1, 1)
        plt.plot(theta, projection, 'b-', linewidth=2, label='投影效率 cos(θ)')
        plt.plot(theta, weight, 'g--', linewidth=2, label='权重因子 sin(θ)')
        plt.axhline(y=0.5, color='r', linestyle='-.', label='正确平均投影效率: 0.5')
        plt.axhline(y=0.63662, color='m', linestyle=':', label='之前计算的平均投影效率: 0.63662')
        plt.xlabel('极角 θ (弧度)')
        plt.ylabel('效率/权重')
        plt.title('投影效率与权重因子分布')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.subplot(2, 1, 2)
        plt.plot(theta, weighted_projection, 'r-', linewidth=2, label='加权投影效率 cos(θ)sin(θ)')
        plt.fill_between(theta, weighted_projection, alpha=0.3, color='red')
        plt.axhline(y=0.25, color='g', linestyle='--', label='加权平均: 0.25')
        plt.xlabel('极角 θ (弧度)')
        plt.ylabel('加权投影效率')
        plt.title('加权投影效率分布（用于半球面积分）')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('几何因子详细分析.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_thesis_impact_analysis(self):
        """生成对论文影响的分析"""
        print("\n=== 对论文的影响分析 ===")
        print("1. 问题严重性: 几何因子是引力光速统一方程G=2Z/c的核心理论基础之一")
        print()
        print("2. 影响评估:")
        print("   - 方程形式: 如果几何因子不是2.0，方程形式需要修正为 G=kZ/c，其中k为正确的几何因子")
        print("   - 物理意义: Z常量的物理意义将发生变化")
        print("   - 理论一致性: 需要重新验证与统一场论其他方程的一致性")
        print()
        print("3. 修正建议:")
        print("   - 重新计算半球面平均投影效率，确保正确应用球面坐标权重")
        print("   - 验证几何因子是否确实为2.0，这是方程G=2Z/c成立的关键")
        print("   - 如果几何因子确实为2.0，则之前的计算存在错误，需要修正")
        print("   - 如果几何因子不是2.0，则需要调整方程形式并重新推导")
        print()
        print("4. 结论:")
        print("   - 几何因子的准确值对论文的核心结论至关重要")
        print("   - 需要通过严格的数学推导和数值计算来确定正确的几何因子")
        print("   - 建议进行多种方法的交叉验证，确保结果的准确性")

def main():
    """主函数"""
    verifier = GeometricFactorVerification()
    
    # 重新计算平均投影效率和几何因子
    avg_efficiency, geometric_factor = verifier.calculate_hemisphere_projection()
    
    # 分析之前的计算结果
    verifier.analyze_previous_result()
    
    # 生成可视化
    verifier.visualize_projection()
    
    # 分析对论文的影响
    verifier.generate_thesis_impact_analysis()

if __name__ == "__main__":
    main()
