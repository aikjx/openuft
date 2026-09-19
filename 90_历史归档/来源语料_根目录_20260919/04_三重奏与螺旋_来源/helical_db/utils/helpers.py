import time
import random
import math
import uuid
from helical_db.config.constants import CONST_C

# 时间相关函数
def time_now():
    """获取当前时间戳"""
    return time.time()

# 数学计算函数
def calculate_spiral_distance(params1, params2):
    """计算两个螺旋参数之间的距离"""
    r1, ω1, p1 = params1['r'], params1['ω'], params1['p']
    r2, ω2, p2 = params2['r'], params2['ω'], params2['p']
    
    # 计算欧几里得距离
    distance = math.sqrt(
        (r1 - r2)**2 +
        (ω1 - ω2)**2 +
        (p1 - p2)**2
    )
    return distance

def adjust_parameters(r, ω, p):
    """调整参数以满足光速约束"""
    # 计算当前速度平方和
    current_sum = (r * ω)**2 + p**2
    
    if current_sum == 0:
        return r, ω, p
    
    # 缩放因子
    scale_factor = CONST_C / math.sqrt(current_sum)
    
    # 调整参数
    new_r = r * scale_factor
    new_ω = ω * scale_factor
    new_p = p * scale_factor
    
    return new_r, new_ω, new_p

# 生成唯一ID
def generate_spiral_id():
    """生成螺旋量子唯一ID"""
    return str(uuid.uuid4())

# 数据处理函数
def invert_data(data):
    """生成数据的负版本"""
    if isinstance(data, dict):
        return {k: invert_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [invert_data(item) for item in data]
    elif isinstance(data, (int, float)):
        return -data
    elif isinstance(data, str):
        return data[::-1]  # 字符串反转
    else:
        return data

# 投影函数
def project_to_2d(xyz):
    """将三维坐标投影到二维平面"""
    x, y, z = xyz
    return (x, y)

def back_project_to_3d(xy, z=0):
    """将二维坐标反投影到三维空间"""
    x, y = xy
    return (x, y, z)

# 随机参数生成
def generate_random_params():
    """生成随机螺旋参数"""
    r = random.uniform(0, 1000)
    ω = random.uniform(0, 1000)
    p = random.uniform(0, 1000)
    
    # 调整参数以满足光速约束
    r, ω, p = adjust_parameters(r, ω, p)
    
    return {
        'r': r,
        'ω': ω,
        'p': p
    }

# 序列生成器
def generate_infinite_sequence(start=0, step=1):
    """生成无限序列"""
    current = start
    while True:
        yield current
        current += step

# 约束检查
def satisfy_constraint(r, ω, p):
    """检查参数是否满足光速约束"""
    return (r * ω)**2 + p**2 <= CONST_C**2
