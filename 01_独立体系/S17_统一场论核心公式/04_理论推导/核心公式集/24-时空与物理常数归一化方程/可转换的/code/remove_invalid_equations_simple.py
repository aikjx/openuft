# 读取原始文件
with open('d:\\a10\\aikjx\\code\\my_lib\\utf\\10-统一场论核心公式\\公式验证论文\\24-时空与物理常数归一化方程\\可转换的\\归一化方程转换4.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 需要移除的方程行
invalid_equations = [
    '$$\\boxed{m_{\\pm} = m = \\frac{|\\omega|^2 r^3}{G}}$$',
    '$$\\boxed{\\rho_{vac} = \\frac{c^7}{4\\pi G^2 h} = \\frac{3 H^2 c^2}{8\\pi G}}$$',
    '$$\\boxed{m_n = \\sqrt{n} \\cdot m_p}$$',
    '$$\\boxed{r_n = \\sqrt{n} \\cdot l_p}$$',
    '$$\\boxed{\\frac{c^2}{G} \\cdot \\frac{d^2 r}{dt^2} = \\frac{1}{4\\pi \\varepsilon_0} \\cdot \\frac{d^2 e}{dt^2}}$$',
    '$$\\boxed{\\frac{4\\pi^2 r^3 c^2}{G T^2 h \\nu} = \\frac{e^2}{4\\pi \\varepsilon_0 \\alpha \\hbar c} = \\frac{k_B T_{temp}}{h \\nu} = c^2 \\mu_0 \\varepsilon_0 = \\gamma \\sqrt{1-\\frac{v^2}{c^2}} = 1}$$'
]

# 过滤掉无效方程
filtered_lines = []
for line in lines:
    if not any(eq in line for eq in invalid_equations):
        filtered_lines.append(line)

# 保存修正后的文件
with open('d:\\a10\\aikjx\\code\\my_lib\\utf\\10-统一场论核心公式\\公式验证论文\\24-时空与物理常数归一化方程\\可转换的\\归一化方程转换4_corrected.md', 'w', encoding='utf-8') as f:
    f.writelines(filtered_lines)

print("已移除量纲不正确的方程并生成修正后的文件")
