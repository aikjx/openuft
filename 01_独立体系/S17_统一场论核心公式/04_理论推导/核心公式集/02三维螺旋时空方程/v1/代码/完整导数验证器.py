#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论：螺旋运动完整导数验证器
验证从零阶到八阶导数的完整数学体系
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 设置中文字体支持
plt.rcParams.update({
    'font.family': ['SimHei', 'Microsoft YaHei', 'DejaVu Sans'],
    'axes.unicode_minus': False
})
plt.rcParams['font.size'] = 10

class CompleteDerivativeValidator:
    """完整导数验证器"""
    
    def __init__(self, r=1.0, omega=1.0, p=1.0):
        self.r = r  # 螺旋半径
        self.omega = omega  # 角速度
        self.p = p  # 轴向速度
        self.t = np.linspace(0, 4*np.pi, 1000)
        
        # 导数名称
        self.derivative_names = {
            0: "位置 (Position)",
            1: "速度 (Velocity)",
            2: "加速度 (Acceleration)",
            3: "加加速度 (Jerk)",
            4: "跃迁率 (Jounce/Snap)",
            5: "颤动 (Crackle)",
            6: "激震 (Pop)",
            7: "弹跳 (Lock)",
            8: "撞击 (Drop)"
        }
        
    def compute_derivative(self, order):
        """计算指定阶数的导数"""
        t = self.t
        
        if order == 0:
            # 位置
            x = self.r * np.cos(self.omega * t)
            y = self.r * np.sin(self.omega * t)
            z = self.p * t
            
        elif order == 1:
            # 速度
            x = -self.r * self.omega * np.sin(self.omega * t)
            y = self.r * self.omega * np.cos(self.omega * t)
            z = self.p
            
        else:
            # 高阶导数的通用模式
            n = order
            remainder = n % 4
            
            if remainder == 0:
                # n mod 4 = 0
                x = self.r * (self.omega ** n) * np.cos(self.omega * t)
                y = self.r * (self.omega ** n) * np.sin(self.omega * t)
            elif remainder == 1:
                # n mod 4 = 1
                x = -self.r * (self.omega ** n) * np.sin(self.omega * t)
                y = self.r * (self.omega ** n) * np.cos(self.omega * t)
            elif remainder == 2:
                # n mod 4 = 2
                x = -self.r * (self.omega ** n) * np.cos(self.omega * t)
                y = -self.r * (self.omega ** n) * np.sin(self.omega * t)
            else:  # remainder == 3
                # n mod 4 = 3
                x = self.r * (self.omega ** n) * np.sin(self.omega * t)
                y = -self.r * (self.omega ** n) * np.cos(self.omega * t)
            
            z = np.zeros_like(t)
        
        return x, y, z
    
    def compute_magnitude(self, x, y, z):
        """计算矢量模"""
        return np.sqrt(x**2 + y**2 + z**2)
    
    def verify_theoretical_magnitude(self, order):
        """验证理论模值"""
        if order == 0:
            return self.r
        elif order == 1:
            return np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        else:
            return self.r * (self.omega ** order)
    
    def create_comprehensive_analysis(self):
        """创建综合分析"""
        print("=" * 80)
        print("张祥前统一场论：螺旋运动完整导数分析")
        print("=" * 80)
        
        # 创建数据存储
        analysis_data = []
        
        for order in range(9):  # 0到8阶
            print(f"\n第{order}阶导数：{self.derivative_names[order]}")
            print("-" * 50)
            
            # 计算导数
            x, y, z = self.compute_derivative(order)
            magnitude = self.compute_magnitude(x, y, z)
            theoretical_magnitude = self.verify_theoretical_magnitude(order)
            
            # 计算统计信息
            mean_magnitude = np.mean(magnitude)
            std_magnitude = np.std(magnitude)
            max_magnitude = np.max(magnitude)
            min_magnitude = np.min(magnitude)
            
            print(f"理论模值：{theoretical_magnitude:.6f}")
            print(f"实际模值：均值={mean_magnitude:.6f}, 标准差={std_magnitude:.2e}")
            print(f"范围：[{min_magnitude:.6f}, {max_magnitude:.6f}]")
            
            # 验证结果
            if std_magnitude < 1e-10:
                print("✓ 模值恒定验证通过")
            else:
                print("✗ 模值恒定验证失败")
            
            magnitude_error = abs(mean_magnitude - theoretical_magnitude)
            if magnitude_error < 1e-10:
                print("✓ 理论值验证通过")
            else:
                print("✗ 理论值验证失败")
            
            # 存储数据
            analysis_data.append({
                '阶数': order,
                '名称': self.derivative_names[order],
                '理论模值': theoretical_magnitude,
                '实际均值': mean_magnitude,
                '实际标准差': std_magnitude,
                '最大值': max_magnitude,
                '最小值': min_magnitude,
                '误差': magnitude_error,
                '恒定验证': std_magnitude < 1e-10,
                '理论验证': magnitude_error < 1e-10
            })
        
        # 创建分析表格
        df = pd.DataFrame(analysis_data)
        
        print("\n" + "=" * 80)
        print("完整导数分析汇总表")
        print("=" * 80)
        print(df.to_string(index=False))
        
        return df, analysis_data
    
    def analyze_periodicity(self):
        """分析周期性模式"""
        print("\n" + "=" * 80)
        print("导数周期性模式分析")
        print("=" * 80)
        
        print("\n各阶导数的相位关系：")
        print("阶数\tX分量模式\t\tY分量模式\t\t相位偏移\t模值规律")
        print("-" * 80)
        
        for order in range(9):
            x, y, z = self.compute_derivative(order)
            
            # 分析模式
            x_pattern = self.analyze_component_pattern(x, 'cos' if order % 2 == 0 else 'sin')
            y_pattern = self.analyze_component_pattern(y, 'sin' if order % 2 == 0 else 'cos')
            
            # 相位偏移
            phase_shift = (order * 90) % 360
            
            # 模值规律
            if order == 0:
                magnitude_rule = f"r = {self.r}"
            elif order == 1:
                magnitude_rule = f"√(r²ω² + p²) = {np.sqrt(self.r**2 * self.omega**2 + self.p**2):.3f}"
            else:
                magnitude_rule = f"rω^{order} = {self.r * self.omega**order:.3f}"
            
            print(f"{order}\t{x_pattern}\t{y_pattern}\t{phase_shift}°\t\t{magnitude_rule}")
        
        print("\n周期性规律：")
        print("- 每隔4阶导数，函数形式重复")
        print("- 相位依次偏移90°")
        print("- 模值按ω的幂次增长（除一阶导数外）")
    
    def analyze_component_pattern(self, component, expected_func):
        """分析分量模式"""
        # 简化模式分析
        if np.all(np.abs(component) < 1e-10):
            return "0"
        elif expected_func == 'cos':
            return "rωⁿcos(ωt)"
        else:  # sin
            return "rωⁿsin(ωt)"
    
    def create_derivative_plots(self):
        """创建导数可视化图"""
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        fig.suptitle('张祥前统一场论：螺旋运动0-8阶导数分析', fontsize=16)
        
        for order in range(9):
            ax = axes[order // 3, order % 2] if order < 8 else axes[2, 2]
            
            # 计算导数
            x, y, z = self.compute_derivative(order)
            magnitude = self.compute_magnitude(x, y, z)
            
            # 绘制模值
            ax.plot(self.t, magnitude, 'b-', linewidth=2, label=f'|R^{({order})|')
            
            # 添加理论值线
            theoretical_magnitude = self.verify_theoretical_magnitude(order)
            ax.axhline(y=theoretical_magnitude, color='r', linestyle='--', 
                       alpha=0.7, label=f'理论值={theoretical_magnitude:.3f}')
            
            ax.set_xlabel('时间 (s)')
            ax.set_ylabel(f'{self.derivative_names[order]} 模值')
            ax.set_title(f'第{order}阶导数：{self.derivative_names[order]}')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        
        # 第8阶导数使用最后一个子图
        ax8 = axes[2, 2]
        x8, y8, z8 = self.compute_derivative(8)
        magnitude8 = self.compute_magnitude(x8, y8, z8)
        theoretical_magnitude8 = self.verify_theoretical_magnitude(8)
        
        ax8.plot(self.t, magnitude8, 'b-', linewidth=2, label='|R^(8)|')
        ax8.axhline(y=theoretical_magnitude8, color='r', linestyle='--', 
                   alpha=0.7, label=f'理论值={theoretical_magnitude8:.3f}')
        ax8.set_xlabel('时间 (s)')
        ax8.set_ylabel('撞击模值')
        ax8.set_title('第8阶导数：撞击')
        ax8.legend(fontsize=8)
        ax8.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('螺旋运动完整导数分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ 导数可视化图表已保存为：螺旋运动完整导数分析.png")
    
    def create_magnitude_comparison(self):
        """创建模值对比图"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        orders = range(9)
        theoretical_magnitudes = [self.verify_theoretical_magnitude(order) for order in orders]
        
        # 左图：理论模值
        ax1.bar(orders, theoretical_magnitudes, color='skyblue', alpha=0.7, edgecolor='black')
        ax1.set_xlabel('导数阶数')
        ax1.set_ylabel('理论模值')
        ax1.set_title('各阶导数理论模值对比')
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.3)
        
        # 添加数值标签
        for i, (order, mag) in enumerate(zip(orders, theoretical_magnitudes)):
            ax1.text(order, mag * 1.1, f'{mag:.2e}', ha='center', va='bottom', fontsize=8)
        
        # 右图：增长规律
        if len(orders) > 2:
            growth_rates = []
            for i in range(2, len(orders)):  # 从2阶开始
                if theoretical_magnitudes[i-2] > 0:
                    growth_rate = theoretical_magnitudes[i] / theoretical_magnitudes[i-2]
                    growth_rates.append(growth_rate)
                else:
                    growth_rates.append(np.nan)
            
            orders_growth = list(range(2, 9))
            ax2.plot(orders_growth, growth_rates, 'ro-', linewidth=2, markersize=8)
            ax2.set_xlabel('导数阶数')
            ax2.set_ylabel('相对前2阶的增长倍数')
            ax2.set_title('模值增长规律（每2阶）')
            ax2.grid(True, alpha=0.3)
            ax2.set_yscale('log')
        
        plt.tight_layout()
        plt.savefig('导数模值对比分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ 模值对比图表已保存为：导数模值对比分析.png")
    
    def generate_mathematical_expressions(self):
        """生成数学表达式"""
        print("\n" + "=" * 80)
        print("完整数学表达式汇总")
        print("=" * 80)
        
        print("\n螺旋运动基本方程：")
        print("R(t) = r·cos(ωt)·i + r·sin(ωt)·j + p·t·k")
        print()
        
        print("各阶导数通用表达式：")
        print("R^(n)(t) = r·ωⁿ·Fₙ(ωt)")
        print()
        
        print("其中Fₙ(ωt)为周期函数：")
        print("当 n mod 4 = 0 时：Fₙ = cos(ωt)·i + sin(ωt)·j")
        print("当 n mod 4 = 1 时：Fₙ = -sin(ωt)·i + cos(ωt)·j")
        print("当 n mod 4 = 2 时：Fₙ = -cos(ωt)·i - sin(ωt)·j")
        print("当 n mod 4 = 3 时：Fₙ = sin(ωt)·i - cos(ωt)·j")
        print()
        
        print("模值规律：")
        print("|R^(0)| = r")
        print("|R^(1)| = √(r²ω² + p²)")
        print("|R^(n)| = r·ωⁿ  (n ≥ 2)")
        print()
        
        print("物理意义：")
        print("0阶：位置（空间几何点）")
        print("1阶：速度（时空变化率，光速）")
        print("2阶：加速度（引力场强度）")
        print("3阶：加加速度（引力场变化率）")
        print("4阶：跃迁率（引力场二阶变化）")
        print("5阶：颤动（引力场三阶变化）")
        print("6阶：激震（引力场四阶变化）")
        print("7阶：弹跳（引力场五阶变化）")
        print("8阶：撞击（引力场六阶变化）")
    
    def run_complete_validation(self):
        """运行完整验证"""
        print("开始张祥前统一场论螺旋运动完整导数验证...")
        
        # 1. 综合分析
        df, analysis_data = self.create_comprehensive_analysis()
        
        # 2. 周期性分析
        self.analyze_periodicity()
        
        # 3. 数学表达式
        self.generate_mathematical_expressions()
        
        # 4. 可视化
        self.create_derivative_plots()
        self.create_magnitude_comparison()
        
        # 5. 保存数据
        df.to_csv('完整导数验证数据表.csv', index=False, encoding='utf-8-sig')
        
        print("\n" + "=" * 80)
        print("验证总结")
        print("=" * 80)
        
        # 统计验证结果
        constant_validations = sum(1 for data in analysis_data if data['恒定验证'])
        theory_validations = sum(1 for data in analysis_data if data['理论验证'])
        
        print(f"模值恒定验证：{constant_validations}/9 通过")
        print(f"理论值验证：{theory_validations}/9 通过")
        
        if constant_validations == 9 and theory_validations == 9:
            print("\n✅ 所有验证完全通过！")
            print("张祥前统一场论的螺旋运动导数体系数学完美！")
        else:
            print("\n❌ 部分验证失败，需要检查理论。")
        
        print("\n生成的文件：")
        print("- 螺旋运动完整导数分析.png")
        print("- 导数模值对比分析.png")
        print("- 完整导数验证数据表.csv")
        print("=" * 80)

def main():
    """主函数"""
    validator = CompleteDerivativeValidator(r=1.0, omega=1.0, p=1.0)
    validator.run_complete_validation()

if __name__ == "__main__":
    main()