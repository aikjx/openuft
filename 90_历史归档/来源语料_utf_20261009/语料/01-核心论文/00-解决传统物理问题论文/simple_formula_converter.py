#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单高效的公式LaTeX转换工具
专注于常见数学表达式的转换，避免复杂正则导致的性能问题
"""

import os
import re
import argparse
from typing import List, Pattern

def setup_logger():
    """设置日志"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

class SimpleFormulaConverter:
    def __init__(self, root_dir: str, recursive: bool = True):
        self.root_dir = root_dir
        self.recursive = recursive
        self.logger = setup_logger()
        self.total_files = 0
        self.processed_files = 0
        self.converted_formulas = 0
        
        # 已存在的LaTeX公式模式
        self.existing_latex_patterns: List[Pattern] = [
            re.compile(r'\$(.*?)\$'),
            re.compile(r'\$\$(.*?)\$\$', re.DOTALL),
            re.compile(r'```(?:math|latex)\s*(.*?)\s*```', re.DOTALL),
        ]
        
        # 常见的数学符号和运算符
        self.math_symbols = set('±×÷=<>≠≈≤≥√∫∑∏∂∇∈∉∪∩⊂⊃⊆⊇≡≅≡⊕⊗')
        self.math_operators = set('+-*/=<>!()[]{}^_')
    
    def _is_in_latex_formula(self, content: str, pos: int) -> bool:
        """检查位置是否在已有的LaTeX公式内"""
        for pattern in self.existing_latex_patterns:
            for match in pattern.finditer(content):
                if match.start() <= pos <= match.end():
                    return True
        return False
    
    def _contains_math(self, text: str) -> bool:
        """检查文本是否包含数学内容"""
        # 检查是否包含数学符号
        for char in text:
            if char in self.math_symbols or char in '^_':
                return True
        
        # 检查是否包含运算符和数字组合
        has_op = any(op in text for op in '*=<>')
        has_digit = any(char.isdigit() for char in text)
        if has_op and has_digit:
            return True
        
        # 检查分数形式
        if '/' in text and len(text) > 2:
            parts = text.split('/')
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                if not any(c in text for c in 'http:/.'):
                    if (any(c.isalnum() for c in parts[0]) and 
                        any(c.isalnum() for c in parts[1])):
                        return True
        
        return False
    
    def _is_plain_word(self, text: str) -> bool:
        """检查是否是纯英文单词"""
        return bool(re.match(r'^[a-zA-Z]+$', text))
    
    def _convert_to_latex(self, formula: str) -> str:
        """简单转换公式"""
        result = formula
        
        # 转换上标
        result = re.sub(r'(\w)\^([0-9])', r'\1^{\2}', result)
        result = re.sub(r'(\w)\^([a-zA-Z])', r'\1^{\2}', result)
        
        # 转换下标
        result = re.sub(r'(\w)_(\w)', r'\1_{\2}', result)
        
        # 转换平方根
        result = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', result)
        
        # 转换求和符号
        result = result.replace('sum_', '\\sum_')
        
        # 转换积分符号
        result = result.replace('int_', '\\int_')
        
        # 转换特殊上标数字
        sup_mapping = {
            '²': '^2', '³': '^3', '¹': '^1', '⁴': '^4', '⁵': '^5',
            '⁶': '^6', '⁷': '^7', '⁸': '^8', '⁹': '^9', '⁰': '^0'
        }
        for sup, replace in sup_mapping.items():
            if sup in result:
                result = result.replace(sup, replace)
        
        return result
    
    def _process_file(self, file_path: str) -> int:
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经包含LaTeX公式
            has_latex = any(pattern.search(content) for pattern in self.existing_latex_patterns)
            
            # 简单的公式匹配模式
            # 1. 包含数学符号的表达式
            formula_pattern = re.compile(r'\b[A-Za-z0-9\s\(\)\[\]{}^_+-]+[=<>≠≈≤≥][A-Za-z0-9\s\(\)\[\]{}^_+-]+\b')
            
            new_content = content
            offset = 0
            formula_count = 0
            
            for match in formula_pattern.finditer(content):
                formula = match.group(0).strip()
                start = match.start()
                end = match.end()
                
                # 跳过已在LaTeX公式内的内容
                if self._is_in_latex_formula(content, start):
                    continue
                
                # 跳过纯英文单词
                if self._is_plain_word(formula):
                    continue
                
                # 检查是否包含数学内容
                if self._contains_math(formula):
                    # 转换公式
                    converted = self._convert_to_latex(formula)
                    latex_formula = f"${converted}$"
                    
                    # 更新内容
                    new_content = (new_content[:start + offset] + 
                                  latex_formula + 
                                  new_content[end + offset:])
                    
                    offset += len(latex_formula) - len(formula)
                    formula_count += 1
            
            # 2. 特殊数学表达式: E=mc² 类型
            sup_pattern = re.compile(r'(\w)([²³¹⁴⁵⁶⁷⁸⁹⁰])')
            for match in sup_pattern.finditer(new_content):
                start = match.start()
                if not self._is_in_latex_formula(new_content, start):
                    char = match.group(1)
                    sup = match.group(2)
                    latex = f"${char}^{{ord('0')-ord(sup)}}$"  # 简化处理
                    new_content = (new_content[:start] + 
                                  latex + 
                                  new_content[start + 2:])
                    formula_count += 1
            
            # 保存文件
            if formula_count > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.logger.info(f"处理文件: {file_path}, 转换了 {formula_count} 个公式")
            elif has_latex:
                self.logger.info(f"文件 {file_path} 已包含LaTeX公式，无需转换")
            
            return formula_count
            
        except Exception as e:
            self.logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            return 0
    
    def run(self):
        """运行转换"""
        self.logger.info(f"开始转换目录: {self.root_dir}")
        
        if self.recursive:
            for root, _, files in os.walk(self.root_dir):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        self.total_files += 1
                        count = self._process_file(file_path)
                        if count > 0:
                            self.processed_files += 1
                            self.converted_formulas += count
        else:
            # 非递归模式
            for file in os.listdir(self.root_dir):
                file_path = os.path.join(self.root_dir, file)
                if os.path.isfile(file_path) and file.endswith('.md'):
                    self.total_files += 1
                    count = self._process_file(file_path)
                    if count > 0:
                        self.processed_files += 1
                        self.converted_formulas += count
        
        self.logger.info(f"转换完成!")
        self.logger.info(f"总文件数: {self.total_files}")
        self.logger.info(f"处理的文件数: {self.processed_files}")
        self.logger.info(f"转换的公式数: {self.converted_formulas}")

def main():
    parser = argparse.ArgumentParser(description='简单公式LaTeX转换工具')
    parser.add_argument('--root-dir', 
                       default='d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\00-解决传统物理问题论文',
                       help='要处理的根目录')
    parser.add_argument('--non-recursive', action='store_true', help='非递归处理')
    
    args = parser.parse_args()
    
    converter = SimpleFormulaConverter(
        root_dir=args.root_dir,
        recursive=not args.non_recursive
    )
    converter.run()

if __name__ == "__main__":
    main()
