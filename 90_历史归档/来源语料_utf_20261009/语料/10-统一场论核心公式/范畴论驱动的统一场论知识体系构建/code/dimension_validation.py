#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论量纲一致性验证
该脚本用于验证张祥前统一场论20个核心公式和模块的量纲一致性
"""

import os
import json
from typing import Dict, List, Tuple, Any

class DimensionValidator:
    """量纲验证器"""
    
    def __init__(self):
        """初始化数据"""
        # 通用积木模块库，包含量纲信息
        self.modules = {
            'M01': {'name': '光速矢量', 'formula': '\\vec{c}', 'meaning': '时空统一常数', 'dimension': '[L][T]^{-1}'},
            'M02': {'name': '时空位置矢量', 'formula': '\\vec{r} = x\\vec{i} + y\\vec{j} + z\\vec{k}', 'meaning': '空间位置表示', 'dimension': '[L]'},
            'M03': {'name': '立体角变化率', 'formula': '\\dfrac{d\\Omega}{dt}', 'meaning': '空间几何旋转速率', 'dimension': '[T]^{-1}'},
            'M04': {'name': '质量变化率', 'formula': '\\dfrac{dm}{dt}', 'meaning': '质量随时间变化', 'dimension': '[M][T]^{-1}'},
            'M05': {'name': '径向衰减因子', 'formula': '\\dfrac{1}{r^3} 或 \\dfrac{\\vec{r}}{r^3}', 'meaning': '场强空间分布', 'dimension': '[L]^{-3}'},
            'M06': {'name': '动量核心结构', 'formula': 'm(\\vec{c} - \\vec{v})', 'meaning': '统一场论动量定义', 'dimension': '[M][L][T]^{-1}'},
            'M07': {'name': '力的微分形式', 'formula': '\\dfrac{d\\vec{P}}{dt}', 'meaning': '力的基本定义', 'dimension': '[M][L][T]^{-2}'},
            'M08': {'name': '引力耦合项', 'formula': 'Gk', 'meaning': '引力相互作用强度', 'dimension': '[L]^3[T]^{-2}[M]^{-1}'},
            'M09': {'name': '电磁耦合项', 'formula': '\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0}', 'meaning': '电磁相互作用强度', 'dimension': '[L]^3[T]^{-2}[M]'},
            'M10': {'name': '相对论因子', 'formula': '\\sqrt{1 - \\dfrac{v^2}{c^2}} 或 \\gamma', 'meaning': '高速运动修正', 'dimension': '1'},
            'M11': {'name': '质量定义', 'formula': 'm = k \\dfrac{dn}{d\\Omega}', 'meaning': '质量的几何定义', 'dimension': '[M]'},
            'M12': {'name': '磁矢势旋度', 'formula': '\\vec{\\nabla} \\times \\vec{A}', 'meaning': '磁矢势的旋度', 'dimension': '[M][T]^{-2}[I]^{-1}'},
            'M13': {'name': '矢量时间导数', 'formula': '\\dfrac{d\\vec{A}}{dt}', 'meaning': '矢量随时间的变化率', 'dimension': '[L][T]^{-2}'},
            'M14': {'name': '统一场论常数', 'formula': 'f', 'meaning': '统一场论中的重要常数', 'dimension': '[L][T]^{-1}'}
        }
        
        # 公式量纲信息
        self.formula_dimensions = {
            '公式1': {'name': '时空同一化方程', 'dimension': '[L]'},
            '公式2': {'name': '三维螺旋时空方程', 'dimension': '[L]'},
            '公式3': {'name': '质量定义方程', 'dimension': '[M]'},
            '公式4': {'name': '引力场定义方程', 'dimension': '[L][T]^{-2}'},
            '公式5': {'name': '静止动量方程', 'dimension': '[M][L][T]^{-1}'},
            '公式6': {'name': '运动动量方程', 'dimension': '[M][L][T]^{-1}'},
            '公式7': {'name': '宇宙大统一方程', 'dimension': '[M][L][T]^{-2}'},
            '公式8': {'name': '空间波动方程', 'dimension': '[L]^{-1}'},
            '公式9': {'name': '电荷定义方程', 'dimension': '[I][T]'},
            '公式10': {'name': '电场定义方程', 'dimension': '[M][L][T]^{-3}[I]^{-1}'},
            '公式11': {'name': '磁场定义方程', 'dimension': '[M][T]^{-2}[I]^{-1}'},
            '公式12': {'name': '变化的引力场产生电磁场', 'dimension': '[L][T]^{-2}'},
            '公式13': {'name': '磁矢势方程', 'dimension': '[M][T]^{-2}[I]^{-1}'},
            '公式14': {'name': '变化的引力场产生电场', 'dimension': '[M][L][T]^{-3}[I]^{-1}'},
            '公式15': {'name': '变化的磁场产生引力场和电场', 'dimension': '[M][T]^{-3}[I]^{-1}'},
            '公式16': {'name': '统一场论能量方程', 'dimension': '[M][L]^2[T]^{-2}'},
            '公式17': {'name': '光速飞行器动力学方程', 'dimension': '[M][L][T]^{-2}'},
            '公式18': {'name': '核力场定义方程', 'dimension': '[L]^{-2}[T]^{-2}'},
            '公式19': {'name': '引力光速统一方程', 'dimension': '[L]^3[T]^{-2}'},
            '公式20': {'name': '电磁光速几何耦合常数', 'dimension': '[L]^3[T]^{-2}'}
        }
        
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
        
        # 量纲转换规则
        self.dimension_rules = {
            '长度': '[L]',
            '时间': '[T]',
            '质量': '[M]',
            '电流': '[I]',
            '速度': '[L][T]^{-1}',
            '加速度': '[L][T]^{-2}',
            '力': '[M][L][T]^{-2}',
            '动量': '[M][L][T]^{-1}',
            '能量': '[M][L]^2[T]^{-2}',
            '电荷': '[I][T]',
            '电场': '[M][L][T]^{-3}[I]^{-1}',
            '磁场': '[M][T]^{-2}[I]^{-1}'
        }
    
    def parse_dimension(self, dimension_str: str) -> Dict[str, int]:
        """
        解析量纲字符串为字典形式
        
        Args:
            dimension_str: 量纲字符串，如 '[L][T]^{-1}'
            
        Returns:
            量纲字典，如 {'L': 1, 'T': -1}
        """
        if dimension_str == '1':
            return {}
        
        # 移除方括号并分割
        parts = dimension_str.replace('[', '').replace(']', '').split('^')
        
        result = {}
        current_base = None
        
        for part in parts:
            if any(char in 'LMIT' for char in part):
                # 基础量纲
                for char in part:
                    if char in 'LMIT':
                        current_base = char
                        result[current_base] = result.get(current_base, 0) + 1
            elif '{' in part and '}' in part:
                # 指数部分
                if current_base:
                    exponent = int(part.replace('{', '').replace('}', ''))
                    result[current_base] = exponent
        
        return result
    
    def combine_dimensions(self, dimensions: List[Dict[str, int]]) -> Dict[str, int]:
        """
        合并多个量纲
        
        Args:
            dimensions: 量纲字典列表
            
        Returns:
            合并后的量纲字典
        """
        combined = {}
        
        for dim in dimensions:
            for base, exponent in dim.items():
                combined[base] = combined.get(base, 0) + exponent
        
        return combined
    
    def validate_module_dimensions(self) -> List[Dict[str, Any]]:
        """
        验证模块量纲
        
        Returns:
            验证结果列表
        """
        results = []
        
        for module_id, module_info in self.modules.items():
            dim_str = module_info['dimension']
            dim_dict = self.parse_dimension(dim_str)
            
            # 检查量纲是否合法
            valid = all(base in 'LMIT' for base in dim_dict.keys())
            
            results.append({
                'module_id': module_id,
                'module_name': module_info['name'],
                'dimension': dim_str,
                'parsed_dimension': dim_dict,
                'valid': valid,
                'issues': [] if valid else ['量纲包含非法基本量']
            })
        
        return results
    
    def validate_formula_dimensions(self) -> List[Dict[str, Any]]:
        """
        验证公式量纲
        
        Returns:
            验证结果列表
        """
        results = []
        
        for formula_id, modules in self.formula_modules.items():
            formula_info = self.formula_dimensions[formula_id]
            formula_name = formula_info['name']
            expected_dim_str = formula_info['dimension']
            expected_dim = self.parse_dimension(expected_dim_str)
            
            # 计算模块组合的量纲
            module_dims = []
            for module_id in modules:
                module_info = self.modules[module_id]
                module_dim_str = module_info['dimension']
                module_dim = self.parse_dimension(module_dim_str)
                module_dims.append(module_dim)
            
            # 合并模块量纲
            actual_dim = self.combine_dimensions(module_dims)
            
            # 检查量纲是否一致
            valid = actual_dim == expected_dim
            
            issues = []
            if not valid:
                issues.append(f'量纲不一致：期望 {expected_dim_str}，实际 {actual_dim}')
            
            results.append({
                'formula_id': formula_id,
                'formula_name': formula_name,
                'expected_dimension': expected_dim_str,
                'actual_dimension': actual_dim,
                'modules': modules,
                'valid': valid,
                'issues': issues
            })
        
        return results
    
    def validate_physical_consistency(self) -> List[Dict[str, Any]]:
        """
        验证物理意义一致性
        
        Returns:
            验证结果列表
        """
        results = []
        
        # 检查常见物理量的量纲
        physical_quantities = {
            '速度': '[L][T]^{-1}',
            '加速度': '[L][T]^{-2}',
            '力': '[M][L][T]^{-2}',
            '动量': '[M][L][T]^{-1}',
            '能量': '[M][L]^2[T]^{-2}',
            '电荷': '[I][T]',
            '电场': '[M][L][T]^{-3}[I]^{-1}',
            '磁场': '[M][T]^{-2}[I]^{-1}'
        }
        
        for quantity, expected_dim in physical_quantities.items():
            # 查找相关公式
            related_formulas = []
            for formula_id, formula_info in self.formula_dimensions.items():
                if quantity in formula_info['name']:
                    actual_dim = formula_info['dimension']
                    valid = actual_dim == expected_dim
                    related_formulas.append({
                        'formula_id': formula_id,
                        'formula_name': formula_info['name'],
                        'actual_dimension': actual_dim,
                        'expected_dimension': expected_dim,
                        'valid': valid
                    })
            
            if related_formulas:
                all_valid = all(f['valid'] for f in related_formulas)
                results.append({
                    'physical_quantity': quantity,
                    'expected_dimension': expected_dim,
                    'related_formulas': related_formulas,
                    'all_valid': all_valid
                })
        
        return results
    
    def generate_validation_report(self) -> str:
        """
        生成验证报告
        
        Returns:
            验证报告内容
        """
        from datetime import datetime
        
        report = "# 统一场论量纲一致性验证报告\n\n"
        report += f"**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}\n\n"
        
        # 模块量纲验证
        module_results = self.validate_module_dimensions()
        report += "## 1. 模块量纲验证\n\n"
        report += "| 模块ID | 模块名称 | 量纲 | 验证结果 | 问题 |\n"
        report += "|-------|---------|------|---------|------|\n"
        
        valid_modules = 0
        total_modules = len(module_results)
        
        for result in module_results:
            status = "✓" if result['valid'] else "✗"
            issues = ", ".join(result['issues']) if result['issues'] else "无"
            report += f"| {result['module_id']} | {result['module_name']} | {result['dimension']} | {status} | {issues} |\n"
            if result['valid']:
                valid_modules += 1
        
        report += f"\n**模块量纲验证结果**：{valid_modules}/{total_modules} 个模块量纲正确\n\n"
        
        # 公式量纲验证
        formula_results = self.validate_formula_dimensions()
        report += "## 2. 公式量纲验证\n\n"
        report += "| 公式ID | 公式名称 | 期望量纲 | 实际量纲 | 验证结果 | 问题 |\n"
        report += "|-------|---------|----------|----------|---------|------|\n"
        
        valid_formulas = 0
        total_formulas = len(formula_results)
        
        for result in formula_results:
            status = "✓" if result['valid'] else "✗"
            issues = ", ".join(result['issues']) if result['issues'] else "无"
            report += f"| {result['formula_id']} | {result['formula_name']} | {result['expected_dimension']} | {result['actual_dimension']} | {status} | {issues} |\n"
            if result['valid']:
                valid_formulas += 1
        
        report += f"\n**公式量纲验证结果**：{valid_formulas}/{total_formulas} 个公式量纲正确\n\n"
        
        # 物理意义一致性验证
        physical_results = self.validate_physical_consistency()
        report += "## 3. 物理意义一致性验证\n\n"
        report += "| 物理量 | 期望量纲 | 相关公式验证结果 |\n"
        report += "|-------|----------|----------------|\n"
        
        valid_physical = 0
        total_physical = len(physical_results)
        
        for result in physical_results:
            status = "✓" if result['all_valid'] else "✗"
            report += f"| {result['physical_quantity']} | {result['expected_dimension']} | {status} |\n"
            if result['all_valid']:
                valid_physical += 1
        
        report += f"\n**物理意义一致性验证结果**：{valid_physical}/{total_physical} 个物理量量纲正确\n\n"
        
        # 综合分析
        report += "## 4. 综合分析\n\n"
        
        # 计算总体正确率
        overall_valid = valid_modules + valid_formulas + valid_physical
        overall_total = total_modules + total_formulas + total_physical
        overall_accuracy = (overall_valid / overall_total) * 100 if overall_total > 0 else 0
        
        report += f"- **总体验证正确率**：{overall_accuracy:.1f}%\n"
        report += f"- **模块量纲正确率**：{(valid_modules / total_modules) * 100:.1f}%\n"
        report += f"- **公式量纲正确率**：{(valid_formulas / total_formulas) * 100:.1f}%\n"
        report += f"- **物理意义正确率**：{(valid_physical / total_physical) * 100:.1f}%\n\n"
        
        # 常见问题分析
        report += "### 4.1 常见问题分析\n\n"
        
        # 收集所有问题
        all_issues = []
        for result in formula_results:
            if not result['valid']:
                all_issues.extend(result['issues'])
        
        if all_issues:
            report += "**发现的问题**：\n\n"
            for issue in set(all_issues):
                report += f"- {issue}\n"
        else:
            report += "**未发现明显问题**\n\n"
        
        # 建议
        report += "### 4.2 改进建议\n\n"
        if valid_formulas < total_formulas:
            report += "1. **检查模块与公式的关联**：确保每个公式使用的模块正确反映其物理意义\n"
            report += "2. **修正量纲不一致**：对于量纲不一致的公式，调整模块关联或量纲定义\n"
            report += "3. **验证物理常量**：确保所有物理常量的量纲正确\n"
        else:
            report += "1. **保持现有结构**：量纲验证结果良好，建议保持现有模块和公式结构\n"
            report += "2. **扩展验证范围**：可以考虑验证更多物理量的量纲一致性\n"
            report += "3. **建立自动验证机制**：在公式更新时自动进行量纲验证\n"
        
        # 结论
        report += "## 5. 结论\n\n"
        
        if overall_accuracy >= 90:
            report += "**验证结果**：优秀\n"
            report += "统一场论公式和模块的量纲一致性验证结果良好，表明理论体系在量纲层面是自洽的。\n"
        elif overall_accuracy >= 70:
            report += "**验证结果**：良好\n"
            report += "统一场论公式和模块的量纲一致性基本正确，但存在一些需要修正的问题。\n"
        else:
            report += "**验证结果**：需要改进\n"
            report += "统一场论公式和模块的量纲一致性存在较多问题，需要系统检查和修正。\n"
        
        report += "\n**量纲一致性是物理理论的基本要求**，通过本次验证，可以确保统一场论在数学形式上的正确性，为进一步的物理意义验证和实验验证奠定基础。\n"
        
        return report

if __name__ == "__main__":
    # 创建验证器实例
    validator = DimensionValidator()
    
    # 生成验证报告
    report = validator.generate_validation_report()
    
    # 保存报告
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = os.path.join(output_dir, "dimension_validation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"量纲一致性验证报告已生成：{report_path}")
    
    # 打印验证摘要
    module_results = validator.validate_module_dimensions()
    formula_results = validator.validate_formula_dimensions()
    physical_results = validator.validate_physical_consistency()
    
    valid_modules = sum(1 for r in module_results if r['valid'])
    valid_formulas = sum(1 for r in formula_results if r['valid'])
    valid_physical = sum(1 for r in physical_results if r['all_valid'])
    
    print(f"\n验证摘要：")
    print(f"模块量纲：{valid_modules}/{len(module_results)} 正确")
    print(f"公式量纲：{valid_formulas}/{len(formula_results)} 正确")
    print(f"物理意义：{valid_physical}/{len(physical_results)} 正确")
    print(f"总体正确率：{(valid_modules + valid_formulas + valid_physical) / (len(module_results) + len(formula_results) + len(physical_results)) * 100:.1f}%")
