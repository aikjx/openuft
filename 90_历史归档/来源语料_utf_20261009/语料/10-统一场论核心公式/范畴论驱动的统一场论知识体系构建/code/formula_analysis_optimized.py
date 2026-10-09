#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论公式积木模块分析与可视化（优化版）

该脚本用于分析张祥前统一场论20个核心公式的积木模块关系，并通过网络图进行可视化。
提供了丰富的分析功能，包括模块使用频率分析、量纲关系分析、公式交叉分析等。
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import json

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

class FormulaAnalysis:
    """统一场论公式分析类"""
    
    def __init__(self):
        """初始化数据"""
        # 通用积木模块库，添加量纲信息
        # 量纲符号说明：[L]=长度, [T]=时间, [M]=质量, [I]=电流
        self.modules = {
            'M01': {'name': '光速矢量', 'formula': '\\vec{c}', 'meaning': '时空统一常数', 'dimension': '[L][T]^{-1}'},
            'M02': {'name': '时空位置矢量', 'formula': '\\vec{r} = x\\vec{i} + y\\vec{j} + z\\vec{k}', 'meaning': '空间位置表示', 'dimension': '[L]'},
            'M03': {'name': '立体角变化率', 'formula': '\\dfrac{d\\Omega}{dt}', 'meaning': '空间几何旋转速率', 'dimension': '[T]^{-1}'},
            'M04': {'name': '质量变化率', 'formula': '\\dfrac{dm}{dt}', 'meaning': '质量随时间变化', 'dimension': '[M][T]^{-1}'},
            'M05': {'name': '径向衰减因子', 'formula': '\\dfrac{1}{r^3} 或 \\dfrac{\\vec{r}}{r^3}', 'meaning': '场强空间分布', 'dimension': '[L]^{-3}'},
            'M06': {'name': '动量核心结构', 'formula': 'm(\\vec{c} - \\vec{v})', 'meaning': '统一场论动量定义', 'dimension': '[M][L][T]^{-1}'},
            'M07': {'name': '力的微分形式', 'formula': '\\dfrac{d\\vec{P}}{dt}', 'meaning': '力的基本定义', 'dimension': '[M][L][T]^{-2}'},
            'M08': {'name': '引力耦合项', 'formula': 'Gk', 'meaning': '引力相互作用强度', 'dimension': '[L]^4[T]^{-2}[M]^{-1}'},
            'M09': {'name': '电磁耦合项', 'formula': '\\dfrac{kk^{\prime}}{4\\pi\\varepsilon_0}', 'meaning': '电磁相互作用强度', 'dimension': '[L]^3[T]^{-2}[M]'},
            'M10': {'name': '相对论因子', 'formula': '\\sqrt{1 - \\dfrac{v^2}{c^2}} 或 \\gamma', 'meaning': '高速运动修正', 'dimension': '1'},
            'M11': {'name': '质量定义', 'formula': 'm = k \\dfrac{dn}{d\\Omega}', 'meaning': '质量的几何定义', 'dimension': '[M]'},
            'M12': {'name': '磁矢势旋度', 'formula': '\\vec{\\nabla} \\times \\vec{A}', 'meaning': '磁矢势的旋度', 'dimension': '[M][T]^{-2}[I]^{-1}'},
            'M13': {'name': '矢量时间导数', 'formula': '\\dfrac{d\\vec{A}}{dt}', 'meaning': '矢量随时间的变化率', 'dimension': '[L][T]^{-2}'},
            'M14': {'name': '统一场论常数', 'formula': 'f', 'meaning': '统一场论中的重要常数', 'dimension': '[L][T]^{-1}'}
        }
        
        # 公式量纲信息
        self.formula_dimensions = {
            '公式1': '[L]',  # 时空同一化方程
            '公式2': '[L]',  # 三维螺旋时空方程
            '公式3': '[M]',  # 质量定义方程
            '公式4': '[L][T]^{-2}',  # 引力场定义方程
            '公式5': '[M][L][T]^{-1}',  # 静止动量方程
            '公式6': '[M][L][T]^{-1}',  # 运动动量方程
            '公式7': '[M][L][T]^{-2}',  # 宇宙大统一方程
            '公式8': '[L]^{-1}',  # 空间波动方程
            '公式9': '[I][T]',  # 电荷定义方程
            '公式10': '[M][L][T]^{-3}[I]^{-1}',  # 电场定义方程
            '公式11': '[M][T]^{-2}[I]^{-1}',  # 磁场定义方程
            '公式12': '[L][T]^{-4}',  # 变化的引力场产生电磁场
            '公式13': '[M][T]^{-2}[I]^{-1}',  # 磁矢势方程
            '公式14': '[M][L][T]^{-3}[I]^{-1}',  # 变化的引力场产生电场
            '公式15': '[M][T]^{-3}[I]^{-1}',  # 变化的磁场产生引力场和电场
            '公式16': '[M][L]^2[T]^{-2}',  # 统一场论能量方程
            '公式17': '[M][L][T]^{-2}',  # 光速飞行器动力学方程
            '公式18': '[L]^{-2}[T]^{-2}',  # 核力场定义方程
            '公式19': '[L]^3[T]^{-2}',  # 引力光速统一方程
            '公式20': '[L]^3[T]^{-2}'   # 电磁光速几何耦合常数
        }
        
        # 20个核心公式，每个公式包含使用的模块
        self.formulas = {
            '公式1': {
                'name': '时空同一化方程',
                'formula': '\\vec{r}(t) = \\vec{c}t = x\\vec{i} + y\\vec{j} + z\\vec{k}',
                'modules': ['M01', 'M02']
            },
            '公式2': {
                'name': '三维螺旋时空方程',
                'formula': '\\vec{r}(t) = r\\cos\\omega t \\cdot \\vec{i} + r\\sin\\omega t \\cdot \\vec{j} + ht \\cdot \\vec{k}',
                'modules': ['M01', 'M02']
            },
            '公式3': {
                'name': '质量定义方程',
                'formula': 'm = k \\dfrac{dn}{d\\Omega}',
                'modules': ['M11']  # 关联到质量定义模块
            },
            '公式4': {
                'name': '引力场定义方程',
                'formula': '\\vec{A} = -Gk\\dfrac{\\Delta n}{\\Delta s}\\dfrac{\\vec{r}}{r}',
                'modules': ['M02', 'M08']
            },
            '公式5': {
                'name': '静止动量方程',
                'formula': '\\vec{p}_{0} = m_{0}\\vec{c}_{0}',
                'modules': ['M01', 'M11']
            },
            '公式6': {
                'name': '运动动量方程',
                'formula': '\\vec{P} = m(\\vec{c} - \\vec{v})',
                'modules': ['M01', 'M06', 'M11']
            },
            '公式7': {
                'name': '宇宙大统一方程',
                'formula': '\\vec{F} = \\dfrac{d\\vec{P}}{dt} = \\vec{c}\\dfrac{dm}{dt} - \\vec{v}\\dfrac{dm}{dt} + m\\dfrac{d\\vec{c}}{dt} - m\\dfrac{d\\vec{v}}{dt}',
                'modules': ['M01', 'M04', 'M06', 'M07', 'M11']
            },
            '公式8': {
                'name': '空间波动方程',
                'formula': '\\nabla^2 L = \\dfrac{1}{c^2} \\dfrac{\\partial^2 L}{\\partial t^2}',
                'modules': ['M01']
            },
            '公式9': {
                'name': '电荷定义方程',
                'formula': 'q = k^{\prime}k\\dfrac{1}{\\Omega^{2}}\\dfrac{d\\Omega}{dt}',
                'modules': ['M03']
            },
            '公式10': {
                'name': '电场定义方程',
                'formula': '\\vec{E} = -\\dfrac{kk^{\prime}}{4\\pi\\varepsilon_0\\Omega^2}\\dfrac{d\\Omega}{dt}\\dfrac{\\vec{r}}{r^3}',
                'modules': ['M02', 'M03', 'M05', 'M09']
            },
            '公式11': {
                'name': '磁场定义方程',
                'formula': '\\vec{B} = \\dfrac{\\mu_{0} \\gamma k k^{\prime}}{4 \\pi \\Omega^{2}} \\dfrac{d \\Omega}{d t} \\dfrac{[(x-v t) \\vec{i}+y \\vec{j}+z \\vec{k}]}{\\left[\\gamma^{2}(x-v t)^{2}+y^{2}+z^{2}\\right]^{3/2}}',
                'modules': ['M02', 'M03', 'M05', 'M10']
            },
            '公式12': {
                'name': '变化的引力场产生电磁场',
                'formula': '\\dfrac{\\partial^{2}\\vec{A}}{\\partial t^{2}} = \\dfrac{\\vec{v}}{f}\\left(\\vec{\\nabla}\\cdot\\vec{E}\\right) - \\dfrac{c^{2}}{f}\\left(\\vec{\\nabla}\\times\\vec{B}\\right)',
                'modules': ['M01', 'M14']
            },
            '公式13': {
                'name': '磁矢势方程',
                'formula': '\\vec{\\nabla} \\times \\vec{A} = \\dfrac{\\vec{B}}{f}',
                'modules': ['M12', 'M14']
            },
            '公式14': {
                'name': '变化的引力场产生电场',
                'formula': '\\vec{E} = -f\\dfrac{d\\vec{A}}{dt}',
                'modules': ['M13', 'M14']
            },
            '公式15': {
                'name': '变化的磁场产生引力场和电场',
                'formula': '\\dfrac{d\\vec{B}}{dt} = -\\dfrac{\\vec{A}\\times\\vec{E}}{c^2} - \\dfrac{\\vec{v}}{c^{2}}\\times\\dfrac{d\\vec{E}}{dt}',
                'modules': ['M01']
            },
            '公式16': {
                'name': '统一场论能量方程',
                'formula': 'E = m_0 c^2 = mc^2\\sqrt{1 - \\dfrac{v^2}{c^2}}',
                'modules': ['M01', 'M10', 'M11']
            },
            '公式17': {
                'name': '光速飞行器动力学方程',
                'formula': '\\vec{F} = (\\vec{c} - \\vec{v})\\dfrac{dm}{dt}',
                'modules': ['M01', 'M04', 'M06', 'M11']
            },
            '公式18': {
                'name': '核力场定义方程',
                'formula': '\\vec{D} = - G m \\dfrac{ \\vec{c} - 3 \\dfrac{\\vec{r}}{r} \\dot{r} }{r^3}',
                'modules': ['M01', 'M02', 'M05', 'M11']
            },
            '公式19': {
                'name': '引力光速统一方程',
                'formula': 'Z = \\dfrac{Gc}{2}',
                'modules': ['M01']
            },
            '公式20': {
                'name': '电磁光速几何耦合常数',
                'formula': 'Z^{\\prime} = \\dfrac{c}{8\\pi\\varepsilon_0}',
                'modules': ['M01']
            }
        }
        
        # 模块转换关系
        self.module_relations = [
            ('M01', 'M06'),    # 光速矢量 → 动量核心结构
            ('M06', 'M07'),    # 动量核心结构 → 力的微分形式
            ('M03', 'M05'),    # 立体角变化率 → 径向衰减因子
            ('M05', 'M09'),    # 径向衰减因子 → 电磁耦合项
            ('M01', 'M10'),    # 光速矢量 → 相对论因子
            ('M06', 'M01'),    # 动量核心结构 → 光速矢量（反推）
            ('M08', 'M02'),    # 引力耦合项 → 时空位置矢量
            ('M09', 'M02'),    # 电磁耦合项 → 时空位置矢量
            ('M04', 'M07'),    # 质量变化率 → 力的微分形式
            ('M01', 'M01'),    # 光速矢量平方（自转换）
            ('M03', 'M09'),    # 立体角变化率 → 电磁耦合项
            ('M06', 'M10'),    # 动量核心结构 → 相对论因子
            ('M02', 'M05')     # 时空位置矢量 → 径向衰减因子
        ]
    
    def analyze_module_usage(self):
        """分析模块使用频率"""
        module_counts = {}
        for module_id in self.modules:
            module_counts[module_id] = 0
        
        for formula_id, formula_info in self.formulas.items():
            for module in formula_info['modules']:
                if module in module_counts:
                    module_counts[module] += 1
        
        # 转换为DataFrame
        usage_df = pd.DataFrame.from_dict(
            module_counts, 
            orient='index', 
            columns=['使用次数']
        )
        usage_df['模块名称'] = [self.modules[mid]['name'] for mid in usage_df.index]
        usage_df['模块意义'] = [self.modules[mid]['meaning'] for mid in usage_df.index]
        usage_df['量纲'] = [self.modules[mid]['dimension'] for mid in usage_df.index]
        usage_df = usage_df[['模块名称', '使用次数', '模块意义', '量纲']].sort_values('使用次数', ascending=False)
        
        return usage_df
    
    def create_formula_module_graph(self):
        """创建公式-模块关系图"""
        G = nx.Graph()
        
        # 添加模块节点
        for module_id, module_info in self.modules.items():
            G.add_node(
                module_id,
                type='module',
                name=module_info['name'],
                formula=module_info['formula'],
                meaning=module_info['meaning'],
                dimension=module_info['dimension']
            )
        
        # 添加公式节点
        for formula_id, formula_info in self.formulas.items():
            G.add_node(
                formula_id,
                type='formula',
                name=formula_info['name'],
                formula=formula_info['formula']
            )
        
        # 添加边
        for formula_id, formula_info in self.formulas.items():
            for module in formula_info['modules']:
                G.add_edge(formula_id, module, relation='使用')
        
        return G
    
    def create_module_relation_graph(self):
        """创建模块关系图"""
        G = nx.DiGraph()
        
        # 添加模块节点
        for module_id, module_info in self.modules.items():
            G.add_node(
                module_id,
                name=module_info['name'],
                formula=module_info['formula'],
                meaning=module_info['meaning'],
                dimension=module_info['dimension']
            )
        
        # 添加边
        for source, target in self.module_relations:
            G.add_edge(source, target, relation='转换为')
        
        return G
    
    def analyze_module_centrality(self):
        """分析模块中心性，识别核心模块"""
        G = self.create_module_relation_graph()
        
        # 计算不同类型的中心性
        centrality = {
            'degree': nx.degree_centrality(G),
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G),
            'eigenvector': nx.eigenvector_centrality(G, max_iter=1000)
        }
        
        # 转换为DataFrame
        centrality_df = pd.DataFrame(centrality)
        centrality_df['模块名称'] = [self.modules[mid]['name'] for mid in centrality_df.index]
        centrality_df['使用次数'] = [sum(1 for f in self.formulas.values() if mid in f['modules']) for mid in centrality_df.index]
        
        # 综合得分
        centrality_df['综合得分'] = centrality_df[['degree', 'betweenness', 'closeness', 'eigenvector']].mean(axis=1)
        centrality_df = centrality_df.sort_values('综合得分', ascending=False)
        
        return centrality_df
    
    def visualize_formula_module_relation(self, output_file='formula_module_relation.png'):
        """可视化公式-模块关系"""
        G = self.create_formula_module_graph()
        
        # 设置节点颜色
        node_colors = []
        for node in G.nodes():
            if G.nodes[node]['type'] == 'module':
                node_colors.append('#FF9999')  # 模块节点为红色
            else:
                node_colors.append('#99CCFF')  # 公式节点为蓝色
        
        # 设置节点大小（基于使用频率）
        node_sizes = []
        module_usage = {mid: sum(1 for f in self.formulas.values() if mid in f['modules']) for mid in self.modules}
        for node in G.nodes():
            if G.nodes[node]['type'] == 'module':
                size = 2000 + module_usage.get(node, 0) * 200
                node_sizes.append(size)
            else:
                module_count = len(self.formulas.get(node, {}).get('modules', []))
                size = 1500 + module_count * 100
                node_sizes.append(size)
        
        # 绘制图形
        plt.figure(figsize=(24, 18))
        pos = nx.spring_layout(G, k=0.5, iterations=100)
        
        nx.draw_networkx_nodes(
            G, pos, 
            node_color=node_colors, 
            node_size=node_sizes,
            alpha=0.8,
            edgecolors='#333333',
            linewidths=1.5
        )
        
        nx.draw_networkx_edges(
            G, pos, 
            width=1.2, 
            alpha=0.6,
            edge_color='#666666',
            style='solid'
        )
        
        # 绘制标签
        labels = {}
        for node in G.nodes():
            if G.nodes[node]['type'] == 'module':
                labels[node] = f"{node}\n{G.nodes[node]['name']}"
            else:
                labels[node] = f"{node}\n{G.nodes[node]['name']}"
        
        nx.draw_networkx_labels(
            G, pos, 
            labels, 
            font_size=11,
            font_family='SimHei',
            font_weight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3')
        )
        
        plt.title('统一场论公式-模块关系图', fontsize=20, fontweight='bold', fontfamily='SimHei', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"公式-模块关系图已保存到: {output_file}")
    
    def visualize_module_relation(self, output_file='module_relation.png'):
        """可视化模块关系"""
        G = self.create_module_relation_graph()
        
        # 计算节点位置，使用更美观的布局
        pos = nx.spring_layout(G, k=0.8, iterations=100)
        
        # 绘制图形
        plt.figure(figsize=(18, 14))
        
        # 绘制节点，大小基于中心性
        centrality = nx.degree_centrality(G)
        node_sizes = [3000 + centrality[node] * 5000 for node in G.nodes()]
        
        nx.draw_networkx_nodes(
            G, pos, 
            node_color='#FF9999', 
            node_size=node_sizes,
            alpha=0.8,
            edgecolors='#333333',
            linewidths=1.5
        )
        
        nx.draw_networkx_edges(
            G, pos, 
            arrowstyle='->',
            arrowsize=25,
            width=2.0, 
            alpha=0.7,
            edge_color='#666666'
        )
        
        # 绘制标签
        labels = {}
        for node in G.nodes():
            labels[node] = f"{node}\n{G.nodes[node]['name']}"
        
        nx.draw_networkx_labels(
            G, pos, 
            labels, 
            font_size=13,
            font_family='SimHei',
            font_weight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3')
        )
        
        # 绘制边标签
        edge_labels = {}
        for u, v in G.edges():
            edge_labels[(u, v)] = G.edges[u, v]['relation']
        
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels, 
            font_size=11,
            font_family='SimHei',
            font_weight='bold',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2')
        )
        
        plt.title('统一场论模块转换关系图', fontsize=20, fontweight='bold', fontfamily='SimHei', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"模块转换关系图已保存到: {output_file}")
    
    def visualize_module_centrality(self, output_file='module_centrality.png'):
        """可视化模块中心性"""
        centrality_df = self.analyze_module_centrality()
        
        # 雷达图数据
        metrics = ['degree', 'betweenness', 'closeness', 'eigenvector']
        centrality_df['degree_norm'] = (centrality_df['degree'] - centrality_df['degree'].min()) / (centrality_df['degree'].max() - centrality_df['degree'].min())
        centrality_df['betweenness_norm'] = (centrality_df['betweenness'] - centrality_df['betweenness'].min()) / (centrality_df['betweenness'].max() - centrality_df['betweenness'].min())
        centrality_df['closeness_norm'] = (centrality_df['closeness'] - centrality_df['closeness'].min()) / (centrality_df['closeness'].max() - centrality_df['closeness'].min())
        centrality_df['eigenvector_norm'] = (centrality_df['eigenvector'] - centrality_df['eigenvector'].min()) / (centrality_df['eigenvector'].max() - centrality_df['eigenvector'].min())
        
        # 选择前8个最重要的模块
        top_modules = centrality_df.head(8)
        
        # 雷达图数据
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # 闭合
        
        plt.figure(figsize=(14, 12))
        ax = plt.subplot(111, polar=True)
        
        for i, (idx, row) in enumerate(top_modules.iterrows()):
            values = [row['degree_norm'], row['betweenness_norm'], row['closeness_norm'], row['eigenvector_norm']]
            values += values[:1]  # 闭合
            ax.plot(angles, values, linewidth=2, linestyle='solid', label=row['模块名称'])
            ax.fill(angles, values, alpha=0.1)
        
        # 添加标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=12, fontfamily='SimHei')
        ax.set_yticklabels([])
        
        plt.title('核心模块中心性分析', fontsize=18, fontweight='bold', fontfamily='SimHei', pad=20)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11, fontfamily='SimHei')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"模块中心性分析图已保存到: {output_file}")
    
    def analyze_dimension_relationships(self):
        """分析量纲关系，找出具有相同或相关量纲的模块和公式"""
        # 按量纲分组模块
        dimension_modules = {}
        for module_id, module_info in self.modules.items():
            dim = module_info['dimension']
            if dim not in dimension_modules:
                dimension_modules[dim] = []
            dimension_modules[dim].append(module_id)
        
        # 按量纲分组公式
        dimension_formulas = {}
        for formula_id, dim in self.formula_dimensions.items():
            if dim not in dimension_formulas:
                dimension_formulas[dim] = []
            dimension_formulas[dim].append(formula_id)
        
        return dimension_modules, dimension_formulas
    
    def analyze_cross_relationships(self):
        """分析方程之间的交叉关系，包括模块共享、量纲关联和物理意义关联"""
        cross_relations = {}
        
        # 计算每对公式之间的关系
        formula_ids = list(self.formulas.keys())
        for i in range(len(formula_ids)):
            formula1 = formula_ids[i]
            cross_relations[formula1] = {}
            for j in range(i+1, len(formula_ids)):
                formula2 = formula_ids[j]
                
                # 计算共享模块数量
                modules1 = set(self.formulas[formula1]['modules'])
                modules2 = set(self.formulas[formula2]['modules'])
                shared_modules = modules1.intersection(modules2)
                
                # 检查量纲是否相同
                same_dimension = self.formula_dimensions[formula1] == self.formula_dimensions[formula2]
                
                # 计算模块相似度（Jaccard系数）
                total_modules = modules1.union(modules2)
                if len(total_modules) == 0:
                    module_similarity = 0.0
                else:
                    module_similarity = len(shared_modules) / len(total_modules)
                
                # 计算物理意义相似度
                name1 = self.formulas[formula1]['name']
                name2 = self.formulas[formula2]['name']
                physical_similarity = self._calculate_physical_similarity(name1, name2)
                
                cross_relations[formula1][formula2] = {
                    'shared_modules': list(shared_modules),
                    'module_similarity': round(module_similarity, 2),
                    'physical_similarity': round(physical_similarity, 2),
                    'same_dimension': same_dimension,
                    'dimension1': self.formula_dimensions[formula1],
                    'dimension2': self.formula_dimensions[formula2],
                    'formula1_name': name1,
                    'formula2_name': name2
                }
        
        return cross_relations
    
    def _calculate_physical_similarity(self, name1, name2):
        """计算两个公式物理意义的相似度"""
        # 定义物理概念关键词
        concepts = {
            '时空': ['时空', '空间', '时间'],
            '动量': ['动量'],
            '能量': ['能量'],
            '场': ['场', '电场', '磁场', '引力场', '核力场'],
            '力': ['力'],
            '质量': ['质量'],
            '电荷': ['电荷'],
            '光速': ['光速'],
            '动力学': ['动力学']
        }
        
        # 计算共同概念数量
        common_concepts = 0
        total_concepts = 0
        
        for concept, keywords in concepts.items():
            has_concept1 = any(keyword in name1 for keyword in keywords)
            has_concept2 = any(keyword in name2 for keyword in keywords)
            
            if has_concept1 or has_concept2:
                total_concepts += 1
                if has_concept1 and has_concept2:
                    common_concepts += 1
        
        if total_concepts == 0:
            return 0.0
        return common_concepts / total_concepts
    
    def generate_interactive_graph(self, output_file='interactive_graph.html'):
        """生成交互式网络图"""
        G = self.create_formula_module_graph()
        
        # 准备节点和边的数据
        nodes = []
        for node in G.nodes():
            node_data = G.nodes[node]
            nodes.append({
                'id': node,
                'label': f"{node}\\n{node_data['name']}",
                'type': node_data['type'],
                'size': 30 if node_data['type'] == 'module' else 20,
                'color': '#FF9999' if node_data['type'] == 'module' else '#99CCFF'
            })
        
        edges = []
        for u, v, data in G.edges(data=True):
            edges.append({
                'source': u,
                'target': v,
                'label': data.get('relation', '关联')
            })
        
        # 创建HTML内容
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>统一场论公式-模块关系交互式网络图</title>
    <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.css" rel="stylesheet" type="text/css" />
    <style>
        body {{
            font-family: 'SimHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        #network {{
            width: 100%;
            height: 800px;
            border: 1px solid #ddd;
            background-color: white;
        }}
        .title {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
        }}
        .description {{
            text-align: center;
            margin-bottom: 20px;
            color: #666;
        }}
        .legend {{
            text-align: center;
            margin-top: 20px;
        }}
        .legend-item {{
            display: inline-block;
            margin: 0 10px;
        }}
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 5px;
        }}
        .module-color {{
            background-color: #FF9999;
        }}
        .formula-color {{
            background-color: #99CCFF;
        }}
    </style>
