from unified_field_visualizer import SpiralSpacetimeVisualizer

print("测试 SpiralSpacetimeVisualizer...")
try:
    viz = SpiralSpacetimeVisualizer()
    print("创建可视化器成功")
    
    figs = viz.visualize()
    print(f"可视化成功，生成了 {len(figs)} 个图形")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()