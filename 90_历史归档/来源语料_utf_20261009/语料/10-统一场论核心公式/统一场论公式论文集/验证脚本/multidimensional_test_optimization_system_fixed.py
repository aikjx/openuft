import time
import os

# 导入原始模块中的MultidimensionalTestOptimizer类
try:
    from multidimensional_test_optimization_system import MultidimensionalTestOptimizer
except ImportError:
    print("警告: 无法导入原始模块，将使用简化版本")
    
    # 简化版本的类定义，用于演示修复
    class MultidimensionalTestOptimizer:
        def __init__(self):
            self.results_dir = os.path.join(os.getcwd(), "multidimensional_test_results")
        
        def run_full_multidimensional_test(self, formulas=None):
            return {"status": "success"}
        
        def run_optimized_testing(self, formulas, dimensions):
            return {"status": "success"}
        
        def export_results_to_csv(self):
            return os.path.join(self.results_dir, "results.csv")

def main():
    # 创建多维测试优化系统实例
    test_optimizer = MultidimensionalTestOptimizer()
    
    print("统一场论多维测试优化系统启动中...")
    print("选项:")
    print("1. 运行完整多维测试")
    print("2. 运行优化测试")
    print("3. 测试特定公式")
    print("4. 退出")
    
    try:
        choice = input("请选择操作 (1-4): ")
        
        if choice == '1':
            # 运行完整多维测试
            test_optimizer.start_time = time.time()
            results = test_optimizer.run_full_multidimensional_test()
            
            # 导出CSV结果
            csv_path = test_optimizer.export_results_to_csv()
            
            print(f"\n多维测试完成!")
            print(f"综合报告保存在: {test_optimizer.results_dir}/reports/")
            print(f"可视化图表保存在: {test_optimizer.results_dir}/figures/")
            print(f"数据导出到: {csv_path}")
            
        elif choice == '2':
            # 运行优化测试
            # 默认优化测试重点公式（高优先级）
            high_priority_formulas = [1, 2, 3, 4, 7, 17]  # 高优先级公式
            
            # 默认优化测试重点维度
            priority_dimensions = ['数学推导', '物理意义', '数值验证']
            
            print(f"\n优化测试将重点测试以下内容:")
            print(f"- 重点公式: {[f'公式{i:02d}' for i in high_priority_formulas]}")
            print(f"- 重点维度: {priority_dimensions}")
            
            confirm = input("是否继续? (y/n): ")
            if confirm.lower() in ['y', 'yes']:
                test_optimizer.start_time = time.time()
                results = test_optimizer.run_optimized_testing(high_priority_formulas, priority_dimensions)
                
                print(f"\n优化测试完成!")
                print(f"优化报告保存在: {test_optimizer.results_dir}/reports/")
        
        elif choice == '3':
            # 测试特定公式
            try:
                formula_ids_input = input("请输入要测试的公式ID (用逗号分隔，如1,3,5): ")
                formula_ids = [int(id.strip()) for id in formula_ids_input.split(',')]
                
                # 验证公式ID
                valid_ids = []
                for formula_id in formula_ids:
                    if 1 <= formula_id <= 18:
                        valid_ids.append(formula_id)
                    else:
                        print(f"警告: 公式ID {formula_id} 无效，跳过")
                
                if valid_ids:
                    test_optimizer.start_time = time.time()
                    results = test_optimizer.run_full_multidimensional_test(valid_ids)
                    
                    print(f"\n特定公式测试完成!")
                    print(f"报告保存在: {test_optimizer.results_dir}/reports/")
                else:
                    print("没有有效的公式ID，退出")
            except ValueError:
                print("输入格式错误，请输入有效的公式ID")
        
        elif choice == '4':
            print("感谢使用统一场论多维测试优化系统，再见!")
            return
        
        else:
            print("无效选择，退出")
            return
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"运行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试任务完成")

if __name__ == "__main__":
    main()