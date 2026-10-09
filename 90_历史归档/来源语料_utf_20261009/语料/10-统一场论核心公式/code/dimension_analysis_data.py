# 张祥前统一场论公式量纲分析数据集
# 整理自两个文件的公式和量纲信息

# 基本物理量量纲定义
base_dimensions = {
    'length': 'L',      # 长度
    'mass': 'M',        # 质量
    'time': 'T',        # 时间
    'charge': 'Q',      # 电荷
    'current': 'I'      # 电流 (Q/T)
}

# 导出物理量量纲定义
derived_dimensions = {
    'velocity': 'L T^-1',            # 速度
    'acceleration': 'L T^-2',        # 加速度
    'momentum': 'M L T^-1',           # 动量
    'force': 'M L T^-2',              # 力
    'energy': 'M L^2 T^-2',           # 能量
    'power': 'M L^2 T^-3',            # 功率
    'gravitational_field': 'L T^-2',  # 引力场强度
    'electric_field': 'M L I^-1 T^-3', # 电场强度
    'magnetic_field': 'M I^-1 T^-2',  # 磁感应强度
    'nuclear_field': 'L T^-3',        # 核力场强度
    'coupling_constant': 'L^4 M^-1 T^-3',  # 耦合常数
    'electromagnetic_coupling': 'L^4 M T^-3 Q^-2'  # 电磁耦合
}

