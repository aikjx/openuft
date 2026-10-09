# 张祥前统一场论公式量纲验证代码
# 验证公式量纲的一致性和正确性

import re
from dimension_analysis_data import formulas_data, physical_constants, coupling_constants

class DimensionAnalyzer:
    def __init__(self):
        self.base_dimensions = ['L', 'M', 'T', 'Q', 'I']
    
    def parse_dimension(self, dim_str):
        """解析量纲字符串为字典形式"""
        if dim_str == '1':
            return {dim: 0 for dim in self.base_dimensions}
        
        # 处理形如 'L T^-1' 的量纲表达式
        dim_parts = dim_str.split()
        dim_dict = {dim: 0 for dim in self.base_dimensions}
        
        for part in dim_parts:
            # 匹配基本量纲和指数
            match = re.match(r'([LMTQI])(?:\^(-?\d+))?', part)
            if match:
                dim, exp = match.groups()
                exp = int(exp) if exp else 1
                dim_dict[dim] = exp
        
        return dim_dict
    
    def multiply_dimensions(self, dims1, dims2):
        """计算两个量纲的乘积"""
        result = {}
        for dim in self.base_dimensions:
            result[dim] = dims1.get(dim, 0) + dims2.get(dim, 0)
        return result
    
    def divide_dimensions(self, dims1, dims2):
        """计算两个量纲的商"""
        result = {}
        for dim in self.base_dimensions:
            result[dim] = dims1.get(dim, 0) - dims2.get(dim, 0)
        return result
    
    def format_dimension(self, dim_dict):
        """将量纲字典格式化为字符串"""
        parts = []
        for dim in self.base_dimensions:
            exp = dim_dict.get(dim, 0)
            if exp != 0:
                if exp == 1:
                    parts.append(dim)
                else:
                    parts.append(f"{dim}^{exp}")
        
        if not parts:
            return '1'
        return ' '.join(parts)
    
    def analyze_formula(self, formula):
        """分析单个公式的量纲一致性"""
        formula_id = formula['id']
        formula_name = formula['name']
        expected_dim = formula['dimension']
        variables = formula['variables']
        
        print(f"\n=== 分析公式 {formula_id}: {formula_name} ===")
        print(f"预期量纲: {expected_dim}")
        
        # 解析预期量纲
        expected_dim_dict = self.parse_dimension(expected_dim)
        
        # 分析变量量纲
        variable_dims = {}
        for var, dim_str in variables.items():
            var_dim = self.parse_dimension(dim_str)
            variable_dims[var] = var_dim
            print(f"  {var}: {dim_str}")
        
        # 根据公式类型分析量纲一致性
        # 这里我们根据公式的结构进行不同的分析
        if formula_id == 1:  # 时空同一化方程
            # 验证 vec{r} = vec{c}t 的量纲
            c_dim = variable_dims['vec{c}']
            t_dim = variable_dims['t']
            calculated_dim = self.multiply_dimensions(c_dim, t_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (vec{{c}} * t): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 2:  # 三维螺旋时空方程
            # 验证 vec{r}(t) = rcosωt · vec{i} + rsinωt · vec{j} + ht · vec{k} 的量纲
            r_dim = variable_dims['r']
            h_dim = variable_dims['h']
            t_dim = variable_dims['t']
            # 验证 ht 的量纲（与r的量纲应一致）
            ht_dim = self.multiply_dimensions(h_dim, t_dim)
            ht_dim_str = self.format_dimension(ht_dim)
            print(f"  计算量纲 (h * t): {ht_dim_str}")
            
            if ht_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 3:  # 质量定义方程
            # 验证 m = k * dn/dΩ
            k_dim = variable_dims['k']
            dn_dΩ_dim = variable_dims['dn/dΩ']
            calculated_dim = self.multiply_dimensions(k_dim, dn_dΩ_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (k * dn/dΩ): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 4:  # 引力场定义方程
            # 验证 vec{A} = -GkΔn/Δs vec{r}/r^2
            G_dim = self.parse_dimension('L^3 M^-1 T^-2')
            k_dim = variable_dims['k']
            delta_n_delta_s_dim = variable_dims['Δn/Δs']
            vec_r_r2_dim = variable_dims['vec{r}/r^2']
            
            # 计算分子量纲: G * k * Δn/Δs * vec{r}/r^2
            temp1 = self.multiply_dimensions(G_dim, k_dim)
            temp2 = self.multiply_dimensions(temp1, delta_n_delta_s_dim)
            calculated_dim = self.multiply_dimensions(temp2, vec_r_r2_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (G * k * Δn/Δs * vec{{r}}/r^2): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id in [5, 6]:  # 动量方程
            # 验证动量 = 质量 * 速度
            m_dim = variable_dims.get('m_0', variable_dims.get('m'))
            v_dim = variable_dims.get('vec{c}_0', variable_dims.get('vec{c}'))
            calculated_dim = self.multiply_dimensions(m_dim, v_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (质量 * 速度): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 7:  # 力方程
            # 验证力 = dP/dt
            P_dim = self.parse_dimension('M L T^-1')
            t_dim = self.parse_dimension('T')
            calculated_dim = self.divide_dimensions(P_dim, t_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (dP/dt): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 8:  # 空间波动方程
            # 验证 ∇²L = 1/c² ∂²L/∂t²
            # 左侧: ∇²L 的量纲是 L^-1
            # 右侧: 1/c² * ∂²L/∂t² 的量纲是 (T² L^-2) * (L T^-2) = L^-1
            left_dim = self.parse_dimension('L^-1')
            c_squared_dim = self.parse_dimension('L^2 T^-2')
            d2L_dt2_dim = variable_dims['∂²L/∂t²']
            
            right_dim = self.multiply_dimensions(self.divide_dimensions(self.parse_dimension('1'), c_squared_dim), d2L_dt2_dim)
            right_dim_str = self.format_dimension(right_dim)
            print(f"  左侧量纲 (∇²L): L^-1")
            print(f"  右侧量纲 (1/c² * ∂²L/∂t²): {right_dim_str}")
            
            if left_dim == right_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 9:  # 电荷定义方程
            # 验证 q = k' k 1/Ω² dΩ/dt
            k_prime_dim = variable_dims['k\'']
            k_dim = variable_dims['k']
            one_over_omega2_dim = variable_dims['1/Ω²']
            domega_dt_dim = variable_dims['dΩ/dt']
            
            temp1 = self.multiply_dimensions(k_prime_dim, k_dim)
            temp2 = self.multiply_dimensions(temp1, one_over_omega2_dim)
            calculated_dim = self.multiply_dimensions(temp2, domega_dt_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (k' * k * 1/Ω² * dΩ/dt): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 10:  # 电场定义方程
            # 验证 vec{E} = -kk'/(4πε₀Ω²) dΩ/dt vec{r}/r³
            k_dim = variable_dims['k']
            k_prime_dim = variable_dims['k\'']
            one_over_epsilon0_dim = variable_dims['1/ε₀']
            one_over_omega2_dim = self.parse_dimension('1')  # 无量纲
            domega_dt_dim = variable_dims['dΩ/dt']
            vec_r_r3_dim = variable_dims['vec{r}/r³']
            
            temp1 = self.multiply_dimensions(k_dim, k_prime_dim)
            temp2 = self.multiply_dimensions(temp1, one_over_epsilon0_dim)
            temp3 = self.multiply_dimensions(temp2, one_over_omega2_dim)
            temp4 = self.multiply_dimensions(temp3, domega_dt_dim)
            calculated_dim = self.multiply_dimensions(temp4, vec_r_r3_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (k * k' * 1/ε₀ * 1/Ω² * dΩ/dt * vec{{r}}/r³): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 11:  # 磁场定义方程
            # 验证 vec{B} = μ₀ γ k k'/(4π Ω²) dΩ/dt * vector_term / denominator
            mu0_dim = self.parse_dimension('M L I^-2 T^-2')
            gamma_dim = self.parse_dimension('1')  # 无量纲
            k_dim = variable_dims['k']
            k_prime_dim = variable_dims['k\'']
            one_over_omega2_dim = self.parse_dimension('1')  # 无量纲
            domega_dt_dim = variable_dims['dΩ/dt']
            vector_term_dim = variable_dims['vector_term']
            denominator_dim = variable_dims['denominator']
            
            temp1 = self.multiply_dimensions(mu0_dim, gamma_dim)
            temp2 = self.multiply_dimensions(temp1, k_dim)
            temp3 = self.multiply_dimensions(temp2, k_prime_dim)
            temp4 = self.multiply_dimensions(temp3, one_over_omega2_dim)
            temp5 = self.multiply_dimensions(temp4, domega_dt_dim)
            temp6 = self.multiply_dimensions(temp5, vector_term_dim)
            calculated_dim = self.divide_dimensions(temp6, denominator_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            print(f"  计算量纲 (μ₀ * γ * k * k' * 1/Ω² * dΩ/dt * vector_term / denominator): {calculated_dim_str}")
            
            # 修正磁场定义方程的量纲分析
            # 问题：当前计算结果为 L^-1 M T^-1 I^-1，预期为 M I^-1 T^-2
            # 解决方案：调整k'的量纲定义，添加时间因子
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                print("  建议：调整k'的量纲定义为 I T^3 M^-1 以确保量纲一致")
                return False
                
        elif formula_id == 12:  # 变化的引力场产生电磁场
            # 验证 ∂³vec{A}/∂t³ = vec{v}/f (∇·vec{E}) - c²/f (∇×vec{B})
            left_dim = variable_dims['∂³vec{A}/∂t³']
            
            # 计算右侧第一项: vec{v}/f * (∇·vec{E})
            v_dim = variable_dims['vec{v}']
            f_dim = self.parse_dimension('M I^-1')
            div_E_dim = variable_dims['∇·vec{E}']
            
            term1_dim = self.multiply_dimensions(self.divide_dimensions(v_dim, f_dim), div_E_dim)
            
            # 计算右侧第二项: c²/f * (∇×vec{B})
            c2_dim = variable_dims['c²']
            curl_B_dim = variable_dims['∇×vec{B}']
            
            term2_dim = self.multiply_dimensions(self.divide_dimensions(c2_dim, f_dim), curl_B_dim)
            
            print(f"  左侧量纲 (∂³vec{{A}}/∂t³): {self.format_dimension(left_dim)}")
            print(f"  右侧第一项量纲 (vec{{v}}/f * (∇·vec{{E}})): {self.format_dimension(term1_dim)}")
            print(f"  右侧第二项量纲 (c²/f * (∇×vec{{B}})): {self.format_dimension(term2_dim)}")
            
            # 修正变化的引力场产生电磁场方程的量纲分析
            # 问题：右侧第一项量纲为 L T^-4，左侧和右侧第二项量纲为 L T^-5
            # 解决方案：调整f的量纲定义，添加时间因子
            if left_dim == term1_dim and left_dim == term2_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                print("  建议：调整f的量纲定义为 M I^-1 T 以确保量纲一致")
                return False
                
        elif formula_id == 13:  # 磁矢势方程
            # 验证 ∇×vec{A} = vec{B}/f
            left_dim = variable_dims['∇×vec{A}']
            
            # 计算右侧: vec{B}/f
            B_dim = variable_dims['vec{B}']
            f_dim = self.parse_dimension('M I^-1')
            right_dim = self.divide_dimensions(B_dim, f_dim)
            
            print(f"  左侧量纲 (∇×vec{{A}}): {self.format_dimension(left_dim)}")
            print(f"  右侧量纲 (vec{{B}}/f): {self.format_dimension(right_dim)}")
            
            if left_dim == right_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 14:  # 变化的引力场产生电场
            # 验证 vec{E} = -f dvec{A}/dt
            expected_dim = variable_dims['vec{E}']
            
            # 计算右侧: f * dvec{A}/dt
            f_dim = self.parse_dimension('M I^-1')
            dA_dt_dim = variable_dims['dvec{A}/dt']
            calculated_dim = self.multiply_dimensions(f_dim, dA_dt_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            
            print(f"  计算量纲 (f * dvec{{A}}/dt): {calculated_dim_str}")
            
            if calculated_dim == expected_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 15:  # 变化的磁场产生引力场和电场
            # 验证 d²vec{B}/dt² = -vec{A}×vec{E}/c² - vec{v}/c² × dvec{E}/dt
            left_dim = variable_dims['d²vec{B}/dt²']
            
            # 计算右侧第一项: vec{A}×vec{E}/c²
            A_dim = variable_dims['vec{A}']
            E_dim = variable_dims['vec{E}']
            c2_dim = variable_dims['c²']
            term1_dim = self.divide_dimensions(self.multiply_dimensions(A_dim, E_dim), c2_dim)
            
            # 计算右侧第二项: vec{v}/c² × dvec{E}/dt
            v_dim = variable_dims['vec{v}']
            dE_dt_dim = variable_dims['dvec{E}/dt']
            term2_dim = self.divide_dimensions(self.multiply_dimensions(v_dim, dE_dt_dim), c2_dim)
            
            print(f"  左侧量纲 (d²vec{{B}}/dt²): {self.format_dimension(left_dim)}")
            print(f"  右侧第一项量纲 (vec{{A}}×vec{{E}}/c²): {self.format_dimension(term1_dim)}")
            print(f"  右侧第二项量纲 (vec{{v}}/c² × dvec{{E}}/dt): {self.format_dimension(term2_dim)}")
            
            # 修正变化的磁场产生引力场和电场方程的量纲分析
            # 问题：左侧量纲为 M T^-3 I^-1，右侧量纲为 L M T^-3 I^-1
            # 解决方案：调整vec{A}的量纲定义，移除长度因子
            if left_dim == term1_dim and left_dim == term2_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                print("  建议：调整vec{A}的量纲定义为 T^-2（移除长度因子）以确保量纲一致")
                return False
                
        elif formula_id == 16:  # 统一场论能量方程
            # 验证 E = m₀c²
            expected_dim = variable_dims['E']
            
            # 计算右侧: m₀ * c²
            m0_dim = self.parse_dimension('M')
            c2_dim = variable_dims['c²']
            calculated_dim = self.multiply_dimensions(m0_dim, c2_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            
            print(f"  计算量纲 (m₀ * c²): {calculated_dim_str}")
            
            if calculated_dim == expected_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 17:  # 光速飞行器动力学方程
            # 验证 vec{F} = (vec{c} - vec{v}) dm/dt
            expected_dim = variable_dims['vec{F}']
            
            # 计算右侧: (vec{c} - vec{v}) * dm/dt
            # vec{c} - vec{v} 的量纲与 vec{c} 相同
            c_dim = variable_dims['vec{c}']
            dm_dt_dim = variable_dims['dm/dt']
            calculated_dim = self.multiply_dimensions(c_dim, dm_dt_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            
            print(f"  计算量纲 ((vec{{c}} - vec{{v}}) * dm/dt): {calculated_dim_str}")
            
            if calculated_dim == expected_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 18:  # 核力场定义方程
            # 验证 vec{D} = -G m (vec{c} - 3 vec{r}/r ṙ)/r³
            expected_dim = variable_dims['vec{D}']
            
            # 计算右侧: G * m * (vec{c} - 3 vec{r}/r ṙ) / r³
            G_dim = self.parse_dimension('L^3 M^-1 T^-2')
            m_dim = variable_dims['m']
            c_dim = variable_dims['vec{c}']  # (vec{c} - 3 vec{r}/r ṙ) 的量纲与 vec{c} 相同
            r3_dim = self.parse_dimension('L^3')
            
            temp1 = self.multiply_dimensions(G_dim, m_dim)
            temp2 = self.multiply_dimensions(temp1, c_dim)
            calculated_dim = self.divide_dimensions(temp2, r3_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            
            print(f"  计算量纲 (G * m * vec{{c}} / r³): {calculated_dim_str}")
            
            if calculated_dim == expected_dim:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 19:  # 引力光速统一方程
            # 验证 Z = Gc/2
            expected_dim = formula['dimension']
            expected_dim_dict = self.parse_dimension(expected_dim)
            
            # 计算右侧: G * c
            G_dim = self.parse_dimension('L^3 M^-1 T^-2')
            c_dim = self.parse_dimension('L T^-1')
            calculated_dim = self.multiply_dimensions(G_dim, c_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            
            print(f"  计算量纲 (G * c): {calculated_dim_str}")
            
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                return False
                
        elif formula_id == 20:  # 电磁光速几何耦合常数
            # 验证 Z' = c/(8πε₀)
            expected_dim = formula['dimension']
            expected_dim_dict = self.parse_dimension(expected_dim)
            
            # 计算右侧: c * (1/ε₀)
            c_dim = self.parse_dimension('L T^-1')
            one_over_epsilon0_dim = self.parse_dimension('M L³ I^-2 T^-4')
            calculated_dim = self.multiply_dimensions(c_dim, one_over_epsilon0_dim)
            calculated_dim_str = self.format_dimension(calculated_dim)
            
            print(f"  计算量纲 (c * 1/ε₀): {calculated_dim_str}")
            
            # 修正电磁光速几何耦合常数方程的量纲分析
            # 问题：当前计算结果为 L^2 M T^-5 I^-2，预期为 L^4 M T^-5 I^-2
            # 解决方案：调整公式结构，添加长度平方因子
            if calculated_dim == expected_dim_dict:
                print("  ✅ 量纲一致")
                return True
            else:
                print("  ❌ 量纲不一致")
                print("  建议：调整公式为 Z' = c²/(8πε₀) 或添加长度平方因子以确保量纲一致")
                return False
                
        return False

def main():
    """主函数，验证所有公式的量纲"""
    print("张祥前统一场论公式量纲验证")
    print("=" * 60)
    
    analyzer = DimensionAnalyzer()
    results = []
    
    for formula in formulas_data:
        is_consistent = analyzer.analyze_formula(formula)
        results.append({
            'id': formula['id'],
            'name': formula['name'],
            'consistent': is_consistent
        })
    
    # 生成验证报告
    print("\n" + "=" * 60)
    print("量纲验证报告")
    print("=" * 60)
    
    consistent_count = sum(1 for r in results if r['consistent'])
    total_count = len(results)
    
    print(f"验证公式总数: {total_count}")
    print(f"量纲一致的公式: {consistent_count}")
    print(f"量纲不一致的公式: {total_count - consistent_count}")
    print(f"一致性比例: {consistent_count/total_count*100:.1f}%")
    
    if total_count - consistent_count > 0:
        print("\n量纲不一致的公式:")
        for r in results:
            if not r['consistent']:
                print(f"  - 公式 {r['id']}: {r['name']}")
    
    print("\n验证完成！")

if __name__ == "__main__":
    main()
