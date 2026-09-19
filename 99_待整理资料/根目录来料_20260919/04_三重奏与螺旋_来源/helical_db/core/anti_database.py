from helical_db.utils.helpers import invert_data

class SpiralCluster:
    """螺旋簇 - 子数据库的基础结构"""
    
    def __init__(self, quanta):
        """
        初始化螺旋簇
        
        Args:
            quanta: 量子列表
        """
        self.quanta = quanta
        self.center = self.calculate_center()
        self.radius = self.calculate_radius()
    
    def calculate_center(self):
        """计算螺旋簇中心"""
        if not self.quanta:
            return (0, 0, 0)
        
        total_x = sum(q.x for q in self.quanta)
        total_y = sum(q.y for q in self.quanta)
        total_z = sum(q.z for q in self.quanta)
        count = len(self.quanta)
        
        return (total_x/count, total_y/count, total_z/count)
    
    def calculate_radius(self):
        """计算螺旋簇半径"""
        if not self.quanta:
            return 0
        
        max_distance = 0
        cx, cy, cz = self.center
        
        for q in self.quanta:
            distance = ((q.x - cx)**2 + (q.y - cy)**2 + (q.z - cz)**2)**0.5
            if distance > max_distance:
                max_distance = distance
        
        return max_distance
    
    def get_quanta(self):
        """获取量子列表"""
        return self.quanta

class AntiDatabase:
    """负数据库 - 存储反向、镜像、互补数据"""
    
    def __init__(self, main_db):
        """
        初始化负数据库
        
        Args:
            main_db: 主数据库实例
        """
        self.main_db = main_db
        self.anti_storage = {}
        self.sub_dbs = {}
        
    def store_anti(self, quantum):
        """存储数据的负版本"""
        # 1. 创建负螺旋（参数取反）
        anti_quantum = quantum.copy()
        anti_quantum.ω = -quantum.ω  # 反向旋转
        anti_quantum.p = -quantum.p  # 反向运动
        anti_quantum.data = self.invert_data(quantum.data)
        
        # 2. 存储在负空间
        anti_key = f"anti_{quantum.id}"
        self.anti_storage[anti_key] = anti_quantum
        
        # 3. 建立正负关联
        self.link_positive_negative(quantum, anti_quantum)
        
        return anti_quantum
    
    def invert_data(self, data):
        """生成数据的负版本"""
        return invert_data(data)
    
    def link_positive_negative(self, quantum, anti_quantum):
        """建立正负关联"""
        # 在主数据库和负数据库之间建立关联
        # 实际实现中需要更复杂的关联机制
        pass
    
    def create_sub_database(self, filter_params):
        """创建子数据库（无限个）"""
        sub_db_id = f"subdb_{hash(str(filter_params))}"
        
        # 基于螺旋参数过滤
        sub_quanta = []
        if hasattr(self.main_db, 'storage'):
            for quantum in self.main_db.storage.get_all_quanta():
                if self.match_spiral_params(quantum, filter_params):
                    sub_quanta.append(quantum)
        
        # 创建子螺旋
        sub_spiral = SpiralCluster(sub_quanta)
        
        # 子数据库可以有自己的子数据库（无限递归）
        sub_db = {
            'id': sub_db_id,
            'spiral': sub_spiral,
            'anti_db': AntiDatabase(self),  # 子数据库也有负版本
            'sub_dbs': {}  # 可以继续创建子子数据库
        }
        
        self.sub_dbs[sub_db_id] = sub_db
        
        return sub_db
    
    def match_spiral_params(self, quantum, filter_params):
        """匹配螺旋参数"""
        # 基于过滤参数匹配量子
        for param_name, param_value in filter_params.items():
            if hasattr(quantum, param_name):
                quantum_value = getattr(quantum, param_name)
                
                if isinstance(param_value, (int, float)):
                    if not (param_value - 0.1 <= quantum_value <= param_value + 0.1):
                        return False
                elif isinstance(param_value, dict):
                    if 'min' in param_value and quantum_value < param_value['min']:
                        return False
                    if 'max' in param_value and quantum_value > param_value['max']:
                        return False
        
        return True
    
    def get_anti_quantum(self, quantum_id):
        """获取负量子"""
        anti_key = f"anti_{quantum_id}"
        return self.anti_storage.get(anti_key)
    
    def get_all_anti_quanta(self):
        """获取所有负量子"""
        return list(self.anti_storage.values())
    
    def get_sub_database(self, sub_db_id):
        """获取子数据库"""
        return self.sub_dbs.get(sub_db_id)
    
    def get_all_sub_databases(self):
        """获取所有子数据库"""
        return list(self.sub_dbs.values())
    
    def delete_anti_quantum(self, quantum_id):
        """删除负量子"""
        anti_key = f"anti_{quantum_id}"
        if anti_key in self.anti_storage:
            del self.anti_storage[anti_key]
    
    def delete_sub_database(self, sub_db_id):
        """删除子数据库"""
        if sub_db_id in self.sub_dbs:
            del self.sub_dbs[sub_db_id]
    
    def clear(self):
        """清空负数据库"""
        self.anti_storage.clear()
        self.sub_dbs.clear()
    
    def get_stats(self):
        """获取负数据库统计信息"""
        return {
            'anti_quanta_count': len(self.anti_storage),
            'sub_db_count': len(self.sub_dbs)
        }
    
    def __str__(self):
        """字符串表示"""
        stats = self.get_stats()
        return f"AntiDatabase(anti_quanta={stats['anti_quanta_count']}, sub_dbs={stats['sub_db_count']})"
    
    def __repr__(self):
        """官方字符串表示"""
        return self.__str__()
