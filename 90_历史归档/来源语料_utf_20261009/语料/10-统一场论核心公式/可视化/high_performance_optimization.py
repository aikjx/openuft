import numpy as np
import time
from typing import List, Tuple, Union, Callable

try:
    from numba import jit, cuda, vectorize, float64, int32
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    print("Numba not available, using regular Python implementation")

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    print("CuPy not available, GPU acceleration disabled")


class HighPerformanceCalculator:
    """
    高性能计算类，提供数值计算和GPU加速功能
    """
    
    def __init__(self):
        """初始化高性能计算器"""
        self.gpu_available = CUPY_AVAILABLE
        self.numba_available = NUMBA_AVAILABLE
        self.performance_logs = []
    
    def benchmark(self, func: Callable, *args, **kwargs) -> Tuple[float, any]:
        """
        基准测试函数性能
        
        Args:
            func: 要测试的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        
        Returns:
            执行时间（秒）和函数返回值
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.performance_logs.append({
            'function': func.__name__,
            'execution_time': execution_time,
            'args': str(args)[:100],
            'timestamp': time.time()
        })
        
        return execution_time, result
    
    def compare_performance(self, funcs: List[Callable], *args, **kwargs) -> List[dict]:
        """
        比较多个函数的性能
        
        Args:
            funcs: 函数列表
            *args: 函数参数
            **kwargs: 函数关键字参数
        
        Returns:
            性能比较结果列表
        """
        results = []
        for func in funcs:
            exec_time, result = self.benchmark(func, *args, **kwargs)
            results.append({
                'function': func.__name__,
                'execution_time': exec_time,
                'speedup': None,  # 第一个函数作为基准
                'result': result
            })
        
        # 计算加速比
        if results:
            baseline_time = results[0]['execution_time']
            for i in range(1, len(results)):
                results[i]['speedup'] = baseline_time / results[i]['execution_time']
        
        return results
    
    def get_performance_stats(self) -> dict:
        """
        获取性能统计信息
        
        Returns:
            性能统计字典
        """
        if not self.performance_logs:
            return {}
        
        times = [log['execution_time'] for log in self.performance_logs]
        return {
            'total_operations': len(self.performance_logs),
            'average_time': np.mean(times),
            'median_time': np.median(times),
            'min_time': np.min(times),
            'max_time': np.max(times),
            'total_time': sum(times)
        }


# 数值计算优化
class NumericalOptimizer:
    """
    数值计算优化类
    """
    
    @staticmethod
    def regular_calculation(x: np.ndarray) -> np.ndarray:
        """
        常规Python计算
        
        Args:
            x: 输入数组
        
        Returns:
            计算结果
        """
        result = np.zeros_like(x)
        for i in range(len(x)):
            result[i] = np.sin(x[i]) * np.cos(x[i]) + np.exp(-x[i]**2)
        return result
    
    @staticmethod
    def numba_optimized(x: np.ndarray) -> np.ndarray:
        """
        Numba优化计算
        
        Args:
            x: 输入数组
        
        Returns:
            计算结果
        """
        if NUMBA_AVAILABLE:
            # 使用更高效的Numba实现
            @jit(nopython=True, fastmath=True, cache=True)
            def optimized_calc(x):
                result = np.zeros_like(x)
                for i in range(len(x)):
                    result[i] = np.sin(x[i]) * np.cos(x[i]) + np.exp(-x[i]**2)
                return result
            
            # 预热函数
            optimized_calc(np.array([0.0, 1.0]))
            return optimized_calc(x)
        else:
            # 回退到常规计算
            return NumericalOptimizer.regular_calculation(x)
    
    @staticmethod
    def numpy_vectorized(x: np.ndarray) -> np.ndarray:
        """
        NumPy向量化计算
        
        Args:
            x: 输入数组
        
        Returns:
            计算结果
        """
        return np.sin(x) * np.cos(x) + np.exp(-x**2)
    
    @staticmethod
    def gpu_optimized(x: np.ndarray) -> np.ndarray:
        """
        GPU优化计算
        
        Args:
            x: 输入数组
        
        Returns:
            计算结果
        """
        if not CUPY_AVAILABLE:
            return NumericalOptimizer.numpy_vectorized(x)
        
        x_gpu = cp.asarray(x)
        result_gpu = cp.sin(x_gpu) * cp.cos(x_gpu) + cp.exp(-x_gpu**2)
        return cp.asnumpy(result_gpu)
    
    @staticmethod
    def fft_optimized(signal: np.ndarray) -> np.ndarray:
        """
        FFT优化计算，用于信号处理
        
        Args:
            signal: 输入信号
        
        Returns:
            FFT变换结果
        """
        try:
            # 使用NumPy的FFT实现
            fft_result = np.fft.fft(signal)
            return np.abs(fft_result)
        except Exception as e:
            print(f"FFT优化失败: {e}")
            return signal


# 场计算优化
class FieldCalculator:
    """
    场计算优化类
    """
    
    def __init__(self):
        self.calculator = HighPerformanceCalculator()
    
    def calculate_electric_field_regular(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, 
                                       v1: np.ndarray, v2: np.ndarray, k: float, dm_dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        常规电场计算
        
        Args:
            x, y, z: 空间坐标
            v1, v2: 速度矢量
            k: 比例常数
            dm_dt: 质量变化率
        
        Returns:
            Ex, Ey, Ez: 电场分量
        """
        Ex = np.zeros_like(x)
        Ey = np.zeros_like(y)
        Ez = np.zeros_like(z)
        
        for i in range(len(x)):
            r = np.sqrt(x[i]**2 + y[i]**2 + z[i]**2)
            if r < 1e-6:
                r = 1e-6
            
            # 计算叉积 V1 × V2
            cross_x = v1[1] * v2[2] - v1[2] * v2[1]
            cross_y = v1[2] * v2[0] - v1[0] * v2[2]
            cross_z = v1[0] * v2[1] - v1[1] * v2[0]
            
            Ex[i] = k * dm_dt * cross_x / (r**3)
            Ey[i] = k * dm_dt * cross_y / (r**3)
            Ez[i] = k * dm_dt * cross_z / (r**3)
        
        return Ex, Ey, Ez
    
    @staticmethod
    def _electric_field_kernel(x: np.ndarray, y: np.ndarray, z: np.ndarray, 
                              v1x: float, v1y: float, v1z: float, 
                              v2x: float, v2y: float, v2z: float, 
                              k: float, dm_dt: float, 
                              Ex: np.ndarray, Ey: np.ndarray, Ez: np.ndarray):
        """
        电场计算内核（Numba优化）
        """
        if NUMBA_AVAILABLE:
            @jit(nopython=True, fastmath=True)
            def kernel(x, y, z, v1x, v1y, v1z, v2x, v2y, v2z, k, dm_dt, Ex, Ey, Ez):
                # 计算叉积 V1 × V2
                cross_x = v1y * v2z - v1z * v2y
                cross_y = v1z * v2x - v1x * v2z
                cross_z = v1x * v2y - v1y * v2x
                
                for i in range(len(x)):
                    r = np.sqrt(x[i]**2 + y[i]**2 + z[i]**2)
                    if r < 1e-6:
                        r = 1e-6
                    
                    Ex[i] = k * dm_dt * cross_x / (r**3)
                    Ey[i] = k * dm_dt * cross_y / (r**3)
                    Ez[i] = k * dm_dt * cross_z / (r**3)
            
            kernel(x, y, z, v1x, v1y, v1z, v2x, v2y, v2z, k, dm_dt, Ex, Ey, Ez)
        else:
            # 常规Python实现
            cross_x = v1y * v2z - v1z * v2y
            cross_y = v1z * v2x - v1x * v2z
            cross_z = v1x * v2y - v1y * v2x
            
            for i in range(len(x)):
                r = np.sqrt(x[i]**2 + y[i]**2 + z[i]**2)
                if r < 1e-6:
                    r = 1e-6
                
                Ex[i] = k * dm_dt * cross_x / (r**3)
                Ey[i] = k * dm_dt * cross_y / (r**3)
                Ez[i] = k * dm_dt * cross_z / (r**3)
    
    def calculate_electric_field_optimized(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, 
                                          v1: np.ndarray, v2: np.ndarray, k: float, dm_dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        优化的电场计算
        
        Args:
            x, y, z: 空间坐标
            v1, v2: 速度矢量
            k: 比例常数
            dm_dt: 质量变化率
        
        Returns:
            Ex, Ey, Ez: 电场分量
        """
        Ex = np.zeros_like(x)
        Ey = np.zeros_like(y)
        Ez = np.zeros_like(z)
        
        if NUMBA_AVAILABLE:
            FieldCalculator._electric_field_kernel(
                x, y, z,
                v1[0], v1[1], v1[2],
                v2[0], v2[1], v2[2],
                k, dm_dt,
                Ex, Ey, Ez
            )
        else:
            return self.calculate_electric_field_regular(x, y, z, v1, v2, k, dm_dt)
        
        return Ex, Ey, Ez
    
    def calculate_electric_field_vectorized(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, 
                                           v1: np.ndarray, v2: np.ndarray, k: float, dm_dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        向量化的电场计算
        
        Args:
            x, y, z: 空间坐标
            v1, v2: 速度矢量
            k: 比例常数
            dm_dt: 质量变化率
        
        Returns:
            Ex, Ey, Ez: 电场分量
        """
        # 计算距离
        r = np.sqrt(x**2 + y**2 + z**2)
        r_safe = np.maximum(r, 1e-6)
        
        # 计算叉积 V1 × V2
        cross_x = v1[1] * v2[2] - v1[2] * v2[1]
        cross_y = v1[2] * v2[0] - v1[0] * v2[2]
        cross_z = v1[0] * v2[1] - v1[1] * v2[0]
        
        # 计算电场分量
        Ex = k * dm_dt * cross_x / (r_safe**3)
        Ey = k * dm_dt * cross_y / (r_safe**3)
        Ez = k * dm_dt * cross_z / (r_safe**3)
        
        return Ex, Ey, Ez


# 自适应采样算法
class AdaptiveSampler:
    """
    自适应采样算法类
    """
    
    @staticmethod
    def uniform_sampling(domain: Tuple[float, float], samples: int) -> np.ndarray:
        """
        均匀采样
        
        Args:
            domain: 采样域 [min, max]
            samples: 采样点数量
        
        Returns:
            采样点数组
        """
        return np.linspace(domain[0], domain[1], samples)
    
    @staticmethod
    def adaptive_sampling(func: Callable, domain: Tuple[float, float], 
                         error_threshold: float = 1e-6, 
                         max_samples: int = 10000) -> np.ndarray:
        """
        自适应采样算法
        
        Args:
            func: 要采样的函数
            domain: 采样域 [min, max]
            error_threshold: 误差阈值
            max_samples: 最大采样点数量
        
        Returns:
            自适应采样点数组
        """
        # 初始均匀采样
        x = np.linspace(domain[0], domain[1], 100)
        y = func(x)
        
        samples = list(x)
        values = list(y)
        
        # 迭代细化采样
        for _ in range(10):  # 最多迭代10次
            if len(samples) >= max_samples:
                break
            
            new_samples = []
            new_values = []
            
            # 检查相邻点之间的误差
            for i in range(len(samples) - 1):
                x1, x2 = samples[i], samples[i+1]
                y1, y2 = values[i], values[i+1]
                
                # 计算中点
                x_mid = (x1 + x2) / 2
                y_mid = func(x_mid)
                
                # 线性插值估计
                y_interp = (y1 + y2) / 2
                
                # 计算误差
                error = abs(y_mid - y_interp)
                
                if error > error_threshold:
                    new_samples.append(x_mid)
                    new_values.append(y_mid)
            
            if not new_samples:
                break
            
            # 合并并排序采样点
            all_samples = samples + new_samples
            all_values = values + new_values
            
            # 排序
            sorted_indices = np.argsort(all_samples)
            samples = [all_samples[i] for i in sorted_indices]
            values = [all_values[i] for i in sorted_indices]
        
        return np.array(samples)
    
    @staticmethod
    def fast_adaptive_sampling(func: Callable, domain: Tuple[float, float], 
                              error_threshold: float = 1e-6, 
                              max_samples: int = 10000) -> np.ndarray:
        """
        快速自适应采样算法
        
        Args:
            func: 要采样的函数
            domain: 采样域 [min, max]
            error_threshold: 误差阈值
            max_samples: 最大采样点数量
        
        Returns:
            自适应采样点数组
        """
        # 使用NumPy向量化操作加速
        def sample_func(x):
            if isinstance(x, (list, tuple)):
                x = np.array(x)
            return np.array([func(xi) for xi in x])
        
        # 初始采样
        x = np.linspace(domain[0], domain[1], 50)
        y = sample_func(x)
        
        for _ in range(8):  # 减少迭代次数提高速度
            if len(x) >= max_samples:
                break
            
            # 计算相邻点之间的误差
            dy = np.abs(np.diff(y))
            max_error_indices = np.where(dy > error_threshold)[0]
            
            if len(max_error_indices) == 0:
                break
            
            # 在误差大的区域插入新采样点
            new_x = []
            for i in max_error_indices:
                x_mid = (x[i] + x[i+1]) / 2
                new_x.append(x_mid)
            
            if new_x:
                new_x = np.array(new_x)
                new_y = sample_func(new_x)
                
                # 合并并排序
                all_x = np.concatenate([x, new_x])
                all_y = np.concatenate([y, new_y])
                
                sorted_indices = np.argsort(all_x)
                x = all_x[sorted_indices]
                y = all_y[sorted_indices]
        
        return x
    
    @staticmethod
    def parallel_adaptive_sampling(func: Callable, domain: Tuple[float, float], 
                                  error_threshold: float = 1e-6, 
                                  max_samples: int = 10000) -> np.ndarray:
        """
        并行自适应采样算法
        
        Args:
            func: 要采样的函数
            domain: 采样域 [min, max]
            error_threshold: 误差阈值
            max_samples: 最大采样点数量
        
        Returns:
            自适应采样点数组
        """
        try:
            from concurrent.futures import ThreadPoolExecutor
            
            def parallel_eval(x_points):
                with ThreadPoolExecutor() as executor:
                    return np.array(list(executor.map(func, x_points)))
            
            # 初始采样
            x = np.linspace(domain[0], domain[1], 100)
            y = parallel_eval(x)
            
            for _ in range(10):
                if len(x) >= max_samples:
                    break
                
                # 计算相邻点之间的误差
                dy = np.abs(np.diff(y))
                error_positions = np.where(dy > error_threshold)[0]
                
                if len(error_positions) == 0:
                    break
                
                # 生成新的采样点
                new_x = []
                for i in error_positions:
                    new_x.extend([
                        (x[i] + x[i+1])/2,
                        (x[i] + 3*x[i+1])/4,
                        (3*x[i] + x[i+1])/4
                    ])
                
                # 去重
                new_x = np.unique(new_x)
                new_y = parallel_eval(new_x)
                
                # 合并并排序
                all_x = np.concatenate([x, new_x])
                all_y = np.concatenate([y, new_y])
                
                sorted_indices = np.argsort(all_x)
                x = all_x[sorted_indices]
                y = all_y[sorted_indices]
            
            return x
        except ImportError:
            # 回退到常规自适应采样
            return AdaptiveSampler.adaptive_sampling(func, domain, error_threshold, max_samples)
    
    @staticmethod
    def multi_resolution_sampling(func: Callable, domain: Tuple[float, float], 
                                 levels: int = 3) -> np.ndarray:
        """
        多分辨率采样算法
        
        Args:
            func: 要采样的函数
            domain: 采样域 [min, max]
            levels: 分辨率级别
        
        Returns:
            多分辨率采样点数组
        """
        samples = []
        
        for level in range(levels):
            # 每个级别增加采样密度
            n_samples = 20 * (2 ** level)
            x = np.linspace(domain[0], domain[1], n_samples)
            samples.extend(x)
        
        # 去重并排序
        samples = np.unique(samples)
        return np.sort(samples)


# GPU加速计算（如果可用）
class GPUAccelerator:
    """
    GPU加速计算类
    """
    
    def __init__(self):
        self.available = CUPY_AVAILABLE
        self.device = None
        if self.available:
            self.device = cp.cuda.Device(0)
            print(f"GPU available: {self.device.name()}")
    
    def to_gpu(self, data: Union[np.ndarray, list]) -> any:
        """
        将数据移至GPU
        
        Args:
            data: 输入数据
        
        Returns:
            GPU上的数据
        """
        if not self.available:
            return data
        return cp.asarray(data)
    
    def to_cpu(self, data: any) -> np.ndarray:
        """
        将数据移至CPU
        
        Args:
            data: GPU上的数据
        
        Returns:
            CPU上的numpy数组
        """
        if not self.available:
            return data
        return cp.asnumpy(data)
    
    def gpu_available(self) -> bool:
        """
        检查GPU是否可用
        
        Returns:
            GPU是否可用
        """
        return self.available
    
    def run_on_gpu(self, func: Callable, *args, **kwargs) -> any:
        """
        在GPU上运行函数
        
        Args:
            func: 要运行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        
        Returns:
            函数运行结果
        """
        if not self.available:
            return func(*args, **kwargs)
        
        # 将参数移至GPU
        gpu_args = []
        for arg in args:
            if isinstance(arg, np.ndarray):
                gpu_args.append(self.to_gpu(arg))
            else:
                gpu_args.append(arg)
        
        # 运行函数
        result = func(*gpu_args, **kwargs)
        
        # 将结果移回CPU
        if isinstance(result, (tuple, list)):
            return [self.to_cpu(item) if hasattr(item, 'get') else item for item in result]
        elif hasattr(result, 'get'):
            return self.to_cpu(result)
        else:
            return result


# 高性能算法优化模块测试
if __name__ == "__main__":
    print("高性能算法优化模块测试")
    print("=" * 60)
    
    # 初始化
    calculator = HighPerformanceCalculator()
    optimizer = NumericalOptimizer()
    field_calc = FieldCalculator()
    sampler = AdaptiveSampler()
    gpu_accel = GPUAccelerator()
    
    # 测试数值计算性能
    print("\n1. 数值计算性能测试")
    print("-" * 40)
    
    # 创建测试数据
    large_array = np.random.rand(1000000)
    
    # 比较不同计算方法
    funcs = [
        optimizer.regular_calculation,
        optimizer.numpy_vectorized
    ]
    
    if NUMBA_AVAILABLE:
        funcs.append(optimizer.numba_optimized)
    
    if CUPY_AVAILABLE:
        funcs.append(optimizer.gpu_optimized)
    
    performance_results = calculator.compare_performance(funcs, large_array)
    
    for i, result in enumerate(performance_results):
        print(f"  {i+1}. {result['function']}: {result['execution_time']:.6f}s", end='')
        speedup = result.get('speedup')
        if speedup is not None and speedup != 0:
            try:
                print(f" (Speedup: {speedup:.2f}x)")
            except Exception:
                print(f" (Speedup: {speedup}x)")
        else:
            print()
    
    # 测试场计算性能
    print("\n2. 电场计算性能测试")
    print("-" * 40)
    
    # 创建测试数据
    n_points = 100000
    x = np.random.rand(n_points) * 10 - 5
    y = np.random.rand(n_points) * 10 - 5
    z = np.random.rand(n_points) * 10 - 5
    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])
    k = 1.0
    dm_dt = 0.5
    
    # 测试不同电场计算方法
    field_funcs = [
        field_calc.calculate_electric_field_regular,
        field_calc.calculate_electric_field_vectorized
    ]
    
    if NUMBA_AVAILABLE:
        field_funcs.append(field_calc.calculate_electric_field_optimized)
    
    field_results = calculator.compare_performance(
        field_funcs, x, y, z, v1, v2, k, dm_dt
    )
    
    for i, result in enumerate(field_results):
        print(f"  {i+1}. {result['function']}: {result['execution_time']:.6f}s", end='')
        speedup = result.get('speedup')
        if speedup is not None and speedup != 0:
            try:
                print(f" (Speedup: {speedup:.2f}x)")
            except Exception:
                print(f" (Speedup: {speedup}x)")
        else:
            print()
    
    # 测试自适应采样
    print("\n3. 自适应采样测试")
    print("-" * 40)
    
    # 测试函数
    def test_function(x):
        return np.sin(10*x) + np.cos(5*x)
    
    # 均匀采样
    uniform_samples = sampler.uniform_sampling([0, 2*np.pi], 100)
    print(f"  均匀采样: {len(uniform_samples)} 个点")
    
    # 自适应采样
    adaptive_samples = sampler.adaptive_sampling(test_function, [0, 2*np.pi], 1e-3)
    print(f"  自适应采样: {len(adaptive_samples)} 个点")
    print(f"  采样效率提升: {len(uniform_samples)/len(adaptive_samples):.2f}x")
    
    # 测试高级采样
    print("\n4. 高级采样测试")
    print("-" * 40)
    
    # 测试快速采样
    fast_samples = sampler.fast_adaptive_sampling(test_function, [0, 2*np.pi], 1e-3)
    print(f"  快速自适应采样: {len(fast_samples)} 个点")
    
    # 测试并行采样
    parallel_samples = sampler.parallel_adaptive_sampling(test_function, [0, 2*np.pi], 1e-3)
    print(f"  并行自适应采样: {len(parallel_samples)} 个点")
    
    # 测试多分辨率采样
    multi_res_samples = sampler.multi_resolution_sampling(test_function, [0, 2*np.pi], 3)
    print(f"  多分辨率采样: {len(multi_res_samples)} 个点")
    
    # 测试FFT优化
    print("\n5. FFT优化测试")
    print("-" * 40)
    
    # 创建测试信号
    t = np.linspace(0, 10, 1000000)
    signal = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*10*t) + np.sin(2*np.pi*15*t)
    
    # 测试FFT优化
    if hasattr(optimizer, 'fft_optimized'):
        fft_result = optimizer.fft_optimized(signal)
        print(f"  FFT优化: 成功处理信号，频率分量数量: {len(fft_result)}")
    
    # 打印性能统计
    print("\n6. 性能统计")
    print("-" * 40)
    stats = calculator.get_performance_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n高性能算法优化模块测试完成！")
    print("=" * 60)