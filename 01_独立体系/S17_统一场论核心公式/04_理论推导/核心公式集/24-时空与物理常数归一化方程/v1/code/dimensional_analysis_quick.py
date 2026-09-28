# 快速量纲分析脚本

"""
快速验证修订版论文中的核心公式量纲闭合性
"""

# 基本物理量的索引
L, M, T, I, K = 0, 1, 2, 3, 4

# 物理量的量纲（[长度, 质量, 时间, 电流, 温度]）
dim_map = {
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
    'ω':      [0, 0, -1, 0, 0],   # 角速度 1/T
    'ν':      [0, 0, -1, 0, 0],   # 频率 1/T
    'T':      [0, 0, 1, 0, 0],    # 周期 T
    'a':      [1, 0, -2, 0, 0],   # 加速度 L/T²
    'L':      [2, 1, -1, 0, 0],   # 角动量 M·L²/T
    'E':      [2, 1, -2, 0, 0],   # 能量 M·L²/T²
    'p':      [1, 1, -1, 0, 0],   # 动量 M·L/T
    'ρ':      [-3, 1, 0, 0, 0],   # 密度 M/L³
    'k':      [-1, 0, 0, 0, 0],   # 曲率 1/L
    'Φ':      [2, 0, -2, 0, 0],   # 引力势 L²/T²
    'γ':      [0, 0, 0, 0, 0],    # 洛伦兹因子（无量纲）
    'R':      [-2, 0, 0, 0, 0],   # 时空曲率 1/L²
    'R_s':    [1, 0, 0, 0, 0],    # 史瓦西半径 L
    'T_H':    [0, 0, 0, 0, 1],    # 霍金温度 K
    'S_BH':   [2, 1, -2, 0, -1],  # 黑洞熵 M·L²/(T²·K)
    'H':      [0, 0, -1, 0, 0],   # 哈勃常数 1/T
    'Λ':      [-2, 0, 0, 0, 0],   # 宇宙学常数 1/L²
    'α':      [0, 0, 0, 0, 0],    # 精细结构常数（无量纲）
    'ρ_vac':  [-3, 1, 0, 0, 0],  # 真空能密度 M/L³
    'F':      [1, 1, -2, 0, 0],   # 力 M·L/T²
    'F_g':    [1, 1, -2, 0, 0],   # 引力 M·L/T²
    'F_e':    [1, 1, -2, 0, 0],   # 电磁力 M·L/T²
    'λ':      [1, 0, 0, 0, 0],    # 波长 L
    'A':      [2, 0, 0, 0, 0],    # 面积 L²
    'v':      [1, 0, -1, 0, 0],   # 速度 L/T
    'ε₀':     [-3, -1, 4, 2, 0],   # 真空介电常数 I²·T⁴/(M·L³)
    
    # 数字（无量纲）
    '1':      [0, 0, 0, 0, 0],
    '2':      [0, 0, 0, 0, 0],
    '3':      [0, 0, 0, 0, 0],
    '4':      [0, 0, 0, 0, 0],
    '8':      [0, 0, 0, 0, 0],
    'π':      [0, 0, 0, 0, 0],
}

# 解析表达式的量纲
def get_dim(expr):
    """快速解析表达式的量纲"""
    expr = expr.replace(' ', '')
    expr = expr.replace('²', '**2')
    expr = expr.replace('³', '**3')
    expr = expr.replace('⁴', '**4')
    expr = expr.replace('⁷', '**7')
    expr = expr.replace('ħ', 'hbar')
    expr = expr.replace('ε₀', 'epsilon0')
    
    # 处理分数
    if '/' in expr:
        num, den = expr.split('/')
        return add_dims(get_dim(num), scale_dim(get_dim(den), -1))
    
    # 处理乘法
    if '*' in expr:
        terms = expr.split('*')
        dim = [0, 0, 0, 0, 0]
        for term in terms:
            dim = add_dims(dim, get_dim(term))
        return dim
    
    # 处理幂次
    if '**' in expr:
        base, power = expr.split('**')
        dim = get_dim(base)
        try:
            power = float(power)
            return scale_dim(dim, power)
        except:
            return [0, 0, 0, 0, 0]
    
    # 处理开方
    if expr.startswith('sqrt(') and expr.endswith(')'):
        inside = expr[5:-1]
        dim = get_dim(inside)
        return scale_dim(dim, 0.5)
    
    # 直接查找
    if expr in dim_map:
        return dim_map[expr]
    
    # 处理变量名
    import re
    match = re.match(r'([a-zA-Z_ωνγΛαρε₀]+)', expr)
    if match:
        var = match.group(1)
        if var in dim_map:
            return dim_map[var]
    
    return [0, 0, 0, 0, 0]

def add_dims(d1, d2):
    """添加两个量纲"""
    return [a+b for a,b in zip(d1, d2)]

def scale_dim(d, factor):
    """缩放量纲"""
    return [a*factor for a in d]

def check_formula(formula):
    """检查公式的量纲闭合性"""
    if '=' in formula:
        left, right = formula.split('=')
        left_dim = get_dim(left.strip())
        right_dim = get_dim(right.strip())
        return left_dim == right_dim
    return True

# 核心公式验证
core_formulas = {
    '第一性原理': [
        'ωr = c',
        'T = 2π/ω',
        'ν = 1/T'
    ],
    '源头归一化关联式': [
        'm = c²r/G',
        'hν = mc²',
        '4π²r³c²/(GT²hν) = 1'
    ],
    '双隐含量': [
        'ω = c/r',
        'm = c²r/G',
        'm = ω²r³/G'
    ],
    '核心恒等式': [
        'mω²rc²/(Ghν) = 1',
        'ωr = c',
        'Gm/(c²r) = 1'
    ]
}

# 验证核心公式
def verify_core_formulas():
    print("=== 核心公式量纲验证 ===")
    total = 0
    passed = 0
    
    for category, formulas in core_formulas.items():
        print(f"\n{category}:")
        for formula in formulas:
            total += 1
            result = check_formula(formula)
            status = "✓" if result else "✗"
            print(f"  {status} {formula}")
            if result:
                passed += 1
    
    print(f"\n=== 验证结果 ===")
    print(f"总公式数: {total}")
    print(f"通过验证: {passed}")
    print(f"验证通过率: {passed/total*100:.1f}%")

if __name__ == '__main__':
    verify_core_formulas()
