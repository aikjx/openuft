import re

# 读取原始文件
with open('d:\\a10\\aikjx\\code\\my_lib\\utf\\10-统一场论核心公式\\公式验证论文\\24-时空与物理常数归一化方程\\可转换的\\归一化方程转换4.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 需要移除的方程模式
# 1. 手性正反物质统一方程2
pattern1 = r'\$\$\\boxed\{m_{\\pm} = m = \\frac{\\|\\omega\\|^2 r^3}{G}\} \$\$'

# 2. 真空零点能归一化方程
pattern2 = r'\$\$\\boxed\{\\rho_{vac} = \\frac{c^7}{4\\pi G^2 h} = \\frac{3 H^2 c^2}{8\\pi G}\} \$\$'

# 3. 粒子质量谱量子化方程1
pattern3 = r'\$\$\\boxed\{m_n = \\sqrt{n} \\cdot m_p\} \$\$'

# 4. 粒子质量谱量子化方程2
pattern4 = r'\$\$\\boxed\{r_n = \\sqrt{n} \\cdot l_p\} \$\$'

# 5. 引力-电磁辐射统一方程1
pattern5 = r'\$\$\\boxed\{\\frac{c^2}{G} \\cdot \\frac{d^2 r}{dt^2} = \\frac{1}{4\\pi \\varepsilon_0} \\cdot \\frac{d^2 e}{dt^2}\} \$\$'

# 6. 宇宙基本常数全归一化超恒等式
pattern6 = r'\$\$\\boxed\{\\frac{4\\pi^2 r^3 c^2}{G T^2 h \\nu} = \\frac{e^2}{4\\pi \\varepsilon_0 \\alpha \\hbar c} = \\frac{k_B T_{temp}}{h \\nu} = c^2 \\mu_0 \\varepsilon_0 = \\gamma \\sqrt{1-\\frac{v^2}{c^2}} = 1\} \$\$'

# 移除方程
modified_content = content
modified_content = re.sub(pattern1, '', modified_content)
modified_content = re.sub(pattern2, '', modified_content)
modified_content = re.sub(pattern3, '', modified_content)
modified_content = re.sub(pattern4, '', modified_content)
modified_content = re.sub(pattern5, '', modified_content)
modified_content = re.sub(pattern6, '', modified_content)

# 移除空的公式部分
modified_content = re.sub(r'## 核心原创公式.*?---', '---', modified_content, flags=re.DOTALL)

# 保存修正后的文件
with open('d:\\a10\\aikjx\\code\\my_lib\\utf\\10-统一场论核心公式\\公式验证论文\\24-时空与物理常数归一化方程\\可转换的\\归一化方程转换4_corrected.md', 'w', encoding='utf-8') as f:
    f.write(modified_content)

print("已移除量纲不正确的方程并生成修正后的文件")
