#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论代码行数统计脚本
Unified Field Theory Code Line Counter

该脚本用于统计统一场论代码库的总代码行数，验证是否达到100万行的目标。
This script is used to count the total lines of code in the unified field theory codebase,
verifying if it meets the 1,000,000 lines target.
"""

import os
import re
import time
import json

def count_lines_in_file(file_path):
    """统计单个文件的代码行数"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # 过滤空行和注释
        code_lines = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//'):
                code_lines += 1
        
        return code_lines
    except Exception as e:
        print(f"统计文件 {file_path} 时出错: {str(e)}")
        return 0

def count_lines_in_directory(directory):
    """递归统计目录中的代码行数"""
    total_lines = 0
    file_count = 0
    extension_stats = {}
    
    for root, dirs, files in os.walk(directory):
        # 跳过某些目录
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'env', '.history']]
        
        for file in files:
            # 只统计代码文件
            if file.endswith(('.py', '.pyw', '.py3', '.pyc')):
                file_path = os.path.join(root, file)
                lines = count_lines_in_file(file_path)
                total_lines += lines
                file_count += 1
                
                # 按扩展名统计
                ext = os.path.splitext(file)[1]
                if ext not in extension_stats:
                    extension_stats[ext] = 0
                extension_stats[ext] += lines
    
    return total_lines, file_count, extension_stats

def main():
    """主函数"""
    print("=== 统一场论代码行数统计 ===")
    print("开始时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # 统计整个utf目录
    utf_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"统计目录: {utf_directory}")
    print()
    
    # 统计核心算法目录
    core_algorithm_dir = os.path.join(utf_directory, "核心算法")
    print("1. 统计核心算法目录...")
    core_lines, core_files, core_extensions = count_lines_in_directory(core_algorithm_dir)
    print(f"核心算法代码行数: {core_lines:,}")
    print(f"核心算法文件数: {core_files}")
    print(f"核心算法扩展名统计: {core_extensions}")
    print()
    
    # 统计10-统一场论核心公式目录
    core_formulas_dir = os.path.join(utf_directory, "10-统一场论核心公式")
    print("2. 统计统一场论核心公式目录...")
    formulas_lines, formulas_files, formulas_extensions = count_lines_in_directory(core_formulas_dir)
    print(f"核心公式代码行数: {formulas_lines:,}")
    print(f"核心公式文件数: {formulas_files}")
    print(f"核心公式扩展名统计: {formulas_extensions}")
    print()
    
    # 统计其他目录
    print("3. 统计其他目录...")
    other_lines = 0
    other_files = 0
    
    # 遍历所有子目录
    for item in os.listdir(utf_directory):
        item_path = os.path.join(utf_directory, item)
        if os.path.isdir(item_path) and item not in ["核心算法", "10-统一场论核心公式", ".git", "__pycache__", "venv", "env", ".history"]:
            lines, files, _ = count_lines_in_directory(item_path)
            other_lines += lines
            other_files += files
            print(f"  {item}: {lines:,} 行, {files} 文件")
    
    print(f"其他目录代码行数: {other_lines:,}")
    print(f"其他目录文件数: {other_files}")
    print()
    
    # 总计
    total_lines = core_lines + formulas_lines + other_lines
    total_files = core_files + formulas_files + other_files
    
    print("=== 统计结果 ===")
    print(f"总代码行数: {total_lines:,}")
    print(f"总文件数: {total_files}")
    print(f"平均每文件代码行数: {total_lines / total_files:.2f}")
    print()
    
    # 验证目标
    target_lines = 1000000
    if total_lines >= target_lines:
        print(f"✓ 代码行数达到目标: {total_lines:,} >= {target_lines:,}")
        print(f"超出目标: {total_lines - target_lines:,} 行")
    else:
        print(f"✗ 代码行数未达到目标: {total_lines:,} < {target_lines:,}")
        print(f"还差: {target_lines - total_lines:,} 行")
    
    # 保存统计结果
    stats = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_lines": total_lines,
        "total_files": total_files,
        "core_algorithm": {
            "lines": core_lines,
            "files": core_files,
            "extensions": core_extensions
        },
        "core_formulas": {
            "lines": formulas_lines,
            "files": formulas_files,
            "extensions": formulas_extensions
        },
        "other": {
            "lines": other_lines,
            "files": other_files
        },
        "target": target_lines,
        "achieved": total_lines >= target_lines
    }
    
    output_file = f"code_line_count_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n统计结果已保存至: {output_file}")
    print("结束时间:", time.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
