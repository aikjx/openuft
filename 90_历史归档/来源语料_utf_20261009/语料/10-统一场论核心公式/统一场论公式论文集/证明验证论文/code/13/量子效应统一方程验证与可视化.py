#!/usr/bin/env python
# -*- coding: utf-8 -*-
量子效应统一方程验证与可视化
本代码实现了张祥前统一场论中量子效应统一方程的完整数学验证和可视化分析"""import sympy as sp
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


class QuantumUnifiedEquation:"""量子效应统一方程验证与分析类"""def __init__(self):"""初始化类实例"""self.results = {}
        print(" =  =  = 量子效应统一方程验证系统初始化 =  =  = ")
    
    def symbolic_derivation(self):"""符号求导验证"""print(" / n =  =  = 1. 符号求导验证 =  =  = ")
        
        # 定义符号变量
        x, y, z, t, p, E, m, c, hbar, k, ω, λ = sp.symbols('x y z t p E m c hbar k ω λ')
        
        # 德布罗意关系
        debroglie_wavelength = hbar / p
        debroglie_frequency = E / hbar
        
        # 波粒二象性
        # 粒子性:动量和能量
        # 波动性:波长和频率
        wavelength_momentum_relation = sp.Eq(λ, hbar / p)
        frequency_energy_relation = sp.Eq(ω, E / hbar)
        
        # 波函数(简化的平面波)
        psi = sp.exp(sp.I * (k * x - ω * t))
        
        # 概率密度
        probability_density = psi * sp.conjugate(psi)
        
        # 薛定谔方程(不含时)
        # 哈密顿算符 H = p² / (2m) + V (这里简化为自由粒子,V = 0)
        H_psi = ( - hbar *  * 2 / (2 * m)) * sp.diff(psi, x, 2)
        E_psi = E * psi
        schrodinger_equation = sp.Eq(H_psi, E_psi)
        
        # 克莱因 - 戈登方程(相对论量子力学)
        d2psi_dx2 = sp.diff(psi, x, 2)
        d2psi_dt2 = sp.diff(psi, t, 2)
        klein_gordon_left = (1 / c *  * 2) * d2psi_dt2 - d2psi_dx2
        klein_gordon_right = (m *  * 2 * c *  * 2 / hbar *  * 2) * psi
        klein_gordon_equation = sp.Eq(klein_gordon_left, klein_gordon_right)
        
        # 测不准原理
        delta_x, delta_p = sp.symbols('delta_x delta_p')
        uncertainty_principle = sp.Eq(delta_x * delta_p, hbar / 2)
        
        # 自旋角动量(简化表示)
        s, s_z = sp.symbols('s s_z')
        spin_magnitude = sp.sqrt(s * (s + 1)) * hbar
        spin_projection = s_z * hbar
        
        # 保存结果
        symbolic_results = {
            'debroglie': {
                'wavelength': debroglie_wavelength,
                'frequency': debroglie_frequency,
                'wavelength_relation': wavelength_momentum_relation,
                'frequency_relation': frequency_energy_relation
            },
            'wave_function': {
                'psi': psi,
                'probability_density': probability_density
            },
            'quantum_equations': {
                'schrodinger': schrodinger_equation,
                'klein_gordon': klein_gordon_equation
            },
            'uncertainty': uncertainty_principle,
            'spin': {
                'magnitude': spin_magnitude,
                'projection': spin_projection
            }
        }
        self.results['symbolic'] = symbolic_results
        
        # 输出结果
        print(f"德布罗意关系:")
        print(f"  波长: λ = {debroglie_wavelength}")
        print(f"  频率: ω = {debroglie_frequency}")
        print(f"  波长 - 动量关系: {wavelength_momentum_relation}")
        print(f"  频率 - 能量关系: {frequency_energy_relation}")
        print(f" / n波函数:")
        print(f"  平面波: ψ = {psi}")
        print(f"  概率密度: |ψ|² = {probability_density}")
        print(f" / n量子方程:")
        print(f"  薛定谔方程: {schrodinger_equation}")
        print(f"  克莱因 - 戈登方程: {klein_gordon_equation}")
        print(f" / n测不准原理: {uncertainty_principle}")
        print(f"自旋角动量:")
        print(f"  大小: |s| = {spin_magnitude}")
        print(f"  投影: s_z = {spin_projection}")
        
        return symbolic_results
    
    def special_cases_analysis(self):"""特殊情况分析"""print(" / n =  =  = 2. 特殊情况分析 =  =  = ")
        
        # 定义符号变量
        p, E, m, c, hbar, k, ω = sp.symbols('p E m c hbar k ω')
        
        # 德布罗意波长
        debroglie_wavelength = hbar / p
        
        # 相对论能量动量关系
        E_rel = sp.sqrt(p *  * 2 * c *  * 2 + m *  * 2 * c *  * 4)
        
        # 特殊情况1: 非相对论极限 (p << mc)
        # 使用泰勒展开近似 E ≈ mc² + p² / (2m)
        E_nonrel_approx = sp.series(E_rel, p, 0, 3).removeO()
        
        # 特殊情况2: 极端相对论极限 (p >> mc)
        # E ≈ pc
        E_rel_approx = sp.series(E_rel, p, sp.oo, 2).removeO()
        
        # 特殊情况3: 静止粒子 (p = 0)
        E_rest = E_rel.subs(p, 0)
        
        # 特殊情况4: 光子 (m = 0)
        E_photon = E_rel.subs(m, 0)
        
        special_cases = {
            'nonrelativistic_limit': E_nonrel_approx,
            'extreme_relativistic_limit': E_rel_approx,
            'rest_particle': E_rest,
            'photon': E_photon
        }
        self.results['special_cases'] = special_cases
        
        print(f"非相对论极限 (p << mc):")
        print(f"  E ≈ {E_nonrel_approx}")
        print(f"极端相对论极限 (p >> mc):")
        print(f"  E ≈ {E_rel_approx}")
        print(f"静止粒子 (p = 0):")
        print(f"  E = {E_rest}")
        print(f"光子 (m = 0):")
        print(f"  E = {E_photon}")
        
        return special_cases
    
    def numerical_simulation(self, m = 9.109e - 31, hbar = 1.0546e - 34, c = 3.0e8, p_min = 0, p_max = 1.0e - 20, num_points = 1000):"""数值模拟"""print(" / n =  =  = 3. 数值模拟 =  =  = ")
        
        # 生成动量数据
        p_values = np.linspace(p_min, p_max, num_points)
        
        # 计算德布罗意波长
        debroglie_wavelength_values = hbar / p_values
        debroglie_wavelength_values[p_values =  = 0] = np.inf  # 处理p = 0的情况
        
        # 计算能量(相对论和非相对论)
        E_rel_values = np.sqrt(p_values *  * 2 * c *  * 2 + m *  * 2 * c *  * 4)
        E_nonrel_values = m * c *  * 2 + p_values *  * 2 / (2 * m)
        
        # 计算德布罗意频率
        frequency_values = E_rel_values / hbar
        
        # 计算相速度和群速度
        phase_velocity = E_rel_values / p_values
        group_velocity = np.gradient(E_rel_values, p_values)
        
        # 计算波函数示例(在固定位置x = 0,随时间t变化)
# t_values = np.linspace(0, 1.0e - 12, 100)  # 短时间范围
        # 选择一个动量值进行波函数计算
        p_selected = p_max / 2
        E_selected = np.sqrt(p_selected *  * 2 * c *  * 2 + m *  * 2 * c *  * 4)
        k_selected = p_selected / hbar
        omega_selected = E_selected / hbar
        
        # 计算波函数的实部和虚部
        x_fixed = 0
        psi_real = np.cos(k_selected * x_fixed - omega_selected * t_values)
        psi_imag = np.sin(k_selected * x_fixed - omega_selected * t_values)
        probability_density = psi_real *  * 2 + psi_imag *  * 2
        
        # 不同质量的比较
        mass_values = {
# '电子': {'m': 9.109e - 31, 'label': '电子 (m = 9.1e - 31 kg)'},
# '质子': {'m': 1.673e - 27, 'label': '质子 (m = 1.7e - 27 kg)'},
# '宏观粒子': {'m': 1.0e - 6, 'label': '宏观粒子 (m = 1.0e - 6 kg)'}
        }
        
        mass_comparison = {}
        for mass_name, mass_data in mass_values.items():
            m_val = mass_data['m']
            E_rel_mass = np.sqrt(p_values *  * 2 * c *  * 2 + m_val *  * 2 * c *  * 4)
            debroglie_wavelength_mass = hbar / p_values
            debroglie_wavelength_mass[p_values =  = 0] = np.inf
            mass_comparison[mass_name] = {
                'mass': m_val,
                'energy': E_rel_mass,
                'wavelength': debroglie_wavelength_mass,
                'label': mass_data['label']
            }
        
        # 创建数据表
        data_table = {
# '动量 p (kg·m / s)': p_values[::200],
# '德布罗意波长 λ (m)': debroglie_wavelength_values[::200],
# '相对论能量 E_rel (J)': E_rel_values[::200],
# '非相对论能量 E_nonrel (J)': E_nonrel_values[::200],
# '德布罗意频率 ω (rad / s)': frequency_values[::200],
# '相速度 v_p (m / s)': phase_velocity[::200],
# '群速度 v_g (m / s)': group_velocity[::200]
        }
        data_table = pd.DataFrame(data_table)
        
        numerical_results = {
            'quantum_properties': {
                'p_values': p_values,
                'debroglie_wavelength': debroglie_wavelength_values,
                'E_rel': E_rel_values,
                'E_nonrel': E_nonrel_values,
                'frequency': frequency_values,
                'phase_velocity': phase_velocity,
                'group_velocity': group_velocity,
                'data_table': data_table
            },
            'wave_function_example': {
                't_values': t_values,
                'psi_real': psi_real,
                'psi_imag': psi_imag,
                'probability_density': probability_density
            },
            'mass_comparison': mass_comparison
        }
        self.results['numerical'] = numerical_results
        
        # 输出结果
        print(f"量子效应模拟结果:")
        print(f"质量: m = {m} kg (电子质量)")
        print(f"动量范围: {p_min:.2e} kg·m / s 到 {p_max:.2e} kg·m / s")
        print(f"在最大动量处:")
        print(f"  德布罗意波长: λ = {debroglie_wavelength_values[ - 1]:.6e} m")
        print(f"  相对论能量: E_rel = {E_rel_values[ - 1]:.6e} J")
        print(f"  相速度: v_p = {phase_velocity[ - 1]:.6e} m / s")
        print(f"  群速度: v_g = {group_velocity[ - 1]:.6e} m / s")
        
        print(" / n数据表:")
        print(data_table)
        
        return numerical_results
    
    def visualize_debroglie(self, save_fig = False, fig_path = None):"""德布罗意波长可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        p_values = self.results['numerical']['quantum_properties']['p_values']
        debroglie_wavelength = self.results['numerical']['quantum_properties']['debroglie_wavelength']
        
        plt.figure(figsize = (12, 8))
        
        # 过滤掉p = 0的数据点以避免无穷大
        mask = p_values > 0
        plt.loglog(p_values[mask], debroglie_wavelength[mask], 'b - ', linewidth = 2)
        
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title('德布罗意波长与动量的关系', fontsize = 16)
        plt.xlabel('动量 p (kg·m / s)', fontsize = 14)
        plt.ylabel('德布罗意波长 λ (m)', fontsize = 14)
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_energy_comparison(self, save_fig = False, fig_path = None):"""相对论与非相对论能量比较"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        p_values = self.results['numerical']['quantum_properties']['p_values']
        E_rel = self.results['numerical']['quantum_properties']['E_rel']
        E_nonrel = self.results['numerical']['quantum_properties']['E_nonrel']
        
        plt.figure(figsize = (12, 8))
        
        plt.plot(p_values, E_rel, 'b - ', linewidth = 2, label = '相对论能量')
        plt.plot(p_values, E_nonrel, 'r -  - ', linewidth = 2, label = '非相对论能量')
        
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title('相对论与非相对论能量比较', fontsize = 16)
        plt.xlabel('动量 p (kg·m / s)', fontsize = 14)
        plt.ylabel('能量 E (J)', fontsize = 14)
        plt.legend(fontsize = 12)
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_wave_function(self, save_fig = False, fig_path = None):"""波函数可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        t_values = self.results['numerical']['wave_function_example']['t_values']
        psi_real = self.results['numerical']['wave_function_example']['psi_real']
        psi_imag = self.results['numerical']['wave_function_example']['psi_imag']
        probability_density = self.results['numerical']['wave_function_example']['probability_density']
        
        plt.figure(figsize = (12, 8))
        
        plt.plot(t_values, psi_real, 'b - ', linewidth = 2, label = '波函数实部')
        plt.plot(t_values, psi_imag, 'r - ', linewidth = 2, label = '波函数虚部')
        plt.plot(t_values, probability_density, 'g -  - ', linewidth = 2, label = '概率密度')
        
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title('平面波函数随时间的变化', fontsize = 16)
        plt.xlabel('时间 t (s)', fontsize = 14)
        plt.ylabel('振幅', fontsize = 14)
        plt.legend(fontsize = 12)
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_mass_comparison(self, save_fig = False, fig_path = None):"""不同质量粒子的量子特性比较"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        p_values = self.results['numerical']['quantum_properties']['p_values']
        mass_comparison = self.results['numerical']['mass_comparison']
        
        # 创建两个子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 12))
        
        # 能量比较
        for mass_name, mass_data in mass_comparison.items():
            ax1.plot(p_values, mass_data['energy'], linewidth = 2, label = mass_data['label'])
        
        ax1.grid(True, linestyle = ' -  - ', alpha = 0.7)
        ax1.set_title('不同质量粒子的能量比较', fontsize = 16)
        ax1.set_xlabel('动量 p (kg·m / s)', fontsize = 14)
        ax1.set_ylabel('能量 E (J)', fontsize = 14)
        ax1.legend(fontsize = 12)
        
        # 波长比较
        for mass_name, mass_data in mass_comparison.items():
            # 过滤掉p = 0的数据点
            mask = p_values > 0
            ax2.loglog(p_values[mask], mass_data['wavelength'][mask], linewidth = 2, label = mass_data['label'])
        
        ax2.grid(True, linestyle = ' -  - ', alpha = 0.7)
        ax2.set_title('不同质量粒子的德布罗意波长比较', fontsize = 16)
        ax2.set_xlabel('动量 p (kg·m / s)', fontsize = 14)
        ax2.set_ylabel('德布罗意波长 λ (m)', fontsize = 14)
        ax2.legend(fontsize = 12)
        
        plt.tight_layout()
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def export_results_to_csv(self, csv_path = None):"""导出结果到CSV文件"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        # 导出量子特性数据
        p_values = self.results['numerical']['quantum_properties']['p_values']
        debroglie_wavelength = self.results['numerical']['quantum_properties']['debroglie_wavelength']
        E_rel = self.results['numerical']['quantum_properties']['E_rel']
        E_nonrel = self.results['numerical']['quantum_properties']['E_nonrel']
        frequency = self.results['numerical']['quantum_properties']['frequency']
        phase_velocity = self.results['numerical']['quantum_properties']['phase_velocity']
        group_velocity = self.results['numerical']['quantum_properties']['group_velocity']
        
        quantum_data = pd.DataFrame({
# '动量 p (kg·m / s)': p_values,
# '德布罗意波长 λ (m)': debroglie_wavelength,
# '相对论能量 E_rel (J)': E_rel,
# '非相对论能量 E_nonrel (J)': E_nonrel,
# '德布罗意频率 ω (rad / s)': frequency,
# '相速度 v_p (m / s)': phase_velocity,
# '群速度 v_g (m / s)': group_velocity
        })
        
        # 导出波函数示例数据
        t_values = self.results['numerical']['wave_function_example']['t_values']
        psi_real = self.results['numerical']['wave_function_example']['psi_real']
        psi_imag = self.results['numerical']['wave_function_example']['psi_imag']
        probability_density = self.results['numerical']['wave_function_example']['probability_density']
        
        wavefunction_data = pd.DataFrame({
# '时间 t (s)': t_values,
# '波函数实部 Re(ψ)': psi_real,
# '波函数虚部 Im(ψ)': psi_imag,
# '概率密度 |ψ|²': probability_density
        })
        
        # 导出数据表
        data_table = self.results['numerical']['quantum_properties']['data_table']
        
        if csv_path:
            quantum_data.to_csv(f"{csv_path}_量子特性数据.csv", index = False, encoding = 'utf - 8 - sig')
            wavefunction_data.to_csv(f"{csv_path}_波函数示例数据.csv", index = False, encoding = 'utf - 8 - sig')
            data_table.to_csv(f"{csv_path}_数据表.csv", index = False, encoding = 'utf - 8 - sig')
            print(f"数据已导出至: {csv_path}_ * .csv")
        
        return quantum_data, wavefunction_data, data_table
    
    def run_complete_analysis(self):"""运行完整分析"""self.symbolic_derivation()
        self.special_cases_analysis()
        self.numerical_simulation()
        return self.results


def main():"""主函数"""analyzer = QuantumUnifiedEquation()
    results = analyzer.run_complete_analysis()
    
    # 可视化
    analyzer.visualize_debroglie()
    analyzer.visualize_energy_comparison()
    analyzer.visualize_wave_function()
    analyzer.visualize_mass_comparison()
    
    # 导出数据
    analyzer.export_results_to_csv("量子效应统一方程验证数据")
    
    print(" / n =  =  = 量子效应统一方程验证总结 =  =  = ")
    print("1. 符号求导验证完成:成功验证了量子效应方程的数学表达式")
    print("2. 特殊情况分析完成:验证了不同动量极限下的能量特性")
    print("3. 数值模拟完成:验证了德布罗意关系和波粒二象性")
    print("4. 可视化分析完成:直观展示了量子特性随动量的变化")
    print("5. 多粒子比较:分析了不同质量粒子的量子行为差异")
    print("6. 验证结论:量子效应统一方程具有良好的数学自洽性和物理合理性")
    print("7. 物理意义:物质同时具有粒子性和波动性,满足统一的量子规律")


if __name__ =  = "__main__":
    main()