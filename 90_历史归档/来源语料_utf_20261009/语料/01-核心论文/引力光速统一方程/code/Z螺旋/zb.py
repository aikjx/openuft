#!/usr/bin/env python3
"""
Z'常数验证工具 - 张祥前统一场论电磁常数验证
功能：计算和比较不同Z'表达式，验证与电磁常数的对称关系
作者：基于理论推导与物理常数验证
"""

import math
from scipy.constants import hbar, e, c, epsilon_0, alpha

def calculate_Z_prime_beta(beta=1.0):
    """通过对称关系计算Z'：1/(4πε₀) = β·(2Z'/c)"""
    Z_prime = c / (8 * math.pi * epsilon_0 * beta)
    return Z_prime

def calculate_beta_from_Z_prime(Z_prime_candidate):
    """从候选Z'值反推所需的β值"""
    beta = (1/(4*math.pi*epsilon_0)) / (2*Z_prime_candidate/c)
    return beta

def verify_Z_prime_expressions():
    """验证三种主要的Z'表达式"""
    results = []
    
    # 1. 用户原始候选：Z' = ħ/(2e²)
    Z1 = hbar / (2 * e**2)
    beta1 = calculate_beta_from_Z_prime(Z1)
    results.append({
        '表达式': r"Z' = \hbar/(2e^2)",
        'Z′值': Z1,
        '所需β': beta1,
        '备注': '用户原始候选，需极大β值'
    })
    
    # 2. 库仑映射：Z' = c/(8πε₀) [β=1]
    Z2 = calculate_Z_prime_beta(beta=1.0)
    beta2 = 1.0
    results.append({
        '表达式': r"Z' = c/(8\pi\varepsilon_0) [β=1]",
        'Z′值': Z2,
        '所需β': beta2,
        '备注': '自然对称，量纲自洽'
    })
    
    # 3. 精细结构常数形式：Z' = αħc²/(2e²)
    Z3 = alpha * hbar * c**2 / (2 * e**2)
    beta3 = calculate_beta_from_Z_prime(Z3)
    results.append({
        '表达式': r"Z' = \alpha\hbar c^2/(2e^2)",
        'Z′值': Z3,
        '所需β': beta3,
        '备注': '等价于库仑映射形式'
    })
    
    return results

def interactive_calculator():
    """交互式计算器：用户输入Z'或β进行计算"""
    print("\n" + "="*60)
    print("Z'常数交互验证工具")
    print("="*60)
    
    while True:
        print("\n选择计算模式：")
        print("1. 已知β值，计算Z'")
        print("2. 已知Z'候选值，计算所需β")
        print("3. 显示所有预设表达式结果")
        print("4. 退出")
        
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == '1':
            try:
                beta_input = float(input("请输入β值 (默认=1): ") or "1")
                Z_result = calculate_Z_prime_beta(beta_input)
                print(f"\n结果: Z' = {Z_result:.4e}")
                print(f"     = {Z_result:.4e} kg·m⁴·s⁻³·C⁻²")
                if beta_input == 1.0:
                    print("备注: 这是自然的对称关系 (β=1)")
            except ValueError:
                print("错误: 请输入有效的数字")
                
        elif choice == '2':
            try:
                Z_input = float(input("请输入Z'候选值: "))
                beta_result = calculate_beta_from_Z_prime(Z_input)
                print(f"\n结果: 所需β = {beta_result:.4e}")
                if abs(beta_result - 1.0) < 1e-6:
                    print("备注: 完美符合自然对称!")
                elif beta_result > 1e10:
                    print("备注: 需要极大的β值，可能不自然")
                elif beta_result < 1e-10:
                    print("备注: 需要极小的β值，可能不自然")
            except ValueError:
                print("错误: 请输入有效的数字")
                
        elif choice == '3':
            print("\n预设表达式验证结果:")
            print("-" * 80)
            results = verify_Z_prime_expressions()
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['表达式']}")
                print(f"   Z′ = {result['Z′值']:.4e}")
                print(f"   所需β = {result['所需β']:.4e}")
                print(f"   备注: {result['备注']}")
                if i < len(results):
                    print()
                    
        elif choice == '4':
            print("感谢使用Z'验证工具！")
            break
        else:
            print("无效选择，请重新输入")

def main():
    """主函数"""
    print("张祥前统一场论 - Z'常数验证工具")
    print("理论关系: 1/(4πε₀) = β·(2Z'/c)")
    print("推导得到: Z' = c/(8πε₀β)")
    print("="*50)
    
    # 显示基本常数
    print("基本常数参考值:")
    print(f"ħ = {hbar:.3e} J·s")
    print(f"e = {e:.3e} C")
    print(f"c = {c:.3e} m/s")
    print(f"ε₀ = {epsilon_0:.3e} F/m")
    print(f"α = {alpha:.7f}")
    print("="*50)
    
    # 运行交互式计算器
    interactive_calculator()

if __name__ == "__main__":
    main()
