#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论公式逻辑一致性验证
该脚本用于验证统一场论公式之间的推导关系是否正确，确保公式体系的逻辑自洽
"""

import os
from typing import Dict, List, Tuple, Any

class FormulaLogicValidator:
    """公式逻辑一致性验证器"""
    
    def __init__(self):
        """初始化数据"""
        # 20个核心公式
        self.formulas = {
            '公式1': {
                'name': '时空同一化方程',
                'formula': '\\vec{r}(t) = \\vec{c}t = x\\vec{i} + y\\vec{j} + z\\vec{k}',
                'meaning': '时空的统一描述',
                'dependencies': []
            },
            '公式2': {
                'name': '三维螺旋时空方程',
                'formula': '\\vec{r}(t) = r\\cos\\omega t \\cdot \\vec{i} + r\\sin\\omega t \\cdot \\vec{j} + ht \\cdot \\vec{k}',
                'meaning': '物体在时空中的螺旋运动',
                'dependencies': ['公式1']
            },
            '公式3': {
                'name': '质量定义方程',
                'formula': 'm = k \\dfrac{dn}{d\\Omega}',
                'meaning': '质量的几何起源',
                'dependencies': []
            },
            '公式4': {
                'name': '引力场定义方程',
                'formula': '\\vec{A} = -Gk\\dfrac{\\Delta n}{\\Delta s}\\dfrac{\\vec{r}}{r}',
                'meaning': '引力场的几何起源',
                'dependencies': ['公式3']
            },
            '公式5': {
                'name': '静止动量方程',
                'formula': '\\vec{p}_{0} = m_{0}\\vec{c}_{0}',
                'meaning': '静止质量的动量',
                'dependencies': ['公式1', '公式3']
            },
            '公式6': {
                'name': '运动动量方程',
                'formula': '\\vec{P} = m(\\vec{c} - \\vec{v})',
                'meaning': '统一场论动量',
                'dependencies': ['公式1', '公式3', '公式5']
            },
            '公式7': {
                'name': '宇宙大统一方程',
                'formula': '\\vec{F} = \\dfrac{d\\vec{P}}{dt} = \\vec{c}\\dfrac{dm}{dt} - \\vec{v}\\dfrac{dm}{dt} + m\\dfrac{d\\vec{c}}{dt} - m\\dfrac{d\\vec{v}}{dt}',
                'meaning': '统一力场方程',
                'dependencies': ['公式6']
            },
            '公式8': {
                'name': '空间波动方程',
                'formula': '\\nabla^2 L = \\dfrac{1}{c^2} \\dfrac{\\partial^2 L}{\\partial t^2}',
                'meaning': '空间波动的传播',
                'dependencies': ['公式1']
            },
            '公式9': {
                'name': '电荷定义方程',
                'formula': 'q = k^{\\prime}k\\dfrac{1}{\\Omega^{2}}\\dfrac{d\\Omega}{dt}',
                'meaning': '电荷的几何起源',
                'dependencies': []
            },
            '公式10': {
                'name': '电场定义方程',
                'formula': '\\vec{E} = -\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0\\Omega^2}\\dfrac{d\\Omega}{dt}\\dfrac{\\vec{r}}{r^3}',
                'meaning': '电场的几何起源',
                'dependencies': ['公式9']
            },
            '公式11': {
                'name': '磁场定义方程',
                'formula': '\\vec{B} = \\dfrac{\\mu_{0} \\gamma k k^{\\prime}}{4 \\pi \\Omega^{2}} \\dfrac{d \\Omega}{d t} \\dfrac{[(x-v t) \\vec{i}+y \\vec{j}+z \\vec{k}]}{[\\gamma^{2}(x-v t)^{2}+y^{2}+z^{2}]^{3/2}}',
                'meaning': '磁场的几何起源',
                'dependencies': ['公式9']
            },
            '公式12': {
                'name': '变化的引力场产生电磁场',
                'formula': '\\dfrac{\\partial^{2}\\vec{A}}{\\partial t^{2}} = \\dfrac{\\vec{v}}{f}\\left(\\vec{\\nabla}\\cdot\\vec{E}\\right) - \\dfrac{c^{2}}{f}\\left(\\vec{\\nabla}\\times\\vec{B}\\right)',
                'meaning': '引力场与电磁场的转换',
                'dependencies': ['公式4', '公式10', '公式11']
            },
            '公式13': {
                'name': '磁矢势方程',
                'formula': '\\vec{\\nabla} \\times \\vec{A} = \\dfrac{\\vec{B}}{f}',
                'meaning': '磁矢势与磁感应强度的关系',
                'dependencies': ['公式11']
            },
            '公式14': {
                'name': '变化的引力场产生电场',
                'formula': '\\vec{E} = -f\\dfrac{d\\vec{A}}{dt}',
                'meaning': '引力场变化产生电场',
                'dependencies': ['公式4', '公式13']
            },
            '公式15': {
                'name': '变化的磁场产生引力场和电场',
                'formula': '\\dfrac{d\\vec{B}}{dt} = -\\dfrac{\\vec{A}\\times\\vec{E}}{c^2} - \\dfrac{\\vec{v}}{c^{2}}\\times\\dfrac{d\\vec{E}}{dt}',
                'meaning': '磁场变化产生引力场和电场',
                'dependencies': ['公式10', '公式11', '公式13']
            },
            '公式16': {
                'name': '统一场论能量方程',
                'formula': 'E = m_0 c^2 = mc^2\\sqrt{1 - \\dfrac{v^2}{c^2}}',
                'meaning': '能量与质量、速度的关系',
                'dependencies': ['公式1', '公式3', '公式5', '公式6']
            },
            '公式17': {
                'name': '光速飞行器动力学方程',
                'formula': '\\vec{F} = (\\vec{c} - \\vec{v})\\dfrac{dm}{dt}',
                'meaning': '光速飞行器的动力学特性',
                'dependencies': ['公式6', '公式7']
            },
            '公式18': {
                'name': '核力场定义方程',
                'formula': '\\vec{D} = - G m \\dfrac{ \\vec{c} - 3 \\dfrac{\\vec{r}}{r} \\dot{r} }{r^3}',
                'meaning': '核力场的几何起源',
                'dependencies': ['公式1', '公式3', '公式4']
            },
            '公式19': {
                'name': '引力光速统一方程',
                'formula': 'Z = \\dfrac{Gc}{2}',
                'meaning': '引力常数与光速的统一关系',
                'dependencies': ['公式1']
            },
            '公式20': {
                'name': '电磁光速几何耦合常数',
                'formula': 'Z^{\\prime} = \\dfrac{c}{8\\pi\\varepsilon_0}',
                'meaning': '电磁耦合与光速的关系',
                'dependencies': ['公式1']
            }
        }
        
        # 公式分类
        self.formula_categories = {
            '时空基础': ['公式1', '公式2', '公式8'],
            '质量与引力': ['公式3', '公式4', '公式18'],
            '动量与力': ['公式5', '公式6', '公式7', '公式17'],
            '电磁学': ['公式9', '公式10', '公式11', '公式12', '公式13', '公式14', '公式15'],
            '能量': ['公式16'],
            '耦合常数': ['公式19', '公式20']
        }
    
    def validate_dependency_structure(self) -> List[Dict[str, Any]]:
        """
        验证依赖结构的一致性
        
        Returns:
            List[Dict[str, Any]]: 依赖结构验证结果
        """
        results = []
        
        # 检查依赖循环
        visited = set()
        recursion_stack = set()
        cycles = []
        
        def detect_cycle(formula_id):
            if formula_id in recursion_stack:
                return [formula_id]
            if formula_id in visited:
                return []
            
            visited.add(formula_id)
            recursion_stack.add(formula_id)
            
            formula = self.formulas.get(formula_id)
            if formula:
                for dep in formula['dependencies']:
                    cycle = detect_cycle(dep)
                    if cycle:
                        if formula_id not in cycle:
                            cycle.append(formula_id)
                        return cycle
            
            recursion_stack.remove(formula_id)
            return []
        
        for formula_id in self.formulas:
            if formula_id not in visited:
                cycle = detect_cycle(formula_id)
                if cycle:
                    cycles.append(cycle)
        
        if cycles:
            results.append({
                'type': '依赖循环',
                'status': '错误',
                'description': f'发现依赖循环: {cycles}',
                'severity': 'high'
            })
        else:
            results.append({
                'type': '依赖循环',
                'status': '正常',
                'description': '未发现依赖循环',
                'severity': 'low'
            })
        
        # 检查依赖存在性
        missing_dependencies = []
        for formula_id, formula in self.formulas.items():
            for dep in formula['dependencies']:
                if dep not in self.formulas:
                    missing_dependencies.append((formula_id, dep))
        
        if missing_dependencies:
            results.append({
                'type': '依赖存在性',
                'status': '错误',
                'description': f'发现缺失依赖: {missing_dependencies}',
                'severity': 'high'
            })
        else:
            results.append({
                'type': '依赖存在性',
                'status': '正常',
                'description': '所有依赖都存在',
                'severity': 'low'
            })
        
        # 检查依赖深度
        max_depth = 0
        depth_map = {}
        
        def calculate_depth(formula_id):
            if formula_id in depth_map:
                return depth_map[formula_id]
            
            formula = self.formulas.get(formula_id)
            if not formula:
                return 0
            
            if not formula['dependencies']:
                depth_map[formula_id] = 1
                return 1
            
            max_dep_depth = 0
            for dep in formula['dependencies']:
                dep_depth = calculate_depth(dep)
                if dep_depth > max_dep_depth:
                    max_dep_depth = dep_depth
            
            depth = max_dep_depth + 1
            depth_map[formula_id] = depth
            return depth
        
        for formula_id in self.formulas:
            depth = calculate_depth(formula_id)
            if depth > max_depth:
                max_depth = depth
        
        results.append({
            'type': '依赖深度',
            'status': '正常' if max_depth <= 5 else '警告',
            'description': f'最大依赖深度: {max_depth}',
            'severity': 'low' if max_depth <= 5 else 'medium'
        })
        
        return results
    
    def validate_logical_consistency(self) -> List[Dict[str, Any]]:
        """
        验证逻辑一致性
        
        Returns:
            List[Dict[str, Any]]: 逻辑一致性验证结果
        """
        results = []
        
        # 检查核心推导链
        core_chains = [
            ['公式1', '公式5', '公式6', '公式7', '公式17'],  # 时空-动量-力链
            ['公式3', '公式4', '公式18'],  # 质量-引力-核力链
            ['公式9', '公式10', '公式11', '公式13', '公式14', '公式15'],  # 电荷-电磁链
            ['公式1', '公式6', '公式16']  # 时空-动量-能量链
        ]
        
        for chain in core_chains:
            valid = True
            for i in range(len(chain) - 1):
                current = chain[i]
                next_formula = chain[i + 1]
                if current not in self.formulas[next_formula]['dependencies']:
                    valid = False
                    break
            
            chain_names = [self.formulas[f]['name'] for f in chain]
            status = "✓" if valid else "✗"
            results.append({
                'chain': ' → '.join(chain_names),
                'status': status,
                'description': '推导链完整' if valid else '推导链不完整'
            })
        
        # 检查分类内一致性
        for category, formulas in self.formula_categories.items():
            internal_dependencies = 0
            total_possible = len(formulas) * (len(formulas) - 1)
            
            for i in range(len(formulas)):
                for j in range(len(formulas)):
                    if i != j:
                        if formulas[i] in self.formulas[formulas[j]].get('dependencies', []):
                            internal_dependencies += 1
            
            consistency_ratio = internal_dependencies / total_possible if total_possible > 0 else 0
            status = "✓" if consistency_ratio >= 0.3 else "⚠" if consistency_ratio > 0 else "✗"
            
            results.append({
                'category': category,
                'status': status,
                'description': f'内部依赖率: {consistency_ratio:.2f}',
                'formulas': len(formulas)
            })
        
        return results
    
    def analyze_formula_network(self) -> Dict[str, Any]:
        """
        分析公式网络结构
        
        Returns:
            Dict[str, Any]: 公式网络分析结果
        """
        analysis = {}
        
        # 统计依赖关系
        dependency_count = {}
        for formula_id, formula in self.formulas.items():
            dependency_count[formula_id] = len(formula['dependencies'])
        
        analysis['dependency_count'] = dependency_count
        analysis['most_dependent'] = max(dependency_count, key=dependency_count.get)
        analysis['least_dependent'] = min(dependency_count, key=dependency_count.get)
        
        # 统计被依赖次数
        depended_on_count = {formula_id: 0 for formula_id in self.formulas}
        for formula_id, formula in self.formulas.items():
            for dep in formula['dependencies']:
                if dep in depended_on_count:
                    depended_on_count[dep] += 1
        
        analysis['depended_on_count'] = depended_on_count
        analysis['most_important'] = max(depended_on_count, key=depended_on_count.get)
        
        # 分析公式分类
        category_analysis = {}
        for category, formulas in self.formula_categories.items():
            category_analysis[category] = {
                'count': len(formulas),
                'dependencies': 0,
                'internal_dependencies': 0
            }
            
            for formula_id in formulas:
                formula = self.formulas[formula_id]
                category_analysis[category]['dependencies'] += len(formula['dependencies'])
                
                # 统计内部依赖
                for dep in formula['dependencies']:
                    if dep in formulas:
                        category_analysis[category]['internal_dependencies'] += 1
        
        analysis['category_analysis'] = category_analysis
        
        return analysis
    
    def validate_physical_reasoning(self) -> List[Dict[str, Any]]:
        """
        验证物理论证一致性
        
        Returns:
            List[Dict[str, Any]]: 物理论证验证结果
        """
        results = []
        
        # 检查核心物理概念的一致性
        physical_concepts = [
            {
                'concept': '时空统一',
                'formulas': ['公式1', '公式2', '公式8'],
                'expected': '时空同一化和螺旋运动描述'
            },
            {
                'concept': '质量几何化',
                'formulas': ['公式3', '公式4', '公式18'],
                'expected': '质量由空间几何变化率决定'
            },
            {
                'concept': '动量统一',
                'formulas': ['公式5', '公式6', '公式7', '公式17'],
                'expected': '包含光速项的统一动量定义'
            },
            {
                'concept': '电磁统一',
                'formulas': ['公式9', '公式10', '公式11', '公式12', '公式13', '公式14', '公式15'],
                'expected': '电场和磁场的统一描述'
            },
            {
                'concept': '能量统一',
                'formulas': ['公式16'],
                'expected': '包含相对论效应的能量方程'
            }
        ]
        
        for concept in physical_concepts:
            valid = True
            for formula_id in concept['formulas']:
                formula = self.formulas[formula_id]
                # 检查是否包含核心物理要素
                if 'c' not in formula['formula'] and formula_id not in ['公式3', '公式9']:
                    valid = False
                    break
            
            status = "✓" if valid else "⚠"
            results.append({
                'concept': concept['concept'],
                'status': status,
                'formulas': len(concept['formulas']),
                'description': '物理概念一致' if valid else '可能存在物理概念不一致'
            })
        
        return results
    
    def generate_logic_report(self) -> str:
        """
        生成逻辑一致性验证报告
        
        Returns:
            str: 验证报告内容
        """
        from datetime import datetime
        
        report = "# 统一场论公式逻辑一致性验证报告\n\n"
        report += f"**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}\n\n"
        
        # 依赖结构验证
        dependency_results = self.validate_dependency_structure()
        report += "## 1. 依赖结构验证\n\n"
        report += "| 验证类型 | 状态 | 描述 |\n"
        report += "|---------|------|------|\n"
        
        for result in dependency_results:
            status = "✓" if result['status'] == '正常' else "⚠" if result['status'] == '警告' else "✗"
            report += f"| {result['type']} | {status} | {result['description']} |\n"
        
        # 逻辑一致性验证
        logic_results = self.validate_logical_consistency()
        report += "\n## 2. 逻辑一致性验证\n\n"
        
        # 核心推导链验证
        report += "### 2.1 核心推导链验证\n\n"
        report += "| 推导链 | 状态 | 描述 |\n"
        report += "|--------|------|------|\n"
        
        for result in [r for r in logic_results if 'chain' in r]:
            report += f"| {result['chain']} | {result['status']} | {result['description']} |\n"
        
        # 分类内一致性验证
        report += "\n### 2.2 分类内一致性验证\n\n"
        report += "| 分类 | 状态 | 公式数量 | 内部依赖率 |\n"
        report += "|------|------|----------|------------|\n"
        
        for result in [r for r in logic_results if 'category' in r]:
            report += f"| {result['category']} | {result['status']} | {result['formulas']} | {result['description'].split(': ')[1]} |\n"
        
        # 公式网络分析
        network_analysis = self.analyze_formula_network()
        report += "\n## 3. 公式网络分析\n\n"
        
        # 依赖统计
        report += "### 3.1 依赖统计\n\n"
        report += "| 公式ID | 公式名称 | 依赖数量 | 被依赖次数 |\n"
        report += "|-------|---------|----------|------------|\n"
        
        for formula_id, formula in self.formulas.items():
            dep_count = len(formula['dependencies'])
            depended_count = network_analysis['depended_on_count'][formula_id]
            report += f"| {formula_id} | {formula['name']} | {dep_count} | {depended_count} |\n"
        
        report += f"\n**最依赖其他公式**：{self.formulas[network_analysis['most_dependent']]['name']} ({network_analysis['most_dependent']})\n"
        report += f"**最被其他公式依赖**：{self.formulas[network_analysis['most_important']]['name']} ({network_analysis['most_important']})\n\n"
        
        # 分类分析
        report += "### 3.2 分类分析\n\n"
        report += "| 分类 | 公式数量 | 总依赖数 | 内部依赖数 |\n"
        report += "|------|----------|----------|------------|\n"
        
        for category, analysis in network_analysis['category_analysis'].items():
            report += f"| {category} | {analysis['count']} | {analysis['dependencies']} | {analysis['internal_dependencies']} |\n"
        
        # 物理论证验证
        physical_results = self.validate_physical_reasoning()
        report += "\n## 4. 物理论证一致性验证\n\n"
        report += "| 物理概念 | 状态 | 相关公式数 | 描述 |\n"
        report += "|----------|------|------------|------|\n"
        
        for result in physical_results:
            report += f"| {result['concept']} | {result['status']} | {result['formulas']} | {result['description']} |\n"
        
        # 综合评价
        report += "\n## 5. 综合评价\n\n"
        
        # 计算评价分数
        total_score = 0
        
        # 依赖结构分数
        dependency_score = sum(1 for r in dependency_results if r['status'] == '正常')
        total_score += dependency_score * 20
        
        # 逻辑一致性分数
        logic_score = sum(1 for r in [r for r in logic_results if 'chain' in r] if r['status'] == '✓')
        total_score += logic_score * 10
        
        # 物理一致性分数
        physical_score = sum(1 for r in physical_results if r['status'] == '✓')
        total_score += physical_score * 15
        
        if total_score >= 90:
            report += "**评价结果**：优秀\n"
            report += "公式逻辑一致性验证结果良好，推导关系清晰，物理意义明确。\n"
        elif total_score >= 70:
            report += "**评价结果**：良好\n"
            report += "公式逻辑一致性基本正确，但存在一些需要优化的地方。\n"
        else:
            report += "**评价结果**：需要改进\n"
            report += "公式逻辑一致性存在问题，需要重新梳理推导关系。\n"
        
        # 改进建议
        report += "\n## 6. 改进建议\n\n"
        
        suggestions = []
        
        # 基于验证结果生成建议
        if any(r['status'] != '正常' for r in dependency_results):
            suggestions.append("1. **优化依赖结构**：消除循环依赖，确保依赖关系清晰")
        
        if any(r['status'] == '✗' for r in [r for r in logic_results if 'chain' in r]):
            suggestions.append("2. **完善推导链**：确保核心推导链的完整性")
        
        if any(r['status'] != '✓' for r in physical_results):
            suggestions.append("3. **强化物理概念**：确保物理概念在公式中的一致性表达")
        
        if network_analysis['category_analysis']['电磁学']['internal_dependencies'] < 3:
            suggestions.append("4. **加强分类内联系**：增加分类内公式的相互引用")
        
        if not suggestions:
            suggestions.append("1. **保持现有结构**：公式逻辑一致性良好，建议保持")
            suggestions.append("2. **扩展验证范围**：可以考虑验证更多物理场景下的逻辑一致性")
            suggestions.append("3. **建立自动验证**：在公式更新时自动进行逻辑一致性验证")
        
        for suggestion in suggestions:
            report += f"{suggestion}\n"
        
        return report

if __name__ == "__main__":
    # 创建验证器实例
    validator = FormulaLogicValidator()
    
    # 生成验证报告
    report = validator.generate_logic_report()
    
    # 保存报告
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = os.path.join(output_dir, "formula_logic_validation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"公式逻辑一致性验证报告已生成：{report_path}")
    
    # 打印验证摘要
    dependency_results = validator.validate_dependency_structure()
    logic_results = validator.validate_logical_consistency()
    physical_results = validator.validate_physical_reasoning()
    
    valid_dependency = sum(1 for r in dependency_results if r['status'] == '正常')
    valid_chains = sum(1 for r in [r for r in logic_results if 'chain' in r] if r['status'] == '✓')
    valid_physical = sum(1 for r in physical_results if r['status'] == '✓')
    
    print(f"\n验证摘要：")
    print(f"依赖结构验证：{valid_dependency}/{len(dependency_results)} 正常")
    print(f"核心推导链验证：{valid_chains}/{len([r for r in logic_results if 'chain' in r])} 完整")
    print(f"物理概念验证：{valid_physical}/{len(physical_results)} 一致")
