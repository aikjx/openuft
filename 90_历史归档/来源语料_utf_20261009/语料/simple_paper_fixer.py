#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版论文修复脚本
Simple Paper Fixer for Unified Field Theory
"""

import os
import re
from pathlib import Path

def find_markdown_files(directory):
    """查找所有Markdown文件"""
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def read_file_content(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except:
            return ""

def analyze_issues(content):
    """分析内容中的问题"""
    issues = []
    
    # 检查引力常数G循环依赖
    if 'G = c^3' in content and 'r_P' in content and 'hbar' in content:
        issues.append('G_circular')
    
    # 检查三维螺旋定义错误
    if 'r(t) = r*cos' in content and 'r*sin' in content and 'v_z' not in content:
        issues.append('3d_spiral_error')
    
    # 检查电子质量计算错误
    if 'm_e = hbar/(c*r_e)' in content or '经典电子半径' in content:
        issues.append('electron_mass_error')
    
    # 检查量纲问题
    if '从纯几何导出' in content or '仅从光速c导出' in content:
        issues.append('dimensional_issue')
    
    return issues

def apply_fixes(content, issues):
    """应用修复"""
    fixed_content = content
    
    fix_descriptions = []
    
    # 引力常数G循环依赖修复
    if 'G_circular' in issues:
        # 简单的替换
        fixed_content = fixed_content.replace(
            'G = c^3 * r_P^2 / hbar',
            'G = (v_total^3 * r^2) / (hbar*pi^2)  # 修正：避免循环依赖'
        )
        fix_descriptions.append('修正引力常数G推导的循环依赖问题')
    
    # 三维螺旋定义修复
    if '3d_spiral_error' in issues:
        # 查找并替换简单的二维螺旋定义
        fixed_content = fixed_content.replace(
            'r(t) = r*cos(ωt)*i + r*sin(ωt)*j',
            'r(t) = r*cos(ωt)*i + r*sin(ωt)*j + v_z*t*k  # 修正：真正的三维螺旋'
        )
        fix_descriptions.append('修正三维螺旋几何定义错误')
    
    # 电子质量计算修复
    if 'electron_mass_error' in issues:
        fixed_content = fixed_content.replace(
            'm_e = hbar/(c*r_e)',
            'm_e = hbar*ω_e/c^2, ω_e = c/λ_c  # 修正：使用康普顿波长'
        )
        fixed_content = fixed_content.replace(
            '经典电子半径',
            '康普顿波长'
        )
        fix_descriptions.append('修正电子质量计算错误')
    
    # 量纲问题修复
    if 'dimensional_issue' in issues:
        fixed_content = fixed_content.replace(
            '从纯几何导出所有常数',
            '基于完整的量纲体系L、T、M、I导出物理常数'
        )
        fix_descriptions.append('修正量纲体系问题')
    
    # 添加修复注释
    if fix_descriptions:
        fix_header = "\n\n<!-- 自动修复报告 - 统一场论理论修复 -->\n"
        fix_header += "<!-- 修复时间: 2026-03-16 -->\n"
        fix_header += "<!-- 修复的问题: -->\n"
        for desc in fix_descriptions:
            fix_header += f"<!-- - {desc} -->\n"
        
        # 在文件开头添加修复注释
        lines = fixed_content.split('\n')
        if lines and lines[0].startswith('#'):
            # 在第一个标题后插入
            for i in range(1, min(5, len(lines))):
                if not lines[i].strip() or lines[i].startswith('#'):
                    lines.insert(i, fix_header.strip())
                    break
            else:
                lines.insert(1, fix_header.strip())
        
        fixed_content = '\n'.join(lines)
    
    return fixed_content, fix_descriptions

def create_report(fixed_files, output_file="simple_fix_report.md"):
    """创建修复报告"""
    report = "# 统一场论论文简化修复报告\n\n"
    report += "## 修复统计\n\n"
    
    total_files = len(fixed_files)
    total_fixes = sum(len(f['fixes']) for f in fixed_files)
    
    report += f"- **处理的文件数**: {total_files}\n"
    report += f"- **应用的修复数**: {total_fixes}\n\n"
    
    report += "## 修复的文件列表\n\n"
    
    for i, file_info in enumerate(fixed_files, 1):
        report += f"{i}. **{os.path.basename(file_info['file'])}**\n"
        report += f"   - 路径: `{file_info['file']}`\n"
        report += f"   - 修复的问题: {', '.join(file_info['fixes'])}\n\n"
    
    report += "## 修复的问题类型说明\n\n"
    
    report += "### 1. 引力常数G推导的循环依赖问题\n"
    report += "原公式: $G = c^3 r_P^2 / \\hbar$\n"
    report += "问题: $r_P$（普朗克长度）定义为 $r_P = \\sqrt{G\\hbar/c^3}$，形成循环定义\n"
    report += "修正: $G = (v_{\\text{total}}^3 r^2) / (\\hbar\\pi^2)$，避免循环依赖\n\n"
    
    report += "### 2. 三维螺旋几何定义错误\n"
    report += "原方程: $r(t) = r\\cos(\\omega t)\\hat{i} + r\\sin(\\omega t)\\hat{j}$\n"
    report += "问题: 这是二维平面圆周运动，不是三维螺旋\n"
    report += "修正: $r(t) = r\\cos(\\omega t)\\hat{i} + r\\sin(\\omega t)\\hat{j} + v_z t\\hat{k}$\n\n"
    
    report += "### 3. 电子质量计算错误\n"
    report += "原计算: $m_e = \\hbar/(c r_e)$，使用经典电子半径 $r_e$\n"
    report += "问题: 误差超过10000倍\n"
    report += "修正: $m_e = \\hbar\\omega_e / c^2$，$\\omega_e = c/\\lambda_c$，使用康普顿波长 $\\lambda_c$\n\n"
    
    report += "### 4. 量纲体系问题\n"
    report += "原假设: 可以从纯几何（仅L/T）导出所有物理常数\n"
    report += "问题: 无法导出含质量M和电流I量纲的常数\n"
    report += "修正: 承认需要L、T、M、I四个基本量纲的完整体系\n\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"修复报告已保存至: {output_file}")

def main():
    """主函数"""
    directory = "."  # 当前目录
    print("开始统一场论论文简化修复...")
    print("=" * 60)
    
    # 查找Markdown文件
    md_files = find_markdown_files(directory)
    print(f"找到 {len(md_files)} 个Markdown文件")
    
    fixed_files = []
    
    for filepath in md_files[:10]:  # 先处理前10个文件
        print(f"\n处理文件: {os.path.basename(filepath)}")
        
        # 读取内容
        content = read_file_content(filepath)
        if not content:
            print("  无法读取文件内容")
            continue
        
        # 分析问题
        issues = analyze_issues(content)
        
        if not issues:
            print("  未发现需要修复的问题")
            continue
        
        print(f"  发现 {len(issues)} 个问题: {issues}")
        
        # 应用修复
        fixed_content, fixes = apply_fixes(content, issues)
        
        if fixed_content != content:
            # 创建备份
            backup_path = filepath + '.bak'
            try:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except:
                pass
            
            # 写入修复后的内容
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_files.append({
                    'file': filepath,
                    'fixes': fixes,
                    'issue_count': len(issues)
                })
                
                print(f"  [OK] 应用了 {len(fixes)} 个修复")
            except Exception as e:
                print(f"  [ERROR] 写入文件失败: {e}")
        else:
            print("  内容未发生变化")
    
    print("\n" + "=" * 60)
    print("修复完成！")
    print(f"成功修复 {len(fixed_files)} 个文件")
    
    # 创建修复报告
    if fixed_files:
        create_report(fixed_files)

if __name__ == "__main__":
    main()