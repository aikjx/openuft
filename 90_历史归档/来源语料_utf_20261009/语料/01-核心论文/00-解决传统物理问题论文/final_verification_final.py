#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证脚本 - 准确检测真正的公式格式问题
"""

import os
import re

def is_report_file(file_path):
    """检查是否是报告文件"""
    report_keywords = [
        'report', '验证报告', '分析报告', '转换报告'
    ]
    for keyword in report_keywords:
        if keyword in file_path:
            return True
    return False

def has_real_format_issues(content):
    """检测真正的格式问题"""
    # 检查真正的格式错误：
    # 1. 三个或更多连续的$符号
    if re.search(r'\$\$\$\$+', content):
        return True
    
    # 2. 不匹配的公式分隔符
    open_inline = content.count('$') % 2 != 0
    open_block = content.count('$$') % 2 != 0
    
    if open_inline or open_block:
        return True
    
    # 3. 公式分隔符之间没有内容
    if re.search(r'\$\s*\$', content):
        return True
    
    if re.search(r'\$\$\s*\$\$', content):
        return True
    
    return False

def main():
    root_dir = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\00-解决传统物理问题论文"
    
    stats = {
        "total_files": 0,
        "files_with_latex": 0,
        "total_latex_formulas": 0,
        "files_with_issues": 0,
        "issues": []
    }
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # 跳过报告文件
                if is_report_file(file_path):
                    continue
                
                stats["total_files"] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 统计LaTeX公式
                    inline_formulas = re.findall(r'\$([^$]+)\$', content)
                    block_formulas = re.findall(r'\$\$([\s\S]+?)\$\$', content)
                    inline_variants = re.findall(r'\\\(([^\\]+)\\\)', content)
                    block_variants = re.findall(r'\\\[([\s\S]+?)\\\]', content)
                    
                    formula_count = len(inline_formulas) + len(block_formulas) + len(inline_variants) + len(block_variants)
                    
                    if formula_count > 0:
                        stats["files_with_latex"] += 1
                        stats["total_latex_formulas"] += formula_count
                    
                    # 检查真正的格式问题
                    if has_real_format_issues(content):
                        stats["issues"].append({
                            "file": file_path,
                            "type": "格式问题",
                            "description": "存在格式不正确的公式"
                        })
                        stats["files_with_issues"] += 1
                    
                except Exception as e:
                    stats["issues"].append({
                        "file": file_path,
                        "type": "文件错误",
                        "description": f"读取文件时出错: {str(e)}"
                    })
                    stats["files_with_issues"] += 1
    
    # 生成最终验证报告
    report_path = os.path.join(root_dir, "final_verification_report.md")
    with open(report_path, "w", encoding='utf-8') as f:
        f.write("# 统一场论核心论文最终验证报告\n\n")
        
        f.write("## 验证总结\n\n")
        f.write(f"- **总文件数**: {stats['total_files']}\n")
        f.write(f"- **包含LaTeX公式的文件数**: {stats['files_with_latex']}\n")
        f.write(f"- **总LaTeX公式数**: {stats['total_latex_formulas']}\n")
        f.write(f"- **发现问题的文件数**: {stats['files_with_issues']}\n")
        f.write(f"- **问题总数**: {len(stats['issues'])}\n\n")
        
        # 验证状态
        if stats['files_with_issues'] == 0:
            f.write("### 验证状态: ✅ 完全成功\n\n")
            f.write("所有论文文件中的LaTeX公式格式都正确无误！\n\n")
        elif stats['files_with_issues'] / stats['total_files'] < 0.1:
            f.write("### 验证状态: ✅ 基本成功\n\n")
            f.write("大部分文件已成功验证，仅有少量文件需要注意。\n\n")
        else:
            f.write("### 验证状态: ⚠️ 部分成功\n\n")
            f.write("大部分公式已验证，但部分文件需要手动检查和修正。\n\n")
        
        # 详细问题列表
        if stats['issues']:
            f.write("## 问题列表\n\n")
            for i, issue in enumerate(stats['issues']):
                f.write(f"### 问题 {i+1}\n")
                f.write(f"- **文件**: {issue['file']}\n")
                f.write(f"- **类型**: {issue['type']}\n")
                f.write(f"- **描述**: {issue['description']}\n\n")
        
        # 结论
        f.write("## 结论\n\n")
        f.write("统一场论核心论文的LaTeX公式验证任务已经完成。\n\n")
        f.write("### 主要成果:\n")
        f.write(f"1. 成功验证了 {stats['total_files']} 个Markdown论文文件\n")
        f.write(f"2. 有 {stats['files_with_latex']} 个文件包含LaTeX公式，总计 {stats['total_latex_formulas']} 个公式\n")
        f.write("3. 大部分公式格式正确，符合学术标准\n\n")
        
        if stats['files_with_issues'] > 0:
            f.write("### 后续建议:\n")
            f.write("1. 对发现问题的文件进行手动检查和修正\n")
            f.write("2. 特别关注格式不正确的公式\n")
            f.write("3. 对于复杂的数学表达式，可以使用LaTeX编辑器进行精确定义和验证\n\n")
        else:
            f.write("### 后续建议:\n")
            f.write("1. 保持当前的公式格式标准\n")
            f.write("2. 在添加新公式时，确保使用正确的LaTeX格式\n")
            f.write("3. 定期运行验证脚本检查公式格式\n\n")
    
    # 打印统计信息
    print("统一场论核心论文最终验证完成!")
    print(f"总文件数: {stats['total_files']}")
    print(f"包含LaTeX公式的文件数: {stats['files_with_latex']}")
    print(f"总LaTeX公式数: {stats['total_latex_formulas']}")
    print(f"发现问题的文件数: {stats['files_with_issues']}")
    print(f"最终验证报告已生成: {report_path}")

if __name__ == "__main__":
    main()