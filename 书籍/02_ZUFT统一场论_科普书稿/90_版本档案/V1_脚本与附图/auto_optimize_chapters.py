# -*- coding: utf-8 -*-
"""
统一场论书籍章节自动优化脚本
功能：批量优化所有章节，添加导航、表格、emoji等视觉元素
"""

import os
import re
from pathlib import Path

# 章节配置
CHAPTERS_DIR = r"d:/a10/aikjx/code/my_lib/utf/12-书籍/人人都能理解统一场论/V1"

# 每个章节的优化配置
CHAPTER_CONFIG = {
    "第2章：空间的本质.md": {
        "quote": "宇宙中最难理解的不是遥远的星系，而是我们生活其中的空间。—— 爱因斯坦",
        "navigation": [
            "📖 2.1 我们生活的三维空间：从日常经验到科学认知",
            "💡 2.2 空间是运动的吗？",
            "🚀 2.3 空间的基本属性",
            "🔍 2.4 物质与空间的相互关系"
        ],
        "table_rows": [
            ["空间是三维的", "长、宽、高、坐标系", "2.1"],
            ["空间是运动的", "像流动的水、动态流体", "2.2"],
            ["空间的四重属性", "连续、无限、均匀、各向同性", "2.3"],
            ["物质与空间相互影响", "物质影响空间、空间决定物质", "2.4"],
            ["力是空间运动的表现", "引力、电磁力、核力", "第3-4章"]
        ],
        "goals": [
            "描述空间的三维特性及其感知方式",
            "理解空间运动的证据和特点",
            "掌握空间的四重基本属性",
            "解释物质与空间的相互关系"
        ]
    },
    "第3章：空间的基本构成.md": {
        "quote": "宇宙是由最小的空间单元组成的，这些单元的运动构成了我们所看到的一切。",
        "navigation": [
            "📖 3.1 空间是否有最小单元？",
            "💡 3.2 空间单元的运动特性",
            "🚀 3.3 空间单元的相互作用",
            "🔍 3.4 空间与物质的相互转化"
        ],
        "table_rows": [
            ["空间的最小单元", "普朗克长度、量子化", "3.1"],
            ["螺旋运动", "旋转与直线运动的结合", "3.2"],
            ["排斥与吸引", "空间单元的相互作用", "3.3"],
            ["相互转化", "E=mc²、质能关系", "3.4"]
        ],
        "goals": [
            "理解普朗克长度和空间单元的概念",
            "掌握空间单元的螺旋运动特性",
            "了解空间单元之间的相互作用",
            "认识空间与物质的相互转化"
        ]
    },
    "第4章：时间的本质.md": {
        "quote": "时间是宇宙最神秘的维度，我们无法看见它，却无处不在感受它。",
        "navigation": [
            "📖 4.1 时间的流逝：从过去到未来",
            "💡 4.2 时间的本质：传统与现代时间观",
            "🚀 4.3 时间与空间的关系",
            "🔍 4.4 时间的测量：时钟的原理"
        ],
        "table_rows": [
            ["时间的方向性", "熵增原理、时间箭头", "4.1"],
            ["相对时间观", "牛顿与爱因斯坦的时间观", "4.2"],
            ["时空同一性", "R=ct、光速不变", "4.3"],
            ["时钟原理", "周期性运动、时间测量", "4.4"]
        ],
        "goals": [
            "理解时间的单向性和方向性",
            "掌握相对论的时间观",
            "了解时间与空间的密切关系",
            "认识时钟的测量原理"
        ]
    },
    "第5章：时间的几何化.md": {
        "quote": "时间是空间的运动，空间位移可以表示时间。—— 时空同一化原理",
        "navigation": [
            "📖 5.1 时间是空间的运动：几何定义",
            "💡 5.2 时间流逝与空间运动的关系",
            "🚀 5.3 时间的方向性：单向性的起源",
            "🔍 5.4 时间旅行的可能性：理论与现实"
        ],
        "table_rows": [
            ["时间的几何化", "R=ct、空间位移表示时间", "5.1"],
            ["时间膨胀", "t'=t/√(1-v²/c²)", "5.2"],
            ["时间箭头", "熵增、不可逆性", "5.3"],
            ["时间旅行", "虫洞、悖论", "5.4"]
        ],
        "goals": [
            "理解时间的几何化描述",
            "掌握时间膨胀公式",
            "了解时间的方向性起源",
            "探讨时间旅行的可能性"
        ]
    }
}

def get_default_config(chapter_title):
    """获取默认配置（适用于大多数章节）"""
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
    goals = config.get("goals", [])

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

def create_section_enhancement(section_title):
    """创建小节增强"""
    return f"> 💡 **本节导读**：本节将深入探讨{section_title}的核心内容。\n\n"

def create_chapter_summary(goals):
    """创建章节总结"""
    summary = "\n## 本章小结\n\n"
    summary += "### 📚 知识要点回顾\n\n"
    summary += "通过本章学习，我们深入了解了相关概念和原理。\n\n"
    summary += "### 🎯 学习目标达成\n\n"
    summary += "通过本章学习，你应该能够：\n\n"
    for goal in goals:
        summary += f"- ✅ {goal}\n"
    summary += "\n"
    return summary

def optimize_chapter(filename):
    """优化单个章节"""
    filepath = os.path.join(CHAPTERS_DIR, filename)

    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filename}")
        return False

    # 读取文件
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取章节标题
    title_match = re.search(r'^# (.+)', content, re.MULTILINE)
    if not title_match:
        print(f"⚠️  无法提取章节标题: {filename}")
        return False
    title = title_match.group(1)

    # 获取配置
    config = CHAPTER_CONFIG.get(filename, get_default_config(title))

    # 创建优化后的头部
    new_header = create_optimized_header(title, config)

    # 替换原始头部
    # 找到第一个二级标题的位置
    first_h2_match = re.search(r'^## ', content, re.MULTILINE)
    if first_h2_match:
        split_pos = first_h2_match.start()
        original_content = content[split_pos:]

        # 移除原有的"核心观点预览"和"引言"部分（如果有）
        original_content = re.sub(r'## 核心观点预览.*?^## ', '## ', original_content,
                                flags=re.MULTILINE | re.DOTALL)

        new_content = new_header + original_content
    else:
        new_content = new_header + content

    # 在章节末尾添加总结（如果没有的话）
    if "## 本章小结" not in content:
        summary = create_chapter_summary(config.get("goals", []))
        new_content += summary

    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ 已优化: {filename}")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("统一场论书籍章节自动优化")
    print("=" * 60)

    # 获取所有章节文件
    chapter_files = []
    for filename in os.listdir(CHAPTERS_DIR):
        if filename.startswith("第") and filename.endswith(".md"):
            # 排除已优化的第1章
            if filename != "第1章：统一场论概述.md":
                chapter_files.append(filename)

    # 按章节编号排序
    chapter_files.sort()

    print(f"\n找到 {len(chapter_files)} 个待优化章节\n")

    # 优化每个章节
    success_count = 0
    for filename in chapter_files:
        if optimize_chapter(filename):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"优化完成！成功: {success_count}/{len(chapter_files)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
