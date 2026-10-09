# 图表质量和说明分析脚本
import re
import os

# 读取论文内容
with open('A Geometric Derivation of the Gravitational Constant from First Principles.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("===== 图表质量和说明分析报告 =====\n")

# 1. 图表基本信息
print("1. 图表基本信息:")

# 检查所有图片环境
figure_environments = re.findall(r'\\begin{figure}(.*?)\\end{figure}', content, re.DOTALL)
print(f"   ✓ 论文包含 {len(figure_environments)} 个图片环境")

# 提取所有图表标题和引用
figure_captions = []
figure_references = []
figure_files = []

for i, fig_env in enumerate(figure_environments, 1):
    # 提取图表标题
    caption_match = re.search(r'\\caption\{([^\}]*)\}', fig_env)
    if caption_match:
        caption = caption_match.group(1).strip()
        figure_captions.append((i, caption))
        print(f"   图表 {i} 标题: {caption[:80]}{'...' if len(caption) > 80 else ''}")
    else:
        print(f"   ⚠ 图表 {i} 缺少标题")
    
    # 提取图片文件名
    figure_matches = re.findall(r'\\includegraphics\[?[^\]]*\]?\{([^\}]*)\}', fig_env)
    for fig_file in figure_matches:
        figure_files.append((i, fig_file))
        print(f"   图表 {i} 文件: {fig_file}")

# 检查表格环境
table_environments = re.findall(r'\\begin{table}(.*?)\\end{table}', content, re.DOTALL)
print(f"   ✓ 论文包含 {len(table_environments)} 个表格环境")

# 2. 图表格式检查
print("\n2. 图表格式检查:")

# 检查图片格式
valid_formats = ['.eps', '.pdf', '.tiff']
format_issues = []

for fig_num, fig_file in figure_files:
    ext = os.path.splitext(fig_file)[1].lower()
    if any(ext == valid_ext for valid_ext in valid_formats):
        print(f"   ✓ 图表 {fig_num} 格式有效: {fig_file}")
    else:
        format_issues.append((fig_num, fig_file, ext))
        print(f"   ⚠ 图表 {fig_num} 格式可能不推荐: {fig_file} (Nature推荐EPS或PDF)")

# 检查图表放置选项
float_options = re.findall(r'\\begin{figure\[([^\]]*)\]', content)
if float_options:
    print("   ✓ 图表使用了浮动位置选项")
    for i, option in enumerate(float_options, 1):
        print(f"     图表 {i} 浮动选项: [{option}]")
else:
    print("   ⚠ 图表未指定浮动位置选项，可能影响排版")

# 检查图表宽度/高度设置
width_settings = re.findall(r'\\includegraphics\[(.*?)width=([^,\]]*)', content)
if width_settings:
    print(f"   ✓ 有 {len(width_settings)} 个图表设置了宽度")
    for setting in width_settings:
        width = setting[1].strip()
        if '\textwidth' in width or '\columnwidth' in width:
            print(f"     ✓ 使用相对宽度设置: {width}")
        else:
            print(f"     ⚠ 使用固定宽度设置: {width}")
else:
    print("   ⚠ 未找到明确的图表宽度设置")

# 3. 图表说明文本质量
print("\n3. 图表说明文本质量:")

caption_scores = []

for fig_num, caption in figure_captions:
    # 检查标题长度
    words = caption.split()
    caption_score = 10
    
    if len(words) < 10:
        caption_score -= 3
        print(f"   ⚠ 图表 {fig_num} 说明过于简短 ({len(words)} 个单词)")
    elif len(words) > 50:
        caption_score -= 2
        print(f"   ⚠ 图表 {fig_num} 说明过于冗长 ({len(words)} 个单词)")
    else:
        print(f"   ✓ 图表 {fig_num} 说明长度适中 ({len(words)} 个单词)")
    
    # 检查是否包含足够的说明内容
    if any(keyword in caption.lower() for keyword in ['shows', 'illustrates', 'demonstrates', 'presents', 'compares']):
        print(f"   ✓ 图表 {fig_num} 说明包含描述性动词")
    else:
        caption_score -= 2
        print(f"   ⚠ 图表 {fig_num} 说明缺少描述性动词")
    
    # 检查是否包含必要的细节
    if 'figure' not in caption.lower() and 'fig' not in caption.lower():
        print(f"   ✓ 图表 {fig_num} 说明不重复'figure'字样")
    else:
        caption_score -= 1
        print(f"   ⚠ 图表 {fig_num} 说明包含多余的'figure'字样")
    
    caption_scores.append(caption_score)

avg_caption_score = sum(caption_scores) / len(caption_scores) if caption_scores else 0
print(f"   ✓ 平均图表说明质量评分: {avg_caption_score:.1f}/10")

if avg_caption_score >= 8:
    print("   ✓ 图表说明文本质量良好")
elif avg_caption_score >= 5:
    print("   ⚠ 图表说明文本质量一般")
else:
    print("   ✗ 图表说明文本质量较差")

# 4. 图表引用检查
print("\n4. 图表引用检查:")

# 检查正文对图表的引用
figure_refs = re.findall(r'\\ref\{fig:([^\}]*)\}', content)
print(f"   ✓ 论文中引用图表 {len(figure_refs)} 次")

# 检查引用的唯一性和完整性
referenced_figs = set(figure_refs)
print(f"   ✓ 被引用的图表数量: {len(referenced_figs)}")

# 检查是否有图表未被引用
all_fig_labels = re.findall(r'\\label\{fig:([^\}]*)\}', content)
all_figs = set(all_fig_labels)

if all_figs:
    unused_figs = all_figs - referenced_figs
    if unused_figs:
        print(f"   ⚠ 有 {len(unused_figs)} 个图表未被引用: {', '.join(unused_figs)}")
    else:
        print("   ✓ 所有图表均在正文中被引用")
else:
    print("   ⚠ 未找到图表标签定义")

# 5. 图表相关性和信息传递
print("\n5. 图表相关性和信息传递:")

# 分析图表的主题相关性
fig_topics = []
for fig_num, caption in figure_captions:
    if any(keyword in caption.lower() for keyword in ['gravity', 'gravitational', 'g=']):
        topic = 'Gravitational Constant'
    elif any(keyword in caption.lower() for keyword in ['light', 'speed', 'c=']):
        topic = 'Speed of Light'
    elif any(keyword in caption.lower() for keyword in ['spacetime', 'space-time', 'geometry']):
        topic = 'Spacetime Geometry'
    elif any(keyword in caption.lower() for keyword in ['relationship', 'unification', 'connection']):
        topic = 'Unification Relationship'
    else:
        topic = 'Other'
    
    fig_topics.append((fig_num, topic))
    print(f"   图表 {fig_num} 主题: {topic}")

# 检查图表多样性
unique_topics = set(topic for num, topic in fig_topics)
print(f"   ✓ 图表涵盖 {len(unique_topics)} 个不同主题")

if len(unique_topics) >= 3 and len(figure_environments) >= 3:
    print("   ✓ 图表主题多样性良好")
else:
    print("   ⚠ 图表主题多样性不足")

# 6. 图表文件存在性检查
print("\n6. 图表文件存在性检查:")

missing_files = []
for fig_num, fig_file in figure_files:
    if os.path.exists(fig_file):
        print(f"   ✓ 图表 {fig_num} 文件存在: {fig_file}")
    else:
        missing_files.append((fig_num, fig_file))
        print(f"   ⚠ 图表 {fig_num} 文件可能不存在: {fig_file}")

# 7. 图表综合质量评分
print("\n===== 图表综合质量评分 =====")

# 评分系统 (0-100)
score = 100

# 格式评分
if format_issues:
    score -= len(format_issues) * 10
    print(f"✗ 图表格式不规范 (-{len(format_issues)*10})")

# 说明文本评分
if avg_caption_score < 5:
    score -= 20
    print("✗ 图表说明文本质量较差 (-20)")
elif avg_caption_score < 8:
    score -= 10
    print("⚠ 图表说明文本质量一般 (-10)")

# 引用完整性评分
if all_figs and unused_figs:
    score -= len(unused_figs) * 10
    print(f"✗ 部分图表未被引用 (-{len(unused_figs)*10})")

# 文件存在性评分
if missing_files:
    score -= len(missing_files) * 15
    print(f"✗ 图表文件缺失 (-{len(missing_files)*15})")

# 多样性评分
if len(unique_topics) < 3 and len(figure_environments) >= 3:
    score -= 10
    print("⚠ 图表主题多样性不足 (-10)")

# 加分项
if not format_issues:
    score += 10
    print("✓ 图表格式规范 (+10)")
if avg_caption_score >= 8:
    score += 10
    print("✓ 图表说明文本质量优秀 (+10)")
if all_figs and not unused_figs:
    score += 5
    print("✓ 所有图表均被合理引用 (+5)")
if len(figure_environments) >= 4:
    score += 5
    print("✓ 图表数量充足 (+5)")

score = max(0, min(100, score))  # 确保分数在0-100之间

print(f"\n最终图表质量评分: {score}/100")

if score >= 80:
    print("✓ 图表质量优秀，符合学术发表要求")
elif score >= 60:
    print("⚠ 图表质量基本合格，但有改进空间")
else:
    print("✗ 图表质量存在严重问题，需要改进")

print("\n===== 图表改进建议 =====")
suggestions = []

if format_issues:
    suggestions.append("将所有图表转换为EPS或PDF格式，符合Nature期刊要求")
if avg_caption_score < 8:
    suggestions.append("改进图表说明文本，确保包含足够的细节和描述性语言")
if all_figs and unused_figs:
    suggestions.append("确保所有图表在正文中被适当引用")
if missing_files:
    suggestions.append("确保所有图表文件存在并正确命名")
if len(unique_topics) < 3 and len(figure_environments) >= 3:
    suggestions.append("增加图表主题多样性，涵盖更多核心概念")
if not float_options:
    suggestions.append("为图表添加适当的浮动位置选项，改善排版效果")
if not width_settings:
    suggestions.append("为图表设置合适的宽度，使用相对单位（如\textwidth）")

if suggestions:
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
else:
    print("✓ 图表方面无需重大改进")
