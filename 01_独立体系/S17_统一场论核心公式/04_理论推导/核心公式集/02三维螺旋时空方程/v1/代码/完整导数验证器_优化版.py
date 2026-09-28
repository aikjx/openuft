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

class CompleteDerivativeValidator:
    """完整导数验证器"""
    
    def __init__(self, r=1.0, omega=1.0, p=1.0):
        self.r = r          # 螺旋半径
        self.omega = omega  # 角速度
        self.p = p          # 轴向速度
        self.t = np.linspace(0, 4*np.pi, 1000)
        
        # 导数名称
        self.derivative_names = {
            0: "Position",
            1: "Velocity", 
            2: "Acceleration",
            3: "Jerk",
            4: "Jounce/Snap",
            5: "Crackle",
            6: "Pop",
            7: "Lock",
            8: "Drop"
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
                x = self.r * (self.omega ** n) * np.cos(self.omega * t)
                y = self.r * (self.omega ** n) * np.sin(self.omega * t)
            elif remainder == 1:
                x = -self.r * (self.omega ** n) * np.sin(self.omega * t)
                y = self.r * (self.omega ** n) * np.cos(self.omega * t)
            elif remainder == 2:
                x = -self.r * (self.omega ** n) * np.cos(self.omega * t)
                y = -self.r * (self.omega ** n) * np.sin(self.omega * t)
            else:  # remainder == 3
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
        print("Complete Derivative Analysis: Helical Motion")
        print("=" * 80)
        
        analysis_data = []
        
        for order in range(9):  # 0到8阶
            print(f"\nOrder {order}: {self.derivative_names[order]}")
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
            
            print(f"Theoretical magnitude: {theoretical_magnitude:.6f}")
            print(f"Actual magnitude: mean={mean_magnitude:.6f}, std={std_magnitude:.2e}")
            print(f"Range: [{min_magnitude:.6f}, {max_magnitude:.6f}]")
            
            # 验证结果
            if std_magnitude < 1e-10:
                print("✓ Constant magnitude verified")
            else:
                print("✗ Constant magnitude failed")
            
            magnitude_error = abs(mean_magnitude - theoretical_magnitude)
            if magnitude_error < 1e-10:
                print("✓ Theoretical value verified")
            else:
                print("✗ Theoretical value failed")
            
            # 存储数据
            analysis_data.append({
                'Order': order,
                'Name': self.derivative_names[order],
                'Theoretical_Mag': theoretical_magnitude,
                'Actual_Mean': mean_magnitude,
                'Actual_Std': std_magnitude,
                'Max_Value': max_magnitude,
                'Min_Value': min_magnitude,
                'Error': magnitude_error,
                'Constant_Verified': std_magnitude < 1e-10,
                'Theory_Verified': magnitude_error < 1e-10
            })
        
        # 创建分析表格
        df = pd.DataFrame(analysis_data)
        
        print("\n" + "=" * 80)
        print("Complete Derivative Analysis Summary")
        print("=" * 80)
        print(df.to_string(index=False))
        
        return df, analysis_data
    
    def analyze_periodicity(self):
        """分析周期性模式"""
        print("\n" + "=" * 80)
        print("Periodicity Pattern Analysis")
        print("=" * 80)
        
        print("\nPhase relationships of each derivative:")
        print("Order\tX Pattern\t\tY Pattern\t\tPhase Shift\tMagnitude Rule")
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
        
        print("\nPeriodicity patterns:")
        print("- Function form repeats every 4 derivatives")
        print("- Phase shifts by 90° sequentially")
        print("- Magnitude grows by powers of ω (except 1st order)")
    
    def analyze_component_pattern(self, component, expected_func):
        """分析分量模式"""
        if np.all(np.abs(component) < 1e-10):
            return "0"
        elif expected_func == 'cos':
            return "rωⁿcos(ωt)"
        else:  # sin
            return "rωⁿsin(ωt)"
    
    def create_derivative_plots(self):
        """创建导数可视化图"""
        fig = plt.figure(figsize=(18, 12))
        fig.suptitle('Complete Derivative Analysis: Helical Motion (0-8 Orders)', fontsize=16, fontweight='bold')
        
        # 创建3x3网格
        for order in range(9):
            ax = fig.add_subplot(3, 3, order + 1)
            
            # 计算导数
            x, y, z = self.compute_derivative(order)
            magnitude = self.compute_magnitude(x, y, z)
            
            # 绘制模值
            ax.plot(self.t, magnitude, 'b-', linewidth=2.5, label=f'|R^({order})|')
            
            # 添加理论值线
            theoretical_magnitude = self.verify_theoretical_magnitude(order)
            ax.axhline(y=theoretical_magnitude, color='r', linestyle='--', 
                      alpha=0.8, linewidth=1.5, label=f'Theory={theoretical_magnitude:.3f}')
            
            ax.set_xlabel('Time (s)', fontsize=9)
            ax.set_ylabel(f'{self.derivative_names[order]} Magnitude', fontsize=9)
            ax.set_title(f'Order {order}: {self.derivative_names[order]}', fontsize=10, fontweight='bold')
            ax.legend(fontsize=7, loc='upper right')
            ax.grid(True, alpha=0.3)
            ax.tick_params(labelsize=8)
        
        plt.tight_layout()
        plt.savefig('Complete_Derivative_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Derivative visualization saved: Complete_Derivative_Analysis.png")
    
    def create_magnitude_comparison(self):
        """创建模值对比图"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        orders = range(9)
        theoretical_magnitudes = [self.verify_theoretical_magnitude(order) for order in orders]
        
        # 左图：理论模值
        bars = ax1.bar(orders, theoretical_magnitudes, color='skyblue', alpha=0.8, 
                      edgecolor='navy', linewidth=1.5)
        ax1.set_xlabel('Derivative Order', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Theoretical Magnitude', fontsize=12, fontweight='bold')
        ax1.set_title('Theoretical Magnitude Comparison', fontsize=14, fontweight='bold')
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 添加数值标签
        for i, (order, mag, bar) in enumerate(zip(orders, theoretical_magnitudes, bars)):
            if mag > 0:
                ax1.text(order, mag * 1.2, f'{mag:.2e}', ha='center', va='bottom', 
                       fontsize=8, fontweight='bold')
        
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
            ax2.plot(orders_growth, growth_rates, 'ro-', linewidth=2.5, markersize=8, 
                     markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=2)
            ax2.set_xlabel('Derivative Order', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Growth Factor (vs 2 orders before)', fontsize=12, fontweight='bold')
            ax2.set_title('Magnitude Growth Pattern', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.set_yscale('log')
            
            # 添加增长因子标注
            for i, (order, rate) in enumerate(zip(orders_growth, growth_rates)):
                if not np.isnan(rate):
                    ax2.annotate(f'{rate:.1f}x', (order, rate), 
                               xytext=(order, rate*1.3), fontsize=8, 
                               ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('Magnitude_Comparison_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Magnitude comparison saved: Magnitude_Comparison_Analysis.png")
    
    def generate_mathematical_expressions(self):
        """生成数学表达式"""
        print("\n" + "=" * 80)
        print("Complete Mathematical Expressions")
        print("=" * 80)
        
        print("\nBasic Helical Motion Equation:")
        print("R(t) = r·cos(ωt)·i + r·sin(ωt)·j + p·t·k")
        print()
        
        print("General Derivative Expression:")
        print("R^(n)(t) = r·ωⁿ·Fₙ(ωt)")
        print()
        
        print("Where Fₙ(ωt) are periodic functions:")
        print("When n mod 4 = 0: Fₙ = cos(ωt)·i + sin(ωt)·j")
        print("When n mod 4 = 1: Fₙ = -sin(ωt)·i + cos(ωt)·j")
        print("When n mod 4 = 2: Fₙ = -cos(ωt)·i - sin(ωt)·j")
        print("When n mod 4 = 3: Fₙ = sin(ωt)·i - cos(ωt)·j")
        print()
        
        print("Magnitude Patterns:")
        print("|R^(0)| = r")
        print("|R^(1)| = √(r²ω² + p²)")
        print("|R^(n)| = r·ωⁿ  (n ≥ 2)")
        print()
        
        print("Physical Significance:")
        print("0th: Position (spatial geometric point)")
        print("1st: Velocity (spacetime change rate, speed of light)")
        print("2nd: Acceleration (gravitational field strength)")
        print("3rd: Jerk (gravitational field change rate)")
        print("4th: Jounce/Snap (second-order change)")
        print("5th: Crackle (third-order change)")
        print("6th: Pop (fourth-order change)")
        print("7th: Lock (fifth-order change)")
        print("8th: Drop (sixth-order change)")
    
    def run_complete_validation(self):
        """运行完整验证"""
        print("Starting complete derivative validation for helical motion...")
        
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
        df.to_csv('Complete_Derivative_Validation_Data.csv', index=False, encoding='utf-8-sig')
        
        print("\n" + "=" * 80)
        print("Validation Summary")
        print("=" * 80)
        
        # 统计验证结果
        constant_validations = sum(1 for data in analysis_data if data['Constant_Verified'])
        theory_validations = sum(1 for data in analysis_data if data['Theory_Verified'])
        
        print(f"Constant magnitude verification: {constant_validations}/9 passed")
        print(f"Theoretical value verification: {theory_validations}/9 passed")
        
        if constant_validations == 9 and theory_validations == 9:
            print("\n✅ All verifications passed!")
            print("The helical motion derivative system is mathematically perfect!")
        else:
            print("\n❌ Some verifications failed, theory needs review.")
        
        print("\nGenerated files:")
        print("- Complete_Derivative_Analysis.png")
        print("- Magnitude_Comparison_Analysis.png")
        print("- Complete_Derivative_Validation_Data.csv")
        print("=" * 80)

def main():
    """主函数"""
    validator = CompleteDerivativeValidator(r=1.0, omega=1.0, p=1.0)
    validator.run_complete_validation()

if __name__ == "__main__":
    main()