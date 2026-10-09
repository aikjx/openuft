import re
from typing import Dict, Tuple, Optional, List

class Dimension:
    def __init__(self, length=0, mass=0, time=0, current=0):
        self.length = length
        self.mass = mass
        self.time = time
        self.current = current
    
    def __repr__(self):
        terms = []
        if self.length != 0:
            terms.append(f"L^{self.length}")
        if self.mass != 0:
            terms.append(f"M^{self.mass}")
        if self.time != 0:
            terms.append(f"T^{self.time}")
        if self.current != 0:
            terms.append(f"I^{self.current}")
        return "[" + " ".join(terms) + "]" if terms else "[1]"
    
    def __eq__(self, other):
        if not isinstance(other, Dimension):
            return False
        return (
            self.length == other.length and
            self.mass == other.mass and
            self.time == other.time and
            self.current == other.current
        )
    
    def __mul__(self, other):
        if not isinstance(other, Dimension):
            return self
        return Dimension(
            self.length + other.length,
            self.mass + other.mass,
            self.time + other.time,
            self.current + other.current
        )
    
    def __truediv__(self, other):
        if not isinstance(other, Dimension):
            return self
        return Dimension(
            self.length - other.length,
            self.mass - other.mass,
            self.time - other.time,
            self.current - other.current
        )
    
    def __pow__(self, power):
        return Dimension(
            self.length * power,
            self.mass * power,
            self.time * power,
            self.current * power
        )

