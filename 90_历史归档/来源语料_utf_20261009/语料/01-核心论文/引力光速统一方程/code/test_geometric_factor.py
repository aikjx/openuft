#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
几何因子2验证分析测试脚本

用于验证修复后的几何因子2验证分析代码能否正常运行，
检查所有功能模块是否正常工作，并生成验证结果。
"""

import os
import sys
import importlib.util
import numpy as np

# 检查当前目录是否在Python路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_module_import():
    """测试模块是否能正常导入"""
    print("===== 测试模块导入 =====")
    try:
        # 尝试导入几何因子验证分析模块
        spec = importlib.util.spec_from_file_location(
            "几何因子验证分析", 
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "几何因子验证分析.py")
        )
        if spec is None:
            print("❌ 模块规范创建失败")
            return False
        
        geometric_factor_module = importlib.util.module_from_spec(spec)
        if geometric_factor_module is None:
            print("❌ 模块创建失败")
            return False
        
        spec.loader.exec_module(geometric_factor_module)
        print("✅ 模块导入成功")
        return geometric_factor_module
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_class_creation(module):
    """测试类是否能正常创建"""
    print("\n===== 测试类创建 =====")
    try:
        verifier = module.GeometricFactorVerification()
        print("✅ GeometricFactorVerification类创建成功")
        return verifier
    except AttributeError:
        print("❌ GeometricFactorVerification类不存在")
        return False
    except Exception as e:
        print(f"❌ 创建类实例失败: {e}")
        return False

def test_solid_angle_integration(verifier):
    """测试立体角积分验证功能"""
    print("\n===== 测试立体角积分验证 =====")
    try:
        result = verifier.verify_solid_angle_integration()
        # 验证结果是否合理
        standard_solid_angle = result["standard_solid_angle"]
        effective_contribution = result["effective_contribution_integral"]
        
        # 检查标准立体角积分是否接近4π
        standard_check = np.isclose(standard_solid_angle, 4 * np.pi, atol=1e-6)
        # 检查有效贡献积分是否接近2
        effective_check = np.isclose(effective_contribution, 2, atol=1e-6)
        
        print(f"✅ 标准立体角积分结果: {standard_solid_angle:.6f} ≈ 4π = {4*np.pi:.6f}")
        print(f"✅ 有效贡献积分结果: {effective_contribution:.6f} ≈ 2")
        
        if standard_check and effective_check:
            print("✅ 立体角积分验证通过")
            return True
        else:
            print("❌ 立体角积分验证失败")
            return False
    except Exception as e:
        print(f"❌ 立体角积分验证失败: {e}")
        return False

def test_projection_geometry(verifier):
    """测试投影几何分析功能"""
    print("\n===== 测试投影几何分析 =====")
    try:
        result = verifier.analyze_projection_geometry()
        # 验证结果是否合理
        upper_hemisphere = result["upper_hemisphere_integral"]
        full_space = result["full_space_integral"]
        geometric_factor = result["geometric_factor"]
        
        # 检查上半球积分是否接近1
        upper_check = np.isclose(upper_hemisphere, 1, atol=1e-6)
        # 检查完整空间积分是否接近2
        full_check = np.isclose(full_space, 2, atol=1e-6)
        # 检查几何因子是否接近2
        factor_check = np.isclose(geometric_factor, 2, atol=1e-6)
        
        print(f"✅ 上半球积分结果: {upper_hemisphere:.6f} ≈ 1")
        print(f"✅ 完整空间积分结果: {full_space:.6f} ≈ 2")
        print(f"✅ 几何因子: {geometric_factor:.6f} ≈ 2")
        
        if upper_check and full_check and factor_check:
            print("✅ 投影几何分析通过")
            return True
        else:
            print("❌ 投影几何分析失败")
            return False
    except Exception as e:
        print(f"❌ 投影几何分析失败: {e}")
        return False

def test_standalone_functions(module):
    """测试独立函数"""
    print("\n===== 测试独立函数 =====")
    results = []
    
    # 测试correct_solid_angle_calculation函数
    try:
        result = module.correct_solid_angle_calculation()
        # 验证结果是否合理
        standard_integral = result["standard_integral"]
        effective_integral = result["effective_integral"]
        geometric_factor = result["geometric_factor"]
        
        standard_check = np.isclose(standard_integral, 4 * np.pi, atol=1e-6)
        effective_check = np.isclose(effective_integral, 2, atol=1e-6)
        factor_check = np.isclose(geometric_factor, 2, atol=1e-6)
        
        print(f"✅ correct_solid_angle_calculation函数结果:")
        print(f"   标准立体角积分: {standard_integral:.6f} ≈ 4π")
        print(f"   有效贡献积分: {effective_integral:.6f} ≈ 2")
        print(f"   几何因子: {geometric_factor:.6f} ≈ 2")
        
        if standard_check and effective_check and factor_check:
            print("✅ correct_solid_angle_calculation函数通过")
            results.append(True)
        else:
            print("❌ correct_solid_angle_calculation函数失败")
            results.append(False)
    except Exception as e:
        print(f"❌ correct_solid_angle_calculation函数失败: {e}")
        results.append(False)
    
    # 测试comprehensive_analysis函数
    try:
        module.comprehensive_analysis()
        print("✅ comprehensive_analysis函数执行成功")
        results.append(True)
    except Exception as e:
        print(f"❌ comprehensive_analysis函数失败: {e}")
        results.append(False)
    
    # 图表生成函数不在这里测试，因为它会显示图形界面
    
    return all(results)

def test_main_execution():
    """测试主程序执行"""
    print("\n===== 测试主程序执行 =====")
    try:
        # 获取几何因子验证分析.py文件的完整路径
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "几何因子验证分析.py")
        
        # 检查文件是否存在
        if not os.path.exists(script_path):
            print(f"❌ 文件不存在: {script_path}")
            return False
        
        # 读取文件内容并执行
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 创建一个局部环境，用于执行代码
        local_env = {}
        exec(code, local_env)
        
        print("✅ 主程序执行成功")
        return True
    except Exception as e:
        print(f"❌ 主程序执行失败: {e}")
        return False

def main():
    """主测试函数"""
    print("几何因子2验证分析代码测试开始")
    print("=" * 50)
    
    # 1. 测试模块导入
    module = test_module_import()
    if not module:
        print("\n测试失败: 无法导入模块")
        return False
    
    # 2. 测试类创建
    verifier = test_class_creation(module)
    if not verifier:
        print("\n测试失败: 无法创建类实例")
        return False
    
    # 3. 测试立体角积分验证
    solid_angle_result = test_solid_angle_integration(verifier)
    if not solid_angle_result:
        print("立体角积分验证失败")
    
    # 4. 测试投影几何分析
    projection_result = test_projection_geometry(verifier)
    if not projection_result:
        print("投影几何分析失败")
    
    # 5. 测试独立函数
    standalone_result = test_standalone_functions(module)
    if not standalone_result:
        print("独立函数测试失败")
    
    # 6. 测试主程序执行
    main_result = test_main_execution()
    if not main_result:
        print("主程序执行测试失败")
    
    # 总结测试结果
    print("\n" + "=" * 50)
    print("几何因子2验证分析代码测试总结")
    
    all_tests_passed = (solid_angle_result and projection_result and 
                       standalone_result and main_result)
    
    if all_tests_passed:
        print("✅ 所有测试通过！修复后的代码能够正常工作。")
    else:
        print("❌ 部分测试失败，请检查修复后的代码。")
    
    return all_tests_passed

if __name__ == "__main__":
    main()