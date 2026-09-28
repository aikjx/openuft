#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论：简化顶尖学术图表生成系统
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置学术期刊级别的样式
plt.rcParams.update({
    'font.family': ['SimHei', 'Times New Roman', 'Microsoft YaHei'],
    'font.size': 12,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'grid.alpha': 0.3
})

class SimplifiedAcademicCharts:
    """简化顶尖学术图表生成器"""
    
    def __init__(self):
        # 物理参数
        self.r = 1.0  # 螺旋半径
        self.omega = 1.0  # 角速度
        self.p = 1.0  # 轴向速度
        self.c = 299792458  # 光速
        
        # 时间数组
        self.t = np.linspace(0, 4*np.pi, 1000)
        
        # 颜色主题
        self.colors = {
            'primary': '#2E86AB',    # 深蓝色
            'secondary': '#A23B72',  # 紫红色
            'tertiary': '#F18F01',   # 橙色
            'quaternary': '#C73E1D', # 红色
            'neutral': '#6C757D'    # 灰色
        }
        
    def chart_1_trajectory_3d(self):
        """图1：三维螺旋轨迹"""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 计算螺旋轨迹
        x = self.r * np.cos(self.omega * self.t)
        y = self.r * np.sin(self.omega * self.t)
        z = self.p * self.t
        
        # 主轨迹
        ax.plot(x, y, z, color=self.colors['primary'], linewidth=2.5)
        
        # 关键点标记
        key_times = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        key_labels = ['起点', '90°', '180°', '270°', '360°']
        
        for t_key, label in zip(key_times, key_labels):
            x_key = self.r * np.cos(self.omega * t_key)
            y_key = self.r * np.sin(self.omega * t_key)
            z_key = self.p * t_key
            ax.scatter(x_key, y_key, z_key, color=self.colors['tertiary'], s=80)
            ax.text(x_key, y_key, z_key + 0.3, label, fontsize=9, ha='center')
        
        # 坐标轴设置
        ax.set_xlabel('X (m)', fontsize=12)
        ax.set_ylabel('Y (m)', fontsize=12)
        ax.set_zlabel('Z (m)', fontsize=12)
        ax.set_title('三维圆柱螺旋运动轨迹\n$\\vec{R}(t) = r\\cos(\\omega t)\\hat{i} + r\\sin(\\omega t)\\hat{j} + pt\\hat{k}$', 
                    fontsize=14, pad=20)
        
        # 视角
        ax.view_init(elev=20, azim=45)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('01_三维螺旋运动轨迹.png')
        plt.close()
        
    def chart_2_velocity_analysis(self):
        """图2：速度分析"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 计算速度分量
        Vx = -self.r * self.omega * np.sin(self.omega * self.t)
        Vy = self.r * self.omega * np.cos(self.omega * self.t)
        Vz = np.full_like(self.t, self.p)
        V_magnitude = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        
        # 子图1：速度分量
        ax1 = axes[0, 0]
        ax1.plot(self.t, Vx, color=self.colors['primary'], linewidth=2, label='$V_x$')
        ax1.plot(self.t, Vy, color=self.colors['secondary'], linewidth=2, label='$V_y$')
        ax1.plot(self.t, Vz, color=self.colors['tertiary'], linewidth=2, label='$V_z$')
        ax1.set_xlabel('时间 $t$ (s)')
        ax1.set_ylabel('速度分量 (m/s)')
        ax1.set_title('速度分量随时间变化')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 子图2：速度模
        ax2 = axes[0, 1]
        theoretical_V = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        ax2.plot(self.t, V_magnitude, color=self.colors['quaternary'], linewidth=2.5, label='计算值')
        ax2.axhline(y=theoretical_V, color=self.colors['neutral'], linestyle='--', 
                   linewidth=2, label=f'理论值 $\\sqrt{{r^2\\omega^2 + p^2}} = {theoretical_V:.3f}$')
        ax2.set_xlabel('时间 $t$ (s)')
        ax2.set_ylabel('速度模 $|\\vec{V}|$ (m/s)')
        ax2.set_title('速度模恒定验证')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 子图3：速度矢量相位图
        ax3 = axes[1, 0]
        ax3.plot(Vx, Vy, color=self.colors['primary'], linewidth=1.5, alpha=0.8)
        ax3.scatter(Vx[0], Vy[0], color=self.colors['tertiary'], s=100, edgecolors='black', label='起点')
        ax3.scatter(Vx[-1], Vy[-1], color=self.colors['quaternary'], s=100, edgecolors='black', label='终点')
        ax3.set_xlabel('$V_x$ (m/s)')
        ax3.set_ylabel('$V_y$ (m/s)')
        ax3.set_title('XY平面速度矢量轨迹')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.axis('equal')
        
        # 子图4：速度大小分布直方图
        ax4 = axes[1, 1]
        ax4.hist(V_magnitude, bins=30, color=self.colors['primary'], alpha=0.7, edgecolor='black')
        ax4.axvline(x=theoretical_V, color=self.colors['tertiary'], linestyle='--', linewidth=2, 
                   label=f'理论值 = {theoretical_V:.3f}')
        ax4.set_xlabel('速度模 (m/s)')
        ax4.set_ylabel('频次')
        ax4.set_title('速度模分布')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('速度场完整分析', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('02_速度分量分析.png')
        plt.close()
        
    def chart_3_acceleration_analysis(self):
        """图3：加速度分析"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 计算加速度分量
        ax_array = -self.r * self.omega**2 * np.cos(self.omega * self.t)
        ay_array = -self.r * self.omega**2 * np.sin(self.omega * self.t)
        az_array = np.zeros_like(self.t)
        a_magnitude = np.sqrt(ax_array**2 + ay_array**2 + az_array**2)
        
        # 子图1：加速度分量
        ax1 = axes[0, 0]
        ax1.plot(self.t, ax_array, color=self.colors['primary'], linewidth=2, label='$a_x$')
        ax1.plot(self.t, ay_array, color=self.colors['secondary'], linewidth=2, label='$a_y$')
        ax1.plot(self.t, az_array, color=self.colors['neutral'], linewidth=2, label='$a_z$')
        ax1.set_xlabel('时间 $t$ (s)')
        ax1.set_ylabel('加速度分量 (m/s²)')
        ax1.set_title('加速度分量随时间变化')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 子图2：加速度模
        ax2 = axes[0, 1]
        theoretical_a = self.r * self.omega**2
        ax2.plot(self.t, a_magnitude, color=self.colors['quaternary'], linewidth=2.5, label='计算值')
        ax2.axhline(y=theoretical_a, color=self.colors['neutral'], linestyle='--', 
                   linewidth=2, label=f'理论值 $r\\omega^2 = {theoretical_a:.3f}$')
        ax2.set_xlabel('时间 $t$ (s)')
        ax2.set_ylabel('加速度模 $|\\vec{a}|$ (m/s²)')
        ax2.set_title('加速度模恒定验证')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 子图3：向心加速度分布
        ax3 = axes[1, 0]
        theta = np.linspace(0, 2*np.pi, 100)
        r_values = np.linspace(0.5, 2.0, 50)
        THETA, R = np.meshgrid(theta, r_values)
        
        # 向心加速度大小
        a_centripetal = self.r * self.omega**2
        Z = np.full_like(THETA, a_centripetal)
        
        contour = ax3.contourf(THETA, R, Z, levels=10, cmap='viridis', alpha=0.8)
        ax3.set_xlabel('角度 $\\theta$ (rad)')
        ax3.set_ylabel('半径 $r$ (m)')
        ax3.set_title('向心加速度分布')
        plt.colorbar(contour, ax=ax3, label='加速度 (m/s²)')
        
        # 子图4：加速度-速度相位关系
        ax4 = axes[1, 1]
        Vx = -self.r * self.omega * np.sin(self.omega * self.t)
        ax4.plot(self.t, Vx, color=self.colors['primary'], linewidth=2, label='$V_x$', alpha=0.8)
        ax4.plot(self.t, ax_array/self.r/self.omega, color=self.colors['secondary'], 
                linewidth=2, label='$a_x/(r\\omega)$', linestyle='--')
        ax4.set_xlabel('时间 $t$ (s)')
        ax4.set_ylabel('归一化值')
        ax4.set_title('速度-加速度相位关系')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('加速度场完整分析', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('03_加速度场分析.png')
        plt.close()
        
    def chart_4_energy_analysis(self):
        """图4：能量分析"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 计算能量分量
        V_magnitude = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        kinetic_energy = 0.5 * V_magnitude**2
        
        # 分解能量
        V_rot = self.r * self.omega
        V_lin = self.p
        KE_rot = 0.5 * V_rot**2
        KE_lin = 0.5 * V_lin**2
        
        # 子图1：能量分量分解
        ax1 = axes[0, 0]
        energy_total = np.full_like(self.t, kinetic_energy)
        ke_rot_array = np.full_like(self.t, KE_rot)
        ke_lin_array = np.full_like(self.t, KE_lin)
        
        ax1.fill_between(self.t, 0, ke_rot_array, color=self.colors['primary'], 
                        alpha=0.6, label='旋转动能')
        ax1.fill_between(self.t, ke_rot_array, energy_total, color=self.colors['secondary'], 
                        alpha=0.6, label='直线动能')
        ax1.set_xlabel('时间 $t$ (s)')
        ax1.set_ylabel('动能密度 (J/kg)')
        ax1.set_title('动能分量分解')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 子图2：能量守恒验证
        ax2 = axes[0, 1]
        ax2.plot(self.t, energy_total, color=self.colors['tertiary'], linewidth=2.5)
        ax2.axhline(y=kinetic_energy, color=self.colors['neutral'], linestyle='--', 
                   linewidth=2, label=f'理论值 $E = {kinetic_energy:.3f}$ J/kg')
        ax2.set_xlabel('时间 $t$ (s)')
        ax2.set_ylabel('总动能 (J/kg)')
        ax2.set_title('能量守恒验证')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 子图3：能量分配饼图
        ax3 = axes[1, 0]
        rot_ratio = KE_rot / kinetic_energy
        lin_ratio = KE_lin / kinetic_energy
        
        ax3.pie([rot_ratio, lin_ratio], 
                labels=['旋转分量', '直线分量'],
                colors=[self.colors['primary'], self.colors['secondary']],
                autopct='%1.1f%%',
                startangle=90)
        ax3.set_title('动能分配比例')
        
        # 子图4：参数-能量关系
        ax4 = axes[1, 1]
        omega_range = np.linspace(0.5, 2.0, 100)
        energy_curve = 0.5 * (self.r**2 * omega_range**2 + self.p**2)
        
        ax4.plot(omega_range, energy_curve, color=self.colors['quaternary'], linewidth=2.5)
        ax4.scatter([self.omega], [kinetic_energy], color=self.colors['tertiary'], 
                   s=100, edgecolors='black', linewidth=2, label='当前参数', zorder=5)
        ax4.set_xlabel('角速度 $\\omega$ (rad/s)')
        ax4.set_ylabel('总动能 (J/kg)')
        ax4.set_title('角速度-能量关系')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('能量守恒定律验证', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('04_能量守恒分析.png')
        plt.close()
        
    def chart_5_physics_interpretation(self):
        """图5：物理诠释"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 子图1：场强分量
        ax1 = axes[0, 0]
        theta = np.linspace(0, 2*np.pi, 100)
        
        # 电场（直线分量）
        E_magnitude = self.p
        ax1.axhline(y=E_magnitude, color=self.colors['primary'], linewidth=3, 
                   label=f'电场强度 $E = {E_magnitude:.1f}$')
        
        # 磁场（旋转分量）
        B_magnitude = self.r * self.omega
        ax1.plot(theta, B_magnitude * np.cos(theta), 
                color=self.colors['secondary'], linewidth=3, 
                label='磁场分量 $B(\\theta)$')
        
        ax1.set_xlabel('相位 $\\theta$ (rad)')
        ax1.set_ylabel('场强 (相对单位)')
        ax1.set_title('电磁场分量变化')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 2*np.pi)
        
        # 子图2：引力场分布
        ax2 = axes[0, 1]
        r_range = np.linspace(0.5, 3.0, 100)
        g_field = self.r * self.omega**2 * (self.r / r_range)**2
        
        ax2.plot(r_range, g_field, color=self.colors['tertiary'], linewidth=2.5)
        ax2.scatter([self.r], [self.r * self.omega**2], 
                   color=self.colors['quaternary'], s=100, 
                   edgecolors='black', linewidth=2, label='参考点', zorder=5)
        ax2.set_xlabel('距离 $r$ (m)')
        ax2.set_ylabel('引力场强度 (相对单位)')
        ax2.set_title('引力场径向分布 $\\propto 1/r^2$')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')
        
        # 子图3：统一场相位关系
        ax3 = axes[1, 0]
        phase = np.linspace(0, 2*np.pi, 100)
        
        # 归一化的场分量
        E_normalized = np.ones_like(phase) * self.p / np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        B_normalized = self.r * self.omega * np.cos(phase) / np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        g_normalized = -np.sin(phase)  # 归一化的引力分量
        
        ax3.plot(phase, E_normalized, color=self.colors['primary'], 
                linewidth=2, label='电场分量')
        ax3.plot(phase, B_normalized, color=self.colors['secondary'], 
                linewidth=2, label='磁场分量')
        ax3.plot(phase, g_normalized, color=self.colors['tertiary'], 
                linewidth=2, label='引力分量')
        
        ax3.set_xlabel('相位 $\\omega t$ (rad)')
        ax3.set_ylabel('归一化场强')
        ax3.set_title('统一场相位关系')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # 子图4：场强矢量图
        ax4 = axes[1, 1]
        # 创建二维网格表示场分布
        x = np.linspace(-2, 2, 15)
        y = np.linspace(-2, 2, 15)
        X, Y = np.meshgrid(x, y)
        
        # 计算每个点的场强（简化模型）
        R = np.sqrt(X**2 + Y**2)
        R[R < 0.5] = 0.5
        
        # 引力场（指向中心）
        Ex = -X / R**2
        Ey = -Y / R**2
        
        magnitude = np.sqrt(Ex**2 + Ey**2)
        
        ax4.quiver(X, Y, Ex, Ey, magnitude, cmap='viridis', alpha=0.7)
        circle = plt.Circle((0, 0), self.r, fill=False, edgecolor=self.colors['quaternary'], 
                           linewidth=2, linestyle='--')
        ax4.add_patch(circle)
        ax4.set_xlabel('X (m)')
        ax4.set_ylabel('Y (m)')
        ax4.set_title('引力场矢量分布')
        ax4.set_aspect('equal')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('物理场的几何起源诠释', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('05_物理场诠释.png')
        plt.close()
        
    def chart_6_data_table(self):
        """图6：数据表格"""
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # 计算转一圈的关键数据
        key_times = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]) / self.omega
        key_labels = ['起点', '90°', '180°', '270°', '360°']
        
        # 计算各参数
        angles = self.omega * key_times
        x_coords = self.r * np.cos(angles)
        y_coords = self.r * np.sin(angles)
        z_coords = self.p * key_times
        
        vx = -self.r * self.omega * np.sin(angles)
        vy = self.r * self.omega * np.cos(angles)
        vz = np.full_like(key_times, self.p)
        v_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
        
        ax_comps = -self.r * self.omega**2 * np.cos(angles)
        ay_comps = -self.r * self.omega**2 * np.sin(angles)
        az_comps = np.zeros_like(key_times)
        a_magnitude = np.sqrt(ax_comps**2 + ay_comps**2 + az_comps**2)
        
        # 创建表格数据
        table_data = []
        for i, (label, t, angle, x, y, z) in enumerate(zip(key_labels, key_times, angles, x_coords, y_coords, z_coords)):
            row = [
                label,
                f'{t:.3f}',
                f'{angle:.3f}',
                f'{x:.3f}',
                f'{y:.3f}',
                f'{z:.3f}',
                f'{vx[i]:.3f}',
                f'{vy[i]:.3f}',
                f'{vz[i]:.3f}',
                f'{v_magnitude[i]:.3f}',
                f'{ax_comps[i]:.3f}',
                f'{ay_comps[i]:.3f}',
                f'{az_comps[i]:.3f}',
                f'{a_magnitude[i]:.3f}'
            ]
            table_data.append(row)
        
        # 创建表格
        columns = [
            '阶段', '时间(s)', '角度(rad)', 
            'X(m)', 'Y(m)', 'Z(m)',
            'Vx(m/s)', 'Vy(m/s)', 'Vz(m/s)', '|V|(m/s)',
            'ax(m/s²)', 'ay(m/s²)', 'az(m/s²)', '|a|(m/s²)'
        ]
        
        table = ax.table(cellText=table_data, colLabels=columns, 
                        cellLoc='center', loc='center',
                        colWidths=[0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 
                                  0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07])
        
        # 设置表格样式
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # 设置表头样式
        for i in range(len(columns)):
            table[(0, i)].set_facecolor(self.colors['primary'])
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # 设置关键行的背景色
        for i in range(1, len(table_data) + 1):
            if i % 2 == 0:
                for j in range(len(columns)):
                    table[(i, j)].set_facecolor('#f0f0f0')
        
        # 添加标题和说明
        title_text = '圆柱螺旋运动"转一圈"完整数据表\n'
        title_text += f'参数设置: $r = {self.r}$ m, $\\omega = {self.omega}$ rad/s, $p = {self.p}$ m/s\n'
        title_text += f'周期: $T = 2\\pi/\\omega = {2*np.pi/self.omega:.3f}$ s, '
        title_text += f'螺距: $p \\cdot T = {self.p * 2*np.pi/self.omega:.3f}$ m'
        
        fig.text(0.5, 0.95, title_text, ha='center', va='top', fontsize=14, 
                weight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.savefig('06_转一圈完整数据表.png')
        plt.close()
        
    def generate_all_charts(self):
        """生成所有顶尖学术图表"""
        print("=" * 60)
        print("开始生成顶尖学术图表...")
        print("=" * 60)
        
        charts_info = [
            ("三维螺旋运动轨迹", self.chart_1_trajectory_3d),
            ("速度分量分析", self.chart_2_velocity_analysis),
            ("加速度场分析", self.chart_3_acceleration_analysis),
            ("能量守恒分析", self.chart_4_energy_analysis),
            ("物理场诠释", self.chart_5_physics_interpretation),
            ("转一圈完整数据表", self.chart_6_data_table)
        ]
        
        for i, (name, func) in enumerate(charts_info, 1):
            print(f"正在生成第{i}张图: {name}")
            try:
                func()
                print(f"✓ {name} 生成成功")
            except Exception as e:
                print(f"✗ {name} 生成失败: {str(e)}")
        
        print("=" * 60)
        print("所有顶尖学术图表生成完成！")
        print("文件保存格式：PNG，300 DPI，期刊级别质量")
        print("=" * 60)

def main():
    """主函数"""
    generator = SimplifiedAcademicCharts()
    generator.generate_all_charts()

if __name__ == "__main__":
    main()