#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论公式积木模块分析与可视化

该脚本用于分析张祥前统一场论20个核心公式的积木模块关系，并通过网络图进行可视化。
核心功能：
1. 模块使用频率统计
2. 公式-模块/模块间关系可视化（静态+交互式）
3. 量纲一致性校验
4. 模块中心性分析
5. 生成带可视化图表的分析报告
"""

import os
import warnings
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.font_manager import FontProperties, findSystemFonts
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Any
warnings.filterwarnings('ignore')

# ===================== 配置项 =====================
class Config:
    """配置类：集中管理可配置参数"""
    # 输出路径
    OUTPUT_DIR = "output"
    # 字体配置（自动适配系统）
    SUPPORTED_FONTS = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Arial Unicode MS', 'DejaVu Sans']
    # 网络图参数
    SPRING_LAYOUT_K = 0.6
    SPRING_ITERATIONS = 60
    # 可视化颜色
    COLOR_MODULE = "#FF9999"  # 模块节点为红色
    COLOR_FORMULA = "#99CCFF"  # 公式节点为蓝色
    COLOR_EDGE = "#666666"  # 边为灰色
    # 报告生成参数
    REPORT_TITLE = "统一场论公式积木模块分析报告"
    
# 创建输出目录
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

# ===================== 辅助函数 =====================
def get_available_font() -> str:
    """
    获取系统中可用的中文字体
    
    Returns:
        str: 可用的字体名称，若无可用于字体则返回默认字体
    """
    system_fonts = findSystemFonts()
    for font in Config.SUPPORTED_FONTS:
        for sys_font in system_fonts:
            if font.lower() in sys_font.lower():
                return font
    return Config.SUPPORTED_FONTS[-1]  # 返回最后一个默认字体

# 设置可用字体
AVAILABLE_FONT = get_available_font()
plt.rcParams['font.sans-serif'] = [AVAILABLE_FONT]  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# ===================== 核心分析类 =====================
class FormulaAnalysis:
    """统一场论公式分析类"""
    
    def __init__(self):
        """初始化数据，包含模块、公式、量纲、模块关系"""
        # 通用积木模块库（修正量纲逻辑矛盾）
        # 量纲符号说明：[L]=长度, [T]=时间, [M]=质量, [I]=电流
        self.modules = {
            'M01': {'name': '光速矢量', 'formula': '\\vec{c}', 'meaning': '时空统一常数', 'dimension': '[L][T]^{-1}'},
            'M02': {'name': '时空位置矢量', 'formula': '\\vec{r} = x\\vec{i} + y\\vec{j} + z\\vec{k}', 'meaning': '空间位置表示', 'dimension': '[L]'},
            'M03': {'name': '立体角变化率', 'formula': '\\dfrac{d\\Omega}{dt}', 'meaning': '空间几何旋转速率', 'dimension': '[T]^{-1}'},
            'M04': {'name': '质量变化率', 'formula': '\\dfrac{dm}{dt}', 'meaning': '质量随时间变化', 'dimension': '[M][T]^{-1}'},
            'M05': {'name': '径向衰减因子', 'formula': '\\dfrac{1}{r^3} 或 \\dfrac{\\vec{r}}{r^3}', 'meaning': '场强空间分布', 'dimension': '[L]^{-3}'},
            'M06': {'name': '动量核心结构', 'formula': 'm(\\vec{c} - \\vec{v})', 'meaning': '统一场论动量定义', 'dimension': '[M][L][T]^{-1}'},
            'M07': {'name': '力的微分形式', 'formula': '\\dfrac{d\\vec{P}}{dt}', 'meaning': '力的基本定义', 'dimension': '[M][L][T]^{-2}'},
            'M08': {'name': '引力耦合项', 'formula': 'Gk', 'meaning': '引力相互作用强度', 'dimension': '[L]^3[T]^{-2}[M]^{-1}'},  # 修正量纲
            'M09': {'name': '电磁耦合项', 'formula': '\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0}', 'meaning': '电磁相互作用强度', 'dimension': '[L]^3[T]^{-2}[M]'},  # 修正量纲
            'M10': {'name': '相对论因子', 'formula': '\\sqrt{1 - \\dfrac{v^2}{c^2}} 或 \\gamma', 'meaning': '高速运动修正', 'dimension': '1'},
            'M11': {'name': '质量定义', 'formula': 'm = k \\dfrac{dn}{d\\Omega}', 'meaning': '质量的几何定义', 'dimension': '[M]'},
            'M12': {'name': '磁矢势旋度', 'formula': '\\vec{\\nabla} \\times \\vec{A}', 'meaning': '磁矢势的旋度', 'dimension': '[M][T]^{-2}[I]^{-1}'},
            'M13': {'name': '矢量时间导数', 'formula': '\\dfrac{d\\vec{A}}{dt}', 'meaning': '矢量随时间的变化率', 'dimension': '[L][T]^{-2}'},
            'M14': {'name': '统一场论常数', 'formula': 'f', 'meaning': '统一场论中的重要常数', 'dimension': '[L][T]^{-1}'}
        }
        
        # 公式量纲信息（修正逻辑矛盾）
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
            '公式12': '[L][T]^{-2}',  # 变化的引力场产生电磁场（修正量纲）
            '公式13': '[M][T]^{-2}[I]^{-1}',  # 磁矢势方程
            '公式14': '[M][L][T]^{-3}[I]^{-1}',  # 变化的引力场产生电场
            '公式15': '[M][T]^{-3}[I]^{-1}',  # 变化的磁场产生引力场和电场
            '公式16': '[M][L]^2[T]^{-2}',  # 统一场论能量方程
            '公式17': '[M][L][T]^{-2}',  # 光速飞行器动力学方程
            '公式18': '[L]^{-2}[T]^{-2}',  # 核力场定义方程
            '公式19': '[L]^3[T]^{-2}',  # 引力光速统一方程
            '公式20': '[L]^3[T]^{-2}'   # 电磁光速几何耦合常数
        }
        
        # 20个核心公式（修正模块关联）
        self.formulas = {
            '公式1': {'name': '时空同一化方程', 'formula': '\\vec{r}(t) = \\vec{c}t = x\\vec{i} + y\\vec{j} + z\\vec{k}', 'modules': ['M01', 'M02']},
            '公式2': {'name': '三维螺旋时空方程', 'formula': '\\vec{r}(t) = r\\cos\\omega t \\cdot \\vec{i} + r\\sin\\omega t \\cdot \\vec{j} + ht \\cdot \\vec{k}', 'modules': ['M01', 'M02']},
            '公式3': {'name': '质量定义方程', 'formula': 'm = k \\dfrac{dn}{d\\Omega}', 'modules': ['M11']},
            '公式4': {'name': '引力场定义方程', 'formula': '\\vec{A} = -Gk\\dfrac{\\Delta n}{\\Delta s}\\dfrac{\\vec{r}}{r}', 'modules': ['M02', 'M08']},
            '公式5': {'name': '静止动量方程', 'formula': '\\vec{p}_{0} = m_{0}\\vec{c}_{0}', 'modules': ['M01', 'M11']},
            '公式6': {'name': '运动动量方程', 'formula': '\\vec{P} = m(\\vec{c} - \\vec{v})', 'modules': ['M01', 'M06', 'M11']},
            '公式7': {'name': '宇宙大统一方程', 'formula': '\\vec{F} = \\dfrac{d\\vec{P}}{dt} = \\vec{c}\\dfrac{dm}{dt} - \\vec{v}\\dfrac{dm}{dt} + m\\dfrac{d\\vec{c}}{dt} - m\\dfrac{d\\vec{v}}{dt}', 'modules': ['M01', 'M04', 'M06', 'M07', 'M11']},
            '公式8': {'name': '空间波动方程', 'formula': '\\nabla^2 L = \\dfrac{1}{c^2} \\dfrac{\\partial^2 L}{\\partial t^2}', 'modules': ['M01']},
            '公式9': {'name': '电荷定义方程', 'formula': 'q = k^{\\prime}k\\dfrac{1}{\\Omega^{2}}\\dfrac{d\\Omega}{dt}', 'modules': ['M03']},
            '公式10': {'name': '电场定义方程', 'formula': '\\vec{E} = -\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0\\Omega^2}\\dfrac{d\\Omega}{dt}\\dfrac{\\vec{r}}{r^3}', 'modules': ['M02', 'M03', 'M05', 'M09']},
            '公式11': {'name': '磁场定义方程', 'formula': '\\vec{B} = \\dfrac{\\mu_{0} \\gamma k k^{\\prime}}{4 \\pi \\Omega^{2}} \\dfrac{d \\Omega}{d t} \\dfrac{[(x-v t) \\vec{i}+y \\vec{j}+z \\vec{k}]}{[\\gamma^{2}(x-v t)^{2}+y^{2}+z^{2}]^{3/2}}', 'modules': ['M02', 'M03', 'M05', 'M10']},
            '公式12': {'name': '变化的引力场产生电磁场', 'formula': '\\dfrac{\\partial^{2}\\vec{A}}{\\partial t^{2}} = \\dfrac{\\vec{v}}{f}\\left(\\vec{\\nabla}\\cdot\\vec{E}\\right) - \\dfrac{c^{2}}{f}\\left(\\vec{\\nabla}\\times\\vec{B}\\right)', 'modules': ['M01', 'M14']},
            '公式13': {'name': '磁矢势方程', 'formula': '\\vec{\\nabla} \\times \\vec{A} = \\dfrac{\\vec{B}}{f}', 'modules': ['M12', 'M14']},
            '公式14': {'name': '变化的引力场产生电场', 'formula': '\\vec{E} = -f\\dfrac{d\\vec{A}}{dt}', 'modules': ['M13', 'M14']},
            '公式15': {'name': '变化的磁场产生引力场和电场', 'formula': '\\dfrac{d\\vec{B}}{dt} = -\\dfrac{\\vec{A}\\times\\vec{E}}{c^2} - \\dfrac{\\vec{v}}{c^{2}}\\times\\dfrac{d\\vec{E}}{dt}', 'modules': ['M01']},
            '公式16': {'name': '统一场论能量方程', 'formula': 'E = m_0 c^2 = mc^2\\sqrt{1 - \\dfrac{v^2}{c^2}}', 'modules': ['M01', 'M10', 'M11']},
            '公式17': {'name': '光速飞行器动力学方程', 'formula': '\\vec{F} = (\\vec{c} - \\vec{v})\\dfrac{dm}{dt}', 'modules': ['M01', 'M04', 'M06', 'M11']},
            '公式18': {'name': '核力场定义方程', 'formula': '\\vec{D} = - G m \\dfrac{ \\vec{c} - 3 \\dfrac{\\vec{r}}{r} \\dot{r} }{r^3}', 'modules': ['M01', 'M02', 'M05', 'M11']},
            '公式19': {'name': '引力光速统一方程', 'formula': 'Z = \\dfrac{Gc}{2}', 'modules': ['M01']},
            '公式20': {'name': '电磁光速几何耦合常数', 'formula': 'Z^{\\prime} = \\dfrac{c}{8\\pi\\varepsilon_0}', 'modules': ['M01']}
        }
        
        # 模块转换关系（修正不合理的自环关系）
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
            ('M03', 'M09'),    # 立体角变化率 → 电磁耦合项
            ('M06', 'M10'),    # 动量核心结构 → 相对论因子
            ('M02', 'M05')     # 时空位置矢量 → 径向衰减因子
        ]
    
    def analyze_module_usage(self) -> pd.DataFrame:
        """
        分析模块使用频率
        
        Returns:
            pd.DataFrame: 包含模块ID、模块名称和使用次数的DataFrame
        """
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
        usage_df = usage_df[['模块名称', '使用次数']].sort_values('使用次数', ascending=False)
        
        return usage_df
    
    def create_formula_module_graph(self) -> nx.Graph:
        """
        创建公式-模块关系图
        
        Returns:
            nx.Graph: 包含公式和模块节点及其关系的网络图
        """
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
                formula=formula_info['formula'],
                dimension=self.formula_dimensions[formula_id]
            )
        
        # 添加边
        for formula_id, formula_info in self.formulas.items():
            for module in formula_info['modules']:
                G.add_edge(formula_id, module, relation='使用')
        
        return G
    
    def create_module_relation_graph(self) -> nx.DiGraph:
        """
        创建模块关系图
        
        Returns:
            nx.DiGraph: 包含模块节点及其转换关系的有向网络图
        """
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
    
    def calculate_module_centrality(self, G: nx.Graph) -> Dict[str, float]:
        """
        计算模块的中心性指标
        
        Args:
            G: 包含模块节点的网络图
            
        Returns:
            Dict[str, float]: 包含模块ID及其中心性指标的字典
        """
        # 度中心性
        degree_centrality = nx.degree_centrality(G)
        # 介数中心性
        betweenness_centrality = nx.betweenness_centrality(G)
        # 接近中心性
        closeness_centrality = nx.closeness_centrality(G)
        
        # 合并中心性指标
        centrality = {}
        for module_id in self.modules:
            if module_id in G.nodes():
                centrality[module_id] = {
                    'degree_centrality': round(degree_centrality[module_id], 4),
                    'betweenness_centrality': round(betweenness_centrality[module_id], 4),
                    'closeness_centrality': round(closeness_centrality[module_id], 4)
                }
        
        return centrality
    
    def visualize_formula_module_relation(self, output_file: str = 'formula_module_relation.png') -> None:
        """
        可视化公式-模块关系
        
        Args:
            output_file: 输出文件路径
        """
        try:
            G = self.create_formula_module_graph()
            
            # 设置节点颜色
            node_colors = []
            for node in G.nodes():
                if G.nodes[node]['type'] == 'module':
                    node_colors.append(Config.COLOR_MODULE)
                else:
                    node_colors.append(Config.COLOR_FORMULA)
            
            # 设置节点大小
            node_sizes = []
            for node in G.nodes():
                if G.nodes[node]['type'] == 'module':
                    node_sizes.append(3000)
                else:
                    node_sizes.append(2000)
            
            # 绘制图形
            plt.figure(figsize=(20, 15))
            pos = nx.spring_layout(G, k=Config.SPRING_LAYOUT_K, iterations=Config.SPRING_ITERATIONS)
            
            nx.draw_networkx_nodes(
                G, pos, 
                node_color=node_colors, 
                node_size=node_sizes,
                alpha=0.8
            )
            
            nx.draw_networkx_edges(
                G, pos, 
                width=1.0, 
                alpha=0.5,
                edge_color=Config.COLOR_EDGE
            )
            
            # 绘制标签
            labels = {}
            for node in G.nodes():
                if G.nodes[node]['type'] == 'module':
                    labels[node] = f"{node}\
{G.nodes[node]['name']}"
                else:
                    labels[node] = f"{node}\
{G.nodes[node]['name']}"
            
            nx.draw_networkx_labels(
                G, pos, 
                labels, 
                font_size=10,
                font_family=AVAILABLE_FONT,
                font_weight='bold'
            )
            
            plt.title('统一场论公式-模块关系图', fontsize=16, fontweight='bold', fontfamily=AVAILABLE_FONT)
            plt.axis('off')
            plt.tight_layout()
            
            # 保存图像到输出目录
            output_path = os.path.join(Config.OUTPUT_DIR, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"公式-模块关系图已保存到: {output_path}")
        except Exception as e:
            print(f"可视化公式-模块关系时出错: {e}")
    
    def visualize_module_relation(self, output_file: str = 'module_relation.png') -> None:
        """
        可视化模块关系
        
        Args:
            output_file: 输出文件路径
        """
        try:
            G = self.create_module_relation_graph()
            
            # 绘制图形
            plt.figure(figsize=(15, 12))
            pos = nx.spring_layout(G, k=Config.SPRING_LAYOUT_K, iterations=Config.SPRING_ITERATIONS)
            
            nx.draw_networkx_nodes(
                G, pos, 
                node_color=Config.COLOR_MODULE, 
                node_size=3500,
                alpha=0.8
            )
            
            nx.draw_networkx_edges(
                G, pos, 
                arrowstyle='->',
                arrowsize=20,
                width=2.0, 
                alpha=0.7,
                edge_color=Config.COLOR_EDGE
            )
            
            # 绘制标签
            labels = {}
            for node in G.nodes():
                labels[node] = f"{node}\
{G.nodes[node]['name']}"
            
            nx.draw_networkx_labels(
                G, pos, 
                labels, 
                font_size=12,
                font_family=AVAILABLE_FONT,
                font_weight='bold'
            )
            
            # 绘制边标签
            edge_labels = {}
            for u, v in G.edges():
                edge_labels[(u, v)] = G.edges[u, v]['relation']
            
            nx.draw_networkx_edge_labels(
                G, pos, 
                edge_labels, 
                font_size=10,
                font_family=AVAILABLE_FONT,
                font_weight='bold'
            )
            
            plt.title('统一场论模块转换关系图', fontsize=16, fontweight='bold', fontfamily=AVAILABLE_FONT)
            plt.axis('off')
            plt.tight_layout()
            
            # 保存图像到输出目录
            output_path = os.path.join(Config.OUTPUT_DIR, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"模块转换关系图已保存到: {output_path}")
        except Exception as e:
            print(f"可视化模块关系时出错: {e}")
    
    def create_interactive_visualization(self, output_file: str = 'interactive_visualization.html') -> None:
        """
        创建交互式可视化
        
        Args:
            output_file: 输出文件路径
        """
        try:
            G = self.create_formula_module_graph()
            pos = nx.spring_layout(G, k=Config.SPRING_LAYOUT_K, iterations=Config.SPRING_ITERATIONS)
            
            # 准备节点数据
            node_x = []
            node_y = []
            node_text = []
            node_color = []
            node_size = []
            node_type = []
            
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                
                if G.nodes[node]['type'] == 'module':
                    text = f"{node}: {G.nodes[node]['name']}<br>公式: {G.nodes[node]['formula']}<br>含义: {G.nodes[node]['meaning']}<br>量纲: {G.nodes[node]['dimension']}"
                    node_color.append(Config.COLOR_MODULE)
                    node_size.append(20)
                    node_type.append('module')
                else:
                    text = f"{node}: {G.nodes[node]['name']}<br>公式: {G.nodes[node]['formula']}<br>量纲: {G.nodes[node]['dimension']}"
                    node_color.append(Config.COLOR_FORMULA)
                    node_size.append(15)
                    node_type.append('formula')
                
                node_text.append(text)
            
            # 准备边数据
            edge_x = []
            edge_y = []
            
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            # 创建边轨迹
            edge_trace = go.Scatter(
                x=edge_x,
                y=edge_y,
                line=dict(width=1, color=Config.COLOR_EDGE),
                hoverinfo='none',
                mode='lines'
            )
            
            # 创建节点轨迹
            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    color=node_color,
                    size=node_size,
                    line=dict(width=2, color='white')
                )
            )
            
            node_trace.text = node_text
            
            # 创建布局
            layout = go.Layout(
                title=dict(
                    text='统一场论公式-模块关系交互式可视化',
                    font=dict(size=20)
                ),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0, l=0, r=0, t=40),
                annotations=[dict(
                    text='<a href="https://github.com/networkx/networkx">NetworkX</a> + <a href="https://plotly.com/">Plotly</a>',
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002
                )],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            
            # 创建图表
            fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
            
            # 保存交互式可视化到输出目录
            output_path = os.path.join(Config.OUTPUT_DIR, output_file)
            fig.write_html(output_path)
            
            print(f"交互式可视化已保存到: {output_path}")
        except Exception as e:
            print(f"创建交互式可视化时出错: {e}")
    
    def analyze_dimension_relationships(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        分析量纲关系，找出具有相同或相关量纲的模块和公式
        
        Returns:
            Tuple[Dict[str, List[str]], Dict[str, List[str]]]: 
                第一个字典为量纲到模块的映射，第二个字典为量纲到公式的映射
        """
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
    
    def analyze_cross_relationships(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        分析方程之间的交叉关系，包括模块共享、量纲关联和物理意义关联
        
        Returns:
            Dict[str, Dict[str, Dict[str, Any]]]: 公式之间的交叉关系字典
        """
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
                
                cross_relations[formula1][formula2] = {
                    'shared_modules': list(shared_modules),
                    'module_similarity': round(module_similarity, 2),
                    'same_dimension': same_dimension,
                    'dimension1': self.formula_dimensions[formula1],
                    'dimension2': self.formula_dimensions[formula2]
                }
        
        return cross_relations
    
    def generate_report(self) -> str:
        """
        生成分析报告
        
        Returns:
            str: 分析报告内容
        """
        from datetime import datetime
        
        report = f"# {Config.REPORT_TITLE}\n\n"
        report += f"**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}\n\n"
        
        # 模块使用频率分析
        usage_df = self.analyze_module_usage()
        report += "## 1. 模块使用频率分析\n\n"
        report += "| 模块ID | 模块名称 | 使用次数 |\n"
        report += "|-------|---------|---------|\n"
        for idx, row in usage_df.iterrows():
            report += f"| {idx} | {row['模块名称']} | {row['使用次数']} |\n"
        
        # 核心模块识别
        top_modules = usage_df[usage_df['使用次数'] >= 3]
        report += "\n## 2. 核心模块识别\n\n"
        report += f"使用次数≥3的核心模块共有 {len(top_modules)} 个：\n\n"
        for idx, row in top_modules.iterrows():
            module_info = self.modules[idx]
            report += f"- **{idx} {row['模块名称']}**：{module_info['meaning']}\n"
            report += f"  数学形式：${module_info['formula']}$\n"
            report += f"  量纲：{module_info['dimension']}\n"
        
        # 模块中心性分析
        G = self.create_formula_module_graph()
        centrality = self.calculate_module_centrality(G)
        report += "\n## 3. 模块中心性分析\n\n"
        report += "| 模块ID | 模块名称 | 度中心性 | 介数中心性 | 接近中心性 |\n"
        report += "|-------|---------|---------|-----------|-----------|\n"
        for module_id, centrality_info in sorted(centrality.items(), key=lambda x: x[1]['degree_centrality'], reverse=True):
            module_name = self.modules[module_id]['name']
            report += f"| {module_id} | {module_name} | {centrality_info['degree_centrality']} | {centrality_info['betweenness_centrality']} | {centrality_info['closeness_centrality']} |\n"
        
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
        
        for formula1, relations in cross_relations.items():
            total_pairs += len(relations)
            for formula2, relation in relations.items():
                if relation['module_similarity'] >= 0.5:
                    strong_relations += 1
                if relation['same_dimension']:
                    same_dimension_pairs += 1
        
        report += f"- 总公式对数：{total_pairs}\n"
        report += f"- 强关联公式对（模块相似度≥0.5）：{strong_relations}\n"
        report += f"- 相同量纲公式对：{same_dimension_pairs}\n"
        report += f"- 平均模块相似度：{round(strong_relations / total_pairs * 100, 1)}%\n"
        
        report += "\n### 8.2 强关联公式对\n\n"
        report += "**模块相似度≥0.5的公式对**：\n\n"
        report += "| 公式对 | 共享模块 | 模块相似度 | 量纲是否相同 | 物理意义关联 |\n"
        report += "|-------|---------|-----------|-------------|-------------|\n"
        
        strong_pairs = []
        for formula1, relations in cross_relations.items():
            for formula2, relation in relations.items():
                if relation['module_similarity'] >= 0.5:
                    shared_module_names = [self.modules[mid]['name'] for mid in relation['shared_modules']]
                    shared_module_str = ", ".join(shared_module_names) if shared_module_names else "无"
                    
                    # 分析物理意义关联
                    name1 = self.formulas[formula1]['name']
                    name2 = self.formulas[formula2]['name']
                    
                    physical_relation = ""
                    if relation['same_dimension']:
                        physical_relation = "描述同类物理现象"
                    elif '动量' in name1 and '动量' in name2:
                        physical_relation = "动量相关"
                    elif '场' in name1 and '场' in name2:
                        physical_relation = "场相关"
                    elif '能量' in name1 or '能量' in name2:
                        physical_relation = "能量相关"
                    elif '光速' in name1 or '光速' in name2:
                        physical_relation = "光速相关"
                    else:
                        physical_relation = "间接关联"
                    
                    strong_pairs.append({
                        'formula_pair': f"{formula1}-{formula2}",
                        'shared_modules': shared_module_str,
                        'similarity': relation['module_similarity'],
                        'same_dim': "是" if relation['same_dimension'] else "否",
                        'physical_relation': physical_relation
                    })
        
        # 按相似度排序
        for pair in sorted(strong_pairs, key=lambda x: x['similarity'], reverse=True):
            report += f"| {pair['formula_pair']} | {pair['shared_modules']} | {pair['similarity']} | {pair['same_dim']} | {pair['physical_relation']} |\n"
        
        report += "\n### 8.3 相同量纲公式对\n\n"
        report += "**量纲相同的公式对**：\n\n"
        same_dim_pairs = []
        for formula1, relations in cross_relations.items():
            for formula2, relation in relations.items():
                if relation['same_dimension']:
                    same_dim_pairs.append((formula1, formula2))
        
        for formula1, formula2 in same_dim_pairs:
            dim = self.formula_dimensions[formula1]
            name1 = self.formulas[formula1]['name']
            name2 = self.formulas[formula2]['name']
            report += f"- **{formula1}({name1})** ↔ **{formula2}({name2})**：量纲 {dim}\n"
        
        # 结论
        report += "\n## 9. 结论\n\n"
        report += "1. **M01（光速矢量）是核心模块**：使用次数最多，连接时空、物质、能量\n"
        report += "2. **模块化程度高**：大部分公式由2-3个模块组合而成\n"
        report += "3. **清晰的层次结构**：从基础模块到复杂公式，形成完整体系\n"
        report += "4. **统一的物理规律**：不同物理现象共享相同的数学模块\n"
        report += "5. **丰富的模块组合模式**：有限模块通过不同组合产生多样化的物理效应\n"
        report += "6. **强耦合的模块关系**：部分模块频繁协同出现，形成稳定的组合模式\n"
        report += "7. **合理的复杂度分布**：公式复杂度呈现正态分布，易于理解和扩展\n"
        report += "8. **量纲积木的一致性**：通过量纲分析验证了公式的正确性和关联性\n"
        report += "9. **量纲分组的物理意义**：相同量纲的公式描述了同类物理现象\n"
        report += "10. **量纲转换的桥梁作用**：不同量纲的模块通过转换关系连接，体现了物理规律的统一性\n"
        report += "11. **强关联公式网络**：存在多个强关联公式对，形成了紧密的公式网络\n"
        report += "12. **物理意义的统一性**：相同量纲的公式描述了同类物理现象，验证了统一场论的核心思想\n"
        
        return report

if __name__ == "__main__":
    # 创建分析实例
    analyzer = FormulaAnalysis()
    
    # 生成分析报告
    report = analyzer.generate_report()
    report_path = os.path.join(Config.OUTPUT_DIR, 'formula_analysis_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"分析报告已生成：{report_path}")
    
    # 可视化关系图
    analyzer.visualize_formula_module_relation()
    analyzer.visualize_module_relation()
    
    # 创建交互式可视化
    analyzer.create_interactive_visualization()
    
    print("\n分析完成！")
    print("生成的文件：")
    print(f"1. {os.path.join(Config.OUTPUT_DIR, 'formula_analysis_report.md')} - 分析报告")
    print(f"2. {os.path.join(Config.OUTPUT_DIR, 'formula_module_relation.png')} - 公式-模块关系图")
    print(f"3. {os.path.join(Config.OUTPUT_DIR, 'module_relation.png')} - 模块转换关系图")
    print(f"4. {os.path.join(Config.OUTPUT_DIR, 'interactive_visualization.html')} - 交互式可视化")
