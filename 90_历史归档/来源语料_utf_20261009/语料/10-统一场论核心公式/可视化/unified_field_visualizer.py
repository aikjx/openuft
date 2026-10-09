import os
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any, Union

class UnifiedFieldVisualizer(ABC):
    """
    统一场论核心公式可视化基类
    为所有核心公式的可视化提供标准化的框架和接口
    """
    
    def __init__(self, formula_name: str, formula_equation: str):
        """
        初始化可视化器
        
        Args:
            formula_name: 公式名称
            formula_equation: 公式的数学表达式
        """
        self.formula_name = formula_name
        self.formula_equation = formula_equation
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(self.base_dir, 'img')
        self._setup_environment()
    
    def _setup_environment(self):
        """设置绘图环境和目录结构"""
        # 确保img目录存在
        os.makedirs(self.img_dir, exist_ok=True)
        
        # 设置中文字体
        plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
        plt.rcParams["axes.unicode_minus"] = False
        plt.rcParams["text.usetex"] = False
        plt.rcParams["mathtext.fontset"] = "cm"
        
        # 额外的字体设置
        plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
        plt.rcParams['axes.unicode_minus'] = False
    
    @abstractmethod
    def visualize(self) -> List[plt.Figure]:
        """
        核心可视化方法，子类必须实现
        
        Returns:
            生成的所有图形对象列表
        """
        pass
    
    def _save_figure(self, fig: plt.Figure, filename: str) -> str:
        """
        保存图形到文件
        
        Args:
            fig: 图形对象
            filename: 文件名（不含路径）
        
        Returns:
            保存的文件路径
        """
        filepath = os.path.join(self.img_dir, filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        return filepath
    
    def _add_formula_text(self, fig: plt.Figure, position: Tuple[float, float] = (0.5, 0.01)):
        """
        在图形中添加公式文本
        
        Args:
            fig: 图形对象
            position: 文本位置，默认在底部中央
        """
        fig.text(
            position[0], position[1],
            f"{self.formula_name}: {self.formula_equation}",
            ha='center', fontsize=14,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6)
        )
    
    def _add_parameter_explanation(self, fig: plt.Figure, explanation: str):
        """
        在图形中添加参数解释文本框
        
        Args:
            fig: 图形对象
            explanation: 参数解释文本
        """
        fig.text(
            0.02, 0.02,
            explanation,
            fontsize=10,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
    
    def _create_subplots(self, rows: int, cols: int, figsize: Tuple[int, int] = (12, 10)) -> Tuple[plt.Figure, np.ndarray]:
        """
        创建标准化的子图布局
        
        Args:
            rows: 行数
            cols: 列数
            figsize: 图形大小
        
        Returns:
            图形对象和子图数组
        """
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        fig.suptitle(self.formula_name, fontsize=16)
        return fig, axes
    
    def _ensure_directory(self, directory: str):
        """
        确保目录存在
        
        Args:
            directory: 目录路径
        """
        os.makedirs(directory, exist_ok=True)
    
    def _get_figure_size(self, complexity: str = 'medium') -> Tuple[int, int]:
        """
        根据复杂度获取合适的图形大小
        
        Args:
            complexity: 复杂度级别 ('simple', 'medium', 'complex')
        
        Returns:
            图形大小元组
        """
        size_map = {
            'simple': (10, 6),
            'medium': (12, 10),
            'complex': (15, 12)
        }
        return size_map.get(complexity, (12, 10))
    
    def run(self) -> List[str]:
        """
        运行完整的可视化流程
        
        Returns:
            保存的文件路径列表
        """
        try:
            figures = self.visualize()
            saved_files = []
            
            for i, fig in enumerate(figures):
                filename = f"{self.formula_name}_{i+1}.png"
                saved_path = self._save_figure(fig, filename)
                saved_files.append(saved_path)
                plt.close(fig)  # 释放内存
            
            print(f"✓ {self.formula_name} 可视化完成，保存了 {len(saved_files)} 个文件")
            return saved_files
            
        except Exception as e:
            print(f"✗ {self.formula_name} 可视化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    @staticmethod
    def _safe_divide(numerator: Union[float, np.ndarray], denominator: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        安全除法，避免除零错误
        
        Args:
            numerator: 分子
            denominator: 分母
        
        Returns:
            除法结果
        """
        if isinstance(denominator, np.ndarray):
            denominator_safe = np.maximum(denominator, 1e-10)
        else:
            denominator_safe = max(denominator, 1e-10)
        return numerator / denominator
    
    @staticmethod
    def _calculate_vector_magnitude(vectors: np.ndarray) -> np.ndarray:
        """
        计算矢量的大小
        
        Args:
            vectors: 形状为 (N, 3) 的矢量数组
        
        Returns:
            大小数组，形状为 (N,)
        """
        return np.linalg.norm(vectors, axis=1)


class SpiralSpacetimeVisualizer(UnifiedFieldVisualizer):
    """
    三维螺旋时空方程可视化器
    方程: r(t) = r cos(ω t) i + r sin(ω t) j + h t k
    """
    
    def __init__(self):
        super().__init__(
            "三维螺旋时空方程",
            "r(t) = r cos(ω t) i + r sin(ω t) j + h t k"
        )
    
    def visualize(self) -> List[plt.Figure]:
        """可视化三维螺旋时空方程"""
        figures = []
        
        # 1. 基础螺旋轨迹可视化
        fig1 = self._visualize_spiral_trajectory()
        figures.append(fig1)
        
        # 2. 速度分量分析
        fig2 = self._visualize_velocity_components()
        figures.append(fig2)
        
        # 3. 三维立体可视化
        fig3 = self._visualize_3d_spiral()
        figures.append(fig3)
        
        return figures
    
    def _visualize_spiral_trajectory(self) -> plt.Figure:
        """可视化螺旋运动轨迹"""
        t = np.linspace(0, 4*np.pi, 100)
        r, w, h = 2, 1, 0.3
        
        x = r * np.cos(w*t)
        y = r * np.sin(w*t)
        z = h * t
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.plot(x, y, z, 'b-', linewidth=2, label='运动轨迹')
        ax.quiver(0, 0, 0, r, 0, 0, color='r', linewidth=2, label='基矢量 i')
        ax.quiver(0, 0, 0, 0, r, 0, color='g', linewidth=2, label='基矢量 j')
        ax.quiver(0, 0, 0, 0, 0, h*4*np.pi, color='k', linewidth=2, label='基矢量 k')
        
        ax.set_xlabel('X轴')
        ax.set_ylabel('Y轴')
        ax.set_zlabel('Z轴')
        ax.set_title('三维螺旋时空方程 - 螺旋运动轨迹', fontsize=14)
        ax.legend()
        
        self._add_formula_text(fig)
        self._add_parameter_explanation(fig, self._get_spiral_explanation())
        
        return fig
    
    def _visualize_velocity_components(self) -> plt.Figure:
        """可视化速度分量"""
        t = np.linspace(0, 4*np.pi, 100)
        r, w, h = 2, 1, 0.3
        
        # 位置
        x = r * np.cos(w*t)
        y = r * np.sin(w*t)
        z = h * t
        
        # 速度分量
        vx = -r * w * np.sin(w*t)
        vy = r * w * np.cos(w*t)
        vz = np.full_like(t, h)
        
        # 速度大小
        v_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
        
        fig, axes = self._create_subplots(2, 2, figsize=(15, 12))
        
        # 速度分量随时间变化
        axes[0, 0].plot(t, vx, 'r-', linewidth=2, label='Vx')
        axes[0, 0].plot(t, vy, 'g-', linewidth=2, label='Vy')
        axes[0, 0].plot(t, vz, 'b-', linewidth=2, label='Vz')
        axes[0, 0].set_title('速度分量随时间变化', fontsize=14)
        axes[0, 0].set_xlabel('时间 t')
        axes[0, 0].set_ylabel('速度分量')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 速度大小随时间变化
        axes[0, 1].plot(t, v_magnitude, 'k-', linewidth=2)
        axes[0, 1].set_title('速度大小随时间变化', fontsize=14)
        axes[0, 1].set_xlabel('时间 t')
        axes[0, 1].set_ylabel('速度大小')
        axes[0, 1].grid(True, alpha=0.3)
        
        # XY平面投影
        axes[1, 0].plot(x, y, 'b-', linewidth=2)
        axes[1, 0].set_title('XY平面投影 (圆周运动)', fontsize=14)
        axes[1, 0].set_xlabel('X坐标')
        axes[1, 0].set_ylabel('Y坐标')
        axes[1, 0].set_aspect('equal')
        axes[1, 0].grid(True, alpha=0.3)
        
        # XZ平面投影
        axes[1, 1].plot(x, z, 'b-', linewidth=2)
        axes[1, 1].set_title('XZ平面投影', fontsize=14)
        axes[1, 1].set_xlabel('X坐标')
        axes[1, 1].set_ylabel('Z坐标')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_3d_spiral(self) -> plt.Figure:
        """创建更高级的3D螺旋可视化"""
        t = np.linspace(0, 6*np.pi, 200)
        r, w, h = 2, 1, 0.3
        
        x = r * np.cos(w*t)
        y = r * np.sin(w*t)
        z = h * t
        
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制螺旋线
        ax.plot(x, y, z, 'b-', linewidth=2.5, label='螺旋轨迹')
        
        # 添加时间点标记
        time_points = [0, np.pi, 2*np.pi, 3*np.pi, 4*np.pi, 5*np.pi, 6*np.pi]
        for i, tp in enumerate(time_points):
            idx = int(tp / (6*np.pi) * (len(t)-1))  # 使用 len(t)-1 避免索引越界
            ax.scatter(x[idx], y[idx], z[idx], color='red', s=100, zorder=5)
            ax.text(x[idx]+0.2, y[idx]+0.2, z[idx]+0.2, f't={tp:.1f}', fontsize=10)
        
        # 设置视角
        ax.view_init(elev=30, azim=45)
        
        ax.set_xlabel('X轴')
        ax.set_ylabel('Y轴')
        ax.set_zlabel('Z轴')
        ax.set_title('三维螺旋时空方程 - 高级3D可视化', fontsize=14)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig
    
    def _get_spiral_explanation(self) -> str:
        """获取螺旋时空方程的参数解释"""
        return (
            f"{self.formula_name} 参数详解:\n"
            f"{self.formula_equation}\n\n"
            "参数含义:\n"
            "- r(t): 位置矢量\n"
            "- r: 螺旋半径（常数）\n"
            "- ω: 角速度\n"
            "- h: 轴向移动系数\n"
            "- t: 时间变量\n"
            "- i, j, k: X、Y、Z轴的单位矢量\n\n"
            "物理意义:\n"
            "- XY平面分量构成匀速圆周运动\n"
            "- Z轴分量构成匀速直线运动\n"
            "- 两者合成形成空间螺旋运动轨迹\n"
            "- 这是统一场论中描述时空本质的核心方程\n"
            "- 揭示了空间运动的螺旋本质"
        )


if __name__ == "__main__":
    # 测试基类功能
    print("统一场论可视化框架基类创建完成")
    print("开始测试三维螺旋时空方程可视化...")
    
    visualizer = SpiralSpacetimeVisualizer()
    files = visualizer.run()
    print(f"测试完成，保存的文件: {files}")