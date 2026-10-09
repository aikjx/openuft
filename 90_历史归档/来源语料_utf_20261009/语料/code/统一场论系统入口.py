#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心算法系统入口
Unified Field Theory Core Algorithm System Entry

该文件是统一场论核心算法系统的主入口，提供命令行界面和批处理功能。
This file is the main entry point for the unified field theory core algorithm system, providing command-line interface and batch processing functionality.

功能：
1. 命令行参数解析
2. 批处理模式执行
3. 交互式模式运行
4. 系统状态检查
5. 模块测试
6. 性能分析
7. 结果导出

作者：统一场论算法联盟
Author: Unified Field Theory Algorithm Alliance
创建日期：2026-01-17
Creation Date: 2026-01-17
版本：1.0.0
Version: 1.0.0
"""

import argparse
import json
import os
import sys
import time
import logging
from typing import Dict, Any, List, Optional

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入整合器
from 统一场论核心算法整合模块 import (
    get_integrator,
    calculate_geometric_factor,
    calculate_gravity_light_speed,
    calculate_electromagnetic_coupling,
    calculate_spacetime_unification,
    calculate_three_dimensional_spiral,
    calculate_cosmic_grand_unification,
    calculate_wave_equation,
    optimize_performance,
    train_model,
    verify_equation,
    run_performance_test,
    visualize_data,
    run_unified_verification,
    run_comprehensive_calculation,
    get_system_status,
    get_system_info
)

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("utf_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("UTF_System")

class UTFSystem:
    """统一场论系统类"""
    
    def __init__(self):
        """初始化系统"""
        self.integrator = get_integrator()
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def parse_arguments(self) -> argparse.Namespace:
        """解析命令行参数"""
        parser = argparse.ArgumentParser(
            description='统一场论核心算法系统',
            formatter_class=argparse.RawTextHelpFormatter
        )
        
        # 模式选择
        parser.add_argument('--mode', choices=['batch', 'interactive', 'test', 'status', 'performance'],
                          default='interactive', help='运行模式')
        
        # 批处理模式参数
        parser.add_argument('--batch-file', type=str, help='批处理配置文件路径')
        
        # 计算类型
        parser.add_argument('--calculation', choices=[
            'geometric_factor', 'gravity_light_speed', 'electromagnetic_coupling',
            'spacetime_unification', 'three_dimensional_spiral', 'cosmic_grand_unification',
            'wave_equation', 'unified_field_theory', 'performance_analysis', 'visualization_analysis'
        ], help='计算类型')
        
        # 验证参数
        parser.add_argument('--verify', action='store_true', help='运行验证')
        parser.add_argument('--equations', nargs='+', help='要验证的方程列表')
        
        # 性能测试参数
        parser.add_argument('--performance-test', choices=['speed', 'accuracy', 'memory'],
                          help='性能测试类型')
        
        # 可视化参数
        parser.add_argument('--visualize', action='store_true', help='生成可视化结果')
        parser.add_argument('--visualization-type', type=str, help='可视化类型')
        
        # 输出参数
        parser.add_argument('--output', type=str, help='输出文件路径')
        parser.add_argument('--format', choices=['json', 'csv', 'txt'], default='json', help='输出格式')
        
        # 系统参数
        parser.add_argument('--verbose', action='store_true', help='详细输出')
        parser.add_argument('--debug', action='store_true', help='调试模式')
        
        return parser.parse_args()
    
    def run_batch_mode(self, batch_file: str) -> Dict[str, Any]:
        """运行批处理模式"""
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.info(f"开始批处理模式，配置文件: {batch_file}")
            
            results = {}
            total_start_time = time.time()
            
            for task in config.get('tasks', []):
                task_name = task.get('name', f'task_{len(results)}')
                task_type = task.get('type')
                task_params = task.get('parameters', {})
                
                logger.info(f"执行任务: {task_name} (类型: {task_type})")
                
                try:
                    task_start_time = time.time()
                    
                    if task_type == 'geometric_factor':
                        result = calculate_geometric_factor(**task_params)
                    elif task_type == 'gravity_light_speed':
                        result = calculate_gravity_light_speed(**task_params)
                    elif task_type == 'electromagnetic_coupling':
                        result = calculate_electromagnetic_coupling(**task_params)
                    elif task_type == 'spacetime_unification':
                        result = calculate_spacetime_unification(**task_params)
                    elif task_type == 'three_dimensional_spiral':
                        result = calculate_three_dimensional_spiral(**task_params)
                    elif task_type == 'cosmic_grand_unification':
                        result = calculate_cosmic_grand_unification(**task_params)
                    elif task_type == 'wave_equation':
                        result = calculate_wave_equation(**task_params)
                    elif task_type == 'unified_field_theory':
                        result = run_comprehensive_calculation('unified_field_theory', **task_params)
                    elif task_type == 'performance_analysis':
                        result = run_comprehensive_calculation('performance_analysis', **task_params)
                    elif task_type == 'visualization_analysis':
                        result = run_comprehensive_calculation('visualization_analysis', **task_params)
                    elif task_type == 'verify':
                        result = run_unified_verification(**task_params)
                    elif task_type == 'performance_test':
                        result = run_performance_test(**task_params)
                    elif task_type == 'visualize':
                        data = task_params.pop('data', {})
                        result = visualize_data(**task_params, data=data)
                    else:
                        result = {"error": f"未知任务类型: {task_type}"}
                    
                    task_end_time = time.time()
                    result['execution_time'] = task_end_time - task_start_time
                    results[task_name] = result
                    
                    logger.info(f"任务 {task_name} 完成，耗时: {result['execution_time']:.2f} 秒")
                    
                except Exception as e:
                    error_msg = f"执行任务 {task_name} 时发生错误: {str(e)}"
                    logger.error(error_msg)
                    results[task_name] = {"error": error_msg}
            
            total_end_time = time.time()
            summary = {
                "total_tasks": len(config.get('tasks', [])),
                "total_execution_time": total_end_time - total_start_time,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            results['summary'] = summary
            
            # 保存结果
            output_file = config.get('output_file', os.path.join(self.output_dir, f'batch_result_{time.strftime("%Y%m%d_%H%M%S")}.json'))
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"批处理完成，结果保存至: {output_file}")
            return results
            
        except Exception as e:
            error_msg = f"运行批处理模式时发生错误: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def run_interactive_mode(self) -> None:
        """运行交互式模式"""
        print("=== 统一场论核心算法系统 ===")
        print("交互式模式启动，输入 'help' 查看可用命令")
        print("输入 'exit' 退出系统")
        print("=" * 50)
        
        while True:
            try:
                command = input(">>> ").strip()
                
                if not command:
                    continue
                
                if command == 'exit' or command == 'quit':
                    print("系统退出")
                    break
                
                if command == 'help':
                    self.show_help()
                    continue
                
                if command == 'status':
                    self.show_status()
                    continue
                
                if command == 'modules':
                    self.show_modules()
                    continue
                
                if command == 'info':
                    self.show_info()
                    continue
                
                # 解析命令
                parts = command.split()
                cmd = parts[0]
                
                if cmd == 'calculate':
                    if len(parts) < 2:
                        print("请指定计算类型")
                        continue
                    calculation_type = parts[1]
                    self.run_calculation(calculation_type, parts[2:])
                
                elif cmd == 'verify':
                    equations = parts[1:] if len(parts) > 1 else None
                    self.run_verification(equations)
                
                elif cmd == 'test':
                    if len(parts) < 2:
                        print("请指定测试类型")
                        continue
                    test_type = parts[1]
                    self.run_test(test_type)
                
                elif cmd == 'visualize':
                    if len(parts) < 2:
                        print("请指定可视化类型")
                        continue
                    viz_type = parts[1]
                    self.run_visualization(viz_type)
                
                elif cmd == 'performance':
                    if len(parts) < 2:
                        print("请指定性能测试类型")
                        continue
                    perf_type = parts[1]
                    self.run_performance_test(perf_type)
                
                else:
                    print(f"未知命令: {command}")
                    print("输入 'help' 查看可用命令")
            
            except KeyboardInterrupt:
                print("\n系统退出")
                break
            except Exception as e:
                print(f"执行命令时发生错误: {str(e)}")
    
    def show_help(self) -> None:
        """显示帮助信息"""
        print("=== 可用命令 ===")
        print("help           - 显示帮助信息")
        print("status         - 显示系统状态")
        print("modules        - 显示已加载模块")
        print("info           - 显示系统信息")
        print("calculate <type> [params] - 执行计算")
        print("verify [equations] - 运行验证")
        print("test <type>    - 运行测试")
        print("visualize <type> - 生成可视化")
        print("performance <type> - 运行性能测试")
        print("exit/quit      - 退出系统")
        print("=" * 50)
    
    def show_status(self) -> None:
        """显示系统状态"""
        status = get_system_status()
        print("=== 系统状态 ===")
        print(f"已加载模块: {len(status.get('loaded_modules', []))}")
        print(f"模块状态:")
        for module, module_status in status.get('module_status', {}).items():
            print(f"  {module}: {'已加载' if module_status else '未加载'}")
        print(f"性能指标: {len(status.get('performance_metrics', {}))} 项")
        print(f"验证结果: {len(status.get('verification_results', {}))} 项")
        print(f"系统时间: {status.get('system_time')}")
        print("=" * 50)
    
    def show_modules(self) -> None:
        """显示已加载模块"""
        modules = self.integrator.get_loaded_modules()
        print("=== 已加载模块 ===")
        for module in modules:
            print(f"  - {module}")
        print(f"总计: {len(modules)} 个模块")
        print("=" * 50)
    
    def show_info(self) -> None:
        """显示系统信息"""
        info = get_system_info()
        print("=== 系统信息 ===")
        for key, value in info.items():
            print(f"{key}: {value}")
        print("=" * 50)
    
    def run_calculation(self, calculation_type: str, params: List[str]) -> None:
        """运行计算"""
        print(f"开始计算: {calculation_type}")
        
        try:
            if calculation_type == 'geometric_factor':
                result = calculate_geometric_factor()
            elif calculation_type == 'gravity_light_speed':
                result = calculate_gravity_light_speed()
            elif calculation_type == 'electromagnetic_coupling':
                result = calculate_electromagnetic_coupling()
            elif calculation_type == 'spacetime_unification':
                result = calculate_spacetime_unification()
            elif calculation_type == 'three_dimensional_spiral':
                result = calculate_three_dimensional_spiral()
            elif calculation_type == 'cosmic_grand_unification':
                result = calculate_cosmic_grand_unification()
            elif calculation_type == 'wave_equation':
                result = calculate_wave_equation()
            elif calculation_type == 'unified_field_theory':
                result = run_comprehensive_calculation('unified_field_theory')
            else:
                print(f"未知计算类型: {calculation_type}")
                return
            
            print("计算结果:")
            self._print_result(result)
            
        except Exception as e:
            print(f"计算时发生错误: {str(e)}")
    
    def run_verification(self, equations: List[str] = None) -> None:
        """运行验证"""
        print("开始验证...")
        
        try:
            result = run_unified_verification(equations=equations)
            print("验证结果:")
            self._print_result(result)
            
        except Exception as e:
            print(f"验证时发生错误: {str(e)}")
    
    def run_test(self, test_type: str) -> None:
        """运行测试"""
        print(f"开始测试: {test_type}")
        
        try:
            if test_type == 'modules':
                self.test_modules()
            elif test_type == 'calculations':
                self.test_calculations()
            elif test_type == 'performance':
                self.test_performance()
            else:
                print(f"未知测试类型: {test_type}")
                
        except Exception as e:
            print(f"测试时发生错误: {str(e)}")
    
    def test_modules(self) -> None:
        """测试模块加载"""
        print("=== 模块测试 ===")
        status = self.integrator.get_module_status()
        for module, module_status in status.items():
            print(f"{module}: {'✓' if module_status else '✗'}")
        print(f"模块加载成功率: {sum(status.values())/len(status)*100:.1f}%")
    
    def test_calculations(self) -> None:
        """测试计算功能"""
        print("=== 计算功能测试 ===")
        
        tests = [
            ('几何因子', calculate_geometric_factor),
            ('引力光速统一方程', calculate_gravity_light_speed),
            ('电磁光速几何耦合常数', calculate_electromagnetic_coupling),
            ('时空同一化', calculate_spacetime_unification),
            ('三维螺旋时空', calculate_three_dimensional_spiral),
            ('宇宙大统一方程', calculate_cosmic_grand_unification),
            ('波动方程', calculate_wave_equation)
        ]
        
        for test_name, test_func in tests:
            try:
                start_time = time.time()
                result = test_func()
                end_time = time.time()
                
                if 'error' not in result:
                    print(f"{test_name}: ✓ 耗时: {end_time - start_time:.2f} 秒")
                else:
                    print(f"{test_name}: ✗ 错误: {result['error']}")
                    
            except Exception as e:
                print(f"{test_name}: ✗ 异常: {str(e)}")
    
    def test_performance(self) -> None:
        """测试性能"""
        print("=== 性能测试 ===")
        
        test_funcs = [
            ('几何因子计算', calculate_geometric_factor),
            ('引力光速计算', calculate_gravity_light_speed),
            ('电磁耦合计算', calculate_electromagnetic_coupling)
        ]
        
        for test_name, test_func in test_funcs:
            try:
                start_time = time.time()
                # 运行多次以获得更准确的性能数据
                for _ in range(10):
                    test_func()
                end_time = time.time()
                avg_time = (end_time - start_time) / 10
                print(f"{test_name}: 平均耗时: {avg_time:.4f} 秒")
            except Exception as e:
                print(f"{test_name}: 测试失败: {str(e)}")
    
    def run_visualization(self, viz_type: str) -> None:
        """运行可视化"""
        print(f"生成可视化: {viz_type}")
        
        try:
            # 生成示例数据
            data = {
                "title": f"统一场论{viz_type}可视化",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            result = visualize_data(viz_type, data)
            print("可视化结果:")
            self._print_result(result)
            
        except Exception as e:
            print(f"可视化时发生错误: {str(e)}")
    
    def run_performance_test(self, perf_type: str) -> None:
        """运行性能测试"""
        print(f"运行性能测试: {perf_type}")
        
        try:
            result = run_performance_test(perf_type)
            print("性能测试结果:")
            self._print_result(result)
            
        except Exception as e:
            print(f"性能测试时发生错误: {str(e)}")
    
    def _print_result(self, result: Dict[str, Any]) -> None:
        """打印结果"""
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for sub_key, sub_value in value.items():
                        print(f"  {sub_key}: {sub_value}")
                else:
                    print(f"{key}: {value}")
        else:
            print(result)
        print()
    
    def save_result(self, result: Dict[str, Any], output_file: str, format_type: str) -> None:
        """保存结果"""
        if format_type == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        elif format_type == 'txt':
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"统一场论计算结果\n")
                f.write(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"结果:\n")
                self._write_dict_to_txt(result, f)
        else:
            logger.warning(f"不支持的格式: {format_type}")
    
    def _write_dict_to_txt(self, data: Dict[str, Any], file_handle, indent: int = 0) -> None:
        """将字典写入文本文件"""
        for key, value in data.items():
            prefix = '  ' * indent
            if isinstance(value, dict):
                file_handle.write(f"{prefix}{key}:\n")
                self._write_dict_to_txt(value, file_handle, indent + 1)
            else:
                file_handle.write(f"{prefix}{key}: {value}\n")
    
    def run(self) -> None:
        """运行系统"""
        args = self.parse_arguments()
        
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
        
        try:
            if args.mode == 'batch':
                if not args.batch_file:
                    logger.error("批处理模式需要指定批处理配置文件")
                    return
                self.run_batch_mode(args.batch_file)
            
            elif args.mode == 'interactive':
                self.run_interactive_mode()
            
            elif args.mode == 'test':
                self.run_test('modules')
                self.run_test('calculations')
            
            elif args.mode == 'status':
                self.show_status()
            
            elif args.mode == 'performance':
                self.run_test('performance')
            
            else:
                logger.error(f"未知运行模式: {args.mode}")
                
        except Exception as e:
            logger.error(f"运行系统时发生错误: {str(e)}")
            raise

def main():
    """主函数"""
    try:
        system = UTFSystem()
        system.run()
    except Exception as e:
        logger.error(f"系统运行失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