# 公式量纲数据
formulas_data = [
    {
        'id': 1,
        'name': '时空同一化方程',
        'expression': 'vec{r}(t) = vec{c}t = xvec{i} + yvec{j} + zvec{k}',
        'dimension': 'L',
        'variables': {
            'vec{r}': 'L',
            'vec{c}': 'L T^-1',
            't': 'T',
            'x': 'L',
            'y': 'L',
            'z': 'L'
        }
    },
    {
        'id': 2,
        'name': '三维螺旋时空方程',
        'expression': 'vec{r}(t) = rcosωt · vec{i} + rsinωt · vec{j} + ht · vec{k}',
        'dimension': 'L',
        'variables': {
            'vec{r}': 'L',
            'r': 'L',
            'ω': 'T^-1',
            't': 'T',
            'h': 'L T^-1',
            'vec{i}': '1',
            'vec{j}': '1',
            'vec{k}': '1'
        }
    },
    {
        'id': 3,
        'name': '质量定义方程',
        'expression': 'm = k dn/dΩ',
        'dimension': 'M',
        'variables': {
            'm': 'M',
            'k': 'M',
            'dn/dΩ': '1'  # 无量纲
        }
    },
    {
        'id': 4,
        'name': '引力场定义方程',
        'expression': 'vec{A} = -GkΔn/Δs vec{r}/r^2 (原始形式)',
        'dimension': 'L T^-2',
        'variables': {
            'vec{A}': 'L T^-2',
            'G': 'L^3 M^-1 T^-2',
            'k': 'M',
            'Δn/Δs': 'L^-1',
            'vec{r}/r^2': 'L^-1'
        }
    },
    {
        'id': 5,
        'name': '静止动量方程',
        'expression': 'vec{p}_0 = m_0 vec{c}_0',
        'dimension': 'M L T^-1',
        'variables': {
            'vec{p}_0': 'M L T^-1',
            'm_0': 'M',
            'vec{c}_0': 'L T^-1'
        }
    },
    {
        'id': 6,
        'name': '运动动量方程',
        'expression': 'vec{P} = m (vec{c} - vec{v})',
        'dimension': 'M L T^-1',
        'variables': {
            'vec{P}': 'M L T^-1',
            'm': 'M',
            'vec{c}': 'L T^-1',
            'vec{v}': 'L T^-1'
        }
    },
    {
        'id': 7,
        'name': '宇宙大统一方程（力方程）',
        'expression': 'vec{F} = dvec{P}/dt = vec{c} dm/dt - vec{v} dm/dt + m dvec{c}/dt - m dvec{v}/dt',
        'dimension': 'M L T^-2',
        'variables': {
            'vec{F}': 'M L T^-2',
            'vec{P}': 'M L T^-1',
            't': 'T',
            'vec{c}': 'L T^-1',
            'dm/dt': 'M T^-1',
            'vec{v}': 'L T^-1',
            'm': 'M',
            'dvec{c}/dt': 'L T^-2',
            'dvec{v}/dt': 'L T^-2'
        }
    },
    {
        'id': 8,
        'name': '空间波动方程',
        'expression': '∇²L = 1/c² ∂²L/∂t²',
        'dimension': 'L T^-2',
        'variables': {
            '∇²L': 'L^-1',
            '1/c²': 'T² L^-2',
            '∂²L/∂t²': 'L T^-2'
        }
    },
    {
        'id': 9,
        'name': '电荷定义方程',
        'expression': 'q = k\' k 1/Ω² dΩ/dt',
        'dimension': 'I T',
        'variables': {
            'q': 'I T',
            'k\'': 'I T^2 M^-1',
            'k': 'M',
            '1/Ω²': '1',  # 无量纲
            'dΩ/dt': 'T^-1'
        }
    },
    {
        'id': 10,
        'name': '电场定义方程',
        'expression': 'vec{E} = -kk\'/(4πε₀Ω²) dΩ/dt vec{r}/r³ (原始形式)',
        'dimension': 'M L I^-1 T^-3',
        'variables': {
            'vec{E}': 'M L I^-1 T^-3',
            'k': 'M',
            'k\'': 'I T^2 M^-1',
            '1/ε₀': 'M L^3 I^-2 T^-4',
            '1/Ω²': '1',  # 无量纲
            'dΩ/dt': 'T^-1',
            'vec{r}/r³': 'L^-2'
        }
    },
    {
        'id': 11,
        'name': '磁场定义方程',
        'expression': 'vec{B} = μ₀ γ k k\'/(4π Ω²) dΩ/dt [(x-vt)vec{i}+yvec{j}+zvec{k}]/[γ²(x-vt)²+y²+z²]^3/2 (原始形式)',
        'dimension': 'M I^-1 T^-2',
        'variables': {
            'vec{B}': 'M I^-1 T^-2',
            'μ₀': 'M I^-2 T^-2',
            'γ': '1',  # 无量纲
            'k': 'M',
            'k\'': 'I T^1 M^-1',
            '1/Ω²': '1',  # 无量纲
            'dΩ/dt': 'T^-1',
            'vector_term': '1',
            'denominator': '1'
        }
    },
    {
        'id': 12,
        'name': '变化的引力场产生电磁场',
        'expression': '∂³vec{A}/∂t³ = vec{v}/f (∇·vec{E}) - c²/f (∇×vec{B})',
        'dimension': 'L T^-5',
        'variables': {
            '∂³vec{A}/∂t³': 'L T^-5',
            'vec{v}': 'L T^-1',
            'f': 'M I^-1',
            '∇·vec{E}': 'M I^-1 T^-4',
            'c²': 'L² T^-2',
            '∇×vec{B}': 'M I^-1 T^-3'
        }
    },
    {
        'id': 13,
        'name': '磁矢势方程',
        'expression': '∇×vec{A} = vec{B}/f',
        'dimension': 'T^-2',
        'variables': {
            '∇×vec{A}': 'T^-2',
            'vec{B}': 'M I^-1 T^-2',
            'f': 'M I^-1'
        }
    },
    {
        'id': 14,
        'name': '变化的引力场产生电场',
        'expression': 'vec{E} = -f dvec{A}/dt',
        'dimension': 'M L I^-1 T^-3',
        'variables': {
            'vec{E}': 'M L I^-1 T^-3',
            'f': 'M I^-1',
            'dvec{A}/dt': 'L T^-3'
        }
    },
    {
        'id': 15,
        'name': '变化的磁场产生引力场和电场',
        'expression': 'd²vec{B}/dt² = -vec{A}×vec{E}/c² - vec{v}/c² × dvec{E}/dt',
        'dimension': 'M I^-1 T^-3',
        'variables': {
            'd²vec{B}/dt²': 'M I^-1 T^-3',
            'vec{A}': 'L T^-2',
            'vec{E}': 'M I^-1 T^-3',
            'c²': 'L² T^-2',
            'vec{v}': 'L T^-1',
            'dvec{E}/dt': 'M I^-1 T^-4'
        }
    },
    {
        'id': 16,
        'name': '统一场论能量方程',
        'expression': 'E = m₀c² = mc²√(1 - v²/c²)',
        'dimension': 'M L² T^-2',
        'variables': {
            'E': 'M L² T^-2',
            'm₀': 'M',
            'c²': 'L² T^-2',
            'm': 'M',
            'v²/c²': '1'  # 无量纲
        }
    },
    {
        'id': 17,
        'name': '光速飞行器动力学方程',
        'expression': 'vec{F} = (vec{c} - vec{v}) dm/dt',
        'dimension': 'M L T^-2',
        'variables': {
            'vec{F}': 'M L T^-2',
            'vec{c}': 'L T^-1',
            'vec{v}': 'L T^-1',
            'dm/dt': 'M T^-1'
        }
    },
    {
        'id': 18,
        'name': '核力场定义方程',
        'expression': 'vec{D} = -G m (vec{c} - 3 vec{r}/r ṙ)/r³ (原始形式)',
        'dimension': 'L T^-3',
        'variables': {
            'vec{D}': 'L T^-3',
            'G': 'L^3 M^-1 T^-2',
            'm': 'M',
            'vec{c}': 'L T^-1',
            'vec{r}/r': '1',  # 无量纲
            'ṙ': 'L T^-1',
            '1/r³': 'L^-3'
        }
    },
    {
        'id': 19,
        'name': '引力光速统一方程',
        'expression': 'Z = Gc/2',
        'dimension': 'L^4 M^-1 T^-3',
        'variables': {
            'Z': 'L^4 M^-1 T^-3',
            'G': 'L^3 M^-1 T^-2',
            'c': 'L T^-1'
        }
    },
    {
        'id': 20,
        'name': '电磁光速几何耦合常数',
        'expression': 'Z\' = c/(8πε₀)',
        'dimension': 'L^4 M T^-5 I^-2',
        'variables': {
            'Z\'': 'L^4 M T^-5 I^-2',
            'c': 'L T^-1',
            '1/ε₀': 'M L^3 I^-2 T^-4'
        }
    }
]

# 物理常数的量纲
physical_constants = {
    'c': 'L T^-1',      # 光速
    'G': 'L^3 M^-1 T^-2',  # 万有引力常数
    'ε₀': 'M^-1 L^-3 I^2 T^4',  # 真空介电常数
    'μ₀': 'M L I^-2 T^-2',  # 真空磁导率
    'ħ': 'M L^2 T^-1'   # 约化普朗克常数
}

# 耦合常数的量纲
coupling_constants = {
    'k': 'M',           # 空间-质量耦合常数
    'k\'': 'I T^2 M^-1',  # 空间-电荷耦合常数
    'f': 'M I^-1',      # 场转化耦合常数
    'Z': 'L^4 M^-1 T^-3',  # 引力光速统一常数
    'Z\'': 'L^4 M T^-3 I^-2'  # 电磁光速几何耦合常数
}