class DimensionValidator:
    def __init__(self):
        self.base_dimensions = {
            'length': Dimension(length=1),
            'mass': Dimension(mass=1),
            'time': Dimension(time=1),
            'current': Dimension(current=1),
        }
        
        self.derived_dimensions = {
            'velocity': Dimension(length=1, time=-1),  # L T⁻¹
            'acceleration': Dimension(length=1, time=-2),  # L T⁻²
            'force': Dimension(length=1, mass=1, time=-2),  # M L T⁻²
            'momentum': Dimension(length=1, mass=1, time=-1),  # M L T⁻¹
            'energy': Dimension(length=2, mass=1, time=-2),  # M L² T⁻²
            'electric_field': Dimension(length=1, mass=1, time=-3, current=-1),  # M L I⁻¹ T⁻³
            'magnetic_field': Dimension(mass=1, time=-2, current=-1),  # M I⁻¹ T⁻²
            'gravitational_field': Dimension(length=1, time=-2),  # L T⁻²
            'nuclear_field': Dimension(length=1, time=-3),  # L T⁻³
            'charge': Dimension(current=1, time=1),  # I T
            'coupling_constant': Dimension(length=4, mass=-1, time=-3),  # L⁴ M⁻¹ T⁻³
            'electromagnetic_coupling': Dimension(length=4, mass=1, time=-5, current=-2),  # L⁴ M T⁻⁵ I⁻²
            'cosmological_constant': Dimension(length=-2),  # L⁻²
        }
        
        self.constants = {
            'C': Dimension(length=1, time=-1),  # 光速
            'G': Dimension(length=3, mass=-1, time=-2),  # 万有引力常数
            'ε0': Dimension(length=-3, mass=-1, time=4, current=2),  # 真空介电常数
            'μ0': Dimension(length=1, mass=1, time=-2, current=-2),  # 真空磁导率
            'k': Dimension(mass=1),  # 空间-质量耦合常数
            'k': Dimension(current=1, time=1, mass=-1),  # 电荷-空间耦合常数
            'Z': Dimension(length=4, mass=-1, time=-3),  # 引力光速统一常数
            'Z': Dimension(length=4, mass=1, time=-5, current=-2),  # 电磁光速几何耦合常数
            'h': Dimension(length=2, mass=1, time=-1),  # 普朗克常数
            'hbar': Dimension(length=2, mass=1, time=-1),  # 约化普朗克常数
            'H0': Dimension(time=-1),  # 哈勃常数
            'f': Dimension(mass=1, current=-1),  # 场转换耦合常数
        }
        
        self.special_symbols = {
            'n': Dimension(),  # 空间几何参数（无量纲）
            'Ω': Dimension(),  # 立体角（无量纲）
            'γ': Dimension(),  # 洛伦兹因子（无量纲）
            'r': Dimension(length=1),  # 位置矢量
            'V': Dimension(length=1, time=-1),  # 速度矢量
            'A': Dimension(length=1, time=-2),  # 引力场强度
            'E': Dimension(length=1, mass=1, time=-3, current=-1),  # 电场强度
            'B': Dimension(mass=1, time=-2, current=-1),  # 磁感应强度
            'D': Dimension(length=1, time=-3),  # 核力场强度
            'P': Dimension(length=1, mass=1, time=-1),  # 动量
            'F': Dimension(length=1, mass=1, time=-2),  # 力
            'E_energy': Dimension(length=2, mass=1, time=-2),  # 能量
            'L': Dimension(length=1),  # 空间波动幅度
            'Ψ': Dimension(),  # 波函数（无量纲）
            'm': Dimension(mass=1),  # 质量
            'm0': Dimension(mass=1),  # 静止质量
            'q': Dimension(current=1, time=1),  # 电荷
            'Λ': Dimension(length=-2),  # 宇宙学常数
        }
    
    def parse_expression(self, expr):
        # 移除所有空格和换行
        expr = re.sub(r'\s+', '', expr)
        # 简化处理，直接返回表达式
        return expr
    
    def get_dimension(self, term):
        # 处理基本常数和符号
        if term in self.constants:
            return self.constants[term]
        elif term in self.special_symbols:
            return self.special_symbols[term]
        # 处理长度单位
        elif term in ['x', 'y', 'z', 'r']:
            return Dimension(length=1)
        # 处理无量纲量
        elif term in ['i', 'j', 'k', 't', 'n', 'Ω', 'γ']:
            return Dimension()
        # 处理微分表达式（简化处理）
        elif 'd' in term and 'dt' in term:
            return Dimension(time=-1)
        # 处理偏微分表达式（简化处理）
        elif 'partial' in term or '∂' in term:
            return Dimension(time=-1)
        # 处理矢量运算（简化处理）
        elif 'nabla' in term or '∇' in term:
            return Dimension(length=-1)
        # 处理点积和叉积（简化处理）
        elif 'cdot' in term or 'times' in term:
            return Dimension()
        # 处理括号和其他符号
        elif '(' in term or ')' in term or '[' in term or ']' in term:
            return Dimension()
        # 处理分数和其他运算符号
        elif '/' in term or '*' in term or '+' in term or '-' in term:
            return Dimension()
        # 处理希腊字母
        elif term in ['μ', 'ν', 'theta', 'θ']:
            return Dimension()
        return Dimension()
    
    def validate_equation(self, left_expr, right_expr):
        left_dim = self.calculate_dimension(left_expr)
        right_dim = self.calculate_dimension(right_expr)
        return left_dim == right_dim, left_dim, right_dim
    
    def calculate_dimension(self, expr):
        # 解析表达式
        parsed_expr = self.parse_expression(expr)
        
        # 初始化量纲
        dim = Dimension()
        
        # 检查表达式中的关键物理量和常数
        if 'C' in parsed_expr:
            dim = dim * self.constants.get('C', Dimension())
        if 'G' in parsed_expr:
            dim = dim * self.constants.get('G', Dimension())
        if 'ε0' in parsed_expr or 'varepsilon0' in parsed_expr:
            dim = dim * self.constants.get('ε0', Dimension())
        if 'μ0' in parsed_expr or 'mu0' in parsed_expr:
            dim = dim * self.constants.get('μ0', Dimension())
        if 'h' in parsed_expr or 'hbar' in parsed_expr:
            dim = dim * self.constants.get('h', Dimension())
        if 'H0' in parsed_expr:
            dim = dim * self.constants.get('H0', Dimension())
        
        # 检查特殊符号
        if 'm' in parsed_expr:
            dim = dim * self.special_symbols.get('m', Dimension())
        if 'm0' in parsed_expr:
            dim = dim * self.special_symbols.get('m0', Dimension())
        if 'q' in parsed_expr:
            dim = dim * self.special_symbols.get('q', Dimension())
        if 'A' in parsed_expr:
            dim = dim * self.special_symbols.get('A', Dimension())
        if 'E' in parsed_expr:
            dim = dim * self.special_symbols.get('E', Dimension())
        if 'B' in parsed_expr:
            dim = dim * self.special_symbols.get('B', Dimension())
        if 'D' in parsed_expr:
            dim = dim * self.special_symbols.get('D', Dimension())
        if 'P' in parsed_expr:
            dim = dim * self.special_symbols.get('P', Dimension())
        if 'F' in parsed_expr:
            dim = dim * self.special_symbols.get('F', Dimension())
        if 'L' in parsed_expr:
            dim = dim * self.special_symbols.get('L', Dimension())
        if 'Λ' in parsed_expr or 'Lambda' in parsed_expr:
            dim = dim * self.special_symbols.get('Λ', Dimension())
        
        # 检查微分和偏微分
        if 'd' in parsed_expr and 'dt' in parsed_expr:
            dim = dim * Dimension(time=-1)
        if 'partial' in parsed_expr or '∂' in parsed_expr:
            dim = dim * Dimension(time=-1)
        
        # 检查矢量运算
        if 'nabla' in parsed_expr or '∇' in parsed_expr:
            dim = dim * Dimension(length=-1)
        
        # 检查长度相关量
        if 'r' in parsed_expr or 'x' in parsed_expr or 'y' in parsed_expr or 'z' in parsed_expr:
            dim = dim * Dimension(length=1)
        
        # 检查时间相关量
        if 't' in parsed_expr:
            dim = dim * Dimension(time=1)
        
        return dim

