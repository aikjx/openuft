#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论三维螺旋运动方程的完整求导验证器
包含速度、加速度、曲率、挠率等运动学量的计算和可视化
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体支持
plt.rcParams.update({
    'font.family': ['SimHei', 'Microsoft YaHei', 'DejaVu Sans'],
    'axes.unicode_minus': False
})
import sympy as sp
import pandas as pd
from scipy.optimize import fsolve

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

class HelicalMotionDerivativeAnalyzer:
    """螺旋运动求导分析器"""
    
    def __init__(self):
        # 物理常数
        self.c = 299792458  # 光速 m/s
        
        # 符号变量
        self.t, self.r, self.omega, self.p = sp.symbols('t r omega p', positive=True, real=True)
        
        # 位置矢量的符号表达式
        self.R_sym = sp.Matrix([
            self.r * sp.cos(self.omega * self.t),
            self.r * sp.sin(self.omega * self.t),
            self.p * self.t
        ])
        
    def symbolic_derivatives(self):
        """符号求导：计算所有运动学量"""
        results = {}
        
        # 1. 位置矢量
        results['R'] = self.R_sym
        
        # 2. 速度矢量（一阶导数）
        V_sym = sp.diff(self.R_sym, self.t)
        results['V'] = V_sym
        
        # 3. 加速度矢量（二阶导数）
        a_sym = sp.diff(V_sym, self.t)
        results['a'] = a_sym
        
        # 4. 加加速度（三阶导数）
        j_sym = sp.diff(a_sym, self.t)
        results['j'] = j_sym
        
        # 5. 速度模
        V_magnitude_sym = sp.sqrt(V_sym.dot(V_sym))
        results['V_magnitude'] = V_magnitude_sym
        
        # 6. 加速度模
        a_magnitude_sym = sp.sqrt(a_sym.dot(a_sym))
        results['a_magnitude'] = a_magnitude_sym
        
        # 7. 光速约束
        light_speed_constraint = sp.simplify(V_magnitude_sym**2)
        results['light_speed_constraint'] = light_speed_constraint
        
        return results
    
    def numeric_derivatives(self, r_val=1.0, omega_val=1.0, p_val=1.0, num_points=100):
        """数值求导：计算具体的运动学量"""
        t_array = np.linspace(0, 4*np.pi, num_points)
        
        results = {
            't': t_array,
            'x': r_val * np.cos(omega_val * t_array),
            'y': r_val * np.sin(omega_val * t_array),
            'z': p_val * t_array,
            
            # 速度分量
            'Vx': -r_val * omega_val * np.sin(omega_val * t_array),
            'Vy': r_val * omega_val * np.cos(omega_val * t_array),
            'Vz': np.full_like(t_array, p_val),
            
            # 加速度分量
            'ax': -r_val * omega_val**2 * np.cos(omega_val * t_array),
            'ay': -r_val * omega_val**2 * np.sin(omega_val * t_array),
            'az': np.zeros_like(t_array),
            
            # 加加速度分量
            'jx': r_val * omega_val**3 * np.sin(omega_val * t_array),
            'jy': -r_val * omega_val**3 * np.cos(omega_val * t_array),
            'jz': np.zeros_like(t_array)
        }
        
        # 速度模和加速度模
        results['V_magnitude'] = np.sqrt(results['Vx']**2 + results['Vy']**2 + results['Vz']**2)
        results['a_magnitude'] = np.sqrt(results['ax']**2 + results['ay']**2 + results['az']**2)
        results['j_magnitude'] = np.sqrt(results['jx']**2 + results['jy']**2 + results['jz']**2)
        
        # 曲率和挠率
        results['curvature'] = self.calculate_curvature(results)
        results['torsion'] = self.calculate_torsion(results)
        
        return results
    
    def calculate_curvature(self, data):
        """计算曲率"""
        V_cross_a = np.cross(
            np.column_stack([data['Vx'], data['Vy'], data['Vz']]),
            np.column_stack([data['ax'], data['ay'], data['az']])
        )
        V_cross_a_magnitude = np.linalg.norm(V_cross_a, axis=1)
        
        curvature = (data['V_magnitude']**3) / V_cross_a_magnitude
        return curvature
    
    def calculate_torsion(self, data):
        """计算挠率"""
        V_cross_a = np.cross(
            np.column_stack([data['Vx'], data['Vy'], data['Vz']]),
            np.column_stack([data['ax'], data['ay'], data['az']])
        )
        V_cross_a_dot_j = np.einsum('ij,ij->i', V_cross_a, 
                                   np.column_stack([data['jx'], data['jy'], data['jz']]))
        
        torsion = V_cross_a_dot_j / (np.linalg.norm(V_cross_a, axis=1)**2)
        return torsion
    
    def verify_light_speed_constraint(self, r_val, omega_val, p_val):
        """验证光速约束"""
        theoretical_velocity = np.sqrt(r_val**2 * omega_val**2 + p_val**2)
        error_percent = abs(theoretical_velocity - self.c) / self.c * 100
        constraint_satisfied = error_percent < 1e-10
        
        return {
            'r': r_val,
            'omega': omega_val,
            'p': p_val,
            'theoretical_velocity': theoretical_velocity,
            'light_speed': self.c,
            'error_percent': error_percent,
            'constraint_satisfied': constraint_satisfied,
            'constraint_value': r_val**2 * omega_val**2 + p_val**2,
            'constraint_target': self.c**2
        }
    
    def find_physical_parameters(self, target_frequency=1e15):
        """寻找满足光速约束的物理参数"""
        def equations(params):
            r_val, omega_val = params
            p_val = np.sqrt(self.c**2 - r_val**2 * omega_val**2)
            return [
                omega_val - 2 * np.pi * target_frequency,  # 目标频率约束
                r_val - 1e-8  # 目标尺度约束
            ]
        
        # 初始猜测
        initial_guess = [1e-8, 2*np.pi*target_frequency]
        
        try:
            solution = fsolve(equations, initial_guess)
            r_val, omega_val = solution[0], solution[1]
            p_val = np.sqrt(self.c**2 - r_val**2 * omega_val**2)
            
            return {
                'r': r_val,
                'omega': omega_val,
                'p': p_val,
                'frequency': target_frequency,
                'wavelength': self.c / target_frequency,
                'period': 2 * np.pi / omega_val,
                'verification': self.verify_light_speed_constraint(r_val, omega_val, p_val)
            }
        except:
            return None
    
    def generate_revolution_data(self, r_val=1.0, omega_val=1.0, p_val=1.0):
        """生成转一圈的详细数据"""
        period = 2 * np.pi / omega_val
        time_points = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]) / omega_val
        
        data = []
        for i, t in enumerate(time_points):
            angle = omega_val * t
            x = r_val * np.cos(angle)
            y = r_val * np.sin(angle)
            z = p_val * t
            
            # 计算速度
            vx = -r_val * omega_val * np.sin(angle)
            vy = r_val * omega_val * np.cos(angle)
            vz = p_val
            v_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
            
            # 计算加速度
            ax = -r_val * omega_val**2 * np.cos(angle)
            ay = -r_val * omega_val**2 * np.sin(angle)
            az = 0
            a_magnitude = np.sqrt(ax**2 + ay**2 + az**2)
            
            data.append({
                '阶段': ['起点', '旋转90°', '旋转180°', '旋转270°', '旋转360°'][i],
                '时间(s)': t,
                '角度(rad)': angle,
                'x坐标(m)': x,
                'y坐标(m)': y,
                'z坐标(m)': z,
                '速度x(m/s)': vx,
                '速度y(m/s)': vy,
                '速度z(m/s)': vz,
                '速度模(m/s)': v_magnitude,
                '加速度x(m/s²)': ax,
                '加速度y(m/s²)': ay,
                '加速度z(m/s²)': az,
                '加速度模(m/s²)': a_magnitude
            })
        
        return {
            'trajectory_data': pd.DataFrame(data),
            'period': period,
            'pitch': p_val * period,
            'parameters': {'r': r_val, 'omega': omega_val, 'p': p_val}
        }
    
    def create_derivative_plots(self, r_val=1.0, omega_val=1.0, p_val=1.0):
        """创建求导结果可视化图"""
        data = self.numeric_derivatives(r_val, omega_val, p_val)
        
        fig, axes = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle(f'螺旋运动完整求导分析 (r={r_val}, ω={omega_val}, p={p_val})', fontsize=16)
        
        # 第一行：位置和速度
        # 3D轨迹
        ax1 = fig.add_subplot(3, 3, 1, projection='3d')
        ax1.plot(data['x'], data['y'], data['z'], 'b-', linewidth=2)
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('三维轨迹')
        
        # 速度分量
        ax2 = fig.add_subplot(3, 3, 2)
        ax2.plot(data['t'], data['Vx'], 'r-', label='Vx')
        ax2.plot(data['t'], data['Vy'], 'g-', label='Vy')
        ax2.plot(data['t'], data['Vz'], 'b-', label='Vz')
        ax2.set_xlabel('时间 (s)')
        ax2.set_ylabel('速度 (m/s)')
        ax2.set_title('速度分量')
        ax2.legend()
        ax2.grid(True)
        
        # 速度模
        ax3 = fig.add_subplot(3, 3, 3)
        ax3.plot(data['t'], data['V_magnitude'], 'k-', linewidth=2)
        ax3.axhline(y=np.sqrt(r_val**2 * omega_val**2 + p_val**2), color='r', linestyle='--', 
                   label=f'理论值: {np.sqrt(r_val**2 * omega_val**2 + p_val**2):.3f}')
        ax3.set_xlabel('时间 (s)')
        ax3.set_ylabel('速度模 (m/s)')
        ax3.set_title('速度模（光速约束验证）')
        ax3.legend()
        ax3.grid(True)
        
        # 第二行：加速度
        # 加速度分量
        ax4 = fig.add_subplot(3, 3, 4)
        ax4.plot(data['t'], data['ax'], 'r-', label='ax')
        ax4.plot(data['t'], data['ay'], 'g-', label='ay')
        ax4.plot(data['t'], data['az'], 'b-', label='az')
        ax4.set_xlabel('时间 (s)')
        ax4.set_ylabel('加速度 (m/s²)')
        ax4.set_title('加速度分量')
        ax4.legend()
        ax4.grid(True)
        
        # 加速度模
        ax5 = fig.add_subplot(3, 3, 5)
        ax5.plot(data['t'], data['a_magnitude'], 'k-', linewidth=2)
        ax5.axhline(y=r_val * omega_val**2, color='r', linestyle='--', 
                   label=f'理论值: {r_val * omega_val**2:.3f}')
        ax5.set_xlabel('时间 (s)')
        ax5.set_ylabel('加速度模 (m/s²)')
        ax5.set_title('加速度模')
        ax5.legend()
        ax5.grid(True)
        
        # 速度-加速度相位关系
        ax6 = fig.add_subplot(3, 3, 6)
        ax6.plot(data['Vx'], data['ax'], 'r-', label='Vx-ax')
        ax6.plot(data['Vy'], data['ay'], 'g-', label='Vy-ay')
        ax6.set_xlabel('速度 (m/s)')
        ax6.set_ylabel('加速度 (m/s²)')
        ax6.set_title('速度-加速度相位关系')
        ax6.legend()
        ax6.grid(True)
        
        # 第三行：曲率和挠率
        # 曲率
        ax7 = fig.add_subplot(3, 3, 7)
        ax7.plot(data['t'], data['curvature'], 'b-', linewidth=2)
        theoretical_curvature = (r_val**2 * omega_val**2 + p_val**2) / (r_val * omega_val**2)
        ax7.axhline(y=theoretical_curvature, color='r', linestyle='--', 
                   label=f'理论值: {theoretical_curvature:.3f}')
        ax7.set_xlabel('时间 (s)')
        ax7.set_ylabel('曲率 (1/m)')
        ax7.set_title('曲率半径倒数')
        ax7.legend()
        ax7.grid(True)
        
        # 挠率
        ax8 = fig.add_subplot(3, 3, 8)
        ax8.plot(data['t'], data['torsion'], 'g-', linewidth=2)
        theoretical_torsion = p_val * omega_val / (r_val**2 * omega_val**2 + p_val**2)
        ax8.axhline(y=theoretical_torsion, color='r', linestyle='--', 
                   label=f'理论值: {theoretical_torsion:.3f}')
        ax8.set_xlabel('时间 (s)')
        ax8.set_ylabel('挠率 (rad/m)')
        ax8.set_title('挠率')
        ax8.legend()
        ax8.grid(True)
        
        # 能量分析
        ax9 = fig.add_subplot(3, 3, 9)
        kinetic_energy = 0.5 * data['V_magnitude']**2  # 假设m=1
        ax9.plot(data['t'], kinetic_energy, 'purple', linewidth=2, label='动能')
        ax9.set_xlabel('时间 (s)')
        ax9.set_ylabel('能量 (J/kg)')
        ax9.set_title('动能密度（相对）')
        ax9.legend()
        ax9.grid(True)
        
        plt.tight_layout()
        return fig
    
    def print_symbolic_derivatives(self):
        """打印符号求导结果"""
        results = self.symbolic_derivatives()
        
        print("=" * 60)
        print("张祥前统一场论三维螺旋运动方程 - 符号求导结果")
        print("=" * 60)
        
        print("\n1. 位置矢量:")
        print(f"R(t) = {results['R']}")
        
        print("\n2. 速度矢量（一阶导数）:")
        print(f"V(t) = dR/dt = {results['V']}")
        
        print("\n3. 加速度矢量（二阶导数）:")
        print(f"a(t) = dV/dt = {results['a']}")
        
        print("\n4. 加加速度（三阶导数）:")
        print(f"j(t) = da/dt = {results['j']}")
        
        print("\n5. 速度模:")
        print(f"|V| = {sp.simplify(results['V_magnitude'])}")
        
        print("\n6. 加速度模:")
        print(f"|a| = {sp.simplify(results['a_magnitude'])}")
        
        print("\n7. 光速约束:")
        print(f"|V|² = {sp.simplify(results['light_speed_constraint'])}")
        print("因此约束条件为: r²ω² + p² = c²")
        
        print("\n" + "=" * 60)
    
    def print_numerical_analysis(self, r_val=1.0, omega_val=1.0, p_val=1.0):
        """打印数值分析结果"""
        print("=" * 60)
        print("数值分析结果")
        print("=" * 60)
        
        # 光速约束验证
        constraint_result = self.verify_light_speed_constraint(r_val, omega_val, p_val)
        print(f"\n光速约束验证:")
        print(f"参数: r={r_val}, ω={omega_val}, p={p_val}")
        print(f"理论速度: {constraint_result['theoretical_velocity']:.6f} m/s")
        print(f"光速: {constraint_result['light_speed']:.6f} m/s")
        print(f"误差: {constraint_result['error_percent']:.10f}%")
        print(f"约束满足: {'是' if constraint_result['constraint_satisfied'] else '否'}")
        
        # 理论运动学量
        print(f"\n理论运动学量:")
        print(f"速度模: √(r²ω² + p²) = √({r_val**2 * omega_val**2 + p_val**2}) = {np.sqrt(r_val**2 * omega_val**2 + p_val**2):.6f} m/s")
        print(f"加速度模: rω² = {r_val * omega_val**2:.6f} m/s²")
        print(f"曲率半径: (r²ω² + p²)/(rω²) = {(r_val**2 * omega_val**2 + p_val**2)/(r_val * omega_val**2):.6f} m")
        print(f"挠率: pω/(r²ω² + p²) = {p_val * omega_val/(r_val**2 * omega_val**2 + p_val**2):.6f} rad/m")
        
        # 转一圈数据
        revolution_data = self.generate_revolution_data(r_val, omega_val, p_val)
        print(f"\n转一圈数据:")
        print(f"周期: {revolution_data['period']:.6f} s")
        print(f"螺距: {revolution_data['pitch']:.6f} m")
        
        print("\n" + "=" * 60)
    
    def save_detailed_analysis(self, filename="螺旋运动求导详细分析.txt", r_val=1.0, omega_val=1.0, p_val=1.0):
        """保存详细分析到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            # 符号结果
            results = self.symbolic_derivatives()
            f.write("张祥前统一场论三维螺旋运动方程 - 完整求导分析\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("1. 位置矢量:\n")
            f.write(f"R(t) = {results['R']}\n\n")
            
            f.write("2. 速度矢量（一阶导数）:\n")
            f.write(f"V(t) = dR/dt = {results['V']}\n\n")
            
            f.write("3. 加速度矢量（二阶导数）:\n")
            f.write(f"a(t) = dV/dt = {results['a']}\n\n")
            
            f.write("4. 加加速度（三阶导数）:\n")
            f.write(f"j(t) = da/dt = {results['j']}\n\n")
            
            f.write("5. 速度模:\n")
            f.write(f"|V| = {sp.simplify(results['V_magnitude'])}\n\n")
            
            f.write("6. 加速度模:\n")
            f.write(f"|a| = {sp.simplify(results['a_magnitude'])}\n\n")
            
            f.write("7. 光速约束:\n")
            f.write(f"|V|² = {sp.simplify(results['light_speed_constraint'])}\n")
            f.write("因此约束条件为: r²ω² + p² = c²\n\n")
            
            # 数值分析
            revolution_data = self.generate_revolution_data(r_val, omega_val, p_val)
            f.write(f"数值参数: r={r_val}, ω={omega_val}, p={p_val}\n")
            f.write(f"周期: {revolution_data['period']:.6f} s\n")
            f.write(f"螺距: {revolution_data['pitch']:.6f} m\n\n")
            
            f.write("转一圈详细数据:\n")
            f.write(revolution_data['trajectory_data'].to_string(index=False))

def main():
    """主函数"""
    analyzer = HelicalMotionDerivativeAnalyzer()
    
    # 打印符号求导结果
    analyzer.print_symbolic_derivatives()
    
    # 数值分析
    r, omega, p = 1.0, 1.0, 1.0
    analyzer.print_numerical_analysis(r, omega, p)
    
    # 创建可视化
    print("\n正在生成求导分析图...")
    fig = analyzer.create_derivative_plots(r, omega, p)
    fig.savefig('螺旋运动完整求导分析.png', dpi=300, bbox_inches='tight')
    print("求导分析图已保存为: 螺旋运动完整求导分析.png")
    
    # 保存详细分析
    analyzer.save_detailed_analysis()
    print("详细分析已保存到: 螺旋运动求导详细分析.txt")
    
    # 寻找物理参数示例
    print("\n正在寻找满足光速约束的物理参数...")
    physical_params = analyzer.find_physical_parameters(target_frequency=1e14)  # 红外频率
    if physical_params:
        print(f"找到物理参数:")
        print(f"螺旋半径: {physical_params['r']:.2e} m")
        print(f"角速度: {physical_params['omega']:.2e} rad/s")
        print(f"轴向速度: {physical_params['p']:.2e} m/s")
        print(f"频率: {physical_params['frequency']:.2e} Hz")
        print(f"波长: {physical_params['wavelength']:.2e} m")
        print(f"周期: {physical_params['period']:.2e} s")
    
    # 生成转一圈数据表格
    revolution_data = analyzer.generate_revolution_data(r, omega, p)
    revolution_data['trajectory_data'].to_csv('螺旋运动转一圈完整数据.csv', index=False, encoding='utf-8-sig')
    print("\n转一圈数据已保存到: 螺旋运动转一圈完整数据.csv")
    
    print("\n" + "=" * 60)
    print("螺旋运动求导验证完成！")
    print("=" * 60)
    
    plt.show()
    
    return analyzer

if __name__ == "__main__":
    analyzer = main()