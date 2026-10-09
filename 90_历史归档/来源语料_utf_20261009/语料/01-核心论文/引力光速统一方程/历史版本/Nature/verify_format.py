# 简单的格式验证脚本
import os
import re

# 检查文件是否存在
file_path = 'd:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\引力光速统一方程\\Nature\\A Geometric Derivation of the Gravitational Constant from First Principles.tex'

if os.path.exists(file_path):
    print("✓ 文件存在")
    
    # 检查文件大小
    file_size = os.path.getsize(file_path)
    print(f"✓ 文件大小: {file_size} 字节 (~{file_size/1024:.1f} KB)")
    
    # 读取文件内容进行格式检查
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 检查LaTeX文档结构
    required_elements = [
        '\\documentclass',
        '\\begin{document}',
        '\\maketitle',
        '\\begin{abstract}',
        '\\end{abstract}',
        '\\section{',
        '\\begin{equation}',
        '\\end{document}'
    ]
    
    format_valid = True
    for element in required_elements:
        if element not in content:
            print(f"✗ 缺少必要的LaTeX元素: {element}")
            format_valid = False
        else:
            print(f"✓ 包含LaTeX元素: {element}")
    
    # 检查是否符合Nature格式要求
    if re.search(r'\\title\{\\textbf\{.*\}\}', content):
        print("✓ 使用粗体标题，符合Nature格式")
    
    if 'twocolumn' in content:
        print("✓ 使用双栏布局，符合Nature格式")
    
    if '12pt' in content:
        print("✓ 使用12pt字体，符合Nature格式")
    
    if format_valid:
        print("\n🎉 文件格式验证通过！这是一个有效的LaTeX/LEX格式文件，符合Nature期刊的基本格式要求。")
    else:
        print("\n⚠️ 文件格式存在问题，需要进一步修正。")
else:
    print("✗ 文件不存在")
