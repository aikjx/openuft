#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试核心算法文件的功能
"""

import os
import time
from core_algorithm import FormulaCalculator, ConsistencyVerifier, PerformanceBenchmarker

# 获取公式规格数据库路径
db_path = os.path.join(os.path.dirname(__file__), "公式规格数据库.json")

print("=== 测试核心算法功能 ===")
print(f"使用公式规格数据库: {db_path}")

# 测试1: 初始化公式计算器
try:
    calculator = FormulaCalculator(db_path)
    print("✅ 公式计算器初始化成功")
except Exception as e:
    print(f"❌ 公式计算器初始化失败: {e}")
    exit(1)

# 测试2: 计算单个公式
test_formulas = [
    "01",  # 时空同一化方程
    "02",  # 三维螺旋时空方程
    "03",  # 质量定义方程
    "04",  # 引力场定义方程
    "05",  # 动量方程
    "06",  # 运动动量方程
    "07",  # 宇宙大统一方程（力方程）
    "08",  # 空间波动方程
    "09",  # 电荷定义方程
    "10",  # 电场定义方程
    "11",  # 磁场定义方程
    "12",  # 变化引力场产生电磁场
    "13",  # 磁矢势方程
    "14",  # 变化引力场产生电场
    "15",  # 变化磁场产生引力场和电场
    "16",  # 能量方程
    "17"   # 光速飞行器动力学方程
]

print("\n=== 测试公式计算功能 ===")
success_count = 0
for formula_id in test_formulas:
    try:
        result = calculator.calculate_formula(formula_id)
        if result['status'] == 'success':
            print(f"✅ 公式 {formula_id} ({result['formula_name']}) 计算成功")
            success_count += 1
        else:
            print(f"❌ 公式 {formula_id} 计算失败: {result['error']}")
    except Exception as e:
        print(f"❌ 公式 {formula_id} 计算异常: {e}")

print(f"\n公式计算测试结果: {success_count}/{len(test_formulas)} 个公式计算成功")

# 测试3: 计算所有公式
try:
    all_results = calculator.calculate_all_formulas()
    print("\n=== 测试计算所有公式 ===")
    print(f"总公式数: {all_results['summary']['total_modules']}")
    print(f"成功计算: {all_results['summary']['successful_modules']}")
    print(f"成功率: {all_results['summary']['successful_modules'] / all_results['summary']['total_modules'] * 100:.1f}%")
    print(f"执行时间: {all_results['summary']['execution_time']:.6f}秒")
except Exception as e:
    print(f"❌ 计算所有公式失败: {e}")

# 测试4: 验证公式一致性
try:
    verifier = ConsistencyVerifier(calculator)
    consistency_result = verifier.verify_consistency()
    print("\n=== 测试公式一致性 ===")
    print(f"一致性测试数: {consistency_result['summary']['total_tests']}")
    print(f"通过测试数: {consistency_result['summary']['consistent_tests']}")
    print(f"一致性率: {consistency_result['summary']['consistency_rate'] * 100:.1f}%")
    
    # 打印详细的一致性测试结果
    for test_id, test_result in consistency_result.items():
        if test_id != 'summary':
            status = "通过" if test_result['consistent'] else "失败"
            print(f"  {test_result['description']}: {status}")
            if not test_result['consistent'] and 'error' in test_result:
                print(f"    错误: {test_result['error']}")
except Exception as e:
    print(f"❌ 验证公式一致性失败: {e}")

# 测试5: 性能基准测试
try:
    benchmarker = PerformanceBenchmarker(calculator)
    performance_result = benchmarker.benchmark_performance(iterations=10)
    print("\n=== 测试性能基准 ===")
    print(f"测试模块数: {performance_result['summary']['total_modules_tested']}")
    
    # 检查是否存在average_execution_time字段
    if 'average_execution_time' in performance_result['summary']:
        print(f"平均执行时间: {performance_result['summary']['average_execution_time']:.6f}秒")
    else:
        print(f"平均执行时间: 无法获取")
    
    # 打印最快的模块
    print("\n最快的模块:")
    if 'fastest_modules' in performance_result['summary']:
        fastest_modules = performance_result['summary']['fastest_modules'][:3]  # 只显示前3个
        for i, (module_name, performance) in enumerate(fastest_modules):
            print(f"  {i+1}. {module_name} ({performance.get('formula_name', '未知')}): {performance.get('average_time', 0):.6f}秒")
    else:
        print("  无法获取最快模块信息")
    
    # 打印最慢的模块
    print("\n最慢的模块:")
    if 'slowest_modules' in performance_result['summary']:
        slowest_modules = performance_result['summary']['slowest_modules'][:3]  # 只显示前3个
        for i, (module_name, performance) in enumerate(slowest_modules):
            print(f"  {i+1}. {module_name} ({performance.get('formula_name', '未知')}): {performance.get('average_time', 0):.6f}秒")
    else:
        print("  无法获取最慢模块信息")
    
    # 测试计算所有公式的性能
    try:
        all_formulas_performance = benchmarker.benchmark_all_formulas(iterations=5)
        print("\n=== 计算所有公式性能测试 ===")
        print(f"平均时间: {all_formulas_performance['average_time']:.6f}秒")
        print(f"最小时间: {all_formulas_performance['min_time']:.6f}秒")
        print(f"最大时间: {all_formulas_performance['max_time']:.6f}秒")
        print(f"标准差: {all_formulas_performance['std_time']:.6f}秒")
    except Exception as e:
        print(f"❌ 计算所有公式性能测试失败: {e}")
except Exception as e:
    print(f"❌ 性能基准测试失败: {e}")

# 测试6: 缓存测试
try:
    print("\n=== 测试缓存功能 ===")
    
    # 清除缓存
    calculator.clear_cache()
    print("✅ 缓存已清除")
    
    # 第一次计算（无缓存）
    start_time = time.time()
    result1 = calculator.calculate_formula("02", {"t": 10, "r": 5, "omega": 2, "h": 1})
    time1 = time.time() - start_time
    
    # 第二次计算（有缓存）
    start_time = time.time()
    result2 = calculator.calculate_formula("02", {"t": 10, "r": 5, "omega": 2, "h": 1})
    time2 = time.time() - start_time
    
    if result1['status'] == 'success' and result2['status'] == 'success':
        print(f"✅ 缓存测试成功")
        print(f"  第一次计算时间: {time1:.6f}秒")
        print(f"  第二次计算时间: {time2:.6f}秒")
        if time2 > 0:
            print(f"  缓存加速比: {time1/time2:.2f}x")
        else:
            print(f"  缓存加速比: 无法计算（第二次计算时间为0）")
except Exception as e:
    print(f"❌ 缓存测试失败: {e}")

# 测试7: 参数化测试
try:
    print("\n=== 测试参数化计算 ===")
    
    # 测试不同参数下的三维螺旋时空方程
    test_parameters = [
        {"t": 0, "r": 5, "omega": 1, "h": 1},
        {"t": 1, "r": 5, "omega": 1, "h": 1},
        {"t": 2, "r": 5, "omega": 1, "h": 1},
        {"t": 3, "r": 5, "omega": 1, "h": 1}
    ]
    
    for params in test_parameters:
        result = calculator.calculate_formula("02", params)
        if result['status'] == 'success':
            pos = result['result']['position']
            print(f"✅ t={params['t']}: 位置 ({pos['x']:.2f}, {pos['y']:.2f}, {pos['z']:.2f})")
        else:
            print(f"❌ t={params['t']}: 计算失败")
except Exception as e:
    print(f"❌ 参数化测试失败: {e}")

print("\n=== 测试完成 ===")
print("\n🎉 统一场论核心算法测试全部完成！")
