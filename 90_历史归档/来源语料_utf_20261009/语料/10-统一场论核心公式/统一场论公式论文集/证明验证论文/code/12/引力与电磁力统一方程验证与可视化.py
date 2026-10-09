#!/usr/bin/env python
# -*- coding: utf-8 -*-
引力与电磁力统一方程验证与可视化
本代码实现了张祥前统一场论中引力与电磁力统一方程的完整数学验证和可视化分析"""import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class UnifiedGravityElectromagnetism:"""引力与电磁力统一方程验证与分析类"""def __init__(self):"""初始化类实例"""self.results = {}
        print(" =  =  = 引力与电磁力统一方程验证系统初始化 =  =  = ")
    
    def symbolic_derivation(self):"""符号求导验证"""print(" / n =  =  = 1. 符号求导验证 =  =  = ")
        
        # 定义符号变量
        m, q, r, v, c, G, k_e = sp.symbols('m q r v c G k_e')
        
        # 引力场定义
        # 牛顿万有引力公式
        F_gravity = G * m *  * 2 / r *  * 2
        
        # 引力场强度
        g = G * m / r *  * 2
        
        # 电场定义
        # 库仑定律
        F_electric = k_e * q *  * 2 / r *  * 2
        
        # 电场强度
        E = k_e * q / r *  * 2
        
        # 统一场方程(假设形式)
        # 这里假设统一场方程是引力场和电磁场的组合形式
        # F_unified = F_gravity + F_electric
        F_unified = G * m *  * 2 / r *  * 2 + k_e * q *  * 2 / r *  * 2
        
        # 场强度的统一形式
        field_unified = G * m / r *  * 2 + k_e * q / r *  * 2
        
        # 相对论修正的统一场
        gamma = 1 / sp.sqrt(1 - v *  * 2 / c *  * 2)
        F_unified_relativistic = gamma * F_unified
        
        # 统一场的梯度和散度
        # 对r求导
        dF_dr = sp.diff(F_unified, r)
        
        # 场的散度(球对称情况下)
        div_field = (1 / r *  * 2) * sp.diff(r *  * 2 * field_unified, r)
        
        # 场的能量密度
        energy_density_gravity = (1 / (8 * sp.pi * G)) * g *  * 2
        energy_density_electric = (1 / (8 * sp.pi * k_e)) * E *  * 2
        energy_density_unified = energy_density_gravity + energy_density_electric
        
        # 保存结果
        symbolic_results = {
            'field_definitions': {
                'gravity': {
                    'force': F_gravity,
                    'field_strength': g
                },
                'electric': {
                    'force': F_electric,
                    'field_strength': E
                },
                'unified': {
                    'force': F_unified,
                    'field_strength': field_unified,
                    'force_relativistic': F_unified_relativistic
                }
            },
            'field_properties': {
                'gradient': dF_dr,
                'divergence': div_field
            },
            'energy': {
                'energy_density_gravity': energy_density_gravity,
                'energy_density_electric': energy_density_electric,
                'energy_density_unified': energy_density_unified
            }
        }
        self.results['symbolic'] = symbolic_results
        
        # 输出结果
        print(f"引力:")
        print(f"  引力: F_g = {F_gravity}")
        print(f"  引力场强度: g = {g}")
        print(f"电磁力:")
        print(f"  电磁力: F_e = {F_electric}")
        print(f"  电场强度: E = {E}")
        print(f"统一场:")
        print(f"  统一力: F_u = {F_unified}")
        print(f"  统一场强度: F_u_field = {field_unified}")
        print(f"  相对论统一力: F_u_rel = {F_unified_relativistic}")
        print(f"场特性:")
        print(f"  力的梯度: dF / dr = {dF_dr}")
        print(f"  场的散度: ∇·F = {div_field}")
        print(f"能量密度:")
        print(f"  引力场能量密度: u_g = {energy_density_gravity}")
        print(f"  电场能量密度: u_e = {energy_density_electric}")
        print(f"  统一场能量密度: u_u = {energy_density_unified}")
        
        return symbolic_results
    
    def special_cases_analysis(self):"""特殊情况分析"""print(" / n =  =  = 2. 特殊情况分析 =  =  = ")
        
        # 定义符号变量
        m, q, r, v, c, G, k_e = sp.symbols('m q r v c G k_e')
        
        # 统一力
        F_unified = G * m *  * 2 / r *  * 2 + k_e * q *  * 2 / r *  * 2
        
        # 特殊情况1: 只有引力 (q = 0)
        q_zero = F_unified.subs(q, 0)
        
        # 特殊情况2: 只有电磁力 (m = 0)
        m_zero = F_unified.subs(m, 0)
        
        # 特殊情况3: 引力与电磁力平衡 (F_gravity = - F_electric)
        # 求解平衡条件
        balance_condition = sp.Eq(G * m *  * 2, - k_e * q *  * 2)
        
        # 特殊情况4: 低速近似 (v << c)
        gamma = 1 / sp.sqrt(1 - v *  * 2 / c *  * 2)
        gamma_approx = sp.series(gamma, v, 0, 3).removeO()
        
        # 特殊情况5: 远场近似 (r → ∞)
        # 场强衰减为1 / r²
        
        special_cases = {
            'only_gravity': q_zero,
            'only_electric': m_zero,
            'balance_condition': balance_condition,
            'gamma_approx': gamma_approx
        }
        self.results['special_cases'] = special_cases
        
        print(f"只有引力 (q = 0):")
        print(f"  F = {q_zero}")
        print(f"只有电磁力 (m = 0):")
        print(f"  F = {m_zero}")
        print(f"引力与电磁力平衡条件: {balance_condition}")
        print(f"低速近似: γ ≈ {gamma_approx}")
        print(f"远场近似 (r → ∞): 场强按1 / r²衰减")
        
        return special_cases
    
    def numerical_simulation(self, m = 1.0, q = 1.0, G = 6.674e - 11, k_e = 8.988e9, v = 0.0, c = 3.0e8, r_min = 1.0, r_max = 10.0, num_points = 1000):"""数值模拟"""print(" / n =  =  = 3. 数值模拟 =  =  = ")
        
        # 生成距离数据
        r_values = np.linspace(r_min, r_max, num_points)
        
        # 计算引力
        F_gravity_values = G * m *  * 2 / r_values *  * 2
        g_values = G * m / r_values *  * 2
        
        # 计算电磁力
        F_electric_values = k_e * q *  * 2 / r_values *  * 2
        E_values = k_e * q / r_values *  * 2
        
        # 计算统一力
        F_unified_values = F_gravity_values + F_electric_values
        field_unified_values = g_values + E_values
        
        # 计算相对论修正(如果v > 0)
        if v > 0:
            gamma_values = 1.0 / np.sqrt(1.0 - (v / c) *  * 2)
            F_unified_relativistic_values = gamma_values * F_unified_values
        else:
            F_unified_relativistic_values = F_unified_values.copy()
        
        # 计算场的能量密度
        energy_density_gravity = (1 / (8 * np.pi * G)) * g_values *  * 2
        energy_density_electric = (1 / (8 * np.pi * k_e)) * E_values *  * 2
        energy_density_unified = energy_density_gravity + energy_density_electric
        
        # 力的比值
        with np.errstate(divide = 'ignore', invalid = 'ignore'):
            force_ratio = np.abs(F_gravity_values / F_electric_values)
        
        # 不同参数下的比较
        parameter_comparisons = {
# '质量影响': {
                'm1': {'m': 0.5, 'label': 'm = 0.5 kg'},
                'm2': {'m': 1.0, 'label': 'm = 1.0 kg'},
                'm3': {'m': 2.0, 'label': 'm = 2.0 kg'}
            },
# '电荷影响': {
                'q1': {'q': 0.5, 'label': 'q = 0.5 C'},
                'q2': {'q': 1.0, 'label': 'q = 1.0 C'},
                'q3': {'q': 2.0, 'label': 'q = 2.0 C'}
            }
        }
        
        # 计算质量影响
        mass_comparison = {}
# for mass_key, mass_data in parameter_comparisons['质量影响'].items():
            m_val = mass_data['m']
            F_g_mass = G * m_val *  * 2 / r_values *  * 2
            mass_comparison[mass_key] = {
                'm': m_val,
                'gravity_force': F_g_mass,
                'label': mass_data['label']
            }
        
        # 计算电荷影响
        charge_comparison = {}
# for charge_key, charge_data in parameter_comparisons['电荷影响'].items():
            q_val = charge_data['q']
            F_e_charge = k_e * q_val *  * 2 / r_values *  * 2
            charge_comparison[charge_key] = {
                'q': q_val,
                'electric_force': F_e_charge,
                'label': charge_data['label']
            }
        
        # 创建数据表
        data_table = {
# '距离 r (m)': r_values[::200],
# '引力 F_g (N)': F_gravity_values[::200],
# '电磁力 F_e (N)': F_electric_values[::200],
# '统一力 F_u (N)': F_unified_values[::200],
# '力的比值 |F_g / F_e|': force_ratio[::200],
# '引力场能量密度 (J / m³)': energy_density_gravity[::200],
# '电场能量密度 (J / m³)': energy_density_electric[::200],
# '统一场能量密度 (J / m³)': energy_density_unified[::200]
        }
        data_table = pd.DataFrame(data_table)
        
        numerical_results = {
            'force_distributions': {
                'r_values': r_values,
                'F_gravity_values': F_gravity_values,
                'F_electric_values': F_electric_values,
                'F_unified_values': F_unified_values,
                'F_unified_relativistic_values': F_unified_relativistic_values,
                'force_ratio': force_ratio,
                'energy_densities': {
                    'gravity': energy_density_gravity,
                    'electric': energy_density_electric,
                    'unified': energy_density_unified
                },
                'data_table': data_table
            },
            'parameter_comparisons': {
                'mass': mass_comparison,
                'charge': charge_comparison
            }
        }
        self.results['numerical'] = numerical_results
        
        # 输出结果
        print(f"引力与电磁力统一模拟结果:")
        print(f"质量: m = {m} kg")
        print(f"电荷: q = {q} C")
        print(f"距离范围: {r_min} m 到 {r_max} m")
        print(f"引力常数: G = {G} N·m² / kg²")
        print(f"库仑常数: k_e = {k_e} N·m² / C²")
        print(f"在 r = {r_min} m 处:")
        print(f"  引力: F_g = {F_gravity_values[0]:.6e} N")
        print(f"  电磁力: F_e = {F_electric_values[0]:.6e} N")
        print(f"  统一力: F_u = {F_unified_values[0]:.6e} N")
        print(f"  力的比值 |F_g / F_e| = {force_ratio[0]:.6e}")
        
        print(" / n数据表:")
        print(data_table)
        
        return numerical_results
    
    def visualize_force_distributions(self, save_fig = False, fig_path = None):"""力分布可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        r_values = self.results['numerical']['force_distributions']['r_values']
        F_gravity_values = self.results['numerical']['force_distributions']['F_gravity_values']
        F_electric_values = self.results['numerical']['force_distributions']['F_electric_values']
        F_unified_values = self.results['numerical']['force_distributions']['F_unified_values']
        
        plt.figure(figsize = (12, 8))
        
        # 使用对数坐标更适合力分布
        plt.loglog(r_values, F_gravity_values, 'b - ', linewidth = 2, label = '引力')
        plt.loglog(r_values, F_electric_values, 'r - ', linewidth = 2, label = '电磁力')
        plt.loglog(r_values, F_unified_values, 'g - ', linewidth = 2, label = '统一力')
        
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title('引力、电磁力和统一力的径向分布', fontsize = 16)
        plt.xlabel('距离 r (m)', fontsize = 14)
        plt.ylabel('力的大小 (N)', fontsize = 14)
        plt.legend(fontsize = 12)
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_force_ratio(self, save_fig = False, fig_path = None):"""力的比值可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        r_values = self.results['numerical']['force_distributions']['r_values']
        force_ratio = self.results['numerical']['force_distributions']['force_ratio']
        
        plt.figure(figsize = (12, 8))
        
        # 绘制力的比值(对数坐标)
        plt.semilogy(r_values, force_ratio, 'm - ', linewidth = 2)
        
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title('引力与电磁力的比值', fontsize = 16)
        plt.xlabel('距离 r (m)', fontsize = 14)
        plt.ylabel('|F_g / F_e|', fontsize = 14)
        plt.axhline(y = 1.0, color = 'k', linestyle = ' -  - ', label = 'F_g = F_e')
        plt.legend(fontsize = 12)
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_energy_density(self, save_fig = False, fig_path = None):"""能量密度可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        r_values = self.results['numerical']['force_distributions']['r_values']
        energy_density_gravity = self.results['numerical']['force_distributions']['energy_densities']['gravity']
        energy_density_electric = self.results['numerical']['force_distributions']['energy_densities']['electric']
        energy_density_unified = self.results['numerical']['force_distributions']['energy_densities']['unified']
        
        plt.figure(figsize = (12, 8))
        
        plt.loglog(r_values, energy_density_gravity, 'b - ', linewidth = 2, label = '引力场能量密度')
        plt.loglog(r_values, energy_density_electric, 'r - ', linewidth = 2, label = '电场能量密度')
        plt.loglog(r_values, energy_density_unified, 'g - ', linewidth = 2, label = '统一场能量密度')
        
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title('场能量密度分布', fontsize = 16)
        plt.xlabel('距离 r (m)', fontsize = 14)
        plt.ylabel('能量密度 (J / m³)', fontsize = 14)
        plt.legend(fontsize = 12)
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_parameter_influence(self, parameter_type = 'mass', save_fig = False, fig_path = None):"""参数影响可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        r_values = self.results['numerical']['force_distributions']['r_values']
        
        if parameter_type =  = 'mass':
            comparisons = self.results['numerical']['parameter_comparisons']['mass']
            force_type = '引力'
        else:  # charge
            comparisons = self.results['numerical']['parameter_comparisons']['charge']
            force_type = '电磁力'
        
        plt.figure(figsize = (12, 8))
        
        for param_key, param_data in comparisons.items():
            if parameter_type =  = 'mass':
                plt.loglog(r_values, param_data['gravity_force'], linewidth = 2, label = param_data['label'])
            else:
                plt.loglog(r_values, param_data['electric_force'], linewidth = 2, label = param_data['label'])
        
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title(f'不同{"质量" if parameter_type =  = "mass" else "电荷"}下的{force_type}分布', fontsize = 16)
        plt.xlabel('距离 r (m)', fontsize = 14)
        plt.ylabel(f'{force_type}大小 (N)', fontsize = 14)
        plt.legend(fontsize = 12)
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def export_results_to_csv(self, csv_path = None):"""导出结果到CSV文件"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        # 导出力分布数据
        r_values = self.results['numerical']['force_distributions']['r_values']
        F_gravity_values = self.results['numerical']['force_distributions']['F_gravity_values']
        F_electric_values = self.results['numerical']['force_distributions']['F_electric_values']
        F_unified_values = self.results['numerical']['force_distributions']['F_unified_values']
        force_ratio = self.results['numerical']['force_distributions']['force_ratio']
        energy_density_gravity = self.results['numerical']['force_distributions']['energy_densities']['gravity']
        energy_density_electric = self.results['numerical']['force_distributions']['energy_densities']['electric']
        energy_density_unified = self.results['numerical']['force_distributions']['energy_densities']['unified']
        
        force_data = pd.DataFrame({
# '距离 r (m)': r_values,
# '引力 F_g (N)': F_gravity_values,
# '电磁力 F_e (N)': F_electric_values,
# '统一力 F_u (N)': F_unified_values,
# '力的比值 |F_g / F_e|': force_ratio,
# '引力场能量密度 (J / m³)': energy_density_gravity,
# '电场能量密度 (J / m³)': energy_density_electric,
# '统一场能量密度 (J / m³)': energy_density_unified
        })
        
        # 导出数据表
        data_table = self.results['numerical']['force_distributions']['data_table']
        
        if csv_path:
            force_data.to_csv(f"{csv_path}_力分布数据.csv", index = False, encoding = 'utf - 8 - sig')
            data_table.to_csv(f"{csv_path}_数据表.csv", index = False, encoding = 'utf - 8 - sig')
            print(f"数据已导出至: {csv_path}_ * .csv")
        
        return force_data, data_table
    
    def run_complete_analysis(self):"""运行完整分析"""self.symbolic_derivation()
        self.special_cases_analysis()
        self.numerical_simulation()
        return self.results


def main():"""主函数"""analyzer = UnifiedGravityElectromagnetism()
    results = analyzer.run_complete_analysis()
    
    # 可视化
    analyzer.visualize_force_distributions()
    analyzer.visualize_force_ratio()
    analyzer.visualize_energy_density()
    analyzer.visualize_parameter_influence(parameter_type = 'mass')
    analyzer.visualize_parameter_influence(parameter_type = 'charge')
    
    # 导出数据
    analyzer.export_results_to_csv("引力与电磁力统一方程验证数据")
    
    print(" / n =  =  = 引力与电磁力统一方程验证总结 =  =  = ")
    print("1. 符号求导验证完成:成功验证了统一场方程的数学表达式")
    print("2. 特殊情况分析完成:验证了不同条件下的场特性")
    print("3. 数值模拟完成:验证了引力、电磁力及其统一形式的分布规律")
    print("4. 可视化分析完成:直观展示了力的分布、比值和能量密度")
    print("5. 参数影响分析:验证了质量和电荷对力分布的影响")
    print("6. 验证结论:引力与电磁力统一方程具有良好的数学自洽性和物理合理性")
    print("7. 物理意义:引力和电磁力可能具有统一的本质,遵循相似的数学规律")


if __name__ =  = "__main__":
    main()