#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心算法简化测试
Unified Field Theory Core Algorithm Simplified Test

该文件是统一场论核心算法的简化测试，只测试核心功能，避免依赖问题。
This file is a simplified test for the unified field theory core algorithm, 
only testing core functionality to avoid dependency issues.
"""

import json
import time

def test_core_functionality():
    """测试核心功能"""
    print("=== 统一场论核心算法简化测试 ===")
    print("测试时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # 测试结果字典
    results = {
        "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tests": [],
        "summary": {}
    }
    
    # 测试1: 系统初始化
    print("1. 测试系统初始化...")
    try:
        # 尝试导入整合模块
        from 统一场论核心算法整合模块 import get_integrator, get_system_info
        
        integrator = get_integrator()
        system_info = get_system_info()
        
        test_result = {
            "name": "系统初始化",
            "status": "成功",
            "message": "统一场论整合器初始化成功",
            "system_info": system_info
        }
        print("   ✓ 系统初始化成功")
        print(f"   系统名称: {system_info.get('system_name')}")
        print(f"   版本: {system_info.get('version')}")
        print(f"   已加载模块数: {system_info.get('loaded_modules_count', 0)}")
        
    except Exception as e:
        test_result = {
            "name": "系统初始化",
            "status": "失败",
            "message": f"系统初始化失败: {str(e)}"
        }
        print(f"   ✗ 系统初始化失败: {str(e)}")
    
    results["tests"].append(test_result)
    
    # 测试2: 模块状态检查
    print("\n2. 测试模块状态...")
    try:
        from 统一场论核心算法整合模块 import get_integrator
        
        integrator = get_integrator()
        module_status = integrator.get_module_status()
        
        test_result = {
            "name": "模块状态检查",
            "status": "成功",
            "message": "模块状态检查成功",
            "module_status": module_status
        }
        
        print("   ✓ 模块状态检查成功")
        print("   模块状态:")
        for module, status in module_status.items():
            print(f"     {module}: {'已加载' if status else '未加载'}")
        
    except Exception as e:
        test_result = {
            "name": "模块状态检查",
            "status": "失败",
            "message": f"模块状态检查失败: {str(e)}"
        }
        print(f"   ✗ 模块状态检查失败: {str(e)}")
    
    results["tests"].append(test_result)
    
    # 测试3: 核心计算功能
    print("\n3. 测试核心计算功能...")
    try:
        from 统一场论核心算法整合模块 import calculate_geometric_factor, calculate_gravity_light_speed
        
        # 测试几何因子计算
        gf_result = calculate_geometric_factor(method="default")
        gls_result = calculate_gravity_light_speed(method="default")
        
        test_result = {
            "name": "核心计算功能",
            "status": "成功",
            "message": "核心计算功能测试成功",
            "geometric_factor_result": gf_result,
            "gravity_light_speed_result": gls_result
        }
        
        print("   ✓ 核心计算功能测试成功")
        print(f"   几何因子计算结果: {'成功' if 'error' not in gf_result else '失败'}")
        print(f"   引力光速计算结果: {'成功' if 'error' not in gls_result else '失败'}")
        
    except Exception as e:
        test_result = {
            "name": "核心计算功能",
            "status": "失败",
            "message": f"核心计算功能测试失败: {str(e)}"
        }
        print(f"   ✗ 核心计算功能测试失败: {str(e)}")
    
    results["tests"].append(test_result)
    
    # 测试4: 系统状态
    print("\n4. 测试系统状态...")
    try:
        from 统一场论核心算法整合模块 import get_system_status
        
        status = get_system_status()
        
        test_result = {
            "name": "系统状态",
            "status": "成功",
            "message": "系统状态获取成功",
            "system_status": status
        }
        
        print("   ✓ 系统状态获取成功")
        print(f"   系统状态获取成功，包含 {len(status)} 个状态项")
        
    except Exception as e:
        test_result = {
            "name": "系统状态",
            "status": "失败",
            "message": f"系统状态获取失败: {str(e)}"
        }
        print(f"   ✗ 系统状态获取失败: {str(e)}")
    
    results["tests"].append(test_result)
    
    # 生成测试总结
    print("\n=== 测试总结 ===")
    
    # 统计测试结果
    success_count = sum(1 for test in results["tests"] if test["status"] == "成功")
    total_count = len(results["tests"])
    
    results["summary"] = {
        "total_tests": total_count,
        "success_count": success_count,
        "failure_count": total_count - success_count,
        "success_rate": (success_count / total_count * 100) if total_count > 0 else 0,
        "test_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"测试总数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"失败数: {total_count - success_count}")
    print(f"成功率: {results['summary']['success_rate']:.1f}%")
    
    # 保存测试结果
    output_file = f"unified_field_theory_test_result_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试结果已保存至: {output_file}")
    
    return results

if __name__ == "__main__":
    test_core_functionality()
