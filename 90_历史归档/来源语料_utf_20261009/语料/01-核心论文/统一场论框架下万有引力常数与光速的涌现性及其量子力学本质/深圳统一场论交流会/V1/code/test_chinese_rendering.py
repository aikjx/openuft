import matplotlib.pyplot as plt
import os

# 测试不同的中文配置
configs = [
    {
        'name': '配置1 - 基础中文设置',
        'rcParams': {
            'font.family': ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans'],
            'axes.unicode_minus': False,
            'font.size': 12,
        }
    },
    {
        'name': '配置2 - 仅系统字体',
        'rcParams': {
            'font.family': ['sans-serif'],
            'font.sans-serif': ['Microsoft YaHei', 'SimHei', 'sans-serif'],
            'axes.unicode_minus': False,
            'font.size': 12,
        }
    }
]

# 确保输出目录存在
code_dir = os.path.dirname(os.path.abspath(__file__))
test_dir = os.path.join(code_dir, 'test_output')
os.makedirs(test_dir, exist_ok=True)

# 中文测试文本
chinese_texts = [
    '空间光速螺旋运动',
    '引力场强度随距离变化',
    'G的量子几何起源',
    '质量与空间位移矢量条数关系',
    '普朗克质量',
    '地球质量',
    '普通人质量',
    '趋势线: n = 1.00e+00 m^1.00',
]

# 测试每个配置
for config in configs:
    print(f"\n测试: {config['name']}")
    plt.rcParams.clear()
    plt.rcParams.update(config['rcParams'])
    
    # 创建测试图表
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制简单曲线
    x = list(range(len(chinese_texts)))
    y = [i**2 for i in x]
    ax.plot(x, y, 'b-', linewidth=2, label='测试曲线')
    
    # 添加中文标签到图表
    for i, text in enumerate(chinese_texts):
        ax.annotate(text, (x[i], y[i]), xytext=(5, 5), textcoords='offset points',
                   fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # 设置中文标题和标签
    ax.set_title('中文渲染测试', fontsize=16, pad=20)
    ax.set_xlabel('X轴标签（中文）', fontsize=12, labelpad=10)
    ax.set_ylabel('Y轴标签（中文）', fontsize=12, labelpad=10)
    ax.legend()
    
    # 保存测试图表
    output_path = os.path.join(test_dir, f'chinese_test_{config["name"].replace(" ", "_").replace("- ", "")}.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ 测试图表已保存: {output_path}")
    
    # 检查字体是否可用
    from matplotlib.font_manager import findfont, FontProperties
    print("\n可用字体检查:")
    for font_name in config['rcParams'].get('font.sans-serif', config['rcParams'].get('font.family', [])):
        try:
            font = findfont(FontProperties(family=[font_name]))
            print(f"✓ 字体 '{font_name}' 可用: {font}")
        except Exception as e:
            print(f"✗ 字体 '{font_name}' 不可用: {e}")

print("\n所有测试完成！")
print(f"测试结果保存在: {test_dir}")
