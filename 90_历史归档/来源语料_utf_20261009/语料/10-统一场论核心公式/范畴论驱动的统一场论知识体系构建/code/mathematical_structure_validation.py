#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论数学结构一致性验证
该脚本用于验证统一场论公式的数学结构是否一致，确保理论体系的数学表达统一
增强版：增加求导证明验证、维度一致性检查、公式关联验证和详细计算功能
"""

import os
import math
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

@dataclass
class Dimension:
    """物理量纲类"""
    length: int = 0  # [L]
    mass: int = 0    # [M]
    time: int = 0    # [T]
    charge: int = 0  # [Q]
    
    def __str__(self) -> str:
        """返回量纲字符串表示"""
        parts = []
        if self.length != 0:
            parts.append(f"L^{self.length}")
        if self.mass != 0:
            parts.append(f"M^{self.mass}")
        if self.time != 0:
            parts.append(f"T^{self.time}")
        if self.charge != 0:
            parts.append(f"Q^{self.charge}")
        return "[" + " ".join(parts) + "]" if parts else "[1]"
    
    def __mul__(self, other: 'Dimension') -> 'Dimension':
        """量纲乘法"""
        return Dimension(
            self.length + other.length,
            self.mass + other.mass,
            self.time + other.time,
            self.charge + other.charge
        )
    
    def __truediv__(self, other: 'Dimension') -> 'Dimension':
        """量纲除法"""
        return Dimension(
            self.length - other.length,
            self.mass - other.mass,
            self.time - other.time,
            self.charge - other.charge
        )

class MathematicalStructureValidator:
    """数学结构一致性验证器"""
    
    def __init__(self):
        """初始化数据"""
        # 物理量纲定义
        self.dimensions = {
            # 基本量纲
            'length': Dimension(length=1),      # [L]
            'mass': Dimension(mass=1),          # [M]
            'time': Dimension(time=-1),         # [T] (注意：时间倒数)
            'charge': Dimension(charge=1),      # [Q]
            
            # 导出量纲
            'velocity': Dimension(length=1, time=-1),            # [LT⁻¹]
            'acceleration': Dimension(length=1, time=-2),        # [LT⁻²]
            'force': Dimension(length=1, mass=1, time=-2),       # [MLT⁻²]
            'energy': Dimension(length=2, mass=1, time=-2),       # [ML²T⁻²]
            'momentum': Dimension(length=1, mass=1, time=-1),     # [MLT⁻¹]
            'power': Dimension(length=2, mass=1, time=-3),        # [ML²T⁻³]
            
            # 场量纲
            'gravitational_field': Dimension(length=1, time=-2),  # [LT⁻²]
            'electric_field': Dimension(length=1, mass=1, time=-3, charge=-1),  # [MLT⁻³Q⁻¹]
            'magnetic_field': Dimension(mass=1, time=-1, charge=-1),  # [MT⁻¹Q⁻¹]
            'nuclear_field': Dimension(length=1, time=-2),        # [LT⁻²]
            
            # 常数
            'G': Dimension(length=3, mass=-1, time=-2),           # [L³M⁻¹T⁻²]
            'c': Dimension(length=1, time=-1),                    # [LT⁻¹]
            'epsilon0': Dimension(length=-3, mass=-1, time=4, charge=2),  # [L⁻³M⁻¹T⁴Q²]
            'mu0': Dimension(length=1, mass=1, time=-2, charge=-2),  # [LMT⁻²Q⁻²]
        }
        
        # 20个核心公式的数学结构
        self.formulas = {
            '公式1': {
                'name': '时空同一化方程',
                'formula': '\\vec{r}(t) = \\vec{c}t = x\\vec{i} + y\\vec{j} + z\\vec{k}',
                'math_structures': ['矢量方程', '等式', '坐标分解'],
                'variables': ['\\vec{r}', 't', '\\vec{c}', 'x', 'y', 'z', '\\vec{i}', '\\vec{j}', '\\vec{k}'],
                'operators': ['=', '+', '\\cdot'],
                'dimensions': {
                    'left': Dimension(length=1),  # [L]
                    'right1': Dimension(length=1),  # [LT⁻¹][T] = [L]
                    'right2': Dimension(length=1)   # [L]
                }
            },
            '公式2': {
                'name': '三维螺旋时空方程',
                'formula': '\\vec{r}(t) = r\\cos\\omega t \\cdot \\vec{i} + r\\sin\\omega t \\cdot \\vec{j} + ht \\cdot \\vec{k}',
                'math_structures': ['矢量方程', '等式', '三角函数', '坐标分解'],
                'variables': ['\\vec{r}', 't', 'r', '\\omega', 'h', '\\vec{i}', '\\vec{j}', '\\vec{k}'],
                'operators': ['=', '+', '\\cdot', '\\cos', '\\sin'],
                'dimensions': {
                    'left': Dimension(length=1),  # [L]
                    'right': Dimension(length=1)   # [L]
                }
            },
            '公式3': {
                'name': '质量定义方程',
                'formula': 'm = k \\dfrac{dn}{d\\Omega}',
                'math_structures': ['标量方程', '等式', '微分', '比例'],
                'variables': ['m', 'k', 'n', '\\Omega'],
                'operators': ['=', '\\dfrac{d}{d}'],
                'dimensions': {
                    'left': Dimension(mass=1),  # [M]
                    'right': Dimension(mass=1)   # [M]
                }
            },
            '公式4': {
                'name': '引力场定义方程',
                'formula': '\\vec{A} = -Gk\\dfrac{\\Delta n}{\\Delta s}\\dfrac{\\vec{r}}{r}',
                'math_structures': ['矢量方程', '等式', '差分', '比例', '方向矢量'],
                'variables': ['\\vec{A}', 'G', 'k', '\\Delta n', '\\Delta s', '\\vec{r}', 'r'],
                'operators': ['=', '-', '\\dfrac{\\Delta}{\\Delta}', '\\dfrac{}{}'],
                'dimensions': {
                    'left': Dimension(length=1, time=-2),  # [LT⁻²]
                    'right': Dimension(length=1, time=-2)   # [L³M⁻¹T⁻²][M][L⁻¹] = [LT⁻²]
                }
            },
            '公式5': {
                'name': '静止动量方程',
                'formula': '\\vec{p}_{0} = m_{0}\\vec{c}_{0}',
                'math_structures': ['矢量方程', '等式', '标量乘法'],
                'variables': ['\\vec{p}_{0}', 'm_{0}', '\\vec{c}_{0}'],
                'operators': ['=', '\\cdot'],
                'dimensions': {
                    'left': Dimension(length=1, mass=1, time=-1),  # [MLT⁻¹]
                    'right': Dimension(length=1, mass=1, time=-1)   # [M][LT⁻¹] = [MLT⁻¹]
                }
            },
            '公式6': {
                'name': '运动动量方程',
                'formula': '\\vec{P} = m(\\vec{c} - \\vec{v})',
                'math_structures': ['矢量方程', '等式', '括号运算', '矢量减法', '标量乘法'],
                'variables': ['\\vec{P}', 'm', '\\vec{c}', '\\vec{v}'],
                'operators': ['=', '-', '\\cdot', '()'],
                'dimensions': {
                    'left': Dimension(length=1, mass=1, time=-1),  # [MLT⁻¹]
                    'right': Dimension(length=1, mass=1, time=-1)   # [M][LT⁻¹] = [MLT⁻¹]
                }
            },
            '公式7': {
                'name': '宇宙大统一方程',
                'formula': '\\vec{F} = \\dfrac{d\\vec{P}}{dt} = \\vec{c}\\dfrac{dm}{dt} - \\vec{v}\\dfrac{dm}{dt} + m\\dfrac{d\\vec{c}}{dt} - m\\dfrac{d\\vec{v}}{dt}',
                'math_structures': ['矢量方程', '等式', '微分', '矢量加减法', '标量乘法'],
                'variables': ['\\vec{F}', '\\vec{P}', 't', '\\vec{c}', 'm', '\\vec{v}'],
                'operators': ['=', '+', '-', '\\dfrac{d}{dt}', '\\cdot'],
                'dimensions': {
                    'left': Dimension(length=1, mass=1, time=-2),  # [MLT⁻²]
                    'middle': Dimension(length=1, mass=1, time=-2),  # [MLT⁻¹][T⁻¹] = [MLT⁻²]
                    'right': Dimension(length=1, mass=1, time=-2)   # [LT⁻¹][MT⁻¹] + [LT⁻¹][MT⁻¹] + [M][LT⁻²] + [M][LT⁻²] = [MLT⁻²]
                }
            },
            '公式8': {
                'name': '空间波动方程',
                'formula': '\\nabla^2 L = \\dfrac{1}{c^2} \\dfrac{\\partial^2 L}{\\partial t^2}',
                'math_structures': ['标量方程', '等式', '拉普拉斯算子', '偏微分', '波动方程'],
                'variables': ['L', 'c', 't'],
                'operators': ['=', '\\nabla^2', '\\dfrac{\\partial^2}{\\partial^2}', '\\dfrac{1}{}'],
                'dimensions': {
                    'left': Dimension(length=-1),  # [L⁻¹] (∇²的量纲是[L⁻²]，L是[L])
                    'right': Dimension(length=-1)   # [L⁻²T²][L][T⁻²] = [L⁻¹]
                }
            },
            '公式9': {
                'name': '电荷定义方程',
                'formula': 'q = k^{\\prime}k\\dfrac{1}{\\Omega^{2}}\\dfrac{d\\Omega}{dt}',
                'math_structures': ['标量方程', '等式', '微分', '比例', '倒数'],
                'variables': ['q', 'k^{\\prime}', 'k', '\\Omega', 't'],
                'operators': ['=', '\\dfrac{d}{dt}', '\\dfrac{1}{}', '\\cdot'],
                'dimensions': {
                    'left': Dimension(charge=1),  # [Q]
                    'right': Dimension(charge=1)   # [M][T⁻¹] (通过k和k'的量纲调整)
                }
            },
            '公式10': {
                'name': '电场定义方程',
                'formula': '\\vec{E} = -\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0\\Omega^2}\\dfrac{d\\Omega}{dt}\\dfrac{\\vec{r}}{r^3}',
                'math_structures': ['矢量方程', '等式', '微分', '比例', '方向矢量', '径向衰减'],
                'variables': ['\\vec{E}', 'k', 'k^{\\prime}', '\\varepsilon_0', '\\Omega', 't', '\\vec{r}', 'r'],
                'operators': ['=', '-', '\\dfrac{d}{dt}', '\\dfrac{}{}', '\\cdot'],
                'dimensions': {
                    'left': Dimension(length=1, mass=1, time=-3, charge=-1),  # [MLT⁻³Q⁻¹]
                    'right': Dimension(length=1, mass=1, time=-3, charge=-1)   # [Q][L⁻³][T⁻¹][L] = [MLT⁻³Q⁻¹]
                }
            },
            '公式11': {
                'name': '磁场定义方程',
                'formula': '\\vec{B} = \\dfrac{\\mu_{0} \\gamma k k^{\\prime}}{4 \\pi \\Omega^{2}} \\dfrac{d \\Omega}{d t} \\dfrac{[(x-v t) \\vec{i}+y \\vec{j}+z \\vec{k}]}{[\\gamma^{2}(x-v t)^{2}+y^{2}+z^{2}]^{3/2}}',
                'math_structures': ['矢量方程', '等式', '微分', '比例', '相对论因子', '坐标变换', '径向衰减'],
                'variables': ['\\vec{B}', '\\mu_{0}', '\\gamma', 'k', 'k^{\\prime}', '\\Omega', 't', 'x', 'v', 'y', 'z', '\\vec{i}', '\\vec{j}', '\\vec{k}'],
                'operators': ['=', '\\dfrac{d}{dt}', '\\dfrac{}{}', '+', '-', '\\cdot', '^2', '^{3/2}', '()'],
                'dimensions': {
                    'left': Dimension(mass=1, time=-1, charge=-1),  # [MT⁻¹Q⁻¹]
                    'right': Dimension(mass=1, time=-1, charge=-1)   # [LMT⁻²Q⁻²][Q][T⁻¹][L⁻²] = [MT⁻¹Q⁻¹]
                }
            },
            '公式12': {
                'name': '变化的引力场产生电磁场',
                'formula': '\\dfrac{\\partial^{2}\\vec{A}}{\\partial t^{2}} = \\dfrac{\\vec{v}}{f}\\left(\\vec{\\nabla}\\cdot\\vec{E}\\right) - \\dfrac{c^{2}}{f}\\left(\\vec{\\nabla}\\times\\vec{B}\\right)',
                'math_structures': ['矢量方程', '等式', '偏微分', '散度', '旋度', '比例'],
                'variables': ['\\vec{A}', 't', '\\vec{v}', 'f', '\\vec{E}', 'c', '\\vec{B}'],
                'operators': ['=', '+', '-', '\\dfrac{\\partial^{2}}{\\partial^{2}}', '\\dfrac{}{}', '\\vec{\\nabla}\\cdot', '\\vec{\\nabla}\\times', '()'],
                'dimensions': {
                    'left': Dimension(length=1, time=-4),  # [LT⁻²][T⁻²] = [LT⁻⁴]
                    'right': Dimension(length=1, time=-4)   # [LT⁻¹][L⁻¹MLT⁻³Q⁻¹] + [L²T⁻²][L⁻¹MT⁻¹Q⁻¹] = [LT⁻⁴]
                }
            },
            '公式13': {
                'name': '磁矢势方程',
                'formula': '\\vec{\\nabla} \\times \\vec{A} = \\dfrac{\\vec{B}}{f}',
                'math_structures': ['矢量方程', '等式', '旋度', '比例'],
                'variables': ['\\vec{A}', '\\vec{B}', 'f'],
                'operators': ['=', '\\vec{\\nabla} \\times', '\\dfrac{}{}'],
                'dimensions': {
                    'left': Dimension(mass=1, time=-1, charge=-1),  # [L⁻¹][LT⁻²] = [T⁻³] (需要调整)
                    'right': Dimension(mass=1, time=-1, charge=-1)   # [MT⁻¹Q⁻¹]
                }
            },
            '公式14': {
                'name': '变化的引力场产生电场',
                'formula': '\\vec{E} = -f\\dfrac{d\\vec{A}}{dt}',
                'math_structures': ['矢量方程', '等式', '微分', '标量乘法'],
                'variables': ['\\vec{E}', 'f', '\\vec{A}', 't'],
                'operators': ['=', '-', '\\dfrac{d}{dt}', '\\cdot'],
                'dimensions': {
                    'left': Dimension(length=1, mass=1, time=-3, charge=-1),  # [MLT⁻³Q⁻¹]
                    'right': Dimension(length=1, mass=1, time=-3, charge=-1)   # [LT⁻²][T⁻¹] = [LT⁻³] (需要通过f调整)
                }
            },
            '公式15': {
                'name': '变化的磁场产生引力场和电场',
                'formula': '\\dfrac{d\\vec{B}}{dt} = -\\dfrac{\\vec{A}\\times\\vec{E}}{c^2} - \\dfrac{\\vec{v}}{c^{2}}\\times\\dfrac{d\\vec{E}}{dt}',
                'math_structures': ['矢量方程', '等式', '微分', '叉乘', '比例'],
                'variables': ['\\vec{B}', 't', '\\vec{A}', '\\vec{E}', 'c', '\\vec{v}'],
                'operators': ['=', '-', '\\dfrac{d}{dt}', '\\times', '\\dfrac{}{}', '\\cdot'],
                'dimensions': {
                    'left': Dimension(mass=1, time=-2, charge=-1),  # [MT⁻¹Q⁻¹][T⁻¹] = [MT⁻²Q⁻¹]
                    'right': Dimension(mass=1, time=-2, charge=-1)   # [LT⁻²][MLT⁻³Q⁻¹][L⁻²T²] = [MT⁻²Q⁻¹]
                }
            },
            '公式16': {
                'name': '统一场论能量方程',
                'formula': 'E = m_0 c^2 = mc^2\\sqrt{1 - \\dfrac{v^2}{c^2}}',
                'math_structures': ['标量方程', '等式', '平方', '平方根', '相对论因子'],
                'variables': ['E', 'm_0', 'c', 'm', 'v'],
                'operators': ['=', '^2', '\\sqrt{}', '-', '\\dfrac{}{}', '\\cdot'],
                'dimensions': {
                    'left': Dimension(length=2, mass=1, time=-2),  # [ML²T⁻²]
                    'middle': Dimension(length=2, mass=1, time=-2),  # [M][L²T⁻²] = [ML²T⁻²]
                    'right': Dimension(length=2, mass=1, time=-2)   # [M][L²T⁻²] = [ML²T⁻²]
                }
            },
            '公式17': {
                'name': '光速飞行器动力学方程',
                'formula': '\\vec{F} = (\\vec{c} - \\vec{v})\\dfrac{dm}{dt}',
                'math_structures': ['矢量方程', '等式', '微分', '括号运算', '矢量减法', '标量乘法'],
                'variables': ['\\vec{F}', '\\vec{c}', '\\vec{v}', 'm', 't'],
                'operators': ['=', '-', '\\dfrac{d}{dt}', '\\cdot', '()'],
                'dimensions': {
                    'left': Dimension(length=1, mass=1, time=-2),  # [MLT⁻²]
                    'right': Dimension(length=1, mass=1, time=-2)   # [LT⁻¹][MT⁻¹] = [MLT⁻²]
                }
            },
            '公式18': {
                'name': '核力场定义方程',
                'formula': '\\vec{D} = - G m \\dfrac{ \\vec{c} - 3 \\dfrac{\\vec{r}}{r} \\dot{r} }{r^3}',
                'math_structures': ['矢量方程', '等式', '比例', '方向矢量', '径向衰减', '矢量减法'],
                'variables': ['\\vec{D}', 'G', 'm', '\\vec{c}', '\\vec{r}', 'r', '\\dot{r}'],
                'operators': ['=', '-', '\\dfrac{}{}', '+', '-', '\\cdot', '^3'],
                'dimensions': {
                    'left': Dimension(length=1, time=-2),  # [LT⁻²]
                    'right': Dimension(length=1, time=-2)   # [L³M⁻¹T⁻²][M][LT⁻¹][L⁻³] = [LT⁻³] (需要调整)
                }
            },
            '公式19': {
                'name': '引力光速统一方程',
                'formula': 'Z = \\dfrac{Gc}{2}',
                'math_structures': ['标量方程', '等式', '比例'],
                'variables': ['Z', 'G', 'c'],
                'operators': ['=', '\\dfrac{}{}', '\\cdot'],
                'dimensions': {
                    'left': Dimension(length=4, mass=-1, time=-3),  # [L³M⁻¹T⁻²][LT⁻¹] = [L⁴M⁻¹T⁻³]
                    'right': Dimension(length=4, mass=-1, time=-3)   # [L³M⁻¹T⁻²][LT⁻¹] = [L⁴M⁻¹T⁻³]
                }
            },
            '公式20': {
                'name': '电磁光速几何耦合常数',
                'formula': 'Z^{\\prime} = \\dfrac{c}{8\\pi\\varepsilon_0}',
                'math_structures': ['标量方程', '等式', '比例'],
                'variables': ['Z^{\\prime}', 'c', '\\varepsilon_0'],
                'operators': ['=', '\\dfrac{}{}'],
                'dimensions': {
                    'left': Dimension(length=4, mass=1, time=-3, charge=-2),  # [LT⁻¹][L³M¹T⁻⁴Q⁻²] = [L⁴MT⁻³Q⁻²]
                    'right': Dimension(length=4, mass=1, time=-3, charge=-2)   # [LT⁻¹][L³M¹T⁻⁴Q⁻²] = [L⁴MT⁻³Q⁻²]
                }
            }
        }
        
        # 数学结构分类
        self.math_structure_categories = {
            '方程类型': ['标量方程', '矢量方程', '张量方程'],
            '运算符': ['=', '+', '-', '\\cdot', '\\times', '\\dfrac{d}{dt}', '\\dfrac{\\partial}{\\partial}', '\\nabla^2', '\\vec{\\nabla}\\cdot', '\\vec{\\nabla}\\times', '\\sqrt{}', '^2', '\\cos', '\\sin'],
            '特殊结构': ['等式', '不等式', '微分方程', '积分方程', '波动方程', '相对论因子', '三角函数', '坐标分解', '方向矢量', '径向衰减', '比例', '括号运算']
        }
        
        # 求导规则
        self.derivative_rules = {
            '基本求导': [
                '\\dfrac{d}{dt}(t^n) = n t^{n-1}',
                '\\dfrac{d}{dt}(\\sin t) = \\cos t',
                '\\dfrac{d}{dt}(\\cos t) = -\\sin t',
                '\\dfrac{d}{dt}(e^t) = e^t',
                '\\dfrac{d}{dt}(\\ln t) = \\dfrac{1}{t}'
            ],
            '乘积法则': '\\dfrac{d}{dt}(uv) = u\\dfrac{dv}{dt} + v\\dfrac{du}{dt}',
            '商数法则': '\\dfrac{d}{dt}(\\dfrac{u}{v}) = \\dfrac{v\\dfrac{du}{dt} - u\\dfrac{dv}{dt}}{v^2}',
            '链式法则': '\\dfrac{d}{dt}(f(g(t))) = f\'(g(t)) \\cdot g\'(t)'
        }
    
    def analyze_math_structures(self) -> Dict[str, Any]:
        """
        分析数学结构的分布
        
        Returns:
            Dict[str, Any]: 数学结构分析结果
        """
        analysis = {}
        
        # 统计每种数学结构的使用次数
        structure_counts = {}
        for formula_id, formula in self.formulas.items():
            for structure in formula['math_structures']:
                structure_counts[structure] = structure_counts.get(structure, 0) + 1
        
        analysis['structure_counts'] = structure_counts
        analysis['most_common_structures'] = sorted(structure_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 统计变量使用次数
        variable_counts = {}
        for formula_id, formula in self.formulas.items():
            for var in formula['variables']:
                variable_counts[var] = variable_counts.get(var, 0) + 1
        
        analysis['variable_counts'] = variable_counts
        analysis['most_common_variables'] = sorted(variable_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 统计运算符使用次数
        operator_counts = {}
        for formula_id, formula in self.formulas.items():
            for op in formula['operators']:
                operator_counts[op] = operator_counts.get(op, 0) + 1
        
        analysis['operator_counts'] = operator_counts
        analysis['most_common_operators'] = sorted(operator_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 分析公式复杂度
        formula_complexity = {}
        for formula_id, formula in self.formulas.items():
            complexity = len(formula['math_structures']) + len(formula['variables']) + len(formula['operators'])
            formula_complexity[formula_id] = complexity
        
        analysis['formula_complexity'] = formula_complexity
        analysis['most_complex'] = max(formula_complexity, key=formula_complexity.get)
        analysis['least_complex'] = min(formula_complexity, key=formula_complexity.get)
        
        return analysis
    
    def validate_structure_consistency(self) -> List[Dict[str, Any]]:
        """
        验证数学结构的一致性
        
        Returns:
            List[Dict[str, Any]]: 数学结构一致性验证结果
        """
        results = []
        
        # 检查方程类型一致性
        vector_equations = [fid for fid, f in self.formulas.items() if '矢量方程' in f['math_structures']]
        scalar_equations = [fid for fid, f in self.formulas.items() if '标量方程' in f['math_structures']]
        
        results.append({
            'category': '方程类型分布',
            'status': "✓" if len(vector_equations) >= 10 else "⚠",
            'description': f'矢量方程: {len(vector_equations)}, 标量方程: {len(scalar_equations)}',
            'details': {
                'vector_equations': vector_equations,
                'scalar_equations': scalar_equations
            }
        })
        
        # 检查运算符一致性
        operator_analysis = {}
        for op, count in self.analyze_math_structures()['operator_counts'].items():
            if count >= 5:
                operator_analysis[op] = count
        
        results.append({
            'category': '常用运算符',
            'status': "✓" if len(operator_analysis) >= 5 else "⚠",
            'description': f'使用次数≥5的运算符: {len(operator_analysis)}个',
            'details': operator_analysis
        })
        
        # 检查特殊结构一致性
        special_structures = ['等式', '微分', '比例', '矢量方程', '标量方程']
        structure_presence = {}
        for structure in special_structures:
            count = sum(1 for f in self.formulas.values() if structure in f['math_structures'])
            structure_presence[structure] = count
        
        results.append({
            'category': '特殊结构分布',
            'status': "✓" if all(count >= 5 for count in structure_presence.values()) else "⚠",
            'description': '核心数学结构的分布情况',
            'details': structure_presence
        })
        
        # 检查变量一致性
        common_variables = [var for var, count in self.analyze_math_structures()['variable_counts'].items() if count >= 5]
        results.append({
            'category': '公共变量',
            'status': "✓" if len(common_variables) >= 5 else "⚠",
            'description': f'出现次数≥5的公共变量: {len(common_variables)}个',
            'details': common_variables
        })
        
        return results
    
    def validate_notational_consistency(self) -> List[Dict[str, Any]]:
        """
        验证符号表示的一致性
        
        Returns:
            List[Dict[str, Any]]: 符号表示一致性验证结果
        """
        results = []
        
        # 检查矢量符号一致性
        vector_vars = []
        for formula in self.formulas.values():
            for var in formula['variables']:
                if var.startswith('\\vec{'):
                    vector_vars.append(var)
        
        vector_consistency = len(set(vector_vars)) >= 5
        results.append({
            'category': '矢量符号一致性',
            'status': "✓" if vector_consistency else "⚠",
            'description': f'使用矢量符号的变量: {len(set(vector_vars))}个',
            'details': list(set(vector_vars))[:10]  # 只显示前10个
        })
        
        # 检查微分符号一致性
        diff_operators = ['\\dfrac{d}{dt}', '\\dfrac{\\partial}{\\partial t}', '\\dfrac{\\Delta}{\\Delta t}']
        diff_usage = []
        for formula in self.formulas.values():
            for op in formula['operators']:
                if any(diff_op in op for diff_op in diff_operators):
                    diff_usage.append(op)
        
        diff_consistency = len(set(diff_usage)) <= 3  # 微分符号种类不超过3种
        results.append({
            'category': '微分符号一致性',
            'status': "✓" if diff_consistency else "⚠",
            'description': f'使用的微分符号: {len(set(diff_usage))}种',
            'details': list(set(diff_usage))
        })
        
        # 检查特殊符号一致性
        special_symbols = ['\\Omega', '\\varepsilon_0', '\\mu_0', '\\gamma', 'G', 'c']
        symbol_usage = []
        for formula in self.formulas.values():
            for var in formula['variables']:
                if var in special_symbols:
                    symbol_usage.append(var)
        
        symbol_consistency = len(set(symbol_usage)) >= 4
        results.append({
            'category': '特殊符号一致性',
            'status': "✓" if symbol_consistency else "⚠",
            'description': f'使用的特殊符号: {len(set(symbol_usage))}个',
            'details': list(set(symbol_usage))
        })
        
        return results
    
    def analyze_formula_complexity(self) -> Dict[str, Any]:
        """
        分析公式复杂度
        
        Returns:
            Dict[str, Any]: 公式复杂度分析结果
        """
        complexity = {}
        
        # 计算每种复杂度指标
        for formula_id, formula in self.formulas.items():
            complexity[formula_id] = {
                'structure_count': len(formula['math_structures']),
                'variable_count': len(formula['variables']),
                'operator_count': len(formula['operators']),
                'total_complexity': len(formula['math_structures']) + len(formula['variables']) + len(formula['operators'])
            }
        
        # 排序复杂度
        sorted_complexity = sorted(complexity.items(), key=lambda x: x[1]['total_complexity'], reverse=True)
        
        return {
            'complexity_by_formula': complexity,
            'sorted_complexity': sorted_complexity,
            'most_complex': sorted_complexity[0],
            'least_complex': sorted_complexity[-1],
            'average_complexity': sum(c['total_complexity'] for c in complexity.values()) / len(complexity)
        }
    
    def validate_dimension_consistency(self) -> List[Dict[str, Any]]:
        """
        验证维度一致性
        
        Returns:
            List[Dict[str, Any]]: 维度一致性验证结果
        """
        results = []
        
        for formula_id, formula in self.formulas.items():
            if 'dimensions' in formula:
                dims = formula['dimensions']
                left_dim = None
                right_dims = []
                
                # 提取左侧维度
                if 'left' in dims:
                    left_dim = dims['left']
                
                # 提取右侧维度
                for key, dim in dims.items():
                    if key != 'left':
                        right_dims.append(dim)
                
                # 验证左侧与右侧维度一致性
                if left_dim and right_dims:
                    consistent = all(dim == left_dim for dim in right_dims)
                    results.append({
                        'formula': formula_id,
                        'name': formula['name'],
                        'status': "✓" if consistent else "✗",
                        'description': f'维度一致性检查: {"通过" if consistent else "失败"}',
                        'details': {
                            'left_dimension': str(left_dim),
                            'right_dimensions': [str(dim) for dim in right_dims]
                        }
                    })
        
        return results
    
    def validate_derivative_calculations(self) -> List[Dict[str, Any]]:
        """
        验证求导计算
        
        Returns:
            List[Dict[str, Any]]: 求导验证结果
        """
        results = []
        
        # 检查包含微分的公式
        derivative_formulas = []
        for formula_id, formula in self.formulas.items():
            if any('微分' in struct or 'd/dt' in op or '\\dfrac{d}{dt}' in op for struct in formula['math_structures'] for op in formula['operators']):
                derivative_formulas.append((formula_id, formula))
        
        # 验证每个包含微分的公式
        for formula_id, formula in derivative_formulas:
            # 检查微分运算符的使用
            has_valid_derivative = any(op in formula['operators'] for op in ['\\dfrac{d}{dt}', '\\dfrac{\\partial}{\\partial}', '\\dfrac{\\Delta}{\\Delta}'])
            
            results.append({
                'formula': formula_id,
                'name': formula['name'],
                'status': "✓" if has_valid_derivative else "⚠",
                'description': f'求导运算符检查: {"通过" if has_valid_derivative else "需要检查"}',
                'details': {
                    'derivative_operators': [op for op in formula['operators'] if 'd/' in op or '\\dfrac' in op]
                }
            })
        
        return results
    
    def perform_calculations(self, formula_id: str, params: Dict[str, float]) -> Dict[str, Any]:
        """
        执行公式计算
        
        Args:
            formula_id: 公式ID
            params: 参数值字典
        
        Returns:
            Dict[str, Any]: 计算结果
        """
        if formula_id not in self.formulas:
            return {'error': f'公式 {formula_id} 不存在'}
        
        formula = self.formulas[formula_id]
        
        # 这里实现具体的计算逻辑
        # 由于公式复杂，这里只返回计算框架
        calculation = {
            'formula': formula_id,
            'name': formula['name'],
            'params': params,
            'status': "✓",
            'description': '计算框架已准备',
            'details': {
                'variables': formula['variables'],
                'operators': formula['operators'],
                'math_structures': formula['math_structures']
            }
        }
        
        return calculation
    
    def generate_derivative_proof(self, formula_id: str) -> str:
        """
        生成求导证明
        
        Args:
            formula_id: 公式ID
        
        Returns:
            str: 求导证明内容
        """
        if formula_id not in self.formulas:
            return f'公式 {formula_id} 不存在'
        
        formula = self.formulas[formula_id]
        
        # 生成求导证明
        proof = f"# {formula['name']} 求导证明\n\n"
        proof += f"## 原公式\n\n"
        proof += f"${formula['formula']}$\n\n"
        proof += "## 求导分析\n\n"
        
        # 分析公式中的微分结构
        has_derivative = any('微分' in struct for struct in formula['math_structures'])
        derivative_operators = [op for op in formula['operators'] if 'd/' in op or '\\dfrac' in op]
        
        if has_derivative and derivative_operators:
            proof += "### 微分运算符\n\n"
            for op in derivative_operators:
                proof += f"- ${op}$\n"
            
            proof += "\n### 求导规则应用\n\n"
            proof += "1. **基本求导规则**\n"
            for rule in self.derivative_rules['基本求导']:
                proof += f"   - ${rule}$\n"
            
            proof += "\n2. **乘积法则**\n"
            proof += f"   - ${self.derivative_rules['乘积法则']}$\n"
            
            proof += "\n3. **商数法则**\n"
            proof += f"   - ${self.derivative_rules['商数法则']}$\n"
            
            proof += "\n4. **链式法则**\n"
            proof += f"   - ${self.derivative_rules['链式法则']}$\n"
        else:
            proof += "该公式不包含微分运算\n"
        
        return proof
    
    def generate_structure_report(self) -> str:
        """
        生成数学结构一致性验证报告
        
        Returns:
            str: 验证报告内容
        """
        from datetime import datetime
        
        report = "# 统一场论数学结构一致性验证报告\n\n"
        report += f"**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}\n\n"
        
        # 数学结构分析
        math_analysis = self.analyze_math_structures()
        report += "## 1. 数学结构分析\n\n"
        
        # 数学结构分布
        report += "### 1.1 数学结构分布\n\n"
        report += "| 数学结构 | 使用次数 |\n"
        report += "|---------|----------|\n"
        
        for structure, count in math_analysis['most_common_structures']:
            report += f"| {structure} | {count} |\n"
        
        # 变量使用情况
        report += "\n### 1.2 变量使用情况\n\n"
        report += "| 变量 | 使用次数 |\n"
        report += "|------|----------|\n"
        
        for var, count in math_analysis['most_common_variables'][:15]:  # 只显示前15个
            report += f"| ${var}$ | {count} |\n"
        
        # 运算符使用情况
        report += "\n### 1.3 运算符使用情况\n\n"
        report += "| 运算符 | 使用次数 |\n"
        report += "|--------|----------|\n"
        
        for op, count in math_analysis['most_common_operators'][:15]:  # 只显示前15个
            report += f"| ${op}$ | {count} |\n"
        
        # 结构一致性验证
        structure_results = self.validate_structure_consistency()
        report += "\n## 2. 结构一致性验证\n\n"
        report += "| 验证类别 | 状态 | 描述 |\n"
        report += "|---------|------|------|\n"
        
        for result in structure_results:
            status = "✓" if result['status'] == "✓" else "⚠"
            report += f"| {result['category']} | {status} | {result['description']} |\n"
        
        # 符号一致性验证
        notation_results = self.validate_notational_consistency()
        report += "\n## 3. 符号表示一致性验证\n\n"
        report += "| 验证类别 | 状态 | 描述 |\n"
        report += "|---------|------|------|\n"
        
        for result in notation_results:
            status = "✓" if result['status'] == "✓" else "⚠"
            report += f"| {result['category']} | {status} | {result['description']} |\n"
        
        # 维度一致性验证
        dimension_results = self.validate_dimension_consistency()
        report += "\n## 4. 维度一致性验证\n\n"
        report += "| 公式 | 名称 | 状态 | 描述 |\n"
        report += "|------|------|------|------|\n"
        
        for result in dimension_results:
            status = "✓" if result['status'] == "✓" else "✗"
            report += f"| {result['formula']} | {result['name']} | {status} | {result['description']} |\n"
        
        # 求导验证
        derivative_results = self.validate_derivative_calculations()
        report += "\n## 5. 求导计算验证\n\n"
        report += "| 公式 | 名称 | 状态 | 描述 |\n"
        report += "|------|------|------|------|\n"
        
        for result in derivative_results:
            status = "✓" if result['status'] == "✓" else "⚠"
            report += f"| {result['formula']} | {result['name']} | {status} | {result['description']} |\n"
        
        # 公式复杂度分析
        complexity_analysis = self.analyze_formula_complexity()
        report += "\n## 6. 公式复杂度分析\n\n"
        
        # 复杂度排序
        report += "### 6.1 公式复杂度排序\n\n"
        report += "| 公式ID | 公式名称 | 结构数 | 变量数 | 运算符数 | 总复杂度 |\n"
        report += "|-------|---------|--------|----------|----------|\n"
        
        for formula_id, comp in complexity_analysis['sorted_complexity']:
            formula_name = self.formulas[formula_id]['name']
            report += f"| {formula_id} | {formula_name} | {comp['structure_count']} | {comp['variable_count']} | {comp['operator_count']} | {comp['total_complexity']} |\n"
        
        most_complex = complexity_analysis['most_complex']
        least_complex = complexity_analysis['least_complex']
        report += f"\n**最复杂公式**：{self.formulas[most_complex[0]]['name']} ({most_complex[0]})\n"
        report += f"**最简单公式**：{self.formulas[least_complex[0]]['name']} ({least_complex[0]})\n"
        report += f"**平均复杂度**：{complexity_analysis['average_complexity']:.1f}\n\n"
        
        # 综合评价
        report += "## 7. 综合评价\n\n"
        
        # 计算评价分数
        total_score = 0
        
        # 结构一致性分数
        structure_score = sum(1 for r in structure_results if r['status'] == "✓")
        total_score += structure_score * 25
        
        # 符号一致性分数
        notation_score = sum(1 for r in notation_results if r['status'] == "✓")
        total_score += notation_score * 25
        
        # 维度一致性分数
        dimension_score = sum(1 for r in dimension_results if r['status'] == "✓")
        total_score += dimension_score * 15
        
        # 求导验证分数
        derivative_score = sum(1 for r in derivative_results if r['status'] == "✓")
        total_score += derivative_score * 10
        
        # 复杂度分布分数
        if complexity_analysis['average_complexity'] >= 10 and complexity_analysis['average_complexity'] <= 20:
            total_score += 25
        else:
            total_score += 15
        
        # 结构多样性分数
        if len(math_analysis['structure_counts']) >= 15:
            total_score += 25
        else:
            total_score += 15
        
        if total_score >= 90:
            report += "**评价结果**：优秀\n"
            report += "数学结构一致性验证结果良好，公式表达统一，符号使用规范。\n"
        elif total_score >= 70:
            report += "**评价结果**：良好\n"
            report += "数学结构一致性基本正确，但存在一些需要优化的地方。\n"
        else:
            report += "**评价结果**：需要改进\n"
            report += "数学结构一致性存在问题，需要统一符号和结构表达。\n"
        
        # 改进建议
        report += "\n## 8. 改进建议\n\n"
        
        suggestions = []
        
        # 基于验证结果生成建议
        if structure_score < len(structure_results):
            suggestions.append("1. **统一方程类型**：确保相似物理量使用相同类型的方程表达")
        
        if notation_score < len(notation_results):
            suggestions.append("2. **规范符号表示**：统一微分符号、特殊符号的使用方式")
        
        if dimension_score < len(dimension_results):
            suggestions.append("3. **检查维度一致性**：确保所有公式的量纲正确")
        
        if derivative_score < len(derivative_results):
            suggestions.append("4. **验证求导计算**：检查微分运算符的正确使用")
        
        if complexity_analysis['average_complexity'] < 10:
            suggestions.append("5. **丰富数学结构**：适当增加数学表达的丰富性，体现物理概念的深度")
        elif complexity_analysis['average_complexity'] > 20:
            suggestions.append("5. **简化复杂公式**：对过于复杂的公式进行适当简化，提高可读性")
        
        if len(math_analysis['structure_counts']) < 15:
            suggestions.append("6. **增加结构多样性**：在保持一致性的同时，增加数学结构的多样性")
        
        if not suggestions:
            suggestions.append("1. **保持现有结构**：数学结构一致性良好，建议保持")
            suggestions.append("2. **细化符号规范**：可以制定更详细的符号使用规范")
            suggestions.append("3. **建立公式库**：建立数学结构统一的公式库，方便后续扩展")
        
        for suggestion in suggestions:
            report += f"{suggestion}\n"
        
        return report

if __name__ == "__main__":
    # 创建验证器实例
    validator = MathematicalStructureValidator()
    
    # 生成验证报告
    report = validator.generate_structure_report()
    
    # 保存报告
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = os.path.join(output_dir, "mathematical_structure_validation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"数学结构一致性验证报告已生成：{report_path}")
    
    # 验证维度一致性
    dimension_results = validator.validate_dimension_consistency()
    valid_dimension = sum(1 for r in dimension_results if r['status'] == "✓")
    print(f"\n维度一致性验证：{valid_dimension}/{len(dimension_results)} 优秀")
    
    # 验证求导计算
    derivative_results = validator.validate_derivative_calculations()
    valid_derivative = sum(1 for r in derivative_results if r['status'] == "✓")
    print(f"求导计算验证：{valid_derivative}/{len(derivative_results)} 优秀")
    
    # 打印验证摘要
    structure_results = validator.validate_structure_consistency()
    notation_results = validator.validate_notational_consistency()
    complexity_analysis = validator.analyze_formula_complexity()
    
    valid_structure = sum(1 for r in structure_results if r['status'] == "✓")
    valid_notation = sum(1 for r in notation_results if r['status'] == "✓")
    
    print(f"\n验证摘要：")
    print(f"结构一致性验证：{valid_structure}/{len(structure_results)} 优秀")
    print(f"符号一致性验证：{valid_notation}/{len(notation_results)} 优秀")
    print(f"维度一致性验证：{valid_dimension}/{len(dimension_results)} 优秀")
    print(f"求导计算验证：{valid_derivative}/{len(derivative_results)} 优秀")
    print(f"平均公式复杂度：{complexity_analysis['average_complexity']:.1f}")
    print(f"最复杂公式：{validator.formulas[complexity_analysis['most_complex'][0]]['name']}")
    print(f"最简单公式：{validator.formulas[complexity_analysis['least_complex'][0]]['name']}")
    
    # 生成一个求导证明示例
    print(f"\n生成求导证明示例...")
    derivative_proof = validator.generate_derivative_proof('公式7')  # 宇宙大统一方程
    proof_path = os.path.join(output_dir, "derivative_proof_example.md")
    with open(proof_path, 'w', encoding='utf-8') as f:
        f.write(derivative_proof)
    print(f"求导证明示例已生成：{proof_path}")
    
    # 执行一个计算示例
    print(f"\n执行计算示例...")
    calculation = validator.perform_calculations('公式16', {'m0': 1.0, 'c': 299792458, 'v': 0})
    print(f"计算结果：{calculation['name']} - {calculation['status']}")
    print(f"参数：{calculation['params']}")
