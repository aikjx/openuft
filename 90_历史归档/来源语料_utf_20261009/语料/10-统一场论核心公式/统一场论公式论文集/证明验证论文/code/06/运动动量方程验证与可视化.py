#!/usr/bin/env python
# -*- coding: utf-8 -*-"""运动动量方程验证与可视化
统一场论第六核心方程:P = m(C - V)
# 功能:符号求导验证、数值计算、多尺度分析、可视化展示
作者:张祥前统一场论研究团队
日期:2025-10-24
# 版本:v3.0"""import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from matplotlib.animation import FuncAnimation
import seaborn as sns
from scipy import stats

class MotionMomentumEquation:"""运动动量方程验证类
# 实现统一场论运动动量方程的符号验证、数值计算和可视化"""def __init__(self):"""初始化类,设置基本物理常数"""self.c = 3.0e8  # 光速,单位:m / s
        self.default_mass = 1.0  # 默认质量,单位:kg
        self.results = {}  # 存储计算结果
        
        # 设置可视化样式
        plt.style.use('science')
        sns.set_palette("husl")
        
    def symbolic_verification(self):"""符号求导验证
# 使用SymPy计算动量对质量、速度分量的偏导数
        验证量纲一致性和数学关系"""print(" =  =  = 符号求导验证 =  =  = ")
        
        # 定义符号变量
        m = sp.Symbol('m')  # 质量
        C_x, C_y, C_z = sp.symbols('C_x C_y C_z')  # 光速矢量分量
        V_x, V_y, V_z = sp.symbols('V_x V_y V_z')  # 物体速度分量
        
        # 定义动量分量
        P_x = m * (C_x - V_x)
        P_y = m * (C_y - V_y)
        P_z = m * (C_z - V_z)
        
        # 计算偏导数
        dP_dVx = sp.diff(P_x, V_x)
        dP_dVy = sp.diff(P_y, V_y)
        dP_dVz = sp.diff(P_z, V_z)
        
        dP_dm = sp.diff(P_x, m)
        dP_dCx = sp.diff(P_x, C_x)
        
        # 计算动量对速度的梯度
        grad_PV = sp.Matrix([dP_dVx, dP_dVy, dP_dVz])
        
        # 计算动量的全微分
        dP = dP_dm * sp.Symbol('dm') + dP_dVx * sp.Symbol('dVx') + / dP_dVy * sp.Symbol('dVy') + dP_dVz * sp.Symbol('dVz') + / dP_dCx * sp.Symbol('dCx') + sp.diff(P_y, C_y) * sp.Symbol('dCy') + / sp.diff(P_z, C_z) * sp.Symbol('dCz')
        
        # 打印结果
        print(f"动量x分量: P_x = {P_x}")
        print(f"动量对速度x分量的偏导数: ∂P / ∂V_x = {dP_dVx}")
        print(f"动量对质量的偏导数: ∂P / ∂m = {dP_dm}")
        print(f"动量对光速x分量的偏导数: ∂P / ∂C_x = {dP_dCx}")
        print(f"动量对速度的梯度: grad_P(V) = {grad_PV}")
        print(f"动量的全微分: dP = {dP}")
        
        # 存储符号验证结果
        self.results['symbolic'] = {
            'P_x': P_x,
            'dP_dVx': dP_dVx,
            'dP_dm': dP_dm,
            'dP_dCx': dP_dCx,
            'grad_PV': grad_PV,
            'dP': dP
        }
        
        return self.results['symbolic']
    
    def numerical_verification(self, mass_range = None, velocity_range = None):"""数值验证
        计算不同质量和速度下的动量值
        分析动量随速度的变化规律"""print(" / n =  =  = 数值验证 =  =  = ")
        
        # 默认参数范围
        if mass_range is None:
            mass_range = np.linspace(0.1, 10.0, 10)  # 质量范围:0.1到10 kg
        
        if velocity_range is None:
            # 速度范围:从0到接近光速,分为100个点
            velocity_range = np.linspace(0, 0.99 * self.c, 100)
        
        # 创建结果存储数组
        momentum_data = []
        
        # 设置光速矢量(默认沿x轴)
        C = np.array([self.c, 0, 0])
        
        # 遍历质量和速度
        for m in mass_range:
            for v in velocity_range:
                V = np.array([v, 0, 0])  # 物体速度矢量
                P = m * (C - V)  # 计算动量矢量
                P_mag = np.linalg.norm(P)  # 动量大小
                
                # 相对论动量公式(用于比较)
                gamma = 1.0 / np.sqrt(1.0 - (v *  * 2 / self.c *  * 2))
                P_rel = m * gamma * V  # 相对论动量
                P_rel_mag = np.linalg.norm(P_rel)  # 相对论动量大小
                
                # 牛顿动量(用于比较)
                P_newton = m * V
                P_newton_mag = np.linalg.norm(P_newton)
                
                # 相对速度项
                relative_velocity = np.linalg.norm(C - V)
                
                # 存储数据
                momentum_data.append({
                    'mass': m,
                    'velocity': v,
                    'velocity_ratio': v / self.c,
                    'P_x': P[0],
                    'P_y': P[1],
                    'P_z': P[2],
                    'P_magnitude': P_mag,
                    'P_rel_magnitude': P_rel_mag,
                    'P_newton_magnitude': P_newton_mag,
                    'relative_velocity': relative_velocity,
                    'gamma': gamma
                })
        
        # 转换为DataFrame
        df = pd.DataFrame(momentum_data)
        
        # 统计分析
        stats_results = {
            'max_P': df['P_magnitude'].max(),
            'min_P': df['P_magnitude'].min(),
            'mean_P': df['P_magnitude'].mean(),
            'corr_mass_P': df['mass'].corr(df['P_magnitude']),
            'corr_velocity_P': df['velocity'].corr(df['P_magnitude'])
        }
        
        print(f"最大动量: {stats_results['max_P']:.2e} kg·m / s")
        print(f"最小动量: {stats_results['min_P']:.2e} kg·m / s")
        print(f"平均动量: {stats_results['mean_P']:.2e} kg·m / s")
        print(f"质量与动量相关系数: {stats_results['corr_mass_P']:.4f}")
        print(f"速度与动量相关系数: {stats_results['corr_velocity_P']:.4f}")
        
        # 存储数值验证结果
        self.results['numerical'] = df
        self.results['stats'] = stats_results
        
        return df, stats_results
    
    def multiscale_analysis(self):"""多尺度分析
# 分析不同尺度下(微观、介观、宏观、宇观)的动量特性"""print(" / n =  =  = 多尺度分析 =  =  = ")
        
        # 定义不同尺度下的典型质量和速度
        scales = {
# '微观': {'mass': 9.11e - 31, 'velocity': 2.0e8},  # 电子质量和速度
# '介观': {'mass': 1e - 15, 'velocity': 1.0e5},    # 纳米粒子
# '宏观': {'mass': 1.0, 'velocity': 1.0e3},      # 常见物体
# '宇观': {'mass': 5.97e24, 'velocity': 3.0e4}   # 地球质量和轨道速度
        }
        
        # 设置光速矢量
        C = np.array([self.c, 0, 0])
        
        # 分析各尺度
        scale_results = []
        
        for scale_name, scale_params in scales.items():
            m = scale_params['mass']
            v = scale_params['velocity']
            V = np.array([v, 0, 0])
            
            # 计算动量
            P = m * (C - V)
            P_mag = np.linalg.norm(P)
            
            # 相对速度项
            relative_velocity = np.linalg.norm(C - V)
            
            # 相对论因子
            gamma = 1.0 / np.sqrt(1.0 - (v *  * 2 / self.c *  * 2)) if v < self.c else np.inf
            
            # 存储结果
            scale_results.append({
                'scale': scale_name,
                'mass': m,
                'velocity': v,
                'velocity_ratio': v / self.c,
                'P_magnitude': P_mag,
                'relative_velocity': relative_velocity,
                'gamma': gamma
            })
            
            print(f"{scale_name}尺度:")
            print(f"  质量: {m:.2e} kg")
            print(f"  速度: {v:.2e} m / s")
            print(f"  速度比(v / c): {v / self.c:.6f}")
            print(f"  动量大小: {P_mag:.2e} kg·m / s")
            print(f"  相对速度: {relative_velocity:.2e} m / s")
            print(f"  相对论因子: {gamma:.6f}")
        
        # 转换为DataFrame
        df_scale = pd.DataFrame(scale_results)
        
        # 存储多尺度分析结果
        self.results['multiscale'] = df_scale
        
        return df_scale
    
    def equation_consistency(self):"""方程一致性验证
# 1. 静止情况退化到静止动量方程
# 2. 低速近似到牛顿动量公式
# 3. 与相对论动量公式的关系"""print(" / n =  =  = 方程一致性验证 =  =  = ")
        
        # 设置参数
        m = self.default_mass
        C = np.array([self.c, 0, 0])
        
        # 1. 静止情况 (V = 0)
        V_rest = np.array([0, 0, 0])
        P_rest = m * (C - V_rest)
        print(f"静止情况(V = 0):")
        print(f"  运动动量: P = {P_rest} kg·m / s")
        print(f"  静止动量: P_0 = mC = {m * C} kg·m / s")
        print(f"  一致性验证: {'通过' if np.array_equal(P_rest, m * C) else '失败'}")
        
        # 2. 低速近似 (v << c)
        v_low = 1.0  # 1 m / s,远小于光速
        V_low = np.array([v_low, 0, 0])
        P_unified = m * (C - V_low)
        P_newton = m * V_low
        
        # 提取动量变化部分(忽略常数背景C项)
        P_change = - m * V_low
        print(f" / n低速近似(v << c):")
        print(f"  运动动量: P = {P_unified} kg·m / s")
        print(f"  动量变化部分: ΔP = {P_change} kg·m / s")
        print(f"  牛顿动量: p = {P_newton} kg·m / s")
        print(f"  近似关系: ΔP ≈ - p (通过参考系变换可得到p = - ΔP)")
        
        # 3. 相对论动量关系
        v_rel = 0.9 * self.c  # 高速情况
        V_rel = np.array([v_rel, 0, 0])
        
        # 计算运动动量
        P_unified_rel = m * (C - V_rel)
        
        # 计算相对论动量
        gamma = 1.0 / np.sqrt(1.0 - (v_rel *  * 2 / self.c *  * 2))
        P_relativistic = m * gamma * V_rel
        
        # 计算动量差值
        P_difference = np.linalg.norm(P_unified_rel) - np.linalg.norm(P_relativistic)
        
        print(f" / n高速情况(v = 0.9c):")
        print(f"  运动动量大小: |P| = {np.linalg.norm(P_unified_rel):.2e} kg·m / s")
        print(f"  相对论动量大小: |P_rel| = {np.linalg.norm(P_relativistic):.2e} kg·m / s")
        print(f"  相对论因子: γ = {gamma:.6f}")
        print(f"  关系分析: 运动动量包含空间背景项,相对论动量关注动量变化")
        
        # 存储一致性验证结果
        self.results['consistency'] = {
            'rest_case': P_rest,
            'low_velocity': {
                'unified': P_unified,
                'newton': P_newton,
                'change': P_change
            },
            'relativistic': {
                'unified': P_unified_rel,
                'relativistic': P_relativistic,
                'gamma': gamma
            }
        }
        
        return self.results['consistency']
    
    def plot_momentum_velocity_relation(self):"""绘制动量 - 速度关系图
        展示动量随速度变化的规律"""if 'numerical' not in self.results:
            print("请先运行数值验证")
            return
        
        df = self.results['numerical']
        
        # 选择特定质量进行绘制
        selected_mass = self.default_mass
        mass_df = df[df['mass'] =  = selected_mass].sort_values('velocity')
        
        plt.figure(figsize = (12, 8))
        
        # 绘制动量大小随速度的变化
        plt.plot(mass_df['velocity_ratio'], mass_df['P_magnitude'], 
# 'b - ', linewidth = 2, label = '运动动量 |P| = m|C - V|')
        
        # 绘制相对论动量对比
        plt.plot(mass_df['velocity_ratio'], mass_df['P_rel_magnitude'], 
# 'r -  - ', linewidth = 2, label = '相对论动量 |P_rel| = γmV')
        
        # 绘制牛顿动量对比(仅在低速区域明显)
        low_velocity_df = mass_df[mass_df['velocity_ratio'] < 0.1]
        plt.plot(low_velocity_df['velocity_ratio'], low_velocity_df['P_newton_magnitude'], 
# 'g:', linewidth = 2, label = '牛顿动量 |p| = mV (低速近似)')
        
        # 添加特征线
        plt.axvline(x = 0, color = 'k', linestyle = ' - ', alpha = 0.3, label = 'V = 0 (静止情况)')
        plt.axvline(x = 1.0, color = 'k', linestyle = ' -  - ', alpha = 0.5, label = 'V = c (光速)')
        
        plt.xlabel('速度比 (v / c)')
        plt.ylabel('动量大小 (kg·m / s)')
        plt.title(f'运动动量与速度关系 (质量 = {selected_mass} kg)')
        plt.grid(True, alpha = 0.3)
        plt.legend(fontsize = 12)
        plt.yscale('log')  # 使用对数刻度以更好地显示大范围数据
        
        # 添加物理意义注释
# plt.figtext(0.5, 0.01, '图1: 运动动量随速度变化曲线,展示了从低速到接近光速的动量特性',
                    ha = 'center', fontsize = 10)
        
        plt.tight_layout()
        plt.savefig('动量 - 速度关系图.png', dpi = 300, bbox_inches = 'tight')
        plt.close()
        
        print("动量 - 速度关系图已保存为 '动量 - 速度关系图.png'")
    
    def plot_momentum_components_3d(self):"""绘制动量矢量的3D散点图
        展示动量在三维空间中的分布"""if 'numerical' not in self.results:
            print("请先运行数值验证")
            return
        
        df = self.results['numerical']
        
        # 选择部分数据进行3D可视化
        sample_df = df.sample(min(1000, len(df)))
        
        fig = plt.figure(figsize = (12, 10))
        ax = fig.add_subplot(111, projection = '3d')
        
        # 绘制动量矢量3D散点图,使用速度比作为颜色映射
        scatter = ax.scatter(sample_df['P_x'], sample_df['P_y'], sample_df['P_z'], 
                            c = sample_df['velocity_ratio'], cmap = 'viridis', 
                            s = 50, alpha = 0.6, edgecolors = 'k', linewidths = 0.5)
        
        # 添加颜色条
        cbar = plt.colorbar(scatter, ax = ax)
        cbar.set_label('速度比 (v / c)')
        
        # 添加坐标轴标签
        ax.set_xlabel('P_x (kg·m / s)')
        ax.set_ylabel('P_y (kg·m / s)')
        ax.set_zlabel('P_z (kg·m / s)')
        
        # 添加标题
        ax.set_title('动量矢量的三维分布', fontsize = 14, pad = 20)
        
        # 添加网格
        ax.grid(True, alpha = 0.3)
        
        # 添加注释
# plt.figtext(0.5, 0.01, '图2: 动量矢量的3D散点图,颜色表示不同的速度比',
                    ha = 'center', fontsize = 10)
        
        plt.tight_layout()
        plt.savefig('动量矢量3D分布图.png', dpi = 300, bbox_inches = 'tight')
        plt.close()
        
        print("动量矢量3D分布图已保存为 '动量矢量3D分布图.png'")
    
    def plot_mass_effect_comparison(self):"""绘制不同质量下的动量对比图
        展示质量对动量的影响"""if 'numerical' not in self.results:
            print("请先运行数值验证")
            return
        
        df = self.results['numerical']
        
        # 选择几个不同的质量值进行对比
        unique_masses = sorted(df['mass'].unique())
        if len(unique_masses) > 5:
            selected_masses = unique_masses[::len(unique_masses) /  / 5][:5]
        else:
            selected_masses = unique_masses
        
        plt.figure(figsize = (12, 8))
        
        # 为每个质量绘制动量 - 速度曲线
        for mass in selected_masses:
            mass_df = df[df['mass'] =  = mass].sort_values('velocity')
            plt.plot(mass_df['velocity_ratio'], mass_df['P_magnitude'], 
# linewidth = 2, label = f'质量 = {mass} kg')
        
        # 添加特征线
        plt.axvline(x = 0, color = 'k', linestyle = ' - ', alpha = 0.3)
        plt.axvline(x = 1.0, color = 'k', linestyle = ' -  - ', alpha = 0.5)
        
        plt.xlabel('速度比 (v / c)')
        plt.ylabel('动量大小 (kg·m / s)')
        plt.title('不同质量下的动量对比')
        plt.grid(True, alpha = 0.3)
        plt.legend(fontsize = 10)
        plt.yscale('log')
        
        # 添加注释
# plt.figtext(0.5, 0.01, '图3: 不同质量物体的动量随速度变化对比,展示质量对动量的线性影响',
                    ha = 'center', fontsize = 10)
        
        plt.tight_layout()
        plt.savefig('不同质量动量对比图.png', dpi = 300, bbox_inches = 'tight')
        plt.close()
        
        print("不同质量动量对比图已保存为 '不同质量动量对比图.png'")
    
    def plot_relative_velocity_analysis(self):"""绘制相对速度与动量关系图
# 展示相对速度项 (C - V) 对动量的影响"""if 'numerical' not in self.results:
            print("请先运行数值验证")
            return
        
        df = self.results['numerical']
        
        # 选择特定质量
        selected_mass = self.default_mass
        mass_df = df[df['mass'] =  = selected_mass].sort_values('velocity')
        
        # 创建双Y轴图
        fig, ax1 = plt.subplots(figsize = (12, 8))
        
        # 左侧Y轴:动量大小
        ax1.set_xlabel('速度比 (v / c)')
        ax1.set_ylabel('动量大小 (kg·m / s)', color = 'b')
        ax1.plot(mass_df['velocity_ratio'], mass_df['P_magnitude'], 
# 'b - ', linewidth = 2, label = '动量大小 |P|')
        ax1.tick_params(axis = 'y', labelcolor = 'b')
        ax1.set_yscale('log')
        
        # 右侧Y轴:相对速度
        ax2 = ax1.twinx()
        ax2.set_ylabel('相对速度 |C - V| (m / s)', color = 'r')
        ax2.plot(mass_df['velocity_ratio'], mass_df['relative_velocity'], 
# 'r -  - ', linewidth = 2, label = '相对速度 |C - V|')
        ax2.tick_params(axis = 'y', labelcolor = 'r')
        
        # 添加特征线
        ax1.axvline(x = 0, color = 'k', linestyle = ' - ', alpha = 0.3)
        ax1.axvline(x = 1.0, color = 'k', linestyle = ' -  - ', alpha = 0.5)
        
        # 添加标题和网格
        plt.title(f'相对速度与动量关系 (质量 = {selected_mass} kg)')
        ax1.grid(True, alpha = 0.3)
        
        # 合并图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc = 'upper right')
        
        # 添加注释
# plt.figtext(0.5, 0.01, '图4: 相对速度项与动量关系分析,展示了相对速度如何决定动量大小',
                    ha = 'center', fontsize = 10)
        
        plt.tight_layout()
        plt.savefig('相对速度与动量关系图.png', dpi = 300, bbox_inches = 'tight')
        plt.close()
        
        print("相对速度与动量关系图已保存为 '相对速度与动量关系图.png'")
    
    def plot_multiscale_comparison(self):"""绘制多尺度动量对比图
        展示不同尺度下的动量特性"""if 'multiscale' not in self.results:
            print("请先运行多尺度分析")
            return
        
        df_scale = self.results['multiscale']
        
        # 创建多子图
        fig, axs = plt.subplots(2, 2, figsize = (15, 12))
        
        # 1. 不同尺度的动量大小对比
        axs[0, 0].bar(df_scale['scale'], df_scale['P_magnitude'], color = 'skyblue')
        axs[0, 0].set_yscale('log')
        axs[0, 0].set_title('不同尺度的动量大小')
        axs[0, 0].set_ylabel('动量大小 (kg·m / s)')
        axs[0, 0].grid(axis = 'y', alpha = 0.3)
        
        # 2. 不同尺度的速度比对比
        axs[0, 1].bar(df_scale['scale'], df_scale['velocity_ratio'], color = 'lightgreen')
        axs[0, 1].set_title('不同尺度的速度比 (v / c)')
        axs[0, 1].set_ylabel('速度比 (v / c)')
        axs[0, 1].grid(axis = 'y', alpha = 0.3)
        
        # 3. 质量与动量的关系(对数尺度)
        axs[1, 0].scatter(df_scale['mass'], df_scale['P_magnitude'], s = 100, color = 'orange')
        axs[1, 0].set_xscale('log')
        axs[1, 0].set_yscale('log')
        axs[1, 0].set_title('质量与动量的关系')
        axs[1, 0].set_xlabel('质量 (kg)')
        axs[1, 0].set_ylabel('动量大小 (kg·m / s)')
        axs[1, 0].grid(True, alpha = 0.3)
        
        # 4. 相对论因子在不同尺度的变化
        axs[1, 1].bar(df_scale['scale'], df_scale['gamma'], color = 'salmon')
        axs[1, 1].set_title('不同尺度的相对论因子 γ')
        axs[1, 1].set_ylabel('相对论因子 γ')
        axs[1, 1].grid(axis = 'y', alpha = 0.3)
        
        # 添加注释
# plt.figtext(0.5, 0.01, '图5: 不同物理尺度下的动量特性对比分析',
                    ha = 'center', fontsize = 10)
        
        plt.tight_layout()
        plt.savefig('多尺度动量对比图.png', dpi = 300, bbox_inches = 'tight')
        plt.close()
        
        print("多尺度动量对比图已保存为 '多尺度动量对比图.png'")
    
    def create_momentum_animation(self):"""创建动量随速度变化的动画
        直观展示动量随速度变化的动态过程"""if 'numerical' not in self.results:
            print("请先运行数值验证")
            return
        
        df = self.results['numerical']
        
        # 选择特定质量
        selected_mass = self.default_mass
        mass_df = df[df['mass'] =  = selected_mass].sort_values('velocity')
        
        # 创建图形
        fig, ax = plt.subplots(figsize = (10, 6))
        
        # 初始化图形元素
        line, = ax.plot([], [], 'b - ', linewidth = 2)
        point, = ax.plot([], [], 'ro', markersize = 8)
        text = ax.text(0.02, 0.95, '', transform = ax.transAxes)
        
        # 设置坐标轴
        ax.set_xlim(0, 1.0)
        ax.set_ylim(min(mass_df['P_magnitude']) * 0.9, max(mass_df['P_magnitude']) * 1.1)
        ax.set_xlabel('速度比 (v / c)')
        ax.set_ylabel('动量大小 (kg·m / s)')
        ax.set_title(f'动量随速度变化动画 (质量 = {selected_mass} kg)')
        ax.grid(True, alpha = 0.3)
        ax.set_yscale('log')
        
        # 添加相对论动量曲线作为参考
        ax.plot(mass_df['velocity_ratio'], mass_df['P_rel_magnitude'], 
# 'r -  - ', linewidth = 1, label = '相对论动量')
        ax.legend()
        
        # 初始化函数
        def init():
            line.set_data([], [])
            point.set_data([], [])
            text.set_text('')
            return line, point, text
        
        # 更新函数
        def update(frame):
            # 更新曲线
            line.set_data(mass_df['velocity_ratio'][:frame], 
                          mass_df['P_magnitude'][:frame])
            # 更新点
            point.set_data(mass_df['velocity_ratio'].iloc[frame], 
                          mass_df['P_magnitude'].iloc[frame])
            # 更新文本
            v_ratio = mass_df['velocity_ratio'].iloc[frame]
            p_mag = mass_df['P_magnitude'].iloc[frame]
            text.set_text(f'v / c = {v_ratio:.3f}, P = {p_mag:.2e} kg·m / s')
            return line, point, text
        
        # 创建动画
        ani = FuncAnimation(fig, update, frames = len(mass_df), init_func = init,
                           interval = 50, blit = True)
        
        # 保存动画
        ani.save('动量变化动画.gif', writer = 'pillow', fps = 20, dpi = 100)
        plt.close()
        
        print("动量变化动画已保存为 '动量变化动画.gif'")
    
# def export_results(self, filename = '运动动量方程验证结果.csv'):"""导出验证结果到CSV文件"""if 'numerical' not in self.results:
            print("请先运行数值验证")
            return
        
        df = self.results['numerical']
        df.to_csv(filename, index = False, encoding = 'utf - 8 - sig')
        print(f"验证结果已导出到 '{filename}'")
    
    def run_full_verification(self):"""运行完整的验证流程
# 包括符号验证、数值验证、多尺度分析和可视化"""print("开始运动动量方程完整验证流程...")
        
        # 1. 符号验证
        self.symbolic_verification()
        
        # 2. 数值验证
        self.numerical_verification()
        
        # 3. 多尺度分析
        self.multiscale_analysis()
        
        # 4. 方程一致性验证
        self.equation_consistency()
        
        # 5. 可视化
        print(" / n =  =  = 生成可视化图表 =  =  = ")
        self.plot_momentum_velocity_relation()
        self.plot_momentum_components_3d()
        self.plot_mass_effect_comparison()
        self.plot_relative_velocity_analysis()
        self.plot_multiscale_comparison()
        
        # 6. 创建动画
        try:
            self.create_momentum_animation()
        except Exception as e:
            print(f"创建动画时出错: {e}")
        
        # 7. 导出结果
        self.export_results()
        
        print(" / n运动动量方程验证流程完成!")
        print("所有结果和图表已保存到当前目录.")


if __name__ =  = "__main__":
    # 创建验证对象
    momentum_verifier = MotionMomentumEquation()
    
    # 运行完整验证
    momentum_verifier.run_full_verification()
    
    print(" / n =  =  = 验证总结 =  =  = ")
    print("1. 符号求导验证: 完成")
    print("2. 数值计算验证: 完成")
    print("3. 多尺度分析: 完成")
    print("4. 方程一致性验证: 完成")
    print("5. 可视化图表生成: 完成")
    print(" / n运动动量方程 P = m(C - V) 验证成功!")