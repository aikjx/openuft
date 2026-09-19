import unittest
from helical_db.core.helical_spacetime_database import HelicalSpacetimeDatabase
from helical_db.core.helical_quantum import HelicalQuantum

class TestHelicalSpacetimeDatabase(unittest.TestCase):
    """测试螺旋时空数据库"""
    
    def setUp(self):
        """设置测试环境"""
        self.db = HelicalSpacetimeDatabase()
    
    def test_insert(self):
        """测试插入功能"""
        # 测试插入简单数据
        test_data = {'name': 'test', 'value': 123}
        quantum_id = self.db.insert(test_data)
        
        # 验证插入成功
        self.assertIsNotNone(quantum_id)
        self.assertEqual(len(quantum_id), 36)  # UUID长度
    
    def test_query(self):
        """测试查询功能"""
        # 插入测试数据
        test_data = {'name': 'test', 'value': 123}
        self.db.insert(test_data)
        
        # 测试瞬间查询
        results = self.db.query({}, mode='instant')
        self.assertGreater(len(results), 0)
    
    def test_create_sub_database(self):
        """测试创建子数据库"""
        # 插入测试数据
        for i in range(10):
            test_data = {'name': f'test_{i}', 'value': i}
            self.db.insert(test_data)
        
        # 创建子数据库
        def filter_func(quantum):
            return quantum.data.get('value', 0) > 5
        
        sub_db = self.db.create_sub_database(filter_func)
        self.assertIsNotNone(sub_db)
        self.assertIn('id', sub_db)
        self.assertIn('storage', sub_db)
    
    def test_expand(self):
        """测试扩展功能"""
        # 测试参数扩展
        parametric_expansions = self.db.expand('parametric')
        self.assertGreater(len(parametric_expansions), 0)
        
        # 测试拓扑扩展
        topological_expansions = list(self.db.expand('topological'))
        self.assertGreater(len(topological_expansions), 0)
        
        # 测试维度扩展
        dimensional_expansions = list(self.db.expand('dimensional'))
        self.assertGreater(len(dimensional_expansions), 0)
        
        # 测试时间扩展
        temporal_expansions = self.db.expand('temporal')
        self.assertGreater(len(temporal_expansions), 0)
    
    def test_add_node(self):
        """测试添加分布式节点"""
        node = self.db.add_node()
        self.assertIsNotNone(node)
        self.assertIn('id', node.__dict__)
    
    def test_get_stats(self):
        """测试获取统计信息"""
        stats = self.db.get_stats()
        self.assertIsNotNone(stats)
        self.assertIn('db_stats', stats)
        self.assertIn('storage_stats', stats)
        self.assertIn('query_stats', stats)
        self.assertIn('association_stats', stats)
        self.assertIn('distributed_stats', stats)
        self.assertIn('expansion_stats', stats)
    
    def test_clear(self):
        """测试清空数据库"""
        # 插入测试数据
        self.db.insert({'name': 'test', 'value': 123})
        
        # 清空数据库
        self.db.clear()
        
        # 验证清空成功
        stats = self.db.get_stats()
        self.assertEqual(stats['db_stats']['total_inserts'], 0)

class TestHelicalQuantum(unittest.TestCase):
    """测试螺旋量子"""
    
    def test_create(self):
        """测试创建螺旋量子"""
        test_data = {'name': 'test', 'value': 123}
        quantum = HelicalQuantum(test_data)
        
        # 验证量子创建成功
        self.assertIsNotNone(quantum)
        self.assertIsNotNone(quantum.id)
        self.assertEqual(quantum.data, test_data)
    
    def test_get_coordinates(self):
        """测试获取坐标"""
        quantum = HelicalQuantum({'name': 'test'})
        coords = quantum.get_coordinates()
        
        # 验证坐标是三维的
        self.assertEqual(len(coords), 3)
        for coord in coords:
            self.assertIsInstance(coord, (int, float))
    
    def test_get_params(self):
        """测试获取参数"""
        quantum = HelicalQuantum({'name': 'test'})
        params = quantum.get_params()
        
        # 验证参数包含必要字段
        self.assertIn('r', params)
        self.assertIn('ω', params)
        self.assertIn('p', params)
        self.assertIn('t', params)

if __name__ == '__main__':
    unittest.main()
