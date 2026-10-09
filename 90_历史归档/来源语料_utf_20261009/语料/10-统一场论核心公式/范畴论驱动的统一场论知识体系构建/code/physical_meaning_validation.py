#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论物理意义一致性验证
该脚本用于验证统一场论公式的物理意义是否合理，确保理论体系的物理概念一致
"""

import os
from typing import Dict, List, Tuple, Any

class PhysicalMeaningValidator:
    """物理意义一致性验证器"""
    
    def __init__(self):
        """初始化数据"""
        # 20个核心公式的物理意义
        self.formulas = {
            '公式1': {
                'name': '时空同一化方程',
                'formula': '\\vec{r}(t) = \\vec{c}t = x\\vec{i} + y\\vec{j} + z\\vec{k}',
                'meaning': '时空的统一描述',
                'physical_concepts': ['时空统一', '光速不变', '空间位置'],
                'expected_meaning': '描述空间和时间的统一关系，空间位移与时间的比例由光速决定'
            },
            '公式2': {
                'name': '三维螺旋时空方程',
                'formula': '\\vec{r}(t) = r\\cos\\omega t \\cdot \\vec{i} + r\\sin\\omega t \\cdot \\vec{j} + ht \\cdot \\vec{k}',
                'meaning': '物体在时空中的螺旋运动',
                'physical_concepts': ['螺旋运动', '时空几何', '运动轨迹'],
                'expected_meaning': '描述物体在时空中的螺旋运动轨迹，结合旋转和平移'
            },
            '公式3': {
                'name': '质量定义方程',
                'formula': 'm = k \\dfrac{dn}{d\\Omega}',
                'meaning': '质量的几何起源',
                'physical_concepts': ['质量几何化', '空间几何', '立体角'],
                'expected_meaning': '从空间几何角度定义质量，质量与空间几何变化率成正比'
            },
            '公式4': {
                'name': '引力场定义方程',
                'formula': '\\vec{A} = -Gk\\dfrac{\\Delta n}{\\Delta s}\\dfrac{\\vec{r}}{r}',
                'meaning': '引力场的几何起源',
                'physical_concepts': ['引力场', '空间几何', '场强分布'],
                'expected_meaning': '描述引力场的空间分布，与质量的空间变化率相关'
            },
            '公式5': {
                'name': '静止动量方程',
                'formula': '\\vec{p}_{0} = m_{0}\\vec{c}_{0}',
                'meaning': '静止质量的动量',
                'physical_concepts': ['静止动量', '质量', '光速'],
                'expected_meaning': '描述静止质量的内在动量，体现质能等价'
            },
            '公式6': {
                'name': '运动动量方程',
                'formula': '\\vec{P} = m(\\vec{c} - \\vec{v})',
                'meaning': '统一场论动量',
                'physical_concepts': ['运动动量', '质量', '光速', '速度'],
                'expected_meaning': '描述运动物体的动量，考虑物体速度对动量的影响'
            },
            '公式7': {
                'name': '宇宙大统一方程',
                'formula': '\\vec{F} = \\dfrac{d\\vec{P}}{dt} = \\vec{c}\\dfrac{dm}{dt} - \\vec{v}\\dfrac{dm}{dt} + m\\dfrac{d\\vec{c}}{dt} - m\\dfrac{d\\vec{v}}{dt}',
                'meaning': '统一力场方程',
                'physical_concepts': ['力', '动量变化', '质量变化', '速度变化'],
                'expected_meaning': '统一描述所有基本力，包括惯性力、引力、电磁力和核力'
            },
            '公式8': {
                'name': '空间波动方程',
                'formula': '\\nabla^2 L = \\dfrac{1}{c^2} \\dfrac{\\partial^2 L}{\\partial t^2}',
                'meaning': '空间波动的传播',
                'physical_concepts': ['空间波动', '波动方程', '光速'],
                'expected_meaning': '描述空间本身的波动特性，是统一场论中波粒二象性的基础'
            },
            '公式9': {
                'name': '电荷定义方程',
                'formula': 'q = k^{\\prime}k\\dfrac{1}{\\Omega^{2}}\\dfrac{d\\Omega}{dt}',
                'meaning': '电荷的几何起源',
                'physical_concepts': ['电荷几何化', '空间旋转', '立体角变化'],
                'expected_meaning': '从空间几何角度定义电荷，体现电荷与空间旋转的关系'
            },
            '公式10': {
                'name': '电场定义方程',
                'formula': '\\vec{E} = -\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0\\Omega^2}\\dfrac{d\\Omega}{dt}\\dfrac{\\vec{r}}{r^3}',
                'meaning': '电场的几何起源',
                'physical_concepts': ['电场', '电荷', '场强分布', '空间几何'],
                'expected_meaning': '描述电场的空间分布，与电荷的空间变化率相关'
            },
            '公式11': {
                'name': '磁场定义方程',
                'formula': '\\vec{B} = \\dfrac{\\mu_{0} \\gamma k k^{\\prime}}{4 \\pi \\Omega^{2}} \\dfrac{d \\Omega}{d t} \\dfrac{[(x-v t) \\vec{i}+y \\vec{j}+z \\vec{k}]}{[\\gamma^{2}(x-v t)^{2}+y^{2}+z^{2}]^{3/2}}',
                'meaning': '磁场的几何起源',
                'physical_concepts': ['磁场', '运动电荷', '相对论效应', '空间几何'],
                'expected_meaning': '描述磁场的空间分布，考虑运动电荷的相对论效应'
            },
            '公式12': {
                'name': '变化的引力场产生电磁场',
                'formula': '\\dfrac{\\partial^{2}\\vec{A}}{\\partial t^{2}} = \\dfrac{\\vec{v}}{f}\\left(\\vec{\\nabla}\\cdot\\vec{E}\\right) - \\dfrac{c^{2}}{f}\\left(\\vec{\\nabla}\\times\\vec{B}\\right)',
                'meaning': '引力场与电磁场的转换',
                'physical_concepts': ['引力场变化', '电磁场产生', '场转换'],
                'expected_meaning': '描述引力场变化如何产生电磁场，体现引力与电磁力的统一'
            },
            '公式13': {
                'name': '磁矢势方程',
                'formula': '\\vec{\\nabla} \\times \\vec{A} = \\dfrac{\\vec{B}}{f}',
                'meaning': '磁矢势与磁感应强度的关系',
                'physical_concepts': ['磁矢势', '磁感应强度', '旋度'],
                'expected_meaning': '描述磁矢势与磁感应强度的关系'
            },
            '公式14': {
                'name': '变化的引力场产生电场',
                'formula': '\\vec{E} = -f\\dfrac{d\\vec{A}}{dt}',
                'meaning': '引力场变化产生电场',
                'physical_concepts': ['引力场变化', '电场产生', '场转换'],
                'expected_meaning': '描述引力场变化如何直接产生电场，体现引力与电磁力的统一'
            },
            '公式15': {
                'name': '变化的磁场产生引力场和电场',
                'formula': '\\dfrac{d\\vec{B}}{dt} = -\\dfrac{\\vec{A}\\times\\vec{E}}{c^2} - \\dfrac{\\vec{v}}{c^{2}}\\times\\dfrac{d\\vec{E}}{dt}',
                'meaning': '磁场变化产生引力场和电场',
                'physical_concepts': ['磁场变化', '引力场产生', '电场产生', '场转换'],
                'expected_meaning': '描述磁场变化如何产生引力场和电场，体现电磁力与引力的统一'
            },
            '公式16': {
                'name': '统一场论能量方程',
                'formula': 'E = m_0 c^2 = mc^2\\sqrt{1 - \\dfrac{v^2}{c^2}}',
                'meaning': '能量与质量、速度的关系',
                'physical_concepts': ['能量', '质量', '速度', '相对论效应'],
                'expected_meaning': '描述物体的能量与质量、速度的关系，是质能等价的推广'
            },
            '公式17': {
                'name': '光速飞行器动力学方程',
                'formula': '\\vec{F} = (\\vec{c} - \\vec{v})\\dfrac{dm}{dt}',
                'meaning': '光速飞行器的动力学特性',
                'physical_concepts': ['光速飞行', '动力学', '质量变化', '推力'],
                'expected_meaning': '描述接近光速运动的飞行器的动力学特性'
            },
            '公式18': {
                'name': '核力场定义方程',
                'formula': '\\vec{D} = - G m \\dfrac{ \\vec{c} - 3 \\dfrac{\\vec{r}}{r} \\dot{r} }{r^3}',
                'meaning': '核力场的几何起源',
                'physical_concepts': ['核力场', '质量', '光速', '空间几何'],
                'expected_meaning': '描述核力场的空间分布，体现核力与引力、电磁力的统一'
            },
            '公式19': {
                'name': '引力光速统一方程',
                'formula': 'Z = \\dfrac{Gc}{2}',
                'meaning': '引力常数与光速的统一关系',
                'physical_concepts': ['引力常数', '光速', '耦合常数'],
                'expected_meaning': '描述引力常数与光速的统一关系，体现引力与时空的深层联系'
            },
            '公式20': {
                'name': '电磁光速几何耦合常数',
                'formula': 'Z^{\\prime} = \\dfrac{c}{8\\pi\\varepsilon_0}',
                'meaning': '电磁耦合与光速的关系',
                'physical_concepts': ['电磁耦合', '光速', '真空介电常数'],
                'expected_meaning': '描述电磁相互作用的耦合强度，体现电磁力与时空的深层联系'
            }
        }
        
        # 核心物理概念
        self.core_concepts = {
            '时空统一': {
                'description': '空间和时间的统一描述',
                'formulas': ['公式1', '公式2', '公式8'],
                'expected_elements': ['光速', '时空坐标', '波动方程']
            },
            '质量几何化': {
                'description': '质量由空间几何变化率决定',
                'formulas': ['公式3', '公式4', '公式18'],
                'expected_elements': ['立体角', '空间变化率', '几何因子']
            },
            '动量统一': {
                'description': '包含光速项的统一动量定义',
                'formulas': ['公式5', '公式6', '公式7', '公式17'],
                'expected_elements': ['质量', '光速', '速度', '动量变化']
            },
            '电磁统一': {
                'description': '电场和磁场的统一描述',
                'formulas': ['公式9', '公式10', '公式11', '公式12', '公式13', '公式14', '公式15'],
                'expected_elements': ['电荷', '电场', '磁场', '场转换']
            },
            '能量统一': {
                'description': '能量与质量、速度的统一关系',
                'formulas': ['公式16'],
                'expected_elements': ['质量', '光速', '速度', '相对论因子']
            },
            '力场统一': {
                'description': '所有力场的统一描述',
                'formulas': ['公式4', '公式7', '公式10', '公式11', '公式18'],
                'expected_elements': ['引力场', '电场', '磁场', '核力场']
            }
        }
    
    def validate_formula_meaning(self) -> List[Dict[str, Any]]:
        """
        验证单个公式的物理意义
        
        Returns:
            List[Dict[str, Any]]: 公式物理意义验证结果
        """
        results = []
        
        for formula_id, formula in self.formulas.items():
            # 检查物理概念是否完整
            concepts = formula['physical_concepts']
            formula_text = formula['formula']
            
            # 检查关键物理要素是否存在
            missing_elements = []
            for concept in concepts:
                if concept == '光速' and 'c' not in formula_text:
                    missing_elements.append('光速项')
                elif concept == '质量' and 'm' not in formula_text:
                    missing_elements.append('质量项')
                elif concept == '速度' and 'v' not in formula_text:
                    missing_elements.append('速度项')
                elif concept == '电荷' and ('q' not in formula_text and 'k^{\prime}' not in formula_text):
                    missing_elements.append('电荷项')
                elif concept == '电场' and 'E' not in formula_text:
                    missing_elements.append('电场项')
                elif concept == '磁场' and 'B' not in formula_text:
                    missing_elements.append('磁场项')
                elif concept == '引力场' and 'A' not in formula_text:
                    missing_elements.append('引力场项')
                elif concept == '立体角' and 'Omega' not in formula_text and '\\Omega' not in formula_text:
                    missing_elements.append('立体角项')
                elif concept == '相对论效应' and ('gamma' not in formula_text and '\\gamma' not in formula_text and 'sqrt' not in formula_text):
                    missing_elements.append('相对论因子')
            
            # 评估物理意义完整性
            if not missing_elements:
                status = "✓"
                description = "物理意义完整"
            elif len(missing_elements) < 2:
                status = "⚠"
                description = f"缺少部分物理要素: {', '.join(missing_elements)}"
            else:
                status = "✗"
                description = f"缺少关键物理要素: {', '.join(missing_elements)}"
            
            results.append({
                'formula_id': formula_id,
                'formula_name': formula['name'],
                'status': status,
                'description': description,
                'missing_elements': missing_elements
            })
        
        return results
    
    def validate_concept_consistency(self) -> List[Dict[str, Any]]:
        """
        验证核心物理概念的一致性
        
        Returns:
            List[Dict[str, Any]]: 核心物理概念一致性验证结果
        """
        results = []
        
        for concept_name, concept_info in self.core_concepts.items():
            formulas = concept_info['formulas']
            expected_elements = concept_info['expected_elements']
            
            # 检查每个公式是否包含预期的物理要素
            inconsistent_formulas = []
            
            for formula_id in formulas:
                if formula_id in self.formulas:
                    formula_text = self.formulas[formula_id]['formula']
                    missing_elements = []
                    
                    for element in expected_elements:
                        if element == '光速' and 'c' not in formula_text:
                            missing_elements.append('光速项')
                        elif element == '质量' and 'm' not in formula_text:
                            missing_elements.append('质量项')
                        elif element == '速度' and 'v' not in formula_text:
                            missing_elements.append('速度项')
                        elif element == '电荷' and ('q' not in formula_text and 'k^{\prime}' not in formula_text):
                            missing_elements.append('电荷项')
                        elif element == '电场' and 'E' not in formula_text:
                            missing_elements.append('电场项')
                        elif element == '磁场' and 'B' not in formula_text:
                            missing_elements.append('磁场项')
                        elif element == '引力场' and 'A' not in formula_text:
                            missing_elements.append('引力场项')
                        elif element == '立体角' and 'Omega' not in formula_text and '\\Omega' not in formula_text:
                            missing_elements.append('立体角项')
                        elif element == '相对论因子' and ('gamma' not in formula_text and '\\gamma' not in formula_text and 'sqrt' not in formula_text):
                            missing_elements.append('相对论因子')
                        elif element == '时空坐标' and ('r' not in formula_text and '\\vec{r}' not in formula_text):
                            missing_elements.append('时空坐标项')
                        elif element == '波动方程' and ('nabla' not in formula_text and '\\nabla' not in formula_text and 'partial' not in formula_text):
                            missing_elements.append('波动方程项')
                        elif element == '几何因子' and ('dn' not in formula_text and 'd\\Omega' not in formula_text):
                            missing_elements.append('几何因子项')
                        elif element == '动量变化' and ('dP' not in formula_text and '\\dfrac{d\\vec{P}}{dt}' not in formula_text):
                            missing_elements.append('动量变化项')
                        elif element == '场转换' and ('dA' not in formula_text and 'd\\vec{A}' not in formula_text and 'dB' not in formula_text and 'd\\vec{B}' not in formula_text):
                            missing_elements.append('场转换项')
                        elif element == '真空介电常数' and 'varepsilon' not in formula_text and '\\varepsilon' not in formula_text:
                            missing_elements.append('真空介电常数项')
                    
                    if missing_elements:
                        inconsistent_formulas.append({
                            'formula_id': formula_id,
                            'formula_name': self.formulas[formula_id]['name'],
                            'missing_elements': missing_elements
                        })
            
            # 评估概念一致性
            if not inconsistent_formulas:
                status = "✓"
                description = "概念一致性良好"
            elif len(inconsistent_formulas) < len(formulas) / 2:
                status = "⚠"
                description = f"部分公式存在概念不一致: {len(inconsistent_formulas)}/{len(formulas)}"
            else:
                status = "✗"
                description = f"多数公式存在概念不一致: {len(inconsistent_formulas)}/{len(formulas)}"
            
            results.append({
                'concept': concept_name,
                'status': status,
                'description': description,
                'inconsistent_formulas': inconsistent_formulas
            })
        
        return results
    
    def analyze_physical_connections(self) -> Dict[str, Any]:
        """
        分析物理概念之间的联系
        
        Returns:
            Dict[str, Any]: 物理概念联系分析结果
        """
        connections = {}
        
        # 分析概念之间的重叠公式
        concept_overlaps = {}
        for concept1, info1 in self.core_concepts.items():
            concept_overlaps[concept1] = {}
            for concept2, info2 in self.core_concepts.items():
                if concept1 != concept2:
                    overlap_formulas = set(info1['formulas']) & set(info2['formulas'])
                    if overlap_formulas:
                        concept_overlaps[concept1][concept2] = list(overlap_formulas)
        
        connections['concept_overlaps'] = concept_overlaps
        
        # 分析公式涉及的概念数量
        formula_concept_count = {}
        for formula_id, formula in self.formulas.items():
            formula_concept_count[formula_id] = len(formula['physical_concepts'])
        
        connections['formula_concept_count'] = formula_concept_count
        connections['most_conceptual'] = max(formula_concept_count, key=formula_concept_count.get)
        connections['least_conceptual'] = min(formula_concept_count, key=formula_concept_count.get)
        
        # 分析核心概念的重要性
        concept_importance = {}
        for concept, info in self.core_concepts.items():
            importance = len(info['formulas'])
            concept_importance[concept] = importance
        
        connections['concept_importance'] = concept_importance
        connections['most_important_concept'] = max(concept_importance, key=concept_importance.get)
        
        return connections
    
    def validate_unification_principle(self) -> List[Dict[str, Any]]:
        """
        验证统一原理的体现
        
        Returns:
            List[Dict[str, Any]]: 统一原理验证结果
        """
        results = []
        
        # 检查光速在各公式中的一致性
        c_formulas = [fid for fid, f in self.formulas.items() if 'c' in f['formula']]
        results.append({
            'principle': '光速统一性',
            'status': "✓" if len(c_formulas) >= 10 else "⚠",
            'description': f'光速项出现在 {len(c_formulas)}/20 个公式中',
            'formulas': c_formulas
        })
        
        # 检查几何化原理的体现
        geometry_formulas = [fid for fid, f in self.formulas.items() if 'Omega' in f['formula'] or '\\Omega' in f['formula'] or 'dn' in f['formula']]
        results.append({
            'principle': '几何化原理',
            'status': "✓" if len(geometry_formulas) >= 5 else "⚠",
            'description': f'几何化项出现在 {len(geometry_formulas)}/20 个公式中',
            'formulas': geometry_formulas
        })
        
        # 检查场转换原理的体现
        field_conversion_formulas = ['公式12', '公式14', '公式15']
        valid_conversion = all(fid in self.formulas for fid in field_conversion_formulas)
        results.append({
            'principle': '场转换原理',
            'status': "✓" if valid_conversion else "✗",
            'description': '场转换公式是否完整',
            'formulas': field_conversion_formulas
        })
        
        # 检查相对论效应的体现
        relativity_formulas = [fid for fid, f in self.formulas.items() if 'gamma' in f['formula'] or '\\gamma' in f['formula'] or 'sqrt' in f['formula']]
        results.append({
            'principle': '相对论效应',
            'status': "✓" if len(relativity_formulas) >= 3 else "⚠",
            'description': f'相对论效应出现在 {len(relativity_formulas)}/20 个公式中',
            'formulas': relativity_formulas
        })
        
        return results
    
    def generate_meaning_report(self) -> str:
        """
        生成物理意义一致性验证报告
        
        Returns:
            str: 验证报告内容
        """
        from datetime import datetime
        
        report = "# 统一场论物理意义一致性验证报告\n\n"
        report += f"**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}\n\n"
        
        # 公式物理意义验证
        formula_results = self.validate_formula_meaning()
        report += "## 1. 公式物理意义验证\n\n"
        report += "| 公式ID | 公式名称 | 状态 | 描述 |\n"
        report += "|-------|---------|------|------|\n"
        
        valid_formulas = 0
        for result in formula_results:
            valid_formulas += 1 if result['status'] == "✓" else 0
            report += f"| {result['formula_id']} | {result['formula_name']} | {result['status']} | {result['description']} |\n"
        
        report += f"\n**物理意义完整的公式**：{valid_formulas}/{len(formula_results)}\n\n"
        
        # 核心概念一致性验证
        concept_results = self.validate_concept_consistency()
        report += "## 2. 核心概念一致性验证\n\n"
        report += "| 物理概念 | 状态 | 描述 |\n"
        report += "|----------|------|------|\n"
        
        valid_concepts = 0
        for result in concept_results:
            valid_concepts += 1 if result['status'] == "✓" else 0
            report += f"| {result['concept']} | {result['status']} | {result['description']} |\n"
        
        report += f"\n**概念一致性良好的核心概念**：{valid_concepts}/{len(concept_results)}\n\n"
        
        # 物理概念联系分析
        connection_analysis = self.analyze_physical_connections()
        report += "## 3. 物理概念联系分析\n\n"
        
        # 概念重叠分析
        report += "### 3.1 概念重叠分析\n\n"
        for concept1, overlaps in connection_analysis['concept_overlaps'].items():
            if overlaps:
                report += f"- **{concept1}** 与其他概念的重叠：\n"
                for concept2, formulas in overlaps.items():
                    formula_names = [self.formulas[f]['name'] for f in formulas]
                    report += f"  - {concept2}：{', '.join(formula_names)}\n"
        
        # 公式概念丰富度
        report += "\n### 3.2 公式概念丰富度\n\n"
        report += "| 公式ID | 公式名称 | 涉及概念数 |\n"
        report += "|-------|---------|------------|\n"
        
        for formula_id, count in sorted(connection_analysis['formula_concept_count'].items(), key=lambda x: x[1], reverse=True):
            report += f"| {formula_id} | {self.formulas[formula_id]['name']} | {count} |\n"
        
        most_conceptual = connection_analysis['most_conceptual']
        least_conceptual = connection_analysis['least_conceptual']
        report += f"\n**概念最丰富的公式**：{self.formulas[most_conceptual]['name']} ({most_conceptual})\n"
        report += f"**概念最简单的公式**：{self.formulas[least_conceptual]['name']} ({least_conceptual})\n\n"
        
        # 统一原理验证
        unification_results = self.validate_unification_principle()
        report += "## 4. 统一原理验证\n\n"
        report += "| 统一原理 | 状态 | 描述 |\n"
        report += "|----------|------|------|\n"
        
        for result in unification_results:
            report += f"| {result['principle']} | {result['status']} | {result['description']} |\n"
        
        # 综合评价
        report += "\n## 5. 综合评价\n\n"
        
        # 计算评价分数
        total_score = 0
        total_score += valid_formulas * 2
        total_score += valid_concepts * 5
        
        # 统一原理分数
        unification_score = sum(1 for r in unification_results if r['status'] == "✓")
        total_score += unification_score * 10
        
        if total_score >= 100:
            report += "**评价结果**：优秀\n"
            report += "物理意义一致性验证结果良好，核心概念清晰，统一原理体现充分。\n"
        elif total_score >= 70:
            report += "**评价结果**：良好\n"
            report += "物理意义一致性基本正确，但存在一些需要优化的地方。\n"
        else:
            report += "**评价结果**：需要改进\n"
            report += "物理意义一致性存在问题，需要重新梳理物理概念。\n"
        
        # 改进建议
        report += "\n## 6. 改进建议\n\n"
        
        suggestions = []
        
        # 基于验证结果生成建议
        if valid_formulas < len(formula_results) * 0.8:
            suggestions.append("1. **强化物理要素**：确保每个公式包含其描述物理现象所需的关键要素")
        
        if valid_concepts < len(concept_results) * 0.8:
            suggestions.append("2. **统一概念表达**：确保核心物理概念在相关公式中保持一致的表达")
        
        if unification_score < len(unification_results) * 0.8:
            suggestions.append("3. **加强统一原理**：在更多公式中体现统一场论的核心原理")
        
        if not suggestions:
            suggestions.append("1. **保持现有结构**：物理意义一致性良好，建议保持")
            suggestions.append("2. **扩展物理验证**：可以考虑验证更多物理场景下的概念一致性")
            suggestions.append("3. **建立概念图谱**：构建物理概念之间的关联图谱，加深理解")
        
        for suggestion in suggestions:
            report += f"{suggestion}\n"
        
        return report

if __name__ == "__main__":
    # 创建验证器实例
    validator = PhysicalMeaningValidator()
    
    # 生成验证报告
    report = validator.generate_meaning_report()
    
    # 保存报告
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = os.path.join(output_dir, "physical_meaning_validation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"物理意义一致性验证报告已生成：{report_path}")
    
    # 打印验证摘要
    formula_results = validator.validate_formula_meaning()
    concept_results = validator.validate_concept_consistency()
    unification_results = validator.validate_unification_principle()
    
    valid_formulas = sum(1 for r in formula_results if r['status'] == "✓")
    valid_concepts = sum(1 for r in concept_results if r['status'] == "✓")
    valid_unification = sum(1 for r in unification_results if r['status'] == "✓")
    
    print(f"\n验证摘要：")
    print(f"公式物理意义：{valid_formulas}/{len(formula_results)} 完整")
    print(f"核心概念一致性：{valid_concepts}/{len(concept_results)} 良好")
    print(f"统一原理体现：{valid_unification}/{len(unification_results)} 优秀")
