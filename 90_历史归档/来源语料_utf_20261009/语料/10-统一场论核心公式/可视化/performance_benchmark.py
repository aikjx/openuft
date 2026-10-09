#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论高性能计算基准测试
全面测试系统的计算性能和优化效果
"""

import numpy as np
import time
import matplotlib.pyplot as plt
import json
from datetime import datetime

# 导入高性能计算模块
try:
    from high_performance_optimization import (
        HighPerformanceCalculator, NumericalOptimizer, FieldCalculator,
        AdaptiveSampler, GPUAccelerator
    )
    HIGH_PERFORMANCE_AVAILABLE = True
except ImportError as e:
    HIGH_PERFORMANCE_AVAILABLE = False
    print(f"高性能计算模块加载失败: {e}")

class PerformanceBenchmark:
    """性能基准测试类"""
    
    def __init__(self):
        """初始化性能基准测试"""
        self.calculator = HighPerformanceCalculator() if HIGH_PERFORMANCE_AVAILABLE else None
        self.optimizer = NumericalOptimizer() if HIGH_PERFORMANCE_AVAILABLE else None
        self.field_calc = FieldCalculator() if HIGH_PERFORMANCE_AVAILABLE else None
        self.sampler = AdaptiveSampler() if HIGH_PERFORMANCE_AVAILABLE else None
        self.gpu_accel = GPUAccelerator() if HIGH_PERFORMANCE_AVAILABLE else None
        
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {
                'high_performance_available': HIGH_PERFORMANCE_AVAILABLE,
                'gpu_available': self.gpu_accel.gpu_available() if self.gpu_accel else False,
                'numpy_version': np.__version__
            },
            'benchmarks': {}
        }
    
    def benchmark_numerical_calculation(self):
        """测试数值计算性能"""
        print("测试数值计算性能...")
        
        # 不同规模的测试数据
        sizes = [1000, 10000, 100000, 1000000]
        results = []
        
        for size in sizes:
            print(f"  测试数据规模: {size}")
            test_array = np.random.rand(size)
            
            # 测试不同计算方法
            methods = ['regular_calculation', 'numpy_vectorized']
            if HIGH_PERFORMANCE_AVAILABLE:
                methods.extend(['numba_optimized', 'gpu_optimized'])
            
            method_results = {}
            for method_name in methods:
                try:
                    method = getattr(self.optimizer, method_name)
                    exec_time, _ = self.calculator.benchmark(method, test_array)
                    method_results[method_name] = exec_time
                    print(f"    {method_name}: {exec_time:.6f}s")
                except Exception as e:
                    print(f"    {method_name}: 错误 - {e}")
            
            results.append({
                'size': size,
                'methods': method_results
            })
        
        self.results['benchmarks']['numerical_calculation'] = results
        return results
    
    def benchmark_field_calculation(self):
        """测试场计算性能"""
        print("测试场计算性能...")
        
        # 不同规模的测试数据
        sizes = [1000, 10000, 100000]
        results = []
        
        for size in sizes:
            print(f"  测试数据规模: {size}")
            
            # 生成测试数据
            x = np.random.rand(size) * 10 - 5
            y = np.random.rand(size) * 10 - 5
            z = np.random.rand(size) * 10 - 5
            v1 = np.array([1, 0, 0])
            v2 = np.array([0, 1, 0])
            k = 1.0
            dm_dt = 0.5
            
            # 测试不同计算方法
            methods = ['calculate_electric_field_regular', 'calculate_electric_field_vectorized']
            if HIGH_PERFORMANCE_AVAILABLE:
                methods.append('calculate_electric_field_optimized')
            
            method_results = {}
            for method_name in methods:
                try:
                    method = getattr(self.field_calc, method_name)
                    exec_time, _ = self.calculator.benchmark(method, x, y, z, v1, v2, k, dm_dt)
                    method_results[method_name] = exec_time
                    print(f"    {method_name}: {exec_time:.6f}s")
                except Exception as e:
                    print(f"    {method_name}: 错误 - {e}")
            
            results.append({
                'size': size,
                'methods': method_results
            })
        
        self.results['benchmarks']['field_calculation'] = results
        return results
    
    def benchmark_sampling_performance(self):
        """测试采样性能"""
        print("测试采样性能...")
        
        # 测试函数
        def test_function(x):
            return np.sin(10*x) + np.cos(5*x)
        
        # 不同误差阈值的测试
        error_thresholds = [1e-2, 1e-3, 1e-4, 1e-5]
        results = []
        
        for threshold in error_thresholds:
            print(f"  测试误差阈值: {threshold}")
            
            # 测试均匀采样
            exec_time, uniform_samples = self.calculator.benchmark(
                self.sampler.uniform_sampling, [0, 2*np.pi], 1000
            )
            
            # 测试自适应采样
            adaptive_time, adaptive_samples = self.calculator.benchmark(
                self.sampler.adaptive_sampling, test_function, [0, 2*np.pi], threshold
            )
            
            results.append({
                'threshold': threshold,
                'uniform_time': exec_time,
                'adaptive_time': adaptive_time,
                'uniform_samples': len(uniform_samples),
                'adaptive_samples': len(adaptive_samples),
                'efficiency': len(uniform_samples) / len(adaptive_samples)
            })
            
            print(f"    均匀采样: {exec_time:.6f}s ({len(uniform_samples)} 点)")
            print(f"    自适应采样: {adaptive_time:.6f}s ({len(adaptive_samples)} 点)")
            print(f"    效率提升: {len(uniform_samples)/len(adaptive_samples):.2f}x")
        
        self.results['benchmarks']['sampling_performance'] = results
        return results
    
    def benchmark_gpu_performance(self):
        """测试GPU性能"""
        print("测试GPU性能...")
        
        if not (HIGH_PERFORMANCE_AVAILABLE and self.gpu_accel.gpu_available()):
            print("  GPU不可用，跳过测试")
            return []
        
        # 不同规模的测试数据
        sizes = [100000, 1000000, 10000000]
        results = []
        
        for size in sizes:
            print(f"  测试数据规模: {size}")
            
            # 生成测试数据
            test_array = np.random.rand(size)
            
            # 测试CPU性能
            def cpu_test():
                return np.sin(test_array) * np.cos(test_array) + np.exp(-test_array**2)
            
            cpu_time, _ = self.calculator.benchmark(cpu_test)
            print(f"    CPU: {cpu_time:.6f}s")
            
            # 测试GPU性能
            def gpu_test():
                return self.gpu_accel.run_on_gpu(cpu_test)
            
            gpu_time, _ = self.calculator.benchmark(gpu_test)
            print(f"    GPU: {gpu_time:.6f}s")
            
            speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            print(f"    加速比: {speedup:.2fx}")
            
            results.append({
                'size': size,
                'cpu_time': cpu_time,
                'gpu_time': gpu_time,
                'speedup': speedup
            })
        
        self.results['benchmarks']['gpu_performance'] = results
        return results
    
    def generate_performance_report(self):
        """生成性能报告"""
        print("生成性能报告...")
        
        # 保存结果到JSON文件
        report_path = f"performance_benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"性能报告已保存为: {report_path}")
        
        # 生成性能图表
        self.generate_performance_charts()
        
        return report_path
    
    def generate_performance_charts(self):
        """生成性能图表"""
        print("生成性能图表...")
        
        # 数值计算性能图表
        if 'numerical_calculation' in self.results['benchmarks']:
            results = self.results['benchmarks']['numerical_calculation']
            
            plt.figure(figsize=(12, 8))
            for method in ['regular_calculation', 'numpy_vectorized']:
                times = [r['methods'].get(method, np.nan) for r in results]
                sizes = [r['size'] for r in results]
                plt.plot(sizes, times, marker='o', label=method)
            
            if HIGH_PERFORMANCE_AVAILABLE:
                for method in ['numba_optimized', 'gpu_optimized']:
                    times = [r['methods'].get(method, np.nan) for r in results]
                    sizes = [r['size'] for r in results]
                    plt.plot(sizes, times, marker='s', label=method)
            
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('数据规模')
            plt.ylabel('执行时间 (s)')
            plt.title('数值计算性能比较')
            plt.legend()
            plt.grid(True)
            plt.savefig('numerical_performance.png', dpi=150, bbox_inches='tight')
            print("数值计算性能图表已保存为: numerical_performance.png")
        
        # 场计算性能图表
        if 'field_calculation' in self.results['benchmarks']:
            results = self.results['benchmarks']['field_calculation']
            
            plt.figure(figsize=(12, 8))
            for method in ['calculate_electric_field_regular', 'calculate_electric_field_vectorized']:
                times = [r['methods'].get(method, np.nan) for r in results]
                sizes = [r['size'] for r in results]
                plt.plot(sizes, times, marker='o', label=method)
            
            if HIGH_PERFORMANCE_AVAILABLE:
                times = [r['methods'].get('calculate_electric_field_optimized', np.nan) for r in results]
                sizes = [r['size'] for r in results]
                plt.plot(sizes, times, marker='s', label='calculate_electric_field_optimized')
            
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('数据规模')
            plt.ylabel('执行时间 (s)')
            plt.title('场计算性能比较')
            plt.legend()
            plt.grid(True)
            plt.savefig('field_performance.png', dpi=150, bbox_inches='tight')
            print("场计算性能图表已保存为: field_performance.png")
        
        # GPU性能图表
        if 'gpu_performance' in self.results['benchmarks'] and self.results['benchmarks']['gpu_performance']:
            results = self.results['benchmarks']['gpu_performance']
            
            plt.figure(figsize=(12, 8))
            sizes = [r['size'] for r in results]
            cpu_times = [r['cpu_time'] for r in results]
            gpu_times = [r['gpu_time'] for r in results]
            speedups = [r['speedup'] for r in results]
            
            plt.subplot(2, 1, 1)
            plt.plot(sizes, cpu_times, marker='o', label='CPU')
            plt.plot(sizes, gpu_times, marker='s', label='GPU')
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('数据规模')
            plt.ylabel('执行时间 (s)')
            plt.title('CPU vs GPU性能比较')
            plt.legend()
            plt.grid(True)
            
            plt.subplot(2, 1, 2)
            plt.plot(sizes, speedups, marker='o', color='green')
            plt.xscale('log')
            plt.xlabel('数据规模')
            plt.ylabel('加速比 (CPU/GPU)')
            plt.title('GPU加速比')
            plt.grid(True)
            
            plt.tight_layout()
            plt.savefig('gpu_performance.png', dpi=150, bbox_inches='tight')
            print("GPU性能图表已保存为: gpu_performance.png")
        
        plt.close('all')
    
    def run_all_benchmarks(self):
        """运行所有基准测试"""
        print("=" * 120)
        print("统一场论高性能计算基准测试")
        print("=" * 120)
        print()
        
        if not HIGH_PERFORMANCE_AVAILABLE:
            print("高性能计算模块不可用，无法运行基准测试")
            return
        
        # 运行所有基准测试
        print("1. 测试数值计算性能")
        print("-" * 60)
        self.benchmark_numerical_calculation()
        print()
        
        print("2. 测试场计算性能")
        print("-" * 60)
        self.benchmark_field_calculation()
        print()
        
        print("3. 测试采样性能")
        print("-" * 60)
        self.benchmark_sampling_performance()
        print()
        
        print("4. 测试GPU性能")
        print("-" * 60)
        self.benchmark_gpu_performance()
        print()
        
        # 生成报告
        report_path = self.generate_performance_report()
        print()
        print("=" * 120)
        print("基准测试完成！")
        print(f"详细报告: {report_path}")
        print("性能图表已生成到当前目录")
        print("=" * 120)

if __name__ == "__main__":
    benchmark = PerformanceBenchmark()
    benchmark.run_all_benchmarks()
