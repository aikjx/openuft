# 简化的量纲分析脚本

"""
对修订版论文中的公式进行量纲分析，验证量纲闭合性
使用基本量纲幂次的方法，更准确可靠
"""

# 基本物理量的索引
L, M, T, I, K = 0, 1, 2, 3, 4

# 物理量的量纲（[长度, 质量, 时间, 电流, 温度]）
dimensions = {
    # 基本常数
    'c':      [1, 0, -1, 0, 0],  # 光速 L/T
    'G':      [3, -1, -2, 0, 0],  # 万有引力常数 L³/(M·T²)
    'h':      [2, 1, -1, 0, 0],  # 普朗克常数 M·L²/T
    'hbar':   [2, 1, -1, 0, 0],  # 约化普朗克常数 M·L²/T
    'k_B':    [2, 1, -2, 0, -1], # 玻尔兹曼常数 M·L²/(T²·K)
    'epsilon0': [-3, -1, 4, 2, 0], # 真空介电常数 I²·T⁴/(M·L³)
    'e':      [0, 0, 1, 1, 0],    # 元电荷 I·T
    
    # 变量
    'm':      [0, 1, 0, 0, 0],    # 质量 M
    'r':      [1, 0, 0, 0, 0],    # 半径 L
    'omega':  [0, 0, -1, 0, 0],   # 角速度 1/T
    'ω':      [0, 0, -1, 0, 0],   # 角速度 1/T
    'nu':     [0, 0, -1, 0, 0],   # 频率 1/T
    'ν':      [0, 0, -1, 0, 0],   # 频率 1/T
    'T':      [0, 0, 1, 0, 0],    # 周期 T
    'T_period': [0, 0, 1, 0, 0],  # 周期 T
    'a':      [1, 0, -2, 0, 0],   # 加速度 L/T²
    'L':      [2, 1, -1, 0, 0],   # 角动量 M·L²/T
    'L_ang':  [2, 1, -1, 0, 0],   # 角动量 M·L²/T
    'E':      [2, 1, -2, 0, 0],   # 能量 M·L²/T²
    'p':      [1, 1, -1, 0, 0],   # 动量 M·L/T
    'rho':    [-3, 1, 0, 0, 0],   # 密度 M/L³
    'ρ':      [-3, 1, 0, 0, 0],   # 密度 M/L³
    'k':      [-1, 0, 0, 0, 0],   # 曲率 1/L
    'Phi':    [2, 0, -2, 0, 0],   # 引力势 L²/T²
    'γ':      [0, 0, 0, 0, 0],    # 洛伦兹因子（无量纲）
    'gamma':  [0, 0, 0, 0, 0],    # 洛伦兹因子（无量纲）
    'R':      [-2, 0, 0, 0, 0],   # 时空曲率 1/L²
    'R_s':    [1, 0, 0, 0, 0],    # 史瓦西半径 L
    'T_H':    [0, 0, 0, 0, 1],    # 霍金温度 K
    'S_BH':   [2, 1, -2, 0, -1],  # 黑洞熵 M·L²/(T²·K)
    'H':      [0, 0, -1, 0, 0],   # 哈勃常数 1/T
    'Λ':      [-2, 0, 0, 0, 0],   # 宇宙学常数 1/L²
    'Lambda': [-2, 0, 0, 0, 0],   # 宇宙学常数 1/L²
    'alpha':  [0, 0, 0, 0, 0],    # 精细结构常数（无量纲）
    'α':      [0, 0, 0, 0, 0],    # 精细结构常数（无量纲）
    'rho_vac': [-3, 1, 0, 0, 0],  # 真空能密度 M/L³
    'P_tunnel': [0, 0, 0, 0, 0],  # 隧穿概率（无量纲）
    'delta_E': [2, 1, -2, 0, 0],  # 能量变化 M·L²/T²
    'Δ':      [0, 0, 0, 0, 0],    # 变化量（无量纲）
    'λ':      [1, 0, 0, 0, 0],    # 波长 L
    'A':      [2, 0, 0, 0, 0],    # 面积 L²
    'v':      [1, 0, -1, 0, 0],   # 速度 L/T
    'F':      [1, 1, -2, 0, 0],   # 力 M·L/T²
    'F_g':    [1, 1, -2, 0, 0],   # 引力 M·L/T²
    'F_e':    [1, 1, -2, 0, 0],   # 电磁力 M·L/T²
    'Φ':      [2, 0, -2, 0, 0],   # 引力势 L²/T²
    'epsilon0': [-3, -1, 4, 2, 0], # 真空介电常数 I²·T⁴/(M·L³)
    'ε0':     [-3, -1, 4, 2, 0],   # 真空介电常数 I²·T⁴/(M·L³)
    'ε₀':     [-3, -1, 4, 2, 0],   # 真空介电常数 I²·T⁴/(M·L³)
    
    # 其他
    'pi':     [0, 0, 0, 0, 0],    # π（无量纲）
    'π':      [0, 0, 0, 0, 0],    # π（无量纲）
    '1':      [0, 0, 0, 0, 0],    # 常数1（无量纲）
    '2':      [0, 0, 0, 0, 0],    # 常数2（无量纲）
    '3':      [0, 0, 0, 0, 0],    # 常数3（无量纲）
    '4':      [0, 0, 0, 0, 0],    # 常数4（无量纲）
    '8':      [0, 0, 0, 0, 0],    # 常数8（无量纲）
}

