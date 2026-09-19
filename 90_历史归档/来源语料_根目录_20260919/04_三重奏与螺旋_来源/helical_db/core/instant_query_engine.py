import math
from helical_db.config.constants import GRID_SIZE
from helical_db.utils.helpers import project_to_2d

class InstantQueryEngine:
    """瞬间查询引擎 - 基于二维世界投影实现O(1)查询"""
    
    def __init__(self, storage):
        """
        初始化瞬间查询引擎
        
        Args:
            storage: InfiniteStorage实例
        """
        self.storage = storage
        # 创建二维查询平面
        self.query_plane = self.create_2d_plane()
        
        # 查询统计
        self.query_stats = {
            'total_queries': 0,
            'average_query_time': 0,
            'last_query_time': 0
        }
    
    def create_2d_plane(self):
        """将三维螺旋投影到二维平面"""
        plane = {}
        
        # 获取所有量子
        quanta = self.storage.get_all_quanta()
        
        for quantum in quanta:
            # 投影到二维平面
            x_2d, y_2d = project_to_2d(quantum.get_coordinates())
            
            # 在二维平面建立网格索引
            cell_x = int(x_2d / GRID_SIZE)
            cell_y = int(y_2d / GRID_SIZE)
            cell_key = f"{cell_x}:{cell_y}"
            
            if cell_key not in plane:
                plane[cell_key] = []
            plane[cell_key].append(quantum)
        
        return plane
    
    def update_query_plane(self):
        """更新查询平面"""
        self.query_plane = self.create_2d_plane()
    
    def instant_query(self, query_params):
        """瞬间查询：在二维平面直接定位"""
        import time
        start_time = time.time()
        
        # 1. 如果查询平面为空，重新创建
        if not self.query_plane:
            self.update_query_plane()
        
        # 2. 将查询条件投影到二维
        query_2d = self.project_to_2d(query_params)
        
        # 3. 在二维网格中直接定位（O(1)时间复杂度）
        target_cell = self.locate_cell(query_2d)
        
        # 4. 返回该网格所有数据
        results = self.query_plane.get(target_cell, [])
        
        # 5. 如果结果为空，尝试获取所有量子
        if not results:
            results = self.storage.get_all_quanta()
        
        # 6. 如果需要三维精度，进行微调
        if query_params.get('need_3d_precision'):
            results = self.refine_3d(results, query_params)
        
        # 7. 更新查询统计
        query_time = time.time() - start_time
        self.query_stats['total_queries'] += 1
        self.query_stats['last_query_time'] = query_time
        
        # 更新平均查询时间
        if self.query_stats['total_queries'] == 1:
            self.query_stats['average_query_time'] = query_time
        else:
            self.query_stats['average_query_time'] = (
                self.query_stats['average_query_time'] * (self.query_stats['total_queries'] - 1) + 
                query_time
            ) / self.query_stats['total_queries']
        
        return results
    
    def project_to_2d(self, query):
        """将任意查询降维到二维"""
        # 根据统一场论：光速运动时，一维空间长度缩短为零
        # 因此我们可以安全地忽略一个维度
        
        if 'x' in query and 'y' in query:
            # 直接使用x,y坐标
            return {'x': query['x'], 'y': query['y']}
        elif 'r' in query and 'ω' in query:
            # 从螺旋参数计算二维坐标
            t = query.get('t', 0)
            x = query['r'] * math.cos(query['ω'] * t)
            y = query['r'] * math.sin(query['ω'] * t)
            return {'x': x, 'y': y}
        elif 'coordinates' in query:
            # 使用完整坐标
            x, y, z = query['coordinates']
            return {'x': x, 'y': y}
        else:
            # 默认返回原点
            return {'x': 0, 'y': 0}
    
    def locate_cell(self, query_2d):
        """在二维平面中定位网格单元"""
        x = query_2d.get('x', 0)
        y = query_2d.get('y', 0)
        
        # 计算网格坐标
        cell_x = int(x / GRID_SIZE)
        cell_y = int(y / GRID_SIZE)
        
        return f"{cell_x}:{cell_y}"
    
    def refine_3d(self, results, query_params):
        """对查询结果进行三维精度微调"""
        refined_results = []
        
        for quantum in results:
            # 检查三维条件
            if self.matches_3d_conditions(quantum, query_params):
                refined_results.append(quantum)
        
        return refined_results
    
    def matches_3d_conditions(self, quantum, query_params):
        """检查量子是否满足三维查询条件"""
        # 检查z坐标条件
        if 'z' in query_params:
            z_condition = query_params['z']
            if isinstance(z_condition, (int, float)):
                # 精确匹配
                if not math.isclose(quantum.z, z_condition, rel_tol=1e-6):
                    return False
            elif isinstance(z_condition, dict):
                # 范围匹配
                if 'min' in z_condition and quantum.z < z_condition['min']:
                    return False
                if 'max' in z_condition and quantum.z > z_condition['max']:
                    return False
        
        # 检查其他三维条件
        if 't' in query_params:
            t_condition = query_params['t']
            if isinstance(t_condition, (int, float)):
                if not math.isclose(quantum.t, t_condition, rel_tol=1e-6):
                    return False
            elif isinstance(t_condition, dict):
                if 'min' in t_condition and quantum.t < t_condition['min']:
                    return False
                if 'max' in t_condition and quantum.t > t_condition['max']:
                    return False
        
        return True
    
    def batch_query(self, query_params_list):
        """批量查询"""
        results = []
        
        for query_params in query_params_list:
            query_results = self.instant_query(query_params)
            results.extend(query_results)
        
        # 去重
        unique_results = []
        seen_ids = set()
        
        for quantum in results:
            if quantum.id not in seen_ids:
                seen_ids.add(quantum.id)
                unique_results.append(quantum)
        
        return unique_results
    
    def range_query(self, min_coords, max_coords):
        """范围查询"""
        # 计算查询范围覆盖的网格
        min_x, min_y, min_z = min_coords
        max_x, max_y, max_z = max_coords
        
        # 计算网格范围
        start_cell_x = int(min_x / GRID_SIZE)
        end_cell_x = int(max_x / GRID_SIZE)
        start_cell_y = int(min_y / GRID_SIZE)
        end_cell_y = int(max_y / GRID_SIZE)
        
        results = []
        
        # 遍历所有相关网格
        for cell_x in range(start_cell_x, end_cell_x + 1):
            for cell_y in range(start_cell_y, end_cell_y + 1):
                cell_key = f"{cell_x}:{cell_y}"
                if cell_key in self.query_plane:
                    cell_results = self.query_plane[cell_key]
                    # 过滤出在三维范围内的结果
                    for quantum in cell_results:
                        if (min_x <= quantum.x <= max_x and 
                            min_y <= quantum.y <= max_y and 
                            min_z <= quantum.z <= max_z):
                            results.append(quantum)
        
        return results
    
    def get_query_stats(self):
        """获取查询统计信息"""
        return self.query_stats
    
    def clear_query_stats(self):
        """清空查询统计信息"""
        self.query_stats = {
            'total_queries': 0,
            'average_query_time': 0,
            'last_query_time': 0
        }
    
    def __str__(self):
        """字符串表示"""
        stats = self.get_query_stats()
        return f"InstantQueryEngine(cells={len(self.query_plane)}, avg_time={stats['average_query_time']:.6f}s)"
    
    def __repr__(self):
        """官方字符串表示"""
        return self.__str__()
