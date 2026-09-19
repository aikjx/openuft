from helical_db.config.constants import INITIAL_STORAGE_LAYERS, MAX_STORAGE_LAYERS

class InfiniteStorage:
    """无限存储机制 - 基于空间无限可分原理"""
    
    def __init__(self):
        """初始化无限存储"""
        # 存储层结构
        self.storage_layers = {
            'layer_0': {},      # 基础层（三维螺旋存储）
            'layer_1': {},      # 压缩层（二维投影存储）
            'layer_2': {},      # 超压缩层（一维线性存储）
            'layer_inf': {}     # 零维点存储（信息奇点）
        }
        
        # 初始化额外存储层
        for i in range(3, INITIAL_STORAGE_LAYERS):
            layer_name = f"layer_{i}"
            self.storage_layers[layer_name] = {}
        
        # 存储统计
        self.stats = {
            'total_quanta': 0,
            'layers_count': len(self.storage_layers),
            'last_layer_created': None
        }
    
    def store(self, quantum):
        """存储螺旋量子到多个维度"""
        # 1. 三维螺旋存储
        key_3d = f"{quantum.x:.6f}:{quantum.y:.6f}:{quantum.z:.6f}"
        self.storage_layers['layer_0'][key_3d] = quantum
        
        # 2. 二维投影存储（实现快速查询）
        key_2d = f"{quantum.x:.6f}:{quantum.y:.6f}"
        self.storage_layers['layer_1'][key_2d] = quantum
        
        # 3. 一维线性存储（极致压缩）
        key_1d = f"{quantum.t:.6f}"
        self.storage_layers['layer_2'][key_1d] = quantum
        
        # 4. 零维点存储（信息奇点）
        key_0d = quantum.id
        self.storage_layers['layer_inf'][key_0d] = quantum.data
        
        # 5. 存储到其他层（如果存在）
        for i in range(3, len(self.storage_layers) - 1):  # 排除layer_inf
            layer_name = f"layer_{i}"
            if layer_name in self.storage_layers:
                # 基于层索引的特殊存储方式
                layer_key = self._generate_layer_key(quantum, i)
                self.storage_layers[layer_name][layer_key] = quantum
        
        # 更新统计信息
        self.stats['total_quanta'] += 1
        
        # 自动创建新存储层（无限扩展）
        if self.need_new_layer():
            self._create_new_layer()
    
    def retrieve(self, layer_name, key):
        """从指定层检索数据"""
        if layer_name in self.storage_layers:
            return self.storage_layers[layer_name].get(key)
        return None
    
    def delete(self, quantum):
        """从所有层删除数据"""
        # 1. 从三维层删除
        key_3d = f"{quantum.x:.6f}:{quantum.y:.6f}:{quantum.z:.6f}"
        if key_3d in self.storage_layers['layer_0']:
            del self.storage_layers['layer_0'][key_3d]
        
        # 2. 从二维层删除
        key_2d = f"{quantum.x:.6f}:{quantum.y:.6f}"
        if key_2d in self.storage_layers['layer_1']:
            del self.storage_layers['layer_1'][key_2d]
        
        # 3. 从一维层删除
        key_1d = f"{quantum.t:.6f}"
        if key_1d in self.storage_layers['layer_2']:
            del self.storage_layers['layer_2'][key_1d]
        
        # 4. 从零维层删除
        key_0d = quantum.id
        if key_0d in self.storage_layers['layer_inf']:
            del self.storage_layers['layer_inf'][key_0d]
        
        # 5. 从其他层删除
        for i in range(3, len(self.storage_layers) - 1):
            layer_name = f"layer_{i}"
            if layer_name in self.storage_layers:
                layer_key = self._generate_layer_key(quantum, i)
                if layer_key in self.storage_layers[layer_name]:
                    del self.storage_layers[layer_name][layer_key]
        
        # 更新统计信息
        if self.stats['total_quanta'] > 0:
            self.stats['total_quanta'] -= 1
    
    def get_all_quanta(self):
        """获取所有螺旋量子"""
        # 从基础层获取所有量子
        quanta = list(self.storage_layers['layer_0'].values())
        return quanta
    
    def get_quanta_by_layer(self, layer_name):
        """从指定层获取量子"""
        if layer_name in self.storage_layers:
            if layer_name == 'layer_inf':
                # 零维层只存储数据，不存储量子对象
                return list(self.storage_layers['layer_inf'].values())
            return list(self.storage_layers[layer_name].values())
        return []
    
    def need_new_layer(self):
        """判断是否需要创建新存储层"""
        # 基于存储量和层数的判断
        layer_count = len(self.storage_layers) - 1  # 排除layer_inf
        
        # 当存储量超过阈值且层数未达上限时
        storage_threshold = 1000 * layer_count
        return (self.stats['total_quanta'] > storage_threshold and 
                layer_count < MAX_STORAGE_LAYERS)
    
    def _create_new_layer(self):
        """创建新存储层"""
        layer_count = len(self.storage_layers) - 1  # 排除layer_inf
        
        if layer_count < MAX_STORAGE_LAYERS:
            new_layer_name = f"layer_{layer_count}"
            self.storage_layers[new_layer_name] = {}
            self.stats['layers_count'] = len(self.storage_layers)
            self.stats['last_layer_created'] = new_layer_name
            return new_layer_name
        return None
    
    def _generate_layer_key(self, quantum, layer_index):
        """基于层索引生成存储键"""
        # 不同层使用不同的键生成策略
        if layer_index % 3 == 0:
            # 基于x和z的组合
            return f"{quantum.x:.6f}:{quantum.z:.6f}"
        elif layer_index % 3 == 1:
            # 基于y和z的组合
            return f"{quantum.y:.6f}:{quantum.z:.6f}"
        else:
            # 基于参数的哈希
            return f"{quantum.r:.6f}:{quantum.ω:.6f}:{layer_index}"
    
    def clear(self):
        """清空所有存储"""
        for layer_name in list(self.storage_layers.keys()):
            if layer_name != 'layer_inf':
                self.storage_layers[layer_name].clear()
        
        # 保留零维层但清空内容
        self.storage_layers['layer_inf'].clear()
        
        # 重置统计信息
        self.stats = {
            'total_quanta': 0,
            'layers_count': len(self.storage_layers),
            'last_layer_created': self.stats['last_layer_created']
        }
    
    def get_stats(self):
        """获取存储统计信息"""
        # 计算每层的存储量
        layer_stats = {}
        for layer_name, layer_data in self.storage_layers.items():
            layer_stats[layer_name] = len(layer_data)
        
        return {
            **self.stats,
            'layer_stats': layer_stats
        }
    
    def __str__(self):
        """字符串表示"""
        stats = self.get_stats()
        return f"InfiniteStorage(layers={stats['layers_count']}, quanta={stats['total_quanta']})"
    
    def __repr__(self):
        """官方字符串表示"""
        return self.__str__()
