# 论文语言表达和专业术语分析脚本
import re
import string

# 读取论文内容
with open('A Geometric Derivation of the Gravitational Constant from First Principles.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("===== 语言表达和专业术语分析报告 =====\n")

# 1. 基本语言统计
print("1. 基本语言统计:")

# 移除LaTeX命令和环境，获取纯文本
plain_text = re.sub(r'\\begin\{[^}]*\}|\\end\{[^}]*\}', '', content)
plain_text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', plain_text)
plain_text = re.sub(r'\\[a-zA-Z]+', '', plain_text)
plain_text = re.sub(r'\$[^$]*\$', '', plain_text)  # 移除数学公式
plain_text = re.sub(r'%.*\n', '\n', plain_text)  # 移除注释
plain_text = re.sub(r'\s+', ' ', plain_text).strip()  # 标准化空白

# 计算单词数
words = plain_text.split()
word_count = len(words)
print(f"   ✓ 估计单词数: {word_count}")

# 计算句子数（简单估计）
sentences = re.split(r'[.!?]+', plain_text)
sentence_count = len([s for s in sentences if s.strip()])
print(f"   ✓ 估计句子数: {sentence_count}")

if sentence_count > 0:
    avg_words_per_sentence = word_count / sentence_count
    print(f"   ✓ 平均句长: {avg_words_per_sentence:.1f} 个单词")
    
    if 15 <= avg_words_per_sentence <= 25:
        print("   ✓ 平均句长适中，有利于阅读")
    elif avg_words_per_sentence > 30:
        print("   ⚠ 平均句长过长，可能影响可读性")
    else:
        print("   ⚠ 平均句长过短，可能影响学术表达的严谨性")

# 2. 专业术语使用分析
print("\n2. 专业术语使用分析:")

# 物理学术语库
physics_terms = {
    'gravitational constant': {'G', 'gravitational constant', 'Newtonian constant of gravitation'},
    'speed of light': {'c', 'speed of light', 'light speed', 'speed of electromagnetic waves'},
    'spacetime': {'spacetime', 'space-time', 'four-dimensional space'},
    'relativity': {'relativity', 'general relativity', 'special relativity', 'Einstein'},
    'quantum': {'quantum', 'quantum mechanics', 'quantum gravity', 'gravitons'},
    'geometry': {'geometry', 'geometric', 'curvature', 'metric tensor'},
    'unification': {'unification', 'unified field theory', 'grand unified theory'},
    'dimensions': {'dimension', '3D', '4D', 'higher dimensions'},
    'constants': {'physical constant', 'fundamental constant', 'natural constant'},
    'mathematics': {'equation', 'formula', 'derivation', 'theorem'}
}

# 检查术语使用
term_usage = {category: set() for category in physics_terms}
term_frequency = {category: 0 for category in physics_terms}

for category, terms in physics_terms.items():
    for term in terms:
        pattern = r'\\b' + re.escape(term) + r'\\b'
        matches = re.findall(pattern, plain_text, re.IGNORECASE)
        if matches:
            term_usage[category].add(term.lower())
            term_frequency[category] += len(matches)

# 显示术语使用情况
covered_categories = sum(1 for category, used in term_usage.items() if used)
print(f"   ✓ 覆盖的术语类别: {covered_categories}/{len(physics_terms)}")

print("   术语类别使用详情:")
for category, used_terms in term_usage.items():
    if used_terms:
        print(f"     ✓ {category}: 使用 {term_frequency[category]} 次 ({', '.join(used_terms)})")
    else:
        print(f"     ⚠ {category}: 未使用该类术语")

# 3. 语言清晰度和简洁性
print("\n3. 语言清晰度和简洁性:")

# 检查复杂词和冗余表达
complex_words = re.findall(r'\\b[a-z]{10,}\\b', plain_text.lower())
redundant_phrases = [
    ('in order to', 'to'),
    ('due to the fact that', 'because'),
    ('in terms of', ''),
    ('at this point in time', 'now'),
    ('with reference to', 'about'),
    ('it is important to note that', ''),
    ('as a matter of fact', ''),
    ('in the event that', 'if'),
    ('on account of', 'because'),
    ('with regard to', 'about')
]

redundancy_count = 0
for phrase, _ in redundant_phrases:
    redundancy_count += plain_text.lower().count(phrase)

print(f"   ✓ 长词数量(≥10个字母): {len(complex_words)}")
print(f"   ✓ 潜在冗余表达数量: {redundancy_count}")

if len(complex_words) / word_count * 100 if word_count else 0 <= 5:
    print("   ✓ 语言较为简洁，复杂词比例适中")
else:
    print("   ⚠ 复杂词比例较高，可能影响可读性")

if redundancy_count < 10:
    print("   ✓ 冗余表达较少，语言较为简洁")
else:
    print("   ⚠ 冗余表达较多，建议简化")

# 4. 语法和一致性检查
print("\n4. 语法和一致性检查:")

# 简单的一致性检查
tense_issues = []

# 检查时态一致性（简单示例）
present_tense = re.findall(r'\\b(?:is|are|exists|shows|demonstrates|suggests)\\b', plain_text.lower())
past_tense = re.findall(r'\\b(?:was|were|existed|showed|demonstrated|suggested)\\b', plain_text.lower())

print(f"   ✓ 现在时态动词使用: {len(present_tense)} 次")
print(f"   ✓ 过去时态动词使用: {len(past_tense)} 次")

if len(present_tense) > len(past_tense) * 2:
    print("   ✓ 主要使用现在时态，符合学术写作惯例")
elif len(past_tense) > len(present_tense) * 2:
    print("   ⚠ 过多使用过去时态，学术论文通常以现在时态为主")
else:
    print("   ⚠ 时态使用不够一致，建议统一")

# 检查术语拼写一致性
double_spellings = {
    'spacetime': ['spacetime', 'space-time', 'space time'],
    'coordinate': ['coordinate', 'co-ordinate'],
    'parameter': ['parameter', 'parametre'],
    'theoretical': ['theoretical', 'theoretic'],
    'analyze': ['analyze', 'analyse'],
    'center': ['center', 'centre'],
    'color': ['color', 'colour']
}

spelling_inconsistencies = []
for term, variants in double_spellings.items():
    found_variants = [variant for variant in variants if variant.lower() in plain_text.lower()]
    if len(found_variants) > 1:
        spelling_inconsistencies.append((term, found_variants))
        print(f"   ⚠ 术语拼写不一致: {term} 的变体 {', '.join(found_variants)}")

if not spelling_inconsistencies:
    print("   ✓ 未发现明显的术语拼写不一致")

# 5. 学术写作风格检查
print("\n5. 学术写作风格检查:")

# 检查人称使用
first_person = re.findall(r'\\b(?:I|we|our|us|my)\\b', plain_text, re.IGNORECASE)
passive_voice = re.findall(r'\\b(?:is|are|was|were)\\s+[a-z]+ed\\b', plain_text, re.IGNORECASE)

print(f"   ✓ 第一人称使用: {len(first_person)} 次")
print(f"   ✓ 被动语态使用: {len(passive_voice)} 次")

if len(first_person) < 10:
    print("   ✓ 第一人称使用较少，符合学术客观性要求")
else:
    print("   ⚠ 第一人称使用较多，可能影响学术客观性")

# 检查模糊表达
vague_expressions = ['some', 'many', 'several', 'a few', 'quite', 'rather', 'very', 'pretty', 'fairly']
vague_count = sum(plain_text.lower().count(exp) for exp in vague_expressions)

print(f"   ✓ 模糊表达使用: {vague_count} 次")

if vague_count / word_count * 100 if word_count else 0 <= 2:
    print("   ✓ 模糊表达使用适中")
else:
    print("   ⚠ 模糊表达使用较多，建议使用更精确的表述")

# 检查断言强度
strong_assertions = ['proves', 'definitely', 'certainly', 'undoubtedly', 'absolutely', 'unequivocally']
weak_assertions = ['suggests', 'indicates', 'may', 'might', 'could', 'potentially', 'appears']

strong_count = sum(plain_text.lower().count(assertion) for assertion in strong_assertions)
weak_count = sum(plain_text.lower().count(assertion) for assertion in weak_assertions)

print(f"   ✓ 强断言使用: {strong_count} 次")
print(f"   ✓ 谨慎表述使用: {weak_count} 次")

if strong_count == 0 or weak_count > strong_count:
    print("   ✓ 断言强度适中，符合科学严谨性要求")
else:
    print("   ⚠ 强断言使用过多，可能缺乏科学谨慎性")

# 6. 专业术语准确性检查
print("\n6. 专业术语准确性检查:")

# 检查常见术语错误或不当使用
term_issues = []

# 检查关键物理常数符号
if 'G' not in plain_text and 'gravitational constant' not in plain_text.lower():
    term_issues.append("缺少引力常数G的引用")
if 'c' not in plain_text and 'speed of light' not in plain_text.lower():
    term_issues.append("缺少光速c的引用")

# 检查单位表述
unit_terms = ['meters per second', 'm/s', 'kg', 'm', 's', 'Newton', 'N', 'joule', 'J']
unit_count = sum(plain_text.lower().count(unit) for unit in unit_terms)

print(f"   ✓ 物理单位使用: {unit_count} 次")

if not term_issues:
    print("   ✓ 未发现明显的专业术语使用错误")
else:
    print("   ⚠ 发现以下术语使用问题:")
    for issue in term_issues:
        print(f"     - {issue}")

# 7. 语言表达综合评分
print("\n===== 语言表达和术语使用综合评分 =====")

# 评分系统 (0-100)
score = 100

# 语言清晰度评分
if avg_words_per_sentence > 30 and sentence_count > 0:
    score -= 10
    print("✗ 句子过长，影响可读性 (-10)")
if len(complex_words) / word_count * 100 if word_count else 0 > 10:
    score -= 10
    print("✗ 复杂词过多，影响可读性 (-10)")
if redundancy_count > 15:
    score -= 10
    print("✗ 冗余表达过多 (-10)")

# 学术风格评分
if len(first_person) > 15:
    score -= 10
    print("✗ 第一人称使用过多，影响学术客观性 (-10)")
if strong_count > weak_count:
    score -= 10
    print("✗ 强断言过多，缺乏科学谨慎性 (-10)")
if vague_count / word_count * 100 if word_count else 0 > 5:
    score -= 5
    print("✗ 模糊表达过多 (-5)")

# 术语使用评分
if covered_categories < len(physics_terms) * 0.5:
    score -= 15
    print("✗ 专业术语覆盖不足 (-15)")
elif covered_categories < len(physics_terms) * 0.8:
    score -= 5
    print("⚠ 部分专业术语类别未覆盖 (-5)")

if spelling_inconsistencies:
    score -= len(spelling_inconsistencies) * 5
    print(f"✗ 术语拼写不一致 (-{len(spelling_inconsistencies)*5})")

if term_issues:
    score -= len(term_issues) * 10
    print(f"✗ 专业术语使用错误 (-{len(term_issues)*10})")

# 时态一致性评分
if len(present_tense) <= len(past_tense) and len(past_tense) <= len(present_tense):
    score -= 10
    print("✗ 时态使用不一致 (-10)")

# 加分项
if avg_words_per_sentence >= 15 and avg_words_per_sentence <= 25 and sentence_count > 0:
    score += 10
    print("✓ 句子长度适中，可读性良好 (+10)")
if weak_count > 10:
    score += 5
    print("✓ 使用了适当的谨慎表述，符合科学严谨性 (+5)")
if covered_categories == len(physics_terms):
    score += 10
    print("✓ 专业术语覆盖全面 (+10)")

score = max(0, min(100, score))  # 确保分数在0-100之间

print(f"\n最终语言表达评分: {score}/100")

if score >= 80:
    print("✓ 语言表达优秀，专业术语使用准确，符合学术发表要求")
elif score >= 60:
    print("⚠ 语言表达基本合格，但有改进空间")
else:
    print("✗ 语言表达存在严重问题，需要重大修改")

print("\n===== 语言表达改进建议 =====")
suggestions = []

if avg_words_per_sentence > 30 and sentence_count > 0:
    suggestions.append("将过长的句子拆分为更短的句子，提高可读性")
if redundancy_count > 10:
    suggestions.append("移除冗余表达，使语言更加简洁")
if len(first_person) > 10:
    suggestions.append("减少第一人称使用，增强学术客观性")
if strong_count > weak_count:
    suggestions.append("使用更多谨慎的科学表述，避免过度断言")
if spelling_inconsistencies:
    suggestions.append("统一术语拼写，确保一致性")
if covered_categories < len(physics_terms) * 0.7:
    suggestions.append("增加专业术语使用，提升学术深度")
if vague_count > word_count * 0.02 and word_count > 0:
    suggestions.append("减少模糊表达，使用更精确的描述")

if suggestions:
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
else:
    print("✓ 语言表达方面无需重大改进")
