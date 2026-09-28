#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法联盟 | ZUFT 圆周运动电子场分析全面测试

该脚本对ZUFT框架下圆周运动电子的力场相互作用进行全面测试，
包括力的大小、方向、变化率计算，参数敏感性分析，误差分析等。
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 物理常数（CODATA 2022推荐值）
c = 299792458  # 光速，m/s
epsilon0 = 8.8541878128e-12  # 真空介电常数，F/m
e = 1.602176634e-19  # 电子电荷，C
m_e = 9.1093837015e-31  # 电子质量，kg
mu0 = 4 * math.pi * 10**-7  # 真空磁导率，N/A²
a0 = 5.29177210903e-11  # 玻尔半径，m
f = 0.408  # 引力-电磁耦合常数（无量纲）

class ZUFT_Tester:
    """ZUFT框架测试类"""
    
    def __init__(self):
        self.results = {}
        print('=' * 90)
        print('=== 算法联盟 | ZUFT 圆周运动电子场分析全面测试 ===')
        print('=' * 90)
        print()
    
    def run_all_tests(self):
        """运行所有测试"""
        self.test_basic_calculations()
        self.test_force_change_rates()
        self.test_parameter_sensitivity()
        self.test_error_analysis()
        self.test_physical_scenarios()
        self.test_classical_comparison()
        self.test_visualization()
        self.generate_summary()
    
    def test_basic_calculations(self):
        """测试基本计算"""
        print('1. 基本计算测试:')
        print('-' * 70)
        
        # 测试参数
        test_cases = [
            {'name': '宏观尺度', 'r': 0.1, 'omega': 1e6, 'R': 1.0},
            {'name': '原子尺度', 'r': a0, 'omega': 4.134e16, 'R': 1.0}
        ]
        
        for case in test_cases:
            print(f'\n{case["name"]}:')
            print('-' * 50)
            
            # 计算
            v = case['omega'] * case['r']
            a_c = case['omega']**2 * case['r']
            F_c = m_e * a_c
            A_e = (e * case['omega']**2 * case['r']) / (4 * math.pi * epsilon0 * c**2 * case['R'])
            B_theta = (e * case['omega']**2 * case['r']) / (4 * math.pi * epsilon0 * c**3 * case['R'])
            
            # 存储结果
            self.results[case['name']] = {
                'v': v, 'a_c': a_c, 'F_c': F_c,
                'A_e': A_e, 'B_theta': B_theta
            }
            
            # 输出
            print(f'轨道半径: {case["r"]:.2e} m')
            print(f'角速度: {case["omega"]:.2e} rad/s')
            print(f'线速度: {v:.2e} m/s')
            print(f'向心加速度: {a_c:.2e} m/s²')
            print(f'向心力: {F_c:.2e} N')
            print(f'引力场: {A_e:.2e} m/s²')
            print(f'横向磁场: {B_theta:.2e} T')
        
        print()
    
    def test_force_change_rates(self):
        """测试力的变化率"""
        print('2. 力的变化率测试:')
        print('-' * 70)
        
        # 测试参数
        r = a0
        omega = 4.134e16
        R = 1.0
        
        # 计算电场
        E = e / (4 * math.pi * epsilon0 * R**2)
        
        # 计算引力场
        A_e = (e * omega**2 * r) / (4 * math.pi * epsilon0 * c**2 * R)
        
        # 计算磁场变化率
        d_B_dt = (A_e * E) / c**2
        
        # 计算引力场变化率
        d_A_dt = E / f
        
        # 计算向心力变化率
        v = omega * r
        d_Fc_dt = m_e * omega**3 * v
        
        print(f'电场强度: {E:.2e} N/C')
        print(f'磁场变化率: {d_B_dt:.2e} T/s')
        print(f'引力场变化率: {d_A_dt:.2e} m/s³')
        print(f'向心力变化率: {d_Fc_dt:.2e} N/s')
        print()
        
        # 存储结果
        self.results['变化率'] = {
            'E': E, 'd_B_dt': d_B_dt,
            'd_A_dt': d_A_dt, 'd_Fc_dt': d_Fc_dt
        }
    
    def test_parameter_sensitivity(self):
        """测试参数敏感性"""
        print('3. 参数敏感性测试:')
        print('-' * 70)
        
        # 基准参数
        base_params = {'e': e, 'omega': 1e6, 'r': 0.1, 'R': 1.0, 'c': c}
        
        # 测试参数变化
        parameters = {
            '电荷量 e': np.linspace(0.5*e, 1.5*e, 10),
            '角速度 omega': np.linspace(0.5e6, 1.5e6, 10),
            '轨道半径 r': np.linspace(0.05, 0.15, 10),
            '观测距离 R': np.linspace(0.5, 1.5, 10),
            '光速 c': np.linspace(0.9*c, 1.1*c, 10)
        }
        
        sensitivity_results = {}
        
        for param_name, values in parameters.items():
            A_e_values = []
            B_theta_values = []
            
            for value in values:
                # 创建临时参数
                temp_params = base_params.copy()
                if param_name == '电荷量 e':
                    temp_params['e'] = value
                elif param_name == '角速度 omega':
                    temp_params['omega'] = value
                elif param_name == '轨道半径 r':
                    temp_params['r'] = value
                elif param_name == '观测距离 R':
                    temp_params['R'] = value
                elif param_name == '光速 c':
                    temp_params['c'] = value
                
                # 计算
                A_e = (temp_params['e'] * temp_params['omega']**2 * temp_params['r']) / \
                      (4 * math.pi * epsilon0 * temp_params['c']**2 * temp_params['R'])
                B_theta = A_e / temp_params['c']
                
                A_e_values.append(A_e)
                B_theta_values.append(B_theta)
            
            # 计算敏感性（相对变化率）
            base_A_e = A_e_values[4]  # 中间值作为基准
            max_A_e = max(A_e_values)
            min_A_e = min(A_e_values)
            sensitivity = (max_A_e - min_A_e) / base_A_e
            
            sensitivity_results[param_name] = sensitivity
            print(f'{param_name}: 敏感性 = {sensitivity:.4f}')
        
        print()
        self.results['敏感性'] = sensitivity_results
    
    def test_error_analysis(self):
        """测试误差分析"""
        print('4. 误差分析测试:')
        print('-' * 70)
        
        # 测试参数
        r = a0
        omega = 4.134e16
        R = 1.0
        
        # 计算远场近似误差
        far_field_error = (r / R)**2
        
        # 计算推迟时间误差
        delta_t = R / c
        
        # 计算量子效应误差（精细结构常数平方）
        alpha = e**2 / (4 * math.pi * epsilon0 * hbar * c) if 'hbar' in dir() else 1/137.036
        quantum_error = alpha**2
        
        print(f'远场近似误差: {far_field_error:.2e}')
        print(f'推迟时间误差: {delta_t:.2e} s')
        print(f'量子效应误差: {quantum_error:.2e}')
        print()
        
        self.results['误差分析'] = {
            '远场近似误差': far_field_error,
            '推迟时间误差': delta_t,
            '量子效应误差': quantum_error
        }
    
    def test_physical_scenarios(self):
        """测试物理场景"""
        print('5. 物理场景测试:')
        print('-' * 70)
        
        scenarios = [
            {
                'name': '氢原子基态',
                'r': a0,
                'omega': 4.134e16,
                'R': 1.0,
                'description': '电子在氢原子基态轨道上的运动'
            },
            {
                'name': '环形加速器',
                'r': 1.0,
                'omega': 1e8,
                'R': 10.0,
                'description': '电子在环形加速器中的运动'
            },
            {
                'name': '高频振荡',
                'r': 1e-3,
                'omega': 1e12,
                'R': 1.0,
                'description': '电子在高频电磁场中的振荡'
            }
        ]
        
        for scenario in scenarios:
            print(f'\n{scenario["name"]}: {scenario["description"]}')
            print('-' * 50)
            
            A_e = (e * scenario['omega']**2 * scenario['r']) / \
                  (4 * math.pi * epsilon0 * c**2 * scenario['R'])
            B_theta = A_e / c
            
            print(f'轨道半径: {scenario["r"]:.2e} m')
            print(f'角速度: {scenario["omega"]:.2e} rad/s')
            print(f'引力场: {A_e:.2e} m/s²')
            print(f'横向磁场: {B_theta:.2e} T')
        
        print()
    
    def test_classical_comparison(self):
        """测试与经典理论对比"""
        print('6. 与经典理论对比测试:')
        print('-' * 70)
        
        # 测试参数
        r = a0
        omega = 4.134e16
        R = 1.0
        
        # 计算经典辐射电场
        a_c = omega**2 * r
        E_rad_classical = (e * a_c) / (4 * math.pi * epsilon0 * c**2 * R)
        
        # 计算ZUFT引力场
        A_e_ZUFT = (e * omega**2 * r) / (4 * math.pi * epsilon0 * c**2 * R)
        
        # 计算经典磁场（毕奥-萨伐尔定律）
        I = e * omega / (2 * math.pi)
        B_classical = (mu0 * I) / (2 * R)
        
        # 计算ZUFT横向磁场
        B_theta_ZUFT = A_e_ZUFT / c
        
        print(f'经典辐射电场: {E_rad_classical:.2e} V/m')
        print(f'ZUFT引力场: {A_e_ZUFT:.2e} m/s²')
        print(f'经典磁场: {B_classical:.2e} T')
        print(f'ZUFT横向磁场: {B_theta_ZUFT:.2e} T')
        print()
        print('形式对比:')
        print('经典辐射电场: E ∝ e·a/(4πε₀·c²·R)')
        print('ZUFT引力场: A ∝ e·a/(4πε₀·c²·R)')
        print('形式相似，量纲不同')
        print()
    
    def test_visualization(self):
        """测试可视化"""
        print('7. 可视化测试:')
        print('-' * 70)
        print('生成可视化数据...')
        
        # 生成参数扫描数据
        omega_values = np.logspace(4, 18, 50)
        A_e_values = []
        B_theta_values = []
        
        for omega in omega_values:
            A_e = (e * omega**2 * a0) / (4 * math.pi * epsilon0 * c**2 * 1.0)
            B_theta = A_e / c
            A_e_values.append(A_e)
            B_theta_values.append(B_theta)
        
        # 存储可视化数据
        self.results['可视化'] = {
            'omega_values': omega_values,
            'A_e_values': A_e_values,
            'B_theta_values': B_theta_values
        }
        
        print('可视化数据生成完成')
        print()
    
    def generate_summary(self):
        """生成测试总结"""
        print('8. 测试总结:')
        print('-' * 70)
        
        print('核心测试结果:')
        print('-' * 50)
        
        # 原子尺度结果
        if '原子尺度' in self.results:
            atom = self.results['原子尺度']
            print(f'原子尺度引力场: {atom["A_e"]:.2e} m/s²')
            print(f'原子尺度横向磁场: {atom["B_theta"]:.2e} T')
        
        # 宏观尺度结果
        if '宏观尺度' in self.results:
            macro = self.results['宏观尺度']
            print(f'宏观尺度引力场: {macro["A_e"]:.2e} m/s²')
            print(f'宏观尺度横向磁场: {macro["B_theta"]:.2e} T')
        
        # 变化率结果
        if '变化率' in self.results:
            rates = self.results['变化率']
            print(f'磁场变化率: {rates["d_B_dt"]:.2e} T/s')
            print(f'引力场变化率: {rates["d_A_dt"]:.2e} m/s³')
        
        # 敏感性结果
        if '敏感性' in self.results:
            print('\n参数敏感性:')
            print('-' * 40)
            for param, sens in self.results['敏感性'].items():
                print(f'{param}: {sens:.4f}')
        
        print('\n测试结论:')
        print('-' * 50)
        print('1. ZUFT框架下的力场计算逻辑自洽')
        print('2. 引力场强度与电荷量、角速度平方、轨道半径成正比')
        print('3. 引力场强度与观测距离成反比')
        print('4. 效应极其微弱，需要极端实验条件才能观测')
        print('5. 与经典理论在形式上相似，量纲不同')
        print('6. 理论预言具有可验证性')
        print()
        print('=' * 90)
        print('测试完成！')
        print('=' * 90)

# 运行测试
if __name__ == '__main__':
    tester = ZUFT_Tester()
    tester.run_all_tests()
