#!/usr/bin/env python3
"""
量纲分析脚本：统一场论核心方程的量纲一致性验证

验证以下核心方程的量纲一致性：
1. 磁矢势方程: ∇×A = B/f
2. 电场方程: E = -f(dA/dt)
3. 场转化方程: ∂²A/∂t² = (v/f)(∇·E) - (c²/f)(∇×B)

使用国际单位制（SI）进行量纲分析
"""

# 定义量纲符号
# L: 长度, M: 质量, T: 时间, I: 电流

# 基础物理量的量纲
dimensions = {
    'A': {'L': 1, 'M': 1, 'T': -2, 'I': -1},  # 磁矢势，单位：T·m 或 N·s/(C·m)
    'B': {'L': 0, 'M': 1, 'T': -2, 'I': -1},  # 磁感应强度，单位：T
    'E': {'L': 1, 'M': 1, 'T': -3, 'I': -1},  # 电场强度，单位：V/m 或 N/C
    'f': {'L': 0, 'M': 0, 'T': 0, 'I': 0},    # 耦合系数，无量纲
    'v': {'L': 1, 'T': -1},                    # 速度，单位：m/s
    'c': {'L': 1, 'T': -1},                    # 光速，单位：m/s
    'nabla': {'L': -1},                        # 梯度算符，单位：1/m
    'dt': {'T': -1},                           # 时间导数，单位：1/s
    'dt2': {'T': -2},                          # 二阶时间导数，单位：1/s²
}

# 计算量纲的函数
def calculate_dimension(expression, dims):
    """计算表达式的量纲
    
    参数：
        expression: 表达式字符串
        dims: 基础量纲字典
    
    返回：
        计算得到的量纲字典
    """
    # 简化版量纲计算，仅处理基本运算
    # 这里我们手动计算每个方程的量纲
    pass

# 验证磁矢势方程: ∇×A = B/f
def validate_magnetic_vector_potential_equation():
    print("=== 磁矢势方程: ∇×A = B/f ===")
    
    # 左边：∇×A
    left = {}
    for key in dimensions['nabla']:
        left[key] = dimensions['nabla'][key]
    for key in dimensions['A']:
        if key in left:
            left[key] += dimensions['A'][key]
        else:
            left[key] = dimensions['A'][key]
    
    print("左边 (∇×A) 量纲:", left)
    
    # 右边：B/f
    right = {}
    for key in dimensions['B']:
        right[key] = dimensions['B'][key]
    # f 无量纲，不影响量纲
    
    print("右边 (B/f) 量纲:", right)
    
    # 验证量纲一致性
    if left == right:
        print("✅ 量纲一致！")
    else:
        print("❌ 量纲不一致！")
    
    print()

# 验证电场方程: E = -f(dA/dt)
def validate_electric_field_equation():
    print("=== 电场方程: E = -f(dA/dt) ===")
    
    # 左边：E
    left = dimensions['E'].copy()
    print("左边 (E) 量纲:", left)
    
    # 右边：-f(dA/dt)
    right = {}
    for key in dimensions['A']:
        right[key] = dimensions['A'][key]
    right['T'] += dimensions['dt']['T']  # 添加时间导数的量纲
    # f 无量纲，不影响量纲
    
    print("右边 (f(dA/dt)) 量纲:", right)
    
    # 验证量纲一致性
    if left == right:
        print("✅ 量纲一致！")
    else:
        print("❌ 量纲不一致！")
    
    print()

