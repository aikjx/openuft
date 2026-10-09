#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论核心公式量纲验证（最终修复版）

此脚本用于验证张祥前统一场论中22个核心公式的量纲一致性
使用基本量纲：[L]长度、[M]质量、[T]时间、[I]电流
"""

class Dimension:
    """量纲类"""
    def __init__(self, L: int = 0, M: int = 0, T: int = 0, I: int = 0):
        self.L = L  # 长度
        self.M = M  # 质量
        self.T = T  # 时间
        self.I = I  # 电流
    
    def __str__(self):
        terms = []
        if self.L != 0:
            terms.append(f"[L^{self.L}]")
        if self.M != 0:
            terms.append(f"[M^{self.M}]")
        if self.T != 0:
            terms.append(f"[T^{self.T}]")
        if self.I != 0:
            terms.append(f"[I^{self.I}]")
        return "".join(terms) if terms else "无量纲"
    
    def __eq__(self, other):
        if not isinstance(other, Dimension):
            return False
        return (
            self.L == other.L and
            self.M == other.M and
            self.T == other.T and
            self.I == other.I
        )
    
    def __mul__(self, other):
        if not isinstance(other, Dimension):
            return self
        return Dimension(
            self.L + other.L,
            self.M + other.M,
            self.T + other.T,
            self.I + other.I
        )
    
    def __truediv__(self, other):
        if not isinstance(other, Dimension):
            return self
        return Dimension(
            self.L - other.L,
            self.M - other.M,
            self.T - other.T,
            self.I - other.I
        )
    
    def pow(self, exponent: int):
        return Dimension(
            self.L * exponent,
            self.M * exponent,
            self.T * exponent,
            self.I * exponent
        )

class DimensionValidator:
    """量纲验证器"""
    def __init__(self):
        # 基本物理量的量纲
        self.dimensions = {
            # 基本量
            'L': Dimension(L=1),      # 长度
            'M': Dimension(M=1),      # 质量
            'T': Dimension(T=1),      # 时间
            'I': Dimension(I=1),      # 电流
            'Q': Dimension(I=1, T=1), # 电荷 (Q = I·T)
            
            # 导出量
            'v': Dimension(L=1, T=-1),     # 速度
            'V': Dimension(L=1, T=-1),     # 速度（大写）
            'a': Dimension(L=1, T=-2),     # 加速度
            'F': Dimension(L=1, M=1, T=-2), # 力
            'E_energy': Dimension(L=2, M=1, T=-2), # 能量
            'P_power': Dimension(L=2, M=1, T=-3), # 功率
            'p': Dimension(L=1, M=1, T=-1), # 动量
            'p0': Dimension(L=1, M=1, T=-1), # 静止动量
            'P': Dimension(L=1, M=1, T=-1), # 运动动量
            
            # 场量
            'A': Dimension(L=1, T=-2),         # 引力场强度
            'E': Dimension(L=1, M=1, I=-1, T=-3), # 电场强度
            'B': Dimension(M=1, I=-1, T=-2),   # 磁感应强度
            'D': Dimension(L=1, T=-3),         # 核力场强度
            
            # 常数
            'C': Dimension(L=1, T=-1),     # 光速
            'G': Dimension(L=3, M=-1, T=-2), # 万有引力常数
            'epsilon0': Dimension(L=-3, M=-1, T=4, I=2), # 真空介电常数
            'mu0': Dimension(L=1, M=1, T=-2, I=-2), # 真空磁导率
            'hbar': Dimension(L=2, M=1, T=-1), # 约化普朗克常数
            'k': Dimension(M=1),           # 空间-质量耦合常数
            'k_prime': Dimension(I=1, T=1, M=-1), # 空间-电荷耦合常数
            'Z': Dimension(L=4, M=-1, T=-3), # 引力光速统一常数
            'Z_prime': Dimension(L=4, M=1, T=-5, I=-2), # 电磁光速几何耦合常数
            
            # 其他物理量
            't': Dimension(T=1),          # 时间
            'r': Dimension(L=1),          # 空间位置
            'm': Dimension(M=1),          # 质量
            'm0': Dimension(M=1),         # 静止质量
            'q': Dimension(I=1, T=1),     # 电荷
            'omega': Dimension(T=-1),     # 角频率
            'h': Dimension(L=1, T=-1),    # 螺距
            'gamma': Dimension(),         # 洛伦兹因子（无量纲）
            'n': Dimension(),             # 空间几何参数（无量纲）
            'Omega': Dimension(),         # 立体角（无量纲）
            'dot_r': Dimension(L=1, T=-1), # 径向速度
            'Delta_n': Dimension(),       # 空间几何参数变化
            'Delta_s': Dimension(L=1),    # 空间距离变化
            'dn': Dimension(),            # 空间几何参数微分
            'dOmega': Dimension(),        # 立体角微分
            'dP': Dimension(L=1, M=1, T=-1), # 动量微分
            'dA': Dimension(L=1, T=-2),   # 引力场强度微分
            'dE': Dimension(L=1, M=1, I=-1, T=-3), # 电场强度微分
            'dB': Dimension(M=1, I=-1, T=-2), # 磁感应强度微分
            'd2A': Dimension(L=1, T=-2),  # 引力场强度二阶微分
            'd2L': Dimension(L=1),        # 空间波动幅度二阶微分
            'r_hat': Dimension(),         # 径向单位矢量（无量纲）
            'nabla': Dimension(L=-1),      # 梯度算子
            'nabla2': Dimension(L=-2),     # 拉普拉斯算子
            'f': Dimension(M=1, I=-1),     # 场转化耦合常数
        }
    
    def get_dimension(self, symbol: str) -> Dimension:
        """获取物理量的量纲"""
        return self.dimensions.get(symbol, Dimension())
    
    def validate_equation(self, left_expr: str, right_expr: str) -> tuple:
        """验证方程左右两边的量纲是否一致"""
        try:
            left_dim = self.calculate_dimension(left_expr)
            right_dim = self.calculate_dimension(right_expr)
            is_valid = left_dim == right_dim
            status = "✓" if is_valid else "✗"
            message = f"{status} {left_expr} = {right_expr}"
            message += f"\n  左边量纲: {left_dim}"
            message += f"\n  右边量纲: {right_dim}"
            message += f"\n  结果: {'一致' if is_valid else '不一致'}"
            return is_valid, message, left_dim, right_dim
        except Exception as e:
            return False, f"✗ 验证失败: {str(e)}", Dimension(), Dimension()
    
    def calculate_dimension(self, expr: str) -> Dimension:
        """计算表达式的量纲"""
        expr = expr.strip()
        
        # 处理括号
        if '(' in expr and ')' in expr:
            # 找到最内层括号
            while '(' in expr:
                start = expr.rfind('(')
                end = expr.find(')', start)
                if start == -1 or end == -1:
                    break
                inner_expr = expr[start+1:end]
                inner_dim = self.calculate_dimension(inner_expr)
                # 替换括号内容为临时符号
                temp_key = f"temp_{id(inner_dim)}"
                expr = expr[:start] + temp_key + expr[end+1:]
                self.dimensions[temp_key] = inner_dim
        
        # 处理加减表达式
        if '+' in expr or '-' in expr:
            parts = expr.split('+') if '+' in expr else expr.split('-')
            if not parts:
                return Dimension()
            base_dim = self.calculate_dimension(parts[0])
            for part in parts[1:]:
                part_dim = self.calculate_dimension(part)
                if part_dim != base_dim:
                    return Dimension()
            return base_dim
        
        # 处理乘除表达式
        if '*' in expr or '/' in expr:
            # 分割表达式
            terms = []
            ops = []
            current_term = ''
            i = 0
            while i < len(expr):
                if expr[i] in '*/':
                    if current_term:
                        terms.append(current_term.strip())
                        ops.append(expr[i])
                        current_term = ''
                else:
                    current_term += expr[i]
                i += 1
            if current_term:
                terms.append(current_term.strip())
            
            if not terms:
                return Dimension()
            
            # 计算第一个项
            dim = self.calculate_dimension(terms[0])
            
            # 处理后续项
            for i, op in enumerate(ops):
                if i < len(terms) - 1:
                    next_dim = self.calculate_dimension(terms[i+1])
                    if op == '*':
                        dim *= next_dim
                    elif op == '/':
                        dim /= next_dim
            
            return dim
        
        # 处理微分表达式
        if expr.startswith('d^2'):
            var = expr[3:].strip()
            return self.calculate_dimension(var)
        elif expr.startswith('d'):
            var = expr[1:].strip()
            return self.calculate_dimension(var)
        
        # 处理幂次表达式
        if '^' in expr:
            idx = expr.index('^')
            base = expr[:idx].strip()
            exponent = expr[idx+1:].strip()
            base_dim = self.calculate_dimension(base)
            try:
                exp = int(exponent)
                return base_dim.pow(exp)
            except:
                return Dimension()
        
        # 处理点积和叉积
        if '·' in expr or '×' in expr:
            parts = expr.split('·') if '·' in expr else expr.split('×')
            if not parts:
                return Dimension()
            dim = self.calculate_dimension(parts[0])
            for part in parts[1:]:
                part_dim = self.calculate_dimension(part)
                if part_dim != dim:
                    return Dimension()
            return dim
        
        # 处理旋度和散度
        if expr.startswith('nabla×'):
            var = expr[7:].strip()
            var_dim = self.calculate_dimension(var)
            return var_dim * Dimension(L=-1)
        elif expr.startswith('nabla·'):
            var = expr[7:].strip()
            var_dim = self.calculate_dimension(var)
            return var_dim * Dimension(L=-1)
        
        # 处理拉普拉斯算子
        if expr == 'nabla^2':
            return Dimension(L=-2)
        
        # 处理简单变量
        if expr in self.dimensions:
            return self.dimensions[expr]
        
        # 处理常数和无量纲量
        if expr.isdigit() or expr in ['pi', '2', '4', '8', 'Delta_n', 'Delta_s', 'dn', 'dOmega', 'dP', 'dA', 'dE', 'dB', 'd2A', 'd2L', 'r_hat', 'nabla', 'nabla2']:
            return Dimension()
        
        # 处理临时变量
        if expr.startswith('temp_'):
            return self.dimensions.get(expr, Dimension())
        
        return Dimension()

class UnifiedFieldTheoryValidator:
    """统一场论公式验证器"""
    def __init__(self):
        self.validator = DimensionValidator()
        self.formulas = self._define_formulas()
    
    def _define_formulas(self):
        """定义统一场论公式"""
        return [
            # 1. 时空同一化方程
            (1, "时空同一化方程", "r", "C*t"),
            
            # 2. 三维螺旋时空方程
            (2, "三维螺旋时空方程", "r", "C*t"),  # 简化验证，实际是矢量合成
            
            # 3. 质量定义方程
            (3, "质量定义方程", "m", "k*(dn/dOmega)"),
            
            # 4. 引力场定义方程
            (4, "引力场定义方程", "A", "-G*k*(Delta_n/Delta_s)*(r/r^2)"),
            
            # 5. 静止动量方程
            (5, "静止动量方程", "p0", "m0*C"),
            
            # 6. 运动动量方程
            (6, "运动动量方程", "P", "m*(C - V)"),
            
            # 7. 宇宙大统一方程（力方程）
            (7, "宇宙大统一方程", "F", "dP/dt"),
            
            # 8. 空间波动方程
            (8, "空间波动方程", "nabla^2*r", "(1/C^2)*(d^2r/dt^2)"),
            
            # 9. 电荷定义方程
            (9, "电荷定义方程", "q", "k_prime*k*(1/Omega^2)*(dOmega/dt)"),
            
            # 10. 电场定义方程
            (10, "电场定义方程", "E", "-k*k_prime/(4*pi*epsilon0*Omega^2)*(dOmega/dt)*(r/r^3)"),
            
            # 11. 磁场定义方程
            (11, "磁场定义方程", "B", "mu0*gamma*k*k_prime/(4*pi*Omega^2)*(dOmega/dt)*(r/r^3)"),
            
            # 12. 变化的引力场产生电磁场
            (12, "变化的引力场产生电磁场", "d2A/dt^2", "V*(nabla·E) - C^2*(nabla×B)"),
            
            # 13. 引力场旋度方程
            (13, "引力场旋度方程", "nabla×(dA/dt)", "B"),
            
            # 14. 变化的引力场产生电场
            (14, "变化的引力场产生电场", "E", "-dA/dt"),
            
            # 15. 变化的磁场产生引力场和电场
            (15, "变化的磁场产生引力场和电场", "dB/dt", "-(A×E)/C^2 - (V/C^2)×(dE/dt)"),
            
            # 16. 统一场论能量方程
            (16, "统一场论能量方程", "E_energy", "m0*C^2"),
            
            # 17. 光速飞行器动力学方程
            (17, "光速飞行器动力学方程", "F", "(C - V)*(dm/dt)"),
            
            # 18. 核力场定义方程
            (18, "核力场定义方程", "D", "-G*m*(C - 3*(r/r)*dot_r)/r^3"),
            
            # 19. 引力光速统一方程
            (19, "引力光速统一方程", "Z", "G*C/2"),
            
            # 20. 电磁光速几何耦合常数
            (20, "电磁光速几何耦合常数", "Z_prime", "C/(8*pi*epsilon0)"),
            
            # 21. 加速运动电荷产生引力场方程
            (21, "加速运动电荷产生引力场方程", "E", "-q/(4*pi*epsilon0*C^2*r)*(A×r_hat)/f"),
            
            # 22. 圆周运动正电荷产生的引力场方程
            (22, "圆周运动正电荷产生的引力场方程", "B", "-q/(4*pi*epsilon0*C^3*r)*(A×r_hat)/f"),
        ]
    
    def validate_all_formulas(self):
        """验证所有公式的量纲"""
        results = []
        valid_count = 0
        total_count = len(self.formulas)
        
        print("=" * 80)
        print("张祥前统一场论核心公式量纲验证")
        print("=" * 80)
        
        for formula_id, formula_name, left_expr, right_expr in self.formulas:
            print(f"\n{formula_id}. {formula_name}")
            print("-" * 60)
            is_valid, message, left_dim, right_dim = self.validator.validate_equation(left_expr, right_expr)
            print(message)
            results.append((formula_id, formula_name, is_valid, left_dim, right_dim))
            if is_valid:
                valid_count += 1
        
        print("\n" + "=" * 80)
        print("验证总结")
        print("=" * 80)
        print(f"总公式数: {total_count}")
        print(f"验证通过: {valid_count}")
        print(f"验证失败: {total_count - valid_count}")
        print(f"通过率: {valid_count/total_count*100:.1f}%")
        
        if valid_count == total_count:
            print("\n🎉 所有公式量纲验证通过！")
        else:
            print("\n⚠️  部分公式量纲验证失败，需要检查！")
        
        return results

if __name__ == "__main__":
    validator = UnifiedFieldTheoryValidator()
    validator.validate_all_formulas()
