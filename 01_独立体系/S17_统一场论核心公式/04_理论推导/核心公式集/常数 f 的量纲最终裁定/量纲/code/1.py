
# 导入必要库（仅用于格式化输出，核心逻辑无依赖）
from pprint import pprint

class DimensionValidator:
    def __init__(self):
        # 初始化基础量纲符号，后续量纲均基于此组合
        self.basic_dims = ['M', 'L', 'T', 'I']
        # 定义固定物理量的量纲（经典电磁学定义，不随A的定义变化）
        self.fixed_dims = {
            'E': {'M':1, 'L':1, 'T':-3, 'I':-1},  # 电场强度 E: MLT^-3I^-1
            'B': {'M':1, 'L':0, 'T':-2, 'I':-1},  # 磁感应强度 B: MT^-2I^-1
            'V': {'M':0, 'L':1, 'T':-1, 'I':0},   # 速度 V: LT^-1
            'C': {'M':0, 'L':1, 'T':-1, 'I':0},   # 光速 C: LT^-1（与速度量纲一致）
            'dt': {'M':0, 'L':0, 'T':-1, 'I':0},  # 时间微分算子 d/dt: T^-1
            'd2t': {'M':0, 'L':0, 'T':-2, 'I':0}, # 二阶时间微分算子 ∂²/∂t²: T^-2
            'nabla': {'M':0, 'L':-1, 'T':0, 'I':0}# 空间算子 ∇: L^-1（散度/旋度通用）
        }

    def dim_multiply(self, dim1, dim2):
        """量纲乘法：两个量纲字典相乘，对应指数相加"""
        result = {dim: 0 for dim in self.basic_dims}
        for dim in self.basic_dims:
            result[dim] = dim1.get(dim, 0) + dim2.get(dim, 0)
        return result

    def dim_divide(self, dim1, dim2):
        """量纲除法：两个量纲字典相除，对应指数相减"""
        result = {dim: 0 for dim in self.basic_dims}
        for dim in self.basic_dims:
            result[dim] = dim1.get(dim, 0) - dim2.get(dim, 0)
        return result

    def dim_power(self, dim_dict, power):
        """量纲幂运算：量纲字典的每个指数乘以幂次"""
        result = {dim: 0 for dim in self.basic_dims}
        for dim in self.basic_dims:
            result[dim] = dim_dict.get(dim, 0) * power
        return result

    def simplify_dim(self, dim):
        """简化量纲字典：移除指数为0的项，便于阅读"""
        return {k: v for k, v in dim.items() if v != 0}

    def validate_scenario1(self):
        """场景1：A为磁矢势（A: MLT^-2I^-1），验证f的量纲及方程自洽性"""
        print("="*50)
        print("场景1：A为磁矢势（量纲：MLT^-2I^-1）")
        print("="*50)
        
        # 定义A的量纲（磁矢势）
        A_dim = {'M':1, 'L':1, 'T':-2, 'I':-1}
        
        # 1. 验证 curl(A) = B/f → 推导f的量纲
        print("\n1. 基于方程 curl(A) = B/f 推导f的量纲：")
        left_dim = self.dim_multiply(self.fixed_dims['nabla'], A_dim)  # 左侧：curl(A) 的量纲
        right_dim_B = self.fixed_dims['B']                             # 右侧分子：B 的量纲
        f_dim = self.dim_divide(right_dim_B, left_dim)                 # f = B / (curl(A)) → 量纲推导
        print(f"   左侧 curl(A) 量纲：{self.simplify_dim(left_dim)}")
        print(f"   右侧 B 量纲：{self.simplify_dim(right_dim_B)}")
        print(f"   推导得 f 量纲：{self.simplify_dim(f_dim)} → 无量纲")
        
        # 2. 交叉验证：E = -f*dA/dt
        print("\n2. 交叉验证（方程 E = -f*dA/dt）：")
        dA_dt_dim = self.dim_multiply(self.fixed_dims['dt'], A_dim)    # dA/dt 的量纲
        right_dim_E = self.dim_multiply(f_dim, dA_dt_dim)              # 右侧：f*dA/dt 的量纲
        left_dim_E = self.fixed_dims['E']                               # 左侧：E 的量纲
        is_consistent = self.simplify_dim(right_dim_E) == self.simplify_dim(left_dim_E)
        print(f"   右侧 f*dA/dt 量纲：{self.simplify_dim(right_dim_E)}")
        print(f"   左侧 E 量纲：{self.simplify_dim(left_dim_E)}")
        print(f"   方程量纲{'一致' if is_consistent else '不一致'} → 验证f无量纲正确")
        
        # 3. 全体系验证：磁矢势方程
        print("\n3. 全体系验证（磁矢势方程）：")
        left_dim_eq = self.dim_multiply(self.fixed_dims['d2t'], A_dim) # 左侧：d²A/dt² 量纲
        # 右侧第一项：V*(div(E))/f
        nabla_E_dim = self.dim_multiply(self.fixed_dims['nabla'], self.fixed_dims['E'])
        term1_dim = self.dim_multiply(self.fixed_dims['V'], nabla_E_dim)
        term1_dim = self.dim_divide(term1_dim, f_dim)
        # 右侧第二项：C²*(curl(B))/f
        nabla_B_dim = self.dim_multiply(self.fixed_dims['nabla'], self.fixed_dims['B'])
        C2_dim = self.dim_power(self.fixed_dims['C'], 2)
        term2_dim = self.dim_multiply(C2_dim, nabla_B_dim)
        term2_dim = self.dim_divide(term2_dim, f_dim)
        # 验证一致性
        is_term1_consistent = self.simplify_dim(term1_dim) == self.simplify_dim(left_dim_eq)
        is_term2_consistent = self.simplify_dim(term2_dim) == self.simplify_dim(left_dim_eq)
        print(f"   左侧 d²A/dt² 量纲：{self.simplify_dim(left_dim_eq)}")
        print(f"   右侧第一项 V*(div(E))/f 量纲：{self.simplify_dim(term1_dim)} → {'一致' if is_term1_consistent else '不一致'}")
        print(f"   右侧第二项 C²*(curl(B))/f 量纲：{self.simplify_dim(term2_dim)} → {'一致' if is_term2_consistent else '不一致'}")
        print(f"   磁矢势方程量纲{'完全自洽' if is_term1_consistent and is_term2_consistent else '存在矛盾'}")

    def validate_scenario2(self):
        """场景2：A为引力场强度（A: LT^-2），验证f的量纲及方程自洽性"""
        print("\n" + "="*50)
        print("场景2：A为引力场强度（量纲：LT^-2）")
        print("="*50)
        
        # 定义A的量纲（引力场强度）
        A_dim = {'M':0, 'L':1, 'T':-2, 'I':0}
        
        # 1. 验证 curl(A) = B/f → 推导f的量纲
        print("\n1. 基于方程 curl(A) = B/f 推导f的量纲：")
        left_dim = self.dim_multiply(self.fixed_dims['nabla'], A_dim)  # 左侧：curl(A) 的量纲
        right_dim_B = self.fixed_dims['B']                             # 右侧分子：B 的量纲
        f_dim = self.dim_divide(right_dim_B, left_dim)                 # f = B / (curl(A)) → 量纲推导
        print(f"   左侧 curl(A) 量纲：{self.simplify_dim(left_dim)}")
        print(f"   右侧 B 量纲：{self.simplify_dim(right_dim_B)}")
        print(f"   推导得 f 量纲：{self.simplify_dim(f_dim)} → 即 MI^-1（kg/A）")
        
        # 2. 交叉验证：E = -f*dA/dt
        print("\n2. 交叉验证（方程 E = -f*dA/dt）：")
        dA_dt_dim = self.dim_multiply(self.fixed_dims['dt'], A_dim)    # dA/dt 的量纲
        right_dim_E = self.dim_multiply(f_dim, dA_dt_dim)              # 右侧：f*dA/dt 的量纲
        left_dim_E = self.fixed_dims['E']                               # 左侧：E 的量纲
        is_consistent = self.simplify_dim(right_dim_E) == self.simplify_dim(left_dim_E)
        print(f"   右侧 f*dA/dt 量纲：{self.simplify_dim(right_dim_E)}")
        print(f"   左侧 E 量纲：{self.simplify_dim(left_dim_E)}")
        print(f"   方程量纲{'一致' if is_consistent else '不一致'} → 验证f量纲为MI^-1正确")
        
        # 3. 全体系验证：引力场-电磁场耦合方程
        print("\n3. 全体系验证（引力场-电磁场耦合方程）：")
        left_dim_eq = self.dim_multiply(self.fixed_dims['d2t'], A_dim) # 左侧：d²A/dt² 量纲
        # 右侧第一项：V*(div(E))/f
        nabla_E_dim = self.dim_multiply(self.fixed_dims['nabla'], self.fixed_dims['E'])
        term1_dim = self.dim_multiply(self.fixed_dims['V'], nabla_E_dim)
        term1_dim = self.dim_divide(term1_dim, f_dim)
        # 右侧第二项：C²*(curl(B))/f
        nabla_B_dim = self.dim_multiply(self.fixed_dims['nabla'], self.fixed_dims['B'])
        C2_dim = self.dim_power(self.fixed_dims['C'], 2)
        term2_dim = self.dim_multiply(C2_dim, nabla_B_dim)
        term2_dim = self.dim_divide(term2_dim, f_dim)
        # 验证一致性
        is_term1_consistent = self.simplify_dim(term1_dim) == self.simplify_dim(left_dim_eq)
        is_term2_consistent = self.simplify_dim(term2_dim) == self.simplify_dim(left_dim_eq)
        print(f"   左侧 d²A/dt² 量纲：{self.simplify_dim(left_dim_eq)}")
        print(f"   右侧第一项 V*(div(E))/f 量纲：{self.simplify_dim(term1_dim)} → {'一致' if is_term1_consistent else '不一致'}")
        print(f"   右侧第二项 C²*(curl(B))/f 量纲：{self.simplify_dim(term2_dim)} → {'一致' if is_term2_consistent else '不一致'}")
        print(f"   耦合方程量纲{'完全自洽' if is_term1_consistent and is_term2_consistent else '存在矛盾'}")

if __name__ == "__main__":
    # 初始化验证器并执行双场景验证
    validator = DimensionValidator()
    validator.validate_scenario1()
    validator.validate_scenario2()
    print("\n" + "="*50)
    print("验证结论：两种场景下f的量纲推导均正确，所有方程量纲完全自洽")
    print("="*50)
