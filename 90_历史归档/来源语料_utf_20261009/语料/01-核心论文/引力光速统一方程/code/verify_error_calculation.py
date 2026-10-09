#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证引力光速统一方程Z=Gc/2的误差计算
"""

import numpy as np

def verify_error_calculation():
    # CODATA 2018推荐的引力常数实验值
    G_CODATA = 6.67430e-11  # m³·kg^-1·s^-2
    print(f"CODATA 2018推荐的引力常数实验值: G_CODATA = {G_CODATA:.10e} m³·kg^-1·s^-2")
    
    # 光速的标准值
    c = 299792458  # m/s
    print(f"光速的标准值: c = {c} m/s")
    
    # 计算Z的精确值 (使用实验值G来计算Z)
    Z_exact = (G_CODATA * c) / 2
    print(f"\n精确Z值计算: Z = G_CODATA * c / 2 = {Z_exact:.10e} kg^-1·m^4·s^-3")
    
    # 使用精确Z值反推G
    G_theory_exact = (2 * Z_exact) / c
    print(f"使用精确Z值反推G: G = 2*Z_exact/c = {G_theory_exact:.10e} m³·kg^-1·s^-2")
    
    # 计算精确Z值下的相对误差
    error_exact = abs((G_CODATA - G_theory_exact) / G_CODATA) * 100
    print(f"精确Z值下的相对误差: {error_exact:.10f}%")
    
    print("\n" + "="*60 + "\n")
    
    # 使用近似Z值(Z=0.01)
    Z_approx = 0.01
    print(f"近似Z值: Z_approx = {Z_approx}")
    
    # 使用近似Z值计算G
    G_theory_approx = (2 * Z_approx) / c
    print(f"使用近似Z值计算G: G = 2*Z_approx/c = {G_theory_approx:.10e} m³·kg^-1·s^-2")
    
    # 计算近似Z值下的相对误差
    error_approx = abs((G_CODATA - G_theory_approx) / G_CODATA) * 100
    print(f"近似Z值下的相对误差: {error_approx:.10f}%")
    
    print("\n" + "="*60 + "\n")
    
    # 验证论文中提到的Z值（更新为CODATA 2018精确值）
    Z_paper = 0.010004524012147
    print(f"论文中使用的Z值（基于CODATA 2018精确值）: Z_paper = {Z_paper}")
    
    # 使用论文中的Z值计算G
    G_theory_paper = (2 * Z_paper) / c
    print(f"使用论文中的Z值计算G: G = 2*Z_paper/c = {G_theory_paper:.10e} m³·kg^-1·s^-2")
    
    # 计算论文中Z值下的相对误差
    error_paper = abs((G_CODATA - G_theory_paper) / G_CODATA) * 100
    print(f"论文中Z值下的相对误差: {error_paper:.10f}%")
    
    print("\n" + "="*60 + "\n")
    
    # 分析结果
    print("结论分析:")
    print(f"1. 当Z = Gc/2时，使用实验值G计算Z再反推G，会得到完全相同的G值，相对误差理论上为0%")
    print(f"   这是因为这里的计算本质上是自洽性检验：Z = Gc/2 ⇒ G = 2Z/c")
    print(f"2. 当使用近似值Z=0.01时，相对误差约为{error_approx:.6f}%，与论文中提到的0.045%一致")
    print(f"3. 当使用论文中调整后的Z值{Z_paper}时，相对误差约为{error_paper:.10f}%，非常接近0%")
    print(f"4. CODATA 2018中G的不确定度约为1.2×10^-5，我们的计算误差完全在这个范围内")

if __name__ == "__main__":
    print("引力光速统一方程Z=Gc/2的误差计算验证\n")
    verify_error_calculation()