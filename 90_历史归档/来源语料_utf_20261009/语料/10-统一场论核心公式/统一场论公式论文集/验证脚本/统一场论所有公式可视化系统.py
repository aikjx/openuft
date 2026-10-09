#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论所有公式可视化系统
功能：对统一场论18个核心公式进行交互式可视化展示
作者：张祥前统一场论研究团队
日期：2025-10-26
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_pdf import PdfPages
import os
import json
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Microsoft YaHei', 'Arial', 'DejaVu Sans']  # 提供多种字体支持
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

class 统一场论公式可视化系统:
    def __init__(self):
        # 数据目录
        self.data_dir = 'd:/a10/aikjx/code/my_lib/utf/11-统一场论公式论文集/验证数据'
        self.output_dir = 'd:/a10/aikjx/code/my_lib/utf/11-统一场论公式论文集/所有公式可视化'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 18个核心公式信息
        self.formulas = [
            {
                'id': 1,
                'name': '时空同一化方程',
                'formula': 'r(t) = C·t',
                'description': '空间坐标与时间成线性关系，表明空间以光速向四周传播',
                'physics_meaning': '揭示了时空的统一性，光速是空间本身的运动速度',
                'color': '#1f77b4',
                'icon': '🌀',
                'type': '时空方程'
            },
            {
                'id': 2,
                'name': '三维螺旋时空方程',
                'formula': 'x = Rcos(ωt), y = Rsin(ωt), z = vt',
                'description': '物体在空间中的螺旋运动轨迹',
                'physics_meaning': '解释了物质粒子的波动性和螺旋运动本质',
                'color': '#ff7f0e',
                'icon': '🧬',
                'type': '时空方程'
            },
            {
                'id': 3,
                'name': '质量定义方程',
                'formula': 'm = k·n/r²',
                'description': '质量与空间位移条数密度的平方反比关系',
                'physics_meaning': '揭示了质量的本质是空间的运动效应',
                'color': '#2ca02c',
                'icon': '⚖️',
                'type': '场方程'
            },
            {
                'id': 4,
                'name': '引力场定义方程',
                'formula': 'A = -G·M/r²',
                'description': '引力场强度与质量成正比，与距离平方成反比',
                'physics_meaning': '统一了牛顿万有引力定律，揭示引力本质',
                'color': '#d62728',
                'icon': '🌌',
                'type': '场方程'
            },
            {
                'id': 5,
                'name': '静止动量方程',
                'formula': 'P₀ = m₀c',
                'description': '静止物体的动量等于质量乘以光速',
                'physics_meaning': '揭示了静止物体内部的运动本质',
                'color': '#9467bd',
                'icon': '🏃‍♂️',
                'type': '动力学方程'
            },
            {
                'id': 6,
                'name': '运动动量方程',
                'formula': 'P = m₀v/√(1-v²/c²)',
                'description': '运动物体的动量公式',
                'physics_meaning': '与相对论动量公式一致，验证了理论自洽性',
                'color': '#8c564b',
                'icon': '🚀',
                'type': '动力学方程'
            },
            {
                'id': 7,
                'name': '宇宙大统一方程',
                'formula': 'F = ma = dp/dt',
                'description': '力、加速度、动量变化率的统一关系',
                'physics_meaning': '宇宙中所有力的统一描述',
                'color': '#e377c2',
                'icon': '🌍',
                'type': '统一方程'
            },
            {
                'id': 8,
                'name': '空间波动方程',
                'formula': '∇²ψ - (1/c²)∂²ψ/∂t² = 0',
                'description': '空间的波动传播方程',
                'physics_meaning': '解释了电磁波和物质波的本质',
                'color': '#7f7f7f',
                'icon': '🌊',
                'type': '场方程'
            },
            {
                'id': 9,
                'name': '电荷定义方程',
                'formula': 'Q = ∫ρdV',
                'description': '电荷是空间旋转运动的表现',
                'physics_meaning': '揭示了电荷的本质是空间的运动状态',
                'color': '#bcbd22',
                'icon': '⚡',
                'type': '场方程'
            },
            {
                'id': 10,
                'name': '电场定义方程',
                'formula': 'E = F/q',
                'description': '电场强度等于作用力除以电荷量',
                'physics_meaning': '统一了电场的定义和本质',
                'color': '#17becf',
                'icon': '🔌',
                'type': '场方程'
            },
            {
                'id': 11,
                'name': '磁场定义方程',
                'formula': 'B = F/(qv)',
                'description': '磁场强度与电荷运动相关',
                'physics_meaning': '解释了磁场的本质是空间的旋转运动',
                'color': '#ffbc79',
                'icon': '🧲',
                'type': '场方程'
            },
            {
                'id': 12,
                'name': '变化的引力场产生电磁场方程',
                'formula': '∇×E = -∂B/∂t',
                'description': '法拉第电磁感应定律的统一形式',
                'physics_meaning': '揭示了引力场和电磁场的相互转化关系',
                'color': '#c5b0d5',
                'icon': '🔄',
                'type': '统一方程'
            },
            {
                'id': 13,
                'name': '磁矢势方程',
                'formula': 'B = ∇×A',
                'description': '磁场是磁矢势的旋度',
                'physics_meaning': '统一了磁场的矢量描述',
                'color': '#c49c94',
                'icon': '🧭',
                'type': '场方程'
            },
            {
                'id': 14,
                'name': '变化的引力场产生电场方程',
                'formula': '∇·E = ρ/ε₀',
                'description': '高斯电场定理的统一形式',
                'physics_meaning': '解释了电荷如何产生电场',
                'color': '#dbdb8d',
                'icon': '⚡🌌',
                'type': '统一方程'
            },
            {
                'id': 15,
                'name': '变化的磁场产生引力场和电场方程',
                'formula': '∇×B = μ₀J + μ₀ε₀∂E/∂t',
                'description': '安培-麦克斯韦方程的统一形式',
                'physics_meaning': '揭示了电磁现象和引力现象的统一性',
                'color': '#9edae5',
                'icon': '🧲🌌',
                'type': '统一方程'
            },
            {
                'id': 16,
                'name': '统一场论能量方程',
                'formula': 'E = mc²',
                'description': '能量与质量的等价关系',
                'physics_meaning': '揭示了能量的本质是物质的运动',
                'color': '#ff9896',
                'icon': '💥',
                'type': '动力学方程'
            },
            {
                'id': 17,
                'name': '引力场与电磁场的统一方程',
                'formula': 'A·E = k',
                'description': '引力场与电场的乘积为常数',
                'physics_meaning': '直接统一了引力和电磁力',
                'color': '#aec7e8',
                'icon': '🔗',
                'type': '统一方程'
            },
            {
                'id': 18,
                'name': '核力场定义方程',
                'formula': 'F = k e^(-λr)/r²',
                'description': '核力场强度与距离的指数衰减平方反比关系',
                'physics_meaning': '解释了核力的短程特性',
                'color': '#ffbb78',
                'icon': '⚛️',
                'type': '场方程'
            }
        ]
    
    def 生成公式概览图(self):
        """生成所有公式的概览图表"""
        # 创建公式类型分布饼图
        plt.figure(figsize=(12, 10))
        
        # 统计不同类型的公式数量
        type_counts = {}
        for formula in self.formulas:
            formula_type = formula['type']
            type_counts[formula_type] = type_counts.get(formula_type, 0) + 1
        
        # 绘制饼图
        plt.subplot(2, 1, 1)
        labels = list(type_counts.keys())
        sizes = list(type_counts.values())
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, shadow=True)
        plt.axis('equal')
        plt.title('统一场论18个核心公式类型分布', fontsize=16)
        
        # 绘制公式类型数量柱状图
        plt.subplot(2, 1, 2)
        plt.bar(range(len(type_counts)), sizes, tick_label=labels, color=colors)
        plt.title('不同类型公式数量统计', fontsize=14)
        plt.xlabel('公式类型')
        plt.ylabel('公式数量')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/公式类型分布.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"公式类型分布图已保存到: {self.output_dir}/公式类型分布.png")
    
    def 可视化所有公式(self):
        """为所有18个公式生成可视化图表"""
        print("开始生成所有公式的可视化图表...")
        
        # 为每个公式生成可视化
        for formula in self.formulas:
            formula_id = formula['id']
            formula_name = formula['name']
            formula_text = formula['formula']
            
            try:
                # 检查是否有对应的CSV数据文件
                csv_file = f'{self.data_dir}/方程{formula_id:02d}_{formula_name}验证数据.csv'
                
                if os.path.exists(csv_file):
                    # 使用实际验证数据进行可视化
                    df = pd.read_csv(csv_file)
                    self._可视化单个公式_with_data(formula, df)
                else:
                    # 生成模拟数据进行可视化
                    self._可视化单个公式_with_simulation(formula)
                    
                print(f"公式{formula_id:02d} ({formula_name}) 可视化完成")
            except Exception as e:
                print(f"公式{formula_id:02d} ({formula_name}) 可视化失败: {e}")
    
    def _可视化单个公式_with_data(self, formula, df):
        """使用实际验证数据可视化单个公式"""
        formula_id = formula['id']
        formula_name = formula['name']
        formula_text = formula['formula']
        color = formula['color']
        
        # 创建可视化图表
        plt.figure(figsize=(12, 8))
        
        # 根据公式类型选择可视化方式
        if formula_id == 1:  # 时空同一化方程
            plt.subplot(2, 1, 1)
            plt.plot(df['时间(t)'], df['速度大小'], color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('时间 (s)')
            plt.ylabel('速度大小 (m/s)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
            plt.subplot(2, 1, 2)
            plt.plot(df['时间(t)'], df['位置x'], 'r-', label='X方向', linewidth=1.5)
            plt.plot(df['时间(t)'], df['位置y'], 'g-', label='Y方向', linewidth=1.5)
            plt.plot(df['时间(t)'], df['位置z'], 'b-', label='Z方向', linewidth=1.5)
            plt.xlabel('时间 (s)')
            plt.ylabel('位置坐标 (m)')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 2:  # 三维螺旋时空方程
            plt.subplot(2, 1, 1)
            plt.plot(df['位置x'], df['位置y'], color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('X位置 (m)')
            plt.ylabel('Y位置 (m)')
            plt.axis('equal')
            plt.grid(True, linestyle='--', alpha=0.7)
            
            plt.subplot(2, 1, 2)
            radius = np.sqrt(df['位置x']**2 + df['位置y']**2 + df['位置z']**2)
            plt.plot(df['时间(t)'], radius, color=color, linewidth=2)
            plt.xlabel('时间 (s)')
            plt.ylabel('半径 (m)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 3:  # 质量定义方程
            plt.subplot(2, 1, 1)
            plt.plot(df['距离(r)'], df['质量(m)'], color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('距离 (m)')
            plt.ylabel('质量 (kg)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
            plt.subplot(2, 1, 2)
            plt.loglog(df['距离(r)'], df['质量(m)'], color=color, linewidth=2)
            plt.xlabel('距离 (m)')
            plt.ylabel('质量 (kg)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 4:  # 引力场定义方程
            plt.plot(df['距离(r)'], df['引力场强度(A)'], color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('距离 (m)')
            plt.ylabel('引力场强度 (m/s²)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 17:  # 引力场与电磁场的统一方程
            plt.scatter(df['引力场(A)'], df['电场(E)'], color=color, alpha=0.6, s=50)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('引力场强度 (A)')
            plt.ylabel('电场强度 (E)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        else:  # 其他公式的通用可视化
            # 尝试绘制第一列和第二列的关系
            if len(df.columns) >= 2:
                plt.plot(df.iloc[:, 0], df.iloc[:, 1], color=color, linewidth=2)
                plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
                plt.xlabel(df.columns[0])
                plt.ylabel(df.columns[1])
                plt.grid(True, linestyle='--', alpha=0.7)
            else:
                plt.text(0.5, 0.5, f'公式: {formula_text}\n{formula["description"]}',
                         horizontalalignment='center', verticalalignment='center',
                         fontsize=12, transform=plt.gca().transAxes)
                plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
        
        # 添加公式文本
        plt.figtext(0.5, 0.01, f'公式: {formula_text}', ha='center', fontsize=12, bbox=dict(facecolor='yellow', alpha=0.3))
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        plt.savefig(f'{self.output_dir}/公式{formula_id:02d}_{formula_name}.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _可视化单个公式_with_simulation(self, formula):
        """使用模拟数据可视化单个公式"""
        formula_id = formula['id']
        formula_name = formula['name']
        formula_text = formula['formula']
        color = formula['color']
        
        plt.figure(figsize=(12, 8))
        
        # 根据公式类型生成模拟数据
        if formula_id == 5:  # 静止动量方程
            # P0 = m0c
            m_values = np.linspace(0, 1, 100)
            c = 3e8  # 光速
            p_values = m_values * c
            
            plt.plot(m_values, p_values, color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('质量 (kg)')
            plt.ylabel('静止动量 (kg·m/s)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 6:  # 运动动量方程
            # P = m0v/√(1-v²/c²)
            v_values = np.linspace(0, 0.99*3e8, 100)
            m0 = 1  # 静止质量
            c = 3e8  # 光速
            p_values = m0 * v_values / np.sqrt(1 - (v_values/c)**2)
            
            plt.plot(v_values/c, p_values, color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('速度/光速 (v/c)')
            plt.ylabel('动量 (kg·m/s)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 8:  # 空间波动方程
            # 模拟波动
            x = np.linspace(0, 10, 1000)
            t = 0
            y = np.sin(x - 3e8*t)  # 行波解
            
            plt.plot(x, y, color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('位置 (m)')
            plt.ylabel('波动振幅')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 16:  # 能量方程
            # E = mc²
            m_values = np.linspace(0, 1e-3, 100)  # 从0到1克
            c = 3e8  # 光速
            e_values = m_values * c**2
            
            plt.plot(m_values, e_values, color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('质量 (kg)')
            plt.ylabel('能量 (J)')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        elif formula_id == 18:  # 核力场定义方程
            # F = k e^(-λr)/r²
            r_values = np.linspace(0.1, 10, 100)
            k = 1
            λ = 1
            f_values = k * np.exp(-λ*r_values) / r_values**2
            
            plt.plot(r_values, f_values, color=color, linewidth=2)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
            plt.xlabel('距离 (m)')
            plt.ylabel('核力场强度')
            plt.grid(True, linestyle='--', alpha=0.7)
            
        else:  # 其他公式的默认可视化
            plt.text(0.5, 0.5, f'公式: {formula_text}\n{formula["description"]}\n{formula["physics_meaning"]}',
                     horizontalalignment='center', verticalalignment='center',
                     fontsize=12, transform=plt.gca().transAxes)
            plt.title(f'公式{formula_id:02d}: {formula_name}', fontsize=14)
        
        # 添加公式类型和物理意义
        plt.figtext(0.5, 0.01, f'公式类型: {formula["type"]}', ha='center', fontsize=10, bbox=dict(facecolor='lightblue', alpha=0.3))
        plt.figtext(0.5, 0.05, f'公式: {formula_text}', ha='center', fontsize=12, bbox=dict(facecolor='yellow', alpha=0.3))
        
        plt.tight_layout(rect=[0, 0.1, 1, 0.97])
        plt.savefig(f'{self.output_dir}/公式{formula_id:02d}_{formula_name}.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def 生成公式关系网络(self):
        """生成公式之间的关系网络可视化"""
        plt.figure(figsize=(14, 12))
        
        # 定义公式之间的关系（示例）
        relationships = [
            (1, 2),  # 时空同一化方程 → 三维螺旋时空方程
            (1, 16), # 时空同一化方程 → 能量方程
            (3, 4),  # 质量定义方程 → 引力场定义方程
            (5, 6),  # 静止动量方程 → 运动动量方程
            (4, 17), # 引力场定义方程 → 引力场与电磁场的统一方程
            (10, 17),# 电场定义方程 → 引力场与电磁场的统一方程
            (14, 15) # 变化的引力场产生电场方程 → 变化的磁场产生引力场和电场方程
        ]
        
        # 创建公式位置（使用圆形布局）
        n = len(self.formulas)
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        x = np.cos(angles) * 10
        y = np.sin(angles) * 10
        
        # 绘制关系连接线
        for src, dest in relationships:
            plt.plot([x[src-1], x[dest-1]], [y[src-1], y[dest-1]], 'k-', alpha=0.3, zorder=1)
        
        # 绘制公式节点
        type_colors = {'时空方程': '#1f77b4', '动力学方程': '#ff7f0e', '场方程': '#2ca02c', '统一方程': '#d62728'}
        
        for i, formula in enumerate(self.formulas):
            color = type_colors[formula['type']]
            plt.scatter(x[i], y[i], s=200, color=color, alpha=0.8, edgecolors='black', zorder=2)
            plt.text(x[i], y[i], f"{formula['id']}", ha='center', va='center', fontsize=10, fontweight='bold', zorder=3)
        
        # 添加图例
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                                      label=formula_type, markersize=10) 
                          for formula_type, color in type_colors.items()]
        plt.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.5, -0.05), ncol=4)
        
        plt.title('统一场论18个核心公式关系网络图', fontsize=18)
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/公式关系网络图.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"公式关系网络图已保存到: {self.output_dir}/公式关系网络图.png")
    
    def 生成公式家族树(self):
        """生成公式的家族树结构"""
        plt.figure(figsize=(16, 12))
        
        # 定义公式家族树结构（层级关系）
        levels = [
            [1],           # 第1层：基础方程
            [2, 3, 5],     # 第2层：核心推导方程
            [4, 6, 8, 9, 16],  # 第3层：应用方程
            [10, 11, 12, 13, 14, 15, 17, 18]  # 第4层：具体场方程
        ]
        
        # 绘制家族树
        max_levels = len(levels)
        max_nodes = max(len(layer) for layer in levels)
        
        y_step = 1 / max_levels
        
        # 存储节点位置
        node_positions = {}
        
        # 绘制节点
        for level_idx, layer in enumerate(levels):
            y_pos = 1 - level_idx * y_step - y_step/2
            x_step = 1 / max_nodes
            offset = (1 - len(layer) * x_step) / 2
            
            for node_idx, formula_id in enumerate(layer):
                x_pos = offset + node_idx * x_step
                node_positions[formula_id] = (x_pos, y_pos)
                
                # 获取公式信息
                formula = next(f for f in self.formulas if f['id'] == formula_id)
                color = formula['color']
                
                # 绘制节点
                plt.scatter(x_pos, y_pos, s=300, color=color, alpha=0.8, edgecolors='black', zorder=3)
                plt.text(x_pos, y_pos, f"{formula_id}", ha='center', va='center', fontsize=10, fontweight='bold', zorder=4)
        
        # 定义层级间的连接关系
        connections = [
            (1, 2), (1, 3), (1, 5),  # 第1层到第2层
            (2, 8), (2, 12), (3, 4), (3, 9), (5, 6), (5, 16),  # 第2层到第3层
            (4, 14), (4, 17), (8, 13), (9, 10), (9, 11), (12, 15), (16, 18)  # 第3层到第4层
        ]
        
        # 绘制连接线
        for src, dest in connections:
            if src in node_positions and dest in node_positions:
                x1, y1 = node_positions[src]
                x2, y2 = node_positions[dest]
                plt.plot([x1, x2], [y1, y2], 'k-', alpha=0.5, linewidth=1.5, zorder=2)
        
        # 添加公式名称标签
        for formula_id, (x, y) in node_positions.items():
            formula = next(f for f in self.formulas if f['id'] == formula_id)
            plt.text(x, y-0.03, f"{formula['name'][:6]}...", ha='center', va='top', fontsize=8, zorder=4)
        
        plt.title('统一场论18个核心公式家族树结构', fontsize=18)
        plt.xlim(-0.1, 1.1)
        plt.ylim(-0.1, 1.1)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/公式家族树.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"公式家族树已保存到: {self.output_dir}/公式家族树.png")
    
    def 生成综合HTML可视化报告(self):
        """生成综合HTML可视化报告"""
        html_file = f'{self.output_dir}/统一场论18核心公式可视化报告.html'
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>统一场论18核心公式可视化报告</title>
    <link href="https://cdn.jsdelivr.net/npm/antd@5.0.0/dist/reset.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #1a1a2e;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 1.2em;
        }}
        .overview-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .overview-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .overview-card:hover {{
            transform: translateY(-5px);
        }}
        .overview-card h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
        }}
        .overview-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        .chart-container {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }}
        .chart {{
            width: 100%;
            height: 400px;
        }}
        .formula-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 40px;
        }}
        .formula-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 4px solid #3498db;
        }}
        .formula-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }}
        .formula-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .formula-number {{
            background: #3498db;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        .formula-type {{
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        .type-spacetime {{
            background: #1f77b4;
            color: white;
        }}
        .type-dynamic {{
            background: #ff7f0e;
            color: white;
        }}
        .type-field {{
            background: #2ca02c;
            color: white;
        }}
        .type-unified {{
            background: #d62728;
            color: white;
        }}
        .formula-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin: 10px 0;
        }}
        .formula-text {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            margin: 10px 0;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        .formula-description, .formula-physics {{
            color: #666;
            margin: 8px 0;
            line-height: 1.5;
        }}
        .formula-image {{
            margin-top: 15px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e9ecef;
        }}
        .formula-image img {{
            width: 100%;
            height: auto;
            transition: transform 0.3s ease;
        }}
        .formula-image img:hover {{
            transform: scale(1.05);
        }}
        .navigation {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .navigation h2 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .navigation-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .nav-button {{
            padding: 8px 16px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        .nav-button:hover {{
            background: #2980b9;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            color: #666;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌀 统一场论18核心公式可视化报告</h1>
            <p>基于数学验证的统一场论核心公式完整展示</p>
            <p>生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </div>
        
        <div class="overview-section">
            <div class="overview-card">
                <h3>总公式数量</h3>
                <div class="number">18</div>
            </div>
            <div class="overview-card">
                <h3>时空方程</h3>
                <div class="number" style="color: #1f77b4;">2</div>
            </div>
            <div class="overview-card">
                <h3>动力学方程</h3>
                <div class="number" style="color: #ff7f0e;">4</div>
            </div>
            <div class="overview-card">
                <h3>场方程</h3>
                <div class="number" style="color: #2ca02c;">8</div>
            </div>
            <div class="overview-card">
                <h3>统一方程</h3>
                <div class="number" style="color: #d62728;">4</div>
            </div>
        </div>
        
        <div class="chart-grid">
            <div class="chart-container">
                <div class="chart-title">公式类型分布</div>
                <div id="formulaTypeChart" class="chart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title">公式重要性关系</div>
                <div id="formulaRelationChart" class="chart"></div>
            </div>
        </div>
        
        <div class="navigation">
            <h2>快速导航</h2>
            <div class="navigation-buttons">
                <button class="nav-button" onclick="scrollToSection('formula1')">公式01：时空同一化方程</button>
                <button class="nav-button" onclick="scrollToSection('formula2')">公式02：三维螺旋时空方程</button>
                <button class="nav-button" onclick="scrollToSection('formula3')">公式03：质量定义方程</button>
                <button class="nav-button" onclick="scrollToSection('formula4')">公式04：引力场定义方程</button>
                <button class="nav-button" onclick="scrollToSection('formula17')">公式17：引力场与电磁场的统一方程</button>
            </div>
        </div>
        
        <div class="formula-grid">
''')
            
            # 生成每个公式的卡片
            for formula in self.formulas:
                formula_id = formula['id']
                formula_name = formula['name']
                formula_text = formula['formula']
                description = formula['description']
                physics_meaning = formula['physics_meaning']
                formula_type = formula['type']
                icon = formula['icon']
                
                # 根据公式类型设置CSS类
                type_class = {
                    '时空方程': 'type-spacetime',
                    '动力学方程': 'type-dynamic',
                    '场方程': 'type-field',
                    '统一方程': 'type-unified'
                }[formula_type]
                
                f.write(f'''
            <div class="formula-card" id="formula{formula_id}">
                <div class="formula-header">
                    <div class="formula-number">{formula_id}</div>
                    <span class="formula-type {type_class}">{formula_type}</span>
                </div>
                <div class="formula-icon" style="font-size: 2em; margin-bottom: 10px;">{icon}</div>
                <div class="formula-name">{formula_name}</div>
                <div class="formula-text">{formula_text}</div>
                <div class="formula-description"><strong>公式描述：</strong>{description}</div>
                <div class="formula-physics"><strong>物理意义：</strong>{physics_meaning}</div>
                <div class="formula-image">
                    <img src="公式{formula_id:02d}_{formula_name}.png" alt="{formula_name}可视化">
                </div>
            </div>
''')
            
            f.write('''
        </div>
        
        <div class="footer">
            <p>© 2025 张祥前统一场论研究团队 | 基于Python和Matplotlib生成的可视化报告</p>
        </div>
    </div>
    
    <script>
        // 初始化公式类型分布图
        var typeChart = echarts.init(document.getElementById('formulaTypeChart'));
        var typeOption = {
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            legend: {
                top: 'bottom'
            },
            series: [
                {
                    name: '公式类型',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: 20,
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: [
                        { value: 2, name: '时空方程', itemStyle: { color: '#1f77b4' } },
                        { value: 4, name: '动力学方程', itemStyle: { color: '#ff7f0e' } },
                        { value: 8, name: '场方程', itemStyle: { color: '#2ca02c' } },
                        { value: 4, name: '统一方程', itemStyle: { color: '#d62728' } }
                    ]
                }
            ]
        };
        typeChart.setOption(typeOption);
        
        // 初始化公式关系图
        var relationChart = echarts.init(document.getElementById('formulaRelationChart'));
        var relationOption = {
            tooltip: {},
            legend: [{
                data: ['时空方程', '动力学方程', '场方程', '统一方程']
            }],
            animationDurationUpdate: 1500,
            animationEasingUpdate: 'quinticInOut',
            series: [{
                type: 'graph',
                layout: 'force',
                force: {
                    repulsion: 300,
                    edgeLength: [80, 120]
                },
                roam: true,
                label: {
                    show: true,
                    formatter: '{c}'
                },
                data: [
                    { name: '1', value: '时空同一化方程', category: '时空方程', symbolSize: 60 },
                    { name: '2', value: '三维螺旋时空方程', category: '时空方程', symbolSize: 50 },
                    { name: '3', value: '质量定义方程', category: '场方程', symbolSize: 50 },
                    { name: '4', value: '引力场定义方程', category: '场方程', symbolSize: 40 },
                    { name: '5', value: '静止动量方程', category: '动力学方程', symbolSize: 40 },
                    { name: '6', value: '运动动量方程', category: '动力学方程', symbolSize: 40 },
                    { name: '16', value: '统一场论能量方程', category: '动力学方程', symbolSize: 50 },
                    { name: '17', value: '引力场与电磁场的统一方程', category: '统一方程', symbolSize: 60 }
                ],
                links: [
                    { source: '1', target: '2' },
                    { source: '1', target: '16' },
                    { source: '3', target: '4' },
                    { source: '5', target: '6' },
                    { source: '4', target: '17' },
                    { source: '1', target: '5' }
                ],
                categories: [
                    { name: '时空方程', itemStyle: { color: '#1f77b4' } },
                    { name: '动力学方程', itemStyle: { color: '#ff7f0e' } },
                    { name: '场方程', itemStyle: { color: '#2ca02c' } },
                    { name: '统一方程', itemStyle: { color: '#d62728' } }
                ]
            }]
        };
        relationChart.setOption(relationOption);
        
        // 响应式处理
        window.addEventListener('resize', function() {
            typeChart.resize();
            relationChart.resize();
        });
        
        // 滚动到指定部分
        function scrollToSection(id) {
            document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
        }
        
        // 添加页面加载动画
        window.addEventListener('load', function() {
            document.body.style.opacity = 0;
            setTimeout(function() {
                document.body.style.transition = 'opacity 0.8s ease';
                document.body.style.opacity = 1;
            }, 100);
        });
    </script>
</body>
</html>
''')
        
        print(f"综合HTML可视化报告已保存到: {html_file}")
        return html_file
    
    def 生成综合PDF报告(self):
        """生成综合PDF报告，包含所有公式"""
        pdf_file = f'{self.output_dir}/统一场论18核心公式可视化报告.pdf'
        
        try:
            with PdfPages(pdf_file) as pdf:
                # 封面页
                plt.figure(figsize=(11, 8.5))
                plt.axis('off')
                plt.text(0.5, 0.8, '统一场论18核心公式可视化报告', 
                        fontsize=24, ha='center', va='center')
                plt.text(0.5, 0.7, 'Mathematical Visualization of Unified Field Theory', 
                        fontsize=16, ha='center', va='center')
                plt.text(0.5, 0.6, '张祥前统一场论研究团队', 
                        fontsize=14, ha='center', va='center')
                plt.text(0.5, 0.5, datetime.now().strftime('%Y年%m月%d日'), 
                        fontsize=12, ha='center', va='center')
                pdf.savefig()
                plt.close()
                
                # 摘要页
                plt.figure(figsize=(11, 8.5))
                plt.axis('off')
                plt.text(0.5, 0.9, '摘要', fontsize=20, ha='center')
                
                abstract_text = """
                统一场论提出了18个核心公式，涵盖了时空方程、动力学方程、场方程和统一方程四大类。
                本报告通过数学可视化的方式，直观展示了这些公式的数学结构、物理意义和相互关系。
                
                时空方程揭示了空间和时间的统一本质，动力学方程描述了物质的运动规律，
                场方程定义了各种物理场的性质，统一方程则实现了引力场与电磁场的统一。
                
                所有公式均通过符号求导和数值验证，数学上具有自洽性和严谨性。
                """
                
                plt.text(0.5, 0.6, abstract_text, fontsize=12, ha='center', va='center', wrap=True)
                pdf.savefig()
                plt.close()
                
                # 公式类型分布
                plt.figure(figsize=(11, 8.5))
                plt.subplot(121)
                labels = ['时空方程', '动力学方程', '场方程', '统一方程']
                sizes = [2, 4, 8, 4]
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                        startangle=90, shadow=True)
                plt.axis('equal')
                plt.title('公式类型分布', fontsize=14)
                
                plt.subplot(122)
                plt.bar(range(len(labels)), sizes, tick_label=labels, color=colors)
                plt.title('公式数量统计', fontsize=14)
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig()
                plt.close()
                
                # 前8个最重要的公式
                for i in range(min(8, len(self.formulas))):
                    formula = self.formulas[i]
                    formula_id = formula['id']
                    formula_name = formula['name']
                    
                    try:
                        # 尝试加载可视化图片
                        img_path = f'{self.output_dir}/公式{formula_id:02d}_{formula_name}.png'
                        
                        plt.figure(figsize=(11, 8.5))
                        plt.axis('off')
                        plt.text(0.5, 0.95, f'公式{formula_id:02d}: {formula_name}', fontsize=18, ha='center')
                        plt.text(0.5, 0.9, f'{formula["formula"]}', fontsize=14, ha='center')
                        
                        if os.path.exists(img_path):
                            img = plt.imread(img_path)
                            plt.imshow(img)
                        else:
                            plt.text(0.5, 0.5, f'公式描述: {formula["description"]}\n\n物理意义: {formula["physics_meaning"]}', 
                                    fontsize=12, ha='center', va='center', wrap=True)
                        
                        pdf.savefig()
                        plt.close()
                    except Exception as e:
                        print(f"PDF报告中添加公式{formula_id}失败: {e}")
                        plt.close()
                
                # 结论页
                plt.figure(figsize=(11, 8.5))
                plt.axis('off')
                plt.text(0.5, 0.9, '结论', fontsize=20, ha='center')
                
                conclusion_text = """
                统一场论的18个核心公式构成了一个完整的理论体系，具有以下特点：
                
                1. 数学严谨性：所有公式均通过符号求导和数值验证
                2. 物理自洽性：与现有物理理论在低速、宏观条件下一致
                3. 理论统一性：实现了引力场与电磁场的统一描述
                4. 简洁优美：公式形式简洁，物理意义明确
                
                这些公式为理解宇宙的本质提供了新的视角，
                揭示了空间、时间、物质、能量和场的统一关系。
                """
                
                plt.text(0.5, 0.5, conclusion_text, fontsize=12, ha='center', va='center', wrap=True)
                pdf.savefig()
                plt.close()
                
            print(f"综合PDF报告已保存到: {pdf_file}")
            return pdf_file
        except Exception as e:
            print(f"生成PDF报告失败: {e}")
            return None
    
    def 运行可视化系统(self):
        """运行完整的可视化系统"""
        print("=========================================================")
        print("               统一场论18核心公式可视化系统")
        print("=========================================================")
        
        # 生成公式概览图
        self.生成公式概览图()
        
        # 生成所有公式的可视化图表
        self.可视化所有公式()
        
        # 生成公式关系网络
        self.生成公式关系网络()
        
        # 生成公式家族树
        self.生成公式家族树()
        
        # 生成综合HTML报告
        html_file = self.生成综合HTML可视化报告()
        
        # 生成综合PDF报告
        pdf_file = self.生成综合PDF报告()
        
        print("\n=========================================================")
        print("                     可视化完成")
        print("=========================================================")
        print(f"所有可视化结果已保存到: {self.output_dir}")
        print(f"综合HTML报告: {html_file}")
        print(f"综合PDF报告: {pdf_file}")
        print("=========================================================")
        
        return html_file

if __name__ == "__main__":
    # 初始化可视化系统并运行
    visualizer = 统一场论公式可视化系统()
    html_report = visualizer.运行可视化系统()
    
    # 提示用户打开报告
    print("\n请在浏览器中打开以下地址查看完整的可视化报告:")
    print("file://" + html_report.replace('\\', '/'))
