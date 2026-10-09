#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式15可视化修复专用脚本（支持中英文切换）
功能：为公式15生成干净的可视化图片，避免乱码，支持中文和英文显示模式
作者：张祥前统一场论研究团队
日期：2025-10-26
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

# 创建输出目录
output_dir = 'd:/a10/aikjx/code/my_lib/utf/11-统一场论公式论文集/所有公式可视化_修复版'
os.makedirs(output_dir, exist_ok=True)

# 语言配置字典
LANGUAGE_CONFIG = {
    'zh': {
        'title_prefix': '公式',
        'formula': '公式',
        'description': '描述',
        'physics_meaning': '物理意义',
        'time_label': '时间(t)',
        'magnetic_field_label': '磁场(B)',
        'formula_name': '变化的磁场产生引力场和电场方程',
        'formula_description': '安培-麦克斯韦方程的统一形式',
        'formula_physics_meaning': '揭示了电磁现象和引力现象的统一性',
        'start_message': '开始修复公式15的可视化图片...',
        'finish_message': '修复完成！请检查生成的图片是否正常显示。',
        'save_message': '公式15可视化图片已成功生成并保存到: '
    },
    'en': {
        'title_prefix': 'Formula',
        'formula': 'Formula',
        'description': 'Description',
        'physics_meaning': 'Physical Meaning',
        'time_label': 'Time(t)',
        'magnetic_field_label': 'Magnetic Field(B)',
        'formula_name': 'Equation of Changing Magnetic Field Producing Gravitational and Electric Fields',
        'formula_description': 'Unified form of Ampère-Maxwell equation',
        'formula_physics_meaning': 'Reveals the unity of electromagnetic and gravitational phenomena',
        'start_message': 'Starting to fix the visualization of Formula 15...',
        'finish_message': 'Fix completed! Please check if the generated image displays correctly.',
        'save_message': 'Formula 15 visualization image has been successfully generated and saved to: '
    }
}

def setup_matplotlib(language='zh'):
    """设置matplotlib配置，确保正确显示中文字体"""
    plt.rcParams['backend'] = 'Agg'
    
    # 根据语言选择字体配置
    if language == 'zh':
        # 中文配置：优先使用支持中文的字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans', 'Arial']
    else:
        # 英文配置：使用标准西文字体
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans', 'sans-serif']
    
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['text.usetex'] = False  # 禁用LaTeX避免编码问题
    plt.rcParams['mathtext.fontset'] = 'cm'  # 使用Computer Modern字体集
    plt.rcParams['font.family'] = ['sans-serif']
    
    # 确保字体渲染正确
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

def generate_formula15_visualization(language='zh'):
    """生成公式15的可视化图片，支持中英文切换"""
    # 设置matplotlib
    setup_matplotlib(language)
    
    # 获取语言配置
    config = LANGUAGE_CONFIG[language]
    
    formula_id = 15
    formula_name = config['formula_name']
    
    # 创建图表
    plt.figure(figsize=(10, 6), dpi=300)
    
    # 生成模拟数据 - 磁场随时间变化
    t = np.linspace(0, 10, 100)
    B = np.sin(t)  # 模拟磁场
    
    # 绘制磁场曲线
    plt.plot(t, B, 'b-', linewidth=2)
    
    # 添加标题和标签（使用对应语言）
    plt.title(f'{config["title_prefix"]}{formula_id:02d}: {formula_name}', fontsize=14)
    plt.xlabel(config['time_label'], fontsize=12)
    plt.ylabel(config['magnetic_field_label'], fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 添加公式文本 - 使用纯ASCII字符表示，避免任何特殊字符导致的乱码
    formula_text = "nabla X B = mu0 J + mu0 epsilon0 dE/dt"
    plt.figtext(0.5, 0.01, f'{config["formula"]}: {formula_text}', ha='center', fontsize=10, 
                bbox=dict(facecolor='yellow', alpha=0.3))
    
    # 添加公式描述和物理意义（使用对应语言）
    plt.figtext(0.5, 0.05, f'{config["description"]}: {config["formula_description"]}', ha='center', fontsize=9, 
                bbox=dict(facecolor='lightblue', alpha=0.3))
    plt.figtext(0.5, 0.10, f'{config["physics_meaning"]}: {config["formula_physics_meaning"]}', ha='center', fontsize=9, 
                bbox=dict(facecolor='lightgreen', alpha=0.3))
    
    # 调整布局并保存
    plt.tight_layout(rect=[0, 0.15, 1, 0.95])
    
    # 生成文件名，英文模式下使用英文文件名，中文模式下使用中文文件名
    if language == 'en':
        file_name = f'Formula{formula_id:02d}_{formula_name.replace(" ", "_")}.png'
    else:
        file_name = f'公式{formula_id:02d}_{formula_name}.png'
    
    output_file = os.path.join(output_dir, file_name)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', format='png')
    plt.close()
    
    print(f"{config['save_message']}{output_file}")
    return output_file

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='公式15可视化修复脚本（支持中英文切换）')
    parser.add_argument('--lang', choices=['zh', 'en'], default='zh', 
                        help='设置显示语言（zh=中文，en=英文）')
    return parser.parse_args()

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_arguments()
    
    # 获取语言配置
    config = LANGUAGE_CONFIG[args.lang]
    
    print(config['start_message'])
    output_file = generate_formula15_visualization(args.lang)
    print(config['finish_message'])
