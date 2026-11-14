#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查书籍附录文件的完整性
"""

import os
import re

def check_appendices(version_dir, version_name):
    """检查指定版本的附录文件完整性"""
    print(f"\n=== 检查 {version_name} 版本附录文件 ===")
    
    # 从目录.md文件中提取所有附录链接
    directory_path = os.path.join(version_dir, "目录.md")
    if not os.path.exists(directory_path):
        print(f"  目录文件不存在！")
        return False
    
    with open(directory_path, 'r', encoding='utf-8') as f:
        directory_content = f.read()
    
    # 提取目录中的附录文件
    appendix_links = re.findall(r'\- \[.*?\]\((.*?\.md)\)', directory_content)
    expected_appendices = [os.path.basename(link) for link in appendix_links if "附录" in link or "附录" in os.path.basename(link)]
    
    print(f"  目录中列出的附录数量: {len(expected_appendices)}")
    if expected_appendices:
        print(f"  \n目录中列出的附录：")
        for appendix in expected_appendices:
            print(f"    {appendix}")
    
    # 获取实际存在的附录文件
    actual_appendices = []
    for file in os.listdir(version_dir):
        if re.match(r'^(附录|附录一|附录二|附录三|附录四|附录五|附录六|附录七|附录八|附录九|附录十|附录十一).*\.md$', file):
            actual_appendices.append(file)
    
    print(f"  \n实际存在的附录数量: {len(actual_appendices)}")
    if actual_appendices:
        print(f"  \n实际存在的附录：")
        for appendix in actual_appendices:
            print(f"    {appendix}")
    
    # 检查缺失的附录
    missing_appendices = [appendix for appendix in expected_appendices if appendix not in actual_appendices]
    if missing_appendices:
        print(f"  \n❌ 缺失的附录文件: {len(missing_appendices)}个")
        for appendix in missing_appendices:
            print(f"    {appendix}")
    else:
        print(f"  \n✅ 所有目录中列出的附录文件都存在！")
    
    # 检查额外的附录（不在目录中的附录）
    extra_appendices = [appendix for appendix in actual_appendices if appendix not in expected_appendices]
    if extra_appendices:
        print(f"  \n⚠️  额外的附录文件（不在目录中）: {len(extra_appendices)}个")
        for appendix in extra_appendices:
            print(f"    {appendix}")
    else:
        print(f"  \n✅ 没有额外的附录文件！")
    
    return len(missing_appendices) == 0 and len(extra_appendices) == 0

def main():
    """主函数"""
    
    # 定义书籍根目录
    book_root = "d:\\a10\\aikjx\\code\\my_lib\\utf\\12-书籍\\人人都能理解统一场论"
    
    # 检查V1版本
    v1_dir = os.path.join(book_root, "V1")
    check_appendices(v1_dir, "V1")
    
    # 检查V6版本
    v6_dir = os.path.join(book_root, "V6")
    check_appendices(v6_dir, "V6")
    
    print(f"\n=== 附录文件检查完成 ===")

if __name__ == "__main__":
    main()