# 验证场转化方程: ∂²A/∂t² = (v/f)(∇·E) - (c²/f)(∇×B)
def validate_field_transformation_equation():
    print("=== 场转化方程: ∂²A/∂t² = (v/f)(∇·E) - (c²/f)(∇×B) ===")
    
    # 左边：∂²A/∂t²
    left = {}
    for key in dimensions['A']:
        left[key] = dimensions['A'][key]
    left['T'] += dimensions['dt2']['T']  # 添加二阶时间导数的量纲
    
    print("左边 (∂²A/∂t²) 量纲:", left)
    
    # 右边第一项：(v/f)(∇·E)
    right1 = {}
    for key in dimensions['v']:
        right1[key] = dimensions['v'][key]
    for key in dimensions['nabla']:
        right1[key] += dimensions['nabla'][key]
    for key in dimensions['E']:
        if key in right1:
            right1[key] += dimensions['E'][key]
        else:
            right1[key] = dimensions['E'][key]
    # f 无量纲，不影响量纲
    
    print("右边第一项 ((v/f)(∇·E)) 量纲:", right1)
    
    # 右边第二项：(c²/f)(∇×B)
    right2 = {}
    for key in dimensions['c']:
        right2[key] = 2 * dimensions['c'][key]  # c²
    for key in dimensions['nabla']:
        right2[key] += dimensions['nabla'][key]
    for key in dimensions['B']:
        if key in right2:
            right2[key] += dimensions['B'][key]
        else:
            right2[key] = dimensions['B'][key]
    # f 无量纲，不影响量纲
    
    print("右边第二项 ((c²/f)(∇×B)) 量纲:", right2)
    
    # 验证量纲一致性
    if left == right1 == right2:
        print("✅ 量纲一致！")
    else:
        print("❌ 量纲不一致！")
    
    print()

# 验证角速度普适公式: ω = √(2Z M / r³)
def validate_angular_velocity_formula():
    print("=== 角速度普适公式: ω = √(2Z M / r³) ===")
    
    # 定义额外量纲
    dims_extra = {
        'ω': {'T': -1},            # 角速度，单位：rad/s
        'Z': {'L': 4, 'M': -1, 'T': -3},  # 核心常数，单位：N·m³/(kg·s)
        'M': {'M': 1},              # 质量，单位：kg
        'r': {'L': 1},              # 半径，单位：m
        'G': {'L': 3, 'M': -1, 'T': -2},  # 万有引力常数，单位：m³/(kg·s²)
    }
    
    # 左边：ω
    left = dims_extra['ω'].copy()
    print("左边 (ω) 量纲:", left)
    
    # 右边：√(2Z M / r³)
    # 先计算根号内的量纲
    inside = {}
    for key in dims_extra['Z']:
        inside[key] = dims_extra['Z'][key]
    for key in dims_extra['M']:
        if key in inside:
            inside[key] += dims_extra['M'][key]
        else:
            inside[key] = dims_extra['M'][key]
    inside['L'] -= 3 * dims_extra['r']['L']  # 除以 r³
    
    # 开平方根
    right = {}
    for key, value in inside.items():
        right[key] = value / 2
    
    print("右边 (√(2Z M / r³)) 量纲:", right)
    
    # 验证量纲一致性
    if left == right:
        print("✅ 量纲一致！")
    else:
        print("❌ 量纲不一致！")
    
    # 验证修正后的公式: ω = √(G M / r³)
    print("\n=== 修正后的角速度公式: ω = √(G M / r³) ===")
    
    # 计算修正后公式的量纲
    inside_corrected = {}
    for key in dims_extra['G']:
        inside_corrected[key] = dims_extra['G'][key]
    for key in dims_extra['M']:
        if key in inside_corrected:
            inside_corrected[key] += dims_extra['M'][key]
        else:
            inside_corrected[key] = dims_extra['M'][key]
    inside_corrected['L'] -= 3 * dims_extra['r']['L']  # 除以 r³
    
    # 开平方根
    right_corrected = {}
    for key, value in inside_corrected.items():
        right_corrected[key] = value / 2
    
    print("右边 (√(G M / r³)) 量纲:", right_corrected)
    
    # 验证量纲一致性
    # 比较时忽略键的顺序，只比较值
    left_clean = {k: v for k, v in left.items() if v != 0}
    right_clean = {k: v for k, v in right_corrected.items() if v != 0}
    
    if left_clean == right_clean:
        print("✅ 量纲一致！")
    else:
        print("❌ 量纲不一致！")
    
    # 打印详细比较
    print(f"左边（简化）: {left_clean}")
    print(f"右边（简化）: {right_clean}")
    
    print()


# 主函数
if __name__ == "__main__":
    print("统一场论核心方程的量纲分析\n")
    
    validate_magnetic_vector_potential_equation()
    validate_electric_field_equation()
    validate_field_transformation_equation()
    validate_angular_velocity_formula()
    
    print("=== 量纲分析完成 ===")
