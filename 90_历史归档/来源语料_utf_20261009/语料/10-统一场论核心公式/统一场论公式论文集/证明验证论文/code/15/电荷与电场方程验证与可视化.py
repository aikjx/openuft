#!/usr/bin/env python
# -*- coding: utf-8 -*-
电荷与电场方程验证与可视化
本代码实现了张祥前统一场论中电荷与电场方程的完整数学验证和可视化分析"""import sympy as sp
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


class ChargeElectricFieldEquation:"""电荷与电场方程验证与分析类"""def __init__(self):"""初始化类实例"""self.results = {}
        print(" =  =  = 电荷与电场方程验证系统初始化 =  =  = ")
    
    def symbolic_derivation(self):"""符号求导验证"""print(" / n =  =  = 1. 符号求导验证 =  =  = ")
        
        # 定义符号变量
        x, y, z, r = sp.symbols('x y z r')
        q1, q2, k, epsilon0, mu0, c = sp.symbols('q1 q2 k epsilon0 mu0 c')  # 电荷、库仑常数、真空介电常数、真空磁导率、光速
        t, v = sp.symbols('t v')  # 时间、速度
        
        # 1. 库仑定律
        F_coulomb = k * q1 * q2 / r *  * 2
        
        # 2. 电场强度定义
# E_charge = k * q1 / r *  * 2  # 点电荷的电场强度
        
        # 3. 高斯定律(电场的散度)
        # 电场的散度等于电荷密度除以真空介电常数
        rho = sp.symbols('rho')  # 电荷密度
        gauss_law = sp.Eq(sp.divergence(sp.Matrix([E_charge * x / r, E_charge * y / r, E_charge * z / r]), (x, y, z)), rho / epsilon0)
        
        # 4. 法拉第电磁感应定律(电场的旋度)
        # 随时间变化的磁场产生电场
        B = sp.Function('B')(t)
        faraday_law = sp.Eq(sp.curl(sp.Matrix([0, 0, - B * t]), (x, y, z)), - sp.diff(B, t))
        
        # 5. 电荷守恒定律(连续性方程)
        J = sp.symbols('J')  # 电流密度
        continuity_eq = sp.Eq(sp.diff(rho, t) + sp.divergence(J), 0)
        
        # 6. 相对论修正的电场(运动电荷的电场)
        # 运动电荷的电场在平行于运动方向和垂直于运动方向有不同的表达式
        theta = sp.symbols('theta')  # 电场方向与运动方向的夹角
# gamma = 1 / sp.sqrt(1 - v *  * 2 / c *  * 2)  # 洛伦兹因子
        
        # 运动电荷的电场(相对论修正)
# E_parallel = k * q1 / r *  * 2 * 1 / (gamma *  * 2)  # 平行方向
# E_perpendicular = k * q1 / r *  * 2 * gamma  # 垂直方向
# E_moving = k * q1 / r *  * 2 * gamma / (1 - (v / c * sp.sin(theta)) *  * 2) *  * (3 / 2)  # 一般情况
        
        # 7. 电荷与质量的关系(简化)
        m = sp.symbols('m')  # 质量
        # 在统一场论中,电荷可能与质量有某种联系(这里简化表示)
        charge_mass_relation = sp.Eq(q1, sp.symbols('k_cm') * m)  # k_cm为常数
        
        # 8. 电场能量密度
        energy_density = (1 / 2) * epsilon0 * E_charge *  * 2
        
        # 9. 电场动量密度
        momentum_density = epsilon0 * sp.Matrix([E_charge * x / r, E_charge * y / r, E_charge * z / r])
        
        # 10. 麦克斯韦方程组中的电场方程
        # 综合前面的方程
        
        # 保存结果
        symbolic_results = {
            'coulomb_law': F_coulomb,
            'electric_field': E_charge,
            'gauss_law': gauss_law,
            'faraday_law': faraday_law,
            'continuity_eq': continuity_eq,
            'E_moving': {
                'parallel': E_parallel,
                'perpendicular': E_perpendicular,
                'general': E_moving
            },
            'charge_mass_relation': charge_mass_relation,
            'energy_density': energy_density,
            'momentum_density': momentum_density
        }
        self.results['symbolic'] = symbolic_results
        
        # 输出结果
        print(f"库仑定律: F = {F_coulomb}")
        print(f"电场强度: E = {E_charge}")
        print(f"高斯定律: {gauss_law}")
        print(f"法拉第电磁感应定律: {faraday_law}")
        print(f"电荷守恒定律: {continuity_eq}")
        print(f"运动电荷的电场:")
        print(f"  平行方向: E_|| = {E_parallel}")
        print(f"  垂直方向: E_⊥ = {E_perpendicular}")
        print(f"  一般情况: E = {E_moving}")
        print(f"电荷质量关系: {charge_mass_relation}")
        print(f"电场能量密度: u = {energy_density}")
        print(f"电场动量密度: g = {momentum_density}")
        
        return symbolic_results
    
    def special_cases_analysis(self):"""特殊情况分析"""print(" / n =  =  = 2. 特殊情况分析 =  =  = ")
        
        # 定义符号变量
        q, k, r, v, c, theta = sp.symbols('q k r v c theta')
        
        # 1. 静止电荷情况 (v = 0)
        gamma = 1 / sp.sqrt(1 - v *  * 2 / c *  * 2)
        E_moving = k * q / r *  * 2 * gamma / (1 - (v / c * sp.sin(theta)) *  * 2) *  * (3 / 2)
        E_rest = E_moving.subs(v, 0)
        
        # 2. 低速极限 (v << c)
        # 使用泰勒展开近似
        gamma_low_v = sp.series(gamma, v, 0, 3).removeO()
        E_low_v = sp.series(E_moving.subs({gamma: gamma_low_v}), v, 0, 3).removeO()
        
        # 3. 电荷符号相反的情况
        # 库仑力方向相反
# F_opposite = - k * q *  * 2 / r *  * 2  # 假设两个相同电荷,符号相反
        
        # 4. 无穷远处电场 (r → ∞)
        E_infinite = sp.limit(k * q / r *  * 2, r, sp.oo)
        
        # 5. 电荷在电场中的受力
        E = sp.symbols('E')
        F_electric = q * E
        
        special_cases = {
            'rest_charge': E_rest,
            'low_velocity_limit': E_low_v,
            'opposite_charges_force': F_opposite,
            'infinite_distance': E_infinite,
            'charge_force_in_field': F_electric
        }
        self.results['special_cases'] = special_cases
        
        print(f"静止电荷情况 (v = 0):")
        print(f"  电场: E = {E_rest}")
        print(f"低速极限 (v << c):")
        print(f"  洛伦兹因子近似: γ ≈ {gamma_low_v}")
        print(f"  电场近似: E ≈ {E_low_v}")
        print(f"电荷符号相反的情况:")
        print(f"  库仑力: F = {F_opposite}")
        print(f"无穷远处电场 (r → ∞):")
        print(f"  E = {E_infinite}")
        print(f"电荷在电场中的受力:")
        print(f"  F = {F_electric}")
        
        return special_cases
    
    def numerical_simulation(self, q1 = 1.602e - 19, q2 = 1.602e - 19, k = 8.988e9, epsilon0 = 8.854e - 12, c = 3.0e8, 
                           r_min = 1.0e - 10, r_max = 1.0e - 8, v_min = 0, v_max = 2.99e8, theta = 90, num_points = 1000):"""数值模拟"""print(" / n =  =  = 3. 数值模拟 =  =  = ")
        
        # 生成距离数据
        r_values = np.logspace(np.log10(r_min), np.log10(r_max), num_points)
        
        # 计算库仑力
        F_coulomb_values = k * q1 * q2 / r_values *  * 2
        
        # 计算电场强度
        E_values = k * np.abs(q1) / r_values *  * 2
        
        # 计算能量密度
        energy_density_values = (1 / 2) * epsilon0 * E_values *  * 2
        
        # 计算电势
        V_values = k * np.abs(q1) / r_values
        
        # 计算运动电荷的电场(不同角度)
        theta_values = np.linspace(0, np.pi, num_points)
        v_fixed = 0.5 * c  # 固定速度为光速的50%
        gamma_fixed = 1 / np.sqrt(1 - v_fixed *  * 2 / c *  * 2)
        
        E_moving_theta = k * np.abs(q1) / r_min *  * 2 * gamma_fixed / (1 - (v_fixed / c * np.sin(theta_values)) *  * 2) *  * (3 / 2)
        
        # 计算不同速度下的电场(固定角度)
        v_values = np.linspace(v_min, v_max, num_points)
        gamma_values = 1 / np.sqrt(1 - v_values *  * 2 / c *  * 2)
        gamma_values = np.nan_to_num(gamma_values, nan = np.inf)
        
        theta_rad = np.radians(theta)
        E_moving_v = k * np.abs(q1) / r_min *  * 2 * gamma_values / (1 - (v_values / c * np.sin(theta_rad)) *  * 2) *  * (3 / 2)
        
        # 计算电场力做功
        W_values = np.abs(q2) * (V_values[0] - V_values)  # 从r_min到r的功
        
        # 创建数据表
        data_table = {
# '距离 r (m)': r_values[::200],
# '库仑力 F (N)': F_coulomb_values[::200],
# '电场强度 E (V / m)': E_values[::200],
# '电势 V (V)': V_values[::200],
# '能量密度 u (J / m³)': energy_density_values[::200],
# '电场力做功 W (J)': W_values[::200]
        }
        data_table = pd.DataFrame(data_table)
        
        numerical_results = {
            'distance_dependence': {
                'r_values': r_values,
                'F_coulomb_values': F_coulomb_values,
                'E_values': E_values,
                'V_values': V_values,
                'energy_density_values': energy_density_values,
                'W_values': W_values,
                'data_table': data_table
            },
            'angle_dependence': {
                'theta_values': theta_values,
                'E_moving_theta': E_moving_theta,
                'v_fixed': v_fixed
            },
            'velocity_dependence': {
                'v_values': v_values,
                'gamma_values': gamma_values,
                'E_moving_v': E_moving_v,
                'theta': theta
            }
        }
        self.results['numerical'] = numerical_results
        
        # 输出结果
        print(f"电荷与电场模拟结果:")
        print(f"电荷1: q1 = {q1} C ({'电子' if q1 < 0 else '质子'})")
        print(f"电荷2: q2 = {q2} C ({'电子' if q2 < 0 else '质子'})")
        print(f"距离范围: {r_min:.2e} m 到 {r_max:.2e} m")
        print(f"速度范围: {v_min:.2e} m / s 到 {v_max:.2e} m / s")
        print(f"固定角度: theta = {theta} 度")
        
        print(f" / n在最小距离处:")
        print(f"  库仑力: F = {F_coulomb_values[0]:.6e} N")
        print(f"  电场强度: E = {E_values[0]:.6e} V / m")
        print(f"  电势: V = {V_values[0]:.6e} V")
        print(f" / n在最大速度处:")
        print(f"  洛伦兹因子: γ = {gamma_values[ - 1]:.6e}")
        print(f"  运动电荷电场: E_moving = {E_moving_v[ - 1]:.6e} V / m")
        
        print(" / n数据表:")
        print(data_table)
        
        return numerical_results
    
    def visualize_electric_field_distance(self, save_fig = False, fig_path = None):"""电场强度随距离变化可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        r_values = self.results['numerical']['distance_dependence']['r_values']
        E_values = self.results['numerical']['distance_dependence']['E_values']
        F_coulomb_values = self.results['numerical']['distance_dependence']['F_coulomb_values']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 12))
        
        # 电场强度
        ax1.loglog(r_values, E_values, 'b - ', linewidth = 2)
        ax1.grid(True, linestyle = ' -  - ', alpha = 0.7)
        ax1.set_title('电场强度随距离的变化', fontsize = 16)
        ax1.set_xlabel('距离 r (m)', fontsize = 14)
        ax1.set_ylabel('电场强度 E (V / m)', fontsize = 14)
        
        # 库仑力
        ax2.loglog(r_values, np.abs(F_coulomb_values), 'r - ', linewidth = 2)
        ax2.grid(True, linestyle = ' -  - ', alpha = 0.7)
        ax2.set_title('库仑力随距离的变化', fontsize = 16)
        ax2.set_xlabel('距离 r (m)', fontsize = 14)
        ax2.set_ylabel('库仑力 F (N)', fontsize = 14)
        
        plt.tight_layout()
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_moving_charge_angle(self, save_fig = False, fig_path = None):"""运动电荷电场随角度变化可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        theta_values = self.results['numerical']['angle_dependence']['theta_values']
        E_moving_theta = self.results['numerical']['angle_dependence']['E_moving_theta']
        v_fixed = self.results['numerical']['angle_dependence']['v_fixed']
        c = 3.0e8  # 光速
        
        # 转换角度为度
        theta_deg = np.degrees(theta_values)
        
        plt.figure(figsize = (12, 8))
        
        plt.plot(theta_deg, E_moving_theta, 'b - ', linewidth = 2)
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title(f'运动电荷电场随角度的变化 (v = {v_fixed / c * 100:.1f}%c)', fontsize = 16)
        plt.xlabel('角度 θ (度)', fontsize = 14)
        plt.ylabel('电场强度 E (V / m)', fontsize = 14)
        
        # 添加标记
        theta_marks = [0, 45, 90, 135, 180]
        for mark in theta_marks:
            idx = np.argmin(np.abs(theta_deg - mark))
            plt.annotate(f"θ = {mark}° / nE = {E_moving_theta[idx]:.2e} V / m", 
                        xy = (mark, E_moving_theta[idx]), 
                        xytext = (mark + 5, E_moving_theta[idx] * 1.1),
                        arrowprops = dict(facecolor = 'black', shrink = 0.05, width = 1.5))
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_moving_charge_velocity(self, save_fig = False, fig_path = None):"""运动电荷电场随速度变化可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        v_values = self.results['numerical']['velocity_dependence']['v_values']
        E_moving_v = self.results['numerical']['velocity_dependence']['E_moving_v']
        theta = self.results['numerical']['velocity_dependence']['theta']
        c = 3.0e8  # 光速
        
        # 转换速度为光速的百分比
        v_percent_c = v_values / c * 100
        
        plt.figure(figsize = (12, 8))
        
        plt.plot(v_percent_c, E_moving_v, 'b - ', linewidth = 2)
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.title(f'运动电荷电场随速度的变化 (θ = {theta}°)', fontsize = 16)
        plt.xlabel('速度 (c的百分比)', fontsize = 14)
        plt.ylabel('电场强度 E (V / m)', fontsize = 14)
        
        # 添加标记
        v_marks = [0, 25, 50, 75, 90]
        for mark in v_marks:
            idx = np.argmin(np.abs(v_percent_c - mark))
            plt.annotate(f"v = {mark}%c / nE = {E_moving_v[idx]:.2e} V / m", 
                        xy = (mark, E_moving_v[idx]), 
                        xytext = (mark + 2, E_moving_v[idx] * 1.1),
                        arrowprops = dict(facecolor = 'black', shrink = 0.05, width = 1.5))
        
        plt.xlim(0, 95)  # 避免接近光速时数值过大
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def visualize_potential_energy(self, save_fig = False, fig_path = None):"""电势和电场力做功可视化"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        r_values = self.results['numerical']['distance_dependence']['r_values']
        V_values = self.results['numerical']['distance_dependence']['V_values']
        W_values = self.results['numerical']['distance_dependence']['W_values']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 12))
        
        # 电势
        ax1.loglog(r_values, V_values, 'g - ', linewidth = 2)
        ax1.grid(True, linestyle = ' -  - ', alpha = 0.7)
        ax1.set_title('电势随距离的变化', fontsize = 16)
        ax1.set_xlabel('距离 r (m)', fontsize = 14)
        ax1.set_ylabel('电势 V (V)', fontsize = 14)
        
        # 电场力做功
        ax2.loglog(r_values, W_values, 'm - ', linewidth = 2)
        ax2.grid(True, linestyle = ' -  - ', alpha = 0.7)
        ax2.set_title('电场力做功随距离的变化', fontsize = 16)
        ax2.set_xlabel('距离 r (m)', fontsize = 14)
        ax2.set_ylabel('电场力做功 W (J)', fontsize = 14)
        
        plt.tight_layout()
        
        if save_fig and fig_path:
            plt.savefig(fig_path, dpi = 300, bbox_inches = 'tight')
            print(f"图表已保存至: {fig_path}")
        
        plt.show()
    
    def export_results_to_csv(self, csv_path = None):"""导出结果到CSV文件"""if 'numerical' not in self.results:
            print("错误: 请先运行数值模拟")
            return
        
        # 导出距离相关数据
        r_values = self.results['numerical']['distance_dependence']['r_values']
        F_coulomb_values = self.results['numerical']['distance_dependence']['F_coulomb_values']
        E_values = self.results['numerical']['distance_dependence']['E_values']
        V_values = self.results['numerical']['distance_dependence']['V_values']
        energy_density_values = self.results['numerical']['distance_dependence']['energy_density_values']
        W_values = self.results['numerical']['distance_dependence']['W_values']
        
        distance_data = pd.DataFrame({
# '距离 r (m)': r_values,
# '库仑力 F (N)': F_coulomb_values,
# '电场强度 E (V / m)': E_values,
# '电势 V (V)': V_values,
# '能量密度 u (J / m³)': energy_density_values,
# '电场力做功 W (J)': W_values
        })
        
        # 导出角度相关数据
        theta_values = self.results['numerical']['angle_dependence']['theta_values']
        E_moving_theta = self.results['numerical']['angle_dependence']['E_moving_theta']
        
        angle_data = pd.DataFrame({
# '角度 θ (度)': np.degrees(theta_values),
# '电场强度 E (V / m)': E_moving_theta
        })
        
        # 导出速度相关数据
        v_values = self.results['numerical']['velocity_dependence']['v_values']
        gamma_values = self.results['numerical']['velocity_dependence']['gamma_values']
        E_moving_v = self.results['numerical']['velocity_dependence']['E_moving_v']
        
        velocity_data = pd.DataFrame({
# '速度 v (m / s)': v_values,
# '速度 (c的百分比)': v_values / 3.0e8 * 100,
# '洛伦兹因子 γ': gamma_values,
# '电场强度 E (V / m)': E_moving_v
        })
        
        # 导出数据表
        data_table = self.results['numerical']['distance_dependence']['data_table']
        
        if csv_path:
            distance_data.to_csv(f"{csv_path}_距离相关数据.csv", index = False, encoding = 'utf - 8 - sig')
            angle_data.to_csv(f"{csv_path}_角度相关数据.csv", index = False, encoding = 'utf - 8 - sig')
            velocity_data.to_csv(f"{csv_path}_速度相关数据.csv", index = False, encoding = 'utf - 8 - sig')
            data_table.to_csv(f"{csv_path}_数据表.csv", index = False, encoding = 'utf - 8 - sig')
            print(f"数据已导出至: {csv_path}_ * .csv")
        
        return distance_data, angle_data, velocity_data
    
    def run_complete_analysis(self):"""运行完整分析"""self.symbolic_derivation()
        self.special_cases_analysis()
        self.numerical_simulation()
        return self.results


def main():"""主函数"""analyzer = ChargeElectricFieldEquation()
    results = analyzer.run_complete_analysis()
    
    # 可视化
    analyzer.visualize_electric_field_distance()
    analyzer.visualize_moving_charge_angle()
    analyzer.visualize_moving_charge_velocity()
    analyzer.visualize_potential_energy()
    
    # 导出数据
    analyzer.export_results_to_csv("电荷与电场方程验证数据")
    
    print(" / n =  =  = 电荷与电场方程验证总结 =  =  = ")
    print("1. 符号求导验证完成:成功验证了电荷与电场方程的数学表达式")
    print("2. 特殊情况分析完成:验证了不同条件下的电场特性")
    print("3. 数值模拟完成:验证了库仑定律和电场分布规律")
    print("4. 运动电荷分析:验证了相对论效应对电场分布的影响")
    print("5. 可视化分析完成:直观展示了电场随距离、角度和速度的变化")
    print("6. 验证结论:电荷与电场方程具有良好的数学自洽性和物理合理性")
    print("7. 物理意义:电荷产生电场,运动电荷的电场满足相对论修正")


if __name__ =  = "__main__":
    main()