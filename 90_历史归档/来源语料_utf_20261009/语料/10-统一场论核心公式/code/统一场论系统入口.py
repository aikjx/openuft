import time
import argparse
import json
import os
import logging
from typing import Dict, List, Tuple, Optional, Union, Any
import numpy as np

# 统一场论系统入口
# 版本: 3.1
# 功能: 提供统一场论核心算法的命令行接口

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'uft_system.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('UnifiedFieldTheory')

# 导入核心算法模块
from core_algorithm import FormulaCalculator, ConsistencyVerifier, PerformanceBenchmarker

class UnifiedFieldTheoryCore:
    def __init__(self, formula_db_path: str):
        """初始化统一场论核心
        
        Args:
            formula_db_path: 公式规格数据库路径
        """
        self.formula_db_path = formula_db_path
        self.formula_calculator = FormulaCalculator(formula_db_path)
        self.verifier = ConsistencyVerifier(self.formula_calculator)
        self.benchmarker = PerformanceBenchmarker(self.formula_calculator)
        self.modules = [
            "时空同一化方程",
            "三维螺旋时空方程",
            "质量定义方程",
            "引力场定义方程",
            "静止动量方程",
            "运动动量方程",
            "宇宙大统一方程",
            "空间波动方程",
            "电荷定义方程",
            "电场定义方程",
            "磁场定义方程",
            "变化引力场产生电磁场",
            "磁矢势方程",
            "变化引力场产生电场",
            "变化磁场产生引力场和电场",
            "统一场论能量方程",
            "光速飞行器动力学方程"
        ]
        logger.info(f"统一场论核心初始化完成，加载了 {len(self.formula_calculator.formula_db['formulas'])} 个公式")

def get_formula_db_path() -> str:
    """获取公式规格数据库路径"""
    return os.path.join(os.path.dirname(__file__), "公式规格数据库.json")

def calculate_all_core_algorithms(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """计算所有核心算法"""
    try:
        formula_db_path = get_formula_db_path()
        logger.info(f"开始计算所有核心算法，使用数据库: {formula_db_path}")
        calculator = FormulaCalculator(formula_db_path)
        results = calculator.calculate_all_formulas(parameters)
        logger.info(f"核心算法计算完成，成功: {results['summary']['successful_modules']}/{results['summary']['total_modules']}")
        return results
    except Exception as e:
        logger.error(f"计算核心算法时出错: {e}")
        raise

def verify_core_consistency() -> Dict[str, Any]:
    """验证核心算法一致性"""
    try:
        formula_db_path = get_formula_db_path()
        logger.info(f"开始验证核心算法一致性，使用数据库: {formula_db_path}")
        calculator = FormulaCalculator(formula_db_path)
        verifier = ConsistencyVerifier(calculator)
        results = verifier.verify_consistency()
        logger.info(f"一致性验证完成，通过: {results['summary']['consistent_tests']}/{results['summary']['total_tests']}")
        return results
    except Exception as e:
        logger.error(f"验证核心算法一致性时出错: {e}")
        raise

def benchmark_core_performance(iterations: int) -> Dict[str, Any]:
    """基准测试核心算法性能"""
    try:
        formula_db_path = get_formula_db_path()
        logger.info(f"开始基准测试核心算法性能，迭代次数: {iterations}")
        calculator = FormulaCalculator(formula_db_path)
        benchmarker = PerformanceBenchmarker(calculator)
        results = benchmarker.benchmark_performance(iterations)
        logger.info(f"性能基准测试完成，测试模块数: {results['summary']['total_modules_tested']}")
        return results
    except Exception as e:
        logger.error(f"基准测试核心算法性能时出错: {e}")
        raise

def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='统一场论核心算法系统')
    
    parser.add_argument('--mode', type=str, default='calculate', 
                        choices=['calculate', 'verify', 'benchmark', 'info'],
                        help='运行模式')
    
    parser.add_argument('--parameters', type=str, default='{}',
                        help='计算参数 (JSON格式)')
    
    parser.add_argument('--iterations', type=int, default=10,
                        help='基准测试迭代次数')
    
    parser.add_argument('--output', type=str, default=None,
                        help='输出文件路径')
    
    parser.add_argument('--verbose', action='store_true',
                        help='详细输出')
    
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='日志级别')
    
    return parser.parse_args()

