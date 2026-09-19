import math
from helical_db.config.constants import CONST_C
from helical_db.utils.helpers import time_now, generate_spiral_id, adjust_parameters

class HelicalQuantum:
    """螺旋量子 - 数据库的基础数据单元"""
    
    def __init__(self, data, spiral_params=None):
        """
        初始化螺旋量子
        
        Args:
            data: 存储的数据内容
            spiral_params: 螺旋参数字典，包含r, ω, p
        """
        # 时间参数
        self.t = time_now()
        
        # 螺旋参数
        if spiral_params:
            self.r = spiral_params.get('r', 0)
            self.ω = spiral_params.get('ω', 0)
            self.p = spiral_params.get('p', 0)
        else:
            # 默认参数
            self.r = 1.0
            self.ω = 1.0
            self.p = 1.0
        
        # 光速常数
        self.c = CONST_C
        
        # 调整参数以满足光速约束
        self.adjust_parameters()
        
        # 计算三维坐标
        self.calculate_coordinates()
        
        # 数据内容
        self.data = data
        
        # 生成唯一ID
        self.id = generate_spiral_id()
        
        # 关联维度（垂直原理）
        self.associations = {
            'radial': [],    # 径向关联（引力场方向）
            'angular': [],   # 角向关联（电场方向）
            'axial': []      # 轴向关联（磁场方向）
        }
    
    def adjust_parameters(self):
        """调整参数以满足光速约束"""
        self.r, self.ω, self.p = adjust_parameters(self.r, self.ω, self.p)
    
    def calculate_coordinates(self):
        """计算三维坐标"""
        # 螺旋坐标计算公式
        self.x = self.r * math.cos(self.ω * self.t)
        self.y = self.r * math.sin(self.ω * self.t)
        self.z = self.p * self.t
    
    def get_coordinates(self):
        """获取三维坐标"""
        return (self.x, self.y, self.z)
    
    def get_params(self):
        """获取螺旋参数"""
        return {
            'r': self.r,
            'ω': self.ω,
            'p': self.p,
            't': self.t
        }
    
    def update_time(self, new_time=None):
        """更新时间参数并重新计算坐标"""
        if new_time:
            self.t = new_time
        else:
            self.t = time_now()
        self.calculate_coordinates()
    
    def add_association(self, association_type, quantum):
        """添加关联"""
        if association_type in self.associations:
            self.associations[association_type].append(quantum)
    
    def remove_association(self, association_type, quantum):
        """移除关联"""
        if association_type in self.associations:
            try:
                self.associations[association_type].remove(quantum)
            except ValueError:
                pass
    
    def get_associations(self, association_type=None):
        """获取关联"""
        if association_type:
            return self.associations.get(association_type, [])
        else:
            return self.associations
    
    def copy(self):
        """创建副本"""
        # 创建新的螺旋量子
        copy_quantum = HelicalQuantum(
            data=self.data,
            spiral_params=self.get_params()
        )
        # 复制关联
        for assoc_type, quanta in self.associations.items():
            copy_quantum.associations[assoc_type] = quanta.copy()
        
        return copy_quantum
    
    def __str__(self):
        """字符串表示"""
        return f"HelicalQuantum(id={self.id[:8]}..., coords=({self.x:.2f}, {self.y:.2f}, {self.z:.2f}))"
    
    def __repr__(self):
        """官方字符串表示"""
        return self.__str__()
