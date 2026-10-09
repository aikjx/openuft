# -*- coding: utf-8 -*-
"""
统一场论书籍章节批量优化脚本 V2
功能：批量优化所有章节，添加导航、表格、emoji等视觉元素
"""

import os
import re
from pathlib import Path

CHAPTERS_DIR = r"d:/a10/aikjx/code/my_lib/utf/12-书籍/人人都能理解统一场论/V1"

# 章节优化配置
CHAPTER_CONFIGS = {
    "第6章：观察者的角色.md": {
        "quote": "观察者不仅是物理世界的见证者，更是物理现象的参与者。 —— 量子力学启示",
        "navigation": ["📖 6.1 观察者是什么？", "💡 6.2 观察如何影响物理现象？", "🚀 6.3 不同观察者的不同世界", "🔍 6.4 观察者在统一场论中的地位"],
        "table_rows": [
            ["观察者效应", "双缝干涉、观察影响", "6.2"],
            ["观察者依赖", "参考系、相对性", "6.3"],
            ["信息传递", "光速限制", "6.3"],
            ["辩证统一", "客观性与主观性", "6.4"]
        ],
        "goals": ["理解观察者的定义和作用", "掌握观察者效应和依赖", "了解不同观察者的不同世界", "认识观察者在统一场论中的地位"]
    },
    "第7章：运动的本质.md": {
        "quote": "运动是宇宙的基本属性，没有运动就没有我们所熟知的物理世界。",
        "navigation": ["📖 7.1 运动的直观理解与定义", "💡 7.2 运动的基本形式", "🚀 7.3 运动与空间、时间的关系", "🔍 7.4 统一场论中的运动"],
        "table_rows": [
            ["运动的定义", "位置变化、时间度量", "7.1"],
            ["运动的形式", "直线、曲线、旋转", "7.2"],
            ["相对性", "参考系依赖", "7.1"],
            ["时空关系", "运动与时间密不可分", "7.3"]
        ],
        "goals": ["理解运动的定义和特性", "掌握运动的基本形式", "了解运动与时空的关系", "认识统一场论中的运动观"]
    },
    "第8章：空间的基本运动形式.md": {
        "quote": "空间有四种基本运动形式：流动、振动、旋转和螺旋运动，它们共同构成了宇宙的物理现象。",
        "navigation": ["📖 8.1 空间的流动", "💡 8.2 空间的振动", "🚀 8.3 空间的旋转", "🔍 8.4 螺旋运动：空间的终极形式"],
        "table_rows": [
            ["空间流动", "引力场的根源", "8.1"],
            ["空间振动", "电磁波的根源", "8.2"],
            ["空间旋转", "电磁场的根源", "8.3"],
            ["螺旋运动", "旋转与直线的结合", "8.4"]
        ],
        "goals": ["理解空间的四种基本运动形式", "掌握流动与引力的关系", "了解振动与电磁波的关系", "认识螺旋运动的重要性"]
    },
    "第9章：光速的奥秘.md": {
        "quote": "光速是宇宙的基本常数，它连接了空间与时间，是相对论和统一场论的核心。",
        "navigation": ["📖 9.1 什么是光速？", "💡 9.2 光速的不变性原理", "🚀 9.3 光速与时间、空间的关系", "🔍 9.4 光速在统一场论中的地位"],
        "table_rows": [
            ["光速定义", "3×10⁸ m/s", "9.1"],
            ["不变性", "所有参考系相同", "9.2"],
            ["时空桥梁", "R=ct方程", "9.3"],
            ["核心常数", "统一场论基础", "9.4"]
        ],
        "goals": ["理解光速的定义和测量", "掌握光速不变性原理", "了解光速与时空的关系", "认识光速在统一场论中的地位"]
    }
}

