#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式转换验证工具
用于验证所有Markdown文件中的公式是否已正确转换为LaTeX格式
"""

import os
import re
import argparse
import logging
from typing import List, Dict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('formula_verification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FormulaConversionVerifier:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.total_files = 0
        self.files_with_formulas = 0
        self.total_latex_formulas = 0
        self.issues_found = 0
        self.files_with_issues = []
        
        # LaTeX公式模式
        self.latex_patterns = [
            # 行内公式: $公式$
            ('行内公式', re.compile(r'\$(.*?)\$', re.DOTALL)),
            # 块级公式: $$公式$$
            ('块级公式', re.compile(r'\$\$(.*?)\$\$', re.DOTALL)),
            # 块级公式: ```math或```latex
            ('代码块公式', re.compile(r'```(?:math|latex)\s*(.*?)\s*```', re.DOTALL)),
        ]
        
        # 可能存在问题的公式模式（未完全转换的公式）
        self.problematic_patterns = [
            # 未转换的上标
            (re.compile(r'[^\\][a-zA-Z0-9]+\^[^\\{]'), '未转换的上标（如 x^2 应改为 x^{2}）'),
            # 未转换的下标
            (re.compile(r'[^\\][a-zA-Z0-9]+_[^\\{]'), '未转换的下标（如 x_i 应改为 x_{i}）'),
            # 未转换的分数
            (re.compile(r'[^\\/][a-zA-Z0-9\(\)]+/[^\\/]'), '未转换的分数（如 a/b 应改为 \\frac{a}{b}）'),
            # 未包含在$中的数学表达式
            (re.compile(r'\b[a-zA-Z0-9\(\)\[\]{}^_+\-*/=<>!]{4,}\b'), '可能是未转换的公式（未包含在$中）'),
        ]
    
    def _verify_file(self, file_path: str) -> Dict:
        """验证单个文件中的公式转换情况"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_info = {
                'path': file_path,
                'latex_formulas': [],
                'issues': []
            }
            
            # 统计LaTeX公式
            for pattern_name, pattern in self.latex_patterns:
                matches = pattern.finditer(content)
                for match in matches:
                    formula = match.group(1).strip() if pattern_name != '代码块公式' else match.group(1).strip()
                    file_info['latex_formulas'].append({
                        'type': pattern_name,
                        'content': formula,
                        'start_pos': match.start(),
                        'end_pos': match.end()
                    })
            
            # 检查可能存在问题的公式
            for pattern, issue_description in self.problematic_patterns:
                matches = pattern.finditer(content)
                for match in matches:
                    # 确保问题模式不在已识别的LaTeX公式内
                    in_latex_formula = False
                    for formula_info in file_info['latex_formulas']:
                        if formula_info['start_pos'] <= match.start() and match.end() <= formula_info['end_pos']:
                            in_latex_formula = True
                            break
                    
                    if not in_latex_formula and len(match.group(0).strip()) > 2:
                        file_info['issues'].append({
                            'description': issue_description,
                            'content': match.group(0),
                            'start_pos': match.start(),
                            'end_pos': match.end()
                        })
            
            return file_info
            
        except Exception as e:
            logger.error(f"验证文件 {file_path} 时出错: {str(e)}")
            return {
                'path': file_path,
                'latex_formulas': [],
                'issues': [{'description': f'文件读取错误: {str(e)}', 'content': '', 'start_pos': 0, 'end_pos': 0}]
            }
    
    def run_verification(self) -> None:
        """运行验证并生成报告"""
        logger.info(f"开始验证目录: {self.root_dir}")
        
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self.total_files += 1
                    
                    file_info = self._verify_file(file_path)
                    formula_count = len(file_info['latex_formulas'])
                    issue_count = len(file_info['issues'])
                    
                    if formula_count > 0:
                        self.files_with_formulas += 1
                        self.total_latex_formulas += formula_count
                        logger.info(f"文件 {file_path} 包含 {formula_count} 个LaTeX公式")
                    
                    if issue_count > 0:
                        self.issues_found += issue_count
                        self.files_with_issues.append(file_info)
                        logger.warning(f"文件 {file_path} 发现 {issue_count} 个潜在问题")
        
        self._generate_report()
    
    def _generate_report(self) -> None:
        """生成验证报告"""
        report_path = 'formula_conversion_report.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 公式LaTeX转换验证报告\n\n")
            
            # 总结部分
            f.write("## 转换总结\n\n")
            f.write(f"- **总文件数**: {self.total_files}\n")
            f.write(f"- **包含公式的文件数**: {self.files_with_formulas}\n")
            f.write(f"- **总LaTeX公式数**: {self.total_latex_formulas}\n")
            f.write(f"- **发现问题数**: {self.issues_found}\n")
            f.write(f"- **问题文件数**: {len(self.files_with_issues)}\n\n")
            
            if self.issues_found == 0:
                f.write("### 转换状态: ✅ 成功\n\n")
                f.write("所有公式已成功转换为LaTeX格式，未发现任何问题。\n\n")
            else:
                f.write("### 转换状态: ⚠️ 需要注意\n\n")
                f.write("发现一些潜在问题，建议检查并手动修正。\n\n")
            
            # 详细问题列表
            if self.files_with_issues:
                f.write("## 详细问题列表\n\n")
                for file_info in self.files_with_issues:
                    f.write(f"### 文件: {file_info['path']}\n\n")
                    for issue in file_info['issues']:
                        f.write(f"- **问题类型**: {issue['description']}\n")
                        f.write(f"- **问题内容**: `{issue['content']}`\n\n")
            
            # 验证说明
            f.write("## 验证说明\n\n")
            f.write("1. 本报告通过正则表达式自动检测文件中的LaTeX公式和潜在问题。\n")
            f.write("2. 某些复杂公式可能需要手动检查和修正，特别是包含特殊符号或格式的公式。\n")
            f.write("3. 对于未完全转换的公式，建议参考LaTeX语法规范进行手动修正。\n\n")
        
        logger.info(f"验证报告已生成: {report_path}")
        logger.info(f"验证完成! 共检查 {self.total_files} 个文件，发现 {self.total_latex_formulas} 个LaTeX公式，{self.issues_found} 个潜在问题")

def main():
    parser = argparse.ArgumentParser(description='公式LaTeX转换验证工具')
    parser.add_argument('--root-dir', 
                       default='d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\00-解决传统物理问题论文',
                       help='要验证的根目录')
    
    args = parser.parse_args()
    
    verifier = FormulaConversionVerifier(args.root_dir)
    verifier.run_verification()

if __name__ == "__main__":
    main()
