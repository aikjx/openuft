import numpy as np
from high_performance_optimization import HighPerformanceCalculator, NumericalOptimizer

# 初始化
calculator = HighPerformanceCalculator()
optimizer = NumericalOptimizer()

# 创建测试数据
large_array = np.random.rand(100000)

# 比较不同计算方法
funcs = [
    optimizer.regular_calculation,
    optimizer.numpy_vectorized
]

performance_results = calculator.compare_performance(funcs, large_array)
print("Performance results:")
for i, result in enumerate(performance_results):
    print(f"\nResult {i}:")
    print(f"  Function: {result['function']}")
    print(f"  Execution time: {result['execution_time']}")
    print(f"  Speedup: {result.get('speedup')}")
    print(f"  Speedup type: {type(result.get('speedup'))}")
    print(f"  Speedup is None: {result.get('speedup') is None}")