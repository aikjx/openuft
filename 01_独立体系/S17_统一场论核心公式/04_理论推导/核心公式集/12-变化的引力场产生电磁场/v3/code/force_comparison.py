import numpy as np

# 经典情况下引力与各力大小比较
def calculate_force_comparison():
    print("===== 10个经典情况下引力与各力大小比较 =====")
    print()
    
    # 基本物理常数
    G = 6.67430e-11       # 万有引力常数 (m³·kg⁻¹·s⁻²)
    c = 299792458         # 光速 (m/s)
    epsilon0 = 8.8541878128e-12  # 真空介电常数 (F/m)
    e = 1.602176634e-19   # 基本电荷 (C)
    m_e = 9.1093837015e-31  # 电子质量 (kg)
    m_p = 1.67262192369e-27  # 质子质量 (kg)
    h_bar = 1.054571817e-34  # 约化普朗克常数 (J·s)
    alpha = 1/137.035999084  # 精细结构常数
    
    # 强核力和弱核力的近似值
    # 强核力耦合常数
    g_s = 1.2              # 强核力耦合常数
    # 弱核力耦合常数
    g_w = 0.65             # 弱核力耦合常数
    
    # 场景定义
    scenarios = [
        {
            "name": "两个电子之间的引力与电磁力",
            "mass1": m_e,
            "mass2": m_e,
            "charge1": e,
            "charge2": e,
            "distance": 1e-10,  # 原子尺度
            "force_types": ["gravity", "electromagnetic"]
        },
        {
            "name": "两个质子之间的引力与电磁力",
            "mass1": m_p,
            "mass2": m_p,
            "charge1": e,
            "charge2": e,
            "distance": 1e-10,  # 原子尺度
            "force_types": ["gravity", "electromagnetic"]
        },
        {
            "name": "质子和电子之间的引力与电磁力",
            "mass1": m_p,
            "mass2": m_e,
            "charge1": e,
            "charge2": -e,
            "distance": 5.29177210903e-11,  # 氢原子玻尔半径
            "force_types": ["gravity", "electromagnetic"]
        },
        {
            "name": "地球和月球之间的引力",
            "mass1": 5.972e24,  # 地球质量
            "mass2": 7.342e22,  # 月球质量
            "charge1": 0,
            "charge2": 0,
            "distance": 3.844e8,  # 地月距离
            "force_types": ["gravity"]
        },
        {
            "name": "太阳和地球之间的引力",
            "mass1": 1.989e30,  # 太阳质量
            "mass2": 5.972e24,  # 地球质量
            "charge1": 0,
            "charge2": 0,
            "distance": 1.496e11,  # 日地距离
            "force_types": ["gravity"]
        },
        {
            "name": "原子核内质子间的强核力与电磁力",
            "mass1": m_p,
            "mass2": m_p,
            "charge1": e,
            "charge2": e,
            "distance": 1e-15,  # 核子尺度
            "force_types": ["gravity", "electromagnetic", "strong"]
        },
        {
            "name": "β衰变中的弱核力",
            "mass1": m_p,
            "mass2": m_e,
            "charge1": e,
            "charge2": -e,
            "distance": 1e-18,  # 弱相互作用尺度
            "force_types": ["gravity", "electromagnetic", "weak"]
        },
        {
            "name": "中子星表面的引力",
            "mass1": 1.4 * 1.989e30,  # 典型中子星质量
            "mass2": m_p,  # 单个质子
            "charge1": 0,
            "charge2": 0,
            "distance": 1e4,  # 中子星半径
            "force_types": ["gravity"]
        },
        {
            "name": "黑洞视界处的引力",
            "mass1": 10 * 1.989e30,  # 10倍太阳质量黑洞
            "mass2": m_p,  # 单个质子
            "charge1": 0,
            "charge2": 0,
            "distance": 29531,  # 史瓦西半径
            "force_types": ["gravity"]
        },
        {
            "name": "星系中心黑洞与恒星的引力",
            "mass1": 4e6 * 1.989e30,  # 400万倍太阳质量黑洞
            "mass2": 1.989e30,  # 太阳质量恒星
            "charge1": 0,
            "charge2": 0,
            "distance": 8e3 * 9.461e15,  # 8千光年
            "force_types": ["gravity"]
        }
    ]
    
    # 力的计算函数
    def calculate_gravitational_force(m1, m2, r):
        return G * m1 * m2 / r**2
    
    def calculate_electromagnetic_force(q1, q2, r):
        return (1/(4 * np.pi * epsilon0)) * abs(q1 * q2) / r**2
    
    def calculate_strong_force(r):
        # 强核力的近似计算（ Yukawa势）
        # 强核力的力程约为 1e-15 m
        lambda_s = 1e-15  # 强核力力程
        return (g_s**2 / r**2) * np.exp(-r / lambda_s)
    
    def calculate_weak_force(r):
        # 弱核力的近似计算（ Yukawa势）
        # 弱核力的力程约为 1e-18 m
        lambda_w = 1e-18  # 弱核力力程
        return (g_w**2 / r**2) * np.exp(-r / lambda_w)
    
    # 计算并打印结果
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print("-" * 60)
        
        m1 = scenario['mass1']
        m2 = scenario['mass2']
        q1 = scenario['charge1']
        q2 = scenario['charge2']
        r = scenario['distance']
        
        forces = {}
        
        if 'gravity' in scenario['force_types']:
            F_g = calculate_gravitational_force(m1, m2, r)
            forces['gravity'] = F_g
            print(f"  引力: {F_g:.2e} N")
        
        if 'electromagnetic' in scenario['force_types']:
            F_em = calculate_electromagnetic_force(q1, q2, r)
            forces['electromagnetic'] = F_em
            print(f"  电磁力: {F_em:.2e} N")
            if 'gravity' in forces:
                ratio = F_em / forces['gravity']
                print(f"  电磁力/引力: {ratio:.2e}")
        
        if 'strong' in scenario['force_types']:
            F_strong = calculate_strong_force(r)
            forces['strong'] = F_strong
            print(f"  强核力: {F_strong:.2e} N")
            if 'gravity' in forces:
                ratio = F_strong / forces['gravity']
                print(f"  强核力/引力: {ratio:.2e}")
            if 'electromagnetic' in forces:
                ratio = F_strong / forces['electromagnetic']
                print(f"  强核力/电磁力: {ratio:.2e}")
        
        if 'weak' in scenario['force_types']:
            F_weak = calculate_weak_force(r)
            forces['weak'] = F_weak
            print(f"  弱核力: {F_weak:.2e} N")
            if 'gravity' in forces:
                ratio = F_weak / forces['gravity']
                print(f"  弱核力/引力: {ratio:.2e}")
            if 'electromagnetic' in forces:
                ratio = F_weak / forces['electromagnetic']
                print(f"  弱核力/电磁力: {ratio:.2e}")
        
        # 打印主要力的比较
        if len(forces) > 1:
            main_force = max(forces, key=forces.get)
            main_force_value = forces[main_force]
            print(f"  主导力: {main_force} ({main_force_value:.2e} N)")
        
        print()
    
    # 总结
    print("===== 力的强度总结 =====")
    print()
    print("力的强度从大到小排序:")
    print("1. 强核力: ~10^-8 N (核子尺度)")
    print("2. 电磁力: ~10^-8 N (原子尺度) / ~10^2 N (宏观尺度)")
    print("3. 弱核力: ~10^-12 N (弱相互作用尺度)")
    print("4. 引力: ~10^-47 N (微观尺度) / ~10^20 N (天体尺度)")
    print()
    print("关键结论:")
    print("- 微观尺度: 强核力和电磁力主导，引力可忽略")
    print("- 宏观尺度: 电磁力和引力主导")
    print("- 天体尺度: 引力主导")
    print("- 引力虽然最弱，但在大质量物体和长距离上起主导作用")

if __name__ == "__main__":
    calculate_force_comparison()
