#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式自动转换为LaTeX格式工具
用于扫描指定目录中的Markdown文件，识别非LaTeX格式的数学公式，并自动转换为LaTeX格式
"""

import os
import re
import argparse
import logging
from typing import List, Dict, Tuple, Pattern

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('formula_conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FormulaToLatexConverter:
    def __init__(self, root_dir: str, recursive: bool = True):
        self.root_dir = root_dir
        self.recursive = recursive
        self.processed_files = 0
        self.converted_formulas = 0
        
        # 已经是LaTeX格式的公式模式（避免重复转换）
        self.existing_latex_patterns = [
            # 行内公式: $公式$
            re.compile(r'\$(.*?)\$', re.DOTALL),
            # 块级公式: $$公式$$
            re.compile(r'\$\$(.*?)\$\$', re.DOTALL),
            # 块级公式: ```math或```latex
            re.compile(r'```(?:math|latex)\s*(.*?)\s*```', re.DOTALL),
        ]
        
        # 需要转换的公式模式列表
        self.conversion_patterns = self._init_conversion_patterns()
    
    def _init_conversion_patterns(self) -> List[Tuple[Pattern, str]]:
        """初始化需要转换的公式模式和对应的替换格式"""
        patterns = []
        
        # 1. 上标模式: x^2, a^b, E=mc^2
        patterns.append((
            re.compile(r'(\\?[a-zA-Z0-9\\(\\)\\[\\]{}]+)\^(\\?[a-zA-Z0-9\\(\\)\\[\\]{}]+)'),
            lambda m: f"{m.group(1)}^{{{m.group(2)}}}"
        ))
        
        # 2. 下标模式: x_i, a_1, H_0
        patterns.append((
            re.compile(r'(\\?[a-zA-Z0-9\\(\\)\\[\\]{}]+)_(\\?[a-zA-Z0-9\\(\\)\\[\\]{}]+)'),
            lambda m: f"{m.group(1)}_{{{m.group(2)}}}"
        ))
        
        # 3. 分数模式: a/b, (a+b)/(c+d)
        patterns.append((
            re.compile(r'(\\?[a-zA-Z0-9\\(\\)\\[\\]{}+\-*/\\s]+)/(\\?[a-zA-Z0-9\\(\\)\\[\\]{}+\-*/\\s]+)'),
            lambda m: f"\\frac{{{m.group(1).strip()}}}{{{m.group(2).strip()}}}"
        ))
        
        # 4. 平方根模式: sqrt(a), sqrt(x^2+y^2)
        patterns.append((
            re.compile(r'sqrt\\((.*?)\\)'),
            lambda m: f"\\sqrt{{{m.group(1)}}}"
        ))
        
        # 5. 常见数学符号替换
        math_symbols = {
            r'alpha': r'\\alpha',
            r'beta': r'\\beta',
            r'gamma': r'\\gamma',
            r'delta': r'\\delta',
            r'epsilon': r'\\epsilon',
            r'lambda': r'\\lambda',
            r'mu': r'\\mu',
            r'pi': r'\\pi',
            r'sigma': r'\\sigma',
            r'omega': r'\\omega',
            r'\|': r'\\',
            r'->': r'\\rightarrow',
            r'<-': r'\\leftarrow',
            r'<->': r'\\leftrightarrow',
            r'<<': r'\\ll',
            r'>>': r'\\gg',
            r'>=': r'\\geq',
            r'<=': r'\\leq',
            r'!=': r'\\neq',
            r'==': r'\\equiv',
        }
        
        for symbol, latex_symbol in math_symbols.items():
            patterns.append((
                re.compile(re.escape(symbol)),
                latex_symbol
            ))
        
        return patterns
    
    def _is_latex_formula(self, text: str) -> bool:
        """检查文本是否已经是LaTeX格式的公式"""
        for pattern in self.existing_latex_patterns:
            if pattern.search(text):
                return True
        return False
    
    def _extract_formula_candidates(self, content: str) -> List[Tuple[int, int, str]]:
        """从文本中提取可能是公式的候选内容"""
        candidates = []
        
        # 1. 提取可能的数学表达式（包含数学符号的文本）
        # 匹配包含数字、字母、常见数学符号的连续文本
        formula_pattern = re.compile(r'[a-zA-Z0-9\\(\\)\\[\\]{}^_+\-*/=<>!|\\s]+')
        matches = formula_pattern.finditer(content)
        
        for match in matches:
            text = match.group(0).strip()
            # 过滤掉太短或不包含数学符号的文本
            if len(text) > 2 and any(char in '^_=+-*/()[]{}<>!|' for char in text):
                # 检查是否在代码块中
                if not self._in_code_block(content, match.start(), match.end()):
                    candidates.append((match.start(), match.end(), text))
        
        # 2. 特殊处理独立行的公式（通常是块级公式）
        lines = content.split('\n')
        line_start = 0
        for line in lines:
            line_text = line.strip()
            # 检查是否是独立行的公式（不包含普通文本，只包含数学表达式）
            if len(line_text) > 2 and all(char.isalnum() or char in '^_=+-*/()[]{}<>!|\s\\' for char in line_text):
                if any(char in '^_=+-*/()[]{}<>!' for char in line_text) and not self._is_latex_formula(line_text):
                    line_end = line_start + len(line)
                    candidates.append((line_start, line_end, line_text))
            line_start += len(line) + 1  # +1 for the newline
        
        # 去重重叠的候选
        unique_candidates = []
        seen_ranges = set()
        for start, end, text in candidates:
            if (start, end) not in seen_ranges:
                # 检查是否与已添加的候选重叠
                overlapping = False
                for s, e, _ in unique_candidates:
                    if not (end <= s or start >= e):
                        overlapping = True
                        # 保留较长的候选
                        if end - start > e - s:
                            unique_candidates.remove((s, e, _))
                            unique_candidates.append((start, end, text))
                            seen_ranges.add((start, end))
                            seen_ranges.remove((s, e))
                        break
                if not overlapping:
                    unique_candidates.append((start, end, text))
                    seen_ranges.add((start, end))
        
        return sorted(unique_candidates, key=lambda x: x[0])
    
    def _in_code_block(self, content: str, start: int, end: int) -> bool:
        """检查指定位置是否在代码块内"""
        # 查找所有代码块标记
        code_block_markers = list(re.finditer(r'```', content))
        
        in_code_block = False
        for i, marker in enumerate(code_block_markers):
            marker_pos = marker.start()
            if marker_pos < start:
                in_code_block = not in_code_block
            elif marker_pos < end:
                # 如果结束位置在代码块标记之后，说明跨越了代码块边界
                return True
            else:
                break
        
        return in_code_block
    
    def _convert_formula_to_latex(self, formula: str) -> str:
        """将非LaTeX格式的公式转换为LaTeX格式"""
        # 应用所有转换模式
        latex_formula = formula
        
        for pattern, replacement in self.conversion_patterns:
            if callable(replacement):
                latex_formula = pattern.sub(replacement, latex_formula)
            else:
                latex_formula = pattern.sub(replacement, latex_formula)
        
        return latex_formula
    
    def _process_file(self, file_path: str) -> bool:
        """处理单个Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取公式候选
            formula_candidates = self._extract_formula_candidates(content)
            
            if not formula_candidates:
                logger.info(f"文件 {file_path} 中未发现需要转换的公式")
                return False
            
            # 从后往前替换，避免位置偏移
            formula_candidates.reverse()
            modified_content = content
            converted_count = 0
            
            for start, end, formula in formula_candidates:
                # 检查这个公式是否已经在LaTeX环境中
                if not self._is_latex_formula(formula):
                    # 判断是行内公式还是块级公式
                    if '\n' in formula or len(formula) > 50 or any(line.strip() for line in formula.split('\n')):
                        # 块级公式
                        latex_formula = self._convert_formula_to_latex(formula.strip())
                        modified_content = modified_content[:start] + f"$$\n{latex_formula}\n$$" + modified_content[end:]
                    else:
                        # 行内公式
                        latex_formula = self._convert_formula_to_latex(formula)
                        modified_content = modified_content[:start] + f"${latex_formula}$" + modified_content[end:]
                    converted_count += 1
            
            if converted_count > 0:
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                logger.info(f"文件 {file_path} 已处理，转换了 {converted_count} 个公式")
                self.processed_files += 1
                self.converted_formulas += converted_count
                return True
            else:
                logger.info(f"文件 {file_path} 中没有需要转换的新公式")
                return False
                
        except Exception as e:
            logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            return False
    
    def run(self) -> None:
        """运行转换工具的主函数"""
        logger.info(f"开始扫描目录: {self.root_dir}")
        
        if self.recursive:
            for root, _, files in os.walk(self.root_dir):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        self._process_file(file_path)
        else:
            # 只处理根目录下的文件
            for file in os.listdir(self.root_dir):
                file_path = os.path.join(self.root_dir, file)
                if os.path.isfile(file_path) and file.endswith('.md'):
                    self._process_file(file_path)
        
        logger.info(f"转换完成! 共处理 {self.processed_files} 个文件，转换了 {self.converted_formulas} 个公式")

def main():
    parser = argparse.ArgumentParser(description='公式自动转换为LaTeX格式工具')
    parser.add_argument('--root-dir', 
                       default='d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\00-解决传统物理问题论文',
                       help='要扫描的根目录')
    parser.add_argument('--non-recursive', action='store_true',
                       help='是否只处理根目录下的文件（不递归子目录）')
    
    args = parser.parse_args()
    
    converter = FormulaToLatexConverter(args.root_dir, not args.non_recursive)
    converter.run()

if __name__ == "__main__":
    main()
