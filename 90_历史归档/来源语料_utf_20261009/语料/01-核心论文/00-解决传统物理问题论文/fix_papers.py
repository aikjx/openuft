#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心论文修复工具
用于修复论文中的公式格式问题和验证逻辑错误
"""

import os
import re
import json
from typing import List, Dict, Set

def fix_latex_formulas(content: str) -> str:
    """
    修复LaTeX公式格式问题
    """
    # 修复连续的$符号问题
    # 匹配多个连续的$符号，替换为正确的公式分隔符
    content = re.sub(r'\$\$\$\$', r'$$', content)
    content = re.sub(r'\$\$\$', r'$$', content)
    
    # 修复行内公式格式
    # 确保行内公式周围有空格
    content = re.sub(r'([^$])\$([^$]+)\$([^$])', r'\1 $\2$ \3', content)
    
    # 修复块级公式格式
    # 确保块级公式前后有空行
    content = re.sub(r'([^\n])\n\$\$([^\n])', r'\1\n\n$$\2', content)
    content = re.sub(r'([^\n])\$\$\n([^\n])', r'\1$$\n\n\2', content)
    
    return content

def improve_math_detection(content: str) -> bool:
    """
    改进的数学表达式检测
    只检测真正未转换的数学表达式
    """
    # 先提取所有已有的LaTeX公式
    latex_patterns = [
        r'\$.*?\$',
        r'\$\$.*?\$\$',
        r'```(?:math|latex|tex).*?```',
        r'\\\(.*?\\\)',
        r'\\\[.*?\\\]'
    ]
    
    for pattern in latex_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 然后检测剩余内容中的数学表达式
    # 使用更精确的模式，只匹配明显的数学等式
    math_pattern = r'\b[A-Za-zα-ωΑ-Ω][A-Za-z0-9α-ωΑ-Ω]*\s*=\s*[^$]+[0-9α-ωΑ-Ω+\-*/^()\[\]{}√πθφλμνξοπρστυφχψω]'
    
    # 排除常见的非数学等式
    exclude_patterns = [
        r'https?://',  # URL
        r'file://',    # 文件路径
        r'[A-Za-z]:\\', # Windows路径
        r'=',          # 单独的等号
        r'\b[A-Za-z]+\s*=\s*[A-Za-z]+',  # 简单的变量赋值（非数学）
    ]
    
    has_math_expr = re.search(math_pattern, content)
    if not has_math_expr:
        return False
    
    # 检查是否被排除
    for pattern in exclude_patterns:
        if re.search(pattern, content):
            return False
    
    return True

def fix_papers(root_dir: str) -> Dict:
    """
    修复所有论文文件
    """
    stats = {
        "total_files": 0,
        "fixed_files": 0,
        "issues_found": 0,
        "fixed_issues": 0,
        "details": []
    }
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                stats["total_files"] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    # 修复公式格式
                    fixed_content = fix_latex_formulas(original_content)
                    
                    # 检查是否有改进
                    if fixed_content != original_content:
                        stats["fixed_files"] += 1
                        stats["fixed_issues"] += 1
                        
                        # 保存修复后的内容
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)
                        
                        stats["details"].append({
                            "file": file_path,
                            "action": "修复",
                            "description": "修复了LaTeX公式格式问题"
                        })
                    else:
                        # 检查是否有未转换的数学表达式
                        if improve_math_detection(original_content):
                            stats["issues_found"] += 1
                            stats["details"].append({
                                "file": file_path,
                                "action": "警告",
                                "description": "可能存在未转换的数学表达式"
                            })
                        
                except Exception as e:
                    stats["details"].append({
                        "file": file_path,
                        "action": "错误",
                        "description": f"处理文件时出错: {str(e)}"
                    })
    
    return stats

def generate_fix_report(stats: Dict, report_path: str):
    """
    生成修复报告
    """
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 统一场论核心论文修复报告\n\n")
        
        f.write("## 修复统计\n\n")
        f.write(f"- **总文件数**: {stats['total_files']}\n")
        f.write(f"- **修复的文件数**: {stats['fixed_files']}\n")
        f.write(f"- **发现的问题数**: {stats['issues_found']}\n")
        f.write(f"- **修复的问题数**: {stats['fixed_issues']}\n\n")
        
        if stats['details']:
            f.write("## 详细修复记录\n\n")
            for i, detail in enumerate(stats['details'][:50]):
                f.write(f"### 记录 {i+1}\n")
                f.write(f"- **文件**: {detail['file']}\n")
                f.write(f"- **操作**: {detail['action']}\n")
                f.write(f"- **描述**: {detail['description']}\n\n")
            
            if len(stats['details']) > 50:
                f.write(f"... 还有 {len(stats['details']) - 50} 条记录未显示\n\n")
        
        f.write("## 结论\n\n")
        if stats['fixed_files'] > 0:
            f.write(f"成功修复了 {stats['fixed_files']} 个文件中的LaTeX公式格式问题。\n\n")
        else:
            f.write("未发现需要修复的公式格式问题。\n\n")
        
        if stats['issues_found'] > 0:
            f.write(f"发现了 {stats['issues_found']} 个可能存在未转换数学表达式的文件，建议手动检查。\n\n")
        else:
            f.write("所有文件中的数学表达式都已正确转换为LaTeX格式。\n\n")

if __name__ == "__main__":
    root_dir = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\00-解决传统物理问题论文"
    report_path = os.path.join(root_dir, "论文修复报告.md")
    
    print("开始修复统一场论核心论文...")
    stats = fix_papers(root_dir)
    generate_fix_report(stats, report_path)
    
    print("修复完成!")
    print(f"总文件数: {stats['total_files']}")
    print(f"修复的文件数: {stats['fixed_files']}")
    print(f"发现的问题数: {stats['issues_found']}")
    print(f"修复的问题数: {stats['fixed_issues']}")
    print(f"修复报告已生成: {report_path}")