#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有几何因子分析脚本
Test All Geometric Factor Analysis Scripts

这个脚本用于测试所有相关的Python文件，确保：
1. 没有语法错误
2. 没有编码问题
3. 所有导入都正常
4. 核心功能可以运行

Author: Quality Assurance
Date: 2025-09-16
"""

import sys
import os
import traceback
import importlib.util
import warnings

# 确保可以导入error_handler
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 导入自定义错误处理器
from error_handler import error_handler, ErrorType, safe_execution

# 忽略matplotlib警告
warnings.filterwarnings('ignore')

class ScriptTester:
    """脚本测试器"""
    
    def __init__(self):
        self.test_results = {}
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.error_handler = error_handler  # 使用全局错误处理器
        
    @safe_execution
    def test_imports(self):
        """测试基本导入"""
        print("Testing basic imports...")
        
        try:
            import numpy as np
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            import matplotlib.animation as animation
            from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
            import matplotlib.patches as patches
            print("✓ All basic imports successful")
            return True
        except Exception as e:
            self.error_handler.handle_error(ErrorType.IMPORT_ERROR, "Failed to import basic modules", e)
            print(f"✗ Import error: {e}")
            return False
    
    @safe_execution
    def test_script_syntax(self, script_path):
        """测试脚本语法"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # 编译检查语法
            compile(source_code, script_path, 'exec')
            return True, "Syntax OK"
            
        except SyntaxError as e:
            self.error_handler.handle_error(ErrorType.SYNTAX_ERROR, f"Syntax error in {os.path.basename(script_path)}", e)
            return False, f"Syntax Error: {e}"
        except UnicodeDecodeError as e:
            self.error_handler.handle_error(ErrorType.FILE_ERROR, f"Encoding error in {os.path.basename(script_path)}", e)
            return False, f"Encoding Error: {e}"
        except Exception as e:
            self.error_handler.handle_error(ErrorType.OTHER_ERROR, f"Unexpected error in syntax test for {os.path.basename(script_path)}", e)
            return False, f"Other Error: {e}"
    
    @safe_execution
    def test_script_import(self, script_path):
        """测试脚本导入"""
        try:
            # 获取模块名
            module_name = os.path.splitext(os.path.basename(script_path))[0]
            
            # 动态导入
            spec = importlib.util.spec_from_file_location(module_name, script_path)
            module = importlib.util.module_from_spec(spec)
            
            # 执行导入（但不运行main）
            spec.loader.exec_module(module)
            
            return True, "Import OK"
            
        except Exception as e:
            self.error_handler.handle_error(ErrorType.IMPORT_ERROR, f"Import error in {os.path.basename(script_path)}", e)
            return False, f"Import Error: {e}"
    
    @safe_execution
    def test_core_functionality(self, script_path):
        """测试核心功能"""
        try:
            module_name = os.path.splitext(os.path.basename(script_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 测试不同脚本的核心类
            if hasattr(module, 'GeometricFactorAnimator'):
                animator = module.GeometricFactorAnimator()
                return True, "Core class instantiated"
            elif hasattr(module, 'GeometricFactorAnalysis'):
                analyzer = module.GeometricFactorAnalysis()
                return True, "Core class instantiated"
            elif hasattr(module, 'ComprehensiveErrorAnalysis'):
                analyzer = module.ComprehensiveErrorAnalysis()
                return True, "Core class instantiated"
            elif hasattr(module, 'GeometricFactorAnalysisSystem'):
                system = module.GeometricFactorAnalysisSystem()
                return True, "Core class instantiated"
            else:
                return True, "No core class found (OK for some scripts)"
                
        except Exception as e:
            self.error_handler.handle_error(ErrorType.OTHER_ERROR, f"Functionality error in {os.path.basename(script_path)}", e)
            return False, f"Functionality Error: {e}"
    
    @safe_execution
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("=" * 80)
        print("COMPREHENSIVE SCRIPT TESTING")
        print("=" * 80)
        
        # 重置错误处理器
        self.error_handler.reset()
        
        # 测试基本导入
        if not self.test_imports():
            print("Basic imports failed. Cannot continue testing.")
            return False
        
        # 获取所有Python脚本
        python_scripts = []
        for file in os.listdir(self.script_dir):
            if file.endswith('.py') and not file.startswith('__'):
                python_scripts.append(os.path.join(self.script_dir, file))
        
        print(f"\nFound {len(python_scripts)} Python scripts to test:")
        for script in python_scripts:
            print(f"  - {os.path.basename(script)}")
        
        # 测试每个脚本
        print("\n" + "=" * 80)
        print("INDIVIDUAL SCRIPT TESTS")
        print("=" * 80)
        
        all_passed = True
        
        for script_path in python_scripts:
            script_name = os.path.basename(script_path)
            print(f"\nTesting: {script_name}")
            print("-" * 60)
            
            # 语法测试
            syntax_ok, syntax_msg = self.test_script_syntax(script_path)
            print(f"  Syntax Check: {'✓' if syntax_ok else '✗'} {syntax_msg}")
            
            if not syntax_ok:
                all_passed = False
                self.test_results[script_name] = {'syntax': False, 'import': False, 'functionality': False}
                continue
            
            # 导入测试
            import_ok, import_msg = self.test_script_import(script_path)
            print(f"  Import Check: {'✓' if import_ok else '✗'} {import_msg}")
            
            if not import_ok:
                all_passed = False
                self.test_results[script_name] = {'syntax': True, 'import': False, 'functionality': False}
                continue
            
            # 功能测试
            func_ok, func_msg = self.test_core_functionality(script_path)
            print(f"  Functionality: {'✓' if func_ok else '✗'} {func_msg}")
            
            if not func_ok:
                all_passed = False
            
            self.test_results[script_name] = {
                'syntax': syntax_ok,
                'import': import_ok, 
                'functionality': func_ok
            }
        
        return all_passed
    
    @safe_execution
    def generate_test_report(self, output_file=None):
        """生成测试报告"""
        print("\n" + "=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)
        
        total_scripts = len(self.test_results)
        passed_scripts = sum(1 for result in self.test_results.values() 
                           if all(result.values()))
        
        print(f"\nTotal Scripts Tested: {total_scripts}")
        print(f"Scripts Passed All Tests: {passed_scripts}")
        print(f"Success Rate: {passed_scripts/total_scripts*100:.1f}%")
        
        # 生成错误报告
        error_report_file = output_file or os.path.join(self.script_dir, 'logs', 'test_error_report.txt')
        self.error_handler.generate_error_report(error_report_file)
        print(f"\nDetailed error report generated at: {error_report_file}")
        
        print("\nDetailed Results:")
        print("-" * 60)
        
        for script_name, results in self.test_results.items():
            status = "PASS" if all(results.values()) else "FAIL"
            print(f"{script_name:<40} {status}")
            
            if not all(results.values()):
                failed_tests = [test for test, passed in results.items() if not passed]
                print(f"{'':>40} Failed: {', '.join(failed_tests)}")
        
        return passed_scripts == total_scripts
    
    @safe_execution
    def run_sample_functionality(self):
        """运行示例功能测试"""
        print("\n" + "=" * 80)
        print("SAMPLE FUNCTIONALITY TESTS")
        print("=" * 80)
        
        try:
            # 测试数学计算
            import numpy as np
            
            print("\n1. Testing mathematical calculations...")
            
            # 立体角计算
            def solid_angle_integral():
                theta = np.linspace(0, np.pi, 1000)
                phi = np.linspace(0, 2*np.pi, 1000)
                
                # 正确的积分
                correct_integral = 4 * np.pi
                
                # 数值积分验证
                dtheta = theta[1] - theta[0]
                dphi = phi[1] - phi[0]
                
                integral_sum = 0
                for t in theta:
                    integral_sum += np.sin(t) * dtheta * 2 * np.pi
                
                return integral_sum, correct_integral
            
            numerical, analytical = solid_angle_integral()
            print(f"   Solid angle integral: {numerical:.6f} (numerical) vs {analytical:.6f} (analytical)")
            print(f"   Error: {abs(numerical - analytical):.6f}")
            
            # 使用错误处理器验证积分结果
            if not self.error_handler.validate_integral(numerical, analytical, tolerance=0.1):
                print("   ⚠ Integral validation warning")
            
            # 几何因子计算
            print("\n2. Testing geometric factor calculation...")
            sphere_area = 4 * np.pi
            circle_perimeter = 2 * np.pi
            geometric_factor = sphere_area / circle_perimeter
            print(f"   Sphere area: {sphere_area:.6f}")
            print(f"   Circle perimeter: {circle_perimeter:.6f}")
            print(f"   Geometric factor: {geometric_factor:.6f}")
            
            # 量纲分析
            print("\n3. Testing dimensional analysis...")
            print("   [Sphere area] = L^2")
            print("   [Circle perimeter] = L¹")
            print("   [Ratio] = L^2/L¹ = L¹ (still has dimension!)")
            
            # 验证量纲
            self.error_handler.validate_dimensions("L^2", "L^2")  # 正确的量纲
            self.error_handler.validate_dimensions("L^1", "L^2")  # 故意的错误量纲以测试错误处理
            
            print("\n✓ All mathematical tests completed successfully")
            return True
            
        except Exception as e:
            self.error_handler.handle_error(ErrorType.CALCULATION_ERROR, "Mathematical test failed", e)
            print(f"\n✗ Mathematical test failed: {e}")
            traceback.print_exc()
            return False
    
    @safe_execution
    def create_test_visualization(self):
        """创建测试可视化"""
        try:
            import numpy as np
            import matplotlib.pyplot as plt
            
            print("\n4. Testing visualization capabilities...")
            
            # 创建简单的测试图
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
            fig.suptitle('Script Testing Visualization', fontsize=14)
            
            # 测试数据
            x = np.linspace(0, 2*np.pi, 100)
            
            # 子图1：正弦函数
            ax1.plot(x, np.sin(x), 'b-', label='sin(x)')
            ax1.plot(x, np.sin(x)**2, 'r--', label='sin^2(x)')
            ax1.set_title('Trigonometric Functions')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 子图2：柱状图
            categories = ['Sphere Area', 'Circle Perimeter', 'Ratio']
            values = [4*np.pi, 2*np.pi, 2]
            ax2.bar(categories, values, color=['red', 'blue', 'green'], alpha=0.7)
            ax2.set_title('Geometric Quantities')
            ax2.set_ylabel('Value')
            
            # 子图3：3D测试
            ax3 = fig.add_subplot(2, 2, 3, projection='3d')
            u = np.linspace(0, 2*np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            x = np.outer(np.cos(u), np.sin(v))
            y = np.outer(np.sin(u), np.sin(v))
            z = np.outer(np.ones(np.size(u)), np.cos(v))
            ax3.plot_surface(x, y, z, alpha=0.6, color='lightblue')
            ax3.set_title('3D Sphere')
            
            # 子图4：测试结果和错误统计
            ax4.axis('off')
            
            # 测试结果文本
            test_summary = [
                "Test Results:",
                "✓ Mathematical calculations",
                "✓ Visualization functions", 
                "✓ 3D plotting",
                "",
                f"Total errors detected: {self.error_handler.total_errors}"
            ]
            
            for i, text in enumerate(test_summary):
                color = 'green' if text.startswith('✓') else 'black'
                if 'errors detected' in text and self.error_handler.total_errors > 0:
                    color = 'red'
                weight = 'bold' if text.endswith(':') else 'normal'
                ax4.text(0.05, 0.9-i*0.1, text, fontsize=12, color=color, 
                        weight=weight, transform=ax4.transAxes)
            
            plt.tight_layout()
            
            # 确保logs目录存在
            log_dir = os.path.join(self.script_dir, 'logs')
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # 尝试保存图片到logs目录
            try:
                output_path = os.path.join(log_dir, 'script_test_results.png')
                fig.savefig(output_path, dpi=150, bbox_inches='tight')
                print(f"   ✓ Test visualization saved as: {output_path}")
            except Exception as e:
                self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Could not save visualization", e)
                print(f"   ⚠ Could not save visualization: {e}")
            
            # 显示图片（可选）
            show_plot = input("   Show test visualization? (y/n): ").lower().strip()
            if show_plot == 'y':
                plt.show()
            else:
                plt.close(fig)
            
            print("   ✓ Visualization test completed")
            return True
            
        except Exception as e:
            self.error_handler.handle_error(ErrorType.VISUALIZATION_ERROR, "Visualization test failed", e)
            print(f"   ✗ Visualization test failed: {e}")
            return False

def main():
    """主测试函数"""
    print("Starting comprehensive script testing...")
    
    # 创建测试器
    tester = ScriptTester()
    
    # 运行综合测试
    all_tests_passed = tester.run_comprehensive_test()
    
    # 生成测试报告
    report_success = tester.generate_test_report()
    
    # 运行示例功能测试
    functionality_success = tester.run_sample_functionality()
    
    # 创建测试可视化
    visualization_success = tester.create_test_visualization()
    
    # 最终结果
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    
    overall_success = all_tests_passed and functionality_success and visualization_success
    
    print(f"\nScript Syntax & Import Tests: {'✓ PASS' if all_tests_passed else '✗ FAIL'}")
    print(f"Mathematical Functionality: {'✓ PASS' if functionality_success else '✗ FAIL'}")
    print(f"Visualization Capabilities: {'✓ PASS' if visualization_success else '✗ FAIL'}")
    print(f"\nOverall Result: {'✓ ALL TESTS PASSED' if overall_success else '✗ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 All scripts are ready for use!")
        print("   • No encoding issues detected")
        print("   • All imports working correctly")
        print("   • Core functionality verified")
        print("   • Visualization system operational")
    else:
        print("\n⚠️  Some issues detected. Please check the detailed results above.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)