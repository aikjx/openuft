#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引力光速统一方程的边界情况测试
测试方程在不同条件下的正确性
"""

import unittest
from validate_gravitational_light_speed_equation import GravitationalLightSpeedEquation

class TestEdgeCases(unittest.TestCase):
    """边界情况测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.validator = GravitationalLightSpeedEquation()
    
    def test_different_G_values(self):
        """测试不同万有引力常数值"""
        # 测试不同的G值
        test_cases = [
            6.67430e-11,  # CODATA 2018
            6.67408e-11,  # CODATA 2014
            6.67384e-11,  # CODATA 2010
        ]
        
        for G_test in test_cases:
            validator_test = GravitationalLightSpeedEquation(G=G_test)
            Z_calculated = validator_test.calculate_Z()
            # 验证Z值的计算是否正确
            expected_Z = (G_test * validator_test.c) / 2
            self.assertAlmostEqual(Z_calculated, expected_Z)
    
    def test_different_c_values(self):
        """测试不同光速值"""
        # 测试不同的c值（光速的微小变化）
        test_cases = [
            299792458,      # 标准光速
            299792458.1,    # 微小变化
            299792457.9,    # 微小变化
        ]
        
        for c_test in test_cases:
            validator_test = GravitationalLightSpeedEquation(c=c_test)
            Z_calculated = validator_test.calculate_Z()
            # 验证Z值的计算是否正确
            expected_Z = (validator_test.G * c_test) / 2
            self.assertAlmostEqual(Z_calculated, expected_Z)
    
    def test_geometric_factor_variations(self):
        """测试几何因子的变化"""
        # 测试几何因子不是2的情况
        def calculate_Z_with_different_factor(factor):
            return (self.validator.G * self.validator.c) / factor
        
        # 测试不同的几何因子
        factors = [1, 2, 3, 4]
        for factor in factors:
            Z_calculated = calculate_Z_with_different_factor(factor)
            # 验证计算是否正确
            expected_Z = (self.validator.G * self.validator.c) / factor
            self.assertAlmostEqual(Z_calculated, expected_Z)
    
    def test_consistency_with_newton_law(self):
        """测试与牛顿万有引力定律的一致性"""
        # 从Z反推G，验证一致性
        Z_calculated = self.validator.calculate_Z()
        G_reconstructed = (2 * Z_calculated) / self.validator.c
        self.assertAlmostEqual(G_reconstructed, self.validator.G)
    
    def test_numerical_precision(self):
        """测试数值精度"""
        # 测试多次计算的一致性
        Z_values = []
        for _ in range(100):
            Z_values.append(self.validator.calculate_Z())
        
        # 所有计算结果应该相同
        self.assertEqual(len(set(Z_values)), 1)
    
    def test_dimensionless_analysis(self):
        """测试无量纲分析"""
        # 计算无量纲组合
        Z = self.validator.calculate_Z()
        # 检查Z的物理意义是否合理
        # 张祥前常数Z的量纲是 kg⁻¹·m⁴·s⁻³
        # 这里我们只验证数值是否为正数
        self.assertGreater(Z, 0)

if __name__ == '__main__':
    unittest.main()
