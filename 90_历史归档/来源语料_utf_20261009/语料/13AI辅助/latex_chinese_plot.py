#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成包含LaTeX公式且中文不乱码的论文图片的综合解决方案

整合了Gemini-2.5-Flash和Grok-4-Fast的最佳实践
支持Windows/macOS/Linux，确保中文和LaTeX公式正确显示
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import matplotlib as mpl
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class LatexChinesePlot:
    """
    生成包含LaTeX公式且中文不乱码的论文图片的类
    
    主要特性：
    1. 支持Windows/macOS/Linux
    2. 自动检测并使用系统中安装的中文字体
    3. 集成LaTeX渲染，支持复杂数学公式
    4. 提供论文级别的美化样式
    5. 支持多种输出格式（png, pdf, svg）
    """
    
    def __init__(self, figsize=(8, 6), dpi=300, font_size=12):
        """
        初始化绘图类
        
        参数:
        figsize : tuple, 图片尺寸 (宽度, 高度)，单位为英寸
        dpi : int, 分辨率
        font_size : int, 默认字体大小
        """
        self.figsize = figsize
        self.dpi = dpi
        self.font_size = font_size
        
        # 预定义不同操作系统的中文字体路径
        self.chinese_fonts = {
            # Windows系统字体
            'Windows': [
                'C:/Windows/Fonts/simhei.ttf',      # 黑体
                'C:/Windows/Fonts/msyh.ttc',        # 微软雅黑
                'C:/Windows/Fonts/simsun.ttc',      # 宋体
            ],
            # macOS系统字体
            'Darwin': [
                '/System/Library/Fonts/STHeiti Light.ttc',  # 黑体
                '/Library/Fonts/Microsoft YaHei.ttf',       # 微软雅黑
                '/Library/Fonts/Songti.ttc',                # 宋体
            ],
            # Linux系统字体
            'Linux': [
                '/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf',  # Noto Sans CJK SC
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',               # 文泉驿正黑
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',            # 文泉驿微米黑
            ]
        }
        
        # 检测当前操作系统
        self.os_type = os.name
        if self.os_type == 'nt':
            self.os_type = 'Windows'
        else:
            import platform
            self.os_type = platform.system()
        
        # 配置matplotlib
        self._configure_matplotlib()
        
    def _configure_matplotlib(self):
        """配置matplotlib，支持中文和LaTeX"""
        
        # 设置默认字体大小
        rcParams.update({
            # 基础设置
            'font.size': self.font_size,
            'axes.titlesize': self.font_size + 2,
            'axes.labelsize': self.font_size,
            'xtick.labelsize': self.font_size - 2,
            'ytick.labelsize': self.font_size - 2,
            'legend.fontsize': self.font_size - 2,
            'figure.titlesize': self.font_size + 4,
            
            # 图片质量
            'figure.dpi': self.dpi,
            'savefig.dpi': self.dpi,
            'figure.figsize': self.figsize,
            
            # 线条样式
            'lines.linewidth': 2.0,
            'lines.markersize': 6,
            'axes.linewidth': 1.2,
            
            # 网格样式
            'grid.alpha': 0.3,
            'grid.linestyle': '--',
            
            # 图例样式
            'legend.frameon': True,
            'legend.framealpha': 0.8,
            'legend.fancybox': True,
            'legend.shadow': False,
            
            # 坐标轴样式
            'axes.spines.top': False,
            'axes.spines.right': False,
            
            # 颜色循环
            'axes.prop_cycle': plt.cycler(
                color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                       '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            )
        })
        
        # 配置LaTeX支持
        rcParams.update({
            'text.usetex': True,
            'text.latex.engine': 'xelatex',  # 使用xelatex引擎，支持中文
            'text.latex.preamble': r'\usepackage{xeCJK}\usepackage{amsmath}\usepackage{amssymb}',
        })
        
        # 尝试加载中文字体
        self._load_chinese_font()
    
    def _load_chinese_font(self):
        """自动检测并加载系统中的中文字体"""
        
        # 获取当前操作系统的字体列表
        font_list = self.chinese_fonts.get(self.os_type, [])
        
        # 检测字体是否存在
        for font_path in font_list:
            if os.path.exists(font_path):
                font_name = os.path.basename(font_path)
                print(f"✓ 成功加载中文字体: {font_name} ({font_path})")
                
                # 设置中文字体
                rcParams.update({
                    'font.family': ['sans-serif'],
                    'font.sans-serif': ['SimHei', 'WenQuanYi Micro Hei', 'DejaVu Sans'],
                    'axes.unicode_minus': False,  # 解决负号显示问题
                })
                
                # 在LaTeX preamble中添加字体设置
                rcParams['text.latex.preamble'] += rf'\setCJKmainfont{{{font_path}}}'
                rcParams['text.latex.preamble'] += rf'\setCJKsansfont{{{font_path}}}'
                return True
        
        # 如果没有找到预定义字体，尝试使用系统默认字体
        print("⚠ 未找到预定义的中文字体，将使用系统默认字体")
        print("   建议手动安装中文字体或修改字体路径")
        return False
    
    def create_example_plot(self, save_dir='./figures'):
        """
        创建一个包含中文和LaTeX公式的示例图片
        
        参数:
        save_dir : str, 图片保存目录
        
        返回:
        保存的文件路径列表
        """
        # 创建保存目录
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        
        # 生成示例数据
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = np.sin(x) * np.cos(x)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # 绘制曲线
        ax.plot(x, y1, label='$y_1 = \sin(x)$', linewidth=2.5)
        ax.plot(x, y2, label='$y_2 = \cos(x)$', linewidth=2.5)
        ax.plot(x, y3, label='$y_3 = \sin(x)\cos(x)$', linewidth=2.5)
        
        # 设置标题（包含中文和LaTeX公式）
        ax.set_title(r'\textbf{一个包含中文和LaTeX公式的图表示例}', fontsize=self.font_size + 2)
        
        # 设置坐标轴标签（包含中文）
        ax.set_xlabel('X 轴：变量 $t$', fontsize=self.font_size)
        ax.set_ylabel('Y 轴：函数值 $f(t)$', fontsize=self.font_size)
        
        # 设置图例
        ax.legend(loc='upper right', fontsize=self.font_size - 1)
        
        # 添加网格
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 添加LaTeX公式注解
        ax.text(1.5, 0.8, r'$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$', 
                fontsize=self.font_size + 1, color='red',
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
        
        # 添加中文注解
        ax.text(6, -0.8, '这是中文注解：曲线在$x=\pi$处相交', 
                fontsize=self.font_size, color='blue',
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
        
        # 调整布局
        plt.tight_layout(pad=2.0)
        
        # 保存图片
        file_paths = []
        for fmt in ['png', 'pdf', 'svg']:
            file_path = os.path.join(save_dir, f'latex_chinese_example.{fmt}')
            plt.savefig(file_path, format=fmt, dpi=self.dpi, bbox_inches='tight')
            file_paths.append(file_path)
            print(f"✓ 已保存图片: {file_path}")
        
        plt.close(fig)
        return file_paths
    
    def create_subplot_example(self, save_dir='./figures'):
        """
        创建包含多个子图的示例，展示更复杂的布局
        
        参数:
        save_dir : str, 图片保存目录
        
        返回:
        保存的文件路径列表
        """
        # 创建保存目录
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        
        # 创建2x2子图
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=self.dpi)
        
        # 生成示例数据
        x = np.linspace(0, 10, 100)
        
        # 子图1: 正弦和余弦曲线
        ax = axes[0, 0]
        ax.plot(x, np.sin(x), label='$\sin(x)$')
        ax.plot(x, np.cos(x), label='$\cos(x)$')
        ax.set_title('正弦和余弦函数', fontsize=self.font_size + 1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 子图2: 指数函数
        ax = axes[0, 1]
        ax.plot(x, np.exp(-x/5) * np.sin(x), label='$e^{-x/5} \sin(x)$')
        ax.plot(x, np.exp(-x/5) * np.cos(x), label='$e^{-x/5} \cos(x)$')
        ax.set_title('衰减振荡函数', fontsize=self.font_size + 1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 子图3: 幂函数
        ax = axes[1, 0]
        ax.plot(x, x**2, label='$x^2$')
        ax.plot(x, x**3, label='$x^3$')
        ax.set_title('幂函数', fontsize=self.font_size + 1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 子图4: 高斯函数
        ax = axes[1, 1]
        ax.plot(x, np.exp(-(x-5)**2/2), label='$e^{-(x-5)^2/2}$')
        ax.set_title('高斯函数', fontsize=self.font_size + 1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 添加总标题
        fig.suptitle(r'\textbf{多种数学函数示例（包含中文）}', 
                   fontsize=self.font_size + 4, y=0.98)
        
        # 调整布局
        plt.tight_layout(pad=3.0, w_pad=2.0, h_pad=2.0)
        
        # 保存图片
        file_paths = []
        for fmt in ['png', 'pdf', 'svg']:
            file_path = os.path.join(save_dir, f'latex_chinese_subplots.{fmt}')
            plt.savefig(file_path, format=fmt, dpi=self.dpi, bbox_inches='tight')
            file_paths.append(file_path)
            print(f"✓ 已保存子图示例: {file_path}")
        
        plt.close(fig)
        return file_paths

def main():
    """主函数，演示如何使用LatexChinesePlot类"""
    print("=" * 60)
    print("   Python生成包含LaTeX公式且中文不乱码的论文图片")
    print("=" * 60)
    
    # 创建绘图实例
    plotter = LatexChinesePlot(figsize=(10, 6), dpi=300, font_size=14)
    
    print("\n1. 创建简单示例图片...")
    plotter.create_example_plot()
    
    print("\n2. 创建子图示例图片...")
    plotter.create_subplot_example()
    
    print("\n" + "=" * 60)
    print("   图片生成完成！")
    print("   请检查 ./figures 目录下的图片文件")
    print("=" * 60)

if __name__ == "__main__":
    main()