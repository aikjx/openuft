#!/usr/bin/env python3
"""
统一场论核心公式可视化系统 - 性能测试与质量保证脚本

该脚本用于测试系统的性能和确保质量，包括：
1. 计算性能测试
2. 渲染性能测试
3. 功能完整性测试
4. 代码质量检查
"""

import numpy as np
import time
import os
import sys
import json
from typing import Dict, List, Tuple

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 自定义JSON编码器，处理numpy类型
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        return super(NumpyEncoder, self).default(obj)

try:
    from high_performance_optimization import HighPerformanceCalculator, NumericalOptimizer, FieldCalculator
    from unified_field_visualizer import SpiralSpacetimeVisualizer
    from enhanced_visualizations import MassDefinitionVisualizer, UnifiedForceVisualizer
    PERFORMANCE_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"警告: 无法导入性能测试模块: {e}")
    PERFORMANCE_MODULE_AVAILABLE = False


class PerformanceTester:
    """性能测试类"""
    
    def __init__(self):
        """初始化性能测试器"""
        self.results = {}
        self.start_time = 0
        self.end_time = 0
    
    def start_timer(self):
        """开始计时"""
        self.start_time = time.time()
    
    def stop_timer(self) -> float:
        """停止计时并返回执行时间"""
        self.end_time = time.time()
        return self.end_time - self.start_time
    
    def test_calculation_performance(self) -> Dict:
        """测试计算性能"""
        if not PERFORMANCE_MODULE_AVAILABLE:
            return {"error": "性能模块不可用"}
        
        results = {}
        
        try:
            calculator = HighPerformanceCalculator()
            optimizer = NumericalOptimizer()
            field_calc = FieldCalculator()
            
            # 测试数值计算性能
            large_array = np.random.rand(1000000)
            calc_results = calculator.compare_performance(
                [optimizer.regular_calculation, optimizer.numpy_vectorized],
                large_array
            )
            
            if PERFORMANCE_MODULE_AVAILABLE and hasattr(optimizer, 'numba_optimized'):
                calc_results.extend(calculator.compare_performance(
                    [optimizer.numba_optimized],
                    large_array
                ))
            
            results['numerical_calculation'] = calc_results
            
            # 测试场计算性能
            n_points = 100000
            x = np.random.rand(n_points) * 10 - 5
            y = np.random.rand(n_points) * 10 - 5
            z = np.random.rand(n_points) * 10 - 5
            v1 = np.array([1, 0, 0])
            v2 = np.array([0, 1, 0])
            k = 1.0
            dm_dt = 0.5
            
            field_results = calculator.compare_performance(
                [field_calc.calculate_electric_field_regular, field_calc.calculate_electric_field_vectorized],
                x, y, z, v1, v2, k, dm_dt
            )
            
            if PERFORMANCE_MODULE_AVAILABLE and hasattr(field_calc, 'calculate_electric_field_optimized'):
                field_results.extend(calculator.compare_performance(
                    [field_calc.calculate_electric_field_optimized],
                    x, y, z, v1, v2, k, dm_dt
                ))
            
            results['field_calculation'] = field_results
            
            # 获取性能统计
            results['performance_stats'] = calculator.get_performance_stats()
            
        except Exception as e:
            results['error'] = f"测试失败: {str(e)}"
        
        return results
    
    def test_rendering_performance(self) -> Dict:
        """测试渲染性能"""
        results = {}
        
        try:
            # 测试基础可视化性能
            if PERFORMANCE_MODULE_AVAILABLE:
                visualizers = [
                    SpiralSpacetimeVisualizer(),
                    MassDefinitionVisualizer(),
                    UnifiedForceVisualizer()
                ]
                
                for viz in visualizers:
                    self.start_timer()
                    figures = viz.visualize()
                    exec_time = self.stop_timer()
                    
                    results[viz.formula_name] = {
                        'execution_time': exec_time,
                        'figures_generated': len(figures)
                    }
                    
                    # 释放内存
                    for fig in figures:
                        import matplotlib.pyplot as plt
                        plt.close(fig)
            
        except Exception as e:
            results['error'] = f"渲染测试失败: {str(e)}"
        
        return results
    
    def test_functionality(self) -> Dict:
        """测试功能完整性"""
        results = {
            'modules_available': {},
            'files_exist': {},
            'functionality_tests': []
        }
        
        # 检查模块可用性
        results['modules_available']['numpy'] = 'numpy' in sys.modules
        results['modules_available']['matplotlib'] = 'matplotlib' in sys.modules
        results['modules_available']['high_performance'] = PERFORMANCE_MODULE_AVAILABLE
        
        # 检查关键文件存在
        critical_files = [
            'unified_field_visualizer.py',
            'enhanced_visualizations.py',
            'field_visualizations.py',
            'missing_formulas_visualization.py',
            'remaining_formulas_visualization.py',
            'high_performance_optimization.py',
            'comprehensive_dashboard.html',
            'advanced_visualization.html',
            'README.md'
        ]
        
        for file in critical_files:
            file_path = os.path.join(os.path.dirname(__file__), file)
            results['files_exist'][file] = os.path.exists(file_path)
        
        # 运行简单的功能测试
        test_cases = [
            {
                'name': '基本可视化测试',
                'test': self._test_basic_visualization
            },
            {
                'name': '文件写入测试',
                'test': self._test_file_writing
            },
            {
                'name': '参数处理测试',
                'test': self._test_parameter_handling
            }
        ]
        
        for test_case in test_cases:
            try:
                result = test_case['test']()
                results['functionality_tests'].append({
                    'name': test_case['name'],
                    'result': '通过' if result else '失败'
                })
            except Exception as e:
                results['functionality_tests'].append({
                    'name': test_case['name'],
                    'result': f'错误: {str(e)}'
                })
        
        return results
    
    def _test_basic_visualization(self) -> bool:
        """测试基本可视化功能"""
        if not PERFORMANCE_MODULE_AVAILABLE:
            return False
        
        try:
            viz = SpiralSpacetimeVisualizer()
            figures = viz.visualize()
            return len(figures) > 0
        except:
            return False
    
    def _test_file_writing(self) -> bool:
        """测试文件写入功能"""
        try:
            test_dir = os.path.join(os.path.dirname(__file__), 'test_output')
            os.makedirs(test_dir, exist_ok=True)
            
            test_file = os.path.join(test_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            
            success = os.path.exists(test_file)
            
            # 清理
            if success:
                os.remove(test_file)
                if os.path.exists(test_dir):
                    os.rmdir(test_dir)
            
            return success
        except:
            return False
    
    def _test_parameter_handling(self) -> bool:
        """测试参数处理功能"""
        if not PERFORMANCE_MODULE_AVAILABLE:
            return False
        
        try:
            viz = MassDefinitionVisualizer()
            # 测试不同参数值
            omega = np.array([1.0, 2.0, 3.0])
            mass = viz.calculate_mass(omega)
            return len(mass) == len(omega)
        except:
            return False
    
    def generate_report(self) -> Dict:
        """生成完整的测试报告"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': {
                'python_version': sys.version,
                'numpy_version': np.__version__ if 'numpy' in sys.modules else '未安装',
                'cwd': os.getcwd(),
                'platform': sys.platform
            },
            'performance_tests': {
                'calculation': self.test_calculation_performance(),
                'rendering': self.test_rendering_performance()
            },
            'functionality_test': self.test_functionality(),
            'summary': self._generate_summary()
        }
        
        return report
    
    def _generate_summary(self) -> Dict:
        """生成测试摘要"""
        functionality_test = self.test_functionality()
        
        # 计算文件存在率
        files_exist = functionality_test.get('files_exist', {})
        total_files = len(files_exist)
        existing_files = sum(1 for exists in files_exist.values() if exists)
        file_existence_rate = (existing_files / total_files * 100) if total_files > 0 else 0
        
        # 计算功能测试通过率
        functionality_tests = functionality_test.get('functionality_tests', [])
        passed_tests = sum(1 for test in functionality_tests if test.get('result') == '通过')
        test_pass_rate = (passed_tests / len(functionality_tests) * 100) if functionality_tests else 0
        
        return {
            'file_existence_rate': file_existence_rate,
            'test_pass_rate': test_pass_rate,
            'modules_available': functionality_test.get('modules_available', {}),
            'status': '成功' if file_existence_rate == 100 and test_pass_rate == 100 else '需要关注'
        }
    
    def save_report(self, report: Dict, filename: str = 'performance_report.json'):
        """保存测试报告到文件"""
        report_path = os.path.join(os.path.dirname(__file__), filename)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
        return report_path


def main():
    """主函数"""
    print("统一场论核心公式可视化系统 - 性能测试与质量保证")
    print("=" * 80)
    
    tester = PerformanceTester()
    
    print("\n1. 开始性能测试...")
    print("-" * 60)
    
    # 生成测试报告
    report = tester.generate_report()
    
    print("\n2. 测试结果摘要:")
    print("-" * 60)
    
    summary = report['summary']
    print(f"文件存在率: {summary['file_existence_rate']:.1f}%")
    print(f"测试通过率: {summary['test_pass_rate']:.1f}%")
    print(f"系统状态: {summary['status']}")
    
    print("\n3. 模块可用性:")
    for module, available in summary['modules_available'].items():
        status = "✓" if available else "✗"
        print(f"  {status} {module}")
    
    print("\n4. 计算性能测试:")
    calc_results = report['performance_tests']['calculation']
    if 'numerical_calculation' in calc_results:
        for result in calc_results['numerical_calculation'][:3]:  # 只显示前3个结果
            print(f"  {result['function']}: {result['execution_time']:.6f}s", end='')
            if 'speedup' in result and result['speedup'] is not None:
                print(f" (Speedup: {result['speedup']:.2f}x)")
            else:
                print()
    
    print("\n5. 渲染性能测试:")
    render_results = report['performance_tests']['rendering']
    for viz_name, result in render_results.items():
        if 'execution_time' in result:
            print(f"  {viz_name}: {result['execution_time']:.6f}s")
    
    # 保存测试报告
    report_path = tester.save_report(report)
    print(f"\n6. 测试报告已保存到: {report_path}")
    
    print("\n" + "=" * 80)
    print("性能测试与质量保证完成!")
    print(f"系统状态: {summary['status']}")
    
    if summary['status'] == '成功':
        print("✓ 所有测试通过，系统运行正常!")
    else:
        print("⚠ 部分测试未通过，建议检查系统配置")


if __name__ == "__main__":
    main()