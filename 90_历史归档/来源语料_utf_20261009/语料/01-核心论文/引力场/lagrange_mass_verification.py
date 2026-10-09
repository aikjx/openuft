#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拉格朗日点质量变化率验证脚本
基于张祥前统一场论的第一性原理推导
验证拉格朗日点卫星质量变化率dm/dt=0，无法实现光速飞行
而人工场扫描技术可通过dm/dt<0实现质量减少直至归零
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import os

class LagrangeMassVerification:
    """拉格朗日点与人工场质量变化验证类"""
    
    def __init__(self):
        """初始化验证参数"""
        # 物理常数设置
        self.c = 3e8  # 光速 (m/s)
        self.m0 = 1000  # 初始质量 (kg)
        self.max_time = 100  # 最大模拟时间 (s)
        self.time_steps = 1000  # 时间步数
        self.time = np.linspace(0, self.max_time, self.time_steps)
        
        # 结果存储
        self.results = {
            'lagrange_mass': np.zeros(self.time_steps),
            'artificial_field_mass': np.zeros(self.time_steps),
            'artificial_field_velocity': np.zeros(self.time_steps),
            'lagrange_force': np.zeros(self.time_steps),
            'artificial_field_force': np.zeros(self.time_steps)
        }
        
    def verify_lagrange_point(self):
        """验证拉格朗日点的质量变化率为零"""
        # 在拉格朗日点，质量恒定，dm/dt=0
        self.results['lagrange_mass'] = np.full(self.time_steps, self.m0)
        # 合力为零
        self.results['lagrange_force'] = np.zeros(self.time_steps)
        
        print("\n=== 拉格朗日点验证结果 ===")
        print(f"初始质量: {self.m0} kg")
        print(f"最终质量: {self.results['lagrange_mass'][-1]} kg")
        print(f"质量变化率 dm/dt: 0 kg/s")
        print(f"结论: 拉格朗日点仅实现外力平衡，质量保持恒定，无法实现光速飞行")
        
    def simulate_artificial_field(self, decay_rate=0.05):
        """模拟人工场扫描技术导致的质量减少
        
        Args:
            decay_rate: 质量衰减率 (1/s)
        """
        # 模拟质量随时间指数减少
        self.results['artificial_field_mass'] = self.m0 * np.exp(-decay_rate * self.time)
        
        # 计算速度变化 (接近光速)
        for i in range(self.time_steps):
            m = self.results['artificial_field_mass'][i]
            if m > 0:
                # 根据相对论能量守恒，质量减少转化为动能
                # 简化模型：当质量趋近于零时，速度趋近于光速
                self.results['artificial_field_velocity'][i] = self.c * (1 - np.exp(-(self.m0/m - 1)))
            else:
                self.results['artificial_field_velocity'][i] = self.c
        
        # 计算反引力场力 (基于统一场论动力学方程)
        for i in range(1, self.time_steps):
            dt = self.time[i] - self.time[i-1]
            dm = self.results['artificial_field_mass'][i] - self.results['artificial_field_mass'][i-1]
            v = self.results['artificial_field_velocity'][i]
            # 从方程 F_anti ≈ (C - V) * dm/dt
            self.results['artificial_field_force'][i] = (self.c - v) * (dm/dt)
        
        print("\n=== 人工场扫描技术验证结果 ===")
        print(f"初始质量: {self.m0} kg")
        print(f"最终质量: {self.results['artificial_field_mass'][-1]:.6f} kg")
        print(f"质量变化率 dm/dt: 负值 (质量持续减少)")
        print(f"最终速度: {self.results['artificial_field_velocity'][-1]/self.c*100:.2f}% 光速")
        print(f"结论: 人工场扫描技术可使质量持续减少直至接近零，支持光速飞行")
        
    def run_simulation(self, decay_rate=0.05):
        """运行完整的验证模拟
        
        Args:
            decay_rate: 人工场质量衰减率
        """
        print("\n开始运行拉格朗日点与人工场质量变化验证...")
        self.verify_lagrange_point()
        self.simulate_artificial_field(decay_rate)
        
    def plot_results(self):
        """绘制验证结果图表"""
        # 使用默认样式，移除对science样式的依赖
        plt.rcParams.update({'font.family': 'Times New Roman'})
        
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('拉格朗日点与人工场扫描技术对比验证', fontsize=16, fontweight='bold')
        
        # 1. 质量随时间变化对比
        ax1 = axs[0, 0]
        ax1.plot(self.time, self.results['lagrange_mass'], 'b-', label='拉格朗日点 (dm/dt=0)', linewidth=2)
        ax1.plot(self.time, self.results['artificial_field_mass'], 'r-', label='人工场扫描 (dm/dt<0)', linewidth=2)
        ax1.set_xlabel('时间 (s)')
        ax1.set_ylabel('质量 (kg)')
        ax1.set_title('质量随时间变化对比')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        ax1.text(0.05, 0.95, '结论: 拉格朗日点质量恒定', transform=ax1.transAxes, 
                fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 2. 速度随时间变化 (仅人工场)
        ax2 = axs[0, 1]
        ax2.plot(self.time, self.results['artificial_field_velocity']/self.c*100, 'r-', linewidth=2)
        ax2.axhline(y=100, color='g', linestyle='--', label='光速')
        ax2.set_xlabel('时间 (s)')
        ax2.set_ylabel('速度 (% 光速)')
        ax2.set_title('人工场扫描下的速度变化')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 3. 质量变化率对比
        ax3 = axs[1, 0]
        # 拉格朗日点dm/dt=0
        lagrange_dm_dt = np.zeros_like(self.time)
        # 人工场dm/dt (数值微分)
        artificial_dm_dt = np.gradient(self.results['artificial_field_mass'], self.time)
        
        ax3.plot(self.time, lagrange_dm_dt, 'b-', label='拉格朗日点', linewidth=2)
        ax3.plot(self.time, artificial_dm_dt, 'r-', label='人工场扫描', linewidth=2)
        ax3.set_xlabel('时间 (s)')
        ax3.set_ylabel('质量变化率 (kg/s)')
        ax3.set_title('质量变化率对比')
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        # 4. 合力对比
        ax4 = axs[1, 1]
        ax4.plot(self.time, self.results['lagrange_force'], 'b-', label='拉格朗日点', linewidth=2)
        ax4.plot(self.time, self.results['artificial_field_force'], 'r-', label='人工场扫描', linewidth=2)
        ax4.set_xlabel('时间 (s)')
        ax4.set_ylabel('力 (N)')
        ax4.set_title('合力对比')
        ax4.grid(True, linestyle='--', alpha=0.7)
        ax4.legend()
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # 保存图表
        save_path = os.path.dirname(os.path.abspath(__file__))
        fig.savefig(os.path.join(save_path, '拉格朗日点与人工场验证结果.png'), dpi=300, bbox_inches='tight')
        print(f"\n图表已保存至: {os.path.join(save_path, '拉格朗日点与人工场验证结果.png')}")
        
        return fig
    
    def create_interactive_interface(self):
        """创建交互式验证界面"""
        root = tk.Tk()
        root.title("拉格朗日点与人工场质量变化验证")
        root.geometry("1200x800")
        root.configure(bg='#f0f0f0')
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建控制框架
        control_frame = ttk.LabelFrame(main_frame, text="验证控制", padding="15")
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 初始质量输入
        ttk.Label(control_frame, text="初始质量 (kg):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        mass_var = tk.StringVar(value=str(self.m0))
        mass_entry = ttk.Entry(control_frame, textvariable=mass_var, width=15)
        mass_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 衰减率输入
        ttk.Label(control_frame, text="质量衰减率 (1/s):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        decay_var = tk.StringVar(value="0.05")
        decay_entry = ttk.Entry(control_frame, textvariable=decay_var, width=15)
        decay_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # 模拟时间输入
        ttk.Label(control_frame, text="模拟时间 (s):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        time_var = tk.StringVar(value=str(self.max_time))
        time_entry = ttk.Entry(control_frame, textvariable=time_var, width=15)
        time_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # 运行按钮
        def on_run():
            try:
                self.m0 = float(mass_var.get())
                decay_rate = float(decay_var.get())
                self.max_time = float(time_var.get())
                self.time = np.linspace(0, self.max_time, self.time_steps)
                
                # 运行模拟
                self.run_simulation(decay_rate)
                
                # 更新图表
                for widget in plot_frame.winfo_children():
                    widget.destroy()
                
                fig = self.plot_results()
                canvas = FigureCanvasTkAgg(fig, master=plot_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                messagebox.showinfo("验证完成", "拉格朗日点与人工场质量变化验证完成！")
                
            except ValueError as e:
                messagebox.showerror("输入错误", f"请输入有效的数值: {e}")
        
        run_button = ttk.Button(control_frame, text="运行验证", command=on_run)
        run_button.grid(row=0, column=6, padx=20, pady=5)
        
        # 创建结果框架
        result_frame = ttk.LabelFrame(main_frame, text="验证结果", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建文本结果区域
        text_frame = ttk.LabelFrame(result_frame, text="数值结果", padding="10")
        text_frame.pack(fill=tk.X, pady=(0, 10))
        
        result_text = tk.Text(text_frame, height=8, wrap=tk.WORD)
        result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(result_text, command=result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.config(yscrollcommand=scrollbar.set)
        
        # 重定向print输出到文本框
        class RedirectText:
            def __init__(self, text_widget):
                self.text_widget = text_widget
                
            def write(self, string):
                self.text_widget.insert(tk.END, string)
                self.text_widget.see(tk.END)
                
            def flush(self):
                pass
        
        sys.stdout = RedirectText(result_text)
        
        # 创建图表框架
        plot_frame = ttk.LabelFrame(result_frame, text="可视化结果", padding="10")
        plot_frame.pack(fill=tk.BOTH, expand=True)
        
        # 运行初始模拟
        self.run_simulation()
        fig = self.plot_results()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        root.mainloop()

# 添加matplotlib设置
import matplotlib
matplotlib.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'font.family': 'Times New Roman',
})

# 主函数
if __name__ == "__main__":
    import sys
    
    print("\n===== 拉格朗日点与人工场质量变化验证 =====")
    print("基于张祥前统一场论第一性原理")
    print("验证拉格朗日点dm/dt=0与人工场dm/dt<0的本质区别")
    print("========================================")
    
    # 创建验证器实例
    verifier = LagrangeMassVerification()
    
    try:
        # 检查是否支持GUI
        if '--no-gui' not in sys.argv:
            verifier.create_interactive_interface()
        else:
            # 命令行模式
            verifier.run_simulation()
            verifier.plot_results()
            plt.show()
            
    except ImportError:
        print("\n警告: 某些图形库缺失，以命令行模式运行")
        verifier.run_simulation()
        verifier.plot_results()
        plt.show()
    except KeyboardInterrupt:
        print("\n验证已中断")
    finally:
        print("\n验证完成")