def run_calculate_mode(parameters: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """运行计算模式"""
    logger.info("运行计算模式")
    print("运行计算模式...")
    print("=" * 60)
    
    start_time = time.time()
    results = calculate_all_core_algorithms(parameters)
    end_time = time.time()
    
    print(f"\n计算完成! 总耗时: {end_time - start_time:.4f} 秒")
    print(f"成功计算: {results['summary']['successful_modules']}/{results['summary']['total_modules']} 个模块")
    
    if verbose:
        print("\n详细结果:")
        for module_name, module_result in results.items():
            if module_name != 'summary':
                print(f"\n{module_name}:")
                if module_result['status'] == 'success':
                    print(f"  状态: 成功")
                    if 'execution_time' in module_result:
                        print(f"  执行时间: {module_result['execution_time']:.6f} 秒")
                    if 'result' in module_result:
                        result = module_result['result']
                        if isinstance(result, (int, float)):
                            print(f"  结果: {result:.6e}")
                        elif isinstance(result, dict):
                            print(f"  结果: {json.dumps(result, indent=4, ensure_ascii=False)}")
                        else:
                            print(f"  结果: {result}")
                else:
                    print(f"  状态: 错误")
                    print(f"  错误信息: {module_result['error']}")
    
    return results

def run_verify_mode(verbose: bool) -> Dict[str, Any]:
    """运行验证模式"""
    logger.info("运行验证模式")
    print("运行验证模式...")
    print("=" * 60)
    
    start_time = time.time()
    results = verify_core_consistency()
    end_time = time.time()
    
    print(f"\n验证完成! 总耗时: {end_time - start_time:.4f} 秒")
    print(f"通过验证: {results['summary']['consistent_tests']}/{results['summary']['total_tests']} 项测试")
    print(f"一致性率: {results['summary']['consistency_rate']:.2%}")
    
    if verbose:
        print("\n详细验证结果:")
        for test_name, test_result in results.items():
            if test_name != 'summary':
                print(f"\n{test_name}:")
                print(f"  一致性: {'通过' if test_result['consistent'] else '失败'}")
                if 'error' in test_result:
                    print(f"  错误信息: {test_result['error']}")
                else:
                    for key, value in test_result.items():
                        if key != 'consistent':
                            if isinstance(value, (int, float)):
                                print(f"  {key}: {value:.6e}")
                            else:
                                print(f"  {key}: {value}")
    
    return results

def run_benchmark_mode(iterations: int, verbose: bool) -> Dict[str, Any]:
    """运行基准测试模式"""
    logger.info(f"运行基准测试模式，迭代次数: {iterations}")
    print("运行基准测试模式...")
    print("=" * 60)
    
    start_time = time.time()
    results = benchmark_core_performance(iterations)
    end_time = time.time()
    
    print(f"\n基准测试完成! 总耗时: {end_time - start_time:.4f} 秒")
    print(f"测试模块数: {results['summary']['total_modules_tested']}")
    
    if verbose:
        print("\n性能排名 (从快到慢):")
        for module_name, performance_data in results['summary']['fastest_modules']:
            if isinstance(performance_data, dict) and 'average_time' in performance_data:
                print(f"  {module_name}: {performance_data['average_time']:.6f} 秒")
            else:
                print(f"  {module_name}: {performance_data:.6f} 秒")
        
        print("\n详细性能结果:")
        for module_name, performance_data in results.items():
            if module_name != 'summary':
                print(f"\n{module_name}:")
                if 'average_time' in performance_data:
                    print(f"  平均时间: {performance_data['average_time']:.6f} 秒")
                    print(f"  最小时间: {performance_data['min_time']:.6f} 秒")
                    print(f"  最大时间: {performance_data['max_time']:.6f} 秒")
                    print(f"  标准差: {performance_data['std_time']:.6f} 秒")
                else:
                    print(f"  状态: 错误")
                    print(f"  错误信息: {performance_data.get('error', '未知错误')}")
    
    return results

def run_info_mode() -> Dict[str, Any]:
    """运行信息模式"""
    logger.info("运行信息模式")
    print("统一场论核心算法系统信息")
    print("=" * 60)
    
    try:
        formula_db_path = get_formula_db_path()
        uft_core = UnifiedFieldTheoryCore(formula_db_path)
        
        print("\n系统信息:")
        print(f"  核心算法模块数: {len(uft_core.modules)}")
        print(f"  系统版本: 3.1")
        print(f"  Python版本: {__import__('sys').version}")
        print(f"  NumPy版本: {np.__version__}")
        print(f"  公式规格数据库: {formula_db_path}")
        print(f"  已实现公式数: {len(uft_core.formula_calculator.formula_db['formulas'])}")
        
        print("\n已加载模块:")
        for module_name in uft_core.modules:
            print(f"  - {module_name}")
        
        print("\n已实现公式:")
        for formula in uft_core.formula_calculator.formula_db['formulas']:
            print(f"  - {formula['id']}: {formula['name']}")
        
        print("\n系统功能:")
        print("  1. 几何因子计算")
        print("  2. 引力光速统一方程")
        print("  3. 电磁光速几何耦合常数计算")
        print("  4. 时空同一化方程计算")
        print("  5. 三维螺旋时空方程计算")
        print("  6. 质量定义方程计算")
        print("  7. 引力场定义方程计算")
        print("  8. 公式一致性验证")
        print("  9. 性能基准测试")
        print("  10. 并行计算优化")
        
        print("\n使用示例:")
        print("  # 计算所有核心算法")
        print("  python 统一场论系统入口.py --mode calculate")
        
        print("  # 验证核心算法一致性")
        print("  python 统一场论系统入口.py --mode verify")
        
        print("  # 运行性能基准测试")
        print("  python 统一场论系统入口.py --mode benchmark --iterations 100")
        
        print("  # 查看系统信息")
        print("  python 统一场论系统入口.py --mode info")
        
        logger.info("信息模式运行完成")
        return {"status": "success", "message": "System information displayed"}
    except Exception as e:
        logger.error(f"运行信息模式时出错: {e}")
        print(f"\n错误: {e}")
        return {"status": "error", "message": str(e)}

def save_output(results: Dict[str, Any], output_path: str) -> None:
    """保存输出结果"""
    if output_path:
        try:
            logger.info(f"保存结果到: {output_path}")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n结果已保存到: {output_path}")
            logger.info("结果保存成功")
        except Exception as e:
            logger.error(f"保存输出失败: {e}")
            print(f"\n保存输出失败: {e}")

def main() -> int:
    """主函数"""
    try:
        args = parse_arguments()
        
        # 设置日志级别
        logging.getLogger().setLevel(args.log_level)
        
        try:
            parameters = json.loads(args.parameters)
        except json.JSONDecodeError as e:
            logger.error(f"参数解析错误: {e}")
            print(f"参数解析错误: {e}")
            return 1
        
        logger.info(f"启动统一场论核心算法系统，模式: {args.mode}")
        print("统一场论核心算法系统")
        print("=" * 60)
        print(f"运行模式: {args.mode}")
        print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"日志级别: {args.log_level}")
        print()
        
        if args.mode == 'calculate':
            results = run_calculate_mode(parameters, args.verbose)
        elif args.mode == 'verify':
            results = run_verify_mode(args.verbose)
        elif args.mode == 'benchmark':
            results = run_benchmark_mode(args.iterations, args.verbose)
        elif args.mode == 'info':
            results = run_info_mode()
        else:
            logger.error(f"未知模式: {args.mode}")
            print(f"未知模式: {args.mode}")
            return 1
        
        if args.output:
            save_output(results, args.output)
        
        logger.info("系统运行完成")
        print("\n" + "=" * 60)
        print("系统运行完成!")
        
        return 0
    except Exception as e:
        logger.critical(f"系统运行时发生严重错误: {e}")
        print(f"\n系统错误: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
