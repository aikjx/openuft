from helical_db.config.constants import TOPOLOGY_TYPES
from helical_db.utils.helpers import generate_infinite_sequence, satisfy_constraint

class InfiniteExpansionEngine:
    """无限扩展引擎 - 支持参数、拓扑、维度和时间扩展"""
    
    def __init__(self):
        """初始化无限扩展引擎"""
        # 扩展维度配置
        self.expansion_dimensions = {
            'parametric': True,   # 参数扩展
            'topological': True,  # 拓扑扩展
            'dimensional': True,  # 维度扩展
            'temporal': True,     # 时间扩展
        }
        
        # 扩展统计
        self.expansion_stats = {
            'parametric_expansions': 0,
            'topological_expansions': 0,
            'dimensional_expansions': 0,
            'temporal_expansions': 0
        }
    
    def expand_parametric(self, quantum=None):
        """参数无限扩展"""
        # 生成无限参数组合
        param_combinations = []
        
        # 使用无限序列生成器
        r_sequence = generate_infinite_sequence(0.1, 0.1)
        ω_sequence = generate_infinite_sequence(0.1, 0.1)
        p_sequence = generate_infinite_sequence(0.1, 0.1)
        
        # 生成参数组合（实际实现中需要限制数量）
        for i in range(100):  # 限制为100个组合以避免无限循环
            try:
                r = next(r_sequence)
                ω = next(ω_sequence)
                p = next(p_sequence)
                
                if satisfy_constraint(r, ω, p):
                    param_combinations.append((r, ω, p))
                    self.expansion_stats['parametric_expansions'] += 1
            except StopIteration:
                break
        
        return param_combinations
    
    def expand_topological(self):
        """拓扑无限扩展"""
        # 创建新的螺旋拓扑
        for topology in TOPOLOGY_TYPES:
            topology_instance = self.create_topology(topology)
            self.expansion_stats['topological_expansions'] += 1
            yield topology_instance
        
        # 生成更多拓扑类型
        custom_topologies = [
            'branching_spiral',
            'converging_spiral',
            'diverging_spiral',
            'chaotic_spiral',
            'symmetric_spiral'
        ]
        
        for topology in custom_topologies:
            topology_instance = self.create_topology(topology)
            self.expansion_stats['topological_expansions'] += 1
            yield topology_instance
    
    def create_topology(self, topology_type):
        """创建指定类型的拓扑"""
        topology_config = {
            'type': topology_type,
            'parameters': {},
            'description': f'{topology_type} topology'
        }
        
        # 根据拓扑类型设置参数
        if topology_type == 'single_spiral':
            topology_config['parameters'] = {'arms': 1}
        elif topology_type == 'double_spiral':
            topology_config['parameters'] = {'arms': 2, 'phase_shift': 180}
        elif topology_type == 'nested_spiral':
            topology_config['parameters'] = {'layers': 3, 'scale_factor': 0.5}
        elif topology_type == 'interwoven_spiral':
            topology_config['parameters'] = {'strands': 2, 'twist_rate': 0.1}
        elif topology_type == 'fractal_spiral':
            topology_config['parameters'] = {'iterations': 5, 'self_similarity': 0.8}
        else:
            topology_config['parameters'] = {'custom': True}
        
        return topology_config
    
    def expand_dimensions(self):
        """维度无限扩展"""
        # 从3D螺旋扩展到更高维度
        for dim in range(3, 11):  # 限制到10维以避免无限循环
            higher_dim_config = self.project_to_higher_dimension(dim)
            self.expansion_stats['dimensional_expansions'] += 1
            yield higher_dim_config
    
    def project_to_higher_dimension(self, dimension):
        """投影到更高维度"""
        # 生成高维配置
        high_dim_config = {
            'dimension': dimension,
            'projection_method': 'spiral_hyperplane',
            'basis_vectors': [],
            'parameters': {}
        }
        
        # 生成基向量
        for i in range(dimension):
            basis_vector = [0] * dimension
            basis_vector[i] = 1
            high_dim_config['basis_vectors'].append(basis_vector)
        
        # 设置高维参数
        high_dim_config['parameters'] = {
            'curvature': 1.0 / dimension,
            'torsion': 1.0 / (dimension * 2),
            'scaling': 1.0
        }
        
        return high_dim_config
    
    def expand_temporally(self, start_time=None, end_time=None):
        """时间扩展：向过去和未来无限延伸"""
        # 时间序列生成
        temporal_expansions = []
        
        # 生成过去时间点
        past_times = generate_infinite_sequence(-1, -1)  # 步长为-1，向过去延伸
        # 生成未来时间点
        future_times = generate_infinite_sequence(1, 1)   # 步长为1，向未来延伸
        
        # 生成时间点（实际实现中需要限制数量）
        for i in range(100):  # 限制为100个时间点
            try:
                past_time = next(past_times)
                future_time = next(future_times)
                
                temporal_expansions.append(('past', past_time))
                temporal_expansions.append(('future', future_time))
                
                self.expansion_stats['temporal_expansions'] += 2
            except StopIteration:
                break
        
        return temporal_expansions
    
    def expand(self, expansion_type, **kwargs):
        """通用扩展方法"""
        if expansion_type == 'parametric':
            return self.expand_parametric(**kwargs)
        elif expansion_type == 'topological':
            return list(self.expand_topological())
        elif expansion_type == 'dimensional':
            return list(self.expand_dimensions())
        elif expansion_type == 'temporal':
            return self.expand_temporally(**kwargs)
        else:
            raise ValueError(f"Unknown expansion type: {expansion_type}")
    
    def enable_expansion(self, dimension, enable=True):
        """启用或禁用特定维度的扩展"""
        if dimension in self.expansion_dimensions:
            self.expansion_dimensions[dimension] = enable
    
    def is_expansion_enabled(self, dimension):
        """检查特定维度的扩展是否启用"""
        return self.expansion_dimensions.get(dimension, False)
    
    def get_expansion_stats(self):
        """获取扩展统计信息"""
        return self.expansion_stats
    
    def reset_expansion_stats(self):
        """重置扩展统计信息"""
        self.expansion_stats = {
            'parametric_expansions': 0,
            'topological_expansions': 0,
            'dimensional_expansions': 0,
            'temporal_expansions': 0
        }
    
    def __str__(self):
        """字符串表示"""
        stats = self.get_expansion_stats()
        return f"InfiniteExpansionEngine(topo_expansions={stats['topological_expansions']}, dim_expansions={stats['dimensional_expansions']})"
    
    def __repr__(self):
        """官方字符串表示"""
        return self.__str__()
