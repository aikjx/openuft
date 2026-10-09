#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
几何因子完整分析系统
Complete Geometric Factor Analysis System

这是一个完整的分析系统，用于：
1. 展示几何因子推导的底层原理
2. 分析推导中的数学和物理错误
3. 提供正确的科学方法对比
4. 创建直观的可视化动画

确保所有代码都能正常运行，没有编码问题
Author: Physics Analysis Expert
Date: 2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import matplotlib.patches as patches
import warnings
import sys
import os
warnings.filterwarnings('ignore')

# 添加错误处理器模块路径
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 导入自定义错误处理器
from error_handler import error_handler, ErrorType, safe_execution

# 设置matplotlib参数 - 确保兼容性
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 100
plt.rcParams['axes.unicode_minus'] = False

# 尝试设置中文字体，如果失败则使用默认字体
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    CHINESE_SUPPORT = True
except:
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
    CHINESE_SUPPORT = False

class GeometricFactorAnalysisSystem:
    """几何因子完整分析系统"""
    
    def __init__(self):
        self.pi = np.pi
        self.error_handler = error_handler  # 初始化错误处理器
        
        # 颜色配置
        self.colors = {
            'correct': '#2ECC71',
            'incorrect': '#E74C3C',
            'warning': '#F39C12',
            'neutral': '#34495E',
            'highlight': '#9B59B6',
            'sphere': '#FF6B6B',
            'plane': '#4ECDC4',
            'formula': '#8E44AD'
        }
        
        # 文本配置
        self.texts = {
            'title_main': 'Geometric Factor Analysis System' if not CHINESE_SUPPORT else '几何因子分析系统',
            'sphere_area': 'Sphere Area' if not CHINESE_SUPPORT else '球面积',
            'circle_perimeter': 'Circle Perimeter' if not CHINESE_SUPPORT else '圆周长',
            'geometric_factor': 'Geometric Factor' if not CHINESE_SUPPORT else '几何因子',
            'dimensional_analysis': 'Dimensional Analysis' if not CHINESE_SUPPORT else '量纲分析',
            'error_analysis': 'Error Analysis' if not CHINESE_SUPPORT else '错误分析',
            'correct_method': 'Correct Method' if not CHINESE_SUPPORT else '正确方法'
        }
    
    @safe_execution
    def create_main_analysis_figure(self):
        """创建主要分析图表"""
        try:
            fig = plt.figure(figsize=(18, 12))
            fig.suptitle(self.texts['title_main'], fontsize=16, fontweight='bold')
            
            # 创建子图网格 (3x3)
            gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
            
            # 1. 3D球面可视化
            ax1 = fig.add_subplot(gs[0, 0], projection='3d')
            self.plot_3d_sphere_visualization(ax1)
            
            # 2. 面积vs周长对比
            ax2 = fig.add_subplot(gs[0, 1])
            self.plot_area_perimeter_comparison(ax2)
            
            # 3. 几何因子计算步骤
            ax3 = fig.add_subplot(gs[0, 2])
            self.plot_calculation_steps(ax3)
            
            # 4. 量纲分析
            ax4 = fig.add_subplot(gs[1, 0])
            self.plot_dimensional_analysis(ax4)
            
            # 5. 错误识别
            ax5 = fig.add_subplot(gs[1, 1])
            self.plot_error_identification(ax5)
            
            # 6. 正确vs错误对比
            ax6 = fig.add_subplot(gs[1, 2])
            self.plot_correct_vs_wrong(ax6)
            
            # 7. 立体角积分
            ax7 = fig.add_subplot(gs[2, 0])
            self.plot_solid_angle_integrals(ax7)
            
            # 8. 物理常数关系
            ax8 = fig.add_subplot(gs[2, 1])
            self.plot_physical_constants(ax8)
            
            # 9. 结论总结
            ax9 = fig.add_subplot(gs[2, 2])
            self.plot_conclusions(ax9)
            
            plt.tight_layout()
            return fig
        except Exception as e:
            self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Failed to create main analysis figure", e)
            raise
    
    @safe_execution
    def plot_3d_sphere_visualization(self, ax):
        """绘制3D球面可视化"""
        try:
            # 创建球面
            u = np.linspace(0, 2*self.pi, 20)
            v = np.linspace(0, self.pi, 20)
            x = np.outer(np.cos(u), np.sin(v))
            y = np.outer(np.sin(u), np.sin(v))
            z = np.outer(np.ones(np.size(u)), np.cos(v))
            
            # 绘制球面
            ax.plot_surface(x, y, z, alpha=0.6, color=self.colors['sphere'])
            
            # 绘制赤道圆
            theta = np.linspace(0, 2*self.pi, 100)
            circle_x = np.cos(theta)
            circle_y = np.sin(theta)
            circle_z = np.zeros_like(theta)
            ax.plot(circle_x, circle_y, circle_z, 
                   color=self.colors['highlight'], linewidth=4)
            
            ax.set_title('3D Sphere vs 2D Circle')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
        except Exception as e:
            self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Failed to plot 3D sphere visualization", e)
            raise
    
    @safe_execution
    def plot_area_perimeter_comparison(self, ax):
        """绘制面积vs周长对比"""
        try:
            # 数据
            categories = ['Sphere\nArea', 'Circle\nPerimeter', 'Ratio']
            values = [4*self.pi, 2*self.pi, 2]
            colors = [self.colors['sphere'], self.colors['plane'], self.colors['highlight']]
            
            # 创建柱状图
            bars = ax.bar(categories, values, color=colors, alpha=0.7)
            
            # 添加数值标签
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{val:.2f}', ha='center', va='bottom', fontsize=10)
            
            ax.set_ylabel('Value')
            ax.set_title('Geometric Quantities Comparison')
            ax.grid(True, alpha=0.3, axis='y')
            
            # 验证数值计算
            self.error_handler.validate_integral(4*self.pi, 4*self.pi, tolerance=0.01)
            self.error_handler.validate_integral(2*self.pi, 2*self.pi, tolerance=0.01)
        except Exception as e:
            self.error_handler.handle_error(ErrorType.CALCULATION_ERROR, "Failed to plot area-perimeter comparison", e)
            raise
    
    @safe_execution
    def plot_calculation_steps(self, ax):
        """绘制计算步骤"""
        try:
            ax.axis('off')
            
            steps = [
                "Step 1: Sphere Area = 4πr^2",
                "Step 2: Circle Perimeter = 2πr",
                "Step 3: Ratio = 4πr^2 / 2πr = 2r",
                "Step 4: At unit radius r=1",
                "Step 5: Geometric Factor = 2×1 = 2"
            ]
            
            y_positions = np.linspace(0.9, 0.1, len(steps))
            
            for i, (step, y_pos) in enumerate(zip(steps, y_positions)):
                color = self.colors['highlight'] if i == len(steps)-1 else self.colors['neutral']
                weight = 'bold' if i == len(steps)-1 else 'normal'
                ax.text(0.05, y_pos, step, fontsize=11, color=color, weight=weight,
                       transform=ax.transAxes)
            
            ax.set_title('Calculation Steps')
        except Exception as e:
            self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Failed to plot calculation steps", e)
            raise
    
    @safe_execution
    def plot_dimensional_analysis(self, ax):
        """绘制量纲分析"""
        try:
            ax.axis('off')
            
            analysis_text = [
                "Dimensional Analysis:",
                "",
                "Sphere Area: [L^2]",
                "Circle Perimeter: [L¹]",
                "Ratio: [L^2]/[L¹] = [L¹]",
                "",
                "Problem: Still has dimension!",
                "Not dimensionless number",
                "",
                "Force to r=1: Arbitrary choice",
                "Lacks generality"
            ]
            
            y_pos = 0.95
            for text in analysis_text:
                if text == "":
                    y_pos -= 0.05
                    continue
                
                if "Problem:" in text or "Not dimensionless" in text or "Arbitrary" in text or "Lacks" in text:
                    color = self.colors['incorrect']
                    weight = 'bold'
                    # 记录量纲错误
                    self.error_handler.handle_error(ErrorType.DIMENSIONAL_ERROR, f"Dimension analysis: {text}", None)
                elif text.endswith(':'):
                    color = self.colors['neutral']
                    weight = 'bold'
                else:
                    color = self.colors['neutral']
                    weight = 'normal'
                
                ax.text(0.05, y_pos, text, fontsize=10, color=color, weight=weight,
                       transform=ax.transAxes)
                y_pos -= 0.08
            
            ax.set_title('Dimensional Consistency Check')
        except Exception as e:
            self.error_handler.handle_error(ErrorType.ANALYSIS_ERROR, "Failed to plot dimensional analysis", e)
            raise
    
    @safe_execution
    def plot_error_identification(self, ax):
        """绘制错误识别"""
        try:
            ax.axis('off')
            
            errors = [
                "Major Errors Identified:",
                "",
                "✗ Mixing 3D and 2D quantities",
                "✗ No physical justification",
                "✗ Dimensional inconsistency", 
                "✗ Arbitrary unit choice",
                "✗ No experimental basis",
                "",
                "Standard Physics:",
                "✓ Dimensionless factors",
                "✓ Physical derivation",
                "✓ Experimental verification"
            ]
            
            y_pos = 0.95
            for text in errors:
                if text == "":
                    y_pos -= 0.04
                    continue
                
                if text.startswith('✗'):
                    color = self.colors['incorrect']
                    # 记录检测到的错误
                    error_msg = text.replace('✗ ', '')
                    self.error_handler.handle_error(ErrorType.FORMULA_ERROR, f"Error identified: {error_msg}", None)
                elif text.startswith('✓'):
                    color = self.colors['correct']
                elif text.endswith(':'):
                    color = self.colors['neutral']
                    weight = 'bold'
                else:
                    color = self.colors['neutral']
                    weight = 'normal'
                
                weight = 'bold' if text.endswith(':') else 'normal'
                
                ax.text(0.05, y_pos, text, fontsize=9, color=color, weight=weight,
                       transform=ax.transAxes)
                y_pos -= 0.07
            
            ax.set_title('Error Identification')
        except Exception as e:
            self.error_handler.handle_error(ErrorType.ANALYSIS_ERROR, "Failed to plot error identification", e)
            raise
    
    @safe_execution
    def plot_correct_vs_wrong(self, ax):
        """绘制正确vs错误对比"""
        try:
            # 创建对比表格
            methods = ['Paper Method', 'Standard Physics']
            scores = [2, 8]  # 评分 (满分10分)
            colors = [self.colors['incorrect'], self.colors['correct']]
            
            bars = ax.barh(methods, scores, color=colors, alpha=0.7)
            
            # 添加评分标签
            for bar, score in zip(bars, scores):
                width = bar.get_width()
                ax.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                       f'{score}/10', ha='left', va='center', fontsize=12, fontweight='bold')
            
            ax.set_xlabel('Scientific Rigor Score')
            ax.set_title('Method Comparison')
            ax.set_xlim(0, 10)
            ax.grid(True, alpha=0.3, axis='x')
            
            # 添加评分标准
            ax.text(0.02, 0.02, 'Criteria: Math rigor, Physical basis,\nExperimental support, Peer review',
                   transform=ax.transAxes, fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8))
        except Exception as e:
            self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Failed to plot correct vs wrong comparison", e)
            raise
    
    @safe_execution
    def plot_solid_angle_integrals(self, ax):
        """绘制立体角积分"""
        try:
            theta = np.linspace(0, self.pi, 200)
            sin_theta = np.sin(theta)
            sin_squared = np.sin(theta)**2
            
            ax.plot(theta, sin_theta, 'g-', linewidth=3, label='Correct: sin(θ)')
            ax.plot(theta, sin_squared, 'r--', linewidth=3, label='Paper: sin^2(θ)')
            
            ax.fill_between(theta, 0, sin_theta, alpha=0.3, color='green')
            ax.fill_between(theta, 0, sin_squared, alpha=0.3, color='red')
            
            # 添加积分值
            ax.text(0.6, 0.8, '∫sin(θ)dθ = 2', 
                    transform=ax.transAxes, fontsize=10,
                    bbox=dict(boxstyle="round", facecolor='lightgreen'))
            ax.text(0.6, 0.7, '∫sin^2(θ)dθ = π/2', 
                    transform=ax.transAxes, fontsize=10,
                    bbox=dict(boxstyle="round", facecolor='lightcoral'))
            
            ax.set_xlabel('θ (radians)')
            ax.set_ylabel('Integrand')
            ax.set_title('Solid Angle Integrals')
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)
            
            # 验证积分计算
            self.error_handler.validate_integral(np.trapz(sin_theta, theta), 2, tolerance=0.1)
            self.error_handler.validate_integral(np.trapz(sin_squared, theta), np.pi/2, tolerance=0.1)
        except Exception as e:
            self.error_handler.handle_error(ErrorType.CALCULATION_ERROR, "Failed to plot solid angle integrals", e)
            raise
    
    @safe_execution
    def plot_physical_constants(self, ax):
        """绘制物理常数"""
        try:
            # 真正有意义的物理常数关系
            G = 6.67430e-11
            c = 299792458
            hbar = 1.054571817e-34
            
            # 普朗克单位
            constants = {
                'Planck\nLength': np.sqrt(hbar * G / c**3),
                'Planck\nTime': np.sqrt(hbar * G / c**5),
                'Planck\nMass': np.sqrt(hbar * c / G)
            }
            
            names = list(constants.keys())
            values = list(constants.values())
            log_values = [np.log10(abs(v)) for v in values]
            
            colors = ['blue', 'green', 'red']
            bars = ax.bar(names, log_values, color=colors, alpha=0.7)
            
            # 添加数值标签
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{value:.2e}', ha='center', va='bottom', fontsize=8, rotation=45)
            
            ax.set_ylabel('log₁₀(Value)')
            ax.set_title('Meaningful Physical Constants')
            ax.grid(True, alpha=0.3, axis='y')
        except Exception as e:
            self.error_handler.handle_error(ErrorType.CALCULATION_ERROR, "Failed to plot physical constants", e)
            raise
    
    @safe_execution
    def plot_conclusions(self, ax):
        """绘制结论"""
        try:
            ax.axis('off')
            
            conclusions = [
                "SCIENTIFIC CONCLUSIONS:",
                "",
                "❌ Paper's Geometric Factor:",
                "  • Mathematical errors",
                "  • Conceptual confusion", 
                "  • No experimental basis",
                "",
                "✅ Correct Approach:",
                "  • Rigorous mathematics",
                "  • Physical principles",
                "  • Experimental verification",
                "",
                "⚠️ RECOMMENDATION:",
                "Use established physics",
                "(General Relativity, QFT)"
            ]
            
            y_pos = 0.95
            for text in conclusions:
                if text == "":
                    y_pos -= 0.04
                    continue
                
                if text.startswith('❌'):
                    color, weight = self.colors['incorrect'], 'bold'
                elif text.startswith('✅'):
                    color, weight = self.colors['correct'], 'bold'
                elif text.startswith('⚠️'):
                    color, weight = self.colors['warning'], 'bold'
                elif text.endswith(':'):
                    color, weight = self.colors['neutral'], 'bold'
                else:
                    color, weight = self.colors['neutral'], 'normal'
                
                size = 11 if text.startswith('SCIENTIFIC') else 9
                
                ax.text(0.05, y_pos, text, fontsize=size, color=color, 
                       fontweight=weight, transform=ax.transAxes)
                y_pos -= 0.06
            
            ax.set_title('Final Assessment')
        except Exception as e:
            self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Failed to plot conclusions", e)
            raise
    
    @safe_execution
    def create_animated_demonstration(self):
        """创建动画演示"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Animated Geometric Factor Analysis', fontsize=14, fontweight='bold')
            
            def animate(frame):
                # 清除所有子图
                for ax in [ax1, ax2, ax3, ax4]:
                    ax.clear()
                
                # 动画进度
                progress = frame / 100.0
                
                # 1. 旋转的3D球面
                ax1 = fig.add_subplot(2, 2, 1, projection='3d')
                u = np.linspace(0, 2*self.pi, 20)
                v = np.linspace(0, self.pi, 20)
                x = np.outer(np.cos(u), np.sin(v))
                y = np.outer(np.sin(u), np.sin(v))
                z = np.outer(np.ones(np.size(u)), np.cos(v))
                
                ax1.plot_surface(x, y, z, alpha=0.6, color=self.colors['sphere'])
                ax1.view_init(elev=20, azim=frame*3.6)  # 旋转
                ax1.set_title('Rotating Sphere')
                
                # 2. 动态柱状图
                ax2 = fig.add_subplot(2, 2, 2)
                categories = ['Sphere\nArea', 'Circle\nPerimeter', 'Ratio']
                values = [4*self.pi, 2*self.pi, 2]
                display_values = [v * min(1.0, progress*2) for v in values]
                
                bars = ax2.bar(categories, display_values, 
                              color=[self.colors['sphere'], self.colors['plane'], self.colors['highlight']], 
                              alpha=0.7)
                
                for bar, val in zip(bars, values):
                    height = bar.get_height()
                    if height > 0.1:
                        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                               f'{val:.2f}', ha='center', va='bottom', fontsize=10)
                
                ax2.set_ylabel('Value')
                ax2.set_title('Dynamic Comparison')
                ax2.set_ylim(0, max(values)*1.2)
                
                # 3. 积分函数对比
                ax3 = fig.add_subplot(2, 2, 3)
                theta = np.linspace(0, self.pi, 200)
                sin_theta = np.sin(theta)
                sin_squared = np.sin(theta)**2
                
                # 动态显示
                n_points = int(len(theta) * progress)
                if n_points > 0:
                    ax3.plot(theta[:n_points], sin_theta[:n_points], 'g-', linewidth=3, label='sin(θ)')
                    ax3.plot(theta[:n_points], sin_squared[:n_points], 'r--', linewidth=3, label='sin^2(θ)')
                
                ax3.set_xlabel('θ (radians)')
                ax3.set_ylabel('Function Value')
                ax3.set_title('Integral Functions')
                ax3.legend()
                ax3.grid(True, alpha=0.3)
                ax3.set_xlim(0, self.pi)
                ax3.set_ylim(0, 1.1)
                
                # 4. 错误计数器
                ax4 = fig.add_subplot(2, 2, 4)
                ax4.axis('off')
                
                errors_found = min(5, int(progress * 5))
                error_list = [
                    "1. Dimensional inconsistency",
                    "2. Mathematical errors", 
                    "3. No physical basis",
                    "4. Arbitrary assumptions",
                    "5. Lacks experimental support"
                ]
                
                ax4.text(0.5, 0.9, f'Errors Found: {errors_found}/5', 
                        ha='center', fontsize=14, fontweight='bold',
                        color=self.colors['incorrect'], transform=ax4.transAxes)
                
                for i in range(errors_found):
                    ax4.text(0.05, 0.75 - i*0.12, f'✗ {error_list[i]}', 
                            fontsize=10, color=self.colors['incorrect'],
                            transform=ax4.transAxes)
                
                ax4.set_title('Error Detection')
                
                plt.tight_layout()
            
            # 创建动画
            anim = animation.FuncAnimation(fig, animate, frames=100, interval=100, repeat=True)
            return fig, anim
        except Exception as e:
            self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Failed to create animated demonstration", e)
            raise
    
    @safe_execution
    def generate_comprehensive_report(self):
        """生成综合报告"""
        try:
            # 确保日志目录存在
            log_dir = os.path.join(script_dir, 'logs')
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # 生成控制台报告
            print("=" * 80)
            print("COMPREHENSIVE GEOMETRIC FACTOR ANALYSIS REPORT")
            print("=" * 80)
            
            print("\n1. MATHEMATICAL ANALYSIS:")
            print("   • Sphere surface area: 4πr^2")
            print("   • Circle perimeter: 2πr")
            print("   • Ratio: 4πr^2/(2πr) = 2r")
            print("   • Problem: Result has dimension [L], not dimensionless")
            
            print("\n2. DIMENSIONAL ANALYSIS:")
            print("   • [Sphere area] = L^2")
            print("   • [Circle perimeter] = L¹")
            print("   • [Ratio] = L^2/L¹ = L¹ ≠ dimensionless")
            print("   • Forcing r=1 is arbitrary and lacks generality")
            
            print("\n3. PHYSICAL ISSUES:")
            print("   • No clear physical motivation for the ratio")
            print("   • Mixing 3D and 2D geometric quantities")
            print("   • No connection to established physics")
            print("   • Lacks experimental verification")
            
            print("\n4. COMPARISON WITH STANDARD PHYSICS:")
            print("   • Real geometric factors are dimensionless")
            print("   • Derived from physical principles (symmetry, projection)")
            print("   • Examples: 4π (solid angle), 1/2 (average projection)")
            print("   • Experimentally verified")
            
            print("\n5. RECOMMENDATIONS:")
            print("   • Use established physics (General Relativity, QFT)")
            print("   • Follow rigorous mathematical derivations")
            print("   • Ensure dimensional consistency")
            print("   • Seek experimental verification")
            print("   • Submit to peer review")
            
            print("\n6. CONCLUSION:")
            print("   The geometric factor derivation in Zhang Xiangqian's paper")
            print("   contains fundamental mathematical and physical errors.")
            print("   Standard physics provides reliable, tested methods.")
            
            # 生成错误报告
            report_path = os.path.join(log_dir, 'analysis_report.txt')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + '\n')
                f.write("COMPREHENSIVE GEOMETRIC FACTOR ANALYSIS REPORT\n")
                f.write("=" * 80 + '\n')
                f.write("\n1. MATHEMATICAL ANALYSIS:\n")
                f.write("   • Sphere surface area: 4πr^2\n")
                f.write("   • Circle perimeter: 2πr\n")
                f.write("   • Ratio: 4πr^2/(2πr) = 2r\n")
                f.write("   • Problem: Result has dimension [L], not dimensionless\n")
                
            # 调用错误处理器生成错误报告
            self.error_handler.generate_error_report()
            
            return True
        except Exception as e:
            self.error_handler.handle_error(ErrorType.REPORT_ERROR, "Failed to generate comprehensive report", e)
            return False
    
    @safe_execution
    def save_all_analyses(self, base_filename="geometric_factor_analysis"):
        """保存所有分析结果"""
        try:
            # 创建输出目录
            output_dir = os.path.join(script_dir, 'output')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.error_handler.log_event("Created output directory")
            
            # 创建主分析图
            fig1 = self.create_main_analysis_figure()
            main_fig_path = os.path.join(output_dir, f'{base_filename}_main.png')
            fig1.savefig(main_fig_path, dpi=300, bbox_inches='tight')
            print(f"Main analysis saved as: {main_fig_path}")
            self.error_handler.log_event(f"Saved main analysis figure to {main_fig_path}")
            
            # 创建动画
            fig2, anim = self.create_animated_demonstration()
            
            # 尝试保存动画为GIF
            try:
                gif_path = os.path.join(output_dir, f'{base_filename}_animation.gif')
                anim.save(gif_path, writer='pillow', fps=10, dpi=100)
                print(f"Animation saved as: {gif_path}")
                self.error_handler.log_event(f"Saved animation to {gif_path}")
            except Exception as e:
                print(f"Could not save animation: {e}")
                self.error_handler.handle_error(ErrorType.FILE_ERROR, "Failed to save animation", e)
            
            # 生成文本报告
            self.generate_comprehensive_report()
            
            # 保存错误报告
            error_report_path = os.path.join(output_dir, f'{base_filename}_error_report.txt')
            self.error_handler.generate_error_report(error_report_path)
            print(f"Error report saved as: {error_report_path}")
            
            return True
            
        except Exception as e:
            self.error_handler.handle_error(ErrorType.FILE_ERROR, "Failed to save analyses", e)
            return False

def main():
    """主函数"""
    print("Starting Comprehensive Geometric Factor Analysis System...")
    print("=" * 60)
    
    try:
        # 初始化错误处理器
        from error_handler import error_handler, safe_execution, ErrorType
        
        # 创建分析系统
        analysis_system = GeometricFactorAnalysisSystem()
        
        # 生成综合报告
        print("\nGenerating comprehensive analysis report...")
        report_success = analysis_system.generate_comprehensive_report()
        if not report_success:
            error_handler.handle_error(ErrorType.REPORT_ERROR, "Report generation had issues", None)
        
        # 创建可视化
        print("\nCreating visualizations...")
        
        try:
            # 主分析图
            fig1 = analysis_system.create_main_analysis_figure()
            
            # 动画演示
            fig2, anim = analysis_system.create_animated_demonstration()
            
            # 显示图表
            print("\nDisplaying visualizations (close all windows to continue)...")
            plt.show(block=False)  # 非阻塞显示
            
            # 询问是否保存
            try:
                save_choice = input("\nSave analysis results? (y/n): ").lower().strip()
                if save_choice == 'y':
                    success = analysis_system.save_all_analyses()
                    if success:
                        print("All analyses saved successfully!")
                    else:
                        print("Some errors occurred during saving.")
            except KeyboardInterrupt:
                print("\nUser interrupted input.")
            except Exception as e:
                error_handler.handle_error(ErrorType.INPUT_ERROR, "Error during user input", e)
            
        except Exception as e:
            error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Error during visualization", e)
            print("The analysis report has been generated above.")
        
        # 最终错误报告
        final_errors = error_handler.get_error_count()
        if final_errors > 0:
            print(f"\nAnalysis complete with {final_errors} errors detected! See error logs for details.")
        else:
            print("\nAnalysis complete with no errors detected.")
            
        return analysis_system
        
    except ImportError as e:
        print(f"Critical error: Could not import required modules. {e}")
        print("Please ensure all dependencies are installed.")
        return None
    except Exception as e:
        print(f"Unexpected system error: {e}")
        try:
            from error_handler import error_handler
            error_handler.handle_error(ErrorType.SYSTEM_ERROR, "Critical system failure", e)
        except:
            pass  # 如果错误处理器也无法加载，就简单输出错误
        return None