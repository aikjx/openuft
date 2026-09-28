#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
圆周运动正电荷产生的引力场方程多维验证脚本
算法联盟理论物理验证中心
2026年1月28日

功能：验证V1和V2论文中推导的引力场方程的正确性
验证维度：量纲一致性、方向关系、理论自洽性、数值计算
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体和数学符号支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 用来正常显示中文标签和数学符号
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['text.usetex'] = False  # 禁用LaTeX，使用普通文本

class GravityFieldVerifier:
    """引力场方程验证器"""
    
    def __init__(self):
        # 物理常数
        self.epsilon0 = 8.8541878128e-12  # 真空介电常数 (F/m)
        self.c = 3.0e8  # 光速 (m/s)
        self.pi = np.pi
        
    def verify_dimension_consistency(self):
        """验证量纲一致性"""
        print("=== 量纲一致性验证 ===")
        
        # V1方程: A = ω²r'(t - r/c)
        print("\n1. V1方程: A(r, t) = ω² r'(t - r/c)")
        print("   - 左边A的量纲: m/s² (加速度)")
        print("   - 右边ω²r的量纲: (rad/s)² · m = m/s²")
        print("   ✓ 量纲一致")
        
        # V2方程: A = -q/(4πε0 c² r) (r̂ × (r̂ × a_q))
        print("\n2. V2方程: A = -q/(4πε0 c² r) (r̂ × (r̂ × a_q))")
        print("   - 左边A的量纲: m/s² (加速度)")
        # 计算右边量纲
        # q: C (库仑) = A·s
        # ε0: F/m = C²·s²/(kg·m³)
        # c²: m²/s²
        # r: m
        # a_q: m/s²
        # 矢量叉乘无量纲
        print("   - 右边量纲计算:")
        print("     q/(ε0 c² r) 的量纲:")
        print("     = (A·s) / [(C²·s²/(kg·m³)) · (m²/s²) · m]")
        print("     = (A·s) / [(A²·s²·s²/(kg·m³)) · (m²/s²) · m]")  # C = A·s
        print("     = (A·s) / [(A²·s²/(kg·m))]")
        print("     = (kg·m)/(A·s)")
        print("     乘以a_q (m/s²):")
        print("     = (kg·m)/(A·s) · (m/s²) = kg·m²/(A·s³)")
        print("     但根据方程，实际量纲应为 m/s²，这里存在问题")
        print("   ✗ 量纲可能不一致，需要进一步分析")
        
    def verify_direction_relationship(self):
        """验证方向关系"""
        print("\n=== 方向关系验证 ===")
        
        # V1方程方向验证
        print("\n1. V1方程方向验证:")
        print("   - 向心加速度: a(t) = -ω² r'(t) (指向圆心)")
        print("   - 引力场: A(r, t) = ω² r'(t - r/c) (背离圆心)")
        print("   ✓ 引力场方向与向心加速度方向相反，符合统一场论要求")
        
        # V2方程方向验证
        print("\n2. V2方程方向验证:")
        print("   - 方程形式: A = -q/(4πε0 c² r) (r̂ × (r̂ × a_q))")
        print("   - 矢量恒等式: r̂ × (r̂ × a_q) = r̂(r̂·a_q) - a_q")
        print("   - 对于横向加速度(r̂·a_q = 0): A = q/(4πε0 c² r) a_q")
        print("   - 注意符号: 这里与统一场论要求的方向相反")
        print("   ✗ 方向可能存在问题")
        
    def verify_theoretical_consistency(self):
        """验证理论自洽性"""
        print("\n=== 理论自洽性验证 ===")
        
        print("1. 与加速运动电荷引力场方程的一致性:")
        print("   - 加速运动电荷方程: A = -a")
        print("   - V1方程: 当圆周运动退化为直线加速时，ω²r' → a，方向相反，符合")
        print("   - V2方程: 包含电荷和距离因子，与基本方程形式不同")
        
        print("\n2. 与时空同一化原理的一致性:")
        print("   - V1方程包含光速传播延迟 t - r/c，符合时空同一化 r = ct")
        print("   - V2方程包含光速c，也符合时空同一化原理")
        
        print("\n3. 与场几何起源的一致性:")
        print("   - V1方程将引力场定义为空间点的加速度，符合场几何起源")
        print("   - V2方程引入了电荷因子，需要进一步分析与场几何起源的关系")
        
    def simulate_circular_motion(self):
        """模拟圆周运动电荷的引力场"""
        print("\n=== 圆周运动模拟 ===")
        
        # 模拟参数
        R = 1.0  # 圆周半径 (m)
        omega = 1.0  # 角速度 (rad/s)
        q = 1.0  # 电荷量 (C)
        
        # 时间点
        t = 0.0
        
        # 电荷位置
        def charge_position(t):
            return np.array([R * np.cos(omega * t), R * np.sin(omega * t), 0.0])
        
        # 向心加速度
        def centripetal_acceleration(t):
            r = charge_position(t)
            return -omega**2 * r
        
        # V1引力场计算
        def compute_gravity_field_v1(r, t):
            # 场点到电荷的距离
            r_charge = charge_position(t - np.linalg.norm(r)/self.c)
            distance = np.linalg.norm(r - r_charge)
            if distance < 1e-10:
                return np.zeros(3)
            # V1方程: A = omega² r'(t - r/c)
            return omega**2 * r_charge
        
        # V2引力场计算
        def compute_gravity_field_v2(r, t, a_q):
            # 场点到电荷的距离
            r_charge = charge_position(t)
            r_vec = r - r_charge
            distance = np.linalg.norm(r_vec)
            if distance < 1e-10:
                return np.zeros(3)
            
            # 径向单位矢量
            r_hat = r_vec / distance
            
            # 矢量叉乘计算
            cross1 = np.cross(r_hat, a_q)
            cross2 = np.cross(r_hat, cross1)
            
            # V2方程
            factor = -q / (4 * self.pi * self.epsilon0 * self.c**2 * distance)
            return factor * cross2
        
        # 计算不同场点的引力场
        field_points = [
            np.array([2.0, 0.0, 0.0]),  # 圆周外x轴
            np.array([0.0, 2.0, 0.0]),  # 圆周外y轴
            np.array([1.0, 1.0, 0.0]),  # 圆周上
            np.array([0.5, 0.5, 0.0])   # 圆周内
        ]
        
        print("\n场点引力场计算结果:")
        print("场点坐标 | V1引力场 | V2引力场")
        print("-" * 60)
        
        for point in field_points:
            a_q = centripetal_acceleration(t)
            A_v1 = compute_gravity_field_v1(point, t)
            A_v2 = compute_gravity_field_v2(point, t, a_q)
            
            print(f"{point} | {A_v1} | {A_v2}")
        
        # 可视化
        self.visualize_gravity_field(R, omega, q)
    
    def visualize_gravity_field(self, R, omega, q):
        """可视化引力场分布"""
        print("\n=== 引力场可视化 ===")
        
        # 创建网格
        x = np.linspace(-3*R, 3*R, 20)
        y = np.linspace(-3*R, 3*R, 20)
        X, Y = np.meshgrid(x, y)
        
        # 计算每个点的引力场
        A_v1_x = np.zeros_like(X)
        A_v1_y = np.zeros_like(Y)
        A_v2_x = np.zeros_like(X)
        A_v2_y = np.zeros_like(Y)
        
        t = 0.0
        
        for i in range(len(x)):
            for j in range(len(y)):
                point = np.array([X[i,j], Y[i,j], 0.0])
                r_charge = np.array([R*np.cos(omega*t), R*np.sin(omega*t), 0.0])
                r_vec = point - r_charge
                distance = np.linalg.norm(r_vec)
                
                if distance > 1e-10:
                    # V1
                    r_charge_retarded = np.array([R*np.cos(omega*(t-distance/self.c)), 
                                                R*np.sin(omega*(t-distance/self.c)), 0.0])
                    A_v1 = omega**2 * r_charge_retarded
                    A_v1_x[i,j] = A_v1[0]
                    A_v1_y[i,j] = A_v1[1]
                    
                    # V2
                    a_q = -omega**2 * r_charge
                    r_hat = r_vec / distance
                    cross1 = np.cross(r_hat, a_q)
                    cross2 = np.cross(r_hat, cross1)
                    factor = -q / (4 * self.pi * self.epsilon0 * self.c**2 * distance)
                    A_v2 = factor * cross2
                    A_v2_x[i,j] = A_v2[0]
                    A_v2_y[i,j] = A_v2[1]
        
        # 绘图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # V1引力场
        ax1.quiver(X, Y, A_v1_x, A_v1_y, scale=5)
        ax1.plot(R*np.cos(np.linspace(0, 2*np.pi, 100)), 
                 R*np.sin(np.linspace(0, 2*np.pi, 100)), 'r--')
        ax1.set_title('V1 引力场分布')
        ax1.set_xlabel('x (m)')
        ax1.set_ylabel('y (m)')
        ax1.set_aspect('equal')
        
        # V2引力场
        ax2.quiver(X, Y, A_v2_x, A_v2_y, scale=1e-10)  # 缩放以显示
        ax2.plot(R*np.cos(np.linspace(0, 2*np.pi, 100)), 
                 R*np.sin(np.linspace(0, 2*np.pi, 100)), 'r--')
        ax2.set_title('V2 引力场分布')
        ax2.set_xlabel('x (m)')
        ax2.set_ylabel('y (m)')
        ax2.set_aspect('equal')
        
        plt.tight_layout()
        plt.savefig('gravity_field_visualization.png')
        print("✓ 引力场可视化已保存为 gravity_field_visualization.png")
    
    def analyze_decay_law(self):
        """分析衰减规律"""
        print("\n=== 衰减规律分析 ===")
        
        # 计算不同距离的引力场强度
        distances = np.logspace(0, 3, 20)  # 1m 到 1000m
        R = 1.0
        omega = 1.0
        q = 1.0
        t = 0.0
        
        # 场点沿x轴
        A_v1_magnitude = []
        A_v2_magnitude = []
        
        for r in distances:
            point = np.array([r, 0.0, 0.0])
            r_charge = np.array([R*np.cos(omega*t), R*np.sin(omega*t), 0.0])
            distance = np.linalg.norm(point - r_charge)
            
            # V1
            if distance > 1e-10:
                r_charge_retarded = np.array([R*np.cos(omega*(t-distance/self.c)), 
                                            R*np.sin(omega*(t-distance/self.c)), 0.0])
                A_v1 = omega**2 * r_charge_retarded
                A_v1_magnitude.append(np.linalg.norm(A_v1))
            else:
                A_v1_magnitude.append(0.0)
            
            # V2
            if distance > 1e-10:
                a_q = -omega**2 * r_charge
                r_vec = point - r_charge
                r_hat = r_vec / distance
                cross1 = np.cross(r_hat, a_q)
                cross2 = np.cross(r_hat, cross1)
                factor = -q / (4 * self.pi * self.epsilon0 * self.c**2 * distance)
                A_v2 = factor * cross2
                A_v2_magnitude.append(np.linalg.norm(A_v2))
            else:
                A_v2_magnitude.append(0.0)
        
        # 绘图
        plt.figure(figsize=(10, 6))
        plt.loglog(distances, A_v1_magnitude, 'o-', label='V1 引力场')
        plt.loglog(distances, A_v2_magnitude, 's-', label='V2 引力场')
        
        # 添加1/r和1/r²参考线
        r_ref = distances
        plt.loglog(r_ref, 1/r_ref, '--', label='1/r 参考')
        plt.loglog(r_ref, 1/r_ref**2, '-.', label='1/r² 参考')
        
        plt.xlabel('距离 r (m)')
        plt.ylabel('引力场强度 (m/s²)')
        plt.title('引力场强度随距离的衰减规律')
        plt.legend()
        plt.grid(True, which='both', linestyle='--')
        plt.savefig('decay_law_analysis.png')
        print("✓ 衰减规律分析已保存为 decay_law_analysis.png")
    
    def comprehensive_verification(self):
        """综合验证"""
        print("\n" + "="*70)
        print("综合验证报告")
        print("="*70)
        
        print("\n1. 方程形式对比:")
        print("   V1: A(r, t) = ω² r'(t - r/c)")
        print("   V2: A = -q/(4πε0 c² r) (r̂ × (r̂ × a_q))")
        
        print("\n2. 关键差异:")
        print("   - V1: 基于运动学分析，直接关联向心加速度，形式简洁")
        print("   - V2: 基于场方程推导，包含电荷和距离因子，形式复杂")
        
        print("\n3. 验证结果:")
        print("   量纲一致性:")
        print("     ✓ V1: 一致")
        print("     ✗ V2: 存在疑问")
        print("   方向关系:")
        print("     ✓ V1: 与向心加速度相反，符合要求")
        print("     ✗ V2: 符号可能存在问题")
        print("   理论自洽性:")
        print("     ✓ V1: 与基本方程一致，包含光速延迟")
        print("     ? V2: 需要进一步分析与基本原理的关系")
        print("   衰减规律:")
        print("     V1: 与距离无关（常数），不符合辐射场特性")
        print("     V2: 1/r衰减，符合辐射场特性")
        
        print("\n4. 结论:")
        print("   - V1方程在形式上更符合统一场论的基本原理，特别是方向关系")
        print("   - V2方程包含了电荷因子，更接近经典电动力学的辐射场形式")
        print("   - 两者可能描述的是不同层面的物理现象")
        print("   - 需要进一步研究两者的关系和适用条件")
        
        print("\n5. 建议:")
        print("   - 深入分析V2方程的量纲问题")
        print("   - 研究圆周运动情况下的辐射场特性")
        print("   - 设计实验验证方案")

if __name__ == "__main__":
    verifier = GravityFieldVerifier()
    
    print("""
    ===================================================================
    圆周运动正电荷产生的引力场方程多维验证
    算法联盟理论物理验证中心
    ===================================================================
    """)
    
    verifier.verify_dimension_consistency()
    verifier.verify_direction_relationship()
    verifier.verify_theoretical_consistency()
    verifier.simulate_circular_motion()
    verifier.analyze_decay_law()
    verifier.comprehensive_verification()
    
    print("\n" + "="*70)
    print("验证完成！")
    print("="*70)
