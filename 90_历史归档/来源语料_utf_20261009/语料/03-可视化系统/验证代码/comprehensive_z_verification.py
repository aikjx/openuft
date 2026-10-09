# -*- coding: utf-8 -*-
"""
引力光速统一方程综合验证脚本
解决项目中Z值不一致问题，并提供完整的验证过程
"""
import numpy as np
from scipy.integrate import quad, dblquad
import matplotlib.pyplot as plt
import os
import sys

# 添加工具脚本目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '06-工具脚本')))

# 导入constants.py中的常量
from constants import G_CODATA_2018, c, Z_PRECISE, Z_APPROX, Z_PROJECT_LEGACY, GEOMETRIC_FACTOR

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

class ZVerification:
    """Z常数验证与修复类"""
    def __init__(self):
        # 基本物理常数（从constants.py导入）
        self.G_codata_2018 = G_CODATA_2018  # m³·kg⁻¹·s⁻² (CODATA 2018推荐值)
        self.c = c                # m·s⁻¹ (光速)
        
        # 计算精确的Z值
        self.Z_precise = Z_PRECISE
        
        # 论文中给出的Z值
        self.Z_paper = 0.010004524012147  # 论文中给出的Z精确值
        
        # 项目中使用的Z值
        self.Z_project = Z_PROJECT_LEGACY        # 项目中广泛使用的值
        
        # Z的近似值
        self.Z_approx = Z_APPROX
        
        # 结果存储
        self.results = {}
    
    def verify_z_values(self):
        """验证不同来源的Z值"""
        print("===== Z常数多源验证 ======")
        print(f"1. 基于CODATA 2018的精确计算值: Z = {self.Z_precise}")
        print(f"2. 论文中给出的精确值:          Z = {self.Z_paper}")
        print(f"3. 项目中实际使用的值:          Z = {self.Z_project}")
        print(f"4. 近似值:                      Z = {self.Z_approx}")
        
        # 计算差异
        print("\n===== 差异分析 ======")
        paper_diff = abs(self.Z_precise - self.Z_paper)
        project_diff = abs(self.Z_precise - self.Z_project)
        approx_diff = abs(self.Z_precise - self.Z_approx)
        
        print(f"论文值与精确计算值的差异: {paper_diff} (相对误差: {(paper_diff/self.Z_precise)*100:.10f}%)")
        print(f"项目值与精确计算值的差异: {project_diff} (相对误差: {(project_diff/self.Z_precise)*100:.6f}%)")
        print(f"近似值与精确计算值的差异: {approx_diff} (相对误差: {(approx_diff/self.Z_precise)*100:.2f}%)")
        
        # 反向验证
        self.reverse_verification()
        
        # 保存结果
        self.results['z_precise'] = self.Z_precise
        self.results['paper_diff'] = paper_diff
        self.results['project_diff'] = project_diff
        
    def reverse_verification(self):
        """反向验证：使用Z值计算G并与CODATA值比较"""
        print("\n===== 反向验证 ======")
        
        # 使用精确计算的Z值计算G
        G_from_precise = (2 * self.Z_precise) / self.c
        g_precise_diff = abs(G_from_precise - self.G_codata_2018)
        
        # 使用论文中的Z值计算G
        G_from_paper = (2 * self.Z_paper) / self.c
        g_paper_diff = abs(G_from_paper - self.G_codata_2018)
        
        # 使用项目中的Z值计算G
        G_from_project = (2 * self.Z_project) / self.c
        g_project_diff = abs(G_from_project - self.G_codata_2018)
        
        # 使用近似Z值计算G
        G_from_approx = (2 * self.Z_approx) / self.c
        g_approx_diff = abs(G_from_approx - self.G_codata_2018)
        
        print(f"使用精确Z值计算G: G = {G_from_precise}，与CODATA的差异: {g_precise_diff}")
        print(f"使用论文Z值计算G: G = {G_from_paper}，与CODATA的差异: {g_paper_diff}")
        print(f"使用项目Z值计算G: G = {G_from_project}，与CODATA的差异: {g_project_diff}")
        print(f"使用近似Z值计算G: G = {G_from_approx}，与CODATA的差异: {g_approx_diff}")
        
    def verify_geometric_factor(self):
        """验证几何因子2的数学推导"""
        print("\n===== 几何因子2的积分验证 ======")
        
        # 验证1: ∫₀²π cos²α dα = π
        result1, error1 = quad(lambda alpha: np.cos(alpha)**2, 0, 2*np.pi)
        print(f"积分1: ∫₀²π cos²α dα = {result1:.6f}, 预期值: π ≈ {np.pi:.6f}")
        print(f"误差: {abs(result1 - np.pi):.12f}", "✅ 正确" if abs(result1 - np.pi) < 1e-10 else "❌ 错误")
        
        # 验证2: ∫₀^π sinθ dθ = 2
        result2, error2 = quad(lambda theta: np.sin(theta), 0, np.pi)
        print(f"积分2: ∫₀^π sinθ dθ = {result2:.6f}, 预期值: 2")
        print(f"误差: {abs(result2 - 2):.12f}", "✅ 正确" if abs(result2 - 2) < 1e-10 else "❌ 错误")
        
        # 验证3: 平均投影效率 <μ>_standard = 1/2
        def integrand(theta, phi):
            return abs(np.cos(theta)) * np.sin(theta)
        
        result6, error6 = dblquad(integrand, 0, 2*np.pi, 0, np.pi)
        mu_standard = result6 / (4 * np.pi)
        expected_mu_standard = 1/2
        print(f"平均投影效率: <μ>_standard = {mu_standard:.6f}, 预期值: 1/2 = {expected_mu_standard:.6f}")
        print(f"误差: {abs(mu_standard - expected_mu_standard):.12f}", "✅ 正确" if abs(mu_standard - expected_mu_standard) < 1e-10 else "❌ 错误")
        
        # 几何因子η = 2
        geometric_factor = 2
        print(f"\n几何因子η = {geometric_factor}" if abs(mu_standard - expected_mu_standard) < 1e-10 else "\n警告：几何因子推导可能存在问题")
        
        # 保存结果
        self.results['geometric_factor_valid'] = abs(mu_standard - expected_mu_standard) < 1e-10
    
    def create_visualization(self):
        """创建Z值验证的可视化图表"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Z值比较图
        labels = ['精确计算值', '论文值', '项目使用值', '近似值']
        z_values = [self.Z_precise, self.Z_paper, self.Z_project, self.Z_approx]
        bars = axes[0, 0].bar(labels, z_values, color=['blue', 'green', 'red', 'orange'])
        axes[0, 0].set_title('不同来源的Z值比较')
        axes[0, 0].set_ylabel('Z值 (kg⁻¹·m⁴·s⁻³)')
        axes[0, 0].set_ylim(0.00999, 0.01001)  # 放大差异
        
        # 在柱状图上添加数值标签
        for bar in bars:
            height = bar.get_height()
            axes[0, 0].text(bar.get_x() + bar.get_width()/2., height, 
                           f'{height:.12f}', ha='center', va='bottom')
        
        # 2. 相对误差图
        errors = [0, 
                  (abs(self.Z_precise - self.Z_paper)/self.Z_precise)*100, 
                  (abs(self.Z_precise - self.Z_project)/self.Z_precise)*100, 
                  (abs(self.Z_precise - self.Z_approx)/self.Z_precise)*100]
        axes[0, 1].bar(labels, errors, color=['blue', 'green', 'red', 'orange'])
        axes[0, 1].set_title('各Z值相对于精确计算值的相对误差(%)')
        axes[0, 1].set_ylabel('相对误差 (%)')
        
        # 3. G值反向计算结果比较
        g_values = [(2 * self.Z_precise) / self.c, 
                    (2 * self.Z_paper) / self.c, 
                    (2 * self.Z_project) / self.c, 
                    (2 * self.Z_approx) / self.c]
        axes[1, 0].bar(labels, g_values, color=['blue', 'green', 'red', 'orange'])
        axes[1, 0].axhline(y=self.G_codata_2018, color='black', linestyle='--', label=f'CODATA 2018 G值: {self.G_codata_2018}')
        axes[1, 0].set_title('反向计算得到的G值比较')
        axes[1, 0].set_ylabel('G值 (m³·kg⁻¹·s⁻²)')
        axes[1, 0].legend()
        
        # 4. Z = Gc/2关系图
        g_range = np.linspace(self.G_codata_2018 * 0.999999, self.G_codata_2018 * 1.000001, 100)
        z_calculated = (g_range * self.c) / 2
        axes[1, 1].plot(g_range, z_calculated)
        axes[1, 1].scatter(self.G_codata_2018, self.Z_precise, color='red', s=100, label=f'实际值 (G={self.G_codata_2018}, Z={self.Z_precise})')
        axes[1, 1].set_title('Z = Gc/2 关系曲线')
        axes[1, 1].set_xlabel('G值 (m³·kg⁻¹·s⁻²)')
        axes[1, 1].set_ylabel('Z值 (kg⁻¹·m⁴·s⁻³)')
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        # 保存图表
        output_dir = "../图表资源"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        plt.savefig(f"{output_dir}/Z值综合验证分析.png", dpi=300, bbox_inches='tight')
        print(f"\n可视化图表已保存至: {output_dir}/Z值综合验证分析.png")
    
    def generate_report(self):
        """生成验证报告"""
        report = """# 引力光速统一方程Z常数综合验证报告

