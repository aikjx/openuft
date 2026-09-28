# 量纲分析脚本

"""
对修订版论文中的公式进行量纲分析，验证量纲闭合性
"""

import re
from sympy import symbols, simplify

# 基本物理量的量纲
dimensions = {
    'L': 'L',      # 长度
    'M': 'M',      # 质量
    'T': 'T',      # 时间
    'I': 'I',      # 电流
    'K': 'K'       # 热力学温度
}

# 导出物理量的量纲
derived_dimensions = {
    'c': 'L/T',        # 光速
    'G': 'L^3/(M*T^2)',  # 万有引力常数
    'h': 'M*L^2/T',    # 普朗克常数
    'hbar': 'M*L^2/T', # 约化普朗克常数
    'k_B': 'M*L^2/(T^2*K)',  # 玻尔兹曼常数
    'epsilon0': 'I^2*T^4/(M*L^3)',  # 真空介电常数
    'e': 'I*T',        # 元电荷
    'm': 'M',          # 质量
    'r': 'L',          # 半径
    'omega': '1/T',     # 角速度
    'nu': '1/T',        # 频率
    'T_period': 'T',    # 周期
    'a': 'L/T^2',       # 加速度
    'L_ang': 'M*L^2/T', # 角动量
    'E': 'M*L^2/T^2',   # 能量
    'p': 'M*L/T',       # 动量
    'rho': 'M/L^3',     # 密度
    'k': '1/L',         # 曲率
    'Phi': 'L^2/T^2',   # 引力势
    'gamma': '1',       # 洛伦兹因子（无量纲）
    'R': '1/L^2',       # 时空曲率
    'R_s': 'L',         # 史瓦西半径
    'T_H': 'K',         # 霍金温度
    'S_BH': 'M*L^2/(T^2*K)',  # 黑洞熵
    'H': '1/T',         # 哈勃常数
    'Lambda': '1/L^2',   # 宇宙学常数
    'alpha': '1',        # 精细结构常数（无量纲）
    'rho_vac': 'M/L^3',  # 真空能密度
    'P_tunnel': '1',     # 隧穿概率（无量纲）
    'delta_E': 'M*L^2/T^2'  # 能量变化
}

# 替换公式中的符号为量纲
def replace_symbols_with_dimensions(formula):
    # 替换常见符号
    formula = formula.replace('π', '1')  # π是无量纲的
    formula = formula.replace('Δ', '')   # 忽略Δ符号
    formula = formula.replace('d²', '')  # 忽略二阶导数符号
    formula = formula.replace('dt²', 'T^2')
    formula = formula.replace('dr', 'L')
    formula = formula.replace('de', 'I*T')
    
    # 替换物理量符号
    for symbol, dim in derived_dimensions.items():
        # 确保只替换完整的符号
        formula = re.sub(rf'\\b{symbol}\\b', dim, formula)
    
    # 替换基本量纲
    for symbol, dim in dimensions.items():
        formula = re.sub(rf'\\b{symbol}\\b', dim, formula)
    
    return formula

# 计算表达式的量纲
def calculate_dimension(expression):
    # 处理幂次
    expression = expression.replace('^', '**')
    # 处理开方
    expression = expression.replace('sqrt', '**(1/2)')
    # 处理分数
    # 这里不直接替换，让sympy处理分数
    
    try:
        # 创建符号
        L, M, T, I, K = symbols('L M T I K')
        # 替换表达式中的量纲符号
        expr = expression
        # 计算表达式
        result = eval(expr)
        # 简化结果
        simplified = simplify(result)
        return str(simplified)
    except Exception as e:
        return f"错误: {str(e)}"

# 分析公式的量纲闭合性
def analyze_formula(formula):
    # 处理等号
    if '=' in formula:
        parts = formula.split('=')
        left = parts[0].strip()
        right = parts[1].strip()
        
        # 替换符号为量纲
        left_dim = replace_symbols_with_dimensions(left)
        right_dim = replace_symbols_with_dimensions(right)
        
        # 计算量纲
        left_result = calculate_dimension(left_dim)
        right_result = calculate_dimension(right_dim)
        
        # 检查量纲是否一致
        is_consistent = left_result == right_result and '错误' not in left_result and '错误' not in right_result
        
        return {
            'formula': formula,
            'left_side': left,
            'right_side': right,
            'left_dimension': left_dim,
            'right_dimension': right_dim,
            'left_result': left_result,
            'right_result': right_result,
            'consistent': is_consistent
        }
    else:
        # 对于没有等号的公式，只计算量纲
        dim = replace_symbols_with_dimensions(formula)
        result = calculate_dimension(dim)
        return {
            'formula': formula,
            'dimension': dim,
            'result': result
        }

# 分析所有核心公式
def analyze_all_formulas():
    from formulas_extraction import CORE_FORMULAS
    
    results = {}
    for category, formulas in CORE_FORMULAS.items():
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
                    print(f"    左侧量纲: {result['left_result']}")
                    print(f"    右侧量纲: {result['right_result']}")
            else:
                print(f"  - {name}: {result['formula']}")
                print(f"    量纲: {result['result']}")
    
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
