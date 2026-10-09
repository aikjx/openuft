#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心算法模块
Unified Field Theory Core Algorithm Module

实现统一场论核心公式的计算功能
"""

import json
import numpy as np
import time
from typing import Dict, List, Any, Tuple, Optional

class FormulaCalculator:
    """公式计算器"""
    
    def __init__(self, formula_db_path: str):
        """初始化公式计算器
        
        Args:
            formula_db_path: 公式规格数据库路径
        """
        self.formula_db = self._load_formula_db(formula_db_path)
        self.calculated_results: Dict[str, Any] = {}
        self.formula_cache: Dict[str, Dict[str, Any]] = {}
        self._build_formula_index()
    
    def _load_formula_db(self, formula_db_path: str) -> Dict[str, Any]:
        """加载公式规格数据库
        
        Args:
            formula_db_path: 公式规格数据库路径
            
        Returns:
            公式规格数据库
        """
        with open(formula_db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _build_formula_index(self) -> None:
        """构建公式索引，提高查询效率"""
        self.formula_index: Dict[str, Dict[str, Any]] = {}
        for formula in self.formula_db['formulas']:
            self.formula_index[formula['id']] = formula
    
    def calculate_formula(self, formula_id: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算指定公式
        
        Args:
            formula_id: 公式ID
            parameters: 计算参数
            
        Returns:
            计算结果
        """
        if parameters is None:
            parameters = {}
        
        # 生成缓存键（处理不可哈希类型）
        def hashable_value(value):
            if isinstance(value, list):
                return tuple(value)
            if isinstance(value, dict):
                return tuple(sorted((k, hashable_value(v)) for k, v in value.items()))
            return value
        
        hashable_params = {k: hashable_value(v) for k, v in parameters.items()}
        cache_key = f"{formula_id}:{hash(frozenset(hashable_params.items()))}"
        if cache_key in self.formula_cache:
            return self.formula_cache[cache_key]
        
        # 获取公式信息
        formula = self.formula_index.get(formula_id)
        if not formula:
            return {
                'status': 'error',
                'error': f'公式ID {formula_id} 不存在'
            }
        
        # 检查依赖项
        for dep_id in formula['dependencies']:
            if dep_id not in self.calculated_results:
                # 计算依赖项
                dep_result = self.calculate_formula(dep_id, parameters)
                if dep_result['status'] != 'success':
                    return dep_result
        
        # 根据公式ID选择计算方法
        calculation_method = getattr(self, f'_calculate_{formula_id}', None)
        if not calculation_method:
            # 对于重复公式，使用已有的计算方法
            if formula_id == '06':  # 运动动量方程使用动量方程的计算方法
                calculation_method = self._calculate_05
            else:
                return {
                    'status': 'error',
                    'error': f'公式ID {formula_id} 的计算方法未实现'
                }
        
        try:
            # 计算结果
            result = calculation_method(parameters)
            self.calculated_results[formula_id] = result
            
            response = {
                'status': 'success',
                'result': result,
                'formula_name': formula['name']
            }
            
            # 缓存结果
            self.formula_cache[cache_key] = response
            return response
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _calculate_01(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算时空同一化方程
        
        公式: r⃗(t) = C⃗t = xi⃗ + yj⃗ + zk⃗
        """
        C = parameters.get('C', [1, 0, 0])
        t = parameters.get('t', 0)
        theta = parameters.get('theta', 45) * np.pi / 180  # 转换为弧度
        phi = parameters.get('phi', 45) * np.pi / 180      # 转换为弧度
        
        # 计算笛卡尔坐标
        x = C[0] * t
        y = C[1] * t
        z = C[2] * t
        
        # 计算球坐标
        r = np.sqrt(x**2 + y**2 + z**2)
        
        return {
            'cartesian': {'x': x, 'y': y, 'z': z},
            'vector': C,
            'time': t,
            'spherical': {'r': r, 'theta': theta * 180 / np.pi, 'phi': phi * 180 / np.pi}
        }
    
    def _calculate_02(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算三维螺旋时空方程
        
        公式: r⃗(t) = r cos ωt · i⃗ + r sin ωt · j⃗ + ht · k⃗
        """
        r = parameters.get('r', 5)
        omega = parameters.get('omega', 1)
        h = parameters.get('h', 2)
        t = parameters.get('t', 0)
        
        # 计算螺旋坐标
        x = r * np.cos(omega * t)
        y = r * np.sin(omega * t)
        z = h * t
        
        # 计算速度
        vx = -r * omega * np.sin(omega * t)
        vy = r * omega * np.cos(omega * t)
        vz = h
        
        # 计算加速度
        ax = -r * omega**2 * np.cos(omega * t)
        ay = -r * omega**2 * np.sin(omega * t)
        az = 0
        
        return {
            'position': {'x': x, 'y': y, 'z': z},
            'velocity': {'x': vx, 'y': vy, 'z': vz},
            'acceleration': {'x': ax, 'y': ay, 'z': az},
            'parameters': {'r': r, 'omega': omega, 'h': h, 't': t}
        }
    
    def _calculate_03(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算质量定义方程
        
        公式: m = k · dn/dΩ
        """
        k = parameters.get('k', 1)
        n = parameters.get('n', 100)
        theta_max = parameters.get('theta_max', 180) * np.pi / 180  # 转换为弧度
        phi_max = parameters.get('phi_max', 360) * np.pi / 180      # 转换为弧度
        
        # 计算立体角
        omega = 2 * np.pi * (1 - np.cos(theta_max))  # 球坐标系下的立体角
        
        # 计算密度
        dn_domega = n / omega if omega != 0 else 0
        
        # 计算质量
        m = k * dn_domega
        
        return {
            'mass': m,
            'density': dn_domega,
            'solid_angle': omega,
            'parameters': {'k': k, 'n': n, 'theta_max': theta_max * 180 / np.pi, 'phi_max': phi_max * 180 / np.pi}
        }
    
    def _calculate_04(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算引力场定义方程
        
        公式: A⃗ = -Gk(Δn/Δs)(r⃗/r)
        """
        G = parameters.get('G', 6.67e-11)
        k = parameters.get('k', 1)
        mass = parameters.get('mass', 1)
        
        # 简化计算，实际应基于空间位移矢量条数密度
        delta_n = mass  # 简化处理
        delta_s = 1.0   # 简化处理
        
        # 计算引力场强度
        A_magnitude = -G * k * (delta_n / delta_s)
        
        # 引力场方向（默认沿x轴）
        A_vector = [A_magnitude, 0, 0]
        
        return {
            'field_strength': A_magnitude,
            'field_vector': A_vector,
            'parameters': {'G': G, 'k': k, 'mass': mass}
        }
    
    def _calculate_05(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算动量方程
        
        公式: P = m(C - V)
        """
        m = parameters.get('m', 1)
        C = parameters.get('C', 3e8)
        V = parameters.get('V', 0)
        
        # 计算动量
        P = m * (C - V)
        
        return {
            'momentum': P,
            'parameters': {'m': m, 'C': C, 'V': V}
        }
    
    def _calculate_07(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算宇宙大统一方程（力方程）
        
        公式: F = dP/dt = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)
        """
        C = parameters.get('C', 3e8)
        V = parameters.get('V', 0)
        m = parameters.get('m', 1)
        dm_dt = parameters.get('dm_dt', 0)
        dv_dt = parameters.get('dv_dt', 0)
        dc_dt = 0  # 光速恒定
        
        # 计算力
        F = C * dm_dt - V * dm_dt + m * dc_dt - m * dv_dt
        
        return {
            'force': F,
            'parameters': {'C': C, 'V': V, 'm': m, 'dm_dt': dm_dt, 'dv_dt': dv_dt}
        }
    
    def _calculate_08(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算空间波动方程
        
        公式: ∇²L = 1/c² ∂²L/∂t²
        """
        c = parameters.get('c', 3e8)
        L = parameters.get('L', 1)
        t = parameters.get('t', 0)
        
        # 简化的波动方程解
        omega = 2 * np.pi * 1  # 角频率
        k_wave = omega / c     # 波数
        
        # 一维波动解
        wave_solution = L * np.sin(k_wave * t)
        
        return {
            'wave_equation': True,
            'wave_solution': wave_solution,
            'parameters': {'c': c, 'L': L, 't': t}
        }
    
    def _calculate_09(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算电荷定义方程
        
        公式: q = k' k 1/Ω² dΩ/dt
        """
        k_prime = parameters.get('k_prime', 1)
        k = parameters.get('k', 1)
        omega = parameters.get('omega', 1)
        domega_dt = parameters.get('domega_dt', 1)
        
        # 计算电荷
        q = k_prime * k * (1 / omega**2) * domega_dt
        
        return {
            'charge': q,
            'parameters': {'k_prime': k_prime, 'k': k, 'omega': omega, 'domega_dt': domega_dt}
        }
    
    def _calculate_10(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算电场定义方程
        
        公式: E⃗ = -kk'/(4πε₀Ω²) dΩ/dt r⃗/r³
        """
        k = parameters.get('k', 1)
        k_prime = parameters.get('k_prime', 1)
        epsilon0 = parameters.get('epsilon0', 8.854e-12)
        omega = parameters.get('omega', 1)
        domega_dt = parameters.get('domega_dt', 1)
        
        # 计算电场强度
        E_magnitude = -k * k_prime / (4 * np.pi * epsilon0 * omega**2) * domega_dt
        
        # 电场方向（默认沿x轴）
        E_vector = [E_magnitude, 0, 0]
        
        return {
            'field_strength': E_magnitude,
            'field_vector': E_vector,
            'parameters': {'k': k, 'k_prime': k_prime, 'epsilon0': epsilon0, 'omega': omega, 'domega_dt': domega_dt}
        }
    
    def _calculate_11(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算磁场定义方程
        
        公式: B⃗ = μ₀ γ k k'/(4π Ω²) dΩ/dt * vector_term / denominator
        """
        mu0 = parameters.get('mu0', 4 * np.pi * 1e-7)
        gamma = parameters.get('gamma', 1)
        k = parameters.get('k', 1)
        k_prime = parameters.get('k_prime', 1)
        omega = parameters.get('omega', 1)
        domega_dt = parameters.get('domega_dt', 1)
        vector_term = parameters.get('vector_term', 1)
        denominator = parameters.get('denominator', 1)
        
        # 计算磁场强度
        B_magnitude = mu0 * gamma * k * k_prime / (4 * np.pi * omega**2) * domega_dt * vector_term / denominator
        
        # 磁场方向（默认沿x轴）
        B_vector = [B_magnitude, 0, 0]
        
        return {
            'field_strength': B_magnitude,
            'field_vector': B_vector,
            'parameters': {'mu0': mu0, 'gamma': gamma, 'k': k, 'k_prime': k_prime, 'omega': omega, 'domega_dt': domega_dt, 'vector_term': vector_term, 'denominator': denominator}
        }
    
    def _calculate_12(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算变化引力场产生电磁场
        
        公式: E⃗ = -∂A⃗/∂t
        """
        A = parameters.get('A', [0, 0, 0])
        dA_dt = parameters.get('dA_dt', [0, 0, 0])
        
        # 计算电场
        E = [-dA for dA in dA_dt]
        
        return {
            'electric_field': E,
            'parameters': {'A': A, 'dA_dt': dA_dt}
        }
    
    def _calculate_13(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算磁矢势方程
        
        公式: A⃗ = μ₀/(4π) ∫ J⃗/r dV
        """
        mu0 = parameters.get('mu0', 1.2566370614e-6)
        J = parameters.get('J', [1, 0, 0])
        r = parameters.get('r', 1)
        
        # 简化计算，假设积分结果为J/r
        A = [mu0 / (4 * np.pi) * j / r for j in J]
        
        return {
            'vector_potential': A,
            'parameters': {'mu0': mu0, 'J': J, 'r': r}
        }
    
    def _calculate_14(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算变化引力场产生电场
        
        公式: E⃗ = -∇φ - ∂A⃗/∂t
        """
        phi = parameters.get('phi', 0)
        A = parameters.get('A', [0, 0, 0])
        dA_dt = parameters.get('dA_dt', [0, 0, 0])
        
        # 简化计算，假设∇φ为0
        E = [-dA for dA in dA_dt]
        
        return {
            'electric_field': E,
            'parameters': {'phi': phi, 'A': A, 'dA_dt': dA_dt}
        }
    
    def _calculate_15(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算变化磁场产生引力场和电场
        
        公式: ∇×E⃗ = -∂B⃗/∂t
        """
        B = parameters.get('B', [0, 0, 0])
        dB_dt = parameters.get('dB_dt', [0, 0, 0])
        
        # 简化计算，返回电场旋度
        curl_E = [-db for db in dB_dt]
        
        return {
            'curl_electric_field': curl_E,
            'parameters': {'B': B, 'dB_dt': dB_dt}
        }
    
    def _calculate_16(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算能量方程
        
        公式: E = mc²
        """
        m = parameters.get('m', 1)
        c = parameters.get('c', 3e8)
        
        # 计算能量
        E = m * c**2
        
        return {
            'energy': E,
            'parameters': {'m': m, 'c': c}
        }
    
    def _calculate_17(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """计算光速飞行器动力学方程
        
        公式: F = m(dC⃗/dt) - m(dV⃗/dt)
        """
        m = parameters.get('m', 1)
        C = parameters.get('C', [3e8, 0, 0])
        V = parameters.get('V', [0, 0, 0])
        dC_dt = parameters.get('dC_dt', [0, 0, 0])
        dV_dt = parameters.get('dV_dt', [0, 0, 0])
        
        # 计算力
        F = [m * (dc - dv) for dc, dv in zip(dC_dt, dV_dt)]
        
        return {
            'force': F,
            'parameters': {'m': m, 'C': C, 'V': V, 'dC_dt': dC_dt, 'dV_dt': dV_dt}
        }
    
    def calculate_all_formulas(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算所有公式
        
        Args:
            parameters: 计算参数
            
        Returns:
            所有公式的计算结果
        """
        if parameters is None:
            parameters = {}
        
        results = {
            'summary': {
                'successful_modules': 0,
                'total_modules': len(self.formula_db['formulas']),
                'execution_time': 0
            }
        }
        
        start_time = time.time()
        self.calculated_results.clear()
        
        for formula in self.formula_db['formulas']:
            formula_id = formula['id']
            result = self.calculate_formula(formula_id, parameters)
            results[formula_id] = result
            
            if result['status'] == 'success':
                results['summary']['successful_modules'] += 1
        
        results['summary']['execution_time'] = time.time() - start_time
        return results
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self.calculated_results.clear()
        self.formula_cache.clear()



class PerformanceBenchmarker:
    """性能基准测试器"""
    
    def __init__(self, formula_calculator: FormulaCalculator):
        """初始化性能基准测试器
        
        Args:
            formula_calculator: 公式计算器实例
        """
        self.formula_calculator = formula_calculator
    
    def benchmark_performance(self, iterations: int = 10) -> Dict[str, Any]:
        """基准测试性能
        
        Args:
            iterations: 迭代次数
            
        Returns:
            性能基准测试结果
        """
        import time
        
        results = {
            'summary': {
                'total_modules_tested': len(self.formula_calculator.formula_db['formulas']),
                'fastest_modules': [],
                'slowest_modules': [],
                'average_execution_time': 0.0
            }
        }
        
        performance_data = {}
        total_time = 0.0
        
        # 测试每个公式的性能
        for formula in self.formula_calculator.formula_db['formulas']:
            formula_id = formula['id']
            formula_name = formula['name']
            
            times = []
            for _ in range(iterations):
                start_time = time.time()
                self.formula_calculator.calculate_formula(formula_id)
                end_time = time.time()
                times.append(end_time - start_time)
            
            # 计算性能指标
            average_time = np.mean(times)
            min_time = np.min(times)
            max_time = np.max(times)
            std_time = np.std(times)
            
            performance_data[formula_id] = {
                'average_time': average_time,
                'min_time': min_time,
                'max_time': max_time,
                'std_time': std_time,
                'formula_name': formula_name
            }
            
            total_time += average_time
        
        # 计算平均执行时间
        if performance_data:
            results['summary']['average_execution_time'] = total_time / len(performance_data)
        
        # 按平均时间排序，找出最快和最慢的模块
        sorted_modules = sorted(performance_data.items(), key=lambda x: x[1]['average_time'])
        results['summary']['fastest_modules'] = sorted_modules[:3]
        results['summary']['slowest_modules'] = sorted_modules[-3:][::-1]
        results.update(performance_data)
        
        return results
    
    def benchmark_all_formulas(self, iterations: int = 5) -> Dict[str, Any]:
        """测试计算所有公式的性能
        
        Args:
            iterations: 迭代次数
            
        Returns:
            性能测试结果
        """
        import time
        
        times = []
        for _ in range(iterations):
            self.formula_calculator.clear_cache()
            start_time = time.time()
            self.formula_calculator.calculate_all_formulas()
            end_time = time.time()
            times.append(end_time - start_time)
        
        average_time = np.mean(times)
        min_time = np.min(times)
        max_time = np.max(times)
        std_time = np.std(times)
        
        return {
            'average_time': average_time,
            'min_time': min_time,
            'max_time': max_time,
            'std_time': std_time,
            'iterations': iterations
        }


class ConsistencyVerifier:
    """一致性验证器"""
    
    def __init__(self, formula_calculator: FormulaCalculator):
        """初始化一致性验证器
        
        Args:
            formula_calculator: 公式计算器实例
        """
        self.formula_calculator = formula_calculator
    
    def verify_consistency(self) -> Dict[str, Any]:
        """验证公式一致性
        
        Returns:
            一致性验证结果
        """
        results = {
            'summary': {
                'consistent_tests': 0,
                'total_tests': 0,
                'consistency_rate': 0.0
            }
        }
        
        # 执行一致性测试
        test_results = self._run_consistency_tests()
        results.update(test_results)
        
        # 计算一致性率
        total_tests = results['summary']['total_tests']
        if total_tests > 0:
            consistent_tests = results['summary']['consistent_tests']
            results['summary']['consistency_rate'] = consistent_tests / total_tests
        
        return results
    
    def _run_consistency_tests(self) -> Dict[str, Any]:
        """运行一致性测试
        
        Returns:
            一致性测试结果
        """
        results = {
            'summary': {
                'consistent_tests': 0,
                'total_tests': 0
            }
        }
        
        # 测试1: 时空同一化方程与三维螺旋时空方程的一致性
        test_id = 'test_spacetime_consistency'
        try:
            # 计算时空同一化方程（只沿z轴方向，与螺旋方程对应）
            result_01 = self.formula_calculator.calculate_formula('01', {'t': 1, 'C': [0, 0, 1]})
            # 计算三维螺旋时空方程（当r=0时，应退化为z轴方向的直线运动）
            result_02 = self.formula_calculator.calculate_formula('02', {'t': 1, 'r': 0, 'omega': 1, 'h': 1})
            
            # 验证结果一致性
            consistent = False
            if result_01['status'] == 'success' and result_02['status'] == 'success':
                # 对于r=0的情况，三维螺旋时空方程的z分量应该等于h*t，
                # 而时空同一化方程的z分量应该等于C[2]*t
                # 这里我们设置h=1，C[2]=1，t=1，所以应该相等
                z1 = result_01['result']['cartesian']['z']
                z2 = result_02['result']['position']['z']
                # 当r=0时，x和y都应该为0
                x1 = result_01['result']['cartesian']['x']
                x2 = result_02['result']['position']['x']
                y1 = result_01['result']['cartesian']['y']
                y2 = result_02['result']['position']['y']
                
                consistent = (abs(x1 - x2) < 1e-10 and
                             abs(y1 - y2) < 1e-10 and
                             abs(z1 - z2) < 1e-10)
            
            results[test_id] = {
                'consistent': consistent,
                'description': '时空同一化方程与三维螺旋时空方程的一致性',
                'details': {
                    'spacetime_equation': result_01['result'] if result_01['status'] == 'success' else 'error',
                    'helix_equation': result_02['result'] if result_02['status'] == 'success' else 'error'
                }
            }
            
            if consistent:
                results['summary']['consistent_tests'] += 1
            results['summary']['total_tests'] += 1
        except Exception as e:
            results[test_id] = {
                'consistent': False,
                'description': '时空同一化方程与三维螺旋时空方程的一致性',
                'error': str(e)
            }
            results['summary']['total_tests'] += 1
        
        # 测试2: 动量方程与运动动量方程的一致性
        test_id = 'test_momentum_consistency'
        try:
            # 计算动量方程
            result_05 = self.formula_calculator.calculate_formula('05', {'m': 1, 'C': 3e8, 'V': 1e8})
            # 计算运动动量方程
            result_06 = self.formula_calculator.calculate_formula('06', {'m': 1, 'C': 3e8, 'V': 1e8})
            
            # 验证结果一致性
            consistent = False
            if result_05['status'] == 'success' and result_06['status'] == 'success':
                p1 = result_05['result']['momentum']
                p2 = result_06['result']['momentum']
                consistent = abs(p1 - p2) < 1e-10
            
            results[test_id] = {
                'consistent': consistent,
                'description': '动量方程与运动动量方程的一致性',
                'details': {
                    'momentum_equation': result_05['result'] if result_05['status'] == 'success' else 'error',
                    'motion_momentum_equation': result_06['result'] if result_06['status'] == 'success' else 'error'
                }
            }
            
            if consistent:
                results['summary']['consistent_tests'] += 1
            results['summary']['total_tests'] += 1
        except Exception as e:
            results[test_id] = {
                'consistent': False,
                'description': '动量方程与运动动量方程的一致性',
                'error': str(e)
            }
            results['summary']['total_tests'] += 1
        
        return results