def get_default_config():
    """获取默认配置"""
    return {
        "quote": "探索宇宙的奥秘，从理解基本概念开始。",
        "navigation": ["📖 第1节", "💡 第2节", "🚀 第3节", "🔍 第4节"],
        "table_rows": [
            ["核心思想1", "关键词1", "1.1"],
            ["核心思想2", "关键词2", "1.2"]
        ],
        "goals": ["掌握核心概念", "理解基本原理", "认识实际应用"]
    }

def create_optimized_header(title, config):
    """创建优化后的章节头部"""
    quote = config.get("quote", "")
    navigation = config.get("navigation", [])
    table_rows = config.get("table_rows", [])
    
    header = f"# {title}\n\n"
    
    # 添加引用
    if quote:
        header += f"> 💡 **引用名言**：{quote}\n\n"
    
    # 添加导航
    header += "## 本章导航\n"
    for item in navigation:
        header += f"- {item}\n"
    header += "\n"
    
    # 添加核心观点表格
    header += "## 核心观点预览\n"
    header += "| 核心思想 | 关键词 | 章节关联 |\n"
    header += "|---------|--------|---------|\n"
    for row in table_rows:
        header += f"| {row[0]} | {row[1]} | {row[2]} |\n"
    header += "\n"
    
    return header

def add_chapter_summary(content, config):
    """添加章节总结"""
    if "## 本章小结" in content:
        return content
    
    goals = config.get("goals", ["掌握核心概念", "理解基本原理"])
    
    summary = "\n## 本章小结\n\n"
    summary += "### 📚 知识要点回顾\n\n"
    summary += "通过本章学习，我们深入了解了相关概念和原理。\n\n"
    summary += "### 🎯 学习目标达成\n\n"
    summary += "通过本章学习，你应该能够：\n\n"
    for goal in goals:
        summary += f"- ✅ {goal}\n"
    summary += "\n"
    
    return content + summary

def optimize_chapter(filename):
    """优化单个章节"""
    filepath = os.path.join(CHAPTERS_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filename}")
        return False
    
    # 读取文件
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️  读取文件失败: {filename}, 错误: {e}")
        return False
    
    # 提取章节标题
    title_match = re.search(r'^# (.+)', content, re.MULTILINE)
    if not title_match:
        print(f"⚠️  无法提取章节标题: {filename}")
        return False
    title = title_match.group(1)
    
    # 获取配置
    config = CHAPTER_CONFIGS.get(filename, get_default_config())
    
    # 创建优化后的头部
    new_header = create_optimized_header(title, config)
    
    # 找到第一个二级标题的位置
    first_h2_match = re.search(r'^## ', content, re.MULTILINE)
    if first_h2_match:
        split_pos = first_h2_match.start()
        original_content = content[split_pos:]
        
        # 移除原有的"核心观点预览"和"引言"部分
        original_content = re.sub(r'## 核心观点预览.*?^## ', '## ', original_content,
                                flags=re.MULTILINE | re.DOTALL)
        
        new_content = new_header + original_content
    else:
        new_content = new_header + content
    
    # 添加章节总结
    new_content = add_chapter_summary(new_content, config)
    
    # 写回文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 已优化: {filename}")
        return True
    except Exception as e:
        print(f"⚠️  写入文件失败: {filename}, 错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("统一场论书籍章节批量优化 V2")
    print("=" * 60)
    
    # 获取所有章节文件
    chapter_files = []
    for filename in os.listdir(CHAPTERS_DIR):
        if filename.startswith("第") and filename.endswith(".md"):
            # 排除已优化的章节
            if filename not in ["第1章：统一场论概述.md", "第3章：空间的基本构成.md"]:
                chapter_files.append(filename)
    
    # 按章节编号排序
    chapter_files.sort()
    
    print(f"\n找到 {len(chapter_files)} 个待优化章节\n")
    
    # 优化每个章节
    success_count = 0
    fail_count = 0
    for filename in chapter_files:
        if optimize_chapter(filename):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"优化完成！")
    print(f"成功: {success_count}/{len(chapter_files)}")
    print(f"失败: {fail_count}/{len(chapter_files)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