# 解析表达式的量纲
def parse_expression(expr):
    """解析表达式，返回其量纲"""
    # 移除空格
    expr = expr.replace(' ', '')
    
    # 处理常见函数和符号
    expr = expr.replace('π', 'pi')
    expr = expr.replace('Δ', 'delta')
    expr = expr.replace('d²', '')
    expr = expr.replace('dt²', 'T**2')
    expr = expr.replace('dr', 'r')
    expr = expr.replace('de', 'e')
    expr = expr.replace('c⁴', 'c**4')
    expr = expr.replace('c³', 'c**3')
    expr = expr.replace('c²', 'c**2')
    expr = expr.replace('ħ', 'hbar')
    expr = expr.replace('ε₀', 'epsilon0')
    expr = expr.replace('ε0', 'epsilon0')
    
    # 处理分数
    if '/' in expr:
        parts = expr.split('/')
        if len(parts) > 2:
            # 处理多个除号的情况，从左到右依次计算
            result = parse_expression(parts[0])
            for part in parts[1:]:
                result = add_dimensions(result, scale_dimensions(parse_expression(part), -1))
            return result
        else:
            numerator, denominator = parts
            return add_dimensions(parse_expression(numerator), 
                                scale_dimensions(parse_expression(denominator), -1))
    
    # 处理乘法
    if '*' in expr:
        terms = expr.split('*')
        result = [0, 0, 0, 0, 0]
        for term in terms:
            result = add_dimensions(result, parse_term(term))
        return result
    
    # 处理幂次
    if '**' in expr:
        base, power = expr.split('**')
        base_dim = parse_term(base)
        try:
            power = float(power)
            return scale_dimensions(base_dim, power)
        except:
            return [0, 0, 0, 0, 0]  # 无法解析的幂次，返回无量纲
    
    # 单个项
    return parse_term(expr)

def parse_term(term):
    """解析单个项的量纲"""
    # 处理开方
    if term.startswith('sqrt(') and term.endswith(')'):
        inside = term[5:-1]
        inside_dim = parse_expression(inside)
        return scale_dimensions(inside_dim, 0.5)
    
    # 查找已知量纲
    if term in dimensions:
        return dimensions[term]
    
    # 处理数字
    try:
        float(term)
        return [0, 0, 0, 0, 0]  # 数字是无量纲的
    except:
        pass
    
    # 处理其他情况
    # 尝试提取变量名
    import re
    var_match = re.match(r'([a-zA-Z_]+)', term)
    if var_match:
        var_name = var_match.group(1)
        if var_name in dimensions:
            return dimensions[var_name]
    
    return [0, 0, 0, 0, 0]  # 未知量，返回无量纲

def add_dimensions(dim1, dim2):
    """添加两个量纲"""
    return [d1 + d2 for d1, d2 in zip(dim1, dim2)]

def scale_dimensions(dim, factor):
    """缩放量纲"""
    return [d * factor for d in dim]

def analyze_formula(formula):
    """分析公式的量纲闭合性"""
    if '=' in formula:
        parts = formula.split('=')
        left = parts[0].strip()
        right = parts[1].strip()
        
        left_dim = parse_expression(left)
        right_dim = parse_expression(right)
        
        consistent = left_dim == right_dim
        
        return {
            'formula': formula,
            'left_side': left,
            'right_side': right,
            'left_dimension': left_dim,
            'right_dimension': right_dim,
            'consistent': consistent
        }
    else:
        dim = parse_expression(formula)
        return {
            'formula': formula,
            'dimension': dim
        }

# 分析所有核心公式
def analyze_all_formulas():
    from formulas_extraction import FormulaAnalyzer
    
    analyzer = FormulaAnalyzer()
    core_formulas = analyzer.core_formulas
    
    results = {}
    for category, formulas in core_formulas.items():
        category_results = {}
        for name, formula in formulas.items():
            # 处理多个等号的情况
            if '=' in formula:
                parts = formula.split('=')
                # 只分析第一个等式
                main_formula = f"{parts[0].strip()} = {parts[1].strip()}"
                category_results[name] = analyze_formula(main_formula)
            else:
                category_results[name] = analyze_formula(formula)
        results[category] = category_results
    return results

# 验证核心公式的量纲闭合性
def verify_dimensions():
    results = analyze_all_formulas()
    
    print("=== 量纲分析结果 ===")
    print(f"分析的公式总数: {sum(len(v) for v in results.values())}")
    
    inconsistent_count = 0
    inconsistent_formulas = []
    
    for category, formulas in results.items():
        print(f"\n{category}:")
        for name, result in formulas.items():
            if 'consistent' in result:
                status = "✓" if result['consistent'] else "✗"
                print(f"  {status} {name}: {result['formula']}")
                if not result['consistent']:
                    inconsistent_count += 1
                    inconsistent_formulas.append(f"{category} - {name}: {result['formula']}")
                    print(f"    左侧量纲: {result['left_dimension']}")
                    print(f"    右侧量纲: {result['right_dimension']}")
            else:
                print(f"  - {name}: {result['formula']}")
                print(f"    量纲: {result['dimension']}")
    
    print(f"\n=== 分析总结 ===")
    print(f"一致的公式: {sum(len(v) for v in results.values()) - inconsistent_count}")
    print(f"不一致的公式: {inconsistent_count}")
    
    if inconsistent_formulas:
        print("\n不一致的公式:")
        for formula in inconsistent_formulas:
            print(f"  - {formula}")
    
    return results

if __name__ == '__main__':
    verify_dimensions()
