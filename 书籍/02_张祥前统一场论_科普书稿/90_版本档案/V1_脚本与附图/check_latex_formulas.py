import os
import re
import glob

def check_latex_formulas():
    # 获取所有 Markdown 文件
    md_files = glob.glob('*.md')
    
    results = []
    
    # 公式相关的正则表达式
    # 查找可能的公式模式：数字+点+空格+公式内容，或者直接的数学表达式
    formula_patterns = [
        r'\d+\.\s*[^\n]+[=+\-*/][^\n]+',  # 1. E = mc² 这样的模式
        r'[A-Za-z]+\s*[=+\-*/][^\n]+',      # E = mc² 这样的模式
        r'\b[=+\-*/][^\n]+',                # = 开头的模式
    ]
    
    # LaTeX 格式的模式
    latex_patterns = [
        r'\$[^\$]+\$',  # 行内 LaTeX: $E = mc^2$
        r'\\[[^\\]+\\]',  # 块级 LaTeX: \[E = mc^2\]
        r'\\begin\{equation\}[^\\]+\\end\{equation\}',  # equation 环境
    ]
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含公式
            has_formulas = False
            non_latex_formulas = []
            
            # 查找所有可能的公式
            all_matches = []
            for pattern in formula_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                all_matches.extend(matches)
            
            # 去重
            all_matches = list(set(all_matches))
            
            # 检查每个可能的公式是否使用了 LaTeX 格式
            for match in all_matches:
                # 跳过太短的匹配
                if len(match) < 5:
                    continue
                
                # 跳过纯文本
                if not re.search(r'[=+\-*/]', match):
                    continue
                
                # 检查是否在 LaTeX 环境中
                in_latex = False
                for latex_pattern in latex_patterns:
                    latex_matches = re.findall(latex_pattern, content, re.DOTALL)
                    for latex_match in latex_matches:
                        if match.strip() in latex_match:
                            in_latex = True
                            break
                    if in_latex:
                        break
                
                # 检查是否是行内 LaTeX
                if not in_latex:
                    line_matches = re.findall(r'\$[^\$]+\$', content)
                    for line_match in line_matches:
                        if match.strip() in line_match:
                            in_latex = True
                            break
                
                if not in_latex:
                    non_latex_formulas.append(match.strip())
                    has_formulas = True
            
            # 检查是否有明显的数学符号但不是 LaTeX
            math_symbols = r'[=+\-*/^√πθφ∂∇∫∑∏]'
            if re.search(math_symbols, content):
                # 检查是否有 LaTeX 格式
                has_latex = any(re.search(pattern, content, re.DOTALL) for pattern in latex_patterns)
                has_inline_latex = bool(re.search(r'\$[^\$]+\$', content))
                
                if not has_latex and not has_inline_latex:
                    # 可能有非 LaTeX 格式的公式
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if re.search(math_symbols, line) and len(line.strip()) > 10:
                            # 检查是否是列表项或标题
                            if not (line.strip().startswith('#') or line.strip().startswith('*') or line.strip().startswith('-')):
                                non_latex_formulas.append(f"行 {i+1}: {line.strip()}")
                                has_formulas = True
            
            results.append({
                'file': file_path,
                'has_formulas': has_formulas,
                'non_latex_formulas': non_latex_formulas,
                'total_non_latex': len(non_latex_formulas)
            })
            
        except Exception as e:
            results.append({
                'file': file_path,
                'has_formulas': False,
                'non_latex_formulas': [f'Error reading file: {str(e)}'],
                'total_non_latex': 1
            })
    
    # 生成报告
    generate_report(results)

def generate_report(results):
    report_path = 'formula_latex_check_report.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# 公式 LaTeX 格式检查报告\n\n')
        f.write(f'检查时间: {os.popen("date /t").read().strip()}\n\n')
        f.write(f'检查文件数: {len(results)}\n\n')
        
        # 统计
        total_files = len(results)
        files_with_formulas = sum(1 for r in results if r['has_formulas'])
        files_with_non_latex = sum(1 for r in results if r['total_non_latex'] > 0)
        total_non_latex = sum(r['total_non_latex'] for r in results)
        
        f.write('## 统计概览\n\n')
        f.write(f'- 总文件数: {total_files}\n')
        f.write(f'- 包含公式的文件数: {files_with_formulas}\n')
        f.write(f'- 包含非 LaTeX 格式公式的文件数: {files_with_non_latex}\n')
        f.write(f'- 非 LaTeX 格式公式总数: {total_non_latex}\n\n')
        
        # 详细结果
        f.write('## 详细结果\n\n')
        
        for result in results:
            if result['total_non_latex'] > 0:
                f.write(f'### {result["file"]}\n')
                f.write(f'- 非 LaTeX 格式公式数: {result["total_non_latex"]}\n')
                if result['non_latex_formulas']:
                    f.write('\n**非 LaTeX 格式的公式:**\n\n')
                    for formula in result['non_latex_formulas'][:10]:  # 最多显示10个
                        f.write(f'- {formula}\n')
                    if len(result['non_latex_formulas']) > 10:
                        f.write(f'- ... 等 {len(result["non_latex_formulas"])} 个公式\n')
                f.write('\n')
        
        # 总结
        f.write('## 总结\n\n')
        if files_with_non_latex == 0:
            f.write('✅ 所有公式都使用了 LaTeX 格式！\n')
        else:
            f.write('❌ 发现非 LaTeX 格式的公式，需要进行转换。\n')
            f.write('建议：将所有公式转换为 LaTeX 格式，例如：\n')
            f.write('- 行内公式：$E = mc^2$\n')
            f.write('- 块级公式：\\[E = mc^2\\] 或 \\begin{equation}E = mc^2\\end{equation}\n')

if __name__ == '__main__':
    check_latex_formulas()
    print('检查完成，报告已生成: formula_latex_check_report.md')