class UnifiedFieldTheoryValidator:
    def __init__(self):
        self.validator = DimensionValidator()
        self.formulas = [
            {
                "name": "时空同一化方程",
                "expression": "\\vec{r}(t) = \\vec{C}t",
                "expected_dimension": "长度 [L]"
            },
            {
                "name": "三维螺旋时空方程",
                "expression": "\\vec{r}(t) = r\\cos\\omega t \\cdot \\vec{i} + r\\sin\\omega t \\cdot \\vec{j} + ht \\cdot \\vec{k}",
                "expected_dimension": "长度 [L]"
            },
            {
                "name": "质量定义方程",
                "expression": "m = k \\dfrac{dn}{d\\Omega}",
                "expected_dimension": "质量 [M]"
            },
            {
                "name": "引力场定义方程",
                "expression": "\\vec{A} = -Gk\\dfrac{\\Delta n}{\\Delta s}\\dfrac{\\vec{r}}{r^2}",
                "expected_dimension": "引力场强度 [LT⁻²]"
            },
            {
                "name": "静止动量方程",
                "expression": "\\vec{p}_{0} = m_{0}\\vec{C}_{0}",
                "expected_dimension": "动量 [MLT⁻¹]"
            },
            {
                "name": "运动动量方程",
                "expression": "\\vec{P} = m(\\vec{C} - \\vec{V})",
                "expected_dimension": "动量 [MLT⁻¹]"
            },
            {
                "name": "宇宙大统一方程（力方程）",
                "expression": "\\vec{F} = \\dfrac{d\\vec{P}}{dt} = \\vec{C}\\dfrac{dm}{dt} - \\vec{V}\\dfrac{dm}{dt} + m\\dfrac{d\\vec{C}}{dt} - m\\dfrac{d\\vec{V}}{dt}",
                "expected_dimension": "力 [MLT⁻²]"
            },
            {
                "name": "空间波动方程",
                "expression": "\\nabla^2 L = \\dfrac{1}{C^2} \\dfrac{\\partial^2 L}{\\partial t^2}",
                "expected_dimension": "波动方程"
            },
            {
                "name": "电荷定义方程",
                "expression": "q = k^{\\prime}k\\dfrac{1}{\\Omega^{2}}\\dfrac{d\\Omega}{dt}",
                "expected_dimension": "电荷 [Q]"
            },
            {
                "name": "电场定义方程",
                "expression": "\\vec{E} = -\\dfrac{kk^{\\prime}}{4\\pi\\varepsilon_0\\Omega^2}\\dfrac{d\\Omega}{dt}\\dfrac{\\vec{r}}{r^3}",
                "expected_dimension": "电场强度 [MLI⁻¹T⁻³]"
            },
            {
                "name": "磁场定义方程",
                "expression": "\\vec{B} = \\dfrac{\\mu_{0} \\gamma k k^{\\prime}}{4 \\pi \\Omega^{2}} \\dfrac{d \\Omega}{d t} \\dfrac{[(x-V t) \\vec{i}+y \\vec{j}+z \\vec{k}]}{[\\gamma^{2}(x-V t)^{2}+y^{2}+z^{2}]^{3/2}}",
                "expected_dimension": "磁感应强度 [MI⁻¹T⁻²]"
            },
            {
                "name": "变化的引力场产生电磁场",
                "expression": "\\dfrac{\\partial^{2}\\vec{A}}{\\partial t^{2}} = \\vec{V}(\\vec{\\nabla}\\cdot\\vec{E}) - C^{2}(\\vec{\\nabla}\\times\\vec{B})",
                "expected_dimension": "场变化率 [LT⁻³]"
            },
            {
                "name": "引力场旋度方程",
                "expression": "\\vec{\\nabla} \\times \\dfrac{\\partial\\vec{A}}{\\partial t} = \\vec{B}",
                "expected_dimension": "引力场强度 [LT⁻²]"
            },
            {
                "name": "变化的引力场产生电场",
                "expression": "\\vec{E} = -\\dfrac{d\\vec{A}}{dt}",
                "expected_dimension": "电场强度 [MLI⁻¹T⁻³]"
            },
            {
                "name": "变化的磁场产生引力场和电场",
                "expression": "\\dfrac{d\\vec{B}}{dt} = -\\dfrac{\\vec{A}\\times\\vec{E}}{C^2} - \\dfrac{\\vec{V}}{C^{2}}\\times\\dfrac{d\\vec{E}}{dt}",
                "expected_dimension": "磁场变化率 [MI⁻¹T⁻³]"
            },
            {
                "name": "统一场论能量方程",
                "expression": "E = m_0 C^2 = mC^2\\sqrt{1 - \\dfrac{V^2}{C^2}}",
                "expected_dimension": "能量 [ML²T⁻²]"
            },
            {
                "name": "光速飞行器动力学方程",
                "expression": "\\vec{F} = (\\vec{C} - \\vec{V})\\dfrac{dm}{dt}",
                "expected_dimension": "力 [MLT⁻²]"
            },
            {
                "name": "核力场定义方程",
                "expression": "\\vec{D} = - G m \\dfrac{ \\vec{C} - 3 \\dfrac{\\vec{r}}{r} \\dot{r} }{r^3}",
                "expected_dimension": "核力场强度 [LT⁻³]"
            },
            {
                "name": "引力光速统一方程",
                "expression": "Z = \\dfrac{GC}{2}",
                "expected_dimension": "耦合常数 [L⁴M⁻¹T⁻³]"
            },
            {
                "name": "电磁光速几何耦合常数",
                "expression": "Z' = \\dfrac{C}{8\\pi\\varepsilon_0}",
                "expected_dimension": "电磁耦合 [L⁴MT⁻³I⁻²]"
            },
            {
                "name": "加速运动电荷产生引力场方程",
                "expression": "\\vec{E}_{\\theta} = \frac{-q}{4\\pi \\varepsilon_0 C^2 r} \\vec{A} \\times \\hat{r}",
                "expected_dimension": "电场强度 [MLI⁻¹T⁻³]"
            },
            {
                "name": "圆周运动正电荷产生的引力场方程",
                "expression": "\\vec{B}_{\\theta} = -\\frac{q}{4\\pi\\varepsilon_0 C^3 r} \\left( \\vec{A} \\times \\hat{r} \\right)",
                "expected_dimension": "磁感应强度 [MI⁻¹T⁻²]"
            },
            {
                "name": "量子化质量方程",
                "expression": "m = n \\cdot m_0",
                "expected_dimension": "质量 [M]"
            },
            {
                "name": "宇宙学常数方程",
                "expression": "\\Lambda = \\dfrac{3H_0^2}{C^2}",
                "expected_dimension": "宇宙学常数 [L⁻²]"
            },
            {
                "name": "场的量子化方程",
                "expression": "\\hat{\\vec{A}} = \\sum_{k} \\sqrt{\\dfrac{\\hbar}{2\\omega_k}} (\\hat{a}_k \\vec{e}_k + \\hat{a}_k^\\dagger \\vec{e}_k^*)",
                "expected_dimension": "量子场算符"
            },
            {
                "name": "时空曲率方程",
                "expression": "R_{\\mu\\nu} - \\dfrac{1}{2}g_{\\mu\\nu}R + \\Lambda g_{\\mu\\nu} = \\dfrac{8\\pi G}{C^4}T_{\\mu\\nu}",
                "expected_dimension": "曲率张量"
            },
            {
                "name": "统一场论波函数方程",
                "expression": "i\\hbar \\dfrac{\\partial\\Psi}{\\partial t} = -\\dfrac{\\hbar^2}{2m}\\nabla^2\\Psi + V(\\vec{r})\\Psi",
                "expected_dimension": "波函数方程"
            }
        ]
    
    def validate_all_formulas(self):
        results = []
        for i, formula in enumerate(self.formulas, 1):
            name = formula["name"]
            expression = formula["expression"]
            expected = formula["expected_dimension"]
            
            # 分离左右两边
            if "=" in expression:
                parts = expression.split("=")
                left_expr = parts[0]
                right_expr = "=".join(parts[1:])
                
                valid, left_dim, right_dim = self.validator.validate_equation(left_expr, right_expr)
                results.append({
                    "formula": i,
                    "name": name,
                    "valid": valid,
                    "left_dim": str(left_dim),
                    "right_dim": str(right_dim),
                    "expected": expected
                })
        return results

if __name__ == "__main__":
    validator = UnifiedFieldTheoryValidator()
    results = validator.validate_all_formulas()
    
    print("张祥前统一场论公式量纲验证结果")
    print("=" * 100)
    
    valid_count = 0
    total_count = len(results)
    
    for result in results:
        status = "✓" if result["valid"] else "✗"
        print(f"{result['formula']}. {result['name']}")
        print(f"   状态: {status}")
        print(f"   左侧量纲: {result['left_dim']}")
        print(f"   右侧量纲: {result['right_dim']}")
        print(f"   预期量纲: {result['expected']}")
        print()
        if result["valid"]:
            valid_count += 1
    
    print("=" * 100)
    print(f"验证结果: {valid_count}/{total_count} 个公式量纲正确")
    print(f"正确率: {valid_count/total_count*100:.2f}%")
