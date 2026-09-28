import re

# 基本量纲定义
fundamental_units = {
    'length': 'L',      # 长度
    'mass': 'M',        # 质量
    'time': 'T',        # 时间
    'current': 'I',      # 电流
    'temperature': 'Θ',  # 温度
    'amount': 'N',       # 物质的量
    'luminosity': 'J'    # 发光强度
}

# 物理常数的量纲
constants_dimensions = {
    'c': {'length': 1, 'time': -1},  # 光速 [L/T]
    'G': {'length': 3, 'mass': -1, 'time': -2},  # 引力常数 [L^3/(M*T^2)]
    'h': {'length': 2, 'mass': 1, 'time': -1},  # 普朗克常数 [L^2*M/T]
    'hbar': {'length': 2, 'mass': 1, 'time': -1},  # 约化普朗克常数 [L^2*M/T]
    'epsilon0': {'length': -3, 'mass': -1, 'time': 4, 'current': 2},  # 真空介电常数 [L^-3*M^-1*T^4*I^2]
    'mu0': {'length': 1, 'mass': 1, 'time': -2, 'current': -2},  # 真空磁导率 [L*M*T^-2*I^-2]
    'e': {'current': 1, 'time': 1},  # 元电荷 [I*T]
    'alpha': {},  # 精细结构常数（无量纲）
    'k_B': {'length': 2, 'mass': 1, 'time': -2, 'temperature': -1},  # 玻尔兹曼常数 [L^2*M*T^-2*Θ^-1]
    'H': {'time': -1},  # 哈勃常数 [1/T]
}

# 变量的量纲
variables_dimensions = {
    'm': {'mass': 1},  # 质量 [M]
    'r': {'length': 1},  # 长度 [L]
    'omega': {'time': -1},  # 角速度 [1/T]
    'rho_vac': {'mass': 1, 'length': -1, 'time': -2},  # 能量密度 [M/(L*T^2)]
    't': {'time': 1},  # 时间 [T]
    'T_temp': {'temperature': 1},  # 温度 [Θ]
    'nu': {'time': -1},  # 频率 [1/T]
    'T': {'time': 1},  # 周期 [T]
    'v': {'length': 1, 'time': -1},  # 速度 [L/T]
    'gamma': {},  # 洛伦兹因子（无量纲）
    'N_plus': {},  # 数量（无量纲）
    'N_minus': {},  # 数量（无量纲）
}

