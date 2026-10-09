# 参考文献评估脚本
import re
import datetime

# 读取论文内容
with open('A Geometric Derivation of the Gravitational Constant from First Principles.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("===== 参考文献评估报告 =====\n")

# 1. 参考文献基本信息
print("1. 参考文献基本信息:")

# 提取参考文献环境内容
if '\\begin{thebibliography}' in content and '\\end{thebibliography}' in content:
    bib_env = re.search(r'\\begin{thebibliography}.*?\\end{thebibliography}', content, re.DOTALL)
    if bib_env:
        bib_content = bib_env.group(0)
        
        # 提取所有参考文献条目
        bib_entries = re.findall(r'\\bibitem\{([^\}]*)\}(.*?)(?=\\bibitem|\\end{thebibliography})', bib_content, re.DOTALL)
        print(f"   ✓ 参考文献总数: {len(bib_entries)}")
        
        # 统计引用次数
        citations = re.findall(r'\\cite\{([^\}]*)\}', content)
        cited_keys = set()
        citation_count = {}
        
        for cite in citations:
            keys = cite.split(',')
            for key in keys:
                key = key.strip()
                cited_keys.add(key)
                citation_count[key] = citation_count.get(key, 0) + 1
        
        print(f"   ✓ 论文中引用次数: {len(citations)} 次")
        print(f"   ✓ 被引用的参考文献数: {len(cited_keys)} 篇")
        
        # 检查未引用的参考文献
        all_bib_keys = {entry[0] for entry in bib_entries}
        unused_refs = all_bib_keys - cited_keys
        if unused_refs:
            print(f"   ⚠ 未被引用的参考文献: {len(unused_refs)} 篇 ({', '.join(unused_refs)})")
        else:
            print("   ✓ 所有参考文献均被合理引用")
        
        # 检查引用频率
        high_cited = [key for key, count in citation_count.items() if count >= 3]
        if high_cited:
            print(f"   ✓ 被多次引用的核心文献: {', '.join(high_cited)}")
        
else:
    print("   ✗ 未找到标准参考文献环境")
    bib_entries = []
    cited_keys = set()

# 2. 参考文献时效性分析
print("\n2. 参考文献时效性分析:")

current_year = datetime.datetime.now().year
publication_years = []

for entry in bib_entries:
    # 尝试提取年份（多种格式）
    year_match = re.search(r'(?:\b|\()(19[5-9]\d|20[0-2]\d)(?:\b|\))', entry[1])
    if year_match:
        year = int(year_match.group(1))
        publication_years.append(year)

if publication_years:
    avg_year = sum(publication_years) / len(publication_years)
    min_year = min(publication_years)
    max_year = max(publication_years)
    
    recent_refs = [year for year in publication_years if current_year - year <= 10]
    
    print(f"   ✓ 参考文献平均发表年份: {avg_year:.1f}")
    print(f"   ✓ 最早文献年份: {min_year}")
    print(f"   ✓ 最新文献年份: {max_year}")
    print(f"   ✓ 近10年内发表的文献: {len(recent_refs)}/{len(bib_entries)} ({len(recent_refs)/len(bib_entries)*100:.1f}%)")
    
    if len(recent_refs) / len(bib_entries) >= 0.5:
        print("   ✓ 参考文献时效性良好，包含足够的最新研究")
    else:
        print("   ⚠ 参考文献可能缺乏足够的最新研究")
    
    if max_year >= current_year - 5:
        print("   ✓ 包含近5年内的研究成果")
    else:
        print("   ⚠ 未包含近5年内的研究成果")
else:
    print("   ⚠ 无法提取参考文献年份信息")

# 3. 参考文献来源多样性
print("\n3. 参考文献来源多样性:")

# 尝试识别期刊、会议、书籍等
journal_keywords = ['Nature', 'Science', 'Phys\. Rev\.', 'J\. Phys\.', 'Physica', 'Astronomy', 'Astrophysics']
conference_keywords = ['Conference', 'Symposium', 'Workshop', 'Meeting', 'Proceedings']
book_keywords = ['Book', 'Textbook', 'Monograph']
preprint_keywords = ['arXiv', 'preprint']

journal_count = 0
conference_count = 0
book_count = 0
preprint_count = 0
other_count = 0

for entry in bib_entries:
    entry_text = entry[1].lower()
    entry_type = 'other'
    
    if any(kw.lower() in entry_text for kw in preprint_keywords):
        preprint_count += 1
        entry_type = 'preprint'
    elif any(kw.lower() in entry_text for kw in journal_keywords):
        journal_count += 1
        entry_type = 'journal'
    elif any(kw.lower() in entry_text for kw in conference_keywords):
        conference_count += 1
        entry_type = 'conference'
    elif any(kw.lower() in entry_text for kw in book_keywords):
        book_count += 1
        entry_type = 'book'
    else:
        other_count += 1

print(f"   ✓ 期刊论文: {journal_count}")
print(f"   ✓ 会议论文: {conference_count}")
print(f"   ✓ 书籍: {book_count}")
print(f"   ✓ 预印本: {preprint_count}")
print(f"   ✓ 其他来源: {other_count}")

if journal_count >= 5:
    print("   ✓ 包含足够的期刊论文引用")
else:
    print("   ⚠ 期刊论文引用可能不足")

if preprint_count / len(bib_entries) if bib_entries else 0 <= 0.3:
    print("   ✓ 预印本比例在合理范围内")
else:
    print("   ⚠ 预印本比例较高，建议更多引用已发表文献")

# 4. 参考文献格式规范性
print("\n4. 参考文献格式规范性:")

format_scores = []
format_issues = []

for key, entry_text in bib_entries:
    entry_score = 10
    
    # 检查作者信息
    if not re.search(r'[A-Z][a-z]+\s+(?:[A-Z]\.)+', entry_text):
        entry_score -= 3
        if 'author format' not in format_issues:
            format_issues.append('author format')
    
    # 检查年份信息
    if not re.search(r'(?:\b|\()(19[5-9]\d|20[0-2]\d)(?:\b|\))', entry_text):
        entry_score -= 2
        if 'year missing' not in format_issues:
            format_issues.append('year missing')
    
    # 检查标题信息
    if not re.search(r'"[^"\n]+"|[A-Z][a-z][^.]*\.', entry_text):
        entry_score -= 2
        if 'title missing' not in format_issues:
            format_issues.append('title missing')
    
    # 检查期刊/会议信息
    if not (any(kw in entry_text for kw in journal_keywords) or any(kw in entry_text for kw in conference_keywords)):
        entry_score -= 2
        if 'publication info missing' not in format_issues:
            format_issues.append('publication info missing')
    
    # 检查页码或DOI
    if not (re.search(r'\d+–\d+', entry_text) or re.search(r'DOI', entry_text, re.IGNORECASE)):
        entry_score -= 1
        if 'page/doi missing' not in format_issues:
            format_issues.append('page/doi missing')
    
    format_scores.append(entry_score)

avg_format_score = sum(format_scores) / len(format_scores) if format_scores else 0

print(f"   ✓ 参考文献平均格式评分: {avg_format_score:.1f}/10")

if avg_format_score >= 8:
    print("   ✓ 参考文献格式较为规范")
elif avg_format_score >= 5:
    print("   ⚠ 参考文献格式存在一些不规范之处")
else:
    print("   ✗ 参考文献格式存在严重不规范问题")

if format_issues:
    print("   主要格式问题:")
    for issue in format_issues:
        print(f"     - {issue}")

# 5. 参考文献相关性评估
print("\n5. 参考文献相关性评估:")

# 检查核心主题的参考文献覆盖
core_topics = [
    ('Gravitational Constant', 'G|gravity|gravitational constant'),
    ('Speed of Light', 'c|speed of light|light speed'),
    ('General Relativity', 'relativity|Einstein|general relativity'),
    ('Quantum Gravity', 'quantum gravity|gravitons|quantum'),
    ('Geometric Physics', 'geometric|geometry|spacetime'),
    ('Unified Theories', 'unification|unified|theory of everything')
]

topic_coverage = []
for topic_name, regex_pattern in core_topics:
    pattern = re.compile(regex_pattern, re.IGNORECASE)
    matched_entries = [entry for key, entry in bib_entries if pattern.search(entry)]
    if len(matched_entries) >= 2:
        coverage = 'good'
        mark = '✓'
    elif len(matched_entries) >= 1:
        coverage = 'moderate'
        mark = '⚠'
    else:
        coverage = 'poor'
        mark = '✗'
    
    topic_coverage.append((topic_name, len(matched_entries), coverage, mark))
    print(f"   {mark} {topic_name}: {len(matched_entries)} 篇参考文献")

# 检查引用核心文献
if 'Einstein' in content or 'Newton' in content:
    print("   ✓ 引用了物理学领域的核心人物的研究")
else:
    print("   ⚠ 可能未引用足够的物理学核心文献")

# 6. 自引用检查
print("\n6. 自引用检查:")

# 简单检查作者名或机构名在参考文献中的重复出现
self_cite_patterns = ['author', 'institution', 'our previous work']
self_cite_count = 0

for key, entry in bib_entries:
    if any(pattern.lower() in entry.lower() for pattern in self_cite_patterns):
        self_cite_count += 1

if self_cite_count > 0:
    print(f"   ⚠ 可能包含 {self_cite_count} 篇自引用文献")
    if self_cite_count / len(bib_entries) > 0.3:
        print("   ⚠ 自引用比例较高，可能影响学术客观性")
else:
    print("   ✓ 未检测到明显的自引用")

# 7. 参考文献完整性评分
print("\n===== 参考文献完整性综合评分 =====")

# 评分系统 (0-100)
score = 100

# 数量评分
if len(bib_entries) < 5:
    score -= 30
    print("✗ 参考文献数量过少 (-30)")
elif len(bib_entries) < 10:
    score -= 10
    print("⚠ 参考文献数量略少 (-10)")

# 引用完整性
if unused_refs:
    score -= 10
    print(f"⚠ 存在未引用的参考文献 (-10)")

# 时效性评分
if publication_years:
    if len(recent_refs) / len(bib_entries) < 0.3:
        score -= 15
        print("✗ 缺乏足够的最新研究文献 (-15)")
    elif len(recent_refs) / len(bib_entries) < 0.5:
        score -= 5
        print("⚠ 最新研究文献比例偏低 (-5)")

# 格式评分
if avg_format_score < 5:
    score -= 20
    print("✗ 参考文献格式严重不规范 (-20)")
elif avg_format_score < 8:
    score -= 10
    print("⚠ 参考文献格式存在不规范之处 (-10)")

# 主题覆盖评分
poor_topics = [topic for topic, count, coverage, mark in topic_coverage if coverage == 'poor']
if len(poor_topics) > 2:
    score -= 15
    print(f"✗ 多个核心主题缺乏相关参考文献 (-15)")
elif len(poor_topics) > 0:
    score -= 5
    print(f"⚠ 部分核心主题参考文献覆盖不足 (-5)")

# 自引用评分
if self_cite_count / len(bib_entries) if bib_entries else 0 > 0.3:
    score -= 10
    print("⚠ 自引用比例过高 (-10)")

# 加分项
if journal_count >= 5:
    score += 5
    print("✓ 包含足够的高质量期刊文献 (+5)")
if len(topic_coverage) - len(poor_topics) >= 4:
    score += 5
    print("✓ 核心主题参考文献覆盖良好 (+5)")
if avg_format_score >= 8:
    score += 5
    print("✓ 参考文献格式规范 (+5)")

score = max(0, min(100, score))  # 确保分数在0-100之间

print(f"\n最终参考文献评分: {score}/100")

if score >= 80:
    print("✓ 参考文献整体质量良好，符合学术发表要求")
elif score >= 60:
    print("⚠ 参考文献基本符合要求，但有改进空间")
else:
    print("✗ 参考文献存在严重问题，需要重大修改")

print("\n===== 参考文献改进建议 =====")
suggestions = []

if len(bib_entries) < 10:
    suggestions.append("增加参考文献数量，确保覆盖相关研究领域的重要成果")
if unused_refs:
    suggestions.append("移除未引用的参考文献，或在正文中适当引用它们")
if publication_years and len(recent_refs) / len(bib_entries) < 0.5:
    suggestions.append("增加近5年内发表的相关研究文献")
if avg_format_score < 8:
    suggestions.append("统一参考文献格式，确保包含作者、年份、标题、出版物等完整信息")
if poor_topics:
    suggestions.append(f"增加与以下主题相关的参考文献: {', '.join(poor_topics)}")
if self_cite_count / len(bib_entries) if bib_entries else 0 > 0.3:
    suggestions.append("减少自引用比例，增加引用其他研究者的工作")

if suggestions:
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
else:
    print("✓ 参考文献方面无需重大改进")
