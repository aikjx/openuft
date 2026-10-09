#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终智能修复脚本 - 准确修复LaTeX公式格式问题
"""

import os
import re

def fix_formula_format(content):
    """
    修复内容中的LaTeX公式格式问题
    """
    # 1. 修复连续的公式分隔符
    content = re.sub(r'\$\$\$+', r'$$', content)
    
    # 2. 修复公式周围的空格问题
    # 确保公式前后有空格
    content = re.sub(r'([a-zA-Z0-9])\$', r'\1 $', content)
    content = re.sub(r'\$([a-zA-Z0-9])', r'$ \1', content)
    
    # 3. 修复公式分隔符之间的空格
    content = re.sub(r'\$\s+\$', r'$$', content)
    content = re.sub(r'\$\$\s+\$\$', r'$$', content)
    
    # 4. 修复未闭合的公式
    # 检查并修复行内公式
    open_inline = content.count('$') % 2 != 0
    if open_inline:
        # 找到最后一个未闭合的$并闭合它
        last_dollar = content.rfind('$')
        if last_dollar != -1:
            content = content[:last_dollar+1] + '$' + content[last_dollar+1:]
    
    # 检查并修复块级公式
    open_block = content.count('$$') % 2 != 0
    if open_block:
        # 找到最后一个未闭合的$$并闭合它
        last_double_dollar = content.rfind('$$')
        if last_double_dollar != -1:
            content = content[:last_double_dollar+2] + '$$' + content[last_double_dollar+2:]
    
    return content

def process_file(file_path):
    """
    处理单个文件，修复公式格式问题
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 修复公式格式
        fixed_content = fix_formula_format(original_content)
        
        # 保存修复后的内容
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"处理文件时出错 {file_path}: {e}")
        return False

def main():
    root_dir = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\00-解决传统物理问题论文"
    
    print("开始最终智能修复...")
    
    fixed_count = 0
    total_count = 0
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                # 跳过报告文件
                if 'report' in file.lower() or '验证' in file or '分析' in file:
                    continue
                
                file_path = os.path.join(root, file)
                total_count += 1
                
                if process_file(file_path):
                    fixed_count += 1
    
    print("最终智能修复完成!")
    print(f"处理文件数: {total_count}")
    print(f"修复文件数: {fixed_count}")

if __name__ == "__main__":
    main()