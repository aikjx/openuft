import os
import re

# 定义要修复的目录
VISUALIZATION_DIR = r'd:\a10\aikjx\code\my_lib\utf\10-统一场论核心公式\可视化'

# Python 文件修复函数
def fix_python_files():
    """修复 Python 文件中的中文和 LaTeX 公式显示问题"""
    # 遍历所有子目录中的 Python 文件
    for root, dirs, files in os.walk(VISUALIZATION_DIR):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f'正在修复 Python 文件: {file_path}')
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    print(f'警告: 无法以UTF-8编码打开 {file_path}，尝试其他编码...')
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                    except:
                        print(f'错误: 无法打开 {file_path}，跳过此文件。')
                        continue
                
                # 检查是否已经设置了中文字体
                if 'plt.rcParams["font.family"]' not in content:
                    # 在导入 matplotlib 后添加中文字体设置
                    matplotlib_import_pattern = r'import matplotlib\.pyplot as plt'
                    font_settings = '''\n# 设置中文字体 - Windows系统通用字体\nplt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]\nplt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题\nplt.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染\nplt.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式'''
                    
                    if re.search(matplotlib_import_pattern, content):
                        new_content = re.sub(matplotlib_import_pattern, f'{matplotlib_import_pattern}{font_settings}', content)
                    else:
                        # 如果没有找到 matplotlib 导入，在文件开头添加
                        new_content = f'''# -*- coding: utf-8 -*-
# 设置中文字体支持 - Windows系统通用字体
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
matplotlib.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染
matplotlib.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式
{content}'''
                else:
                    new_content = content
                    # 确保中文字体配置完整
                    new_content = re.sub(r'plt\.rcParams\["font\.family"\]\s*=\s*\[.*?\]', 
                                        'plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]', 
                                        new_content)
                
                # 确保 LaTeX 渲染配置正确
                if 'plt.rcParams["text.usetex"]' not in new_content:
                    # 添加 LaTeX 配置
                    if re.search(r'plt\.rcParams\["axes\.unicode_minus"\]\s*=\s*False', new_content):
                        new_content = re.sub(r'plt\.rcParams\["axes\.unicode_minus"\]\s*=\s*False', 
                                            'plt.rcParams["axes.unicode_minus"] = False\nplt.rcParams["text.usetex"] = False\nplt.rcParams["mathtext.fontset"] = "cm"', 
                                            new_content)
                    else:
                        # 在文件开头添加
                        new_content = f'''{new_content}

# LaTeX 公式渲染配置
plt.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染
plt.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式'''
                
                # 保存修复后的文件
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                except:
                    print(f'错误: 无法保存 {file_path}，跳过此文件。')

# HTML 文件修复函数
def fix_html_files():
    """修复 HTML 文件中的中文和 KaTeX 公式显示问题"""
    # KaTeX 初始化代码
    katex_init_code = '''\n    <script>\n        document.addEventListener("DOMContentLoaded", function() {\n            // 渲染所有 LaTeX 公式\n            renderMathInElement(document.body, {\n                delimiters: [\n                    {left: "$", right: "$", display: false},\n                    {left: "$$", right: "$$", display: true}\n                ],\n                throwOnError : false,\n                trust: true\n            });\n        });\n    </script>'''
    
    # KaTeX CDN 代码
    katex_cdn_code = '''\n    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>\n    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>\n    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">'''
    
    # 遍历所有子目录中的 HTML 文件
    for root, dirs, files in os.walk(VISUALIZATION_DIR):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f'正在修复 HTML 文件: {file_path}')
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    print(f'警告: 无法以UTF-8编码打开 {file_path}，尝试其他编码...')
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                    except:
                        print(f'错误: 无法打开 {file_path}，跳过此文件。')
                        continue
                
                new_content = content
                
                # 确保设置了正确的 charset
                if 'meta charset="UTF-8"' not in new_content and 'meta charset=utf-8' not in new_content:
                    if '<head>' in new_content:
                        new_content = new_content.replace('<head>', '<head>\n    <meta charset="UTF-8">')
                    else:
                        # 在文件开头添加
                        new_content = '<meta charset="UTF-8">\n' + new_content
                
                # 确保设置了语言为中文
                if 'lang="zh-CN"' not in new_content and 'lang=zh-CN' not in new_content:
                    if '<html' in new_content:
                        new_content = new_content.replace('<html', '<html lang="zh-CN"')
                    else:
                        # 在 head 标签中添加
                        if '<head>' in new_content:
                            new_content = new_content.replace('<head>', '<head>\n    <html lang="zh-CN">')
                
                # 确保引入了 KaTeX 库
                if 'katex.min.js' not in new_content:
                    if '</head>' in new_content:
                        new_content = new_content.replace('</head>', katex_cdn_code + '\n    </head>')
                
                # 确保添加了 KaTeX 初始化代码
                if 'renderMathInElement' not in new_content:
                    if '</body>' in new_content:
                        new_content = new_content.replace('</body>', katex_init_code + '\n    </body>')
                
                # 确保页面有合适的中文字体
                if 'font-family' not in new_content.lower():
                    # 添加基本样式
                    basic_style = '''\n    <style>\n        body {\n            font-family: 'Microsoft YaHei', 'PingFang SC', 'Hiragino Sans GB', 'SimHei', sans-serif;\n        }\n    </style>'''
                    if '</head>' in new_content:
                        new_content = new_content.replace('</head>', basic_style + '\n    </head>')
                
                # 保存修复后的文件
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                except:
                    print(f'错误: 无法保存 {file_path}，跳过此文件。')

# 创建修复日志文件
def create_fix_log():
    """创建修复日志文件"""
    log_path = os.path.join(VISUALIZATION_DIR, 'font_and_latex_fix_log.txt')
    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('统一场论可视化文件中文和LaTeX公式修复日志\n')
            f.write('=======================================\n\n')
            f.write('修复内容:\n')
            f.write('1. 为Python文件添加中文字体支持\n')
            f.write('2. 配置Matplotlib的LaTeX公式渲染\n')
            f.write('3. 确保HTML文件正确加载KaTeX库并渲染LaTeX公式\n')
            f.write('4. 添加合适的中文字体设置\n\n')
            f.write('修复完成时间: ' + str(os.path.getmtime(__file__)) + '\n\n')
            f.write('使用说明:\n')
            f.write('1. 修复后的Python文件可以直接运行，中文和公式应该能正常显示\n')
            f.write('2. 修复后的HTML文件需要在浏览器中打开，LaTeX公式会自动渲染\n')
            f.write('3. 如果仍然遇到显示问题，可能需要安装相应的字体库\n')
    except:
        print('警告: 无法创建修复日志文件。')

# 主函数
def main():
    print('开始修复统一场论可视化文件的中文和LaTeX公式显示问题...')
    
    # 修复 Python 文件
    fix_python_files()
    
    # 修复 HTML 文件
    fix_html_files()
    
    # 创建修复日志
    create_fix_log()
    
    print('修复完成！')
    print('请查看各可视化文件，中文和公式应该已经可以正常显示。')
    print('如果仍有问题，请参考生成的日志文件获取更多信息。')

if __name__ == '__main__':
    main()