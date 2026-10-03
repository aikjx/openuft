#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论书籍全自动分析修复优化工具
功能：
1. 书籍结构分析（版本比较、章节完整性检查）
2. 章节内容分析（格式检查、内容质量评估）
3. 自动修复（缺失章节检测、内容补充）
4. 批量优化（整合现有优化脚本功能）
5. 优化结果验证（格式验证、内容一致性检查）
6. 详细报告生成（分析结果、优化建议）
"""

import os
import re
import json
import datetime
from pathlib import Path

# 书籍主目录
BOOK_ROOT_DIR = r"d:/a10/aikjx/code/my_lib/utf/12-书籍/人人都能理解统一场论"

# 章节优化配置（整合现有配置）
CHAPTER_CONFIGS = {
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
    },
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

class BookAnalyzer:
    """书籍分析器"""
    
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.analysis_results = {}
        self.reports_dir = os.path.join(root_dir, "分析报告")
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def analyze_book_structure(self):
        """分析书籍结构"""
        print("\n" + "=" * 80)
        print("📚 开始分析书籍结构")
        print("=" * 80)
        
        # 分析版本结构
        versions = []
        for item in os.listdir(self.root_dir):
            version_path = os.path.join(self.root_dir, item)
            if os.path.isdir(version_path) and item.startswith("V"):
                versions.append(item)
        
        print(f"\n📋 发现的版本: {len(versions)}个")
        for version in versions:
            print(f"  - {version}")
        
        # 分析每个版本的章节
        for version in versions:
            version_path = os.path.join(self.root_dir, version)
            print(f"\n🔍 分析版本: {version}")
            
            # 检查章节文件
            chapter_files = []
            for file in os.listdir(version_path):
                if re.match(r'^第.*章.*\.md$', file):
                    chapter_files.append(file)
            
            print(f"  📚 章节数量: {len(chapter_files)}")
            
            # 检查目录文件
            directory_file = os.path.join(version_path, "目录.md")
            if os.path.exists(directory_file):
                print("  ✅ 目录文件存在")
            else:
                print("  ❌ 目录文件不存在")
        
        self.analysis_results["structure"] = {
            "versions": versions,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    def analyze_chapter_content(self, version="V1"):
        """分析章节内容"""
        print("\n" + "=" * 80)
        print(f"📝 开始分析{version}版本章节内容")
        print("=" * 80)
        
        version_path = os.path.join(self.root_dir, version)
        if not os.path.exists(version_path):
            print(f"❌ 版本目录不存在: {version}")
            return
        
        chapter_files = []
        for file in os.listdir(version_path):
            if re.match(r'^第.*章.*\.md$', file):
                chapter_files.append(file)
        
        print(f"\n📋 待分析章节数量: {len(chapter_files)}")
        
        content_analysis = []
        for chapter_file in chapter_files:
            chapter_path = os.path.join(version_path, chapter_file)
            print(f"\n🔍 分析章节: {chapter_file}")
            
            try:
                with open(chapter_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查格式
                has_title = re.search(r'^# .+', content, re.MULTILINE) is not None
                has_navigation = "## 本章导航" in content
                has_core_points = "## 核心观点预览" in content
                has_summary = "## 本章小结" in content
                
                # 检查内容质量
                word_count = len(content)
                section_count = len(re.findall(r'^## .+', content, re.MULTILINE))
                
                analysis = {
                    "file": chapter_file,
                    "format": {
                        "has_title": has_title,
                        "has_navigation": has_navigation,
                        "has_core_points": has_core_points,
                        "has_summary": has_summary
                    },
                    "quality": {
                        "word_count": word_count,
                        "section_count": section_count
                    }
                }
                
                content_analysis.append(analysis)
                
                # 打印分析结果
                print(f"  ✅ 标题: {'有' if has_title else '无'}")
                print(f"  ✅ 导航: {'有' if has_navigation else '无'}")
                print(f"  ✅ 核心观点: {'有' if has_core_points else '无'}")
                print(f"  ✅ 小结: {'有' if has_summary else '无'}")
                print(f"  ✅ 字数: {word_count}")
                print(f"  ✅ 节数: {section_count}")
                
            except Exception as e:
                print(f"  ❌ 分析失败: {e}")
        
        self.analysis_results["content"] = {
            "version": version,
            "chapters": content_analysis,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def detect_missing_chapters(self, version="V1"):
        """检测缺失章节"""
        print("\n" + "=" * 80)
        print(f"🔍 开始检测{version}版本缺失章节")
        print("=" * 80)
        
        version_path = os.path.join(self.root_dir, version)
        if not os.path.exists(version_path):
            print(f"❌ 版本目录不存在: {version}")
            return
        
        # 从目录.md文件中提取所有章节链接
        directory_path = os.path.join(version_path, "目录.md")
        if not os.path.exists(directory_path):
            print("❌ 目录文件不存在！")
            return
        
        with open(directory_path, 'r', encoding='utf-8') as f:
            directory_content = f.read()
        
        # 提取目录中的章节文件
        chapter_links = re.findall(r'\- \[.*?\]\((\./第.*?章.*?\.md)\)', directory_content)
        expected_chapters = [os.path.basename(link) for link in chapter_links]
        
        print(f"\n📋 目录中列出的章节数量: {len(expected_chapters)}")
        
        # 获取实际存在的章节文件
        actual_chapters = []
        for file in os.listdir(version_path):
            if re.match(r'^第.*章.*\.md$', file):
                actual_chapters.append(file)
        
        print(f"📋 实际存在的章节数量: {len(actual_chapters)}")
        
        # 检查缺失的章节
        missing_chapters = [chapter for chapter in expected_chapters if chapter not in actual_chapters]
        if missing_chapters:
            print(f"\n❌ 缺失的章节文件: {len(missing_chapters)}个")
            for chapter in missing_chapters:
                print(f"  - {chapter}")
        else:
            print("\n✅ 所有目录中列出的章节文件都存在！")
        
        # 检查额外的章节（不在目录中的章节）
        extra_chapters = [chapter for chapter in actual_chapters if chapter not in expected_chapters]
        if extra_chapters:
            print(f"\n⚠️  额外的章节文件（不在目录中）: {len(extra_chapters)}个")
            for chapter in extra_chapters:
                print(f"  - {chapter}")
        else:
            print("\n✅ 没有额外的章节文件！")
        
        self.analysis_results["missing_chapters"] = {
            "version": version,
            "expected": expected_chapters,
            "actual": actual_chapters,
            "missing": missing_chapters,
            "extra": extra_chapters,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def generate_report(self):
        """生成分析报告"""
        print("\n" + "=" * 80)
        print("📊 生成分析报告")
        print("=" * 80)
        
        report_file = os.path.join(self.reports_dir, f"分析报告_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        
        report_content = f"# 统一场论书籍分析报告\n\n"
        report_content += f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 书籍结构分析
        if "structure" in self.analysis_results:
            structure = self.analysis_results["structure"]
            report_content += "## 一、书籍结构分析\n\n"
            report_content += f"### 1.1 版本信息\n"
            report_content += f"发现的版本数量: {len(structure['versions'])}个\n\n"
            report_content += "版本列表:\n"
            for version in structure['versions']:
                report_content += f"- {version}\n"
            report_content += "\n"
        
        # 章节内容分析
        if "content" in self.analysis_results:
            content = self.analysis_results["content"]
            report_content += f"## 二、{content['version']}版本章节内容分析\n\n"
            report_content += f"### 2.1 章节概览\n"
            report_content += f"分析的章节数量: {len(content['chapters'])}个\n\n"
            
            # 格式问题统计
            format_issues = []
            for chapter in content['chapters']:
                issues = []
                if not chapter['format']['has_title']:
                    issues.append("缺少标题")
                if not chapter['format']['has_navigation']:
                    issues.append("缺少导航")
                if not chapter['format']['has_core_points']:
                    issues.append("缺少核心观点")
                if not chapter['format']['has_summary']:
                    issues.append("缺少小结")
                if issues:
                    format_issues.append({"file": chapter['file'], "issues": issues})
            
            if format_issues:
                report_content += "### 2.2 格式问题\n"
                report_content += f"存在格式问题的章节数量: {len(format_issues)}个\n\n"
                for issue in format_issues:
                    report_content += f"- **{issue['file']}**: {', '.join(issue['issues'])}\n"
                report_content += "\n"
            else:
                report_content += "### 2.2 格式问题\n"
                report_content += "✅ 所有章节格式完整\n\n"
        
        # 缺失章节分析
        if "missing_chapters" in self.analysis_results:
            missing = self.analysis_results["missing_chapters"]
            report_content += f"## 三、{missing['version']}版本章节完整性分析\n\n"
            report_content += f"### 3.1 章节统计\n"
            report_content += f"目录中列出的章节: {len(missing['expected'])}个\n"
            report_content += f"实际存在的章节: {len(missing['actual'])}个\n"
            report_content += f"缺失的章节: {len(missing['missing'])}个\n"
            report_content += f"额外的章节: {len(missing['extra'])}个\n\n"
            
            if missing['missing']:
                report_content += "### 3.2 缺失章节列表\n"
                for chapter in missing['missing']:
                    report_content += f"- {chapter}\n"
                report_content += "\n"
            
            if missing['extra']:
                report_content += "### 3.3 额外章节列表\n"
                for chapter in missing['extra']:
                    report_content += f"- {chapter}\n"
                report_content += "\n"
        
        # 优化建议
        report_content += "## 四、优化建议\n\n"
        report_content += "### 4.1 结构优化\n"
        report_content += "- 确保每个版本都有完整的目录文件\n"
        report_content += "- 统一章节命名格式\n"
        report_content += "- 建立版本间的内容映射关系\n\n"
        
        report_content += "### 4.2 内容优化\n"
        report_content += "- 为所有章节添加标准格式（标题、导航、核心观点、小结）\n"
        report_content += "- 确保章节内容的一致性和连贯性\n"
        report_content += "- 补充缺失的章节内容\n\n"
        
        report_content += "### 4.3 格式优化\n"
        report_content += "- 统一使用emoji增强可读性\n"
        report_content += "- 添加表格和列表提高信息组织\n"
        report_content += "- 确保Markdown格式的正确性\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ 分析报告已生成: {report_file}")
        return report_file

class BookFixer:
    """书籍修复器"""
    
    def __init__(self, root_dir):
        self.root_dir = root_dir
    
    def fix_missing_chapters(self, version="V1"):
        """修复缺失章节"""
        print("\n" + "=" * 80)
        print(f"🔧 开始修复{version}版本缺失章节")
        print("=" * 80)
        
        version_path = os.path.join(self.root_dir, version)
        if not os.path.exists(version_path):
            print(f"❌ 版本目录不存在: {version}")
            return
        
        # 从目录.md文件中提取所有章节链接
        directory_path = os.path.join(version_path, "目录.md")
        if not os.path.exists(directory_path):
            print("❌ 目录文件不存在，无法检测缺失章节！")
            return
        
        with open(directory_path, 'r', encoding='utf-8') as f:
            directory_content = f.read()
        
        # 提取目录中的章节文件
        chapter_links = re.findall(r'\- \[.*?\]\((\./第.*?章.*?\.md)\)', directory_content)
        expected_chapters = [os.path.basename(link) for link in chapter_links]
        
        # 获取实际存在的章节文件
        actual_chapters = []
        for file in os.listdir(version_path):
            if re.match(r'^第.*章.*\.md$', file):
                actual_chapters.append(file)
        
        # 检查缺失的章节
        missing_chapters = [chapter for chapter in expected_chapters if chapter not in actual_chapters]
        
        if not missing_chapters:
            print("✅ 没有缺失的章节文件，无需修复！")
            return
        
        print(f"\n⚠️  发现{len(missing_chapters)}个缺失章节，开始创建占位文件...")
        
        for chapter in missing_chapters:
            chapter_path = os.path.join(version_path, chapter)
            print(f"\n🔧 创建章节文件: {chapter}")
            
            # 提取章节标题
            title_match = re.search(r'第.*章：(.*?)\.md', chapter)
            if title_match:
                chapter_title = title_match.group(1)
            else:
                chapter_title = chapter.replace('.md', '')
            
            # 创建占位内容
            placeholder_content = f"# {chapter_title}\n\n"
            placeholder_content += f"> 💡 **引用名言**：探索宇宙的奥秘，从理解基本概念开始。\n\n"
            placeholder_content += "## 本章导航\n"
            placeholder_content += "- 📖 第1节\n"
            placeholder_content += "- 💡 第2节\n"
            placeholder_content += "- 🚀 第3节\n"
            placeholder_content += "- 🔍 第4节\n\n"
            placeholder_content += "## 核心观点预览\n"
            placeholder_content += "| 核心思想 | 关键词 | 章节关联 |\n"
            placeholder_content += "|---------|--------|---------|\n"
            placeholder_content += "| 核心思想1 | 关键词1 | 1.1 |\n"
            placeholder_content += "| 核心思想2 | 关键词2 | 1.2 |\n\n"
            placeholder_content += "## 章节内容\n\n"
            placeholder_content += "### 1.1 基本概念\n\n"
            placeholder_content += "本节将介绍基本概念...\n\n"
            placeholder_content += "### 1.2 核心原理\n\n"
            placeholder_content += "本节将介绍核心原理...\n\n"
            placeholder_content += "### 1.3 实际应用\n\n"
            placeholder_content += "本节将介绍实际应用...\n\n"
            placeholder_content += "### 1.4 总结与展望\n\n"
            placeholder_content += "本节将进行总结与展望...\n\n"
            placeholder_content += "## 本章小结\n\n"
            placeholder_content += "### 📚 知识要点回顾\n\n"
            placeholder_content += "通过本章学习，我们深入了解了相关概念和原理。\n\n"
            placeholder_content += "### 🎯 学习目标达成\n\n"
            placeholder_content += "通过本章学习，你应该能够：\n\n"
            placeholder_content += "- ✅ 掌握核心概念\n"
            placeholder_content += "- ✅ 理解基本原理\n"
            placeholder_content += "- ✅ 认识实际应用\n"
            
            try:
                with open(chapter_path, 'w', encoding='utf-8') as f:
                    f.write(placeholder_content)
                print(f"  ✅ 成功创建章节文件")
            except Exception as e:
                print(f"  ❌ 创建失败: {e}")
        
        print(f"\n✅ 修复完成！创建了{len(missing_chapters)}个缺失章节的占位文件。")

class BookOptimizer:
    """书籍优化器"""
    
    def __init__(self, root_dir):
        self.root_dir = root_dir
    
    def create_optimized_header(self, title, config):
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
    
    def add_chapter_summary(self, content, config):
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
    
    def optimize_chapter(self, chapter_path, chapter_file):
        """优化单个章节"""
        print(f"\n🔧 优化章节: {chapter_file}")
        
        try:
            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取章节标题
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            if not title_match:
                print(f"  ⚠️  无法提取章节标题")
                return False
            title = title_match.group(1)
            
            # 获取配置
            config = CHAPTER_CONFIGS.get(chapter_file, get_default_config(title))
            
            # 创建优化后的头部
            new_header = self.create_optimized_header(title, config)
            
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
            new_content = self.add_chapter_summary(new_content, config)
            
            # 写回文件
            with open(chapter_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ 优化成功")
            return True
        except Exception as e:
            print(f"  ❌ 优化失败: {e}")
            return False
    
    def batch_optimize(self, version="V1"):
        """批量优化章节"""
        print("\n" + "=" * 80)
        print(f"🚀 开始批量优化{version}版本章节")
        print("=" * 80)
        
        version_path = os.path.join(self.root_dir, version)
        if not os.path.exists(version_path):
            print(f"❌ 版本目录不存在: {version}")
            return
        
        # 获取所有章节文件
        chapter_files = []
        for file in os.listdir(version_path):
            if re.match(r'^第.*章.*\.md$', file):
                chapter_files.append(file)
        
        print(f"\n📋 待优化章节数量: {len(chapter_files)}")
        
        # 优化每个章节
        success_count = 0
        fail_count = 0
        
        for chapter_file in chapter_files:
            chapter_path = os.path.join(version_path, chapter_file)
            if self.optimize_chapter(chapter_path, chapter_file):
                success_count += 1
            else:
                fail_count += 1
        
        print("\n" + "=" * 80)
        print(f"优化完成！")
        print(f"成功: {success_count}/{len(chapter_files)}")
        print(f"失败: {fail_count}/{len(chapter_files)}")
        print("=" * 80)

class BookValidator:
    """书籍验证器"""
    
    def __init__(self, root_dir):
        self.root_dir = root_dir
    
    def validate_format(self, version="V1"):
        """验证章节格式"""
        print("\n" + "=" * 80)
        print(f"✅ 开始验证{version}版本章节格式")
        print("=" * 80)
        
        version_path = os.path.join(self.root_dir, version)
        if not os.path.exists(version_path):
            print(f"❌ 版本目录不存在: {version}")
            return
        
        # 获取所有章节文件
        chapter_files = []
        for file in os.listdir(version_path):
            if re.match(r'^第.*章.*\.md$', file):
                chapter_files.append(file)
        
        print(f"\n📋 待验证章节数量: {len(chapter_files)}")
        
        valid_count = 0
        invalid_count = 0
        invalid_chapters = []
        
        for chapter_file in chapter_files:
            chapter_path = os.path.join(version_path, chapter_file)
            print(f"\n🔍 验证章节: {chapter_file}")
            
            try:
                with open(chapter_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查格式
                has_title = re.search(r'^# .+', content, re.MULTILINE) is not None
                has_navigation = "## 本章导航" in content
                has_core_points = "## 核心观点预览" in content
                has_summary = "## 本章小结" in content
                
                # 验证结果
                is_valid = has_title and has_navigation and has_core_points and has_summary
                
                if is_valid:
                    print("  ✅ 格式验证通过")
                    valid_count += 1
                else:
                    print("  ❌ 格式验证失败")
                    issues = []
                    if not has_title:
                        issues.append("缺少标题")
                    if not has_navigation:
                        issues.append("缺少导航")
                    if not has_core_points:
                        issues.append("缺少核心观点")
                    if not has_summary:
                        issues.append("缺少小结")
                    print(f"  ⚠️  问题: {', '.join(issues)}")
                    invalid_count += 1
                    invalid_chapters.append({"file": chapter_file, "issues": issues})
                    
            except Exception as e:
                print(f"  ❌ 验证失败: {e}")
                invalid_count += 1
                invalid_chapters.append({"file": chapter_file, "issues": [f"读取错误: {str(e)}"]})
        
        print("\n" + "=" * 80)
        print(f"验证完成！")
        print(f"通过: {valid_count}/{len(chapter_files)}")
        print(f"失败: {invalid_count}/{len(chapter_files)}")
        print("=" * 80)
        
        return valid_count, invalid_count, invalid_chapters

def main():
    """主函数"""
    print("""
    ================================================================================
    🚀 统一场论书籍全自动分析修复优化工具
    ================================================================================
    功能：
    1. 书籍结构分析（版本比较、章节完整性检查）
    2. 章节内容分析（格式检查、内容质量评估）
    3. 自动修复（缺失章节检测、内容补充）
    4. 批量优化（整合现有优化脚本功能）
    5. 优化结果验证（格式验证、内容一致性检查）
    6. 详细报告生成（分析结果、优化建议）
    ================================================================================
    """)
    
    # 初始化工具
    analyzer = BookAnalyzer(BOOK_ROOT_DIR)
    fixer = BookFixer(BOOK_ROOT_DIR)
    optimizer = BookOptimizer(BOOK_ROOT_DIR)
    validator = BookValidator(BOOK_ROOT_DIR)
    
    # 步骤1: 书籍结构分析
    analyzer.analyze_book_structure()
    
    # 步骤2: 章节内容分析
    analyzer.analyze_chapter_content(version="V1")
    
    # 步骤3: 检测缺失章节
    analyzer.detect_missing_chapters(version="V1")
    
    # 步骤4: 生成分析报告
    analyzer.generate_report()
    
    # 步骤5: 修复缺失章节
    fixer.fix_missing_chapters(version="V1")
    
    # 步骤6: 批量优化章节
    optimizer.batch_optimize(version="V1")
    
    # 步骤7: 验证优化结果
    validator.validate_format(version="V1")
    
    print("\n" + "=" * 80)
    print("🎉 全自动分析修复优化完成！")
    print("=" * 80)
    print("\n📋 执行结果:")
    print("1. ✅ 书籍结构分析完成")
    print("2. ✅ 章节内容分析完成")
    print("3. ✅ 缺失章节检测完成")
    print("4. ✅ 分析报告生成完成")
    print("5. ✅ 缺失章节修复完成")
    print("6. ✅ 章节批量优化完成")
    print("7. ✅ 优化结果验证完成")
    print("\n📁 分析报告保存位置:")
    print(f"   {analyzer.reports_dir}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
