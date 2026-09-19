import time
import random
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from helical_db.core.helical_spacetime_database import HelicalSpacetimeDatabase

def test_insert_performance():
    """测试插入性能"""
    db = HelicalSpacetimeDatabase()
    test_count = 1000
    
    print(f"测试插入性能：{test_count} 条数据")
    start_time = time.time()
    
    for i in range(test_count):
        test_data = {
            'id': i,
            'name': f'test_{i}',
            'value': random.randint(0, 1000),
            'timestamp': time.time()
        }
        db.insert(test_data)
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / test_count
    
    print(f"总插入时间：{total_time:.4f} 秒")
    print(f"平均插入时间：{avg_time:.6f} 秒")
    print(f"插入速度：{test_count / total_time:.2f} 条/秒")
    
    return total_time

def test_query_performance():
    """测试查询性能"""
    db = HelicalSpacetimeDatabase()
    
    # 先插入测试数据
    test_count = 1000
    for i in range(test_count):
        test_data = {
            'id': i,
            'name': f'test_{i}',
            'value': random.randint(0, 1000),
            'timestamp': time.time()
        }
        db.insert(test_data)
    
    # 测试查询性能
    query_count = 100
    print(f"\n测试查询性能：{query_count} 次查询")
    start_time = time.time()
    
    for i in range(query_count):
        # 随机查询条件
        query_conditions = {
            'x': random.uniform(-100, 100),
            'y': random.uniform(-100, 100)
        }
        db.query(query_conditions, mode='instant')
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / query_count
    
    print(f"总查询时间：{total_time:.4f} 秒")
    print(f"平均查询时间：{avg_time:.6f} 秒")
    print(f"查询速度：{query_count / total_time:.2f} 次/秒")
    
    return total_time

def test_expansion_performance():
    """测试扩展性能"""
    db = HelicalSpacetimeDatabase()
    
    print("\n测试扩展性能")
    
    # 测试参数扩展
    start_time = time.time()
    parametric_expansions = db.expand('parametric')
    parametric_time = time.time() - start_time
    print(f"参数扩展时间：{parametric_time:.4f} 秒，生成 {len(parametric_expansions)} 个组合")
    
    # 测试拓扑扩展
    start_time = time.time()
    topological_expansions = list(db.expand('topological'))
    topological_time = time.time() - start_time
    print(f"拓扑扩展时间：{topological_time:.4f} 秒，生成 {len(topological_expansions)} 个拓扑")
    
    # 测试维度扩展
    start_time = time.time()
    dimensional_expansions = list(db.expand('dimensional'))
    dimensional_time = time.time() - start_time
    print(f"维度扩展时间：{dimensional_time:.4f} 秒，生成 {len(dimensional_expansions)} 个维度配置")
    
    # 测试时间扩展
    start_time = time.time()
    temporal_expansions = db.expand('temporal')
    temporal_time = time.time() - start_time
    print(f"时间扩展时间：{temporal_time:.4f} 秒，生成 {len(temporal_expansions)} 个时间点")
    
    return parametric_time + topological_time + dimensional_time + temporal_time

if __name__ == '__main__':
    print("=== 螺旋时空数据库性能测试 ===")
    
    # 测试插入性能
    insert_time = test_insert_performance()
    
    # 测试查询性能
    query_time = test_query_performance()
    
    # 测试扩展性能
    expansion_time = test_expansion_performance()
    
    print("\n=== 性能测试完成 ===")
    print(f"总测试时间：{insert_time + query_time + expansion_time:.4f} 秒")
