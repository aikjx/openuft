# LaTeX文件可编译性检查脚本
import os
import re

# 设置论文文件路径
tex_file = 'A Geometric Derivation of the Gravitational Constant from First Principles.tex'

# 检查文件是否存在
if os.path.exists(tex_file):
    print(f"✓ LaTeX文件 '{tex_file}' 存在")
    
    # 读取文件内容
    with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 检查LaTeX文档结构完整性
    structure_checks = [
        ('\\documentclass', '文档类声明'),
        ('\\begin{document}', '文档开始'),
        ('\\end{document}', '文档结束'),
        ('\\begin{abstract}', '摘要开始'),
        ('\\end{abstract}', '摘要结束'),
        ('\\maketitle', '标题生成命令'),
    ]
    
    all_structure_ok = True
    for command, description in structure_checks:
        if content.count(command) < 1:
            print(f"✗ 缺少{description}: {command}")
            all_structure_ok = False
    
    # 检查括号匹配
    def check_brackets(text):
        bracket_pairs = {
            '(': ')',
            '[': ']',
            '{': '}'
        }
        stack = []
        for i, char in enumerate(text):
            if char in bracket_pairs:
                stack.append((char, i))
            elif char in bracket_pairs.values():
                if not stack:
                    line_num = text[:i].count('\n')+1
                    return False, f"行 {line_num}: 多余的结束括号 '{char}'"
                opening, _ = stack.pop()
                if bracket_pairs[opening] != char:
                    line_num = text[:i].count('\n')+1
                    return False, f"行 {line_num}: 括号不匹配: '{opening}' 和 '{char}'"
        if stack:
            opening, pos = stack[-1]
            line = text[:pos].count('\n')+1
            return False, f"行 {line}: 未闭合的括号 '{opening}'"
        return True, "所有括号匹配正常"
    
    brackets_ok, brackets_msg = check_brackets(content)
    if not brackets_ok:
        print(f"✗ 括号匹配错误: {brackets_msg}")
        all_structure_ok = False
    else:
        print(f"✓ {brackets_msg}")
    
    # 检查图片引用
    image_refs = re.findall(r'\\\\includegraphics\\[.*?\\]\\{(.*?)\\}', content)
    if image_refs:
        print(f"✓ 找到 {len(image_refs)} 个图片引用")
        for img in image_refs:
            if os.path.exists(img) or os.path.exists(f"{img}.png") or os.path.exists(f"{img}.pdf"):
                print(f"  ✓ 图片 '{img}' 文件存在")
            else:
                print(f"  ⚠ 图片 '{img}' 文件未找到，但编译时可能会自动处理")
    
    # 检查公式环境
    eq_start_count = content.count('\\\\begin{equation}')
    eq_end_count = content.count('\\\\end{equation}')
    if eq_start_count == eq_end_count:
        print(f"✓ 公式环境匹配: {eq_start_count} 个公式环境")
    else:
        print(f"✗ 公式环境不匹配: {eq_start_count} 个开始，{eq_end_count} 个结束")
        all_structure_ok = False
    
    # 检查引用
    cite_count = content.count('\\\\cite{')
    bibitem_count = content.count('\\\\bibitem{')
    print(f"✓ 参考文献项目数: {bibitem_count}")
    if cite_count > 0:
        print(f"✓ 引用数: {cite_count}")
    
    # 最终评估
    if all_structure_ok:
        print("\n🎉 LaTeX文件结构完整，应该可以正常编译！")
        print("建议使用以下命令进行实际编译:")
        print("  pdflatex 'A Geometric Derivation of the Gravitational Constant from First Principles.tex'")
        print("  pdflatex 'A Geometric Derivation of the Gravitational Constant from First Principles.tex'")  # 再次运行以解析引用
    else:
        print("\n⚠️ LaTeX文件结构存在问题，需要修复后才能正常编译。")
else:
    print(f"✗ 错误: LaTeX文件 '{tex_file}' 不存在")
