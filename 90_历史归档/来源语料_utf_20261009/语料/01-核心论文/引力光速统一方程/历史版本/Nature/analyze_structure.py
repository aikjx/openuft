# 论文结构分析脚本
import re

# 读取论文内容
with open('A Geometric Derivation of the Gravitational Constant from First Principles.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# 分析论文结构
print("===== 论文结构分析报告 =====\n")

# 1. 检查基本结构元素
print("1. 基本结构元素检查:")
structure_elements = [
    ('\\documentclass', '文档类声明'),
    ('\\begin{document}', '文档开始'),
    ('\\end{document}', '文档结束'),
    ('\\maketitle', '标题生成'),
    ('\\begin{abstract}', '摘要开始'),
    ('\\end{abstract}', '摘要结束'),
    ('\\section{', '章节'),
]

for cmd, desc in structure_elements:
    if cmd in content:
        print(f"   ✓ {desc}")
    else:
        print(f"   ✗ {desc} 缺失")

# 2. 分析章节结构
print("\n2. 章节结构分析:")
sections = re.findall(r'\\section\{(.*?)\}', content)
for i, section in enumerate(sections, 1):
    print(f"   {i}. {section}")

# 3. 检查章节数量和顺序
print(f"\n3. 章节总数: {len(sections)}")

# 4. 检查逻辑连贯性
print("\n4. 逻辑连贯性评估:")

# 检查引言->理论->推导->应用->结论的逻辑流
required_sections = ['Introduction', 'Core Theoretical Framework', 'Derivation', 'Physical Implications', 'Experimental Verification', 'Conclusion', 'Methods']
missing_sections = []

for req_section in required_sections:
    found = False
    for section in sections:
        if req_section.lower() in section.lower():
            found = True
            break
    if not found:
        missing_sections.append(req_section)

if not missing_sections:
    print("   ✓ 包含所有核心章节，逻辑结构完整")
else:
    print(f"   ✗ 缺少关键章节: {', '.join(missing_sections)}")

# 5. 检查摘要内容
print("\n5. 摘要内容分析:")
abstract_match = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', content, re.DOTALL)
if abstract_match:
    abstract = abstract_match.group(1).strip()
    if len(abstract) > 100:
        print(f"   ✓ 摘要长度适中 ({len(abstract)} 字符)")
    else:
        print(f"   ⚠ 摘要可能过短 ({len(abstract)} 字符)")
    
    # 检查摘要是否包含关键元素
    key_elements = [
        ('研究问题', 'gravitational constant'),
        ('研究方法', 'geometric principles'),
        ('主要发现', 'G = 2Z/c'),
        ('结论意义', 'unified field theory')
    ]
    
    for element, keyword in key_elements:
        if keyword.lower() in abstract.lower():
            print(f"   ✓ 摘要包含{element}")
        else:
            print(f"   ✗ 摘要缺少{element}")
else:
    print("   ✗ 未找到摘要")

# 6. 检查参考文献部分
print("\n6. 参考文献检查:")
if '\\begin{thebibliography}' in content:
    bib_count = len(re.findall(r'\\bibitem', content))
    print(f"   ✓ 参考文献数量: {bib_count}")
    if bib_count >= 10:
        print("   ✓ 参考文献数量充足")
    else:
        print("   ⚠ 参考文献数量可能不足")
else:
    print("   ✗ 未找到参考文献部分")

# 7. 检查图表引用
print("\n7. 图表引用分析:")
fig_count = len(re.findall(r'\\begin{figure}', content))
ref_count = len(re.findall(r'\\ref\{.*?\}', content))
print(f"   ✓ 图表数量: {fig_count}")
print(f"   ✓ 交叉引用数量: {ref_count}")

# 8. 综合评估
print("\n===== 结构综合评估 =====")
if len(sections) >= 6 and len(abstract) > 150 and bib_count >= 8:
    print("✓ 论文结构基本完整，符合学术发表要求")
else:
    print("⚠ 论文结构存在不足，需要改进")

print("\n===== 结构改进建议 =====")
suggestions = []
if len(sections) < 6:
    suggestions.append("考虑增加章节以完善论文结构")
if 'Introduction' not in [s.lower() for s in sections]:
    suggestions.append("确保包含引言部分，清晰阐述研究背景和意义")
if 'Conclusion' not in [s.lower() for s in sections]:
    suggestions.append("添加结论部分，总结主要发现和意义")
if bib_count < 10:
    suggestions.append("增加更多相关参考文献以增强学术支撑")
if fig_count == 0:
    suggestions.append("添加图表以可视化关键概念和结果")

if suggestions:
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
else:
    print("✓ 结构方面无需重大改进")
