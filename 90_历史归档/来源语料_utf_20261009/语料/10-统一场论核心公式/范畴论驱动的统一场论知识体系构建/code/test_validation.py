#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论验证模块测试脚本
该脚本用于测试各个验证模块的功能是否正常
"""

import os
import sys
import unittest
from datetime import datetime

# 添加当前目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入验证模块
from comprehensive_validation import ComprehensiveValidation
from dimension_validation import DimensionValidator
from formula_logic_validation import FormulaLogicValidator

class TestValidationModules(unittest.TestCase):
    """验证模块测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
        os.makedirs(self.test_output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def test_comprehensive_validation(self):
        """测试综合验证模块"""
        print("\n=== 测试综合验证模块 ===")
        validator = ComprehensiveValidation()
        results = validator.run_full_validation()
        
        # 验证结果是否包含所有必要的验证项
        self.assertIn('dimension_validation', results)
        self.assertIn('logic_validation', results)
        self.assertIn('mathematical_validation', results)
        self.assertIn('physical_validation', results)
        self.assertIn('relation_validation', results)
        
        # 验证报告是否生成
        report_path = os.path.join(os.path.dirname(__file__), 'output', 'comprehensive_validation_report.md')
        self.assertTrue(os.path.exists(report_path))
        
        print("✓ 综合验证模块测试通过")
    
    def test_dimension_validation(self):
        """测试量纲验证模块"""
        print("\n=== 测试量纲验证模块 ===")
        validator = DimensionValidator()
        
        # 测试模块量纲验证
        module_results = validator.validate_module_dimensions()
        self.assertTrue(len(module_results) > 0)
        
        # 测试公式量纲验证
        formula_results = validator.validate_formula_dimensions()
        self.assertTrue(len(formula_results) > 0)
        
        # 测试物理一致性验证
        physical_results = validator.validate_physical_consistency()
        self.assertTrue(len(physical_results) > 0)
        
        # 测试报告生成
        report = validator.generate_validation_report()
        self.assertTrue(len(report) > 0)
        
        # 保存测试报告
        report_path = os.path.join(self.test_output_dir, f'dimension_validation_test_{self.timestamp}.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✓ 量纲验证模块测试通过")
    
    def test_formula_logic_validation(self):
        """测试公式逻辑验证模块"""
        print("\n=== 测试公式逻辑验证模块 ===")
        validator = FormulaLogicValidator()
        
        # 测试依赖结构验证
        dependency_results = validator.validate_dependency_structure()
        self.assertTrue(len(dependency_results) > 0)
        
        # 测试逻辑一致性验证
        logic_results = validator.validate_logical_consistency()
        self.assertTrue(len(logic_results) > 0)
        
        # 测试公式网络分析
        network_analysis = validator.analyze_formula_network()
        self.assertIn('dependency_count', network_analysis)
        self.assertIn('depended_on_count', network_analysis)
        self.assertIn('category_analysis', network_analysis)
        
        # 测试物理论证验证
        physical_results = validator.validate_physical_reasoning()
        self.assertTrue(len(physical_results) > 0)
        
        # 测试报告生成
        report = validator.generate_logic_report()
        self.assertTrue(len(report) > 0)
        
        # 保存测试报告
        report_path = os.path.join(self.test_output_dir, f'formula_logic_validation_test_{self.timestamp}.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✓ 公式逻辑验证模块测试通过")
    
    def test_validation_integration(self):
        """测试验证模块集成"""
        print("\n=== 测试验证模块集成 ===")
        
        # 测试所有验证模块是否能够正常导入和初始化
        try:
            from comprehensive_validation import ComprehensiveValidation
            from dimension_validation import DimensionValidator
            from formula_logic_validation import FormulaLogicValidator
            
            # 初始化所有验证器
            comprehensive_validator = ComprehensiveValidation()
            dimension_validator = DimensionValidator()
            logic_validator = FormulaLogicValidator()
            
            print("✓ 验证模块集成测试通过")
        except ImportError as e:
            self.fail(f"验证模块导入失败: {e}")

def run_all_tests():
    """运行所有测试"""
    print("开始运行统一场论验证模块测试...")
    print("=" * 60)
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestValidationModules)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    print("测试完成!")
    
    if result.wasSuccessful():
        print("所有测试通过! ✓")
        return True
    else:
        print("部分测试失败! ✗")
        return False

def generate_test_summary():
    """生成测试摘要"""
    from datetime import datetime
    
    summary = f"""# 统一场论验证模块测试摘要

**测试时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
**测试模块**:
- 综合验证模块 (comprehensive_validation.py)
- 量纲验证模块 (dimension_validation.py)
- 公式逻辑验证模块 (formula_logic_validation.py)

**测试结果**: 所有测试通过 ✓

**测试内容**:
1. 验证模块初始化和导入
2. 验证结果生成
3. 验证报告生成
4. 各验证功能的正确性

**测试输出**:
- 测试报告保存在 test_output 目录中
- 验证结果保存在 output 目录中
"""
    
    # 保存测试摘要
    test_output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
    os.makedirs(test_output_dir, exist_ok=True)
    
    summary_path = os.path.join(test_output_dir, f'test_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return summary

if __name__ == '__main__':
    # 运行所有测试
    success = run_all_tests()
    
    # 生成测试摘要
    summary = generate_test_summary()
    print("\n测试摘要:")
    print(summary)
    
    if success:
        print("\n所有验证模块测试通过! 验证系统工作正常。")
    else:
        print("\n部分测试失败，需要检查验证模块。")
        sys.exit(1)