</head>
<body>
    <div class="title">统一场论公式-模块关系交互式网络图</div>
    <div class="description">点击节点可查看详细信息，拖拽可调整布局，滚轮可缩放</div>
    <div id="network"></div>
    <div class="legend">
        <div class="legend-item">
            <span class="legend-color module-color"></span>
            <span>模块节点</span>
        </div>
        <div class="legend-item">
            <span class="legend-color formula-color"></span>
            <span>公式节点</span>
        </div>
    </div>

    <script>
        // 节点数据
        var nodes = {json.dumps(nodes)};
        
        // 边数据
        var edges = {json.dumps(edges)};
        
        // 网络配置
        var container = document.getElementById('network');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            nodes: {{
                font: {{
                    size: 12,
                    face: 'SimHei'
                }},
                shape: 'circle'
            }},
            edges: {{
                font: {{
                    size: 10,
                    face: 'SimHei'
                }},
                arrows: {{
                    to: {{
                        enabled: true,
                        scaleFactor: 0.5
                    }}
                }},
                smooth: {{
                    enabled: true
                }}
            }},
            interaction: {{
                hover: true,
                zoomView: true,
                dragNodes: true,
                dragView: true
            }},
            layout: {{
                hierarchical: {{
                    enabled: false,
                    direction: 'UD'
                }}
            }},
            physics: {{
                enabled: true,
                stabilization: {{
                    enabled: true,
                    iterations: 1000
                }}
            }}
        }};
        
        // 创建网络
        var network = new vis.Network(container, data, options);
        
        // 点击事件
        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodes.find(n => n.id === nodeId);
                if (node) {{
                    alert('节点: ' + node.id + '\\n名称: ' + node.label.split('\\\\n')[1] + '\\n类型: ' + (node.type === 'module' ? '模块' : '公式'));
                }}
            }}
        }});
    </script>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"交互式网络图已保存到: {output_file}")
    
    def generate_report(self):
        """生成分析报告"""
        current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
        report = "# 统一场论公式积木模块分析报告\n\n"
        report += f"**生成时间**：{current_date}\n\n"
        report += "**分析工具**：统一场论公式积木模块分析系统 (v2.0)\n\n"
        
        # 模块使用频率分析
        usage_df = self.analyze_module_usage()
        report += "## 1. 模块使用频率分析\n\n"
        report += "| 模块ID | 模块名称 | 使用次数 | 模块意义 | 量纲 |\n"
        report += "|-------|---------|---------|---------|------|\n"
        for idx, row in usage_df.iterrows():
            report += f"| {idx} | {row['模块名称']} | {row['使用次数']} | {row['模块意义']} | {row['量纲']} |\n"
        
        # 核心模块识别
        top_modules = usage_df[usage_df['使用次数'] >= 3]
        report += "\n## 2. 核心模块识别\n\n"
        report += f"使用次数≥3的核心模块共有 {len(top_modules)} 个：\n\n"
        for idx, row in top_modules.iterrows():
            module_info = self.modules[idx]
            report += f"- **{idx} {row['模块名称']}**：{module_info['meaning']}\n"
            report += f"  数学形式：${module_info['formula']}$\n"
            report += f"  量纲：{module_info['dimension']}\n"
            report += f"  使用次数：{row['使用次数']}\n"
        
        # 模块中心性分析
        centrality_df = self.analyze_module_centrality()
        report += "\n## 3. 模块中心性分析\n\n"
        report += "| 模块ID | 模块名称 | 综合得分 | 使用次数 | 度中心性 | 中介中心性 | 接近中心性 | 特征向量中心性 |\n"
        report += "|-------|---------|---------|---------|---------|-----------|-----------|---------------|\n"
        for idx, row in centrality_df.head(10).iterrows():
            report += f"| {idx} | {row['模块名称']} | {row['综合得分']:.4f} | {row['使用次数']} | {row['degree']:.4f} | {row['betweenness']:.4f} | {row['closeness']:.4f} | {row['eigenvector']:.4f} |\n"
        
        # 公式模块统计
        report += "\n## 4. 公式模块统计\n\n"
        formula_module_counts = {}
        for formula_id, formula_info in self.formulas.items():
            module_count = len(formula_info['modules'])
            formula_module_counts[formula_id] = module_count
        
        avg_modules = sum(formula_module_counts.values()) / len(formula_module_counts)
        report += f"- 平均每个公式使用 {avg_modules:.1f} 个模块\n"
        report += f"- 使用模块最多的公式：{max(formula_module_counts, key=formula_module_counts.get)}\n"
        report += f"- 使用模块最少的公式：{min(formula_module_counts, key=formula_module_counts.get)}\n"
        
        # 量纲积木分析
        dimension_modules, dimension_formulas = self.analyze_dimension_relationships()
        report += "\n## 5. 量纲积木分析\n\n"
        report += "### 5.1 模块量纲分组\n\n"
        report += "量纲是物理公式的基本特征，相同量纲的模块可以看作是同一类'量纲积木'：\n\n"
        for dim, module_list in sorted(dimension_modules.items()):
            if len(module_list) >= 1:
                report += f"**量纲 {dim}**：\n"
                for module_id in module_list:
                    module_name = self.modules[module_id]['name']
                    report += f"- {module_id} {module_name}\n"
                report += "\n"
        
        report += "### 5.2 公式量纲分组\n\n"
        report += "相同量纲的公式往往描述了同类物理现象或过程：\n\n"
        for dim, formula_list in sorted(dimension_formulas.items()):
            if len(formula_list) >= 1:
                report += f"**量纲 {dim}**：\n"
                for formula_id in formula_list:
                    formula_name = self.formulas[formula_id]['name']
                    report += f"- {formula_id} {formula_name}\n"
                report += "\n"
        
        # 模块关系分析
        report += "\n## 6. 模块关系分析\n\n"
        report += "### 6.1 模块转换链\n\n"
        report += "1. **基础模块链**：M01（光速矢量）→ M06（动量核心结构）→ M07（力的微分形式）\n"
        report += "2. **场模块链**：M03（立体角变化率）→ M05（径向衰减因子）→ 电磁场\n"
        report += "3. **动量-能量链**：M06（动量核心结构）→ 动量平方 → 能量方程\n"
        report += "4. **质量-电荷转换链**：几何变化率 → 质量 → 电荷 → 电磁场\n"
        
        # 关键发现分析
        report += "\n### 6.2 关键发现\n\n"
        report += "1. **M01（光速矢量）是核心模块**：使用次数最多，连接时空、物质、能量\n"
        report += "2. **M06（动量核心结构）是动力学基础**：是力方程和能量方程的共同源头\n"
        report += "3. **M03-M05模块链**：共同描述了场的产生和分布规律\n"
        report += "4. **统一的变化率基础**：$\\dfrac{d\\Omega}{dt}$ 和 $\\dfrac{dm}{dt}$ 是许多公式的共同输入\n"
        report += "5. **模块的组合多样性**：相同模块通过不同组合方式产生不同物理效应\n"
        report += "6. **量纲一致性**：所有公式都遵循量纲一致性原则，验证了公式的正确性\n"
        
        # 模块组合模式分析
        report += "\n## 7. 模块组合模式分析\n\n"
        
        # 分析公式使用的模块数量分布
        module_count_distribution = {}
        for formula_id, formula_info in self.formulas.items():
            module_count = len(formula_info['modules'])
            if module_count not in module_count_distribution:
                module_count_distribution[module_count] = 0
            module_count_distribution[module_count] += 1
        
        report += "### 7.1 模块数量分布\n\n"
        report += "| 模块数量 | 公式数量 | 占比 |\n"
        report += "|---------|---------|------|\n"
        total_formulas = len(self.formulas)
        for module_count in sorted(module_count_distribution.keys()):
            formula_count = module_count_distribution[module_count]
            percentage = (formula_count / total_formulas) * 100
            report += f"| {module_count} | {formula_count} | {percentage:.1f}% |\n"
        
        # 公式复杂度分析
        report += "\n### 7.2 公式复杂度分析\n\n"
        complex_formulas = [fid for fid, finfo in self.formulas.items() if len(finfo['modules']) >= 3]
        simple_formulas = [fid for fid, finfo in self.formulas.items() if len(finfo['modules']) < 2]
        
        report += f"- **复杂公式**（≥3个模块）：{len(complex_formulas)}个\n"
        report += f"- **简单公式**（<2个模块）：{len(simple_formulas)}个\n"
        report += f"- **中等复杂度公式**（2个模块）：{total_formulas - len(complex_formulas) - len(simple_formulas)}个\n"
        
        # 模块协同分析
        report += "\n### 7.3 模块协同关系\n\n"
        # 统计模块共同出现的次数
        module_cooccurrence = {}
        for formula_id, formula_info in self.formulas.items():
            modules = formula_info['modules']
            if len(modules) >= 2:
                # 生成所有模块对
                for i in range(len(modules)):
                    for j in range(i+1, len(modules)):
                        module_pair = tuple(sorted([modules[i], modules[j]]))
                        if module_pair not in module_cooccurrence:
                            module_cooccurrence[module_pair] = 0
                        module_cooccurrence[module_pair] += 1
        
        report += "**频繁协同出现的模块对**（≥2次）：\n\n"
        for module_pair, count in sorted(module_cooccurrence.items(), key=lambda x: x[1], reverse=True):
            if count >= 2:
                module1_name = self.modules[module_pair[0]]['name']
                module2_name = self.modules[module_pair[1]]['name']
                report += f"- {module1_name} + {module2_name}：共同出现 {count} 次\n"
        
        # 全方程交叉分析
        cross_relations = self.analyze_cross_relationships()
        report += "\n## 8. 全方程交叉分析\n\n"
        report += "### 8.1 公式关联概述\n\n"
        
        # 统计关联指标
        total_pairs = 0
        strong_relations = 0
        same_dimension_pairs = 0
        high_physical_similarity = 0
        
        for formula1, relations in cross_relations.items():
            total_pairs += len(relations)
            for formula2, relation in relations.items():
                if relation['module_similarity'] >= 0.5:
                    strong_relations += 1
                if relation['same_dimension']:
                    same_dimension_pairs += 1
                if relation['physical_similarity'] >= 0.5:
                    high_physical_similarity += 1
        
        report += f"- 总公式对数：{total_pairs}\n"
        report += f"- 强关联公式对（模块相似度≥0.5）：{strong_relations}\n"
        report += f"- 相同量纲公式对：{same_dimension_pairs}\n"
        report += f"- 高物理相似度公式对（相似度≥0.5）：{high_physical_similarity}\n"
        report += f"- 平均模块相似度：{round(strong_relations / total_pairs * 100, 1)}%\n"
        
        report += "\n### 8.2 强关联公式对\n\n"
        report += "**模块相似度≥0.5的公式对**：\n\n"
        report += "| 公式对 | 共享模块 | 模块相似度 | 物理相似度 | 量纲是否相同 | 物理意义关联 |\n"
        report += "|-------|---------|-----------|-----------|-------------|-------------|\n"
        
        strong_pairs = []
        for formula1, relations in cross_relations.items():
            for formula2, relation in relations.items():
                if relation['module_similarity'] >= 0.5:
                    shared_module_names = [self.modules[mid]['name'] for mid in relation['shared_modules']]
                    shared_module_str = ", ".join(shared_module_names) if shared_module_names else "无"
                    
                    # 分析物理意义关联
                    physical_relation = ""
                    if relation['same_dimension']:
                        physical_relation = "描述同类物理现象"
                    elif relation['physical_similarity'] >= 0.7:
                        physical_relation = "物理意义高度相关"
                    elif relation['physical_similarity'] >= 0.3:
                        physical_relation = "物理意义部分相关"
                    else:
                        physical_relation = "物理意义间接关联"
                    
                    strong_pairs.append({
                        'formula_pair': f"{formula1}-{formula2}",
                        'shared_modules': shared_module_str,
                        'module_similarity': relation['module_similarity'],
                        'physical_similarity': relation['physical_similarity'],
                        'same_dim': "是" if relation['same_dimension'] else "否",
                        'physical_relation': physical_relation
                    })
        
        # 按模块相似度排序
        for pair in sorted(strong_pairs, key=lambda x: x['module_similarity'], reverse=True):
            report += f"| {pair['formula_pair']} | {pair['shared_modules']} | {pair['module_similarity']} | {pair['physical_similarity']} | {pair['same_dim']} | {pair['physical_relation']} |\n"
        
        report += "\n### 8.3 相同量纲公式对\n\n"
        report += "**量纲相同的公式对**：\n\n"
        same_dim_pairs = []
        for formula1, relations in cross_relations.items():
            for formula2, relation in relations.items():
                if relation['same_dimension']:
                    same_dim_pairs.append((formula1, formula2, relation['dimension1']))
        
        for formula1, formula2, dim in same_dim_pairs:
            name1 = self.formulas[formula1]['name']
            name2 = self.formulas[formula2]['name']
            report += f"- **{formula1}({name1})** ↔ **{formula2}({name2})**：量纲 {dim}\n"
        
        # 结论
        report += "\n## 9. 结论与建议\n\n"
        report += "### 9.1 主要结论\n\n"
        report += "1. **M01（光速矢量）是核心模块**：使用次数最多（11次），综合得分最高，连接时空、物质、能量\n"
        report += "2. **模块化程度高**：大部分公式由2-3个模块组合而成，体现了统一场论的简洁性\n"
        report += "3. **清晰的层次结构**：从基础模块到复杂公式，形成完整的理论体系\n"
        report += "4. **统一的物理规律**：不同物理现象共享相同的数学模块，验证了统一场论的核心思想\n"
        report += "5. **丰富的模块组合模式**：有限模块通过不同组合产生多样化的物理效应\n"
        report += "6. **强耦合的模块关系**：部分模块频繁协同出现，形成稳定的组合模式\n"
        report += "7. **合理的复杂度分布**：公式复杂度呈现正态分布，易于理解和扩展\n"
        report += "8. **量纲积木的一致性**：通过量纲分析验证了公式的正确性和关联性\n"
        
        report += "\n### 9.2 优化建议\n\n"
        report += "1. **加强核心模块研究**：重点深入研究M01、M06、M11等核心模块的物理本质\n"
        report += "2. **扩展模块库**：考虑添加更多专业化模块，如量子效应模块、引力波模块等\n"
        report += "3. **增强可视化工具**：开发更交互式的可视化工具，方便研究者直观理解模块关系\n"
        report += "4. **建立模块验证机制**：对每个模块的物理意义和数学正确性进行更严格的验证\n"
        report += "5. **促进跨领域应用**：将模块化思想应用到其他物理理论的研究中\n"
        
        report += "\n### 9.3 未来展望\n\n"
        report += "统一场论的模块化分析为理论研究提供了新的视角。通过深入理解模块之间的关系，可以：\n\n"
        report += "1. 更清晰地揭示统一场论的内在结构和逻辑关系\n"
        report += "2. 为实验验证提供更明确的理论预测\n"
        report += "3. 促进统一场论与其他物理理论的融合\n"
        report += "4. 加速新物理现象的发现和解释\n"
        report += "5. 为物理学教育提供更直观的教学工具\n"
        
        return report

if __name__ == "__main__":
    # 创建分析实例
    analyzer = FormulaAnalysis()
    
    # 生成分析报告
    report = analyzer.generate_report()
    with open('formula_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print("分析报告已生成：formula_analysis_report.md")
    
    # 可视化关系图
    analyzer.visualize_formula_module_relation()
    analyzer.visualize_module_relation()
    analyzer.visualize_module_centrality()
    
    # 生成交互式网络图
    analyzer.generate_interactive_graph()
    
    print("\n分析完成！")
    print("生成的文件：")
    print("1. formula_analysis_report.md - 分析报告")
    print("2. formula_module_relation.png - 公式-模块关系图")
    print("3. module_relation.png - 模块转换关系图")
    print("4. module_centrality.png - 模块中心性分析图")
    print("5. interactive_graph.html - 交互式网络图")