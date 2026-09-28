#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证加速运动正电荷产生加速度反向引力场的公式（中文版）

公式：E_theta = (-q/(4*pi*epsilon0*c**2*r)) * (A × r_hat)

验证维度：
1. 核心公式计算验证
2. 横向电场推导验证
3. 磁场与引力场关系验证
4. 量纲分析验证
5. 方向关系验证
6. 衰减规律验证
7. 实验关联性验证
"""

# 导入模块化组件
from core.field_calculator import FieldCalculator
from visualization.field_visualizer import (
    plot_electric_field_distribution,
    plot_experiment_simulation,
    plot_3d_vector_visualization,
    plot_tokamak_z_pinch_simulation
)
import numpy as np

# 保持向后兼容性，定义FieldVerifier类作为FieldCalculator的别名
class FieldVerifier(FieldCalculator):
    """场验证器类（向后兼容）"""
    pass

# 主函数
def main():
    """主函数"""
    print("=== 加速运动正电荷产生引力场公式验证 ===")
    print()
    
    # 创建验证器
    verifier = FieldVerifier()
    
    # 运行综合验证
    results = verifier.run_comprehensive_verification()
    
    # 打印维度分析验证结果
    print("1. 维度分析验证：")
    print(f"   维度一致：{results['dimension_analysis_verification']}")
    print()
    
    # 打印测试用例结果
    print("2. 多个测试用例验证：")
    print(f"   总测试用例数：{results['total_test_cases']}")
    print(f"   通过测试用例数：{results['passed_test_cases']}")
    print()
    
    # 打印每个测试用例的详细结果
    for case in results['test_case_results']:
        print(f"   测试用例 {case['test_case']}：")
        print(f"      状态：{case['verification_status']}")
        if case['verification_status'] == "passed":
            print(f"      参数：电荷={case['parameters']['charge']:.2e} C, 加速度={case['parameters']['acceleration']:.2e} m/s², 距离={case['parameters']['distance']:.2f} m, 角度={case['parameters']['angle']:.2f} rad")
            print(f"      横向电场强度：{case['core_formula_verification']['transverse_electric_field_magnitude']:.2e} V/m")
            print(f"      磁场强度：{case['magnetic_field_verification']['magnetic_field_magnitude']:.2e} T")
            print(f"      遵循1/r衰减规律：{case['decay_law_verification']['follows_1_over_r_law']}")
        else:
            print(f"      错误信息：{case['error_message']}")
        print()
    
    # 绘制电场分布（使用第一个测试用例的参数）
    print("3. 电场分布可视化：")
    r_values = np.linspace(0.1, 10, 100)
    plot_electric_field_distribution(verifier, 1.6e-19, 1e10, r_values, np.pi/2)
    
    # 绘制实验模拟结果（使用第一个测试用例的结果）
    if results['test_case_results'] and results['test_case_results'][0]['verification_status'] == "passed":
        print("4. 实验模拟结果可视化：")
        plot_experiment_simulation(results['test_case_results'][0]['experiment_simulation'])
    
    # 绘制3D矢量可视化
    print("5. 3D矢量可视化：")
    # 使用第一个测试用例的参数
    test_case_params = [1.6e-19, 1e10, 1.0, np.pi/2, [1, 0, 0], [0, 1, 0]]
    q, a, r, theta, a_direction, r_hat_direction = test_case_params
    plot_3d_vector_visualization(verifier, q, a, r, a_direction, r_hat_direction)
    
    # 绘制托卡马克Z箍缩实验模拟
    print("6. 托卡马克Z箍缩实验模拟：")
    # 使用合理的托卡马克实验参数
    tokamak_params = {
        'current': 1e6,  # 1 MA
        'current_change_rate': 1e12,  # 1e12 A/s
        'plasma_radius': 0.1,  # 0.1 m
        'distance': 0.5  # 0.5 m
    }
    tokamak_results = verifier.simulate_tokamak_z_pinch_experiment(
        tokamak_params['current'],
        tokamak_params['current_change_rate'],
        tokamak_params['plasma_radius'],
        tokamak_params['distance']
    )
    plot_tokamak_z_pinch_simulation(tokamak_results)
    
    # 验证总结
    all_passed = results['dimension_analysis_verification'] and (results['passed_test_cases'] == results['total_test_cases'])
    
    print("=== 验证总结 ===")
    print(f"所有验证通过：{all_passed}")
    print(f"通过测试用例：{results['passed_test_cases']}/{results['total_test_cases']}")
    
    if all_passed:
        print("✓ 加速运动正电荷产生引力场公式验证通过！")
    else:
        print("✗ 部分验证失败，请检查参数和推导过程。")

if __name__ == "__main__":
    main()