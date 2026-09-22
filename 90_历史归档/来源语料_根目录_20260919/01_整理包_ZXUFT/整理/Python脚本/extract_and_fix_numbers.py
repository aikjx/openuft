#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def extract_numbers(file_path):
    """
    从文件中提取各种序号，包括章节号、方程号、图片编号等
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取章节号（如2.1, 3.2.1等）
    section_pattern = r'^##\s+(\d+(?:\.\d+)*)\s+'
    sections = re.findall(section_pattern, content, re.MULTILINE)
    
    # 提取方程号（如(2-1), (3-2)等）
    equation_pattern = r'\\tag\{([\d-]+)\}'
    equations = re.findall(equation_pattern, content)
    
    # 提取图片编号（如图2-1, 图3-2等）
    figure_pattern = r'图(\d+-\d+)：'
    figures = re.findall(figure_pattern, content)
    
    # 提取列表项（如1. 2. 3.等）
    list_pattern = r'^\s*(\d+)\.\s+'
    lists = re.findall(list_pattern, content, re.MULTILINE)
    
    return {
        'sections': sections,
        'equations': equations,
        'figures': figures,
        'lists': lists
    }

def analyze_sequences(numbers, pattern_name):
    """
    分析序号序列的连续性和格式
    """
    if not numbers:
        return []
    
    issues = []
    
    # 按类型分组分析
    if pattern_name == 'sections':
        # 章节号分组（如2.1, 2.2属于同一章）
        chapters = {}
        for section in numbers:
            parts = section.split('.')
            chapter = parts[0]
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append(section)
        
        # 分析每章的小节
        for chapter, sections in chapters.items():
            # 按层级排序
            sections.sort(key=lambda x: list(map(int, x.split('.'))))
            
            # 检查连续性
            for i in range(len(sections) - 1):
                curr_parts = list(map(int, sections[i].split('.')))
                next_parts = list(map(int, sections[i+1].split('.')))
                
                # 检查同一层级的连续性
                if len(curr_parts) == len(next_parts):
                    if next_parts[-1] != curr_parts[-1] + 1:
                        issues.append(f"章节号不连续：{sections[i]} 后面应为 {'.'.join(map(str, curr_parts[:-1] + [curr_parts[-1]+1]))}，但实际是 {sections[i+1]}")
    
    elif pattern_name in ['equations', 'figures']:
        # 按章节分组
        chapters = {}
        for num in numbers:
            if '-' not in num:
                issues.append(f"{pattern_name} 格式错误：{num}，应为 '章节-序号' 格式")
                continue
            
            chapter, seq = num.split('-')
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append(int(seq))
        
        # 分析每章的序号
        for chapter, seqs in chapters.items():
            seqs.sort()
            
            # 检查连续性
            for i in range(len(seqs) - 1):
                if seqs[i+1] != seqs[i] + 1:
                    issues.append(f"{pattern_name} 不连续：第 {chapter} 章的 {seqs[i]} 后面应为 {seqs[i]+1}，但实际是 {seqs[i+1]}")
    
    elif pattern_name == 'lists':
        # 列表项可能跨多个区域，这里只检查相邻的数字
        prev = None
        for num in numbers:
            curr = int(num)
            if prev is not None:
                if curr != prev + 1:
                    issues.append(f"列表项不连续：{prev} 后面应为 {prev+1}，但实际是 {curr}")
            prev = curr
    
    return issues

def fix_sequences(content):
    """
    修复文件中的序号问题
    """
    new_content = content
    
    # 1. 修复方程号
    print("修复方程号...")
    equation_pattern = r'(\\tag\{)([\d-]+)(\})'
    chapters = {}
    
    def replace_equation(match):
        prefix, num, suffix = match.groups()
        if '-' not in num:
            return match.group(0)  # 保持不变
        
        chapter, seq = num.split('-')
        if chapter not in chapters:
            chapters[chapter] = 0
        chapters[chapter] += 1
        return f"{prefix}{chapter}-{chapters[chapter]}{suffix}"
    
    new_content = re.sub(equation_pattern, replace_equation, new_content)
    
    # 2. 修复图片编号
    print("修复图片编号...")
    figure_pattern = r'图(\d+-\d+)：'
    figure_chapters = {}
    
    def replace_figure(match):
        num = match.group(1)
        if '-' not in num:
            return match.group(0)  # 保持不变
        
        chapter, seq = num.split('-')
        if chapter not in figure_chapters:
            figure_chapters[chapter] = 0
        figure_chapters[chapter] += 1
        return f"图{chapter}-{figure_chapters[chapter]}："
    
    new_content = re.sub(figure_pattern, replace_figure, new_content)
    
    # 3. 修复列表项（简化处理，只修复连续列表）
    print("修复列表项...")
    # 这个修复比较复杂，因为列表可能跨多个区域，这里只做简单处理
    
    return new_content

def main():
    file_path = 'd:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\引力光速统一方程\\引力光速统一方程：从空间动力学原理到常数统一的理论推导与验证.md'
    
    print(f"分析文件：{file_path}")
    print("=" * 60)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件不存在！{file_path}")
        return
    
    # 提取序号
    try:
        numbers = extract_numbers(file_path)
        print(f"成功提取序号")
    except Exception as e:
        print(f"提取序号时出错：{e}")
        import traceback
        traceback.print_exc()
        return
    
    # 分析各类型序号
    all_issues = []
    for pattern_name, nums in numbers.items():
        print(f"\n{pattern_name} 总数：{len(nums)}")
        print(f"示例：{nums[:5] if nums else '无'}")
        
        issues = analyze_sequences(nums, pattern_name)
        all_issues.extend(issues)
        
        if issues:
            print(f"存在问题：")
            for issue in issues[:10]:  # 只显示前10个问题
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... 还有 {len(issues) - 10} 个问题")
        else:
            print(f"无问题")
    
    # 生成修复报告
    print("\n" + "=" * 60)
    if all_issues:
        print(f"共发现 {len(all_issues)} 个问题")
        
        # 读取文件内容进行修复
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复内容
        new_content = fix_sequences(content)
        
        # 保存修复后的文件
        fixed_file_path = file_path.replace('.md', '_fixed.md')
        with open(fixed_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"修复后的文件已保存至：{fixed_file_path}")
    else:
        print("未发现序号问题")
    
    print("=" * 60)
    print("分析完成")

if __name__ == '__main__':
    main()
