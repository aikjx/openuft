#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX公式可视化工具
用于扫描指定目录中的Markdown文件，识别LaTeX公式，并生成HTML页面进行可视化
"""

import os
import re
import argparse
import datetime

class LatexFormulaVisualizer:
    def __init__(self, root_dir, output_dir):
        self.root_dir = root_dir
        self.output_dir = output_dir
        self.formula_patterns = [
            # 行内公式: $公式$
            (r'\$(.*?)\$', False),
            # 块级公式: $$公式$$
            (r'\$\$(.*?)\$\$', True),
            # 块级公式: ```
            (r'```(?:math|latex)\s*(.*?)\s*```', True),
        ]
        self.collected_formulas = []
        self.collected_files = []
    
    def scan_files(self):
        """扫描目录中的Markdown文件，收集LaTeX公式"""
        print(f"开始扫描目录: {self.root_dir}")
        
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self._process_file(file_path)
        
        print(f"扫描完成! 共处理 {len(self.collected_files)} 个文件，发现 {len(self.collected_formulas)} 个公式")
    
    def _process_file(self, file_path):
        """处理单个Markdown文件，提取其中的LaTeX公式"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = os.path.relpath(file_path, self.root_dir)
            file_info = {
                'path': relative_path,
                'formulas': []
            }
            
            for pattern, is_block in self.formula_patterns:
                matches = re.finditer(pattern, content, re.DOTALL)
                for match in matches:
                    formula = match.group(1).strip()
                    # 过滤掉简单的文本或非常短的内容
                    if len(formula) > 3 and any(c in '+-*/=()[]{}^_\\' for c in formula):
                        formula_info = {
                            'content': formula,
                            'is_block': is_block,
                            'context': self._extract_context(content, match.start(), match.end())
                        }
                        self.collected_formulas.append({
                            'file': relative_path,
                            'formula': formula_info
                        })
                        file_info['formulas'].append(formula_info)
            
            if file_info['formulas']:
                self.collected_files.append(file_info)
                print(f"  从 {relative_path} 中提取了 {len(file_info['formulas'])} 个公式")
                
        except Exception as e:
            print(f"  处理文件 {file_path} 时出错: {str(e)}")
    
    def _extract_context(self, content, start, end):
        """提取公式周围的上下文文本"""
        context_start = max(0, start - 100)
        context_end = min(len(content), end + 100)
        context = content[context_start:context_end]
        # 清理上下文，移除多余的换行
        context = ' '.join(context.split())
        return context
    
    def generate_html(self):
        """生成包含KaTeX库和所有公式的HTML页面"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        output_file = os.path.join(self.output_dir, 'latex_formulas_visualization.html')
        
        html_content = self._get_html_template()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML页面已生成: {output_file}")
        return output_file
    
    def _get_html_template(self):
        """获取HTML模板内容"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 生成公式列表HTML
        formulas_html = ""
        for i, item in enumerate(self.collected_formulas):
            file_path = item['file']
            formula_info = item['formula']
            formula = formula_info['content']
            is_block = formula_info['is_block']
            context = formula_info['context']
            
            # 转义公式中的特殊字符
            escaped_formula = formula.replace('\\', '\\\\').replace('"', '\\"')
            
            display_mode = 'true' if is_block else 'false'
            formulas_html += f'''
            <div class="formula-item">
                <div class="formula-header">
                    <span class="formula-id">公式 {i+1}</span>
                    <span class="formula-file">文件: {file_path}</span>
                </div>
                <div class="formula-content">
                    <div class="formula-render" data-formula="{escaped_formula}" data-display="{display_mode}"></div>
                    <div class="formula-code">{formula}</div>
                </div>
                <div class="formula-context">
                    <strong>上下文:</strong> {context}
                </div>
            </div>
            '''
        
        # 生成文件索引HTML
        files_html = ""
        for file_info in self.collected_files:
            file_path = file_info['path']
            formula_count = len(file_info['formulas'])
            files_html += f'''
            <li class="file-item">
                <a href="#" class="file-link" data-file="{file_path}">{file_path} ({formula_count}个公式)</a>
            </li>
            '''
        
        return f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LaTeX公式可视化</title>
    
    <!-- KaTeX支持 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/contrib/auto-render.min.js"></script>
    
    <style>
        /* 全局样式 */
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        /* 头部样式 */
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        
        .header-info {{
            margin-top: 10px;
            font-size: 14px;
            opacity: 0.9;
        }}
        
        /* 主内容区域 */
        .main-content {{
            display: flex;
            flex-wrap: wrap;
        }}
        
        /* 侧边栏 */
        .sidebar {{
            width: 250px;
            padding: 20px;
            background-color: #f8f9fa;
            border-right: 1px solid #e9ecef;
            overflow-y: auto;
            max-height: calc(100vh - 120px);
        }}
        
        .sidebar h2 {{
            font-size: 18px;
            margin-bottom: 15px;
            color: #2c3e50;
        }}
        
        .file-list {{
            list-style: none;
        }}
        
        .file-item {{
            margin-bottom: 8px;
        }}
        
        .file-link {{
            text-decoration: none;
            color: #3498db;
            display: block;
            padding: 8px 12px;
            border-radius: 4px;
            transition: all 0.3s ease;
            font-size: 14px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .file-link:hover {{
            background-color: #e9ecef;
            color: #2980b9;
        }}
        
        .file-link.active {{
            background-color: #3498db;
            color: white;
        }}
        
        /* 公式显示区域 */
        .formulas-container {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            max-height: calc(100vh - 120px);
        }}
        
        .formula-item {{
            margin-bottom: 30px;
            padding: 20px;
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .formula-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .formula-id {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .formula-file {{
            font-size: 14px;
            color: #7f8c8d;
            font-family: monospace;
        }}
        
        .formula-content {{
            margin-bottom: 15px;
        }}
        
        .formula-render {{
            margin-bottom: 10px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
            overflow-x: auto;
        }}
        
        .formula-code {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 4px;
            font-size: 14px;
            overflow-x: auto;
            color: #e74c3c;
        }}
        
        .formula-context {{
            font-size: 14px;
            color: #7f8c8d;
            font-style: italic;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }}
        
        /* 搜索栏 */
        .search-container {{
            padding: 15px 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .search-input {{
            width: 100%;
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .main-content {{
                flex-direction: column;
            }}
            
            .sidebar {{
                width: 100%;
                max-height: 200px;
                border-right: none;
                border-bottom: 1px solid #e9ecef;
            }}
            
            .formulas-container {{
                max-height: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>LaTeX公式可视化</h1>
            <div class="header-info">
                扫描目录: {self.root_dir}<br>
                生成时间: {timestamp}<br>
                共发现 {len(self.collected_formulas)} 个公式，分布在 {len(self.collected_files)} 个文件中
            </div>
        </div>
        
        <div class="search-container">
            <input type="text" id="search-input" class="search-input" placeholder="搜索公式...">
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <h2>文件列表</h2>
                <ul class="file-list">
                    {files_html}
                </ul>
            </div>
            
            <div class="formulas-container" id="formulas-container">
                {formulas_html}
            </div>
        </div>
    </div>
    
    <script>
        // 渲染所有公式
        document.addEventListener("DOMContentLoaded", function() {{
            // 渲染公式
            const formulaElements = document.querySelectorAll('.formula-render');
            formulaElements.forEach(element => {{
                const formula = element.getAttribute('data-formula');
                const displayMode = element.getAttribute('data-display') === 'true';
                
                try {{
                    katex.render(formula, element, {{
                        displayMode: displayMode,
                        throwOnError: false,
                        trust: true
                    }});
                }} catch (e) {{
                    console.error('KaTeX渲染错误:', e);
                    element.textContent = '渲染错误: ' + formula;
                    element.style.color = 'red';
                }}
            }});
            
            // 文件过滤功能
            const fileLinks = document.querySelectorAll('.file-link');
            fileLinks.forEach(link => {{
                link.addEventListener('click', function(e) {{
                    e.preventDefault();
                    
                    // 移除所有活动状态
                    fileLinks.forEach(l => l.classList.remove('active'));
                    // 添加当前活动状态
                    this.classList.add('active');
                    
                    const targetFile = this.getAttribute('data-file');
                    filterByFile(targetFile);
                }});
            }});
            
            // 搜索功能
            const searchInput = document.getElementById('search-input');
            searchInput.addEventListener('input', function() {{
                const searchTerm = this.value.toLowerCase();
                searchFormulas(searchTerm);
            }});
        }});
        
        // 根据文件过滤公式
        function filterByFile(filePath) {{
            const formulaItems = document.querySelectorAll('.formula-item');
            formulaItems.forEach(item => {{
                const fileElement = item.querySelector('.formula-file');
                if (fileElement && fileElement.textContent.includes(filePath)) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}
        
        // 搜索公式
        function searchFormulas(searchTerm) {{
            if (!searchTerm) {{
                // 显示所有公式
                document.querySelectorAll('.formula-item').forEach(item => {{
                    item.style.display = 'block';
                }});
                return;
            }}
            
            const formulaItems = document.querySelectorAll('.formula-item');
            formulaItems.forEach(item => {{
                const formulaCode = item.querySelector('.formula-code').textContent.toLowerCase();
                const context = item.querySelector('.formula-context').textContent.toLowerCase();
                const filePath = item.querySelector('.formula-file').textContent.toLowerCase();
                
                if (formulaCode.includes(searchTerm) || 
                    context.includes(searchTerm) || 
                    filePath.includes(searchTerm)) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
'''
    
    def run(self):
        """运行可视化工具的主函数"""
        self.scan_files()
        if self.collected_formulas:
            return self.generate_html()
        else:
            print("没有找到任何LaTeX公式!")
            return None

def main():
    parser = argparse.ArgumentParser(description='LaTeX公式可视化工具')
    parser.add_argument('--root-dir', 
                       default='d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\00-解决传统物理问题论文',
                       help='要扫描的根目录')
    parser.add_argument('--output-dir', 
                       default='d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\00-解决传统物理问题论文\\latex_visualization',
                       help='输出HTML文件的目录')
    
    args = parser.parse_args()
    
    visualizer = LatexFormulaVisualizer(args.root_dir, args.output_dir)
    html_file = visualizer.run()
    
    if html_file:
        print(f"\n可视化完成! 请在浏览器中打开 {html_file} 查看结果")

if __name__ == "__main__":
    main()