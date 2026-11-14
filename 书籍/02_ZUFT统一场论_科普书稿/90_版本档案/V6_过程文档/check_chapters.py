#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查V6版本章节文件的完整性
"""

import os
import re

def check_v6_chapters():
    """检查V6版本章节文件的完整性"""
    
    # 定义V6版本目录
    v6_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 从目录.md文件中提取所有章节链接
    directory_path = os.path.join(v6_dir, "目录.md")
    if not os.path.exists(directory_path):
        print("目录文件不存在！")
        return False
    
    with open(directory_path, 'r', encoding='utf-8') as f:
        directory_content = f.read()
    
    # 提取目录中的章节文件
    chapter_links = re.findall(r'\d+\. \[.*?\]\((.*?\.md)\)', directory_content)
    expected_chapters = [os.path.basename(link) for link in chapter_links]
    
    print(f"目录中列出的章节数量: {len(expected_chapters)}")
    print("\n目录中列出的章节：")
    for chapter in expected_chapters:
        print(f"  {chapter}")
    
    # 获取实际存在的章节文件
    actual_chapters = []
    for file in os.listdir(v6_dir):
        if re.match(r'^(第一章|第二章|第三章|第四章|第五章|第六章|第七章|第八章|第九章|第十章|第十一章|第十二章|第十三章|第十四章|第十五章|第十六章|第十七章|第十八章|第十九章|第二十章|第二十一章|第二十二章|第二十三章|第二十四章|第二十五章|第二十六章)：.*\.md$', file):
            actual_chapters.append(file)
    
    print(f"\n实际存在的章节数量: {len(actual_chapters)}")
    print("\n实际存在的章节：")
    for chapter in actual_chapters:
        print(f"  {chapter}")
    
    # 检查缺失的章节
    missing_chapters = [chapter for chapter in expected_chapters if chapter not in actual_chapters]
    if missing_chapters:
        print(f"\n❌ 缺失的章节文件: {len(missing_chapters)}个")
        for chapter in missing_chapters:
            print(f"  {chapter}")
    else:
        print("\n✅ 所有目录中列出的章节文件都存在！")
    
    # 检查额外的章节（不在目录中的章节）
    extra_chapters = [chapter for chapter in actual_chapters if chapter not in expected_chapters]
    if extra_chapters:
        print(f"\n⚠️  额外的章节文件（不在目录中）: {len(extra_chapters)}个")
        for chapter in extra_chapters:
            print(f"  {chapter}")
    else:
        print("\n✅ 没有额外的章节文件！")
    
    return len(missing_chapters) == 0 and len(extra_chapters) == 0

if __name__ == "__main__":
    check_v6_chapters()
