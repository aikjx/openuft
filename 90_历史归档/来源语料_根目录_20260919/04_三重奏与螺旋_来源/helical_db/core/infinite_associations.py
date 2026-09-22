import math
from helical_db.config.constants import CONST_Z, CONST_ZPRIME

class InfiniteAssociations:
    """无限关联关系系统 - 基于三维垂直原理"""
    
    def __init__(self):
        """初始化无限关联系统"""
        # 关联网络
        self.association_network = {
            'level_0': {},  # 直接关联
            'level_1': {},  # 间接关联（一度分离）
            'level_2': {},  # 二度分离
            # 更高层级会自动创建
        }
        
        # 关联强度
        self.association_strengths = {}
        
        # 关联统计
        self.association_stats = {
            'total_associations': 0,
            'max_depth': 0,
            'average_strength': 0
        }
    
    def create_association(self, q1, q2, relation_type):
        """创建三维垂直关联"""
        # 1. 径向关联（引力场方向）
        if relation_type == 'radial':
            vector = self.calculate_radial_vector(q1, q2)
            strength = self.calculate_gravitational_strength(q1, q2)
        
        # 2. 角向关联（电场方向）
        elif relation_type == 'angular':
            vector = self.calculate_angular_vector(q1, q2)
            strength = self.calculate_electric_strength(q1, q2)
        
        # 3. 轴向关联（磁场方向）
        elif relation_type == 'axial':
            vector = self.calculate_axial_vector(q1, q2)
            strength = self.calculate_magnetic_strength(q1, q2)
        
        # 4. 复合关联（三力垂直）
        elif relation_type == 'tri_force':
            # 同时建立三种关联，形成垂直结构
            self.create_association(q1, q2, 'radial')
            self.create_association(q1, q2, 'angular')
            self.create_association(q1, q2, 'axial')
            return
        
        else:
            return
        
        # 添加关联到量子对象
        q1.add_association(relation_type, q2)
        q2.add_association(relation_type, q1)
        
        # 添加到关联网络
        self._add_to_network(q1, q2, relation_type, strength)
        
        # 关联强度无限增强
        self.increase_association_strength(q1, q2, strength)
        
        # 更新统计信息
        self.association_stats['total_associations'] += 1
    
    def calculate_radial_vector(self, q1, q2):
        """计算径向向量"""
        dx = q2.x - q1.x
        dy = q2.y - q1.y
        dz = q2.z - q1.z
        
        # 计算距离
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        
        if distance == 0:
            return (0, 0, 0)
        
        # 单位向量
        return (dx/distance, dy/distance, dz/distance)
    
    def calculate_angular_vector(self, q1, q2):
        """计算角向向量"""
        # 角向向量垂直于径向向量
        radial = self.calculate_radial_vector(q1, q2)
        
        # 生成垂直向量
        if radial[0] != 0 or radial[1] != 0:
            # 与x-y平面垂直
            return (-radial[1], radial[0], 0)
        else:
            # 与z轴垂直
            return (1, 0, 0)
    
    def calculate_axial_vector(self, q1, q2):
        """计算轴向向量"""
        # 轴向向量垂直于径向和角向向量
        radial = self.calculate_radial_vector(q1, q2)
        angular = self.calculate_angular_vector(q1, q2)
        
        # 叉乘计算轴向向量
        ax = radial[1] * angular[2] - radial[2] * angular[1]
        ay = radial[2] * angular[0] - radial[0] * angular[2]
        az = radial[0] * angular[1] - radial[1] * angular[0]
        
        return (ax, ay, az)
    
    def calculate_gravitational_strength(self, q1, q2):
        """计算引力强度"""
        distance = math.sqrt(
            (q2.x - q1.x)**2 +
            (q2.y - q1.y)**2 +
            (q2.z - q1.z)**2
        )
        
        if distance == 0:
            return 0
        
        # 基于引力常数的强度计算
        strength = CONST_Z / (distance**2)
        return strength
    
    def calculate_electric_strength(self, q1, q2):
        """计算电场强度"""
        distance = math.sqrt(
            (q2.x - q1.x)**2 +
            (q2.y - q1.y)**2 +
            (q2.z - q1.z)**2
        )
        
        if distance == 0:
            return 0
        
        # 基于电磁常数的强度计算
        strength = CONST_ZPRIME / (distance**2)
        return strength
    
    def calculate_magnetic_strength(self, q1, q2):
        """计算磁场强度"""
        # 磁场强度与角速度和轴向速度相关
        angular_velocity = abs(q1.ω - q2.ω)
        axial_velocity = abs(q1.p - q2.p)
        
        # 组合强度
        strength = angular_velocity * axial_velocity
        return strength
    
    def increase_association_strength(self, q1, q2, strength_increment):
        """增强关联强度"""
        key = f"{min(q1.id, q2.id)}:{max(q1.id, q2.id)}"
        
        if key not in self.association_strengths:
            self.association_strengths[key] = 0
        
        self.association_strengths[key] += strength_increment
        
        # 更新平均强度
        total_strength = sum(self.association_strengths.values())
        count = len(self.association_strengths)
        self.association_stats['average_strength'] = total_strength / count if count > 0 else 0
    
    def find_related(self, quantum, max_degrees=10):
        """查找无限度关联的数据"""
        results = []
        visited = set()
        
        def traverse(current, degree):
            if degree > max_degrees or current.id in visited:
                return
                
            visited.add(current.id)
            results.append((current, degree))
            
            # 更新最大深度
            if degree > self.association_stats['max_depth']:
                self.association_stats['max_depth'] = degree
            
            # 查找所有关联
            for assoc_type in ['radial', 'angular', 'axial']:
                for related in current.get_associations(assoc_type):
                    traverse(related, degree + 1)
        
        traverse(quantum, 0)
        return results
    
    def find_reverse_associations(self, quantum, assoc_type):
        """查找反向关联"""
        reverse_associations = []
        
        # 遍历所有关联层级
        for level, level_data in self.association_network.items():
            if quantum.id in level_data:
                for related_id, relation_info in level_data[quantum.id].items():
                    if relation_info['type'] == assoc_type:
                        # 这里需要根据ID找到对应的量子对象
                        # 实际实现中需要有量子对象的索引
                        reverse_associations.append(related_id)
        
        return reverse_associations
    
    def auto_associate(self, quantum, max_associations=10):
        """自动关联新量子"""
        # 这里需要实现基于空间距离的自动关联
        # 实际实现中需要访问存储系统获取其他量子
        pass
    
    def _add_to_network(self, q1, q2, relation_type, strength):
        """添加关联到网络"""
        # 确保层级存在
        for level in ['level_0', 'level_1', 'level_2']:
            if level not in self.association_network:
                self.association_network[level] = {}
        
        # 添加到直接关联网络
        if q1.id not in self.association_network['level_0']:
            self.association_network['level_0'][q1.id] = {}
        
        self.association_network['level_0'][q1.id][q2.id] = {
            'type': relation_type,
            'strength': strength,
            'timestamp': None
        }
        
        # 对称添加
        if q2.id not in self.association_network['level_0']:
            self.association_network['level_0'][q2.id] = {}
        
        self.association_network['level_0'][q2.id][q1.id] = {
            'type': relation_type,
            'strength': strength,
            'timestamp': None
        }
    
    def get_association_strength(self, q1, q2):
        """获取关联强度"""
        key = f"{min(q1.id, q2.id)}:{max(q1.id, q2.id)}"
        return self.association_strengths.get(key, 0)
    
    def remove_association(self, q1, q2, relation_type):
        """移除关联"""
        # 从量子对象中移除
        q1.remove_association(relation_type, q2)
        q2.remove_association(relation_type, q1)
        
        # 从网络中移除
        if q1.id in self.association_network.get('level_0', {}):
            if q2.id in self.association_network['level_0'][q1.id]:
                del self.association_network['level_0'][q1.id][q2.id]
        
        if q2.id in self.association_network.get('level_0', {}):
            if q1.id in self.association_network['level_0'][q2.id]:
                del self.association_network['level_0'][q2.id][q1.id]
        
        # 从强度记录中移除
        key = f"{min(q1.id, q2.id)}:{max(q1.id, q2.id)}"
        if key in self.association_strengths:
            del self.association_strengths[key]
        
        # 更新统计信息
        if self.association_stats['total_associations'] > 0:
            self.association_stats['total_associations'] -= 1
    
    def get_association_stats(self):
        """获取关联统计信息"""
        return self.association_stats
    
    def clear_associations(self):
        """清空所有关联"""
        # 清空关联网络
        self.association_network = {
            'level_0': {},
            'level_1': {},
            'level_2': {}
        }
        
        # 清空强度记录
        self.association_strengths.clear()
        
        # 重置统计信息
        self.association_stats = {
            'total_associations': 0,
            'max_depth': 0,
            'average_strength': 0
        }
    
    def __str__(self):
        """字符串表示"""
        stats = self.get_association_stats()
        return f"InfiniteAssociations(total={stats['total_associations']}, max_depth={stats['max_depth']})"
    
    def __repr__(self):
        """官方字符串表示"""
        return self.__str__()
