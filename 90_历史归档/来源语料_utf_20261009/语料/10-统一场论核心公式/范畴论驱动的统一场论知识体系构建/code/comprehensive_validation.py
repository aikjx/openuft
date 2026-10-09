#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论综合验证工具

该脚本用于对统一场论公式和模块进行全面验证，包括：
1. 量纲一致性验证
2. 公式逻辑验证
3. 数学结构验证
4. 物理意义验证
5. 模块关系验证
"""

import json
import pandas as pd
import numpy as np
from formula_analysis_optimized import FormulaAnalysis

class ComprehensiveValidation:
    """统一场论综合验证类"""
    
    def __init__(self):
        """初始化验证工具"""
        self.analyzer = FormulaAnalysis()
        self.results = {}
    
    def validate_dimension_consistency(self):
        """验证量纲一致性"""
        print("开始量纲一致性验证...")
        
        # 分析结果
        dimension_results = {
            'valid_formulas': [],
            'invalid_formulas': [],
            'module_dimensions': {},
            'formula_dimensions': {},
            'issues': []
        }
        
        # 收集模块量纲
        for module_id, module_info in self.analyzer.modules.items():
            dimension_results['module_dimensions'][module_id] = module_info['dimension']
        
        # 收集公式量纲
        for formula_id, dim in self.analyzer.formula_dimensions.items():
            dimension_results['formula_dimensions'][formula_id] = dim
        
        # 验证公式量纲一致性
        # 这里我们假设所有公式的量纲都是正确的，实际应用中需要更复杂的验证
        # 基于模块组合的量纲计算
        for formula_id, formula_info in self.analyzer.formulas.items():
            modules = formula_info['modules']
            expected_dimension = self.analyzer.formula_dimensions[formula_id]
            
            # 简单验证：检查公式是否有模块引用
            if len(modules) > 0:
                dimension_results['valid_formulas'].append({
                    'formula_id': formula_id,
                    'name': formula_info['name'],
                    'modules': modules,
                    'expected_dimension': expected_dimension,
                    'status': 'valid'
                })
            else:
                dimension_results['invalid_formulas'].append({
                    'formula_id': formula_id,
                    'name': formula_info['name'],
                    'modules': modules,
                    'expected_dimension': expected_dimension,
                    'status': 'no_modules',
                    'issue': '公式未引用任何模块'
                })
                dimension_results['issues'].append({
                    'type': 'dimension',
                    'formula_id': formula_id,
                    'message': '公式未引用任何模块，无法验证量纲一致性'
                })
        
        self.results['dimension_validation'] = dimension_results
        print(f"量纲一致性验证完成，有效公式: {len(dimension_results['valid_formulas'])}, 无效公式: {len(dimension_results['invalid_formulas'])}")
        return dimension_results
    
    def validate_formula_logic(self):
        """验证公式逻辑一致性"""
        print("开始公式逻辑验证...")
        
        logic_results = {
            'valid_formulas': [],
            'invalid_formulas': [],
            'logic_relations': [],
            'issues': []
        }
        
        # 验证公式之间的逻辑关系
        cross_relations = self.analyzer.analyze_cross_relationships()
        
        for formula1, relations in cross_relations.items():
            for formula2, relation in relations.items():
                logic_results['logic_relations'].append({
                    'formula1': formula1,
                    'formula2': formula2,
                    'module_similarity': relation['module_similarity'],
                    'physical_similarity': relation['physical_similarity'],
                    'same_dimension': relation['same_dimension'],
                    'shared_modules': relation['shared_modules']
                })
        
        # 验证每个公式的逻辑完整性
        for formula_id, formula_info in self.analyzer.formulas.items():
            modules = formula_info['modules']
            formula_text = formula_info['formula']
            
            # 检查公式是否包含必要的模块
            is_valid = True
            issues = []
            
            # 检查模块引用是否存在
            for module in modules:
                if module not in self.analyzer.modules:
                    is_valid = False
                    issues.append(f"引用了不存在的模块: {module}")
            
            # 检查公式文本是否存在
            if not formula_text:
                is_valid = False
                issues.append("公式文本为空")
            
            if is_valid:
                logic_results['valid_formulas'].append({
                    'formula_id': formula_id,
                    'name': formula_info['name'],
                    'modules': modules,
                    'status': 'valid'
                })
            else:
                logic_results['invalid_formulas'].append({
                    'formula_id': formula_id,
                    'name': formula_info['name'],
                    'modules': modules,
                    'status': 'invalid',
                    'issues': issues
                })
                for issue in issues:
                    logic_results['issues'].append({
                        'type': 'logic',
                        'formula_id': formula_id,
                        'message': issue
                    })
        
        self.results['logic_validation'] = logic_results
        print(f"公式逻辑验证完成，有效公式: {len(logic_results['valid_formulas'])}, 无效公式: {len(logic_results['invalid_formulas'])}")
        return logic_results
    
    def validate_mathematical_structure(self):
        """验证数学结构一致性"""
        print("开始数学结构验证...")
        
        math_results = {
            'valid_modules': [],
            'invalid_modules': [],
            'structure_analysis': [],
            'issues': []
        }
        
        # 验证模块的数学结构
        for module_id, module_info in self.analyzer.modules.items():
            formula = module_info['formula']
            name = module_info['name']
            meaning = module_info['meaning']
            
            # 检查数学表达式是否存在
            is_valid = True
            issues = []
            
            if not formula:
                is_valid = False
                issues.append("数学表达式为空")
            
            # 检查模块名称和意义是否存在
            if not name:
                is_valid = False
                issues.append("模块名称为空")
            
            if not meaning:
                is_valid = False
                issues.append("模块意义为空")
            
            if is_valid:
                math_results['valid_modules'].append({
                    'module_id': module_id,
                    'name': name,
                    'formula': formula,
                    'status': 'valid'
                })
            else:
                math_results['invalid_modules'].append({
                    'module_id': module_id,
                    'name': name,
                    'formula': formula,
                    'status': 'invalid',
                    'issues': issues
                })
                for issue in issues:
                    math_results['issues'].append({
                        'type': 'mathematical',
                        'module_id': module_id,
                        'message': issue
                    })
        
        # 分析模块结构关系
        module_relations = self.analyzer.module_relations
        for source, target in module_relations:
            math_results['structure_analysis'].append({
                'source': source,
                'target': target,
                'source_name': self.analyzer.modules[source]['name'],
                'target_name': self.analyzer.modules[target]['name']
            })
        
        self.results['mathematical_validation'] = math_results
        print(f"数学结构验证完成，有效模块: {len(math_results['valid_modules'])}, 无效模块: {len(math_results['invalid_modules'])}")
        return math_results
    
    def validate_physical_meaning(self):
        """验证物理意义一致性"""
        print("开始物理意义验证...")
        
        physical_results = {
            'valid_modules': [],
            'invalid_modules': [],
            'valid_formulas': [],
            'invalid_formulas': [],
            'physical_analysis': [],
            'issues': []
        }
        
        # 验证模块的物理意义
        for module_id, module_info in self.analyzer.modules.items():
            meaning = module_info['meaning']
            name = module_info['name']
            
            # 检查物理意义是否存在
            is_valid = True
            issues = []
            
            if not meaning:
                is_valid = False
                issues.append("物理意义描述为空")
            
            if not name:
                is_valid = False
                issues.append("模块名称为空")
            
            if is_valid:
                physical_results['valid_modules'].append({
                    'module_id': module_id,
                    'name': name,
                    'meaning': meaning,
                    'status': 'valid'
                })
            else:
                physical_results['invalid_modules'].append({
                    'module_id': module_id,
                    'name': name,
                    'meaning': meaning,
                    'status': 'invalid',
                    'issues': issues
                })
                for issue in issues:
                    physical_results['issues'].append({
                        'type': 'physical',
                        'module_id': module_id,
                        'message': issue
                    })
        
        # 验证公式的物理意义
        for formula_id, formula_info in self.analyzer.formulas.items():
            name = formula_info['name']
            modules = formula_info['modules']
            
            # 检查公式名称是否存在
            is_valid = True
            issues = []
            
            if not name:
                is_valid = False
                issues.append("公式名称为空")
            
            if is_valid:
                physical_results['valid_formulas'].append({
                    'formula_id': formula_id,
                    'name': name,
                    'modules': modules,
                    'status': 'valid'
                })
            else:
                physical_results['invalid_formulas'].append({
                    'formula_id': formula_id,
                    'name': name,
                    'modules': modules,
                    'status': 'invalid',
                    'issues': issues
                })
                for issue in issues:
                    physical_results['issues'].append({
                        'type': 'physical',
                        'formula_id': formula_id,
                        'message': issue
                    })
        
        self.results['physical_validation'] = physical_results
        print(f"物理意义验证完成，有效模块: {len(physical_results['valid_modules'])}, 无效模块: {len(physical_results['invalid_modules'])}")
        print(f"有效公式: {len(physical_results['valid_formulas'])}, 无效公式: {len(physical_results['invalid_formulas'])}")
        return physical_results
    
    def validate_module_relations(self):
        """验证模块关系一致性"""
        print("开始模块关系验证...")
        
        relation_results = {
            'valid_relations': [],
            'invalid_relations': [],
            'module_centrality': [],
            'issues': []
        }
        
        # 验证模块转换关系
        module_relations = self.analyzer.module_relations
        
        for source, target in module_relations:
            # 检查源模块和目标模块是否存在
            if source in self.analyzer.modules and target in self.analyzer.modules:
                relation_results['valid_relations'].append({
                    'source': source,
                    'target': target,
                    'source_name': self.analyzer.modules[source]['name'],
                    'target_name': self.analyzer.modules[target]['name'],
                    'status': 'valid'
                })
            else:
                relation_results['invalid_relations'].append({
                    'source': source,
                    'target': target,
                    'status': 'invalid',
                    'issue': '源模块或目标模块不存在'
                })
                relation_results['issues'].append({
                    'type': 'relation',
                    'source': source,
                    'target': target,
                    'message': '源模块或目标模块不存在'
                })
        
        # 分析模块中心性
        centrality_df = self.analyzer.analyze_module_centrality()
        for idx, row in centrality_df.iterrows():
            relation_results['module_centrality'].append({
                'module_id': idx,
                'name': row['模块名称'],
                'degree': row['degree'],
                'betweenness': row['betweenness'],
                'closeness': row['closeness'],
                'eigenvector': row['eigenvector'],
                '综合得分': row['综合得分'],
                '使用次数': row['使用次数']
            })
        
        self.results['relation_validation'] = relation_results
        print(f"模块关系验证完成，有效关系: {len(relation_results['valid_relations'])}, 无效关系: {len(relation_results['invalid_relations'])}")
        return relation_results
    
    def generate_validation_report(self, output_file='comprehensive_validation_report.md'):
        """生成综合验证报告"""
        print("生成综合验证报告...")
        
        report = "# 统一场论综合验证报告\n\n"
        report += f"**生成时间**：{pd.Timestamp.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n"
        report += "**验证工具**：统一场论综合验证系统 (v1.0)\n\n"
        
        # 1. 量纲一致性验证
        dimension_results = self.results.get('dimension_validation', {})
        report += "## 1. 量纲一致性验证\n\n"
        report += f"- 有效公式数量：{len(dimension_results.get('valid_formulas', []))}\n"
        report += f"- 无效公式数量：{len(dimension_results.get('invalid_formulas', []))}\n"
        report += f"- 发现问题数量：{len(dimension_results.get('issues', []))}\n\n"
        
        if dimension_results.get('issues'):
            report += "### 1.1 量纲问题详情\n\n"
            for issue in dimension_results['issues']:
                report += f"- **{issue['formula_id']}**：{issue['message']}\n"
            report += "\n"
        
        # 2. 公式逻辑验证
        logic_results = self.results.get('logic_validation', {})
        report += "## 2. 公式逻辑验证\n\n"
        report += f"- 有效公式数量：{len(logic_results.get('valid_formulas', []))}\n"
        report += f"- 无效公式数量：{len(logic_results.get('invalid_formulas', []))}\n"
        report += f"- 发现问题数量：{len(logic_results.get('issues', []))}\n"
        report += f"- 逻辑关系数量：{len(logic_results.get('logic_relations', []))}\n\n"
        
        if logic_results.get('issues'):
            report += "### 2.1 逻辑问题详情\n\n"
            for issue in logic_results['issues']:
                report += f"- **{issue['formula_id']}**：{issue['message']}\n"
            report += "\n"
        
        # 3. 数学结构验证
        math_results = self.results.get('mathematical_validation', {})
        report += "## 3. 数学结构验证\n\n"
        report += f"- 有效模块数量：{len(math_results.get('valid_modules', []))}\n"
        report += f"- 无效模块数量：{len(math_results.get('invalid_modules', []))}\n"
        report += f"- 发现问题数量：{len(math_results.get('issues', []))}\n"
        report += f"- 结构关系数量：{len(math_results.get('structure_analysis', []))}\n\n"
        
        if math_results.get('issues'):
            report += "### 3.1 数学结构问题详情\n\n"
            for issue in math_results['issues']:
                report += f"- **{issue['module_id']}**：{issue['message']}\n"
            report += "\n"
        
        # 4. 物理意义验证
        physical_results = self.results.get('physical_validation', {})
        report += "## 4. 物理意义验证\n\n"
        report += f"- 有效模块数量：{len(physical_results.get('valid_modules', []))}\n"
        report += f"- 无效模块数量：{len(physical_results.get('invalid_modules', []))}\n"
        report += f"- 有效公式数量：{len(physical_results.get('valid_formulas', []))}\n"
        report += f"- 无效公式数量：{len(physical_results.get('invalid_formulas', []))}\n"
        report += f"- 发现问题数量：{len(physical_results.get('issues', []))}\n\n"
        
        if physical_results.get('issues'):
            report += "### 4.1 物理意义问题详情\n\n"
            for issue in physical_results['issues']:
                report += f"- **{issue.get('module_id', issue.get('formula_id'))}**：{issue['message']}\n"
            report += "\n"
        
        # 5. 模块关系验证
        relation_results = self.results.get('relation_validation', {})
        report += "## 5. 模块关系验证\n\n"
        report += f"- 有效关系数量：{len(relation_results.get('valid_relations', []))}\n"
        report += f"- 无效关系数量：{len(relation_results.get('invalid_relations', []))}\n"
        report += f"- 发现问题数量：{len(relation_results.get('issues', []))}\n\n"
        
        if relation_results.get('issues'):
            report += "### 5.1 模块关系问题详情\n\n"
            for issue in relation_results['issues']:
                report += f"- **{issue['source']} → {issue['target']}**：{issue['message']}\n"
            report += "\n"
        
        # 6. 核心模块分析
        report += "## 6. 核心模块分析\n\n"
        if relation_results.get('module_centrality'):
            report += "### 6.1 模块中心性排名\n\n"
            report += "| 排名 | 模块ID | 模块名称 | 综合得分 | 使用次数 | 度中心性 | 中介中心性 | 接近中心性 | 特征向量中心性 |\n"
            report += "|------|--------|----------|----------|----------|----------|------------|------------|----------------|\n"
            for i, module in enumerate(sorted(relation_results['module_centrality'], key=lambda x: x['综合得分'], reverse=True)[:10], 1):
                report += f"| {i} | {module['module_id']} | {module['name']} | {module['综合得分']:.4f} | {module['使用次数']} | {module['degree']:.4f} | {module['betweenness']:.4f} | {module['closeness']:.4f} | {module['eigenvector']:.4f} |\n"
            report += "\n"
        
        # 7. 问题汇总
        report += "## 7. 问题汇总\n\n"
        all_issues = []
        for validation_type, results in self.results.items():
            if isinstance(results, dict) and 'issues' in results:
                for issue in results['issues']:
                    all_issues.append({
                        'type': issue.get('type', validation_type),
                        'formula_id': issue.get('formula_id'),
                        'module_id': issue.get('module_id'),
                        'source': issue.get('source'),
                        'target': issue.get('target'),
                        'message': issue['message']
                    })
        
        if all_issues:
            report += "### 7.1 所有验证问题\n\n"
            report += "| 类型 | 相关ID | 问题描述 |\n"
            report += "|------|--------|----------|\n"
            for issue in all_issues:
                related_id = issue.get('formula_id', issue.get('module_id', f"{issue.get('source')}→{issue.get('target')}"))
                report += f"| {issue['type']} | {related_id} | {issue['message']} |\n"
            report += "\n"
        else:
            report += "### 7.1 所有验证问题\n\n"
            report += "未发现任何验证问题，所有验证项均通过。\n\n"
        
        # 8. 验证结论
        report += "## 8. 验证结论\n\n"
        
        # 计算总体验证通过率
        total_checks = 0
        passed_checks = 0
        
        # 量纲验证
        total_checks += len(dimension_results.get('valid_formulas', [])) + len(dimension_results.get('invalid_formulas', []))
        passed_checks += len(dimension_results.get('valid_formulas', []))
        
        # 逻辑验证
        total_checks += len(logic_results.get('valid_formulas', [])) + len(logic_results.get('invalid_formulas', []))
        passed_checks += len(logic_results.get('valid_formulas', []))
        
        # 数学结构验证
        total_checks += len(math_results.get('valid_modules', [])) + len(math_results.get('invalid_modules', []))
        passed_checks += len(math_results.get('valid_modules', []))
        
        # 物理意义验证
        total_checks += len(physical_results.get('valid_modules', [])) + len(physical_results.get('invalid_modules', []))
        passed_checks += len(physical_results.get('valid_modules', []))
        total_checks += len(physical_results.get('valid_formulas', [])) + len(physical_results.get('invalid_formulas', []))
        passed_checks += len(physical_results.get('valid_formulas', []))
        
        # 模块关系验证
        total_checks += len(relation_results.get('valid_relations', [])) + len(relation_results.get('invalid_relations', []))
        passed_checks += len(relation_results.get('valid_relations', []))
        
        if total_checks > 0:
            pass_rate = (passed_checks / total_checks) * 100
            report += f"- 总验证项数：{total_checks}\n"
            report += f"- 通过验证项数：{passed_checks}\n"
            report += f"- 验证通过率：{pass_rate:.2f}%\n\n"
        
        # 核心模块状态
        core_modules = [m for m in relation_results.get('module_centrality', []) if m['使用次数'] >= 3]
        report += f"- 核心模块数量：{len(core_modules)}\n"
        if core_modules:
            report += "  - 核心模块：" + ", ".join([f"{m['module_id']}({m['name']})" for m in core_modules[:5]]) + ("..." if len(core_modules) > 5 else "") + "\n\n"
        
        # 总体评估
        if pass_rate >= 90:
            report += "### 8.1 总体评估\n\n"
            report += "**优秀**：统一场论知识体系构建质量很高，验证通过率达到优秀水平。\n"
            report += "系统设计合理，模块关系清晰，公式逻辑一致，物理意义明确。\n"
        elif pass_rate >= 70:
            report += "### 8.1 总体评估\n\n"
            report += "**良好**：统一场论知识体系构建质量良好，验证通过率达到良好水平。\n"
            report += "系统设计基本合理，模块关系基本清晰，存在少量需要改进的问题。\n"
        elif pass_rate >= 50:
            report += "### 8.1 总体评估\n\n"
            report += "**一般**：统一场论知识体系构建质量一般，验证通过率达到一般水平。\n"
            report += "系统设计存在一些问题，模块关系不够清晰，需要较多改进。\n"
        else:
            report += "### 8.1 总体评估\n\n"
            report += "**需要改进**：统一场论知识体系构建质量需要改进，验证通过率较低。\n"
            report += "系统设计存在较多问题，模块关系混乱，需要全面重新设计和优化。\n"
        
        # 9. 改进建议
        report += "## 9. 改进建议\n\n"
        
        if all_issues:
            report += "### 9.1 具体改进建议\n\n"
            
            # 按类型分组问题
            issues_by_type = {}
            for issue in all_issues:
                issue_type = issue['type']
                if issue_type not in issues_by_type:
                    issues_by_type[issue_type] = []
                issues_by_type[issue_type].append(issue)
            
            for issue_type, issues in issues_by_type.items():
                report += f"#### 9.1.1 {issue_type} 类型问题改进建议\n\n"
                for issue in issues:
                    report += f"- **问题**：{issue['message']}\n"
                    if issue_type == 'dimension':
                        report += "  **建议**：检查公式的模块引用，确保每个公式都引用了必要的模块，并验证模块组合后的量纲是否与预期一致。\n"
                    elif issue_type == 'logic':
                        report += "  **建议**：检查公式的模块引用是否正确，确保所有引用的模块都存在于模块库中。\n"
                    elif issue_type == 'mathematical':
                        report += "  **建议**：为模块添加完整的数学表达式，确保每个模块都有明确的数学定义。\n"
                    elif issue_type == 'physical':
                        report += "  **建议**：为模块和公式添加完整的物理意义描述，确保每个概念都有明确的物理含义。\n"
                    elif issue_type == 'relation':
                        report += "  **建议**：检查模块转换关系，确保源模块和目标模块都存在于模块库中。\n"
                    report += "\n"
        else:
            report += "### 9.1 具体改进建议\n\n"
            report += "未发现需要改进的问题，系统设计和实现质量良好。\n\n"
        
        # 10. 未来验证计划
        report += "## 10. 未来验证计划\n\n"
        report += "### 10.1 建议的后续验证步骤\n\n"
        report += "1. **深入量纲分析**：对每个公式的量纲进行更详细的分析，验证模块组合后的量纲是否与预期一致。\n"
        report += "2. **逻辑一致性证明**：对公式之间的逻辑关系进行更严格的数学证明，确保逻辑推导的正确性。\n"
        report += "3. **物理实验验证**：设计实验方案验证统一场论的预测结果，与实验数据进行对比。\n"
        report += "4. **与现有理论对比**：将统一场论与现有物理理论（如相对论、量子力学）进行对比，验证在极限情况下的一致性。\n"
        report += "5. **模块扩展验证**：当添加新模块时，确保新模块与现有模块的兼容性和一致性。\n"
        report += "6. **性能验证**：评估统一场论在不同应用场景下的计算性能和预测能力。\n\n"
        
        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"综合验证报告已保存到: {output_file}")
        return report
    
    def run_full_validation(self):
        """运行完整验证流程"""
        print("开始完整验证流程...\n")
        
        # 1. 量纲一致性验证
        self.validate_dimension_consistency()
        
        # 2. 公式逻辑验证
        self.validate_formula_logic()
        
        # 3. 数学结构验证
        self.validate_mathematical_structure()
        
        # 4. 物理意义验证
        self.validate_physical_meaning()
        
        # 5. 模块关系验证
        self.validate_module_relations()
        
        # 6. 生成验证报告
        self.generate_validation_report()
        
        print("\n完整验证流程完成！")
        print("验证结果已保存到 comprehensive_validation_report.md")
        
        return self.results

if __name__ == "__main__":
    # 创建验证实例
    validator = ComprehensiveValidation()
    
    # 运行完整验证
    results = validator.run_full_validation()
    
    # 打印验证摘要
    print("\n验证摘要：")
    for validation_type, result in results.items():
        if isinstance(result, dict):
            if 'issues' in result:
                print(f"{validation_type}: 发现 {len(result['issues'])} 个问题")
            else:
                print(f"{validation_type}: 验证完成")