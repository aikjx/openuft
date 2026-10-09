import os
import sys
import importlib
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any

# 设置全局中文字体和绘图参数
plt.rcParams.update({
    "font.family": ["SimHei", "Microsoft YaHei", "SimSun", "Arial"],
    "axes.unicode_minus": False,
    "text.usetex": False,
    "mathtext.fontset": "cm",
    "font.sans-serif": ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC'],
    "figure.figsize": (12, 10),
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12
})

class FormulaVisualizationManager:
    """
    统一场论公式可视化管理器
    负责生成所有公式的教科书级别可视化
    """
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, "textbook_visualizations")
        self.formula_directories = self._get_formula_directories()
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("=" * 60)
        print("统一场论公式教科书级别可视化管理器")
        print(f"基础目录: {self.base_dir}")
        print(f"输出目录: {self.output_dir}")
        print(f"发现 {len(self.formula_directories)} 个公式目录")
        print("=" * 60)
    
    def _get_formula_directories(self) -> List[str]:
        """
        获取所有公式目录
        """
        formula_dirs = []
        for item in os.listdir(self.base_dir):
            item_path = os.path.join(self.base_dir, item)
            if os.path.isdir(item_path) and (item.startswith("0") or item.startswith("1")):
                formula_dirs.append(item_path)
        return sorted(formula_dirs)
    
    def _load_formula_visualizer(self, formula_dir: str) -> Any:
        """
        加载指定公式目录中的可视化模块
        """
        try:
            # 查找可视化文件
            visualizer_files = []
            for file in os.listdir(formula_dir):
                if file.endswith(".py") and not file.startswith("__"):
                    visualizer_files.append(file)
            
            if not visualizer_files:
                return None
            
            # 选择主可视化文件（优先选择1.py或main.py）
            main_file = None
            for file in visualizer_files:
                if file in ["1.py", "main.py"]:
                    main_file = file
                    break
            if not main_file:
                main_file = visualizer_files[0]
            
            file_path = os.path.join(formula_dir, main_file)
            print(f"  加载可视化文件: {file_path}")
            
            # 动态导入模块
            module_name = f"visualizer_{os.path.basename(formula_dir)}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            return module
            
        except Exception as e:
            print(f"  加载可视化模块失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_textbook_visualization(self, formula_name: str, formula_eq: str):
        """
        创建标准化的教科书级别可视化模板
        """
        fig = plt.figure(figsize=(14, 12))
        
        # 添加标题
        plt.title(f"{formula_name}", fontsize=18, fontweight='bold', pad=20)
        
        # 添加公式
        plt.figtext(0.5, 0.01, f"公式: {formula_eq}", ha='center', fontsize=16, 
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        return fig
    
    def generate_all_visualizations(self):
        """
        生成所有公式的教科书级别可视化
        """
        import importlib
        
        for formula_dir in self.formula_directories:
            formula_name = os.path.basename(formula_dir)
            print(f"\n正在处理: {formula_name}")
            
            # 加载可视化模块
            module = self._load_formula_visualizer(formula_dir)
            if not module:
                print(f"  跳过 {formula_name}，无法加载可视化模块")
                continue
            
            # 根据模块类型执行可视化
            try:
                # 检查模块是否有可视化类或函数
                if hasattr(module, "MassDefinitionEquation"):
                    # 质量定义方程
                    visualizer = module.MassDefinitionEquation()
                    fig_2d = visualizer.visualize_2d()
                    fig_3d = visualizer.visualize_3d()
                    
                    # 保存可视化结果
                    output_subdir = os.path.join(self.output_dir, formula_name)
                    os.makedirs(output_subdir, exist_ok=True)
                    
                    fig_2d.savefig(os.path.join(output_subdir, f"{formula_name}_2D可视化.png"), 
                                  dpi=300, bbox_inches='tight')
                    fig_3d.savefig(os.path.join(output_subdir, f"{formula_name}_3D可视化.png"), 
                                  dpi=300, bbox_inches='tight')
                    
                    plt.close(fig_2d)
                    plt.close(fig_3d)
                    
                    print(f"  ✓ {formula_name} 可视化完成")
                    
                elif hasattr(module, "main"):
                    # 有main函数的模块
                    module.main()
                    print(f"  ✓ {formula_name} 可视化完成")
                    
                else:
                    # 尝试直接执行文件
                    exec(open(os.path.join(formula_dir, "1.py")).read())
                    print(f"  ✓ {formula_name} 可视化完成")
                    
            except Exception as e:
                print(f"  ✗ {formula_name} 可视化失败: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
    
    def create_unified_textbook(self):
        """
        创建统一的教科书级别可视化报告
        """
        print("\n" + "=" * 60)
        print("创建统一的教科书级别可视化报告")
        print("=" * 60)
        
        # 创建HTML报告
        html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>统一场论核心公式 - 教科书级别可视化</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: "SimHei", "Microsoft YaHei", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        
        h2 {
            color: #3498db;
            margin-top: 40px;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .formula-section {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 30px;
        }
        
        .formula-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .formula-equation {
            font-size: 1.3em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background-color: #e8f4f8;
            border-radius: 5px;
        }
        
        .visualization-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        }
        
        .visualization-item {
            flex: 1;
            min-width: 300px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .visualization-item img {
            width: 100%;
            height: auto;
            display: block;
        }
        
        .visualization-caption {
            padding: 15px;
            background-color: #f9f9f9;
            text-align: center;
            font-size: 0.9em;
        }
        
        .parameter-explanation {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
        
        .parameter-explanation h3 {
            margin-bottom: 10px;
            color: #3498db;
        }
        
        .parameter-explanation ul {
            margin-left: 20px;
        }
        
        .parameter-explanation li {
            margin-bottom: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>统一场论核心公式 - 教科书级别可视化</h1>
        
        <!-- 公式内容将动态生成 -->
        <div id="formula-content">
        
        <!-- 时空同一化方程 -->
        <div class="formula-section">
            <h2>1. 时空同一化方程</h2>
            <div class="formula-title">时空本质的数学表达</div>
            <div class="formula-equation">x = ct</div>
            <div class="parameter-explanation">
                <h3>参数说明</h3>
                <ul>
                    <li><strong>x</strong>: 空间坐标，描述物体在空间中的位置</li>
                    <li><strong>c</strong>: 光速，宇宙中信息传播的最大速度</li>
                    <li><strong>t</strong>: 时间坐标，描述事件发生的顺序</li>
                </ul>
                <h3>物理意义</h3>
                <p>时空同一化方程揭示了空间和时间的本质联系，它们是同一物理实体的不同表现形式。在高速运动或强引力场中，空间和时间会相互转化，这是相对论的核心思想。</p>
            </div>
            <div class="visualization-container">
                <div class="visualization-item">
                    <img src="01-时空同一化方程/matplotlib_visualization.html" alt="时空同一化方程可视化">
                    <div class="visualization-caption">时空同一化方程可视化</div>
                </div>
            </div>
        </div>
        
        <!-- 三维螺旋时空方程 -->
        <div class="formula-section">
            <h2>2. 三维螺旋时空方程</h2>
            <div class="formula-title">空间运动的螺旋本质</div>
            <div class="formula-equation">r(t) = r cos(ω t) i + r sin(ω t) j + h t k</div>
            <div class="parameter-explanation">
                <h3>参数说明</h3>
                <ul>
                    <li><strong>r(t)</strong>: 位置矢量，描述物体在三维空间中的运动轨迹</li>
                    <li><strong>r</strong>: 螺旋半径，描述圆周运动的规模</li>
                    <li><strong>ω</strong>: 角速度，描述圆周运动的快慢</li>
                    <li><strong>h</strong>: 轴向移动系数，描述轴向运动的速度</li>
                    <li><strong>t</strong>: 时间变量</li>
                    <li><strong>i, j, k</strong>: 三维空间的单位矢量</li>
                </ul>
                <h3>物理意义</h3>
                <p>三维螺旋时空方程描述了空间中物体运动的本质形式。所有物质在空间中都以螺旋轨迹运动，这是统一场论中空间基本属性的体现。螺旋运动的组合产生了我们观察到的各种物理现象。</p>
            </div>
        </div>
        
        <!-- 质量定义方程 -->
        <div class="formula-section">
            <h2>3. 质量定义方程</h2>
            <div class="formula-title">质量的空间本质</div>
            <div class="formula-equation">m = k · dn/dΩ</div>
            <div class="parameter-explanation">
                <h3>参数说明</h3>
                <ul>
                    <li><strong>m</strong>: 物体的质量，是物体惯性和引力属性的量度</li>
                    <li><strong>k</strong>: 比例常数，与空间基本属性相关的系数</li>
                    <li><strong>dn/dΩ</strong>: 单位立体角内的空间运动量变化率</li>
                    <li><strong>Ω</strong>: 立体角，描述空间方向的量度</li>
                </ul>
                <h3>物理意义</h3>
                <p>质量定义方程从空间几何角度重新定义了质量，揭示了质量是空间运动量分布特征的表现。质量并非物体的固有属性，而是空间运动效应的结果，这是统一场论的核心思想之一。</p>
            </div>
            <div class="visualization-container">
                <div class="visualization-item">
                    <img src="03质量定义方程/img/质量定义方程_2D可视化.png" alt="质量定义方程2D可视化">
                    <div class="visualization-caption">质量随立体角变化的2D可视化</div>
                </div>
                <div class="visualization-item">
                    <img src="03质量定义方程/img/质量定义方程_3D可视化.png" alt="质量定义方程3D可视化">
                    <div class="visualization-caption">质量在空间立体角上的3D分布</div>
                </div>
            </div>
        </div>
        
        </div>
    </div>
</body>
</html>
        """
        
        # 保存HTML报告
        html_path = os.path.join(self.output_dir, "textbook_visualizations.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n统一教科书级别可视化报告已生成: {html_path}")
    
    def run(self):
        """
        运行可视化管理器
        """
        print("开始生成所有公式的教科书级别可视化...")
        
        # 生成所有公式的可视化
        # self.generate_all_visualizations()
        
        # 生成统一的HTML报告
        self.generate_all_visualizations()
        self.create_unified_textbook()
        
        print("\n" + "=" * 60)
        print("所有可视化生成完成！")
        print(f"输出目录: {self.output_dir}")
        print("=" * 60)

if __name__ == "__main__":
    manager = FormulaVisualizationManager()
    manager.run()
