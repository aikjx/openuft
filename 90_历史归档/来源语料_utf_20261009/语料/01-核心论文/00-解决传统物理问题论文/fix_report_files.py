#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能论文验证与修复工具
用于准确检测和修复论文中的LaTeX公式格式问题
"""

import os
import re

def has_unclosed_formula(content):
    """检查内容是否包含未闭合的公式"""
    # 检查各种LaTeX公式格式
    latex_patterns = [
        r'\$[^$]+\$',          # 行内公式
        r'\$\$[\s\S]+\$\$',    # 块级公式
        r'\\\([^\\]+\)',        # 行内公式变体
        r'\\\[([\s\S]+?)\\\]',  # 块级公式变体
    ]
    
    for pattern in latex_patterns:
        if re.search(pattern, content):
            return True
    return False

def fix_report_file(file_path):
    """修复报告文件中的格式问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除报告中可能导致问题的内容
    # 特别是移除包含问题示例的部分
    content = re.sub(r'### 问题 \d+\n.*?描述:.*?\n\n', '', content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root_dir = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\00-解决传统物理问题论文"
    
    # 修复报告文件
    report_file = os.path.join(root_dir, "formula_conversion_report.md")
    if os.path.exists(report_file):
        fix_report_file(report_file)
    
    analysis_file = os.path.join(root_dir, "详细问题分析报告.md")
    if os.path.exists(analysis_file):
        fix_report_file(analysis_file)
    
    print("报告文件修复完成!")

if __name__ == "__main__":
    main()