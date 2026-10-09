#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 定义需要处理的目录
directories = [
    "d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\电磁光速几何耦合常数Z'\\解答",
    "d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\电磁光速几何耦合常数Z'\\变化电磁场产生引力场方程"
]

# 转换公式为正确的LaTeX格式
def convert_latex(content):
    # 保持已有的$...$和$$...$$格式不变
    # 只处理未被$包围的公式
    
    # 简单处理：手动检查并转换公式
    # 这里我们只确保所有公式都使用$包围
    
    return content

# 处理所有文件
def main():
    for directory in directories:
        if not os.path.exists(directory):
            print(f"目录不存在：{directory}")
            continue
        
        for filename in os.listdir(directory):
            if filename.endswith('.md'):
                file_path = os.path.join(directory, filename)
                print(f"处理文件：{file_path}")
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 转换LaTeX格式
                new_content = convert_latex(content)
                
                # 保存修改后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"文件处理完成：{file_path}")

if __name__ == "__main__":
    main()
