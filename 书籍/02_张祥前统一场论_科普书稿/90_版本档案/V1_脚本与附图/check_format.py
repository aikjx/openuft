#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 检查标题格式
def check_title_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 检查章标题格式：# 第X章：XXXXX
    chapter_pattern = r'^# 第(\d+)章：(.+)$'
    chapter_matches = re.findall(chapter_pattern, content, re.MULTILINE)
    if not chapter_matches:
        issues.append("没有找到符合格式的章标题：# 第X章：XXXXX")
    
    # 检查节标题格式：## X.X 节标题
    section_pattern = r'^## (\d+)\.(\d+) (.+)$'
    section_matches = re.findall(section_pattern, content, re.MULTILINE)
    for match in section_matches:
        chapter_num, section_num, title = match
        # 检查节编号是否与章编号一致
        if chapter_matches:
            expected_chapter = chapter_matches[0][0]
            if chapter_num != expected_chapter:
                issues.append(f"节编号 {chapter_num}.{section_num} 与章编号 {expected_chapter} 不一致")
    
    return issues

# 检查术语使用
def check_terminology(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 术语统一检查
    terminology_map = {
        '空间几何点': '空间单元',
        '时空统一性': '时空同一化',
        '几何描述': '几何化',
        '空间流动': '空间运动',
        '垂直原理': '空间单元运动规律'
    }
    
    for old_term, new_term in terminology_map.items():
        if old_term in content:
            issues.append(f"发现不统一术语：'{old_term}'，应使用 '{new_term}'")
    
    return issues

# 主函数
def main():
    md_files = [f for f in os.listdir('.') if f.endswith('.md')]
    total_issues = 0
    
    for file in md_files:
        print(f"\n检查文件：{file}")
        
        # 检查标题格式
        title_issues = check_title_format(file)
        if title_issues:
            print("标题格式问题：")
            for issue in title_issues:
                print(f"  - {issue}")
                total_issues += 1
        else:
            print("标题格式检查通过")
        
        # 检查术语使用
        term_issues = check_terminology(file)
        if term_issues:
            print("术语使用问题：")
            for issue in term_issues:
                print(f"  - {issue}")
                total_issues += 1
        else:
            print("术语使用检查通过")
    
    print(f"\n总问题数：{total_issues}")
    if total_issues == 0:
        print("所有检查通过！")
    else:
        print("发现问题，请修复后再检查。")

if __name__ == "__main__":
    main()