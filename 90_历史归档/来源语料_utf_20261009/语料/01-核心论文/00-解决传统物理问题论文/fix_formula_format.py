#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式格式修复工具
用于修复转换后的LaTeX公式中存在的格式问题
主要修复：多个$符号连续使用的问题
"""

import os
import re

def fix_formula_format(content):
    # 修复连续的$符号问题
    
    # 处理行内公式中的多个$符号
    # 先找到所有可能的行内公式
    def fix_inline_formula(match):
        # 匹配内容中可能有多余的$符号
        formula_content = match.group(1)
        # 移除公式内容两端的$符号
        formula_content = formula_content.strip('$')
        # 返回修复后的公式
        return f'${formula_content}$'
    
    # 使用正则表达式找到所有可能的行内公式模式
    # 处理 $...$ 格式的行内公式
    content = re.sub(r'\$([^$]*?)\$', fix_inline_formula, content)
    
    # 处理块级公式中的多个$符号
    def fix_block_formula(match):
        formula_content = match.group(1)
        # 移除公式内容两端的$符号和空白
        formula_content = formula_content.strip('$\n ')
        # 返回修复后的块级公式
        return f'\n$$\n{formula_content}\n$$\n'
    
    # 处理 $$...$$ 格式的块级公式
    content = re.sub(r'\$\$\s*(.*?)\s*\$\$', fix_block_formula, content, flags=re.DOTALL)
    
    # 处理连续多个$符号的特殊情况
    # 例如：$$$...$$$ 或 $$$$...$$$$
    content = re.sub(r'\$\$\$+\s*(.*?)\s*\$\$\$+', '\\n$$\\n\1\\n$$\\n', content, flags=re.DOTALL)
    
    # 修复单个$符号后面紧跟着另一个$符号的情况
    content = re.sub(r'\$\$\$', '$$', content)
    
    # 修复行内公式中不必要的空白
    content = re.sub(r'\$\s*(.*?)\s*\$', '\$\1\$', content)
    
    # 修复块级公式中的额外空白
    content = re.sub(r'\$\$\s*\n\s*(.*?)\s*\n\s*\$\$', '\\n$$\\n\1\\n$$\\n', content, flags=re.DOTALL)
    
    return content

def main():
    root_dir = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\00-解决传统物理问题论文"
    
    # 排除验证报告文件本身
    exclude_files = ['formula_conversion_report.md', 'final_verification_report.md']
    
    # 统计信息
    stats = {
        "total_files": 0,
        "fixed_files": 0,
        "issues_fixed": 0
    }
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md') and file not in exclude_files:
                file_path = os.path.join(root, file)
                stats["total_files"] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查是否需要修复
                    has_issues = False
                    if re.search(r'\$\$\$', content) or re.search(r'\$[^$]*\$\$', content):
                        has_issues = True
                    
                    # 修复公式格式
                    fixed_content = fix_formula_format(content)
                    
                    # 检查是否有修改
                    if content != fixed_content:
                        # 写回文件
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)
                        stats["fixed_files"] += 1
                        stats["issues_fixed"] += 1
                        print(f"已修复: {file_path}")
                    
                except Exception as e:
                    print(f"处理文件出错 {file_path}: {str(e)}")
    
    print("\n公式格式修复完成!")
    print(f"总文件数: {stats['total_files']}")
    print(f"修复的文件数: {stats['fixed_files']}")
    print(f"修复的问题数: {stats['issues_fixed']}")

if __name__ == "__main__":
    main()
