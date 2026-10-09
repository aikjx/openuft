#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式LaTeX转换工具（优化版）
用于将Markdown文件中的非LaTeX格式公式转换为LaTeX格式
使用更精确的正则表达式和上下文识别，减少误报
"""

import os
import re
import argparse
import logging
from typing import Tuple, List, Pattern

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FormulaConverter:
    def __init__(self, root_dir: str, recursive: bool = True, dry_run: bool = False):
        self.root_dir = root_dir
        self.recursive = recursive
        self.dry_run = dry_run
        self.total_files = 0
        self.processed_files = 0
        self.converted_formulas = 0
        
        # 数学符号和运算符
        self.math_symbols = '±×÷=<>≠≈≤≥√∫∑∏∂∇∈∉∪∩⊂⊃⊆⊇≡≅≡⊕⊗'
        self.math_operators = '+-*/=<>!()[]{}^_'
        
        # 已存在的LaTeX公式模式
        self.existing_latex_patterns: List[Pattern] = [
            # 行内公式: $公式$
            re.compile(r'\$(.*?)\$'),
            # 块级公式: $$公式$$
            re.compile(r'\$\$(.*?)\$\$', re.DOTALL),
            # 块级公式: ```math或```latex
            re.compile(r'```(?:math|latex)\s*(.*?)\s*```', re.DOTALL),
        ]
    
    def _is_in_existing_latex(self, content: str, pos: int) -> bool:
        """检查指定位置是否在已有的LaTeX公式内"""
        for pattern in self.existing_latex_patterns:
            for match in pattern.finditer(content):
                if match.start() <= pos <= match.end():
                    return True
        return False
    
    def _contains_math_content(self, text: str) -> bool:
        """检查文本是否包含数学内容"""
        # 检查是否包含数学符号
        for char in text:
            if char in self.math_symbols or char in '^_':
                return True
        
        # 检查是否包含数学运算符和数字的组合
        if any(op in text for op in '*/=<>!') and any(char.isdigit() for char in text):
            return True
            
        # 检查分数形式 (a/b)
        if '/' in text and len(text) > 2:
            parts = text.split('/')
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                # 确保不是URL或文件路径
                if not any(c in text for c in 'http:\\.'):
                    # 确保分子和分母包含数字或字母
                    if (any(c.isalnum() for c in parts[0]) and 
                        any(c.isalnum() for c in parts[1])):
                        return True
        
        return False
    
    def _convert_formula(self, formula: str) -> str:
        """将非LaTeX格式的公式转换为LaTeX格式"""
        converted = formula
        
        # 转换上标: x^2 -> x^{2}
        converted = re.sub(r'(\w|\))\^(\w|\()', r'\1^{\2}', converted)
        
        # 转换下标: x_i -> x_{i}
        converted = re.sub(r'(\w|\))_(\w|\()', r'\1_{\2}', converted)
        
        # 转换分数: a/b -> \frac{a}{b}
        def replace_fraction(match):
            numerator = match.group(1).strip()
            denominator = match.group(2).strip()
            if len(numerator) > 1 or len(denominator) > 1:
                return f"\\frac{{{numerator}}}{{{denominator}}}"
            return match.group(0)
        
        fraction_pattern = r'(\w+(?:\^\{?\w+\}?|_\{?\w+\}?)?\*?\+?\-?)\s*\/\s*(\*?\+?\-?\w+(?:\^\{?\w+\}?|_\{?\w+\}?)?)'
        converted = re.sub(fraction_pattern, replace_fraction, converted)
        
        # 转换平方根: sqrt(x) -> \sqrt{x}
        converted = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', converted)
        
        # 转换求和
        if 'sum_' in converted:
            converted = converted.replace('sum_', '\\sum_')
        
        # 转换积分
        if 'int_' in converted:
            converted = converted.replace('int_', '\\int_')
        
        return converted
    
    def _detect_and_convert_formulas(self, content: str) -> Tuple[str, int]:
        """检测并转换文本中的公式"""
        converted_content = content
        formula_count = 0
        
        # 模式1: 包含数学符号或运算符的文本
        math_pattern = re.compile(r'[a-zA-Z0-9\s]+[' + re.escape(self.math_symbols + self.math_operators) + r'][a-zA-Z0-9\s]+')
        
        matches = list(math_pattern.finditer(content))
        
        for match in reversed(matches):
            formula_text = match.group(0).strip()
            start_pos = match.start()
            end_pos = match.end()
            
            # 跳过已在LaTeX公式内的内容
            if self._is_in_existing_latex(content, start_pos):
                continue
            
            # 跳过纯英文单词
            if re.match(r'^[a-zA-Z]+$', formula_text):
                continue
            
            # 跳过URL和邮箱
            if re.match(r'^https?://', formula_text.lower()) or '@' in formula_text:
                continue
            
            # 检查是否真正包含数学内容
            if self._contains_math_content(formula_text):
                # 转换公式
                converted_formula = self._convert_formula(formula_text)
                
                # 包装为行内LaTeX公式
                new_content = f"${converted_formula}$"
                
                # 更新内容
                converted_content = (converted_content[:start_pos] + 
                                    new_content + 
                                    converted_content[end_pos:])
                
                formula_count += 1
        
        # 模式2: 上标数字
        sup_pattern = re.compile(r'(\w)([²³¹⁴⁵⁶⁷⁸⁹⁰])')
        sup_mapping = {'²': '^2', '³': '^3', '¹': '^1', '⁴': '^4', '⁵': '^5', 
                      '⁶': '^6', '⁷': '^7', '⁸': '^8', '⁹': '^9', '⁰': '^0'}
        
        def replace_superscript(match):
            char = match.group(1)
            sup = match.group(2)
            replacement = f"{char}{sup_mapping[sup]}"
            return f"${replacement}$" if not self._is_in_existing_latex(converted_content, match.start()) else match.group(0)
        
        converted_content, sup_count = sup_pattern.subn(replace_superscript, converted_content)
        formula_count += sup_count
        
        return converted_content, formula_count
    
    def _process_file(self, file_path: str) -> int:
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查文件是否已经包含LaTeX公式
            has_existing_latex = any(pattern.search(content) for pattern in self.existing_latex_patterns)
            
            # 转换公式
            converted_content, formula_count = self._detect_and_convert_formulas(content)
            
            # 如果有转换，写入文件
            if formula_count > 0 and not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(converted_content)
                logger.info(f"已处理文件: {file_path}, 转换了 {formula_count} 个公式")
            elif formula_count == 0 and has_existing_latex:
                logger.info(f"文件 {file_path} 已包含LaTeX公式，无需转换")
            
            return formula_count
            
        except Exception as e:
            logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            return 0
    
    def run(self) -> None:
        """运行转换"""
        logger.info(f"开始转换目录: {self.root_dir}")
        
        if self.recursive:
            for root, _, files in os.walk(self.root_dir):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        self.total_files += 1
                        formula_count = self._process_file(file_path)
                        if formula_count > 0:
                            self.processed_files += 1
                            self.converted_formulas += formula_count
        else:
            # 非递归模式
            for file in os.listdir(self.root_dir):
                file_path = os.path.join(self.root_dir, file)
                if os.path.isfile(file_path) and file.endswith('.md'):
                    self.total_files += 1
                    formula_count = self._process_file(file_path)
                    if formula_count > 0:
                        self.processed_files += 1
                        self.converted_formulas += formula_count
        
        logger.info(f"转换完成!")
        logger.info(f"总文件数: {self.total_files}")
        logger.info(f"处理的文件数: {self.processed_files}")
        logger.info(f"转换的公式数: {self.converted_formulas}")

def main():
    parser = argparse.ArgumentParser(description='公式LaTeX转换工具（优化版）')
    parser.add_argument('--root-dir', 
                       default='d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\00-解决传统物理问题论文',
                       help='要处理的根目录')
    parser.add_argument('--non-recursive', action='store_true', help='非递归处理')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际修改文件')
    
    args = parser.parse_args()
    
    converter = FormulaConverter(
        root_dir=args.root_dir,
        recursive=not args.non_recursive,
        dry_run=args.dry_run
    )
    converter.run()

if __name__ == "__main__":
    main()