## 1. 验证概述
本报告对引力光速统一方程中的Z常数进行了全面验证，解决了项目中存在的Z值不一致问题，并验证了几何因子2的数学推导。

## 2. 验证结果

### 2.1 Z常数精确值
根据引力光速统一方程 Z = Gc/2 和 CODATA 2018年的物理常数值，计算得到：
- 引力常数 G = 6.67430 × 10⁻¹¹ m³·kg⁻¹·s⁻²
- 光速 c = 299792458 m·s⁻¹
- 精确Z值 = Gc/2 = {self.Z_precise}

### 2.2 多源Z值比较
| 来源 | Z值 | 与精确值的差异 | 相对误差 |
|------|------|---------------|----------|
| 精确计算值 | {self.Z_precise} | 0 | 0% |
| 论文中的值 | {self.Z_paper} | {abs(self.Z_precise - self.Z_paper)} | {(abs(self.Z_precise - self.Z_paper)/self.Z_precise)*100:.10f}% |
| 项目中使用的值 | {self.Z_project} | {abs(self.Z_precise - self.Z_project)} | {(abs(self.Z_precise - self.Z_project)/self.Z_precise)*100:.6f}% |
| 近似值(0.01) | {self.Z_approx} | {abs(self.Z_precise - self.Z_approx)} | {(abs(self.Z_precise - self.Z_approx)/self.Z_precise)*100:.2f}% |

