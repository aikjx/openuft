"""
mpmath兼容层 - 使用numpy和math提供基础功能
用于在没有mpmath的环境中运行验证代码
精度为float64（约15-17位有效数字），足够验证用途
"""

import numpy as np
import math

# 基本常数
pi = math.pi
e = math.e
inf = math.inf

# 高精度浮点数（使用numpy float64）
def mpf(x):
    """转换为float64"""
    return np.float64(x)

# 数学函数
def sqrt(x):
    return np.sqrt(x)

def exp(x):
    return np.exp(x)

def log(x):
    return np.log(x)

def log10(x):
    return np.log10(x)

def sin(x):
    return np.sin(x)

def cos(x):
    return np.cos(x)

def tan(x):
    return np.tan(x)

def abs(x):
    return np.abs(x)

def power(x, y):
    return np.power(x, y)

# 精度设置（兼容接口，实际使用float64）
class _MP:
    def __init__(self):
        self.dps = 15  # float64约15位有效数字
    
    def __setattr__(self, name, value):
        if name == 'dps':
            # 忽略，使用固定精度
            object.__setattr__(self, name, 15)
        else:
            object.__setattr__(self, name, value)

mp = _MP()
# 兼容 mp.mp.dps 的访问方式
mp.mp = mp
