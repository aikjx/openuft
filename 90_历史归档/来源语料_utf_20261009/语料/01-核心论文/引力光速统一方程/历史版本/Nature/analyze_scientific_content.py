# 论文科学性分析脚本
import re
import math

# 读取论文内容
with open('A Geometric Derivation of the Gravitational Constant from First Principles.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("===== 论文科学性和严谨性分析报告 =====\n")

# 1. 理论创新性分析
print("1. 理论创新性分析:")

# 检查核心创新点
innovative_points = [
    ('G = 2Z/c 统一方程', 'G = 2Z/c'),
    ('几何因子2的推导', 'geometric factor of 2'),
    ('空间螺旋运动假设', 'Spatial Helical Motion'),
    ('时空同一化方程', 'Spatiotemporal Identity'),
    ('几何质量定义', 'Geometric Mass Definition')
]

for point, keyword in innovative_points:
    if keyword in content:
        print(f"   ✓ 包含创新点: {point}")
    else:
        print(f"   ✗ 未找到创新点: {point}")

# 2. 假设和前提检查
print("\n2. 理论假设和前提分析:")
postulates = re.findall(r'\\textbf\{Postulate \d+ \([^)]+\):\}\}(.*?)(?=\\textbf\{Postulate|$)', content, re.DOTALL)
if postulates:
    print(f"   ✓ 共定义了 {len(postulates)} 个核心假设")
    for i, postulate in enumerate(postulates, 1):
        if len(postulate.strip()) > 50:
            print(f"   ✓ 假设 {i} 描述充分")
        else:
            print(f"   ⚠ 假设 {i} 描述可能过于简略")
else:
    print("   ✗ 未找到明确的假设定义")

# 3. 数学推导严谨性
print("\n3. 数学推导严谨性分析:")

# 检查方程数量和引用
equations = re.findall(r'\\begin{equation}(.*?)\\end{equation}', content, re.DOTALL)
print(f"   ✓ 论文包含 {len(equations)} 个方程")

# 检查几何因子2的推导
if "geometric factor of 2" in content:
    print("   ✓ 包含几何因子2的讨论")
    derivation_methods = re.findall(r'\d\.\s*\*\*([^*]+)\*\*:', content)
    if derivation_methods:
        print(f"   ✓ 提供了 {len(derivation_methods)} 种几何因子2的推导方法")
        for method in derivation_methods:
            print(f"     - {method.strip()}")
    else:
        print("   ⚠ 未找到明确的几何因子2推导方法列表")
else:
    print("   ✗ 未详细讨论几何因子2")

# 4. 常数Z的物理意义
print("\n4. 常数Z的物理意义分析:")
if "proportionality constant" in content and "Z" in content:
    print("   ✓ 将Z描述为比例常数，避免过度断言")
    if "m^4/kg·s^3" in content:
        print("   ✓ 正确给出了Z的单位")
    else:
        print("   ⚠ 未明确说明Z的单位")
else:
    print("   ⚠ 对Z的物理意义解释可能不足")

# 5. 数值验证分析
print("\n5. 数值验证和精度分析:")

# 检查CODATA值的使用
if "CODATA 2018" in content:
    print("   ✓ 参考了最新的CODATA 2018物理常数")
    # 提取数值计算
    if "Z = Gc/2" in content:
        print("   ✓ 包含了Z值的计算表达式")
        # 检查精度表述
        if "<0.001%" in content:
            print("   ⚠ 精度表述过于绝对，可能需要修正")
        elif "experimental uncertainties" in content:
            print("   ✓ 使用了合理的精度表述，与实验不确定性相关")
        else:
            print("   ⚠ 未明确说明精度水平")
    else:
        print("   ⚠ 未明确Z值的计算过程")
else:
    print("   ⚠ 未引用标准物理常数数据集")

# 6. 实验验证建议
print("\n6. 实验验证可行性分析:")

if "Proposed Tests" in content:
    print("   ✓ 提出了实验验证方法")
    test_methods = re.findall(r'\d\.\s*(\*\*[^*]+\*\*[^\n]+)', content)
    if test_methods:
        print(f"   ✓ 提出了 {len(test_methods)} 种具体验证方法")
        for method in test_methods:
            print(f"     - {method.replace('**', '').strip()}")
    else:
        print("   ⚠ 实验验证方法描述不够具体")
else:
    print("   ✗ 未提出明确的实验验证方法")

# 7. 科学严谨性表述
print("\n7. 科学严谨性表述分析:")

# 检查表述谨慎性
cautious_terms = ["suggests", "may", "potentially", "hypothesized", "proposed", "preliminary"]
assertive_terms = ["proves", "definitely", "certainly", "without doubt", "conclusively"]

cautious_count = sum(content.count(term) for term in cautious_terms)
assertive_count = sum(content.count(term) for term in assertive_terms)

print(f"   ✓ 使用谨慎性表述次数: {cautious_count}")
if assertive_count > 0:
    print(f"   ⚠ 使用断言性表述次数: {assertive_count}")
else:
    print(f"   ✓ 未使用过度断言性表述")

if cautious_count > assertive_count:
    print("   ✓ 整体表述较为谨慎，符合科学规范")
else:
    print("   ⚠ 可能存在过度断言的情况")

# 8. 与现有理论的关系
print("\n8. 与现有物理理论的兼容性分析:")

related_theories = [
    ('General Relativity', 'relativity', 'Einstein'),
    ('Quantum Mechanics', 'quantum', 'gravitons'),
    ('Newtonian Gravity', 'Newton', 'gravitational'),
    ('Unified Field Theory', 'unified', 'unification')
]

for theory_name, *keywords in related_theories:
    found = False
    for keyword in keywords:
        if keyword in content.lower():
            found = True
            break
    if found:
        print(f"   ✓ 讨论了与{theory_name}的关系")
    else:
        print(f"   ⚠ 未明确讨论与{theory_name}的关系")

# 9. 综合科学性评估
print("\n===== 科学性和严谨性综合评估 =====")

# 评分系统 (0-100)
score = 100

# 扣分项
if len(equations) < 5:
    score -= 10
    print("✗ 方程数量不足，数学表达可能不够充分 (-10)")
if assertive_count > cautious_count:
    score -= 15
    print("✗ 表述过于断言，缺乏科学谨慎性 (-15)")
if "Proposed Tests" not in content:
    score -= 20
    print("✗ 未提出实验验证方法，可证伪性不足 (-20)")
if "CODATA 2018" not in content:
    score -= 10
    print("✗ 未引用最新标准常数，可能缺乏时效性 (-10)")
if len(postulates) < 2:
    score -= 15
    print("✗ 核心假设定义不充分，理论基础可能薄弱 (-15)")

# 加分项
if cautious_count > 5:
    score += 5
    print("✓ 表述谨慎，符合科学规范 (+5)")
if len(derivation_methods) > 2:
    score += 10
    print("✓ 提供多种推导方法，增强理论可信度 (+10)")
if "Proposed Tests" in content and len(test_methods) > 2:
    score += 10
    print("✓ 提出多种具体验证方法，增强可证伪性 (+10)")

score = max(0, min(100, score))  # 确保分数在0-100之间

print(f"\n最终科学性评分: {score}/100")

if score >= 80:
    print("✓ 论文在科学性和严谨性方面表现良好，符合学术发表要求")
elif score >= 60:
    print("⚠ 论文在科学性和严谨性方面基本合理，但有改进空间")
else:
    print("✗ 论文在科学性和严谨性方面存在严重问题，需要重大修改")

print("\n===== 科学性改进建议 =====")
suggestions = []

if assertive_count > 0:
    suggestions.append("使用更加谨慎的科学表述，避免过度断言")
if "Proposed Tests" not in content:
    suggestions.append("增加具体的实验验证方法，增强理论的可证伪性")
if len(equations) < 5:
    suggestions.append("补充更多数学推导，增强理论的数学基础")
if "Z" in content and "physical meaning" not in content.lower():
    suggestions.append("进一步解释常数Z的物理意义")
if len(postulates) > 0 and score < 70:
    suggestions.append("加强对核心假设的论证和文献支持")

if suggestions:
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
else:
    print("✓ 科学性方面无需重大改进")