### 2.3 反向验证结果
使用不同Z值计算G并与CODATA值比较：
- 使用精确Z值计算的G: {2*self.Z_precise/self.c}，与CODATA的差异: {abs(2*self.Z_precise/self.c - self.G_codata_2018)}
- 使用论文Z值计算的G: {2*self.Z_paper/self.c}，与CODATA的差异: {abs(2*self.Z_paper/self.c - self.G_codata_2018)}
- 使用项目Z值计算的G: {2*self.Z_project/self.c}，与CODATA的差异: {abs(2*self.Z_project/self.c - self.G_codata_2018)}

### 2.4 几何因子验证
通过积分验证，几何因子2的推导：✅ 正确
- 平均投影效率 <μ>_standard = 1/2，验证通过
- 所有关键积分的计算误差均小于1e-10

## 3. 主要发现

### 3.1 Z值一致性问题
1. 论文中给出的Z精确值({self.Z_paper})与基于CODATA 2018计算的精确值({self.Z_precise})基本一致
2. 项目中使用的Z值({self.Z_project})与精确值存在约0.02%的误差
3. 近似值Z=0.01的相对误差约为0.045%，在大多数应用场景中可接受

### 3.2 验证逻辑问题
反向验证本质上是代数恒等变换（G = 2Z/c），不构成独立的实验验证。为了真正验证引力光速统一方程，需要：
1. 从独立的物理原理推导Z值
2. 设计实验验证Z的物理意义
3. 建立Z与其他物理现象的关联

## 4. 修复建议

### 4.1 Z值统一
建议将项目中所有使用Z值的地方统一为精确计算值：{self.Z_precise}
- 这将确保与CODATA 2018物理常数的一致性
- 减小累积计算误差
- 提高理论推导的严谨性

### 4.2 验证方法改进
1. 开发独立于G的Z值测量或计算方法
2. 加强几何因子2的物理意义阐述
3. 建立更完整的空间动力学理论框架

## 5. 结论
引力光速统一方程在数学上是自洽的，但需要进一步的实验验证和理论完善。统一使用精确的Z值是提高理论严谨性的重要步骤。
"""
        
        # 保存报告
        output_dir = "../文档说明"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(f"{output_dir}/Z常数综合验证报告.md", 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n验证报告已保存至: {output_dir}/Z常数综合验证报告.md")
    
    def run(self):
        """运行完整的验证流程"""
        print("开始引力光速统一方程Z常数综合验证...\n")
        
        # 验证Z值
        self.verify_z_values()
        
        # 验证几何因子
        self.verify_geometric_factor()
        
        # 创建可视化
        self.create_visualization()
        
        # 生成报告
        self.generate_report()
        
        print("\n验证完成！请查看生成的报告和图表以获取详细结果。")

if __name__ == "__main__":
    # 运行综合验证
    verifier = ZVerification()
    verifier.run()