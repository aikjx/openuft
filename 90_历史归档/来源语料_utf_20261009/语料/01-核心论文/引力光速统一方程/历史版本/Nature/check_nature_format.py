# Nature期刊格式检查脚本
import re
import os

# 读取论文内容
with open('A Geometric Derivation of the Gravitational Constant from First Principles.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("===== Nature期刊格式检查报告 =====\n")

# Nature格式要求参考：
# - 双栏布局 (twocolumn)
# - 12pt字体
# - 无编号章节
# - 标题粗体
# - 摘要不超过250个字
# - 参考文献格式
# - 图表格式

# 1. 文档类和基本设置
print("1. 文档类和基本设置检查:")

# 检查documentclass
documentclass_match = re.search(r'\\documentclass\[([^\]]+)\]\{([^\}]+)\}', content)
if documentclass_match:
    options = documentclass_match.group(1).split(',')
    document_class = documentclass_match.group(2)
    
    print(f"   ✓ 使用文档类: {document_class}")
    
    # 检查双栏设置
    if 'twocolumn' in options:
        print("   ✓ 正确使用双栏布局 (twocolumn)")
    else:
        print("   ✗ 未使用双栏布局，Nature要求双栏格式")
    
    # 检查字体大小
    if '12pt' in options:
        print("   ✓ 正确使用12pt字体")
    else:
        print("   ✗ 未使用12pt字体，Nature建议12pt字体")
else:
    print("   ✗ 未找到\documentclass定义")

# 2. 标题格式
print("\n2. 标题格式检查:")

# 检查标题粗体
if '\\textbf\\{title\\}' in content or '\\section\\*{\\textbf{' in content:
    print("   ✓ 标题使用了粗体格式")
else:
    print("   ⚠ 标题可能未使用粗体格式")

# 3. 摘要格式
print("\n3. 摘要格式检查:")

# 检查摘要环境
if '\\begin\\{abstract\\}' in content and '\\end\\{abstract\\}' in content:
    print("   ✓ 包含摘要环境")
    
    # 提取摘要内容
    abstract_match = re.search(r'\\begin\\{abstract\\}(.*?)\\end\\{abstract\\}', content, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
        abstract_length = len(abstract_text.split())  # 英文单词数
        abstract_chars = len(abstract_text.replace('\\', '').replace('{', '').replace('}', ''))
        
        print(f"   ✓ 摘要长度: {abstract_length} 个单词 / 约 {abstract_chars} 个字符")
        
        if abstract_chars <= 1500:  # Nature摘要通常不超过250词，大约1500字符
            print("   ✓ 摘要长度符合Nature要求")
        else:
            print("   ⚠ 摘要可能过长，Nature建议不超过250个单词")
else:
    print("   ✗ 未找到标准摘要环境")

# 4. 章节格式
print("\n4. 章节格式检查:")

# 检查章节使用
sections = re.findall(r'\\section\*?\{([^\}]*)\}', content)
if sections:
    print(f"   ✓ 包含 {len(sections)} 个章节")
    
    # 检查章节是否使用无编号格式
    starred_sections = re.findall(r'\\section\*\{([^\}]*)\}', content)
    if len(starred_sections) == len(sections):
        print("   ✓ 所有章节均使用无编号格式 (*)")
    else:
        print(f"   ⚠ 部分章节使用了编号格式，Nature通常使用无编号章节")
    
    # 检查章节标题
    print("   章节标题:")
    for i, section in enumerate(sections, 1):
        print(f"     {i}. {section}")
else:
    print("   ✗ 未找到章节定义")

# 5. 参考文献格式
print("\n5. 参考文献格式检查:")

# 检查参考文献环境
if '\\begin{thebibliography}' in content and '\\end{thebibliography}' in content:
    print("   ✓ 包含参考文献环境")
    
    # 检查参考文献数量
    bib_entries = re.findall(r'\\bibitem\{([^\}]*)\}', content)
    print(f"   ✓ 参考文献数量: {len(bib_entries)} 篇")
    
    # 检查参考文献格式
    if '\\bibitem{' in content and '\\cite{' in content:
        print("   ✓ 使用标准LaTeX参考文献格式")
    else:
        print("   ⚠ 参考文献格式可能不符合标准")
else:
    print("   ✗ 未找到标准参考文献环境")

# 6. 图表格式
print("\n6. 图表格式检查:")

# 检查图片环境
figures = re.findall(r'\\begin{figure}', content)
if figures:
    print(f"   ✓ 包含 {len(figures)} 个图片环境")
    
    # 检查图片格式
    figure_formats = re.findall(r'\\includegraphics\[?[^\]]*\]?\{([^\}]*)\}', content)
    if figure_formats:
        print(f"   ✓ 引用了 {len(figure_formats)} 个图片文件")
        valid_formats = ['.eps', '.pdf', '.tiff']
        for fmt in figure_formats:
            ext = os.path.splitext(fmt)[1].lower()
            if any(ext == valid_ext for valid_ext in valid_formats):
                print(f"     ✓ 图片格式有效: {fmt}")
            else:
                print(f"     ⚠ 图片格式可能不推荐: {fmt} (Nature推荐EPS或PDF)")
else:
    print("   ⚠ 未找到标准图片环境")

# 检查表格环境
tables = re.findall(r'\\begin{table}', content)
if tables:
    print(f"   ✓ 包含 {len(tables)} 个表格环境")
else:
    print("   ⚠ 未找到标准表格环境")

# 7. 数学公式格式
print("\n7. 数学公式格式检查:")

# 检查公式环境
equations = re.findall(r'\\begin{equation}', content)
if equations:
    print(f"   ✓ 包含 {len(equations)} 个带编号公式")
else:
    print("   ⚠ 未找到带编号公式")

inline_math = re.findall(r'\\\(([^)]*)\\\)', content)
if inline_math:
    print(f"   ✓ 包含 {len(inline_math)} 个行内公式")
else:
    print("   ⚠ 未找到行内公式")

# 8. 特殊要求
print("\n8. Nature特殊格式要求检查:")

# 检查行号
if 'linenumbers' in content:
    print("   ✓ 包含行号设置")
else:
    print("   ⚠ 未设置行号，Nature投稿通常需要行号")

# 检查引用格式
if re.search(r'\\cite\{[^\}]+\}', content):
    print("   ✓ 使用标准引用格式")
else:
    print("   ⚠ 可能未使用标准引用格式")

# 9. 长度检查
print("\n9. 论文长度检查:")

# 统计内容行数
lines = content.split('\n')
print(f"   ✓ 论文文件总行数: {len(lines)}")

# 统计正文长度（估算）
word_count = len(re.findall(r'\\b[A-Za-z]+\\b', content))
print(f"   ✓ 英文单词数: 约 {word_count}")

# Nature通常限制为5-6页
if word_count <= 7000:
    print("   ✓ 论文长度可能符合Nature的页数限制")
else:
    print("   ⚠ 论文可能过长，Nature通常限制为5-6页")

# 10. 格式合规性综合评分
print("\n===== Nature格式合规性综合评分 =====")

# 评分系统 (0-100)
score = 100

# 重要扣分项
if 'twocolumn' not in options and documentclass_match:
    score -= 20
    print("✗ 未使用双栏布局，这是Nature的基本要求 (-20)")
if '12pt' not in options and documentclass_match:
    score -= 10
    print("✗ 未使用12pt字体 (-10)")
if '\\begin{abstract}' not in content:
    score -= 15
    print("✗ 缺少标准摘要环境 (-15)")
if len(sections) < 2:
    score -= 15
    print("✗ 章节结构不完整 (-15)")
if '\\begin{thebibliography}' not in content:
    score -= 20
    print("✗ 缺少标准参考文献环境 (-20)")

# 次要扣分项
if 'linenumbers' not in content:
    score -= 5
    print("✗ 未设置行号 (-5)")
if word_count > 7000:
    score -= 5
    print("✗ 论文可能过长 (-5)")
if len(starred_sections) != len(sections) and sections:
    score -= 5
    print("✗ 部分章节使用了编号格式 (-5)")

score = max(0, min(100, score))  # 确保分数在0-100之间

print(f"\n最终格式评分: {score}/100")

if score >= 80:
    print("✓ 论文格式基本符合Nature期刊投稿要求")
elif score >= 60:
    print("⚠ 论文格式基本合理，但有较多需要修改的地方")
else:
    print("✗ 论文格式不符合Nature期刊投稿要求，需要重大修改")

print("\n===== 格式改进建议 =====")
suggestions = []

if 'twocolumn' not in options and documentclass_match:
    suggestions.append("在documentclass中添加twocolumn选项")
if '12pt' not in options and documentclass_match:
    suggestions.append("在documentclass中添加12pt选项")
if '\\begin{abstract}' not in content:
    suggestions.append("添加标准摘要环境")
if 'linenumbers' not in content:
    suggestions.append("添加行号设置")
if len(sections) < 2:
    suggestions.append("完善章节结构")
if len(starred_sections) != len(sections) and sections:
    suggestions.append("将所有章节改为无编号格式（添加*）")

if suggestions:
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
else:
    print("✓ 格式方面无需重大改进")
