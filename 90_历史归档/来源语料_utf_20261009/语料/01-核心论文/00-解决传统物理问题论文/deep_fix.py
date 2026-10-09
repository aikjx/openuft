#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心论文深度修复工具
用于修复论文中的公式格式问题，特别是连续公式的分隔问题
"""

import os
import re
from typing import List, Dict

def fix_consecutive_formulas(content: str) -> str:
    """
    修复连续的公式分隔符问题
    """
    # 修复连续的行内公式
    # 匹配模式: $$公式$$公式$$
    content = re.sub(r'\$\$([^$]+)\$\$([^$]+)\$\$', r'$$\1$$\n\n$$\2$$', content)
    
    # 修复多个连续的块级公式
    content = re.sub(r'\$\$([^$]+)\$\$([^$]+)\$\$([^$]+)\$\$', r'$$\1$$\n\n$$\2$$\n\n$$\3$$', content)
    
    # 修复公式之间缺少换行的问题
    # 匹配模式: $$公式$$ 其他内容 $$公式$$
    content = re.sub(r'\$\$([^$]+)\$\$([^\n]+)\$\$([^$]+)\$\$', r'$$\1$$\n\n\2\n\n$$\3$$', content)
    
    # 修复更复杂的连续公式情况
    # 匹配模式: $$公式$$公式$$公式$$...
    pattern = r'\$\$([^$]+)\$\$'
    formulas = re.findall(pattern, content)
    
    if len(formulas) > 1:
        # 重建内容，确保每个公式之间有换行
        new_content = content
        for formula in formulas:
            # 替换每个公式为正确的格式
            old_str = f'$$公式$$'
            new_str = f'$$公式$$\n\n'
            new_content = new_content.replace(old_str, new_str)
    
    return content

def fix_formula_spacing(content: str) -> str:
    """
    修复公式周围的空格问题
    """
    # 修复公式前缺少空格的问题
    content = re.sub(r'([a-zA-Z0-9])\$', r'\1 $', content)
    
    # 修复公式后缺少空格的问题
    content = re.sub(r'\$([a-zA-Z0-9])', r'$ \1', content)
    
    # 修复公式分隔符之间的空格问题
    content = re.sub(r'\$\s+\$', r'$$', content)
    content = re.sub(r'\$\$\s+\$\$', r'$$', content)
    
    # 修复公式内部的多余空格
    content = re.sub(r'\$\s+([^$]+)\s+\$', r'$\1$', content)
    content = re.sub(r'\$\$\s+([^$]+)\s+\$\$', r'$$\1$$', content)
    
    return content

def fix_unclosed_formulas(content: str) -> str:
    """
    尝试修复未闭合的公式
    """
    # 检查并修复行内公式
    open_inline = content.count('$') % 2 != 0
    if open_inline:
        # 尝试找到最后一个未闭合的公式并闭合它
        content = content + '$'
    
    # 检查并修复块级公式
    open_block = content.count('$$') % 2 != 0
    if open_block:
        # 尝试找到最后一个未闭合的块级公式并闭合它
        content = content + '$$'
    
    return content

def process_file(file_path: str) -> bool:
    """
    处理单个文件，修复公式格式问题
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 应用修复
        content = original_content
        content = fix_consecutive_formulas(content)
        content = fix_formula_spacing(content)
        content = fix_unclosed_formulas(content)
        
        # 保存修复后的内容
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"处理文件时出错 {file_path}: {e}")
        return False

def batch_process(root_dir: str) -> Dict:
    """
    批量处理所有论文文件
    """
    stats = {
        "total_files": 0,
        "fixed_files": 0,
        "failed_files": 0
    }
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                stats["total_files"] += 1
                
                try:
                    fixed = process_file(file_path)
                    if fixed:
                        stats["fixed_files"] += 1
                except Exception as e:
                    stats["failed_files"] += 1
                    print(f"处理文件失败 {file_path}: {e}")
    
    return stats

if __name__ == "__main__":
    root_dir = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\00-解决传统物理问题论文"
    
    print("开始深度修复统一场论核心论文...")
    stats = batch_process(root_dir)
    
    print("深度修复完成!")
    print(f"总文件数: {stats['total_files']}")
    print(f"修复的文件数: {stats['fixed_files']}")
    print(f"失败的文件数: {stats['failed_files']}")