import os

# 定义要处理的目录
directory = r"d:\a10\aikjx\code\my_lib\utf\01-核心论文\数学论文"

# 定义需要转换的LaTeX命令和符号
# 使用简单的替换映射，避免复杂的正则表达式
latex_replacements = [
    # 常见LaTeX命令
    ('frac{', '\\frac{'),
    ('binom{', '\\binom{'),
    ('sqrt{', '\\sqrt{'),
    ('sum{', '\\sum{'),
    ('prod{', '\\prod{'),
    ('int{', '\\int{'),
    ('lim{', '\\lim{'),
    ('max{', '\\max{'),
    ('min{', '\\min{'),
    ('vec{', '\\vec{'),
    ('mathbf{', '\\mathbf{'),
    
    # 数学函数
    ('\\ln', '\\ln'),  # 已经是正确格式
    ('\\sin', '\\sin'),
    ('\\cos', '\\cos'),
    ('\\tan', '\\tan'),
    ('\\exp', '\\exp'),
    ('ln ', '\\ln '),
    ('sin ', '\\sin '),
    ('cos ', '\\cos '),
    ('tan ', '\\tan '),
    ('exp ', '\\exp '),
    
    # 希腊字母
    ('alpha', '\\alpha'),
    ('beta', '\\beta'),
    ('gamma', '\\gamma'),
    ('delta', '\\delta'),
    ('epsilon', '\\epsilon'),
    ('zeta', '\\zeta'),
    ('eta', '\\eta'),
    ('theta', '\\theta'),
    ('iota', '\\iota'),
    ('kappa', '\\kappa'),
    ('lambda', '\\lambda'),
    ('mu', '\\mu'),
    ('nu', '\\nu'),
    ('xi', '\\xi'),
    ('omicron', '\\omicron'),
    ('pi', '\\pi'),
    ('rho', '\\rho'),
    ('sigma', '\\sigma'),
    ('tau', '\\tau'),
    ('upsilon', '\\upsilon'),
    ('phi', '\\phi'),
    ('chi', '\\chi'),
    ('psi', '\\psi'),
    ('omega', '\\omega'),
    ('Delta', '\\Delta'),
    
    # 其他数学符号
    ('nabla', '\\nabla'),
    ('infty', '\\infty'),
    ('partial', '\\partial'),
    ('Re', '\\text{Re}'),
]

def process_file(file_path):
    """处理单个文件，将公式转换为LaTeX格式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 保存原始内容，用于比较是否有修改
        original_content = content
        
        # 只处理公式环境内的内容
        # 先找到所有公式块 $$...$$
        lines = content.split('\n')
        in_block_formula = False
        new_lines = []
        
        for line in lines:
            # 检查是否在块公式环境中
            if '$$' in line:
                parts = line.split('$$')
                processed_line = ''
                for i, part in enumerate(parts):
                    if i % 2 == 1:  # 公式部分
                        # 处理公式内容
                        formula_part = part
                        for old, new in latex_replacements:
                            formula_part = formula_part.replace(old, new)
                        processed_line += '$$' + formula_part + '$$'
                    else:  # 非公式部分
                        processed_line += part
                new_lines.append(processed_line)
            else:
                # 处理行内公式 $...$
                if '$' in line:
                    parts = line.split('$')
                    processed_line = ''
                    for i, part in enumerate(parts):
                        if i % 2 == 1:  # 公式部分
                            # 处理公式内容
                            formula_part = part
                            for old, new in latex_replacements:
                                formula_part = formula_part.replace(old, new)
                            processed_line += '$' + formula_part + '$'
                        else:  # 非公式部分
                            processed_line += part
                    new_lines.append(processed_line)
                else:
                    new_lines.append(line)
        
        # 重新组合内容
        content = '\n'.join(new_lines)
        
        # 检查是否有修改
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已更新文件: {file_path}")
        else:
            print(f"文件无需更新: {file_path}")
            
    except Exception as e:
        print(f"处理文件时出错 {file_path}: {str(e)}")

def main():
    """遍历目录中的所有.md文件并处理"""
    # 确保目录存在
    if not os.path.exists(directory):
        print(f"目录不存在: {directory}")
        return
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # 使用os.path.normpath确保路径格式正确
                file_path = os.path.normpath(os.path.join(root, file))
                process_file(file_path)

if __name__ == "__main__":
    main()
    print("\n所有.md文件中的数学公式已转换为标准LaTeX格式！")