# 系统常量定义

# 光速（m/s）
CONST_C = 299792458

# 引力常数Z（基于统一场论）
CONST_Z = 6.67430e-11 * CONST_C / 2

# 电磁常数Z'（基于统一场论）
CONST_ZPRIME = CONST_C / (8 * 3.141592653589793 * 8.854187817e-12)

# 网格大小（用于二维查询平面）
GRID_SIZE = 0.1

# 连接阈值（用于分布式节点）
CONNECTION_THRESHOLD = 100.0

# 存储层配置
INITIAL_STORAGE_LAYERS = 3
MAX_STORAGE_LAYERS = 100

# 查询模式
QUERY_MODES = {
    'instant': '瞬间查询',
    'associative': '关联查询',
    'distributed': '分布式查询',
    'holographic': '全息查询'
}

# 关联类型
ASSOCIATION_TYPES = {
    'radial': '径向关联（引力场方向）',
    'angular': '角向关联（电场方向）',
    'axial': '轴向关联（磁场方向）',
    'tri_force': '复合关联（三力垂直）'
}

# 拓扑类型
TOPOLOGY_TYPES = [
    'single_spiral',
    'double_spiral',
    'nested_spiral',
    'interwoven_spiral',
    'fractal_spiral'
]

# 默认参数范围
DEFAULT_PARAM_RANGES = {
    'r': (0, 1000),
    'ω': (0, 1000),
    'p': (0, 1000)
}