# 提取方程
with open('d:\\a10\\aikjx\\code\\my_lib\\utf\\10-统一场论核心公式\\公式验证论文\\24-时空与物理常数归一化方程\\可转换的\\归一化方程转换4.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取所有方程
equations = re.findall(r'\$\$\\boxed\{(.*?)\}\$\$', content, re.DOTALL)

# 方程名称映射
equation_names = [
    '手性正反物质统一方程1',
    '手性正反物质统一方程2',
    '真空零点能归一化方程',
    '粒子质量谱量子化方程1',
    '粒子质量谱量子化方程2',
    '引力-电磁辐射统一方程1',
    '引力-电磁辐射统一方程2',
    '宇宙基本常数全归一化超恒等式',
    '宇宙正反物质不对称方程'
]

def analyze_dimension(expr):
    """分析表达式的量纲"""
    # 简化表达式，移除常数因子和LaTeX格式
    expr = expr.replace('4π', '').replace('8π', '').replace('3', '').replace('2', '').replace('π', '').replace('\n', '')
    expr = expr.replace('\\boxed', '').replace('{', '').replace('}', '')
    
    # 处理分数
    if '/' in expr:
        # 处理LaTeX分数格式
        if '}{' in expr:
            parts = expr.split('}{')
            if len(parts) == 2:
                numerator = parts[0].split('^')[-1] if '^' in parts[0] else parts[0]
                denominator = parts[1].split('^')[0] if '^' in parts[1] else parts[1]
            else:
                numerator, denominator = expr.split('/', 1)
        else:
            numerator, denominator = expr.split('/', 1)
        
        num_dim = analyze_term(numerator)
        den_dim = analyze_term(denominator)
        # 分母的量纲取倒数
        for key in den_dim:
            if key in num_dim:
                num_dim[key] -= den_dim[key]
            else:
                num_dim[key] = -den_dim[key]
        return num_dim
    else:
        return analyze_term(expr)

def analyze_term(term):
    """分析单个项的量纲"""
    dim = {}
    # 处理乘积项
    # 简单处理，只考虑基本变量和常数
    term = term.strip()
    
    # 处理常见的表达式
    if term == 'e_{\pm}' or term == 'm_{\pm}' or term == 'm':
        return variables_dimensions.get('m', {})
    elif term == 'rho_{vac}' or term == '\rho_{vac}':
        return variables_dimensions.get('rho_vac', {})
    elif term == 'm_n':
        return variables_dimensions.get('m', {})
    elif term == 'r_n':
        return variables_dimensions.get('r', {})
    elif term == 'v_g' or term == 'v_em' or term == 'c':
        return constants_dimensions.get('c', {})
    elif term == 'N_+/N_-':
        return {}  # 无量纲
    
    # 处理复合表达式
    # 简化处理：只提取关键变量和常数的量纲
    if 'c^7' in term:
        dim.update({'length': 7, 'time': -7})  # c^7
    if 'G^2' in term:
        dim.update({'length': -6, 'mass': 2, 'time': 4})  # G^-2
    if 'h' in term:
        dim.update({'length': -2, 'mass': -1, 'time': 1})  # h^-1
    if 'H^2' in term:
        dim.update({'time': -2})  # H^2
    if 'G' in term and 'G^2' not in term:
        dim.update({'length': -3, 'mass': 1, 'time': 2})  # G^-1
    
    return dim

def check_equation(equation):
    """检查方程两边的量纲是否一致"""
    if '=' in equation:
        sides = equation.split('=')
        left_dim = analyze_dimension(sides[0])
        right_dim = analyze_dimension(sides[1])
        return left_dim == right_dim, left_dim, right_dim
    else:
        # 单一表达式，检查是否无量纲（如果应该是无量纲的）
        dim = analyze_dimension(equation)
        return len(dim) == 0, dim, {}

# 分析所有方程
results = []
for i, equation in enumerate(equations):
    equation = equation.strip()
    is_valid, left_dim, right_dim = check_equation(equation)
    results.append({
        'name': equation_names[i] if i < len(equation_names) else f'方程{i+1}',
        'equation': equation,
        'is_valid': is_valid,
        'left_dim': left_dim,
        'right_dim': right_dim
    })

# 输出结果
print("方程量纲分析结果：")
print("=" * 80)
for result in results:
    print(f"方程：{result['name']}")
    print(f"表达式：{result['equation']}")
    print(f"量纲正确：{result['is_valid']}")
    if '=' in result['equation']:
        print(f"左边量纲：{result['left_dim']}")
        print(f"右边量纲：{result['right_dim']}")
    else:
        print(f"量纲：{result['left_dim']}")
    print("-" * 80)

# 标记需要移除的方程
invalid_equations = [result['name'] for result in results if not result['is_valid']]
print("需要移除的方程：")
print(invalid_equations)

# 保存结果
with open('dimension_analysis_results.txt', 'w', encoding='utf-8') as f:
    f.write("方程量纲分析结果：\n")
    f.write("=" * 80 + "\n")
    for result in results:
        f.write(f"方程：{result['name']}\n")
        f.write(f"表达式：{result['equation']}\n")
        f.write(f"量纲正确：{result['is_valid']}\n")
        if '=' in result['equation']:
            f.write(f"左边量纲：{result['left_dim']}\n")
            f.write(f"右边量纲：{result['right_dim']}\n")
        else:
            f.write(f"量纲：{result['left_dim']}\n")
        f.write("-" * 80 + "\n")
    f.write("需要移除的方程：\n")
    f.write('\n'.join(invalid_equations) + "\n")
