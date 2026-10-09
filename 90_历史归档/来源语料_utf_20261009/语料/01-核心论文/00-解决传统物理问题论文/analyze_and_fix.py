#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的论文格式问题分析工具
用于确定具体的格式问题并生成修复方案
"""

import os
import re
from typing import List, Dict, Set

def analyze_file(file_path: str) -> Dict:
    """
    分析单个文件的格式问题
    """
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分析具体的格式问题
        # 1. 检查公式分隔符之间的空格问题
        if re.search(r'\$\s+\$', content):
            issues.append({
                "type": "公式空格问题",
                "description": "行内公式分隔符之间有多余空格",
                "examples": re.findall(r'\$\s+\$', content)
            })
        
        if re.search(r'\$\$\s+\$\$', content):
            issues.append({
                "type": "公式空格问题",
                "description": "块级公式分隔符之间有多余空格",
                "examples": re.findall(r'\$\$\s+\$\$', content)
            })
        
        # 2. 检查未闭合的公式
        open_inline = content.count('$') % 2 != 0
        open_block = content.count('$$') % 2 != 0
        
        if open_inline:
            issues.append({
                "type": "未闭合公式",
                "description": "行内公式分隔符不匹配",
                "count": content.count('$')
            })
        
        if open_block:
            issues.append({
                "type": "未闭合公式",
                "description": "块级公式分隔符不匹配",
                "count": content.count('$$')
            })
        
        # 3. 检查公式周围的空格问题
        # 检查公式前缺少空格
        if re.search(r'([a-zA-Z0-9])\$', content):
            issues.append({
                "type": "公式空格问题",
                "description": "公式前缺少空格",
                "examples": re.findall(r'([a-zA-Z0-9])\$', content)
            })
        
        # 检查公式后缺少空格
        if re.search(r'\$([a-zA-Z0-9])', content):
            issues.append({
                "type": "公式空格问题",
                "description": "公式后缺少空格",
                "examples": re.findall(r'\$([a-zA-Z0-9])', content)
            })
        
        # 4. 检查连续的公式分隔符
        if re.search(r'\$\$\$', content):
            issues.append({
                "type": "连续分隔符问题",
                "description": "存在连续的$符号",
                "examples": re.findall(r'\$\$\$+', content)
            })
        
        # 5. 检查数学表达式格式问题
        # 检查未转换的分数形式
        if re.search(r'([a-zA-Z0-9])/([a-zA-Z0-9])', content):
            issues.append({
                "type": "数学表达式格式",
                "description": "存在未转换的分数形式 (a/b)",
                "examples": re.findall(r'([a-zA-Z0-9])/([a-zA-Z0-9])', content)
            })
        
    except Exception as e:
        issues.append({
            "type": "文件错误",
            "description": f"读取文件时出错: {str(e)}"
        })
    
    return issues

def generate_detailed_report(root_dir: str):
    """
    生成详细的问题分析报告
    """
    report_path = os.path.join(root_dir, "详细问题分析报告.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 统一场论核心论文详细问题分析报告\n\n")
        
        total_files = 0
        files_with_issues = 0
        total_issues = 0
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    
                    issues = analyze_file(file_path)
                    if issues:
                        files_with_issues += 1
                        total_issues += len(issues)
                        
                        f.write(f"## 文件: {file_path}\n\n")
                        for i, issue in enumerate(issues):
                            f.write(f"### 问题 {i+1}\n")
                            f.write(f"- **类型**: {issue['type']}\n")
                            f.write(f"- **描述**: {issue['description']}\n")
                            if 'examples' in issue:
                                f.write(f"- **示例**: {issue['examples'][:5]}\n")
                            f.write("\n")
        
        f.write("## 分析总结\n\n")
        f.write(f"- **总文件数**: {total_files}\n")
        f.write(f"- **有问题的文件数**: {files_with_issues}\n")
        f.write(f"- **总问题数**: {total_issues}\n\n")

def batch_fix_issues(root_dir: str):
    """
    批量修复常见的格式问题
    """
    fixed_files = 0
    fixed_issues = 0
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # 修复公式空格问题
                    # 移除公式分隔符之间的多余空格
                    content = re.sub(r'\$\s+\$', r'$$', content)
                    content = re.sub(r'\$\$\s+\$\$', r'$$', content)
                    
                    # 修复公式前后的空格
                    # 在公式前添加空格
                    content = re.sub(r'([a-zA-Z0-9])\$', r'\1 $', content)
                    # 在公式后添加空格
                    content = re.sub(r'\$([a-zA-Z0-9])', r'$ \1', content)
                    
                    # 修复连续的$符号
                    content = re.sub(r'\$\$\$+', r'$$', content)
                    
                    # 保存修复后的内容
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        fixed_files += 1
                        fixed_issues += 1
                        
                except Exception as e:
                    print(f"修复文件时出错 {file_path}: {e}")
    
    return fixed_files, fixed_issues

if __name__ == "__main__":
    root_dir = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\00-解决传统物理问题论文"
    
    print("开始生成详细问题分析报告...")
    generate_detailed_report(root_dir)
    print("详细问题分析报告已生成")
    
    print("\n开始批量修复常见格式问题...")
    fixed_files, fixed_issues = batch_fix_issues(root_dir)
    print(f"批量修复完成!")
    print(f"修复的文件数: {fixed_files}")
    print(f"修复的问题数: {fixed_issues}")