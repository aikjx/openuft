#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论模块关系网络验证
该脚本用于验证统一场论模块之间的转换关系是否合理，分析模块网络的结构特性
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Tuple, Any

class ModuleRelationValidator:
    """模块关系网络验证器"""
    
    def __init__(self):
        """初始化数据"""
        # 通用积木模块库
        self.modules = {
            'M01': {'name': '光速矢量', 'formula': '\\vec{c}', 'meaning': '时空统一常数'},
            'M02': {'name': '时空位置矢量', 'formula': '\\vec{r} = x\\vec{i} + y\\vec{j} + z\\vec{k}', 'meaning': '空间位置表示'},
            'M03': {'name': '立体角变化率', 'formula': '\\dfrac{d\\Omega}{dt}', 'meaning': '空间几何旋转速率'},
            'M04': {'name': '质量变化率', 'formula': '\\dfrac{dm}{dt}', 'meaning': '质量随时间变化'},
            'M05': {'name': '径向衰减因子', 'formula': '\\dfrac{1}{r^3} 或 \\dfrac{\\vec{r}}{r^3}', 'meaning': '场强空间分布'},
            'M06': {'name': '动量核心结构', 'formula': 'm(\\vec{c} - \\vec{v})', 'meaning': '统一场论动量定义'},
            'M07': {'name': '力的微分形式', 'formula': '\\dfrac{d\\vec{P}}{dt}', 'meaning': '力的基本定义'},
            'M08': {'name': '引力耦合项', 'formula': 'Gk', 'meaning': '引力相互作用强度'},
            'M09': {'name': '电磁耦合项', 'formula': '\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0}', 'meaning': '电磁相互作用强度'},
            'M10': {'name': '相对论因子', 'formula': '\\sqrt{1 - \\dfrac{v^2}{c^2}} 或 \\gamma', 'meaning': '高速运动修正'},
            'M11': {'name': '质量定义', 'formula': 'm = k \\dfrac{dn}{d\\Omega}', 'meaning': '质量的几何定义'},
            'M12': {'name': '磁矢势旋度', 'formula': '\\vec{\\nabla} \\times \\vec{A}', 'meaning': '磁矢势的旋度'},
            'M13': {'name': '矢量时间导数', 'formula': '\\dfrac{d\\vec{A}}{dt}', 'meaning': '矢量随时间的变化率'},
            'M14': {'name': '统一场论常数', 'formula': 'f', 'meaning': '统一场论中的重要常数'}
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
            ('M03', 'M09'),    # 立体角变化率 → 电磁耦合项
            ('M06', 'M10'),    # 动量核心结构 → 相对论因子
            ('M02', 'M05')     # 时空位置矢量 → 径向衰减因子
        ]
        
        # 公式使用的模块
        self.formula_modules = {
            '公式1': ['M01', 'M02'],
            '公式2': ['M01', 'M02'],
            '公式3': ['M11'],
            '公式4': ['M02', 'M08'],
            '公式5': ['M01', 'M11'],
            '公式6': ['M01', 'M06', 'M11'],
            '公式7': ['M01', 'M04', 'M06', 'M07', 'M11'],
            '公式8': ['M01'],
            '公式9': ['M03'],
            '公式10': ['M02', 'M03', 'M05', 'M09'],
            '公式11': ['M02', 'M03', 'M05', 'M10'],
            '公式12': ['M01', 'M14'],
            '公式13': ['M12', 'M14'],
            '公式14': ['M13', 'M14'],
            '公式15': ['M01'],
            '公式16': ['M01', 'M10', 'M11'],
            '公式17': ['M01', 'M04', 'M06', 'M11'],
            '公式18': ['M01', 'M02', 'M05', 'M11'],
            '公式19': ['M01'],
            '公式20': ['M01']
        }
        
        # 模块分类
        self.module_categories = {
            '基础模块': ['M01', 'M02'],
            '几何模块': ['M03', 'M05'],
            '动力学模块': ['M04', 'M06', 'M07'],
            '耦合模块': ['M08', 'M09', 'M14'],
            '修正模块': ['M10'],
            '定义模块': ['M11'],
            '电磁模块': ['M12', 'M13']
        }
    
    def create_relation_graph(self) -> nx.DiGraph:
        """
        创建模块关系图
        
        Returns:
            nx.DiGraph: 模块关系有向图
        """
        G = nx.DiGraph()
        
        # 添加模块节点
        for module_id, module_info in self.modules.items():
            G.add_node(
                module_id,
                name=module_info['name'],
                formula=module_info['formula'],
                meaning=module_info['meaning']
            )
        
        # 添加边
        for source, target in self.module_relations:
            G.add_edge(source, target, relation='转换为')
        
        return G
    
    def analyze_network_properties(self, G: nx.DiGraph) -> Dict[str, Any]:
        """
        分析网络特性
        
        Args:
            G: 模块关系图
            
        Returns:
            Dict[str, Any]: 网络特性分析结果
        """
        properties = {}
        
        # 基本统计
        properties['nodes'] = G.number_of_nodes()
        properties['edges'] = G.number_of_edges()
        properties['density'] = nx.density(G)
        
        # 中心性分析
        properties['degree_centrality'] = nx.degree_centrality(G)
        properties['betweenness_centrality'] = nx.betweenness_centrality(G)
        properties['closeness_centrality'] = nx.closeness_centrality(G)
        
        # 连通性分析
        properties['weakly_connected_components'] = list(nx.weakly_connected_components(G))
        properties['strongly_connected_components'] = list(nx.strongly_connected_components(G))
        
        # 路径分析
        properties['average_shortest_path_length'] = nx.average_shortest_path_length(G) if nx.is_strongly_connected(G) else None
        
        # 模块性分析
        properties['modularity'] = self.analyze_modularity(G)
        
        return properties
    
    def analyze_modularity(self, G: nx.DiGraph) -> float:
        """
        分析模块性
        
        Args:
            G: 模块关系图
            
        Returns:
            float: 模块性指标
        """
        # 基于预定义分类计算模块性
        modularity = 0.0
        total_edges = G.number_of_edges()
        
        if total_edges == 0:
            return 0.0
        
        # 计算同一类别内的边数
        same_category_edges = 0
        for source, target in G.edges():
            # 查找源节点和目标节点的类别
            source_category = None
            target_category = None
            
            for category, modules in self.module_categories.items():
                if source in modules:
                    source_category = category
                if target in modules:
                    target_category = category
            
            if source_category and target_category and source_category == target_category:
                same_category_edges += 1
        
        # 计算模块性
        modularity = same_category_edges / total_edges
        return modularity
    
    def validate_relation_consistency(self) -> List[Dict[str, Any]]:
        """
        验证模块关系一致性
        
        Returns:
            List[Dict[str, Any]]: 验证结果
        """
        results = []
        
        # 检查循环依赖
        G = self.create_relation_graph()
        try:
            cycles = list(nx.simple_cycles(G))
            if cycles:
                results.append({
                    'type': '循环依赖',
                    'status': '警告',
                    'description': f'发现循环依赖: {cycles}',
                    'severity': 'medium'
                })
            else:
                results.append({
                    'type': '循环依赖',
                    'status': '正常',
                    'description': '未发现循环依赖',
                    'severity': 'low'
                })
        except:
            results.append({
                'type': '循环依赖',
                'status': '错误',
                'description': '无法分析循环依赖',
                'severity': 'high'
            })
        
        # 检查孤立节点
        isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]
        if isolated_nodes:
            results.append({
                'type': '孤立节点',
                'status': '警告',
                'description': f'发现孤立节点: {isolated_nodes}',
                'severity': 'medium'
            })
        else:
            results.append({
                'type': '孤立节点',
                'status': '正常',
                'description': '无孤立节点',
                'severity': 'low'
            })
        
        # 检查入度为0的节点（源节点）
        in_degree_zero = [node for node in G.nodes() if G.in_degree(node) == 0]
        if len(in_degree_zero) > 3:
            results.append({
                'type': '源节点过多',
                'status': '警告',
                'description': f'源节点过多: {in_degree_zero}',
                'severity': 'medium'
            })
        else:
            results.append({
                'type': '源节点数量',
                'status': '正常',
                'description': f'源节点数量合理: {in_degree_zero}',
                'severity': 'low'
            })
        
        # 检查出度为0的节点（汇节点）
        out_degree_zero = [node for node in G.nodes() if G.out_degree(node) == 0]
        if len(out_degree_zero) > 5:
            results.append({
                'type': '汇节点过多',
                'status': '警告',
                'description': f'汇节点过多: {out_degree_zero}',
                'severity': 'medium'
            })
        else:
            results.append({
                'type': '汇节点数量',
                'status': '正常',
                'description': f'汇节点数量合理: {out_degree_zero}',
                'severity': 'low'
            })
        
        return results
    
    def analyze_module_usage(self) -> Dict[str, Any]:
        """
        分析模块使用情况
        
        Returns:
            Dict[str, Any]: 模块使用分析结果
        """
        usage = {}
        
        # 统计每个模块的使用次数
        module_counts = {module_id: 0 for module_id in self.modules}
        for formula, modules in self.formula_modules.items():
            for module in modules:
                if module in module_counts:
                    module_counts[module] += 1
        
        usage['module_counts'] = module_counts
        usage['most_used'] = max(module_counts, key=module_counts.get)
        usage['least_used'] = min(module_counts, key=module_counts.get)
        usage['average_usage'] = sum(module_counts.values()) / len(module_counts)
        
        # 分析模块在不同公式类型中的分布
        formula_types = {
            '时空公式': ['公式1', '公式2', '公式8'],
            '质量动量公式': ['公式3', '公式4', '公式5', '公式6', '公式7', '公式17'],
            '电磁公式': ['公式9', '公式10', '公式11', '公式12', '公式13', '公式14', '公式15'],
            '能量公式': ['公式16'],
            '耦合公式': ['公式18', '公式19', '公式20']
        }
        
        usage['formula_type_distribution'] = {}
        for formula_type, formulas in formula_types.items():
            type_modules = set()
            for formula in formulas:
                if formula in self.formula_modules:
                    type_modules.update(self.formula_modules[formula])
            usage['formula_type_distribution'][formula_type] = list(type_modules)
        
        return usage
    
    def validate_physical_consistency(self) -> List[Dict[str, Any]]:
        """
        验证物理意义一致性
        
        Returns:
            List[Dict[str, Any]]: 物理意义一致性验证结果
        """
        results = []
        
        # 检查基础模块关系
        basic_relations = [
            ('M01', 'M06'),  # 光速矢量应该用于动量定义
            ('M06', 'M07'),  # 动量应该用于力的定义
            ('M03', 'M09'),  # 立体角变化率应该用于电磁耦合
            ('M01', 'M10')   # 光速应该用于相对论因子
        ]
        
        for source, target in basic_relations:
            if (source, target) in self.module_relations:
                results.append({
                    'relation': f'{self.modules[source]["name"]} → {self.modules[target]["name"]}',
                    'status': '✓',
                    'description': '物理意义合理'
                })
            else:
                results.append({
                    'relation': f'{self.modules[source]["name"]} → {self.modules[target]["name"]}',
                    'status': '✗',
                    'description': '缺少必要的物理关系'
                })
        
        # 检查冗余关系
        redundant_relations = []
        for relation in self.module_relations:
            source, target = relation
            # 检查是否存在反向关系
            if (target, source) in self.module_relations:
                redundant_relations.append(relation)
        
        if redundant_relations:
            results.append({
                'relation': '双向关系',
                'status': '⚠',
                'description': f'发现双向关系: {redundant_relations}'
            })
        
        return results
    
    def generate_relation_report(self) -> str:
        """
        生成关系网络验证报告
        
        Returns:
            str: 验证报告内容
        """
        from datetime import datetime
        
        report = "# 统一场论模块关系网络验证报告\n\n"
        report += f"**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}\n\n"
        
        # 网络基本信息
        G = self.create_relation_graph()
        properties = self.analyze_network_properties(G)
        
        report += "## 1. 网络基本信息\n\n"
        report += f"- **模块数量**：{properties['nodes']}\n"
        report += f"- **关系数量**：{properties['edges']}\n"
        report += f"- **网络密度**：{properties['density']:.3f}\n"
        report += f"- **弱连通组件**：{len(properties['weakly_connected_components'])}\n"
        report += f"- **强连通组件**：{len(properties['strongly_connected_components'])}\n"
        report += f"- **模块性**：{properties['modularity']:.3f}\n\n"
        
        # 中心性分析
        report += "## 2. 中心性分析\n\n"
        report += "| 模块ID | 模块名称 | 度中心性 | 介数中心性 | 接近中心性 |\n"
        report += "|-------|---------|----------|------------|------------|\n"
        
        for module_id in self.modules:
            if module_id in properties['degree_centrality']:
                report += f"| {module_id} | {self.modules[module_id]['name']} | "
                report += f"{properties['degree_centrality'][module_id]:.3f} | "
                report += f"{properties['betweenness_centrality'][module_id]:.3f} | "
                report += f"{properties['closeness_centrality'][module_id]:.3f} |\n"
        
        # 模块使用分析
        usage = self.analyze_module_usage()
        report += "\n## 3. 模块使用分析\n\n"
        report += "| 模块ID | 模块名称 | 使用次数 |\n"
        report += "|-------|---------|----------|\n"
        
        for module_id, count in sorted(usage['module_counts'].items(), key=lambda x: x[1], reverse=True):
            report += f"| {module_id} | {self.modules[module_id]['name']} | {count} |\n"
        
        report += f"\n**最常用模块**：{self.modules[usage['most_used']]['name']} ({usage['most_used']})\n"
        report += f"**最少用模块**：{self.modules[usage['least_used']]['name']} ({usage['least_used']})\n"
        report += f"**平均使用次数**：{usage['average_usage']:.1f}\n\n"
        
        # 模块分布分析
        report += "### 3.1 模块在公式类型中的分布\n\n"
        for formula_type, modules in usage['formula_type_distribution'].items():
            module_names = [self.modules[module]['name'] for module in modules if module in self.modules]
            report += f"- **{formula_type}**：{', '.join(module_names)}\n"
        
        # 关系一致性验证
        consistency_results = self.validate_relation_consistency()
        report += "\n## 4. 关系一致性验证\n\n"
        report += "| 验证类型 | 状态 | 描述 |\n"
        report += "|---------|------|------|\n"
        
        for result in consistency_results:
            status = "✓" if result['status'] == '正常' else "⚠" if result['status'] == '警告' else "✗"
            report += f"| {result['type']} | {status} | {result['description']} |\n"
        
        # 物理意义验证
        physical_results = self.validate_physical_consistency()
        report += "\n## 5. 物理意义一致性验证\n\n"
        report += "| 关系 | 状态 | 描述 |\n"
        report += "|------|------|------|\n"
        
        for result in physical_results:
            report += f"| {result['relation']} | {result['status']} | {result['description']} |\n"
        
        # 模块分类分析
        report += "\n## 6. 模块分类分析\n\n"
        for category, modules in self.module_categories.items():
            module_names = [self.modules[module]['name'] for module in modules if module in self.modules]
            report += f"- **{category}**：{', '.join(module_names)}\n"
        
        # 路径分析
        report += "\n## 7. 关键路径分析\n\n"
        report += "### 7.1 核心模块链\n\n"
        core_paths = [
            ['M01', 'M06', 'M07'],  # 光速 → 动量 → 力
            ['M03', 'M05', 'M09'],  # 立体角变化率 → 径向衰减 → 电磁耦合
            ['M01', 'M10'],         # 光速 → 相对论因子
            ['M02', 'M05']          # 时空位置 → 径向衰减
        ]
        
        for path in core_paths:
            path_names = [self.modules[module]['name'] for module in path if module in self.modules]
            report += f"- {' → '.join(path_names)}\n"
        
        # 综合评价
        report += "\n## 8. 综合评价\n\n"
        
        # 计算评价指标
        network_score = 0
        if properties['density'] > 0.1:
            network_score += 20
        if len(properties['weakly_connected_components']) == 1:
            network_score += 20
        if usage['average_usage'] > 3:
            network_score += 20
        if properties['modularity'] > 0.3:
            network_score += 20
        
        # 检查关键关系
        key_relations = [('M01', 'M06'), ('M06', 'M07'), ('M03', 'M09'), ('M01', 'M10')]
        key_relation_score = sum(1 for rel in key_relations if rel in self.module_relations)
        network_score += key_relation_score * 5
        
        if network_score >= 80:
            report += "**评价结果**：优秀\n"
            report += "模块关系网络结构合理，核心关系完整，物理意义明确。\n"
        elif network_score >= 60:
            report += "**评价结果**：良好\n"
            report += "模块关系网络基本合理，但存在一些需要优化的地方。\n"
        else:
            report += "**评价结果**：需要改进\n"
            report += "模块关系网络存在明显问题，需要重新设计核心关系。\n"
        
        # 改进建议
        report += "\n## 9. 改进建议\n\n"
        
        # 基于分析结果生成建议
        suggestions = []
        
        if len(properties['weakly_connected_components']) > 1:
            suggestions.append("1. **增强网络连通性**：添加必要的模块关系，减少孤立组件")
        
        if usage['average_usage'] < 3:
            suggestions.append("2. **优化模块使用**：提高模块的复用率，减少专用模块")
        
        if properties['modularity'] < 0.3:
            suggestions.append("3. **加强模块分类**：明确模块职责，优化模块组合")
        
        if key_relation_score < len(key_relations):
            suggestions.append("4. **完善核心关系**：确保所有关键物理关系都已建立")
        
        if not suggestions:
            suggestions.append("1. **保持现有结构**：模块关系网络结构良好，建议保持")
            suggestions.append("2. **扩展关系网络**：可以考虑添加更多细化的模块关系")
            suggestions.append("3. **建立动态分析**：在模块更新时自动分析关系网络")
        
        for suggestion in suggestions:
            report += f"{suggestion}\n"
        
        return report

if __name__ == "__main__":
    # 创建验证器实例
    validator = ModuleRelationValidator()
    
    # 生成验证报告
    report = validator.generate_relation_report()
    
    # 保存报告
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = os.path.join(output_dir, "module_relation_validation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"模块关系网络验证报告已生成：{report_path}")
    
    # 打印验证摘要
    G = validator.create_relation_graph()
    properties = validator.analyze_network_properties(G)
    usage = validator.analyze_module_usage()
    
    print(f"\n验证摘要：")
    print(f"模块数量：{properties['nodes']}")
    print(f"关系数量：{properties['edges']}")
    print(f"网络密度：{properties['density']:.3f}")
    print(f"最常用模块：{validator.modules[usage['most_used']]['name']} ({usage['most_used']})")
    print(f"平均使用次数：{usage['average_usage']:.1f}")
